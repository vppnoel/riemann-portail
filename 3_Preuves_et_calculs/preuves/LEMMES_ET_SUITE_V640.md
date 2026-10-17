# V6.40 — Deux lemmes et la question laissée ouverte

Les objets exacts sont les recettes V6.39, pas leurs coordonnées décimales.
On travaille dans l'espace impair modulo 13 avec les six caractères $k=1,3,5,7,9,11$.
Écrire $B_j(s)=z_jL(s,\chi_j)$, $|z_j|=1$ et $F_c=\sum_j c_jB_j$, avec $c$ réel de norme $1$.

## Lemme 1 — Un bord droit uniforme sans zéro

Pour chacun des 24 membres exacts du plan V6.39, F_c(s) est non nul pour
$\operatorname{Re}(s)\geq3$. Plus généralement, cela vaut pour tout vecteur de norme $1$ dont
$|a(1)|>\sqrt6(\zeta(3)-1)$.

**Démonstration.** Dans $\operatorname{Re}(s)>1$, la série de Dirichlet converge absolument.
Ses coefficients sont $a(n)=\sum_j c_jz_j\chi_j(n)$. Comme $|\chi_j(n)|\leq1$,
Cauchy–Schwarz donne $|a(n)|\leq\sum_j|c_j|\leq\sqrt6$. Donc, pour $\sigma\geq3$,

\[
 |F_c(s)-a(1)|\leq\sqrt6\sum_{n=2}^{\infty}n^{-\sigma}
 \leq\sqrt6(\zeta(3)-1).
\]

Or les recettes exactes ont $a(1)=\cos(r)z_i$ et tous les rayons sont $\leq3/4$.
Ainsi $|a(1)|\geq\cos(3/4)$. Une inégalité rationnelle élémentaire suffit :
$\cos(3/4)\geq1-(3/4)^2/2=23/32$, $\sqrt6<5/2$, et

\[
\zeta(3)-1=\frac18+\sum_{n=3}^{\infty}\frac1{n^3}
<\frac18+\int_2^{\infty}\frac{dx}{x^3}=\frac14.
\]

D'où $\sqrt6(\zeta(3)-1)<5/8<23/32\leq\cos(3/4)$.
L'inégalité triangulaire inverse donne $|F_c(s)|>0$. La marge fine
$\cos(3/4)-\sqrt6(\zeta(3)-1)\approx0{,}236753$ est une lecture numérique ; elle
n'est pas nécessaire à la démonstration. La preuve concerne les objets exacts.
Le code vérifie séparément la domination pour les coordonnées arrondies.

Le facteur de complétion commun est non nul et holomorphe dans $\operatorname{Re}(s)\geq3$ :
la même conclusion vaut pour la fonction complétée sur ce demi-plan. Cela ne
démontre pas qu'un contour intérieur soit sans zéro sur chacun de ses segments.

## Lemme 2 — Vitesse locale d'une racine simple

Fixons une ancre $i$ et une direction $u$ de la recette exacte, indépendante de $r$,
et posons $G(s)=\sum_j u_jB_j(s)$. Pour un signe $\eta\in\{+1,-1\}$, définissons

\[
 F_\eta(r,s)=\cos(r)B_i(s)+\eta\sin(r)G(s).
\]

Si $F_\eta(r_0,s_0)=0$ et $\partial_sF_\eta(r_0,s_0)\neq0$, il existe un voisinage de $r_0$
et une unique branche holomorphe $s(r)$, avec $s(r_0)=s_0$, satisfaisant $F_\eta(r,s(r))=0$.
Sa dérivée est

\[
 s'(r)=-\frac{-\sin(r)B_i(s(r))+\eta\cos(r)G(s(r))}
 {\cos(r)B_i'(s(r))+\eta\sin(r)G'(s(r))}.
\]

**Démonstration.** Les $L(s,\chi_j)$ non principaux sont holomorphes, et $\sin/\cos$
sont entières. Le théorème des fonctions implicites holomorphes s'applique
par l'hypothèse $\partial_sF\neq0$. Dériver l'identité $F(r,s(r))=0$ donne
$\partial_rF+\partial_sF\cdot s'=0$ ; la formule annoncée suit par division.

Au voisinage de la branche, $\sin(r)\neq0$ pour les rayons considérés. L'identité
$F_\eta=0$ donne $\eta G(s)=-\cot(r)B_i(s)$, d'où la forme équivalente

\[
s'(r)=\frac{B_i(s(r))}{\sin(r)\,\partial_s F_\eta(r,s(r))}.
\]

Cette dernière formule ne fixe aucun signe pour la partie imaginaire de $s'$.
La variation de l'ordonnée est $\operatorname{Im}(s')$, et celle de $|\operatorname{Im}(s)|$, si $\operatorname{Im}(s)\neq0$, est
$\operatorname{sign}(\operatorname{Im}(s))\operatorname{Im}(s')$. Si le dénominateur s'annule, l'hypothèse de racine simple
cesse : c'est un événement à examiner séparément, pas une raison pour continuer
à employer la formule par division.

Ce lemme est conditionnel. Un petit résidu calculé n'est pas une preuve que
la racine soit simple ; les racines numériques de V6.40 ne fournissent pas ici
un certificat pour ses hypothèses.

## Unités conventionnelles et portée

Les formules précédentes emploient des coordonnées normalisées, d'unité $1$.
Pour leur associer une unité fictive $\mathsf C$, poser $c_j^{\rm phys}=\mathsf Cc_j$ et $F^{\rm phys}=\mathsf CF$.
Les $L$ et les $B_j$ gardent l'unité $1$ ; $F^{\rm phys}$ et $a^{\rm phys}(n)$ portent $\mathsf C$, avec
$\|c^{\rm phys}\|/\mathsf C=1$. Le score $D$ est le quotient d'un carré de défaut de multiplicativité
(unité $\mathsf C^4$) par $\|c^{\rm phys}\|^4$ (unité $\mathsf C^4$) : son unité est $1$. Les coordonnées $s$ et les
angles en radians sont sans dimension. Dans la formule de vitesse, numérateur
et dénominateur, écrits pour $F^{\rm phys}$, ont la même unité $\mathsf C$ : $s'(r)$ a l'unité $1$ par radian conventionnel.
Le paramètre $r$ mesure une variation d'angle. Une dérivée par rapport au temps aurait une unité différente.

Dans la formule simplifiée, le numérateur pour $F^{\rm phys}$ est $\mathsf CB_i$, et le
dénominateur $\mathsf C\partial_sF$ : $\mathsf C$ s'annule. Un changement commun d'échelle ne
modifie ni les racines ni $D$.

## Ce qui reste ouvert et prochaine expérience

Le résultat fini V6.40 teste un ordre de détection dans les 12 strates choisies.
Il ne prouve ni un ordre uniforme selon D, ni causalité, ni absence de racine
avant la tranche, ni GRH aux points d'Euler.

La suite prioritaire est de suivre des branches de racines simples dans les
familles exactes $c_\eta(r)$, puis de comparer leurs déplacements au lemme 2.
Choisir une ancre donnant le signe contraire et une ancre favorable permet de
tester une explication. Le protocole doit être fixé avant cette nouvelle suite :
grille en $r$, identités de branches, conditions d'arrêt quand $\partial_sF$ est
petit, traitement des collisions et conservation de toutes les branches perdues.

Les passages entre branches, les collisions de zéros critiques doubles, un
coefficient complexe A arbitraire, et la positivité globale liée à RH restent
ouverts. L'extension du plafond seule ne tranche aucune de ces questions.
