# Theorem B: referee-ready dossier

*A Cramér-type mean square for the double-pole series G = q² + q′ + 2γ_E·q, under RH*

Corpus `RH_programme_v6_13` (author: Vincent Noël). This internal check was prepared on 2026-10-10 to get the material ready for an external referee. It is not an independent peer review. **No claim toward the Riemann Hypothesis is made.** Theorem B is conditional on RH.

## 0. Summary

- **Object.** Theorem B, as stated in `3_Preuves_et_calculs/preuves/THEOREME_TERME_DOMINANT.md` (v3.4) and in §4 of the v4.5 referee dossier.
- **Verdict.** The proof is correct. I found no error. All remaining gaps are about presentation or citations and can be filled; they are listed in §7 and §11. **Ready to send after small fixes.**
- **Main structural point.** Close pairs of zeros cannot affect the leading term. The tail bound (Lemma T) is uniform in η. Interactions between different zeros are only needed at a fixed height Y while η ↓ 0, and Y → ∞ is taken afterwards. The corpus hypothesis (H3) on close pairs is therefore not used. The same order of limits is why the proof gives no rate.
- **Novelty.** The method is Cramér's: Mellin–Plancherel, local analysis, then a Tauberian theorem. About ten web searches found no earlier statement of Theorem B. A specialist will probably see it as a direct double-pole transposition of the classical result for ψ(x) − x (§9).

## 1. Setting and notation

- ρ = β + iγ runs over the non-trivial zeros of ζ, and m(ρ) is the multiplicity. Unless "distinct" is stated, N(T) and sums over ρ count zeros with multiplicity. γ_E is Euler's constant.
- For Re s > 1, q(s) = −ζ′/ζ(s) = Σ Λ(n) n^(−s).
- c(n) = (Λ∗Λ)(n) − Λ(n) log n + 2γ_E Λ(n). G(s) = Σ c(n) n^(−s). C(x) = Σ_{n≤x} c(n).
- Q(X) = ∫₁^X |C(x)|² x^(−2) dx. U(L) = Q(e^L). For η > 0, Q_η = ∫₁^∞ |C(x)|² x^(−2−2η) dx.
- A_ρ = m(ρ)(m(ρ)+1). S = Σ_{ρ distinct} A_ρ²/|ρ|², summed over γ > 0 and γ < 0. S_y is the same sum restricted to |γ| ≤ y.
- κ = 2 + γ_E − log 4π = 0.0461914179…
- Throughout, s = σ + it with σ = ½ + η.

## 2. Statement

**Theorem B.** Assume RH. Then S < ∞ and

  Q(X) ∼ (S/3)(log X)³  (X → ∞).

Equivalently, lim_{η↓0} η³ Q_η = S/4, and U(L) ∼ (S/3) L³. If all zeros are simple, then S = 4κ and Q(X) ∼ (4κ/3)(log X)³, where 4κ/3 = 0.0615885…

**Corollary B′ (new remark, to be checked).** Assume RH. Then S ≥ 4κ, with equality if and only if every zero is simple. Consequently, under RH, Q(X)/(log X)³ → 4κ/3 if and only if all zeros are simple.

## 3. Classical inputs

The section numbers below are from memory and should be checked against the books before submission.

- **F1** (partial fractions; Titchmarsh, *Theory of the Riemann Zeta-Function*, Thm 9.6(A)). Uniformly for −1 ≤ σ ≤ 2 and |t| ≥ 2:
  ζ′/ζ(s) = Σ_{|t−γ|<1} 1/(s−ρ) + O(log|t|).
- **F2** (Hadamard product; Davenport, *Multiplicative Number Theory*, Ch. 12). We have
  ζ′/ζ(s) = B − 1/(s−1) + ½ log π − ½ (Γ′/Γ)(s/2+1) + Σ_ρ (1/(s−ρ) + 1/ρ).
  Differentiating gives, for Re s ≥ ½ and |s−1| ≥ ½:
  q′(s) = Σ_ρ (s−ρ)^(−2) − (s−1)^(−2) + O(1/|s|),
  where the series converges absolutely.
- **F3** (Titchmarsh, Thm 9.2). N(T+1) − N(T) ≪ log T. Hence m(ρ) ≪ log(|γ|+2), and #{ρ : T < |γ| ≤ 2T} ≪ T log T.
- **F4** (Hardy–Littlewood–Karamata). Let U : [0,∞) → [0,∞) be non-decreasing and right-continuous with U(0) = 0. Assume that ℒU(λ) := ∫_{[0,∞)} e^(−λv) dU(v) is finite for every λ > 0 and that ℒU(λ) ∼ c λ^(−k) as λ ↓ 0, with c ≥ 0 and k ≥ 0. Then U(L) ∼ c L^k / Γ(k+1) as L → ∞. References: Widder, *The Laplace Transform* (1941), Ch. V, Thm 4.3; Feller, *An Introduction to Probability Theory*, Vol. II, XIII.5; Korevaar, *Tauberian Theory* (2004), Ch. I.
- **F5** (Plancherel, written multiplicatively). If h ∈ L¹ ∩ L²((0,∞), dx/x) and h̃(t) = ∫₀^∞ h(x) x^(−it) dx/x, then ∫ |h|² dx/x = (1/2π) ∫_ℝ |h̃(t)|² dt. This is Plancherel on ℝ after the substitution x = e^v.

## 4. Lemmas from the corpus used here

I recomputed each of these.

- **L1.** For Re s > 1, G = q² + q′ + 2γ_E q. Here q² ↔ Λ∗Λ and q′ ↔ −Λ·log.
- **L3.** |c(n)| ≪ log² n.
- **L4.** Near s = 1, q = 1/(s−1) − γ_E + O(s−1). So q² + q′ + 2γ_E q is holomorphic at s = 1.
- **L5.** At a zero ρ of multiplicity m, q = −m/(s−ρ) + q₀ + O(s−ρ). Hence
  G(s) = A_ρ/(s−ρ)² + b_ρ/(s−ρ) + O(1), with A_ρ = m(m+1) and b_ρ = −2m(q₀ + γ_E).
  For a simple zero, b_ρ = ζ″(ρ)/ζ′(ρ) − 2γ_E. Under RH, the poles of G in Re s > 0 are therefore exactly the non-trivial zeros. All of them lie on Re s = ½, and all are double poles.
- **L6.1 (Mellin identity).** For Re s > 1, G(s)/s = ∫₁^∞ C(x) x^(−s−1) dx. This follows by partial summation.
- **A-bound** (Theorem A, v4.5 dossier §3.3, case Θ = ½). Under RH, C(x) ≪_ε x^(1/2+ε) for every ε > 0. Theorem A is reviewed separately. Numerically, max |C(x)|/(√x log² x) = 0.148 on [10³, 10⁸].

## 5. Proof

### Step 1: a priori bound

By the A-bound, Q(X) ≪_ε X^(2ε). Hence Q_η < ∞ for every η > 0, and Q_η = 2η ∫₁^∞ Q(x) x^(−1−2η) dx.

### Step 2: Plancherel identity

Fix η ∈ (0, ¼]. Put σ = ½ + η and h(x) = C(x) x^(−σ) 1_{x≥1}. Then ‖h‖²_{L²(dx/x)} = Q_η.

Take 0 < η′ < η. Cauchy–Schwarz gives

  ∫₁^∞ |C(x)| x^(−σ−1) dx ≤ Q_{η′}^(1/2) (∫₁^∞ x^(−1−2(η−η′)) dx)^(1/2) < ∞,

so h ∈ L¹(dx/x).

The same estimate, with σ replaced by any σ′ > ½, shows that F(s) := ∫₁^∞ C(x) x^(−s−1) dx converges absolutely and locally uniformly on Re s > ½. So F is holomorphic there. By L6.1, F = G/s on Re s > 1. Under RH, G/s is holomorphic on Re s > ½ (L4, L5), so F = G/s on all of Re s > ½. Since h̃(t) = F(σ+it), F5 gives the exact identity

  **(2.1) Q_η = (1/2π) ∫_ℝ |G(σ+it)|² / |σ+it|² dt.**

### Step 3: pointwise bound and uniform tail

**Lemma P.** Assume RH. There is an absolute constant K such that, for 0 < η ≤ ½, σ = ½ + η and |t| ≥ 3,

  |G(σ+it)| ≤ K [ (log|t|)·W(t) + log²|t| ],  where W(t) = W_η(t) = Σ_{|γ−t|<1} 1/((t−γ)² + η²),

with the sum taken over zeros counted with multiplicity.

*Proof.*

1. Let Z(t) = #{ρ : |γ−t| < 1}. By F3, Z(t) ≪ log|t|.
2. Under RH, |s−ρ|² = η² + (t−γ)².
3. By F1 and Cauchy–Schwarz, |q(s)| ≤ Σ_{|γ−t|<1} |s−ρ|^(−1) + O(log|t|) ≤ (Z W)^(1/2) + O(log|t|).
4. By F2, |q′(s)| ≤ W + Σ_{|γ−t|≥1} (t−γ)^(−2) + O(1). Split the far zeros into unit windows at distance k ≥ 1. Each window contains ≪ log(|t|+k) zeros (F3), so the far sum is ≪ Σ_k log(|t|+k)/k² ≪ log|t|.
5. Then |G| ≤ |q|² + |q′| + 2γ_E|q|. Using √(ZW) ≤ 1 + ZW, this is ≤ (2Z + O(Z) + 1)·W + O(log²|t|), which is ≪ (log|t|)·W + log²|t|. ∎

**Lemma T (tail, uniform in η).** Assume RH. For Y ≥ 3 and 0 < η ≤ ½,

  ∫_{|t|≥Y} |G(σ+it)|² / |σ+it|² dt ≤ K′ (log Y)⁴ / (Y η³),

where K′ is absolute.

*Proof.*

1. Since G(s̄) is the complex conjugate of G(s), it is enough to treat t ≥ Y.
2. By Cauchy–Schwarz, W(t)² ≤ Z(t) Σ_{|γ−t|<1} ((t−γ)² + η²)^(−2).
3. Recall ∫_ℝ du/(u² + η²)² = π/(2η³). For T ≥ 3, step 2 and F3 give ∫_T^{2T} W² dt ≪ (log T)·#{ρ : T−1 < γ < 2T+1}·η^(−3) ≪ T (log T)² η^(−3).
4. By Lemma P, ∫_T^{2T} |G|² dt ≪ T (log T)⁴ η^(−3), using η ≤ ½.
5. On [T, 2T], |s|^(−2) ≤ T^(−2). Summing over T = 2^j Y gives the claim. ∎

*Remark.* All the constants are absolute, so the bound is uniform in η. Close pairs of zeros are absorbed by the Cauchy–Schwarz step in (2). That costs one factor Z ≪ log T and uses no information on the gaps between zeros.

### Step 4: local part

**Lemma Loc.** Assume RH and fix Y ≥ 3. As η ↓ 0,

  S_{Y−1}/4 − o_Y(1) ≤ (η³/2π) ∫_{|t|≤Y} |G(σ+it)|² / |σ+it|² dt ≤ S_{Y+2}/4 + o_Y(1).

*Proof.*

Set-up.

- Let ρ_1, …, ρ_J be the distinct zeros with |γ_k| ≤ Y+2. Write A_k = A_{ρ_k} and b_k = b_{ρ_k}.
- Let d_Y = min_{k≠j} |γ_k − γ_j|. This is positive because the set is finite.
- By L4, L5 and RH, R(s) := G(s) − Σ_k [A_k (s−ρ_k)^(−2) + b_k (s−ρ_k)^(−1)] is holomorphic on a neighbourhood of the compact rectangle K_Y = [½, ¾] × [−Y−1, Y+1]. So |R| ≤ M_Y on K_Y.
- For η ≤ ¼, the segment {σ+it : |t| ≤ Y} lies in K_Y.
- Write ⟨f, g⟩ = ∫_{|t|≤Y} f ḡ |s|^(−2) dt, and ‖·‖ for the associated norm. Put P_k = A_k (s−ρ_k)^(−2), P = Σ_k P_k and r = G − P. On the segment, |s|^(−2) ≤ 4.

(a) Diagonal terms.

- With u = t − γ_k, |P_k|² = A_k² / (u² + η²)².
- For |t| ≤ Y, the weight w(t) = |σ+it|^(−2) satisfies |w(t) − |ρ_k|^(−2)| ≤ c_Y (|u| + η). This is because |σ+it|² − |ρ_k|² = η + η² + 2γ_k u + u².
- Three integrals are needed:
  - η³ ∫_ℝ (u²+η²)^(−2) du = π/2;
  - η³ ∫_ℝ |u| (u²+η²)^(−2) du = η;
  - η³ ∫_{|u|>1} (u²+η²)^(−2) du ≤ η³.
- If |γ_k| ≤ Y−1, these give η³‖P_k‖² = (π/2) A_k²/|ρ_k|² + O_Y(η).
- If Y−1 < |γ_k| ≤ Y+2, they give 0 ≤ η³‖P_k‖² ≤ (π/2) A_k²/|ρ_k|² + O_Y(η).

(b) Off-diagonal terms. Take k ≠ j. For every t, one of |t−γ_k| and |t−γ_j| is at least d_Y/2. Therefore

  |⟨P_k, P_j⟩| ≤ 4 |A_k A_j| (4/d_Y²) ∫_ℝ du/(u²+η²) = O_Y(η^(−1)).

(c) Remainder.

- ‖r‖² ≤ (J+1) (Σ_k |b_k|² · 4π/η + 8(Y+1) M_Y²) = O_Y(η^(−1)).
- By (a) and (b), ‖P‖² = O_Y(η^(−3)). So |⟨P, r⟩| ≤ ‖P‖ ‖r‖ = O_Y(η^(−2)).

Conclusion. Combining (a)–(c), η³‖G‖² = η³ Σ_k ‖P_k‖² + O_Y(η). Divide by 2π and use (1/2π)(π/2) = 1/4. ∎

*Remark (where close pairs would enter).* Different zeros interact only in (b), and that bound depends on d_Y, the closest pair below height Y+2. Y is fixed while η ↓ 0, so this costs nothing in the limit. Making (b) uniform in Y is what the η^(−2) term of Proposition C needs, and it is exactly the corpus hypothesis (H3/H3⋆). Theorem B does not need it.

### Step 5: abelian limit

First, S < ∞:

- For T ≥ 2, A_ρ² = m²(m+1)² ≤ 4m⁴ ≤ 4m·(K log T)³.
- Σ_{distinct, T<|γ|≤2T} m ≪ T log T.
- So Σ_{T<|γ|≤2T} A_ρ²/|ρ|² ≪ T^(−2) · log³T · T log T = log⁴T / T, which is summable over T = 2^j.

Next, for every fixed Y ≥ 3, (2.1), Lemma T and Lemma Loc give

  S_{Y−1}/4 ≤ liminf_{η↓0} η³Q_η ≤ limsup_{η↓0} η³Q_η ≤ S_{Y+2}/4 + K′(log Y)⁴/(2πY).

Letting Y → ∞ gives **lim_{η↓0} η³ Q_η = S/4**.

### Step 6: Tauberian step

- U(L) = Q(e^L) = ∫₀^L |C(e^v)|² e^(−v) dv. It is continuous and non-decreasing, with U(0) = 0.
- The substitution x = e^v gives the exact identity Q_η = ∫₀^∞ e^(−2ηv) dU(v) = ℒU(2η). By Step 1 this is finite for every η > 0.
- Put λ = 2η. Step 5 then reads ℒU(λ) ∼ (S/4)(λ/2)^(−3) = 2S λ^(−3).
- F4 with k = 3 and c = 2S gives U(L) ∼ 2S L³/Γ(4) = (S/3) L³. ∎

So the Tauberian variable is L = log x, the transform variable is λ = 2η, and Karamata is applied to the monotone function U itself. It is not applied to a smoothed version of U.

### Value of S for simple zeros

1. If all zeros are simple, A_ρ = 2 and S = 4 Σ_ρ |ρ|^(−2).
2. Under RH, 1 − ρ = ρ̄, so |ρ|² = ρ(1−ρ).
3. Σ_ρ 1/(ρ(1−ρ)) = Σ_ρ (1/ρ + 1/(1−ρ)) = 2 Σ_ρ 1/ρ. The sum is taken symmetrically; ρ ↦ 1−ρ permutes the zeros.
4. 2 Σ_ρ 1/ρ = 2(1 + γ_E/2 − ½ log 4π) = κ (Davenport, Ch. 12).
5. Hence S = 4κ.

*Proof of Corollary B′.* The identity for κ counts zeros with multiplicity, so Σ_{distinct} m/|ρ|² = κ. Therefore S − 4κ = Σ_{distinct} (m²(m+1)² − 4m)/|ρ|². Each term is ≥ 0, and a term vanishes exactly when m = 1. ∎

## 6. Remarks

1. **Hypotheses.** The proof uses RH and F1–F5 only. It assumes nothing about simplicity, ζ′(ρ), b_ρ or gaps between zeros. Multiplicities enter only through F3 and A_ρ.
2. **No rate.** The argument is an abelian limit followed by a Tauberian theorem. A remainder term would need a Tauberian theorem with remainder and uniform control of the η^(−2) terms, which is the corpus hypotheses (H2) and (H3⋆).
3. **Consistency with the explicit formula.** At a simple zero, the residue of G(s) x^s/s is x^ρ [ (2/ρ) log x + (b_ρ − 2/ρ)/ρ ]. So e^(−L/2) C(e^L) ≈ L Σ_ρ (A_ρ/ρ) e^(iγL). By Parseval for almost-periodic functions, its mean square over [0, L] grows like S L³/3. Theorem B makes this leading term rigorous without truncating the explicit formula.
4. **The analogy.** For ψ(x) − x, the same argument with simple poles of residue m(ρ) gives ∫₁^X (ψ(x)−x)² x^(−2) dx ∼ (Σ_{distinct} m²/|ρ|²) log X (see §9). Theorem B replaces the residue m by the double-pole coefficient m(m+1), and log X by (log X)³/3.

## 7. Checkpoints and verdicts

Verdict codes: C = correct, G = fillable gap (what is missing and how to fill it), E = error. **No E was found.**

| # | Where | What was checked | Verdict | Comment |
|---|---|---|---|---|
| B1 | L1, L4, L5 | Coefficient m(m+1); regularity at s = 1; formula for b_ρ | C | Recomputed. b_ρ = −2m(q₀+γ_E); for m = 1 it reduces to ζ″/ζ′(ρ) − 2γ_E. |
| B2 | Step 1 | A priori bound C(x) ≪ x^(1/2+ε) under RH | C | Depends on Theorem A §3.3 (case Θ = ½), which is reviewed separately. Standard. |
| B3 | Step 2 | Plancherel identity (2.1): h ∈ L¹∩L²; transform equals G/s on Re s = ½+η | C | Exact identity. L¹ comes from Q_{η′}, η′ < η. Identification by absolute convergence on Re s > ½ plus analytic continuation. |
| B4 | Lemma P | Bound \|G\| ≪ (log t)·W + log² t from F1–F3, with multiplicities | C | This was REFEREE_B's "major point". Now written in full; the far zeros in q′ contribute ≪ log t. |
| B5 | Lemma T | Tail ≪ (log Y)⁴/(Yη³), uniform in η ∈ (0, ½] | C | Constants are absolute. Cauchy–Schwarz on W absorbs close pairs at a cost of log T. No gap information is used. |
| B6 | Step 4(a) | Local constant A²/(4\|ρ\|²) and the weight variation of \|s\|^(−2) | C, with minor G | Restrict to η ≤ ¼ so that the line lies in the rectangle [½, ¾] (v3.4 says η ∈ (0, ½]). The error is O_Y(η), sharper than the stated O_Y(η^(1/2)). For edge zeros, "at most this value" should read "at most this value + O_Y(η)". |
| B7 | Step 4(b) | Cross terms between distinct zeros | C | O_Y(η^(−1)) with a constant depending on d_Y. Harmless because Y is fixed before η ↓ 0. This is where (H3) would enter if uniformity in Y were required; it is not. |
| B8 | Step 4(c) | Simple-pole and holomorphic remainder | C | ‖r‖² = O_Y(η^(−1)), so the cross term with P is O_Y(η^(−2)) by Cauchy–Schwarz. |
| B9 | Step 5 | S < ∞ with multiplicities; order of limits | C | Dyadic block ≪ log⁴T/T (the corpus gives log⁵T/T, also enough). Limits in the order η → 0, then Y → ∞; legitimate because Lemma T is uniform. |
| B10 | Step 6 | Karamata: monotonicity, variable, constants | C, with minor G (citation) | Q_η = ℒU(2η) exactly; U(L) = Q(e^L) is non-decreasing; the transform is finite for λ > 0. Constants check: 2Sλ^(−3) → (S/3)L³. Add an exact reference for F4 (§3). |
| B11 | Simple-zero value | S = 4κ, κ = 2 + γ_E − log 4π | C | Needs RH for \|ρ\|² = ρ(1−ρ). Numerically confirmed to a relative 8·10^(−6) (§8). |
| B12 | F1–F3 | Citations | G | Titchmarsh Thm 9.6(A) and Thm 9.2; Davenport Ch. 12. Quoted from memory; verify the numbering. |
| B13 | Whole | Priority | Open | No earlier statement of B was found; the method is Cramér's. See §9 and question Q1. |

## 8. Numerical sanity checks

These are illustrations, not evidence for RH. I wrote the code independently of the corpus code.

**κ from the zero list.** I used the 1070 zeros with 0 < γ ≤ 1500.35 in `data/zeta_zeros_1500.csv`.

- 2 Σ 1/|ρ|² = 0.0448179.
- Analytic tail estimate (1/(πT))(log(T/2π) + 1) = 0.0013738.
- Total 0.0461918, against κ = 0.0461914. Relative difference 8·10^(−6).
- With 100, 300 and 600 zeros, the tail-corrected sum is stable to 2·10^(−4) in relative terms.

**Q(X) computed independently.**

- Method: a sieve for n ≤ 10⁸ using the support formula of L3 (c(p^k) = −log²p + 2γ_E log p; c(p^a q^b) = 2 log p log q; c = 0 otherwise).
- Q(X) = Σ_{n<X} C(n)² (1/n − 1/(n+1)).
- For X ≤ 4·10⁶ the values agree with `data/explicit_vs_measured.csv` to every printed digit.
- The "model" column is (4κ/3)L³ + αL² + βL, with the tail-corrected α = −0.3074 and the heuristic β ≈ 0.637 described below.

| X | L = log X | Q(X) | (4κ/3)L³ | Q / leading | model | Q / model |
|---|---|---|---|---|---|---|
| 3·10² | 5.704 | 5.013 | 11.43 | 0.439 | 5.06 | 0.990 |
| 10³ | 6.908 | 8.936 | 20.30 | 0.440 | 10.03 | 0.891 |
| 10⁴ | 9.210 | 27.03 | 48.12 | 0.562 | 27.91 | 0.968 |
| 10⁵ | 11.513 | 60.49 | 93.98 | 0.644 | 60.57 | 0.999 |
| 10⁶ | 13.816 | 111.34 | 162.41 | 0.686 | 112.54 | 0.989 |
| 4·10⁶ | 15.202 | 156.35 | 216.36 | 0.723 | 155.01 | 1.009 |
| 10⁷ | 16.118 | 186.74 | 257.89 | 0.724 | 188.30 | 0.992 |
| 3·10⁷ | 17.217 | 221.82 | 314.30 | 0.706 | 234.16 | 0.947 |
| 10⁸ | 18.421 | 290.58 | 384.96 | 0.755 | 292.39 | 0.994 |

**Why convergence to the leading term is slow.**

- The mean coefficient of L² is α = 2 Σ_ρ [Re b_ρ/|ρ|² − 1/|ρ|⁴], summed over all zeros.
- For a zero on the line, Re(ζ″/ζ′(ρ)) = −2θ′(γ), where θ is the Riemann–Siegel theta function. This was checked to 12 digits on the first three zeros. So Re b_ρ = −2θ′(γ) − 2γ_E exactly, and α can be computed from the ordinates alone, plus an analytic tail.
- Result: α = −0.30745, −0.30746, −0.30739 and −0.30739 with 100, 300, 600 and 1070 zeros respectively.
- The corpus value α ≈ −0.264 is the uncorrected partial sum over 300 zeros; I get −0.26389. Its "drift of 4 % per hundred zeros" is this missing tail.
- β = 2 Σ_{γ>0} |u_γ|² is less certain. Its partial sums are 0.466 (300 zeros) and 0.540 (1070 zeros). A heuristic tail, which fits the mean of (Z″/Z′)²/log²(γ/2π), gives β ≈ 0.64.
- With these values, the ratio to the leading term is ≈ 1 + α/(a₃L) + β/(a₃L²), where a₃ = 4κ/3 and α/a₃ ≈ −4.99. This predicts 0.717 at L = 15.2 (measured 0.723) and 0.760 at L = 18.4 (measured 0.755).
- (Q − leading)/L² stays between −0.20 and −0.31, in line with α + β/L plus an oscillation Φ(L) of about ±0.03.
- Extrapolating, the ratio would reach 0.9 only near L ≈ 48 (X ≈ 10²¹) and 0.95 near L ≈ 98 (X ≈ 10⁴²).

**Conclusion.** The observed ratios of 0.44–0.72 (0.755 at 10⁸) agree with Theorem B together with a large negative mean L² term. There is no tension.

**Side remark (outside Theorem B).** With the corrected α and β, the abelian check at η = 0.2 in `THEOREME_TERME_DOMINANT.md` gives a prediction κ + (α/2)η + (β/2)η² ≈ 0.0282, against 0.0279 measured. That is about 1 %, against 4 % in the corpus. Higher-order terms still matter at η = 0.2, so this is only indicative.

## 9. Literature positioning

Status tags: [read] means the text was read; [abstract/extract] means only an abstract, a web page or an automated extraction of the PDF was seen; [memory] means not checked online.

1. **H. Cramér, "Ein Mittelwertsatz in der Primzahltheorie", Math. Z. 12 (1922), 147–153.** [memory/extract] This bibliographic data is as given in reference [3] of Brent–Platt–Trudgian. I did not locate or read the paper itself. This is the source of the method.
2. **R. P. Brent, D. J. Platt, T. S. Trudgian, "The mean square of the error term in the prime number theorem", J. Number Theory 238 (2022), 740–762.** arXiv:2008.06140 (https://arxiv.org/abs/2008.06140); PDF at https://maths-people.anu.edu.au/brent/pd/rpb274-final.pdf. [abstract/extract]
   - Under RH, limsup I(X)/X² ≤ 0.8603, where I(X) = ∫_X^{2X} (ψ−x)² dx.
   - Their eq. (18), §5.4: G(X) = ∫₁^X (ψ(x)−x)² x^(−2) dx ∼ c₁ log X, with c₁ = Σ_ρ m_ρ/|ρ|² ≈ 0.046, the sum running over zeros counted with multiplicity, that is c₁ = Σ_{distinct} m²/|ρ|² as in Remark 4 of §6. They attribute this to Montgomery–Vaughan, *Multiplicative Number Theory I*, Thm 13.6 and Ex. 13.1.1.3 (not checked).
   - **Theorem B is the exact double-pole analogue of this statement:** c₁ log X becomes (S/3)(log X)³. For simple zeros, c₁ = κ and S/3 = 4κ/3.
3. **A. Akbary, N. Ng, M. Shahabi, "Limiting distributions of the classical error terms of prime number theory".** arXiv:1306.1657 (https://arxiv.org/abs/1306.1657). The journal is Q. J. Math. (2014) according to the authors' file name; volume and pages are unverified. [abstract/extract]
   - This is a general B²-almost-periodic framework. If φ(y) = c + Re Σ r_n e^(iλ_n y) + E(y), with E → 0 in mean square, then (1/Y)∫φ² → c² + ½ Σ|r_n|².
   - Some of their error terms carry a factor y.
   - Applied to e^(−L/2)C(e^L)/L, such a framework should give Theorem B, provided the truncated explicit formula is controlled in mean square. That control would involve b_ρ, i.e. ζ″/ζ′(ρ).
   - The corpus' Plancherel–Tauber route avoids this entirely. I did not check whether their theorems cover our case under RH alone.
4. **W. Banks, S. Sinha, "The Riemann Hypothesis via the generalized von Mangoldt function".** arXiv:2209.11768 (https://arxiv.org/abs/2209.11768). [abstract/extract]
   - RH is equivalent to uniform asymptotics for twisted sums of Λ_k(n) n^(−iy) and of Λ^{∗k}. These are pointwise results; no mean square appears.
   - Λ₂ has Dirichlet series ζ″/ζ = q² − q′, whose double-pole coefficient is m(m−1). That vanishes at simple zeros.
   - G = q² + q′ + 2γ_E q has coefficient m(m+1) (L5 recomputed). So the objects differ, as the corpus already notes in `PRIORITY_CHECK.md`.
5. **S. M. Gonek, S. W. Graham, Y. Lee, "The Lindelöf hypothesis for primes is equivalent to the Riemann hypothesis", Proc. Amer. Math. Soc. 148 (2020), 2863–2875**, https://doi.org/10.1090/proc/14974. [abstract] Neighbour of Theorem A rather than of Theorem B.

**Not found.** I found no explicit statement of Theorem B, and no mean-square asymptotic for Σ_{n≤x}(Λ∗Λ)(n) minus its main terms. This is based on about ten searches; absence from them does not prove absence from the literature.

**Assessment.** The statement may well be unpublished in this form. A specialist would nonetheless see it as a direct transposition of Cramér's theorem, or as a consequence of a B² framework. Its value lies in the explicit constant S, the form with multiplicities, and Corollary B′. It should not be presented as new in method.

## 10. Three questions for the external reviewer

1. **Priority.** Is Theorem B already in the literature, or a general Cramér-type theorem that covers it? Such a theorem would say: a Dirichlet series with poles of order k on Re s = ½ gives a logarithmic mean square of order (log X)^(2k−1). Possible places are Montgomery–Vaughan Ch. 13 or a B²-almost-periodic framework such as Akbary–Ng–Shahabi. If so, which reference should be cited?
2. **Uniformity.** Do you agree that the proof needs no information on gaps between zeros? Lemma T is uniform in η, and the off-diagonal terms (Step 4(b)) are used only at a fixed height Y, before Y → ∞. Is the bound ∫_T^{2T} W² dt ≪ T log²T η^(−3), obtained by Cauchy–Schwarz with Z ≪ log T, acceptable as written?
3. **Rate.** Can a remainder Q(X) = (S/3)(log X)³ + O((log X)^(3−δ)) be obtained under RH alone? Possible routes are a Tauberian theorem with remainder or a direct explicit-formula argument. Or does any rate need a hypothesis on close pairs of zeros or on ζ′(ρ), as Proposition C in the corpus suggests?

## 11. Changes from the v4.5 dossier

1. This note covers Theorem B only and is self-contained. Lemma P (the pointwise bound on G, including the far zeros in q′) and Lemma T are now written in full; REFEREE_B had asked for this.
2. Step 4: η is restricted to (0, ¼] so that the line lies in the rectangle of the local decomposition. The diagonal error is O_Y(η) rather than O_Y(η^(1/2)). The bound for edge zeros now includes its O_Y(η) term.
3. The text now says explicitly that close pairs (H3) cannot affect the leading term, because of the order of limits, and that this is also why there is no rate.
4. Step 6: Q_η is stated as an exact Laplace–Stieltjes transform of the monotone function U at λ = 2η. F4 now has a precise statement and candidate references.
5. Step 5: the dyadic bound for S is tightened to log⁴T/T.
6. New Corollary B′: under RH, S ≥ 4κ, with equality if and only if all zeros are simple.
7. Literature:
   - Cramér's pages (147–153) added.
   - The ψ-analogue is pinned to BPT eq. (18), attributed there to Montgomery–Vaughan.
   - Akbary–Ng–Shahabi added as a nearby framework.
   - Banks–Sinha cited as arXiv:2209.11768 instead of a talk abstract.
   - Gonek–Graham–Lee given in full.
8. Numerics:
   - Independent recomputation of Q(X) up to 10⁸.
   - α corrected from −0.264 (300-zero partial sum) to −0.3074 (tail-corrected, via Re b_ρ = −2θ′(γ) − 2γ_E).
   - β ≈ 0.64 (heuristic tail).
   - The slow convergence is now quantified.
9. Checkpoints are renumbered B1–B13 and come with verdicts.

## References

- H. Cramér, Ein Mittelwertsatz in der Primzahltheorie, Math. Z. 12 (1922), 147–153. [via BPT; not read]
- R. P. Brent, D. J. Platt, T. S. Trudgian, The mean square of the error term in the prime number theorem, J. Number Theory 238 (2022), 740–762; https://arxiv.org/abs/2008.06140; https://maths-people.anu.edu.au/brent/pd/rpb274-final.pdf
- H. L. Montgomery, R. C. Vaughan, Multiplicative Number Theory I, Cambridge, 2007, Thm 13.6 and Ex. 13.1.1.3. [as cited by BPT; not checked]
- A. Akbary, N. Ng, M. Shahabi, Limiting distributions of the classical error terms of prime number theory, https://arxiv.org/abs/1306.1657 [Q. J. Math. 2014; volume and pages unverified]
- W. Banks, S. Sinha, The Riemann Hypothesis via the generalized von Mangoldt function, https://arxiv.org/abs/2209.11768
- S. M. Gonek, S. W. Graham, Y. Lee, The Lindelöf hypothesis for primes is equivalent to the Riemann hypothesis, Proc. AMS 148 (2020), 2863–2875, https://doi.org/10.1090/proc/14974
- E. C. Titchmarsh, The Theory of the Riemann Zeta-Function, 2nd ed. (rev. D. R. Heath-Brown), Oxford, 1986, §9.2, §9.6. [memory]
- H. Davenport, Multiplicative Number Theory, 3rd ed., Springer, Ch. 12. [memory]
- D. V. Widder, The Laplace Transform, Princeton, 1941, Ch. V; W. Feller, An Introduction to Probability Theory and Its Applications, Vol. II, XIII.5; J. Korevaar, Tauberian Theory: A Century of Developments, Springer, 2004, Ch. I. [memory; theorem numbers to verify]
