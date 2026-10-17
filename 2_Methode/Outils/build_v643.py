"""Build document 67 and a self-contained map/contract planner."""
from pathlib import Path
import json,subprocess,tempfile,shutil,importlib.util,html,argparse
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'1_Presentation';D=ROOT/'3_Preuves_et_calculs/data';STEM='67_CONSTRUIRE_DES_PONTS_AVEC_BELLMAN'


def graph():
    nodes=[
      dict(id='nb',label='Beurling et dilatations',status='demontre',row=0,col=0,detail='B1 : J est unitaire ; D devient le semi-groupe isométrique R. La densité NB reste équivalente à RH.'),
      dict(id='primes',label='Translations des premiers',status='demontre',row=0,col=2,detail='B1 : compression exacte K_X vers la demi-droite. L’identité ne fournit aucun signe ; la norme de K_X diverge sur tout L².'),
      dict(id='reg',label='Régularisation et décalage',status='demontre',row=1,col=0,detail='B4 : Γ_S et Pχ(ηδ*Γ_S). Erreur H¹ bornée par Cδ^-3 fois erreur L². Cutoffs variables nécessaires à la couverture.'),
      dict(id='form',label='Forme complète sur H¹',status='demontre',row=1,col=2,detail='B2 : métrique externe ; Q_W continue à S fixé ; représentant T_S autoadjoint signé. Aucune positivité supposée.'),
      dict(id='core',label='Cœur admissible dense',status='demontre',row=2,col=0,detail='B3 : correction des deux moments par φ et φ′. Union des images régularisées dense avec entrées L² arbitraires.'),
      dict(id='blocks',label='Compressions et masse',status='demontre',row=2,col=2,detail='B3 : G_S,n et métrique B_S,n. Erreur ε_n contrôlée dans H¹ ; les matrices positives finies seules ne suffisent pas.'),
      dict(id='schur',label='Bellman de la forme',status='demontre',row=3,col=2,detail='B5 : élimination exacte et dette a−c*G†c. G⪰0, couplage dans Ran G et dette non négative sont tous nécessaires.'),
      dict(id='invariant',label='Invariant arithmétique',status='ouvert',row=4,col=2,detail='À construire : expression et estimation de la dette pour la forme complète, conditions de noyau et portée sur toute une famille.'),
      dict(id='uniform',label='Pour tout n et support',status='ouvert',row=4,col=0,detail='Estimation G_S,n⪰−ε_n B_S,n pour tous n, ε_n→0, chaque S entier. Aucun indice fini ne remplit ce contrat.'),
      dict(id='rh',label='Positivité globale et RH',status='ouvert',row=5,col=1,detail='Le cœur, la continuité et l’estimation de toute la famille impliqueraient le signe global, puis RH par le critère de Weil. Estimation manquante.'),
      dict(id='local',label='Certificat local V642',status='local',row=3,col=0,detail='Une paire locale et un pli sont certifiés. Le compagnon n’a pas de métrique positive au double. Aucun transfert de signe à ζ.'),
    ]
    edges=[('nb','reg','transport'),('nb','primes','transport'),('reg','core','preuve'),('primes','form','definition'),('core','blocks','definition'),('form','blocks','definition'),('blocks','schur','preuve'),('schur','invariant','construction'),('invariant','uniform','condition'),('uniform','rh','condition'),('core','rh','condition'),('form','rh','condition'),('local','invariant','diagnostic')]
    return dict(nodes=nodes,edges=[dict(source=a,target=b,kind=k) for a,b,k in edges],
                and_gate=dict(target='rh',requires=['core','form','uniform']),scope='Typed implications; dotted links are obligations, not established theorems')


def static_figure(g):
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
    colors={'demontre':'#dceee5','ouvert':'#f8e8c9','local':'#dee7f2'}
    pos={n['id']:(n['col']*2.7,-n['row']*1.18) for n in g['nodes']}
    fig,ax=plt.subplots(figsize=(8,8.3))
    for e in g['edges']:
        a,b=pos[e['source']],pos[e['target']];dotted=e['kind'] in ('condition','construction','diagnostic')
        ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=12,linewidth=1.25,color='#9c6e32' if dotted else '#577369',linestyle='--' if dotted else '-',shrinkA=27,shrinkB=27,connectionstyle='arc3,rad=0.12' if abs(a[1]-b[1])>2 else 'arc3,rad=0'))
    for n in g['nodes']:
        x,y=pos[n['id']];ax.add_patch(FancyBboxPatch((x-1.2,y-.27),2.4,.54,boxstyle='round,pad=.03',facecolor=colors[n['status']],edgecolor='#54705f',linewidth=.8))
        ax.text(x,y,n['label'],ha='center',va='center',fontsize=8.5,color='#21352a')
    ax.text(2.7,.72,'Des transports démontrés vers une estimation de famille encore ouverte',ha='center',fontsize=11,weight='bold')
    ax.text(2.7,-6.68,'Plein : construction / implication acquise. Pointillé : obligation / diagnostic.\nPour RH, cœur ET continuité ET estimation de toute la famille.',ha='center',fontsize=8.5)
    ax.set_xlim(-1.55,6.95);ax.set_ylim(-7,.95);ax.axis('off');fig.tight_layout()
    fig.savefig(P/'67_PONTS_ET_OBLIGATIONS.png',dpi=190);fig.savefig(P/'67_PONTS_ET_OBLIGATIONS.svg');plt.close(fig)


def build_html(g):
    spec=importlib.util.spec_from_file_location('bi643',ROOT/'2_Methode/Indicateur/build_indicateur.py');bi=importlib.util.module_from_spec(spec);spec.loader.exec_module(bi)
    model=json.loads((D/'v643_modele_ponts.json').read_text());results=json.loads((D/'v643_bellman_ponts.json').read_text())
    payload=json.dumps(dict(graph=g,model=model,results=results),ensure_ascii=False).replace('</','<\\/')
    coords={n['id']:(60+260*n['col'],30+100*n['row']) for n in g['nodes']};svg=['<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#648373"/></marker></defs>']
    for e in g['edges']:
        x1,y1=coords[e['source']];x2,y2=coords[e['target']]
        dx=x2-x1;dy=y2-y1;t=min(105/abs(dx) if dx else 1000,22/abs(dy) if dy else 1000)
        sx=x1+105+t*dx;sy=y1+22+t*dy;tx=x2+105-t*dx;ty=y2+22-t*dy
        svg.append(f'<path d="M{sx},{sy} L{tx},{ty}" marker-end="url(#arrow)" class="edge {e["kind"]}" data-from="{e["source"]}" data-to="{e["target"]}"/>')
    for n in g['nodes']:
        x,y=coords[n['id']];svg.append(f'<g class="node {n["status"]}" data-node="{n["id"]}" role="button" tabindex="0" aria-label="{html.escape(n["label"])}"><rect x="{x}" y="{y}" width="210" height="44" rx="8"/><text x="{x+105}" y="{y+27}" text-anchor="middle">{html.escape(n["label"])}</text></g>')
    css='''body{margin:0;background:#f4f2e9;color:#24382e;font:16px/1.55 system-ui}main{max-width:1150px;margin:auto;padding:24px}nav{display:flex;gap:16px;flex-wrap:wrap;border-bottom:1px solid #bccabe;padding-bottom:12px}a{color:#276652}h1,h2{font-family:Georgia,serif}h1{font-size:38px;line-height:1.14}section{background:#fffdf7;border:1px solid #d9d9c9;border-radius:10px;padding:22px;margin:20px 0}.map{display:grid;grid-template-columns:minmax(0,3fr) minmax(220px,1fr);gap:20px}svg{width:100%;height:auto}.node{cursor:pointer}.node rect{stroke:#608272;fill:#dceee5}.node.ouvert rect{fill:#f8e8c9;stroke:#b08c43}.node.local rect{fill:#dee7f2}.node text{font:13px system-ui;fill:#24382e}.node.active rect{stroke:#102b23;stroke-width:3}.edge{stroke:#648373;stroke-width:1.6;fill:none}.edge.condition,.edge.construction,.edge.diagnostic{stroke:#aa833f;stroke-dasharray:5 5}.edge.selected{stroke-width:3}.muted{font-size:14px;color:#64736a}.controls{display:flex;flex-wrap:wrap;gap:16px}label{display:grid;gap:4px}select,button{font:inherit;padding:6px;border:1px solid #8ca294;border-radius:5px;background:white}table{border-collapse:collapse;width:100%;font-size:14px}th,td{padding:10px;border-bottom:1px solid #dcded3;text-align:left;vertical-align:top}#detail{border-left:3px solid #91b3a0;padding-left:16px}#plans{padding:14px;background:#eef4ec;margin-top:16px}.small{font-size:14px}@media(max-width:800px){.map{grid-template-columns:1fr}main{padding:12px}h1{font-size:30px}section{padding:15px}}'''
    body='''<header><p class="muted">Programme Riemann · V6.43 · Document 67</p><h1>Construire des ponts avec Bellman</h1><p>Un transport exact, un domaine contrôlé et une dette de couplage : les constructions intermédiaires donnent une question arithmétique précise à traiter.</p><p><a href="67_CONSTRUIRE_DES_PONTS_AVEC_BELLMAN.pdf">Dossier PDF</a> · <a href="67_CONSTRUIRE_DES_PONTS_AVEC_BELLMAN.tex">LaTeX</a> · <a href="../3_Preuves_et_calculs/preuves/V643_PONTS_MATHEMATIQUES.md">Preuves et limites</a></p></header>
<section><h2>Carte des constructions et des obligations</h2><p class="muted">Sélectionnez un pilier. Vert : démontré dans le dossier. Ocre : ouvert. Bleu : certificat local. Une arête pointillée conserve une obligation ; elle ne lui donne pas le statut de preuve.</p><div class="map"><svg viewBox="0 0 840 590" aria-label="Graphe de ponts mathématiques">SVG</svg><aside id="detail" aria-live="polite"></aside></div><p><strong>Jonction finale :</strong> cœur admissible ET continuité ET estimation pour tout indice et tout support. La dernière obligation reste ouverte.</p></section>
<section><h2>Deux rôles distincts de Bellman</h2><p><strong>Dans la forme :</strong> éliminer x dans q(x,y) laisse y*(C−B*A⁻¹B)y. La dette de Schur doit rester non négative ; un noyau impose aussi une condition de portée.</p><p><strong>Dans le pilote :</strong> choisir des constructions complémentaires, puis adapter la suite à leur issue. Les études achevées et leurs résultats sont distingués.</p></section>
<section><h2>Comparer les contrats de recherche</h2><p>Scénarios déclarés, durées conventionnelles, aucune probabilité de RH. Les valeurs portent sur des capacités de contrôle ou de compréhension ; elles ne mesurent pas une distance à la preuve.</p><div class="controls"><label>Budget restant H<select id="budget"><option>2</option><option>4</option><option>6</option><option selected>8</option><option>10</option></select></label><label>Construction<select id="structural"><option>1</option><option>2</option><option>3</option></select></label><label>Diagnostic local<select id="local"><option>1</option><option>2</option><option>3</option></select></label><label>Lecture et réfutation<select id="clarity"><option>1</option><option>2</option><option>3</option></select></label></div><div id="plans" aria-live="polite"></div><details><summary>Contrats, issues et durées</summary><div id="actions"></div></details><p class="muted">Enveloppe basse : issue défavorable déclarée et durée haute. Enveloppe haute : issue favorable et durée basse. L’intervalle décrit le modèle, pas une confiance statistique. Un budget trop court peut conduire à STOP ; le modèle n’en déduit pas une impasse mathématique.</p></section>
<section><h2>Ce qui a été réellement construit</h2><ul><li>B1 : unité de Mellin et transport des dilatations vers les translations.</li><li>B2–B3 : continuité dans H¹, opérateur signé, cœur et critère sur toute la famille.</li><li>B4 : lissage, décalage, couverture et budget d’erreur à paramètres fixés.</li><li>B5 : complément de Schur, condition de noyau et élimination dynamique.</li></ul><p>Le signe global, un invariant arithmétique de toute la famille et les limites uniformes restent ouverts.</p><p class="small">270 cas Python / graphe explicite / JavaScript sont concordants. L’exemple synthétique de complémentarité donne 12 contre 6 ; ces chiffres sont des préférences, pas des gains mesurés sur RH.</p></section>'''.replace('SVG',''.join(svg))
    script=(ROOT/'2_Methode/Outils/bridge_planning_client.js').read_text()+'''
const data=JSON.parse(document.getElementById('bridge-data').textContent);
function selectNode(id){const n=data.graph.nodes.find(n=>n.id===id);document.querySelectorAll('[data-node]').forEach(e=>e.classList.toggle('active',e.dataset.node===id));document.querySelectorAll('.edge').forEach(e=>e.classList.toggle('selected',e.dataset.from===id||e.dataset.to===id));const box=document.getElementById('detail');box.replaceChildren();const title=document.createElement('h3');title.textContent=n.label;const p=document.createElement('p');p.textContent=n.detail;const status=document.createElement('p');status.className='muted';status.textContent=n.status==='demontre'?'Lemme démontré ; limites dans le dossier':n.status==='local'?'Portée locale':'Obligation ouverte';box.append(title,status,p);}
document.querySelectorAll('[data-node]').forEach(e=>{e.addEventListener('click',()=>selectNode(e.dataset.node));e.addEventListener('keydown',v=>{if(v.key==='Enter'||v.key===' '){v.preventDefault();selectNode(e.dataset.node);}})});
function renderPlan(){const m=JSON.parse(JSON.stringify(data.model));const weights=['structural','local','clarity'].map(id=>Number(document.getElementById(id).value));for(const c of m.capabilities){const i=['contrat_structurel','noyau_resolu','pont_conditionnel','transfert_controle'].includes(c.id)?0:c.id==='local'?1:2;c.weight*=weights[i];}const b=Number(document.getElementById('budget').value);const lo=solveBridge(m,b,'lower'),hi=solveBridge(m,b,'upper');const labels=Object.fromEntries(m.actions.map(a=>[a.id,a.label]));labels.STOP='Arrêter à ce budget';const box=document.getElementById('plans');box.replaceChildren();for(const [label,r] of [['Basse',lo],['Haute',hi]]){const p=document.createElement('p');p.textContent=label+' : '+r.value+' U ; premiers choix équivalents : '+r.first_choices.map(k=>labels[k]).join(' ; ');box.append(p);} }
for(const id of ['budget','structural','local','clarity'])document.getElementById(id).addEventListener('change',renderPlan);
const aBox=document.getElementById('actions');for(const a of data.model.actions){const p=document.createElement('p');p.textContent=a.label+' · '+a.duration.join(' à ')+' H · issues : '+a.outcomes.map(o=>o.id.replaceAll('_',' ')).join(' / ');aBox.append(p);}selectNode('schur');renderPlan();
'''
    return '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V6.43 · Ponts et Bellman</title><style>'+css+'</style></head><body><main>'+bi.topnav('graphe','../')+body+'</main><script id="bridge-data" type="application/json">'+payload+'</script><script>'+script+'</script></body></html>'


def document():
    text=(ROOT/'3_Preuves_et_calculs/preuves/V643_PONTS_MATHEMATIQUES.md').read_text(encoding='utf-8-sig')
    text=text.replace('Vincent P. P. NOËL. 12 octobre 2026.', '**Document 67 · Vincent P. P. NOËL · 12 octobre 2026.**',1)
    text=text.replace('## 2. Pont B1', '\\newpage\n\n![Carte des constructions : les obligations ouvertes gardent leur statut.](67_PONTS_ET_OBLIGATIONS.png){width=90%}\n\n\\newpage\n\n## 2. Pont B1')
    for n in ('3. Pont B2','4. Pont B3','5. Pont B4','6. Pont B5','7. Un Bellman','8. Unités'):
        text=text.replace('## '+n,'\\newpage\n\n## '+n)
    text=text.replace('## Sources et portée de la lecture','\\newpage\n\n## Sources et portée de la lecture')
    r=json.loads((D/'v643_bellman_ponts.json').read_text())
    table='\n\n| Budget H | Valeur basse U | Premiers choix bas | Valeur haute U |\n|:--|:--|:--|:--|\n'
    labels={a['id']:a['label'] for a in json.loads((D/'v643_modele_ponts.json').read_text())['actions']};labels['STOP']='STOP'
    for row in r['results']:table+=f"| {row['budget']} | {row['lower']['value']} | {' ; '.join(labels[k] for k in row['lower']['first_choices'])} | {row['upper']['value']} |\n"
    text=text.replace('## 8. Unités',table+'\n\n## 8. Unités')
    (P/(STEM+'.md')).write_text(text,encoding='utf-8-sig')
    header=r'''\usepackage{etoolbox}
\usepackage{microtype}
\usepackage{float}
\floatplacement{figure}{H}
\setlength{\emergencystretch}{3em}
\AtBeginEnvironment{longtable}{\small}
'''
    with tempfile.TemporaryDirectory(prefix='v643_pdf_') as directory:
        tmp=Path(directory);(tmp/'header.tex').write_text(header)
        args=['pandoc',STEM+'.md','-s','-f','markdown+tex_math_single_backslash','--resource-path=.','--include-in-header='+str(tmp/'header.tex'),'-V','geometry:margin=19mm','-V','papersize=a4','-V','mainfont=DejaVu Sans','-V','monofont=DejaVu Sans Mono','-V','fontsize=10pt','-V','lang=fr-FR','-o',STEM+'.tex']
        p=subprocess.run(args,cwd=P,capture_output=True,text=True);logs=p.stdout+p.stderr
        if p.returncode:raise RuntimeError(logs)
        for _ in range(2):
            p=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(tmp),STEM+'.tex'],cwd=P,capture_output=True,text=True);logs+=p.stdout+p.stderr
            if p.returncode:(D/'v643_pdf_compile.log').write_text(logs);raise RuntimeError(logs[-3000:])
        shutil.copy2(tmp/(STEM+'.pdf'),P/(STEM+'.pdf'));(D/'v643_pdf_compile.log').write_text(logs)


def main():
    g=graph();(D/'v643_graphe_ponts.json').write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n')
    static_figure(g);(P/'67_GRAPHE_DES_PONTS.html').write_text(build_html(g));document()
    print('Document 67 : PDF, LaTeX, Markdown ; carte et pilote autonomes')
if __name__=='__main__':main()
