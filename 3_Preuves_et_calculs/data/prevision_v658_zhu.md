# Prévisions V6.58 — Reproduire Zhu (2026) : la positivité de Weil sur la fenêtre [−0,8 ; 0,8] (écrites avant le calcul)

Auteur et titulaire des droits : Vincent NOËL. Écrit le 17 octobre 2026 à 09:10 UTC (11 h 10 à Bruxelles), avant tout calcul.

Objet : λ*(L) = inf Q(f)/‖f‖² sur les fonctions réelles de support [−L, L] (Zhu, arXiv:2608.24827 v2), avec
Q(f) = 2F(i/2)F(−i/2) + (1/2π) ∫ |F(t)|² [Re ψ(1/4 + it/2) − log π − Σ_{log n < 2L} 2Λ(n) n^{−1/2} cos(t log n)] dt, F = f̂.
Calcul indépendant (phase A, non certifiée) : écriture de Q en variable x (autocorrélation g = f ⋆ f̃, intégrales sur [0, 2L]),
base de Legendre paire (puis impaire) sur [−L, L], quadratures de Gauss, 60 chiffres, valeurs propres de la matrice de Galerkin
(majorants variationnels de λ*).
Valeurs de Zhu à reproduire (« planchers » de référence non certifiés, secteur pair, tableau 1) :
9,34·10⁻⁷ (L = 0,5) ; 1,61·10⁻⁹ (0,6) ; 4,18·10⁻¹³ (0,7) ; 1,65·10⁻¹⁷ (0,8). Majorant certifié à 0,8 : 2,27·10⁻¹⁷ ; minorant certifié : 8,9·10⁻¹⁸.

- Z1. Contrôle de la formule : pour une bosse lisse f (cos⁴), Q(f) calculé en variable x et Σ_{γ ≤ 1500} 2|F(γ)|² calculé avec les zéros connus concordent à 10⁻⁸ près (relatif).
- Z2. Nos valeurs λ_N(L) décroissent avec le nombre N de modes et se stabilisent ; à N = 40, elles sont dans un facteur 1,5 des planchers de Zhu aux quatre valeurs de L.
- Z3. À L = 0,8, notre λ_N est compris entre 8,9·10⁻¹⁸ et 2,27·10⁻¹⁷ (l'encadrement certifié de Zhu).
- Z4. Le secteur impair a une plus petite valeur propre au moins 30 fois plus grande que le secteur pair à L = 0,8.


## Ajout du 17 octobre, 9 h 47 UTC (avant calcul) — raccord avec le document 75

Z5. Sur le noyau des moments (secteur pair, 32 modes), la plus petite valeur à L = 11/20 = 0,55 est au-dessus du minorant certifié du document 75 (3/10000) et au-dessous de la valeur à 0,5 (0,0119). Valeur attendue : entre 6·10⁻⁴ et 3·10⁻³.
