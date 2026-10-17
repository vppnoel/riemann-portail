"""Synchronize active interfaces while retaining the scientific history."""
from pathlib import Path
import sys,json,re,hashlib,subprocess,importlib.util
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'1_Presentation';D=ROOT/'3_Preuves_et_calculs/data'
STEM='72_CONCENTRATION_PROJETEE_ET_OPERATEUR_COMMUN'
STATUS='Tous tests complexes, 0<S≤3/8 : Q_W≥masse/12 et R/100, premier2 présent. Concentration Schatten2 encadrée sur des sous-niveaux projetés. Opérateur commun démontré ; diagnostic positif à S=1/2 encore non certifié. Sources générales et couverture non bornée ouvertes.'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def module(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
def patch(p,a,b):
    t=p.read_text(encoding='utf-8-sig')
    if a in t:p.write_text(t.replace(a,b),encoding='utf-8-sig' if p.suffix=='.md' else 'utf-8')
def metadata():
    state=read(D/'v646_etat_recherche.json');state.update(version='V6.47',result=STATUS,document=STEM+'.pdf',graph='72_CONCENTRATION_PROJETEE.html',
        current_dictionary='v647_parcours_pedagogique.json',current_dictionary_archive='v647_dictionnaire.json',
        next_actions=['v647_norme_commune','v647_sources_communes','v647_multi_premiers','v647_transport_non_borne'],
        local_certificate=dict(all_tests=True,maximum_support='3/8',mass_floor='1/12',R_floor='1/100',head_dimension=0,nonempty_prime_term=True,method='projected sublevels + certified Schatten2'),
        open=['certified common operator at S=1/2','certified actual sources and complete tails','joint multi-prime compensation and unbounded transport','historical branches, collisions and arbitrary complex A'],
        global_sign_certified=False,maturity_levels_unchanged=True,pedagogy='36 fiches en cinq étapes ; 13 outils avec usages et limites ; archives séparées')
    write(D/'v647_etat_recherche.json',state)
    np=ROOT/'2_Methode/Navigateur/carte_navigation.json';nav=read(np)
    rows=[('v647_concentration_certifiee','Certifier les interactions de fréquences','fait',STATUS,3),
        ('v647_norme_commune','Certifier la norme de l’opérateur commun','ouvert','À S=1/2, Nyström donne une petite marge positive. Il faut une compression et une erreur sur tout l’espace.',4),
        ('v647_sources_communes','Construire tête, sources et queue ensemble','ouvert','Les colonnes de l’opérateur commun fournissent les sources du bloc croisé ; leurs Grams et les erreurs restent à certifier.',4),
        ('v647_multi_premiers','Conserver les phases des nouveaux premiers','ouvert','Étendre b=a+2Σw(1−cos) et ses sous-niveaux, avec le nouveau décalage de masse et les gardes de support.',4),
        ('v647_transport_non_borne','Construire le transport au-delà des supports bornés','ouvert','Maintenir les contrats lorsque S augmente, avec nouvelles directions, nouveaux premiers et convergence de forme.',5)]
    for id,title,status,text,cost in rows:
        if any(x['id']==id for x in nav['coups']):continue
        nav['coups'].append(dict(id=id,titre=title,statut=status,type='construction',question=text,these=text,cout=cost,version='V6.47',temoin=STATUS,document=STEM+'.pdf',
            gains={},probabilite=.5,probabilite_scope='Convention éditoriale historique ; ni recalcul ni probabilité de RH.',prerequis=[],debloque=[],operateurs=[],croise=['RH'],repond_a=[],
            refutation='Échec d’une condition suffisante : indéterminé. Seul un témoin négatif complet réfuterait le signe.',
            prevision=dict(gains={},probabilite=.5,cout=cost,refutation='Famille bornée et diagnostic ne prouvent pas RH.'),**({'appris':STATUS} if status=='fait' else {})))
    nav['bilan_v647']=dict(document=STEM+'.pdf',graphe=state['graph'],resultat=STATUS);write(np,nav)
    ip=ROOT/'2_Methode/Indicateur/indicateur_avancement.json';ind=read(ip)
    if not any(x['id']=='v647' for x in ind['etapes']):ind['etapes'].append(dict(id='v647',court='V6.47',versions='V6.47',jour='13 oct.',franchi=STATUS,
        pourquoi=dict(comprendre='Les interactions projetées certifient le support3/8 ; l’opérateur commun garde un même test à travers les couches.',case='Signe local acquis ; norme commune à1/2, sources et loi non bornée restent ouvertes.'),
        niveaux=dict(ind['etapes'][-1]['niveaux']),documents=[['Concentration et opérateur commun',STEM+'.pdf'],['Lego des concentrations',state['graph']],['Dictionnaire courant',state['dictionary']]]))
    write(ip,ind)
    sp=ROOT/'2_Methode/Sources/sources.json';sources=read(sp)
    for s in sources:
        if s['cle'] in ('CC21','NIS10'):
            if '72' not in s.setdefault('docs',[]):s['docs'].append('72')
        if s['cle']=='CC21':
            note=' V6.47 : introduction (4) et théorème1 relus ; cadre de concentration et projection. Notre certificat avec premier2 est dérivé directement ; pas de transfert du signe global ni de priorité revendiquée.'
            if note.strip() not in s['ce_qui_a_ete_verifie']:s['ce_qui_a_ete_verifie']+=note
    write(sp,sources)
    mp=ROOT/'2_Methode/Matrice/matrice_theories.json';mat=read(mp);mat['version']='V6.47'
    for n in mat['noeuds']:
        if n['id']=='WEIL':
            note=' V6.47 : concentration projetée Schatten2, tous tests jusqu’à3/8. Opérateur commun et compression tête/queue/source ; S=1/2 demeure exploratoire.'
            if note.strip() not in n.get('apport_note',''):n['apport_note']=n.get('apport_note','')+note
            if '72' not in n.setdefault('docs',[]):n['docs'].append('72')
    write(mp,mat)
    port=ROOT/'2_Methode/Portail/build_portail.py'
    patch(port,"current_path = ROOT / '3_Preuves_et_calculs/data/v646_etat_recherche.json'","current_path = ROOT / '3_Preuves_et_calculs/data/v647_etat_recherche.json'\n    if not current_path.exists():current_path=ROOT/'3_Preuves_et_calculs/data/v646_etat_recherche.json'")
    patch(port,'Les 71 documents ; Lego V6.46 et certificat borné complet, dictionnaire enrichi et modèles historiques conservés.','Les 72 documents ; concentration V6.47 et certificat jusqu’à3/8 ; dictionnaire progressif et modèles historiques conservés.')
    t=port.read_text()
    if '("Lego des concentrations",' not in t:t=t.replace('        ("Le Lego réutilisable",','        ("Lego des concentrations", "1_Presentation/72_CONCENTRATION_PROJETEE.html", "Tous tests jusqu’à3/8 ; opérateur commun ; tête et sources à construire."),\n        ("Concentration et opérateur commun", "1_Presentation/'+STEM+'.pdf", "Document72 : huit lemmes, intervalles, erreurs, certificat et diagnostic séparé."),\n        ("Le Lego réutilisable",',1)
    port.write_text(t)
    nbuild=ROOT/'2_Methode/Navigateur/build_navigateur.py'
    patch(nbuild,"    if carte.get('bilan_v646'):","    if carte.get('bilan_v647'):\n        phase='<section class=\"sheet\"><h2>V6.47 : concentration et opérateur commun</h2><p>'+carte['bilan_v647']['resultat']+'</p><p><a href=\"72_CONCENTRATION_PROJETEE.html\">Lego des concentrations</a> · <a href=\"'+carte['bilan_v647']['document']+'\">Huit lemmes et certificat</a></p></section>'\n    elif carte.get('bilan_v646'):")
    atlas=ROOT/'2_Methode/Outils/build_v638_atlas.py'
    patch(atlas,"    if registry.get('version')=='V6.46':","    if registry.get('version')=='V6.47':\n        body=body.replace('<header>','<section><h2>V6.47 : concentration projetée</h2><p><a href=\"72_CONCENTRATION_PROJETEE.html\">Certificat jusqu’à3/8 et opérateur commun</a> · <a href=\"69_LANGUE_DES_PASSAGES.html\">Dictionnaire courant</a>. Norme à1/2 exploratoire, sources et couverture non bornée ouvertes.</p></section><header>',1)\n        body=body.replace('Comparer les suites de travaux','Modèle documentaire de référence V6.42')\n        body=body.replace('data/v642_decisions.json','data/v647_decisions.json')\n    elif registry.get('version')=='V6.46':")
    vp=ROOT/'VERSION.txt';old=vp.read_text(encoding='utf-8-sig')
    if not old.startswith('Programme Riemann — V6.47'):vp.write_text('Programme Riemann — V6.47\nDate: 2026-10-13\n'+STATUS+'\n\nHistorique conservé :\n'+old,encoding='utf-8-sig')
    patch(ROOT/'CITATION.cff','version 6.46','version 6.47');patch(ROOT/'CITATION.cff','version: "6.46"','version: "6.47"')
    rp=ROOT/'README.md';text=rp.read_text(encoding='utf-8-sig')
    section='## V6.47 - Concentration projetée et opérateur commun (document72)\n\n'+STATUS+'\n\nOuvrir `1_Presentation/72_CONCENTRATION_PROJETEE.html`. L’article démontre huit lemmes et le certificat. Les programmes, le protocole figé et le journal exact sont inclus. Le dictionnaire courant propose 36 fiches, cinq étapes et 13 usages. Les éditions PDF antérieures et les données scientifiques restent conservées. Les diagnostics à1/2 ne sont pas des certificats. Aucun article n’est publié à l’extérieur.\n\n'
    if '## V6.47 -' not in text:text=section+text
    rp.write_text(text,encoding='utf-8-sig')
def finish():
    for rel in ['Sources/build_sources.py','Matrice/build_matrice.py','Indicateur/build_indicateur.py','Navigateur/build_navigateur.py','Figures/build_figures.py','Portail/build_portail.py']:
        subprocess.run([sys.executable,str(ROOT/'2_Methode'/rel)],check=True,stdout=subprocess.DEVNULL)
    bi=module('nav647finish',ROOT/'2_Methode/Indicateur/build_indicateur.py')
    for rel in ['00_Carte_des_idees.html','1_Presentation/65_GRAPHE_DES_PASSAGES.html','1_Presentation/66_GRAPHE_DES_CERTIFICATS.html','1_Presentation/67_GRAPHE_DES_PONTS.html','1_Presentation/70_PONT_ARITHMETIQUE.html','1_Presentation/71_LEGO_REUTILISABLE.html']:
        p=ROOT/rel;t=p.read_text(encoding='utf-8-sig');prefix='' if p.parent==ROOT else '../';target='1_Presentation/72_CONCENTRATION_PROJETEE.html' if not prefix else '72_CONCENTRATION_PROJETEE.html'
        if not prefix:t=t.replace('Version 6.46.','Version 6.47.').replace('programme Riemann V6.46','programme Riemann V6.47')
        t=re.sub(r'<nav class=[\'\"]topnav[\'\"].*?</nav>',bi.topnav('carte' if not prefix else 'graphe',prefix),t,count=1,flags=re.S)
        banner='<p class="guard" data-current="v647"><a href="'+target+'">État courant V6.47 : tous tests jusqu’à3/8 ; opérateur commun, sources et couverture à poursuivre.</a> Cette page conserve son analyse historique.</p>'
        if 'data-current="v647"' not in t:t=t.replace('</header>','</header>'+banner,1) if '</header>' in t else t.replace('<main>','<main>'+banner,1)
        p.write_text(t,encoding='utf-8-sig' if not prefix else 'utf-8')
    for p in [ROOT/'README.md',ROOT/'3_Preuves_et_calculs/preuves/V647_CONCENTRATION_PROJETEE.md']:
        if not p.read_bytes().startswith(b'\xef\xbb\xbf'):p.write_bytes(b'\xef\xbb\xbf'+p.read_bytes())
    registry=read(D/'v646_decisions.json');registry.update(version='V6.47',coverage=dict(presentation_documents=72,numbers=list(range(1,73))),corpus_base='V6.47 ; données et éditions scientifiques historiques conservées')
    registry['documents'].append(dict(numero=72,id='doc72',titre='Concentration projetée et opérateur commun',etat_anterieur='V646 : certificat jusqu’à347/1000 ; diagnostic de sous-niveaux insuffisant aux supports suivants.',
        question='Peut-on garder les phases et les interactions de fréquences, puis un même test entre couches ?',action='Schatten2, cellules certifiées, erreurs C² ; pont commun et diagnostic à1/2.',
        resultat=STATUS,statut='certificat_analytique_et_intervalles_local_complet',nature='certificat_analytique_et_intervalles_local_complet',consequences='Q_W≥masse/12 et R/100 ; 0<S≤3/8 ; tête nulle pour cette famille.',
        limites='Famille bornée ; norme commune à1/2, vraies sources et règle non bornée ouvertes. Pas de publication extérieure ni priorité revendiquée.',
        sources=[dict(path='1_Presentation/'+STEM+'.md'),dict(path='3_Preuves_et_calculs/preuves/V647_CONCENTRATION_PROJETEE.md'),dict(path='3_Preuves_et_calculs/data/v647_concentration_resultats.json'),dict(path='3_Preuves_et_calculs/data/v647_operator_diagnostic.json')],
        formats_regroupes=['1_Presentation/'+STEM+ext for ext in ('.md','.pdf','.tex')]+['1_Presentation/72_CONCENTRATION_PROJETEE.html'],correctifs_ulterieurs=[],
        alternatives_documentees=['Trace seule : borne indéterminée','Schatten2 par couches : certificat3/8','Opérateur commun : diagnostic positif1/2 non certifié'],
        prevision_et_apres_coup='Protocole choisi après exploration puis figé avant intervalles. Thèse et critique relient les deux constructions.'))
    for row in registry['documents']:
        if row['numero']==69:row['correctifs_ulterieurs'].append('V647 :36fiches et13outils avec usages ; quatre nouveaux concepts progressifs. PDF69 conserve son éditionV644.')
        for s in row.get('sources',[]):
            if isinstance(s,dict):s['sha256']=hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()
    write(D/'v647_decisions.json',registry)
    atlas=module('atlas647',ROOT/'2_Methode/Outils/build_v638_atlas.py');(P/'62_ATLAS_DES_DECISIONS_BELLMAN.html').write_text(atlas.html_atlas(registry,read(D/'v642_modele_bellman.json'),read(D/'v642_bellman_resultats.json')))
    print('V647 :72documents ; interfaces courantes synchronisées ; maturité globale inchangée.')
def main():
    sys.path.insert(0,str(ROOT/'2_Methode/Outils'));metadata();module('build647',ROOT/'2_Methode/Outils/build_v647.py').main();finish()
if __name__=='__main__':main()
