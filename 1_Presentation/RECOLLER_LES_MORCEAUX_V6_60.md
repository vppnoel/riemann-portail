# V6.60 — Recoller les morceaux : une échelle vers la preuve, par nos propres moyens

**Document de travail · 22 novembre 2026 · numéro 83 proposé, à attribuer par l’auteur à l’acceptation**  
**Auteur :** Vincent P. P. NOËL · Programme Riemann  
**Statut :** plan de recherche, avec un premier calcul fait (niveau 0, §5) et sa prévision écrite avant (`3_Preuves_et_calculs/data/prevision_v660_echelle.md`). Deux prévisions justes, une fausse. La lecture de la preuve d'Alpöge est **secondaire** : elle s'appuie sur les premières expositions publiées (Rubinstein, Zhang, guide d'architecture), pas sur une lecture du code Lean. Elle est soumise à la vérification adverse de TAC-010.  
**Demande de l'auteur :** « Comment on produit un document qui recolle les morceaux pour aller vers la preuve par nos propres moyens ? »

## 1. La question, et ce qu'on peut honnêtement viser

Le 20 novembre 2026, L. Alpöge a annoncé une preuve de l'hypothèse de Riemann généralisée, obtenue avec Claude et vérifiée par machine (voir `NOTE_ALPOGE_2026.md`). Sa version lisible par un humain dépasserait 250 000 pages. Elle mobilise des outils de spécialiste : relèvements thêta, périodes de formes automorphes sur un corps CM, formule de Chowla–Selberg, inégalité de pente de Bost, théorie d'Iwasawa.

**Refaire cette preuve par nos propres moyens n'est pas un objectif réaliste.** Ce que l'on peut faire, c'est autre chose, et c'est ce que le corpus fait depuis le début : **reconstruire le mécanisme à des échelles de plus en plus grandes**, en vérifiant à chaque échelle qu'il marche, pourquoi il marche, et ce qui manque pour passer à la suivante. Le document 59 l'a déjà fait pour les courbes elliptiques. Le but n'est pas de redémontrer RH, mais de **comprendre pourquoi elle est vraie** : c'est la question de l'hypothèse de travail.

## 2. La preuve en quatre étages, et les pièces que le corpus possède déjà

Le document 47 avait dressé, pour ζ, la liste des pièces de la preuve de Stepanov–Bombieri pour les courbes. La preuve annoncée suit cette architecture. Voici, étage par étage, ce qu'elle fait et ce que le corpus a déjà.

| Étage | Ce que fait la preuve (lecture secondaire) | Ce que le corpus a déjà | Où |
|---|---|---|---|
| **1. Des zéros aux premiers** | Un zéro de partie réelle θ > ½ force une somme lissée de Λ(n) à dépasser x^θ ; il suffit donc d'une **majoration** (théorème de Landau, localisé). Une famille de fonctions L à poids positifs empêche les compensations. | Landau comme analogue de Pringsheim ; Λ ≥ 0 ; pas de zéro réel ; théorème A, qui lit Θ sur la croissance de Q(X). | doc. 47 §4 ; théorème A |
| **2. La majoration vient des entiers** | Un entier non nul ne peut pas être à la fois petit et très divisible : Σ_p e_p log p ≤ log\|Δ\|. Des périodes entières encodent la somme sur les premiers par leur divisibilité en chaque p ; leur taille est calculable. | L'obstacle exactement posé : la propriété du Frobenius existe « pour chaque premier séparément, mais pas pour tous à la fois ». La formule du produit est la colle qui recolle les premiers un par un. | doc. 49 §2 |
| **3. La multiplicité est fabriquée** | Un seul relèvement ne donne pas assez de divisibilité ; une chaîne de m relèvements additionne les gains, comme la fonction auxiliaire de Stepanov qui s'annule à un ordre élevé. | La fonction auxiliaire de Stepanov construite en algèbre linéaire exacte ; l'effondrement du rang des conditions ; le lemme des jets. | docs 48, 58 |
| **4. L'équilibre en √x, et la tour** | Les deux erreurs principales valent x/m et m ; elles s'équilibrent pour m ≈ √x, d'où l'exposant ½. La tour cyclotomique remplace la tour des extensions des constantes. | La chaîne complète « jets → rang → multiplicité → tour → spectre » pour les cubiques, jusqu'à la borne de Hasse exacte. | doc. 59 |

**Ce qui manquait au corpus, dit simplement.** Le document 47 notait deux pièces manquantes : un « Frobenius absolu » agissant sur tous les premiers, et une tour d'extensions (« Spec Z n'a pas d'extensions des constantes »). La preuve annoncée n'a construit ni l'un ni l'autre sous cette forme. Elle a **contourné** le premier, en travaillant premier par premier et en recollant par l'intégrité. Elle a **remplacé** le second, par la tour cyclotomique. Le document 51 avait cherché la première pièce chez Connes–Consani, ne l'y avait pas trouvée, et avait ramené l'axe J vers la route de Weil.

## 3. La voie en blocs, en logique humaine

L'auteur demande si l'on peut expliquer la voie avec des idées simples, en se servant des blocs que le corpus a déjà construits. Voici une tentative : sept blocs, chacun dit d'abord dans la langue de tous les jours, puis rattaché à son nom dans le corpus (registre des métaphores, doc. 20) et à l'étage de la preuve. C'est une **interprétation**, pas une démonstration ; elle hérite des limites de la lecture secondaire du §2.

| Bloc | L'idée, dite simplement | Son nom dans le corpus | Étage |
|---|---|---|---|
| **1. La nacelle se voit d'en bas** | Un zéro qui quitte la droite, c'est une nacelle du **Carrousel** qui s'élève. On ne la voit pas directement, mais elle donne de la fièvre aux nombres premiers : leur écart à la moyenne grandit comme x^θ. | Le Carrousel ; le Thermomètre (théorème A) | 1 |
| **2. Un plafond suffit** | Pour prouver qu'il n'y a pas d'incendie, inutile de connaître la température exacte : il suffit de montrer qu'elle ne dépasse jamais un plafond. Comme les premiers ne se comptent qu'avec des signes positifs, une borne **d'un seul côté** suffit (Landau). | Le Thermomètre, lu comme thermomètre à maximum | 1 |
| **3. La population plutôt que l'individu** | Un seul zéro pourrait se cacher derrière un autre. Une foule de fonctions, chacune comptée positivement, ne peut pas se compenser : on surveille la population entière. | Le Microscope de population | 1 |
| **4. Le sac qui ne peut pas mentir** | Un sac de contenance connue ne peut pas contenir plus de billes qu'il n'en tient. De même, un entier de taille connue ne peut pas être divisible par trop de nombres premiers. Si les premiers étaient trop nombreux, un certain entier serait trop divisible pour sa taille. | Nouveau bloc ; voisin du **verrou premier** (PRIME-LOCK) ; calculé au niveau 0 (§5) | 2 |
| **5. Le zoom** | Le sac de Tchebychev est trop grand : il contient aussi beaucoup de petites billes inutiles (39 % au niveau 0). On le resserre en zoomant : répéter la construction m fois multiplie les billes utiles plus vite que les inutiles. C'est la fonction auxiliaire de Stepanov, qui s'annule à un ordre élevé. | La **Loupe double**, généralisée en loupe d'ordre m ; docs 48, 58 | 3 |
| **6. Le bon réglage du zoom** | Un zoom améliore l'image jusqu'au moment où le grain du capteur domine. Le meilleur réglage est à m ≈ √x. C'est de là que vient le ½ : la droite critique n'est pas une frontière arbitraire, c'est **le réglage optimal du zoom**. | La tour du doc. 59, où le même équilibre donne √q | 4 |
| **7. Le Sosie n'a pas de sac** | Davenport–Heilbronn a le même visage que ζ, mais pas de produit d'Euler. Ses « premiers » ne sont encodés dans aucun entier : les blocs 4 à 6 ne peuvent même pas commencer. C'est cohérent avec ses zéros hors de la droite. | Le **Sosie**, jumeau de crash-test ; l'Archipel d'Euler (doc. 30) | témoin |

**La chaîne en une phrase.** Si une nacelle s'élevait (1), les premiers auraient de la fièvre ; pour l'exclure, un plafond suffit (2), surveillé sur toute une population (3) ; le plafond vient d'un sac qui ne peut pas mentir sur sa contenance (4), resserré par un zoom (5), dont le réglage optimal donne exactement ½ (6). Le Sosie, qui n'a pas de sac, échoue, comme il doit (7).

**Où cette chaîne a déjà été vue en entier.** Dans le **Modèle réduit** : pour les courbes sur 𝔽_q, les blocs 1 à 6 sont la preuve de Stepanov–Bombieri, que le corpus a refaite (docs 47, 48, 58, 59). Le Modèle réduit était donc bien la maquette de la vraie preuve ; le corpus l'a lu, en V6.26, comme la maquette d'une autre preuve, celle du carré.

**Ce qui reste sans bloc humain.** Le **sac** lui-même. Pour les courbes, c'est l'espace des fonctions sur la courbe, et l'on voit pourquoi les points y sont encodés. Pour ζ, ce sont des périodes de formes automorphes : la preuve montre qu'elles conviennent, mais nous n'avons pas encore d'image simple de **pourquoi** ces entiers-là encodent les nombres premiers. C'est la nouvelle forme de la **Scène manquante** : ce n'est plus le théâtre d'un carré qui manque, c'est l'intuition du sac.

## 4. L'échelle

Chaque niveau reprend les quatre étages avec un objet plus riche. On ne passe au suivant qu'après avoir écrit ce qui manque.

| Niveau | Objet | Étages réalisés | État | Ce qu'on apprend |
|---|---|---|---|---|
| **0** | Le coefficient binomial C(2n, n) (Tchebychev, 1852) | 2 seulement | **fait ici (§4)** | L'intégrité seule donne une majoration des premiers, mais avec une erreur d'ordre x, pas √x. |
| **1** | Rapports de factorielles plus riches (Tchebychev, Sylvester ; limites de Diamond–Erdős, à vérifier sur l'original) | 2, plus un début de 3 | à faire | Jusqu'où l'intégrité **sans multiplicité** peut aller. Prévision à écrire : la constante s'améliore, l'ordre de l'erreur ne change pas. |
| **2** | Les courbes sur 𝔽_q (Stepanov–Bombieri) | 1, 2, 3, 4 | **fait (docs 47, 48, 58, 59)** | Le mécanisme complet. À ajouter : vérifier que le paramètre optimal de multiplicité croît comme √q, c'est-à-dire que l'équilibre de l'étage 4 est le même. |
| **3** | Une famille de fonctions L de Dirichlet et le théorème A | 1 | à faire | Écrire la localisation de Landau avec les objets du corpus : la somme lissée, les poids positifs de famille, et Q(X). C'est le seul étage de la vraie preuve accessible sans outil de spécialiste. |
| **4** | Les périodes automorphes et les relèvements thêta | 2, 3 | **hors de nos moyens** | Lecture seulement : dresser, section par section du guide, le dictionnaire entre la preuve et les niveaux 0 à 3. |

**Pourquoi cet ordre.** Le niveau 0 montre la colle (l'intégrité) dans sa forme la plus simple. Le niveau 2 montre la multiplicité là où elle est déjà démontrée. Le niveau 3 montre le premier étage pour ζ elle-même. Entre les trois, il ne manque que l'objet du niveau 4 : un entier qui soit à la fois **assez divisible** et **assez multiple**. C'est exactement ce que les outils de spécialiste fournissent.

## 5. Le niveau 0, calculé

**Le mécanisme.** L'entier C(2n, n) = (2n)!/(n!)² est divisible par chaque premier p de ]n, 2n], puisque p divise (2n)! mais pas (n!)². Donc le produit de ces premiers divise C(2n, n), et
  θ(2n) − θ(n) ≤ log C(2n, n) < 2n log 2,
où θ(x) = Σ_{p ≤ x} log p. En sommant sur les puissances de 2, on obtient θ(x) < 2 log 2 · x ≈ 1,386 x. C'est l'étage 2 de la preuve, sans les autres : un entier de taille connue ne peut pas être trop divisible.

**Les résultats** (script `3_Preuves_et_calculs/run_v660_niveau0.py`, entiers jusqu'à 400 000, quelques secondes) :

| | Prévision | Résultat | Verdict |
|---|---|---|---|
| P1 | aucune exception à θ(2n) − θ(n) ≤ log C(2n, n) pour n ≤ 200 000 | 0 exception | **juste** (contrôle du code) |
| P2 | rapport maximal θ(x)/x entre 1,0 et 1,1, loin de 1,386 | maximum **0,9993** : θ(x) reste sous x dans tout l'intervalle | **fausse** pour la fourchette ; juste sur le fond (la borne est grossière) |
| P3 | le « gaspillage » log C(2n, n) − (θ(2n) − θ(n)) est d'ordre n, rapport entre 0,3 et 0,7 | rapport stable à **0,387** ; rapporté à √n, il croît (39 à 173) | **juste** |

**Ce qu'on apprend.**
1. **La colle marche, mais elle gaspille.** Environ 39 % de la divisibilité de C(2n, n) ne vient pas des premiers que l'on veut compter, mais des petits premiers. Ce gaspillage est d'ordre n. C'est pourquoi l'intégrité seule donne une erreur d'ordre x et non √x.
2. **C'est la raison d'être de la multiplicité**, dans la lecture du §2. Pour descendre de x à √x, il faut que l'objet entier soit **très** divisible par les premiers voulus et **peu** par les autres. Une chaîne de m relèvements, comme une fonction auxiliaire d'ordre m, augmente la divisibilité utile plus vite que le gaspillage. L'équilibre se fait à m ≈ √x.
3. **La prévision P2 était fausse dans sa fourchette**, parce que θ(x) < x pour tous les x calculés. C'est un fait connu (θ(x) < x jusqu'à des hauteurs considérables), que je n'avais pas en tête en écrivant la prévision.

## 6. Les questions où le corpus peut apporter quelque chose de neuf

La preuve dit **que** RH est vraie. Les questions suivantes portent sur le **pourquoi**, et restent ouvertes.

1. **La simplicité des zéros.** Le corollaire B′ devient : la limite de Q(X)/(log X)³ vaut 4κ/3 si et seulement si tous les zéros sont simples. Le mécanisme de la preuve (divisibilité et multiplicité) dit-il quelque chose de la multiplicité des **zéros** ? Une piste concrète : comparer la multiplicité fabriquée (étage 3) avec les marges de la Rencontre à trois (doc. 40).
2. **L'exposant ½ comme équilibre.** Si ½ est le point d'équilibre entre coût et gain de la multiplicité, l'Archipel d'Euler (doc. 30) et le temps de Heisenberg (doc. 38) devraient montrer le même équilibre. À tester au niveau 2, puis au niveau 3.
3. **Le relief de l'Archipel.** Davenport–Heilbronn n'a pas de produit d'Euler, donc pas d'entiers qui encodent ses « premiers ». Le niveau 0 appliqué aux coefficients de DH devrait échouer dès l'étage 2. C'est un test simple à écrire.

## 7. Méthode

- **Une seule voie active** : cette échelle. Les autres fiches sont gelées en l'état, sans rien supprimer.
- **Une fiche par niveau**, avec prévision avant calcul et critère de rejet. Au plus deux fiches actives à la fois.
- **Ordre proposé** : niveau 1 (rapports de factorielles), puis le test DH du §6.3, puis le niveau 3 (Landau localisé). Le niveau 4 reste une lecture, menée par l'auteur.
- **La relecture humaine** reste le coup le plus rentable. Elle porte désormais aussi sur la lecture secondaire du §2.

## 8. Démontré, mesuré, supposé

| | Énoncé |
|---|---|
| **Démontré (classique)** | La majoration de Tchebychev par C(2n, n) ; la preuve de Stepanov–Bombieri pour les courbes ; le théorème de Landau. |
| **Mesuré** | Niveau 0 : aucune exception jusqu'à 400 000 ; gaspillage d'ordre n, de rapport 0,387. |
| **Supposé** | Que la preuve annoncée suive les quatre étages décrits au §2 (lecture secondaire, soumise à TAC-010) ; que l'équilibre en √x soit le même aux niveaux 2 et 3. |

## 9. Lecture selon l'hypothèse de travail

L'hypothèse de travail disait : RH n'existe que parce qu'elle est nécessaire à quelque chose de plus grand. Le niveau 0 montre la plus petite forme de cette chose plus grande : **les nombres premiers sont encodés dans des entiers, et un entier ne peut pas mentir sur sa taille**. Le reste de l'échelle consiste à comprendre comment cette contrainte, presque triviale pour C(2n, n), devient exacte lorsqu'on sait fabriquer assez de multiplicité. Ce n'est pas un carré qui manquait (doc. 80), ou pas seulement : c'était une **multiplicité recollée premier par premier**.

## Annexe A — Le guide d'architecture face au corpus

*Ajoutée le 22 novembre 2026 à la demande de l'auteur (« Guide de l'architecture de la preuve… versus corpus »). Source : L. Alpöge, guide de l'architecture de la preuve, https://nasqret.github.io/riemann-rev/guide/proof-guide.pdf. Le guide précise lui-même que ses §§4 à 7 sont lus dans le code Lean et l'annonce, non redémontrés. Les rapprochements ci-dessous sont ceux de Claude, soumis à TAC-010.*

| Section du guide | Ce qu'elle fait | Ce que le corpus a | Verdict |
|---|---|---|---|
| **Analogie de Stepanov** | annuler à l'ordre m → divisibilité d'une chaîne de m relèvements ; compter les degrés → inégalité de pente de Bost ; extensions de 𝔽 → tour cyclotomique ; « une borne d'un côté suffit » → Landau | docs 47, 48, 58, 59 : la même liste de pièces, dont deux « manquantes » | **même charpente** |
| **§1 Réflexion** | facteurs d'Euler et équation fonctionnelle : il suffit de traiter Re s > ½ et les caractères primitifs | Archipel d'Euler (doc. 30), symétrie de Hardy | **possédé** (classique) |
| **§2 La statistique** | G(y) = Σ Λ(n)(y/n − 1) − y(log y − 1 − γ), somme « en rampe » ; sous RH, \|G − log 2π\| ≤ 0,0462 √y | 0,0462 est **κ = 2 + γ − log 4π**, la « Note fondamentale » ; le doc. 77 utilise déjà des rampes (t − τ_q)₊ (signal de Suzuki) | **très proche** |
| **§3 Landau localisé** | un zéro à droite de θ force G > C·y^θ dans **chaque fenêtre** [Y, Y^(3/2)] ; poids positifs ; dérivées d'ordre élevé pour localiser ; un seul côté suffit | théorème A : la même idée, mais **globale** (limsup) et sans familles ; doc. 38 : la notion de fenêtre | **partiel** : il manque la localisation |
| **§4 Chaîne de relèvements thêta** | divisibilité aux places finies ; formule du produit et pente de Bost ; périodes aux places infinies (Chowla–Selberg) ; erreur x/m + m + √x, optimum m ≍ √x | le mécanisme dans le Modèle réduit (docs 48, 58, 59) et au niveau 0 (§5) | **le mécanisme oui, l'objet non** |
| **§5 Moyenne sur les caractères** | positivité **construite** (poids 1 et 1/(3o + 1)) ; caractères tordus éliminés ; ensemble épais de Behrend ; le « 9 » de la borne vient d'un bilan des pertes | doc. 30 combine aussi des caractères, mais **les fonctions L elles-mêmes**, ce qui brise le produit d'Euler | **différence instructive** (A.3) |
| **§6 Iwasawa** | le « prix » de la divisibilité, un défaut cohomologique, borné dans la même tour (Ferrero–Washington, Poitou–Tate) | rien ; les « dettes » du doc. 70 et de TAC-003 n'ont qu'un nom en commun | **absent** |
| **§7 Représentations galoisiennes** | le socle automorphe (Harris–Taylor, Shin, Chenevier–Harris, Caraiani) | rien | **absent**, hors de portée |

**A.1. κ est la constante de la cible.** Sous RH, la statistique du guide reste dans ±κ·√y. C'est le κ du corollaire B′ (4κ/3) : κ = Σ 1/|ρ|² est la somme des résidus de tous les zéros, avec une rampe (pôles simples) dans le guide et la Loupe double (pôles doubles) dans le corpus. Le Thermomètre et la statistique du guide sont des **cousins** : même famille d'objets, ordre des pôles différent.

**A.2. Le théorème A est la version globale du §3.** Le théorème A lit Θ sur la croissance de Q à l'infini. Le §3 voit un zéro hors de la droite dans chaque fenêtre tardive, parce que la construction arithmétique n'existe qu'à des échelles spéciales (§6 du guide). Localiser le théorème A sur des fenêtres est le niveau 3 de l'échelle (§4).

**A.3. L'Archipel et le §5 du guide font le contraire l'un de l'autre.** L'Archipel additionne des **fonctions L** : le produit d'Euler se brise et RH devient fausse hors des points d'Euler (Saias–Weingartner). Le guide additionne leurs **dérivées logarithmiques**, donc leurs zéros, avec des poids positifs : chaque fonction garde son produit d'Euler, et aucun zéro ne peut en compenser un autre. L'Archipel montrait pourquoi il ne fallait pas mélanger les fonctions ; la preuve mélange leurs zéros.

**A.4. Ce qui en découle pour l'échelle.** À portée : localiser le théorème A sur des fenêtres (niveau 3) ; refaire au niveau 0 un bilan des pertes analogue à celui du §5 du guide, pour comprendre d'où vient chaque morceau de l'exposant. Hors de portée : §4c, §6, §7 du guide, que l'on peut seulement lire et nommer.

## Sources

- L. Alpöge, annonce et formalisation Lean (20 novembre 2026) ; voir `NOTE_ALPOGE_2026.md` pour les liens et l'état de la vérification.
- M. Rubinstein et al., exposition de la preuve pour ζ (brouillon, 21 novembre 2026) : https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/zeta-paper.pdf
- R. Zhang, note préliminaire (21 novembre 2026) : https://www.ihes.fr/~rzhang/files/GRH%20note.pdf
- L. Alpöge, guide de l'architecture de la preuve (« Its architecture: the statements, the flow, and why each idea calls for the next ») : https://nasqret.github.io/riemann-rev/guide/proof-guide.pdf
- P. Tchebychev, *Mémoire sur les nombres premiers* (1852) ; S. A. Stepanov (1969) et E. Bombieri (1973), fiches du registre des sources (document 42) ; H. Diamond et P. Erdős, sur les méthodes de Tchebychev (1980, à vérifier sur l'original avant usage).

---

*Usage d'IA : rédigé avec Claude à partir du corpus et des expositions publiées, à la demande de l'auteur.*
