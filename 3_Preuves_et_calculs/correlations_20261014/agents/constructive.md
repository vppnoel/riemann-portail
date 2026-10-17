# Audit constructif — corrélations, empreinte et réduction

Date : 14 octobre 2026. Résultats ci-dessous : lemmes auxiliaires et reformulations ; aucune borne globale nouvelle n'est démontrée.

## 1. Pont prioritaire : énergie positive et corrélations ancrées

Posons E(x)=ψ(x)−x et J(X)=∫₁ˣ E(x)² dx. Pour toute séquence a(n) localement finie et sa somme A(x)=Σ_{n≤x}a(n), l'identité exacte suivante est valable, sans approximation :

J_a(X)=Σ_{m,n≤X}a(m)a(n)(X−max(m,n))−Σ_{n≤X}a(n)(X²−n²)+(X³−1)/3.

Preuve : développer (A(x)−x)² puis intégrer chacun des indicateurs 1_{m≤x}1_{n≤x}. Le noyau X−max(m,n) est ancré à la position absolue des indices. Il conserve le début, le bord et l'ordre de cumul ; ce n'est pas une autocorrélation invariante par translation.

Pour a=Λ, le premier terme vaut exactement :

Σ_n Λ(n)²(X−n)+2Σ_{h≥1}Σ_{n≤X−h}Λ(n)Λ(n+h)(X−n−h).

On peut donc chercher une compensation pondérée entre le carré de chaque poids et les corrélations de deux poids, tout en conservant l'ancrage qui disparaît dans beaucoup de statistiques moyennées.

### Critère de croissance (classique ; pas une découverte)

RH équivaut à J(X)=O(X²). Le sens RH⇒J=O(X²) est le résultat classique de Cramér, à partir de la borne dyadique ∫_X^{2X}E²≪X². Le sens inverse se prouve avec Mellin et Cauchy–Schwarz.

Une version plus facile à vérifier par une preuve entièrement élémentaire du passage analytique est : RH équivaut à J(X)=O_ε(X^{2+ε}) pour tout ε>0. Si σ>1/2, choisir 0<ε<2σ−1. Sur chaque dyade [Y,2Y],

∫_Y^{2Y}|E(x)|x^{−σ−1}dx ≪ Y^{1/2−σ+ε/2}.

La série dyadique converge. L'intégrale F(s)=∫₁∞E(x)x^{−s−1}dx est donc absolument convergente et holomorphe dans Re(s)>1/2. Dans Re(s)>1 on a

−ζ′(s)/ζ(s)=s/(s−1)+sF(s).

Le prolongement interdit toute singularité du logarithme dérivé dans Re(s)>1/2, sauf le pôle de ζ à 1. Donc ζ est sans zéro dans ce demi-plan, et la symétrie fonctionnelle donne RH. RH⇒version faible suit déjà de E(x)=O(√x log²x).

Cette réduction ne donne encore aucune borne arithmétique indépendante. Elle transforme toutefois l'obligation de signe en une question de croissance d'une énergie positive et fournit un détecteur qui ne perd pas un zéro exceptionnel.

### Pourquoi une moyenne peut détecter une exception

Un mode isolé x^β cos(γ log x), β>1/2 et γ≠0, a une énergie d'ordre X^{2β+1}. En effet, avec a=2β+1,

∫₁ˣ x^{2β}cos²(γ log x)dx = Xᵃ/(2a)+(1/2)Re[X^{a+2iγ}/(a+2iγ)]+constante.

Le coefficient oscillant est dominé strictement par 1/(2√(a²+4γ²))<1/(2a). Un tel mode dépasse donc X² malgré sa rareté spectrale. Ceci est un exemple de mécanisme, pas une preuve que tous les autres modes de ζ n'interfèrent pas : la preuve générale par Mellin traite précisément cette difficulté.

## 2. Empreinte arithmétique exacte

La seule positivité des poids et leur support sur les puissances premières ne caractérisent pas Λ. L'identité de divisibilité

Σ_{d|n}Λ(d)=log n

la caractérise exactement et sans RH. Dans l'algèbre de Dirichlet, 1*Λ=log et Λ=μ*log. Preuve de rigidité : si 1*a=log, alors μ*(1*a)=a=μ*log=Λ. Par induction, le premier coefficient faux fait échouer l'identité au même entier.

Cette empreinte doit être couplée au profil archimédien de ζ et à l'ancrage analytique. Elle exclut des contre-modèles génériques ; elle ne prouve pas le bon signe.

### Réponse exacte à un défaut d'empreinte

Pour a=Λ+e, posons r=1*e, autrement dit r(n)=Σ_{d|n}a(d)−log n. Alors e=μ*r. Pour le potentiel arithmétique P_a(t)=Σ_{n≤eᵗ}a(n)n^{−1/2}(t−log n), l'erreur se traduit exactement par

P_a(t)−P_Λ(t)=Σ_{m≤eᵗ}r(m)m^{−1/2}K_μ(t−log m),

K_μ(v)=Σ_{d≤eᵛ}μ(d)d^{−1/2}(v−log d), v≥0.

Preuve : substituer e=μ*r et écrire n=dm ; toutes les sommes sont finies à t fixé. Le noyau de Möbius est signé. Cette formule rend visible la frontière : caractériser les vrais coefficients est facile ; maîtriser globalement l'inversion de leurs défauts au poids critique n'est pas acquis.

## 3. Bispectre : pont secondaire d'identification, pas de positivité

Sur Z/NZ, pour une suite f dont tous les coefficients de Fourier F_k sont non nuls, le bispectre B_f(k,l)=F_kF_l conj(F_{k+l}) détermine f à une translation cyclique près. Preuve : si B_g=B_f, les rapports r_k=G_k/F_k ont module 1 (prendre l=0), et r_{k+l}=r_kr_l. Ce sont les caractères de Z/NZ, donc une translation. Un ancrage enlève cette ambiguïté.

Attention : les coefficients de Fourier de nos fluctuations réelles peuvent s'annuler ; la condition doit être vérifiée, pas supposée. Même une reconstruction exacte ne donne aucune loi de signe. L'intérêt est de diagnostiquer la phase perdue par l'ordre deux ; la cible RH plus utile reste la corrélation ancrée de l'énergie J.

## 4. Sources primaires vérifiées

- Brent, Platt, Trudgian, *The mean square of the error term in the prime number theorem*, J. Number Theory 238 (2022), 740–762 : https://maths-people.anu.edu.au/~brent/pd/rpb274-final.pdf. P. 1 : borne dyadique O(X²) sous RH, attribution Cramér. P. 2 : si RH est fausse le ratio est non borné. Th. 2 : ce ratio n'a pas de limite. Leur borne explicite 0,8603 est conditionnelle à RH, donc inutilisable comme entrée indépendante.
- Bendory, Boumal, Ma, Zhao, Singer, *Bispectrum Inversion with Application to Multireference Alignment* (2017), https://arxiv.org/html/1705.00641v2. Section II et propositions II.1–II.2 : information de phase et reconstruction sous conditions de nonannulation, à translation près.
- Tao, notes originales de cours *Elementary multiplicative number theory* (2014), https://terrytao.wordpress.com/2014/11/23/254a-notes-1-elementary-multiplicative-number-theory/. Identités de Λ, inversion de Möbius, convolution et Dirichlet.
- Matomäki, Radziwiłł, Tao, *Correlations of the von Mangoldt and higher divisor functions I. Long shift ranges*, https://arxiv.org/abs/1707.01315. Des estimations existent pour presque tous les décalages dans certaines plages ; elles ne sont pas automatiquement des bornes de notre énergie ancrée à toutes les échelles.
- Goldston, Lee, Schettler, Suriajaya, *Pair Correlation Conjecture … I: Simple and Critical Zeros* (2025), https://arxiv.org/abs/2503.15449. Leur implication de PCC sans supposer RH donne asymptotiquement 100 % des zéros sur la ligne et simples, pas tous les zéros. C'est une limite utile des seuls résultats de densité, sans rejeter l'utilité des moyennes.

## Choix conseillé

Priorité à l'énergie positive ancrée, en gardant l'identité de divisibilité comme contrat d'identité des coefficients. Prochain test utile : décomposer J en diagonal, hors-diagonal et terme déterministe ; repérer exactement le résidu qu'une identité multiplicative contrôle ou laisse incontrôlé. Aucune prétendue borne globale O(X²) ne doit être importée d'un travail qui suppose RH.
