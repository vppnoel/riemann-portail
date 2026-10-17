"""Document64: all frozen comparisons, numerical evidence, lemmas and next step."""
from pathlib import Path
import json
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'1_Presentation'
D=ROOT/'3_Preuves_et_calculs/data'
STEM='64_COMPARAISON_EXACTE_V13'


def load(name):return json.loads((D/name).read_text(encoding='utf-8-sig'))
def number(x,digits=6):return f'{float(x):.{digits}f}'.replace('.',',')


def main():
    manifest=load('v639_couples_fixes.json')
    result=load('v640_resultats.json')
    rows=load('v640_directions.json')
    roots=load('v640_racines_recoupees.json')
    inputs=load('v640_erreur_entree.json')
    by_id={r['id']:r for r in rows}
    root_by={r['id']:r for r in roots['jobs']}
    report=result['analysis']['reports'][-1]
    counts=report['counts']
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(10.2,3.4),sharey=True)
    radii=('9/20','pi/6','13/20','3/4')
    x=[.45,3.141592653589793/6,.65,.75]
    for ax,k in zip(axes,(1,3,5)):
        pairs={p['radius']:p for p in manifest['pairs'] if p['character_k']==k}
        for side,label,color,marker in (('plus','D bas','#126880','o'),('minus','D haut','#b34b3b','s')):
            y=[by_id[pairs[r]['id']+'_'+side]['first_detected'] for r in radii]
            ax.plot(x,y,color=color,marker=marker,label=label)
        ax.set_title(f'Ancre χ{k}')
        ax.set_xticks(x,['0,45','π/6','0,65','0,75'],rotation=25)
        ax.set_xlabel('Rayon exact (rad)')
        ax.grid(alpha=.2)
        ax.set_ylim(3,22)
    axes[0].set_ylabel('Première tranche de déficit numérique')
    axes[2].legend(loc='upper right',fontsize=8)
    fig.suptitle('Le signe de la comparaison dépend de l’ancre',fontsize=13)
    fig.tight_layout();fig.savefig(P/'64_Tranches_par_ancre.png',dpi=180);plt.close(fig)
    max_input=max(float(r['max_binary64_coordinate_error']) for r in inputs['rows'])
    max_agreement=max(float(j['confirmation']['precision_agreement']) for j in roots['jobs'] if j['root_found'])
    max_shift=max(float(j['confirmation']['binary64_sensitivity']['input_shift']) for j in roots['jobs'] if j['root_found'])
    hmin=min(r['sampled_boundary_horizontal_min'] for r in rows)
    rmin=min(r['sampled_boundary_vertical_min'] for r in rows)
    L=[
        '# V6.40 — Comparaison exacte V13 : le signe dépend de l’ancre','',
        '**Document 64 · Vincent P. P. NOËL · 12 octobre 2026**','',
        'Note de recherche, expérience prospective, relecture interne et source LaTeX.','',
        '## 1. Le résultat et la décision','',
        f'**Les 12 couples préparés en V6.39 ont été comparés : {counts["higher_D_earlier"]} donnent une détection plus précoce pour le membre de D élevé, {counts["higher_D_later"]} une détection plus tardive.** Aucune égalité de tranche, aucune non-détection sous le plafond 150 et aucun cas non résolu ne sont retirés du bilan. Les 24 membres disposent chacun d’une racine hors droite recoupée à 80 et 110 chiffres de travail.','',
        'La prévision descriptive « une majorité des 12 strates » est atteinte : le seuil fixé avant calcul était 7 sur 12. Le résultat le plus instructif est sa structure. Les quatre rayons de χ₁ donnent le signe contraire ; ceux de χ₃ et χ₅ donnent le signe favorable. Le score D n’impose donc pas ici une orientation numérique uniforme, même après contrôle exact du premier coefficient complexe, de l’ancre et du rayon à l’intérieur de chaque couple.','',
        'Les douze couples ne sont pas douze réplications indépendantes. Les rayons d’une même ancre partagent une direction ; χ₃ et χ₅ emploient le même support de trois caractères. Le rapport 8/12 décrit ce plan déterministe. Il ne reçoit ni valeur p, ni interprétation causale, ni généralisation à toutes les directions de V13.','',
        '![Premières tranches des déficits numériques : D haut détecte plus tard pour χ₁ et plus tôt pour χ₃, χ₅. Les lignes relient seulement quatre rayons calculés ; elles ne suivent pas une branche de racines.](64_Tranches_par_ancre.png)','',
        '**Suite retenue : suivre des branches de racines dans les mêmes familles exactes et confronter leur mouvement à une formule locale démontrée.** Augmenter seulement le plafond ou accumuler des couples n’expliquerait pas ce changement de signe.','',
        r'\newpage','',
        '## 2. Les douze résultats, sans sélection après calcul','',
        'Pour chaque ancre i et chaque rayon r, la recette définit exactement','',
        r'\[c_\pm=\cos(r)e_i\pm\sin(r)u,\quad u_i=0,\quad\|u\|=1,\quad\sum_j u_jz_j=0.\]','',
        r'\[a_+(1)=a_-(1)=\cos(r)z_i,\qquad D_+<D_-.\]','',
        'Le membre « + » a D bas, le membre « − » D haut. Les valeurs D ci-dessous sont arrondies pour lecture ; les égalités de contraintes viennent des recettes, démontrées dans le document 63. La phase et la valeur de A varient entre strates, mais sont identiques au sein d’une strate.','',
        '| Ancre | Rayon exact | D bas | D haut | Tranche, D bas | Tranche, D haut | Ordre, D haut |',
        '|:--|:--|--:|--:|--:|--:|:--|']
    for k in (1,3,5):
        for radius in radii:
            p=next(p for p in manifest['pairs'] if p['character_k']==k and p['radius']==radius)
            a=by_id[p['id']+'_plus'];b=by_id[p['id']+'_minus']
            order='plus tôt' if b['first_detected']<a['first_detected'] else 'plus tard'
            L.append(f"| χ{k} | {radius} | {number(a['D'])} | {number(b['D'])} | {a['first_detected']} | {b['first_detected']} | {order} |")
    L += ['',
        'Les bilans aux plafonds 50, 100 et 150 ont le même ordre : toutes les premières détections du plan se situent au plus à la tranche 20. Des détections supplémentaires à plus grande hauteur existent ; le fichier de comptages conserve les 150 niveaux pour chaque membre.','',
        'Le seuil minimal d’écart D=1/40 est conservé. Aucun support ni rayon n’a été remplacé en fonction du résultat. Le manifeste V6.39 est repris octet pour octet, avec son empreinte conservée. Les six ancres ont trois classes conjuguées pour un observable symétrique en |t| ; les conjugates ne sont pas ajoutées au dénominateur.','',
        '**Exemple : χ₁, r=π/6.** D bas≈0,591417 détecte à la tranche 5 ; D haut≈0,658583 détecte à la tranche 12. À χ₅ au même rayon, le sens s’inverse : tranches 16 et 11. Le coefficient A est contrôlé à l’intérieur de chacune de ces deux paires ; il n’est pas égal entre les deux ancres.','',
        r'\newpage','',
        '## 3. Ce que le détecteur mesure et ses contrôles','',
        r'\[\widehat N_{\rm déficit}(T)=\widehat N_{\rm contour}(T)-\widehat N_{\rm signes}(T).\]','',
        'Le contour de la fonction complétée couvre −2≤Re(s)≤3 et |Im(s)|≤T. La symétrie de l’équation fonctionnelle permet de le calculer depuis le côté droit. Le compte critique utilise les changements de signe de la fonction de Hardy réelle. La première tranche retenue est le premier entier T où le déficit devient positif.','',
        'Un zéro critique double, ou deux zéros critiques proches manqués par la grille, peuvent produire un déficit sans racine hors droite. Pour cette raison, les détections admissibles sont recoupées séparément. La présence d’une racine dans la tranche ne démontre pas qu’aucune racine hors droite n’existe avant : « première détection » reste un terme d’instrument.','',
        '| Contrôle figé avant résultat | Bilan V6.40 |','|:--|:--|',
        '| Deux contours : dt=0,02/0,01 et ds=0,05/0,025, avec raffinement adaptatif | Aucun compte modifié sur les 30 directions et 150 niveaux |',
        '| Trois grilles critiques : dt=0,02/0,01/0,005 | Aucun compte modifié |',
        '| Déficit pair, non négatif ; monotonie des trois comptes | 30 directions admissibles sur 30 |',
        '| Ambiguïtés de phase restantes | Zéro |',
        '| Six axes d’Euler | Aucune détection sous 150 ; comptes stables |',
        '| Coordonnées exportées vs recettes reconstruites et réarrondies | Aucun compte ni classement modifié |',
        '| Recoupements : recette analytique, 80/110 chiffres, partenaire fonctionnel | 24 membres sur 24 acceptés |','',
        f'Les minima relatifs **échantillonnés** sur les bords sont {hmin:.3e} horizontalement et {rmin:.3e} verticalement, pour un seuil fixé à 1e−10. Les résidus d’enroulement à l’entier sont inférieurs à 2,7e−11. Les incréments de phase restent sous 0,8 après raffinement. Ces observations ne fournissent pas des bornes sur les segments continus du contour.','',
        f'L’erreur maximale estimée des coordonnées binary64 face à la recette reconstruite est {max_input:.3e}. Le contrôle de sensibilité refait les comptes fins après reconstruction à 110 chiffres puis arrondissement binary64 : les contours eux-mêmes restent en double précision. Il ne s’agit pas d’un contour évalué à 110 chiffres.','',
        'Le bord droit R=3 possède une justification analytique uniforme par domination de a(1). Sa preuve rationnelle est donnée en annexe. Elle sécurise ce bord, sans certifier les autres segments ni la complétude du comptage intérieur.','',
        r'\newpage','',
        '## 4. Les vingt-quatre racines recoupées','',
        'Chaque localisation Euler–Maclaurin est reprise avec la recette analytique exacte et un évaluateur mpmath.dirichlet. Le contrôle lève également les floats comme nombres binaires exacts, et vérifie le partenaire 1−conj(s) après correction de l’échelle Gamma. Les valeurs arrondies ci-dessous désignent une racine dans chaque tranche, sans assertion d’unicité ou d’absence antérieure.','',
        '| Ancre | Rayon | Membre | Re(s) | Im(s), signe conservé |','|:--|:--|:--|--:|--:|']
    for k in (1,3,5):
        for radius in radii:
            p=next(p for p in manifest['pairs'] if p['character_k']==k and p['radius']==radius)
            for side,label in (('plus','D bas'),('minus','D haut')):
                c=root_by[p['id']+'_'+side]['confirmation']
                L.append(f"| χ{k} | {radius} | {label} | {number(c['beta_mp'])} | {number(c['gamma_mp'])} |")
    L += ['',
        f'L’accord maximal entre 80 et 110 chiffres de travail est {max_agreement:.3e} ; le déplacement maximal dû aux coordonnées binary64 est {max_shift:.3e}. Ces nombres sont des résultats de recoupement, pas des bornes certifiées sur l’erreur des ordonnées.','',
        'Les seuils prospectifs sont : résidus <1e−50/1e−75, partenaire ramené à même échelle <1e−45/1e−70, accord entre précisions <1e−30, accord EM/MP <1e−7 et déplacement des entrées <1e−9. La racine doit être strictement à droite de 0,500001 et dans la même tranche de |t|. Tous ces critères sont satisfaits.','',
        'Deux contrôles de relecture postérieurs, à χ₁ et χ₅ pour r=π/6 et D bas, reconstruisent les phases par Arg et évaluent explicitement la somme des six Hurwitz. Ils concordent avec les racines ci-dessus. Ils utilisent le même backend mpmath et sont présentés comme contrôles de formule, pas comme certifications indépendantes par intervalles.','',
        r'\newpage','',
        '## 5. Interprétation, ouvertures et prochaine étape','',
        'L’expérience écarte une explication simple selon laquelle contrôler A complexe ferait disparaître toute tendance dans le plan choisi. Une majorité subsiste, mais avec une inversion systématique par ancre. Elle ne suffit pas à attribuer le déplacement à D : les autres coefficients de la série changent également entre les membres opposés.','',
        '| Question | État après V6.40 |','|:--|:--|',
        '| D peut-il varier à A complexe, ancre et rayon identiques ? | Démontré en V6.39, pour A=cos(r)z_i |',
        '| La majorité précoce annoncée se retrouve-t-elle dans les 12 strates ? | Oui, pour l’observable numérique figé : 8/12 |',
        '| Le signe est-il uniforme entre les trois ancres ? | Non dans ce plan numérique : χ₁ inverse χ₃ et χ₅ |',
        '| D cause-t-il une sortie plus précoce ? | Ouvert ; aucun contraste causal isolant D seul |',
        '| Les détections sont-elles les vrais premiers zéros hors droite ? | Non certifié |',
        '| Le cas d’un A complexe arbitraire est-il traité ? | Ouvert |',
        '| Un mécanisme de positivité globale impose-t-il RH pour ζ ? | Ouvert |','',
        '**Étape suivante concrète.** Construire une continuation des branches simples de F±(r,s)=0 en r dans les mêmes familles exactes. Fixer auparavant la grille, l’identité des branches, les conditions d’arrêt et le traitement des collisions. Pour les ancres χ₁ et χ₅, vérifier si le signe contraire résulte d’une autre branche devenant première, d’une collision critique, ou de la vitesse propre de la branche suivie. Conserver les pertes de branches ; une continuation interrompue n’est pas une absence.','',
        'Le lemme local de l’annexe donne la vitesse s′(r) sous l’hypothèse de racine simple. Il n’impose pas le signe de Im(s′). C’est un outil pour formuler une explication testable ; la vérification de ses hypothèses et le suivi des branches restent à faire.','',
        '**Bellman et le corpus.** Les actions « contraintes V13 » et « comparaison V13 » sont désormais achevées dans l’état courant du portail. Les utilités documentaires sont attribuées au travail réalisé, y compris à ses limites ; elles ne récompensent pas une preuve de RH. Le modèle fini historique ne contient pas encore l’action de continuation : il faut l’expliciter avant de la soumettre à cette planification. Les niveaux de maturité concernant RH ne sont pas augmentés par cette mesure.','',
        'Les trois articles existants gardent leur portée. Cette note fournit un nouveau résultat numérique contrôlé et deux lemmes auxiliaires. Une généralisation analytique, une certification locale des racines et une relecture humaine spécialisée sont des travaux distincts encore ouverts.','',
        r'\newpage','',
        '## Annexe A — Démonstrations et unités','']
    proof=(ROOT/'3_Preuves_et_calculs/preuves/LEMMES_ET_SUITE_V640.md').read_text()
    proof='\n'.join('### '+line[3:] if line.startswith('## ') else line for line in proof.splitlines()[2:])
    proof=proof.replace('### Lemme 2',r'\newpage'+'\n\n### Lemme 2',1)
    L += [proof,'',r'\newpage','',
        '## Annexe B — Reproduction et provenance','',
        'La sélection analytique V6.39 précède les nouveaux comptes. La précision du protocole d’exécution V6.40 est datée du 12 octobre 2026, à 13:17:04 UTC. Le début d’exécution enregistré est 13:19:55 UTC. Les relectures supplémentaires postérieures sont explicitement distinguées.','',
        '| Fichier dans le corpus | Fonction |','|:--|:--|',
        '| data/v639_couples_fixes.json | 12 couples et recettes immuables |',
        '| data/prevision_v640_comparaison.md | Critères, prévision et censure avant calcul |',
        '| data/v640_protocole_verrouille.json | Empreintes et seuils figés |',
        '| data/v640_resultats.json | Bilans complets aux trois plafonds |',
        '| data/v640_directions.csv et .json | Tous les membres et contrôles |',
        '| data/v640_comptages.npz | Matrices de comptes et sensibilités |',
        '| data/v640_racines_recoupees.json | 24 statuts, résidus et partenaires |',
        '| data/v640_erreur_entree.json | Erreurs estimées des coordonnées et phases |',
        '| preuves/V640_RELECTURE_CONSTRUCTIVE.md et CRITIQUE.md | Lectures complémentaires |','',
        'Les chemins data/ et preuves/ ci-dessus sont relatifs à 3_Preuves_et_calculs. Les sources de la note sont dans 1_Presentation ; sa figure accompagne le LaTeX dans le ZIP global. Les sorties historiques sont conservées.','',
        'Après les premiers tests, les nouveaux Markdown ont reçu le préfixe UTF-8 de trois octets exigé par le corpus. Les octets originaux de la prévision sont conservés sous le même nom dans le dossier 4_Archives/recus/V640, avec l’empreinte du verrou inchangée. La copie de lecture a le même texte ; le vérificateur ignore seulement ce préfixe. Aucun support, seuil, rayon ou résultat expérimental n’a été modifié. Le correctif de présentation est daté dans data/v640_correctifs_presentation.json.','',
        'Pour rejouer : extraire une copie du corpus ; conserver le manifeste et le verrou, puis déplacer dans un autre dossier les sorties v640_resultats.json, v640_comptages.npz et v640_racines_recoupees.json. Le lanceur refuse de les écraser silencieusement. Les caches de grilles sont reproductibles et ne sont pas nécessaires à la lecture.','',
        '```bash',
        'cd 3_Preuves_et_calculs',
        'python scripts/run_v640_comparaison.py --run',
        'python scripts/run_v640_comparaison.py --roots',
        'python tests/run_all_tests.py',
        'cd ..',
        'python 2_Methode/Outils/build_v640_document.py',
        '```','',
        'Dépendances numériques : NumPy, SciPy, pandas, mpmath 1.3.0 ; génération de la figure : Matplotlib ; source et PDF : Pandoc et XeLaTeX. Les dépendances globales figurent dans requirements.txt.','',
        'L’empreinte du payload du manifeste, calculée sans son champ sha256, est :','',
        '`'+manifest['sha256']+'`','',
        'Le ZIP global conserve l’ensemble des documents, articles, données, codes, prévisions et historiques. Ouvrir 00_PORTAIL.html après extraction donne accès au bilan courant, aux PDF et aux sources.','',
        'Aucune première ordonnée exacte, absence antérieure, causalité ou preuve de RH n’est revendiquée.']
    text='\n'.join(L)+'\n'
    text=text.replace('Deux contrôles de relecture postérieurs, à χ₁ et χ₅ pour r=π/6 et D bas, reconstruisent les phases par Arg et évaluent explicitement la somme des six Hurwitz. Ils concordent avec les racines ci-dessus. Ils utilisent le même backend mpmath et sont présentés comme contrôles de formule, pas comme certifications indépendantes par intervalles.',
        'La relecture constructive recalcule deux racines et la relecture critique les vingt-quatre positions à 90 chiffres, par une reconstruction distincte et une somme explicite des Hurwitz. Les résidus maximaux des vingt-quatre positions sont inférieurs à 3,3e−90. Ces contrôles de formule sont postérieurs aux comptes ; ils utilisent le même backend mpmath et ne sont pas des certifications par intervalles.')
    (P/(STEM+'.md')).write_text(text,encoding='utf-8-sig')
    header=r'''\usepackage{etoolbox}
\usepackage{microtype}
\setlength{\emergencystretch}{3em}
\AtBeginEnvironment{longtable}{\small}
\AtBeginDocument{\hypersetup{colorlinks=true,linkcolor=blue!45!black,urlcolor=blue!45!black}}
'''
    with tempfile.TemporaryDirectory(prefix='v640_pdf_') as directory:
        tmp=Path(directory);(tmp/'header.tex').write_text(header)
        args=['pandoc',STEM+'.md','-s','-f','markdown+tex_math_single_backslash',
            '--resource-path=.','--include-in-header='+str(tmp/'header.tex'),
            '-V','geometry:margin=19mm','-V','papersize=a4','-V','mainfont=DejaVu Sans',
            '-V','monofont=DejaVu Sans Mono','-V','fontsize=10pt','-V','lang=fr-FR',
            '-o',STEM+'.tex']
        run=subprocess.run(args,cwd=P,capture_output=True,text=True)
        logs=run.stdout+run.stderr
        if run.returncode:raise RuntimeError(logs)
        source=P/(STEM+'.tex')
        source.write_text(source.read_text().replace('\\real{0.1429}','\\real{0.142857}'))
        for _ in range(2):
            run=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',
                '-output-directory='+str(tmp),STEM+'.tex'],cwd=P,capture_output=True,text=True)
            logs+=run.stdout+run.stderr
            if run.returncode:
                (D/'v640_pdf_compile.log').write_text(logs);raise RuntimeError(logs[-5000:])
        (D/'v640_pdf_compile.log').write_text(logs)
        shutil.copy2(tmp/(STEM+'.pdf'),P/(STEM+'.pdf'))
    print('Document64 PDF, Markdown and LaTeX generated')


if __name__=='__main__':main()
