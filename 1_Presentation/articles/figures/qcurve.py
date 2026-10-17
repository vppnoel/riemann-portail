# Auteur et titulaire des droits : Vincent NOËL. Figures des articles (V6.30). A lancer depuis ce dossier.
import numpy as np, json, time
NMAX=10**7; g=0.5772156649015329
t=time.time()
spf=np.zeros(NMAX+1,dtype=np.int32)
for p in range(2,int(NMAX**.5)+1):
    if spf[p]==0:
        idx=np.arange(p*p,NMAX+1,p); m=spf[idx]==0; spf[idx[m]]=p
n=np.arange(NMAX+1); pr=(spf==0)&(n>=2); spf[pr]=n[pr]
m=n.copy(); p=spf.copy(); p[:2]=1
act=n>=2
while True:
    d=act&(m%p==0)&(m>1)
    if not d.any(): break
    m[d]//=p[d]
rest=m
q=np.where(rest>1,spf[np.maximum(rest,0)],1)
m2=rest.copy(); act2=rest>1
while True:
    d=act2&(m2%q==0)&(m2>1)
    if not d.any(): break
    m2[d]//=q[d]
c=np.zeros(NMAX+1)
lp=np.log(np.maximum(p,1)); lq=np.log(np.maximum(q,1))
pp=(n>=2)&(rest==1); c[pp]=-lp[pp]**2+2*g*lp[pp]
two=(n>=2)&(rest>1)&(m2==1); c[two]=2*lp[two]*lq[two]
C=np.cumsum(c)
k=np.arange(1,NMAX+1); w=C[1:]**2*(1/k-1/(k+1)); Qc=np.concatenate([[0],np.cumsum(w)])  # Qc[X-1]=sum_{n<X}
Xs=np.unique(np.round(np.logspace(np.log10(300),7,120)).astype(int))
Q=[float(Qc[X-1]) for X in Xs]
json.dump(dict(X=Xs.tolist(),Q=Q,maxC_over_sqrtx_log2=float(np.max(np.abs(C[1000:])/(np.sqrt(n[1000:])*np.log(n[1000:])**2)))),open("qcurve.json","w"))
for X in (300,1000,10**4,10**5,10**6,4*10**6-1,10**7): print(X,Qc[X-1])
print(time.time()-t)
