# TAC-008 — Décomposer la cohérence K : diagonale, même premier, premiers distincts

*Producteur : ia:claude · 18 octobre 2026 · branche `tac-008` · Programme Riemann V6.59. Auteur et titulaire des droits : Vincent NOËL.*

**Complément du 18 octobre** (fil #4). À la demande de l'auteur, j'ai retiré le premier dépôt avant toute vérification (`taches.py retirer`, règle de la PR #10) pour y ajouter un témoin négatif. Celui-ci a sa propre prévision, enregistrée avant calcul, et ses fichiers : `temoin_negatif.py`, `temoin_negatif.json`. Le reste du rapport est inchangé.

**Révision du 18 octobre au soir** (vérification de ChatGPT, PR #20, points R1 et R2, fil #4). Je n'ai fait aucun nouveau calcul ; les chiffres sont ceux de `resultats.json` et `temoin_negatif.json`.
- **R1.** J'avais déclaré le critère de rejet « atteint » en m'appuyant sur W1 contre W2. Or le critère porte sur {ζ, L(χ₅)} contre DH. La confrontation directe est maintenant faite plus bas : **le critère n'est pas établi**.
- **R2.** La conclusion était trop générale. Elle est ramenée au canal et au réglage testés, et le statut proposé passe de « obstacle » à **diagnostic**.
- **Précisions.**
  - À T = 10, K_chaîne est très petit (10⁻¹⁵ à 10⁻¹³ de la trace), mais il n'est pas nul.
  - « Plus de 98 % dans K_croisé » ne vaut qu'à T = 1 ; à T = 10 et η = 2, c'est 93,0 %.
  - Un écart réduit entre moyennes et un écart à l'échelle d'un tirage ne sont pas la même chose.

## Prévision

Elle a été enregistrée avant tout calcul, le 17 octobre 2026 vers 22 h 15 UTC (`taches.py prevoir`, commit `46ce861` sur `main`). Les réglages ont été fixés avec elle :

- b_F : coefficients de −F′/F, pour n ≤ 20 000 ;
- fenêtre gaussienne de largeur h = 0,5 en log n ;
- échelles u = 2 à 8, par pas de 0,25 ;
- ψ gaussienne, avec deux résolutions T = 10 et T = 1 ;
- deux témoins à 20 tirages chacun :
  - W1, multiplicatif aléatoire : b(pᵏ) = α_pᵏ log p, avec |α_p| = 1 ;
  - W2, phases brouillées indépendantes : b(pᵏ) = Λ(pᵏ)·e^{iθ_{p,k}}.

Prévisions :

- **P1.** À T = 10, K_chaîne pèse moins de 1 % pour toutes les fonctions, et la séparation entre DH et ζ vient de K_diag et de K_croisé.
- **P2.** À T = 1, K_chaîne pèse entre 1 % et 20 % pour ζ et sépare ζ de W2 à plus de deux écarts-types, mais ne sépare pas W1 de W2.
- **P3.** La part de K_chaîne est plus faible pour L(χ₅) que pour ζ.

**Prévision du témoin** (journal des tâches, 18 octobre, avant calcul). On injecte dans ζ deux sortes de défauts eulériens :
- D_η : b(pᵏ) = Λ(pᵏ)·(1 + η) pour k ≥ 2, avec η = 0,5, 1 et 2 ;
- D_phase : b(p²) = −Λ(p²).

Ce qui était prévu :
- **T1.** À T = 1, le défaut se voit dans K_chaîne au moins dix fois plus que dans K_diag et K_croisé, et cet effet croît avec η.
- **T2.** Pour η = 1, la part relative de K_chaîne bouge d'au moins 20 %.
- **T3.** À T = 10, le défaut est invisible dans K_chaîne, et seul K_diag le voit.

Critère de réfutation : un défaut non localisé dans K_chaîne à T = 1, ou visible dans K_chaîne à T = 10.

## Méthode

Le script est `decomposition_K.py`. Avec ψ(y) = exp(−y²/2), la transformée de Fourier rend la matrice exacte :

K_ij = Σ_{n,m} c_n · conj(c_m) · w_i(n) · w_j(m) · Ψ(log n − log m),  avec Ψ(x) = T√(2π)·exp(−(Tx)²/2) et c_n = b_F(n)/√n.

On sépare trois parts :
- **K_diag** : les termes n = m ;
- **K_chaîne** : n ≠ m, puissances d'un même premier ;
- **K_croisé** : tout le reste, c'est-à-dire des premiers distincts, ou des entiers qui ne sont pas des puissances de premiers (cas de DH).

Les coefficients viennent de `3_Preuves_et_calculs/src/rejection.py` (ζ, L(χ₅) et DH, les mêmes que pour les documents 15 à 18 et le test v614). Indicateurs calculés :
- les parts relatives des normes de Frobenius ;
- le rapport ‖K_chaîne‖/trace(K) ;
- les distances entre les matrices R normalisées, et entre les composantes normalisées par la trace ;
- des écarts réduits (z) par rapport aux tirages des témoins.

La graine des tirages est 20261018. Aucun zéro n'est utilisé.

**Témoin négatif** (`temoin_negatif.py`, environ 90 s). Il importe `decomposition_K.py` sans le modifier et garde les mêmes réglages.

Pour chaque composante X, on mesure d_X = ‖X(défaut) − X(ζ)‖_F / trace K(ζ). La trace est celle de ζ et reste fixe, pour éviter tout effet de normalisation.

## Résultat

Tous les chiffres sont dans `resultats.json`. Parts des normes de Frobenius :

| | T = 10 : diag / chaîne / croisé | T = 1 : diag / chaîne / croisé |
|---|---|---|
| ζ | 0,023 / 0 / 0,977 | 0,003 / 0,00006 / 0,997 |
| L(χ₅) | 0,578 / 0 / 0,422 | 0,501 / 0,0012 / 0,498 |
| DH | 0,525 / 0 / 0,475 | 0,500 / 0,0010 / 0,499 |
| W1, moyenne de 20 | 0,752 / 0 / 0,248 | 0,497 / 0,0036 / 0,499 |
| W2, moyenne de 20 | 0,779 / 0 / 0,221 | 0,516 / 0,0035 / 0,481 |

**Ce qui sépare.**

- **ζ se distingue de toutes les autres fonctions par K_croisé**, qui porte 98 % à 99,7 % de sa norme. Ses coefficients Λ(n) sont tous réels et positifs, si bien que les termes de premiers distincts et voisins (|log p − log q| ≲ 1/T) s'ajoutent tous dans le même sens. Pour L(χ₅) et pour les témoins, les phases se compensent, et K_croisé n'est pas plus grand que K_diag.
- **DH se distingue par l'amplitude** de ses coefficients, qui ne sont pas portés par les seules puissances de premiers et croissent avec n à cause de ses zéros hors de la droite. Cela gonfle K_diag et K_croisé une fois normalisés par la trace : 3,1 fois la trace à T = 10, 137 fois à T = 1.
- **K_chaîne est négligeable partout.**
  - À T = 10, il est très petit (10⁻¹⁵ à 10⁻¹³ de la trace) sans être nul : deux puissances d'un même premier sont distantes d'au moins log 2 en log n, alors que la résolution est de 0,1, et le noyau gaussien les couple à exp(−(10 log 2)²/2) près.
  - À T = 1, il pèse au plus 0,4 %.
  - Les distances entre fonctions dues à K_chaîne sont de 2 à 3 ordres de grandeur sous celles dues à K_diag et à K_croisé.
- **W1 contre W2 à T = 1.** Le produit d'Euler aléatoire et les phases brouillées ont des K_chaîne voisines : l'écart réduit des moyennes vaut z = −0,74 sur 20 tirages, et −0,16 à l'échelle d'un tirage. Cela ne démontre pas que les deux lois sont égales ; c'est seulement qu'aucune différence n'est détectée avec 20 tirages et ce réglage.
- **ζ contre W2 à T = 1** : z = −2,14. ζ a *moins* de K_chaîne relatif que les phases brouillées. C'est un effet de normalisation : la trace de ζ est dominée par sa partie croisée cohérente.
- **À T = 10**, l'écart réduit des moyennes W1/W2 sur K_chaîne vaut 4,5, mais seulement 1,0 à l'échelle d'un tirage, et il porte sur des quantités de l'ordre de 10⁻¹³. Je ne l'interprète pas.

**Témoin négatif** (`temoin_negatif.json`)

| Défaut | T | d_diag | d_chaîne | d_croisé | d_chaîne / max(autres) | part de K_chaîne |
|---|---|---|---|---|---|---|
| η = 0,5 | 1 | 8,5·10⁻⁵ | 5,0·10⁻⁵ | 1,33·10⁻² | 0,0037 | 6,2·10⁻⁵ → 1,24·10⁻⁴ |
| η = 1 | 1 | 2,0·10⁻⁴ | 1,2·10⁻⁴ | 2,68·10⁻² | 0,0044 | 6,2·10⁻⁵ → 2,04·10⁻⁴ (+229 %) |
| η = 2 | 1 | 5,5·10⁻⁴ | 3,0·10⁻⁴ | 5,41·10⁻² | 0,0056 | 6,2·10⁻⁵ → 4,20·10⁻⁴ |
| phase | 1 | 0 | 6,3·10⁻⁵ | 3,58·10⁻² | 0,0018 | 6,2·10⁻⁵ → 2,6·10⁻⁵ (−58 %) |
| η = 0,5 | 10 | 5,0·10⁻⁴ | 6·10⁻¹⁵ | 1,05·10⁻² | 0 (arrondi) | arrondi |
| η = 1 | 10 | 1,2·10⁻³ | 1·10⁻¹⁴ | 2,11·10⁻² | 0 (arrondi) | arrondi |
| η = 2 | 10 | 3,2·10⁻³ | 4·10⁻¹⁴ | 4,24·10⁻² | 0 (arrondi) | arrondi |
| phase | 10 | 0 | 3·10⁻¹⁵ | 2,86·10⁻² | 0 (arrondi) | arrondi |

- **La décomposition détecte chaque défaut injecté**, mais presque entièrement dans K_croisé.
  - À T = 1, c'est 98,5 à 99,8 % de la somme des trois normes de différences, soit 180 à 570 fois plus que dans K_chaîne.
  - À T = 10, c'est 93,0 à 100 %.
  - Les trois composantes ne sont pas orthogonales : ces parts rapportent les normes à leur somme. Ce ne sont pas des parts de variance.
- **Pourquoi.** Une puissance pᵏ a bien plus de voisins proches en log n parmi les autres entiers (premiers q ≠ p) que parmi les autres puissances du même p. Le défaut porté par pᵏ passe donc surtout par les paires (pᵏ, q).
- **Le défaut de phase** ne change pas |b| : il est invisible pour K_diag, et se voit dans K_croisé.

## Portée

- **Ce que dit ce calcul.** C'est une mesure, à deux résolutions, avec un seul choix de fenêtre et d'échelles, et un nombre fini de coefficients (n ≤ 20 000).
- **Ce que voit cette matrice de cohérence au second ordre.**
  - **Le signe des coefficients.** ζ a tous ses coefficients positifs, d'où une cohérence entre premiers distincts.
  - **Le support et la taille des coefficients.** Pour DH, ils ne sont pas portés par les seules puissances de premiers et croissent avec n.
  - **La structure eulérienne, pas avec ce réglage.** La part « même premier » est faible, et avec 20 tirages elle ne distingue pas un produit d'Euler aléatoire de phases brouillées.
- **Conclusion, limitée au canal et au réglage testés** (fenêtres gaussiennes h = 0,5, échelles u de 2 à 8, T = 1 et 10, n ≤ 20 000, 20 tirages).
  - Un défaut eulérien injecté se lit surtout dans K_croisé, pas dans K_chaîne.
  - Le découpage « même premier / premiers distincts » ne fournit donc pas, ici, un indicateur localisé de la structure eulérienne.
- **Ce que ce calcul ne montre pas.** Il ne montre pas qu'une statistique d'ordre deux est aveugle à la multiplicativité.
  - Contre-exemple élémentaire, relevé par le vérificateur : remplacer b(p²) par −b(p²) change K_chaîne pour toute largeur finie.
  - Le document 17 traite un autre objet, un Gram de translations circulaires. Son résultat ne se transporte pas tel quel à ce canal.
  - PRIME-LOCK (document 18) reste un test distinct.
- **Aucune conséquence** sur le signe de Weil ni sur RH : voir les documents 21 à 24, où verrou local et signe global sont indépendants.

## Critère de rejet

| Critère, écrit avant | Observé | Verdict |
|---|---|---|
| K_chaîne ne sépare pas {ζ, L(χ₅)} de DH plus que les témoins, au-delà de deux écarts-types, ou bien toute la séparation vient de K_diag | Voir la confrontation ci-dessous : selon la normalisation, la séparation est très forte ou faible, et je n'ai pas d'incertitude de référence motivée pour la normalisation qui neutralise la trace. | **Non établi** (révision du 18 octobre ; le premier dépôt disait « atteint » à partir de W1/W2, ce qui ne répondait pas au critère). |

**Confrontation directe au critère, à T = 1** (`resultats.json`).

| | ‖K_chaîne‖ / trace K | écart à W2, en écarts-types des tirages W2 | ‖K_croisé‖ / trace K | ‖K_chaîne‖ / ‖K_croisé‖ |
|---|---|---|---|---|
| ζ | 4,9·10⁻⁵ | −2,1 | 0,78 | 6,2·10⁻⁵ |
| L(χ₅) | 0,064 | +33,9 | 25,7 | 2,5·10⁻³ |
| DH | 0,279 | +155,0 | 136,7 | 2,0·10⁻³ |
| W1, moyenne | 0,0035 | — | — | ≈ 7,2·10⁻³ |
| W2, moyenne (écart-type des tirages) | 0,0039 (0,0018) | — | — | ≈ 7,3·10⁻³ |

- **Normalisé par la trace,** K_chaîne sépare fortement L(χ₅) de DH : 121 écarts-types des tirages W2. Ce n'est pas un score gaussien.
- **Mais ce scalaire est dominé par la trace,** qui est petite devant K_croisé pour L(χ₅) (25,7) et pour DH (137) à cause des compensations de phase et de la taille des coefficients.
- **Rapporté à K_croisé,** ce qui neutralise la trace, L(χ₅) et DH sont proches (2,5·10⁻³ et 2,0·10⁻³). Tous deux sont sous les témoins (≈ 7·10⁻³), et ζ est très en dessous à cause de ses coefficients positifs. Je n'ai pas calculé la dispersion des témoins pour ce rapport.
- **Conclusion pour le critère :** il n'est ni atteint ni réfuté. Ce que K_chaîne sépare dépend de la normalisation, et rien n'indique que la séparation observée vienne d'une empreinte eulérienne plutôt que des amplitudes.

**Prévisions :**
- **P1 juste.** K_chaîne est négligeable à T = 10 (moins de 10⁻¹² de la trace), et la séparation entre DH et ζ passe par K_diag et K_croisé.
- **P2 partiellement fausse.**
  - Fausse sur la fourchette : la part de K_chaîne pour ζ est de 0,006 %, et non de 1 % à 20 %.
  - Fausse sur le sens : ζ ne sépare de W2 qu'à |z| = 2,14, et dans le sens opposé, par un effet de normalisation.
  - Juste sur l'essentiel : K_chaîne ne sépare pas W1 de W2.
- **P3 fausse.** La part de K_chaîne de L(χ₅) (0,12 %) dépasse celle de ζ (0,006 %), toujours parce que la trace de ζ est dominée par sa partie croisée.

**Prévisions du témoin :**
- **T1 fausse sur la localisation.** À T = 1, le défaut passe à plus de 98 % par K_croisé et non par K_chaîne : le rapport d_chaîne / max(autres) vaut 0,002 à 0,006, et non plus de 10. Elle est juste sur la croissance avec η.
- **T2 juste.** Pour η = 1, la part de K_chaîne varie de +229 %, mais sur une part de 10⁻⁴.
- **T3 juste pour K_chaîne,** qui reste invisible à T = 10. **Fausse pour « seul K_diag le voit » :** c'est K_croisé qui domine, et K_diag ne voit pas le défaut de phase.
- **Le critère de réfutation est atteint :** à T = 1, le défaut n'est pas localisé dans K_chaîne.

**Ce que cela change.** Avec ce réglage, un défaut porté uniquement par les puissances de premiers ne se lit pas surtout dans la part « même premier » : il se lit surtout dans les couplages avec les premiers voisins. Le découpage « même premier / premiers distincts » n'est donc pas, ici, un indicateur localisé de la structure eulérienne. Ce n'est pas une impossibilité générale (voir la Portée).

## Statut proposé

**diagnostic** (révision du 18 octobre ; le premier dépôt proposait « obstacle »). Ce que le travail apporte :
- une mesure de la décomposition à deux résolutions ;
- une prévision de localisation réfutée par un témoin négatif : le défaut eulérien est vu surtout dans K_croisé ;
- un critère de rejet initial non établi, selon la normalisation.

Ce n'est pas une obstruction générale, et ce résultat n'est pas équivalent à RH.

Ce qui reste ouvert, et ne relève pas de cette fiche :
- une incertitude de référence pour ‖K_chaîne‖/‖K_croisé‖ ;
- d'autres fenêtres ou d'autres échelles ;
- une version à verrou de phase explicite, comme PRIME-LOCK.

**Fichiers :** `decomposition_K.py`, `resultats.json`, `temoin_negatif.py`, `temoin_negatif.json`, ce rapport.
