# Dimension de l'énergie : nouvelle branche active (v5.2)

## Idée

Le `1/2` de RH peut être interprété exactement comme la dimension d'une **generalized fractal string positive** construite à partir de l'énergie du programme.

On définit

\[
\mathcal Z_E(s)=\int_1^\infty |C(x)|^2x^{-1-2s}\,dx.
\]

Cette fonction est la zêta géométrique d'une mesure positive obtenue à partir de `|C(x)|^2 dx/x` par le changement d'échelle `y=x^2`.

Le Théorème A donne alors

\[
\boxed{D_E=\Theta},
\]

où `D_E` est l'abscisse de convergence de `Z_E` et `Theta` la partie réelle du zéro le plus à droite.

Ainsi

\[
\boxed{RH\iff D_E=1/2.}
\]

C'est une reformulation rigoureuse, pas une preuve de RH.

## Retour à l'énergie

Pour `s=1/2+eta`,

\[
\mathcal Z_E(1/2+\eta)=Q_\eta.
\]

Sous RH, le Théorème B devient

\[
\mathcal Z_E(1/2+\eta)\sim \frac{S}{4\eta^3},
\]

et, pour des zéros simples,

\[
\mathcal Z_E(1/2+\eta)\sim \frac{\kappa}{\eta^3}.
\]

Le `1/2` est donc à la fois la dimension critique et le bord où l'énergie amortie diverge cubiquement.

## Dimensions complexes du modèle fini

Dans un modèle avec un nombre fini de zéros, la transformée d'énergie possède des pôles aux positions

\[
\boxed{\omega_{jk}=\frac{\rho_j+\rho_k}{2}.}
\]

Sous RH, toutes ces valeurs sont sur `Re s=1/2`. Les fréquences imaginaires sont les demi-sommes/demi-différences des ordinées des zéros : ce sont exactement les battements observés dans les termes inférieurs de l'énergie.

Une paire synthétique `rho=0.63±7i` produit un pôle réel à `s=0.63`.

## Ce que les tests montrent

- identité exacte `Z_E(1/2+eta)=Q_eta` sur les troncatures arithmétiques ;
- formule finie des pôles validée contre une quadrature directe à `1.6×10^-10` ;
- toutes les dimensions complexes du modèle RH fini ont partie réelle `1/2` ;
- une paire hors ligne déplace immédiatement la dimension réelle vers `beta` ;
- la dimension effective de Davenport–Heilbronn [DH36b] [DH36a] est `≈0.781` à l'échelle calculée, cohérente avec la présence d'un zéro à `beta≈0.8085`.

Suite de tests du package : **43/43**.

## Nouvelle question d'attaque

La théorie des fractal strings ne force pas à elle seule `D_E=1/2`. Il faut donc rechercher une propriété additionnelle de la mesure d'énergie qui soit :

1. vraie pour `zeta` ;
2. liée au produit d'Euler ou à une positivité non automatique ;
3. fausse pour Davenport–Heilbronn ;
4. suffisamment forte pour imposer `D_E<=1/2`.

C'est désormais le point actif de la branche énergie/dimension.

Pour les preuves, formules et résultats numériques : `3_Preuves_et_calculs/preuves/ENERGY_FRACTAL_DIMENSION.md`.

<!-- references:debut -->

## Références

Format : [clé] auteurs, *titre*, publication, lien. Fiches complètes et état de vérification : document 42 (registre des sources).

- [DH36a] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series*. J. London Math. Soc. 11 (1936), no. 3, 181–185. <https://doi.org/10.1112/jlms/s1-11.3.181> — partiellement vérifié
- [DH36b] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series. II*. J. London Math. Soc. 11 (1936), no. 4, 307–312. <https://doi.org/10.1112/jlms/s1-11.4.307> — partiellement vérifié

<!-- references:fin -->
