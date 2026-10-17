# Prévisions V6.23 — Axe J5, le Frobenius qui n'est pas un morphisme (écrites avant le calcul)

Auteur et titulaire des droits : Vincent NOËL. Écrit le 11 octobre 2026 à 22 h 12 UTC (horloge du conteneur ; 0 h 12 à Bruxelles), avant tout calcul de J5.

Expérience : la construction de Stepanov, faite pour de vrai, en algèbre linéaire sur F_p. Courbe y² = f(x), S = {x ∈ F_p : f(x) carré non nul}.
Fonction auxiliaire A(x) = Σ_{j<J} (r_j(x) + s_j(x) g(x)) φ(x)^j, g = f^{(p−1)/2}, deg r_j, s_j < K : 2JK inconnues.
Conditions : A s'annule à l'ordre M en chaque point de S : M·|S| équations linéaires. On compare trois choix de φ :
 (F) φ(x) = x^p, le Frobenius (morphisme inséparable : sa dérivée est nulle) ;
 (I) φ(x) = x, l'identité (morphisme séparable) ;
 (P) φ = une permutation aléatoire de F_p, écrite comme polynôme d'interpolation (pas un morphisme de la courbe).
- P1 : avec (F), le rang des conditions est bien inférieur à M·|S| (les dérivées de x^p s'annulent) : il existe une fonction
  auxiliaire non nulle même quand M·|S| > 2JK.
- P2 : avec (P), le rang vaut min(M·|S|, 2JK) (conditions génériques) : aucune fonction auxiliaire dès que M·|S| > 2JK.
- P3 : avec (I), même comportement qu'avec (P) : ce n'est pas d'être un morphisme qui compte, c'est l'inséparabilité.
- P4 : avec (F), la borne déduite |S| ≤ deg A / M est de la forme p/2 + O(√p), et elle est respectée par |S| mesuré.
