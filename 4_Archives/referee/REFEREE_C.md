# Simulation de referee C — termes inférieurs et quasi-périodicité

## Objet

Le programme distingue :

1. une expansion **abélienne** de `Q_eta` en puissances de `eta^{-1}` ;
2. une expansion **ponctuelle** de `U(L)=Q(e^L)` où le coefficient de `L^2` contient une composante oscillante `Phi(L)`.

## Verdict provisoire

**Bonne correction conceptuelle, mais le résultat pour zeta est conditionnel et doit être énoncé comme tel.** La formule à nombre fini de zéros est algébriquement contrôlable ; le passage à l'ensemble infini des zéros exige des hypothèses supplémentaires non connues sous RH seule.

## C1. Expansion abélienne

Le calcul local autour d'un zéro simple produit les ordres

\[
\eta^{-3},\quad \eta^{-2},\quad \eta^{-1}.
\]

La cohérence entre la dérivation locale et la formule explicite à nombre fini de zéros est un bon contrôle interne.

### Réserve

Pour `zeta` elle-même, la sommation des coefficients contenant

\[
b_\rho=\frac{\zeta''(\rho)}{\zeta'(\rho)}-2\gamma_E
\]

nécessite des hypothèses de moment sur `1/zeta'(rho)` et du contrôle sur les paires de zéros proches. Le texte doit continuer à séparer clairement le modèle fini du théorème infini.

## C2. Terme L^2 presque périodique

La présence d'intégrales

\[
\int_0^L t^2 e^{i(\gamma-\gamma')t}dt
\]

produit naturellement des termes de taille `L^2/(gamma-gamma')` pour `gamma != gamma'`. Il est donc correct de corriger l'ancienne attente d'un coefficient constant : à niveau fini, le coefficient contient une fonction oscillante explicite `Phi_N(L)`.

### Point critique

Le passage `N->infinity` demande une condition de sommabilité sur les écarts. Le package propose une hypothèse `H_pair`. Cette hypothèse ne doit pas être présentée comme une conséquence connue de RH. Il faut aussi vérifier si la condition choisie est optimale ou seulement suffisante.

## C3. Presque-périodicité

Pour un nombre fini de fréquences, `Phi_N` est quasi-périodique au sens élémentaire. Pour l'infini, employer le terme « presque périodique » seulement après avoir précisé le mode de convergence : uniforme (Bohr), quadratique/Besicovitch, ou autre.

## C4. Relation avec GUE / petits écarts

L'idée que la répulsion de type GUE rendrait les paires très proches suffisamment rares est heuristique. Toute phrase de ce type doit être marquée comme conjecturale et ne doit pas être utilisée dans la preuve de B.

## Recommandation

Présenter C en trois étages :

- **C-fini** : formule exacte pour un ensemble fini de zéros ;
- **C-Abel** : expansion conditionnelle de `Q_eta` sous hypothèses de moments et paires proches ;
- **C-pointwise** : formule avec `Phi(L)` sous une hypothèse explicite de sommabilité des écarts.

Ne pas annoncer un développement asymptotique ponctuel avec coefficients constants `alpha,beta`.
