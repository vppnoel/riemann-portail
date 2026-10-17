"""Figure du document 58, exclusivement depuis les données conservées."""
from pathlib import Path
import json,numpy as np,pandas as pd
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data'

def main():
    f=pd.read_csv(D/'v634_independant_v11.csv');f=f[~f.euler]
    sel=json.loads((D/'v634_selection_v11.json').read_text());C=np.array([r['coefficients'] for r in sel if not r['euler']])
    dist=np.arccos(np.clip(np.max(np.abs(C),axis=1),0,1))
    jets=json.loads((D/'v634_jets_certificats.json').read_text())
    fig,axes=plt.subplots(1,2,figsize=(11.3,4.2),layout='constrained')
    ax=axes[0];ok=~f.censure;sc=ax.scatter(f.a1[ok],f.premiere_detection[ok],c=dist[ok],s=32,cmap='viridis',edgecolors='white',linewidths=.4)
    ax.scatter(f.a1[~ok],np.full((~ok).sum(),150),marker='^',c='#b03b36',s=65,label='3 observations censurées à 150')
    ax.set(xlabel='Premier coefficient normalisé |a(1)|',ylabel='Première détection directe (hauteur entière)',title='V₁₁ : échantillon indépendant, 96 directions',ylim=(0,157))
    ax.legend(loc='upper left',fontsize=8);ax.grid(alpha=.16)
    fig.colorbar(sc,ax=ax,shrink=.73,label="Distance au point d'Euler (radians)")
    ax=axes[1];p=np.array([r['p'] for r in jets]);upper=np.array([r['borne_ecart'] for r in jets])/np.sqrt(p)
    actual=np.array([abs(r['points_courbe']-(r['p']+1)) for r in jets])/np.sqrt(p)
    ax.semilogx(p,upper,'o-',c='#225f91',label='Borne démontrée, paramètres optimisés')
    ax.semilogx(p,actual,'s--',c='#27845a',label='Écart exact pour y² = x³ + x + 1')
    ax.set(xlabel='Nombre premier p',ylabel='|N − (p + 1)| / √p',title='Jets : une erreur bornée en O(√p)',ylim=(0,5.5))
    ax.grid(alpha=.16);ax.legend(loc='center right',fontsize=8)
    fig.savefig(ROOT.parent/'1_Presentation/58_Validation_directe_et_jets.png',dpi=180)
    plt.close(fig)
if __name__=='__main__':main()
