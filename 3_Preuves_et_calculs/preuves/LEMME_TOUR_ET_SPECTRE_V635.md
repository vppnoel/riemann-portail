# V6.35 - Lemme des jets sur les extensions finies et conséquence spectrale

**Statut.** Démonstration dans les corps finis de caractéristique impaire. Le lemme de rang est établi pour toute cubique, y compris singulière. La conséquence spectrale concerne exclusivement la courbe projective **lisse** de genre un associée à une cubique sans racines multiples. La méthode de comptage est classique, de Stepanov ; aucun résultat nouveau n'est revendiqué. Aucun transfert à la fonction zêta de Riemann n'est établi.

**Progression par rapport à V6.34.** On remplace le passage par les dérivées ordinaires et les facteurs \(k!\) par un calcul direct avec les dérivées de Hasse. La borne s'applique ainsi à \(q=p^n\), avec \(M<q\), même lorsque \(M\ge p\). Son uniformité dans \(n\) permet ensuite de déterminer les modules des deux racines inverses de la fonction zêta d'une courbe elliptique, après une justification séparée de sa rationalité.

## 1. Cadre et définition des jets

Soit \(q=p^n\ge5\), où \(p\) est un nombre premier impair et \(n\ge1\). Soit \(f\in\mathbb F_q[x]\) un polynôme de degré exactement trois. Posons

\[
e=\frac{q-1}{2},\qquad g=f^e,\qquad
S=\{u\in\mathbb F_q:f(u)\ne0,\ g(u)=1\}.
\]

Les éléments de \(S\) sont les abscisses où \(f(u)\) est un carré non nul.

Pour \(A\in\mathbb F_q[x]\), sa dérivée de Hasse d'ordre \(k\) est définie par

\[
A(x+h)=\sum_{k\ge0} D^{[k]}A(x)\,h^k.
\]

En particulier,

\[
D^{[k]}x^a=\binom ak x^{a-k}
\]

si \(0\le k\le a\), et cette dérivée est nulle si \(k>a\). Les coefficients binomiaux sont réduits dans la caractéristique \(p\). La règle du produit est

\[
D^{[k]}(AB)=\sum_{\ell=0}^{k}
 D^{[k-\ell]}A\,D^{[\ell]}B.
\]

Il n'y a pas de facteur \(\binom k\ell\) dans cette règle. Aucun \(k!\) n'est inversé.

Le jet d'ordre \(M-1\) de \(A\) au point \(u\) est le vecteur

\[
\bigl(D^{[0]}A(u),\ldots,D^{[M-1]}A(u)\bigr).
\]

Ces \(M\) coordonnées sont nulles si et seulement si \((x-u)^M\) divise \(A\), puisque ce sont les \(M\) premiers coefficients du développement de \(A(u+h)\). Cette équivalence vaut en toute caractéristique.

## 2. Identité de Hasse pour la puissance de la cubique

Pour tout entier \(k\ge0\), définissons

\[
P_k(x)=\sum_{\ell=0}^{\min(e,k)}
 \binom e\ell f(x)^{k-\ell}
 [h^k]\bigl(f(x+h)-f(x)\bigr)^\ell.
\]

Ici \([h^k]\) désigne l'extraction du coefficient de \(h^k\). Chaque exposant \(k-\ell\) est non négatif : \(P_k\) est donc un polynôme, et non une expression rationnelle.

**Identité.** Pour tout \(k\ge0\),

\[
f^kD^{[k]}g=gP_k,\qquad \deg P_k\le2k.
\]

La convention est que le degré du polynôme nul est \(-\infty\).

**Preuve.** Le développement binomial exact donne

\[
f(x+h)^e=
 \sum_{\ell=0}^{e}\binom e\ell
 f(x)^{e-\ell}\bigl(f(x+h)-f(x)\bigr)^\ell.
\]

Puisque \(f(x+h)-f(x)\) est divisible par \(h\), seuls les termes \(\ell\le k\) contribuent au coefficient de \(h^k\). Multiplier ce coefficient par \(f(x)^k\) et factoriser \(f(x)^e=g(x)\) donne l'identité.

Pour la borne de degré, écrivons

\[
f(x+h)-f(x)=c_1(x)h+c_2(x)h^2+c_3h^3,
\qquad \deg c_i\le3-i.
\]

Un produit de \(\ell\) facteurs contribuant à \(h^k\) a degré en \(x\) au plus \(3\ell-k\). Après multiplication par \(f^{k-\ell}\), son degré est au plus

\[
3(k-\ell)+(3\ell-k)=2k.
\]

La somme conserve cette borne. La preuve ne suppose ni \(k<p\), ni \(f\) sans racines multiples.

## 3. Espace auxiliaire : dimension et Frobenius

Soient

\[
J\ge1,\qquad 1\le K\le\frac{q-3}{2},\qquad 1\le M<q.
\]

On travaille dans l'anneau de polynômes \(\mathbb F_q[x]\), **sans quotient par \(x^q-x\)**. Définissons

\[
W=\operatorname{span}_{\mathbb F_q}
 \{x^{jq+a},\ x^{jq+a}g:
       0\le j<J,\ 0\le a<K\}.
\]

**Dimension.** On a \(\dim W=2JK\).

En effet, les degrés dominants de la première famille sont \(jq+a\). Ceux de la seconde sont

\[
jq+a+\frac{3(q-1)}2
 =(j+1)q+\frac{q-3}{2}+a.
\]

Les résidus modulo \(q\) appartiennent respectivement aux deux intervalles disjoints

\[
[0,K-1],\qquad
\left[\frac{q-3}{2},\frac{q-3}{2}+K-1\right],
\]

tous deux contenus dans \([0,q-1]\). Les degrés dominants des \(2JK\) polynômes sont donc distincts. Une combinaison non triviale ne peut être le polynôme nul.

Le degré maximal dans \(W\) est

\[
D=(J-1)q+K-1+\frac{3(q-1)}2.
\]

**Annulation des jets des facteurs de Frobenius.** Dans la caractéristique \(p\),

\[
(x+h)^{jq}=(x^q+h^q)^j.
\]

Ainsi

\[
D^{[i]}x^{jq}=0\quad\text{pour }0<i<q.
\]

Aux points de \(\mathbb F_q\), on a aussi \(u^{jq}=u^j\). Cette combinaison d'une annulation des jets et d'une identité d'évaluation est le mécanisme spécifique aux corps finis utilisé ci-dessous.

## 4. Borne de rang

Soit

\[
\mathcal J_M:W\longrightarrow\mathbb F_q^{M|S|},
\qquad
A\longmapsto\bigl(D^{[k]}A(u)\bigr)_{\substack{u\in S\\0\le k<M}}.
\]

Alors

\[
\operatorname{rang}\mathcal J_M
 \le\sum_{k=0}^{M-1}
   \min\{|S|,K+J-1+2k\}
 \le R,
\]

où

\[
R=M(K+J-1)+M(M-1).
\]

**Preuve.** Fixons \(0\le k<M<q\). Multiplions chaque ligne d'évaluation au point \(u\) par \(f(u)^k\). Ces facteurs sont non nuls sur \(S\) ; le rang ne change pas.

Pour les polynômes de la première famille, l'annulation des dérivées de Hasse positives de \(x^{jq}\) et l'identité \(u^{jq}=u^j\) montrent que ces lignes sont les évaluations sur \(S\) des polynômes

\[
x^j f^kD^{[k]}x^a.
\]

Leur degré est au plus \(j+a+2k\).

Pour la seconde famille, la règle du produit, l'identité de la section 2 et \(g(u)=1\) donnent les évaluations des polynômes

\[
x^j\sum_{\ell=0}^{k}
 f^{k-\ell}D^{[k-\ell]}x^a\,P_\ell.
\]

Chaque terme non nul a degré au plus

\[
j+3(k-\ell)+a-(k-\ell)+2\ell
 =j+a+2k.
\]

Le bloc d'ordre \(k\) se factorise donc par l'évaluation sur \(S\) des polynômes de degré au plus \(K+J-2+2k\). Son rang est au plus \(\min(|S|,K+J-1+2k)\). Le rang de l'empilement est au plus la somme des rangs des blocs.

Cette somme est une majoration ; elle ne suppose pas l'indépendance des différents blocs de jets.

## 5. Existence et comptage par multiplicité

Si

\[
2JK>R,
\]

le noyau de \(\mathcal J_M\) a dimension au moins \(2JK-R>0\). Il contient donc un **polynôme non nul** \(A\), de degré au plus \(D\), divisible par \((x-u)^M\) pour chaque \(u\in S\).

Les facteurs correspondant aux points distincts sont premiers entre eux. Par conséquent,

\[
\prod_{u\in S}(x-u)^M\mid A,\qquad
M|S|\le\deg A\le D.
\]

On obtient la borne

\[
|S|\le U,\qquad
U=\left\lfloor
 \frac{(J-1)q+K-1+3(q-1)/2}{M}
\right\rfloor.
\]

Ni l'existence du noyau ni cette valeur de \(U\) n'utilisent un dénombrement préalable de \(S\). Un témoin calculé à partir de \(S\) est un certificat supplémentaire pour une instance particulière.

## 6. Famille explicite et torsion

Soit \(r\ge1\) tel que

\[
6r^2-2r+5\le q.
\]

Choisissons

\[
J=r+1,\qquad M=2r,\qquad K=3r^2-r+1.
\]

La restriction \(K\le(q-3)/2\) est respectée. On a également \(M<q\), car \(q\ge6r^2-2r+5>2r\). Un calcul direct donne

\[
2JK-R=2.
\]

Le polynôme auxiliaire existe donc. Sa borne devient

\[
U=
\left\lfloor
 \frac q2+\frac{3(q-1)}{4r}+\frac{3r-1}{2}
\right\rfloor.
\]

Soit \(z=\#\{u\in\mathbb F_q:f(u)=0\}\), où les racines distinctes sont comptées une seule fois ; \(0\le z\le3\). Le nombre de points du modèle projectif \(y^2=f(x)\), avec son unique point à l'infini, est

\[
N_q=2|S|+z+1.
\]

Cette identité de dénombrement reste vraie si la cubique est singulière ; la conséquence elliptique de la section 8 exige en revanche la lissité.

Choisissons un non-résidu quadratique \(\nu\in\mathbb F_q^\times\). La cubique \(\nu f\) échange les valeurs carrées et non carrées et garde les mêmes \(z\) racines. Ainsi

\[
|S_{\nu f}|=q-z-|S|.
\]

Le lemme donne la même borne \(U\) pour \(f\) et pour \(\nu f\). On en déduit

\[
2q-z-2U+1\le N_q\le2U+z+1,
\]

puis

\[
|N_q-(q+1)|\le2U-q+z.
\]

L'existence simultanée des deux bornes implique que le membre de droite est non négatif.

## 7. Constante uniforme explicite sur toute la tour

Pour toute puissance impaire \(q=p^n\), y compris \(q=3\), on a

\[
\boxed{\ |N_q-(q+1)|\le10\sqrt q\ }.
\]

La constante 10 est un choix simple, sans recherche d'optimalité.

**Petits corps.** Si \(3\le q<29\), le caractère quadratique \(\chi_q\), prolongé par \(\chi_q(0)=0\), donne

\[
N_q-(q+1)=\sum_{u\in\mathbb F_q}\chi_q(f(u)).
\]

Donc \(|N_q-(q+1)|\le q<10\sqrt q\). On n'utilise aucun espace \(W\) lorsque le domaine des paramètres est vide, notamment pour \(q=3\).

**Corps de taille au moins 29.** Prenons

\[
r=\left\lfloor\sqrt{\frac{q-5}{6}}\right\rfloor.
\]

Ce choix donne \(r\ge2\) et \(6r^2-2r+5\le q\). Posons \(v=\sqrt{(q-5)/6}\). Comme \(v\ge2\),

\[
r\ge v/2,\qquad r\le\sqrt{q/6}.
\]

La section 6 et \(z\le3\) donnent

\[
|N_q-(q+1)|
 \le\frac{3(q-1)}{2r}+3r+2.
\]

En utilisant \(q/(q-5)\le29/24\), on obtient

\[
\begin{aligned}
|N_q-(q+1)|
&\le\left(
 3\sqrt6\sqrt{\frac{29}{24}}
 +\sqrt{\frac32}+\frac2{\sqrt{29}}
 \right)\sqrt q\\
&=\left(
 \frac32\sqrt{29}
 +\sqrt{\frac32}+\frac2{\sqrt{29}}
 \right)\sqrt q\\
&<10\sqrt q.
\end{aligned}
\]

La dernière constante vaut moins de \(9{,}674\). La majoration 10 est donc uniforme en \(p\), \(n\) et \(f\).

**Constante asymptotique.** Avec ce même choix,

\[
r=\sqrt{q/6}+O(1),
\]

et la formule de \(U\) donne

\[
U=\frac q2+\sqrt6\sqrt q+O(1).
\]

Par conséquent,

\[
|N_q-(q+1)|\le2\sqrt6\sqrt q+O(1),
\]

où la constante du \(O(1)\) peut être choisie indépendante du corps et de la cubique. La constante asymptotique \(2\sqrt6\) reste plus faible que la constante 2 de Hasse. C'est l'uniformité sur toutes les extensions, et non l'amélioration de cette constante intermédiaire, qui est utilisée ensuite.

## 8. Données classiques indépendantes de la borne de Hasse

Fixons maintenant un nombre premier impair \(p\) et une cubique \(f\in\mathbb F_p[x]\) **sans racines multiples**. Son modèle projectif lisse \(E\), muni du point à l'infini \(O\), est une courbe elliptique. Posons

\[
N_n=\#E(\mathbb F_{p^n}),\qquad
t=p+1-N_1.
\]

Les données de rationalité et d'équation fonctionnelle sont établies séparément du comptage. Voici une justification par Riemann-Roch, sans borne de Hasse ni hypothèse sur des modules spectraux.

Pour un diviseur de degré \(d\ge1\) sur une courbe de genre un, Riemann-Roch donne \(\dim L(D)=d\). L'identification \(P\mapsto[(P)-(O)]\) entre \(E(\mathbb F_p)\) et les classes de degré zéro montre qu'il y a \(N_1\) classes de chaque degré : chaque classe de degré \(d\) est représentée par \((P)+(d-1)(O)\), avec \(P\in E(\mathbb F_p)\). Chaque classe contient \((p^d-1)/(p-1)\) diviseurs effectifs : ils correspondent aux éléments non nuls de \(L(D)\), modulo multiplication par \(\mathbb F_p^\times\). Ainsi leur nombre total est

\[
a_d=N_1\frac{p^d-1}{p-1},\qquad a_0=1.
\]

Le produit sur les points fermés, ou sa série de diviseurs effectifs, donne

\[
\begin{aligned}
Z(E,T)
 &=\sum_{d\ge0}a_dT^d
 =1+\frac{N_1}{p-1}
 \left(\frac{pT}{1-pT}-\frac{T}{1-T}\right)\\
 &=\frac{1-tT+pT^2}{(1-T)(1-pT)}.
\end{aligned}
\]

L'identité des classes est une bijection définie sur le corps de base ; elle ne suppose pas que tout point géométrique soit rationnel.

**Référence précise.** J. S. Milne, *Elliptic Curves*, deuxième édition, 2021, chapitre I, théorème 4.13 et formule (8), pp. 35-36 ; chapitre IV, proposition 9.9 et théorème 9.10, pp. 155-156. Texte sur le site de l'auteur : <https://www.jmilne.org/math/Books/EC2.pdf>. La preuve de rationalité citée utilise Riemann-Roch et les diviseurs. Elle n'utilise pas le théorème 9.4 de Hasse, même si celui-ci est présenté auparavant dans le livre.

Factorisons maintenant, dans \(\mathbb C[T]\),

\[
1-tT+pT^2=(1-\alpha T)(1-\beta T).
\]

À ce stade, on sait seulement

\[
\alpha+\beta=t,\qquad \alpha\beta=p.
\]

On ne suppose pas \(|\alpha|=|\beta|=\sqrt p\).

La forme réciproque du numérateur et du dénominateur donne l'équation fonctionnelle

\[
Z\left(E,\frac1{pT}\right)=Z(E,T).
\]

Elle exprime la symétrie \(\alpha\leftrightarrow p/\alpha\), mais ne fixe pas à elle seule les modules.

Enfin, le produit sur les points fermés donne formellement

\[
Z(E,T)=\exp\left(\sum_{n\ge1}\frac{N_n}{n}T^n\right).
\]

En effet, un point fermé de degré \(d\) contribue \(d\) points sur \(\mathbb F_{p^n}\) exactement lorsque \(d\mid n\). Comparer les logarithmes formels avec la factorisation rationnelle entraîne

\[
\boxed{\ N_n=p^n+1-\alpha^n-\beta^n\quad(n\ge1).\ }
\]

Ces identités de séries et cette factorisation ne requièrent aucune convergence analytique ni hypothèse de pureté. Voir aussi Milne, chapitre IV, remarque 9.11(a), p. 156.

## 9. La borne uniforme détermine les modules

La cubique reste sans racines multiples après toute extension du corps. La section 7 s'applique à chacun des corps \(\mathbb F_{p^n}\) et donne

\[
|\alpha^n+\beta^n|
 =|N_n-(p^n+1)|
 \le10p^{n/2}
 \quad\text{pour tout }n\ge1.
\]

Supposons, après permutation éventuelle, que \(A=|\alpha|>\sqrt p\). Comme \(\alpha\beta=p\),

\[
|\beta|=\frac pA<\sqrt p.
\]

L'inégalité triangulaire inverse donne

\[
|\alpha^n+\beta^n|
 \ge A^n-\left(\frac pA\right)^n.
\]

Après division par \(p^{n/2}\), il vient

\[
10\ge
 \left(\frac A{\sqrt p}\right)^n
 \left(1-\left(\frac p{A^2}\right)^n\right).
\]

Le premier facteur tend vers l'infini et le second vers 1. Contradiction. Aucun des deux modules ne peut donc dépasser \(\sqrt p\). Leur produit étant \(p\), on conclut

\[
\boxed{\ |\alpha|=|\beta|=\sqrt p.\ }
\]

L'argument exclut une compensation persistante entre deux termes d'amplitudes différentes ; il ne suppose pas leurs phases.

Pour tout \(n\ge1\), on en déduit la borne précise

\[
\boxed{\ |N_n-(p^n+1)|\le2p^{n/2}.\ }
\]

En particulier, \(n=1\) donne la borne de Hasse \(|N_1-(p+1)|\le2\sqrt p\).

## 10. Zéros dans la variable complexe \(s\)

Définissons la fonction zêta de cette courbe par

\[
\zeta_E(s)=Z(E,p^{-s})
 =\frac{(1-\alpha p^{-s})(1-\beta p^{-s})}
        {(1-p^{-s})(1-p^{1-s})}.
\]

Un zéro du numérateur vérifie \(p^s=\alpha\) ou \(p^s=\beta\). Ainsi

\[
p^{\operatorname{Re}s}=\sqrt p,
\qquad
\operatorname{Re}s=\frac12.
\]

Ces zéros ne sont pas annulés par les pôles du dénominateur, dont les parties réelles sont 0 et 1. Les familles de zéros et de pôles sont périodiques dans la direction imaginaire, de période \(2\pi/\log p\). L'équation fonctionnelle prend la forme \(\zeta_E(s)=\zeta_E(1-s)\).

C'est l'hypothèse de Riemann pour la fonction zêta de cette courbe elliptique sur un corps fini. Ce n'est pas l'hypothèse de Riemann pour \(\zeta(s)\) sur les entiers.

## 11. Séparation des preuves, certificats et problèmes restants

La chaîne logique est la suivante :

1. Les identités de Hasse et l'indépendance polynomiale produisent une borne de rang.
2. Une dimension supérieure au rang produit un polynôme auxiliaire non nul.
3. Le degré et la torsion produisent une borne \(10\sqrt q\) sur chaque extension.
4. Riemann-Roch fournit séparément la rationalité et le produit \(\alpha\beta=p\).
5. L'uniformité sur la tour force les modules \(\sqrt p\), puis la constante précise 2.

Un certificat en \(\mathbb F_{27}\), avec \(J=3,K=11,M=4\), est particulièrement utile : \(M>p=3\), donc il vérifie un cas inaccessible à l'ancien passage par \(k!\). Les paramètres garantissent \(\dim W=66>R=64\), \(D=103\) et \(|S|\le25\). La preuve universelle ne dépend pas de l'exécution de ce certificat ; les données effectives et le témoin sont rapportés séparément.

La partie de comptage reste valide pour une cubique singulière, mais on ne lui applique pas la fonction zêta elliptique de degré deux. Cette restriction est nécessaire : pour \(f=x^2(x+a)\), avec \(a\) non carré dans \(\mathbb F_p\), le modèle projectif singulier brut vérifie

\[
N_n=p^n+1-(-1)^n,\qquad
Z_{\mathrm{brut}}(T)=\frac{1+T}{(1-T)(1-pT)}.
\]

En effet, \(\sum_x\chi_{p^n}(x+a)=0\), et retirer \(x=0\) donne \(-\chi_{p^n}(a)=-(-1)^n\). Son comptage satisfait une borne en racine carrée, mais son zéro \(T=-1\) a module 1. Le passage spectral exige donc la forme elliptique du numérateur et le produit \(\alpha\beta=p\), et pas seulement la borne de comptage. La fonction zêta du modèle singulier brut ne doit pas être confondue avec celle de sa normalisation.

La caractéristique 2 n'est pas couverte. L'optimisation générale des paramètres n'est pas réglée par cette famille explicite.

Pour les entiers, il manque toujours un espace indépendant, un opérateur imposant une diminution structurelle du rang et un contrôle global des zéros jouant le rôle du degré. Des unités fictives peuvent accompagner un calcul homogène ; elles ne remplacent aucun de ces trois objets ni la preuve de leurs propriétés.

## 12. Sources et portée historique

- S. A. Stepanov (1969), *On the number of points of a hyperelliptic curve over a finite prime field*, <https://mathnet.ru/eng/im2197>. Référence de la méthode de polynômes auxiliaires et de multiplicités.
- E. Bombieri, *Counting points on curves over finite fields (d'après S. A. Stepanov)*, Séminaire Bourbaki, exposé 430 en 1973, publication en 1974, <https://www.numdam.org/item/SB_1972-1973__15__234_0/>.
- J. S. Milne (2021), *Elliptic Curves*, deuxième édition, World Scientific ; passages de rationalité précisés à la section 8, <https://www.jmilne.org/math/Books/EC2.pdf>. Site mathématique de l'auteur : <https://www.jmilne.org/math/>.

La contribution de V6.35 est la reconstruction explicite de cette chaîne dans le programme, avec sa séparation des hypothèses et des certificats. Elle ne revendique ni une nouvelle preuve historique de Hasse ni un transfert acquis à la fonction zêta de Riemann.

