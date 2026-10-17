"""Lemme de rang et borne de Stepanov pour les polynômes cubiques sur F_p.

Les certificats utilisent des entiers exacts. L'optimisation ne connaît ni
le nombre de points ni les racines de la courbe. Il s'agit d'une variante
élémentaire d'une méthode classique, et non d'un nouveau théorème de Weil.
"""
from __future__ import annotations
import math
import numpy as np

def rank_upper(p,J,K,M,cardinality=None):
    if not (p>=5 and 1<=M<p and J>=1 and 1<=K<=(p-3)//2):
        raise ValueError('Paramètres hors du domaine du lemme cubique')
    terms=[K+J-1+2*k for k in range(M)]
    return sum(min(cardinality,t) for t in terms) if cardinality is not None else sum(terms)

def bound(p,J,K,M):
    dim=2*J*K;rank=rank_upper(p,J,K,M)
    if dim<=rank:raise ValueError('Existence non garantie par le lemme')
    degree=(J-1)*p+K-1+3*(p-1)//2
    return dict(p=p,J=J,K=K,M=M,dimension=dim,rang_majore=rank,
                noyau_minimal=dim-rank,degre=degree,borne_S=degree//M)

def optimize(p,limit=256):
    """Minimum dans la fenêtre déclarée 1<=J,M<=limit; pas un optimum absolu."""
    best=None
    for M in range(1,min(p,limit+1)):
        for J in range(M//2+1,limit+1):
            K=M*(J+M-2)//(2*J-M)+1
            if not 1<=K<=(p-3)//2:continue
            r=bound(p,J,K,M)
            key=(r['borne_S'],r['dimension'],r['degre'],M,J,K)
            if best is None or key<best[0]:best=(key,r)
    if best is None:raise ValueError('Aucun paramétrage dans la fenêtre')
    return dict(best[1],limite_optimisation=limit)

def explicit_sqrt_parameters(p):
    """Famille J=r+1, M=2r, K=3r²-r+1, r=floor(sqrt((p-5)/6))."""
    r=math.isqrt((p-5)//6)
    if r<1:raise ValueError('p trop petit pour cette famille')
    return bound(p,r+1,3*r*r-r+1,2*r)

def polynomial_power(f,e,p):
    out=np.array([1],dtype=np.int64);b=np.array(f,dtype=np.int64)%p
    while e:
        if e&1:out=np.convolve(out,b)%p
        e>>=1
        if e:b=np.convolve(b,b)%p
    return out

def basis(p,f,J,K):
    g=polynomial_power(f,(p-1)//2,p)
    degree=(J-1)*p+K-1+len(g)-1
    polys=[]
    for j in range(J):
        for a in range(K):
            shift=j*p+a
            b=np.zeros(degree+1,dtype=np.int64);b[shift]=1;polys.append(b)
            b=np.zeros(degree+1,dtype=np.int64);b[shift:shift+len(g)]=g;polys.append(b)
    return np.array(polys).T

def square_points(f,p):
    vals=[sum(c*pow(x,i,p) for i,c in enumerate(f))%p for x in range(p)]
    return [x for x in range(p) if vals[x] and pow(vals[x],(p-1)//2,p)==1],vals.count(0)

def hasse_matrix(B,xs,M,p):
    n=B.shape[0];rows=[]
    for x in xs:
        for k in range(M):
            row=np.array([0 if i<k else math.comb(i,k)*pow(x,i-k,p)%p for i in range(n)],dtype=np.int64)
            rows.append(row@B%p)
    return np.array(rows,dtype=np.int64).reshape(len(xs)*M,B.shape[1])

def kernel_vector(A,p):
    """Réduction modulaire exacte; renvoie rang et un vecteur non nul du noyau."""
    A=A.copy()%p;rows,cols=A.shape;r=0;pivots=[]
    for c in range(cols):
        ids=np.flatnonzero(A[r:,c])
        if not len(ids):continue
        pivot=r+int(ids[0]);A[[r,pivot]]=A[[pivot,r]]
        A[r]=A[r]*pow(int(A[r,c]),p-2,p)%p
        ids=np.flatnonzero(A[:,c]);ids=ids[ids!=r]
        A[ids]=(A[ids]-A[ids,c,None]*A[r])%p
        pivots.append(c);r+=1
        if r==rows:break
    free=next((c for c in range(cols) if c not in pivots),None)
    if free is None:raise ValueError('Noyau nul')
    v=np.zeros(cols,dtype=np.int64);v[free]=1
    for i,c in enumerate(pivots):v[c]=-A[i,free]%p
    return r,v

def multiplicity(poly,x,p):
    """Division synthétique indépendante du calcul des dérivées de Hasse."""
    a=[int(t)%p for t in poly]
    while a and a[-1]==0:a.pop()
    if not a:raise ValueError('Polynôme nul')
    count=0
    while len(a)>1:
        b=[0]*(len(a)-1);b[-1]=a[-1]
        for i in range(len(b)-2,-1,-1):b[i]=(a[i+1]+x*b[i+1])%p
        if (a[0]+x*b[0])%p:break
        count+=1;a=b
    return count

def certificate(p,f,J,K,M):
    r=bound(p,J,K,M);S,z=square_points(f,p)
    B=basis(p,f,J,K);A=hasse_matrix(B,S,M,p)
    rank,v=kernel_vector(A,p);poly=B@v%p
    degree=int(np.flatnonzero(poly)[-1]);mult=[multiplicity(poly,x,p) for x in S]
    assert np.all(A@v%p==0) and min(mult,default=M)>=M
    assert rank<=rank_upper(p,J,K,M,len(S)) and M*len(S)<=degree
    return dict(r,f=f,S=len(S),racines_f=z,points_courbe=2*len(S)+z+1,
        rang_exact=rank,noyau_exact=r['dimension']-rank,
        rang_majore_avec_S=rank_upper(p,J,K,M,len(S)),
        degre_temoin=degree,multiplicite_minimale=min(mult,default=M),
        coefficients_temoin=poly[:degree+1].tolist(),vecteur_noyau=v.tolist())
