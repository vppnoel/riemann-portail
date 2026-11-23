# Travailler sur GitHub — Programme Riemann

*V6.59 · 17 octobre 2026 · Vincent NOËL. Ce texte applique à GitHub la procédure de [`CIBLAGE.md`](2_Methode/Pilotage/CIBLAGE.md). Il ne la modifie pas.*

**Où en est le travail ?** La page [`2_Methode/Echanges/ETAT.md`](2_Methode/Echanges/ETAT.md) le dit, fiche par fiche : statut, vérifications, qui doit agir et quoi. Elle est régénérée automatiquement après chaque changement du registre.

## 1. Un seul dépôt, privé

**Un seul dépôt `programme-riemann`.** Les documents, programmes, tests et vues se citent par des chemins relatifs à la racine. Quatre dépôts séparés casseraient les tests, les reconstructions et les empreintes. Le découpage en cinq parties sert donc à l'**import**, pas à l'organisation du dépôt.

**Dépôt privé recommandé.**
- Deux fichiers Word du dossier de relecture et un journal historique contiennent l'adresse électronique de l'auteur.
- `4_Archives/recus/` contient des pièces reçues, non publiées.

Une copie publique demanderait de retirer ces éléments d'abord, comme pour la copie publique de V6.33.

## 2. Importer en cinq parties

| Ordre | Archive | Contenu | Taille décompressée |
|---|---|---|---|
| 1 | `partie1_entree_et_methode.zip` | Racine (README, plan, tables, guides, portail, inventaires), `2_Methode/`, `4_Exports/`, `.github/`, `.gitignore` | ≈ 16 Mo |
| 2a | `partie2a_presentation_fondations_01_58.zip` | `1_Presentation/` : documents 01 à 58 (énergie Q, instruments, familles et Modèle réduit, opérateurs, surface virtuelle), articles, dossier de relecture, pages hors numérotation | ≈ 23 Mo |
| 2b | `partie2b_presentation_front_weil_59_82.zip` | `1_Presentation/` : documents 59 à 82 (positivité de Weil : certificats, ponts, obligations ; ciblage), dictionnaires V6.46–V6.49, versions anglaises | ≈ 25 Mo |
| 3 | `partie3_preuves_et_calculs.zip` | `3_Preuves_et_calculs/` : preuves, programmes, données, prévisions, tests | ≈ 57 Mo |
| 4 | `partie4_archives.zip` | `4_Archives/` : originaux et états antérieurs, jamais modifiés | ≈ 50 Mo |

Chaque archive se décompresse **à la racine** du dépôt cloné. Ses chemins commencent directement par les dossiers du corpus.

L'import par le navigateur (« Add file → Upload files ») ne convient pas : il est limité à 100 fichiers par envoi, et le corpus en compte près de 1 900. Il faut passer par GitHub Desktop ou par `git`. Aucun fichier ne dépasse 20 Mo : Git LFS n'est pas nécessaire.

```sh
# 1. Sur github.com : créer le dépôt privé « programme-riemann », vide (sans README ni licence).
git clone https://github.com/<compte>/programme-riemann.git
cd programme-riemann
# 2. Une partie, un commit, dans l'ordre.
unzip ../partie1_entree_et_methode.zip      && git add -A && git commit -m "V6.59 — partie 1 : entrée et méthode"
unzip ../partie2a_presentation_fondations_01_58.zip && git add -A && git commit -m "V6.59 — partie 2a : présentation, documents 01 à 58"
unzip ../partie2b_presentation_front_weil_59_82.zip && git add -A && git commit -m "V6.59 — partie 2b : présentation, documents 59 à 82"
unzip ../partie3_preuves_et_calculs.zip     && git add -A && git commit -m "V6.59 — partie 3 : preuves et calculs"
unzip ../partie4_archives.zip               && git add -A && git commit -m "V6.59 — partie 4 : archives"
# 3. Vérifier l'intégrité complète, puis publier.
sha256sum -c CHECKSUMS.sha256 --quiet && git push -u origin main
git tag v6.59 && git push origin v6.59
```

Pour vérifier une partie seule : `sha256sum -c CHECKSUMS.sha256 --ignore-missing --quiet`.

Avec GitHub Desktop, la marche est la même :
1. cloner le dépôt vide ;
2. décompresser la partie 1 dans le dossier du dépôt ;
3. valider (« Commit to main ») ;
4. recommencer pour les parties 2a, 2b, 3 et 4 ;
5. publier (« Push origin »).

## 3. Travailler ensuite

La branche `main` porte l'état publié. **Les commandes `taches.py` ne s'exécutent que sur `main`**, par le coordinateur ou par l'auteur. Le registre des fiches et son journal chaîné restent ainsi linéaires, sans conflit de fusion entre branches.

| Étape (CIBLAGE.md) | Sur GitHub |
|---|---|
| Ouvrir, répartir | Sur `main` : `taches.py ouvrir` ou `creer`, puis `assigner`, puis commit |
| Prévoir | Sur `main`, avant tout travail : `taches.py prevoir TAC-xxx --par ACTEUR --texte "…"`, puis commit. L'heure du commit double celle du journal. |
| Discuter | Fil `TAC-xxx — discussion` (issue GitHub), à toute étape : voir § 4.3 |
| Produire | Branche `tac-xxx` (par exemple `tac-007`), qui ne contient que `2_Methode/Depot/TAC-xxx/`. Le contrôle automatique refuse tout autre fichier. |
| Déposer | Pull request de la branche, avec le modèle fourni. Après fusion sur `main` : `taches.py deposer`, puis commit. |
| Retirer | Avant toute vérification, le producteur peut retirer son dépôt pour le compléter : `taches.py retirer TAC-xxx --par … --motif "…"` sur `main`, en citant le fil. Puis branche `tac-xxx`, pull request, nouveau dépôt. |
| Vérifier | Un **autre** acteur relit la pull request ou le dossier fusionné. Il ajoute `TAC-xxx/verification/VERIFICATION.md` (branche `tac-xxx-verif`), puis lance `taches.py verifier` sur `main`. |
| Décider | L'auteur seul : `taches.py decider` sur `main`, ou, depuis un téléphone, le formulaire « decision-auteur » (onglet Actions, bouton « Run workflow ») ; aucune IA ne le lance. **Fusionner une pull request n'est pas accepter un résultat** : la fusion fait seulement entrer le dépôt. |
| Intégrer | Après acceptation : documents, pilotage et indicateur selon le protocole, par un script d'intégration ; reconstruction, tests, sommes de contrôle, **horodatage de la version** (`2_Methode/Horodatage/horodater_version.py`, voir son README), puis une étiquette de version (`v6.60`…). |

**Contrôles automatiques** (`.github/workflows/verifier.yml`), à chaque push et pull request :
- périmètre des branches `tac-xxx` ;
- `taches.py controler` ;
- `verify_ciblage.py` et le contrôle de l'interface ;
- `verify_contracts.py` et `verify_pilotage.py` ;
- la suite de tests.

Les sommes de contrôle ne sont recalculées qu'à la livraison d'une version (sans les preuves `.ots`, qui évoluent).

**Horodatage** (`.github/workflows/horodater.yml`) : à chaque nouvelle version figée dans `2_Methode/Horodatage/`, GitHub envoie son empreinte aux calendriers OpenTimestamps et dépose la preuve `.ots` ; chaque jour il complète les preuves en attente. Le contenu reste privé.

**Boîtes aux lettres.** `2_Methode/Echanges/<acteur>/A_FAIRE.md` dit à chaque IA ou agent ce qu'il doit produire et vérifier, avec la consigne de chaque fiche. Le flux `.github/workflows/boites.yml` les régénère après chaque changement du registre des fiches.

**Un acteur sans accès au dépôt** (une IA dans une autre application, par exemple) reçoit l'archive et une consigne de lot (`2_Methode/Pilotage/lots/`) :
1. il rend d'abord ses prévisions ;
2. l'auteur les enregistre ;
3. l'acteur rend ensuite ses dossiers `TAC-xxx/`, que l'auteur dépose sur une branche `tac-xxx`.

## 4. Règles de travail communes

*Écrites le 18 octobre 2026 à la demande de l'auteur. Elles valent pour toutes les IA, tous les agents et l'auteur.*

### 4.1 Ce qui va directement sur `main`, et ce qui passe par une pull request

| Changement | Chemin | Qui fusionne |
|---|---|---|
| Commandes de fiches : `taches.py creer`, `ouvrir`, `assigner`, `prevoir`, `deposer`, `retirer`, `verifier`, `decider`, `integrer`, `abandonner`, `boites` | Directement sur `main`, un commit par commande, rien d'autre dans le commit | — |
| Travail sur une fiche (`2_Methode/Depot/TAC-xxx/`) | Branche `tac-xxx`, pull request | Le producteur, une fois les contrôles automatiques passés |
| Vérification d'un dépôt (`TAC-xxx/verification/`) | Branche `tac-xxx-verif`, pull request | Le vérificateur, une fois les contrôles passés |
| Outillage sans effet sur la méthode : vues régénérées, mise en page, correction d'un lien | Branche, pull request | L'acteur, une fois les contrôles passés |
| **Méthode** : workflows (`.github/workflows/`, § 4.6), tests et leurs tolérances, contrôles automatiques et versions imposées, règles (`CIBLAGE.md`, ce texte), scripts de vérification ou d'intégration, registres scientifiques, indicateur | Branche, pull request marquée « méthode » | **L'auteur seul**, après avoir écrit son accord dans la pull request |
| Ajout d'une source au registre (`2_Methode/Sources/sources.json`) : nouvelles fiches complètes seulement, sans toucher aux fiches existantes (§ 4.7) | Dans la pull request de l'article ou de la fiche qui la cite, registre et vues reconstruits | L'acteur, une fois les contrôles passés, dont `garde-sources` |
| Dialogue autonome Claude ↔ ChatGPT (workflow `dialogue-ia`, sorties dans `2_Methode/Dialogue_Lean/travail/`) | Branche `ia-dialogue` uniquement, jamais fusionnée telle quelle | **Personne** : on en extrait des éléments par une fiche (§ 4.5) |

En cas de doute, un changement est traité comme un changement de méthode.

### 4.2 Identité

- Chaque acteur signe ses commits sous son propre nom (`Claude`, `ChatGPT`…) et ses opérations de fiche sous son identifiant (`ia:claude`, `ia:chatgpt-sol-6.1-max`).
- Si un outil ne peut écrire que sous le compte GitHub de l'auteur, le message du commit commence par l'identifiant de l'acteur réel, par exemple `[ia:chatgpt-sol-6.1-max] Vérification TAC-007`.
- Aucun acteur n'écrit `--par auteur:vincent-noel` : seul l'auteur le fait.
- Pas de workflow temporaire pour écrire à la place d'un acteur : on passe par une branche et une pull request.

### 4.3 Discuter des itérations

Chaque fiche a **un fil de discussion**, une *issue* GitHub intitulée `TAC-xxx — discussion`. C'est là que l'auteur et les acteurs discutent :
- de ce qu'il faut refaire quand une fiche est `a_reprendre` ;
- d'une nouvelle prévision, d'un changement de question ou de critère de rejet ;
- d'une fiche suivante proposée par un rapport.

Le fil se lit et s'écrit depuis l'application GitHub sur téléphone. Lien de recherche, valable pour toute fiche : `https://github.com/Vppnoel/riemann/issues?q=TAC-xxx` (remplacer `xxx`). Chaque boîte aux lettres donne le lien de ses fiches.

Trois règles :
1. **Avant de reprendre une fiche, l'acteur lit son fil en entier.** Une IA qui ne peut pas lire les issues demande à l'auteur de coller le fil.
2. **Une discussion ne décide rien.** Ce qui est convenu est inscrit au registre par une commande de fiche (nouvelle prévision, décision de l'auteur avec son motif), et le commit cite le commentaire.
3. **Le producteur répond dans le fil** à chaque point soulevé par la vérification ou par l'auteur, en disant ce qu'il fait ou pourquoi il ne le fait pas.

Une question qui ne porte sur aucune fiche (règle, outillage, choix de la suite) a son propre fil, sans numéro de fiche.

### 4.4 Ce qui n'est pas imposé techniquement

Sur un dépôt privé gratuit, GitHub ne permet pas d'interdire les écritures directes sur `main`. Ces règles reposent donc sur les acteurs. Un écart constaté est signalé dans un fil, et corrigé par une pull request que l'auteur accepte ou refuse.

### 4.5 Deux modes de travail

*Ajouté le 23 novembre 2026 à la demande de l'auteur.*

1. **Mode fiches.** Le seul qui fait entrer quelque chose dans le corpus : fiche TAC, prévision avant le travail, producteur, vérificateur, décision de l'auteur (`CIBLAGE.md`).
2. **Mode dialogue autonome.** Claude et ChatGPT travaillent sans intervention humaine sur les unités de `2_Methode/Dialogue_Lean/programme.json` (commit Lean figé), selon `2_Methode/Dialogue_Lean/CHARTE.md` et le protocole pré-enregistré `2_Methode/Dialogue_Lean/PROTOCOLE.md`. Le workflow écrit seulement sur la branche `ia-dialogue`. Ses sorties sont un matériau d'expérience : elles ne sont ni démontrées, ni vérifiées au sens de `CIBLAGE.md`. Elles n'ont aucun statut dans le corpus.

**Passerelle.** Pour reprendre un chapitre du dialogue, l'auteur crée une fiche, par exemple « Intégrer le chapitre E1 du dialogue Lean ». Aucun acteur ne la crée à sa place. Trois règles :
- l'**entrée** de la fiche est une **copie figée** du chapitre, déposée dans `2_Methode/Depot/TAC-xxx/` avec son empreinte, jamais le fichier vivant de `ia-dialogue` : la nuit suivante rendrait sinon la fiche périmée ;
- le **vérificateur** n'est aucune des deux IA qui ont écrit et relu ce chapitre dans la même passe. À défaut, la vérification est signalée comme **corrélée** ;
- tant que le dialogue traite le §5 (`CoreGm`), la fiche TAC-020 n'est pas assignée en parallèle, sauf si elle sert de passerelle.

**Ce que le dialogue ne touche pas.** `main`, les entrées des fiches, `2_Methode/Depot/TAC-*`, `taches.json` et le journal des fiches, et toute publication externe (Zulip, MathOverflow, dépôt Lean). Le workflow refuse d'enregistrer un changement hors de `2_Methode/Dialogue_Lean/travail/`.

**Arrêt.** Créer `2_Methode/Dialogue_Lean/STOP` sur `main`, ou désactiver le workflow `dialogue-ia`.

### 4.6 Workflows et clés API

*Ajouté le 23 novembre 2026 à la demande de l'auteur, avant le premier passage du dialogue autonome.*

Les workflows de `.github/workflows/` s'exécutent avec les secrets du dépôt, dont les clés API du dialogue. Tout acteur qui peut pousser une branche peut aussi y ajouter un workflow, et ce workflow s'exécute dès qu'il est poussé.

1. **Règle.** Aucun acteur IA ne crée, ne modifie ni ne supprime un fichier de `.github/workflows/` autrement que par une pull request de méthode : branche `methode/…`, titre contenant « [méthode] », fusionnée par l'auteur seul après son accord écrit. Cela vaut pour toutes les branches, `ia-dialogue` comprise.
2. **Contrôle.** Le workflow `garde-workflows` fait échouer :
   - une pull request qui modifie un workflow sans venir d'une branche `methode/…` ou sans « [méthode] » dans son titre ;
   - un push sur une autre branche qui modifie un workflow hors d'une branche `methode/…` ;
   - un commit qui modifie un workflow sur `main` sans provenir d'une pull request de méthode fusionnée. Dans ce cas, il ouvre aussi un fil de signalement.
3. **Limite.** Ce contrôle détecte et signale ; il n'empêche pas un workflow déjà poussé de s'exécuter, et un acteur qui peut pousser peut aussi modifier le contrôle lui-même. La protection des clés repose donc d'abord sur leur usage : **des clés dédiées au dialogue, avec un plafond de dépense dans chaque console, révocables d'un clic.** En cas de signalement, l'auteur révoque les clés et en crée de nouvelles.

### 4.7 Ajouter une source au registre

*Ajouté le 23 novembre 2026 à la demande de l'auteur.*

Le registre des sources est un registre scientifique : le modifier est un changement de méthode. Une exception est faite pour l'**ajout** d'une source, parce qu'un article ou un dépôt qui cite une référence nouvelle ne peut pas passer les tests tant qu'elle n'est pas enregistrée.

1. **Ce qui est permis hors PR de méthode.** Ajouter une ou plusieurs fiches nouvelles à `sources.json`, dans la pull request de l'article ou de la fiche qui les cite. Chaque fiche ajoutée est complète : tous les champs du registre, un lien `https`, la date et la description de ce qui a été vérifié, un statut, un verdict et un intérêt parmi les valeurs admises. Le registre et les vues sont reconstruits dans la même pull request.
2. **Ce qui reste un changement de méthode.** Modifier ou supprimer une fiche existante, y compris son verdict ou son statut. La pull request porte alors « [méthode] » et c'est l'auteur qui la fusionne.
3. **Contrôle.** Le workflow `garde-sources` compare le registre avant et après la pull request (`2_Methode/Sources/verifier_ajout_sources.py`). Il échoue si une fiche existante change ou disparaît, ou si une fiche ajoutée est incomplète.
4. **Relecture.** Une source ajoutée n'est pas vérifiée par un autre acteur avant la fusion. Le vérificateur de la fiche ou de l'article qui la cite contrôle l'entrée, et tout acteur peut la contester dans le fil. Une correction passe alors par une PR de méthode.

## 5. Répartition au 17 octobre 2026

| Fiche | Acteur | Tâche |
|---|---|---|
| TAC-007 | ia:claude | Certificat du noyau des moments à S = 0,8 |
| TAC-008 | ia:claude | Décomposer la cohérence K (diagonale, même premier, premiers distincts) |
| TAC-001 | ia:claude | Lier une instance exécutable à l'étude Bellman « noyaux et couplages » |
| TAC-009 | ia:chatgpt-sol-6.1-max | Gram de Nyman–Beurling sur des différences d'échelle |
| TAC-003 | ia:chatgpt-sol-6.1-max | Dette de Schur dans la norme duale |
| TAC-002 | ia:chatgpt-sol-6.1-max | Paquets signés : garder premiers, coupures et dette |
| TAC-004, TAC-005, TAC-006 | non assignées | Deux filtres ; corrélations de μ ; fibre à A fixé |

**Vérification croisée.** Les dépôts de ia:claude sont vérifiés par un autre acteur, et inversement. L'état vivant reste celui de `python -B 2_Methode/Pilotage/taches.py etat`.
