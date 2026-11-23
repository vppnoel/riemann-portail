# TAC-018 — Théorème A par fenêtres : le Landau localisé pour la Loupe double

*Producteur : ia:claude · 23 novembre 2026. La preuve suit pas à pas celle de TAC-017 (`2_Methode/Depot/TAC-017/PREUVE.md`, notée « T17 »), dont chaque étape est confrontée au code Lean. Ici, il n'y a **pas** de code Lean : les pôles doubles ne sont pas traités dans l'archive d'Alpöge. Chaque différence avec T17 est signalée par ◆.*

## Énoncé

**Notations** (article 1).
- c(n) = (Λ∗Λ)(n) − Λ(n) log n + 2γΛ(n).
- Pour Re s > 1, Σ c(n) n^(−s) = G_c(s) = q(s)² + q′(s) + 2γ q(s), avec q = −ζ′/ζ. G_c est régulière en s = 1.
- **Statistique en rampe** : H(y) = Σ_{n ≤ y} c(n)(y/n − 1) − G_c(1)·y, et h(u) = H(eᵘ).

**Valeur de G_c(1).** On note t = s − 1. Comme ζ(s) = 1/t + γ − γ₁ t + …, on a q = 1/t − γ + (γ² + 2γ₁) t + O(t²). En développant q² + q′ + 2γq, les termes en 1/t² et en 1/t s'annulent, et il reste **G_c(1) = 2γ² + 6γ₁ ≈ 0,229461**, où γ₁ est la première constante de Stieltjes.

**Théorème A′ (par fenêtres).** Soit 0 < θ < 1, δ > 0 et C réel.

(i) **Plancher.** Si, pour tout Y₀, il existe Y ≥ Y₀ tel que H(y) ≥ −C·y^θ pour tout y de [Y, Y^(1+δ)], alors ζ(s) ≠ 0 pour Re s > θ.

(ii) **Plafond.** Il en va de même avec H(y) ≤ C·y^θ, mais **seulement parce que ζ n'a pas de zéro réel dans ]0, 1[**. Pour une fonction ayant un zéro réel β > θ, un plafond ne l'exclut pas. Le plancher, lui, l'exclut toujours.

(iii) **Réciproque.** Si ζ(s) ≠ 0 pour Re s > θ, alors H(y) ≪_ε y^(θ+ε) pour tout ε > 0. Cela repose sur une borne classique, rappelée à l'étape 6.

**Corollaire (caractérisation de Θ).** Θ = inf{θ : H(y) ≥ −y^θ sur des fenêtres [Y, Y^(1+δ)] arbitrairement tardives}. En particulier, RH équivaut à : pour tout ε > 0, H(y) ≥ −y^(½+ε) sur des fenêtres arbitrairement tardives.

## Étape 1 — La fonction méromorphe (◆ pôles doubles)

**(a) Mellin.** Pour Re s > 1, ∫₁^∞ Σ c(n)(y/n − 1)₊ y^(−s−1) dy = G_c(s)/(s(s − 1)), par la transformée de la rampe (T17, étape 1). On retire la transformée de G_c(1)·y, qui vaut G_c(1)/(s − 1). On obtient :

  Φ_c(s) := ∫₁^∞ H(y) y^(−s−1) dy = ( G_c(s) − s·G_c(1) ) / ( s(s − 1) ).

Le numérateur s'annule en s = 1, et G_c y est régulière : Φ_c est **régulière en 1**, c'est le rôle du centrage. En u = log y, Φ_c(s) = ∫₀^∞ h(u) e^(−su) du pour Re s > 2. La croissance est grossière : |H(y)| ≪ y log² y ≤ C₀ y².

**(b) Pôles doubles.** Près d'un zéro ρ de multiplicité m, on écrit q = −m/(s − ρ) + r₀ + r₁(s − ρ) + …. Alors :
- q² = m²/(s − ρ)² − 2m r₀/(s − ρ) + … ;
- q′ = m/(s − ρ)² + r₁ + … ;
- 2γq = −2γm/(s − ρ) + ….

Donc G_c = m(m + 1)/(s − ρ)² − 2m(r₀ + γ)/(s − ρ) + (analytique). En divisant par s(s − 1), Φ_c a en ρ une partie principale

  c₂/(s − ρ)² + c₁/(s − ρ),  avec  **c₂(ρ) = m(m + 1)/(ρ(ρ − 1)) ≠ 0**.

**(c) ◆ Le signe change.** Pour ρ réel dans ]0, 1[, ρ(ρ − 1) < 0, donc **c₂ < 0**. Pour les pôles simples de T17, le résidu −m/(ρ(ρ − 1)) était au contraire **positif**. Le signe s'inverse parce que m(m + 1) remplace −m.

## Étape 2 — Coefficients de Taylor (identique à T17)

Pour Re z > 2, a_k(z) = (−1)^k Φ_c^(k)(z)/k! = ∫₀^∞ h(u) u^k e^(−zu)/k! du.

## Étape 3 — Un seul côté suffit (◆ plancher au lieu de plafond)

Sur la fenêtre W = [U, (1 + δ)U], on suppose h ≥ −R, avec R ≥ 0. On note h⁻ = max(−h, 0). Alors |h| = 2h⁻ + h, et :

  |a_k(σ + iγ)| ≤ ∫ |h| K = 2∫ h⁻ K + Re a_k(σ),  avec K(u) = u^k e^(−σu)/k!.

Le reste est identique à T17 (étapes 3 et 4) : on borne h⁻ ≤ R sur W et |h| ≤ C₀e^(2u) hors de W, on applique Chernoff pour les queues, et l'hypothèse « H ≥ −C y^θ » donne ∫_W R e^(−θu) ≤ e^(ηU). On obtient, pour des U arbitrairement grands, un k ≥ U et tout γ :

  |a_k(σ + iγ)| **−** Re a_k(σ) ≤ C′ e^(ηU) / (σ − θ)^k.   (★′)

Avec un plafond, on retrouve (★) de T17 : |a_k(σ + iγ)| **+** Re a_k(σ) ≤ C′ e^(ηU)/(σ − θ)^k.

## Étape 4 — Développement près d'un pôle double (◆)

Si Φ_c est holomorphe sur B(z, r) privé de ρ, avec la partie principale ci-dessus, alors pour tout r′ < r il existe M tel que, pour tout k :

  | a_k(z) − (k + 1) c₂/(z − ρ)^(k+2) − c₁/(z − ρ)^(k+1) | ≤ M / r′^k.

*Preuve.* (−1)^k/k! · d^k/dz^k (z − ρ)^(−2) = (k + 1)(z − ρ)^(−k−2), et de même avec l'exposant −1 sans le facteur k + 1. Le reste est holomorphe sur B(z, r) et relève des inégalités de Cauchy. C'est l'analogue de [`landau_pole_asym`] avec un terme de plus. ∎

## Étape 5 — La contradiction

Supposons un zéro ρ₀ avec Re ρ₀ > θ. On reprend la dichotomie de T17 [`landau_dichotomy`].

**Cas 1 : pôle réel le plus proche, β > θ.** a_k(σ) est réel, et c₁, c₂ le sont aussi puisque Φ_c est réelle sur l'axe réel. Par l'étape 4 :

  −a_k(σ) ≥ (k + 1)|c₂|/(σ − β)^(k+2) − |c₁|/(σ − β)^(k+1) − M/r′^k ≥ ½ (k + 1)|c₂|/(σ − β)^(k+2)

pour k grand, **car c₂ < 0**. Le membre de gauche de (★′), pris en γ = 0, vaut |a_k(σ)| − a_k(σ) ≥ −a_k(σ). Il croît comme (σ − β)^(−k) avec σ − β < σ − θ, ce qui contredit (★′) pour η petit.

◆ **Avec un plafond**, le membre de gauche est |a_k(σ)| + a_k(σ) = 0 quand a_k(σ) < 0 : il n'y a **pas** de contradiction. Exemple témoin : h(u) = −u·e^(βu) a pour transformée de Laplace −1/(s − β)², un pôle double réel de coefficient négatif. Elle vérifie le plafond h ≤ 0 partout, et pourtant β > θ. **Un plafond ne peut pas exclure un zéro réel ; un plancher le peut.**

**Cas 2 : sinon.** C'est identique à T17. On choisit γ de sorte que z = σ + iγ ait un unique pôle le plus proche ρ, à distance d < D ≤ σ − θ ; les inégalités de Cauchy sur B(σ, D) donnent |Re a_k(σ)| ≤ M′/r′^k. Par l'étape 4 :

  |a_k(z)| ≥ (k + 1)|c₂|/d^(k+2) − |c₁|/d^(k+1) − M/r′^k,

avec d < r′. C'est contradictoire avec (★′), mais aussi avec (★), puisque seul |Re a_k(σ)| intervient et qu'il est petit. Le facteur k + 1 **aide** la contradiction.

**Conclusion.** (i) est démontré. (ii) suit, puisque le cas 1 ne se produit pas pour ζ : ζ(σ) < 0 sur ]0, 1[.

## Étape 6 — Réciproque (iii)

Si ζ(s) ≠ 0 pour Re s > θ, alors Φ_c est holomorphe sur Re s > θ, et H(y) = (1/2πi) ∫_{(2)} Φ_c(s) y^s ds. Classiquement (Titchmarsh, ch. 14 ; **à vérifier sur l'original**), l'absence de zéros pour Re s > θ entraîne q(σ + it) ≪ (log |t|)^A pour σ ≥ θ + ε et |t| ≥ 2. Donc G_c ≪ (log |t|)^(2A). Comme Φ_c décroît alors comme |s|^(−2) au log près, on peut déplacer la droite d'intégration jusqu'à Re s = θ + ε, et l'intégrale converge absolument : H(y) ≪_ε y^(θ+ε). ∎ *(modulo la borne citée)*

La forme plus fine H(y) ≪ y^θ log y, que j'avais prévue (P3), demanderait la convergence absolue de Σ_ρ |c₁(ρ)|. Or c₁ dépend du terme constant r₀ de q en ρ, qui peut être grand quand deux zéros sont proches. **Je ne l'ai pas démontrée.**

## Ce que la preuve utilise

Les mêmes ingrédients que T17, plus deux choses :
- le développement près d'un pôle double ;
- le fait classique que ζ < 0 sur ]0, 1[, pour le point (ii) seulement.

La réciproque utilise en plus la borne classique sur ζ′/ζ hors des zéros.
