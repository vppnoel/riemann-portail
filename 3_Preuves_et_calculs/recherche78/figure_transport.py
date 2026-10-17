"""Figure scientifique : stock fini et noyau initial continu."""
from pathlib import Path
import json
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parent
reserve = json.loads((ROOT/"reserve_radiale_1000.json").read_text())
block = json.loads((ROOT/"bloc_initial_certificat.json").read_text())
xs,ys = [],[]
running = float("inf")
for row in reserve["rows"]:
    running = min(running,float(row["radial_reserve"]["midpoint"]))
    item = row["last_prime_power"]
    if item:
        xs.append(math.log(item[2]))
        ys.append(running)
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.spines.top":False,"axes.spines.right":False})
fig, axes = plt.subplots(1,2,figsize=(12,4.9),gridspec_kw={"width_ratios":[1.05,1]})
fig.patch.set_facecolor("#f8fafc")
for ax in axes:
    ax.set_facecolor("#f8fafc")
ax=axes[0]
ax.step(xs,ys,where="post",color="#146d92",lw=2.5)
ax.set_yscale("log")
ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f"{v:.3f}".replace(".",",")))
ax.set_xlabel("Échelle du préfixe : log q")
ax.set_ylabel("Stock restant au point zéro")
ax.set_title("Balayage canonique\n194 préfixes finis encadrés",loc="left",weight="bold",pad=15)
ax.grid(axis="y",alpha=.2)
rx=math.log(529);ry=float(reserve["minimum_reserve"]["midpoint"])
ax.scatter([rx],[ry],s=50,color="#b46915",zorder=5)
ax.annotate("Record : 529 = 23²\nStock ≈ 0,00481684",(rx,ry),
            xytext=(3.8,.0089),arrowprops={"arrowstyle":"->","color":"#b46915"},fontsize=10,color="#87510e")
ax.text(.03,.045,"Plafond 1000 ; aucune extrapolation",transform=ax.transAxes,fontsize=10,color="#64748b")
ax=axes[1]
t=math.log(2);l=.8409704668464286;b=1.020590318173408
c=float(block["demand_mass"]["midpoint"]);m=float(block["origin_mass"]["midpoint"])
u=np.linspace(l,b,250)
density=(np.exp(u/2)-np.exp(-2.5*u)/(1-np.exp(-2*u)))/c
ax.fill_between(u,0,density,color="#23896b",alpha=.26)
ax.plot(u,density,color="#23896b",lw=2.5)
ax.vlines([l,b],0,[density[0],density[-1]],color="#23896b",lw=1.4)
ax.axvline(t,color="#99541d",linestyle="--",lw=1.7)
ax.scatter([0],[.15],s=190,color="#146d92",zorder=5)
ax.annotate(f"Atome en 0\n{m/c:.1%} de la ligne".replace(".",","),(0,.15),
            xytext=(.11,1.08),arrowprops={"arrowstyle":"->","color":"#146d92"},color="#146d92",fontsize=10)
ax.text(.54,4.31,"Centre moyen T = log 2",color="#99541d",fontsize=10)
ax.text(.76,1.52,"Matière continue\nsur [ℓ, b]",fontsize=11,color="#146449")
ax.set_title("Une première ligne non minimale\nTout l'atome zéro est consommé",loc="left",weight="bold",pad=15)
ax.set_xlabel("Position du matériau utilisé : u")
ax.set_ylabel("Densité de probabilité de la partie continue")
ax.set_xlim(-.07,1.16);ax.set_ylim(0,4.7)
ax.set_xticks([0,t,l,b,math.log(3)]);ax.set_xticklabels(["0","T","ℓ","b","log 3"])
fig.text(.625,.027,"Racines encadrées ; b < log 3",fontsize=10,color="#64748b")
fig.subplots_adjust(left=.08,right=.98,bottom=.19,top=.82,wspace=.33)
fig.savefig(ROOT/"78_CARTE_TRANSPORT.png",dpi=180)
fig.savefig(ROOT/"78_CARTE_TRANSPORT.svg")
