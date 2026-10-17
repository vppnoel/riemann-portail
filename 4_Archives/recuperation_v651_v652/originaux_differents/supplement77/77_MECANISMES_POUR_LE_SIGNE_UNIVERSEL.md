# Mécanismes possibles pour le signe universel de Weil

Complément de recherche après V6.51 - 14 octobre 2026, heure de Bruxelles.

**Avis issu de la confrontation.** La piste la plus concrète est un transport
positif conservant masse et barycentre : il imposerait par Jensen un signe
scalaire, et un théorème de Suzuki transmettrait ce signe à RH, donc à toutes
les formes de Weil. La construction arithmétique du transport reste inconnue.
Une réalisation de Gram commune constitue une autre architecture forte.

Ce texte distingue trois niveaux : théorèmes primaires relus, identités
auxiliaires reconstruites ici, programmes conditionnels. Aucun mécanisme
universel de signe pour ζ n'est obtenu dans cette passe.

## 1. Ce qui impose réellement un signe

Une somme de carrés, un Gram d'un même espace hilbertien ou le défaut d'une
contraction fixent le signe de toutes les combinaisons, avec leurs termes
croisés. Une identité d'énergie pourrait avoir la forme

\[
Q_W(f)=\|Af\|_{\mathcal H}^2-\|CAf\|_{\mathcal H}^2,\qquad C^*C\preceq I.
\]

Il faut construire A, C et le Hilbert externe à partir de l'arithmétique,
indépendamment du signe recherché. Prendre la racine positive de Q ou compléter
un espace pour la norme Q avant de démontrer son signe serait circulaire.

Une colligation unitaire avec bilan d'énergie exact pourrait fournir une telle
contraction. L'unitarité d'une phase isolée, l'autoadjonction d'un opérateur,
la compactité d'un défaut ou la positivité des filtres premiers ne suffisent pas.

Un cocycle arithmétique dans un Hilbert construit indépendamment,
$b(t+u)=b(t)+V_tb(u)$, serait une version relationnelle : si
$\|b(t)\|^2=2S_\zeta(t)$, alors ses Grams paieraient les couplages.
L'objet b n'est pas construit ici.

## 2. Un pont primaire plus ciblé : le signal de Suzuki

La référence Suzuki2026 figurait déjà dans le registre du corpus, avec une
vérification limitée au résumé. La lecture du texte et des travaux2023/2025
fournit maintenant une cible plus précise. Ce n'est pas un théorème nouveau du
présent dossier.

Notons $S_\zeta=-g_\zeta$, différent de la fonction de Chebyshev Ψ. Pour $t\ge0$,

\[
S_\zeta(t)=A(t)-P(t),\qquad
P(t)=\sum_{q=p^m}c_q(t-\tau_q)_+,
\quad c_q=\frac{\log p}{\sqrt q},\quad \tau_q=\log q.
\]

\[
A(t)=4(e^{t/2}+e^{-t/2}-2)-\frac{C_0t}{2}
+\sum_{n\ge0}\frac{1-e^{-b_nt}}{b_n^2},
\quad C_0=\log(8\pi)+\gamma_E+\frac{\pi}{2},\quad b_n=2n+\frac12.
\]

Suzuki2023, théorème1.7, prouve RH équivalente à $S_\zeta(t)\ge0$ pour tout t.
L'extension2025, théorème1.1, permet pour ζ de demander seulement le signe
au-delà d'un seuil. Le lien ne vaut pas pour une fonction scalaire quelconque :
la transformée de Laplace de ce signal est reliée à $\xi'/\xi$, et l'absence
de zéros réels de la fonction complétée permet l'argument de Landau-Widder.
Un signe éventuel contraindrait alors tous les zéros non triviaux.

Contre-exemple générique : $g(t)=-t^4$ est pair et négatif, mais son noyau
$g(t-u)-g(t)-g(-u)+g(0)$ aux points1 et−1 vaut

\[
\begin{pmatrix}2&-14\\-14&2\end{pmatrix},
\]

avec une valeur propre−12. La structure analytique spécifique de ζ est donc
indispensable au pont scalaire.

## 3. Reconstruction : une frontière convexe pour les premiers

La formule explicite donne, par différentiation,

\[
A'(t)=2(e^{t/2}-e^{-t/2})-\frac{C_0}{2}
+\operatorname{atanh}(e^{-t/2})+\arctan(e^{-t/2}),
\]

\[
A''(t)=e^{t/2}-\frac{e^{-5t/2}}{1-e^{-2t}}>0\quad(t\ge\log2).
\]

Ordonner les puissances premières et former les deux cumulants
$C_j=\sum_{i\le j}c_{q_i}$ et $L_j=\sum_{i\le j}c_{q_i}\log q_i$.
Le préfixe vide a C=L=0. Comme les poids sont positifs,

\[
P(t)=\sup_{j\ge0}(C_jt-L_j).
\]

Pour un seuil $T\ge\log2$, définir
$A_T^*(c)=\sup_{t\ge T}(ct-A(t))$. On obtient exactement

\[
S_\zeta(t)\ge0\ \forall t\ge T
\quad\Longleftrightarrow\quad
L_j\ge A_T^*(C_j)\ \forall j.
\]

La courbe A est strictement convexe et croît exponentiellement : le dual est
fini. Son optimum est T si $c\le A'(T)$, sinon l'unique $t_j$ où $A'(t_j)=c$.
La loi de signe devient ainsi une frontière portant sur deux cumulants
arithmétiques. C'est une reformulation structurée, pas une preuve de la loi.

Pour un optimum intérieur, l'identité de Bregman explicite le gain :

\[
A(t)-C_jt+L_j
=\underbrace{L_j-A_T^*(C_j)}_{\text{défaut arithmétique}}
+\underbrace{A(t)-A(t_j)-A'(t_j)(t-t_j)}_{\ge0\text{ par convexité}}.
\]

Un seul défaut par préfixe couvre donc tous ses t, sans grille temporelle.
Pour l'optimum au bord, ajouter le terme positif
$(A'(T)-C_j)(t-T)$. Il reste à imposer le bon signe à tous les défauts
arithmétiques, par une structure indépendante.

## 4. Programme inventif : transporter les masses en gardant leur barycentre

Choisir $T\ge\log2$ avec $S_\zeta(T)\ge0$ déjà encadré, puis poser
$m=S_\zeta(T)/T$, $a=S_\zeta'(T+)$ et $\beta=A''$.

\[
\mu=\mathbf1_{(T,\infty)}\beta(u)\,du+m\delta_0+(a-m)_+\delta_T,
\qquad
\nu=\sum_{\tau_q>T}c_q\delta_{\tau_q}+(m-a)_+\delta_T.
\]

Ces mesures sont positives et localement finies, mais de masse totale infinie.
Leurs termes de bord ne réclament aucun plancher positif uniforme. Une
intégration deux fois donne, pour $t\ge T$,

\[
S_\zeta(t)=\int(t-u)_+\,\mu(du)-\int(t-u)_+\,\nu(du).
\]

La construction recherchée serait un noyau de probabilités $K_x(du)$ tel que

\[
\mu(du)=\int K_x(du)\,\nu(dx),\qquad \int uK_x(du)=x.
\]

Autrement dit, chaque masse première est répartie sur le matériau archimédien
sans changer son centre moyen. Jensen pour $u\mapsto(t-u)_+$ donnerait alors le
signe pour tous t. Les intégrales concernées sont finies à t fixé ; Tonelli
permet cet argument malgré la masse totale infinie.

**Obligation ouverte :** construire K depuis les nombres premiers, avec poids
non négatifs, marginale exacte et premier moment conservé. Déduire son existence
de l'ordre convexe déjà positif serait circulaire. Un théorème de transport
pour probabilités finies ne justifie pas automatiquement le passage à ces
mesures infinies. Les limites doivent conserver les marginales et les moments
sans fuite.

Un échec d'une règle locale de transport ferme cette règle. Un défaut de
Fenchel négatif certifié pour le signal exact contredirait son signe global.

## 5. Autre mécanisme : un flot de congruence positif

Sur un domaine fixe, une identité indépendante

\[
\partial_s\mathcal A_s
=X_s^*\mathcal A_s+\mathcal A_sX_s+Y_s^*Y_s
\]

propagerait une positivité initiale par congruence. Il faut les domaines
communs, une évolution bien définie et une gestion des seuils premiers.
Choisir X à l'aide de $\mathcal A_s^{-1}$ déplacerait la difficulté et serait
singulier à l'éventuel passage par zéro. Ce flot est un programme moins
concret que le transport, pas une identité établie pour Weil.

## 6. Confrontation, test fini et limites

L'exploration et l'audit se rejoignent sur la priorité du transport, après
contrôle de ses bords. Le Gram commun est structurellement plus direct pour
les couplages ; Suzuki permet au transport scalaire de les atteindre autrement.

Le prototype a encadré **194 préfixes**, vide compris, jusqu'au plafond entier
1000, avec une plus petite marge affichée d'environ0,02802. Les candidats
numériques servent uniquement à proposer les positions ; leurs dérivées sont
ensuite encadrées et les minima évalués par intervalles. Il n'utilise aucun zéro.
La portée est un signe du signal sur $[\log2,\log1000]$, dans le modèle
d'arrondi déclaré. Ce n'est pas un certificat de la forme de Weil sur les
supports correspondants : le pont scalaire exige un signe éventuel universel.

Sous RH, le signal est strictement positif pour chaque t non nul, mais son
infimum au-delà de tout seuil est zéro, par récurrence simultanée des phases
et sommabilité de la queue. Une erreur absolue fixe ou une marge uniforme
positive serait donc une mauvaise cible.

**Priorité de recherche.** Prédéfinir une règle d'appariement de cellules
archimédiennes et d'atomes premiers ; tester ses bilans de masse et de moment,
puis chercher une loi d'ajout compatible. Le but est une conservation qui
force le signe, et non l'accumulation d'un nombre fini de préfixes positifs.

## Sources et reproduction

- M. Suzuki, *Aspects of the screw function corresponding to the Riemann zeta
  function*, Journal of the London Mathematical Society108 (2023),1448–1487 :
  théorèmes1.1,1.7 et preuve7.2,
  https://arxiv.org/pdf/2206.03682.
- M. Suzuki, *Screw functions of Dirichlet series in the extended Selberg
  class*, version2025 : théorème1.1 et preuve de la suffisance,
  https://arxiv.org/pdf/2209.12832.
- M. Suzuki, *Weil's quadratic form via the screw function*, prépublication2026
  v3 : formule1.3 et cadre opératoriel,
  https://arxiv.org/html/2606.09096v3.

Fenchel, Bregman et transport ci-dessus sont des reconstructions de travail.
Le prototype, son journal et les deux rapports sont conservés dans le paquet.
Pour le rejouer : installer mpmath1.3.0 puis

    python3 prototype_fenchel.py --corpus mini_corpus --cutoff 1000 --output resultat.json

Le modèle numérique n'est pas une vérification formelle du processeur ou de
l'implémentation des fonctions élémentaires. La positivité universelle de
Weil et RH restent ouvertes dans ce travail.
