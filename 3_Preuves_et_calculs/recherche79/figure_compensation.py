#!/usr/bin/env python3
"""Static scientific figure from the archived finite diagnostics."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
d=json.loads((ROOT/'results/compensation_diagnostics.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(1,2,figsize=(10.8,4.3),gridspec_kw={'width_ratios':[1.2,1]})
fig.patch.set_facecolor('#f5f7fa')
for ax in axes:
    ax.set_facecolor('#f5f7fa')
    ax.axhline(0,color='#667085',linewidth=.8)
    ax.grid(axis='y',alpha=.17)
x=np.array([float(b['left']) for b in d['blocks']])
real=np.array([float(b['actual_min']) for b in d['blocks']])
guard=np.array([float(b['guard']) for b in d['blocks']])
axes[0].plot(x,real,'o-',color='#17655b',label='Plus petit défaut réel du bloc',linewidth=2,markersize=5)
axes[0].plot(x,guard,'s-',color='#b4443d',label='Garde avec support, masse et moment',linewidth=2,markersize=5)
axes[0].set_xscale('log',base=2)
axes[0].set_xticks([2,8,32,128,512],['2','8','32','128','512'])
axes[0].set_xlabel('Début du bloc X (le dernier finit à 1000)')
axes[0].set_ylabel('Défaut / garde')
axes[0].set_title('Un bon bloc peut avoir une mauvaise garde',loc='left',fontweight='bold',pad=12)
axes[0].legend(loc='lower left',fontsize=8.7,frameon=False)
r=d['refinements']
parts=[a['parts_per_block'] for a in r]
g=[float(a['minimum_guard']) for a in r]
axes[1].plot(parts,g,'o-',color='#254d83',linewidth=2)
axes[1].set_xscale('log',base=2)
axes[1].set_xticks(parts,[str(p) for p in parts])
axes[1].set_xlabel('Nombre de parties logarithmiques par bloc')
axes[1].set_title('Le profil intérieur rétablit la garde finie',loc='left',fontweight='bold',pad=12)
axes[1].annotate('8 parties : 53 gardes positives\nVérification distincte par intervalles',xy=(8,g[3]),xytext=(6,-.52),
                 arrowprops={'arrowstyle':'->','color':'#254d83'},color='#254d83',fontsize=9)
fig.text(.06,.01,'q ≤ 1000 seulement. L’obstruction asymptotique interdit l’extrapolation à toutes les échelles.',fontsize=9,color='#475467')
fig.tight_layout(rect=[0,.05,1,1],w_pad=2)
fig.savefig(ROOT/'79_COMPENSATION_VISUEL.png',dpi=190)
fig.savefig(ROOT/'79_COMPENSATION_VISUEL.svg')
