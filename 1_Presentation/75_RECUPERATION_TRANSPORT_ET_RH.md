---
title: "Après V6.49 : retrouver le travail et garder RH comme destination"
subtitle: "Programme Riemann - V6.50 - Document 75"
author: "Vincent P. P. NOËL - dossier de recherche, rédaction assistée"
date: "13 octobre 2026"
---

# 1. Ce qui a été retrouvé et ce qui a été reconstruit

Le ZIP V6.49 a été retrouvé complet : 1 259 entrées, contrôle CRC sans erreur,
empreinte SHA-256
`b14d7f9ccc3dce31aa55d70593e57b6b36029050709dc5ab515674c502dc58b7`.
Les documents, programmes, résultats et certificats qu'il contient constituent
le point de reprise vérifiable. Aucun artefact original enregistré après cette
version n'a été retrouvé dans les espaces consultés. Les sorties intermédiaires
signalées dans le fil n'étaient donc pas un nouveau ZIP finalisé.

V6.50 contient une **nouvelle reconstruction**, une relecture contradictoire et
des recalculs. Cette provenance est distinguée de la récupération des fichiers
originaux. Il n'est pas possible d'attester, à partir des traces retrouvées, une
durée de plusieurs heures ni la récupération intégrale de cette passe.

| Élément | Provenance | Statut à la reprise |
|---|---|---|
| Documents et données jusqu'au document 74 | ZIP original V6.49 | Retrouvés et conservés |
| Marge à S = 11/20, U = 10, T = 700 | Journal original V6.49 | Diagnostic flottant, déjà présent avant la perte du fil |
| Interpolation N = 512 / N = 640 | Notes du fil, puis nouveau recalcul | Reconstituée ; ancienne borne trop grande à N = 512 |
| Poids de cellules, queue de série, plafond matriciel | Nouvelle exécution V6.50 | Budgets partiels puis raccord continu ; journal distinct du diagnostic |
| Transport des supports et des moments | Construction et relecture V6.50 | Lemme démontré dans ce dossier |
| Positivité globale de Weil / RH | Aucun certificat retrouvé ou construit | Ouvert |

Une preuve interne dans ce dossier n'est pas une relecture indépendante publiée.
Les conventions arithmétiques et les hypothèses de calcul sont conservées avec
les programmes. Le nombre de tests réussis n'est pas une probabilité que RH soit
vraie, ni un pourcentage de distance à sa preuve.

![Carte des résultats, obligations et destination.](75_CARTE_RH.png)

# 2. Le sens du programme pour RH

L'objectif n'est pas ambigu : démontrer la positivité de la forme de Weil pour
**chaque fonction test compacte admissible**. L'énergie positive intervient
dans cette forme, mais deux factures y sont soustraites : la masse et les
corrélations arithmétiques. La positivité de l'énergie ne fixe donc pas le
signe du bilan.

Pour S positif, les fonctions sont prolongées par zéro hors de [-S,S]. Posons
\[
\ell_\pm(f)=\int f(x)e^{\pm x/2}\,dx.
\]
\[
X_S=\{f\in L^2:\operatorname{supp}f\subset[-S,S],\ \ell_\pm(f)=0,\ \mathcal E(f)<\infty\}.
\]
Avec la Fourier unitaire,
\[
\mathcal E(f)=\int a(t)|\widehat f(t)|^2dt,\quad
R(f)=\|f\|_2^2+\mathcal E(f),\qquad
a(t)=\sum_{n\ge0}\frac{2t^2}{b_n(b_n^2+t^2)},\quad b_n=2n+\tfrac12.
\]
La forme pertinente est
\[
Q_W(f)=\mathcal E(f)-C_0\|f\|_2^2
-2\sum_{\log q<2S}c_q\Re\int f(x)\overline{f(x-\log q)}\,dx,
\]
\[
C_0=\log(8\pi)+\gamma_E+\frac\pi2,\qquad
q=p^m,\quad c_q=\frac{\log p}{\sqrt q}.
\]
Les unités fictives restent celles du corpus : les coefficients et les
paramètres logarithmiques sont sans dimension ; la masse, l'énergie et Q ont
l'unité d'amplitude au carré. Une unité fictive aide à contrôler une formule ;
elle ne fournit pas son signe.

Le critère de Weil, dans la formulation Connes-Consani [CC21, équation (4),
appendice C, proposition C.1], autorise ces deux annulations polaires sans
affaiblir l'équivalence avec RH. La normalisation est vérifiée par
\[
a(t)-C_0=\Re\psi_{\rm digamma}(1/4+it/2)-\log\pi.
\]
La classe X n'est donc pas un détour qui aurait abandonné RH. Le quantificateur
qui manque est **tous les supports**, avec tous les tests dans chacun d'eux.

Le certificat du document 73 couvre un espace infini entier pour 0 < S <= 1/2.
Le document 74 certifie un paiement conjoint de plusieurs corrélations ; à
S = 1, son enveloppe est inférieure à 0,796, contre plus de 1,24 pour la somme
des paiements séparés. Cette brique conserve de l'énergie dans une minoration,
mais la masse soustraite doit encore être payée. Aucun de ces faits ne prouve
le signe pour tous les supports.

## Lemme 1. Une exhaustion suffit ; une marge uniforme n'est pas requise

Si \(S_n\) tend vers l'infini et si Q est non négative sur chaque \(X_{S_n}\), alors
RH. Les minorations peuvent dépendre de n et tendre vers zéro.

**Preuve.** Tout test compact admissible appartient à l'un de ces espaces.
Les nouveaux premiers ajoutés lorsqu'on agrandit la boîte ont une corrélation
nulle sur ce test tant que leur translation dépasse son diamètre. La valeur
de Q du test ne change donc pas par inclusion dans une boîte plus grande.
Sa positivité résulte du certificat de cette boîte. Appliquer le critère de
Weil. Une limite d'opérateurs globaux et une constante uniforme strictement
positive ne sont pas nécessaires à cet argument. Une liste finie de boîtes
ne satisfait pas son hypothèse. □

# 3. Un transport exact : la même grammaire sur plusieurs supports

L'image est celle d'un moule : une graine k fabrique f en annulant les deux
moments. Étirer seulement f déplace les points où ses moments s'annulent.
Le transport ci-dessous ajuste le moule pendant l'étirement.

Pour r > 0, définir
\[
P_r=\partial_x^2-r^2/4,\qquad
K_r=P_r^{-1},\quad K_r f=-r^{-1}e^{-r|\cdot|/2}*f,
\]
\[
(D_rh)(x)=r^{-1/2}h(x/r),\qquad T_r=D_rP_rK_1.
\]
Le facteur de D rend cette dilatation unitaire en L². L'inverse P n'est pas
appliqué aveuglément à une fonction quelconque : le lemme établit pourquoi
les annulations polaires rendent la graine compacte.

## Lemme 2. Support, moments, inversion et composition

\(T_r\) est un isomorphisme de \(X_S\) vers \(X_{rS}\). Il vérifie
\[
T_1=I,\qquad T_rT_s=T_{rs},\qquad T_r^{-1}=T_{1/r}=P_1K_rD_r^{-1}.
\]

**Preuve des domaines.** La dérivée de -exp(-|x|/2) a un saut de 1 en zéro,
donc \(P_1K_1=I\) au sens des distributions. Pour \(f\in X_S\), \(k=K_1f\) est
dans H². Hors de la boîte,
\[
k(x)=-e^{-x/2}\ell_+(f)=0\quad(x>S),\qquad
k(x)=-e^{x/2}\ell_-(f)=0\quad(x<-S).
\]
La graine k est ainsi portée par la même boîte. La fonction
\(P_rk=f+(1-r^2)k/4\) est encore L² et de même support. Ses moments en
plus ou moins r/2 sont nuls par intégration par parties. Le changement de
variable \(x=ry\) dans D transforme précisément ces moments en \(\ell_+\) et \(\ell_-\).
Pour inverser, \(D_r^{-1}\) transporte les moments du test cible en plus ou moins
\(r/2\) ; le même calcul rend \(K_rD_r^{-1}\) compact. L'inverse indiqué suit.

**Preuve de la composition.** La dérivation donne \(D_rP_r=r^2P_1D_r\), donc
\(T_r=r^2P_1D_rK_1\). Sur les graines H² compactes, \(K_1P_1=I\). Comme
\(D_rD_s=D_{rs}\), les facteurs se composent et donnent \(T_rT_s=T_{rs}\).
La conservation du domaine d'énergie est justifiée par le lemme suivant. □

Ce résultat résout deux problèmes ensemble : changer de support et conserver
les tests admissibles. Il conserve aussi une loi de composition exacte.
Il ne conserve pas automatiquement le signe de Q.

## Lemme 3. Les normes accompagnent le transport

Poser \(w_r(t)=(t^2+r^2/4)/(t^2+1/4)\). Alors
\[
\widehat{T_rf}(t)=\sqrt r\,w_r(rt)\widehat f(rt),\qquad
R(T_rf)=\int w_r(t)^2[1+a(t/r)]|\widehat f(t)|^2dt,
\]
\[
\min(1,r^4)\|f\|_2^2\le\|T_rf\|_2^2\le\max(1,r^4)\|f\|_2^2,
\]
\[
\boxed{\min(r^4,r^{-2})R(f)\le R(T_rf)\le\max(r^4,r^{-2})R(f).}
\]

**Preuve.** La Fourier de \(P_rK_1\) est \(w_r\), compris entre \(\min(1,r^2)\) et
\(\max(1,r^2)\). Dans chaque terme de la série positive de a, la dilatation
\(t\) vers \(t/r\) change le facteur \(t^2/(b^2+t^2)\) dans un rapport compris entre
\(\min(1,r^{-2})\) et \(\max(1,r^{-2})\). Les mêmes bornes valent pour la somme et
pour 1+a. Le changement de variable fréquentiel annule le facteur r de
la masse. Multiplier les bornes fournit les constantes annoncées. Elles
s'appliquent aussi à l'inverse et donnent l'isomorphisme d'énergie finie. □

À r = 11/10, la boîte 1/2 devient 11/20 et les normes R restent comparables
avec des facteurs 100/121 et 14641/10000. Cette comparaison borne une taille ;
elle n'est pas une minoration de Q.

## Lemme 4. Le transport construit le cœur nécessaire à la positivité

Les fonctions lisses de support strictement intérieur à [-S,S], avec les
deux moments nuls, sont denses dans \(X_S\) pour la norme \(\sqrt R\).

**Preuve.** Prendre r < 1 puis r tendant vers 1. T_rf conserve les moments
et libère une marge de support. Les dilatations sont fortement continues dans
le Hilbert de Fourier de poids 1+a : le vérifier d'abord sur des fonctions
de Schwartz, puis utiliser les bornes du lemme 3 uniformes près de r = 1.
Le multiplicateur \(w_r\) converge uniformément vers 1. Ainsi \(T_rf\) tend vers f
en norme \(\sqrt R\). Mollifier \(T_rf\) avec un noyau positif, lisse, compact,
d'intégrale 1 et de support plus petit que la marge libérée. Les moments de
la convolution sont les produits des moments des deux facteurs et restent
nuls. Le multiplicateur de mollification est borné par 1 et tend vers 1.
La convergence dominée donne la convergence en norme \(\sqrt R\). □

La forme polarisée satisfait à support fixé
\[
|Q_W(f,g)|\le(1+C_0+2\sum c_q)\sqrt{R(f)R(g)}.
\]
Cauchy-Schwarz borne l'énergie, la masse et chaque translation. Le signe
passe donc du cœur à X_S. La norme de **forme** suffit ici. Une norme de
graphe plus forte reste pertinente lorsque la voie choisie demande des
sources fortes dans L² ; ce n'est pas une obligation supplémentaire du
simple argument de positivité par densité.

## La loi globale manquante est maintenant écrite sur un espace fixe

Sur \(X_{S_0}\), le transport donne exactement
\[
\mathcal Q_r(f)=Q_W(T_rf)=\int w_r(t)^2
\left[a(t/r)-C_0-2\sum_{\log q<2rS_0}c_q\cos(t\log q/r)\right]
|\widehat f(t)|^2dt.
\]
Les termes de translation qui ne rencontrent pas le support ont une
contribution intégrée nulle. Tous les facteurs de dilatation sont explicités.
L'isomorphisme précédent et le critère de Weil donnent
\[
\mathrm{RH}\quad\Longleftrightarrow\quad
\forall r>0,\ \forall f\in X_{S_0},\quad \mathcal Q_r(f)\ge0.
\]
Le domaine de départ est fixe et les changements de langue sont exacts.
L'inégalité universelle reste à prouver. Cette reformulation ne la résout
pas par elle-même, mais précise ce qu'une nouvelle structure doit apporter.

# 4. Les calculs reconstitués à 11/20 : de quels certificats parle-t-on ?

Le journal V6.49 contenait déjà, à S = 11/20, U = 10, T = 700 et N = 512,
une marge paire de +0,0005830255155. La différence entre deux résolutions
était environ 2,8 fois 10^(-8). Ces nombres décrivaient une stabilité
numérique. Ils n'encadraient pas la norme de l'opérateur continu.

La reconstruction distingue cinq obligations :

1. **Identité et domaine.** La même forme de Weil et les mêmes moments
   doivent accompagner toutes les représentations.
2. **Queue.** Une minoration analytique exclut les fréquences omises.
3. **Quadrature.** Une erreur de norme couvre chaque cellule, y compris
   le changement de régime de la partie positive du poids.
4. **Matrice.** Un plafond rigoureux couvre une matrice finie précisément
   définie ; son origine approchée a une erreur séparée.
5. **Relèvement.** Nœuds, poids de Gauss, fonctions trigonométriques, Gram,
   produits matriciels et interpolation relient cette matrice à tous les tests.

La positivité suit seulement si la réserve reste positive après **toutes**
ces erreurs. Un plafond certifié sur une matrice flottante traitée comme
matrice dyadique exacte ne certifie pas automatiquement son opérateur parent.

| Poste | Valeur ou résultat | Portée |
|---|---|---|
| Support | 11/20 ; 640 nœuds ; 700 000 cellules | Tous les tests admissibles dans cette boîte |
| Table | 0.0001093826833 | Majorant du journal rationnel |
| Quadrature pondérée | 0.0001521640668 | Majorant du journal rationnel |
| Interpolation spatiale | 3.713853486e-53 | Majorant du journal rationnel |
| Poids intégrés | 4.857225733e-11 | Majorant du journal rationnel |
| Assemblage | 1.108347935e-05 | Majorant du journal rationnel |
| Relèvement even | 0.0002726507906 | Somme de toutes les erreurs de norme |
| Relèvement odd | 0.0002726508415 | Somme de toutes les erreurs de norme |
| Marge minimale | 0.0003004510351 | Minorant strict positif exact conservé dans le journal |

**Résultat exécuté.** Le certificat ferme les cinq obligations pour S = 11/20 dans son modèle arithmétique déclaré. Par inclusion des supports, il vaut aussi pour 0 < S <= 11/20. Les fonctions complexes sont couvertes par la séparation des deux parités et des parties réelle et imaginaire. Le résultat ne porte pas sur tous les supports et ne prouve pas RH.


## Théorème local exécuté et modèle de preuve

Lorsque le journal intégral et sa vérification sont positifs, le certificat
donne, pour les tests complexes de X_S avec 0 < S <= 11/20,
\[
Q_W(f)\ge\frac{3}{10000}\|f\|_2^2,\qquad
Q_W(f)\ge\frac{1}{25001}R(f).
\]
Ces deux minorations sont vérifiées dans le modèle arithmétique déclaré :
primitives IEEE binaire64 arrondies vers l'extérieur, modèle gamma_n des
produits et sommes matriciels, intervalles mpmath, signes polynomiaux entiers
exacts. La lecture contradictoire contrôle les lemmes et budgets ; elle ne
constitue pas une validation formelle du compilateur ou du processeur.

**Preuve du relèvement.** Écrire
\[
b_S(t)=a(t)+2\sum_q c_q[1-\cos(t\log q)],\quad C_S=C_0+2\sum_qc_q,\quad\phi=(U-b_S)_+.
\]
Le coût \(b_S\) est supérieur ou égal à \(U-\phi\). Sur le noyau des moments, l'intégrale de \(\phi\) est la forme d'un
opérateur positif B. Le journal exclut la queue t > 700 et établit
\[
\|B\|\le\max_{\rm parites}(\tau+\delta),\qquad
U-C_S-\max_{\rm parites}(\tau+\delta)>0{,}00030045.
\]
Le plafond tau est prouvé par congruence ; delta additionne les erreurs de
table, quadrature, interpolation, ondes, poids, assemblage et symétrisation.
L'isométrie du repère cardinal de Gauss et l'erreur d'interpolation relient
la matrice à tout l'espace L² ; il ne s'agit pas de tester seulement les
640 fonctions d'un sous-espace. Le journal exact dépasse 3/10000, ce qui
donne la minoration massique. Les deux parités et les parties réelle et
imaginaire couvrent tous les tests complexes.

Pour la minoration en R, les deux déplacements log 2 et log 3 dépassent
S = 11/20. Les deux bandes d'un même déplacement sont donc disjointes.
L'inégalité \(2|uv|\le|u|^2+|v|^2\) donne \(|Q_{\rm pr}|\le(c_2+c_3)m\). Le contrôle
par intervalles vérifie C_0+c_2+c_3 < 13/2. Par conséquent
\[
\mathcal E\le Q_W+\tfrac{13}{2}m,\qquad
R\le Q_W+\tfrac{15}{2}m
\le\left(1+\frac{15/2}{3/10000}\right)Q_W=25001 Q_W.
\]
L'inclusion dans la boîte 11/20 conserve les moments, l'énergie et la valeur
de Q pour chaque support plus petit. Cela achève les deux minorations. □

Les deux améliorations analytiques sont détaillées dans le rapport constructif
archivé : intégration du poids linéaire positif dans chaque cellule, et
encadrement de la queue de série par une représentation de Laplace et un
sandwich de coth. Les données enregistrent leurs paramètres et la clôture des postes
du budget. Les normes calculées des vecteurs échantillonnés
restent distinctes des normes des vecteurs continus.

Le passage N = 512 vers N = 640 ne prouve rien sur RH en lui-même. Il répare
un défaut précis de l'ancienne borne d'interpolation, pour la bande T = 700.
La somme du journal ferme ici la certification locale. Elle ne démontre pas une règle pour tous les S.

# 5. Ce que la littérature change dans notre priorité

Connes-Consani [CC21] fournit le pont conceptuel de la positivité et la
justification de la classe polaire. Son programme semi-local indique où
une structure positive pourrait absorber les contributions premières.

La prépublication [Zhu26, v2], déjà présente au registre, annonce une positivité certifiée pour
toutes les fonctions complexes de support [-0,8 ; 0,8], ainsi que des
minorations et majorations spectrales. Sur le noyau des deux moments, ses
conventions coïncident avec les nôtres ; son domaine est plus large.
Cette annonce n'a pas été indépendamment reproduite dans V6.50 et n'est pas
ajoutée au compteur des certificats du corpus. Elle impose d'éviter toute
revendication de priorité pour le seul franchissement de S = 0,55.

Ce texte décrit aussi une barrière de coût pour son architecture de majorants
ponctuels. La même difficulté apparaît dans la garde actuelle du corpus :
Q >= (U-C_S-||B||)m exige U > C_S et l'exclusion de queue utilisée demande
a(T) > U. Avec C_S = C_0+2 sum c_q et la croissance logarithmique de a,
le plafond T peut croître extrêmement vite lorsque S augmente. Une barrière
de coût de cette architecture n'est pas un théorème d'impossibilité de RH.

Le bon prochain gain serait une borne **sur les formes et les directions
admissibles**, conservant les phases, ou une décomposition positive globale.
La liste finie des phases premières peut s'aligner arbitrairement bien : une
marge uniforme obtenue par les seules phases est déjà exclue par le lemme L6
du document 74. Il faut donc garder l'action de l'énergie et la localisation
du test dans l'estimation arithmétique.

# 6. Les quatre portes et le prochain protocole

| Porte | Gain V6.50 | Obligation qui porte encore le signe |
|---|---|---|
| Arithmétique | Forme transportée exacte ; phases et poids conservés | Loi de signe des corrélations sur les directions admissibles |
| Tête et queue | Relèvement continu certifié à 11/20 ; erreurs améliorées | Réutilisation efficace pour une famille de supports non bornée |
| Couplages | Contrats de minorant borné séparés des sources fortes de Q | Sources et Schur nécessaires à la voie effectivement choisie |
| Couverture | Action T_r et cœur dense en norme de forme | Positivité pour chaque r, ou une exhaustion démontrée |

Ces portes servent à comparer des voies. Le certificat par minorant borné,
le Schur de la forme originale et une représentation positive structurelle
sont des **alternatives**. Réussir chacune d'elles n'est pas requis
simultanément pour RH. Dans une voie donnée, en revanche, ses hypothèses
doivent toutes être satisfaites.

Bellman peut organiser ce graphe de contrats : un embranchement choisit une
voie ; une conjonction exige tous ses lemmes. Dans une forme, Schur élimine
une variable et mesure une dette exacte. Aucun classement de protocoles,
score ou récompense ne remplace la loi de signe manquante.

Le relèvement continu du test 11/20 est fermé dans cette version. Le prochain protocole étudie la famille Q_r comme un seul problème d’opérateurs sur un domaine fixe, et doit produire
une inégalité qui fonctionne pour une famille non bornée de r. Sans ce gain,
une série d'essais locaux demeure une exploration de couverture bornée.

**Avis.** Ce programme garde un sens pour RH parce que son objet positif est
équivalent au but, que ses traductions ont désormais des domaines et que ses
obstacles sont identifiés. Les outils constituent un progrès méthodologique.
La loi globale de signe reste une question mathématique entière ; aucune
probabilité de succès ni échéance de preuve n'est justifiée par ce dossier.

# Références et reproduction

- [CC21] Alain Connes, Caterina Consani, *Weil positivity and Trace formula,
  the archimedean place*, version du 4 juillet 2021, équations (4), (154),
  appendice C, proposition C.1 :
  <https://alainconnes.org/wp-content/uploads/Selecta.pdf>.
- [Zhu26] Xuefeng Zhu, *Weil positivity in compact windows: a finite
  reduction, certified two-sided bounds, and a Landau-Widom decay law*,
  arXiv:2608.24827v2, 2 septembre 2026 :
  <https://arxiv.org/html/2608.24827v2>. Les métadonnées de v1 donnaient un
  autre nom d'auteur ; V6.50 retient la version courante vérifiée.
- V6.49, documents 73 et 74, journaux v648_common_certificate_resultats.json,
  v649_joint_payment_resultats.json et v649_multi_prime_diagnostic.json.
- V6.50 : rapports constructif et critique dans 4_Archives/recus/V650 ;
  programmes et journaux dédiés dans 3_Preuves_et_calculs.

Exécuter le script v650_support_transport_experiment.py reproduit six exemples
de transport. La conjugaison polynomiale est vérifiée par fractions exactes ;
les moments et masses de ces exemples sont des diagnostics flottants. La
preuve universelle est celle des lemmes 2 et 3, pas ces six observations.

<!-- references:debut -->

## Références

Format : [clé] auteurs, *titre*, publication, lien. Fiches complètes et état de vérification : document 42 (registre des sources).

- [CC21] A. Connes, C. Consani. *Weil positivity and Trace formula, the archimedean place*. PDF auteur daté du 4 juillet 2021 ; arXiv:2006.13771. <https://alainconnes.org/wp-content/uploads/Selecta.pdf> — partiellement vérifié
- [Zhu26] X. Zhu. *Weil positivity in compact windows: a finite reduction, certified two-sided bounds, and a Landau–Widom decay law*. arXiv:2608.24827 (v2, sept. 2026). <https://arxiv.org/abs/2608.24827> — vérifié en ligne. **Correctif V6.18 :** λ*(L) est un infimum variationnel sur toutes les fonctions test de support [−L, L] ; la plus petite valeur propre d'une matrice de Weil de taille finie en est un majorant (Zhu, remarque 2.2).

<!-- references:fin -->
