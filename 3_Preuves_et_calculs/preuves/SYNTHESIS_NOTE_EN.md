# A Mean-Square Energy Framework for the Riemann Hypothesis: What Is Proved, What Is Not, and Where the Approach Stops

*Synthesis note, programme `RH_programme` v3.9 (2026-10-03). Companion files and scripts are cited in §11.*

> **Status.** This note does **not** prove the Riemann Hypothesis (RH) and does not claim to be close to doing so. It records the
> results that survived scrutiny (several of them classical in method), the numerical calibrations, and the three tests that led us to
> stop the direct attack. It has not been refereed; the proofs of Theorems A and B should be read by a third party before any use.

## Abstract

We study the quadratic functional Q(X) = ∫₁^X |C(x)|² x⁻² dx, where C(x) = Σ_{n≤x} c(n) and c = Λ∗Λ − Λ·log + 2γΛ. Its Dirichlet series
G = ζ·(f″ + 2γf′) (f = 1/ζ) is regular at s = 1 and has a **double** pole m(m+1)/(s−ρ)² at every zero ρ of multiplicity m. We prove:
(A) unconditionally, Θ − ½ = ½·limsup log(1+Q(X))/log X, where Θ = sup Re ρ, so that RH ⇔ Q(X) = X^{o(1)};
(B) under RH, Q(X) ∼ (S/3)(log X)³ with S = Σ_ρ m²(m+1)²/|ρ|² (S = 4κ and Q ∼ (4κ/3)(log X)³ for simple zeros, κ = 2 + γ − log 4π);
(C) a **correction** to the natural expectation: the coefficient of L² (L = log X) in Q is not a constant but α + Φ(L) with Φ almost periodic.
We locate the framework inside the Nyman–Beurling–Báez-Duarte setting, reproduce numerically the constant κ as the expected limit of
d_N² log N, and report three calibration tests (Davenport–Heilbronn, function-field analogue, zero-density) which show that the framework
contains neither a Weil-type positivity nor any gain over known large-value technology. **A is equivalent to RH, so it cannot be a stepping stone by itself.**

---

## 1. Setting

Let Λ be the von Mangoldt function, γ Euler's constant, γ₁ the first Stieltjes constant (ζ(s) = 1/(s−1) + γ − γ₁(s−1) + …), f = 1/ζ and
q = −ζ′/ζ = ΣΛ(n)n⁻ˢ. Define

- c = Λ∗Λ − Λ·log + 2γΛ, a(n) = μ(n)(log²n − 2γ log n),
- G(s) = Σ c(n)n⁻ˢ, C(x) = Σ_{n≤x} c(n), Q(X) = ∫₁^X |C(x)|² x⁻² dx, U(L) = Q(e^L).

Zeros ρ = β + iγ are non-trivial zeros; Θ = sup{β}, so ½ ≤ Θ ≤ 1. κ = Σ_ρ 1/(ρ(1−ρ)) = 2 + γ − log 4π ≈ 0.046191 (an unconditional identity), which equals
Σ_ρ 1/|ρ|² under RH.

## 2. Exact identities (unconditional)

**Lemma 1 (generating series).** G = q² + q′ + 2γq = ζ·(f″ + 2γf′).
*Proof.* q² ↔ Λ∗Λ, q′ ↔ −Λ log; and f′ = fq, f″ = fq² + fq′. ∎

**Lemma 2 (factorisation).** c = 1∗a. *Proof.* f′ = −Σμ(n)log n·n⁻ˢ and f″ = Σμ(n)log²n·n⁻ˢ, so f″ + 2γf′ = Σa(n)n⁻ˢ; multiply by ζ. ∎

**Lemma 3 (support).** c(pᵏ) = −log²p + 2γ log p; c(pᵃqᵇ) = 2 log p log q for p ≠ q; c(n) = 0 if n has ≥ 3 distinct prime factors.
*Proof.* (Λ∗Λ)(pᵏ) = (k−1)log²p and Λ(pᵏ)log pᵏ = k log²p; for n = pᵃqᵇ, Λ(n) = 0 and Λ∗Λ counts the two orderings. ∎

**Lemma 4 (regularity at s = 1).** f(s) = ε − γε² + (γ² + γ₁)ε³ + …, ε = s−1. Hence f′(1) = 1, f″(1) = −2γ, f″ + 2γf′ vanishes at 1, G is holomorphic there, and G(1) = 2γ² + 6γ₁. In particular Σa(n)/n = 0 (conditionally convergent, equivalent in strength to the prime number theorem). ∎

**Lemma 5 (double poles).** At a zero ρ of multiplicity m, q = −m/(s−ρ) + q₀ + …, so G = m(m+1)/(s−ρ)² + b_ρ/(s−ρ) + …; for a simple zero b_ρ = 2c₀ − 2γ with c₀ = ζ″(ρ)/(2ζ′(ρ)). ∎

*Why this particular c.* The combination q² + q′ is the one with an exact double pole of weight m(m+1) (a first-order object, q alone, would give simple poles and a single power of L);
the term 2γq cancels the second-order pole of ζ at s = 1 so that G has no singularity there. Lemma 3 shows c lives on integers with at most two distinct prime factors.

## 3. The energy criterion (Theorem A, unconditional)

**Theorem A.** ½·limsup_{X→∞} log(1+Q(X))/log X = Θ − ½. In particular RH ⇔ Q(X) = X^{o(1)}.

*Proof.* For Re s > 1, G(s)/s = ∫₁^∞ C(x)x^{−s−1}dx.
(≥) Suppose limsup log(1+Q(X))/log X < 2a. By Cauchy–Schwarz on dyadic blocks, ∫|C|x^{−σ−1}dx < ∞ for σ > ½ + a. The integral is then holomorphic on Re s > ½ + a and equals G(s)/s
there by analytic continuation; but G has a double pole with non-zero coefficient m(m+1) at any zero in that half-plane. Hence Θ ≤ ½ + a.
(≤) By Perron's formula with T = x², and shifting the contour to Re s = Θ + ε using q(σ+it) = O_ε(log t) for σ ≥ Θ + ε (partial fractions), C(x) ≪ x^{Θ+ε}; hence Q(X) ≪ X^{2Θ−1+2ε}. ∎

This is the exact analogue, for G, of the classical equivalence ψ(x) = x + O(x^{½+ε}) ⇔ RH. **It is a reformulation**: any bound Q(X) = X^{o(1)} is a proof of RH, and the weaker
Q(X) ≪ X^{1−δ} would already give Θ < 1, which is open.

## 4. The leading term under RH (Theorem B)

**Theorem B.** Assume RH. Put A_ρ = m(m+1) and S = Σ_{ρ distinct} A_ρ²/|ρ|² < ∞. Then Q(X) ∼ (S/3)(log X)³. For simple zeros S = 4κ and Q(X) ∼ (4κ/3)(log X)³.

*Proof (six steps).* Classical facts used: (F1) ζ′/ζ(s) = Σ_{|t−γ|<1}1/(s−ρ) + O(log|t|) uniformly in −1 ≤ σ ≤ 2; (F2) the Hadamard expansion of (ζ′/ζ)′ (absolutely convergent Σ(s−ρ)⁻²,
error O(1/|s|)); (F3) N(T+1) − N(T) ≪ log T, hence m(ρ) ≪ log|γ|; (F4) Karamata's Tauberian theorem; (F5) Mellin–Plancherel.

1. *A priori.* Under RH, C(x) ≪ x^{½+ε}, so Q(X) ≪ X^{2ε}.
2. *Plancherel.* For σ = ½ + η, Q_η := ∫₁^∞|C|²x^{−2−2η}dx = (1/2π)∫_ℝ|G(σ+it)|²/|σ+it|² dt.
3. *Tail.* With W(t) = Σ_{|γ−t|<1}((t−γ)²+η²)⁻¹, one has |G| ≪ log t·W + log²t, ∫_T^{2T}W² dt ≪ T log²T·η⁻³, hence ∫_{|t|≥Y}|G|²/|s|² ≪ (log Y)⁴/(Y η³), uniformly in η.
4. *Local part.* For |t| ≤ Y only finitely many distinct zeros matter; near each, |A_ρ/(s−ρ)²|² integrates to A_ρ²π/(2η³), cross terms and remainders are O_Y(η⁻²).
5. *Limit.* Letting η → 0 then Y → ∞: η³Q_η → S/4.
6. *Tauber.* With λ = 2η, Q_η = ∫e^{−λL}dU(L) ∼ 2Sλ⁻³, so by (F4) U(L) ∼ 2S L³/Γ(4) = S L³/3. ∎

No simplicity hypothesis is needed. The theorem is the analogue, with a double pole, of Cramér's mean-square theorem for ψ(x) − x; **its value is exactness, not novelty**
(priority has not been checked against the literature). It gives no rate and no information on lower-order terms.

*Numerical illustration.* For X up to 4·10⁶ the measured Q(X) is 0.44–0.72 of (4κ/3)L³: convergence is slow because the L² and L terms are large (§5).

## 5. Lower-order structure: a correction (Proposition C)

Write A_γ = 2/ρ, u_γ = (b_ρ − 2/ρ)/ρ, s₃ = Σ_{γ>0}|A|²/3, s₂ = Σ_{γ>0}Re(Aū), s₁ = Σ_{γ>0}|u|². The explicit formula gives, for N zeros,
U(L) = 2(s₃L³ + s₂L² + s₁L) + L²Φ(L) + O(L), where

Φ(L) = 2 Re Σ_{γ≠γ′} A_γ Ā_γ′ e^{i(γ−γ′)L}/(i(γ−γ′)) + 2 Re Σ_{γ,γ′} A_γ A_γ′ e^{i(γ+γ′)L}/(i(γ+γ′)).

**Proposition C.** (i) (*Abelian level.*) The η-expansion of Q_η has coefficients κ/η³, s₂/η², s₁/η, computed locally and independently of the explicit formula; for a model with
300 zeros the numerical check gives 0.2327 versus s₁ = 0.2328 (and agreement at the other orders to four digits). (ii) (*Pointwise level.*) The coefficient of L² is α + Φ(L), α = 2s₂,
with Φ almost periodic and bounded under a hypothesis on close pairs of zeros; **α and β = 2s₁ are means, not pointwise constants**.

*Numerics.* With 300 zeros: α ≈ −0.264, β ≈ 0.466 (still drifting by about 4 % per hundred zeros); Φ ranges over [−0.032, +0.027]; the formula for Φ has correlation 0.996 with the measured deviation
of the explicit formula from its diagonal part. This explains why free fits of α, β to U(L) are unstable: the oscillation L²Φ (≈ 3–6 on U ≈ 100) is comparable to βL ≈ 7.

*Hypotheses for ζ itself* (not proved): (H1) RH and simple zeros; (H2) convergence of Σ|b_ρ|²/|ρ|², which follows from the Bettin–Conrey–Farmer moment condition Σ_{|γ|≤T}|ζ′(ρ)|⁻² ≪ T^{3/2−δ} together with Lindelöf;
(H3) control of pairs of zeros at distance ≲ η, which is beyond RH alone (it would follow from a GUE-type repulsion, not proved). The Gonek-type moment is numerically consistent: Σ|ζ′(ρ)|⁻² over 300 zeros is
0.976 × (6/π³)T at T ≈ 542, with effective exponent 0.915.

## 6. Relation with Nyman–Beurling

Let ρ_k(x) = {1/(kx)} and χ = 1_{(0,1)}. By Mellin transform, ‖χ + Σa_kρ_k‖²_{L²(0,∞)} = (1/2π)∫|1 − ζ(½+it)A(½+it)|² dt/(¼+t²), A = Σa_k k⁻ˢ; d_N² is the infimum over A supported on k ≤ N
(Báez-Duarte; this is the integral form used by Bettin–Conrey–Farmer). The Gram entries are G(a,b) = ∫₀^∞{y/a}{y/b}y⁻²dy and ⟨χ,ρ_a⟩ = (log a + 1 − γ)/a. They were computed exactly cell by cell with a
Richardson tail whose mean is ¼ + gcd(a,b)²/(12ab) (this uses the Franel–Landau formula ∫₀¹((ax))((bx))dx = gcd(a,b)²/(12ab), 1924).

*Validation.* G(1,1) = log 2π − γ to 10⁻¹⁴; ‖χ+ρ₁‖² = 3.1062 against 3.1078 from direct integration of ζ on the critical line (queue approximated); E(V₁₀) = 0.6715 against 0.6758; perturbing G by 10⁻¹⁰ changes d₁₀₀² by 10⁻¹⁰ (cond ≤ 3.7·10⁴).

| N | d_N² | d_N² · log N | ratio to κ |
|---|---|---|---|
| 10 | 0.02377 | 0.05474 | 1.185 |
| 30 | 0.01453 | 0.04942 | 1.070 |
| 50 | 0.01187 | 0.04643 | 1.005 |
| 80 | 0.01098 | 0.04813 | 1.042 |
| 100 | 0.01019 | 0.04692 | 1.016 |

For N = 40…100, d_N² log N lies within 0.5–4 % of κ but is **not monotone** (±2 % oscillations, of the order of the gap to κ). The Burnol lower bound (as reported by Bettin–Conrey–Farmer) is a liminf and cannot be read pointwise.
For the Bettin–Conrey–Farmer polynomial V_N, E(V_N)·log N decreases from 2.11 (N = 5) to 0.71 (N = 200), still ≈ 15 κ: its asymptotic regime is not visible at these sizes.

*Dictionary.* BCF work at first order, 1 − ζV_N ≈ −q/log N (exact identity on coefficients: [n=1] + Λ(n)/log N − Σ_{d|n, d>N}μ(d)(1 − log d/log N)); this programme at second order (G = q² + q′ + 2γq). Both diagonalise the
same sum Σ_ρ 1/|ρ|², hence the same constant κ; neither new constant nor new equivalence is claimed. The “terminal channel” formula
H_∞(q) = Σ_{q|d}a(d)/d = −(2μ(q)/φ(q))·Σ_{p|q} p log p/(p−1) follows from Σ_{q|d}μ(d)d⁻ˢ = μ(q)q⁻ˢ∏_{p|q}(1−p⁻ˢ)⁻¹/ζ(s) and Lemma 4: it is an elementary corollary of a standard identity.

## 7. What the numerics show — and do not show

| Check | Result | What it tests |
|---|---|---|
| Explicit formula, 300 zeros vs measured Q up to 4·10⁶ | within ≈5 %; correlation of B(t) 0.976 | coherence with the explicit formula |
| Local η-expansion model | 0.2327 vs 0.2328 | algebra of Prop. C |
| Localisation of zeros by windowed energy | 18/20 peaks within 0.5 of a zero | the observable resolves heights up to γ ≈ 100 |
| Signal/noise of zero lines | 55, 11.5, 3.3 for γ in 8–25, 25–45, 45–80 (∝ 1/γ²); noise floor Σ_{n≤3·10⁵}c(n)²/n = 6 691 | detector limits |
| Gonek-type moment | ratio 0.976 at T ≈ 542 | hypothesis (H2), consistent |

**None of these tests RH.** RH is known to hold up to height ≈ 3·10¹², so a counterexample would sit far beyond anything reachable at X ≲ 10⁷; the numerics check the internal coherence of the identities and the explicit formula.

## 8. Calibration tests and why the approach stops

**8.1 Davenport–Heilbronn (no Euler product).** f = ½(1−iκ_D)L(s,χ) + ½(1+iκ_D)L(s,χ̄), χ mod 5 with χ(2) = i, κ_D = (√(10−2√5) − 2)/(√5 − 1); the functional equation holds to 10⁻¹⁶. Running the same pipeline
(Λ_f from f·Λ_f = a·log, c_f = Λ_f∗Λ_f − Λ_f log) gives slopes of log Q/log X of 0.33 (ζ), 0.34 (L(s,χ₅)), **0.56 (DH)**. The DH zeros off the critical line found up to t = 200 (130 zeros by an argument-principle count; corrected 2026-10-07, the earlier list of 125 missed six) include 0.8085 + 85.699i and
0.7243 + 176.703i; the largest real part is 0.8085, predicting a slope 2σ−1 ≈ 0.62. Q therefore detects off-line zeros generically; the Euler product enters only through the sparsity of c (Lemma 3), which no argument has used.

**8.2 Function-field analogue.** Weil's proof uses (I) rationality of Z(T), (II) the tower of constant-field extensions (it suffices to prove the bound for a power of q), (III) the Hodge index theorem on C × C (Castelnuovo–Severi inequality), giving |N_r − q^r − 1| ≤ 2g·q^{r/2};
Stepanov–Bombieri also work on C × C. For Spec ℤ, Spec ℤ × Spec ℤ = Spec ℤ is one-dimensional (van Frankenhuijsen). In the framework: Q is the *square* of the explicit formula (quadratic in c), whereas Weil's positivity concerns the explicit formula applied to a square f∗f̃; Q's positivity is of Parseval type, automatic,
and its leading coefficient is Σ|f̂(ρ)|² rather than the signed f̂(ρ)·conj f̂(1−ρ̄) of Weil's criterion. A faithful finite-field analogue (elliptic curves over 𝔽₁₀₁, q_n = −s_n, c_n = (s∗s)_n + n s_n) gives Q_M/M³ ≈ 2.5–2.9 when |α| = √p
but 10⁵…10³⁴ when a = 25 (violating Hasse); over all 10 100 smooth curves y² = x³ + Ax + B on 𝔽₁₀₁, max|a| = 20 ≤ 2√101 = 20.1 and a = 25 never occurs. **Q is a thermometer, not a prohibition**: the bound comes from geometry, which the framework does not contain.

**8.3 Zero-density.** Three routes from Q all reduce to large values of Dirichlet polynomials with coefficients bounded by log²n: (A) Plancherel is valid only on lines σ′ > Θ (circular); (B) energy of a frequency window cannot be bounded below by a subset of zeros because nearby frequencies are not
orthogonal and the remaining zeros can cancel — density methods avoid this by evaluating *at* zeros, which leads to the Halász–Montgomery/Huxley/Guth–Maynard machinery; (C) the partial sums of G are, up to the range constraint pq ≤ X, the square of a prime polynomial.
The best known exponent is 30/13 (Guth–Maynard) against 2 for the density hypothesis; the framework offers no mechanism to improve it.

**Decision.** The stopping rule set in advance is triggered: tests 2 and 3 fail, test 1 does not distinguish the framework. We stop the direct attack on RH and keep the results of §§2–6 as calibration material.

## 9. Status summary

| Claim | Status |
|---|---|
| Lemmas 1–5 (identities, support, regularity, double poles) | proved; numerically checked |
| Theorem A (exponent ⇔ Θ; RH ⇔ Q = X^{o(1)}) | proved, **equivalent to RH** |
| Theorem B (Q ∼ (S/3)log³X under RH) | proof complete modulo F1–F5; not refereed; likely not novel (Cramér analogue) |
| Prop. C (η-expansion; Φ(L) structure) | local expansion proved/checked; passage to ζ conditional on (H1)–(H3) |
| NB dictionary, Gram numerics | validated; consistent with d_N² ∼ κ/log N, not a test of RH |
| Weil-type positivity in the framework | **absent** |
| Gain on zero-density | **none** |

## 10. Open items and verification flags

Not verified: the numerical RH verification height (≈3·10¹², quoted from memory); the exact link between Franel–Landau and the function A(λ) of Báez-Duarte–Balazard–Landreau–Saias (and Vasyunin's cotangent sums); priority for Theorem B; the statements of Weil's positivity criterion and of the Halász–Montgomery inequality (quoted from memory); L7 is claimed as no more than elementary.
Sources were read through abstracts or web pages on 2026-10-03, not in full, except Bettin–Conrey–Farmer (read in full). Not done: a third-party reading of Theorems A and B; the asymptotic regime of E(V_N); the dependence of the detector's signal-to-noise ratio on L.

## 11. Reproducibility

Package `RH_programme_v3_9_2026-10-03` (all numbers above): `docs/LEMMES_RIGOUREUX.md`, `docs/THEOREME_TERME_DOMINANT.md`, `docs/ALPHA_BETA_ANALYSE.md`, `docs/NB_GRAM.md`, `docs/COMPARAISON_BCF.md`, `docs/DAVENPORT_HEILBRONN_TEST.md`,
`docs/MEMO_P2_2_WEIL.md`, `docs/MEMO_P2_3_DENSITE.md`; scripts under `scripts/` (`run_v2.py`, `run_abelian_check.py`, `run_alpha_beta.py`, `run_nb_gram.py`, `run_nb_gram_ext.py`, `run_rejection.py`, `run_localisation.py`, `run_gonek_moment.py`, `run_function_field_analog.py`);
`python tests/test_identities.py` runs 21 tests (21/21 pass); `sha256sum -c CHECKSUMS.sha256` checks integrity.

## References

*Checked in full:* A. Bettin, B. Conrey, D. Farmer, “An optimal choice of Dirichlet polynomials for the Nyman–Beurling criterion”, Proc. Steklov Inst. 280 (2013), arXiv:1211.5191.
*Checked via abstract or page:* L. Báez-Duarte, Rend. Mat. Acc. Lincei 14 (2003) and Publ. Inst. Math. 78 (2005); L. Báez-Duarte, M. Balazard, B. Landreau, É. Saias, Ramanujan J. 9 (2005); B. Landreau, F. Richard, Exp. Math. 11 (2002);
M. Balazard, B. Martin, arXiv:1305.4395; J.-F. Burnol (lower bound for d_N², as reported in BCF); J. Franel, Göttingen Nachrichten (1924), 198–201, and E. Landau (1924) for ∫₀¹((ax))((bx))dx = (a,b)²/(12ab);
L. Guth, J. Maynard, “New large value estimates for Dirichlet polynomials”, Ann. of Math. 203 (2026), arXiv:2405.20552; M. van Frankenhuijsen, arXiv:0806.0044; R. Schoof, *The Riemann hypothesis for curves over finite fields* (notes, 2003);
K. Kedlaya, *Weil cohomology*, ch. 5 (notes); A. Weil (1942–48); E. Bombieri, S. A. Stepanov (1969–73).
*Classical background (from memory):* Titchmarsh, *The Theory of the Riemann Zeta-Function*, §9.6 (partial fractions), H. Cramér (1919–22) for the mean-square theorem on ψ(x) − x, J. Karamata (Tauberian theorem), Montgomery–Vaughan, Huxley, Ingham (zero-density).
