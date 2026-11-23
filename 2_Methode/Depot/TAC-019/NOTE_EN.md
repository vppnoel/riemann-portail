# From the windowed bound (⋆) to GRH: the analytic part of the announced proof, in human-readable form

*Vincent P. P. NOËL, MSc Cogn. Neurosci. (independent, amateur) — written with Claude (Anthropic) — 23 November 2026. Unofficial reading aid. Lean source consulted: `leanprover-community/riemann-hypothesis`, commit `51d9b1a28026d458aef9c9af3df8b083276e3d2d`. Declaration names are given in brackets. Errors are ours; please report them.*

## 0. Scope

The announced proof has one hard arithmetic estimate, (⋆) in the architecture guide (§§4–7, packaged in Lean as `TopG` together with the existence of hosts). This note does **not** treat (⋆). It gives a complete human-readable proof of everything **after** it:

  (⋆) for every primitive ψ  ⟹  no zero of any Dirichlet L-function with Re s > ½  ⟹  zeros in the strip lie on Re s = ½  ⟹  RH.

Every step is matched to the Lean declaration that checks it. The core analytic lemma (the windowed Landau theorem) is written out in full for ζ in a companion note (`TAC-017/PREUVE.md`, in French). Here we give the changes needed for families. The proofs of the lemmas below were read in the Lean source, except where marked *(statement only)*.

## 1. Objects

**Primitive characters** [`Formalism.HC.PChar`]. A PChar is a primitive Dirichlet character ψ of conductor N. `PChar.one` is the trivial character mod 1, whose L-function is ζ. `PChar.of χ` is the primitive character inducing χ.

**Levels** [`Formalism.HC.Level`, `KSet`, file `TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean`]. A level Λ consists of:
- a finite set KEPT of PChars, containing `one` and closed under ψ ↦ ψ⁻¹ ;
- an optional distinguished real odd character `psK` ;
- an integer o.

Its weights are wt(ψ) = 1 if ψ = psK, and (3o + 1)⁻¹ otherwise [`Level.wt`]. Its statistic is [`Level.Gm`]

  Gm(y) = G(y) + Σ_{ψ ∈ KEPT, ψ ≠ 1} wt(ψ) · Re g_ψ(y),

with the centred ramp sums of guide §2 [`Deduction.G`, `Deduction.Gchi`]:
- G(y) = Σ_{n≤y} Λ(n)(y/n − 1) − y(log y − 1 − γ) ;
- g_ψ(y) = Σ_{n≤y} Λ(n)ψ(n)(y/n − 1) + y·L′/L(1, ψ) for ψ ≠ 1.

**The cyclic level of ψ** [`Level.cyc`, `Level.ofSub`]. KEPT is the set of primitive characters inducing the powers of ψ, o is the order of ψ, and there is no psK. Its weights are therefore 1 on the trivial character and 1/(3o + 1) on the others. These are the positive weights P(ψ) of guide §3. Moreover ψ ∈ KEPT [`Level.mem_cyc`].

## 2. Theorem 1 — windowed Landau for a positive family

**Statement** [`Deduction.zeroFree_of_rpow_window`]. Let F be a finite family of characters χ_i with weights a_i > 0, where each χ_i is either the trivial character mod 1 or non-trivial [`Deduction.CharFamily`, field `adm`]. Let G_F(y) = Σ a_i Re g_{χ_i}(y) [`Deduction.Gm`]. Let 0 < θ < 1, δ > 0 and C be real. Suppose that for every Y₀ there is Y ≥ Y₀ with G_F(y) ≤ C y^θ for all y ∈ [Y, Y^(1+δ)]. Then no L(s, χ_i) vanishes for Re s > θ.

**Proof.** It is the proof for ζ (companion note, steps 1–5), with one change in step 1. We have Re g_χ = (g_χ + g_χ̄)/2, so the Laplace transform of g_F(u) = G_F(eᵘ) is [`poleData`]

  Φ_F(s) = Σ_i (a_i/2) · ( Φ_{χ_i}(s) + Φ_{χ_i⁻¹}(s) ),

where Φ_χ is the transform of g_χ [`poleData_char`]. Φ_χ has a simple pole at each zero ρ of L(s, χ), with residue m_χ(ρ) · (−1/(ρ(ρ − 1))), where m_χ is the multiplicity.

Hence Φ_F is meromorphic on Re s > 0, with poles exactly at the zeros of the L(s, χ_i) and of their conjugates [`zeroSet`]. The residue at ρ is

  c(ρ) = −(1/(ρ(ρ − 1))) · Σ_i (a_i/2) (m_{χ_i}(ρ) + m_{χ_i⁻¹}(ρ)).

The sum is a positive combination of non-negative integers, at least one of which is positive. So **c(ρ) ≠ 0: zeros of different members cannot cancel**, which is guide §3, idea 1. If ρ is real, ρ(ρ − 1) < 0 and c(ρ) > 0. The rest of the proof uses only these properties, packaged as `PoleData`, and is the abstract lemma [`Deduction.landau_window`]. In particular, a real zero close to 1, a "Siegel zero", is handled by the same argument as any other real pole (case 1 of step 5): **there is no separate treatment of Siegel zeros**. ∎

## 3. Theorem 2 — every level satisfies the windowed criterion

**Statement** [`UpperTheory.Comparison₂.formB`; definitions `Level.FormB`, `Level.FormBAt`, `HasWindows`, file `TotientGaloisClasses/Window.lean`]. Let Λ be a level, λ > 1 and 0 < θ < 1. Suppose that for every y₀ there is Y ≥ y₀ such that Λ.Gm(x) ≤ x^θ for all x ∈ [Y, Y^λ]. Then every ψ ∈ KEPT has L(s, ψ) ≠ 0 for Re s > θ.

**Proof.** Form the family F indexed by KEPT, with the weight of ψ equal to 1 if ψ is trivial and Λ.wt(ψ) otherwise. All weights are positive, and every member is admissible: a primitive principal character has conductor 1. Then G_F = Λ.Gm, by unfolding the definitions. Apply Theorem 1 with δ = λ − 1 and C = 1. ∎

*Remark.* Only the positivity of the weights is used. The specific values 1 and 1/(3o + 1) play no role here: they come from the averaging of guide §5.

## 4. Theorem 3 — the order of choices

**Statement** [`Formalism.HC.level_of_tiedWin`, file `TotientGaloisClasses/TopWin.lean`]. Let Λ be a level and λ > 1. Suppose there are constants e_D, e_L and ε₁ > 0 such that, for every 0 < ε < ε₁, there is a set of scales W_ε with the following two properties:
- it contains windows [Y, Y^λ] for arbitrarily large Y ;
- Λ.Gm(x) ≤ x^(½ + (e_D + e_L + 7)ε) for all large x ∈ W_ε.

Then every ψ ∈ KEPT has no zero with Re s > ½.

*(In Lean, W_ε is the window set of an auxiliary "family" `Fm` produced by the arithmetic supply, and the inequality is `ChebyshevInequalityOnWindows`; we have stated only what the proof uses.)*

**Proof.** Let ψ ∈ KEPT and Re s > ½. Put μ = min(Re s − ½, ½) > 0.
- Choose ε ∈ (0, ε₁) with (e_D + e_L + 7)ε ≤ μ/2 [`exists_small_eps`].
- Put θ = ½ + μ/2. Then ½ < θ < Re s and θ < 1.
- For large x in the windows, Λ.Gm(x) ≤ x^(½ + μ/2) = x^θ, since x ≥ 1.

So the hypothesis of Theorem 2 holds, and L(s, ψ) ≠ 0. ∎

This is the guide's "θ is chosen after the zero, and ε after θ". The guide writes the exponent as ½ + 9ε; the Lean statement carries the constants e_D + e_L + 7 explicitly. This is a difference of presentation only: the argument works for any fixed constant.

## 5. Theorem 4 — all primitive characters

**Statement** [`UpperTheory.Top.zeroFreeAll_of_topG`, `zeroFreeOn_of_tiedWin_cyc`, `zeroFreeOn_of_levels`]. If the arithmetic supply `TopG` holds, and hosts exist on windows for every ψ [`HostExW`], then every primitive ψ has L(s, ψ) ≠ 0 for Re s > ½ [`ZeroFreeAll`].

**Proof.** For each ψ, apply Theorem 3 to the cyclic level Λ = Level.cyc ψ, which contains ψ.
- The hypothesis of Theorem 3 is supplied by `TopG`, which provides e_D, e_L, ε₁ and the families; this is the content of (⋆) and is **admitted here**.
- The conclusion for the members of Λ is Theorem 3; it applies to ψ itself because ψ ∈ KEPT. ∎

## 6. Theorem 5 — imprimitive characters, the strip, and ζ

**(a) Imprimitive characters** [`UpperTheory.Top.imprimitive`]. If every primitive ψ is zero-free on Re s > ½, then so is every χ, at every s with Re s > ½ and (χ ≠ 1 or s ≠ 1). Indeed, L(s, χ) = L(s, χ*) · Π_{p | N} (1 − χ*(p) p^(−s)), where χ* = `PChar.of χ`. Each Euler factor is non-zero for Re s > 0, because |χ*(p) p^(−s)| < 1 [`Claim.factor_ne_zero`].

**(b) The strip** [`Claim.strip`]. Suppose L(s, χ) = 0 with 0 < Re s < 1.
- If Re s > ½, this contradicts (a).
- If Re s < ½, then L(s, χ*) = 0 [`Claim.prim_zero`], because the Euler factors do not vanish. The functional equation of the completed L-function of the primitive χ*, together with the non-vanishing of the gamma factor for Re > 0, gives L(1 − s, χ*⁻¹) = 0 [`Claim.prim_reflect`]. Since Re(1 − s) > ½, this contradicts (a).

Hence Re s = ½.

**(c) ζ** [`Claim.zeta`, `riemannHypothesis`]. A zero s of ζ with s ≠ 1 and s not a trivial zero −2(n + 1) has Re s > 0: if Re s ≤ 0, the gamma factor does not vanish, so the completed zeta function vanishes at s, hence ζ(1 − s) = 0 with Re(1 − s) ≥ 1, which is impossible. ζ has no zero with Re s ≥ 1. So 0 < Re s < 1, and (b) applies with the trivial character mod 1. This is Mathlib's `RiemannHypothesis`. ∎

*Not traced.* In `Main.lean`, the half-plane statement is the term `UpperTheory.FinalTheorems.everyCharacter`, obtained in `CharacterBoxes/MainConclusion.lean` from `every_character_of_literature_of_vWin`. We did not read how that term calls Theorem 4 and (a). The statements match exactly: `EveryCharacter` and the conclusion of (a) are the same proposition.

## 7. What this part uses, and what it does not

**Uses:**
- the Mellin transform of the ramp ;
- the logarithmic derivative of L near its zeros (simple poles, residue = multiplicity) ;
- a crude growth bound |g_χ(y)| ≪ y² [`Gchi_growth`] ;
- Cauchy's estimates ;
- a Chernoff tail bound ;
- Euler factors at p | N ;
- the functional equation for primitive characters.

**Does not use:**
- zero-density estimates or zero counting ;
- any bound on L′/L off the zeros ;
- any special argument for Siegel zeros ;
- the positivity of the Dirichlet coefficients: the positivity used is that of the **multiplicities of zeros** and of the **family weights** ;
- anything automorphic.

## 8. Guide, Lean, and this note

| Point | Guide | Lean (51d9b1a) | Status |
|---|---|---|---|
| Landau proposition | contrapositive form, "for every C" | `zeroFree_of_rpow_window`: hypothesis form, any C, δ, θ ∈ (0, 1) | equivalent; Lean is slightly more general |
| Weights of P(ψ) | 1 and 1/(3o + 1) | `Level.wt`, with an optional psK of weight 1 | same for `Level.cyc`; only positivity is used |
| Exponent in (⋆) | ½ + 9ε | ½ + (e_D + e_L + 7)ε, constants existential | presentation only |
| Windows | [Y, Y^(3/2)] | `HasWindows S λ`, any λ > 1 | Lean is more general |
| Siegel zeros | covered by positivity | no separate code; case 1 of `landau_window` | as the guide says |
| Imprimitive χ | §1, before | `imprimitive`, applied **after** `ZeroFreeAll` | the order differs; the content is the same |

*Disclosure.* This note was drafted by Claude (Anthropic), the AI system used to produce the proof, within an amateur research corpus. It is offered as a reading aid; it is not a referee report. The companion proof for ζ (TAC-017) and this note are being cross-checked by a second AI system (ChatGPT), and they have not been reviewed by a human specialist.
