"""Exact phase bookkeeping and interval-certified joint edge payment.

The certified output bounds |Q_pr|/arch_energy, not the sign of Q_W.
All overlap multiplicities are retained. No zero data or RH assumption.
"""
from fractions import Fraction as F
from math import isqrt
import mpmath as mp
import prime_centered_bridge as b
from certificate_lego import J_interval

def prime_power(n):
    if isinstance(n,bool) or not isinstance(n,int) or n<2:
        raise ValueError('integer n>=2 required')
    p=next((d for d in range(2,isqrt(n)+1) if n%d==0),n)
    q=n;m=0
    while q%p==0:q//=p;m+=1
    return (p,m,n) if q==1 else None

def active_powers(S,limit=10000):
    S=F(S)
    if S<=0:raise ValueError('positive support required')
    cap=b.hi(mp.iv.exp(b.I(2*S)))
    if cap>=limit:raise ValueError('explicit enumeration resource ceiling reached')
    records=[]
    for n in range(2,cap.numerator//cap.denominator+1):
        item=prime_power(n)
        if item is None:continue
        d=mp.iv.log(b.I(n))
        if b.lo(d)<=2*S<=b.hi(d):raise ValueError('activation threshold unresolved')
        if b.hi(d)<2*S:
            p,m,n=item;records.append(dict(p=p,m=m,q=n,shift=d,weight=mp.iv.log(b.I(p))/mp.iv.sqrt(b.I(n))))
    return records

def joint_multiplier(t,S,K=256):
    t=F(t)
    return b.multiplier_enclosure(t,K)+sum((2*r['weight']*(1-mp.iv.cos(b.I(t)*r['shift'])) for r in active_powers(S)),b.I(0))

def potential(S,x):
    S=F(S)
    return J_interval(b.I(S)-x)+J_interval(b.I(S)+x)

def joint_edge_payment(S,only_q=None):
    """Uniform interval upper bound for sup D_S(x)/V_S(x).

    D_q=w_q(1_{x<=S-d_q}+1_{x>=d_q-S}); overlapping bands count twice.
    V is even convex, hence increasing on [0,S]; D is stepwise constant.
    Every segment's supremum is its right-hand density divided by V(left).
    """
    S=F(S);records=active_powers(S)
    if only_q is not None:
        wanted=set(only_q)
        if not wanted.issubset({r['q'] for r in records}):raise ValueError('requested term not active')
        records=[r for r in records if r['q'] in wanted]
    points=[]
    for r in records:
        d=r['shift']
        if b.hi(d)<S:
            a=b.I(S)-d;direction='minus';initial=2
        elif b.lo(d)>S:
            a=d-b.I(S);direction='plus';initial=0
        else:raise ValueError('overlap threshold unresolved')
        points.append((a,r,direction,initial))
    points.sort(key=lambda z:b.lo(z[0]))
    for i in range(1,len(points)):
        if b.hi(points[i-1][0])>=b.lo(points[i][0]):raise ValueError('breakpoint order unresolved')
    density=sum((initial*r['weight'] for a,r,direction,initial in points),b.I(0))
    previous=b.I(0);segments=[];lower=F(0);upper=F(0)
    for a,r,direction,initial in points+[(b.I(S),None,None,None)]:
        if b.hi(density)>0:
            ratio=density/potential(S,previous)
            lower=max(lower,b.lo(ratio));upper=max(upper,b.hi(ratio))
            segments.append(dict(left=b.pack(previous),right=b.pack(a),density=b.pack(density),
                ratio=b.pack(ratio),ratio_lower=str(b.lo(ratio)),ratio_upper=str(b.hi(ratio))))
        if r is not None:
            density+=r['weight'] if direction=='plus' else -r['weight']
        previous=a
    return dict(S=str(S),status='certified_joint_relative_arithmetic_payment',
        inequality='abs(Q_pr(f)) <= alpha_upper * arch_energy(f)',
        alpha_lower=str(lower),alpha_upper=str(upper),active_q=[r['q'] for r in records],
        alpha_lower_scope='lower bound of the spatial envelope supremum only; not the arithmetic operator norm',
        terms=[dict(p=r['p'],m=r['m'],q=r['q'],shift=b.pack(r['shift']),weight=b.pack(r['weight'])) for r in records],
        segments=segments,overlap_multiplicity_retained=True,all_complex_finite_energy_tests=True,
        global_RH_claim=False,Q_positive_certified=False,zero_data_used=False)

def sufficient_sign(alpha_upper,energy_floor,c0_upper):
    """Conditional algebra: an independently certified energy floor is required."""
    alpha,lam,c0=map(F,(alpha_upper,energy_floor,c0_upper))
    if alpha<0 or lam<0 or c0<=0:raise ValueError('valid nonnegative premises required')
    if alpha>=1:return dict(status='inconclusive',reason='coefficient of energy not positive',global_RH_claim=False)
    margin=(1-alpha)*lam-c0
    return dict(status='positive_if_energy_premise_certified' if margin>0 else 'inconclusive',
        mass_floor=str(margin),premises_authenticated=False,global_RH_claim=False)

def derivative_budgets(S):
    r=active_powers(S)
    first=F(21,16)*F(109,25)+sum((b.hi(2*x['weight']*x['shift']) for x in r),F(0))
    second=F(4052,125)+sum((b.hi(2*x['weight']*x['shift']**2) for x in r),F(0))
    return dict(first_upper=str(first),second_upper=str(second),
        use='joint table interpolation and frequency-cell operator errors',
        does_not_certify_infinite_operator_norm=True)
