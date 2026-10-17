# Balayage quantile, réserve radiale et fermeture finie

## Résultat exploitable

On peut construire un noyau directement sur la vraie mesure archimédienne
`μ`, sans discrétiser sa densité. À chaque atome de `ν`, on retire du reliquat
un bloc de quantiles de même masse et de même barycentre. La réussite de toutes
les étapes produit un sous-couplage σ-fini par une somme explicite. Elle suffit
à prouver `S≥0` par Jensen ; aucun théorème de Strassen pour des mesures de masse
infinie n'est utilisé.

Le calcul à 60 chiffres pour `q≤1000` réussit et livre les morceaux du noyau,
mais reste un diagnostic sans arrondis par intervalles. La masse résiduelle au
point 0 vaut exactement, pour le balayage mathématique,

\[
r_N=\inf_{t>0}\frac{P_\mu(t)-P_{\nu_N}(t)}{t}.
\]

C'est un budget de transport concret, calculable par des records de déficits
radiaux. Sa nonnégativité à tous les préfixes est encore une obligation globale
équivalente à RH. La construction ne l'établit pas.

## 1. Mesures et noyau élémentaire

On écrit `P_η(t)=∫(t−u)_+η(du)`. Dans les mesures fournies au départ,

\[
T=\log2,\quad m=0.09169132879719468059\ldots,
\quad a=-0.26515392328408097187\ldots,
\]

donc, dans ce cas précis,

\[
\mu=m\delta_0+1_{(T,\infty)}\beta(u)\,du,
\qquad
\nu=(m-a)\delta_T+\sum_{q>2}c_q\delta_{\log q}.
\]

L'atome de `ν` en T a la masse
`m−a=0.35684525208127565247…`. Ce n'est pas la masse première originale
`c₂=log2/√2=0.49012907173427359586…` ; la représentation a absorbé le terme
initial de pente dans cet atome de demande.

**Lemme du bloc.** Soit R un reliquat positif, localement fini sur `[0,∞)`,
de masse infinie, avec quantile G_R. Pour un atome `cδ_x`, `c>0`, il existe un
sous-mesure θ≤R de masse c et de barycentre x si et seulement si

\[
B_c(0):=\frac1c\int_0^cG_R(v)\,dv\le x.
\]

Si l'inégalité est satisfaite, prendre une solution `s≥0` de

\[
B_c(s)=\frac1c\int_s^{s+c}G_R(v)\,dv=x,
\qquad
\theta=(G_R)_\#1_{[s,s+c]}dv,
\qquad K_x=\theta/c.
\]

Pour une source finie de masse M, il faut en plus `c≤M` et
`x≤B_c(M−c)`.

*Preuve.* La fonction B_c est continue et non décroissante, car elle est une
différence de primitives du quantile. Comme R est localement finie de masse
infinie, `G_R(v)→∞`, donc `B_c(s)→∞`. L'existence du bloc suit de la valeur
intermédiaire. Le bloc conserve sa masse et son premier moment par définition.
Inversement, parmi toutes les sous-mesures de R de masse c, les c unités de
masse les plus à gauche minimisent le premier moment. Cela se démontre par
`θ((t,∞))≥(c−R([0,t]))_+` et l'intégration en t. Ainsi une sous-mesure de
barycentre x impose `c x≥∫_0^cG_R`.

**Algorithme.** Ordonner les atomes de ν par positions croissantes, y compris
l'atome de demande en T. Initialiser `R₀=μ`. À l'étape j, appliquer le lemme à
`R_{j−1}` et à `c_jδ_{x_j}`, puis poser `R_j=R_{j−1}−θ_j`.
L'invariant automatique est `R_j≥0` et la conservation de la masse et du
barycentre de chaque ligne. La faisabilité `B_{c_j}(0)≤x_j` constitue le test,
et non un invariant qu'on peut postuler.

## 2. Passage σ-fini sans fuite de masse

**Lemme de sommation.** Si toutes les étapes réussissent, alors

\[
\sigma=\sum_j\theta_j\le\mu,
\quad
\pi=\sum_j\delta_{x_j}\otimes\theta_j,
\quad
\rho=\mu-\sigma\ge0
\]

définissent un sous-couplage explicite de ν vers μ : la première marginale
de π est ν, la seconde est σ, et chaque noyau `θ_j/c_j` a moyenne x_j. Pour
tout t≥0,

\[
S(t)=P_\rho(t)+\sum_j
\left[\int(t-u)_+\theta_j(du)-c_j(t-x_j)_+\right]\ge0.
\tag{1}
\]

*Preuve.* Les mesures finies `∑_{j≤n}θ_j` sont croissantes et dominées par μ,
donc leur somme définit σ. π est σ-finie, car ν possède un nombre fini
d'atomes sur chaque compact. Pour t fixé, `P_μ(t)<∞` et `P_ν(t)<∞` ; les
deux sommes de puts convergent donc séparément, ce qui justifie (1). Chaque
crochet est non négatif par Jensen. Il n'y a ni compactness globale ni échange
de deux quantités infinies dans cette preuve.

La surjectivité vers toute μ n'est pas requise pour Jensen. Elle suit pourtant
après coup : le succès donne `S≥0`, donc RH par Suzuki ; sous RH, S est bornée.
Si `ρ([0,R])>0`, (1) donnerait `S(t)≥(t−R)ρ([0,R])` pour t≥R, une
contradiction. Le reliquat final doit donc être nul.

Pour la réciproque, on peut rester entièrement dans le cadre fini : les ombres
atomiques et leur associativité dans Beiglböck–Juillet assurent la réussite du
balayage pour deux mesures finies en ordre convexe. La fermeture de la section
4 fournit ces mesures finies pour chaque préfixe sous `S≥0`. On choisit le cap
assez grand pour contenir les lignes déjà retirées ; les premiers blocs quantiles
sont alors ceux de la source infinie. Cela justifie la réussite sous RH sans
invoquer un résultat de transport infini.

## 3. Identité exacte de la réserve au point 0

Notons `H_N=P_μ−P_{ν_N}`, où ν_N contient le véritable atome de demande en T
et un préfixe des atomes `q>2`, et `r_N=R_N({0})`.

**Lemme de réserve radiale.** Pour tout balayage quantile réussi sur ce
préfixe croissant,

\[
r_N=\inf_{t>0}H_N(t)/t.
\tag{2}
\]

*Preuve.* Jensen pour les N lignes donne `H_N(t)≥P_{R_N}(t)≥r_N t`, donc
`r_N≤inf H_N/t`. Si aucune ligne n'a consommé l'atome en 0, le rapport vaut
m pour les petits t>0, et l'égalité suit. Sinon, soit k la dernière ligne ayant
consommé une partie de cet atome, et b son extrémité droite. Son extrémité
gauche est 0 et `b>x_k`. Le retrait d'un bloc de quantiles épuise tout le
reliquat dans l'intervalle ouvert entre ses extrémités ; après k, le seul
reliquat dans `[0,b)` est donc `r_Nδ₀`.

Toutes les lignes précédentes ont leur extrémité droite ≤b. En effet, b est
dans l'adhérence du support du reliquat avant k, et ne peut être à l'intérieur
d'un intervalle déjà balayé. Si une ancienne ligne avait son extrémité droite
>b, son extrémité gauche serait ≥b, donc son barycentre serait ≥b>x_k,
ce qui contredirait l'ordre croissant des barycentres. Ainsi tous les crochets
de Jensen des premières k lignes s'annulent au point b, et `H_k(b)=r_N b`.
Les lignes suivantes, qui ne consomment plus 0, prennent leur masse à des
positions ≥b, donc leurs barycentres sont ≥b. Elles ne modifient pas `H_N(b)`.
D'où `H_N(b)=r_N b`, ce qui prouve (2).

Cette preuve utilise la densité strictement positive au-dessus de T pour que
l'extrémité droite b, quand la ligne contient 0, soit une vraie extrémité de
support. Les deux atomes initiaux sont traités explicitement.

Pour le préfixe original terminé en `q_j`, poser

\[
C_j=\sum_{q\le q_j}c_q,
\qquad P_j=\sum_{q\le q_j}c_q\log q,
\qquad x_j=\log q_j.
\]

Pour `t≥x_j`, `H_j(t)=A(t)−C_j t+P_j`. L'ajout de l'atome ne change pas le
potentiel avant x_j. On obtient donc la règle de records

\[
r_j=\min\left(r_{j-1},\inf_{t\ge x_j}
              \frac{A(t)-C_jt+P_j}{t}\right).
\tag{3}
\]

Le minimum du nouveau rapport est unique : sa dérivée a le signe de
`tA'(t)−A(t)−P_j`, et la dérivée de cette expression est `tβ(t)>0`. Si le
minimum est intérieur, sa position τ_j satisfait

\[
\tau_j A'(\tau_j)-A(\tau_j)=P_j,
\qquad d_j^{\rm radial}=A'(\tau_j)-C_j.
\]

Sinon il est au bord x_j. Pour le premier atome de demande en T, la formule
sur t≥T correspond au préfixe original `q=2`, avec C₂=c₂ et P₂=c₂T ; on ne
remplace pas la masse de demande `m−a` par c₂.

**Obstruction de portée pour ce glouton.** Sous RH, Suzuki donne `S(t)>0`
pour t>0. Tous les potentiels de préfixes sont alors strictement positifs.
Par (2) et l'attainment démontré ci-dessus, `r_N>0` après tout préfixe fini.
Or la sommation globale force `r_N↓0`. Il faut donc une infinité de lignes
envoyant une masse positive vers 0, depuis des positions x_j arbitrairement
grandes. Le noyau quantile construit n'a pas de portée uniformément bornée.
Ceci n'exclut pas un autre noyau martingale de portée bornée.

## 4. Budget exact pour fermer une troncature

Pour un seuil X, `L=log X`, ν_X contient le vrai atome en T et les atomes
premiers `2<q≤X`. On prolonge son potentiel par

\[
S_X(t)=A(t)-C_Xt+P_X\quad(t\ge L).
\]

Supposons `S_X(L)>0`. Il existe un unique `U>L` satisfaisant

\[
\int_L^U(u-L)\beta(u)du=S_X(L).
\tag{4}
\]

Poser `D=S_X'(U)=A'(U)−C_X`. Si D≥0, les mesures finies

\[
\mu_U=\mu|_{[0,U]},\qquad
\widehat\nu_X=\nu_X+D\delta_L
\]

ont exactement la même masse et le même premier moment. Leurs puts diffèrent
de

\[
P_{\mu_U}(t)-P_{\widehat\nu_X}(t)=
\begin{cases}
P_\mu(t)-P_{\nu_X}(t),&t\le L,\\
\int_t^U(u-t)\beta(u)du,&L\le t\le U,\\
0,&t\ge U.
\end{cases}
\tag{5}
\]

*Preuve.* La différence de masses est `S_X'(U)=D`. La différence des premiers
moments est `UD−S_X(U)`. L'identité (4), obtenue aussi par intégration par
parties, est `S_X(U)=(U−L)D`, donc ce premier moment vaut LD. Après l'ajout
de `Dδ_L`, la différence sur `[L,U]` a courbure β et valeur/pente nulles en U,
ce qui donne (5).

Le signe D n'est pas automatique. Si `S_X'(L)<0` et v>L est le point de
récupération `S_X'(v)=0`, alors
`∫_L^v(u−L)β−S_X(L)=−S_X(v)`. Ainsi D a le même signe que le minimum de
récupération `S_X(v)` ; si la pente initiale est non négative, D>0. Cela
identifie précisément l'hypothèse arithmétique derrière une fermeture positive.
L'atome `Dδ_L` est une demande artificielle de bord : (5) n'affirme rien sur
sa réalisation par les futurs premiers.

## 5. Calcul fini et noyau livré

`shadow_sweep_high_precision.py` calcule A et A' par une série géométrique à
140 termes, avec 60 chiffres de travail. Sur t≥T la queue de ces séries est
<10^-84, mais les itérations numériques ne sont pas encadrées par des
intervalles : les résultats ci-dessous ne sont pas appelés certifiés.

| Quantité | X=10 | X=1000 |
|---|---:|---:|
| Nombre de puissances premières q≤X | 7 | 193 |
| Nombre d'atomes premiers q>2 transportés | 6 | 192 |
| Masse réelle de demande en T | 0.356845252081276 | identique |
| S(log X) | 0.0384269622177544 | 0.0559288777557354 |
| Prolongement U−log X | 0.152039194204077 | 0.0588931788592263 |
| Demande artificielle de bord D | 0.601366198695518 | 1.94176217282833 |
| Réserve réelle en u=0 avant le bord | 0.0161772371932264 | 0.00481683660325385 |
| Masse totale source/ν avec bord | 4.00558519330877 | 62.3162348210272 |
| Premier moment total commun | 6.71315908275383 | 327.113961130607 |

Pour X=1000, les 192 lignes premières q>2 et le raccord en T réussissent ;
avec la ligne artificielle de bord, le test contient 194 lignes. Le raccord
en T est distinct de l'atome premier original c₂δ_T. Les erreurs maximales de conservation observées
sont `2.95×10^-59` en masse et `3.33×10^-48` en premier moment. Le reliquat
après fermeture est numériquement nul. Le plus petit écart au test de
disponibilité des lignes premières est `0.0436732617874311`, à q=13.

Avant le bord, la réserve `r₀=0.00481683660325385` contribue
`r₀ log1000=0.0332735284741212` au budget `S(log1000)=0.0559288777557354`.
La ligne q=529 utilise encore 0 et atteint une extrémité droite
`6.27773235549703`, donnant cette grande largeur de noyau. La somme des coûts
quadratiques des lignes premières et du raccord vaut `0.381728513014416` ; celle de la seule
ligne de bord vaut `0.238466738909456`. Ces nombres distinguent clairement
la vraie construction du budget artificiel de clôture.

Le JSON des noyaux représente chaque θ_j par des intervalles `[ℓ,r]` dans
les coordonnées de masse de la source originale μ. Soit G son quantile :

\[
K_{x_j}(B)=\frac1{c_j}\sum_{[\ell,r]}\int_\ell^r1_B(G(v))dv.
\]

Il s'agit donc de restrictions de la véritable densité β, avec les fractions
nécessaires de l'atome en 0. Il n'y a aucune approximation par un centroïde.
Les primitives utilisées pour inverser le quantile sont

\[
M(u)=m+A'(u)-A'(T),\qquad
H(u)=uA'(u)-A(u)-TA'(T)+A(T).
\]

Les premières lignes sont lisibles :

| Demande | Masse | Intervalle extrême de source | Masse laissée en 0 après ligne |
|---|---:|---:|---:|
| T | 0.356845252081276 | [0,0.922377651424…] | 0.0394986465124290 |
| log 3 | 0.634284100597564 | [0,1.295991314392…] | 0.0292590260672238 |
| log 4 | 0.346573590279973 | [1.296692854649…,1.473026734524…] | identique |

Les fichiers `*_radial_records.json` vérifient indépendamment (2)–(3) contre
la réserve calculée par les morceaux du noyau. Pour X=1000, le record est
atteint au préfixe q=529, en

\[
t_*=6.27773235549703098979018343475430752247\ldots,
\quad r_N=0.00481683660325385372318480035031835691844\ldots.
\]

L'écart observé entre le calcul radial et les morceaux du noyau est
`2.72×10^-49` ; la même identité est vérifiée à cette précision pour chacun
des 193 préfixes. Les 387 intervalles de masse des noyaux, bord compris,
forment une partition numérique sans chevauchement ni lacune de la source
finie. Le minimiseur radial du dernier préfixe n'est donc pas celui
qui gouverne la réserve : celle-ci est un record conservé du préfixe q=529.

Exécution :

```sh
PYTHONPATH=/workspace/scratch/72030dde7ad1/v635_runtime_deps \
  "$CODEX_PRIMARY_RUNTIME_PYTHON" shadow_sweep_high_precision.py 1000
```

Le premier argument est facultatif. Les fichiers de sortie portent X dans
leur nom ; la ligne `boundary` est séparée des atomes premiers q>2 et du raccord en T.

## 6. Verrou global précis

Le prolongement utile serait une estimation arithmétique prouvant
`B_{c_j}^{R_{j−1}}(0)≤x_j` à tous les rangs, ou, par la loi radiale, la
nonnégativité de tous les nouveaux budgets de (3). Cela exige les mêmes
annulations fines entre A et les sommes pondérées sur les premiers que RH.
La conservation des blocs, l'extension σ-finie et la fermeture de bord ne
fournissent pas cette estimation. Une marge positive constatée jusqu'à 1000
ne peut pas être extrapolée.

Un développement calculatoire concret est maintenant disponible : calculer
les records radiaux et les masses envoyées vers 0 à chaque nouveau préfixe,
puis tester une règle analytique de mise à jour contre ces records. La
portée non bornée du balayage montre qu'une fermeture purement locale à
longueur constante ne décrit pas ce noyau.

La variante `nonminimal_report.md` conserve un autre raccord initial qui
consomme toute la masse en 0 dès la première ligne. L'identité (2) et son
obstruction via la masse en 0 concernent le balayage minimal décrit ici :
elles ne s'appliquent pas à un raccord initial non minimal arbitraire.

## Sources primaires consultées

- Masatoshi Suzuki, *Aspects of the screw function corresponding to the Riemann
  zeta function*, Theorem 1.7 et §7.2 :
  https://arxiv.org/pdf/2206.03682 ; version publiée, JLMS 108 (2023), 1448–1487.
- Mathias Beiglböck et Nicolas Juillet, *On a problem of optimal transport under
  marginal martingale constraints*, Ann. Probab. 44 (2016), 42–106,
  Exemple 4.7 (ombre d'un atome), Lemme 4.12 (retrait), Exemple 4.20
  (balayage des atomes croissants) :
  https://irma.math.unistra.fr/~juillet/papers/AOP_BJ.pdf.

Les lemmes de sommation, de réserve radiale et de fermeture de bord ci-dessus
sont dérivés explicitement pour les mesures du présent problème ; ils ne sont
pas présentés comme des théorèmes nouveaux de ces sources.
