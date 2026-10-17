# Prévisions V6.22 — Axe J2, le Riemann–Roch virtuel (écrites avant le calcul)

Auteur et titulaire des droits : Vincent NOËL. Écrit le 10 octobre 2026 à 22 h 01 UTC (11 octobre, 0 h 01 à Bruxelles), avant tout calcul de J2.

Consigne : viser une propriété d'existence, de dimension ou de dualité, justifiée indépendamment de RH.
Dans le Modèle réduit, on teste sur les 425 courbes et les 220 faux jumeaux, le long de la tour F_{q^m} (m = 1 à 80),
trois contraintes que toute courbe lisse de genre g vérifie, démontrées SANS RH :
- (E) existence : le groupe Pic⁰(F_{q^m}) contient au moins la classe nulle, h_m = Π(1 − α_i^m) ≥ 1 ;
- (C) dimension (Clifford, conséquence de Riemann–Roch) : pour 1 ≤ n ≤ 2g − 2, le nombre A_n de diviseurs effectifs
  de degré n vérifie A_n ≤ h_m (q^{m(⌊n/2⌋+1)} − 1)/(q^m − 1) ;
- (S) existence d'une fonction auxiliaire par comptage de dimension (Stepanov–Bombieri, Riemann–Roch sur la courbe) :
  si q^m est un carré et q^m > (g + 1)⁴, alors N_m ≤ q^m + (2g + 1) q^{m/2} + 1.
(La dualité, ℓ(D) − ℓ(K − D) = n − g + 1, est déjà satisfaite par les jumeaux : c'est leur équation fonctionnelle.)
Par le théorème de Pringsheim, (S) à tous les étages entraîne RH : c'est la preuve de Bombieri (1973).

- P1 : aucune des 425 courbes ne viole (E), (C) ou (S) jusqu'à m = 80 (ce sont des théorèmes ; contrôle des données).
- P2 : chacun des 220 jumeaux viole au moins une des trois contraintes avant m = 80.
- P3 : (S) seule démasque les jumeaux plus tard que Castelnuovo (médiane du rapport des étages ≥ 1).
- P4 : (E) et (C), sans (S), démasquent au moins un quart des jumeaux, certains avant Castelnuovo.

## Ajout après le premier calcul (horloge du conteneur : 22 h 01 UTC), avant le second

Résultat du premier calcul : P2 est fausse, (S) n'attrape que 121 jumeaux sur 220. Explication attendue : (S) ne borne N_m
que par le haut ; un jumeau dont la racine dominante est réelle positive a trop PEU de points, jamais trop. La borne par le
bas, chez Bombieri, vient d'un revêtement galoisien : pour une courbe hyperelliptique, le tordu quadratique existe sur chaque
F_{q^m} (propriété d'existence, sans RH) et compte Q + 1 + S_m points.
- P5 : avec (S′), la borne de Stepanov–Bombieri appliquée au tordu (Q + 1 + S_m ≤ Q + (2g + 1)√Q + 1, même condition sur Q),
  et (E′) l'existence de son groupe Pic⁰ (Π(1 + α_i^m) ≥ 1), les 220 jumeaux sont tous attrapés avant m = 80, et aucune courbe.
