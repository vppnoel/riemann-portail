# Reading the Lean proof: human-readable notes

*Vincent P. P. NOËL, MSc Cogn. Neurosci. — 23 November 2026. Written with Claude (Anthropic), checked by ChatGPT (OpenAI), accepted by the author. Unofficial reading aids, not referee reports. Errors are ours; please report them.*

On 20 November 2026, L. Alpöge announced a proof of the Generalized Riemann Hypothesis, released as a Lean 4 formalisation (`leanprover-community/riemann-hypothesis`). These notes rewrite the **analytic part** of that proof for a human reader, step by step, each step linked to the Lean declaration it corresponds to, at the fixed commit `51d9b1a`.

| File | Language | What it proves | Status |
|---|---|---|---|
| [`02_FROM_STAR_TO_GRH_EN.md`](02_FROM_STAR_TO_GRH_EN.md) | English | From the windowed bound (⋆) to GRH and RH: windowed Landau for a positive family, the level criterion, the order of choices, all primitive characters, imprimitive characters, the strip and ζ. Names and locates the three formal inputs that produce (⋆), and traces the chain from `Main.lean`. | Checked against the Lean code; **(⋆) itself is admitted**, not proved here |
| [`01_LANDAU_FENETRES_ZETA_FR.md`](01_LANDAU_FENETRES_ZETA_FR.md) | French | The windowed Landau step for ζ alone, in five steps, with 40 links to the Lean code, and an exact computation of the guide's numerical figure (0.023 √y up to 10⁷: the maximum is 0.022681). | Checked and accepted |
| [`03_POLES_DOUBLES_FENETRES_FR.md`](03_POLES_DOUBLES_FENETRES_FR.md) | French | An analogue outside the Lean proof, for a statistic with **double** poles (from this corpus, article 1): a one-sided *floor* on late windows excludes zeros to the right of θ, and conversely, with no such zero, \|H(y)\| = O(y^θ log y). Hence RH ⇔ H(y) = O(√y log y). | Checked and accepted. The direct implication is **classical**: it follows from Kaczorowski and Pintz (1986, Theorem 1), who even give overshoots of both signs in every late window. The note proves it in the Lean proof's style; the converse at the threshold is the part written out here |

**Scope.** The notes cover the analytic steps; (⋆), the hard arithmetic estimate (guide §§ 4–7), is taken as given. The third note is an equivalent reformulation of RH.

**How they were produced.** Each note was written by Claude with a forecast registered before the work, then checked by ChatGPT, which did not write it. Each check found real errors, which were corrected before acceptance:
- in the first note, a geometric step confused horizontal and Euclidean distance;
- in the second, a definition (`HostExW`) was stated too broadly, and two links pointed at the wrong declaration;
- in the third, an earlier version of the converse moved a contour where the integral did not converge.

The record of these errors is part of the method: two AI systems checking each other are not two independent checks, and they are not a specialist.

**Two precisions** from the check of the third note, to keep in mind:
- in step 1(a), the crude bound to use is \|H(y)\| ≪ y log³(2y) ≪ y², which is all the proof needs;
- the equivalence theorem is proved unconditionally; it is the *bound* H(y) = O(√y log y) that is equivalent to RH.
