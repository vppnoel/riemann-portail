# V6.42 — Certifier un pli, sa paire et les opérateurs qui la décrivent

## 1. Objet exact et sélection avant calcul

Le verrou V6.42 reprend la recette Gauss/minor de `k1_rpi_6`, membre plus.
Parmi les six plis attribués de V6.41, la règle choisit celui de plus petite
hauteur absolue, `fold_k1_plus_5`. Les quatre graines de racines proviennent
des sorties V6.41. Aucun nouveau support, rayon de contour ou centre n’est
choisi selon une issue favorable.

La fonction est exactement
$F(r,s)=\cos r\,f_i(s)+\sin r\,f_u(s)$,
où $f_i=z_iL(s,\chi_i)$ et $f_u=\sum u_jz_jL(s,\chi_j)$.
Les $u_j$ sont les mineurs normalisés avec l’orientation du manifeste ;
ils sont réels, de norme un, et $\sum u_jz_j=0$ par l’identité des mineurs.
Le rayon varie : $A=\cos r\,z_i$ varie aussi. Ce travail ne déploie pas
encore un pli sur une fibre à A constant.

## 2. Lemme I1 — Un reste analytique et ses dérivées sont bornés

Pour $a>0$, $s\ne1$ et $\sigma+2M>1$, Euler–Maclaurin donne

\[
\begin{aligned}
\zeta(s,a)={}&\sum_{n=0}^{N-1}(n+a)^{-s}
+{(N+a)^{1-s}\over s-1}+\tfrac12(N+a)^{-s}\\
&+\sum_{k=1}^M {B_{2k}\over(2k)!}(s)_{2k-1}(N+a)^{1-s-2k}
+R_{N,M}(s,a).
\end{aligned}
\]

La série de Fourier des Bernoulli périodiques donne
$|\widetilde B_{2M}(x)|/(2M)!\le2\zeta(2M)/(2\pi)^{2M}$.
L’intégrale du reste implique donc

\[
|R_{N,M}(s,a)|\le
{2\zeta(2M)\over(2\pi)^{2M}}
{|(s)_{2M}|(N+a)^{1-\sigma-2M}\over\sigma+2M-1}.
\]

**Preuve.** Prendre le module dans l’intégrale du Bernoulli périodique
contre $(s)_{2M}(x+a)^{-s-2M}$, puis intégrer
$(x+a)^{-\sigma-2M}$ depuis N. Tous les facteurs sont explicitement
majorés ; $\zeta(2M)\le1+1/(2M-1)$ résulte du test intégral. □

Dans le rectangle déclaré, étendu d’une marge $\delta=1/8$, chaque facteur
$|s+j|$ est majoré à partir des bornes réelles et imaginaires. Pour une
série périodique de période 13,
$L(s)=13^{-s}\sum_{a=1}^{12}T_a\zeta(s,a/13)$,
la somme des modules des $T_a$ et $13^{-\sigma}$ donnent un majorant R
du reste sur ce rectangle étendu. La formule de Cauchy donne ensuite

\[
|\partial_s^k R_L(s)|\le k!R/\delta^k,\qquad k=0,1,2.
\]

Ces majorants s’ajoutent, dans les deux composantes, aux expressions finies
des jets. Une petite différence entre deux précisions n’est pas utilisée
à la place du reste. Les Bernoulli sont calculés par une récurrence rationnelle.
Les logarithmes portent sur des entiers positifs ; les exponentielles
complexes utilisent seulement exp, cos et sin réels avec intervalles.

Sources primaires des identités : [DLMF 25.11(iii)](https://dlmf.nist.gov/25.11.iii)
et [DLMF 24.8(i)](https://dlmf.nist.gov/24.8.i). Les majorations ci-dessus
sont explicitées ici séparément.

## 3. Lemme I2 — Une projection réelle fixe préserve le pli

L’équation fonctionnelle commune donne sur la droite critique
$F(r,1/2+it)=e^{-i\theta(t)}Z(r,t)$, avec Z réel analytique.
Pour un complexe constant $\omega$, poser
$H(r,t)=\Re[\omega F(r,1/2+it)]=h(t)Z(r,t)$,
$h(t)=\Re[\omega e^{-i\theta(t)}]$.

Si $\Re[\omega f_i(1/2+it)]$ est séparé de zéro sur la boîte de hauteur,
h ne s’annule pas : ce terme est $h(t)Z_i(t)$. Alors

\[
H=H_t=0\iff Z=Z_t=0,
\quad H_r=hZ_r,\quad H_{tt}=hZ_{tt}
\quad\text{au zéro double}.
\]

**Preuve.** Diviser H par h ; au zéro de Z, dériver une première fois,
puis au zéro de $Z_t$ une seconde fois. La dérivée radiale ne dérive pas h.
La projection d’ancre non nulle sépare simultanément h et $Z_i$ de zéro. □

Ainsi $\kappa=-2H_r/H_{tt}=-2Z_r/Z_{tt}$. Les jets du système réel
$G=(H,H_t)$ sont évalués directement depuis $F,F_s,F_{ss}$ ; aucun jet
Gamma n’est évalué par intervalles. Une non-annulation de $H_{tt}$ prouve
aussi que le zéro de F en s est exactement double. Les phases exactes et
le facteur Gamma commun justifient l’équation fonctionnelle employée.

## 4. Théorème I3 — Inclusion et contraction donnent existence et unicité

Soit une boîte réelle B de centre rationnel $x_0$, et C une matrice
rationnelle inversible. Soient des intervalles contenant $G(x_0)$ et chaque
entrée de $DG(B)$. Définir

\[
K=x_0-CG(x_0)+(I-CDG(B))(B-x_0).
\]

Si $K\subset\operatorname{int}B$ et
$q=\sup\|I-CDG(B)\|_\infty<1$, G possède exactement un zéro dans B.

**Preuve.** Pour $T(x)=x-CG(x)$, la formule intégrale de la valeur moyenne
donne $T(B)\subset K\subset B$. La même borne matricielle donne
$\|T(x)-T(y)\|_\infty\le q\|x-y\|_\infty$ sur B. La boîte est complète ;
le théorème du point fixe fournit une unique solution de $T(x)=x$.
C étant inversible, elle équivaut à $G(x)=0$. Toute solution appartient à K. □

La borne q est la somme maximale des modules des entrées d’une ligne.
Les inclusions sont strictes, comparées comme fractions exactes aux bornes
rationnelles. Le préconditionneur provient de l’inverse rationnel d’un
jacobien arrondi selon la règle fixée ; il n’a pas besoin d’être un inverse
exact du vrai jacobien.

La même démonstration s’applique uniformément pour un paramètre r dans un
intervalle : pour chaque r, $T_r$ conserve la boîte et possède la même borne
de contraction. Pour un zéro complexe de F, le jacobien réel est
$\begin{pmatrix}\Re F_s&-\Im F_s\\\Im F_s&\Re F_s\end{pmatrix}$.

## 5. Lemme I4 — Rouché contrôle le contour continu et tout le paramètre

Prendre $w=-i(s-1/2)$, $w_0=t_0$ et le cercle $|w-w_0|=R=1/5$.
Choisir un complexe rationnel non nul α et $P(w)=\alpha(w-w_0)^2$.
Écrire $D=F-P$. Sur un arc de milieu $w_m$ et de distance maximale d,

\[
|D(w)|\le |D(w_m)|+|D_w(w_m)|d+\tfrac12 B_2d^2,
\quad B_2\ge\sup|D_{ww}|.
\]

**Preuve.** La formule de Taylor avec reste intégral sur le segment de
$w_m$ à w donne l’inégalité. Le segment reste dans le disque, couvert par
le rectangle déclaré. Pour n arcs égaux,
$d=2R\sin(\pi/(2n))$. Les jets sont majorés pour tout r de l’intervalle.
Si chaque majorant est strictement inférieur à $|\alpha|R^2$, Rouché
donne exactement deux zéros, avec multiplicité, pour chaque r. □

Le cercle entier est couvert, pas seulement ses points de grille. La
borne de dérivée seconde complète le calcul aux milieux des arcs. L’absence
de pôle dans le disque est justifiée par l’analyticité des fonctions L
et, même sans leur cancellation globale, par l’absence de s=1 dans ce disque.

## 6. Lemme I5 — Symétrie et unicité décident critique ou hors droite

Pour r réel, l’équation fonctionnelle associe à un zéro s son partenaire
$1-\overline s$, avec facteurs de complétion non nuls dans les boîtes.
Si une boîte centrée en $\Re s=1/2$ est invariante par cette symétrie et
contient un zéro unique, ce zéro est critique : son partenaire est le même.
Si une boîte exclut la droite critique, son zéro validé est hors droite.

**Preuve.** Le partenaire appartient à la même boîte invariante et est un
zéro ; l’unicité impose $s=1-\overline s$. Le second cas est immédiat. □

Deux boîtes disjointes incluses dans le cercle, avec les deux zéros uniques,
identifient toute la paire locale lorsque le compte de Rouché vaut deux.
On peut donc certifier le changement de configuration aux deux paramètres
$r_*\pm10^{-4}$, même si $r_*$ est fourni par un encadrement.

## 7. Portée de la certification et vérifications

Le certificat calculatoire repose sur les majorants analytiques démontrés,
les recettes exactes, et le backend mpmath 1.3.0 d’arithmétique élémentaire
par intervalles. La documentation qualifie son support d’expérimental :
aucune validation indépendante de tout le backend n’est présupposée.
Le constructeur de copie iv.mpc et l’involution complexe non supportés
sont évités ; les correctifs d’implémentation restent datés dans les données.
Les formules de jets sont recoupées avec Hurwitz en haute précision, avec
le même backend : ce contrôle est distinct du majorant analytique.

Un vérificateur rationnel relit séparément les intervalles du certificat,
recalcule inclusion, contraction et critères géométriques. Il vérifie le
calcul fini des inégalités ; il ne remplace pas une réévaluation indépendante
des primitives transcendantales. Les sorties et les refus des plans fixés
sont conservés.

Ce certificat concerne une famille V13, un pli, un contour et quatre boîtes.
Il ne certifie pas le premier zéro global, toutes les collisions ou la
positivité arithmétique de ζ. La métrique du compagnon dépend du discriminant
de la paire ; elle ne donne toujours pas le signe global de la forme de Weil.

## 8. Théorème I6 — Obstacle à toute métrique positive du compagnon au pli

Fixer l’unité de hauteur pour rendre les coordonnées adimensionnées. Pour
$H=\begin{pmatrix}a&1\\\mu&a\end{pmatrix}$ réel, une matrice symétrique
$G=\begin{pmatrix}p&q\\q&r\end{pmatrix}$ vérifie $H^TG=GH$ si et seulement
si $p=\mu r$. Un tel G défini positif existe si et seulement si $\mu>0$.

**Preuve.** La multiplication impose $p=\mu r$. La positivité exige $r>0$
et $pr-q^2=\mu r^2-q^2>0$, donc $\mu>0$. Réciproquement,
$G=\operatorname{diag}(\mu,1)$ convient. □

Pour une métrique hermitienne complexe, l’équation impose également
$q=\overline q$ ; le même calcul couvre donc ce cas.

Pour $0<\mu\le1$, le rapport des valeurs propres de G est au moins
$r/p=1/\mu$, par les quotients de Rayleigh sur les vecteurs de base.
Si $cI\le G\le CI$, on a $\mu=p/r\ge c/C$.
Une métrique uniformément positive et bornée ne peut donc accompagner ce
compagnon jusqu’à μ=0. Au double, le bloc de Jordan interdit toute métrique
définie positive ; après le pli, les valeurs propres complexes l’interdisent
aussi. Cela ferme la voie d’une positivité non dégénérée automatique de ce
compagnon à travers la collision. Cela ne ferme pas un programme distinct
pour ζ.
