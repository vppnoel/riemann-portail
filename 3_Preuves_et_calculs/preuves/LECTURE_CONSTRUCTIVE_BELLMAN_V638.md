# V6.38 — Lecture constructive : atlas de décisions et principe de Bellman

**Date :** 12 octobre 2026. **Nature :** lecture interne constructive des décisions documentées. Elle est confrontée à la lecture critique parallèle. Aucun résultat nouveau sur RH, aucune expertise humaine et aucune publication externe ne sont revendiqués.

## 1. Ce que la reprise du corpus permet

Le corpus possède déjà les éléments d’une recherche séquentielle : des objets précis, des interventions, des témoins négatifs, des prévisions, des résultats, des règles d’arrêt et des révisions de priorités. Bellman peut articuler ces éléments, en tenant compte de ce qu’une action rend possible ensuite. Il ne remplace ni un lemme arithmétique ni la justification d’un choix de récompense.

L’acquis utile n’est pas toujours une affirmation positive. L’échec de TOMO3 a identifié une confusion de canaux. L’échec de la taille effective réelle a éliminé un modèle inadmissible. La validation directe du relief a rectifié son observable. Ces résultats réduisent l’incertitude et ferment des extrapolations abusives. Ils doivent apparaître dans l’état, avec leur portée, plutôt que comme des « échecs de recherche » sans valeur.

## 2. Couverture et limites

Le registre `data/v638_decisions.json` couvre les **61 documents numérotés 01 à 61**, avec une source principale par numéro et regroupement des formats équivalents. Les sources ont été intégralement extraites en texte. La lecture sémantique est ciblée : introductions, sections de résultats, conclusions, règles d’arrêt, limites et correctifs ; les grands documents sont parcourus par sections. Les textes récents 55–61 et plusieurs petits textes ont été lus intégralement. Ce travail n’est pas une nouvelle expertise ligne à ligne de chaque preuve.

Les **44 étapes historiques de l’indicateur, jusqu’à V6.37**, sont également conservées. Leur résumé est une donnée historique du corpus, pas un résultat redémontré en V6.38. La nouvelle étape V6.38 est exclue de cette base historique pour éviter que l’audit se cite lui-même comme acquis antérieur.

Les principaux compléments parcourus sont les lemmas A, le terme dominant B, les difficultés H3 et Nyman–Beurling, les mémos Weil/densité, les dossiers de pré-relecture A/B/Archipel, les preuves des jets V6.34 et de la tour V6.35, le certificat V6.36 et la relecture V6.37. Les trois articles actuels sont situés par leurs énoncés et corrections documentés dans les dossiers récents ; ils ne sont pas trois expertises intégrales nouvelles. Les programmes historiques ne sont pas tous réexécutés ici. Les 163 sources externes ne sont pas toutes relues dans leurs originaux.

Les empreintes sont des **empreintes de lecture** des octets disponibles pendant l’audit. Les pages générées peuvent être modifiées ensuite lors des corrections V6.38. Les documents 01, 06 et 07 sont explicitement des vues historiques V6.24. Un fichier nommé « fait » ou « présentable » ne prouve ni la thèse annoncée ni une relecture extérieure.

## 3. Trois trajectoires qui justifient l’atlas

| Trajectoire | Résultat conservé | Correction ou question ouverte | Décision qu’elle éclaire |
|---|---|---|---|
| Énergie Q → projection → annulation du pôle | Identité exacte e²=β²Q+T_N | Normalisation de β, contrôle du reste et conclusions asymptotiques restent conditionnels | Auditer les hypothèses avant un nouveau plateau numérique |
| Compression de Weil → audit → certificat DH | Un sous-espace de dimension 25 est validé négatif dans une fenêtre | Compte total exact, complément et autres fenêtres ouverts | Passer de concordance de programmes à un budget d’erreur complet |
| Relief relatif → a(1) après coup → V11 → V13 | Association a1 retrouvée ; comparaison appariée descriptive | Phase, tolérances résiduelles et variation de D à premier coefficient exactement fixé | Tester d’abord la faisabilité des contraintes exactes |

La distinction de temps est essentielle. Le critère persistant T* du document 56 est choisi après observation du bruit ; il ne devient pas le critère prévu. L’hypothèse a1 du document 57 est exploratoire puis retestée en V6.34 et V6.37. La cinquième prévision du document 47 est postérieure au premier calcul, mais antérieure au second. Une date d’antériorité doit donc être relative à l’expérience concernée.

## 4. État, action et utilité

Un état utile est un ensemble structuré d’acquis et d’incertitudes : objets définis, assertions avec hypothèses, contrôles numériques, certificats, provenance, contre-exemples, options encore faisables et coûts estimés. Le numéro d’un document ou les sept niveaux de l’indicateur ne suffisent pas à résumer cet état. Ils pourraient masquer un correctif décisif.

Une action produit un dossier vérifiable : étude de faisabilité, protocole figé, contrôle de calcul, tentative de borne avec obstacle explicite, notice de conditions d’une source ou paquet de relecture. La réussite d’une action de documentation ne promet pas que l’effet espéré existe. Une impossibilité démontrée ou documentée peut satisfaire le contrat de l’action.

Les acquis sont comptés une fois. Une seconde figure ou un PDF des mêmes observations ne gagne pas un second crédit de découverte. Une certification peut avoir une valeur propre car elle change le statut du résultat. Les unités conventionnelles d’utilité et de travail rendent la formule homogène ; elles ne rendent pas les pondérations objectives et ne donnent pas une énergie physique.

## 5. Premier modèle défendable

Le premier usage est une planification déterministe, à budget fini, de dossiers vérifiables. Si A(s,b) est l’ensemble des actions admissibles, F la transition documentaire et c(a)>0 le coût entier, on peut définir

\[
W_{\mathrm{gain}}(s,b)=\max\left\{0,\max_{a\in A(s,b)}
\left[r(s,a)+W_{\mathrm{gain}}(F(s,a),b-c(a))\right]\right\}.
\]

Cette valeur porte seulement sur les gains nouveaux : elle correspond à W=V−U dans l’annexe formelle et le code, où V comprend l’utilité terminale déjà acquise. La récompense r est la différence d’utilité de l’union des tokens. Le zéro autorise l’arrêt. Le budget strictement décroissant termine la récursion. Une action déjà réalisée ne peut pas être rejouée pour accumuler la même utilité. Le maximum dépend des prérequis et du coût déclaré. Une définition terminale fondée sur un ensemble de jetons distincts évite le double comptage et permet d’examiner plusieurs pondérations.

Le modèle construit par root comporte neuf actions et seize jetons documentaires ; les coûts et critères sont déclarés, non appris dans l’histoire. La lecture critique a confronté programmation dynamique et énumération exhaustive pour 972 configurations. Ce contrôle valide le calcul **relativement au modèle**, pas l’optimalité de la stratégie réelle de recherche. Les probabilités de succès et transitions empiriques ne sont pas identifiées par le corpus. Les fréquences d’un portefeuille dans une grille de poids sont des fréquences de scénarios de préférence, jamais des probabilités de résoudre RH.

## 6. Leviers concrets

**Ancrage V13 : définir les contraintes avant les zéros.** L’espace impair modulo 13 a six coordonnées réelles. Pour une ancre i, les contraintes u_i=0 et somme u_j exp(−iφ_j)=0 sont trois contraintes réelles au plus. Leur noyau et sa sphère unitaire doivent être définis puis contrôlés. Fixer c=cos(r)e_i+sin(r)u donne alors a(1)=cos(r)exp(−iφ_i) dans la strate. Il reste à vérifier la variation effective de D, la sélection de couples et le coût des comptages. Aucun couple exploitable ni contraste suffisant n’est promis avant cette étude.

**Certificat DH : conserver le résultat exactement formulé.** V6.36 établit au moins 25 directions négatives pour a=0,02, h=0,005, L=1115, sous le modèle d’intervalles/arrondi annoncé. Cela demeure le contrôle le plus solide de cette chaîne, sans positivité du complément. Une extension peut informer la stabilité, mais ne doit pas récompenser comme « découverte » le seul rejeu du même témoin.

**Socle analytique : enlever les hypothèses implicites.** Dans Nyman–Beurling, l’identité β²Q+T_N est acquise, la limite de β ou T_N ne l’est pas. L’audit des conditions et la préparation d’un dossier de relecture ont un coût relativement faible et protègent plusieurs travaux futurs. Aucun envoi n’est impliqué par la préparation du dossier.

**Jets : conserver un modèle complet avant toute transplantation.** La chaîne jets, rang, multiplicités, tour et spectre est démontrée dans le cadre fini annoncé. Pour les entiers, les quatre objets correspondants restent à définir indépendamment des zéros. La prudence n’exclut pas la création d’un candidat ; elle impose que le candidat existe avant son interprétation.

## 7. Un pont mathématique interne plausible

Le pont le plus concret concerne **la recherche d’un témoin quadratique dans des espaces de fonctions tests**, plutôt qu’un Bellman appliqué au mot « RH ».

Fixons une forme hermitienne W et une collection finie de fonctions admissibles, avec leurs intervalles de coefficients et un budget. L’état comprend les fonctions sélectionnées, les contraintes, les encadrements et la précision. Une action ajoute une fonction, change une précision ou tente une compression ; le contrat terminal est un signe certifié avec marge strictement supérieure au budget d’erreur. Bellman optimise alors le coût d’obtenir ce certificat dans le modèle fini. La règle de composition et les prérequis doivent être définis et testables. Si aucun candidat ne donne un signe certifiable dans cette classe et ce budget, une issue « aucun certificat obtenu » est obligatoire ; l’optimisation ne peut promettre l’existence du témoin.

Un second cas est l’optimisation des paramètres J,K,M d’un espace de jets. À q fixé et dans un domaine fini, l’objectif est de minimiser D/M sous dimension supérieure au rang majoré. Une programmation dynamique n’est justifiée que si des sous-problèmes avec état suffisant sont réellement isolés ; une simple énumération peut être meilleure. Le choix des paramètres améliore la borne intermédiaire, tandis que la preuve de rang et de multiplicité fournit son contenu arithmétique.

Ces deux usages ne prouvent pas la positivité de W pour ζ. Pour aller plus loin, il faudrait montrer qu’une valeur ou un point fixe conserve l’information arithmétique pertinente, qu’elle n’introduit pas RH dans la transition, et qu’un énoncé uniforme valable hors du modèle fini en découle. Une contraction obtenue en ajoutant un facteur γ<1 n’établit pas ce lien.

## 8. Confrontation constructive et critique

La lecture constructive proposait de valoriser les possibilités ouvertes par une expérience. La critique a rappelé que l’histoire ne révèle pas le résultat des actions non réalisées et que les anciennes probabilités du navigateur sont subjectives. La synthèse conserve les prérequis et remplace l’optimisation supposée de la découverte par celle de livrables déclarés, avec sensibilité des poids et des coûts.

La critique a aussi insisté sur trois gardes appliquées au registre : exposant de croissance Q=2Θ−1 alors que le demi-exposant normalisé vaut Θ−1/2 ; générateur D dépendant d’une branche de logarithme de F ; T* relatif distinct d’une première sortie directe. Les statuts V6.37 et V6.36 restent séparés : 36/36 A1 et 25/8/3 D sont descriptifs, tandis que le certificat DH donne une borne inférieure sous modèle arithmétique explicite.

La relecture critique du registre a confirmé les statuts des épisodes sensibles et l’existence des 61 sources. Elle a fait préciser les prévisions historiques conservées dans le navigateur pour les documents 35 et 36, sans attester leur antériorité indépendante ; la formulation du correctif T* du document 58 et le sens de « caractéristique impaire » au document 59 ont aussi été précisés.

Les deux lectures s’accordent pour avancer par actions courtes, falsifiables et traçables. Bellman donne ici un moyen de montrer ce qui justifie un choix, ce que ses hypothèses promettent et ce qu’un autre choix de préférences changerait. Le mécanisme qui imposerait RH demeure une question mathématique distincte.
