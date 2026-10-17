# 3 · Preuves et calculs

## V6.54 - Corrélations, identité et énergie

Le dossier `correlations_20261014/` contient les programmes, les résultats,
les contre-modèles exacts et les audits des deux lectures indépendantes.
L'identité de diviseurs est vérifiée symboliquement jusqu'à1000. L'énergie
est recoupée par deux formules et par une intégration indépendante.

Les diagnostics ne donnent aucune borne à l'infini. Les signes des deux
contre-modèles sont contrôlés par intervalles à400bits. Le critère classique
et sa preuve du sens borne vers RH sont dans
`../1_Presentation/CORRELATIONS_IDENTITE_ET_ENERGIE.md`.

Le registre transversal est `data/parcours_et_proprietes.json`, les61notices
historiques sont dans `data/notices_historiques_01_61.json`.
La note éditoriale courante est V6.54 ; les journaux originaux gardent leur
provenance scientifique, sans recalcul attribué à la correction de numéro.


Tout ce qui est vérifiable par exécution.

| Dossier | Contenu |
|---|---|
| `preuves/` | lemmes et théorèmes (`LEMMES_RIGOUREUX.md`, `THEOREME_TERME_DOMINANT.md`), analyses (`ALPHA_BETA_ANALYSE.md`, `H3_ANALYSIS.md`), comparaisons (`COMPARAISON_BCF.md`, `NB_GRAM.md`), tests de rejet (`DAVENPORT_HEILBRONN_TEST.md`, `MEMO_P2_2_WEIL.md`, `MEMO_P2_3_DENSITE.md`), bibliographie, note de synthèse (EN), dimension énergétique/fractale (`ENERGY_FRACTAL_DIMENSION.md`), trous ouverts (`KNOWN_GAPS.md`) |
| `src/`, `scripts/` | modules et scripts reproductibles |
| `data/` | sorties numériques des scripts |
| `tests/` | suite de 219 tests (lanceur : `python tests/run_all_tests.py` ; un fichier dont une dépendance manque est signalé « NON EXÉCUTÉ ») |

**Exécuter** (depuis ce dossier) :
```
pip install -r requirements.txt
python tests/test_identities.py
python -m pytest -q tests

# détecteur V6 DARK-ZETA / TOMO
python scripts/run_dark_zeta.py

# détecteur V6.2 PRIME-LOCK
python scripts/run_prime_lock.py
```
Les tests lisent aussi des fichiers de `../1_Presentation` et `../2_Methode` : ne pas séparer les dossiers.


## V6 — DARK-ZETA
Le premier détecteur est documenté dans `preuves/DARK_ZETA_DETECTOR.md`. Les sorties `dark_zeta_*` dans `data/` sont générées par `scripts/run_dark_zeta.py`. TOMO-3 brut est actuellement rétrogradé après calibration par surrogats à phases randomisées ; TOMO-2 est conservé comme diagnostic, pas comme invariant universel de multiplicativité.


## V6.2 — PRIME-LOCK
La note technique est `preuves/PRIME_LOCK_DETECTOR.md`. Le script `scripts/run_prime_lock.py` produit les sorties `prime_lock_*` et teste : support de `-F'/F` sur les puissances de premiers, loi locale de degré 1, eulérisation contrôlée et propagation vers le signal global. PRIME-LOCK est un détecteur de structure eulérienne locale ; il n'est pas un critère de RH.

## V6.3 — DUAL-LOCK / Résidu sombre

- `src/dual_lock.py` : compressions finies local/global de la forme explicite.
- `scripts/run_dual_lock.py` : scan adversarial DH, confirmations précises, comparaison aux zéros seulement post hoc.
- `tests/test_dual_lock.py` : symétrie, contrôle positif, témoin négatif DH.
- `src/dark_residual.py` : décomposition archimédien / conducteur / pôle / local et indice de cancellation.
- `scripts/run_dark_residual.py` : cas confirmés + sweep de stabilité.
- `tests/test_dark_residual.py` : fermeture de la décomposition, résidu DH, contrôle apparié.
- `preuves/DARK_RESIDUAL.md` : définition et garde-fous.

Statut après intégration : **62 tests passent**. Le Résidu sombre est un diagnostic de cancellation, pas un critère de RH.


## V6.3d — classement des instruments

Aucun de ces fichiers ne dépend de mpmath (évaluation des fonctions L par Euler–Maclaurin en double précision).

- `src/lock_witnesses.py` : témoins F6 et E2, compression de Weil pour des coefficients Λ_F quelconques.
- `src/zero_reconstruction.py` : évaluation de ζ, L(s, χ₅), DH ; signal TOMO reconstruit à partir des zéros ; même signal à partir des coefficients.
- `scripts/run_lock_independence.py` : les quatre coins (`data/lock_independence_*.csv`).
- `scripts/run_tomo_zero_reconciliation.py` : coefficients contre zéros (`data/tomo_zero_*.csv`).
- `scripts/run_tomo3_channels.py` : fermeture ternaire dans le canal t (`data/tomo3_bohr_closure.csv`).
- `scripts/run_zero_difference_resonances.py` : différences de zéros contre zéros de ζ (`data/zero_difference_*`).
- `scripts/compute_zeros_numpy.py` : zéros de L(s, χ₅) et de DH jusqu'à |t| = 600, avec contrôle par le principe de l'argument (environ 5 minutes).
- `scripts/audit_dh_zero_count.py` : comptage exact des zéros de DH pour t ≤ 200,5.
- `scripts/run_dip_width_full.py` (V6.3e) : demi-largeur du creux, profil sommé sur les zéros voisins (`data/zero_difference_width*.csv/.png`) ; `scripts/run_dip_width.py` : même ajustement avec un profil isolé (`data/zero_difference_dip_width.csv`).
- `tests/test_v63d_classification.py` : 16 tests.
- `scripts/compute_zeta_zeros_numpy.py` (V6.3f) : zéros de ζ jusqu'à t = 1500 (environ 1 minute) ; `scripts/run_dip_width_heights.py` : demi-largeur du creux par tranches de hauteur (`data/zero_difference_width_heights.csv/.png`, environ 2 minutes). À lancer dans cet ordre.

Ordre d'exécution : `compute_zeros_numpy.py`, `audit_dh_zero_count.py`, puis les quatre `run_*`.


## V6.4 — seuil τ_c (test de l'Atlas)

- `scripts/run_tau_threshold.py` : seuil par trois calculs (premiers ×2, zéros), dimensions 5 à 13, balayage en largeur, carte (τ, δ), témoins E2 et F6 ; sorties `data/tau_threshold*.csv/.png` (environ 4 minutes ; `--figure` pour la figure seule).
- `tests/test_v64_tau_threshold.py` : 6 tests.

## V6.4.1 — recoupement par mpmath

- `tests/test_v64_mpmath_crosscheck.py` : 3 tests (exige mpmath). `tests/test_identities.py` exige mpmath et sympy.

## V6.5 — famille modulo 7

- `src/family_mod7.py` : caractères modulo 7, sosie f₇, famille F_θ, fonctions de Hardy.
- `scripts/run_family_mod7.py` : carte des rencontres de paires, plage de survie, proportion sur la droite, trajectoire d'une paire, empreinte de ζ ; sorties `data/family_mod7*` (environ 2 minutes 30).
- `tests/test_v65_family_mod7.py` : 7 tests ; un test de recoupement ajouté dans `tests/test_v64_mpmath_crosscheck.py`.
- `scripts/run_family_mod7_proved_part.py` (V6.5.1) : zéros à droite de Re s = 0,75 et de Re s = 1 le long de la famille (`data/family_mod7_right_count.csv`, `_rightmost.csv` ; environ 13 minutes, à lancer en arrière-plan).

## V6.6 — le Modèle réduit (courbes sur les corps finis)

- `src/function_field.py` : corps F_{qⁿ} par tables de logarithmes, comptage de points de y² = f(x), polynôme P(u) par identités de Newton et équation fonctionnelle, sommes de puissances exactes, points fermés (Möbius), rapports de Castelnuovo ρ_n, plage de survie.
- `scripts/run_reduced_model.py` : vraies courbes, tour, faux jumeaux, plage de survie ; sorties `data/reduced_model_*` (environ 15 secondes ; `--figure` pour la figure seule).
- `tests/test_v66_reduced_model.py` : 7 tests (comptages recoupés par un calcul naïf indépendant sur F₃ et F₉, recompte d'une courbe de genre 3 sur F₈₁ et F₂₄₃, faux jumeaux, saturation exacte).

## V6.7 — STABILITY-RADIUS

- `src/stability_radius.py` : forme de Weil fenêtrée du Modèle réduit (Toeplitz des comptages), écriture de Chebyshev, rayon structuré en forme close, seuils de la forme et de l'objet, comptages d'Euler réels.
- `src/family_mod5.py` : trajets L(s, χ₅) → DH à symétrie de Hardy conservée.
- `src/dual_lock_audit.py` : ajout de `gram_matrix_closed` (Gram en forme close des tentes modulées).
- `scripts/run_stability_model.py` (environ 5 minutes ; 3 minutes de plus la première fois pour les courbes de genre 9 à 12), `scripts/run_rank_law.py`, `scripts/run_object_vs_form.py` (quelques secondes ; lit les sorties du premier). Sorties `data/stability_model_*`, `data/rank_law*`, `data/family_mod5_intervals.csv`, `data/object_vs_form.csv`, `data/structured_scaling.csv`.
- `tests/test_v67_stability_radius.py` : 8 tests.

## V6.8 — L'Archipel d'Euler

- `src/euler_archipelago.py` : caractères modulo q premier, nombres racines, fonctions de Hardy vectorisées (Hurwitz par Euler–Maclaurin), distance au zéro double en forme close, wronskien (dimension 2), raffinement par évaluation directe, défaut d'Euler au premier ordre, valeurs de F_c en tout point.
- `scripts/run_euler_archipelago.py` (environ 5 minutes) : espaces, rigidité, îles, contrôles, carte de V₇ impair ; sorties `data/archipelago_*.csv`, `data/archipelago.png`.
- `scripts/run_euler_right_of_one.py` (environ 15 minutes) : zéros dans Re s > 1 et Re s > 0,75 ; sortie `data/archipelago_right_of_1.csv`.
- `tests/test_v68_euler_archipelago.py` : 6 tests.

## V6.9 — Le chaînon

- `src/frobenius_chain.py` : traces depuis P (Newton), reconstruction GNS/Krylov du Frobenius depuis les comptages, masses spectrales, symétrie λ ↦ 1/λ, spectre des longueurs lu dans les zéros, coefficients de −F′/F, zéros périodiques d'une courbe.
- `scripts/run_frobenius_chain.py` (quelques secondes ; lit `stability_model_curves.csv`, `stability_model_fakes.csv`, `zeta_zeros_1500.csv` et les listes de zéros de L et DH) : sorties `data/chain_gns.csv`, `data/chain_length_spectrum.csv`, `data/chain_lengths.csv`, `data/chain.png`.
- `tests/test_v69_frobenius_chain.py` : 4 tests.

## V6.10 — Le générateur des premiers ; la base comme pas de temps (calculs)

- `src/prime_generator.py` : fonction test cos⁴ et sa transformée en forme close ; traces par les nombres premiers (formule explicite pour des fonctions test non paires) et par les zéros ; faisceau de Toeplitz ; masses spectrales.
- `scripts/run_prime_generator.py` (environ 2 minutes ; `--figure` pour la figure seule) : sorties `data/generator_summary.csv`, `data/generator_eigen.csv`, `data/generator_convergence.csv`, `data/generator_dh_metric.csv`, `data/generator_step.csv`, `data/generator.png`.
- `tests/test_v610_prime_generator.py` : 4 tests ; `tests/test_v610_navigateur.py` : 1 test (carte du navigateur et page).
- Suite 2 : voir V6.11.

## V6.11 — La base comme pas de temps

- `src/base_change.py` : traces sur F_q², reconstruction, polynômes de Weil réels, descentes, facteurs irréductibles.
- `scripts/run_base_change.py` (environ 90 secondes ; `--figure` pour la figure seule) : sorties `data/base_change.csv`, `data/base_metric_step.csv`, `data/base_step.png`.
- `tests/test_v611_base_change.py` : 3 tests.

## V6.12 — Les idées rejetées relues

- `src/prime_generator.py` : fonction `levinson` (innovations et coefficients de réflexion).
- `scripts/run_rejected_reread.py` (environ 90 secondes ; `--figure` pour la figure seule) : sorties `data/reread_levinson.csv`, `data/reread_levinson_summary.csv`, `data/reread_threshold.csv`, `data/reread_quadruplets.csv`, `data/reread_sources.csv`, `data/reread_theoremA.csv`, `data/reread.png`.
- `tests/test_v612_reread.py` : 2 tests.


## V6.34 — Contours directs et preuve des jets

- `src/relief_direct.py` : contour de la fonction complétée, domination du premier terme, raffinement de phase et comptage critique.
- `scripts/run_v634_relief_direct.py --part all` : sélection V7 et échantillon indépendant V11 ; plafonds 300 et 150. Caches facultatifs reconstruits au besoin.
- `scripts/run_v634_root_crosscheck.py` : six racines recoupées à 50 chiffres par mpmath.
- `src/jet_bound.py`, `scripts/run_v634_jet_bound.py` : optimisation sans connaître les points, puis certificats polynomiaux exacts.
- `preuves/LEMME_RANG_JETS_V634.md` : preuve complète ; erreur O(√p) pour les cubiques, méthode de Stepanov classique.
- `scripts/figure_v634.py`, `scripts/build_v634_document.py` : figure et texte du document 58 depuis les données.
- `tests/test_v634_direct.py` (5), `tests/test_v634_jets.py` (4). Protocole : `data/prevision_v634_relief.md`.


## V6.37 — Couples V13 fixés avant comptage

- `src/v637_apparie.py` : sélection sans zéros, géométrie exacte, calipers, analyse censurée sans imputation.
- `scripts/run_v637_apparie.py --run` : comptages au plafond 150, bord droit 9, pas 0,02/0,01/0,005 ; `--postchecks` vérifie notamment les monotonies.
- `scripts/run_v637_root_crosscheck.py` : 24 jobs prédéfinis, évaluateurs EM et mpmath indépendants, partenaires critiques.
- `scripts/build_v637_document.py`, `../2_Methode/Outils/build_v637_pdf.py` : document 61 et figures depuis les données.
- Le protocole original sous `../4_Archives/recus/V637/` conserve ses octets et son SHA-256 ; la copie affichable dans `data/` ne diffère que par le BOM.
- Les caches sont facultatifs. Les 11 nouveaux tests portent sur invariants, censure, intégrité et identités d’évaluation ; ils ne prouvent pas l’absence de zéros.
