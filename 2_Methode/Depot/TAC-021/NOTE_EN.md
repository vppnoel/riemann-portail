# From the windowed bound (⋆) to GRH: the analytic part of the announced proof, in human-readable form

*Vincent P. P. NOËL, MSc Cogn. Neurosci. (independent, amateur) — written with Claude (Anthropic) — 23 November 2026, revised the same day after an independent check. Unofficial reading aid. Lean source consulted: `leanprover-community/riemann-hypothesis`, commit `51d9b1a28026d458aef9c9af3df8b083276e3d2d`. Declaration names are given in brackets. Errors are ours; please report them.*

## 0. Scope

The announced proof has one hard arithmetic estimate, (⋆) in the architecture guide (§§4–7, packaged in Lean as [`TopG`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/CharacterBoxes/ZeroFreeAllOfTopG.lean#L16) together with the existence of hosts). This note does **not** treat (⋆). It gives a complete human-readable proof of everything **after** it:

  (⋆) for every primitive ψ  ⟹  no zero of any Dirichlet L-function with Re s > ½  ⟹  zeros in the strip lie on Re s = ½  ⟹  RH.

Every step is matched to the Lean declaration that checks it. The core analytic lemma (the windowed Landau theorem) is written out in full for ζ in a companion note (`TAC-017/PREUVE.md`, in French). Here we give the changes needed for families. The proofs of the lemmas below were read in the Lean source, except where marked *(statement only)*.

## 1. Objects

**Primitive characters** [[`Formalism.HC.PChar`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/PrimePairSizeCondition.lean#L11)]. A PChar is a primitive Dirichlet character ψ of conductor N. `PChar.one` is the trivial character mod 1, whose L-function is ζ. `PChar.of χ` is the primitive character inducing χ.

**Levels** [[`Formalism.HC.Level`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean#L12), [`KSet`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/PrimePairSizeCondition.lean#L37), file `TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean`]. A level Λ consists of:
- a finite set KEPT of PChars, containing `one` and closed under ψ ↦ ψ⁻¹ ;
- an optional distinguished real odd character `psK` ;
- an integer o.

Its weights are wt(ψ) = 1 if ψ = psK, and (3o + 1)⁻¹ otherwise [[`Level.wt`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean#L36)]. Its statistic is [[`Level.Gm`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean#L38)]

  Gm(y) = G(y) + Σ_{ψ ∈ KEPT, ψ ≠ 1} wt(ψ) · Re g_ψ(y),

with the centred ramp sums of guide §2 [[`Deduction.G`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/CharFamily.lean#L25), [`Deduction.Gchi`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/CharFamily.lean#L19)]:
- G(y) = Σ_{n≤y} Λ(n)(y/n − 1) − y(log y − 1 − γ) ;
- g_ψ(y) = Σ_{n≤y} Λ(n)ψ(n)(y/n − 1) + y·L′/L(1, ψ) for ψ ≠ 1.

**The cyclic level of ψ** [[`Level.cyc`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean#L118), [`Level.ofSub`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean#L102)]. KEPT is the set of primitive characters inducing the powers of ψ, o is the order of ψ, and there is no psK. Its weights are therefore 1 on the trivial character and 1/(3o + 1) on the others. These are the positive weights P(ψ) of guide §3. Moreover ψ ∈ KEPT [[`Level.mem_cyc`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean#L120)].

## 2. Theorem 1 — windowed Landau for a positive family

**Statement** [[`Deduction.zeroFree_of_rpow_window`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/ZeroFreeOfRpowWindow.lean#L15)]. Let F be a finite family of characters χ_i with weights a_i > 0, where each χ_i is either the trivial character mod 1 or non-trivial [[`Deduction.CharFamily`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/CharFamily.lean#L28), field `adm`]. Let G_F(y) = Σ a_i Re g_{χ_i}(y) [[`Deduction.Gm`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/CharFamily.lean#L40)]. Let 0 < θ < 1, δ > 0 and C be real. Suppose that for every Y₀ there is Y ≥ Y₀ with G_F(y) ≤ C y^θ for all y ∈ [Y, Y^(1+δ)]. Then no L(s, χ_i) vanishes for Re s > θ.

**Proof.** It is the proof for ζ (companion note, steps 1–5, in its corrected version), with one change in step 1. We have Re g_χ = (g_χ + g_χ̄)/2, so the Laplace transform of g_F(u) = G_F(eᵘ) is [[`poleData`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/poleData.lean#L252)]

  Φ_F(s) = Σ_i (a_i/2) · ( Φ_{χ_i}(s) + Φ_{χ_i⁻¹}(s) ),

where Φ_χ is the transform of g_χ [[`poleData_char`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/poleData.lean#L141)]. Φ_χ has a simple pole at each zero ρ of L(s, χ), with residue m_χ(ρ) · (−1/(ρ(ρ − 1))), where m_χ is the multiplicity.

Hence Φ_F is meromorphic on Re s > 0, with poles exactly at the zeros of the L(s, χ_i) and of their conjugates [[`zeroSet`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauZeroFreeCriterion.lean#L15)]. The residue at ρ is

  c(ρ) = −(1/(ρ(ρ − 1))) · Σ_i (a_i/2) (m_{χ_i}(ρ) + m_{χ_i⁻¹}(ρ)).

The sum is a positive combination of non-negative integers, at least one of which is positive. So **c(ρ) ≠ 0: zeros of different members cannot cancel**, which is guide §3, idea 1. If ρ is real, ρ(ρ − 1) < 0 and c(ρ) > 0. The rest of the proof uses only these properties, packaged as [`PoleData`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauZeroFreeCriterion.lean#L19), and is the abstract lemma [[`Deduction.landau_window`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/landauWindow.lean#L87)]. We recall its geometric core, because a first version of the companion note stated it wrongly. Fix σ > 2; all poles lie to the left of σ [[`landau_pole_re_le`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/LandauPoleReLe.lean#L33)], and a zero ρ₀ with Re ρ₀ > θ is at **horizontal** distance σ − Re ρ₀ < σ − θ from σ, while its Euclidean distance may be much larger. The dichotomy [[`landau_dichotomy`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/LandauDichotomy.lean#L28)] is: either (A) there is D ≤ σ − θ such that the disc B(σ, D) contains no pole but some pole lies at horizontal distance < D; or (B) there is a real pole β > θ which is the only pole in some disc B(σ, r) with σ − β < r ≤ σ − θ. (If the closed disc of radius σ − θ contains no pole, take D = σ − θ. Otherwise let d be the least distance from σ to a pole; if some pole has horizontal distance < d, take D = d; if not, every pole at distance d is real, and it gives (B).) In case (B), the Taylor coefficients at σ grow like c(β)(σ − β)^(−k−1) with c(β) > 0, which contradicts the one-sided bound. In case (A), one moves the centre vertically to σ + iγ so that a single pole ρ is nearest, at distance d′ < r ≤ D [[`landau_nearest`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/LandauNearest.lean#L40)]; Cauchy's estimates on B(σ, D) control the real-axis term, and the pole forces growth like d′^(−k), again a contradiction for small η and large k [[`landau_window_contra`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/landauWindow.lean#L24)]. In particular, a real zero close to 1, a "Siegel zero", is handled by case (B) like any other real pole: **there is no separate treatment of Siegel zeros**. ∎

## 3. Theorem 2 — every level satisfies the windowed criterion

**Statement** [[`UpperTheory.Comparison₂.formB`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/PrimitiveCosets/Imports.lean#L12); definitions [`Level.FormB`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/Window.lean#L28), [`Level.FormBAt`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/Window.lean#L25), [`HasWindows`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/Window.lean#L11), file `TotientGaloisClasses/Window.lean`]. Let Λ be a level, λ > 1 and 0 < θ < 1. Suppose that for every y₀ there is Y ≥ y₀ such that Λ.Gm(x) ≤ x^θ for all x ∈ [Y, Y^λ]. Then every ψ ∈ KEPT has L(s, ψ) ≠ 0 for Re s > θ.

**Proof.** Form the family F indexed by KEPT, with the weight of ψ equal to 1 if ψ is trivial and Λ.wt(ψ) otherwise. All weights are positive, and every member is admissible: a primitive principal character has conductor 1. Then G_F = Λ.Gm, by unfolding the definitions. Apply Theorem 1 with δ = λ − 1 and C = 1. ∎

*Remark.* Only the positivity of the weights is used. The specific values 1 and 1/(3o + 1) play no role here: they come from the averaging of guide §5.

## 4. Theorem 3 — the order of choices

**Statement** [[`Formalism.HC.level_of_tiedWin`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/TopWin.lean#L45), file `TotientGaloisClasses/TopWin.lean`]. Let Λ be a level and λ > 1. Suppose there are constants e_D, e_L and ε₁ > 0 such that, for every 0 < ε < ε₁, there is a set of scales W_ε with the following two properties:
- it contains windows [Y, Y^λ] for arbitrarily large Y ;
- Λ.Gm(x) ≤ x^(½ + (e_D + e_L + 7)ε) for all large x ∈ W_ε.

Then every ψ ∈ KEPT has no zero with Re s > ½.

*(In Lean, W_ε is the window set of an auxiliary "family" `Fm` produced by the arithmetic supply, and the inequality is `ChebyshevInequalityOnWindows`; we have stated only what the proof uses.)*

**Proof.** Let ψ ∈ KEPT and Re s > ½. Put μ = min(Re s − ½, ½) > 0.
- Choose ε ∈ (0, ε₁) with (e_D + e_L + 7)ε ≤ μ/2 [[`exists_small_eps`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/TopWin.lean#L36)].
- Put θ = ½ + μ/2. Then ½ < θ < Re s and θ < 1.
- For large x in the windows, Λ.Gm(x) ≤ x^(½ + μ/2) = x^θ, since x ≥ 1.

So the hypothesis of Theorem 2 holds, and L(s, ψ) ≠ 0. ∎

This is the guide's "θ is chosen after the zero, and ε after θ". The guide writes the exponent as ½ + 9ε; the Lean statement carries the constants e_D + e_L + 7 explicitly. This is a difference of presentation only: the argument works for any fixed constant.

## 5. Theorem 4 — all primitive characters

**Statement** [[`UpperTheory.Top.zeroFreeAll_of_topG`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/CharacterBoxes/ZeroFreeAllOfTopG.lean#L30), [`zeroFreeOn_of_tiedWin_cyc`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/TopWin.lean#L67), [`zeroFreeOn_of_levels`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean#L42)]. If the arithmetic supply [`TopG`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/CharacterBoxes/ZeroFreeAllOfTopG.lean#L16) holds, and hosts exist on windows for every ψ [[`HostExW`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/CharacterBoxes/ZeroFreeAllOfTopG.lean)], then every primitive ψ has L(s, ψ) ≠ 0 for Re s > ½ [[`ZeroFreeAll`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean#L20)].

**Proof.** For each ψ, apply Theorem 3 to the cyclic level Λ = Level.cyc ψ, which contains ψ.
- The hypothesis of Theorem 3 is supplied by [`TopG`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/CharacterBoxes/ZeroFreeAllOfTopG.lean#L16), which provides e_D, e_L, ε₁ and the families; this is the content of (⋆) and is **admitted here**.
- The conclusion for the members of Λ is Theorem 3; it applies to ψ itself because ψ ∈ KEPT. ∎

## 6. Theorem 5 — imprimitive characters, the strip, and ζ

**(a) Imprimitive characters** [[`UpperTheory.Top.imprimitive`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/CharacterBoxes/Imprimitive.lean#L10)]. If every primitive ψ is zero-free on Re s > ½, then so is every χ, at every s with Re s > ½ and (χ ≠ 1 or s ≠ 1). Indeed, L(s, χ) = L(s, χ*) · Π_{p | N} (1 − χ*(p) p^(−s)), where χ* = `PChar.of χ`. Each Euler factor is non-zero for Re s > 0, because |χ*(p) p^(−s)| < 1 [[`Claim.factor_ne_zero`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/CharacterBoxes/HalfPlane.lean#L19)].

**(b) The strip** [[`Claim.strip`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/CharacterBoxes/ClaimStrip.lean#L47)]. Suppose L(s, χ) = 0 with 0 < Re s < 1.
- If Re s > ½, this contradicts (a).
- If Re s < ½, then L(s, χ*) = 0 [[`Claim.prim_zero`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/CharacterBoxes/ClaimStrip.lean#L11)], because the Euler factors do not vanish. The functional equation of the completed L-function of the primitive χ*, together with the non-vanishing of the gamma factor for Re > 0, gives L(1 − s, χ*⁻¹) = 0 [[`Claim.prim_reflect`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/CharacterBoxes/ClaimStrip.lean#L30)]. Since Re(1 − s) > ½, this contradicts (a).

Hence Re s = ½.

**(c) ζ** [[`Claim.zeta`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/CharacterBoxes/ClaimStrip.lean#L63), [`riemannHypothesis`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Main.lean#L13)]. A zero s of ζ with s ≠ 1 and s not a trivial zero −2(n + 1) has Re s > 0: if Re s ≤ 0, the gamma factor does not vanish, so the completed zeta function vanishes at s, hence ζ(1 − s) = 0 with Re(1 − s) ≥ 1, which is impossible. ζ has no zero with Re s ≥ 1. So 0 < Re s < 1, and (b) applies with the trivial character mod 1. This is Mathlib's `RiemannHypothesis`. ∎

*Not traced.* In `Main.lean`, the half-plane statement is the term [`UpperTheory.FinalTheorems.everyCharacter`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/CharacterBoxes/MainConclusion.lean#L19), obtained in `CharacterBoxes/MainConclusion.lean` from [`every_character_of_literature_of_vWin`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/CharacterBoxes/MainConclusion.lean). We did not read how that term calls Theorem 4 and (a). The statements match exactly: [`EveryCharacter`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/CharacterBoxes/EveryCharacter.lean#L7) and the conclusion of (a) are the same proposition.

## 7. What this part uses, and what it does not

**Uses:**
- the Mellin transform of the ramp ;
- the logarithmic derivative of L near its zeros (simple poles, residue = multiplicity) ;
- a crude growth bound |g_χ(y)| ≪ y² [[`Gchi_growth`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/GchiGrowth.lean#L41)] ;
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
| Landau proposition | 0 < θ < 1, δ > 0, "for every C"; θ > ½ only in its application | [`zeroFree_of_rpow_window`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/ZeroFreeOfRpowWindow.lean#L15): hypothesis form, same θ, δ, any C | contrapositives of each other, **same parameters** |
| Weights of P(ψ) | 1 and 1/(3o + 1) | [`Level.wt`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean#L36), with an optional psK of weight 1 | same for [`Level.cyc`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean#L118); only positivity is used |
| Exponent in (⋆) | ½ + 9ε | ½ + (e_D + e_L + 7)ε, constants existential | presentation only |
| Windows | [Y, Y^(3/2)] in (⋆) | `HasWindows S λ`, stated for a parameter λ > 1 | the guide's choice is λ = 3/2 |
| Siegel zeros | covered by positivity | no separate code; case 1 of `landau_window` | as the guide says |
| Imprimitive χ | §1, before | `imprimitive`, applied **after** [`ZeroFreeAll`](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean#L20) | the order differs; the content is the same |

*Revision (23 November 2026).* An independent check (ChatGPT) of the companion note found that its geometric step was misstated and that it wrongly called the Lean statement more general than the guide. Both are corrected here (§2 and §8), and every Lean declaration is now linked to its line at the commit consulted.

*Disclosure.* This note was drafted by Claude (Anthropic), the AI system used to produce the proof, within an amateur research corpus. It is offered as a reading aid; it is not a referee report. The companion proof for ζ (TAC-017) and this note are being cross-checked by a second AI system (ChatGPT), and they have not been reviewed by a human specialist.
