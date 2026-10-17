"""Build the reproducible document 62: atlas HTML, Markdown, PDF and sensitivity figure."""
from pathlib import Path
import json
import html
import importlib.util
import subprocess
import tempfile
import shutil
import base64

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / '1_Presentation'
D = ROOT / '3_Preuves_et_calculs/data'
STEM = '62_ATLAS_DES_DECISIONS_BELLMAN'

def load(name):
    return json.loads((D / name).read_text(encoding='utf-8-sig'))

def plain(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return '; '.join(plain(x) for x in value)
    if isinstance(value, dict):
        return '; '.join(str(k) + ': ' + plain(v) for k, v in value.items())
    return str(value or '')

def short(value, n=55):
    words = plain(value).split()
    return ' '.join(words[:n]) + (' [...]' if len(words) > n else '')

def source_path(record):
    for source in record.get('sources', []):
        if isinstance(source, str):
            return source
        if source.get('path'):
            return source['path']
    candidates = sorted(P.glob(f"{int(record['numero']):02d}_*.md"))
    candidates += sorted(P.glob(f"{int(record['numero']):02d}_*.pdf"))
    candidates += sorted(P.glob(f"{int(record['numero']):02d}_*.docx"))
    return str(candidates[0].relative_to(ROOT)) if candidates else ''

def figure(model, results):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    rows = results['results']
    labels = [a['label'] for a in model['actions']]
    matrix = np.array([[x['in_all_optimal_portfolios'][a['id']] for x in rows] for a in model['actions']])
    fig, ax = plt.subplots(figsize=(10.5, 6.4))
    ax.imshow(matrix, cmap='Blues', vmin=0, vmax=243, aspect='auto')
    ax.set_xticks(range(4), [str(x['budget']) + ' H' for x in rows])
    ax.set_yticks(range(len(labels)), labels, fontsize=9)
    for i in range(len(labels)):
        for j in range(4):
            ax.text(j, i, f'{matrix[i,j]}/243', ha='center', va='center', fontsize=10,
                    color='white' if matrix[i,j] > 150 else '#173249')
    ax.set_title('Présence dans tous les portefeuilles optimaux\nFréquences sur une grille de poids, sans interprétation probabiliste', fontsize=12, pad=15)
    ax.set_xlabel('Budget conventionnel ; coûts de base')
    fig.tight_layout()
    fig.savefig(P / '62_Bellman_sensibilite.png', dpi=170)
    plt.close(fig)

def markdown(registry, model, result):
    lines = ['# V6.38 - Atlas des décisions et équations de Bellman', '',
             '**Document 62. Vincent P. P. NOËL. 12 octobre 2026.**', '',
             'Type : atlas de recherche, audit documentaire et modèle de planification reproductible. Ce document ne constitue ni un nouvel article prouvant RH, ni une expertise externe de toutes les preuves du corpus.', '',
             '## 1. État final recherché', '',
             'La reprise vise un corpus dans lequel une prochaine décision peut être justifiée : acquis, hypothèses, réfutations, questions ouvertes, dépendances et contrôles sont traçables. Son état final documentaire est un atlas relié aux sources et un modèle explicite comparant des suites de livrables. L’état final mathématique reste distinct : construire un mécanisme arithmétique qui impose la positivité pertinente pour ζ sur toute la classe requise, puis établir son implication vers RH.', '',
             'Le registre couvre les 61 documents de présentation de la base V6.37, les étapes historiques de l’indicateur et des annexes de preuve/relecture sélectionnées. Un inventaire séparé recense tous les fichiers. Cette couverture documentaire ne signifie pas que chaque preuve, chaque ligne de code ou chaque citation externe a reçu une nouvelle validation indépendante. Les trois articles sont situés à travers leurs documents de présentation et les annexes lues.', '',
             'Les anciennes synthèses 01, 06 et 07 restent des vues historiques. Les demandes de relecture 04 et 05 sont des brouillons : aucun envoi ni avis de spécialiste n’est attesté. Les documents historiques gardent leur portée d’origine ; leurs correctifs sont exposés séparément.', '',
             '## 2. Ce que la reprise change', '',
             '| Point | Lecture actuelle |', '|:--|:--|',
             '| Énergie Q | Quantité quadratique non négative ; pour ζ, le demi-exposant normalisé vaut Θ−1/2 dans le Théorème A. L’exposant de Q est 2Θ−1. Une fenêtre n’atteint pas automatiquement le supremum global. |',
             '| Positivité de ζ | Observations dans des compressions et seuils testés ; aucune positivité globale obtenue par le corpus. |',
             '| DH, document 60 | Certificat d’au moins 25 directions négatives dans une fenêtre fixée, sous le modèle d’erreur explicité ; compte exact ouvert. |',
             '| V13, document 61 | 72 couples préfixés ; A1 :36/36 détections tardives ; D :25 précoces,8 tardives,3 mêmes tranches. Association descriptive, sans causalité ni certificat d’absence antérieure. |',
             '| Relief T* | Déficit relatif persistant, pas hauteur absolue de la première sortie. |',
             '| Générateur D | Reconstruction exponentielle ne garantit pas un logarithme unique : choix de branche nécessaire. |',
             '| Maillons ouverts | Compte de catégories, sans distance chiffrée à RH ni nombre garanti d’étapes. |', '',
             'Les prévisions avant calcul sont conservées. Une thèse ancienne et son bilan sont deux objets différents : le champ « fait » atteste l’exécution d’un travail, pas la vérité de sa thèse.', '',
             '## 3. Thèse, antithèse et synthèse', '',
             '**Thèse constructive.** Bellman relie une action à ce qu’elle ouvre ensuite. Reproduire un certificat, établir l’impossibilité d’un appariement ou invalider une prévision peut avoir une utilité de recherche. Le registre doit créditer les acquis nouveaux, et non un simple changement de présentation.', '',
             '**Antithèse critique.** Le corpus contient surtout la trajectoire effectivement suivie. Les résultats des alternatives non choisies ne sont pas connus. Les récompenses, les coûts et le découpage des actions restent des conventions ; le passé relu après connaissance du résultat n’est pas un préenregistrement. L’état réel de la recherche n’est pas établi comme markovien.', '',
             '**Synthèse.** Nous construisons une planification documentaire finie et conditionnelle, avec ses limites visibles. Son optimalité se démontre et se contrôle exactement dans le modèle ; elle ne démontre pas l’optimalité scientifique réelle de la stratégie.', '',
             '## 4. États, unités et deux écritures de Bellman', '',
             'L’état est (D,b) : ensemble des actions déjà achevées et budget restant. Une action n’est admissible que si ses prérequis sont achevés. Chaque action coûte un nombre entier strictement positif de H, unité conventionnelle de travail ; H n’est pas une heure mesurée. Chaque token représente un livrable documentaire vérifiable, y compris un rapport concluant à un obstacle. La catégorie « certification » évalue un dossier de contrôle ; elle ne promet pas un nouveau théorème.', '',
             r'\[ U(D)=\sum_{k\in\cup_{a\in D}K(a)}w_{j(k)},\qquad [U]=\mathsf U,\quad[b]=[c]=\mathsf H. \]', '',
             'Les cinq critères sont discrimination, certification, reproduction, articulation et transmission. Les coefficients numériques des profils sont 1, 2 ou 3 ; un poids dimensionné est ce coefficient multiplié par l’unité U par token. Un même token partagé n’est compté qu’une fois. Cette homogénéité ne transforme pas l’utilité en énergie physique, et n’identifie pas U à Q.', '',
             r'\[V(D,b)=\max\{U(D),\max_{a\text{ admissible}}V(D\cup\{a\},b-c(a))\}.\]', '',
             'La première possibilité est STOP. V comprend les acquis et V(D,0)=U(D). Pour la valeur des gains nouveaux W=V−U, on a W(D,0)=0 et la récompense immédiate est U(D union {a})−U(D). Cette différence empêche le double comptage. Les coûts positifs et les actions uniques rendent l’horizon fini : aucun facteur γ inférieur à 1 n’est nécessaire. La preuve complète figure dans l’annexe des lemmes.', '',
             'Une efficacité documentaire peut être définie par ΔU/ΔH, avec unité U/H. Elle demeure un rapport conventionnel de planification ; aucune puissance physique ni propriété arithmétique nouvelle n’en résulte.', '',
             '## 5. Neuf actions explicites, avec achèvement conditionnel', '',
             '| Action | Coût H et prérequis | Livrable |', '|:--|:--|:--|']
    names = {a['id']: a['label'] for a in model['actions']}
    for a in model['actions']:
        req = ', '.join(names[k] for k in a['requires']) or 'aucun'
        lines.append(f"| {a['label']} | {a['cost']} ; {req} | {a['output']} |")
    lines += ['', 'La sélection de ces neuf actions n’est pas justifiée par Bellman lui-même. Elle découle des questions ouvertes identifiées dans le corpus. Les tokens et les coûts favorisent ici des dossiers préparatoires bon marché : leur présence dans un optimum ne constitue pas une découverte autonome de leur supériorité scientifique. Si les contraintes V13 sont impossibles, la suite est un rapport de fermeture de branche, pas une expérience fictivement réalisée.', '',
              '## 6. Calcul exécuté et sensibilité', '',
              'La prévision informatique a été enregistrée avant l’exécution. La programmation dynamique est comparée à une énumération indépendante des sous-ensembles réalisables : les 972 configurations passent, soit 4 budgets et 243 profils de poids. La lecture critique a aussi recoupé les valeurs, tous les portefeuilles et tous les premiers choix avec sa propre reconstruction. Il n’y a ni probabilités de transition apprises, ni taux de réussite scientifique estimé.', '',
              '| Budget | Portefeuille à poids égaux | Valeur U |', '|:--|:--|:--|']
    short_names = {'v13_contraintes':'V13 contraintes', 'v13_comparaison':'V13 comparaison',
                   'dh_rejeu':'DH rejeu', 'dh_fenetres':'DH fenêtres', 'nb_audit':'NB audit',
                   'nb_reste':'NB reste', 'sources_conditions':'Sources',
                   'dossier_relecture':'Dossier humain', 'bellman_objet':'Bellman spectral'}
    for b in result['results']:
        portfolios = [' + '.join(short_names[k] for k in p) for p in b['equal_weights']['portfolios']]
        lines.append(f"| {b['budget']} H | {' OU '.join(portfolios)} | {b['equal_weights']['value']} |")
    lines += ['', 'Un portefeuille n’impose pas un ordre unique. Dans ce modèle à utilité terminale, plusieurs actions préparatoires peuvent être des premiers choix optimaux du même portefeuille. Tous les ex aequo sont conservés.', '',
              '![Présence dans tous les portefeuilles optimaux, sur 243 profils de poids. Ces fréquences ne sont pas des probabilités.](62_Bellman_sensibilite.png)', '',
              'À budget 4, les contraintes V13 appartiennent à tous les portefeuilles optimaux pour les243 profils testés, sans imposer qu’elles soient réalisées en premier. À budget 6, contraintes V13, rejeu DH, audit NB et sources appartiennent à tous les portefeuilles optimaux sur cette grille. Ce constat vaut pour les coûts de base et les poids 1, 2, 3 ; il ne vaut pas pour tous les coûts ou tous les poids possibles.', '',
              'Trois scénarios de coûts illustrent cette limite : comparaison V13 coût 1, extension DH coût 1, et contraintes V13 coût 2. À budget 2 et poids égaux, doubler le coût des contraintes V13 remplace le couple contraintes V13 + rejeu DH par rejeu DH + audit NB OU rejeu DH + sources. Les coûts doivent donc être confrontés à du travail effectivement mesuré avant usage prescriptif fort.', '',
              '## 7. Un pont mathématique précis, encore local', '',
              'Pour une matrice hermitienne G sur un espace muni d’un produit scalaire positif fixé, on peut organiser la minimisation de la trace sur un repère orthonormé par Bellman :', '',
              r'\[ B_k(W)=\min_{\substack{v\in W\\\|v\|=1}}[\langle v,Gv\rangle+B_{k-1}(W\cap v^\perp)],\quad B_0(W)=0.\]', '',
              'Le résultat est la somme des k plus petites valeurs propres du comprimé. La preuve par décomposition dans une base propre est donnée dans l’annexe. C’est une réécriture variationnelle classique, distincte du modèle documentaire ; elle ne fournit pas à elle seule une nouvelle borne.', '',
              'Une trace négative ne prouve pas k directions négatives : diag(−100,1) a une trace négative et une seule direction négative. Le certificat V6.36 contrôle une compression strictement négative de dimension 25, termes croisés et erreurs compris. Une contraction artificielle ou un optimum de trace ne remplace pas ce contrôle, ni une preuve de positivité générale pour ζ.', '',
              '## 8. Priorité proposée et critères d’arrêt', '',
              'La recommandation opérationnelle est de préciser les contraintes V13 exactes avant de relancer un comptage : même ancre, même rayon, même coefficient complexe et sa phase. Si le noyau admissible ne permet aucune variation de D, l’expérience doit être close dans cette strate. Si des couples existent, ils doivent être figés avant le calcul, avec contours, raffinements et traitement explicite des non-détections. Cette recommandation s’appuie sur la question ouverte de V6.37, pas sur un premier choix unique imposé par Bellman.', '',
              'En parallèle, le rejeu du témoin DH, l’audit des conditions NB et des sources prioritaires sont des contrôles séparés. Une extension DH exige un nouveau budget d’erreur ; un calcul spectral favorable ne suffit pas. Une borne NB doit contrôler les termes effectivement requis ; la tendance numérique de beta ne suffit pas.', '',
              'L’atlas est achevé quand les 61 documents sont reliés aux sources, les décisions passées séparées de leur interprétation, les scénarios reproductibles et les pages actives synchronisées. Le protocole mathématique reste ouvert après cet achèvement documentaire.', '',
              '## 9. Annexes reproductibles et source historique', '',
              '- Registre complet : ../3_Preuves_et_calculs/data/v638_decisions.json.',
              '- Inventaire exhaustif : ../3_Preuves_et_calculs/data/v638_inventaire.json.',
              '- Modèle et résultats : ../3_Preuves_et_calculs/data/v638_modele_bellman.json et v638_bellman_resultats.json.',
              '- Deux lectures : ../3_Preuves_et_calculs/preuves/LECTURE_CONSTRUCTIVE_BELLMAN_V638.md et LECTURE_CRITIQUE_BELLMAN_V638.md.',
              '- Preuves : ../3_Preuves_et_calculs/preuves/LEMMES_BELLMAN_V638.md.',
              '- Reproduction : python 3_Preuves_et_calculs/scripts/run_v638_bellman.py ; python 2_Methode/Outils/build_v638_atlas.py ; python 3_Preuves_et_calculs/tests/run_all_tests.py.', '',
              'Source historique [Bel53] : R. Bellman, Some Functional Equations in the Theory of Dynamic Programming, PNAS39 (1953),1077-1082, DOI10.1073/pnas.39.10.1077 ; https://pubmed.ncbi.nlm.nih.gov/16589377/. Notice primaire vérifiée ; texte intégral non audité. Les deux lemmes de cette reprise sont entièrement démontrés dans l’annexe.', '',
              '## 10. Répertoire des 61 documents de la base V6.37', '',
              'Les notices suivantes sont une synthèse courte. Les champs complets, alternatives documentées, sections sources, correctifs et limites se trouvent dans l’atlas interactif et le registre JSON.']
    for record in registry['documents']:
        path = source_path(record)
        lines += ['', f"### {int(record['numero']):02d}. {record['titre']}", '',
                  '**Question.** ' + short(record.get('question'), 35), '',
                  '**Bilan.** ' + short(record.get('resultat'), 55), '',
                  '**Statut et portée.** ' + short(record.get('statut'), 20).replace('_',' ') + ' ; ' + short(record.get('limites'), 35), '',
                  f"Source : [document {int(record['numero']):02d}](../{path})."]
    return ('\n'.join(lines) + '\n').replace('les243','les 243').replace('dimension25','dimension 25')

def html_atlas(registry, model, results):
    spec = importlib.util.spec_from_file_location('v638_ind', ROOT / '2_Methode/Indicateur/build_indicateur.py')
    bi = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bi)
    state_file=next((D/name for name in ('v642_etat_recherche.json','v641_etat_recherche.json','v640_etat_recherche.json','v639_etat_recherche.json') if (D/name).exists()),D/'v639_etat_recherche.json')
    state=json.loads(state_file.read_text(encoding='utf-8-sig')) if state_file.exists() else None
    payload = json.dumps({'registry': registry, 'model': model, 'results': results, 'current_state':state}, ensure_ascii=False).replace('</', '<\\/')
    css = '''body{margin:0;background:#f5f4ef;color:#182e3b;font:16px/1.6 system-ui,sans-serif}main{max-width:1100px;margin:auto;padding:24px}h1,h2{font-family:Georgia,serif;line-height:1.2}h1{font-size:38px}h2{font-size:26px}nav{display:flex;gap:14px;flex-wrap:wrap;border-bottom:1px solid #c9d3d5;padding-bottom:14px}a{color:#135577}section,details{background:#fff;border:1px solid #d8e0e1;border-radius:6px;padding:20px;margin:18px 0}summary{cursor:pointer;font-weight:650}.muted{color:#526672;font-size:14px}.controls{display:flex;gap:16px;flex-wrap:wrap}label{display:grid;gap:4px}input,select{font:inherit;border:1px solid #8195a0;border-radius:4px;padding:7px}input[type=search]{width:min(95%,600px)}table{border-collapse:collapse;width:100%;font-size:14px}th,td{padding:9px;text-align:left;vertical-align:top;border-bottom:1px solid #dfe6e7}.tablewrap{overflow:auto}.tag{display:inline-block;background:#e8f0f1;padding:3px 9px;border-radius:3px;font-size:13px}#plan{border-left:4px solid #28708b;padding-left:15px}img{width:100%;height:auto}button{font:inherit;cursor:pointer}.docfield{margin:12px 0}.docfield b{display:block}footer{padding:20px 0} @media(max-width:600px){main{padding:14px}h1{font-size:30px}section,details{padding:14px}}'''
    body = '''<header><p class="muted">Programme Riemann · V6.38 · 12 octobre 2026</p><h1>Atlas des décisions</h1><p>Les61 documents de la base V6.37, leurs questions et leurs limites ; un modèle de Bellman pour comparer des suites de livrables.</p></header>
<section><h2>État final recherché</h2><p>Choisir la prochaine recherche avec des raisons vérifiables : acquis, hypothèses, réfutations, dépendances et contrôles reliés aux sources. La cible mathématique demeure un mécanisme arithmétique imposant la positivité pertinente pour ζ ; cette construction reste ouverte.</p><p><a href="62_ATLAS_DES_DECISIONS_BELLMAN.pdf">Lire l’atlas PDF</a> · <a href="../3_Preuves_et_calculs/preuves/LEMMES_BELLMAN_V638.md">Lemmes et preuves</a> · <a href="../3_Preuves_et_calculs/data/v638_decisions.json">Registre complet</a></p><p class="muted">Couverture documentaire et inventaire exhaustif ; aucune nouvelle validation indépendante de toutes les mathématiques ni de toutes les citations externes n’est revendiquée.</p></section>
<section><h2>Comparer les suites de travaux</h2><p>H est une unité conventionnelle de travail, sans conversion en heures. U mesure des livrables documentaires proposés. Le calcul suppose leur achèvement, y compris un rapport concluant à une impossibilité. Aucun succès mathématique n’est promis.</p><div class="controls"><label>Budget H<select id="budget"><option>2</option><option selected>4</option><option>6</option><option>8</option></select></label><label>Coûts<select id="cost"><option value="base">Coûts de base</option><option value="v13_comparaison">Comparaison V13 : coût 1</option><option value="dh_fenetres">Extension DH : coût 1</option><option value="v13_contraintes">Contraintes V13 : coût 2</option></select></label></div><div class="controls" id="weights"></div><div id="plan" aria-live="polite"></div><p class="muted">Les poids et coûts sont des choix de modèle. Les ex aequo sont conservés ; un portefeuille optimal n’impose pas un ordre unique. Les coûts de base favorisent les dossiers préparatoires bon marché. Bellman ne justifie pas lui-même ce découpage.</p></section>
<section><h2>Sensibilité aux préférences</h2><img src="62_Bellman_sensibilite.png" alt="Présence des actions dans tous les portefeuilles optimaux sur 243 profils de poids et quatre budgets"><p class="muted">Fréquences sur la grille 1, 2, 3 des cinq critères ; ce ne sont pas des probabilités. Les972 configurations concordent avec une énumération indépendante. Coûts de base uniquement.</p></section>
<section><h2>Ce qui reste ouvert</h2><p>Au moins25 directions négatives DH sont certifiées dans une fenêtre fixée ; le compte exact et les autres fenêtres restent ouverts. V13 montre une association numérique, sans causalité ni certificat d’absence antérieure. Pour NB, le contrôle des termes requis ne découle pas d’une simple tendance de beta. Une trace minimale négative ne prouve pas un sous-espace de dimension k strictement négatif.</p><p><a href="../3_Preuves_et_calculs/preuves/LECTURE_CONSTRUCTIVE_BELLMAN_V638.md">Lecture constructive</a> · <a href="../3_Preuves_et_calculs/preuves/LECTURE_CRITIQUE_BELLMAN_V638.md">Lecture critique</a> · <a href="../3_Preuves_et_calculs/data/v638_corrections_actives.json">Corrections des pages actives</a></p></section>
<section><h2>Parcourir les 61 documents</h2><p>État antérieur, action, résultat et correctifs restent séparés. Les anciennes synthèses sont des vues historiques ; « travail fait » ne signifie pas « thèse démontrée ».</p><label>Rechercher une question, un résultat ou un numéro<input id="search" type="search" placeholder="Ex. jets, DH, ancrage, réfutation"></label><p id="count" class="muted"></p><div id="documents"></div></section>
<footer class="muted">Auteur : Vincent P. P. NOËL. Généré depuis les sources du corpus ; aucune expertise externe ou publication scientifique nouvelle revendiquée.</footer>'''
    script = (ROOT / '2_Methode/Outils/bellman_atlas_client.js').read_text() + '''
const data=JSON.parse(document.getElementById('atlas-data').textContent), base=data.model;
const labels=Object.fromEntries(base.actions.map(a=>[a.id,a.label]));
const weightsBox=document.getElementById('weights');
base.criteria.forEach(c=>{const label=document.createElement('label');label.textContent=c.charAt(0).toUpperCase()+c.slice(1);const s=document.createElement('select');s.id='w-'+c;[1,2,3].forEach(n=>{const o=document.createElement('option');o.value=n;o.textContent=n;s.append(o)});label.append(s);weightsBox.append(label);s.addEventListener('change',showPlan)});
function showPlan(){const model=JSON.parse(JSON.stringify(base)),scenario=document.getElementById('cost').value;if(scenario!=='base')model.actions.find(a=>a.id===scenario).cost=scenario==='v13_contraintes'?2:1;const weights=Object.fromEntries(base.criteria.map(c=>[c,Number(document.getElementById('w-'+c).value)]));const completed=(data.current_state&&document.getElementById('initial-state')&&document.getElementById('initial-state').value==='current')?data.current_state.completed_bellman_actions:[];const solution=solveAtlas(model,Number(document.getElementById('budget').value),weights,completed);const out=document.getElementById('plan');out.replaceChildren();const p=document.createElement('p');p.textContent='Utilité terminale : '+solution.value+' U ; gain supplémentaire : '+solution.gain+' U ; '+solution.portfolios.length+' portefeuille(s) optimal(aux).';out.append(p);solution.portfolios.forEach(port=>{const p=document.createElement('p');p.textContent=port.filter(k=>!completed.includes(k)).map(k=>labels[k]).join(' + ')||'STOP';out.append(p)});const last=document.createElement('p');last.textContent='Premiers choix équivalents : '+solution.first_choices.map(k=>labels[k]||k).join(' ; ');out.append(last)}
if(document.getElementById('initial-state'))document.getElementById('initial-state').addEventListener('change',showPlan);document.getElementById('budget').addEventListener('change',showPlan);document.getElementById('cost').addEventListener('change',showPlan);showPlan();
function textOf(v){if(typeof v==='string')return v;if(Array.isArray(v))return v.map(textOf).join('; ');if(v&&typeof v==='object')return Object.entries(v).map(([k,x])=>k+': '+textOf(x)).join('; ');return String(v||'')}
function renderDocs(){const query=document.getElementById('search').value.toLocaleLowerCase('fr');const box=document.getElementById('documents');box.replaceChildren();const docs=data.registry.documents.filter(r=>JSON.stringify(r).toLocaleLowerCase('fr').includes(query));document.getElementById('count').textContent=docs.length+' / 61 documents';docs.forEach(r=>{const detail=document.createElement('details'),sum=document.createElement('summary');sum.textContent=String(r.numero).padStart(2,'0')+'. '+r.titre;detail.append(sum);[['etat_anterieur','État antérieur'],['question','Question'],['action','Action'],['resultat','Résultat'],['statut','Statut'],['nature','Nature'],['consequences','Conséquences'],['alternatives_documentees','Alternatives documentées'],['correctifs_ulterieurs','Correctifs ultérieurs'],['limites','Limites']].forEach(([k,label])=>{if(!r[k])return;const p=document.createElement('p'),b=document.createElement('b');p.className='docfield';b.textContent=label;p.append(b,document.createTextNode(textOf(r[k])));detail.append(p)});(r.sources||[]).forEach(s=>{const path=typeof s==='string'?s:s.path;if(!path)return;const p=document.createElement('p'),a=document.createElement('a');a.href='../'+path;a.textContent='Source : '+path.split('/').pop();p.append(a);detail.append(p)});box.append(detail)})}
document.getElementById('search').addEventListener('input',renderDocs);renderDocs();
'''
    if state:
        version=state['version']
        body=body.replace('Programme Riemann · V6.38 · 12 octobre 2026',f'Programme Riemann · {version} · 12 octobre 2026')
        if version=='V6.42':
            banner='<section><h2>État V6.42 : un pli et sa paire certifiés</h2><p>Existence et unicité locales, contour continu de deux zéros et quatre boîtes de racines validés par intervalles. Un résultat local choisi, avec backend et domaine explicités. <a href="66_GRAPHE_DES_CERTIFICATS.html">Graphe courant</a> · <a href="66_UN_PLI_CERTIFIE_ET_SA_PAIRE.pdf">Dossier et preuves</a> · <a href="66_UN_PLI_CERTIFIE_ET_SA_PAIRE.tex">LaTeX</a>.</p><p>L’inégalité arithmétique de Weil est explicitée ; son signe global reste ouvert. Une métrique positive du compagnon au pli et une norme uniforme de la seule partie première sur L² sont des voies fermées dans leurs domaines précisés.</p><p>Modèle documentaire : douze actions, cinq achevées. Le contrôle des sources de Weil est inclus dans l’audit du contrat ; l’action plus large de sources prioritaires reste distincte. Cette dépendance est corrigée dans le nouveau modèle éditorial, après résultats.</p></section>'
            initial_label='V6.42 : cinq dossiers achevés'
            body=body.replace('Les61 documents de la base V6.37',f"Les {len(registry['documents'])} documents du corpus courant")
            body=body.replace('Lire l’atlas PDF','Lire l’atlas historique V6.38 (PDF)').replace('data/v638_decisions.json','data/v642_decisions.json')
            body=body.replace('src="62_Bellman_sensibilite.png"','src="66_Bellman_sensibilite.png"').replace('Les972 configurations','Les 972 configurations du modèle courant')
            body=body.replace('V13 montre une association numérique, sans causalité ni certificat d’absence antérieure.','V13 : un pli choisi et une paire locale sont certifiés ; l’association de D reste descriptive et l’absence antérieure globale non certifiée.')
        elif version=='V6.41':
            banner='<section><h2>État V6.41 : le graphe des passages</h2><p>Fibres pour A prescrit, jets, 20 candidats de collisions, six plis attribués, 18 blocs et 24 racines recoupées. Les mesures restent numériques. <a href="65_GRAPHE_DES_PASSAGES.html">Graphe, énoncés et preuves</a> · <a href="65_FIBRES_PLIS_ET_POSITIVITE.pdf">Dossier PDF</a> · <a href="65_FIBRES_PLIS_ET_POSITIVITE.tex">LaTeX</a>.</p><p>La destination RH est précise ; le pont arithmétique reste ouvert. Deux voies sont distinguées : positivité sur tous les tests de Weil, ou borne Q(X)=X^{o(1)} depuis les premiers. Modèle courant : douze actions, dont contraintes, comparaison et passages V13 achevés. Neuf actions historiques conservées dans le modèle V6.38 ; coûts et poids conventionnels.</p></section>'
            initial_label='V6.41 : trois actions V13 achevées'
            body=body.replace('Les61 documents de la base V6.37',f"Les {len(registry['documents'])} documents du corpus courant")
            body=body.replace('Lire l’atlas PDF','Lire l’atlas historique V6.38 (PDF)')
            body=body.replace('data/v638_decisions.json','data/v641_decisions.json')
            body=body.replace('src="62_Bellman_sensibilite.png"','src="65_Bellman_sensibilite.png"')
            body=body.replace('Les972 configurations','Les 972 configurations du modèle courant')
            body=body.replace('Les coûts de base favorisent les dossiers préparatoires bon marché.','La grille actuelle inclut aussi un audit de certification locale et le contrat global ; les coûts restent des choix documentaires.')
        elif version=='V6.40':
            banner='<section><h2>État V6.40 : comparaison exacte V13 achevée</h2><p>12 couples conservés : 8 détections plus précoces et 4 plus tardives à D élevé ; 24 racines hors droite recoupées. Le signe dépend de l’ancre. <a href="64_COMPARAISON_EXACTE_V13.pdf">Bilan, lemmes et suite</a> · <a href="64_COMPARAISON_EXACTE_V13.tex">Source LaTeX</a>.</p><p>Les actions contraintes et comparaison sont achevées. La continuation des branches est proposée dans le navigateur ; elle ne figure pas encore dans les neuf actions du modèle historique. Les poids et coûts restent conventionnels.</p></section>'
            initial_label='V6.40 : contraintes et comparaison achevées'
        else:
            banner='<section><h2>État V6.39 : contraintes V13 résolues</h2><p>D varie à A=cos(r)z_i, ancre et rayon exactement fixés. <a href="63_CONTRAINTES_EXACTES_V13.pdf">Lire la preuve et les témoins</a>. La comparaison des zéros reste à effectuer.</p></section>'
            initial_label='V6.39 : contraintes V13 achevées'
        body=body.replace('<section><h2>État final recherché</h2>',banner+'<section><h2>État final recherché</h2>')
        body=body.replace('<div class="controls"><label>Budget H',f'<div class="controls"><label>État initial<select id="initial-state"><option value="current">{initial_label}</option><option value="base">Base historique V6.38</option></select></label><label>Budget restant H')
    body=body.replace('Parcourir les 61 documents',f"Parcourir les {len(registry['documents'])} documents")
    if state and state['version']=='V6.42':body=body.replace('Base historique V6.38</option>','Aucune action achevée (modèle courant)</option>')
    if registry.get('version')=='V6.48':
        body=body.replace('<header>','<section><h2>V6.48 : opérateur commun certifié</h2><p><a href="73_OPERATEUR_COMMUN.html">Tous tests jusqu’à1/2 ; tête, sources et queue du minorant</a> · <a href="69_LANGUE_DES_PASSAGES.html">Dictionnaire courant</a>. Multi-premiers, sources fortes de Q et couverture non bornée ouverts.</p></section><header>',1)
        body=body.replace('Comparer les suites de travaux','Modèle documentaire de référence V6.42')
        body=body.replace('data/v642_decisions.json','data/v648_decisions.json')
    elif registry.get('version')=='V6.47':
        body=body.replace('<header>','<section><h2>V6.47 : concentration projetée</h2><p><a href="72_CONCENTRATION_PROJETEE.html">Certificat jusqu’à3/8 et opérateur commun</a> · <a href="69_LANGUE_DES_PASSAGES.html">Dictionnaire courant</a>. Norme à1/2 exploratoire, sources et couverture non bornée ouvertes.</p></section><header>',1)
        body=body.replace('Comparer les suites de travaux','Modèle documentaire de référence V6.42')
        body=body.replace('data/v642_decisions.json','data/v647_decisions.json')
    elif registry.get('version')=='V6.46':
        body=body.replace('<header>','<section><h2>V6.46 : Lego réutilisable</h2><p><a href="71_LEGO_REUTILISABLE.html">Certificat complet et raccords</a> · <a href="69_LANGUE_DES_PASSAGES.html">Dictionnaire courant</a>. Tous tests pour 0&lt;S≤347/1000 ; premier2 présent ; transport non borné ouvert.</p></section><header>',1)
        body=body.replace('Comparer les suites de travaux','Modèle documentaire de référence V6.42')
        body=body.replace('data/v642_decisions.json','data/v646_decisions.json')
    elif registry.get('version')=='V6.45':
        body=body.replace('<header>','<section><h2>V6.45 : pont arithmétique</h2><p><a href="70_PONT_ARITHMETIQUE.html">Fluctuation, budgets et dette</a> · <a href="69_LANGUE_DES_PASSAGES.html">Dictionnaire enrichi</a>. Annulation polaire et obstruction uniforme du modèle continu démontrées ; signe tous supports encore ouvert. <a href="67_GRAPHE_DES_PONTS.html">Pilote des contrats V6.43</a>.</p></section><header>',1)
        body=body.replace('Comparer les suites de travaux','Modèle documentaire de référence V6.42')
        body=body.replace('data/v642_decisions.json','data/v645_decisions.json')
    elif registry.get('version')=='V6.44':
        body=body.replace('<header>','<section><h2>V6.44 : langue des passages</h2><p><a href="69_LANGUE_DES_PASSAGES.html">Dictionnaire et grammaire</a> · <a href="68_ARITHMETIQUE_DES_PASSAGES_ET_QUEUE_EFFECTIVE.pdf">Huit preuves et expériences</a>. Queue positive effective à support fixé ; signe de Schur tous supports encore ouvert. <a href="67_GRAPHE_DES_PONTS.html">Pilote de contrats V6.43</a>.</p></section><header>',1)
        body=body.replace('Comparer les suites de travaux','Modèle documentaire de référence V6.42')
        body=body.replace('data/v642_decisions.json','data/v644_decisions.json')
    elif registry.get('version')=='V6.43':
        body=body.replace('<header>','<section><h2>Pilote de contrats V6.43</h2><p><a href="67_GRAPHE_DES_PONTS.html">Construire et évaluer des ponts</a> : AND/OR, résultats conditionnels et durées. Le calcul documentaire ci-dessous conserve le modèle V6.42 pour comparaison ; il ne pilote plus seul la phase courante.</p></section><header>',1)
        body=body.replace('Comparer les suites de travaux','Modèle documentaire de référence V6.42')
        body=body.replace('data/v642_decisions.json','data/v643_decisions.json')
    script=script.replace("docs.length+' / 61 documents'",f"docs.length+' / {len(registry['documents'])} documents'")
    for image_name in ('62_Bellman_sensibilite.png','65_Bellman_sensibilite.png','66_Bellman_sensibilite.png'):
        if (P/image_name).exists():body=body.replace('src="'+image_name+'"','src="data:image/png;base64,'+base64.b64encode((P/image_name).read_bytes()).decode()+'"')
    return '<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Atlas des décisions</title><style>'+css+'</style><main>'+bi.topnav('atlas','../')+body+'</main><script id="atlas-data" type="application/json">'+payload+'</script><script>'+script+'</script></html>'

def main():
    registry = load('v638_decisions.json')
    assert sorted(int(x['numero']) for x in registry['documents']) == list(range(1,62))
    model = load('v638_modele_bellman.json')
    result = load('v638_bellman_resultats.json')
    figure(model, result)
    (P / (STEM+'.md')).write_text(markdown(registry, model, result), encoding='utf-8-sig')
    source_spec = importlib.util.spec_from_file_location('v638_sources', ROOT/'2_Methode/Sources/build_sources.py')
    source_module = importlib.util.module_from_spec(source_spec)
    source_spec.loader.exec_module(source_module)
    source_module.sync_docs(source_module.load(), write=True)
    html_registry=load('v640_decisions.json') if (D/'v640_decisions.json').exists() else registry
    (P / (STEM+'.html')).write_text(html_atlas(html_registry, model, result))
    header = r'''\usepackage{etoolbox}
\usepackage{microtype}
\setlength{\emergencystretch}{3em}
\AtBeginEnvironment{longtable}{\small}
\AtBeginDocument{\hypersetup{colorlinks=true,linkcolor=blue!45!black,urlcolor=blue!45!black}}
'''
    with tempfile.TemporaryDirectory(prefix='v638_atlas_pdf_') as directory:
        tmp=Path(directory)
        (tmp/'header.tex').write_text(header)
        run=subprocess.run(['pandoc',STEM+'.md','-f','markdown+tex_math_single_backslash',
            '--pdf-engine=xelatex','--resource-path=.','--include-in-header='+str(tmp/'header.tex'),
            '-V','geometry:margin=19mm','-V','papersize=a4','-V','mainfont=DejaVu Sans',
            '-V','monofont=DejaVu Sans Mono','-V','fontsize=10pt','-V','lang=fr-FR',
            '-o',str(tmp/(STEM+'.pdf'))],cwd=P,capture_output=True,text=True)
        (D/'v638_pdf_compile.log').write_text(run.stdout+run.stderr)
        if run.returncode:
            raise RuntimeError(run.stdout+run.stderr)
        shutil.copy2(tmp/(STEM+'.pdf'),P/(STEM+'.pdf'))
    print('Atlas HTML, Markdown and PDF generated')

if __name__ == '__main__':
    main()
