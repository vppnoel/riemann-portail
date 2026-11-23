# Note: the announced proof of the Riemann Hypothesis (November 2026)

*Vincent P. P. NOËL, MSc Cogn. Neurosci. — 22 November 2026, corrected 23 November 2026 (see « Corrections » at the end). This note does not change any document of the corpus: each of them describes the state at its date.*

## What happened

On 20 November 2026, Levent Alpöge (Anthropic) announced a proof of the Generalized Riemann Hypothesis for Dirichlet L-functions, and so of the Riemann Hypothesis, obtained with Claude. The proof was released as a Lean 4 formalisation (about 175,000 modules), with a short guide.

Within two days:

- it was built independently (A. Sutherland, MIT; a separate build on the LUMI supercomputer, with matching hashes);
- it was replayed by independent kernels (nanoda, con-leche) and found to use only Lean's three standard axioms;
- the question raised by K. Buzzard, whether the Lean *statement* is really RH/GRH, was answered positively by E. Glazer and by the Lean and Mathlib communities, who issued a joint statement of full confidence.

What does not exist yet: a proof a human can read in full (the figure of over 250,000 pages that circulated is Alpöge's own, about a draft write-up he had generated automatically; T. Bloom relayed it, then clarified that it does not measure the length of a careful human exposition), peer review, or publication in a journal. The first human expositions (M. Rubinstein, R. Zhang, the "guide to its architecture") are partly AI-assisted readings of the Lean code, and their authors say so.

## Why it works, as far as I understand it

This is my reading of those expositions, not a verified summary.

1. **Zeros become a one-sided bound on primes.** Take a smoothed prime sum G(x), built from Λ(n) with a ramp weight (x/n − 1)₊. A zero with real part β > 1/2 forces, for every θ with 1/2 < θ < β, the centred statistic G(x) to exceed any multiple of x^θ somewhere in every late window (a localised version of Landau's theorem; the centring term matters, and the lemma does not give the exponent θ = β itself). So it is enough to show the *upper bound* G(x) ≤ x^(1/2+ε) on windows [Y, Y^(3/2)], for arbitrarily large Y. Taking a family of L-functions with positive weights prevents zeros from different functions from cancelling.

2. **The upper bound comes from integrality.** A nonzero integer divisible by many prime powers must be large: the sum of e_p log p is at most log|Δ|. The proof builds arithmetic objects (periods of automorphic forms, via theta lifts over a CM field) whose divisibility at each prime p encodes the prime sum G, and whose archimedean size can be computed (Chowla–Selberg, Bost's slope inequality). "Too much divisibility" would contradict "known size". This turns the bound on G into a statement about integers.

3. **Multiplicity is manufactured.** One theta lift does not give enough divisibility. A chain of m lifts adds the gains, much as an auxiliary polynomial vanishing to high order does in Stepanov's elementary proof of the Riemann Hypothesis for curves over finite fields. The expositions call the proof "a descendant of Stepanov's": the tower of finite field extensions is replaced by a cyclotomic tower, and Iwasawa theory controls the denominators.

4. **Why exactly 1/2.** The two main errors have sizes x/m and m. They balance at m ≈ √x, which gives the exponent 1/2. In this reading, the critical line is the balance point between the cost of building multiplicity and the gain it brings.

My summary in one sentence: **RH holds because primes are encoded in integers that cannot be at once too small and too divisible, and because enough multiplicity can be built to make that constraint sharp.**

## What this changes for the corpus

If the proof stands:

- **Theorems A and B (Paper 1) become unconditional.** The growth exponent 2(Θ − ½) of Q(X) is 0, and Q(X) ∼ (S/3)(log X)³. The criterion then reads: the limit of Q(X)/(log X)³ equals 4κ/3 *if and only if all zeros of ζ are simple*. Simplicity remains open, and the proof does not claim it. Paper 1 keeps its object, which is now cleaner.
- **Document 80 ("what is missing is not a count but a square") needs a nuance.** For curves, RH has two proofs: Weil's, through the positivity of a square (Rosati), and Stepanov–Bombieri's, through counting with multiplicity. The announced proof follows the second route. The missing object was not necessarily a square; it may have been multiplicity in bulk.
- **The Weil-positivity track (documents 71–76) is not the route that was taken.** The positivity used by the proof is the positivity of family weights, not Weil positivity on test functions. These documents stay as a record of a reasonable track that turned out not to be the one.
- **The working hypothesis of the programme still stands, and is sharper.** I asked what larger necessity makes RH necessary. A machine-checked proof shows *that* RH is true. The expositions suggest a candidate for the *why*: integrality and the product formula, applied to automorphic periods. Understanding that properly is now the most interesting part of the question, and it is open.

## For the study of bias

This episode is also data. A corpus built over months with AI systems took a reasonable direction (Weil positivity, the missing square) that was not the one that worked. Meanwhile an AI system, guided by a specialist, produced a proof that no human has yet read in full and that is trusted because a machine checked it. Both situations raise the same question from opposite sides: what does it mean to *know* a mathematical result when understanding and verification come apart?

## Sources

- [Washington Times, 20 Nov 2026](https://www.washingtontimes.com/news/2026/nov/20/riemann-hypothesis-may-proved-ai-mathematician/)
- [Scientific American (via Yahoo), updated 21 Nov 2026](https://www.yahoo.com/news/science/articles/ai-riemann-hypothesis-proof-almost-210000837.html)
- [Mathematicians' reactions (OfficeChai)](https://officechai.com/ai/how-mathematicians-have-reacted-to-claimed-riemann-hypothesis-proof-by-anthropics-levent-alpoge/)
- [Independent build and axiom audit on LUMI](https://github.com/aapolipponen/rh-lean-check-lumi)
- [M. Rubinstein et al., the proof explained for ζ (draft, 21 Nov 2026)](https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/zeta-paper.pdf)
- [R. Zhang, a preliminary note on the proposed proof (21 Nov 2026)](https://www.ihes.fr/~rzhang/files/GRH%20note.pdf)
- [A guide to the architecture of the proof](https://nasqret.github.io/riemann-rev/guide/proof-guide.pdf)

---

*AI use: drafted with Claude from published expositions and my instructions. I have read it and stand behind every sentence; the reading of the proof is secondary and may be corrected.*

## Corrections (23 November 2026)

An adversarial review of this note was carried out within the research programme by a second AI system (ChatGPT, OpenAI), with a forecast registered before the analysis. It found two errors, corrected above:

1. **The 250,000-page figure was misattributed.** The first version attributed to T. Bloom an estimate of the length of a human-readable proof. The figure is Alpöge's, about a draft write-up he had produced automatically; Bloom relayed it and then said it does not measure a careful human exposition.
2. **The Landau step was stated too strongly.** The first version said that a zero with real part θ forces the overshoot at the exponent θ itself. The localised Landau lemma gives the overshoot only for exponents strictly below the real part of the zero, β = Re ρ: for every θ with 1/2 < θ < β. A human-readable proof of this step, checked against the Lean code, is now available (see the update of 23 November 2026 in the README).

The same review marks several other statements of this note as imprecise rather than wrong (attributions within the community discussion, the exact scope of the independent checks). They are left as written, pending the author's decision on the full review.
