# Riemann Programme — Synthesis

*English version of [document 01](../01_SYNTHESE_FR.md), updated at V6.58, 17 October 2026. State described: V6.58. In case of discrepancy, the French text prevails.*

**Status:** the essentials in a few pages, for a reader discovering the programme. For the current state at a glance, see “Read first” in [README_EN](../../README_EN.md); for the full logic, the [logical table](../../LOGICAL_TABLE.md).  
**Author:** Vincent NOËL

> **Key points**
>
> - No proof of the Riemann Hypothesis (RH) is claimed. The results below are presented for what they are.
> - Three analytic statements are proved (Theorems A and B, Corollary B′) and were internally pre-reviewed at V6.13. No specialist has reviewed them yet; that is the next step.
> - Weil positivity is **certified on all test functions** with vanishing moments, but only on bounded windows (support up to 11/20). Zhu (2026) certifies it up to 0.8 for all functions; the margin collapses at each widening.
> - In the reduced model, where RH is a theorem, the sign comes neither from point counts nor from isogeny degrees, but from a **square** (a polarization). ζ already passes the first two levels. What is missing is the object that would supply the square.
> - Each recent step writes its prediction before the computation. Several predictions were false, and the documents say so.

## 1. The question and the working hypothesis

**The starting question.** To the primes we attach a quantity Q(X), a sum of squares built so that every zero of the Riemann zeta function becomes a double pole. Its growth rate tells how far the farthest zero lies from the critical line. Versions 1 to 5 established and checked this reformulation.

**The author's working hypothesis.**

> *RH exists only because it is necessary to something larger that makes it necessary.*

Wherever an analogue of RH is proved, the proof goes through a positivity on an object larger than the function itself: the surface C × C for curves over finite fields (Weil, 1948 [Wei48]), a Hilbert space for the Selberg zeta function (Selberg, 1956 [Sel56]). For ζ, that object has not been built. The programme does not attack it head-on. It asks three smaller questions: what does a proved necessity look like? Does ζ show it? What, exactly, is missing?

## 2. What is proved

The statements in logical form, with their hypotheses and status, are in the [logical table](../../LOGICAL_TABLE.md).

| | Statement | Status |
|---|---|---|
| **Theorem A** | With c = Λ∗Λ − Λ·log + 2γΛ, C(x) = Σ~n≤x~ c(n) and Q(X) = ∫~1~^X^ \|C(x)\|² x^−2^ dx: ½·limsup log(1+Q(X))/log X = Θ − ½, where Θ is the largest real part of the zeros. Hence RH ⟺ Q(X) = X^o(1)^. | Proved, unconditionally; pre-reviewed (doc. 37). An exact reformulation of RH, not a step towards it. |
| **Theorem B** | Under RH, Q(X) ∼ (S/3)(log X)³, with S = Σ~ρ~ m²(m+1)²/\|ρ\|². | Proved under RH; the double-pole analogue of Cramér's theorem [Cra22]. |
| **Corollary B′** | Under RH, Q(X)/(log X)³ → 4κ/3 if and only if all zeros are simple (κ = 2 + γ − log 4π). Together with A, a joint criterion for RH and simplicity. | Proved; new as far as we know, to be checked. |
| **Weil certificates** (docs. 71, 73, 75) | For every test function supported in [−S, S], of finite energy, with vanishing exponential moments: Q_W(f) ≥ ‖f‖²/25 if S ≤ 0.347; ≥ ‖f‖²/250 if S ≤ 1/2; ≥ (3/10000)‖f‖² if S ≤ 11/20. No zeros, no RH. | Certified by interval arithmetic in the declared model. In range, covered by Zhu's certified lower bound [Zhu26]. |
| **Head of conductors** (essay V6.55) | Exact restitution of the Möbius sum; the head q ≤ H is bounded explicitly at every scale. | Proved under its guards. The large tail remains open. |
| **Three levels of the sign** (doc. 80) | For a polynomial stable under α ↦ q/α: degrees N(u) ≥ 0 ⟺ real roots of even multiplicity; with distinct roots, the form B = Tr(u·ι(u)) has r/2 negative directions. | Proved (elementary); 645 polynomials checked exactly. |
| **Others** | First-order rigidity at the Euler points (doc. 30; “RH ⇒ Euler point” is a case of Saias–Weingartner [SW09]); inertia lemma (38); local margin = pair correlation (40); jet lemma (58); negative certificate for DH (60). | Proved in their setting. |

The pre-review was done by three mutually independent reviews, carried out by models of the same family as those that helped write the proofs. It does not replace a specialist.

## 3. The most solid measurements

All these measurements are reproducible: data, scripts and tests (`python tests/run_all_tests.py`).

| Result (document) | What is measured | Key figures |
|---|---|---|
| **Reduced model** (28, 29, 80) | On curves over finite fields, where RH is a theorem: the functional equation and a positive Euler product are not enough; Castelnuovo positivity [MT58], floor by floor, unmasks the fakes. At V6.58: isogeny degrees are not enough either; only the trace of a square unmasks the 119 genus-2 fake twins. | 425 curves; 220 fake twins; exact Gram realization for 424 curves. |
| **Euler archipelago** (30) | Among functions with the same functional equation, RH survives only around the Euler points, in islands that shrink with height. | 27 islands; median radius 0.091 (\|t\| ≤ 25), then 0.008 (\|t\| ≤ 300). |
| **Generator of the primes** (33) | The operator of ζ is rebuilt from the primes alone. Its metric is positive for ζ and L(s, χ~5~), negative for Davenport–Heilbronn [DH36a] [DH36b] exactly at its off-line zeros. | 284 zeros of ζ with the primes ≤ 23,862; no false detection. |
| **Heisenberg time** (38, 39) | An off-line quadruple is heard once the window reaches log(q·γ~0~/2π); the law doubles in degree 2. | Ratio 0.95–1.08 for ζ and L. |
| **Meeting of three and margin law** (40, 41) | RH, simplicity and repulsion are read on one quantity, Montgomery's pair correlation [Mon73]. | 1,070 zeros of ζ: 4 margins < 0.1 (GUE: 13; Poisson: 320). |
| **Weil windows** (81) | Zhu's values λ*(L) for L = 0.5 to 0.8, recovered by an independent method (form in the variable x, checked against the zeros to 2·10⁻¹³). On zero-moment test functions the margin is much larger. | λ*(0.8) ≈ 1.8·10⁻¹⁷; moment kernel: 9.2·10⁻⁴ at 11/20, 5.4·10⁻¹² at 0.8. |

The reading that links these measurements is this. ζ shows every observable signature of a proved necessity, except the object that carries it. What is missing is neither the operator, which can be rebuilt, nor a count, which is already positive: it is a square imposed by a structure, not merely measured.

## 4. What remains open or assumed

**Open, in the sense of the logical table.**

- The sign law on a covering family of test functions, and the coverage that transports it to all test functions (route W: W9, W10, W11).
- The object that would supply the square for ζ (route C: C5).
- Slow growth of Q from the primes alone (route Q: Q4), equivalent to RH.
- The signed debt of large conductors, then the bound J ≪ X² (route J: J5, J7).
- An exhaustive spectral realization (route H: H3, H4).

**Assumed.**

- That a larger object carries the positivity of ζ, as the polarized Jacobian does for a curve. This is the working hypothesis itself.
- That the same object also imposes the margin law between zeros, as the monodromy group does over finite fields (Katz–Sarnak [KS99]).
- That the islands of the archipelago close down to zero at large height.
- That the deficit of small margins comes from finite height (Bogomolny et al. [BBLM06]).

## 5. The path since V6.24

| Versions | What was done | Status |
|---|---|---|
| V6.25–V6.33 | Audit of fictitious units (50); characteristic-one Frobenius, read (51); the square in the continuum (52); meeting at height (53); the gap of three (54); presentable papers (55); relief of the archipelago and its driving force (56, 57). | measured; several false predictions, stated |
| V6.34–V6.37 | Jet lemma (58); from the finite tower to the spectral bound (59); three LaTeX papers and a negativity certificate for DH (60); paired anchoring (61). | proved in the setting; certificate |
| V6.38–V6.43 | Decision atlas and Bellman (62); exact constraints and comparison (63, 64); fibres, folds and a certified fold (65, 66); bridges with Bellman (67). | tools; auxiliary proofs |
| V6.44–V6.50 | Domains and effective tail (68, 69); arithmetic bridge and coupling debt (70); first complete Weil certificates on windows, up to S = 11/20 (71 to 75). | certified in the declared domain |
| V6.51–V6.57 | Global Weil track rebuilt (76) and its supplement (Suzuki parity suspended, one-sided operator T₊); mechanisms for the sign (77); positive transport (78); compensation, profiles and obstructions (79) and the signal (supplement 79); anchored correlations; arithmetic amplification (head established, tail open). | auxiliary proofs; obstructions; open |
| V6.58 | Where the sign comes from: counts, degrees or a square (80); Zhu reproduced (81); reorganization (README, corpus map, logical table, ranked references, guide for an AI, English layer). | proved (elementary); measured |

## 6. The progress indicator at V6.58, and what comes next

The indicator places the programme on a scale from 0 (nothing) to 9 (solved). The levels have not moved since V6.18; each stage was re-evaluated and justified.

| Dimension | V5 (5 Oct.) | V6.58 (17 Oct.) | Level reached |
|---|---:|---:|---|
| See | 4 | 4 | Robust measurement |
| Understand | 3 | 5 | Mechanism understood, in a case where RH is proved |
| Situate | 3 | 6 | Statement proved |
| Extend to degree 2 | 0 | 4 | Robust measurement |
| Prove, get reviewed | 6 | 6 | Statement proved |
| The empty box | 2 | 4 | Robust measurement |
| Cross | 0 | 6 | Statement proved |

No dimension reaches 7 (“reviewed”): that requires a human reader.

**Next.** The most valuable step remains human: having paper 1 (Theorems A and B) reviewed by a specialist, who could also endorse a first arXiv submission. On the research side, the logical table shows two clear gaps: the sign law on a covering family (route W) and the object that would supply the square (route C, with no open investigation so far). Extending windows one by one is not a strategy towards RH.

## 7. How to read the corpus

| Entry | What it is for |
|---|---|
| [README_EN](../../README_EN.md), “Read first” | Six essential points, their statuses and links. |
| `00_PORTAL` (`00_PORTAIL.html`, in French) | The interactive entry page: state, latest steps, catalogue of all files. |
| [Logical table](../../LOGICAL_TABLE.md) | Statements in logical form, five routes towards RH, what is missing at the shortest. |
| [Ranked references](../../REFERENCES_RANKED.md) | The 177 references by role; those to verify first. |
| `1_Presentation/articles/` and `relecture/` | The three papers (English) and the file to send to a specialist. |
| [Guide for an AI](../../GUIDE_FOR_AN_AI.md) | Instructions to give another AI, with the procedure for proposing next steps. |

For a first reading: this document, then the [intuitive reading guide](07_READING_GUIDE_EN.md), then [document 80](80_WHERE_THE_SIGN_COMES_FROM.md) (where the sign comes from). Most other documents are in French.

The work was carried out with the help of ChatGPT (OpenAI) and Claude (Anthropic) for exploration, code, bibliographic research and writing. The author takes final responsibility for the content.

*Bracketed keys such as [Wei48] refer to the [ranked references](../../REFERENCES_RANKED.md) and to the full register ([document 42](../42_REGISTRE_DES_SOURCES.md)).*
