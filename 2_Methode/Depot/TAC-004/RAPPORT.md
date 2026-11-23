# TAC-004 — Deux filtres : approximants et norme de forme

*Producteur : ia:claude · 18 octobre 2026 · branche `tac-004` · Programme Riemann V6.59. Auteur et titulaire des droits : Vincent NOËL. Fil : [#11](https://github.com/Vppnoel/riemann/issues/11).*

**En une phrase.** La couverture qualitative du lemme F (doc. 76) devient une **décomposition exacte et linéaire** f = B₂g₂ + B₃g₃ de tout test polaire. Le budget de support est fixe, sans passage à la limite. Elle repose sur deux théorèmes classiques : Hörmander pour les générateurs, Baker pour les formes linéaires en logarithmes. Mais **son coût est réglé par les quasi-collisions 3ᵏ ≈ 2ˡ** (les « commas ») : toute décomposition paie au moins 1/‖k·log 3/log 2‖ près de la fréquence 2πk/log 2. L'application f ↦ g₃ ne peut donc être bornée de H^m dans ν que si m ≥ μ(θ) − 1, où μ(θ) est l'exposant d'irrationalité de log 3/log 2. Une borne ν(g₃) ≤ C ν(f) exigerait que log 3/log 2 soit mal approchable, ce qui n'est pas connu. Le contrat d'erreur de forme est explicite, uniforme en support, avec C_W ≈ 24,55. **Le signe de Q_W n'est pas touché.**

## Prévision

Elle a été enregistrée avant tout calcul, le 18 octobre 2026 vers 0 h 30 UTC (`taches.py prevoir`, commit `3c4c223` sur `main`). Texte intégral dans `taches.json`. En résumé :

- **P1.** Une décomposition exacte f = B₂g₂ + B₃g₃ avec gₚ = φₚ ∗ P⁻¹f, pour une paire universelle de distributions à support compact (Bézout dans l'algèbre de Paley–Wiener–Schwartz).
- **P2.** Un budget de support ch supp f + [−log 3, log 3].
- **P3.** L'ingrédient arithmétique est une minoration polynomiale de ‖k·log 3/log 2‖ (Baker). Les commas 3¹² ≈ 2¹⁹ et 3⁵³ ≈ 2⁸⁴ fixent l'ordre des distributions.
- **P4.** Un algorithme par moindres carrés en norme ν, avec le contrat |Q_W(f) − Q_W(f_h)| ≤ C_W ν(f − f_h)(ν(f) + ν(f_h)).
- **Ce qui donnerait tort :**
  - pas de minoration polynomiale de |b₂| + |b₃| ;
  - des approximants convergents en L² seulement, ou à support croissant ;
  - des témoins non détectés : la paire (2,4), le filtre seul et une cible à moments non nuls doivent stagner, et le schéma de Neumann doit converger en L² et diverger en ν.

## Méthode

**Conventions** (doc. 76) :
- Uₐg(x) = g(x − a) ;
- G(s) = ∫ g(x) eˢˣ dx ;
- ℓ±(f) = F(±½) ;
- P = ∂² − ¼, de symbole s² − ¼ ;
- Bₚ = (1 + 1/p) − p^{−1/2}(U_{log p} + U_{−log p}), de symbole bₚ(s) = (1 − p^{s−½})(1 − p^{−s−½}) ;
- ν(u)² = ∫ e^{2|x|}(|u|² + |u′|²) dx.

**Démonstrations (§ 1 à 3 ci-dessous).** Une factorisation Bₚ = P ∘ (rₚ ∗) ramène le problème à une équation de Bézout. On vérifie ensuite la condition de Hörmander à l'aide d'une minoration de Baker. Le coût est minoré aux zéros de b₂, et le contrat de forme se déduit des majorations du lemme F.

**Programmes, sans aucun zéro de ζ :**
- `p1_bezout_diophantien.py` : symboles, noyaux rₚ, fraction continue de θ = log 3/log 2 en précision 120 chiffres, |b₃| aux zéros de b₂, constantes. 19 contrôles.
- `p2_approximants_nu.py` : moindres carrés en ν sur des splines cubiques à boîtes **fixées**, résidu recalculé a posteriori sur une seconde quadrature indépendante, cinq témoins négatifs et contrat de forme mesuré. Voir `p2_resultats.json` : 13 contrôles, 0 échec, 1 non concluant. La première passe, conservée dans `p2_resultats_passe1.json`, est commentée au § 5.4.

Graine 20261018. Les nombres des programmes sont **mesurés** en double précision. Ils ne sont pas certifiés.

## Résultat

### 1. Factorisation : les deux filtres ne sont que P suivi de deux convolutions

**Lemme 1.** Posons, pour |x| ≤ log p, et 0 au-delà :

  rₚ(x) = (2/p) cosh(x/2) − (1 + 1/p) e^{−|x|/2}.

Alors rₚ est continue et nulle en ±log p, et sa transformée est Rₚ(s) = bₚ(s)/(s² − ¼). Donc **Bₚ = P ∘ (rₚ ∗)**.

*Preuve.*
1. La fonction (s² − ¼)⁻¹bₚ est entière : bₚ s'annule en ±½.
2. Elle est de type exponentiel log p, et elle est intégrable sur les droites verticales.
3. Paley–Wiener donne un noyau continu à support [−log p, log p].
4. Le calcul direct par fractions simples donne la formule.

Contrôles A2–A3 : transformée de Laplace par quadrature indépendante, écart ≤ 3·10⁻¹⁶ sur 8 points complexes.

Ainsi, pour f = Pψ avec ψ ∈ C_c^∞ (ce qui équivaut à « f polaire »), f = B₂g₂ + B₃g₃ équivaut, P étant injectif sur les supports compacts, à

  **ψ = r₂ ∗ g₂ + r₃ ∗ g₃.**

Le problème des approximants devient un **problème de déconvolution à deux noyaux**.

### 2. Décomposition exacte (P1 confirmée ; P2 non établie)

**Proposition 2.** Il existe deux distributions à support compact μ₂, μ₃, d'ordre fini, telles que

  r₂ ∗ μ₂ + r₃ ∗ μ₃ = δ.

Par conséquent, pour tout test polaire f ∈ C_c^∞, avec ψ = P⁻¹f :

  **gₚ = μₚ ∗ ψ ∈ C_c^∞,  f = B₂g₂ + B₃g₃ exactement,  supp gₚ ⊂ ch supp f + supp μₚ.**

L'application f ↦ (g₂, g₃) est linéaire et universelle : μₚ ne dépend pas de f. Son budget de support est fixe.

*Preuve.* Il suffit de vérifier la condition de Hörmander [H67] dans l'algèbre des transformées de Fourier–Laplace de ℰ′(ℝ). Il s'agit de

  |R₂(s)| + |R₃(s)| ≥ ε (1 + |s|)^{−N} e^{−H|Re s|}.

Les zéros de bₚ sont ±½ + 2πiℤ/log p.
1. **Loin des deux droites Re s = ±½**, bₚ est minoré par une constante. Pour |Re s| grand, elle croît comme p^{|Re s|−½}.
2. **Aux points ±½**, Rₚ(±½) = ±bₚ′(±½) ≠ 0 (contrôle A4 : zéros simples).
3. **Près de Re s = ½**, écrire w = s − ½ = σ + iy. Le second facteur de bₚ est encadré entre 1 − p^{−1} et 1 + p^{−1}. Et |1 − eᶻ| ≥ c(|Re z| + dist(Im z, 2πℤ)) pour |Re z| ≤ 1. Avec u = y log 2/2π, k l'entier le plus proche, et θ = log 3/log 2 :

     ‖kθ‖ ≤ ‖uθ‖ + θ‖u‖.

   D'où
     |b₂(s)| + |b₃(s)| ≥ c′ ‖kθ‖,  k ≈ |Im s| log 2/2π.

   La droite Re s = −½ se traite de même.
4. Pour le **théorème de Baker** sur les formes linéaires en deux logarithmes de rationnels [BW93] :
   |k log 3 − l log 2| ≥ max(k, l)^{−C}, avec une constante C effective.
   Comme ‖kθ‖ = |k log 3 − l log 2|/log 2, on obtient ‖kθ‖ ≥ c k^{−C}. La minoration est donc polynomiale en |s|. ∎

**Ce que la preuve ne donne pas.**
- **Le support de μₚ n'est pas quantifié.** La prévision P2 (budget [−log 3, log 3]) **n'est pas démontrée**. Les mesures du § 4 la rendent seulement plausible.
- L'ordre de μₚ n'est pas explicité ; il dépend de l'exposant de Baker.

**Témoins de la prémisse diophantienne :**
- **Paire (2,4)** : tout zéro de b₂ annule b₄ (contrôle W1). La condition échoue, et aucune paire (μ₂, μ₄) n'existe.
- **Corps de fonctions** : les filtres de degrés 1 et 2 ont des zéros communs (contrôle W3). La grammaire à deux filtres n'a pas d'analogue direct là-bas.
- Le mécanisme est donc **propre à l'incommensurabilité de log 2 et log 3**. Ce n'est pas un ingrédient qui pourrait porter un signe.

### 3. Le coût est réglé par les commas (P3 confirmée, sous une forme plus précise)

**Proposition 3 (coût minimal).** Soit λ un zéro de b₂ sur Re s = ±½. Pour **toute** écriture f = B₂g₂ + B₃g₃ + e :

  |F(λ)| ≤ √2 · |b₃(λ)| · ν(g₃) + √2 · ν(e).

*Preuve.* Pour Re λ = ±½, |G(λ)| ≤ ∫|g| e^{|x|/2} ≤ √2 ν(g), par Cauchy–Schwarz avec ∫e^{−|x|} = 2. Comme b₂(λ) = 0, il reste F(λ) = b₃(λ)G₃(λ) + E(λ). ∎

On a 4·(2/3)‖kθ‖ ≤ |b₃(λ_k)| ≤ 2π·(4/3)‖kθ‖, pour λ_k = ½ + 2πik/log 2 (contrôle B3). Prenons fₖ = P(ψ cos(yₖx)), avec yₖ = 2πk/log 2. Alors |Fₖ(λₖ)| ≍ yₖ², et ‖fₖ‖_{H^m} ≍ yₖ^{2+m} à support fixe. Les mesures le confirment : de k = 5 à k = 12, |F| croît comme y² et ν(f) comme y³. D'où, pour toute décomposition à erreur ν(e) ≤ ¼|Fₖ(λₖ)| :

  **ν(g₃) ≥ c · yₖ²/‖kθ‖.**

**Corollaire (perte de dérivées).** Si une décomposition, linéaire ou non, vérifie ν(g₃) ≤ C‖f‖_{H^m} sur les tests polaires à support dans [−1, 1], alors ‖kθ‖ ≥ c′k^{−m} pour tout k. Donc m ≥ μ(θ) − 1, où μ(θ) ≥ 2 est l'exposant d'irrationalité.
- **Cas m = 1**, c'est-à-dire ν → ν : il faut ‖kθ‖ ≥ c′/k, autrement dit que θ soit mal approchable (quotients partiels bornés). **Ce n'est ni démontré ni réfuté.** Une borne ν → ν n'est donc pas exclue par cette passe ; elle est seulement suspendue à une question diophantienne ouverte.
- **Ce qui est démontré :** aucune borne H^m → ν avec m < 1, et dans l'autre sens une perte au plus polynomiale (proposition 2, exposant de Baker non explicité).
- **Mesuré**, aux réduites k ≤ 2·10⁶ : k‖kθ‖ descend à 0,042 (k = 665) puis 0,018 (k = 190 537). C'est compatible avec des quotients non bornés (23, 55, …), mais une suite finie ne le prouve pas.

Fraction continue de θ = [1; 1, 1, 2, 2, 3, 1, 5, 2, **23**, 2, 2, 1, 1, **55**, …]. Les grands quotients signalent les commas les plus coûteux :

| k | l | 3ᵏ/2ˡ (cents) | ‖kθ‖ | \|b₃(λₖ)\| | coefficient \|vₖ\| = \|λₖ² − ¼\|/\|b₃(λₖ)\| |
|---|---|---|---|---|---|
| 5 | 8 | −90,2 | 7,5·10⁻² | 0,337 | 6,1·10³ |
| 12 | 19 | 23,5 (pythagoricien) | 2,0·10⁻² | 0,082 | 1,4·10⁵ |
| 53 | 84 | 3,6 (Mercator) | 3,0·10⁻³ | 0,013 | 1,8·10⁷ |
| 665 | 1054 | 0,076 | 6,3·10⁻⁵ | 2,6·10⁻⁴ | 1,4·10¹¹ |
| 190 537 | 301 994 | 1,3·10⁻⁴ | 9,3·10⁻⁸ | 3,9·10⁻⁷ | 7,7·10¹⁸ |

**Contrôles B1–B2.** Les records de ‖kθ‖ pour k ≤ 2·10⁶ sont exactement les dénominateurs des réduites, et ils sont confirmés en précision 120 chiffres.

**Contrôle B4.** Aucun zéro commun n'apparaît sur les deux droites jusqu'à Im s = 4000 : le minimum de |b₂| + |b₃| vaut 3,1·10⁻³ en Im s ≈ 2773,8, qui est le comma k = 306.

### 4. Algorithme d'approximation et contrat d'erreur (P4)

**Contrat de forme (démontré, uniforme en support).** Pour f, g ∈ C_c^∞ :

  |Q_W(f, g)| ≤ C_W ν(f)ν(g),  C_W = ζ(3, ¼)/4 + C₀ + 2 Σ Λ(n) n^{−3/2} ≈ 16,166 + 5,372 + 3,010 = **24,549**.

*Preuve.* Trois majorations, une par terme :
- a(t) ≤ t² Σ 2/b_n³ = (ζ(3, ¼)/4)·t², d'où |ℰ(f, g)| ≤ (ζ(3, ¼)/4)‖f′‖‖g′‖ ;
- |C₀ m(f, g)| ≤ C₀ ν(f)ν(g) ;
- |h_{f,g}(d)| ≤ e^{−|d|}ν(f)ν(g) (lemme F), et Σ_q c_q e^{−log q} = Σ Λ(n) n^{−3/2}.

Constantes contrôlées par deux calculs indépendants (C1–C2) : la dérivée de ζ contre un crible jusqu'à 2·10⁶, et le digamma contre la série de a(t). On en déduit, pour tout approximant f_h :

  **|Q_W(f) − Q_W(f_h)| ≤ C_W · ε(2ν(f) + ε),  ε = ν(f − f_h).**

Le transfert de signe vers f exige ε → 0 **en ν**, à support borné. L'erreur L² seule n'y suffit pas.

**Algorithme mis en œuvre** (`p2_approximants_nu.py`) :
1. Choisir g₂, g₃ dans des splines cubiques de pas h, sur les boîtes fixes ch supp f + [−log 3, log 3] et ch supp f + [−log 2, log 2].
2. Minimiser ν(f − B₂g₂ − B₃g₃) par équations normales régularisées (seuil spectral 10⁻¹³).
3. Recalculer le résidu ε_h a posteriori sur une quadrature différente.

Les moments de f_h sont nuls **algébriquement** : bₚ(±½) = 0.

**Mesures, sur la cible lisse T1 = Pψ avec ψ = exp(−1/(1 − x²)) :**

| h | 1/4 | 1/8 | 1/16 | 1/32 | 1/64 | 1/128 |
|---|---|---|---|---|---|---|
| ε_h/ν(f) | 0,83 | 0,64 | 0,34 | 0,125 | 0,039 | **0,0060** |
| ν(g₂), ν(g₃) | 1,2·10⁴ ; 6,3·10³ | 9,0·10⁴ ; 5,0·10⁴ | 1,6·10⁵ ; 8,8·10⁴ | 4 183 ; 3 416 | 1 184 ; 1 277 | **672 ; 357** |

- La convergence en ν à support fixe est mesurée, avec une pente qui atteint 2,7 au dernier pas.
- Avec des boîtes doublées, l'erreur passe de 0,125 à 0,101 à h = 1/32 : **le résidu ne dépend pas d'un support croissant**.
- Le contrat est vérifié sur T1 à h = 1/128 (contrôle F1) : |Q_W(f) − Q_W(f_h)| = 7,3·10⁻⁵, sous la borne 5,8·10³. La borne est valide mais lâche ; elle est dominée par le poids e^{2|x|} de ν. La valeur Q_W(T1) ≈ 8,95 est une mesure, pas un certificat.

**Cibles oscillantes aux commas** (contrôle N5) :

| k | yₖ = 2πk/log 2 | \|b₃(λₖ)\| | pas h | ε/ν(f) | ν(g₃)/ν(f) mesuré | minorant démontré de ν(g₃) |
|---|---|---|---|---|---|---|
| 5 | 45,3 | 0,337 | 1/128 | 2,9·10⁻³ | 10,6 | 684 (observé 3,6·10⁵) : **vérifié** |
| 12 | 108,8 | 0,082 | 1/256 | 6,0·10⁻² | 48,1 | vide (résidu trop grand) : **non concluant** |

- Les ν(g₃) mesurés dépassent de loin le minorant. Les moindres carrés minimisent le résidu, pas la norme des coefficients, si bien que les rapports mesurés ne doivent pas être lus comme la loi de la proposition 3.
- Au pas 1/512, l'essai k = 12 dépasse la mémoire de l'environnement. Il n'a pas abouti et n'est pas compté.

### 5. Témoins négatifs et contrôles anti-circularité

**5.1 Témoins exigés par la fiche.** Chacun est détecté avec un minorant **démontré**, celui de la proposition 3 ou son analogue en ±½ :

| Témoin | Prévu | Observé |
|---|---|---|
| N1 filtre seul B₂ | résidu ν ≥ max |F(λ)|/√2 = 0,98 aux zéros de b₂ ; stagnation | ε = 116 → 95 → 75 : bloqué, ≥ minorant |
| N2 paire commensurable (2,4) | idem (zéros communs) | ε = 92 → 79 → 75 : bloqué, ≥ minorant |
| N3 cible à moments non nuls (« moments perdus ») | résidu ≥ \|ℓ±(f)\|/√2 = 0,32 | ε = 0,766 → 0,758 → 0,757 : bloqué |
| N4 Neumann à un filtre (« convergence L² seule », « support sans borne ») | L² ∝ 2^{−J/2} → 0, ν ∝ 2^{J/2} → ∞, support ∝ J | rapports successifs 0,707 et 1,414 à 2 % près, pour J = 6 à 12 ; demi-support 8,6 à J = 12 |
| N5 commas | ν(g₃) ≥ (\|F(λₖ)\| − √2ε)/(√2\|b₃(λₖ)\|) | vérifié pour k = 5 ; non concluant pour k = 12 (voir § 4) |

Le schéma de Neumann est la construction naïve : inverser E₂ par sa série. C'est exactement le témoin de la fiche. Il converge en L², mais il diverge en ν et son support croît. Il est donc **refusé par le critère de rejet**.

**5.2 Davenport–Heilbronn.**
- Les propositions 2 et 3 ne font intervenir que des translations : elles valent **mot pour mot** pour la forme de Weil de DH.
- Elles ne peuvent donc **pas** servir seules pour RH, ce qui était prévu.
- Leur rôle est de réduire le problème : RH ⟺ Q_W(B₂g₂ + B₃g₃) ≥ 0 pour tout couple (g₂, g₃), avec une application de couverture **exacte**. Le lemme F ne la donnait que par densité.

**5.3 Corps de fonctions.** Toutes les fréquences y sont commensurables (log q^d) : la grammaire à deux filtres y **échoue** (contrôle W3). L'outil n'importe donc aucune positivité de là-bas.

**5.4 Aucune donnée injectée ; transparence sur les seuils.**
- Aucun zéro de ζ n'est utilisé ; la seule arithmétique est le crible pour Σ Λ(n) n^{−3/2}.
- **La première passe de `p2` a échoué sur trois contrôles.** Le journal est conservé dans `p2_resultats_passe1.json`.
  - E1 : ε_rel = 3,9·10⁻² au pas 1/64, au-dessus du seuil 10⁻³ fixé avant.
  - E2 : moments lus ≈ 2·10⁻⁶ aux pas grossiers. Ce sont des erreurs de quadrature proportionnelles à ν(g) ≈ 10⁵.
  - N4 : seuil L² 10⁻³ trop strict, alors que la décroissance théorique 2^{−J/2} donne 2·10⁻² à J = 12.
- Les seuils ont été **révisés après lecture des résultats** :
  - E1 : un pas de plus et un seuil de 10⁻² ;
  - E2 : critère relatif à ν(g) ;
  - N4 : test des taux théoriques 2^{∓1/2}.

  Ces révisions ne changent aucun énoncé démontré. Le vérificateur doit les juger en connaissant leur ordre.

**5.5 Constantes.** C_W est donné avec ses trois termes. Σ Λ(n) n^{−3/2} = 1,505235 par ζ′/ζ(3/2), contre 1,503821 + queue ≤ 1,5·10⁻³ par le crible. Les valeurs de k‖kθ‖ sont des mesures sur k ≤ 2·10⁶, pas des bornes.

## Portée

**Démontré**, dans le dossier, à partir de résultats classiques rappelés et non redémontrés :
- lemme 1, factorisation exacte, élémentaire ;
- proposition 2, sous [H67] et [BW93] : décomposition exacte et linéaire de tout test polaire C_c^∞ par deux filtres, à budget de support fixe, mais non quantifié ;
- proposition 3, élémentaire : minoration de coût en tout zéro de b₂, et corollaire : perte d'au moins μ(θ) − 1 dérivées. Le cas ν → ν reste suspendu à la mal-approchabilité de log 3/log 2 ;
- contrat |Q_W(f, g)| ≤ C_W ν(f)ν(g), uniforme en support, et son corollaire pour les approximants.

**Mesuré**, sans certificat :
- convergence des moindres carrés en ν à boîtes fixées, sur une cible lisse et deux cibles oscillantes ;
- tailles de ν(gₚ) ;
- valeurs de k‖kθ‖ aux réduites ;
- Q_W(T1) ≈ 8,95.

**Ouvert :**
- support minimal de μₚ (prévision P2) ;
- ordre explicite de μₚ ;
- formule d'interpolation constructive de μₚ : M₃(λ) = 1/R₃(λ) aux zéros de R₂, puis M₂ = (1 − R₃M₃)/R₂. Elle est décrite ici, mais non mise en œuvre ;
- version certifiée par intervalles des mesures du § 4.

**Non obtenu, et non visé :** le signe de Q_W sur la famille, et a fortiori RH.

**Ce que cela change pour la loi de signe (IDE-051).** La forme quadratique Q̃(g₂, g₃) = Q_W(B₂g₂ + B₃g₃) est maintenant **exactement** équivalente au critère de Weil, sans limite. Mais toute estimation de Q̃ en fonction de ν(g₂), ν(g₃) devra tenir compte des commas : près de Im s ≈ 2πk/log 2, avec k une réduite de θ, les coefficients sont forcés d'ordre y²/‖kθ‖ (proposition 3). C'est un renseignement **arithmétique précis** sur le coût de cette grammaire. Ce n'est pas un défaut de méthode.

## Critère de rejet

Écrit avant : « La suite ne converge pas dans la topologie exigée ; le transfert de signe est alors refusé. »

- **Non déclenché pour la décomposition exacte.** La proposition 2 ne demande aucune suite. Le contrat de forme y est sans erreur.
- **Non déclenché pour l'algorithme numérique.** La convergence est mesurée en ν, la topologie qui rend Q_W continue, à support fixe.
- **Déclenché, comme prévu, pour les trois témoins :**
  - Neumann : convergence L² seule et support sans borne ;
  - filtre seul et paire (2,4) : zéros communs ;
  - cible non polaire : moments perdus.

  Le transfert de signe leur est refusé.

## Statut proposé

**partiel.**
- La construction exacte et le contrat d'erreur de forme sont démontrés, sous des théorèmes classiques cités.
- L'obstruction quantitative des commas est démontrée.
- Le budget de support minimal, l'ordre des μₚ et la certification des approximants restent ouverts.

Pas `--equivalent-rh` : la décomposition n'entraîne pas RH. L'équivalence « RH ⟺ Q̃ ≥ 0 » était déjà acquise (doc. 76, lemme F) ; ce travail la rend exacte, il ne l'établit pas.

**Fiches suivantes proposées** (à discuter dans le fil #11) :
1. budget de support minimal de (μ₂, μ₃), par interpolation explicite ;
2. version certifiée par intervalles de l'essai T1 ;
3. lecture de Q̃ près des commas k = 12, 53 et 665 : la dette de Schur y est-elle concentrée ?

## Références

- [H67] L. Hörmander, *Generators for some rings of analytic functions*, Bull. Amer. Math. Soc. 73 (1967), 943–949. <https://www.ams.org/bull/1967-73-06/S0002-9904-1967-11860-3/>. L'énoncé utilisé (générateurs de l'unité dans A_p ⟺ minoration Σ|fⱼ| ≥ ε e^{−Cp}) est rappelé de mémoire ; **à vérifier sur l'original**.
- [BW93] A. Baker, G. Wüstholz, *Logarithmic forms and group varieties*, J. reine angew. Math. 442 (1993) ; exposé dans *Logarithmic Forms and Diophantine Geometry*, Cambridge University Press, 2007, chap. 7. <https://www.cambridge.org/core/books/logarithmic-forms-and-diophantine-geometry/quantitative-theory/23FA26710B76362AB76BBE9FDC3D9958>. Seule la forme qualitative est utilisée : minoration polynomiale pour α₁, α₂ fixés. Aucune valeur d'exposant n'est revendiquée.
- Déconvolution à deux noyaux d'intervalles et condition diophantienne : tradition de C. A. Berenstein, B. A. Taylor et A. Yger. Voir C. A. Berenstein, A. Yger, *Analytic Bezout identities*, Adv. Appl. Math. 10 (1989) 51–74, <https://www.math.u-bordeaux.fr/~ayger/analyticBezout.pdf>. Le cas exact (χ_{[−r₁,r₁]}, χ_{[−r₂,r₂]}, r₁/r₂ non Liouville) n'a **pas été retrouvé** sur un original lors de cette passe ; c'est non trouvé, pas absent.
- W. Zudilin, *An essay on irrationality measures of π and other logarithms*, arXiv:math/0404523 (2004). Mesures dans ℚ log 2 + ℚ log 3, mais pas pour le rapport log 3/log 2 : non utilisé dans les preuves.
- Corpus : doc. 76 (§ 2.4, lemmes E et F), complément 76 (§ 3, § 6, § 10), doc. 67 (pont B3).
