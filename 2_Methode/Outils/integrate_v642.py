"""Current V642 corpus views, retaining V641 data and historical outputs."""
from pathlib import Path
import json,hashlib,importlib.util,subprocess,sys,re
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'1_Presentation';D=ROOT/'3_Preuves_et_calculs/data';STEM='66_UN_PLI_CERTIFIE_ET_SA_PAIRE'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def module(name,p):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def run(p,*args):subprocess.run([sys.executable,str(ROOT/p),*args],check=True)
def figure(model,result):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    actions=[a for a in model['actions'] if a['id'] not in result['completed']];values=np.array([[r['in_all_optimal_portfolios'][a['id']] for r in result['results']] for a in actions])
    fig,ax=plt.subplots(figsize=(10,5));ax.imshow(values,cmap='Blues',vmin=0,vmax=243,aspect='auto');ax.set_yticks(range(len(actions)),[a['label'] for a in actions],fontsize=9);ax.set_xticks(range(4),[str(r['budget'])+' H restants' for r in result['results']])
    for i in range(len(actions)):
        for j in range(4):ax.text(j,i,f'{values[i,j]}/243',ha='center',va='center',color='white' if values[i,j]>150 else '#23465a',fontsize=9)
    ax.set_title('V6.42 : sept actions restantes après cinq dossiers achevés\nPrésence dans tous les portefeuilles optimaux, sans probabilité scientifique',fontsize=11);fig.tight_layout();fig.savefig(P/'66_Bellman_sensibilite.png',dpi=180);plt.close(fig)

def main():
    cert=read(D/'v642_certification.json');audit=read(D/'v642_verification_rationnelle.json');assert cert['fold_certified'] and cert['contour']['accepted'] and cert['four_root_boxes_certified'] and audit['rational_checks_passed']
    status='Un pli V13 choisi certifié dans sa boîte ; contour continu de deux zéros pour tout le petit intervalle radial ; quatre boîtes uniformes, deux critiques avant et une paire hors droite après. Inégalité de Weil explicitée ; signe global ouvert.'
    model=read(D/'v642_modele_bellman.json');result=read(D/'v642_bellman_resultats.json')
    state=dict(version='V6.42',completed_bellman_actions=result['completed'],document=STEM+'.pdf',graph='66_GRAPHE_DES_CERTIFICATS.html',result=status,next_actions=['v641_deploiement_A_fixe','v642_compensation_arithmetique'],current_bellman_model='v642_modele_bellman.json',scope='One selected family, fold box and local contour; interval backend explicit, no independent backend verification or global RH proof.',maturity_levels_unchanged=True)
    write(D/'v642_etat_recherche.json',state)
    navpath=ROOT/'2_Methode/Navigateur/carte_navigation.json';nav=read(navpath)
    for c in nav['coups']:
        if c['id']=='certifier_bloc_local':c.update(statut='fait',version='V6.42',document=STEM+'.pdf',appris=status,limites_v642='Un seul pli ; backend iv et modèles d’erreur explicites ; pas d’exhaustivité, pas de relecture indépendante du backend.')
        if c['id']=='audit_positivite_uniforme':c.update(statut='fait',version='V6.42',document=STEM+'.pdf',appris='Convention Mellin, somme finie à support fixé, inégalité signée et norme de la partie première divergente sur L². Signe global non établi.',debloque=['v642_compensation_arithmetique'])
    if not any(c['id']=='v642_compensation_arithmetique' for c in nav['coups']):nav['coups'].append(dict(id='v642_compensation_arithmetique',titre='Définir le budget de la forme arithmétique complète',statut='ouvert',type='audit',cout=2.0,question='Quel domaine et quelle borne d’erreur permettent de contrôler la compensation archimédienne et les corrélations signées ?',these='Une représentation depuis les premiers et une hiérarchie dense donnent des contrats vérifiables, avec refus explicite si la borne uniforme manque.',temoin='Norme de la seule partie première divergente, métrique dégénérée au pli, compression positive sans contrôle du complément.',refutation='La borne globale de signe reste une route à construire : aucun certificat fini ne la remplace.',operateurs=['La Rencontre figée','La Tour'],prerequis=['audit_positivite_uniforme'],debloque=[],repond_a=['Domaine de la forme complète','Erreur de compression','Compensation signée'],gains={'comprendre':1},probabilite=.5,origine='Priorité conventionnelle de dossier ; aucune probabilité de prouver RH.',prevision=dict(these='Écrire ou refuser un contrat uniforme justifié.',cout=2.0,gains={'comprendre':1},probabilite=.5)))
    nav['bilan_v642']=dict(document=STEM+'.pdf',graphe=state['graph'],resultat=status,pont_global='ouvert');write(navpath,nav)
    ip=ROOT/'2_Methode/Indicateur/indicateur_avancement.json';ind=read(ip)
    if not any(e['id']=='v642' for e in ind['etapes']):ind['etapes'].append(dict(id='v642',court='V6.42',jour='12 oct.',versions='V6.42',niveaux=dict(ind['etapes'][-1]['niveaux']),franchi=status,pourquoi=dict(voir='Configurations avant/après certifiées dans les boîtes choisies.',comprendre='Paire isolée ; impossibilité de métrique positive au pli ; contrat arithmétique exact.',demontrer='Certificat calculatoire avec majorants analytiques et relecture rationnelle ; domaine et backend précisés.',case='Aucun signe global de Weil ni borne Q(X)=X^{o(1)} obtenu.'),documents=[['Un pli certifié et sa paire',STEM+'.pdf'],['LaTeX',STEM+'.tex'],['Graphe des certificats',state['graph']]]))
    write(ip,ind)
    mp=ROOT/'2_Methode/Matrice/matrice_theories.json';matrix=read(mp);matrix['version']='V6.42'
    for n in matrix['noeuds']:
        if n['id']=='ARCH':
            if '66' not in n['docs']:n['docs'].append('66')
            if 'V6.42 :' not in n['apport_note']:n['apport_note']+=' V6.42 : '+status+' La métrique positive du compagnon ne traverse pas le point double ; norme première seule non uniforme sur L².'
    write(mp,matrix)
    sp=ROOT/'2_Methode/Sources/sources.json';sources=read(sp)
    for s in sources:
        if s['cle']=='CC21':
            if '66' not in s['docs']:s['docs'].append('66')
            s['ce_qui_a_ete_verifie']+=' V6.42 : appendice B (149)–(151), convention Mellin et passage additif explicités ; la positivité globale n’est pas obtenue.'
    for s in [dict(cle='Dlm26',auteurs='NIST',annee=2026,titre='Digital Library of Mathematical Functions : 25.11 et 24.8',publication='Version en ligne consultée le 12 octobre 2026',type='documentation',lien='https://dlmf.nist.gov/25.11.iii',statut='partiellement vérifié',ce_qui_a_ete_verifie='Représentations Euler–Maclaurin, Bernoulli périodiques et développement de Fourier ; majorants supplémentaires démontrés dans la note locale.',usage_corpus='Base des identités du reste analytique pour les jets validés.',interet='appui'),dict(cle='Mpm13',auteurs='mpmath developers',annee=2026,titre='Contexts : interval arithmetic, documentation 1.3.0',publication='Documentation de la version utilisée, consultée le 12 octobre 2026',type='documentation',lien='https://mpmath.org/doc/current/contexts.html',statut='partiellement vérifié',ce_qui_a_ete_verifie='Extrait de la documentation primaire : support iv expérimental ; version installée 1.3.0 et primitives effectivement utilisées contrôlées localement.',usage_corpus='Backend explicité ; pas de réévaluation indépendante de toutes les primitives.',interet='contexte')]:
        s.update(verifie_le='2026-10-12',extrait='',verdict='exact',correction='',docs=['66'],motifs=[],conjectures=['RH'],dimensions=['situer'],cite_aussi=[])
        if not any(a['cle']==s['cle'] for a in sources):sources.append(s)
    write(sp,sources)
    bi=module('ind642',ROOT/'2_Methode/Indicateur/build_indicateur.py');cp=ROOT/'00_Carte_des_idees.html';text=cp.read_text(encoding='utf-8-sig')
    text=re.sub(r"<nav class=['\"]topnav['\"].*?</nav>",bi.topnav('carte',''),text,count=1,flags=re.S).replace('Version 6.41.','Version 6.42.').replace('programme Riemann V6.41','programme Riemann V6.42')
    if 'V6.42 : un pli et sa paire certifiés' not in text:text=text.replace('<footer>','<section class="panel"><h2>V6.42 : un pli et sa paire certifiés</h2><p>'+status+'</p><p><a href="1_Presentation/66_GRAPHE_DES_CERTIFICATS.html">Graphe courant</a> · <a href="1_Presentation/66_UN_PLI_CERTIFIE_ET_SA_PAIRE.pdf">Dossier et preuves</a></p></section><footer>',1)
    cp.write_text(text,encoding='utf-8-sig')
    vp=ROOT/'VERSION.txt';text=vp.read_text(encoding='utf-8-sig')
    if not text.startswith('Programme Riemann — V6.42'):vp.write_text('Programme Riemann — V6.42\nDate: 2026-10-12\nStatut: un pli et sa paire validés par intervalles\n- '+status+'\n- Niveaux RH conservés ; prochaine phase à A fixé et compensation globale.\n\nHistorique conservé :\n'+text,encoding='utf-8-sig')
    cf=ROOT/'CITATION.cff';cf.write_text(cf.read_text().replace('version 6.41','version 6.42').replace('version: "6.41"','version: "6.42"'))
    rp=ROOT/'README.md';text=rp.read_text(encoding='utf-8-sig').replace('version 6.41','version 6.42',1).replace('# 257 tests','# 262 tests',1)
    section='''## V6.42 - Un pli certifié et sa paire (document 66)

**Un pli choisi est maintenant validé par intervalles.** Deux contractions 50/80 décimales, un contour continu de deux zéros sur 256 arcs, quatre boîtes uniformes : deux racines critiques avant, une paire hors droite après. Les majorants analytiques et les inégalités rationnelles sont fournis ; le backend iv est explicité et n’est pas indépendamment réévalué. La métrique positive du compagnon ne traverse pas le double. Le contrat arithmétique global devient une inégalité signée précise ; son signe reste ouvert.

- [Dossier PDF et preuves](1_Presentation/66_UN_PLI_CERTIFIE_ET_SA_PAIRE.pdf), [LaTeX](1_Presentation/66_UN_PLI_CERTIFIE_ET_SA_PAIRE.tex), [graphe courant](1_Presentation/66_GRAPHE_DES_CERTIFICATS.html).
- [Certificats complets](3_Preuves_et_calculs/data/v642_certification.json) et [relecture rationnelle](3_Preuves_et_calculs/data/v642_verification_rationnelle.json).
- [Contrat arithmétique](3_Preuves_et_calculs/preuves/V642_CONTRAT_ARITHMETIQUE.md) et [protocole prospectif](3_Preuves_et_calculs/data/prevision_v642_certification.md).
- Modèle Bellman courant : douze actions, cinq dossiers achevés ; dependency des sources de Weil corrigée éditorialement après résultats. Poids et coûts conventionnels.
- Suite : déployer un candidat sur sa fibre à A fixé ; contrôler la forme arithmétique complète, pas la norme de la seule partie première.

~~~bash
python 3_Preuves_et_calculs/scripts/run_v642_certification.py
python 3_Preuves_et_calculs/scripts/check_v642_certificate.py
node 3_Preuves_et_calculs/scripts/check_v642_bellman.js
~~~

Rejouer sur une copie après déplacement des sorties : le lanceur refuse leur écrasement. Le même backend sert aux recoupements de formule ; ceux-ci ne sont pas des validations indépendantes du backend.

'''
    if '## V6.42 - Un pli certifié' not in text:text=text.replace('## V6.41 — Graphe des passages',section+'## V6.41 — Graphe des passages',1)
    rp.write_text(text,encoding='utf-8-sig');figure(model,result)
    run('2_Methode/Outils/build_v642_figures.py');run('2_Methode/Outils/build_v642_document.py','--write-only')
    # Add source keys for the formal bibliography, without rewriting historical articles.
    doc=P/(STEM+'.md');t=doc.read_text(encoding='utf-8-sig');t=t.replace('Sources primaires des identités :','Sources primaires des identités [Dlm26] :').replace('La documentation du backend qualifie','La documentation du backend [Mpm13] qualifie');doc.write_text(t,encoding='utf-8-sig')
    run('2_Methode/Sources/build_sources.py');run('2_Methode/Outils/build_v642_document.py','--compile-only')
    registry=read(D/'v641_decisions.json');registry.update(version='V6.42',corpus_base='V6.42 ; états et résultats historiques conservés',coverage=dict(presentation_documents=66,numbers=list(range(1,67))))
    relative=str(doc.relative_to(ROOT));registry['documents'].append(dict(numero=66,id='doc66',titre='Un pli certifié, sa paire et la porte arithmétique',etat_anterieur='Collisions et contours V6.41 recoupés mais non certifiés.',question='Un pli et une paire locaux peuvent-ils être validés, et quel contrat global manque ?',action='Majoration analytique, contractions strictes, Rouché continu, symétrie et audit arithmétique.',resultat=status,statut='certificat_local_et_preuves',nature='certificat_local_et_preuves',consequences='Une paire locale certifiée ; deux voies de positivité automatique fermées dans leurs domaines ; déploiement à A fixé et signe global ouverts.',limites='Un seul pli ; backend d’intervalles précisé sans validation indépendante ; pas d’exhaustivité, de premier zéro global ou de RH.',sources=[dict(path=relative,sha256=hashlib.sha256(doc.read_bytes()).hexdigest())],formats_regroupes=[relative,str(doc.with_suffix('.pdf').relative_to(ROOT)),str(doc.with_suffix('.tex').relative_to(ROOT)),'1_Presentation/66_GRAPHE_DES_CERTIFICATS.html'],correctifs_ulterieurs=[],alternatives_documentees=['Projection réelle fixe et contrôle d’ancre ; pas de Gamma par intervalles.','Forme arithmétique signée ; norme de la seule partie première non uniforme.'],prevision_et_apres_coup='Protocole avant nouvelles évaluations L ; diagnostics rationnels et modification documentaire de dépendance après résultats.'))
    for r in registry['documents']:
        if r['numero'] in (58,63,64,65):r['correctifs_ulterieurs'].append(dict(version='V6.42',texte=status,source=relative))
        for s in r.get('sources',[]):
            if isinstance(s,dict) and (ROOT/s['path']).exists():s['sha256']=hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()
    assert sorted(r['numero'] for r in registry['documents'])==list(range(1,67));write(D/'v642_decisions.json',registry)
    atlas=module('atlas642',ROOT/'2_Methode/Outils/build_v638_atlas.py');(P/'62_ATLAS_DES_DECISIONS_BELLMAN.html').write_text(atlas.html_atlas(registry,model,result))
    for s in ('2_Methode/Matrice/build_matrice.py','2_Methode/Indicateur/build_indicateur.py','2_Methode/Navigateur/build_navigateur.py','2_Methode/Figures/build_figures.py','2_Methode/Portail/build_portail.py'):run(s)
    for p in ROOT.rglob('*.md'):
        if 'recus' not in p.parts and not p.read_bytes().startswith(b'\xef\xbb\xbf'):p.write_bytes(b'\xef\xbb\xbf'+p.read_bytes())
    print('V642: 66 documents and all active menus synchronized; historical outputs retained')
if __name__=='__main__':main()
