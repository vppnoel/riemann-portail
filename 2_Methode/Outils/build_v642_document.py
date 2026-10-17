"""Document 66: validated local passage and exact arithmetic contract."""
from pathlib import Path
from fractions import Fraction
import argparse
import json
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[2];P=ROOT/'1_Presentation';D=ROOT/'3_Preuves_et_calculs/data'
STEM='66_UN_PLI_CERTIFIE_ET_SA_PAIRE'
def load(n):return json.loads((D/n).read_text(encoding='utf-8-sig'))
def dec(x,n=12):return f'{float(Fraction(x)):.{n}f}'.replace('.',',')
def bound(x,places=12,up=False):
    scaled=Fraction(x)*10**places
    integer=-((-scaled.numerator)//scaled.denominator) if up else scaled.numerator//scaled.denominator
    sign='-' if integer<0 else '';integer=abs(integer)
    return f'{sign}{integer//10**places}.{integer%10**places:0{places}d}'

def write_markdown():
    data=load('v642_certification.json');protocol=load('v642_protocole_verrouille.json');fold=data['fold_attempts'][-1];contour=data['contour'];attempt=contour['arc_attempts'][-1]
    assert data['fold_certified'] and data['four_root_boxes_certified'] and contour['accepted']
    text=r'''# V6.42 - Un pli certifié, sa paire et la porte arithmétique

**Document 66 · Vincent P. P. NOËL · 12 octobre 2026**

Dossier de recherche, preuves auxiliaires, certificat calculatoire et source LaTeX.

## 1. La suite a été exécutée : un passage local est maintenant validé

**La famille exacte V13 choisie possède un pli critique double unique dans
la boîte fixée.** Le contrôle de Rouché couvre le contour continu et tout
le petit intervalle radial : il contient exactement deux zéros avec
multiplicité. Aux paramètres $r_*\pm10^{-4}$, quatre boîtes de racines
sont validées uniformément malgré l’incertitude sur $r_*$ : deux zéros
critiques avant, une paire hors droite après.

Ce résultat dépasse un accord entre précisions : une borne analytique du
reste, une inclusion stricte et une contraction fournissent existence et
unicité. Le calcul repose sur le backend d’intervalles explicité ; une
validation indépendante de tout ce backend n’est pas revendiquée.

| Point | Résultat V6.42 | Portée |
|:--|:--|:--|
| Pli sélectionné | Validations à 50 puis 80 décimales | Même boîte et même recette ; projection réelle non nulle |
| Contour | 256 arcs, comparaison stricte de Rouché | Cercle continu, pour tout r du petit intervalle |
| Quatre racines | Quatre contractions uniformes et boîtes disjointes | Deux critiques par symétrie et unicité ; deux hors droite |
| Paire et opérateur | Signature locale certifiée avant et après | Pas de métrique positive non dégénérée au point double |
| Porte globale | Forme arithmétique et inégalité uniforme explicites | Le signe de la forme complète demeure ouvert |

**Une voie est fermée précisément.** Toute métrique hermitienne positive
symétrisant le compagnon réel exige μ>0. Elle dégénère ou devient non
uniformément bornée à l’approche du pli ; au double, le bloc de Jordan
interdit une métrique définie positive. C’est une impossibilité locale,
pas une impossibilité de prouver RH.

La cible RH et les deux portes globales gardent leur portée : le certificat
ne fournit ni le signe de Weil pour tous les tests, ni une borne suffisante
sur l’énergie arithmétique Q(X). Il certifie une composante choisie de V13.
Dans cette continuation radiale, $A=\cos r\,z_i$ varie ; le déploiement sur
une fibre à A constant reste une expérience distincte.

\newpage

## 2. Encadrements, marges et sens de la preuve

Le protocole sélectionne, parmi les six plis attribués V6.41, celui de plus
petite hauteur absolue : `fold_k1_plus_5`, famille `k1_rpi_6`, membre plus.
Les centres rationnels sont $r_0=0,243079394165$ et
$t_0=4,861023490998$, avec demi-largeur $10^{-9}$. Le verrou est antérieur
à toute nouvelle évaluation de fonction L.

| Contrôle | Valeur ou encadrement certifié |
|:--|:--|
'''
    kr,kt=fold['certificate']['K_intervals'];kappa=fold['kappa']
    text+=f"| r* | [{kr['lower']} ; {kr['upper']}] |\n| t* | [{kt['lower']} ; {kt['upper']}] |\n"
    text+=f"| κ=−2 Hr/Htt | [{kappa['lower']} ; {kappa['upper']}] |\n"
    for a in data['fold_attempts']:text+=f"| Contraction du pli, {a['digits']} décimales | q ≤ {bound(a['certificate']['contraction_upper'],12,True)} < 1 |\n"
    text+=f"| Module de comparaison sur le cercle | ≥ {bound(contour['comparison_modulus_lower'],10)} |\n| Majorant du défaut sur les 256 arcs | ≤ {bound(attempt['maximum_defect_upper'],10,True)} |\n| Marge uniforme de Rouché | ≥ {bound(attempt['minimum_margin_lower'],10)} > 0 |\n"
    text+=r'''
Les décimales affichées du tableau sont des résumés. Les bornes complètes
et les endpoints binaires, exportés vers l’extérieur, figurent dans le
certificat JSON. Les quatre encadrements ci-dessous sont volontairement
élargis pour une lecture simple :

| Paramètre | Re(s) | Encadrement de Im(s) |
|:--|:--|:--|
| r*−10⁻⁴, racine haute | 1/2 exactement | [4,874488964703 ; 4,874488964747] |
| r*−10⁻⁴, racine basse | 1/2 exactement | [4,847596737039 ; 4,847596737084] |
| r*+10⁻⁴, racine gauche | [0,486553813589 ; 0,486553813637] | [4,861004131596 ; 4,861004131643] |
| r*+10⁻⁴, racine droite | [0,513446186366 ; 0,513446186408] | [4,861004131599 ; 4,861004131641] |

La criticité des deux premières ne vient pas d’un intervalle étroit autour
de 1/2 : chaque boîte est invariante par $s\mapsto1-\overline s$, et son
zéro unique est donc fixé par la symétrie fonctionnelle. Les deux autres
boîtes excluent la droite critique. Les quatre localisations sont uniformes
pour les intervalles de paramètres contenant les valeurs exactes
$r_*\pm10^{-4}$.

![Deux configurations certifiées de la même paire. Les centres sont marqués ; les boîtes de validation ont largeur 2×10⁻⁸ et sont invisibles à cette échelle.](66_Paire_certifiee.png)

![Majorants sur les 256 arcs : la borne inclut tous les points de chaque arc et tout le petit intervalle radial. Ce tracé représente une borne, pas des échantillons du module exact.](66_Controle_du_contour.png)

Une précision de travail de 80 décimales ne signifie pas 80 décimales
certifiées sur les coordonnées. La dépendance des intervalles dans une
boîte de largeur fixée reste dominante. Les encadrements obtenus sont
ceux du tableau et des données, avec leurs marges réellement calculées.

\newpage

## 3. Le graphe courant des acquis et des obstacles

![Un pli et une paire sont validés ; le compagnon rencontre une impossibilité de métrique au double ; les deux portes arithmétiques globales restent ouvertes.](66_Graphe_des_certificats.png){width=85%}

Le lecteur interactif `66_GRAPHE_DES_CERTIFICATS.html` relie chaque nœud à
ses preuves et à ses hypothèses. Le graphe historique du document 65 est
conservé. L’observation des 20 candidats V6.41 n’est pas transformée en
une certification des 20 : seul le pli sélectionné reçoit ce nouveau statut.

\newpage

## 4. Démonstrations locales et limites du compagnon

'''
    local=(ROOT/'3_Preuves_et_calculs/preuves/V642_CERTIFICATION_LOCALE.md').read_text(encoding='utf-8-sig')
    text+='\n'.join('### '+line[3:] if line.startswith('## ') else line for line in local.splitlines()[2:])
    text+=r'''

\newpage

## 5. L’inégalité globale et l’opérateur de translations

'''
    global_=(ROOT/'3_Preuves_et_calculs/preuves/V642_CONTRAT_ARITHMETIQUE.md').read_text(encoding='utf-8-sig')
    text+='\n'.join('### '+line[3:] if line.startswith('## ') else line for line in global_.splitlines()[2:])
    text+=r'''

\newpage

## 6. Reproduction, contrôles et étapes ultérieures

Le verrou est écrit le 12 octobre 2026 à 17:06:48 UTC, avant les nouveaux
calculs L. Les deux plans (50 décimales, N=32 ; 80 décimales, N=48) utilisent
douze corrections Euler–Maclaurin. Le premier choix de projection ω=1
et la première grille de contour de 256 arcs passent : les choix de recours
ω=i et 512/1024 arcs n’ont pas été exécutés. Aucun refus n’est effacé.

Le reste uniforme du premier plan est inférieur à $1,1\times10^{-28}$ pour
la composante d’ancre ; ses dérivées jusqu’à deux sont majorées par Cauchy.
Il s’agit d’un reste analytique, distinct des erreurs d’arrondi englobées
par les intervalles. Les jets sont recoupés en trois points avec Hurwitz en
haute précision ; ce contrôle utilise le même backend. La relecture rationnelle
recalcule ensuite les inclusions et contractions sans les opérations iv.
Elle ne réévalue pas indépendamment les primitives transcendantales.

Les correctifs d’implémentation et d’export sont datés ; codes exécutés et
premier export restent archivés. Les paramètres et bornes sont conservés.
Le diagnostic rationnel reproduit les quatre certificats à l’identique.

| Chemin relatif à `3_Preuves_et_calculs` | Fonction |
|:--|:--|
| `data/prevision_v642_certification.md` | Sélection et critères avant évaluation L |
| `data/v642_protocole_verrouille.json` | Empreintes, boîtes, graines et plans |
| `src/v642_intervalles.py` | Jets validés, reste analytique et contraction |
| `scripts/run_v642_certification.py` | Calcul des certificats et des essais |
| `data/v642_certification.json` | Deux validations du même pli exact, contour et quatre boîtes |
| `scripts/check_v642_certificate.py` | Vérification rationnelle des inégalités finies |
| `data/v642_verification_rationnelle.json` | Relecture rationnelle et portée exacte |
| `data/v642_root_audit_inputs.json` | Diagnostics postérieurs reproduisant les certificats |
| `preuves/V642_CERTIFICATION_LOCALE.md` | I1–I6, existence, unicité, Rouché et métriques |
| `preuves/V642_CONTRAT_ARITHMETIQUE.md` | A1–A2, forme et obstacle à la norme uniforme |

Pour rejouer, extraire une copie et déplacer `v642_certification.json` dans
un autre dossier : le lanceur refuse de l’écraser. Conserver le protocole
et les données V6.39/V6.41. Le diagnostic de relecture est documenté dans
les données ; les états historiques et reçus restent dans le ZIP.

```bash
cd 3_Preuves_et_calculs
python scripts/run_v642_certification.py
python scripts/check_v642_certificate.py
python tests/run_all_tests.py
cd ..
python 2_Methode/Outils/build_v642_figures.py
python 2_Methode/Outils/build_v642_document.py
```

Dépendances : Python, NumPy/SciPy et mpmath 1.3.0 ; figures Matplotlib ;
PDF Pandoc et XeLaTeX. La documentation du backend qualifie l’arithmétique
iv d’expérimentale ; les seules fonctions élémentaires utilisées, les
rectangles de calcul et les bornes d’erreur sont explicités.

**Suite locale :** choisir une des quatre directions de jets V6.41 et un
déplacement sur sa fibre exacte, à A, ancre et rayon constants ; fixer le
paramètre et les critères de transversalité avant calcul. La famille
radiale validée ici ne répond pas à cette autre question.

**Suite globale :** contrôler les corrélations signées et leur compensation
archimédienne sur la hiérarchie complète des tests admissibles. Le nouvel
opérateur de translations donne une cible calculable, mais sa norme sur L²
seul diverge. Une compression positive ou le compagnon local ne constitue
pas la borne uniforme exigée. L’autre porte, Q(X)=X^{o(1)} depuis les
premiers, demeure ouverte.

Les unités fictives du document 65 restent cohérentes : w porte T, les
moments m_k portent T^k et μ porte T². Les matrices et conditionnements
de I6 se lisent dans la base de hauteur normalisée par T. Les formes de
corrélation portent le carré de l’unité d’amplitude du test ; la traduction
en opérateurs n’identifie pas un Hamiltonien physique.

Le portail et ses indices couvrent les 66 documents. Le niveau de maturité
RH reste inchangé ; aucune relecture humaine nouvelle n’est revendiquée.
'''
    text=text.replace('—','-').replace('–','-')
    (P/(STEM+'.md')).write_text(text,encoding='utf-8-sig')

def compile_document():
    header=r'''\usepackage{etoolbox}
\usepackage{microtype}
\usepackage{float}
\floatplacement{figure}{H}
\setlength{\emergencystretch}{3em}
\setlength{\parskip}{0.35em}
\AtBeginEnvironment{longtable}{\small}
'''
    with tempfile.TemporaryDirectory(prefix='v642_pdf_') as directory:
        tmp=Path(directory);(tmp/'header.tex').write_text(header)
        args=['pandoc',STEM+'.md','-s','-f','markdown+tex_math_single_backslash','--resource-path=.','--include-in-header='+str(tmp/'header.tex'),'-V','geometry:margin=19mm','-V','papersize=a4','-V','mainfont=DejaVu Sans','-V','monofont=DejaVu Sans Mono','-V','fontsize=10pt','-V','lang=fr-FR','-o',STEM+'.tex']
        run=subprocess.run(args,cwd=P,capture_output=True,text=True);logs=run.stdout+run.stderr
        if run.returncode:raise RuntimeError(logs)
        source=P/(STEM+'.tex');source.write_text(source.read_text().replace('\\real{0.1429}','\\real{0.142857}'))
        for _ in range(2):
            run=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(tmp),STEM+'.tex'],cwd=P,capture_output=True,text=True);logs+=run.stdout+run.stderr
            if run.returncode:(D/'v642_pdf_compile.log').write_text(logs);raise RuntimeError(logs[-3500:])
        (D/'v642_pdf_compile.log').write_text(logs);shutil.copy2(tmp/(STEM+'.pdf'),P/(STEM+'.pdf'))
    print('Document 66 created: PDF, LaTeX, Markdown')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write-only',action='store_true');parser.add_argument('--compile-only',action='store_true');args=parser.parse_args()
    if not args.compile_only:write_markdown()
    if not args.write_only:compile_document()

if __name__=='__main__':main()
