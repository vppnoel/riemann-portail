# Compensation entre blocs : deux mécanismes et leur confrontation

Ce rapport constitue une passe de recherche. Il ne démontre aucune nouvelle loi de signe globale pour la fonction de Riemann. Les identités ci-dessous sont démontrées ; les entrées arithmétiques manquantes sont identifiées séparément. La garde de préfixes et les contre-modèles ont été confrontés directement avec l'agent critique.

## 1. Comptabilité de Fenchel : crédit positif et dette de phase

On conserve exactement le modèle du document 78 :

\[
S(t)=A(t)-\sum_{q=p^k}c_q(t-x_q)_+,
\quad x_q=\log q,\quad c_q=\frac{\log p}{\sqrt q},\quad T=\log2.
\]

Sur \([T,\infty)\), \(A''=\beta>0\), où

\[
\beta(t)=e^{t/2}-\frac{e^{-5t/2}}{1-e^{-2t}}.
\]

On note \(G=A_T^*\) la transformée de Legendre restreinte, \(\theta=G'\) — donc \(\theta(C)=T\) avant le seuil \(A'(T)\), puis \((A')^{-1}(C)\). Pour les préfixes arithmétiques ordonnés,

\[
C_j=\sum_{i\le j}c_i,\quad L_j=\sum_{i\le j}c_i x_i,
\quad H_j=L_j-G(C_j).
\]

### Lemme 1 : séparation exacte du crédit et de la dette

\[
H_j-H_{j-1}=c_j(x_j-\theta_j)+B_j,
\qquad \theta_j=\theta(C_j),
\]

\[
B_j=\int_{C_{j-1}}^{C_j}(\theta_j-\theta(v))\,dv\ge0.
\]

Preuve : \(G(C_j)-G(C_{j-1})=\int\theta(v)dv\). Ajouter et retrancher \(c_j\theta_j\). La monotonie de \(\theta\) donne le signe de \(B_j\).

Interprétation : chaque événement arithmétique apporte un crédit de courbure positif. Le terme \(c_j(x_j-\theta_j)\) mesure son avance ou son retard relativement à l'horloge de la réserve continue. Il peut être négatif. Cette identité organise les compensations ; elle n'établit pas leur signe cumulé.

### Lemme 2 : le crédit de courbure total est fini, sans RH

\[
\sum_j B_j<\infty.
\]

Preuve : \(\beta\) est croissante sur \((0,\infty)\), puisque le terme soustrait dans sa définition est décroissant. Pour les indices suffisamment grands,

\[
B_j\le \frac{c_j^2}{2\beta(\theta_{j-1})}.
\]

Les bornes classiques de Chebyshev \(\psi(X)\asymp X\) impliquent, par sommation partielle, \(C_j\asymp\sqrt{q_j}\). Soustraire l'unique saut \(c_j\le\log q_j/\sqrt{q_j}\) laisse aussi \(C_{j-1}\asymp\sqrt{q_j}\). Comme \(A'(u)\sim2e^{u/2}\) et \(\beta(u)\sim e^{u/2}\), on obtient \(\beta(\theta_{j-1})\asymp\sqrt{q_j}\). Par conséquent,

\[
B_j\ll\frac{(\log q_j)^2}{q_j^{3/2}}.
\]

Cette série converge, même si l'on somme sur tous les entiers. Les premiers indices sont en nombre fini. Aucune hypothèse sur les zéros de zêta n'intervient.

Conséquence précise : le crédit positif de dispersion n'augmente pas indéfiniment. Il ne peut, à lui seul, justifier une dette arbitrairement grande. Le signe global exige une propriété spécifique du cumul des avances et retards arithmétiques.

### Garde de bloc obtenue avec l'agent critique

Un bloc de masse \(D\), de moment \(M\), à support dans \([a,b]\), a pour tout préfixe de masse \(d\) un moment au moins égal à

\[
\max\{ad,\,M-b(D-d)\}.
\]

Avec réserve initiale \(H_0\) et masse cumulée \(C_0\), cela donne la garde

\[
H_{\mathrm{préfixe}}\ge H_0+
\max\{ad,M-b(D-d)\}
-\bigl[G(C_0+d)-G(C_0)\bigr].
\]

Le minimum de ce minorant se calcule aux trois masses

\[
0,\quad D,\quad d_* = \frac{Db-M}{b-a},
\]

car, sur chaque partie, le minorant est concave. Cette garde contrôle les coupures internes et pas seulement les deux extrémités. Elle est optimale si l'on ne connaît que support, masse et moment : le modèle concentré aux extrémités atteint la borne.

Obligation manquante : un profil arithmétique intrabloc plus informatif que ces trois données. Les expériences sur les blocs à rapport fixe peuvent réfuter l'idée que leur seul bilan assure l'extension.

## 2. Couplage multiplicatif : la couche Selberg

Cette seconde entrée utilise une identité arithmétique indépendante de RH, et non une hypothèse de réserve positive.

Soit \(\Lambda\) la fonction de von Mangoldt. La convolution de Dirichlet est \((f*g)(n)=\sum_{d\mid n}f(d)g(n/d)\). On a

\[
\Lambda_2(n)=\Lambda(n)\log n+(\Lambda*\Lambda)(n)
=\sum_{d\mid n}\mu(d)\log^2(n/d)\ge0.
\]

Preuve élémentaire : partir de \(\log=1*\Lambda\), appliquer la dérivation arithmétique \(Df(n)=f(n)\log n\), qui vérifie la règle de Leibniz pour la convolution, puis convoler par \(\mu\). La positivité est visible dans la première expression. Les coefficients sont \((2k-1)(\log p)^2\) pour \(n=p^k\), \(2\log p\log r\) pour \(n=p^k r^\ell\), et nuls si \(n\) possède plus de deux facteurs premiers distincts.

Cette identité est classique (Selberg). Elle donne un pont entre la contribution des premiers et celle de leurs produits. Elle constitue une entrée arithmétique réelle, mais son signe positif ne transmet pas automatiquement le bon signe au signal de premier ordre.

Pour l'écrire dans la langue du transport, poser

\[
\nu=\sum_{n\ge2}\frac{\Lambda(n)}{\sqrt n}\delta_{\log n},
\quad\nu_0=e^{x/2}\,dx,\quad R=\nu_0-\nu,
\]

\[
\kappa_2=x\nu+\nu*\nu,
\quad \kappa_{2,0}=2xe^{x/2}\,dx,
\quad D=\kappa_{2,0}-\kappa_2.
\]

La convolution est maintenant additive dans la variable logarithmique. L'identité exacte est

\[
D=xR+(\nu_0+\nu)*R.
\]

Avec \(Z(t)=\int(t-x)_+R(dx)\), son double potentiel est

\[
Q(t)=tZ(t)-2\int_0^t Z(s)\,ds+((\nu_0+\nu)*Z)(t).
\]

En effet, \(P_{xR}=tP_R-2\int P_R\) et \(P_{K*R}=K*P_R\). Toutes les intégrales sont finies sur les compacts ; aucune soustraction de masses infinies n'est requise.

Expression arithmétique directement calculable :

\[
Q(t)=8[(t-4)e^{t/2}+t+4]
-\sum_{n\le e^t}\frac{\Lambda_2(n)}{\sqrt n}(t-\log n).
\]

Attention à l'ancrage archimédien : \(S=Z+E\), avec

\[
E(t)=4e^{-t/2}-4+(2-C_0/2)t
+\sum_{k\ge0}\frac{1-e^{-(2k+1/2)t}}{(2k+1/2)^2}.
\]

Ainsi \(Z\) et \(S\) ne sont pas interchangeables.

### Contre-modèle : l'inversion ne conserve pas la positivité

Le contre-modèle suivant utilise exactement le réservoir continu \(\nu_0=e^{x/2}dx\). Il remplace seulement la mesure des vrais premiers par une mesure artificielle :

\[
\nu=12\delta_{12/5}.
\]

Alors

\[
Z(t)=4(e^{t/2}-1-t/2)-12(t-12/5)_+,
\]

\[
Z(4)=4e^2-156/5<-8/5<0.
\]

En revanche,

\[
Q(t)=8[(t-4)e^{t/2}+t+4]
-\frac{144}{5}(t-12/5)_+-144(t-24/5)_+
\]

est positif pour tout \(t>0\).

Preuve globale : avant \(b=12/5\), \(Q\) est le potentiel d'une mesure positive. Sur \([b,2b]\), \(Q''=2te^{t/2}\ge72/5\). Les bornes élémentaires \(4.4<e^{3/2}<4.5\) donnent \(Q(3)\ge68/25\) et \(|Q'(3)|\le16/5\). La minoration quadratique uniforme donne

\[
Q\ge\frac{68}{25}-\frac{(16/5)^2}{2(72/5)}
=\frac{532}{225}>0.
\]

Sur \([2b,\infty)\), \(Q''\ge96\). Avec \(12<e^{5/2}<12.3\) et \(e^{12/5}>10\), on a \(Q(5)\ge1608/25\) et \(|Q'(5)|\le104/5\). Donc

\[
Q\ge\frac{1608}{25}-\frac{(104/5)^2}{192}
=\frac{931}{15}>0.
\]

Ces bornes exponentielles se vérifient par séries de Taylor avec reste géométriquement majoré. L'agent critique a revérifié les expressions et les minorations.

Portée exacte : il s'agit d'un contre-exemple au principe générique « forcing Selberg double intégré positif implique signal de premier ordre positif », même en conservant le réservoir exponentiel exact. Ce n'est pas un contre-exemple à RH, ni à une propriété plus forte utilisant les vrais coefficients \(\Lambda(n)\). La positivité de la couche semipremière seule est insuffisante ; il faut une information supplémentaire sur sa phase ou son inversion.

## 3. Nouveau résultat publié à intégrer, sans lui attribuer le verrou résolu

Suzuki, *Weil's quadratic form via the screw function*, arXiv:2606.09096v3, version du 23 septembre 2026, fournit sans RH une réalisation de l'opérateur localisé comme extension de Friedrichs de \(D^*G_aD\), la continuité de sa plus petite valeur propre et un résultat de positivité/simplicité pour les petites portées. La construction d'extensions auto-adjointes après décalage \(\lambda<\lambda_a\) ne prouve pas \(\lambda_a\ge0\) pour toutes les portées. Le passage limite reste conjectural ; l'auteur précise que le choix \(\lambda=0\) à grande portée est équivalent à RH. Il faut citer ce travail dans le corpus plutôt que présenter cette traduction comme une découverte du programme.

## 4. Décision de recherche

La priorité est le premier mécanisme : mesurer les dettes de préfixes et montrer où la garde fondée sur masse/moment/support échoue, puis identifier l'information arithmétique supplémentaire nécessaire. Le second mécanisme demeure un pont exact réutilisable, accompagné d'un contre-modèle qui interdit une inversion positive simpliste.

Un prochain résultat ne compte comme progrès sur la loi de signe que s'il apporte un contrôle indépendant du profil ou de la phase, démontré sans supposer le signe global. L'énoncé « toutes les réserves sont positives » reste une reformulation. La couche Selberg classique, prise isolément, ne fournit pas ce contrôle.

## Sources primaires consultées

- M. Suzuki, *Aspects of the screw function corresponding to the Riemann zeta function*, https://arxiv.org/pdf/2206.03682 (critères globaux, cadre du signal).
- M. Suzuki, *Weil's quadratic form via the screw function*, https://arxiv.org/pdf/2606.09096 (version 3 vérifiée, 23 septembre 2026 ; Théorèmes 1.1, 1.3, 1.4 et Corollaire 1.6).
- T. Tao, cours 254A, *Notes 1: Elementary multiplicative number theory*, https://terrytao.wordpress.com/2014/11/23/254a-notes-1-elementary-multiplicative-number-theory/ (bornes de Chebyshev et identités classiques de \(\Lambda_k\), équations 70–72).
