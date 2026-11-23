# Livraison V6.59 — note de livraison

**17 octobre 2026 · Vincent NOËL.** Cette note dit ce qui a changé, pourquoi, et ce qui reste à décider. La procédure est dans [`CIBLAGE.md`](CIBLAGE.md) ; sa version de lecture est le [document 82](../../1_Presentation/82_CIBLAGE_ET_REPARTITION.pdf). L'entrée du corpus est le [README](../../README.md).

## 1. Demande

« Je veux que le ciblage soit défini pour pouvoir travailler de manière itérative indépendamment de l'IA. Choisir et pouvoir répartir le travail entre IA et agents. » Et, avant cela : « On veut adapter les méthodes et en avoir une seule au final. »

Décisions de l'auteur sur les deux points soumis :
- une IA ou un agent dépose dans une zone séparée, sans écrire dans le corpus ;
- l'auteur décide de l'acceptation.

## 2. Ce qui est livré

| Pièce | Rôle |
|---|---|
| `2_Methode/Pilotage/CIBLAGE.md`, `TARGETING_EN.md` | Référence de la méthode de travail, en français et en anglais |
| `1_Presentation/82_CIBLAGE_ET_REPARTITION` (md, pdf) et sa version anglaise | Document 82 : la procédure, avec l'état courant généré |
| `2_Methode/Pilotage/ciblage.py`, `ciblage_contrats.json` | Ciblage en lecture seule : demandes de calcul, choix Bellman, front des investigations, fiches proposées |
| `2_Methode/Pilotage/taches.py`, `taches.json`, `journal_taches.json` | Fiches de tâche : création, assignation, prévision, dépôt, vérification, décision, intégration ; journal chaîné |
| `2_Methode/Depot/` | Zone de dépôt, un dossier par fiche |
| `2_Methode/Pilotage/verify_ciblage.py` | 46 contrôles adverses du ciblage et des fiches |
| Navigateur | Bloc « Ciblage : que faire maintenant, et qui le fait » en tête ; résumé Bellman synchronisé avec les réglages ; lien depuis le portail |
| `GUIDE_POUR_UNE_IA.md`, `GUIDE_FOR_AN_AI.md` | Prompt mis à jour : une IA qui reçoit une fiche suit la fiche et la zone de dépôt ; l'état courant liste les fiches |
| `3_Preuves_et_calculs/tests/test_v659_ciblage.py` | Test : contrôles du ciblage et des fiches, cohérence des registres, document 82 à jour |

Sept fiches sont ouvertes, aucune n'est assignée :
- une étude Bellman à lier à une instance : auditer noyaux et couplages ;
- six investigations du front : paquets signés, dette de Schur duale, deux filtres, corrélations de μ, fibre à A fixé, noyau des moments à S = 0,8.

## 3. Une seule méthode : ce qui a été tranché

| Point | Corpus V6.58 | Branche ciblage (16 octobre) | Retenu |
|---|---|---|---|
| Chiffres et textes des vues | Calculés depuis les données | Écrits en dur (99 actions, « huit fiches », « V6.58 ») | Données |
| « À lire d'abord » | `points_d_attention.json` | Texte dans `build_pilotage.py` | `points_d_attention.json` |
| Empreintes | `reviewed_source_hashes` | Second registre dans `ciblage_contrats.json` | Registre unique ; le contrat ne déclare que des chemins. Les neuf empreintes observées par la branche ont été retrouvées identiques et versées au registre. |
| Prérequis | Statut de l'investigation | Issue positive attestée avec sa portée | Attestation (branche) |
| Recommandations | — | Lecture seule, fractions exactes | Repris tels quels |
| Front des investigations | — | Liste fixe de quatre investigations | Toutes les investigations ouvertes du pilotage |
| Rôles et garde-fous | Protocole multi-agents du 5 octobre, non relié | — | Appliqués aux fiches (rôles, anti-circularité, relecture à l'aveugle, règle d'arrêt) |
| Langues | Français et anglais | Français | Français et anglais |
| Lien de téléchargement externe | — | Présent dans la page de continuité | Retiré |

Les autres différences du dossier reçu étaient des versions antérieures à V6.58 de fichiers du corpus : `pilotage_recherche.json` sans les ajouts V6.58, `verify_pilotage.py` avec ses comptes figés, la marque BOM retirée de deux pages. Elles ne sont pas reprises.

## 4. Pièces reçues

Les six pièces reçues le 17 octobre sont archivées telles quelles dans `4_Archives/recus/2026-10-17/`, avec leurs empreintes et une table d'intégration.

- **Notice « 76_CIBLAGE_AUTOMATIQUE ».** Remplacée par le document 82, le numéro 76 étant déjà pris.
- **Complément 79.** Texte identique à celui du corpus.
- **Critique « tomographie de phase ».** Déjà traitée pour l'essentiel (docs 15 à 24). Deux éléments nouveaux peuvent devenir des fiches, avec l'accord de l'auteur :
  - le Gram de Nyman–Beurling sur des différences d'échelle ;
  - la décomposition de K.
- **Critique des quatre pistes.** Déjà couverte par l'atlas du document 14 et ses suites.
- **Brouillon de working paper.** Non intégré ; trois corrections sont à faire avant un dépôt.

## 5. Ce qui n'a pas changé

- Aucun fait mathématique, niveau d'indicateur, statut d'idée ou coût Bellman.
- Aucun original : `4_Archives` reçoit seulement des fichiers ajoutés.
- Aucun numéro de document réattribué.

Le script `integrate_v658.py` est inchangé dans ses effets : ses listes « Ce qui change » et sa commande de reproduction sont devenues des variables, et son README est reproduit à l'octet près.

## 6. Décisions qui restent à l'auteur

1. **Répartir les sept fiches** (`taches.py assigner`) entre toi, des IA et des agents.
2. **Ouvrir deux fiches**, si tu le souhaites, pour les éléments nouveaux de la critique « tomographie de phase ».
3. **Quoi pré-publier** : proposition inchangée (note V6.58, § 3 quater).

## 7. Vérifications

- `verify_ciblage.py` : 46 contrôles.
- `taches.py controler` : aucune erreur.
- `verify_contracts.py` et `verify_pilotage.py`.
- Suite de tests complète.
- `sha256sum -c CHECKSUMS.sha256`.

## 8. Complément du 17 octobre au soir

À la demande de l'auteur : « Ouvrir les deux nouvelles fiches. Répartir les tâches en ce que tu préfères d'abord et donner à ChatGPT une autre partie. Couper en trois ou quatre parties cohérentes pour pouvoir les importer sur GitHub et travailler dessus. »

- **Deux fiches ouvertes** à partir de la critique « tomographie de phase ». Leur sortie attendue et leur critère de rejet sont écrits à la création.
  - TAC-008 décompose la cohérence K en trois parts : diagonale, même premier, premiers distincts.
  - TAC-009 construit le Gram de Nyman–Beurling sur des différences d'échelle.
- **Répartition**, enregistrée par le coordinateur (`ia:claude`), qui l'a choisie.
  - **ia:claude** prend les fiches qui prolongent ses calculs : TAC-007 (noyau des moments à 0,8, méthode du document 81), TAC-008 (prolonge PRIME-LOCK) et TAC-001 (lier une instance à l'étude Bellman).
  - **ChatGPT** (`ia:chatgpt-sol-6.1-max`) prend TAC-009, TAC-003 et TAC-002. Sa consigne est `lots/LOT_01_CHATGPT.md` : prévisions d'abord, enregistrées par l'auteur, puis le travail.
  - TAC-004 à TAC-006 restent à attribuer.
- **GitHub** : voir [`GITHUB.md`](../../GITHUB.md).
  - Un dépôt privé unique, importé en cinq parties : entrée et méthode ; présentation, documents 01 à 58 ; présentation, documents 59 à 82 ; preuves et calculs ; archives.
  - Les commandes `taches.py` ne s'exécutent que sur `main`.
  - Les branches `tac-xxx` sont limitées à la zone de dépôt.
  - Les contrôles automatiques sont dans `.github/workflows/verifier.yml`.
  - Modèle de pull request fourni.
- **`.gitignore` corrigé.** Il excluait les journaux `*.log` du corpus (30 fichiers de `3_Preuves_et_calculs/data/` et des archives), qui font partie des pièces ; ils sont maintenant suivis.
- **Import en cinq parties** (demande de 19 h 58 : « Split part 2 in 2 parts »). La présentation est coupée selon le plan du corpus : documents 01 à 58 (fondations) et documents 59 à 82 (front de la positivité de Weil, avec les dictionnaires et les versions anglaises).
- **Horodatage des versions** (demande de 22 h : « Fais-le »). Chaque version livrée est figée (`2_Methode/Horodatage/CHECKSUMS_<version>.sha256`, empreintes de tout le corpus) et inscrite au registre. GitHub envoie ensuite son empreinte à OpenTimestamps et dépose la preuve `.ots`, complétée chaque jour jusqu'à l'ancrage Bitcoin. Seule l'empreinte sort du dépôt privé. L'e-Soleau (INPI) reste un geste de l'auteur aux moments importants. V6.59 est la première version horodatée.
