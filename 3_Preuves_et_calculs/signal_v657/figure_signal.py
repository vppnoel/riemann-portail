"""Figure de diagnostic : certificats de cellules et information de phase."""
from pathlib import Path
import json,math
from fractions import Fraction
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).parent
r=json.loads((D/'resolution_resultats.json').read_text());g=json.loads((D/'v657_signal_couplings_resultats.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,(a,b)=plt.subplots(2,1,figsize=(10,7.4),gridspec_kw={'height_ratios':[1.15,1]});fig.patch.set_facecolor('#faf8f1')
for ax in [a,b]:ax.set_facecolor('#faf8f1');ax.grid(True,color='#cec9bb',linewidth=.5,alpha=.65)
T0,T1=math.log(2),math.log(1000)
x=[];y=[]
for row in r['leaves']:
 l=T0+float(Fraction(row['u_a']))*(T1-T0);h=T0+float(Fraction(row['u_b']))*(T1-T0)
 a.fill_between([l,h],0,row['lower_bound_float'],color='#22644b',alpha=.6)
 # Numerical display of certified interval midpoints; interval widths are in JSON.
 x.append(l);y.append(float(row['S_a']['midpoint']))
x.append(T1);y.append(float(r['leaves'][-1]['S_b']['midpoint']))
a.plot(x,y,'o-',color='#16483a',ms=3,lw=1,label='Valeurs encadrées aux 45 bords')
a.axhline(.001,color='#a76d28',ls='--',lw=1,label='Borne 1/1000 sur toute la fenêtre')
a.set(xlabel='t (échelle logarithmique)',ylabel='Signal scalaire S(t)',title='44 cellules : les intervalles verts contrôlent aussi l’espace entre les points',xlim=(T0,T1));a.legend(loc='upper left',fontsize=8)
S=[];ratio=[]
for row in g['supports']:
 S.append(float(Fraction(row['S'])));ratio.append(float(row['energy_metric_resolutions'][-1]['same_amplitudes_phase_witness']['q_high_over_q_low']))
b.bar([str(s) for s in S],ratio,color='#476c94',width=.5);b.set_yscale('log');b.set(xlabel='Demi-support S des matrices V644 (8 dimensions)',ylabel='Rapport des deux énergies',title='Mêmes modules de coefficients et norme R ; seuls les signes changent')
for i,v in enumerate(ratio):b.text(i,v*1.22,f'{v:.3g}',ha='center',fontsize=9)
b.set_ylim(1,max(ratio)*6)
fig.text(.06,.025,'Haut : certificat du signal scalaire sur une fenêtre déjà étudiée. Bas : quadratures exploratoires, sans certificat d’erreur.',fontsize=8,color='#444')
fig.tight_layout(rect=(0,.045,1,1));out=ROOT/'1_Presentation/79_SIGNAL_RESOLUTION_VISUEL'
fig.savefig(out.with_suffix('.png'),dpi=170);fig.savefig(out.with_suffix('.svg'))
print('Figure écrite')
