"""Certified root-box geometry, continuous contour bounds and typed research map."""
from pathlib import Path
from fractions import Fraction
import base64
import importlib.util
import json

ROOT=Path(__file__).resolve().parents[2];P=ROOT/'1_Presentation';D=ROOT/'3_Preuves_et_calculs/data'
def load(n):return json.loads((D/n).read_text(encoding='utf-8-sig'))

def graph_data():
    local='3_Preuves_et_calculs/preuves/V642_CERTIFICATION_LOCALE.md';global_='3_Preuves_et_calculs/preuves/V642_CONTRAT_ARITHMETIQUE.md'
    nodes=[
      ('pli','I1–I3 · Pli unique','demontre',0,0,'Deux inclusions strictes et contractions, 50/80 décimales ; existence et unicité dans la boîte rationnelle. Projection réelle fixe non nulle ; Hr et Htt séparés de zéro. Certificat calculatoire, backend iv précisé.',local),
      ('isolation','I4 · Deux zéros isolés','demontre',1,0,'Rouché sur 256 arcs continus, pour tout r du petit intervalle. Borne du défaut strictement inférieure à celle du polynôme de comparaison ; exactement deux zéros avec multiplicité.',local),
      ('racines','I5 · Quatre boîtes','demontre',2,0,'Contractions uniformes en r : deux boîtes critiques avant, deux boîtes hors droite après. Criticité exacte par unicité et symétrie fonctionnelle, et non par une partie réelle approximativement égale à 1/2.',local),
      ('paire','Paire et compagnon','demontre',1,1,'Le contour isolant rend les moments de la paire valides. Avant : mu>0 ; au double : mu=0 et bloc de Jordan ; après : mu<0. Les deux paramètres latéraux sont certifiés.',local),
      ('metrique','I6 · Métrique au pli impossible','ferme',0,2,'Toute métrique hermitienne positive symétrisant ce compagnon exige mu>0. Son conditionnement diverge quand mu approche zéro. Cela ferme cette construction locale automatique ; cela ne ferme pas RH.',local),
      ('a1','A1 · Forme depuis les premiers','demontre',2,2,'À support [-S,S], les puissances premières au-delà de exp(2S) ne contribuent pas. La queue archimédienne est explicite. Le signe de la forme complète demeure à démontrer.',global_),
      ('pont','Pont arithmétique manquant','ouvert',1,3,'Un certificat local V13 ne donne pas le signe de la forme de Weil pour zêta. Il manque une inégalité arithmétique sur tous les tests admissibles ou une borne de croissance indépendante de RH.',global_),
      ('a2','A2 · Norme première divergente','ferme',0,4,'Sur L² avant restriction aux tests admissibles, la norme de la somme positive de translations vaut exactement deux fois la somme de ses poids et diverge. Pas de norme uniforme de cette seule partie ; la compensation archimédienne reste à contrôler.',global_),
      ('uniforme','Inégalité sur chaque support','ouvert',2,4,'Pour chaque S et f=(d²/dx²−1/4)psi à support compact : Qarch(f) doit dominer la somme signée des corrélations aux logarithmes des puissances premières. Cette inégalité reste ouverte.',global_),
      ('croissance','Borne Q(X) depuis les premiers','ouvert',0,5,'L’autre porte du corpus exige Q(X)=X^{o(1)} indépendamment de RH. La positivité automatique Q(X)≥0 ne la fournit pas. Le théorème B suppose déjà RH.', '3_Preuves_et_calculs/preuves/V641_PASSAGE_AU_GLOBAL.md'),
      ('weil','Critère de Weil','conditionnel',2,5,'Le critère publié relie la positivité sur tous les tests admissibles à RH, dans la normalisation explicite. Un support ou une compression finie ne remplit pas le quantificateur global.',global_),
      ('rh','Destination précise · RH','ouvert',1,6,'Les zéros non triviaux de zêta ont tous partie réelle 1/2. Le certificat local et les voies fermées précisent la recherche ; aucune preuve globale n’est obtenue.',global_),
    ]
    edges=[('pli','paire','preuve','pli local'),('isolation','paire','preuve','moments valides'),('racines','paire','preuve','signature certifiée'),('paire','metrique','preuve','classification complète'),('paire','pont','ouvert','transfert absent'),('a1','uniforme','condition','signe à établir'),('pont','uniforme','ouvert','contrat de signe'),('pont','croissance','ouvert','contrat de croissance'),('a2','uniforme','obstruction','norme seule insuffisante'),('uniforme','weil','condition','tous S et tous tests'),('weil','rh','equivalence','critère publié'),('croissance','rh','condition','théorème A du corpus')]
    return {'version':'V6.42','title':'Graphe des certificats et du contrat global','nodes':[dict(id=i,label=l,status=s,x=x,y=y,detail=t,source=p) for i,l,s,x,y,t,p in nodes],'edges':[dict(source=s,target=t,kind=k,label=l) for s,t,k,l in edges],'author':'Vincent P. P. NOËL','date':'2026-10-12','edge_contract':'Les flèches ouvertes ne sont pas des implications. Les certificats locaux mentionnent leur backend et leur domaine.'}

def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle,FancyBboxPatch,FancyArrowPatch
    import numpy as np
    result=load('v642_certification.json');assert result['fold_certified'] and result['four_root_boxes_certified'] and result['contour']['accepted']
    fig,axes=plt.subplots(1,2,figsize=(9.5,3.8),sharex=True,sharey=True)
    for ax,h,title in zip(axes,(-1,1),('Avant le pli : deux zéros critiques','Après le pli : une paire hors droite')):
        for r in result['roots']:
            if Fraction(r['offset'])*h<=0:continue
            beta,t=map(lambda x:float(Fraction(x)),r['centre']);box=r['certificate']['box_intervals']
            a,b=[float(v['lower']) for v in box];width,height=[float(Fraction(v['upper'])-Fraction(v['lower'])) for v in box]
            ax.add_patch(Rectangle((a,b),width,height,facecolor='#23737d',edgecolor='#23737d'))
            ax.plot(beta,t,'+',color='#23737d',ms=10,mew=1.6)
        ax.axvline(.5,color='#9ba8a5',ls='--',lw=1);ax.set_title(title,fontsize=10);ax.set_xlabel('Re(s)');ax.grid(alpha=.2)
        ax.set_xlim(.481,.519);ax.set_ylim(4.843,4.879)
    axes[0].set_ylabel('Im(s)')
    fig.suptitle('Boîtes validées à r* ± 10⁻⁴ · largeur 2×10⁻⁸ invisible à cette échelle',fontsize=11)
    fig.tight_layout();fig.savefig(P/'66_Paire_certifiee.png',dpi=185);plt.close(fig)
    attempt=result['contour']['arc_attempts'][-1];q=float(Fraction(result['contour']['comparison_modulus_lower']))
    values=[float(Fraction(r['defect_upper']))/q for r in attempt['arcs']]
    fig,ax=plt.subplots(figsize=(9.4,3.1));x=np.arange(len(values)+1)*360/len(values)
    ax.step(x,values+[values[-1]],where='post',color='#23737d',lw=1.5);ax.axhline(1,color='#ab5846',lw=1.2,ls='--')
    ax.set_xlim(0,360);ax.set_ylim(0,1.12);ax.set_xticks([0,90,180,270,360]);ax.grid(alpha=.2)
    ax.set_xlabel('Arc du contour (degrés)');ax.set_ylabel('Majorant du défaut / minorant de |P|')
    ax.set_title('Chaque arc est couvert : maximum < 0,695 ; seuil de Rouché = 1',fontsize=11)
    fig.tight_layout();fig.savefig(P/'66_Controle_du_contour.png',dpi=180);plt.close(fig)
    graph=graph_data();(D/'v642_graphe_recherche.json').write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n')
    fills={'demontre':'#dfede6','ferme':'#f2e0d7','ouvert':'#f8eacb','conditionnel':'#e0e9f0'}
    fig,ax=plt.subplots(figsize=(10,11.3));ax.set_xlim(-.15,3.15);ax.set_ylim(7.25,-.45);ax.axis('off');by={n['id']:n for n in graph['nodes']}
    for edge in graph['edges']:
        a,b=by[edge['source']],by[edge['target']];start=(a['x']+.5,a['y']+.44);end=(b['x']+.5,b['y']-.13)
        style='--' if edge['kind'] in ('ouvert','condition') else '-';color='#b2782a' if edge['kind']=='ouvert' else '#a45845' if edge['kind']=='obstruction' else '#3b7260'
        if edge['source']=='pont' and edge['target']=='croissance':
            from matplotlib.path import Path as MplPath
            path=MplPath([start,(1.5,4.6),end],[MplPath.MOVETO,MplPath.LINETO,MplPath.LINETO])
            arrow=FancyArrowPatch(path=path,arrowstyle='-|>',mutation_scale=11,lw=1.15,color=color,linestyle=style)
        else:
            if a['y']==b['y']:start=(a['x']+1.005,a['y']+.15);end=(b['x']-.005,b['y']+.15)
            arrow=FancyArrowPatch(start,end,arrowstyle='<->' if edge['kind']=='equivalence' else '-|>',mutation_scale=11,lw=1.15,color=color,linestyle=style)
        ax.add_patch(arrow)
    labels={'pli':'I1–I3 · Pli unique\nBoîte et jets validés','isolation':'I4 · Deux zéros isolés\n256 arcs continus','racines':'I5 · Quatre boîtes\nAvant / après certifiés','paire':'Paire et compagnon\nSignature locale décidée','metrique':'I6 · Métrique au pli impossible\nNon dégénérée et positive','a1':'A1 · Forme depuis les premiers\nSomme finie à support fixé','pont':'Pont arithmétique manquant\nV13 → zêta reste ouvert','a2':'A2 · Norme première divergente\nSur L² avant restriction','uniforme':'Inégalité sur chaque support\nToutes les corrélations signées','croissance':'Borne Q(X) depuis les premiers\nThéorème A du corpus','weil':'Critère de Weil\nTous supports et tous tests','rh':'Destination précise · RH\nMécanisme global ouvert'}
    for n in graph['nodes']:
        ax.add_patch(FancyBboxPatch((n['x']+.025,n['y']-.08),.95,.47,boxstyle='round,pad=.02',facecolor=fills[n['status']],edgecolor='#a0b0ab',lw=.8))
        ax.text(n['x']+.5,n['y']+.15,labels[n['id']],ha='center',va='center',fontsize=10.5,color='#193b46',linespacing=1.5)
    ax.text(1.5,6.92,'Vert : preuve ou certificat dans le domaine indiqué · Terre : voie fermée sous hypothèses\nOcre : ouvert · Les flèches conditionnelles exigent leurs hypothèses',ha='center',fontsize=10,color='#3c545c',linespacing=1.8)
    fig.suptitle('V6.42 : une collision certifiée ; l’inégalité globale maintenant explicite',fontsize=13,y=.995)
    fig.tight_layout();fig.savefig(P/'66_Graphe_des_certificats.png',dpi=180);fig.savefig(P/'66_Graphe_des_certificats.svg');plt.close(fig)
    spec=importlib.util.spec_from_file_location('reader641',ROOT/'2_Methode/Outils/build_v641_graph.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    oldsvg=base64.b64encode((P/'65_Graphe_des_passages.svg').read_bytes()).decode();newsvg=base64.b64encode((P/'66_Graphe_des_certificats.svg').read_bytes()).decode()
    page=m.reader(graph).replace(oldsvg,newsvg).replace('V6.41','V6.42').replace('document 65','document 66').replace('65_FIBRES_PLIS_ET_POSITIVITE','66_UN_PLI_CERTIFIE_ET_SA_PAIRE')
    page=page.replace('Certifier par intervalles un pli attribué et un contour isolant la paire ; contrôler Zr, Ztt et le bord continu.','Déployer un candidat de jets sur sa fibre à A fixé ; la certification radiale choisie est achevée.')
    page=page.replace('Le graphe des passages','Le graphe des certificats').replace('Graphe des passages','Graphe des certificats')
    page=page.replace('Graphe : fibres, jets et paire locale ; deux portes globales vers RH, pont manquant et voies fermées','Graphe : pli et paire certifiés ; impossibilités locales précises ; contrats arithmétiques globaux ouverts')
    page=page.replace('Fixer la forme de Weil et son domaine, puis une estimation de la queue et du couplage, ou une borne Q(X)=X^{o(1)} depuis les premiers.','Contrôler la compensation archimédienne et les corrélations signées sur tous les tests admissibles ; l’inégalité globale est explicite.')
    (P/'66_GRAPHE_DES_CERTIFICATS.html').write_text(page)
    print('V642: three precise figures; typed graph and portable reader created')

if __name__=='__main__':main()
