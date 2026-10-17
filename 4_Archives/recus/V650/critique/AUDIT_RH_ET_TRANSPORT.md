# Audit critique après V6.49 : le pont vers RH et ses limites

Date : 13 octobre 2026. Nouvelle reconstruction critique, à partir du corpus
V6.49 récupéré. Ce rapport ne certifie pas la récupération de calculs originaux
postérieurs à V6.49. Il ne modifie pas les certificats et archives du corpus.

## 1. Ce qui a un sens pour RH

Le programme a une destination mathématique précise : démontrer le signe de la
forme de Weil pour chaque fonction test compacte admissible. Les termes
« admissible », « compacte » et « chaque » portent l'essentiel du contenu.
Construire une fonction d'énergie positive ne suffit pas : la forme pertinente
est une différence entre cette énergie, une masse et des corrélations premières.

Le résultat du document 73 porte sur un espace infini entier, avec
\(0<S\le 1/2\). Il est donc plus fort qu'une collection de valeurs propres
positives sur des matrices d'essai. Sa couverture demeure bornée. L'essai
\(S=11/20\) vérifie l'entrée du premier 3 et la possibilité de réutiliser
l'architecture, mais ne fournit aucun mécanisme allant à tous les supports.

Le résultat réutilisable du document 74 est un paiement conjoint des attaches
premières par l'énergie de bord. Cette localisation évite de payer plusieurs
fois une énergie traitée séparément. Elle ne paie pas, à elle seule, le terme
\(C_0\|f\|_2^2\) soustrait dans la forme de Weil.

L'utilité scientifique de l'étape suivante dépend ainsi de deux livrables :
un raccord local réellement certifié et une formulation plus nette de la loi
globale manquante. Une amélioration de calcul qui ne rapproche aucun de ces
deux livrables ne doit pas être comptée comme un progrès vers RH.

## 2. Le critère exact et la classe polaire

Définissons, pour \(S>0\),
\[
\ell_\pm(f)=\int_{-S}^{S}f(x)e^{\pm x/2}\,dx,
\qquad P_1=\partial_x^2-\frac14,
\]
\[
X_S=\{f\in L^2(\mathbb R):\operatorname{supp}f\subset[-S,S],
\ell_+(f)=\ell_-(f)=0,\ \mathcal E(f)<\infty\}.
\]
Les fonctions sont prolongées par zéro. Avec la Fourier unitaire,
\[
\mathcal E(f)=\int_{\mathbb R}a(t)|\widehat f(t)|^2dt,
\quad a(t)=\sum_{n\ge0}\frac{2t^2}{b_n(b_n^2+t^2)},
\quad b_n=2n+\tfrac12,
\]
\[
R(f)=\|f\|_2^2+\mathcal E(f),
\quad Q_W(f)=\mathcal E(f)-C_0\|f\|_2^2
-2\sum_{\log q<2S}c_q\Re\langle f,U_{\log q}f\rangle,
\]
\[
C_0=\log(8\pi)+\gamma_E+\frac\pi2,
\quad q=p^m,\quad c_q=\frac{\log p}{\sqrt q}.
\]
Un terme à \(\log q=2S\) est nul, car deux fonctions portées par
\([-S,S]\) n'ont alors qu'une intersection de supports de mesure nulle.

Le primaire Connes–Consani [CC21], équation (4) et appendice C,
proposition C.1, confirme que les annulations Mellin en 0 et 1 peuvent être
imposées sans affaiblir le critère de RH. Sous \(x=\log u\), elles deviennent
précisément \(\ell_\pm=0\). Les formules (153)–(154) vérifient aussi la
normalisation archimédienne, puisque
\[
a(t)-C_0=\Re\psi_{\mathrm{digamma}}(1/4+it/2)-\log\pi.
\]
La positivité sur tous ces tests compacts est donc une vraie destination
équivalente à RH. Elle ne suppose ni la simplicité des zéros ni le contrôle
des collisions des anciennes familles.

### Lemme A — Le moule polaire représente exactement les tests lisses

Pour \(f\in C_c^\infty((-S,S))\) avec \(\ell_\pm(f)=0\), il existe une
unique \(\psi\in C_c^\infty((-S,S))\) telle que \(f=P_1\psi\).
Réciproquement, toute \(P_1\psi\) de cette classe annule les deux moments.

**Preuve.** Le noyau
\(G_1(x)=-e^{-|x|/2}\) vérifie \(P_1G_1=\delta_0\) : sa dérivée
présente un saut égal à 1 en 0. Poser \(\psi=G_1*f\). Pour \(x>S\),
\(\psi(x)=-e^{-x/2}\ell_+(f)=0\); pour \(x<-S\),
\(\psi(x)=-e^{x/2}\ell_-(f)=0\). L'équation différentielle assure la
régularité lisse. Une solution compacte de \(P_1\psi=0\) est nulle.
La réciproque résulte de deux intégrations par parties. □

Ce lemme est déjà sous-jacent aux documents 68–70. Sa reformulation précise
qu'utiliser des graines ne perd aucune direction test lisse admissible.

## 3. La couverture globale : le quantificateur manquant

### Lemme B — Une exhaustion suffit, sans marge uniforme

Soit \(S_n\to\infty\). Si \(Q_W(f)\ge0\) pour tous \(f\in X_{S_n}\)
et chaque \(n\), alors RH. Une constante positive indépendante de \(n\)
n'est pas requise. Il n'est pas non plus nécessaire de construire une limite
en norme d'un opérateur global.

**Preuve.** Toute fonction test compacte admissible a son support dans
\([-S_n,S_n]\) pour un \(n\) assez grand. La forme globale de cette
fonction et ses moments ne changent pas quand on l'inclut dans un support
plus grand : les nouveaux termes premiers ont une corrélation nulle. La
positivité pour ce \(n\) donne celle du test. Appliquer le critère de Weil.
□

La règle de couverture est élémentaire mais indispensable : une liste
finie de supports, même très longs, n'est pas une exhaustion démontrée.
Une procédure qui a réussi chaque essai exécuté n'est pas encore un
théorème de terminaison pour tous les \(n\).

### Lemme C — Une preuve de signe de forme utilise la norme de forme

Pour \(f,g\in X_S\), la polarisation de \(Q_W\) est continue dans
\(\|f\|_R=\sqrt{R(f)}\), avec
\[
|Q_W(f,g)|\le
\Bigl(1+C_0+2\sum_{\log q<2S}c_q\Bigr)\|f\|_R\|g\|_R.
\]

**Preuve.** Cauchy–Schwarz dans l'intégrale définissant \(\mathcal E\)
majore sa polarisation par \(\sqrt{\mathcal E(f)\mathcal E(g)}\).
La masse et chaque translation se majorent par \(\|f\|_2\|g\|_2\).
Chacune de ces normes est dominée par \(\|\cdot\|_R\). La somme première
est finie à support fixé. □

Par conséquent, le signe sur un cœur dense en norme \(R\) passe à
\(X_S\). Une convergence en norme de graphe plus forte est nécessaire
quand la stratégie exige que des *sources fortes* convergent en \(L^2\).
Cette garde supplémentaire ne doit pas être imposée à une simple extension
du signe par continuité de forme. Pour le minorant borné du document 73,
une borne de norme opérateur \(L^2\) est le contrat adapté.

### Lemme D — Un témoin négatif a une approximation finie

Si \(Q_W(f)<0\) pour un \(f\in X_S\), toute famille admissible dense
en norme \(R\) contient une combinaison finie avec une forme strictement
négative. Les coefficients peuvent être approximés par des rationnels.

**Preuve.** Approcher \(f\) en norme \(R\), puis utiliser le lemme C.
Une inégalité stricte négative subsiste pour une approximation assez fine.
Dans un sous-espace fini, la forme dépend continûment des coefficients. □

Cela donne une asymétrie logique utile : une recherche exhaustive peut
trouver un contre-exemple fini validé ; une succession de réponses positives
finies ne prouve pas l'absence globale de contre-exemple. Une table Bellman
peut organiser la recherche, mais ne change pas cette asymétrie.

## 4. Un pont constructif global : transporter les moments avec le support

Cette construction a été proposée par le coordinateur et vérifiée dans
cette lecture critique. Elle est une nouvelle brique dans ce dossier,
sans revendication de priorité bibliographique.

Pour \(r>0\), définir
\[
P_r=\partial_x^2-\frac{r^2}{4},\qquad
K_r=P_r^{-1},\quad K_r f=-\frac1r e^{-r|\cdot|/2}*f,
\]
\[
(D_rh)(x)=r^{-1/2}h(x/r),\qquad T_r=D_rP_rK_1.
\]
Le facteur \(r^{-1/2}\) rend \(D_r\) unitaire sur \(L^2\).

### Lemme E — Support, admissibilité, inversion et loi de composition

Sur \(H_S=\{f\in L^2:\operatorname{supp}f\subset[-S,S],
\ell_\pm(f)=0\}\), \(T_r\) est un isomorphisme borné vers \(H_{rS}\).
Il se restreint à un isomorphisme \(X_S\to X_{rS}\). Il satisfait
\[
T_1=I,\qquad T_rT_s=T_{rs},\qquad T_r^{-1}=T_{1/r}
=P_1K_rD_r^{-1}.
\]

**Preuve des domaines.** Pour \(f\in H_S\), \(K_1f\in H^2(\mathbb R)\)
et est porté par \([-S,S]\), comme au lemme A. Écrire
\(P_rK_1f=f+(1-r^2)K_1f/4\); cette fonction est donc \(L^2\) et de
même support. Les moments en \(\pm r/2\) sont nuls par intégration par
parties dans \(H^2\). Le changement de variable \(x=ry\) transforme ces
moments en \(\ell_\pm(T_rf)=0\). Pour un test de \(H_{rS}\),
\(D_r^{-1}\) donne les annulations en \(\pm r/2\), qui rendent
\(K_rD_r^{-1}\) compact ; la formule de l'inverse suit.

**Preuve de la composition.** L'identité de dérivation
\(D_rP_r=r^2P_1D_r\) donne
\(T_r=r^2P_1D_rK_1\). Sur les graines compactes,
\(K_1P_1=I\). Comme \(D_rD_s=D_{rs}\), on obtient immédiatement
\(T_rT_s=T_{rs}\). L'identité
\(K_1T_rf=r^2D_rK_1f\) décrit aussi la graine transportée. □

### Lemme F — Le transport mesure précisément son coût

Poser
\[
w_r(t)=\frac{t^2+r^2/4}{t^2+1/4}.
\]
Alors
\[
\widehat{T_rf}(t)=\sqrt r\,w_r(rt)\widehat f(rt),
\]
\[
R(T_rf)=\int_{\mathbb R}w_r(t)^2[1+a(t/r)]
|\widehat f(t)|^2dt,
\]
\[
\boxed{\min(r^4,r^{-2})R(f)\le R(T_rf)
\le\max(r^4,r^{-2})R(f).}
\]

**Preuve.** La Fourier de \(P_rK_1\) est le multiplicateur \(w_r\),
et celle de \(D_r\) est la dilatation indiquée. Le changement de variable
\(t\mapsto t/r\) dans l'intégrale annule le facteur \(r\) de la masse.
On a \(\min(1,r^2)\le w_r\le\max(1,r^2)\). Dans chaque terme de la
série positive de \(a\),
\[
\min(1,r^{-2})\le
\frac{(t/r)^2/[b_n^2+(t/r)^2]}{t^2/(b_n^2+t^2)}
\le\max(1,r^{-2}),\quad t\ne0.
\]
La même inégalité vaut après sommation et après ajout de 1. Multiplier les
deux bornes fournit les constantes écrites. Elles assurent notamment que
le transport et son inverse préservent le domaine d'énergie finie. □

### Lemme G — Le transport donne aussi un cœur dense

Le cœur \(C_c^\infty((-S,S))\cap\ker\ell_+\cap\ker\ell_-\) est dense
dans \(X_S\) pour la norme \(R\).

**Preuve.** Pour \(0<r<1\), \(T_rf\) est porté par \([-rS,rS]\) et
conserve les moments. Les dilatations sont fortement continues dans le
Hilbert de Fourier de poids \(1+a(t)\); on peut le vérifier d'abord sur
les fonctions de Schwartz, puis utiliser les bornes uniformes du lemme F
sur un voisinage de \(r=1\). Le multiplicateur \(P_rK_1\) converge
uniformément vers 1 quand \(r\to1\). Ainsi \(T_rf\to f\) en norme \(R\).
Mollifier ensuite \(T_rf\) avec un noyau lisse compact de support assez
petit pour rester à l'intérieur de \((-S,S)\). Les moments de la
convolution sont les produits des moments du noyau et de \(T_rf\), donc
restent nuls. La Fourier de la mollification est bornée par 1 et converge
ponctuellement vers 1 ; la convergence en norme \(R\) résulte de la
convergence dominée. Choisir successivement \(r\to1\) et le pas de
mollification vers 0. □

Ce transport apporte un coup double exact : agrandir ou réduire le support
en gardant la grammaire polaire, et établir le cœur nécessaire à la
continuité des formes. Il ne conserve pas le signe de \(Q_W\).

### La forme globale, désormais sur un espace fixe

Sur un \(X_{S_0}\) fixé, le transport donne exactement
\[
\mathcal Q_r(f):=Q_W(T_rf)
=\int_{\mathbb R}w_r(t)^2
\left[a(t/r)-C_0
-2\sum_{\log q<2rS_0}c_q\cos(t\log q/r)\right]
|\widehat f(t)|^2dt.
\]
Pour tout \(r\), les termes qui ne peuvent joindre deux points du support
ont une contribution intégrée nulle. Les étapes de dilution, multiplication
et changement de variable ont toutes leurs facteurs explicités.

Par le lemme E et le critère de Weil,
\[
\boxed{\mathrm{RH}\quad\Longleftrightarrow\quad
\forall r\ge1,\ \forall f\in X_{S_0},\quad\mathcal Q_r(f)\ge0.}
\]
Le changement de langue est réel : les espaces variables deviennent une
action de dilatations sur une classe fixe. La difficulté arithmétique reste
dans le multiplicateur signé et l'arrivée des nouvelles puissances premières.
Une preuve ne peut pas supposer le membre de droite pour justifier ce pont.

## 5. Une obstruction démontrable de l'architecture actuelle

À support \(S\), le document 74 utilise
\[
b_S(t)=a(t)+2\sum_{\log q<2S}c_q[1-\cos(t\log q)],
\quad C_S=C_0+2\sum_{\log q<2S}c_q.
\]
Le minorant plafonné est
\[
A_{S,U}=(U-C_S)I-B_{S,U},\qquad B_{S,U}\succeq0,
\]
et sa queue fréquentielle est actuellement exclue par la garde
\(a(T)>U\), puisque \(b_S\ge a\).

### Lemme H — Cette garde impose une échelle doublement exponentielle

Une positivité stricte de ce minorant exige \(U>C_S\). L'exclusion de
queue par \(a(T)>U\) impose donc \(a(T)>C_S\). En utilisant uniquement
le théorème des nombres premiers et l'asymptotique de la digamma,
\[
2\sum_{q<e^{2S}}\frac{\Lambda(q)}{\sqrt q}
=(4+o(1))e^S,
\qquad a(T)-C_0=\log(T/(2\pi))+o(1),
\]
d'où
\[
\boxed{T\ge2\pi\exp\bigl((4+o(1))e^S\bigr).}
\]

**Preuve.** Si \(U\le C_S\), la forme de \(A_{S,U}\) est nonpositive,
car \(B_{S,U}\) est positif ; une marge strictement positive est impossible.
Pour la somme première, écrire \(X=e^{2S}\) et appliquer l'intégration de
Stieltjes à \(\sum_{q<X}\Lambda(q)/\sqrt q\) avec
\(\Psi(X)\sim X\). Le terme terminal vaut \(\sqrt X+o(\sqrt X)\),
l'intégrale vaut \(\sqrt X+o(\sqrt X)\), puis multiplier par 2.
L'asymptotique archimédienne donne la seconde formule. Les deux gardes
imposent alors l'inégalité annoncée. □

Cette obstruction concerne la combinaison **plafond uniforme + queue
exclue par \(b_S\ge a\)**. Elle n'exclut pas une meilleure majoration
opératoire, des exclusions fréquentielles validées qui utilisent la phase,
ni une factorisation arithmétique positive. Elle ne prouve aucune impasse
universelle vers RH. Elle justifie de développer un mécanisme de compensation
dans les fonctions admissibles plutôt que d'agrandir indéfiniment le même
calcul brut.

La norme Lagrange utilisée dans le document 73 a, en régime \(TS\) grand,
un reste \((TS)^N/(N!L_N)\), où
\(L_N=(2N)!/(2^N(N!)^2)\). Stirling place son seuil pratique vers
\(N>eTS/2\). Avec la garde du lemme H, la tête spatiale connaît elle aussi
une croissance doublement exponentielle dans cette architecture.

### Lemme I — Complétude locale des plafonds sous une marge déjà démontrée

À \(S\) fixé, supposons \(Q_W(f)\ge c\|f\|_2^2\) sur \(X_S\), avec
\(c>0\). Il existe \(U_0\) tel que tous les plafonds \(U\ge U_0\)
donnent \(A_{S,U}\ge(c/2)I\) sur le sous-espace polaire \(H_S\).
Ce lemme ne fournit aucune taille effective pour \(U_0\).

**Preuve.** Supposer le contraire. Pour une suite \(U_j\to\infty\),
choisir \(f_j\in H_S\) de masse 1 avec
\[
\int\min(b_S(t),U_j)|\widehat f_j(t)|^2dt<C_S+c/2.
\]
À \(T\) fixé et pour \(U_j\ge a(T)\), la croissance de \(a\) et
\(b_S\ge a\) donnent
\[
\int_{|t|>T}|\widehat f_j(t)|^2dt
\le\frac{C_S+c/2}{a(T)}.
\]
Le membre de droite tend vers 0 quand \(T\to\infty\). Le support spatial
reste dans \([-S,S]\). Les deux confinements impliquent la précompacité
\(L^2\) de la suite : couper la Fourier à \([-T,T]\) donne un opérateur
de Hilbert–Schmidt du support fixé vers cette bande, et le reste est
uniformément petit. Une sous-suite converge donc fortement vers un
\(f\in H_S\) de masse 1. Pour chaque plafond \(V\) fixé, et \(j\)
assez grand, \(\min(b_S,V)\le\min(b_S,U_j)\). La forme de
\(\min(b_S,V)\) est bornée sur \(L^2\), donc la limite satisfait
\(\int\min(b_S,V)|\widehat f|^2\le C_S+c/2\). Faire
\(V\to\infty\) par convergence monotone montre que \(f\in X_S\)
et \(Q_W(f)\le c/2\), ce qui contredit la marge supposée. □

Cette preuve explique pourquoi l'échec d'un plafond particulier ne ferme
pas toute la famille à ce support. Elle utilise comme hypothèse le signe
local que l'on cherche à certifier ; elle ne peut servir à l'affirmer sans
autre preuve. La couverture de tous les supports conserve son verrou.

## 6. Le contrat global à remplir, sans circularité

Une famille de certificats opératoires suffirait si, pour chaque entier
\(n\), on construisait \(S_n\to\infty\), \(U_n,T_n,N_n,h_n,H_n\),
des matrices \(M_{n,\pm}\), des budgets \(\delta_{n,\pm}\) et des
plafonds rationnels \(\tau_{n,\pm}\) tels que :

1. Le minorant exact et son domaine sont ceux de \(Q_W\) sur \(X_{S_n}\).
2. Le poids fréquentiel exact est nul au-delà de la coupure déclarée, par une
   preuve de queue entière.
3. \(\|B_{n,\pm}-\widetilde B_{n,\pm}\|\le\delta_{n,\pm}\), avec
   toutes les erreurs de quadrature, table, vecteurs, interpolation et arrondi.
4. \(\lambda_{\max}(M_{n,\pm})\le\tau_{n,\pm}\), par opérations
   exactes ou une factorisation résiduelle validée.
5. \(c_n=U_n-C_{S_n}-\max_\pm(\tau_{n,\pm}+\delta_{n,\pm})\ge0\).
6. Une preuve générale établit ces contrats pour tout \(n\), ou établit
   la terminaison de l'algorithme qui les fournit.

Les cinq premières conditions à un \(n\) fixé produisent un certificat
local. La sixième ferme la couverture. La proposition
« une bonne taille existe pour chaque support et la marge reste positive »
ne doit pas être une prémisse non démontrée : elle contient exactement
le verrou de RH de cette route.

Un mécanisme global plus conceptuel pourrait fournir une identité
\(\mathcal Q_r(f)=\|\mathcal A_rf\|^2+\mathcal R_r(f)\) avec
\(\mathcal R_r\ge0\) et domaines vérifiés, ou un Schur signé dont une
inégalité arithmétique couvre tous les \(r\). L'existence d'une telle
factorisation reste à construire. Les nouvelles graines, moments et
translations peuvent en organiser la recherche ; ils ne l'impliquent pas.

## 7. Risques précis de la transposition vers S=0,55

Le module `common_operator_certificate.py` refuse explicitement tout autre
port que \(S=1/2\) et tout autre jeu que \(U=8,T=90,N=80\),
\(h=1/1000,H=1/100,K=256\), 44 bits fixes. Ce refus est correct.
La version actuelle de son sinus a un contrat de phase \(|z|\le45\),
l'exponentielle un contrat \(|z|\le1/4\), et les ondes une norme \(\le1\).
Ces gardes doivent être adaptées avant une transposition.

Pour \(S=11/20,T=700\), \(TS=385\) et
\[
\frac{(TS)^{512}}{512!L_{512}}\simeq4,90468\,10^4,
\qquad
\frac{(TS)^{640}}{640!L_{640}}\simeq7,55906\,10^{-57}.
\]
Une précision ponctuelle excellente avec 512 nœuds n'est donc pas couverte
par ce reste de Lagrange. Cela indique l'échec d'une borne, pas celui de la
quadrature ni une négativité de la forme.

Le budget poids et cellules de V6.48, environ 0,00372087, dépasse la marge
exploratoire annoncée pour \(S=0,55\), environ 0,000583. Recopier ce budget
ne peut pas certifier cette marge. Les constructions nouvelles de poids de
cellules et de queue scalaire visent précisément cette perte. Elles doivent
encore être raccordées à un plafond matriciel validé et au reste de tout
l'espace avant d'annoncer un nouveau théorème.

Les premiers actifs sont 2 et 3, avec \(\log3<1,1<\log4\). Leur
disjonction de bandes à ce support donne
\(|Q_{\rm pr}|\le(c_2+c_3)\|f\|_2^2\), mais pas une suppression
de leurs phases dans le calcul conjoint. Pour convertir une marge massique
\(c>0\) en marge \(R\), prendre \(L=C_0+c_2+c_3\) et
\(\mu=c/(c+L+1)\).

## 8. Vérification bibliographique récente et comparaison des domaines

Le primaire [Z26], version 2, annonce une positivité jusqu'à
\(L=0,8\) sur toute la classe complexe compacte. Les sections 5–6 décrivent
la certification ; les artefacts et le vérificateur sont annoncés en
section 17. Cette lecture n'est pas une reproduction des fichiers de preuve.
Le nom actuel de l'auteur est Xuefeng Zhu. L'équation (2) conserve un terme
polaire, tandis que celui-ci s'annule dans notre classe de moments :
\(L=S\), la transformée non unitaire vaut \(\sqrt{2\pi}\widehat f\).
Les infima sur la classe entière et sur son sous-espace polaire diffèrent,
donc leurs marges ne se comparent pas directement. Les déclarations locales
au-delà de 1/2 doivent être situées bibliographiquement. La barrière discutée
dans ce préprint concerne des certificats par enveloppe ponctuelle ; sa loi
Landau–Widom est annoncée comme empirique, pas comme une impossibilité
universelle de prouver RH.

## 9. Thèse, antithèse, décision

**Thèse constructive.** Le transport \(T_r\) et sa loi de composition
fabriquent un système de traduction global. Le contrôle des moments et du
cœur est exact. Les nouveaux budgets de quadrature peuvent donner une
extension locale et plusieurs outils réutilisables.

**Antithèse critique.** Ce système conserve le domaine, pas le signe. Le
plafond et la garde de queue actuels grossissent à une échelle qui rend la
répétition brute impraticable. Même un succès local supplémentaire ne prouve
pas une loi arithmétique couvrante ; RH reste dans \(\forall r\).

**Décision proposée.** Conserver l'essai 0,55 comme test d'intégration des
briques. Faire du transport et de la forme \(\mathcal Q_r\) le cadre du
prochain travail conceptuel. Exiger que chaque nouvel outil ferme un contrat
identifié — domaine, erreur, dette ou compensation — et présente la portée
de ce contrat. La cible suivante est une identité ou inégalité de signe
valable pour une famille non bornée, avec hypothèses plus faibles que RH.

## Références et sources de cet audit

- [CC21] A. Connes et C. Consani, *Weil positivity and Trace formula, the
  archimedean place*, texte auteur, 4 juillet 2021. Critère : introduction,
  équation (4), appendice C proposition C.1. Normalisation : appendice B,
  équations (153)–(154). https://alainconnes.org/wp-content/uploads/Selecta.pdf
- [Z26] Xuefeng Zhu, *Weil positivity in compact windows: a finite reduction,
  certified two-sided bounds, and a Landau–Widom decay law*, arXiv:2608.24827v2,
  version déposée le 2 septembre 2026. Normalisation : (2)–(3). Construction :
  sections 4–6. Limites : sections 14–15. Artefacts annoncés : section 17.
  https://arxiv.org/html/2608.24827v2
- Corpus local V6.49 : documents 68, 70–74 ; modules
  `prime_centered_bridge.py`, `common_operator_certificate.py`,
  `multi_prime_compensation.py` et leurs données de protocoles.

Les lemmes E–H sont ici démontrés dans les conventions du corpus. Une
confirmation numérique ou un article lu ne tient pas lieu de démonstration
de leurs autres conséquences.
