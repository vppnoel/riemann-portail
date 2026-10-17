# Priorités — programme RH (v3, 2026-10-03)

La v3 remplace l'objectif vague « pousser `Q(X)` jusqu'à RH » par un programme de
**calibration spectrale falsifiable**. Toute nouvelle inégalité doit d'abord montrer qu'elle
fait mieux qu'une simple reformulation de RH.

## Constat de départ

- Par L6,
  \[
  \frac12\limsup_{X\to\infty}\frac{\log Q(X)}{\log X}=\Theta-\frac12,
  \qquad
  \Theta=\sup_\rho\Re\rho.
  \]
  Donc `Q(X)=X^{o(1)}` est **équivalent** à RH.
- Le palier classique connu est `\Theta\le1`, avec absence de zéro sur `Re s=1`.
  On **ne sait pas** que `\Theta=1`.
- Obtenir `Q(X)\ll X^{1-\delta}` pour un `\delta>0` fixe donnerait déjà
  `\Theta\le1-\delta/2`, c'est-à-dire une bande sans zéro fixe : résultat majeur.
- Les calculs numériques à `X\le4\cdot10^6` vérifient la cohérence des identités et de la
  formule explicite basse hauteur. Ils ne contraignent pas un contre-exemple à très grande
  hauteur.

---

## P0 — Socle rigoureux et reproductible

| Action | Livrable | Statut v3 |
|---|---|---|
| Tests indépendants des identités | `tests/test_identities.py` | **11/11 OK** |
| `sympy.factorint` disponible explicitement | `requirements.txt`, tests | intégré |
| Preuve courte de `H_∞(q)` | L7 | **[RIG/PNT]** |
| Passage exposant de `Q` ↔ `Θ` | L6 | **[RIG]**, Perron aux demi-entiers |
| Lien exact Nyman–Beurling | L10 | **[RIG/PNT]** |
| Observable spectrale à deux paramètres | L11 + `src/spectral_calibration.py` | définition **[RIG]**, aucune densité revendiquée |

**Critère d'acceptation P0 :** tous les tests passent et aucune étape `[RIG]` ne dépend d'une
hypothèse RH cachée.

---

## P1 — Théorème conditionnel propre

### Énoncé visé

Sous RH et simplicité des zéros,

\[
Q(e^L)=\frac{4\kappa}{3}L^3+\alpha L^2+\beta L+o(L),
\qquad
\kappa=2+\gamma_E-\log(4\pi).
\]

Avec

\[
A_\rho=\frac2\rho,
\qquad
u_\rho=\frac{2c_0(\rho)-2\gamma_E-2/\rho}{\rho},
\qquad
c_0(\rho)=\frac{\zeta''(\rho)}{2\zeta'(\rho)},
\]

la partie diagonale suggère

\[
\alpha=2\Re\sum_{\gamma>0}A_\rho\overline{\nu_\rho},
\qquad
\beta=2\sum_{\gamma>0}|\nu_\rho|^2,
\]

sous les hypothèses de convergence nécessaires.

### Pourquoi le garder

La v2/v3 montre numériquement que la formule explicite avec 300 zéros reproduit `Q` à
quelques pourcents jusqu'à `X=4·10^6` et `B(t)` avec corrélation d'environ `0.976`. Ceci est
un test de cohérence, pas un test de RH.

### Critère d'acceptation

- terme `L^3` avec reste explicite : **[RIG sous RH]** ;
- termes `L^2` et `L` : ne pas les étiqueter `[RIG]` avant contrôle des sommes hors diagonale.

---

## P2 — Calibration / tests de rejet avant toute attaque directe

### P2.1 — Davenport–Heilbronn

Construire l'analogue de `G`, de `C` et de `Q` pour une série de Dirichlet satisfaisant une
équation fonctionnelle mais sans produit d'Euler et possédant des zéros hors de la droite
critique.

**Diagnostic déjà obtenu :** la partie analytique « pôle aux zéros ↔ croissance de l'énergie »
est générique et survivra. Le produit d'Euler de `ζ` intervient spécifiquement dans :

1. `q=\sum\Lambda(n)n^{-s}` ;
2. `1/ζ=\sum\mu(n)n^{-s}` ;
3. la parcimonie de `c(n)` (support sur ≤2 premiers distincts) ;
4. la formule multiplicative des canaux `H_∞(q)`.

**Test réussi seulement si** une future inégalité utilise l'un de ces quatre ingrédients de
manière irréversible et échoue effectivement pour Davenport–Heilbronn.

### P2.2 — Corps de fonctions / Weil

Chercher l'analogue de `Q` et de `c=1*a`, puis identifier une positivité spécifique au produit
d'Euler / à la géométrie. Une simple positivité de Gram ou de norme `L²` ne suffit pas : elle
est générique.

**Test réussi si** le formalisme retrouve une positivité qui joue le rôle analytique de la
positivité géométrique dans la preuve de Weil.

### P2.3 — Benchmark inconditionnel : densité de zéros

Le scalaire `Q(X)` ne voit essentiellement que `sup Re ρ`. La v3 introduit donc

\[
Q_{w,W}(L;T,\Delta)
\]

(L11), qui conserve aussi la hauteur spectrale.

Premier benchmark : récupérer, même avec pertes, **une borne classique de densité de zéros**.
La référence moderne de comparaison est Guth–Maynard (Annals 2026), qui obtient

\[
N(\sigma,T)\le T^{\frac{30}{13}(1-\sigma)+o(1)}.
\]

Le but initial n'est pas de battre cet exposant ; il est de vérifier que le formalisme sait
au moins transformer une estimation de polynômes de Dirichlet en une borne de densité.

### Règle d'arrêt P2

Si le cadre :

- ne distingue pas Davenport–Heilbronn de `ζ`, **et**
- ne redonne aucune densité de zéros non triviale,

alors suspendre l'attaque directe de RH et limiter le projet à P0/P1.

---

## P3 — Familles de caractères : terrain inconditionnel crédible

Définir l'analogue

\[
Q_\chi(X,T)
\]

pour `L(s,χ)` puis moyenner sur les caractères modulo `q` dans une famille.

Ici le grand crible, Barban–Davenport–Halberstam et les théorèmes de densité de familles
fournissent réellement des informations inconditionnelles. Le test scientifique est :

> le formalisme `Q_χ(X,T)` retrouve-t-il un exposant connu lorsque l'on injecte un grand
> crible standard ?

Si oui, il devient une interface utile entre géométrie Nyman–Beurling et outils de familles.

---

## P4 — Suspendre comme routes de preuve

- Information Kalman / « GPS analytique » : conserver comme diagnostic numérique et langage
  de covariance, **pas** comme source indépendante d'information.
- Parseval locale uniforme de Möbius à l'échelle `1/N` : trop proche d'une borne racine
  carrée de Mertens, donc probablement RH déguisée.
- Extension brute des calculs numériques : utile pour validation de code, pas pour décider RH.
- Type I/II appliqué sans nouvel ingrédient : les versions testées retombent sur un gain trop
  faible ou sur le seuil naturel de RH.

---

## Ordre de travail v3

1. **P0** : tests + L6 + scripts spectraux.
2. **P1** : rédiger proprement le terme conditionnel `L^3`, puis seulement les termes suivants.
3. **P2.1** : documenter Davenport–Heilbronn comme test de rejet.
4. **P2.3** : tenter une vraie borne de densité à partir de `Q(X,T)`.
5. **P3** seulement si P2.3 montre que l'interface spectrale est compétitive.


## Mise à jour v3.7
P2 exécuté : P2.1 partiel (couche générique), P2.2 NO-GO, P2.3 NO-GO (voir ROADMAP_HISTORY §16). **Règle d'arrêt déclenchée** : poursuivre P0/P1 (rédaction, relecture, positionnement), abandonner P3 (moyenne sur les caractères) comme voie d'attaque de RH.


## P5 — Branche expérimentale : localisation inverse de sources (V4.1)

Cette branche n'annule pas la règle d'arrêt P2. Elle sert de banc de recherche transversal inspiré des méthodes de localisation de sources.

Ordre de validation :
1. injection synthétique de sources `(beta,gamma)` ;
2. Davenport–Heilbronn comme contrôle positif hors ligne ;
3. étude de la visibilité / plus petite valeur singulière en fonction de la hauteur ;
4. comparaison de fenêtres (moyennage, Morlet, Laplacien régularisé) ;
5. seulement si une borne uniforme spécifique au produit d'Euler apparaît, reclasser la branche comme priorité analytique.

**Critère d'arrêt P5 :** si la visibilité se dégrade jusqu'à zéro avec la hauteur sans mécanisme arithmétique compensateur, conserver la méthode comme outil de visualisation/localisation uniquement.


## Branche V4.2 — Schrödinger / flux

Statut : exploration contrôlée, hors voie principale A/B/C. Priorité uniquement si un mécanisme **arithmétique** permet de dériver l'opérateur ou de forcer l'annulation de sa partie anti-hermitienne. Sans cela, rester au niveau diagnostic / problème inverse et ne pas rouvrir une attaque directe de RH.

## Branche expérimentale V4.3 — générateur arithmétique

Cette branche n'est pas prioritaire sur l'audit A/B/C. Elle devient intéressante seulement si elle passe deux tests :

1. **Davenport–Heilbronn** : conserver des énergies complexes / défauts de conservation lorsque des zéros hors ligne sont présents ;
2. **stabilité en dimension** : obtenir une métrique positive `M` dont le conditionnement et la coercivité ne se dégradent pas catastrophiquement quand hauteur, résolution et nombre de canaux augmentent.

Le livrable analytique visé est `GAP-SCHR-GEN`, non un ajustement numérique de spectre.
