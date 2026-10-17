# Diagnostic constructif : conserver les interférences

## Matériel réutilisé

Les matrices arithmétiques `v644_family_resultats.json` sont celles déjà produites dans le corpus, aux supports S=1/2,1,2,3 et aux précisions de travail 40 et 70 chiffres. Les huit tests sont

\[
f_k(x)=(\partial_x^2-1/4)\{(x/S)^k[1-(x/S)^2]^4\},\qquad k=0,\dots,7,
\]

sur [-S,S], avec prolongement nul. Leurs jets de bord rendent les deux moments polaires nuls et les placent dans le domaine H1 requis par les calculs. Aucune liste de zéros n'est lue et aucun nouveau coefficient premier n'est calculé dans cette réanalyse.

Deux métriques externes sont examinées : B=masse+norme L2 de la dérivée, déjà stockée ; et R=masse+énergie archimédienne, reconstruite comme `arch+(C0+1)*mass`, avec la masse polynomiale rationnelle exacte du module existant. La reconstruction de R utilise encore les quadratures archimédiennes exploratoires de V644. Elle n'est donc pas un nouvel encadrement certifié.

Avec M=LL^T, les fonctions phi_j de coordonnées L^(-T) sont orthonormales pour M et la forme devient Q=L^(-1)GL^(-T). Ceci conserve la forme, les domaines finis et l'inertie. Il n'ajoute aucun signe.

## Ce qui est perdu par les seules énergies individuelles

Fixons des amplitudes de coefficients a_i>=0 et choisissons des phases réelles epsilon_i dans {-1,1}. Les tests c_i=epsilon_i a_i ont exactement la même norme métrique et la même observation diagonale D=sum Q_ii a_i². Pourtant

\[
q(c)=D+2\sum_{i<j}Q_{ij}a_i a_j\epsilon_i\epsilon_j.
\]

Pour des signes indépendants équiprobables,

\[
\mathbb E q(c)=D,
\qquad
\operatorname{Var}q(c)=4\sum_{i<j}Q_{ij}^2a_i^2a_j^2.
\]

Preuve : les caractères epsilon_i epsilon_j ont une espérance nulle et sont orthogonaux deux à deux ; développer le carré. Fixer epsilon_1=1 retire seulement la duplication par signe global et conserve toutes les valeurs de q. L'énumération exhaustive des 128 signes vérifie ces identités dans chaque calcul à précision élevée. Ces identités sont algébriques classiques ; elles ne constituent pas une nouvelle loi arithmétique.

L'observation diagonale correspond donc à une moyenne sur des phases effacées. Une moyenne positive ne contrôle pas chaque phase. Dans une base réelle de Weil, les Q_ij sont réels par structure ; les signes réels suffisent déjà à rendre cette perte visible. Nous n'attribuons pas à cette forme des parties imaginaires arbitraires absentes de sa définition.

Les amplitudes ont été choisies après inspection comme les valeurs absolues du vecteur propre de plus petite valeur propre. Cette sélection cherche une direction sensible ; elle n'est pas un échantillonnage statistique représentatif. Tous les changements de signes sont ensuite énumérés exactement quant à leur combinatoire. Les valeurs des formes restent numériques.

## Résultats dans la métrique R

| S | q minimum parmi les phases testées | q maximum parmi les phases testées | Rapport | Condition spectrale de la matrice complète |
|---|---:|---:|---:|---:|
| 1/2 | 0,00372112678 | 0,04945040561 | 13,2891 | 63,0069 |
| 1 | 2,18017014e-8 | 0,00134366281 | 61 631,1 | 1,14904e7 |
| 2 | 2,26562328e-11 | 0,000217698400 | 9,60876e6 | 6,20239e8 |
| 3 | 5,35414911e-13 | 0,00004974607481 | 9,29113e7 | 6,22804e9 |

Pour chacune des deux phases comparées, la norme R du test est 1 et tous les modules des coefficients dans la même base R-orthonormale sont identiques. Ce ne sont pas des égalités du module ponctuel |f(x)|. Toutes les valeurs calculées sont positives ; il n'y a aucun témoin négatif de Weil ni contre-exemple à RH.

Les rapports H1 correspondants sont 11,2833 ; 65 891,7 ; 9,48955e6 ; 9,33322e7. La sensibilité observée persiste donc dans la métrique R utilisée par les certificats du corpus ; elle ne provient pas exclusivement du choix H1. Les matrices complètes sont mal conditionnées aux plus grands supports dans cette famille finie. Le changement de métrique, seul, ne résout pas cette difficulté.

## Réduction fidèle par Schur

Une partition Q=[[H,B],[B^T,C]] avec C strictement positive possède le minorant exact sur les fibres de tête

\[
\min_y q(x,y)=x^T(H-BC^{-1}B^T)x,
\quad y_*=-C^{-1}B^Tx.
\]

La matrice de dette D=BC^(-1)B^T est positive. Si H est strictement positive, le rayon relatif

\[
r=\lambda_{\max}(H^{-1/2}DH^{-1/2})
\]

vaut au plus 1 exactement lorsque H-D est positive ou nulle. Il mesure la fraction de tête absorbée par cette dette pour la partition choisie. Son invariance concerne un changement de coordonnées dans une même décomposition, pas un changement arbitraire de complément mélangeant les sous-espaces.

Pour la partition des quatre premières coordonnées et des quatre dernières dans la base R-orthonormale, les r sont : 0,276211917 ; 0,999826597 ; 0,999998744 ; 0,999999832. Les résidus des identités de complétion sont archivés. Une sous-matrice positive isolée ne représente donc pas ce que le complément fait réellement à sa marge.

La comparaison `minimum(diag Q)-norm(Q-diag Q)` donne une borne négative aux quatre supports. Elle échoue à conserver le signe observé de la matrice complète. Cela réfute l'efficacité de ce minorant dans ces cas, pas la positivité de la forme.

## Portée exacte et usage

Le complément dans ce calcul a quatre dimensions. Il n'est pas la queue fonctionnelle infinie. Le résultat n'établit aucun contrat de queue et ne peut être employé comme certificat de tout X_S.

Le document 73 avait déjà certifié tous les tests dans X_S pour S<=1/2, au moyen d'une erreur en norme opérateur ; ce fait doit rester présenté comme un acquis. Le diagnostic actuel ajoute une mesure explicite des interférences effacées dans les résumés et une comparaison entre deux métriques. Il ne remplace pas le certificat antérieur et n'accroît pas sa portée.

L'écart entre les deux précisions stockées, de l'ordre de 1e-35 pour les minima les plus sensibles, montre une stabilité interne. Il ne borne pas l'erreur commune des quadratures de V644. Une seconde voie NumPy/Cholesky, conduite par la lecture critique, retrouve les diagnostics H1 avec des écarts relatifs compatibles avec le conditionnement. Aucun de ces recoupements ne devient un encadrement rigoureux de la forme.

Action utile : conserver les matrices complètes dans les observations et utiliser la dette relative pour identifier les partitions qui perdent le contrôle. Puis rechercher une loi arithmétique ou un minorant opératoire qui contrôle cette dette à tous les supports. Ajouter seulement des diagonales ou augmenter la précision d'un résumé qui a déjà effacé les interférences ne récupère pas cette information.

## Reproduction

Python et mpmath 1.3.0 :

    python v657_signal_couplings.py --corpus /chemin/programme-riemann \
        --output v657_signal_couplings_resultats.json

Le programme ne modifie aucune pièce source. Le SHA-256 de la matrice V644 et les normalisations se trouvent dans le JSON. Les preuves de Schur et de couverture du corpus gardent leurs hypothèses ; aucune nouveauté bibliographique n'est revendiquée.
