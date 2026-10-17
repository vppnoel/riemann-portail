"""Create the V644 proof report, progressive dictionary and standalone grammar."""
from pathlib import Path
import json,sys,subprocess,tempfile,shutil,importlib.util,html,base64
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'1_Presentation';D=ROOT/'3_Preuves_et_calculs/data'
S68='68_ARITHMETIQUE_DES_PASSAGES_ET_QUEUE_EFFECTIVE';S69='69_DICTIONNAIRE_PROGRESSIF_DES_DOMAINES'
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def pdf(stem):
    header=r'''\usepackage{etoolbox}
\usepackage{microtype}
\usepackage{float}
\floatplacement{figure}{H}
\sloppy
\setlength{\emergencystretch}{5em}
\AtBeginEnvironment{longtable}{\small}
'''
    with tempfile.TemporaryDirectory(prefix='v644_pdf_') as dr:
        t=Path(dr);(t/'head.tex').write_text(header)
        args=['pandoc',stem+'.md','-s','-f','markdown+tex_math_single_backslash','--resource-path=.','--include-in-header='+str(t/'head.tex'),'-V','geometry:margin=19mm','-V','papersize=a4','-V','mainfont=DejaVu Sans','-V','monofont=DejaVu Sans Mono','-V','fontsize=9pt' if stem==S69 else 'fontsize=10pt','-V','lang=fr-FR','--toc','--toc-depth='+('1' if stem==S69 else '2'),'-o',stem+'.tex']
        p=subprocess.run(args,cwd=P,capture_output=True,text=True);log=p.stdout+p.stderr
        if p.returncode:raise RuntimeError(log)
        for _ in range(3):
            p=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(t),stem+'.tex'],cwd=P,capture_output=True,text=True);log+=p.stdout+p.stderr
            if p.returncode:(D/(stem+'_compile.log')).write_text(log);raise RuntimeError(log[-2500:])
        shutil.copy2(t/(stem+'.pdf'),P/(stem+'.pdf'));(D/(stem+'_compile.log')).write_text(log)
def report():
    results=read(D/'v644_family_resultats.json');tails=read(D/'v644_contrats_queue_entiers.json')
    num='| S | n | minimum généralisé dans H¹ | dette finale normalisée |\n|---|---|---|---|\n'
    for r in results['supports']:
      for e in r['precisions'][-1]['prefixes']:
        num+=f"| {r['S']} | {e['n']} | {float(e['lambda_min']):.8e} | {float(e['normalized_last_schur_debt']):.8e} |\n"
    tail='| S | M | T symbolique | chiffres de q | marge de queue ≥ |\n|---|---|---|---|---|\n'
    for r in tails['contracts']:tail+=f"| {r['S']} | {r['prime_power_count']} | {r['T_expression']} | {r['q_decimal_digits']} | {r['coercivity_lower']} |\n"
    text=(ROOT/'3_Preuves_et_calculs/preuves/V644_LANGUE_ET_DOMAINES.md').read_text(encoding='utf-8-sig')
    text=text.replace('{{NUMERIC_TABLE}}',num).replace('{{TAIL_TABLE}}',tail)
    text=text.replace('# 3. L1', '![Les traductions et leurs obligations.](68_GRAPHE_LANGUE.png)\n\n# 3. L1')
    (P/(S68+'.md')).write_text(text,encoding='utf-8-sig');pdf(S68)
def dictionary():
    data=read(D/'v644_dictionnaire.json');code=read(D/'v644_index_fonctions.json');core=[r for r in data['entries'] if r['kind']=='math'];met=[r for r in data['entries'] if r['kind']=='metaphor']
    count=sum(r['kind']=='function' for r in code['entries']);classes=sum(r['kind']=='class' for r in code['entries'])
    text='''---
title: "Dictionnaire progressif des domaines"
subtitle: "La langue des passages - V6.44 - Document 69"
author: "Vincent P. P. NOËL - dossier de recherche, rédaction assistée"
date: "12 octobre 2026"
---

# Comment apprendre cette langue

Une fiche commence par une image simple, puis donne un symbole, son domaine et
la condition qui rend le geste autorisé. Le nom imagé aide à comprendre ; la
définition et la garde portent le calcul. Les mots usuels restent canoniques.

La langue des passages relie le **moule** P, la **valise** U, la **portée** Fourier
ou Mellin, le **puzzle** de changement de base et la **balance** de Schur.
Son arithmétique distingue addition, produit ordinaire et convolution. Sa logique
écrit ce qui est conservé, ce qui se perd et le budget du passage. Les preuves
L1–L8 et les domaines exacts sont dans le document 68.

Une phrase possède quatre étiquettes : support S, ordre de jets r aux ±1/2,
ordre q en 0, et unité d’amplitude A^u. Le geste P gagne r ; la dérivée gagne q ;
la convolution additionne les ordres. Le produit ordinaire peut perdre les moments.
Les jets de test aux ±1/2, les jets de test en 0 et les jets des zéros critiques
sont trois entrées différentes de la langue.

Le noyau ci-dessous explique les objets de l’expérience actuelle et les principaux
objets du corpus. Tous les 95 noms du registre canonique sont repris avec leur
ancrage et leur garde. L’index technique séparé donne toutes les déclarations
Python analysées : une fonction de programme n’est pas automatiquement un
opérateur mathématique. Cette édition ne prétend pas avoir désambiguïsé chaque
symbole de toutes les archives historiques.

Une fiche marquée définition n’est pas une preuve nouvelle ; un statut du registre
est hérité, sans validation additionnelle. Les calculs V644 sont exploratoires,
sauf l’algèbre rationnelle et le contrat analytique entier de queue explicités.

'''
    text+=f"Cette édition contient **{len(core)} fiches du noyau**, **{len(met)} métaphores nommées** et un index de **{count} fonctions**, **{classes} classes**, dans **{code['file_count']} fichiers avec déclarations**, avec {len(code['parse_errors'])} erreur de parseur.\n\n"
    levels={1:'Les petits mots et les unités',2:'Les fonctions et leurs miroirs',3:'Les pièces où vivent les fonctions',4:'Les formes, opérations et invariants',5:'Les contrats de recherche et leurs limites'}
    def sanitize(s):
        # Protect plain mathematical underscores and Markdown punctuation in formulas.
        return s.replace('\\(','$').replace('\\)','$').replace('§','').replace('−','-').replace('–','-').replace('—','-')
    def plain(s):
        s=sanitize(s)
        for c in '_*^':s=s.replace(c,'\\'+c)
        return s
    for level,title in levels.items():
        text+='\n# Niveau '+str(level)+' - '+title+'\n\n'
        for r in core:
            if r['level']!=level:continue
            text+='## '+r['name']+'\n\n'
            text+='**Comme un premier jeu.** '+plain(r['image'])+'\n\n'
            formula=sanitize(r['symbol'])
            for c in '_*^':formula=formula.replace(c,'\\'+c)
            text+='**Symbole.** '+formula+'\n\n'
            text+='**Sens et domaine.** '+plain(r['exact'])+'\n\n'
            text+='**Garde.** '+plain(r['guard'])+'\n\n'
            text+='**Ancrage.** '+sanitize(r['source']).replace('_','\\_')+' ; '+sanitize(r['status'])+'.\n\n'
    text+='\n# Annexe - Tous les noms du registre canonique\n\nLes 95 entrées suivantes conservent les dernières lignes nommées du registre 20. Les images historiques peuvent rester plus techniques que celles du noyau. Leur absence éventuelle de statut explicite est signalée.\n\n'
    for r in met:
        text+='## '+r['name']+'\n\n'
        text+='**Image héritée.** '+sanitize(r['image'])+'\n\n**Ancrage exact.** '+sanitize(r['exact'])+'\n\n**Garde héritée.** '+sanitize(r['guard'])+'\n\n'
        if r['authorized']:text+='**Correspondance autorisée.** '+sanitize(r['authorized'])+'\n\n'
        text+='**Provenance.** '+sanitize(r['source']).replace('_','\\_')+'. **Statut :** '+sanitize(r['status'])+'.\n\n'
    text+='''
# Index technique et version interactive

Le lecteur interactif `69_LANGUE_DES_PASSAGES.html` permet recherche par nom,
symbole, image ou garde, filtres de niveau et consultation d’une fiche à la fois.
L’atelier applique les règles typées et signale les moments perdus.

L’index `v644_index_fonctions.csv` / `.json`, dans le dossier de données, donne
fichier, ligne, nom qualifié, signature, type et docstring. Sans docstring,
le comportement n’est pas inventé. La couverture technique est celle de l’AST,
non une analyse sémantique certifiée de tous les programmes.

Le dictionnaire JSON permet d’ajouter des entrées qualifiées en conservant leur
provenance. Les symboles G, P, D, U, R, gamma et kappa demandent leur contexte :
le même caractère écrit ne suffit pas à définir le même objet.

Les unités fictives accompagnent les calculs : x logarithmique sans dimension,
f d’amplitude A, Q et métriques d’unité A², quotient spectral sans dimension.
Le mot énergie, chaleur ou entropie ne fournit pas une preuve de signe.

Les preuves complètes et les expériences figurent dans le document 68 ; les
critères globaux, branches, collisions et coefficients des anciennes familles
gardent leurs obligations ouvertes. Cette langue crée des phrases vérifiables
et des ponts de domaines ; elle ne fournit pas encore la loi arithmétique globale.
'''
    (P/(S69+'.md')).write_text(text,encoding='utf-8-sig');pdf(S69)
def figure():
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
    nodes={'seed':(0,0,'Graines / algèbre Cc∞','proved'),'test':(0,-1.25,'P et jets admissibles','proved'),'h1':(-2,-2.65,'Métrique H¹\nRiesz compact','proved'),'r':(2,-2.65,'Métrique logarithmique R\nI - compact','proved'),'nogap':(-2,-4,'Marge H¹ stricte\nimpossible','closed'),'tail':(2,-4,'Queue de moments\nborne effective','proved'),'schur':(0,-5.35,'Schur fini avec couplages\nsigne à établir','open'),'rh':(0,-6.7,'Tous supports + signe\ncritère global RH','open')}
    edges=[('seed','test',False),('test','h1',False),('test','r',False),('h1','nogap',False),('r','tail',False),('tail','schur',False),('test','schur',True),('schur','rh',True)]
    fig,ax=plt.subplots(figsize=(8,8));colors={'proved':'#d9eee3','closed':'#f5d9d7','open':'#fff0ca'}
    for a,b,dash in edges:
        x,y,_l,_s=nodes[a];xx,yy,_l,_s=nodes[b];ax.add_patch(FancyArrowPatch((x,y),(xx,yy),arrowstyle='-|>',mutation_scale=13,shrinkA=28,shrinkB=28,color='#40584d',linestyle='--' if dash else '-'))
    for x,y,label,st in nodes.values():
        ax.add_patch(FancyBboxPatch((x-1.5,y-.37),3,.74,boxstyle='round,pad=.035',facecolor=colors[st],edgecolor='#537163'));ax.text(x,y,label,ha='center',va='center',fontsize=9)
    ax.text(0,.8,'Une langue de passages, une réduction réelle',ha='center',weight='bold',fontsize=14)
    ax.text(0,-7.55,'Vert : construction démontrée. Rouge : route précisément fermée.\nJaune : obligation ouverte. Pointillé : prémisse de signe manquante.',ha='center',fontsize=9)
    ax.set_xlim(-3.85,3.85);ax.set_ylim(-8,1.1);ax.axis('off');fig.tight_layout();fig.savefig(P/'68_GRAPHE_LANGUE.png',dpi=180);fig.savefig(P/'68_GRAPHE_LANGUE.svg');plt.close(fig)
def interactive():
    pedagogy=ROOT/'2_Methode/Outils/build_v648_pedagogy.py'
    if pedagogy.exists() and (D/'v648_dictionnaire.json').exists():
        module('pedagogy648current',pedagogy).build();return
    pedagogy=ROOT/'2_Methode/Outils/build_v647_pedagogy.py'
    if pedagogy.exists() and (D/'v647_dictionnaire.json').exists():
        module('pedagogy647current',pedagogy).build();return
    pedagogy=ROOT/'2_Methode/Outils/build_v646_pedagogy.py'
    if pedagogy.exists() and (D/'v646_dictionnaire.json').exists():
        module('pedagogy646current',pedagogy).build();return
    grammar=module('grammar644',ROOT/'3_Preuves_et_calculs/src/domain_grammar.py')
    edition='v646' if (D/'v646_dictionnaire.json').exists() else ('v645' if (D/'v645_dictionnaire.json').exists() else 'v644')
    version=read(D/(edition+'_dictionnaire.json'))['version']
    payload=dict(dictionary=read(D/(edition+'_dictionnaire.json')),rules=grammar.RULES,examples=grammar.examples(),code=read(D/(edition+'_index_fonctions.json')),tails=read(D/'v644_contrats_queue_entiers.json'))
    if not (D/'v644_grammaire.json').exists():
        (D/'v644_grammaire.json').write_text(json.dumps(dict(version='V6.44',semantic_domain='Cc∞, A(S;r,q;u)',rules=grammar.RULES,examples=grammar.examples()),ensure_ascii=False,indent=2)+'\n')
    bi=module('bi644',ROOT/'2_Methode/Indicateur/build_indicateur.py')
    css='''body{margin:0;background:#f3f5ef;color:#20372b;font:16px/1.55 system-ui,sans-serif}main{max-width:1240px;margin:auto;padding:25px}header{background:#183f34;color:white;padding:28px;border-radius:15px}h1{font-size:30px;line-height:1.15}h2{font-size:22px}a{color:#236356}header a{color:#d2f0dd}.bar,.panel{background:white;border:1px solid #cfdbce;border-radius:12px;padding:18px;margin:18px 0}.row{display:flex;gap:12px;flex-wrap:wrap}.layout{display:grid;grid-template-columns:330px 1fr;gap:18px}input,select,button{font:inherit;padding:8px;border:1px solid #9aad9f;border-radius:7px;max-width:100%;box-sizing:border-box}button{cursor:pointer;background:#eef5eb;color:#20372b}button:hover,button.active{background:#d2e9d9}#list{height:650px;overflow:auto}#list button{display:block;width:100%;text-align:left;margin:5px 0}.badge{display:inline-block;background:#e3eee1;border-radius:8px;padding:3px 8px;margin:2px;font-size:13px}.guard{border-left:5px solid #b87730;background:#fff5df;padding:12px}.muted{color:#58685f;font-size:14px}.formula{font-size:21px;overflow-wrap:anywhere;padding:12px;background:#f2f7ef}.zones{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}label{display:block}#result{white-space:pre-wrap;font-size:17px;padding:15px;background:#f1f6ef;border-radius:8px}table{width:100%;border-collapse:collapse}td,th{padding:8px;border-bottom:1px solid #ddd;text-align:left}img{max-width:100%}.topnav{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:16px}.topnav a{padding:5px;text-decoration:none}@media(max-width:800px){.layout,.zones{grid-template-columns:1fr}#list{height:300px}main{padding:12px}}'''
    body=f'''<header><span class="badge">{version} · calcul typé</span><h1>La langue des passages</h1><p>Un mot, une boîte, une relation conservée. Apprendre les gestes, construire des phrases, voir leurs pertes.</p><p><a href="{S68}.pdf">Preuves et expériences · PDF</a> · <a href="{S69}.pdf">Dictionnaire · PDF (édition V6.44)</a> · <a href="{S68}.tex">Article · LaTeX</a></p></header>
<section class="bar"><label for="search">Chercher un nom, symbole, image ou garde</label><input id="search" placeholder="moule, P, convolution, Bellman…" style="width:100%"><div class="row"><label>Niveau <select id="level"><option value="all">Tous les niveaux</option>{''.join(f'<option value="{i}">Niveau {i}</option>' for i in range(1,6))}</select></label><label>Tiroir <select id="kind"><option value="all">Tout le dictionnaire</option><option value="math">Objets mathématiques</option><option value="metaphor">95 métaphores historiques</option></select></label></div><p id="count" aria-live="polite"></p></section>
<section class="layout"><div id="list" class="panel" aria-label="Entrées du dictionnaire"></div><article id="entry" class="panel" aria-live="polite"></article></section>
<section class="panel"><h2>Jouer avec l’arithmétique des domaines</h2><p>On raisonne ici sur le cœur lisse Cc∞. r compte les jets nuls du test aux ±1/2 ; q compte ceux en 0. Ces jets se distinguent des zéros critiques de ζ. Les nombres S affichés sont une illustration du contrat de support.</p><div class="row"><label>Support S de f <input id="S" type="number" min="0.1" value="1" step="0.5"></label><label>Ordre r aux ±1/2 <input id="r" type="number" min="0" value="1"></label><label>Ordre q en 0 <input id="q" type="number" min="0" value="0"></label><label>Unité A^u <input id="u" type="number" min="0" value="1"></label><label>Geste <select id="op">{''.join('<option value="'+x['op']+'">'+x['label']+'</option>' for x in grammar.RULES)}</select></label><label>Paramètre a,τ ou λ <input id="parameter" type="number" value="1" step="0.5"></label></div><p>Pour une opération à deux fonctions, g porte le même type que f ; il s’agit d’un exemple de calcul de contrats.</p><button id="play">Appliquer le geste</button><div id="result" aria-live="polite"></div><button id="global">Conclure au signe global ?</button><p id="global-result" class="guard" hidden></p></section>
<section class="panel"><h2>Les zones où une clé ouvre deux portes</h2><div class="zones"><div><h3>Algèbre et jets</h3><p>I_r=P^r A. Convolution et opérateurs font circuler des annulations garanties ; les gardes rendent les pertes visibles.</p></div><div><h3>Métrique et queue</h3><p>R donne I−compact et une queue coercive effective. Le contrat entier est démontré ; V6.45 resserre le budget. Pour S=3, q possède 38 chiffres au lieu de 493, encore prohibitif.</p></div><div><h3>Schur et couplages</h3><p>La réduction garde l’infini dans un inverse de queue. V6.45 : un Gram de résidus de sources borne la dette sans solveur Riesz exact. Sources L² et tête complète restent à certifier.</p></div><div><h3>Loi couvrante</h3><p>Décider le signe du Schur pour tous supports demeure ouvert. Branches, collisions et A complexe des anciennes familles gardent leur portée propre.</p></div></div><img src="68_GRAPHE_LANGUE.png" alt="Graphe des preuves et obligations de la langue des passages"></section>
<section class="panel"><h2>Tous les outils des programmes</h2><p id="code-count"></p><label for="code-search">Rechercher une fonction Python ou un fichier</label><input id="code-search" placeholder="nom, signature, docstring, fichier"><div id="code-list"></div><p><a href="../3_Preuves_et_calculs/data/{edition}_index_fonctions.csv">Index complet · CSV</a> · <a href="../3_Preuves_et_calculs/data/{edition}_index_fonctions.json">Index · JSON</a> · <a href="../3_Preuves_et_calculs/data/{edition}_dictionnaire.json">Dictionnaire réutilisable · JSON</a></p><p class="muted">Une déclaration Python peut fabriquer du HTML, lire un fichier ou calculer une matrice. Sa présence dans cet index ne lui attribue pas un statut d’opérateur mathématique.</p></section><footer><p>Périmètre : noyau pédagogique explicite, 95 noms du registre, toutes déclarations Python analysées. Les contrats codés sont partiels ; les preuves sont dans les documents 68, 70 et 71. Aucune preuve de RH annoncée.</p></footer>'''
    js=r'''
const D=JSON.parse(document.getElementById('language-data').textContent);const E=D.dictionary.entries;let selected=E[0].id;
const el=id=>document.getElementById(id);const esc=x=>String(x||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));const norm=x=>String(x).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
function entry(r){selected=r.id;el('entry').innerHTML='<span class="badge">'+esc(r.kind==='math'?'Niveau '+r.level:'Registre historique')+'</span><h2>'+esc(r.name)+'</h2><p><strong>Premier jeu.</strong> '+esc(r.image)+'</p><div class="formula">'+esc(r.symbol)+'</div><p><strong>Sens et domaine.</strong> '+esc(r.exact)+'</p><p class="guard"><strong>Garde.</strong> '+esc(r.guard)+'</p><p class="muted">'+esc(r.status)+'</p><p class="muted">'+esc(r.source)+'</p><p class="muted">Identifiant : '+esc(r.id)+'</p>';}
function filter(){const s=norm(el('search').value),lv=el('level').value,k=el('kind').value;const rows=E.filter(r=>(lv==='all'||String(r.level)===lv)&&(k==='all'||r.kind===k)&&norm([r.name,r.symbol,r.image,r.exact,r.guard].join(' ')).includes(s));el('count').textContent=rows.length+' fiches visibles / '+E.length;el('list').innerHTML=rows.map(r=>'<button data-entry="'+esc(r.id)+'">'+esc(r.name)+' <small>· '+(r.kind==='math'?'N'+r.level:'image')+'</small></button>').join('');if(rows.length&&!rows.some(r=>r.id===selected))entry(rows[0]);if(!rows.length)el('entry').innerHTML='<p>Aucune fiche correspondante. Une définition manquante n’est pas inventée.</p>';}
['search','level','kind'].forEach(id=>el(id).addEventListener('input',filter));el('list').addEventListener('click',e=>{const b=e.target.closest('[data-entry]');if(b)entry(E.find(r=>r.id===b.dataset.entry));});
function infer(op,f,p){if(!D.rules.some(r=>r.op===op)||!Number.isFinite(p))throw Error('Geste ou paramètre non reconnu.');const out={...f};if(!Number.isFinite(f.S)||!(f.S>0)||!Number.isSafeInteger(f.r)||f.r<0||!Number.isSafeInteger(f.q)||f.q<0||!Number.isSafeInteger(f.u)||f.u<0)throw Error('Support positif et ordres/degré entiers non négatifs exigés.');if(op==='add'){}else if(op==='multiply'){out.r=0;out.q=0;out.u=2*f.u;}else if(op==='convolve'){out.S=2*f.S;out.r=2*f.r;out.q=2*f.q;out.u=2*f.u;}else if(op==='P'){out.r++;}else if(op==='derivative'){out.q++;}else if(op==='position'){out.r=Math.max(0,f.r-1);out.q=Math.max(0,f.q-1);}else if(op==='translate'){out.S+=Math.abs(p);}else if(op==='modulate'&&p!==0){out.r=0;out.q=0;}else if(op==='rescale'){if(!(p>0))throw Error('Échelle strictement positive exigée.');out.S*=p;out.r=0;/* origin jets preserved by scaling */}return out;}
function play(){try{const op=el('op').value,f={S:Number(el('S').value),r:Number(el('r').value),q:Number(el('q').value),u:Number(el('u').value)},p=Number(el('parameter').value),o=infer(op,f,p),rule=D.rules.find(r=>r.op===op);el('result').textContent='Phrase obtenue : A(S='+o.S+' ; r='+o.r+' ; q='+o.q+' ; unité A^'+o.u+')\n'+(o.r>=1?'Deux moments admissibles garantis.':'Deux moments admissibles non garantis.')+'\nConserve : '+rule.conserves+'\nCoût / perte : '+rule.loss+'\nLe signe de Q_W exige encore son contrat de queue et de Schur.';}catch(e){el('result').textContent='Composition refusée : '+e.message;}}
el('play').addEventListener('click',play);el('global').addEventListener('click',()=>{el('global-result').hidden=false;el('global-result').textContent='Implication globale non acquittée : il manque le signe certifié du Schur effectif et une loi couvrant tous les supports. Les lemmes, la queue positive et les matrices finies ne fournissent pas ces prémisses.';});
function codeFilter(){const s=norm(el('code-search').value);const rows=D.code.entries.filter(r=>norm([r.path,r.name,r.signature,r.docstring].join(' ')).includes(s));el('code-count').textContent=D.code.entries.length+' déclarations techniques indexées ; '+rows.length+' correspondances. Les 40 premières sont affichées.';el('code-list').innerHTML=rows.slice(0,40).map(r=>'<details><summary>'+esc(r.name)+' · '+esc(r.kind)+'</summary><p>'+esc(r.path)+':'+r.line+'</p><code>'+esc(r.signature)+'</code><p>'+esc(r.docstring||'Aucune docstring ; comportement non inféré.')+'</p></details>').join('');}el('code-search').addEventListener('input',codeFilter);filter();entry(E[0]);play();codeFilter();
window.languageGrammar={infer,filter,entry,codeFilter};
'''
    if edition in ('v645','v646'):
        body=body.replace('</header>','<p><a href="70_PONT_ARITHMETIQUE.html">Pont arithmétique et dette · atelier V6.45</a> · <a href="70_PONT_ARITHMETIQUE_ET_DETTE_DE_COUPLAGE.pdf">Document 70 · PDF</a> · <a href="70_PONT_ARITHMETIQUE_ET_DETTE_DE_COUPLAGE.tex">LaTeX</a></p></header>',1)
    if edition=='v646':
        body=body.replace('</header>','<p><a href="71_LEGO_REUTILISABLE.html">Lego V6.46 : certificat complet sur tous tests, 0&lt;S≤0,347</a> · <a href="71_LEGO_REUTILISABLE_ET_PREMIER_CERTIFICAT_COMPLET.pdf">Document71 · PDF</a></p></header>',1)
        body=body.replace('V6.45 : un Gram de résidus','V6.45–V6.46 : projection commune et Gram de résidus')
        body=body.replace('sa tête grossière reste immense.','sa tête grossière reste immense.')
    body=body.replace('src="68_GRAPHE_LANGUE.png"','src="data:image/png;base64,'+base64.b64encode((P/'68_GRAPHE_LANGUE.png').read_bytes()).decode()+'"')
    (P/'69_LANGUE_DES_PASSAGES.html').write_text('<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+version+' · Langue des passages</title><style>'+css+'</style></head><body><main>'+bi.topnav('graphe','../')+body+'</main><script id="language-data" type="application/json">'+json.dumps(payload,ensure_ascii=False).replace('</',r'<\/')+'</script><script>'+js+'</script></body></html>')
def main():
    module('dict644',ROOT/'2_Methode/Outils/build_v644_dictionary.py').main()
    figure();interactive();report();dictionary()
    print('V644 : deux PDF/LaTeX, graphe et dictionnaire/grammaire autonome')
if __name__=='__main__':main()
