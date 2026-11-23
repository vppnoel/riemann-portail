# Targeting and division of work — common procedure

*Riemann Programme V6.59 · 17 October 2026 · Vincent NOËL. English version of [CIBLAGE.md](CIBLAGE.md), which is the reference; document 82 is the reading version with the current state. Commands and file names are the same in both languages.*

## 1. Purpose

Work in short iterations, **independently of the AI in use**, and **divide the work** between the author, AIs and agents.

- **The corpus is the only memory.** A task is resumed from the files alone, without oral context or chat history.
- **No model name is assumed.** An actor is written `type:name`, with `type` = `auteur` (author), `ia` (AI) or `agent`.
- **One method.** This procedure merges the steering protocol (prediction written first, scope, review, indicator re-examined), the read-only targeting layer of the 16 October branch, and the roles and safeguards of the *multi-agent protocol* of 5 October (`2_Methode/Protocole_multi_agents_et_panorama_physique_RH.docx`).

## 2. The loop

| Step | Who | Command | Effect |
|---|---|---|---|
| 1. Target | any actor | `python -B 2_Methode/Pilotage/ciblage.py` | Read-only report: calculation requests, Bellman choices, investigation front, proposed task cards. |
| 2. Open | coordinator | `taches.py ouvrir --par ACTOR` | Creates the proposed cards that have no card in progress (idempotent). |
| 3. Assign | coordinator | `taches.py assigner TAC-001 ia:name --par ACTOR` | One card, one producing actor. |
| 4. Predict | producer | `taches.py prevoir TAC-001 --par ia:name --texte "…"` | Time-stamped prediction **before** the work: what is expected, what would prove it wrong. |
| 5. Produce | producer | — | Work only in `2_Methode/Depot/TAC-001/`; `RAPPORT.md` required. |
| 6. Deposit | producer | `taches.py deposer TAC-001 --par ia:name --statut-propose STATUS` | The deposit is frozen by hashes. |
| 6a. Withdraw | producer | `taches.py retirer TAC-001 --par ia:name --motif "…"` | Only before any verification: the card goes back to "to be redone" so the deposit can be completed. The reason cites the discussion thread; the withdrawn deposit stays in the log. |
| 7. Verify | auditor, not the producer | `taches.py verifier TAC-001 --par agent:x --verdict conforme --note "…"` | Checklist in `TAC-001/verification/VERIFICATION.md`. |
| 8. Decide | author | `taches.py decider TAC-001 --par auteur:vincent-noel --decision acceptee` | Accepted, rejected or to be redone. |
| 9. Integrate | designated actor | `taches.py integrer TAC-001 --par … --pieces …` | The result enters the corpus under the steering protocol; the pieces are recorded. |
| 10. Retarget | — | `ciblage.py --actualiser-vues` | Views and `data/ciblage_courant.json` are rebuilt; the loop starts again. |

To hand a card to an AI or an agent, give it the corpus archive and the brief printed by `taches.py fiche TAC-001` (or `--verification` for the verifier; the producer is not named: blind review). `taches.py etat` shows the live state; `taches.py controler` checks the register, the log and the deposits.

## 3. The task card

Required fields: `genre` (calcul, investigation, lier_instance, verification_temoin, bibliographie, formalisation, redaction), `role`, `titre`, `question`, `entrees` (input files with their SHA-256 at creation), `sortie_attendue` (expected output) and `critere_rejet` (rejection criterion written in advance). Optional: `objet`, `domaine`, `commande` (bounded command), `temoin` (counter-witness), `budget`, `noeuds` (graph ideas).

The targeting fills these fields from the data. For a steering investigation, question, witness, expected output and refutation criterion are already pre-registered. For a Bellman study, the card first asks for an executable instance (`lier_instance`). For an unresolved calculation cell, it asks for the detailed balance.

Card statuses: open → assigned → deposited → verified → accepted → integrated; or to be redone, rejected, abandoned, stale (an input changed after creation).

## 4. Roles

From the multi-agent protocol: coordinator (opens and assigns, writes no proof), explorer (one reformulation, no shared context before depositing), auditor (adversarial check: circularity, disguised equivalence with RH, sign errors, hidden hypotheses), librarian (references checked on the original; "not found" is not "absent"), numerics (every test must be able to fail; no injected data), formaliser (only precise, frozen statements), rapporteur (no wording beyond the established status). One actor may hold several roles, **never producer and verifier of the same card**. Only the author accepts or rejects.

## 5. Rules

Enforced by `taches.py`: (1) expected output and rejection criterion exist at creation; (2) the prediction precedes the deposit; (3) the producer writes only in the deposit area, frozen by hashes; (4) a changed input makes the card stale; (5) the verifier differs from the producer; (6) only a declared author accepts or rejects, and acceptance requires a conforming verification; (7) every event is appended to a hash-chained log.

Method, for every actor: anti-circularity checks (Davenport–Heilbronn, function-field analogue, no injected answer, a negative witness, flag any statement equivalent to RH, every constant with its error); the proposed status uses the corpus vocabulary; independent explorers; stopping rule after three cycles of the same key without a new result; a documented failure is a result.

## 6. What the targeting reads and recommends

It reads the state without changing anything: no mathematical fact, indicator level or Bellman cost is written. It separates calculation requests (cells, Bellman studies — a Bellman study is not an executable programme until an instance, inputs and a bounded command are attached) from the investigation front (open investigations whose prerequisites are met; a prerequisite is met only by a positive outcome declared with its full scope: object, domain, norm, quantifiers, source; an investigation closed by refutation does not meet it). The files read are declared in `ciblage_contrats.json`; their reference hashes live in the steering's **single register** (`reviewed_source_hashes`).

## 7. Author's decisions (17 October 2026)

1. **A deposit area**: an AI or an agent never writes directly into the corpus.
2. **The author decides**: the verifier gives a verdict; acceptance or rejection belongs to the author.
3. **One method**: any later change to this procedure needs a proposal and the author's prior agreement.

## 8. Limits

These rules organise the work; they **do not check a proof** and are not access control (an actor declaring itself author is not authenticated; the guarantee comes from the chained log and the author's review). HTML views are snapshots of the last rebuild.
