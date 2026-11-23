# TAC-023 — Piste 1, module 1 (v3) : de (⋆) au théorème, note anglaise complétée

*Producteur : ia:claude · 23 novembre 2026 · branche `tac-023`. Auteur et titulaire des droits : Vincent NOËL. Fil : [#64](https://github.com/vppnoel/Riemann/issues/64). Code Lean consulté : `leanprover-community/riemann-hypothesis`, commit `51d9b1a` (23 novembre 2026). Reprise de TAC-021, périmée.*

**En une phrase.** *Reprise du 23 novembre 2026 : la définition de `HostExW` et trois points mineurs sont corrigés après vérification (voir « Reprise »).* La note anglaise (`NOTE_EN.md`) applique maintenant les trois corrections demandées par la vérification de TAC-021 : un §2 autonome, un §5 qui sépare (⋆) de ses trois entrées formelles, et le cas s = 0 au §6(c). Elle trace en outre toute la chaîne Lean, de `Main.lean` jusqu'au théorème 4. La lecture du code a réfuté une de mes prévisions : le lemme `level_gm_le_on_family_scales` n'est pas une formalité analytique, c'est la moyenne sur les caractères du §5 du guide.

## Prévision

Enregistrée le 23 novembre 2026 vers 2 h 55 UTC (commit `b97c21f` sur `main`), après lecture de la vérification de TAC-021, mais avant d'ouvrir les fichiers Lean concernés. Elle est **nouvelle**, et non recopiée de TAC-021. Texte intégral dans le journal (`journal_taches.json`, événement 102). En résumé :
- **P1** : les compléments (1) et (3) n'exigent aucun ingrédient nouveau.
- **P2** : `level_gm_le_on_family_scales` est un lemme de comparaison, de l'analyse élémentaire sans rien d'automorphe.
- **P3** : `HostExW` affirme l'existence de « corps hôtes » sur des fenêtres ; c'est une hypothèse arithmétique, du côté de (⋆).
- **P4** : `every_character_of_literature_of_vWin` prend des énoncés de la littérature et la fenêtre cohomologique, et passe par `zeroFreeAll_of_topG` puis `imprimitive`.
- **P5** : après les compléments, rien dans la note ne dépendra d'une lecture non faite, sauf TopG et les hôtes, qui seront marqués comme admis.

## Méthode

1. **Lecture du code Lean** au commit `51d9b1a`, par clonage partiel. J'ai lu :
   - la preuve complète de `landau_window_key`, `landau_window_contra` et des deux cas de `landau_window` ;
   - les énoncés de `landau_window_ineq`, `landau_tails`, `landau_coeff`, `landau_growth_contra`, `windowHyp_of_rpow`, `WindowHypU` et `WindowHyp` ;
   - les définitions de `HostExW`, `Scales`, `VWin`, `VWinAt`, `TopG`, `GChi`, `cls`, `ChebyshevInequalityOnWindows`, `ChebyshevInequalityAtWindowScale` et `OpenLiteratureStatements` ;
   - les preuves de `zeroFreeAll_of_topG`, `level_of_tiedWin`, `supplyChi`, `Claim.zeta`, et les termes d'appel de `MainConclusion.lean`, `EveryCharacterOfLiteratureOfVWin.lean`, `SiegelEisensteinSecondTermHypotheses.lean` et `TopPlug.lean` ;
   - l'énoncé de `core_gm` et la liste des faits qu'utilise sa preuve, mais pas cette preuve ligne à ligne.
2. **Rédaction** de la note à partir de la version de TAC-021 (entrée figée, empreinte `52fa6cb2…`) et de la preuve vérifiée de TAC-017 (`7aa1000a…`). Les deux empreintes sont toujours valides au moment du dépôt.
3. **Contrôle des liens** par un script : 92 liens vers 40 fichiers Lean. Chaque fichier existe au commit cité, et chaque ligne citée contient la déclaration nommée. Les deux seules exceptions sont voulues : `Main.lean#L13` pointe sur `riemannHypothesis`, et `TopPlug.lean#L19` sur l'appel `zeroFreeAll_of_topG (la := 3 / 2)`.

## Résultat

**Les trois corrections.**
1. **§2 autonome.** La note définit U = log Y, la fonction de majoration R(u) = |C|e^(θu) sur la fenêtre, et les moments A_k(s) = (−1)^k Φ_F^(k)(s)/k!. Elle démontre l'inégalité clé (K), |A_k(σ + iγ)| + Re A_k(σ) ≤ C₁e^(ηU)/(σ − θ)^k avec k ≥ U, à partir de :
   - l'identité |g| + g = 2g⁺ ;
   - le découpage de l'intégrale, la fenêtre étant contrôlée par le maximum du noyau, et les queues par `landau_tails` (énoncé seulement) ;
   - le lemme numérique de contradiction, avec η = ½ log(e/d) < log((σ − θ)/d).
   Elle explique pourquoi il faut k ≥ U : la perte e^(ηU) venue de la fenêtre est battue par le gain (e/d)^k venu du pôle. Les cas (A) et (B) sont détaillés, avec les estimations de Cauchy.
2. **§5.** Le théorème 4 a maintenant **deux** hypothèses explicites : TopG, et les hôtes `HostExW λ (GChi ψ).req`. Il s'appuie en outre sur deux lemmes, `level_gm_le_on_family_scales` et `formB`. Les définitions de `HostExW` (avec `Scales`), de `TopG` et de `GChi` sont données. Les trois hypothèses du théorème 3 sont attribuées chacune à son entrée. Le tableau a une nouvelle ligne « (⋆) dans son ensemble ». Le paragraphe « On the parameter λ » dit que des hôtes pour λ = 3/2 ne donnent pas les autres λ, et que toute la chaîne formelle utilise λ = 3/2 (`supplyChi`, `TopPlug`).
3. **§6(c).** On établit d'abord s ≠ 0 par ζ(0) = −½. Il le faut parce que Mathlib donne à Γ la valeur 0 en ses pôles, de sorte que Γ_ℝ s'annule exactement en 0, −2, −4, … La réflexion vient ensuite. Le §6(e) précise qu'appliquer le moteur de Landau à DH ne lui fournit pas (⋆).

**Les deux définitions demandées.**
- `HostExW λ P` [ThinScalesIffHostBound.lean, l. 102] : pour tout 0 < ε < 1/52, il existe des constantes et une famille d'échelles S, de paramètre S.J fixé, dont l'ensemble S.Win contient des fenêtres entières [Y, Y^λ] arbitrairement loin. Toute échelle **de la famille** (s.eps = ε, s.J = S.J, s.x ∈ S.Win), de point assez grand, porte alors un hôte qui vérifie `RankVal`, `HostGood` et l'exigence P. *(Corrigé à la reprise : la première version omettait la condition s.J = S.J.)*
- `every_character_of_literature_of_vWin` [EveryCharacterOfLiteratureOfVWin.lean, l. 5943] : `(O : OpenLiteratureStatements) (hV : VWin) : EveryCharacter`. La structure O a trois champs : Caraiani local–global, existence de Langlands local, et représentations galoisiennes des paires polarisées.

**La chaîne tracée (§6(d)) :**

everyCharacter → everyCharacter_of_row → every_character_of_literature_of_vWin → every_character_of_theta_integrals_local_matching → every_character_of_green_v_win = imprimitive ∘ zero_free_all_of_green_v_win → zeroFreeAll_of_topG (λ = 3/2), avec hôtes = supplyChi ψ (hV ψ).

| | Prévision | Résultat | Verdict |
|---|---|---|---|
| **P1** | (1) et (3) sans ingrédient nouveau | (1) reprend les étapes de TAC-017 et du Lean ; (3) se règle par ζ(0) = −½ et la convention de Mathlib pour Γ | **juste** |
| **P2** | `level_gm_le_on_family_scales` = comparaison élémentaire | c'est un appel à `windowInequality_of_artinInputs`, donc à `core_gm`, qui transforme les données d'hôte (`EAtH`, `CoreAtH`) en borne sur Λ.Gm par une somme de caractères pondérée : c'est la **moyenne du §5 du guide** | **fausse** (l'absence d'automorphe n'est pas vérifiée : preuve non lue) |
| **P3** | HostExW = hôtes sur fenêtres, hypothèse arithmétique sans analyse | juste sur le fond ; l'exigence contient une borne d'erreur `EAtH` et une borne cohomologique `VVle`. Les corps de type `IsChiField` (sous-corps cyclotomiques découpés par ψ, q, d) n'apparaissent qu'en amont, dans `VWinAt`. Je les avais appelés « CM », ce que je n'ai pas vérifié | **juste sur le fond, imprécise sur le détail** |
| **P4** | chemin par `zeroFreeAll_of_topG` puis `imprimitive` | oui, mais par trois termes intermédiaires que je n'avais pas prévus (intégrales thêta, hypothèse « Green ») | **juste** |
| **P5** | seules restent admises TopG et les hôtes | restent aussi admis `core_gm` (entrée 3) et le mécanisme interne de `landau_tails`, tous deux marqués dans la note | **juste, mais incomplète** : l'entrée 3 s'ajoute à la liste |

*Ces verdicts sont ceux du producteur. Lors des fiches précédentes, j'ai eu tendance à juger « juste » trop vite (voir TAC-017 et TAC-016) ; le vérificateur doit les rejuger.*

## Portée

1. **Une frontière plus nette entre analyse et arithmétique.** La version précédente laissait croire que tout ce qui précède le théorème 3 relevait de TopG. En Lean, (⋆) est en fait assemblée de **trois** entrées : les hôtes, les familles et la moyenne. La troisième, `core_gm`, est la moyenne du §5 du guide. La partie que la note démontre se réduit à Landau par fenêtres, au critère par niveau, à l'ordre des choix et à la réflexion. Elle est plus petite qu'on pouvait le croire, mais exactement délimitée.
2. **Pour TAC-020 (module 2, moyenne sur les caractères).** La cible est maintenant localisée : `core_gm` et ses imports (`ch_core`, `charsA`, `GmAEq`, `SigALe`, `hostFactsS`). Le module 2 devra partir de là.
3. **Pour le Sosie.** Le §6(e) le dit : DH doit échouer dans les entrées 1 à 3, pas dans le moteur analytique. C'est cohérent avec TAC-016, qui situait l'échec à l'étape des entiers.
4. **Anti-circularité.** Rien n'utilise RH. La note démontre une implication, (⋆) ⇒ GRH ⇒ RH, et n'affirme pas (⋆).

## Reprise (23 novembre 2026, après la vérification)

La vérification de `ia:chatgpt-sol-6.1-max` ([`verification/VERIFICATION.md`](verification/VERIFICATION.md), PR [#70](https://github.com/vppnoel/Riemann/pull/70)) a jugé le dépôt **non conforme**. Elle valide la déduction (⋆) ⇒ GRH ⇒ RH, mais relève un écart et trois retouches. Tous les quatre sont fondés et corrigés dans `NOTE_EN.md` (quatrième version) :

1. **Définition de `HostExW` (écart bloquant).** J'avais écrit que tout point grand d'une fenêtre porte un hôte. Le Lean ne le promet que pour les échelles d'**une famille** S : `S.Mem s` exige s.J = S.J et s.x ∈ S.Win ([Scales.lean, l. 23](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/PrimeDiscriminants/Scales.lean#L23)). Une échelle de même ε et de même point mais d'un autre J n'est pas couverte. Le §5 reprend la formulation proposée par le vérificateur, et le dit explicitement. J'avais lu la structure `Scales` sans lire `Mem` : c'est une erreur de lecture, du même type que la P2 fausse de ce dépôt (s'arrêter à l'énoncé de surface).
2. **Deux liens `landau_pole_asym`** pointaient à la ligne 14, où commence `landau_pole_asym_deriv`. Ils pointent maintenant à la ligne 23. Mon contrôle mécanique ne l'avait pas vu, parce qu'il acceptait un nom qui n'est que le préfixe d'un autre. Le script est corrigé à part (PR de méthode), et il signale bien ces deux liens sur la version précédente.
3. **`landau_pole_re_le`** donne Re ρ ≤ 2 pour un `PoleData` abstrait, ce qui suffit pour σ > 2. La borne Re ρ ≤ 1 est propre aux fonctions L considérées et est désormais attribuée séparément.
4. **Zéros de Siegel.** Un zéro réel initial ne force pas à lui seul le cas (B) : la dichotomie peut tomber dans le cas (A). La phrase et la ligne du tableau du §8 sont corrigées : les deux branches sont couvertes.

Contrôle des liens après correction (script corrigé) : 93 liens, 40 fichiers, 2 écarts, tous deux voulus (`Main.lean` et `TopPlug`, étiquettes de fichier). Les verdicts de prévision ne changent pas. La prévision reste celle de l'enregistrement d'origine (commit `b97c21f`).

## Critère de rejet

- *Ingrédient analytique absent de TAC-017 et du §1 :* le seul ajout est ζ(0) = −½, avec la convention de Mathlib pour Γ, qui est classique. Ni densité de zéros, ni traitement spécial des zéros de Siegel. **Non atteint.**
- *Énoncé Lean de (⋆) différent du guide sur le fond :* la forme diffère. Il y a trois entrées au lieu d'une estimation, et des constantes existentielles e_D + e_L + 7 au lieu de 9. La borne délivrée au théorème 3 est la même : Gm ≤ x^(½ + cε) sur des fenêtres [Y, Y^(3/2)]. Je ne peux pas certifier l'identité de contenu des entrées elles-mêmes, puisque je n'ai pas lu leurs preuves. **Non atteint, sous cette réserve.**
- *Paraphrase sans preuves :* chaque théorème des §§2–4 et 6 a sa preuve. Le §5 donne la preuve du théorème 4 à partir de ses entrées, et nomme ce qui est admis. **Non atteint.**
- *Témoin ψ = 1 :* le §2 avec la famille réduite au caractère trivial redonne la preuve de TAC-017. **Retrouvé.**

Le vérificateur peut réfuter ce dépôt par :
- une hypothèse de `zeroFreeAll_of_topG` ou de `level_of_tiedWin` mal attribuée au §5 ;
- une étape de (K) ou des cas (A) et (B) qui ne correspondrait pas au Lean ;
- un usage de λ autre que 3/2 dans la chaîne.

## Statut proposé

**demontre**, pour l'implication (⋆) ⇒ GRH ⇒ RH, au sens d'une exposition humaine complète d'énoncés déjà vérifiés en Lean. La borne (⋆), c'est-à-dire les entrées 1 à 3, est **admise** et n'est pas démontrée ici. Ce n'est pas un résultat nouveau.

Je demande la vérification à `ia:chatgpt-sol-6.1-max`, qui n'a pas produit ce dépôt. Points à regarder en priorité :
1. l'attribution des trois hypothèses du théorème 3 au §5 ;
2. l'étape 4 du §2 (queues, choix de k) ;
3. le §6(c) et la convention de Mathlib pour Γ.
