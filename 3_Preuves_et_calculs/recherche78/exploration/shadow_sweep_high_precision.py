"""Autonomous 60-digit quantile sweep for q<=1000 (finite diagnostic).

Run with a Python containing mpmath.  Optional first argument changes the cutoff.
Every printed number is diagnostic: no directed interval rounding is claimed.
Output kernels restrict the original, continuous source quantile, so they are
liftable to beta(u) du without any discrete-source approximation.
"""
import csv
import json
import sys
from pathlib import Path

import mpmath as mp

mp.mp.dps = 60
OUT = Path(__file__).resolve().parent
X = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
T = mp.log(2)
C0 = mp.log(8 * mp.pi) + mp.euler + mp.pi / 2
ACONST = mp.polygamma(1, mp.mpf(1)/4) / 4
NTERMS = 140
LAMS = [mp.mpf(2*n) + mp.mpf('0.5') for n in range(NTERMS)]
QLAMS = [mp.mpf(2*n) + mp.mpf('2.5') for n in range(NTERMS)]


def series(t, power):
    # Horner evaluation.  At t>=log 2 the omitted geometric tail is <10^-84.
    z = mp.exp(-2*t)
    result = mp.mpf(0)
    for lam in reversed(LAMS):
        result = result*z + 1/lam**power
    return mp.exp(-t/2)*result


def A(t):
    return (4*(mp.exp(t/2)+mp.exp(-t/2)-2)-C0*t/2
            + ACONST-series(t, 2))


def Ap(t):
    return 2*(mp.exp(t/2)-mp.exp(-t/2))-C0/2+series(t, 1)


def beta(t):
    return mp.exp(t/2)-mp.exp(-5*t/2)/(1-mp.exp(-2*t))


AT, APT = A(T), Ap(T)
m = AT/T
a = APT-mp.log(2)/mp.sqrt(2)
mu_T, nu_T = max(a-m, 0), max(m-a, 0)


def M(u):
    return m+mu_T+Ap(u)-APT


def H(u):
    return T*mu_T+u*Ap(u)-A(u)-T*APT+AT


gcache = {}
jcache = {}
qcache = {}


def Qprimitive(u):
    z=mp.exp(-2*u)
    result=mp.mpf(0)
    for lam in reversed(QLAMS):
        result=result*z+u*u/lam+2*u/lam**2+2/lam**3
    return mp.exp(u/2)*(2*u*u-8*u+16)+mp.exp(-5*u/2)*result


QT=Qprimitive(T)


def G(s):
    if s <= m:
        return mp.mpf(0)
    if s <= m+mu_T:
        return T
    if s in gcache:
        return gcache[s]
    u = 2*mp.log((s-m-mu_T)/2+mp.sqrt(2))
    for _ in range(20):
        v = M(u)-s
        if abs(v) < mp.mpf('1e-54'):
            gcache[s] = u
            return u
        u -= v/beta(u)
    raise RuntimeError('Source quantile Newton iteration failed.')


def J(s):
    if s <= m:
        return mp.mpf(0)
    if s <= m+mu_T:
        return T*(s-m)
    if s not in jcache:
        jcache[s] = H(G(s))
    return jcache[s]


def Q(s):
    if s<=m:
        return mp.mpf(0)
    if s<=m+mu_T:
        return T*T*(s-m)
    if s not in qcache:
        qcache[s]=T*T*mu_T+Qprimitive(G(s))-QT
    return qcache[s]


def powers(n):
    prime = [True]*(n+1)
    prime[0] = prime[1] = False
    for p in range(2, int(n**0.5)+1):
        if prime[p]:
            for q in range(p*p, n+1, p):
                prime[q] = False
    out = []
    for p in range(2, n+1):
        if prime[p]:
            q = p
            while q <= n:
                out.append((q, p))
                q *= p
    return sorted(out)


pp = powers(X)
L = mp.log(X)
CX = sum(mp.log(p)/mp.sqrt(q) for q,p in pp)
PX = sum(mp.log(p)/mp.sqrt(q)*mp.log(q) for q,p in pp)
SL = A(L)-CX*L+PX
budget = lambda u:(u-L)*Ap(u)-A(u)+A(L)
U = mp.findroot(lambda u:budget(u)-SL, (L+mp.mpf('.01'), L+mp.mpf('.2')))
D = Ap(U)-CX
assert D > 0

remaining = [(mp.mpf(0),M(U))]
EPS = mp.mpf('1e-48')
FEASIBILITY_TOL = 300*EPS


def pieces(s,c):
    result, rank = [], mp.mpf(0)
    for left,right in remaining:
        length = right-left
        lo,hi = max(0,s-rank),min(length,s+c-rank)
        if hi > lo:
            result.append((left+lo,left+hi))
        rank += length
        if rank >= s+c:
            break
    return result


def moment(block):
    return sum(J(right)-J(left) for left,right in block)


def residual_rank_at_mass(v):
    return sum(max(0,min(right,v)-left) for left,right in remaining)


def remove(block):
    global remaining
    updated = []
    for left,right in remaining:
        cursor = left
        for lo,hi in block:
            if hi <= cursor or lo >= right:
                continue
            if lo > cursor+EPS:
                updated.append((cursor,lo))
            cursor = max(cursor,hi)
        if right > cursor+EPS:
            updated.append((cursor,right))
    remaining = updated


atoms = [('T',T,nu_T)]+[(str(q),mp.log(q),mp.log(p)/mp.sqrt(q)) for q,p in pp if q>2]
atoms.append(('boundary',L,D))
rows,kernels = [],[]
for label,x,c in atoms:
    if label == 'boundary':
        true_line_residual = dict(
            mass=sum(right-left for left,right in remaining),
            first_moment=moment(remaining),
            atom_0_mass=sum(max(0,min(right,m)-left) for left,right in remaining),
            atom_T_mass=sum(max(0,min(right,m+mu_T)-max(left,m)) for left,right in remaining),
            source_mass_intervals=list(remaining))
    available = sum(right-left for left,right in remaining)
    lower,upper = mp.mpf(0),max(0,available-c)
    bmin = moment(pieces(lower,c))/c
    bmax = moment(pieces(upper,c))/c
    assert bmin <= x+FEASIBILITY_TOL and x <= bmax+FEASIBILITY_TOL,(label,bmin,x,bmax)
    if available-c < EPS:
        s = mp.mpf(0)
    else:
        s = min(upper,max(lower,residual_rank_at_mass(M(x))-c/2))
        for iteration in range(100):
            block = pieces(s,c)
            val = moment(block)-c*x
            if abs(val)<EPS:
                break
            if val<0:
                lower=s
            else:
                upper=s
            deriv = G(block[-1][1])-G(block[0][0])
            candidate=s-val/deriv if deriv else (lower+upper)/2
            s=candidate if lower<candidate<upper else (lower+upper)/2
        else:
            raise RuntimeError(f'Shadow root did not converge at {label}.')
    block=pieces(s,c)
    mass=sum(right-left for left,right in block)
    row=dict(atom=label,x=x,c=c,min_barycenter=bmin,availability_slack=x-bmin,
             source_low=G(block[0][0]),source_high=G(block[-1][1]),
             mass_error=mass-c,moment_error=moment(block)-c*x,
             source_atom_0_mass=sum(max(0,min(right,m)-left) for left,right in block),
             quadratic_cost=sum(Q(right)-Q(left) for left,right in block)
                            -2*x*moment(block)+x*x*mass,
             pieces=len(block))
    row['conditional_variance']=row['quadratic_cost']/c
    rows.append(row)
    kernels.append(dict(atom=label,x=x,c=c,residual_quantile_start=s,
                        source_mass_intervals=block))
    remove(block)
    if label in {'T','3','4','997','boundary'}:
        print(label, 'slack',mp.nstr(x-bmin,20),'pieces',len(block),flush=True)

summary=dict(cutoff=X,prime_power_count=len(pp),actual_nu_atoms=len(atoms)-1,
             digits=mp.mp.dps,series_terms=NTERMS,T=T,S_T=AT,m=m,a=a,nu_T=nu_T,
             L=L,S_L=SL,U=U,U_minus_L=U-L,boundary_mass=D,
             source_mass=M(U),demand_mass=sum(c for _,_,c in atoms),
             source_first_moment=H(U),demand_first_moment=sum(x*c for _,x,c in atoms),
             total_mass_error=M(U)-sum(c for _,_,c in atoms),
             total_moment_error=H(U)-sum(x*c for _,x,c in atoms),
             max_atom_mass_error=max(abs(r['mass_error']) for r in rows),
             max_atom_moment_error=max(abs(r['moment_error']) for r in rows),
             residual_source_mass=sum(right-left for left,right in remaining),
             min_availability_slack=min(r['availability_slack'] for r in rows[:-1]),
             max_actual_source=max(r['source_high'] for r in rows[:-1]),
             max_kernel_width=max(r['source_high']-r['source_low'] for r in rows[:-1]),
             true_lines_total_quadratic_cost=sum(r['quadratic_cost'] for r in rows[:-1]),
             boundary_quadratic_cost=rows[-1]['quadratic_cost'],
             max_true_line_conditional_variance=max(r['conditional_variance'] for r in rows[:-1]))
summary['residual_after_true_lines_before_boundary'] = true_line_residual

# Independent radial characterization of the atom left at zero.  Adding the
# artificial demand at T corresponds, for t>=T, to the original prime q=2;
# its actual demand mass is nu_T, not c_2.
radial_rows=[]
radial_record=m
radial_record_q=None
cumulative_c=cumulative_p=mp.mpf(0)
for q,p in pp:
    c=mp.log(p)/mp.sqrt(q)
    x=mp.log(q)
    cumulative_c+=c
    cumulative_p+=c*x
    radial_t=x
    if x*Ap(x)-A(x)<cumulative_p:
        for _ in range(30):
            val=radial_t*Ap(radial_t)-A(radial_t)-cumulative_p
            if abs(val)<mp.mpf('1e-48'):
                break
            radial_t-=val/(radial_t*beta(radial_t))
        else:
            raise RuntimeError('Radial Newton iteration did not converge.')
    radial_value=(A(radial_t)-cumulative_c*radial_t+cumulative_p)/radial_t
    if radial_value<radial_record:
        radial_record=radial_value
        radial_record_q=q
        radial_record_t=radial_t
    radial_rows.append(dict(q=q,x=x,C=cumulative_c,P=cumulative_p,
                            constrained_radial_minimizer=radial_t,
                            constrained_radial_minimum=radial_value,
                            residual_atom_0_record=radial_record))
summary['radial_reservoir_identity']=dict(
    record=radial_record,attaining_prefix_q=radial_record_q,
    attaining_t=radial_record_t,
    error_against_shadow_atom_0=radial_record-true_line_residual['atom_0_mass'])


def serial(value):
    if isinstance(value,mp.mpf):
        return mp.nstr(value,60)
    if isinstance(value,dict):
        return {key:serial(val) for key,val in value.items()}
    if isinstance(value,(list,tuple)):
        return [serial(val) for val in value]
    return value


prefix=OUT/f'shadow_high_precision_x{X}'
Path(str(prefix)+'_kernels.json').write_text(json.dumps(serial(kernels),indent=2))
Path(str(prefix)+'_summary.json').write_text(json.dumps(serial(summary),indent=2))
Path(str(prefix)+'_radial_records.json').write_text(json.dumps(serial(radial_rows),indent=2))
with Path(str(prefix)+'_rows.csv').open('w') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(serial(rows))
print(json.dumps(serial(summary),indent=2))
