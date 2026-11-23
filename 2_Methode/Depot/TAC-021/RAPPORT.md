# TAC-021 (reprise de TAC-019) — Piste 1, module 1 : de (⋆) au théorème, une preuve lisible confrontée au Lean

*Producteur : ia:claude · 23 novembre 2026 · branche `tac-021`. Auteur et titulaire des droits : Vincent NOËL. Fil : [#53](https://github.com/vppnoel/Riemann/issues/53) (historique : [#46](https://github.com/vppnoel/Riemann/issues/46)). Code Lean consulté : `leanprover-community/riemann-hypothesis`, commit `51d9b1a`.*

**En une phrase.** Toute la partie analytique de la preuve annoncée, de la borne arithmétique (⋆) jusqu'à RH, tient en environ cinq pages lisibles, en anglais (`NOTE_EN.md`), chaque étape renvoyant à sa déclaration Lean. Elle n'utilise que de l'analyse classique, les facteurs d'Euler et l'équation fonctionnelle. C'est le premier module de la piste 1, prêt à être proposé à la communauté une fois vérifié.

## Prévision

Enregistrée pour TAC-019 le 23 novembre 2026 à 1 h 50 UTC (commit `3dd43b0`), avant l'ouverture des fichiers Lean concernés. **Recopiée après coup pour TAC-021**, avec mention explicite dans le registre : sa valeur de prévision vient uniquement de l'enregistrement d'origine. En résumé :
- **P1** : aucun ingrédient au-delà de TAC-017 et du §1 ; 4 à 6 pages.
- **P2** : pas de traitement spécial des zéros de Siegel.
- **P3** : les poids précis ne jouent aucun rôle, seule leur positivité compte.
- **P4** : le (⋆) de Lean a la forme du guide, à un écart de forme près.
- **P5** : la réduction aux caractères primitifs se fait **avant** Landau, et l'équation fonctionnelle seulement à la fin.

## Méthode

J'ai lu au commit `51d9b1a` :
- `Main.lean` et `Statements.lean` ;
- dans `CharacterBoxes/` : `ZeroFreeAllOfTopG`, `ClaimStrip`, `HalfPlane`, `Imprimitive`, `EveryCharacter` et `MainConclusion` ;
- `PrimitiveCosets/Imports` (`formB`) ;
- dans `TotientGaloisClasses/` : `TopWin`, `Window`, `TopDefs`, `ExplicitFormulaErrorOfHostConditions` (`Level`, `wt`, `Gm`, `Level.cyc`) et `PrimePairSizeCondition` (`PChar`, `KSet`) ;
- `LandauTheorems/poleData` (`poleData`), en plus des fichiers de TAC-017.

Les preuves de `formB`, `level_of_tiedWin`, `zeroFreeOn_of_tiedWin(_cyc)`, `zeroFreeAll_of_topG`, `imprimitive`, `strip`, `zeta`, `prim_zero` et `prim_reflect` ont été lues en entier. Un seul chemin n'a pas été tracé : comment `every_character_of_literature_of_vWin` appelle `ZeroFreeAll`. La note le dit (§6).

## Résultat

| | Prévision | Résultat | Verdict |
|---|---|---|---|
| **P1** | aucun ingrédient de plus ; 4 à 6 pages | aucun : Mellin, forme logarithmique, croissance grossière, Cauchy, Chernoff, facteurs d'Euler, équation fonctionnelle ; environ 5 pages | **juste** |
| **P2** | pas de traitement de Siegel | aucun code dédié : un zéro réel est un pôle de résidu > 0, traité par le cas 1 de `landau_window` | **juste** |
| **P3** | seule la positivité des poids compte | `formB` vaut pour **tout** `Level` : il ne demande que wt > 0 | **juste** |
| **P4** | écart de forme seulement | exposant ½ + (e_D + e_L + 7)ε avec des constantes existentielles, au lieu de ½ + 9ε ; fenêtres [Y, Y^λ] pour tout λ > 1 | **juste** |
| **P5** | réduction aux primitifs avant Landau ; équation fonctionnelle à la fin | Landau porte d'emblée sur des caractères **primitifs** (`PChar`) ; la réduction des imprimitifs vient **après** `ZeroFreeAll` (`imprimitive`) ; l'équation fonctionnelle n'apparaît qu'à la fin (`strip`, `zeta`) | **à moitié juste** : l'ordre de la réduction est inverse de celui prévu |

## Portée

1. **Ce qui est établi.** Une preuve complète et lisible de l'implication « (⋆) pour tout ψ primitif ⟹ GRH pour les fonctions L de Dirichlet ⟹ RH », confrontée au Lean déclaration par déclaration. Ce n'est pas un résultat nouveau : c'est une **exposition**, et c'est l'objet de la piste 1.
2. **Pourquoi c'est utile maintenant.** Le guide résume cette partie en quelques paragraphes, et il n'existait pas, à ma connaissance, de preuve lisible complète de cette partie confrontée au Lean. Elle délimite exactement ce qui reste à comprendre : l'énoncé `TopG`, c'est-à-dire (⋆), et lui seul.
3. **Ce que cela montre de la structure.** La partie analytique est « universelle » : elle ne sait rien de l'arithmétique. Toute la difficulté, et tout le produit d'Euler au sens fort, est dans (⋆). Cela confirme TAC-016 (le Sosie franchit cette partie) et TAC-017.
4. **Limites.**
   - Le lien `everyCharacter` ← `ZeroFreeAll` n'a pas été tracé ligne à ligne.
   - La note n'a pas encore été vérifiée par un autre acteur.
   - **Rien ne doit être posté à l'extérieur sans la décision de l'auteur.**

## Reprise

**Provenance.** Ce dossier reprend celui de TAC-019. TAC-019 a été retirée avant vérification parce qu'elle héritait d'un défaut de TAC-017, puis elle est devenue périmée quand la reprise de TAC-017 a modifié son entrée.

**Corrections apportées à la note (`NOTE_EN.md`)**, toutes issues de la vérification de TAC-017 ([#40](https://github.com/vppnoel/Riemann/issues/40)) :
1. **Le §2 rappelle maintenant le cœur géométrique de l'argument**, avec la dichotomie exacte du Lean (`landau_dichotomy`, cas A et B). La note ne dépend donc plus de l'étape 5 erronée de la première version de TAC-017.
2. **Le tableau du §8 est corrigé.** La Proposition de Landau a **les mêmes** paramètres dans le guide et dans le Lean (0 < θ < 1). La ligne sur les fenêtres est reformulée sans parler de généralité.
3. **Chaque déclaration Lean est un lien** vers sa ligne au commit `51d9b1a` (51 liens).
4. Un paragraphe « Revision » signale ces corrections au lecteur.

Le reste (§§1, 3–7) est inchangé : la vérification de TAC-017 ne le mettait pas en cause.

## Critère de rejet

Le critère de la fiche portait sur trois points :
- un ingrédient analytique non prévu : **aucun** ;
- un (⋆) différent sur le fond : **non** ;
- une note qui paraphraserait le guide : non, chaque théorème a sa preuve.

**Il n'est pas atteint.** Le vérificateur peut réfuter ce rapport par :
- une déclaration Lean mal citée ;
- une étape de preuve qui ne correspond pas au code ;
- un usage caché d'un autre résultat dans `level_of_tiedWin` ou `formB`.

## Statut proposé

**demontre**, au sens d'une exposition complète, confrontée au Lean, de la partie analytique. Je demande la vérification à `ia:chatgpt-sol-6.1-max`. Points à regarder en priorité :
1. le §2 de la note, avec la forme du résidu pour une famille et le rôle des conjugués ;
2. le §4, avec le choix de ε et de θ ;
3. le §6 et le chemin non tracé.

**Suite proposée (piste 1)** : le module 2 serait le §5 du guide, la moyenne sur les caractères et l'ensemble épais de Behrend, avec le bilan qui donne le « 9 ». C'est le module accessible suivant.
