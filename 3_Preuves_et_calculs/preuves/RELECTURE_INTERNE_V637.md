# V6.37 — Relecture critique de l'expérience V13 appariée

Date : 12 octobre 2026. Statut : relecture interne de la méthode ; aucune relecture externe ni certification d'intervalles n'est prétendue.

## 1. Ce que l'appariement peut isoler

Dans V13 impair, les six caractères sont indexés par k = 1, 3, 5, 7, 9, 11. Les coefficients réels c sont normalisés par ||c||₂ = 1. Avec bᵢ = cᵢ exp(−iφᵢ), on compare

    a1 = |Σᵢ bᵢ|,
    D = 1 + a1² − 2 Re[(Σᵢ bᵢ)(Σᵢ |bᵢ|² conjugate(bᵢ))].

D contient donc a1 algébriquement. Deux bras qui font varier a1 à D comparable et D à a1 comparable peuvent néanmoins fournir des comparaisons conditionnelles locales. Le mot « dissociation » décrit les variables de sélection ; il ne transforme pas ces variables en causes indépendantes.

Une strate fixe une ancre eᵢ et un **angle projectif** r. Pour

    c = cos(r)eᵢ + sin(r)u,  u ⟂ eᵢ,  ||u||₂ = 1,

avec 0 < r < π/4, on a |cᵢ| = cos(r) > sin(r) ≥ |cⱼ| pour j ≠ i. L'ancre la plus proche est donc unique et la distance projective arccos(maxⱼ|cⱼ|) est exactement r. Cette convention ne doit pas être confondue avec la distance sin(r) employée dans certains calculs historiques de projection.

Les seuils d'appariement et les coefficients doivent être figés avant le comptage. Une strate sans couple admissible reste un échec de faisabilité ; relâcher son seuil après consultation des zéros modifierait le protocole. Conserver les valeurs des deux membres et les écarts effectifs permet d'évaluer le contrôle résiduel imparfait des covariables.

Les couples sont ciblés et choisis dans un réservoir de candidats. Ils ne constituent pas un tirage uniforme de V13. Les résultats décrivent ces strates et ce mécanisme de sélection ; ils ne donnent pas, à eux seuls, un effet moyen sur toute la famille ni une estimation causale.

## 2. Comptage total et comptage sur la droite

Le contour symétrique et la domination du premier coefficient fournissent une bonne méthode de comptage numérique. La majoration analytique

    a1 > sqrt(6)(ζ(σR) − 1)

exclut les zéros sur et à droite du bord σR, sous l'interprétation mathématique exacte des coefficients. La réflexion contrôle le bord opposé. Cette majoration ne certifie pas les variations d'argument sur les bords horizontaux.

Le module historique `relief_direct.py` compte les zéros sur la droite par changements stricts de signe de la fonction de Hardy. Il peut manquer :

- deux racines simples contenues dans le même pas ;
- une racine de multiplicité paire, notamment un zéro double ;
- une racine exactement sur un nœud, car le produit de deux valeurs vaut alors zéro et non une quantité strictement négative.

Le déficit `total − critical` peut alors être positif même si les zéros concernés sont sur la droite. Un déficit pair, positif et stable à deux pas ne résout pas ce problème logique : une paire assez proche peut échapper aux deux grilles. La désignation correcte est **déficit numérique de comptage**, puis **détection numérique de zéros hors droite** lorsque des racines complexes indépendantes sont effectivement localisées.

Les variations d'argument obtenues par arguments principaux peuvent également manquer un tour complet entre deux nœuds. La petitesse des sauts observés et du résidu à l'entier contrôle les valeurs échantillonnées ; elle ne borne pas à elle seule la variation entre elles. Aucun résidu flottant proche d'un entier n'est un certificat du principe de l'argument.

Contrôles recommandés :

1. Refaire le comptage critique et le bord vertical à plusieurs pas, et raffiner davantage les cas qui changent ou les minima suspects.
2. Vérifier la cohérence des totaux, la parité et la positivité du déficit, mais aussi sa monotonie en T : un vrai nombre de zéros hors droite ne peut diminuer quand le rectangle grandit.
3. Enregistrer une marge relative sur chaque segment du contour, par exemple |ΣᵢcᵢAᵢ| / Σᵢ|cᵢAᵢ|, et signaler les niveaux qui passent près d'un zéro au lieu d'arrondir automatiquement leur enroulement.
4. Localiser les racines complexes aux premières détections retenues et les recouper avec un second évaluateur à haute précision, reconstructeur indépendant des caractères et phases.
5. Si le maillage ou le contour reste ambigu, conserver un état non résolu et l'exclure d'une conclusion ordonnée ; ne pas convertir cette ambiguïté en censure physique.

Le recoupement par haute précision confirme numériquement une racine. Sans bornes d'erreur validées ou argument de Rouché/intervalle, il ne constitue pas une preuve d'existence au sens d'un certificat formel. De même, aucun de ces contrôles numériques ne démontre l'absence de racines hors droite sur la fenêtre.

## 3. Première détection, intervalle et censure

Si le premier niveau positif du déficit est k et les niveaux sont 1, 2, …, l'intervalle (k−1,k] situe le changement de l'instrument. Il ne situe le premier vrai zéro que si les comptages et la classification sont exacts. Une racine complexe recoupée dans cet intervalle confirme une présence ; elle ne prouve pas qu'aucune racine antérieure n'a été manquée.

Pour l'analyse numérique de cet instrument, les cas doivent rester distincts :

- deux intervalles disjoints donnent un ordre ;
- deux premières détections dans le même intervalle donnent une égalité de grille, pas une égalité de hauteurs ;
- des intervalles qui se chevauchent ne donnent pas d'ordre ;
- une détection avant Tmax et une non-détection à Tmax donnent un ordre de l'instrument, sous réserve de sa fiabilité ;
- deux non-détections à Tmax ne donnent aucun ordre ;
- un cas non résolu constitue une ambiguïté instrumentale, pas une observation censurée fiable.

Écrire « aucune détection jusqu'à Tmax » est plus précis qu'écrire « le premier zéro est supérieur à Tmax ». Affecter Tmax+1 aux censures fabrique des hauteurs inexistantes. Les signes comparables peuvent être rapportés sans imputation.

## 4. Analyse et portée d'une expérience finie

Pour chaque bras et chaque strate, rapporter les signes favorables, défavorables, égalités de grille, chevauchements, doubles censures et non-résolutions. Le dénominateur des proportions est le nombre de couples ordonnables ; le nombre total prévu doit rester visible. Une forte proportion favorable sur quelques couples seulement est moins informative que le même résultat largement réparti entre ancres et rayons.

Les six ancres ne sont pas six types complètement distincts. La conjugaison des caractères k ↔ 12−k correspond à la permutation d'indices [5,4,3,2,1,0]. Elle conserve a1 et D et remplace les ordonnées par leurs opposées ; les hauteurs absolues des zéros sont identiques. Cette symétrie fournit un contrôle du compteur. Une transformation conjuguée d'un point ne constitue pas une réplication indépendante.

L'absence d'un signe agrégé net pour D ne démontre pas l'absence d'effet. Une puissance faible, des censures, des calipers encore larges ou des effets opposés selon les strates peuvent donner ce résultat. De même, un signe favorable récurrent pour a1 soutient une association conditionnelle dans les strates testées ; il ne produit ni un mécanisme analytique général ni une borne sur les zéros.

La conclusion possible est : « la prévision définie avant le comptage résiste, échoue ou reste indéterminée dans ce dessin expérimental ». Le passage à un théorème demanderait une propriété structurelle contrôlant les zéros pour une famille infinie. L'expérience ne prouve ni RH, ni GRH, ni leur négation ; elle teste une proposition numérique locale sur des combinaisons de fonctions L.

## 5. Échanges et recommandations avant calcul

Ces remarques ont été transmises à la lecture constructive avant les nouveaux comptages : conserver ancres/rayons et calipers exacts, séparer censure et ambiguïté, recouper les racines décisives, publier les strates et éviter toute conclusion causale. Le présent mémo pourra être complété par la liste des contrôles effectivement réalisés et de leurs résultats ; les recommandations ci-dessus ne doivent pas être présentées comme déjà exécutées.

## 6. Contrôles effectivement exécutés sur le dessin expérimental

Les huit fonctions de `tests/test_v637_apparie.py` passent lors de cette relecture. Elles vérifient :

- la reconstruction déterministe des candidats et du manifeste, sans consultation de zéros ;
- les 150 directions retenues, dont six témoins d'Euler, et les 72 couples répartis dans 36 strates toutes faisables ;
- les normes, angles projectifs et ancres, ainsi que les calipers, contrastes minimaux et absence de réutilisation des candidats ;
- le score D par calcul indépendant de sa définition originale sur les 12 × 12 couples de classes non nulles modulo 13, et non par répétition de sa formule fermée ;
- l'invariance des scores par changement d'échelle et la symétrie de conjugaison, également vérifiée sur les valeurs complexes de F ;
- la distinction entre censure, données non résolues, égalité de grille, intervalles contigus et chevauchants ;
- le rejet de données non finies, de doublons, d'identifiants d'observation étrangers et de manifestes modifiés ;
- l'analyse à différents plafonds d'un jeu incomplet, sans remplacement des censures par des hauteurs fabriquées.

Ces contrôles portent sur le protocole et son traitement de données. Ils ne valident pas le comptage des zéros, l'existence ou l'absence de racines, ni les prévisions P3 et P4.

L'audit du pilote `scripts/run_v637_apparie.py` a aussi demandé de contrôler la monotonie du déficit **hors droite**, en plus de celle du comptage total, de distinguer les non-détections fiables des cas ambigus et de qualifier les marges de bord comme des marges **échantillonnées**. Ces contrôles sont maintenant intégrés et exécutés ; leurs résultats sont rapportés ci-dessous.

## 7. Relecture des résultats effectivement obtenus

Sources internes relues : `data/v637_v13.json`, `data/v637_v13.csv`, `data/v637_v13_comptages.npz`, `data/v637_selection_v13.json`, `data/v637_racines_recoupees.json`. Aucun coefficient, couple, seuil d'appariement ou texte scientifique de prévision n'a été modifié pendant cette relecture des résultats. L'original octet pour octet du protocole est conservé dans `4_Archives/recus/V637/prevision_v637_apparie.md` ; son SHA256 relu est `844842c26c5eb0bb1ebe0092792753d1255448a1b2005d23e90b1c497ef1a802`, identique à celui enregistré avant comptage. La copie de lecture dans `data/` ajoute seulement un BOM pour l'encodage Windows. Les analyses de covariables signées ci-dessous sont des diagnostics après calcul, et non de nouvelles prévisions.

### Fiabilité numérique effectivement contrôlée

Les 150 directions satisfont les critères numériques fixés. La comparaison indépendante des tableaux NPZ retrouve :

- aucun changement des totaux entre les pas 0,02 et 0,01 ;
- aucun changement des comptages critiques entre les pas 0,02, 0,01 et 0,005 ;
- une identité exacte des tableaux entiers `off = total_fine − critical_finest` ;
- des déficits pairs, non négatifs et non décroissants en T ;
- des comptages totaux et critiques non décroissants ;
- aucun contour horizontal non résolu selon le critère numérique ;
- des marges relatives **échantillonnées** d'au moins 3,2546897 × 10⁻⁵ sur les bords horizontaux et 0,0042703 sur le bord droit.

Le bord droit commun est σR = 9 ; la marge de domination du premier coefficient est 0,0047773. Les deux résidus maximaux d'enroulement entier sont environ 1,2 × 10⁻¹⁰. Les six témoins d'Euler n'ont aucun déficit détecté. Les cinq non-détections non Euler sont admissibles et distinctes d'une ambiguïté instrumentale ; aucun cas ambigu n'est recensé.

Ces chiffres contrôlent une réalisation numérique, dans les limites de la section 2. Ils ne changent pas son statut en certificat d'absence ou de premier zéro.

Le recoupement indépendant annoncé dans le protocole est terminé et relu : 24 racines sur 24 sont retrouvées à une précision de travail de 50 chiffres. Il couvre les deux membres du premier couple de chaque bras et de chaque ancre au rayon médian 0,65. Toutes les racines sont dans la tranche de détection annoncée et strictement hors droite, avec Re(ρ) − 1/2 ≥ 0,0572644. Leurs 24 partenaires de réflexion sont également acceptés. Le résidu maximal de racine est 3,5754 × 10⁻⁵⁴ ; le résidu maximal du partenaire après le facteur de réflexion est 1,1519 × 10⁻⁴⁹. L'écart maximal entre localisations Euler–Maclaurin et mpmath est 2,2299 × 10⁻¹².

Ces résultats écartent notamment l'hypothèse d'un simple déficit de racines critiques pour les 24 détections représentatives recoupées. Ils ne certifient ni l'absence d'une paire antérieure, ni tous les autres déficits. Les 50 chiffres sont une précision de travail et non 50 chiffres dont l'erreur serait certifiée.

### Bras A1

Les 36 couples donnent tous une première détection plus tardive du côté où a1 est plus grand, aux plafonds 50, 100 et 150. Le résultat couvre toutes les ancres et tous les rayons du dessin fixé. Les trois plafonds sont des lectures emboîtées des mêmes observations, pas trois réplications indépendantes.

Le contraste est très ciblé :

| Grandeur | Intervalle effectivement sélectionné |
|---|---:|
| a1 du membre bas | 0,0096969 à 0,3535640 |
| a1 du membre haut | 1,1728138 à 1,4858326 |
| Écart haut moins bas | 0,9881108 à 1,3903827 |
| Écart signé D haut moins D bas | −0,0328022 à +0,0396574 |
| Première détection du membre bas | 1 à 9 |
| Première détection du membre haut non censuré | 28 à 135 |

Les cinq membres hauts sans détection sont censurés à 150 ; leur hauteur n'est pas imputée. L'écart de a1 médian est 1,1972342, très au-dessus du minimum prévu de 0,20. L'optimisation des contrastes a donc choisi deux régions assez éloignées en a1. Les 36 signes favorables valident P3 dans ce dessin ; ils ne démontrent pas une loi monotone pour de petites variations de a1, une causalité ni un résultat sur tout V13.

### Bras D : tendance réelle et hétérogénéité

Sur 36 couples, un D plus grand accompagne 25 détections plus précoces, huit plus tardives et trois égalités de grille. Parmi les 33 couples ordonnables, la proportion plus précoce est 25/33 = 75,76 %. Il s'agit d'une proportion descriptive sur des couples ciblés, sans test p confirmatoire.

| Ancre | Caractère k | D haut : plus précoce | Plus tardif | Même tranche |
|---:|---:|---:|---:|---:|
| 0 | 1 | 6 | 0 | 0 |
| 1 | 3 | 4 | 2 | 0 |
| 2 | 5 | 4 | 2 | 0 |
| 3 | 7 | 5 | 1 | 0 |
| 4 | 9 | 2 | 2 | 2 |
| 5 | 11 | 4 | 1 | 1 |

| Angle projectif | D haut : plus précoce | Plus tardif | Même tranche |
|---:|---:|---:|---:|
| 0,45 | 9 | 3 | 0 |
| 0,65 | 5 | 4 | 3 |
| 0,75 | 11 | 1 | 0 |

La direction majoritaire est la même pour les trois rayons et pour cinq ancres ; la sixième est équilibrée. À la résolution des 18 strates ancre × rayon, dix strates ont deux signes plus précoces, cinq ont un signe de chaque sens, une a deux égalités de grille, une a deux signes plus tardifs et une a un signe plus tardif avec une égalité. L'hétérogénéité est donc établie, mais elle coexiste avec une tendance majoritaire.

### Le caliper résiduel de a1 explique-t-il cette tendance ?

Notons Δa1 = a1 du membre D haut − a1 du membre D bas. Sa plage est [−0,0216649 ; +0,0292762], avec médiane +0,0194847. L'écart de D est compris entre 0,3691866 et 0,9639865, avec médiane 0,6740213.

| Signe résiduel de Δa1 | D haut : plus précoce | Plus tardif | Même tranche | Total |
|---|---:|---:|---:|---:|
| Δa1 > 0 | 17 | 5 | 3 | 25 |
| Δa1 < 0 | 8 | 3 | 0 | 11 |

Huit des 25 signes plus précoces sont compatibles avec l'explication simple « a1 est un peu plus petit ». Les 17 autres se produisent alors que a1 est **plus grand**, ce qui va dans le sens opposé à l'association attendue du bras A1. Une diminution résiduelle de a1 ne peut donc expliquer à elle seule l'ensemble des 25 signes sous un modèle monotone où a1 serait l'unique facteur du classement.

Ce diagnostic ne prouve toutefois pas un effet indépendant de D. Le contrôle de a1 est approximatif ; aucune borne de sensibilité des hauteurs à a1 n'est démontrée, et les autres composantes des directions varient. Une comparaison de deux fonctions ne constitue pas une intervention qui modifierait seulement D. Le résultat exclut une lecture simpliste du biais résiduel ; il laisse ouverte l'identification d'un mécanisme propre à D.

### Statut précis de P4

P4, telle qu'écrite avant calcul, demandait une direction **non uniforme** entre ancres et rayons. Les signes opposés et les strates de sens contraire constatent cette nonuniformité au sens descriptif faible. Le protocole ne fixait pas de seuil quantitatif pour une « absence de direction stable » ou une neutralité de D ; ces propositions plus fortes ne peuvent pas être déclarées vérifiées après coup.

La formulation recommandée est donc : **« Le contraste D est majoritairement associé à une détection plus précoce, avec des exceptions et une hétérogénéité marquée ; son indépendance et son mécanisme restent ouverts. »** Écrire « D n'a pas d'effet » ou « aucun signe résiduel » serait contraire au résultat observé. Écrire « une seconde force de D est démontrée » dépasserait également ce que l'expérience établit.
