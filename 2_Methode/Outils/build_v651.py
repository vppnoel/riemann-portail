"""Publier la reconstruction globale sans modifier les certificats historiques."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / '1_Presentation'
D = ROOT / '3_Preuves_et_calculs/data'
STEM = '76_RECONSTRUIRE_LA_PISTE_GLOBALE_DE_WEIL'
RESULT = ('Compensation signée reprise ; dette duale et deux grammaires couvrantes '
          'démontrées dans le dossier. Loi globale du signe de Weil ouverte. '
          'Certificat local conservé jusqu’à S=11/20.')

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m

def state_and_protocol():
    state = copy.deepcopy(read(D/'v650_etat_recherche.json'))
    state.update(version='V6.51', date='2026-10-13', result=RESULT,
                 global_sign_certified=False, maturity_levels_unchanged=True,
                 current_protocol='v651_protocole_global.json',
                 reconstruction_origin='Traces 67–74 + new public proofs; not recovered hidden reasoning',
                 next_actions=[
                     'Écrire les noyaux de paquets depuis la fluctuation signée et tous les premiers actifs.',
                     'Construire une borne certifiée de la norme duale restreinte des couplages.',
                     'Chercher une loi des dettes de Schur pour toutes les tailles et tous les pas.',
                     'Rendre constructive la couverture par deux filtres, sans confondre coût et signe.'])
    state['new_auxiliary_proofs'] = {
        'dual_debt': True, 'Toeplitz_coverage': True, 'two_prime_filter_coverage': True,
        'weighted_global_continuity': True, 'boundary_envelope_global_failure': True,
        'new_universal_sign_law': False, 'quantitative_two_filter_decomposition': False}
    write(D/'v651_etat_recherche.json', state)
    protocol = dict(version='V6.51', origin='explicit reconstruction from traces',
        target='Weil positivity for every compact polar test', RH_proved=False,
        logic='AND sign + coverage within a route; OR between covering grammars',
        routes=[
            dict(id='toeplitz', coverage_proved=True,
                 quantifiers='all n,m>=1 and all N>=0',
                 sign_obligation='T_(1/n,1/m,N) is positive semidefinite',
                 guards=['full arithmetic form','complex coefficients','all coupling terms']),
            dict(id='two_filters', coverage_proved=True, quantitative_coverage=False,
                 quantifiers='all compact smooth complex g2,g3',
                 sign_obligation='Q_W(B2*g2+B3*g3)>=0',
                 guards=['all primes in Q_W','mixed B2/B3 couplings','weighted continuity']),
            dict(id='exhaustion', coverage_implication_proved=True,
                 quantifiers='S_j tends to infinity; all tests in each box',
                 sign_obligation='Q_W is nonnegative in every box')],
        actions=state['next_actions'],
        refused_inferences=['positive constructor implies positive Weil',
                            'positive finite sample implies universal sign',
                            'negative minorant implies negative complete Q',
                            'absolute boundary payment remains globally sufficient',
                            'RH-equivalent prime error bound may be assumed'],
        classifications=dict(traced=[67,68,70,71,72,73,74], posterior=[75],
                             reconstructed=[76]))
    write(D/'v651_protocole_global.json', protocol)

def configure():
    path = ROOT/'2_Methode/Indicateur/build_indicateur.py'
    t = path.read_text(encoding='utf-8-sig')
    entry = '("piste", "Piste globale", "1_Presentation/'+STEM+'.html"), '
    if entry not in t:
        t = t.replace('pages = [', 'pages = ['+entry, 1)
    t = t.replace('data/v650_etat_recherche.json','data/v651_etat_recherche.json')
    t = t.replace('href = prefix + "1_Presentation/75_RECUPERATION_TRANSPORT_ET_RH.html"',
                  'href = prefix + "1_Presentation/'+STEM+'.html"')
    t = t.replace('data-current="v650"','data-current="v651"').replace('État courant V6.50.','État courant V6.51.')
    path.write_text(t,encoding='utf-8')
    ind_path = ROOT/'2_Methode/Indicateur/indicateur_avancement.json'
    ind = read(ind_path)
    stage = copy.deepcopy(ind['etapes'][-1])
    stage.update(id='v651', court='V6.51', versions='V6.51', jour='13 oct.',
                 franchi=RESULT, documents=[['Reconstruction en cinq étapes',STEM+'.pdf'],
                                            ['Piste globale',STEM+'.html']])
    stage['pourquoi'] = dict(comprendre='Distinguer la loi de signe de sa couverture ; rouvrir les corrélations signées.',
                            case='Couvertures auxiliaires établies ; aucun signe global obtenu.')
    if ind['etapes'][-1]['id']=='v651': ind['etapes'][-1]=stage
    else: ind['etapes'].append(stage)
    write(ind_path,ind)
    vp = ROOT/'VERSION.txt'
    text = vp.read_text(encoding='utf-8-sig')
    if not text.startswith('Programme Riemann — V6.51'):
        vp.write_text('Programme Riemann — V6.51\n\n'+RESULT+'\n\n'+text,encoding='utf-8')
    cff = ROOT/'CITATION.cff'
    t=cff.read_text().replace('version: 6.50','version: 6.51')
    t=t.replace('version: "6.50"','version: "6.51"').replace('Programme Riemann — V6.50','Programme Riemann — V6.51')
    cff.write_text(t)
    for name in ['test_v644_domain_language.py','test_v645_prime_centered_bridge.py','test_v646_certificate_lego.py']:
        path=ROOT/'3_Preuves_et_calculs/tests'/name
        t=path.read_text()
        if "'v651_decisions.json'" not in t:
            t=t.replace("'v650_decisions.json' if (D/'v650_decisions.json').exists()",
                        "'v651_decisions.json' if (D/'v651_decisions.json').exists() else 'v650_decisions.json' if (D/'v650_decisions.json').exists()")
            t=t.replace("current='v650' if (D/'v650_decisions.json').exists()",
                        "current='v651' if (D/'v651_decisions.json').exists() else 'v650' if (D/'v650_decisions.json').exists()")
            t=t.replace("'v650_index_fonctions.json' if (D/'v650_index_fonctions.json').exists()",
                        "'v651_index_fonctions.json' if (D/'v651_index_fonctions.json').exists() else 'v650_index_fonctions.json' if (D/'v650_index_fonctions.json').exists()")
        path.write_text(t)
    rp=ROOT/'README.md'
    t=rp.read_text(encoding='utf-8-sig')
    mark='<!-- CURRENT_V651 -->'
    if mark not in t:
        block=(mark+'\n## V6.51 - Reprendre la piste globale de Weil\n\n'+RESULT+
               '\n\n[Piste globale](1_Presentation/'+STEM+'.html), [PDF](1_Presentation/'+STEM+
               '.pdf), [LaTeX](1_Presentation/'+STEM+'.tex).\n\n'
               'Reproduire les fermetures de méthodes (jamais une négativité de Q complet) :\n\n'
               '    python3 3_Preuves_et_calculs/scripts/v651_verifier_pistes_globales.py '
               '--corpus . --output /tmp/v651_resultats.json\n\n')
        pos=t.find('<!-- CURRENT_V650 -->')
        if pos<0:pos=t.find('\n\n')+2
        t=t[:pos]+block+t[pos:]
        rp.write_text(t,encoding='utf-8-sig')

def views():
    bi=module('ind651',ROOT/'2_Methode/Indicateur/build_indicateur.py')
    style=P/'v651_style.css'
    style.write_text('body{max-width:1000px;margin:auto;padding:28px 24px;color:#153044;'
                    'font:17px/1.65 system-ui,sans-serif;background:#f7f9fb}h1,h2{line-height:1.2}'
                    'h1{font-size:36px}h2{margin-top:2em}a{color:#17608c}.topnav{display:flex;flex-wrap:wrap;'
                    'gap:8px 16px;font-size:13px;border-bottom:1px solid #b4c7d5;padding-bottom:12px}'
                    'img{max-width:100%;height:auto}math[display=block]{overflow-x:auto;'
                    'padding:16px;font-size:1.1em}table{border-collapse:collapse;width:100%;font-size:15px}'
                    'td,th{padding:10px;text-align:left;vertical-align:top;border-bottom:1px solid #cbd9e3}'
                    'th{background:#eaf1f6}pre,code{overflow-wrap:anywhere}nav#TOC{font-size:15px}',encoding='utf-8')
    before=P/'v651_nav.html'
    before.write_text(bi.topnav('piste','../')+
        '<p><a href="https://chatgpt.com/api/library/files/libfile_e12b21a3a190819196641d18ac05665a/download">'
        'Télécharger le ZIP global courant</a> · <a href="'+STEM+'.pdf">PDF</a> · '
        '<a href="'+STEM+'.tex">LaTeX</a></p>',encoding='utf-8')
    subprocess.run(['pandoc',STEM+'.md','-s','-f','markdown+tex_math_single_backslash',
                    '--mathml','--embed-resources','--toc','--toc-depth=2','--css',style.name,
                    '--include-before-body',before.name,'-o',STEM+'.html'],cwd=P,check=True)
    generated={'00_PORTAIL.html','00_Liste_des_figures.html',
               '1_Presentation/31_INDICATEUR_D_AVANCEMENT.html',
               '1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html',
               '1_Presentation/44_MATRICE_DES_THEORIES.html'}
    for rel in ['Sources/build_sources.py','Matrice/build_matrice.py','Indicateur/build_indicateur.py',
                'Navigateur/build_navigateur.py','Figures/build_figures.py','Portail/build_portail.py']:
        subprocess.run([sys.executable,str(ROOT/'2_Methode'/rel)],check=True,stdout=subprocess.DEVNULL)
    old=module('b650views',ROOT/'2_Methode/Outils/build_v650.py')
    active=old.ACTIVE+['1_Presentation/75_RECUPERATION_TRANSPORT_ET_RH.html']
    for rel in active:
        if rel in generated:continue
        path=ROOT/rel
        t=path.read_text(encoding='utf-8-sig')
        t=re.sub(r'<aside data-current="v65[01]".*?</aside>','',t,flags=re.S)
        prefix='' if path.parent==ROOT else '../'
        t=re.sub(r'<nav class=[\'"]topnav[\'"].*?</nav>',bi.topnav('',prefix),t,count=1,flags=re.S)
        path.write_text(t,encoding='utf-8')
    carte=ROOT/'00_Carte_des_idees.html'
    carte.write_text(carte.read_text(encoding='utf-8-sig').replace('Version 6.50.','Version 6.51.'),encoding='utf-8')
    write(D/'v651_pages_actives.json',dict(pages=active+['1_Presentation/'+STEM+'.html']))
    proof=ROOT/'3_Preuves_et_calculs/preuves/V651_RECONSTRUCTION_GLOBALE_WEIL.md'
    proof.write_text((P/(STEM+'.md')).read_text(encoding='utf-8-sig').replace(
                    '](76_CARTE_PISTES_GLOBALES.png)','](../../1_Presentation/76_CARTE_PISTES_GLOBALES.png)'),
                    encoding='utf-8-sig')
    for folder in [P,ROOT/'2_Methode']:
        for path in folder.rglob('*.md'):
            if not path.read_bytes().startswith(b'\xef\xbb\xbf'):
                path.write_text(path.read_text(encoding='utf-8-sig'),encoding='utf-8-sig')

def registry():
    registry=copy.deepcopy(read(D/'v650_decisions.json'))
    registry.update(version='V6.51',date='2026-10-13',
                    nature='Reconstruction critique globale ; preuves auxiliaires, signe global ouvert')
    registry['coverage']=dict(presentation_documents=76,numbers=list(range(1,77)))
    registry['documents'].append(dict(numero=76,id='DOC076',titre='Reconstruire la piste globale de Weil',
        statut='preuves_auxiliaires_et_obligation_globale_ouverte',
        nature='Traces distinguées des reconstructions',
        consequences='Dette duale et deux grammaires couvrantes ; enveloppe de sortie globale réfutée.',
        limites='Aucune loi de signe globale ; aucune priorité historique revendiquée.',
        sources=[dict(path='1_Presentation/'+STEM+'.md'),
                 dict(path='3_Preuves_et_calculs/preuves/V651_RECONSTRUCTION_GLOBALE_WEIL.md'),
                 dict(path='3_Preuves_et_calculs/scripts/v651_verifier_pistes_globales.py')],
        formats_regroupes=['1_Presentation/'+STEM+ext for ext in ['.md','.tex','.pdf','.html']],
        correctifs_ulterieurs=[],alternatives_documentees=['Toeplitz','Deux filtres','Exhaustion'],
        prevision_et_apres_coup='Reconstruction nouvelle, pas récupération de raisonnements internes.'))
    for row in registry['documents']:
        for source in row.get('sources',[]):
            if isinstance(source,dict):
                source['sha256']=hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest()
    write(D/'v651_decisions.json',registry)
    inventory=module('index651',ROOT/'2_Methode/Outils/build_v644_dictionary.py').code_inventory()
    if inventory['parse_errors']:raise ValueError(inventory['parse_errors'])
    write(D/'v651_index_fonctions.json',inventory)

def main():
    state_and_protocol()
    configure()
    views()
    registry()
    print('V6.51 : 76 documents ; 18 pages actives ; signe global ouvert.')

if __name__=='__main__':
    main()
