"""Rational polynomial tests and full prime-side Weil matrices.

Symbolic algebra is exact; transcendental quadratures/eigenvalues are exploratory.
No zeros are read. Supports/dimensions/precisions come from the frozen protocol.
"""
from fractions import Fraction as F
from math import comb,isqrt
import mpmath as mp

def trim(p):
    p=list(p)
    while len(p)>1 and not p[-1]:p.pop()
    return p
def add(p,q):return trim([(p[i] if i<len(p) else F(0))+(q[i] if i<len(q) else F(0)) for i in range(max(len(p),len(q)))])
def scale(p,a):return trim([F(a)*x for x in p])
def mul(p,q):
    z=[F(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):z[i+j]+=a*b
    return trim(z)
def derivative(p,n=1):
    for _ in range(n):p=[F(i)*a for i,a in enumerate(p)][1:] or [F(0)]
    return trim(p)
def integral_even(p):return sum(F(2)*a/F(i+1) for i,a in enumerate(p) if i%2==0)
def shift(p,b):
    z=[F(0)]*len(p)
    for j,a in enumerate(p):
        for k in range(j+1):z[k]+=a*comb(j,k)*F(b)**(j-k)
    return trim(z)
def evalq(p,x):
    s=F(0)
    for a in reversed(p):s=s*F(x)+a
    return s
def evalmp(p,x):
    s=mp.mpf(0)
    for a in reversed(p):s=s*x+mp.mpf(a.numerator)/a.denominator
    return s
def seed(k):return [F(0)]*k+[F(1),F(0),F(-4),F(0),F(6),F(0),F(-4),F(0),F(1)]
def test(S,k):
    S=F(S);p=seed(k)
    return add(scale(derivative(p,2),1/S**2),scale(p,F(-1,4)))
def mass(S,i,j):return F(S)*integral_even(mul(test(S,i),test(S,j)))
def metric(S,i,j):
    return mass(S,i,j)+1/F(S)*integral_even(mul(derivative(test(S,i)),derivative(test(S,j))))
def seed_metric(S,i,j):
    out=F(0)
    for n,w in [(3,F(1)),(2,F(3,2)),(1,F(9,16)),(0,F(1,16))]:
        out+=w*F(S)**(1-2*n)*integral_even(mul(derivative(seed(i),n),derivative(seed(j),n)))
    return out

def correlation(S,i,j):
    """h_ij(S*z), 0<=z<=2, by exact integral over u in[z-1,1]."""
    S=F(S);p=test(S,i);q=test(S,j);out=[F(0)]
    for a,pa in enumerate(p):
      for b,qb in enumerate(q):
       if not pa or not qb:continue
       for k in range(b+1):
        degree=a+k+1
        boundary=[F(1)]+[F(0)]*degree
        for t in range(degree+1):boundary[t]-=F(comb(degree,t))*F(-1)**(degree-t)
        term=[F(0)]*(b-k)+scale(boundary,S*pa*qb*comb(b,k)*F(-1)**(b-k)/degree)
        out=add(out,term)
    return trim(out)

def symmetric_correlation(S,i,j):return scale(add(correlation(S,i,j),correlation(S,j,i)),F(1,2))
def mpq(q):return mp.mpf(q.numerator)/q.denominator

def exp_floor_certificate(x,terms=96):
    x=F(x)
    if x<0 or x>=terms+2:raise ValueError('Taylor range')
    term=F(1);s=term
    for k in range(1,terms+1):term*=x/k;s+=term
    tail=(term*x/(terms+1))/(1-x/F(terms+2))
    lo=s.numerator//s.denominator;hi=(s+tail).numerator//(s+tail).denominator
    if lo!=hi:raise ValueError('Cutoff not certified')
    return dict(cutoff=lo,lower=str(s),upper=str(s+tail),terms=terms)

def prime_powers(X):
    flags=[True]*(X+1)
    if X>=0:flags[0]=False
    if X>=1:flags[1]=False
    for p in range(2,isqrt(X)+1):
        if flags[p]:
            for k in range(p*p,X+1,p):flags[k]=False
    rows=[]
    for p in range(2,X+1):
        if flags[p]:
            v=p;m=1
            while v<=X:rows.append((p,m,v));v*=p;m+=1
    return sorted(rows,key=lambda r:r[2])

def arch(S,i,j,alternative=False):
    Sr=F(S);S=mpq(Sr);h=symmetric_correlation(Sr,i,j);c=mpq(h[0]);rest=h[1:]
    # h-c has a zero constant and linear coefficient, before evaluation.
    assert not rest or rest[0]==0
    def difference(x):return (x/S)*evalmp(rest,x/S)
    if alternative:
        def f(x):
            if not x:return mp.mpf(0)
            return -2*mp.exp(-x/2)*difference(x)/(-mp.expm1(-2*x))
        return mp.quad(f,[0,S,2*S])+2*c*(mp.atanh(mp.exp(-S))+mp.atan(mp.exp(-S)))-(mp.log(8*mp.pi)+mp.euler+mp.pi/2)*c
    def f(x):
        if not x:return c/2
        return 2*mp.exp(-x/2)*(difference(x)-c*mp.expm1(-x/2))/(-mp.expm1(-2*x))
    return -(mp.log(4*mp.pi)+mp.euler)*c-mp.quad(f,[0,S,2*S])+2*c*mp.atanh(mp.exp(-2*S))

def matrices(S,n,digits):
    with mp.workdps(digits):
        S=F(S);cut=exp_floor_certificate(2*S);powers=prime_powers(cut['cutoff']);sm=mpq(S)
        weighted=[(mp.log(p)*mp.power(p,-mp.mpf(m)/2),mp.log(v)/sm) for p,m,v in powers]
        G=mp.matrix(n);B=mp.matrix(n);C=mp.matrix(n);A=mp.matrix(n);Pr=mp.matrix(n)
        for i in range(n):
          for j in range(i,n):
            B[i,j]=B[j,i]=mpq(metric(S,i,j));C[i,j]=C[j,i]=mpq(mass(S,i,j))
            if (i+j)%2:
                G[i,j]=G[j,i]=A[i,j]=A[j,i]=Pr[i,j]=Pr[j,i]=0;continue
            h=symmetric_correlation(S,i,j)
            first=2*sum(w*evalmp(h,z) for w,z in weighted)
            av=arch(S,i,j);G[i,j]=G[j,i]=av-first;A[i,j]=A[j,i]=av;Pr[i,j]=Pr[j,i]=first
        return dict(G=G,B=B,C=C,arch=A,primes=Pr,cutoff=cut,powers=powers)

def normalized_spectrum(G,B):
    L=mp.cholesky(B);inv=L**-1;H=inv*G*inv.T;H=(H+H.T)/2
    return mp.eigsy(H,eigvals_only=True)
def debt(M):
    n=M.rows
    if n==1:return M[0,0]
    A=M[:n-1,:n-1];c=M[:n-1,n-1];z=mp.lu_solve(A,c)
    return M[n-1,n-1]-(c.T*z)[0]
