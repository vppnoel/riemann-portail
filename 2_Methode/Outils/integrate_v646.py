"""Update active interfaces for the bounded-family Lego certificate."""
from pathlib import Path
import sys,json,hashlib,subprocess,re,importlib.util
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'1_Presentation';D=ROOT/'3_Preuves_et_calculs/data'
S71='71_LEGO_REUTILISABLE_ET_PREMIER_CERTIFICAT_COMPLET'
STATUS='Certificat complet sur tout X_S pour 0<S≤347/1000, premier2 présent : Q_W≥masse/25 et R/200. Projection commune aux sources/fréquences, couches par parité et coût de bord assemblés. Supports plus grands, sources des têtes et transport non borné restent ouverts.'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def module(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
def patch(p,a,b):
    t=p.read_text(encoding='utf-8-sig')
    if a in t:p.write_text(t.replace(a,b),encoding='utf-8-sig' if p.suffix=='.md' else 'utf-8')
def metadata():
    state=read(D/'v645_etat_recherche.json');state.update(version='V6.46',result=STATUS,document=S71+'.pdf',dictionary='69_LANGUE_DES_PASSAGES.html',graph='71_LEGO_REUTILISABLE.html',
        current_dictionary='v646_parcours_pedagogique.json',current_dictionary_archive='v646_dictionnaire.json',next_actions=['v646_operateur_conjoint','v646_tete_praticable','v646_sources_tetes','v646_transport_non_borne'],
        open=['joint energy/prime bounds for larger supports','certified actual strong sources for noncoercive heads','transport to an unbounded support family','historical branch/collision/complex-A questions'],
        local_certificate=dict(all_tests=True,maximum_support='347/1000',mass_floor='1/25',R_floor='1/200',beta='3/20',nonempty_prime_term=True),global_sign_certified=False,maturity_levels_unchanged=True)
    state['four_doors']=['compensation arithmétique','tête praticable','couplages et sources certifiés','couverture non bornée']
    state['pedagogy']='32 fiches en cinq étapes ; formules vectorielles ; catalogue des usages séparé des archives'
    write(D/'v646_etat_recherche.json',state)
    np=ROOT/'2_Methode/Navigateur/carte_navigation.json';nav=read(np)
    rows=[('v646_lego_complet','Assembler le premier Lego complet','fait','K1–K7, bornes et tous tests sur une famille bornée',STATUS,4),
        ('v646_operateur_conjoint','Affiner conjointement énergie et déplacements premiers','ouvert','Comment conserver le coût énergétique des attaches quand le support et les bandes grandissent ?','Concentration par opérateur et potentiels par cellules ; une norme première séparée perd la compensation.',4),
        ('v646_tete_praticable','Affiner la concentration sans tête brute','ouvert','Comment remplacer la seule trace par un contrôle opératoire certifié, avec un coût praticable ?','Même Gram, concentrations par bandes et éventuel contrôle Schatten2 ; source du gain et coût doivent être explicités.',4),
        ('v646_sources_tetes','Réutiliser la projection pour les vraies sources des têtes','ouvert','Comment certifier les sources et leur Gram optimal en L² avec leurs erreurs ?','Même projection pour les fréquences et les résidus ; certificat borné direct n’a pas encore exécuté cette branche générale.',4),
        ('v646_transport_non_borne','Construire la règle d’agrandissement non bornée','ouvert','Quelle loi couvre une suite S_n→∞ avec les nouvelles directions et les couplages ?','L’inclusion fournit tous S≤S₀ ; les supports au-delà demandent une nouvelle construction.',5)]
    for id,title,status,question,thesis,cost in rows:
        if any(x['id']==id for x in nav['coups']):continue
        c=dict(id=id,titre=title,statut=status,type='construction',question=question,these=thesis,cout=cost,version='V6.46',temoin='Document71 : premier2 présent, bornes binaires, marge et contrôle perturbé.',document=S71+'.pdf',
            gains={},probabilite=0.5,probabilite_scope='Convention éditoriale historique ; aucune probabilité de RH.',prerequis=[],debloque=[],operateurs=[],croise=['RH'],repond_a=[],
            refutation='Témoin négatif de la forme complète sous toutes les gardes ; échec du certificat reste indéterminé.',
            prevision=dict(gains={},probabilite=0.5,cout=cost,refutation='Un modèle perturbé ne réfute pas RH ; une famille bornée ne couvre pas l’infini.'))
        if status=='fait':c['appris']=STATUS
        nav['coups'].append(c)
    nav['bilan_v646']=dict(document=S71+'.pdf',graphe=state['graph'],resultat=STATUS);write(np,nav)
    ip=ROOT/'2_Methode/Indicateur/indicateur_avancement.json';ind=read(ip)
    if not any(x['id']=='v646' for x in ind['etapes']):
        ind['etapes'].append(dict(id='v646',court='V6.46',versions='V6.46',jour='12 oct.',franchi=STATUS,
            pourquoi=dict(comprendre='Même Gram pour sources/fréquences ; même bord pour coût et attaches. Premier certificat complet borné.',case='Le signe local est prouvé ; les niveaux globaux restent inchangés, sans loi vers l’infini.'),
            niveaux=dict(ind['etapes'][-1]['niveaux']),documents=[['Lego et certificat complet',S71+'.pdf'],['Atelier Lego',state['graph']],['Dictionnaire courant',state['dictionary']]]))
    write(ip,ind)
    sp=ROOT/'2_Methode/Sources/sources.json';sources=read(sp)
    for s in sources:
        if s['cle'] in ('CC21','NIS10'):
            if '71' not in s.setdefault('docs',[]):s['docs'].append('71')
        if s['cle']=='CC21':
            note=' V6.46 : introduction (4) et théorème1 relus pour situer support et projections ; nos lemmes locaux sont reconstruits directement, sans transfert de positivité globale ni priorité revendiquée.'
            if note.strip() not in s['ce_qui_a_ete_verifie']:s['ce_qui_a_ete_verifie']+=note
    write(sp,sources)
    mp=ROOT/'2_Methode/Matrice/matrice_theories.json';mat=read(mp);mat['version']='V6.46'
    for n in mat['noeuds']:
        if n['id']=='WEIL':
            note=' V6.46 : certificat coercif sur tous tests pour 0<S≤0,347, premier2 présent. Projection/couches/bord réutilisables ; loi non bornée ouverte.'
            if note.strip() not in n.get('apport_note',''):n['apport_note']=n.get('apport_note','')+note
            if '71' not in n.setdefault('docs',[]):n['docs'].append('71')
    write(mp,mat)
    patch(ROOT/'2_Methode/Indicateur/build_indicateur.py','"Langue et preuves"','"Langue et Lego"')
    port=ROOT/'2_Methode/Portail/build_portail.py'
    patch(port,"current_path = ROOT / '3_Preuves_et_calculs/data/v645_etat_recherche.json'","current_path = ROOT / '3_Preuves_et_calculs/data/v646_etat_recherche.json'\n    if not current_path.exists():current_path=ROOT/'3_Preuves_et_calculs/data/v645_etat_recherche.json'")
    patch(port,'Les 70 documents ; pont arithmétique V6.45, dictionnaire enrichi, contrats V6.43 et modèle documentaire V6.42 conservés.','Les 71 documents ; Lego V6.46 et certificat borné complet, dictionnaire enrichi et modèles historiques conservés.')
    t=port.read_text()
    if '("Le Lego réutilisable",' not in t:t=t.replace('        ("Le pont arithmétique",','        ("Le Lego réutilisable", "1_Presentation/71_LEGO_REUTILISABLE.html", "Premier certificat complet : tous tests, premier2 présent, 0<S≤0,347 ; atelier de raccords."),\n        ("Certificat local complet", "1_Presentation/'+S71+'.pdf", "Document71 : K1–K7, intervalles, constantes rationnelles, modèles perturbés et gardes."),\n        ("Le pont arithmétique",',1)
    port.write_text(t)
    nbuild=ROOT/'2_Methode/Navigateur/build_navigateur.py'
    patch(nbuild,"    if carte.get('bilan_v645'):","    if carte.get('bilan_v646'):\n        phase='<section class=\"sheet\"><h2>V6.46 : Lego et certificat borné complet</h2><p>'+carte['bilan_v646']['resultat']+'</p><p><a href=\"71_LEGO_REUTILISABLE.html\">Atelier de raccords</a> · <a href=\"'+carte['bilan_v646']['document']+'\">K1–K7 et encadrements</a></p></section>'\n    elif carte.get('bilan_v645'):")
    ap=ROOT/'2_Methode/Outils/build_v638_atlas.py'
    patch(ap,"    if registry.get('version')=='V6.45':","    if registry.get('version')=='V6.46':\n        body=body.replace('<header>','<section><h2>V6.46 : Lego réutilisable</h2><p><a href=\"71_LEGO_REUTILISABLE.html\">Certificat complet et raccords</a> · <a href=\"69_LANGUE_DES_PASSAGES.html\">Dictionnaire courant</a>. Tous tests pour 0&lt;S≤347/1000 ; premier2 présent ; transport non borné ouvert.</p></section><header>',1)\n        body=body.replace('Comparer les suites de travaux','Modèle documentaire de référence V6.42')\n        body=body.replace('data/v642_decisions.json','data/v646_decisions.json')\n    elif registry.get('version')=='V6.45':")
    vp=ROOT/'VERSION.txt';old=vp.read_text(encoding='utf-8-sig')
    if not old.startswith('Programme Riemann — V6.46'):vp.write_text('Programme Riemann — V6.46\nDate: 2026-10-12\n'+STATUS+'\n\nHistorique conservé :\n'+old,encoding='utf-8-sig')
    patch(ROOT/'CITATION.cff','version 6.45','version 6.46');patch(ROOT/'CITATION.cff','version: "6.45"','version: "6.46"')
    rp=ROOT/'README.md';t=rp.read_text(encoding='utf-8-sig').replace('version 6.45','version 6.46',1)
    section='## V6.46 - Lego réutilisable et certificat complet (document71)\n\n'+STATUS+'\n\nOuvrir `1_Presentation/71_LEGO_REUTILISABLE.html`. Le document71 démontre les raccords K1–K7 et les constantes simples. Le certificat est analytique et numérique, sans preuve formelle automatisée. Il couvre une famille bornée, pas une exhaustion ; les essais 0,348 et 0,5 restent indéterminés. Les sources fortes des têtes générales ne sont pas certifiées par l’exemple algébrique. Les éditions PDF antérieures sont conservées.\n\n'
    if '## V6.46 -' not in t:t=section+t
    rp.write_text(t,encoding='utf-8-sig')
    cp=ROOT/'00_Carte_des_idees.html';t=cp.read_text(encoding='utf-8-sig').replace('Version 6.45.','Version 6.46.').replace('programme Riemann V6.45','programme Riemann V6.46')
    if 'V6.46 : Lego' not in t:t=t.replace('<footer>','<section class="panel"><h2>V6.46 : Lego et certificat local</h2><p>'+STATUS+'</p><p><a href="1_Presentation/71_LEGO_REUTILISABLE.html">Raccords et résultats</a> · <a href="1_Presentation/'+S71+'.pdf">Preuves K1–K7</a></p></section><footer>',1)
    bi=module('nav646card',ROOT/'2_Methode/Indicateur/build_indicateur.py');t=re.sub(r'<nav class=[\'\"]topnav[\'\"].*?</nav>',bi.topnav('carte',''),t,count=1,flags=re.S);cp.write_text(t,encoding='utf-8-sig')
def finish():
    for rel in ('2_Methode/Sources/build_sources.py','2_Methode/Matrice/build_matrice.py','2_Methode/Indicateur/build_indicateur.py','2_Methode/Navigateur/build_navigateur.py','2_Methode/Figures/build_figures.py','2_Methode/Portail/build_portail.py'):
        subprocess.run([sys.executable,str(ROOT/rel)],check=True,stdout=subprocess.DEVNULL)
    bi=module('nav646finish',ROOT/'2_Methode/Indicateur/build_indicateur.py')
    for name in ['65_GRAPHE_DES_PASSAGES.html','66_GRAPHE_DES_CERTIFICATS.html','67_GRAPHE_DES_PONTS.html','70_PONT_ARITHMETIQUE.html']:
        p=P/name;t=p.read_text(encoding='utf-8-sig');t=re.sub(r'<nav class=[\'\"]topnav[\'\"].*?</nav>',bi.topnav('graphe','../'),t,count=1,flags=re.S)
        if 'Lego V6.46' not in t:t=t.replace('<main>','<main><p><a href="71_LEGO_REUTILISABLE.html">Lego V6.46 : certificat complet borné et raccords</a></p>',1)
        p.write_text(t)
    for p in ROOT.rglob('*.md'):
        if 'recus' not in p.parts and not p.read_bytes().startswith(b'\xef\xbb\xbf'):p.write_bytes(b'\xef\xbb\xbf'+p.read_bytes())
    registry=read(D/'v645_decisions.json');registry.update(version='V6.46',coverage=dict(presentation_documents=71,numbers=list(range(1,72))),corpus_base='V6.46, éditions et données scientifiques historiques conservées')
    registry['documents'].append(dict(numero=71,id='doc71',titre='Lego réutilisable et premier certificat complet',etat_anterieur='V645 : source-Schur suffisant et queue astronomique, signe local non certifié.',
        question='Peut-on assembler un certificat complet praticable en conservant les coups doubles ?',action='Projection, parité, couches, potentiel de bord et coût du premier2.',resultat=STATUS,
        statut='certificat_analytique_et_intervalles_local_complet',nature='certificat_analytique_et_intervalles_local_complet',consequences='Tous tests et contrats R sur 0<S≤347/1000 ; tête nulle.',
        limites='Famille bornée seulement ; sources des têtes générales et loi non bornée ouvertes ; pas de priorité bibliographique ni preuve formelle automatisée.',
        sources=[dict(path='1_Presentation/'+S71+'.md'),dict(path='3_Preuves_et_calculs/preuves/V646_LEGO_CERTIFICATS.md'),dict(path='3_Preuves_et_calculs/data/v646_lego_resultats.json')],
        formats_regroupes=['1_Presentation/'+S71+ext for ext in ('.md','.pdf','.tex')]+['1_Presentation/71_LEGO_REUTILISABLE.html'],correctifs_ulterieurs=[],
        alternatives_documentees=['Énergie−norme première indépendante : budget échoue','Énergie/premier joints : certificat positif','Au-delà : échec du gabarit, pas réfutation'],
        prevision_et_apres_coup='Maillage et supports choisis après exploration ; protocole figé avant encadrements. Contrôle négatif sur modèle modifié explicitement déclaré.'))
    for r in registry['documents']:
        if r['numero']==69:r['correctifs_ulterieurs'].append('V646 : parcours reconstruit en32fiches et5étapes, formulesSVG et10usages explicités ; archives et index séparés. PDF69 reste édition V644.')
        for s in r.get('sources',[]):
            if isinstance(s,dict) and (ROOT/s['path']).exists():s['sha256']=hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()
    write(D/'v646_decisions.json',registry)
    atlas=module('atlas646',ROOT/'2_Methode/Outils/build_v638_atlas.py');(P/'62_ATLAS_DES_DECISIONS_BELLMAN.html').write_text(atlas.html_atlas(registry,read(D/'v642_modele_bellman.json'),read(D/'v642_bellman_resultats.json')))
    print('V646 intégrée : 71 documents, interfaces courantes synchronisées, signe global toujours ouvert.')
def main():
    metadata();module('build646integrated',ROOT/'2_Methode/Outils/build_v646.py').main()
    module('language646current',ROOT/'2_Methode/Outils/build_v644.py').interactive();finish()
if __name__=='__main__':main()
