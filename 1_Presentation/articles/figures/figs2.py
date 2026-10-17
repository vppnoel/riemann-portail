# Auteur et titulaire des droits : Vincent NOËL. Figures des articles (V6.30). A lancer depuis ce dossier.
import sys, math, json, numpy as np, pandas as pd, matplotlib
C=str(__import__("pathlib").Path(__file__).resolve().parents[3]/"3_Preuves_et_calculs")+""
sys.path.insert(0,C+"/src"); sys.path.insert(0,C+"/scripts")
import run_prime_generator as RPG
from prime_generator import traces_from_primes, traces_from_zeros, g_hat, toeplitz_pencil
matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.size":9,"font.family":"serif","mathtext.fontset":"cm","pdf.fonttype":42})
from function_field import roots_alpha
zDH=RPG.nontrivial_zeros("DH") if hasattr(RPG,"nontrivial_zeros") else None
off=[complex(z) for z in zDH if abs(z.real-0.5)>1e-6 and z.imag>0]
print("DH off-line zeros (Im>0):",[(round(z.real,4),round(z.imag,3)) for z in sorted(off,key=lambda z:z.imag)])
print("total DH zeros",len(zDH), "max Im", max(z.imag for z in zDH))
a,h,L=0.04,0.01,600
res={}
for kind in ("zeta","L_chi5","DH"):
    M=int(math.exp(L*h+2*a))+2
    t=traces_from_primes(kind,RPG.coeff_cache(kind,M),L,h,a)
    tz=traces_from_zeros(RPG.zeros(kind),L,h,a)
    G,_=toeplitz_pencil(t,L); G=0.5*(G+G.conj().T); ev=np.sort(np.linalg.eigvalsh(G))
    res[kind]=ev; print(kind,"audit",np.max(np.abs(t-tz))/np.max(np.abs(tz)),"lam_min",ev[:4],"lam_max",ev[-1], "neg",int(np.sum(ev< -1e-11*ev[-1])))
fig,ax=plt.subplots(figsize=(5.4,3.1))
for kind,col,nm,mk in (("zeta","k",r"$\zeta$","o"),("L_chi5","0.5",r"$L(s,\chi_5)$","s"),("DH","tab:red","Davenport–Heilbronn","^")):
    ev=res[kind][:40]; ax.plot(np.arange(1,41),np.sign(ev)*np.log10(1+np.abs(ev)/1e-12),mk,ms=2.8,color=col,mfc="none" if kind!="zeta" else col,label=nm)
ax.axhline(0,color="0.6",lw=.6); ax.set_xlabel("index $k$ (eigenvalues in increasing order)")
ax.set_ylabel(r"$\mathrm{sign}(\lambda_k)\,\log_{10}(1+|\lambda_k|/10^{-12})$"); ax.legend(fontsize=7.5,frameon=False)
fig.tight_layout(); fig.savefig("art2_fig2.pdf"); fig.savefig("art2_fig2.png",dpi=110)
json.dump({k:v[:12].tolist() for k,v in res.items()},open("art2_eigs.json","w"))
# Fig 1: counts over 180 settings
df=pd.read_csv(C+"/data/carre_continu.csv")
fig,ax=plt.subplots(figsize=(5.4,3.1))
for kind,col,nm,mk,off_ in (("zeta","k",r"$\zeta$ (positive directions $-1$)","o",0.12),("L_chi5","0.5",r"$L(s,\chi_5)$","s",-0.12),("DH","tab:red","Davenport–Heilbronn","^",0)):
    s=df[df.objet==kind]; ax.scatter(s.X,s.en_trop+off_,s=9,marker=mk,facecolors="none" if kind!="zeta" else col,edgecolors=col,lw=.7,label=nm)
ax.set_xscale("log"); ax.set_xlabel(r"prime powers used, up to $X=e^{Lh+2a}$"); ax.set_ylabel("excess positive directions")
ax.legend(fontsize=7.5,frameon=False,loc="upper left"); fig.tight_layout(); fig.savefig("art2_fig1.pdf"); fig.savefig("art2_fig1.png",dpi=110)
