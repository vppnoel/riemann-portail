# Calibration spectrale — `Q(X,T)` (v3)

## But

`Q(X)` compresse trop fortement l'information : son exposant asymptotique ne retient que
le zéro le plus à droite. Pour comparer le cadre aux théorèmes de **densité de zéros**, il
faut conserver simultanément :

- une longueur logarithmique `L=log X` ;
- une hauteur spectrale `T` ;
- une largeur de bande `Δ`.

La v3 introduit donc un observable à deux paramètres (en pratique trois avec `Δ`).

## Définition

Avec

\[
B(t)=e^{-t/2}C(e^t),
\]

choisissons une fenêtre temporelle lisse `w` supportée dans `(0,1)` et définissons

\[
\mathcal B_{L,w}(\tau)
=\int_0^L B(t)w(t/L)e^{-i\tau t}\,dt.
\]

Pour une fenêtre fréquentielle non négative `W`,

\[
Q_{w,W}(L;T,\Delta)
=\frac1{2\pi}\int_{\mathbb R}
W\!\left(\frac{\tau-T}{\Delta}\right)
|\mathcal B_{L,w}(\tau)|^2d\tau.
\]

Cette quantité est positive et calculable à partir de `C(x)`.

## Pourquoi cela peut voir une densité

Sous la formule explicite, un zéro

\[
\rho=\beta+i\gamma
\]

contribue à `B(t)` par une oscillation de fréquence `γ` et d'amplitude comportant
`e^{(β-1/2)t}`. Une fenêtre centrée en `T` isole donc principalement les zéros avec
`γ≈T`, alors que la dépendance en `L` conserve l'information sur `β`.

Le scénario recherché est une inégalité de la forme

\[
Q_{w,W}(L;T,\Delta)
\gtrsim
\sum_{\substack{|\gamma-T|\lesssim\Delta\\\beta\ge\sigma}}
\text{poids}(\rho,L),
\]

puis une majoration arithmétique indépendante du côté gauche. **Aucune telle inégalité
suffisante n'est prouvée dans v3.**

## Benchmark

La référence quantitative moderne est la borne de Guth–Maynard (2026)

\[
N(\sigma,T)\le T^{30(1-\sigma)/13+o(1)}.
\]

Le premier objectif n'est pas de la battre mais de montrer que notre observable sait produire
une densité non triviale lorsque l'on injecte un outil standard sur les polynômes de Dirichlet.

## Implémentation

`src/spectral_calibration.py` contient :

- fenêtres Hann lisses discrètes ;
- transformée locale de `B(t)` ;
- intégration d'énergie par bandes ;
- comparaison possible avec `B_explicit` de `src/explicit_formula.py`.

`scripts/run_v3.py` crée une petite table de calibration sans prétention asymptotique.

## Critère de rejet

Si `Q(X,T)` n'arrive pas à retrouver une borne de densité déjà connue, il ne faut pas
continuer à l'utiliser comme route directe vers RH. Il restera un outil de reformulation et de
diagnostic spectral.

## Résultats de localisation (v3.2)
`scripts/run_localisation.py` : fenêtre de Hann sur t ∈ [4, ln 3·10⁵], bande ω ∈ [8, 80].
Parmi les 20 pics d'énergie les plus élevés, **18 sont à moins de 0,5 d'un zéro de ζ** (résolution
2π/L ≈ 0,73) ; les deux autres (ω ≈ 10,9 et 35,0) ont une énergie négligeable (≈ 0,03). Le premier
zéro (14,13) est le pic dominant. L'observable *localise* donc les zéros en hauteur : c'est le
minimum requis pour P2.3, pas un résultat de densité.

## Précision sur la référence Guth–Maynard
L'estimation N(σ,T) ≤ T^{30(1−σ)/13+o(1)} n'améliore Huxley (12/5) et Ingham que dans la plage
voisine de σ = 3/4 (d'après les exposés des auteurs : environ 7/10 < σ ≲ 3/4). Ailleurs elle n'est pas
la meilleure borne connue.

## Analyse P2.3 (jugement, non démontré)
Par Mellin–Plancherel, pour σ > 1 : ∫|C|² x^{-2σ-1}dx = (1/2π)∫|G(σ+it)|²/|σ+it|² dt. Aller à σ < 1
exige de contrôler Σ_{n≤x} c(n) n^{-1/2-iτ} en moyenne sur τ : le théorème de valeur moyenne ne
donne que la borne triviale, et tout gain exige une estimation de grandes valeurs pour des coefficients
de type Möbius, c'est-à-dire la machinerie Halász–Montgomery–Huxley–Guth–Maynard. Attente : une
reformulation, pas une densité nouvelle ; le test reste à faire.
