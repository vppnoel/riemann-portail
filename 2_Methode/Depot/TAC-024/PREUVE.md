# TAC-024 (reprise de TAC-022) — Théorème A par fenêtres pour la Loupe double : énoncé, sens direct et réciproque

*Producteur : ia:claude · 23 novembre 2026. Le sens direct reprend celui de TAC-022, que la vérification ([#54](https://github.com/vppnoel/Riemann/issues/54)) a jugé correct. Il est rattaché aux étapes de la preuve vérifiée de TAC-017 (`2_Methode/Depot/TAC-017/PREUVE.md`, notée « T17 »), elle-même confrontée au code Lean d'Alpöge. La réciproque (étape 6) est **entièrement refaite**. Il n'y a pas de code Lean pour les pôles doubles. Chaque différence avec T17 est signalée par ◆.*

## Énoncé

**Notations** (article 1).
- c(n) = (Λ∗Λ)(n) − Λ(n) log n + 2γΛ(n).
- Pour Re s > 1, Σ c(n) n^(−s) = G_c(s) = q(s)² + q′(s) + 2γ q(s), avec q = −ζ′/ζ. G_c est régulière en s = 1.
- **Statistique en rampe** : H(y) = Σ_{n ≤ y} c(n)(y/n − 1) − G_c(1)·y, et h(u) = H(eᵘ).
- Θ = sup{Re ρ : ζ(ρ) = 0, 0 < Re ρ < 1}. On sait que ½ ≤ Θ ≤ 1, puisqu'il y a des zéros sur Re s = ½.

**Valeur de G_c(1).** On note t = s − 1. Comme ζ(s) = 1/t + γ − γ₁ t + …, on a q = 1/t − γ + (γ² + 2γ₁) t + O(t²). En développant q² + q′ + 2γq, les termes en 1/t² et en 1/t s'annulent, et il reste **G_c(1) = 2γ² + 6γ₁ ≈ 0,229461**, où γ₁ est la première constante de Stieltjes.

**Théorème A′.** Soit 0 < θ < 1, δ > 0 et C réel.

(i) **Plancher.** Si, pour tout Y₀, il existe Y ≥ Y₀ tel que H(y) ≥ −C·y^θ pour tout y de [Y, Y^(1+δ)], alors ζ(s) ≠ 0 pour Re s > θ.

(ii) **Plafond.** Il en va de même avec H(y) ≤ C·y^θ, mais **seulement parce que ζ n'a pas de zéro réel dans ]0, 1[**. Pour une fonction ayant un zéro réel β > θ, un plafond ne l'exclut pas. Le plancher, lui, l'exclut toujours.

(iii) **Réciproque, au seuil.** Soit ½ ≤ θ < 1. Si ζ(s) ≠ 0 pour Re s > θ, alors, pour tout y ≥ y₀(θ) = exp(4/(1 − θ)),

  |H(y)| ≤ A · y^θ · ( log y + 1/(1 − θ) ),

où A est une constante absolue. En particulier H(y) = O_θ(y^θ log y), pour **tous** les y grands, et pas seulement sur des fenêtres. (Pour θ < ½, l'hypothèse est fausse, puisque ζ a des zéros sur Re s = ½.)

**Corollaire 1 (caractérisation de Θ).** Avec la convention inf ∅ = 1,

  Θ = inf{ θ ∈ ]0, 1[ : H(y) ≥ −y^θ pour tout y de fenêtres [Y, Y^(1+δ)] arbitrairement tardives, pour un δ > 0 }.

*Preuve.* Notons I l'infimum. Si θ est dans l'ensemble, (i) avec C = 1 donne Θ ≤ θ ; donc Θ ≤ I (y compris si l'ensemble est vide, car Θ ≤ 1 = inf ∅). Réciproquement, si Θ < 1, soit θ′ ∈ ]Θ, 1[. On applique (iii) avec θ = max(Θ, ½) = Θ : |H(y)| ≤ A y^Θ (log y + 1/(1 − Θ)) ≤ y^θ′ pour y grand. Le plancher vaut donc pour **tout** y grand, a fortiori sur des fenêtres, et θ′ est dans l'ensemble. Ainsi I ≤ θ′ pour tout θ′ > Θ, d'où I ≤ Θ. Si Θ = 1, l'ensemble est vide (par (i)) et I = 1 = Θ. ∎

**Corollaire 2.** Les énoncés suivants sont équivalents :
- RH ;
- H(y) = O(√y log y) ;
- pour tout ε > 0, H(y) ≥ −y^(½+ε) sur des fenêtres [Y, Y^(1+δ)] arbitrairement tardives (pour un δ > 0 qui peut dépendre de ε).

*Preuve.* RH entraîne la deuxième par (iii) avec θ = ½. La deuxième entraîne la troisième. La troisième entraîne Θ ≤ ½ + ε pour tout ε, par (i), donc RH. ∎

## Étape 1 — La fonction méromorphe (◆ pôles doubles)

**(a) Mellin.** Pour Re s > 1, ∫₁^∞ Σ c(n)(y/n − 1)₊ y^(−s−1) dy = G_c(s)/(s(s − 1)), par la transformée de la rampe (T17, étape 1). On retire la transformée de G_c(1)·y, qui vaut G_c(1)/(s − 1). On obtient :

  Φ_c(s) := ∫₁^∞ H(y) y^(−s−1) dy = ( G_c(s) − s·G_c(1) ) / ( s(s − 1) ).

Le numérateur s'annule en s = 1, où G_c est régulière : Φ_c est **régulière en 1**, c'est le rôle du centrage. En u = log y, Φ_c(s) = ∫₀^∞ h(u) e^(−su) du pour Re s > 2. La croissance est grossière : |c(n)| ≪ log² n, donc |H(y)| ≪ y log² y ≤ C₀ y² (pour y ≥ 1), soit |h(u)| ≤ C₀ e^(2u). Φ_c se prolonge en une fonction méromorphe sur Re s > 0, dont les pôles sont exactement les zéros non triviaux de ζ.

**(b) Pôles doubles.** Près d'un zéro ρ de multiplicité m, on écrit q = −m/(s − ρ) + r₀ + r₁(s − ρ) + …. Alors :
- q² = m²/(s − ρ)² − 2m r₀/(s − ρ) + … ;
- q′ = m/(s − ρ)² + r₁ + … ;
- 2γq = −2γm/(s − ρ) + ….

Donc G_c = m(m + 1)/(s − ρ)² − 2m(r₀ + γ)/(s − ρ) + (analytique). En divisant par s(s − 1), Φ_c a en ρ une partie principale

  c₂/(s − ρ)² + c₁/(s − ρ),  avec  **c₂(ρ) = m(m + 1)/(ρ(ρ − 1)) ≠ 0**.

**(c) ◆ Le signe change.** Pour ρ réel dans ]0, 1[, ρ(ρ − 1) < 0, donc **c₂ < 0**. Pour les pôles simples de T17, le résidu −m/(ρ(ρ − 1)) était au contraire **positif**. Le signe s'inverse parce que m(m + 1) remplace −m.

## Étape 2 — Coefficients de Taylor (identique à T17)

Pour Re z > 2, a_k(z) = (−1)^k Φ_c^(k)(z)/k! = ∫₀^∞ h(u) u^k e^(−zu)/k! du. C'est l'analogue de [`landau_coeff`] (T17).

## Étape 3 — Un seul côté suffit (◆ plancher au lieu de plafond)

Soit U = log Y et W = [U, (1 + δ)U]. L'hypothèse de (i) donne h ≥ −R sur W, avec R(u) = |C| e^(θu) ≥ 0, et ∫_W R(u) e^(−θu) du = |C| δ U ≤ e^(ηU) pour U grand, quel que soit η > 0 fixé (comme [`windowHyp_of_rpow`] dans T17).

On note h⁻ = max(−h, 0). Comme h est réelle, |h| = 2h⁻ + h. Avec K(u) = u^k e^(−σu)/k! ≥ 0, on a donc, pour σ > 2 et γ réel :

  |a_k(σ + iγ)| ≤ ∫ |h| K = 2∫ h⁻ K + a_k(σ).

Le reste est identique à T17 (étapes 3 et 4, [`landau_window_ineq`], [`landau_kernel_max`], [`landau_tails`]) : h⁻ ≤ R sur W, |h| ≤ C₀ e^(2u) hors de W, et l'on contrôle les queues. On obtient σ > 2 et C′ tels que, pour tout η > 0, il existe des U arbitrairement grands et un entier k ≥ U avec, pour tout γ :

  |a_k(σ + iγ)| **−** Re a_k(σ) ≤ C′ e^(ηU) / (σ − θ)^k.   (★′)

Avec un plafond, on retrouve l'inégalité (K) de T17 : |a_k(σ + iγ)| **+** Re a_k(σ) ≤ C′ e^(ηU)/(σ − θ)^k.

## Étape 4 — Développement près d'un pôle double (◆)

Si Φ_c est holomorphe sur B(z, r) privé de ρ, avec la partie principale ci-dessus, alors pour tout r′ < r il existe M tel que, pour tout k :

  | a_k(z) − (k + 1) c₂/(z − ρ)^(k+2) − c₁/(z − ρ)^(k+1) | ≤ M / r′^k.

*Preuve.* On a (−1)^k/k! · d^k/dz^k (z − ρ)^(−2) = (k + 1)(z − ρ)^(−k−2), et de même avec l'exposant −1, sans le facteur k + 1. Le reste est holomorphe sur B(z, r) et relève des inégalités de Cauchy. C'est l'analogue de [`landau_pole_asym`] avec un terme de plus. ∎

## Étape 5 — La contradiction

On suit la dichotomie exacte du Lean, qui est purement géométrique et vaut donc telle quelle pour les pôles doubles : elle n'utilise que le fait que les pôles soient isolés et tous à gauche de σ.

Supposons un zéro ρ₀ avec Re ρ₀ > θ. On fixe σ > 2 comme dans (★′) : tous les pôles de Φ_c sont à gauche de σ, et ρ₀ est à distance **horizontale** σ − Re ρ₀ < σ − θ de σ (sa distance euclidienne peut être bien plus grande). **Dichotomie** [`landau_dichotomy`] :
- **(A)** il existe D ≤ σ − θ tel que B(σ, D) ne contienne aucun pôle, mais qu'un pôle soit à distance horizontale < D ;
- **(B)** il existe un pôle réel β > θ, seul pôle d'un disque B(σ, r) avec σ − β < r ≤ σ − θ.

Pour l'obtenir : si le disque fermé B̄(σ, σ − θ) est sans pôle, on prend D = σ − θ (cas A, témoin ρ₀). Sinon, soit d la plus petite distance de σ à un pôle. Si un pôle a une distance horizontale < d, on prend D = d (cas A). Sinon, tout pôle à distance d est réel ; il donne β, avec β > θ puisque d ≤ σ − Re ρ₀ < σ − θ (cas B).

**Le lemme de contradiction** (T17, [`landau_growth_contra`], [`landau_window_contra`]). Soit 0 < d < e ≤ E, c > 0, M et C′ réels, et η = ½ log(e/d) < log(E/d). Une inégalité c/d^k ≤ M/e^k + C′e^(ηU)/E^k ne peut pas valoir pour des U arbitrairement grands avec k ≥ U. Ici, le facteur k + 1 du pôle double ne fait que renforcer le membre de gauche.

**Cas B : pôle réel β > θ, seul dans B(σ, r).** a_k(σ) est réel, et c₁, c₂ le sont aussi, puisque Φ_c est réelle sur l'axe réel. Soit d = σ − β et e = (d + r)/2. Par l'étape 4 :

  −a_k(σ) ≥ (k + 1)|c₂|/d^(k+2) − |c₁|/d^(k+1) − M/e^k ≥ |c₂|/d^(k+2) − M/e^k

pour k ≥ |c₁| d/|c₂|, **car c₂ < 0**. Le membre de gauche de (★′), pris en γ = 0, vaut |a_k(σ)| − a_k(σ) ≥ −a_k(σ). Avec (★′), on obtient (|c₂|/d²)/d^k ≤ M/e^k + C′e^(ηU)/(σ − θ)^k, ce que le lemme exclut (E = σ − θ ≥ r > e).

◆ **Avec un plafond**, le membre de gauche est |a_k(σ)| + a_k(σ) = 0 quand a_k(σ) < 0 : il n'y a **pas** de contradiction. Exemple témoin : h(u) = −u·e^(βu) a pour transformée de Laplace −1/(s − β)², un pôle double réel de coefficient négatif. Elle vérifie le plafond h ≤ 0 partout, et pourtant β > θ. **Un plafond ne peut pas exclure un zéro réel ; un plancher le peut.**

**Cas A : B(σ, D) sans pôle, D ≤ σ − θ.** On déplace le centre verticalement [`landau_nearest`] : il existe γ, un pôle ρ et un rayon r ≤ D tels que, pour z = σ + iγ, d := |z − ρ| < r, ρ étant le seul pôle de B(z, r). Soit e = (d + r)/2 < r ≤ D. Alors :
- par l'étape 4, |a_k(z)| ≥ (k + 1)|c₂|/d^(k+2) − |c₁|/d^(k+1) − M/e^k ≥ |c₂|/d^(k+2) − M/e^k pour k grand ;
- Φ_c est holomorphe sur B(σ, D) et e < D, donc |Re a_k(σ)| ≤ M′/e^k (Cauchy, [`landau_cauchy`]).

Le membre de gauche de (★′) est au moins |a_k(z)| − |Re a_k(σ)|. On obtient (|c₂|/d²)/d^k ≤ (M + M′)/e^k + C′e^(ηU)/(σ − θ)^k, ce que le lemme exclut. Le même calcul vaut avec un plafond.

**Conclusion.** (i) est démontré. (ii) suit, puisque le cas B ne se produit pas pour ζ : il exigerait un zéro réel β ∈ ]θ, 1[, or ζ(σ) < 0 sur ]0, 1[.

## Étape 6 — Réciproque (iii), refaite

*La version de TAC-022 déplaçait le contour de Φ_c, qui n'est pas absolument intégrable sur Re s = 2 : le terme G_c(1)/(s − 1) a un module ~ |G_c(1)|/|t| (objection de la vérification, #54). On suit la piste du vérificateur : on déplace le contour de la rampe **non centrée**, on récupère G_c(1)·y comme résidu en 1, puis on contrôle l'intégrale par blocs.*

**Deux faits classiques** (Titchmarsh, *The Theory of the Riemann Zeta-Function*, 2ᵉ éd., théorèmes 9.2 et 9.6(A) ; Davenport, *Multiplicative Number Theory*, ch. 15) :
- **(F1)** le nombre de zéros ρ = β + iγ avec T ≤ γ ≤ T + 1, comptés avec multiplicité, est O(log T) pour T ≥ 2 ;
- **(F2)** uniformément pour −1 ≤ σ ≤ 2 et |t| ≥ 2, ζ′/ζ(s) = Σ_{|t−γ|<1} 1/(s − ρ) + O(log |t|).

Ce sont des énoncés inconditionnels, qui portent sur tous les zéros. Ils ne demandent aucune densité de zéros. Je n'ai pas eu les deux livres sous la main. Les deux énoncés ont été contrôlés le 23 novembre 2026 sur un cours en ligne : [N. H. Bingham, *Analytic Number Theory*, Imperial College, leçon 27](https://www.ma.ic.ac.uk/~bin06/M34PM16-Analytic-Number-Theory/2013/m3pm16l27(13).pdf). Il énonce (F2) pour t ≥ 1 et −1 ≤ σ ≤ 2, avec |t − γ| ≤ 1 au lieu de < 1, ce qui ne change rien ici, et il donne (F1) sous la forme « O(log T) zéros avec |γ − T| ≤ 1 ».

**(a) Formule de Perron exacte.** Pour x > 0 et c > 1, (1/2πi) ∫_{(c)} x^s/(s(s − 1)) ds = (x − 1)₊ : pour x > 1, on déplace vers la gauche et l'on ramasse les résidus x en 1 et −1 en 0 ; pour x < 1, on déplace vers la droite. L'intégrale converge absolument. On pose F(s) = G_c(s)/(s(s − 1)). Comme G_c est bornée sur Re s = 2 (série absolument convergente), on peut intervertir somme et intégrale. Pour tout y > 0 :

  Σ_{n ≤ y} c(n)(y/n − 1) = (1/2πi) ∫_{(2)} F(s) y^s ds.

**(b) Déplacement du contour.** On suppose ½ ≤ θ < 1 et aucun zéro avec Re ρ > θ. Soit 0 < a ≤ (1 − θ)/2 et σ₀ = θ + a. Dans la bande σ₀ ≤ Re s ≤ 2, F est méromorphe avec un seul pôle, simple, en s = 1 : s = 0 est hors de la bande, et les zéros sont à gauche de σ₀. Son résidu est G_c(1), car G_c est régulière en 1. Le résidu de F(s)y^s en 1 est donc G_c(1)·y. On déplace l'intégrale de Re s = 2 à Re s = σ₀, entre les hauteurs ±T. Les segments horizontaux tendent vers 0 quand T → ∞ (point (e) ci-dessous). On obtient :

  H(y) = (1/2πi) ∫_{(σ₀)} F(s) y^s ds,  donc  |H(y)| ≤ (y^(σ₀)/2π) ∫_{−∞}^{+∞} |F(σ₀ + it)| dt.

**(c) Le lemme des blocs.** Il existe une constante absolue B telle que, pour tout entier j ≥ 3, sous l'hypothèse de (b) :

  ∫_j^{j+1} |G_c(σ₀ + it)| dt ≤ B log²j / a.

*Preuve.* Soit Z_j l'ensemble des zéros ρ = β + iγ avec j − 2 ≤ γ ≤ j + 3, comptés avec multiplicité. Par (F1), son cardinal N_j est ≤ B₁ log j. On considère le rectangle R_j = {−1 ≤ σ ≤ 2, j − ½ ≤ t ≤ j + 3/2} et

  E_j(s) = q(s) + Σ_{ρ ∈ Z_j} 1/(s − ρ).

- *E_j est holomorphe sur R_j.* En un zéro ρ de multiplicité m, q = −ζ′/ζ a un pôle simple de résidu −m, que la somme compense exactement si ρ ∈ Z_j. Les zéros hors de Z_j sont à distance > 3/2 de R_j. Le pôle s = 1 et les zéros triviaux sont hors de R_j, puisque j ≥ 3 et σ ≥ −1.
- *|E_j| ≤ B₂ log j sur R_j.* Pour s ∈ R_j, (F2) donne q(s) = −Σ_{|t−γ|<1} 1/(s − ρ) + O(log t). Les zéros avec |t − γ| < 1 sont dans Z_j. Les autres zéros de Z_j vérifient |s − ρ| ≥ 1, et ils sont au plus B₁ log j. L'inégalité vaut hors des zéros, donc partout sur R_j par continuité.
- *|E_j′| ≤ 4B₂ log j* aux points σ₀ + it, j ≤ t ≤ j + 1, par l'inégalité de Cauchy sur le disque de rayon ¼, qui est contenu dans R_j (car ¼ ≤ σ₀ ± ¼ ≤ 2).

Pour s = σ₀ + it et ρ ∈ Z_j, on a β ≤ θ, donc |s − ρ|² ≥ a² + (t − γ)², et ∫_ℝ dt/(a² + (t − γ)²) = π/a. On note S(s) = Σ_{Z_j} 1/(s − ρ). Alors q = E_j − S et q′ = E_j′ + Σ_{Z_j} 1/(s − ρ)². Par Cauchy–Schwarz, |S|² ≤ N_j Σ_{Z_j} 1/|s − ρ|². Donc, sur le bloc :
- ∫ |q|² ≤ 2∫ |E_j|² + 2∫ |S|² ≤ 2B₂² log²j + 2N_j² π/a ;
- ∫ |q′| ≤ 4B₂ log j + N_j π/a ;
- ∫ |q| ≤ (∫ |q|²)^(1/2).

Comme a ≤ ½ et G_c = q² + q′ + 2γq, la somme est ≤ B log²j/a. ∎

**(d) L'intégrale sur la droite.**
- *Hauteurs |t| ≥ 3.* Sur le bloc [j, j + 1], |s(s − 1)| ≥ t² ≥ j², donc ∫_{|t|≥3} |F| ≤ 2 Σ_{j≥3} B log²j/(a j²) = B₃/a. Les t négatifs se traitent par conjugaison : G_c(s̄) est le conjugué de G_c(s).
- *Hauteurs |t| ≤ 3.* Le rectangle [½, 1] × [−3, 3] ne contient aucun zéro de ζ, car le premier zéro a une hauteur ≈ 14,13. G_c y est holomorphe, puisque le seul pôle de q y est s = 1, où G_c est régulière. On a donc |G_c| ≤ B₄ sur ce rectangle, avec B₄ absolue. Sur la droite, |s| ≥ ½ et |s − 1| ≥ 1 − σ₀ ≥ (1 − θ)/2. Cette partie de l'intégrale est ≤ 24 B₄/(1 − θ).

Ainsi ∫ |F(σ₀ + it)| dt ≤ B₃/a + 24B₄/(1 − θ).

**(e) Segments horizontaux.** Soit T ≥ 3, j = ⌊T⌋, et s = σ + iT.
- Pour σ ∈ [σ₀, 7/4], on applique le découpage de (c) au bloc [j, j + 1]. Le disque de Cauchy de rayon ¼ autour de s reste dans R_j. On a |s − ρ| ≥ σ − β ≥ a pour tout zéro, donc |q| ≤ B₂ log T + N_j/a et |q′| ≤ 4B₂ log T + N_j/a², avec N_j ≪ log T.
- Pour σ ∈ [7/4, 2], |q(s)| ≤ Σ Λ(n) n^(−7/4) et |q′(s)| ≤ Σ Λ(n) log n · n^(−7/4) sont bornés.

Donc |G_c(σ + iT)| ≪ log²T/a² sur tout le segment. Le segment contribue au plus y² log²T/(a²T²), qui tend vers 0 quand T → ∞.

**(f) Conclusion.** Pour y ≥ y₀(θ) = exp(4/(1 − θ)), on prend a = 1/log y ≤ (1 − θ)/4. Alors y^(σ₀) = e·y^θ, et

  |H(y)| ≤ (e/2π) · y^θ · ( B₃ log y + 24B₄/(1 − θ) ).

C'est (iii), avec A = (e/2π)·max(B₃, 24B₄). ∎

*Remarques.*
1. Le seul ingrédient sur les zéros est leur comptage local (F1), qui est classique. Les zéros proches les uns des autres, qui empêchaient de sommer les résidus c₁(ρ) dans TAC-022, ne gênent plus : on ne somme aucun résidu, on intègre sur une droite située à distance a de tous les zéros.
2. La constante ne dépend de θ que par le terme 1/(1 − θ) et le seuil y₀(θ). Le facteur log y vient de 1/a, c'est-à-dire de l'intégrale ∫ dt/|s − ρ|² le long de la droite.
3. Le contrôle numérique de TAC-022, rejoué sans changement, donne max |H(y)|/(√y log y) = 0,0938 sur [10, 10⁶], atteint en y = 10. C'est compatible avec le corollaire 2 sous RH. Ce n'est pas une preuve : la mesure ne dit rien de l'asymptotique.

## Ce que la preuve utilise

- Sens direct : les mêmes ingrédients que T17, plus le développement près d'un pôle double, et le fait classique que ζ < 0 sur ]0, 1[ pour le point (ii) seulement.
- Réciproque : la formule de Perron pour le noyau 1/(s(s − 1)), le comptage local des zéros (F1), la formule locale de ζ′/ζ (F2), les inégalités de Cauchy et de Cauchy–Schwarz, et l'absence de zéros de hauteur < 14.

**Elle n'utilise pas** : de densité de zéros, d'hypothèse sur l'espacement des zéros, ni de borne de ζ′/ζ du type (log t)^A à l'intérieur de la bande critique au-delà de (F2).
