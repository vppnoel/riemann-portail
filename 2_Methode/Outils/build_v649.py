"""Build the executed multi-prime bridge, article and current corpus views."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,csv,base64,re,hashlib,subprocess,math
from integrate_v647 import module,read,write,patch as _patch
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'1_Presentation';D=ROOT/'3_Preuves_et_calculs/data'
STEM='74_COMPENSATION_MULTI_PREMIERS'
STATUS='Coût multi-premiers exact ; paiement joint D/V certifié avec multiplicité. À S=1 : alpha<0,796 contre somme séparée>1,24. Positivité complète inchangée jusqu’à1/2 ; extension à0,55 exploratoire seulement. Transport des supports et sources fortes de Q ouverts.'

def patch(p,a,b):
    if b not in p.read_text(encoding='utf-8-sig'):_patch(p,a,b)

def upper_decimal(s):
    f=F(s);q=10**9;n=-(-(f*q).numerator//(f*q).denominator)
    return format(n/q,'.9f')

def inventory():
    x=read(D/('v649_dictionnaire.json' if (D/'v649_dictionnaire.json').exists() else 'v648_dictionnaire.json'));x.update(version='V6.49',current_article='Document74 ; compensation multi-premiers',pedagogical_lessons=43)
    write(D/'v649_dictionnaire.json',x)
    x=module('index649',ROOT/'2_Methode/Outils/build_v644_dictionary.py').code_inventory();assert not x['parse_errors']
    write(D/'v649_index_fonctions.json',x)
    with (D/'v649_index_fonctions.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['path','line','name','kind','signature','docstring','explanation_status']);w.writeheader();w.writerows(x['entries'])

def figure():
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    sys.path.insert(0,str(ROOT/'3_Preuves_et_calculs/src'))
    import multi_prime_compensation as c
    import prime_centered_bridge as b
    b.setup(240);S=.7;rs=c.active_powers(F(7,10));xs=np.linspace(-S+1e-6,S-1e-6,1401)
    density=np.zeros_like(xs)
    for r in rs:
        d=math.log(r['q']);w=math.log(r['p'])/math.sqrt(r['q'])
        density+=w*((xs<=S-d).astype(int)+(xs>=d-S).astype(int))
    def J(d):r=np.exp(-d/2);return np.arctanh(r)+np.arctan(r)
    V=J(S-xs)+J(S+xs);a=float(F(c.joint_edge_payment(F(7,10))['alpha_upper']))
    fig,ax=plt.subplots(2,1,figsize=(10,6),sharex=True)
    ax[0].plot(xs,V,label='V : coût minimal de bord',color='#486b58');ax[0].step(xs,density,label='D : attaches de 2, 3 et 4',where='mid',color='#b46c22');ax[0].set_ylim(0,8);ax[0].legend();ax[0].set_ylabel('Densité sans dimension')
    ax[1].plot(xs,density/V,color='#38547b',label='Rapport local D/V');ax[1].axhline(a,color='#b46c22',linestyle='--',label='Majorant certifié alpha < 0,353');ax[1].legend();ax[1].set_ylabel('Part relative de l’énergie');ax[1].set_xlabel('Position x dans le support [-0,7 ; 0,7]')
    fig.suptitle('Paiement conjoint : conserver les lieux et les recouvrements',fontsize=14)
    fig.text(.5,.005,'Courbes illustratives ; le supremum est certifié par segments et intervalles, indépendamment de la grille.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.03,1,.96));fig.savefig(P/'74_PAIEMENT_CONJOINT.png',dpi=180);fig.savefig(P/'74_PAIEMENT_CONJOINT.svg');plt.close(fig)

def report():
    payment=read(D/'v649_joint_payment_resultats.json');diag=read(D/'v649_multi_prime_diagnostic.json')
    table='| S | Termes actifs | Paiement joint, majorant | Somme séparée, majorant |\n|---|---|---|---|\n'
    for r in payment['supports']:
        powers=', '.join(map(str,r['active_q'])) if len(r['active_q'])<10 else str(len(r['active_q']))+' puissances'
        table+='| '+r['S']+' | '+powers+' | '+upper_decimal(r['alpha_upper'])+' | '+upper_decimal(r['separate_alpha_sum_upper'])+' |\n'
    table+='\nMajorants décimaux arrondis vers le haut. Les fractions et intervalles binaires du journal sont les valeurs de calcul.\n'
    dt='| S | U=9 | U=9,5 | U=10 |\n|---|---|---|---|\n'
    for r in diag['supports']:
        dt+='| '+r['S']+' | '+' | '.join(format(x['resolutions'][-1]['margin'],'+.9f') for x in r['cases'])+' |\n'
    text=(ROOT/'3_Preuves_et_calculs/preuves/V649_COMPENSATION_MULTI_PREMIERS.md').read_text(encoding='utf-8-sig').replace('{{PAYMENT_TABLE}}',table).replace('{{DIAGNOSTIC_TABLE}}',dt)
    (P/(STEM+'.md')).write_text(text,encoding='utf-8-sig')
    module('pdf649',ROOT/'2_Methode/Outils/build_v644.py').pdf(STEM)

def metadata():
    state=read(D/'v648_etat_recherche.json');state.update(version='V6.49',result=STATUS,document=STEM+'.pdf',graph=STEM+'.html',current_dictionary='v649_parcours_pedagogique.json',current_dictionary_archive='v649_dictionnaire.json',
        next_actions=['v649_frequency_split','v648_cadres_transport','v648_sources_Q','v648_transport_non_borne'],
        current_multi_prime_payment='v649_joint_payment_resultats.json',extended_positive_support_certificate=False,
        open=['pay remaining mass after joint arithmetic compensation','certified low/high frequency head and Schur','transport moments and forms in R across supports','original Q sources and unbounded coverage'],
        pedagogy='43 fiches progressives, cinq étapes ;19outils avec usages ; paiement relatif distinct du signe global')
    write(D/'v649_etat_recherche.json',state)
    navpath=ROOT/'2_Methode/Navigateur/carte_navigation.json';nav=read(navpath)
    for r in nav['coups']:
        if r['id']=='v648_multi_premiers':r['appris']=STATUS
    if not any(x['id']=='v649_frequency_split' for x in nav['coups']):
        source=next(x for x in nav['coups'] if x['id']=='v648_cadres_transport');x=json.loads(json.dumps(source));x.update(id='v649_frequency_split',titre='Certifier le découpage basse et haute fréquence',question='Traiter la haute fréquence par sa petite action sur la tête, puis Schur, au lieu d’une tête brute.',these='Conserver le même opérateur et payer sa queue en norme et dans les sources croisées.',version='V6.49',document=STEM+'.pdf',temoin=STATUS);nav['coups'].append(x)
    nav['bilan_v649']=dict(document=STEM+'.pdf',graphe=STEM+'.html',resultat=STATUS);write(navpath,nav)
    ip=ROOT/'2_Methode/Indicateur/indicateur_avancement.json';ind=read(ip)
    if not any(x['id']=='v649' for x in ind['etapes']):ind['etapes'].append(dict(id='v649',court='V6.49',versions='V6.49',jour='13 oct.',franchi=STATUS,niveaux=dict(ind['etapes'][-1]['niveaux']),pourquoi=dict(comprendre='Une enveloppe commune paie une seule fois l’énergie ; les nouveaux seuils sont petits dans R mais pas L².',case='Paiement relatif certifié ; pas d’extension du théorème positif.'),documents=[['Compensation multi-premiers',STEM+'.pdf'],['Atelier des paiements',STEM+'.html'],['Dictionnaire courant','69_LANGUE_DES_PASSAGES.html']]))
    write(ip,ind)
    sp=ROOT/'2_Methode/Sources/sources.json';sources=read(sp)
    for x in sources:
        if x['cle']=='NIS10':
            if '74' not in x.setdefault('docs',[]):x['docs'].append('74')
            note=' V649 : DLMF5.11.2 relu pour la croissance logarithmique de la digamma ; le paiement joint est démontré directement.'
            if note.strip() not in x['ce_qui_a_ete_verifie']:x['ce_qui_a_ete_verifie']+=note
    write(sp,sources)
    mp=ROOT/'2_Methode/Matrice/matrice_theories.json';mat=read(mp);mat['version']='V6.49'
    for x in mat['noeuds']:
        if x['id']=='WEIL':
            note=' V649 : coût conjoint multi-premiers exact et paiement D/V certifié ; positivité complète toujours limitée à1/2, diagnostic0,55 non certifié.'
            if note.strip() not in x.get('apport_note',''):x['apport_note']=x.get('apport_note','')+note
            if '74' not in x.setdefault('docs',[]):x['docs'].append('74')
    write(mp,mat)
    navbuilder=ROOT/'2_Methode/Indicateur/build_indicateur.py'
    t=navbuilder.read_text();entry='("compensation", "Compensation multi-premiers", "1_Presentation/'+STEM+'.html")'
    while t.count(entry)>1:t=t.replace(entry+', ','',1)
    navbuilder.write_text(t)
    patch(navbuilder,'("figures", "Figures", "00_Liste_des_figures.html")','("compensation", "Compensation multi-premiers", "1_Presentation/'+STEM+'.html"), ("figures", "Figures", "00_Liste_des_figures.html")')
    port=ROOT/'2_Methode/Portail/build_portail.py'
    patch(port,"current_path = ROOT / '3_Preuves_et_calculs/data/v648_etat_recherche.json'","current_path = ROOT / '3_Preuves_et_calculs/data/v649_etat_recherche.json'\n    if not current_path.exists():current_path=ROOT/'3_Preuves_et_calculs/data/v648_etat_recherche.json'")
    t=port.read_text();token='        ("Opérateur commun certifié",'
    if '("Compensation multi-premiers",' not in t:t=t.replace(token,'        ("Compensation multi-premiers", "1_Presentation/'+STEM+'.html", "Paiement joint certifié ; saut L² et petite dette en R ; extension positive ouverte."),\n        ("Compensation et preuves", "1_Presentation/'+STEM+'.pdf", "Document74 : huit lemmes, comparaisons exécutées et prochain raccord."),\n'+token,1)
    t=t.replace('Les 73 documents ; opérateur commun V6.48 et certificat jusqu’à1/2 ;40fiches progressives et16outils avec usages.','Les 74 documents ; paiement multi-premiers V6.49 ; certificat positif toujours jusqu’à1/2 ;43fiches et19outils avec usages.');port.write_text(t)
    nb=ROOT/'2_Methode/Navigateur/build_navigateur.py'
    patch(nb,"    if carte.get('bilan_v648'):","    if carte.get('bilan_v649'):\n        phase='<section class=\"sheet\"><h2>V6.49 : compensation multi-premiers</h2><p>'+carte['bilan_v649']['resultat']+'</p><p><a href=\"'+carte['bilan_v649']['graphe']+'\">Paiement conjoint</a> · <a href=\"'+carte['bilan_v649']['document']+'\">Preuves et limites</a></p></section>'\n    elif carte.get('bilan_v648'):")
    vp=ROOT/'VERSION.txt';old=vp.read_text(encoding='utf-8-sig')
    if not old.startswith('Programme Riemann — V6.49'):vp.write_text('Programme Riemann — V6.49\nDate:2026-10-13\n'+STATUS+'\n\nHistorique conservé :\n'+old,encoding='utf-8-sig')
    patch(ROOT/'CITATION.cff','version 6.48','version 6.49');patch(ROOT/'CITATION.cff','version: "6.48"','version: "6.49"')
    rp=ROOT/'README.md';t=rp.read_text(encoding='utf-8-sig');section='## V6.49 - Compensation multi-premiers (document74)\n\n'+STATUS+'\n\nOuvrir `1_Presentation/'+STEM+'.html`. Le journal intervalle certifie les paiements relatifs ; les diagnostics de norme sont séparés et non certifiés. Les anciennes données scientifiques sont conservées.\n\n'
    if '## V6.49 -' not in t:rp.write_text(section+t,encoding='utf-8-sig')
    for name in ['test_v644_domain_language.py','test_v645_prime_centered_bridge.py','test_v646_certificate_lego.py']:
        p=ROOT/'3_Preuves_et_calculs/tests'/name;t=p.read_text()
        for file in ['decisions','index_fonctions','etat_recherche']:
            for quote in ["'",'"']:
                old=quote+'v648_'+file+'.json'+quote+' if (D/'+quote+'v648_'+file+'.json'+quote+').exists() else '
                if old in t and quote+'v649_'+file+'.json'+quote+' if ' not in t:
                    t=t.replace(old,quote+'v649_'+file+'.json'+quote+' if (D/'+quote+'v649_'+file+'.json'+quote+').exists() else '+old)
        old="current='v648' if (D/'v648_decisions.json').exists() else "
        if old in t and "current='v649'" not in t:
            t=t.replace(old,"current='v649' if (D/'v649_decisions.json').exists() else 'v648' if (D/'v648_decisions.json').exists() else ")
        p.write_text(t)

def interface():
    data=read(D/'v649_joint_payment_resultats.json');diag=read(D/'v649_multi_prime_diagnostic.json');bi=module('nav649ui',ROOT/'2_Methode/Indicateur/build_indicateur.py')
    css='body{background:#f5f6ef;color:#20392f;font:17px/1.65 system-ui;margin:0}main{max-width:1150px;margin:auto;padding:24px}.topnav{display:flex;flex-wrap:wrap;gap:12px}header,.card{padding:24px;border:1px solid #cbd8c8;border-radius:12px;background:white;margin:20px 0}header{background:#163f34;color:white}a{color:#286344}header a{color:#d9efda}select,button{font:inherit;padding:10px}table{border-collapse:collapse;width:100%}td,th{padding:10px;border-bottom:1px solid #d0dacd;text-align:left}.guard{background:#fff0d8;padding:18px}.good{background:#e2efdf;padding:18px}.row{display:flex;flex-wrap:wrap;gap:22px}.math{font-size:22px;padding:15px;overflow:auto}.figure{max-width:100%;height:auto}.muted{font-size:14px}code{overflow-wrap:anywhere}'
    figure=base64.b64encode((P/'74_PAIEMENT_CONJOINT.png').read_bytes()).decode()
    body='<header><h1>Compensation multi-premiers</h1><p>V6.49 · document74. Paiement relatif certifié ; positivité complète limitée à S≤1/2.</p><p><a href="'+STEM+'.pdf">Preuves · PDF</a> · <a href="'+STEM+'.tex">Source LaTeX</a> · <a href="69_LANGUE_DES_PASSAGES.html">Comprendre les briques</a></p></header><section class="card"><h2>Une même énergie, toutes les attaches</h2><p>Chaque premier lit une rencontre entre deux copies de la fonction. Les bandes qui se recouvrent sont comptées deux fois. On additionne les factures locales avant de chercher leur rapport maximal au coût de bord.</p><div class="math">|Q<sub>pr</sub>(f)| ≤ α · E(f), &nbsp; α = sup D(x)/V(x)</div><label>Support déjà calculé <select id="support"></select></label><div id="payment"></div><p class="guard">Alpha est le supremum d’une enveloppe suffisante. Il ne mesure ni la norme optimale des corrélations, ni le signe de la forme complète. La masse soustraite reste à payer.</p><img class="figure" src="data:image/png;base64,'+figure+'" alt="Densité des attaches et coût de bord à S=0,7"></section><section class="card"><h2>Le même opérateur, avec les phases conservées</h2><p>La phase de p puissance m est la phase de p répétée m fois ; le poids reste log(p)/racine(p puissance m). On conserve les phases dans le coût commun b, puis on soustrait la constante C.</p><label>Plafond exploratoire <select id="cap"><option>9</option><option>9.5</option><option selected>10</option></select></label><div id="diagnostic"></div><p class="guard">Ces valeurs sont exploratoires. Une marge flottante positive et deux résolutions proches ne certifient pas la norme de l’opérateur infini.</p></section><section class="card"><h2>Au seuil : deux métriques, deux comportements</h2><p>Une bande très étroite peut concentrer une fonction de masse1 : son couplage ne devient pas petit en L². Mais rester près du bord coûte de l’énergie. Relativement à E et R, la nouvelle attache devient petite, au taux logarithmique.</p><div class="math">|Q<sub>q</sub>(f)| ≤ c<sub>q</sub> / [J(δ)+J(log q)] · E(f)</div><p>Il faut encore transporter la forme de base et les moments sur le nouveau support avant d’employer cette petite dette.</p></section><section class="card"><h2>Prochain raccord</h2><p>Découper le même opérateur en basse et haute fréquence, certifier la petite action de la haute fréquence sur la tête, puis ses sources et le Schur. Cette étape doit éviter une tête brute couvrant toutes les fréquences.</p><p><a href="../3_Preuves_et_calculs/data/v649_joint_payment_resultats.json">Paiements certifiés · journal</a> · <a href="../3_Preuves_et_calculs/data/v649_multi_prime_diagnostic.json">Diagnostic distinct · journal</a></p></section>'
    js=r'''const DATA=JSON.parse(document.getElementById('payment-data').textContent),DIAG=JSON.parse(document.getElementById('diagnostic-data').textContent),el=id=>document.getElementById(id),num=x=>rationalDisplay(String(x));
el('support').innerHTML=DATA.supports.map(r=>'<option value="'+r.S+'"'+(r.S==='1'?' selected':'')+'>'+r.S+'</option>').join('');
function render(){const r=DATA.supports.find(x=>x.S===el('support').value);if(!r){el('payment').textContent='Aucun certificat pour ce support';return;}const a=num(r.alpha_upper),s=num(r.separate_alpha_sum_upper);el('payment').innerHTML='<p>Puissances actives : '+r.active_q.join(', ')+'</p><table><tr><th>Enveloppe jointe, majorant</th><th>Somme séparée, majorant</th></tr><tr><td>'+a.toPrecision(10)+'</td><td>'+s.toPrecision(10)+'</td></tr></table><p class="'+(a<1?'good':'guard')+'">'+(a<1?'Réserve d’énergie positive dans cette borne suffisante. Le signe de Q reste à établir.':'Paiement suffisant trop grand pour conserver une réserve d’énergie ; aucune conclusion sur le signe de Q.')+'</p>';const d=DIAG.supports.find(x=>x.S===r.S),c=d&&d.cases.find(x=>x.U===Number(el('cap').value));el('diagnostic').innerHTML=c?'<table><tr><th>Parité</th><th>Marge exploratoire</th></tr>'+c.resolutions.slice(-1)[0].parity.map(p=>'<tr><td>'+p.parity+'</td><td>'+p.margin.toPrecision(10)+'</td></tr>').join('')+'</table><p class="muted">Deux résolutions ; stabilité seulement. Aucune extension du certificat positif.</p>':'<p>Pas de diagnostic enregistré pour ce support et ce plafond.</p>';}
el('support').addEventListener('change',render);el('cap').addEventListener('change',render);render();window.multiPrimeWorkshop={render};'''
    html='<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V6.49 · Compensation multi-premiers</title><style>'+css+'</style></head><body><main>'+bi.topnav('compensation','../')+body+'</main><script id="payment-data" type="application/json">'+json.dumps(data,ensure_ascii=False)+'</script><script id="diagnostic-data" type="application/json">'+json.dumps(diag,ensure_ascii=False)+'</script><script>'+(ROOT/'2_Methode/Outils/rational_display.js').read_text()+js+'</script></body></html>'
    (P/(STEM+'.html')).write_text(html)

def finish():
    for rel in ['Sources/build_sources.py','Matrice/build_matrice.py','Indicateur/build_indicateur.py','Navigateur/build_navigateur.py','Figures/build_figures.py','Portail/build_portail.py']:
        subprocess.run([sys.executable,str(ROOT/'2_Methode'/rel)],check=True,stdout=subprocess.DEVNULL)
    bi=module('nav649finish',ROOT/'2_Methode/Indicateur/build_indicateur.py')
    active=['00_Carte_des_idees.html']+['1_Presentation/'+n for n in ['65_GRAPHE_DES_PASSAGES.html','66_GRAPHE_DES_CERTIFICATS.html','67_GRAPHE_DES_PONTS.html','70_PONT_ARITHMETIQUE.html','71_LEGO_REUTILISABLE.html','72_CONCENTRATION_PROJETEE.html','73_OPERATEUR_COMMUN.html']]
    for rel in active:
        p=ROOT/rel;t=p.read_text(encoding='utf-8-sig');prefix='' if p.parent==ROOT else '../'
        t=re.sub(r'<nav class=[\'\"]topnav[\'\"].*?</nav>',bi.topnav('carte' if not prefix else 'graphe',prefix),t,count=1,flags=re.S)
        t=t.replace('Version 6.48.','Version 6.49.').replace('programme Riemann V6.48','programme Riemann V6.49')
        t=re.sub(r'<p class="guard" data-current="v648">.*?</p>','',t,flags=re.S)
        target=('1_Presentation/' if not prefix else '')+STEM+'.html';banner='<p class="guard" data-current="v649"><a href="'+target+'">V6.49 : paiement multi-premiers certifié ; positivité complète toujours limitée à1/2.</a> Analyse de cette page conservée.</p>'
        if 'data-current="v649"' not in t:t=t.replace('</header>','</header>'+banner,1) if '</header>' in t else t.replace('<main>','<main>'+banner,1)
        p.write_text(t,encoding='utf-8-sig' if not prefix else 'utf-8')
    registry=read(D/'v648_decisions.json');registry.update(version='V6.49',coverage=dict(presentation_documents=74,numbers=list(range(1,75))),corpus_base='V6.49 ; anciennes données scientifiques conservées')
    registry['documents'].append(dict(numero=74,id='doc74',titre='Compensation multi-premiers : un paiement commun',etat_anterieur='V648 : positif jusqu’à1/2, coût multi-premiers et transport ouverts.',question='Peut-on payer plusieurs attaches avec une même énergie ?',action='Identité de phases, densité avec multiplicité, supremum par segments en intervalles ; diagnostic commun séparé.',resultat=STATUS,statut='paiement_relatif_certifie_positivite_ouverte',nature='paiement_relatif_certifie_positivite_ouverte',consequences='Pont énergétique au nouveau seuil et gain conjoint sur les paiements séparés.',limites='Pas de signe global ni extension positive ; alpha est une enveloppe, la masse et le transport restent à payer.',sources=[dict(path='1_Presentation/'+STEM+'.md'),dict(path='3_Preuves_et_calculs/preuves/V649_COMPENSATION_MULTI_PREMIERS.md'),dict(path='3_Preuves_et_calculs/src/multi_prime_compensation.py'),dict(path='3_Preuves_et_calculs/data/v649_joint_payment_resultats.json'),dict(path='3_Preuves_et_calculs/data/v649_multi_prime_diagnostic.json')],formats_regroupes=['1_Presentation/'+STEM+ext for ext in ['.md','.tex','.pdf','.html']],correctifs_ulterieurs=[],alternatives_documentees=['Paiements séparés : perte de localisation','Petit déplacement en L² : obstruction au seuil','Paiement relatif en E/R : démontré','Basse/haute fréquence et Schur : à certifier'],prevision_et_apres_coup='Deux raisonnements constructif/critique ; garde fermée des seuils corrigée avant validation ; diagnostics flottants explicitement distincts.'))
    for row in registry['documents']:
        if row['numero']==69:row['correctifs_ulterieurs'].append('V649 :43fiches et19outils ; phases, multiplicité et paiement conjoint. PDF69 reste historique.')
        for source in row.get('sources',[]):
            if isinstance(source,dict):source['sha256']=hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest()
    write(D/'v649_decisions.json',registry)
    atlas=module('atlas649',ROOT/'2_Methode/Outils/build_v638_atlas.py');t=atlas.html_atlas(registry,read(D/'v642_modele_bellman.json'),read(D/'v642_bellman_resultats.json'))
    t=t.replace('<header>','<section><h2>V6.49 : compensation multi-premiers</h2><p>'+STATUS+'</p><p><a href="'+STEM+'.html">Paiement conjoint et obligations suivantes</a></p></section><header>',1).replace('data/v642_decisions.json','data/v649_decisions.json').replace('Comparer les suites de travaux','Modèle documentaire de référence V6.42')
    (P/'62_ATLAS_DES_DECISIONS_BELLMAN.html').write_text(t)
    print('V649 :74documents ;43fiches ;19outils ; certificat positif inchangé, paiement relatif exécuté.')

def main():
    sys.path.insert(0,str(ROOT/'2_Methode/Outils'));metadata();inventory();figure();report();module('ped649',ROOT/'2_Methode/Outils/build_v649_pedagogy.py').build();interface();finish()
if __name__=='__main__':main()
