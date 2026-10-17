# Prévisions V6.58 — D'où vient le signe dans le Modèle réduit : comptage, degré, ou carré ? (écrites avant le calcul)

Auteur et titulaire des droits : Vincent NOËL. Écrit le 17 octobre 2026 à 08:50 UTC (10 h 50 à Bruxelles), avant tout calcul.

Objets : les 425 courbes et les 220 faux jumeaux du Modèle réduit (docs 28, 46). Pour chaque polynôme P (polynôme L), on note χ(T) = T^{2g} P(1/T), de racines α₁…α_{2g}, et l'algèbre K = ℚ[T]/(χ) avec l'involution ι(T) = q/T.
Trois niveaux de positivité, tous calculables à partir des seuls comptages de points :
1. le comptage : nombres de points fermés a_d ≥ 0 (vrai pour les 425 courbes et, par construction, pour les 220 faux jumeaux) ;
2. le degré : la forme norme N(u) = ∏ u(αᵢ) = Res(χ, u), qui est le degré de l'isogénie u(F) de la jacobienne (pour u = 1 − T^k : le nombre de points de la jacobienne sur 𝔽_{q^k}) ;
3. le carré : la forme trace de Rosati B(u) = Σ u(αᵢ)·u(q/αᵢ) = Tr(u·ι(u)), qui est la métrique de Weil du corpus.

- G1. Pour les 425 courbes : N(u) ≥ 0 pour tout u (toute racine réelle de χ a une multiplicité paire) et B est positive (rang 2g sauf racines confondues).
- G2. Le niveau 2 ne suffit pas en genre 2 : les 119 faux jumeaux à 4 racines hors du cercle n'ont aucune racine réelle, donc N(u) ≥ 0 pour tout u (« les degrés sont positifs ») alors que RH est fausse ; les 101 faux jumeaux à 2 racines hors du cercle (dont les 4 de genre 1) ont une racine réelle simple, donc N prend des valeurs négatives.
- G3. Pour ces 101, un u à coefficients entiers de module au plus 3 et de degré au plus 2g − 1 suffit à rendre N(u) < 0 : « une isogénie de degré négatif », impossible.
- G4. Le niveau 3 sépare tout : B est indéfinie pour les 220 faux jumeaux, avec r/2 directions négatives (proposition d'inertie de l'article 2).
