# Prévisions V6.33 — La force qui abaisse le relief : le défaut de multiplicativité (écrites avant le calcul)

Auteur et titulaire des droits : Vincent NOËL. Écrit le 11 octobre 2026 à 21:00 UTC (23 h 00 à Bruxelles), avant le calcul.

Objet : la carte de V₇ impair (doc. 56, 141 × 141 points, T* critère persistant). En chaque point c, les coefficients de F_c ne dépendent que de n modulo 7 : A(r) = Σ_χ c_χ e^{−iφ_χ} χ(r). Défaut de multiplicativité, sans unité :
D(c) = Σ_{r,s} |A(1)·A(rs) − A(r)·A(s)|² / (Σ_r |A(r)|²)², nul exactement aux points d'Euler.
Distance au point d'Euler le plus proche : d(c) = arccos(max_χ |c_χ| / ‖c‖).

- D1. Sur toute la carte, T* décroît quand D croît : corrélation de rang (Spearman) entre T* et D inférieure à −0,6.
- D2. À distance égale, D n'ajoute presque rien : la corrélation partielle de rang entre T* et D, une fois retirée l'influence de d, est comprise entre −0,2 et +0,2. La « force » serait alors surtout l'éloignement, pas la forme du défaut.
- D3. Le col où les trois îles se séparent (points où T* vaut exactement 145, doc. 56) passe par les endroits de plus faible défaut : pour plus de la moitié de ces points, D est sous la médiane des points de même distance d.
