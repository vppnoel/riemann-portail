# Théorème — terme dominant de Q(X) sous RH (v3.4)

**Statut.** Preuve complète *modulo* cinq faits classiques F1–F5 (listés ci-dessous), conditionnelle
à RH. Elle suit la méthode de Cramér pour ψ(x)−x (même schéma : Plancherel de Mellin + analyse locale
aux zéros + Tauber). Non relue par un tiers ; l'antériorité exacte n'est pas recoupée ([À VÉRIFIER]).

## Énoncé

> **Théorème.** Supposons RH. Pour chaque zéro ρ de multiplicité m(ρ), posons A_ρ = m(ρ)(m(ρ)+1) et  
> S = Σ_{ρ distincts} A_ρ² / |ρ|²  (somme sur tous les zéros non triviaux, γ>0 et γ<0). Alors S<∞ et
> **Q(X) = ∫₁^X |C(x)|² x⁻² dx ∼ (S/3)(log X)³**  (X→∞).  
> Si les zéros sont simples : S = 4κ, soit **Q(X) ∼ (4κ/3)(log X)³**, κ = Σ_ρ 1/|ρ|² = 2+γ_E−log 4π.

Aucune hypothèse de simplicité n'est nécessaire. Pas de vitesse : le résultat est un équivalent.

## Faits classiques utilisés
- **F1** (partial fractions, Titchmarsh 9.6). Uniformément pour −1 ≤ σ ≤ 2, |t| ≥ 2 :  
  ζ'/ζ(s) = Σ_{|t−γ|<1} 1/(s−ρ) + O(log |t|).
- **F2** (Hadamard). Pour Re s ≥ ½, |s−1| ≥ ½ : (ζ'/ζ)'(s) = 1/(s−1)² − Σ_ρ (s−ρ)⁻² + O(1/|s|),
  la série convergeant absolument. *Contrôle numérique* (`v3.4`, 4 points, 300 zéros) :  
  l'écart vaut ≈ 0,5/|s| (0,0249 à |s|=20 ; 0,0059 à |s|=100).
- **F3** (comptage). N(T+1)−N(T) ≪ log T, comptés avec multiplicité ; donc m(ρ) ≪ log(|γ|+2).
- **F4** (Karamata). Si U est croissante, U(0)=0 et ∫₀^∞ e^{−λL}dU(L) ∼ c·λ^{−3} (λ→0⁺), alors U(L) ∼ c L³/Γ(4).
- **F5** (Plancherel de Mellin). f ∈ L¹∩L²(dx/x) ⇒ ∫|f|²dx/x = (1/2π)∫|f̃(t)|²dt, f̃(t)=∫f(x)x^{−it}dx/x.

## Preuve

**Étape 1 — a priori sous RH.** D'après L6 (Perron à la droite Re s = b, déplacement de contour jusqu'à
Re s = ½+ε), C(x) ≪ x^{1/2+ε}, donc Q(X) ≪ X^{2ε} pour tout ε>0.

**Étape 2 — identité de Plancherel.** Fixons η ∈ (0, ½], σ = ½+η et posons
Q_η := ∫₁^∞ |C(x)|² x^{−2−2η} dx. L'étape 1 donne Q_η<∞. Par Cauchy–Schwarz comme dans L6,
f(x)=C(x)x^{−σ}·1_{x≥1} est dans L¹(dx/x) (bornée par Q_{η'}^{1/2}, η'<η) et dans L²(dx/x).  
Sa transformée est F(σ+it)=∫₁^∞ C(x)x^{−σ−it−1}dx, holomorphe sur Re s>½ et égale à G(s)/s sur Re s>1,
donc partout sur Re s>½ par prolongement analytique. D'après F5 :  
**Q_η = (1/2π) ∫_ℝ |G(σ+it)|² / |σ+it|² dt =: I(η).**

**Étape 3 — queue uniformément petite.** Pour |t|≥2 et σ=½+η, F1 et F2 donnent, avec Z(t) = #{ρ : |γ−t|<1} ≪ log t
(F3) et W(t) := Σ_{|γ−t|<1} 1/((t−γ)²+η²) :  
|q| ≤ (Z·W)^{1/2} + O(log t), |q'| ≤ W + O(log t) (les zéros éloignés contribuent Σ|s−ρ|⁻² ≪ log t), d'où  
**|G| ≪ (log t)·W(t) + (log t)².**  
Par Cauchy–Schwarz, W² ≤ Z·Σ_{|γ−t|<1}((t−γ)²+η²)⁻², et ∫_ℝ dt/((t−γ)²+η²)² = π/(2η³), donc  
∫_T^{2T} W² dt ≪ (log T)·(T log T)·η⁻³. Il vient ∫_T^{2T}|G|² dt ≪ T (log T)⁴ η⁻³, et avec le poids 1/|s|² ≤ T⁻² :  
**∫_{|t|≥Y} |G|²/|s|² dt ≪ (log Y)⁴ / (Y η³)**, uniformément en η ∈ (0,½]. Ce terme est ≤ ε_Y/η³ avec ε_Y → 0.

**Étape 4 — partie locale |t|≤Y.** Soient ρ_1,…,ρ_J les zéros distincts avec |γ|≤Y+2 (J fini, écart minimal d_Y>0).
Par L5, G(s) = Σ_k [A_k/(s−ρ_k)² + b_k/(s−ρ_k)] + R(s), R holomorphe et bornée (par M_Y) sur la bande compacte
{½≤σ≤¾, |t|≤Y+1}. Notons ‖·‖ la norme de L²(|s|⁻²dt). Alors :  
- ‖A_k/(s−ρ_k)²‖² = (|A_k|²/|ρ_k|²)·(π/(2η³))(1+O_Y(η^{1/2})) pour |γ_k|<Y−1 (le noyau est concentré à l'échelle η, le
  poids |s|⁻² varie à l'échelle |ρ_k|) ; pour |γ_k| ∈ [Y−1, Y+2] c'est au plus cette valeur ;
- produits croisés entre zéros distincts : O_Y(η⁻¹) (car |ρ_j−ρ_k|≥d_Y) ;
- reste Σ b_k/(s−ρ_k)+R : ‖·‖² = O_Y(η⁻¹), d'où une contribution croisée O_Y(η⁻³ᐟ²·η⁻¹ᐟ²)=O_Y(η⁻²).  

Donc, en divisant par 2π : η³ ∫_{|t|≤Y}|G|²/(2π|s|²) dt ∈ [S_{Y−1}/4 − o(1), S_{Y+2}/4 + o(1)] quand η→0,
où S_y = Σ_{|γ|≤y} A_ρ²/|ρ|².

**Étape 5 — limite de Q_η.** S<∞ car A_ρ ≪ (log|γ|)² (F3) et le nombre de zéros avec |γ|~T est ≪ T log T, donc Σ_{|γ|~T}A²/|ρ|² ≪ (log T)⁵/T.
Combinant 3 et 4, puis Y→∞ (S_{Y+2}−S_{Y−1} → 0) :  
**lim_{η→0⁺} η³ Q_η = S/4.**

**Étape 6 — Tauber.** Avec U(L)=Q(e^L) croissante, U(0)=0 et λ=2η, Q_η = ∫₀^∞ e^{−λL}dU(L) ∼ (S/4)(λ/2)⁻³ = 2S λ⁻³.
Par F4, U(L) ∼ 2S L³/6 = S L³/3. ∎

## Contrôles numériques (illustratifs, pas des preuves)
- Constantes : ∫dt/(t²+η²)² = π/(2η³) ; Laplace de AL³ = 6A/λ⁴ ; S=4κ ⇒ S/3=4κ/3 (tests dans `tests/`).
- Niveau abélien (`scripts/run_abelian_check.py`, `data/abelian_check.csv`) : à η=0,2, η³Q_η mesuré = 0,0279 ; la prédiction
  κ + (α/2)η + (β/2)η² avec α,β calculés sur 300 zéros vaut 0,0291 (écart 4 %) ; le rapport mesure/prédiction diagonale
  est 0,96 (η=0,2), 0,84 (η=0,25) puis se dégrade pour η grand, où l'intégrale pondère les petits L, que le polynôme
  diagonal ne décrit pas (autres pôles de G). Seuls η ≤ 0,25 sont informatifs.

## Ce que le théorème n'est pas
- Il **ne prouve pas RH** : il décrit Q *si* RH est vraie. La réciproque est L6.
- Il ne donne **ni vitesse, ni les termes en L², L** (GAP-3) : la méthode de Tauber ne voit que l'équivalent. **v3.6** : ces termes ne sont d'ailleurs pas des constantes — le coefficient de L² oscille de façon presque périodique (`ALPHA_BETA_ANALYSE.md`).
- C'est l'analogue, pour G, du théorème de Cramér sur ∫(ψ(x)−x)²x⁻²dx, avec un pôle double au lieu d'un pôle simple
  (d'où L³ au lieu de L). Sa valeur est d'exactitude, non de nouveauté.
