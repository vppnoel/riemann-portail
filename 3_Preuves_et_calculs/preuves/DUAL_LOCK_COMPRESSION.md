# DUAL-LOCK — compression finie de la forme explicite

**Statut :** expérience structurelle V6.3, calculée sans utiliser les zéros dans la construction.  
**Revendiquer une nouvelle preuve ou un nouveau critère de RH : interdit.**

## 1. Forme utilisée

Pour une fonction test compacte `f`, on considère l'autocorrélation `g=f*\tilde f`. La formule explicite de Guinand–Weil exprime la forme spectrale associée comme la somme de trois blocs calculables :

1. facteur gamma / conducteur (archimédien) ;
2. coefficients de `-F'/F` (local) ;
3. terme de pôle pour zeta.

Sous RH, le côté zéros de la forme de Weil est une somme de carrés. La positivité sur tout l'espace de tests est déjà équivalente à RH : V6.3 ne cherche donc qu'une **compression finie adversariale**.

## 2. Base finie

La base est fixée par

\[
f_j(x)=\left(1-\frac{|x|}{w}\right)_+\cos(\xi_jx),
\qquad
\xi_j=T+\Delta\left(j-\frac{m-1}{2}\right).
\]

Sa transformée de Fourier est explicite et le support de `f_i*f_j` est `[-2w,2w]`. La somme locale est donc finie : seuls les coefficients avec

\[
\log n<2w
\]

interviennent.

La matrice

\[
M_{ij}^{(F)}=\mathcal W_F(f_i*\widetilde f_j)
\]

est assemblée uniquement avec le conducteur, le facteur gamma et les coefficients de la dérivée logarithmique. **Aucun zéro n'entre dans sa construction.**

## 3. Contrôle apparié

Pour éviter de confondre différence d'Euler-produit et différence triviale de facteur gamma, on compare Davenport–Heilbronn à la moyenne des formes explicites de `L(s,chi)` et `L(s,conj chi)` pour le caractère primitif d'ordre 4 modulo 5. Les deux utilisent `q=5` et le même gamma impair.

## 4. Protocole

- dimension `m=7` ;
- pas fréquentiel `Delta=0.6` ;
- scan `T=0,...,200` ;
- deux demi-largeurs : `w=2.5` et `w=3.5` ;
- premier passage rapide par convolution FFT ;
- toute poche négative candidate est recalculée par quadrature directe ;
- les zéros DH déjà présents dans le corpus ne sont consultés **qu'après** le scan, comme contrôle post hoc.

## 5. Lecture

Une valeur propre négative signifie seulement qu'une direction du sous-espace fini choisi rend la forme négative. Pour DH, c'est attendu puisque la fonction possède des zéros hors droite. Pour zeta, une négativité réelle serait extraordinairement grave ; en pratique les valeurs propres extrêmement petites exigent une arithmétique certifiée, car l'annulation du côté géométrique est numériquement délicate.

Les travaux récents sur la positivité de Weil en fenêtres compactes confirment ce point : les compressions finies sont un outil naturel, mais les petites valeurs propres demandent des bornes rigoureuses / multiprécision pour éviter des faux négatifs.

## 6. Métaphore V6

Nom : **l'interféromètre de Weil**.

- `w` = ouverture de l'instrument ;
- `T` = fréquence pointée ;
- la plus petite valeur propre = défaut de compatibilité dans la sous-famille de tests ;
- l'inertie = nombre de directions de signe négatif détectées.

Correspondance interdite : une poche négative d'un modèle adversarial n'est ni une découverte de zéro ni une preuve concernant zeta. Le dispositif sert à comprendre comment une structure locale+globale se manifeste dans une compression finie.
