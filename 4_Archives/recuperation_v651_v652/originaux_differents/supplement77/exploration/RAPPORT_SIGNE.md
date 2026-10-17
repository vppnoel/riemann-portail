# Trois mécanismes de signe — exploration critique

**Priorité : le certificat scalaire par domination convexe, puis un Gram commun.** Les propositions ci-dessous sont des programmes conditionnels, pas des preuves de RH. Leur intérêt est de désigner une construction manquante et un échec observable. La positivité des filtres $B_p=E_p^*E_p$, prise isolément, ne fournit aucune des constructions.

## 1. Un Gram commun, éventuellement obtenu par dilatation

Le résultat à construire serait une identité, valable sur tous les tests polaires,

\[
Q_W(f)=\|Af\|_{\mathcal H}^2-\|CAf\|_{\mathcal H}^2,
\qquad C^*C\leq I.
\]

Les coefficients diagonaux **et croisés** de cette identité doivent restituer exactement les contributions archimédiennes et premières. $A$, $C$ et l'espace ordinaire $\mathcal H$ doivent être construits à partir de ces données, avant toute hypothèse de signe. Une dilatation de contractions locales pourrait être le mécanisme ; il manquerait une compatibilité globale des couplages et une borne uniforme sur les compositions. Les filtres premiers positifs peuvent aider à paramétrer les tests, mais leur positivité ne prouve pas cette compatibilité.

Une version plus rigide serait un cocycle $b(t+u)=b(t)+V_t b(u)$, dans un espace hilbertien déjà défini, pour un groupe orthogonal $V_t$, tel que $\|b(t)\|^2=2h(t)$, où $h=-g_\zeta$. Il donnerait

\[
\langle b(t),b(u)\rangle
=h(t)+h(u)-h(t-u),\qquad
Q_W(f)=\left\|\int b(t)f'(t)\,dt\right\|^2.
\]

**Hypothèse manquante :** une réalisation arithmétique indépendante de ce cocycle, ou de la contraction globale. **Falsification :** un seul coefficient croisé incorrect, ou une section finie où la contraction dépasse 1. Définir $A=Q_W^{1/2}$, compléter pour la norme $Q_W$, ou appliquer GNS au noyau supposé positif serait circulaire. Le « coup double » d'une vraie réalisation serait le signe scalaire et le signe quadratique, avec le même objet.

## 2. Domination convexe et transport martingale

Écrivons, pour $t\geq0$,

\[
h(t)=B(t)-\sum_q c_q(t-\tau_q)_+,
\qquad \tau_q=\log q,\quad c_q=\Lambda(q)/\sqrt q,
\]

où $q$ parcourt les puissances de nombres premiers. La formule explicite de Suzuki donne

\[
B(t)=4(e^{t/2}+e^{-t/2}-2)
+\frac t2[\psi(1/4)-\log\pi]
+\sum_{k\geq0}\frac{1-e^{-(2k+1/2)t}}{(2k+1/2)^2}.
\]

Par différentiation, pour $t>0$,

\[
\beta(t):=B''(t)
=e^{t/2}-\frac{e^{-5t/2}}{1-e^{-2t}}>0
\quad(t\geq\log2).
\]

Entre deux valeurs successives de $\tau_q$, $h=B-S_jt+R_j$ est donc strictement convexe, avec $S_j=\sum_{i\leq j}c_{q_i}$, $R_j=\sum_{i\leq j}c_{q_i}\tau_{q_i}$. Son minimum est un bord ou le point $B'(t)=S_j$. Plus globalement,

\[
\sum_q c_q(t-\tau_q)_+=\sup_j(S_jt-R_j),
\qquad
h(t)\geq0\ (t\geq T)
\Longleftrightarrow
R_j\geq B_T^*(S_j)\ \text{pour tout }j,
\]

où $B_T^*(s)=\sup_{t\geq T}(st-B(t))$. Le préfixe vide est inclus. Cela fournit un test exact par préfixes, pas encore une raison du signe.

**Construction pouvant fournir cette raison.** Fixons $T>0$ tel que $\beta>0$ sur $[T,\infty)$ et $h(T)\geq0$, puis posons

\[
m=h(T)/T,\quad a=h'(T+),\quad
\mu=\mathbf1_{(T,\infty)}\beta(u)\,du+m\delta_0+(a-m)_+\delta_T,
\]
\[
\nu=\sum_{\tau_q>T}c_q\delta_{\tau_q}+(m-a)_+\delta_T.
\]

Les deux mesures sont positives, localement finies et de masse totale infinie. En intégrant deux fois sur la demi-droite,

\[
\boxed{\ h(t)=\int(t-u)_+\,\mu(du)-\int(t-u)_+\,\nu(du),\qquad t\geq T.\ }
\]

Chaque intégrale est finie pour un $t$ fixé. Cherchons des lois de probabilité $K_x$, de premier moment fini, vérifiant

\[
\int u\,K_x(du)=x,\qquad
\mu(du)=\int K_x(du)\,\nu(dx).
\]

Jensen pour la fonction convexe $(t-u)_+$ donne alors **exactement** $h(t)\geq0$. La forme du certificat est concrète : répartir les masses premières sur la densité archimédienne, en conservant chaque barycentre. Des répartitions à deux extrémités donnent des contributions triangulaires positives. Les données à $T$ sont incorporées au transport ; elles ne deviennent pas un plancher positif artificiel.

**Hypothèse manquante :** construire les $K_x$ par une règle arithmétique, avec bilan exact et poids non négatifs. Leur existence déduite d'un théorème d'ordre convexe supposant déjà $h\geq0$ ne serait qu'une reformulation. Une méthode plausible à tester est un appariement local de masses et de moments, avec fenêtres prescrites avant le calcul et budgets de bord explicites.

**Falsification :** échec d'un bilan, poids négatif ou défaut de barycentre dans ce transport prescrit ; plus radicalement, un préfixe $R_j<B_T^*(S_j)$. Un échec du transport local invalide seulement cette construction. Un déficit de Fenchel certifié invaliderait le signe lui-même. Ne pas normaliser les mesures infinies en probabilités, ni passer à la limite dans des transports tronqués sans contrôler les deux budgets de bord.

Le « coup double » passe ici par le théorème de Suzuki : pour ζ, le signe éventuel de $h$ implique RH et donc le signe universel de Weil. Jensen, tout seul, ne transforme pas les triangles obtenus en un Gram du noyau $h(t)+h(u)-h(t-u)$.

## 3. Empêcher le premier passage spectral à zéro

Après remise des intervalles de support sur un domaine fixe, chercher un flot de formes

\[
\partial_a\mathcal A_a
=X_a^*\mathcal A_a+\mathcal A_aX_a+Y_a^*Y_a.
\]

Si $X_a$ est localement intégrable, son évolution $R'=-X_aR$ donne

\[
R_a^*\mathcal A_aR_a
=\mathcal A_{a_0}+\int_{a_0}^a R_s^*Y_s^*Y_sR_s\,ds\geq0.
\]

La positivité sur un petit support se propagerait à tous les supports : les nouvelles interactions seraient absorbées par une congruence et un apport positif. **Hypothèse manquante :** dériver $X_a,Y_a$ de l'arithmétique, sur un domaine commun, avec les seuils $a$ des nouvelles interactions correctement traités. **Falsification :** reste ayant une direction négative, singularité non intégrable à un seuil, ou incompatibilité de domaines. Choisir $X_a=\tfrac12\mathcal A_a^{-1}\partial_a\mathcal A_a$ serait tautologique et précisément singulier au passage à zéro. Cette piste est moins concrète que le transport.

## Classement

Une somme de carrés directe fournirait le signe quadratique, mais la décomposition déjà étudiée contient $B_0<0$ : aucune somme de termes individuellement positifs n'en découle. Un **Gram commun** maîtriserait toutes les interférences. La **domination convexe** maîtrise seulement un signe scalaire ; pour ζ, le pont de Suzuki suffit à l'élever au signe universel. Son avantage actuel est la disponibilité de coefficients, de minima et de déficits exactement testables.

Sources primaires : [Suzuki, théorème 1.1](https://arxiv.org/pdf/2209.12832), [Suzuki, formule (1.3) et approche opératorielle, v3](https://arxiv.org/html/2606.09096v3). Les transports et le flot proposés ci-dessus sont des pistes exploratoires, non des résultats de ces articles.
