"""Carte publique : familles couvrantes acquises, loi de signe encore ouverte."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / '1_Presentation'

def main():
    fig, ax = plt.subplots(figsize=(11.5, 7.2), dpi=170)
    fig.patch.set_facecolor('#f6f8fa')
    ax.set_facecolor('#f6f8fa')
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 7.2)
    ax.axis('off')
    ink = '#152f42'
    green, amber = '#e4f2ea', '#fff0d0'
    ax.text(0.35, 6.86, 'Vers RH : une loi de signe et une couverture globale',
            fontsize=18, weight='bold', color=ink, va='center')
    ax.text(0.35, 6.5, 'Traces antérieures et constructions nouvelles distinguées',
            fontsize=11.3, color='#516575')

    def box(x, y, w, h, title, sub, fill):
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.04,rounding_size=0.12',
                                   facecolor=fill,edgecolor='#91a7b7',linewidth=1.15))
        ax.text(x+w/2,y+h*.67,title,ha='center',va='center',fontsize=12.4,weight='bold',color=ink)
        ax.text(x+w/2,y+h*.28,sub,ha='center',va='center',fontsize=10.4,color=ink)

    def arrow(a,b,dashed=False):
        ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=15,
                                    color='#587389',linewidth=1.45,
                                    linestyle='--' if dashed else '-'))

    box(.5,4.97,4.85,.92,'Compensation signée [T]','Document 70 : Q = B₀ + fluctuation',green)
    box(6.13,4.97,4.85,.92,'Dette dans le dual [R]','Lemme acquis ; calcul restreint à construire',green)
    box(.5,3.4,4.85,.92,'Paquets traduits / Toeplitz [R]','Admissibilité + couverture démontrées',green)
    box(6.13,3.4,4.85,.92,'Deux filtres B₂ et B₃ [R]','Admissibilité + couverture dense démontrées',green)
    arrow((2.92,4.96),(2.92,4.37),True)
    arrow((8.55,4.96),(8.55,4.37),True)
    arrow((2.92,3.35),(4.68,2.68))
    arrow((8.55,3.35),(6.83,2.68))
    ax.text(5.75,3.88,'OU',ha='center',va='center',weight='bold',fontsize=11,color='#587389')
    box(2.45,1.61,6.6,1.03,'LOI UNIVERSELLE DE SIGNE : OUVERTE',
        'Forme complète, tous les couplages, tous les paramètres',amber)
    arrow((5.75,1.54),(5.75,1.01))
    ax.text(5.75,1.22,'si cette loi est démontrée',ha='center',fontsize=10,color='#795011',
            bbox={'facecolor':'#f6f8fa','edgecolor':'none','pad':2})
    box(4.2,.28,3.1,.63,'RH par Weil','Conclusion conditionnelle',amber)
    ax.text(.5,.02,'[T] trace avant interruption   [R] reconstruction actuelle   Vert : lemme auxiliaire, pas preuve de RH',
            fontsize=9.1,color='#516575',va='bottom')
    fig.savefig(P/'76_CARTE_PISTES_GLOBALES.png',bbox_inches='tight')
    fig.savefig(P/'76_CARTE_PISTES_GLOBALES.svg',bbox_inches='tight')
    plt.close(fig)

if __name__ == '__main__':
    main()
