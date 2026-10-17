# V6.40 : relecture critique du protocole à contraintes exactes

Date : 12 octobre 2026. Relecture interne indépendante. Cette première partie a été rédigée avant de consulter tout nouveau comptage V6.40. Elle ne constitue pas une évaluation externe par les pairs.

## 1. Ce qui est effectivement figé

Le manifeste `data/v639_couples_fixes.json` contient 12 couples : les ancres représentatives k=1,3,5, croisées avec les quatre rayons 9/20, 13/20, 3/4 et pi/6. Le membre `c_plus` a le défaut D le plus faible ; `c_minus` a le défaut le plus fort. Les contrastes certifiés sont tous supérieurs au seuil 1/40. Les supports et le signe de la direction ont été déterminés sans consulter les zéros.

Son empreinte canonique, après exclusion du champ supérieur `sha256`, est :

`1218d67a838989857e0b174f991181019f155c79f7b6c9ef02ab974288d4b9ec`.

La faisabilité analytique des 12 couples est déjà établie. La comparabilité des observations numériques sera une question différente. Ces deux notions ne doivent pas être fusionnées sous le terme « faisable » après les résultats.

La prévision héritée est : D fort donne une première détection numérique plus précoce dans une majorité des strates faisables. Il faut préciser son dénominateur avant calcul. La règle critique proposée est une majorité stricte sur les 12 strates analytiquement faisables, soit au moins sept signes « D fort plus tôt ». Un bilan secondaire peut compter les signes strictement comparables, en gardant affichés les égalités, les doubles censures et les ambiguïtés. Ce bilan secondaire ne remplace pas la règle principale.

## 2. Dépendances et portée de l'expérience

Les quatre rayons d'une même ancre utilisent la même direction de noyau : ils explorent une courbe déterministe, pas quatre tirages indépendants. Les ancres k=3 et k=5 emploient en outre la même direction de noyau supportée par k=1,7,11. Le recoupement des signes entre rayons est utile pour décrire une forme, mais il ne fournit pas douze réplications indépendantes.

Les ancres conjuguées n'ajoutent pas de répétitions indépendantes pour un observable en |Im(s)|. Le choix des trois représentants respecte cette limite. Les six contrôles d'Euler peuvent servir au diagnostic d'implémentation, sans les comptabiliser comme six validations indépendantes.

Le contrôle exact de A complexe, de l'ancre et du rayon ne fixe pas tous les autres coefficients de Dirichlet. Changer de membre du couple modifie la fonction entière. Une concordance de signes établirait un résultat descriptif sur cette construction ; elle ne démontrerait pas que D exerce un effet causal autonome ni qu'il prédit toutes les directions de la sphère contrainte.

## 3. Observable et censure

L'observable calculé par `DirectGrid` est la première hauteur entière T pour laquelle le comptage numérique par contour dépasse le nombre de changements de signe de Hardy sur la droite critique. Il convient de l'appeler « première tranche de déficit numérique » ou « première détection par cet instrument ».

Un résultat T place cette détection dans la tranche (T-1,T]. Il ne certifie pas l'ordonnée du premier véritable zéro hors droite. Deux T identiques constituent une égalité de tranches, pas une égalité d'ordonnées.

Une absence de détection jusqu'à 150 est une censure à droite pour cet instrument. Elle n'est ni la valeur 151 ni un certificat d'absence de zéro hors droite. Une détection admissible opposée à une censure permet d'ordonner les deux observations de l'instrument ; deux censures ne permettent pas de les ordonner. Une direction numériquement non résolue rend son couple indéterminé, même si une grille brute affiche un premier déficit.

Le même tableau de catégories doit être conservé aux plafonds 50, 100 et 150. Les plafonds intermédiaires sont descriptifs : la prévision principale porte sur 150.

## 4. Critères numériques proposés avant comptage

Reprendre les deux grilles de contour historiques, avec pas verticaux 0,02 et 0,01, pas horizontaux maximaux 0,05 et 0,025, puis raffinement adaptatif. Reprendre toute la droite critique à 0,005. Le bord droit doit satisfaire la domination du premier terme avant consultation des zéros.

Une direction admissible doit avoir les mêmes comptages totaux sur les deux grilles, les mêmes comptages critiques aux trois pas, un déficit non négatif et pair, des comptages total, critique et de déficit non décroissants avec T, aucune ligne horizontale non résolue, un résidu d'enroulement inférieur à 1e-8, un incrément vertical maximal inférieur à 0,8 radian, et une marge relative de bord échantillonnée au moins égale à 1e-10. Les contrôles d'Euler doivent également être publiés. Une valeur brute rejetée reste dans les données ; elle n'entre pas dans les signes admissibles.

Ces critères doivent être appliqués à toutes les directions selon la même règle. Si des diagnostics ne sont disponibles que globalement pour un lot, la règle globale choisie doit être conservée et documentée ; une panne ne doit pas être attribuée après coup seulement aux couples qui contredisent la prévision.

La stabilité entre grilles est un contrôle de reproductibilité numérique. Elle ne garantit pas que la courbe de phase continue entre les nœuds n'effectue pas un tour supplémentaire. La proximité de l'enroulement avec un entier ne résout pas à elle seule ce problème.

## 5. Les changements de signe ne comptent pas toute multiplicité

La soustraction contour moins changements de signe présente une limite structurelle. Un zéro critique de multiplicité paire ne change pas le signe. Deux zéros critiques simples très rapprochés peuvent également se situer entre les mêmes nœuds et être omis. Ces situations peuvent produire un déficit positif sans zéro hors droite dans la tranche considérée.

Il faut donc localiser indépendamment des racines hors droite lorsqu'un déficit est annoncé. Une racine recoupée en haute précision, avec un résidu faible et un déplacement réel distinct de 1/2, confirme l'existence d'une racine représentative. Elle ne certifie ni l'absence de racines plus basses ni l'exhaustivité du comptage. Le recoupement ne doit pas transformer rétroactivement la première tranche numérique en « premier zéro mathématique ».

## 6. Entrées exactes et calcul en binary64

Les égalités de contraintes concernent les recettes exactes définies par les sommes de Gauss et les mineurs. Les vecteurs décimaux exportés dans le manifeste sont des approximations binary64. Le calcul de la base emploie aussi des phases numériques. Les résidus flottants de norme, de noyau ou de A doivent être mesurés, sans être présentés comme la preuve des identités exactes.

Pour contrôler l'entrée, reconstruire les coefficients et les phases à haute précision à partir de la recette, comparer chaque coordonnée à son export binaire et enregistrer la différence maximale. Pour une base B_j(s), la seule erreur de coefficient vérifie

\[
|F_{c+\delta c}(s)-F_c(s)|\leq\sum_j|\delta c_j|\,|B_j(s)|.
\]

Cette borne ne comprend pas l'erreur d'évaluation des B_j eux-mêmes. Sur un contour échantillonné, comparer le membre de droite à la marge |F_c(s)| échantillonnée peut vérifier que l'arrondi des coefficients est négligeable aux nœuds. Cela ne produit pas une borne pour tout le contour continu.

Les racines recoupées devraient être recalculées pour la recette exacte à haute précision, puis comparées à celles obtenues avec les coefficients binary64. Une différence très petite teste la stabilité de ces racines particulières ; elle ne certifie pas la stabilité de tous les comptages entre les nœuds.

## 7. Conclusions autorisées et prochaines obligations

Quel que soit le signe obtenu, conserver les 12 couples, les données brutes, les critères d'admissibilité, les censures et les échecs éventuels. Ne pas optimiser une nouvelle direction puis la présenter comme appartenant au plan initial. Une nouvelle sélection appartient à une expérience ultérieure.

Un bilan positif autoriserait à explorer un mécanisme analytique et d'autres directions préenregistrées. Un bilan négatif interdirait d'utiliser D seul comme règle universelle sur ces strates, et rendrait utile une étude des autres coefficients ou de la géométrie locale des zéros. Aucun de ces deux bilans ne décide RH, GRH ou une positivité globale.

La poursuite la plus probante serait une certification du comptage et du premier événement sur un petit nombre de strates défini sans consulter le nouveau résultat, avec contrôle de toute la frontière et des multiplicités critiques. L'élargissement du nombre de courbes vient ensuite : davantage de grilles flottantes ne supprime pas la limite du détecteur.

## 8. Audit du verrou avant comptage

Le verrou `data/v640_protocole_verrouille.json`, daté du 12 octobre 2026 à 13:17:04 UTC, et la prévision `data/prevision_v640_comparaison.md` ont été contrôlés avant consultation de nouveaux comptes. Les empreintes du fichier de sélection, de son contenu canonique et de la prévision correspondent aux valeurs enregistrées. La règle principale est bien 7/12 ; les catégories indéterminées sont conservées. La règle d'entrée, les recoupements à 80 et 110 chiffres et leurs seuils sont fixés.

Le choix R=3 satisfait la domination du premier terme : la marge minimale cos(3/4)-sqrt(6)(zeta(3)-1) est approximativement 0,2367525571258607542. Une reconstruction indépendante à 160 chiffres, directement par les sommes de Gauss et les mineurs prescrits, donne les repères numériques suivants, sans évaluer de fonction L :

| Quantité sur les 12 couples | Maximum observé |
|---|---:|
| Erreur absolue d'une coordonnée binary64 contre la recette exacte | 5,0175421109034513264e-17 |
| Différence de A entre les deux membres binary64, avec phases reconstruites | 6,2209237570068526510e-17 |
| Écart de la norme au carré à un | 1,0210409793155171550e-16 |
| Écart du rayon projectif normalisé à son rayon prescrit, en radians | 4,3509375397203191268e-17 |

Ces nombres confirment une implémentation des entrées à la précision attendue de binary64. Ils sont des recoupements numériques, pas des bornes d'intervalles. Aucun blocage du protocole n'est identifié à ce stade.

## 9. Audit des résultats

Les résultats ont été consultés après le signal du responsable du calcul. Les sections 1 à 8 précèdent cette consultation.

### 9.1. Recoupement indépendant des comptes sauvegardés

Les matrices NPZ, le tableau de directions JSON et le bilan JSON ont été contrôlés indépendamment de la fonction d'analyse du programme. Les coefficients sauvegardés sont exactement les 24 vecteurs du manifeste binary64, suivis des six axes d'Euler. Les matrices ont toutes les dimensions attendues, 30 directions par 150 niveaux entiers.

Les identités suivantes sont vérifiées sur tous les niveaux sauvegardés : comptes totaux grossiers égaux aux comptes fins ; comptes critiques aux pas 0,02, 0,01 et 0,005 égaux ; déficit égal au total moins critique ; comptes non négatifs et non décroissants ; déficit pair. Les comptes des recettes reconstruites puis arrondies sont identiques. Les premières tranches ont été recalculées directement à partir du déficit sauvegardé, sans utiliser le résumé fourni.

| Ancre | Rayon | Première tranche D faible | Première tranche D fort | Ordre de D fort |
|---|---|---:|---:|---|
| 1 | 9/20 | 5 | 12 | Plus tard |
| 1 | 13/20 | 5 | 12 | Plus tard |
| 1 | 3/4 | 5 | 8 | Plus tard |
| 1 | pi/6 | 5 | 12 | Plus tard |
| 3 | 9/20 | 15 | 9 | Plus tôt |
| 3 | 13/20 | 15 | 9 | Plus tôt |
| 3 | 3/4 | 15 | 9 | Plus tôt |
| 3 | pi/6 | 15 | 9 | Plus tôt |
| 5 | 9/20 | 20 | 10 | Plus tôt |
| 5 | 13/20 | 16 | 11 | Plus tôt |
| 5 | 3/4 | 16 | 11 | Plus tôt |
| 5 | pi/6 | 16 | 11 | Plus tôt |

Le bilan brut est donc huit signes plus précoces et quatre plus tardifs, sans égalité ni censure des 24 directions nouvelles. Les six contrôles d'Euler restent sans détection jusqu'à 150. Les 30 directions passent les critères des grilles.

La marge horizontale relative minimale échantillonnée vaut environ 2,4609446713432014e-4 ; la marge verticale minimale vaut 0,2943059987674568. Les incréments verticaux maximaux sont environ 0,06307 et 0,03154 ; les incréments horizontaux maximaux sont 0,79956 et 0,79766. Le résidu maximal d'enroulement est inférieur à 2,64e-11, sans ligne horizontale non résolue. Toutes ces quantités passent les seuils annoncés.

L'examen du programme d'exécution et de l'analyse n'identifie aucun défaut bloquant pour ce bilan numérique. Les résultats avant recoupement des racines sont conservés dans un champ séparé ; l'analyse principale attend la validation de chaque racine. Cette séparation respecte la prévision.

### 9.2. Recoupements de racines

Le fichier final `data/v640_racines_recoupees.json` conserve les 24 travaux et les 24 réussites. Son empreinte correspond à celle du bilan final ; les identifiants et les premières tranches concordent avec le tableau de directions. Les seuils ont été vérifiés à partir des valeurs enregistrées, et pas seulement à partir des indicateurs booléens.

Chaque position satisfait Re(s)>0,500001, Re(s)<3 et T-1<|Im(s)|<=T. Les positions partenaires vérifient les identités beta_partenaire=1-beta et gamma_partenaire=gamma aux arrondis d'affichage près. Les résidus, accords entre précisions, écarts à la localisation EM et déplacements dus à l'entrée binaire passent les limites du verrou.

| Contrôle des 24 racines | Maximum enregistré ou recalculé |
|---|---:|
| Résidu primaire à 80 chiffres | 2,106891490209351e-84 |
| Résidu primaire à 110 chiffres | 1,150646073347766e-114 |
| Résidu du partenaire, ramené à l'échelle primaire, à 80 chiffres | 3,591916316760971e-80 |
| Même contrôle à 110 chiffres | 3,138089961611111e-110 |
| Écart entre positions décimales archivées à 80/110 chiffres | 4,774409703248417e-79 |
| Écart à la localisation Euler–Maclaurin | 1,132362249921444e-13 |
| Déplacement lié aux coefficients binary64 | 7,604642443007224e-17 |

Les positions exactes du plan ont également été réévaluées par un code de relecture indépendant du module `v640_racines`, à 90 chiffres, en reconstruisant les sommes de Gauss, les mineurs et la somme finie de zêtas de Hurwitz. Aucun nouveau zéro n'a été recherché pour ce contrôle. Le résidu primaire maximal recalculé est 3,25247414671566481e-90 ; celui des partenaires à la même échelle est 2,71537648401961985e-90. Ce recoupement emploie lui aussi mpmath : il vérifie un autre chemin de calcul et la reconstruction, sans revendiquer un backend indépendant ni des bornes certifiées.

L'analyse finale conserve huit signes plus précoces, quatre plus tardifs, aucune égalité et aucun ordre indéterminé aux plafonds 50, 100 et 150. Le résultat identique aux trois plafonds vient du fait que toutes les détections nouvelles sont au plus à 20 ; il n'ajoute pas trois expériences. Les contrôles d'Euler restent censurés sans détection sous 150.

Les 24 recoupements confirment numériquement des racines représentatives dans les tranches annoncées. Ils ne prouvent ni l'exhaustivité des zéros ni l'absence de zéro plus bas. Le statut de « première tranche de déficit numérique » est conservé.

### 9.3. Interprétation du signe

Le résultat brut se regroupe par ancre : une courbe (k=1) est contraire sur ses quatre rayons ; les deux autres (k=3 et k=5) sont favorables sur leurs quatre rayons. Le nombre 8/12 respecte le dénominateur du plan figé, mais la cohérence entre rayons n'en fait pas huit confirmations indépendantes. Il faut publier les quatre signes contraires aussi clairement que les huit favorables.

Les 24 recoupements passent les seuils fixés : le critère majoritaire 7/12 est donc observé pour cet instrument et ce plan. Ce résultat ne permet pas de convertir D en règle universelle de classement de la première ordonnée mathématique ; celle-ci n'est pas certifiée par le protocole. Le mécanisme dépendant de l'ancre et la certification d'un premier événement restent des tâches distinctes.

## 10. Audit des deux lemmes de poursuite

Le premier lemme de `preuves/LEMMES_ET_SUITE_V640.md` est correct. La borne de coefficients sqrt(6) découle de Cauchy–Schwarz ; la majoration de la queue par zeta(3)-1 vaut sur tout le demi-plan Re(s)>=3. La comparaison stricte de la série avec l'intégrale fournit zeta(3)-1<1/4. Avec sqrt(6)<5/2 et cos(3/4)>=23/32, la séparation 5/8<23/32 démontre la domination sans dépendre d'une approximation numérique. Les facteurs de complétion sont holomorphes et non nuls sur ce demi-plan.

Le second lemme est également correct, sous son hypothèse explicite de racine simple. Les caractères non principaux donnent des fonctions L entières ; la dépendance en r par sin/cos est holomorphe. Le théorème des fonctions implicites produit une branche locale unique. La dérivation donne s'=-partial_r F/partial_s F ; sur une racine, eta G=-cot(r)B_i, donc partial_r F=-B_i/sin(r) et s'=B_i/(sin(r)partial_s F). Ce quotient ne fixe aucun signe pour Im(s'). Une collision ou annulation de partial_s F sort des hypothèses ; elle doit arrêter l'application de cette formule.

Les unités fictives sont cohérentes après le choix de coordonnées normalisées sans dimension, de c^phys=Cc et F^phys=CF, avec B_j d'unité1. Le défaut de multiplicativité physique a l'unité C^2, son carré C^4, compensée par ||c^phys||^4. Les facteurs C se compensent dans la dérivée de la position. Le paramètre r n'est pas un temps physique. Ce contrôle d'unités n'ajoute aucune interprétation énergétique aux théorèmes.

Avis final de relecture : les calculs et les deux lemmes peuvent être intégrés avec les limites publiées. La poursuite par suivi de branches simples est justifiée comme nouvelle expérience ; une certification du premier événement demeure nécessaire pour changer le statut des premières hauteurs.
