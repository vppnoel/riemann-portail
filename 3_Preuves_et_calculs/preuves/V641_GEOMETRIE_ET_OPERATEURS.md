# V6.41 — Fibres complexes, sections de jets et opérateurs de passage

Date : 12 octobre 2026. Statut : démonstrations internes en dimension finie ; géométrie et algèbre classiques appliquées aux conventions exactes de V13. Les applications aux collisions sont conditionnelles. Cette note ne démontre ni une collision effective de la famille étudiée, ni une propriété globale des zéros, ni RH.

## 1. Une représentation qui garde les contraintes visibles

L'image utile est un **faisceau de fibres au-dessus d'une ellipse**, traversé par une **surface de zéros**. Elle sépare deux projections qui ne doivent pas être confondues.

La première projection associe à un vecteur de coefficients son premier coefficient complexe : $c\mapsto A(c)$. Son bord peut être calculé exactement par algèbre linéaire. La seconde projection associe à une paire $(c,s)$ satisfaisant $F_c(s)=0$ son vecteur $c$. Elle est localement régulière à un zéro simple et peut se ramifier à un zéro multiple. Le bord de l'ellipse n'est pas le lieu des collisions de zéros.

| Image | Objet symbolique | Opérateur effectivement disponible |
|---|---|---|
| Disque elliptique des cibles | $A\in t z_i+s\{b:b^TG_i^{-1}b\le1\}$ | $M_i$, $M_i^+$, $G_i=M_iM_i^T$ |
| Sphère au-dessus d'une cible intérieure | $u=u_0+\rho Nv$, $v\in S^2$ | projecteur $P_K=I-M_i^+M_i$ |
| Directions permises sur une fibre | $\dot u\in T_u\mathcal F_A$ | $N(I-vv^T)N^T$ |
| Surface de zéros au-dessus des coefficients | $F_c(s)=0$ | évaluation $\mathcal E_s:c\mapsto F_c(s)$ |
| Pli ou collision candidate | $Z_c(t)=\partial_t Z_c(t)=0$ | jets $\mathcal J_t:c\mapsto(Z_c(t),Z_c'(t))$ |
| Paire suivie sans étiquettes individuelles | moments d'un contour isolant deux zéros | $F'/F$ et matrice compagnon $2\times2$ |

Cette représentation permet de changer de coordonnées sans changer le problème. Une image seule n'impose cependant ni le rang des jets, ni le signe d'une forme arithmétique.

## 2. Conventions exactes et carte locale d'ancre

Les six caractères impairs modulo 13 portent les indices $k=1,3,5,7,9,11$. Les phases exactes $z_j$ sont celles de V6.39 : $|z_j|=1$ et $z_{j^*}=\overline{z_j}$. La recette par sommes de Gauss et demi-angle fixe la branche. Le rang requis ci-dessous est garanti pour toutes les ancres par les mineurs non nuls démontrés dans `LEMME_CONTRAINTES_V13_V639.md` ; il ne dépend pas d'une conjecture sur les zéros.

On fixe une ancre $i$ et un rayon **strictement** compris entre $0$ et $\pi/4$. Écrire $t=\cos r$, $s=\sin r$. La carte choisit le représentant de phase $c_i=+t$ et impose $\|c\|_2=1$. Alors

\[
c=t e_i+s u,\qquad u_i=0,\qquad\|u\|_2=1.
\]

Comme $|c_j|\le s<t$ pour $j\ne i$, l'ancre projective est unique et sa distance angulaire est exactement $r$. Le représentant $c_i=-t$ donne une autre carte, de centre $-t z_i$ ; il n'est pas inclus tacitement dans la carte positive. À $r=0$, la fibre est simplement $\{e_i\}$ si $A=z_i$, et vide sinon. La division par $\sin r$ n'y est pas autorisée.

## 3. Théorème — Tout coefficient complexe prescrit a un test exact de faisabilité

Retirer la coordonnée $i$ et identifier $u$ à un vecteur de $\mathbb R^5$. Définir

\[
M_i=\begin{pmatrix}(\Re z_j)_{j\ne i}\\(\Im z_j)_{j\ne i}\end{pmatrix},
\quad G_i=M_iM_i^T,
\quad b=\frac1s\begin{pmatrix}\Re(A-tz_i)\\\Im(A-tz_i)\end{pmatrix}.
\]

La matrice $M_i$ est de rang deux et $G_i$ est définie positive. Posons

\[
R_i=M_i^T G_i^{-1},\qquad
u_0=R_i b,\qquad
\eta=b^TG_i^{-1}b,\qquad P_K=I_5-R_iM_i.
\]

**Théorème 1.** Dans la carte d'ancre précédente, l'ensemble des vecteurs normalisés ayant le coefficient complexe $A$ est :

- vide si $\eta>1$ ;
- un singleton si $\eta=1$ ;
- une sphère affine de dimension deux si $\eta<1$.

Dans le dernier cas, pour toute isométrie $N:\mathbb R^3\to\ker M_i$,

\[
\boxed{c=t e_i+s\bigl(u_0+\sqrt{1-\eta}\,Nv\bigr),\qquad v\in S^2.} \tag{1}
\]

La notation inclut la réinsertion d'une coordonnée nulle à l'indice $i$ dans le terme entre parenthèses.

**Démonstration.** On a $M_iR_i=I_2$. Ainsi $u_0$ résout $M_iu=b$ et appartient à l'image de $M_i^T$, orthogonale au noyau. Toute autre solution est exactement $u_0+w$ avec $w\in\ker M_i$. Puis

\[
\|u_0\|^2=b^TG_i^{-1}M_iM_i^TG_i^{-1}b=\eta,
\qquad \|u_0+w\|^2=\eta+\|w\|^2.
\]

La norme prescrite $1$ équivaut donc à $\|w\|^2=1-\eta$. Le noyau a dimension $5-2=3$. Les trois cas annoncés en découlent. La formule (1) préserve la norme, l'ancre, le rayon et les deux composantes de $A$. $\square$

**Corollaire.** Les cibles réalisables sont exactement une ellipse pleine de centre $t z_i$. Dans les coordonnées complexes identifiées à $\mathbb R^2$, ses demi-axes ont pour longueurs

\[
s\sqrt{\lambda_1(G_i)},\qquad s\sqrt{\lambda_2(G_i)}.
\]

Le mot « arbitraire » signifie donc **toute cible prescrite, après test de compatibilité**. Il ne signifie pas que tout $A\in\mathbb C$ serait accessible à ancre et rayon fixés. V6.39 avait construit uniquement le centre de cette ellipse, où $b=0$, $u_0=0$ et la fibre est le noyau unitaire.

Le projecteur $P_K$ est symétrique, idempotent et de rang trois. Au point $v\in S^2$ d'une fibre intérieure, le projecteur sur les déplacements infinitésimaux permis dans les cinq coordonnées est

\[
P_T(v)=N(I_3-vv^T)N^T.
\]

Il a rang deux. Les déplacements $\dot c=s\rho N\dot v$, avec $v^T\dot v=0$, préservent exactement $A$, l'ancre et le rayon à l'ordre infinitésimal. Ici $\rho=\sqrt{1-\eta}$.

## 4. Le défaut sur une fibre devient un polynôme cubique

Pour des coefficients de norme un, le défaut du corpus est

\[
D(c)=1+|A|^2-2\Re\left[A\sum_j c_j^3\overline{z_j}\right].
\]

Avec $\beta_j=\Re(A\overline{z_j})$, $a=u_0$ et $n_j^T$ la ligne $j$ de $N$, la fibre (1) donne

\[
D(v)=1+|A|^2-2t^3\beta_i
-2s^3\sum_{j\ne i}\beta_j(a_j+\rho n_j^Tv)^3. \tag{2}
\]

Ainsi $D(v)=C+P_1(v)+P_2(v)+P_3(v)$, les $P_k$ étant homogènes de degré $k$ :

\[
\begin{aligned}
P_1(v)&=-6s^3\rho\sum_j\beta_j a_j^2(n_j^Tv),\\
P_2(v)&=-6s^3\rho^2\sum_j\beta_j a_j(n_j^Tv)^2,\\
P_3(v)&=-2s^3\rho^3\sum_j\beta_j(n_j^Tv)^3.
\end{aligned}
\]

Les sommes portent sur les cinq indices hors de l'ancre. Il s'agit d'une traduction explicite en une forme linéaire, une forme quadratique symétrique et un tenseur cubique symétrique. Aucun nouveau zéro n'est utilisé pour la construire.

**Lemme 2 — Critère exact de constance.** Sur une fibre intérieure, $D$ est constant si et seulement s'il existe un réel $q$ tel que

\[
P_2(v)=q\|v\|^2,
\qquad P_3(v)+\|v\|^2P_1(v)=0
\quad\text{comme identités polynomiales.} \tag{3}
\]

**Démonstration.** Si $D$ est constant sur $S^2$, les évaluations en $v$ et $-v$ donnent $P_1(v)+P_3(v)=0$. Pour tout $v\ne0$, appliquer cette égalité à $v/\|v\|$ puis multiplier par $\|v\|^3$ donne $P_3(v)+\|v\|^2P_1(v)=0$. L'identité se prolonge à zéro. La partie paire $C+P_2$ est constante sur $S^2$ : diagonaliser sa matrice symétrique montre que les trois valeurs propres de $P_2$ sont égales. Donc $P_2=q\|v\|^2$. Réciproquement, (3) donne $D(v)=C+q$ lorsque $\|v\|=1$. $\square$

Le critère est invariant par changement de base orthonormée du noyau. En coordonnées de tenseur, si $P_1=L\cdot v$, $P_2=v^TQv$ et $P_3=T[v,v,v]$, il s'écrit $Q=(\operatorname{tr}Q/3)I$ et

\[
T_{abc}+\frac{\delta_{ab}L_c+\delta_{ac}L_b+\delta_{bc}L_a}{3}=0.
\]

Un petit résidu numérique de ces identités est un diagnostic. Il ne démontre pas leur annulation exacte.

## 5. Deux obstacles réels à une variation uniforme de D

**Contreexemple intérieur.** Si $A=0$, la définition donne exactement $D(c)=1$ pour tout vecteur normalisé de la fibre. Ce cas est effectivement réalisable dans V13 à $r=13/20<\pi/4$, pour chacune des six ancres. Le certificat des sommes finies de Gauss à 80 décimales donne :

| Ancre représentative | Encadrement de $\eta(A=0)$ | Marge $1-\eta$, minorée |
|---|---|---|
| $k=1$ | $[0.773778141912,0.773778141913]$ | $0.226221858087$ |
| $k=3$ | $[0.853767785835,0.853767785836]$ | $0.146232214164$ |
| $k=5$ | $[0.975929422513,0.975929422514]$ | $0.024070577486$ |

Les autres ancres donnent les mêmes valeurs par conjugaison. La séparation stricte de $\eta$ et $1$ garantit une fibre intérieure ; le caractère constant de $D$ vient de l'identité $A=0$, pas d'un échantillonnage de points.

**Contreexemple de bord.** Au bord de l'ellipse, la fibre est un singleton. Il n'existe donc aucun couple distinct à comparer. Une recette exacte de bord, disponible pour chaque ancre, est

\[
u_j=\frac{\Re z_j}{\sqrt{\sum_{\ell\ne i}(\Re z_\ell)^2}},\quad j\ne i.
\]

Elle vérifie $\|u\|=1$ et $u\in\operatorname{Im}(M_i^T)$. Son image $b$ a exactement $b^TG_i^{-1}b=1$. Cette égalité est démontrée algébriquement ; un intervalle numérique contenant $1$ ne suffirait pas à la prouver.

**Corollaire — Variation générique, sans borne uniforme.** Pour une ancre et un rayon fixés, l'ensemble des cibles intérieures où $D$ est non constant est ouvert et dense dans l'ellipse intérieure.

**Démonstration.** Choisir $N$ une fois pour toutes. Les coefficients des conditions (3) dépendent réellement analytiquement de $A$ sur l'ellipse intérieure : $u_0$ est affine en $A$ et $\rho=\sqrt{1-\eta}$ y est analytique. La somme des carrés des coefficients de $Q-(\operatorname{tr}Q/3)I$ et de $P_3+\|v\|^2P_1$ est une fonction analytique $R(A)\ge0$. Son annulation équivaut à la constance. Au centre $A=t z_i$, V6.39 démontre une variation stricte ; donc $R$ n'est pas identiquement nulle. Sur le domaine intérieur connexe, son lieu d'annulation n'a pas d'intérieur. Son complément est ouvert et dense. $\square$

Ce résultat ne donne ni un signe pour un déplacement de zéro, ni un contraste minimal. L'existence d'un cas intérieur constant exclut précisément une conclusion universelle.

**Lemme 3 — Contraction de la plage du défaut.** Sur toute fibre intérieure,

\[
\boxed{\sup D-\inf D\le12\sin^3(r)|A|\sqrt{1-\eta}.} \tag{4}
\]

**Démonstration.** Pour $h(u)=\sum_{j\ne i}\beta_j u_j^3$ sur la boule unité,

\[
\|\nabla h(u)\|\le3|A|\left(\sum_j u_j^4\right)^{1/2}\le3|A|.
\]

Le segment entre deux points de la fibre reste dans cette boule, et leur distance est au plus $2\rho$. La formule (2) donne une constante de Lipschitz $6s^3|A|$ pour $D$ comme fonction de $u$. D'où (4). $\square$

La plage se contracte donc lorsque $A\to0$ ou lorsque la cible approche le bord. Le bord géométrique est une obstruction mesurable à la précision d'un contraste, même sans collision de zéros.

## 6. Sections de jets — Construire des candidats de collision à A fixé

Soit $Z_j(t)$ la complétion exacte réelle du terme $z_jL(1/2+it,\chi_j)$ sur la droite critique. Les caractères ont même conducteur et même parité, donc le facteur de complétion est commun. La fonction

\[
Z_c(t)=\sum_j c_jZ_j(t)
\]

est réelle pour $t\in\mathbb R$ et possède un prolongement analytique local en $t$. Utiliser le facteur gamma exact, ou démontrer l'équivalence des jets après retrait d'un facteur réel non nul, est nécessaire avant une certification.

Pour une hauteur réelle fixée, définir

\[
C_i(t)=\begin{pmatrix}
e_i^T\\\Re z^T\\\Im z^T\\Z(t)^T\\Z'(t)^T
\end{pmatrix},
\qquad b_i=\begin{pmatrix}t_r\\\Re A\\\Im A\\0\\0\end{pmatrix},
\qquad t_r=\cos r.
\]

Le symbole $t_r$ évite de confondre le cosinus du rayon avec la hauteur $t$. Les contraintes $C_i(t)c=b_i$ imposent ancre, coefficient complexe, zéro critique et jet d'ordre un nul.

**Lemme 4 — Section de collision de rang cinq.** Supposons $\operatorname{rang}C_i(t)=5$. Posons

\[
c_0=C_i(t)^T[C_i(t)C_i(t)^T]^{-1}b_i,
\qquad\nu=\|c_0\|^2,
\]

et soit $n$ un vecteur unitaire de son noyau, de dimension un. Les solutions normalisées sont exactement

\[
\begin{cases}
\varnothing,&\nu>1,\\
\{c_0\},&\nu=1,\\
\{c_0+\sqrt{1-\nu}\,n,\ c_0-\sqrt{1-\nu}\,n\},&\nu<1.
\end{cases} \tag{5}
\]

**Démonstration.** La matrice possède un inverse à droite, donc les contraintes sont compatibles. Le vecteur $c_0$ est leur solution de norme minimale et est orthogonal au noyau. Toute solution est $c_0+\alpha n$, de norme carrée $\nu+\alpha^2$. L'équation de norme donne (5). Le rayon strict $r<\pi/4$ garantit l'ancre unique comme dans la section 2. $\square$

Ces candidats satisfont une multiplicité **au moins deux**. La multiplicité est exactement deux seulement si $Z_c''(t)\ne0$. Une collision donnant un pli de branches exige également une transversalité dans le paramètre de déplacement. Un rang numérique apparent de cinq, ou un petit résidu de jets, ne certifie aucune de ces hypothèses.

**Rangs inférieurs.** Avec $q=\operatorname{rang}C_i(t)<5$, il faut d'abord imposer $b_i\in\operatorname{Im}C_i(t)$. Si cette compatibilité échoue, la section est vide. Si elle réussit, la pseudo-inverse définit $c_0=C_i(t)^+b_i$ et la même preuve donne une sphère $S^{5-q}$ pour $\nu<1$, un singleton pour $\nu=1$, et une section vide pour $\nu>1$. On ne doit pas inverser une matrice de Gram singulière.

Le passage « ellipse faisable → section de jets faisable » est une nouvelle question. La condition $\eta\le1$ ne garantit pas $\nu\le1$. Le lemme décrit un calcul pour chercher des collisions compatibles, sans annoncer qu'elles existent.

## 7. L'opérateur de déplacement d'un zéro simple

Écrire $B_j(s)=z_jL(s,\chi_j)$ et $F_c(s)=\sum_jc_jB_j(s)$. Au-dessus d'un zéro simple, la surface incidente

\[
\mathfrak Z=\{(c,s):F_c(s)=0\}
\]

possède une branche locale unique. Pour un chemin differentiable $c(\lambda)$ à travers ce point,

\[
\frac{ds}{d\lambda}=-\frac{\sum_j\dot c_j(\lambda)B_j(s)}{F_c'(s)}. \tag{6}
\]

Cette identité vient du théorème des fonctions implicites, puis de la dérivation de $F_{c(\lambda)}(s(\lambda))=0$. Sur une fibre à $A,r,i$ fixés, le numérateur devient l'évaluation d'un déplacement tangent $s_r\rho N\dot v$. Cela donne un opérateur linéaire local de $T_c\mathcal F_A$ vers $\mathbb C$.

Lorsque $F_c'(s)$ s'annule, la formule (6) cesse d'être définie. L'explosion du conditionnement est une information de protocole : elle requiert une section de jets ou un suivi de paire, et pas une extrapolation du quotient. L'existence d'une branche locale ne détermine ni le signe de sa vitesse imaginaire, ni une identité globale de branche après plusieurs collisions.

## 8. Deux zéros peuvent être suivis sans choisir leur étiquette

Supposons qu'un contour fermé contienne exactement deux zéros d'une fonction holomorphe $F$, comptés avec multiplicité, sans zéro sur le contour et sans pôle à l'intérieur. Par le théorème des résidus,

\[
m_k=\frac1{2\pi i}\oint s^k\frac{F'(s)}{F(s)}\,ds=\rho_1^k+\rho_2^k,
\qquad k=0,1,2.
\]

On a $m_0=2$ et les deux invariants

\[
a=m_1/2,\qquad\Delta=2m_2-m_1^2=(\rho_1-\rho_2)^2.
\]

La matrice compagnon

\[
H_{\rm paire}=\begin{pmatrix}a&1\\\Delta/4&a\end{pmatrix} \tag{7}
\]

possède exactement ces deux zéros comme valeurs propres, y compris au point double. Les labels individuels peuvent s'échanger tandis que $a$ et $\Delta$ restent bien définis. Le contour doit être maintenu isolant pendant le déplacement ; un zéro franchissant le contour invalide l'interprétation « même paire ».

Dans la variable complexe de hauteur $t$ d'une fonction $Z$ réelle analytique, un contour isolant une paire invariante par conjugaison donne $a$ et $\Delta$ réels. Avec $d=\Delta/4$,

\[
M=\begin{pmatrix}d&0\\0&1\end{pmatrix},\qquad H_{\rm paire}^TM=MH_{\rm paire}.
\]

Si $d>0$, les deux hauteurs sont réelles et cette métrique est positive. Si $d<0$, elle est indéfinie et les hauteurs forment une paire non réelle. Si $d=0$, cette métrique devient singulière et la matrice (7) est un bloc de Jordan. Cette construction montre un mécanisme local de perte de coercivité. Elle **n'impose pas** $d\ge0$ et n'est pas un opérateur de Hilbert–Pólya dérivé de l'arithmétique.

Une quadrature donnant $m_0\approx2$ et $\Delta\approx0$ ne constitue pas un certificat de contour ni un certificat de collision. La traduction opératoire indique ce qu'il faut contrôler, sans remplacer ce contrôle.

## 9. Les unités fictives accompagnent les opérations

Toutes les coordonnées précédentes sont normalisées, d'unité $1$. Pour écrire une convention d'unité $\mathsf C$, poser $c^{\mathsf C}=\mathsf Cc$, $A^{\mathsf C}=\mathsf CA$ et $F^{\mathsf C}=\mathsf CF$. Les contraintes complexes portent alors $\mathsf C$, leur normalisation par $\mathsf C\sin r$ donne le vecteur $b$ d'unité $1$. Les phases, $M_i$, les projecteurs et les formes de Gram normalisées gardent l'unité $1$.

Si la hauteur porte une unité conventionnelle $\mathsf T$, les jets d'ordre $k$ portent $\mathsf C\mathsf T^{-k}$. Empiler les lignes $\mathsf T^k Z^{(k)}$ donne des lignes de même unité. Leur rescaling par des constantes non nulles ne modifie ni le noyau ni la solution de norme minimale des contraintes exactes. Cette précaution évite de présenter une addition de jets de dimensions différentes comme un calcul homogène.

Le score $D$ reste sans dimension. On peut lui associer une unité fictive $\mathsf E$ par $\mathcal E=\mathsf E D$. Une dérivée par rapport à un temps conventionnel a alors l'unité $\mathsf E/\mathsf T$. Sa positivité ne découle pas de $D\ge0$ : un score positif peut augmenter ou diminuer. Une convention d'unité rend les calculs lisibles ; elle ne crée pas une loi énergétique ou une inégalité arithmétique.

## 10. La positivité qui manque demeure distincte

$G_i$ est positive parce qu'elle est $M_iM_i^T$. Le même constat vaut pour un Gram de jets de rang plein. Le défaut $D$ est le carré moyen normalisé d'un défaut de multiplicativité, donc sa positivité est également automatique. Ces positivités existent avant toute information sur la position des zéros.

Dans le critère de Weil, la positivité pertinente porte sur une fonctionnelle arithmétique évaluée sur toutes les autocorrélations admissibles. Elle contient un appariement entre valeurs spectrales reliées par $\rho\mapsto1-\overline\rho$ : sur la droite critique, il devient un carré ; hors de la droite, un bloc peut devenir indéfini. Le mémo historique `MEMO_P2_2_WEIL.md` demandait déjà une vérification primaire de la formulation exacte. La présente note ne transforme pas une analogie de Gram en démonstration de ce critère.

Pour franchir le verrou RH, il faut au minimum une forme construite depuis l'arithmétique, un espace admissible dense et un domaine explicite, une identité exacte reliant cette forme au spectre recherché, et des bornes uniformes lorsque la hauteur et la dimension augmentent. Une métrique construite après connaissance des racines est un diagnostic du signe, pas une cause qui l'imposerait. Le test Davenport–Heilbronn sert à empêcher qu'une identité générique soit prise pour une propriété spécifique du produit d'Euler.

## 11. Ce qui change effectivement le prochain protocole

1. Une cible complexe est désormais testable avant toute recherche de zéro. Archiver $A,r,i$, le critère $\eta$ et la marge $1-\eta$ ; conserver les fibres vides ou proches du bord.
2. La variation de $D$ est testable par les coefficients de (3). Conserver explicitement $A=0$ et le bord comme contreexemples ; ne pas chercher à les éliminer après lecture des résultats.
3. Un chemin peut être construit sur une même fibre en paramétrant $v\in S^2$. Le calcul de branches peut donc contrôler simultanément coefficient complexe, ancre et rayon.
4. À proximité d'un zéro multiple, empiler les jets pour tester la section (5). Archiver rang, compatibilité, norme minimale, résidus et conditions $Z''\ne0$ et transversalité lorsqu'elles sont certifiées.
5. Maintenir les paires de racines par un contour isolant et les invariants (7), en conservant toute perte d'isolation. Cette procédure vise les passages entre branches ; elle ne les réduit pas à une extension du plafond.

Le module `src/v641_fibres.py` construit ces opérateurs en flottant et fournit un certificat d'intervalles pour la géométrie finie. Les huit tests associés comprennent une preuve symbolique indépendante de la pseudo-inverse dans un modèle rationnel, un calcul du défaut par moyenne de groupe indépendante du polynôme, et les deux contreexemples. Le module ne compte aucun nouveau zéro.

## 12. Bilan logique

**Démontré :** faisabilité de toute cible prescrite par l'ellipse ; dimension exacte des fibres ; critère de constance du défaut ; variation générique intérieure ; contreexemple $A=0$ effectivement faisable ; contraction quantitative au bord ; section de jets de rang cinq, sous cette hypothèse.

**Conditionnel :** vitesse d'une branche simple ; interprétation d'un contour isolant deux zéros ; représentation compagnon et changement de signature de sa métrique ; multiplicité deux et pli uniquement après contrôle des hypothèses supplémentaires.

**Toujours ouvert :** existence et certification des collisions de la famille étudiée, passage global entre branches, couverture de toutes les fibres et de toutes les hauteurs, et positivité arithmétique uniforme conduisant à RH. La géométrie enlève une ambiguïté du problème ; elle ne supprime pas ces verrous analytiques.

## 13. Audit constructif après exécution — 12 octobre 2026

Cette section est ajoutée après verrouillage du protocole et production des données V6.41. Elle conserve les énoncés antérieurs et distingue leur preuve des nouvelles lectures numériques. Elle ne transforme pas une conjecture préenregistrée en théorème après observation.

**Géométrie.** Les 120 lignes de `data/v641_geometrie.json` ont été recomputées depuis les phases de Gauss : les valeurs de $\eta$, les statuts et les résidus du critère polynomial sont identiques à l'export archivé dans ce recoupement binary64. On compte 72 lignes intérieures, 24 lignes `boundary_tolerance` et 24 lignes extérieures. Les 24 lignes de centre $\eta=0$ représentent seulement 12 centres, chacun répété pour les deux axes de l'ellipse. Le nombre 120 décrit un inventaire de recettes ; il ne constitue ni 120 expériences indépendantes ni une couverture de toute l'ellipse. La preuve de faisabilité reste le théorème 1, et la faisabilité exacte de $A=0$ reste étayée par le certificat d'intervalles des six ancres.

**Jets.** Parmi 36 sections numériques à $r=\pi/6$, aux hauteurs $5,10,15,20$, pour les trois ancres représentatives et les trois cibles $\eta=0,1/4,1$, deux sections ont une norme minimale inférieure à un :

| Ancre | Hauteur prescrite | Cible | $\nu$ numérique | Nombre de candidats |
|---|---|---|---|---|
| $k=1$ | $5$ | $A=\cos(\pi/6)z_1$ | $0.8288412580171716$ | $2$ |
| $k=3$ | $15$ | $A=\cos(\pi/6)z_3$ | $0.9382168857291140$ | $2$ |

Les 34 autres sections sont vides dans le calcul déclaré ; les rangs sont numériques et les jets ne sont pas certifiés par intervalles. Les quatre vecteurs construits sont donc des candidats de multiplicité au moins deux dans la section, avec des dérivées secondes numériquement non nulles. Il n'est pas justifié de les appeler quatre collisions exactes certifiées. Toutes les sections actuellement faisables ont $\eta=0$ : la géométrie étend bien le domaine des cibles possibles, mais cette expérience n'a pas encore produit un exemple de collision vérifiée à cible complexe hors du centre.

**Plis.** Le fichier `data/v641_collisions.json` conserve 20 candidats, recoupés à 40 et 70 chiffres, et indique explicitement `interval_certification=false`. Les petits résidus et l'accord de précision renforcent leur plausibilité ; ils ne remplacent pas un théorème d'existence unique dans une boîte, ni une exclusion sur les bords. Le suivi de branches utilise des rayons variables et donc $A(r)=\cos(r)z_i$ variable. Il ne doit pas être décrit comme un suivi à $A$ constant. Les sections de jets et le suivi radial sont deux expériences complémentaires avec des contraintes différentes.

**Critique du graphe.** Une flèche utile nomme l'implication et ses hypothèses, plutôt que la seule proximité visuelle des deux objets :

| Passage | Statut et condition exacte | Ce que les calculs autorisent à dire |
|---|---|---|
| Idée de fibre → ellipse et opérateurs | démontré, rang deux des phases | tout $A$ prescrit a un test de compatibilité |
| Fibre faisable → section de jets | aucune implication générale ; ajouter compatibilité, rang et $\nu\le1$ | 2 sections sur 36 sont numériquement faisables |
| Jets nuls → zéro double exact | ajouter existence exacte et $Z''\ne0$ | quatre candidats à vérifier, pas quatre certificats |
| Zéro double → pli d'une paire | ajouter transversalité et isolement de la paire | 20 candidats de pli recoupés, globalement non exhaustifs |
| Paire isolée → compagnon | démontré sous hypothèses du contour | les moments décrivent une paire sans labels individuels |
| Compagnon local de V13 → forme globale de Weil pour $\zeta$ | aucun pont démontré | un laboratoire local et des contre-épreuves |
| Hiérarchie dense de Weil → positivité globale → RH | conditionnel à tous les niveaux, continuité et contrôle d'erreur ; critère global vérifié dans sa convention | aucun préfixe fini ne remplit seul les quantificateurs globaux |

Pour la ligne du compagnon, le discriminant doit être nommé avec sa variable : $w=-i(s-1/2)$ donne $\Delta_w=-\Delta_s$. La métrique réelle positive lorsque les deux hauteurs critiques sont réelles porte sur le compagnon en variable $w$. Son signe ne doit pas être reporté inchangé sur le discriminant en variable $s$.

**Passage au global.** Les lemmes G1–G4 de `V641_PASSAGE_AU_GLOBAL.md` ont été relus. L'image exacte de $P=\partial_x^2-1/4$ est bien l'espace des tests avec les deux moments polaires nuls. La construction de Fourier avec coupure donne une approximation dans la topologie des tests : support compact commun et convergence de toutes les dérivées. Le passage à la limite pour une forme continue est valide si les positivités portent sur tous les espaces finis de cette hiérarchie, ou si un budget d'erreur adéquat est démontré le long des approximations. Le contreexemple de préfixe positif et le complément de Schur sont également corrects avec leurs hypothèses de domaine et de bornitude explicites. Aucun de ces lemmes ne prouve encore la positivité des compressions arithmétiques requises.

La formulation primaire du critère de Weil et son signe sont désormais consignés dans cette note globale, à partir de Connes–Consani, *Weil positivity and Trace formula, the archimedean place*, introduction (4) et proposition C.1 : https://alainconnes.org/wp-content/uploads/Selecta.pdf. Cette vérification remplace, pour la formulation citée, la réserve bibliographique du mémo historique. Elle n'étend pas le théorème archimédien particulier de cette source à toute la somme arithmétique ni à tous les supports sans hypothèses supplémentaires.

Prendre de la hauteur dans le labyrinthe fournit donc deux bénéfices précis : certains couloirs locaux ont maintenant une carte exacte, et la porte globale porte un contrat de passage formulé avec ses quantificateurs. La carte ne démontre pas que les couloirs locaux rejoignent cette porte. Le prochain progrès pertinent serait soit un certificat de paire/collision à cible complexe non centrale, soit une estimation arithmétique uniforme sur la hiérarchie admissible, avec le couplage et la queue contrôlés.

**Relecture finale du code de blocs, même date.** `src/v641_blocs.py` emploie bien la pseudo-inverse SVD pour la solution minimale, puis le vecteur du noyau pour les deux candidats. Il conserve séparément incompatibilité, rang inférieur à cinq, section vide et frontière à tolérance. Les 36 matrices archivées sont classées de rang cinq avec un seuil relatif $10^{-10}$ ; leur plus petit rapport de valeurs singulières est environ $0.00769388$, donc la décision n'est pas proche de ce seuil dans les matrices calculées. Cela ne certifie pas le rang des matrices exactes : le jet d'ordre un est construit ici par différence centrée de pas $10^{-4}$ et l'erreur de troncature n'est pas bornée. Le maximum des résidus de compatibilité est $8.18\cdot10^{-15}$ et celui des quatre candidats $1.57\cdot10^{-15}$ dans ces matrices approchées.

`pair_from_moments` utilise les identités de Newton correctes et demande un compte numérique proche de deux. Ce contrôle reste distinct du compte exact du principe de l'argument. La réalité de la moyenne et du discriminant est contrôlée dans le runner avant l'acceptation d'un bloc réel. L'identité de métrique dans la note s'applique à ce bloc en variable de hauteur ; elle ne garantit aucune métrique coercive uniforme lorsque le discriminant tend vers zéro. Les deux destinations globales doivent donc demeurer séparées sur le graphe : $Q_W(f)\ge0$ pour **tout** test admissible, ou $Q(X)=X^{o(1)}$ obtenu indépendamment de RH par le théorème A. Le théorème B, conditionnel à RH, ne ferme aucune de ces portes sans levée préalable de son hypothèse.
