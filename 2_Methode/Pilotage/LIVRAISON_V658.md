# Livraison V6.58 — note de livraison

**17 octobre 2026 · Vincent NOËL.** Cette note dit ce qui a changé, pourquoi, et ce qui reste à décider. Les résultats scientifiques sont dans les documents 80 et 81 ; l'entrée du corpus est le [README](../../README.md).

## 1. Résultats

- [Document 80 : d'où vient le signe](../../1_Presentation/80_D_OU_VIENT_LE_SIGNE.pdf). Dans le Modèle réduit, comptages et degrés d'isogénie restent positifs pour 119 faux jumeaux qui violent RH ; seule la trace d'un carré (Rosati) les exclut. Prévisions G1 à G4, toutes justes.
- [Document 81 : Zhu reproduit](../../1_Presentation/81_ZHU_REPRODUIT.pdf). Les valeurs de Zhu sont retrouvées par une méthode indépendante, non certifiée. Sur le noyau des moments, la marge vaut 9,2·10⁻⁴ à 11/20 (le document 75 certifie 3·10⁻⁴) et 5,4·10⁻¹² à 0,8. Prévisions Z1 à Z5, toutes justes.

## 2. Intégration au pilotage, selon le protocole

| Outil | Modification |
|---|---|
| Registre des identifiants | DOC-080 et DOC-081 ; aucun numéro réattribué. |
| Navigateur | Trois actions : `v658_trois_niveaux` et `v658_zhu_reproduit` (faites) ; `v658_certificat_noyau_S08` (route à construire, prévision écrite avant, aucune probabilité attribuée). Bilan `bilan_v658`. |
| Indicateur | Étape V6.58. Les sept niveaux sont inchangés : le mécanisme du signe est localisé dans le Modèle réduit, pas pour ζ ; aucune fenêtre nouvelle n'est certifiée. |
| Pilotage | Évaluations « Voir », « Comprendre », « Croiser » et « La case vide » motivées et reliées aux documents 80 et 81 ; fiches IDE-022, IDE-036, IDE-040 et IDE-048 reliées ; investigation `noyau_S08` pré-enregistrée. |
| Sources | Zhu26 mise à jour (PDF relu, valeurs reproduites) ; Wei48 reliée au document 80 ; Mum70 ajoutée (livre non consulté, renvoi au §21 confirmé indirectement). |
| Empreintes revues | `registre_figures.json` (FIG-081, FIG-082), `42_REGISTRE_DES_SOURCES.md` (régénéré), `carte_navigation.json` (trois actions), et les compléments 76 et 79 (marque BOM et section « Références » générée, texte inchangé). Chaque écart a été relu avant la mise à jour de l'empreinte. |

Le script `2_Methode/Outils/integrate_v658.py` fait ces modifications de données ; il est idempotent.

## 3. Réorganisation de l'entrée

- Le README ne garde que l'entrée : **À lire d'abord** (six points, leurs statuts et leurs liens), ce qui change, où aller, organisation, reproduction, licences.
- Le bloc « À lire d'abord » a une source unique, `points_d_attention.json`, rendue aussi en tête du portail.
- [Plan du corpus](../../PLAN_DU_CORPUS.md) : les 81 documents rangés en sept questions, avec leurs fichiers.
- [Historique des livraisons](../../HISTORIQUE_DES_LIVRAISONS.md) : tous les anciens README, conservés tels quels.
- Les quatre pages principales renvoient au README, au plan et à l'historique.
- Aucun document n'est déplacé ni renuméroté : les liens, les identifiants et les inventaires d'intégrité restent valides.

## 3 bis. Outils de lecture

Trois documents à la racine, générés depuis les données par `2_Methode/Outils/build_outils_de_lecture.py`. Le test `test_v658_integrite` vérifie qu'ils restent à jour.

- **[Table logique](../../TABLE_LOGIQUE.md)** ([PDF](../../TABLE_LOGIQUE.pdf)) :
  - 32 énoncés en forme logique (hypothèses, statut, portée, pièce), répartis sur cinq routes vers RH : Weil, le carré, l'énergie Q, l'énergie J, la réalisation spectrale ;
  - trois témoins contraires et sept obstructions ;
  - la « coupe ouverte » de chaque route, avec les investigations qui la visent ;
  - les 79 relations typées du graphe des idées, avec leurs gardes.
  
  Le statut d'une fiche est lu en direct dans le pilotage. Le statut propre d'un énoncé, par exemple un critère classique dont la conclusion reste ouverte, est donné dans `table_logique.json`.
- **[Références hiérarchisées](../../REFERENCES_HIERARCHISEES.md)** ([PDF](../../REFERENCES_HIERARCHISEES.pdf)) : 177 fiches en quatre rangs.
  - A, fondements logiques (23) : les références citées par une ligne de la table ;
  - B, confrontations (34) ;
  - C, appuis et outils (58) ;
  - D, contexte (62).
  
  Dans chaque rang, l'ordre suit l'usage dans le corpus. Une section 0 liste les 24 fiches des rangs A et B dont la vérification est partielle ou l'usage jugé imprécis. Le registre complet reste le document 42.
- **[Guide pour une IA](../../GUIDE_POUR_UNE_IA.md)** : un prompt à copier, qui donne :
  - ce qu'il faut lire, et dans quel ordre ;
  - les sources de vérité ;
  - dix règles de méthode ;
  - les commandes ;
  - la procédure pour déterminer les prochaines étapes (coupe ouverte, chantiers existants, Bellman, six critères, obstructions à écarter, au plus trois propositions en tableau) ;
  - ce qu'il faut rendre et ce qu'il ne faut pas faire.
  
  Il est suivi d'un état courant régénéré.

Les PDF sont rendus avec pandoc et Chromium, en A4 paysage.

## 3 ter. Couche anglaise et correctif de portée

- **En anglais :**
  - `README_EN.md` ;
  - `LOGICAL_TABLE.md` (et PDF), `REFERENCES_RANKED.md` (et PDF), `GUIDE_FOR_AN_AI.md` ;
  - les documents 80 et 81 dans `1_Presentation/english/`, avec leurs figures anglaises (scripts : option `--figure-en`).
  
  Ces fichiers sont générés à partir des mêmes données que les versions françaises. Le reste du corpus reste en français ; les trois articles et le dossier de relecture existaient déjà en anglais.
- **Correctif du 17 octobre (document 81, §4).** Le minorant certifié de Zhu, λ*(0,8) ≥ 8,9·10⁻¹⁸, vaut pour toutes les fonctions de support [−0,8 ; 0,8], donc aussi sur le noyau des moments. Il couvre en portée les certificats des documents 71 à 75. Certifier la marge du noyau à 0,8 donnerait une marge indépendante, environ 10⁵ fois plus forte, mais pas une fenêtre nouvelle. La portée est corrigée partout : document 81, table logique, action du navigateur, investigation, évaluation « La case vide », bloc « À lire d'abord ».

## 3 quater. Pré-publication : proposition (décision de l'auteur)

1. **D'abord l'article 1** (Théorèmes A et B, critère conjoint RH–simplicité), en anglais, 10 pages. C'est le candidat le plus solide. Son résumé ne revendique déjà aucun progrès vers RH.
   - arXiv demande, depuis décembre 2025, un parrainage personnel en mathématiques pour un premier dépôt sans article de mathématiques antérieur.
   - Il faut donc d'abord un spécialiste, qui peut à la fois relire et parrainer. C'est l'usage prévu de la lettre « Cher Professeur » et du dossier `relecture/`.
2. **Ensuite l'article 2, enrichi du document 80.** Il compte déjà l'inertie de la forme d'intersection sur 425 courbes et 220 faux jumeaux. Les trois niveaux (comptage, degré, carré) et les 119 faux jumeaux dont les degrés sont positifs le rendent plus net.
3. **Un dépôt du corpus avec DOI** (archive ouverte), sans parrainage, pour dater et rendre citables les programmes et les données. Ce serait la couche d'entrée anglaise, avec le corpus complet en annexe.
4. **À ne pas pré-publier seuls :**
   - les certificats par fenêtres (docs 71 à 75), dominés en portée par Zhu ;
   - les mesures du document 81.
   
   Ils servent d'appui reproductible, pas de résultat principal.

## 4. Réparations

- **Pages générées désynchronisées en V6.57.** Le registre des sources, le registre des identifiants et la matrice ne reflétaient plus leurs données. Ils sont régénérés, et rien n'est perdu : les fiches SuzH23 et SuzSig23, ajoutées à la main en bas du registre, figurent maintenant dans les tables.
- **Calcul du noyau des moments.** Il est désormais scripté (`run_zhu_reproduction.py --noyau`) et redonne exactement les valeurs du document 81. Une première version par Gram–Schmidt était instable, car les composantes du moment décroissent plus vite que toute exponentielle : elle donnait des valeurs non monotones. Elle est remplacée par un réflecteur de Householder et décrite dans le document 81.
- **Tests dont l'écart venait du test, et non d'un résultat :**
  - `test_v610` : le statut « partiel », introduit en V6.42, est admis.
  - `test_v632` : la marque BOM est exigée partout, sauf dans `4_Archives` et pour les 25 originaux figés listés dans `originaux_figes.json`. Ces originaux sont des copies identiques enregistrées dans les inventaires d'intégrité, et le nouveau test `test_v658_integrite` vérifie leurs empreintes.
  - `test_v618` : les originaux figés sont exemptés de la section « Références » générée.
  - `test_v637` : la sélection figée est identique ; seule la version de NumPy consignée diffère d'un environnement à l'autre, et elle est neutralisée dans la comparaison.
  - `test_v6111` : il vérifie maintenant la carte des idées dans la grammaire V6.55 (`data-node`, en-tête « Programme Riemann · V… »), car la carte V6.11 a été remplacée. Il lit le numéro de version dans `VERSION.txt`, et son contrôle de liens ignore les gabarits JavaScript embarqués.

## 5. Décisions de l'auteur (17 octobre)

1. **Registres V6.44 à V6.50 déclarés historiques**, à la demande de l'auteur (« Déclarer historique le pb des versions 6.50 versus 6.55 »).
   - La déclaration est dans `3_Preuves_et_calculs/data/registres_historiques_v650.json` : 27 instantanés avec leur empreinte, et les fichiers du pilotage qui les remplacent.
   - Les quatre tests concernés (`test_v644`, `test_v645` ×2, `test_v646`) vérifient maintenant ces registres pour eux-mêmes : fichier inchangé, fiches de sources bien formées, étape de l'indicateur à sa place. Ils ne les comparent plus au corpus courant.
   - L'index courant du code doit seulement se lire sans erreur d'analyse.
2. **Synthèse (doc. 01) et guide de lecture (doc. 07) mis à jour en V6.58**, en français, avec une version anglaise (`1_Presentation/english/01_SYNTHESIS_EN`, `07_READING_GUIDE_EN`).
   - Les versions V6.24 sont conservées dans `4_Archives/historique/` : fichiers ajoutés, aucun fichier existant modifié.
   - Le guide reçoit quatre images nouvelles : le Lego et les fenêtres, la dette des couplages, l'amplification, comptage-degré-carré. L'anglais en est une adaptation condensée et complète.
3. **Encore ouvert : quoi pré-publier.** Voir la proposition au § 3 quater.
4. **Numéros 76 et 79.** Chacun porte deux pièces (un document et son complément). La règle de non-renumérotation les garde tels quels, et le plan du corpus les distingue.

## 6. Vérifications

Elles sont faites sur une copie propre, issue des deux archives partielles :
- `sha256sum -c CHECKSUMS.sha256` ;
- `verify_contracts.py` et `verify_pilotage.py` ;
- toute la suite de tests, qui doit passer entièrement depuis que les registres V6.50 sont déclarés historiques.
