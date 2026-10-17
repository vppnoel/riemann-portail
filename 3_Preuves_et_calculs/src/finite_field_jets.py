"""V6.35 : corps finis d'extension et certificats exacts des jets de Hasse.

Les éléments sont encodés par leurs chiffres en base p dans F_p[u]/(m).
L'arithmétique se fait avec m irréductible, jamais modulo l'entier p**n.
Les tables sont limitées à q<=1024 ; la preuve écrite n'a pas cette limite.
"""
from __future__ import annotations
from functools import lru_cache
import math
import numpy as np

def _prime(p):
    return p>=2 and all(p%d for d in range(2,math.isqrt(p)+1))

def _trim(a):
    a=list(a)
    while len(a)>1 and a[-1]==0:a.pop()
    return a

def _rem(a,m,p):
    a=_trim([int(x)%p for x in a]);m=_trim(m)
    while len(a)>=len(m) and a!=[0]:
        h=a[-1]*pow(m[-1],p-2,p)%p;j=len(a)-len(m)
        for i,x in enumerate(m):a[j+i]=(a[j+i]-h*x)%p
        a=_trim(a)
    return a

def _pmul(a,b,p):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
    return _trim(c)

def _ppowmod(a,e,m,p):
    r=[1];a=_rem(a,m,p)
    while e:
        if e&1:r=_rem(_pmul(r,a,p),m,p)
        a=_rem(_pmul(a,a,p),m,p);e//=2
    return r

def _gcd(a,b,p):
    while b!=[0]:a,b=b,_rem(a,b,p)
    inv=pow(a[-1],p-2,p)
    return [(x*inv)%p for x in a]

def irreducible(m,p):
    if not _prime(p):return False
    m=_trim([x%p for x in m]);n=len(m)-1
    if n<1 or m[-1]!=1:return False
    x=_rem([0,1],m,p);h=x
    for j in range(1,n+1):
        h=_ppowmod(h,p,m,p)
        d=h+[0]*max(0,len(x)-len(h))
        for i,v in enumerate(x):d[i]=(d[i]-v)%p
        if j<=n//2 and len(_gcd(m,_trim(d),p))>1:return False
    return h==x

def find_modulus(p,n):
    if not _prime(p) or n<1:raise ValueError('p premier et n positif requis')
    if n==1:return (0,1)
    for a in range(1,p**n):
        coeff=tuple((a//p**i)%p for i in range(n))+(1,)
        if coeff[0] and irreducible(coeff,p):return coeff
    raise RuntimeError('Polynôme irréductible non trouvé')

class FiniteField:
    def __init__(self,p,modulus):
        if not _prime(p):raise ValueError('Caractéristique première requise')
        self.p=p;self.modulus=tuple(_trim([int(c)%p for c in modulus]))
        self.n=len(self.modulus)-1;self.q=p**self.n
        if not irreducible(self.modulus,p):raise ValueError('Corps : module irréductible monique requis')
        if self.q>1024:raise ValueError('Implémentation des tables limitée à q<=1024')
        self.digits=np.array([[(a//p**i)%p for i in range(self.n)] for a in range(self.q)],dtype=np.int32)
        self.neg=np.sum((-self.digits%p)*np.array([p**i for i in range(self.n)]),axis=1).astype(np.int32)
        self.add=np.zeros((self.q,self.q),dtype=np.int32)
        for i in range(self.n):self.add+=((self.digits[:,i,None]+self.digits[None,:,i])%p)*p**i
        if self.n==1:self.mul=(np.arange(p)[:,None]*np.arange(p)[None,:]%p).astype(np.int32)
        else:
            self.mul=np.zeros((self.q,self.q),dtype=np.int32)
            self.mul[1,:]=np.arange(self.q);self.mul[:,1]=np.arange(self.q)
            for a in range(2,self.q):
                for b in range(a,self.q):
                    c=_rem(_pmul(self.digits[a],self.digits[b],p),self.modulus,p)
                    value=sum(int(v)*p**i for i,v in enumerate(c));self.mul[a,b]=self.mul[b,a]=value
        self.inv=np.zeros(self.q,dtype=np.int32)
        for a in range(1,self.q):self.inv[a]=self.pow(a,self.q-2)
        if not np.all(self.mul[np.arange(1,self.q),self.inv[1:]]==1):raise ArithmeticError('Inverses invalides')

    def pow(self,a,e):
        if e<0:
            if a==0:raise ZeroDivisionError
            return self.pow(int(self.inv[a]),-e)
        r=1
        while e:
            if e&1:r=int(self.mul[r,a])
            a=int(self.mul[a,a]);e//=2
        return r

    def eval(self,f,x):
        r=0
        for c in reversed(f):r=int(self.add[self.mul[r,x],c])
        return r

@lru_cache(maxsize=16)
def _cached_field(p,modulus):
    return FiniteField(p,modulus)

def field(p,n,modulus=None):
    if not _prime(p) or n<1 or p**n>1024:raise ValueError('p premier, n positif et q<=1024 requis')
    modulus=find_modulus(p,n) if modulus is None else tuple(_trim([int(c)%p for c in modulus]))
    if len(modulus)-1!=n:raise ValueError('Degré du module différent de n')
    return _cached_field(p,modulus)

def poly_mul(a,b,F):
    c=np.zeros(len(a)+len(b)-1,dtype=np.int32)
    for i,x in enumerate(a):
        if x:c[i:i+len(b)]=F.add[c[i:i+len(b)],F.mul[x,np.asarray(b,dtype=np.int32)]]
    return np.array(_trim(c),dtype=np.int32)

def poly_pow(f,e,F):
    r=np.array([1],dtype=np.int32);b=np.array(f,dtype=np.int32)
    while e:
        if e&1:r=poly_mul(r,b,F)
        e//=2
        if e:b=poly_mul(b,b,F)
    return r

def square_points(f,F):
    values=np.array([F.eval(f,x) for x in range(F.q)],dtype=np.int32)
    S=[x for x,v in enumerate(values) if v and F.pow(int(v),(F.q-1)//2)==1]
    return S,int(np.sum(values==0))

def parameters(q,J,K,M):
    if q<5 or q%2==0 or not(1<=M<q and J>=1 and 1<=K<=(q-3)//2):raise ValueError('Paramètres hors du lemme')
    dimension=2*J*K;rank=M*(K+J-1)+M*(M-1)
    if dimension<=rank:raise ValueError('Existence non garantie')
    degree=(J-1)*q+K-1+3*(q-1)//2
    return dict(q=q,J=J,K=K,M=M,dimension=dimension,rang_majore=rank,
                noyau_minimal=dimension-rank,degre_max=degree,borne_S=degree//M)

def hasse_values(poly,xs,M,F):
    """Évaluation directe par coefficients binomiaux ; aucun k!^{-1}."""
    xs=np.array(xs,dtype=np.int32);powers=np.ones((len(xs),len(poly)),dtype=np.int32)
    for j in range(1,len(poly)):powers[:,j]=F.mul[powers[:,j-1],xs]
    out=np.zeros((len(xs),M),dtype=np.int32)
    for k in range(M):
        for j in range(k,len(poly)):
            c=int(F.mul[int(poly[j]),math.comb(j,k)%F.p])
            if c:out[:,k]=F.add[out[:,k],F.mul[c,powers[:,j-k]]]
    return out

def jet_matrix(f,xs,J,K,M,F):
    """Hasse-Leibniz : D^[k](uv)=sum D^[l](u) D^[k-l](v)."""
    parameters(F.q,J,K,M);xs=np.array(xs,dtype=np.int32)
    g=poly_pow(f,(F.q-1)//2,F);gd=hasse_values(g,xs,M,F)
    powers=np.ones((len(xs),max(J,K)),dtype=np.int32)
    for j in range(1,powers.shape[1]):powers[:,j]=F.mul[powers[:,j-1],xs]
    mono=np.zeros((len(xs),M,K),dtype=np.int32)
    for k in range(M):
        for a in range(k,K):mono[:,k,a]=F.mul[math.comb(a,k)%F.p,powers[:,a-k]]
    columns=[]
    for j in range(J):
        for a in range(K):
            plain=F.mul[powers[:,j,None],mono[:,:,a]]
            mixed=np.zeros((len(xs),M),dtype=np.int32)
            for k in range(M):
                for l in range(k+1):mixed[:,k]=F.add[mixed[:,k],F.mul[mono[:,k-l,a],gd[:,l]]]
            columns.extend((plain.reshape(-1),F.mul[powers[:,j,None],mixed].reshape(-1)))
    return np.array(columns,dtype=np.int32).T,g

def kernel_vector(A,F):
    A=A.copy();rows,cols=A.shape;r=0;pivots=[]
    for c in range(cols):
        ids=np.flatnonzero(A[r:,c])
        if not len(ids):continue
        pivot=r+int(ids[0]);A[[r,pivot]]=A[[pivot,r]]
        A[r,c:]=F.mul[A[r,c:],F.inv[A[r,c]]]
        ids=np.flatnonzero(A[:,c]);ids=ids[ids!=r]
        if len(ids):A[ids,c:]=F.add[A[ids,c:],F.neg[F.mul[A[ids,c,None],A[r,None,c:]]]]
        pivots.append(c);r+=1
        if r==rows:break
    free=next((i for i in range(cols) if i not in pivots),None)
    if free is None:raise ValueError('Noyau nul')
    v=np.zeros(cols,dtype=np.int32);v[free]=1
    for i,c in enumerate(pivots):v[c]=F.neg[A[i,free]]
    return r,v

def combine(v,g,J,K,F):
    out=np.zeros((J-1)*F.q+K+len(g)-1,dtype=np.int32);index=0
    for j in range(J):
        for a in range(K):
            shift=j*F.q+a
            out[shift]=F.add[out[shift],v[index]]
            out[shift:shift+len(g)]=F.add[out[shift:shift+len(g)],F.mul[v[index+1],g]]
            index+=2
    return np.array(_trim(out),dtype=np.int32)

def multiplicity(poly,x,F):
    a=_trim(poly);count=0
    if a==[0]:raise ValueError('Polynôme nul')
    while len(a)>1:
        b=[0]*(len(a)-1);b[-1]=a[-1]
        for j in range(len(b)-2,-1,-1):b[j]=int(F.add[a[j+1],F.mul[x,b[j+1]]])
        if F.add[a[0],F.mul[x,b[0]]]:break
        count+=1;a=b
    return count

def certificate(p,n,f,J,K,M,modulus=None):
    F=field(p,n,modulus);r=parameters(F.q,J,K,M)
    if len(f)!=4 or not f[-1]:raise ValueError('Cubique requise')
    S,z=square_points(f,F);A,g=jet_matrix(f,S,J,K,M,F)
    rank,v=kernel_vector(A,F);poly=combine(v,g,J,K,F)
    direct=hasse_values(poly,S,M,F);mult=[multiplicity(poly,x,F) for x in S]
    R=sum(min(len(S),K+J-1+2*k) for k in range(M))
    assert rank<=R and np.any(poly) and not np.any(direct)
    assert min(mult,default=M)>=M and M*len(S)<=len(poly)-1<=r['degre_max']
    return dict(r,p=p,n=n,module=list(F.modulus),f=list(f),S=len(S),racines_f=z,
        N=2*len(S)+z+1,conditions_naives=M*len(S),rang_exact=rank,
        rang_majore_avec_S=R,noyau_exact=r['dimension']-rank,
        degre_temoin=len(poly)-1,multiplicite_minimale=min(mult,default=M),
        points_S=S,coefficients_temoin=poly.tolist(),vecteur_noyau=v.tolist())

def tower_trace(p,t,n):
    if n==0:return 2
    a,b=2,t
    for _ in range(2,n+1):a,b=b,t*b-p*a
    return b

def spectral_status(p,t):
    """Contrôle exact de la conclusion ; ne sert pas au comptage ni à sa preuve."""
    return dict(p=p,trace=t,discriminant=t*t-4*p,hasse_exact=t*t<=4*p)
