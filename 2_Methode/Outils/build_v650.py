"""Publish the reconstructed V6.50 state without changing frozen certificates."""
from pathlib import Path
import json,sys,re,base64,hashlib,importlib.util,subprocess,copy

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'1_Presentation';D=ROOT/'3_Preuves_et_calculs/data'
STEM='75_RECUPERATION_TRANSPORT_ET_RH'
ACTIVE=['00_PORTAIL.html','00_Carte_des_idees.html','00_Liste_des_figures.html']+[
 '1_Presentation/'+n for n in ['31_INDICATEUR_D_AVANCEMENT.html','34_NAVIGATEUR_DE_RECHERCHE.html','44_MATRICE_DES_THEORIES.html',
 '62_ATLAS_DES_DECISIONS_BELLMAN.html','65_GRAPHE_DES_PASSAGES.html','66_GRAPHE_DES_CERTIFICATS.html','67_GRAPHE_DES_PONTS.html',
 '69_LANGUE_DES_PASSAGES.html','70_PONT_ARITHMETIQUE.html','71_LEGO_REUTILISABLE.html','72_CONCENTRATION_PROJETEE.html',
 '73_OPERATEUR_COMMUN.html','74_COMPENSATION_MULTI_PREMIERS.html']]


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def module(name,p):
    spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec)
    sys.modules[name]=m;spec.loader.exec_module(m);return m


def certificate():
    p=D/'v650_certificat_integral.json'
    return read(p) if p.exists() else {'continuous_positive_certificate':False}


def status():
    c=certificate()
    if c.get('continuous_positive_certificate'):
        return 'Transport exact et cœur dense ; certificat local complet jusqu’à S=11/20 dans le modèle arithmétique déclaré. Positivité pour tous les supports ouverte.'
    return 'Transport exact et cœur dense ; quadrature et plafond matriciel reconstruits. Relèvement continu à S=11/20 non achevé ; certificat conservé jusqu’à 1/2. Positivité globale ouverte.'


def report():
    text=(ROOT/'3_Preuves_et_calculs/preuves/V650_RECUPERATION_TRANSPORT_ET_RH.md').read_text(encoding='utf-8-sig')
    c=certificate()
    rows='| Poste | Valeur ou résultat | Portée |\n|---|---|---|\n'
    if c.get('continuous_positive_certificate'):
        rows+='| Support | 11/20 ; 640 nœuds ; 700 000 cellules | Tous les tests admissibles dans cette boîte |\n'
        for key,label in [('table_error_float','Table'),('weighted_quadrature_error_float','Quadrature pondérée'),
                          ('spatial_error_float','Interpolation spatiale'),('integrated_weight_error_float','Poids intégrés'),
                          ('assembly_error_float','Assemblage')]:
            rows+=f"| {label} | {c[key]:.10g} | Majorant du journal rationnel |\n"
        for a in c['parities']:
            rows+=f"| Relèvement {a['parity']} | {a['total_operator_error_float']:.10g} | Somme de toutes les erreurs de norme |\n"
        rows+=f"| Marge minimale | {c['mass_floor_lower_float']:.10g} | Minorant strict positif exact conservé dans le journal |\n"
        rows+='\n**Résultat exécuté.** Le certificat ferme les cinq obligations pour S = 11/20 dans son modèle arithmétique déclaré. Par inclusion des supports, il vaut aussi pour 0 < S <= 11/20. Les fonctions complexes sont couvertes par la séparation des deux parités et des parties réelle et imaginaire. Le résultat ne porte pas sur tous les supports et ne prouve pas RH.\n'
        text=text.replace('La positivité suit seulement si la réserve reste positive après **toutes**','La positivité suit seulement si la réserve reste positive après **toutes**')
        text=re.sub(r"Le prochain protocole utile a deux sorties concrètes : finir le relèvement\ncontinu du test 11/20 avec un budget fermé, et étudier la famille Q_r comme\nun seul problème d.opérateurs sur un domaine fixe\. Le second axe doit produire",'Le relèvement continu du test 11/20 est fermé dans cette version. Le prochain protocole étudie la famille Q_r comme un seul problème d’opérateurs sur un domaine fixe, et doit produire',text)
        text=text.replace('Le passage à un budget plus petit rend une certification locale possible à\nexaminer ; il ne démontre ni son achèvement ni une règle pour tous les S.','La somme du journal ferme ici la certification locale. Elle ne démontre pas une règle pour tous les S.')
    else:
        rows+='| Interpolation N = 512 | 49046,8125 environ | Borne inutilisable à T = 700 |\n'
        rows+='| Interpolation N = 640 | 7,56 × 10^(-57) environ | Borne ponctuelle analytique |\n'
        rows+='| Table + quadrature | 0,00026155 environ | Budget analytique partiel |\n'
        rows+='| Plafond pair de matrice | 19951609/8388608 | Matrice dyadique exacte, parent continu non validé |\n'
        rows+='| Réserve avant relèvement | 0,00031156 environ | Réserve descriptive, aucun nouveau signe certifié |\n'
    text=text.replace('{{RECONSTRUCTION_TABLE}}',rows)
    (P/(STEM+'.md')).write_text(text,encoding='utf-8-sig')


def metadata():
    c=certificate();state=copy.deepcopy(read(D/'v649_etat_recherche.json'))
    state.update(version='V6.50',result=status(),document=STEM+'.pdf',graph=STEM+'.html',
      recovered_base='V6.49',current_protocol='v650_protocole_global.json',original_post_v649_artifacts_found=False,
      reconstruction_origin='New executions and proofs after recovery; not recovered original V650 files',
      support_transport=dict(proved=True,operator='T_r=D_r P_r P_1^-1',group_law='T_rT_s=T_rs',sign_preserved=False,form_core_dense=True),
      next_actions=['v650_global_transported_sign','v650_scaled_cap_cost','v650_optional_Q_sources','v650_unbounded_exhaustion'],
      global_sign_certified=False,extended_positive_support_certificate=bool(c.get('continuous_positive_certificate')))
    if c.get('continuous_positive_certificate'):
        state['local_certificate'].update(maximum_support='11/20',mass_floor_exact=c['mass_floor_lower'],mass_floor='3/10000',R_floor='1/25001',
            method='integrated cell weights, certified Gauss640, common operator and validated congruence',
            head_dimension=640,parity_dimensions=[320,320],arithmetic_model=c['arithmetic_model'])
    state['open']=['global sign of the transported family for all r','effective nonbounded support coverage',
      'strong Q sources if that alternative is selected']
    write(D/'v650_etat_recherche.json',state)
    indpath=ROOT/'2_Methode/Indicateur/indicateur_avancement.json';ind=read(indpath)
    ind['etapes']=[x for x in ind['etapes'] if x['id']!='v650']
    ind['etapes'].append(dict(id='v650',court='V6.50',versions='V6.50',jour='13 oct.',franchi=status(),
      niveaux=copy.deepcopy(ind['etapes'][-1]['niveaux']),pourquoi=dict(comprendre='Le transport conserve support, moments et domaine d’énergie ; la loi de signe globale reste ouverte.',case='Distinguer certificat local et couverture de RH.'),
      documents=[['État et preuves',STEM+'.pdf'],['Fiche visuelle',STEM+'.html']]))
    write(indpath,ind)
    navpath=ROOT/'2_Methode/Navigateur/carte_navigation.json';nav=read(navpath)
    nav['bilan_v650']=dict(document=STEM+'.pdf',graphe=STEM+'.html',resultat=status(),
      cible='∀r>0, ∀f∈X_(1/2), Q_W(T_rf)≥0',current_state='v650_etat_recherche.json')
    write(navpath,nav)
    mp=ROOT/'2_Methode/Matrice/matrice_theories.json';mat=read(mp);mat['version']='V6.50'
    for e in mat['noeuds']:
        if e['id']=='WEIL':
            note=' V650 : deux moments compatibles avec RH ; transport exact T_r et cœur dense en norme R ; quantificateur tous supports ouvert.'
            if note.strip() not in e.get('apport_note',''):e['apport_note']=e.get('apport_note','')+note
            if '75' not in e.setdefault('docs',[]):e['docs'].append('75')
    write(mp,mat)
    sp=ROOT/'2_Methode/Sources/sources.json';sources=read(sp)
    if not any(x['cle']=='Zhu26' for x in sources):
        sources.append(dict(cle='Zhu26',auteurs='Xuefeng Zhu',annee=2026,
          titre='Weil positivity in compact windows: a finite reduction, certified two-sided bounds, and a Landau-Widom decay law',
          publication='arXiv:2608.24827v2, 2 septembre 2026',type='prépublication',lien='https://arxiv.org/html/2608.24827v2',
          statut='vérifié en ligne',ce_qui_a_ete_verifie='HTML v2 : normalisation, support L=S, domaine plus large, certificat annoncé à L=0.8, barrière propre aux majorants ponctuels. Calculs non reproduits indépendamment.',
          extrait='',usage_corpus='Comparer la portée et la priorité des essais locaux ; distinguer preuve annoncée et certificat exécuté ici.',
          verdict='non vérifiable',motifs=['Zhu26'],verifie_le='2026-10-13',correction='',
          conjectures=['RH'],dimensions=['situer'],interet='confronter',docs=['75'],cite_aussi=[]))
    sources=[row for row in sources if row['cle']!='ZHU26']
    for row in sources:
        if row['cle']=='Zhu26':
            note=' V650 : HTML v2 relu ; domaine sans contraintes comparé au noyau polaire du corpus, L=S. Certification à L=0.8 annoncée, non reproduite ici ; coût des majorants ponctuels identifié comme une limite de cette architecture.'
            if note.strip() not in row['ce_qui_a_ete_verifie']:row['ce_qui_a_ete_verifie']+=note
            row['verifie_le']='2026-10-13'
            if '75' not in row.setdefault('docs',[]):row['docs'].append('75')
    write(sp,sources)
    registry=copy.deepcopy(read(D/'v649_decisions.json'))
    registry.update(version='V6.50',coverage=dict(presentation_documents=75,numbers=list(range(1,76))))
    registry['documents'].append(dict(numero=75,id='doc75',titre='Après V6.49 : retrouver le travail et garder RH comme destination',
      etat_anterieur='ZIP V649 retrouvé ; aucun artefact original V650 retrouvé.',question='Que conserve le travail et quel pont mène encore à RH ?',
      action='Reconstruction contradictoire, budgets de calcul, action exacte de transport et densité.',resultat=status(),
      statut='transport_demontre_et_certificat_local' if c.get('continuous_positive_certificate') else 'transport_demontre_validation_locale_partielle',
      nature='reconstruction_et_preuves_internes',consequences='Famille de formes sur un espace fixe ; obligations explicites.',
      limites='Aucun signe global, aucune priorité bibliographique revendiquée.',
      sources=[dict(path='3_Preuves_et_calculs/preuves/V650_RECUPERATION_TRANSPORT_ET_RH.md'),dict(path='3_Preuves_et_calculs/src/support_transport.py')],
      formats_regroupes=['1_Presentation/'+STEM+e for e in ['.md','.tex','.pdf','.html']],correctifs_ulterieurs=[],
      alternatives_documentees=['Minorant borné','Sources fortes et Schur de Q','Structure positive globale'],prevision_et_apres_coup='Nouvelle reconstruction ; calculs originaux post49 non retrouvés.'))
    write(D/'v650_decisions.json',registry)


def dashboard():
    bi=module('ind650',ROOT/'2_Methode/Indicateur/build_indicateur.py');c=certificate()
    graphic=base64.b64encode((P/'75_CARTE_RH.png').read_bytes()).decode()
    local='jusqu’à 11/20' if c.get('continuous_positive_certificate') else 'jusqu’à 1/2'
    result='Le raccord continu à 0,55 est certifié dans le modèle arithmétique déclaré.' if c.get('continuous_positive_certificate') else 'Le plafond de la matrice finie est certifié ; le raccord à l’opérateur continu reste ouvert.'
    html='''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V6.50 · État du travail vers RH</title><style>
    :root{color-scheme:light;--ink:#152d3e;--muted:#516c80;--green:#21694d;--orange:#875800;--red:#923e4b}*{box-sizing:border-box}body{margin:0;background:#f5f8fa;color:var(--ink);font:17px/1.6 system-ui,sans-serif}main{max-width:1100px;margin:auto;padding:26px 20px 64px}h1{font-size:clamp(27px,5vw,43px);line-height:1.14}h2{font-size:24px;margin-top:0}p{max-width:80ch}a{color:#175d8b}.topnav{display:flex;gap:7px 17px;flex-wrap:wrap;font-size:13px;border-bottom:1px solid #bccbd6;padding-bottom:14px}.topnav a{text-decoration:none}section,.card{background:white;border:1px solid #d0dce4;border-radius:10px;padding:23px;margin-top:20px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}.cards .card{margin:0}.tag{font-size:12px;text-transform:uppercase;letter-spacing:.04em;font-weight:750}.green{color:var(--green)}.orange{color:var(--orange)}.red{color:var(--red)}.muted{color:var(--muted)}.actions{display:flex;gap:10px;flex-wrap:wrap}.actions a{padding:10px 15px;border:1px solid #175d8b;border-radius:7px;text-decoration:none}.actions a:first-child{background:#175d8b;color:white}img{display:block;max-width:100%;height:auto;margin:auto}table{width:100%;border-collapse:collapse;font-size:15px}th,td{text-align:left;vertical-align:top;padding:12px;border-bottom:1px solid #d4dfe7}th{background:#f0f5f8}.scroll{overflow-x:auto}summary{cursor:pointer;font-weight:650;padding:12px 0}details p{font-size:16px}.formula{padding:14px;background:#f1f6f9;font-size:20px;overflow-x:auto}.foot{font-size:13px;color:var(--muted)}@media print{.topnav,.actions{display:none}section{break-inside:avoid}body{font-size:12px}main{padding:0}}
    </style></head><body><main>'''+bi.topnav('etat','../')+'''
    <header><p class="muted">Programme Riemann · V6.50 · 13 octobre 2026</p><h1>Ce que nous faisons.<br>Ce que cela apporte à RH.</h1><p>La destination est la positivité de Weil pour chaque test compact admissible. Le travail actuel construit les traductions et les certificats nécessaires à cette affirmation.</p><div class="actions"><a href="https://chatgpt.com/api/library/files/libfile_e12b21a3a190819196641d18ac05665a/download">Télécharger le ZIP global courant</a><a href="'''+STEM+'''.pdf">Lire les preuves · PDF</a><a href="'''+STEM+'''.tex">Source LaTeX</a></div></header>
    <section><h2>Où en sommes-nous ?</h2><div class="cards"><div class="card"><span class="tag green">Récupéré</span><h3>V6.49 complète</h3><p>Le ZIP original et ses 1 259 entrées sont intacts. Aucun fichier original postérieur retrouvé ; cette suite est une reconstruction nouvelle.</p></div><div class="card"><span class="tag green">Démontré dans le dossier</span><h3>Transport des tests</h3><p>Nous changeons leur support en conservant les moments, avec des coûts de norme explicites et une loi de composition.</p></div><div class="card"><span class="tag red">Ouvert</span><h3>La portée globale</h3><p>Le certificat local porte '''+local+'''. Il faut démontrer le signe pour des supports arbitrairement grands. Aucune preuve de RH n’est obtenue.</p></div></div></section>
    <section><h2>La carte de la preuve</h2><img src="data:image/png;base64,'''+graphic+'''" alt="Deux branches : transport exact et certificats locaux. La loi de signe pour tous les supports reste ouverte avant RH."></section>
    <section><h2>Le nouveau pont, d’abord en mots</h2><p>Une graine fabrique une fonction qui annule les deux moments. Pour agrandir cette fonction, nous ajustons son moule pendant l’étirement. On retrouve ainsi un test autorisé dans la nouvelle boîte.</p><p>Cette règle compose les changements : agrandir par r puis par s produit exactement l’agrandissement par r×s. Elle construit aussi les approximations lisses nécessaires aux preuves de signe.</p><details><summary>Voir les symboles, puis leurs conditions</summary><div class="formula">T<sub>r</sub> = D<sub>r</sub> P<sub>r</sub> P<sub>1</sub><sup>−1</sup> ; T<sub>r</sub>T<sub>s</sub> = T<sub>rs</sub></div><p>P<sub>r</sub> est la dérivée seconde moins r²/4. D<sub>r</sub> étire avec le facteur qui conserve la masse L². L’inverse P<sub>1</sub> rend une graine compacte grâce aux deux moments nuls. Les lemmes du PDF établissent les domaines et les facteurs.</p><p><strong>Limite :</strong> cette traduction conserve les tests autorisés et contrôle leurs normes. Le signe de leur forme de Weil doit être prouvé séparément.</p></details></section>
    <section><h2>L’essai à 0,55</h2><p>'''+result+'''</p><p>Les corrections ont un usage concret : intégrer les cassures du poids, réduire la dette de queue et contrôler le plafond de la matrice par congruence. Les résultats exacts et le modèle arithmétique sont conservés dans le ZIP.</p><details><summary>Pourquoi une matrice positive ne suffit-elle pas ?</summary><p>Il faut une identité exacte, un domaine précis, une queue bornée, toutes les erreurs de discrétisation et d’arrondi encadrées, puis une réserve positive après leur somme. La valeur propre d’une matrice d’essai ne couvre pas à elle seule les fonctions absentes de cette matrice.</p></details></section>
    <section><h2>Le contrat qui ferait aboutir à RH</h2><div class="formula">Pour chaque r &gt; 0 et chaque f admissible : Q<sub>W</sub>(T<sub>r</sub>f) ≥ 0.</div><p>Le domaine de départ peut rester fixe. Les transformations sont désormais exactes ; la loi universelle de signe reste à établir. Une suite de supports démontrée non bornée suffit. Une marge strictement positive uniforme n’est pas requise.</p><div class="scroll"><table><tr><th>Porte</th><th>Ce qui sert</th><th>Ce qui porte encore le signe</th></tr><tr><td>Arithmétique</td><td>Phases et paiements conjoints</td><td>Corrélations sur toutes les directions admissibles</td></tr><tr><td>Tête et queue</td><td>Budgets et validation matricielle</td><td>Relèvement continu, puis coût sur une famille non bornée</td></tr><tr><td>Couplages</td><td>Minorants et Schur</td><td>Sources requises par la voie choisie</td></tr><tr><td>Couverture</td><td>Transport et cœur dense</td><td>Positivité pour chaque r</td></tr></table></div></section>
    <section><h2>Thèse, critique, suite</h2><p><strong>Thèse :</strong> le transport et les corrections numériques forment des briques réutilisables qui rendent les obligations vérifiables.</p><p><strong>Critique :</strong> un support supplémentaire ne produit pas une preuve globale. La garde de queue actuelle devient coûteuse ; il faut contrôler les formes et les phases sur les tests plutôt que grossir les calculs sans loi nouvelle.</p><p><strong>Suite :</strong> étudier la famille transportée sur un même espace, en cherchant une décomposition positive ou une estimation arithmétique valable pour tout r. Bellman organise les contrats et Schur élimine des variables ; ils n’attribuent aucun signe sans ses hypothèses.</p><p><a href="https://alainconnes.org/wp-content/uploads/Selecta.pdf">Connes-Consani : critère polaire, appendice C</a> · <a href="https://arxiv.org/html/2608.24827v2">Zhu, prépublication 2026 : comparaison de portée</a></p></section><p class="foot">Lecture progressive : cette fiche donne le sens et la carte ; le PDF porte les domaines et démonstrations ; les programmes et journaux portent la reproduction. Les dates et statuts sont explicites. Les données historiques ne sont pas promues en preuve globale.</p></main></body></html>'''
    (P/(STEM+'.html')).write_text(html,encoding='utf-8')


def finish():
    bi_path=ROOT/'2_Methode/Indicateur/build_indicateur.py';t=bi_path.read_text()
    entry='("etat", "État du travail", "1_Presentation/'+STEM+'.html")'
    if entry not in t:t=t.replace('pages = [','pages = ['+entry+', ',1)
    bi_path.write_text(t)
    dashboard()
    for rel in ['Sources/build_sources.py','Matrice/build_matrice.py','Indicateur/build_indicateur.py','Navigateur/build_navigateur.py','Figures/build_figures.py','Portail/build_portail.py']:
        subprocess.run([sys.executable,str(ROOT/'2_Methode'/rel)],check=True,stdout=subprocess.DEVNULL)
    bi=module('ind650final',bi_path)
    generated={'00_PORTAIL.html','00_Liste_des_figures.html','1_Presentation/31_INDICATEUR_D_AVANCEMENT.html','1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html','1_Presentation/44_MATRICE_DES_THEORIES.html'}
    for rel in ACTIVE:
        if rel in generated:continue
        p=ROOT/rel;t=p.read_text(encoding='utf-8-sig');prefix='' if p.parent==ROOT else '../'
        t=re.sub(r'<nav class=[\'\"]topnav[\'\"].*?</nav>',bi.topnav('','../' if prefix else ''),t,count=1,flags=re.S)
        t=re.sub(r'<aside data-current="v650".*?</aside>','',t,flags=re.S)
        href=('' if prefix else '1_Presentation/')+STEM+'.html'
        banner='<aside data-current="v650" style="margin:16px 0;padding:14px;border:1px solid #97b0c0;background:#eef5f9;color:#172b3c"><strong>État courant V6.50.</strong> '+status()+' <a href="'+href+'">Carte, preuves et dernier ZIP</a>. Les résultats datés de cette page conservent leur portée.</aside>'
        pos=t.find('</nav>')
        if pos<0:raise ValueError('top navigation missing: '+rel)
        t=t[:pos+6]+banner+t[pos+6:]
        p.write_text(t,encoding='utf-8')
    carte=ROOT/'00_Carte_des_idees.html';carte.write_text(carte.read_text(encoding='utf-8-sig').replace('Version 6.49.','Version 6.50.'),encoding='utf-8')
    dashboard()
    vp=ROOT/'VERSION.txt';v=vp.read_text(encoding='utf-8-sig')
    if not v.startswith('Programme Riemann — V6.50'):vp.write_text('Programme Riemann — V6.50\n\n'+status()+'\n\n'+v,encoding='utf-8')
    rp=ROOT/'README.md';t=rp.read_text(encoding='utf-8-sig');mark='<!-- CURRENT_V650 -->'
    block=mark+'\n## V6.50 - Récupération, transport et destination RH\n\n'+status()+'\n\n[Ouvrir la fiche visuelle](1_Presentation/'+STEM+'.html), [preuves PDF](1_Presentation/'+STEM+'.pdf), [LaTeX](1_Presentation/'+STEM+'.tex).\n\nLe corpus V6.49 est conservé ; les calculs suivant cette version sont nouvellement reconstruits, sans prétendre récupérer leurs sorties originales. Aucun pourcentage de progression vers RH n’est attribué.\n<!-- END_CURRENT_V650 -->\n\n'
    commands='\nReproduction du nouveau certificat :\n\n~~~bash\npython 3_Preuves_et_calculs/scripts/verify_v650_certificate.py\npython 3_Preuves_et_calculs/scripts/run_v650_certificate.py\n~~~\n\nLe premier vérifie les témoins archivés et les budgets ; le second reconstruit tout le certificat dans un nouveau dossier. Dépendances : `requirements.txt`.\n'
    block=block.replace('<!-- END_CURRENT_V650 -->',commands+'<!-- END_CURRENT_V650 -->')
    t=re.sub(r'<!-- CURRENT_V650 -->.*?<!-- END_CURRENT_V650 -->\s*','',t,flags=re.S)
    rp.write_text(block+t,encoding='utf-8-sig')
    # VERSION is part of the portal header; generate it after its final update.
    subprocess.run([sys.executable,str(ROOT/'2_Methode/Portail/build_portail.py')],check=True,stdout=subprocess.DEVNULL)
    write(D/'v650_active_pages.json',ACTIVE+['1_Presentation/'+STEM+'.html'])
    registry=read(D/'v650_decisions.json')
    for row in registry['documents']:
        for src in row.get('sources',[]):
            if isinstance(src,dict):src['sha256']=hashlib.sha256((ROOT/src['path']).read_bytes()).hexdigest()
    write(D/'v650_decisions.json',registry)
    inventory=module('index650',ROOT/'2_Methode/Outils/build_v644_dictionary.py').code_inventory()
    if inventory['parse_errors']:raise ValueError(inventory['parse_errors'])
    write(D/'v650_index_fonctions.json',inventory)


def main():
    metadata();report();finish()
    print(status())


if __name__=='__main__':main()
