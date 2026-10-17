"""Synchronize V645 active views while retaining historical science and editions."""
from pathlib import Path
import sys,json,hashlib,subprocess,re,importlib.util
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'1_Presentation';D=ROOT/'3_Preuves_et_calculs/data'
S70='70_PONT_ARITHMETIQUE_ET_DETTE_DE_COUPLAGE'
STATUS='Annulation polaire et identité de fluctuation de Chebyshev démontrées ; modèle continu négatif pour tout S≥16 ; moments finis insuffisants pour réduire la norme première L² ; queue resserrée et dette de Schur bornée par résidus de sources. Sources/tête certifiées et signe pour tous supports restent ouverts.'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def module(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
def patch(p,a,b):
    t=p.read_text(encoding='utf-8-sig')
    if a in t:p.write_text(t.replace(a,b),encoding='utf-8-sig' if p.suffix=='.md' else 'utf-8')
def metadata():
    previous=read(D/'v644_etat_recherche.json')
    state=dict(version='V6.45',result=STATUS,document=S70+'.pdf',dictionary='69_LANGUE_DES_PASSAGES.html',graph='70_PONT_ARITHMETIQUE.html',
        completed_bellman_actions=previous['completed_bellman_actions'],current_bellman_model=previous['current_bellman_model'],
        current_grammar=previous['current_grammar'],current_dictionary='v645_dictionnaire.json',
        next_actions=['v645_sources_residus','v645_tete_structuree','v645_loi_tous_supports'],maturity_levels_unchanged=True,
        open=['validated L2 strong-source and Gram bounds','practicable complete head with graph-norm control','effective Schur sign for every support','historical branch/collision/complex-A questions'],
        novelty_scope='internal reconstruction; no priority claim; no RH proof',global_sign_certified=False)
    write(D/'v645_etat_recherche.json',state)
    navp=ROOT/'2_Methode/Navigateur/carte_navigation.json';nav=read(navp)
    nodes=[('v645_pont_arithmetique','Retirer le pôle et garder la fluctuation','fait','C1–C5, intervalles et témoin uniforme',STATUS,4),
        ('v645_sources_residus','Certifier les sources et les résidus en L²','ouvert','Comment encadrer les intégrales de source et leur Gram avec des erreurs L² garanties ?','Le majorant de dette H−β·Gramρ/μ évite le solveur Riesz exact sous ses prémisses.',4),
        ('v645_tete_structuree','Construire une tête complète de taille praticable','ouvert','Quelle représentation compacte garde les couplages et contrôle les sources en norme de graphe ?','La queue améliorée reste immense ; la densité en R seule ne garantit pas la convergence des sources.',5),
        ('v645_loi_tous_supports','Établir une loi de signe des compensations et couplages','ouvert','Quelle propriété arithmétique force le signe du Schur complet pour tout S sans présupposer RH ?','Le modèle continu échoue ; garder phase et corrélations de la fluctuation première.',5)]
    for id,title,status,question,thesis,cost in nodes:
        if any(x['id']==id for x in nav['coups']):continue
        c=dict(id=id,titre=title,statut=status,type='construction',question=question,these=thesis,cout=cost,version='V6.45',
            temoin='Document 70 : C1–C5, 144 entrées encadrées, budget de queue et obstruction S≥16.',document=S70+'.pdf',gains={},probabilite=0.5,
            probabilite_scope='Convention éditoriale historique, aucune probabilité de RH.',prerequis=[],debloque=[],operateurs=[],croise=['RH'],repond_a=[],
            refutation='Témoin négatif encadré de Q_W avec toutes les gardes ; échec de calcul ou B0 négative ne tranche pas RH.',
            prevision=dict(gains={},probabilite=0.5,cout=cost,refutation='Nommer sources, tête ou loi manquantes ; aucun budget fini promu en signe global.'))
        if status=='fait':c['appris']=STATUS
        nav['coups'].append(c)
    nav['bilan_v645']=dict(document=S70+'.pdf',graphe=state['graph'],dictionnaire=state['dictionary'],resultat=STATUS)
    write(navp,nav)
    indp=ROOT/'2_Methode/Indicateur/indicateur_avancement.json';ind=read(indp)
    if not any(x['id']=='v645' for x in ind['etapes']):
        ind['etapes'].append(dict(id='v645',court='V6.45',versions='V6.45',jour='12 oct.',franchi=STATUS,
            pourquoi=dict(comprendre='Les moments annulent le pôle et isolent la compensation arithmétique ; les sources rendent la dette mesurable.',case='Sources, tête et loi couvrante restent ouvertes ; aucun niveau global accru.'),
            niveaux=dict(ind['etapes'][-1]['niveaux']),documents=[['Pont arithmétique et dette',S70+'.pdf'],['Atelier arithmétique',state['graph']],['Dictionnaire enrichi',state['dictionary']]]))
    write(indp,ind)
    sp=ROOT/'2_Methode/Sources/sources.json';sources=read(sp)
    for s in sources:
        if s['cle']=='CC21':
            note=' V6.45 : §3, proposition 3.5 et théorème 3.6 relus : opérateur différentiel de moments et −2I plus compact pour le traitement archimédien ; aucune extension au signe global premier.'
            if note.strip() not in s['ce_qui_a_ete_verifie']:s['ce_qui_a_ete_verifie']+=note
            if '70' not in s.setdefault('docs',[]):s['docs'].append('70')
    extra=[dict(cle='NIS26',auteurs='NIST, Digital Library of Mathematical Functions',annee=2010,
        titre='DLMF, chapitre 25, §25.16(i), Prime Number Theory',publication='Référence en ligne consultée le 12 octobre 2026',type='référence en ligne',
        lien='https://dlmf.nist.gov/25.16',statut='vérifié en ligne',verifie_le='2026-10-12',
        ce_qui_a_ete_verifie='Équations 25.16.1, 25.16.3 et 25.16.4 : définition de Ψ, théorème des nombres premiers, équivalence de RH avec Ψ(x)−x=O(x^(1/2+ε)) pour chaque ε>0.',
        usage_corpus='Définition de Chebyshev et garde contre une hypothèse de compensation déjà équivalente à RH.',verdict='exact',correction='',extrait='',
        docs=['70'],cite_aussi=[],motifs=['[NIS26]'],conjectures=['RH'],dimensions=['comprendre','situer'],interet='appui'),
        dict(cle='Gro26',auteurs='Akiva Groskin',annee=2026,titre='A finite Guinand-Weil dictionary and archimedean tail order for the truncated Weil quadratic form',
        publication='arXiv:2607.02828, version du 2 juillet 2026',type='préprint',lien='https://arxiv.org/abs/2607.02828',
        statut='partiellement vérifié',verifie_le='2026-10-12',ce_qui_a_ete_verifie='Métadonnées et résumé primaire uniquement ; preuves et artefacts non audités.',
        usage_corpus='Comparaison à examiner : dictionnaire fini pour une forme tronquée et une bande. Aucune prémisse de C1–C5 ne repose sur ce résumé.',
        verdict='non vérifiable',correction='',extrait='',docs=['70'],cite_aussi=[],motifs=['[Gro26]'],conjectures=['RH'],dimensions=['situer'],interet='confronter')]
    for s in extra:
        if not any(x['cle']==s['cle'] for x in sources):sources.append(s)
    write(sp,sources)
    matp=ROOT/'2_Methode/Matrice/matrice_theories.json';mat=read(matp);mat['version']='V6.45'
    for n in mat['noeuds']:
        if n['id']=='WEIL':
            note=' V6.45 : annulation polaire, fluctuation exacte et dette par Gram de sources ; modèle continu négatif pour tout S≥16. Tête praticable et signe tous supports ouverts.'
            if note.strip() not in n.get('apport_note',''):n['apport_note']=n.get('apport_note','')+note
            if '70' not in n.setdefault('docs',[]):n['docs'].append('70')
    write(matp,mat)
    port=ROOT/'2_Methode/Portail/build_portail.py'
    patch(port,"current_path = ROOT / '3_Preuves_et_calculs/data/v644_etat_recherche.json'","current_path = ROOT / '3_Preuves_et_calculs/data/v645_etat_recherche.json'\n    if not current_path.exists():current_path=ROOT/'3_Preuves_et_calculs/data/v644_etat_recherche.json'")
    patch(port,'Les 69 documents ; langue et domaines V6.44, contrats V6.43, modèle documentaire V6.42 conservé.','Les 70 documents ; pont arithmétique V6.45, dictionnaire enrichi, contrats V6.43 et modèle documentaire V6.42 conservés.')
    t=port.read_text()
    if '("Le pont arithmétique",' not in t:
        t=t.replace('        ("La langue des passages",','        ("Le pont arithmétique", "1_Presentation/70_PONT_ARITHMETIQUE.html", "Annulation du pôle, fluctuation de Chebyshev, dette par résidus et budgets encadrés."),\n        ("Pont arithmétique et dette", "1_Presentation/'+S70+'.pdf", "Document 70 : C1–C5, obstruction uniforme du modèle continu et contrats suffisants."),\n        ("La langue des passages",',1)
    port.write_text(t)
    np=ROOT/'2_Methode/Navigateur/build_navigateur.py'
    patch(np,"    if carte.get('bilan_v644'):","    if carte.get('bilan_v645'):\n        phase='<section class=\"sheet\"><h2>V6.45 : pont arithmétique et dette des sources</h2><p>'+carte['bilan_v645']['resultat']+'</p><p><a href=\"70_PONT_ARITHMETIQUE.html\">Atelier et contrats</a> · <a href=\"'+carte['bilan_v645']['document']+'\">C1–C5 et exécution</a></p></section>'\n    elif carte.get('bilan_v644'):")
    ap=ROOT/'2_Methode/Outils/build_v638_atlas.py'
    patch(ap,"    if registry.get('version')=='V6.44':","    if registry.get('version')=='V6.45':\n        body=body.replace('<header>','<section><h2>V6.45 : pont arithmétique</h2><p><a href=\"70_PONT_ARITHMETIQUE.html\">Fluctuation, budgets et dette</a> · <a href=\"69_LANGUE_DES_PASSAGES.html\">Dictionnaire enrichi</a>. Annulation polaire et obstruction uniforme du modèle continu démontrées ; signe tous supports encore ouvert. <a href=\"67_GRAPHE_DES_PONTS.html\">Pilote des contrats V6.43</a>.</p></section><header>',1)\n        body=body.replace('Comparer les suites de travaux','Modèle documentaire de référence V6.42')\n        body=body.replace('data/v642_decisions.json','data/v645_decisions.json')\n    elif registry.get('version')=='V6.44':")
    vp=ROOT/'VERSION.txt';old=vp.read_text(encoding='utf-8-sig')
    if not old.startswith('Programme Riemann — V6.45'):vp.write_text('Programme Riemann — V6.45\nDate: 2026-10-12\n'+STATUS+'\n\nHistorique conservé :\n'+old,encoding='utf-8-sig')
    patch(ROOT/'CITATION.cff','version 6.44','version 6.45');patch(ROOT/'CITATION.cff','version: "6.44"','version: "6.45"')
    rp=ROOT/'README.md';t=rp.read_text(encoding='utf-8-sig').replace('version 6.44','version 6.45',1)
    section='## V6.45 - Pont arithmétique et dette de couplage (document 70)\n\n'+STATUS+'\n\nOuvrir `1_Presentation/70_PONT_ARITHMETIQUE.html` pour les budgets et le contrat de dette, et `69_LANGUE_DES_PASSAGES.html` pour le dictionnaire courant. Le document 70 contient les preuves C1–C5, les intervalles et les gardes. Les PDF 68–69 conservent leur édition V6.44 ; le lecteur interactif 69 reçoit treize fiches nouvelles. Les 144 entrées premières/résiduelles sont encadrées ; la quadrature archimédienne et le total restent exploratoires. Aucune tête de dimension 10^37 n’a été calculée.\n\n'
    if '## V6.45 -' not in t:t=section+t
    rp.write_text(t,encoding='utf-8-sig')
    cp=ROOT/'00_Carte_des_idees.html';t=cp.read_text(encoding='utf-8-sig').replace('Version 6.44.','Version 6.45.').replace('programme Riemann V6.44','programme Riemann V6.45')
    if 'V6.45 : pont arithmétique' not in t:t=t.replace('<footer>','<section class="panel"><h2>V6.45 : pont arithmétique</h2><p>'+STATUS+'</p><p><a href="1_Presentation/70_PONT_ARITHMETIQUE.html">Budgets, compensation et contrat</a> · <a href="1_Presentation/'+S70+'.pdf">Preuves</a></p></section><footer>',1)
    bi=module('nav645',ROOT/'2_Methode/Indicateur/build_indicateur.py')
    t=re.sub(r'<nav class=[\'\"]topnav[\'\"].*?</nav>',bi.topnav('carte',''),t,count=1,flags=re.S);cp.write_text(t,encoding='utf-8-sig')
    sys.path.insert(0,str(ROOT/'3_Preuves_et_calculs/src'))
    import prime_centered_bridge as b
    results=read(D/'v645_arithmetique_resultats.json');results['uniform_negative_base_certificate']=b.uniform_negative_base_certificate();write(D/'v645_arithmetique_resultats.json',results)
def finish():
    for rel in ('2_Methode/Sources/build_sources.py','2_Methode/Matrice/build_matrice.py','2_Methode/Indicateur/build_indicateur.py','2_Methode/Navigateur/build_navigateur.py','2_Methode/Figures/build_figures.py','2_Methode/Portail/build_portail.py'):
        subprocess.run([sys.executable,str(ROOT/rel)],check=True,stdout=subprocess.DEVNULL)
    bi=module('nav645final',ROOT/'2_Methode/Indicateur/build_indicateur.py')
    for number,stem in [(65,'PASSAGES'),(66,'CERTIFICATS'),(67,'PONTS')]:
        p=P/(str(number)+'_GRAPHE_DES_'+stem+'.html');t=p.read_text(encoding='utf-8-sig')
        t=re.sub(r'<nav class=[\'\"]topnav[\'\"].*?</nav>',bi.topnav('graphe','../'),t,count=1,flags=re.S)
        if 'Pont V6.45' not in t:t=t.replace('<main>','<main><p><a href="70_PONT_ARITHMETIQUE.html">Pont V6.45 : compensation arithmétique et dette de sources</a></p>',1)
        p.write_text(t)
    for p in ROOT.rglob('*.md'):
        if 'recus' not in p.parts and not p.read_bytes().startswith(b'\xef\xbb\xbf'):p.write_bytes(b'\xef\xbb\xbf'+p.read_bytes())
    registry=read(D/'v644_decisions.json');registry.update(version='V6.45',coverage=dict(presentation_documents=70,numbers=list(range(1,71))),corpus_base='V6.45, éditions historiques et données conservées')
    if not any(x['numero']==70 for x in registry['documents']):
        registry['documents'].append(dict(numero=70,id='doc70',titre='Le pont arithmétique et la dette de couplage',etat_anterieur='V644 : identité moins compact et queue effective, signe global ouvert.',
            question='Quelle compensation première et quelle dette de tête contrôlent la forme complète ?',action='Annulation polaire, Chebyshev, obstructions, budget du support et sources fortes.',
            resultat=STATUS,statut='preuves_auxiliaires_et_encadrements_locaux',nature='preuves_auxiliaires_et_encadrements_locaux',
            consequences='Réduction suffisante par résidus de sources ; queue améliorée, tête non calculée.',limites='Pas de certificat total de quadrature archimédienne, ni de signe tous supports ; convergence en norme de graphe encore à établir.',
            sources=[dict(path='1_Presentation/'+S70+'.md'),dict(path='3_Preuves_et_calculs/preuves/V645_PONT_ARITHMETIQUE.md'),dict(path='3_Preuves_et_calculs/data/v645_arithmetique_resultats.json')],
            formats_regroupes=['1_Presentation/'+S70+ext for ext in ('.md','.pdf','.tex')]+['1_Presentation/70_PONT_ARITHMETIQUE.html'],
            correctifs_ulterieurs=[],alternatives_documentees=['Modèle continu seul : obstruction S≥16','Moments seuls : norme L² inchangée','Résidus L² : certificat suffisant sans garantie de terminaison'],
            prevision_et_apres_coup='Protocole figé avant encadrements ; données et signes V644 déjà connus ; directions de compensation proposées après décomposition. Obstruction uniforme prouvée après exécution.'))
    for r in registry['documents']:
        if r['numero']==69:
            r['correctifs_ulterieurs'].append('V645 : lecteur HTML et index technique enrichis ; PDF 69 demeure édition V644.')
        for s in r.get('sources',[]):
            if isinstance(s,dict) and (ROOT/s['path']).exists():s['sha256']=hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()
    write(D/'v645_decisions.json',registry)
    atlas=module('atlas645',ROOT/'2_Methode/Outils/build_v638_atlas.py')
    (P/'62_ATLAS_DES_DECISIONS_BELLMAN.html').write_text(atlas.html_atlas(registry,read(D/'v642_modele_bellman.json'),read(D/'v642_bellman_resultats.json')))
    print('V645 synchronisée : 70 documents, niveaux globaux inchangés, historique conservé.')
def main():
    metadata()
    build=module('build645integrated',ROOT/'2_Methode/Outils/build_v645.py');build.main()
    module('language645current',ROOT/'2_Methode/Outils/build_v644.py').interactive()
    finish()
if __name__=='__main__':main()
