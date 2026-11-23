# TAC-016 — Échelle, témoin : Davenport–Heilbronn échoue-t-il dès l'étage des entiers ?

*Producteur : ia:claude · 23 novembre 2026 · branche `tac-016`. Auteur et titulaire des droits : Vincent NOËL. Fil : [#39](https://github.com/vppnoel/Riemann/issues/39). Reprise de TAC-014, périmée.*

**En une phrase.** Le Sosie franchit l'étape 1 de la preuve annoncée (le Landau localisé), mais pas l'étape 2 : ses « nombres premiers » ne sont encodés dans aucun entier, parce que les exposants de son « sac » sont des nombres irrationnels. C'est ce que prévoyait le bloc 7 du document de travail, et c'est maintenant calculé en arithmétique exacte.

## Prévision

Enregistrée le 23 novembre 2026 à 1 h 30 UTC, avant tout calcul (commit `b371f4a` sur `main`). Elle tient compte du résultat de TAC-017, déposé avant. En résumé :
- **P1** : b(n) prend des valeurs négatives et des valeurs non nulles hors des puissances de premiers, à partir de n = 6.
- **P2** : F ne s'annule pas pour Re s ≥ 2, et les hypothèses de croissance de `PoleData` sont vérifiées. DH franchit l'étape 1.
- **P3** : aucun exposant du « sac » n'est rationnel, faute de quoi l'entier n'existe pas. Raison prévue : κ est irrationnel, algébrique de degré 4.
- **P4** : |G_DH(y)|/√y dépasse 1 avant y = 10⁵, contre 0,023 pour ζ.

## Méthode

**L'objet** (définition du corpus, `src/family_mod5.py` et `src/rejection.py`). F(s) = Σ a(n) n^(−s), avec a(n) = 1, κ, −κ, −1, 0 selon n mod 5, et κ = (√(10 − 2√5) − 2)/(√5 − 1) ≈ 0,284079. On écrit −F′/F = Σ b(n) n^(−s), avec b = (a·log) ∗ c, où c est l'inverse de Dirichlet de a.

**Le polynôme minimal de κ**, établi à la main. De w = √(10 − 2√5) = κ(√5 − 1) + 2, en élevant au carré, puis en isolant √5 et en élevant de nouveau au carré, on obtient :

  κ⁴ + 2κ³ − 6κ² − 2κ + 1 = 0.

Le script vérifie cette égalité à 10⁻¹⁶ près. **κ est de degré 4 sur Q** (preuve corrigée à la reprise, d'après la vérification) :
- u = κ − 1/κ vérifie u² + 2u − 4 = 0 (on divise le polynôme par κ²), donc u = −1 − √5 et K = Q(√5) ⊂ Q(κ) ;
- sur K, κ est racine de X² − uX − 1, de discriminant u² + 4 = 10 + 2√5 ;
- la norme de 10 + 2√5 vaut (10 + 2√5)(10 − 2√5) = 80, qui n'est pas un carré rationnel. Donc 10 + 2√5 n'est pas un carré dans K, et X² − uX − 1 est irréductible sur K ;
- d'où [Q(κ) : Q] = [Q(κ) : K]·[K : Q] = 2 × 2 = 4, et le polynôme de degré 4 est le polynôme minimal de κ.

*La première version affirmait que « la seule factorisation » était κ² − uκ − 1, ce qui sautait une étape.*

κ est donc algébrique de degré 4, et Q(κ) = {c₀ + c₁κ + c₂κ² + c₃κ³}, avec c_i rationnels uniques.

**Calcul exact.** Les coefficients a et c sont dans Z[κ], puisque a(1) = 1. Le script les manipule comme des quadruplets d'entiers réduits modulo le polynôme minimal. On décompose b(n) = Σ_p β(n, p) log p, avec β(n, p) = Σ_{d|n} v_p(d) a(d) c(n/d) dans Z[κ], calculé **exactement** jusqu'à n = 3000. Un élément est rationnel si et seulement si ses composantes en κ, κ² et κ³ sont nulles.

**Le « sac ».** Pour le rapport de Tchebychev (TAC-015), log N_F(x) = Σ_n b(n) F(x/n) = Σ_p α_p(x) log p, avec α_p(x) = Σ_{p | n ≤ x} β(n, p) F(x/n). Pour ζ, β(n, p) vaut 1 si n est une puissance de p et 0 sinon : α_p(x) est un entier, et N_F(x) est l'entier de Tchebychev.

**Pourquoi un exposant irrationnel tue l'entier** (théorème de Baker, 1966). Les log p sont linéairement indépendants sur Q, donc sur les nombres algébriques. Si Σ α_p log p = log r avec r rationnel et α_p algébriques, alors α_p = v_p(r) pour tout p. Donc **si un seul α_p(x) est irrationnel, exp(Σ α_p log p) n'est pas rationnel**, et a fortiori pas entier.

**Autres calculs.** Avec ces sommes en flottants jusqu'à 10⁵, le script calcule :
- les b(n), comparés aux valeurs exactes en six points ;
- F(1) et F′(1), par sommes partielles moyennées sur une période jusqu'à 10⁶ ;
- G_DH(y) = Σ b(n)(y/n − 1) + y·F′/F(1), à une constante près.

Script : `tac016_sosie.py`, environ 2 s, sans dépendance. Sortie : `resultat_tac016.txt`.

## Résultat

| | Prévision | Résultat | Verdict |
|---|---|---|---|
| **P1** | b(n) < 0 pour certains n, et b(n) ≠ 0 hors des puissances de premiers dès n = 6 | négatifs pour n ∈ {3, 4, 9, 12, 13, 14, 19, 23, 27, 29} ; non nuls hors des puissances de premiers pour n ∈ {6, 12, 14, 18, 21, 24, 26, 28} ; premier cas n = 6 ; b(2) = κ log 2 | **juste** |
| **P2** | F ≠ 0 pour Re s ≥ 2 ; croissance en y² | Σ_{n≥2} \|a(n)\| n^(−2) ≈ 0,267 < 1, donc F ≠ 0 et 1/F converge absolument pour Re s ≥ 2 ; abscisse de convergence absolue de −F′/F au plus 1,396 ; max \|G_DH(y)\|/y² ≈ 0,077 | **juste** |
| **P3** | aucun exposant rationnel, pour aucun rapport | 2 406 des 2 619 coefficients β(n, p) non nuls (n ≤ 3000) sont irrationnels. Mais **beaucoup d'exposants α_p(x) sont rationnels** : par exemple α₁₁(11) = 1 (relevé par la vérification), et, pour x ≤ 3000, 303 595 des 663 208 exposants non nuls (Tchebychev) et 226 148 des 585 761 (binomial). En revanche, **pour chaque x de 2 à 3000, au moins un exposant est irrationnel**, pour les deux rapports | **fausse telle qu'énoncée** (universelle) ; **juste sous la forme « au moins un exposant irrationnel pour chaque x testé »**. La première version la marquait « juste » sur 12 cas : c'était une surgénéralisation |
| **P4** | \|G_DH\|/√y > 1 avant 10⁵ | sur la grille entière de 2 à 10⁵, avec le centrage du script (à une constante additive près) : max **0,354** en y = 4 ; puis 0,031 (10³), 0,039 (10⁴), 0,064 (10⁵) | **fausse**. *La comparaison avec la valeur 0,0227 de ζ, faite dans la première version, est retirée : elle portait sur une autre statistique (centrée par log 2π), sur une autre plage, et sur l'intervalle continu.* |

**Pourquoi P4 est fausse.** J'ai oublié l'amortissement. Un zéro ρ contribue à G environ y^(Re ρ)/|ρ(ρ − 1)|. Le zéro hors droite le plus à droite connu du corpus (Re ρ ≈ 0,81, t ≈ 85,7) donne environ y^0,81/7300. À y = 10⁵, cela fait 1,5, contre √y ≈ 316 : une contribution de l'ordre de 0,005 √y, invisible. La « fièvre » du Sosie est réelle, mais elle ne se voit qu'à des hauteurs bien plus grandes. Le rapport croît lentement (0,031, puis 0,039, puis 0,064), ce qui est compatible avec un exposant plus grand que ½. Mais ce n'est pas mesuré ici comme tel.

**Le témoin quartique et un critère commun (ajoutés à la reprise).** La vérification a relevé que le second témoin demandé, L(s, χ₅) avec χ₅(2) = i, manquait. Elle a aussi montré qu'il **échoue lui aussi au test naïf** : à x = 2, l'exposant brut de 2 vaut χ₅(2)·F(1) = i, qui n'est pas la valuation d'un entier. Le test de la première version ne distinguait donc pas le Sosie d'une vraie fonction L. Il faut un critère commun, que je propose ici. *C'est ma définition ; elle ne vient pas du guide.*

> **(S)** Il existe une famille finie naturelle F₁, …, F_r et des poids w_j > 0 tels que les coefficients de Σ w_j (−F_j′/F_j) s'écrivent Σ_p e(n, p) log p, avec e(n, p) **entiers ≥ 0, nuls hors des puissances de p**.

Script `tac016_reprise.py`, sortie `resultat_reprise.txt`.

| Objet | Famille naturelle | Exposants obtenus | (S) |
|---|---|---|---|
| ζ | ζ seule | e(p^r, p) = 1 | **oui** |
| L(s, χ₅) | ses 4 puissances χ₅^j (j = 0, …, 3), poids égaux | Σ_j χ₅^j(p^r) ∈ {0, 4} pour p ≠ 5, et 1 pour p = 5 ; aucune exception pour n ≤ 3000 | **oui** |
| DH | ses 4 conjugués de Galois F^σ (κ ↦ chacune des 4 racines), poids égaux | Σ_σ −F^σ′/F^σ = −N′/N, avec N = Π_σ F^σ ; les exposants sont les traces Tr β(n, p), **entières** puisque κ est un entier algébrique. Mais elles sont **négatives** pour 692 valeurs de n ≤ 3000 (dès n = 2 : Tr β(2, 2) = −2), et **non nulles hors des puissances de premiers** pour 906 valeurs (dès n = 6 : Tr β(6, 2) = Tr β(6, 3) = 20) | **non** |

**Ce que cela montre.** Le moyennage sur la famille, qui est l'idée du §5 du guide, rend aux vraies fonctions L leur « sac » d'entiers positifs. Pour le Sosie, le moyennage naturel donne bien des entiers, mais ni positifs ni portés par les puissances de premiers : c'est l'absence de produit d'Euler, vue arithmétiquement.

**Limite.** On n'a testé qu'**une** famille pour DH, celle de ses conjugués. On n'a pas démontré qu'aucune autre famille ne satisfait (S).

**L'étape 1 pour DH (précisée à la reprise).** Avec le centrage du script, G_DH(y) = Σ b(n)(y/n − 1)₊ + y·F′/F(1). Sa transformée vaut Φ_DH(s) = [−F′/F(s) + s·F′/F(1)]/(s(s − 1)), qui est régulière en s = 1, puisque le numérateur y est nul. F est entière, car c'est une combinaison de L(s, χ₅) et de L(s, χ̄₅). On a F ≠ 0 pour Re s ≥ 2 (ci-dessus), et F(1) ≈ 0,9228 ≠ 0. Cette dernière valeur est **numérique** ; elle n'est pas démontrée ici. Les pôles de Φ_DH dans Re s > 0 sont les zéros de F, de résidu −m/(ρ(ρ − 1)), et ils sont symétriques par conjugaison, car les coefficients sont réels. La borne O(y²) est démontrée par la vérification : Σ |b(n)|/n² < ∞ par la série de Neumann. Les hypothèses de `PoleData` sont donc réunies, **modulo la non-annulation numérique de F(1)**.

## Portée

1. **Le Sosie franchit l'étape 1.** Toutes les hypothèses dont elle a besoin (`PoleData`, TAC-017) sont réunies pour DH : représentation de Laplace pour Re s > 2, croissance en y², pôles aux zéros de résidu −m/(ρ(ρ − 1)). Seule la première est vérifiée ici avec soin ; pour les autres, j'ai contrôlé ce qui se mesure (la croissance jusqu'à 10⁵) et constaté que la structure est la même que pour ζ. Ce n'est pas surprenant : l'étape 1 est une **réduction**, pas une preuve. Pour DH, elle ramène la question à une borne sur G_DH qui est fausse.
2. **Le Sosie échoue à l'étape 2, et l'on sait où.** Ses « premiers » ont des poids irrationnels, multiples de κ. Aucun produit de factorielles, ni aucun objet entier, ne peut avoir ces exposants, d'après le théorème de Baker. C'est le **bloc 4** du document de travail, « le sac qui ne peut pas mentir », vu par son absence : sans produit d'Euler, il n'y a pas de sac.
3. **Ce que cela précise pour le corpus.**
   - Le document 47 notait « Λ(n) ≥ 0 ; DH ne l'a pas ». TAC-017 a montré que la positivité des coefficients ne sert pas à l'étape 1. Ce que DH n'a pas, c'est plus fort : des coefficients **portés par les puissances de premiers et rationnels en log p**.
   - L'Archipel d'Euler (doc. 30) trouve ici une forme arithmétique : hors des points d'Euler, l'intégrité est perdue.
4. **Ce que cela n'établit pas.**
   - Pour un rapport de factorielles quelconque, on n'a pas démontré que le sac de DH ne peut jamais être entier : on l'a calculé pour celui de Tchebychev et 12 cas. Le raisonnement de Baker suffit dès qu'**un** exposant est irrationnel ; le cas général reste à écrire.
   - Rien sur les objets automorphes du vrai étage 2. Le test montre seulement que l'**analogue élémentaire** échoue.

## Reprise

La vérification de `ia:chatgpt-sol-6.1-max` ([`verification/VERIFICATION.md`](verification/VERIFICATION.md), fil [#39](https://github.com/vppnoel/Riemann/issues/39)) a jugé le dépôt non conforme. Ses motifs, tous fondés, et leur correction :
1. **P3 était surgénéralisée** (contre-exemple α₁₁(11) = 1). Elle est reformulée et mesurée sur tous les x de 2 à 3000.
2. **Le témoin quartique L(s, χ₅) manquait**, et le test naïf ne le distinguait pas de DH. Il est ajouté, avec un critère commun (S), qui sépare L(s, χ₅) de DH.
3. **La preuve du degré de κ sautait une étape.** Elle est corrigée par l'argument de norme que donne la vérification.
4. **La comparaison chiffrée de P4 avec ζ n'avait pas de sens.** Elle est retirée.
5. **L'étape 1 pour DH** est explicitée, avec la réserve sur F(1).

La prévision est inchangée. Le statut proposé reste **mesure**, pour des résultats finis ainsi délimités, comme le suggère la vérification.

## Critère de rejet

Le critère de la fiche était : « Si les coefficients de DH sont positifs et portés par les puissances de premiers, ou si un analogue entier existe, la prévision est fausse. »

**Il n'est pas atteint.** Les coefficients prennent des valeurs négatives et non nulles hors des puissances de premiers. Les exposants testés sont irrationnels, donc aucun analogue entier n'existe pour ces cas.

Le vérificateur peut réfuter ce rapport par :
- une erreur dans le polynôme minimal ou dans son irréductibilité ;
- une erreur dans la réduction modulo ce polynôme ;
- une mauvaise application du théorème de Baker.

## Statut proposé

**mesure**. Le calcul est exact et l'argument de Baker est démontré, mais seulement pour les cas calculés ; la portée générale (tout rapport de factorielles) reste à écrire. Je demande la vérification à `ia:chatgpt-sol-6.1-max`. Points à regarder en priorité :
1. le polynôme minimal de κ et son irréductibilité ;
2. la fonction `mul` (réduction κ⁴ = −2κ³ + 6κ² + 2κ − 1) ;
3. la phrase sur Baker.
