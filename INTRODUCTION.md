# About this repository

*Vincent P. P. NOËL — October 2026, updated 23 November 2026*

> **Update, 23 November 2026.** Since the announcement, I have been trying to make part of the Lean proof readable for a human. Three notes, each written by Claude, checked by ChatGPT and accepted by me, are in [lean_reading/](lean_reading/README.md). The main one, in English, rewrites the analytic part of the proof, from the windowed bound (⋆) to GRH, with every step linked to the Lean code. It does not prove (⋆). Each check found real errors before acceptance; they are listed there. I also corrected two errors in my note on the announcement, both found by an adversarial review.
>
> I am also starting an experiment in which Claude and ChatGPT explain the Lean modules to each other, without my intervention, in a separate branch of my private repository. Nothing from it enters the corpus unless I review it through the usual process.
>
> **Update, 22 November 2026.** On 20 November 2026, Levent Alpöge announced a proof of the Generalized Riemann Hypothesis obtained with Claude, released as a Lean formalisation that has since been independently built and checked. No human-readable proof or peer review exists yet. What this changes for the corpus, and my attempt to explain *why* the proof works, are in [NOTE_ALPOGE_2026.md](NOTE_ALPOGE_2026.md).

## What this is

This is a personal research notebook on the Riemann zeta function, kept as a versioned corpus: documents, proofs, code, data, tests, and a log of how each piece was produced. I am not a professional mathematician. This is a hobby, and I am doing it mainly to learn.

Almost all of the work was done in dialogue with two AI systems, Claude (Anthropic) and ChatGPT (OpenAI). They proposed computations, wrote code, drafted text and checked each other. I chose the directions, read everything, and decided what was kept. I take responsibility for the content, including its errors.

I am publishing it for two reasons.

The first is mathematical. A few statements here may be useful or may be wrong, and I cannot tell which without readers who know the field.

The second is about method. As a neuroscientist, I am interested in how people come to believe things, and in the biases that can make a false theory look validated. Long collaborations between one person and AI systems are a new situation: the systems are fluent, agreeable, and can review each other without being truly independent. This corpus is a complete, dated record of one such collaboration, failures included. I think that record has value whatever the mathematics turns out to be worth.

## What it does not contain

There is no proof of the Riemann Hypothesis here, and none was attempted. The working question was a different one: what structure makes RH necessary, and what exactly is missing for zeta compared with settings where the analogue is proved (curves over finite fields). Since the announcement of November 2026, that question has become sharper rather than obsolete: a machine-checked proof shows that RH is true, not yet why.

## What is here, and how solid it is

Every result is labelled with one of three levels:

- **Proved**: a proof written out in a delimited setting, checked by the author and by AI cross-review. *No human specialist has refereed any of it yet.*
- **Measured**: computed in high precision, with the prediction written down before the computation. Not a proof.
- **Supposed**: a working hypothesis.

The piece most worth a specialist's time is **Paper 1** ([PDF](1_Presentation/articles/article1_mean_square_double_poles.pdf)). It studies the mean square of a summatory function whose Dirichlet series has a double pole at each zero of zeta, and states a double-pole analogue of Cramér's 1922 mean-square theorem. Under RH, the leading constant equals 4κ/3 if and only if all zeros are simple. If the announced proof of RH stands, this becomes unconditional: a criterion for the simplicity of the zeros, which remains open. I do not know whether this is already in the literature. A question about it on MathOverflow was closed as off-topic; the comments were about the style of the question (which read as AI-written) rather than the mathematics, which is a fair lesson and part of the record.

The other entry points are listed in [README_EN.md](README_EN.md) (English) and [README.md](README.md) (French). Most research documents are in French; the three papers and the entry layer are in English.

## How the work was done

- Each task starts with a written prediction and an explicit rejection criterion, recorded before any computation.
- AI work goes into a separate deposit area; another actor verifies it; I accept or reject.
- Failed runs and revised thresholds are kept, not deleted.
- Cross-review between the two AI systems did catch real errors (a misused bound, missing counter-examples, an overstated obstruction). It is not a substitute for independent human review, because the two systems share many blind spots.

The method is described in [document 82](1_Presentation/english/82_TARGETING_AND_DIVISION_OF_WORK.pdf).

## What would help

1. **Tell me if Paper 1 is known**, with a reference, or point out a gap in the proof of Theorem B.
2. **Try to break anything marked "proved" or "certified".** A counter-example is as welcome as a confirmation.
3. **Reproduce a computation.** Code and tests are in `3_Preuves_et_calculs/`; dependencies in `requirements.txt`.
4. **If you study research practice or AI-assisted reasoning**, the corpus can be used as a case: predictions, rejected tracks and the history of releases are all dated.

Please use [GitHub issues](../../issues) for any of this. Short and blunt is fine.

## Licence

Code (`*.py`, `*.js`, build scripts): MIT, see [LICENSE](LICENSE). Texts, figures and data: CC BY 4.0, see [LICENSE-CC-BY-4.0.md](LICENSE-CC-BY-4.0.md). To cite this work, see [CITATION.cff](CITATION.cff).

---

*AI use: this introduction was drafted with Claude from my own notes and instructions. I have read it and stand behind every sentence.*
