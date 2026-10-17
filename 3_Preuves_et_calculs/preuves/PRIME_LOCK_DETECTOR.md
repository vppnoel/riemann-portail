# PRIME-LOCK — note technique

## Proposition de calibration

Soit une série de Dirichlet admettant, dans un demi-plan d'absolue convergence, un Euler-produit

\[
F(s)=\prod_p F_p(p^{-s})^{-1}.
\]

En développant \(\log F_p\), la dérivée logarithmique

\[
-\frac{F'}{F}(s)=\sum_n \Lambda_F(n)n^{-s}
\]

est supportée sur les puissances de nombres premiers \(n=p^k\).

Dans le cas particulier de facteurs locaux de degré 1

\[
F_p(p^{-s})=1-\alpha_p p^{-s},
\]

on a

\[
\Lambda_F(p^k)=\alpha_p^k\log p.
\]

PRIME-LOCK mesure séparément :

1. la fuite hors de l'ensemble \(\{p^k\}\) ;
2. le défaut de la loi locale de degré 1 ;
3. la propagation de ces défauts vers le signal global \(c_F\) utilisé depuis V3–V5.

## Intervention eulérisée

On fixe les données aux premiers par

\[
\alpha_p=\Lambda_F(p)/\log p
\]

et on définit

\[
\widehat\Lambda_F(p^k)=\alpha_p^k\log p,
\qquad
\widehat\Lambda_F(n)=0\quad(n\ne p^k).
\]

Cette construction est volontairement une intervention : elle ne prétend pas être la fonction originale. Elle demande : **que devient le signal global si l'on force exactement la structure locale absente ?**

## Limite

La loi \(\alpha_p^k\) est propre au degré 1. Pour un Euler-produit de degré supérieur, la bonne généralisation est d'abord le support sur les puissances de premiers, puis la reconstruction via les paramètres locaux appropriés.

## Résultat numérique principal

À \(N=32768\), zeta et \(L(s,\chi_5)\) satisfont les deux verrous à environ \(10^{-31}\), tandis que Davenport–Heilbronn donne une fuite \(\simeq0.9106\) et un défaut de tour \(\simeq0.7976\). L'eulérisation de DH préserve ses données aux premiers mais produit un signal global presque orthogonal au signal original (cohérence \(\simeq0.075\)).

Les témoins Steinhaus complètement multiplicatifs satisfont PRIME-LOCK malgré l'absence de structure analytique globale comparable. PRIME-LOCK est donc un détecteur de structure eulérienne locale, pas de RH.
