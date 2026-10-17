# Prévisions V6.27 — J6, le carré en continu (écrites avant le calcul)

Auteur et titulaire des droits : Vincent NOËL. Écrit le 11 octobre 2026 à 22:57 UTC (horloge du conteneur), avant tout calcul de J6.

On refait la forme d'intersection virtuelle du doc. 46 (fibres ↔ pôle, intersections ↔ puissances de premiers, genre ↔ terme
archimédien), calculée depuis les seuls premiers, pour une grille de réglages : largeur de la fonction-test a ∈ {0,02 ; 0,04 ;
0,08 ; 0,16}, pas h ∈ {0,005 ; 0,01 ; 0,02}, fenêtres jusqu'à X = e^{Lh+2a} ≤ 3 000. Un réglage est « fiable » si les traces
calculées depuis les premiers et depuis les zéros connus concordent à 10⁻⁶ près (relatif).
- P1 : ζ : exactement une direction positive dans tous les réglages fiables ; L(χ5) : aucune.
- P2 : DH : des directions en trop dès que X ≥ 61, en nombre croissant avec X.
- P3 : à X fixé, le nombre de directions en trop de DH ne dépend pas du pas h (il compte des quadruplets de zéros, pas une grille).
- P4 : DH : le nombre de directions en trop est pair dans tous les réglages (deux par quadruplet).
