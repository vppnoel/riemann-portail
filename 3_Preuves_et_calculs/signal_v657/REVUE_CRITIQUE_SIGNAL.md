# Revue critique du canal de calcul — 16 octobre 2026

Documents effectivement relus : 70 (dette et contrats de queue), 73 (certificat opérateur commun), 76 (complément audité), 79 (profils de compensation et obstructions).

## 1. Correction de diagnostic

Le document 73 certifie déjà un espace de fonctions infini entier : tous les tests admissibles de X_S pour 0<S≤1/2. L'erreur en norme opérateur ferme réellement les directions qui ne sont pas dans la matrice. Décrire tout le corpus comme une simple accumulation d'échantillons serait donc faux. La limite globale porte sur les supports non bornés et sur une loi arithmétique couvrante, non sur une impossibilité générale de porter une conclusion infinie par un certificat fini.

## 2. Information minimale à conserver

Proposition algébrique. Soit L une application linéaire de l'espace réel des matrices hermitiennes n×n vers un espace de statistiques. Si L permet de décider pour toute matrice G si G est positive ou nulle, alors L est injective.

Preuve. Si D≠0 est hermitienne dans ker L, G0=cI est strictement positive et L(G0+tD)=L(G0) pour tout réel t. Une valeur propre non nulle de D permet de choisir t tel que G0+tD ait une valeur propre négative. Les mêmes données ne peuvent alors décider les deux signes. Pour des matrices réelles symétriques, la même preuve vaut dans cet espace plus petit. □

Portée : cela n'impose pas de conserver n² nombres pour Weil si une identité arithmétique ou une symétrie réduit la classe admissible. Cela interdit seulement d'attendre d'une compression linéaire générique, avec des directions matricielles libres perdues, une décision universelle sans garde. Un scalaire non linéaire comme la plus petite valeur propre décide bien le signe une fois calculé : le théorème ne l'interdit pas.

Pour une base réelle et une forme de Weil réelle symétrique, les couplages imaginaires sont nuls par structure. Le contre-modèle hermitien complexe générique du document 76 ne doit pas être attribué à une telle matrice de Weil.

## 3. Diagnostic relatif de Schur

Sous les contrats du document 70, écrire H pour la tête et kC=(β/μ)C pour le majorant positif de la dette. Si H≻0, poser

r = λmax(H^(-1/2) kC H^(-1/2)).

Alors H−kC⪰0 si et seulement si r≤1. Ce r est sans dimension et invariant par changement de coordonnées inversible du complément : il mesure la part de tête consommée par la dette. Ce n'est ni une probabilité de RH ni un nouvel indicateur de progression globale. Pour H singulière, il faut en plus que la dette annihile ker H ; la pseudo-inverse n'autorise pas à oublier cette garde.

Dans le document 73, les bornes déjà certifiées donnent pour le bloc pair une marge de tête ≥0,004745324 et une dette ≤0,000008443, soit r≤0,001780 par un majorant scalaire. Moins de 0,18 % de cette marge est consommé par la dette. Ce chiffre ne s'extrapole pas aux supports suivants. Il montre que, dans ce certificat précis, la tête et la couverture globale sont des obstacles distincts d'un manque de contrôle des couplages.

Une queue contenue dans une matrice mère finie fournit uniquement un diagnostic de Schur fini. Elle ne représente pas toutes les directions fonctionnelles omises sans contrat opérateur externe.

## 4. Garde de courbure pour le signal exact

Sur [a,b]⊂[log 2,∞), le signal Suzuki du document 79 vérifie dans les distributions

S'' = β(t)dt − Σ c_q δ_(log q) ≤ B dt,

si B≥sup_[a,b] β. Poser L_S pour la corde joignant les deux valeurs S(a),S(b). La fonction

S(t)−L_S(t)+(B/2)(t−a)(b−t)

est concave, et vaut zéro aux deux bords. Elle est donc positive ou nulle. Ainsi

S(t) ≥ L_S(t)−(B/2)(t−a)(b−t)
     ≥ min(S(a),S(b))−B(b−a)²/8.

La preuve vaut même lorsque plusieurs atomes premiers se trouvent dans la cellule : leurs sauts de pente sont négatifs et renforcent la concavité auxiliaire.

Version plus exacte. Le potentiel premier F=A−S est une somme de charnières positives, donc il est convexe. Par F(t)≤L_F(t),

S(t) ≥ L_S(t)−[L_A(t)−A(t)].

Cette garde conserve la courbure archimédienne exacte et peut éviter le coût d'une borne B uniforme.

Avec une marge de bord certifiée m>0, la condition Δ≤sqrt(8m/B) est suffisante pour certifier toute la cellule. Elle n'est pas nécessaire pour le signe du vrai signal, ni pour toute autre méthode de preuve. Si l'on suppose des marges bornées et β(t)≈exp(t/2), cette garde demande une résolution d'ordre exp(−t/4) ; ce constat porte sur la garde, pas sur une nécessité universelle de la recherche.

Un algorithme de subdivision termine sur un compact où min S>0, si les erreurs des évaluations sont elles-mêmes raffinables. Il découvre éventuellement une négativité stricte si elle existe. Un contact nul peut empêcher sa terminaison. Aucun nombre fini de cellules ne couvre automatiquement l'axe non borné.

Cette garde est apparentée à la convexité et aux profils intérieurs du document 79. Son exécution apporte une représentation et un contrôle de pertes, pas une nouvelle preuve de RH. Le document 79 certifie déjà le signal sur [log2,log1000] : reprendre cette fenêtre ne doit pas être compté comme une extension de la portée.

## 5. Deux confusions à exclure

La positivité du signal scalaire sur une fenêtre ne certifie pas la forme de Weil pour tous les tests de support comparable. Le critère global publié concerne le signal arithmétique précis sur tout l'axe. Pour un signal générique, même S(t)≥0 partout n'implique pas la positivité du noyau S(t)+S(u)−S(t−u) : S(t)=t⁴ donne, pour t=±1, la matrice [[2,−14],[−14,2]], de valeur propre −12.

Une normalisation par R ou un changement de métrique préserve l'inertie de la forme par congruence ; il ne crée pas le signe. Si les normes changent avec le rang, ε_n→0 ne suffit pas : le produit ε_n R_n(f) doit tendre vers zéro pour chaque test fixé. Cette garde était déjà démontrée au document 76 et doit rester active.

## 6. Littérature contrôlée

M. Suzuki, Weil's quadratic form via the screw function, arXiv:2606.09096v3, 23 septembre 2026, https://arxiv.org/html/2606.09096v3. Consulté dans cette passe : cadre local fermé, minimum spectral et petits supports. Les constructions opératorielles sont inconditionnelles ; le prolongement spectral limite reste conjectural. Ce résultat est déjà référencé dans le document 79 ; il n'est pas une découverte de cette passe.

## Décision proposée

Conserver les matrices complètes et les certificats opérateurs ; ajouter un diagnostic de perte par comparaison diagonal/complet et par dette relative ; employer la grille adaptative comme certificat de cellules et outil de localisation. Ne pas promouvoir l'augmentation du nombre de cellules, la reconstruction d'un outil existant ou un Schur de matrice finie en progrès sur la loi de signe universelle. Le verrou est l'estimation arithmétique structurée qui continue de fonctionner à toutes les échelles.
