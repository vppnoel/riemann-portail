# TAC-016 — Deuxième vérification indépendante

**Verdict du 23 novembre 2026 : conforme pour le statut `mesure`, limité aux constructions précisées dans la reprise.** Le test du caractère quartique a été ajouté, la preuve du degré de κ est corrigée et la conclusion universelle sur les exposants a été retirée. Vérificateur : `ia:chatgpt-sol-6.1-max`. [Deuxième dépôt](https://github.com/vppnoel/Riemann/pull/58) · [Fil de discussion](https://github.com/vppnoel/Riemann/issues/39).

Les scripts d'origine et de reprise reproduisent les sorties. Le calcul indépendant par la récurrence a∗b=a log, puis par les sauts des poids en arithmétique entière, confirme que pour **chacun des 2 999 entiers x de 2 à 3000**, les deux produits DH testés ont au moins un exposant irrationnel. Cela reste compatible avec 303 595 exposants rationnels non nuls sur 663 208 pour Tchebychev et 226 148 sur 585 761 pour le binomial. L'argument de Baker s'applique à chacun de ces produits finis.

Pour le test de support et de positivité, il faut garder les familles fixes du tableau. Pour ζ, les exposants élémentaires sont ceux des puissances de premiers. Pour le caractère quartique du corpus, χ₅(2)=i fait échouer le test brut sur le caractère isolé. La somme des quatre puissances fournit des coefficients positifs ou nuls par orthogonalité des racines quatrièmes de l'unité. Au premier 5 la valeur 1 correspond à la puissance zéro représentée par son caractère primitif induisant de conducteur 1. Pour les quatre conjugués de DH, Tr β(2,2)=−2 et Tr β(6,2)=Tr β(6,3)=20. Les 692 indices à trace négative et les 906 indices mixtes à trace non nulle sont reproduits. Plus généralement les quatre plongements de κ sont réels, et b^σ(6)=(1+σ(κ)²)log 6 est strictement positif pour chacun. Avec des poids strictement positifs sur ces conjugués, l'indice 6 reste donc hors du support attendu.

La formulation existentielle du critère (S) ne définit pas l'ensemble des « familles naturelles ». La ligne négative du tableau se lit comme l'échec de la famille testée. Une impossibilité pour tout encodage entier, ou pour toute famille concevable, reste ouverte. Le test positif sur une famille attachée au caractère distingue effectivement le témoin DH dans l'expérience déclarée. Pour la réserve en s=1, F(s)>0 sur l'axe réel s>0 découle des différences strictement positives par blocs de cinq (détails dans le premier avis). L'étape de Landau et l'hypothèse arithmétique ultérieure restent distinctes. Les autres contrôles et limites du premier examen sont conservés ci-dessous. La décision appartient à l'auteur.

---

# TAC-016 — Vérification indépendante

**Verdict de vérification : `non_conforme`.** Les coefficients signés, le premier indice mixte et les quatre produits testés constituent des résultats reproductibles. Le témoin quartique requis manque et la conclusion sur tous les exposants est fausse telle qu'elle figure au tableau P3.

Vérificateur : `ia:chatgpt-sol-6.1-max`, 23 novembre 2026. Contrôle SHA-256 des pièces et entrées. Le rejeu `python -I -B tac016_sosie.py` reproduit la sortie déposée. La vérification porte sur la construction multiplicative chiffrée par la fiche et sur les hypothèses analytiques invoquées. [Fiche et discussion](https://github.com/vppnoel/Riemann/issues/39).

## Calcul exact et test adverse

J'ai recalculé les β par **récurrence directe** à partir de a ∗ b = a log, sans construire l'inverse de Dirichlet. Pour chaque p divisant n, β(n,p) = v_p(n)a(n) − Σ_{d|n, d>1} a(d)β(n/d,p). J'ai ensuite évalué les parties entières sous la forme x div (nk), en entiers. Jusqu'à n=3000, je retrouve 2 619 β non nuls dont 2 406 irrationnels et les 12 exposants irrationnels aux quatre x choisis. Pour (x,p)=(60,2), j'obtiens −2+6κ+9κ²−30κ³.

- b(2)=κ log 2, b(3)=−κ log 3 et b(6)=(1+κ²)log 6. Les indices 2 à 5 étant premiers ou puissances de premiers, 6 est le premier indice mixte et b(6) est strictement positif.
- Pour le poids de Tchebychev, **α₁₁(11)=1**. En effet 11 est le seul multiple contributif de 11, a(11)=1 et le poids en 1 vaut 1. C'est un contre-exemple à « aucun exposant rationnel ». Il n'implique aucune rationalité des autres exposants du même produit.
- Inversement, à x=2, le produit de DH testé vaut déjà 2^κ. Tout poids avec F(1)=1 donne ce même obstacle à x=2 pour cette définition du produit. Un seul x suffit pour exclure une *suite partout entière de cette forme*. Les mesures à quatre x ne prouvent pas que chaque produit à chaque x est irrationnel ni qu'aucun codage d'une autre nature ne peut exister.

L'irréductibilité du polynôme affiché est vraie mais l'argument « seule factorisation » du rapport saute une étape. Posons u = κ−1/κ = −1−√5. Sur K=Q(√5), κ satisfait X²−uX−1. Le discriminant u²+4 = 10+2√5 a pour norme 80, qui n'est pas un carré rationnel. Il n'est donc pas un carré dans K, d'où [Q(κ):Q]=4. La réduction des produits en base (1,κ,κ²,κ³) est alors justifiée. L'application du théorème de Baker est correcte pour un produit fini à exposants algébriques réels. Pour comparer à un rationnel positif r, on inclut aussi ses facteurs premiers dans la relation. L'indépendance rationnelle des log p résulte de l'unicité de la factorisation et la présence de 2πi dans la formulation de Baker ne pose aucune difficulté pour ces logarithmes réels. [A. Baker, rappel du théorème dans Mathematika, consulté le 23 novembre 2026](https://doi.org/10.1112/S0025579300008068).

## Témoin positif et sens de l'encodage

Pour ζ, b(pʳ)=log p et le poids entier non négatif donne bien un produit entier. Le second témoin demandé est **le caractère quartique du corpus** avec χ₅(2)=i. On a b(pʳ)=χ₅(p)ʳ log p et b(6)=0 par le produit d'Euler. Au test x=2 le poids vaut 1, donc l'exposant brut est **i**, qui ne peut être la valuation d'un entier. Le témoin passe le test du support sur les puissances de premiers, mais échoue au test de valuation brute imposé à DH. Pour tester une divisibilité avec des caractères, il faut définir et tester le même encodage pour les trois objets (par exemple préciser les entiers avant la pondération par χ). Le passage de ce témoin à l'étage 2 dans un autre sens demeure ouvert ici. [Définition de χ₅ et de DH dans le corpus, consultée le 23 novembre 2026](https://github.com/vppnoel/Riemann/blob/3a86016d25447750c94315ec90e8f0448e799760/3_Preuves_et_calculs/src/family_mod5.py).

## Étape analytique et comparaison numérique

Comme |a(n)| ≤ 1, Σ_{n≥2}|a(n)|/n² ≤ ζ(2)−1 < 1. La série de Neumann pour l'inverse de Dirichlet et Σ log(n)/n² < ∞ donnent Σ |b(n)|/n² < ∞. Pour y ≥ 1, (y/n−1)₊ ≤ (y/n)². Ceci prouve la borne uniforme O(y²) de la somme de rampes, même après ajout du centrage linéaire. Une mesure sur 10⁵ entiers seule ne pourrait l'établir. Le seuil 1,396 du script est arrondi, avec une queue estimée. Il est superflu pour cette preuve.

Pour justifier entièrement le passage à l'étape 1, il reste à identifier explicitement la transformée méromorphe du G retenu et ses pôles, y compris l'élimination du point s=1, puis les hypothèses exactes de `PoleData`. Pour la convention affichée dans le script et Re s>2, l'identité attendue est Φ(s)=[−F′(s)/F(s)]/[s(s−1)] + [F′(1)/F(1)]/(s−1). Le pôle en 1 est amovible si F(1)≠0. Pour s réel positif, le regroupement par périodes de [(5j+1)^(−s)−(5j+4)^(−s)] + κ[(5j+2)^(−s)−(5j+3)^(−s)] établit F(s)>0. Cette observation couvre le point 1 et exclut les pôles associés à des zéros réels dans ce domaine.

Le maximum annoncé de 0,354 (y=4) est reproduit **sur la grille entière 2 à 10⁵**, avec le centrage du script. La valeur 0,0227 de ζ concerne une statistique centrée par log(2π) et une autre plage. Avant une comparaison quantitative, fixer la constante additive de DH et employer les mêmes intervalles. P4 est bien une prévision manquée pour la mesure publiée. Aucune conclusion sur RH ou sur les objets automorphes ne découle de cette expérience.

**Reprise demandée.** Corriger P3 et la preuve de degré, ajouter le témoin quartique avec une définition commune du succès, puis distinguer l'obstruction élémentaire démontrée de l'affirmation générale sur l'étage 2. Le statut scientifique `mesure` convient aux résultats finis ainsi délimités.
