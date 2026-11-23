# TAC-013 — Échelle, niveau 1 : jusqu'où va l'intégrité sans multiplicité

*Producteur : ia:claude · 23 novembre 2026 · branche `tac-013` · document de travail `1_Presentation/RECOLLER_LES_MORCEAUX_V6_60.md`. Auteur et titulaire des droits : Vincent NOËL. Fil : [#33](https://github.com/vppnoel/Riemann/issues/33).*

**En une phrase.** Pour toute méthode de Tchebychev à rapport de factorielles fixé, le gaspillage est exactement d'ordre x, avec une limite calculable A − 1 + 1/c. L'intégrité sans multiplicité améliore la constante, jamais l'ordre de l'erreur : c'est ce que prévoyait le document de travail.

## Prévision

Enregistrée avant tout calcul, le 23 novembre 2026 à 0 h 49 UTC (`taches.py prevoir`, commit `584a519` sur `main`). Le raisonnement analytique de P1 a été fait **avant** le calcul, et la prévision le dit.

- **P1.** Pour chaque F fixé, W(x)/x tend vers ∫_c^∞ F(y) dy/y² > 0. Limites attendues : 0,193 pour C(2n, n) et 0,088 pour Tchebychev. Écart mesuré inférieur à 0,01 jusqu'à x = 10⁶.
- **P2.** La constante s'améliore (1,386, puis 1,1056), mais W/√x croît sans borne.
- **P3.** Une recherche sur les poids ±1 portés par les diviseurs de 210, avec a₂ = a₃ = a₅ = a₇ = −1 imposés, trouve un F valide avec c > 6 et une constante < 1,1056.
- **P4.** Diamond et Erdős (1980) : des constantes arbitrairement proches de 1, au prix de valeurs de μ jusqu'à un T qui croît, sans erreur o(x) pour un F fixé. À vérifier sur l'original.

## Méthode

**Le cadre (Tchebychev, 1852).** On prend des poids entiers a_k tels que Σ a_k/k = 0, et l'on pose F(y) = Σ a_k ⌊y/k⌋. F est bornée et périodique, de période ppcm(k). Si 0 ≤ F ≤ 1 et F = 1 sur [1, c), alors :
- l'entier N_F(x) = Π ⌊x/k⌋!^(a_k) a pour logarithme log N_F(x) = Σ_n Λ(n) F(x/n) ;
- d'où ψ(x) − ψ(x/c) ≤ log N_F(x) = A x + O(log x), avec A = −Σ a_k log k / k ;
- d'où, en sommant, ψ(x) ≤ (A c/(c − 1)) x + O(log² x).

Le **gaspillage** est la part de log N_F qui ne vient pas des premiers visés :
  W(x) = log N_F(x) − (ψ(x) − ψ(x/c)) = Σ_{n ≤ x/c} Λ(n) F(x/n) ≥ 0.

**Lemme (démontré, en admettant le théorème des nombres premiers).** W(x)/x → ∫_c^∞ F(y) dy/y² = A − 1 + 1/c. Cette limite est strictement positive dès que F n'est pas identiquement nulle sur [c, ∞), ce qui est toujours le cas pour F périodique non nulle.

*Preuve.* D'une part, log N_F(x)/x → A (Stirling). D'autre part, (ψ(x) − ψ(x/c))/x → 1 − 1/c (théorème des nombres premiers). La différence des deux limites est égale à l'intégrale, par sommation de Λ contre F(x/·). ∎

Le lemme n'est qu'une reformulation de la méthode de Tchebychev. Il est donné pour fixer la quantité mesurée, non comme résultat nouveau.

**Calculs.**
- `tac013_niveau1.py` : crible exact de ψ jusqu'à 10⁶ ; W(x) pour C(2n, n) et pour le rapport de Tchebychev ; recherche exhaustive de P3 (177 147 essais). Durée : environ 2 s, sans dépendance. Sortie : `resultat_tac013.txt`.
- `tac013_exploration_apres_coup.py` : recherche **non prévue**, lancée après l'échec de P3. Poids ±1 sur les 15 diviseurs de 210 autres que 1, sans base imposée (14 348 907 essais). Durée : environ 16 s. Sortie : `resultat_exploration_apres_coup.txt`.
- **Source vérifiée sur l'original** : H. G. Diamond, P. Erdős, « On sharp elementary prime number estimates », *L'Enseignement Mathématique* 26 (1980), 313–321, https://www.renyi.hu/~p_erdos/1981-11.pdf (consulté le 23 novembre 2026).

## Résultat

| Rapport | c | A | Constante ψ(x) ≤ K x | Limite W/x | W/x mesuré à 10⁶ | W/√x à 10⁴, 10⁵, 10⁶ |
|---|---|---|---|---|---|---|
| C(2n, n) | 2 | 0,69315 | 1,3863 | 0,1931 | 0,1937 | 19,1 · 60,9 · 193,7 |
| Tchebychev (1, 2, 3, 5, 30) | 6 | 0,92129 | 1,1056 | 0,0880 | 0,0882 | 8,7 · 27,7 · 88,2 |

| | Verdict |
|---|---|
| **P1** | **juste**. Écart à la limite : au plus 0,002 (à 10⁴), et 0,0005 et 0,0003 à 10⁶. La borne ψ(x) − ψ(x/c) ≤ log N_F(x) est vérifiée pour x = 10⁴, 10⁵ et 10⁶. |
| **P2** | **juste**. W/√x est multiplié par √10 ≈ 3,16 à chaque décade, ce qui est la signature d'un gaspillage proportionnel à x. |
| **P3** | **fausse**. Aucun F valide avec la base imposée (0 sur 177 147). L'exploration après coup, sans base imposée, ne trouve qu'**un seul** F valide parmi les 14 348 907 essais : celui de Tchebychev lui-même. |
| **P4** | **juste, avec une nuance**. Le théorème garantit \|π(x)/(x/log x) − 1\| < ε en limite supérieure, à partir des valeurs de μ sur [1, T(ε)). Mais la preuve « utilise des résultats équivalents au théorème des nombres premiers », et les auteurs écrivent que leur méthode « ne conduit pas à une nouvelle preuve » de ce théorème. Leurs constantes numériques (environ 0,924 et 1,085) n'améliorent que modestement celles de Tchebychev. |

## Portée

- **Ce que cela établit pour l'échelle.** Au niveau 1, l'intégrité sans multiplicité ne donne jamais mieux qu'une erreur d'ordre x pour un rapport fixé. Diamond–Erdős montrent que la constante peut approcher 1, mais seulement en laissant croître le rapport, et sans pouvoir conclure sans des résultats équivalents au théorème des nombres premiers. Le §5 du document de travail est confirmé : pour descendre de x à √x, il faut autre chose. Dans la preuve annoncée, c'est la multiplicité.
- **Ce que l'échec de P3 apprend.** Avec des poids ±1 sur les diviseurs de 210, le rapport de Tchebychev de 1852 est la **seule** solution. Les améliorations connues (Sylvester, Diamond–Erdős) exigent des poids plus grands ou des périodes plus longues. Ma prévision a sous-estimé cette rigidité.
- **Ce que cela n'établit pas.** Rien sur RH, ni sur le mécanisme de multiplicité lui-même : c'est l'objet du niveau 2 (Stepanov) et de la lecture du guide. Le lemme admet le théorème des nombres premiers ; c'est sans conséquence ici, puisqu'on mesure une méthode et qu'on ne démontre pas ce théorème.
- **Anti-circularité.** Aucun calcul n'utilise de zéro de ζ, ni RH. Les limites de W/x viennent de Stirling et du théorème des nombres premiers.

## Critère de rejet

Le critère de la fiche était : « Si un rapport de factorielles donnait un gaspillage d'ordre o(n), la lecture du document de travail serait fausse à ce niveau. »

**Il n'est pas atteint.** Les deux rapports mesurés ont un gaspillage proportionnel à x, comme le prédit le lemme, et ce lemme s'applique à tout rapport fixé. Le vérificateur peut réfuter ce rapport de trois façons :
- un F valide avec A − 1 + 1/c = 0 ;
- une erreur dans le lemme ;
- une source montrant qu'un rapport de factorielles fixé donne une erreur o(x).

## Statut proposé

**classique**. Le résultat est une reformulation mesurée de la méthode de Tchebychev et de sa limite connue (Diamond–Erdős) ; il n'a rien de nouveau. Il fixe une marche de l'échelle avec un chiffre vérifiable. Je demande la vérification à `ia:chatgpt-sol-6.1-max`, qui n'a pas produit ce dépôt.

Points à regarder en priorité pour le vérificateur :
1. la preuve du lemme, en particulier l'égalité de l'intégrale avec A − 1 + 1/c ;
2. la recherche de P3, qui a échoué, et l'exploration après coup, clairement séparée ;
3. la lecture de Diamond–Erdős, faite sur une extraction de l'original : vérifier la page du théorème et les deux citations.
