# Roadmap history — programme RH

Version : **v4.3 — 2026-10-04**

Ce document sert de carte unique du programme. Il ne cherche pas à embellir la trajectoire : il indique, pour chaque phase, **l'idée**, **ce qu'elle a effectivement apporté**, **le statut actuel**, et **la raison du maintien, de la rétrogradation ou de l'abandon**.

## 0. Principe directeur actuel

Le programme n'est plus organisé autour de l'objectif vague « pousser jusqu'à RH ». La règle actuelle est :

1. verrouiller les identités et équivalences exactes ;
2. distinguer les reformulations équivalentes à RH des vrais gains analytiques ;
3. tester chaque nouvelle idée sur des benchmarks où l'on connaît déjà la réponse ;
4. abandonner toute route qui ne distingue pas zêta d'un modèle sans produit d'Euler ou qui ne reproduit aucune borne inconditionnelle connue ;
5. n'envisager une attaque directe de RH qu'après avoir démontré que le formalisme transporte réellement de l'information analytique nouvelle.

Le statut central est désormais :

\[
\frac12\limsup_{X\to\infty}\frac{\log Q(X)}{\log X}=\Theta-\frac12,
\qquad
\Theta=\sup_\rho \Re\rho.
\]

Ainsi `Q(X)=X^{o(1)}` est **équivalent à RH**. Toute preuve de cette cible serait déjà une preuve de RH ; ce n'est donc pas un « lemme intermédiaire ».

---

## 1. Phase Nyman–Beurling / Báez-Duarte

### Idée

Utiliser le critère de Nyman–Beurling : approcher `χ_(0,1)` dans `L²(0,1)` par des combinaisons de dilatations de la partie fractionnaire. Pour une famille finie, écrire explicitement le problème comme une projection dans un espace de Gram.

### Résultats obtenus

- Formulation matricielle exacte de la distance finie.
- Calculs numériques des distances optimales.
- Identification d'une structure de Gram logarithmique après renormalisation.
- Vérification que les constantes observées sont compatibles avec la constante classique
  \[
  \kappa=2+\gamma_E-\log(4\pi).
  \]

### Ce que cela a appris

Le critère est un excellent **coordinateur** du problème, mais la difficulté se déplace vers l'inversion d'un Gram presque singulier ou vers le contrôle de coefficients arithmétiques. Il ne produit pas à lui seul un mécanisme nouveau.

### Statut

**Conservé comme cadre fonctionnel.** Pas considéré comme une route indépendante vers RH.

---

## 2. Phase opérateur / dissipateur / Krylov / observabilité

### Idée

Encoder l'approximation dans un opérateur positif `S=A*A`, puis étudier noyau, résolvante, régularisation de Tikhonov et espaces de Krylov. Chercher une condition d'observabilité qui forcerait la composante « sombre » à disparaître.

### Résultats obtenus

- Reformulations exactes de la condition RH dans des termes opératoriels.
- Bornes numériques de Krylov convaincantes à petite taille.
- Identification de la bonne forme d'observabilité : contrôler `|<χ,f>|` par une combinaison de `||f||` et `||Af||`.

### Pourquoi la route a été rétrogradée

Les conditions spectrales positives seules perdent précisément la composante de noyau qu'il faudrait exclure. Une condition suffisamment forte pour fermer l'argument réintroduit RH sous une forme équivalente.

### Statut

**Rétrogradé en langage structurel.** Utile pour comprendre la géométrie, pas comme source actuelle de gain analytique.

---

## 3. Phase mollificateurs Möbius et apodisation

### Idée

Construire explicitement des approximants de `1/ζ(s)` par des polynômes de Dirichlet Möbius pondérés, avec fenêtres lisses contrôlant à la fois biais local et fuite spectrale.

### Résultats obtenus

- Familles de fenêtres bêta et polynomiales.
- Identités exactes pour les coefficients intérieurs en termes de convolutions de `Λ`.
- Mise en évidence du compromis : améliorer le biais local augmente la fuite.
- Lien avec les méthodes de polynômes de Dirichlet longs et les estimations Type I/II.

### Route à plateau long

Une fenêtre égale à `1` sur une longue zone semblait permettre une forte suppression de bord. L'analyse exacte a révélé un terme de résidu `M_N(1)` qui doit lui-même être de taille presque RH pour que la construction marche.

### Décision

**Fenêtre à plateau abandonnée comme route directe.** Elle déplace le verrou au lieu de le supprimer.

---

## 4. Phase Type I/II, grand crible et intervalles courts

### Idée

Utiliser les progrès récents sur Möbius/Liouville dans les intervalles courts et les sommes Type I/II pour contrôler la fuite des mollificateurs ou les corrélations hyperboliques.

### Résultats obtenus

- Traduction précise des longueurs de facteurs et des seuils nécessaires.
- Identification du fait que, dans plusieurs régimes du programme, la structure naturelle est Type I plutôt que Type II.
- Vérification que les résultats disponibles donnent souvent des économies logarithmiques ou des gains de puissance trop faibles pour atteindre l'échelle racine carrée requise.

### Diagnostic

La difficulté n'est pas l'absence totale de cancellation, mais l'écart entre `H/log^A` et `sqrt(H)·polylog` dans la norme pertinente.

### Statut

**Suspendu sans nouvel ingrédient.** Toute nouvelle utilisation devra annoncer à l'avance le gain d'exposant visé.

---

## 5. Phase fenêtre compensée et extraction de l'observable `c(n)`

### Idée

Optimiser des fenêtres polynomiales de petite dimension. Les calculs ont montré qu'un paramètre proche de `1` annule le biais dominant associé à `s=1`.

### Résultat conceptuel majeur

Extraction de la suite arithmétique indépendante de `N`

\[
c(n)=(\Lambda*\Lambda)(n)-\Lambda(n)\log n+2\gamma_E\Lambda(n),
\]

avec série de Dirichlet

\[
G(s)=q(s)^2+q'(s)+2\gamma_E q(s),
\qquad q=-\zeta'/\zeta.
\]

### Propriétés obtenues

- `G` est régulière en `s=1`.
- Si `ρ` est un zéro de multiplicité `m`, `G` a un double pôle principal
  \[
  \frac{m(m+1)}{(s-\rho)^2}.
  \]
- `c(n)` est très parcimonieuse : support sur les entiers ayant au plus deux facteurs premiers distincts.

### Statut

**Conservé.** C'est l'un des objets les plus propres produits par le programme.

---

## 6. Phase énergie `Q(X)` et exposant spectral

### Définition

\[
C(x)=\sum_{n\le x}c(n),
\qquad
Q(X)=\int_1^X\frac{|C(x)|^2}{x^2}\,dx.
\]

### Résultats

- Transformée de Laplace/Mellin exacte de `C` vers `G(s)/s`.
- Relation entre croissance de `Q` et position des pôles de `G`.
- En v3, fermeture rigoureuse de
  \[
  \frac12\limsup\frac{\log Q(X)}{\log X}=\Theta-\frac12.
  \]

### Conséquence méthodologique

`Q(X)=X^{o(1)}` est exactement RH. De même, tout gain fixe

\[
Q(X)\ll X^{1-\delta}
\]

donnerait déjà une bande sans zéro fixe, résultat majeur inconnu.

### Décision

**Ne plus présenter `Q(X)=X^{o(1)}` comme un palier.** `Q` devient une jauge exacte de la difficulté horizontale.

---

## 7. Phase factorisation Möbius / parties fractionnaires

### Idée

Définir

\[
a(n)=\mu(n)\big((\log n)^2-2\gamma_E\log n\big).
\]

Alors

\[
c=1*a,
\qquad
\sum_{n\ge1}\frac{a(n)}n=0.
\]

### Apport

Le moment nul explique l'annulation du mode cohérent principal. On obtient aussi une réécriture de `C(x)` en somme de parties fractionnaires et un lien exact avec Nyman–Beurling.

### Ce qui a été appris

La très forte annulation numérique entre partie diagonale et énergie complète n'est pas une surprise « RH » : une large part est forcée par la régularité exacte en `s=1` et par le moment nul.

### Statut

**Conservé comme structure arithmétique de base.** Les résultats numériques seuls ne sont plus interprétés comme évidence pour RH.

---

## 8. Phase Fourier locale / phases réciproques

### Idée

Après décomposition hyperbolique, réduire la queue critique à des sommes de type

\[
\sum_{n\asymp N}\mu(n)P(\log n)e(hx/n).
\]

Développer le carré et interpréter l'intégration en `x` comme une énergie Fourier locale de Möbius.

### Résultat

Le régime extrême conduit à une « Parseval locale » à l'échelle `1/N`. Une telle borne uniforme serait assez forte pour impliquer des estimations de type racine carrée pour Mertens.

### Décision

**Rétrogradé.** La version uniforme semble être RH déguisée. Conserver seulement comme diagnostic fréquentiel.

---

## 9. Phase GPS / Kalman analytique

### Idée

Traiter chaque échelle comme une mesure avec variance et covariance ; calculer l'innovation, le gain optimal et la variance posteriori, comme dans un filtre de Kalman / filtre d'information.

### Résultats

- Compléments de Schur exacts pour la réduction de variance.
- Covariance exacte des dents de scie
  \[
  \langle\psi_d,\psi_e\rangle=\frac{\gcd(d,e)^2}{12de}.
  \]
- Factorisation par les canaux de diviseurs via `J_2`.
- Réductions numériques réelles de variance quand plusieurs échelles sont combinées.

### Limite révélée par les données

L'information normalisée `info_per_logX` ne montre aucune loi stable de type constante positive. Les gains numériques ne prouvent donc aucune accumulation asymptotique suffisante.

### Décision

**Conserver comme outil de diagnostic/covariance, suspendre comme route de preuve.**

---

## 10. Phase canaux terminaux `H_∞(q)`

### Idée

Pour chaque canal arithmétique `q`, calculer la destination exacte de la somme harmonique Möbius au lieu de seulement mesurer son résidu.

### Résultat

Pour `q` sans carré,

\[
H_\infty(q)
=-\frac{2\mu(q)}{\varphi(q)}
\sum_{p\mid q}\frac{p\log p}{p-1}.
\]

La preuve courte utilise

\[
\Phi_q(s)=\frac{\mu(q)h_q(s)}{\zeta(s)},
\qquad
h_q(s)=\prod_{p\mid q}(p^s-1)^{-1},
\]

et les termes en `γ_E` s'annulent exactement.

### Apport

Le « GPS analytique » possède une destination exacte par canal. Le sous-problème restant est la variance pondérée de la queue vers cette destination.

### Statut

**Conservé comme identité rigoureuse et sous-problème possible**, mais pas encore comme mécanisme de gain d'exposant.

---

## 11. Phase formule explicite et calibration numérique

### Idée

Comparer `Q(X)` et `B(t)` calculés directement à la formule explicite construite avec les premiers zéros de `ζ`.

### Résultats v2/v3

- 300 zéros utilisés.
- Calcul de `c_0(ρ)=ζ''(ρ)/(2ζ'(ρ))`.
- Inclusion des termes d'ordre `L²` et `L`, pas seulement du terme principal `(4κ/3)L³`.
- Accord numérique de `Q` à quelques pourcents jusqu'à `X=4·10^6`.
- Corrélation de `B(t)` d'environ `0.976`.

### Interprétation correcte

Ces calculs valident les identités, les normalisations et le code **dans la plage accessible**. Ils ne testent pas RH : un zéro hors droite à une hauteur inaccessible resterait invisible.

### Décision

**Conserver comme calibration de code, pas comme argument probabiliste pour RH.**

---

## 12. Tests de rejet introduits en v3

### Davenport–Heilbronn

Une équation fonctionnelle de type Riemann sans produit d'Euler peut coexister avec des zéros hors droite. La partie analytique « pôles ↔ croissance d'énergie » est donc générique.

**Exigence :** toute future idée de preuve doit utiliser irréversiblement une structure issue du produit d'Euler (`Λ`, `μ`, parcimonie de `c`, canaux multiplicatifs) et échouer pour le modèle Davenport–Heilbronn.

### Corps de fonctions / Weil

La preuve de Weil contient une positivité géométrique profonde. Les positivités actuelles du programme (normes `L²`, Gram, Schur) sont génériques.

**Exigence :** identifier un analogue arithmétique réellement spécifique, sinon le test n'est pas passé.

### Benchmark inconditionnel

Un cadre crédible doit au moins reproduire une borne connue de densité de zéros ou une région sans zéro à partir d'outils standards.

---

## 13. Phase actuelle : calibration spectrale `Q(X,T)`

### Motivation

Le scalaire `Q(X)` compresse presque toute l'information en `sup Re ρ`. Pour mesurer une densité de zéros, il faut conserver aussi la hauteur `γ`.

### Objet actuel

La v3 introduit une énergie spectrale fenêtrée à deux paramètres, notée génériquement

\[
Q(X,T)
\]

ou, dans la version la plus générale du package,

\[
Q_{w,W}(L;T,\Delta).
\]

### Objectif

Ne **pas** chercher d'abord RH. Chercher à démontrer que, lorsqu'on injecte des estimations standards de polynômes de Dirichlet, l'observable redonne une borne de densité de zéros déjà connue, même avec pertes.

### Benchmark

Comparer au minimum aux bornes classiques et, comme référence moderne, à Guth–Maynard.

### Critère de réussite

Le formalisme doit transformer une information quantitative sur les polynômes de Dirichlet en une borne quantitative sur

\[
N(\sigma,T).
\]

S'il n'y arrive pas, il est trop compressé pour être une voie crédible vers RH.

---

## 14. Étape suivante si la calibration réussit : familles de caractères

### Objet

Définir

\[
Q_\chi(X,T)
\]

pour `L(s,χ)` et moyenner sur les caractères.

### Pourquoi

Dans ce cadre, le grand crible et les théorèmes de densité de familles sont disponibles inconditionnellement. Cela fournit un banc d'essai réel : si le formalisme est sain, il doit pouvoir retrouver au moins un exposant connu à partir de ces outils.

### Décision conditionnelle

**Ne passer à cette phase que si `Q(X,T)` réussit le benchmark de densité.**

---

## 15. Théorème conditionnel parallèle à rédiger

Sous RH et simplicité des zéros, viser une rédaction propre de

\[
Q(e^L)=\frac{4\kappa}{3}L^3+\alpha L^2+\beta L+o(L),
\]

avec contrôle rigoureux des termes hors diagonale avant de revendiquer `α` et `β`.

Ce résultat ne prouverait pas RH, mais constituerait un livrable mathématique autonome et vérifierait la cohérence spectrale de l'observable.

---

## 16. Règle d'arrêt actuelle

Le programme doit être **arrêté comme attaque directe de RH** si les deux faits suivants persistent :

1. aucune étape ne distingue réellement zêta d'un analogue Davenport–Heilbronn sans produit d'Euler ;
2. `Q(X,T)` ne permet de redémontrer aucune borne non triviale de densité de zéros avec des outils standards.

Dans ce cas, le contenu publiable resterait :

- les identités et équivalences rigoureuses ;
- la formule terminale des canaux ;
- la calibration conditionnelle par formule explicite ;
- les diagnostics numériques et les tests de rejet.

---

## 17. Carte synthétique

```text
Nyman–Beurling
      |
      v
Gram / opérateurs / Krylov
      |              \
      |               -> rétrogradé (pas de gain analytique)
      v
Mollificateurs Möbius / fenêtres
      |
      +--> plateau long --------> abandonné (résidu M_N(1))
      |
      v
Fenêtre compensée
      |
      v
c(n), G(s), C(x), Q(X)
      |
      +--> Q=X^{o(1)} ----------> équivalent à RH, plus un palier
      |
      +--> factorisation Möbius / canaux / H_inf
      |         |
      |         +--> GPS/Kalman -> diagnostic seulement
      |
      +--> Fourier locale ------> version uniforme ~ RH déguisée
      |
      v
L6 : exposant de Q = distance horizontale des zéros
      |
      v
Tests de rejet : Davenport–Heilbronn / Weil / benchmark connu
      |
      v
Q(X,T) : conserver hauteur + position horizontale
      |
      +--> échec densité connue --> arrêter attaque directe RH
      |
      +--> succès
             |
             v
       Q_chi(X,T) + grand crible
             |
             v
       seulement alors chercher un gain nouveau
```

## 18. Lecture recommandée du package

Pour reconstruire le projet rapidement :

1. `README.md` — position scientifique actuelle ;
2. **ce fichier** — chronologie et décisions ;
3. `docs/LEMMES_RIGOUREUX.md` — ce qui est démontré ;
4. `KNOWN_GAPS.md` — ce qui ne l'est pas ;
5. `docs/PRIORITES.md` — ordre de travail ;
6. `docs/DAVENPORT_HEILBRONN_TEST.md` et `docs/CALIBRATION_SPECTRALE.md` — tests actuels ;
7. `CHANGELOG.md` — détail des versions ;
8. `REPORT_FR.md` — rapport long et historique mathématique.

---

## 10. Phase banc de rejet, localisation et bibliographie (v3.2)

### Idée
Exécuter les tests de rejet plutôt que les décrire, et situer le programme dans la littérature
Nyman–Beurling avant toute revendication.

### Résultats obtenus
- Définition exécutable de Davenport–Heilbronn, équation fonctionnelle vérifiée ; pipeline G→c→Q
  générique validé sur ζ (écart 10⁻¹³).
- Q détecte la couche générique (zéros hors droite) : pente 0,56 pour DH contre ≈ 0,33 pour ζ et L(s,χ₅).
- L'observable spectrale localise les zéros de ζ en hauteur (18 pics sur 20 à < 0,5 d'un zéro).
- κ identifié comme constante de Burnol/Bettin–Conrey–Farmer ; L8 et L7 restent [À VÉRIFIER] en nouveauté.
- Correction : α et β (GAP-3) ne sont pas confirmables numériquement.

### Ce que cela a appris
Les tests passés sont des tests de *cohérence* ; aucun ne met à l'épreuve une inégalité candidate,
car il n'y en a pas. Le cadre reste une reformulation de RH.

### Statut
**Conservé comme instrument de diagnostic.** Règle d'arrêt P2 inchangée.

---

## 11. Tableau d'activités (Claude) — état au 2026-10-03 (v3.3)

| # | Activité | Livrable | État |
|---|---|---|---|
| 1 | Positionnement bibliographique NB / Báez-Duarte / Burnol / BCF | `docs/BIBLIO_POSITIONNEMENT.md` | **Fait** (2 lignes [À VÉRIFIER] : L8, nouveauté de L7) |
| 2 | Banc de rejet exécutable (ζ, L, DH) | `src/rejection.py`, `scripts/run_rejection.py`, `docs/DAVENPORT_HEILBRONN_TEST.md` | **Fait** |
| 2b | Localisation spectrale de Q_{w,W} | `scripts/run_localisation.py` | **Fait** (18 pics sur 20) |
| 3 | Preuve du terme dominant (4κ/3)L³ sous RH (Plancherel de Mellin + analyse locale + Tauber) | `docs/THEOREME_TERME_DOMINANT.md`, `scripts/run_abelian_check.py` | **Fait** (sans hypothèse de simplicité ; modulo faits classiques F1–F5 ; non relu par un tiers) |
| 4 | Mémo go/no-go P2.3 | `docs/MEMO_P2_3_DENSITE.md` | **Fait** : NO-GO pour une densité nouvelle ; SNR des raies ∝ 1/γ² mesuré (plancher de bruit 6 691) |
| 5 | Mémo P2.2 : positivité de Weil vs Q | `docs/MEMO_P2_2_WEIL.md`, `scripts/run_function_field_analog.py` | **Fait** : NO-GO ; aucun des trois ingrédients (rationalité, tour, Hodge) n'a d'image dans Q |
| 6 | Comparaison avec Bettin–Conrey–Farmer | `docs/COMPARAISON_BCF.md`, test d'identité, `scripts/run_gonek_moment.py` | **Fait (analytique)** ; reproduction numérique de d_N² reportée (→ 8) |
| 7 | Compléter les zéros de DH (t ≤ 200) | `data/dh_zeros.csv` | **Fait** : 125 pour ≈ 129,5 attendus ; aucun σ > 1 jusqu'à t = 200 |
| 8 | Matrice de Gram NB via ∫₁^∞{y/a}{y/b}y⁻²dy et queue gcd²/(12ab) pour reproduire d_N² log N → κ | `src/nyman_beurling.py`, `scripts/run_nb_gram.py`, `docs/NB_GRAM.md` | **Fait** (d_N² log N = 1,07 κ à N=20–30, au-dessus de κ ; E(V_N) log N encore ≈ 15 κ à N=200 : pas de confirmation asymptotique) |
| 9 | Contrôle des termes en L² et L (α, β) | `docs/ALPHA_BETA_ANALYSE.md`, `scripts/run_alpha_beta.py` | **Fait (analyse)** : coefficients η⁻³, η⁻², η⁻¹ confirmés à 4 chiffres sur le modèle local ; **α, β ne sont pas ponctuels** (Φ(L) presque périodique, ±0,03). Passage à ζ conditionnel à (H1)–(H3) |

**Ordre proposé** : plus d'activité P2 en attente ; décision de pivot (§16) (puis, si utile, étendre l'optimum de d_N² à N=50–100). Règle d'arrêt inchangée : si 4 et le test de rejet d'une
inégalité candidate échouent, limiter le projet à P0/P1.

## 12. Phase comparaison BCF (v3.3)

### Idée
Situer le programme face au résultat le plus proche de la littérature (Bettin–Conrey–Farmer 2013).

### Résultats obtenus
- Dictionnaire exact : BCF travaille au premier ordre (1−ζV_N ≈ −q/log N, identité vérifiée sur les
  coefficients), le programme au second ordre (G = q²+q'+2γq). Même mécanique de zéros, même constante κ.
- Les coefficients α, β de GAP-3 font intervenir 1/ζ'(ρ) : ils convergent sous les mêmes hypothèses que BCF
  (esquisse [STD]) ; le moment de Gonek est numériquement cohérent (ratio 0,976 à T ≈ 542, exposant 0,915).

### Statut
**Conservé comme positionnement.** Aucune revendication de nouveauté sur κ.

## 13. Phase théorème du terme dominant (v3.4)

### Idée
Remplacer le diagnostic numérique « (4κ/3)L³ » par un énoncé démontré, par la route de Cramér :
Mellin–Plancherel sur la droite Re s=½+η, analyse locale aux doubles pôles, puis Tauber.

### Résultats obtenus
- Théorème : sous RH, Q(X) ∼ (S/3)(log X)³, S=Σ m²(m+1)²/|ρ|² ; 4κ/3 pour des zéros simples.
  La simplicité n'est pas nécessaire.
- Le niveau abélien est confirmé numériquement à η=0,2 (écart 4 % sur η³Q_η avec α,β calculés sur 300 zéros).
- La preuve éclaire GAP-3 : les termes en L², L correspondent à η⁻², η⁻¹ de I(η) et exigent un contrôle fin
  des termes croisés, que Tauber ne donne pas.

### Statut
**Conservé : résultat conditionnel à RH**, de valeur d'exactitude (analogue de Cramér), non de nouveauté.

## 14. Phase Gram de Nyman–Beurling (v3.5)

### Idée
Reproduire numériquement d_N² log N → κ par un calcul exact du produit scalaire de Nyman–Beurling, au lieu
d'intégrer ζ sur la droite critique (queue trop lourde).

### Résultats obtenus
- Gram exacte à ~10⁻¹² (G(1,1)=log 2π−γ ; dictionnaire de Mellin validé à 0,05 % et 0,6 %).
- d_N² optimal : d_N² log N = 0,058 / 0,055 / 0,049 / 0,049 pour N=5/10/20/30, au-dessus de κ=0,0462 (rapport 1,07 à N=20–30).
- E(V_N) log N = 0,71 à N=200 : l'asymptotique de BCF n'est pas encore atteinte.

### Statut
**Conservé comme outil de calibration.** Ne teste pas RH ; confirme la cohérence de la constante κ avec la littérature.

## 15. Phase termes d'ordre inférieur (v3.6)

### Idée
Obtenir α et β par le développement de I(η), dans le cadre de la preuve du théorème.

### Résultats obtenus
- Le coefficient de η⁻² est exactement s₂ (= α/2) et celui de η⁻¹ est s₁ (= β/2) : dérivation locale indépendante de la
  formule explicite, confirmée à 4 chiffres (0,2327 contre 0,2328) sur un modèle à 300 zéros.
- **Correction de fond** : le coefficient de L² dans U(L) n'est pas constant mais α+Φ(L), Φ presque périodique
  (amplitude ≈ ±0,03, corrélation 0,996 avec l'écart mesuré). Un développement ponctuel en puissances de L est faux ; cela explique
  l'instabilité des ajustements libres de α,β.
- Passage à ζ : hypothèses (H1)–(H3) explicitées, dont le contrôle des paires de zéros proches (hors de portée de RH seule).

### Statut
**Conservé : analyse conditionnelle, avec GAP-3 reformulé.** Un énoncé corrigé remplace l'ancien.

## 16. Phase décision P2 (v3.7)

### Résultats
- **P2.1 (Davenport–Heilbronn)** : couche générique confirmée ; localisation du produit d'Euler dans la parcimonie de c (L3), non exploitée.
- **P2.2 (Weil)** : NO-GO. Q est le carré de la formule explicite, sa positivité est de type Parseval (automatique) ; la positivité de Weil porte sur un signe
  qui n'existe pas dans Q. Le test numérique corps de fonctions montre que Q enregistre la croissance après coup (a=25 → exponentiel) sans pouvoir exclure a=25 ;
  seule la géométrie (10 100 courbes sur F_101, max|a|=20) l'exclut.
- **P2.3 (densité)** : NO-GO. Les trois routes se ramènent à des grandes valeurs de polynômes de Dirichlet à coefficients bornés ; SNR des raies ∝ 1/γ².

### Règle d'arrêt
Les tests 2 et 3 de P2 échouent ; le test 1 ne distingue pas le cadre. **La règle d'arrêt est déclenchée** : cesser l'attaque directe de RH par ce cadre.

### Plan de repli (P0/P1)
1. Rédiger la note : L6 (équivalence exposant ⇔ Θ, inconditionnelle), L7, L10, théorème du terme dominant (conditionnel à RH), analyse α/β avec Φ(L).
2. Positionner le tout dans la littérature NB (BIBLIO_POSITIONNEMENT, COMPARAISON_BCF, NB_GRAM) en tant que cadre de calibration.
3. Faire relire les preuves L6 et du théorème par un tiers.
4. Optionnel : étendre d_N² à N=50–100 ; vérifier les deux lignes [À VÉRIFIER] de la bibliographie.

## 17. Phase plan optionnel (v3.8)

### Réalisé
1. **Extension de d_N² à N=100** : d_N² log N entre 1,005 κ et 1,042 κ pour N=40…100, non monotone (oscillations ±2 %). Stabilité 10⁻¹⁰.
2. **Vérification bibliographique** : L8 = formule de Franel (1924) démontrée par Landau (1924) → aucune nouveauté revendiquée ; L7 = corollaire élémentaire d'une identité standard.

### Reste [À VÉRIFIER]
Lien exact L8 ↔ A(λ)/Vasyunin ; antériorité du théorème du terme dominant ; critère de Weil et Halász–Montgomery cités de mémoire.

### Prochaine étape (plan de repli P0/P1)
Rédiger la note de synthèse ; faire relire L6 et le théorème par un tiers.

## 18. Phase synthesis note (v3.9)

### Réalisé
Note de synthèse en anglais (`docs/SYNTHESIS_NOTE_EN.md`, ≈2 700 mots) : lemmes 1–5, théorème A (équivalent à RH), théorème B (conditionnel à RH), proposition C (structure Φ(L)), pont Nyman–Beurling, tableau des vérifications numériques, trois tests d'étalonnage et décision d'arrêt, tableau de statut, drapeaux de vérification.

### Reste
Relecture par un tiers des théorèmes A et B ; vérification des points [À VÉRIFIER] listés au §10 de la note.


## 19. Phase V4.1 — traitement de signal / localisation de sources

### Origine
Transposition explicite des méthodes de localisation de sources utilisées pour les potentiels évoqués : moyennage préalable, filtres multirésolution, Laplacien régularisé, ondelettes, covariance et inversion linéaire.

### Formulation
La formule explicite est traitée comme un modèle direct où un zéro `rho=beta+i gamma` engendre le mode `exp((beta-1/2)t) exp(i gamma t)`. RH correspond à l'absence de sources à croissance positive `beta>1/2`.

### Réalisé
- `src/source_localization.py` ;
- carte matched-filter / GLS `P(beta,gamma)` ;
- enveloppe Morlet et estimation de croissance ;
- Laplacien régularisé ;
- métriques de visibilité par valeurs singulières ;
- démonstrateur synthétique récupérant une source injectée `(0.60,21)` et une croissance ≈0.10 ;
- 3 tests nouveaux, total 24/24.

### Positionnement littérature
Harmonic inversion / filter diagonalization sur zeta existe déjà (Main et al. 1997) ; la formule de Guinand–Weil fournit déjà un filtrage rigoureux par fonctions tests ; Connes fournit une lecture spectrale/absorption. L'élément éventuellement distinct est la combinaison systématique multicanal + covariance + localisation `(beta,gamma)` + test d'observabilité uniforme. Nouveauté non revendiquée.

### Verrou
Une carte finie ne teste pas RH. Il faudrait une constante d'observabilité uniforme pour toute source hors ligne. Statut : **branche expérimentale, pas voie de preuve active**.


## V4.2 — Schrödinger / flux (2026-10-04)

**Idée.** Interpréter le temps logarithmique comme temps d'évolution : `rho=beta+i gamma` donne le mode `exp((beta-1/2)t)exp(i gamma t)` et l'énergie complexe `E=-gamma+i(beta-1/2)`. Utiliser l'équation de continuité pour distinguer flux de bord et source interne.

**Apport.** Unifie la localisation de sources V4.1, Hilbert–Pólya et une lecture système ouvert/résonance. Formalise le critère : RH correspondrait à l'absence de partie anti-hermitienne **si** l'opérateur est dérivé exactement de l'arithmétique.

**Garde-fou.** Wu–Sprung montre déjà qu'un potentiel fini peut être reconstruit à partir de zéros ; ce n'est pas une preuve. Le verrou est `GAP-SCHR`: dériver `(H,M)` et prouver l'auto-adjointeté/observabilité, pas ajuster un spectre.


## 14. Phase localisation de sources / Schrödinger / générateur identifié (V4.1–V4.3)

### Idée

Traiter la formule explicite comme un problème inverse spectral : les nombres premiers fournissent les observations et les zéros des modes latents `exp((beta-1/2+i gamma)t)`. Après prétraitement multicanal, identifier un propagateur `A`, puis un générateur `H_eff=(i/dt)log A`.

### Apports

- dictionnaire `rho ↔ E=-gamma+i(beta-1/2)` ;
- lecture flux/source par équation de continuité ;
- localisation synthétique de modes hors ligne ;
- métrique positive non euclidienne `M` et test `H^*M=MH` ;
- connexion explicite aux Grams/covariances des phases précédentes.

### Test de rejet

Davenport–Heilbronn doit rester non conservatif / à spectre complexe lorsque des zéros hors ligne sont présents. Un pipeline qui la rendrait artificiellement hermitienne est invalide.

### Verrou

Dériver `(H,M)` exactement depuis l'arithmétique, avec positivité/coercivité uniformes et correspondance spectrale exacte. Sans cela, la phase reste un diagnostic fini-dimensionnel.

### Statut

**Expérimental ; conservé comme nouvelle branche structurante, pas comme preuve.**
