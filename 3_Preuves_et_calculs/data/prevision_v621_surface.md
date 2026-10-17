# Prévisions V6.21 — Axe J, la surface virtuelle (écrites avant le calcul)

Auteur et titulaire des droits : Vincent NOËL. Écrit le 10 octobre 2026 à 19 h 10 UTC (21 h 10 à Bruxelles), avant tout calcul de l'axe J.

Idée de l'auteur : résoudre par une géométrie « impossible ou virtuelle ». Dans le Modèle réduit, la surface C × C existe ;
RH y découle de la positivité de Castelnuovo (théorème de l'indice de Hodge). Pour ζ, la surface n'existe pas : on construit
seulement sa forme d'intersection, à partir des nombres premiers, et l'on regarde si elle a la signature d'une vraie surface.

Dictionnaire attendu (à démontrer) : graphes de Frobenius Γ_n, fibres f1 = pt × C, f2 = C × pt.
Γ_m·Γ_n = q^min(m,n) N_|m−n| (m ≠ n) ; Γ_n·Γ_n = q^n (2 − 2g) ; Γ_n·f1 = 1 ; Γ_n·f2 = q^n ; f1·f2 = 1.
Orthogonalement aux fibres, après normalisation q^−n/2 : D_m·D_n = −q^−|m−n|/2 S_|m−n| (S_d = Σ α^d), diagonale −2g.
Donc : nombre de directions positives = 1 + nombre de valeurs propres négatives de la forme de Toeplitz du corpus (doc. 29).

- P1 (courbes) : pour les 425 courbes du Modèle réduit, la forme d'intersection sur {f1, f2, Γ_0, …, Γ_4g} a exactement
  une direction positive (indice de Hodge), à 10⁻⁹ près relatif.
- P2 (faux jumeaux) : pour chaque faux jumeau (équation fonctionnelle, comptages ≥ 0, RH fausse), au moins deux directions
  positives dès la fenêtre 2g + 1 ; le surplus vaut (nombre de racines hors du cercle |α| = √q)/2.
- P3 (ζ, L(χ5), DH, depuis les seuls premiers) : la forme virtuelle a une seule direction positive pour ζ et L(χ5) à toutes
  les fenêtres fiables ; pour DH, le surplus vaut 2 par quadruplet hors de la droite résolu (comme les directions négatives
  de la métrique des premiers, doc. 33).
- P4 (rang) : dans le Modèle réduit, le rang de la forme sur les graphes, orthogonalement aux fibres, vaut 2g (genre) dès la
  fenêtre 2g ; pour ζ, le rang effectif à la fenêtre de Heisenberg suit le nombre de zéros résolus (« genre virtuel »).
