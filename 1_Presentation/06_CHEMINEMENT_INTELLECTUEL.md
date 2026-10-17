# D'où viennent les intuitions : le cheminement intellectuel du programme Riemann

**Date :** 10 octobre 2026
**Statut :** récit reconstruit à partir du corpus (README, indicateur, documents 14 à 49 ; mis à jour en V6.24, 11 octobre 2026) ; ce n'est pas une interview. Ce qui est démontré, mesuré et supposé est séparé au §15.

*Mis à jour en V6.18, 10 octobre 2026 ; version d'origine : document 06 antérieur à la V6 (13 étapes, de Nyman–Beurling [Nym50] [Beu55] aux archives physiques).*

## 0. Comment lire ce document

- Chaque étape donne : l'intuition, ce qui l'a testée (avec le fichier ou le chiffre) et ce qui en reste.
- Les origines sont celles écrites dans le corpus : documents, analogies explicitement listées, demandes de l'auteur citées dans le README. Quand le corpus ne dit pas d'où vient une idée, c'est marqué « à préciser par l'auteur » : ce document ne devine pas la pensée de l'auteur.
- Les verdicts reposent sur des tables lues, pas sur l'impression qu'un calcul « marche ». Depuis la V6.14, une partie des tests est précédée de prévisions écrites et horodatées avant le calcul ; leur sort est donné, y compris quand elles sont fausses.
- Une fois pour toutes : **aucune preuve de RH n'est revendiquée.** Les deux énoncés démontrés (Théorèmes A et B) ont été pré-relus en interne, pas encore par un spécialiste. Le reste se lit pour ce qu'il est : des identités, des mesures, des lectures.

## 1. Avant la V6 : treize étapes

Le premier récit comptait treize étapes. Quatre résultats propres étaient conservés (5, 6, 7 et 10), plus un cadre emprunté à la littérature (1) ; les autres étaient des outils, des diagnostics ou des pistes arrêtées. Ce tableau reste juste ; seule la dernière colonne a été complétée par ce que la V6 en a fait.

| # | L'intuition | D'où elle vient | Ce qui l'a testée | Ce qui en reste |
|---|---|---|---|---|
| 1 | RH se traduit en un problème d'approximation dans un espace de Hilbert. | Littérature : critère de Nyman–Beurling, renforcé par Báez-Duarte [Bae05] [Bae03]. | Matrice de Gram exacte : G(1,1) = log 2π − γ à 10^−14^ ; d~N~²·log N entre 1,005 κ et 1,042 κ pour N = 40…100. | Cadre. En V5, la projection de Nyman–Beurling se ramène exactement à Q : branche close. |
| 2 | Encoder l'approximation dans un opérateur positif et chercher une condition d'observabilité. | Langage du contrôle et des problèmes inverses (Tikhonov, Krylov). | Aucun gain analytique mesurable. | Langage. Krylov revient en V6.9 comme outil de reconstruction. |
| 3 | Approcher 1/ζ par des polynômes de Dirichlet Möbius. | Littérature (Bettin–Conrey [Con89]–Farmer [BCF13]). | E(V~N~)·log N passe de 2,11 à 0,71 (N = 5 → 200), encore loin de l'asymptotique. | Outil. |
| 4 | Les progrès récents sur Möbius (sommes de type I/II) contrôlent les erreurs. | Littérature récente (intervalles courts). | Aucun gain d'exposant annoncé ni obtenu. | Suspendu. |
| 5 | Une fenêtre bien choisie annule le biais lié à s = 1. | Calcul exploratoire. | G est régulière en s = 1 ; c n'a de support que sur les entiers à au plus deux facteurs premiers distincts. | Conservé : l'objet propre du projet. |
| 6 | La croissance de la somme de carrés Q mesure la distance du zéro le plus à droite. | Analogie avec les critères classiques (ψ(x) − x ≪ x^1/2+ε^), ici avec un pôle double. | Théorème A (preuve) ; Théorème B sous RH ; Q mesurée contre 300 zéros à environ 5 %. | Théorème A : RH équivaut à Q(X) = X^o(1)^. Théorème B : sous RH, Q(X) ∼ (4κ/3)·log³X. Pré-relus en V6.13. |
| 7 | c se factorise : c = 1∗a, a(n) = μ(n)(log²n − 2γ log n). | Dérivation de 1/ζ. | Tests d'identité. | Conservé. |
| 8 | Réduire la queue critique à des sommes exponentielles de Möbius. | Méthodes classiques. | Se ramène à de la cancellation de type Mertens en √X. | Diagnostic. |
| 9 | Traiter chaque échelle comme une mesure bruitée : filtre de Kalman (« GPS analytique ») et trajectoire de référence (« Apollo »). | Navigation et estimation. À préciser par l'auteur : d'où vient ce choix d'analogie. | Information par log X sans loi ; rapport Q / référence de 0,34 à 0,64. | Rétrogradé en V4.3, relu en V6.12 : le Kalman devient la récurrence de Levinson (§7). |
| 10 | Chaque canal arithmétique a une destination exacte H~∞~(q) ; la formule explicite doit reproduire Q. | Calcul de séries de Dirichlet. | Preuve courte ; formule explicite à 300 zéros : accord à environ 5 %. | Conservé. En V6.0, côté premiers = côté zéros à 5·10^−9^. |
| 11 | Avant d'investir, tester le cadre contre trois témoins. | Pratique de la preuve de rejet. | Davenport–Heilbronn [DH36b] [DH36a] (DH) : pente 0,56 contre 0,33 pour ζ ; Weil : aucune positivité ; densité : grandes valeurs. | Arrêt de l'attaque directe. DH devient le témoin permanent du programme. |
| 12 | Les zéros sont des sources cachées que les nombres premiers « captent » ; un zéro hors ligne est un mode à gain positif, comme un flux à travers une surface cellulaire. | Analogie listée avec la localisation de sources de potentiels évoqués. À préciser par l'auteur. | Biais de la partie réelle ; mode fantôme sur DH (Im ≈ 73,8). | Rétrogradé en V4.3, relu en V6.12 : le fantôme ne pèse rien (§7). |
| 13 | Le diagramme masse-rayon et l'amplitude de Remmen relieraient RH à la physique. | Archives reçues. | Recalcul des constantes : erreurs de pente, d'axes, de placement ; Remmen écrit lui-même « sans prouver » RH. | Aucun lien établi. |

Le fil qui revenait déjà : **la valeur ½ est-elle imposée, ou émerge-t-elle d'une contrainte ?** Seuil de croissance de Q (Théorème A), absence de « création interne » d'un flux quand l'opérateur est auto-adjoint (étape 12), symétrie ζ(s) ↔ ζ(1−s). Lien proposé, à confirmer par l'auteur : le même thème dans le projet GPF Atlas (dérivée d'ordre ½ qui émerge de l'équation de la chaleur).

La leçon de cette période tient en une règle : plusieurs erreurs (E01 signe inversé, E03–E04 réponse injectée dans le test, E05 mode fantôme pris pour un zéro, E09 ajustements libres instables, E14–E15 physique mal recalculée) ont d'abord été écrites comme des résultats. **Lire les tables avant de conclure.** Le banc d'audit (`2_Methode/Banc_d_audit`) en garde la trace ; il compte aujourd'hui 21 erreurs plantées.

## 2. La bascule V6 : cartographier des mécanismes

**L'intuition.** À la clôture de la V5.8, un constat : accumuler des reformulations équivalentes de RH, ou des énergies positives par construction, ne fait pas avancer. Il faut une structure qui porte une information arithmétique discriminante. D'où un changement de question (document 14) : non plus « cette idée prouve-t-elle RH ? », mais **« quel mécanisme cette idée révèle-t-elle, que conserve-t-elle, que détruit-elle, avec quoi se recombine-t-elle ? »** La règle : divergence conceptuelle forte, validation mathématique stricte. Une métaphore n'a de valeur que si elle conduit à un objet exact, un observable, un témoin négatif et une règle d'arrêt.

**Ce qui l'a testée.** Les instruments TOMO, PRIME-LOCK, DUAL-LOCK (documents 15 à 21), puis leur audit (22, 23) et leur classement (24, V6.3d) : tous voient les zéros, aucun ne voit plus. Le verrou local et le signe global sont indépendants (quatre coins). Le test prioritaire de l'Atlas des métaphores (V6.4, document 26) : le seuil τ~c~ existe, mais ce n'est pas un invariant ; il mesure le pouvoir de résolution de la fenêtre.

**Ce qui en reste.** La méthode : nommer, croiser, imposer des témoins. Et une question posée par l'auteur en V6.5, qui devient le fil de tout ce qui suit : **RH n'existe-t-elle que parce qu'elle est nécessaire à quelque chose de plus grand ?** Premier test : la famille F~θ~ = (1 − θ)·L(s, χ₃ mod 7) + θ·f~7~, qui garde l'équation fonctionnelle et n'a de produit d'Euler qu'en θ = 0 (document 27). Les 958 zéros jusqu'à t = 1000 ne restent sur la droite que pour θ entre −0,0096 et +0,072 ; la plage se referme avec la hauteur. Chaque sortie est une rencontre de deux zéros voisins. Même la partie démontrée (aucun zéro à droite de Re s = 1) disparaît hors du point d'Euler. La symétrie seule ne rend pas RH nécessaire.

## 3. Le Modèle réduit et la nécessité démontrée (V6.6–V6.7)

**L'intuition.** Si l'on veut savoir à quoi ressemble « ce qui rend RH nécessaire », il faut le regarder là où RH est un théorème : les courbes sur les corps finis, Weil (1948) [Wei48]. On mesure la nécessité là où elle est démontrée, pour savoir quoi chercher du côté de ζ. C'est le **Modèle réduit**.

**Ce qui l'a testée (V6.6, document 28).** 425 courbes hyperelliptiques de genre 1 à 8 sur F~3~, F~5~, F~7~ : fonction zêta reconstruite depuis les comptages de points (425 sur 425), positivité de Castelnuovo [MT58] exacte jusqu'à l'étage 60. En face, **le Faux jumeau entier** : 220 polynômes qui ont l'équation fonctionnelle et un produit d'Euler à comptages entiers positifs, mais RH fausse. Aucun n'est une courbe ; la positivité de Castelnuovo les démasque à un étage fini (2 à 5 en genre 2). Le produit d'Euler positif seul ne leur donne que « aucun zéro sur Re s = 1 ». **La Positivité saturée** : la marge s'annule en montant dans la Tour, exactement pour y² = x⁵ + x³ + 1 sur F~3~ à l'étage 4.

**Ce qui en reste.** La signature d'une nécessité démontrée, en quatre traits : (1) équation fonctionnelle et produit d'Euler ne suffisent pas ; (2) une positivité indexée par une tour démasque les faux à un étage fini ; (3) cette positivité tient sans marge, parfois exactement ; (4) elle vient d'un objet d'un étage au-dessus, la surface C × C. **ζ présente les trois premiers traits ; il lui manque l'objet.** Une question divergente en sort : quel est l'« étage n » de ζ ?

**V6.7 (document 29) : deux marges.** Le programme vient d'une réponse reçue par l'auteur : quelle est la marge de stabilité de la positivité de Weil [Wei52] ? Sur 525 courbes, la **marge de la forme** est exactement nulle dès que la fenêtre dépasse le nombre de zéros (2g) ; à la fenêtre 2g, le nombre de directions négatives compte exactement les zéros hors droite (220 faux jumeaux sur 220). La **marge de l'objet** est en général positive, fixée par la paire de zéros la plus serrée ; elle est nulle pour les courbes à zéros confondus, où RH reste un théorème. En interpolant de L(s, χ₅) à DH, exactement quatre paires quittent la droite : ce sont les quatre paires hors droite de DH. Un correctif au document 26 en est sorti. Ce qui reste est une phrase : **la nécessité n'éloigne pas du bord, elle interdit le passage.**

## 4. L'Archipel d'Euler (V6.8)

**L'intuition.** Parmi les fonctions qui ont la même équation fonctionnelle, une sortie de RH peut-elle garder un produit d'Euler ? Si la nécessité est réelle, RH et le produit d'Euler devraient être solidaires.

**Ce qui l'a testée (document 30).** Les espaces V~q~ (q premier ≤ 13) : combinaisons réelles des L(s, χ) à la même équation fonctionnelle. Une rigidité au premier ordre, prouvée : aucune direction qui garde l'équation fonctionnelle ne garde le produit d'Euler. Avec Saias–Weingartner [SW09] (2009) : dans V~q~, toute fonction sans zéro dans Re s > 1 est un point d'Euler. Mesuré : autour de chacun des 27 points d'Euler, une île dont le rayon décroît avec la hauteur (médiane 0,091 à |t| ≤ 25, 0,008 à |t| ≤ 300) ; on en sort par la paire la plus serrée (112 sorties sur 116).

**Ce qui en reste.** **En degré 1, RH implique le produit d'Euler** (démontré). La pré-relecture (V6.13) a montré que ce corollaire était déjà publié ; la carte des îles, elle, est mesurée ici. Et une réponse partielle à la question de l'étage : **la hauteur T joue le rôle de l'étage de la tour.** Le degré 2 est posé comme question.

## 5. Le chaînon et le générateur des premiers (V6.9–V6.11)

**L'intuition (V6.9).** Les mots de l'auteur : « il manque un opérateur symbolique entre la version discrète/réduite et la version continue/complète ». Dans le Modèle réduit, F = q^D^ : les zéros sont le spectre d'un générateur D, et le pas discret est l'exponentielle d'un générateur, comme dans le calcul symbolique (E = e^hD^).

**Ce qui l'a testée (document 32).** L'opérateur se reconstruit depuis les seuls comptages (749 objets). Pour les 524 vraies courbes : valeurs propres à 10^−13^, opérateur unitaire, métrique positive. Pour les 220 faux jumeaux : opérateur et symétrie reconstruits aussi bien, mais métrique jamais positive. Le spectre des longueurs se lit dans les zéros : pics aux log p^k^ pour ζ ; pour DH, 45,6 % du signal aux longueurs composites, l'absence de produit d'Euler lue dans les seuls zéros.

**Ce qui en reste.** **Ce qui manque pour ζ n'est pas l'opérateur, c'est la métrique.** L'objet cherché a désormais une place : il doit porter la métrique.

**Le générateur des premiers (V6.10, document 33).** Même construction, cette fois pour ζ, avec les seuls nombres premiers via la formule explicite. Avec les premiers ≤ 439 : 226 zéros de ζ, 334 de L(s, χ₅), 330 de DH, aucune fausse détection, chaque valeur propre de masse 1 (zéro simple). Avec les premiers ≤ 23 862 : 284 zéros de ζ. La métrique se lit aussi depuis les premiers : positive pour ζ et L ; pour DH, deux directions négatives par quadruplet hors droite.

**La base comme pas de temps (V6.11, document 35).** Dans le Modèle réduit, D est intrinsèque (525 courbes) et la métrique survit au changement de base. Pour ζ, à nombres premiers fixés, un pas grossier noie la métrique de DH : **le seul pas qui convienne à ζ est le flot.**

## 6. L'indicateur et le navigateur

**L'intuition.** Deux outils. En V6.8.1, mesurer l'avancement sur une échelle inspirée des niveaux de maturité technologique. En V6.10, une demande de l'auteur : « repenser la démonstration comme un itinéraire (GPS), les métaphores comme opérateurs symboliques, l'indicateur comme but ». On retrouve là, transformée, l'analogie de navigation de l'étape 9.

**Ce qui l'a testée.** L'indicateur (document 31) : six dimensions, de 0 à 9 (voir, comprendre, situer, étendre au degré 2, démontrer et faire relire, la case vide), puis une septième, « Croiser », en V6.16. Il a dû être corrigé dès son premier instantané : l'histoire complète montrait des niveaux plus hauts que ceux publiés. Le navigateur (document 34) : position = l'indicateur ; opérateurs = les métaphores du registre (69 en V6.10, 87 en V6.17), chacune avec sa garde ; coups avec thèse, témoin contraire, réfutation, gain et coût ; score = (valeur + explicatif) / coût. En V6.11, il a reçu une distance au but (le chaînon) et le **pré-enregistrement des prévisions**.

**Ce qui en reste.** Les métaphores ne sont plus des images : ce sont des noms d'opérateurs, avec leur domaine de validité et leur limite (document 20). Le niveau 7 (relecture extérieure) n'a jamais été atteint, et l'indicateur le dit. Le pré-enregistrement a changé la façon de travailler : depuis la V6.14, presque chaque coup commence par une prévision horodatée.

## 7. Les idées rejetées relues (V6.12)

**L'intuition.** La demande de l'auteur : voir si les trois idées rejetées en V4.3 « ne peuvent pas être relues symboliquement au regard du dictionnaire des idées ». Une idée rejetée l'a été avec les outils de son époque ; les opérateurs du chaînon sont plus fins.

**Ce qui l'a testée (document 36).**

| Idée rejetée en V4.3 | Relue avec le chaînon | Ce qui en reste |
|---|---|---|
| Le Kalman (« GPS analytique ») | Sur les traces des premiers, le rôle du filtre de Kalman (1960) [Kal60] est tenu par la récurrence de Levinson (1947) [Lev47], qui calcule les innovations du prédicteur linéaire. Innovations positives pour ζ et L ; pour DH, première innovation négative avec les premiers ≤ 36. | Un détecteur réel. Les seuils par quadruplet seront corrigés en V6.14. |
| Les sources cachées | Le mode fantôme de V4.3 (Im ≈ 73,8) porte une masse de 1,3·10^−9^ ; le vrai zéro hors droite, 1. | Le fantôme ne pèse rien : le rejet était juste, la raison est maintenant mesurée. |
| Le Schrödinger | L'opérateur existe sans zéro injecté ; le Théorème A se lit au rayon spectral (DH : 0,308517 ; ζ et L : < 10^−6^). | Le verrou « métrique positive ⟺ RH » reste, mais situé. |

**Ce qui en reste.** Le « GPS » de la première heure n'était pas une mauvaise intuition, c'était une intuition sans instrument. Les priorités ont été refaites : la loi de seuil d'abord.

## 8. La pré-relecture (V6.13)

**L'intuition.** Avant d'envoyer quoi que ce soit, se relire soi-même comme le ferait un relecteur hostile, en parallèle et de façon indépendante.

**Ce qui l'a testée (document 37).** Trois relectures : Théorème A, Théorème B, note sur l'Archipel. Chacune a refait la preuve pas à pas, avec contrôles numériques et recherche d'antériorité. A et B : corrects, quelques retouches ; A est une méthode standard, B une transposition du théorème de Cramér [Cra22] au pôle double. L'Archipel : correct sur le fond, une phrase fausse corrigée ; le corollaire n'est pas nouveau (Saias–Weingartner ; Booker–Thorne [BT14] en degré 2).

**Ce qui en reste.** Un corollaire nouveau, **B′** : sous RH, Q(X)/(log X)³ → 4κ/3 si et seulement si tous les zéros sont simples. C'est le premier croisement entre RH et la simplicité des zéros produit par le programme. Un dossier en anglais prêt à envoyer. Et une ligne tenue : **une relecture interne n'est pas une relecture** ; aucun niveau de l'indicateur ne bouge.

## 9. Le temps de Heisenberg (V6.14)

**L'intuition.** Si les premiers « entendent » un quadruplet hors droite, il doit exister une loi qui dit à partir de quand. La loi a été trouvée sur le fond de L(s, χ₅) : la fenêtre critique suit la hauteur du quadruplet.

**Ce qui l'a testée (document 38).** Quatre prévisions écrites avant les tests (horodatées 00 h 29 UTC) :

| Prévision | Résultat | Verdict |
|---|---|---|
| P1 : pour ζ, L~c~ ≈ log(γ~0~/2π) à ±15 % | rapport 1,03 à 1,08 | tenue |
| P2 : L~c~ ne dépend pas du pas h | 4,15 ; 4,20 ; 4,32 | tenue |
| P3 : L~c~ dépend peu de la largeur | 4,25 ; 4,20 ; 4,12 | tenue |
| P4 : un quadruplet qui remplace un zéro du fond est détecté vers 0,8–0,85 L~H~ | 0,82 à 0,99 | réfutée |

Et une correction de la V6.12 : le signe d'une innovation de Levinson n'est pas fiable dès que la métrique est mal conditionnée (**le Signe fragile**). Les seuils par quadruplet de la V6.12 (2,71 ; 3,30 ; 2,78 ; 2,76) étaient du bruit. La détection principale de DH (premiers ≤ 36) et l'absence d'alarme pour ζ et L tiennent.

**Ce qui en reste.** **La loi de seuil** : un quadruplet hors droite à la hauteur γ~0~ s'entend au **temps de Heisenberg** log(q·γ~0~/2π), c'est-à-dire avec les premiers jusqu'au conducteur analytique (rapport 0,95–1,08 pour ζ et L, 0,80–0,89 pour DH). Un lemme d'inertie exact. Et l'expérience d'une correction de sa propre version précédente, faite le jour même.

## 10. Le degré 2 (V6.15)

**L'intuition.** Tout ce qui précède est en degré 1. Une loi qui ne survit pas au degré 2 dirait quelque chose de ζ seule, pas du mécanisme. Le candidat naturel : L(Δ, s), la fonction de Ramanujan [Ram16], où la RH locale est un théorème, Deligne (1974) [Del74].

**Ce qui l'a testée (document 39).** Six prévisions écrites avant tout calcul (06 h 26 UTC). L(Δ, s) reconstruite depuis les seuls τ(n), zéros à 1,2·10^−9^ de ceux calculés sans les premiers. P1 et P2 tenues : la loi de seuil double, L~c~(Δ)/L~c~(ζ) = 1,91–2,07. P5 tenue (aucune direction négative pour L(s, χ₅)). P4 et P6 tenues à une exception près. P3 (« exactement 30 directions négatives » pour DH) **fausse dans sa lettre** : on en trouve 50, parce que la fenêtre voit aussi les zéros plus hauts que la cible. Le **recensement** : 25 quadruplets hors droite de DH jusqu'à 1 464, tous identifiés ; aucune direction négative pour ζ ni L.

**Ce qui en reste.** La longueur d'écoute est le **poids archimédien** Ω(γ~0~), 2π fois la densité des zéros. L'indicateur « degré 2 » passe de 2 à 3. Et un indice non pré-enregistré, noté comme tel : le produit ζ·L(s, χ₅) s'allume plus tôt, comme DH. Deux familles de zéros sans répulsion mutuelle.

## 11. La Rencontre à trois et les croisements (V6.16)

**L'intuition.** Une phrase de l'auteur : « Ce qui m'étonne, c'est qu'il n'y a pas de croisement entre les 3 aussi difficiles que RH. » Les trois sont RH, la simplicité des zéros et leur répulsion. Depuis la V6.5, chaque sortie de la droite passe par une rencontre de deux zéros : si la rencontre est le passage, la répulsion devrait se lire sur la même quantité que RH.

**Ce qui l'a testée (document 40).** Une identité élémentaire : à la fenêtre de Heisenberg, la marge locale de la métrique pour une paire de zéros d'écart normalisé s vaut **1 − sinc²(πs)**, la corrélation de paires de Montgomery (1973) [Mon73], nulle à la rencontre, négative hors de la droite. Cinq prévisions (10 h 54 UTC), dont trois fausses dans leur lettre. Sur 1 070 zéros de ζ : 4 marges sous 0,1, contre 13 pour le GUE et 320 pour Poisson. La répulsion est nette, mais trois fois plus forte que le GUE prévu : P1 tenue qualitativement, fausse quantitativement. P2 et P3 supposaient que β, le coefficient de Q, lisait les paires serrées : faux, β est lisse à 95 % ; c'est sa **part d'écart** qui les compte. P4 (Σβ = 0,540 ± 0,005) tenue. P5 à moitié : la paire de Lehmer (1956) [Leh56] a bien une marge de 0,006, mais elle pèse 39 à 43 fois la médiane dans β, pas cent ; c'est dans la part d'écart qu'elle pèse environ mille fois.

**Ce qui en reste.** **RH, simplicité et répulsion se lisent sur la même quantité** : la marge de la métrique. Le croisement entre dans l'indicateur comme septième dimension, « Croiser », comptée rétroactivement (V6.5 : 4 ; V6.7 : 5 ; V6.13 : 6), avec une carte des croisements et ses zones d'ombre. Le navigateur reçoit la règle du pendant : tout croisement trouvé pour ζ doit être cherché dans le Modèle réduit.

## 12. La Rencontre en degré 2 et la Loi de la marge (V6.17)

**L'intuition.** Deux coups en tête du navigateur : la Rencontre en degré 2, et son pendant dans le Modèle réduit. Si la répulsion est une signature de l'objet, elle doit apparaître pour Δ, et la même loi doit être un théorème là où RH en est un.

**Ce qui l'a testée (document 41).** D'abord un instrument : **le Contour tourné**, une rotation du contour de Mellin repliée par la modularité, qui supprime l'annulation exponentielle. 2 139 zéros de L(Δ, s) jusqu'à 1 500, en double précision (accord 10^−13^ avec mpmath, complétude de Turing (1953) [Tur53]). Il a corrigé au passage la V6.15 : 196 zéros jusqu'à 232,08, et non 189. Puis cinq prévisions (11 h 55 UTC) :

| Prévision | Verdict |
|---|---|
| P1 : zéros de Δ au moins 10 fois sous Poisson | tenue (8 marges sous 0,1, contre 26 pour le GUE et 641 pour Poisson) |
| P2 : le déficit par rapport au GUE est plus faible pour Δ que pour ζ | fausse au seuil 0,1 (0,31 pour les deux) ; le déficit ne dépend pas que de la densité |
| P3 : ζ·L(χ5) : 14 à 20 % de marges sous 0,1, au moins 90 % de paires mixtes, aucune collision | tenue (15,3 % ; 100 % de paires mixtes) |
| P4 : aux premiers de Δ, marges selon Sato–Tate | tenue (Kolmogorov–Smirnov p = 0,86 ; marge minimale 0,026) |
| P5 : Modèle réduit, Sato–Tate ; à l'étage 2, collisions = courbes supersingulières ; proportion décroissante avec p | tenue, sauf la décroissance : fausse |

**Ce qui en reste.** Trois identités : à la fenêtre N, la marge totale de la métrique est la densité de Weyl [Wey39] de U(N) ; la marge d'une paire est la corrélation de paires du CUE(N) ; pour une paire conjuguée, marge = sin²θ = (π/2) × densité de Sato–Tate. Aux premiers de Δ, la marge de la paire (α~p~, β~p~) réunit trois choses démontrées : positivité (Deligne), non-collision, Sato–Tate, démontré par Barnet-Lamb, Geraghty, Harris et Taylor (2011) [BGHT11]. Dans le Modèle réduit, sur 561 258 courbes, Sato–Tate ; à l'étage 2, les collisions tombent exactement sur les 18 338 courbes supersingulières, et RH y reste vraie. Une collision n'est donc pas une sortie.

De tout cela sort un énoncé, nommé **la Loi de la marge** : dans tous les cas où une loi est démontrée (Weyl, Sato–Tate, Dyson (1962) [Dys62]), la fréquence d'une configuration est proportionnelle à la marge qu'elle laisse à la métrique. Pour les zéros de ζ et de Δ, elle est mesurée, avec un déficit à basse hauteur. Sa limite est déjà connue : pour les familles symplectiques (genre ≥ 2), la densité de USp(2g) n'est plus le déterminant de la métrique de taille 2g. D'où le coup suivant, la Loi de la marge en genre 2, et une prévision chiffrée pour tester si le déficit de Δ est un effet de hauteur finie : la constante Λ~Δ~ de la formule de Bogomolny–Keating [BBLM06] devrait tomber entre 2,8 et 5,1. L'indicateur « degré 2 » passe de 3 à 4.

## 12 bis. Les sources et le plan (V6.18–V6.19)

L'auteur demande où sont les sources et où elles sont citées. Le registre (doc. 42) en fait une fiche par article, avec sa couleur d'intérêt et son état de vérification. Les nouvelles lectures montrent des figures déjà connues du corpus, mais avec un axe de plus. La première est calculée tout de suite : la marge d'un groupe de n zéros est leur corrélation à n points, et les triplets de ζ suivent le noyau sinus (doc. 43). Le plan de recherche garde la méthode symbolique → opérateur → fonctions → identification. La matrice des théories (doc. 44) situe chaque théorie par rapport à RH.

## 12 ter. Le palier recalculé et les redécouvertes (V6.20)

L'auteur demande de refaire le calcul du « 4/3 » pour voir s'il n'est pas légèrement différent. Il l'est : 0,985 × 4/3 en médiane jusqu'à 5·10⁶, par compensation de trois facteurs, avec des pics là où une somme de Möbius s'annule. Au passage, le corpus recense ce qu'il a retrouvé par ses propres chemins puis reconnu dans la littérature : Saias–Weingartner, Burnol, Franel, Lapidus, Montgomery, Dyson, Rubinstein et d'autres (doc. 45). Ces redécouvertes valident les chemins pris.

## 12 quater. La géométrie virtuelle (V6.21–V6.24)

L'auteur propose de « résoudre par une géométrie impossible ou virtuelle ». Le corpus découvre alors que sa marge, mesurée depuis la V6.7, est la forme d'intersection d'une surface. Dans le Modèle réduit, cette surface existe, et l'indice de Hodge y vaut pour toutes les courbes et pour aucun faux jumeau. Pour ζ, la surface « virtuelle » calculée depuis les nombres premiers a la bonne signature. Le sosie DH n'en a aucune (doc. 46).

Un relecteur extérieur demande ensuite une propriété d'existence, de dimension ou de dualité, démontrée sans RH. Le corpus les teste toutes sur les faux jumeaux. La dualité et Clifford n'en démasquent aucun. La fonction auxiliaire de Stepanov, avec un revêtement, les démasque tous (doc. 47). Puis il démonte cette fonction : elle n'existe qu'avec le Frobenius. L'identité, qui prend pourtant les mêmes valeurs aux points, échoue, et une permutation aussi (doc. 48). Ce qui compte, c'est qu'une fonction de très haut degré coïncide aux points avec une fonction simple tout en restant invisible aux dérivations (doc. 49).

Le chemin arrive ainsi, par les faux jumeaux, à la question de Connes et Consani : quel Frobenius agit sur les entiers ? Au même moment, le calcul des deux tiers d'Alpöge–Furman, refait sur les zéros du corpus, donne 56 % à la fenêtre démontrée et 88 % si la corrélation de paires était connue deux fois plus loin (doc. 49).

## 13. Les prévisions écrites avant le calcul

Avant la V6.11, une erreur se découvrait après coup, parfois après avoir été écrite comme un résultat. Depuis, la prévision est écrite avant, horodatée, et son sort est publié.

| Version | Prévisions | Tenues | Partielles | Fausses |
|---|---|---|---|---|
| V6.14 (temps de Heisenberg) | 4 | 3 | – | 1 (P4) |
| V6.15 (degré 2, recensement) | 6 | 3 | 2 (à une exception près) | 1 (P3, dans sa lettre) |
| V6.16 (Rencontre à trois) | 5 | 1 | 2 (P1 qualitative ; P5 à moitié) | 2 (P2, P3 pour β) |
| V6.17 (Rencontre en degré 2) | 5 | 3 | 1 (P5, sauf une clause) | 1 (P2) |

Les prévisions fausses ont été les plus instructives. P4 de la V6.14 a montré qu'un quadruplet qui remplace un zéro s'entend presque comme un quadruplet ajouté. P3 de la V6.15 a révélé les 20 directions négatives venues de plus haut, d'où le recensement. P2 et P3 de la V6.16 ont déplacé le regard de β vers sa part d'écart. P2 de la V6.17 a montré que le déficit de répulsion ne tient pas qu'à la densité des zéros, et a produit la prévision suivante.

**Ce que seul l'auteur peut dire.** Les huit questions du premier récit restent ouvertes (origine de l'intérêt pour RH, choix de Q, analogies de navigation et de sources, lien avec GPF Atlas, surprises, acceptation des corrections). Une s'ajoute : d'où vient l'hypothèse de travail elle-même ?

## 14. Ce que le chemin enseigne

- **Les intuitions ne meurent pas, elles changent de statut.** Le « GPS analytique » de l'étape 9 a été rétrogradé, puis relu comme la récurrence de Levinson, puis il est devenu le navigateur. Les sources cachées de l'étape 12 ont été rejetées, et la V6.12 a mesuré pourquoi elles devaient l'être. Garder une trace exacte de la raison d'un rejet permet de rouvrir la question quand les outils changent.
- **Changer de question a plus servi que chercher une nouvelle réponse.** Tant que chaque idée devait prouver RH, chacune finissait en reformulation équivalente. Quand la question est devenue « quel mécanisme ? », puis « à quoi ressemble une nécessité démontrée ? », le Modèle réduit a donné une cible précise : ce qui manque à ζ n'est pas l'opérateur, c'est la métrique.
- **Regarder là où c'est démontré.** Le Modèle réduit, les premiers de Δ, les courbes sur F~p~ : chaque fois qu'une lecture semblait tenir pour ζ, on a cherché son pendant là où RH est un théorème. Les collisions supersingulières de l'étage 2 rappellent qu'un pendant peut aussi corriger une intuition : une rencontre n'est pas une sortie.
- **Un témoin permanent.** Davenport–Heilbronn, arrivé à l'étape 11 comme test de rejet, est resté le témoin de chaque instrument : tout ce qui voit ζ « bien se tenir » doit voir DH mal se tenir, et dire où.
- **Écrire la prévision avant le calcul.** C'est la forme mûre de la règle « lire les tables avant de conclure ». Sur 20 prévisions, 10 tenues, 5 partielles, 5 fausses : c'est ce que l'on attend d'un programme qui teste vraiment.
- **Se corriger vite.** La V6.14 corrige la V6.12, la V6.17 corrige la V6.15, la V6.7 corrige le document 26. Chaque correction est datée et laissée visible.
- **Une pré-relecture n'est pas une relecture.** Le niveau 7 reste à atteindre : il dépend d'un regard extérieur.

## 15. Lecture selon l'hypothèse

L'hypothèse de travail de l'auteur : **RH n'existe que parce qu'elle est nécessaire à quelque chose de plus grand qui la rend nécessaire.**

| | Ce que le chemin a établi | Statut |
|---|---|---|
| Démontré | En degré 1, dans les espaces V~q~, RH implique le produit d'Euler (avec Saias–Weingartner). Dans le Modèle réduit, la positivité vient de la surface C × C (Weil). Aux premiers de Δ, positivité et Sato–Tate viennent d'un même objet, la représentation galoisienne. | Théorèmes cités ou prouvés ici. |
| Mesuré | La symétrie seule ne rend pas RH nécessaire (famille modulo 7). ζ présente trois des quatre traits d'une nécessité démontrée. Ce qui manque est la métrique, et la métrique se lit depuis les premiers. Pour ζ et Δ, la répulsion suit la Loi de la marge ; une superposition (ζ·L(χ5)) n'a pas de répulsion mutuelle. | Mesures reproduites, avec témoins. |
| Supposé | Qu'un objet plus grand existe pour ζ, qui porte la métrique positive, comme C × C la porte pour une courbe. S'il existe, il devrait aussi imposer la Loi de la marge entre les zéros, comme le groupe de monodromie le fait sur les corps finis. | Lecture, non démontrée. |

Lu dans ce sens, le chemin a resserré la question. Au début, « quelque chose de plus grand » était une intuition. En V6.6, c'est un objet d'un étage au-dessus, dont on connaît les trois signatures visibles. En V6.9, c'est ce qui doit porter la métrique. En V6.17, c'est ce qui imposerait à la fois la positivité (« marge ≥ 0 ») et la statistique (« fréquence ∝ marge »). La répulsion mesurée entre les zéros de ζ et de Δ serait alors une trace de cet objet ; l'absence de répulsion mutuelle dans ζ·L(χ5) dirait que, derrière un produit, il y a deux objets et non un seul. Ce n'est pas une démonstration. C'est la forme précise que l'hypothèse a prise en chemin, et elle se teste : le prochain coup, la Loi de la marge en genre 2, demande quelle métrique a pour marge la densité de USp(2g).

<!-- references:debut -->

## Références

Format : [clé] auteurs, *titre*, publication, lien. Fiches complètes et état de vérification : document 42 (registre des sources).

- [Bae03] L. Báez-Duarte. *A strengthening of the Nyman–Beurling criterion for the Riemann hypothesis*. Atti Accad. Naz. Lincei Rend. Lincei Mat. Appl. (9) 14 (2003), 5–11 ; arXiv:math/0202141. <https://arxiv.org/abs/math/0202141> — vérifié en ligne
- [Bae05] L. Báez-Duarte. *A general strong Nyman–Beurling criterion for the Riemann hypothesis*. Publ. Inst. Math. (Beograd) (N.S.) 78(92) (2005), 117–125. — partiellement vérifié
- [BBLM06] E. Bogomolny, O. Bohigas, P. Leboeuf, A. G. Monastra. *On the spacing distribution of the Riemann zeros: corrections to the asymptotic result*. J. Phys. A 39 (2006), 10743–10754 ; arXiv:math/0602270. <https://arxiv.org/abs/math/0602270> — vérifié en ligne
- [BCF13] S. Bettin, J. B. Conrey, D. W. Farmer. *An optimal choice of Dirichlet polynomials for the Nyman–Beurling criterion*. Proc. Steklov Inst. Math. 280 (2013) ; arXiv:1211.5191. <https://arxiv.org/abs/1211.5191> — vérifié en ligne
- [Beu55] A. Beurling. *A closure problem related to the Riemann zeta-function*. Proc. Natl. Acad. Sci. USA 41 (1955), 312–314. <https://www.pnas.org/doi/pdf/10.1073/pnas.41.5.312> — vérifié en ligne
- [BGHT11] T. Barnet-Lamb, D. Geraghty, M. Harris, R. Taylor. *A family of Calabi–Yau varieties and potential automorphy II*. Publ. RIMS 47 (2011), 29–98 ; DOI 10.2977/PRIMS/31. <https://ems.press/journals/prims/articles/4468> — vérifié en ligne
- [BT14] A. R. Booker, F. Thorne. *Zeros of L-functions outside the critical strip*. Algebra Number Theory 8 (2014), no. 9, 2027–2042 ; DOI 10.2140/ant.2014.8.2027 ; arXiv:1306.6362 ; correction ANT 8:9. <https://arxiv.org/abs/1306.6362> — vérifié en ligne
- [Con89] J. B. Conrey. *More than two fifths of the zeros of the Riemann zeta function are on the critical line*. J. reine angew. Math. 399 (1989), 1–26 ; annonce : Bull. AMS 20 (1989), 79–81. <https://www.ams.org/bull/1989-20-01/S0273-0979-1989-15704-2/> — partiellement vérifié
- [Cra22] H. Cramér. *Ein Mittelwertsatz in der Primzahltheorie*. Math. Z. 12 (1922), 147–153. — partiellement vérifié
- [Del74] P. Deligne. *La conjecture de Weil. I*. Publ. Math. IHÉS 43 (1974), 273–307 ; DOI 10.1007/BF02684373. <https://www.numdam.org/item/PMIHES_1974__43__273_0/> — vérifié en ligne
- [DH36a] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series*. J. London Math. Soc. 11 (1936), no. 3, 181–185. <https://doi.org/10.1112/jlms/s1-11.3.181> — partiellement vérifié
- [DH36b] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series. II*. J. London Math. Soc. 11 (1936), no. 4, 307–312. <https://doi.org/10.1112/jlms/s1-11.4.307> — partiellement vérifié
- [Dys62] F. J. Dyson. *Statistical theory of the energy levels of complex systems. I–III*. J. Math. Phys. 3 (1962), 140–156, 157–165, 166–175. <https://doi.org/10.1063/1.1703773> — partiellement vérifié
- [Kal60] R. E. Kalman. *A new approach to linear filtering and prediction problems*. J. Basic Eng. 82 (1960), 35–45. <https://www.cs.unc.edu/~welch/kalman/kalmanPaper.html> — partiellement vérifié
- [Leh56] D. H. Lehmer. *On the roots of the Riemann zeta-function*. Acta Math. 95 (1956), 291–298. <https://en.wikipedia.org/wiki/Lehmer_pair> — partiellement vérifié
- [Lev47] N. Levinson. *The Wiener RMS (root mean square) error criterion in filter design and prediction*. J. Math. Phys. 25 (1947), 261–278 ; amélioré par J. Durbin, Rev. Inst. Int. Stat. 28 (1960), 233–243. <https://en.wikipedia.org/wiki/Levinson_recursion> — partiellement vérifié
- [Mon73] H. L. Montgomery. *The pair correlation of zeros of the zeta function*. Analytic Number Theory, Proc. Sympos. Pure Math. 24, AMS (1973), 181–193. <https://public.websites.umich.edu/~hlm/paircor1.pdf> — vérifié en ligne
- [MT58] A. Mattuck, J. Tate. *On the inequality of Castelnuovo–Severi*. Abh. Math. Sem. Univ. Hamburg 22 (1958), 295–299 (volume et pages non confirmés en ligne). <https://arxiv.org/abs/1210.7459> — partiellement vérifié
- [Nym50] B. Nyman. *On the one-dimensional translation group and semi-group in certain function spaces*. Thèse, Université d'Uppsala, 1950. — partiellement vérifié
- [Ram16] S. Ramanujan. *On certain arithmetical functions*. Trans. Cambridge Philos. Soc. 22 (1916), 159–184. <https://encyclopediaofmath.org/wiki/Ramanujan_function> — partiellement vérifié
- [SW09] É. Saias, A. Weingartner. *Zeros of Dirichlet series with periodic coefficients*. Acta Arith. 140 (2009), no. 4, 335–344 ; DOI 10.4064/aa140-4-4 ; arXiv:0807.0783. <https://arxiv.org/abs/0807.0783> — vérifié en ligne
- [Tur53] A. M. Turing. *Some calculations of the Riemann zeta-function*. Proc. London Math. Soc. (3) 3 (1953), 99–117. <https://en.wikipedia.org/wiki/Turing%27s_method> — partiellement vérifié. **Correctif V6.18 :** Le corpus applique une forme simple (contrôle empirique de S(t)) de la méthode de Turing ; la méthode certifiée utilise une borne explicite sur ∫S(t)dt et les points de Gram.
- [Wei48] A. Weil. *Sur les courbes algébriques et les variétés qui s'en déduisent*. Actualités Sci. Ind. 1041, Hermann, Paris (1948). <https://denisevellachemla.eu/Weil-courbes-varietes.pdf> — partiellement vérifié. **Correctif V6.18 :** Le mémoire Sur les courbes… établit directement la positivité par correspondances, intersections et Riemann–Roch. La fiche précédente le résumait trop exclusivement par la jacobienne ; ne pas confondre ce mémoire et celui sur les variétés abéliennes.
- [Wei52] A. Weil. *Sur les « formules explicites » de la théorie des nombres premiers*. Comm. Sém. Math. Univ. Lund, vol. suppl. dédié à M. Riesz (1952), 252–265. <https://en.wikipedia.org/wiki/Weil%27s_criterion> — partiellement vérifié
- [Wey39] H. Weyl. *The Classical Groups: Their Invariants and Representations*. Princeton University Press (1939). <https://press.princeton.edu/books/paperback/9780691057569/the-classical-groups> — partiellement vérifié

<!-- references:fin -->
