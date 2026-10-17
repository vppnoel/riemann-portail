#!/usr/bin/env python3
"""Anchored correlations, exact fingerprints and finite diagnostics.

No zeta zeros are used. Prime-energy values are diagnostic mpmath arithmetic;
the homometric countermodel and divisor identities are checked with integers.
The Mobius-kernel sign uses a separate directed interval evaluation.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
import argparse
import csv
import json
import mpmath as mp


def factor(n):
    out={};p=2
    while p*p<=n:
        while n%p==0:
            out[p]=out.get(p,0)+1;n//=p
        p+=1
    if n>1:out[n]=out.get(n,0)+1
    return out


def divisors(n):
    d=[1]
    for p,k in factor(n).items():
        d=[a*p**j for a in d for j in range(k+1)]
    return d


def mobius(n):
    f=factor(n)
    return 0 if any(k>1 for k in f.values()) else (-1)**len(f)


def symbolic_lambda(n):
    f=factor(n)
    return {next(iter(f)):1} if len(f)==1 else {}


def homometric_test():
    p=[0,30,80];q=[0,1,6,8,10];r=[10-x for x in q]
    a=sorted(x+y for x in p for y in q)
    b=sorted(x+y for x in p for y in r)
    assert len(set(a))==len(a)==len(set(b))==len(b)==15
    def ac(v):return Counter(x-y for x in v for y in v)
    def triple(v,h,k):
        s=set(v)
        return sum(x+h in s and x+k in s for x in s)
    def put(v,t):return sum(max(F(t)-x,F(0)) for x in v)
    assert ac(a)==ac(b)
    assert sum(a)==sum(b)==625
    assert min(a)==min(b)==0 and max(a)==max(b)==90
    assert put(a,3)==5 and put(b,3)==4
    assert put(a,7)==14 and put(b,7)==15
    assert triple(a,1,6)==3 and triple(b,1,6)==0
    return dict(A=a,B=b,mass=15,first_moment=625,support_min=0,support_max=90,
                all_signed_pair_difference_counts_identical=True,
                pair_counts={str(k):v for k,v in sorted(ac(a).items())},
                triple_1_6=[3,0],potentials_at_3=[5,4],potentials_at_7=[14,15],
                common_source_A_signal_B_at_7=-1,
                status='exact integer and rational algebra; abstract measures, not prime coefficients')


def unit_profile_countermodel():
    # a(1)=0 and a(n)=1 for n>=2.  Its global error has |E_a|<=2.
    iv=mp.iv
    def I(x):
        x=F(x);return iv.mpf(x.numerator)/x.denominator
    def endpoint(t):
        sign,man,exp,bc=t
        return F((-1 if sign else 1)*man)*F(2)**exp
    n=1024;hn=sum((F(1,k) for k in range(1,n+1)),F(0))
    upper=I(hn)-iv.log(I(n))-I(F(1,2*n))+I(F(1,12*n*n))
    lower=I(endpoint(upper._mpi_[0])-F(1,120*n**4))
    gamma=iv.mpf([lower.a,upper.b])
    constant=iv.log(8*iv.pi)+gamma+iv.pi/2
    t=iv.log(I(1000));b=F(257,2)
    tail=iv.exp(-I(b)*t)/(I(b*b)*(1-iv.exp(-2*t)))
    series=sum((iv.exp(-I(F(2*k)+F(1,2))*t)/I((F(2*k)+F(1,2))**2)
                for k in range(64)),I(0))+iv.mpf([0,tail.b])
    A=4*(iv.exp(t/2)+iv.exp(-t/2)-2)-constant*t/2+iv.pi**2/4+2*iv.catalan-series
    P=sum(((t-iv.log(I(j)))/iv.sqrt(I(j)) for j in range(2,1001)),I(0))
    lo,hi=map(endpoint,(A-P)._mpi_)
    assert hi<0
    return dict(profile='a(1)=0; a(n)=1 for every n>=2',psi='floor(x)-1 for x>=1',
                global_energy_bound='J_a(X)<=4*(X-1)<=4*X^2 for X>=1',
                exact_divisor_identity_fails_at_n2=True,
                same_Suzuki_archimedean_A=True,
                signal_at_log1000_lower=str(lo),signal_at_log1000_upper=str(hi),
                negative_certified=True,not_RH_counterexample=True,
                interval_model='mpmath.iv 400 bits; directed Euler remainder; positive geometric archimedean tail')


def run(bound,digits,out):
    mp.mp.dps=digits;mp.iv.prec=400
    lam={n:mp.log(next(iter(factor(n)))) for n in range(2,bound+1) if len(factor(n))==1}
    good=bad=0
    for n in range(1,bound+1):
        signature=Counter()
        for d in divisors(n):signature.update(symbolic_lambda(d))
        assert dict(signature)==factor(n)
        good+=1
        fake=signature.copy()
        if n%2==0:fake[2]+=1
        if dict(fake)!=factor(n):bad+=1
    points=sorted(lam)
    def positive_energy(X):
        before=mp.mpf(1);psi=mp.mpf(0);total=mp.mpf(0)
        for x in [n for n in points if n<=X]+[X]:
            width=mp.mpf(x)-before
            total+=width*((psi-(before+x)/2)**2+width**2/12)
            psi+=lam.get(x,0) if x!=X else 0
            before=mp.mpf(x)
        return total
    def correlated_energy(X):
        picked=[n for n in points if n<=X]
        pair=sum((lam[m]*lam[n]*(X-max(m,n)) for m in picked for n in picked),mp.mpf(0))
        anchor=sum((lam[n]*(X**2-n**2) for n in picked),mp.mpf(0))
        background=mp.mpf(X**3-1)/3
        return pair-anchor+background,pair,anchor,background
    samples=[]
    for X in [10,100,bound]:
        if X>bound:continue
        J=positive_energy(X)
        reconstructed,pair,anchor,background=correlated_energy(X)
        err=abs(J-reconstructed)
        assert err<mp.mpf(10)**(-digits+14)
        samples.append(dict(X=X,J=mp.nstr(J,35),J_over_X_squared=mp.nstr(J/X**2,35),
                            correlation_reconstruction_error=mp.nstr(err,8),
                            quadratic_pair_term=mp.nstr(pair,35),
                            linear_anchor_term=mp.nstr(anchor,35),background=mp.nstr(background,35)))
    iv=mp.iv
    v=iv.log(iv.mpf(15))
    K=sum((iv.mpf(mobius(d))/iv.sqrt(iv.mpf(d))*(v-iv.log(iv.mpf(d))) for d in range(1,16)),iv.mpf(0))
    def binary(t):
        sign,man,exp,bc=t
        return F((-1 if sign else 1)*man)*F(2)**exp
    klo,khi=map(binary,K._mpi_)
    assert khi<0
    result=dict(cutoff=bound,digits=digits,prime_power_count=len(points),
                true_divisor_identity_exact_count=good,
                fake_profile='a(2)=2*Lambda(2), a(n)=Lambda(n) otherwise',
                fake_first_divisor_violation_at_n=2,fake_divisor_violations=bad,
                energies=samples,homometric=homometric_test(),
                mobius_kernel_at_log15=dict(lower=str(klo),upper=str(khi),negative_certified=True,
                                             model='mpmath.iv 400 bits; exact Mobius coefficients; log and sqrt intervals'),
                RH_proved=False,global_energy_bound_proved=False,
                new_global_sign_estimate_found=False,
                known_reduction='RH iff J(X)=O(X^2), with J=integral_1^X(psi-x)^2')
    out.mkdir(parents=True,exist_ok=True)
    (out/'anchored_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    (out/'unit_profile_countermodel.json').write_text(json.dumps(unit_profile_countermodel(),ensure_ascii=False,indent=2)+'\n')
    with (out/'energy_curve.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['X','J_over_X_squared'])
        for X in range(2,bound+1):w.writerow([X,mp.nstr(positive_energy(X)/X**2,28)])
    print(json.dumps({k:v for k,v in result.items() if k not in ['homometric','mobius_kernel_at_log15']},ensure_ascii=False,indent=2))
    print('Homometric model: pair identity exact, triple and anchored potentials differ.')
    print('Directed Mobius kernel:',mp.nstr(mp.mpf(klo.numerator)/klo.denominator,20),
          mp.nstr(mp.mpf(khi.numerator)/khi.denominator,20))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cutoff',type=int,default=1000)
    p.add_argument('--digits',type=int,default=70)
    p.add_argument('--output',type=Path,default=Path('results'))
    a=p.parse_args()
    if a.cutoff<15:p.error('cutoff must be at least 15')
    run(a.cutoff,a.digits,a.output)
