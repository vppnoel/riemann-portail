# Termes en L² et L de Q(X) (GAP-3) — analyse (v3.6)

**Résultat principal, avec une correction de fond.** Les coefficients α, β ne sont pas ceux d'un développement
asymptotique en puissances de L : le « coefficient de L² » oscille de façon presque périodique. Ce que le
programme peut établir est (i) le développement de Q_η en η⁻³, η⁻², η⁻¹ (niveau abélien, moyenné), et
(ii) la forme **U(L) = (4κ/3)L³ + (α + Φ(L))L² + O(L)** avec Φ presque périodique, bornée, explicite.

Notation : U(L)=Q(e^L), ρ=½+iγ zéro simple, A_γ=2/ρ, b_ρ=2c₀(ρ)−2γ_E, u_γ=(b_ρ−2/ρ)/ρ ;  
s₃=Σ_{γ>0}|A|²/3, s₂=Σ_{γ>0}Re(A ū), s₁=Σ_{γ>0}|u|² ; α=2s₂, β=2s₁.

## 1. Développement de I(η)=Q_η (niveau abélien)

**Calcul local** (zéro simple ρ, u=t−γ, s−ρ=η+iu, |s|²=|ρ|²+η+η²+2γu+u²). Trois contributions à l'ordre η⁻² :
1. noyau principal : |2/(s−ρ)²|² = 4/(η²+u²)², ∫du = 2π/η³ ; le poids 1/|s|² donne 1/|ρ|²(1−η/|ρ|²+…) :  
   par zéro, (1/2π)·… = 1/(|ρ|²η³) − 1/(|ρ|⁴η²) ;
2. terme croisé avec b/(s−ρ) : 2Re[2b̄/((η+iu)²(η−iu))] = 4Re[b̄(η−iu)]/(η²+u²)², ∫ = 2π Re(b)/η² ;  
   par zéro : Re(b)/(|ρ|²η²) ;
3. les termes impairs en u, la courbure du poids et |b|²/|s−ρ|² ne contribuent qu'à l'ordre η⁻¹.

Somme sur les zéros (γ>0 et γ<0, Re b identique) : coefficient de η⁻² = Σ[Re b/|ρ|² − 1/|ρ|⁴] = **s₂**, 
et l'on vérifie Re(Aū)=2[Re b/|ρ|²−1/|ρ|⁴] ; de même le coefficient de η⁻¹ est s₁.
Laplace : Q_η = 2(6s₃/λ³ + 2s₂/λ² + s₁/λ), λ=2η, est donc **la même** prédiction que celle de la formule
explicite : deux dérivations indépendantes concordent.

**Contrôle numérique** (modèle local à 300 zéros, intégration directe de |G_N|²/|s|², `data/eta_expansion_model.csv`) :

| η | η³I | κ_N + s₂η | (η³I − κ_N − s₂η)/η² |
|---|---|---|---|
| 0,01 | 0,04170 | 0,04167 | 0,2353 |
| 0,02 | 0,04045 | 0,04035 | 0,2378 |
| 0,04 | 0,03810 | 0,03771 | 0,2430 |

Extrapolé à η→0 : 0,2327 ; valeur de s₁ : **0,2328**. Les coefficients η⁻³ (κ_N=0,04299), η⁻² (s₂=−0,13195) et
η⁻¹ (s₁) sont confirmés à 4 chiffres, termes croisés entre zéros inclus.

**Passage du modèle à ζ.** Il exige trois choses :
- *(H1)* RH et zéros simples ;
- *(H2)* convergence de Σ|b|²/|ρ|² et Σ|b|/|ρ|² : vraie sous la condition (2) de BCF + Lindelöf (voir COMPARAISON_BCF §3) ;
- *(H3)* contrôle des paires proches : le terme croisé entre deux pôles doubles vaut (1/2π)·8Re[(2η−id)⁻³]/(|ρ||ρ'|) (d=γ−γ'),
  borné par 8/(|ρρ'|max(2η,|d|)³). Pour d fixé il est O(1) (partie réelle O(η/d⁴)), mais une paire à distance ≲ η coûte η⁻³.
  Il suffit que M(η):=Σ_{|d|<1}|ρρ'|⁻¹max(η,|d|)⁻³ = o(η⁻²) (somme sur les paires de zéros).
  La borne triviale (≤ C log T voisins à distance ≤1) ne suffit que pour les hauteurs T ≳ η⁻¹log²T ; en dessous il
  faut un contrôle des petits écarts (répulsion), hors de portée de RH seule — attendu vrai sous GUE (densité d'écarts ∼ d²).
La queue |t|>Y=η^{-1-ε} est ≪ η^{-2+ε} par l'étape 3 du théorème : elle est négligeable.

## 2. Structure ponctuelle : Φ(L)

Avec B(t)=Σ_{γ>0}2Re[(A_γt+u_γ)e^{iγt}] et ∫₀^L t²e^{iδt}dt = L²e^{iδL}/(iδ)+O(L/δ²), les termes non diagonaux
d'ordre L² dans U(L)=∫₀^L B² sont :
Φ(L) = 2 Re Σ_{γ≠γ'} A_γĀ_{γ'} e^{i(γ−γ')L}/(i(γ−γ')) + 2 Re Σ_{γ,γ'} A_γA_{γ'} e^{i(γ+γ')L}/(i(γ+γ')),
sommes sur les paires γ,γ'>0 (l'une inclut les termes diagonaux γ=γ' de la seconde). Φ est presque périodique ;
elle est bornée si H_pair : Σ_{γ≠γ'}1/(|ρ||ρ'||γ−γ'|)<∞ (même mécanisme que H3, moment de l'écart inverse).

**Contrôle numérique** (`data/L2_oscillation.csv`, 300 zéros, L∈[6,15]) :
- (U_num − U_diag)/L² oscille entre −0,0235 et +0,0234, de moyenne 0,0025 (à comparer à |α|=0,264) ;
- la formule Φ(L) a une amplitude de −0,032 à +0,027 et une **corrélation 0,996** avec cet écart pour L≥9.
Le coefficient de L² est donc α+Φ(L) avec Φ≈±0,03 : ≈ 10 % de |α|, mais jamais constant.

## 3. Conséquences
1. **GAP-3 reformulé.** L'énoncé correct et le meilleur possible est U(L) = (4κ/3)L³ + O(L²) (sous H_pair), avec α moyenne
   de Besicovitch du coefficient de L². Un développement « (4κ/3)L³ + αL² + βL + o(L) » est faux au sens ponctuel.
2. **Explication de l'instabilité numérique.** Un ajustement libre de α,β sur L∈[8,15] ne peut converger : les
   oscillations Φ(L)L² (amplitude ≈ 3–6 sur U≈100) sont du même ordre que βL≈7 et que les erreurs de la queue de zéros.
3. **Rôle de α et β.** Ils restent bien définis comme coefficients de l'expansion de Q_η (moyennes), donc comme prédictions
   conditionnelles sur les échelles lissées — pas comme valeurs de U(L).
4. **Ce qu'il faudrait pour un théorème complet.** (a) H_pair/H3 prouvés ou supposés ; (b) un Tauber avec reste (Wiener–Ikehara
   quantitatif) pour passer de Q_η à une moyenne de Cesàro de U ; (c) la borne uniforme en L de Φ.
   Aucun n'est démontré ici.

## 4. Statut
| Énoncé | Statut |
|---|---|
| coefficients η⁻³, η⁻², η⁻¹ du modèle local | calcul + vérification numérique à 4 chiffres |
| même développement pour ζ | conditionnel à (H1)–(H3) ; esquisse |
| U(L)=(4κ/3)L³+(α+Φ)L²+O(L) | formule exacte pour N zéros (corrélation 0,996) ; limite N→∞ sous H_pair |
| α, β comme valeurs ponctuelles | **réfuté** |

## Correctif V6.13 (pré-relecture du Théorème B)

La valeur α ≈ −0,264 est une somme partielle sur 300 zéros, sans correction de queue. Avec la formule exacte Re b_ρ = −2θ′(γ) − 2γ_E et une correction de queue, α ≈ −0,3074, stable de 100 à 1 070 zéros ; β ≈ 0,64 reste une estimation heuristique. Avec ces valeurs, le modèle (4κ/3)L³ + αL² + βL reproduit Q(X) à 1–5 % près jusqu'à X = 10⁸. Les conclusions de cette note (α et β comme moyennes, pas comme valeurs ponctuelles) ne changent pas. Voir `1_Presentation/relecture/RELECTURE_THEOREME_B_EN.md`, §8.

