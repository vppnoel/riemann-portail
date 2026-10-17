# Simulation de referee A — Théorème A

## Énoncé audité

\[
\frac12\limsup_{X\to\infty}\frac{\log Q(X)}{\log X}=\Theta-\frac12,
\qquad
Q(X)=\int_1^X\frac{|C(x)|^2}{x^2}\,dx.
\]

## Verdict provisoire

**Plausible et probablement correct ; révision majeure de présentation avant diffusion.** Aucun contre-exemple interne n'a été identifié. Le résultat reste une reformulation exacte de la position horizontale du zéro le plus à droite ; il ne constitue pas en soi une avancée vers RH.

## A1. Sens énergie -> région sans zéro

Le passage par Cauchy–Schwarz sur blocs dyadiques est convaincant : si `Q(X) << X^{2a}`, alors

\[
\int_1^\infty |C(x)|x^{-\sigma-1}dx<\infty
\]

pour `sigma>1/2+a`. L'intégrale définit donc une fonction holomorphe dans ce demi-plan et coïncide avec `G(s)/s` sur `Re s>1`.

### Point à rendre explicite

Si l'on suppose l'existence d'un zéro `rho` dans le demi-plan, `G(s)/s` est méromorphe et possède un double pôle en `rho`. Il faut écrire proprement l'argument de prolongement : l'égalité sur `Re s>1` se prolonge sur le demi-plan privé des pôles ; la fonction définie par l'intégrale reste holomorphe au voisinage de `rho`, contradiction avec le principal part non nul de L5.

## A2. Sens région sans zéro -> borne sur C

Le déplacement de Perron vers `sigma_0=Theta+epsilon/2` est standard en esprit. Les points suivants doivent être cités précisément :

1. une version de Perron tronquée pour une suite `c(n)=O(log^2 n)` évaluée à un demi-entier ;
2. une estimation uniforme de `zeta'/zeta` et de sa dérivée dans `sigma>=Theta+epsilon` ;
3. le contrôle des segments horizontaux du rectangle.

Le choix `x=N+1/2` est utile : il évite la singularité du noyau de Perron au voisinage d'un saut de `C`.

### Vérification des exponents

Sur la verticale déplacée,

\[
G(\sigma_0+it)=O_\epsilon(\log^2(|t|+2))
\]

donne

\[
C(x)\ll_\epsilon x^{\Theta+\epsilon/2}\log^3x
\ll_\epsilon x^{\Theta+\epsilon}.
\]

Puis

\[
Q(X)\ll_\epsilon X^{2\Theta-1+O(\epsilon)}.
\]

Le cas `Theta=1` se traite par la borne triviale `C(x)<<x log^2 x`, suffisante pour l'exposant. Le cas `Theta=1/2` conduit bien à `Q(X)=X^{o(1)}`.

## A3. Points mineurs

- Dans L6.2, la phrase « choisissons `a_1<a` » semble être un reliquat rédactionnel : `a_1` n'est pas utilisé.
- Il serait utile de préciser que `Q(X)>0` à partir d'un certain point, afin que `log Q(X)` soit sans ambiguïté ; alternativement remplacer par `log(1+Q(X))`, ce qui ne change pas l'exposant.
- Fixer une référence exacte pour l'estimation partielle de `zeta'/zeta` et la version de Perron utilisée.

## A4. Question de nouveauté

Le mécanisme « abscisse des pôles <-> exposant de croissance d'une somme arithmétique » est classique. Avant toute revendication, comparer explicitement avec :

- les critères fondés sur les fonctions de von Mangoldt généralisées ;
- les reformulations de type Nyman–Beurling ;
- les théorèmes taubériens / Perron classiques pour séries de Dirichlet méromorphes.

## Recommandation

**Acceptable comme proposition/théorème de calibration si la preuve de Perron est rédigée avec une référence précise et si l'absence de revendication de progrès vers RH est maintenue.**
