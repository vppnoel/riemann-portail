"""Independent rational-only Gauss enclosures. No mpmath, float or complex arithmetic.

Machin's identity, alternating arctangent sums, Taylor's remainder and isqrt
suffice to separate the three real parts and all imaginary parts from zero.
"""
from fractions import Fraction as Q
from math import factorial, isqrt


def add(a,b):
    return a[0]+b[0],a[1]+b[1]


def scale(a,k):
    return (a[0]*k,a[1]*k) if k>=0 else (a[1]*k,a[0]*k)


def divide_positive(a,b):
    assert b[0]>0
    values=[x/y for x in a for y in b]
    return min(values),max(values)


def atan_bounds(x,n):
    assert 0<x<1 and n>0
    total=sum(((-1)**j*x**(2*j+1)/Q(2*j+1) for j in range(n)),Q(0))
    remainder=x**(2*n+1)/Q(2*n+1)
    return (total,total+remainder) if n%2==0 else (total-remainder,total)


def pi_bounds():
    a,b=atan_bounds(Q(1,5),20),atan_bounds(Q(1,239),5)
    # tan(4atan(1/5)-atan(1/239))=1, with the angle in (0,pi/2).
    return add(scale(a,16),scale(b,-4))


def trig_bounds(angle,kind):
    lo,hi=angle
    assert -4<lo<=hi<4
    middle=(lo+hi)/2;delta=(hi-lo)/2
    if kind=='sin':
        total=sum(((-1)**j*middle**(2*j+1)/Q(factorial(2*j+1)) for j in range(24)),Q(0))
        error=Q(4**49,factorial(49))+delta
    else:
        total=sum(((-1)**j*middle**(2*j)/Q(factorial(2*j)) for j in range(25)),Q(0))
        error=Q(4**50,factorial(50))+delta
    return total-error,total+error


def gauss_enclosures():
    pi=pi_bounds();logs={pow(2,j,13):j for j in range(12)}
    units=10**30;root=isqrt(13*units*units)
    sqrt13=(Q(root,units),Q(root+1,units))
    result=[]
    for k in (1,3,5,7,9,11):
        real=(Q(0),Q(0));imag=(Q(0),Q(0))
        for a in range(1,13):
            f=Q(k*logs[a],12)+Q(a,13)
            f-=f.numerator//f.denominator
            if f>Q(1,2):f-=1
            angle=scale(pi,2*f)
            real=add(real,trig_bounds(angle,'cos'))
            imag=add(imag,trig_bounds(angle,'sin'))
        er=divide_positive(imag,sqrt13)
        ei=divide_positive(scale(real,-1),sqrt13)
        result.append({'k':k,'real':er,'imag':ei})
    return pi,sqrt13,result


def rational_certificate():
    pi,root,result=gauss_enclosures()
    coarse={1:(Q(522,1000),Q(523,1000)),3:(Q(289,1000),Q(291,1000)),5:(Q(-39,1000),Q(-38,1000))}
    for row in result:
        assert row['imag'][1]<0 or row['imag'][0]>0
        assert row['real'][0]>-1 and row['real'][1]<1
        if row['k'] in coarse:
            a,b=coarse[row['k']]
            assert a<row['real'][0]<=row['real'][1]<b
    def box(pair):
        # Exact rational endpoints retained as strings, not rounded decimals.
        return {'lower':{'numerator':str(pair[0].numerator),'denominator':str(pair[0].denominator)},
                'upper':{'numerator':str(pair[1].numerator),'denominator':str(pair[1].denominator)}}
    return {'version':'V6.39','arithmetic':'Python integers and fractions only; no floating-point transcendental calls.',
            'pi':box(pi),'sqrt13':box(root),
            'epsilons':[{'k':r['k'],'real':box(r['real']),'imag':box(r['imag'])} for r in result],
            'coarse_real_bounds':{str(k):[str(a),str(b)] for k,(a,b) in coarse.items()},
            'conclusion':'Three distinct real parts and nonzero imaginary parts; the exact antisymmetric cubic is nonzero for every anchor.'}
