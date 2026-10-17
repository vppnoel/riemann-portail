# Audit réfutatif du transport positif

Le balayage par blocs quantiles apporte une construction cohérente, mais sa
réussite à tous les rangs est exactement équivalente à la domination des puts.
Dans le cadre zêta, elle est donc exactement équivalente à RH. Il évite un
passage à la limite dangereux ; il ne supprime pas l'obligation arithmétique
infinie.

## 1. Conditions de bord

On écrit `Pλ(t)=∫(t-y)+ λ(dy)`. Les mesures données satisfont

    Pμ(t)−Pν(t)=mt                     (0≤t≤T),
    Pμ(t)−Pν(t)=S(t)                   (t≥T).

Les trois conditions nécessaires sont : `mT=S(T)`, la pente gauche `m`, et le
saut de pente `μ{T}−ν{T}=a−m`, avec `a=S'(T+)`. Le terme `q=2` est déjà absorbé
dans `a`; la somme atomique de ν doit donc être strictement `log q>T`.

Valeurs à 50 chiffres de travail (aucune assertion d'intervalles ici) :

    S(T) = 0.063555586037570414238712283438725700692725015264564
    m    = 0.091691328797194680593651036778631536351278698717481
    a    = −0.26515392328408097187166697222900375969999776704518
    ν{T} = 0.35684525208127565246531800900763529605127646576266
    μ{T} = 0.

Pour les restrictions μ_R,ν_R à `[0,R]`, poser

    h=S(R),  s=S'(R+) = μ_R([0,R])−ν_R([0,R]).

Alors la différence des premiers moments vaut exactement `Rs−h`. Si R est
un logarithme de puissance première, le signe `+` doit inclure cet atome.
Pour `t≥R`, le put de la paire tronquée est `h+s(t−R)`.

Une paire finie de même masse et de même premier moment doit donc satisfaire
les deux conditions terminales `h=0` et `s=0`. La positivité de S sur le seul
intervalle `[0,R]` ne suffit pas. Sous RH, `S(R)>0` pour R>0 : les restrictions
brutes ne sont jamais directement en ordre convexe.

## 2. Pourquoi des extensions finies peuvent tromper

Supposons le put tronqué positif sur `[0,R]`, et h≥0. Choisir B>R, et poser

    d=h/(B−R),  k=s+d.
    μ_B = μ_R + (−k)+ δ_R + d δ_B,
    ν_B = ν_R + k+ δ_R.

La différence des puts après R est `h−d(t−R)` jusqu'à B, puis zéro. Ces
mesures sont positives, de même masse, de même premier moment et en ordre
convexe. Il existe donc un transport martingale fini pour chaque B, quelle
que soit la conduite du vrai S après R.

Mais `dδ_B` tend vaguement vers zéro quand B→∞ alors que son premier moment
`Bd` tend vers h. C'est une perte de premier moment exacte, et non un détail
de compacité. Une extension finie obtenue par des atomes de correction est
un certificat pour la paire modifiée, pas pour les mesures originales.

Autre obstruction de bord : si une fermeture remplace une queue source
par `Dδ_L`, avec D>0, on ne peut rouvrir cet atome en une combinaison
positive d'atomes x>L tout en conservant sa masse D et son moment DL.
Le moment de cette combinaison serait `DL+Σc_x(x−L)>DL` (ou infini).
La ligne de fermeture reste donc fictive : seules les vraies lignes
antérieures peuvent être conservées, et la réouverture doit apporter de
nouvelles réserves de μ pour satisfaire le nouveau moment.

Contre-exemple minimal, même sous domination par une mesure fixe localement
finie :

    α=δ_1,
    η_N=(1−1/N)δ_0+(1/N)δ_N,
    M=δ_0+Σ_(N≥2)(1/N)δ_N.

Chaque η_N≤M a masse 1 et barycentre 1. Le transport `δ_1→η_N` est une
martingale. Pourtant `η_N⇒δ_0`, de barycentre zéro. Une suite de certificats
dominés par une réserve infinie ne conserve donc pas nécessairement le
barycentre. Il faut une uniformité des premiers moments de chaque ligne,
ou fixer la ligne une fois pour toutes.

## 3. Théorème du balayage quantile sur une réserve infinie

**Théorème.** Soit μ une mesure positive localement finie sur `[0,∞)`, de
masse infinie, et ν une mesure atomique localement finie
`ν=Σ_i c_iδ_(x_i)`, avec c_i>0 et x_i≥0. Énumérer tous ses atomes. À chaque
rang, prendre dans le reliquat de μ le bloc de c_i unités consécutives de
masse quantile dont le barycentre est x_i, puis le retirer. Le balayage
réussit à tous les rangs si et seulement si

    Pν(t)≤Pμ(t)  pour tout t≥0.

La réserve après un nombre fini de retraits reste infinie. Si Q est sa
fonction quantile, la moyenne du bloc est

    B_c(s)=(1/c)∫_[s,s+c] Q(u)du.

Elle est continue et croissante, tend vers l'infini, et son minimum est
`B_c(0)`. Ainsi le critère exact de l'étape est `B_c(0)≤x`. Les atomes aux
extrémités peuvent être fractionnés. Des paramètres s différents dans un
plateau donnent la même sous-mesure.

**Preuve de la suffisance du balayage.** Chaque bloc η_i a masse c_i et
premier moment c_ix_i. Les retraits impliquent `σ=Σ_iη_i≤μ`. Jensen puis
Tonelli donnent `Pν≤Pσ≤Pμ`. Les puts sont finis sur tout compact, grâce à
la finitude locale et au support positif. Aucun premier moment global
infini n'est soustrait.

**Preuve du sens inverse.** Pour un préfixe fini α de ν, on a `Pα≤Pμ`.
Prendre R contenant le support de α et noter sa masse M et son premier
moment D. Choisir B>R assez grand pour que λ=μ|[0,B] vérifie

    λ([0,B])≥M,  Cλ(R)=∫(y−R)+λ(dy)≥D.

Cela est possible parce que la masse de la queue de μ est infinie. Pour
`t≤B`, les puts de λ sont ceux de μ. Pour `t≥B`, leur différence avec ceux
d'α est affine de pente non négative, déjà positive en B. Les calls sont
également dominants : pour `0≤t≤R`, `Cλ(t)≥Cλ(R)≥D≥Cα(t)`; pour t≥R, le
call d'α est nul; pour t<0, la domination découle de la masse et du premier
moment de λ. Les constantes, calls et puts engendrent les fonctions
convexes positives. On a donc `α≤_E λ`, ordre convexe étendu fini.

L'ombre finie existe. L'ombre d'un atome est exactement le bloc quantile de
bonne masse et de bon barycentre, et l'associativité garantit la réussite
de toutes les étapes du préfixe. Tous ces blocs sont dans `[0,B]`; les
quantiles de λ et μ y coïncident, donc les étapes sont celles du balayage
sur μ. Comme le préfixe était arbitraire, le balayage infini réussit.

Référence finie utilisée : Beiglböck–Juillet, *On a problem of optimal
transport under marginal martingale constraints*, Definition 4.3,
Proposition 4.4, Lemma 4.6, Example 4.7 et Theorem 4.8.

**Application zêta.** La domination des puts est `S≥0` pour t≥T et `mt≥0`
avant T. Ainsi, une fois le raccord initial vérifié,

    balayage réussi à tous les rangs ⇔ S≥0 ⇔ RH.

Il s'agit d'un résultat conditionnel d'existence exact, pas d'une preuve
de réussite inconditionnelle. Le critère glouton n'est pas plus fort que
le critère du signe : son infinité en est une reformulation.

Pour un préfixe ordonné fini, on a plus précisément : réussite des n
étapes ⇔ `Pα_n≤Pμ` partout. Avec le raccord initial, le put tronqué est
exactement `A(t)−Σ_(q≤q_n)c_q(t−log q)+` pour t≥T. Comme la somme des
hinges est le maximum des droites de préfixes, cette condition est
équivalente aux mêmes inégalités de Fenchel pour les préfixes concernés.
Le balayage réexprime donc aussi exactement le diagnostic fini ; il ne
convertit pas les 194 tests en certificat pour la queue.

## 4. Sous-transport fini et résidu légitime

Un certificat fini valable consiste en des mesures η_i≥0 avec

    η_i(R)=c_i,  ∫yη_i(dy)=c_ix_i,  Σ_(i≤n)η_i≤μ.

Poser α_n=Σ_(i≤n)c_iδ_(x_i), σ_n=Σ_(i≤n)η_i, ρ_n=μ−σ_n≥0 et
`G_n=Pσ_n−Pα_n≥0`. L'identité exacte est

    S = G_n + Pρ_n − P(ν−α_n)              (t≥T).

Lorsque le préfixe contient tous les atomes avant R, le put de `ν−α_n`
est nul pour t≤R. Le certificat établit donc légitimement `S≥0` sur cette
fenêtre, y compris si les blocs η_i dépassent R. Le reliquat ρ_n est une
vraie mesure positive, sans atome fictif de correction.

Pour une preuve globale, il reste à dominer les puts de `ν−α_n` par ceux
de ρ_n. Cette obligation ne disparaît pas. Si les η_i sont supportées dans
`[0,B]`, alors G_n(t)=0 pour t≥B. Plus généralement, σ_n a masse et premier
moment finis, égaux à ceux d'α_n, donc G_n(t)→0. Un transport fini n'ajoute
aucune marge constante dans la queue.

Le théorème fini explicite permettant de produire le certificat est
`α_n≤_E λ` pour une réserve finie `λ≤μ`. Il garantit une sous-mesure
`η≤λ` telle que `α_n≤_cx η`, ou permet directement les blocs quantiles
successifs. Masse, calls et puts sont les conditions de vérification.
Lorsque λ est la densité β sur un nombre fini d'intervalles et des atomes,
les différences de puts/calls sont convexes entre les atomes : leurs
minima se trouvent aux bornes ou aux zéros de la dérivée. Ces vérifications
peuvent donc être finies et rigoureusement encadrées.

## 5. Le résidu d'un balayage infini disparaît automatiquement

Si toutes les étapes réussissent, `σ≤μ` donne déjà S≥0, donc RH. Suzuki
2023, Theorem 1.6, implique alors que S est bornée. Pour `ρ=μ−σ≥0`, Jensen
donne `Pρ≤S`. Toute masse positive de ρ dans un compact K entraîne
`Pρ(t)≥(t−sup K)ρ(K)`, une contradiction. Ainsi ρ=0.

Le sous-couplage construit ligne par ligne est donc finalement un
couplage complet, sans qu'il soit nécessaire de l'imposer d'abord ou
d'appliquer un Strassen infini. C'est un avantage de construction réel.

## 6. Obstructions à des familles précises de noyaux

1. **Noyaux entièrement atomiques.** Pour un atome source x>T, tout atome
   terminal y>T est interdit par `σ≤μ`, puisque μ{y}=0. Une probabilité
   purement atomique ne pourrait alors être supportée qu'en 0 et T, et
   aurait un barycentre ≤T. Les noyaux à deux points, à un nombre fini de
   points ou à support dénombrable sont donc impossibles pour les lignes
   x>T. Il faut une composante diffuse.

2. **Loi de déplacement fixe centrée.** Supposons, pour toutes les grandes
   lignes, `K_x(dy)=k(d(y−x))`, avec k de portée bornée et de moyenne zéro.
   Le théorème des nombres premiers et β(t)~e^(t/2) imposent

       ∫e^(−z/2)k(dz)=1.

   En effet la masse d'un intervalle `[t,t+h]` est asymptotiquement
   `2(e^(h/2)−1)e^(t/2)` pour les deux mesures ; la convolution multiplie
   ce coefficient par l'intégrale affichée. Jensen strict impose
   k=δ_0, incompatible avec le caractère diffus de μ. Cette famille est
   donc impossible, sans supposer RH au préalable.

3. **Portée bornée et dispersion uniforme.** Si `|Y−x|≤D` et si le couplage
   existe, S est bornée sous RH. Pour le gap d'une ligne,

       g_x(t)=∫(t−y)+K_x(dy)−(t−x)+,
       ∫g_x(t)dt=Var(K_x)/2.

   Le support de g_x est dans `[x−D,x+D]`. En intégrant sur
   `[r−D,r+h+D]`, on obtient

       ∫_[r,r+h]Var(K_x)ν(dx) ≤ 2||S||∞(h+2D).

   Or `ν([r,r+h])~2(e^(h/2)−1)e^(r/2)`. La variance moyenne pondérée doit
   donc être O(e^(−r/2)). Une variance uniformément minorée par v>0, ou
   une fraction uniforme de sauts de taille ≥δ>0, est impossible.
   **La portée bornée seule n'est pas exclue** : des noyaux variables dont
   la dispersion devient très petite restent possibles en principe.

4. **Marge de signe uniforme.** Une borne `S(t)≥ε>0` pour tous les grands t
   implique RH par la preuve de Suzuki 2025 appliquée à ξ, sans zéros
   réels ; sous RH, la série absolument convergente
   sur les zéros et la récurrence simultanée des phases donnent
   `inf_(t≥R)S(t)=0` pour tout R. Cette marge est donc impossible. Le même
   argument donne `liminf_j[L_j−A_T*(C_j)]=0` sous RH : aux instants où
   S est petit, le préfixe actif a un minimum de Fenchel au plus égal à S.
   Attention : une marge de position `x−B_c(0)≥ε` n'est pas cette marge ;
   le défaut dual est `c[x−B_c(0)]`, et c tend vers zéro.

## 7. Réserve à zéro et obstruction propre au shadow canonique

Soit α_N le préfixe contenant la vraie ligne de bord ν{T}δ_T et les
puissances premières suivantes, et σ_N son shadow dans μ. Pour un
préfixe réalisable, poser `S_N=Pμ−Pα_N`, prolongé par zéro pour t<0.
On a exactement

    P(μ−σ_N)=conv(S_N),
    r_N:=(μ−σ_N){0}=inf_(t>0)S_N(t)/t.

La formule du potentiel résiduel est la formule finie de l'ombre,
transposée des potentiels absolus U aux puts P (l'ajout affine ne change
pas l'enveloppe convexe). Pour la réserve infinie, choisir une troncature
B contenant tous les blocs déjà retirés : le shadow y est identique et
de support compact. Le put résiduel égale S_N au-delà de ce support.
Si une minorante convexe du vrai S_N dépassait le put résiduel avant B,
prendre leur maximum, qui coïncide avec S_N près de B, puis le prolonger
au-delà de B par la droite du potentiel tronqué. On obtiendrait une
minorante convexe du signal tronqué supérieure à son enveloppe finie,
une contradiction. Cela justifie la formule sur toute R.

Pour la pente, une fonction convexe g avec g(0)=0 vérifie
`g'_+(0)≤g(t)/t≤S_N(t)/t`. Réciproquement, si r est l'infimum affiché,
`r·t+` est une minorante convexe de S_N. Sa pente en zéro impose celle de
l'enveloppe. La dérivée droite d'un put en zéro est exactement la masse
de l'atome zéro.

Pour t≥T, le signal tronqué s'écrit
`min_(j≤N)[A(t)−C_jt+L_j]`. Donc

    r_N=min(m, min_(j≤N)d_j),
    d_j=inf_(t≥T)[A(t)+L_j]/t−C_j.

Écrire `Q(t)=tA'(t)−A(t)`. Comme `Q'(t)=tβ(t)>0`, si L_j≥Q(T), l'unique
minimiseur τ_j≥T est donné par `Q(τ_j)=L_j`, et

    d_j=A'(τ_j)−C_j.

Si L_j<Q(T), le minimum est au bord T et vaut
`[A(T)+L_j]/T−C_j`. Dans notre cadre, tous les préfixes contenant q=2
ont `L_j≥L_2≈0.33973158>Q(T)≈0.09238530` : le cas intérieur s'applique.
Attention : ν{T} vaut m−a et n'est pas le poids c_2. Le raccord convertit
ce poids de bord en la bonne droite première de pente c_2.

Si θ_j résout `A'(θ_j)=C_j`, le défaut de Fenchel H_j et la réserve
radiale d_j vérifient les identités exactes

    H_j=L_j−A_T*(C_j)=∫_[θ_j,τ_j]uβ(u)du,
    d_j=∫_[θ_j,τ_j]β(u)du.

Ici tous les θ_j sont intérieurs, car `C_j≥c_2>A'(T)`. H_j et d_j ont
exactement le même signe. Lorsque H_j≥0,
`θ_jd_j≤H_j≤τ_jd_j`. Voilà le pont entre Fenchel, stock et records.

Sous RH, chaque S_N est strictement positive pour t>0, égale mt avant T,
et son quotient par t tend vers l'infini à l'infini (N est fini). Donc
`r_N>0` pour tout N. Mais S_N décroît vers S après T, et S est bornée;
les infimums commutent, donc `r_N↓0`. L'ombre laisse une partie de l'atome
zéro à tout rang fini et doit en consommer encore à des rangs arbitrairement
grands. Une infinité de lignes de source x→∞ ont ainsi `K_x{0}>0`.

**Conclusion précise : tout balayage shadow complet réussi dans ce cadre
a une portée non bornée.** Cette obstruction ne s'étend pas automatiquement
aux couplages non minimaux, qui peuvent consommer plus tôt une plus grande
part de la réserve gauche.

Diagnostic du premier préfixe : `τ_2≈0.92237765142377` et
`r_2≈0.03949864651243`, contre `m≈0.09169132879719` initialement.

## 8. Statut

- Prouvé : raccords, corrections finies, mécanisme de perte de moment,
  validité du sous-transport, et équivalence du balayage à la domination
  globale des puts.
- Conditionnel à RH : existence du balayage infini et épuisement de μ.
- Impossible pour les familles indiquées : noyaux entièrement atomiques,
  déplacement fixe centré de portée bornée, dispersion uniforme à portée
  bornée, marge de signe ou de Fenchel uniforme, et portée bornée pour
  le balayage shadow canonique complet.
- Encore ouvert : une estimation arithmétique indépendante qui garantit
  toutes les étapes, un invariant de reliquat vérifiable par une induction
  finie, et la possibilité d'une portée uniformément bornée avec des
  noyaux variables qui se concentrent.

## Sources primaires consultées

- Suzuki 2023 : https://arxiv.org/pdf/2206.03682, Theorems 1.1, 1.6, 1.7.
  Références de navigation : turn140view0, turn142view1.
- Suzuki 2025 : https://arxiv.org/pdf/2209.12832, Theorem 1.1 et preuve §3.
  Références de navigation : turn149view1, turn142view0.
- Beiglböck–Juillet :
  https://www.mat.univie.ac.at/~mathias/MartingaleTransport_BJ.pdf,
  Example 4.7 et Theorem 4.8 pour les blocs et l'associativité ;
  Definition 4.3/Proposition 4.4/Lemma 4.6 pour le sous-transport fini.
  Références de navigation : turn149view0, turn149view2, turn148view1.
- Brückerhoff–Huesmann–Juillet, *Shadow martingales*, Lemma 4.12 :
  https://juillet.perso.math.cnrs.fr/papers/MnMs.pdf,
  formule explicite de l'enveloppe convexe du potentiel résiduel.
  Références de navigation : turn153view0, turn153view1.

Les extensions infinies et les obstructions ci-dessus sont des déductions
de cet audit, pas des théorèmes attribués aux articles consultés.
