---
title: "Amplification arithmétique - V6.55"
subtitle: "Restitution exacte, petits conducteurs contrôlés et dette restante"
author: "Dossier de Vincent P. P. NOËL - rédaction assistée"
date: "14 octobre 2026"
lang: fr
fontsize: 11pt
papersize: a4
geometry: margin=23mm
colorlinks: true
linkcolor: NavyBlue
urlcolor: NavyBlue
header-includes:
  - \usepackage[dvipsnames]{xcolor}
  - \usepackage{amsmath,amssymb}
  - \usepackage{microtype}
  - \setlength{\emergencystretch}{3em}
  - \setlength{\parskip}{5pt}
---

# Ce que l'essai a effectivement produit

**Type de document :** note de recherche avec preuves auxiliaires, confrontation
constructive et critique, programmes et diagnostics reproductibles. Version V6.55, qui prolonge
le dossier V6.54 ; cette tentative n'établit aucune nouvelle borne sur l'énergie
totale et ne démontre pas RH. Aucune priorité historique n'est revendiquée.

L'amplification est essayée ici sur les entiers avec le poids exact du dossier.
On construit une famille de traductions arithmétiques, puis on demande si son
énergie moyenne contrôle la somme initiale. Trois éléments sont démontrés :

1. Les paramètres carrés permettent une **restitution exacte**, par différence
   entre deux échelles, sans erreur de copie.
2. La dette des corrélations se regroupe selon un indice unique $q$, le
   conducteur d'un caractère quadratique.
3. Toute la partie $q\le H$ est majorée à l'échelle $HX^2$, à des logarithmes
   près, pour toutes les échelles. Le reste porte sur $q>H$.

| Opération | Résultat | Portée |
|:--|:--|:--|
| Retrouver la cible dans la famille | Identité exacte et restitution stable | Démontré |
| Contrôler la diagonale et les petits conducteurs | Bornes explicites, sans RH | Démontré |
| Contrôler la dette à grand conducteur | Borne supérieure signée uniforme | Ouvert |
| En déduire un demi-plan sans zéros | $\Re s>3/4$ si la borne restante est prouvée | Implication conditionnelle |
| Atteindre la ligne $1/2$ | Contrôle plus fort de l'énergie initiale | Ouvert |

**Verdict.** Le mécanisme de copie fonctionne. Le grand crible ordinaire ne
fournit pas l'annulation nécessaire. Une partie croissante de la dette est
maintenant contrôlée analytiquement ; cela ne constitue pas un gain d'exposant
sur la somme complète. Le verrou restant est localisé, pas franchi.

Le résultat conditionnel recherché dans cet essai est volontairement plus
faible que RH. Prouver sa dernière estimation constituerait un changement
quantitatif global dans cette construction. Ajouter des copies ou augmenter
un plafond de calcul ne le remplace pas.

\newpage

# 1. La source exacte et ses bornes élémentaires

Écrivons $\Lambda(p^k)=\log p$, et $\Lambda(n)=0$ sinon. Posons
\[
\psi(x)=\sum_{n\le x}\Lambda(n),\qquad
E(x)=\psi(x)-x,\qquad c=1+\gamma_E.
\]
Pour $x\ge1$, avec $N=\lfloor x\rfloor$, définissons
\[
A(x)=E(x)+c,\qquad
B(x)=\log(N!)-x h_N+cN,\qquad
h_N=\sum_{j=1}^N\frac1j.
\]
Nous prolongeons $A$ et $B$ par zéro sur $x<1$. Cette convention s'appliquera
à toutes les fonctions et dilatations ci-dessous.

**Identité de diviseurs et inversion.** Pour tout $x\ge1$,
\[
\sum_{k\le x}A(x/k)=B(x),\qquad
A(x)=\sum_{k\le x}\mu(k)B(x/k).
\]
En effet, $\sum_{d\mid n}\Lambda(d)=\log n$ entraîne
$\sum_{k\le x}\psi(x/k)=\log(N!)$. Les deux autres termes donnent
$-xh_N+cN$. Pour inverser, regrouper les sommes finies par $j=k\ell$ et
utiliser $\sum_{k\mid j}\mu(k)=\mathbf1_{j=1}$. Aucune limite n'intervient.

**Borne explicite de la source.** Si $x=N+\theta$, $0\le\theta<1$,
les restes de Stirling et du développement harmonique donnent
\[
\begin{aligned}
B(x)={}&(\tfrac12-\theta)\log N
 +\tfrac12\log(2\pi)-\tfrac12-\gamma_E\theta\\
 &-\frac{\theta}{2N}+r_N+(N+\theta)e_N,\\
&0<r_N<\frac1{12N},\qquad 0<e_N<\frac1{12N^2}.
\end{aligned}
\]
Le reste après $(1/2-\theta)\log N$ est compris entre $-3/2$ et $3/4$.
Il en résulte la borne commode
\[
|B(x)|\le\tfrac12\log x+2\qquad(x\ge1).
\]

**Deux coûts utiles.** La comparaison avec les fonctions décroissantes de $t$
$\tfrac12\log(x/t)+2$ et son carré, sur $0<t\le x$, donne
\[
\sum_{n\le x}|B(x/n)|\le\frac52 x,
\qquad
\sum_{n\le x}|B(x/n)|^2\le\frac{13}{2}x.
\]
Par exemple, la seconde somme est au plus
$\int_0^x(\frac12\log(x/t)+2)^2dt=13x/2$.
La diagonale de l'énergie $J_A(X)=\int_1^XA(x)^2dx$ vérifie donc
\[
D(X)\le\frac{13}{4}(X^2-1).
\]
Cela améliore la constante auxiliaire $13/2$ précédemment annoncée ; cela
n'améliore pas la borne de l'énergie totale. Les bornitudes quadratiques de
$J_A$ et de $J=\int_1^XE(x)^2dx$ sont équivalentes par $(a+b)^2\le2a^2+2b^2$.

\newpage

# 2. Construire les copies et les restituer

Le symbole de Jacobi $(u/n)$ prend les valeurs $-1,0,1$ pour un dénominateur
impair positif ; $(u/1)=1$. Pour $n$ sans carré, c'est un caractère
quadratique, nul si $u$ et $n$ ont un facteur premier commun.

Définissons la composante impaire et la famille
\[
A_o(x)=\sum_{\substack{n\le x\\n\text{ impair}}}\mu(n)B(x/n),\qquad
F_u(x)=\sum_{\substack{n\le x\\n\text{ impair}}}
\mu(n)\left(\frac un\right)B(x/n).
\]
Les termes non sans carré sont automatiquement nuls. En séparant les indices
pairs dans l'inversion de Möbius,
\[
\boxed{A(x)=A_o(x)-A_o(x/2).}
\]

**Lemme de restitution.** Pour tout premier impair $p$,
\[
\boxed{A_o(x)=F_{p^2}(x)-F_{p^2}(x/p).}
\]
En effet, $(p^2/n)=\mathbf1_{(n,p)=1}$ pour les indices retenus. La somme
$F_{p^2}$ est donc $A_o$ privée des multiples de $p$. Ces multiples sont
$n=pm$, avec $(m,p)=1$ ; leur contribution est $-F_{p^2}(x/p)$, par
$\mu(pm)=-\mu(m)$. C'est une identité finie, pas une approximation.

**Opérateur réutilisable.** Posons $L_pf(x)=f(x/p)$. Pour
\[
\mathcal N_T(f)=\sup_{1\le Y\le T}
\frac1Y\left(\int_1^Y|f(x)|^2dx\right)^{1/2},
\]
le changement de variable donne $\mathcal N_T(L_pf)\le p^{-1/2}\mathcal N_T(f)$.
La restitution s'écrit $A_o=(I-L_p)F_{p^2}$ et son inverse
\[
F_{p^2}=(I-L_p)^{-1}A_o=\sum_{j\ge0}L_p^jA_o.
\]
La somme est finie en chaque point ; sur la norme énergétique, la série des
coûts est majorée par $\sum_jp^{-j/2}$. Ainsi
\[
\frac{\mathcal N_T(A_o)}{1+p^{-1/2}}
\le\mathcal N_T(F_{p^2})
\le\frac{\mathcal N_T(A_o)}{1-p^{-1/2}}.
\]
La stabilité est uniforme en $T$. Elle ne prouve pas que ces normes restent
bornées lorsque $T$ croît : elle compare les copies à leur source.

Plus généralement, si $u=rs^2$ avec $r$ sans carré, posons
$A_r=F_r$. Les dilatations commutent et la même preuve donne
\[
F_{rs^2}=\prod_{\substack{p\mid s\\p\text{ premier impair}}}
\left(I-\left(\frac rp\right)L_p\right)^{-1}A_r.
\]
Cette grammaire d'opérateurs décrit exactement toutes les lignes, y compris
les copies issues de $r=1$. Les facteurs 2 de $s$ ne changent rien, les
dénominateurs étant impairs. Cette écriture ne rend pas les copies indépendantes.

\newpage

# 3. Regrouper la dette selon son conducteur

Pour un entier $H\ge1$, introduisons l'énergie moyenne
\[
Q_H(X)=\sum_{u=1}^H\int_1^X|F_u(x)|^2dx=D_H(X)+R_H(X).
\]
La diagonale est positive et satisfait
\[
D_H(X)=\sum_{\substack{n\le X\\n\text{ impair}}}\mu(n)^2
\#\{u\le H:(u,n)=1\}\int_n^XB(x/n)^2dx
\le\frac{13}{4}H(X^2-1).
\]

Pour deux indices sans carré, écrire $n=ga$, $m=gb$. Alors $a,b,g$ sont
impairs, sans carré et deux à deux premiers entre eux. Avec $q=ab$,
\[
\mu(n)\mu(m)=\mu(q),\qquad
\left(\frac un\right)\left(\frac um\right)
=\mathbf1_{(u,g)=1}\left(\frac uq\right).
\]
Le facteur commun disparaît du signe de Möbius et devient une condition de
coprimalité. Le signe restant appartient au seul indice $q$.

Posons
\[
\begin{aligned}
K_X(g;a,b)&=\int_{g\max(a,b)}^X
B\!\left(\frac{x}{ga}\right)B\!\left(\frac{x}{gb}\right)dx,\\
S(H;q,g)&=\sum_{\substack{u\le H\\(u,g)=1}}\left(\frac uq\right).
\end{aligned}
\]
Le noyau vaut zéro si sa borne inférieure dépasse $X$. Le regroupement exact
de toute la dette est
\[
\boxed{
R_H(X)=\sum_{\substack{q>1\\q\text{ impair, sans carré}}}\mu(q)
\sum_{a\mid q}
\sum_{\substack{g\le X/\max(a,q/a)\\
g\text{ impair, sans carré}\\(g,q)=1}}
K_X(g;a,q/a)S(H;q,g).}
\]
Tous les couples ordonnés sont comptés : la somme sur $a\mid q$ inclut
les deux orientations. Le cas $q=1$ redonne exactement $D_H$, sans facteur 2
supplémentaire. Les conducteurs $q>1$ sont au plus $X^2$.

Cette écriture conserve les coupures, les poids et les signes. Ce n'est pas
une assertion de positivité terme par terme : $K_X$, $S$ et $\mu(q)$ peuvent
avoir des signes différents.

\newpage

# 4. Un domaine croissant contrôlé sans RH

**Lemme des petits conducteurs.** Pour $X\ge1$, $Q\ge2$ et tout entier
$H\ge1$, la partie $1<q\le Q$ de la somme précédente vérifie
\[
\boxed{\begin{aligned}
|R_{1<q\le Q}(X,H)|\le{}&X^2Q(1+\log X)(1+\log Q)^2\\
&\times\left(\frac{13}{2}+\frac54\log Q\right).
\end{aligned}}
\]

**Preuve, étape 1 : Fourier et coprimalité.** Pour $q>1$ impair sans carré,
$\chi_q(v)=(v/q)$ est primitif et non principal. Sa somme de Gauss a module
$\sqrt q$. La transformation de Fourier finie, la somme géométrique et
$\sin(\pi j/q)\ge2j/q$ pour $1\le j\le(q-1)/2$ donnent
\[
\left|\sum_{v\le Y}\chi_q(v)\right|
\le\sqrt q\,h_{(q-1)/2}\le\sqrt q(1+\log q).
\]
La borne est uniforme en $Y$ : les périodes complètes ont une somme nulle.
L'inclusion-exclusion donne exactement
\[
S(H;q,g)=\sum_{d\mid g}\mu(d)\left(\frac dq\right)
\sum_{v\le H/d}\left(\frac vq\right),
\quad |S(H;q,g)|\le\tau(g)\sqrt q(1+\log q),
\]
où $\tau(g)$ est le nombre des diviseurs de $g$.

**Étape 2 : payer tous les multiplicateurs communs.** Si $a\le b$, le
changement $x=gu$ puis la comparaison
$\sum_{g\le Y}g\tau(g)\le Y^2(1+\log Y)$ entraînent
\[
\sum_{g\le X/b}\tau(g)|K_X(g;a,b)|
\le X^2(1+\log X)\int_b^\infty
\frac{|B(u/a)B(u/b)|}{u^2}du.
\]
La borne de $B$, avec $u=bv$, donne
\[
\int_b^\infty\frac{|B(u/a)B(u/b)|}{u^2}du
\le\frac1b\left(\frac{13}{2}+\frac54\log\frac ba\right).
\]

**Étape 3 : sommer les conducteurs.** Puisque $ab=q$,
$\sqrt q/\max(a,b)\le1$ et $\log(b/a)\le\log q$. Utiliser enfin
$\sum_{q\le Q}\tau(q)\le Q(1+\log Q)$. Supprimer les restrictions de
coprimalité, de parité et de carré dans ces majorations positives ne fait
qu'augmenter le membre de droite. Cela prouve le lemme.

**Conséquence.** Choisir $Q=H$ contrôle la tête à $HX^2$, avec des logarithmes.
À $H=X\ge2$, elle est $O(X^3(1+\log X)^4)$. Le reste est situé dans
\[
\boxed{X<q\le X^2,\qquad g<\sqrt X.}
\]
La borne de la tête est absolue. Elle ne constitue pas une loi de signe globale.

\newpage

# 5. Pourquoi le grand crible usuel ne termine pas

Le grand crible quadratique primitif contrôle les lignes impaires sans carré.
Sur un bloc $n\asymp D$, il donne un coût
$(H+D)\sum_n|a_n|^2$, à un facteur $(HD)^\varepsilon$ près [1,2].
Les paramètres carrés nécessaires aux copies n'appartiennent pas à cette famille.

Pour réintroduire toutes les lignes $u=rs^2$, on applique ce résultat aux
coefficients $a_n\mathbf1_{(n,s)=1}$ puis on somme $s\le\sqrt H$. Les lignes
paires se traitent en tordant les coefficients par $(2/n)$. On obtient
\[
\sum_{u\le H}\left|\sum_{n\asymp D}a_n\left(\frac un\right)\right|^2
\ll_\varepsilon(HD)^\varepsilon
\left(H+D\sqrt H\right)\sum_n|a_n|^2.
\]
Le terme supplémentaire vient de la somme des coûts $D$, pour chaque $s$.
Avec le poids exact et les bornes du §1, l'intégration laisse un terme
$X^3\sqrt H$, à des facteurs $X^\varepsilon H^\varepsilon$ près. Après division
par le nombre des copies, ce terme rend une borne de taille $X^3$ : aucun
gain fixe d'exposant n'en résulte.

**Le terme ne peut pas disparaître pour des coefficients arbitraires.** Prenons
$H=D$ et des coefficients $-1$ sur les premiers $D/2<n\le D$, zéro ailleurs.
Ces coefficients sont précisément $\mu(n)$ sur ce support. Si $D>4$, chaque
carré $u=s^2$, $s\le\sqrt D$, est premier à tous ces indices ; sa ligne vaut
donc moins le nombre $L_D$ de premiers du support. Ces seules lignes imposent
\[
\sum_{u\le D}\left|\sum_n a_n\left(\frac un\right)\right|^2
\ge\lfloor\sqrt D\rfloor L_D^2,
\qquad L_D\asymp\frac D{\log D}.
\]
Cela exclut une borne universelle $\ll_\varepsilon D^{2+2\varepsilon}$ pour
$\varepsilon<1/4$. Le masque limité aux premiers diffère du poids exact $B$ :
**ce contre-modèle ne réfute pas l'estimation spéciale recherchée**. Il prouve
qu'elle doit utiliser les relations entre premiers et composés, au-delà du
seul fait que les coefficients portent un signe de Möbius.

**Confrontation des deux analyses.** La construction fournit des copies exactes
et un classement par conducteur. La critique montre que traiter ces copies
par un théorème pour lignes primitives oublie leur coût. Les deux analyses
valident le contrôle des petits conducteurs ; aucune ne majore encore le reste.

\newpage

# 6. L'estimation restante et ce qu'elle donnerait

Pour un entier $X$ grand, poser $H=X$ et
\[
\mathcal P=\{p\text{ premier impair}:\sqrt X/2<p\le\sqrt X\},
\qquad M=|\mathcal P|\asymp\sqrt X/\log X.
\]
Le comptage asymptotique des premiers est inconditionnel. Les petites valeurs
où $\mathcal P$ est vide se traitent séparément sur un intervalle compact.

Avec $J_o(X)=\int_1^X|A_o(x)|^2dx$, la restitution exacte et le coût
$|F_{p^2}(t)|\le5t/2$ donnent
\[
\begin{aligned}
M J_o(X)
&\le 2Q_H(X)+\frac{25}{6}X^3\sum_{p\in\mathcal P}\frac1{p^2},\\
J_o(X)&\le\frac{2Q_H(X)}M+\frac{50}{3}X^2.
\end{aligned}
\]
La seconde contribution paie la plus petite échelle $x/p$. Elle est déjà
sous contrôle ; aucune borne de niveau RH n'a été utilisée pour la payer.

**Proposition conditionnelle.** Si l'on démontrait, avec $C,k$ fixes et
indépendants de $X$, la majoration signée
\[
\boxed{R_{q>X}(X;H=X)\le C X^3(1+\log X)^k,}
\]
alors le lemme des petits conducteurs et la diagonale donneraient
\[
Q_X(X)\ll X^3(1+\log X)^{\max(k,4)},\quad
J_o(X)\ll X^{5/2}(1+\log X)^{\max(k,4)+1}.
\]
Puis $A=A_o-A_o(\cdot/2)$ entraîne
$J_A(X)\le2J_o(X)+4J_o(X/2)$. La même borne vaut pour $J$. Le passage des
entiers aux réels utilise la croissance de l'intégrale positive et
$X\le\lceil X\rceil$. La couverture est donc globale, si l'hypothèse est prouvée.

Pour $\sigma>3/4$, Cauchy-Schwarz sur $[U,2U]$ donne alors
\[
\int_U^{2U}|E(x)|x^{-\sigma-1}dx
\ll U^{3/4-\sigma}(1+\log U)^{(\max(k,4)+1)/2}.
\]
La somme dyadique converge. La transformée de Mellin est holomorphe pour
$\Re s>3/4$, et l'identité
\[
-\frac{\zeta'}{\zeta}(s)=\frac{s}{s-1}
+s\int_1^\infty E(x)x^{-s-1}dx
\]
y exclut les pôles provenant de zéros. **La conclusion conditionnelle est
l'absence de zéros pour $\Re s>3/4$, pas RH.**

Le critère classique $J(X)=O(X^2)$ vise encore la ligne $1/2$ et, par Weil,
la positivité sur tous les tests admissibles [3,5]. Le demi-plan $\Re s>3/4$
ne suffirait pas à cette positivité globale. Aucun gain de cet ordre,
ni même le gain conditionnel précédent, n'est démontré dans cet essai.

\newpage

# 7. Calculs exécutés, limites et prochaine attaque

Le programme `calcul_famille.py` utilise les coefficients entiers exacts de
Möbius et Jacobi. Chaque $F_u$ est affine sur $[j,j+1)$ ; son énergie est
intégrée par une primitive polynomiale, sans quadrature. Les coefficients
réels sont calculés en double précision.

| $X=H$ | $Q_H/(HX^2)$ | $D_H/(HX^2)$ | $R_H/(HX^2)$ |
|--:|--:|--:|--:|
| 100 | 0,05975949 | 0,05982849 | -0,00006900 |
| 300 | 0,05801004 | 0,05861269 | -0,00060265 |
| 1000 | 0,05640214 | 0,05766501 | -0,00126287 |

Ces nombres vérifient un calcul fini ; leurs signes n'établissent aucune loi
infinie. Le programme indépendant `verifier_identites.py` recalcule la source
en arithmétique décimale à 70 chiffres et vérifie :

- inversion de diviseurs, séparation paire et restitution des copies sur
  sept valeurs réelles et quatre premiers ; résidu maximal $3,04\,10^{-66}$ ;
- regroupement ponctuel par conducteur : résidu $2\,10^{-68}$ ;
- intégration indépendante à $X=31$ et $100$, à partir des valeurs et dérivées
  directes plutôt que des sauts ; différence avec le moteur flottant à
  $X=100$ inférieure à $1,1\,10^{-10}$ pour $Q_H$ et $D_H$ ;
- contre-modèle aux coefficients arbitraires : lignes carrées comptées
  exactement pour cinq tailles, jusqu'à un million.

Les diagnostics décimaux ne sont pas des certificats par intervalles.
À $X=31$, le regroupement intégré donne respectivement environ $-36,2662$
et $-8,5194$ pour les dettes $q\le X$ et $q>X$. Cela ne justifie aucune
extrapolation sur la seconde.

**Prochaine attaque retenue.** Pour $q>X$, conserver $\mu(q)$ dans la somme
et appliquer la transformation de Fourier avant de prendre les valeurs
absolues. La transformation quadratique usuelle laisse le facteur $\mu(q)$
intact. Il faut une identité supplémentaire qui le convertisse en une
structure estimable, ou une estimation bilinéaire spéciale de cette dette.
La grandeur de sortie exigée est maintenant écrite au §6 ; aucune de ces
deux voies n'est présumée réussir.

**Garde concernant le préprint sextique [4].** Son estimation moyenne comporte
une norme de dérivées du poids lisse. Or $B(m)-B(m^-)=\log m+\gamma_E$ :
substituer directement $B(X/n)$ n'offre pas une constante uniforme. De plus,
dans $K=\mathbb Q(\sqrt{-3})$, pour $(n,3)=1$,
$N((n))=n^2$ et $\mu_K((n))=\mu(n)^2\chi_{-3}(n)$, pas $\mu(n)$.
Un transfert spectral par $\zeta_K=\zeta L(\chi_{-3})$ serait possible si
le théorème profond était validé ; sa preuve complète n'est pas auditée ici.
Il n'est utilisé dans aucun lemme de cette note.

\newpage

# Références, reproduction et statut

**[1] D. R. Heath-Brown**, *A mean value estimate for real character sums*,
Acta Arithmetica 72 (1995), 235-275.
Notice primaire :
<https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/72/3/108575/a-mean-value-estimate-for-real-character-sums>.

**[2] L. Goldmakher et B. Louvel**, *A quadratic large sieve inequality over
number fields*, arXiv:1112.1642v2 (2012), introduction, équation (1.1).
<https://arxiv.org/pdf/1112.1642>.
Le théorème est appliqué uniquement à sa famille primitive ; le coût de
réintroduction des carrés est démontré séparément au §5.

**[3] R. P. Brent, D. J. Platt et T. S. Trudgian**, *The mean square of the
error term in the prime number theorem*, Journal of Number Theory 238 (2022),
740-762. <https://maths-people.anu.edu.au/~brent/pd/rpb274-final.pdf>.
Le critère énergétique classique demeure une cible, pas une borne disponible
indépendamment de RH. Aucun comportement de plateau de l'énergie normalisée
n'est exigé.

**[4] OpenAI**, préprint *The Quasi-Riemann Hypothesis*, 5 octobre 2026,
source `build/paper2.tex`, proposition moyenne et extraction par puissances.
<https://github.com/openai/math/tree/main/preprints/The-Quasi-Riemann-Hypothesis-October-5-2026>.
Source exploratoire, sans recours à ses énoncés profonds. Le dépôt distingue
plusieurs états de vérification : <https://github.com/openai/math>.

**[5] M. Suzuki**, *Aspects of the screw function corresponding to the Riemann
zeta function*, arXiv:2206.03682v4 (2023), théorème 1.3 et §3 sur la positivité
de Weil. <https://arxiv.org/pdf/2206.03682>.

**Provenance locale du raisonnement.** Le dossier V6.54 contient l'identité
des poids premiers, le développement de l'énergie ancrée et le critère
classique. La présente passe démontre les identités de restitution et le
lemme des petits conducteurs dans son propre cadre. La construction a été
confrontée à une analyse critique indépendante ; les deux ont validé ces
preuves auxiliaires. Cette confrontation n'est pas une validation externe
de l'ensemble du programme.

Pour reproduire les diagnostics depuis le dossier :

```bash
python3 verifier_identites.py --output results --precision 70
python3 calcul_famille.py --ceilings 100 300 1000
```

Le premier programme utilise seulement la bibliothèque standard Python ; le
second requiert NumPy. Les JSON conservent les résultats et leurs limites.
Le plafond de calcul de la famille est volontairement borné : les preuves
des §§1-6 ne reposent pas sur ce plafond.

**Synthèse de statut.** Démontré : source exacte, restitution, stabilité,
regroupement, diagonale et tête de conducteurs. Conditionnel : le transfert
d'une borne de la queue vers le demi-plan $\Re s>3/4$. Ouvert : cette borne
de la queue, la croissance quadratique totale et la positivité globale de
Weil. L'amplification ordinaire ne suffit pas ; l'amplification exploitant
la signature arithmétique de la queue reste à construire.
