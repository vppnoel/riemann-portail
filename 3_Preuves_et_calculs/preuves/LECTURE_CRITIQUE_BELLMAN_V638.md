# V6.38 — Lecture critique : reprendre le corpus avec Bellman

Date : 12 octobre 2026. Statut : relecture interne indépendante des décisions et de leur représentation. Cette note ne constitue pas une expertise externe des Théorèmes A et B, une nouvelle vérification de chaque calcul historique, ni une preuve de RH.

## 1. Verdict

Bellman apporte un cadre utile pour rendre les décisions explicites, comparer des suites d'actions et tenir compte des prérequis. Le corpus permet une reconstruction documentaire de ce parcours. Il ne fournit pas un modèle probabiliste calibré de la recherche, ni les résultats des actions qui n'ont pas été exécutées.

Le premier usage défendable est donc une **planification déterministe à budget fini de livrables vérifiables**. Son optimum est exact relativement au modèle déclaré ; son interprétation scientifique reste conventionnelle. Le fait qu'un portefeuille soit optimal dans ce modèle ne démontre ni qu'il maximise la probabilité de résoudre RH, ni qu'il sera réalisable au coût prévu.

Le corpus contient des preuves internes, des identités, des expériences et des métaphores. Une action marquée « faite » signifie que le travail a été réalisé : elle ne signifie pas que sa thèse est prouvée. Un échec de prévision peut laisser un acquis méthodologique important.

## 2. Ce qui a été relu

La critique s'appuie sur la carte des 63 coups du navigateur V6.37, son code de classement, les pages actives du portail, la reconstruction historique du document 06, le classement des instruments (22–24), les bilans récents 45, 47–60, le protocole V13 et sa relecture interne, ainsi que les énoncés de l'article 1. Le registre construit par la lecture parallèle fournit la couverture documentaire de l'ensemble des documents numérotés 01–61 et a été recoupé après son achèvement.

Cette lecture recoupe les catégories et les transitions ; elle ne prétend pas refaire toutes les preuves ni tous les programmes de l'archive. Les chiffres historiques restent ceux des expériences auxquelles ils se rapportent. Le contrôle du modèle de Bellman est rapporté séparément ci-dessous, après inspection de son code et de ses sorties.

## 3. Six confusions à éviter

### 3.1 Prévision et interprétation rétrospective

Il faut conserver trois textes distincts : la proposition avant calcul, le résultat obtenu et l'interprétation après calcul. Un texte qui explique un résultat une fois connu ne devient pas une prévision par son insertion dans un graphe de décisions.

Exemples importants du corpus :

| Épisode | Fait documentaire | Conséquence pour l'atlas |
|---|---|---|
| Innovations de Levinson, document 36, corrigé en V6.14 | Quatre seuils attribués à des quadruplets étaient du bruit numérique ; la détection principale DH demeure | Conserver la correction instrumentale ; ne pas présenter les anciens seuils comme succès prévus |
| Recensement DH, V6.15 | La prévision « exactement 30 » donne 50 dans la fenêtre, qui reçoit aussi des contributions plus hautes | La réfutation a précisé l'instrument ; elle n'autorise pas un décompte universel par quadruplets |
| Riemann–Roch virtuel, document 47 | Une cinquième prévision est formulée après un premier calcul, avant un second | L'antériorité s'apprécie par rapport au calcul concerné ; elle n'est pas globale à l'épisode |
| Relief T*, documents 56 et 58 | Le critère corrigé est choisi après observation du bruit ; T* ne coïncide pas toujours avec la première détection directe | Statut exploratoire, puis contrôle distinct ; ne pas réécrire le critère initial |
| Premier coefficient, document 57 | Les trois prévisions sont fausses ; l'association avec a(1) est proposée après coup | Hypothèse exploratoire ensuite retestée sur V11 et V13 |
| V13, document 61 | 72 couples fixés avant comptage ; diagnostic signé des calipers après résultat | Comparaisons prévues et diagnostics ultérieurs doivent rester étiquetés séparément |

Le reçu V637 et son SHA256 permettent de contrôler l'identité du protocole conservé. Cette traçabilité interne ne doit pas être décrite comme un horodatage indépendant délivré par un tiers.

### 3.2 Actions observées et alternatives non observées

Les coups ouverts du navigateur attestent des possibilités envisagées. Ils ne renseignent pas leur résultat contrefactuel. On peut enregistrer qu'une expérience A fut préférée à une expérience B documentée ; on ne peut en déduire que B aurait été moins utile.

Une analyse rétrospective fondée seulement sur les succès publiés serait biaisée. Les coups réfutés, les cas ambigus, les censures, les routes à construire et les lectures restées partielles doivent rester visibles. Ne pas inventer d'autres options « qu'on aurait dû choisir » sans les distinguer des alternatives effectivement écrites.

### 3.3 Récompense conventionnelle et progrès vers RH

Les niveaux de l'indicateur sont des classes de maturité, pas des distances métriques. Un passage de 4 à 5 n'est pas nécessairement le même gain qu'un passage de 5 à 6. Additionner des incréments reste un choix éditorial, non une mesure naturelle du progrès mathématique.

Le nombre de maillons nommés comme manquants ne borne ni le nombre de lemmes nécessaires, ni le coût d'une démonstration. « Il reste une catégorie ouverte : la positivité globale » ne signifie pas « il reste une étape avant RH ».

Les tokens du modèle V638 doivent désigner des livrables contrôlables : provenance, contre-épreuve, contrôle d'erreur, formulation d'un énoncé ou préparation d'une relecture. Ils ne peuvent promettre « un résultat positif », « un lemme réussi », « une bonne signature » ou « un rapprochement de RH ». Un bilan négatif explicite peut remplir un token de discrimination exactement comme un bilan favorable.

### 3.4 État suffisant et propriété de Markov

Pour la recherche réelle, les sept niveaux de l'indicateur et la liste des documents ne forment pas un état suffisant. Le prochain travail dépend des hypothèses, des marges, des conditions d'application, de la confiance dans les compteurs, des covariables, des sources vérifiées et des résultats particuliers.

En revanche, dans un problème documentaire fini où les coûts, les prérequis et la valeur des tokens sont fixes, l'ensemble des actions achevées et le budget restant forment un état suffisant **par construction**. C'est une hypothèse limitée et vérifiable de ce modèle, pas la découverte que la recherche sur RH est un processus markovien.

### 3.5 Probabilités subjectives et fréquences

Les champs `probabilite` historiques sont des estimations déclarées du navigateur. Ils ne doivent pas devenir des probabilités de transition de Bellman sans calibration et sans définition de l'événement.

Les 36 signes A1 favorables sur 36 couples V13 ne donnent pas une probabilité de succès de 1 pour le prochain test : les couples sont ciblés, sélectionnés avec des contrastes importants, et non tirés au hasard d'une population représentative. Les trois plafonds 50, 100 et 150 sont des lectures emboîtées des mêmes données. La conjugaison fournit un contrôle de symétrie, pas une réplication indépendante.

Sans probabilités défendables, ne pas inventer une espérance. On peut comparer des scénarios, publier des ensembles de solutions optimales, ou employer un minimax avec un ensemble d'issues **explicitement déclaré**. Un minimax arbitrairement restreint ne devient pas, lui non plus, une garantie empirique.

### 3.6 Unités fictives et énergie

Attribuer l'unité d'utilité scientifique conventionnelle \(\mathsf U\) à une valeur, et l'unité de travail conventionnelle \(\mathsf H\) à un budget, rend les calculs homogènes :

\[
[U]=[V]=[r]=\mathsf U,\qquad [b]=[c]=\mathsf H.
\]

Si une pénalité de coût est ajoutée, son coefficient porte \(\mathsf U/\mathsf H\). Si l'on utilise un ratio de classement, son unité est \(\mathsf U/\mathsf H\). Les pondérations de critères peuvent rester sans unité lorsque les tokens ont déjà l'unité \(\mathsf U\).

\(\mathsf H\) ne désigne pas une heure mesurée. \(\mathsf U\) ne désigne pas une énergie physique. Le document 50 montre déjà qu'un bilan mécaniquement cohérent peut être une identité d'Abel vraie pour toute suite, sans imposer de contrainte supplémentaire sur les zéros. Bellman doit respecter la même garde : l'homogénéité n'ajoute aucune positivité arithmétique.

## 4. Statuts exacts des résultats récents

| Résultat | Statut retenu | Ce qui n'est pas établi |
|---|---|---|
| Article 1 : Théorème A | Preuve interne d'une caractérisation de l'exposant asymptotique ; méthode standard ; relecture spécialisée encore ouverte | RH n'est pas démontrée par le critère |
| Article 1 : Théorème B et B′ | Preuves internes sous RH, multiplicité explicitement comptée | RH et simplicité ne sont pas acquises pour les appliquer inconditionnellement |
| Jets de Hasse et zêta elliptique, V635/article 3 | Démonstration expositive de la méthode classique ; espaces formels et certificats exacts | Ni nouveauté historique revendiquée, ni transfert à la zêta des entiers |
| DH V636, a=0,02, h=0,005, L=1115 | Sous le modèle d'arithmétique décrit : un sous-espace négatif de dimension 25 est certifié | Le compte exact 25, le complément positif, les 180 autres réglages et la positivité globale de ζ |
| V13 A1, V637 | 36/36 premières détections plus tardives du côté a1 haut dans le dessin ciblé | Loi monotone générale, causalité, premier zéro certifié, petites perturbations |
| V13 D, V637 | 25 détections plus précoces, 8 plus tardives et 3 égalités de tranche ; tendance et hétérogénéité | Absence d'effet, effet indépendant prouvé ou mécanisme propre à D |
| Racines V13 recoupées | 24 racines représentatives retrouvées à haute précision, hors droite | Certificat d'existence par intervalles, complétude des détections ou absence de racine antérieure |

Ne pas fusionner le statut numérique V637 et le statut computationnel validé V636. Ne pas remplacer « aucune détection jusqu'à 150 » par « premier zéro supérieur à 150 ». Les cinq non-détections du bras A1 restent conservées sans hauteur imputée.

## 5. Un modèle fini exact possible

Soit \(A\) un ensemble fini d'actions documentaires, \(D\subseteq A\) celles qui ont été achevées, \(P_a\) les prérequis de l'action \(a\), \(c_a\) son coût entier strictement positif et \(B\) le budget initial. L'action n'est admissible que si \(a\notin D\), \(P_a\subseteq D\) et \(c_a\le b\). Les prérequis déjà acquis avant V638 peuvent être retirés du graphe, à condition de les nommer explicitement.

Une action peut produire un ensemble de tokens documentaires \(T_a\). La valeur terminale tient compte de leur **union** :

\[
U_w(D)=\sum_{t\in T_0\cup\bigcup_{a\in D}T_a} w_{j(t)}u_t,
\]

où \(T_0\) est l'ensemble des acquis initiaux, \(j(t)\) le critère du token, \(u_t\) sa valeur conventionnelle et \(w_j\) un poids déclaré. Un token partagé par deux actions ne compte qu'une fois. Un changement de format sans acquis documentaire nouveau ne doit pas multiplier la valeur.

La récurrence terminale correcte est

\[
V_w(D,b)=\max\left\{U_w(D),\;
\max_{a\ \mathrm{admissible}}V_w(D\cup\{a\},b-c_a)\right\}.
\]

La première branche signifie « arrêter ici ». S'il n'y a pas d'action admissible, \(V_w(D,b)=U_w(D)\). La profondeur est finie parce qu'une action n'est exécutée qu'une fois et que le budget diminue strictement.

Une formulation en récompenses additionnelles est équivalente si

\[
r(D,a)=U_w(D\cup\{a\})-U_w(D).
\]

Utiliser \(r=U_w(D\cup\{a\})\) recompterait les acquis à chaque étape et pourrait favoriser artificiellement une longue suite de documents.

La preuve de la récurrence se fait par induction sur le budget : une suite admissible s'arrête immédiatement ou commence par une action admissible ; son suffixe a exactement le problème d'état suivant. Une énumération exhaustive indépendante peut contrôler le programme sur ces petites instances.

Il n'y a aucune nécessité d'introduire \(\gamma<1\), d'apprendre une fonction Q ou de supposer un processus aléatoire. Le modèle décrit l'achèvement conditionnel de livrables. Il ne décrit pas la réussite mathématique de l'expérience qui y figure.

## 6. Sensibilité et priorité robuste

Avec cinq critères et des poids dans \(\{1,2,3\}\), les 243 profils représentent une grille déclarée. Pour plusieurs budgets, il convient de publier :

1. la valeur optimale et tous les portefeuilles optimaux, et non seulement une solution choisie par ordre alphabétique ;
2. l'ensemble des premières actions pouvant commencer une suite optimale ;
3. les tokens communs à tous les portefeuilles optimaux ;
4. les changements de portefeuille lorsque les poids ou le budget changent ;
5. le regret de la règle gloutonne, seulement relativement au même modèle.

Plusieurs ordres peuvent être équivalents pour une utilité terminale. Dans ce cas, une action de premier rang dans une sortie du programme n'est pas une priorité scientifique unique. « Présente dans tout portefeuille optimal » et « peut être exécutée en premier » sont deux propriétés différentes.

La robustesse constatée sur 243 profils reste une robustesse sur cette grille. Elle ne couvre pas les coûts mal estimés, les prérequis oubliés, les tokens attribués de façon contestable ou tous les poids réels positifs. Les recommandations doivent donc préciser le budget, les poids et le domaine de variation contrôlé.

Une action préparatoire peut être utile par les travaux qu'elle débloque, même si sa valeur immédiate est faible. Ce principe justifie Bellman face au seul ratio gain/coût ; il ne justifie pas la liste particulière d'actions ni leurs scores sans examen documentaire.

## 7. Corrections proposées aux pages actives

Les documents historiques et leurs prévisions doivent rester conservés. Les résumés actuels, le navigateur et ses sources JSON peuvent être corrigés en donnant un lien vers le résultat de référence.

| Emplacement actif V637 | Formulation à revoir | Correction précise |
|---|---|---|
| Navigateur : « Distance au but » | Un maillon manquant est présenté comme distance à RH | Nombre de catégories ouvertes ; aucune distance mathématique ou temporelle à RH |
| Coup `theoreme_A_rayon` | « Exposant de Q = Θ−1/2 » | Le demi-exposant normalisé vaut Θ−1/2 ; l'exposant de Q vaut 2Θ−1. Les fenêtres résolues donnent au plus une borne inférieure spectrale, pas le supremum global |
| Chaîne `metrique`, coup `generateur_premiers`, carte des idées | « Positive pour ζ et L » sans borne de portée immédiate | Positivité observée aux seuils numériques des fenêtres testées ; globale non démontrée |
| Résumés du générateur et recensement DH | Décompte historique « attribué exactement » | Séparer attribution numérique et signature exacte d'un quadruplet isolé ; ne pas généraliser le décompte à toutes les compressions |
| Coup V13 `these` | « D ne donne pas un signe résiduel stable » | Étiqueter comme prévision historique conservée ; bilan courant : tendance majoritaire hétérogène 25/8/3 |
| Coup `bases_q_q2` | « D est intrinsèque » sans convention | L'opérateur F est reconstruit ; un logarithme de F demande une convention et comporte une ambiguïté de période |
| Indicateur : résumé actif V631 | T* présenté comme hauteur de la première paire hors droite | Déficit relatif persistant, distingué du comptage direct par V634 |

Les pentes anciennes 0,33 / 0,34 / 0,56 peuvent rester des observations datées. Elles ne doivent pas être expliquées par la seule expression 3 log log X / log X : l'article 1 révisé ajoute la constante log(S/3) et rappelle l'absence de borne d'erreur effective à ce X.

## 8. Bellman comme outil de preuve interne : possibilité conditionnelle

Les paramètres de fonctions auxiliaires, l'extension d'espaces tests et des choix de fenêtres peuvent se prêter à une optimisation finie. Pour les jets, on pourrait par exemple chercher des paramètres admissibles minimisant une borne déjà démontrée. Une récurrence qui réutilise des sous-problèmes correctement définis peut accélérer cette recherche et donner une preuve d'optimalité **dans la classe fixée**.

Ce bénéfice ne fournit pas une propriété arithmétique manquante. Pour agir sur RH, il faut une construction indépendante de RH, puis un lemme démontrant que sa valeur ou son point fixe impose une propriété pertinente des zéros. Ajouter une actualisation \(\gamma<1\) donne une contraction d'un opérateur modifié ; la convergence obtenue ne prouve pas que cette modification conserve l'information nécessaire sur ζ.

La priorité est donc double : optimiser la conduite du programme avec un modèle fini lisible, et garder un dossier séparé pour les conditions d'un éventuel transfert mathématique.

## 9. Dialogue avec la lecture constructive

La lecture constructive a proposé un registre de tous les documents, distinguant nature du résultat, provenance des prévisions et alternatives effectivement documentées. La présente lecture a demandé explicitement de séparer la réalisation d'une procédure du statut de sa thèse, de conserver les réfutations et de ne pas assimiler les états numériques V637 à un certificat.

Accord retenu : reconstruction documentaire complète, modèle déterministe fini initial, statuts précis, unités conventionnelles, aucun crédit de progrès vers RH attribué au calcul de Bellman. Les divergences sur les tokens, coûts et prérequis doivent être exposées dans les données du modèle plutôt que réglées par une probabilité subjective.

## 10. Contrôle de l'implémentation V638

Fichiers effectivement lus : `src/bellman_research.py`, `scripts/run_v638_bellman.py`, `tests/test_v638_bellman.py`, `data/v638_modele_bellman.json`, `data/v638_bellman_resultats.json` et `data/prevision_v638_bellman.md`.

Le code réalise la récurrence terminale avec STOP. Il mémorise les valeurs sur l'ensemble des actions achevées et le budget restant, empêche une action d'être rejouée, exige des coûts entiers positifs, refuse les cycles de prérequis, et conserve les solutions de même valeur. Les tokens partagés sont comptés par union. Le calcul inclut les premières actions optimales et les portefeuilles terminaux ; ces objets sont distincts.

Un contrôle indépendant de cette lecture a reconstruit les **162 sous-ensembles réalisables** des neuf actions, leur coût et leur nombre de tokens par critère, sans appeler la fonction d'utilité ni l'énumérateur livrés avec le modèle. Pour chaque budget 2, 4, 6, 8 et chaque profil de cinq poids dans {1,2,3}, ce contrôle a vérifié la valeur, tous les portefeuilles et l'ensemble de toutes les premières actions optimales. Les **972 configurations** concordent exactement.

Les six tests ciblés ont également été exécutés pendant cette relecture et passent : intérêt d'un livrable différé, saturation des tokens partagés, STOP, conservation des choix équivalents, refus des cycles et coûts nuls, contrôle par sous-ensembles pour les budgets 0 à 8, puis couverture des 61 documents par le registre achevé. Ce dernier test vérifie les numéros couverts ; il ne vérifie pas la vérité mathématique des statuts documentaires.

À poids égaux, le résultat lu est :

| Budget conventionnel | Valeur du modèle | Portefeuilles optimaux | Premiers choix optimaux |
|---:|---:|---|---|
| 2 | 6 | Contraintes V13 et rejeu DH | L'une ou l'autre action, sans préférence d'ordre |
| 4 | 10 | Contraintes V13, rejeu DH, audit NB et contrôle des sources | L'une des quatre actions |
| 6 | 12 | Les quatre actions précédentes, puis comparaison V13 | L'une des quatre actions sans prérequis ; la comparaison attend les contraintes |
| 8 | 13 | Le portefeuille précédent avec soit objet Bellman, soit préparation de relecture | Plusieurs premiers choix ; deux portefeuilles de même valeur |

La grille donne des changements effectifs de priorités : au budget 2, les contraintes V13 et le rejeu DH sont chacun présents dans tout portefeuille optimal pour 210 profils sur 243, et dans au moins un portefeuille optimal pour 237 profils. Au budget 4, les contraintes V13 figurent dans tout portefeuille optimal pour les 243 profils. Ces nombres sont des comptages de profils d'une grille, pas des probabilités scientifiques.

Trois diagnostics exploratoires de coût ont été ajoutés : comparaison V13 ramenée à 1, extension DH ramenée à 1, contraintes V13 portées à 2. Leurs douze sorties à poids égaux ont été recoupées indépendamment de la même façon, y compris les portefeuilles et premières actions. Doubler le coût des contraintes V13 change les valeurs optimales aux quatre budgets en 5, 8, 10 et 12, au lieu de 6, 10, 12 et 13. Les deux réductions de coût modifient notamment des ex aequo. Ces variations montrent la dépendance aux coûts déclarés ; elles ne les calibrent pas et ne couvrent pas tous les scénarios de coût.

La présence d'une action dans tous les portefeuilles peut provenir du coût fixé, de la réutilisation des tokens ou de son rôle de prérequis. Elle ne donne pas un argument indépendant en faveur de sa thèse mathématique. Les portefeuilles ne rendent pas les risques de faisabilité observables : notamment, un bilan négatif des contraintes V13 peut rendre impossible la production de couples. Cette réserve a été transmise et traitée : le second acte porte désormais les tokens `etude_appariement_exact` et `bilan_conditionnel`, avec un rapport de comparaison si elle est faisable, ou une conclusion explicite d'impossibilité avec fermeture de la branche. Aucun couple n'est promis. Ce changement de noms et de portée ne modifie pas les comptages ni les optima rapportés.

Verdict informatique : récurrence et sorties contrôlées pour les instances annoncées. Verdict scientifique : modèle documentaire lisible, conditionnel, sensible à ses hypothèses ; aucune politique optimale de la recherche réelle ni avancée automatique vers RH n'est établie.

### Recoupement du registre historique

Le registre `data/v638_decisions.json` a ensuite été relu : **61 documents numérotés**, **44 étapes historiques** jusqu'à V6.37, distinguées de l'étape V6.38 de l'indicateur courant. Les 61 sources principales existent et leur SHA256 correspond au moment de cette vérification. Les conclusions des documents 12/45, 35/36, 47/51, 56/57/58 et 60/61 ont été recoupées contre les textes et leurs correctifs.

La couverture est documentaire : les textes sont intégralement extraits, puis inspectés par leurs sections pertinentes ; plusieurs textes récents sont lus intégralement. Ni le registre ni ce recoupement n'affirment une expertise ligne à ligne de toutes les preuves, une comparaison de tous les formats alternatifs ou une réexécution de tous les programmes. Les trois articles sont reliés aux bilans récents sans être présentés comme une nouvelle expertise externe.

Deux précisions ont été demandées à la lecture constructive et appliquées au registre : les documents 35/36 possèdent des prévisions historiques conservées dans le navigateur, même si aucun reçu autonome antérieur au calcul n'est identifié ; le document 58 réfute l'identification universelle de T* à une première détection, pas l'existence du seuil relatif lui-même. La borne des cubiques concerne des corps de caractéristique impaire, pas seulement des polynômes impairs. Ces précisions ne modifient aucun résultat de Bellman.

La note constructive a aussi été relue. Sa proposition de contraintes V13, \(u_i=0\) et \(\sum_j u_j e^{-i\phi_j}=0\), fixe effectivement le premier coefficient complexe de \(c=\cos(r)e_i+\sin(r)u\) à \(\cos(r)e^{-i\phi_i}\). Le noyau a une dimension réelle d'au moins trois, donc sa sphère unitaire existe. La variation de D et l'existence de couples avec un contraste suffisant restent à contrôler avant les zéros. Ce constat de dimension ne vaut pas une observation nouvelle de zéros.

## 11. Garde du lemme variationnel sur une compression

Le second usage envisagé de Bellman porte sur une matrice hermitienne G dans un espace doté d'un produit scalaire positif fixé. Pour un sous-espace W de dimension au moins k, la valeur minimale de la somme de k quotients de Rayleigh orthonormés satisfait

\[
F_0(W)=0,\qquad
F_k(W)=\min_{v\in W,\,\|v\|=1}
\{v^*Gv+F_{k-1}(W\cap v^\perp)\}.
\]

Les séquences admissibles sont exactement les repères orthonormés de taille k. Leur somme est la trace de la compression à leur espace engendré. Le minimum vaut donc la somme des k plus petites valeurs propres de la compression à W, par le principe variationnel de trace. Il s'agit d'une réécriture d'un résultat classique en termes de Bellman ; l'optimisation est continue, contrairement au modèle documentaire fini de la section 5.

La garde déterminante est : **une somme négative ne prouve pas k directions négatives**. Par exemple diag(−100,1,1) a une trace négative mais une seule valeur propre négative. Pour établir au moins k valeurs propres négatives, il faut contrôler la k-ième valeur propre, ou exhiber un sous-espace de dimension k sur lequel la forme est définie négative.

Le certificat V636 fait le second travail : il contrôle la compression exacte de dimension 25 avec une borne d'erreur et Gershgorin. La récursion sur la trace ne renforce pas cette conclusion et ne fournit aucune positivité globale pour ζ. Elle propose une organisation variationnelle de la recherche de témoins ; un apport nouveau demanderait une borne arithmétique indépendante qui dépasse le calcul de la matrice déjà connue.

