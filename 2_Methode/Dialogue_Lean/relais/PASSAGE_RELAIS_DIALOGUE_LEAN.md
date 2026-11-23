# Passage de relais vers le mode dialogue autonome (Dialogue Lean)

*Rédigé par Claude, depuis la conversation du « mode fiches », le 23 novembre 2026, pour la conversation « Preuve Lean de Riemann », qui met en place le dialogue autonome Claude ↔ ChatGPT. Destinataire : la session qui construit `2_Methode/Dialogue_Lean/` sur la branche `ia-dialogue`. Auteur et décideur : Vincent NOËL.*

## 1. Ce qui existe déjà en mode fiches, et qu'il ne faut pas refaire à l'aveugle

Code Lean de référence pour tout ce qui suit : `leanprover-community/riemann-hypothesis`, **commit `51d9b1a28026d458aef9c9af3df8b083276e3d2d`**. Fige ce commit dans le dialogue (`LEAN_COMMIT`), sinon les numéros de ligne divergeront.

| Module de la preuve (guide d'Alpöge) | Fiche | État au 23/11 | Pièces |
|---|---|---|---|
| §3 Landau par fenêtres, cas de ζ (`landau_window` et sa chaîne, 32 fichiers de `LandauTheorems/`) | TAC-017 | **vérifiée conforme** par ChatGPT, **acceptée** par Vincent | [PREUVE.md](https://github.com/vppnoel/Riemann/blob/main/2_Methode/Depot/TAC-017/PREUVE.md) (français, 40 liens Lean) |
| De (⋆) à RH : Landau pour une famille, critère par niveau (`formB`), ordre des choix (`level_of_tiedWin`), tous les caractères (`zeroFreeAll_of_topG`), réflexion et ζ (`Claim.*`), chaîne depuis `Main.lean` | TAC-023 | déposée, **en attente de vérification** | [NOTE_EN.md](https://github.com/vppnoel/Riemann/blob/main/2_Methode/Depot/TAC-023/NOTE_EN.md) (anglais, 92 liens) |
| §5 moyenne sur les caractères (`core_gm`, `ch_core`, poids 1/(3o + 1) et 4o) | TAC-020 | fiche **préparée, non assignée** | — |
| Analogue pour pôles doubles (hors Lean) | TAC-024 | déposée, en attente de vérification | [PREUVE.md](https://github.com/vppnoel/Riemann/blob/main/2_Methode/Depot/TAC-024/PREUVE.md) |

**Proposition : un étalonnage.** Fais d'abord passer le dialogue sur les deux modules déjà couverts, `LandauTheorems/` et la chaîne de `ZeroFreeAllOfTopG.lean`, **sans lui donner** TAC-017 ni TAC-023. Compare ensuite son texte à ces dépôts. On obtient une mesure : quelles erreurs le duo autonome rattrape, lesquelles il laisse passer, et lesquelles il ajoute. C'est la condition de contrôle la plus solide qu'on ait, puisque ces textes ont été relus et corrigés par un vérificateur, et pour TAC-017 acceptés par Vincent.

Pour éviter un travail en double, le dialogue devrait commencer ses modules **nouveaux** par §5 (`PrimitiveCosets/CoreGm.lean` et ses imports). Si c'est fait, il faut dire à Vincent de ne pas assigner TAC-020 en parallèle, ou d'en faire la passerelle.

## 2. Les erreurs réellement commises cette nuit, à faire chercher par le critique

Aucune de ces erreurs n'aurait été vue par un contrôle des seuls **noms** Lean : tous les noms cités étaient justes. Le critique doit confronter les **énoncés**, c'est-à-dire les hypothèses, les quantificateurs et les paramètres.

1. **Géométrie relâchée** (TAC-017, v1). « ρ₀ est dans le disque B(σ, σ − θ) », alors que seule sa distance **horizontale** à σ est < σ − θ. Le Lean évite ce piège par une dichotomie explicite (`landau_dichotomy`). → Faire vérifier chaque passage « donc ρ est dans tel disque ».
2. **Comparaison guide/Lean inventée** (TAC-017, v1). « Le Lean est plus général que le guide (θ quelconque) », alors que le guide énonce lui aussi 0 < θ < 1. → Toute phrase qui compare deux énoncés doit citer les deux énoncés.
3. **Mauvaise fonction optimisée** (TAC-017, v1). Le script cherchait les zéros de G′ pour maximiser |G − log 2π|/√y. Le bon résultat était tombé par hasard. → Un critique qui relit un calcul doit dériver lui-même la condition d'optimalité.
4. **Statut d'un lemme sous-estimé** (TAC-023, prévision P2). `level_gm_le_on_family_scales` tient en une ligne, mais il appelle `windowInequality_of_artinInputs`, qui appelle `core_gm` : c'est la moyenne du §5, pas une formalité. → Un lemme court n'est pas un lemme facile. Il faut suivre les appels jusqu'au contenu.
5. **Paramètre généralisé à tort** (TAC-021). « Pour tout λ > 1 », alors que les hôtes ne sont fournis que pour λ = 3/2 (`supplyChi`) et que des fenêtres [Y, Y^(3/2)] ne donnent pas [Y, Y²]. → Traquer les « pour tout » qui viennent d'un énoncé paramétré mais utilisé en un seul point.
6. **Cas limite oublié** (TAC-021). Dans `Claim.zeta`, s = 0 doit être exclu par ζ(0) = −½ **avant** la réflexion, parce que Mathlib donne à Γ la valeur 0 en ses pôles. → Les conventions de Mathlib (valeurs aux pôles, division par zéro = 0) créent des cas limites invisibles en mathématiques ordinaires.
7. **Analyse fausse hors Lean** (TAC-022). Un contour déplacé alors que l'intégrande n'était pas absolument intégrable (un terme en 1/|t|). → Pour toute intégrale complexe : convergence absolue, segments horizontaux, résidus récupérés.
8. **Auto-évaluation complaisante.** Le producteur a jugé ses prévisions « justes » après des vérifications partielles. → Dans le dialogue, l'auteur ne doit pas noter sa propre explication. Seul le critique note, ou mieux, un troisième passage.

## 3. Le contrôle mécanique minimal

Le contrôle des noms prévu dans `dialogue_ia.py` est nécessaire mais insuffisant. Le script joint, `verifier_liens_lean.py` (bibliothèque standard seulement), vérifie pour chaque lien Lean du texte :
- que le commit est celui attendu ;
- que le fichier existe à ce commit ;
- que la ligne citée contient bien la déclaration nommée.

Il fonctionne sur un clone **partiel** (`git show`), sans tout télécharger. Testé sur la note de TAC-023 : 92 liens, 40 fichiers, 2 écarts, tous deux voulus (l'étiquette est un nom de fichier, pas de déclaration).

```
python3 -I verifier_liens_lean.py TEXTE.md CHEMIN_DU_CLONE_LEAN [COMMIT]
```

Suggestion : imposer dans la charte que chaque déclaration citée ait un lien `fichier#Lnn`, et faire tourner ce script avant que le critique ne lise. Un écart doit valoir REVISER automatiquement.

## 4. Pièges techniques rencontrés avec le dépôt Lean

- **Taille.** Le dépôt est très gros. `EveryCharacterOfLiteratureOfVWin.lean` compte 5 945 lignes, dont plus de 5 300 imports. Cloner avec `--filter=blob:none --sparse`, puis faire `git sparse-checkout add` répertoire par répertoire.
- **`git grep` sur un clone partiel** télécharge les objets un par un : c'est très lent, voire bloquant. Il vaut mieux ajouter le répertoire en sparse-checkout, puis faire un `grep` local. La recherche de code de l'API GitHub n'a rien renvoyé sur ce dépôt.
- **Répertoires utiles** pour la partie analytique et l'assemblage :
  - `src/Development/AutomorphicArithmetic/DedekindLFunctions/` (et `LandauTheorems/`) ;
  - `src/Development/AutomorphicArithmetic/CharacterBoxes/` ;
  - `src/Development/AutomorphicArithmetic/PrimitiveCosets/` ;
  - `src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/` ;
  - `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/` (le haut de la chaîne) ;
  - `src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/` (pour `HostExW`).
- **Les noms sont qualifiés par des espaces de noms**, souvent ouverts plus haut dans le fichier : `UpperTheory.Top.`, `UpperTheory.Comparison₂.`, `Formalism.HC.`, `Deduction.`, `GlobalTheory.EX.`. Un contrôle des noms doit accepter le dernier composant seul.
- **Le tarball de codeload est refusé** depuis l'environnement de Claude. Le clonage git fonctionne.

## 5. Ce que le dialogue ne doit pas toucher

- `main`, et tout fichier listé comme **entrée** d'une fiche. Une seule modification rend la fiche périmée. C'est arrivé cette nuit, deux fois : TAC-013, et TAC-021/022 à cause d'un fichier de vérification réécrit.
- Les dossiers `2_Methode/Depot/TAC-*`, `taches.json` et le journal.
- Toute publication externe : Zulip, MathOverflow, le dépôt Lean. Rien n'en sort sans la décision de Vincent.

## 6. Pour la passerelle vers le mode fiches

Quand un chapitre du dialogue paraît bon à Vincent, la fiche d'intégration devrait prendre en **entrée** une copie figée du chapitre, avec son empreinte, et non le fichier vivant de la branche `ia-dialogue`. Sinon, la nuit suivante la rendra périmée. Le vérificateur de cette fiche ne devrait être aucune des deux IA qui ont écrit le chapitre dans la même passe. À défaut, il faut le signaler comme une vérification corrélée.
