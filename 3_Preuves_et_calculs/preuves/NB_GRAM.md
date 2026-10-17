# Matrice de Gram de Nyman–Beurling et reproduction de d_N² (v3.5)

## Dictionnaire (vérifié numériquement)
ρ_k(x)={1/(kx)}, χ=1_{(0,1)}. Mellin : ρ_k ↔ −ζ(s)k^{-s}/s, χ ↔ 1/s. Pour A(s)=Σa_k k^{-s} :
(1/2π)∫|1−ζA(½+it)|² dt/(¼+t²) = ‖χ + Σa_kρ_k‖²_{L²(0,∞)} (version de BCF, avec la contrainte
« pas de condition Σa_k/k=0 »). Avec y=1/x :
- G(a,b)=⟨ρ_a,ρ_b⟩ = ∫₀^∞{y/a}{y/b}y⁻²dy = 1/(ab)+∫₁^∞… ; G(a,b)=G(a/g,b/g)/g ;
- ⟨χ,ρ_a⟩ = (log a + 1 − γ)/a (exact) ; ‖χ‖²=1.

Calcul de G : somme exacte par cellules entre multiples de a et b jusqu'à Y=Kℓ (ℓ=ab/g²), puis queue
M/Y + F̄/Y², M = ¼ + gcd²/(12ab) (c'est là qu'intervient la covariance L8), F̄ déterminé par extrapolation
de Richardson entre Y et 2Y. Précision visée ≈ 10⁻¹².

## Contrôles
| Test | Résultat |
|---|---|
| G(1,1) vs log 2π − γ | 1,26066140150780 vs …81 (10⁻¹⁴) |
| ‖χ+ρ₁‖² (Gram) vs intégrale critique | 3,1062 vs 3,1078 (0,05 %, queue approchée) |
| E(V₁₀) (Gram) vs intégrale critique | 0,6715 vs 0,6758 (0,6 %, queue approchée) |
| Stabilité de d_N² sous bruit relatif 10⁻¹¹ sur G | variation < 2·10⁻¹¹ ; cond(G)≈3·10³ à N=30 |

## Résultats (`data/nb_gram_dN.csv`, `scripts/run_nb_gram.py`)
| N | log N | d_N² optimal | d_N² · log N | κ/log N | E(V_N) · log N |
|---|---|---|---|---|---|
| 5 | 1,61 | 0,03610 | 0,0581 | 0,0287 | 2,110 |
| 10 | 2,30 | 0,02377 | 0,0547 | 0,0201 | 1,546 |
| 20 | 3,00 | 0,01650 | 0,0494 | 0,0154 | 1,229 |
| 30 | 3,40 | 0,01453 | 0,0494 | 0,0136 | 1,104 |
| 50 | 3,91 | — | — | 0,0118 | 0,951 |
| 120 | 4,79 | — | — | 0,0096 | 0,785 |
| 200 | 5,30 | — | — | 0,0087 | 0,714 |

κ = 2+γ−log 4π = 0,04619.

## Lecture
1. **d_N² log N reste au-dessus de κ et s'en rapproche** : 1,26 κ (N=5) → 1,07 κ (N=20, 30). C'est cohérent avec la borne
   inférieure de Burnol (liminf d_N² log N ≥ κ sous RH et zéros simples, rapportée par BCF) et avec la conjecture
   d_N² ∼ κ/log N. Ce n'est pas une confirmation : N≤30, un seul point par ordre de grandeur, la convergence en 1/log N
   est lente, et l'optimum n'a pas été calculé pour N>30.
2. **Le polynôme de BCF n'est pas encore asymptotique** : E(V_N)·log N décroît de 2,11 à 0,71 (N=5→200) mais
   reste ≈ 15 κ. L'équivalent E(V_N) ∼ κ/log N de BCF n'est donc pas visible à ces tailles : V_N est très sous-optimal
   pour N petit. On ne peut pas conclure sur la limite par ces calculs.
3. **Pont avec le programme.** La même constante κ gouverne d_N² (premier ordre, 1/log N) et Q(X)
   (second ordre, (4κ/3)log³X) : les deux sont des énergies diagonales Σ1/|ρ|², l'une pour un pôle simple,
   l'autre pour un pôle double. Le calcul de Gram utilise la covariance gcd² (L8) pour sa queue.

## Limites
Le calcul est exact à ≈10⁻¹² mais borné à N≲200 pour V_N (≈200 s) et N≲30 pour l'optimum. Aucune
information sur le comportement asymptotique réel de d_N² au-delà ; RH n'est pas testée (d_N→0 ⇔ RH est un
énoncé asymptotique).


## Extension de l'optimum à N ≤ 100 (v3.8, `scripts/run_nb_gram_ext.py`, `data/nb_gram_dN_ext.csv`)
Gram complète 100×100 (5 050 entrées, calcul reprenable) ; solveur en précision étendue (80 chiffres).
Stabilité : bruit relatif 10⁻¹⁰ sur G ⇒ variation de d₁₀₀² de 1,1·10⁻¹⁰ ; cond(G) ≤ 3,7·10⁴.

| N | d_N² | d_N² · log N | rapport à κ | cond(G) |
|---|---|---|---|---|
| 10 | 0,02377 | 0,05474 | 1,185 | 3,3·10² |
| 20 | 0,01650 | 0,04944 | 1,070 | 1,4·10³ |
| 30 | 0,01453 | 0,04942 | 1,070 | 3,1·10³ |
| 40 | 0,01272 | 0,04690 | 1,015 | 5,7·10³ |
| 50 | 0,01187 | 0,04643 | 1,005 | 9,4·10³ |
| 60 | 0,01147 | 0,04697 | 1,017 | 1,3·10⁴ |
| 70 | 0,01114 | 0,04732 | 1,025 | 1,8·10⁴ |
| 80 | 0,01098 | 0,04813 | 1,042 | 2,4·10⁴ |
| 90 | 0,01067 | 0,04803 | 1,040 | 2,9·10⁴ |
| 100 | 0,01019 | 0,04692 | 1,016 | 3,7·10⁴ |

**Lecture.** Pour N=40…100, d_N² log N reste entre 1,005 κ et 1,042 κ : l'estimation d_N² ∼ κ/log N est vérifiée à 1–4 % près sur cette plage.
Mais la suite **n'est pas monotone** (1,005 à N=50, 1,042 à N=80, 1,016 à N=100) : d_N² dépend de l'arithmétique de N, et les oscillations (±2 %)
sont du même ordre que l'écart à κ. Elle ne dit rien sur la limite : la conjecture est asymptotique, la correction en 1/log N est de l'ordre de
quelques pour cent à log N ≈ 4,5, et la borne de Burnol est un liminf. On ne doit pas lire « d_N² log N ≥ κ pour tout N » dans ces chiffres :
la plage 40–100 passe très près de κ (1,005) et rien n'interdit de passer en dessous.
