# V6.37 — 2026-10-12 — Ancrage apparié V13

- Protocole et 72 couples verrouillés avant comptage : 36 couples A1 et 36 couples D, 6 ancres, 3 rayons ; six témoins supplémentaires.
- A1 : 36/36 détections plus tardives pour de grands contrastes. D : 25 précoces, 8 tardives, 3 mêmes tranches ; tendance majoritaire et hétérogène, pas absence de signal.
- Totaux aux pas 0,02/0,01 et critiques aux pas 0,02/0,01/0,005 concordants ; monotonies, marges échantillonnées et censures relues. 24 racines représentatives recoupées à 50 chiffres de travail.
- Document 61 ; sélection, CSV, NPZ, rapports, relecture interne et 11 tests supplémentaires. Prochain coup : premier coefficient complexe exactement constant.
- Le premier vrai zéro et l’absence de zéros ne sont pas certifiés ; aucune preuve de RH ni nouvelle publication externe.

---

# V6.33 — 2026-10-11 — La force qui abaisse le relief

Demande de l'auteur : mesurer si la hauteur T* du relief suit le défaut de multiplicativité.
- `1_Presentation/57_LA_FORCE_DU_RELIEF.md/.pdf/.png` : défaut de multiplicativité D (nul aux points d'Euler) sur la carte de V₇ impair. Les trois prévisions sont fausses : corrélation T*–D −0,31 ; à distance égale, plus de défaut va avec plus de hauteur (+0,38) ; le col des îles passe là où le défaut est fort. Après coup (non prévu) : à distance égale, la hauteur suit le premier coefficient |a(1)| (corrélation partielle +0,81) ; à |a(1)| égal, le défaut abaisse bien le relief (−0,24). Deux forces : un ancrage (a(1)) et une poussée (le défaut). À retester avec des prévisions sur V₁₁ ou V₁₃.
- Script `scripts/run_force_multiplicativite.py` ; prévisions `data/prevision_v633_force.md` ; données `data/force_multiplicativite.csv/.json` ; test `tests/test_v633_force.py` (1).

---

# V6.32 — 2026-10-11 — Les accents des fichiers .md

Demande de l'auteur : « Pourquoi tous les fichiers .md posent problème pour les signes diacritiques ? »
- Cause : les fichiers sont en UTF-8 valide, mais un fichier .md n'annonce pas son encodage. Ouvert directement dans un navigateur ou un éditeur Windows, il est lu dans l'ancien encodage Windows-1252 : « é » devient « Ã© ».
- Correction : la marque UTF-8 (BOM) est ajoutée à tous les fichiers .md (115, hors documents reçus, laissés intacts) par `2_Methode/Outils/md_utf8_bom.py` ; tous les scripts lisent désormais en « utf-8-sig » (avec ou sans marque) ; les générateurs écrivent leurs .md avec la marque. Pages produites inchangées.
- Test `tests/test_v632_encodage.py` (1).

---

# V6.31 — 2026-10-11 — Le relief de l'archipel, les formules de la matrice, la liste des figures, le dépôt GitHub

Demandes de l'auteur : préparer la publication sur GitHub (licence, README) ; les formules de chaque théorie en popup dans la matrice ; une liste des figures ; une seule vue 3D oblique pour l'archipel (« trois îlots, puis une grande île »).
- `1_Presentation/56_LE_RELIEF_DE_L_ARCHIPEL.md/.pdf/.png` : relief T*(u, v) de la carte de V₇ impair (hauteur de la première paire hors droite) ; un seul continent jusqu'à T = 144, trois îles dès T = 145. Prévisions : fausses avec le critère prévu (dominé par un bruit de bord : 75 % des points ont un déficit transitoire) ; critère persistant choisi après coup. Script `scripts/run_archipel_relief.py` ; prévisions `data/prevision_v631_relief.md` ; données `data/archipel_relief.csv/.json`.
- Matrice (doc. 44) : chaque théorie a sa formule (champ `formule`, LaTeX), rendue en MathML (`2_Methode/Matrice/render_formules.js`) ; popup au survol ou au toucher du nom, et formule dans la fiche.
- `00_Liste_des_figures.html` et `1_Presentation/LISTE_DES_FIGURES.md` (générateur `2_Methode/Figures/build_figures.py`) : 29 figures des documents, 28 figures de calcul, 4 figures d’articles ; lien « Figures » dans la barre de navigation.
- Publication : `LICENSE` (MIT, code), `LICENSE-CC-BY-4.0.md` (textes, figures, données), `CITATION.cff`, `requirements.txt`, `.gitignore` ; README d'accueil bilingue. La copie publique (préparée à part) exclut le document reçu de tiers et remplace l'adresse électronique personnelle dans trois fichiers ; détail dans `4_Archives/NON_PUBLIE.md` de cette copie.
- Test `tests/test_v631.py` (1).

---

# V6.30 — 2026-10-11 — Les articles présentables

Demande de l'auteur : « Prépare les articles présentables » ; lettre avec « Cher Professeur », sans nom.
- `1_Presentation/articles/` : article 1 (*A mean square with double poles at the zeros of ζ*, 10 pages : Théorèmes A et B, corollaire B′, identité de Nyman–Beurling, Q(X) jusqu'à 10⁸) et article 2 (*Prime-side Weil forms in finite windows*, 6 pages : dictionnaire C × C, proposition d'inertie des faux polynômes, 180 réglages avec le témoin DH), en LaTeX et PDF ; lettres `lettre_FR.txt` et `letter_EN.txt` ; liste des vérifications à faire avant envoi (`LISEZMOI_ARTICLES.md`) ; scripts des figures (`figures/`).
- `1_Presentation/55_ARTICLES_PRESENTABLES.md/.pdf` : présentation. Correctif au doc. 52 : le seuil de DH se situe entre X ≈ 20 et X ≈ 56 (47 réglages sur 48 dès X ≥ 55,7), et non à 61.
- Portail : le dossier des articles est rattaché au document 55. Test `tests/test_v630_articles.py` (1) : les chiffres des articles sont recoupés avec les données.

---

# V6.29 — 2026-10-11 — Le trou à trois, lu ; les proportions de 2026 ; la matrice complétée

Demande de l'auteur : « Suites ».

- `1_Presentation/54_LE_TROU_A_TROIS_LU.md/.pdf/.png` : la correction de Bogomolny et al. prise dans son domaine (CUE de taille N ≥ 3) donne un déficit de triples serrés du bon sens mais trop faible (CUE(3) : 0,0082, soit 8,8 attendus pour ζ ; 0 observé) ; le rapport de deux écarts consécutifs (Nishigaki 2025), insensible à l'échelle et au dépliage, s'écarte aussi du noyau sinus (ζ +2,7σ, L(χ5) +4,4σ, Δ +5,2σ) : le trou à trois est une rigidité de forme. Prévisions : B1 juste, B2 et B3 fausses ; prévision du navigateur tenue. Les deux tiers d'Alpöge–Furman : sous forme normalisée, la borne rang–trace est une fonction des marges des paires (identité). Matrice : 11 cases sourcées, dont Mertens ⇔ RH (Titchmarsh, cité de mémoire) et DH ✗ proportion (Bombieri–Hejhal) ; ligne « Lindelöf pour les premiers ».
- Registre : 160 fiches (Nishigaki 2025, Bogomolny–Keating 2013, Atas et al. 2013). Navigateur : trois coups faits ; ouverts : « Le trou à trois par la formule à trois points de Bogomolny–Keating », « Compléter la matrice, deuxième séance ». Plan (doc. 43) adapté.
- Script `scripts/run_bblm_trou_a_trois.py` ; prévisions `data/prevision_v629_bblm.md` ; résultats `data/bblm_trou_a_trois.json` ; test `tests/test_v629_bblm.py` (1) ; le test de la matrice de la V6.19 vérifie désormais la transitivité sur Weil × Nyman–Beurling, la case Weil × Li étant écrite.

---

# V6.28 — 2026-10-11 — Axe A : la Rencontre à n en hauteur

- `1_Presentation/53_LA_RENCONTRE_EN_HAUTEUR.md/.pdf` : la formule det[D_N] prolongée à la taille effective de Bogomolny et al. (N ≈ 1,0–1,26) donne des densités négatives : modèle inutilisable à ces hauteurs (les trois prévisions sont fausses). Fait mesuré, le trou à trois : triples de zéros consécutifs de portée < 1 : ζ 0 pour 15,6 attendus (t ≤ 1 500), L(χ5) 0 pour 7,2, Δ 3 pour 31,1 ; le CUE de taille 20 et 60 suit le noyau sinus (la taille finie seule ne crée pas le trou).
- Navigateur : axe A fait ; « Lire Bogomolny et al. pour de vrai » ouvert. Script `scripts/run_rencontre_hauteur.py` ; prévisions `data/prevision_v628_hauteur.md` ; résultats `data/rencontre_hauteur.json` ; test `tests/test_v628_hauteur.py` (1).

---

# V6.27 — 2026-10-11 — J6 : le carré, en continu

- `1_Presentation/52_J6_LE_CARRE_EN_CONTINU.md/.pdf/.png` : surface virtuelle recalculée sur 180 réglages fiables (4 largeurs, 3 pas, 5 fenêtres, jusqu'à X = 3 000) ; ζ : une seule direction positive dans 60 réglages sur 60 ; L(χ5) : aucune (60/60) ; DH : directions en trop dès X ≥ 61 (39/39). Le nombre de directions en trop de DH dépend du pas et de la largeur (prévision P3 fausse) : il n'est pas un invariant. Axe A reformulé (N_eff ≈ 1).
- Script `scripts/run_carre_continu.py` ; prévisions `data/prevision_v627_carre.md` ; résultats `data/carre_continu.csv/.json` ; test `tests/test_v627_carre.py` (1).

---

# V6.26 — 2026-10-11 — J3b : le Frobenius de caractéristique un

- `1_Presentation/51_J3B_LE_FROBENIUS_DE_CARACTERISTIQUE_UN.md/.pdf` : lecture ciblée (Arithmetic Site, caractéristique un et entropie, semi-anneaux thermodynamiques) ; le Frobenius de caractéristique un est un automorphisme pour tout λ > 0, il dilate les pentes et n'annule aucune dérivation : il ne fournit pas l'élément dont Stepanov a besoin (prévision tenue). J3 sous la forme de Stepanov est écarté ; l'axe J revient à la route de Weil, celle de Connes–Consani (positivité sur le carré) ; prochain coup J6, le carré en continu.
- Registre : 157 fiches (Connes–Consani 2009 et 2014, Marcolli–Thorngren). Navigateur : J3b fait, J3 dans les pistes écartées, J6 ouvert. Registre des métaphores : Le Frobenius trop bon.

---

# V6.25 — 2026-10-11 — Les unités fictives : audit du document reçu

- `1_Presentation/50_LES_UNITES_FICTIVES_AUDIT.md/.pdf` : script relancé en lecture seule sur la V6.24, résultats identiques ; formules vérifiées ; le bilan K + Q = Σ W_n est une sommation par parties (identité vraie pour toute suite) ; masses négatives = directions négatives de la métrique = directions positives en trop de la surface virtuelle ; borner le travail total revient à borner Q, donc à RH ; l'analyse dimensionnelle désigne 2Θ − 1 comme seul nombre sans unité du Théorème A, sans en fixer la valeur.
- Test `tests/test_v625_unites.py` (1).

---

# V6.24 — 2026-10-11 — Analyse de risques, J3 simplifié, les deux tiers, documents de description

- `1_Presentation/49_ANALYSE_DE_RISQUES_J3_ET_LES_DEUX_TIERS.md/.pdf/.png` : tableau de décision (J3 par petites étapes, axe A en parallèle) ; J3a : l'additivité ne décide rien, ce qui compte est la présence de x^p dans l'espace des fonctions auxiliaires ; les 67 % sont d'Alpöge–Furman (rang–trace sur la forme de Weil, sans hypothèse), pas d'OpenAI ni d'un tamis ; le même calcul sur nos zéros : 56 % de simples à la fenêtre démontrée (théorie 50 %), 88 % à A = 2, 97 % à A = 4 ; mélange ζ·L(χ5) : 30 %.
- Documents de description mis à jour jusqu'à V6.24 : synthèse (01), cheminement intellectuel (06), guide de lecture (07, avec un glossaire étendu).
- Navigateur : J3a et « le même calcul » faits ; J3b (lecture ciblée de Connes–Consani) ouvert. Plan : J par petites étapes, A en parallèle.
- Script `scripts/run_v624.py` ; prévisions `data/prevision_v624.md` ; résultats `data/v624.json` ; tests `tests/test_v624.py` (2).

---

# V6.23 — 2026-10-11 — Axe J5 : le Frobenius qui n'est pas un morphisme

- `1_Presentation/48_LE_FROBENIUS_QUI_N_EST_PAS_UN_MORPHISME.md/.pdf/.png` : construction de Stepanov faite en algèbre linéaire exacte sur F_61 et F_101 ; avec le Frobenius, 13 à 52 fonctions auxiliaires (10 cas sur 12) ; avec l'identité (mêmes valeurs aux points) ou une permutation aléatoire, aucune (sauf deux coïncidences de rang) ; ce qui compte est l'inséparabilité (dérivée nulle). Prévisions : 3 justes (dont une à une exception près), 1 fausse (borne triviale aux tailles calculées). Note : les dimensions fictives du Théorème A sont la dimension énergétique (doc. 08) ; une dérivation fractionnaire ne la déplace pas.
- Plan : J5 fait, J3 précisé (l'action d'échelle a-t-elle une dérivée nulle ?). Navigateur, matrice, registre des métaphores (La Dérivée nulle) mis à jour.
- Script `scripts/run_frobenius_non_geometrique.py` ; prévisions `data/prevision_v623_frobenius.md` ; résultats `data/frobenius_non_geometrique.json` ; tests `tests/test_v623_frobenius.py` (2).

---

# V6.22 — 2026-10-11 — Axe J2 : le Riemann–Roch virtuel

- `1_Presentation/47_LE_RIEMANN_ROCH_VIRTUEL.md/.pdf/.png` : sur 425 courbes et 220 faux jumeaux, le long de la tour (m ≤ 80) : existence (Pic⁰ non vide) 2 jumeaux, Clifford 0, Stepanov–Bombieri 121, Stepanov + tordu quadratique 220 sur 220 (étage médian 4 ; Castelnuovo 3) ; aucune courbe en défaut. Prévisions : 2 justes, 2 fausses, 1 ajoutée entre les deux calculs (juste). Le lemme manquant pour ζ est formulé : une borne unilatérale de ψ(x) − x obtenue par une fonction auxiliaire, ce qui demande un Frobenius absolu.
- Registre : Connes–Consani 2022 et 2024, van der Geer–Schoof, Groenewegen (154 fiches). Matrice : lignes Stepanov–Bombieri, borne unilatérale des premiers, Riemann–Roch pour Spec Z. Navigateur : J2 fait ; J5 (le Frobenius qui n'est pas un morphisme) et J3 (la fonction auxiliaire pour les premiers) ouverts. Registre des métaphores : La Fonction auxiliaire, Le Frobenius absolu.
- Script `scripts/run_riemann_roch_virtuel.py` ; prévisions `data/prevision_v622_riemann_roch.md` ; résultats `data/riemann_roch_virtuel.csv/.json` ; tests `tests/test_v622_riemann_roch.py` (2).

---

# V6.21 — 2026-10-10 — Axe J : la surface virtuelle

- `1_Presentation/46_LA_SURFACE_VIRTUELLE.md/.pdf/.png` : dictionnaire démontré dans le Modèle réduit (fibres ↔ pôle, intersections ↔ puissances de premiers, genre ↔ terme archimédien ; orthogonalement aux fibres, forme d'intersection = −métrique des zéros) ; indice de Hodge vérifié pour 425 courbes sur 425, violé avec un surplus exact pour les 220 faux jumeaux ; surface virtuelle de ζ calculée depuis les premiers ≤ 439 : une seule direction positive ; DH : 2 puis 10 en trop. Dictionnaire classique (Weil, Bombieri, Connes) : redécouverte, signalée.
- Plan (doc. 43) : axe J en tête (J2 Riemann–Roch virtuel, J3, J4). Navigateur : coup fait « La surface virtuelle », coup ouvert « Le Riemann–Roch virtuel ». Matrice : ligne « Indice de Hodge de la surface virtuelle » ; ligne CF renommée « Modèle réduit (RH des corps de fonctions) ».
- Script `scripts/run_surface_virtuelle.py` ; prévisions `data/prevision_v621_surface.md` ; résultats `data/surface_virtuelle*.csv/.json` ; tests `tests/test_v621_surface.py` (2).

---

# V6.20 — 2026-10-10 — Le Palier recalculé, les pistes d'OpenAI, les redécouvertes

- `1_Presentation/45_LE_PALIER_RECALCULE_ET_LES_REDECOUVERTES.md/.pdf/.png` : palier recalculé jusqu'à 5·10⁶ (prévisions écrites avant : 2 justes, 2 à moitié) ; médiane 1,313 = 0,985 × 4/3, sans montée visible ; le 4/3 apparent est une compensation (b² ≈ 1,16, r_Q ≈ 0,72, queue ≈ 0,15) ; pics jusqu'à 3,27 × 4/3 là où A_N s'annule ; correctif à la clôture V5.6 ; recensement de 14 résultats retrouvés ici puis reconnus dans la littérature, avec documents du corpus et clés.
- Matrice (doc. 44) : 22 théories ; provenance « retrouvé puis reconnu » ; coin bleu et « OA » pour ce qui vient d'OpenAI ; lignes Archipel d'Euler, dimension ½ (Lapidus), Tamis à deux ; cases NB × simplicité (palier), DH × (★), Tamis × NB ; tableau « Ce que le programme a retrouvé ».
- Plan (doc. 43) adapté : correspondance des 27 pistes d'OpenAI avec les axes et la matrice ; axes H (Tamis à deux) et I (Palier et simplicité) ; ordre refait.
- Script `scripts/run_palier_quatre_tiers.py` ; prévisions `data/prevision_v620_palier.md` ; résultats `data/palier_quatre_tiers.csv/.json`, `data/palier_balayage.csv` ; tests `tests/test_v620_palier.py` (3).

---

# V6.19.1 — 2026-10-10 — La matrice plus lisible, avec la provenance

- Matrice (doc. 44) : chaque théorie et chaque relation porte sa provenance (littérature, recalculé ou vérifié ici, éventuellement nouveau, question ouverte, déduit), avec une note qui renvoie aux documents ; couleur au choix par provenance ou par type de relation ; cases déduites atténuées et masquables ; cases vides discrètes ; traits épais entre les groupes de force ; ligne et colonne éclairées au survol.
- En-têtes : lien ↗ vers le résumé de l'article principal de chaque théorie ; liste des 48 articles de la matrice avec leurs liens.
- Bilan : 8 théories recalculées dans le programme, 3 éventuellement nouvelles (Théorème A, critère (★), identité de la Rencontre à n), toutes à confirmer par la littérature ou une relecture.
- `build_matrice.py` : champs `apport` et `apport_note` (nœuds), `apport` (relations), contrôlés par `check()`.

---

# V6.19 — 2026-10-10 — Plan de recherche : la Rencontre à n et la matrice des théories

- `1_Presentation/43_PLAN_DE_RECHERCHE_LA_RENCONTRE_A_N.md/.pdf/.png` : identité démontrée (la marge d'un n-uplet est sa corrélation à n points du CUE(N)) ; triplets des zéros de ζ conformes au noyau sinus (χ² 1,34 ; Poisson 17,3) ; loi de superposition des Familles étrangères (χ² 0,87) ; déficit à basse hauteur ; sept axes avec prévisions, témoins et règles d'arrêt.
- `1_Presentation/44_MATRICE_DES_THEORIES.html` (générée par `2_Methode/Matrice/build_matrice.py` depuis `matrice_theories.json`) : 19 théories, 50 cases écrites, 144 déduites par transitivité, 148 à compléter ; fiche de chaque théorie selon les quatre temps de la méthode ; échelle de force.
- Navigateur : coup fait « La Rencontre à n » ; coups ouverts : la Rencontre à n en hauteur, Montgomery sans RH, les collisions du flot, lire les proportions de 2026, compléter la matrice. Registre des métaphores : La Rencontre à n, Le Carillon de Bohr. Registre des sources : Rudnick–Sarnak 1996 (150 fiches).
- Script `scripts/run_rencontre_a_n.py` ; prévisions `data/prevision_v619.md` ; résultats `data/rencontre_a_n.json`, `data/rencontre_a_n_zeta.csv` ; tests `tests/test_v619_rencontre_a_n.py`.

---

# V6.18.1 — 2026-10-10 — Toutes les références, au bon format

- `build_sources.py` : `fmt()` (format uniforme), `doc_refs()` et `sync_docs()` (section « Références » de chaque document) ; 7 fiches ajoutées ; clés ajoutées dans tous les documents numérotés ; corrections dans les documents 21, 29, 30, 39, 41.
- `build_sources.py` : `textes()` et `docx_text()` (documents Word seuls) ; `citations()` tient compte de `cite_aussi`. Sources d'OpenAI et documents Word : le registre lit aussi les documents qui n'existent qu'en Word (02 à 05, 09 à 13, dont les audits des réponses d'OpenAI). Dix fiches ajoutées, 149 au total : Maier–Rassias 2018, Conrey 2003 (Notices AMS), MathOverflow 400779 (non vérifiée : site bloqué), Gonek 1989, Platt–Trudgian 2021, Baluyot–Goldston–Suriajaya–Turnage-Butterbaugh 2024, B. Wang 2026 (deux prépublications), Pearce-Crump 2026, Besicovitch 1932 (non vérifiée). Liens d'OpenAI nettoyés du traceur utm_source.
- Test : la section « Références » de chaque document est à jour.

---

# V6.18 — 2026-10-10 — Les sources, la carte des croisements, les documents explicatifs

- `2_Methode/Sources/sources.json` et `build_sources.py` → `1_Presentation/42_REGISTRE_DES_SOURCES.md` (132 fiches). Vérifications du 10 octobre (48 par l'assistant, 84 par un agent, dont la transcription des bibliographies antérieures avec leur date d'origine). Clés insérées après les citations dans le texte (111). Note : deux séries d'agents ont été interrompues par une limite d'usage (15 h 09, 16 h 40) sans rien enregistrer ; le travail a été refait après 17 h 50, avec enregistrement au fil de l'eau.
- Indicateur : `crossings()` avec colonne Modèle réduit, liens vers les documents, pastilles de sources ; étape V6.18 (aucun niveau ne bouge).
- Navigateur : coups lire_Wei48, lire_Ham21, lire_Beu55 ; 7 coups et 7 pistes écartées venus de l'inventaire des pistes OpenAI (`origine`).
- Documents 01, 06, 07 réécrits en Markdown/PDF (anciens .docx/.pdf archivés) ; portail : ces documents et le registre en tête, publiés en ligne.
- Tests : `tests/test_v618_sources.py` (2).

---

# V6.17 — 2026-10-10 — La Rencontre en degré 2, et son pendant dans le Modèle réduit

- Demande de l'auteur : « Suite » : coups « La Rencontre en degré 2 » (3,00) et « La Rencontre dans le Modèle réduit » (2,00). Prévisions P1–P5 écrites avant tout calcul (`data/prevision_v617.md`, 11 h 55 UTC).
- `src/delta_contour.py` : le Contour tourné, Λ(6+it) = 2e^{−φt} Re(e^{6iφ} A(6+it)), φ = π/2 − 6/t, Gauss–Legendre par panneaux ; validé contre mpmath à t = 20, 100, 200, 612,3 et 1 001,7 (écart relatif ≤ 6·10⁻¹³).
- `scripts/compute_delta_zeros_contour.py` (~2 min) : 2 139 zéros jusqu'à 1 500, raffinement de Brent, examen fin des minima de |Z|, complétude de Turing (`delta_zeros_contour_audit.csv`). Correctif V6.15 : le générateur avait manqué 7 zéros entre 224 et 232 (note ajoutée au document 39).
- `scripts/run_rencontre_degre2.py` (~75 s) : CUE simulé (N = 200 et N petit), marges de Δ, de ζ·L(χ5) (réunion), angles de Satake (p ≤ 25 000), toutes les courbes y² = x³ + ax + b sur F_p (p = 101 à 503), étage 2, identités sur les 425 courbes de la V6.6 ; `degre2_*.csv`, figure `degre2.png`. Correction pendant le travail : les fils BLAS se marchaient dessus (QR 300 fois trop lent), un seul fil imposé.
- Indicateur : étape V6.17, degré 2 : 3 → 4 ; croisements rencontre_degre2, rencontre_locale, familles_etrangeres ; pendants de marge_heisenberg et ecoute. Navigateur : repulsion_degre2 et rencontre_modele_reduit faits ; nouveaux coups taille_effective_delta, loi_marge_genre2, dbn_degre2. Registre : 3 noms (87 opérateurs). Carte : nœud « La Rencontre en degré 2 ». Portail : document 41 en ligne.
- Tests : `tests/test_v617_degre2.py` (4) ; 158 au total, tous exécutés et réussis.

---

# V6.16 — 2026-10-10 — La Rencontre à trois, et les croisements dans l'indicateur

- Demandes de l'auteur : croiser les problèmes aussi difficiles que RH (simplicité, répulsion, degré 2) ; prendre les croisements en compte dans l'indicateur. Deux textes reçus (« Nécessité démontrée du Modèle réduit », « Classement des instruments 3D ») : lus ; vocabulaire d'ingénierie non repris ; trois règles gardées (carte à axes croisés, pendant dans le Modèle réduit, veille rétrospective).
- `scripts/run_rencontre_a_trois.py` (~6 min) : Z''/Z' et θ' aux 1 070 zéros (mpmath), β_k et sa part d'écart, marges 1 − sinc²(πs), comparaison GUE/Poisson, paire de Lehmer (zéros 6 709–6 710) et 223 zéros de 6 900 à 7 100, blocs dyadiques simulés, exploratoire sur la métrique des premiers ; données `rencontre_*.csv`, figure `rencontre.png` ; `data/prevision_v616.md` (10 h 54 UTC).
- Correction de lecture pendant le travail : les prévisions P2, P3, P5 portaient sur β entier alors que le contrôle préalable portait sur sa part d'écart ; β est lisse à 95 %. Erreur de calcul corrigée en cours de route (part d'écart divisée par |ρ|⁴ au lieu de |ρ|²).
- Indicateur : dimension « croiser », champs `conjectures`, `croisements`, `regle_croiser` ; niveaux rétroactifs (V6.5 : 4 ; V6.7 : 5 ; V6.13 : 6) ; carte des croisements et zones d'ombre dans le document 31 ; encart « Pas encore » et panneau des degrés remis à jour.
- Navigateur : `poids_croisement`, champ `croise`, colonne « Croisement », `pistes_ecartees` et section « Veille rétrospective », règle du pendant ; paires_lehmer devenu « La Rencontre à trois » (fait) ; nouveaux coups repulsion_degre2, rencontre_modele_reduit, constante_Q_modele_reduit.
- Registre : 3 noms (84 opérateurs). Carte des idées : nœud « La Rencontre à trois ». Portail : document 40 en ligne.
- Tests : `tests/test_v616_rencontre_croisements.py` (3) ; `tests/test_v613_relecture.py` adapté (la dimension « croiser », rétroactive, est exclue de la comparaison V6.12/V6.13) ; 154 au total, tous exécutés et réussis.

---

# V6.15 — 2026-10-10 — Le degré 2 et le recensement

- Demande de l'auteur : « Faire les deux points suivants » : les coups « Le temps de Heisenberg en degré 2 (Δ de Ramanujan) » et « La métrique des premiers, plus haut ». Prévisions P1–P6 écrites avant tout calcul (`data/prevision_v615.md`, 06 h 26 UTC).
- `src/delta_ramanujan.py` : τ(n) exacts (Jacobi, puissance 8 modulo six premiers, restes chinois), coefficients normalisés, terme archimédien Ω(r) = 2 Re ψ(6 + ir) − 2 log 2π, traces de L(Δ, s), Λ(6 + it) par les gamma incomplètes (mpmath).
- `scripts/run_delta_heisenberg.py` : contrôles de τ ; 13 zéros t ≤ 40 sans les premiers ; formule explicite (2·10⁻⁷) ; générateur (189 zéros, écart 1,2·10⁻⁹, loi de Weyl) ; quadruplets synthétiques sur L(Δ, s), ζ et ζ·L(s, χ₅). Correction pendant le travail : une première recherche de racines (méthode d'Anderson sur un intervalle) donnait quatre zéros faux à 4·10⁻³ ; remplacée par une dichotomie.
- `scripts/compute_dh_zeros_high.py` : zéros de DH de 600 à 1 700 (méthode V6.3d, principe de l'argument sur 55 bandes, toutes en accord) ; 18 puis 32 quadruplets hors droite.
- `scripts/run_metric_height.py` : recensement (DH 50, L 0, ζ 0 ; 0 après retrait des quadruplets ≤ 1 700), escalier, allumage de chaque quadruplet, attribution par le générateur (14 sur 15).
- Navigateur : heisenberg_degre2 et generateur_hauteur faits ; facteur_dh et degre2_archipel révisés (coût 2,5 → 2). Registre : 3 noms (81 opérateurs). Indicateur : étape V6.15, degré 2 : 2 → 3. Carte : nœud « Le degré 2 et le recensement ». Portail : document 39 en ligne.
- Tests : `tests/test_v615_degre2_recensement.py` (4) ; 151 au total, tous exécutés et réussis.

---

# V6.14 — 2026-10-10 — La loi de seuil : le temps de Heisenberg

- Coup du navigateur « La loi de seuil des innovations » (score 2,33), joué après la pré-relecture, à la demande « puis les autres ».
- `src/prime_generator.py` : `lmin_ratio`, `first_negative_size` (dichotomie sur λ_min, monotone par entrelacement), `heisenberg_length`. `scripts/run_detection_threshold.py` (~100 s) ; données `seuil_*.csv`, `seuil_prevision.md`, figure `seuil.png` ; `1_Presentation/38_LA_LOI_DE_SEUIL_LE_TEMPS_DE_HEISENBERG` (md + pdf + png).
- Correction : `scripts/run_rejected_reread.py` lit les seuils sur les valeurs propres (τ = 10⁻¹⁰) ; `reread_quadruplets.csv` (3,50 ; 3,91 ; 4,35 ; 4,17 ; 4,21 au lieu de 3,48 ; 2,71 ; 3,30 ; 2,78 ; 2,76) et `reread_threshold.csv` (a = 0,3 : 5,55 ; a = 0,2 : 5,05) régénérés ; correctif dans le document 36 ; `tests/test_v612_reread.py` mis à jour.
- Chemin : une première hypothèse (le seuil compte les zéros plus bas que le quadruplet) a été réfutée par le retrait de zéros ; la loi de Heisenberg, trouvée sur le fond de L(s, χ₅), a été pré-enregistrée avant les tests sur ζ, le pas, la largeur et le « trou » (P4 réfutée).
- Précision étendue (mpmath) : premier changement de signe exact stable à 80 chiffres (4,08), faux à 30 chiffres (3,63) ; le critère en double précision retarde de 0,1 à 0,16.
- Navigateur : loi_de_seuil fait ; nouveaux coups heisenberg_degre2, facteur_dh, devineur ; révisions de kalman_relu et generateur_hauteur. Registre : 3 noms (78 opérateurs). Indicateur : étape V6.14 (aucun niveau ne change). Carte : nœud « Le temps de Heisenberg ».
- Tests : `tests/test_v614_seuil.py` (3) ; 147 au total, tous exécutés et réussis.

---

# V6.13 — 2026-10-10 — La pré-relecture

- Demande de l'auteur : « Suis cette trajectoire avec les 3 relectures d'abord en parallèle puis les autres. » Les trois relectures : Théorème A, Théorème B, note sur l'Archipel (coup « Préparer la relecture » du navigateur).
- Méthode : trois agents indépendants, en parallèle, un résultat chacun ; preuve refaite pas à pas, contrôles numériques avec leur propre code, recherche d'antériorité, note anglaise envoyable et résumé français. Interrompus par une limite de session puis repris sans calcul lourd.
- Verdicts : A correct (3 retouches) ; B correct (4 retouches) ; Archipel correct sur le fond (§3.1 faux hors de V_q, trou comblable au §3.4). Aucune erreur dans A ni B : la réfutation pré-enregistrée n'a pas eu lieu.
- Nouveauté : A = analogue au second ordre de la caractérisation classique de Θ ; B = transposition de Cramér au pôle double ; corollaire 3.4 de l'Archipel = cas particulier de Saias–Weingartner, Th. 2 (Booker–Thorne, Th. 1.1, pour S₂₄). Nouveau, à faire vérifier : B′ (S ≥ 4κ, égalité ⟺ zéros simples) ; identité exacte de rigidité λ²(3Σβ² + |Σβu|²).
- Fichiers : `1_Presentation/relecture/` (7 fichiers), `1_Presentation/37_PRE_RELECTURE_A_B_ARCHIPEL` (md + pdf) ; corrections dans `30_ARCHIPEL_D_EULER` (md + pdf), `LEMMES_RIGOUREUX.md`, `ALPHA_BETA_ANALYSE.md` ; dans la note B, précision sur la constante de Cramér (somme avec multiplicité).
- Navigateur : preparer_relecture fait ; relecture (humain) a pour prérequis le dossier ; degré 2 recentré sur la rigidité et les îles (une question de relecture ajoutée). Classement : loi de seuil 2,33 ; métrique plus haut 1,75 ; île vue par les premiers 1,5 ; degré 2 1,36 ; Lehmer 1,0 ; loi du rayon 0,33.
- Carte des idées (version 6.13) : A, B, Archipel annotés « pré-relu », fiche « Relecture externe » réécrite, prochain coup mis à jour. Portail : document 37 et dossier de relecture en ligne. Indicateur : étape V6.13 (aucun niveau ne change).
- Tests : `tests/test_v613_relecture.py` (3) ; 144 au total, tous exécutés et réussis.

---

# V6.12 — 2026-10-10 — Les idées rejetées relues ; les priorités refaites

- Demande de l'auteur : « D'abord refaire les priorités au regard de la relecture. Voir aussi si les 3 idées rejetées ne peuvent pas être relues symboliquement au regard du dictionnaire des idées et voir ce que ça donne comme autres idées. » (Relecture : celle du corpus entier, pour le portail ; idées rejetées : les trois « diagnostics rétrogradés » de la carte.)
- `src/prime_generator.py` (`levinson`), `scripts/run_rejected_reread.py`, `data/reread_*`, `tests/test_v612_reread.py` (2 tests), `1_Presentation/36_LES_IDEES_REJETEES_RELUES` (md + pdf), figure `36_Les_idees_rejetees_relues.png`.
- Innovations (a = 0,04 ; h = 0,01 ; n ≤ 1 000) : horizons numériques (|E/E0| < 10⁻⁷) ζ 613, L 823, DH 529 ; |k| max avant l'horizon 0,755 (ζ), 0,791 (L) ; DH : première innovation négative n = 352 (fenêtre 3,52, premiers ≤ 36, E/E0 = −3·10⁻⁴), attribuée au quadruplet 85,7. Seuils par quadruplet seul : 3,48 ; 2,71 ; 3,30 ; 2,78 ; 2,76. Balayage (a, h) : 3,48 à 3,53 au pas fin pour des poids ≥ 2·10⁻⁵ ; retard ou pas d'alarme au pas double ou pour des poids infimes.
- Correction pendant le travail : une innovation de −4·10⁻⁹ pour ζ à n = 804 (puis −1,4·10⁻⁷ à n = 950) est du bruit numérique au-delà de l'horizon (métrique de taille 805 sans valeur propre négative, plus petite −10⁻¹⁵ relativement) ; la détection est désormais limitée à l'avant de l'horizon, avec un seuil |E/E0| > 10⁻⁷.
- Fantôme de V4.3 (Im ≈ 73,8) : valeur propre 73,955 + 0,008i, masse 1,3·10⁻⁹ ; 74,324982 et 85,699348 ± 0,308517i de masse 1.
- Théorème A au rayon spectral (valeurs propres de masse 1 à 10⁻⁶ près) : DH 0,308517 ; ζ 1,4·10⁻⁷ ; L 4,2·10⁻⁷.
- Navigateur : coups faits kalman_relu, sources_relues, theoreme_A_rayon ; nouveaux coups loi_de_seuil, ile_par_les_premiers, preparer_relecture ; degré 2 revu (coût 4 → 2,5, révision notée) ; registre : L'Innovation, Le Fantôme pesé, Le Rayon spectral (75 opérateurs).
- Carte des idées : les trois nœuds rétrogradés renvoient à leur relecture. Indicateur : étape V6.12 (aucun niveau ne change). Portail : document 36 en ligne.
- Tests : 141 au total, tous exécutés et réussis.

---

# V6.11.1 — 2026-10-10 — Le portail

- Demandes de l'auteur : « Que dois-je ouvrir pour consulter le travail de manière dynamique ? Y a-t-il un fichier d'index qui reprend tout de manière intelligente ? » ; « Et ils sont tous à jour, on peut passer de l'un à l'autre et vers les docs importants ? » (réponse : non ; la carte datait de la version 6.1, le navigateur ne renvoyait à aucune autre page).
- `2_Methode/Portail/build_portail.py`, `00_PORTAIL.html`, `3_Preuves_et_calculs/tests/test_v6111_portail.py` (2 tests).
- `00_Carte_des_idees.html` : partie « V6.4 à V6.11 · Nécessité et chaînon » (seuil τ_c, famille modulo 7, Modèle réduit, marges, Archipel, chaînon, générateur des premiers, base comme pas de temps, prochain coup, indicateur, navigateur, objet qui porte la métrique) ; statut « mesuré, reproduit » (jetons clair et sombre) ; fiches Positivité de Weil, Hilbert–Pólya et Kalman complétées ; version 6.11.1.
- Barre de navigation commune : `topnav()` dans `build_indicateur.py`, utilisée par l'indicateur, le navigateur et le portail ; ajoutée à la main dans la carte.
- Copie de publication : 104 fichiers, 8,6 Mo ; 678 liens vérifiés, aucun cassé.
- Indicateur : étape V6.11.1 (aucun niveau ne change). Tests : 139 au total, tous exécutés et réussis.

---

# V6.11 — 2026-10-10 — La base comme pas de temps ; le navigateur calibré

- Demande de l'auteur : « Ok on avance. Si des fichiers peuvent être supprimés fais-le » (après la proposition : rédiger la suite 2, puis ajuster le navigateur : calibration et distance au but).
- `src/base_change.py`, `scripts/run_base_change.py` (partie métrique selon le pas ajoutée), `data/base_change.csv` (colonne autres_courbes_meme_image), `data/base_metric_step.csv`, `data/base_step.png` (troisième panneau), `tests/test_v611_base_change.py` (3 tests), `1_Presentation/35_LA_BASE_COMME_PAS_DE_TEMPS` (md + pdf), figure `35_La_base_comme_pas_de_temps.png`.
- Modèle réduit sur F_q² : rang = zéros distincts de β² (525 et 220) ; unitaires 525 / 0 ; négatifs des faux jumeaux = hors cercle distincts / 2 (220) ; dimension qui baisse : 51 courbes (dont les 31 égales à leur tordue) ; zéros = courbe ∪ tordue (525) ; descentes {1 : 30, 2 : 440, 3 : 1, 4 : 48, 6 : 2, 8 : 3, 12 : 1} = choix de signes des facteurs irréductibles (525) ; autres courbes du corpus de même image : 0 ; courbes à descentes hors corpus : 55.
- Métrique selon le pas (a = 0,04) : ζ et L, 0 négatif à tous les pas ; DH à X ≈ 440 : 10, 4, 2, 0, 0, 0, 0 pour h = 0,01 … log 2 ; à N = 300 : 4, 8, 10, 10 pour h = 0,02 … 0,05 (premiers jusqu'à 3,5 millions).
- Navigateur : `chaine` (maillons et états), `poids_maillon`, champ `maillon` des coups, `prevision` pré-enregistrée, `refutation_tenue`, sections « Distance au but » et « Bilan : prévu contre obtenu » ; deux règles ajoutées ; test du navigateur étendu.
- Ménage : espace de travail, copies V6.3d à V6.9 (dossiers et zips) supprimées ; sorties : 29 fichiers isolés identiques à un fichier d'un zip conservé supprimés ; les zips de toutes les versions sont gardés.
- Indicateur : étape V6.11, aucun niveau ne change. Registre : Le Pas de base, La Descente, La Métrique noyée. Documents 32 et 33 : renvois au document 35.
- Tests : 137 au total, tous exécutés et réussis.

---

# V6.10 — 2026-10-10 — Le générateur des premiers ; navigateur de recherche

- Demandes de l'auteur : « Tenter les 3 suites envisagées. Par priorité explicative » (ordre retenu : générateur des premiers, bases q et q², degré 2) ; « repenser la démonstration comme un itinéraire… nos métaphores comme opérateurs symboliques, notre outil d'évaluation comme objectif » ; « finis le 1, puis laisse-le proposer une suite et dis ce que tu en penses ».
- `src/prime_generator.py`, `scripts/run_prime_generator.py`, `data/generator_*`, `tests/test_v610_prime_generator.py` (4 tests), `1_Presentation/33_LE_GENERATEUR_DES_PREMIERS` (md + pdf), figure `33_Generateur_des_premiers.png`.
- Audit premiers = zéros : 3,5·10⁻¹⁴ (ζ) ; 1,5·10⁻¹⁰ (L, DH, troncature des listes à 600).
- Fenêtre a = 0,04, h = 0,01, N = 600 (premiers ≤ 439) : ζ 226 / L 334 / DH 330 valeurs propres de masse 1, aucune fausse ; écart max 7,9·10⁻³ ; premiers zéros à quelques 10⁻¹⁰. DH : 16 zéros hors droite retrouvés (85,699348 ± 0,308517i à 6·10⁻¹⁰), 10 directions négatives (5 quadruplets, dont 240,4 vu par la métrique seulement). Attribution : Gram sur les seuls zéros sur la droite, 0 négatif (5 fenêtres) ; + k quadruplets : 2, 2, 4, 10, 10 = côté premiers.
- Convergence : premiers ≤ 4 → premier zéro ; ≤ 23 862 → 284 zéros de ζ sur 294 de la bande, écart ≤ 1,6·10⁻⁴. Fausses détections hors de la fenêtre principale : surtout des zéros mal localisés (0,015 à 0,06), deux vraies erreurs (L, X = 99).
- Corrections pendant le travail : masses par Vandermonde mal conditionnées quand des valeurs propres sortent du cercle (colonnes normalisées) ; une note intermédiaire attribuait les zéros manquants au creux de ĝ vers 235 : faux, quatre paires ont la bonne position mais une masse de 1,02 à 1,50, la cinquième est au bord de la bande ; la phrase « aucune fausse détection à partir de X = 99 » ne valait que pour ζ.
- Navigateur de recherche : `2_Methode/Navigateur/carte_navigation.json`, `build_navigateur.py`, `1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html`, `tests/test_v610_navigateur.py` ; 69 opérateurs lus dans le registre ; questions divergentes de V6.10 reliées aux coups ouverts. Classement : la base comme pas de temps (3,0), la métrique des premiers plus haut (1,0), le degré 2 (0,6), les paires de Lehmer (0,5), la loi du rayon (0,33).
- Suite 2 : calculs faits (`src/base_change.py`, `scripts/run_base_change.py`, `data/base_change.csv`, `data/base_step.png`), rédaction à venir.
- Interruption : limite d'usage atteinte le 9 octobre à 23 h 52, reprise le 10 à 0 h 01 sans recalcul.
- Indicateur : étape V6.10, case vide 3 → 4. Registre : Le Générateur des premiers, La Masse unité, Le Repliement, La Métrique en avance. Document 32 : renvoi au document 33.
- Tests : 134 au total, tous exécutés et réussis.

---

# V6.9 — 2026-10-09 — Le chaînon

- Demande de l'auteur : « C'est comme s'il manquait un opérateur symbolique entre la version discrète/réduite et la version continue/complète » ; « Essaie. On explorera le niveau deux plus tard. »
- `src/frobenius_chain.py`, `scripts/run_frobenius_chain.py`, `data/chain_*`, `tests/test_v69_frobenius_chain.py` (4 tests), `1_Presentation/32_LE_CHAINON_DU_DISCRET_AU_CONTINU` (md + pdf), figure `32_Le_chainon.png`.
- Reconstruction depuis N_1..N_{2g+5} : 749 objets ; courbes : écart ≤ 1,0·10⁻¹³, 524/524 unitaires ; faux jumeaux : écart ≤ 2,3·10⁻¹⁴, 0/220 unitaires (écart 0,18 à 1,24), négatifs = hors cercle / 2 (220/220) ; zéros confondus : rang = zéros distincts < 2g, masses 2, 2 et 2, 2, 1, 1 ; symétrie ≤ 1,4·10⁻¹³.
- Spectre des longueurs (fenêtre gaussienne) : ζ 1 070 zéros, 35 longueurs, écart 0,045, 4,4 % hors puissances de premiers (fond lisse) ; L(χ₅) 988 zéros, 0,006, 0,1 % ; DH 988 zéros (60 hors droite), 0,005, 45,6 % ; courbe F₃ 0,011 ; faux jumeau F₅ 0,016 (réseau intact) ; deux courbes 0,018.
- Corrections pendant le travail : la première courbe de F₃ retenue avait des traces nulles aux premiers étages (aucun pic visible) ; choix de la courbe aux traces les plus marquées. Étiquettes de figure superposées : mise en page refaite.
- Indicateur : étape V6.9 (aucun niveau ne change ; raisons précisées pour « comprendre » et « la case vide ») ; l'instantané garde désormais la raison la plus récente de chaque dimension. Registre : Le Chaînon, Le Spectre des longueurs, L'Axe par zéro distinct, La Métrique manquante. Documents 28 et 29 : renvois au document 32.
- Réexécution : sorties identiques au bit près. Tests : 129 au total, tous exécutés et réussis.

---

# V6.8.1 — 2026-10-09 — l'indicateur d'avancement

- Demande de l'auteur : garder l'analyse de l'avancement comme indicateur des étapes franchies, et l'appliquer à toutes les versions avec un lien vers les documents produits.
- `1_Presentation/31_INDICATEUR_D_AVANCEMENT.html` (généré), `2_Methode/Indicateur/indicateur_avancement.json` (niveaux, raisons, documents), `2_Methode/Indicateur/build_indicateur.py` (vérifie les liens ; variante sans liens pour une page publiée hors du corpus), `3_Preuves_et_calculs/tests/test_v681_indicateur.py`.
- 14 étapes, 51 liens vers des documents. Niveaux au 9 octobre : voir 4, comprendre 5, situer 6, degré 2 : 2, démontrer 6, case vide 3.
- Correction de l'instantané publié le 9 octobre au soir (niveaux du 7 octobre sous-estimés pour « comprendre », « situer » et « la case vide »).
- README : règle de mise à jour à chaque version. Carte des idées : lien. Tests : 125.

---

# V6.8 — 2026-10-09 — L'Archipel d'Euler

- Demande de l'auteur : « prochaine étape » (document 29, §10, suite 2) : la sortie de RH la plus proche peut-elle garder un produit d'Euler ?
- `src/euler_archipelago.py`, `scripts/run_euler_archipelago.py`, `scripts/run_euler_right_of_one.py`, `data/archipelago_*`, `tests/test_v68_euler_archipelago.py` (6 tests), `1_Presentation/30_ARCHIPEL_D_EULER` (md + pdf), figure `30_Archipel_d_Euler.png`.
- Espaces V_q, q premier ≤ 13 : dimensions 1 (q = 3 impair, q = 5 pair) à 6 (q = 13 impair) ; 27 points d'Euler en dimension ≥ 2 ; fonctions de Hardy réelles (défaut ≤ 6·10⁻⁸ jusqu'à |t| = 300).
- Rigidité au premier ordre : défaut u·u'·(χ' − χ)(m)·(χ' − χ)(n) (prouvé) ; valeur propre minimale 2,36 à 3,27.
- Îles : rayon par la distance au zéro double (forme close) ; correction pendant le travail : le minimum sur la grille (pas 0,005) et un raffinement parabolique sous-estimaient ou surestimaient certains rayons (jusqu'à un facteur 2,6) ; tous les minima locaux sont maintenant raffinés par évaluation directe. Contrôles : 27/27 à 0,95·r et à 1,05·r, 100/100 directions au hasard ; comptage = comptage lisse à ±1,4.
- Rayon médian : 0,091 (T = 25), 0,022 (100), 0,008 (300) ; pente médiane −0,77 ; 112 sorties sur 116 par une paire dans les 5 % d'écarts les plus petits.
- Carte de V₇ impair : sans paire hors droite sur 32 % (T = 50), 2,6 % (150), 1,0 % (300).
- Zéros dans Re s > 1 (|t| ≤ 300) : 0 aux points d'Euler ; de 42 à au moins 89 au point milieu de petit |a(1)| de chaque espace ; 0 au point milieu de grand |a(1)| (mais 0 à 7 zéros dans Re s > 0,75).
- Documents 28 et 29 : renvois au document 30. Registre : L'Archipel d'Euler, L'Île sans mer, Le Continent bas.
- Tests : 124 au total, tous exécutés et réussis.

---

# V6.7 — 2026-10-08 — STABILITY-RADIUS : la marge de la forme et la marge de l'objet

- Demande de l'auteur : lancer le programme STABILITY-RADIUS proposé dans une réponse reçue (rédigée sans la V6.6), d'abord dans le Modèle réduit, puis pour ζ, L(s, χ₅), DH.
- `src/stability_radius.py`, `src/family_mod5.py`, `gram_matrix_closed` dans `src/dual_lock_audit.py` ; `scripts/run_stability_model.py`, `run_rank_law.py`, `run_object_vs_form.py` ; `data/stability_model_*`, `rank_law*`, `family_mod5_intervals.csv`, `object_vs_form.csv`, `structured_scaling.csv` ; `tests/test_v67_stability_radius.py` (8 tests) ; `1_Presentation/29_STABILITY_RADIUS_MARGE_DE_LA_FORME_ET_DE_L_OBJET` (md + pdf), figures `29_*.png`.
- Modèle réduit : 100 courbes nouvelles sur F₃ (genre 9 à 12), recomptées ; forme de Weil fenêtrée exactement singulière pour L > 2g (|λ| ≤ 1,8·10⁻¹⁵, 525/525) ; loi d'inertie (900/900 en 60 chiffres, 220/220) ; marge de l'objet médiane F₃ 0,85 (g = 1) → 0,07 (g = 12) ; nulle pour 1 courbe sur 525 et 4 polynômes de genre 2 sur F₅ ; Euler bloque la sortie la plus proche pour 24/525.
- Trajets vers les faux jumeaux : seuil de la forme 0 exactement à L = 2g + 1 (220/220) ; seuil de l'objet médian 0,17 (genre 2).
- Loi de rang (725 mesures) : aucune valeur négative pour ζ, L, F6 ; pentes −0,8 à −0,9 décade par dimension excédentaire à W = 5 ; DH négatif dès m = 3 au voisinage de ses zéros hors droite, et à 14–21 unités quand m dépasse les zéros atteints de 4 à 9.
- L(s, χ₅) → DH : trajet + : 4 paires quittent la droite (θ = 0,280 ; 0,602 ; 0,646 ; 0,937), les 4 paires hors droite de DH ; trajet − : 29 rencontres.
- **Correctif** au document 26 : la décroissance de τ_c vers 0 avec W n'était vraie qu'à 85,7 ; ailleurs non monotone (jusqu'à 0,97 à W = 10). Section ajoutée en fin du document 26.
- Forme close de τ_c vérifiée (26/26, 10⁻⁹). Gram en forme close : identique à la quadrature à 10⁻¹⁵ pour T ≤ 200 ; la quadrature se dégrade à T = 1400 (aucun résultat antérieur à ces hauteurs).
- Document 28, §9 : suite 1 marquée faite (version discrète). Registre : Le Rang, Le Recensement, La Rencontre figée, Le Passage interdit.
- Tests : 118 au total, tous exécutés et réussis.

---

# V6.6 — 2026-10-08 — le Modèle réduit : signature d'une nécessité démontrée

- Demande de l'auteur : « Modèle réduit » (proposition 1 du §9 du document 27) — mesurer, là où RH est un théorème, ce qui la rend nécessaire.
- `src/function_field.py`, `scripts/run_reduced_model.py`, `data/reduced_model_*` (curves, tower, fakes, example, figure), `tests/test_v66_reduced_model.py` (7 tests), `1_Presentation/28_MODELE_REDUIT_NECESSITE_DEMONTREE` (md + pdf), figure `28_Modele_reduit.png`.
- 425 courbes y² = f(x) (genre 1 à 8 sur F₃, 1 à 5 sur F₅, 1 à 4 sur F₇) : N_(g+1) recompté = prédit, 425 sur 425 ; écart RH ≤ 7,9·10⁻⁹ ; Castelnuovo exact jusqu'à n = 60, 425 sur 425.
- Faux jumeaux (équation fonctionnelle, a_d entiers ≥ 0 jusqu'à d = 200, RH fausse) : 1 (F₃, g = 1), 17 (F₃, g = 2), 3 (F₅, g = 1), 199 (F₅, g = 2). Aucun réalisé par une courbe. En genre 2 : invisibles à l'étage 1, démasqués aux étages 2 à 5, tous |α| < q.
- Marge médiane 1 − max ρ_n (F₃) jusqu'à n = 10⁵ : de 8·10⁻¹¹ (g = 1) à 0,07 (g = 8) ; saturation exacte ρ_4 = 1 pour P(u) = 1 + 9u⁴.
- Plage de survie relative médiane (F₃) : 0,27 (g = 1) → 0,02 (g = 8).
- Correction pendant le travail : identités de Newton pour les sommes de puissances (indice de borne) ; test RH exact en entiers pour g ≤ 2 (racines doubles mal classées en flottant).
- Registre (document 20) : La Tour, La Positivité saturée, Le Faux jumeau entier. Document 27, §9 : proposition 1 marquée faite.
- Tests : 110 au total, tous exécutés et réussis.

---

# V6.5.1 — 2026-10-08 — ce qui est démontré ; sympy rétabli

- Question de l'auteur : qu'est-ce qui, parmi les choses démontrées, rend RH nécessaire ? Réponse rédigée au §8 du document 27 (tableau des résultats démontrés et de leur mécanisme : positivité sur un objet plus grand ; pour ζ, démontré jusqu'à Re s = 1).
- `scripts/run_family_mod7_proved_part.py`, `data/family_mod7_right_count.csv`, `data/family_mod7_rightmost.csv` : zéros à droite de Re s = 0,75 / de Re s = 1 pour 0 < t ≤ 1000 : θ = 0 : 0 / 0 ; θ = 0,5 : 12 / 0 ; sosie : 50 / 5 (le plus à droite : 1,0612 + 249,382i, confirmé par mpmath) ; θ = −0,5 : 127 / 71 ; θ = −1 : 173 / 139.
- sympy 1.14.0 installé depuis un fichier fourni par l'auteur (empreintes internes vérifiées) ; `tests/run_all_tests.py` exécute maintenant les 103 tests, tous réussis.

---

# V6.5 — 2026-10-08 — famille modulo 7 : RH ne tient qu'au point d'Euler

- Demande de l'auteur : lancer la piste 1 de l'Atlas, et lire les résultats selon son hypothèse (RH nécessaire à quelque chose de plus grand) plutôt que selon la distance à une preuve.
- `src/family_mod7.py`, `scripts/run_family_mod7.py`, `data/family_mod7*`, `tests/test_v65_family_mod7.py` (7 tests), `1_Presentation/27_FAMILLE_MODULO_7_POINT_D_EULER` (md + pdf), figure `27_Famille_modulo_7.png`.
- F_θ = (1 − θ)·L(s, χ₃) + θ·f₇, f₇ = (L(s, χ₁) + ε·L(s, χ̄₁))/(1 + ε) : même équation fonctionnelle pour tout θ (défaut 10⁻¹³), recoupé par mpmath (10⁻¹²).
- 958 zéros de L(s, χ₃) pour t ≤ 1000. Plage de survie : [−0,249 ; +1,32] à T = 25, [−0,0157 ; +0,240] à T = 200, [−0,0096 ; +0,072] à T = 1000.
- 451 bosses ; seuil contre écart normalisé : Spearman 0,71, pente 1,76 ; 89 des 100 seuils les plus bas négatifs ; loi en racine à la sortie (exposant 0,50).
- Proportion sur la droite : 100 % (θ = 0), 93,9 % (0,5), 86,6 % (sosie), 60,2 % (−1).
- Empreinte de ζ (déficit) : 12,4 % (θ = 0), 10,1 % (0,1), 2,0 % (0,5), 5,1 % (sosie).
- Tests : 101 au total, tous exécutés et réussis.

---

# V6.4.1 — 2026-10-08 — mpmath rétabli, recoupement

- mpmath 1.3.0 installé depuis un fichier fourni par l'auteur (wheel en Python pur, empreintes internes vérifiées).
- `tests/test_identities.py` : 47 sur 47 (les 7 tests qui exigeaient mpmath passent). sympy toujours absent de la session : `factorint` remplacé, dans le lanceur de la session, par une factorisation par divisions successives.
- `tests/test_v64_mpmath_crosscheck.py` (3 tests) : évaluateur maison contre mpmath (10⁻⁹) ; 1 070 zéros de ζ (comptage `nzeros` et valeurs `zetazero`) ; zéros de L(s, χ₅) et de DH jusqu'à 600, dont les 30 hors droite et les deux zéros bas de la V6.3d.
- Total : 93 tests, tous exécutés et réussis. Aucun résultat des versions V6.3d à V6.4 n'est modifié.

---

# V6.4 — 2026-10-08 — Atlas des métaphores : test du seuil τ_c exécuté

- Reçu de l'auteur : `24_Atlas_metaphores_physique_mathematique_V6.pdf`, rangé sous `1_Presentation/25_Atlas_metaphores_physique_mathematique_V6.pdf` (le numéro 24 était pris).
- `scripts/run_tau_threshold.py`, `data/tau_threshold*.csv/.png`, `tests/test_v64_tau_threshold.py` (6 tests), `1_Presentation/26_SEUIL_TAU_C_TEST_DE_L_ATLAS` (md + pdf).
- Seuil τ_c (dimension 5) : 0,674 (T = 86), 0,910 (113), 0,955 (167), 0,872 (176). Zéros = Gauss–Legendre à 1,2·10⁻⁷ ; quadrature adaptative à 4,3·10⁻⁴ (T = 176).
- λ_min(τ) concave ⇒ seuil unique ; espaces emboîtés ⇒ τ_c décroît avec la dimension (−1 à −6 % de 5 à 13) ; largeur W du support : aucun seuil à 1,5 ; 0,87 ; 0,67 ; 0,30 ; 0,018 ; 0,0039 ; 0,00017 de W = 2 à 10. Lecture : critère de Weil, le seuil mesure la résolution de la fenêtre.
- τ_c = a/(a − b) (masse des zéros de L contre celle des zéros de DH) : les zéros ne bougent pas, pas de transition de phase.
- Carte (τ, δ) : M_q = log(q/π)·G ⇒ λ_min(τ, δ) = λ_min(τ) + δ·log(5/π), vérifié à 10⁻¹².
- Témoins : ζ → E2 a un seuil, ζ → F6 n'en a pas.
- Précision sur le document 23 : l'écart de 1,4·10⁻⁶ à T = 176 venait de la quadrature adaptative (Gauss–Legendre : 2·10⁻⁹).
- Tests : 90 au total ; 83 exécutés et réussis, 7 exigent mpmath.

---

# V6.3f — 2026-10-08 — le cas de ζ tranché : la largeur du creux selon la hauteur

- Calcul relancé à la demande de l'auteur : `scripts/compute_zeta_zeros_numpy.py`, `data/zeta_zeros_1500.csv` (1 070 zéros pour t ≤ 1500, tous sur la droite, complétude contrôlée dans 75 bandes ; les 300 premiers coïncident avec `zeros_300.csv` à 10⁻¹² près).
- `scripts/run_dip_width_heights.py`, `data/zero_difference_width_heights.csv/.png` : demi-largeur du creux par tranches de hauteur de 300. ζ : 0,73 ; 0,61 ; 0,60 ; 0,55 ; 0,51 (± 0,04), amplitude ajustée/attendue de 1,8 à 1,0. L(s, χ₅) : 0,56 ; 0,49. Paires hautes et cibles basses pour ζ : 0,53 ± 0,03. Attendu : 0,5.
- Conclusion : le désaccord de ζ en V6.3e (0,68 avec 300 zéros) tenait aux basses hauteurs. Le test passe pour ζ et L aux hauteurs atteintes. Reformulation de RH, mesurée sur des zéros déjà connus sur la droite : aucun progrès vers une preuve.
- Doc 24 §7.4 complété (tableau, figure `24_Largeur_selon_la_hauteur.png`) ; doc 20 : « Le Pied à coulisse » mis à jour. Tests : 1 ajouté (84 au total ; 77 exécutés et réussis, 7 exigent mpmath).

---

# V6.3e — 2026-10-07 — une idée hors cadre, testée

- Doc 24, §7.4 : la demi-largeur du creux des différences de zéros vaudrait 1 − β (profil tiré de Re (ζ′/ζ)′(1 + ir), heuristique citée de mémoire). Ajustement complet (`scripts/run_dip_width_full.py`, profil sommé sur les zéros voisins, trois fenêtres) : 0,53 ± 0,02 pour L(s, χ₅) (accord, amplitude à 10 %), 0,68 à 0,71 pour ζ (désaccord, amplitude presque double), 0,63 à 0,67 ± 0,08 pour DH. Ajustement simplifié (`scripts/run_dip_width.py`, un profil isolé, six réglages) : 0,51 à 0,63 (ζ), 0,41 à 0,47 (L), 0,47 à 0,60 (DH) ; moins fiable. Largeur 0,3 exclue pour ζ et L. Statut : test non concluant ; reformulation probablement circulaire.
- Un calcul des zéros de ζ jusqu'à t = 1500, lancé pour trancher le cas de ζ, a été interrompu par l'auteur ; ses sorties ne sont pas dans le corpus.
- Deux pistes notées, non exécutées : programme de Dyson (quasi-cristaux, Kurasov–Sarnak comme cinquième témoin) ; exporter la méthode du double comptage.
- Doc 20 : nom « Le Pied à coulisse ». Tests : 2 ajoutés (83 au total ; 76 exécutés et réussis, 7 exigent mpmath).

---

# V6.3d — 2026-10-07 — classement des instruments, quatre coins, correction des zéros de DH

- `1_Presentation/24_CLASSEMENT_DES_INSTRUMENTS_V6_3D.md` (+ figure `24_Differences_de_zeros.png`).
- Quatre coins : `src/lock_witnesses.py`, `scripts/run_lock_independence.py`. F6 = (1 + 6^(1/2−s))ζ : fuite 0,089, λ_G > 0 ; E2 = (1 − 2^(0,8−s))(1 − 2^(0,2−s))ζ : fuite nulle, λ_G ≈ −1,4 à −1,5. Côté premiers = côté zéros à 1,9–4,0·10⁻⁹.
- TOMO-2 : `src/zero_reconstruction.py`, `scripts/run_tomo_zero_reconciliation.py`. Signal reconstruit à partir des zéros (écart ≤ 1,1·10⁻⁸) ; entropies identiques ; zéros hors droite de DH = 18 % de l'énergie (σ = 0,01) et tout l'excès d'entropie sur L.
- TOMO-3 : `scripts/run_tomo3_channels.py` (fermeture ternaire = défaut multiplicatif dans le canal t) ; `scripts/run_zero_difference_resonances.py` (déficit des différences de zéros près des zéros de ζ : 0,70 pour ζ, 0,83 pour L, 0,95 pour DH ; témoins à 1,00).
- **Correction** : `data/dh_zeros.csv` complété par t = 5,094160 et t = 8,939914 (manquants depuis la v3.3). Le comptage « 129 » de la V6.3b était faux : 130 pour 0 < t ≤ 200,5 (`scripts/audit_dh_zero_count.py`). Corrigé dans : doc 23, README, `DAVENPORT_HEILBRONN_TEST.md`, `SYNTHESIS_NOTE_EN.md`, banc d'audit (E12 réécrite), `generator_real_signal.csv` (régénéré). L'audit DUAL-LOCK est inchangé (≤ 7·10⁻⁷).
- Nouvelles listes : `data/L_chi5_zeros_600.csv` (988 zéros), `data/dh_zeros_600.csv` (494 zéros, 15 paires hors droite), complétude contrôlée dans 90 bandes (`scripts/compute_zeros_numpy.py`, sans mpmath).
- Tests : `tests/test_v63d_classification.py` (13) ; `run_all_tests.py` signale les fichiers non exécutables. Session de production : 74 tests exécutés et réussis sur 81 (34 hors `test_identities.py` ; 40 de `test_identities.py` avec un module de remplacement pour mpmath/sympy) ; 7 tests exigeant mpmath non relancés (registre de paquets bloqué).
- Docs 15, 17, 18 : renvois ; doc 20 : quatre noms proposés ; carte des idées : liens.

---

# V6.3c — 2026-10-05 — choses simples

- `scripts/compute_L_chi5_zeros.py`, `data/L_chi5_zeros.csv` (334 zéros) ; audit L(s, χ₅) ajouté à `run_explicit_formula_audit.py` (écarts 1,1·10⁻⁸ à 9,3·10⁻⁸, λ_G positifs) ; zéro manquant t = −119,999 détecté par l'audit puis confirmé par comptage de changements de signe.
- Doc 21 : référence Kim et al. arXiv:2607.24830 et Suzuki arXiv:2606.09096 ; doc 23 : §8 (contrôle L) et §9 (positionnement : Connes–Consani–Moscovici, Connes–van Suijlekom).
- Doc 22 : « certifié » → « vérifié par recoupement ».
- Doc 20 : annexe B (lexique v6.0) et carte ; `tests/run_all_tests.py` ; pytest facultatif dans requirements ; tests 68/68.

---

# V6.3b — 2026-10-05 — audit des conventions de la formule explicite (DUAL-LOCK)

- `scripts/run_explicit_formula_audit.py` ; données `explicit_formula_audit.csv`, `explicit_formula_attribution.csv` ; tests `tests/test_explicit_formula_audit.py`.
- Côté premiers (compression_accurate) = côté zéros (Σ_ρ H_i(γ)H_j(γ)) : ζ 5·10⁻⁹ (T = 20, 40) ; DH ≤ 1,4·10⁻⁶ (T = 86, 113, 167, 176). Conventions validées (Fourier, 2π, gamma, conducteur, pôle, Λ_f de DH).
- Attribution : chaque λ_G négatif de DH = un quadruplet hors droite (0,8085 + 85,699i ; 0,6508 + 114,163i ; 0,5744 + 166,479i ; 0,7243 + 176,702i), zéros sur la droite positifs.
- Correction : les 4 zéros DH « manquants » (v3.3) étaient les partenaires 1 − σ ; 129 zéros jusqu'à t = 200.
- `1_Presentation/23_AUDIT_V6_3B_FORMULE_EXPLICITE.md`.

---

# V5.8 — 2026-10-05 — la leçon de 2026

- `1_Presentation/13_Lecon_2026` (Word + PDF, 2 p.) : mécanisme du résultat d'Alpöge–Furman (compression finie de la forme hermitienne de Weil, inégalité rang–trace, loi d'inertie de Sylvester), comparaison avec Q, prolongements déjà publiés (Dirichlet, intervalles courts, preuve de Lamzouri, formalisation), conclusion : plus de cible réaliste pour ce programme.
- Correction : la piste « extension aux fonctions L de Dirichlet » proposée en v5.7 était déjà traitée dans l'article d'Alpöge–Furman.
- Sources de 2026 lues sur résumés, pages et extraits seulement. Tests inchangés (47/47).

---

# V5.7 — 2026-10-05 — article court mis à jour

- `1_Presentation/02_Article_court_EN` (Word + PDF, 5 p.) : §6 « An exact link with Q (pole cancellation) » — identité exacte, plateau 1,28–1,31 κ/log N jusqu'à 10⁵, b_N → −1 − 2γ/log N (résidus sous RH, observé jusqu'à 10⁷), retour exact à Q ; référence [23] Maier–Rassias (arXiv:1806.05070, résumé lu) ; date du brouillon 2026-10-05.
- Aucun changement de code ; tests 47/47.

---

# V5.6 — 2026-10-05 — annulation du pôle : vérification, extension, retour à Q

- `scripts/run_pole_cancellation.py` ; données `pole_cancellation_check.csv`, `pole_cancellation_extension.csv`, `pole_cancellation_bN.csv`, `pole_cancellation_figure.png`.
- Document reçu vérifié (écart ≤ 5·10⁻⁸, limité par la troncature de la queue) (identité e² = β²Q(N) + T_N avec β = −S_N/A_N ; chiffres reproduits). Référence Maier–Rassias arXiv:1806.05070 vérifiée (résumé).
- Extension : e²·log N/κ = 1,29 → 1,31 jusqu'à N = 10⁵ ; b_N → −1 − 2γ/log N (calcul par résidus sous RH, confirmé jusqu'à 10⁷) ; part β²Q → 4/3 sous RH.
- Décision : branche Nyman–Beurling close (ramène exactement à Q). Banc d'audit : E21, D07. `1_Presentation/12_Annulation_du_pole`. Tests 47/47.

---

# V5.5 — 2026-10-05 — estimation sous RH testée

- `scripts/run_rh_heuristic_test.py`, `scripts/run_rh_heuristic_flatness.py` ; données `rh_heuristic_test.csv`, `rh_heuristic_flatness.csv`.
- Résultat : le terme principal sous RH, e² ≈ κ∫P′²/log N, ne décrit pas N ≤ 998 (R = 12,2 pour 1 − x ; 0,6 à 3 pour les poids plats en 0). Pour 1 − x : e² ≈ κ/log N + 3,6/log²N (coefficient stable de N = 100 à 998). Ordre des poids plats en 0 par |P″(0)|.
- Conséquence : estimer Γ₀₀, Γ₀₁, Γ₁₁ par le terme principal n'expliquerait pas le plateau ; il faut le terme en 1/log²N (forme quadratique en P′(0), P″(0), P′(1)).
- `1_Presentation/11_Estimation_sous_RH` (Word + PDF, 2 p.) ; test `test_rh_heuristic_v55` ; tests 46/46.

---

# V5.4 — 2026-10-05 — attaque 2 par itérations jusqu'à N = 998

- `scripts/run_attack_iter.py` : construction reprenable de la Gram sans carré (Y = 10⁵, écart ≤ 2·10⁻¹¹ vs 3·10⁵), analyse du plus grand bloc complet, journal et résultats réécrits à chaque itération et copiés vers les sorties.
- Données : `nb_gram_sqfree1000.npy` (complète jusqu'à 998), `attack_iter_results.csv`, `attack_iter_figure.png` ; journal `preuves/ATTAQUE_JOURNAL.md`, tableau `preuves/ATTAQUE_RESULTATS_COURANTS.md`.
- Résultats : {μ, a} entre 1,22 et 1,36 κ/log N (N = 50…998) ; polynôme de degré 5 ≈ 1,10–1,28 ; optimum sans carré 0,98–1,07 (passe sous 1 vers N = 700, contrôle de précision consigné) ; β·log²N → −1,1 à −1,2 ; part lisse du poids optimal 92 % → 71 %.
- `1_Presentation/10_Attaque2_resultats_N1000` (Word + PDF, 2 p.). Test `test_attack_iter_results` ; tests 45/45.

---

# V5.3 — 2026-10-05 — audit et amélioration de deux attaques reçues

- `1_Presentation/09_Attaques_audit_et_amelioration` (Word + PDF, 3 p.) : verdict sur l'« énergie transverse / dissipation » (reformulation : (★) ⇔ Q ≪ L³ ; contractivité automatique) et sur la projection de Nyman–Beurling (tableau reçu reproduit : 0,01956 ; 0,01443 ; 0,01363).
- Scripts `run_attack_nb_family.py`, `run_attack_controls.py`, `run_attack_audit.py` ; données `attack_*.csv` ; Gram sans carré 200 (`nb_gram_sqfree200.npy`). `nyman_beurling.py` : Y ≥ 25·lcm pour les grands indices (résultats inchangés pour N ≤ 100).
- Constats : le gain vient de la courbure en log n (13 familles témoins) ; plateau e_N² log N / κ ≈ 1,2–1,4 jusqu'à N = 200 ; β_N log² N ≈ −1,3 ; irrégularité de μ seul expliquée par ¼ M(N)² ; K(L) distingue ζ et Davenport–Heilbronn.
- Banc d'audit : E17–E20 (20 erreurs, 6 leurres). Tests 44/44.

---

# V5.1 — révision éditoriale de cohérence

- `1_Presentation/02_Article_court_EN.docx` remplacé par la version signée : Vincent P. P. NOËL (adresse électronique retirée de la copie publique) ; déclaration explicite de l’usage de ChatGPT (OpenAI) et Claude (Anthropic).
- Ajout de `1_Presentation/07_Guide_de_lecture_intuitif.docx`, lecture conceptuelle incluant la chaîne Mellin → Fourier → formule explicite → Selberg → opérateur et les réserves sur positivité, complétude, signe, densité et statistique.
- Coordonnées et déclaration IA harmonisées dans la synthèse, le dossier et le message au relecteur ; versions visibles mises à jour.
- `KNOWN_GAPS.md` retitré « état V5.1 ». Aucune modification des résultats mathématiques.
- Suite inchangée : 39/39 tests OK. Manifeste de checksums régénéré après les changements éditoriaux.

---

# V5.0 — 2026-10-05 — réorganisation présentable

- Nouvelle arborescence en 4 dossiers (présentation, méthode, preuves et calculs, archives) ; l'ancien INDEX est remplacé par le README.
- Nouveaux documents : synthèse (FR, 3 p.), cheminement intellectuel (FR, 3 p., frise et questionnaire d'origine), brief et message au relecteur (Word).
- Tests inchangés (39/39) ; chemins des tests adaptés à la nouvelle arborescence.

---

# V4.9 — 2026-10-04 — index, plan d'impact, banc d'audit

- `INDEX.md`, `docs/PLAN_IMPACT.md` : où ranger les quatre axes d'impact et comment suivre leur statut.
- `audit_bench/` : `planted_errors.json` (E01–E16, D01–D06), `PLANTED_ERRORS.md`, `score_auditor.py`, `example_findings.json`.
- `docs/CASE_STUDY_OUTLINE.md` (axe 3) ; `docs/COLLAB_BRIEF.md` (axe 4, anglais).
- Test `test_audit_bench_scorer` ; tests 39/39. Aucune modification mathématique.

---

# V4.8 — 2026-10-04 — protocole multi-agents et panorama physique

- `docs/Protocole_multi_agents_et_panorama_physique_RH.docx` : protocole (A1–A9, dont garde-fous cognitifs) et panorama physique (B0–B4).
- Constats : aucune circonstance physique ne confirme RH ; l'accord GUE s'écarte par corrections de taille finie (N_eff = log(E/2π)/√(12Λ), Λ = 1,57314, BBLM 2006) ; les expériences (ion piégé Yb⁺, RMN 5 qubits) reproduisent des zéros connus à paramètre réel ; seul encadrement exact : 0 ≤ Λ ≤ 0,22 (Rodgers–Tao ; Polymath15).
- Test `test_protocol_document_present` ; tests 38/38.

---

# V4.7 — 2026-10-04 — H3 et travaux récents

- `docs/H3_ANALYSIS.md` : (H3) → (H3⋆) ; noyau croisé K_η d'intégrale nulle (vérifié 10⁻¹⁴) ; non levée par Montgomery/BGST (échelle ≳ 2π/log T) ni par les proportions de zéros simples.
- Article : état de l'art mis à jour (Alpöge–Furman arXiv:2608.13637, Lamzouri arXiv:2609.02882, BGST Acta Arith. 2024, Montgomery 1973), (H3⋆), ligne « écarts » dans le tableau de vérifications.
- Test `test_h3_gap_statistics` ; tests 37/37. Sources récentes lues sur résumés/pages seulement.

---

# V4.6 — 2026-10-04 — article court

- `docs/Article_short_energy_functional.docx` (Word, anglais, 5 p.). Remarque Li : κ = 2λ₁, « useful positivity landmark, but no additional Li-type criterion is used here ».
- Test `test_kappa_is_twice_first_li_coefficient` ; tests 36/36.
- À faire avant soumission : relecture externe de A et B, vérification des références citées de mémoire (pages de [1],[3],[11],[14],[15],[18]), auteurs, déclaration d'assistance.

---

# V4.5 — 2026-10-04 — dossier de relecture externe

- `docs/Referee_dossier_Theorems_A_B.docx` (Word, anglais, 4 p.) : lemmes 1–5, Théorème A, Théorème B, grille de 9 points de contrôle.
- `docs/REVIEW_PLAN.md`, `docs/PRIORITY_CHECK.md` : antériorité du cas pôle simple (Cramér 1922 ; Brent–Platt–Trudgian 2022) ; Banks–Sinha comparés, non identiques (Λ_2 ↔ ζ″/ζ n'a pas de double pôle aux zéros simples).
- L6 : reliquat `a_1` supprimé ; `log Q` → `log(1+Q)` (README, KNOWN_GAPS, note de synthèse). Test de conventions ajouté ; tests 35/35.

---

# V4.4 — 2026-10-04 — audit des branches V4.1–V4.3

- `docs/AUDIT_V4_3.md` ; `scripts/run_generator_real_signal.py` ; `data/generator_real_signal.csv` (ESPRIT sur ψ et sur Λ_f de Davenport–Heilbronn).
- Constats : tests V4.3 circulaires ; Re λ biaisé (−0,002 à −0,09) sur zéros critiques ; mode fantôme à Im≈73,8, Re=+0,345 sur DH ; signal d'ordre 2 défectif ; M>0 ⇔ spectre réel.
- `spectral_metric` : paramètre `metric_cond_max` ; tests 34/34.

---

# V4.0 — 2026-10-04 — audit/referee

- Base mathématique conservée de la V3.9.
- Intégration des corrections utilisateur dans `docs/USER_CORRECTIONS_2026-10-04.md`.
- Ajout de la bibliographie consolidée `docs/SOURCES_RH_PROGRAMME.md`.
- Ajout de simulations de referee A/B/C et d'un protocole de relecture indépendante.
- Correction des métadonnées README/version ; cible de tests mise à 21/21.
- Aucun nouveau résultat RH n'est revendiqué dans cette version.

---

# Changelog conceptuel

## 2026-10-03 — v3.9 (note de synthèse en anglais)

1. `docs/SYNTHESIS_NOTE_EN.md` : synthèse (Lemmas 1–5, Theorems A et B, Proposition C, Nyman–Beurling, étalonnages, décision d'arrêt, statut, références avec niveau de vérification).
2. README mis à jour ; roadmap §18. Aucun code modifié ; tests 21/21.

## 2026-10-03 — v3.8 (plan optionnel : d_N² jusqu'à N=100, bibliographie)

1. `scripts/run_nb_gram_ext.py` (reprenable) : Gram 100×100 ; d_N² log N = 1,005–1,042 κ pour N=40…100, non monotone ; stabilité 10⁻¹⁰, cond ≤ 3,7·10⁴.
2. Bibliographie : L8 = Franel 1924 / Landau 1924 [VÉRIFIÉ] ; L7 = corollaire élémentaire, sans revendication de nouveauté.
3. Tests 21/21. Roadmap §17.

## 2026-10-03 — v3.7 (décision P2 : mémos P2.2 et P2.3)

1. `docs/MEMO_P2_2_WEIL.md` + `scripts/run_function_field_analog.py` : les trois ingrédients de la preuve sur F_q (rationalité, tour, Hodge) n'ont pas d'image dans Q ; Q est le carré de la formule explicite ; analogue exact : cubique si |α|=√p, exponentiel sinon (a=25) ; 10 100 courbes sur F_101, max|a|=20.
2. `docs/MEMO_P2_3_DENSITE.md` : trois routes ramenées aux grandes valeurs ; plancher de bruit Σc²/n = 6 691 ; SNR des raies ∝ 1/γ² (55 → 11,5 → 3,3).
3. **Règle d'arrêt P2 déclenchée** ; plan de repli P0/P1 (roadmap §16). Tests 20/20.

## 2026-10-03 — v3.6 (termes d'ordre inférieur : α, β)

1. `docs/ALPHA_BETA_ANALYSE.md` : coefficients η⁻³, η⁻², η⁻¹ de I(η) dérivés localement ; modèle à 300 zéros : 0,2327 vs s₁ = 0,2328.
2. **Correction** : le coefficient de L² est α+Φ(L), Φ presque périodique (±0,03, corr. 0,996) ; α, β sont des moyennes, pas des valeurs ponctuelles.
3. GAP-3 reformulé (U = (4κ/3)L³ + O(L²) sous hypothèse de paires proches) ; hypothèses (H1)–(H3) explicites.
4. `scripts/run_alpha_beta.py`, tests 19/19. Roadmap : activité 9 faite, §15.

## 2026-10-03 — v3.5 (matrice de Gram de Nyman–Beurling)

1. `src/nyman_beurling.py` : Gram exacte par cellules + queue M/Y + F̄/Y² (M = ¼ + gcd²/(12ab)) ; ⟨χ,ρ_a⟩ exact ; d_N² optimal en précision étendue.
2. Validations : G(1,1)=log 2π−γ (10⁻¹⁴) ; dictionnaire de Mellin vs intégrale critique (0,05 % et 0,6 %) ; stabilité de d_N² (cond 3·10³ à N=30).
3. Résultat : d_N² log N = 0,058→0,049 (N=5→30), 1,07 κ à N=20–30 ; E(V_N) log N = 0,71 à N=200 (≈15 κ).
4. Tests 18/18. Roadmap : activité 8 faite, §14.

## 2026-10-03 — v3.4 (théorème du terme dominant)

1. `docs/THEOREME_TERME_DOMINANT.md` : sous RH, Q(X) ∼ (S/3)(log X)³ (4κ/3 si zéros simples), sans hypothèse de simplicité ; preuve en 6 étapes modulo F1–F5.
2. `scripts/run_abelian_check.py` : η³Q_η mesuré 0,0279 à η=0,2 vs 0,0291 prédit (κ + αη/2 + βη²/2, 300 zéros).
3. Tests : constantes du théorème et décomposition en éléments simples de q' (16/16).
4. GAP-3 : terme dominant devenu théorème conditionnel ; L² et L restent ouverts. Roadmap : activité 3 faite, §13.

## 2026-10-03 — v3.3 (comparaison BCF, moment de Gonek, zéros de DH)

1. `docs/COMPARAISON_BCF.md` : dictionnaire exact avec Bettin–Conrey–Farmer (arXiv:1211.5191 lu en entier) ; identité du premier ordre testée (`test_bcf_first_order_identity`).
2. `scripts/run_gonek_moment.py` : S(T)=Σ1/|ζ'(ρ)|² vs (6/π³)T sur 300 zéros (ratio 0,976 à T≈542 ; exposant effectif 0,915 < 3/2).
3. Esquisse : les séries α, β de GAP-3 convergent sous les hypothèses de BCF ; hors diagonale toujours ouvert.
4. Zéros de DH complétés : 125 pour ≈129,5 attendus (t ≤ 200), aucun σ > 1 ; comptages corrigés dans la doc.
5. Roadmap : §11 mis à jour (activités 6 et 7 faites, 8 et 9 ajoutées), nouveau §12. Tests 14/14.

## 2026-10-03 — v3.2 (banc de rejet, localisation, bibliographie)

1. `src/rejection.py` + `scripts/run_rejection.py` : pipeline G→c→C→Q générique pour ζ, L(s,χ₅) et Davenport–Heilbronn (équation fonctionnelle de DH vérifiée à 10⁻¹⁶).
2. Résultat : pente de log Q/log X = 0,33 (ζ), 0,34 (L), 0,56 (DH) ; zéros de DH hors droite retrouvés (125/≈129,5 attendus, t ≤ 200).
3. `scripts/run_localisation.py` : 18 pics sur 20 de l'énergie de bande à < 0,5 d'un zéro de ζ.
4. `docs/BIBLIO_POSITIONNEMENT.md` : κ est la constante de Burnol/BCF ; lignes [VÉRIFIÉ]/[À VÉRIFIER].
5. GAP-3 corrigé (α, β non confirmables) ; plage d'utilité de Guth–Maynard précisée ; analyse P2.3.
6. Roadmap : nouvelle phase 10 et tableau d'activités (docs/ROADMAP_HISTORY.md §10–11). Tests 13/13.

## 2026-10-03 — v3.1 (roadmap history)

1. Ajout de `docs/ROADMAP_HISTORY.md`, carte chronologique unique du programme.
2. Pour chaque phase : idée testée, résultat réellement obtenu, verrou rencontré, décision actuelle.
3. Les pistes abandonnées ou rétrogradées sont distinguées des objets rigoureux conservés.
4. La règle d’arrêt et la trajectoire `Q(X,T) -> densité -> Q_chi(X,T)` sont visibles dans une seule carte.
5. Aucun changement mathématique ni numérique par rapport à v3 ; cette version est une consolidation éditoriale et méthodologique.


## 2026-10-03 — v3 (calibration spectrale et tests de rejet)

1. **GAP-2 fermé** : preuve du théorème
   `1/2 limsup log Q/log X = Theta - 1/2` dans L6, avec Perron tronqué aux demi-entiers.
2. Correction du palier classique : `Theta <= 1` est connu ; `Theta = 1` n'est pas connu.
3. Introduction de l'observable spectrale à deux paramètres `Q_{w,W}(L;T,Delta)` (L11) et
   du module `src/spectral_calibration.py`.
4. Davenport–Heilbronn devient un **test de rejet** explicite : une future preuve doit utiliser
   irréversiblement le produit d'Euler.
5. Benchmark principal remplacé par une question falsifiable : le cadre peut-il reproduire
   une densité de zéros connue ?
6. Référence de calibration ajoutée : Guth–Maynard, Annals of Mathematics 203 (2026),
   `N(sigma,T) <= T^{30(1-sigma)/13+o(1)}`.
7. `sympy.factorint` conservé comme dépendance explicite de test ; nettoyage du test de
   `H_inf` dans la forme courte `Phi_q=mu(q)h_q/zeta`.
8. Nettoyage du test de régularité en `s=1` via la valeur limite exacte
   `G(1)=2 gamma_E^2+6 gamma_1`.
9. Les pistes Kalman/Apollo, Fourier locale uniforme et extension numérique brute sont
   officiellement rétrogradées au rang de diagnostics.

## 2026-10-03 — v2 (priorisation et durcissement)

1. Plan priorisé P0–P4 (`docs/PRIORITES.md`) ; règle d'arrêt après étalonnage.
2. Lemmes L1–L10 avec preuves ; **H_∞ simplifiée** : H_∞(q)=2μ(q)h'(1), h=∏(p^s−1)^{-1}.
3. Équivalence cible ⇔ RH énoncée en tête (GAP-0).
4. Formule explicite avec termes d'ordre L², L ; 300 zéros ; Q mesurée jusqu'à 4·10⁶ ;
   accord à ~5 % (et corrélation 0,976 sur B(t)) : l'ancienne référence (4κ/3)L³ seule était trop grossière.
5. Tests indépendants (10/10). Mise en garde sur la baseline « diagonale » et sur `info_per_logX`.

## 2026-10-03 — version consolidée

1. **Nyman–Beurling / Báez-Duarte** retenu comme cadre fonctionnel de base.
2. Passage en variable logarithmique et interprétation par translations / opérateurs de Gram.
3. Introduction de mollificateurs Möbius apodisés; constat du compromis biais local / fuite spectrale.
4. Abandon de la fenêtre à plateau comme route directe: le résidu `M_N(1)` transporte le verrou RH au lieu de le supprimer.
5. Fenêtres compensées polynomiales; identification de la compensation `theta ≈ 1` et du rôle de la singularité en `s=1`.
6. Extraction d'une observable indépendante de `N`:
   \[
   c(n)=(\Lambda*\Lambda)(n)-\Lambda(n)\log n+2\gamma\Lambda(n).
   \]
7. Dirichlet génératrice:
   \[
   G(s)=\sum c(n)n^{-s}=q(s)^2+q'(s)+2\gamma q(s),\quad q=-\zeta'/\zeta.
   \]
8. Aux zéros de zêta, `G` possède un double pôle de coefficient principal universel `m(m+1)`.
9. Introduction de
   \[
   Q(X)=\int_1^X |C(x)|^2x^{-2}dx.
   \]
10. Factorisation Möbius:
    \[
    a(n)=\mu(n)((\log n)^2-2\gamma\log n),\qquad c=1*a.
    \]
11. Moment nul exact:
    \[
    \sum a(n)/n=0.
    \]
    Ceci explique une cancellation cohérente de rang un.
12. Réécriture en parties fractionnaires et décomposition hyperbolique; localisation du verrou dans la queue.
13. Analyse des phases réciproques et formulation d'une concentration Fourier locale de Möbius.
14. Introduction d'un schéma “GPS/Kalman”: innovations multiscales, covariances, complément de Schur, information cumulée.
15. Identification d'une covariance arithmétique exacte pour les dents de scie:
    \[
    \langle \psi_d,\psi_e\rangle = \gcd(d,e)^2/(12de).
    \]
16. Factorisation de cette covariance par les canaux de diviseurs via `J_2`.
17. Tests numériques: annulation très forte entre diagonale et hors-diagonale; information multiscale positive mais aucune loi `c log X` établie.
18. Cette version corrige les formulations antérieures trop optimistes: le filtre Kalman est traité comme outil de diagnostic/projection, pas comme preuve.

19. **Canaux terminaux (dernière évolution)**: dérivation de la formule fermée
    \[
    H_\infty(q)=-2\mu(q)\varphi(q)^{-1}\left(\log q+\sum_{p\mid q}\frac{\log p}{p-1}\right)
    \]
    pour `q` sans carré. Le “GPS analytique” possède désormais une destination exacte par canal; le problème restant est la variance de la queue vers cette destination.


## 2026-10-04 — V4.1 « source localization »

1. Ajout de `docs/SOURCE_LOCALIZATION.md` : RH vue comme problème inverse spectral, avec séparation claire diagnostic/preuve.
2. Ajout de `src/source_localization.py` : moyennage gaussien, Laplacien régularisé, analyse Morlet, matched filter/GLS, visibilité par SVD.
3. Ajout de `scripts/run_source_localization_demo.py` et `data/source_localization_demo.csv`.
4. Démonstrateur synthétique : localisation des modes `(0.5,14)` et `(0.60,21)` ; pente d'enveloppe estimée `0.0997` pour une cible `0.10`.
5. Ajout de trois tests ; suite complète `24/24`.
6. Positionnement littérature : harmonic inversion de zeta, Guinand–Weil, Connes / spectre d'absorption ; aucune nouveauté revendiquée.
7. Nouveau GAP-8 : absence de borne uniforme d'observabilité pour les sources hors ligne.


## V4.2 — 2026-10-04 — Schrödinger / flux

- Ajout de `docs/SCHRODINGER_FLUX.md`.
- Dictionnaire `rho=beta+i gamma` ↔ `E=-gamma+i(beta-1/2)` pour l'évolution en temps logarithmique.
- Ajout de l'équation de continuité et de la lecture source/sink d'un zéro hors ligne.
- Ajout de `src/schrodinger_flux.py`, du démonstrateur et de trois tests.
- Positionnement explicite par rapport à Wu–Sprung, Berry–Keating, Sierra–Rodríguez-Laguna et Connes.
- Nouveau `GAP-SCHR` : la difficulté est de dériver l'opérateur depuis l'arithmétique et de prouver son auto-adjointeté, non d'ajuster un spectre fini.


## V4.3 — 2026-10-04 — générateur arithmétique / quasi-Hermitien

- Ajout de `docs/ARITHMETIC_SCHRODINGER_GENERATOR.md`.
- Formalisation de la chaîne primes → signaux multicanaux → `A` → `H_eff=(i/dt)log A` → métrique positive `M`.
- Ajout de `src/arithmetic_generator.py`, `scripts/run_arithmetic_generator_demo.py` et `data/arithmetic_generator_demo.csv`.
- Diagnostic fini-dimensionnel `H^*M=MH` / `A^*MA=M` et certificat spectral pour matrices diagonalisables à spectre réel.
- Contrôle synthétique : deux modes RH-like donnent un certificat métrique ; un mode `beta=0.60` produit `Im E=0.10` et est rejeté par ce certificat.
- Nouveau `GAP-SCHR-GEN` : dérivation exacte et uniforme depuis l'arithmétique.
- Ajout de trois tests ; suite complète `30/30`.
- Positionnement littérature ajouté : DMD/Koopman et pseudo-Hermiticity/quasi-Hermiticity.
