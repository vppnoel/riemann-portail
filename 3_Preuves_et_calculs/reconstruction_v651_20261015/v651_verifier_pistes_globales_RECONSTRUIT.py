#!/usr/bin/env python3
"""Reconstruction du 15-10-2026, PAS le programme original V6.51 retrouvé.

Reproduit les témoins finis décrits dans le document76, sections3 et5.1.
Calcul principal: Fraction et intervalles dyadiques à arrondi extérieur,
bibliothèque standard uniquement. --cross-check-mpmath ajoute un recoupement
avec mpmath1.3.0 et les deux modules originaux copiés dans sources/.

python3 -B v651_verifier_pistes_globales_RECONSTRUIT.py
python3 -B v651_verifier_pistes_globales_RECONSTRUIT.py --cross-check-mpmath

Ne calcule ni le signe de Q_W complet ni les quantificateurs globaux de Weil.
"""
from fractions import Fraction as F
from pathlib import Path
from math import comb,isqrt
from decimal import Decimal,localcontext
import argparse,hashlib,json,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
BITS=160

def down(x):return F((F(x)*(1<<BITS)).numerator//(F(x)*(1<<BITS)).denominator,1<<BITS)
def up(x):return -down(-F(x))
class Interval:
    def __init__(self,lo,hi=None):
        hi=lo if hi is None else hi
        assert F(lo)<=F(hi)
        self.lo,self.hi=down(lo),up(hi)
    def __add__(self,v):
        v=iv(v);return Interval(self.lo+v.lo,self.hi+v.hi)
    __radd__=__add__
    def __neg__(self):return Interval(-self.hi,-self.lo)
    def __sub__(self,v):return self+-iv(v)
    def __rsub__(self,v):return iv(v)+-self
    def __mul__(self,v):
        v=iv(v);ends=[a*b for a in [self.lo,self.hi] for b in [v.lo,v.hi]]
        return Interval(min(ends),max(ends))
    __rmul__=__mul__
    def __truediv__(self,v):
        v=iv(v)
        if v.lo<=0<=v.hi:raise ZeroDivisionError('Interval denominator crosses zero')
        return self*Interval(1/v.hi,1/v.lo)
    def __rtruediv__(self,v):return iv(v)/self
    def __pow__(self,n):
        if n<0:return 1/(self**(-n))
        v=iv(1)
        for _ in range(n):v=v*self
        return v
def iv(v):return v if isinstance(v,Interval) else Interval(v)
def decimal(x):
    with localcontext() as c:
        c.prec=24;return str(Decimal(x.numerator)/Decimal(x.denominator))
def pack(v):
    v=iv(v)
    return {'lower_exact':str(v.lo),'upper_exact':str(v.hi),
            'midpoint_display_only':decimal((v.lo+v.hi)/2),'width_exact':str(v.hi-v.lo)}

def log_bound(x,terms=220):
    """log x=2 sum r^(2k+1)/(2k+1), r=(x-1)/(x+1), x>=1."""
    x=F(x)
    if x<1:return -log_bound(1/x,terms)
    r=(x-1)/(x+1);s=sum((r**(2*k+1)/F(2*k+1) for k in range(terms)),F(0))
    tail=2*r**(2*terms+1)/(F(2*terms+1)*(1-r*r))
    return Interval(2*s,2*s+tail)
def sqrt_bound(x):
    x=F(x)
    if x<0:raise ValueError('Nonnegative radicand required')
    floor=isqrt((x.numerator<<(2*BITS))//x.denominator)
    lo=F(floor,1<<BITS)
    return Interval(lo,lo if lo*lo==x else F(floor+1,1<<BITS))
def exp_positive_bound(x,terms=100):
    x=F(x)
    if not 0<=x<terms+2:raise ValueError('Taylor guard')
    term=F(1);s=term
    for k in range(1,terms+1):term*=x/k;s+=term
    tail=term*x/F(terms+1)/(1-x/F(terms+2))
    return Interval(s,s+tail)
def J_bound(S,terms=32):
    """atanh(z)+atan(z)=2 sum z^(4k+1)/(4k+1), z=exp(-S/2)."""
    z=1/exp_positive_bound(F(S,2));s=iv(0)
    for k in range(terms):s+=2*z**(4*k+1)/F(4*k+1)
    tail=2*z**(4*terms+1)/(F(4*terms+1)*(1-z**4))
    return Interval(s.lo,(s+Interval(0,tail.hi)).hi)
def constant_guards():
    def atan(x,terms=12):
        x=F(x);s=sum((F(-1)**k*x**(2*k+1)/F(2*k+1) for k in range(terms)),F(0))
        other=s+F(-1)**terms*x**(2*terms+1)/F(2*terms+1)
        return Interval(min(s,other),max(s,other))
    pi=16*atan(F(1,5))-4*atan(F(1,239))
    log24=log_bound(24);log2=log_bound(2)
    assert pi.lo>3 and log24.lo>3 and 1-log2.hi>0 and F(9,2)>F(25,6)
    return {'pi_Machin_enclosure':pack(pi),'log24_enclosure':pack(log24),
            'gamma_lower_via_H1_minus_log2':str(1-log2.hi),
            'C0_argument':'pi>3, log24>3, gamma>=1-log2>0 imply C0>9/2>25/6',
            'C2_argument':'2 sum_(n>=0)(2n+1/2)^(-3) <=16+(1/4)(1+integral_1^infty x^(-3)dx)=131/8',
            'uses_RH':False}

def add(p,q):
    return [(p[k] if k<len(p) else F(0))+(q[k] if k<len(q) else F(0)) for k in range(max(len(p),len(q)))]
def scale(p,x):return [F(x)*v for v in p]
def derivative(p,n=1):
    for _ in range(n):p=[i*p[i] for i in range(1,len(p))] or [F(0)]
    return p
def product(p,q):
    out=[F(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):out[i+j]+=a*b
    return out
def integ(p):return sum((F(2)*a/F(i+1) for i,a in enumerate(p) if i%2==0),F(0))
def evaluate(p,x):
    out=iv(0) if isinstance(x,Interval) else F(0)
    for a in reversed(p):out=out*x+a
    return out
SEED=list(map(F,[1,0,-4,0,6,0,-4,0,1]))
def family(S):
    S=F(S);f=add(scale(derivative(SEED,2),1/S**2),scale(SEED,F(-1,4)))
    mass=S*integ(product(f,f));d=integ(product(derivative(f),derivative(f)))/S
    p0=integ(product(derivative(SEED),derivative(SEED)))/S+S/4*integ(product(SEED,SEED))
    # h(S*z)=S int_{z-1}^1 f(u)f(u-z)du; exact polynomial integration.
    h=[F(0)]*(2*len(f))
    for i,a in enumerate(f):
        for j,b in enumerate(f):
            for k in range(j+1):
                degree=i+k+1;power=j-k;c=S*a*b*comb(j,k)*F(-1)**power/degree
                h[power]+=c
                for ell in range(degree+1):h[power+ell]-=c*comb(degree,ell)*F(-1)**(degree-ell)
    while len(h)>1 and h[-1]==0:h.pop()
    h=[a/S**k for k,a in enumerate(h)]
    return f,mass,d,p0,h
def polar_identity(S,p0,h):
    primitive=[F(0)];d=list(h);j=0
    while any(d):
        primitive=add(primitive,scale(d,F(-1)**j/F(1,2)**(j+1)));d=derivative(d);j+=1
    assert evaluate(primitive,2*S)==0 and 2*primitive[0]==p0
    return {'primitive_at_2S_exact':'0','twice_primitive_at_zero_exact':str(2*primitive[0]),
            'P0_exact':str(p0),'identity_2_integral_exp_half_h_equals_minus_P0':True}

POWERS=[(2,1,2),(3,1,3),(2,2,4),(5,1,5),(7,1,7)]
def truncated_witness(S):
    f,mass,d,p0,h=family(S)
    assert mass>0 and evaluate(h,F(0))==mass and evaluate(h,2*S)==0 and evaluate(derivative(h),F(0))==0
    for endpoint in [F(-1),F(1)]:
        for n in range(4):assert evaluate(derivative(SEED,n),endpoint)==0
        assert evaluate(f,endpoint)==0 and evaluate(derivative(f),endpoint)==0
    upper=iv(F(131,8)*d-F(25,6)*mass);terms=[]
    for p,j,q in POWERS:
        shift=log_bound(q);weight=log_bound(p)/sqrt_bound(q)
        assert shift.hi<2*S
        corr=evaluate(h,shift);contribution=2*weight*corr;upper-=contribution
        terms.append({'p':p,'power':j,'q':q,'weight':pack(weight),'correlation':pack(corr)})
    upper/=iv(mass)
    return {'S':S,'seed':'(1-x^2/S^2)^4 on [-S,S], zero outside',
            'regularity':'Finite polynomial test is H1, not claimed C-infinity',
            'mass_exact':str(mass),'derivative_mass_exact':str(d),'P0_exact':str(p0),
            'polar_identity':polar_identity(S,p0,h),'C2_upper_exact':'131/8','C0_lower_exact':'25/6',
            'upper_bound_on_Q_A_over_mass':pack(upper),'negative_certified':upper.hi<0,
            'inconclusive':upper.hi>=0,'terms':terms,
            'scope':'Fixed A={2,3,4,5,7}; NOT the complete Weil form; positive upper bound proves no positivity.'}

# Gaussian rational arithmetic for explicit complex Hermitian fixtures.
def c(v):return v if isinstance(v,tuple) else (F(v),F(0))
def ca(x,y):x,y=c(x),c(y);return (x[0]+y[0],x[1]+y[1])
def cm(x,y):x,y=c(x),c(y);return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def cj(x):x=c(x);return (x[0],-x[1])
def quadratic(A,z):
    out=c(0)
    for i in range(len(z)):
        for j in range(len(z)):out=ca(out,cm(cm(cj(z[i]),A[i][j]),z[j]))
    assert out[1]==0;return out[0]
def algebra_checks():
    a=F(3,4);A=[[1,(F(0),a),a],[(F(0),-a),1,(F(0),a)],[a,(F(0),-a),1]]
    z=[1,(F(0),F(1)),-1];value=quadratic(A,z)
    assert value==F(-3,2) and 1-a*a==F(7,16)
    singular=[[1,1,1],[1,1,-1],[1,-1,1]];sing_value=quadratic(singular,[1,-1,-1])
    assert sing_value==-3
    moments={str(p):str(F(1)+F(1,p)-F(1)-F(1,p)) for p in [2,3,5,7]}
    assert all(x=='0' for x in moments.values())
    return {'origin':'New reconstruction fixtures, not alleged original test cases',
            'two_packet_conditions_insufficient':{'all_2x2_principal_minors':'7/16','complex_vector':['1','i','-1'],
              'quadratic_value_exact':str(value),'Toeplitz_Hermitian':True,'is_arithmetic_Weil_matrix':False},
            'singular_Schur_requires_range_guard':{'previous_block_rank':1,'coupling_in_previous_range':False,
              'pseudoinverse_only_delta':'1','negative_witness_value_exact':str(sing_value),'is_arithmetic_Weil_matrix':False},
            'prime_filter_polar_symbol_identity_exact':moments,
            'finite_logarithm_commutator_coefficient_identity':{
                'j_tested':list(range(1,9)),'j_times_inverse_j_exact':[str(F(j)*F(1,j)) for j in range(1,9)],
                'identity':'-[X,-r^j U_(j log p)/j] = log(p) r^j U_(j log p)',
                'scope':'Finite coefficients only; no infinite-prime norm convergence or sign claim'}}

def cross_check(rows,boundaries):
    sys.path.insert(0,str(HERE/'sources'))
    import mpmath as mp
    import symbolic_weil_family as w
    import prime_centered_bridge as b
    if mp.__version__!='1.3.0':raise RuntimeError('Pinned cross-check requires mpmath1.3.0')
    cross_bits=max(320,BITS+160);b.setup(cross_bits);report=[]
    for row in rows:
        S=row['S'];f,m,d,p0,h=family(S)
        assert f==w.test(S,0) and m==w.mass(S,0,0) and h==b.t_correlation(S,0,0)
        v=b.I(F(131,8)*d-F(25,6)*m)
        for p,j,q in POWERS:v-=2*mp.iv.log(b.I(p))/mp.iv.sqrt(b.I(q))*b.ev(h,mp.iv.log(b.I(q)))
        v/=b.I(m);saved=row['upper_bound_on_Q_A_over_mass']
        assert F(saved['lower_exact'])<=b.lo(v)<=b.hi(v)<=F(saved['upper_exact'])
        report.append({'S':S,'polynomial_and_mass_exact_match_original_modules':True,'mpmath_interval_contained':True})
    for row in boundaries:
        S=row['S'];z=mp.iv.exp(-b.I(S)/2);J=mp.iv.log((1+z)/(1-z))/2+mp.iv.atan2(z,b.I(1))
        v=mp.iv.log(b.I(2))/mp.iv.sqrt(b.I(2))/J;saved=row['lower_bound_on_envelope_alpha']
        assert F(saved['lower_exact'])<=b.lo(v)<=b.hi(v)<=F(saved['upper_exact'])
    return {'executed':True,'backend':f'mpmath1.3.0 interval arithmetic at{cross_bits}bits','truncated_witnesses':report,
            'boundary_cases':len(boundaries),'independent_human_or_agent_review_completed':False}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--bits',type=int,default=160)
    parser.add_argument('--output',type=Path,default=HERE/'v651_pistes_globales_resultats_RECONSTRUITS.json')
    parser.add_argument('--cross-check-mpmath',action='store_true');args=parser.parse_args()
    if sys.flags.optimize:raise RuntimeError('Assertions require non-optimized Python')
    if not 80<=args.bits<=512:raise ValueError('Precision must be80–512bits')
    global BITS;BITS=args.bits
    rows=[truncated_witness(S) for S in [4,8,16,32,64,128]]
    assert [r['negative_certified'] for r in rows]==[False,True,True,True,True,True]
    boundaries=[]
    for S,threshold in [(4,F(181,100)),(8,F(1338,100)),(16,F(73052,100))]:
        J=J_bound(S);ratio=(log_bound(2)/sqrt_bound(2))/J
        assert ratio.lo>threshold
        boundaries.append({'S':S,'J_enclosure':pack(J),'lower_bound_on_envelope_alpha':pack(ratio),
                           'document76_threshold_exact':str(threshold),'threshold_exceeded':True,
                           'scope':'Bounds c2/J(S); does NOT compute alpha supremum or arithmetic operator norm.'})
    files=['sources/document_76_original.md','sources/v651_protocole_global_original.json',
           'sources/symbolic_weil_family.py','sources/prime_centered_bridge.py']
    result={'schema':'v651_reconstruction_20261015_v1','date':'2026-10-15','status':'RECONSTRUCTION, NOT RECOVERED ORIGINAL',
            'original_script_recovered':False,'original_result_log_recovered':False,'global_archive_modified':False,
            'arithmetic':'Exact Fraction polynomial algebra; outward-rounded dyadic intervals',
            'precision_bits':BITS,'series_terms':{'log':220,'positive_exp':100,'J':32},
            'source_sha256':{p:hashlib.sha256((HERE/p).read_bytes()).hexdigest() for p in files},'constant_guards':constant_guards(),
            'fixed_prime_truncation_witnesses':rows,'boundary_envelope_witnesses':boundaries,'finite_algebra_checks':algebra_checks(),
            'cross_check':cross_check(rows,boundaries) if args.cross_check_mpmath else {'executed':False},
            'not_computationally_certified':['Universal Weil sign law','All Toeplitz dimensions and meshes',
              'Dual restriction algorithm and its convergence','Distributional two-filter density theorem','All compact supports'],
            'global_sign_proved':False,'RH_proved':False}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'output':str(args.output),'status':result['status'],'negative_fixed_A_cases':5,
                     'inconclusive_fixed_A_cases':1,'boundary_cases':3,'cross_check':result['cross_check']['executed'],
                     'RH_proved':False},ensure_ascii=False))
if __name__=='__main__':main()
