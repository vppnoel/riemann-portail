#!/usr/bin/env python3
"""Rebuild the four living steering views from their shared, reviewed sources.

Run: python -B 2_Methode/Pilotage/build_pilotage.py
No historical scientific calculation or specialist review is claimed by this command.
"""
from pathlib import Path
from collections import Counter
import json,html,hashlib,re,sys,importlib.util
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PRES=ROOT/'1_Presentation'
DATA=ROOT/'3_Preuves_et_calculs/data'
spec=importlib.util.spec_from_file_location('pilotage_engine',HERE/'engine.py')
engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine)
def load_component(name):
    spec=importlib.util.spec_from_file_location('pilotage_'+name,HERE/(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
visuals=load_component('visualisations_claude');advanced=load_component('graphe_avance');navigation=load_component('navigation');catalogue=load_component('catalogue')
INPUTS=['2_Methode/Pilotage/pilotage_recherche.json','2_Methode/Pilotage/graphe_source.json',
        '2_Methode/Indicateur/indicateur_avancement.json','2_Methode/Navigateur/carte_navigation.json',
        '3_Preuves_et_calculs/data/etat_recherche_courant.json','RECUPERATION_2026_10_15.json',
        '3_Preuves_et_calculs/data/parcours_et_proprietes.json',
        '2_Methode/Pilotage/engine.py','2_Methode/Pilotage/ui.js','2_Methode/Pilotage/style.css',
        '2_Methode/Pilotage/build_pilotage.py','2_Methode/Pilotage/registre_identifiants.json',
        '2_Methode/Pilotage/relier_graphes.py','3_Preuves_et_calculs/data/references_graphes.json',
        '2_Methode/Pilotage/style_claude.css','2_Methode/Pilotage/style_graphe_claude.css',
        '2_Methode/Pilotage/style_adapter.css','2_Methode/Pilotage/graphe_layout_claude.html',
        '2_Methode/Pilotage/bellman_contrats_v643.json','2_Methode/Pilotage/bellman_contracts.js',
        '2_Methode/Pilotage/visualisations_claude.py','2_Methode/Pilotage/graphe_avance.py','2_Methode/Pilotage/navigation.py',
        'RECUPERATION_2026_10_15_V651_V652.json','2_Methode/Pilotage/catalogue.py',
        '2_Methode/Sources/sources.json','2_Methode/Sources/references_articles.json','2_Methode/Figures/build_figures.py',
        '2_Methode/Pilotage/reconstruction_integree.py','INTEGRATION_GLOBALE_20261015.json',
        '2_Methode/Pilotage/points_d_attention.json',
        '2_Methode/Pilotage/ciblage.py','2_Methode/Pilotage/ciblage_contrats.json','2_Methode/Pilotage/taches.py']
STATUS={'demontre':'Démontré dans le dossier','classique':'Classique / cité','mesure':'Mesuré dans le cadre déclaré',
        'ouvert':'Ouvert','partiel':'Acquis partiel','conditionnel':'Conditionnel','obstacle':'Obstruction ciblée',
        'diagnostic':'Diagnostic réutilisable','outil':'Outil actif'}

def read(rel):return json.loads((ROOT/rel).read_text(encoding='utf-8-sig'))
def esc(x):return html.escape(str(x),quote=True)
def dump(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def anchor(path,label,prefix=''):return f'<a href="{esc(prefix+path)}">{esc(label)}</a>'

def load_state():
    config=read(INPUTS[0]); ind=read(INPUTS[2]); nav=read(INPUTS[3]); research=read(INPUTS[4]); recovery=read(INPUTS[5])
    actual_hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in config['reviewed_source_hashes']}
    changed=[p for p,h in actual_hashes.items() if h!=config['reviewed_source_hashes'][p]]
    if changed:raise ValueError('Réévaluer les fiches après modification de leurs sources : '+', '.join(changed))

    ids=[n['id'] for n in config['nodes']]
    if len(set(ids))!=len(ids):raise ValueError('Duplicate graph node')
    registry=read('2_Methode/Pilotage/registre_identifiants.json')
    registered={n['key']:n['uid'] for n in registry['ideas']}
    if len(set(registered.values()))!=len(registered):raise ValueError('Duplicate permanent idea ID')
    for n in config['nodes']:
        if registered.get(n['id'])!=n.get('uid'):raise ValueError('Permanent idea ID changed: '+n['id'])
    for e in config['edges']:
        if not {e['source'],e['target'],*e.get('requires',[])}<=set(ids):raise ValueError('Unknown graph endpoint')
    for k,v in config['reviews'].items():
        if v['level']!=ind['etapes'][-1]['niveaux'][k]:raise ValueError(f'Reevaluate dimension {k} after changing its level')
    if ind['comparaison']['apres']!=ind['etapes'][-1]['id']:raise ValueError('Indicator comparison does not reach the current stage')
    engine.validate_model(config['bellman'])
    for a in config['bellman']['actions']:
        if not set(a['nodes'])<=set(ids):raise ValueError('Unknown action graph node')
    for n in config['nodes']:
        for p in n['evidence']:
            if not (ROOT/p).is_file():raise ValueError('Missing evidence '+p)
    # Keep publications directly reachable from each idea; include retained original links.
    node_by_key={n['id']:n for n in config['nodes']}
    for n in config['nodes']:
        candidates=list(n['evidence'])
        candidates+=re.findall(r'href=["\']([^"\']+\.pdf)["\']',n.get('initial_detail_html',''))
        if n['id'] in ['Q_bound','lemmes']:candidates+=node_by_key['thA']['evidence']
        pdfs=[]
        for candidate in candidates:
            candidate=html.unescape(candidate)
            if '://' in candidate:continue
            pdf=str(Path(candidate).with_suffix('.pdf'))
            if (ROOT/pdf).is_file() and pdf not in pdfs:pdfs.append(pdf)
        n['pdf_documents']=pdfs
    publication_hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted({p for n in config['nodes'] for p in n['pdf_documents']})}
    fingerprint=hashlib.sha256(b''.join(p.encode()+b'\0'+(ROOT/p).read_bytes() for p in INPUTS)+json.dumps(actual_hashes,sort_keys=True).encode()+json.dumps(publication_hashes,sort_keys=True).encode()).hexdigest()
    for c in nav['coups']:
        if not c.get('evaluation_courante'):raise ValueError('Unevaluated action '+c['id'])
        if not (ROOT/c['evaluation_courante']['source']).is_file():raise ValueError('Missing action evidence '+c['id'])
    # No success flag may be implied by an interface repair.
    if research['RH_proved'] or research['global_arithmetic_sign_proved'] or research['global_energy_bound_proved']:
        raise ValueError('A new global proof requires a separate scientific review')
    missing=[p for p in recovery['missing_source_paths_from_v649_index'] if not (ROOT/p).is_file()]
    missing_notes=[p for p in ['3_Preuves_et_calculs/preuves/V642_CERTIFICATION_LOCALE.md',
                               '3_Preuves_et_calculs/preuves/V642_CONTRAT_ARITHMETIQUE.md',
                               '3_Preuves_et_calculs/preuves/V643_PONTS_MATHEMATIQUES.md'] if not (ROOT/p).is_file()]
    missing_later=[p for p in recovery.get('remaining_known_missing_references',[]) if not (ROOT/p).is_file()]
    routes=read('3_Preuves_et_calculs/data/parcours_et_proprietes.json')['events']
    for route in routes:
        route['nodes']=config['route_mapping'][route['id']]
        if not set(route['nodes'])<=set(ids):raise ValueError('Unknown route node')
    state=dict(version=config['version'],revision=config['revision'],date=config['date'],fingerprint=fingerprint,
               review_scope=config['review_scope'],primary_pages=config['primary_pages'],research=research,
               indicator=ind,reviews=config['reviews'],gates=config['gates'],nodes=config['nodes'],edges=config['edges'],
               actions=nav['coups'],bellman=config['bellman'],bellman_state=config['bellman_state'],
               investigations=config['investigations'],defects_fixed=config['defects_fixed'],
               historical_recovery_complete=not missing and not missing_notes and not missing_later,missing_historical_sources=missing,
               missing_separate_notes=missing_notes,missing_later_sources=missing_later,recovery=recovery,routes=routes,
               graph_views=config['graph_views'],reference_registry=registry,
               graph_cases=read('3_Preuves_et_calculs/data/references_graphes.json')['cases'],
               attention=read('2_Methode/Pilotage/points_d_attention.json'))
    state['decisions']=[dict(profile=name,weights=w,**engine.solve(engine.apply_weight_profile(config['bellman'],w),b,mode,
                          facts=config['bellman_state']['facts'],completed=config['bellman_state']['completed']))
                        for name,w in config['bellman']['profiles'].items() for b in range(13) for mode in ['lower','upper']]
    # Ciblage en lecture seule (V6.59) : recommandations et fiches proposées, sans effet sur faits, niveaux ou coûts.
    state['targeting']=load_component('ciblage').analyse(ROOT,state)
    # Instantané du registre des fiches : travail en cours, hors empreinte de l'état publié.
    # Les vues lisent un instantané figé à la reconstruction (build_all), jamais le registre vivant :
    # une opération sur une fiche ne doit pas désynchroniser les pages publiées.
    tp=ROOT/'2_Methode/Pilotage/taches_instantane.json'
    state['taches']=json.loads(tp.read_text(encoding='utf-8-sig'))['taches'] if tp.exists() else []
    state['catalogue']=catalogue.collect(state)
    state['catalogue_kinds']=catalogue.KINDS
    state['fingerprint']=hashlib.sha256((fingerprint+json.dumps(state['catalogue'],ensure_ascii=False,sort_keys=True)).encode()).hexdigest()
    return state

def nav_html(state,current,prefix=''):
    return navigation.render_nav(current,prefix,state['primary_pages'])

_NODE_LABELS=None
def node_link(k,label=None):
    global _NODE_LABELS
    if _NODE_LABELS is None:_NODE_LABELS={n['id']:n['title'] for n in read(INPUTS[0])['nodes']}
    return f'<button class="textlink" data-node="{esc(k)}">{esc(label or _NODE_LABELS.get(k,k))}</button>'
def evidence(paths,prefix=''):
    return ' · '.join(anchor(p,Path(p).name,prefix) for p in dict.fromkeys(paths))
def card(k,title,text):return f'<article class="metric"><div class="eyebrow">{esc(k)}</div><strong>{esc(title)}</strong><p>{esc(text)}</p></article>'
def section(title,body,id=None,lead=None):
    return f'<section class="sheet"'+(f' id="{id}"' if id else '')+f'><h2>{title}</h2>'+ (f'<p class="intro">{lead}</p>' if lead else '')+body+'</section>'

def gate_table(s,prefix):
    return '<div class="tablewrap"><table><thead><tr><th>Porte</th><th>Acquis réutilisable</th><th>Obligation courante</th></tr></thead><tbody>'+''.join(
        f'<tr><th>{esc(g["title"])}</th><td>{esc(g["acquired"])}</td><td>{esc(g["remaining"])}<div class="links">'+
        ' · '.join(node_link(k) for k in g['nodes'])+'</div></td></tr>' for g in s['gates'])+'</tbody></table></div>'

def portal(s,prefix):
    r=s['research']; model=s['bellman']; default=next(d for d in s['decisions'] if d['mode']=='lower' and d['budget']==model['default_budget'])
    acts={a['id']:a for a in model['actions']}
    choices=' · '.join(anchor('1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html#contrat-'+k,acts[k]['label'],prefix) if k!='STOP' else 'STOP' for k in default['first_choices'])
    att=s['attention']
    items=''.join(f'<article class="result" id="attention-{esc(pt["id"])}"><h3>{i}. {esc(pt["titre"])}</h3><p class="foot">{esc(pt["statut"])}</p><p>{esc(pt["texte"])}</p><p class="links">'+' · '.join(anchor(b,a,prefix) for a,b in pt['liens'])+'</p></article>' for i,pt in enumerate(att['points'],1))
    body=section('À lire d’abord',f'<p><strong>{esc(att["etat"])}</strong></p>'+items+'<details><summary>Précautions de lecture</summary><ul>'+''.join(f'<li>{esc(x)}</li>' for x in att['precautions'])+'</ul></details><p class="links">'+' · '.join(anchor(b,a,prefix) for a,b in att['outils'])+'</p>',id='a-lire-d-abord')
    body+='<div class="metrics">'+card('But','RH reste ouverte','Loi de signe et couverture de Weil restent à établir.')+card('Dernier acquis',att['dernier_acquis']['titre'],att['dernier_acquis']['texte'])+card('Outils','7 dimensions réévaluées',f'{len(s["actions"])} bilans conservés ; 13 corrections ciblées de statut ou de date.')+'</div>'
    body+=section('Ce qui oriente le travail',
        '<p>Le noyau initial Q, les détecteurs et les certificats locaux restent des briques utilisables. La question centrale est maintenant de faire payer le bilan complet par les vrais poids arithmétiques, sur une famille qui couvre tous les tests.</p>'+
        gate_table(s,prefix),id='portes')
    body+=section('Prochaines investigations, recalculées',
        f'<p><strong>Modèle à contrats du document67, état attesté et budget de {model["default_budget"]} lots H, enveloppe pessimiste :</strong> {choices}.</p>'+
        '<p>Les capacités complémentaires, les issues et les enveloppes sont conservées. Deux études bornées sont rapprochées des bilans ; les obligations globales correspondantes restent ouvertes. Les grands conducteurs V6.55 restent visibles parmi les questions, sans score inventé dans ce modèle.</p>'+
        '<p>'+anchor('1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html#ciblage','Ciblage : que faire maintenant, et qui le fait',prefix)+' · '+anchor('1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html#bellman','Modifier budget, poids et coûts',prefix)+' · '+anchor('00_Carte_des_idees.html','Voir les conséquences jusqu’à RH',prefix)+'</p>',id='choix')
    recent=s['indicator']['etapes'][-3:]
    body+=section('Derniers résultats et leur portée',''.join(
        f'<article class="result"><h3>{esc(e["versions"])}</h3><p>{esc(e["franchi"])}</p><p class="links">'+
        ' · '.join(anchor('1_Presentation/'+p,t,prefix) for t,p in e['documents'])+'</p></article>' for e in reversed(recent)),id='resultats')
    body+=section('Catalogue : documents, fichiers et fiches',catalogue.render(s)+
        '<p class="links">'+evidence(['1_Presentation/44_MATRICE_DES_THEORIES.html','1_Presentation/42_REGISTRE_DES_SOURCES.html','00_Liste_des_figures.html','README.md'],prefix)+'</p>',id='documents')
    papers=[('Article1 — Énergie moyenne et pôles doubles','article1_mean_square_double_poles'),
            ('Article2 — Formes de Weil du côté des premiers','article2_prime_side_weil_forms'),
            ('Article3 — Jets de Hasse et borne spectrale','article3_hasse_jets_and_spectral_bound')]
    paperlinks='<ul>'+''.join('<li>'+esc(label)+' : '+evidence(['1_Presentation/articles/'+stem+'.pdf','1_Presentation/articles/'+stem+'.tex'],prefix)+'</li>' for label,stem in papers)+'</ul>'
    body+=section('Articles PDF et sources LaTeX',paperlinks,id='articles')
    miss=s['missing_historical_sources']
    body+=section('Reproductibilité et continuité',
        '<p><strong>'+str(s['recovery']['files_restored_count'])+' fichiers originaux retrouvés dans votre ZIP V6.50.</strong> Les 27 scripts/modules du relevé V649 et les trois notes recherchées sont réintégrés. Les liens vers leurs preuves et données sont rétablis. Les deux originaux V6.51 non retrouvés ont désormais leurs contrôles reconstruits intégrés, explicitement identifiés.</p>'+
        '<p><strong>La reconstruction V6.51 est intégrée dans ce ZIP global.</strong> Programme, journal calculé, notice et sources sont disponibles depuis les fiches et le catalogue. Les originaux manquants restent distincts de leurs remplaçants reconstruits.</p><p>'+evidence(['1_Presentation/RECONSTRUCTION_V651_INTEGREE.html','4_Exports/V651_RECONSTRUCTION_DOCUMENTEE_20261015.zip','INTEGRATION_GLOBALE_20261015.json'],prefix)+'</p>'+
        '<p>'+evidence(['RECUPERATION.html','RECUPERATION_2026_10_15.json'],prefix)+'</p>'+
        '<details><summary>Récupération, absences restantes et réparations</summary><ul>'+''.join(f'<li>{esc(x)}</li>' for x in s['defects_fixed'])+'</ul>'+
        '<h3>Originaux non retrouvés — reconstructions intégrées</h3><ul class="mono">'+''.join(f'<li>{esc(x)}</li>' for x in miss+s['missing_separate_notes']+s['missing_later_sources'])+'</ul><p>Les absences d’originaux sont recalculées depuis les fichiers présents. Leurs contrôles reconstruits sont fournis séparément dans le corpus et reliés aux fiches. Récupérer un original, vérifier un calcul et démontrer un énoncé restent trois constats distincts.</p></details>'+
        '<p>Le ZIP global '+esc(s['version'])+' est livré avec ce dossier : archive complète, ou deux parties (documents ; preuves et calculs).</p>',id='continuite')
    body+=section('Méthode et références stables',
        '<p>Le protocole de recherche convenu reste la référence : preuves, programmes, analyses critiques, sources LaTeX et PDF. Toute proposition de changement de méthode demande votre accord préalable.</p>'+
        f'<p>{esc(s["version"])} est la version globale. Les documents 1 à {max(d["number"] for d in s["reference_registry"]["documents"])} gardent leurs numéros ; les idées portent un identifiant permanent IDE-xxx, commun aux différentes cartes. Chaque case renvoie au travail et au dossier conservés.</p><p class="links">'+
        evidence(['2_Methode/Pilotage/REGISTRE_DES_IDENTIFIANTS.md','2_Methode/Pilotage/README.md','2_Methode/Pilotage/CONTINUITE_V655.md'],prefix)+'</p>',id='methode')
    return body

def indicator(s,prefix):
    ind=s['indicator']; et=ind['etapes']; dims=ind['dimensions']; current=et[-1]
    rows=[]
    for d in dims:
        v=s['reviews'][d['id']]
        rows.append(f'<tr><th>{esc(d["nom"])}<span class="level">{v["level"]}/9</span></th><td>{esc(v["reason"])}</td><td>{esc(v["change"])}<p class="links">{evidence(v["evidence"],prefix)}</p></td></tr>')
    body=section('Le parcours, dimension par dimension',visuals.render_indicator_chart(s,prefix),id='graphiques-indicateurs')
    body+=section('Évaluation actuelle des sept dimensions',
        '<p>Les sept niveaux ont été réexaminés. Ils restent inchangés parce que les nouveaux résultats ne franchissent pas les critères globaux ni la relecture externe. Leur stabilité n’est plus une absence d’évaluation.</p>'+
        '<div class="tablewrap"><table><thead><tr><th>Dimension</th><th>Pourquoi ce niveau est maintenu</th><th>Ce qui permettrait la marche suivante</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>',id='evaluations')
    hist=[]
    for i,e in enumerate(et):
        delta={k:e['niveaux'][k]-et[i-1]['niveaux'][k] for k in e['niveaux'] if i and e['niveaux'][k]!=et[i-1]['niveaux'][k]}
        names={d['id']:d['nom'] for d in dims}
        change=', '.join(f'{names[k]} {v:+}' for k,v in delta.items()) if delta else 'Niveaux stables'
        hist.append(f'<tr data-search-row><th>{esc(e["versions"])}<small>{esc(e["jour"])}</small></th><td>{esc(e["franchi"])}</td><td>{esc(change)}</td><td>'+ ' · '.join(anchor('1_Presentation/'+p,t,prefix) for t,p in e['documents'])+'</td></tr>')
    body+=section('Parcours continu : toutes les étapes','<label class="search">Filtrer les étapes <input type="search" data-search="history" placeholder="certificat, couverture, V6.49…"></label><details><summary>Consulter les '+str(len(et))+' étapes et leurs pièces</summary><div class="tablewrap"><table id="history"><thead><tr><th>Étape</th><th>Acquis déclaré et limites</th><th>Évolution de niveau</th><th>Documents</th></tr></thead><tbody>'+''.join(hist)+'</tbody></table></div></details>',id='parcours')
    ladder='<ol start="0" class="ladder">'+''.join(f'<li><b>{i}. {esc(t)}</b><span>{esc(x)}</span></li>' for i,(t,x) in enumerate(ind['echelle']))+'</ol>'
    body+=section('Critères de l’échelle',ladder+'<p>Les niveaux sont des catégories de maturité ; les additionner ne donne ni pourcentage de RH ni probabilité de preuve.</p>',id='echelle')
    # Keep every original crossing and its source, rather than silently dropping this tool.
    crossings=[]
    for x in ind.get('croisements',[]):
        title=x.get('nom',x.get('titre',x['id']))
        crossings.append(f'<tr data-search-row><th>{esc(title)}</th><td>{esc(x.get("enonce",x.get("question","")))}<p class="foot">Cadre : {esc(x.get("lieu",""))}</p><p class="foot">Pendant du modèle réduit : {esc(x.get("pendant_modele_reduit") or "Non renseigné : une zone d’ombre à conserver.")}</p></td><td>{esc(x.get("niveau",""))}</td><td>'+evidence(['1_Presentation/'+x['document']] if x.get('document') else [],prefix)+'</td></tr>')
    body+=section('Croisements conservés et reliés','<p>Les croisements restent des instruments de recherche. Leur niveau déclaré n’a pas été augmenté dans cette révision ; les ponts vers les obligations courantes sont visibles dans le graphe.</p><details><summary>Les '+str(len(crossings))+' croisements du registre initial</summary><div class="tablewrap"><table><thead><tr><th>Croisement</th><th>Énoncé</th><th>Niveau</th><th>Pièce</th></tr></thead><tbody>'+''.join(crossings)+'</tbody></table></div></details>',id='croisements')
    return body

STATUTS_FICHE={'ouverte':'ouverte','assignee':'assignée','a_reprendre':'à reprendre','deposee':'déposée','verifiee':'vérifiée',
               'acceptee':'acceptée','integree':'intégrée','rejetee':'rejetée','abandonnee':'abandonnée','perimee':'périmée'}
def render_targeting(s,prefix):
    t=s['targeting'];scalar=t['scalar']
    local='Aucune nouvelle subdivision requise dans la fenêtre déjà certifiée.' if scalar['closed_in_declared_window'] else scalar['reason']
    text='<p><strong>Demandes de calcul :</strong> '+esc(local)+'</p>'
    for action in t['calculation_requests']:text+='<p>'+esc(action['type']+' : '+action['reason'])+'</p>'
    text+='<div id="ciblage-bellman-live"><p><strong>Étude du modèle Bellman à ses réglages initiaux :</strong> '+esc(' ; '.join(x['label'] for x in t['bellman']['choices']))+'.</p></div>'
    text+='<p class="foot">Une étude retenue par Bellman n’est pas un programme lancé : il faut d’abord lui lier une instance, des entrées et une commande bornée. Les investigations sans raccord restent hors modèle ; aucune probabilité ni coût n’est inventé.</p>'
    text+='<p><strong>Prochain résultat théorique :</strong> '+esc(t['next_theoretical_result'])+'</p><div class="taskgrid">'
    for a in t['theoretical_front']:
        text+='<article class="task"><h3>'+esc(a['label'])+'</h3><p>'+esc(a['question'])+'</p><p class="foot">Critère de rejet : '+esc(a['refutation'])+'</p><p class="links">'+' · '.join(node_link(k) for k in a['nodes'])+' · '+evidence([a['source']],prefix)+'</p></article>'
    text+='</div><details><summary>Gardes, provenance et dépendances</summary><ul>'
    for a in t['investigations']:
        if a['missing_prerequisites']:text+='<li>'+esc(a['label']+' : attend '+' ET '.join(a['missing_prerequisites'])+' (une issue positive déclarée avec sa portée)')+'</li>'
    for key,audit in t['dependency_audits'].items():text+='<li>'+esc(key+' : '+('dépendances lues identiques au registre des empreintes revues' if audit['unchanged'] else 'à revérifier'))+'</li>'
    text+='</ul><p>'+esc(t['provenance_note'])+'</p><p>Une borne suffisante négative reste une indécision. Une sous-tâche exécutée ne ferme pas son obligation. Une investigation close par réfutation ne satisfait pas un prérequis. Aucun niveau ni fait de preuve n’est modifié.</p></details>'
    rows=''.join('<tr data-search-row><th>'+esc(f['id'])+'</th><td>'+esc(f['titre'])+'<p class="foot">'+esc(f['genre']+' · rôle '+f['role']+' · cycle '+str(f['cycle']))+'</p></td><td>'+esc(STATUTS_FICHE.get(f['statut'],f['statut']))+'</td><td>'+esc(f['assigne_a'] or '—')+'</td></tr>' for f in s['taches'])
    text+='<h3>Fiches de tâche (instantané de construction)</h3><p>Le travail est réparti par fiches : un acteur (auteur, IA ou agent) produit dans la zone de dépôt, un autre vérifie, l’auteur décide. État vivant : <code>python -B 2_Methode/Pilotage/taches.py etat</code>.</p>'
    text+=('<div class="tablewrap"><table><thead><tr><th>Fiche</th><th>Tâche</th><th>Statut</th><th>Assignée à</th></tr></thead><tbody>'+rows+'</tbody></table></div>') if rows else '<p>Aucune fiche ouverte.</p>'
    text+='<p class="links">'+evidence(['2_Methode/Pilotage/CIBLAGE.md','1_Presentation/82_CIBLAGE_ET_REPARTITION.pdf','3_Preuves_et_calculs/data/ciblage_courant.json','2_Methode/Pilotage/ciblage.py','2_Methode/Pilotage/taches.py'],prefix)+'</p>'
    return section('Ciblage : que faire maintenant, et qui le fait',text,id='ciblage')

def navigator(s,prefix):
    body=render_targeting(s,prefix)
    body+=section('Position et destination',visuals.render_navigation_chart(s,prefix),id='position')
    body+=section('Choisir des investigations qui répondent au verrou',
        '<p>La loi de signe et la couverture restent au centre. Les anciens résultats ne sont pas rejoués comme nouveaux projets : les tâches achevées sont clôturées dans leur périmètre, les résultats partiels gardent leur reste ouvert et les doublons pointent vers une même investigation.</p>'+gate_table(s,prefix),id='obligations')
    model=s['bellman']
    controls='<div class="controls"><label>Budget en lots H <input id="budget" type="number" min="0" max="12" value="6"></label></div><div id="weights" class="weights"></div>'
    controls+='<div class="decision" id="bellman-result" aria-live="polite"></div><details><summary>Durées conventionnelles des études</summary><div id="costs" class="costgrid"></div></details>'
    controls+='<p class="foot">Réglages du modèle conservé dans le document67 : facteurs de préférence, intervalles de durée, issues et STOP. Aucun de ces nombres ne mesure une probabilité de preuve.</p>'
    math='<math display="block"><mrow><msub><mi>V</mi><mo>−</mo></msub><mo>(</mo><mi>K</mi><mo>,</mo><mi>D</mi><mo>,</mo><mi>b</mi><mo>)</mo><mo>=</mo><mo>max</mo><mo>{</mo><mi>U</mi><mo>(</mo><mi>K</mi><mo>)</mo><mo>,</mo><munder><mo>max</mo><mi>a</mi></munder><munder><mo>min</mo><mi>o</mi></munder><msub><mi>V</mi><mo>−</mo></msub><mo>(</mo><mi>K</mi><mo>∪</mo><msub><mi>F</mi><mi>o</mi></msub><mo>,</mo><mi>D</mi><mo>∪</mo><mo>{</mo><mi>a</mi><mo>}</mo><mo>,</mo><mi>b</mi><mo>−</mo><msubsup><mi>c</mi><mi>a</mi><mo>+</mo></msubsup><mo>)</mo><mo>}</mo></mrow></math>'
    body+=section('Bellman : contrats complémentaires et issues',controls+'<div class="math-scroll">'+math+'</div>'+
        '<p>K contient les faits attestés, D les études bornées exécutées, b le budget restant. Une capacité exige tous les faits de son contrat. L’enveloppe basse prend la durée haute et l’issue la moins favorable ; l’enveloppe haute prend la durée basse et l’issue la plus favorable. Le plan ultérieur dépend de l’issue observée.</p>',id='bellman')
    facts=s['bellman_state']
    reconciliation='<p>'+esc(facts['scope'])+'</p><ul>'+''.join('<li><strong>'+esc(x['study'])+'</strong> : '+esc(x['scope'])+' '+evidence([x['source']]+x.get('also',[]),prefix)+'</li>' for x in facts['evidence'])+'</ul><p>'+esc(facts['restriction'])+'</p>'
    reconciliation+='<p>Ces clôtures d’études bornées ne ferment pas les questions globales des bilans. Aucun invariant candidat ni certificat à A fixé n’est crédité.</p>'
    body+=section('État attesté et rapprochement des bilans',reconciliation,id='etat-bellman')
    contract_rows=[]
    for a in model['actions']:
        req=' OU '.join(' ET '.join(x) or 'Aucun' for x in a['requires_any'])
        outcomes=' ; '.join(o['id']+' → '+', '.join(o['adds']) for o in a['outcomes'])
        current='Étude bornée examinée, obligation globale conservée' if a['id'] in facts['completed'] else 'Ouvert sous ses prérequis'
        contract_rows.append(f'<tr id="contrat-{a["id"]}"><th>{esc(a["label"])}</th><td>{esc(current)}<br>{a["duration"][0]}–{a["duration"][1]} H</td><td>{esc(req)}</td><td>{esc(outcomes)}<p class="links">'+' · '.join(node_link(k) for k in a['nodes'])+'</p></td></tr>')
    body+=section('Contrats conservés du document67','<details><summary>Études, prérequis et issues</summary><div class="tablewrap"><table><thead><tr><th>Étude</th><th>État et durée</th><th>Contrat</th><th>Issues possibles et idées</th></tr></thead><tbody>'+''.join(contract_rows)+'</tbody></table></div></details>',id='contrats')
    investigations=s['investigations']
    tasks=[]
    for a in investigations:
        req=', '.join(next(x['label'] for x in investigations if x['id']==k) for k in a['requires']) or 'Aucun livrable nouveau requis'
        dimensions=', '.join(next(d['nom'] for d in s['indicator']['dimensions'] if d['id']==k) for k in a['dimensions'])
        task_status="Récupération documentaire réalisée" if a.get("status")=="cloture_documentaire" else "Question ouverte dans le protocole"
        tasks.append(f'<article class="task" id="action-{a["id"]}"><div class="eyebrow">{task_status}</div><h3>{esc(a["label"])}</h3><p>{esc(a["question"])}</p><p class="foot">Questions de l’indicateur visées : {esc(dimensions)}. Aucun gain de niveau pré-attribué.</p><dl><dt>Livrable recevable</dt><dd>{esc(a["output"])}</dd><dt>Témoin contraire</dt><dd>{esc(a["witness"])}</dd><dt>Critère de rejet</dt><dd>{esc(a["refutation"])}</dd><dt>Prérequis</dt><dd>{esc(req)}</dd></dl><p class="links">'+ ' · '.join(node_link(k) for k in a['nodes'])+' · '+evidence([a['source']],prefix)+'</p></article>')
    body+=section('Questions courantes et protocoles associés', f'<p>Ces {len(tasks)} fiches gardent leurs témoins et critères de rejet. La récupération des27sources est réalisée ; les questions scientifiques restent ouvertes et ne reçoivent aucun score ajouté au modèle du document67.</p><div class="taskgrid">'+''.join(tasks)+'</div>',id='protocoles')
    ledger=[]
    ind=s['indicator']; stages=ind['etapes']; index={e['versions']:i for i,e in enumerate(stages)}
    for c in s['actions']:
        e=c['evaluation_courante']; pv=c.get('prevision'); i=index.get(c.get('version'))
        delta={k:stages[i]['niveaux'][k]-stages[i-1]['niveaux'][k] for k in stages[i]['niveaux'] if i and stages[i]['niveaux'][k]!=stages[i-1]['niveaux'][k]} if i is not None else None
        forecast=('Prévision absente' if pv is None else 'Prévision enregistrée : '+json.dumps(pv.get('gains',{}),ensure_ascii=False)+' ; p='+str(pv.get('probabilite','non renseignée')))
        current=(('Variation d’étape : '+(str(delta) if delta else 'aucun niveau')) if delta is not None else 'Pas de variation d’étape attribuable')
        group=next((a for a in investigations if a['id']==e['groupe']),None)
        use=anchor('1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html#action-'+group['id'],group['label'],prefix) if group else ('Rapport externe requis' if e['groupe']=='relecture' else 'Brique acquise' if c['statut']=='fait' else 'Piste secondaire ouverte')
        ledger.append(f'<tr data-search-row><th>{esc(c["titre"])}<small>{esc(c["id"])}</small></th><td><span class="badge">{esc(c["statut"])}</span><small>{esc(c.get("version") or "Non réalisé")}</small></td><td>{esc(e["raison"])}<p>{esc(c.get("appris") or "")}</p><p class="links">{evidence([e["source"]],prefix)}</p></td><td>{use}<details><summary>Prévu / constaté</summary><p>{esc(forecast)}</p><p>{esc(current)}. La variation appartient à toute l’étape ; ce n’est pas un effet causal mesuré de ce seul coup.</p><p>{esc(c.get("refutation_tenue") or "Pas de verdict de réfutation enregistré.")}</p></details></td></tr>')
    counts=Counter(c['statut'] for c in s['actions'])
    body+=section('Toutes les actions restent évaluables','<p>'+esc(' · '.join(f'{v} {k}' for k,v in counts.items()))+'. Les '+str(len(s['actions']))+' bilans sont conservés et rapprochés de leurs pièces ; 13 dates ou statuts ont reçu une correction ciblée. Les autres bilans n’ont pas été redémontrés ni tous réévalués individuellement.</p><label class="search">Chercher dans les '+str(len(s['actions']))+' actions <input data-search="ledger" type="search" placeholder="Möbius, sources, V13, queue…"></label><details><summary>Ouvrir le registre complet des '+str(len(s['actions']))+' actions</summary><div class="tablewrap"><table id="ledger"><thead><tr><th>Question d’origine</th><th>Statut courant</th><th>Évaluation et acquis réutilisable</th><th>Usage actuel et prévision</th></tr></thead><tbody>'+''.join(ledger)+'</tbody></table></div></details>',id='registre')
    body+=section('Continuité des modèles et de leurs domaines',
        '<p>Le moteur ci-dessus reprend les contrats complémentaires et les issues du document67. Le modèle à union de tokens du document62 reste consultable dans son périmètre. Le calcul de dette de Schur est un objet mathématique distinct du choix documentaire des études.</p><p class="links">'+evidence(['1_Presentation/62_ATLAS_DES_DECISIONS_BELLMAN.html','1_Presentation/67_GRAPHE_DES_PONTS.html','1_Presentation/44_MATRICE_DES_THEORIES.html'],prefix)+'</p>',id='modeles')
    return body

def map_svg(s):
    # Topology is exact; dashed edges denote an obligation rather than an implication.
    positions={'identity':(250,40),'fluctuation':(20,150),'J':(480,150),'schur':(20,260),'coverage':(250,260),
               'J_bound':(480,370),'global_sign':(20,370),'weil_all':(250,480),'RH':(250,590)}
    titles={'identity':['Poids arithmétiques','Identité exacte de Λ'], 'fluctuation':['Fluctuation signée','Acquise ; signe à contrôler'],
            'J':['Énergie positive J','Croissance à contrôler'],'schur':['Couplages / Schur','Dette générale ouverte'],
            'coverage':['Famille couvrante','Domaine et limite requis'],'J_bound':['J(X) = O(X²)','Borne globale ouverte'],
            'global_sign':['Loi de signe','Ouverte sur la famille'],'weil_all':['Weil sur tous les tests','Signe ET couverture'],'RH':['RH','Non démontrée']}
    links=[('identity','fluctuation',False),('identity','J',False),('fluctuation','schur',False),('schur','global_sign',True),
           ('J','J_bound',True),('global_sign','weil_all',True),('coverage','weil_all',True),('weil_all','RH',False),('J_bound','RH',False)]
    out=['<svg class="logicmap" viewBox="0 0 720 680" role="img" aria-labelledby="logic-title"><title id="logic-title">Deux portes vers RH : signe et couverture de Weil ; borne globale de l’énergie J</title><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="#5b6d7c"/></marker></defs>']
    for a,b,dashed in links:
        x,y=positions[a];xx,yy=positions[b]
        path=(f'M{x+100},{y+64} C680,450 680,622 450,622' if a=='J_bound' else f'M{x+100},{y+64} C{x+100},{y+94} {xx+100},{yy-25} {xx+100},{yy}')
        out.append(f'<path d="{path}" class="edge'+(' missing' if dashed else '')+'" marker-end="url(#arrow)"/>')
    by={n['id']:n for n in s['nodes']}
    for k,(x,y) in positions.items():
        a,b=titles[k];status=by[k]['status']
        out.append(f'<g class="mapnode {status}" data-node="{k}" role="button" tabindex="0" aria-label="{esc(a)}"><rect x="{x}" y="{y}" width="200" height="64" rx="9"/><text x="{x+100}" y="{y+26}" text-anchor="middle">{esc(a)}</text><text class="sub" x="{x+100}" y="{y+47}" text-anchor="middle">{esc(b)}</text></g>')
    out.append('</svg>');return ''.join(out)

def retained_graph(s):
    """Keep Claude's original grouping and geometry; update the node content in place."""
    layout=(HERE/'graphe_layout_claude.html').read_text()
    by={n['id']:n for n in s['nodes']}
    codes={'demontre':'core','classique':'lit','obstacle':'neg','diagnostic':'low',
           'conditionnel':'cond','mesure':'mes','outil':'act','ouvert':'cond','partiel':'cond'}
    def update(m):
        key=m[2];body=m[3]
        if key=='sources':key='sources_registre' if 'registre' in re.sub('<[^>]*>','',body).lower() else 'sources_locales'
        n=by[key]
        return f'<button class="node" data-s="{codes[n["status"]]}" data-node="{key}"><small class="stable-id">{n["uid"]}</small><strong>{esc(n["title"])}</strong><span class="current-summary">{esc(n["summary"])}</span></button>'
    layout=re.sub(r'<button([^>]*?)data-k="([^"]+)"[^>]*>(.*?)</button>',update,layout,flags=re.S)
    return '<div class="retained-graph" id="graphe-origine">'+layout+'</div>'


def graph(s,prefix):
    body=section('Cartes 2D des cibles actuelles',advanced.render(s,prefix),id='vers-rh')
    body+=retained_graph(s)
    body+=section('L’amplification : une étape distincte',
        '<div class="flowcards">'+''.join('<div class="flowcard">'+node_link(k,next(n['title'] for n in s['nodes'] if n['id']==k))+'</div>' for k in ['copies','head','large_q','threequarters'])+'</div><p>La restitution et la tête sont acquises. La grande queue manque. Même obtenue avec l’exposant visé, cette estimation donnerait seulement la région Re(s) &gt; 3/4 : un gain supplémentaire serait nécessaire pour RH.</p>',id='amplification')
    families=sorted({n['family'] for n in s['nodes']})
    filters='<div class="controls"><label>Famille <select id="graph-family"><option value="">Toutes</option>'+''.join(f'<option>{esc(f)}</option>' for f in families)+'</select></label><label>Statut <select id="graph-status"><option value="">Tous</option>'+''.join(f'<option value="{k}">{v}</option>' for k,v in STATUS.items())+'</select></label><label>Recherche <input id="graph-search" type="search" placeholder="Kalman, jets, Weil, Möbius…"></label></div><p id="graph-count" class="foot"></p>'
    cards=[]
    for n in s['nodes']:
        cards.append(f'<button class="idea {n["status"]}" data-node="{n["id"]}" data-family="{esc(n["family"])}" data-status="{n["status"]}" data-idea-card><span class="eyebrow">{esc(n["uid"])} · {esc(n["family"])}</span><strong>{esc(n["title"])}</strong><span class="badge">{STATUS[n["status"]]}</span><span>{esc(n["summary"])}</span></button>')
    body+=section('Carte complète : origines, réemplois et obligations',filters+'<div class="ideagrid">'+''.join(cards)+'</div>',id='carte-complete',lead=f'{len(s["nodes"])} nœuds et {len(s["edges"])} relations typées. Les anciennes idées ont une évaluation courante et des liens explicites vers ce qu’elles peuvent encore éclairer.')
    edges=[]
    by={n['id']:n for n in s['nodes']}
    for e in s['edges']:
        req=' ; ET : '+', '.join(by[k]['title'] for k in e.get('requires',[])) if e.get('requires') else ''
        edges.append(f'<tr data-search-row><td>{node_link(e["source"],by[e["source"]]["title"])}</td><td>{esc(e["kind"])}</td><td>{node_link(e["target"],by[e["target"]]["title"])}</td><td>{esc(e["label"]+req)}</td></tr>')
    body+=section('Contrats des relations','<p>Une relation d’usage, une analogie et une obligation ne sont pas des implications. Une flèche conditionnelle exige tous les termes de sa garde.</p><details><summary>Consulter les '+str(len(s['edges']))+' relations et leurs gardes</summary><div class="tablewrap"><table><thead><tr><th>Origine</th><th>Nature</th><th>Destination</th><th>Contrat</th></tr></thead><tbody>'+''.join(edges)+'</tbody></table></div></details>',id='relations')
    route_rows=[]
    for r in s['routes']:
        route_rows.append('<tr data-search-row><th>'+esc(r.get('system',r['id']))+'</th><td>'+esc(r.get('properties',''))+'</td><td>'+esc(r.get('limitations_and_bifurcations',''))+'<p class="links">'+' · '.join(node_link(k,by[k]['title']) for k in r['nodes'])+'</p><p class="links">'+evidence(r.get('sources',[]),prefix)+'</p></td></tr>')
    body+=section('Chemins parcourus et réemplois actuels','<p>Chaque parcours est relié aux nœuds actuels. Une fermeture de méthode garde son périmètre ; elle ne devient pas une impossibilité générale.</p><label class="search">Retrouver une trajectoire <input type="search" data-search="routes" placeholder="Frobenius, Bellman, corrélations…"></label><details><summary>Parcours, propriétés et bifurcations</summary><div class="tablewrap"><table id="routes"><thead><tr><th>Parcours ou outil</th><th>Propriété retenue</th><th>Limite, bifurcation et usage actuel</th></tr></thead><tbody>'+''.join(route_rows)+'</tbody></table></div></details>',id='chemins')
    body+=section('Une identité par idée, plusieurs vues possibles',
        '<p>Les '+str(len(s['graph_cases']))+' cases des cartes détaillées renvoient aux idées stables et à leurs dossiers. Les libellés locaux I1, T2, L4 ou B5 restent ceux de leurs documents ; ils ne sont pas confondus avec les identifiants IDE-xxx.</p><p>'+evidence(['2_Methode/Pilotage/REGISTRE_DES_IDENTIFIANTS.md'],prefix)+'</p>',id='identifiants')
    return body

def render(s,key):
    page=next(p for p in s['primary_pages'] if p['id']==key)
    prefix='../'*(len(Path(page['path']).parts)-1)
    title={'portail':'Portail du Programme Riemann','indicateur':'Les étapes franchies, version par version',
           'navigateur':'La démonstration comme itinéraire','carte':'Programme Riemann : carte des idées'}[key]
    intro={'portail':'Le portail présente l’état commun. Les indicateurs l’évaluent, le navigateur choisit les investigations et le graphe montre leurs dépendances.',
           'indicateur':'Chaque niveau est justifié par des pièces et un critère de progression. Les acquis locaux, les obligations globales et la relecture restent distincts.',
           'navigateur':'Le Bellman à contrats du document67 reprend les faits attestés depuis ses bilans ; les questions récentes gardent leurs témoins et leurs gardes. Les coûts et les préférences restent conventionnels.',
           'carte':'Les idées gardent leur place et leur portée actuelle. Les voies fermées ont une raison précise ; les réouvertures indiquent ce qui a changé.'}[key]
    css=(HERE/'style.css').read_text()+(HERE/('style_graphe_claude.css' if key=='carte' else 'style_claude.css')).read_text()+(HERE/'style_adapter.css').read_text()
    js=(HERE/'bellman_contracts.js').read_text()+'\n'+(HERE/'ui.js').read_text()
    # Full common data is embedded, so each view works offline without fetch or a server.
    payload=json.dumps(dict(**{k:v for k,v in s.items() if k!='catalogue'},prefix=prefix,page=key,status_labels=STATUS),ensure_ascii=False).replace('</','<\\/')
    body={'portail':portal,'indicateur':indicator,'navigateur':navigator,'carte':graph}[key](s,prefix)
    if key in ('portail','carte'):
        paths=[('65_GRAPHE_DES_PASSAGES.html','65 · Passages'),('66_GRAPHE_DES_CERTIFICATS.html','66 · Certificats'),('67_GRAPHE_DES_PONTS.html','67 · Ponts et Bellman'),('69_LANGUE_DES_PASSAGES.html','69 · Domaines'),('71_LEGO_REUTILISABLE.html','71 · Lego'),('72_CONCENTRATION_PROJETEE.html','72 · Concentration'),('73_OPERATEUR_COMMUN.html','73 · Opérateur commun')]
        body='<p class="links" aria-label="Cartes détaillées existantes"><strong>Cartes détaillées existantes :</strong> '+' · '.join('<a href="'+prefix+'1_Presentation/'+path+'">'+label+'</a>' for path,label in paths)+'</p>'+body
    dialog='<dialog id="node-dialog"><div class="dialoghead"><span id="node-status" class="badge"></span><button id="close-dialog" aria-label="Fermer la fiche">Fermer ×</button></div><h2 id="node-title"></h2><div id="node-body"></div></dialog>'
    return '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(page['label'])+' — Programme Riemann '+esc(s['version'])+'</title><meta name="research-snapshot" content="'+s['fingerprint']+'"><style>'+css+'</style></head><body data-tool="'+key+'"><div class="wrap">'+nav_html(s,key,prefix)+f'<header class="head"><div class="eyebrow">Programme Riemann · {esc(s["version"])} · continuité des outils</div><h1>{esc(title)}</h1><p class="lede">{intro}</p><p class="scope">RH : ouverte · Signe global : ouvert · Couverture avec signe : ouverte</p></header>'+body+f'<footer><p>{esc(s["review_scope"])}</p><p class="links"><a href="{prefix}README.md">README : à lire d’abord</a> · <a href="{prefix}PLAN_DU_CORPUS.md">Plan du corpus</a> · <a href="{prefix}HISTORIQUE_DES_LIVRAISONS.md">Historique des livraisons</a></p><p>État partagé : <code>{s["fingerprint"][:16]}</code> · Vincent P. P. NOËL</p></footer></div>'+dialog+'<script type="application/json" id="steering-data">'+payload+'</script><script>'+js+'</script></body></html>\n'

def instantane_taches():
    src=ROOT/'2_Methode/Pilotage/taches.json'
    if src.exists():
        reg=json.loads(src.read_text(encoding='utf-8-sig'))
        dump(ROOT/'2_Methode/Pilotage/taches_instantane.json',dict(schema='taches_instantane_v1',source='taches.json',taches=reg['taches']))

def build_all():
    instantane_taches()
    load_component('reconstruction_integree').build()
    s=load_state()
    advanced.export_svgs(s)
    for p in s['primary_pages']:(ROOT/p['path']).write_text(render(s,p['id']),encoding='utf-8')
    dump(DATA/'pilotage_courant.json',s)
    dump(DATA/'ciblage_courant.json',s['targeting'])
    dump(ROOT/catalogue.INDEX,dict(**s['catalogue'],kinds=catalogue.KINDS))
    dump(DATA/'v655_etat_recherche.json',s['research'])
    dump(DATA/'v655_carte_bellman.json',dict(**s['bellman'],type='Contract-scenario Bellman from document67, with reconciled bounded-study state',current_state=s['bellman_state'],probabilities_assigned=False,RH_proved=False,decisions=s['decisions']))
    dump(DATA/'v655_evaluations_outils.json',dict(version=s['version'],revision=s['revision'],date=s['date'],fingerprint=s['fingerprint'],dimensions=s['reviews'],actions=[dict(id=c['id'],**c['evaluation_courante']) for c in s['actions']],
        nodes=[{k:n[k] for k in ['id','status','review','reviewed_on','evidence']} for n in s['nodes']]))
    print(json.dumps(dict(primary_pages=4,dimensions=7,actions=len(s['actions']),nodes=len(s['nodes']),edges=len(s['edges']),bellman_cases=len(s['decisions']),fingerprint=s['fingerprint']),ensure_ascii=False))
    return s

if __name__=='__main__':build_all()
