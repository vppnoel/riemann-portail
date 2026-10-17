# Intuitive reading guide

*English adaptation of [document 07](../07_GUIDE_DE_LECTURE_INTUITIF.md), updated at V6.58, 17 October 2026. Every section of the French guide is kept, in a condensed form; the figures, tables and full arguments are in the French text and in the documents cited. In case of discrepancy, the French text prevails.*

**Status:** companion document, no new result.  
**Author:** Vincent NOËL

## 0. How to read this guide

This guide is for non-specialists. It is a **path**, from the simplest image to the finest. Each image comes with three things:

- **the image** itself, to fix the intuition;
- **the exact statement** it summarizes, with its status (proved, measured or assumed);
- **where the image breaks**, that is, what it must not be made to say.

One thing is said once and for all. **The programme claims no proof of the Riemann Hypothesis (RH).** The two proved theorems (A and B) were pre-reviewed internally at V6.13, not yet by a specialist. The other proved statements are elementary identities, certificates in a bounded domain, or cited theorems; the rest is measured or assumed, and the guide says so each time.

The author's working hypothesis is the thread: **“RH exists only because it is necessary to something larger that makes it necessary.”** Its reading is gathered in §15.

## 1. The starting image: a signal and its frequencies

**The image.** The primes form an irregular signal. The zeros of ζ are its hidden frequencies.

**The exact statement.** The explicit formula (Riemann, von Mangoldt; in Weil's form [Wei52]) relates a sum over prime powers to a sum over zeros. A zero ρ = β + iγ contributes a term x^ρ^; with x = e^u^ and normalization by e^u/2^, x^ρ−1/2^ = e^(β−1/2)u^ · e^iγu^. The height γ is a frequency, the gap β − ½ a growth of amplitude. This duality is **unconditional**; RH says only that every β equals ½: all modes are pure oscillations.

**Where it breaks.** It is an identity between two functionals tested against a suitable function h, not between two lists. A truncated sum shows peaks near the zeros with a finite resolution (§10 says which resolution suffices).

## 2. The Thermometer: an energy that reads the position of the zeros

**The image.** A microphone records the signal of the primes; we measure its mean energy without letting positive and negative parts cancel. The rate at which this energy rises tells how far the farthest zero lies from the critical line.

**The construction.** c = Λ∗Λ − Λ·log + 2γΛ, C(x) = Σ~n≤x~ c(n), Q(X) = ∫~1~^X^ |C(x)|²/x² dx. Its Dirichlet series G = q² + q′ + 2γq (q = −ζ′/ζ) has a double pole m(m+1)/(s − ρ)² at each zero of multiplicity m (**the double magnifier**); the term 2γΛ makes G regular at s = 1 (**the counterweight**).

**The exact statements.**

- **Theorem A (proved).** ½ limsup log(1 + Q(X))/log X = Θ − ½. Hence RH ⟺ Q(X) = X^o(1)^.
- **Theorem B (proved, under RH).** Q(X) ∼ (S/3)(log X)³; for simple zeros, Q(X) ∼ (4κ/3)(log X)³, κ = 2 + γ − log 4π.
- **Corollary B′ (to be checked).** Under RH, Q(X)/(log X)³ → 4κ/3 if and only if all zeros are simple.
- **Proposition C.** The (log X)² term carries “beats” between neighbouring zeros (conditional; hypotheses H1–H3).

**Where it breaks.** Reading the fever does not lower it: Theorem A is an **exact reformulation** of RH. The pure tone appears only at infinity (measured Q reaches 44–72 % of its asymptotic value up to 4·10⁶).

## 3. The Look-alike: a detector is not a law

**The image.** The look-alike has the same face as ζ (the same functional equation) but not the same engine: no Euler product, and zeros off the line.

**The exact statement.** The Davenport–Heilbronn function [DH36a] [DH36b] (DH) has a zero at 0.8085 + 85.699i; the thermometer rises faster for it (slope 0.56 versus 0.33 for ζ). Q detects misplaced zeros but forbids nothing. **Lesson:** a proof of RH must use the Euler product, since DH has everything else.

**Where it breaks.** DH is not a model of ζ; it is a crash-test witness.

## 4. The reduced model and Castelnuovo positivity [MT58]

**The image.** A scale model in which RH is true, thanks to a geometry the original lacks. It shows what a *necessary* RH looks like.

**The exact statement.** For a curve C over a finite field, RH is a theorem (Hasse [Has36] in genus 1, Weil [Wei48] in general). What makes it necessary lives on the surface C × C: at each floor n of the tower of extensions, an intersection form must be positive. Measured (doc. 28): 425 curves are positive at every floor up to 60; **220 fake twins** have the functional equation and a positive integral Euler product but violate RH, and Castelnuovo positivity unmasks each of them at a finite floor.

**The signature of a proved necessity:** (1) functional equation and Euler product are not enough; (2) a positivity indexed by a tower unmasks the fakes; (3) it holds without margin; (4) it comes from an object one floor up. **ζ shows the first three. It lacks the object.**

**Where it breaks.** There is no known “Spec ℤ × Spec ℤ” playing the role of C × C, and ζ has no Frobenius, hence no obvious tower.

## 5. The Metric

**The image.** A machine (an operator) whose eigenfrequencies would be the zeros. The machine exists; what is missing is the ruler that measures: **the metric**.

**The exact statement.** If H\*M = MH with M positive definite, the spectrum of H is real; with M indefinite, one only gets a symmetry the functional equation already gives. **Positivity of M is the whole substance.** In the reduced model (doc. 32), the operator rebuilt from the point counts separates nothing; only the metric does: positive for all 524 genuine curves, never positive for the 220 fakes.

**Where it breaks.** For ζ, nobody knows where a positive metric would come from, and it is measured only in finite windows.

## 6. The Forbidden passage

**The image.** A door flush with the wall, but bricked up: one can stand exactly at the edge of the RH region with no passage to the other side.

**The exact statement (doc. 29).** In the reduced model, the margin of the form vanishes beyond the number of zeros, and the margin of the object can vanish too, yet no genuine curve leaves the RH region. **Necessity does not keep you away from the edge; it forbids the passage.**

**Where it breaks.** It is formulated and checked in the reduced model; for ζ the question becomes whether an exit can keep an Euler product (§7).

## 7. The Euler archipelago

**The image.** Islands in a rising sea. Each island surrounds a point where an object stands behind the function; the higher one looks, the higher the sea.

**The exact statements (doc. 30).** In the spaces V~q~ of combinations of L-functions sharing one functional equation: first-order rigidity at the Euler points (proved here); any function without zeros in Re s > 1 is an Euler point (a case of Saias–Weingartner [SW09]); islands around the 27 Euler points shrink with height (measured).

**Where it breaks.** The archipelago says **where** RH can live, not **why** it lives there.

## 8. The Link, and what the Selberg analogy really says

**The image.** The discrete step is the exponential of a continuous generator: F = q^D^.

**The exact statement (doc. 32).** For a curve, the zeros are the spectrum of D, and the explicit formula is a trace formula (sum over zeros = sum over closed orbits). For ζ, three differences remain with Selberg's trace formula [Sel56]: the sign of the prime term, the density of zeros, and their statistics (GUE rather than GOE).

**Where it breaks.** ζ has neither period nor natural cadence: **the only step that suits it is the flow** e^tD^.

## 9. The Generator of the primes

**The image.** The primes play the score; the operator is the instrument deduced from it.

**The exact statement (doc. 33).** Traces computed from the primes alone give, through Toeplitz pencils, the translation operator: 284 zeros of ζ with the primes up to 23,862, unit masses, and a metric that is positive for ζ and L and negative for DH exactly at its off-line zeros.

**Where it breaks.** Everything holds in a finite window. **Completeness is the true lock**: showing that all zeros are captured, with the right multiplicity.

## 10. The Heisenberg time

**The image.** A note is heard only once the ear can separate the neighbouring notes.

**The exact statement (doc. 38).** An off-line quadruple at height γ~0~ is detected at the window L~c~ ≈ log(q·γ~0~/2π), the Heisenberg time (ratio 0.95–1.08 for ζ and L); the law doubles in degree 2 (doc. 39). The inertia lemma is proved.

**Where it breaks.** The test is local in height: no finite family of primes watches every height.

## 11. The Meeting of three

**The image.** Three paths crossing at one junction: the collision of two zeros. RH, simplicity and repulsion all pass through it.

**The exact statement (doc. 40; proved, elementary).** The local margin of a pair of zeros is m(s) = 1 − (sin πs/πs)², exactly Montgomery's pair correlation [Mon73]; an off-line pair gives a negative margin. Measured on 1,070 zeros: 4 margins below 0.1, against about 13 for GUE and 320 for Poisson.

**Where it breaks.** The computation uses a two-atom model; neighbours also matter in the true metric.

## 12. The Margin law

**The image.** A crowd that leaves each person room in proportion to the available space.

**The exact statements (doc. 41).** The margin of a pair is the CUE pair correlation; the total margin is Weyl's density [Wey39]; for a conjugate pair it is the Castelnuovo margin, and Sato–Tate has density (2/π) × the margin. At the primes of Δ, the three problems are three theorems (Deligne [Del74], non-collision, Sato–Tate [BGHT11]).

**Where it breaks.** For the zeros of ζ, the law is Montgomery's conjecture: measured, not proved.

## 13. The Foreign families

**The image.** Two crowds crossing without seeing each other.

**The exact statement.** For ζ·L(s, χ₅), all small margins are mixed pairs (one zero of each); in the reduced model, collisions occur exactly at the 18,338 supersingular curves out of 561,258, and RH still holds. **Simplicity is stronger than RH.**

**Where it breaks.** It says no force separates the two families; it does not say what prevents them from meeting.

## 13 bis. The Meeting of n

The margin of n zeros seen through a window is their n-point correlation (doc. 43, proved); the triples of ζ follow it (measured).

## 13 ter. The Virtual surface

**The image.** A surface whose intersections are known without knowing its points. On a curve, the corpus margin is the intersection form of C × C; RH is the Hodge index. For ζ, the same form computed from the primes has one positive direction; DH has extra ones (doc. 46). **Where it breaks:** the surface of the integers does not exist; only its shadow is known.

## 13 quater. The Auxiliary function and Frobenius

**The image.** A net stretched over all points at once, which tears if there are too many; it holds only thanks to Frobenius x ↦ x^p^, whose derivative vanishes. Measured: it unmasks every fake twin (doc. 47) and fails with the identity or a permutation (doc. 48). **What is missing for ζ:** an “absolute Frobenius” on the integers.

## 13 quinquies. Two thirds

Counting distinct zeros through the “thickness” of their Gram matrix gives Alpöge–Furman's theorem (at least 67.25 % of zeros simple and on the line [AF26]); the same computation on our zeros gives 56 % at the proved window (doc. 49).

## 13 sexies. Lego bricks and windows

**The image.** The wall cannot be inspected all at once; windows of increasing width are certified brick by brick, each window checked in full.

**What is certified (docs. 71, 73, 75).** For all test functions supported in [−S, S] with vanishing exponential moments, the Weil form is positive with a margin: at least ‖f‖²/25 up to S = 0.347, ‖f‖²/250 up to 1/2, (3/10000)‖f‖² up to 11/20, on the whole infinite space, without zeros or RH.

**What is measured (doc. 81).** Zhu [Zhu26] certifies positivity for all functions up to 0.8; the corpus recovers his values by another method. The smallest value collapses: 10⁻⁶ at 0.5, 10⁻¹⁷ at 0.8; on zero-moment functions it stays much larger (5·10⁻¹² at 0.8).

**Where it breaks.** Positivity for all windows *is* RH, and the margin collapses too fast to advance brick by brick. The corpus windows are, in range, already covered by Zhu's: their contribution is a stronger margin on a subspace, not a wider window.

## 13 septies. The coupling debt

**The image.** A house built well room by room can still collapse if the shared walls pull on one another.

**What is proved (docs. 70, 74, 79).** The Weil form splits exactly into a continuous model and a signed arithmetic fluctuation; the continuous model alone can be negative. An exact Schur complement gives the coupling debt; one energy pays all primes once (joint payment); and the best guard using only support, mass and first moment meets an asymptotic obstruction for fixed-ratio blocks.

**Where it breaks.** The debt can be written, not bounded for a family covering all test functions. This is lock W10 of the logical table.

## 13 octies. Amplification: the head and the tail

**The image.** An orchestra where every front-desk player is under control, but the many players at the back each play slightly out of tune.

**What is proved (essay V6.55).** Exact restitution of the Möbius sum; the head of conductors q ≤ H is bounded at every scale. **Open:** the tail of large conductors with its signs μ(q). A bound R ≤ C X³ (1 + log X)^k^ would give no zeros for Re s > 3/4, a real step but still far from RH. The generic sieve is not enough.

## 13 nonies. Counts, degrees, square

**The image.** Three identity checks, ever stricter: count the pieces (the points); weigh each transformation (its degree, the size of its kernel); ask for a notary's signature, the trace of a square, “u times its adjoint”.

**What is proved and measured (doc. 80).** The 425 genuine curves pass all three checks. Some fake twins already fail the second (an isogeny would have degree −1). But **119 fake twins pass the first two** and still violate RH: only the square stops them. For a genuine curve, the square comes from a polarization of its Jacobian (Rosati positivity), an object with an ample class.

**For ζ.** The first two checks are passed (Λ(n) ≥ 0; no real zero in ]0, 1[). The third is RH itself. **What is missing is not a count; it is a square.**

**Where it breaks.** The “notary” for ζ does not yet exist: the involution playing the adjoint is known (f ↦ f̄(−x)), not the reason its trace would be positive.

## 14. Proved, measured, assumed

| Image | Proved | Measured | Assumed |
|---|---|---|---|
| Thermometer (§2) | Theorems A, B (under RH); B′ to be checked | Q at 44–72 % of its asymptote | — |
| Look-alike (§3) | — | slopes 0.56 (DH), 0.33 (ζ) | — |
| Reduced model (§4) | Weil, Castelnuovo (classical) | 425 curves; 220 fake twins | an analogue of C × C for ζ |
| Metric (§5) | M > 0 ⇒ real spectrum (classical) | only the metric separates | the origin of ζ's metric |
| Forbidden passage (§6) | form margin zero beyond 2g | exact census | same mechanism for ζ |
| Archipelago (§7) | first-order rigidity; RH ⇒ Euler point | islands, slope −0.77 | GRH at the Euler points |
| Generator (§9) | — | 284 zeros of ζ without injected zeros | convergence of the operator |
| Heisenberg (§10) | inertia lemma | ratio 0.95–1.08 | mechanism of the threshold |
| Meeting of three (§11) | margin = 1 − sinc²(πs) | 4 margins < 0.1 on 1,070 zeros | — |
| Windows (§13 sexies) | certificates up to 11/20; Zhu up to 0.8 (cited) | λ* from 10⁻⁶ to 10⁻¹⁷ | — |
| Coupling debt (§13 septies) | exact split, Schur, obstructions | — | a sign law on a covering family |
| Amplification (§13 octies) | restitution, bounded head | — | bound on the large tail |
| Counts, degrees, square (§13 nonies) | elementary proposition; Rosati (classical) | 119 fakes with positive degrees | a polarization analogue for ζ |

## 15. Reading according to the hypothesis

- **The reduced model** shows what a necessary RH looks like: a positivity indexed by a tower, without margin, carried by an object one floor up. ζ shows its observable signatures, except the object.
- **The forbidden passage** says how such necessity acts: it bricks up the exit rather than keeping one away from the edge.
- **The Euler archipelago** gives the exact form of the hypothesis in a class of spaces: RH lives only where an object stands behind the function.
- **The link and the generator** locate the gap: operator and symmetry can be rebuilt from the primes; the positive metric is missing.
- **The windows** show the square is there wherever one looks, and that it becomes extremely thin as the window widens.
- **Counts, degrees, square** names what the object must supply: not a count, already positive for ζ, but a square, as a polarization does for a curve.

All this is compatible with the hypothesis and sharpens it. Nothing proves it: the larger object, for ζ, has not been built.

## 16. Mini-glossary

| Term | Meaning |
|---|---|
| ζ(s), non-trivial zero | The Riemann zeta function; its zeros ρ = β + iγ in the strip 0 < β < 1. |
| Critical line, RH | The line β = ½; RH states that all non-trivial zeros lie on it. |
| Λ(n) | von Mangoldt function: log p if n is a power of p, 0 otherwise. |
| Euler product | Writing the function as a product over primes; DH has none. |
| Reduced model | Curves over finite fields, where RH is a theorem. |
| Metric, margin | The Gram matrix measuring lengths; what remains of its positivity before losing it. |
| Weil form, window | The quadratic form of the explicit formula; a window is the support [−S, S] of the test functions. |
| Polarization, Rosati | An ample class on a Jacobian; the involution whose trace positivity gives RH for curves. |
| Heisenberg time | log(q·γ~0~/2π): the window that resolves the mean gap at height γ~0~. |

## 17. What the images do not say

1. **They do not say why the zeros are on the line.** No image contains the law that would impose it on ζ.
2. **They say nothing beyond the window.** Every measurement on ζ is at finite height, and every Weil certificate on a bounded support (11/20 for the corpus, 0.8 for Zhu).
3. **They do not transfer from the model to the original.** A matching feature in the model is an indication, not a transfer.
4. **They do not replace positivity by a name.** “Positive metric”, “margin”, “square” locate Weil's lock; they do not open it.
5. **They do not all have the same status.** The table of §14 makes the difference; an image does not.
6. **They do not replace review.** Theorems A and B and Corollary B′ await a specialist.

**In one sentence.** The programme can build instruments that read exactly where the zeros are, and it has measured, where RH is proved, what makes it necessary; it cannot yet build, for ζ, the object that would carry that necessity.

*Bracketed keys such as [Wei48] refer to the [ranked references](../../REFERENCES_RANKED.md) and to the full register ([document 42](../42_REGISTRE_DES_SOURCES.md)).*
