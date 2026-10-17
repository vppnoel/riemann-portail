"""Exact status map; arrows indicate obligations, not measured progress."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'1_Presentation'


def build(certified=False):
    fig,ax=plt.subplots(figsize=(10,7.3))
    fig.patch.set_facecolor('#f6f8fa');ax.set_facecolor('#f6f8fa')
    ax.set_xlim(0,10);ax.set_ylim(-.3,7);ax.axis('off')
    colors={'proved':('#e9f5ef','#227756'),'partial':('#fff3db','#99630d'),'open':('#f9e9eb','#963e4d')}
    def box(x,y,w,h,text,status):
        bg,fg=colors[status]
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.06,rounding_size=.12',
                                  linewidth=1.5,edgecolor=fg,facecolor=bg,zorder=3))
        ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=12.5,color='#172b3c',linespacing=1.4,zorder=4)
    def arrow(start,end,label=None,dashed=False):
        ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=15,
                                    color='#556b7f',linewidth=1.5,linestyle='--' if dashed else '-',zorder=1))
        if label:
            x=(start[0]+end[0])/2;y=(start[1]+end[1])/2
            ax.text(x,y,label,ha='center',va='center',fontsize=10,color='#556b7f',
                    bbox={'facecolor':'#f6f8fa','edgecolor':'none','pad':3},zorder=2)
    ax.text(.35,6.65,'VERS RH : CE QUI PORTE LA PREUVE',fontsize=16,fontweight='bold',color='#172b3c')
    ax.text(.35,6.2,'V6.50 · reconstruction après V6.49 · aucun signe global établi',fontsize=11,color='#556b7f')
    box(.4,4.6,4.1,1.1,'Transport exact Tᵣ\nSupport + moments + cœur dense','proved')
    box(5.5,4.6,4.1,1.1,'Certificat conservé V6.49\nTous les tests admissibles ; S ≤ 1/2','proved')
    box(.4,2.75,4.1,1.05,'Même espace de départ\nFamille de formes Qᵣ','proved')
    if certified:
        box(5.5,2.75,4.1,1.05,'Nouveau certificat V6.50\nTous les tests ; S ≤ 11/20\nModèle arithmétique déclaré','proved')
    else:
        box(5.5,2.75,4.1,1.05,'Essai S = 0,55\nBudgets et matrice\nValidation partielle','partial')
    arrow((2.45,4.54),(2.45,3.87),'identité exacte')
    arrow((7.55,4.54),(7.55,3.87),'nouveau raccord certifié' if certified else 'raccord à certifier',not certified)
    box(2.25,1,5.5,1.05,'OBLIGATION GLOBALE\nQᵣ(f) ≥ 0 pour chaque r et chaque test','open')
    arrow((2.45,2.69),(3.9,2.13),'loi de signe à établir',True)
    arrow((7.55,2.69),(6.1,2.13),'couverture à démontrer',True)
    box(3.6,-.05,2.8,.6,'RH · critère de Weil','open')
    arrow((5,.94),(5,.62),'équivalence')
    fig.text(.08,.027,'Vert : lemme ou certificat du dossier. Ambre : calcul partiel. Rouge : question ouverte.',fontsize=10,color='#556b7f')
    fig.text(.08,.009,'Les flèches pointillées sont des obligations ; elles ne constituent pas des implications déjà prouvées.',fontsize=9,color='#556b7f')
    fig.savefig(P/'75_CARTE_RH.png',dpi=175,bbox_inches='tight')
    fig.savefig(P/'75_CARTE_RH.svg',bbox_inches='tight')
    plt.close(fig)


if __name__=='__main__':build()
