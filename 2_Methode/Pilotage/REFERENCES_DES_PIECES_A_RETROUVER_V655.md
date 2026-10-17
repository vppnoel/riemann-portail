## Intégration globale du 15 octobre 2026

La reconstruction V6.51 est maintenant intégrée au corpus global : programme, journal calculé, notice, sources et complément ZIP. Ouvrir [la page d’intégration](../../1_Presentation/RECONSTRUCTION_V651_INTEGREE.html). Les originaux manquants restent identifiés comme tels ; leurs remplaçants exécutables sont explicitement marqués RECONSTRUITS.

Les trois fichiers d’origine manquants du complément Amplification et les anciennes versions V6.54 différentes sont aussi conservés dans les archives, sans remplacer les versions courantes. L’inventaire `INTEGRATION_GLOBALE_20261015.json` relie chaque membre des six archives complètes fournies à une copie identique dans le corpus.

Les mentions « paquet séparé » et « ZIP global inchangé » présentes dans les journaux de reconstruction décrivent leur création antérieure ; la présente livraison les réunit désormais dans le ZIP global. Les numéros des documents et les identifiants d’idées restent inchangés.

# Pièces retrouvées et références restantes — V6.55

**Mise à jour du15 octobre 2026 : les30 pièces précédemment recherchées sont toutes retrouvées dans votre ZIP V6.50.**

L’inventaire complet a permis de réintégrer176 fichiers :96 données,10 notes de preuve,32 scripts,9 modules,8 tests et21 pièces d’archives. Les40 anciens fichiers divergents sont archivés ; les versions courantes sont conservées.

## Deux références V6.51 encore absentes

Les deux pièces suivantes restent absentes après comparaison des ZIP V6.50,
V6.51 et V6.52 et des compléments77/75 fournis :

- `3_Preuves_et_calculs/scripts/v651_verifier_pistes_globales.py`
- `3_Preuves_et_calculs/data/v651_pistes_globales_resultats.json`

## Les27 scripts/modules et les trois notes retrouvés

| Pièce | État |
|---|---|
| `3_Preuves_et_calculs/scripts/check_v642_certificate.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/scripts/check_v647_links.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/scripts/check_v648_links.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/scripts/check_v649_links.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/scripts/run_v642_bellman.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/scripts/run_v642_certification.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/scripts/run_v643_bridges.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/scripts/v644_family_experiment.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/scripts/v644_integer_tail.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/scripts/v645_arithmetic_experiment.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/scripts/v645_compensation_directions.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/scripts/v646_fourier_joint_diagnostic.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/scripts/v646_lego_experiment.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/scripts/v647_concentration_experiment.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/scripts/v647_operator_diagnostic.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/scripts/v648_common_certificate_experiment.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/scripts/v648_common_operator_diagnostic.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/scripts/v649_joint_payment_experiment.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/scripts/v649_multi_prime_diagnostic.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/src/bridge_planning.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/src/certificate_lego.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/src/common_operator_certificate.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/src/domain_grammar.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/src/multi_prime_compensation.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/src/projected_concentration.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/src/schur_bridge.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/src/v642_intervalles.py` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/preuves/V642_CERTIFICATION_LOCALE.md` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/preuves/V642_CONTRAT_ARITHMETIQUE.md` | Original retrouvé, empreinte vérifiée |
| `3_Preuves_et_calculs/preuves/V643_PONTS_MATHEMATIQUES.md` | Original retrouvé, empreinte vérifiée |

## Provenance

Archive fournie : `programme-riemann_github_v6_50(1).zip`. CRC intégral valide ;1 298 empreintes du manifeste interne vérifiées. Les1 299 chemins de cette archive sont désormais présents dans le corpus ; les originaux anciens divergents restent disponibles dans les archives.

Les documents 1–79, les articles PDF/LaTeX et les figures restent conservés. La récupération rétablit la possibilité de vérification ; elle ne prouve pas la loi globale de signe ni RH.

## Compléments V6.51 / V6.52 / 77 / 75 examinés

- `programme-riemann_github_v6_51.zip` est tronqué :803 entrées locales complètes,
  toutes vérifiées par CRC ; les enregistrements ultérieurs et le répertoire
  central sont absents. Il n’apporte aucun chemin nouveau récupérable.
- `programme-riemann_v6_52_RECUPERATION_TRANSPORT.zip` est complet :1 215 fichiers,
  CRC valides et1 214 empreintes du manifeste conformes. Ses versions divergentes
  sont archivées ; les programmes courants corrigés restent conservés.
- Le complément77 rétablit deux rapports originaux :
  `3_Preuves_et_calculs/recherche78/exploration/RAPPORT_SIGNE.md` et
  `3_Preuves_et_calculs/recherche78/critique/AUDIT_MECANISMES_UNIVERSELS.md`.
-100 anciennes versions ou pièces de paquet sont préservées sous
  `4_Archives/recuperation_v651_v652/originaux_differents/`.

Les preuves de provenance sont dans `RECUPERATION_2026_10_15_V651_V652.json`.
Le menu Documents ouvre désormais un catalogue de tous les fichiers et fiches,
avec recherche par type, identifiant d’idée, numéro de document et référence.
