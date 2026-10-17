# Prévisions V6.16 — « La Rencontre à trois » — écrites avant tout calcul — 2026-10-10T10:54:58Z

Objet : les 1 070 zéros de zeta jusqu'à t = 1 500 (data/zeta_zeros_1500.csv), plus la paire de Lehmer près de t = 7 005.
Pour chaque zéro k : écart normalisé au plus proche voisin s_k = g_k log(γ_k/2π)/2π ;
marge locale de la métrique à la fenêtre de Heisenberg, m_k = 1 − sinc²(π s_k) (déterminant normalisé du Gram de la paire,
identité exacte du modèle à deux atomes, à démontrer dans le document) ; part de β : β_k = 2|u_k|², u_k = (b_ρ − 2/ρ)/ρ,
b_ρ = ζ''/ζ'(ρ) − 2γ_E, calculée par mpmath (dérivées de Z), sans les premiers.

P1 (répulsion) : la proportion de zéros avec m_k < 0,1 est à ±30 % de la valeur GUE (surmise de Wigner, plus proche voisin)
    et au moins trois fois plus petite que la valeur de Poisson.
P2 (β lit les paires serrées) : sur les 10 % de zéros aux plus petits s_k, la pente de log β_k contre log s_k est entre −2,4 et −1,6.
P3 (part) : les 10 % de zéros aux plus petites marges portent entre 25 % et 40 % de Σ β_k (31 % observé sur 300 zéros avant cette prévision).
P4 (contrôle) : la somme partielle Σ β_k sur les 1 070 zéros redonne 0,540 ± 0,005 (valeur de la relecture B).
P5 (Lehmer) : la paire de Lehmer près de 7 005 a une marge m < 0,01, et chacun de ses deux zéros pèse dans β plus de 100 fois
    la médiane des zéros de 6 900 à 7 100.
Réfutation : marges distribuées comme Poisson (pas de répulsion), ou β_k sans relation avec s_k.
Exploratoire (non pré-enregistré) : marge locale lue directement sur la métrique des premiers pour les paires les plus serrées.
