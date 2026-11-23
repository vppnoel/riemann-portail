# Programme Riemann — V6.59

*17 octobre 2026. Un programme de recherche personnel sur l’hypothèse de Riemann (RH), conservé comme un corpus versionné : documents, preuves, code, données et tests. Auteur : Vincent P. P. NOËL (Strasbourg). Travail mené avec l’aide de ChatGPT (OpenAI) et de Claude (Anthropic) ; l’auteur assume la responsabilité finale du contenu.*

*English: [README_EN.md](README_EN.md).*

> **Première visite ? Commencez par [INTRODUCTION.md](INTRODUCTION.md)** (en anglais) : ce qu’est ce projet, comment il a été mené avec des IA, le degré de solidité de chaque résultat, et comment contribuer.

## À lire d’abord

> **23 novembre 2026.** Trois notes lisibles par un humain sur la preuve Lean annoncée, vérifiées par une seconde IA et acceptées par l'auteur : de la borne (⋆) à GRH (en anglais), le Landau par fenêtres pour ζ, et son analogue pour les pôles doubles de l'article 1. Voir [lean_reading/](lean_reading/README.md). La note sur la preuve annoncée est corrigée sur deux points (voir sa fin).
>
> **22 novembre 2026.** Une preuve de l’hypothèse de Riemann (généralisée) a été annoncée le 20 novembre 2026 par L. Alpöge avec Claude, sous forme d’une formalisation Lean vérifiée depuis de manière indépendante. Le paragraphe ci-dessous décrit l’état au 17 octobre 2026. Ce que cela change (le théorème B devient inconditionnel ; la simplicité des zéros reste ouverte) : [NOTE_ALPOGE_2026.md](NOTE_ALPOGE_2026.md) (en anglais).

**RH reste ouverte. Le corpus ne contient pas de preuve de RH. Il contient des énoncés démontrés dans des cadres délimités, des certificats sur des fenêtres bornées, des mesures avec prévisions écrites avant, et la liste précise de ce qui manque.**

**1. Le noyau analytique : Théorèmes A et B, trois articles à faire relire** — *Démontré, relu en interne · non relu par un spécialiste*

Théorème A : l'exposant de croissance de l'énergie Q(X), intégrale de |C(x)|² x⁻² entre 1 et X, construite avec c = Λ∗Λ − Λ·log + 2γΛ, vaut 2(Θ − ½). Théorème B : sous RH, Q(X) ∼ (S/3)(log X)³ ; la constante vaut 4κ/3 si et seulement si tous les zéros sont simples, d'où un critère conjoint RH–simplicité. Article 1 porte ces énoncés ; article 2 un certificat dans une fenêtre fixée ; article 3 est une note expositive (jets de Hasse), sans nouveauté historique revendiquée. La relecture externe est la marche suivante de l'indicateur (niveau 7).

→ [Article 1](1_Presentation/articles/article1_mean_square_double_poles.pdf) · [Article 2](1_Presentation/articles/article2_prime_side_weil_forms.pdf) · [Article 3](1_Presentation/articles/article3_hasse_jets_and_spectral_bound.pdf) · [Dossier pour un spécialiste](1_Presentation/relecture/00_READ_ME_FIRST_EN.md) · [Pré-relecture (doc. 37)](1_Presentation/37_PRE_RELECTURE_A_B_ARCHIPEL.md)

**2. Ce qui manque n'est pas un comptage, c'est un carré** — *Démontré (élémentaire) · classique cité*

Dans le Modèle réduit (courbes sur 𝔽_q), 119 faux jumeaux qui violent RH ont des comptages positifs et des degrés d'isogénie positifs. Seule la trace d'un carré, la positivité de Rosati qui vient d'une polarisation, les exclut. ζ passe déjà les deux premiers niveaux (Λ ≥ 0, aucun zéro réel). Il lui manque l'objet qui fournirait ce carré.

→ [Document 80](1_Presentation/80_D_OU_VIENT_LE_SIGNE.pdf) · [Modèle réduit (doc. 28)](1_Presentation/28_MODELE_REDUIT_NECESSITE_DEMONTREE.pdf) · [Surface virtuelle (doc. 46)](1_Presentation/46_LA_SURFACE_VIRTUELLE.md)

**3. Positivité de Weil certifiée sur tous les tests, mais dans des fenêtres** — *Certifié dans son domaine · mesuré au-delà*

Sur l'espace infini des tests à moments nuls, sans zéros ni RH : Q_W ≥ ‖f‖²/25 pour S ≤ 0,347 (doc. 71), ≥ ‖f‖²/250 pour S ≤ 1/2 (doc. 73), ≥ 3‖f‖²/10000 pour S ≤ 11/20 (doc. 75). Le doc. 81 retrouve indépendamment les valeurs de Zhu jusqu'à L = 0,8 (non certifié) et mesure, sur le même sous-espace, une marge d'environ 5·10⁻¹² à 0,8. Attention : le minorant certifié de Zhu (λ*(0,8) > 0 pour toutes les fonctions) couvre déjà ces fenêtres en portée ; les certificats du corpus apportent des marges plus fortes sur les tests à moments nuls, pas une fenêtre plus large. La marge s'effondre à chaque élargissement ; aucune approche fenêtre par fenêtre ne démontrera RH.

→ [Document 73](1_Presentation/73_OPERATEUR_COMMUN_TETE_SOURCES_ET_QUEUE.pdf) · [Document 75](1_Presentation/75_RECUPERATION_TRANSPORT_ET_RH.pdf) · [Document 81](1_Presentation/81_ZHU_REPRODUIT.pdf)

**4. L'Archipel d'Euler : RH n'existe qu'aux points d'Euler** — *Démontré dans les espaces déclarés · pré-relu en interne*

Parmi les combinaisons de fonctions L qui partagent l'équation fonctionnelle, RH ne tient qu'aux points où la fonction a un produit d'Euler (espaces V_q de degré 1 déclarés). Le résultat situe la nécessité ; il ne donne pas « produit d'Euler ⇒ RH ».

→ [Document 30](1_Presentation/30_ARCHIPEL_D_EULER.pdf) · [Lemme des jets (doc. 58)](1_Presentation/58_VALIDATION_DIRECTE_DU_RELIEF_ET_LEMME_DES_JETS.md)

**5. Côté arithmétique : la tête est acquise, la grande queue est ouverte** — *Démontré sous ses gardes · ouvert*

La somme de Möbius est restituée exactement et la tête des conducteurs q ≤ H est bornée à toutes les échelles. La dette signée des grands conducteurs reste à contrôler ; la conséquence vers Re(s) > 3/4 est conditionnelle à cette borne.

→ [Essai d'amplification V6.55](1_Presentation/ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.pdf) · [Corrélations, identité et énergie](1_Presentation/CORRELATIONS_IDENTITE_ET_ENERGIE.pdf)

**6. Ce qui reste ouvert, précisément** — *Ouvert*

Trois obligations : la loi de signe sur une famille de tests (IDE-051), la couverture et le passage à la limite (IDE-050), la positivité de Weil sur tous les tests (IDE-052). La piste opératoire Q = ‖Tf‖² tirée de Suzuki est suspendue pour une incohérence de parité dans la convention publiée ; l'opérateur unilatéral T₊ est retenu à la place.

→ [Document 76](1_Presentation/76_RECONSTRUIRE_LA_PISTE_GLOBALE_DE_WEIL.pdf) · [Complément 76 (§8, parité)](1_Presentation/76_COMPLEMENT_COUP_DOUBLE.pdf) · [Document 79](1_Presentation/79_COMPENSATION_PROFILS_ET_OBSTRUCTIONS.pdf) · [Complément 79](1_Presentation/79_SIGNAL_COUPLAGES_ET_RESOLUTION.pdf)

**Précautions de lecture**

- Les niveaux de l'indicateur sont des catégories de maturité : ni un pourcentage de RH, ni une probabilité de preuve.
- « Mesuré » veut dire calculé en haute précision, pas certifié. Seuls les énoncés marqués « certifié » ou « démontré » le sont, et dans leur domaine.
- Deux numéros portent deux pièces : 76 (document et complément) et 79 (document et complément). Les numéros ne sont jamais réattribués.
- Chaque document décrit l'état de sa date. La synthèse (doc. 01) et le guide de lecture (doc. 07) sont à jour en V6.58, en français et en anglais ; les versions V6.24 sont conservées dans 4_Archives/historique.
- Les documents reçus (4_Archives/recus) et les originaux archivés ne sont pas modifiés ; les pièces reconstruites sont marquées comme telles.

## Ce qui change en V6.59

- **Ciblage et répartition du travail.** [Document 82](1_Presentation/82_CIBLAGE_ET_REPARTITION.pdf) et sa référence [`CIBLAGE.md`](2_Methode/Pilotage/CIBLAGE.md). Le ciblage lit l’état sans rien modifier et propose des fiches de tâche. Chaque fiche se confie à l’auteur, à une IA ou à un agent : prévision enregistrée avant, travail dans une zone de dépôt, vérification par un autre acteur, décision de l’auteur, journal chaîné. Sept fiches sont ouvertes, non assignées.
- **Une seule méthode.** La couche « ciblage automatique » de la branche du 16 octobre, le protocole du pilotage et le protocole multi-agents du 5 octobre sont réunis : registre d’empreintes unique, prérequis satisfaits seulement par une issue positive attestée avec sa portée, chiffres des vues calculés depuis les données. La notice reçue sous le numéro 76 devient le document 82 (le numéro 76 était pris).
- **Outils.** `2_Methode/Pilotage/ciblage.py`, `taches.py`, `verify_ciblage.py` (46 contrôles adverses) ; zone de dépôt `2_Methode/Depot/` ; bloc « Ciblage » en tête du navigateur ; [guide pour une IA](GUIDE_POUR_UNE_IA.md) mis à jour.
- **Neuf fiches, réparties.** Deux fiches ajoutées pour la critique « tomographie de phase » (TAC-008 : décomposer la cohérence K ; TAC-009 : Gram de Nyman–Beurling sur des différences d’échelle). Trois fiches à ia:claude (TAC-001, 007, 008), trois à ChatGPT (TAC-002, 003, 009, consigne `2_Methode/Pilotage/lots/LOT_01_CHATGPT.md`), trois non assignées.
- **GitHub.** [`GITHUB.md`](GITHUB.md) : un dépôt privé unique, importé en cinq parties cohérentes ; branches `tac-xxx` limitées à la zone de dépôt ; contrôles automatiques (`.github/workflows/verifier.yml`).
- **Aucun résultat mathématique nouveau** ; niveaux de l’indicateur inchangés. Détail : [note de livraison](2_Methode/Pilotage/LIVRAISON_V659.md). Les changements de V6.58 (documents 80 et 81, entrée réorganisée) sont décrits dans l’[historique des livraisons](HISTORIQUE_DES_LIVRAISONS.md).

## Où aller

- [Portail](00_PORTAIL.html)
- [Guide de lecture intuitif (doc. 07)](1_Presentation/07_GUIDE_DE_LECTURE_INTUITIF.pdf)
- [Synthèse (doc. 01)](1_Presentation/01_SYNTHESE_FR.pdf)
- [Entrée en anglais (README_EN)](README_EN.md)
- [Indicateur d'avancement](1_Presentation/31_INDICATEUR_D_AVANCEMENT.html)
- [Navigateur et Bellman](1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html)
- [Ciblage et répartition du travail (doc. 82)](1_Presentation/82_CIBLAGE_ET_REPARTITION.pdf)
- [Travailler sur GitHub](GITHUB.md)
- [Graphe des idées](00_Carte_des_idees.html)
- [Matrice des théories](1_Presentation/44_MATRICE_DES_THEORIES.html)
- [Registre des sources](1_Presentation/42_REGISTRE_DES_SOURCES.html)
- [Liste des figures](00_Liste_des_figures.html)
- [Table logique](TABLE_LOGIQUE.md)
- [Références hiérarchisées](REFERENCES_HIERARCHISEES.md)
- [Guide pour une IA (prompt)](GUIDE_POUR_UNE_IA.md)
- [Plan du corpus](PLAN_DU_CORPUS.md)

## Organisation

| Dossier | Contenu |
|---|---|
| `1_Presentation/` | les documents numérotés (texte, PDF, pages), les articles, le dossier de relecture |
| `2_Methode/` | pilotage (indicateur, navigateur, graphe, Bellman), sources, figures, matrice, outils de construction |
| `3_Preuves_et_calculs/` | preuves, programmes, données, prévisions, tests (`python tests/run_all_tests.py`) |
| `4_Archives/` | originaux reçus et archivés, états antérieurs ; jamais modifiés |
| `4_Exports/` | compléments ZIP livrés séparément |
| racine | portail, graphe des idées, liste des figures, inventaires de récupération et d’intégrité, licences |

## Reproduire et vérifier

Python 3.12 ou plus récent, avec `numpy`, `scipy`, `pandas`, `matplotlib`, `mpmath`, `sympy` et `python-docx` (voir `requirements.txt`).

```bash
pip install -r requirements.txt
cd 3_Preuves_et_calculs && python tests/run_all_tests.py && cd ..
python -B 2_Methode/Outils/integrate_v659.py
python -B 2_Methode/Outils/integrate_v655.py --rebuild
python -B 2_Methode/Pilotage/verify_contracts.py
python -B 2_Methode/Pilotage/verify_pilotage.py
sha256sum -c CHECKSUMS.sha256
```

Les fichiers `.md` du corpus portent la marque UTF-8 (BOM), sauf les originaux reçus ou archivés, conservés à l’octet près. La méthode de recherche reste celle du protocole convenu ; toute modification de méthode exige une proposition et l’accord préalable de l’auteur.

## Licences

- **Code** (`*.py`, `*.js`, scripts de construction) : licence MIT, voir `LICENSE`.
- **Textes, figures et données** : Creative Commons Attribution 4.0 International (CC BY 4.0), voir `LICENSE-CC-BY-4.0.md`.
- © 2026 Vincent P. P. NOËL. Pour citer ce travail, voir `CITATION.cff`.

## English summary

A personal research programme on the Riemann Hypothesis, kept as a versioned corpus (mostly in French). **No proof of RH is claimed.** The main proved statements are written up in English in `1_Presentation/articles/`: (A) the growth exponent of a mean square Q(X) built from c = Λ∗Λ − Λ·log + 2γΛ equals 2(Θ − ½); (B) under RH, Q(X) ∼ (S/3)(log X)³, and the constant equals 4κ/3 if and only if all zeros are simple. Weil positivity is certified on all admissible test functions for supports up to 11/20 (documents 71–75). In the function-field model, the sign comes neither from point counts nor from isogeny degrees but from a square (Rosati positivity); ζ already satisfies the first two levels (document 80). None of this has been refereed yet. Code: MIT. Texts, figures and data: CC BY 4.0.
