"""Integrate conceptual bridge phase; keep old results and certificate inputs."""
from pathlib import Path
import json,hashlib,importlib.util,subprocess,sys,re
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'1_Presentation';D=ROOT/'3_Preuves_et_calculs/data';STEM='67_CONSTRUIRE_DES_PONTS_AVEC_BELLMAN'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def module(name,p):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def run(p):subprocess.run([sys.executable,str(ROOT/p)],check=True,stdout=subprocess.DEVNULL)
def patch(p,old,new):
    t=p.read_text(encoding='utf-8-sig')
    if old in t:p.write_text(t.replace(old,new),encoding='utf-8-sig' if p.suffix=='.md' else 'utf-8')


def main():
    status='Transport Beurling–translations, continuité de Weil dans H¹, cœur admissible, régularisation décalée et Schur démontrés. Bellman de contrats et de formes distingués ; estimation arithmétique de toute la famille encore ouverte.'
    state=dict(version='V6.43',completed_bellman_actions=read(D/'v642_etat_recherche.json')['completed_bellman_actions'],
               document=STEM+'.pdf',graph='67_GRAPHE_DES_PONTS.html',result=status,
               next_actions=['v643_dette_schur','v643_regime_commun'],current_bellman_model='v643_modele_ponts.json',
               reference_documentary_model='v642_modele_bellman.json',scope='Auxiliary mathematical bridges proved internally; no arithmetic family sign theorem',maturity_levels_unchanged=True)
    write(D/'v643_etat_recherche.json',state)
    navp=ROOT/'2_Methode/Navigateur/carte_navigation.json';nav=read(navp)
    for c in nav['coups']:
        if c['id']=='lire_Ham21':c.update(statut='fait',version='V6.43',appris='Original 1921 relu ; nombre fini de pôles autorisé, croissance contrôlée, séries de Dirichlet et équation exacte. La version Perelli plus étroite n’est pas l’énoncé original.',these='Énoncé original : nombre fini de pôles et croissance e^(|s|^γ) hors disque ; convergence absolue et équation fonctionnelle exacte.',document=STEM+'.pdf')
        if c['id']=='lire_Beu55':c.update(statut='fait',version='V6.43',appris='Texte primaire relu ; semi-groupe invariant, densité ↔ approximation de 1, Mellin et dépendance au théorème 1953 explicités. Pont d’erreur reconstruit sans signe global.',document=STEM+'.pdf')
        if c['id']=='lire_Wei48':c.update(these='Lecture ciblée du mémoire via retranscription : positivité de trace sur les correspondances et Frobenius ; ne pas réduire ce mémoire à la seule jacobienne. Lecture intégrale et recoupement de l’édition encore ouverts.',appris_v643='Théorème 10 et application au Frobenius consultés ; fiche précédente rectifiée, statut intégral non attribué.')
    nodes=[
      dict(id='v643_ponts_construits',titre='Construire les transports, le domaine et Schur',statut='fait',type='construction',question='Quels ponts peuvent être démontrés avant de connaître le signe ?',these='B1–B5 : transports exacts, continuité H¹, cœur, régularisation et Schur.',appris=status,cout=4.0,document=STEM+'.pdf'),
      dict(id='v643_dette_schur',titre='Construire un invariant arithmétique pour la dette de Schur',statut='ouvert',type='construction',question='Pour une famille de tests explicitée, comment borner a_n−c_n*G_n†c_n et contrôler la portée du couplage pour tous les indices ?',these='La forme complète et son domaine, plutôt que la partie première seule, doivent gouverner la récurrence.',temoin='B2–B5 du document 67 ; matrices de masse H¹ ; contre-exemple de portée synthétique.',refutation='Contre-exemple au candidat avec domaine et indices précisés ; absence de borne classée comme question ouverte.',cout=4.0),
      dict(id='v643_regime_commun',titre='Contrôler une famille régularisée et son défaut de transport',statut='ouvert',type='construction',question='Quel choix de cutoffs et paramètres contrôle couverture et défaut dans H¹ sans prendre la densité NB pour un acquis ?',these='T=Pχ(ηδ*Γ_S) donne un contrôle fixe ; la famille et le taux doivent être définis avant toute limite.',temoin='B4 : décalage, borne δ^-3, défaut bilinéaire et dépendance aux cutoffs.',refutation='Défaut non contrôlé ou circularité ; conserver le résultat fixe et fermer seulement la conclusion effectivement réfutée.',cout=3.0)]
    for c in nodes:
        if not any(x['id']==c['id'] for x in nav['coups']):
            c.update(version='V6.43',gains={},probabilite=0.5,prerequis=[],debloque=[],operateurs=[],croise=['RH'])
            c['prevision']=dict(gains={},probabilite=0.5,cout=c['cout'],refutation=c.get('refutation','Preuve auxiliaire ou garde manquante.'))
            c['probabilite_scope']='Convention éditoriale du navigateur historique ; non utilisée par le nouveau Bellman.'
            nav['coups'].append(c)
    for c in nav['coups']:
        if c['id'].startswith('v643_'):
            c.setdefault('version','V6.43')
            c.setdefault('temoin','Document 67 ; preuves B1–B5 et programmes de contrôle.')
            c.setdefault('refutation','Hypothèse de domaine ou étape de preuve invalide ; pas de conclusion globale automatique.')
            c.setdefault('repond_a',[])
    nav['bilan_v643']=dict(document=STEM+'.pdf',graphe=state['graph'],resultat=status,pont_global='estimation de famille ouverte')
    write(navp,nav)
    indp=ROOT/'2_Methode/Indicateur/indicateur_avancement.json';ind=read(indp)
    if not any(e['id']=='v643' for e in ind['etapes']):
        last=ind['etapes'][-1]
        ind['etapes'].append(dict(id='v643',court='V6.43',versions='V6.43',jour='12 oct.',franchi=status,pourquoi={'comprendre':'Transport et domaine établis sans signe présupposé.','case':'Aucun signe de famille acquis ; niveaux inchangés.'},niveaux=dict(last['niveaux']),documents=[['Construire des ponts avec Bellman',STEM+'.pdf'],['Carte et pilote de contrats','67_GRAPHE_DES_PONTS.html']]))
    write(indp,ind)
    sp=ROOT/'2_Methode/Sources/sources.json';sources=read(sp)
    for s in sources:
        if s['cle']=='Ham21':s.update(lien='https://gdz.sub.uni-goettingen.de/download/pdf/PPN266833020_0010/PPN266833020_0010.pdf',statut='vérifié en ligne',verifie_le='2026-10-12',ce_qui_a_ete_verifie='Original Math. Z. 10 (1921), pages 240–254 relu ; énoncé initial, extension avec g et preuve par Mellin/périodicité. Nombre fini de pôles autorisé sous croissance contrôlée.',usage_corpus='Rigidité : série de Dirichlet ordinaire, croissance e^(|s|^γ) hors disque, nombre fini de pôles et équation fonctionnelle exacte de zêta impliquent F=cζ.',correction='La fiche antérieure présentait la condition (s−1)^m F entière d’ordre fini de Perelli comme hypothèse exacte de l’original. C’est une version suffisante plus étroite ; l’original permet un nombre fini de pôles.',verdict='exact')
        if s['cle']=='Beu55':s.update(lien='https://www.pnas.org/doi/pdf/10.1073/pnas.41.5.312',statut='vérifié en ligne',verifie_le='2026-10-12',ce_qui_a_ete_verifie='Texte primaire PNAS 312–314 relu : espace admissible, semi-groupe, approximation de 1, transformée de Mellin, dualité et théorème 1953 cité. Le pont H¹ régularisé est une reconstruction démontrée du dossier 67.',correction='La convergence L² du critère ne contrôle pas directement la forme de Weil sur H¹ ; domaine et régularisation sont nécessaires.')
        if s['cle']=='Wei48':s.update(lien='https://denisevellachemla.eu/Weil-courbes-varietes.pdf',statut='partiellement vérifié',verifie_le='2026-10-12',ce_qui_a_ete_verifie='Lecture ciblée de la retranscription 2022 : anneau des classes de correspondances, théorème 10 σ(ξξ′)>0 et Frobenius, théorème 13/corollaire 3 ; lecture intégrale et recoupement avec l’édition originale encore ouverts.',correction='Le mémoire Sur les courbes… établit directement la positivité par correspondances, intersections et Riemann–Roch. La fiche précédente le résumait trop exclusivement par la jacobienne ; ne pas confondre ce mémoire et celui sur les variétés abéliennes.',usage_corpus='Mécanisme de positivité sur les classes de correspondances, puis inégalité de trace pour le Frobenius ; modèle géométrique, aucun transfert établi à zêta des entiers.')
        if s['cle'] in ('Ham21','Beu55','Wei48','CC21'):
            s.setdefault('docs',[])
            if '67' not in s['docs']:s['docs'].append('67')
    write(sp,sources)
    bi_path=ROOT/'2_Methode/Indicateur/build_indicateur.py';patch(bi_path,'("graphe", "Graphe des certificats", "1_Presentation/66_GRAPHE_DES_CERTIFICATS.html")','("graphe", "Ponts et preuves", "1_Presentation/67_GRAPHE_DES_PONTS.html")')
    port=ROOT/'2_Methode/Portail/build_portail.py'
    patch(port,'current_path = ROOT / \'3_Preuves_et_calculs/data/v642_etat_recherche.json\'','current_path = ROOT / \'3_Preuves_et_calculs/data/v643_etat_recherche.json\'\n    if not current_path.exists():current_path=ROOT/\'3_Preuves_et_calculs/data/v642_etat_recherche.json\'')
    patch(port,'("Un pli certifié et sa paire",','("Construire des ponts avec Bellman", "1_Presentation/'+STEM+'.pdf", "Document 67 : transports, domaine H¹, cœur dense, régularisation et dette de Schur."),\n        ("Ponts et contrats", "1_Presentation/67_GRAPHE_DES_PONTS.html", "Carte des implications et pilote adaptatif de constructions complémentaires."),\n        ("Un pli certifié et sa paire",')
    patch(port,'Les 66 documents, leurs résultats et limites ; état V6.42 et modèle courant de douze actions, dont cinq achevées.','Les 67 documents ; pilote courant de contrats V6.43, modèle documentaire V6.42 conservé pour comparaison.')
    np=ROOT/'2_Methode/Navigateur/build_navigateur.py'
    old="    if carte.get('bilan_v642'):"
    new="""    if carte.get('bilan_v643'):
        phase='<section class="sheet"><h2>Phase V6.43 : construire des ponts</h2><p>Transport opératoire, domaine H¹, cœur admissible, régularisation décalée et Schur sont démontrés. La priorité est un invariant arithmétique sur une famille, avec contrôle des noyaux et du défaut. Le classement général reste documentaire et conventionnel.</p><p><a href="67_GRAPHE_DES_PONTS.html">Carte et pilote courant</a> · <a href="67_CONSTRUIRE_DES_PONTS_AVEC_BELLMAN.pdf">Lemmes et preuves</a></p></section>'
    elif carte.get('bilan_v642'):"""
    patch(np,old,new)
    # Old atlas deliberately continues using its own compatible V642 model/state.
    ap=ROOT/'2_Methode/Outils/build_v638_atlas.py'
    anchor="    script=script.replace(\"docs.length+' / 61 documents'\""
    t=ap.read_text()
    if 'Pilote de contrats V6.43' not in t:
        i=t.index(anchor)
        t=t[:i]+"""    if registry.get('version')=='V6.43':
        body=body.replace('<header>','<section><h2>Pilote de contrats V6.43</h2><p><a href="67_GRAPHE_DES_PONTS.html">Construire et évaluer des ponts</a> : AND/OR, résultats conditionnels et durées. Le calcul documentaire ci-dessous conserve le modèle V6.42 pour comparaison ; il ne pilote plus seul la phase courante.</p></section><header>',1)
        body=body.replace('Comparer les suites de travaux','Modèle documentaire de référence V6.42')
        body=body.replace('data/v642_decisions.json','data/v643_decisions.json')
"""+t[i:];ap.write_text(t)
    cp=ROOT/'00_Carte_des_idees.html';bi=module('ind643',bi_path)
    t=cp.read_text(encoding='utf-8-sig');t=t.replace('Version 6.42.','Version 6.43.').replace('programme Riemann V6.42','programme Riemann V6.43')
    if 'V6.43 : construire des ponts' not in t:t=t.replace('<footer>','<section class="panel"><h2>V6.43 : construire des ponts</h2><p>'+status+'</p><p><a href="1_Presentation/67_GRAPHE_DES_PONTS.html">Carte et pilote</a> · <a href="1_Presentation/'+STEM+'.pdf">Démonstrations</a></p></section><footer>',1)
    t=re.sub(r"<nav class=['\"]topnav['\"].*?</nav>",bi.topnav('carte',''),t,count=1,flags=re.S);cp.write_text(t,encoding='utf-8-sig')
    vp=ROOT/'VERSION.txt';old=vp.read_text(encoding='utf-8-sig')
    if not old.startswith('Programme Riemann — V6.43'):vp.write_text('Programme Riemann — V6.43\nDate: 2026-10-12\nStatut: ponts auxiliaires et Bellman de contrats\n'+status+'\n\nHistorique conservé :\n'+old,encoding='utf-8-sig')
    cf=ROOT/'CITATION.cff';patch(cf,'version 6.42','version 6.43');patch(cf,'version: "6.42"','version: "6.43"')
    rp=ROOT/'README.md';t=rp.read_text(encoding='utf-8-sig').replace('version 6.42','version 6.43',1).replace('# 262 tests','# 271 tests',1)
    section='''## V6.43 - Construire des ponts avec Bellman (document 67)

Des mécanismes sont maintenant reliés par des identités et des domaines explicites : Beurling → translations ; forme complète de Weil → opérateur signé sur H¹ ; cœur dense et famille de compressions ; régularisation avec décalage ; complément de Schur comme élimination dynamique. Les preuves auxiliaires sont données. L’estimation arithmétique pour toute la famille reste ouverte.

- [Dossier PDF](1_Presentation/67_CONSTRUIRE_DES_PONTS_AVEC_BELLMAN.pdf), [LaTeX](1_Presentation/67_CONSTRUIRE_DES_PONTS_AVEC_BELLMAN.tex), [carte et pilote de contrats](1_Presentation/67_GRAPHE_DES_PONTS.html).
- Deux Bellman : élimination dans une forme ; décision sur contrats AND/OR et issues. Modèle documentaire V642 conservé comme référence.
- 270 scénarios contrôlés indépendamment ; durées et valeurs conventionnelles. Aucun scénario ne peut attribuer RH ou le signe global.
- Sources Hamburger/Beurling relues et corrigées ; lecture intégrale de Weil encore ouverte.

~~~bash
python 3_Preuves_et_calculs/scripts/run_v643_bridges.py
node 3_Preuves_et_calculs/scripts/check_v643_client.js
python 2_Methode/Outils/build_v643.py
~~~

'''
    if '## V6.43 - Construire des ponts' not in t:t=t.replace('## V6.42 - Un pli certifié',section+'## V6.42 - Un pli certifié',1)
    rp.write_text(t,encoding='utf-8-sig')
    for script in ('2_Methode/Sources/build_sources.py','2_Methode/Matrice/build_matrice.py','2_Methode/Indicateur/build_indicateur.py','2_Methode/Navigateur/build_navigateur.py','2_Methode/Figures/build_figures.py','2_Methode/Portail/build_portail.py'):run(script)
    # Refresh all active nav bars, including historical graph readers.
    pages=[('00_PORTAIL.html','portail',''),('00_Carte_des_idees.html','carte',''),('00_Liste_des_figures.html','figures',''),('1_Presentation/31_INDICATEUR_D_AVANCEMENT.html','indicateur','../'),('1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html','navigateur','../'),('1_Presentation/44_MATRICE_DES_THEORIES.html','matrice','../'),('1_Presentation/65_GRAPHE_DES_PASSAGES.html','graphe','../'),('1_Presentation/66_GRAPHE_DES_CERTIFICATS.html','graphe','../')]
    for rel,current,prefix in pages:
        p=ROOT/rel;t=p.read_text(encoding='utf-8-sig');t=re.sub(r"<nav class=['\"]topnav['\"].*?</nav>",bi.topnav(current,prefix),t,count=1,flags=re.S);p.write_text(t)
    builder=module('bridges643',ROOT/'2_Methode/Outils/build_v643.py');g=builder.graph();(P/'67_GRAPHE_DES_PONTS.html').write_text(builder.build_html(g))
    registry=read(D/'v642_decisions.json');registry.update(version='V6.43',corpus_base='V6.43 ; modèles et certificats historiques conservés',coverage=dict(presentation_documents=67,numbers=list(range(1,68))))
    proof='3_Preuves_et_calculs/preuves/V643_PONTS_MATHEMATIQUES.md';md='1_Presentation/'+STEM+'.md'
    if not any(r['numero']==67 for r in registry['documents']):registry['documents'].append(dict(numero=67,id='doc67',titre='Construire des ponts avec Bellman',etat_anterieur='Planification documentaire sous-modulaire ; ponts non représentés.',question='Quels transports et domaines conduisent à une estimation arithmétique de famille ?',action='Double examen, preuves B1–B5, complémentarités et scénarios conditionnels.',resultat=status,statut='preuves_auxiliaires_et_scenarios',nature='preuves_auxiliaires_et_scenarios',consequences='Construction d’un opérateur signé sans circularité et contrat de dette ; aucun signe global acquis.',limites='Lecture Weil partielle ; modèle conventionnel, validation de structure sans vérification automatique de toutes les preuves.',sources=[dict(path=proof),dict(path=md)],formats_regroupes=[md,md[:-3]+'.pdf',md[:-3]+'.tex','1_Presentation/67_GRAPHE_DES_PONTS.html'],correctifs_ulterieurs=[],alternatives_documentees=['Plan documentaire V642 conservé','Pilotage de contrats et Bellman de la forme distingués'],prevision_et_apres_coup='Construction théorique et choix éditoriaux après diagnostic ; aucune prévision scientifique rétrospectivement créée.'))
    for r in registry['documents']:
        if r['numero'] in (42,62):r.setdefault('correctifs_ulterieurs',[]).append(dict(version='V6.43',texte='Lecture primaire et modèle de contrats corrigent les limites du classement documentaire.',source=md))
        for s in r.get('sources',[]):
            if isinstance(s,dict) and (ROOT/s['path']).exists():s['sha256']=hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()
    assert sorted(r['numero'] for r in registry['documents'])==list(range(1,68));write(D/'v643_decisions.json',registry)
    atlas=module('atlas643',ap);(P/'62_ATLAS_DES_DECISIONS_BELLMAN.html').write_text(atlas.html_atlas(registry,read(D/'v642_modele_bellman.json'),read(D/'v642_bellman_resultats.json')))
    print('V643 intégré : portail, navigation, sources, indicateur, atlas et 67 documents ; maturité RH inchangée')
if __name__=='__main__':main()
