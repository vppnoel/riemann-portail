"""Certified joint-frequency concentration with one common annihilator Gram.

Analytic premises are proved in V647_CONCENTRATION_PROJETEE.md. Elementary
functions are outward intervals; all pair arithmetic is exact fixed point.
This is a reproducible analytic/numeric certificate, not a formal prover.
"""
from fractions import Fraction as F
import mpmath as mp
import prime_centered_bridge as b
from certificate_lego import Port

def ceilq(x):
    x=F(x);return -(-x.numerator//x.denominator)

def fixed(v,bits):
    if not isinstance(bits,int) or isinstance(bits,bool) or bits<1:raise ValueError('positive integer fixed bits required')
    q=1<<bits
    return (int((b.lo(v)*q).__floor__()),ceilq(b.hi(v)*q))

def product_interval(x,y,q):
    if not isinstance(q,int) or isinstance(q,bool) or q<=0:raise ValueError('positive integer scale required')
    p=(x[0]*y[0],x[0]*y[1],x[1]*y[0],x[1]*y[1])
    return min(p)//q,-(-max(p)//q)

def projected_kernel_fixed(raw_diff,raw_sum,pi,pj,q,parity):
    prod=product_interval(pi,pj,q)
    if parity==0:
        low=raw_diff[0]+raw_sum[0]-prod[1]
        high=raw_diff[1]+raw_sum[1]-prod[0]
    elif parity==1:
        low=raw_diff[0]-raw_sum[1]-prod[1]
        high=raw_diff[1]-raw_sum[0]-prod[0]
    else:raise ValueError('parity is zero or one')
    return low,high

def validate_grid(port,T,h,U,du,bits):
    if not isinstance(port,Port):raise ValueError('typed domain port required')
    if port.form!='Q_W' or port.mass_shift or port.metric!='R=mass+arch_energy' or port.unit!='A_amp^2' or port.annihilators!=('cosh(x/2)','sinh(x/2)'):
        raise ValueError('the exact Q_W, R, units and two moments are required')
    if not all(isinstance(x,F) for x in (T,h,U,du)):raise ValueError('rational grid required')
    if not isinstance(bits,int) or isinstance(bits,bool) or min(T,h,U,du)<=0 or (T/h).denominator!=1 or (U/du).denominator!=1 or bits<32:
        raise ValueError('positive aligned rational grid and at least32 fixed bits required')
    log2=mp.iv.log(b.I(2));log3=mp.iv.log(b.I(3))
    if not b.hi(log2)<2*port.S<min(b.lo(log3),b.lo(2*log2)):
        raise ValueError('one prime and disjoint edge bands required')
    tail=b.multiplier_enclosure(T)
    if b.lo(tail)<=U:raise ValueError('global sublevel tail exclusion not certified')
    return tail

def certify(port,T=F(40),h=F(1,50),U=F(36,5),du=F(1,50),bits=64,progress=None):
    """Whole-domain lower bound via trace and Schatten2 on cell supersets.

    Cell i belongs to a sublevel superset whenever its certified b-floor is
    below the layer level. No estimated root or omitted-frequency minimum is
    used. Positive layers beyond U are omitted, never subtracted.
    """
    tail=validate_grid(port,T,h,U,du,bits);S=port.S;N=int(T/h);q=1<<bits
    s=b.I(S);shift=mp.iv.log(b.I(2));weight=shift/mp.iv.sqrt(b.I(2))
    sh=(mp.iv.exp(s)-mp.iv.exp(-s))/2;gp=s+sh;gm=sh-s
    if b.lo(gm)<=0:raise ValueError('positive annihilator Gram required')
    roots=[mp.iv.sqrt(gp),mp.iv.sqrt(gm)]
    shalf=(mp.iv.exp(s/2)-mp.iv.exp(-s/2))/2
    chalf=(mp.iv.exp(s/2)+mp.iv.exp(-s/2))/2
    sinc=[fixed(b.I(S),bits)]
    for k in range(1,2*N):
        z=b.I(k*h);sinc.append(fixed(mp.iv.sin(s*z)/z,bits))
    moments=[[],[]];floors=[]
    for i in range(N):
        t=(i+F(1,2))*h;v=b.I(t);co=mp.iv.cos(s*v);si=mp.iv.sin(s*v);den=v*v+b.I(F(1,4))
        bc=(shalf*co+2*v*chalf*si)/den
        bs=(chalf*si-2*v*shalf*co)/den
        for p,value in enumerate((bc,bs)):moments[p].append(fixed(value/roots[p],bits))
        cell=b.I(i*h)+mp.iv.mpf([0,1])*b.I(h)
        phase=2*weight*(1-mp.iv.cos(shift*cell))
        # a is increasing; the positive phase is enclosed on the whole cell.
        floors.append(max(F(0),b.lo(b.multiplier_enclosure(i*h))+max(F(0),b.lo(phase))))
    order=sorted(range(N),key=lambda i:(floors[i],i))
    if progress:progress('elementary intervals complete; exact pair accumulation')
    pi_lower=b.lo(mp.iv.pi);pi_upper=b.hi(mp.iv.pi)
    # 1/sqrt5 <9/20; rational derivative constants dominate both parities.
    trace_d2=F(47,15)*S**3;kernel_d2=F(94,15)*S**4
    sums=[0,0];diag=[0,0];selected=[];cursor=0;rows=[];lambdas=[F(0),F(0)];trace_lambdas=[F(0),F(0)]
    for layer in range(1,int(U/du)+1):
        u=layer*du
        while cursor<N and floors[order[cursor]]<u:
            i=order[cursor];cursor+=1
            for p in range(2):
                k=projected_kernel_fixed(sinc[0],sinc[2*i+1],moments[p][i],moments[p][i],q,p)
                diag[p]+=max(0,k[1]);sums[p]+=max(abs(k[0]),abs(k[1]))**2
                for j in selected:
                    k=projected_kernel_fixed(sinc[abs(i-j)],sinc[i+j+1],moments[p][i],moments[p][j],q,p)
                    sums[p]+=2*max(abs(k[0]),abs(k[1]))**2
            selected.append(i)
        A=len(selected)*h;trace_error=trace_d2*A*h*h/(24*pi_lower)
        hs_error=kernel_d2*A*A*h*h/(12*pi_lower*pi_lower)
        trace_upper=[h*F(v,q)/pi_lower+trace_error for v in diag]
        hs_squared=[h*h*F(v,q*q)/(pi_lower*pi_lower)+hs_error for v in sums]
        hs_upper=[b.hi(mp.iv.sqrt(b.I(v))) for v in hs_squared]
        rho=[min(F(1),trace_upper[p],hs_upper[p]) for p in range(2)]
        for p in range(2):
            lambdas[p]+=du*(1-rho[p]);trace_lambdas[p]+=du*(1-min(F(1),trace_upper[p]))
        rows.append(dict(u=str(u),cell_count=len(selected),measure_upper=str(A),
            trace_upper=[str(v) for v in trace_upper],hs_squared_upper=[str(v) for v in hs_squared],
            rho_upper=[str(v) for v in rho],trace_error=str(trace_error),hs_squared_error=str(hs_error),
            joint_energy_cumulative_lower=[str(v) for v in lambdas]))
    c0=mp.iv.log(8*mp.iv.pi)+b.euler_enclosure()+mp.iv.pi/2
    threshold=b.hi(c0+2*weight);lam=min(lambdas);c=lam-threshold;L=b.hi(c0+weight)
    certified=c>0
    # Q>=c*m and Q>=E-L*m imply Q>=c/(c+L+1)*R.
    mu=c/(c+L+1) if certified else None
    return dict(S=str(S),form=port.form,metric=port.metric,unit=port.unit,
        status='certified_local_all_tests' if certified else 'inconclusive',all_tests=True,
        frequency_cells=N,used_cells=len(selected),pair_count_each_parity=len(selected)*(len(selected)+1)//2,
        T=str(T),h=str(h),U=str(U),du=str(du),fixed_bits=bits,interval_bits=mp.iv.prec,
        global_tail_floor=str(b.lo(tail)),global_tail_interval=b.pack(tail),
        gram_intervals=[b.pack(gp),b.pack(gm)],pi_interval=b.pack(mp.iv.pi),
        weight_interval=b.pack(weight),c0_interval=b.pack(c0),threshold_upper=str(threshold),
        trace_second_derivative_upper=str(trace_d2),kernel_squared_second_derivative_upper=str(kernel_d2),
        joint_energy_even_odd_lower=[str(v) for v in lambdas],joint_energy_lower=str(lam),
        trace_only_even_odd_lower=[str(v) for v in trace_lambdas],
        trace_only_mass_floor=str(min(trace_lambdas)-threshold),mass_floor_lower=str(c),
        mu_R_lower=str(mu) if mu is not None else None,
        support_range='0<S<='+str(S) if certified else None,head_dimension=0 if certified else None,
        scope='all complex tests on bounded admissible form domain; analytic lemmas supplied in document72',
        global_RH_claim=False,zero_data_used=False,rows=rows)

def common_operator_floor(U,Cnorm_upper,threshold_upper):
    """Algebraic port for integrating operators before taking their norm.

    C must be the certified common projected weighted operator, not an average
    of unrelated optimal vectors. This function supplies no analytic norm.
    """
    U,Cnorm_upper,threshold_upper=map(F,(U,Cnorm_upper,threshold_upper))
    if U<=0 or Cnorm_upper<0 or threshold_upper<0:raise ValueError('positive cutoff and nonnegative bounds required')
    return U-Cnorm_upper-threshold_upper

def head_tail_norm_bound(head_upper,tail_upper,cross_squared_upper):
    """Conditional operator bound from complete head/tail/cross premises.

    Orthogonal head projection and orthonormal head coordinates are required.
    Reuses source residuals for the cross block. Rational matrix algebra does
    not itself certify an infinite tail, a source, or a Galerkin compression.
    """
    a,d,r2=map(F,(head_upper,tail_upper,cross_squared_upper))
    if min(a,d,r2)<0:raise ValueError('nonnegative operator bounds required')
    return b.hi((b.I(a+d)+mp.iv.sqrt(b.I((a-d)**2+4*r2)))/2)
