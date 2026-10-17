# Guide de lecture intuitif

**Date :** 10 octobre 2026  
**Statut :** document d'accompagnement, sans résultat nouveau. Mis à jour en V6.24, 11 octobre 2026 (précédente mise à jour : V6.18) ; version d'origine : `07_Guide_de_lecture_intuitif.docx` (antérieure à la V6, guide de lecture de l'article sur l'énergie Q).  
**Auteur :** Vincent NOËL

## 0. Comment lire ce guide

Ce guide s'adresse à un non-spécialiste. La version d'origine suivait l'article sur l'énergie Q(X). Depuis (V6.0 à V6.17), le programme parle aussi de métrique, de marge, de Modèle réduit et de temps de Heisenberg. Le guide devient donc un **parcours**, de l'image la plus simple à la plus fine. Chaque image est donnée avec trois choses :

- **l'image** elle-même, pour fixer l'intuition ;
- **l'énoncé exact** qu'elle résume, avec son statut (démontré, mesuré ou supposé) ;
- **l'endroit où l'image casse**, c'est-à-dire ce qu'il ne faut pas lui faire dire.

C'est la règle du registre des métaphores (document 20).

Une chose est dite une fois pour toutes. **Le programme ne revendique aucune preuve de l'hypothèse de Riemann (RH).** Les deux théorèmes démontrés (A et B) ont été pré-relus en interne en V6.13, pas encore par un spécialiste. Les autres énoncés démontrés sont des identités élémentaires ou des théorèmes cités ; le reste est mesuré ou supposé, et le guide le dit à chaque fois.

L'hypothèse de travail de l'auteur sert de fil : **« RH n'existe que parce qu'elle est nécessaire à quelque chose de plus grand qui la rend nécessaire. »** Sa lecture est rassemblée au §15.

## 1. L'image de départ : un signal et ses fréquences

**L'image.** Les nombres premiers forment un signal irrégulier. Les zéros de la fonction ζ en sont les fréquences cachées.

**Pourquoi l'image est naturelle.** Les entiers se fabriquent en multipliant des nombres premiers. Le logarithme change les produits en sommes : une puissance p^k^ devient une position k·log p. Après le changement de variable u = log x, la transformée de Mellin (adaptée aux changements d'échelle) devient une transformée de Fourier. Les longueurs log p apparaissent alors comme des positions dans la variable u.

**L'énoncé exact.** La formule explicite (Riemann, von Mangoldt ; sous la forme de Weil (1952) [Wei52]) relie une somme sur les puissances de nombres premiers à une somme sur les zéros. Un zéro ρ = β + iγ fournit un terme x^ρ^. Avec x = e^u^ et la normalisation par e^u/2^ :

  x^ρ−1/2^ = e^(β−1/2)u^ · e^iγu^.

La hauteur γ est une fréquence. L'écart β − 1/2 est une croissance d'amplitude. Cette dualité est **inconditionnelle** : elle existe que RH soit vraie ou non. RH dit seulement que tous les β valent 1/2, c'est-à-dire que tous les modes sont des oscillations pures, sans croissance.

**Où l'image casse.**

- On ne manipule pas une somme ordinaire Σ e^iγt^. Le pôle de ζ produit un terme de taille e^|t|/2^ : la distribution brute n'est pas tempérée. La formule de Weil se lit contre une fonction test h, analytique dans une bande |Im r| ≤ 1/2 + δ et assez décroissante. C'est une identité entre deux fonctionnelles, pas entre deux listes.
- Une somme tronquée, par exemple −Σ~n≤N~ Λ(n) n^−1/2^ cos(γ log n), montre des pics près des zéros. Leur largeur dépend de N. C'est une résolution finie ; le §10 dira laquelle suffit à une hauteur donnée.

## 2. Le Thermomètre : une énergie qui lit la position des zéros

**L'image.** Un microphone enregistre le signal des premiers. On le prétraite, on l'accumule, et on mesure son énergie moyenne, sans laisser le positif et le négatif s'annuler. Cette énergie est un **thermomètre** : sa vitesse de montée dit de combien le zéro le plus éloigné s'écarte de la droite critique.

**La construction.** À partir de la fonction de von Mangoldt Λ :

  c = Λ∗Λ − Λ·log + 2γΛ,  C(x) = Σ~n≤x~ c(n),  Q(X) = ∫~1~^X^ |C(x)|²/x² dx.

La série G(s) = Σ c(n) n^−s^ vaut q² + q′ + 2γq, avec q = −ζ′/ζ. Elle est **une Loupe double** : près d'un zéro de multiplicité m, G ≈ m(m+1)/(s − ρ)², un pôle double. Le terme 2γΛ est **un Contrepoids** qui rend G régulière en s = 1. Et c ne garde que les entiers à deux facteurs premiers distincts au plus (**le Tamis à deux**).

**Les énoncés exacts.**

- **Théorème A (démontré).** Avec Θ = sup Re ρ : ½ limsup log(1 + Q(X))/log X = Θ − ½. Donc RH ⟺ Q(X) = X^o(1)^. Idée : une énergie petite force la convergence de G(s)/s = ∫ C(x) x^−s−1^ dx, donc interdit les pôles, donc les zéros trop à droite.
- **Théorème B (démontré, sous RH).** Q(X) ∼ (S/3)(log X)³, avec S = Σ m(ρ)²(m(ρ)+1)²/|ρ|². Si tous les zéros sont simples, Q(X) ∼ (4κ/3)(log X)³, avec κ = 2 + γ − log 4π. Idée : chaque zéro est une raie spectrale dont on additionne l'énergie (Plancherel [Tit37], puis Karamata [Kar31]).
- **Corollaire B′ (nouveau en V6.13, à faire vérifier).** Sous RH, Q(X)/(log X)³ → 4κ/3 si et seulement si tous les zéros sont simples. La constante de Q lit donc la simplicité.
- **Proposition C.** Le terme en (log X)² est [α + Φ(log X)](log X)², où Φ est une somme de « battements » entre zéros voisins, de fréquences γ − γ′. Calcul rigoureux pour un modèle fini de zéros ; corrélation 0,996 avec les mesures ; α corrigé en V6.13 : −0,3074.
- **La note fondamentale κ.** κ = 2λ~1~, deux fois le premier coefficient de Li. La même constante apparaît dans la distance de Nyman–Beurling [Nym50] [Beu55] (Burnol [Bur02]). En V5, la projection de Nyman–Beurling s'est ramenée exactement à Q : la branche est close.

**Où l'image casse.**

- Lire la fièvre ne la fait pas baisser. Le Théorème A est une **reformulation exacte** de RH. Pour prouver RH par là, il faudrait établir la croissance lente de Q sans supposer RH.
- Le « son pur » n'apparaît qu'à l'infini. Mesurée jusqu'à X = 4·10^6^, Q n'atteint que 44 à 72 % de sa valeur asymptotique (le Diapason).
- Une loupe grossit aussi les défauts : deux zéros très proches font de grands battements. Le terme suivant demande de contrôler les paires serrées, ce qui sera la question du §11.
- κ = 2λ~1~ n'est qu'un premier coefficient. Le critère de Li porte sur toute la suite.

## 3. Le Sosie : un détecteur n'est pas une loi

**L'image.** Le Sosie a le même visage que ζ (la même équation fonctionnelle) mais pas le même moteur : pas de produit d'Euler, et des zéros hors de la droite.

**L'énoncé exact.** La fonction de Davenport–Heilbronn [DH36b] [DH36a] (DH) a un zéro en 0,8085 + 85,699i. Le thermomètre y monte plus vite : pente de Q de 0,56, contre 0,33 pour ζ et 0,34 pour L(s, χ₅) (banc de rejet, v3.2). Q détecte donc les zéros mal placés, mais rien en lui ne les interdit : sa positivité est celle d'un carré, automatique, pas la positivité de Weil. Un test sur la densité des zéros retombe sur les problèmes classiques de grandes valeurs, sans gain. **La leçon** : une preuve de RH devra utiliser le produit d'Euler, puisque DH a tout le reste. En V6.3d, le classement des instruments l'a confirmé : tous voient les zéros, aucun ne voit plus.

**Où l'image casse.** DH n'est pas un modèle de ζ. C'est un témoin de crash-test, qui sert à rejeter les critères qui ne voient que la symétrie. Et un thermomètre mesure une fièvre ; il ne l'empêche pas.

## 4. Le Modèle réduit et la positivité de Castelnuovo [MT58]

**L'image.** Une maquette où RH est vraie, grâce à une géométrie que l'original n'a pas. Elle montre à quoi ressemble une RH *nécessaire*.

**Le terrain.** Une courbe C sur un corps fini à q éléments, de genre g. On compte ses points N~n~ sur les corps à q^n^ éléments ; la suite de ces corps est **la Tour**. Sa fonction zêta a 2g zéros, une équation fonctionnelle et un produit d'Euler ; pour elle, RH est un théorème : Hasse (1936) [Has36] en genre 1, Weil (1948) [Wei48] en général.

**L'énoncé exact : la positivité de Castelnuovo.** Ce qui rend RH nécessaire vit sur la surface C × C, un étage au-dessus de la courbe. À chaque étage n de la tour, une forme d'intersection doit être positive :

  Q~n~(r, s) = g·r² − (N~n~ − q^n^ − 1)·r·s + g·q^n^·s² ≥ 0,  soit  ρ~n~ = |N~n~ − q^n^ − 1| / (2g·q^n/2^) ≤ 1.

Si ρ~n~ ≤ 1 à tous les étages, RH suit, et réciproquement.

**Ce qui a été mesuré (V6.6, document 28).**

- 425 courbes (genre 1 à 8, sur F₃, F₅, F₇) : positivité de Castelnuovo exacte à tous les étages jusqu'à 60.
- **Le Faux jumeau entier** : 220 polynômes ont l'équation fonctionnelle et un produit d'Euler à comptages entiers positifs, mais RH fausse. Aucun n'est une courbe. La positivité de Castelnuovo les démasque à un étage fini (2 à 5 en genre 2). Le produit d'Euler positif seul ne leur donne que « aucun zéro sur Re s = 1 », le niveau de Hadamard et de la Vallée Poussin (1896) [Had96] pour ζ.
- **La Positivité saturée** : la marge 1 − max ρ~n~ s'annule en montant dans la tour. Elle est exactement nulle pour la courbe y² = x⁵ + x³ + 1 sur F₃ à l'étage 4 (118 points sur F₈₁). RH y est vraie sans aucun jeu, comme pour ζ, où la constante de de Bruijn–Newman [DeB50] [New76] vérifie Λ ≥ 0 (Rodgers–Tao, 2020 [RT20]) : RH, si elle est vraie, l'est « tout juste ».

**La signature d'une nécessité démontrée** tient en quatre traits : (1) équation fonctionnelle et produit d'Euler ne suffisent pas ; (2) une positivité indexée par une tour démasque les faux à un étage fini ; (3) cette positivité tient sans marge ; (4) elle vient d'un objet d'un étage au-dessus. **ζ présente les trois premiers traits. Il lui manque l'objet.**

**Où l'image casse.** La maquette a une dimension de plus que l'original : il n'existe pas de « Spec ℤ × Spec ℤ » connu qui jouerait le rôle de C × C. Et ζ n'a pas de Frobenius, donc pas de tour évidente. La question « quel est l'étage n de ζ ? » reçoit des réponses partielles plus loin (§7, §10), jamais une réponse complète.

## 5. La Métrique

**L'image.** Une machine (un opérateur) dont les fréquences propres seraient les zéros. La machine est là ; il manque la règle qui mesure. Cette règle est **la métrique** : une façon de mesurer les longueurs pour laquelle la machine tourne sans rien grossir ni rétrécir.

**L'énoncé exact, en général.** Si H\*M = MH avec M définie positive, bornée et d'inverse borné, le spectre de H est réel. Si M est indéfinie, on n'obtient qu'une symétrie du spectre, que ζ a déjà par l'équation fonctionnelle (ρ ↔ 1 − ρ̄). **La positivité de M est donc toute la substance** : chez Weil, une positivité de la forme explicite équivaut à RH.

**L'énoncé exact, mesuré (V6.9, document 32).** Dans le Modèle réduit, on reconstruit l'opérateur depuis les seuls comptages de points (construction de type GNS ; 749 objets) :

| Objets | Opérateur reconstruit | Symétrie | Métrique (Gram) |
|---|---|---|---|
| 524 vraies courbes à zéros simples | oui, valeurs propres à 10^−13^ | oui | positive (524 sur 524) |
| 220 faux jumeaux | oui, aussi bien | oui | jamais positive : une direction négative par paire de zéros hors du cercle |
| 5 objets à zéros confondus | oui, un axe par zéro distinct | oui | positive ; la multiplicité reparaît comme masse |

**Ce qui sépare les vraies courbes des imposteurs n'est ni l'opérateur, ni la symétrie, ni le produit d'Euler : c'est la métrique.** C'est **la Métrique manquante** du registre. Pour ζ, le programme mesure ensuite cette métrique depuis les nombres premiers (§9).

**Un voisin dans la littérature.** La même positivité, comprimée en dimension finie, donne des résultats en proportion : plus des deux tiers des zéros de ζ sont simples et sur la droite (Alpöge–Furman, 2026 [AF26] ; nouvelle preuve, Lamzouri, 2026 [Lam26]). C'est **le Compteur** du registre : il compte au lieu de localiser, et ne donne que des proportions.

**Où l'image casse.** Dans le Modèle réduit, la métrique positive vient de la surface C × C. Pour ζ, on ne sait pas d'où elle viendrait. Et « la métrique est positive » n'est mesuré que dans des fenêtres finies.

## 6. Le Passage interdit

**L'image.** Une porte au ras du mur, mais murée. On peut se tenir exactement au bord de la région où RH est vraie, sans qu'il existe de passage vers l'autre côté.

**L'énoncé exact (V6.7, document 29).** Deux marges sont à distinguer.

| | Ce qu'on perturbe | Ce qu'on trouve dans le Modèle réduit (525 courbes, genre 1 à 12) |
|---|---|---|
| **Marge de la forme** | n'importe quelle perturbation de la matrice de Weil | exactement nulle dès que la fenêtre dépasse le nombre de zéros (2g) : la matrice a un rang au plus 2g |
| **Marge de l'objet** | seulement les données locales, équation fonctionnelle conservée | en général positive, fixée par la paire de zéros la plus serrée ; exactement nulle pour les courbes à zéros confondus, où RH reste un théorème |

La fenêtre 2g est aussi celle du **Recensement** : à cette fenêtre, le nombre de valeurs propres négatives est exactement la moitié du nombre de zéros hors de la droite (900 polynômes sur 900 en 60 chiffres, 220 faux jumeaux sur 220).

**La lecture.** Là où RH est démontrée, les deux marges peuvent être nulles, et aucune vraie courbe ne sort pour autant. **La nécessité n'éloigne pas du bord, elle interdit le passage** : aucune perturbation qui sort de la région RH n'est une courbe.

**Où l'image casse.** C'est formulé et vérifié dans le Modèle réduit. Pour ζ, la question devient : une sortie de la droite peut-elle garder un produit d'Euler (§7) ? Dans le modèle, le produit d'Euler seul ne bloque la sortie la plus proche que pour 24 courbes sur 525 : ce qui mure la porte est la géométrie.

## 7. L'Archipel d'Euler

**L'image.** Des îles dans une mer qui monte. Chaque île entoure un point où un objet se tient derrière la fonction. Plus on regarde haut, plus la mer monte ; à la fin, il ne reste que les points.

**Le terrain (V6.8, document 30).** Les espaces V~q~ (q premier ≤ 13, parité fixée) : combinaisons réelles de fonctions L(s, χ) qui ont toutes la même équation fonctionnelle. Un **point d'Euler** est une seule L(s, χ) : la seule à avoir un produit d'Euler.

**Les énoncés exacts.**

- **Démontré (ici, élémentaire).** Rigidité au premier ordre : dans V~q~, aucune direction qui garde l'équation fonctionnelle ne garde le produit d'Euler, même au premier ordre. Le Passage interdit du §6 est donc démontré dans ces espaces.
- **Démontré (cité, pas nouveau).** Dans V~q~, toute fonction qui vérifie RH, et même toute fonction sans zéro dans Re s > 1, est un point d'Euler : c'est un cas particulier de Saias–Weingartner [SW09] (2009) et de Booker–Thorne [BT14] (2014). Pour ζ, l'espace est de dimension 1 : ζ n'a pas de voisine qui garde l'équation fonctionnelle (Hamburger, 1921 [Ham21]) ; c'est **l'Île sans mer**.
- **Mesuré.** Autour de chacun des 27 points d'Euler, une île de rayon médian 0,091 à |t| ≤ 25 et 0,008 à |t| ≤ 300, qui rétrécit avec une pente de −0,77 en fonction du nombre de zéros. On en sort par la paire de zéros la plus serrée (112 sorties sur 116).

**La lecture.** Dans ces espaces, RH n'existe que là où un objet (un caractère) se tient derrière la fonction. Et la hauteur joue le rôle de l'étage de la tour du Modèle réduit : un faux est démasqué à une hauteur finie, d'autant plus haute qu'il est proche d'un point d'Euler.

**Où l'image casse.** La mer n'est pas uniforme : il y a des chenaux le long de certains grands cercles, et à basse hauteur les îles sont reliées (le Continent bas). Surtout, l'Archipel dit **où** RH peut vivre, pas **pourquoi** elle y vit : que chaque point d'Euler vérifie RH reste l'hypothèse de Riemann généralisée.

## 8. Le Chaînon, et ce que l'analogie de Selberg dit vraiment

**L'image.** Le pas discret est l'exponentielle d'un générateur continu. Comme en calcul symbolique, où le décalage f(x) ↦ f(x + h) s'écrit E = e^hD^ avec D = d/dx.

**L'énoncé exact (V6.9, document 32).** Pour une courbe sur F~q~, le Frobenius F s'écrit F = q^D^. Les zéros de la fonction zêta de la courbe sont le spectre du générateur D, répété avec la période 2πi/log q. Les traces des puissances de F comptent les orbites : une orbite fermée de degré n a la longueur n·log q. **La formule explicite est une formule des traces** : somme sur les zéros = somme sur les orbites. Quatre structures font de F un opérateur pour lequel RH est vraie : la finitude (2g zéros ; pour ζ, une infinité), les traces (pour ζ, le produit d'Euler), la symétrie (pour ζ, l'équation fonctionnelle) et la métrique positive (pour ζ, RH elle-même).

**Le Spectre des longueurs (mesuré).** Calculé sur les seuls zéros, un signal S(u) a des pics aux longueurs log n, de hauteur c(n)/√n. Pour ζ, les pics sont aux log p^k^ (35 longueurs). Pour DH, 45,6 % du signal tombe aux longueurs composites (log 6, log 12…) : l'absence de produit d'Euler se lit dans les zéros seuls.

**L'analogie de Selberg, mise à jour.** La formule des traces de Selberg (1956) [Sel56] relie les longueurs des géodésiques fermées d'une surface au spectre d'un laplacien. Le dictionnaire tente : nombre premier p ↔ géodésique primitive ; k·log p ↔ k-ième répétition ; γ ↔ niveau spectral. Le Chaînon montre que ce dictionnaire est exact dans le Modèle réduit. Pour ζ, trois différences restent vraies :

1. **Le signe.** Dans la formule explicite de ζ, le terme des premiers n'a pas naïvement le signe d'une formule de traces de type Gutzwiller. Connes a proposé de lire les zéros comme un spectre d'absorption [Con99] : des raies manquantes plutôt qu'ajoutées.
2. **La densité.** Pour un laplacien de surface compacte, la loi de Weyl [Wey12] donne N(r) ∼ c·r². Pour ζ, N(T) ∼ (T/2π) log T. Les modèles de type H = xp [BK99a] (Berry–Keating) ont la bonne croissance. Cette densité réapparaît au §10, comme une horloge.
3. **La statistique.** Les écarts entre zéros de ζ suivent, conjecturalement et numériquement, la loi GUE et non GOE : pas de symétrie de renversement du temps, contrairement à un flot géodésique réel. Le programme mesure désormais cette statistique directement (§11).

La différence de fond demeure : chez Selberg, l'opérateur existe d'abord et la réalité du spectre en découle. Pour ζ, on a la formule ; l'objet qui l'expliquerait n'est pas construit.

**Où l'image casse.** Dans le Modèle réduit, D n'est connu qu'à la période 2πi/log q près ; changer de base revient à changer la cadence d'une caméra, et D reste le même (V6.11, 525 courbes). ζ n'a ni période ni cadence naturelle : **le seul pas qui lui convienne est le flot** e^tD^, t réel.

## 9. Le Générateur des premiers

**L'image.** Les nombres premiers jouent la partition ; l'opérateur est l'instrument qu'on en déduit.

**Ce que disait la version d'origine, et ce qui a changé.** Le guide d'origine rappelait qu'une évolution « de Schrödinger » choisie après coup a toujours les zéros pour valeurs propres, si on les connaît déjà : le contenu ne commence que si l'opérateur est construit **sans les zéros**. C'est ce qui a été fait, dans une fenêtre finie.

**L'énoncé exact (V6.10, document 33).** Les traces t~n~ = Σ ĝ(γ) e^iγnh^ sont calculées par la formule explicite avec les seuls nombres premiers (audit : 3,5·10^−14^ pour ζ). Un faisceau de matrices de Toeplitz en tire l'opérateur de translation e^hD^.

- Avec les premiers ≤ 439 : 226 zéros de ζ, 334 de L(s, χ₅), 330 de DH, aucune fausse détection. Avec les premiers ≤ 23 862 : 284 zéros de ζ, tous à mieux que 1,6·10^−4^.
- **La Masse unité.** Chaque vraie valeur propre porte la masse ĝ(γ), soit 1 pour un zéro simple. Le mode « fantôme » de la V4.3 pèse 1,3·10^−9^ (V6.12).
- **La métrique, lue depuis les premiers.** Positive pour ζ et L ; pour DH, deux directions négatives par quadruplet de zéros hors droite, attribuées exactement. En V6.15, à l'échelle des premiers ≤ 1 370, elle **recense** 50 directions négatives pour DH, toutes attribuées à 25 quadruplets jusqu'à la hauteur 1 464 ; aucune pour ζ ni L.
- **Le Rayon spectral (V6.12).** L'écart Θ − ½ du Théorème A se lit au bord du spectre du générateur : 0,308517 pour DH, moins de 10^−6^ pour ζ et L. Le thermomètre du §2 et le générateur mesurent la même chose à deux échelles.

**Où l'image casse.**

- Tout cela vaut dans une fenêtre finie, avec un pas h choisi. On ne sait pas vers quoi l'opérateur converge quand la fenêtre grandit.
- **La complétude reste le vrai verrou.** Connes a déjà fourni une réalisation spectrale des zéros critiques ; voir aussi Connes, Consani et Moscovici (2025) [CCM25]. Ce qui manque n'est ni un opérateur ni l'auto-adjonction : c'est de montrer que **tous** les zéros sont capturés, avec la bonne multiplicité, sans exception hors de la droite.
- Les méthodes de signal (moyennage, filtre de Kalman [Kal60], devenu ici la récurrence de Levinson (1947) [Lev47], localisation de sources) sont d'excellents instruments de diagnostic et de calibration. Une résolution finie ne peut pas exclure un zéro hors de la droite plus haut (§10).

## 10. Le Temps de Heisenberg

**L'image.** Une note n'est entendue que lorsque l'oreille sépare les notes voisines. Un zéro hors de la droite, noyé parmi ses voisins, n'apparaît dans la métrique qu'au moment où la fenêtre est assez longue pour distinguer les zéros un par un.

**L'énoncé exact (V6.14, document 38).** Un quadruplet hors droite à la hauteur γ~0~ est détecté à la fenêtre

  L~c~ ≈ L~H~(γ~0~) = log(q·γ~0~/2π),

où q est le conducteur (1 pour ζ, 5 pour L(s, χ₅) et DH). L~H~ est le **temps de Heisenberg** : 2π fois la densité moyenne des zéros à cette hauteur. En nombres premiers, il faut les premiers jusqu'à environ q·γ~0~/2π, le conducteur analytique.

- Mesuré : rapport L~c~/L~H~ entre 0,95 et 1,08 pour ζ et L(s, χ₅), des hauteurs 20 à 200 (recalculé par un vérificateur indépendant ; prévisions écrites avant les tests, trois sur quatre tenues). Pour les quadruplets réels de DH : 0,80 à 0,89.
- **En degré 2 (V6.15)**, avec la fonction L de Δ de Ramanujan [Ram16], la loi double avec la densité des zéros : la longueur d'écoute est le **poids archimédien** Ω(γ~0~) = 2π × densité, avec un rapport de 1,02 à 1,08.
- **Démontré : le lemme d'inertie.** La métrique, fond B plus une paire, cesse d'être positive si et seulement si C^−1^ + U\*B^−1^U est définie positive (Haynsworth, 1968 [Hay68]).
- **Le Signe fragile.** Correction de la V6.12 : quatre seuils annoncés étaient du bruit numérique. Le signe d'une innovation n'est fiable que si la métrique est bien conditionnée ; il a fallu 80 chiffres pour la détection exacte.

**La lecture.** Le test de positivité est **local en hauteur**, et son coût croît avec elle : chaque hauteur a son échelle de nombres premiers, et aucune famille finie de premiers ne surveille toutes les hauteurs.

**Où l'image casse.** Les zéros ne « s'allument » pas : ils sont fixes, c'est la fenêtre qui grandit. Le facteur 0,8–0,9 de DH n'est pas expliqué (peut-être la statistique de ses zéros). Les poids très faibles (sous 10^−5^, lobes secondaires de la fonction test) et un pas trop grossier (h > π/γ~0~, repliement) faussent la loi. Enfin, l'idée que « l'étage n de la tour correspond à log C(T) » est une correspondance de lecture, pas un résultat.

## 11. La Rencontre à trois

**L'image.** Trois chemins qui se croisent au même carrefour. Le carrefour est le choc de deux zéros. Trois problèmes aussi difficiles que RH y passent : RH elle-même, la simplicité des zéros et leur répulsion.

**Pourquoi ce carrefour.** Dans toutes les familles étudiées (V6.5, V6.7, V6.8), deux zéros se rejoignent sur la droite avant de la quitter ensemble. La simplicité dit que la rencontre n'a jamais lieu ; la répulsion dit qu'elle est rare.

**L'énoncé exact (V6.16, document 40 ; démontré, élémentaire).** Deux zéros γ et γ + g entrent dans la métrique par deux directions. Leur **marge locale** est le déterminant normalisé de leur Gram : 1 quand les directions sont orthogonales, 0 quand elles se confondent. À la fenêtre de Heisenberg du §10, et à la limite d'un pas nul,

  m(s) = 1 − (sin πs / πs)²,  s = écart normalisé.

C'est exactement la densité de corrélation de paires de Montgomery (1973) [Mon73]. Une paire hors de la droite donne une marge **négative**.

**RH, simplicité et répulsion sont trois lectures d'une même quantité** : RH dit que la marge n'est jamais négative, la simplicité qu'elle ne s'annule jamais, la répulsion qu'elle est rarement petite.

**Mesuré sur 1 070 zéros de ζ jusqu'à 1 500.** 4 marges sous 0,1, là où le GUE en attend environ 13 et une loi sans répulsion (Poisson) 320. La paire de Lehmer (1956) [Leh56], près de 7 005, a une marge de 0,006. Le Thermomètre porte les trois problèmes, ordre par ordre : son exposant lit RH (A), sa constante lit la simplicité (B′), et la part d'écart de son coefficient β lit les paires serrées (le **Compteur de paires**).

**Où l'image casse.** Le calcul se fait avec un modèle à deux atomes ; dans la vraie métrique, les voisins comptent aussi. L'écart à la prévision (3 fois moins de petites marges que le GUE) n'était pas prévu ; le §12 en donne une explication probable. Enfin, la finitude de la part d'écart de β n'est reliée à la répulsion que par une heuristique.

## 12. La Loi de la marge

**L'image.** Une foule qui laisse à chacun une place en proportion de l'espace disponible. Une configuration de zéros est d'autant plus fréquente qu'elle laisse de la marge à la métrique.

**Les énoncés exacts (V6.17, document 41 ; démontrés, élémentaires).**

- **Une paire, fenêtre N.** La marge d'une paire est la corrélation de paires des matrices unitaires aléatoires de taille N (CUE, Dyson (1962) [Dys62]). Quand N grandit, on retrouve l'identité du §11.
- **Tous les atomes.** La marge totale, det G, est à une constante près la densité de Weyl [Wey39] des angles d'une matrice unitaire tirée au hasard.
- **Une paire conjuguée** (les deux racines d'un premier de Δ, ou d'une courbe de genre 1). La marge vaut sin²θ = 1 − ρ~1~² : c'est la marge de Castelnuovo du §4. Elle est positive si et seulement si la borne de Hasse (courbes) ou de Ramanujan–Deligne (Δ) est vérifiée. Et la loi de Sato–Tate a pour densité (2/π) sin²θ, soit (2/π) × la marge.

**Aux premiers de Δ, les trois problèmes sont trois théorèmes** : positivité (Deligne, 1974 [Del74]), non-collision (automatique : τ(p)² = 4p^11^ est impossible), répulsion (Sato–Tate, Barnet-Lamb, Geraghty, Harris et Taylor, 2011 [BGHT11]). Mesuré sur les 2 762 premiers p ≤ 25 000 : marge minimale 0,026. Sur 561 258 courbes elliptiques du Modèle réduit : la loi de Sato–Tate « verticale » (Birch, 1968 [Bir68]).

**Mesuré pour les zéros.** Un instrument nouveau, **le Contour tourné**, calcule 2 139 zéros de L(Δ, s) jusqu'à 1 500 en double précision. Ils se repoussent : 8 marges sous 0,1, contre 26 pour le GUE et 641 pour Poisson. Le même déficit de petites marges qu'avec ζ (rapport 0,31) a une explication probable par la hauteur finie (Bogomolny, Bohigas, Leboeuf et Monastra, 2006 [BBLM06]), utilisée hors de son domaine.

**Où l'image casse.** La loi est démontrée pour les groupes unitaires et pour une paire conjuguée. En genre 2 et plus (familles symplectiques), la densité de Haar n'est plus le déterminant de la métrique de taille 2g : quelle métrique aurait pour marge la densité de USp(2g) reste ouvert. Pour les zéros de ζ, la loi est la conjecture de Montgomery, mesurée et non démontrée.

## 13. Les Familles étrangères

**L'image.** Deux foules qui se traversent sans se voir.

**L'énoncé exact (V6.15 puis V6.17).** Le produit ζ·L(s, χ₅) est la fonction zêta du corps Q(√5), de degré 2 mais non primitive. Ses 835 zéros jusqu'à 600 sont ceux de ζ (341) et ceux de L(χ₅) (494).

- 15,3 % de ses zéros ont une marge sous 0,1 (la formule de superposition prévoyait 17,2 %) ; **toutes** ces petites marges sont des paires mixtes, un zéro de ζ et un de L(χ₅).
- La paire mixte la plus serrée est en 533,7796 et 533,7805 : distance 8,9·10^−4^, marge 7·10^−6^, 28 fois plus serrée que la paire de Lehmer.
- **Le pendant exact dans le Modèle réduit.** Au changement de base F~p~ → F~p²~, P(u²) = P(u)·P(−u) : les zéros du deuxième étage sont la réunion de deux familles. Les collisions y existent, exactement aux 18 338 courbes supersingulières sur 561 258, et RH y reste vraie.

**La lecture.** La répulsion appartient à une fonction primitive, pas à un produit. Pour ζ·L(χ₅), l'absence de zéro commun n'est protégée par aucune répulsion ; elle relève d'une autre conjecture, l'indépendance linéaire des ordonnées des zéros. Et l'exemple de l'étage 2 montre que **la simplicité est plus forte que RH** : on peut avoir des zéros confondus sans violer RH.

**Où l'image casse.** Sur Q, aucune collision entre zéros de ζ et de L(χ₅) n'est connue ; sur F~p²~, elles existent. L'image dit qu'aucune force ne les sépare ; elle ne dit pas ce qui, en fait, les empêche de se rencontrer.

## 13 bis. La Rencontre à n

**L'image.** La Rencontre à trois vue en relief : une surface au lieu d'une courbe.

**Ce qui est démontré.** Pour n zéros vus à travers une fenêtre, la marge de leur métrique est exactement leur corrélation à n points, celle des matrices unitaires aléatoires (doc. 43).

**Ce qui est mesuré.** Les triplets des 1 070 zéros de ζ suivent cette surface ; deux familles étrangères se superposent sans se voir.

## 13 ter. La Surface virtuelle

**L'image.** Une surface dont on connaît les croisements sans en connaître les points.

**Ce qui est démontré.** Sur une courbe, la marge du corpus est (au signe près) la forme d'intersection de la surface « courbe × courbe ». RH y équivaut à l'indice de Hodge : une seule direction positive. Pour ζ, la même forme se calcule depuis les nombres premiers ; le pôle joue le rôle des fibres, les nombres premiers celui des points d'intersection, le terme archimédien celui du genre (doc. 46).

**Ce qui est mesuré.** Une seule direction positive pour ζ ; deux, puis dix de trop pour le sosie DH.

**Où l'image casse.** La surface des entiers n'existe pas ; on n'en connaît que l'ombre.

## 13 quater. La Fonction auxiliaire et le Frobenius

**L'image.** Un filet tendu sur tous les points à la fois : s'il y en a trop, il se déchire. Le filet ne tient que grâce à une aiguille particulière, le Frobenius x ↦ x^p^, qui pointe aux mêmes endroits que l'identité mais ne bouge pas quand on la touche (dérivée nulle).

**Ce qui est mesuré.** Dans le Modèle réduit, cette fonction démasque tous les faux jumeaux (doc. 47) ; elle n'existe pas si l'on remplace le Frobenius par l'identité ou par une permutation (doc. 48).

**Ce qui manque pour ζ.** Un « Frobenius absolu » sur les entiers. C'est la question de Connes et Consani (doc. 49).

## 13 quinquies. Les deux tiers

**L'image.** Compter les zéros distincts en mesurant combien leur matrice de Gram est « épaisse » : rang ≥ (trace)²/trace du carré.

**Ce qui est démontré (2026).** Au moins 67,25 % des zéros de ζ sont simples et sur la droite (Alpöge–Furman, sans hypothèse).

**Ce qui est mesuré ici.** Le même calcul, sur nos zéros et avec un noyau plus simple, donne 56 % à la fenêtre démontrée, et environ 88 % si la corrélation de paires était connue deux fois plus loin (doc. 49).

## 14. Démontré, mesuré, supposé

| Image | Démontré | Mesuré | Supposé |
|---|---|---|---|
| Thermomètre (§2) | Théorèmes A, B (sous RH) ; B′ à vérifier | Q à 44–72 % de son asymptote | — |
| Sosie (§3) | — | pentes 0,56 (DH), 0,33 (ζ) | — |
| Modèle réduit (§4) | Weil, Castelnuovo (classiques) | 425 courbes ; 220 faux jumeaux | un analogue de C × C pour ζ |
| Métrique (§5) | M > 0 ⟹ spectre réel (classique) | seule la métrique sépare (749 objets) | l'origine de la métrique de ζ |
| Passage interdit (§6) | marge de la forme nulle au-delà de 2g | recensement exact (525 courbes) | même mécanisme pour ζ |
| Archipel (§7) | rigidité au premier ordre ; RH ⟹ point d'Euler | îles, pente −0,77 | GRH aux points d'Euler |
| Chaînon (§8) | F = q^D^ (classique) | spectre des longueurs | le flot comme support |
| Générateur (§9) | — | 284 zéros de ζ sans zéro injecté ; masses 1 | convergence de l'opérateur |
| Heisenberg (§10) | lemme d'inertie | rapport 0,95–1,08 | mécanisme du seuil |
| Rencontre à trois (§11) | marge = 1 − sinc²(πs) | 4 marges < 0,1 sur 1 070 zéros | β fini ⟺ répulsion |
| Loi de la marge (§12) | Weyl, CUE(N), Sato–Tate | 8 marges < 0,1 pour Δ | origine du déficit bas |
| Familles étrangères (§13) | P(u²) = P(u)·P(−u) | 15,3 % de marges mixtes | — |

## 15. Lecture selon l'hypothèse

L'hypothèse de travail est que RH n'existe que parce qu'elle est nécessaire à quelque chose de plus grand qui la rend nécessaire.

- **Le Modèle réduit** montre à quoi ressemble une RH nécessaire : une positivité indexée par une tour, sans marge, portée par un objet d'un étage au-dessus. ζ en a les signatures observables, sauf l'objet.
- **Le Passage interdit** dit comment agit une telle nécessité : elle mure la sortie au lieu d'éloigner du bord.
- **L'Archipel d'Euler** donne la forme exacte de l'hypothèse dans une classe d'espaces : RH n'y existe que là où un objet (un caractère) se tient derrière la fonction.
- **Le Chaînon et le Générateur** localisent le manque : l'opérateur et la symétrie se reconstruisent depuis les premiers ; manque la métrique positive, que l'objet d'en haut fournirait.
- **Le Temps de Heisenberg** dit que cet objet devrait agir à toutes les échelles de premiers à la fois, comme la tour à tous ses étages.
- **La Rencontre à trois et la Loi de la marge** : là où un objet est connu (courbes, premiers de Δ), il impose ensemble la positivité et la statistique « fréquence ∝ marge ». Pour les zéros de ζ et de Δ, cette statistique est mesurée.
- **Les Familles étrangères** sont un contre-témoin : deux objets superposés gardent la positivité mais perdent la répulsion mutuelle.

Tout cela est compatible avec l'hypothèse et la précise. Rien ne la démontre : l'objet plus grand, pour ζ, n'est pas construit. Chercher l'analogue de C × C pour les entiers est aussi le programme de Connes, Consani et d'autres.

## 16. Mini-glossaire

| Terme | Sens |
|---|---|
| ζ(s), zéro non trivial | La fonction zêta de Riemann ; ses zéros ρ = β + iγ dans la bande 0 < β < 1. |
| Droite critique, RH | La droite β = 1/2 ; RH affirme que tous les zéros non triviaux y sont. |
| Λ(n) | Fonction de von Mangoldt : log p si n est une puissance de p, 0 sinon. |
| Produit d'Euler | Écriture de la fonction comme produit sur les nombres premiers ; DH n'en a pas. |
| Modèle réduit | Les courbes sur les corps finis, où RH est un théorème. |
| Tour, étage | La suite des corps à q^n^ éléments ; l'étage n. |
| Métrique | La matrice de Gram qui mesure les longueurs ; sa positivité dans toutes les fenêtres équivaut à RH (critère de Weil). |
| Marge | Ce qui reste de positivité avant de la perdre : plus petite valeur propre (forme), plus petite perturbation (objet), déterminant normalisé (paire). |
| Temps de Heisenberg | log(q·γ~0~/2π) : la fenêtre (longueur L = nh, pas h) qui résout l'écart moyen des zéros à la hauteur γ~0~. |
| GUE, CUE, Poisson | Statistiques de référence : matrices aléatoires (avec répulsion), ou points indépendants (sans). |
| Sato–Tate | Loi des angles θ~p~ aux premiers, de densité (2/π) sin²θ. |
| Surface virtuelle | La forme d'intersection d'une surface qu'on ne sait pas construire, calculée depuis les nombres premiers (doc. 46). |
| Indice de Hodge | Sur une vraie surface, une seule direction positive ; dans le Modèle réduit, c'est RH. |
| Fonction auxiliaire | Fonction qui s'annule fortement en tous les points ; elle borne leur nombre (Stepanov). |
| Frobenius | L'application x ↦ x^q^ d'une courbe sur F~q~ ; sa dérivée est nulle. |
| Rang–trace | Rang d'une matrice positive ≥ (trace)²/trace du carré ; la méthode des deux tiers. |

## 17. Ce que les images ne disent pas

1. **Elles ne disent pas pourquoi les zéros sont sur la droite.** Le thermomètre mesure, la métrique sépare, l'archipel situe. Aucune image ne contient la loi qui l'imposerait à ζ. Ce qui la porterait, l'objet plus grand, est une place vide.
2. **Elles ne disent rien au-delà de la fenêtre.** Chaque mesure sur ζ est faite à hauteur finie (1 500 au plus pour les marges). Le Temps de Heisenberg en dit le prix : chaque hauteur demande ses propres nombres premiers. La complétude, tous les zéros sans exception, reste hors d'atteinte d'un calcul fini.
3. **Elles ne transfèrent pas du modèle à l'original.** Le Modèle réduit a une dimension, une période et une géométrie que ζ n'a pas. Un pendant exact dans le modèle est une indication, pas un transfert.
4. **Elles ne remplacent pas la positivité par un nom.** « Métrique positive », « marge », « passage interdit » situent le verrou de Weil ; ils ne l'ouvrent pas.
5. **Elles n'ont pas toutes le même statut.** Théorème, mesure ou simple lecture : le tableau du §14 fait la différence ; une image ne la fait pas.
6. **Elles ne disent pas ce que suggèrent leurs mots physiques.** Rien ne « transite », aucune « température » n'agit : les zéros de ζ sont fixes. Seuls bougent la fenêtre, la hauteur ou le paramètre d'une famille.
7. **Elles ne remplacent pas la relecture.** Les Théorèmes A et B, et le corollaire B′, attendent un spécialiste. Les noms ajoutés au registre depuis la V6.0 sont des propositions, à arbitrer.

**En une phrase.** Le programme sait construire des instruments qui lisent exactement où sont les zéros, et il a mesuré, là où RH est démontrée, à quoi ressemble ce qui la rend nécessaire ; il ne sait pas construire, pour ζ, l'objet qui porterait cette nécessité.

<!-- references:debut -->

## Références

Format : [clé] auteurs, *titre*, publication, lien. Fiches complètes et état de vérification : document 42 (registre des sources).

- [AF26] L. Alpöge, R. Furman. *More than two thirds of the zeros of the Riemann zeta function are simple and on the critical line*. arXiv:2608.13637 (août 2026). <https://arxiv.org/abs/2608.13637> — vérifié en ligne
- [BBLM06] E. Bogomolny, O. Bohigas, P. Leboeuf, A. G. Monastra. *On the spacing distribution of the Riemann zeros: corrections to the asymptotic result*. J. Phys. A 39 (2006), 10743–10754 ; arXiv:math/0602270. <https://arxiv.org/abs/math/0602270> — vérifié en ligne
- [Beu55] A. Beurling. *A closure problem related to the Riemann zeta-function*. Proc. Natl. Acad. Sci. USA 41 (1955), 312–314. <https://www.pnas.org/doi/pdf/10.1073/pnas.41.5.312> — vérifié en ligne
- [BGHT11] T. Barnet-Lamb, D. Geraghty, M. Harris, R. Taylor. *A family of Calabi–Yau varieties and potential automorphy II*. Publ. RIMS 47 (2011), 29–98 ; DOI 10.2977/PRIMS/31. <https://ems.press/journals/prims/articles/4468> — vérifié en ligne
- [Bir68] B. J. Birch. *How the number of points of an elliptic curve over a fixed prime field varies*. J. London Math. Soc. 43 (1968), 57–60. <https://academic.oup.com/jlms/issue/s1-43/1> — vérifié en ligne
- [BK99a] M. V. Berry, J. P. Keating. *H = xp and the Riemann zeros*. dans Supersymmetry and Trace Formulas: Chaos and Disorder (Kluwer, 1999) ; rapport HP Labs 97-27 (1997). — vérifié en ligne
- [BT14] A. R. Booker, F. Thorne. *Zeros of L-functions outside the critical strip*. Algebra Number Theory 8 (2014), no. 9, 2027–2042 ; DOI 10.2140/ant.2014.8.2027 ; arXiv:1306.6362 ; correction ANT 8:9. <https://arxiv.org/abs/1306.6362> — vérifié en ligne
- [Bur02] J.-F. Burnol. *A lower bound in an approximation problem involving the zeros of the Riemann zeta function*. Adv. Math. 170 (2002), 56–70 ; arXiv:math/0103058. <https://arxiv.org/abs/math/0103058> — vérifié en ligne
- [CCM25] A. Connes, C. Consani, H. Moscovici. *Zeta spectral triples*. arXiv:2511.22755 (27 nov. 2025). <https://arxiv.org/abs/2511.22755> — vérifié en ligne. **Correctif V6.18 :** Le titre est « Zeta spectral triples » ; le résumé parle d'une réalisation spectrale des zéros, pas explicitement de formes de Weil tronquées.
- [Con99] A. Connes. *Trace formula in noncommutative geometry and the zeros of the Riemann zeta function*. Selecta Math. (N.S.) 5 (1999), 29–106 ; arXiv:math/9811068. <https://arxiv.org/abs/math/9811068> — vérifié en ligne
- [DeB50] N. G. de Bruijn. *The roots of trigonometric integrals*. Duke Math. J. 17 (1950), 197–226. <https://en.wikipedia.org/wiki/De_Bruijn%E2%80%93Newman_constant> — partiellement vérifié
- [Del74] P. Deligne. *La conjecture de Weil. I*. Publ. Math. IHÉS 43 (1974), 273–307 ; DOI 10.1007/BF02684373. <https://www.numdam.org/item/PMIHES_1974__43__273_0/> — vérifié en ligne
- [DH36a] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series*. J. London Math. Soc. 11 (1936), no. 3, 181–185. <https://doi.org/10.1112/jlms/s1-11.3.181> — partiellement vérifié
- [DH36b] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series. II*. J. London Math. Soc. 11 (1936), no. 4, 307–312. <https://doi.org/10.1112/jlms/s1-11.4.307> — partiellement vérifié
- [Dys62] F. J. Dyson. *Statistical theory of the energy levels of complex systems. I–III*. J. Math. Phys. 3 (1962), 140–156, 157–165, 166–175. <https://doi.org/10.1063/1.1703773> — partiellement vérifié
- [Had96] J. Hadamard ; Ch.-J. de la Vallée Poussin. *Sur la distribution des zéros de la fonction ζ(s) et ses conséquences arithmétiques ; Recherches analytiques sur la théorie des nombres premiers*. Bull. SMF 24 (1896), 199–220 ; Ann. Soc. Sci. Bruxelles 20 (1896), 183–256 (non vérifiés). <https://people.math.harvard.edu/~elkies/M259.06/free.pdf> — partiellement vérifié. **Correctif V6.18 :** Le théorème est d'Hadamard et de la Vallée Poussin (1896) ; l'inégalité 3 + 4 cos x + cos 2x ≥ 0 est la version de Mertens (1898) [Mer98].
- [Ham21] H. Hamburger. *Über die Riemannsche Funktionalgleichung der ζ-Funktion*. Math. Z. 10 (1921), 240–254. <https://gdz.sub.uni-goettingen.de/download/pdf/PPN266833020_0010/PPN266833020_0010.pdf> — vérifié en ligne
- [Has36] H. Hasse. *Zur Theorie der abstrakten elliptischen Funktionenkörper I, II, III*. J. reine angew. Math. 175 (1936) ; DOI 10.1515/crll.1936.175.193. <https://doi.org/10.1515/crll.1936.175.193> — partiellement vérifié
- [Hay68] E. V. Haynsworth. *Determination of the inertia of a partitioned Hermitian matrix*. Linear Algebra Appl. 1 (1968), 73–81. <https://en.wikipedia.org/wiki/Haynsworth_inertia_additivity_formula> — partiellement vérifié
- [Kal60] R. E. Kalman. *A new approach to linear filtering and prediction problems*. J. Basic Eng. 82 (1960), 35–45. <https://www.cs.unc.edu/~welch/kalman/kalmanPaper.html> — partiellement vérifié
- [Kar31] J. Karamata. *Neuer Beweis und Verallgemeinerung der Tauberschen Sätze, welche die Laplacesche und Stieltjessche Transformation betreffen*. J. reine angew. Math. 164 (1931), 27–39. — non vérifié
- [Lam26] Y. Lamzouri. *A new proof that more than 2/3 of the zeros of the Riemann zeta function are simple and on the critical line*. arXiv:2609.02882 (sept. 2026). <https://arxiv.org/abs/2609.02882> — vérifié en ligne
- [Leh56] D. H. Lehmer. *On the roots of the Riemann zeta-function*. Acta Math. 95 (1956), 291–298. <https://en.wikipedia.org/wiki/Lehmer_pair> — partiellement vérifié
- [Lev47] N. Levinson. *The Wiener RMS (root mean square) error criterion in filter design and prediction*. J. Math. Phys. 25 (1947), 261–278 ; amélioré par J. Durbin, Rev. Inst. Int. Stat. 28 (1960), 233–243. <https://en.wikipedia.org/wiki/Levinson_recursion> — partiellement vérifié
- [Mon73] H. L. Montgomery. *The pair correlation of zeros of the zeta function*. Analytic Number Theory, Proc. Sympos. Pure Math. 24, AMS (1973), 181–193. <https://public.websites.umich.edu/~hlm/paircor1.pdf> — vérifié en ligne
- [MT58] A. Mattuck, J. Tate. *On the inequality of Castelnuovo–Severi*. Abh. Math. Sem. Univ. Hamburg 22 (1958), 295–299 (volume et pages non confirmés en ligne). <https://arxiv.org/abs/1210.7459> — partiellement vérifié
- [New76] C. M. Newman. *Fourier transforms with only real zeros*. Proc. Amer. Math. Soc. 61 (1976), 245–251. <https://en.wikipedia.org/wiki/De_Bruijn%E2%80%93Newman_constant> — partiellement vérifié
- [Nym50] B. Nyman. *On the one-dimensional translation group and semi-group in certain function spaces*. Thèse, Université d'Uppsala, 1950. — partiellement vérifié
- [Ram16] S. Ramanujan. *On certain arithmetical functions*. Trans. Cambridge Philos. Soc. 22 (1916), 159–184. <https://encyclopediaofmath.org/wiki/Ramanujan_function> — partiellement vérifié
- [RT20] B. Rodgers, T. Tao. *The De Bruijn–Newman constant is non-negative*. Forum Math. Pi 8 (2020), e6 ; arXiv:1801.05914. <https://arxiv.org/abs/1801.05914> — vérifié en ligne
- [Sel56] A. Selberg. *Harmonic analysis and discontinuous groups in weakly symmetric Riemannian spaces with applications to Dirichlet series*. J. Indian Math. Soc. 20 (1956), 47–87. <https://informaticsjournals.com/index.php/jims/article/view/16985> — partiellement vérifié
- [SW09] É. Saias, A. Weingartner. *Zeros of Dirichlet series with periodic coefficients*. Acta Arith. 140 (2009), no. 4, 335–344 ; DOI 10.4064/aa140-4-4 ; arXiv:0807.0783. <https://arxiv.org/abs/0807.0783> — vérifié en ligne
- [Tit37] E. C. Titchmarsh. *Introduction to the Theory of Fourier Integrals*. Oxford, Clarendon Press, 1937. — non vérifié
- [Wei48] A. Weil. *Sur les courbes algébriques et les variétés qui s'en déduisent*. Actualités Sci. Ind. 1041, Hermann, Paris (1948). <https://denisevellachemla.eu/Weil-courbes-varietes.pdf> — partiellement vérifié. **Correctif V6.18 :** Le mémoire Sur les courbes… établit directement la positivité par correspondances, intersections et Riemann–Roch. La fiche précédente le résumait trop exclusivement par la jacobienne ; ne pas confondre ce mémoire et celui sur les variétés abéliennes.
- [Wei52] A. Weil. *Sur les « formules explicites » de la théorie des nombres premiers*. Comm. Sém. Math. Univ. Lund, vol. suppl. dédié à M. Riesz (1952), 252–265. <https://en.wikipedia.org/wiki/Weil%27s_criterion> — partiellement vérifié
- [Wey12] H. Weyl. *Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller Differentialgleichungen*. Math. Ann. 71 (1912), 441–479 (non vérifié). — non vérifié
- [Wey39] H. Weyl. *The Classical Groups: Their Invariants and Representations*. Princeton University Press (1939). <https://press.princeton.edu/books/paperback/9780691057569/the-classical-groups> — partiellement vérifié

<!-- references:fin -->
