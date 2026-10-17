# Positionnement bibliographique (v3.2)

Statut des sources : **[VÉRIFIÉ]** = énoncé relu dans le résumé ou la page officielle consultée
le 2026-10-03 ; **[À VÉRIFIER]** = attribution plausible non recoupée. Aucune nouveauté n'est
revendiquée tant qu'une ligne reste [À VÉRIFIER].

| Objet du package | Ce que dit la littérature | Statut |
|---|---|---|
| Critère de Nyman–Beurling | RH ⇔ approximation de χ_(0,1) par des dilatations de la partie fractionnaire (Nyman 1950, Beurling 1955) | [VÉRIFIÉ] (cité par Landreau–Richard, Exp. Math. 11) |
| Renforcement aux dilatations entières ρ_k, k ≤ N | Báez-Duarte, *Rend. Mat. Acc. Lincei* 14 (2003) ; version générale *Publ. Inst. Math.* 78 (2005) | [VÉRIFIÉ] (références croisées) |
| Forme Dirichlet : d_N² = inf (1/2π)∫\|1 − ζA_N(½+it)\|² dt/(¼+t²) | Formulation de Báez-Duarte ; RH ⇔ d_N → 0 | [VÉRIFIÉ] (Bettin–Conrey–Farmer) |
| Constante κ = 2+γ−log 4π | Borne inférieure de Burnol : liminf d_N² log N ≥ Σ m(ρ)²/\|ρ\|² (zéros sur la droite) ; BCF : sous RH et Σ1/\|ζ'(ρ)\|² ≪ T^{3/2−δ}, d_N² ∼ (2+γ−log 4π)/log N | [VÉRIFIÉ] (arXiv:1211.5191) |
| Autocorrélation multiplicative A(λ)=∫₀^∞{λt}{t}t⁻²dt | Báez-Duarte–Balazard–Landreau–Saias, *Ramanujan J.* 9 (2005) ; Balazard–Martin (arXiv:1305.4395) | [VÉRIFIÉ] (titres, résumés) |
| Aspects numériques de NB | Landreau–Richard, *Exp. Math.* 11 (2002) | [VÉRIFIÉ] |
| Covariance gcd(d,e)²/(12de) des dents de scie (L8) | ∫₀¹((ax))((bx))dx = gcd(a,b)²/(12ab) : formule de **Franel (1924), démontrée par Landau (1924)** ; citée telle quelle dans la littérature sur les sommes de Dedekind et les « intégrales de Franel », où elle apparaît aussi dans l'étude de l'appartenance à l'adhérence de NB | [VÉRIFIÉ] (arXiv:2211.06504, arXiv:1306.3315, arXiv:2009.14070). Le lien exact avec A(λ) et les sommes de cotangentes (Vasyunin) reste [À VÉRIFIER] |
| Zéros : densité N(σ,T) ≤ T^{30(1−σ)/13+o(1)} | Guth–Maynard, *Ann. of Math.* 203 (2026) ; améliore 12/5 (Huxley) ; gain près de σ = 3/4 | [VÉRIFIÉ] (page de la revue, arXiv:2405.20552) |

## Ce que cela change pour le package
1. **κ n'est pas une découverte du programme** : c'est la constante de Burnol/BCF. Elle apparaît
   dans Q parce que le terme dominant diagonal de la formule explicite vaut Σ1/\|ρ\|² ;
   rien ne prouve que les deux objets (d_N et Q) soient liés au-delà de cette coïncidence
   de constante.
2. **L10 relie Q à la géométrie NB**, mais Q utilise les coefficients a(d) = μ(d)(log²d − 2γ log d),
   différents de ceux de BCF. Une comparaison directe des deux familles d'approximants est à faire.
3. **L7 (canaux terminaux)** est un corollaire élémentaire de l'identité Σ_{q|d}μ(d)d^{-s}=μ(q)q^{-s}∏_{p|q}(1−p^{-s})^{-1}/ζ(s) (forme standard d'une fonction multiplicative) ; **aucune nouveauté n'est revendiquée** (v3.8).


## Mise à jour v3.5
La constante κ est reproduite numériquement comme limite attendue de d_N² log N (1,07 κ à N=20–30, voir `docs/NB_GRAM.md`) ; cela confirme la cohérence avec Burnol/BCF sans rien prouver.


## Mise à jour v3.8
L8 est une formule classique (Franel 1924, Landau 1924) : ne pas la présenter comme un résultat du programme. Seules restent [À VÉRIFIER] : le lien exact avec A(λ)/Vasyunin ; l'antériorité du théorème du terme dominant (analogue de Cramér) ; les énoncés du critère de Weil et de Halász–Montgomery cités de mémoire.
