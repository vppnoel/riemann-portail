# V6.41 — Fibres, paires de racines et plis : protocole avant nouveaux calculs

Date : 12 octobre 2026. Le protocole utilise les résultats V6.40 comme points
de départ connus. Il est prospectif pour les nouvelles continuations, collisions,
sections de jets et moments de contour ; il n'efface pas cette sélection informée.

## Questions et critères avant calcul

1. Suivre une paire sans prétendre lui donner des étiquettes invariantes :
   centre et discriminant calculés par moments de contour, sous l'hypothèse de
   deux racines dans le contour. Le passage individuel par un zéro double reste
   ambigu à permutation près ; la paire peut rester bien définie.
2. Chercher les collisions critiques simples des quatre familles exactes
   (ancres 1 et 5, signes plus/minus). La normale locale exige Z=Z_t=0 et
   Z_r Z_tt non nul. Conserver les dégénérescences et échecs, sans les renommer
   collisions simples. Distinguer discriminant exact et son approximation linéaire.
3. Démontrer le domaine exact des A sous les contraintes de norme, ancre et
   rayon : une ellipse fermée, avec fibre S² intérieure, singleton au bord,
   vide dehors. Ne pas présupposer que D varie sur toute fibre.
4. Identifier un contrat de passage à la positivité globale : domaine admissible,
   densité, continuité, compatibilité et contrôle uniforme de tous les modes.
   Aucun ensemble fini de matrices positives ne doit être appelé preuve de RH.

## Sélection des branches connue avant V6.41

Six départs, tous extraits des données V6.40, sans nouvelle localisation :
- χ1, plus, rayon pi/6 ; χ1, minus, rayon pi/6 ;
- χ5, plus, rayon pi/6 ; χ5, minus, rayon pi/6 ;
- χ1, minus, rayon 3/4 (autre racine détectée, hauteur positive) ;
- χ5, plus, rayon 9/20 (autre racine détectée, hauteur positive).

Deux grilles de continuation EM, r=j/200 et j/400, de 0 à 3/4, comprenant
aussi pi/6. Reprise depuis chaque départ vers les deux extrémités. Prédicteur
par vitesse locale puis correction ; résidu normalisé<1e-8 et déplacement
maximal 0,2 par pas. La distance à la droite<0,02 ou une correction devenue
critique déclenche un arrêt et une recherche de pli, pas une poursuite avec
étiquettes réputées uniques. Les pertes de branches, sorties de domaine et
incohérences de grilles sont toutes publiées.

Le domaine de suivi est |Im(s)|<=25 et −2<=Re(s)<=3 ; R=3 conserve la preuve
de domination V6.40 pour ces familles et ces rayons. Le suivi n'est pas une
preuve d'absence d'autres branches. Les tranches antérieures restent numériques.

## Recherche et reprise des collisions

Scanner W(t)=X_i(t)Y'(t)−X_i'(t)Y(t) sur [-25,25] à pas 0,01 et 0,005,
avec dérivées EM centrées et racines par changements de signe. En déduire
tan(r)=−X_i/(eta Y), puis garder les rayons 0<r<3/4. Vérifier directement
Z,Z_t ; chercher les cas de dénominateur nul plutôt que les ignorer. Les
changements de signe ne capturent pas nécessairement tous les zéros de W :
aucune exhaustivité du scanner n'est revendiquée.

Reprendre chaque candidat retenu à 40 puis 70 chiffres, par W et par les
équations Z,Z_t. Résidus<1e-25/1e-50, accord (r,t)<1e-20. Transversalité
numériquement séparée de zéro : |Z_r| et |Z_tt|>1e-12 à l'échelle Hardy.
Attribuer une collision à un suivi seulement si |t−t_arrêt|<0,5 et
|r−r_arrêt|<0,05. Un échec d'attribution reste ouvert.

L'évaluateur MP emploie les premières dérivées de Dirichlet et une formule
Hurwitz pour les secondes. Il n'appelle jamais dirichlet(derivative=2) : la
version1.3.0 ne fournit pas cette seconde dérivée. Vérifier la seconde dérivée
par une autre formule sur des points fixés, avant les nouvelles localisations.

## Bloc de deux racines au voisinage d'un pli retenu

Pour les six suivis, si une collision est attribuée et non dégénérée, tester
les paramètres r*−1e-4, r*, r*+1e-4. Utiliser w=−i(s−1/2), un cercle de
rayon0,2 centré en t*, et 128/256 noeuds. Moments m0,m1,m2 par F'/F ; dérivée
EM à cinq points, pas1e-3/5e-4. Exiger |m0−2|<1e-5, accord des moments
m1,m2<1e-6, marge relative échantillonnée>1e-8 et petites parties imaginaires
compatibles avec la symétrie. Si ces critères échouent, aucun bloc de deux
racines n'est admis pour ce cas. Conserver les sorties initiales.

Discriminant Δ=2m2−m1² ; compagnon [[m1/2,1],[Δ/4,m1/2]]. Δ positif donne
deux racines critiques, Δ négatif une paire hors droite, sous les hypothèses
du bloc. Recouper les deux racines de part et d'autre à40/70 chiffres ;
résidus<1e-25/1e-50 et accord<1e-20. Comparer Δ/4 à la pente du jet
−2Z_r/Z_tt·(r−r*), sans transformer cette approximation en identité globale.

## Géométrie et sections de jets fixées

Étudier les ellipses pour ancres1,3,5 et rayons9/20, pi/6,13/20,3/4.
Exemples radiaux eta=0,1/4,81/100,1,121/100 aux deux axes principaux :
intérieur, bord et extérieur doivent être conservés. Contrôler aussi A=0
au rayon13/20, où le score D vaut1 si la fibre est faisable.

Aux hauteurs5,10,15,20, ancre1,3,5 et rayonpi/6, empiler les contraintes
(ancre, ReA, ImA, Z, Z_t). Tester A au centre et deux déplacements radiaux
eta=1/4 et1 sur le premier axe. Si rang5, le nombre de directions candidates
est2/1/0 selon leur norme minimale ; vérifier les résidus et Z_tt. Un rang
non résolu reste explicitement tel. Cela ne localise pas des zéros de ζ.

## Positivité et graphes

Les Gram de contraintes sont positifs automatiquement. Ils ne sont pas la
forme de Weil. Prouver séparément : (a) le lemme de densité/continuité qui
permettrait le passage de toutes les compressions compatibles au global ;
(b) un contreexemple exact montrant que toute liste finie de préfixes positifs
peut manquer une direction négative ; (c) un critère suffisant par complément
de Schur avec budget de couplage. Les hypothèses encore absentes pour ζ sont
affichées dans le graphe, avec liens démontrés, numériques et conjecturaux distincts.

Une voie fermée sous hypothèses précises est un résultat. Cela ne démontre
pas l'inexistence de toute voie vers RH. Aucun succès de continuation, pli,
certificat global, causalité ou nouveauté bibliographique n'est promis.
