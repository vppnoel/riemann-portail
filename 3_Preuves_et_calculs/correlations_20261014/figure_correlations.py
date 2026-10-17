#!/usr/bin/env python3
"""Illustrate exact phase loss and an anchored finite energy."""
from pathlib import Path
import json,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

R=Path(__file__).resolve().parent
d=json.loads((R/'results/anchored_results.json').read_text())
h=d['homometric']
x=np.linspace(0,92,185)
def put(v):return np.maximum(x[:,None]-np.array(v)[None,:],0).sum(axis=1)
diff=put(h['A'])-put(h['B'])
with (R/'results/energy_curve.csv').open() as f:
    curve=list(csv.DictReader(f))
X=np.array([float(z['X']) for z in curve]);E=np.array([float(z['J_over_X_squared']) for z in curve])
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.right':False,'axes.spines.top':False})
fig,ax=plt.subplots(1,2,figsize=(11,4.2))
fig.patch.set_facecolor('#f4f7fa')
for a in ax:a.set_facecolor('#f4f7fa');a.grid(axis='y',alpha=.16)
ax[0].axhline(0,color='#7a8494',linewidth=.8)
ax[0].plot(x,diff,color='#9c484b',linewidth=2)
ax[0].set_title('Les mêmes paires peuvent cacher un autre signe',loc='left',fontweight='bold',fontsize=11)
ax[0].set_xlabel('Coupure t (modèle abstrait)');ax[0].set_ylabel('Potentiel A moins potentiel B')
ax[0].text(.03,.08,'Même masse, barycentre, bornes et autocorrélation.\nLes triplets et les potentiels distinguent A et B.',transform=ax[0].transAxes,fontsize=9,bbox={'facecolor':'#f4f7fa','alpha':.94,'edgecolor':'none','pad':4})
ax[1].plot(X,E,color='#17655b',linewidth=1.4)
ax[1].set_xscale('log');ax[1].set_ylim(bottom=0)
ax[1].set_title('Une énergie positive, une borne globale à trouver',loc='left',fontweight='bold',fontsize=11)
ax[1].set_xlabel('Plafond X (vrais poids premiers, X ≤ 1000)')
ax[1].set_ylabel(r'$J(X)/X^2$')
fig.text(.055,.01,'Le graphe fini ne démontre aucune borne uniforme. RH reste ouverte.',fontsize=9,color='#536476')
fig.tight_layout(rect=[0,.05,1,1],w_pad=2)
fig.savefig(R/'CORRELATIONS_VISUEL.png',dpi=190)
fig.savefig(R/'CORRELATIONS_VISUEL.svg')
