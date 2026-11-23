# TAC-015 — Deuxième vérification indépendante

**Verdict du 23 novembre 2026 : conforme**, dans la portée historique et asymptotique de la fiche. Le troisième exemple demandé est maintenant identifié et mesuré. La comparaison aux deux rapports positifs doit garder le caractère signé du poids de Sylvester. Vérificateur : `ia:chatgpt-sol-6.1-max`. [Deuxième dépôt](https://github.com/vppnoel/Riemann/pull/57) · [Fil de discussion](https://github.com/vppnoel/Riemann/issues/38).

Le nouveau script reproduit la sortie enregistrée. Le calcul sur une période de 30 030 donne un poids entre −1 et 4 avec 70 marches négatives, c=15 et A≈0,98859891746. Par Stirling et le théorème des nombres premiers, la limite de W(x)/x pour le schéma fixe vaut A−1+1/15≈0,05526558412. Une somme directe de Λ(n)F(x/n) pour n≤x/15, indépendante du calcul par log-factorielles, donne 0,05413629, 0,05465772 et 0,05559900 pour W(x)/x aux points 10⁴, 10⁵, 10⁶. Ainsi W(10⁶)/√(10⁶)≈55,599. Les sorties et la vérification précédente des deux autres rapports restent applicables.

J'ai confronté les poids et les constantes à l'original de 1892. Le signe négatif en 66 enlève l'intégralité **uniforme** du quotient : à x=66×67, l'exposant de 67 vaut −1, tandis que certains quotients particuliers peuvent être entiers. Les valeurs 0,95695… et 1,04423… concernent l'encadrement historique de π(x)log(x)/x pour x grand. Les mêmes constantes principales se transportent au cadre ψ/x par sommation partielle et estimation de la contribution des puissances supérieures. Les nombres imprimés dans le tableau sont arrondis et la constante 1,05921 obtenue formellement en un seul passage ne constitue pas une majoration lorsque le poids change de signe. La largeur proportionnelle à x de l'encadrement historique et la limite du gaspillage du poids fixe concernent ces constructions précises. Elles n'établissent pas de borne inférieure pour l'erreur véritable ψ(x)−x ni pour toute méthode itérative imaginable. [J. J. Sylvester, *On arithmetical series*, pp. 113–119, original consulté le 23 novembre 2026](https://rcin.org.pl/Content/108979/PDF/WA35_87684_cz294-1892-t21_Art17.pdf).

Le statut `classique` est cohérent avec ces résultats. La première vérification est reproduite ci-dessous pour conserver l'historique. La décision appartient à l'auteur.

---

# TAC-015 — Vérification indépendante

**Verdict de vérification : `non_conforme`.** La limite du gaspillage est justifiée pour la classe définie et les deux exemples déposés sont reproductibles. La fiche exige trois exemples nommés. Sylvester manque.

Vérificateur : `ia:chatgpt-sol-6.1-max`. Relecture du 23 novembre 2026 sur les pièces du dépôt enregistré, contrôlées par SHA-256 ainsi que ses entrées. La reprise de TAC-013 et la prévision recopiée après calcul sont déclarées et autorisées dans le fil. Elles ne constituent pas un motif de non-conformité. [Fiche et discussion](https://github.com/vppnoel/Riemann/issues/38).

## Rejeu et vérification indépendante

Les commandes `python -I -B tac013_niveau1.py` et `python -I -B tac013_exploration_apres_coup.py` reproduisent les deux sorties enregistrées (comparaison ligne à ligne). Le crible identifie les puissances de premiers par arithmétique entière. Les logarithmes et leurs sommes sont calculés en flottants.

| Rapport | Constante de majoration de ψ, terme principal | Limite de W(x)/x | W(10⁶)/10⁶ mesuré |
|---|---:|---:|---:|
| Binomial central, x = 2n | 1,38629 | 0,193147 | 0,1937 |
| Tchebychev, x = 30n | 1,10555 | 0,08796 | 0,0882 |

Pour le binomial, la limite rapportée à **n** vaut 2 log 2 − 1 ≈ 0,38629. Le changement de normalisation explique la valeur voisine de 0,387 du niveau 0. La première colonne numérique donne le coefficient du terme principal, avec un reste O(log² x).

J'ai réénuméré le domaine exploratoire par une méthode indépendante. Je partage les 15 coefficients libres en deux ensembles de 7 et 8, puis j'apparie les sommes vérifiant exactement Σ (210/k) a_k = 0 avec a₁ = 1. Sur 3¹⁵ configurations, 11 937 sont équilibrées. Le contrôle entier de F sur les 210 résidus ne conserve que les poids (1, −1, −1, −1, 1) aux indices (1, 2, 3, 5, 30). Cette solution a a₇ = 0. La recherche prévue imposant a₇ = −1 a donc bien zéro résultat. L'exploration après coup est correctement signalée.

## Preuve et domaine de validité

Pour les poids fixes du rapport, posons A = −Σ a_k log(k)/k. Stirling donne log N_F(x) = Ax + O(log x). Le théorème des nombres premiers donne (ψ(x) − ψ(x/c))/x → 1 − 1/c. Leur différence a donc pour limite A − 1 + 1/c.

On peut vérifier l'identité intégrale sans argument probabiliste. Si T est un entier multiple de tous les k, une intégration par parties entre 1⁻ et T donne ∫₁ᵀ F(y)dy/y² = Σ (a_k/k) H_{T/k} − F(T)/T, où H_m est le nombre harmonique. Ici F(T)=0 et Σ a_k/k=0. La limite vaut A. Retirer ∫₁ᶜ dy/y² donne la formule annoncée. Par périodicité, un translaté de [1,2) se trouve au-delà de c, avec F=1. La positivité sur cet intervalle et F ≥ 0 partout donnent une limite strictement positive. Ainsi W(x) est linéaire pour tout F fixé respectant ces hypothèses. Cela concerne le gaspillage défini par la fiche. L'argument admet le théorème des nombres premiers et ne démontre aucune nécessité universelle de la multiplicité pour toute estimation de ψ.

## Source et correction demandée

Dans l'original de Diamond et Erdős, le théorème p. 313 donne, pour tout ε > 0, un entier T(ε) permettant la borne sur la limite supérieure relative de π(x). La p. 314 indique l'emploi de résultats équivalents au théorème des nombres premiers pour l'argument général. La p. 320 donne les bornes numériques 0,924 et 1,085. Le calcul sur les diviseurs de 210 ne se substitue pas à une troisième méthode historique. [Diamond et Erdős, 1980, original consulté le 23 novembre 2026](https://www.renyi.hu/~p_erdos/1981-11.pdf).

Le texte de Sylvester de 1881 décrit expressément une itération des inégalités de Tchebychev. Il faut identifier la construction historique retenue, préciser si elle correspond vraiment à un **nouveau rapport fixe**, et fournir sa constante et les deux normalisations de son gaspillage. Si l'identification exigée par la fiche est inadéquate, le producteur peut documenter la distinction et demander à l'auteur d'amender ce point. La conclusion classique sur les deux rapports déjà traités peut être conservée. [Sylvester, 1881, original réédité, consulté le 23 novembre 2026](https://rcin.org.pl/Content/162549/PDF/WA35_189923_11371-3_art-61.pdf).
