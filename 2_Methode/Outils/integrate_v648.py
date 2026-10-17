"""Synchronize the current corpus without rewriting prior scientific data."""
from pathlib import Path
import sys,re,hashlib,subprocess,json
from integrate_v647 import read,write,module,patch
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'1_Presentation';D=ROOT/'3_Preuves_et_calculs/data'
STEM='73_OPERATEUR_COMMUN_TETE_SOURCES_ET_QUEUE'
STATUS='Tous tests complexes, 0<S≤1/2 : Q_W≥masse/250 et R/2000. Norme de l’opérateur commun certifiée, cadre de Gauss80 et deux blocs40. La même erreur certifie tête, sources croisées, queue et Schur du minorant borné. Multi-premiers, sources fortes de Q et couverture non bornée ouverts.'
def metadata():
    state=read(D/'v647_etat_recherche.json');state.update(version='V6.48',result=STATUS,document=STEM+'.pdf',graph='73_OPERATEUR_COMMUN.html',
        current_dictionary='v648_parcours_pedagogique.json',current_dictionary_archive='v648_dictionnaire.json',
        next_actions=['v648_multi_premiers','v648_cadres_transport','v648_sources_Q','v648_transport_non_borne'],
        local_certificate=dict(all_tests=True,maximum_support='1/2',mass_floor='1/250',R_floor='1/2000',head_dimension=80,head_form='bounded A_U minorant',parity_dimensions=[40,40],nonempty_prime_term=True,
            method='certified common operator; cardinal Gauss frame and global error',original_Q_strong_sources_certified=False),
        open=['joint multi-prime compensation','frames and operator error across supports','strong sources of original Q in the general method','unbounded support transport; historical branches/collisions/complex A'],
        global_sign_certified=False,maturity_levels_unchanged=True,pedagogy='40 fiches, cinq étapes,16outils explicités ; sources du minorant distinguées de celles de Q')
    write(D/'v648_etat_recherche.json',state)
    np=ROOT/'2_Methode/Navigateur/carte_navigation.json';nav=read(np)
    for c in nav['coups']:
        if c['id'] in ('v647_norme_commune','v647_sources_communes'):
            c['statut']='fait';c['appris']='V648 : norme commune et sources/queue du minorant certifiées à1/2 ; sources fortes de Q restent une autre obligation.'
    rows=[('v648_operateur_certifie','Certifier le même opérateur, sa tête et ses attaches','fait',STATUS,4),
        ('v648_multi_premiers','Construire le coût conjoint multi-premiers','ouvert','Conserver les phases des nouveaux premiers avec le décalage de masse correct, puis contrôler le même opérateur.',4),
        ('v648_cadres_transport','Transporter les cadres et les erreurs entre supports','ouvert','Réutiliser les cardinaux, leurs Grams et une erreur opératoire lorsque le support et les fréquences changent.',4),
        ('v648_sources_Q','Construire les sources fortes de Q dans la méthode générale','ouvert','Ne pas transférer automatiquement les sources de A vers Q ; contrôler le supplément positif non borné et sa norme de graphe.',5),
        ('v648_transport_non_borne','Établir une règle sur une famille non bornée','ouvert','Couvrir S_n→∞ avec nouveaux premiers, couplages et convergence ; la famille jusqu’à1/2 reste bornée.',5)]
    for id,title,status,text,cost in rows:
        if any(c['id']==id for c in nav['coups']):continue
        nav['coups'].append(dict(id=id,titre=title,statut=status,type='construction',question=text,these=text,cout=cost,version='V6.48',temoin=STATUS,document=STEM+'.pdf',
            gains={},probabilite=.5,probabilite_scope='Convention éditoriale historique, sans recalcul ni probabilité de RH.',prerequis=[],debloque=[],operateurs=[],croise=['RH'],repond_a=[],
            refutation='Échec d’un minorant : indéterminé pour Q. Une matrice finie sans erreur ne prouve pas le signe global.',
            prevision=dict(gains={},probabilite=.5,cout=cost,refutation='Les sources exactes de Q ne sont pas celles de son minorant.'),**({'appris':STATUS} if status=='fait' else {})))
    nav['bilan_v648']=dict(document=STEM+'.pdf',graphe=state['graph'],resultat=STATUS);write(np,nav)
    ip=ROOT/'2_Methode/Indicateur/indicateur_avancement.json';ind=read(ip)
    if not any(c['id']=='v648' for c in ind['etapes']):ind['etapes'].append(dict(id='v648',court='V6.48',versions='V6.48',jour='13 oct.',franchi=STATUS,
        pourquoi=dict(comprendre='Une même erreur globale certifie tête, sources et queue du minorant. Le cadre cardinal conserve exactement le Gram.',case='Norme à1/2 certifiée ; couverture non bornée et sources fortes de Q ouvertes.'),
        niveaux=dict(ind['etapes'][-1]['niveaux']),documents=[['Opérateur commun, tête et sources',STEM+'.pdf'],['Atelier de l’opérateur',state['graph']],['Dictionnaire courant',state['dictionary']]]))
    write(ip,ind)
    sp=ROOT/'2_Methode/Sources/sources.json';sources=read(sp)
    for s in sources:
        if s['cle'] in ('CC21','NIS10'):
            if '73' not in s.setdefault('docs',[]):s['docs'].append('73')
        if s['cle']=='NIS10':
            note=' V648 : DLMF3.5(v),18.3,18.9.15 et18.14.1 relus pour Gauss, Legendre et bornes de dérivées ; portée utilisée explicitement dans le document73.'
            if note.strip() not in s['ce_qui_a_ete_verifie']:s['ce_qui_a_ete_verifie']+=note
    write(sp,sources)
    mp=ROOT/'2_Methode/Matrice/matrice_theories.json';mat=read(mp);mat['version']='V6.48'
    for c in mat['noeuds']:
        if c['id']=='WEIL':
            note=' V648 : opérateur commun certifié jusqu’à1/2 ; tête/sources/queue du minorant assemblées. Sources fortes de Q et transport non borné restent ouverts.'
            if note.strip() not in c.get('apport_note',''):c['apport_note']=c.get('apport_note','')+note
            if '73' not in c.setdefault('docs',[]):c['docs'].append('73')
    write(mp,mat)
    port=ROOT/'2_Methode/Portail/build_portail.py'
    patch(port,"current_path = ROOT / '3_Preuves_et_calculs/data/v647_etat_recherche.json'","current_path = ROOT / '3_Preuves_et_calculs/data/v648_etat_recherche.json'\n    if not current_path.exists():current_path=ROOT/'3_Preuves_et_calculs/data/v647_etat_recherche.json'")
    patch(port,'Les 72 documents ; concentration V6.47 et certificat jusqu’à3/8 ; dictionnaire progressif et modèles historiques conservés.','Les 73 documents ; opérateur commun V6.48 et certificat jusqu’à1/2 ;40fiches progressives et16outils avec usages.')
    t=port.read_text()
    if '("Opérateur commun certifié",' not in t:t=t.replace('        ("Lego des concentrations",','        ("Opérateur commun certifié", "1_Presentation/73_OPERATEUR_COMMUN.html", "Tête, sources et queue du minorant ; tous tests jusqu’à1/2 ; double raccord exécuté."),\n        ("Opérateur, tête et sources", "1_Presentation/'+STEM+'.pdf", "Document73 : huit lemmes, Gauss, erreurs, Bareiss et Schur certifié."),\n        ("Lego des concentrations",',1)
    port.write_text(t)
    nb=ROOT/'2_Methode/Navigateur/build_navigateur.py'
    patch(nb,"    if carte.get('bilan_v647'):","    if carte.get('bilan_v648'):\n        phase='<section class=\"sheet\"><h2>V6.48 : opérateur commun certifié</h2><p>'+carte['bilan_v648']['resultat']+'</p><p><a href=\"73_OPERATEUR_COMMUN.html\">Tête, sources et queue</a> · <a href=\"'+carte['bilan_v648']['document']+'\">Huit lemmes et budgets</a></p></section>'\n    elif carte.get('bilan_v647'):")
    atlas=ROOT/'2_Methode/Outils/build_v638_atlas.py'
    patch(atlas,"    if registry.get('version')=='V6.47':","    if registry.get('version')=='V6.48':\n        body=body.replace('<header>','<section><h2>V6.48 : opérateur commun certifié</h2><p><a href=\"73_OPERATEUR_COMMUN.html\">Tous tests jusqu’à1/2 ; tête, sources et queue du minorant</a> · <a href=\"69_LANGUE_DES_PASSAGES.html\">Dictionnaire courant</a>. Multi-premiers, sources fortes de Q et couverture non bornée ouverts.</p></section><header>',1)\n        body=body.replace('Comparer les suites de travaux','Modèle documentaire de référence V6.42')\n        body=body.replace('data/v642_decisions.json','data/v648_decisions.json')\n    elif registry.get('version')=='V6.47':")
    b644=ROOT/'2_Methode/Outils/build_v644.py'
    patch(b644,"def interactive():\n    pedagogy=ROOT/'2_Methode/Outils/build_v647_pedagogy.py'","def interactive():\n    pedagogy=ROOT/'2_Methode/Outils/build_v648_pedagogy.py'\n    if pedagogy.exists() and (D/'v648_dictionnaire.json').exists():\n        module('pedagogy648current',pedagogy).build();return\n    pedagogy=ROOT/'2_Methode/Outils/build_v647_pedagogy.py'")
    vp=ROOT/'VERSION.txt';old=vp.read_text(encoding='utf-8-sig')
    if not old.startswith('Programme Riemann — V6.48'):vp.write_text('Programme Riemann — V6.48\nDate:2026-10-13\n'+STATUS+'\n\nHistorique conservé :\n'+old,encoding='utf-8-sig')
    patch(ROOT/'CITATION.cff','version 6.47','version 6.48');patch(ROOT/'CITATION.cff','version: "6.47"','version: "6.48"')
    rp=ROOT/'README.md';t=rp.read_text(encoding='utf-8-sig')
    section='## V6.48 - Opérateur commun, tête, sources et queue (document73)\n\n'+STATUS+'\n\nOuvrir `1_Presentation/73_OPERATEUR_COMMUN.html`. Le calcul intervalle couvre Gauss, ondes et moments ; Bareiss prouve les plafonds matriciels. Les erreurs d’opérateur assemblent la queue et les sources du minorant. Le dictionnaire courant compte40fiches en cinq étapes et16outils avec usages. Le diagnostic ponctuel reste séparé. Les anciennes données et éditions scientifiques sont conservées.\n\n'
    if '## V6.48 -' not in t:t=section+t
    rp.write_text(t,encoding='utf-8-sig')
def finish():
    for rel in ['Sources/build_sources.py','Matrice/build_matrice.py','Indicateur/build_indicateur.py','Navigateur/build_navigateur.py','Figures/build_figures.py','Portail/build_portail.py']:
        subprocess.run([sys.executable,str(ROOT/'2_Methode'/rel)],check=True,stdout=subprocess.DEVNULL)
    bi=module('nav648finish',ROOT/'2_Methode/Indicateur/build_indicateur.py')
    for rel in ['00_Carte_des_idees.html']+['1_Presentation/'+x for x in ['65_GRAPHE_DES_PASSAGES.html','66_GRAPHE_DES_CERTIFICATS.html','67_GRAPHE_DES_PONTS.html','70_PONT_ARITHMETIQUE.html','71_LEGO_REUTILISABLE.html','72_CONCENTRATION_PROJETEE.html']]:
        p=ROOT/rel;t=p.read_text(encoding='utf-8-sig');prefix='' if p.parent==ROOT else '../';target='1_Presentation/73_OPERATEUR_COMMUN.html' if not prefix else '73_OPERATEUR_COMMUN.html'
        old_ratio='Number(a[0])/(a.length===2?Number(a[1]):1)'
        if old_ratio in t:
            t=t.replace(old_ratio,'rationalDisplay(String(x))')
            if 'function rationalDisplay' not in t:t=t.replace('<script>','<script>'+(ROOT/'2_Methode/Outils/rational_display.js').read_text(),1)
        if not prefix:t=t.replace('Version 6.47.','Version 6.48.').replace('programme Riemann V6.47','programme Riemann V6.48')
        t=re.sub(r'<nav class=[\'\"]topnav[\'\"].*?</nav>',bi.topnav('carte' if not prefix else 'graphe',prefix),t,count=1,flags=re.S)
        t=re.sub(r'<p class="guard" data-current="v647">.*?</p>','',t,flags=re.S)
        banner='<p class="guard" data-current="v648"><a href="'+target+'">État courant V6.48 : tous tests jusqu’à1/2 ; tête, sources et queue du minorant certifiées.</a> Cette page conserve son analyse historique.</p>'
        if 'data-current="v648"' not in t:t=t.replace('</header>','</header>'+banner,1) if '</header>' in t else t.replace('<main>','<main>'+banner,1)
        p.write_text(t,encoding='utf-8-sig' if not prefix else 'utf-8')
    registry=read(D/'v647_decisions.json');registry.update(version='V6.48',coverage=dict(presentation_documents=73,numbers=list(range(1,74))),corpus_base='V6.48 ; données et éditions scientifiques historiques conservées')
    registry['documents'].append(dict(numero=73,id='doc73',titre='Opérateur commun : tête, sources et queue certifiées',etat_anterieur='V647 : norme commune à1/2 exploratoire ; certificat complet limité à3/8.',
        question='Peut-on certifier l’opérateur infini et trois blocs avec la même approximation ?',action='Cadre cardinal Gauss80, ondes en intervalles, poids, erreurs et plafonds Bareiss ; Schur du minorant assemblé.',
        resultat=STATUS,statut='certificat_analytique_et_numerique_local_complet',nature='certificat_analytique_et_numerique_local_complet',consequences='Signe et contrats R sur0<S≤1/2 ; sources et queue du minorant certifiées.',
        limites='Famille bornée et un premier ; modèle binaire64 déclaré. Sources fortes de Q et transport non borné ouverts ; ni preuve formelle ni priorité.',
        sources=[dict(path='1_Presentation/'+STEM+'.md'),dict(path='3_Preuves_et_calculs/preuves/V648_OPERATEUR_COMMUN_CERTIFIE.md'),dict(path='3_Preuves_et_calculs/data/v648_common_certificate_resultats.json'),dict(path='3_Preuves_et_calculs/data/v648_common_operator_diagnostic.json')],
        formats_regroupes=['1_Presentation/'+STEM+ext for ext in ('.md','.pdf','.tex')]+['1_Presentation/73_OPERATEUR_COMMUN.html'],correctifs_ulterieurs=[],
        alternatives_documentees=['Taylor simple128 : budget trop large','Gauss cardinal80 : reste contrôlé','Nyström ponctuel : exploration, pas prémisse de précision'],
        prevision_et_apres_coup='Paramètres choisis après exploration, figés avant validation ; thèse et critique confrontées ; toutes les erreurs restent explicites.'))
    for row in registry['documents']:
        if row['numero']==69:row['correctifs_ulterieurs'].append('V648 :40fiches et16outils ; cadre cardinal, interpolation, erreur opératoire et sources du minorant. PDF69 reste historique.')
        if row['numero']==72:row['correctifs_ulterieurs'].append('V648 : norme commune et sources/queue du minorant certifiées à1/2 dans le document73 ; diagnostic V647 conservé comme historique.')
        for s in row.get('sources',[]):
            if isinstance(s,dict):s['sha256']=hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()
    write(D/'v648_decisions.json',registry)
    atlas=module('atlas648',ROOT/'2_Methode/Outils/build_v638_atlas.py');(P/'62_ATLAS_DES_DECISIONS_BELLMAN.html').write_text(atlas.html_atlas(registry,read(D/'v642_modele_bellman.json'),read(D/'v642_bellman_resultats.json')))
    print('V648 :73documents ; interfaces courantes et registres synchronisés ; signe global ouvert.')
def main():
    sys.path.insert(0,str(ROOT/'2_Methode/Outils'));metadata();module('build648',ROOT/'2_Methode/Outils/build_v648.py').main();finish()
if __name__=='__main__':main()
