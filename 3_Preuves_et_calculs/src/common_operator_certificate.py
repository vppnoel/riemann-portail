"""Common-operator norm certificate: Gauss cardinal frame, intervals, exact SPD.

The analytic lifting and IEEE binary64 dot-product error model are given in
V648_OPERATEUR_COMMUN_CERTIFIE.md. No numpy sin, cos or digamma enters this
certificate. A floating eigensolver proposes a bound; integer Bareiss proves it.
"""
from fractions import Fraction as F
from math import factorial
import math
import numpy as np
from numpy.polynomial.legendre import leggauss
import mpmath as mp
import prime_centered_bridge as b
from certificate_lego import Port

def fq(x):return F.from_float(float(x))
def down(x):return np.nextafter(x,-np.inf)
def up(x):return np.nextafter(x,np.inf)
def aiv(x):
    if isinstance(x,tuple):return x
    y=float(x);q=fq(y);x=F(x)
    return (np.nextafter(y,-np.inf) if q>x else y,np.nextafter(y,np.inf) if q<x else y)
def from_iv(x):return (aiv(b.lo(x))[0],aiv(b.hi(x))[1])
def add(x,y):return down(x[0]+y[0]),up(x[1]+y[1])
def neg(x):return -x[1],-x[0]
def sub(x,y):return add(x,neg(y))
def mul(x,y):
    values=(x[0]*y[0],x[0]*y[1],x[1]*y[0],x[1]*y[1])
    return down(np.minimum.reduce(values)),up(np.maximum.reduce(values))
def div(x,y):
    if np.any(np.asarray(y[0])<=0) and np.any(np.asarray(y[1])>=0):
        if np.any((np.asarray(y[0])<=0)&(np.asarray(y[1])>=0)):raise ValueError('interval denominator contains zero')
    return mul(x,(down(1/y[1]),up(1/y[0])))
def horner(coeffs,x):
    r=aiv(coeffs[-1])
    for c in coeffs[-2::-1]:r=add(mul(r,x),aiv(c))
    return r
def trig_interval(z):
    """Outward polynomial sin/cos on |z|<=45, six exact angle doublings."""
    if np.any(np.asarray(z[0])<-45) or np.any(np.asarray(z[1])>45+1e-12):raise ValueError('bounded phase required')
    v=mul(z,aiv(F(1,64)));v2=mul(v,v)
    c=horner([F((-1)**k,factorial(2*k)) for k in range(11)],v2)
    s=mul(v,horner([F((-1)**k,factorial(2*k+1)) for k in range(11)],v2))
    # |v|<1: Taylor remainders <=1/22! and <=1/23!.
    c=add(c,(-float(F(1,factorial(22)))*1.001,float(F(1,factorial(22)))*1.001))
    s=add(s,(-float(F(1,factorial(23)))*1.001,float(F(1,factorial(23)))*1.001))
    for _ in range(6):c,s=sub(mul(c,c),mul(s,s)),mul(aiv(2),mul(c,s))
    return c,s
def exp_interval(z):
    if np.any(np.asarray(z[0])<-.25-1e-12) or np.any(np.asarray(z[1])>.25+1e-12):raise ValueError('bounded exponential argument required')
    r=horner([F(1,factorial(k)) for k in range(25)],z)
    rem=F(4,3)*F(1,4)**25/factorial(25);e=float(rem)*1.001
    return add(r,(-e,e))
def legendre_pair(n,x):
    p0=b.I(1);p1=x
    if n==0:return p0,b.I(0)
    for k in range(1,n):p0,p1=p1,((2*k+1)*x*p1-k*p0)/(k+1)
    return p1,p0
def legendre_integer_coefficients(n,derivative=0):
    """Integer coefficients of2^n P_n, optionally differentiated exactly."""
    c=[0]*(n+1)
    for k in range(n//2+1):c[n-2*k]=(-1)**k*factorial(2*n-2*k)//(factorial(k)*factorial(n-k)*factorial(n-2*k))
    for _ in range(derivative):c=[(j+1)*c[j+1] for j in range(len(c)-1)]
    return c
def exact_polynomial_value(coefficients,x,scale=1):
    """Homogeneous integer Horner avoids interval dependency at roots."""
    x=F(x);A,B=x.numerator,x.denominator;p=coefficients[-1];power=1
    for c in coefficients[-2::-1]:power*=B;p=p*A+c*power
    return F(p,scale*B**(len(coefficients)-1))
def signed(v):
    if b.lo(v)>0:return 1
    if b.hi(v)<0:return -1
    raise ValueError('root sign not resolved')
def certify_gauss(n=80,bisections=48):
    if n!=80:raise ValueError('this fixed interpolation contract uses80 nodes')
    guess,_=leggauss(n);positive=guess[n//2:];rows=[];last=F(0)
    coefficients=legendre_integer_coefficients(n);derivative=legendre_integer_coefficients(n,1)
    def exact_sign(x):
        v=exact_polynomial_value(coefficients,x)
        if not v:raise ValueError('root endpoint is an exact zero')
        return 1 if v>0 else -1
    for g in positive:
        center=fq(g);lo=center-F(1,2**42);hi=center+F(1,2**42)
        if not last<lo<hi<1:raise ValueError('disjoint positive root brackets required')
        sl=exact_sign(lo);sh=exact_sign(hi)
        if sl!=-sh:raise ValueError('root bracket sign change required')
        for _ in range(bisections):
            mid=(lo+hi)/2;sm=exact_sign(mid)
            if sm==sl:lo=mid
            else:hi=mid
        x=mp.iv.mpf([b.midpoint(b.I(lo)),b.midpoint(b.I(hi))])
        center=(lo+hi)/2;dp_center=b.I(exact_polynomial_value(derivative,center,2**n))
        # Markov applied twice to |P_n|<=1: |P_n''|<=n^4 on[-1,1].
        error=F(n**4)*(hi-lo)/2;dp=dp_center+mp.iv.mpf([-b.midpoint(b.I(error)),b.midpoint(b.I(error))])
        weight=2/((1-x*x)*dp*dp)
        if b.lo(weight)<=0:raise ValueError('positive Gauss weight required')
        rows.append(dict(root_lo=str(lo),root_hi=str(hi),weight=b.pack(weight)))
        last=hi
    # Forty disjoint sign changes, reflected by even Legendre parity, give all80 roots.
    return rows

def float_mid_interval(v):
    z=float((b.lo(v)+b.hi(v))/2);return z,max(abs(fq(z)-b.lo(v)),abs(fq(z)-b.hi(v)))

def joint_table(T=F(90),H=F(1,100),K=256,bits=44,progress=None):
    q=1<<bits;count=int(T/H);shift=mp.iv.log(b.I(2));weight=shift/mp.iv.sqrt(b.I(2));values=[];radius=F(0);rows=[]
    for i in range(count+1):
        t=i*H;a=b.multiplier_enclosure(t,K);v=a+2*weight*(1-mp.iv.cos(shift*b.I(t)))
        center=(b.lo(v)+b.hi(v))/2;fixed=round(center*q);err=max(abs(F(fixed,q)-b.lo(v)),abs(F(fixed,q)-b.hi(v)))
        radius=max(radius,err);values.append(fixed);rows.append(dict(t=str(t),midpoint_fixed=str(fixed),error_upper=str(err)))
        if progress and i%2000==0:progress('joint table '+str(i)+'/'+str(count))
    return np.asarray(values,dtype=np.int64),radius,rows

def bareiss_spd(A):
    """Exact positive leading minors for a symmetric integer matrix."""
    a=[[int(v) for v in row] for row in A];n=len(a)
    if not n or any(len(r)!=n for r in a) or any(a[i][j]!=a[j][i] for i in range(n) for j in range(n)):
        raise ValueError('nonempty symmetric integer matrix required')
    prev=1;pivots=[]
    for k in range(n):
        pivot=a[k][k]
        if pivot<=0:return False,pivots+[str(pivot)]
        pivots.append(str(pivot))
        for i in range(k+1,n):
            for j in range(i,n):
                value=a[i][j]*pivot-a[i][k]*a[k][j]
                quot,rem=divmod(value,prev)
                if rem:raise ValueError('Bareiss division is not exact')
                a[i][j]=quot;a[j][i]=quot
        prev=pivot
    return True,pivots

def validated_matrix_norm(M,bits=44):
    q=1<<bits;n=M.shape[0]
    if not np.all(np.isfinite(M)):raise ValueError('finite matrix required')
    symmetric=(M+M.T)/2
    integers=[[round(fq(symmetric[i,j])*q) for j in range(n)] for i in range(n)]
    asym=max(abs(fq(M[i,j])-fq(M[j,i])) for i in range(n) for j in range(n))
    rounding=max(abs(F(integers[i][j],q)-fq(M[i,j])) for i in range(n) for j in range(n))
    eig=float(np.linalg.eigvalsh(symmetric)[-1]);tau=F(math.ceil(eig*100000),100000)
    den=math.lcm(q,tau.denominator)
    A=[[(int(tau*den) if i==j else 0)-integers[i][j]*(den//q) for j in range(n)] for i in range(n)]
    ok,pivots=bareiss_spd(A)
    if not ok:raise ValueError('proposed finite norm ceiling not certified')
    return dict(tau=str(tau),point_eigenvalue=eig,integer_matrix=[[str(v) for v in r] for r in integers],
        scale=str(q),leading_minors=pivots,spd=True,rounding_norm_upper=str(n*rounding),asymmetry_entry_upper=str(asym))

def assemble_minorant_contract(tau,error,eta):
    """Exact bounded-minorant head/source/tail algebra in an orthonormal frame.

    The certificate must supply ||B-B_N||<=error and lambda_max(B_N)<=tau.
    This helper does not authenticate arbitrary premises or Q's strong sources.
    """
    tau,error,eta=map(F,(tau,error,eta))
    if min(tau,error)<0 or eta<=0:raise ValueError('nonnegative bounds and positive identity coefficient required')
    tail=eta-error;head=eta-tau-error
    if tail<=0:return dict(status='inconclusive',tail_floor=str(tail),metric='L2 mass',source_form='bounded A_U minorant')
    debt=error*error/tail;schur=head-debt
    return dict(status='certified_bounded_minorant_schur' if schur>0 else 'inconclusive',metric='L2 mass',
        source_form='bounded A_U minorant',head_floor=str(head),tail_floor=str(tail),
        source_gram_operator_upper=str(error*error),debt_operator_upper=str(debt),schur_floor=str(schur),
        original_Q_strong_sources_certified=False,global_RH_claim=False)

def certify(port,T=F(90),U=F(8),h=F(1,1000),H=F(1,100),N=80,K=256,bits=44,progress=None):
    if not isinstance(port,Port) or port.S!=F(1,2) or port.form!='Q_W' or port.mass_shift or port.metric!='R=mass+arch_energy' or port.unit!='A_amp^2' or port.annihilators!=('cosh(x/2)','sinh(x/2)'):
        raise ValueError('the validated half-support Q_W/R/unit/moment contract is required')
    if any(not isinstance(v,int) or isinstance(v,bool) for v in (N,K,bits)) or (T,U,h,H,N,K,bits)!=(F(90),F(8),F(1,1000),F(1,100),80,256,44):
        raise ValueError('frozen grid and resource contract required')
    if np.finfo(np.float64).eps!=2**-52 or np.finfo(np.float64).nmant!=52:raise ValueError('IEEE binary64 required')
    one=np.float64(1);half=np.float64(2**-53)
    if one+half!=one or -one-half!=-one or one+3*half!=np.float64(1+2**-51) or -one-3*half!=-np.float64(1+2**-51):
        raise ValueError('round-to-nearest ties-to-even arithmetic required')
    S=port.S;tail=b.multiplier_enclosure(T,K)
    if b.lo(tail)<=U:raise ValueError('global frequency tail not excluded')
    log2=mp.iv.log(b.I(2));log3=mp.iv.log(b.I(3))
    if not b.hi(log2)<2*S<min(b.lo(log3),b.lo(2*log2)):raise ValueError('one prime/disjoint edge contract required')
    gauss=certify_gauss(N);xlo=np.array([aiv(F(r['root_lo']))[0] for r in gauss]);xhi=np.array([aiv(F(r['root_hi']))[1] for r in gauss])
    # Reconstruct iv endpoints from their exact binary rationals, not display strings.
    weights=[mp.iv.mpf([b.midpoint(b.I(b.endpoint_q(r['weight']['binary'][0]))),b.midpoint(b.I(b.endpoint_q(r['weight']['binary'][1])))]) for r in gauss]
    swlo=np.array([from_iv(mp.iv.sqrt(2*b.I(S)*v))[0] for v in weights]);swhi=np.array([from_iv(mp.iv.sqrt(2*b.I(S)*v))[1] for v in weights])
    xx=mul((xlo[:,None],xhi[:,None]),aiv(S));sw=(swlo[:,None],swhi[:,None])
    ew=exp_interval(mul(xx,aiv(F(1,2))));em=exp_interval(mul(xx,aiv(F(-1,2))))
    cw=mul(add(ew,em),aiv(F(1,2)));ssw=mul(sub(ew,em),aiv(F(1,2)))
    si=b.I(S);gp=si+(mp.iv.exp(si)-mp.iv.exp(-si))/2;gm=(mp.iv.exp(si)-mp.iv.exp(-si))/2-si
    if b.lo(gm)<=F(1,48):raise ValueError('annihilator Gram floor not certified')
    sh=(mp.iv.exp(si/2)-mp.iv.exp(-si/2))/2;ch=(mp.iv.exp(si/2)+mp.iv.exp(-si/2))/2
    fixed,radius,table=joint_table(T,H,K,bits,progress)
    nf=int(T/h);q=1<<bits;ratio=int(H/h);den=2*ratio*q
    idx=np.arange(nf,dtype=np.int64);macro=idx//ratio;k=2*(idx%ratio)+1
    phinum=np.maximum(0,int(U*den)-((2*ratio-k)*fixed[macro]+k*fixed[macro+1]))
    if np.min(fixed)<0 or np.max(phinum)>int(U*den):raise ValueError('weight must lie between zero and U')
    if np.max(np.abs(fixed))*(2*ratio)>=2**53:raise ValueError('exact integer interpolation magnitude exceeded')
    phi=phinum.astype(np.float64)/den
    matrices=[np.zeros((N//2,N//2)),np.zeros((N//2,N//2))];row_errors=[np.zeros(N//2),np.zeros(N//2)];max_norm2=[0.,0.]
    for first in range(0,nf,2048):
        ii=np.arange(first,min(nf,first+2048));tmid=(ii.astype(np.float64)+.5)*float(h)
        # Product of an exact half-integer and rounded h: two ulps enclose it.
        t=(down(down(tmid))[None,:],up(up(tmid))[None,:])
        co,ss=trig_interval(mul(t,aiv(S)));cosx,sinx=trig_interval(mul(xx,t))
        denominator=add(mul(t,t),aiv(F(1,4)))
        bc=div(add(mul(from_iv(sh),co),mul(mul(aiv(2),t),mul(from_iv(ch),ss))),denominator)
        bs=div(sub(mul(from_iv(ch),ss),mul(mul(aiv(2),t),mul(from_iv(sh),co))),denominator)
        even=mul(sw,sub(cosx,mul(div(bc,from_iv(gp)),cw)))
        odd=mul(sw,sub(sinx,mul(div(bs,from_iv(gm)),ssw)))
        scale=phi[ii]*float(h)/float(mp.pi)
        for p,v in enumerate((even,odd)):
            center=(v[0]+v[1])/2
            err=up(np.maximum(np.abs(center-v[0]),np.abs(v[1]-center)))
            row_errors[p]=np.maximum(row_errors[p],np.max(err,axis=1))
            norm2=np.sum(center*center,axis=0);max_norm2[p]=max(max_norm2[p],float(np.max(norm2)))
            matrices[p]+=(center*scale)@center.T
    pi_lower=b.lo(mp.iv.pi);u=F(1,2**53)
    # A nonnegative exact weight and at most2nf+128 elementary roundings per dot.
    gamma=(2*nf+128)*u/(1-(2*nf+128)*u)
    floating_norm_error=32*gamma*U*T/pi_lower
    for value in max_norm2:
        if value>16:raise ValueError('absolute matrix-product budget exceeded')
    vector_eps=[b.hi(mp.iv.sqrt(b.I(sum((fq(e)**2 for e in row),F(0))))) for row in row_errors]
    if max(vector_eps)>F(1,10**6):raise ValueError('sample-frame interval budget exceeded')
    leading=F(factorial(2*N),2**N*factorial(N)**2)
    eps_interp=(F(45)**N+F(28,3)*F(1,4)**N)/(factorial(N)*leading)
    # Interpolated waves have norm <=1+eps_interp; polynomial tails share this bound.
    sample_error=[U*T/pi_lower*(2*(1+eps_interp)*e+e*e) for e in vector_eps]
    spatial_error=U*T/pi_lower*(2*eps_interp+eps_interp*eps_interp)
    table_error=radius+F(33)*H*H/8
    weight_error=table_error+F(13,2)*h/2
    midpoint_error=F(47,15)*S**3*U*T*h*h/(24*pi_lower)
    ceilings=[validated_matrix_norm(M,bits) for M in matrices]
    errors=[weight_error+midpoint_error+spatial_error+sample_error[p]+floating_norm_error+F(ceilings[p]['rounding_norm_upper']) for p in range(2)]
    norm_upper=[F(ceilings[p]['tau'])+errors[p] for p in range(2)]
    weight=log2/mp.iv.sqrt(b.I(2));c0=mp.iv.log(8*mp.iv.pi)+b.euler_enclosure()+mp.iv.pi/2
    C1=b.hi(c0+2*weight);L=b.hi(c0+weight);mass_floor=U-C1-max(norm_upper)
    certified=mass_floor>0
    return dict(status='certified_local_all_tests' if certified else 'inconclusive',S=str(S),form=port.form,metric=port.metric,unit=port.unit,
        all_tests=True,global_RH_claim=False,zero_data_used=False,U=str(U),T=str(T),frequency_step=str(h),table_step=str(H),
        frequency_cells=nf,spatial_nodes=N,parity_head_dimensions=[N//2,N//2],
        tail_interval=b.pack(tail),global_tail_floor=str(b.lo(tail)),gauss_positive_nodes=gauss,joint_table=table,
        table_error_radius=str(radius),table_interpolation_error=str(F(33)*H*H/8),weight_error=str(weight_error),
        kernel_midpoint_error=str(midpoint_error),spatial_interpolation_epsilon=str(eps_interp),spatial_operator_error=str(spatial_error),
        sample_vector_epsilon=[str(v) for v in vector_eps],sample_operator_error=[str(v) for v in sample_error],
        matrix_roundoff_gamma=str(gamma),matrix_roundoff_norm_upper=str(floating_norm_error),max_sample_norm2=max_norm2,
        finite_matrix_certificates=ceilings,total_operator_errors=[str(v) for v in errors],norm_even_odd_upper=[str(v) for v in norm_upper],
        threshold_interval=b.pack(c0+2*weight),C1_upper=str(C1),L_upper=str(L),mass_floor_lower=str(mass_floor),
        mu_R_lower=str(mass_floor/(mass_floor+L+1)) if certified else None,
        support_range='0<S<=1/2' if certified else None,
        head_source_tail_contracts=[dict(head_norm_upper=str(norm_upper[p]),tail_norm_upper=str(errors[p]),
            cross_norm_upper=str(errors[p]),source_gram_operator_upper=str(errors[p]**2),
            assembly=assemble_minorant_contract(F(ceilings[p]['tau']),errors[p],U-C1),
            scope='ambient orthogonal polynomial frame; sources of the bounded common minorant, not original unbounded Q sources') for p in range(2)],
        arithmetic_model='outward binary64 primitives, mpmath elementary intervals, gamma_n dot-product enclosure, exact integer Bareiss',
        scope='whole complex admissible form domain; analytic interpolation and operator lifting in document73; not a formal proof assistant')
