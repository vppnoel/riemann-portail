# V6.3 — DUAL-LOCK et Résidu sombre : résultats du test local/global

**Date :** 5 octobre 2026  
**Statut :** expérience structurelle reproductible — aucune revendication de preuve de RH

## 1. Question testée

Après PRIME-LOCK, la multiplicativité locale ne suffisait pas : des témoins complètement multiplicatifs de type Steinhaus passent le verrou local sans posséder la structure globale d'une fonction L.

DUAL-LOCK teste donc directement une **compression finie de la forme explicite**, construite uniquement avec :

- le facteur archimédien ;
- le conducteur et, le cas échéant, le pôle ;
- les coefficients de dérivée logarithmique du côté arithmétique.

Les zéros ne participent pas à la construction. Ils ne sont chargés qu'après le scan, comme validation post hoc.

La base fixée avant tout examen des zéros est

\[
f_j(x)=\left(1-\frac{|x|}{w}\right)_+\cos(\xi_j x).
\]

Pour chaque fréquence centrale \(T\), on construit la matrice hermitienne réelle de compression \(M_F(T)\) et on observe son inertie.

## 2. Crash-test adversarial

Le couple principal est :

- **contrôle positif :** moyenne de la forme explicite de \(L(s,\chi_5)\) et de son conjugué, avec produit d'Euler ;
- **adversaire :** Davenport–Heilbronn [DH36b] [DH36a], de même type de complétion globale mais sans produit d'Euler.

Sur le scan \(0\le T\le200\), DUAL-LOCK trouve plusieurs intervalles négatifs pour Davenport–Heilbronn. Après seulement, on compare aux zéros hors droite calculés indépendamment.

Exemples :

| intervalle négatif DH | centre le plus négatif | \(\lambda_{\min}\) confirmé | zéro DH hors droite le plus proche |
|---|---:|---:|---:|
| 81–90 | 86 | -0.56097 | \(0.8085+85.6993i\) |
| 112–117 | 113 | -0.05336 | \(0.6508+114.1633i\) |
| 165–168 | 167 | -0.13292 | \(0.4256+166.4793i\) / symétrique |
| 174–179 | 176 | -0.01511 | \(0.7243+176.7025i\) |

Le contrôle \(L_{\chi_5}\) apparié reste positif aux mêmes fenêtres dans les confirmations précises.

**Interprétation autorisée :** la compression finie, construite sans les zéros, sait produire des témoins d'inertie qui discriminent le faux jumeau non eulérien.  
**Interprétation interdite :** ceci n'est pas une nouvelle preuve de Weil/RH ; c'est une réalisation finie et adversariale d'un mécanisme de signe déjà relié à la forme explicite.

## 3. Le Résidu sombre : décomposition exacte de la valeur finale

On décompose la compression

\[
M=M_{\infty}+M_q+M_{\mathrm{pole}}+M_{\mathrm{loc}},
\]

où les termes représentent respectivement archimédien, conducteur, pôle et contribution locale issue de la dérivée logarithmique.

Soit \(v_{\min}\) le vecteur propre de la plus petite valeur propre. On définit

\[
q_i=v_{\min}^{\!*}M_i v_{\min},\qquad
q_{\mathrm{tot}}=\lambda_{\min},
\]

et l'indice de cancellation

\[
\eta_{\mathrm{dark}}
=\frac{|q_{\mathrm{tot}}|}{\sum_i|q_i|},
\qquad
A_{\mathrm{dark}}=\eta_{\mathrm{dark}}^{-1}.
\]

Un petit \(\eta_{\mathrm{dark}}\) signifie que le signe final est un **résidu après cancellation de contributions beaucoup plus grandes**.

### Résultats DH

| T | archimédien | conducteur | local | total | \(\eta_{dark}\) | amplification |
|---:|---:|---:|---:|---:|---:|---:|
| 86 | +2.40898 | +0.29844 | -3.26839 | **-0.56097** | 0.0939 | 10.65× |
| 113 | +0.85520 | +0.09817 | -1.00673 | **-0.05336** | 0.0272 | 36.73× |
| 167 | +4.16895 | +0.43824 | -4.74011 | **-0.13292** | 0.0142 | 70.32× |
| 176 | +0.18880 | +0.01959 | -0.22350 | **-0.01511** | 0.0350 | 28.58× |

La fenêtre \(T=167\) est particulièrement claire : des contributions d'échelle totale \(\approx9.35\) laissent un résidu négatif de taille \(\approx0.133\). Le signe final est donc porté par environ **1,4 %** de l'échelle absolue des contributions projetées.

### Contrôle apparié

Aux mêmes fenêtres, le contrôle \(L_{\chi_5}\) reste positif. Son facteur d'amplification de cancellation est beaucoup plus faible sur trois des quatre témoins (environ 1.0–3.7× contre 10.7–70.3× pour DH).

Cela ne signifie pas que « forte cancellation = zéro hors droite » en général. Cela indique seulement que, dans les témoins d'inertie trouvés par DUAL-LOCK, le signe négatif de DH apparaît bien comme un résidu local/global et non comme un terme dominant isolé.

## 4. Test de stabilité numérique

Le premier témoin DH a été recalculé avec une base de dimension 5 en faisant varier le pas d'intégration archimédien :

\[
\Delta t\in\{0.04,0.03,0.02,0.01\}.
\]

La plus petite valeur propre reste

\[
\lambda_{\min}^{DH}\approx -0.388822647019
\]

sur toute la grille, tandis que le contrôle reste

\[
\lambda_{\min}^{L_{\chi_5}}\approx +0.001071810757.
\]

L'indice de cancellation DH reste \(\eta_{dark}\approx0.09623\). Les variations observées sont de l'ordre de l'arrondi numérique dans ce test.

La version de screening FFT et la recomputation par corrélations intégrées indépendamment donnent en outre le même signe ; les candidats négatifs du scan sont systématiquement raffinés avec la version précise.

## 5. Lien avec le « secteur sombre »

DARK-ZETA était une stratégie d'observabilité : chercher une information perdue par les observables grossiers. Le Résidu sombre fournit maintenant un mécanisme plus précis :

> **l'information de signe peut être portée non par une grosse composante cachée, mais par le petit reliquat d'une cancellation locale/globale.**

L'analogie avec la matière noire reste méthodologique. Ici, rien n'est une substance physique ; ce que l'on « infère » est une information structurelle de signe après soustraction de contributions dominantes.

Il existe un archétype classique de cette logique côté nombres premiers :

\[
\psi(x)-x,
\]

où \(\psi(x)\) est la fonction de Chebyshev. La formule explicite relie ce résidu aux zéros, et RH équivaut à la borne \(\psi(x)=x+O_\varepsilon(x^{1/2+\varepsilon})\). Ce n'est pas une découverte V6 ; c'est un rappel que « terme principal visible + petit résidu spectral » est déjà une structure classique de la théorie.

## 6. Rapport au calcul par éléments finis 2026

Le travail numérique 2026 sur l'opérateur de forme quadratique de Weil utilise une discrétisation P1 par éléments finis et une extrapolation de Richardson. Les auteurs indiquent explicitement que leur réalisation numérique ne prouve pas RH. Leur résultat est cependant pertinent pour V6 : les zéros apparaissent dans le terme d'erreur de la formule explicite du symbole premier, et l'injection d'un zéro hors ligne produit une croissance exponentielle du résidu.

> **Référence identifiée (V6.3c, lue sur résumé et pages) :** T. Kim et al. [Kim26], *A Numerical Realization of Suzuki [Suz26]'s Weil-Quadratic-Form Operator*, arXiv:2607.24830 (juillet 2026) — discrétisation P1 et extrapolation de Richardson de l'opérateur de M. Suzuki, *Weil's quadratic form via the screw function*, arXiv:2606.09096 (juin 2026). Les auteurs présentent leurs résultats comme des réalisations numériques d'identités classiques, sans arithmétique nouvelle ; leur point R6 (positivité de Weil [Wei52] sous forme d'opérateur, explosion avec un zéro hors droite injecté) est très proche de DUAL-LOCK. Voir aussi la réalisation spectrale des zéros de Connes–Consani–Moscovici (« Zeta spectral triples ») [CCM25] (arXiv:2511.22755) et Connes–van Suijlekom [CvS25] (arXiv:2511.23257).

Cela renforce le choix méthodologique suivant : **un petit résidu peut être le canal pertinent, mais précisément parce qu'il est petit il doit être audité plus sévèrement que les termes dominants.**

## 7. Verdict V6.3

### Ce qui survit

1. DUAL-LOCK distingue le contrôle eulérien apparié de Davenport–Heilbronn par l'inertie de compressions finies construites sans zéros.
2. Les fenêtres négatives DH coïncident post hoc avec plusieurs zéros hors droite connus du témoin.
3. Sur les témoins négatifs, la valeur de signe est bien un **résidu de cancellation** entre contributions archimédiennes/conducteur et locales.
4. Ce résidu est stable sous le premier sweep de discrétisation numérique.

### Ce qui n'est pas démontré

- aucune nouvelle implication vers RH ;
- aucune universalité de \(\eta_{dark}\) ;
- aucune preuve qu'une petite cancellation implique un zéro hors droite ;
- aucune justification pour traiter le résidu comme une « énergie » physique.

### Prochaine question

Ne plus chercher une « énergie cachée » mais une **loi de stabilité du résidu** :

\[
\boxed{
\text{quelles déformations des canaux local/global changent le signe du résidu, et lesquelles le laissent invariant ?}
}
\]

C'est un problème de robustesse/inertie beaucoup plus précis que la métaphore initiale.

---

## Erratum / mise à jour V6.3a

Le document `22_AUDIT_V6_3A_INSTRUMENT_DUAL_LOCK.md` remplace les interprétations quantitatives fondées sur les valeurs propres ordinaires. La base de fonctions test est fortement non orthogonale : les confirmations canoniques utilisent désormais le problème généralisé \(Mv=\lambda Gv\). Les anciens facteurs d'amplification sont rétrogradés et remplacés par les facteurs généralisés. Le second mode négatif précédemment signalé à \(T=176\) est retiré comme artefact numérique. Le signe négatif principal DH, lui, survit au nouvel audit.

<!-- references:debut -->

## Références

Format : [clé] auteurs, *titre*, publication, lien. Fiches complètes et état de vérification : document 42 (registre des sources).

- [CCM25] A. Connes, C. Consani, H. Moscovici. *Zeta spectral triples*. arXiv:2511.22755 (27 nov. 2025). <https://arxiv.org/abs/2511.22755> — vérifié en ligne. **Correctif V6.18 :** Le titre est « Zeta spectral triples » ; le résumé parle d'une réalisation spectrale des zéros, pas explicitement de formes de Weil tronquées.
- [CvS25] A. Connes, W. D. van Suijlekom. *Quadratic forms, real zeros and echoes of the spectral action*. arXiv:2511.23257 (28 nov. 2025). <https://arxiv.org/abs/2511.23257> — vérifié en ligne
- [DH36a] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series*. J. London Math. Soc. 11 (1936), no. 3, 181–185. <https://doi.org/10.1112/jlms/s1-11.3.181> — partiellement vérifié
- [DH36b] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series. II*. J. London Math. Soc. 11 (1936), no. 4, 307–312. <https://doi.org/10.1112/jlms/s1-11.4.307> — partiellement vérifié
- [Kim26] T. Kim, Y. Hong, M. Kim, S. Choi, J. Jang, M. Kim. *A numerical realization of Suzuki's Weil-quadratic-form operator*. arXiv:2607.24830 (juillet 2026). <https://arxiv.org/abs/2607.24830> — vérifié en ligne
- [Suz26] M. Suzuki. *Weil's quadratic form via the screw function*. arXiv:2606.09096 (juin 2026 ; v3 du 23 sept. 2026). <https://arxiv.org/abs/2606.09096> — vérifié en ligne
- [Wei52] A. Weil. *Sur les « formules explicites » de la théorie des nombres premiers*. Comm. Sém. Math. Univ. Lund, vol. suppl. dédié à M. Riesz (1952), 252–265. <https://en.wikipedia.org/wiki/Weil%27s_criterion> — partiellement vérifié

<!-- references:fin -->
