# Prévisions V6.17 — « La Rencontre en degré 2 » et son pendant — écrites avant tout calcul — 2026-10-10T11:55:08Z

Rien de ce qui suit n'a été calculé au moment de l'écriture : ni zéros de L(Δ, s) au-delà de t = 232, ni statistiques de
marges pour Δ ou pour ζ·L(χ5), ni angles de Satake, ni courbes elliptiques. Seules des valeurs théoriques (intégrales de
Sato–Tate, formule de superposition, N_eff de Bogomolny et al. 2006) ont été évaluées.

Objets.
- Δ : zéros de L(Δ, s) (poids 12, niveau 1) jusqu'à la hauteur atteinte (cible t = 1 000, au moins 1 200 zéros), par un
  évaluateur nouveau (rotation du contour de Mellin), validé contre les zéros V6.15 (t ≤ 232) et contre mpmath plus haut.
- ζ_K = ζ·L(χ5) (corps Q(√5), degré 2 non primitif) : réunion des zéros de ζ et de L(χ5) jusqu'à t = 600 (fichiers existants).
- Côté premiers : angles de Satake θ_p de Δ, λ(p) = 2 cos θ_p, p ≤ 25 000.
- Modèle réduit : toutes les courbes y² = x³ + ax + b sur F_p, p ∈ {101, 211, 307, 401, 503}.

Marge. Pour un zéro : m = 1 − sinc²(π s), s = écart au plus proche voisin normalisé par la densité locale de la fonction
(fenêtre de Heisenberg, document 40). Pour un premier ou une courbe de genre 1 : m = 1 − λ²/4 = sin²θ (déterminant
normalisé de la métrique 2×2 des deux racines ; pour une courbe, c'est 1 − ρ₁², la marge de Castelnuovo du document 28).

Référence GUE : simulation exacte d'ensembles unitaires circulaires (CUE, N = 200), et non plus la surmise de Wigner.

P1 (répulsion en degré 2) : la proportion de zéros de Δ de marge < 0,1 est au moins 10 fois sous la valeur de Poisson.
P2 (effet de hauteur) : le rapport f_Δ / f_CUE est plus grand que le même rapport pour ζ (données V6.16, même référence),
    et il est dans [0,5 ; 1,2] au seuil 0,1 et dans [0,6 ; 1,1] au seuil 0,3. Raison : la densité de Δ est double à
    hauteur égale ; si la taille effective N_eff = (2π × densité)/√(12Λ) de Bogomolny et al. s'applique avec un Λ du même
    ordre, Δ (N_eff ≈ 2,2) est bien plus près de la limite GUE que ζ (N_eff ≈ 1,1).
P3 (superposition sans répulsion mutuelle) : pour ζ_K, la proportion de zéros de marge < 0,1 est dans [14 % ; 20 %]
    (théorie : 4·x·w₁·w₂ ≈ 17 %, x = 0,178) ; au moins 90 % des paires de marge < 0,1 sont mixtes (un zéro de ζ, un de L(χ5)) ;
    aucune collision : la plus petite distance entre un zéro de ζ et un zéro de L(χ5) dépasse 10⁻⁶.
P4 (rencontre locale aux premiers, Δ) : la proportion de premiers p ≤ 25 000 avec sin²θ_p < 0,1 est à ±30 % de la valeur
    de Sato–Tate (1,385 %) et au moins 10 fois sous la valeur d'angles uniformes (20,5 %) ; la plus petite marge est > 0
    (jamais de collision α_p = β_p : 2p^(11/2) est irrationnel) ; test de Kolmogorov–Smirnov contre Sato–Tate : p-valeur > 0,01.
P5 (Modèle réduit, genre 1) : sur les courbes sur F_p, la proportion de marges < 0,1 est à ±30 % de Sato–Tate (agrégée sur
    les cinq p) ; aucune marge nulle sur F_p ; au deuxième étage de la tour (F_{p²}) des collisions existent et ce sont
    exactement les courbes supersingulières (a_p = 0), où la forme de Castelnuovo devient dégénérée (ρ₂ = 1) sans que RH
    soit violée ; leur proportion décroît quand p croît.
Réfutation : Δ sans répulsion (P1), ζ_K avec répulsion mutuelle (P3), angles de Satake ou courbes uniformes (P4, P5).
