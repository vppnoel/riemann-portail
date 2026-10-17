# V6.41 — Collisions, opérateurs locaux et limites de la voie globale

**Statut.** Note de relecture critique rédigée avant les nouveaux calculs de
collisions. Les identités et le théorème local ci-dessous sont analytiques.
L'existence des collisions recherchées dans V13, leur exhaustivité dans une
fenêtre, et toute implication vers RH restent à distinguer de ces identités.
Les observations numériques seront consignées dans les données V6.41 avec
leurs échecs et leur protocole verrouillé.

## 1. La surface des zéros et le choix des coordonnées

Dans l'espace réel des six caractères impairs modulo 13, les phases de Gauss
fixées en V6.39 permettent d'écrire

\[
 F_c(s)=\sum_{j=1}^6 c_j z_j L(s,\chi_j),\qquad c_j\in\mathbb R.
\]

La complétion commune vérifie la symétrie par réflexion autour de la droite
critique. Sur cette droite, on utilise la normalisation de Hardy

\[
 Z_c(t)=e^{i\theta(t)}F_c(\tfrac12+it)\in\mathbb R,
 \quad
 \theta(t)=\Im\log\Gamma(\tfrac34+it/2)
             +\tfrac t2\log(13/\pi).
\]

Cette normalisation enlève le module très petit du facteur Gamma sans changer
les zéros. Les dérivées de phase sont nécessaires :

\[
 \theta'(t)=\tfrac12\Re\psi(\tfrac34+it/2)+\tfrac12\log(13/\pi),
 \qquad
 \theta''(t)=-\tfrac14\Im\psi_1(\tfrac34+it/2).
\]

La variable naturelle de l'image est
\(\tau=-i(s-\tfrac12)\). Une valeur réelle de \(\tau\) représente un zéro
critique ; une paire conjuguée non réelle représente deux zéros de même
hauteur, réfléchis autour de la droite critique. Une collision est un pli de
la surface \(Z(r,\tau)=0\) au-dessus du paramètre \(r\), et non une
discontinuité de la fonction analytique.

Un facteur analytique non nul ne change ni le diviseur local ni le rapport
\(-2Z_r/Z_{tt}\) à une collision. Il change les dérivées ailleurs. On ne doit
donc pas mélanger des dérivées issues de normalisations différentes dans un
même jet. La continuation holomorphe de la phase de Hardy est locale ; pour
de grands contours on privilégie \(F(\tfrac12+i\tau)\), ou la complétion
entière, afin de ne pas introduire les singularités artificielles de cette
normalisation.

## 2. Réduire une recherche de collision à un Wronskien

Les six familles signées issues des recettes gelées V6.39 ont la forme

\[
 c_\sigma(r)=\cos r\,e_i+\sigma\sin r\,u,
 \quad u_i=0,\quad\|u\|=1,\quad\sum_j u_jz_j=0,
 \quad\sigma\in\{-1,+1\}.
\]

Ainsi, pour \(X(t)=Z_{e_i}(t)\) et \(Y(t)=Z_u(t)\),

\[
 Z_\sigma(r,t)=\cos r\,X(t)+\sigma\sin r\,Y(t).
\]

Une collision critique vérifie \(Z_\sigma=\partial_tZ_\sigma=0\).
Elle implique

\[
 W(t):=X(t)Y'(t)-X'(t)Y(t)=0.
\]

Si \((X(t),Y(t))\ne(0,0)\), le rayon candidat est déterminé modulo
\(\pi\) par

\[
 \tan r=-X(t)/(\sigma Y(t)).
\]

La formule avec `atan2(-X, sigma Y)` traite aussi \(Y=0\) et le quadrant.
Elle est suivie du contrôle des bornes de rayon enregistrées et des deux
équations originales. Un zéro du Wronskien hors des bornes n'est pas une
collision de la famille étudiée. Si \(X=Y=0\), on ne doit pas diviser :
\(Z_r=0\), et la collision éventuelle est dégénérée pour le théorème suivant.

À une collision, l'identité

\[
 W'(t_*)=-\sigma Z_r(r_*,t_*)Z_{tt}(r_*,t_*)
\]

montre qu'un zéro simple du Wronskien correspond à un pli transverse,
une fois les autres équations et les bornes contrôlées. Elle se démontre en
inversant la rotation : \(X=-\sin r\,Z_r\),
\(\sigma Y=\cos r\,Z_r\), puis en dérivant deux fois en \(t\).

**Attention au contrôle de \(A\).** Le long de cette continuation,
\(A(r)=\cos r\,z_i\) varie avec \(r\). Seuls les deux signes au même rayon
partagent exactement \(A\). Une dérivée le long de cette courbe ne constitue
pas une comparaison à \(A\) constant dans toute la courbe.

## 3. Théorème du pli et jet de Hasse d'ordre deux

Supposons \(Z\) réel analytique dans \((r,t)\), avec continuation holomorphe
locale, et supposons

\[
 Z(r_*,t_*)=Z_t(r_*,t_*)=0,
 \qquad Z_r(r_*,t_*)Z_{tt}(r_*,t_*)\ne0.
\]

Le jet de Hasse d'ordre deux, en caractéristique zéro, est le jet de Taylor
avec les coefficients divisés par les factorielles :

\[
 Z(r_*+h,t_*+x)
  =Z_r h+\tfrac12Z_{tt}x^2
     +Z_{rt}hx+O(h^2)+O(x^3).
\]

Le rapport

\[
 \kappa=-2Z_r/Z_{tt},\qquad x^2\simeq\kappa h
\]

est un modèle de premier ordre du déploiement. Le signe de \(\kappa h\)
prévoit deux racines critiques réelles ou une paire hors ligne. Le symbole
\(\simeq\) ne doit pas être remplacé par une égalité exacte à rayon fini.

Pour l'énoncé exact, la préparation de Weierstrass donne, après translation,

\[
 Z=U(h,x)\,[x^2+a_1(h)x+a_0(h)],\qquad U(0,0)\ne0,
 \quad a_0(0)=a_1(0)=0.
\]

Avec \(\xi=x+a_1(h)/2\), on obtient

\[
 Z=U\,[\xi^2-\mu(h)],\qquad
 \mu(h)=a_1(h)^2/4-a_0(h),\quad
 \mu(0)=0,\quad\mu'(0)=\kappa\ne0.
\]

En effet, \(U(0,0)=Z_{tt}/2\) et
\(a_0'(0)=Z_r/U(0,0)\). Les coefficients sont réels pour \(h\) réel.
Dans un voisinage suffisamment petit, \(\mu>0\) donne exactement deux
racines critiques simples ; \(\mu<0\) donne exactement une paire conjuguée
hors ligne ; \(\mu=0\) donne la collision d'ordre deux. La paire est locale,
comptée avec multiplicité. Cette conclusion n'affirme rien sur les autres
zéros, à d'autres hauteurs ou sur une autre composante.

Le jacobien du système \((Z,Z_t)=0\), en variables \((r,t)\), a déterminant
\(Z_rZ_{tt}\). Sa non-annulation rend la collision isolée localement.
Un petit résidu numérique ne prouve pas cette non-annulation dans un
voisinage ; une validation par intervalles est un objectif séparé.

## 4. Un opérateur réel, et la place exacte de la positivité

L'algèbre locale du polynôme préparé est

\[
 \mathcal A_h=\mathbb R[\xi]/(\xi^2-\mu(h)).
\]

La multiplication par \(\xi\), dans la base \((\xi,1)\), a pour matrice

\[
 H_\mu=\begin{pmatrix}0&1\\\mu&0\end{pmatrix},
 \qquad H_\mu^2=\mu I.
\]

Elle encode les deux feuillets par ses valeurs propres
\(\pm\sqrt\mu\). Ce n'est pas un Hamiltonien physique : la correspondance
est une réalisation algébrique du diviseur local des zéros.

Prenons

\[
 J=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
 G_\mu=JH_\mu=\begin{pmatrix}\mu&0\\0&1\end{pmatrix}.
\]

Les deux identités

\[
 H_\mu^T J=JH_\mu,\qquad H_\mu^T G_\mu=G_\mu H_\mu
\]

sont exactes. \(J\) est de signature \((1,1)\), jamais positive.
\(G_\mu\) est positive définie si \(\mu>0\), indéfinie si \(\mu<0\),
et singulière si \(\mu=0\). Pour \(\mu>0\), les deux vecteurs propres ont
des signes opposés pour la forme \(J\). Leur réunion au point singulier
illustre une collision de signature indéfinie. Le compagnon nul en
discriminant est un bloc de Jordan non nul ; une métrique positive définie
qui le rendrait autoadjoint serait impossible, car un opérateur autoadjoint
en dimension finie est diagonalisable.

La positivité locale a donc un contenu réel, mais sa portée est circonscrite :
elle équivaut au côté réel de ce diviseur à deux zéros. Construire
\(G_\mu\) après connaissance de \(\mu\) ne prouve pas la positivité
arithmétique globale requise pour RH. Une preuve globale devrait construire
sa forme indépendamment d'une hypothèse préalable sur tous les zéros.

## 5. Rendre l'opérateur canonique avec des moments de contour

Si un contour en variable \(\tau\) isole exactement deux zéros et ne rencontre
aucun zéro sur son bord, alors

\[
 m_k=\frac1{2\pi i}\oint \tau^k\frac{f'(\tau)}{f(\tau)}\,d\tau,
 \quad m_0=2,\quad
 a=m_1/2,\quad
 \mu=m_2/2-m_1^2/4.
\]

Pour les deux zéros \(\tau_1,\tau_2\), comptés avec multiplicité,
\(a=(\tau_1+\tau_2)/2\) et
\(\mu=(\tau_1-\tau_2)^2/4\). L'opérateur

\[
 H=\begin{pmatrix}a&1\\\mu&a\end{pmatrix}
\]

réalise directement le diviseur isolé. Un même contour non nul sur le bord
permet de suivre les deux zéros ensemble, même quand les étiquettes
individuelles se croisent ou se perdent. Autour d'une collision, le paramètre
complexifié peut échanger les deux feuillets : la monodromie appartient au
modèle, elle ne doit pas être effacée par un tri arbitraire à chaque pas.

Les conditions du contour sont essentielles : un comptage numérique proche
de deux ne certifie pas \(m_0=2\). Il faut contrôler le bord, l'erreur de
quadrature et la variation avec le paramètre. Les moments d'un contour qui
contient trois zéros ne définissent pas ce compagnon à deux racines.
En variable \(s\), le carré de la séparation a le signe opposé ; confondre
\(s\) et \(\tau\) inverse le diagnostic critique/hors ligne.

## 6. Contrainte \(A\) et opérateur de jet empilé : audit

La proposition constructive de fibre est exacte sous les hypothèses
explicitement énoncées. Pour \(0<r<\pi/4\), le choix de signe
\(c_i=\cos r>0\) fixe une carte de l'espace projectif. En retirant la
coordonnée \(i\), \(M_i\) est la matrice réelle de taille \(2\times5\)
dont les colonnes sont \((\Re z_j,\Im z_j)^T\). Si elle est de rang deux,

\[
 b=(A-\cos r\,z_i)/\sin r,
 \qquad\eta=b^T(M_iM_i^T)^{-1}b.
\]

La fibre est une sphère \(S^2\) pour \(\eta<1\), un singleton pour
\(\eta=1\), et vide pour \(\eta>1\). L'ensemble des \(A\) faisables est
une ellipse affine. Le rayon zéro est un cas séparé, où seul \(A=z_i\)
est admis dans cette carte. « \(A\) arbitraire » signifie donc arbitraire
dans cet ensemble faisable, pas dans tout \(\mathbb C\).

L'opérateur empilé

\[
 C_i(t)=\begin{bmatrix}
 e_i^T\\\Re z^T\\\Im z^T\\Z(t)^T\\Z_t(t)^T
 \end{bmatrix},\quad
 b=\begin{bmatrix}\cos r\\\Re A\\\Im A\\0\\0\end{bmatrix}
\]

impose simultanément rayon, coefficient complexe et collision critique.
À rang cinq, la solution de norme minimale \(c_0=C_i^+b\) est orthogonale
au noyau de dimension un. Pour \(\nu=\|c_0\|^2<1\), les deux candidats
normalisés sont \(c_0\pm\sqrt{1-\nu}\,n\). Un singleton existe à
\(\nu=1\), aucun candidat à \(\nu>1\). En rang plus faible, la condition
\(b\in\operatorname{Im}C_i\) reste nécessaire. La multiplicité exactement
deux demande en plus \(Z_{tt}(t)^Tc\ne0\), et un pli demande de choisir
une courbe contrainte avec dérivée transverse non nulle.

Deux limites interdisent une généralisation abusive de la variation de D :
à bord d'ellipse il n'y a qu'un point ; si \(A=0\), alors \(D=1\)
identiquement sur toute fibre normalisée. Le fait de varier génériquement
à l'intérieur n'est pas une variation pour tout \(A\), ni un contraste
uniformément minoré à l'approche du bord ou de \(A=0\).

## 7. Protocole numérique et questions qui demeurent

Le protocole parent fixe les familles, les six branches héritées de V6.40,
les intervalles de rayon et de hauteur, le pas du scan Wronskien, les
tolérances de validation, et les raffinements avant tout nouveau résultat.
Les contrôles pertinents sont les suivants :

1. Conserver la recette analytique gelée ; les coefficients binary64 ne
   servent qu'à localiser, puis leur perturbation est contrôlée séparément.
2. Traiter les hauteurs positives et négatives. Une combinaison réelle de
   caractères complexes n'est pas automatiquement paire en hauteur.
3. Garder les identifiants de branche durant la continuation. La plus petite
   hauteur détectée à chaque rayon peut changer de branche ; son enveloppe
   n'est pas une unique fonction analytique.
4. Relever toutes les candidates du scan, y compris hors des rayons admis,
   puis enregistrer séparément les rejets, dégénérescences et échecs.
5. Raffiner \(Z=Z_t=0\), contrôler \(Z_r\), \(Z_{tt}\), la réalité, la
   stabilité de précision, et les deux zéros de chaque côté du pli.
6. Marquer toute continuation perdue, toute permutation ambiguë, et tout
   passage à un contour contenant un nombre différent de zéros.

Ce protocole peut expliquer des inversions locales observées en V6.40. Il ne
certifie pas l'absence de collisions non échantillonnées, l'identité de toutes
les branches, ni l'absence de zéros hors ligne sous un plafond. Une extension
du plafond ne résout pas ces défauts de définition ou de certification.

## 8. Pont vers RH : conditions manquantes, et voie suivante

La bonne destination est une implication précise : une forme arithmétique
définie sur une classe de tests adaptée est positive pour tous les tests, et
un théorème de type Weil ou Li la relie à RH pour la fonction visée. V13 est
ici un laboratoire de combinaisons de L-fonctions dont les zéros peuvent
sortir de la ligne ; ce laboratoire ne possède pas automatiquement un
produit d'Euler ni la positivité globale d'une L-fonction arithmétique.

| Objet construit | Ce qu'il garantit | Ce qu'il ne garantit pas |
|---|---|---|
| Gram \(M_iM_i^T\) | Géométrie positive de la fibre des coefficients | Position de tous les zéros |
| Compagnon local \(H_\mu\) | Diviseur local à deux zéros, branches et collision | Spectre global de la fonction |
| Métrique \(G_\mu\) | Autoadjonction locale sur le côté \(\mu>0\) | Coercivité uniforme aux collisions |
| Moments de contour | Diviseur isolé si le nombre de zéros est contrôlé | Complétude sur toutes les hauteurs |
| Matrice de Toeplitz positive finie | Un nombre fini d'inégalités de moments | Positivité de toutes les tailles |
| Structure tensorielle ou tannakienne proposée | Un langage de compatibilités si les axiomes sont fournis | Positivité analytique ou RH par son seul nom |

Pour une montée réelle vers le global, il faut un domaine commun de tests,
une forme définie sans présupposer la localisation des zéros, des contrôles
de queue ou une fermeture appropriée, une identité exacte avec la formule
explicite arithmétique, et un théorème d'implication. Les métriques locales
singulières au pli montrent précisément où une simple recollement de
\(G_\mu\) échoue. C'est une obstruction à cette construction particulière,
pas un théorème interdisant tout chemin vers RH.

La suite raisonnable est de construire le graphe des diviseurs isolés par
contours, relier ses arêtes à des métriques locales indépendamment calculées,
et formuler explicitement le lemme de recollement ou de coercivité qui manque.
Un résultat négatif sur ce lemme est aussi informatif qu'un résultat positif.
Il évite de faire passer une image physique suggestive pour une preuve.

## Références primaires et détail d'implémentation

- Mpmath, documentation 1.3.0, fonctions zêta et Dirichlet :
  https://mpmath.org/doc/current/functions/zeta.html . La documentation
  n'annonce que la dérivée première pour `dirichlet`. Le backend installé
  accepte la valeur `derivative=2` mais renvoie alors la branche d'ordre zéro.
  `v641_collisions.py` emploie explicitement les dérivées de Hurwitz pour
  calculer la dérivée seconde ; un test indépendant utilise la formule
  \(\eta(s)=(1-2^{1-s})\zeta(s)\).
- Mpmath, différentiation numérique :
  https://www.mpmath.org/doc/current/calculus/differentiation.html . Les tests
  recoupent les jets analytiques avec une différentiation indépendante de la
  fonction normalisée.
- Jeffrey C. Lagarias, *Li Coefficients for Automorphic L-Functions*,
  arXiv:math/0404394v4, Annales de l'Institut Fourier 57 (2007), 1689–1740 :
  https://arxiv.org/abs/math/0404394 . Le cadre global y concerne des
  L-fonctions automorphes principales et des coefficients liés à la
  fonctionnelle de Weil ; ce cadre n'est pas transféré sans preuve à une
  combinaison réelle arbitraire des six fonctions V13.

Le théorème local utilise la préparation analytique de Weierstrass comme
théorème standard, avec ses hypothèses indiquées, et en déduit explicitement
le discriminant et sa dérivée. Aucune nouvelle positivité globale n'est
affirmée dans cette note.

## Audit final daté du 12 octobre 2026 — après verrouillage à 14:04 UTC

Cet audit porte sur les données sauvegardées `v641_branches.json`,
`v641_wronskiens.json`, `v641_collisions.json`, `v641_blocs_paires.json`, le
runner `run_v641_passages.py`, et la note `V641_PASSAGE_AU_GLOBAL.md`.
Les empreintes de la sélection V6.39, des racines V6.40 et de la prévision
V6.41 correspondent au verrou enregistré le 12 octobre à
14:04:33.689718 UTC. Aucune nouvelle recherche de zéro n'a été lancée pour
cette relecture ; seuls deux jets déjà identifiés ont été recoupés par une
autre formule de différentiation, explicitée ci-dessous.

### Résultats conservés et portée du mot « collision »

Les 20 candidates retenues du scan ont deux étapes acceptées à 40 et 70
chiffres de travail. Les rayons restent dans \((0,3/4)\), les hauteurs dans
\([-25,25]\), et les résidus, défauts de réalité et accords de précision
respectent les seuils gelés. Les valeurs enregistrées de \(Z_r\) et
\(Z_{tt}\) sont séparées du seuil numérique de transversalité. Les ratios
\(-2Z_r/Z_{tt}\), recalculés à partir des nombres arrondis du JSON,
diffèrent des valeurs de \(\kappa\) de moins de \(8\times10^{-18}\).
Toutes les \(\kappa\) de cet ensemble sont négatives.

Six départs distincts sont attribués numériquement à six plis distincts.
Cette attribution repose sur la continuation et un voisinage en hauteur et
en rayon ; elle n'est pas une certification topologique d'identité des
branches. La continuation au pas \(1/200\) de `k1_rpi_6_plus` est perdue à
\(r=0.24\), avec résidu \(0.00608\), et reste enregistrée comme perdue.
La continuation au pas \(1/400\) rejoint le voisinage critique du pli
\(r_*\simeq0.243079394165045\), \(t_*\simeq4.86102349099807\).
Ces deux faits ne doivent pas être fusionnés en une double confirmation
réussie de ce départ. L'extension de l'ensemble aux autres branches ou
hauteurs n'est pas couverte par cet audit.

### Moments de contour, signes et distinction des racines

Pour le cercle \(w=t_*+v\), \(v=0.2e^{ia}\), avec
\(s=\tfrac12+iw\), on a \(\partial_wF=iF_s\). L'intégrande discrétisé
du runner, \(ivF_s/F\), est donc bien celui du principe de l'argument en
variable hauteur. Le compagnon emploie correctement
\(\Delta_w=2m_2-m_1^2\) et \(\mu=\Delta_w/4\) ; en variable \(s\),
on aurait \(\Delta_s=-\Delta_w\).

Les 18 blocs sont acceptés numériquement, avec un accord maximal des
moments de \(4.69\times10^{-9}\) et une marge minimale **échantillonnée**
au bord de \(0.01338\). Pour chacun des six plis, l'offset \(-10^{-4}\)
donne \(\Delta_w>0\), l'offset \(+10^{-4}\) donne \(\Delta_w<0\), et
l'offset zéro reste classé `near_collision`. La petite valeur positive
résiduelle du discriminant à offset nul provient du calcul numérique et
ne constitue pas une séparation réelle affirmée au point double.

Les 24 racines de part et d'autre sont recoupées à 40 et 70 chiffres.
Une vérification arithmétique des valeurs sauvegardées confirme que les
deux racines de chaque bloc sont distinctes : séparation minimale
\(0.0223235\). Du côté critique, le plus grand écart enregistré de
\(\Re s\) à \(1/2\) est \(7.3\times10^{-69}\). Du côté hors ligne,
le plus grand défaut de \(\beta_1+\beta_2=1\) est
\(2\times10^{-70}\), et le plus grand défaut de hauteur commune est
\(1.4\times10^{-68}\). Il s'agit de cohérences numériques, sans borne
certifiée sur les chiffres. Les deux appels de résolution ne se sont donc
pas rabattus sur un même zéro dans les données sauvegardées.

Les normes, la marge et l'accord de deux quadratures ne certifient pas que
le bord entier soit sans zéro, ni que le contour contienne exactement deux
zéros. La dérivée EM est une formule à cinq points sans borne de troncature
globale. Les métriques positives associées aux blocs sont les matrices du
modèle réel exact conditionnel ; un calcul avec centre et discriminant
complexes arrondis doit conserver ses défauts de réalité, ou préciser sa
projection sur les parties réelles.

### Recoupement direct de deux jets, même backend déclaré

Les deux plis `fold_k1_plus_5` et `fold_k5_plus_14` ont été recoupés à
70 chiffres de travail en différentiant directement la fonction de Hardy
analytique avec `mp.diff`. Cela diffère de la formule de jet fondée sur les
dérivées explicites de Hurwitz et de phase, tout en conservant le même
backend mpmath et la même reconstruction analytique des coefficients.
Ce contrôle est une indépendance de formule, pas une indépendance de
bibliothèque d'arithmétique.

| Pli | \(|Z|\) | \(|Z_t|\) | Écart des formules pour \(Z_{tt}\) | \(\kappa\) par `mp.diff` |
|---|---:|---:|---:|---:|
| k1 plus, hauteur 4.86102 | \(9.48\,10^{-71}\) | \(9.28\,10^{-70}\) | \(8.98\,10^{-72}\) | −1.807989520647783433 |
| k5 plus, hauteur −15.77594 | \(2.45\,10^{-70}\) | \(4.44\,10^{-69}\) | \(6.48\,10^{-70}\) | −1.3582664809289763436 |

Les écarts pour \(Z_r\) sont respectivement inférieurs à
\(2.65\times10^{-70}\) et \(2.32\times10^{-71}\). Ce recoupement
confirme les signes et l'inclusion correcte des dérivées de phase dans les
jets testés. Une existence et une unicité formelles demandent encore un
argument avec erreurs contrôlées, par exemple une validation par intervalles
du système \((Z,Z_t)=0\).

### Audit de la porte globale G1–G4

Le PDF auteur de Connes–Consani, *Weil positivity and Trace formula, the
archimedean place* (4 juillet 2021), a été ouvert directement :
https://alainconnes.org/wp-content/uploads/Selecta.pdf . Son introduction,
équation (4), et sa proposition C.1 donnent le critère avec le signe négatif
pour la somme des distributions locales. Le signe opposé choisi pour
\(Q_W\) est cohérent. Les conventions Mellin et Fourier doivent rester
séparées explicitement. En coordonnées additives, la convention est fixée
par \(g(u)=f(\log u)\), \(f^*(x)=\overline{f(-x)}\), et
\(Q_W(f)=-\sum_v W_v(g*g^*)\) dans la convention Fourier de l'introduction.

Le lemme G1 est correct : le noyau compact de
\(P=\partial_x^2-1/4\) est nul, et les deux conditions exponentielles
annulent exactement les deux queues de la solution fondamentale. Le fait
que l'opérateur de la source ait le signe opposé ne change pas l'image
\(E\). La construction des tests admissibles n'impose pas le signe de la
forme de Weil.

Le lemme G2 est correct dans la topologie des tests : choisir \(L\) au-delà
du support de la primitive compacte, prolonger périodiquement, puis
multiplier les sommes de Fourier par \(\chi_L\) assure un support commun
et convergence de toutes les dérivées. Les espaces ne sont pas requis
d'être emboîtés en \(L\). Pour passer à la forme globale, sa continuité et
la positivité de **toutes** les compressions doivent être démontrées. Une
erreur numérique demande son budget dans la norme pertinente. Aucun de ces
quantificateurs ne se remplace par une longue liste finie de matrices.

Le théorème G3 est une obstruction correcte pour les opérateurs bornés
autoadjoints arbitraires soumis uniquement à un nombre fini de préfixes.
Il n'interdit pas une preuve à partir d'une identité arithmétique
supplémentaire. Le lemme G4 de Schur est correct sous les hypothèses
bornées et \(A\ge aI\), \(a>0\) ; une application à une forme non bornée
devrait d'abord définir domaine et fermeture.

L'article primaire ne fournit pas dans cette note une positivité nouvelle
sur toutes les places et tous les supports. Le graphe final peut donc
indiquer deux portes globales précises — la forme de Weil sur tous les tests,
ou une croissance arithmétique suffisante — en conservant entre les outils
V13 et ces portes le lemme de liaison encore manquant. C'est une avancée
dans la définition et la mise à l'épreuve de l'obstacle, pas sa levée globale.
