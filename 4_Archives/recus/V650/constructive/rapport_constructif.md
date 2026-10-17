# Reconstruction nouvelle après V6.49 : poids intégrés, queue précise et plafond matriciel

Ce dossier a été produit pendant la reprise du 13 octobre 2026. Il reconstitue et améliore une voie à partir des sources V6.49 conservées. Il ne constitue pas la récupération d'un fichier V6.50 original disparu.

## Ce que le calcul établit et ce qu'il ne termine pas

La cible est le minorant borné de la forme de Weil sur le support $[-11/20,11/20]$, avec les deux moments exponentiels nuls, $U=10$ et $T=700$. La positivité de la forme complète sur cet espace demeure **non certifiée dans cette reconstruction**. La preuve locale existante dans V6.48 couvre $S\le1/2$.

Trois nouveaux éléments réutilisables sont construits : une borne de quadrature opératoire d'ordre $h^2$ qui traverse les cassures de la partie positive, un encadrement précis de la queue du multiplicateur archimédien, et un plafond prouvé pour les matrices dyadiques calculées. Une matrice calculée ne devient pas automatiquement l'opérateur continu : il faut aussi encadrer les nœuds, poids, ondes, Gram et erreurs de construction.

Les valeurs numériques du premier passage sont conservées dans `resultats_reconstruction.json`. Le script `reconstruction.py --diagnostic` les régénère. L'exécution de référence a duré environ 12 secondes.

## 1. Le reste de Lagrange est la première rupture de contrat

Pour les racines du Legendre $P_N$ mises à l'échelle du support, son coefficient dominant vaut exactement

$$L_N=\frac{(2N)!}{2^N(N!)^2}.$$

Le reste ponctuel de l'onde jusqu'à $T$ est au plus

$$e_N=\frac{(TS)^N}{N!L_N}.$$

Le programme évalue ce rationnel exactement, puis imprime un arrondi descriptif. À $S=11/20$, $T=700$ :

| Degré $N$ | Reste ponctuel $e_N$ | Conséquence |
|---|---:|---|
| 512 | $49046.812508\ldots$ | Cette borne ne justifie aucune bonne interpolation |
| 640 | $7.55906370499\ldots\times10^{-57}$ | Cette borne rend le reste négligeable |

Les valeurs propres stables de V6.49 à $N=512$ demeurent un diagnostic flottant ; la borne utilisée à $N=80,T=90$ ne s'y transpose pas sans vérifier ses nouvelles constantes.

Pour l'onde projetée $r_t=P_W\cos(tx)$ ou $P_W\sin(tx)$, le Gram est $\operatorname{diag}(S+\sinh S,\sinh S-S)$. La contraction de la projection donne

$$\|r_t-I_Nr_t\|_2\le\sqrt{2S}\frac{(TS)^N+\sqrt{2S/(\sinh S-S)}e^{S/2}(S/2)^N}{N!L_N}.$$

À $N=640$, la valeur descriptive est environ $7.93\times10^{-57}$. Le terme exponentiel ajouté est encore beaucoup plus petit.

## 2. Une quadrature qui intègre la cassure au lieu de l'ignorer

Posons $\phi_H(t)=(U-b_H(t))_+$, où $b_H$ est l'interpolant affine d'une table, et

$$K(t)=|r_t\rangle\langle r_t|.$$

Sur la cellule centrée en $m_i$, de largeur $h$, employons le **poids intégré**

$$w_i=\int_{m_i-h/2}^{m_i+h/2}\phi_H(t)\,dt$$

et l'opérateur discret $\pi^{-1}\sum_iw_iK(m_i)$. Le poids affine positif s'intègre exactement, y compris lorsque son signe change dans la cellule. Si ses valeurs aux deux extrémités sont $g_0,g_1$, son intégrale positive vaut :

* $h(g_0+g_1)/2$ si les deux sont positifs ;
* $0$ si les deux sont négatifs ou nuls ;
* $h g_0^2/[2(g_0-g_1)]$ si $g_0>0\ge g_1$ ;
* $h g_1^2/[2(g_1-g_0)]$ si $g_1>0\ge g_0$.

**Lemme.** Si $0\le\phi_H\le U$, si sa constante de Lipschitz est au plus $L$, et si $\|K'\|\le M_1$, $\|K''\|\le M_2$, alors

$$\left\|\frac1\pi\int_0^T\phi_H(t)K(t)dt-\frac1\pi\sum_iw_iK(m_i)\right\|\le\frac{Th^2}{\pi}\left(\frac{LM_1}{12}+\frac{UM_2}{24}\right).$$

**Preuve.** Écrire $u=t-m_i$ et $K(t)=K(m_i)+uK'(m_i)+E_i(t)$ avec $\|E_i(t)\|\le M_2u^2/2$. Le terme constant est payé exactement par $w_i$. Puisque $\int u\,du=0$,

$$\left|\int\phi_H(t)u\,dt\right|=\left|\int[\phi_H(t)-\phi_H(m_i)]u\,dt\right|\le Lh^3/12.$$

Le terme de reste est au plus $UM_2h^3/24$. Additionner les $T/h$ cellules et diviser par $\pi$. La preuve n'exige pas de dérivée de la partie positive au point où elle se casse.

Par contraction de $P_W$,

$$\|r_t\|\le\sqrt{2S},\quad \|r_t'\|\le\sqrt{2S^3/3},\quad \|r_t''\|\le\sqrt{2S^5/5}.$$

La règle du produit de rang un fournit

$$M_1\le4S^2/\sqrt3,\qquad M_2\le4S^3(1/\sqrt5+1/3).$$

Pour les premiers 2 et 3 actifs à $S=11/20$, $|b'|<8$ et $|b''|<35$. En effet, si $b_n=2n+1/2$,

$$\sup|a'|\le\frac{21}{16}\sum_nb_n^{-2}\le\frac{21}{16}\frac{109}{25},\qquad \sup|a''|\le4\sum_nb_n^{-3}\le\frac{4052}{125}=32.416.$$

Les queues de ces séries sont bornées par leur premier terme plus l'intégrale décroissante. Les phases ajoutent respectivement $2\sum_{p=2,3}(\log p)^2/\sqrt p$ et $2\sum_{p=2,3}(\log p)^3/\sqrt p$. Les bornes rationnelles $\log2<0.694$, $\log3<1.099$, $\sqrt2>1.414$, $\sqrt3>1.732$ vérifient les budgets 8 et 35.

Pour une table centrale de rayon d'erreur $r_{\rm tab}$, l'erreur continue de poids est

$$\delta_{\rm table}\le r_{\rm tab}+35H^2/8,$$

sans facteur $T/\pi$, par Plancherel. La pente de son interpolant est bornée par $8+2r_{\rm tab}/H$. Cette correction est incluse dans la version finale du script.

Avec $H=1/200$ et $h=1/1000$, le budget table plus quadrature vaut environ **$0.00026155$**, inférieur à la marge exploratoire V6.49 d'environ $0.00058303$. Cette comparaison indique que l'ancienne dette d'ordre $h$ n'est plus un obstacle de principe ; elle ne paie pas encore les autres erreurs.

## 3. La queue archimédienne gagne plusieurs ordres de grandeur

Pour $f_t(b)=2t^2/[b(b^2+t^2)]$, posons $B=2K+1/2$ et

$$A_K(t)=\sum_{n<K}f_t(2n+1/2)+\frac12\log(1+t^2/B^2)+\frac12f_t(B)-\frac16f_t'(B).$$

**Lemme.** Pour tout $t\ge0$,

$$A_K(t)-\frac4{15B^4}\le a(t)\le A_K(t).$$

**Preuve.** L'identité

$$f_t(b)=\int_0^\infty2(1-\cos(tu))e^{-bu}\,du$$

donne une densité positive. La queue discrète multiplie cette densité par $[1-e^{-2u}]^{-1}=(1+\coth u)/2$. Pour tout $u>0$,

$$\frac1u+\frac u3-\frac{u^3}{45}\le\coth u\le\frac1u+\frac u3.$$

On peut vérifier ces deux inégalités en multipliant par $u\sinh u$ et en développant $\sinh$ et $\cosh$ : les coefficients de la différence ont tous le signe requis. L'intégration des trois premiers termes donne l'intégrale de queue, $f_t(B)/2$ et $-f_t'(B)/6$. Le dernier terme donne une différence au plus

$$\frac1{90}\int_0^\infty2(1-\cos(tu))u^3e^{-Bu}du\le\frac{24}{90B^4}=\frac4{15B^4}.$$

À $K=256$, la largeur analytique est exactement $64/16557193359375$, environ $3.87\times10^{-12}$. L'ancienne comparaison série/intégrale seule a une largeur de l'ordre de $10^{-3}$ à $t=700$.

Le programme vectoriel évalue cette expression avec des primitives binaire64 arrondies vers l'extérieur, des développements de Taylor et des restes explicitement bornés. Pour 140001 points, le rayon maximal de la **table entière b** est d'environ $5.76\times10^{-9}$ ; les doublements d'angle dominent ce rayon.

Il obtient un encadrement de $a(700)$ contenu dans $[10.0853866028235,10.0853866028283]$. Puisque $a$ croît et $b\ge a$, la queue au-delà de $700$ est globalement exclue pour $U=10$. C'est une garde analytique globale en fréquence, pas une lecture du dernier point d'une grille.

## 4. La matrice finie est contrôlée sans 320 grands déterminants

La matrice calculée est symétrisée et considérée comme une matrice **dyadique exacte** $M$. Un calcul de valeur propre propose $\tau$ ; il ne prouve pas le plafond. Une Cholesky flottante propose un changement de coordonnées $C$, triangulaire, également considéré comme une matrice dyadique exacte.

Le programme encadre ensuite $C(\tau I-M)C^T$ par des produits scalaires explicites, dont chaque multiplication et addition est arrondie vers l'extérieur. Il vérifie la positivité du minorant de Gershgorin. Comme $C$ est triangulaire à diagonales non nulles, il est inversible exactement. La congruence prouve alors $\tau I-M\succ0$.

| Parité | Valeur propre flottante | Plafond rationnel certifié sur $M$ | Minorant après congruence |
|---|---:|---:|---:|
| paire | $2.3784071057\ldots$ | $19951609/8388608$ | $>0.99999999$ |
| impaire | $2.3511406106\ldots$ | $19722881/8388608$ | $>0.99999999$ |

La méthode est réutilisable pour toute matrice symétrique exacte. La preuve ne suppose aucune précision du solveur de valeurs propres ou de sa Cholesky : si ses propositions sont mauvaises, la validation de congruence échoue.

Pour le seuil scalaire $C_S$, la borne élémentaire d'Euler à $n=1024$ a une largeur $1/n$, trop grande pour cette petite marge. Le même sandwich de $\coth$ donne un encadrement plus précis :

$$H_n-\log n-\frac1{2n}+\frac1{12n^2}-\frac1{120n^4}\le\gamma_E\le H_n-\log n-\frac1{2n}+\frac1{12n^2}.$$

La preuve utilise $H_n-\log n-\gamma_E=\int_0^\infty e^{-nx}[1/x-1/(e^x-1)]dx$. Cette identité se vérifie par différence entre $n$ et $n+1$, puis par la limite à l'infini. Le noyau est encadré par $1/2-x/12$ et $1/2-x/12+x^3/720$. L'intégration donne les termes affichés et une largeur $1/(120n^4)$, environ $7.58\times10^{-15}$ à $n=1024$.

**Limite explicite.** Les deux matrices de `matrices_exploratoires.npz` ont été assemblées avec des nœuds de Gauss, trigonométries, Gram et poids intégrés évalués en flottant. Le plafond sur leur contenu exact est prouvé dans le modèle IEEE déclaré. Leur distance à l'opérateur continu doit encore être certifiée ; le statut global du calcul reste donc exploratoire.

## 5. Ce qui doit être fini pour fermer la preuve locale

Il faut certifier les 640 nœuds et leurs poids, les ondes projetées et le Gram continu ; évaluer les poids de cellules vers l'extérieur ; comptabiliser l'assemblage matriciel et sa symétrisation ; puis vérifier l'inégalité complète $U-C_S-\tau-\delta>0$.

Après le plafond matriciel et les deux budgets nouveaux, la réserve descriptive paire est d'environ $0.00031156$. Cette réserve est disponible pour les composantes manquantes. Tant que leur somme n'est pas encadrée, elle ne constitue pas une marge certifiée.

## 6. Sens de la reconstruction pour RH

Le but mathématique reste la positivité de la forme de Weil sur une classe de tests suffisante. Les lemmes ci-dessus réparent des traductions entre une expression exacte, une approximation d'opérateur et une vérification finie. Ils ont un usage précis : une même procédure fournit les poids aux cassures et leur dette, et une même congruence valide la tête finie à coût raisonnable.

La positivité sur un support borné seul ne prouve pas RH. Il faut une famille de supports couvrant arbitrairement loin, ou un mécanisme global de transport dont les coûts sont maîtrisés sans circularité. Une éventuelle preuve complète à $S=11/20$ testerait la méthode et fournirait une brique locale. Sa contribution au but RH dépend de sa capacité à alimenter ce pont global ; elle ne vaut pas à elle seule une avance décisive sur RH.

## Reproductibilité

Exemple dans l'environnement de reprise :

```bash
PYTHONPATH=/workspace/scratch/72030dde7ad1/v635_runtime_deps OPENBLAS_NUM_THREADS=1 python reconstruction.py --diagnostic
```

Le script exige NumPy, SciPy et mpmath. Il suppose des opérations élémentaires IEEE binaire64 correctement arrondies ; cette hypothèse arithmétique doit être déclarée dans tout emploi du mot « certifié ».
