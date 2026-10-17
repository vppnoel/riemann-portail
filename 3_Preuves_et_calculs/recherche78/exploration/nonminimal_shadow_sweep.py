"""Autonomous 60-digit sweep after a prescribed nonminimal initial raccord.

Run with a Python containing mpmath.  Optional first argument changes the cutoff.
Every printed number is diagnostic: no directed interval rounding is claimed.
Output kernels restrict the original, continuous source quantile, so they are
liftable to beta(u) du without any discrete-source approximation.  The initial
line consumes all m delta_0 and one interval of the density.  Later prime-power
lines use quantile shadows; the artificial boundary line is separate.
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


# The prescribed raccord has mass nu_T and barycenter T, and consumes all mu_0.
# The diffuse mass is -a.  Both endpoint equations are solved independently of
# the source cap, hence this first line is identical at every cutoff.
assert mu_T == 0 and a < 0
initial_l, initial_b = mp.findroot(
    lambda lo,hi:(M(hi)-M(lo)+a,H(hi)-H(lo)-T*nu_T),
    (mp.mpf('.84097046684643'),mp.mpf('1.02059031817341')))
assert T < initial_l < initial_b < mp.log(3)


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


def essential_source_low(s):
    # G(m)=0 is an isolated quantile endpoint after the atom at 0.  An interval
    # beginning at m contains no mass at 0 and its essential lower support is T.
    return T if s == m else G(s)


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


atoms = [('raccord_T',T,nu_T)]+[(str(q),mp.log(q),mp.log(p)/mp.sqrt(q)) for q,p in pp if q>2]
atoms.append(('boundary',L,D))
rows,kernels = [],[]
for label,x,c in atoms:
    if label == 'boundary':
        nonboundary_residual = dict(
            mass=sum(right-left for left,right in remaining),
            first_moment=moment(remaining),
            atom_0_mass=sum(max(0,min(right,m)-left) for left,right in remaining),
            atom_T_mass=sum(max(0,min(right,m+mu_T)-max(left,m)) for left,right in remaining),
            source_mass_intervals=list(remaining))
    if label == 'raccord_T':
        s=None
        bmin=None
        block=[(mp.mpf(0),m),(M(initial_l),M(initial_b))]
    else:
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
                deriv = G(block[-1][1])-essential_source_low(block[0][0])
                candidate=s-val/deriv if deriv else (lower+upper)/2
                s=candidate if lower<candidate<upper else (lower+upper)/2
            else:
                raise RuntimeError(f'Shadow root did not converge at {label}.')
        block=pieces(s,c)
    mass=sum(right-left for left,right in block)
    kind='initial_raccord' if label=='raccord_T' else ('boundary' if label=='boundary' else 'prime_power')
    row=dict(atom=label,kind=kind,x=x,c=c,min_barycenter=bmin,
             availability_slack=None if bmin is None else x-bmin,
             source_low=essential_source_low(block[0][0]),source_high=G(block[-1][1]),
             mass_error=mass-c,moment_error=moment(block)-c*x,
             source_atom_0_mass=sum(max(0,min(right,m)-left) for left,right in block),
             quadratic_cost=sum(Q(right)-Q(left) for left,right in block)
                            -2*x*moment(block)+x*x*mass,
             pieces=len(block))
    row['conditional_variance']=row['quadratic_cost']/c
    row['source_width']=row['source_high']-row['source_low']
    row['max_transport_distance']=max(x-row['source_low'],row['source_high']-x)
    rows.append(row)
    kernels.append(dict(atom=label,kind=kind,x=x,c=c,residual_quantile_start=s,
                        source_mass_intervals=block))
    remove(block)
    if label in {'raccord_T','3','4','997','boundary'}:
        print(label, 'slack',mp.nstr(row['availability_slack'],20),'pieces',len(block),flush=True)

summary=dict(cutoff=X,variant='nonminimal_initial_raccord',
             prime_power_count_including_2=len(pp),prime_power_lines_q_greater_2=len(pp)-1,
             initial_raccord_lines=1,nonboundary_lines=len(atoms)-1,artificial_boundary_lines=1,
             digits=mp.mp.dps,series_terms=NTERMS,T=T,S_T=AT,m=m,a=a,nu_T=nu_T,
             L=L,S_L=SL,U=U,U_minus_L=U-L,boundary_mass=D,
             source_mass=M(U),demand_mass=sum(c for _,_,c in atoms),
             source_first_moment=H(U),demand_first_moment=sum(x*c for _,x,c in atoms),
             total_mass_error=M(U)-sum(c for _,_,c in atoms),
             total_moment_error=H(U)-sum(x*c for _,x,c in atoms),
             max_atom_mass_error=max(abs(r['mass_error']) for r in rows),
             max_atom_moment_error=max(abs(r['moment_error']) for r in rows),
             residual_source_mass=sum(right-left for left,right in remaining),
             min_prime_power_availability_slack=min(r['availability_slack'] for r in rows[1:-1]),
             max_actual_source=max(r['source_high'] for r in rows[:-1]),
             max_kernel_width=max(r['source_high']-r['source_low'] for r in rows[:-1]),
             max_prime_power_kernel_width=max(r['source_width'] for r in rows[1:-1]),
             max_transport_distance=max(r['max_transport_distance'] for r in rows[:-1]),
             nonboundary_lines_total_quadratic_cost=sum(r['quadratic_cost'] for r in rows[:-1]),
             boundary_quadratic_cost=rows[-1]['quadratic_cost'],
             max_nonboundary_conditional_variance=max(r['conditional_variance'] for r in rows[:-1]))
summary['residual_after_raccord_and_prime_powers_before_boundary'] = nonboundary_residual
summary['fixed_initial_raccord']=dict(
    l=initial_l,b=initial_b,diffuse_mass=-a,target_mass=nu_T,
    mass_error=m+M(initial_b)-M(initial_l)-nu_T,
    moment_error=H(initial_b)-H(initial_l)-T*nu_T,
    all_atom_0_mass_consumed=m,
    gap_zero_at_and_after_b=True,
    b_less_than_log_3=initial_b<mp.log(3))


def serial(value):
    if isinstance(value,mp.mpf):
        return mp.nstr(value,60)
    if isinstance(value,dict):
        return {key:serial(val) for key,val in value.items()}
    if isinstance(value,(list,tuple)):
        return [serial(val) for val in value]
    return value


prefix=OUT/f'nonminimal_x{X}'
Path(str(prefix)+'_kernels.json').write_text(json.dumps(serial(kernels),indent=2))
Path(str(prefix)+'_summary.json').write_text(json.dumps(serial(summary),indent=2))
with Path(str(prefix)+'_rows.csv').open('w') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(serial(rows))
print(json.dumps(serial(summary),indent=2))
