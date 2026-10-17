# V6.40 — Exécution prospective des couples V13 à contraintes exactes

Protocole enregistré le 12 octobre 2026 avant toute évaluation de fonction L
ou comptage des zéros pour les 24 directions V6.39. La sélection est conservée
à l'identique dans `v639_couples_fixes.json` : trois ancres k=1,3,5 et quatre
rayons 9/20, 13/20, 3/4, pi/6. Aucun remplacement de couple après résultat.

La prévision V6.39 est conservée : le membre de D plus élevé a une première
détection numérique plus précoce dans une majorité des strates faisables.
Les douze strates sont analytiquement faisables. Le critère principal est donc
une majorité stricte des douze couples fixes, soit au moins sept signes plus
précoces. Un tableau distinct décrit les seuls signes comparables. Les égalités,
non-détections et ambiguïtés restent dans le tableau principal. Si l'incertitude
empêche de décider le seuil, la prévision reste indéterminée. Aucun test de
significativité : les rayons d'une ancre partagent u ; deux ancres partagent le
même support. Ce ne sont pas douze réplications statistiques indépendantes.

## Calcul figé

- Espace impair modulo 13, six coordonnées réelles ; 24 directions, plus les
  six axes d'Euler comme témoins numériques. Plafond 150, bilans 50,100,150.
- Bord droit R=3, bord gauche 1-R=-2. Avant tout comptage, la domination du
  premier terme est obtenue par sqrt(6)(zeta(3)-1)<cos(3/4). Elle concerne la
  série de Dirichlet ; les zéros triviaux sont supprimés par la complétion.
- Grilles de contour (dt,ds)=(0.02,0.05),(0.01,0.025), raffinement horizontal
  adaptatif déjà implémenté ; droite critique dt=0.02,0.01,0.005.
- Observable : première tranche entière où N_contour-N_signes est positif,
  pour |Im(s)|. C'est un déficit numérique, pas une première ordonnée exacte.
  Un zéro critique double ou deux changements de signe trop proches peuvent
  tromper ce calcul. Le recoupement d'une racine ne démontre pas l'absence avant.
- Admissibilité : accord intégral des comptes sur les deux contours et trois
  droites ; déficit non négatif pair ; monotonie des trois comptes ; zéro
  ambiguïté horizontale restante ; incrément de phase<0.8 ; résidu à l'entier
  <1e-8 ; marges relatives de bord échantillonnées>=1e-10. Ces marges ne sont
  pas des bornes sur le contour continu. Tous les axes d'Euler doivent être
  stables sans détection pour valider le contrôle global.
- Reconstruire les recettes analytiques à haute précision, comparer les
  coordonnées binary64 levées exactement, la norme et A ; refaire les comptes
  fins avec les recettes arrondies à partir de 110 chiffres. Toute différence
  de classement est conservée comme ambiguïté d'entrée.

## Recoupement figé

Pour chacun des 24 membres, publier un statut. Pour toute détection admissible,
chercher une racine à droite dans sa tranche avec les départs EM fixés du code
V6.37, restreints au même bord R=3. Un échec n'est pas une absence : statut
ambigu, conservé. Reconstruire la recette exacte et la fonction via
mpmath.dirichlet indépendamment d'Euler–Maclaurin à 80 et 110 chiffres.

Critères de recoupement : Re(s)>0.500001 et<3, même tranche stricte (T-1,T],
résidus <1e-50 à80 chiffres et <1e-75 à110, accord des deux racines<1e-30,
écart avec localisation EM<1e-7. Pour la racine partenaire 1-conj(s), le résidu
non complété est ramené à la même échelle par le quotient des facteurs Gamma ;
seuils 1e-45/1e-70. Reprendre aussi les coordonnées binary64 exactes et exiger
un déplacement<1e-9. Ces seuils sont des contrôles numériques, pas des bornes
certifiées d'erreur ni des disques d'isolement de racines.

Un signe entre deux tranches détectées est plus précoce, plus tardif ou égal.
Si un seul membre détecte sous le plafond et l'autre est admissible sans
détection, l'ordre vaut uniquement pour l'observable tronqué ; marquer la
censure. Deux non-détections n'établissent aucun ordre. Une entrée non
admissible ou un recoupement échoué rend le couple indéterminé.

Publier les échecs de prévision. Aucun changement de support, rayon, plafond,
seuil ou définition après connaissance des résultats. Toute réparation de code
sera datée comme telle, conservera les sorties initiales et sera explicitée.

L'expérience n'implique ni causalité du défaut D, ni RH/GRH, ni absence globale.
