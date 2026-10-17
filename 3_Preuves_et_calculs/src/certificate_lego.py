"""Reusable real certificate bricks with rational ports and outward intervals.

The analytic lifting is proved in V646_LEGO_CERTIFICATS.md; this code is not a
formal proof assistant. No zero data or archimedean quadrature is imported.
"""
from dataclasses import dataclass
from fractions import Fraction as F
import mpmath as mp
import prime_centered_bridge as b
import symbolic_weil_family as w
from schur_bridge import psd,linear_solution,matrix

@dataclass(frozen=True)
class Port:
    S: F
    form: str='Q_W'
    mass_shift: F=F(0)
    metric: str='R=mass+arch_energy'
    unit: str='A_amp^2'
    annihilators: tuple=('cosh(x/2)','sinh(x/2)')
    def __post_init__(self):
        object.__setattr__(self,'S',F(self.S))
        object.__setattr__(self,'mass_shift',F(self.mass_shift))
        if self.S<=0:raise ValueError('positive support required')
        if self.form=='Q_W':
            if self.mass_shift:raise ValueError('Q_W has no added mass shift')
        elif self.form=='Q_W_minus_eta_mass':
            if self.mass_shift<=0:raise ValueError('positive explicit mass shift required')
        else:raise ValueError('quadratic form not supported by this template')

@dataclass(frozen=True)
class Brick:
    name: str
    port: Port
    payload: dict
    all_tests: bool=True

def check_ports(*bricks):
    if not bricks or any(x.port!=bricks[0].port for x in bricks):raise ValueError('domain, form, norm, unit and annihilators must match')
    if any(not x.all_tests for x in bricks):raise ValueError('finite samples do not cover the whole domain')
    return bricks[0].port

def projection_diagonal(S,t):
    """Squared projected cos/sin norms, with interval elementary functions."""
    S=F(S);t=F(t);s=b.I(S);v=b.I(t)
    ep=mp.iv.exp(s/2);em=mp.iv.exp(-s/2);sh=(ep-em)/2;ch=(ep+em)/2
    gplus=s+(mp.iv.exp(s)-mp.iv.exp(-s))/2;gminus=(mp.iv.exp(s)-mp.iv.exp(-s))/2-s
    if b.lo(gminus)<=0:raise ValueError('annihilator Gram not positive')
    if t:
        co=mp.iv.cos(v*s);si=mp.iv.sin(v*s);den=v*v+b.I(F(1,4))
        bc=(sh*co+2*v*ch*si)/den;bs=(ch*si-2*v*sh*co)/den
        sinc=mp.iv.sin(2*v*s)/(2*v)
    else:
        bc=4*sh;bs=b.I(0);sinc=s
    return s+sinc-bc*bc/gplus,s-sinc-bs*bs/gminus

def multiplier_increment(t0,t1,K=64):
    """Positive series/integral enclosure of a(t1)-a(t0); no subtraction debt."""
    t0,t1=F(t0),F(t1)
    if not 0<=t0<t1:raise ValueError('ordered nonnegative thresholds required')
    bk=F(2*K)+F(1,2)
    if bk<t1:raise ValueError('tail monotonicity needs b_K >= t1')
    delta=t1*t1-t0*t0;partial=b.I(0)
    for n in range(K):
        bn=F(2*n)+F(1,2)
        partial+=b.I(2*bn*delta/((bn*bn+t1*t1)*(bn*bn+t0*t0)))
    integral=mp.iv.log(b.I((bk*bk+t1*t1)/(bk*bk+t0*t0)))/2
    first=b.I(2*bk*delta/((bk*bk+t1*t1)*(bk*bk+t0*t0)))
    return partial+integral,partial+integral+first

def frequency_layers(S,steps=32,step=F(3,8),subdivisions=256,K=64):
    """Finite layer lower bound; midpoint errors use |d'_parity| <= 4S²."""
    S=F(S);step=F(step)
    if S<=0 or steps<1 or subdivisions<1:raise ValueError('positive grid and support required')
    h=step/subdivisions;M=4*S*S;sums=[b.I(0),b.I(0)];lambdas=[F(0),F(0)];rows=[]
    for j in range(1,steps+1):
        for k in range(subdivisions):
            t=((j-1)*subdivisions+k+F(1,2))*h
            values=projection_diagonal(S,t)
            for p in range(2):sums[p]+=values[p]
        T=j*step;error=M*T*h/4
        kappas=[(b.I(h)*sums[p]+b.I(error))/mp.iv.pi for p in range(2)]
        increments=multiplier_increment((j-1)*step,T,K);dl=max(F(0),b.lo(increments[0]))
        ku=[max(F(0),b.hi(x)) for x in kappas]
        for p in range(2):lambdas[p]+=dl*(1-min(F(1),ku[p]))
        rows.append(dict(T=str(T),kappa_upper=[str(x) for x in ku],midpoint_integral=[b.pack(b.I(h)*sums[p]/mp.iv.pi) for p in range(2)],
            quadrature_error_numerator=str(error),increment_lower=str(dl),increment_interval_lower=b.pack(increments[0]),
            lambda_cumulative_lower=[str(x) for x in lambdas]))
    return dict(steps=steps,step=str(step),subdivisions=subdivisions,microstep=str(h),lipschitz_upper=str(M),
        lambda_even_lower=str(lambdas[0]),lambda_odd_lower=str(lambdas[1]),lambda_lower=str(min(lambdas)),rows=rows,
        scope='all admissible tests in both parities; finite layer lower bound, not a spectrum estimate')

def J_interval(d):
    if b.lo(d)<=0:raise ValueError('positive boundary distance required')
    r=mp.iv.exp(-d/2)
    return mp.iv.log((1+r)/(1-r))/2+mp.iv.atan2(r,b.I(1))

def boundary_bricks(port,lambda_lower,eta=0):
    if F(eta)!=port.mass_shift:raise ValueError('mass shift must match the form port')
    S=port.S;delta=2*b.I(S)-mp.iv.log(b.I(2));a=mp.iv.log(b.I(2));D=2*b.I(S)
    if b.lo(delta)<=0 or b.hi(D)>=b.lo(mp.iv.log(b.I(3))) or b.hi(D)>=b.lo(2*a):
        raise ValueError('this template requires log2 < 2S < min(log3,2log2)')
    v0=2*J_interval(b.I(S));v1=J_interval(delta)+J_interval(a);weight=a/mp.iv.sqrt(b.I(2))
    c0=mp.iv.log(8*mp.iv.pi)+b.euler_enclosure()+mp.iv.pi/2+b.I(eta)
    return (Brick('energy',port,dict(lambda_lower=F(lambda_lower))),
        Brick('boundary',port,dict(v0_lower=b.lo(v0),v1_lower=b.lo(v1),v0_interval=b.pack(v0),v1_interval=b.pack(v1),delta_interval=b.pack(delta))),
        Brick('constants',port,dict(weight_upper=b.hi(weight),c0_upper=b.hi(c0),weight_interval=b.pack(weight),c0_interval=b.pack(c0),eta=F(eta))))

def assemble_local_certificate(energy,boundary,constants):
    port=check_ports(energy,boundary,constants)
    if (energy.name,boundary.name,constants.name)!=('energy','boundary','constants'):raise ValueError('expected brick roles required')
    if F(constants.payload['eta'])!=port.mass_shift:raise ValueError('form parameter and constants must match')
    if port.metric!='R=mass+arch_energy' or port.unit!='A_amp^2' or port.annihilators!=('cosh(x/2)','sinh(x/2)'):
        raise ValueError('template metric, unit and moments required')
    la=F(energy.payload['lambda_lower']);v0=F(boundary.payload['v0_lower']);v1=F(boundary.payload['v1_lower'])
    weight=F(constants.payload['weight_upper']);c0=F(constants.payload['c0_upper'])
    if la<0 or weight<0 or c0<0 or not 0<v0<v1:raise ValueError('nonnegative energy/constants and ordered positive floors required')
    alpha=weight/(v1-v0)
    if alpha>1:return dict(status='inconclusive',reason='convex weight exceeds one',S=str(port.S),form=port.form,mass_shift=str(port.mass_shift),global_RH_claim=False)
    c=(1-alpha)*la+alpha*v0-c0;L=c0+weight
    certified=c>0
    return dict(status='certified_local_all_tests' if certified else 'inconclusive',S=str(port.S),form=port.form,mass_shift=str(port.mass_shift),
        mass_floor_lower=str(c),convex_weight=str(alpha),independent_floor_lower=str(la-c0-weight),
        mu_R_lower=str(c/(c+L+1)) if certified else None,beta_R_upper=str(1/(la+1)),
        support_range='0 < S <= '+str(port.S) if certified else None,
        proof_templates=['projection/parity/layers','boundary potential','one-prime edge coupling','convex blend','zero extension'],
        head_dimension=0 if certified else None,scope='whole admissible form domain, with analytic lemmas supplied in document71',global_RH_claim=False)

def local_disjoint_certificate(S):
    S=F(S)
    if S<=0 or b.hi(2*b.I(S))>=b.lo(mp.iv.log(b.I(2))):raise ValueError('no-prime support required')
    floor=2*J_interval(2*b.I(S));c0=mp.iv.log(8*mp.iv.pi)+b.euler_enclosure()+mp.iv.pi/2
    low=b.lo(floor);upper=b.hi(c0);c=low-upper
    return dict(S=str(S),arch_floor_interval=b.pack(floor),c0_interval=b.pack(c0),status='certified_local_all_tests' if c>0 else 'inconclusive',
        mu_R_lower=str(c/(low+1)) if c>0 else None,beta_R_upper=str(1/(low+1)),global_RH_claim=False)

def inverse_spd(G):
    G=matrix(G);n=len(G);rem=[row[:] for row in G]
    while rem:
        p=rem[0][0]
        if p<=0:raise ValueError('strictly positive Gram required')
        rem=[[rem[i][j]-rem[i][0]*rem[0][j]/p for j in range(1,len(rem))] for i in range(1,len(rem))]
    columns=[linear_solution(G,[int(i==j) for i in range(n)]) for j in range(n)]
    return [[columns[j][i] for j in range(n)] for i in range(n)]

def project_source_gram(K,B,G):
    """Exact real Schur projection; accepts only a consistent joint Gram."""
    K=matrix(K);G=matrix(G);n=len(K);m=len(G);B=[[F(x) for x in row] for row in B]
    if len(B)!=m or any(len(row)!=n for row in B):raise ValueError('annihilator by source dimensions required')
    inv=inverse_spd(G);joint=[G[i]+B[i] for i in range(m)]+[[B[j][i] for j in range(m)]+K[i] for i in range(n)]
    if not psd(joint):raise ValueError('consistent positive joint Gram required')
    correction=[[sum(B[a][i]*inv[a][c]*B[c][j] for a in range(m) for c in range(m)) for j in range(n)] for i in range(n)]
    residual=[[K[i][j]-correction[i][j] for j in range(n)] for i in range(n)]
    assert psd(residual) and psd(correction)
    return dict(residual_gram=[[str(v) for v in row] for row in residual],removed_gram=[[str(v) for v in row] for row in correction],
        loewner_optimal=True,scope='exact real joint-Gram algebra; actual L2 sources and all integration errors must be supplied',global_RH_claim=False)

def request_unbounded_coverage(certificate):
    raise ValueError('bounded support family is not an exhaustion to infinity; a transport law is still required')

def rounded_certificate(energy,boundary,constants):
    """Five readable rational inequalities imply the report's uniform theorem."""
    assemble_local_certificate(energy,boundary,constants)
    port=check_ports(energy,boundary,constants)
    if port.form!='Q_W' or port.mass_shift:raise ValueError('rounded theorem is for Q_W only')
    la,v0,v1,c0,weight=F(231,40),F(769,200),F(1627,250),F(5373,1000),F(491,1000)
    if not (F(energy.payload['lambda_lower'])>=la and F(boundary.payload['v0_lower'])>=v0 and
            F(boundary.payload['v1_lower'])>=v1 and F(constants.payload['c0_upper'])<=c0 and F(constants.payload['weight_upper'])<=weight):
        raise ValueError('five rational floors/ceilings are not all established')
    alpha=F(3,16);payment=alpha*(v1-v0)-weight;c=(1-alpha)*la+alpha*v0-c0;mu=c/(c+c0+weight+1);beta=1/(1+la)
    assert payment>=0 and c==F(321,8000)>F(1,25) and mu>F(1,200) and beta<F(3,20)
    return dict(S_max=str(port.S),lambda_lower=str(la),v0_lower=str(v0),v1_lower=str(v1),c0_upper=str(c0),weight_upper=str(weight),
        alpha=str(alpha),edge_payment_surplus=str(payment),mass_floor=str(c),mu_R_lower=str(mu),beta_R_upper=str(beta),
        readable_mass_floor='1/25',readable_R_floor='1/200',readable_beta='3/20',all_tests=True,global_RH_claim=False)
