# Références précises des pièces à retrouver — V6.55

Les documents numérotés **1 à79 sont présents** dans la livraison récupérée. Les fichiers ci-dessous sont des pièces sources séparées non retrouvées dans les archives actuellement accessibles. Cette liste ne conclut pas à leur absence dans vos sauvegardes.

## Trois notes citées par les graphes

| Fichier exact à rechercher | Version | Document conservé |
|---|---|---|
| `V642_CERTIFICATION_LOCALE.md` | V6.42 | **66 — Un pli certifié et sa paire**, `66_UN_PLI_CERTIFIE_ET_SA_PAIRE.pdf` |
| `V642_CONTRAT_ARITHMETIQUE.md` | V6.42 | **66 — Un pli certifié et sa paire**, même PDF |
| `V643_PONTS_MATHEMATIQUES.md` | V6.43 | **67 — Construire des ponts avec Bellman**, `67_CONSTRUIRE_DES_PONTS_AVEC_BELLMAN.pdf` |

Emplacement attendu dans le corpus : `3_Preuves_et_calculs/preuves/`. Les graphes conservent aussi leurs anciens chemins relatifs.

## Dix-neuf scripts du relevé V649

| Fichier exact | Version indiquée par son nom | Dossier documentaire correspondant |
|---|---|---|
| `check_v642_certificate.py` | V6.42 | Document**66** — `66_UN_PLI_CERTIFIE_ET_SA_PAIRE.pdf` |
| `check_v647_links.py` | V6.47 | Document**72** — `72_CONCENTRATION_PROJETEE_ET_OPERATEUR_COMMUN.pdf` |
| `check_v648_links.py` | V6.48 | Document**73** — `73_OPERATEUR_COMMUN_TETE_SOURCES_ET_QUEUE.pdf` |
| `check_v649_links.py` | V6.49 | Document**74** — `74_COMPENSATION_MULTI_PREMIERS.pdf` |
| `run_v642_bellman.py` | V6.42 | Document**66** — `66_UN_PLI_CERTIFIE_ET_SA_PAIRE.pdf` |
| `run_v642_certification.py` | V6.42 | Document**66** — `66_UN_PLI_CERTIFIE_ET_SA_PAIRE.pdf` |
| `run_v643_bridges.py` | V6.43 | Document**67** — `67_CONSTRUIRE_DES_PONTS_AVEC_BELLMAN.pdf` |
| `v644_family_experiment.py` | V6.44 | Document**68** — `68_ARITHMETIQUE_DES_PASSAGES_ET_QUEUE_EFFECTIVE.pdf` ; dictionnaire69 associé |
| `v644_integer_tail.py` | V6.44 | Document**68** — `68_ARITHMETIQUE_DES_PASSAGES_ET_QUEUE_EFFECTIVE.pdf` ; dictionnaire69 associé |
| `v645_arithmetic_experiment.py` | V6.45 | Document**70** — `70_PONT_ARITHMETIQUE_ET_DETTE_DE_COUPLAGE.pdf` |
| `v645_compensation_directions.py` | V6.45 | Document**70** — `70_PONT_ARITHMETIQUE_ET_DETTE_DE_COUPLAGE.pdf` |
| `v646_fourier_joint_diagnostic.py` | V6.46 | Document**71** — `71_LEGO_REUTILISABLE_ET_PREMIER_CERTIFICAT_COMPLET.pdf` |
| `v646_lego_experiment.py` | V6.46 | Document**71** — `71_LEGO_REUTILISABLE_ET_PREMIER_CERTIFICAT_COMPLET.pdf` |
| `v647_concentration_experiment.py` | V6.47 | Document**72** — `72_CONCENTRATION_PROJETEE_ET_OPERATEUR_COMMUN.pdf` |
| `v647_operator_diagnostic.py` | V6.47 | Document**72** — `72_CONCENTRATION_PROJETEE_ET_OPERATEUR_COMMUN.pdf` |
| `v648_common_certificate_experiment.py` | V6.48 | Document**73** — `73_OPERATEUR_COMMUN_TETE_SOURCES_ET_QUEUE.pdf` |
| `v648_common_operator_diagnostic.py` | V6.48 | Document**73** — `73_OPERATEUR_COMMUN_TETE_SOURCES_ET_QUEUE.pdf` |
| `v649_joint_payment_experiment.py` | V6.49 | Document**74** — `74_COMPENSATION_MULTI_PREMIERS.pdf` |
| `v649_multi_prime_diagnostic.py` | V6.49 | Document**74** — `74_COMPENSATION_MULTI_PREMIERS.pdf` |

Emplacement attendu : `3_Preuves_et_calculs/scripts/`. Les scripts `check_*_links.py` contrôlent des raccords ; les autres portent les expériences ou certifications nommées.

## Huit modules du même relevé

Emplacement attendu : `3_Preuves_et_calculs/src/`. Leur nom seul ne suffit pas à affirmer une version de création ; il faut comparer les imports et l’archive originale.

- `bridge_planning.py`
- `certificate_lego.py`
- `common_operator_certificate.py`
- `domain_grammar.py`
- `multi_prime_compensation.py`
- `projected_concentration.py`
- `schur_bridge.py`
- `v642_intervalles.py`

## Quelles sauvegardes comparer en priorité ?

Chercher vos ZIP globaux des versions **V6.42 à V6.49**, en priorité une **V6.49 intacte** ou une version ultérieure contenant ces fichiers. Les noms exacts des ZIP intermédiaires ne sont pas attestés ici ; je ne les invente pas. Les noms de fichiers ci-dessus permettent une recherche même si le ZIP a été renommé.

Les archives anciennes accessibles et effectivement contrôlées ici (`RH_programme_v6_21.zip`, dossiers77 et78, exports79/corrélations/amplification) n’ont pas livré ces27 sources. V6.21 est antérieure à leur période ; les compléments77–79 ne remplacent pas nécessairement un ancien ZIP global.

La récupération se fera par comparaison des fichiers et conservation de leur provenance ; aucune pièce reconstruite ne sera présentée comme un original retrouvé.
