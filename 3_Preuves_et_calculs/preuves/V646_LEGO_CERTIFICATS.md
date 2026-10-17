---
title: "Un Lego réutilisable et un premier certificat complet"
subtitle: "Programme Riemann - V6.46 - Document 71"
author: "Vincent P. P. NOËL - dossier de recherche, rédaction assistée"
date: "12 octobre 2026"
---

# 1. Faisabilité : une construction exécutée

Un premier assemblage complet est réalisé. Il porte sur **tous les tests
admissibles** d'un espace de dimension infinie, avec le premier 2 réellement
présent. Ce résultat dépasse la vérification d'une compression matricielle.

**Théorème local certifié.** Pour tout \(0<S\le347/1000\), et tout \(f\in X_S\)
admissible dans le domaine de la forme de V644–V645,
\[
\boxed{Q_W(f)\ge\frac1{25}\|f\|_2^2,
\qquad Q_W(f)\ge\frac1{200}R(f),
\qquad\|f\|_2^2\le\frac3{20}R(f).}
\]
Ici \(R=\|f\|_2^2+\mathcal E(f)\). La preuve combine les lemmes K1–K6 ci-dessous
avec cinq inégalités rationnelles effectivement encadrées. La marge massique
plus précise du journal est supérieure à 0,0479 ; le théorème conserve des
constantes simples et prudentes. Il n'utilise ni zéros, ni RH, ni les anciennes
quadratures archimédiennes exploratoires.

La positivité est acquise sur une famille **bornée** de supports. Aucune
exhaustion vers l'infini n'est obtenue. Les réponses à S=0,348 et S=1/2 restent
indéterminées pour cet assemblage, sans témoin négatif de Q_W.

Le Lego est constitué de preuves analytiques, d'encadrements numériques et de
raccords typés. Il n'est pas un assistant de preuve formelle : les données d'une
brique arbitraire ne sont pas authentifiées par la seule présence d'un label.
Les constructeurs, les erreurs et les lemmes doivent être contrôlés ensemble.
La nouveauté annoncée est interne au programme ; aucune priorité dans la
littérature n'est revendiquée.

# 2. Les pièces et leurs raccords

| Pièce | Image pour apprendre | Garantie et raccord |
|---|---|---|
| Domaine | Une boîte de taille S | Support, moments, régularité, forme, norme R et unité |
| Moule P | Le moule fabrique une pièce admissible | Pψ respecte les deux moments ; origine V644 |
| Projection | Retirer ce que les balances ne lisent pas | Le même Gram sert aux sources et aux fréquences |
| Parité | Deux tiroirs qui ne se mélangent pas | Découplage exact pair/impair pour énergie et premiers |
| Couches | Plusieurs règles mesurent la même pièce | Une somme finie minore l'énergie sur tous les tests |
| Bord | Les attaches au bord coûtent de l'énergie | Le potentiel pénalise les bandes du couplage premier |
| Assembleur | Vérifier tous les raccords | Mélange convexe, marge, contrôle R et statut |
| Inclusion | Une petite boîte entre dans la grande | Tous S≤S₀ héritent de la preuve sur X_S₀ |

Les tests, les annihilateurs et les sources sont des objets distincts. Les tests
et sources portent l'unité fictive \(A_{\rm amp}\) ; les formes, potentiels
appliqués à une masse et Grams portent \(A_{\rm amp}^2\). S et les fréquences sont
logarithmiques sans dimension. Les constantes λ, μ, β et α sont sans dimension.

Un port contient S, la forme exacte et son éventuel décalage massique, les
annihilateurs, la norme et l'unité. Deux briques de supports, formes ou unités
différents ne se raccordent pas. Une vérification sur des échantillons ne porte
pas le statut « tous les tests ». Un certificat borné ne reçoit pas le statut
« tous les supports jusqu'à l'infini ».

# 3. Cadre commun et conventions

Sur \(I_S=[-S,S]\), prolonger f par zéro et imposer
\[
\int f(x)\cosh(x/2)dx=\int f(x)\sinh(x/2)dx=0.
\]
Ces deux conditions sont équivalentes aux moments exponentiels de V644.
Précisément, X_S est le sous-espace des fonctions L² portées par I_S,
ayant ces deux moments nuls et une énergie finie. R(f) est le carré de
la norme énergétique : \(\|f\|_R=\sqrt{R(f)}\). On utilise
\[
\mathcal E(f)=\int_0^\infty w(t)\|U_tf-f\|_2^2dt,
\quad w(t)=\frac{e^{-t/2}}{1-e^{-2t}},\quad
C_0=\log(8\pi)+\gamma_E+\frac\pi2.
\]
\[
Q_W(f)=\mathcal E(f)-C_0\|f\|_2^2
-2\sum_{p^m\le e^{2S}}\frac{\log p}{p^{m/2}}\Re h_f(m\log p).
\]
La Fourier est unitaire, avec exponentielle e⁻ⁱᵗˣ et facteur \((2\pi)^{-1/2}\).
Son multiplicateur énergétique est
\[
a(T)=\sum_{n\ge0}\frac{2T^2}{b_n(b_n^2+T^2)},\qquad b_n=2n+\tfrac12.
\]
Il est croissant, nul en 0. Chaque terme est positif. La représentation par
digamma, cohérente avec [NIS10], sert à une comparaison ponctuelle indépendante ;
la preuve numérique utilise la série positive et son reste.

Le cadre de Weil et les projections de coupure sont rapprochés de [CC21].
Le résultat de ce document est démontré directement dans nos conventions ;
la lecture bibliographique ne sert pas à supposer son signe.

# 4. K1 - Une projection ouvre deux portes

Soit W un sous-espace fini de L²(I), de base w_j et de Gram G strictement positif.
La projection \(\Pi_W\) possède deux usages.

**Sources.** Pour de vraies sources fortes \(k_i\in L^2(I)\), poser
\(K_{ij}=\langle k_i,k_j\rangle\), \(B_{ji}=\langle w_j,k_i\rangle\). Alors
\[
C_{\rm opt}=\operatorname{Gram}((I-\Pi_W)k_i)=K-B^*G^{-1}B.
\]
Pour toute correction \(p_i\in W\), l'orthogonalité donne
\[
\operatorname{Gram}(k_i-p_i)=C_{\rm opt}
+\operatorname{Gram}(\Pi_Wk_i-p_i)\succeq C_{\rm opt}.
\]
La projection améliore donc la matrice entière en ordre de Loewner, avec les
couplages, pas seulement ses diagonales. Pour l'usage Schur, W doit annihiler
la queue correspondante. Les intégrations, G et son inversion restent à
encadrer lorsque les sources sont numériques. Le programme implémente ici
l'algèbre rationnelle sur un exemple de Gram cohérent ; il ne prétend pas avoir
certifié toutes les sources de ζ.

**Fréquences.** Pour f∈W⊥, Cauchy–Schwarz donne
\[
|\widehat f(t)|^2\le\frac{\|f\|_2^2}{2\pi}
\|(I-\Pi_W)e^{itx}\|_2^2.
\]
Le même G⁻¹ retire donc aussi la part fréquentielle interdite. C'est le premier
coup double. La contraction de \(I-\Pi_W\) conserve les majorants d'erreur L²
des sources ; les erreurs de calcul de la projection doivent s'ajouter. □

# 5. K2 - La parité donne des traces plus fines

Prendre \(W=\operatorname{span}\{\cosh(x/2),\sinh(x/2)\}\).
La réflexion commute avec les déplacements symétrisés et l'énergie. Elle
préserve les moments ; f=f_pair+f_impair découple toutes les formes.
Les deux normes du Gram sont
\[
g_+=S+\sinh S,\qquad g_-=\sinh S-S>0.
\]
Poser
\[
z_S(t)=\frac{2\sinh((1/2+it)S)}{1/2+it},\quad
b_c(t)=\Re z_S(t),\quad b_s(t)=\Im z_S(t).
\]
Les diagonales projetées sont
\[
d_+(t)=S+\frac{\sin(2tS)}{2t}-\frac{b_c(t)^2}{g_+},
\]
\[
d_-(t)=S-\frac{\sin(2tS)}{2t}-\frac{b_s(t)^2}{g_-}.
\]
Les valeurs en 0 sont définies par continuité. Ces expressions sont les normes
carrées projetées de cos(tx) et sin(tx) ; elles sont non négatives.
Pour un test de la parité correspondante,
\[
\int_{-T}^T|\widehat f(t)|^2dt
\le\min(1,\kappa_\pm(T))\|f\|_2^2,
\quad \kappa_\pm(T)=\frac1\pi\int_0^T d_\pm(t)dt.
\]
La borne résulte de K1 puis de l'intégration. Séparer les parités remplace la
trace totale par deux traces plus petites et conserve le contrôle des termes
croisés qui doivent être nuls : deuxième coup double. □

# 6. K3 - Cumuler les couches, sans quadrature infinie

Pour \(0=T_0<T_1<\cdots<T_m\), la monotonie de a donne, point par point,
\[
a(t)\ge\sum_{j=1}^m[a(T_j)-a(T_{j-1})]\,\mathbf1_{|t|\ge T_j}.
\]
Plancherel et K2 donnent donc
\[
\mathcal E(f)\ge\lambda_\pm\|f\|_2^2,
\]
\[
\lambda_\pm=\sum_{j=1}^m
[a(T_j)-a(T_{j-1})]\,[1-\min(1,\kappa_\pm(T_j))].
\]
Le minimum des deux λ couvre tout f admissible, même complexe. La fréquence
au-delà du dernier seuil n'est pas supprimée : le dernier étage reste un
minorant sur toute cette queue. Aucun reste d'une quadrature énergétique
infinie n'est oublié. □

**Encadrement exécuté.** m=32, T_j=3j/8. Chaque intégrale de κ est calculée
par milieux avec h=3/(8·256). Si v=(I−Π)cos(tx) ou sin(tx),
\[
|\partial_t\|v\|^2|\le2\|v\|\|v'\|
\le\frac{4S^2}{\sqrt3}\le4S^2=:M.
\]
La contraction de la projection et \(\int_{-S}^Sx^2dx=2S^3/3\) justifient la borne.
L'erreur totale des milieux jusqu'à T vaut au plus MTh/4, puis on divise par π.
Ce terme d'erreur est ajouté au majorant κ, jamais retranché.

Pour chaque incrément, on somme les n<64 en fractions rationnelles avant les
transcendantes. Pour n≥64, l'incrément est
\[
\frac{2b_n(T_j^2-T_{j-1}^2)}
{(b_n^2+T_j^2)(b_n^2+T_{j-1}^2)}.
\]
Il décroît lorsque b_n≥T_j. La comparaison série/intégrale minore sa somme par
\[
\frac12\log\frac{b_{64}^2+T_j^2}{b_{64}^2+T_{j-1}^2}.
\]
Ajouter le premier terme du reste fournit un majorant. Tous les calculs
élémentaires utilisent des intervalles binaires à 160 bits. Les extrémités
orientées alimentent ensuite l'algèbre rationnelle exacte.

# 7. K4 - Le bord paie précisément les attaches premières

Définir
\[
J(d)=\int_d^\infty w(t)dt
=\frac12\log\frac{1+e^{-d/2}}{1-e^{-d/2}}+\arctan(e^{-d/2}),\quad d>0.
\]
Dans l'énergie des déplacements, les interactions avec l'extérieur de I donnent
\[
\mathcal E(f)\ge\int_I V_S(x)|f(x)|^2dx,
\quad V_S(x)=J(S-x)+J(S+x).
\]
**Preuve.** Séparer les paires de points tous deux dans I des paires dont un
point est hors I, où f vaut zéro. Le premier terme est une intégrale de
différences carrées non négative ; le second est exactement le potentiel
annoncé. Tonelli s'applique aux termes positifs, même pour le domaine de forme.
Le potentiel minimal vaut 2J(S), puisque J est convexe. □

Pour S₀=347/1000, a=log2 et δ=2S₀−a, on a
\[
0<\delta<S_0,\qquad a<2S_0<\log3<2a.
\]
Le seul terme premier est 2. Son couplage se produit entre les deux bandes
\([-S_0,S_0-a]\) et \([-S_0+a,S_0]\), de largeur δ.
Si M_bord est la masse totale dans ces bandes disjointes et w₂=log2/√2,
\[
Q_{\rm pr}(f)\le w_2M_{\rm bord}(f).
\]
Cela suit de \(2\Re(u\bar v)\le|u|^2+|v|^2\).
Sur les bandes, le potentiel est au moins J(δ)+J(a). Si v₀,v₁ sont deux
planchers certifiés, respectivement hors bandes et dans les bandes, alors
\[
\mathcal E(f)\ge v_0\|f\|^2+(v_1-v_0)M_{\rm bord}(f).
\]
La différence v₁−v₀ concerne les **planchers choisis** ; elle n'est pas présentée
comme une minoration de la différence des potentiels exacts.
Le confinement qui crée le couplage premier crée également son coût
énergétique : troisième coup double. □

# 8. K5 - L'assembleur fournit une marge lisible

Avec \(\mathcal E\ge\lambda\|f\|^2\), prendre α∈[0,1] tel que
\(\alpha(v_1-v_0)\ge w_2\). Un mélange des deux minorations de la même énergie donne
\[
Q_W(f)\ge[(1-\alpha)\lambda+\alpha v_0-C_0]\|f\|^2.
\]
Le programme choisit α=w₂_upper/(v₁_lower−v₀_lower) quand ce nombre est ≤1.
Si la marge n'est pas positive, la réponse est **indéterminée** : la forme exacte
peut encore être positive. Une norme première indépendante maximale échoue
ici ; le mélange garde la relation entre coût énergétique et attaches.

Le journal prouve les cinq inégalités rationnelles simples
\[
\lambda\ge\frac{231}{40},\quad v_0\ge\frac{769}{200},
\quad v_1\ge\frac{1627}{250},
\]
\[
C_0\le\frac{5373}{1000},\qquad w_2\le\frac{491}{1000}.
\]
Prendre α=3/16. Son paiement de bord dépasse w₂_upper. L'algèbre exacte donne
\[
c=(1-\alpha)\frac{231}{40}+\alpha\frac{769}{200}
-\frac{5373}{1000}=\frac{321}{8000}>\frac1{25}.
\]
Cette preuve de signe tient dans cinq encadrements et une égalité rationnelle.
Le contrôle d'erreur des couches garantit la première inégalité ; les quatre
autres utilisent les fonctions élémentaires de K4 et l'encadrement de γ_E. □

# 9. K6 - Deuxième usage : contrat R et couverture bornée

Poser m=||f||² et L=C₀_upper+w₂_upper. On a simultanément
\(Q_W\ge c m\) et \(Q_W\ge\mathcal E-Lm\).
Leur mélange, avec poids \(c/(c+L+1)\) sur la seconde, donne
\[
Q_W\ge\frac{c}{c+L+1}(\mathcal E+m)=\mu R.
\]
De \(\mathcal E\ge\lambda m\), on obtient \(m\le R/(1+\lambda)=\beta R\).
Les constantes rationnelles de K5 impliquent μ>1/200 et β<3/20. Le même
assemblage fournit donc signe et contrats directement utilisables dans Schur.
La tête peut être nulle : tout X_S₀ possède déjà une marge coercive. □

Pour S≤S₀, l'extension par zéro identifie X_S à un sous-espace de X_S₀ : support,
moments, R et Q_W globaux restent les mêmes. Toutes les inégalités s'y
restreignent. Aucun test de monotonie numérique des algorithmes λ(S) n'est
nécessaire. Cette preuve couvre une infinité de supports, mais seulement dans
un intervalle borné. L'agrandissement au-delà de S₀ ajoute de nouvelles directions.

# 10. K7 - Contrôle négatif et garde contre les faux raccords

Le contrôle négatif modifie volontairement la forme : Q_η=Q_W−η||f||².
Pour la graine polynomiale f=P(1−x²/S₀²)⁴, les masses sont rationnelles et
\[
Q_W(f)\le\frac{131}{8}\|f'\|^2-\frac{25}{6}\|f\|^2
+w_{2,\rm upper}\|f\|^2.
\]
Choisir un entier η strictement supérieur à ce quotient majoré produit un
vrai témoin négatif encadré de Q_η. L'assembleur ne certifie pas cette forme.
Cela teste sa sensibilité à une perturbation, sans constituer un contre-exemple
à RH. Le port distingue Q_W de Q_η et porte la valeur exacte de η. □

Le code refuse supports ou unités incompatibles, formes non prises en charge,
décalages massiques incohérents, erreurs de rôle et couverture par seuls
échantillons. L'algèbre de projection refuse un Gram singulier ou un Gram joint
incompatible. L'inversion presque singulière reste une difficulté réelle pour
des bases polynomiales/exponentielles plus grandes.

# 11. Exécution et portée des résultats

{{RESULT_TABLE}}

Les supports et le maillage ont été sélectionnés après exploration constructive
et critique. Le protocole a été figé avant ces évaluations par intervalles ;
aucune découverte du signe n'est présentée comme une prévision indépendante.
Le journal sauvegarde les bornes binaires des couches, leur erreur de milieux,
les incréments positifs et les marges rationnelles. Les deux lectures ont
recoupé les facteurs et les domaines. Une quadrature ponctuelle indépendante
confirme les orientations, mais elle n'est pas la source du certificat.

Une brique plus élémentaire, par disjonction des supports des translations,
donne déjà un certificat complet pour S≤1/32 sans premier. Le résultat S₀
franchit log2/2 et rencontre effectivement le premier 2. Il reste très local.

{{FIGURE}}

# 12. Quatre portes creusées : diagnostic d'un opérateur conjoint

Le premier2 peut aussi être conservé directement en Fourier, sans séparer
son poids de sa phase. Avec la Fourier unitaire et un seul premier,
\[
Q_W(f)=\int_{\mathbb R}[b(\tau)-C_0-2w_2]|\widehat f(\tau)|^2d\tau,
\]
\[
b(\tau)=a(\tau)+2w_2[1-\cos(\tau\log2)].
\]
La traduction est exacte. L'enveloppe croissante
\(g(T)=\inf_{\tau\ge T}b(\tau)\) donne un minorant, mais peut perdre beaucoup
des oscillations en créant des plateaux. Une grille ponctuelle ne certifie pas
cet infimum. Des planchers peuvent former une fonction en escalier minorante,
à condition de les monotoniser ; leurs différences ne sont pas supposées être
des minorants des incréments exacts de g.

Une seconde voie conserve les sous-niveaux \(\Omega_u=\{\tau:b(\tau)<u\}\),
qui sont des unions de bandes. La même projection de K2 donne
\[
\kappa_{\pm,b}(u)=\frac1\pi\int_{\tau>0,\ b(\tau)<u}d_\pm(\tau)d\tau.
\]
L'intégration des couches en valeur u, plutôt qu'en fréquence T, fournit
une cible de minoration énergétique par \(\int_0^\infty[1-\min(1,\kappa_{\pm,b}(u))]du\).
Elle garde davantage de la phase du premier et réutilise le Gram déjà construit.

Le script de diagnostic a été réellement exécuté à 40 000 puis 80 000 points,
jusqu'à la fréquence100. Il utilise des évaluations ponctuelles et des intégrales
discrètes : **aucune de ces nouvelles marges n'est certifiée**.

{{DIAGNOSTIC_TABLE}}

À S=1/2, les sous-niveaux améliorent nettement le budget exploratoire, mais
celui-ci reste négatif. Cela indique une insuffisance de ce minorant, pas un
témoin négatif de Q_W. L'accord des deux résolutions mesure une stabilité,
pas une erreur prouvée. Une certification demanderait les frontières des
sous-niveaux, les intégrales et la queue ; b≥a pourrait exclure celle-ci.

La concentration peut encore être affinée par
\(\|K\|\le\min(\operatorname{tr}K,\sqrt{\operatorname{tr}K^2})\)
pour l'opérateur positif projeté. Ce raccord réutiliserait encore le Gram,
mais sa double intégrale n'a pas été exécutée dans ce diagnostic reproductible.

# 13. Les prochaines constructions : conserver les coups doubles

| Porte | Acquis dans cette étape | Travail restant |
|---|---|---|
| Sources et fréquences | Même projection, réduction Loewner et concentration | Sources fortes et erreurs L² réelles pour les têtes non coercives |
| Énergie et premiers | Coût de bord paie le premier 2 sur S≤0,347 | Estimation jointe plus fine quand les bandes s'élargissent ou se recouvrent |
| Queue et tête | Contrat R sur tout X_S₀, tête nulle | Représentation praticable pour des supports plus grands |
| Couverture | Tous les supports d'une famille bornée | Loi de transport ou autre mécanisme atteignant S_n→∞ |
| Convergence | Domaines et gardes explicites | Norme de graphe si une approximation de sources/opérateurs la requiert |

La priorité est d'affiner **l'opérateur conjoint énergie moins déplacements
premiers**, plutôt que d'augmenter une tête brute. Des concentrations par
opérateur, au lieu de la seule trace, et des potentiels par cellules pourraient
conserver davantage de relations utiles. Les projections devront améliorer
simultanément les contrôles fréquentiels et les résidus de sources.

La première brique complète existe maintenant. La règle d'agrandissement reste
le verrou : réussir un support plus grand par le même mécanisme, puis démontrer
ce qui se transporte sur une famille non bornée. RH, les collisions historiques
et les paramètres complexes des autres familles restent ouverts dans leur portée.
