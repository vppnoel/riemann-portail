# Auteur et titulaire des droits : Vincent NOËL. Figures des articles (V6.30). A lancer depuis ce dossier.
import json, math, sys, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.size":9,"font.family":"serif","mathtext.fontset":"cm","pdf.fonttype":42})
C=str(__import__("pathlib").Path(__file__).resolve().parents[3]/"3_Preuves_et_calculs")+""; D=C+"/data"
g=0.5772156649015329; kap=2+g-math.log(4*math.pi); a3=4*kap/3; al=-0.3074; be=0.637
# Fig 1: ratio
q=json.load(open("qcurve.json")); X=np.array(q["X"],float); Q=np.array(q["Q"]); L=np.log(X)
fig,ax=plt.subplots(figsize=(5.2,3.2))
ax.plot(L,Q/(a3*L**3),"-",color="k",lw=1,label=r"$Q(X)/(\frac{4\kappa}{3}\log^3X)$, $X\leq10^7$")
ax.plot([math.log(3e7),math.log(1e8)],[221.82/(a3*math.log(3e7)**3),290.58/(a3*math.log(1e8)**3)],"ko",ms=3,label=r"$X=3\cdot10^7,\,10^8$")
LL=np.linspace(5.5,30,300); ax.plot(LL,1+al/(a3*LL)+be/(a3*LL**2),"--",color="0.4",lw=1,label=r"$1+\alpha/(a_3L)+\beta/(a_3L^2)$")
ax.axhline(1,color="0.6",lw=.6); ax.set_xlabel(r"$L=\log X$"); ax.set_ylabel("ratio"); ax.set_ylim(0.3,1.05); ax.set_xlim(5.5,30)
ax.legend(fontsize=7.5,loc="lower right",frameon=False); fig.tight_layout(); fig.savefig("art1_fig1.pdf")
# Fig 2: NB family (balayage + quatre_tiers)
b=pd.read_csv(D+"/palier_balayage.csv"); t=pd.read_csv(D+"/palier_quatre_tiers.csv")
d=pd.concat([b[["N","total"]],t[["N","total"]]]).drop_duplicates("N").sort_values("N")
fig,ax=plt.subplots(figsize=(5.2,3.0)); ax.semilogx(d.N,d.total,"o",ms=2.5,color="k"); ax.set_yscale("log")
ax.axhline(4/3,color="0.4",ls="--",lw=.8); ax.text(1.2e3,4/3*1.06,r"$4/3$",fontsize=8)
ax.set_xlabel(r"$N$"); ax.set_ylabel(r"$e_N^2\,\log N/\kappa$"); fig.tight_layout(); fig.savefig("art1_fig2.pdf")
print("valeurs",len(d),"mediane",float(np.median(d.total)))
