# Theorem A — referee-ready dossier

*Programme RH, version 6.13. Relecture dated 2026-10-10. Author: Vincent P. P. NOËL. Scope: Theorem A only. Theorem B and the "Archipel d'Euler" note are reviewed separately.*

**Status.** Theorem A is an exact reformulation of the position of the rightmost zero of ζ. It is not a step toward the Riemann Hypothesis (RH), and it is not claimed as new. We ask a specialist to check that it is correct and to point us to the literature.

**Pre-review verdict.** We re-derived both directions of the proof step by step and found no mathematical error. Three points of wording and the exact references needed fixing; all are fixed below. In substance, the result is a routine second-order analogue of the classical characterisation of Θ through ψ(x) − x (see §8).

## 1. Setting and notation

- ζ is the Riemann zeta function.
- ρ = β + iγ runs over the nontrivial zeros, each counted with its multiplicity m(ρ).
- Θ = sup β.
- γ_E is Euler's constant.
- We write s = σ + it.

For Re s > 1, put

- q(s) = −ζ′(s)/ζ(s) = Σ_{n≥1} Λ(n) n^{−s},
- c(n) = (Λ∗Λ)(n) − Λ(n) log n + 2γ_E Λ(n),
- G(s) = Σ_{n≥1} c(n) n^{−s},
- C(x) = Σ_{n≤x} c(n),
- Q(X) = ∫_1^X |C(x)|² x^{−2} dx for X ≥ 1.

**Basic facts about Q.** We have c(1) = 0 and c(2) = log 2 · (2γ_E − log 2) ≈ 0.320 ≠ 0. Hence C vanishes on [1, 2), Q(X) = 0 for X ≤ 2 and Q(X) > 0 for X > 2. Q is continuous and non-decreasing.

**Implied constants.** Implied constants may depend on ε and on ζ (through Θ and the position of the zeros). They never depend on x, X or t.

## 2. Statement

**Theorem A.** Let λ := ½ · limsup_{X→∞} log(1 + Q(X)) / log X. Then

  λ = Θ − ½.

**Consequences.**

- RH ⇔ Q(X) = X^{o(1)}.
- For 0 ≤ δ ≤ ½: Q(X) ≪_ε X^{2δ+ε} for every ε > 0 ⇔ Θ ≤ ½ + δ.

The proof also gives two equivalent forms (proved in §5):

- **(A₀, pointwise form)** limsup_{x→∞} log|C(x)| / log x = Θ.
- **(A′, abscissa form)** ∫_1^∞ |C(x)|² x^{−2σ−1} dx converges for σ > Θ and diverges for σ < Θ.

## 3. Ingredients

**Lemmas of the corpus** (LEMMES_RIGOUREUX.md: L1, L3, L4, L5). The proofs are short, so we reproduce them.

**L1 (generating series).** For Re s > 1, G = q² + q′ + 2γ_E q.

*Proof.* q² corresponds to Λ∗Λ, and q′ = −Σ Λ(n) log n · n^{−s}.

*Consequence.* G extends to a meromorphic function on ℂ. Its only possible poles are the zeros of ζ and the point s = 1.

**L3 (support of c).**

- c(p^k) = −log²p + 2γ_E log p.
- c(p^a r^b) = 2 log p log r for distinct primes p ≠ r.
- c(n) = 0 if n has at least three distinct prime factors.

*Consequences.*

- |c(n)| ≪ log² n.
- Σ |c(n)| n^{−σ} ≤ q(σ)² + |q′(σ)| + 2γ_E q(σ) ≪ (σ − 1)^{−2} as σ → 1+. This bound is the one needed for Perron's formula (F2).

**L4 (regularity at s = 1).** We have q = (s−1)^{−1} − γ_E + O(s−1). Hence:

- q² = (s−1)^{−2} − 2γ_E (s−1)^{−1} + O(1),
- q′ = −(s−1)^{−2} + O(1),
- 2γ_E q = 2γ_E (s−1)^{−1} + O(1).

The polar parts cancel, so G is holomorphic at s = 1. (Its value G(1) = 2γ_E² + 6γ₁ is not used here.)

**L5 (poles at the zeros).** Let ρ be a nontrivial zero of multiplicity m. Then q = −m/(s−ρ) + q₀ + O(s−ρ), and

  G(s) = m(m+1)/(s−ρ)² + O(|s−ρ|^{−1}).

Since m(m+1) ≥ 2, G has a genuine pole at every nontrivial zero. The other singular points behave as follows:

- each trivial zero −2k is a double pole with leading coefficient 2;
- G is regular at s = 0, because ζ(0) = −½ ≠ 0;
- s = 1 is removable, by L4.

**M (Mellin identity).** For Re s > 1,

  G(s)/s = ∫_1^∞ C(x) x^{−s−1} dx.

*Proof.* Partial summation gives Σ_{n≤X} c(n) n^{−s} = C(X) X^{−s} + s ∫_1^X C(x) x^{−s−1} dx. Since C(X) ≪ X log² X, the boundary term tends to 0.

**Classical inputs.**

- **F0.** ½ ≤ Θ ≤ 1. There are no zeros in Re s > 1, because of the Euler product. Also, ρ₁ = ½ + 14.1347…i is a zero.
- **F1.** Titchmarsh, *The Theory of the Riemann Zeta-Function*, Thm 9.6(A) and Thm 9.2; also Davenport, *Multiplicative Number Theory*, Ch. 15. Uniformly for −1 ≤ σ ≤ 2 and |t| ≥ 2:
  - ζ′/ζ(s) = Σ_{|γ−t|<1} 1/(s−ρ) + O(log|t|);
  - #{ρ : |γ − t| < 1} ≪ log|t|, counting multiplicity.
- **F2. Truncated Perron formula.** Titchmarsh, Lemma 3.12; also Montgomery–Vaughan, Cor. 5.3.
  - *Hypotheses.* F(s) = Σ a_n n^{−s}, with a_n = O(A(n)) for some non-decreasing A, and Σ |a_n| n^{−σ} ≪ (σ−1)^{−α} as σ → 1+.
  - *Conclusion.* For b > 1, T ≥ 2, and x > 1 not an integer, with N the integer nearest to x:
    Σ_{n<x} a_n = (1/2πi) ∫_{b−iT}^{b+iT} F(s) x^s s^{−1} ds + O(x^b / (T (b−1)^α)) + O(A(2x) x log x / T) + O(A(N) x / (T |x − N|)).
  - The numbering in both books is quoted from memory and should be checked.
- **F3.** The identity theorem, and the fact that an integral depending on a parameter is holomorphic when it is dominated locally uniformly.

## 4. Proof

**Step 1 — Lower bound: energy forces a zero-free half-plane, so Θ − ½ ≤ λ.**

*Range of λ.* Since Q ≥ 0, we have λ ≥ 0. By L3, |C(x)| ≤ Σ_{n≤x} |c(n)| ≪ x log² x, so Q(X) ≪ X log⁴ X and λ ≤ ½. If λ = ½, the claim follows from F0.

*Setup.* Assume λ < ½ and fix a ∈ (λ, ½). Then 1 + Q(X) ≤ X^{2a} for X ≥ X₀. Since Q is non-decreasing, Q(X) ≤ K X^{2a} for all X ≥ 1, with K = max(1, Q(X₀)).

*Dyadic bound.* For k ≥ 0, Cauchy–Schwarz gives

  ∫_{2^k}^{2^{k+1}} |C(x)| x^{−σ−1} dx ≤ (∫_{2^k}^{2^{k+1}} |C(x)|² x^{−2} dx)^{1/2} · (∫_{2^k}^{2^{k+1}} x^{−2σ} dx)^{1/2} ≪ Q(2^{k+1})^{1/2} · 2^{k(1−2σ)/2} ≪ 2^{k(a + ½ − σ)}.

*Holomorphy of F.* Summing over k, the integral ∫_1^∞ |C(x)| x^{−σ−1} dx converges for σ > ½ + a, uniformly on every half-plane Re s ≥ σ₁ > ½ + a. Hence, by F3, F(s) := ∫_1^∞ C(x) x^{−s−1} dx is holomorphic on H = {Re s > ½ + a}. By M, F = G/s on Re s > 1.

*Contradiction at a zero.* Let P be the set of poles of G/s in H. P is discrete and closed in H, so U = H ∖ P is open and connected. F − G/s is holomorphic on U and vanishes on Re s > 1, hence on all of U.

Suppose some nontrivial zero ρ lay in H. On a punctured disc around ρ, G/s = F, and F is bounded there. But by L5, G(s)/s = m(m+1) ρ^{−1} (s−ρ)^{−2} + O(|s−ρ|^{−1}) with ρ ≠ 0, which is unbounded. This is a contradiction.

*Conclusion.* So Θ ≤ ½ + a. Letting a ↓ λ gives Θ − ½ ≤ λ.

**Step 2 — Upper bound: a zero-free half-plane bounds C, so λ ≤ Θ − ½.**

**Case Θ = 1.** The bound Q(X) ≪ X log⁴ X gives λ ≤ ½ = Θ − ½.

**Case Θ < 1.** Fix 0 < ε < 1 − Θ. Put σ₀ = Θ + ε/2 < 1 and σ₁ = Θ + ε/4.

**(a) Growth of G.**

- *Bound on q.* For σ₁ ≤ σ ≤ 2 and |t| ≥ 2, every zero satisfies σ − β ≥ ε/4. By F1, |q(s)| ≤ (4/ε) · #{ρ : |γ − t| < 1} + O(log|t|) ≪_ε log|t|. For σ ≥ 2, |q(s)| ≤ q(2) < 1. So q ≪_ε log|t| on {Re w ≥ σ₁, |Im w| ≥ 2}.
- *Bound on q′ and G.* For σ ≥ σ₀ and |t| ≥ 3, the circle |w − s| = ε/4 lies inside that region. Cauchy's formula gives q′(s) ≪_ε log|t|. Hence G = q² + q′ + 2γ_E q ≪_ε log²|t| on {σ ≥ σ₀, |t| ≥ 3}.
- *Compact part.* On K = {σ₀ ≤ σ ≤ 2, |t| ≤ 3}, G is holomorphic: no zero has β ≥ σ₀, and s = 1 is removable by L4. So |G| ≤ M_ε on K.

**(b) Perron's formula.**

- *Choice of parameters.* Take x = N + ½ with N ≥ 3, b = 1 + 1/log x, and T = x⁴ (any T ≥ x² would do).
- *Hypotheses of F2.* By L3, F2 applies to a_n = c(n) with A(n) = K′ log²(n+2) and α = 2.
- *The three error terms.*
  - x^b / (T (b−1)²) = e x log² x / T.
  - A(2x) x log x / T ≪ x log³ x / T.
  - A(N) x / (T |x − N|) ≪ x log² x / T, since |x − N| = ½.
- *Result.* C(x) = (1/2πi) ∫_{b−iT}^{b+iT} G(s) x^s s^{−1} ds + O(log³ x / x³).

**(c) Shifting the contour.**

- *No pole is crossed.* G(s) x^s / s is holomorphic on a neighbourhood of the closed rectangle with vertices b ± iT and σ₀ ± iT:
  - nontrivial zeros have β ≤ Θ < σ₀;
  - s = 1 is removable (L4);
  - s = 0 and the trivial zeros lie in Re s ≤ 0.
- *Left side.* Its contribution is at most x^{σ₀} ∫_{−T}^{T} |G(σ₀ + it)| / |σ₀ + it| dt ≪_ε x^{σ₀} (M_ε + ∫_3^T log² t dt / t) ≪_ε x^{σ₀} log³ x.
- *Horizontal sides.* Their contribution is at most ∫_{σ₀}^{b} |G(σ ± iT)| x^σ T^{−1} dσ ≪_ε x^b log² T / T ≪ log² x / x³.
- *Result.* C(N + ½) ≪_ε x^{Θ+ε/2} log³ x ≪_ε (N + ½)^{Θ+ε}.

**(d) All real x.** C is constant on [N, N + 1), so C(x) = C(N + ½) there. Hence |C(x)| ≪_ε x^{Θ+ε} for all x ≥ 1. For x < 4, C is bounded.

**(e) Energy.** Since 2(Θ + ε) − 2 > −1 (by F0), we get Q(X) ≪_ε ∫_1^X x^{2Θ+2ε−2} dx ≪_ε X^{2Θ−1+2ε}. So λ ≤ Θ − ½ + ε for every ε > 0, that is, λ ≤ Θ − ½.

Steps 1 and 2 together prove Theorem A. ∎

**Corollaries.**

1. *RH.* RH ⇔ λ = 0 ⇔ Q(X) = X^{o(1)}. The ratio log(1+Q)/log X is non-negative, so "limsup = 0" already means "lim = 0".
2. *The δ-statement.* (⇐) Step 2 gives Q ≪ X^{2Θ−1+2ε} ≤ X^{2δ+2ε}. (⇒) λ ≤ δ, then apply Step 1.
3. *GAP-1.* A bound Q(X) ≪ X^{1−δ} with δ > 0 fixed would give Θ ≤ 1 − δ/2. This is an open problem.

## 5. Equivalent forms and remarks

**A₀ — the pointwise form: limsup_{x→∞} log|C(x)| / log x = Θ.**

- (≤) This is Step 2(d).
- (≥) Suppose |C(x)| ≤ K x^α for some α < Θ. Then the integral in M converges absolutely on Re s > α, so G/s continues holomorphically to that half-plane. But some zero has β > α. This is the same contradiction as in Step 1.

*What this shows.* At the level of exponents, the mean square carries exactly the same information as the pointwise bound. The two differ only on the logarithmic scale, which is where Theorem B lives. A₀ is the exact analogue, for c, of the classical characterisation of Θ through ψ(x) − x.

**A′ — the abscissa form.**

- For σ > Θ, convergence follows from Step 2(d).
- For σ < Θ, suppose the integral converges. Then for every σ′ > σ, Cauchy–Schwarz gives ∫ |C| x^{−σ′−1} dx ≤ (∫ |C|² x^{−2σ−1} dx)^{1/2} (∫ x^{2σ−2σ′−1} dx)^{1/2} < ∞. So F is holomorphic on Re s > σ, and we get the contradiction of Step 1.

*Corpus statement confirmed.* This confirms the claim "abscissa = Θ" made in GAP-DIM (KNOWN_GAPS.md).

*Side remark, not used.* The integrand is non-negative. By Landau's lemma (Montgomery–Vaughan, Lemma 15.1), Z_E(s) = ∫_1^∞ |C(x)|² x^{−1−2s} dx is therefore not analytic at the real point s = Θ.

**Plancherel — not used in Theorem A.**

- *Setting.* Fix σ > Θ. By Step 2(d), h(u) = C(e^u) e^{−σu} (u ≥ 0) lies in L¹ ∩ L²(ℝ).
- *Transform.* Its Fourier transform is ĥ(t) = ∫_1^∞ C(x) x^{−σ−it−1} dx = G(σ+it)/(σ+it). This uses F = G/s on Re s > Θ, which holds by the identity theorem.
- *Identity.* Hence ∫_1^∞ |C(x)|² x^{−2σ−1} dx = (1/2π) ∫_ℝ |G(σ+it)|² / |σ+it|² dt.
- *Where it is used.* Theorem B uses this identity at σ = ½ + η, under RH. Theorem A needs only absolute convergence (Cauchy–Schwarz), not Plancherel.

**Role of the double pole.**

- *What A uses.* Theorem A uses only that the polar part of G at each zero is non-zero. The order of the pole (2) plays no role in A; it matters only for Theorem B.
- *Why the sign of q′ matters.* The sign in q² + q′ is what guarantees a pole without any extra hypothesis. The other sign gives q² − q′ = ζ″/ζ, the Dirichlet series of Λ₂ = Λ·log + Λ∗Λ. Its leading coefficient is m(m−1), which vanishes at simple zeros. What remains there is a simple pole with residue ζ″(ρ)/ζ′(ρ).
- *Consequence.* For the analogous energy built on Λ₂, Step 1 would need ζ″(ρ) ≠ 0 at every simple zero, which is not known.

**limsup versus lim.**

- Theorem A says nothing about the liminf.
- For Θ = ½, the limit exists and equals 0.
- For Θ > ½, proving that lim log Q(X)/log X = 2Θ − 1 would require a lower bound for Q on every long interval (a localised Ω-theorem of Turán–Pintz type). This is neither claimed nor needed for RH ⇔ Q = X^{o(1)}.

**Finite X.**

- Under RH, Theorem B gives log(1+Q)/log X ≈ 3 log log X / log X. This is still about 0.32 at X = 10⁷ (see §10).
- So an exponent measured over accessible ranges says nothing about Θ. Theorem A is purely asymptotic.

**Effectivity.** The constants in Step 2 depend on ε and on M_ε, so the theorem is ineffective. No explicit X₀ is claimed.

## 6. Checkpoints

Verdicts: **C** = correct, **G** = gap that can be filled (with the fix stated), **E** = error. "Not new" in A20 is a verdict on priority, not on correctness.

| # | Where | Point checked | Verdict | Comment |
|---|---|---|---|---|
| A1 | L1 | G = q² + q′ + 2γ_E q; meromorphic continuation | C | Formal identity for Re s > 1. |
| A2 | L3 | Support of c; \|c(n)\| ≪ log² n; Σ\|c(n)\|n^{−σ} ≪ (σ−1)^{−2} | C | Checked numerically for n ≤ 2·10⁴ (largest deviation 7·10⁻¹⁵). The (σ−1)^{−2} bound, needed for F2, is now written out. |
| A3 | L4 | G regular at s = 1 | C | Laurent expansion. Numerically, G(1 + 10⁻⁶) = 0.2294606, against 2γ_E² + 6γ₁ = 0.2294608. |
| A4 | L5 | Non-zero polar part m(m+1)/(s−ρ)² at every zero | C | Numerically, h²G(ρ₁ + h) → 2. Theorem A uses only that it is non-zero. |
| A5 | M | Mellin identity on Re s > 1 | C | The boundary term C(X)X^{−s} tends to 0. |
| A6 | F0, conventions | ½ ≤ Θ ≤ 1; log(1+Q); Q > 0 for X > 2 | C | c(2) ≈ 0.320 ≠ 0. The "+1" changes no exponent. |
| A7 | Step 1 | Dyadic Cauchy–Schwarz; holomorphy of F on Re s > ½ + a | C | Locally uniform domination. |
| A8 | Step 1 | Identity theorem and contradiction at a zero | C (dossier v4.5) / G (LEMMES v3) | LEMMES L6.2 only says "par L5". Replace with the wording of §4 (H ∖ P is connected; F is bounded near ρ). |
| A9 | Step 2(a) | q, q′ ≪ log\|t\| and G ≪ log²\|t\| on σ ≥ Θ + ε/2 | C, minor G | The Cauchy circle leaves σ ≥ σ₀. Fix: state the F1 bound on σ ≥ Θ + ε/4, and use \|q\| ≤ q(2) for σ ≥ 2. LEMMES (6.3)–(6.4) are stated for σ ≥ Θ + ε but used at Θ + ε/2, a harmless slip in the ε bookkeeping. LEMMES gives q′ ≪ log², which is weaker but enough. |
| A10 | Step 2(a) | Compact part \|t\| ≤ 3, including s = 1 | C | G is holomorphic on a closed set, giving the constant M_ε. The v4.5 dossier states this; LEMMES does not. |
| A11 | Step 2(b) | Truncated Perron at x = N + ½ | C; G (reference) | The hypotheses of Titchmarsh L. 3.12 hold with A(n) = K′log²(n+2) and α = 2. The error is O(x log³x / T). The "+ log² x" term in v4.5 is unnecessary but harmless. Give the exact reference. |
| A12 | Step 2(c) | No pole is crossed | C | Nontrivial zeros have β ≤ Θ < σ₀. s = 1 is removable. s = 0 and −2k lie to the left. |
| A13 | Step 2(c) | Bounds on the sides of the rectangle | C | x^{σ₀} log³x for the left side; log²x / x³ for the horizontal sides. |
| A14 | Step 2(d)–(e) | From half-integers to all x; integration to Q | C | Needs Θ + ε > ½, which holds automatically. |
| A15 | Edge cases | Θ = 1 and Θ = ½ | C | Θ = 1: the trivial bound suffices. Θ = ½: λ ≥ 0 holds trivially. |
| A16 | Statement | limsup versus lim | C (as stated) | The limit is not claimed. For Θ > ½ its existence would need localised Ω-results. |
| A17 | Statement | Multiplicities | C | m(m+1) ≥ 2, and F1 counts zeros with multiplicity. |
| A18 | Plancherel | Identity on σ > Θ | C; not used in A | It is used by Theorem B. |
| A19 | Corpus | Consistency between SYNTHESIS §3, LEMMES L6 and dossier v4.5 | Editorial | T = x² vs x⁴, Θ + ε vs Θ + ε/2, 2ε vs 3ε: all valid, but they should be harmonised. |
| A20 | Priority | Prior statement in the literature | Not new in substance | The pointwise first-order analogue is in textbooks (Montgomery–Vaughan, Ch. 13 and 15). Under RH, C(x) ≪ x^{½} log⁵ x follows from Banks–Sinha Thm 1.1 (k = 2, y = 0) plus classical bounds. No verbatim prior statement was found. |

**No checkpoint receives verdict E.**

## 7. Questions for the external reviewer

1. **Correctness of Step 2.** Is the upper-bound argument complete as written? It uses truncated Perron at half-integers with T = x⁴, then a contour shift to σ₀ = Θ + ε/2 with G ≪ log²|t| derived from Titchmarsh 9.6(A) and Cauchy's formula. We are especially unsure about two points: the uniform bound near s = 1 and for small |t|, and the hypotheses of the Perron lemma for c(n) ≪ log² n.
2. **Priority.** Would you regard Theorem A as a routine consequence of the classical characterisation of Θ by ψ(x) − x (Montgomery–Vaughan, Ex. 13.1.1, the converse on p. 463, Thm 15.2)? This covers both the mean-square form and the pointwise form A₀. Do you know a reference that states it for Λ∗Λ − Λ·log + 2γ_EΛ, or for a general Dirichlet series with a pole at every zero, so that we can cite it rather than present it?
3. **Formulation.** Is the limsup formulation the right one to publish, or would you prefer the abscissa form A′? Should one expect, and state, lim log Q(X)/log X = 2Θ − 1, which would need a localised Ω-theorem?

## 8. Literature positioning

| Reference | Content relevant to A | Relation to A | Checked |
|---|---|---|---|
| H. L. Montgomery, R. C. Vaughan, *Multiplicative Number Theory I*, CUP 2007, Ch. 13 and 15. Ch. 15 PDF: https://personal.science.psu.edu/rcv4/personal/Publications/MNTI/19.0_pp_463_485_Oscillations_of_error_terms.pdf | Ex. 13.1.1: ψ(x) = x + O(x^Θ log² x). p. 463: ψ(x) = x + O(x^{α+ε}) implies no zero with β > α. Lemma 15.1 (Landau). Thm 15.2: ψ(x) − x = Ω±(x^{Θ−ε}). | The first-order, pointwise analogue of A₀. Both of our steps follow the same scheme. | Ch. 15 read through text extraction (some symbols lost). Ex. 13.1.1 is known only as quoted on p. 463. |
| Y.-T. Siu, lecture notes, Harvard Math 213b (2005): https://legacy-www.math.harvard.edu/archive/213b_spring_05/zero_strip_and_growth_error.pdf | Zero-free strip ⇒ error x^θ log² x; error x^α ⇒ zeros in the strip of half-width α. | The same two directions, for ψ. | Page read. |
| H. Cramér, "Ein Mittelwertsatz in der Primzahltheorie", Math. Z. 12 (1922), 147–153 | Mean square of ψ(x) − x under RH. | The mean-square tradition. More relevant to Theorem B. | **Not read.** Citation taken from Brent–Platt–Trudgian. |
| R. P. Brent, D. J. Platt, T. S. Trudgian, "The mean square of the error term in the prime number theorem", J. Number Theory 238 (2022), 740–762. arXiv:2008.06140: https://arxiv.org/abs/2008.06140 | Under RH, limsup I(X)/X² ≤ 0.8603, where I(X) = ∫_X^{2X} (ψ(x) − x)² dx. Unconditionally, I(X)/X² ≥ 1/5374 for X large, and I(X)/X² has no limit. Cites Montgomery–Vaughan Thm 13.6 and Ex. 13.1.1.3 for ∫(ψ−x)² x^{−2} dx ~ c log X under RH. | Context only. **Correction to v4.5**: the c·log X statement is Cramér / Montgomery–Vaughan Thm 13.6, not Brent–Platt–Trudgian. | Abstract and introduction read (final PDF on the ANU site). Thm 13.6 is known only as reported by them. |
| S. M. Gonek, S. W. Graham, Y. Lee, "The Lindelöf hypothesis for primes is equivalent to the Riemann hypothesis", Proc. Amer. Math. Soc. 148 (2020), 2863–2875. https://doi.org/10.1090/proc/14974 | RH ⇔ a uniform bound for twisted sums Σ Λ(n) n^{−it}. | An RH equivalence through sums over primes. | Abstract read. |
| W. D. Banks, S. Sinha, "The Riemann Hypothesis via the generalized von Mangoldt function", arXiv:2209.11768 (version dated 14 March 2023): https://arxiv.org/abs/2209.11768 | Thm 1.1/1.2: RH ⇔ an asymptotic for Σ_{n≤x} Λ^{∗k}(n) n^{−iy} with error O(x^{½}(x+\|y\|)^ε). Thm 1.3/1.4: the same for Λ_k = μ∗log^k. For k = 2 and y = 0, Thm 1.1 gives under RH: Σ_{n≤x} (Λ∗Λ)(n) = x(log x − 2γ_E) − x + O(x^{½} log⁵ x). | The direction RH ⇒ Q = X^{o(1)} follows from this, plus the classical bounds for Σ Λ(n) log n and ψ. The paper has no mean squares and does not use the combination Λ∗Λ − Λ·log. | arXiv PDF read through automated extraction. **Journal publication not found.** |

**Position.**

- *What is classical.* Theorem A is the mean-square version, for G = q² + q′ + 2γ_E q, of the classical characterisation of Θ through ψ(x) − x. Both directions use textbook methods.
- *What is specific.* Two things are specific to the corpus: the choice of c, which makes G regular at s = 1 so that no main term has to be subtracted; and the leading coefficient m(m+1) ≠ 0, which gives a pole at every zero with no extra hypothesis.
- *Search result.* Web searches found no source that states Theorem A verbatim. This does not establish novelty: no MathSciNet or zbMATH search was possible.
- *Recommendation.* Present A as a "proposition (standard method)", and ask the reviewer for a reference that can be cited.

## 9. Changes from the v4.5 dossier

- **Proof.** Unchanged in substance. Both directions were re-derived independently.
- **Ingredients.** Every lemma and classical input is now stated in §3, with its hypotheses. New items:
  - the bound Σ|c(n)|n^{−σ} ≪ (σ−1)^{−2}, which the Perron lemma requires;
  - the exact hypotheses of F2.
- **Step 2(a).**
  - The bound on q is now stated on σ ≥ Θ + ε/4, so that the Cauchy circle stays inside the region where it holds.
  - σ ≥ 2 is handled by |q| ≤ q(2).
  - The compact part |t| ≤ 3, including s = 1, is now treated explicitly.
- **Perron.** The error is now O(log³x / x³); the superfluous "+ log² x" term is gone.
- **New §5.**
  - The pointwise form A₀ and the abscissa form A′: the mean square adds nothing at the level of exponents.
  - Plancherel is not used in A.
  - Only the non-vanishing of the polar part matters for A, not its order. Built on ζ″/ζ instead, the same proof would need ζ″(ρ) ≠ 0.
  - The difference between limsup and lim.
  - A warning that finite-range numerics say nothing about Θ.
- **Checkpoints.** The four checkpoints of v4.5 on A (#1–#4) become twenty (A1–A20), with pre-review verdicts filled in.
- **Literature.**
  - The description of Brent–Platt–Trudgian is corrected.
  - Added: Montgomery–Vaughan Ch. 13 and 15 as the direct first-order analogue, and Banks–Sinha Thm 1.1 (k = 2) as the source of the direction RH ⇒ Q = X^{o(1)}.
  - The Gonek–Graham–Lee and Banks–Sinha references are checked; the journal status of Banks–Sinha is not.
- **Corrected in the corpus after this relecture (V6.13):** in LEMMES_RIGOUREUX, (6.3)–(6.4) were stated for σ ≥ Θ + ε but applied at Θ + ε/2; a corrective note now states them on σ ≥ Θ + ε/4. L6.2 remains terse.

## 10. Numerical sanity check

These checks only test the implementation. They are not evidence about Θ.

- Lemma 3 was compared with the direct definition for n ≤ 2·10⁴. The largest discrepancy is 7·10⁻¹⁵.
- G(1 + 10⁻⁶) = 0.2294606, against 2γ_E² + 6γ₁ = 0.2294608.
- h² G(ρ₁ + h) = 1.99998 − 1.6·10⁻⁶ i for h = 10⁻⁵.
- c(n) was computed directly as Λ∗Λ − Λ·log + 2γ_EΛ up to 10⁷. The table below gives the resulting values of Q.

| X | Q(X) | log(1+Q)/log X | Q / ((4κ/3) log³X) | max_{x≤X} \|C(x)\|/√x |
|---|---|---|---|---|
| 10³ | 8.94 | 0.332 | 0.440 | 4.68 |
| 10⁴ | 27.03 | 0.362 | 0.562 | 7.80 |
| 10⁵ | 60.49 | 0.358 | 0.644 | 13.01 |
| 10⁶ | 111.34 | 0.342 | 0.686 | 14.97 |
| 10⁷ | 186.74 | 0.325 | 0.724 | 17.47 |

*Reading the table.* The ratio log(1+Q)/log X is about 0.33 at X = 10⁷, whereas its limit under RH is 0. This is the slow 3 log log X / log X decay of §5.

## 11. Not verified

- The exact numbering of Titchmarsh Lemma 3.12, Thm 9.2 and Thm 9.6(A), and of Montgomery–Vaughan Cor. 5.3. All are quoted from memory.
- Montgomery–Vaughan Thm 13.6 and Ex. 13.1.1.3, known only as reported by Brent–Platt–Trudgian.
- Cramér (1922), which was not read.
- The journal status of Banks–Sinha.
- The search for prior statements, which was limited to web search.

*Contact: Vincent P. P. NOËL (address as in the covering message).*
