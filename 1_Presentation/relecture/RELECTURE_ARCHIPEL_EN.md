# Referee dossier: "L'Archipel d'Euler" (note 30, §3)

Prepared as a referee-in-advance review of the proved part (§3) of `1_Presentation/30_ARCHIPEL_D_EULER.md`. The measured parts (§4 to §7) are numerical. They were read for context only, and their results are not checked here. The corpus does not claim a proof of RH, and nothing below does either.

**Overall verdict: ready after small fixes.** The mathematics of §3 is correct in substance. There are three issues:

1. The deduction in §3.4 has a fillable gap. The modulus of the character in Saias–Weingartner is not controlled, the phases are dropped, and the degenerate cases are not treated.
2. One sentence of §3.1 is wrong as worded: the claim "same thing" for V₅ even.
3. The main corollary ("in V_q, no zeros in Re s > 1 ⇒ Euler point") is an immediate special case of Saias–Weingartner, Theorem 2. It must be presented as such, not as new.

## 1. Setting

Let q be prime and κ ∈ {0, 1} a parity. Let X = X(q, κ) be the set of non-principal (hence primitive) characters χ mod q with χ(−1) = (−1)^κ, and d = |X|.

**Root numbers and Hardy phases.** Put Λ(s, χ) = (q/π)^((s+κ)/2) Γ((s+κ)/2) L(s, χ). Then Λ(s, χ) = ε_χ Λ(1 − s, χ̄) with ε_χ = τ(χ)/(i^κ √q) and |ε_χ| = 1. Write ε_χ = e^(2iφ_χ) and u_χ = e^(−iφ_χ).

**The space.** V_q = V_q^κ = { F_c(s) = Σ_{χ∈X} c_χ u_χ L(s, χ) : c ∈ ℝ^d }.

The Dirichlet coefficients are a_c(n) = Σ_χ c_χ u_χ χ(n). This sequence is q-periodic, vanishes when q | n, and has a_c(1) = Σ_χ c_χ u_χ.

**Lemma 0 (common functional equation).** Put ξ_c(s) = (q/π)^(s/2) Γ((s+κ)/2) F_c(s). Then ξ_c(1 − s) = conj(ξ_c(conj s)), so ξ_c(1/2 + it) is real.

*Proof.* Using ε_χ = u_χ^(−2), we get u_χ Λ(s, χ) = conj(u_χ) Λ(1 − s, χ̄). Since conj(Λ(conj s, χ)) = Λ(s, χ̄), this says that ξ_χ := u_χ Λ(·, χ) satisfies ξ_χ(1 − s) = conj(ξ_χ(conj s)). Real linear combinations preserve this identity. ∎

Checked numerically: the relative error is about 2·10⁻¹⁵ at s = 0.83 + 7.3i for random real c with q = 7, 11 and 13, using the corpus's `characters()`.

**Euler points.** These are the points c = λ e_χ with λ ∈ ℝ∖{0}, that is F = λ u_χ L(s, χ). There are 27 of them in the spaces of dimension at least 2 for q ≤ 13: 2 + 2 + 3 + 4 + 5 + 5 + 6. The table in §2 of the note was checked.

**Multiplicativity defect.** For a coefficient sequence a, let D_a(m, n) = a(1)·a(mn) − a(m)·a(n).

- If a(1) ≠ 0, then a/a(1) is multiplicative exactly when D_a(m, n) = 0 for all coprime m, n.
- Moreover a(mn)/a(1) − (a(m)/a(1))(a(n)/a(1)) = D_a(m, n)/a(1)².

For a series with periodic coefficients and a(1) ≠ 0, "F/a(1) has an Euler product Π_p Σ_k g(p^k) p^(−ks)" is equivalent to g = a/a(1) being multiplicative. The correct phrasing of the note's "produit d'Euler" is therefore: **the normalised coefficient sequence a/a(1) is multiplicative (and a(1) ≠ 0)**.

## 2. Statements and proofs

**Lemma 1 (the Euler locus of V_q is the union of the axes).** For c ∈ ℝ^d, D_{a_c}(m, n) = 0 for all coprime m, n if and only if c has at most one nonzero coordinate.

*Proof.*

- **Every pair of classes is reached by coprime integers.** Let h be the restriction of a = a_c to G = (ℤ/qℤ)*. For r, s ∈ G, the Chinese remainder theorem gives coprime m ≡ r and n ≡ s (mod q). Take m as the least positive representative of r, and n ≡ s (mod q) with n ≡ 1 (mod m).
- **Case a(1) = 0.** Then h(r)h(s) = 0 for all r, s. Hence h = 0, and c = 0 by linear independence of the characters of G.
- **Case a(1) ≠ 0.** Then ψ = h/h(1) satisfies ψ(rs) = ψ(r)ψ(s), so ψ is a character of G.
- **Conclusion.** The relation Σ_χ c_χ u_χ χ = h(1)·ψ and linear independence force ψ = χ₁ ∈ X, c_{χ₁} u_{χ₁} = h(1), and c_χ = 0 for χ ≠ χ₁.
- **Converse.** It is clear, because characters are completely multiplicative. ∎

The note does not state Lemma 1. It is elementary and is the natural global companion of Proposition 3.3.

**Proposition 3.3 (first-order rigidity; correct).** Let a = λ u_χ χ be an Euler point, and let b = Σ_{χ'∈X} β_{χ'} u_{χ'} χ' be a direction in V_q (β real). Put dD_a(b)(m, n) = a(1)b(mn) + b(1)a(mn) − a(m)b(n) − b(m)a(n). This is the first-order term of D_{a+εb}.

(i) For **all** m, n ≥ 1 (coprimality is not needed, because characters are completely multiplicative):

  dD_a(b)(m, n) = λ u_χ Σ_{χ'≠χ} β_{χ'} u_{χ'} (χ' − χ)(m)·(χ' − χ)(n).

For a single direction b = u'·χ' this is the note's formula u·u'·(χ' − χ)(m)(χ' − χ)(n). The χ'-component with χ' = χ contributes nothing (the scale direction).

(ii) **Quantitative form (new here).** The right-hand side depends only on the classes r = m mod q and s = n mod q, and every pair (r, s) ∈ G×G is reached by coprime (m, n). Its mean square over G×G is

  (1/(q−1)²) Σ_{r,s∈G} |dD_a(b)(r, s)|² = λ² · ( 3 Σ_{χ'≠χ} β_{χ'}² + |Σ_{χ'≠χ} β_{χ'} u_{χ'}|² ) ≥ 3λ² ‖β_⊥‖².

Here β_⊥ is the part of β orthogonal to e_χ.

(iii) Consequently, dD_a(b) vanishes on all coprime pairs if and only if b ∈ ℝ·a. The same holds for the normalised sequence, because d/dε [D_{a+εb}/(a(1)+εb(1))²] at ε = 0 equals dD_a(b)/a(1)², since D_a = 0 and a(1) = λ u_χ ≠ 0.

*Proof.*

- **(i)** Expand, using χ(mn) = χ(m)χ(n), a(1) = λu_χ and b(1) = Σ β_{χ'} u_{χ'}. The four terms of the χ'-component combine to λ u_χ β_{χ'} u_{χ'} [χ'(m)χ'(n) + χ(m)χ(n) − χ(m)χ'(n) − χ'(m)χ(n)], which is the product stated.
- **(ii) Orthogonality.** For χ', χ'' ≠ χ, the orthogonality relations on G give ⟨χ' − χ, χ'' − χ⟩_G = δ_{χ'χ''} + 1. Hence ⟨(χ'−χ)⊗(χ'−χ), (χ''−χ)⊗(χ''−χ)⟩_{G×G} = (1 + δ_{χ'χ''})², which equals 1 + 3δ_{χ'χ''}.
- **(ii) Summation.** Expanding the square gives λ² Σ β_{χ'} β_{χ''} conj(u_{χ'}) u_{χ''} (1 + 3δ), which is the stated value.
- **(iii)** Follows from (ii). ∎

**Single direction made explicit.** χ' ≠ χ means χ'(r) ≠ χ(r) for some r with 2 ≤ r ≤ q − 1. Take m = r and n = r + q. Then gcd(m, n) = gcd(r, q) = 1, and dD = u u' (χ'(r) − χ(r))² ≠ 0. Neither Dirichlet's theorem nor primes are needed.

**What the proposition adds to Lemma 1.** Lemma 1 already says that the Euler locus is the union of the d axes. Proposition 3.3 says that the quadratic equations D = 0 cut out each axis transversally: the Zariski tangent space at a nonzero point of an axis is the axis itself. The constant 3 makes this quantitative.

**Corollary 3.4 (correct after the fix below; not new).** Let c ≠ 0. The following are equivalent:

(a) F_c is an Euler point;

(b) F_c has no zero in Re s > 1.

If F_c is not an Euler point, there is η = η(c) > 0 such that for all 1/2 ≤ σ₁ < σ₂ ≤ 1 + η and all large T, F_c has ≫ T distinct zeros in σ₁ < Re s < σ₂, |Im s| ≤ T.

In particular, if F_c satisfies RH, then F_c is an Euler point. The reason: F_c has no trivial zeros in Re s > 0, and a zero with Re s > 1 is off the critical line.

*Proof, route A (direct).*

- **(a) ⇒ (b).** This is the absolutely convergent Euler product of L(s, χ).
- **Not (a) ⇒ zeros.** If c has at least two nonzero coordinates, F_c = Σ_{χ∈C} P_χ(s) L(s, χ). Here C = supp(c) is a set of at least two primitive characters, and P_χ = c_χ u_χ are nonzero constant Dirichlet polynomials. This is exactly the hypothesis of Saias–Weingartner, Theorem 2 (§4 below), which gives the count.
- **Conclusion.** Take σ₁ = 1 and σ₂ = 1 + η. ∎

*Proof, route B (the note's route, repaired).* This route uses only the abstract-level statement "if F_a is not of the form P(s)L(s, ψ), then …". Suppose F_c = P(s)·L(s, ψ) with P(s) = Σ_{k≤K} p(k) k^(−s), and ψ a Dirichlet character of **some modulus Q**. The abstract does not say that Q = q, and nothing forces it a priori.

- **Coefficients at large primes.** For a prime ℓ > K, the only divisor of ℓ that is at most K is 1. So a_c(ℓ) = p(1)·ψ(ℓ). Let h = Σ c_χ u_χ χ on G. The phases u_χ are dropped in the note: there, "Σ c_χ χ(ℓ)" should read Σ c_χ u_χ χ(ℓ).
- **The case p(1) = 0.** Then h vanishes on every class of G, by Dirichlet's theorem mod q. So c = 0, which is excluded. Hence p(1) ≠ 0.
- **Reduction to a character mod q.** Let N = lcm(q, Q). Every r ∈ (ℤ/Nℤ)* contains primes ℓ > K. So h(r mod q) = p(1)·ψ(r mod Q) for all r ∈ (ℤ/Nℤ)*. The character r ↦ ψ(r mod Q) of (ℤ/Nℤ)* therefore depends only on r mod q. It factors through a character ψ_q of G, and h = p(1)·ψ_q.
- **Conclusion.** By linear independence of the characters of G, ψ_q must lie in X. The trivial character or a character of the wrong parity would force p(1) = 0. So c is supported on the single χ₁ = ψ_q, with c_{χ₁} u_{χ₁} = p(1). F_c is an Euler point. ∎

Dirichlet's theorem can be replaced by the Chinese remainder theorem. Pick n ≡ r (mod N) with n ≡ 1 modulo each prime p ≤ K with p ∤ N. Then every prime factor of n exceeds K, and a(n) = p(1)ψ(n).

**What does not matter.** The real coefficients and the phases u_χ play no role in Corollary 3.4. It holds for every complex combination of at least two distinct primitive L-functions, of any moduli: this is Saias–Weingartner, Theorem 2 itself. The real coefficients and phases matter only for Lemma 0 (Hardy symmetry), which is what makes "RH" and "pairs leaving the line through a double zero" meaningful in §4 to §6.

**Degenerate cases.** c = 0 must be excluded explicitly; F ≡ 0 vanishes everywhere. In dimension-1 spaces the proposition is vacuous (there is no χ' ≠ χ), and the corollary is trivial.

## 3. Checkpoints

| # | Claim (note §) | Verdict | Comment / what to change |
|---|---|---|---|
| 1 | Common functional equation and real Hardy function with φ_χ = arg(ε_χ)/2 (§2) | **correct** | Lemma 0. Numerically 10⁻¹⁵. |
| 2 | Dimension table; 27 Euler points (§2) | **correct** | Parity rule χ_k(−1) = (−1)^k. Principal character excluded. |
| 3 | Hamburger: a Dirichlet series with the functional equation of ζ (finite order, finitely many poles) is c·ζ (§3.1) | **correct as a citation; add hypothesis** | Hamburger assumes absolute convergence in Re s > 1 for both series in the functional equation. State it. Hypotheses taken from the standard statement; the primary source was not re-read (§4). |
| 4 | "Même chose dans V₃ impair et V₅ pair" (§3.1) | **error in wording (local, fillable)** | Inside V_q this is trivially true (dimension 1). In the class the sentence refers to (finite order, finitely many poles), it is **false for V₅ even**. (1 + 5^(1/2−s))ζ(s) has exactly the functional equation of L(s, (·/5)) (Γ(s/2), conductor 5, ω = 1), so L(s, (·/5)) + t(1 + 5^(1/2−s))ζ(s) is a deformation. The note's own parenthesis says this. Rephrase: "trivially inside V_q; among *entire* Dirichlet series with this functional equation, by the Kaczorowski–Perelli structure of degree 1 (not by Hamburger)". For V₃ odd no ζ-type term exists (wrong parity). |
| 5 | Kaczorowski–Perelli: degree-1 Selberg class = {ζ} ∪ {L(s+iθ, χ), χ primitive} (§3.2) | **correct** | Include ζ (θ = 0 only, because of the pole). Note that the shift by iθ changes the gamma factor: with the functional equation fixed, even θ is fixed. |
| 6 | Formula u·u'·(χ'−χ)(m)(χ'−χ)(n) (§3.3) | **correct** | Holds for all m, n, not only coprime ones. Checked: max error 3·10⁻¹⁴ over all 27 points, all directions, all m, n ≤ 40. |
| 7 | "Hence nonzero" for one direction (§3.3) | **correct** | Explicit coprime pair m = r, n = r + q. |
| 8 | General direction: orthogonality on G×G ⇒ kernel = scale (§3.3, proof) | **correct** | Every class pair is reached by coprime integers (Chinese remainder theorem; the note's "distinct primes" via Dirichlet also works). Quantitative identity (ii) above. |
| 9 | Normalisation by a(1); "produit d'Euler" (§3.3) | **fillable (phrasing)** | State it as multiplicativity of a/a(1) with a(1) ≠ 0. At first order the normalised defect is dD/a(1)², with the same kernel. Add Lemma 1 (the global classification). |
| 10 | Bold sentence "Aucune direction qui garde l'équation fonctionnelle…" (§3.3) | **fillable (scope)** | Proved for directions **in V_q**. The full space of Dirichlet series with the same functional equation also contains, for even parity, the direction (1 + q^(1/2−s))ζ(s) (with a pole). Write "aucune direction de V_q". |
| 11 | Eigenvalues 2.36 to 3.27 "vérifié pour les 27 points" (§3.3) | **correct but not intrinsic** | Values depend on the truncation. The CSV uses M = 40; the function default M = 60 gives other values (e.g. V₇ even: 3.27 at M = 40 versus 3.02 at M = 60). The exact mean over G×G is 3 + λ_min(Re(w w*)): 4 for d = 2; 3.17 or 3.61 for V₇ odd; 3 for d ≥ 4. Quote the identity (ii) instead; 10⁻²⁸ for the scale is floating-point zero. |
| 12 | Saias–Weingartner statement as paraphrased (§3.4) | **correct** | Matches the abstract (§4). |
| 13 | "P(s)L(s, χ₀) only reached by multiples of a single L" (§3.4) | **fillable gap** | Missing: (a) the phases u_χ; (b) the modulus Q of χ₀ is arbitrary, so "Dirichlet ⇒ all classes mod q" needs the lcm(q, Q) argument of route B; (c) the cases p(1) = 0, trivial χ₀ and wrong parity; (d) c ≠ 0. Simplest fix: route A (Theorem 2). |
| 14 | "In V_q, RH (or no zero in Re s > 1) ⇒ Euler point; proved without hypothesis" (§3.4, §9) | **correct after #13; not new** | Immediate special case of Saias–Weingartner, Theorem 2. Better as an equivalence: for c ≠ 0, no zero in Re s > 1 ⇔ Euler point. Attribute it as "immediate from Saias–Weingartner (2009), Th. 2". |
| 15 | "As T → ∞ only the Euler points remain" (§8) | **correct as "at most"** | The intersection over T of the RH regions is {Euler points satisfying GRH}. Equality needs GRH; the note's "Supposé" paragraph says so. |
| 16 | Title "parmi les fonctions qui ont l'équation fonctionnelle, RH n'existe qu'aux points d'Euler" | **fillable (scope)** | True in V_q. In the larger functional-equation space (even parity), (1 + q^(1/2−s))ζ(s) has multiplicative coefficients, satisfies RH iff ζ does, and is not in V_q. Add "dans V_q" to the title. |

## 4. Literature (verified, with what was and was not checked)

**Saias & Weingartner.** E. Saias, A. Weingartner, *Zeros of Dirichlet series with periodic coefficients*, Acta Arith. 140 (2009), no. 4, 335–344, DOI 10.4064/aa140-4-4.

- Sources: journal page https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/140/4/82562/zeros-of-dirichlet-series-with-periodic-coefficients ; arXiv https://arxiv.org/abs/0807.0783 ; full text https://ar5iv.labs.arxiv.org/html/0807.0783 .
- **Abstract (verified):** Let a = (a_n) be periodic, F_a(s) the meromorphic continuation of Σ a_n n^(−s), and N_a(σ₁, σ₂, T) the number of zeros of F_a, counted with multiplicity, in σ₁ < Re s < σ₂, |Im s| ≤ T. If F_a(s) is not of the form P(s)L_χ(s), with P(s) a Dirichlet polynomial and L_χ a Dirichlet L-function, then there exists η = η(a) > 0 such that for all 1/2 < σ₁ < σ₂ < 1 + η, c₁T ≤ N_a(σ₁, σ₂, T) ≤ c₂T for T sufficiently large. The positive constants c₁, c₂ depend on a, σ₁ and σ₂.
- **Theorem 2 (verified in the full text):** Let 𝒞 be a finite set of at least two primitive Dirichlet characters, and (P_ψ)_{ψ∈𝒞} non-zero Dirichlet polynomials. Put F(s) = Σ_{ψ∈𝒞} P_ψ(s) L_ψ(s). Then there exists η = η(F) > 0 such that for all 1/2 ≤ σ₁ < σ₂ ≤ 1 + η and all sufficiently large T, N'_F(σ₁, σ₂, T) ≫_{F,σ₁,σ₂} T. Here N' counts distinct zeros in σ₁ < Re s < σ₂, |Im s| ≤ T.
- **Other statements in the paper (verified):**
  - Theorem 1: orthogonal decomposition of the space H_q of q-periodic Dirichlet series into the subspaces E_{q,ψ}.
  - Theorem 3: N_{F_a}(1/2 + u, +∞, T) ≪ T log(1/u)/u.
  - Theorem 4: the general periodic case.
  - The Remark after Theorem 4: if F_a(s) does not vanish in Re s > 1/2, then F_a(s) = P(s)L_ψ(s) with ψ primitive.
- **No "if and only if" is stated** in the paper.
- **Previous work:** the paper builds on Davenport–Heilbronn, Kaczorowski–Kulas and Steuding (the references were seen only as in-text keys).

**Hamburger.** H. Hamburger, *Über die Riemannsche Funktionalgleichung der ζ-Funktion* (Math. Z., 1921–1922, three communications). The "Zweite Mitteilung" (1921, DOI 10.1007/BF01203626) was seen as a record at https://zenodo.org/records/2099496 .

- Statement used: if f(s) = Σ a_n n^(−s) and g(s) = Σ b_n n^(−s) converge absolutely for Re s > 1, (s − 1)f(s) is entire of finite order, and π^(−s/2)Γ(s/2) f(s) = π^(−(1−s)/2) Γ((1−s)/2) g(1 − s), then f = g = a₁ ζ.
- **The exact hypotheses were not re-verified from the primary text.** The publisher and Project Euclid pages were not reachable from this environment. The statement above is the standard one, as I recall it; the Titchmarsh reference, The Theory of the Riemann Zeta-Function, §2.13, is from memory and was not looked up.

**Kaczorowski & Perelli.** J. Kaczorowski, A. Perelli, *On the structure of the Selberg class, I: 0 ≤ d ≤ 1*, Acta Math. 182 (1999), no. 2, 207–241. Bibliographic data from https://archive.ymsc.tsinghua.edu.cn/pacm_paperurl/20170108203333561257577 ; PDF at https://projecteuclid.org/journals/acta-mathematica/volume-182/issue-2/On-the-structure-of-the-Selberg-class-I-0d1/10.1007/BF02392574.pdf .

- The classification was verified through K. Soundararajan, *Degree 1 elements of the Selberg class*, https://arxiv.org/abs/math/0306300 (short proof of the Kaczorowski–Perelli theorem).
- Statement: if F satisfies the Selberg axioms and has degree 1, then F(s) = L(s + iA, χ') with χ' primitive. The introduction of the same paper describes the degree-1 class as consisting of ζ and the shifts of Dirichlet L-functions.
- The structure theorem for the *extended* class S♯ in degree 1 (linear combinations of Dirichlet polynomials times L-functions), used in checkpoint 4, is quoted from memory. It was not re-checked here.

**Degree-2 analogue: Booker & Thorne.** A. R. Booker, F. Thorne, *Zeros of L-functions outside the critical strip*, Algebra & Number Theory 8 (2014), no. 9, DOI 10.2140/ant.2014.8.2027. Sources: arXiv https://arxiv.org/abs/1306.6362 , full text https://ar5iv.labs.arxiv.org/html/1306.6362 , Project Euclid https://projecteuclid.org/euclid.ant/1513730308 .

- **Abstract (verified):** Dirichlet series associated to automorphic forms that lack an Euler product must have zeros in the region of absolute convergence.
- **Theorem 1.1:** if f is a holomorphic cusp form of weight k and level N whose completed L-function has no zeros in Re s > (k+1)/2, then f is an eigenfunction of the Hecke operators T_p for all p ∤ N.
- **Theorem 1.2:** let π₁, …, π_n be pairwise non-isomorphic unitary cuspidal automorphic representations of GL_{r_j}(𝔸_ℚ) satisfying Ramanujan at finite places, and P a polynomial with finite-Dirichlet-series coefficients. Either P(L(s, π₁), …, L(s, π_n)) has a zero with Re s > 1, or P is a monomial D(s)·x₁^{d₁}⋯x_n^{d_n}.
- **Remark 3:** the Ramanujan hypothesis can be relaxed, and the result extends to Maass forms when the tensor square is automorphic, which is known for r_j = 2.
- **Remark 5:** the paper improves Nakamura–Pańkowski (zeros in Re s > 1 − δ) to Re s > 1.
- **Their reading of Saias–Weingartner:** either the series vanishes somewhere in Re s > 1, or it equals D(s)L(s, χ) with χ primitive.
- **Correction (verified):** https://msp.org/ant/2014/8-9/ant-v8-n9-x01-Correction-ZerosOfLFunctions.pdf . It weakens the error term of Lemma 2.1 to O(1/log(2/(σ−1))), and states that the main results remain valid.
- **Consequence for the corpus.** For S₂₄(SL₂(ℤ)) (dimension 2, root number +1, eigenforms with real coefficients), the degree-2 analogue of Corollary 3.4 is already Booker–Thorne, Theorem 1.1. A form f ∈ S₂₄ with L(s, f) ≠ 0 for Re s > 25/2 is a Hecke eigenform; at level 1 that means a multiple of one of the two normalised eigenforms.
- **What is not covered.** The degree-2 analogue of Proposition 3.3 is not in Booker–Thorne. The closed form is the same for coprime m, n: (λ₂ − λ₁)(m)(λ₂ − λ₁)(n). For d ≥ 3 the kernel argument needs linear independence of the functions λ_j ⊗ λ_k on coprime pairs, which replaces character orthogonality.

**Related work.**

- M. Righetti, *Zeros of combinations of Euler products for σ > 1*, DOI 10.1007/s00605-015-0773-0 (Monatsh. Math.), https://arxiv.org/abs/1412.6331 (abstract verified). A non-monomial polynomial expression in Euler products from a wide class (including automorphic L-functions under Ramanujan) has infinitely many zeros in σ > 1. It extends Booker–Thorne.
- A density version, *On the density of zeros of linear combinations of Euler products for σ > 1*, https://arxiv.org/abs/1506.05716 (seen only as a title; not checked).
- Bombieri & Hejhal (1995) studied exactly the Hardy-normalised linear combinations with a common functional equation used in V_q. Subject to GRH and a weak pair-correlation hypothesis, they show that almost all zeros lie on the critical line. This is cited from Booker–Thorne, Remark 2; the reference (Duke Math. J. 80 (1995)) was not re-checked. **This is the right framework in which to place §4 to §6 of the note.**

**Novelty.** "In V_q, no zero in Re s > 1 ⇒ Euler point" (hence "RH ⇒ Euler point") is **not new**. It is an immediate special case of Saias–Weingartner, Theorem 2, and also of Booker–Thorne, Theorem 1.2 with n = 1 and P linear. Proposition 3.3 is correct and elementary; I found no statement of it in the literature, but its content is modest (Lemma 1 plus transversality).

## 5. Numerical checks done for this review

All checks were done in the scratchpad, without modifying the corpus.

- The closed form (i) at all 27 Euler points, all directions, all 1 ≤ m, n ≤ 40: max error 2.9·10⁻¹⁴.
- Rank of the first-order map on G×G: d − 1 in every space, over both ℂ and ℝ.
- The identity (ii) on random directions: relative error 3·10⁻¹³.
- The CSV values are reproduced with M = 40, which is the value used in `scripts/run_euler_archipelago.py`.
- Lemma 0 checked with mpmath (see §1).

## 6. Questions for the external reviewer

1. **Attribution.** Is it accurate and sufficient to present "for c ≠ 0, F_c has no zero in Re s > 1 ⇔ F_c is an Euler point" as an immediate corollary of Saias–Weingartner, Theorem 2? Is there an earlier or more standard reference for linear combinations of Dirichlet L-functions with a common functional equation, for instance Kaczorowski–Kulas (2007)?
2. **Effectivity.** Is anything known, or easily provable, about the dependence of η(F) and of the height of the first zero in Re s > 1 on the distance of c to the nearest axis? The note measures "unmasking heights" (§4 and §7). An effective Saias–Weingartner bound would turn the measured shrinking law r(T) ≈ N^(−0.77) into something comparable with a theorem.
3. **Degree 2.** For S₂₄(SL₂(ℤ)), Booker–Thorne give the analogue of Corollary 3.4. Is the first-order rigidity (Proposition 3.3) at Hecke eigenforms, together with its non-degeneracy for d ≥ 3, known or immediate (for example via linear independence of multiplicative functions)? Is there a natural analogue of the constant 3 in identity (ii)?
