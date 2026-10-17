# Prévisions V6.29 — Lire Bogomolny et al. pour de vrai : le trou à trois (écrites avant le calcul)

Auteur et titulaire des droits : Vincent NOËL. Écrit le 10 octobre 2026 à 23:50 UTC (11 octobre, 1 h 50 à Bruxelles ; horloge du conteneur), avant le calcul des rapports d'écarts et du CUE(3). Déjà calculé à ce moment : la fraction de triples de portée < 1 du CUE(N) pour N = 4 à 40 et son ajustement a + b/N² (a = 0,01464, b = −0,0582 ; `data/bblm_trou_a_trois.json`).

Prévision du navigateur (V6.28, coup « Lire Bogomolny et al. pour de vrai ») : « la correction effective prévoit un déficit du bon sens, mais plus faible que mesuré ».

Lecture faite (résumés) : Bogomolny et al. 2006 [BBLM06] ; Nishigaki 2025 [Nis25], qui montre que dans le rapport de deux écarts consécutifs la correction en N⁻² du CUE s'annule, et que l'écart de ζ au noyau sinus y décroît comme (log(T/2π))⁻³.

- **B1.** Le CUE(3), la plus petite taille qui a des triples, a encore une fraction de triples de portée < 1 entre 0,004 et 0,010. La vraie taille finie ne fait pas le trou : 0 sur 1 068 demande une fraction ≤ 0,0028.
- **B2 (test de Nishigaki).** La moyenne du rapport d'écarts r̃ = min(s_i, s_{i+1})/max(s_i, s_{i+1}) des zéros de ζ (t ≤ 1 500), de L(χ5) (t ≤ 600) et de Δ (t ≤ 1 500) est compatible avec la valeur limite du noyau sinus (CUE de grande taille) à 2 écarts-types près.
- **B3.** Le contraste : pour ζ, la loi de la portée w = s_i + s_{i+1} s'écarte du noyau sinus (test de Kolmogorov–Smirnov, p < 0,01) ; la loi de r̃, elle, n'en s'écarte pas (p > 0,05). Le trou à trois serait alors un effet d'échelle (ce que décrit Bogomolny et al., ou un défaut du dépliage), et non un effet de forme.
