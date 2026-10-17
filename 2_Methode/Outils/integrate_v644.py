"""Integrate the executed language/domain research without changing historical science."""
from pathlib import Path
import sys,json,hashlib,subprocess,re,importlib.util
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'1_Presentation';D=ROOT/'3_Preuves_et_calculs/data'
S68='68_ARITHMETIQUE_DES_PASSAGES_ET_QUEUE_EFFECTIVE';S69='69_DICTIONNAIRE_PROGRESSIF_DES_DOMAINES'
STATUS='P et métrique exacte, famille dense, no-go de marge H¹, représentation I−compact, queue effective et arithmétique graduée des jets démontrés. 16 compressions arithmétiques positives numériquement ; signe du Schur pour tous supports ouvert.'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def module(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
def patch(p,a,b):
    t=p.read_text(encoding='utf-8-sig')
    if a in t:p.write_text(t.replace(a,b),encoding='utf-8-sig' if p.suffix=='.md' else 'utf-8')
def main():
    state=dict(version='V6.44',result=STATUS,document=S68+'.pdf',dictionary=S69+'.pdf',graph='69_LANGUE_DES_PASSAGES.html',
      completed_bellman_actions=read(D/'v643_etat_recherche.json')['completed_bellman_actions'],
      current_bellman_model='v643_modele_ponts.json',current_grammar='v644_grammaire.json',
      next_actions=['v644_queue_serree','v644_schur_effectif','v644_loi_tous_supports'],maturity_levels_unchanged=True,
      open=['certified Riesz/projection solver','effective Schur sign for each S','cover every S','historical branch/collision/complex-A questions'],
      novelty_scope='internal reconstruction; no bibliographic priority claim; no RH proof')
    write(D/'v644_etat_recherche.json',state)
    navp=ROOT/'2_Methode/Navigateur/carte_navigation.json';nav=read(navp)
    nodes=[('v644_langue_domaines','Construire la langue et la queue effective','fait','L1–L8 et tableaux exécutés',STATUS,4),
      ('v644_queue_serree','Resserrer et certifier le contrat de queue','ouvert','Comment réduire la tête astronomique avec une borne validée de r(T), ε et L_S ?','Le corollaire entier fournit une queue prouvée ; chercher un budget utilisable.',3),
      ('v644_schur_effectif','Calculer le Schur effectif avec solveurs certifiés','ouvert','Comment encadrer Riesz, projection, couplages et inverse de queue sans omettre la métrique ?','Conserver les résidus et le reste Neumann ; vérifier un support avant une loi couvrante.',4),
      ('v644_loi_tous_supports','Trouver une loi arithmétique couvrant tous les supports','ouvert','Quelle identité ou borne contrôle le signe du Schur complet pour tous S ?','Interaction premiers/archimédien ; aucun signe global acquis.',5)]
    for id,title,status,question,thesis,cost in nodes:
        if any(x['id']==id for x in nav['coups']):continue
        c=dict(id=id,titre=title,statut=status,type='construction',question=question,these=thesis,cout=cost,version='V6.44',
          temoin='Document 68 : L1–L8, protocole, matrices et contrat de queue.',document=S68+'.pdf',gains={},probabilite=0.5,
          probabilite_scope='Convention historique du navigateur, non une probabilité de RH ; grammaire sans score probabiliste.',
          prerequis=[],debloque=[],operateurs=[],croise=['RH'],repond_a=[],refutation='Garde invalide, borne non contrôlée ou témoin négatif certifié ; échec de calcul reste indéterminé.',
          prevision=dict(gains={},probabilite=0.5,cout=cost,refutation='Nommer la borne manquante ; aucun plafond fini promu en signe global.'))
        if status=='fait':c['appris']=STATUS
        nav['coups'].append(c)
    nav['bilan_v644']=dict(document=S68+'.pdf',dictionnaire=S69+'.pdf',graphe=state['graph'],resultat=STATUS)
    write(navp,nav)
    indp=ROOT/'2_Methode/Indicateur/indicateur_avancement.json';ind=read(indp)
    if not any(x['id']=='v644' for x in ind['etapes']):
        ind['etapes'].append(dict(id='v644',court='V6.44',versions='V6.44',jour='12 oct.',franchi=STATUS,
          pourquoi=dict(comprendre='Structure logarithmique, queue explicite et arithmétique de jets reliées.',case='Les niveaux globaux restent inchangés : le Schur tous supports demeure ouvert.'),
          niveaux=dict(ind['etapes'][-1]['niveaux']),documents=[['Arithmétique et preuves',S68+'.pdf'],['Dictionnaire progressif',S69+'.pdf'],['Langue interactive',state['graph']]]))
    write(indp,ind)
    sp=ROOT/'2_Methode/Sources/sources.json';sources=read(sp)
    for s in sources:
        if s['cle'] in ('Beu55','CC21','Wei48'):
            for number in ('68','69'):
                if number not in s.setdefault('docs',[]):s['docs'].append(number)
    write(sp,sources)
    matp=ROOT/'2_Methode/Matrice/matrice_theories.json';mat=read(matp);mat['version']='V6.44'
    for n in mat['noeuds']:
        if n['id']=='WEIL':
            note=' V6.44 : R externe logarithmique, I−compact, queue de moments effective et réduction Schur finie démontrées ; signe tous supports ouvert.'
            if note.strip() not in n.get('apport_note',''):n['apport_note']=n.get('apport_note','')+note
            for doc in ('68','69'):
                if doc not in n.setdefault('docs',[]):n['docs'].append(doc)
    write(matp,mat)
    bip=ROOT/'2_Methode/Indicateur/build_indicateur.py';patch(bip,'("graphe", "Ponts et preuves", "1_Presentation/67_GRAPHE_DES_PONTS.html")','("graphe", "Langue et preuves", "1_Presentation/69_LANGUE_DES_PASSAGES.html")')
    port=ROOT/'2_Methode/Portail/build_portail.py'
    patch(port,"current_path = ROOT / '3_Preuves_et_calculs/data/v643_etat_recherche.json'","current_path = ROOT / '3_Preuves_et_calculs/data/v644_etat_recherche.json'\n    if not current_path.exists():current_path=ROOT/'3_Preuves_et_calculs/data/v643_etat_recherche.json'")
    patch(port,'Les 67 documents ; pilote courant de contrats V6.43, modèle documentaire V6.42 conservé pour comparaison.','Les 69 documents ; langue et domaines V6.44, contrats V6.43, modèle documentaire V6.42 conservé.')
    t=port.read_text()
    # Deduplicate two repeated historical cards inherited from V643.
    lines=t.splitlines();seen=set();kept=[]
    for line in lines:
        if ('("Construire des ponts avec Bellman",' in line or '("Ponts et contrats",' in line):
            if line in seen:continue
            seen.add(line)
        kept.append(line)
    t='\n'.join(kept)+'\n'
    if '("La langue des passages",' not in t:
        t=t.replace('        ("Construire des ponts avec Bellman",','        ("La langue des passages", "1_Presentation/69_LANGUE_DES_PASSAGES.html", "Dictionnaire progressif, arithmétique des jets et atelier de traduction typée."),\n        ("Arithmétique et queue effective", "1_Presentation/'+S68+'.pdf", "Document 68 : huit preuves auxiliaires, I−compact et réduction Schur avec budget."),\n        ("Dictionnaire des domaines", "1_Presentation/'+S69+'.pdf", "Document 69 : objets, fonctions, opérateurs, images et gardes."),\n        ("Construire des ponts avec Bellman",',1)
    port.write_text(t)
    np=ROOT/'2_Methode/Navigateur/build_navigateur.py'
    patch(np,"    if carte.get('bilan_v643'):","    if carte.get('bilan_v644'):\n        phase='<section class=\"sheet\"><h2>V6.44 : langue des domaines et queue effective</h2><p>'+carte['bilan_v644']['resultat']+'</p><p><a href=\"69_LANGUE_DES_PASSAGES.html\">Dictionnaire et atelier</a> · <a href=\"'+carte['bilan_v644']['document']+'\">Preuves et calculs</a></p></section>'\n    elif carte.get('bilan_v643'):")
    ap=ROOT/'2_Methode/Outils/build_v638_atlas.py'
    patch(ap,"    if registry.get('version')=='V6.43':","    if registry.get('version')=='V6.44':\n        body=body.replace('<header>','<section><h2>V6.44 : langue des passages</h2><p><a href=\"69_LANGUE_DES_PASSAGES.html\">Dictionnaire et grammaire</a> · <a href=\"68_ARITHMETIQUE_DES_PASSAGES_ET_QUEUE_EFFECTIVE.pdf\">Huit preuves et expériences</a>. Queue positive effective à support fixé ; signe de Schur tous supports encore ouvert. <a href=\"67_GRAPHE_DES_PONTS.html\">Pilote de contrats V6.43</a>.</p></section><header>',1)\n        body=body.replace('Comparer les suites de travaux','Modèle documentaire de référence V6.42')\n        body=body.replace('data/v642_decisions.json','data/v644_decisions.json')\n    elif registry.get('version')=='V6.43':")
    vp=ROOT/'VERSION.txt';old=vp.read_text(encoding='utf-8-sig')
    if not old.startswith('Programme Riemann — V6.44'):vp.write_text('Programme Riemann — V6.44\nDate: 2026-10-12\n'+STATUS+'\n\nHistorique conservé :\n'+old,encoding='utf-8-sig')
    patch(ROOT/'CITATION.cff','version 6.43','version 6.44');patch(ROOT/'CITATION.cff','version: "6.43"','version: "6.44"')
    rp=ROOT/'README.md';t=rp.read_text(encoding='utf-8-sig').replace('version 6.43','version 6.44',1)
    section='## V6.44 - La langue des passages (documents 68 et 69)\n\n'+STATUS+'\n\nOuvrir `1_Presentation/69_LANGUE_DES_PASSAGES.html` pour le dictionnaire et le jeu de contrats ; document 68 pour L1–L8, calculs et obligations. Le corollaire entier certifie une queue très grossière ; aucune tête effective immense n’a été calculée. Tous les 95 noms du registre sont inclus ; les fonctions Python sont indexées séparément.\n\n'
    if '## V6.44 -' not in t:t=section+t
    rp.write_text(t,encoding='utf-8-sig')
    bi=module('ind644',bip);cp=ROOT/'00_Carte_des_idees.html';t=cp.read_text(encoding='utf-8-sig').replace('Version 6.43.','Version 6.44.').replace('programme Riemann V6.43','programme Riemann V6.44')
    if 'V6.44 : langue et domaines' not in t:t=t.replace('<footer>','<section class="panel"><h2>V6.44 : langue et domaines</h2><p>'+STATUS+'</p><p><a href="1_Presentation/69_LANGUE_DES_PASSAGES.html">Dictionnaire, arithmétique et jeu</a> · <a href="1_Presentation/'+S68+'.pdf">Démonstrations</a></p></section><footer>',1)
    t=re.sub(r'<nav class=[\'\"]topnav[\'\"].*?</nav>',bi.topnav('carte',''),t,count=1,flags=re.S);cp.write_text(t,encoding='utf-8-sig')
    for rel in ('2_Methode/Sources/build_sources.py','2_Methode/Matrice/build_matrice.py','2_Methode/Indicateur/build_indicateur.py','2_Methode/Navigateur/build_navigateur.py','2_Methode/Figures/build_figures.py','2_Methode/Portail/build_portail.py'):
        subprocess.run([sys.executable,str(ROOT/rel)],check=True,stdout=subprocess.DEVNULL)
    for number,stem in [(65,'PASSAGES'),(66,'CERTIFICATS'),(67,'PONTS')]:
        p=P/(str(number)+'_GRAPHE_DES_'+stem+'.html');t=p.read_text(encoding='utf-8-sig');t=re.sub(r'<nav class=[\'\"]topnav[\'\"].*?</nav>',bi.topnav('graphe','../'),t,count=1,flags=re.S)
        if 'Langue V6.44' not in t:t=t.replace('<main>','<main><p><a href="69_LANGUE_DES_PASSAGES.html">Langue V6.44 : dictionnaire, arithmétique et domaine logarithmique</a></p>',1)
        p.write_text(t)
    for p in ROOT.rglob('*.md'):
        if 'recus' not in p.parts and not p.read_bytes().startswith(b'\xef\xbb\xbf'):p.write_bytes(b'\xef\xbb\xbf'+p.read_bytes())
    registry=read(D/'v643_decisions.json');registry.update(version='V6.44',coverage=dict(presentation_documents=69,numbers=list(range(1,70))),corpus_base='V6.44, preuves historiques et leurs données conservées')
    for num,stem,title,nature in [(68,S68,'Arithmétique des passages et queue effective','preuves_auxiliaires_et_calculs_exploratoires'),(69,S69,'Dictionnaire progressif des domaines','lexique_et_grammaire_typee')]:
        if not any(x['numero']==num for x in registry['documents']):registry['documents'].append(dict(numero=num,id='doc'+str(num),titre=title,etat_anterieur='Ponts H¹ et contrats V643.',question='Comment traduire domaines et invariants sans perdre les couplages ?',action='Construction, double examen, arithmétique de jets et expérience prospective.',resultat=STATUS if num==68 else 'Noyau progressif, 95 métaphores nommées et index AST technique ; grammaire testable.',statut=nature,nature=nature,consequences='Queue et reduction conditionnelle ; signe global encore ouvert.',limites='Aucune priorité bibliographique revendiquée ; diagnostics multiprécision non certifiés ; index historique de symboles non universel.',sources=[dict(path='1_Presentation/'+stem+'.md'),dict(path='3_Preuves_et_calculs/preuves/V644_LANGUE_ET_DOMAINES.md')],formats_regroupes=['1_Presentation/'+stem+ext for ext in ('.md','.pdf','.tex')]+(['1_Presentation/69_LANGUE_DES_PASSAGES.html'] if num==69 else []),correctifs_ulterieurs=[],alternatives_documentees=['H¹ : marge stricte impossible','R : queue effective, Schur ouvert'],prevision_et_apres_coup='Matrices : protocole figé avant valeurs. Pont R et corollaire développés puis explicitement prouvés, non présentés comme prévision numérique.'))
    for r in registry['documents']:
        for s in r.get('sources',[]):
            if isinstance(s,dict) and (ROOT/s['path']).exists():s['sha256']=hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()
    write(D/'v644_decisions.json',registry)
    atlas=module('atlas644',ap);(P/'62_ATLAS_DES_DECISIONS_BELLMAN.html').write_text(atlas.html_atlas(registry,read(D/'v642_modele_bellman.json'),read(D/'v642_bellman_resultats.json')))
    print('Portail, menu, sources, indicateur, navigateur, matrice et atlas synchronisés : 69 documents ; maturité globale inchangée')
if __name__=='__main__':main()
