# TAC-017 — Le Landau localisé pour ζ : une preuve lisible, confrontée au Lean

*Producteur : ia:claude · 23 novembre 2026 ; **reprise** le même jour après la vérification de ChatGPT (#40). Chaque déclaration Lean est un lien vers sa ligne au commit consulté. Code Lean consulté : `leanprover-community/riemann-hypothesis`, commit `51d9b1a28026d458aef9c9af3df8b083276e3d2d` (23 novembre 2026). Chemins relatifs à `src/Development/AutomorphicArithmetic/DedekindLFunctions/`, abrégé `DL/`. Les noms entre crochets sont les déclarations Lean.*

## Énoncé

**Notations.**
- On note G(y) = Σ_{n ≤ y} Λ(n)(y/n − 1) − y(log y − 1 − γ) pour y ≥ 1 [[`Deduction.G`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/CharFamily.lean#L25), `DL/CharFamily.lean`]. Pour ζ, c'est exactement [`Gchi 1`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/CharFamily.lean#L19), la statistique du guide.
- On pose g(u) = G(eᵘ) [[`gm`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauZeroFreeCriterion.lean#L13), `DL/LandauZeroFreeCriterion.lean`].

**Proposition (cas de ζ).** Soit 0 < θ < 1, δ > 0 et C réel. On suppose que pour tout Y₀ il existe Y ≥ Y₀ tel que G(y) ≤ C·y^θ pour **tout** y de [Y, Y^(1+δ)]. Alors ζ(s) ≠ 0 pour Re s > θ.

C'est [[`Deduction.zeroFree_of_rpow_window`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/ZeroFreeOfRpowWindow.lean#L15), `DL/LandauTheorems/ZeroFreeOfRpowWindow.lean`], appliqué à la famille réduite au caractère trivial de module 1 (poids 1). C'est la contraposée de la Proposition du §3 du guide : « s'il y a un zéro de partie réelle > θ, alors, pour tout C, toute fenêtre tardive contient un y avec G(y) > C·y^θ ».

On ne suppose que **l'inégalité d'un seul côté**, et seulement sur des fenêtres arbitrairement tardives, pas sur toute la demi-droite.

## Étape 1 — Passer de y à u, et de G à une fonction méromorphe

**(a) La rampe.** Pour n ≥ 1 et Re s > 1, ∫₁^∞ (y/n − 1)₊ y^(−s−1) dy = n^(−s)/(s(s − 1)) [[`mellin_ramp`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/MellinRamp.lean#L14)]. On somme contre Λ(n), puis on retire les transformées des deux termes correctifs. On obtient, pour Re s > 1 [[`mellin_Gchi_modOne`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/mellinGchiModOne.lean#L119)] :

  ∫₁^∞ G(y) y^(−s−1) dy = −( ζ′/ζ(s) + 1/(s − 1) + 1 − (1 + γ)s ) / (s(s − 1)).

On note Φ(s) le membre de droite. En posant y = eᵘ, Φ(s) = ∫₀^∞ g(u) e^(−su) du pour Re s > 2 [[`poleData_char`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/poleData.lean#L141), [`poleData_integrable`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/poleData.lean#L95)].

**(b) Les singularités de Φ.** Écrivons ζ′/ζ + 1/(s − 1) = h′/h avec h(s) = (s − 1)ζ(s), entière, h(1) = 1 et h′(1) = γ [[`poleData_char`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/poleData.lean#L141)]. Alors Φ est méromorphe sur Re s > 0, et ses seules singularités sont les zéros ρ de ζ.
- Le point s = 1 n'est pas une singularité : c'est le rôle du centrage − y(log y − 1 − γ).
- En un zéro ρ de multiplicité m, Φ a un **pôle simple** de résidu c(ρ) = −m/(ρ(ρ − 1)) [[`poleData_abstract`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/poleData.lean#L26), [`poleData_char`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/poleData.lean#L141)].

**(c) Le seul fait de signe dont on a besoin.** Si ρ est réel, dans ]0, 1[, alors ρ(ρ − 1) < 0, donc **c(ρ) > 0**. Pour ζ, il n'y a pas de tel zéro, mais l'argument ne le sait pas et n'en a pas besoin : il traite le cas uniformément. Pour une famille de poids a_i > 0, les résidus s'additionnent sans pouvoir s'annuler [[`poleData`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/poleData.lean#L252), structure [`PoleData`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauZeroFreeCriterion.lean#L19), champ `pole`].

**(d) Ce qu'on retient, et rien de plus.** La suite n'utilise que les propriétés suivantes [[`PoleData`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauZeroFreeCriterion.lean#L19)] :
- g est mesurable ;
- |g(u)| ≤ C₀ e^(2u), car |G(y)| ≤ C₀ y² [[`Gchi_growth`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/GchiGrowth.lean#L41)] ;
- Φ est la transformée de Laplace de g pour Re s > 2 ;
- Φ est holomorphe sur Re s > 0 hors de l'ensemble Z des zéros, et Z est discret ;
- chaque ρ de Z est un pôle simple de résidu non nul, réel et positif si ρ est réel.

Aucune borne sur le nombre de zéros, aucune croissance de ζ′/ζ, aucun produit d'Euler n'interviennent au-delà de ces propriétés.

## Étape 2 — Les coefficients de Taylor sont des moments

Pour Re s > 2 et k ≥ 0, on pose a_k(s) = (−1)^k Φ^(k)(s)/k!. En dérivant sous l'intégrale [[`landau_coeff`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/LandauCoeff.lean#L14), [`iteratedDeriv_laplace_*`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/IteratedDerivLaplace.lean)] :

  a_k(s) = ∫₀^∞ g(u) · u^k e^(−su)/k! du.

Le noyau u^k e^(−σu)/k! est une bosse centrée en u = k/σ. En réglant k, on la place sur la fenêtre. C'est l'idée « les dérivées d'ordre élevé localisent » du guide.

## Étape 3 — Un seul côté suffit

On fixe σ > 2 et γ réel, et une fenêtre W = [U, (1 + δ)U] sur laquelle g ≤ R, avec R ≥ 0. Comme |g| = 2g⁺ − g et |e^(−(σ+iγ)u)| = e^(−σu), on a, en notant K(u) = u^k e^(−σu)/k! :

  |a_k(σ + iγ)| ≤ ∫ |g| K = 2∫ g⁺ K − ∫ g K = 2∫ g⁺ K − Re a_k(σ).

D'où |a_k(σ + iγ)| + Re a_k(σ) ≤ 2∫ g⁺ K. On coupe l'intégrale en deux :
- **sur W**, g⁺ ≤ R, et u^k e^(−(σ−θ)u)/k! ≤ (σ − θ)^(−k) pour tout u ≥ 0 [[`landau_kernel_max`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/LandauKernelMax.lean#L13)]. Cette partie vaut donc au plus 2(σ − θ)^(−k) ∫_W R(u) e^(−θu) du ;
- **hors de W**, |g| ≤ C₀ e^(2u). Cette partie vaut au plus 2C₀ ∫_{hors W} u^k e^((2−σ)u)/k! du [[`landau_window_ineq`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/landauWindowIneq.lean#L31)].

C'est ici, et seulement ici, qu'intervient l'hypothèse. Elle ne porte que sur g, et d'un seul côté. La quantité Re a_k(σ) passe à gauche : c'est l'astuce qui rend la borne unilatérale suffisante.

## Étape 4 — Régler σ et k

On choisit σ assez grand, selon δ. Pour tout U ≥ 1, il existe alors k ≥ U tel que la partie hors fenêtre soit au plus C/σ^k, par une inégalité de Chernoff [[`landau_tails`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/landauTails.lean#L85)].

Si G(y) ≤ C y^θ sur [Y, Y^(1+δ)], on prend R(u) = max(C, 0) e^(θu) sur la fenêtre en u = log y. Alors ∫_W R e^(−θu) du ≤ max(C, 0)·δU, qui est au plus e^(ηU) pour tout η > 0 et U assez grand [[`windowHyp_of_rpow`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/WindowHypOfRpow.lean#L31), [`windowHypU_of_windowHyp`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/WindowHypUOfWindowHyp.lean#L33)]. *Seuls les énoncés de ces deux lemmes ont été lus ; leur lemme auxiliaire [[`windowHyp_of_rpow_eventually`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/WindowHypOfRpow.lean)] donne bien K log Y ≤ Y^η, ce qui correspond à ce calcul.*

**Bilan** [[`landau_window_key`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/landauWindow.lean#L44)]. Il existe σ > 2 et C′ tels que, pour tout η > 0, il y ait des U arbitrairement grands et un k ≥ U avec, pour tout γ :

  |a_k(σ + iγ)| + Re a_k(σ) ≤ C′ e^(ηU) / (σ − θ)^k.   (★)

## Étape 5 — Un pôle trop proche contredit (★)

*Étape corrigée lors de la reprise (vérification de ChatGPT, fil de discussion 40 du dépôt de recherche privé, §2). La première version affirmait que le disque B(σ, σ − θ) contient ρ₀. C'est faux : seule la distance **horizontale** σ − Re ρ₀ est < σ − θ, et la distance euclidienne √((σ − Re ρ₀)² + (Im ρ₀)²) peut être bien plus grande. Par exemple, σ = 3, θ = ½ et ρ₀ = ¾ + 10i donnent 2,25 contre plus de 10. La dichotomie ci-dessous est celle du Lean.*

Supposons un zéro ρ₀ avec Re ρ₀ > θ. Comme aucune singularité n'a de partie réelle > 2 [[`landau_pole_re_le`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/LandauPoleReLe.lean#L33)] et que σ > 2, tous les pôles sont à gauche de σ, et ρ₀ est à distance **horizontale** σ − Re ρ₀ < σ − θ de σ.

**La dichotomie** [[`landau_dichotomy`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/LandauDichotomy.lean#L28)]. On regarde le disque fermé B̄(σ, σ − θ).
- *S'il ne contient aucun pôle*, on pose D = σ − θ. Le disque B(σ, D) est sans pôle, et ρ₀ est un pôle de distance horizontale < D : on est dans le **cas A**.
- *Sinon*, il contient un nombre fini de pôles, puisque ceux-ci sont isolés et que le disque est compact. Soit d > 0 la plus petite distance euclidienne de σ à l'un d'eux.
  - S'il existe un pôle, n'importe où, de distance horizontale < d, on pose D = d. B(σ, D) est sans pôle : c'est encore le **cas A**.
  - Sinon, tout pôle ρ à distance d vérifie d ≤ σ − Re ρ ≤ |σ − ρ| = d. Il est donc réel : c'est un réel β avec σ − β = d. Comme ρ₀ a une distance horizontale ≥ d, on a d ≤ σ − Re ρ₀ < σ − θ, donc β > θ. Les autres pôles du disque fermé, en nombre fini, sont à distance > d. On peut donc choisir r avec σ − β < r ≤ σ − θ tel que β soit le seul pôle de B(σ, r) : c'est le **cas B**.

**Cas B : un pôle réel β > θ, seul dans B(σ, r).** Pour tout r′ < r, a_k(σ) = c(β)/(σ − β)^(k+1) + O(r′^(−k)) [[`landau_pole_asym`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/LandauPoleAsym.lean#L23)], avec **c(β) > 0** d'après l'étape 1(c). On choisit r′ entre σ − β et r. Alors Re a_k(σ) ≥ c(β)/(σ − β)^(k+1) − O(r′^(−k)), qui croît comme (σ − β)^(−k), alors que σ − β < σ − θ. Comme U ≤ k, on a e^(ηU) ≤ e^(ηk). En prenant η < log((σ − θ)/(σ − β)), le membre de droite de (★) devient négligeable devant Re a_k(σ), ce qui est absurde pour k grand [[`landau_growth_contra`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/LandauGrowthContra.lean#L13)].

C'est le seul endroit où le signe du résidu sert. C'est le théorème de Pringsheim–Landau : un pôle réel de résidu positif se voit sur l'axe réel.

**Cas A : B(σ, D) sans pôle, D ≤ σ − θ, et un pôle ρ₁ de distance horizontale < D.** On déplace le centre verticalement [[`landau_nearest`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/LandauNearest.lean#L40)] : il existe γ réel, un pôle ρ et un rayon r ≤ D tels que, pour z = σ + iγ, on ait d′ := |z − ρ| < r et ρ soit le seul pôle de B(z, r). Le choix de γ évite les points équidistants de deux pôles [[`landau_nearest_equi`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/LandauNearest.lean#L14)]. On prend r′ avec d′ < r′ < r. Alors :
- a_k(z) = c(ρ)/(z − ρ)^(k+1) + O(r′^(−k)) [[`landau_pole_asym`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/LandauPoleAsym.lean#L23)], donc |a_k(z)| ≥ |c(ρ)|/d′^(k+1) − M/r′^k ;
- Φ est holomorphe sur B(σ, D) et r′ < r ≤ D, donc, par les inégalités de Cauchy, |Re a_k(σ)| ≤ |a_k(σ)| ≤ M′/r′^k [[`landau_cauchy`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/LandauCauchy.lean#L13)].

On reporte dans (★) : |c(ρ)|/d′^(k+1) ≤ C′e^(ηU)/(σ − θ)^k + (M + M′)/r′^k, avec d′ < r′ et d′ < r ≤ σ − θ. En prenant η < log((σ − θ)/d′) et en utilisant U ≤ k, c'est absurde pour k grand [[`landau_window_contra`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/landauWindow.lean#L24)].

**Conclusion.** Tout zéro de ζ vérifie Re ρ ≤ θ [[`landau_window`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/landauWindow.lean#L87)]. Avec ζ(s) ≠ 0 pour Re s ≥ 1 [[`charFamily_LFunction_ne_zero_of_one_le_re`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/CharFamilyLFunctionNeZeroOfOneLeRe.lean#L13)], on obtient ζ(s) ≠ 0 pour Re s > θ [[`lemmaL`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/lemmaL.lean#L17), [`zeroFree_of_rpow_window`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/ZeroFreeOfRpowWindow.lean#L15)]. ∎

## Ce que la preuve utilise, en une liste

1. La transformée de Mellin de la rampe, et la forme logarithmique de ζ′/ζ près de ses zéros (multiplicité m, résidu −m/(ρ(ρ − 1))).
2. Une croissance grossière |G(y)| ≪ y².
3. Les inégalités de Cauchy et le développement près d'un pôle simple.
4. Le signe des résidus aux pôles réels, conséquence de m ≥ 1 et de ρ(ρ − 1) < 0.
5. Un réglage de σ, k et η, et une inégalité de Chernoff pour les queues.

Rien d'autre. Il n'y a ni produit d'Euler, ni positivité des coefficients de Dirichlet, ni comptage des zéros, ni théorie automorphe. **Le Lean confirme que cette étape est abstraite** : [[`landau_window`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/landauWindow.lean#L87)] ne prend en entrée qu'une structure [`PoleData`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauZeroFreeCriterion.lean#L19), sans aucune série de Dirichlet.

## Confrontation à l'énoncé du guide

| Point | Guide, §3 | Lean | Écart |
|---|---|---|---|
| Forme | « zéro à droite de θ ⇒ chaque fenêtre tardive contient y avec G > C y^θ » | « G ≤ C y^θ sur des fenêtres arbitrairement tardives ⇒ aucun zéro à droite de θ » | contraposées l'une de l'autre : **équivalentes** |
| θ | 0 < θ < 1 dans l'énoncé de la Proposition (p. 3) ; θ > ½ seulement dans son application (p. 4) | 0 < θ < 1 | **aucun** (corrigé lors de la reprise : la première version disait à tort « Lean est plus général ») |
| δ, C | énoncé pour tout δ, C ; utilisé avec δ = ½, C = 1 | δ > 0 et C réel quelconques | aucun |
| Famille | familles positives F | `CharFamily` : poids a_i > 0, et pour chaque i, N_i = 1 ou χ_i ≠ 1 | Lean exclut les caractères principaux de module > 1, qui se ramènent au primitif par le §1 du guide |
| Statistique | G(y) = Σ Λ(n)(y/n − 1) − y(log y − 1 − γ) | [`Deduction.G`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/CharFamily.lean#L25), identique | aucun |
