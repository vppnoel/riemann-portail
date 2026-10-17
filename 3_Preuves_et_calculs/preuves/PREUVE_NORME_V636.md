# V6.36 — Traces en intervalles et sous-espace négatif de DH

**Cadre.** a=1/50, h=1/200, L=1115, conducteur 5 et parité impaire. La preuve porte sur cette fenêtre fixée. Le modèle d'arrondi employé pour les produits matriciels est IEEE binary64, sans débordement ni sous-flux significatif. Le calcul des traces emploie des intervalles à 60 chiffres ; aucune liste de zéros n'entre dans leur construction.

## 1. Convolution exacte et formule physique

Pour la bosse \(\varphi(u)=\cos^4(\pi u/(2a))\) sur \([-a,a]\), nulle ailleurs, posons \(g=\varphi*\varphi\) et \(b=\pi/a\). L'intégration du produit des harmoniques donne, pour \(0\le x\le2a\),

\[
g(x)=(2a-x)\left(\frac9{64}+\frac18\cos bx+\frac1{128}\cos2bx\right)
+\frac5{24b}\sin bx+\frac{25}{768b}\sin2bx.
\]

On prolonge par parité et par zéro hors du support. Cette expression est évaluée en intervalles, ce qui conserve les annulations près des extrémités. Ses deux branches analytiques sont séparées au point zéro.

La représentation de la fonction digamma (NIST DLMF, 5.9.16) est

\[
\psi(z)+\gamma_E=\int_0^\infty
\frac{e^{-u}-e^{-zu}}{1-e^{-u}}\,du\qquad(\Re z>0).
\]

L'inversion de Fourier donne, avec \(\sigma=3/4\) et \(t=nh\), le terme archimédien exact

\[
A(t)=(\log(5/\pi)-\gamma_E)g(t)
+\int_0^\infty
\frac{e^{-u}g(t)-\frac12 e^{-\sigma u}
 [g(t+u/2)+g(t-u/2)]}{1-e^{-u}}\,du.
\]

Le quotient a une singularité amovible au point 0, de limite \((\sigma-1)g(t)\). Pour \(B=2t+4a\), les deux termes déplacés sont nuls au-delà de \(B\). La queue est exactement

\[
-g(t)\log(1-e^{-B}).
\]

Si \(t>2a\), on a \(g(t)=0\) et le changement de variable \(x=t-u/2\) réduit tout le terme à

\[
A(t)=-\int_{-2a}^{2a}
g(x)\frac{e^{-2\sigma(t-x)}}{1-e^{-2(t-x)}}\,dx.
\]

Les formules physiques évitent une troncature de la queue de Fourier. La comparaison avec l'ancien quadrateur Fourier reste un contrôle mesuré, et non une borne d'erreur.

## 2. Majorants analytiques de quadrature

La quadrature de Gauss–Legendre d'ordre \(m=16\), sur un panneau de longueur \(\ell\), a un reste majoré par

\[
\frac{\ell^{2m+1}(m!)^4}
 {(2m+1)((2m)!)^3}\sup |f^{(2m)}|.
\]

Si chaque point du panneau possède un disque d'analyticité de rayon \(\rho\), sur lequel \(|f|\le M\), l'estimation de Cauchy donne

\[
|E_{\rm panneau}|\le
\frac{\ell^{33}(16!)^4 M}
 {33(32!)^2\rho^{32}}.
\]

Le programme choisit \(\ell\le\rho/2\) et ajoute ce reste, symétriquement, à l'intervalle évalué de la quadrature.

### 2.1. Cas \(t>2a\)

On sépare les deux branches de \(g\) au point 0 et on choisit

\[
\rho=\min\left(\frac1{50},\frac{t-2a}{2}\right).
\]

Le prolongement analytique de la branche positive peut s'écrire comme l'intégrale du produit de deux cosinus à la puissance quatre, sur un segment complexe de longueur \(2a-z\). Pour un disque de rayon \(\rho\) centré dans \([0,2a]\), cette représentation donne

\[
|g(z)|\le(2a+\rho)e^{4\pi\rho/a}.
\]

La branche négative possède le même majorant. On a aussi \(t-\Re z\ge t-2a-\rho>0\), donc

\[
\left|\frac{e^{-2\sigma(t-z)}}{1-e^{-2(t-z)}}\right|
\le\frac1{1-e^{-2(t-2a-\rho)}}.
\]

Le majorant \(M\) utilisé est le produit de ces deux bornes. La division entre branches est indispensable : on n'applique pas Cauchy à une fonction tronquée au travers d'une jonction.

### 2.2. Cas \(n=0,\ldots,8\)

Ici \(0\le t\le2a\). L'intégrale en \(u\) est divisée aux jonctions positives \(2t\), \(4a-2t\) et \(2t+4a\). On emploie \(\rho=1/1000\) et \(M=1000\).

Voici une justification volontairement large de ce dernier majorant. Sur les disques considérés, \(|u|\le0,162\), et les arguments des branches de \(g\) ont une partie réelle entre \(-0,041\) et \(0,121\), avec une partie imaginaire de module au plus \(0,0005\). La formule trigonométrique, avec \(\pi/a<158\) et \(|\sin z|,|\cos z|\le e^{|\Im z|}\), donne

\[
|g_{\rm branche}|\le0,1,\qquad
|g'_{\rm branche}|\le10.
\]

Pour la première branche du quotient, son numérateur \(N(u)\) est analytique, \(N(0)=0\), et \(|N'(u)|<11\) sur les chemins droits allant de 0 aux points des disques. Il en résulte \(|N(u)/u|<11\). D'autre part,

\[
\left|\frac{1-e^{-u}}u-1\right|
\le\frac{e^{|u|}-1-|u|}{|u|}<0,1,
\]

donc \(|u/(1-e^{-u})|<2\) et le quotient est de module inférieur à 22. Cela couvre aussi \(t=0\) et \(t=2a\), par les identités exactes \(g'(0)=0\), \(g(2a)=0\).

Pour les autres branches, le plus petit point de jonction positif est \(0,01\). Leurs disques vérifient \(\Re u\ge0,009\), donc \(|1-e^{-u}|\ge1-e^{-0,009}>0,0089\). Le numérateur a module inférieur à \(0,3\), et le quotient est inférieur à 34. Le majorant commun 1000 couvre donc toutes ces branches. Les noeuds de Gauss restent strictement dans les panneaux ; aucun intervalle évalué ne contient \(u=0\).

## 3. Encadrement des évaluations et des coefficients

Les centres des 16 noeuds de Gauss sont calculés à haute précision puis encadrés. L'évaluation en intervalles du polynôme de Legendre montre deux signes opposés aux extrémités de chaque encadrement. Les 16 encadrements sont disjoints ; ils contiennent donc chacun une racine exacte. Les poids sont encadrés par

\[
w_i=\frac2{(1-x_i^2)(P'_{16}(x_i))^2}.
\]

Pour DH, les coefficients de la série sont périodiques, de valeurs \(0,1,\xi,-\xi,-1\), avec

\[
\xi=\frac{\sqrt{10-2\sqrt5}-2}{\sqrt5-1}.
\]

Les radicaux et les logarithmes sont évalués en intervalles. Si \(a_n\) sont ces coefficients, les coefficients \(c_n\) de la dérivée logarithmique sont obtenus par la récurrence exacte

\[
c_n=a_n\log n-\sum_{\substack{d\mid n\\2\le d<n}}c_d a_{n/d}.
\]

Le support impose \(m\le e^{(L-1)h+2a}\). Le programme vérifie en intervalles que ce maximum est inférieur à la borne entière \(M\) utilisée ; aucun coefficient omis ne peut contribuer. Comme \(\log2>2a\) et \(t\ge0\), le support \(g(-\log m-t)\) est vide pour tous les \(m\ge2\).

Chaque trace exacte est ainsi encadrée. Son centre binary64 est un dyadique exact ; son rayon est arrondi vers l'extérieur. Les extrémités des intervalles sont archivées en représentation binaire exacte de mpmath.

## 4. Passage des rayons à une borne matricielle

Pour la matrice hermitienne de Toeplitz \(G\) et son centre \(\widehat G\), des rayons \(\delta_k\) donnent

\[
\|G-\widehat G\|_2\le\|G-\widehat G\|_F
\le\varepsilon=
\sqrt{L\delta_0^2+2\sum_{k=1}^{L-1}(L-k)\delta_k^2}.
\]

Cette somme et sa racine sont évaluées en intervalles. On ne remplace pas cette borne par la différence de deux programmes.

## 5. Certificat d'un sous-espace négatif

Le calcul flottant des vecteurs propres ne sert qu'à proposer une matrice \(V\) de \(k\) colonnes. Ces colonnes sont ensuite considérées comme des vecteurs dyadiques exacts. Il suffit de démontrer que \(V^TGV\) est négative définie. Cela implique simultanément l'indépendance de ses colonnes et l'existence d'au moins \(k\) directions négatives de \(G\) ; aucun compte exact de toutes les directions n'en découle.

Posons \(u_{\rm machine}=2^{-53}\) et \(\gamma=(2L+2)u_{\rm machine}/(1-(2L+2)u_{\rm machine})\). Le facteur est conservatif pour les produits scalaires en binary64. Pour

\[
S_{\rm fl}={\rm fl}(\widehat GV),\qquad
B_{\rm fl}={\rm fl}(V^TS_{\rm fl}),
\]

le modèle standard des produits matriciels donne la majoration, entrée par entrée,

\[
|B_{\rm fl}-V^T\widehat GV|
\le\gamma|V^T||S_{\rm fl}|
+\gamma|V^T||\widehat G||V|.
\]

Les produits positifs du membre de droite sont à leur tour majorés à partir de leurs évaluations flottantes, par division par \(1-\gamma\) pour un produit et par \((1-\gamma)^2\) pour deux produits. Les opérations scalaires sont majorées vers l'extérieur, avec une inflation de 32 unités d'arrondi.

Les normes carrées des colonnes de \(V\) sont évaluées en intervalles et vérifiées inférieures à 2. Par conséquent, chaque entrée de \(V^T(G-\widehat G)V\) a module au plus \(2\varepsilon\). On ajoute cette quantité au budget précédent.

Si \(e_{ij}\) est le budget final de l'entrée \(ij\), les sommes de Gershgorin, évaluées en intervalles,

\[
(B_{\rm fl})_{ii}
+\sum_{j\ne i}|(B_{\rm fl})_{ij}|+\sum_j e_{ij},
\]

majorent les extrémités droites des disques de la matrice exacte \(V^TGV\). Si leur maximum est strictement négatif, cette matrice est négative définie. Le certificat ne dépend alors d'aucune hypothèse sur l'exactitude des vecteurs propres proposés.

## 6. Portée et limites

Le certificat est reproductible sous les hypothèses de l'arithmétique d'intervalles et du modèle d'arrondi explicités ci-dessus. Il fournit une borne inférieure sur l'inertie de cette fenêtre de DH. Il ne prouve pas le compte exact, ni une règle de parité pour le compte total, ni une positivité de la zêta sur toutes les fenêtres.

Sources primaires : NIST DLMF 5.9.16, <https://dlmf.nist.gov/5.9#E16> ; N. J. Higham et T. Mary, *A New Approach to Probabilistic Rounding Error Analysis* (2019), introduction rappelant le modèle déterministe et \(\gamma_n\), <https://epubs.siam.org/doi/10.1137/18M1226312>. Seul le modèle déterministe est employé ici, aucun argument probabiliste.
