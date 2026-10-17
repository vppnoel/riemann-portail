# V6.38 - Deux récursions de Bellman, deux portées

Vincent P. P. NOËL. 12 octobre 2026. Reconstruction de résultats classiques ; aucune nouveauté historique revendiquée.

## Lemme 1 - Planification finie des livrables

Soit A un ensemble fini d'actions, chacune de coût entier c(a) strictement positif. Les prérequis forment un graphe sans cycle. Une action ne peut être réalisée qu'une fois. L'état est (D,b), où D est un ensemble d'actions achevées fermé par prérequis et b un budget entier non négatif. Pour chaque a, K(a) est un ensemble de tokens documentaires proposés ; K(D) est leur union. Chaque token appartient à un critère j et les poids w_j sont non négatifs. Posons

\[
U(D)=\sum_{k\in K(D)}w_{j(k)},\qquad
[U]=\mathsf U,\quad[c]=[b]=\mathsf H.
\]

Les poids ont l'unité conventionnelle U par token, et H est une unité conventionnelle de travail, sans conversion en heure. Un token décrit un livrable contrôlable, et non un succès de recherche promis. Les coûts et l'utilité sont des conventions de scénario.

Alors la meilleure utilité terminale réalisable dans ce modèle est donnée par

\[
V(D,b)=\max\left\{U(D),\;
\max_{\substack{a\notin D,\ P(a)\subseteq D\\c(a)\leq b}}
V(D\cup\{a\},b-c(a))\right\}.
\]

Le maximum extérieur inclut STOP ; si aucune action n'est admissible, V(D,b)=U(D). En particulier V(D,0)=U(D). La récursion définit une valeur unique et termine.

**Preuve.** Toute suite admissible s'arrête immédiatement ou commence par une action admissible a. Après cette action, les suites restantes sont exactement les suites admissibles depuis (D union {a},b-c(a)), parce que coûts, prérequis et utilité ne dépendent que de cet état dans le modèle. Chaque transition diminue strictement le budget et augmente le nombre d'actions achevées. L'induction sur b, avec cas terminal STOP, prouve la formule, sa terminaison et l'optimalité. Le maximum existe car il n'y a qu'un nombre fini de suites. Fin de preuve.

La valeur des gains nouveaux W(D,b)=V(D,b)-U(D) satisfait W(D,0)=0 et la forme en récompenses marginales

\[
W(D,b)=\max\{0,\max_a[U(D\cup\{a\})-U(D)+W(D\cup\{a\},b-c(a))]\}.
\]

La différence évite de recompter les acquis. Aucun facteur gamma inférieur à un n'est nécessaire : l'horizon est fini. Aucune loi de transition empirique n'a été estimée. La propriété d'état suffisant vaut par construction dans le modèle, sans prouver que le processus réel de recherche est markovien. L'incertitude scientifique réelle exigerait un état enrichi, une loi justifiée ou une analyse de scénarios supplémentaires.

## Lemme 2 - Bellman variationnel sur une compression hermitienne

Soit G un opérateur hermitien sur un espace vectoriel complexe de dimension finie muni d'un produit scalaire positif fixé. Pour un sous-espace W et 0 <= k <= dim W, définissons

\[
B_k(W)=\min_{\substack{v_1,\ldots,v_k\in W\\\langle v_i,v_j\rangle=\delta_{ij}}}
\sum_{i=1}^{k}\langle v_i,Gv_i\rangle,\qquad B_0(W)=0.
\]

Alors

\[
B_k(W)=\min_{\substack{v\in W\\\|v\|=1}}
\left[\langle v,Gv\rangle+B_{k-1}(W\cap v^\perp)\right].
\]

Si lambda_1 <= ... <= lambda_m sont les valeurs propres de la compression P_W G|_W, alors B_k(W)=lambda_1+...+lambda_k.

**Preuve de la récursion.** L'ensemble des repères orthonormés est compact et l'objectif est continu : un minimum existe. Fixer le premier vecteur v laisse exactement un repère orthonormé de k-1 vecteurs dans W intersect v-perp ; prendre les deux minima donne la formule.

**Preuve de la valeur spectrale.** Dans une base propre orthonormée e_j du comprimé, posons p_j=sum_i |<e_j,v_i>|². Alors 0 <= p_j <= 1, sum_j p_j=k et l'objectif vaut sum_j lambda_j p_j. Réallouer une masse depuis un indice plus grand vers un indice plus petit ne l'augmente pas. Le minimum est donc au moins la somme des k plus petites valeurs propres, et il est atteint en choisissant v_i=e_i. Fin de preuve.

Cette récursion continue optimise une trace. Elle est distincte du modèle documentaire fini du lemme1. Elle ne donne aucune nouvelle borne spectrale sans information supplémentaire sur G. Dans notre contexte G peut être une matrice de forme hermitienne finie exprimée dans une base munie de la métrique euclidienne ; il ne faut pas supposer positive la forme G elle-même.

## Obstacle - Une trace négative ne certifie pas k directions négatives

Une somme négative de k valeurs propres est compatible avec une seule valeur propre très négative et k-1 valeurs propres positives. Exemple : diag(-100,1) a B_2=-99, mais seulement une direction négative.

Pour obtenir au moins k directions négatives, il faut contrôler la k-ième valeur propre, par exemple par la caractérisation variationnelle classique

\[
\lambda_k(G)=\min_{\dim S=k}\max_{\substack{v\in S\\\|v\|=1}}\langle v,Gv\rangle<0,
\]

ou exhiber une compression de dimension k strictement négative avec son budget d'erreur. Le témoin V6.36 relève de cette seconde méthode (Gershgorin, intervalles et erreurs binaires) ; il ne découle pas du signe de B_k. Choisir des vecteurs individuellement négatifs ne suffit pas non plus, à cause des termes croisés.

## Ouvert

Pour les entiers, il faudrait définir un état arithmétique, ses transitions et une valeur dont le contrôle impose la positivité pertinente pour zêta sur toute la classe requise de fonctions tests. Ni la planification documentaire ni la compression finie ne fournissent cette construction. Une contraction ajoutée artificiellement à un opérateur ne prouve pas ce lien.

## Source historique et audit

R. Bellman, *Some Functional Equations in the Theory of Dynamic Programming*, PNAS39 (1953), 1077-1082, DOI10.1073/pnas.39.10.1077. Notice primaire : https://pubmed.ncbi.nlm.nih.gov/16589377/. Notice bibliographique consultée ; texte intégral non audité dans cette reprise. Les preuves ci-dessus sont données intégralement et ne dépendent pas d'une citation non lue.
