# V6.41 — Prendre de la hauteur : destination, densité et contrôle uniforme

## 1. La destination logique est connue ; le mécanisme est à construire

La destination RH est un énoncé précis : tout zéro non trivial de ζ a partie
réelle 1/2. Le chemin de preuve demeure inconnu. Un autre objet de recherche
peut servir de destination intermédiaire : une forme arithmétique positive
sur tous les tests admissibles, ou une borne de croissance construite depuis
les nombres premiers. Cela doit être formulé comme une implication vérifiable,
et non comme une promesse qu'un objet « plus grand » apparaîtra.

Le graphe distingue donc la destination logique RH, les critères équivalents,
les résultats auxiliaires locaux et les hypothèses manquantes. Écarter une
voie sous des hypothèses précises retire une ambiguïté ; cela ne démontre pas
l'inexistence de tout chemin de preuve.

## 2. Fixer le critère global sans ambiguïté de signe

Référence primaire : A. Connes et C. Consani, *Weil positivity and Trace formula,
the archimedean place*, 2021, introduction (4) et appendice C, proposition C.1.
PDF auteur : https://alainconnes.org/wp-content/uploads/Selecta.pdf ;
prépublication : https://arxiv.org/abs/2006.13771.

La référence écrit une négativité de la somme des distributions locales.
Nous choisissons son opposée, notée $Q_W$, pour parler de positivité. Dans
les coordonnées additives $x=\log u$, soit

\[
 E=\left\{f\in C_c^\infty(\mathbb R):
 \int f(x)e^{x/2}\,dx=\int f(x)e^{-x/2}\,dx=0\right\}.
\]

Ces deux conditions sont les annulations aux points polaires, après le
changement de convention unitaire de Mellin vers Fourier. L'involution
additive est $f^*(x)=\overline{f(-x)}$. Le critère publié, dans cette
convention, est $Q_W(f)\ge0$ pour tout $f\in E$ si et seulement si RH.
Les évaluations de la distribution sont celles de la formule explicite ;
leur signe ne peut pas être remplacé par celui d'un Gram construit de façon
automatique à partir de vecteurs.

Pour fixer complètement cette notation, employer les distributions $W_v$
dans la convention Fourier de l'introduction de la référence, poser
$g(u)=f(\log u)$ et

\[
Q_W(f)=-\sum_v W_v(g*g^*),\qquad
B_W(f,h)=-\sum_v W_v(g_f*g_h^*).
\]

La convolution et l'involution sont multiplicatives en $u$ ; elles deviennent
la convolution et l'involution additives après $x=\log u$. La convention
Mellin de l'appendice C nécessite le changement de normalisation indiqué
dans l'article : ses distributions ne sont pas à substituer terme à terme
dans cette formule sans ce changement.

La vérification primaire porte ici sur la formulation du critère et ses
conditions, non sur une nouvelle démonstration de l'ensemble de l'article.
Les arguments de densité ci-dessous sont démontrés séparément.

## 3. Lemme G1 — Un opérateur construit exactement les tests admissibles

Posons $P=\partial_x^2-1/4$. Alors

\[
\boxed{E=P\,C_c^\infty(\mathbb R).}
\]

**Démonstration.** Si $f=P\psi$ avec $\psi$ lisse à support compact, deux
intégrations par parties donnent

\[
\int e^{\pm x/2}P\psi(x)\,dx
=\int P(e^{\pm x/2})\psi(x)\,dx=0.
\]

Réciproquement, pour $f\in E$, définir

\[
\psi(x)=\int_{-\infty}^x2\sinh((x-y)/2)f(y)\,dy.
\]

La différentiation donne $P\psi=f$. À gauche du support de $f$, $\psi=0$.
À droite, elle vaut

\[
e^{x/2}\int e^{-y/2}f(y)\,dy
-e^{-x/2}\int e^{y/2}f(y)\,dy=0.
\]

L'équation différentielle et la régularité de $f$ donnent la régularité
$C^\infty$ de $\psi$, qui est donc à support compact. Le noyau de $P$ sur
$C_c^\infty$ est nul, puisque les seules solutions globales de $P\psi=0$
sont des combinaisons de $e^{x/2}$ et $e^{-x/2}$. □

L'opérateur $P$ élimine les deux contraintes d'admissibilité de façon exacte.
Sa construction n'impose aucun signe à $Q_W(P\psi)$.

## 4. Lemme G2 — Une hiérarchie dense, avec un vrai contrat de limite

Pour chaque entier $L\ge1$, choisir $\chi_L\in C_c^\infty((-L-1,L+1))$
égale à 1 sur $[-L,L]$. Considérer les espaces finis

\[
 E_{L,N}=\operatorname{span}\left\{
 P\left(\chi_L(x)e^{in\pi x/(L+1)}\right): |n|\le N\right\}.
\]

Ils sont inclus dans $E$ et sont emboîtés en $N$ pour $L$ fixé. Leur réunion
est dense dans $E$ pour la topologie des tests : les approximations ont un
support compact commun et toutes leurs dérivées convergent uniformément.

**Démonstration.** Écrire $f=P\psi$ grâce à G1, avec support de $\psi$
contenu dans $(-L,L)$. Prolonger $\psi$ périodiquement sur une période
$2(L+1)$. Elle est lisse, nulle au voisinage des extrémités ; ses sommes
partielles de Fourier convergent avec toutes les dérivées. Multiplier ces
sommes par $\chi_L$ puis appliquer $P$ donne des éléments de $E_{L,N}$
convergeant vers $f$. □

Soit $B$ une forme hermitienne continue sur $E$ et $Q(f)=B(f,f)$. Si
$Q\ge0$ sur **tous** les $E_{L,N}$, alors $Q\ge0$ sur $E$. En effet,
pour chaque $f$, la suite précédente donne $Q(f)=\lim Q(f_N)\ge0$.
Une seule taille, ou une liste finie de tailles, ne remplit pas l'hypothèse.

Avec des compressions approchées $\widetilde Q_{L,N}$, il faut au moins une
borne qui assure, pour chaque approximation admissible,

\[
|Q(f_N)-\widetilde Q_{L,N}(f_N)|\le\varepsilon_{L,N}\|f_N\|_*^2,
\qquad \varepsilon_{L,N}\|f_N\|_*^2\longrightarrow0,
\]

ainsi qu'une minoration compatible tendant vers zéro. La norme $\|\cdot\|_*$
et le contrôle de l'erreur doivent être justifiés dans le domaine de la
forme ; le seul nombre de coefficients ne suffit pas. Ces hypothèses ne
sont pas établies pour les calculs ζ du corpus par cette note.

Cela donne un but intermédiaire précis : prouver la positivité de la
hiérarchie arithmétique complète, ou une estimation uniforme qui l'implique.
C'est une reformulation opératoire de l'obstacle, non sa résolution.

## 5. Théorème G3 — Toute liste finie de préfixes positifs peut être trompeuse

Pour tout entier $M$, dans $\ell^2(\mathbb N)$, poser

\[
 K_M=I-2|e_{M+1}\rangle\langle e_{M+1}|.
\]

Les compressions sur les $n$ premières coordonnées, pour $n\le M$, sont
exactement $I_n$, donc positives. Pourtant
$\langle e_{M+1},K_Me_{M+1}\rangle=-1$. L'opérateur est borné,
autoadjoint, de norme 1. Ses compressions sont parfaitement compatibles.

**Démonstration.** Le rang un soustrait est orthogonal aux $M$ premières
coordonnées ; sa valeur sur $e_{M+1}$ est 1. Toutes les affirmations suivent. □

Ainsi, sur la classe des opérateurs bornés autoadjoints arbitraires, aucun
procédé utilisant uniquement un nombre fini de ces préfixes ne peut
distinguer $I$ de $K_M$ et conclure leur positivité globale. Cela ferme la
voie « beaucoup de matrices positives suffisent à elles seules ». Cela
ne ferme pas une voie utilisant une identité arithmétique ou une borne
uniforme supplémentaire. Ce théorème n'est pas une impossibilité de prouver RH.

## 6. Lemme G4 — Une clef possible doit contrôler aussi le couplage

Dans une décomposition $\mathcal H=\mathcal H_0\oplus\mathcal H_1$, soit
un opérateur borné autoadjoint

\[
K=\begin{pmatrix}A&B\\B^*&C\end{pmatrix},\qquad A\ge aI,
\quad a>0.
\]

Alors $K\ge0$ si et seulement si $C-B^*A^{-1}B\ge0$. En particulier,
si $C\ge cI$, $c\ge0$ et $\|B\|^2\le ac$, alors $K\ge0$.

**Démonstration.** Compléter le carré :

\[
\langle(x,y),K(x,y)\rangle
=\|A^{1/2}(x+A^{-1}By)\|^2
+\langle y,(C-B^*A^{-1}B)y\rangle.
\]

Choisir $x=-A^{-1}By$ démontre la nécessité ; la même identité démontre
la suffisance. Enfin $A^{-1}\le a^{-1}I$ donne
$B^*A^{-1}B\le\|B\|^2a^{-1}I\le cI$. □

Ce lemme suggère un budget : marge du bloc étudié, minoration de la queue,
norme du couplage. Les trois doivent être démontrées, dans un domaine
approprié. Une marge $a$ tendant vers zéro peut rendre ce critère insuffisant ;
il ne faut pas supposer une coercivité uniforme parce qu'un petit bloc est
positif. Pour une forme non bornée, domaines et fermeture sont des hypothèses
supplémentaires : le lemme ci-dessus ne s'y applique pas sans travail.

## 7. Où le graphe rejoint les théorèmes du corpus

Le théorème A du corpus relie l'exposant de croissance de $Q(X)$ à
$2(\Theta-1/2)$. Il fournit une autre destination intermédiaire : obtenir
une borne supérieure de croissance suffisante directement depuis les
nombres premiers. La positivité automatique $Q(X)\ge0$ ne fournit pas
cette borne supérieure. Le théorème B suppose déjà RH : l'utiliser pour
prouver RH sans lever cette hypothèse serait circulaire.

La voie Weil est différente : son signe est arithmétique et doit être contrôlé
sur tous les tests. Les fibres V13, jets, plis et compagnons aident à définir
des contre-épreuves et des instruments. Ils ne produisent pas encore la
borne des premiers ni l'estimation uniforme de la forme de Weil.

La clef cherchée est donc identifiable sans prétendre l'avoir : une identité
ou une inégalité arithmétique indépendante des zéros qui impose le signe ou
la croissance requis, avec ses quantificateurs globaux. Le graphe devra
montrer ces deux portes ouvertes et les résultats qui en sont encore séparés.
