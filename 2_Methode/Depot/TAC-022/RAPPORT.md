# TAC-022 (reprise de TAC-018) — Théorème A par fenêtres : le Landau localisé pour la Loupe double

*Producteur : ia:claude · 23 novembre 2026 · branche `tac-022`. Auteur et titulaire des droits : Vincent NOËL. Fil : [#54](https://github.com/vppnoel/Riemann/issues/54) (historique : [#44](https://github.com/vppnoel/Riemann/issues/44)).*

**En une phrase.** Le Landau localisé de la preuve annoncée s'étend à la statistique de l'article 1, qui a des pôles doubles. Mais le côté utile s'inverse : pour la Loupe double, c'est un **plancher** qui suffit, pas un plafond, parce que le coefficient d'un pôle double réel est négatif. On en tire une version par fenêtres du théorème A. L'apport est **modeste** : c'est une remarque pour l'article 1, pas un nouvel article.

## Prévision

Enregistrée pour TAC-018 le 23 novembre 2026 à 1 h 39 UTC (commit `76446af` sur `main`), avant toute rédaction et tout calcul. **Recopiée après coup pour TAC-022**, avec mention explicite : sa valeur de prévision vient uniquement de l'enregistrement d'origine. La prévision signale elle-même que le signe avait été examiné de tête avant de l'écrire. En résumé :
- **P1** : c₂ = m(m + 1)/(ρ(ρ − 1)) est négatif pour ρ réel, donc un plancher suffit, et un plafond n'exclut que les zéros non réels ; pour ζ, les deux côtés suffisent.
- **P2** : la preuve de TAC-017 s'étend avec deux changements.
- **P3** : la réciproque |H| ≪ y^θ log y, et la caractérisation de Θ.
- **P4** : G_c(1) = 2γ² + 6γ₁ ≈ 0,2295 centre H, et max |H|/(√y log y) est entre 0,03 et 0,15 sur [10, 10⁶], sans dérive.
- **P5** : l'apport est une adaptation modeste ; l'énoncé n'est probablement pas dans la littérature tel quel, sans que je puisse l'exclure.

## Méthode

- **Preuve** (`PREUVE.md`) : six étapes, calquées sur TAC-017, chaque différence étant marquée. Il n'y a pas de code Lean pour les pôles doubles : la preuve n'est vérifiée par aucune machine.
- **Calcul** (`tac018_numerique.py`, environ 1,5 s, sans dépendance). On calcule c(n) jusqu'à 10⁶ par convolution exacte sur les puissances de premiers, puis H(y). H est affine sur chaque [n, n + 1), donc son maximum s'obtient aux bords. Sommes compensées. Sortie : `resultat_numerique.txt`.
- **Littérature** : une recherche rapide sur les résultats de signe et les versions locales pour ψ(x) − x, détaillée sous Portée.

## Résultat

| | Prévision | Résultat | Verdict |
|---|---|---|---|
| **P1** | c₂ < 0 pour ρ réel ; plancher suffisant, plafond insuffisant pour les zéros réels ; pour ζ, les deux | démontré (étape 1c, cas 1 de l'étape 5) ; témoin h(u) = −u e^(βu) : plafond vérifié malgré un pôle réel | **juste** |
| **P2** | deux changements | deux changements (\|h\| = 2h⁻ + h ; développement près d'un pôle double), plus le terme c₁ à absorber, sans difficulté | **juste** |
| **P3** | \|H\| ≪ y^θ log y, et la caractérisation de Θ | **caractérisation démontrée**, via \|H\| ≪_ε y^(θ+ε) modulo une borne classique citée ; la forme y^θ log y **n'est pas démontrée** (convergence de Σ\|c₁(ρ)\|) | **juste pour la caractérisation, non démontrée sous la forme prévue** |
| **P4** | G_c(1) ≈ 0,2295 ; max entre 0,03 et 0,15 ; pas de dérive | G_c(1) = 0,229461 ; max **0,0938** (en y = 10) ; entre 0,017 et 0,041 sur les décades 10² à 10⁶ ; H(y)/y de l'ordre de 10⁻⁴ en 10⁵ et 10⁶, donc pas de dérive linéaire | **juste** |
| **P5** | apport modeste, énoncé sans doute inédit tel quel | voir Portée | **juste**, avec une nuance |

**Une coïncidence à noter.** Dans la décade 10⁵, le maximum de |H|/(√y log y) est atteint en y ≈ 319 477. C'est presque le même point que le maximum de la statistique d'Alpöge en TAC-017 (y ≈ 319 439). Les deux statistiques voient sans doute la même irrégularité locale des nombres premiers. Ce n'est pas étudié ici.

## Portée

1. **Ce qui est démontré.** Le théorème A′ (i), (ii) et le corollaire, modulo la borne classique de l'étape 6 pour la réciproque. Par exemple : RH équivaut à « H(y) ≥ −y^(½+ε) sur des fenêtres arbitrairement tardives, pour tout ε ».

2. **Ce qu'il apporte par rapport au théorème A.**

   | | Théorème A | Théorème A′ |
   |---|---|---|
   | statistique | Q, une **moyenne quadratique** | H, une **statistique ponctuelle** |
   | portée | **globale** (limsup) | des **fenêtres** clairsemées suffisent |
   | côtés | les deux | **un seul** |

   A′ est donc plus économe en hypothèses : pour exclure les zéros à droite de θ, il suffit de vérifier un plancher sur des fenêtres. Il ne remplace pas A, qui donne en plus la croissance exacte de Q, et sur lequel reposent le théorème B et le critère de simplicité.

3. **Le changement de côté**, la seule remarque peut-être nouvelle. Pour les pôles simples (Alpöge, TAC-017), c'est un plafond qui sert ; pour la Loupe double, c'est un plancher. La raison est un signe : m(m + 1) au lieu de −m.
   - Pour ζ seule, cela ne change rien, puisqu'elle n'a pas de zéro réel dans ]0, 1[.
   - Pour une famille de fonctions L, où un zéro réel (« zéro de Siegel ») ne peut pas être exclu d'avance, le bon côté deviendrait essentiel. C'est une **hypothèse de travail**, non étudiée.

4. **Ce qui n'est pas nouveau.**
   - Les résultats de signe **globaux** pour ψ(x) − x, de la forme Ω± (x^(Θ−ε)), viennent du théorème de Landau. Ils sont classiques (Landau, 1905 ; exposés par exemple dans Montgomery–Vaughan, ch. 15, référence **à vérifier sur l'original**).
   - Les versions **par fenêtres** existent pour |ψ(x) − x|, des deux côtés à la fois. Par la méthode des sommes de puissances de Turán, Pintz a montré qu'il existe un x dans [X^(1/4), X] avec |Δ(x)| > c x^(σ₀)/γ₀^50 ; Schlage-Puchta ([arXiv:1912.00853](https://arxiv.org/abs/1912.00853)) l'a resserré à [X, X^(1+ε)]. Ces énoncés sont lus dans l'introduction de ce dernier article, non sur les originaux de Turán et de Pintz.

   Ce que A′ ajoute : la version **d'un seul côté**, à la façon d'Alpöge, pour la statistique à **pôles doubles** de l'article 1, avec le changement de côté. Je n'ai pas trouvé cet énoncé tel quel, sans pouvoir l'exclure.

5. **Importance, honnêtement.** C'est une **remarque** pour l'article 1, sous la forme d'une section « version locale du théorème A ». Ce n'est pas un résultat à publier seul. Si la preuve d'Alpöge tient, Θ = ½ est connu, et A′ se lit comme une propriété de la statistique H, plus comme un critère. Son intérêt est surtout de **montrer que la statistique du corpus entre dans la machine de la preuve annoncée**, avec une différence de signe compréhensible.

## Reprise

**Provenance.** Ce dossier reprend celui de TAC-018. TAC-018 a été retirée avant vérification parce que son étape 5 renvoyait à l'étape 5 de TAC-017, dont la transition géométrique était fausse ([#40](https://github.com/vppnoel/Riemann/issues/40), §2). Elle est ensuite devenue périmée quand la reprise de TAC-017 a modifié son entrée.

**Correction.** L'étape 5 de `PREUVE.md` est réécrite. Elle suit maintenant la dichotomie exacte du Lean, qui est purement géométrique et vaut donc pour les pôles doubles. Le cas B (pôle réel) et le cas A (pôle non réel, centre déplacé) sont détaillés, avec le choix des rayons et de η. La conclusion (ii) est reformulée en conséquence.

Le reste (étapes 1 à 4 et 6, calcul, littérature) est inchangé. Le calcul n'a pas été relancé : il ne dépend pas de l'étape 5.

## Critère de rejet

Le critère de la fiche portait sur trois points :
- un coefficient dominant sans signe fixe : **non**, son signe est fixé, et négatif pour ρ réel ;
- une dérive linéaire de H : **non** ;
- un énoncé déjà dans la littérature sous cette forme : **pas trouvé**, mais des énoncés voisins existent (point 4).

**Il n'est pas atteint.** Le vérificateur peut réfuter ce rapport par :
- une erreur de signe dans c₂ ;
- une erreur dans le cas B de l'étape 5 (le passage de |a| − a à −a) ou dans la dichotomie géométrique ;
- un défaut dans la borne citée à l'étape 6 ;
- une référence où l'énoncé figure déjà.

## Statut proposé

**demontre**, pour le théorème A′ (i), (ii) et le corollaire, modulo la borne classique citée à l'étape 6, qui est à vérifier sur Titchmarsh. Il n'y a pas de vérification par machine. Je demande la vérification à `ia:chatgpt-sol-6.1-max`. Points à regarder en priorité :
1. le signe de c₂, la dichotomie géométrique et le cas B ;
2. l'étape 6 et sa référence ;
3. la valeur G_c(1) = 2γ² + 6γ₁.
