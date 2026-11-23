# TAC-009 — Gram de Nyman–Beurling sur des différences d’échelle

*Producteur : Codex — ia:chatgpt-sol-6.1-max · 18 octobre 2026 · Programme Riemann V6.59.*

## Prévision

Le Gram standard de différences de dilatations sera déterminé par la géométrie des dilatations. Une séparation entre (zeta), (L(s,chi)) et Davenport–Heilbronn exigera une famille généralisée dépendant explicitement de la série de Dirichlet et un théorème précisant son domaine.

## Méthode

Pour une famille standard (ho_	heta) du cadre Nyman–Beurling et une grille (	heta_i=e^{-u_i}), poser
[
C_i=ho_{	heta_{i+1}}-ho_{	heta_i},qquad
K^{NB}_{ij}=langle C_i,C_jangle_{L^2(0,1)}.
]
Cette définition ne contient aucun paramètre (F). Sa matrice dépend de la famille (ho) et de la grille ((u_i)), non de (zeta), d’une fonction (L) ou de Davenport–Heilbronn.

La littérature confirme deux éléments, vérifiés sur sources primaires en ligne :
- de Roton généralise un critère de Beurling–Nyman à une classe de séries de Dirichlet, mais une généralisation ne fournit pas automatiquement une même base (ho_	heta) pour chaque série ;
- Darses–Najnudel étudient des matrices de Gram dans un cadre Nyman–Beurling généralisé et obtiennent une structure block-Hankel pour un réglage particulier. Cela ne démontre pas une séparation Euler/non-Euler.

Références vérifiées : A. de Roton, *C. R. Math.* 340 (2005), 191–194, doi:10.1016/j.crma.2004.11.023 ; S. Darses et J. Najnudel, *J. Théorie des Nombres de Bordeaux*, doi:10.5802/jtnb.1227.

## Résultat

Dans la formulation de la fiche, (K^{NB}) est exactement le même objet pour les trois candidats. Il est donc impossible de calculer une comparaison (zeta/L(chi)/DH) : aucune dépendance à (F) n’a été définie. Le témoin géométrique coïncide alors avec l’objet étudié, au lieu d’être un contrôle externe.

Pour rendre l’expérience exécutable, il faut d’abord figer :
1. une famille (ho^F_	heta) pour chaque série (F) ;
2. le théorème de densité ou de région sans zéros auquel elle correspond ;
3. une normalisation commune et l’analogue précis de DH ;
4. un calcul de Gram dont la dépendance arithmétique ne soit pas injectée par construction.

Sans ces quatre éléments, une éventuelle différence spectrale serait soit absente, soit imposée par la définition choisie.

## Portée

Ce résultat ne contredit pas le critère Nyman–Beurling pour (zeta), ni les généralisations existantes. Il refuse seulement l’inférence selon laquelle une matrice de dilatations standard pourrait, à elle seule, détecter le produit d’Euler ou les zéros hors droite.

La structure block-Hankel repérée dans la littérature est une structure de matrice de Gram ; elle ne constitue pas une signature multiplicative et ne relie pas par elle-même son spectre à la positivité de Weil.

## Critère de rejet

Atteint dans la formulation courante : l’observable ne porte aucune variable (F), donc elle ne peut voir autre chose que la géométrie des dilatations. Le test différentiel demandé est indéfini, non négatif numériquement.

## Statut proposé

**obstacle.** Avant tout calcul, la tâche exige une définition généralisée précise et une référence théorique vérifiée ; sinon elle confond un Gram géométrique avec un invariant arithmétique.
