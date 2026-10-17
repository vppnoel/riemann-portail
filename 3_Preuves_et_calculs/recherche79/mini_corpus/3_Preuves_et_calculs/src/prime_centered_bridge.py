"""Pole-centered arithmetic and interval budgets, independent of zero data.

Binary interval endpoints are authoritative. Archived archimedean values are
never promoted to validated intervals by this module.
"""
from fractions import Fraction as F
from bisect import bisect_right
import mpmath as mp
import symbolic_weil_family as w

def setup(bits=400):mp.mp.dps=140;mp.iv.prec=bits
def I(x):
    x=F(x);return mp.iv.mpf(x.numerator)/x.denominator
def endpoint_q(t):
    sign,man,exp,bc=t
    if bc<0:raise ValueError('finite endpoint required')
    return F((-1 if sign else 1)*man)*F(2)**exp
def lo(v):return endpoint_q(v._mpi_[0])
def hi(v):return endpoint_q(v._mpi_[1])
def midpoint(v):return w.mpq((lo(v)+hi(v))/2)
def pack(v):return dict(binary=[list(t) for t in v._mpi_],midpoint=mp.nstr(midpoint(v),18),width=mp.nstr(w.mpq(hi(v)-lo(v)),8))
def ev(p,x):
    s=I(0)
    for a in reversed(p):s=s*x+I(a)
    return s
def t_correlation(S,i,j):
    return [a/F(S)**k for k,a in enumerate(w.symmetric_correlation(S,i,j))]
def seed_energy(S,i,j):
    return w.integral_even(w.mul(w.derivative(w.seed(i)),w.derivative(w.seed(j))))/F(S)+F(S,4)*w.integral_even(w.mul(w.seed(i),w.seed(j)))
def exponential_primitive(p,a):
    a=F(a);out=[F(0)];d=list(p);j=0
    while any(d):
        out=w.add(out,w.scale(d,F(-1)**j/a**(j+1)));d=w.derivative(d);j+=1
    return out
def prime_residual_intervals(S,i,j,powers):
    S=F(S);D=2*S;h=t_correlation(S,i,j);p0=seed_energy(S,i,j)
    if h==[F(0)]:return dict(prime=I(0),residual=I(0),ibp=I(0),continuum=I(0),seed=p0)
    assert w.evalq(h,D)==0
    times=[mp.iv.log(I(n)) for p,m,n in powers];weights=[mp.iv.log(I(p))/mp.iv.sqrt(I(n)) for p,m,n in powers]
    prime=2*sum((a*ev(h,t) for a,t in zip(weights,times)),I(0))
    # Independent closed integration by parts on each Chebyshev step interval.
    q=w.add(w.derivative(h),w.scale(h,F(-1,2)));primitive=exponential_primitive(q,F(1,2));contprim=exponential_primitive(h,F(1,2))
    points=[I(0)]+times+[I(D)]
    fvals=[I(h[0])]+[mp.iv.exp(-t/2)*ev(h,t) for t in times]+[I(0)]
    cvals=[mp.iv.exp(t/2)*ev(primitive,t) for t in points]
    c=I(0);ibp=I(0)
    for k in range(len(points)-1):
        ibp-=2*((c+1)*(fvals[k+1]-fvals[k])-(cvals[k+1]-cvals[k]))
        if k<len(powers):c+=mp.iv.log(I(powers[k][0]))
    continuum=2*(mp.iv.exp(I(S))*ev(contprim,I(D))-ev(contprim,I(0)))
    residual=prime+I(p0)
    assert lo(continuum)<=-p0<=hi(continuum),'continuum identity enclosure failed'
    assert lo(residual)<=hi(ibp) and lo(ibp)<=hi(residual),'independent residual intervals disjoint'
    return dict(prime=prime,residual=residual,ibp=ibp,continuum=continuum,seed=p0)
def euler_enclosure(n=1024):
    hn=sum((F(1,k) for k in range(1,n+1)),F(0));a=I(hn)-mp.iv.log(I(n))
    # Integral comparison: H_n-log n-1/n <= gamma <= H_n-log n.
    return mp.iv.mpf([w.mpq(lo(a)-F(1,n)),w.mpq(hi(a))])
def validated_ceil(v):
    a=lo(v);b=hi(v)
    if a==b and a.denominator==1:return int(a)
    if a.numerator//a.denominator!=b.numerator//b.denominator:raise ValueError('ceiling not resolved')
    return a.numerator//a.denominator+1
def norm_budgets(S,powers,cutoff):
    S=F(S);D=2*S;weights=[mp.iv.log(I(p))/mp.iv.sqrt(I(n)) for p,m,n in powers]
    times=[mp.iv.log(I(n)) for p,m,n in powers];c0=mp.iv.log(8*mp.iv.pi)+euler_enclosure()+mp.iv.pi/2
    raw=c0+1+2*sum(weights,I(0));geo=c0+1;chain_lengths=[]
    for t,a in zip(times,weights):
        n=validated_ceil(I(D)/t);chain_lengths.append(n);geo+=2*a*mp.iv.cos(mp.iv.pi/(n+1))
    values=[n for p,m,n in powers];prefix=[I(0)]
    for a in weights:prefix.append(prefix[-1]+a)
    candidates=[prefix[-1]]
    for k,n in enumerate(values):candidates.append(prefix[k+1]+prefix[bisect_right(values,cutoff//n)])
    rowlo=max(lo(x) for x in candidates);rowhi=max(hi(x) for x in candidates)
    row=c0+1+mp.iv.mpf([w.mpq(rowlo),w.mpq(rowhi)])
    lower=2*sum((a*(1-t/I(D)) for a,t in zip(weights,times)),I(0))
    chosen=min(hi(raw),hi(geo),hi(row))
    return dict(c0=c0,raw=raw,geometric=geo,row=row,prime_norm_lower=lower,chosen_upper=chosen,chain_lengths=chain_lengths)
def multiplier_enclosure(T,K=64):
    T=F(T);p=I(0)
    for n in range(K):
        b=F(2*n)+F(1,2);p+=I(2*T*T/(b*(b*b+T*T)))
    b=F(2*K)+F(1,2);integral=mp.iv.log(1+I(T*T/(b*b)))/2
    low=lo(p+integral);up=hi(p+integral+I(2*T*T/(b*(b*b+T*T))))
    return mp.iv.mpf([w.mpq(low),w.mpq(up)])
def improved_tail(S,L,K=64,Jrange=(1,512)):
    S=F(S);L=F(L)
    for J in range(Jrange[0],Jrange[1]+1):
        T=1<<J;r=1+multiplier_enclosure(T,K)
        if lo(r)>2*L:
            z=6*S*T;q=-(-z.numerator//z.denominator);beta=F(12,11)/lo(r);mu=1-L*beta
            assert mu>0 and q>=1
            return dict(J=J,T_expression='2^'+str(J),q=str(q),q_digits=len(str(q)),r=pack(r),
                r_lower=str(lo(r)),L_upper=str(L),epsilon_upper='1/12',beta_upper=str(beta),
                mu_lower=str(mu),residual_debt_factor_upper=str(beta/mu),
                status='validated tail budget; effective Schur not computed')
    return dict(status='no contract within grid')
def negative_base_bound(S,k=0):
    S=F(S);f=w.test(S,k);mass=w.mass(S,k,k);d=w.integral_even(w.mul(w.derivative(f),w.derivative(f)))/S
    # ∫t²w(t)dt <= 16+(1/4)*(1+1/2)=131/8; C0>25/6.
    upper=F(131,8)*d-F(25,6)*mass+seed_energy(S,k,k)
    return dict(S=str(S),k=k,mass=str(mass),derivative_mass=str(d),seed_energy=str(seed_energy(S,k,k)),
                rational_upper=str(upper),normalized_upper=str(upper/mass),negative_certified=upper<0)

def uniform_negative_base_certificate():
    """Analytic polynomial witness for every S >= 16, not the full Weil form."""
    a=[w.integral_even(w.mul(w.derivative(w.seed(0),j),w.derivative(w.seed(0),j))) for j in range(4)]
    bound=-a[0]/96+F(193,48)*a[2]/16**4+F(131,8)*a[3]/16**6
    assert bound==F(-14112607,4704860160)<0
    return dict(support_range='S >= 16',seed='(1-x^2/S^2)^4',integrals_exact=[str(v) for v in a],
        upper_over_S_coefficients=[str(-a[0]/96),str(-F(23,384)*a[1]),str(F(193,48)*a[2]),str(F(131,8)*a[3])],
        uniform_upper_over_S=str(bound),negative_certified=True,
        scope='continuous base B0 only; not Q_W and not a counterexample to RH')

def residual_matrix_contract(H,C,beta,mu,delta_H=0,delta_C=0,source_errors=(),theta=1):
    """Exact real algebra of the sufficient bound; analytic lifting remains required."""
    from schur_bridge import psd
    H=[[F(x) for x in row] for row in H];C=[[F(x) for x in row] for row in C];n=len(H)
    beta,mu,delta_H,delta_C,theta=map(F,(beta,mu,delta_H,delta_C,theta))
    if mu<=0 or beta<0 or theta<=0 or delta_H<0 or delta_C<0:raise ValueError('positive tail and nonnegative errors required')
    if len(C)!=n or any(len(row)!=n for row in H+C):raise ValueError('square equal dimensions required')
    if any(H[i][j]!=H[j][i] or C[i][j]!=C[j][i] for i in range(n) for j in range(n)):raise ValueError('symmetric matrices required')
    errors=[F(x) for x in source_errors]
    if errors and len(errors)!=n:raise ValueError('one source bound per vector required')
    if any(x<0 for x in errors):raise ValueError('source errors nonnegative')
    eps2=sum((x*x for x in errors),F(0));fac=beta/mu
    if not psd([[C[i][j]+(delta_C if i==j else 0) for j in range(n)] for i in range(n)]):raise ValueError('Gram upper bound must be positive semidefinite')
    cup=[[(C[i][j]+(delta_C if i==j else 0) if not eps2 else (1+theta)*C[i][j]+((1+theta)*delta_C+(1+1/theta)*eps2 if i==j else 0)) for j in range(n)] for i in range(n)]
    low=[[H[i][j]-(delta_H if i==j else 0)-fac*cup[i][j] for j in range(n)] for i in range(n)]
    return dict(lower_matrix=[[str(x) for x in row] for row in low],algebraic_psd=psd(low),
        scope='sufficient real-matrix algebra; analytic source/Gram bounds, complete head and tail premises must be supplied',global_RH_claim=False)
