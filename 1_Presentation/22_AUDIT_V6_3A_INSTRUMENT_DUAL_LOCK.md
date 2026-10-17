# V6.3a — Audit de l'instrument DUAL-LOCK

**Date :** 5 octobre 2026  
**Statut :** audit numérique et méthodologique — aucune revendication nouvelle sur RH

## 1. Pourquoi cet audit

La V6.3 avait mis en évidence des directions négatives pour Davenport–Heilbronn [DH36b] [DH36a] (DH) dans des compressions finies de la forme explicite, tandis que le contrôle eulérien apparié \(L_{\chi_5}\) restait positif. Deux sorties numériques légèrement différentes ont toutefois révélé que plusieurs niveaux de calcul avaient été mélangés : screening, confirmation précise et décomposition « Résidu sombre ».

L'audit V6.3a impose désormais un pipeline unique :

\[
M_i \longrightarrow M=\sum_i M_i \longrightarrow G
\longrightarrow Mv=\lambda Gv,
\qquad v^T Gv=1,
\]

puis

\[
\lambda=v^TMv=\sum_i v^TM_i v.
\]

Ici \(G\) est la matrice de Gram de la base de fonctions test. Le problème généralisé est nécessaire parce que la base utilisée n'est pas orthonormale et devient fortement mal conditionnée lorsque la dimension augmente.

## 2. Réconciliation dans un run unique

Avec exactement les mêmes paramètres pour `compression_accurate` et la somme des composantes, les matrices coïncident à l'arrondi machine (`matrix_reconcile_maxabs` nul ou \(\lesssim 4.5\times10^{-16}\)).

Les valeurs propres généralisées minimales à dimension 7, calculées avec `arch_dt=0.02` et `correlation_eps=2e-8`, sont :

| T | demi-largeur | DH | contrôle \(L_{\chi_5}\) |
|---:|---:|---:|---:|
| 86 | 2.5 | **-1.55861055** | **+1.61384259** |
| 113 | 2.5 | **-0.31276149** | **+2.16116322** |
| 167 | 3.5 | **-0.19045925** | **+1.64785425** |
| 176 | 2.5 | **-0.61334410** | **+3.08618876** |

Le signe est donc beaucoup mieux séparé après normalisation par \(G\) que ne le suggéraient les petites valeurs propres ordinaires du contrôle.

## 3. Conditionnement de la base

À \(T=86\), le conditionnement de \(G\) croît rapidement :

| dimension | \(\kappa(G)\) |
|---:|---:|
| 3 | \(1.75\times10^2\) |
| 5 | \(1.09\times10^4\) |
| 7 | \(5.26\times10^5\) |
| 9 | \(2.33\times10^7\) |
| 11 | \(9.96\times10^8\) |

**Conséquence :** les valeurs propres ordinaires de \(M\) ne sont pas quantitativement canoniques. L'inertie de la forme est l'information robuste ; toute grandeur utilisant un vecteur propre doit être calculée dans le problème généralisé et contrôlée contre le conditionnement.

## 4. Persistance en dimension — partie vérifiée par recoupement

### T = 86

\[
\lambda_{\min}^{DH}= -1.285,-1.516,-1.559,-1.642,-1.744
\]

pour les dimensions \(3,5,7,9,11\), tandis que le contrôle reste positif :

\[
2.466,1.960,1.614,1.513,1.507.
\]

### T = 113

À dimension 3, la direction négative n'est pas encore capturée : \(+1.707\). Elle apparaît à dimension 5 et persiste à dimension 7 :

\[
-0.304,\;-0.313.
\]

Le contrôle reste \(>2\) sur ces dimensions.

### T = 167

Pour les dimensions \(3,5,7\) :

\[
\lambda_{\min}^{DH}= -0.173,-0.175,-0.190,
\]

contre

\[
\lambda_{\min}^{L}=3.458,2.370,1.648.
\]

### T = 176

À dimension 3 le témoin DH reste positif, puis une direction négative apparaît à dimension 5 et persiste à dimension 7 avec la tolérance haute précision :

\[
+0.580,\;-0.551,\;-0.613.
\]

Le contrôle reste autour de \(3.1\).

## 5. Artefact numérique réellement trouvé

La combinaison « grande dimension + base mal conditionnée + tolérance locale trop lâche » peut fabriquer des valeurs propres généralisées absurdes.

Exemple \(T=176\), dimension 7 :

- `correlation_eps = 2e-8` : \(\lambda_{\min}^{DH}\approx -0.61334\) ;
- `correlation_eps = 1e-7` ou `5e-7` : une direction quasi-nulle de \(G\) amplifie l'erreur et produit une valeur artificielle d'environ \(-9.995\).

Une quadrature indépendante (Gauss–Legendre fixe pour les corrélations locales et quadrature Gauss composite pour l'archimédien) donne

\[
\lambda_{\min}^{DH}(176)\approx -0.61345,
\]

et

\[
\lambda_{\min}^{L}(176)\approx +3.08619.
\]

Donc **le signe principal survit**, mais la magnitude généralisée peut devenir catastrophiquement fausse si l'on ne contrôle pas l'erreur en fonction de \(\kappa(G)\).

C'est une correction méthodologique majeure de V6.3.

## 6. Cross-check indépendant à T = 86

À dimension 5 :

- pipeline principal :
  \[
  \lambda_{\min}^{DH}=-1.51595548,\quad
  \lambda_{\min}^{L}=+1.96003081;
  \]
- pipeline indépendant Gauss–Legendre :
  \[
  \lambda_{\min}^{DH}=-1.51595543,\quad
  \lambda_{\min}^{L}=+1.96003097.
  \]

L'accord est de l'ordre de \(10^{-7}\) ou meilleur sur la valeur propre généralisée, avec conservation du signe.

## 7. Résidu sombre recalculé dans la métrique correcte

Les facteurs d'amplification V6.3 étaient calculés avec le vecteur propre ordinaire de \(M\). Ils sont donc rétrogradés. Avec le vecteur propre généralisé normalisé par \(v^TGv=1\), on obtient à dimension 7 :

| T | amplification sombre DH | contrôle |
|---:|---:|---:|
| 86 | **6.42×** | 4.23× |
| 113 | **29.84×** | 3.15× |
| 167 | **52.33×** | 4.93× |
| 176 | **17.12×** | 2.20× |

La métaphore **Résidu sombre** survit donc qualitativement, mais ses nombres ont changé. Le cas \(T=167\) reste la cancellation la plus marquée dans ce jeu : le résidu généralisé représente environ \(1/52\) de la somme des amplitudes projetées.

## 8. Décisions modifiées

1. **DUAL-LOCK reste ouvert.** Les directions négatives DH survivent aux contrôles les plus importants.
2. **Les valeurs propres ordinaires ne doivent plus servir d'échelle quantitative.** Elles peuvent servir au screening de signe, puis toute confirmation utilise \((M,G)\).
3. **Toute dimension élevée doit être accompagnée de \(\kappa(G)\)** et d'une précision de quadrature adaptée.
4. **Le second mode négatif signalé auparavant à \(T=176\) est retiré.** Il n'est pas confirmé.
5. **Les anciens facteurs 10.7×, 36.7×, 70.3×, 28.6× sont remplacés** par les facteurs généralisés ci-dessus.
6. Avant toute nouvelle interprétation, il reste à auditer les conventions de la formule explicite : normalisation de Fourier, facteurs \(2\pi\), facteur gamma, coefficients DH.

## 9. Statut de l'instrument

Le bon résumé n'est plus « Résidu sombre stable » mais :

> **Le signe négatif DH est robuste sur les témoins principaux après normalisation de Gram et cross-check numérique ciblé ; l'instrument reste sensible au conditionnement de la base, donc les magnitudes exigent une précision adaptative et un audit de formule avant exploitation théorique.**

La V6.3a est donc un **audit d'instrument réussi** au sens méthodologique : elle conserve le phénomène principal, retire un faux mode et réduit les revendications quantitatives à ce que les calculs supportent effectivement.


> **Note V6.3c.** « Certifié » a été remplacé par « vérifié par recoupement » : en calcul numérique, « certifié » désigne des bornes rigoureuses (arithmétique d'intervalles), ce qui n'est pas le cas ici.

<!-- references:debut -->

## Références

Format : [clé] auteurs, *titre*, publication, lien. Fiches complètes et état de vérification : document 42 (registre des sources).

- [DH36a] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series*. J. London Math. Soc. 11 (1936), no. 3, 181–185. <https://doi.org/10.1112/jlms/s1-11.3.181> — partiellement vérifié
- [DH36b] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series. II*. J. London Math. Soc. 11 (1936), no. 4, 307–312. <https://doi.org/10.1112/jlms/s1-11.4.307> — partiellement vérifié

<!-- references:fin -->
