# Lecture contradictoire de la reconstruction du certificat V6.50

Date : 13 octobre 2026. Examen de `reconstruction.py` et de
`tentative_certificat_integral.py` dans `v650_reconstruction_constructive`.
La conclusion numérique de l'exécution complète doit être lue dans son
journal final. Cette note examine la chaîne de démonstration et ses domaines.

## 1. La brique qui corrige les cellules de changement de signe

Sur une cellule centrée de largeur h, noter
\(K(t)=|r_t\rangle\langle r_t|\),
\(\phi(t)=(U-b_{\mathrm{lin}}(t))_+\), et
\(W=\int\phi(t)dt\). Si \(\phi\) est L-lipschitzienne,
\(0\le\phi\le U\), \(\|K'\|\le K_1\) et \(\|K''\|\le K_2\),
\[
\left\|\int_{-h/2}^{h/2}\phi(t)K(t)dt-WK(0)\right\|
\le h^3\left(\frac{LK_1}{12}+\frac{UK_2}{24}\right).
\]
**Preuve.** Développer K à l'ordre 1 avec reste borné par
\(K_2t^2/2\). Dans le terme linéaire,
\(\int t\phi(t)dt=\int t[\phi(t)-\phi(0)]dt\), de module au plus
\(L\int t^2dt=Lh^3/12\). Majorer le reste avec \(\phi\le U\).
La partie positive n'a pas besoin d'être deux fois dérivable. □

Pour les ondes projetées sur les deux moments de l'intervalle [-S,S],
\[
K_1\le\frac{4S^2}{\sqrt3},\qquad
K_2\le4S^3\left(\frac1{\sqrt5}+\frac13\right).
\]
La projection orthogonale L² est une contraction : ces bornes suivent de
\(\|r_t^{(j)}\|\le\sqrt{2S^{2j+1}/(2j+1)}\), j=0,1,2.
Les poids W peuvent être intégrés exactement sur un morceau linéaire puis
encadrés par monotonie de ses deux valeurs aux extrémités. La même formule
couvre les cellules où la partie positive change de branche. On évite ainsi
un budget d'ordre h venant d'un poids gelé au milieu.

La table de valeurs de b de rayon epsilon produit une erreur uniforme
\(\epsilon+B_2H^2/8\). Par Plancherel et la contraction de la projection,
cette erreur est une erreur opératoire L² de même taille, sans facteur T/pi.
La pente de la table est majorée par \(B_1+2\epsilon/H\), ce qui explique
le L employé dans le nouveau programme.

## 2. Une queue scalaire beaucoup plus fine

Pour \(f_t(B)=2t^2/[B(B^2+t^2)]\),
\[
f_t(B)=\int_0^\infty e^{-Bu}\,2(1-\cos(tu))du.
\]
La mesure est positive. La queue de la série, dont les abscisses sont
B,B+2,B+4,..., est donc l'intégrale de
\(e^{-Bu}/(1-e^{-2u})\) contre cette mesure. L'identité en fractions
partielles de coth [DLMF4.36.3] donne, pour tout u>0,
\[
\frac1u+\frac u3-\frac{u^3}{45}
\le\coth u\le\frac1u+\frac u3.
\]
On obtient ainsi
\[
A(B,t)-\frac4{15B^4}\le\sum_{k\ge0}f_t(B+2k)\le A(B,t),
\]
\[
A(B,t)=\frac12\log(1+t^2/B^2)
+\frac12f_t(B)-\frac16f_t'(B).
\]
**Justification du reste.** La différence des deux approximations de
\(1/(1-e^{-2u})=(1+\coth u)/2\) est au plus u³/90. Comme
\(2(1-\cos(tu))\le4\), son intégrale vaut au plus
\(4\cdot3!/(90B^4)=4/(15B^4)\). □

Avec B=512,5, la largeur analytique uniforme vaut environ 3,87e-12.
Le rayon plus large de la table reconstruite inclut l'arrondi des autres
opérations. La largeur de la série/intégrale simple du document 73 ne doit
pas être copiée dans ce nouveau calcul.

## 3. Autres raccords relus

| Raccord | Vérification de la lecture critique |
|---|---|
| Euler gamma | Le signe est correct : gamma est entre Hn−log n−1/(2n)+1/(12n²)−1/(120n⁴) et la même expression sans le dernier terme. Les bornes des fonctions élémentaires doivent rester orientées. |
| Gauss640 | Les 320 changements de signe rationnels positifs, leur réflexion, le degré640 et des intervalles disjoints donnent exactement640 racines. La formule des poids est celle de Gauss ; Markov fournit le contrôle de variation de la dérivée. |
| Moments | Le Gram est le Gram analytique diag(S+sinh S,sinh S−S), et ne provient pas des valeurs sur une grille. Les ondes sont projetées avant interpolation. |
| Interpolation | À S=.55,T=700,N640, R0=21/20 domine sqrt(2S). Le coefficient de projection est <7 et exp(S/2)<4/3 ; le facteur28/3 est donc un majorant valide. Le terme rationnel principal est 7,559063705e-57. |
| Sinus et cosinus | La nouvelle réduction /512 suivie de9 doublements porte sur la phase spatiale <=385. Le domaine du certificat historique, <=45, ne pouvait être simplement recopié. |
| Poids intégrés | L'intégrale de la partie positive d'une fonction affine est croissante dans les deux valeurs aux extrémités ; évaluer les extrémités inférieures et supérieures donne l'intervalle du poids exact. |
| Vecteurs | Les intervalles des nœuds, poids, ondes, exponentielles et moments sont propagés dans les coefficients cardinaux. Le maximum de chaque erreur de ligne majore l'erreur L² de chaque colonne entière. |
| Assemblage | Après remplacement par les colonnes et poids dyadiques exacts proposés, les produits et sommes en binaire64 ont un budget supplémentaire. Le modèle gamma_(2nf+128), facteur32, couvre les sommes absolues de colonnes dans les gardes de norme déclarées. |
| Plafond matriciel | Le C dyadique triangularisé est seulement un candidat inversible. L'intervalle direct de C(tau I−M)Cᵀ et sa stricte dominance diagonale positive démontrent la positivité pour la M dyadique exacte, sans confiance dans le solveur. |
| Portée | La borne de norme continue exige la somme de toutes les erreurs, y compris la symétrisation. Le plafond de la matrice seule ne certifie pas la forme infinie. |

Les bornes B1=8 et B2=35 ont des justifications rationnelles simples :
\(\sum b_n^{-2}\le109/25\), \(\sup a'\le(21/16)109/25\),
\(\sup|a''|\le4(8+0,064+0,04)=32,416\).
Les phases des premiers2 et3 ajoutent au plus
\(2(0,7^2/1,4+1,1^2/1,7)\) pour la première dérivée,
\(2(0,7^3/1,4+1,1^3/1,7)\) pour la seconde. Les sommes sont strictement
inférieures à8 et35. Les gardes élémentaires log2<.7, log3<1.1,
sqrt2>1.4 et sqrt3>1.7 peuvent être encadrées indépendamment.

## 4. Corrections demandées et contrôles de portée

1. Le reste de la série de log utilisait une puissance et un quotient
   flottants avec un seul arrondi final. Il a été remplacé par le majorant
   rationnel uniforme 1/(483·2^158), puisque le domaine impose |y|<=1/2.
2. Les extrémités de l'encadrement Euler doivent être prises par arrondi
   inférieur/supérieur, en conservant les rationnels de l'EM ; la prise d'un
   milieu n'exprime pas cette garde.
3. La sérialisation des erreurs rationnelles N640 dépasse la limite Python
   de4300 chiffres. La désactivation locale de cette limite est nécessaire
   avant le journal final ; elle ne change pas les calculs mathématiques.
4. Les matrices finales du certificat doivent être archivées séparément
   de celles du diagnostic, qui n'employait pas exactement la même projection.
   Un plafond doit être revalidé contre la matrice exacte correspondante.

Les deux premières corrections et le problème de sérialisation ont été
confirmés comme pris en charge par l'auteur de la construction. Les nœuds
Gauss640 ont été exécutés et vérifiés. La sauvegarde des matrices intégrales
et leur empreinte a été ajoutée à l'exécution finale.

L'exécution a également été accélérée en construisant les vecteurs seulement
dans les cellules dont le poids central wm est positif. Ce changement est
licite avec une dette déclarée : une cellule omise a un poids exact au plus
maxerror, et son vecteur interpolé exact a une norme au plus R0+epsilonN<2.
Elle coûte donc au plus4·maxerror. Pour les cellules actives, les erreurs de
vecteur et de poids restent celles décrites ci-dessus. La même somme totale
16·nf·maxerror couvre les deux groupes de cellules ; le budget des vecteurs
ne concerne que les colonnes effectivement calculées. L'intégration analytique
et la garde de queue fréquentielle demeurent les mêmes.

Les hypothèses matérielles restent celles déclarées : opérations élémentaires
IEEE binaire64 correctement arrondies, modèle de produits/sommes gamma_n,
intervalles mpmath, signes de polynômes entiers exacts. Cette lecture ne
constitue pas une validation formelle du compilateur ou du processeur.

## 5. Sens d'une éventuelle clôture positive

Si le journal final donne une marge massique strictement positive après
tous ces budgets, le résultat portera sur tous les tests complexes de X_.55,
puis sur tous X_S, S<=.55, par inclusion. Il rencontrera réellement le premier3.
Le transport T_r donne parallèlement un langage global de supports, moments
et domaines. La loi de signe pour tous les supports reste ouverte, et ces
deux avancées ne doivent pas être fusionnées en une affirmation de RH.

Sources primaires vérifiées pour les deux fonctions spéciales :
https://dlmf.nist.gov/4.36#E3 (fractions partielles de coth),
https://dlmf.nist.gov/5.11#E2 et https://dlmf.nist.gov/5.11#ii (digamma et signe
du premier terme négligé sur l'axe réel positif).
