"""Document 65: proofs, complete numerical balances, typed graph and open contracts."""
from pathlib import Path
from collections import Counter
import argparse
import json
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'1_Presentation'
D=ROOT/'3_Preuves_et_calculs/data'
STEM='65_FIBRES_PLIS_ET_POSITIVITE'
def load(name):return json.loads((D/name).read_text(encoding='utf-8-sig'))
def n(x,d=6):return f'{float(x):.{d}f}'.replace('.',',')

def write_markdown():
    folds=load('v641_collisions.json');blocks=load('v641_blocs_paires.json');geom=load('v641_geometrie.json')
    protocol=load('v641_protocole_verrouille.json')
    text=r'''# V6.41 — Fibres, plis et positivité : le graphe des passages

**Document 65 · Vincent P. P. NOËL · 12 octobre 2026**

Note de recherche et dossier LaTeX. Démonstrations auxiliaires, expériences
prospectives et deux relectures internes confrontées.

## 1. La clef locale trouvée, la clef globale encore cherchée

**La destination logique est connue : RH. Le chemin de preuve reste à
construire.** RH affirme que tous les zéros non triviaux de ζ ont partie
réelle 1/2. Une autre « destination » peut désigner l’objet intermédiaire
qui ferait réussir une preuve : nous en fixons deux, avec leurs
quantificateurs et leur implication finale.

Le changement d’objet utile est de suivre **la paire de zéros**, son centre
et son discriminant, au lieu de conserver à tout prix le nom de chacun des
deux zéros. Au point double, les étiquettes deviennent ambiguës ; la paire
non ordonnée possède encore un polynôme et un opérateur compagnon. Sous un
contour isolant, les moments les reconstruisent sans choix de branche.
Cette clef locale n’est pas une preuve de positivité globale.

| Obstacle précédent | Acquis V6.41 | Ce qui reste ouvert |
|:--|:--|:--|
| A complexe prescrit | Test exact de faisabilité : ellipse ; fibre S², singleton ou vide | Aucune affirmation d’accessibilité de tout le plan complexe à ancre et rayon fixés |
| D varie-t-il toujours à A fixé ? | Non : A=0 donne D≡1 ; variation générique démontrée à l’intérieur | Aucun sens uniforme du mouvement des zéros n’en découle |
| Zéros critiques doubles | Théorème conditionnel du pli ; 20 candidats recoupés, six attribués aux branches suivies | Existence et unicité certifiées par intervalles ; autres collisions et hauteurs |
| Passage entre branches | Paire sans étiquette, moments, discriminant et compagnon ; 18 blocs reconstruits | Contours continus isolants et couverture exhaustive non certifiés |
| Positivité liée à RH | Tests admissibles, densité, obstruction aux seuls préfixes finis, budget de Schur | Identité arithmétique et estimations uniformes pour ζ |

Les calculs sont annoncés comme des recoupements numériques. Le certificat
par intervalles présent concerne les sommes finies de phases et la géométrie
de A=0 ; il ne certifie pas les zéros des fonctions L.

**Deux portes vers RH.** Porte 1 : prouver la positivité de la forme
arithmétique de Weil sur chaque test admissible. Porte 2 : obtenir directement
depuis les nombres premiers une borne $Q(X)=X^{o(1)}$, puis appliquer le
théorème A du corpus. Les résultats locaux ci-dessous ne fournissent encore
ni l’une ni l’autre.

Fermer une voie sous des hypothèses précises est un progrès de discrimination.
Cela n’établit pas l’inexistence de tout chemin vers RH. Les noms « théorème »
et « lemme » désignent ici des énoncés accompagnés de preuves dans le corpus,
avec relecture interne ; ils ne désignent pas une validation externe nouvelle.

\newpage

## 2. Le graphe : ce qui mène à quoi

![Graphe des idées, énoncés, mesures et obstacles. Les flèches conditionnelles exigent les hypothèses indiquées ; les ponts ouverts ne sont pas des implications.](65_Graphe_des_passages.png){width=85%}

Le graphe interactif accompagne ce dossier : `65_GRAPHE_DES_PASSAGES.html`.
Chaque nœud expose son énoncé, ses hypothèses, ses relations et sa preuve ou
ses données. Le registre JSON permet de transformer la carte sans confondre
une analogie, une preuve, une observation et une question ouverte.

\newpage

## 3. Du coefficient complexe à une géométrie calculable

La famille V13 emploie les six caractères impairs modulo 13, indexés par
$k=1,3,5,7,9,11$. Leurs phases exactes $z_j$, de module 1, viennent des
sommes finies de Gauss et de la normalisation de l’équation fonctionnelle.
Les coefficients réels $c_j$ vérifient $\|c\|=1$ et
$A=\sum_jc_jz_j$. La carte étudiée fixe une ancre positive
$c_i=\cos r$, avec $0<r<\pi/4$, donc une ancre unique. Le cas $r=0$ et
une ancre négative demandent une autre carte.

Écrire $c=\cos r\,e_i+\sin r\,u$, $u_i=0$, $\|u\|=1$. Sur les cinq
coordonnées hors ancre, poser

\[
M_i=\begin{pmatrix}(\Re z_j)_{j\ne i}\\(\Im z_j)_{j\ne i}\end{pmatrix},
\quad G_i=M_iM_i^T,
\quad b={1\over\sin r}\binom{\Re(A-\cos r\,z_i)}{\Im(A-\cos r\,z_i)}.
\]

Le rang de $M_i$ est deux dans les recettes V13. Pour un $A$ prescrit,
définir $u_0=M_i^TG_i^{-1}b$ et $\eta=b^TG_i^{-1}b$.

**Théorème T1 — Faisabilité exacte.** La fibre est vide si $\eta>1$,
réduite à un point si $\eta=1$, et une sphère affine $S^2$ si $\eta<1$ :

\[
c=\cos r\,e_i+\sin r\left(u_0+\sqrt{1-\eta}\,Nv\right),
\qquad v\in S^2,
\]

où $N:\mathbb R^3\to\ker M_i$ est une isométrie, avec réinsertion de
la coordonnée nulle de l’ancre.

**Preuve.** $M_iM_i^TG_i^{-1}=I_2$, donc $M_iu_0=b$.
La solution $u_0$ appartient à l’image de $M_i^T$, orthogonale au noyau.
Toute solution est $u_0+w$, $w\in\ker M_i$, et
$\|u_0+w\|^2=\eta+\|w\|^2$. Le noyau a dimension trois : la norme
impose $\|w\|^2=1-\eta$, d’où les trois cas. □

Les cibles réalisables forment une ellipse pleine centrée en $\cos r\,z_i$,
de demi-axes $\sin r\sqrt{\lambda_j(G_i)}$. C’est le sens exact de
« A arbitraire » : toute cible prescrite est examinable, puis son
accessibilité est décidée. Le projecteur du noyau est
$I-M_i^TG_i^{-1}M_i$ ; le projecteur tangent à une fibre intérieure est
$N(I-vv^T)N^T$. Ainsi l’image devient un calcul d’opérateurs explicites.

![Ellipses à r=13/20 et A=0 intérieur pour les trois ancres représentatives. Les phases sont évaluées pour la figure ; les encadrements de faisabilité sont conservés dans le certificat.](65_Ellipses_et_fibres.png)

### D devient une cubique ; une voie universelle est fermée

Pour $\|c\|=1$, le défaut du corpus est

\[
D(c)=1+|A|^2-2\Re\left[A\sum_jc_j^3\overline{z_j}\right].
\]

Sur la fibre, il s’écrit $D(v)=C+P_1(v)+P_2(v)+P_3(v)$, avec $P_k$
homogène de degré $k$ : une forme linéaire, une matrice symétrique et un
tenseur cubique. Leur formule complète figure dans la note géométrique.

**Lemme L2.** D est constant sur la fibre intérieure si et seulement si
$P_2=q\|v\|^2$ pour un réel q et
$P_3+\|v\|^2P_1=0$ comme identités polynomiales.

**Preuve.** Comparer $v$ et $-v$ sur la sphère donne $P_1+P_3=0$.
Par homogénéité, cette égalité équivaut à la seconde identité pour tout v.
La partie paire est constante sur la sphère si et seulement si la matrice
de $P_2$ est scalaire. La réciproque résulte des mêmes identités. □

À $A=0$, **D≡1 exactement**. À $r=13/20$, ce cas est intérieur pour les
six ancres ; les représentants ont les encadrements suivants :

| Ancre | $\eta(A=0)$, encadrement |
|:--|:--|
| χ1 | [0,773778141912 ; 0,773778141913] |
| χ3 | [0,853767785835 ; 0,853767785836] |
| χ5 | [0,975929422513 ; 0,975929422514] |

Les ancres conjuguées donnent les mêmes valeurs. Au bord $\eta=1$, aucun
couple distinct ne peut être construit. Ces deux contreexemples réfutent
une variation pour toute cible compatible.

**Variation générique.** Les conditions de constance dépendent réellement
analytiquement de A à l’intérieur. Elles ne sont pas identiquement satisfaites,
puisque V6.39 démontre une variation au centre pour chaque ancre et rayon.
Leur lieu commun d’annulation est donc fermé sans intérieur ; son complément
est ouvert et dense. Cette conclusion n’est pas une variation universelle.

**Lemme L3 — Borne de contraction.**
$\sup D-\inf D\le12\sin^3 r\,|A|\sqrt{1-\eta}$.
En effet, pour $h(u)=\sum_{j\ne i}\Re(A\overline z_j)u_j^3$ sur la boule
unité, $\|\nabla h\|\le3|A|$. D a une constante de Lipschitz
$6\sin^3r|A|$ ; le diamètre de la fibre en u vaut $2\sqrt{1-\eta}$.
Cela prouve la borne et explique la disparition du contraste près de A=0
ou du bord. □

\newpage

## 4. Les jets : un filtre compatible, puis un pli sous conditions

Les fonctions de Hardy $Z_j(t)$ ont une normalisation commune réelle sur la
droite critique. Alors $Z_c(t)=\sum_jc_jZ_j(t)$. À une hauteur t fixée,
empiler les cinq contraintes :

\[
C_i(t)=\begin{pmatrix}e_i^T\\\Re z^T\\\Im z^T\\Z(t)^T\\Z'(t)^T\end{pmatrix},
\qquad b_i=\begin{pmatrix}\cos r\\\Re A\\\Im A\\0\\0\end{pmatrix}.
\]

**Lemme L4.** Si $\operatorname{rang}C_i=5$, poser
$c_0=C_i^T(C_iC_i^T)^{-1}b_i$, $\nu=\|c_0\|^2$ et choisir un vecteur
unitaire n du noyau. Les solutions normalisées sont deux points
$c_0\pm\sqrt{1-\nu}\,n$ si $\nu<1$, un point si $\nu=1$, aucune si
$\nu>1$.

**Preuve.** $c_0$ est orthogonal au noyau, qui a dimension un.
Toute solution vaut $c_0+\alpha n$ et sa norme carrée vaut
$\nu+\alpha^2$. □

À rang $q<5$, vérifier d’abord $b_i\in\operatorname{Im}C_i$ : si cette
compatibilité tient, la même preuve donne une sphère $S^{5-q}$ pour
$\nu<1$. Une matrice de Gram singulière ne doit pas être inversée.
Un candidat satisfait une multiplicité au moins deux ; il faut encore
$Z_c''\ne0$ pour une multiplicité exactement deux et une transversalité
dans le paramètre pour un pli.

**Bilan du plan fixé.** Les 120 lignes géométriques donnent 72 intérieures,
24 frontières à tolérance et 24 extérieures. Les lignes de centre sont
répétées par les deux axes : ce n’est pas un ensemble de 120 réplications
indépendantes. Les 36 sections testent χ1, χ3, χ5 ; t=5,10,15,20 ;
$\eta=0,1/4,1$ ; $r=\pi/6$. Deux sections donnent quatre candidats :

| Ancre et hauteur | A testé | $\nu$ numérique | $Z_{tt}$ des deux candidats |
|:--|:--|--:|:--|
| χ1, t=5 | Centre de l’ellipse | 0,8288412580 | 1,8221119005 ; 1,8594343625 |
| χ3, t=15 | Centre de l’ellipse | 0,9382168857 | −1,8333902743 ; −2,0420694137 |

Les 34 autres sections sont vides selon le diagnostic numérique ; aucune
absence pour toute hauteur ou toute cible A n’en résulte. Les rangs et jets
de cette étape utilisent Euler–Maclaurin et des différences centrées sans
borne d’erreur : ce sont des candidats, pas des collisions certifiées.

### Théorème T2 — Le pli critique double

Soit $Z(r,t)$ réel analytique, avec prolongement holomorphe local.
Supposer $Z=Z_t=0$ en $(r_*,t_*)$ et $Z_rZ_{tt}\ne0$.
La préparation de Weierstrass donne, pour $h=r-r_*$ et $x=t-t_*$,

\[
Z=U(h,x)\,[x^2+a_1(h)x+a_0(h)]
 =U(h,x)\,[\xi^2-\mu(h)],\qquad \xi=x+a_1(h)/2,
\]

où $U(0,0)\ne0$, $a_j(0)=0$, $\mu=a_1^2/4-a_0$, et

\[
\mu(0)=0,\qquad \mu'(0)=\kappa=-2Z_r/Z_{tt}\ne0.
\]

**Preuve.** La multiplicité deux en x autorise la préparation. La réalité
rend les coefficients réels pour h réel. Au point double,
$U(0,0)=Z_{tt}/2$ et $a_0'(0)=Z_r/U(0,0)$ ; dériver la définition de
$\mu$ donne la formule. Ainsi $\mu>0$ donne deux racines critiques simples,
$\mu<0$ une paire conjuguée en hauteur complexe, et $\mu=0$ un zéro
double. Le jacobien du système $(Z,Z_t)$ vaut $Z_rZ_{tt}$, donc le point
de collision est isolé localement. □

Le jet de Hasse d’ordre deux est ici le jet de Taylor divisé par les
factorielles : $Z_rh+\tfrac12Z_{tt}x^2+\cdots$. Son modèle
$x^2\simeq\kappa h$ est une approximation ; $\kappa h$ n’est pas le
discriminant exact à rayon fini. Aucun de ces énoncés n’est une assertion
sur tous les zéros de la famille.

\newpage

## 5. Traverser la collision sans perdre la paire

Prendre la coordonnée de hauteur $w=-i(s-1/2)$. Un zéro critique a w réel ;
le partenaire fonctionnel d’un zéro devient son conjugué en w. Sur un
contour contenant exactement deux zéros et aucun pôle, définir

\[
m_k={1\over2\pi i}\oint w^k{F_w\over F}\,dw.
\]

**Lemme L5 — Reconstruction sans étiquette.** Avec les multiplicités,
$m_0=2$, $m_1=w_1+w_2$, $m_2=w_1^2+w_2^2$. Ainsi

\[
a=m_1/2,\quad\Delta_w=2m_2-m_1^2=(w_1-w_2)^2,
\quad\mu=\Delta_w/4,
\quad H=\begin{pmatrix}a&1\\\mu&a\end{pmatrix}.
\]

**Preuve.** Le théorème des résidus donne les sommes de puissances.
L’identité de Newton fournit $\Delta_w$, et le polynôme caractéristique de
H est $(\lambda-a)^2-\mu$, de racines $w_1,w_2$. □

La matrice a un bloc de Jordan au zéro double. Pour a et μ réels,
$M=\operatorname{diag}(\mu,1)$ vérifie $H^TM=MH$.
Si $\mu>0$, M est définie positive ; si $\mu<0$, elle est indéfinie ;
au double, elle est singulière. La matrice $J=\begin{pmatrix}0&1\\1&0\end{pmatrix}$
donne aussi $H^TJ=JH$ et, après retrait du centre,
$J(H-aI)=\operatorname{diag}(\mu,1)$.

Cette métrique est reconstruite après connaissance de la paire : elle ne
force pas son signe. Elle n’est pas la forme de Weil pour ζ. Le changement
de variable est essentiel : $\Delta_s=-\Delta_w$. La positivité locale de
μ est donc à lire en hauteur w. Une perte d’isolation du contour ou un
compte autre que deux invalide ce bloc.

### Résultats prospectifs complets : 20 candidats de plis

Le verrou est daté du 12 octobre 2026 à **14:04:33 UTC**, avant les nouveaux
calculs de zéros. Les douze couples V6.39 et leurs empreintes sont conservés.
Les deux grilles du Wronskien, t∈[−25,25], ont les pas 0,01 et 0,005.
Elles repèrent les mêmes 20 candidats dans 0<r≤3/4. Tous sont recoupés
à 40 et 70 chiffres de travail par des jets explicites de Hurwitz.

Pour $Z=\cos r\,X+\varepsilon\sin r\,Y$, $\varepsilon=\pm1$, le
Wronskien $W=XY'-X'Y$ annule les candidats ; la recette `atan2` choisit
le quadrant du rayon. Les cas hors domaine et les rejets sont conservés.
Une grille de changements de signe n’épuise pas tous les zéros de W.

\begingroup
\renewcommand{\arraystretch}{0.85}

| Ancre | Membre | $r_*$, arrondi | $t_*$, signe conservé | $\kappa$, arrondi |
|:--|:--|--:|--:|--:|
'''
    for job in folds['jobs']:
        p=job['precisions'][-1]
        text+=f"| χ{job['character_k']} | {'+' if job['side']=='plus' else '−'} | {n(p['radius'])} | {n(p['height'])} | {n(p['kappa'])} |\n"
    text+=r'''
\endgroup

Les 20 valeurs de κ sont négatives dans ce plan. Ce résultat décrit ces
candidats ; ce n’est pas un signe universel pour V13. Résidus petits et
accord entre précisions ne prouvent ni existence et unicité par intervalles,
ni exhaustivité. Deux jets ont également été repris par `mp.diff` à 70
chiffres ; ce contrôle utilise le même backend et reste un recoupement de
formule.

\newpage

## 6. Branches, changement d’enveloppe et blocs numériques

Six graines héritées des racines V6.40 sont suivies sur les grilles
$\Delta r=1/200$ et $1/400$. Les quatre familles sont χ1 et χ5, membres
plus et moins. Les six branches de la grille fine sont attribuées à six
plis par les critères de proximité gelés. Sur la grille coarse, χ1 plus
est perdue au voisinage du pli : cette perte est conservée, et ne devient
ni une absence de zéro ni une continuation réussie.

![Les six branches suivies et leurs plis attribués. Les points sont des localisations numériques ; les lignes relient la continuation fine. La trajectoire radiale fait varier A.](65_Branches_et_plis.png)

Deux changements de branche éclairent l’enveloppe de détection du document
64. Pour χ1 moins, la branche de hauteur proche de −11 continue vers r=3/4,
mais une autre branche, née près de r=0,687215 à t=7,144416, intervient à
plus faible |t|. Pour χ5 plus, la branche de hauteur +19,6 est déjà présente
à r=0,45 ; une autre naît près de r=0,488252 à t=−15,775936 et intervient
à plus faible |t| à r=π/6. La première détection peut donc changer de
composante : ce n’est pas le déplacement d’une seule racine étiquetée.

Cette explication porte sur les branches suivies et l’enveloppe numérique
observée. Elle ne certifie pas le vrai premier zéro hors droite. Les suivis
radiaux ne sont pas des déplacements à A constant : A varie avec r. Les
sections de jets de la section 4 répondent séparément aux contraintes à
A fixé.

### 18 blocs et 24 racines, avec la collision conservée

Autour des six plis attribués, les rayons $r_*−10^{-4}$, $r_*$,
$r_*+10^{-4}$ donnent 18 blocs acceptés selon le protocole. Les cercles
en w ont rayon 0,2, avec 128/256 points et deux pas de différentiation.
Les comptes sont proches de deux et les moments concordent aux seuils
gelés. Les 24 racines aux deux rayons latéraux sont reprises à 40/70
chiffres et distinctes numériquement.

![Moments de contour et modèle linéaire du jet autour des six plis. Au rayon central, un petit discriminant numérique n’est pas présenté comme une annulation exacte.](65_Discriminants_des_paires.png)

Avant le pli ($h<0$), les six blocs ont $\Delta_w>0$ et deux racines
critiques ; après ($h>0$), $\Delta_w<0$ et une paire hors ligne. Le rayon
central porte le statut `near_collision`, sans imposer μ=0 aux résultats
flottants. Les résidus imaginaires des invariants sont conservés et contrôlés.
Les métriques réelles affichées utilisent ces invariants réels dans le
modèle conditionnel ; elles ne certifient pas leur réalité exacte.

Les minima du bord sont **échantillonnés**. Sans borne sur tout le contour,
ces données ne démontrent pas qu’il isole exactement deux zéros. Le bloc
de la section 5 est exact sous cette hypothèse ; son instance numérique
reste à certifier.

### Unités fictives cohérentes

Les coefficients normalisés c, les phases z et D sont sans dimension.
Introduire une unité fictive $\mathsf C$ pour les coefficients effectifs
$\mathsf Cc$ : A et F portent alors $\mathsf C$, et les dérivées
spectrales portent $\mathsf C/\mathsf T^k$ si w porte une unité
$\mathsf T$. Les moments $m_k$ ont l’unité $\mathsf T^k$ ;
$\Delta_w$ et μ portent $\mathsf T^2$. Le rapport $F_w/F$ élimine
l’unité $\mathsf C$.

La matrice dimensionnellement homogène est
$\widetilde H=\begin{pmatrix}a/\mathsf T&1\\\mu/\mathsf T^2&a/\mathsf T\end{pmatrix}$,
avec spectre $w_j/\mathsf T$ ; l’opérateur $\mathsf T\widetilde H$
porte $\mathsf T$. Une énergie fictive $\mathsf E D$ porte
$\mathsf E$ ; sa dérivée par rapport à un temps porte
$\mathsf E/\mathsf T$. Une énergie positive n’impose pas une dérivée
positive. Ces unités accompagnent les calculs sans identifier un
Hamiltonien physique.

\newpage

## 7. La porte globale : tests, limite, queue et couplage

Le critère de Weil publié [CC21] est indépendant des expériences V13.
Dans la convention Fourier de son introduction, les distributions locales
satisfont RH si et seulement si leur somme est non positive sur les
autocorrélations admissibles. Nous prenons son opposée :

\[
E=\left\{f\in C_c^\infty(\mathbb R):\int f(x)e^{\pm x/2}\,dx=0\right\},
\quad Q_W(f)=-\sum_vW_v(g*g^*),\quad g(u)=f(\log u).
\]

Ici $g^*(u)=\overline{g(u^{-1})}$, la convolution multiplicative utilise
$du/u$, et l’involution additive est $f^*(x)=\overline{f(-x)}$.
Dans cette convention : $Q_W(f)\ge0$ pour chaque $f\in E$ équivaut à RH.
Les annulations correspondent aux deux points polaires. La convention
Mellin de l’appendice C emploie un changement de normalisation ; elle ne
se substitue pas terme à terme à la convention Fourier.

La source fournit le critère global et un résultat archimédien à support
restreint ; ce dernier n’est pas une positivité globale de toute la forme
arithmétique. Notre vérification primaire porte sur le critère et ses
conditions, pas sur une validation de l’article entier.

### Lemme G1 — Construire tous les tests admissibles

Avec $P=\partial_x^2-1/4$, on a $E=P C_c^\infty(\mathbb R)$.

**Preuve.** Deux intégrations par parties donnent
$\int e^{\pm x/2}P\psi=\int P(e^{\pm x/2})\psi=0$.
Réciproquement, pour $f\in E$, poser
$\psi(x)=\int_{-\infty}^x2\sinh((x-y)/2)f(y)\,dy$.
La différentiation donne $P\psi=f$. À gauche du support, ψ est nulle ;
à droite elle vaut
$e^{x/2}\int e^{-y/2}f(y)dy-e^{-x/2}\int e^{y/2}f(y)dy=0$.
Elle est lisse et compacte. Le noyau de P sur les fonctions compactes est
nul, car une combinaison des deux exponentielles ne peut être compacte. □

L’opérateur élimine les contraintes d’admissibilité. Il n’impose pas le
signe de $Q_W(P\psi)$.

### Lemme G2 — Une hiérarchie dense, avec un contrat de limite

Choisir $\chi_L\in C_c^\infty((-L-1,L+1))$ égale à 1 sur [−L,L], et poser

\[
E_{L,N}=\operatorname{span}_{|n|\le N}
P\left(\chi_L(x)e^{in\pi x/(L+1)}\right).
\]

Ces espaces sont inclus dans E et emboîtés en N pour L fixé. Leur réunion
sur L,N est dense dans la topologie des tests.

**Preuve.** Écrire $f=P\psi$ par G1 ; choisir L tel que le support de ψ
soit contenu dans (−L,L). Son prolongement périodique de période 2(L+1)
est lisse. Ses sommes de Fourier convergent avec toutes les dérivées.
Multiplier par $\chi_L$ puis appliquer P donne une approximation de f,
avec support compact commun et convergence de toutes les dérivées. □

Si une forme hermitienne est continue dans cette topologie et positive sur
**tous** les $E_{L,N}$, elle est positive sur E, en passant à la limite.
Pour des compressions approchées, il faut notamment

\[
|Q_W(f_N)-\widetilde Q_{L,N}(f_N)|
\le\varepsilon_{L,N}\|f_N\|_*^2\longrightarrow0,
\]

avec une minoration compatible tendant vers zéro et une norme justifiée.
Cette erreur et cette minoration ne sont pas établies pour ζ dans le corpus.
La densité rend le but précis ; elle ne fournit pas le signe manquant.

\newpage

### Théorème G3 — Les seuls préfixes finis ne suffisent pas

Pour chaque M, sur $\ell^2(\mathbb N)$,
$K_M=I-2|e_{M+1}\rangle\langle e_{M+1}|$ est borné autoadjoint de norme 1.
Ses compressions aux n premières coordonnées sont $I_n$ pour $n\le M$,
mais $\langle e_{M+1},K_Me_{M+1}\rangle=-1$.

**Preuve.** Le rang un est orthogonal aux M premières coordonnées et vaut
1 sur $e_{M+1}$. □

Un procédé ne disposant que de ces préfixes ne distingue donc pas I de
$K_M$. C’est une impossibilité sur les opérateurs arbitraires avec ces
seules données. Une identité arithmétique ou une borne uniforme peut
changer les hypothèses. **Ce n’est pas une impossibilité de prouver RH.**

### Lemme G4 — Contrôler la queue et le couplage

Pour un opérateur borné autoadjoint
$K=\begin{pmatrix}\mathcal A&B\\B^*&C\end{pmatrix}$,
$\mathcal A\ge aI$ avec $a>0$,

\[
K\ge0\iff C-B^*\mathcal A^{-1}B\ge0.
\]

**Preuve.** Compléter le carré donne

\[
\langle(x,y),K(x,y)\rangle
=\|\mathcal A^{1/2}(x+\mathcal A^{-1}By)\|^2
+\langle y,(C-B^*\mathcal A^{-1}B)y\rangle.
\]

Choisir $x=-\mathcal A^{-1}By$ démontre la nécessité ; la même identité
prouve la suffisance. En particulier, $C\ge cI$, $c\ge0$ et
$\|B\|^2\le ac$ suffisent, car $\mathcal A^{-1}\le a^{-1}I$. □

Il faut les trois estimations : marge du bloc, minoration de la queue,
norme du couplage. Une marge a qui tend vers zéro peut rendre ce budget
insuffisant. Pour une forme non bornée, domaines et fermeture demandent
un autre travail. Nous n’avons pas construit un opérateur K pour ζ
satisfaisant déjà ces hypothèses.

### La deuxième porte : la croissance de l’énergie arithmétique

Le théorème A du corpus établit

\[
{1\over2}\limsup_{X\to\infty}{\log(1+Q(X))\over\log X}
=\Theta-{1\over2},\qquad
\mathrm{RH}\iff Q(X)=X^{o(1)}.
\]

Il donne une implication exploitable dès qu’une borne suffisante est
obtenue indépendamment de RH depuis les premiers. La positivité
$Q(X)\ge0$ ne contrôle pas cette croissance. Le théorème B suppose RH ;
l’utiliser pour prouver RH sans lever cette hypothèse serait circulaire.
Ces deux théorèmes gardent leur portée antérieure. La note 65 ajoute des
outils et des contre-épreuves, sans ajouter la borne globale manquante.

\newpage

## 8. Les étapes ultérieures, avec critères d’arrêt

| Étape | Travail à réaliser | Condition de réussite ou conclusion utile |
|:--|:--|:--|
| 1. Certifier un pli local | Choisir avant calcul un des six plis attribués ; jet analytique, boîte rationnelle, Newton/Krawczyk par intervalles ; contour continu | Existence et unicité dans la boîte, $Z_rZ_{tt}\ne0$, deux zéros isolés ; sinon obstacle chiffré conservé |
| 2. Déployer à A fixé | Choisir une des deux sections de jets faisables ; paramétrer une géodésique de la fibre exacte ; tester la transversalité | Collision et paramètre compatibles avec A, ancre et rayon constants ; sinon rang, dégénérescence ou incompatibilité identifiés |
| 3. Fixer la porte globale | Spécifier la forme arithmétique, le domaine et la topologie ; construire la hiérarchie G1–G2 et l’expression depuis les premiers | Un contrat de signe ou de croissance écrit sans supposer RH ; absence du pont explicitement démontrée si les objets diffèrent |
| 4. Chercher l’inégalité manquante | Minorer la queue et borner le couplage, ou majorer Q(X) de façon uniforme | Hypothèses et quantificateurs établis ; sinon témoin négatif ou limite de méthode |

Ces étapes sont des programmes de recherche, pas des résultats déjà obtenus.
Les nouveaux calculs devront être précédés d’un nouveau verrou : aucune
sélection postérieure parmi les quatre candidats de jets n’est présentée
comme une prévision réalisée. L’extension du seul plafond ne répond à
aucun des contrats globaux.

Le modèle Bellman courant ajoute aux neuf actions historiques : le dossier
de passages V13, achevé ; la certification d’un bloc local ; l’audit du
contrat global. Coûts H et utilités U sont conventionnels. Un rapport
concluant à un obstacle compte comme livrable, sans recevoir le statut de
preuve de RH. Les ex aequo sont conservés. Le calcul optimise le modèle
documentaire déclaré, pas les chances de résoudre un problème ouvert.

![Modèle courant : neuf actions restantes après les trois actions V13 achevées. La fréquence sur 243 profils est une sensibilité aux poids conventionnels, pas une probabilité de succès.](65_Bellman_sensibilite.png)

## 9. Sources, preuves et reproduction

**[CC21]** A. Connes et C. Consani, *Weil positivity and Trace formula,
the archimedean place* (2021), introduction (4), appendices A–C et
proposition C.1. [PDF auteur](https://alainconnes.org/wp-content/uploads/Selecta.pdf) ;
[prépublication](https://arxiv.org/abs/2006.13771). Vérification primaire
du critère, de l’involution et du changement de normalisation ; validation
de l’ensemble de l’article non revendiquée.

Les résultats de fibres, jets et plis sont démontrés dans les trois notes
ci-dessous. Les préparations de Weierstrass, résidus, pseudo-inverses et
compléments de Schur sont des outils classiques ; aucune nouveauté générale
de ces outils n’est revendiquée. Le résultat de recherche ici est leur
assemblage explicite, ses restrictions, ses contreexemples et le protocole
appliqué aux familles exactes du corpus.

| Chemin relatif à `3_Preuves_et_calculs` | Contenu |
|:--|:--|
| `preuves/V641_GEOMETRIE_ET_OPERATEURS.md` | Fibres, cubique, constance, contractions, sections de jets et audit constructif |
| `preuves/V641_COLLISIONS_ET_LIMITES.md` | Wronskien, pli, moments, opérateurs, audit critique |
| `preuves/V641_PASSAGE_AU_GLOBAL.md` | G1–G4, signe Weil et deux portes globales |
| `data/v641_protocole_verrouille.json` | Empreintes, graines et seuils antérieurs aux calculs |
| `data/v641_branches.json` | Deux grilles, six graines et perte conservée |
| `data/v641_wronskiens.json` | Toutes les détections et tous les rejets |
| `data/v641_collisions.json` | Les 20 recoupements et 11 attributions de grille à six plis |
| `data/v641_blocs_paires.json` | 18 blocs, moments, marges échantillonnées, 24 racines |
| `data/v641_geometrie.json` | 120 lignes géométriques et 36 sections de jets |
| `data/v641_certificat_fibres.json` | Intervalles des phases et faisabilité de A=0 |
| `data/v641_graphe_recherche.json` | Nœuds, statuts, preuves et types de flèches |

Pour rejouer, travailler sur une copie et déplacer les sorties de la phase
concernée : le lanceur refuse de les écraser. Le manifeste V6.39, les
données V6.40 et les prévisions originales sont conservés. Les nouvelles
notes de lecture suivent l’encodage Markdown du corpus ; les reçus originaux
restent inchangés dans `4_Archives/recus/V641`.

```bash
cd 3_Preuves_et_calculs
python scripts/run_v641_passages.py --phase branches
python scripts/run_v641_passages.py --phase scan
python scripts/run_v641_passages.py --phase collisions
python scripts/run_v641_passages.py --phase blocks
python scripts/run_v641_passages.py --phase geometry
python tests/run_all_tests.py
cd ..
python 2_Methode/Outils/build_v641_graph.py
python 2_Methode/Outils/build_v641_document.py
```

Dépendances : NumPy, SciPy, pandas, mpmath 1.3.0 ; figures Matplotlib ; PDF
Pandoc et XeLaTeX. Les jets d’ordre deux utilisent les dérivées de Hurwitz
explicites. Le raccourci `mpmath.dirichlet(..., derivative=2)` n’est pas
employé : cette version ne fournit pas ce contrat, même si elle accepte
l’argument. Les tests comparent les jets à des différentiations numériques.

Le portail, les sources, la carte, la matrice, l’indicateur, le navigateur,
l’atlas et la liste des figures donnent le bilan V6.41. Les états et PDF
historiques restent identifiés comme tels. Les niveaux de maturité RH
ne montent pas du fait d’un nouveau graphe ou d’un nouveau recoupement local.
'''
    (P/(STEM+'.md')).write_text(text,encoding='utf-8-sig')

def compile_document():
    header=r'''\usepackage{etoolbox}
\usepackage{microtype}
\usepackage{float}
\floatplacement{figure}{H}
\setlength{\emergencystretch}{3em}
\setlength{\parskip}{0.35em}
\AtBeginEnvironment{longtable}{\small}
\AtBeginDocument{\hypersetup{colorlinks=true,linkcolor=blue!45!black,urlcolor=blue!45!black}}
'''
    with tempfile.TemporaryDirectory(prefix='v641_pdf_') as directory:
        tmp=Path(directory);(tmp/'header.tex').write_text(header)
        args=['pandoc',STEM+'.md','-s','-f','markdown+tex_math_single_backslash',
          '--resource-path=.','--include-in-header='+str(tmp/'header.tex'),
          '-V','geometry:margin=19mm','-V','papersize=a4','-V','mainfont=DejaVu Sans',
          '-V','monofont=DejaVu Sans Mono','-V','fontsize=10pt','-V','lang=fr-FR','-o',STEM+'.tex']
        run=subprocess.run(args,cwd=P,capture_output=True,text=True);logs=run.stdout+run.stderr
        if run.returncode:raise RuntimeError(logs)
        source=P/(STEM+'.tex');source.write_text(source.read_text().replace('\\real{0.1429}','\\real{0.142857}'))
        for _ in range(2):
            run=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(tmp),STEM+'.tex'],cwd=P,capture_output=True,text=True)
            logs+=run.stdout+run.stderr
            if run.returncode:(D/'v641_pdf_compile.log').write_text(logs);raise RuntimeError(logs[-4500:])
        (D/'v641_pdf_compile.log').write_text(logs)
        shutil.copy2(tmp/(STEM+'.pdf'),P/(STEM+'.pdf'))
    print('Document 65 compiled: PDF, LaTeX and Markdown')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write-only',action='store_true');parser.add_argument('--compile-only',action='store_true');args=parser.parse_args()
    if not args.compile_only:write_markdown()
    if not args.write_only:compile_document()

if __name__=='__main__':main()
