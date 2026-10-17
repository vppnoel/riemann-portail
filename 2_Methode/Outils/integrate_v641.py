"""Synchronize current V641 views, retaining historical states and publications."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
D=ROOT/'3_Preuves_et_calculs/data';P=ROOT/'1_Presentation'
STEM='65_FIBRES_PLIS_ET_POSITIVITE'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def run(relative,*args):subprocess.run([sys.executable,str(ROOT/relative),*args],check=True)

def bellman_figure(model,result):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    actions=[a for a in model['actions'] if a['id'] not in result['completed']]
    values=np.array([[row['in_all_optimal_portfolios'][a['id']] for row in result['results']] for a in actions])
    fig,ax=plt.subplots(figsize=(10.1,5.7));ax.imshow(values,cmap='Blues',vmin=0,vmax=243,aspect='auto')
    ax.set_yticks(range(len(actions)),[a['label'] for a in actions],fontsize=9)
    ax.set_xticks(range(4),[str(r['budget'])+' H restants' for r in result['results']])
    for i in range(len(actions)):
        for j in range(4):ax.text(j,i,f'{values[i,j]}/243',ha='center',va='center',fontsize=9,color='white' if values[i,j]>150 else '#20415b')
    ax.set_title('Modèle V6.41 : neuf actions restantes, trois actions V13 déjà achevées\nPrésence dans tous les portefeuilles optimaux ; fréquences sans interprétation probabiliste',fontsize=11,pad=14)
    fig.tight_layout();fig.savefig(P/'65_Bellman_sensibilite.png',dpi=175);plt.close(fig)

def main():
    folds=read(D/'v641_collisions.json');blocks=read(D/'v641_blocs_paires.json')
    assert folds['n_accepted']==20 and blocks['n_accepted_blocks']==18 and blocks['n_roots_recrossed']==24
    status='A prescrit : ellipse de faisabilité et fibres ; D constant à A=0 ; jets, 20 candidats de plis recoupés, six attribués, 18 blocs et 24 racines. Pont arithmétique global ouvert ; une perte coarse conservée.'
    state=dict(version='V6.41',completed_bellman_actions=['v13_contraintes','v13_comparaison','v13_passages'],document=STEM+'.pdf',graph='65_GRAPHE_DES_PASSAGES.html',result=status,proven='Affine sphere geometry, defect constancy and contraction, conditional folds and two-zero moments, admissible test construction, density, finite-prefix obstruction and bounded Schur lemma.',next_actions=['certifier_bloc_local','audit_positivite_uniforme'],scope='Numerical zero results, local conditional proofs and global contracts; no interval zero certificates, exhaustion or RH proof.',current_bellman_model='v641_modele_bellman.json',maturity_levels_unchanged=True)
    write(D/'v641_etat_recherche.json',state)
    navpath=ROOT/'2_Methode/Navigateur/carte_navigation.json';nav=read(navpath)
    for coup in nav['coups']:
        if coup['id']=='v640_branches_v13':coup.update(statut='fait',version='V6.41',document=STEM+'.pdf',appris=status,debloque=['certifier_bloc_local','v641_deploiement_A_fixe','audit_positivite_uniforme'],limites_v641='Pertes conservées, attribution par proximité, réalité et isolation non certifiées ; A varie dans les suivis radiaux.')
    new=[
      dict(id='certifier_bloc_local',titre='Certifier un pli et un bloc de deux zéros',statut='ouvert',type='calcul',cout=3.0,question='Peut-on certifier un des six plis attribués, sa transversalité et un contour continu isolant exactement deux zéros ?',these='Un jet analytique et une boîte rationnelle permettent une validation locale par intervalles ; succès ou obstacle doivent être documentés.',temoin='Boîte sans contraction, dérivée seconde proche de zéro ou bord de contour contenant un zéro : conserver le refus.',refutation='Aucune existence, unicité ou isolation n’est déduite d’un petit résidu ou d’une marge échantillonnée.',operateurs=["Le Point d'Euler",'La Rencontre figée'],prerequis=['v640_branches_v13'],debloque=['v641_deploiement_A_fixe'],repond_a=['Existence et unicité locale des collisions','Contrat de deux zéros pour les moments'],gains={'demontrer':1},probabilite=.6,origine='Priorité conventionnelle de dossier ; pas probabilité de succès ni de preuve de RH.'),
      dict(id='v641_deploiement_A_fixe',titre='Déployer un candidat de jets sur sa fibre à A fixé',statut='ouvert',type='calcul',cout=2.0,question='Une des quatre directions candidates donne-t-elle un pli transversal sur une géodésique préservant exactement A, ancre et rayon ?',these='Paramétrer la fibre S² permet de séparer la transversalité locale des variations radiales de A.',temoin='Section vide, perte de rang ou dérivée paramétrique nulle ; aucune collision transverse n’est alors promise.',refutation='Les quatre directions ont seulement un jet numérique nul : elles ne sont pas des zéros doubles certifiés.',operateurs=["Le Point d'Euler",'Fermeture multiplicative'],prerequis=['v640_branches_v13'],debloque=[],repond_a=['Pli local à coefficient complexe constant'],gains={'comprendre':1},probabilite=.5,origine='Programme postérieur aux résultats ; choix à verrouiller avant toute nouvelle expérience.'),
      dict(id='audit_positivite_uniforme',titre='Auditer le contrat arithmétique vers le global',statut='ouvert',type='audit',cout=2.0,question='Quelle forme arithmétique, quel domaine et quelle estimation uniforme relient réellement le calcul aux deux portes vers RH ?',these='G1–G4 séparent admissibilité, densité, queue et couplage ; le théorème A exige une borne supérieure depuis les premiers.',temoin='Gram automatiquement positif, préfixes positifs avec direction cachée, métrique construite après les racines, ou hypothèse RH circulaire.',refutation='Aucune identité arithmétique ou borne uniforme établie : consigner le pont absent au lieu de faire monter le niveau RH.',operateurs=['La Rencontre figée','La Tour'],prerequis=['v640_branches_v13'],debloque=[],repond_a=['Positivité globale pour ζ','Croissance indépendante de RH','Limites des préfixes finis'],gains={'comprendre':1},probabilite=.5,origine='Audit de livrable sous budget conventionnel ; la construction mathématique suffisante reste une route à construire.'),
    ]
    for item in new:
        item['prevision']=dict(these=item['these'],gains=item['gains'],probabilite=item['probabilite'],cout=item['cout'])
        if not any(c['id']==item['id'] for c in nav['coups']):nav['coups'].append(item)
    nav['bilan_v641']=dict(document=STEM+'.pdf',graphe=state['graph'],portes_globales=['Forme de Weil positive sur tous les tests admissibles','Borne Q(X)=X^{o(1)} depuis les premiers'],pont_arithmetique='ouvert')
    write(navpath,nav)
    ip=ROOT/'2_Methode/Indicateur/indicateur_avancement.json';ind=read(ip)
    if not any(e['id']=='v641' for e in ind['etapes']):
        ind['etapes'].append(dict(id='v641',court='V6.41',jour='12 oct.',versions='V6.41',niveaux=dict(ind['etapes'][-1]['niveaux']),franchi=status,pourquoi=dict(voir='Branches et paires reconstruisent les passages ; l’isolation continue reste à certifier.',comprendre='A prescrit est décidé par une ellipse ; paire et discriminant remplacent les étiquettes ; deux portes globales explicites.',demontrer='Preuves auxiliaires, contreexemples et contrats ; hypothèses des plis seulement recoupées numériquement.',case='Aucune estimation arithmétique globale pour ζ ni preuve de RH nouvelle.'),documents=[['Fibres, plis et positivité',STEM+'.pdf'],['Source LaTeX',STEM+'.tex'],['Graphe des passages',state['graph']]]))
    write(ip,ind)
    mp=ROOT/'2_Methode/Matrice/matrice_theories.json';matrix=read(mp);matrix['version']='V6.41'
    for node in matrix['noeuds']:
        if node['id']=='ARCH':
            if '65' not in node['docs']:node['docs'].append('65')
            if 'V6.41 :' not in node['apport_note']:node['apport_note']+=' V6.41 : '+status+' Paire locale ≠ forme globale de Weil ; distinguer les deux portes de RH.'
    write(mp,matrix)
    sourcespath=ROOT/'2_Methode/Sources/sources.json';sources=read(sourcespath)
    if not any(s['cle']=='CC21' for s in sources):
        sources.append(dict(cle='CC21',auteurs='A. Connes, C. Consani',annee=2021,titre='Weil positivity and Trace formula, the archimedean place',publication='PDF auteur daté du 4 juillet 2021 ; arXiv:2006.13771',type='article',lien='https://alainconnes.org/wp-content/uploads/Selecta.pdf',statut='partiellement vérifié',verifie_le='2026-10-12',ce_qui_a_ete_verifie='Introduction (4), involution et Fourier/Mellin dans les appendices A–B, proposition C.1 : signe et annulations polaires du critère. Ensemble des preuves non revérifié.',extrait='',usage_corpus='Critère global de Weil et conditions de test ; le résultat archimédien à support restreint ne fournit pas une positivité globale de toute la forme arithmétique.',verdict='exact',correction='',docs=['65'],motifs=['CC21','2006.13771','Selecta.pdf'],conjectures=['RH'],dimensions=['situer','comprendre'],interet='confronter',cite_aussi=['V641_PASSAGE_AU_GLOBAL.md']))
    write(sourcespath,sources)
    cp=ROOT/'00_Carte_des_idees.html';text=cp.read_text(encoding='utf-8-sig')
    bi=module('v641_ind',ROOT/'2_Methode/Indicateur/build_indicateur.py')
    text=re.sub(r'<nav class="topnav".*?</nav>',bi.topnav('carte',''),text,count=1,flags=re.S)
    text=text.replace('Version 6.40.','Version 6.41.').replace('programme Riemann V6.40','programme Riemann V6.41')
    if 'V6.41 : graphe des passages' not in text:
        panel='<section class="panel"><h2>V6.41 : graphe des passages</h2><p>'+status+'</p><p>Destination logique connue : RH. Deux portes ouvertes : positivité sur tous les tests de Weil, ou borne Q(X)=X^{o(1)} depuis les premiers. Les seules matrices finies positives et la variation universelle de D sont des voies réfutées sous les hypothèses précisées.</p><p><a href="1_Presentation/65_GRAPHE_DES_PASSAGES.html">Graphe interactif, hypothèses et preuves</a> · <a href="1_Presentation/65_FIBRES_PLIS_ET_POSITIVITE.pdf">PDF du dossier</a> · <a href="1_Presentation/65_FIBRES_PLIS_ET_POSITIVITE.tex">LaTeX</a></p></section>'
        text=text.replace('<footer>',panel+'<footer>',1)
    cp.write_text(text,encoding='utf-8-sig')
    vp=ROOT/'VERSION.txt';text=vp.read_text(encoding='utf-8-sig')
    if not text.startswith('Programme Riemann — V6.41'):vp.write_text('Programme Riemann — V6.41\nDate: 2026-10-12\nStatut: graphe, preuves auxiliaires et passages locaux exécutés\n- '+status+'\n- Deux portes globales ouvertes ; niveaux RH conservés.\n\nHistorique conservé :\n'+text,encoding='utf-8-sig')
    cf=ROOT/'CITATION.cff';cf.write_text(cf.read_text().replace('version 6.40','version 6.41').replace('version: "6.40"','version: "6.41"'))
    rp=ROOT/'README.md';text=rp.read_text(encoding='utf-8-sig').replace('version 6.40','version 6.41',1).replace('# 239 tests','# 257 tests')
    section='''## V6.41 — Graphe des passages (document 65)

**La destination RH est précise ; son mécanisme arithmétique reste ouvert.** Le dossier établit la géométrie des fibres pour A prescrit, le contreexemple D≡1 à A=0, les sections de jets et les théorèmes conditionnels du pli et des moments. Vingt candidats de collisions sont recoupés ; six sont attribués aux branches suivies ; 18 blocs et 24 racines sont reconstruits. Une perte de continuation coarse reste conservée. Les zéros et les contours ne sont pas certifiés par intervalles.

- [Graphe interactif : idées, énoncés, hypothèses et preuves](1_Presentation/65_GRAPHE_DES_PASSAGES.html).
- [Dossier PDF et démonstrations](1_Presentation/65_FIBRES_PLIS_ET_POSITIVITE.pdf) ; [LaTeX](1_Presentation/65_FIBRES_PLIS_ET_POSITIVITE.tex).
- [Contrat global G1–G4](3_Preuves_et_calculs/preuves/V641_PASSAGE_AU_GLOBAL.md) : tests admissibles, densité, limites des préfixes finis et contrôle de Schur.
- [Atlas courant de 65 documents](1_Presentation/62_ATLAS_DES_DECISIONS_BELLMAN.html) et modèle documentaire de douze actions, dont trois achevées ; coûts et poids conventionnels.
- Suite : certifier un bloc local, déployer un candidat à A fixé, puis auditer l’inégalité arithmétique uniforme requise pour l’une des deux portes vers RH.

~~~bash
python 3_Preuves_et_calculs/scripts/run_v641_passages.py --phase branches
python 3_Preuves_et_calculs/scripts/run_v641_bellman.py
node 3_Preuves_et_calculs/scripts/check_v641_bellman.js
python 2_Methode/Outils/build_v641_graph.py
python 2_Methode/Outils/build_v641_document.py
~~~

Les modèles, documents et résultats historiques sont conservés. Le nouveau modèle Bellman est une extension éditoriale après résultats, pas une prévision scientifique. Les niveaux de maturité RH restent identiques.

'''
    if '## V6.41 — Graphe des passages' not in text:text=text.replace('## V6.40 — Comparaison exacte',section+'## V6.40 — Comparaison exacte',1)
    rp.write_text(text,encoding='utf-8-sig')
    model=read(D/'v641_modele_bellman.json');result=read(D/'v641_bellman_resultats.json');bellman_figure(model,result)
    run('2_Methode/Outils/build_v641_graph.py')
    run('2_Methode/Outils/build_v641_document.py','--write-only')
    run('2_Methode/Sources/build_sources.py')
    run('2_Methode/Outils/build_v641_document.py','--compile-only')
    registry=read(D/'v640_decisions.json');registry.update(version='V6.41',corpus_base='V6.41 ; notices et résultats historiques conservés',coverage=dict(presentation_documents=65,numbers=list(range(1,66))))
    path=P/(STEM+'.md');relative=str(path.relative_to(ROOT))
    registry['documents']=[d for d in registry['documents'] if d['numero']!=65]
    registry['documents'].append(dict(numero=65,id='doc65',titre='Fibres, plis et positivité : le graphe des passages',etat_anterieur='Branches, collisions, A arbitraire et positivité globale ouverts après V6.40.',question='Comment représenter les passages sans étiquettes et préciser les deux portes globales vers RH ?',action='Faisabilité, sections de jets, continuation gelée, Wronskiens, moments, preuves de densité et obstruction aux seuls préfixes.',resultat=status,statut='preuves_et_mesures_conditionnelles',nature='preuves_et_mesures_conditionnelles',consequences='Certification locale et contrat arithmétique uniforme explicités ; niveau RH conservé.',limites='Collisions et contours non certifiés par intervalles ; aucune exhaustivité ni inégalité globale nouvelle pour ζ.',sources=[dict(path=relative,sha256=hashlib.sha256(path.read_bytes()).hexdigest())],formats_regroupes=[relative,str(path.with_suffix('.pdf').relative_to(ROOT)),str(path.with_suffix('.tex').relative_to(ROOT)),'1_Presentation/65_GRAPHE_DES_PASSAGES.html'],correctifs_ulterieurs=[],alternatives_documentees=['Paire non ordonnée plutôt qu’identité de branche ; obstruction à D universel à A=0.','Deux portes : Weil global ou borne des premiers via théorème A.'],prevision_et_apres_coup='Verrou avant les calculs de zéros ; audits et extension documentaire Bellman postérieurs, datés séparément.'))
    for record in registry['documents']:
        if record['numero'] in (30,58,61,63,64):record['correctifs_ulterieurs'].append(dict(version='V6.41',texte=status,source=relative))
    assert sorted(d['numero'] for d in registry['documents'])==list(range(1,66))
    write(D/'v641_decisions.json',registry)
    atlas=module('v641_atlas',ROOT/'2_Methode/Outils/build_v638_atlas.py')
    (P/'62_ATLAS_DES_DECISIONS_BELLMAN.html').write_text(atlas.html_atlas(registry,model,result))
    for script in ('2_Methode/Matrice/build_matrice.py','2_Methode/Indicateur/build_indicateur.py','2_Methode/Navigateur/build_navigateur.py','2_Methode/Figures/build_figures.py','2_Methode/Portail/build_portail.py'):run(script)
    # Existing corpus policy: all Markdown has BOM except immutable original receipts.
    for path in ROOT.rglob('*.md'):
        if 'recus' in path.parts:continue
        raw=path.read_bytes()
        if not raw.startswith(b'\xef\xbb\xbf'):path.write_bytes(b'\xef\xbb\xbf'+raw)
    print('V641 current views synchronized; 65 documents, 12 documentary actions, historical files retained')

if __name__=='__main__':main()
