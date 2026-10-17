# Table logique — Programme Riemann V6.59

*Ce que le corpus établit, sous quelles hypothèses, et ce qui manque pour conclure. Les statuts sont lus en direct dans le pilotage (`pilotage_recherche.json`) ; les énoncés viennent de `2_Methode/Pilotage/table_logique.json`. Auteur : Vincent NOËL.*

**RH reste ouverte.** Une ligne « Démontré » vaut dans le cadre de ses hypothèses ; une ligne « Mesuré » n’est pas une preuve.

## Notation

| Signe | Sens |
|---|---|
| ⇒ | implique (démontré dans le cadre indiqué) |
| ⇔ | équivaut à |
| ⇏ | n'implique pas (contre-exemple ou obstruction exhibée) |
| ∧ | et : toutes les conditions de la garde sont requises |
| Θ | sup des parties réelles des zéros de ζ ; RH ⇔ Θ = ½ |
| Q_W | forme quadratique de Weil (formule explicite), Fourier unitaire |
| X_S | tests de support [−S, S], d'énergie finie, à moments exponentiels nuls |

## 1. Vue d’ensemble : cinq routes vers RH

| Route | Garde logique | Énoncés acquis | Ce qui manque (coupe ouverte) |
|------------|----------------|-----|----------------|
| Route W — positivité de Weil | W10 (signe) ∧ W9 (couverture) ⇒ W11 ; W11 ⇔ RH (W1) | 6 / 12 | W7 (Acquis partiel), W8 (Acquis partiel), W9 (Acquis partiel), W10 (Ouvert), W11 (Ouvert) |
| Route C — le carré (structure qui impose le signe) | C5 (objet qui fournit le carré) ⇒ W10, hypothèse de travail ; puis route W | 2 / 5 | C3 (Acquis partiel), C5 (Ouvert) |
| Route Q — l'énergie initiale | Q4 ⇔ RH (par Q2) | 3 / 4 | Q4 (Ouvert) |
| Route J — l'énergie de Chebyshev et l'amplification | J3 ∧ J4 ∧ J5 ⇒ zéro-libre pour Re s > 3/4 (J6) ; J7 ⇔ RH (J2) | 4 / 7 | J5 (Ouvert), J7 (Ouvert) |
| Route H — réalisation spectrale (Hilbert–Pólya) | H3 ∧ H4 ⇒ RH (H2) | 0 / 4 | H3 (Ouvert), H4 (Ouvert) |

Lecture : une route aboutit quand toute sa coupe ouverte est fermée. Aucune ne l’est. La route W est la plus avancée : son verrou est W10, la loi de signe, à démontrer avec W9, la couverture. La route C dit d’où ce signe pourrait venir.

## 2. Route W — positivité de Weil

RH ⇔ Q_W(f) ≥ 0 pour tous les tests admissibles. Le corpus certifie le signe sur des fenêtres bornées et cherche une loi de signe sur une famille couvrante.

**Garde :** W10 (signe) ∧ W9 (couverture) ⇒ W11 ; W11 ⇔ RH (W1)

| ID | Énoncé (forme logique) | Hypothèses | Statut de l’énoncé | Portée | Pièce | Fiche (statut) |
|--|------------------------------|------------|--------|--------------|------|--------|
| **W0** | Formule explicite : Σ_ρ F(γ_ρ) = pôle + archimédien − Σ_n 2Λ(n) n^{−1/2} g(log n) [Wei52] | f test lisse à support compact | **Classique (cité)** | Identité exacte entre zéros et premiers | [doc. 23](1_Presentation/23_AUDIT_V6_3B_FORMULE_EXPLICITE.md) | IDE-010 (Classique (cité)) |
| **W1** | Critère de Weil : RH ⇔ (∀ f admissible : Q_W(f ∗ f̃) ≥ 0) [Wei52] [Bom00a] | aucune (critère) | **Classique (cité)** | Critère classique ; le domaine exact est précisé dans le doc. 76 | [doc. 76](1_Presentation/76_RECONSTRUIRE_LA_PISTE_GLOBALE_DE_WEIL.pdf) | IDE-052 (Ouvert) |
| **W2** | P = ∂² − ¼ engendre les tests ; transports, cœur dense et parité respectent le domaine de Q_W  | gardes des doc. 67–68 | **Démontré** | Construction des familles de tests | [doc. 67](1_Presentation/67_CONSTRUIRE_DES_PONTS_AVEC_BELLMAN.pdf) | IDE-044 (Démontré) |
| **W3** | Q_W = (modèle continu) + (fluctuation arithmétique signée), exactement ; le modèle continu seul peut être < 0  | annulation polaire (moments nuls) | **Démontré** | La fluctuation doit payer le bilan | [doc. 70](1_Presentation/70_PONT_ARITHMETIQUE_ET_DETTE_DE_COUPLAGE.pdf) | IDE-046 (Démontré) |
| **W4** | ∀ S ≤ 11/20, ∀ f ∈ X_S : Q_W(f) ≥ (3/10000)‖f‖² ; (S ≤ ½ : ‖f‖²/250 ; S ≤ 0,347 : ‖f‖²/25)  | modèle arithmétique d'intervalles déclaré ; sans zéros ni RH | **Démontré** | Certificat sur tout l'espace infini X_S, pas au-delà de 11/20 ; en portée, dominé par le minorant certifié de Zhu (L ≤ 0,8, toutes fonctions) | [doc. 75](1_Presentation/75_RECUPERATION_TRANSPORT_ET_RH.pdf) | IDE-048 (Démontré) |
| **W5** | Mesuré (non certifié) : inf_{X_S} Q_W/‖f‖² ≈ 5,4·10⁻¹² à S = 0,8 ; λ*(0,8) ∈ [8,9·10⁻¹⁸ ; 2,27·10⁻¹⁷] (Zhu, certifié) [Zhu26] | Galerkin 40 modes, 60 chiffres | **Mesuré** | La positivité à 0,8 suit déjà de Zhu ; certifier 5·10⁻¹² sur le noyau renforcerait la marge, pas la portée. La marge s'effondre avec S | [doc. 81](1_Presentation/81_ZHU_REPRODUIT.pdf) | IDE-040 (Ouvert) |
| **W6** | Q_W = identité − compact dans la métrique d'énergie ; pas de marge uniforme > 0 en H¹  | métrique d'énergie déclarée | **Démontré** | Interdit d'espérer une coercivité uniforme | [doc. 68](1_Presentation/68_ARITHMETIQUE_DES_PASSAGES_ET_QUEUE_EFFECTIVE.pdf) | IDE-045 (Démontré) |
| **W7** | Signe de Q_W sur un bloc ⇐ signe de la tête ∧ dette de Schur des couplages bornée  | gardes de Schur | **Acquis partiel** | Identité acquise ; borne de dette non uniforme | [doc. 70](1_Presentation/70_PONT_ARITHMETIQUE_ET_DETTE_DE_COUPLAGE.pdf) | IDE-047 (Acquis partiel) |
| **W8** | Transport exact d'un test positif ⇒ test positif, si réserve ≥ résidu sur la ligne  | brique initiale, réserve | **Acquis partiel** | Existence de toutes les lignes positives ouverte | [doc. 78](1_Presentation/78_TRANSPORT_POSITIF_RESERVE_ET_BRIQUE_INITIALE.pdf) | IDE-049 (Acquis partiel) |
| **W9** | Signe sur une famille couvrante ∧ passage à la limite dans la norme de forme ⇒ signe sur tous les tests [SuzH23] | cœur dense en H¹ (doc. 67, B3) | **Acquis partiel** | Transfert acquis ; signe sur la famille ouvert | [doc. 76 (compl.)](1_Presentation/76_COMPLEMENT_COUP_DOUBLE.pdf) | IDE-050 (Acquis partiel) |
| **W10** | Il existe une loi arithmétique L telle que ∀ f de la famille couvrante : Q_W(f) ≥ 0 [Suz26] [SuzSig23] | à trouver | **Ouvert** | Le verrou central | [doc. 79](1_Presentation/79_COMPENSATION_PROFILS_ET_OBSTRUCTIONS.pdf) | IDE-051 (Ouvert) |
| **W11** | ∀ f admissible : Q_W(f ∗ f̃) ≥ 0  | aucune : c'est la conclusion visée | **Ouvert** | Ouvert ; équivaut à RH par W1 | [doc. 76](1_Presentation/76_RECONSTRUIRE_LA_PISTE_GLOBALE_DE_WEIL.pdf) | IDE-052 (Ouvert) |

## 3. Route C — le carré (structure qui impose le signe)

Là où RH est un théorème, le signe vient d'un carré (polarisation). Pour ζ, l'objet qui fournirait ce carré reste à construire.

**Garde :** C5 (objet qui fournit le carré) ⇒ W10, hypothèse de travail ; puis route W

| ID | Énoncé (forme logique) | Hypothèses | Statut de l’énoncé | Portée | Pièce | Fiche (statut) |
|--|------------------------------|------------|--------|--------------|------|--------|
| **C1** | Courbe C/𝔽_q : B(u) = Tr(u·ι(u)) ≥ 0 ∀u ⇔ RH(C) ; comptages ≥ 0 ∧ degrés ≥ 0 ⇏ RH (119 contre-exemples) [Wei48] [Mum70] [MT58] | racines distinctes pour (b) | **Démontré** | Calcul exact, 425 courbes et 220 faux jumeaux | [doc. 80](1_Presentation/80_D_OU_VIENT_LE_SIGNE.pdf) | IDE-022 (Mesuré) |
| **C2** | Pour C/𝔽_q : positivité de Rosati (polarisation) ⇒ ∣α∣ = √q [Wei48] [Del74] [Has36] | objet géométrique : jacobienne polarisée | **Classique (cité)** | Classique (Weil 1948) | [doc. 28](1_Presentation/28_MODELE_REDUIT_NECESSITE_DEMONTREE.pdf) | IDE-006 (Mesuré) |
| **C3** | Signature d'une « surface virtuelle » calculée depuis les premiers : celle de ζ a la forme attendue (une direction positive) ; DH a des directions en trop [CC21] [Con99] | fenêtres finies | **Acquis partiel** | Signatures construites ; aucun objet imposant le signe | [doc. 46](1_Presentation/46_LA_SURFACE_VIRTUELLE.pdf) | IDE-064 (Acquis partiel) |
| **C4** | Transplantation directe de Stepanov à ζ (modèle d'échelle étudié) ⇏ signe [Ste69] [Bom73] | le modèle étudié | **Obstruction** | Obstruction de méthode, réouvrable avec une dérivation construite | [doc. 51](1_Presentation/51_J3B_LE_FROBENIUS_DE_CARACTERISTIQUE_UN.pdf) | IDE-065 (Obstruction) |
| **C5** | ∃ ? une structure (polarisation, classe ample) telle que Q_W(f) = ‖Af‖² pour une raison de structure [CC21] | à construire | **Ouvert** | Hypothèse de travail ; aucune forme d'objet déclarée nécessaire | [doc. 80](1_Presentation/80_D_OU_VIENT_LE_SIGNE.pdf) | IDE-036 (Ouvert) |

## 4. Route Q — l'énergie initiale

Le Théorème A ramène RH à une borne de croissance de l'énergie Q construite avec les premiers.

**Garde :** Q4 ⇔ RH (par Q2)

| ID | Énoncé (forme logique) | Hypothèses | Statut de l’énoncé | Portée | Pièce | Fiche (statut) |
|--|------------------------------|------------|--------|--------------|------|--------|
| **Q1** | c = Λ∗Λ − Λ·log + 2γΛ = 1∗a, a(n) = μ(n)(log²n − 2γ log n) ; G(s) = ζ·(f″ + 2γf′), f = 1/ζ  | aucune | **Démontré** | Identités exactes | [Lemmes rigoureux](3_Preuves_et_calculs/preuves/LEMMES_RIGOUREUX.md) | IDE-001 (Démontré) |
| **Q2** | Exposant de croissance de Q(X) = 2(Θ − ½) ; d'où le critère RH ⇔ Q(X) = X^{o(1)} [Cra22] [Nym50] [Beu55] | aucune (inconditionnel) | **Démontré** | Démontré, relu en interne | [article 1](1_Presentation/articles/article1_mean_square_double_poles.pdf) | IDE-002 (Démontré) |
| **Q3** | RH ⇒ Q(X) ∼ (S/3)(log X)³ ; RH ⇒ (S = 4κ ⇔ zéros simples) ; Q/(log X)³ → 4κ/3 ⇔ RH ∧ simplicité [Cra22] [Mon73] | RH pour l'asymptotique | **Démontré** | Implication démontrée, relue en interne : une calibration sous RH, pas un pas vers RH | [article 1](1_Presentation/articles/article1_mean_square_double_poles.pdf) | IDE-003 (Conditionnel) |
| **Q4** | Q(X) = X^{o(1)} prouvé depuis les premiers seuls  | à trouver | **Ouvert** | Ouvert ; équivalent à RH par Q2 | [Lemmes rigoureux](3_Preuves_et_calculs/preuves/LEMMES_RIGOUREUX.md) | IDE-058 (Ouvert) |

## 5. Route J — l'énergie de Chebyshev et l'amplification

RH ⇔ J(X) = ∫₁ˣ (ψ − x)² ≪ X². Le corpus restitue exactement la somme de Möbius et contrôle la tête des conducteurs ; la grande queue est ouverte.

**Garde :** J3 ∧ J4 ∧ J5 ⇒ zéro-libre pour Re s > 3/4 (J6) ; J7 ⇔ RH (J2)

| ID | Énoncé (forme logique) | Hypothèses | Statut de l’énoncé | Portée | Pièce | Fiche (statut) |
|--|------------------------------|------------|--------|--------------|------|--------|
| **J1** | Σ_{d∣n} Λ(d) = log n  | aucune | **Classique (cité)** | Classique ; ne borne rien seule | [Corrélations](1_Presentation/CORRELATIONS_IDENTITE_ET_ENERGIE.pdf) | IDE-054 (Classique (cité)) |
| **J2** | Critère : RH ⇔ J(X) = O(X²) pour les vrais Λ [Cra22] | aucune (critère) | **Classique (cité)** | Critère classique | [Corrélations](1_Presentation/CORRELATIONS_IDENTITE_ET_ENERGIE.pdf) | IDE-057 (Ouvert) |
| **J3** | A_o(x) = F_{p²}(x) − F_{p²}(x/p) : restitution exacte, stable par dilatation  | p premier impair | **Démontré** | Démontré | [Essai V6.55](1_Presentation/ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.pdf) | IDE-059 (Démontré) |
| **J4** | Tête q ≤ H bornée explicitement, à toutes les échelles  | paramètres déclarés | **Démontré** | Démontré | [Essai V6.55](1_Presentation/ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.pdf) | IDE-060 (Démontré) |
| **J5** | À H = X : R_{q>X} ≤ C X³(1 + log X)^k, en conservant μ(q)  | à trouver | **Ouvert** | Ouvert ; le crible générique ne suffit pas | [Essai V6.55](1_Presentation/ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.pdf) | IDE-061 (Ouvert) |
| **J6** | copies ∧ head ∧ large_q ⇒ J ≪ X^{5/2} polylog ⇒ ζ(s) ≠ 0 pour Re s > 3/4  | les trois contrats | **Conditionnel** | Conditionnel ; ne donne pas J_bound (5/2 > 2) | [Essai V6.55](1_Presentation/ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.pdf) | IDE-062 (Conditionnel) |
| **J7** | J(X) = O(X²) pour les vrais Λ, à toutes les échelles [Cra22] | aucune : c'est la conclusion visée | **Ouvert** | Ouvert ; équivaut à RH par J2 | [Corrélations](1_Presentation/CORRELATIONS_IDENTITE_ET_ENERGIE.pdf) | IDE-057 (Ouvert) |

## 6. Route H — réalisation spectrale (Hilbert–Pólya)

Un opérateur auto-adjoint arithmétique dont le spectre capture exactement les zéros donnerait RH. Rien d'exhaustif n'est construit.

**Garde :** H3 ∧ H4 ⇒ RH (H2)

| ID | Énoncé (forme logique) | Hypothèses | Statut de l’énoncé | Portée | Pièce | Fiche (statut) |
|--|------------------------------|------------|--------|--------------|------|--------|
| **H1** | L'opérateur de ζ se reconstruit sur une fenêtre finie depuis les seuls premiers ; sa métrique est > 0 pour ζ et L, < 0 pour DH exactement à ses zéros hors droite  | fenêtre finie | **Mesuré** | Mesuré | [doc. 33](1_Presentation/33_LE_GENERATEUR_DES_PREMIERS.pdf) | IDE-026 (Mesuré) |
| **H2** | Auto-adjonction arithmétique ∧ complétude spectrale ⇒ RH [Con99] | les deux | **Conditionnel** | Conditionnel ; aucune des deux n'est acquise | [doc. 32](1_Presentation/32_LE_CHAINON_DU_DISCRET_AU_CONTINU.pdf) | IDE-042 (Ouvert) |
| **H3** | ∃ ? un opérateur auto-adjoint construit depuis l'arithmétique dont les valeurs propres sont les γ [Con99] | à construire | **Ouvert** | Ouvert ; reparamétrisations (Schrödinger, Heff) insuffisantes | [doc. 32](1_Presentation/32_LE_CHAINON_DU_DISCRET_AU_CONTINU.pdf) | IDE-042 (Ouvert) |
| **H4** | Le spectre de cet opérateur capture tous les zéros, avec multiplicités, et son domaine est justifié  | à construire | **Ouvert** | Ouvert ; une fenêtre finie ne suffit pas | [doc. 32](1_Presentation/32_LE_CHAINON_DU_DISCRET_AU_CONTINU.pdf) | IDE-041 (Ouvert) |

## 7. Témoins contraires

Un argument qui prétend imposer le signe doit passer ces témoins.

| ID | Fait | Ce qu’il interdit | Statut | Pièce |
|--|--------------------|--------------------|------|-----|
| **T1** | DH (équation fonctionnelle, sans produit d'Euler) : ≥ 25 directions négatives certifiées dans une fenêtre | Tout argument qui prétend imposer le signe sans utiliser le produit d'Euler doit échouer sur DH. | Démontré | [doc. 60](1_Presentation/60_ARTICLES_ET_CERTIFICAT_DE_NEGATIVITE.pdf) |
| **T2** | Dans V_q (degré 1 déclaré) : RH ⇒ point d'Euler ; la réciproque n'est pas établie | Le produit d'Euler est nécessaire ici ; ce n'est pas une preuve qu'il suffit. | Démontré | [doc. 30](1_Presentation/30_ARCHIPEL_D_EULER.pdf) |
| **T3** | 119 faux jumeaux : comptages ≥ 0 ∧ degrés ≥ 0 ∧ ¬RH | Aucun argument de comptage ou de degré ne remplace un carré. | Mesuré | [doc. 80](1_Presentation/80_D_OU_VIENT_LE_SIGNE.pdf) |

## 8. Obstructions : ce qui ne suffit pas

| Énoncé | Fiche | Pièce |
|------------------------------|----|-----|
| Certificat sur S ≤ 11/20 ⇏ signe sur tous les supports | IDE-048 | [doc. 75](1_Presentation/75_RECUPERATION_TRANSPORT_ET_RH.pdf) |
| Un pli choisi certifié ⇏ signe global | IDE-043 | [doc. 66](1_Presentation/66_UN_PLI_CERTIFIE_ET_SA_PAIRE.pdf) |
| Crible générique ⇏ borne de la grande queue (coût D√H) | IDE-063 | [Essai V6.55](1_Presentation/ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.pdf) |
| Norme de la partie première seule : diverge, ⇏ contrôle de la forme | IDE-069 | [doc. 66](1_Presentation/66_UN_PLI_CERTIFIE_ET_SA_PAIRE.pdf) |
| J ≪ X^{5/2} ⇏ J ≪ X² (exposant insuffisant) | IDE-062 | [Essai V6.55](1_Presentation/ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.pdf) |
| Pas de marge uniforme en H¹ ⇒ pas de preuve par coercivité seule | IDE-045 | [doc. 68](1_Presentation/68_ARITHMETIQUE_DES_PASSAGES_ET_QUEUE_EFFECTIVE.pdf) |
| Fenêtre par fenêtre : marge ∼ 10⁻¹² à S = 0,8 et en chute rapide ⇏ stratégie vers RH | IDE-040 | [doc. 81](1_Presentation/81_ZHU_REPRODUIT.pdf) |

## 9. Ce qui manque, au plus court, et ce qui est déjà en chantier

| Route | Énoncé ouvert | Investigations pré-enregistrées qui le visent |
|--|------------------------|------------------------|
| W | **W7** Signe de Q_W sur un bloc ⇐ signe de la tête ∧ dette de Schur des couplages bornée | `duale_schur` (Dette de Schur dans la norme duale); `test_paquets` (Confronter la loi candidate aux vrais coefficients) |
| W | **W8** Transport exact d'un test positif ⇒ test positif, si réserve ≥ résidu sur la ligne | `signe_paquets` (Paquets signés : garder premiers, coupures et dette) |
| W | **W9** Signe sur une famille couvrante ∧ passage à la limite dans la norme de forme ⇒ signe sur tous les tests | `signe_paquets` (Paquets signés : garder premiers, coupures et dette); `couverture_constructive` (Deux filtres : approximants et norme de forme) |
| W | **W10** Il existe une loi arithmétique L telle que ∀ f de la famille couvrante : Q_W(f) ≥ 0 | `signe_paquets` (Paquets signés : garder premiers, coupures et dette); `duale_schur` (Dette de Schur dans la norme duale); `test_paquets` (Confronter la loi candidate aux vrais coefficients) |
| W | **W11** ∀ f admissible : Q_W(f ∗ f̃) ≥ 0 | `couverture_constructive` (Deux filtres : approximants et norme de forme) |
| C | **C3** Signature d'une « surface virtuelle » calculée depuis les premiers : celle de ζ a la forme attendue (une direc… | aucune : piste à ouvrir |
| C | **C5** ∃ ? une structure (polarisation, classe ample) telle que Q_W(f) = ‖Af‖² pour une raison de structure | aucune : piste à ouvrir |
| Q | **Q4** Q(X) = X^{o(1)} prouvé depuis les premiers seuls | aucune : piste à ouvrir |
| J | **J5** À H = X : R_{q>X} ≤ C X³(1 + log X)^k, en conservant μ(q) | `mu_correlations` (Carte d’identité de μ et corrélations pondérées); `grands_conducteurs` (Tester une loi spécifique des grands conducteurs) |
| J | **J7** J(X) = O(X²) pour les vrais Λ, à toutes les échelles | aucune : piste à ouvrir |
| H | **H3** ∃ ? un opérateur auto-adjoint construit depuis l'arithmétique dont les valeurs propres sont les γ | aucune : piste à ouvrir |
| H | **H4** Le spectre de cet opérateur capture tous les zéros, avec multiplicités, et son domaine est justifié | aucune : piste à ouvrir |

## 10. Les 79 relations typées du graphe des idées

Chaque relation relie deux fiches d’idées ; la garde liste toutes les fiches requises. Une relation d’usage ou une analogie n’est pas une implication.

### ⇔ equivalence — « équivaut à » (3)

| Origine | | Cible | Contenu | Garde |
|--------------|--|--------------|--------------|------|
| IDE-058 Borne de l’énergie initiale Q *(Ouvert)* | ⇔ | IDE-053 Hypothèse de Riemann *(Ouvert)* | Critère A dans son cadre |  |
| IDE-052 Weil sur tous les tests *(Ouvert)* | ⇔ | IDE-053 Hypothèse de Riemann *(Ouvert)* | Critère de Weil, domaine précisé |  |
| IDE-057 Borne de force RH *(Ouvert)* | ⇔ | IDE-053 Hypothèse de Riemann *(Ouvert)* | Critère classique, pour Λ |  |

### ⇐ garde conditionnel — « donne la cible si toute la garde est réunie » (7)

| Origine | | Cible | Contenu | Garde |
|--------------|--|--------------|--------------|------|
| IDE-042 Hilbert–Pólya *(Ouvert)* | ⇐ garde | IDE-053 Hypothèse de Riemann *(Ouvert)* | Auto-adjonction arithmétique ET capture exhaustive | IDE-042 ∧ IDE-041 |
| IDE-051 Loi de signe de la famille *(Ouvert)* | ⇐ garde | IDE-052 Weil sur tous les tests *(Ouvert)* | Signe ET couverture dans le domaine requis | IDE-051 ∧ IDE-050 |
| IDE-050 Couverture et passage à la limite *(Acquis partiel)* | ⇐ garde | IDE-052 Weil sur tous les tests *(Ouvert)* | Signe ET couverture dans le domaine requis | IDE-051 ∧ IDE-050 |
| IDE-059 Restitution et dilatations *(Démontré)* | ⇐ garde | IDE-062 Étape conditionnelle : 3/4 *(Conditionnel)* | Les trois contrats sont requis | IDE-059 ∧ IDE-060 ∧ IDE-061 |
| IDE-060 Diagonale et petits conducteurs *(Démontré)* | ⇐ garde | IDE-062 Étape conditionnelle : 3/4 *(Conditionnel)* | Les trois contrats sont requis | IDE-059 ∧ IDE-060 ∧ IDE-061 |
| IDE-061 Grands conducteurs signés *(Ouvert)* | ⇐ garde | IDE-062 Étape conditionnelle : 3/4 *(Conditionnel)* | Les trois contrats sont requis | IDE-059 ∧ IDE-060 ∧ IDE-061 |
| IDE-004 Proposition C *(Conditionnel)* | ⇐ garde | IDE-003 Théorème B *(Conditionnel)* | Les hypothèses supplémentaires ne sont pas levées |  |

### → construction — « fournit une brique à » (22)

| Origine | | Cible | Contenu | Garde |
|--------------|--|--------------|--------------|------|
| IDE-001 Lemmes 1 à 5 *(Démontré)* | → | IDE-002 Théorème A *(Démontré)* | Pôles et transformée de Mellin |  |
| IDE-001 Lemmes 1 à 5 *(Démontré)* | → | IDE-003 Théorème B *(Conditionnel)* | Identités utiles sous RH |  |
| IDE-014 DARK-ZETA *(Outil)* | → | IDE-055 Corrélations ancrées *(Démontré)* | Repérer la perte de l’origine |  |
| IDE-022 V6.6Le Modèle réduit *(Mesuré)* | → | IDE-025 V6.9Le chaînon F = q^D *(Mesuré)* | Faux jumeaux et métrique |  |
| IDE-025 V6.9Le chaînon F = q^D *(Mesuré)* | → | IDE-026 V6.10Le générateur des premiers *(Mesuré)* | Reconstruire depuis les premiers |  |
| IDE-018 DUAL-LOCK *(Outil)* | → | IDE-047 Dette des couplages *(Acquis partiel)* | Gram et couplages |  |
| IDE-039 Kalman, GPS analytique *(Mesuré)* | → | IDE-047 Dette des couplages *(Acquis partiel)* | Innovations et dette de couplage |  |
| IDE-037 Localisation de sources *(Diagnostic)* | → | IDE-047 Dette des couplages *(Acquis partiel)* | Résidus et Grams |  |
| IDE-024 V6.8L'Archipel d'Euler *(Démontré)* | → | IDE-043 Fibres, jets et pli choisi *(Démontré)* | Comparer sous contraintes exactes |  |
| IDE-044 P, moments et domaines *(Démontré)* | → | IDE-045 Changement de métrique *(Démontré)* | Domaines et métriques compatibles |  |
| IDE-044 P, moments et domaines *(Démontré)* | → | IDE-046 Fluctuation arithmétique signée *(Démontré)* | Moments et annulation polaire |  |
| IDE-045 Changement de métrique *(Démontré)* | → | IDE-048 Lego local : S ≤ 11/20 *(Démontré)* | Réduction tête–queue dans le bon domaine |  |
| IDE-044 P, moments et domaines *(Démontré)* | → | IDE-050 Couverture et passage à la limite *(Acquis partiel)* | Cœur, transports et filtres |  |
| IDE-054 Identité des vrais coefficients *(Classique (cité))* | → | IDE-056 Énergie J *(Classique (cité))* | Vrais poids Λ |  |
| IDE-055 Corrélations ancrées *(Démontré)* | → | IDE-056 Énergie J *(Classique (cité))* | Formule de corrélation avec bords |  |
| IDE-054 Identité des vrais coefficients *(Classique (cité))* | → | IDE-059 Restitution et dilatations *(Démontré)* | Inversion exacte de Möbius |  |
| IDE-059 Restitution et dilatations *(Démontré)* | → | IDE-060 Diagonale et petits conducteurs *(Démontré)* | Regroupement par conducteur |  |
| IDE-010 Formule explicite de Weil *(Classique (cité))* | → | IDE-046 Fluctuation arithmétique signée *(Démontré)* | Forme explicite complète, normalisation et domaine |  |
| IDE-022 V6.6Le Modèle réduit *(Mesuré)* | → | IDE-064 Surface et Frobenius virtuels *(Acquis partiel)* | Chercher la structure d’un étage supérieur |  |
| IDE-066 Lemme des jets et relief *(Démontré)* | → | IDE-043 Fibres, jets et pli choisi *(Démontré)* | Rang, contraintes exactes, fibres et plis |  |
| IDE-005 Davenport–Heilbronn *(Obstruction)* | → | IDE-067 Certificat négatif de DH *(Démontré)* | De témoin numérique à certificat sous budget |  |
| IDE-030 V6.16La Rencontre à trois *(Démontré)* | → | IDE-068 La Rencontre à n *(Mesuré)* | Étudier des interactions à plusieurs zéros |  |

### ⊣ obligation — « laisse à établir pour » (8)

| Origine | | Cible | Contenu | Garde |
|--------------|--|--------------|--------------|------|
| IDE-026 V6.10Le générateur des premiers *(Mesuré)* | ⊣ | IDE-041 Complétude spectrale *(Ouvert)* | Capturer toute la famille, pas seulement une fenêtre |  |
| IDE-026 V6.10Le générateur des premiers *(Mesuré)* | ⊣ | IDE-051 Loi de signe de la famille *(Ouvert)* | La métrique positive ne suit pas de la reconstruction |  |
| IDE-046 Fluctuation arithmétique signée *(Démontré)* | ⊣ | IDE-051 Loi de signe de la famille *(Ouvert)* | Payer la dette réelle à toutes les échelles |  |
| IDE-047 Dette des couplages *(Acquis partiel)* | ⊣ | IDE-051 Loi de signe de la famille *(Ouvert)* | Contrôler les couplages de la famille choisie |  |
| IDE-049 Transport et réserve *(Acquis partiel)* | ⊣ | IDE-051 Loi de signe de la famille *(Ouvert)* | Réserve et résidu pour toutes les lignes |  |
| IDE-056 Énergie J *(Classique (cité))* | ⊣ | IDE-057 Borne de force RH *(Ouvert)* | Majoration indépendante à toute échelle |  |
| IDE-060 Diagonale et petits conducteurs *(Démontré)* | ⊣ | IDE-061 Grands conducteurs signés *(Ouvert)* | Le reste ne disparaît pas |  |
| IDE-055 Corrélations ancrées *(Démontré)* | ⊣ | IDE-051 Loi de signe de la famille *(Ouvert)* | L’ancrage est nécessaire à la stratégie, pas une preuve du signe |  |

### ⇏ insuffisant — « ne suffit pas pour » (3)

| Origine | | Cible | Contenu | Garde |
|--------------|--|--------------|--------------|------|
| IDE-043 Fibres, jets et pli choisi *(Démontré)* | ⇏ | IDE-051 Loi de signe de la famille *(Ouvert)* | Un pli choisi ne donne pas le signe global |  |
| IDE-048 Lego local : S ≤ 11/20 *(Démontré)* | ⇏ | IDE-051 Loi de signe de la famille *(Ouvert)* | Le plafond 11/20 ne couvre pas tous les supports |  |
| IDE-062 Étape conditionnelle : 3/4 *(Conditionnel)* | ⇏ | IDE-057 Borne de force RH *(Ouvert)* | Exposant 5/2 encore au-dessus de 2 |  |

### ✕ obstruction — « bloque une méthode vers » (8)

| Origine | | Cible | Contenu | Garde |
|--------------|--|--------------|--------------|------|
| IDE-016 TOMO-3 brut *(Diagnostic)* | ✕ | IDE-055 Corrélations ancrées *(Démontré)* | Le rejet du bispectre brut ne ferme pas l’ancrage |  |
| IDE-038 Schrödinger, Heff *(Obstruction)* | ✕ | IDE-042 Hilbert–Pólya *(Ouvert)* | Une reparamétrisation ne fournit pas la métrique |  |
| IDE-063 Crible générique : perte des copies *(Obstruction)* | ✕ | IDE-061 Grands conducteurs signés *(Ouvert)* | Exiger une propriété spécifique de μ(q) et B |  |
| IDE-020 V6.4Seuil τ_c *(Obstruction)* | ✕ | IDE-023 V6.7Marges de la forme et de l'objet *(Mesuré)* | Seuil dépendant de la fenêtre |  |
| IDE-007 Densité de zéros *(Obstruction)* | ✕ | IDE-058 Borne de l’énergie initiale Q *(Ouvert)* | Le cadre ancien ne donne pas de gain |  |
| IDE-064 Surface et Frobenius virtuels *(Acquis partiel)* | ✕ | IDE-065 Transplantation directe de Stepanov *(Obstruction)* | La transplantation directe étudiée est insuffisante |  |
| IDE-069 Norme de la partie première seule *(Obstruction)* | ✕ | IDE-044 P, moments et domaines *(Démontré)* | Contrôler la forme complète dans le domaine requis |  |
| IDE-069 Norme de la partie première seule *(Obstruction)* | ✕ | IDE-047 Dette des couplages *(Acquis partiel)* | Ne pas payer le couplage par une norme divergente |  |

### ≡ critere — « énonce le critère de » (2)

| Origine | | Cible | Contenu | Garde |
|--------------|--|--------------|--------------|------|
| IDE-002 Théorème A *(Démontré)* | ≡ | IDE-058 Borne de l’énergie initiale Q *(Ouvert)* | Énonce la borne équivalente, sans la prouver |  |
| IDE-013 Dimension énergétique / fractal strings *(Outil)* | ≡ | IDE-058 Borne de l’énergie initiale Q *(Ouvert)* | Dimension et croissance, même borne manquante |  |

### ⚠ temoin — « témoin contraire pour » (2)

| Origine | | Cible | Contenu | Garde |
|--------------|--|--------------|--------------|------|
| IDE-005 Davenport–Heilbronn *(Obstruction)* | ⚠ | IDE-014 DARK-ZETA *(Outil)* | Témoin adversarial conservé |  |
| IDE-067 Certificat négatif de DH *(Démontré)* | ⚠ | IDE-051 Loi de signe de la famille *(Ouvert)* | Tester les arguments qui prétendent imposer le signe |  |

### ? hypothese — « hypothèse de travail vers » (2)

| Origine | | Cible | Contenu | Garde |
|--------------|--|--------------|--------------|------|
| IDE-036 L'objet qui porte la métrique *(Ouvert)* | ? | IDE-051 Loi de signe de la famille *(Ouvert)* | Structure imposant le signe à construire |  |
| IDE-064 Surface et Frobenius virtuels *(Acquis partiel)* | ? | IDE-036 L'objet qui porte la métrique *(Ouvert)* | Une structure globale imposant le signe reste à construire |  |

### ↺ reouverture — « rouvre » (2)

| Origine | | Cible | Contenu | Garde |
|--------------|--|--------------|--------------|------|
| IDE-008 Arrêt de l'attaque directe *(Obstruction)* | ↺ | IDE-046 Fluctuation arithmétique signée *(Démontré)* | Nouvelle obligation arithmétique discriminante |  |
| IDE-065 Transplantation directe de Stepanov *(Obstruction)* | ↺ | IDE-066 Lemme des jets et relief *(Démontré)* | Des conditions de réouverture exigent des objets définis |  |

### ∼ relation — « éclaire » (15)

| Origine | | Cible | Contenu | Garde |
|--------------|--|--------------|--------------|------|
| IDE-011 Nyman–Beurling *(Classique (cité))* | ∼ | IDE-002 Théorème A *(Démontré)* | Projection étudiée ramenée à Q |  |
| IDE-012 Critère de Li *(Classique (cité))* | ∼ | IDE-001 Lemmes 1 à 5 *(Démontré)* | Constante commune ; pas tous les signes de Li |  |
| IDE-006 Corps de fonctions *(Mesuré)* | ∼ | IDE-022 V6.6Le Modèle réduit *(Mesuré)* | Modèle où la positivité est démontrée |  |
| IDE-017 PRIME-LOCK *(Outil)* | ∼ | IDE-018 DUAL-LOCK *(Outil)* | Détecteurs locaux et globaux distincts |  |
| IDE-019 Résidu sombre *(Outil)* | ∼ | IDE-047 Dette des couplages *(Acquis partiel)* | Normalisation par le vrai Gram |  |
| IDE-023 V6.7Marges de la forme et de l'objet *(Mesuré)* | ∼ | IDE-045 Changement de métrique *(Démontré)* | Forme positive et marge sont distinctes |  |
| IDE-030 V6.16La Rencontre à trois *(Démontré)* | ∼ | IDE-043 Fibres, jets et pli choisi *(Démontré)* | Une identité de marge ne certifie pas toutes les collisions |  |
| IDE-031 V6.17La Rencontre en degré 2 *(Mesuré)* | ∼ | IDE-029 V6.15Le degré 2 et le recensement *(Mesuré)* | Même instrument, cadre de degré 2 |  |
| IDE-028 V6.14Le temps de Heisenberg *(Mesuré)* | ∼ | IDE-026 V6.10Le générateur des premiers *(Mesuré)* | Loi de détection, pas loi de signe |  |
| IDE-021 V6.5Famille modulo 7 *(Mesuré)* | ∼ | IDE-024 V6.8L'Archipel d'Euler *(Démontré)* | Îles observées et rigidité déclarée |  |
| IDE-027 V6.11La base comme pas de temps *(Mesuré)* | ∼ | IDE-025 V6.9Le chaînon F = q^D *(Mesuré)* | Discret et continu |  |
| IDE-054 Identité des vrais coefficients *(Classique (cité))* | ∼ | IDE-046 Fluctuation arithmétique signée *(Démontré)* | Deux descriptions des vrais poids |  |
| IDE-040 Positivité de Weil *(Ouvert)* | ∼ | IDE-051 Loi de signe de la famille *(Ouvert)* | Même exigence de signe ; pas de coercivité uniforme |  |
| IDE-015 TOMO-2 *(Outil)* | ∼ | IDE-014 DARK-ZETA *(Outil)* | Perte de phase dans les observables de puissance |  |
| IDE-068 La Rencontre à n *(Mesuré)* | ∼ | IDE-047 Dette des couplages *(Acquis partiel)* | Les interactions motivent un contrôle des couplages |  |

### ⚙ outil — « outil pour » (5)

| Origine | | Cible | Contenu | Garde |
|--------------|--|--------------|--------------|------|
| IDE-032 V6.18Le registre des sources *(Outil)* | ⚙ | IDE-009 Relecture externe de A et B *(Ouvert)* | Sources et périmètre de relecture |  |
| IDE-034 Indicateur d'avancement *(Outil)* | ⚙ | IDE-035 Navigateur de recherche *(Outil)* | Position et critères de réévaluation |  |
| IDE-035 Navigateur de recherche *(Outil)* | ⚙ | IDE-033 Prochain coup *(Outil)* | Choix recalculés |  |
| IDE-033 Prochain coup *(Outil)* | ⚙ | IDE-051 Loi de signe de la famille *(Ouvert)* | Les investigations visent cette obligation, sans la supposer vraie |  |
| IDE-009 Relecture externe de A et B *(Ouvert)* | ⚙ | IDE-002 Théorème A *(Démontré)* | Relecture de la preuve et de ses conditions |  |
