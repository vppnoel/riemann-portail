# Prévisions V6.24 — J3 simplifié et « le même calcul » que les deux tiers (écrites avant le calcul)

Auteur et titulaire des droits : Vincent NOËL. Écrit le 11 octobre 2026 à 22:23 UTC (horloge du conteneur), avant tout calcul de la V6.24.

## A. J3 simplifié : additivité ou dérivée nulle ?
En caractéristique p, le Frobenius est à la fois additif ((x + y)^p = x^p + y^p) et de dérivée nulle. En « caractéristique un »
(Connes–Consani), le Frobenius x ↦ x^λ reste additif, mais sa dérivée ne s'annule pas (n·a = a). Laquelle des deux propriétés
porte la fonction de Stepanov ? Même construction qu'en V6.23, avec : x^p + 1 (dérivée nulle, non additif), x^p + x (additif,
dérivée 1), x^{2p} (dérivée nulle, non additif), et le Frobenius x^p (les deux).
- A1 : la chute de rang (fonctions auxiliaires > 0) a lieu exactement pour les φ de dérivée nulle (x^p, x^p + 1, x^{2p}),
  et pas pour x^p + x, bien qu'additif.
- A2 : conséquence attendue : le Frobenius de caractéristique un, additif mais de dérivée non nulle, ne donne pas la fonction
  de Stepanov sous cette forme ; J3 complet devrait chercher un autre mécanisme.

## B. « Le même calcul » que les deux tiers d'Alpöge–Furman, sur nos zéros
Inégalité rang–trace sur la métrique des zéros à la fenêtre A (noyau de Fejér, support de Fourier [−A, A] en unités
normalisées) : nombre de zéros distincts ≥ (tr G)²/tr G², proportion de zéros simples ≥ 2 × (distincts) − 1.
- B1 : à A = 1 (portée du théorème de Montgomery), sur les 1 070 zéros de ζ, distincts ≥ 0,75 ± 0,02 et simples ≥ 0,50 ± 0,04
  (valeur du noyau sinus avec ce noyau ; le 0,6725 d'Alpöge–Furman vient d'un noyau optimisé).
- B2 : la borne croît avec A : distincts ≥ 0,95 à A = 4.
- B3 : pour le mélange ζ·L(χ5) (familles étrangères), la borne à A = 1 est plus basse que pour ζ seule.
