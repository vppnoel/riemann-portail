# Dimension fractale de l'énergie — module v5.2

## Statut

Ce module relie exactement la fonctionnelle d'énergie `Q` à la théorie des **generalized fractal strings** de Lapidus. Il ne prouve pas RH. Le résultat principal est une reformulation rigoureuse du Théorème A dans un langage de dimension, suivie d'un modèle fini exact des « dimensions complexes » de l'énergie.

La partie infinie concernant la continuation méromorphe et l'ensemble complet des dimensions complexes reste **ouverte/conditionnelle**.

---

## 1. Objet de départ

On conserve

\[
c(n)=(\Lambda*\Lambda)(n)-\Lambda(n)\log n+2\gamma\Lambda(n),
\qquad
C(x)=\sum_{n\le x}c(n),
\]

et

\[
Q(X)=\int_1^X |C(x)|^2\,x^{-2}\,dx.
\]

Le Théorème A donne

\[
\frac12\limsup_{X\to\infty}\frac{\log(1+Q(X))}{\log X}
=\Theta-\frac12,
\qquad
\Theta=\sup_\rho \Re\rho.
\]

## 2. Zêta d'énergie

Définissons, pour `Re s` assez grand,

\[
\boxed{
\mathcal Z_E(s)=\int_1^\infty |C(x)|^2x^{-1-2s}\,dx.
}
\]

Si `s=1/2+eta`, alors

\[
\mathcal Z_E\left(\frac12+\eta\right)
=\int_1^\infty |C(x)|^2x^{-2-2\eta}\,dx
=Q_\eta,
\]

la même énergie amortie que dans le Théorème B.

En posant

\[
U(L)=Q(e^L),
\]

on a exactement

\[
\boxed{
\mathcal Z_E(s)=
\int_0^\infty e^{-2(s-1/2)L}\,dU(L).
}
\]

Ainsi `Z_E` est une transformée de Laplace–Stieltjes de la mesure d'énergie.

---

## 3. Une generalized fractal string positive

Dans la convention de Lapidus, une generalized fractal string peut être une mesure positive locale `eta` sur `(0,infty)`, et sa zêta géométrique est sa transformée de Mellin

\[
\zeta_\eta(s)=\int_0^\infty y^{-s}\eta(dy).
\]

Définissons la mesure positive `eta_E` comme le push-forward de

\[
|C(x)|^2\frac{dx}{x}
\]

par l'application

\[
y=x^2.
\]

Autrement dit, pour une fonction test `phi`,

\[
\int \phi(y)\,\eta_E(dy)
=
\int_1^\infty \phi(x^2)|C(x)|^2\frac{dx}{x}.
\]

Alors

\[
\boxed{
\zeta_{\eta_E}(s)=\mathcal Z_E(s).
}
\]

La mesure est positive, localement finie, et portée dans `[1,infty)` : elle est donc une generalized fractal string positive au sens de cette théorie.

### Proposition E1 — dimension exacte

Soit `D_E` l'abscisse de convergence de `Z_E`, donc la dimension de `eta_E`. Alors

\[
\boxed{D_E=\Theta.}
\]

### Preuve

Par la relation de Laplace–Stieltjes,

\[
\mathcal Z_E(s)
=
\int_0^\infty
 e^{-2(s-1/2)L}\,dU(L),
\]

avec `U` positive et croissante. L'abscisse de convergence en la variable

\[
\lambda=2(s-1/2)
\]

est le taux exponentiel supérieur de `U`, soit

\[
\limsup_{L\to\infty}\frac{\log(1+U(L))}{L}
=2\Theta-1
\]

par le Théorème A. Donc

\[
2(D_E-1/2)=2\Theta-1,
\]

d'où `D_E=Theta`. ∎

### Corollaire

\[
\boxed{
RH\quad\Longleftrightarrow\quad D_E=\frac12.
}
\]

C'est une vraie dimension au sens des generalized fractal strings, mais c'est **une reformulation du Théorème A**, pas une nouvelle implication vers RH.

---

## 4. Retour au Théorème B : singularité cubique de l'énergie

Sous RH, le Théorème B donne

\[
Q(e^L)\sim \frac{S}{3}L^3.
\]

Par la transformation précédente,

\[
\boxed{
\mathcal Z_E\left(\frac12+\eta\right)
\sim \frac{S}{4\eta^3}
\qquad(\eta\downarrow0).
}
\]

Pour des zéros simples, `S=4 kappa`, donc

\[
\boxed{
\mathcal Z_E\left(\frac12+\eta\right)
\sim \frac{\kappa}{\eta^3}.
}
\]

Cela donne une **singularité abélienne d'ordre trois** au bord `Re s=1/2`. Le Théorème B seul ne fournit pas une continuation méromorphe à travers cette droite ; il serait donc prématuré de parler d'un pôle dans le problème infini sans hypothèse supplémentaire.

---

## 5. Modèle fini : dimensions complexes de l'énergie

Dans le modèle à un nombre fini de zéros, écrivons

\[
B_N(t)=e^{-t/2}C_N(e^t)
=\sum_j (A_j t+u_j)e^{(\rho_j-1/2)t},
\]

où l'ensemble fini des `rho_j` est fermé par conjugaison.

Définissons

\[
\mathcal Z_{E,N}(s)
=\int_0^\infty B_N(t)^2e^{-2(s-1/2)t}\,dt.
\]

L'intégration terme à terme est exacte et donne

\[
\mathcal Z_{E,N}(s)
=\sum_{j,k}
\left[
\frac{2A_jA_k}{d_{jk}^3}
+\frac{A_ju_k+u_jA_k}{d_{jk}^2}
+\frac{u_ju_k}{d_{jk}}
\right],
\]

avec

\[
d_{jk}=2s-\rho_j-\rho_k.
\]

### Proposition E2 — positions des pôles du modèle fini

Les pôles candidats sont donc

\[
\boxed{
\omega_{jk}=\frac{\rho_j+\rho_k}{2}.
}
\]

Sous RH,

\[
\rho_j=\frac12+i\gamma_j,
\]

donc

\[
\boxed{
\omega_{jk}
=\frac12+\frac{i}{2}(\gamma_j+\gamma_k),
}
\]

en utilisant l'ensemble signé des ordinées. Toutes les dimensions complexes du modèle fini sont donc sur `Re s=1/2`.

Avec la représentation par ordinées positives seulement, les mêmes fréquences apparaissent comme demi-sommes et demi-différences, ce qui est exactement la structure de battements déjà rencontrée dans la Proposition C.

### Hors RH

Une paire conjuguée

\[
\rho=\beta+i\gamma,
\qquad
\bar\rho=\beta-i\gamma
\]

produit notamment

\[
\frac{\rho+\bar\rho}{2}=\beta.
\]

Ainsi un zéro hors ligne crée, dans le modèle énergétique fini, une dimension complexe réelle située en `s=beta`.

---

## 6. Tests numériques v5.2

### T1 — identité avec l'énergie amortie

Sur les sommes arithmétiques tronquées :

\[
\mathcal Z_E(1/2+\eta;X)=Q_\eta(X)
\]

est vérifiée numériquement à la précision machine.

### T2 — formule méromorphe du modèle fini

Pour trois zéros et `s=0.84+0.17i`, la formule rationnelle exacte et l'intégration numérique directe diffèrent de

\[
1.6\times10^{-10}.
\]

### T3 — ligne critique

Avec trois paires de zéros sur RH, toutes les valeurs

\[
(\rho_j+\rho_k)/2
\]

ont partie réelle exactement `1/2` dans le calcul.

### T4 — zéro synthétique hors ligne

Pour

\[
\rho=0.63\pm7i,
\]

le modèle produit les dimensions

\[
0.63,
\qquad
0.63\pm7i,
\]

et donc un pôle réel à `0.63`.

### T5 — dimension effective à échelle finie

On peut visualiser

\[
D_{\rm eff}(X)=
\frac12+rac12\frac{\log(1+Q(X))}{\log X}.
\]

Pour ζ, sur les données jusqu'à `X=3,999,999`, cette quantité passe d'environ `0.68` à `0.666`. Cela ne contredit pas `D_E=1/2` sous RH : la convergence est extrêmement lente car `Q(X)` est polylogarithmique.

Sur le test Davenport–Heilbronn, la pente de dernière décade `0.5625` donne

\[
D_{\rm eff}\approx0.7813,
\]

à comparer avec le zéro hors ligne observé à partie réelle `0.8085`. Le biais vient de la faible hauteur/troncature déjà constatée dans les autres diagnostics.

---

## 7. Ce que cela apporte — et ce que cela n'apporte pas

### Apport réel

1. Le `1/2` peut être interprété **rigoureusement comme la dimension d'une generalized fractal string construite à partir de l'énergie**.
2. Le Théorème B devient une loi de singularité au bord de cette dimension critique.
3. Dans le modèle fini, les dimensions complexes de l'énergie sont les moyennes par paires des zéros ; la Proposition C devient alors une structure de battements/complex dimensions.
4. Un zéro hors ligne déplace immédiatement une dimension énergétique réelle vers `beta>1/2`.

### Limite

La théorie générale des generalized fractal strings n'impose pas que cette dimension soit `1/2`. Une mesure positive peut avoir beaucoup d'abscisses différentes. Davenport–Heilbronn fournit justement un témoin où la même construction détecte une dimension effective supérieure à `1/2`.

Ainsi, **nommer Θ une dimension ne force pas Θ=1/2**.

---

## 8. Nouvelle cible d'attaque

Le seul moyen pour que cette reformulation devienne plus qu'un dictionnaire serait de trouver une propriété supplémentaire de `eta_E`, provenant réellement de l'arithmétique de ζ, qui soit absente chez Davenport–Heilbronn et qui impose

\[
D_E\le\frac12.
\]

Candidats à tester :

1. une propriété de positivité plus forte que la positivité automatique de la mesure ;
2. une équation de renouvellement / autosimilarité arithmétique issue du produit d'Euler ;
3. une contrainte sur la continuation méromorphe de `Z_E` et ses dimensions complexes ;
4. une relation entre la structure de paires `((rho+rho')/2)` et une forme positive de type Weil ;
5. une propriété de stabilité sous convolution qui échouerait explicitement pour Davenport–Heilbronn.

Le test de rejet reste obligatoire : toute propriété candidate doit être calculée sur ζ, une fonction `L` avec produit d'Euler, et Davenport–Heilbronn.

---

## 9. Références de positionnement

- M. L. Lapidus & M. van Frankenhuijsen, *Fractal Geometry, Complex Dimensions and Zeta Functions* : generalized fractal strings comme mesures, zêta géométrique comme transformée de Mellin, dimension comme abscisse de convergence.
- M. L. Lapidus & H. Maier, *The Riemann Hypothesis and Inverse Spectral Problems for Fractal Strings*, J. London Math. Soc. 52 (1995), 15–35.
- H. Herichi & M. L. Lapidus, *Fractal Complex Dimensions, Riemann Hypothesis and Invertibility of the Spectral Operator*, Contemp. Math. 600; arXiv:1210.0882.

Le lien `D=1/2` avec RH existe donc déjà dans la littérature des fractal strings. La contribution propre de ce module est plus restreinte : **identifier notre énergie Q avec une generalized fractal string positive dont la dimension est exactement Θ, et exhiber dans le modèle fini les pôles aux moyennes de paires de zéros.** La priorité de cette construction exacte n'a pas été vérifiée exhaustivement.
