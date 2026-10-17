"""A typed research graph, exact scientific figures and a portable local reader."""
from pathlib import Path
import base64
import html
import importlib.util
import json
import sys

ROOT=Path(__file__).resolve().parents[2]
D=ROOT/'3_Preuves_et_calculs/data'
P=ROOT/'1_Presentation'
sys.path.insert(0,str(ROOT/'3_Preuves_et_calculs/src'))

def load(name):return json.loads((D/name).read_text(encoding='utf-8-sig'))

def graph_data():
    geom='3_Preuves_et_calculs/preuves/V641_GEOMETRIE_ET_OPERATEURS.md'
    local='3_Preuves_et_calculs/preuves/V641_COLLISIONS_ET_LIMITES.md'
    glob='3_Preuves_et_calculs/preuves/V641_PASSAGE_AU_GLOBAL.md'
    # x,y are deliberate page positions, not a mathematical embedding.
    nodes=[
      ('image','La paire dans le labyrinthe','idee',1,0,'Changer l’objet suivi : une paire non ordonnée, son centre et son discriminant. L’image guide une construction ; elle ne prouve aucun signe.',local),
      ('fibre','T1 · Ellipse et fibre S²','demontre',0,1,'Pour toute cible complexe A prescrite, eta décide exactement : fibre vide, singleton ou sphère affine S². Hypothèses : rang M=2, ancre positive, 0<r<π/4.',geom),
      ('jet','L4 · Sections de jets','conditionnel',1,1,'C c=b et ||c||=1. Au rang cinq, nu<1 donne deux candidats, nu=1 un, nu>1 aucun. Le rang exact et Ztt≠0 sont à établir pour appliquer le résultat à une collision.',geom),
      ('pli','T2 · Pli critique double','conditionnel',2,1,'Z=Zt=0 et Zr Ztt≠0 donnent une paire locale. mu′(0)=−2 Zr/Ztt. C’est un théorème analytique sous hypothèses, distinct de leurs vérifications numériques.',local),
      ('variation','Voie universelle D fermée','ferme',0,2,'A=0 est réalisable à r=13/20 : D≡1 sur une fibre intérieure. Au bord, la fibre est un singleton. Cela réfute « D varie pour toute cible », sans réfuter une variation générique.',geom),
      ('paire','L5 · Moments et compagnon','conditionnel',1,2,'Contour isolant exactement deux zéros, sans pôle : a=m1/2, Δw=2m2−m1², mu=Δw/4, H=[[a,1],[mu,a]]. Aucune étiquette de branche n’est nécessaire.',local),
      ('mesure','20 plis candidats · 18 blocs','numerique',2,2,'Deux grilles, recoupements à 40/70 chiffres, six plis attribués, 18 blocs et 24 racines. Une perte sur la grille coarse est conservée. Pas de certification par intervalles ni d’exhaustivité.', '3_Preuves_et_calculs/data/v641_blocs_paires.json'),
      ('prefixes','G3 · Préfixes insuffisants','ferme',0,3,'K_M=I−2|e_(M+1)><e_(M+1)| : tous les préfixes jusqu’à M sont positifs, mais une direction négative reste cachée. Impossibilité pour les opérateurs arbitraires et les seules données finies.',glob),
      ('pont','Pont V13 → ζ manquant','ouvert',1,3,'Le compagnon local et sa métrique ne sont pas la forme arithmétique de Weil pour ζ. Il manque une identité arithmétique, un domaine et un contrôle uniforme. Aucune implication n’est actuellement démontrée.',glob),
      ('g1','G1–G2 · Tests et densité','demontre',0,4,'E=(∂²−1/4) Cc∞. Les espaces E_L,N sont denses dans la topologie des tests. La positivité de tous ces espaces passe au global si la forme est continue ; une liste finie ne suffit pas.',glob),
      ('g4','G4 · Queue et couplage','demontre',1,4,'Pour K borné autoadjoint et A≥aI>0 : K≥0 iff C−B* A⁻¹B≥0. Budget suffisant : C≥cI et ||B||²≤ac. Les estimations arithmétiques et les domaines requis restent à fournir.',glob),
      ('borne','Borne sur Q(X) à obtenir','ouvert',2,4,'Obtenir Q(X)=X^{o(1)} directement depuis les premiers. La positivité automatique Q(X)≥0 n’est pas une borne supérieure de croissance.', '1_Presentation/articles/article1_mean_square_double_poles.tex'),
      ('weil','Porte 1 · QW sur tout E','ouvert',0,5,'Critère publié : QW(f)≥0 pour chaque test admissible iff RH. QW est l’opposée de la somme locale dans la convention Fourier. La vérification primaire du critère ne fournit pas la positivité manquante.',glob),
      ('theoremeA','Porte 2 · Théorème A','demontre',2,5,'Théorème A du corpus : (1/2) limsup log(1+Q(X))/log X=Θ−1/2. Ainsi RH iff Q(X)=X^{o(1)}. Statut : démonstration du corpus et relecture interne, sans nouvelle expertise externe.', '1_Presentation/articles/article1_mean_square_double_poles.tex'),
      ('rh','Destination précise · RH','ouvert',1,6,'Tous les zéros non triviaux de ζ ont partie réelle 1/2. La destination logique est connue. Le mécanisme arithmétique qui y mène reste ouvert.',glob),
    ]
    edges=[
      ('image','fibre','analogie','image → contraintes'),
      ('image','pli','analogie','image → paire'),
      ('fibre','jet','condition','jets compatibles'),
      ('fibre','variation','preuve','contreexemple A=0'),
      ('jet','pli','condition','jet 2 et transversalité'),
      ('pli','paire','condition','contour isolant'),
      ('mesure','pli','observation','hypothèses recoupées'),
      ('paire','pont','ouvert','aucun transfert acquis'),
      ('pont','weil','ouvert','identité arithmétique ?'),
      ('pont','borne','ouvert','borne des premiers ?'),
      ('g1','weil','condition','toutes tailles + continuité'),
      ('g4','weil','condition','estimations + domaines'),
      ('prefixes','weil','obstruction','préfixes seuls : impossible'),
      ('borne','theoremeA','condition','borne à démontrer'),
      ('weil','rh','equivalence','critère de Weil'),
      ('theoremeA','rh','equivalence','avec Q=X^{o(1)}'),
    ]
    return {'version':'V6.41','title':'Graphe des passages vers RH','nodes':[dict(id=i,label=l,status=s,x=x,y=y,detail=t,source=p) for i,l,s,x,y,t,p in nodes],
      'edges':[dict(source=s,target=t,kind=k,label=l) for s,t,k,l in edges],
      'edge_contract':'Une flèche conditionnelle exige toutes les hypothèses de sa fiche ; une flèche ouverte n’est pas une implication.',
      'author':'Vincent P. P. NOËL','date':'2026-10-12'}

def scientific_figures(graph):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
    import numpy as np
    from v641_fibres import phase_values,fibre_geometry,ellipse_points
    z=phase_values(70)
    fig,axes=plt.subplots(1,3,figsize=(10.3,3.3),sharex=True,sharey=True)
    for ax,k in zip(axes,(1,3,5)):
        f=fibre_geometry(z,(k-1)//2,.65,0j)
        e=ellipse_points(z,(k-1)//2,.65)
        ax.fill(e.real,e.imag,color='#d8e9e4',alpha=.7)
        ax.plot(e.real,e.imag,color='#31746b',lw=1.6)
        ax.plot([0],[0],'o',color='#b45742',label='A=0 : D constant')
        centre=np.cos(.65)*z[(k-1)//2]
        ax.plot([centre.real],[centre.imag],'+',color='#244c79',ms=9,label='Centre de l’ellipse')
        ax.set_title(f'Ancre χ{k} · η(0)={f.eta:.4f}')
        ax.set_xlabel('Re(A)');ax.set_aspect('equal');ax.grid(alpha=.2)
    axes[0].set_ylabel('Im(A)');axes[1].legend(fontsize=7,loc='upper left')
    fig.suptitle('A prescrit : l’ellipse décide la faisabilité ; A=0 ferme la variation universelle',fontsize=11)
    fig.tight_layout();fig.savefig(P/'65_Ellipses_et_fibres.png',dpi=180);plt.close(fig)
    branches=load('v641_branches.json');collisions=load('v641_collisions.json')
    fig,axes=plt.subplots(2,2,figsize=(10.2,6.0),sharex=True)
    colors={'plus':'#247682','minus':'#b35b47'}
    for row in branches['rows']:
        if row['denominator']!=400:continue
        col=0 if row['character_k']==1 else 1
        points={p['radius']:(p['beta'],p['gamma']) for path in row['paths'] for p in path['points'] if p['kind']!='lost' and abs(p['beta']-.5)>.02}
        points=sorted(points.items());x=[r for r,_ in points]
        label=row['id'].replace('_rpi_6',' · π/6').replace('_r3_4',' · 3/4').replace('_r9_20',' · 9/20')
        for ax,coordinate in ((axes[0,col],0),(axes[1,col],1)):
            ax.plot(x,[abs(v[coordinate]-.5) if coordinate==0 else abs(v[coordinate]) for _,v in points],color=colors[row['side']],ls='--' if 'r3_4' in row['id'] or 'r9_20' in row['id'] else '-',label=label)
    byid={j['id']:j for j in collisions['jobs']}
    for foldid in sorted({a['fold_id'] for a in collisions['attributions']}):
        job=byid[foldid];p=job['precisions'][-1];col=0 if job['character_k']==1 else 1
        axes[0,col].plot(float(p['radius']),0,'o',ms=5,color=colors[job['side']])
        axes[1,col].plot(float(p['radius']),abs(float(p['height'])),'o',ms=5,color=colors[job['side']])
    for col,k in enumerate((1,5)):
        axes[0,col].set_title(f'Ancre χ{k} · branches suivies')
        axes[1,col].set_xlabel('Rayon r (A varie avec r)')
        for ax in axes[:,col]:ax.grid(alpha=.22);ax.set_xlim(.22,.76)
        axes[1,col].legend(fontsize=7,loc='best')
    axes[0,0].set_ylabel('|Re(s)−1/2|');axes[1,0].set_ylabel('|Im(s)|')
    fig.suptitle('Une enveloppe de détection peut changer de branche · aucune exhaustivité revendiquée',fontsize=11)
    fig.tight_layout();fig.savefig(P/'65_Branches_et_plis.png',dpi=170);plt.close(fig)
    blocks=load('v641_blocs_paires.json');foldids=sorted({r['fold_id'] for r in blocks['rows']})
    fig,axes=plt.subplots(2,3,figsize=(10.2,5.3))
    for ax,fid in zip(axes.ravel(),foldids):
        rows=sorted([r for r in blocks['rows'] if r['fold_id']==fid],key=lambda r:r['offset'])
        x=[r['offset']*1e4 for r in rows];y=[r['mu_real']*1e4 for r in rows]
        ax.axhline(0,color='#88999c',lw=.7);ax.plot(x,y,'o-',color='#237684',label='Moments de contour')
        ax.plot(x,[r['mu_linear']*1e4 for r in rows],'--',color='#b35b47',label='Jet κh')
        ax.set_title(fid.replace('fold_','').replace('_',' · '),fontsize=9)
        ax.set_xlabel('h × 10⁴');ax.grid(alpha=.2)
    axes[0,0].set_ylabel('μ × 10⁴');axes[1,0].set_ylabel('μ × 10⁴');axes[0,2].legend(fontsize=7)
    fig.suptitle('Discriminant en hauteur w : deux zéros critiques (μ>0), puis paire hors ligne (μ<0)',fontsize=11)
    fig.tight_layout();fig.savefig(P/'65_Discriminants_des_paires.png',dpi=170);plt.close(fig)
    fills={'idee':'#e9e8e2','demontre':'#e0efe8','conditionnel':'#e1e9f2','ferme':'#f3e1da','numerique':'#e0eef1','ouvert':'#fbecd1'}
    ink={'preuve':'#306b51','condition':'#365a7e','observation':'#207989','ouvert':'#b07625','equivalence':'#306b51','obstruction':'#a24d3e','analogie':'#858378'}
    fig,ax=plt.subplots(figsize=(10,12.0));ax.set_xlim(-.1,3.1);ax.set_ylim(7.3,-.45);ax.axis('off')
    index={n['id']:n for n in graph['nodes']}
    for edge in graph['edges']:
        s,t=index[edge['source']],index[edge['target']]
        if s['y']<t['y']:
            a=(s['x']+.5,s['y']+.44);b=(t['x']+.5,t['y']-.13)
        else:
            a=(s['x']+.5,s['y']-.13);b=(t['x']+.5,t['y']+.44)
        if s['y']==t['y']:a=(s['x']+.99,s['y']+.15);b=(t['x']+.005,t['y']+.15)
        style='--' if edge['kind'] in ('ouvert','condition') else ':' if edge['kind'] in ('analogie','observation') else '-'
        curve=.5 if edge['source']=='prefixes' else 0
        arrow=FancyArrowPatch(a,b,arrowstyle='<->' if edge['kind']=='equivalence' else '-|>',mutation_scale=11,lw=1.1,color=ink[edge['kind']],linestyle=style,connectionstyle=f'arc3,rad={curve}')
        ax.add_patch(arrow)
    labels={
      'image':'La paire dans le labyrinthe\nImage → symbole → opérateur','fibre':'T1 · Ellipse et fibre S²\nA prescrit et compatible','jet':'L4 · Sections de jets\n0, 1 ou 2 candidats au rang 5','pli':'T2 · Pli critique double\nZ=Zt=0 ; Zr Ztt≠0','variation':'Variation universelle fermée\nA=0 ⇒ D≡1','paire':'L5 · Moments et compagnon\nPaire sans étiquette','mesure':'20 candidats · 18 blocs\n24 racines recoupées','prefixes':'G3 · Préfixes insuffisants\nDirection négative cachée','pont':'Pont V13 → ζ manquant\nIdentité arithmétique ?','g1':'G1–G2 · Tests et densité\nToutes tailles + continuité','g4':'G4 · Queue et couplage\nBudget de Schur conditionnel','borne':'Borne sur Q(X) ouverte\nDepuis les nombres premiers','weil':'Porte 1 · Forme de Weil\nQW≥0 pour tout test','theoremeA':'Porte 2 · Théorème A\navec Q(X)=Xᵒ⁽¹⁾','rh':'Destination précise · RH\nMécanisme encore ouvert'}
    for n in graph['nodes']:
        ax.add_patch(FancyBboxPatch((n['x']+.03,n['y']-.08),.94,.47,boxstyle='round,pad=.02',facecolor=fills[n['status']],edgecolor='#98aaa8',lw=.8))
        ax.text(n['x']+.5,n['y']+.15,labels[n['id']],ha='center',va='center',fontsize=11.3,color='#183a46',linespacing=1.5)
    ax.text(1.5,6.93,'Traits pleins : preuve / équivalence sous l’énoncé indiqué\nTirets bleus : hypothèses · Tirets ocre : pont ouvert · Points : analogie / observation',ha='center',fontsize=9,color='#38505b',linespacing=1.8)
    fig.suptitle('Prendre de la hauteur : ce qui mène à quoi, et sous quelles conditions',fontsize=13,y=.995)
    fig.tight_layout();fig.savefig(P/'65_Graphe_des_passages.png',dpi=180);fig.savefig(P/'65_Graphe_des_passages.svg');plt.close(fig)

def reader(graph):
    spec=importlib.util.spec_from_file_location('v641_ind',ROOT/'2_Methode/Indicateur/build_indicateur.py');bi=importlib.util.module_from_spec(spec);spec.loader.exec_module(bi)
    encoded=base64.b64encode((P/'65_Graphe_des_passages.svg').read_bytes()).decode()
    payload=json.dumps(graph,ensure_ascii=False).replace('</','<\\/')
    css='''body{margin:0;background:#f3f2ed;color:#193b46;font:16px/1.55 system-ui,sans-serif}main{max-width:1180px;padding:24px;margin:auto}h1,h2{font-family:Georgia,serif;line-height:1.2}h1{font-size:38px}nav{display:flex;gap:14px;flex-wrap:wrap;border-bottom:1px solid #c8d6d2;padding-bottom:12px}a{color:#155b73}.lead{font-size:19px;max-width:850px}.grid{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(320px,1fr);gap:24px}.card{background:white;border:1px solid #d3deda;border-radius:9px;padding:20px;margin-bottom:18px}.map{width:100%;height:auto}.status{font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:.05em}.controls{display:flex;gap:12px;flex-wrap:wrap;margin:18px 0}label{display:grid;gap:4px}input,select,button{font:inherit;padding:8px;border:1px solid #9aaead;border-radius:5px}button{background:#fff;text-align:left;cursor:pointer;width:100%;margin:6px 0;border-left:5px solid #457b75}button[aria-pressed=true]{background:#e1eee9;outline:2px solid #386d64}.open{border-left-color:#b67b29}.closed{border-left-color:#a8553f}.note{color:#596b70;font-size:14px}.formula{font-family:serif;font-size:21px;white-space:pre-wrap}#detail{position:sticky;top:12px}footer{padding:22px 0;font-size:14px}@media(max-width:850px){.grid{grid-template-columns:1fr}#detail{position:static}main{padding:16px}h1{font-size:30px}}'''
    body='''<header><p>Programme Riemann · V6.41 · document 65</p><h1>Le graphe des passages</h1><p class="lead">La destination logique est connue : RH. La clef manquante est un mécanisme arithmétique qui impose le signe ou la croissance sur toute la classe requise.</p></header><div class="card"><p><b>Le changement utile :</b> suivre une paire de zéros, son centre et son discriminant. Aux collisions, les étiquettes peuvent permuter ; les moments de la paire restent définis si le contour demeure isolant.</p><p class="formula">a = m₁/2 · Δw = 2m₂ − m₁² · μ = Δw/4\nH = [[a, 1], [μ, a]]</p><p><a href="65_FIBRES_PLIS_ET_POSITIVITE.pdf">PDF : explications et démonstrations</a> · <a href="65_FIBRES_PLIS_ET_POSITIVITE.tex">LaTeX</a></p></div><div class="controls"><label>Rechercher<input id="query" type="search" placeholder="Ex. densité, A=0, compagnon"></label><label>Type de résultat<select id="filter"><option value="all">Tous les types</option><option value="demontre">Démontré</option><option value="conditionnel">Théorème sous hypothèses</option><option value="numerique">Numérique</option><option value="ouvert">Ouvert</option><option value="ferme">Voie fermée sous conditions</option><option value="idee">Idée</option></select></label></div><div class="grid"><section><div class="card"><img class="map" src="data:image/svg+xml;base64,ENCODED" alt="Graphe : fibres, jets et paire locale ; deux portes globales vers RH, pont manquant et voies fermées"><p class="note">Une flèche ouverte ne vaut pas implication. Les résultats locaux V13 ne constituent pas une preuve de RH pour ζ.</p></div><div id="nodes" class="card"></div></section><aside><div id="detail" class="card" aria-live="polite"></div><div class="card"><h2>Deux protocoles suivants</h2><p><b>Local :</b> certifier par intervalles un pli attribué et un contour isolant la paire ; contrôler Zr, Ztt et le bord continu.</p><p><b>Global :</b> fixer la forme de Weil et son domaine, puis une estimation de la queue et du couplage, ou une borne Q(X)=X^{o(1)} depuis les premiers.</p><p class="note">Bellman planifie des livrables contrôlables. Il ne choisit pas une preuve inconnue et n’attribue aucune probabilité de résoudre RH.</p></div></aside></div><footer>Vincent P. P. NOËL · preuves, hypothèses, mesures et obstacles restent séparés.</footer>'''.replace('ENCODED',encoded)
    js='''const g=JSON.parse(document.getElementById('graph-data').textContent),by=Object.fromEntries(g.nodes.map(n=>[n.id,n]));const status={idee:'Idée',demontre:'Démontré dans le cadre indiqué',conditionnel:'Théorème sous hypothèses',ferme:'Voie fermée sous conditions',numerique:'Recoupement numérique',ouvert:'Ouvert'};let selected='pont';function describe(id){selected=id;const n=by[id],box=document.getElementById('detail');box.replaceChildren();const tag=document.createElement('p');tag.className='status';tag.textContent=status[n.status];box.append(tag);const h=document.createElement('h2');h.textContent=n.label;box.append(h);const p=document.createElement('p');p.textContent=n.detail;box.append(p);const a=document.createElement('a');a.href='../'+n.source;a.textContent='Ouvrir la preuve ou les données';box.append(a);const eh=document.createElement('h3');eh.textContent='Relations dans le graphe';box.append(eh);g.edges.filter(e=>e.source===id||e.target===id).forEach(e=>{const p=document.createElement('p');p.textContent=by[e.source].label+' → '+by[e.target].label+' : '+e.label+' ['+e.kind+']';box.append(p)});document.querySelectorAll('#nodes button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.id===id)))}function render(){const q=document.getElementById('query').value.toLocaleLowerCase('fr'),f=document.getElementById('filter').value,box=document.getElementById('nodes');box.replaceChildren();const nodes=g.nodes.filter(n=>(f==='all'||n.status===f)&&JSON.stringify(n).toLocaleLowerCase('fr').includes(q));const p=document.createElement('p');p.textContent=nodes.length+' / '+g.nodes.length+' idées, résultats et obstacles';box.append(p);nodes.forEach(n=>{const b=document.createElement('button');b.type='button';b.dataset.id=n.id;b.textContent=n.label+' · '+status[n.status];b.className=n.status==='ouvert'?'open':n.status==='ferme'?'closed':'';b.setAttribute('aria-pressed',String(selected===n.id));b.addEventListener('click',()=>describe(n.id));box.append(b)})}document.getElementById('query').addEventListener('input',render);document.getElementById('filter').addEventListener('change',render);render();describe(selected);'''
    return '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V6.41 · Graphe des passages</title><style>'+css+'</style></head><body><main>'+bi.topnav('graphe','../')+body+'</main><script id="graph-data" type="application/json">'+payload+'</script><script>'+js+'</script></body></html>'

def main():
    graph=graph_data();(D/'v641_graphe_recherche.json').write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n')
    scientific_figures(graph)
    (P/'65_GRAPHE_DES_PASSAGES.html').write_text(reader(graph))
    print('V641 graph: 15 typed nodes, 16 typed edges; four scientific figures; portable HTML')

if __name__=='__main__':main()
