# Riemann Programme — V6.59 (English entry)

*17 October 2026. A personal research programme on the Riemann Hypothesis (RH), kept as a versioned corpus of documents, proofs, code, data and tests. Author: Vincent P. P. NOËL (Strasbourg). The work was carried out with the help of ChatGPT (OpenAI) and Claude (Anthropic); the author takes final responsibility for the content. Most research documents are in French ([README.md](README.md)); this entry layer, the three papers, the specialist review file and documents 80–82 are in English.*

## Read first

**RH remains open. The corpus contains no proof of RH. It contains statements proved in delimited settings, certificates on bounded windows, measurements with predictions written in advance, and a precise list of what is missing.**

**1. The analytic core: Theorems A and B, three papers ready for specialist review** — *Proved, internally reviewed · not yet refereed*

Theorem A: the growth exponent of the energy Q(X), the integral of |C(x)|² x⁻² from 1 to X built from c = Λ∗Λ − Λ·log + 2γΛ, equals 2(Θ − ½). Theorem B: under RH, Q(X) ∼ (S/3)(log X)³; the constant equals 4κ/3 if and only if all zeros are simple, which gives a joint criterion for RH and simplicity. Paper 1 contains these statements; paper 2 a certificate in a fixed window; paper 3 is an expository note (Hasse jets) claiming no historical novelty. External review is the next step of the progress indicator (level 7).

→ [Paper 1](1_Presentation/articles/article1_mean_square_double_poles.pdf) · [Paper 2](1_Presentation/articles/article2_prime_side_weil_forms.pdf) · [Paper 3](1_Presentation/articles/article3_hasse_jets_and_spectral_bound.pdf) · [Specialist review file](1_Presentation/relecture/00_READ_ME_FIRST_EN.md)

**2. What is missing is not a count but a square** — *Proved (elementary) · classical results cited*

In the reduced model (curves over 𝔽_q), 119 fake twins that violate RH have non-negative point counts and non-negative isogeny degrees. Only the trace of a square, the Rosati positivity coming from a polarization, excludes them. ζ already passes the first two levels (Λ ≥ 0, no real zero). What it lacks is the object that would supply this square.

→ [Document 80 (EN)](1_Presentation/english/80_WHERE_THE_SIGN_COMES_FROM.pdf) · [Reduced model (doc. 28, FR)](1_Presentation/28_MODELE_REDUIT_NECESSITE_DEMONTREE.pdf)

**3. Weil positivity certified on all test functions, but within windows** — *Certified in its domain · measured beyond*

On the infinite space of test functions with vanishing moments, without zeros or RH: Q_W ≥ ‖f‖²/25 for S ≤ 0.347 (doc. 71), ≥ ‖f‖²/250 for S ≤ 1/2 (doc. 73), ≥ 3‖f‖²/10000 for S ≤ 11/20 (doc. 75). Document 81 independently reproduces Zhu's values up to L = 0.8 (not certified) and measures, on the same subspace, a margin of about 5·10⁻¹² at 0.8. Caution: Zhu's certified lower bound (λ*(0.8) > 0 for all functions) already covers these windows in range; the corpus certificates give stronger margins on zero-moment test functions, not a wider window.

→ [Document 73 (FR)](1_Presentation/73_OPERATEUR_COMMUN_TETE_SOURCES_ET_QUEUE.pdf) · [Document 75 (FR)](1_Presentation/75_RECUPERATION_TRANSPORT_ET_RH.pdf) · [Document 81 (EN)](1_Presentation/english/81_ZHU_REPRODUCED.pdf)

**4. The Euler archipelago: RH holds only at the Euler points** — *Proved in the declared spaces · internally pre-reviewed*

Among the combinations of L-functions sharing the functional equation, RH holds only at the points where the function has an Euler product (declared degree-1 spaces V_q). The result locates the necessity; it does not give “Euler product ⇒ RH”.

→ [Document 30 (FR)](1_Presentation/30_ARCHIPEL_D_EULER.pdf) · [Archipelago review (EN)](1_Presentation/relecture/RELECTURE_ARCHIPEL_EN.md)

**5. Arithmetic side: the head is controlled, the large tail is open** — *Proved under its guards · open*

The Möbius sum is restored exactly and the head of conductors q ≤ H is bounded at every scale. The signed debt of large conductors remains to be controlled; the consequence towards Re(s) > 3/4 is conditional on that bound.

→ [Amplification essay V6.55 (FR)](1_Presentation/ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.pdf) · [Correlations, identity and energy (FR)](1_Presentation/CORRELATIONS_IDENTITE_ET_ENERGIE.pdf)

**6. What remains open, precisely** — *Open*

Three obligations: the sign law on a family of test functions (IDE-051), coverage and the passage to the limit (IDE-050), Weil positivity on all test functions (IDE-052). The operator route Q = ‖Tf‖² taken from Suzuki is suspended because of a parity inconsistency in the published convention; the one-sided operator T₊ is used instead.

→ [Document 76 (FR)](1_Presentation/76_RECONSTRUIRE_LA_PISTE_GLOBALE_DE_WEIL.pdf) · [Supplement 76, §8 parity (FR)](1_Presentation/76_COMPLEMENT_COUP_DOUBLE.pdf) · [Document 79 (FR)](1_Presentation/79_COMPENSATION_PROFILS_ET_OBSTRUCTIONS.pdf)

**Reading precautions**

- The progress indicator levels are maturity categories: neither a percentage of RH nor a probability of proof.
- “Measured” means computed in high precision, not certified. Only statements marked “certified” or “proved” are so, and only in their domain.
- Two numbers carry two pieces each: 76 and 79 (a document and its supplement). Numbers are never reassigned.
- Each document describes the state at its date. The synthesis (doc. 01) and the reading guide (doc. 07) are up to date at V6.58 in French and English; most other research documents are in French.
- Received documents (4_Archives/recus) and archived originals are never modified; reconstructed pieces are marked as such.

## What changed in V6.59

- **Targeting and division of work.** [Document 82](1_Presentation/english/82_TARGETING_AND_DIVISION_OF_WORK.pdf) and its reference [`TARGETING_EN.md`](2_Methode/Pilotage/TARGETING_EN.md). The targeting reads the state without changing it and proposes task cards; each card can be given to the author, an AI or an agent: prediction recorded first, work in a deposit area, verification by another actor, decision by the author, hash-chained log. Seven cards are open, not yet assigned.
- **One method.** The targeting layer of the 16 October branch, the steering protocol and the multi-agent protocol of 5 October are merged: a single register of reviewed hashes; prerequisites met only by a positive outcome declared with its scope; view figures computed from the data.
- **Nine cards, assigned.** Two cards added from the phase-tomography critique (TAC-008, TAC-009); three to ia:claude, three to ChatGPT, three unassigned.
- **GitHub.** [`GITHUB.md`](GITHUB.md) (French): one private repository imported in five coherent parts; `tac-xxx` branches limited to the deposit area; automatic checks.
- **No new mathematical result**; indicator levels unchanged. V6.58 (documents 80 and 81, reorganised entry) is described in the release history.

## Where to go

- [Intuitive reading guide (doc. 07, EN)](1_Presentation/english/07_READING_GUIDE_EN.pdf)
- [Synthesis (doc. 01, EN)](1_Presentation/english/01_SYNTHESIS_EN.pdf)
- [Portal (FR)](00_PORTAIL.html)
- [Logical table](LOGICAL_TABLE.md)
- [Ranked references](REFERENCES_RANKED.md)
- [Targeting and division of work (doc. 82)](1_Presentation/english/82_TARGETING_AND_DIVISION_OF_WORK.pdf)
- [Working on GitHub (FR)](GITHUB.md)
- [Guide for an AI (prompt)](GUIDE_FOR_AN_AI.md)
- [Papers (PDF and LaTeX)](1_Presentation/articles/LISEZMOI_ARTICLES.md)
- [Documents 80 and 81 in English](1_Presentation/english/80_WHERE_THE_SIGN_COMES_FROM.md)
- [Corpus map (FR)](PLAN_DU_CORPUS.md)

## The corpus at a glance

The 82 numbered documents (in French) are grouped in seven questions in [PLAN_DU_CORPUS.md](PLAN_DU_CORPUS.md):

- **I. Starting point: the energy Q and the first texts**: documents 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13.
- **II. The V6 instruments and their audit**: documents 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26.
- **III. What RH requires: families, reduced model, Euler archipelago**: documents 27, 28, 29, 30, 56, 57, 58, 61, 63, 64.
- **IV. From primes to the continuum: operators, thresholds, encounters**: documents 32, 33, 35, 38, 39, 40, 41, 43, 45, 53, 54.
- **V. The virtual surface and the square**: documents 46, 47, 48, 49, 50, 51, 52, 80.
- **VI. Weil positivity: certificates, bridges and obligations**: documents 59, 60, 65, 66, 67, 68, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 81 and the essays on amplification, correlations and paths.
- **VII. Tools, governance and reviews**: documents 20, 31, 34, 36, 37, 42, 44, 55, 62, 69, 82.

## Reproduce and verify

Python 3.12 or later with `numpy`, `scipy`, `pandas`, `matplotlib`, `mpmath`, `sympy` and `python-docx` (see `requirements.txt`).

```bash
pip install -r requirements.txt
cd 3_Preuves_et_calculs && python tests/run_all_tests.py && cd ..
python -B 2_Methode/Outils/integrate_v659.py
python -B 2_Methode/Outils/integrate_v655.py --rebuild
python -B 2_Methode/Pilotage/verify_contracts.py
python -B 2_Methode/Pilotage/verify_pilotage.py
python -B 2_Methode/Pilotage/verify_ciblage.py
sha256sum -c CHECKSUMS.sha256
```

## Licences

- **Code**: MIT licence, see `LICENSE`.
- **Texts, figures and data**: Creative Commons Attribution 4.0 International (CC BY 4.0), see `LICENSE-CC-BY-4.0.md`.
- © 2026 Vincent P. P. NOËL. To cite this work, see `CITATION.cff`.
