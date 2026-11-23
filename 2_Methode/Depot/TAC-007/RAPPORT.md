# TAC-007 — Certificat du noyau des moments à S = 0,8 : rapport

*Producteur : ia:claude · 17 octobre 2026, repris le 18 octobre · branche `tac-007` · Programme Riemann V6.59. Auteur et titulaire des droits : Vincent NOËL.*

**Reprise du 18 octobre.** La vérification de ChatGPT (`verification/VERIFICATION.md`) a jugé le premier dépôt non conforme, faute de trois contrôles : Davenport–Heilbronn, analogue des corps de fonctions, témoin négatif. Elle ne contredisait ni P1 ni P2. L'auteur a accepté les contrôles proposés dans le fil de discussion (issue #3). Ils sont ajoutés ici sous les repères C0 à C3 : nouvelle prévision, `p3_controles_adverses.py`, `p3_resultats.json`. Le reste du rapport est inchangé.

## Prévision

Elle a été enregistrée avant tout calcul, le 17 octobre 2026 à 21 h 16 UTC (`taches.py prevoir`, journal des tâches, commit `7a480cb` sur `main`).

- **P1.** La marge mesurée du noyau des moments à L = 0,8, secteur pair, se stabilise entre 3·10⁻¹² et 6·10⁻¹² avec 40, 48, 56 et 64 modes. Elle varie de moins de 10 % entre 56 et 64 modes.
- **P2.** Un certificat dans l'architecture binary64 du document 75 est impossible à cette marge, car son seul budget d'assemblage dépasse 10⁻⁸. Il faut une arithmétique d'intervalles en précision multiple, avec une tête d'au moins 100 modes pour un minorant certifié d'au moins 10⁻¹².
- **Critères de rejet.**
  - Marge mesurée sous 10⁻¹³ quand N augmente.
  - Budget binary64 inférieur à la marge.

**Prévision de la reprise** (enregistrée avant calcul le 18 octobre, commit `d777652`, texte complet au journal des tâches) :
- **C1.** La forme de Weil de DH reste positive à 0,8, sur tout le secteur pair et sur le noyau des moments : la fenêtre 0,8 ne distingue pas DH de ζ. La forme générale est d'abord validée sur L(s,χ₅) contre ses zéros, avec un écart relatif inférieur à 10⁻⁶.
- **C2.** Corps de fonctions : la chaîne calculée côté arithmétique concorde avec le côté spectral à 10⁻²⁰, et λ_min ≥ 0 pour la vraie courbe. Une fausse courbe de genre 1 avec a = 5 est invisible dans le secteur pair et détectée dans le secteur impair. Un faux genre 2, avec quatre valeurs propres hors du cercle, est détecté dans le secteur pair pour un M ≤ 3.
- **C3.** Témoins négatifs pour ζ.
  - (a) Un quatuor fictif de zéros hors de la droite, à la hauteur 14,1347 : δ = 0 ne fait pas baisser λ_min, δ = 0,1 le rend négatif, et le seuil δ* est inférieur à 0,1.
  - (b) Le seuil ε* de perturbation de Λ(2) tombe à moins de 5 % de sa prédiction au premier ordre.

## Méthode

**P1, mesure, non certifiée.** Le script `p1_mesure_noyau_08.py` réutilise sans modification la fonction `noyau_des_moments` du document 81 (`3_Preuves_et_calculs/scripts/run_zhu_reproduction.py`).

- Cette fonction calcule la plus petite valeur de Q_W sur le sous-espace où le moment exponentiel est nul, dans une base de Legendre à N modes.
- La forme de Weil y est écrite en variable x : pôle, terme archimédien par quadrature de Gauss à K nœuds, termes premiers 2, 3 et 4.
- Le sous-espace est construit par réflecteur de Householder.

Trois contrôles de convergence :
- N = 40, 48, 56, 64 ;
- K = 48 puis 96 ;
- précision de 60 puis 80 chiffres.

Le secteur impair est calculé une fois, à N = 48. Aucun zéro de ζ n'est utilisé.

**P2, budgets.** Le script `p2_budgets_architecture_doc75.py` lit les budgets d'erreur réellement certifiés à S = 11/20 (`4_Archives/recus/V650/constructive/resultats_certificat_integral.json`). Pour chacun, il calcule la réduction qu'exigerait une marge de 5·10⁻¹², puis le coût induit selon la loi d'échelle écrite dans le code du certificat (`tentative_certificat_integral.py`, lignes 184 à 203).

**Reprise, contrôles adverses** (`p3_controles_adverses.py`, environ 400 s, 60 chiffres, N = 48, K = 48)

- **C0. Forme générale.** Pour une fonction de degré 1, de conducteur q et de facteur Γ((s+κ)/2), la forme en variable x reprend celle du document 81, avec :
  - a = (1+2κ)/4 ;
  - w(x) = 2x·e^{−2ax}/(1 − e^{−2x}) ;
  - C₀(L) = log(q/π) + E₁(4L) + ∫₀^{2L} (e^{−2x} − w(x))/x dx ;
  - les poids 2·Re b(n)/√n, où b(n) sont les coefficients de −F′/F (`src/rejection.py`) ;
  - un terme de pôle seulement pour ζ.

  Pour ζ (a = 1/4, q = 1), elle reproduit `weil_matrix()` du document 81 à 9·10⁻³⁵ près.
- **C1. Davenport–Heilbronn.** DH a la même équation fonctionnelle que L(s,χ₅) : q = 5, κ = 1, pas de pôle.
  - La formule est d'abord validée sur L(s,χ₅) contre ses 988 zéros d'ordonnée |t| < 600, avec f = cos⁴(πx/2L).
  - La même chaîne, appliquée ensuite à DH, n'utilise aucun zéro.
- **C2. Corps de fonctions.** Courbe y² = x³ + x + 1 sur F₅.
  - Les nombres de points N_m sont comptés par énumération dans F_{5^m}, pour m ≤ 6, avec une arithmétique écrite dans le script.
  - Forme côté arithmétique, avec g = f ⋆ f̃ :
    - suites f à support |k| ≤ M ;
    - Q(f) = (2g − 2)·g(0) + 2F̃(√q)F̃(1/√q) − Σ_{m≠0} g(m)·N_|m|·q^{−|m|/2} ;
    - restriction au noyau du pôle, F̃(√q) = 0.
  - Elle est comparée au côté spectral Σ_j F̃(r_j)·F̃(1/r_j), avec r_j = α_j/√q.
  - Les fausses courbes sont définies par leurs α fictifs : il n'existe pour elles aucun comptage géométrique.
- **C3. Témoins négatifs pour ζ à 0,8.**
  - (a) On ajoute à Q la contribution 4·Re F(γ₁ − iδ)² d'un quatuor fictif de zéros ½ ± δ ± iγ₁, avec γ₁ = 14,1347…, projetée sur le noyau. δ* est cherché par dichotomie.
  - (b) On multiplie Λ(2) par 1 + ε. On prédit ε* = λ₀ / (2Λ(2)/√2 · uᵀG₂u), où u est le vecteur propre de λ₀, puis on l'observe par dichotomie.

*Écart corrigé avant dépôt.* Une première exécution comptait mal les points pour m ≥ 3 : l'ordre des coefficients était inversé dans la réduction modulaire. De plus, elle alimentait la vraie courbe avec des N_m tirés de ses valeurs propres, ce qui rendait la comparaison en partie circulaire. Les deux défauts sont corrigés. Les comptes vérifient maintenant la rationalité, N_m = q^m + 1 − α^m − β^m, sans aucun écart, et la vraie courbe est calculée avec ses comptes.

## Résultat

**P1** (`p1_resultats.json`, marge en unités de Q_W/‖f‖²)

| N | K | chiffres | marge, secteur pair |
|---|---|---|---|
| 40 | 48 | 60 | 5,3992·10⁻¹² |
| 48 | 48 | 60 | 5,3788·10⁻¹² |
| 56 | 48 | 60 | 5,3573·10⁻¹² |
| 64 | 48 | 60 | 5,3469·10⁻¹² |
| 48 | 96 | 60 | 5,3852·10⁻¹² |
| 64 | 96 | 60 | 5,3503·10⁻¹² |
| 56 | 48 | 80 | 5,3573·10⁻¹² (identique à 60 chiffres) |
| 64 | 96 | 80 | 5,3503·10⁻¹² (identique à 60 chiffres) |

Secteur impair, N = 48 : 9,86·10⁻¹⁰, soit environ 180 fois la marge paire. Il ne limite pas.

- La marge décroît lentement et de façon monotone avec N (−0,19 % entre 56 et 64), comme attendu d'une valeur de Rayleigh–Ritz, qui majore l'infimum.
- La quadrature (K) n'agit qu'au quatrième chiffre, et la précision n'a aucun effet.
- La limite en N se situe vraisemblablement vers 5,3·10⁻¹² ; ce n'est pas certifié.

**P2** (`p2_resultats.json`). À 11/20, le certificat binary64 a les budgets suivants :

| Budget | Valeur à 11/20 | Réduction pour une marge de 5·10⁻¹² |
|---|---|---|
| table des poids | 1,1·10⁻⁴ | 2,2·10⁷ |
| quadrature en fréquence (trapèzes) | 1,5·10⁻⁴ | 3,0·10⁷ |
| assemblage binary64 | 1,1·10⁻⁵ | 2,2·10⁶ |

L'erreur de quadrature varie comme T·h². La réduire de 3·10⁷ demande environ 3,9·10⁹ cellules de fréquence, contre 7·10⁵. Le budget d'assemblage binary64, proportionnel au nombre de cellules, monterait alors à 6·10⁻², soit dix ordres de grandeur au-dessus de la marge.

**Conclusion de P2.** L'obstacle ne vient pas seulement de la précision binary64 ; il vient de toute l'architecture du document 75 : passage en fréquence, trapèzes, table linéaire des poids. Cette architecture ne peut pas certifier une marge de l'ordre de 10⁻¹².

**Route proposée** (non exécutée ; à ouvrir comme nouvelle fiche si l'auteur l'accepte) :
1. Certifier la tête en variable x, dans la formulation du document 81, en arithmétique d'intervalles à précision multiple :
   - quadrature de Gauss avec reste borné par l'analyticité, l'intégrande archimédien étant analytique sur [0, 2L] après extraction de la singularité en 0 ;
   - termes premiers exacts.
2. Majorer la queue au-delà de N modes par la coercivité du terme archimédien (croissance logarithmique en fréquence), suivant le schéma tête–queue du document 73.
3. Conclure par un complément de Schur certifié.

La marge mesurée et la convergence observée (moins de 0,2 % entre 56 et 64 modes) indiquent qu'une tête de 64 à 100 modes suffirait, si la borne de queue est assez fine. L'outil d'intervalles disponible ici est `mpmath.iv` ; Arb (python-flint) n'a pas pu être installé dans cet environnement.

**Reprise, contrôles adverses** (`p3_resultats.json`)

**C1. Validation, puis DH.**

| Contrôle | Résultat |
|---|---|
| L(s,χ₅), L = 0,8 : formule en x contre somme sur les zéros | 0,196556416291 contre 0,196556416291 ; écart relatif 7,3·10⁻¹⁶ |
| L(s,χ₅), L = 1,5 (cinq termes premiers) | écart relatif 3,1·10⁻¹⁵ |
| Contre-épreuve : facteur archimédien de ζ à la place de celui de χ₅ | écart relatif de 449 % (L = 0,8) et 4 910 % (L = 1,5) : la validation discrimine |
| DH, L = 0,8, secteur pair entier | λ_min = 6,5956·10⁻³ (N = 32), 6,5926·10⁻³ (N = 48) |
| DH, L = 0,8, noyau des moments | λ_min = 1,6222 (N = 32 et 48) |

Les poids de DH (2·Re b(n)/√n) valent +0,278 pour n = 2, −0,360 pour n = 3 et −1,442 pour n = 4, contre +0,980, +1,268 et +0,693 pour ζ.

**C2. Corps de fonctions** (λ_min sur le noyau du pôle ; écart arithmétique–spectral ≤ 8·10⁻⁴⁹ dans tous les cas, à 50 chiffres)

| | M = 1 pair | M = 2 pair | M = 2 impair | M = 3 pair | M = 3 impair |
|---|---|---|---|---|---|
| Vraie courbe (N_m comptés : 9, 27, 108, 675, 3 069, 15 552) | 3,52 | 0 (10⁻⁵¹) | 4,35 | 0 (−1,5·10⁻⁵⁰) | 0 (2·10⁻⁵⁰) |
| Faux genre 1, a = 5 > 2√5 | 0,043 | 0 (10⁻⁵¹) | **−0,024** | 0 (−3·10⁻⁵⁰) | **−0,318** |
| Faux genre 2, P(T) = 1 + 11T² + 25T⁴, \|α\| = 2,79 et 1,79 ≠ √5 | 3,04 | **−0,277** | 7,17 | **−1,555** | **−1,285** |

- **La vraie courbe n'est jamais négative.** Dès M = 2, sa plus petite valeur est nulle à la précision de calcul : une courbe de genre 1 n'a que deux valeurs propres de Frobenius, et un nombre fini de contraintes suffit à les annuler.
- **Le faux genre 1 n'est détecté que dans le secteur impair.** Pour f paire et α réel, F̃(r)F̃(1/r) = F̃(r)² ≥ 0 : une paire réelle hors du cercle est invisible aux tests pairs.
- **Le faux genre 2 est détecté dans le secteur pair dès M = 2.** Son quatuor est complexe, et donne un terme 4·Re F̃(r)², qui peut être négatif.

**C3. Témoins négatifs pour ζ à 0,8, N = 48** (λ₀ = 5,37876479342·10⁻¹²)

| Défaut injecté | λ_min sur le noyau |
|---|---|
| Paire fictive sur la droite (δ = 0) | 5,37876479356·10⁻¹² (ne baisse pas) |
| Quatuor, δ = 0,1 | −4,24·10⁻³ |
| Quatuor, δ = 0,01 | −2,67·10⁻⁵ |
| Quatuor, δ = 0,001 | −2,33·10⁻⁸ |
| Seuil de détection δ* | 2,11·10⁻⁵ |
| Λ(2) × (1 + ε) : ε* prédit au premier ordre | 1,4928·10⁻¹⁰ |
| ε* observé | 1,4902·10⁻¹⁰ (écart 0,17 %) ; dans l'autre sens, λ_min = 1,07·10⁻¹¹ |

## Portée

- **P1 est une mesure, non certifiée.** Elle majore la plus petite valeur sur le noyau, car c'est une valeur de Rayleigh–Ritz dans un espace de dimension finie ; elle ne la minore pas.
- La positivité de Weil à 0,8 est déjà certifiée par Zhu, qui donne λ*(0,8) ≥ 8,9·10⁻¹⁸ sur toutes les fonctions de support [−0,8 ; 0,8]. Ce travail n'ajoute aucune fenêtre ni aucune conséquence globale. Un certificat sur le noyau donnerait seulement une marge indépendante, environ 10⁵ à 10⁶ fois plus forte, sur ce sous-espace.
- **P2 est un constat sur une architecture**, pas une obstruction mathématique. Il ne dit rien d'une autre architecture.
- RH n'est ni utilisée ni approchée : la positivité sur toutes les fenêtres est équivalente à RH, et une fenêtre ne l'implique pas.
- **C1 le montre directement.** La même chaîne, appliquée à DH, qui viole RH, donne une forme positive à 0,8, et même plus largement positive sur le noyau (1,6 contre 5·10⁻¹²).
  - L'énoncé local, et tout certificat futur de la marge à 0,8, sont donc vrais mot pour mot pour une fonction sans RH : ils ne portent par eux-mêmes aucune information sur RH.
  - Leur intérêt reste méthodologique : outil, et contrôle d'une architecture de certificat.
- **C2 donne l'image de la chaîne dans les corps de fonctions.**
  - Elle se transpose exactement : l'écart entre côté arithmétique et côté spectral est de 10⁻⁴⁹.
  - Elle détecte une fausse courbe seulement quand l'espace de test voit le défaut. Une paire réelle hors du cercle échappe au secteur pair, d'où la nécessité de garder les deux secteurs.
  - Elle montre aussi une différence de structure. Dans une fenêtre finie, une courbe a une plus petite valeur exactement nulle dès que la fenêtre dépasse son nombre de zéros. Pour ζ, la marge sur le noyau reste strictement positive, mais petite. Ce n'est pas un argument pour ou contre RH.
- **C3 montre que la chaîne « forme → projection → plus petite valeur » détecte un défaut au bon endroit et à la bonne échelle.**
  - Une paire sur la droite ne crée aucune négativité.
  - Un quatuor hors de la droite à la hauteur du premier zéro est détecté dès δ ≈ 2·10⁻⁵.
  - Une erreur relative de 1,5·10⁻¹⁰ sur Λ(2) suffit à changer le signe, comme prévu au premier ordre.
  - Corollaire : à cette marge, tout certificat devra borner chaque terme premier à mieux que 10⁻¹⁰ en relatif. Cela confirme P2.

## Critère de rejet

| Critère, écrit avant | Observé | Verdict |
|---|---|---|
| Marge mesurée sous 10⁻¹³ quand N augmente | 5,35·10⁻¹² à N = 64, décroissance de 0,2 % par palier de 8 modes | non atteint : la voie par fenêtres n'est pas fermée à 0,8 |
| Budget binary64 inférieur à la marge (P2 fausse) | 1,1·10⁻⁵ déjà à 11/20, et environ 6·10⁻² à la résolution requise | non atteint : P2 juste |

**Critères de la reprise :**

| Critère, écrit avant | Observé | Verdict |
|---|---|---|
| Écart de validation sur L(s,χ₅) au-delà de 10⁻⁶ | 7,3·10⁻¹⁶ et 3,1·10⁻¹⁵ | non atteint |
| λ_min(DH) < 0 à 0,8 | 6,59·10⁻³ (secteur) et 1,62 (noyau) | non atteint : C1 juste |
| Accord arithmétique–spectral moins bon que 10⁻²⁰, ou vraie courbe négative | 8·10⁻⁴⁹ ; plus petite valeur ≥ −2·10⁻⁵⁰, c'est-à-dire nulle à la précision | non atteint : C2 juste |
| Défaut non détecté (faux genre 1 en impair, faux genre 2 en pair, quatuor δ = 0,1) | tous détectés | non atteint |
| δ = 0 rend λ_min négatif | λ_min inchangé | non atteint : C3 (a) juste, δ* = 2,1·10⁻⁵ < 0,1 |
| ε* observé à plus de 5 % de la prédiction | 0,17 % | non atteint : C3 (b) juste |

**Prévisions :**
- P1 juste : la marge reste dans [3, 6]·10⁻¹², avec une variation de 0,19 % entre 56 et 64 modes.
- P2 juste sur l'impossibilité, et plus fortement que prévu : c'est toute l'architecture qui ne convient pas, pas seulement le binary64.
- L'estimation de taille (au moins 100 modes de tête) n'est pas testée, faute de certificat construit.

## Statut proposé

**partiel.** Le travail donne une mesure confirmée (P1) et un obstacle documenté pour l'architecture existante (P2). Il y ajoute trois contrôles adverses, tous conformes à la prévision :
- la fenêtre 0,8 ne distingue pas DH ;
- la chaîne se transpose aux corps de fonctions et y détecte de fausses courbes ;
- elle détecte des défauts injectés au seuil prévu. Le certificat lui-même n'est pas obtenu ; la route proposée ci-dessus est à ouvrir comme fiche suivante si l'auteur l'accepte. Ce résultat n'est pas équivalent à RH.

**Fichiers :**
- `p1_mesure_noyau_08.py` et `p1_resultats.json` : la mesure ;
- `p2_budgets_architecture_doc75.py` et `p2_resultats.json` : l'analyse des budgets ;
- `p3_controles_adverses.py` et `p3_resultats.json` : les contrôles de la reprise ;
- ce rapport.

La route tête–queue (point 4 de la vérification) reste à ouvrir comme fiche séparée. Sa majoration de queue sera écrite avant calcul.
