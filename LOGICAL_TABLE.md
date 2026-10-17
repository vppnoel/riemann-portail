# Logical table — Riemann Programme V6.59

*What the corpus establishes, under which hypotheses, and what is missing to conclude. Statuses are read live from the steering data (`pilotage_recherche.json`); statements come from `2_Methode/Pilotage/table_logique.json`. French version: [TABLE_LOGIQUE.md](TABLE_LOGIQUE.md). Author: Vincent NOËL.*

**RH remains open.** A line marked “Proved” holds within its hypotheses; a line marked “Measured” is not a proof.

## Notation

| Sign | Meaning |
|---|---|
| ⇒ | implies (proved in the stated setting) |
| ⇔ | is equivalent to |
| ⇏ | does not imply (counterexample or obstruction exhibited) |
| ∧ | and: every condition of the guard is required |
| Θ | supremum of the real parts of the zeros of ζ; RH ⇔ Θ = ½ |
| Q_W | Weil quadratic form (explicit formula), unitary Fourier transform |
| X_S | test functions supported in [−S, S], finite energy, vanishing exponential moments |

## 1. Overview: five routes towards RH

| Route | Logical guard | Statements established | What is missing (open cut) |
|------------|----------------|-----|----------------|
| Route W — Weil positivity | W10 (sign) ∧ W9 (coverage) ⇒ W11; W11 ⇔ RH (W1) | 6 / 12 | W7 (Partly established), W8 (Partly established), W9 (Partly established), W10 (Open), W11 (Open) |
| Route C — the square (a structure imposing the sign) | C5 (object supplying the square) ⇒ W10, working hypothesis; then route W | 2 / 5 | C3 (Partly established), C5 (Open) |
| Route Q — the initial energy | Q4 ⇔ RH (by Q2) | 3 / 4 | Q4 (Open) |
| Route J — Chebyshev energy and amplification | J3 ∧ J4 ∧ J5 ⇒ zero-free for Re s > 3/4 (J6); J7 ⇔ RH (J2) | 4 / 7 | J5 (Open), J7 (Open) |
| Route H — spectral realization (Hilbert–Pólya) | H3 ∧ H4 ⇒ RH (H2) | 0 / 4 | H3 (Open), H4 (Open) |

Reading: a route succeeds when its whole open cut is closed. None is. Route W is the most advanced: its lock is W10, the sign law, to be proved together with W9, coverage. Route C says where this sign could come from.

## 2. Route W — Weil positivity

RH ⇔ Q_W(f) ≥ 0 for all admissible test functions. The corpus certifies the sign on bounded windows and looks for a sign law on a covering family.

**Guard:** W10 (sign) ∧ W9 (coverage) ⇒ W11; W11 ⇔ RH (W1)

| ID | Statement (logical form) | Hypotheses | Status of the statement | Scope | Source | Idea card (status) |
|--|------------------------------|------------|--------|--------------|------|--------|
| **W0** | Explicit formula: Σ_ρ F(γ_ρ) = pole + archimedean − Σ_n 2Λ(n) n^{−1/2} g(log n) [Wei52] | smooth compactly supported test f | **Classical (cited)** | Exact identity between zeros and primes | [doc. 23 (FR)](1_Presentation/23_AUDIT_V6_3B_FORMULE_EXPLICITE.md) | IDE-010 (Classical (cited)) |
| **W1** | Weil's criterion: RH ⇔ (∀ admissible f: Q_W(f ∗ f̃) ≥ 0) [Wei52] [Bom00a] | none (criterion) | **Classical (cited)** | Classical criterion; exact domain specified in doc. 76 | [doc. 76 (FR)](1_Presentation/76_RECONSTRUIRE_LA_PISTE_GLOBALE_DE_WEIL.pdf) | IDE-052 (Open) |
| **W2** | P = ∂² − ¼ generates the test functions; transports, dense core and parity respect the domain of Q_W  | guards of docs. 67–68 | **Proved** | Construction of the test families | [doc. 67 (FR)](1_Presentation/67_CONSTRUIRE_DES_PONTS_AVEC_BELLMAN.pdf) | IDE-044 (Proved) |
| **W3** | Q_W = (continuous model) + (signed arithmetic fluctuation), exactly; the continuous model alone can be < 0  | pole cancellation (vanishing moments) | **Proved** | The fluctuation must pay the balance | [doc. 70 (FR)](1_Presentation/70_PONT_ARITHMETIQUE_ET_DETTE_DE_COUPLAGE.pdf) | IDE-046 (Proved) |
| **W4** | ∀ S ≤ 11/20, ∀ f ∈ X_S: Q_W(f) ≥ (3/10000)‖f‖²; (S ≤ ½: ‖f‖²/250; S ≤ 0.347: ‖f‖²/25)  | declared interval-arithmetic model; no zeros, no RH | **Proved** | Certificate on the whole infinite space X_S, not beyond 11/20; in range, dominated by Zhu's certified lower bound (L ≤ 0.8, all functions) | [doc. 75 (FR)](1_Presentation/75_RECUPERATION_TRANSPORT_ET_RH.pdf) | IDE-048 (Proved) |
| **W5** | Measured (not certified): inf over X_S of Q_W/‖f‖² ≈ 5.4·10⁻¹² at S = 0.8; λ*(0.8) ∈ [8.9·10⁻¹⁸, 2.27·10⁻¹⁷] (Zhu, certified) [Zhu26] | Galerkin, 40 modes, 60 digits | **Measured** | Positivity at 0.8 already follows from Zhu; certifying 5·10⁻¹² on the kernel would strengthen the margin, not the range. The margin collapses with S | [doc. 81 (EN)](1_Presentation/english/81_ZHU_REPRODUCED.pdf) | IDE-040 (Open) |
| **W6** | Q_W = identity − compact in the energy metric; no uniform margin > 0 in H¹  | declared energy metric | **Proved** | Rules out hoping for uniform coercivity | [doc. 68 (FR)](1_Presentation/68_ARITHMETIQUE_DES_PASSAGES_ET_QUEUE_EFFECTIVE.pdf) | IDE-045 (Proved) |
| **W7** | Sign of Q_W on a block ⇐ sign of the head ∧ bounded Schur debt of the couplings  | Schur guards | **Partly established** | Identity established; debt bound not uniform | [doc. 70 (FR)](1_Presentation/70_PONT_ARITHMETIQUE_ET_DETTE_DE_COUPLAGE.pdf) | IDE-047 (Partly established) |
| **W8** | Exact transport of a positive test function ⇒ positive test function, if reserve ≥ residue along the line  | initial brick, reserve | **Partly established** | Existence of all positive lines open | [doc. 78 (FR)](1_Presentation/78_TRANSPORT_POSITIF_RESERVE_ET_BRIQUE_INITIALE.pdf) | IDE-049 (Partly established) |
| **W9** | Sign on a covering family ∧ passage to the limit in the form norm ⇒ sign on all test functions [SuzH23] | dense core in H¹ (doc. 67, B3) | **Partly established** | Transfer established; sign on the family open | [doc. 76 (suppl.) (FR)](1_Presentation/76_COMPLEMENT_COUP_DOUBLE.pdf) | IDE-050 (Partly established) |
| **W10** | There is an arithmetic law L such that ∀ f in the covering family: Q_W(f) ≥ 0 [Suz26] [SuzSig23] | to be found | **Open** | The central lock | [doc. 79 (FR)](1_Presentation/79_COMPENSATION_PROFILS_ET_OBSTRUCTIONS.pdf) | IDE-051 (Open) |
| **W11** | ∀ admissible f: Q_W(f ∗ f̃) ≥ 0  | none: this is the target conclusion | **Open** | Open; equivalent to RH by W1 | [doc. 76 (FR)](1_Presentation/76_RECONSTRUIRE_LA_PISTE_GLOBALE_DE_WEIL.pdf) | IDE-052 (Open) |

## 3. Route C — the square (a structure imposing the sign)

Where RH is a theorem, the sign comes from a square (a polarization). For ζ, the object that would supply this square is still to be built.

**Guard:** C5 (object supplying the square) ⇒ W10, working hypothesis; then route W

| ID | Statement (logical form) | Hypotheses | Status of the statement | Scope | Source | Idea card (status) |
|--|------------------------------|------------|--------|--------------|------|--------|
| **C1** | Curve C/𝔽_q: B(u) = Tr(u·ι(u)) ≥ 0 ∀u ⇔ RH(C); counts ≥ 0 ∧ degrees ≥ 0 ⇏ RH (119 counterexamples) [Wei48] [Mum70] [MT58] | distinct roots for (b) | **Proved** | Exact computation, 425 curves and 220 fake twins | [doc. 80 (EN)](1_Presentation/english/80_WHERE_THE_SIGN_COMES_FROM.pdf) | IDE-022 (Measured) |
| **C2** | For C/𝔽_q: Rosati positivity (polarization) ⇒ ∣α∣ = √q [Wei48] [Del74] [Has36] | geometric object: polarized Jacobian | **Classical (cited)** | Classical (Weil 1948) | [doc. 28 (FR)](1_Presentation/28_MODELE_REDUIT_NECESSITE_DEMONTREE.pdf) | IDE-006 (Measured) |
| **C3** | Signature of a “virtual surface” computed from the primes: that of ζ has the expected shape (one positive direction); DH has extra directions [CC21] [Con99] | finite windows | **Partly established** | Signatures built; no object imposing the sign | [doc. 46 (FR)](1_Presentation/46_LA_SURFACE_VIRTUELLE.pdf) | IDE-064 (Partly established) |
| **C4** | Direct transplantation of Stepanov's method to ζ (the scale model studied) ⇏ sign [Ste69] [Bom73] | the model studied | **Obstruction** | Obstruction of method, reopenable with a constructed derivation | [doc. 51 (FR)](1_Presentation/51_J3B_LE_FROBENIUS_DE_CARACTERISTIQUE_UN.pdf) | IDE-065 (Obstruction) |
| **C5** | ∃ ? a structure (polarization, ample class) such that Q_W(f) = ‖Af‖² for a structural reason [CC21] | to be built | **Open** | Working hypothesis; no particular form of object is declared necessary | [doc. 80 (EN)](1_Presentation/english/80_WHERE_THE_SIGN_COMES_FROM.pdf) | IDE-036 (Open) |

## 4. Route Q — the initial energy

Theorem A reduces RH to a growth bound for the energy Q built from the primes.

**Guard:** Q4 ⇔ RH (by Q2)

| ID | Statement (logical form) | Hypotheses | Status of the statement | Scope | Source | Idea card (status) |
|--|------------------------------|------------|--------|--------------|------|--------|
| **Q1** | c = Λ∗Λ − Λ·log + 2γΛ = 1∗a, a(n) = μ(n)(log²n − 2γ log n); G(s) = ζ·(f″ + 2γf′), f = 1/ζ  | none | **Proved** | Exact identities | [Rigorous lemmas (FR)](3_Preuves_et_calculs/preuves/LEMMES_RIGOUREUX.md) | IDE-001 (Proved) |
| **Q2** | Growth exponent of Q(X) = 2(Θ − ½); hence the criterion RH ⇔ Q(X) = X^{o(1)} [Cra22] [Nym50] [Beu55] | none (unconditional) | **Proved** | Proved, internally reviewed | [paper 1](1_Presentation/articles/article1_mean_square_double_poles.pdf) | IDE-002 (Proved) |
| **Q3** | RH ⇒ Q(X) ∼ (S/3)(log X)³; RH ⇒ (S = 4κ ⇔ simple zeros); Q/(log X)³ → 4κ/3 ⇔ RH ∧ simplicity [Cra22] [Mon73] | RH for the asymptotics | **Proved** | Implication proved, internally reviewed: a calibration under RH, not a step towards RH | [paper 1](1_Presentation/articles/article1_mean_square_double_poles.pdf) | IDE-003 (Conditional) |
| **Q4** | Q(X) = X^{o(1)} proved from the primes alone  | to be found | **Open** | Open; equivalent to RH by Q2 | [Rigorous lemmas (FR)](3_Preuves_et_calculs/preuves/LEMMES_RIGOUREUX.md) | IDE-058 (Open) |

## 5. Route J — Chebyshev energy and amplification

RH ⇔ J(X) = ∫₁ˣ (ψ − x)² ≪ X². The corpus restores the Möbius sum exactly and controls the head of conductors; the large tail is open.

**Guard:** J3 ∧ J4 ∧ J5 ⇒ zero-free for Re s > 3/4 (J6); J7 ⇔ RH (J2)

| ID | Statement (logical form) | Hypotheses | Status of the statement | Scope | Source | Idea card (status) |
|--|------------------------------|------------|--------|--------------|------|--------|
| **J1** | Σ_{d∣n} Λ(d) = log n  | none | **Classical (cited)** | Classical; bounds nothing on its own | [Correlations (FR)](1_Presentation/CORRELATIONS_IDENTITE_ET_ENERGIE.pdf) | IDE-054 (Classical (cited)) |
| **J2** | Criterion: RH ⇔ J(X) = O(X²) for the true Λ [Cra22] | none (criterion) | **Classical (cited)** | Classical criterion | [Correlations (FR)](1_Presentation/CORRELATIONS_IDENTITE_ET_ENERGIE.pdf) | IDE-057 (Open) |
| **J3** | A_o(x) = F_{p²}(x) − F_{p²}(x/p): exact restitution, stable under dilation  | odd prime p | **Proved** | Proved | [Essay V6.55 (FR)](1_Presentation/ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.pdf) | IDE-059 (Proved) |
| **J4** | Head q ≤ H bounded explicitly, at every scale  | declared parameters | **Proved** | Proved | [Essay V6.55 (FR)](1_Presentation/ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.pdf) | IDE-060 (Proved) |
| **J5** | At H = X: R_{q>X} ≤ C X³(1 + log X)^k, keeping μ(q)  | to be found | **Open** | Open; the generic sieve is not enough | [Essay V6.55 (FR)](1_Presentation/ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.pdf) | IDE-061 (Open) |
| **J6** | copies ∧ head ∧ large_q ⇒ J ≪ X^{5/2} polylog ⇒ ζ(s) ≠ 0 for Re s > 3/4  | the three contracts | **Conditional** | Conditional; does not give the bound J = O(X²) (5/2 > 2) | [Essay V6.55 (FR)](1_Presentation/ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.pdf) | IDE-062 (Conditional) |
| **J7** | J(X) = O(X²) for the true Λ, at every scale [Cra22] | none: this is the target conclusion | **Open** | Open; equivalent to RH by J2 | [Correlations (FR)](1_Presentation/CORRELATIONS_IDENTITE_ET_ENERGIE.pdf) | IDE-057 (Open) |

## 6. Route H — spectral realization (Hilbert–Pólya)

A self-adjoint arithmetic operator whose spectrum captures exactly the zeros would give RH. Nothing exhaustive has been built.

**Guard:** H3 ∧ H4 ⇒ RH (H2)

| ID | Statement (logical form) | Hypotheses | Status of the statement | Scope | Source | Idea card (status) |
|--|------------------------------|------------|--------|--------------|------|--------|
| **H1** | The operator of ζ is rebuilt on a finite window from the primes alone; its metric is > 0 for ζ and L, < 0 for DH exactly at its off-line zeros  | finite window | **Measured** | Measured | [doc. 33 (FR)](1_Presentation/33_LE_GENERATEUR_DES_PREMIERS.pdf) | IDE-026 (Measured) |
| **H2** | Arithmetic self-adjointness ∧ spectral completeness ⇒ RH [Con99] | both | **Conditional** | Conditional; neither is established | [doc. 32 (FR)](1_Presentation/32_LE_CHAINON_DU_DISCRET_AU_CONTINU.pdf) | IDE-042 (Open) |
| **H3** | ∃ ? a self-adjoint operator built from arithmetic whose eigenvalues are the γ [Con99] | to be built | **Open** | Open; reparametrizations (Schrödinger, H_eff) are not enough | [doc. 32 (FR)](1_Presentation/32_LE_CHAINON_DU_DISCRET_AU_CONTINU.pdf) | IDE-042 (Open) |
| **H4** | The spectrum of this operator captures all zeros, with multiplicities, and its domain is justified  | to be built | **Open** | Open; a finite window is not enough | [doc. 32 (FR)](1_Presentation/32_LE_CHAINON_DU_DISCRET_AU_CONTINU.pdf) | IDE-041 (Open) |

## 7. Counter-witnesses

Any argument claiming to impose the sign must survive these witnesses.

| ID | Fact | What it rules out | Status | Source |
|--|--------------------|--------------------|------|-----|
| **T1** | DH (functional equation, no Euler product): at least 25 negative directions certified in a window | Any argument claiming to impose the sign without using the Euler product must fail on DH. | Proved | [doc. 60 (FR)](1_Presentation/60_ARTICLES_ET_CERTIFICAT_DE_NEGATIVITE.pdf) |
| **T2** | In V_q (declared degree 1): RH ⇒ Euler point; the converse is not established | The Euler product is necessary here; this does not prove it is sufficient. | Proved | [doc. 30 (FR)](1_Presentation/30_ARCHIPEL_D_EULER.pdf) |
| **T3** | 119 fake twins: counts ≥ 0 ∧ degrees ≥ 0 ∧ ¬RH | No count or degree argument replaces a square. | Measured | [doc. 80 (EN)](1_Presentation/english/80_WHERE_THE_SIGN_COMES_FROM.pdf) |

## 8. Obstructions: what is not enough

| Statement | Idea card | Source |
|------------------------------|----|-----|
| Certificate on S ≤ 11/20 ⇏ sign on all supports | IDE-048 | [doc. 75 (FR)](1_Presentation/75_RECUPERATION_TRANSPORT_ET_RH.pdf) |
| A certified chosen fold ⇏ global sign | IDE-043 | [doc. 66 (FR)](1_Presentation/66_UN_PLI_CERTIFIE_ET_SA_PAIRE.pdf) |
| Generic sieve ⇏ bound on the large tail (cost D√H) | IDE-063 | [Essay V6.55 (FR)](1_Presentation/ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.pdf) |
| Norm of the prime part alone: diverges, ⇏ control of the form | IDE-069 | [doc. 66 (FR)](1_Presentation/66_UN_PLI_CERTIFIE_ET_SA_PAIRE.pdf) |
| J ≪ X^{5/2} ⇏ J ≪ X² (exponent insufficient) | IDE-062 | [Essay V6.55 (FR)](1_Presentation/ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.pdf) |
| No uniform margin in H¹ ⇒ no proof by coercivity alone | IDE-045 | [doc. 68 (FR)](1_Presentation/68_ARITHMETIQUE_DES_PASSAGES_ET_QUEUE_EFFECTIVE.pdf) |
| Window by window: margin ∼ 10⁻¹² at S = 0.8 and collapsing fast ⇏ strategy towards RH | IDE-040 | [doc. 81 (EN)](1_Presentation/english/81_ZHU_REPRODUCED.pdf) |

## 9. What is missing, at the shortest, and what is already under way

Investigation identifiers and labels are those of the French steering data.

| Route | Open statement | Pre-registered investigations aiming at it |
|--|------------------------|------------------------|
| W | **W7** Sign of Q_W on a block ⇐ sign of the head ∧ bounded Schur debt of the couplings | `duale_schur`, `test_paquets` |
| W | **W8** Exact transport of a positive test function ⇒ positive test function, if reserve ≥ residue along the line | `signe_paquets` |
| W | **W9** Sign on a covering family ∧ passage to the limit in the form norm ⇒ sign on all test functions | `signe_paquets`, `couverture_constructive` |
| W | **W10** There is an arithmetic law L such that ∀ f in the covering family: Q_W(f) ≥ 0 | `signe_paquets`, `duale_schur`, `test_paquets` |
| W | **W11** ∀ admissible f: Q_W(f ∗ f̃) ≥ 0 | `couverture_constructive` |
| C | **C3** Signature of a “virtual surface” computed from the primes: that of ζ has the expected shape (one positive dire… | none: route to be opened |
| C | **C5** ∃ ? a structure (polarization, ample class) such that Q_W(f) = ‖Af‖² for a structural reason | none: route to be opened |
| Q | **Q4** Q(X) = X^{o(1)} proved from the primes alone | none: route to be opened |
| J | **J5** At H = X: R_{q>X} ≤ C X³(1 + log X)^k, keeping μ(q) | `mu_correlations`, `grands_conducteurs` |
| J | **J7** J(X) = O(X²) for the true Λ, at every scale | none: route to be opened |
| H | **H3** ∃ ? a self-adjoint operator built from arithmetic whose eigenvalues are the γ | none: route to be opened |
| H | **H4** The spectrum of this operator captures all zeros, with multiplicities, and its domain is justified | none: route to be opened |

## 10. The 79 typed relations of the idea graph

Each relation links two idea cards; the guard lists every card required. A relation of use or an analogy is not an implication. Card titles and relation labels are in French, as in the steering data.

### ⇔ equivalence — “is equivalent to” (3)

| Origin | | Target | Content (FR) | Guard |
|--------------|--|--------------|--------------|------|
| IDE-058 Borne de l’énergie initiale Q *(Open)* | ⇔ | IDE-053 Hypothèse de Riemann *(Open)* | Critère A dans son cadre |  |
| IDE-052 Weil sur tous les tests *(Open)* | ⇔ | IDE-053 Hypothèse de Riemann *(Open)* | Critère de Weil, domaine précisé |  |
| IDE-057 Borne de force RH *(Open)* | ⇔ | IDE-053 Hypothèse de Riemann *(Open)* | Critère classique, pour Λ |  |

### ⇐ garde conditionnel — “gives the target if the whole guard holds” (7)

| Origin | | Target | Content (FR) | Guard |
|--------------|--|--------------|--------------|------|
| IDE-042 Hilbert–Pólya *(Open)* | ⇐ garde | IDE-053 Hypothèse de Riemann *(Open)* | Auto-adjonction arithmétique ET capture exhaustive | IDE-042 ∧ IDE-041 |
| IDE-051 Loi de signe de la famille *(Open)* | ⇐ garde | IDE-052 Weil sur tous les tests *(Open)* | Signe ET couverture dans le domaine requis | IDE-051 ∧ IDE-050 |
| IDE-050 Couverture et passage à la limite *(Partly established)* | ⇐ garde | IDE-052 Weil sur tous les tests *(Open)* | Signe ET couverture dans le domaine requis | IDE-051 ∧ IDE-050 |
| IDE-059 Restitution et dilatations *(Proved)* | ⇐ garde | IDE-062 Étape conditionnelle : 3/4 *(Conditional)* | Les trois contrats sont requis | IDE-059 ∧ IDE-060 ∧ IDE-061 |
| IDE-060 Diagonale et petits conducteurs *(Proved)* | ⇐ garde | IDE-062 Étape conditionnelle : 3/4 *(Conditional)* | Les trois contrats sont requis | IDE-059 ∧ IDE-060 ∧ IDE-061 |
| IDE-061 Grands conducteurs signés *(Open)* | ⇐ garde | IDE-062 Étape conditionnelle : 3/4 *(Conditional)* | Les trois contrats sont requis | IDE-059 ∧ IDE-060 ∧ IDE-061 |
| IDE-004 Proposition C *(Conditional)* | ⇐ garde | IDE-003 Théorème B *(Conditional)* | Les hypothèses supplémentaires ne sont pas levées |  |

### → construction — “supplies a brick to” (22)

| Origin | | Target | Content (FR) | Guard |
|--------------|--|--------------|--------------|------|
| IDE-001 Lemmes 1 à 5 *(Proved)* | → | IDE-002 Théorème A *(Proved)* | Pôles et transformée de Mellin |  |
| IDE-001 Lemmes 1 à 5 *(Proved)* | → | IDE-003 Théorème B *(Conditional)* | Identités utiles sous RH |  |
| IDE-014 DARK-ZETA *(Tool)* | → | IDE-055 Corrélations ancrées *(Proved)* | Repérer la perte de l’origine |  |
| IDE-022 V6.6Le Modèle réduit *(Measured)* | → | IDE-025 V6.9Le chaînon F = q^D *(Measured)* | Faux jumeaux et métrique |  |
| IDE-025 V6.9Le chaînon F = q^D *(Measured)* | → | IDE-026 V6.10Le générateur des premiers *(Measured)* | Reconstruire depuis les premiers |  |
| IDE-018 DUAL-LOCK *(Tool)* | → | IDE-047 Dette des couplages *(Partly established)* | Gram et couplages |  |
| IDE-039 Kalman, GPS analytique *(Measured)* | → | IDE-047 Dette des couplages *(Partly established)* | Innovations et dette de couplage |  |
| IDE-037 Localisation de sources *(Diagnostic)* | → | IDE-047 Dette des couplages *(Partly established)* | Résidus et Grams |  |
| IDE-024 V6.8L'Archipel d'Euler *(Proved)* | → | IDE-043 Fibres, jets et pli choisi *(Proved)* | Comparer sous contraintes exactes |  |
| IDE-044 P, moments et domaines *(Proved)* | → | IDE-045 Changement de métrique *(Proved)* | Domaines et métriques compatibles |  |
| IDE-044 P, moments et domaines *(Proved)* | → | IDE-046 Fluctuation arithmétique signée *(Proved)* | Moments et annulation polaire |  |
| IDE-045 Changement de métrique *(Proved)* | → | IDE-048 Lego local : S ≤ 11/20 *(Proved)* | Réduction tête–queue dans le bon domaine |  |
| IDE-044 P, moments et domaines *(Proved)* | → | IDE-050 Couverture et passage à la limite *(Partly established)* | Cœur, transports et filtres |  |
| IDE-054 Identité des vrais coefficients *(Classical (cited))* | → | IDE-056 Énergie J *(Classical (cited))* | Vrais poids Λ |  |
| IDE-055 Corrélations ancrées *(Proved)* | → | IDE-056 Énergie J *(Classical (cited))* | Formule de corrélation avec bords |  |
| IDE-054 Identité des vrais coefficients *(Classical (cited))* | → | IDE-059 Restitution et dilatations *(Proved)* | Inversion exacte de Möbius |  |
| IDE-059 Restitution et dilatations *(Proved)* | → | IDE-060 Diagonale et petits conducteurs *(Proved)* | Regroupement par conducteur |  |
| IDE-010 Formule explicite de Weil *(Classical (cited))* | → | IDE-046 Fluctuation arithmétique signée *(Proved)* | Forme explicite complète, normalisation et domaine |  |
| IDE-022 V6.6Le Modèle réduit *(Measured)* | → | IDE-064 Surface et Frobenius virtuels *(Partly established)* | Chercher la structure d’un étage supérieur |  |
| IDE-066 Lemme des jets et relief *(Proved)* | → | IDE-043 Fibres, jets et pli choisi *(Proved)* | Rang, contraintes exactes, fibres et plis |  |
| IDE-005 Davenport–Heilbronn *(Obstruction)* | → | IDE-067 Certificat négatif de DH *(Proved)* | De témoin numérique à certificat sous budget |  |
| IDE-030 V6.16La Rencontre à trois *(Proved)* | → | IDE-068 La Rencontre à n *(Measured)* | Étudier des interactions à plusieurs zéros |  |

### ⊣ obligation — “leaves to be established for” (8)

| Origin | | Target | Content (FR) | Guard |
|--------------|--|--------------|--------------|------|
| IDE-026 V6.10Le générateur des premiers *(Measured)* | ⊣ | IDE-041 Complétude spectrale *(Open)* | Capturer toute la famille, pas seulement une fenêtre |  |
| IDE-026 V6.10Le générateur des premiers *(Measured)* | ⊣ | IDE-051 Loi de signe de la famille *(Open)* | La métrique positive ne suit pas de la reconstruction |  |
| IDE-046 Fluctuation arithmétique signée *(Proved)* | ⊣ | IDE-051 Loi de signe de la famille *(Open)* | Payer la dette réelle à toutes les échelles |  |
| IDE-047 Dette des couplages *(Partly established)* | ⊣ | IDE-051 Loi de signe de la famille *(Open)* | Contrôler les couplages de la famille choisie |  |
| IDE-049 Transport et réserve *(Partly established)* | ⊣ | IDE-051 Loi de signe de la famille *(Open)* | Réserve et résidu pour toutes les lignes |  |
| IDE-056 Énergie J *(Classical (cited))* | ⊣ | IDE-057 Borne de force RH *(Open)* | Majoration indépendante à toute échelle |  |
| IDE-060 Diagonale et petits conducteurs *(Proved)* | ⊣ | IDE-061 Grands conducteurs signés *(Open)* | Le reste ne disparaît pas |  |
| IDE-055 Corrélations ancrées *(Proved)* | ⊣ | IDE-051 Loi de signe de la famille *(Open)* | L’ancrage est nécessaire à la stratégie, pas une preuve du signe |  |

### ⇏ insuffisant — “is not enough for” (3)

| Origin | | Target | Content (FR) | Guard |
|--------------|--|--------------|--------------|------|
| IDE-043 Fibres, jets et pli choisi *(Proved)* | ⇏ | IDE-051 Loi de signe de la famille *(Open)* | Un pli choisi ne donne pas le signe global |  |
| IDE-048 Lego local : S ≤ 11/20 *(Proved)* | ⇏ | IDE-051 Loi de signe de la famille *(Open)* | Le plafond 11/20 ne couvre pas tous les supports |  |
| IDE-062 Étape conditionnelle : 3/4 *(Conditional)* | ⇏ | IDE-057 Borne de force RH *(Open)* | Exposant 5/2 encore au-dessus de 2 |  |

### ✕ obstruction — “blocks a method towards” (8)

| Origin | | Target | Content (FR) | Guard |
|--------------|--|--------------|--------------|------|
| IDE-016 TOMO-3 brut *(Diagnostic)* | ✕ | IDE-055 Corrélations ancrées *(Proved)* | Le rejet du bispectre brut ne ferme pas l’ancrage |  |
| IDE-038 Schrödinger, Heff *(Obstruction)* | ✕ | IDE-042 Hilbert–Pólya *(Open)* | Une reparamétrisation ne fournit pas la métrique |  |
| IDE-063 Crible générique : perte des copies *(Obstruction)* | ✕ | IDE-061 Grands conducteurs signés *(Open)* | Exiger une propriété spécifique de μ(q) et B |  |
| IDE-020 V6.4Seuil τ_c *(Obstruction)* | ✕ | IDE-023 V6.7Marges de la forme et de l'objet *(Measured)* | Seuil dépendant de la fenêtre |  |
| IDE-007 Densité de zéros *(Obstruction)* | ✕ | IDE-058 Borne de l’énergie initiale Q *(Open)* | Le cadre ancien ne donne pas de gain |  |
| IDE-064 Surface et Frobenius virtuels *(Partly established)* | ✕ | IDE-065 Transplantation directe de Stepanov *(Obstruction)* | La transplantation directe étudiée est insuffisante |  |
| IDE-069 Norme de la partie première seule *(Obstruction)* | ✕ | IDE-044 P, moments et domaines *(Proved)* | Contrôler la forme complète dans le domaine requis |  |
| IDE-069 Norme de la partie première seule *(Obstruction)* | ✕ | IDE-047 Dette des couplages *(Partly established)* | Ne pas payer le couplage par une norme divergente |  |

### ≡ critere — “states the criterion for” (2)

| Origin | | Target | Content (FR) | Guard |
|--------------|--|--------------|--------------|------|
| IDE-002 Théorème A *(Proved)* | ≡ | IDE-058 Borne de l’énergie initiale Q *(Open)* | Énonce la borne équivalente, sans la prouver |  |
| IDE-013 Dimension énergétique / fractal strings *(Tool)* | ≡ | IDE-058 Borne de l’énergie initiale Q *(Open)* | Dimension et croissance, même borne manquante |  |

### ⚠ temoin — “is a counter-witness for” (2)

| Origin | | Target | Content (FR) | Guard |
|--------------|--|--------------|--------------|------|
| IDE-005 Davenport–Heilbronn *(Obstruction)* | ⚠ | IDE-014 DARK-ZETA *(Tool)* | Témoin adversarial conservé |  |
| IDE-067 Certificat négatif de DH *(Proved)* | ⚠ | IDE-051 Loi de signe de la famille *(Open)* | Tester les arguments qui prétendent imposer le signe |  |

### ? hypothese — “is a working hypothesis towards” (2)

| Origin | | Target | Content (FR) | Guard |
|--------------|--|--------------|--------------|------|
| IDE-036 L'objet qui porte la métrique *(Open)* | ? | IDE-051 Loi de signe de la famille *(Open)* | Structure imposant le signe à construire |  |
| IDE-064 Surface et Frobenius virtuels *(Partly established)* | ? | IDE-036 L'objet qui porte la métrique *(Open)* | Une structure globale imposant le signe reste à construire |  |

### ↺ reouverture — “reopens” (2)

| Origin | | Target | Content (FR) | Guard |
|--------------|--|--------------|--------------|------|
| IDE-008 Arrêt de l'attaque directe *(Obstruction)* | ↺ | IDE-046 Fluctuation arithmétique signée *(Proved)* | Nouvelle obligation arithmétique discriminante |  |
| IDE-065 Transplantation directe de Stepanov *(Obstruction)* | ↺ | IDE-066 Lemme des jets et relief *(Proved)* | Des conditions de réouverture exigent des objets définis |  |

### ∼ relation — “sheds light on” (15)

| Origin | | Target | Content (FR) | Guard |
|--------------|--|--------------|--------------|------|
| IDE-011 Nyman–Beurling *(Classical (cited))* | ∼ | IDE-002 Théorème A *(Proved)* | Projection étudiée ramenée à Q |  |
| IDE-012 Critère de Li *(Classical (cited))* | ∼ | IDE-001 Lemmes 1 à 5 *(Proved)* | Constante commune ; pas tous les signes de Li |  |
| IDE-006 Corps de fonctions *(Measured)* | ∼ | IDE-022 V6.6Le Modèle réduit *(Measured)* | Modèle où la positivité est démontrée |  |
| IDE-017 PRIME-LOCK *(Tool)* | ∼ | IDE-018 DUAL-LOCK *(Tool)* | Détecteurs locaux et globaux distincts |  |
| IDE-019 Résidu sombre *(Tool)* | ∼ | IDE-047 Dette des couplages *(Partly established)* | Normalisation par le vrai Gram |  |
| IDE-023 V6.7Marges de la forme et de l'objet *(Measured)* | ∼ | IDE-045 Changement de métrique *(Proved)* | Forme positive et marge sont distinctes |  |
| IDE-030 V6.16La Rencontre à trois *(Proved)* | ∼ | IDE-043 Fibres, jets et pli choisi *(Proved)* | Une identité de marge ne certifie pas toutes les collisions |  |
| IDE-031 V6.17La Rencontre en degré 2 *(Measured)* | ∼ | IDE-029 V6.15Le degré 2 et le recensement *(Measured)* | Même instrument, cadre de degré 2 |  |
| IDE-028 V6.14Le temps de Heisenberg *(Measured)* | ∼ | IDE-026 V6.10Le générateur des premiers *(Measured)* | Loi de détection, pas loi de signe |  |
| IDE-021 V6.5Famille modulo 7 *(Measured)* | ∼ | IDE-024 V6.8L'Archipel d'Euler *(Proved)* | Îles observées et rigidité déclarée |  |
| IDE-027 V6.11La base comme pas de temps *(Measured)* | ∼ | IDE-025 V6.9Le chaînon F = q^D *(Measured)* | Discret et continu |  |
| IDE-054 Identité des vrais coefficients *(Classical (cited))* | ∼ | IDE-046 Fluctuation arithmétique signée *(Proved)* | Deux descriptions des vrais poids |  |
| IDE-040 Positivité de Weil *(Open)* | ∼ | IDE-051 Loi de signe de la famille *(Open)* | Même exigence de signe ; pas de coercivité uniforme |  |
| IDE-015 TOMO-2 *(Tool)* | ∼ | IDE-014 DARK-ZETA *(Tool)* | Perte de phase dans les observables de puissance |  |
| IDE-068 La Rencontre à n *(Measured)* | ∼ | IDE-047 Dette des couplages *(Partly established)* | Les interactions motivent un contrôle des couplages |  |

### ⚙ outil — “is a tool for” (5)

| Origin | | Target | Content (FR) | Guard |
|--------------|--|--------------|--------------|------|
| IDE-032 V6.18Le registre des sources *(Tool)* | ⚙ | IDE-009 Relecture externe de A et B *(Open)* | Sources et périmètre de relecture |  |
| IDE-034 Indicateur d'avancement *(Tool)* | ⚙ | IDE-035 Navigateur de recherche *(Tool)* | Position et critères de réévaluation |  |
| IDE-035 Navigateur de recherche *(Tool)* | ⚙ | IDE-033 Prochain coup *(Tool)* | Choix recalculés |  |
| IDE-033 Prochain coup *(Tool)* | ⚙ | IDE-051 Loi de signe de la famille *(Open)* | Les investigations visent cette obligation, sans la supposer vraie |  |
| IDE-009 Relecture externe de A et B *(Open)* | ⚙ | IDE-002 Théorème A *(Proved)* | Relecture de la preuve et de ses conditions |  |
