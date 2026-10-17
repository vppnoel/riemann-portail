# Travailler sur GitHub — Programme Riemann

*V6.59 · 17 octobre 2026 · Vincent NOËL. Ce texte applique à GitHub la procédure de [`CIBLAGE.md`](2_Methode/Pilotage/CIBLAGE.md). Il ne la modifie pas.*

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
| Produire | Branche `tac-xxx` (par exemple `tac-007`), qui ne contient que `2_Methode/Depot/TAC-xxx/`. Le contrôle automatique refuse tout autre fichier. |
| Déposer | Pull request de la branche, avec le modèle fourni. Après fusion sur `main` : `taches.py deposer`, puis commit. |
| Vérifier | Un **autre** acteur relit la pull request ou le dossier fusionné. Il ajoute `TAC-xxx/verification/VERIFICATION.md` (branche `tac-xxx-verif`), puis lance `taches.py verifier` sur `main`. |
| Décider | L'auteur seul : `taches.py decider` sur `main`. **Fusionner une pull request n'est pas accepter un résultat** : la fusion fait seulement entrer le dépôt. |
| Intégrer | Après acceptation : documents, pilotage et indicateur selon le protocole, par un script d'intégration ; reconstruction, tests, sommes de contrôle, puis une étiquette de version (`v6.60`…). |

**Contrôles automatiques** (`.github/workflows/verifier.yml`), à chaque push et pull request :
- périmètre des branches `tac-xxx` ;
- `taches.py controler` ;
- `verify_ciblage.py` et le contrôle de l'interface ;
- `verify_contracts.py` et `verify_pilotage.py` ;
- la suite de tests.

Les sommes de contrôle ne sont recalculées qu'à la livraison d'une version.

**Un acteur sans accès au dépôt** (une IA dans une autre application, par exemple) reçoit l'archive et une consigne de lot (`2_Methode/Pilotage/lots/`) :
1. il rend d'abord ses prévisions ;
2. l'auteur les enregistre ;
3. l'acteur rend ensuite ses dossiers `TAC-xxx/`, que l'auteur dépose sur une branche `tac-xxx`.

## 4. Répartition au 17 octobre 2026

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
