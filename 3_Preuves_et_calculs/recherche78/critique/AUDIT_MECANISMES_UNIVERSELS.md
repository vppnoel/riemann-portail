# Quels mécanismes peuvent réellement imposer le signe global de Weil ?

Approche analytique et réfutative, 13 octobre 2026. Corpus de référence : V6.51, documents70 et76. Les constructions nouvelles sont des propositions vérifiables ; aucune positivité globale ni preuve de RH n'est annoncée.

## 1. Le degré de structure nécessaire

Un mécanisme universel doit forcer le signe de **toutes les combinaisons complexes**, avec leurs couplages, sur une famille non bornée de supports. Quatre formes de mécanisme pourraient réellement y parvenir :

1. une identité en carrés de normes, construite indépendamment du signe recherché ;
2. une contraction ou un système passif dont l'identité d'énergie restitue exactement les termes archimédiens, premiers et polaires ;
3. une positivité conditionnelle sur l'idéal polaire, avec des compensateurs identifiés et une loi compatible entre supports ;
4. un signe scalaire qui, grâce à une rigidité analytique propre àζ, entraîne toutes les positivités matricielles.

Le quatrième mécanisme est le pont extérieur le plus précis trouvé pendant cette passe. Les trois premiers sont des architectures capables de fournir le signe, mais l'identification arithmétique reste à construire.

## 2. Ce qui ne force aucun signe

| Indice favorable | Contre-exemple ou objection exacte | Structure manquante |
|---|---|---|
| Symétrie, parité et translations | −‖f‖² possède toutes ces symétries | Une propriété d'ordre, pas seulement une invariance |
| Moyenne ou trace positive | diag(10,−1) a trace9 mais une direction négative | Contrôle de tous les Rayleigh/couplages |
| FacteurEuler L² positif | B_p=E_p*E_p≥0, mais cela ne signifie pas Q_W(B_pψ)≥0 | Factorisation de la **forme**, pas du constructeur |
| Unitarité d'une phase | u(z)=1/z a module1 sur le cercle ; sa diagonale de noyau Schur en z=1/2 est −4 | Analyticité contractive dans le bon domaine |
| Quasi-inner/compactité | Pour u(z)=1/z le défaut Hardy est de rang1, mais u n'est pas inner | Signe exact du défaut compact |
| Nombre fixé de petits Grams positifs | Avec diagonale1 et hors-diagonale −1/m, toutes les tailles≤m+1 sontPSD, la taillem+2 est indéfinie | Une loi de taille arbitraire |
| Schur positif d'un préfixe | La dette suivante reste k(0)−v*T†v, avec condition de portée | Une inégalité de dette universelle |
| Phases premières seules | Leur coût simultané peut revenir arbitrairement près de0 | Archimédien et annulations arithmétiques liés |
| g(t)≤0 pour une fonction générale | g=−t⁴ donne aux points1,−1 le noyau [[2,−14],[−14,2]], valeurpropre−12 | Rigidité propre à la fonction spéciale |

Les no-go du document76 restent applicables : une liste fixe de premiers ne couvre pas tous les supports ; l'enveloppe de sortie D/V diverge ; le modèle continu B₀ ne porte pas le signe seul. Le signe arithmétique doit être conservé dans la construction.

## 3. Un vrai pont de loi scalaire vers tous les couplages

### 3.1. Source primaire et mécanisme

Suzuki, *Aspects of the screw function corresponding to the Riemann zeta-function*, JLMS 108 (2023), théorème 1.7 et preuve §7.2, démontre RH équivalente à Ψ(t)≥0 pour tout t, où Ψ=−g est une fonction arithmétique continue explicite. La version étendue, arXiv2209.12832v2, théorème 1.1, permet seulement un signe **éventuel**, pour tout t≥t₀. La garde pertinente porte sur les zéros de la fonction complétéeξ, pas sur les zéros triviaux réels de ζ.

Le mécanisme est la rigidité d'une transformée de Laplace :

\[
\int_0^\infty g(t)e^{izt}dt
=z^{-2}\frac{\xi'}{\xi}(1/2-iz),\qquad\Im z>1/2.
\]

Un signe éventuel force, par le théorème de Landau–Widder, une singularité de convergence sur l'axe réel de Laplace si une obstruction subsiste. Orξ n'a pas de zéro sur la demi-droite réelle correspondante. La transformée ne peut donc conserver de pôles dans le demi-plan interdit. L'équation fonctionnelle entraîneRH, puis Weil donne tous les couplages positifs. C'est une implication analytique démontrée ; il reste à prouver le signe scalaire.

L'exemple g=−t⁴ montre pourquoi cette implication est spéciale : le signe scalaire générique ne donne pas un noyau positif. Ici intervient la relation meromorphe exacte àξ'/ξ.

### 3.2. Une formule qui conserve l'arithmétique et l'archimédien

La formule (1.3) de Suzuki 2026, version 3 du 23 septembre, peut être écrite avec les constantes du corpus :

\[
\boxed{\Psi(t)=A(t)-\mathcal P(t),\qquad t\ge0,}
\]
\[
\mathcal P(t)=\sum_{q=p^r,\ \log q\le t}c_q(t-\log q),
\qquad c_q=\frac{\log p}{\sqrt q},
\]
\[
A(t)=4(e^{t/2}+e^{-t/2}-2)-\frac{C_0t}{2}
+\sum_{n\ge0}\frac{1-e^{-b_nt}}{b_n^2},
\quad b_n=2n+\tfrac12.
\]

**Vérification de traduction.** ψ_digamma(1/4)−logπ=−C₀ ; le termeLerch est exactement la série affichée, car (n+1/4)²=b_n²/4. Le terme des premiers est une intégrale de la même mesure Chebyshev queDoc70. Il n'y a ni approximation des premiers par une moyenne ni donnée de zéros en entrée.

Pour t>0, la série peut être dérivée localement et

\[
A''(t)=2\cosh(t/2)-\frac{e^{-t/2}}{1-e^{-2t}}.
\]

Ainsi A est strictement convexe sur t≥log2 : le dernier quotient y est≤(4/3)e^(−t/2), donc A''≥e^(t/2)−e^(−t/2)/3>0. À l'origine le comportement est singulier ; cette convexité n'est pas postulée sur tout[0,∞).

### 3.3. Un contrôle par deux cumulants premiers

Trier les puissances premières : d_j=log q_j et c_j>0. Poser

\[
C_j=\sum_{i\le j}c_i,\qquad L_j=\sum_{i\le j}c_id_i,
\quad(C_0^{\rm cumul},L_0)=(0,0).
\]

Le symbole C₀ de la forme et le cumul initial0 sont distincts. Pour tout t,

\[
\mathcal P(t)=\sup_{j\ge0}(C_jt-L_j).
\]

**Preuve.** Chaque atome avec d_i≤t augmente le cumul affine ; chaque atome futur le diminue. Le maximum est donc exactement le préfixe actif, ou le préfixe vide. □

Pour un seuil T≥log2, définir

\[
A_T^*(C)=\sup_{t\ge T}\{Ct-A(t)\}.
\]

Comme A est strictement convexe et croît exponentiellement, ce supremum est fini. Son point maximum estT si C≤A'(T), sinon l'unique solution de A'(t)=C. On a l'équivalence exacte

\[
\boxed{\Psi(t)\ge0\quad\forall t\ge T
\quad\Longleftrightarrow\quad
L_j\ge A_T^*(C_j)\quad\forall j\ge0.}
\]

**Preuve.** A≥sup_j(C_jt−L_j) équivaut à chaque inégalité affine pour tout t≥T. Prendre le supremum sur ce même domaine. □

Cette frontière convexe réduit une loi scalaire continue à une famille précise de points arithmétiques(C_j,L_j). Le quantificateur reste infini. « Les points ont l'air au-dessus » sur une liste finie ne remplit pas la loi. L'inégalité complète étant équivalente àRH, la constater comme prémisse ne constitue pas une preuve ; il faut un mécanisme indépendant qui place les points.

## 4. Un mécanisme constructif candidat : transport barycentrique

Fixer T≥log2 et certifier Ψ(T)≥0. Écrire m=Ψ(T)/T et a=Ψ'_+(T), avec la dérivée **droite** siT est un logarithme de puissance première. Définir les mesures positives localement finies sur [0,∞) :

\[
\mu=A''(u)\mathbf1_{(T,\infty)}du+m\delta_0+(a-m)_+\delta_T,
\]
\[
\nu=\sum_{d_q>T}c_q\delta_{d_q}+(m-a)_+\delta_T.
\]

La présence d'un atome àT et son signe sont conservés ; l'exclusion d_q>T est cohérente avec la dérivée droite. Pour t≥T,

\[
\boxed{\Psi(t)=\int(t-u)_+\,d\mu(u)-\int(t-u)_+\,d\nu(u).}
\]

**Preuve.** La différence des mesures est Ψ'' sur(T,∞), plusmδ₀+(a−m)δT. La contribution de ces deux atomes vaut a(t−T)+mT ; les deux conditions de bord donnent Ψ(T)+a(t−T). Pour0≤t<T, la différence des intégrales vaut simplementmt. □

**Théorème conditionnel réellement suffisant.** Si l'on construit un noyau de probabilités P_x sur [0,∞), pourν-presque toutx, avec

\[
\mu(dy)=\int P_x(dy)d\nu(x),\qquad
\int yP_x(dy)=x,
\]

alors Ψ(t)≥0 pour tout t≥T, puisRH.

**Preuve.** La fonction φ_t(u)=(t−u)_+ est convexe. Jensen donne ∫φ_t(y)P_x(dy)≥φ_t(x). Tonelli puis les marginales donnent ∫φ_t dμ≥∫φ_t dν. Chaque intégrale est finie : φ_t est bornée et n'est non nulle que sur [0,t], où les mesures sont finies. Le signe et le théorème de Suzuki concluent. □

**Pourquoi c'est inventif et pourquoi ce n'est pas acquis.** Une carte barycentrique positive entre les atomes premiers et la courbure archimédienne forcerait une classe entière d'inégalités convexes, puis tous les couplages de Weil par le pont scalaire. Ses règles de masse et de premier moment sont des conditions concrètes sur des objets arithmétiques. Aucun tel noyau n'a été construit dans le corpus.

**Garde critique des mesures infinies.** μ etν ont une masse totale infinie. Le théorème de Strassen habituel pour probabilités à premier moment fini n'en donne pas l'existence automatique. Une limite de transports tronqués doit conserver les marginales sur tous les compacts, les barycentres et les moments des lignes ; une fuite au loin peut détruire l'égalité de premier moment. Seule la suffisance Jensen ci-dessus est prouvée ici.

**Objectif intermédiaire falsifiable.** Choisir une règle explicite de transport à bandes ou par cellules — avec paramètres fixés et construits depuis A'',d_q,c_q — puis contrôler masse, premier moment et signe de tous ses poids sur un premier lot comportant plusieurs premiers. Un échec de conservation, un poids négatif ou un contre-exemple à l'inégalité issue de cette règle réfute ce mécanisme précis. S'il passe, rechercher une identité de transition qui conserve les marges et les moments à l'ajout du lot suivant. Un simple transport optimisé après chaque résultat ne prouve pas encore une loi universelle.

## 5. Factorisation et passivité : ce qui imposerait vraiment le signe

### 5.1. Factorisation de Gram, pas racine du résultat souhaité

Si des applications L_ε(d) dans un Hilbert extérieur satisfait

\[
k_\varepsilon(d-e)=\langle L_\varepsilon(e),L_\varepsilon(d)\rangle,
\]

alors tous les Toeplitz deDoc76 sont positifs, sans inspection de chaque taille. Le Hilbert et lesL doivent être construits depuis les facteurs arithmétiques/archimédiens **avant** de supposer le signe. Définir L=T^(1/2) ou l'espaceGNS à partir d'un noyau supposé positif ferait revenir la conclusion dans la prémisse.

Une preuve utilisant un nombre fini de règles peut traiter un espace infini. En revanche, une réalisation rationnelle à un nombre fini d'états ne peut identifierξ'/ξ : cette fonction possède une infinité de pôles, un transfert rationnel seulement un nombre fini.

### 5.2. Une colligation unitaire fournit une identité universelle

**Lemme structurel élémentaire.** Soit U=[[A,B],[C,D]] unitaire sur un Hilbert extérieur état⊕entrée. Pour |z|<1, poser X(z)=(I−zA)⁻¹B et F(z)=D+zCX(z). Alors

\[
\frac{I-F(z)^*F(w)}{1-\bar zw}=X(z)^*X(w).
\]

**Preuve.** U[zX(z);I]=[X(z);F(z)]. L'égalité des produits scalaires avant/aprèsU donne l'identité. □

Ce facteur à droite force toutes les positivités de noyau et tous les couplages. Le travail serait de construireU depuis les places deQ et d'identifier exactement le noyau de gauche à un transport de Weil, avec les compensateurs polaires et le défaut signé. Une phase de module1 sur une frontière n'est pas une telle construction : elle ne garantit ni analyticité ni contraction à l'intérieur.

Connes–Consani prouvent que les produits locaux archimédien+finis premiers sont quasi-inner, avec défaut Hardy compact, et que les espacesSonin correspondants forment un système inductif. Ce résultat fournit une architecture et des domaines ; il ne donne pas le signe du défaut compact qui sépare la trace positive de Weil. La comparaison doit suivre tous les nouveaux premiers et la couverture, pas un ensemble fixe de places.

### 5.3. Positivité conditionnelle sur quotient

Une identité

\[
Q_W(f)=\|Lf\|^2+2\Re\langle\ell(f),Mf\rangle+\langle\ell(f),C\ell(f)\rangle
\]

donnerait le signe sur l'idéal ℓ±=0. Le compensateur est autorisé à vivre dans les directions polaires ; la factorisation restante doit préserver les couplages. Si L est défini par la racine deQ restreinte, c'est encore une circularité. Une famille de contraintes supplémentaires choisies différemment sur chaque support peut artificiellement éliminer toutes les directions difficiles sans couvrir l'idéal initial ; elle n'est pas une preuve de RH.

Une réalisation de type Hamiltonien positif/deBranges ou une positivité géométrique de type Hodge peut remplir cette structure, **si** l'identité à la distribution complète est construite. Le Hilbert Weil/deBranges de Suzuki 2023, arXiv2301.00421, est présenté sousRH ; l'utiliser comme preuve de positivité indépendante serait circulaire. Construire un opérateur auto-adjoint décalé A_a−λI positif ne prouve pas A_a≥0. L'identification limite àξ dans Suzuki 2026 reste conjecturale.

## 6. Une marge scalaire uniforme serait la mauvaise cible

**Proposition conditionnelle démontrée.** SousRH, pour toutT>0,

\[
\inf_{t\ge T}\Psi(t)=0,
\]

bien que Ψ(t)>0 pour chaque t≠0 dans le théorème de Suzuki.

**Preuve.** SousRH,

\[
\Psi(t)=\sum_\gamma\frac{m_\gamma}{\gamma^2}(1-\cos(\gamma t)),
\qquad\sum_\gamma\frac{m_\gamma}{\gamma^2}<\infty.
\]

Choisir une liste finie dont la traîne coûte moins deε. La récurrence simultanée sur le tore donne des t arbitrairement grands pour lesquels toutes les phases de cette liste sont aussi proches de1 que souhaité. La contribution finie est petite et la traîne≤2ε. L'infimum est donc0. Aucune indépendance rationnelle ni simplicité des zéros n'est requise. □

Une erreur absolue fixe ou un plancher Ψ≥δ>0 ne peut payer ces quasi-annulations. Le mécanisme doit fournir un signe exact, une factorisation ou une domination relative qui suit ces annulations. Ce constat concerne la méthode ; il ne donne aucune valeur négative deΨ.

## 7. Gardes de domaine et de croissance

La continuité de g implique g∈D', pas automatiquement g∈S' ni −g'' tempérée. Le passage§2.5 de Suzuki 2026 affirme cette dernière propriété à partir de la continuité seule ; nous ne l'utilisons pas comme prémisse globale. Une fonction continue comme e^(t²) suffit à réfuter cette inférence générale. Les identités sur fenêtres et les convolutions par tests compacts sont valides dansD'. La transformée de Laplace est utilisée dans sa demi-bande de convergence, avec la croissance requise, plutôt qu'une Fourier globale non justifiée.

Les zéros triviaux de ζ aux entiers négatifs pairs ne sont pas les zéros deξ concernés par le critère. La preuve publiée spécifique àζ2023 est la référence principale pour ce pont ; la généralisation2025 porte la qualification correspondante sur la fonction complétée.

## 8. Verdict et prochaine obligation

**Démontré dans cette passe.** Validité du pont publié de signe scalaire/Laplace ; traduction exacte Ψ=A−P ; convexité deA sur la queue ; équivalenceFenchel pour tous les préfixes ; suffisance d'un transport barycentrique explicite, mêmeσ-fini sous les gardes indiquées ; lemma de colligation ; impossibilité d'une marge scalaire strictement positive uniforme sousRH.

**Candidat réellement constructif.** Un transport positif par cellules entre la mesure première et la courbure archimédienne, ou une identité passive qui l'encode. Il associerait le signe arithmétique et les couplages ; le théorème scalaire fournirait la couverture logique versWeil.

**Obligation ouverte.** Trouver et démontrer une règle arithmétique universelle réalisant ce transport, cette contraction ou cette factorisation. La reformulationFenchel est une cible précise, pas cette règle. Les moyennes, symétries et compactités restent des instruments, pas les sources du signe.

## Sources primaires et navigation

- Suzuki 2023, article publié, DOI 10.1112/jlms.12785 : https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/jlms.12785 ; théorèmes 1.6–1.8 et preuve7.2. Refs : turn130search0, turn135view1.
- Suzuki 2025, arXiv2209.12832v2, date mars 2025 : https://arxiv.org/pdf/2209.12832 ; théorème 1.1 et preuve§3.1. Refs : turn126view0, turn127view0, turn129view1.
- Suzuki 2026, arXiv2606.09096v3,23septembre2026 : https://arxiv.org/html/2606.09096v3 ; formule (1.3),§2.5, hypothèses §7 et identification limite conjecturale. Refs : turn135view0, turn136view0.
- Suzuki 2023, *On the Hilbert space derived from the Weil distribution*, arXiv2301.00421 : https://arxiv.org/abs/2301.00421 ; statut conditionnel explicite du Hilbert. Refs : turn126view1, turn127view4.
- Connes–Consani 2021, *Quasi-inner functions and local factors*, PDF auteur : https://alainconnes.org/wp-content/uploads/quasi-inner.pdf ; introduction, définition quasi-inner, système Sonin. Refs : turn125view2, turn126view4.

Ces sources n'ont pas été transformées en preuve de RH. Les propositions nouvelles et leurs limites sont attribuées séparément de leurs équivalences publiées.
