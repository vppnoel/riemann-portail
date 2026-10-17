# Peut-on lever l'hypothèse (H3) de la Proposition C ? (v4.7)

**Réponse courte : non, avec ce que je trouve dans la littérature ; mais (H3) peut être énoncée comme une condition précise sur les petits écarts.** Rien ici n'est démontré ; les sources récentes sont lues sur résumés/pages (§5).

## 1. Ce que (H3) demande exactement
Dans l'expansion de I(η), le terme croisé entre deux zéros ρ, ρ' à distance d = γ−γ' vaut (1/2π)·8·Re[(2η − id)⁻³]/(|ρ||ρ'|), de noyau
K_η(d) = (8η³ − 6ηd²)/(4η²+d²)³. Deux faits :
- **∫K_η(d)dd = 0** (vérifié numériquement à 10⁻¹⁴ pour η = 0,01 ; 0,05 ; 0,1) : K_η n'est pas une approximation de delta, c'est un noyau de moyenne nulle ;
- pour |d| ≫ η, K_η ≈ −6η/d⁴ ; pour |d| ≲ η, |K_η| ≲ η⁻³.
Seules donc comptent (a) les paires à distance ≲ η, (b) la queue −6η/d⁴ sommée sur les petits écarts.

## 2. Condition suffisante précise (esquisse, facteurs logarithmiques non revérifiés)
Soit N_gap(T;δ) = #{(γ,γ') : 0<γ,γ'≤T, 0<|γ−γ'|≤δ}. Les paires à hauteur ~T ont un poids |ρρ'|⁻¹ ≈ T⁻², donc leur contribution au terme η⁻³ est ≲ η⁻³·Σ_{T dyadique}T⁻²·N_gap(T;η).
**(H3⋆)** : il existe ε>0 et C tels que, pour T≥2 et 0<δ≤1/log T, N_gap(T;δ) ≤ C·T·(log T)·(δ log T)^{1+ε}.
Alors la somme vaut O(η^{−2+ε}·polylog) = o(η⁻²) (les paires avec η<|d|<1/log T apportent O(1) par la queue −6η/d⁴). Sous GUE (densité d'écarts ∼ d², donc exposant 2), (H3⋆) est attendue ; l'exposant 1+ε signifie « un peu mieux que linéaire ».
(H3⋆) est un énoncé asymptotique : toute famille finie de zéros la satisfait avec une constante C assez grande, donc l'obstruction est à hauteur infinie.

## 3. Ce que fournissent les résultats connus
- **Montgomery (1973)** : F(α,T) asymptotique pour 0≤α≤1 sous RH. Un test de Fourier à support dans [−1,1] résout des échelles ≳ 1 espacement moyen (2π/log T), pas les échelles ≪ 1/log T qui comptent ici : l'exposant en δ n'est pas amélioré en dessous de cette échelle.
- **Version inconditionnelle (Baluyot–Goldston–Suriajaya–Turnage-Butterbaugh, Acta Arith. 214 (2024))** : même échelle ; la somme porte sur tous les zéros avec un poids ne dépendant que de γ−γ', ce qui est le cadre de nos termes croisés (zéros non supposés sur la droite), mais l'échelle reste ≳ 1/log T.
- **Proportions de zéros simples sur la droite (Alpöge–Furman 2026 ; Lamzouri 2026)** : plus de 67,25 %. Résultat de type « proportion », sans borne sur les écarts : il ne minore aucun écart ni ne majore N_gap en dessous de l'espacement moyen.
- À ma connaissance, aucune minoration inconditionnelle des écarts entre zéros consécutifs (même sous RH) n'est connue ([À VÉRIFIER] par un spécialiste).
Conclusion : (H3⋆) est précisément un énoncé de répulsion sous l'espacement moyen, que ni la corrélation de paires (portée α<1) ni les résultats de proportions ne donnent.

## 4. Données (300 premiers zéros, `scripts/run_h3_gaps.py`, `data/h3_gaps.csv`)
| Mesure | Valeur |
|---|---|
| plus petit écart | 0,418 (γ≈540) |
| plus petit écart normalisé (écart / 2π·log⁻¹) | 0,291 ; 10 plus petits : 0,29–0,39 |
| E[1/s] sur les écarts normalisés | 1,16 (finie, comme attendu sous GUE) |
| part des écarts normalisés < 0,3 | 0,67 % |
| Σ_{γ≠γ'}1/(\|ρ\|\|ρ'\|\|γ−γ'\|), N = 25, 50, 100, 200, 300 | 0,0211 ; 0,0307 ; 0,0408 ; 0,0505 ; 0,0557 |
| part des 5 paires les plus proches dans cette somme (N=300) | 0,21 % |
La somme de paires croît encore lentement ; l'analyse donne une queue ∼ log³T·loglog T/T ≈ 0,1–0,2 à T≈540 : on ne peut pas conclure à la convergence numériquement, seulement l'absence de domination par de petits écarts.

## 5. Statut des sources (v4.7)
Lues sur résumés/pages le 2026-10-04, pas en entier : Alpöge–Furman arXiv:2608.13637 (v1 : ≥ 2/3 simples sur la droite et ≥ 5/6 distincts ; v2 : 0,6725) ; Lamzouri arXiv:2609.02882 (>67,25 % simples sur la droite, ≥ 83,62 % distincts, ≥ 88,76 % simples ou sur la droite) ; Baluyot–Goldston–Suriajaya–Turnage-Butterbaugh, Acta Arith. 214 (2024) 357–376 (≥ 61,7 % simples sous une hypothèse de proximité de la droite ; ≥ 67,9 % sous RH par le théorème de Montgomery). Selon MathWorld, la preuve d'Alpöge–Furman a été trouvée par une exécution autonome d'un modèle de recherche d'Anthropic et comprend une formalisation Lean.
