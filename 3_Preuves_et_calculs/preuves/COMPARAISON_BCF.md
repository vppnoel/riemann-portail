# Comparaison avec Bettin–Conrey–Farmer (BCF) — v3.3

Source lue en entier : arXiv:1211.5191 (Proc. Steklov 280, 2013). Tout ce qui suit sur BCF est
tiré de ce texte ; les parties « analyse » sont de moi et marquées comme telles.

## 1. Dictionnaire exact

| | BCF | Ce programme |
|---|---|---|
| Polynôme | V_N(s)=Σ_{n≤N}(1−log n/log N)μ(n)n^{-s} (coupure en N) | a(n)=μ(n)(log²n−2γ_E log n), **sans** coupure |
| Lien avec f=1/ζ | V_N ≈ f + f'/log N (Lemme 2 de BCF) | Σ a(n)n^{-s} = f''+2γ_E f' |
| Objet d'erreur | 1−ζV_N ≈ −q/log N (+ queue d>N) : **premier ordre** | G=ζ(f''+2γ_E f')=q²+q'+2γ_E q : **second ordre** |
| Singularités aux zéros | pôle simple de q → énergie en 1/log N | double pôle m(m+1)/(s−ρ)² → énergie (log X)³ |
| Constante | Σ m²/\|ρ\|² (Burnol) = 2+γ−log 4π si zéros simples | (4/3)·(2+γ−log 4π)·L³ (terme diagonal, zéros simples) |
| Espace | L²(dt/(¼+t²)) sur Re s=½ | Mellin–Plancherel, L²(dx/x²) ; équivalent formel à L²(0,1) (L10) |
| Ce qu'on prouve | RH + hypothèse (2) ⇒ d_N² ∼ κ/log N | L6 : exposant de Q ⇔ Θ (inconditionnel) |

L'identité de premier ordre est **vérifiée exactement** (test `test_bcf_first_order_identity`) :
coefficient de n^{-s} dans ζV_N = [n=1] + Λ(n)/log N − Σ_{d|n,d>N}μ(d)(1−log d/log N).
Les deux programmes sont donc la même mécanique de zéros à deux ordres de dérivation en s ;
la constante κ est la même parce que les deux énergies sont diagonalisées par Σ1/\|ρ\|².

## 2. Ce que le programme apporte / n'apporte pas
- **Apporte** (modeste) : une observable (Q) dont l'exposant mesure Θ inconditionnellement (L6), et
  un double pôle universel qui rend la formule explicite propre.
- **N'apporte pas** : ni nouvelle constante, ni nouvelle équivalence plus faible que NB–Báez-Duarte.
  Le résultat BCF est plus fort sur son terrain (il fixe la constante de d_N², sous hypothèses).

## 3. Conséquence sur GAP-3 (analyse, esquisse [STD])
Les coefficients α, β font intervenir c₀(ρ)=ζ''(ρ)/(2ζ'(ρ)), donc **1/ζ'(ρ)** — exactement la
quantité contrôlée par la condition (2) de BCF : Σ_{|γ|≤T}1/|ζ'(ρ)|² ≪ T^{3/2−δ}.
Sous RH, zéros simples, Lindelöf (donc ζ''(ρ) ≪ |ρ|^ε par Cauchy, comme dans BCF) et (2) :
\|u_ρ\| ≪ \|ρ\|^{ε−1}/\|ζ'(ρ)\| + \|ρ\|^{-2}, et la sommation par parties donne
Σ\|u_ρ\|² < ∞ ; Cauchy–Schwarz donne Σ\|A_ρ u_ρ\| < ∞. **Les séries α et β convergent donc
absolument sous les mêmes hypothèses que BCF**. La convergence de la série ne suffit pas à
contrôler les termes hors diagonale : GAP-3 reste ouvert pour L² et L (v3.6 : voir `ALPHA_BETA_ANALYSE.md` ; α,β sont des moyennes, le coefficient ponctuel de L² oscille).

## 4. Test numérique de la condition (2) (`scripts/run_gonek_moment.py`)
S(T)=Σ_{|γ|≤T}1/|ζ'(ρ)|², comparé à la conjecture de Gonek/Hughes–Keating–O'Connell (6/π³)T :

| n zéros | T | S(T) | (6/π³)T | ratio |
|---|---|---|---|---|
| 30 | 101,3 | 21,78 | 19,61 | 1,111 |
| 100 | 236,5 | 48,20 | 45,77 | 1,053 |
| 200 | 396,4 | 76,26 | 76,70 | 0,994 |
| 300 | 541,9 | 102,30 | 104,85 | 0,976 |

Exposant effectif entre T≈99 et T≈542 : **0,915** (la condition (2) demande < 3/2). Plus petit
\|ζ'(ρ)\| : 0,793, au premier zéro. C'est de la cohérence (300 zéros), pas une preuve.

## 5. Non fait, et pourquoi
Reproduire numériquement le théorème de BCF (d_N² log N → κ) par intégration directe sur la droite
critique est coûteux : heuristiquement, pour N~10³ la queue t>N pèse autant que le corps de l'intégrale
(estimation non vérifiée), ce qui exigerait une hauteur d'intégration ≫ N. Voie recommandée : matrice
de Gram de Nyman–Beurling, avec produit scalaire ∫₁^∞{x/a}{x/b}x⁻²dx ; sa queue au-delà de X vaut
≈ (¼ + gcd(a,b)²/(12ab))/X, ce qui relie directement la covariance L8 à ce calcul (activité 8).
