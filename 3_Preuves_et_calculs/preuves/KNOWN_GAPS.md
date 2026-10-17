# Trous mathématiques restant à fermer — état V5.1

## GAP-0 — RH reste exactement la cible finale

L6 donne désormais rigoureusement

\[
\frac12\limsup_{X\to\infty}\frac{\log(1+Q(X))}{\log X}=\Theta-\frac12.
\]

Donc

\[
Q(X)=X^{o(1)}\iff RH.
\]

Le cadre ne constitue un progrès vers RH que s'il rend applicable un outil qui produit un
**gain intermédiaire réel**.

## GAP-1 — aucune bande sans zéro fixe nouvelle

On ne sait démontrer ici aucune borne

\[
Q(X)\ll X^{1-\delta}
\]

avec `delta>0` fixe. Par L6, une telle borne donnerait déjà

\[
\Theta\le1-\delta/2<1,
\]

c'est-à-dire une avancée majeure indépendante de RH.

## GAP-2 — FERMÉ en v3

L'ancien passage

\[
\tfrac12\limsup \log Q/\log X=\Theta-\tfrac12
\]

est maintenant L6 `[RIG]`. Le point technique de désmoothement est évité en appliquant
Perron aux demi-entiers, où `|x-n|>=1/2`.

## GAP-3 — théorème conditionnel `L^3+L^2+L`

Sous RH et simplicité des zéros, la formule explicite suggère

\[
Q(e^L)=\frac{4\kappa}{3}L^3+\alpha L^2+\beta L+o(L).
\]

Le coefficient dominant diagonal est compris. **v3.2** : α ≈ −0,26 et β ≈ 0,47 calculés avec 300 zéros dérivent encore de ~4 % par centaine de zéros ; un ajustement libre sur Q mesurée donne des valeurs sans rapport (L², L, 1 quasi colinéaires sur L ∈ [8,15]). Seul le terme (4κ/3)L³ est un énoncé visé ; α et β sont des prédictions non confirmables numériquement. **v3.6 (correction)** : α et β ne sont pas des coefficients ponctuels : le coefficient de L² dans U(L) vaut α+Φ(L) avec Φ presque périodique (≈ ±0,03, corrélation 0,996 avec l'écart mesuré) ; α, β sont des moyennes, définies par le développement de Q_η (η⁻², η⁻¹), vérifié à 4 chiffres sur un modèle local à 300 zéros. Énoncé correct : U(L)=(4κ/3)L³+O(L²) sous une hypothèse de paires proches (`docs/ALPHA_BETA_ANALYSE.md`). **v3.4** : le terme dominant est maintenant un théorème conditionnel à RH (`docs/THEOREME_TERME_DOMINANT.md` : Q(X) ∼ (S/3)(log X)³, S=4κ pour zéros simples) ; seuls L² et L restent ouverts. **v3.3** : leurs séries font intervenir 1/ζ'(ρ) et convergent absolument sous RH + zéros simples + Lindelöf + la condition (2) de Bettin–Conrey–Farmer (esquisse, `docs/COMPARAISON_BCF.md` §3) ; le moment de Gonek est numériquement cohérent. Le contrôle hors diagonale reste ouvert. Les termes
hors diagonale nécessaires au contrôle de `L^2`, `L` et du reste ne sont pas rédigés.

## GAP-4 — test Davenport–Heilbronn non exécuté jusqu'au bout

v3.2 : banc exécutable (`src/rejection.py`, `docs/DAVENPORT_HEILBRONN_TEST.md`) ; la couche générique est confirmée (Q détecte aussi les zéros de DH). La v3 identifie où le produit d'Euler intervient (`Lambda`, `mu`, parcimonie de `c`, canaux
`H_inf`), mais ne possède pas encore une inégalité candidate qui **échoue effectivement**
pour Davenport–Heilbronn.

## GAP-5 — aucune densité de zéros issue de `Q(X,T)`

L11 définit une énergie spectrale fenêtrée

\[
Q_{w,W}(L;T,\Delta),
\]

mais aucune inégalité n'est encore démontrée qui transforme cette énergie en borne utile sur

\[
N(\sigma,T).
\]

C'est le benchmark principal de la v3.

## GAP-6 — pas d'analogue identifié de la positivité de Weil

Les positivités de norme, Gram et compléments de Schur présentes dans le package sont
génériques. Aucune positivité spécifique à l'arithmétique du produit d'Euler, comparable au
mécanisme géométrique des corps de fonctions, n'est isolée.

## GAP-7 — canaux terminaux / Fourier locale

Les diagnostics de canaux, de covariance `gcd^2/(12de)`, de Fourier locale de Möbius et de
filtre Kalman sont reproductibles, mais aucune borne nouvelle n'en ressort qui améliore une
région sans zéro ou une densité de zéros connue.

Ils restent des **outils de diagnostic**, pas des étapes de preuve.


## GAP-8 — localisation inverse des sources : pas de visibilité uniforme

La V4.1 formalise le signal explicite comme somme de modes

\[
s_{\beta,\gamma}(t)=e^{(\beta-1/2)t}e^{i\gamma t}
\]

et fournit des diagnostics finis (matched filter/GLS, enveloppe Morlet, Laplacien régularisé, plus petite valeur singulière).

Le passage à RH demanderait une estimation uniforme du type

\[
\|A s\|_{\rm obs}\ge c\|s_{\rm off}\|,\qquad c>0,
\]

avec `c` ne s'effondrant pas lorsque `|gamma|`, la résolution et la dimension augmentent. Aucune telle borne n'est démontrée. La branche reste donc `[EXP]/[NUM]/[GAP]`.


## GAP-SCHR — opérateur Schrödinger/Hilbert–Pólya dérivé de l'arithmétique

**Statut : ouvert.** Il manque un opérateur `H` et un opérateur d'observation `M` satisfaisant simultanément : (i) lien spectral exact avec les zéros de zêta, (ii) domaine/conditions de bord permettant de prouver l'auto-adjointeté, (iii) reproduction quantitative de la formule explicite ou de `C,Q`. Ajuster numériquement un potentiel à un nombre fini de zéros ne suffit pas. Une voie de preuve devrait montrer que la structure d'Euler force la partie anti-hermitienne à s'annuler sur le sous-espace arithmétique observable.


## GAP-SCHR-GEN — générateur arithmétique et métrique positive uniforme

**Statut : ouvert.** La V4.3 sait, en dimension finie et sur données synthétiques, identifier un propagateur `A`, construire `H_eff=(i/dt)log A` et certifier une métrique positive `M` lorsque le spectre identifié est réel. Cela n'est qu'un diagnostic. Une implication pour RH demanderait simultanément :

1. une construction exacte de l'espace d'état depuis les nombres premiers / la formule explicite ;
2. un générateur `H` dont le spectre encode exactement `E_rho=-gamma+i(beta-1/2)` ;
3. une métrique `M>0` dérivée de l'arithmétique avec bornes de coercivité uniformes en hauteur/dimension ;
4. l'identité `H^* M=M H` sur un domaine invariant approprié ;
5. une observabilité excluant qu'un mode hors ligne soit caché dans un sous-espace non observé.

Sans ces cinq points, la branche reste `[EXP]/[NUM]/[GAP]`.


## GAP-SCHR / GAP-SCHR-GEN — précision v4.4
Ces verrous sont le problème de Hilbert–Pólya (opérateur canonique, auto-adjoint, spectre {γ}). L'audit (`docs/AUDIT_V4_3.md`) montre que (i) la métrique M>0 est équivalente à la réalité du spectre en dimension finie, (ii) l'identification de modes sur le vrai signal des premiers est biaisée (Re λ jusqu'à −0,09) et produit des fantômes sur DH, (iii) le signal d'ordre 2 est défectif. Aucun investissement supplémentaire n'est justifié sans dérivation analytique de (H, M).

## GAP-DIM — Dimension énergétique / generalized fractal string (v5.2)

**Fermé au niveau de la reformulation :** la mesure positive `eta_E`, push-forward de `|C(x)|^2 dx/x` par `y=x^2`, est une generalized fractal string dont la zêta géométrique est

\[
\mathcal Z_E(s)=\int_1^\infty |C(x)|^2x^{-1-2s}dx,
\]

et son abscisse de convergence vaut exactement `Theta` par le Théorème A. Donc RH équivaut à `D_E=1/2`.

**Ouvert :** cette reformulation n'impose pas `D_E=1/2`. Il manque une propriété supplémentaire, propre à l'arithmétique de `zeta`, qui soit fausse pour Davenport–Heilbronn et qui force la dimension à ne pas dépasser `1/2`.

**Ouvert également :** pour le problème infini, aucune continuation méromorphe de `Z_E` jusqu'à/à travers `Re s=1/2` n'est démontrée ici. Les pôles aux moyennes `(rho+rho')/2` sont établis exactement pour le modèle fini ; leur passage à `zeta` exige des contrôles de convergence et de paires de zéros du même type que GAP-3/H3.


## GAP-NB-FAMILLE (v5.3)
Familles d'approximants de Möbius pondérés par des puissances de log n (projection de Nyman–Beurling) : plateau observé e_N² log N / κ ≈ 1,2–1,4 pour 20 ≤ N ≤ 998 (v5.4), β_N log² N ≈ −1,1 à −1,3 ; optimum sans carré ≈ κ/log N (0,98–1,07). **Non démontré** : comportement pour N → ∞, antériorité du plateau, évaluation asymptotique de Γ_00, Γ_01, Γ_11 (sommes de Möbius–gcd de niveau Mertens). Voir `1_Presentation/09_Attaques_audit_et_amelioration`.


## GAP-RH-ORDRE-2 (v5.5)
L'estimation sous RH par le terme principal κ∫P′²/log N ne décrit pas N ≤ 1000. Pour expliquer le plateau de {μ, a}, il faut le terme en 1/log²N de e²(P), forme quadratique en (P′(0), P″(0), P′(1), …). Mesuré : coefficient ≈ 3,6 pour P′(0)² = 1 (poids 1 − x). **Non démontré.**


## GAP-NB-FAMILLE — clôture (v5.6)
Avec β = −S_N/A_N (annulation du pôle), e² = β²Q(N) + T_N exactement. b_N = β log²N → −1 − 2γ/log N (résidus sous RH, confirmé jusqu'à 10⁷). Sous RH et Théorème B, la famille tend vers ≈ (4/3)κ/log N. Montrer e_N → 0 sans RH exige Q(N) = o(log⁴N), donc RH (Théorème A). **Branche close.**


## Volet « cibles » — clôture (v5.8)
Le seul progrès récent sur les zéros (Alpöge–Furman 2026, ≥ 2/3 simples et sur la droite) repose sur une compression finie de la forme hermitienne de Weil (rang–trace, inertie de Sylvester), conformément au diagnostic du mémo P2.2. Prolongements naturels déjà publiés ; aucune cible réaliste pour ce programme. Voir `1_Presentation/13_Lecon_2026`.

## GAP-NB-FAMILLE — correctif (V6.20)
Recalcul jusqu'à 5·10⁶ (doc. 45) : la clôture V5.6 « la famille tend vers ≈ (4/3)κ/log N » ne vaut qu'en valeur typique. Médiane 0,985 × 4/3, sans montée visible de 10⁴ à 5·10⁶ ; pics jusqu'à 3,27 × 4/3 là où A_N s'annule (|b_N| = 93 218 à N = 33 493). Limite 4/3 conditionnelle à RH, aux zéros simples et à T_N log N → 0 (T_N ≈ 2,9 κ/log²N observé). **Non démontré** : la décroissance de la queue (coup « La queue par l'Écho »).

