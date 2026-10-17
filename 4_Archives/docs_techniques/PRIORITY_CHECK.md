# Recherche de priorité — Théorèmes A et B (v4.5)

**Méthode.** Quatre requêtes web le 2026-10-04 ; résumés/pages seulement, aucun texte lu en entier. L'absence de résultat dans ces requêtes **ne prouve pas** l'absence d'antériorité.

| Sujet | Trouvé | Statut |
|---|---|---|
| Moyenne quadratique de ψ(x)−x sous RH | Cramér (1922), *Ein Mittelwertsatz in der Primzahltheorie* ; Brent–Platt–Trudgian, J. Number Theory 238 (2022) 740–762 (limsup I(X)/X² ≤ 0,8603 avec I(X)=∫_X^{2X}(ψ−x)²dx ; I(X)/X² n'a pas de limite ; la moyenne **pondérée logarithmiquement** G(X) ∼ c₁ log X, c₁ lié à Σ1/|ρ|²) | [VÉRIFIÉ PAGE/ABSTRACT, talk de Brent] — **antériorité du cas pôle simple** |
| Théorème B (pôle double, c=Λ∗Λ−Λ log+2γΛ) | aucune occurrence trouvée | [NON TROUVÉ] — à confirmer par un spécialiste |
| Équivalences de RH par sommes tordues de Λ^{∗k} et Λ_k(n)=Σ_{d|n}μ(d)(log n/d)^k | Gonek–Graham–Lee ; Banks–Sinha (abstract : équivalence à des estimations asymptotiques de Σ Λ^{∗k}(n)n^{−iy} et Σ Λ_k(n)n^{−iy}) | [VÉRIFIÉ ABSTRACT] — voisin de Théorème A, **non comparé en détail** |
| Constante κ et d_N² | Burnol ; Bettin–Conrey–Farmer | [LU/VÉRIFIÉ] (déjà dans SOURCES) |

## Lecture
1. **Théorème B est très probablement l'analogue « pôle double » de la loi logarithmique de Cramér** (G(X) ∼ c₁ log X pour ψ ; ici U(L) ∼ (S/3)L³). La nouveauté se limite, au mieux, à l'objet c et à la constante S ; ne pas présenter B comme un résultat de principe.
2. **Remarque de structure.** Les fonctions de von Mangoldt généralisées Λ_k ont pour série (−1)^kζ^{(k)}/ζ ; pour k=2 : q²−q′, dont le coefficient de (s−ρ)^{−2} vaut m²−m = m(m−1) et **s'annule aux zéros simples**. Notre G = f″/f + 2γ f′/f = q²+q′+2γq a le coefficient m(m+1) > 0. Les deux objets sont donc distincts (ζ^{(2)}/ζ contre (1/ζ)^{(2)}/(1/ζ)) ; la parenté avec Banks–Sinha est celle de la famille, non de l'identité. (Calcul de l'auteur de ce package, à faire vérifier.)
3. Un préprint non évalué (preprints.org, 2026) prétend prouver RH par une estimation en moyenne quadratique de ψ ; il n'est pas cité et n'a aucun statut (« not peer-reviewed »).

## À faire par un spécialiste
Indiquer si B (ou sa méthode : Plancherel de Mellin à Re s = ½+η, analyse locale, Tauber de Karamata) figure déjà dans la littérature, pour ψ ou pour d'autres séries à pôles doubles.
