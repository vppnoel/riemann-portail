# Corrections utilisateur intégrées — 2026-10-04

Ce fichier consigne les corrections et décisions méthodologiques qui ont été intégrées à la V3.9 puis consolidées dans la V4.0.

## 1. Statut global

- La cible `Q(X)=X^{o(1)}` est explicitement présentée comme **équivalente à RH**, et non comme un palier intermédiaire.
- Les calculs numériques sont traités comme des **tests de cohérence interne**, jamais comme des tests de RH.
- Les outils Apollo/Kalman, Parseval locale uniforme, Type I/II naïf et extrapolations numériques sont rétrogradés au rang de diagnostics.

## 2. Canaux terminaux

La preuve courte de

\[
H_\infty(q)
=-\frac{2\mu(q)}{\varphi(q)}\sum_{p\mid q}\frac{p\log p}{p-1}
\]

pour `q` sans carré est retenue comme version canonique. Elle part de

\[
\Phi_q(s)=\frac{\mu(q)h_q(s)}{\zeta(s)},
\qquad h_q(s)=\prod_{p\mid q}(p^s-1)^{-1},
\]

puis utilise directement `f'(1)=1`, `f''(1)=-2γ_E`; les termes en `γ_E` s'annulent. Voir `docs/LEMMES_RIGOUREUX.md`, L7.

## 3. Factorisation et tests

- `sympy.factorint` est utilisé explicitement comme factorisation indépendante dans les tests.
- Le test de `H_∞` utilise la forme courte ci-dessus.
- Le test de régularité en `s=1` compare à la valeur limite exacte `G(1)=2γ_E²+6γ_1`.
- La suite actuelle contient 21 tests et doit être exécutée avant diffusion.

## 4. Numérique

- La référence `(4κ/3) log^3 X` n'est qu'un terme dominant et converge lentement.
- La formule explicite avec les contributions des zéros reproduit les calculs de `Q` à quelques pourcents sur la plage testée ; ceci valide les identités et l'implémentation, pas RH.
- L'annulation de la majeure partie du proxy diagonal provient principalement de la régularisation exacte en `s=1`.
- `info_per_logX` ne montre aucune loi asymptotique exploitable.
- Le coefficient de `L²` n'est pas une constante ponctuelle : il comporte une composante presque périodique `Φ(L)`.

## 5. Tests de rejet

Avant toute reprise d'une attaque directe de RH, le cadre doit passer trois contrôles :

1. Davenport–Heilbronn : identifier l'utilisation irréversible du produit d'Euler.
2. Corps de fonctions : identifier une positivité de type Weil/Hodge réellement restrictive.
3. Densité de zéros : reproduire au moins un résultat inconditionnel connu sans simplement réimporter toute la technologie classique des grandes valeurs.

La V3.9 conclut que ces tests ne fournissent pas de nouveau mécanisme et déclenche la règle d'arrêt de l'attaque directe.

## 6. Conséquence éditoriale

La V4.0 est un package d'**audit et de consolidation**, non une nouvelle attaque de RH. Les objectifs prioritaires sont :

- audit externe des Théorèmes A et B ;
- vérification de priorité dans la littérature ;
- séparation stricte entre résultat prouvé, résultat conditionnel et diagnostic numérique ;
- rédaction éventuelle d'un article court centré sur A, B, C et les résultats négatifs des tests de calibration.
