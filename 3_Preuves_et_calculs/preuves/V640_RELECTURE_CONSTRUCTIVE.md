# V6.40 — Relecture constructive : des contraintes exactes aux zéros

## Périmètre et chronologie

Cette relecture porte sur les **12 couples, soit 24 directions**, figés dans
`data/v639_couples_fixes.json`. Elle ne sélectionne aucun couple en fonction
de ses zéros. Le manifeste V6.39 est conservé : son empreinte de contenu est
`1218d67a838989857e0b174f991181019f155c79f7b6c9ef02ab974288d4b9ec`.
Le protocole d'exécution V6.40 a été verrouillé le 12 octobre 2026 à
13:17:04 UTC avant les nouveaux calculs. Les vérifications de reconstruction
ci-dessous n'ont évalué aucune fonction L et n'ont compté aucun zéro.

Les sources inspectées sont `src/relief_direct.py`,
`scripts/run_v637_apparie.py`, `scripts/run_v637_root_crosscheck.py` et
`src/v639_contraintes.py`. Le module neuf `src/v640_racines.py` sépare
reconstruction analytique, localisation EM historique et recoupement
haute précision. Il n'exécute aucune localisation à son chargement.

## Ce qui est acquis avant le comptage

Pour chaque ancre, le support à trois colonnes est celui du manifeste.
Les six caractères sont indexés par $k=1,3,5,7,9,11$, avec générateur 2
modulo 13. Les phases sont reconstruites à partir des sommes de Gauss,
puis du demi-angle principal :

\[
 \epsilon_k=\frac{1}{i\sqrt{13}}
   \sum_{a=1}^{12}\exp\!\left(2\pi i
        \left(\frac{k\log_2 a}{12}+\frac a{13}\right)\right),\qquad
 z_k=\sqrt{\frac{1+\Re\epsilon_k}{2}}
      -i\frac{\Im\epsilon_k}{2\sqrt{(1+\Re\epsilon_k)/2}}.
\]

Le mineur sur le support $(j,k,\ell)$ est
\(w_j=\Im(\bar z_kz_\ell)\),
\(w_k=\Im(\bar z_\ell z_j)\),
\(w_\ell=\Im(\bar z_jz_k)\).
On normalise $u=w/\|w\|$, puis on choisit le signe donnant
\(P_i=\Re(z_i\sum u_j^3\bar z_j)>0\).
Cette règle ne cherche pas un autre support et n'utilise aucun résultat
de zéro. Enfin
\(c_\pm=\cos(r)e_i\pm\sin(r)u\).

Le théorème V6.39 apporte les contraintes **mathématiques exactes** : même
ancre, même distance projective et même premier coefficient complexe.
Il donne également $D(c_-) > D(c_+)$. Le comptage qui suit ajoute une
observation numérique sur ces objets ; il n'améliore pas rétroactivement
la portée du théorème.

## Contrôle indépendant de l'entrée

Une reconstruction ordinaire mpmath, distincte des calculs d'intervalles
V6.39, a comparé les 24 directions à 60 et 90 chiffres de travail.

| Quantité | Maximum observé |
|---|---:|
| Écart d'une coordonnée entre reconstructions 60 et 90 chiffres | $5,37\times10^{-61}$ |
| Écart coordonnée analytique / valeur binary64 exacte | $5,02\times10^{-17}$ |
| Écart du premier coefficient complexe dû aux coordonnées binary64, phases reconstruites | $6,49\times10^{-17}$ |
| Écart de norme carrée dû aux coordonnées binary64 | $1,03\times10^{-16}$ |
| Écart phase historique binary64 / phase reconstruite | $9,31\times10^{-16}$ |

Le module a ensuite reconstruit les 24 directions à 110 chiffres et
vérifié les signes de $P_i$, les supports et les résidus de noyau.
Ces valeurs sont des **observations de précision**, pas des bornes
d'intervalles. Elles distinguent deux sources d'erreur : arrondir les
coordonnées et évaluer les phases en double précision.

Pour la sensibilité, `mp.mpf(float(x))` relève exactement un nombre binaire
stocké ; `mp.mpf(str(float(x)))` relèverait un autre nombre. Le calcul
principal haute précision reconstruit toujours la recette analytique.

## Bord droit et comptages

Le bord $\Re(s)=3$ est choisi avant les zéros par la majoration
\[
 \left|\sum_{n\ge2}a(n)n^{-s}\right|
 \le \sqrt6\,\|c\|_2\,(\zeta(3)-1)
 <\|c\|_2\cos(3/4)\le |a(1)|.
\]
Pour les recettes unitaires, le facteur $\|c\|_2$ vaut 1. Pour les
directions arrondies, il faut contrôler directement la marge normalisée
$|a(1)|/\|c\|_2-\sqrt6(\zeta(3)-1)$ ; la petite erreur d'entrée est
très inférieure à la marge de domination. Cette domination justifie un
bord droit sans zéro. Elle ne justifie pas les bords horizontaux ni
l'absence de zéro sur une autre partie du domaine.

Le protocole utilise les contours $(\Delta t,\Delta\sigma)=
(0,02;0,05)$ et $(0,01;0,025)$, puis des subdivisions adaptatives.
La droite critique est reprise au pas 0,005. L'admissibilité exige la
stabilité des comptages, une marge relative **échantillonnée** de bord
au moins $10^{-10}$, des increments de phase inférieurs à 0,8 et un
résidu d'enroulement inférieur à $10^{-8}$, avec parité et monotonie.
Une marge échantillonnée ne devient pas une borne entre les nœuds.

Le déficit contour moins changements de signe de Hardy constitue une
**détection numérique proposée**. Les changements de signe peuvent
manquer un zéro critique double ou deux zéros simples très rapprochés.
Le raffinement réduit ce problème sans le supprimer logiquement.

## Recoupement de chaque membre détecté

La localisation EM conserve ses multidéparts fixes et explore les deux
signes d'ordonnée. Une combinaison de caractères complexes n'impose pas,
à coefficients fixés, la symétrie $t\mapsto-t$. La symétrie pertinente
de l'équation fonctionnelle est $s\mapsto1-\bar s$.

Chaque membre détecté est ensuite évalué par une seule série de Dirichlet
à coefficients périodiques agrégés, avec phases et coordonnées analytiques
reconstruites. Le recoupement retient :

| Contrôle | 80 chiffres de travail | 110 chiffres de travail |
|---|---:|---:|
| Résidu de la fonction | $<10^{-50}$ | $<10^{-75}$ |
| Résidu du partenaire, ramené par le rapport des facteurs de complétion | $<10^{-45}$ | $<10^{-70}$ |
| Écart avec la localisation EM | $<10^{-7}$ | $<10^{-7}$ |

L'accord entre les deux racines doit être inférieur à $10^{-30}$.
La partie réelle doit satisfaire $0,500001<\Re(s)<3$ et l'ordonnée
rester dans la tranche entière détectée. Une troisième résolution à
80 chiffres, sur les coordonnées binary64 relevées exactement, doit
déplacer la racine de moins de $10^{-9}$ et satisfaire les contrôles
de résidu et de partenaire. Chaque critère était fixé avant les résultats.

Le rapport de facteurs de complétion évite qu'une amplification gamma
à gauche soit prise à tort pour un échec de l'équation fonctionnelle.
Le résidu ainsi ramené reste un résidu numérique ; il ne constitue pas
une estimation certifiée de distance à une racine.

Si une localisation échoue, si le recoupement échoue ou si un comptage
n'est pas admissible, le membre demeure **ambigu**. Il n'est ni supprimé
ni transformé en succès. Chaque direction garde un statut, même sans
détection sous 150. Les six contrôles d'Euler sont des contrôles de
méthode ; ils ne sont pas six observations supplémentaires du contraste.

## Conclusion que les résultats pourront autoriser

Le contraste est descriptif, sur une construction déterministe de douze
couples. La prévision « majorité » porte sur douze, donc demande au
moins sept couples favorables ; on ne change pas ce dénominateur après
avoir observé les cas ambigus. Les égalités, ordres contraires,
non-détections et indéterminations sont publiés. Les quatre rayons d'une
même ancre ne sont pas quatre réplications indépendantes ; les trois
ancres représentent trois classes de conjugaison.

Une racine recoupée dans une tranche confirme numériquement un exemple
hors droite. Elle ne certifie ni une première racine, ni l'absence plus
bas, ni une précision de 80 ou 110 décimales. La formulation autorisée
reste **« première tranche de détection numérique stable et recoupée »**.
L'expérience finie ne démontre aucune implication générale entre $D$
et la hauteur des zéros, aucune causalité, RH ou GRH.

Le progrès concret est de rendre la comparaison plus propre : elle
conserve maintenant le premier coefficient **complexe** exact, au lieu
de seulement rapprocher son module. Après le bilan, la suite pertinente
sera soit un certificat de racine sur un exemple représentatif, soit
une étude de directions supplémentaires dans la même fibre, avec
sélection fixée avant de nouveaux zéros. Le sens de cette suite dépendra
des résultats ; la prévision actuelle doit rester archivée en l'état.

## Complément après exécution : résultats relus

Ce complément est postérieur aux comptages et aux 24 recoupements. Il ne
modifie ni le manifeste ni le protocole. Les 30 directions, six contrôles
compris, satisfont les critères numériques d'admissibilité. Les 24 membres
des couples ont une détection et une racine recoupée. Aucun comptage n'a
changé aux raffinements prévus ; aucun contrôle d'export d'entrée n'a
changé le comptage. Les six directions d'Euler n'ont pas de détection
hors droite sous 150.

Aux trois plafonds 50, 100 et 150, le résultat est le même : **8 couples
avec détection plus précoce pour le D supérieur, 4 avec l'ordre
contraire**, aucune égalité ou indétermination. Les quatre ordres
contraires correspondent aux quatre rayons de l'ancre \(k=1\). Les huit
favorables sont les quatre rayons de \(k=3\) et les quatre rayons de
\(k=5\). La prévision descriptive de majorité est donc observée, mais
la structure par ancre est plus informative que le seul total 8/12.
Le premier coefficient complexe et la distance contrôlés ne rendent
pas le sens du contraste uniforme.

Sur les 24 recoupements, l'écart maximal des racines entre 80 et 110
chiffres de travail est \(2,66\times10^{-80}\), et le déplacement maximal
entre recette analytique et coordonnées binary64 exactement relevées
est \(7,61\times10^{-17}\). Ce sont des diagnostics observés ; ils ne
donnent pas des erreurs certifiées.

### Deux vérifications supplémentaires par une autre formule

Le choix de ces deux vérifications porte sur les covariables : membres
« plus » des ancres \(k=1\) et \(k=5\), au rayon algébrique \(\pi/6\).
Il a été communiqué avant lecture du JSON final des recoupements.
Il s'agit toutefois d'une **relecture supplémentaire postérieure au
protocole**, pas d'une nouvelle prévision.

La reconstruction utilise ici \(z_k=\exp(-i\operatorname{Arg}
\epsilon_k/2)\), puis les trois mineurs, indépendamment du demi-angle
du module principal. La fonction est évaluée par

\[
 F_c(s)=13^{-s}\sum_{k}c_kz_k
       \sum_{a=1}^{12}\chi_k(a)\zeta(s,a/13),
\]

sans appel au module de reconstruction ni à l'agrégation périodique
du recoupement principal. Le solveur est repris à 90 chiffres.
Les deux formules partagent **mpmath et son évaluation Hurwitz** :
c'est un contrôle de formulation et d'entrée, pas un autre backend.

| Direction | \(\Re(s)\), arrondie | \(\Im(s)\), arrondie | Résidu observé | Écart avec le résultat principal à 110 chiffres |
|---|---:|---:|---:|---:|
| k1_rpi_6_plus | 1,228873878901 | 4,807082005639 | \(2,97\times10^{-91}\) | \(7,68\times10^{-91}\) |
| k5_rpi_6_plus | 0,720801817598 | −15,766475725917 | \(1,72\times10^{-90}\) | \(3,44\times10^{-90}\) |

Les résidus des partenaires, ramenés par les facteurs de complétion,
valent respectivement \(1,66\times10^{-90}\) et
\(1,72\times10^{-90}\). Aucune existence de zéro, décimale exacte ou
absence antérieure n'est certifiée par ces deux contrôles.

### Lemmatisation et suite

Les deux lemmes de LEMMES_ET_SUITE_V640.md ont été relus. Le bord
droit se démontre avec les inégalités rationnelles \(5/8<23/32\) ;
sa preuve ne dépend pas de la marge décimale observée. La formule de
vitesse découle correctement du théorème implicite sous l'hypothèse
d'une racine simple. Sur une branche et lorsque \(\sin(r)\ne0\),
\(\partial_r F=-B_i/\sin(r)\), ce qui donne bien
\(s'=B_i/(\sin(r)\partial_sF)\). Cette expression n'impose aucun signe
à la variation de l'ordonnée.

Le suivi de branches dans une ancre contraire et une ancre favorable
constitue une suite explicative cohérente. Il faudra garder les
changements d'identité de branche, les collisions et les échecs de
continuation. Une branche poursuivie numériquement n'est pas un
certificat de simplicité ; le lemme doit conserver son hypothèse.
