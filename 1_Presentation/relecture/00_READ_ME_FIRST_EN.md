# Review package: Theorems A and B, and the Euler Archipelago note

**Author:** Vincent Noël (research programme on the Riemann Hypothesis, corpus version 6.13, October 2026).
**No proof of the Riemann Hypothesis is claimed.** Theorem B is conditional on RH.

## What this package contains

| File | Result | Internal pre-review verdict |
|---|---|---|
| [`RELECTURE_THEOREME_A_EN.md`](RELECTURE_THEOREME_A_EN.md) | Theorem A: with C(x) = Σ_{n≤x} c(n), c = Λ∗Λ − Λ·log + 2γΛ, and Q(X) = ∫₁^X \|C(x)\|² x⁻² dx, one has ½·limsup log(1+Q(X))/log X = Θ − ½ (unconditional). | Correct; ready after small fixes; presented as a proposition with a standard method (analogue of the classical characterisation of Θ by ψ(x) − x). |
| [`RELECTURE_THEOREME_B_EN.md`](RELECTURE_THEOREME_B_EN.md) | Theorem B: under RH, Q(X) ∼ (S/3)(log X)³ with S = Σ_ρ m²(m+1)²/\|ρ\|²; S = 4κ, κ = 2 + γ − log 4π, for simple zeros. | Correct; ready after small fixes; a Cramér-type transposition to a double pole. New corollary to be checked: under RH, S ≥ 4κ with equality iff all zeros are simple. |
| [`RELECTURE_ARCHIPEL_EN.md`](RELECTURE_ARCHIPEL_EN.md) | First-order rigidity at Euler points in spaces of combinations of L(s, χ) with a common functional equation; "no zero in Re s > 1 ⟺ Euler point" in these spaces. | Correct in substance after fixes; the corollary is an immediate special case of Saias–Weingartner (2009, Thm 2), not new; the rigidity proposition is elementary. |

## Status of these notes

They were prepared on 10 October 2026 as an **internal pre-review**: three independent checks, each re-deriving one proof step by step, with short numerical sanity checks and literature searches. This is not a peer review. Every unverified citation is marked as such in the notes.

## The questions we would most like answered

1. **Theorem A.** Is the upper-bound step complete as written (truncated Perron at half-integers, contour shift to Θ + ε/2 with G ≪ log²|t|)? Is A a routine consequence of the classical results on ψ(x) − x, and is there a citable reference?
2. **Theorem B.** Is B, or a general Cramér-type theorem for poles of order k on Re s = ½, already in the literature? Do you accept that the proof needs no information on gaps between zeros? Is the corollary "S = 4κ iff all zeros are simple" correct and known?
3. **Archipelago.** Is "immediate corollary of Saias–Weingartner, Thm 2" the right attribution? In degree 2 (S₂₄(SL₂(ℤ))), is first-order rigidity at Hecke eigenforms known or immediate?
