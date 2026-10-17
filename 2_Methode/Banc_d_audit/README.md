# Banc d'audit (axe 2 du plan d'impact)

Contenu : `planted_errors.json` (corpus : 21 erreurs, 7 leurres), `PLANTED_ERRORS.md` (version lisible), `score_auditor.py` (notation), `example_findings.json` (exemple).
Complète les tests de rejet de `3_Preuves_et_calculs/` : `src/rejection.py` + `scripts/run_rejection.py` (Davenport–Heilbronn), `scripts/run_function_field_analog.py` (corps de fonctions), `scripts/run_generator_real_signal.py` (identification de modes sur signal réel), `tests/test_identities.py`.
Utilisation : `python score_auditor.py findings.json`.
Pour publier le banc : ajouter une licence et séparer les entrées dépendant de fichiers extérieurs (E13, E14, E16).
