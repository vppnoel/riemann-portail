"""Exact rational real-symmetric Schur contracts. No arithmetic sign is assumed."""
from fractions import Fraction as F


def matrix(A):
    A=[[F(x) for x in r] for r in A];n=len(A)
    if any(len(r)!=n for r in A) or any(A[i][j]!=A[j][i] for i in range(n) for j in range(n)):
        raise ValueError('Square symmetric matrix required')
    return A


def psd(A):
    A=matrix(A)
    while A:
        p=A[0][0];c=A[0][1:]
        if p<0:return False
        if p==0:
            if any(c):return False
            A=[r[1:] for r in A[1:]]
        else:
            A=[[A[i][j]-A[i][0]*A[0][j]/p for j in range(1,len(A))]
               for i in range(1,len(A))]
    return True


def linear_solution(A,c):
    n=len(A)
    if len(c)!=n:raise ValueError('Dimension mismatch')
    rows=[list(r)+[F(v)] for r,v in zip(A,c)];pivots=[];i=0
    for j in range(n):
        k=next((k for k in range(i,n) if rows[k][j]),None)
        if k is None:continue
        rows[i],rows[k]=rows[k],rows[i];d=rows[i][j];rows[i]=[x/d for x in rows[i]]
        for k in range(n):
            if k!=i:
                d=rows[k][j];rows[k]=[x-d*y for x,y in zip(rows[k],rows[i])]
        pivots.append(j);i+=1
    if any(not any(r[:-1]) and r[-1] for r in rows):return None
    x=[F(0) for _ in range(n)]
    for i,j in enumerate(pivots):x[j]=rows[i][-1]
    return x


def append_contract(G,c,a):
    G=matrix(G);c=list(map(F,c));a=F(a)
    if len(c)!=len(G):raise ValueError('Dimension mismatch')
    if not psd(G):return dict(accepted=False,reason='old_block_not_psd',debt=None)
    z=linear_solution(G,c)
    if z is None:return dict(accepted=False,reason='coupling_outside_range',debt=None)
    debt=a-sum(ci*zi for ci,zi in zip(c,z))
    return dict(accepted=debt>=0,reason='nonnegative_debt' if debt>=0 else 'negative_debt',
                debt=debt,solution=z)


def quadratic(A,x):
    return sum(F(x[i])*F(A[i][j])*F(x[j]) for i in range(len(x)) for j in range(len(x)))
