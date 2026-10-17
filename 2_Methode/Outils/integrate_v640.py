"""Synchronize the active corpus views after the prospective V6.40 experiment."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
D=ROOT/'3_Preuves_et_calculs/data'
P=ROOT/'1_Presentation'

def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    result=read(D/'v640_resultats.json')
    assert result['n_roots_recrossed']==24
    status='12 couples exacts : 8 détections plus précoces et 4 plus tardives à D élevé ; 24 racines recoupées à 80/110 chiffres de travail. Le signe se regroupe par ancre. Aucun ordre causal ou premier zéro certifié.'
    state={'version':'V6.40','completed_bellman_actions':['v13_contraintes','v13_comparaison'],
        'proven':'Exact constraint feasibility from V6.39; R3 dominance and conditional root velocity lemmas.',
        'document':'64_COMPARAISON_EXACTE_V13.pdf','result':status,
        'next_action':'v640_branches_v13','scope':'Numerical first deficit tranches; no certified earlier absence or causality.',
        'next_action_is_in_historical_bellman_model':False}
    write(D/'v640_etat_recherche.json',state)
    nav_path=ROOT/'2_Methode/Navigateur/carte_navigation.json';nav=read(nav_path)
    for c in nav['coups']:
        if c['id']=='v13_premier_coefficient_complexe_fixe':
            c.update(statut='fait',version='V6.40',document=state['document'],appris=status,
                resultat_prevision_v640='Majorité stricte annoncée de 7/12 atteinte : 8/12 ; quatre signes contraires conservés.',
                limites_v640='Rayons dépendants ; pas de causalité, d’ordre uniforme ni d’absence antérieure certifiée.',
                debloque=['v640_branches_v13'])
            c['appris_etape_preparatoire']=c['appris_etape_preparatoire'].replace('qui reste à exécuter.','qui est exécutée en V6.40 ; cette note reste le bilan antérieur.')
    if not any(c['id']=='v640_branches_v13' for c in nav['coups']):
        nav['coups'].append({'id':'v640_branches_v13','titre':'V13 : suivre les branches et expliquer le signe par ancre',
            'statut':'ouvert','type':'calcul','cout':1.0,
            'question':'Le signe opposé de χ1 vient-il du déplacement d’une branche, d’une collision ou d’un changement de branche première ?',
            'these':'La continuation et la vitesse implicite conditionnelle distinguent ces trois mécanismes dans les familles exactes.',
            'temoin':'Ancres χ1 et χ5, mêmes familles ; conserver branches perdues, dérivée petite et collisions ; vérifier le partenaire fonctionnel.',
            'refutation':'Identité de branche non suivie, racine multiple ou différences non résolues : conserver un bilan indéterminé.',
            'operateurs':["Le Point d'Euler",'Fermeture multiplicative'],
            'prerequis':['v13_premier_coefficient_complexe_fixe'],'debloque':[],
            'repond_a':['Distinguer mouvement de branche et ordre de détection','Expliquer le regroupement du signe par ancre','Tester la formule de vitesse locale'],
            'gains':{'comprendre':1},'probabilite':0.6,
            'origine':'Priorité éditoriale après le bilan V6.40 ; estimation conventionnelle, pas probabilité d’un théorème.',
            'prevision':{'these':'Identifier ou documenter l’échec de suivi du mécanisme local ; protocole de continuation à figer avant calcul.',
                'gains':{'comprendre':1},'probabilite':0.6,'cout':1.0}})
    write(nav_path,nav)
    ip=ROOT/'2_Methode/Indicateur/indicateur_avancement.json';ind=read(ip)
    if not any(e['id']=='v640' for e in ind['etapes']):
        ind['etapes'].append({'id':'v640','court':'V6.40','jour':'12 oct.','versions':'V6.40',
            'niveaux':dict(ind['etapes'][-1]['niveaux']),'franchi':status,
            'pourquoi':{'voir':'Comptages stables, six témoins et 24 recoupements ; mesure finie non certifiée par intervalles.',
                'comprendre':'Le signe dépend de l’ancre ; continuation des branches encore à faire.',
                'demontrer':'Bord droit rationnel et vitesse locale conditionnelle ; relecture interne seulement.',
                'case':'Aucun mécanisme de positivité globale pour ζ ajouté.'},
            'documents':[['Comparaison exacte V13',state['document']],['Source LaTeX','64_COMPARAISON_EXACTE_V13.tex']]})
    write(ip,ind)
    mp=ROOT/'2_Methode/Matrice/matrice_theories.json';matrix=read(mp);matrix['version']='V6.40'
    for n in matrix['noeuds']:
        if n['id']=='ARCH':
            if '64' not in n['docs']:n['docs'].append('64')
            if 'V6.40 :' not in n['apport_note']:n['apport_note']+=' V6.40 : '+status+' Suite : continuation des branches dans les mêmes familles exactes.'
    write(mp,matrix)
    cp=ROOT/'00_Carte_des_idees.html';s=cp.read_text(encoding='utf-8-sig')
    if 'V6.40 : comparaison exacte V13' not in s:
        panel='<section class="panel"><h2>V6.40 : comparaison exacte V13</h2><p>'+status+'</p><p>Suite : suivre les branches simples et comparer leur vitesse ; collisions et pertes de branches à conserver.</p><p><a href="1_Presentation/64_COMPARAISON_EXACTE_V13.pdf">Bilan PDF et lemmes</a> · <a href="1_Presentation/64_COMPARAISON_EXACTE_V13.tex">Source LaTeX</a></p></section>'
        s=s.replace('</section><footer>','</section>'+panel+'<footer>')
    s=s.replace('programme Riemann v6.18.','programme Riemann V6.40 (base graphique V6.18).')
    s=s.replace('Version 6.39.','Version 6.40.')
    cp.write_text(s,encoding='utf-8-sig')
    vp=ROOT/'VERSION.txt';text=vp.read_text(encoding='utf-8-sig')
    if not text.startswith('Programme Riemann — V6.40'):
        vp.write_text('Programme Riemann — V6.40\nDate: 2026-10-12\nStatut: comparaison exacte V13 exécutée\n- '+status+'\n- Suite : suivre les branches ; niveaux RH conservés.\n\nHistorique conservé :\n'+text,encoding='utf-8-sig')
    cf=ROOT/'CITATION.cff';s=cf.read_text().replace('version 6.39','version 6.40').replace('version: "6.39"','version: "6.40"');cf.write_text(s)
    rp=ROOT/'README.md';s=rp.read_text(encoding='utf-8-sig').replace('version 6.39','version 6.40',1)
    section='''## V6.40 — Comparaison exacte V13 (document 64)

**12 couples inchangés : 8 détections plus précoces, 4 plus tardives à D élevé.** Le signe dépend de l’ancre : χ1 contraire, χ3 et χ5 favorables. Comptages stables aux trois pas, six témoins d’Euler, 24 racines recoupées à 80/110 chiffres de travail. Le rapport 8/12 concerne le plan figé ; ni causalité, ni première ordonnée exacte, ni absence antérieure certifiée.

- [Bilan PDF, tableaux, deux lemmes et suite](1_Presentation/64_COMPARAISON_EXACTE_V13.pdf).
- [Source LaTeX](1_Presentation/64_COMPARAISON_EXACTE_V13.tex) et [données complètes](3_Preuves_et_calculs/data/v640_resultats.json).
- [Protocole prospectif](3_Preuves_et_calculs/data/prevision_v640_comparaison.md).
- [Lemmes et prochaine expérience](3_Preuves_et_calculs/preuves/LEMMES_ET_SUITE_V640.md).
- [Atlas courant des 64 documents](1_Presentation/62_ATLAS_DES_DECISIONS_BELLMAN.html) ; les modèles et PDF historiques sont conservés.
- Suite prioritaire : suivre les branches de racines dans les familles exactes et expliquer l’inversion par ancre.

~~~bash
python 3_Preuves_et_calculs/scripts/run_v640_comparaison.py --run
python 3_Preuves_et_calculs/scripts/run_v640_comparaison.py --roots
python 2_Methode/Outils/build_v640_document.py
~~~

Les lanceurs refusent d’écraser les sorties prospectives. Pour rejouer, déplacer les anciennes sorties sur une copie, en conservant manifeste et protocole ; voir document 64.

'''
    if '## V6.40 — Comparaison exacte' not in s:s=s.replace('## V6.39 - Contraintes exactes',section+'## V6.39 - Contraintes exactes')
    s=s.replace('# 233 tests','# 239 tests')
    rp.write_text(s,encoding='utf-8-sig')
    registry=read(D/'v638_decisions.json');registry['version']='V6.40';registry['corpus_base']='V6.40 ; notices historiques et nouveaux résultats conservés';registry['coverage']={'presentation_documents':64,'numbers':list(range(1,65))}
    extras=[(62,'62_ATLAS_DES_DECISIONS_BELLMAN','Reprise du corpus et Bellman','Un corpus dispersé sans état de décision commun.','Comment choisir une suite de livrables sous un budget ?','Registre, lemmes de planification finie, modèle et contrôle indépendant.','Modèle documentaire de neuf actions ; le calcul est conditionnel aux livrables.','modele_documentaire','Coûts et poids conventionnels ; aucune probabilité de découverte ni distance RH.'),
        (63,'63_CONTRAINTES_EXACTES_V13','Contraintes exactes V13','Les couples V6.37 conservent A seulement à tolérance.','D varie-t-il à A complexe, ancre et rayon exacts ?','Construire des directions du noyau ; prouver une cubique non nulle.','Faisabilité pour chaque ancre et 0<r<pi/4 à A=cos(r)z_i ; 12 couples figés.','lemme_demontre','Pas pour tout A arbitraire ; aucune causalité ou étude de zéros dans cette phase.'),
        (64,'64_COMPARAISON_EXACTE_V13','Comparaison exacte V13','Douze couples analytiques disponibles avant comptage.','La majorité précoce survit-elle sous contraintes exactes ?','Compter trois grilles, six témoins et recouper tous les 24 membres.',status,'mesure_numerique','Dépendance des rayons, signe par ancre ; pas d’ordre uniforme, causalité ou absence antérieure certifiée.')]
    for no,stem,title,before,question,action,outcome,kind,limits in extras:
        path=P/(stem+'.md');relative=str(path.relative_to(ROOT))
        registry['documents'].append({'numero':no,'id':f'doc{no}','titre':title,'etat_anterieur':before,'question':question,
            'action':action,'resultat':outcome,'statut':kind,'nature':kind,'consequences':'Bilan courant et prochaine action explicités dans le portail.',
            'limites':limits,'sources':[{'path':relative,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}],
            'formats_regroupes':[relative,str(path.with_suffix('.pdf').relative_to(ROOT))],
            'correctifs_ulterieurs':[],'alternatives_documentees':[],
            'prevision_et_apres_coup':'Sources historiques et bilans datés séparés ; aucun état mental reconstruit.'})
    for record in registry['documents']:
        if record['numero'] in (30,58,61,63):record['correctifs_ulterieurs'].append({'version':'V6.40','texte':status,'source':'1_Presentation/64_COMPARAISON_EXACTE_V13.md'})
    write(D/'v640_decisions.json',registry)
    spec=importlib.util.spec_from_file_location('v640_atlas',ROOT/'2_Methode/Outils/build_v638_atlas.py');atlas=importlib.util.module_from_spec(spec);spec.loader.exec_module(atlas)
    (P/'62_ATLAS_DES_DECISIONS_BELLMAN.html').write_text(atlas.html_atlas(registry,read(D/'v638_modele_bellman.json'),read(D/'v638_bellman_resultats.json')))
    for script in ('2_Methode/Sources/build_sources.py','2_Methode/Matrice/build_matrice.py',
                   '2_Methode/Indicateur/build_indicateur.py','2_Methode/Navigateur/build_navigateur.py',
                   '2_Methode/Figures/build_figures.py','2_Methode/Portail/build_portail.py'):
        subprocess.run([sys.executable,str(ROOT/script)],check=True)
    print('V640 active views synchronized; historical files retained')

if __name__=='__main__':main()
