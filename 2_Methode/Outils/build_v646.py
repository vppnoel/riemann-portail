"""The executable Lego, its proof report and the current dictionary supplement."""
from pathlib import Path
import sys,json,importlib.util,base64,html,csv
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'1_Presentation';D=ROOT/'3_Preuves_et_calculs/data'
STEM='71_LEGO_REUTILISABLE_ET_PREMIER_CERTIFICAT_COMPLET'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def module(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
def supplement():
    dictionary=read(D/'v645_dictionnaire.json');dictionary['version']='V6.46'
    rows=r'''
ports§3§Ports du Lego§(S,forme,η,norme,unité,moments)§Chaque pièce porte la forme de ses attaches.§Signature exacte ; les paramètres de forme et le support doivent coïncider.§Un label n’authentifie pas une preuve ; constructeurs et erreurs doivent être contrôlés.
annihilator_gram§4§Gram des annihilateurs§G_ij=⟨w_i,w_j⟩§Les balances ont une règle commune.§G strictement positif ; projection Π_W ; cosh/sinh séparent les deux parités.§Une base presque dépendante exige contrôle de conditionnement et inversion encadrée.
projection_loewner§4§Projection optimale des sources§C_opt=K−B*G⁻¹B§On retire ensemble les attaches inutiles.§Minimise le Gram entier en ordre de Loewner ; réutilise G pour la concentration Fourier.§Sources L² réelles et erreurs nécessaires ; exemple rationnel seul n’est pas source ζ certifiée.
parity_concentration§4§Concentration par parité§κ±(T)=π⁻¹∫₀ᵀd±(t)dt§Chaque tiroir possède sa propre règle.§Moments projetés et Fourier unitaire ; masse sous bande≤min(1,κ±)·masse.§La trace majore la norme et peut perdre de l’information ; aucun minimum spectral exact annoncé.
frequency_layers§4§Couches fréquentielles positives§λ±=ΣΔa_j(1−min(1,κ±_j))§Empiler plusieurs marches au lieu d’une seule.§Somme finie donnant une minoration sur toutes les fréquences, queue comprise.§Seuils croissants, incréments positifs et majorants κ orientés requis.
midpoint_lipschitz§4§Erreur de milieux contrôlée§erreur≤MTh/4π, M=4S²§La règle possède une épaisseur connue.§Dérivée des normes projetées bornée ; erreur ajoutée au majorant de concentration.§Une précision flottante ne remplace pas ce terme d’erreur d’intégration.
boundary_potential§4§Potentiel de bord§V_S(x)=J(S−x)+J(S+x)§Le bord de la boîte fait payer les déplacements.§E≥∫V_S|f|² ; J(d)=∫_d∞w ; principe valide sur tout le domaine de forme.§Les distances doivent être positives ; la singularité au bord se traite par intégrales positives.
edge_mass§4§Masse des bandes d’attache§M_bord=∫bandes|f|²§Les attaches premières vivent sur deux bandes.§Pour log2<2S<min(log3,2log2), Q_pr≤(log2/√2)M_bord.§Quand les bandes se recouvrent ou un autre premier entre, ce gabarit doit changer.
convex_blend§5§Mélange énergie et premier§c=(1−α)λ+αv₀−C₀§Deux règles paient la même attache.§α∈[0,1] et α(v₁−v₀)≥w₂ donnent Q≥c·masse.§v₀,v₁ sont des planchers certifiés ; c≤0 donne une réponse indéterminée.
whole_space_certificate§5§Certificat sur tout l’espace§Q_W≥(1/25)masse et≥(1/200)R§Toutes les pièces autorisées tiennent dans la boîte.§Tous f∈X_S,0<S≤347/1000 ; dimension infinie ; premier2 présent ; tête nulle.§Le support est borné ; aucune exhaustion jusqu’à l’infini ni preuve de RH.
zero_extension§4§Couverture par inclusion§X_S↪X_S₀ pour S≤S₀§La petite boîte entre dans la grande.§Extension zéro conserve support, moments, énergie et forme globale ; transport du certificat.§L’agrandissement au-delà de S₀ ajoute des directions non couvertes.
model_guard§4§Garde de forme perturbée§Q_η=Q_W−η·masse§Changer le poids change le modèle.§Le port porte le décalage exact ; seuls les deux gabarits définis sont autorisés.§Un résultat sur Q_η ne doit jamais être annoncé sur Q_W.
negative_control§4§Contrôle négatif du dispositif§Q_η(f)<0 pour témoin choisi§Vérifier que la construction détecte une pièce qui casse.§Témoin polynomial et majorant rationnel ; l’assembleur ne certifie pas la forme modifiée.§Aucun contre-exemple à RH ; le contrôle teste une perturbation déclarée.
finite_layer_assembly§5§Assembleur réutilisable§domaines+bornes+erreurs→statut§Les attaches doivent toutes s’accorder.§Briques cohérentes donnent certifié local, indéterminé ou contrat refusé.§Certification analytique et numérique, pas assistant de preuve formelle ni validation de payload arbitraire.
'''
    for line in rows.strip().splitlines():
        i,level,name,symbol,image,exact,guard=line.split('§')
        dictionary['entries'].append(dict(id='math:lego_'+i,level=int(level),kind='math',name=name,symbol=symbol,image=image,exact=exact,guard=guard,
            status='Lemmes K1–K7 et certificat borné V646 ; gardes explicites',source='Document 71 ; V646_LEGO_CERTIFICATS.md'))
    assert len({x['id'] for x in dictionary['entries']})==len(dictionary['entries'])
    (D/'v646_dictionnaire.json').write_text(json.dumps(dictionary,ensure_ascii=False,indent=2)+'\n')
    inventory=module('index646',ROOT/'2_Methode/Outils/build_v644_dictionary.py').code_inventory()
    (D/'v646_index_fonctions.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
    with (D/'v646_index_fonctions.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['path','line','name','kind','signature','docstring','explanation_status']);writer.writeheader();writer.writerows(inventory['entries'])
    print('Dictionnaire',len(dictionary['entries']),'fiches ; index',len(inventory['entries']),'déclarations')
def figure():
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
    fig,ax=plt.subplots(figsize=(10,6.8));ax.set_xlim(-1.15,6.15);ax.set_ylim(-5.1,1.0);ax.axis('off')
    nodes={'domain':(0,0,'Domaine et moments\nXₛ · unités et norme'), 'projection':(2,0,'Projection commune\nGram des annihilateurs'),
        'sources':(4,0,'Sources : C optimal\nAlgèbre prouvée ; sources à certifier'),
        'parity':(0,-2,'Parité\nDeux blocs sans couplage'), 'layers':(2,-2,'Couches fréquentielles\nλ ≥ 231/40'),
        'assembly':(4,-2,'Certificat complet local\nQ ≥ masse/25 et R/200'),
        'boundary':(0,-4,'Potentiel de bord\nCoût des déplacements'), 'prime':(2,-4,'Attaches du premier 2\nQpr ≤ w₂·Mbord'),
        'transport':(4,-4,'Agrandissement non borné\nLoi encore ouverte')}
    edges=[('domain','projection',False),('domain','parity',False),('projection','sources',False),('projection','layers',False),
        ('parity','layers',False),('layers','assembly',False),('boundary','prime',False),('boundary','assembly',False),
        ('prime','assembly',False),('sources','assembly',True),('assembly','transport',True)]
    nodes={key:(x*1.25,y,label) for key,(x,y,label) in nodes.items()}
    for a,b,dashed in edges:
        x,y,_=nodes[a];xx,yy,_=nodes[b]
        dx,dy=xx-x,yy-y;length=(dx*dx+dy*dy)**.5;ux,uy=dx/length,dy/length
        offset=min(1.0/abs(ux) if ux else 1e6,.52/abs(uy) if uy else 1e6)
        ax.add_patch(FancyArrowPatch((x+ux*offset,y+uy*offset),(xx-ux*offset,yy-uy*offset),arrowstyle='-|>',mutation_scale=13,lw=1.5,color='#64766b',linestyle='--' if dashed else '-',shrinkA=0,shrinkB=0,zorder=1))
    for key,(x,y,label) in nodes.items():
        color='#fff0d8' if key in ('sources','transport') else '#e0eee2'
        ax.add_patch(FancyBboxPatch((x-.92,y-.43),1.84,.86,boxstyle='round,pad=.05',facecolor=color,edgecolor='#668476',lw=1.1,zorder=2))
        ax.text(x,y,label,ha='center',va='center',fontsize=10.3,color='#203c30',zorder=3)
    ax.text(2.5,.77,'Des briques qui travaillent deux fois',ha='center',fontsize=16,weight='bold',color='#203c30')
    ax.text(2.5,-4.83,'Vert : preuve ou certificat local · Orange : construction à compléter\nPointillé : raccord conditionnel · Couverture acquise : 0 < S ≤ 347/1000',ha='center',fontsize=10,color='#465d50')
    fig.tight_layout();fig.savefig(P/'71_GRAPHE_LEGO.png',dpi=180);fig.savefig(P/'71_GRAPHE_LEGO.svg');plt.close(fig)
def report(result):
    table='| S | λ inférieur encadré | marge massique de l’assembleur | statut |\n|---|---|---|---|\n'
    for r in result['supports']:
        c=r['certificate'];margin=('{:.8f}'.format(float(F(c['mass_floor_lower']))) if c.get('mass_floor_lower') else 'poids convexe > 1')
        table+='| '+r['S']+' | {:.8f}'.format(float(F(r['layers']['lambda_lower'])))+' | '+margin+' | '+('certifié sur tous les tests' if c['status']=='certified_local_all_tests' else 'indéterminé')+' |\n'
    text=(ROOT/'3_Preuves_et_calculs/preuves/V646_LEGO_CERTIFICATS.md').read_text(encoding='utf-8-sig')
    diagnostic=read(D/'v646_fourier_joint_diagnostic.json')
    dt='| S | séparation géométrique | enveloppe monotone | sous-niveaux joints |\n|---|---|---|---|\n'
    for r in diagnostic['supports']:
        q=r['resolutions'][-1];dt+='| '+r['S']+' | '+ ' | '.join('{:.8f}'.format(q[k]) for k in ['separate_geometric_margin','monotone_envelope_margin','sublevel_joint_margin'])+' |\n'
    text=text.replace('{{DIAGNOSTIC_TABLE}}',dt)
    text=text.replace('{{RESULT_TABLE}}',table).replace('{{FIGURE}}','![Les raccords du Lego et leurs limites.](71_GRAPHE_LEGO.png)')
    refs=module('refs646',ROOT/'2_Methode/Sources/build_sources.py');base=text.split(refs.REF0)[0].rstrip()+'\n'
    text=base+'\n'+refs.doc_refs(base,refs.load())+'\n';(P/(STEM+'.md')).write_text(text,encoding='utf-8-sig')
    module('pdf646',ROOT/'2_Methode/Outils/build_v644.py').pdf(STEM)
def dashboard(result):
    bi=module('nav646ui',ROOT/'2_Methode/Indicateur/build_indicateur.py');payload=json.dumps(result,ensure_ascii=False).replace('</',r'<\/')
    pic='data:image/png;base64,'+base64.b64encode((P/'71_GRAPHE_LEGO.png').read_bytes()).decode()
    css='body{margin:0;background:#f2f5ef;color:#243b30;font:16px/1.6 system-ui}main{max-width:1160px;margin:auto;padding:22px}header{background:#163f34;color:white;padding:26px;border-radius:14px}header a{color:#e0f3df}h1{line-height:1.2}.topnav{display:flex;flex-wrap:wrap;gap:12px;margin:0 0 18px}a{color:#236d53}.panel{background:white;border:1px solid #c8d9cb;padding:20px;border-radius:12px;margin:18px 0}.guard{background:#fff1db;border-left:5px solid #b77e33;padding:14px}.formula{background:#e9f2e8;font-size:22px;padding:15px;overflow-wrap:anywhere}input,select,button{font:inherit;padding:9px;border:1px solid #9aad9d;border-radius:7px;max-width:100%}button{cursor:pointer;background:#e2efdf}.row{display:flex;gap:16px;flex-wrap:wrap}label{display:block}table{width:100%;border-collapse:collapse}th,td{padding:9px;text-align:left;border-bottom:1px solid #dce5db}img{width:100%;height:auto}.muted{font-size:14px;color:#586b5d}@media(max-width:650px){main{padding:10px}table{font-size:13px}td,th{padding:5px}}'
    body=f'''<header><h1>Le Lego réutilisable</h1><p>V6.46 · premier certificat complet, avec le premier 2 présent.</p><p><a href="{STEM}.pdf">Preuves K1–K7 et résultats · PDF</a> · <a href="{STEM}.tex">LaTeX</a> · <a href="69_LANGUE_DES_PASSAGES.html">Dictionnaire progressif</a></p></header>
<section class="panel"><h2>Ce qui tient maintenant</h2><div class="formula">Pour tous les tests admissibles et 0 &lt; S ≤ 347/1000 : Q_W ≥ masse/25 ; Q_W ≥ R/200 ; masse ≤ 3R/20.</div><p>La boîte contient une infinité de fonctions. La preuve couvre toute la boîte, pas seulement une liste de pièces testées. Le terme du premier 2 est présent au support maximal.</p><p class="guard">La famille de supports est bornée. Une loi d’agrandissement jusqu’à l’infini reste ouverte ; aucune preuve de RH n’est annoncée.</p></section>
<section class="panel"><h2>Une pièce qui sert deux fois</h2><p>La projection retire les attaches inutiles aux sources et contrôle aussi les fréquences. Le bord fait payer précisément les bandes où le premier 2 attache deux morceaux de fonction. L’assembleur garde cette relation au lieu de soustraire une norme première maximale indépendante.</p><img src="{pic}" alt="Graphe des briques, couplages et porte d’agrandissement ouverte"></section>
<section class="panel"><h2>Inspecter les trois essais</h2><label>Support S <select id="support">{''.join('<option value="'+r['S']+'">'+r['S']+'</option>' for r in result['supports'])}</select></label><div id="numbers" aria-live="polite"></div><p class="guard">Une marge inférieure non positive, ou un poids convexe trop grand, signifie que ce certificat ne tranche pas. Cela ne prouve pas que Q_W possède une direction négative.</p></section>
<section class="panel"><h2>Vérifier un raccord de domaine</h2><div class="row"><label>Support demandé <input id="requested" type="number" min="0" value="0.3" step="0.01"></label><label>Norme <select id="norm"><option value="R">R = masse + énergie</option><option value="H1">H¹</option></select></label><label>Unité de forme <select id="unit"><option value="A2">A_amp²</option><option value="A">A_amp</option></select></label></div><button id="connect">Raccorder au certificat</button><p id="connection" aria-live="polite"></p><button id="global">Étendre à tous les supports ?</button><p id="coverage" aria-live="polite"></p><p class="muted">Ce jeu lit les contrats déjà établis. Il ne certifie pas une brique arbitraire créée en changeant ses étiquettes.</p></section>
<section class="panel"><h2>Le contrôle des sources</h2><p>Exemple algébrique exact : K = [[5,2],[2,2]], B = [[2,1]], G = [[1]]. Retirer la projection donne C_opt = [[1,0],[0,1]]. Toute correction différente ajoute un Gram positif.</p><p class="guard">Cet exemple valide l’algèbre de la brique. Les sources L² réelles, les intégrations et les erreurs restent à certifier dans son application aux têtes de supports plus grands.</p></section>
<section class="panel"><h2>Contrôle négatif déclaré</h2><p>Une forme modifiée Q_η = Q_W − η·masse possède un témoin négatif rationnel. L’assembleur ne la certifie pas. Ce test empêche une validation aveugle ; il concerne un modèle modifié.</p><p id="negative"></p></section>
<footer><p><a href="../3_Preuves_et_calculs/data/v646_lego_resultats.json">Bornes binaires et marges rationnelles</a> · <a href="../3_Preuves_et_calculs/data/v646_protocole_lego.json">Protocole avant certification</a> · <a href="70_PONT_ARITHMETIQUE.html">Étape V6.45</a></p><p>Prochaine porte : estimation conjointe énergie/premiers pour des supports plus grands, puis règle de transport non bornée.</p></footer>'''
    js=r'''const D=JSON.parse(document.getElementById('lego-data').textContent),el=id=>document.getElementById(id);const q=x=>{if(x===null||x===undefined)return 'non disponible';const a=String(x).split('/');return Number(a[0])/(a.length===2?Number(a[1]):1);};
function render(){const r=D.supports.find(x=>x.S===el('support').value),c=r.certificate;el('numbers').innerHTML='<table><tr><th>Quantité</th><th>Valeur d’affichage</th></tr><tr><td>λ inférieur</td><td>'+q(r.layers.lambda_lower).toFixed(9)+'</td></tr><tr><td>Borne indépendante énergie − C₀ − norme première</td><td>'+(c.independent_floor_lower?q(c.independent_floor_lower).toFixed(9):'non affichée')+'</td></tr><tr><td>Poids convexe</td><td>'+(c.convex_weight?q(c.convex_weight).toFixed(9):'supérieur à 1')+'</td></tr><tr><td>Marge massique jointe</td><td>'+(c.mass_floor_lower?q(c.mass_floor_lower).toFixed(9):'condition non satisfaite')+'</td></tr><tr><td>Statut</td><td>'+(c.status==='certified_local_all_tests'?'Certifié : tous les tests du support et de ses sous-domaines.':'Indéterminé pour ce certificat.')+'</td></tr></table>';}
function connect(){const s=Number(el('requested').value);if(!Number.isFinite(s)||s<=0){el('connection').textContent='Raccord refusé : support strictement positif requis.';return;}if(el('norm').value!=='R'||el('unit').value!=='A2'){el('connection').textContent='Raccord refusé : norme et unité ne correspondent pas au contrat établi.';return;}el('connection').textContent=s<=347/1000?'Raccord valide par inclusion : mêmes moments et forme, Q_W ≥ masse/25 et R/200.':'Support hors de la couverture certifiée ; la positivité reste indéterminée ici.';}
function global(){el('coverage').textContent='Couverture acquise : 0 < S ≤ 347/1000. Couverture non bornée refusée : aucune loi atteignant S_n → infini n’est fournie.';}
el('support').addEventListener('change',render);el('connect').addEventListener('click',connect);el('global').addEventListener('click',global);render();connect();el('negative').textContent='η = '+D.perturbed_negative_control.eta+' ; témoin négatif certifié pour la forme modifiée : '+D.perturbed_negative_control.negative_witness_certified+'.';window.legoDashboard={render,connect,global};'''
    (P/'71_LEGO_REUTILISABLE.html').write_text('<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V6.46 · Lego de certificats</title><style>'+css+'</style></head><body><main>'+bi.topnav('graphe','../')+body+'</main><script id="lego-data" type="application/json">'+payload+'</script><script>'+js+'</script></body></html>')
def main():
    result=read(D/'v646_lego_resultats.json');supplement();figure();report(result);dashboard(result)
if __name__=='__main__':main()
