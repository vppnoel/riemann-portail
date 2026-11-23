# Vérification indépendante — TAC-009

*Vérificateur : ia:claude · 18 octobre 2026 · fil de discussion #9. Verdict : **non conforme**. Le rapport ne calcule rien, et sa prémisse centrale est fausse : le Gram de Nyman–Beurling contient |ζ(½+it)|², et son spectre diffère nettement de celui d'un témoin purement géométrique. Une référence est mal attribuée.*

## Pièces examinées

- La fiche (question, sortie attendue, critère de rejet, témoin), le registre et le journal des tâches.
- `RAPPORT.md`, seule pièce du dépôt : empreinte `f86dad9e…`, inchangée.
- Les entrées : la critique « tomographie de phase » (§ 3–4), le document 12 (annulation du pôle) et le document 15.
- Le fil #9, où le producteur lui-même signale que « l'absence d'un paramètre F dans le Gram standard ne suffit pas, à elle seule, à montrer l'absence de contenu arithmétique ».

## Ce qui a été calculé

Le dépôt ne contient aucun calcul. J'ai écrit un contre-contrôle, `contre_controle.py` ; ses sorties sont dans `contre_controle.json`.

- **Grille :** u = 0,5 ; 1,0 ; … ; 3,0, θ = e^{−u} ;
- **fonctions :** ρ_θ(x) = {θ/x} − θ{1/x} ;
- **différences :** C_i = ρ_{θ_{i+1}} − ρ_{θ_i} ;
- **Gram :** K, puis sa version normalisée R = D^{−1/2} K D^{−1/2}.

1. **Identité de Mellin** (classique) : ∫₀^∞ ρ_θ(x) x^{s−1} dx = −ζ(s)(θ^s − θ)/s pour 0 < Re s < 1. Par Plancherel :

   K_ij = (1/2π) ∫ |ζ(½+it)|² · m_i(t) · conj(m_j(t)) / |½+it|² dt,  avec m_i = θ_{i+1}^s − θ_{i+1} − θ_i^s + θ_i.

   Le Gram « standard » contient donc **explicitement** |ζ|² sur la droite critique. C'est le lien que le document 12 exploite (projection de Nyman–Beurling et énergie Q).
2. **Témoin géométrique W :** même construction avec |ζ|² remplacé par 1. Ce sont les fonctions de transformée −(θ^s − θ)/s, sans arithmétique.
3. **Contrôle en variable x :** intégration exacte par morceaux, ρ_a étant constante entre les points de rupture, sur [1, Y] avec Y = 2·10⁴, 4·10⁴ et 8·10⁴, et extrapolation de la queue en 1/Y. Ce calcul est indépendant de la formule de Mellin.
4. **Version pour L(s, χ₅) et DH :** |ζ|² remplacé par |F(½+it)|². C'est une définition du vérificateur, pas la généralisation publiée de de Roton (voir plus bas).

Les intégrales de Mellin sont tronquées à |t| ≤ 400, au pas de 0,02. Les valeurs propres de R pour ζ sont les mêmes, aux décimales affichées, au pas de 0,005 et au pas de 0,02.

## Résultats

Valeurs propres du Gram normalisé R (cinq différences), avec le rang effectif (exponentielle de l'entropie) :

| Gram | Valeurs propres de R | Rang effectif |
|---|---|---|
| ζ, en variable x (calcul exact par morceaux, queue extrapolée, erreur ≤ 1,3·10⁻⁵) | 0,413 ; 0,756 ; 0,924 ; 1,309 ; 1,598 | — |
| ζ, par Mellin (\|t\| ≤ 400) | 0,416 ; 0,762 ; 0,922 ; 1,306 ; 1,593 | 4,575 |
| Témoin géométrique W (\|ζ\|² → 1) | 0,525 ; 1,038 ; 1,069 ; 1,125 ; 1,243 | 4,829 |
| L(s, χ₅), même formule | 0,395 ; 0,802 ; 1,031 ; 1,195 ; 1,576 | 4,599 |
| DH, même formule | 0,455 ; 0,967 ; 1,100 ; 1,109 ; 1,370 | 4,747 |

- **Les deux calculs de ζ concordent.** Entre la variable x et Mellin, l'écart maximal sur les entrées de K est de 5,0·10⁻³, pour des entrées de taille 0,19. C'est l'erreur de troncature de Mellin, qui sous-estime légèrement la diagonale. Les valeurs propres de R concordent à 0,006 près.
- **ζ et le témoin géométrique sont nettement séparés.** La distance euclidienne entre leurs spectres vaut 0,515, et la plus petite valeur propre passe de 0,525 à 0,413, soit un écart de 0,11 : 20 fois l'écart entre les deux calculs de ζ. **Le Gram standard voit donc autre chose que la géométrie des dilatations : il voit |ζ(½+it)|².**
- **Ce qui sépare les trois fonctions,** avec la définition du vérificateur : ζ–L(χ₅) 0,163 ; ζ–DH 0,405 ; DH–W 0,166 ; L(χ₅)–W 0,436.
  - DH est plus proche du témoin géométrique que ζ et L(χ₅).
  - Ce n'est **pas** une signature eulérienne établie : les amplitudes de |F|² sur la droite et la normalisation y contribuent. Aucune incertitude de référence (tirages de témoins) n'est calculée ici.
  - Je donne ces chiffres seulement pour montrer que la question est calculable et non triviale.

## Écarts

1. **Prémisse fausse.** « K^NB ne contient aucun paramètre F, donc ne voit que la géométrie des dilatations » : le Gram contient |ζ(½+it)|² par Plancherel, et son spectre normalisé diffère de celui du témoin W bien au-delà de l'erreur de troncature. L'objet de la fiche est donc bien défini et calculable ; la conclusion « test indéfini » ne tient pas.
2. **Sortie attendue non fournie.** Rien de ce qui était demandé n'est dans le dépôt : calcul de G^NB et K^NB, spectre, rang effectif, comparaison avec un témoin géométrique.
3. **Référence mal attribuée.** « S. Darses et J. Najnudel, *JTNB*, doi:10.5802/jtnb.1227 » : ce DOI désigne F. Alouges, S. Darses et E. Hillion, *Polynomial approximations in a generalized Nyman–Beurling criterion*, JTNB 34 (2022), n° 3, 767–785. Le résumé de cet article mentionne bien une forme « block Hankel » pour une matrice de Gram. L'affirmation sur le fond est donc plausible, mais les auteurs sont faux.
4. **De Roton** (C. R. Math. 340 (2005), 191–194) : la référence existe. Son résumé parle d'une « classe plus large de séries de Dirichlet » sans la nommer ; la thèse de l'autrice vise la classe de Selberg. **DH n'est pas dans la classe de Selberg** (pas de produit d'Euler). Le rapport ne dit pas si la généralisation s'applique à DH, et c'est le point qui conditionne le test différentiel.
5. **Critère de rejet mal appliqué.** Le critère portait sur un calcul : « spectre identique au témoin géométrique, ou ζ et DH non séparés ». Le déclarer « atteint » sans calcul n'est pas recevable. Le document 12, cité par la fiche comme témoin, n'est pas discuté.
6. **Contrôles anti-circularité :** aucun n'est fait. Il fallait au moins le témoin géométrique, la remarque DH sur la classe de Selberg, et un témoin négatif.
7. **Formules altérées :** « ho » pour `\rho`, « heta » pour `\theta`, « qquad ».
8. **Procédure,** pour mémoire (sans effet sur le verdict) : rapport écrit sur `main` et dépôt enregistré par un workflow temporaire, avant l'adoption des règles ; le producteur le signale.

## Statut proposé

Ni « obstacle », dont la prémisse est fausse, ni « classique », puisque rien n'est calculé. Le statut juste est **ouvert**. Le contre-contrôle ci-dessus montre que le calcul demandé est faisable en quelques minutes, et qu'il donne une réponse non triviale.

## Pour un dépôt conforme

1. Écrire la prévision avant de calculer : grille, normalisation, témoin.
2. Calculer G^NB et K^NB en x et par Mellin, en vérifiant leur accord, puis le spectre et le rang effectif ; comparer au témoin W.
3. Pour le test différentiel, vérifier dans l'original quelle classe couvre de Roton. Si DH n'y est pas, utiliser une définition explicite, comme celle de ce contre-contrôle, et le dire.
4. Rattacher le résultat au document 12 (Nyman–Beurling et énergie Q) pour décider « classique » ou « nouveau ».
5. Corriger la référence JTNB et les formules.

*La relecture n'est pas à l'aveugle : le fil #9 nomme le producteur. La décision revient à l'auteur.*
