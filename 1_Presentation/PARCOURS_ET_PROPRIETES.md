---
title: "Les chemins parcourus : propriétés, bifurcations et portes ouvertes"
subtitle: "V6.54 - Lecture transversale du navigateur, de Bellman, des indicateurs et des graphes"
author: "Vincent P. P. NOËL — dossier de recherche, rédaction assistée"
date: "14 octobre 2026"
lang: fr
---

# Ce que cette carte permet de retrouver

La destination est précise : établir RH. Ce qui manque est un mécanisme
arithmétique capable d'imposer une propriété globale. Les documents donnent
plusieurs chemins vers cette destination ; aucun n'est achevé.

Cette carte retrace les **parcours documentés**, avec leurs bifurcations et
leurs limites. Elle réunit les systèmes qui les décrivaient séparément :
navigateur, indicateur, Bellman, graphes des passages, grammaire des domaines,
Legos et protocoles de calcul. Le complément sur les corrélations est finalisé
et inclus dans le ZIP global V6.54.

**Une propriété vraie ne s'éteint pas.** Une conjecture peut être réfutée, une
méthode devenir insuffisante, ou un programme être suspendu. Nous séparons ces
trois situations. « Fait » dans un navigateur signifie parfois « étude
exécutée », même si sa thèse a échoué.

![Trois chemins globaux ; les obligations orange restent à démontrer.](CARTE_DES_PARCOURS.png)

## Comment lire les verdicts

| Statut | Sens précis |
|---|---|
| **Établi dans le dossier** | Une démonstration circonscrite est écrite et sa portée est indiquée. Les anciennes preuves ne reçoivent pas ici une nouvelle expertise intégrale. |
| **Conditionnel** | L'implication est disponible ; son hypothèse reste à prouver. |
| **Mesuré ou certifié localement** | Un domaine fini et un modèle d'erreur sont indiqués. Un diagnostic flottant et un certificat sont distingués. |
| **Réfuté dans sa portée** | Un contre-exemple ou une obstruction ferme le candidat sous ses hypothèses explicites. |
| **Suspendu** | La piste n'a pas fourni le gain recherché ; aucune impossibilité générale n'en découle. |
| **Ouvert** | L'énoncé nécessaire est identifié mais sa preuve manque. |

Les documents 06 et 62 sont eux-mêmes des reconstructions historiques. Les
explications de transition ci-dessous sont une **synthèse de leurs traces**,
pas une récupération d'un raisonnement interne interrompu. Les scénarios de
réouverture sont nos propositions actuelles, signalées comme telles.

# 1. Le parcours mathématique, de la première énergie aux corrélations ancrées

| Étape et traces | Question et chemin suivi | Propriété conservée | Ce qui a changé ou reste ouvert |
|---|---|---|---|
| Nyman–Beurling et énergie Q ; 06, 12, 37, 62 | Approcher une fonction par des combinaisons arithmétiques, puis suivre une énergie de doubles convolutions de Mangoldt. | Identités de projection et d'annulation ; théorèmes A/B exposés et prérelus dans le corpus. | Les projections étudiées retrouvaient Q. Les bornes asymptotiques suffisantes n'en découlaient pas ; le statut des articles reste celui du dossier. |
| Énergie, dimension et unités ; 08, 50 | Lire l'exposant comme une dimension, et la variation d'énergie comme un bilan. | Homogénéité des unités et identités de sommation par parties. | Positivité et changement de vocabulaire ne bornent pas l'exposant. La lecture mécanique survit comme explication. |
| TOMO et DARK-ZETA ; 15–17, 24 | Chercher une signature statistique de la multiplicativité. | L'ordre 2 conserve la puissance mais perd la phase ; l'ordre 3 conserve certains couplages de phase. | Le bispectre brut du canal choisi teste des relations entre ordonnées de zéros. Dans l'autre canal, il restitue le défaut multiplicatif par définition. Ce candidat précis est clos. |
| PRIME-LOCK et DUAL-LOCK ; 18–24 | Relier produit d'Euler local et signe global. | Détecteurs distincts de structure locale et d'inertie de Weil ; témoins adversariaux. | Le verrou local mesuré ne suffit pas au signe global. Les quatre cas du tableau local/global interdisent ce raccourci. |
| Modèle réduit ; 28–29 | Comprendre une nécessité là où une RH est un théorème : courbes sur corps finis. | La positivité géométrique et les faux jumeaux séparent structure authentique et simple symétrie. | Le transfert de cette géométrie à ζ n'est pas construit. Une marge nulle n'empêche pas la positivité. |
| Archipel d'Euler ; 27, 30, 38–45 | Déformer des fonctions de même équation fonctionnelle et suivre les sorties de la droite. | Rigidité dans les espaces précis de degré 1 ; îles et rencontres observées. | Le corollaire de rigidité était déjà connu. Les lois universelles de hauteur, et l'extension au degré 2, ne résultent pas de la carte finie. |
| Chaînon et générateur ; 32–36 | Traduire comptages, traces, spectre et flot continu. | Reconstructions sans injecter les zéros cibles ; règles de passage discret/continu. | L'opérateur seul ne suffit pas : la métrique positive et la complétude restent décisives. Le logarithme d'un opérateur exige aussi un choix de branche. |
| Surface et Frobenius virtuels ; 46–54 | Chercher l'analogue de l'étage géométrique supérieur. | Des signatures et modèles algébriques de comparaison. | Aucun objet géométrique suffisant pour ζ n'est construit. L'échec de la transplantation directe de Stepanov ferme ce modèle, avec conditions explicites de réouverture. |
| Jets, relief et certificats ; 56–61 | Distinguer multiplicativité, coefficients et mouvements des zéros. | Lemmatisation du rang ; témoin DH avec au moins 25 directions négatives dans une fenêtre, sous le budget déclaré. | Une borne inférieure d'inertie n'est pas un compte exact. Les associations numériques entre défaut et sortie ne démontrent pas une causalité. |
| A complexe, fibres et plis ; 63–66 | Fixer ancre, rayon et coefficient complexe avant de comparer. | Faisabilité par une ellipse ; fibres calculables ; à A=0, D est constant. Un pli et sa paire sont certifiés dans une boîte choisie. | Le sens du déplacement dépend de la strate. Les passages entre toutes branches, toutes collisions et un A arbitraire ne sont pas réglés. |
| Domaines et changement de métrique ; 67–70 | Construire des tests admissibles, une queue positive et un Schur effectif. | P, moments, parité, cœur dense, métrique logarithmique et réduction tête–queue. | La marge uniforme en norme H¹ est exclue. La nouvelle métrique rend la réduction possible ; elle ne fournit pas le signe de la tête corrigée. |
| Legos et opérateur commun ; 71–75 | Payer ensemble tête, sources, queue et couplages. | Certificats locaux du dossier jusqu'à S=11/20 ; paiement multi-premiers et transport exact des supports. | Le diagnostic au-delà de 1/2 a dû être séparé du certificat continu obtenu ensuite. Aucun de ces résultats ne couvre tous les supports. |
| Compensation signée et transport ; 76–79 | Revenir à la fluctuation première, puis chercher un transport positif conservant le barycentre. | Deux grammaires couvrantes ; bilans de réserve ; brique initiale ; gardes de coupures et obstructions précises. | L'admissibilité de toutes les lignes et la loi de signe du profil réel restent ouvertes. Les gardes agrégées de rapport fixe échouent à grande échelle. |
| Corrélations, identité et énergie J ; complément courant | Garder les positions et les coupures, identifier les vrais coefficients, borner une énergie globale. | Identité de diviseurs ; formule exacte de corrélation ancrée ; contre-modèles ; critère classique de Cramér. | La borne globale J(X)=O(X²) reste à démontrer. Ce retour à une énergie retrouve un fil déjà cité dans 37/45. |

Deux énergies ne doivent pas être confondues : **Q** dans les théorèmes A/B
concerne les sommes d'une double convolution ; **J** dans le complément courant
concerne directement l'erreur ψ(x)−x. Les preuves, les normalisations et les
hypothèses doivent accompagner le passage de l'une à l'autre.

# 2. Le parcours des outils de recherche

| Système | Sa fonction dans le parcours | Propriété obtenue | Limite et correction actuelle |
|---|---|---|---|
| **Navigateur — 34** | Comparer des coups avec question, témoin, garde, coût et prévision. | Les décisions et leurs raisons deviennent consultables. | Ses scores sont conventionnels. Ils ne mesurent ni une distance à RH ni une probabilité de succès. Ses bilans ont été prolongés jusqu'au dossier courant. |
| **Indicateur — 31** | Situer sept dimensions : voir, comprendre, situer, degré 2, démontrer, case vide et croiser. | Les mesures, preuves et relectures occupent des niveaux distincts. | Aucun pourcentage global de RH. La synchronisation actuelle ne relève aucun niveau de maturité. |
| **Bellman documentaire — 62** | Optimiser des livrables finis sous budget et prérequis. | Récursion exacte dans le modèle ; tokens partagés comptés une fois ; contrôles par énumération dans le dossier. | L'union de tokens est sous-modulaire : elle représente mal les coups doubles qui n'existent qu'après jonction de deux constructions. |
| **Bellman de contrats — 67** | Représenter des obligations ET et des voies alternatives OU, avec issues favorables ou défavorables. | Une réfutation utile et une preuve positive reçoivent des statuts distincts. Les complémentarités peuvent être représentées. | Les issues et les coûts restent déclarés. Un scénario ne peut créditer automatiquement RH ou le signe global. |
| **Bellman spectral — 62** | Minimiser une trace sur des repères orthonormés. | Réécriture variationnelle de sommes de valeurs propres. | Une trace négative ne compte pas les directions négatives ; cette écriture n'apporte pas seule une borne nouvelle. |
| **Bellman de la forme — 67–70** | Éliminer un bloc d'une forme quadratique. | Le complément de Schur identifie exactement la dette des couplages. | La récursion devient mathématique ; le signe de chaque dette et les conditions de noyau restent à contrôler. |
| **Graphes — 65, 66, 67** | Montrer respectivement passages, certificats et ponts de domaines. | Une implication, une expérience et une obligation manquante peuvent être distinguées. | Un graphe ne prouve pas ses nœuds. Les graphes anciens gardent leur domaine ; la carte présente les relie au lieu de les fusionner. |
| **Grammaire et Legos — 68–75** | Faire circuler les tests avec support, moments, parité, norme et erreur. | Des transformations deviennent réutilisables ; la même erreur peut servir plusieurs contrats. | Les jets d'un test ne sont pas les jets d'un zéro critique. Une opération qui préserve l'admissibilité ne préserve pas nécessairement le signe. |

Le défaut de Bellman n'était donc pas un choix « trop glouton » : la
programmation dynamique explorait le modèle déclaré. Le catalogue d'actions
et la fonction de valeur privilégiaient les livrables préparatoires. Le passage
aux contrats et au Schur constitue la bifurcation conceptuelle documentée.

# 3. Les voies éteintes, révisées et simplement suspendues

## Obstructions établies dans une portée déterminée

| Candidat | Pourquoi il échoue | Ce que l'obstruction ne ferme pas |
|---|---|---|
| TOMO-3 brut comme pont inédit vers la multiplicativité | Mauvaise variable de couplage ; dans le canal adapté, la fermeture redonne le défaut déjà défini. | D'autres statistiques et des corrélations qui gardent l'ancrage. |
| Produit d'Euler ou symétrie seuls comme garanties du signe | Témoins du dossier satisfaisant certains de ces traits sans le signe recherché. | L'identité complète de ζ avec une estimation quantitative supplémentaire. |
| Métrique positive non dégénérée du compagnon local au pli | Un bloc de Jordan non trivial ne peut être autoadjoint dans une métrique définie positive. | Une autre réalisation opératoire ou le signe global de Weil. |
| Marge strictement positive uniforme dans la norme H¹ à support fixé | L'opérateur représentant la forme y est compact, sur un espace de dimension infinie. | Une forme positive sans marge, ou une métrique différente. |
| Modèle continu corrigé B₀ positif sur tous supports | Familles admissibles donnant B₀ négatif aux grandes échelles. | La forme complète B₀ plus la fluctuation première signée. |
| Listes finies de phases ou préfixes matriciels comme contrôle universel | Réalignement des phases ; contre-opérateurs indiscernables sur un préfixe fini. | Une loi arithmétique couvrante et une queue contrôlée. |
| Blocs de transport de rapport fixe contrôlés seulement par masse et moment | La garde agrégée du document 79 devient négative sous le théorème des nombres premiers. | Le profil intérieur réel, un autre découpage ou une garde plus informative. |
| Forçage positif de Selberg ⇒ inversion positive générique | Contre-modèle exact avec réservoir exponentiel. | Une propriété supplémentaire propre aux vrais coefficients premiers. |
| Autocorrélation par écarts ⇒ signe de tous les potentiels | Deux configurations exactes de même masse, barycentre, bornes et paires ont des potentiels différents. | Les corrélations ancrées, qui conservent les positions absolues et les coupures. |
| Borne d'énergie d'une suite quelconque ⇒ signe du signal de Suzuki modifié | La suite a(n)=1, n≥2, a une énergie globalement bornée à l'échelle X² et un signal modifié négatif certifié. | Le transfert pour Λ, rendu valide par son identité arithmétique exacte. |

Ces deux derniers contre-modèles sont construits et vérifiés dans le complément
courant. Ils ne donnent aucun contre-exemple à RH.

## Réouvertures documentées

Le **GPS/Kalman**, rejeté lorsqu'il filtrait Q, a été repris sur les traces des
premiers sous forme d'innovations de **Levinson** : c'est un détecteur d'une
perte de positivité sur les fenêtres testées. Sa positivité à tous les ordres
reste l'obligation globale.

Les **sources cachées** ont été relues avec la masse d'un mode : le mode fantôme
de l'ancien calcul ne portait pas la masse d'un vrai zéro. La recherche d'une
borne d'observabilité uniforme reste différente de cette correction locale.

L'idée **Schrödinger/Hilbert–Pólya** a survécu sous la forme d'une construction
depuis les premiers. La métrique positive et la complétude n'ont pas été
obtenues globalement. Une contractivité automatique ne les remplace pas.

La **compensation signée du document 70** n'a pas été réfutée. Les étapes
71–75 ont surtout amélioré des enveloppes et des certificats locaux. Le
document 76 l'a explicitement remise au centre : c'est la principale piste
qu'il serait injustifié de déclarer morte.

L'**attaque directe sur une énergie**, arrêtée dans son ancien mécanisme,
retrouve maintenant une cible classique avec J. La réduction est valide ;
la borne de croissance reste entière. La nouveauté de présentation ne doit
pas être comptée comme une estimation nouvelle.

## Suspensions qui ne sont pas des impossibilités

Les estimations de densité, les sommes de Möbius, la géométrie virtuelle et
la recherche de fonctions auxiliaires n'ont pas fourni la clôture voulue
dans les modèles documentés. Leur réouverture exige un nouvel objet ou une
nouvelle estimation précise. Le corpus ne démontre pas que toutes leurs
variantes sont impossibles.

# 4. Où tous les chemins rejoignent le but global

La voie directe de Weil demande, avec les domaines et moments déclarés :

\[
\forall S>0,\quad \forall f\in X_S,\qquad Q_W(f)\ge0.
\]

À support fixé, le changement de métrique et la queue positive ramènent la
question au signe d'un Schur effectif. Il reste à contrôler la tête **et sa
dette**, puis à couvrir chaque support. Le nombre fini de directions
potentiellement dangereuses peut dépendre de S.

| Porte | Ce qui est conservé dans les briques | Obligation globale restante |
|---|---|---|
| **Arithmétique** | Annulation polaire, identité de fluctuation, phases et coefficients exacts. | Loi de compensation signée sur les directions admissibles. |
| **Tête et queue** | Queue positive effective et réductions locales du dossier. | Tête et reste contrôlés pour une famille non bornée de supports. |
| **Couplages** | Formule de Schur et résidus des sources ; opérateur commun dans les certificats locaux. | Payer chaque dette avec les sources et normes de la voie effectivement choisie. |
| **Couverture** | Cœurs denses, transport des moments, grammaires couvrantes dans leurs topologies. | Signer toute la famille, puis passer à la limite avec la continuité nécessaire. |

**Correction de portée.** Une norme de graphe est nécessaire lorsqu'on
transporte l'action d'un opérateur non borné. Pour étendre le signe d'une
forme continue, la norme de forme et un cœur dense suffisent dans le cadre
des documents 67 et 75. Exiger partout une norme de graphe ajouterait une
obligation inutile ; ignorer toute topologie de convergence serait incorrect.

Deux autres portes globales sont explicitement reliées à celle de Weil :

- Le **signal spécifique de Suzuki**, non négatif à toutes les échelles,
  satisfait un critère équivalent à RH. Les transports convexes sont des
  mécanismes suffisants candidats ; leur existence globale reste ouverte.
- Pour les **vrais coefficients Λ**, le critère classique est
  \(RH\Longleftrightarrow J(X)=O(X^2)\), avec
  \(J(X)=\int_1^X(\psi(x)-x)^2dx\). Le complément fournit la preuve du sens
  borne vers RH, la formule ancrée et les contre-modèles de portée.

La carte d'identité
\(\sum_{d\mid n}\Lambda(d)=\log n\) identifie la bonne suite ; elle ne
fournit pas la borne. Cette distinction explique pourquoi les statistiques
génériques, même favorables, ne remplissent pas l'obligation de Weil.

# 5. Les bifurcations utiles maintenant

Les trois choix suivants sont des **programmes proposés**, sans résultat
global prédit :

1. **Reprendre la compensation signée sur les directions dangereuses.**
   Utiliser la réduction tête–queue pour cibler les interactions qui décident
   le signe, en gardant les couplages. Un succès exige une inégalité valable
   pour toute la famille, et non une suite de matrices positives.
2. **Remplacer les blocs agrégés par une information de profil.**
   Relier positions, diviseurs et corrélations ancrées aux réserves de
   transport. Une garde qui survit aux contre-modèles et aux bords serait
   un gain ; sa positivité sur tous les blocs reste à établir.
3. **Confronter ces deux voies à la borne énergétique classique.**
   Chercher si une même estimation arithmétique contrôle simultanément la
   dette de signe et la croissance de J. Ce serait un coup double précis.
   Aucune implication générale entre les deux estimations n'est démontrée ici.

Nous disposons de traductions, d'identités, de contre-modèles et de certificats
locaux réutilisables. La propriété encore recherchée est une **contrainte
arithmétique quantitative à toutes les échelles**. Ni le navigateur, ni
Bellman, ni une couverture dense ne peuvent la créditer à la place d'une preuve.

# Sources, traçabilité et achèvement

Le relevé s'appuie sur l'archive identifiée V6.53, ses index, ses états de
recherche et les documents indiqués dans les tableaux. Le registre JSON
joint contient les événements, leur statut, leur domaine et leurs sources.
Les anciennes notices restent accessibles ; elles ne sont pas réécrites
comme si les décisions actuelles avaient été connues auparavant.

Les pages actives donnent accès à cette carte et au complément courant.
Les données et les générateurs de l'indicateur et du navigateur sont
synchronisés ; les maturités et les anciens résultats de Bellman sont
conservés. Cette synchronisation achève le travail documentaire demandé,
sans valider à nouveau toutes les preuves historiques.

**Sources principales du corpus :** 06 (histoire), 24 (instruments), 31/34
(indicateur et navigateur), 36 (rejets relus), 37/45 (Cramér et théorèmes A/B),
50 (unités), 62 (atlas Bellman), 63–66 (contraintes et plis), 67–70 (ponts,
domaines et fluctuation), 71–75 (Legos et certificats), 76–79 (reconstruction,
transport et obstructions), puis la note courante
*Corrélations ancrées, carte d'identité et réduction énergétique*.

**Sources primaires ciblées :** R. P. Brent, D. J. Platt, T. S. Trudgian,
*The mean square of the error term in the prime number theorem*, JNT 238
(2022), 740–762,
<https://maths-people.anu.edu.au/~brent/pd/rpb274-final.pdf> ;
M. Suzuki, *Aspects of the screw function corresponding to the Riemann
zeta-function*, <https://arxiv.org/pdf/2206.03682>.

Le statut de lecture des autres références reste celui des documents sources.
Une réfutation locale ne devient pas une impossibilité de RH, et une piste
non réfutée ne devient pas une preuve probable.
