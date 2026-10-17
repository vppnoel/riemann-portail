# Programme analytique vers RH — état consolidé au 3 octobre 2026

> **Avertissement scientifique.** L'hypothèse de Riemann reste ouverte. Ce document rassemble une tentative structurée, des identités exactes, des réductions, des expériences numériques et des conjectures intermédiaires. Toute étape non fermée est marquée explicitement.

> **Mise à jour v3 — calibration spectrale.** (i) L'ancien GAP-2 est fermé : L6 donne rigoureusement `1/2 limsup log Q/log X = Theta-1/2` ; (ii) le palier classique est `Theta<=1`, pas `Theta=1` ; (iii) la référence `(4κ/3)log³X` n'est que le terme diagonal dominant et les numériques restent des tests de cohérence ; (iv) la priorité n'est plus d'optimiser `Q(X)` directement, mais de passer trois tests de rejet : Davenport–Heilbronn, corps de fonctions, et densité de zéros via le nouvel observable `Q(X,T)` ; voir `docs/PRIORITES.md`.

---

## 0. Objectif

L'hypothèse de Riemann (RH) affirme que tout zéro non trivial `rho` de `zeta(s)` vérifie

\[
\Re\rho=\frac12.
\]

Le programme développé ici cherche une observable arithmétique dont une borne quadratique suffisante exclurait les zéros avec `Re rho > 1/2`, puis tente de comprendre cette borne par opérateurs de Gram, mollification, analyse de Mellin et covariance multiscale.

---

# I. Socle fonctionnel: Nyman–Beurling / Báez-Duarte

## 1. Critère de fermeture [RIG]

Posons

\[
\rho(x)=x-\lfloor x\rfloor,
\qquad
\rho_a(x)=\rho\!\left(\frac1{ax}\right),
\qquad
\chi=\mathbf 1_{(0,1)}.
\]

Le critère de Nyman–Beurling dans sa forme discrète de Báez-Duarte relie RH à l'approximation de `chi` par les dilatations `rho_a`.

Pour un sous-espace fini

\[
V_N=\operatorname{span}\{\rho_1,\ldots,\rho_N\},
\]

on définit

\[
d_N=\inf_{F\in V_N}\|\chi-F\|_2.
\]

Avec

\[
G_{ab}=\langle\rho_a,\rho_b\rangle,
\qquad
v_a=\langle\chi,\rho_a\rangle,
\]

l'optimum fini vérifie

\[
c=G^{-1}v,
\qquad
d_N^2=1-v^T G^{-1}v.
\]

Ce point fournit notre langage d'origine: Gram, projection, résolvante, observabilité.

## 2. Lecture opératorielle [RIG comme reformulation]

Si `A` est l'opérateur d'analyse par les fonctions `rho_n`, alors

\[
S=A^*A\ge0,
\qquad
\ker S=V^\perp.
\]

Le critère RH devient l'absence de composante de `chi` dans l'espace sombre:

\[
P_{\ker S}\chi=0.
\]

Une formulation d'observabilité utile est

\[
\forall\delta>0\ \exists C_\delta:
|\langle\chi,f\rangle|^2
\le \delta\|f\|^2+C_\delta\|Af\|^2.
\]

Cette forme clarifie pourquoi la seule étude du spectre positif de `S` ne suffit pas: une composante sombre peut disparaître dans des observables du type `A^*A`.

---

# II. Mellin, log-temps et mollificateurs

## 3. Symbole Mellin [RIG]

La transformée de Mellin de la partie fractionnaire donne

\[
\mathcal M[\rho_1](s)=-\frac{\zeta(s)}s.
\]

Sur la droite critique, le symbole énergétique naturel est

\[
\sigma(\omega)=
\frac{|\zeta(\frac12+i\omega)|^2}{\frac14+\omega^2}.
\]

La variable logarithmique transforme les dilatations en translations; le Gram devient presque stationnaire en `log n`.

## 4. Mollificateurs [RIG pour les identités, NUM/HEUR pour l'optimisation]

Un mollificateur est écrit

\[
M_N(s)=\sum_{n\le N}\frac{\mu(n)W(\log n/\log N)}{n^s}.
\]

La première famille étudiée était une fenêtre bêta symétrique. Elle améliore les erreurs locales quand son ordre augmente, mais augmente la fuite haute fréquence; pour grand ordre elle raccourcit effectivement le mollificateur vers `N^{1/2+o(1)}`.

Une fenêtre à plateau long a été testée puis abandonnée: sur la partie plate, un mode

\[
M_N(1)=\sum_{n\le N}\frac{a_n}{n}
\]

réapparaît et demande déjà une précision de niveau RH pour être suffisamment petit.

### Fenêtre adaptative compensée [NUM]

Une famille simple a été paramétrée par

\[
W_\theta(u)=1-u+\sum_{j=1}^p\theta_j u^j(1-u),
\]

puis optimisée par moindres carrés dans le Hilbert de Nyman–Beurling. Les calculs montrent une amélioration importante par rapport aux fenêtres bêta de même complexité, mais cela ne constitue pas une preuve asymptotique.

---

# III. Extraction de l'observable arithmétique centrale

## 5. Compensation du pôle en `s=1` [RIG]

Écrivons

\[
f(s)=\frac1{\zeta(s)},
\qquad q(s)=-\frac{\zeta'}\zeta(s)=\frac{f'}f(s).
\]

La combinaison compensée conduit à

\[
G(s)=\zeta(s)\big(f''(s)+2\gamma f'(s)\big)
=q(s)^2+q'(s)+2\gamma q(s).
\]

La singularité apparente en `s=1` s'annule car

\[
f'(1)=1,
\qquad f''(1)=-2\gamma.
\]

## 6. Coefficients exacts [RIG]

On définit

\[
\boxed{
 c(n)=(\Lambda*\Lambda)(n)-\Lambda(n)\log n+2\gamma\Lambda(n)
}
\]

et

\[
G(s)=\sum_{n\ge1}\frac{c(n)}{n^s}
\]

dans le demi-plan de convergence initial.

Structure élémentaire:

- si `n=p^k`, alors
  \[
  c(n)=-(\log p)^2+2\gamma\log p;
  \]
- si `n=p^a q^b`, `p != q`, alors
  \[
  c(n)=2\log p\log q;
  \]
- si `n` a au moins trois facteurs premiers distincts, `c(n)=0`.

## 7. Singularité aux zéros [RIG localement]

Si `rho` est un zéro de multiplicité `m`, alors

\[
q(s)\sim -\frac{m}{s-\rho},
\]

et donc

\[
\boxed{
G(s)=\frac{m(m+1)}{(s-\rho)^2}
+O\!\left(\frac1{s-\rho}\right).
}
\]

Ceci est crucial: tout zéro hors ligne crée un double pôle de `G`.

---

# IV. Énergie arithmétique et critère suffisant

## 8. Somme partielle et énergie [RIG]

Posons

\[
C(x)=\sum_{n\le x}c(n),
\]

et

\[
\boxed{
Q(X)=\int_1^X\frac{|C(x)|^2}{x^2}\,dx.
}
\]

En variable logarithmique

\[
B(t)=e^{-t/2}C(e^t),
\]

on a simplement

\[
Q(e^L)=\int_0^L|B(t)|^2dt.
\]

## 9. Transformée de Laplace [RIG dans le domaine de convergence]

La sommation d'Abel donne

\[
\frac{G(s)}s
=\int_1^\infty C(x)x^{-s-1}\,dx
=\int_0^\infty B(t)e^{-(s-1/2)t}\,dt.
\]

Par Cauchy–Schwarz, si pour tout `eta>0`

\[
\boxed{
\int_1^\infty
\frac{|C(x)|^2}{x^{2+2\eta}}\,dx<\infty,
}
\]

alors `G` n'a aucun pôle dans `Re s > 1/2`, donc aucun zéro de zêta n'y existe. La symétrie fonctionnelle donne alors RH.

Cette implication est l'une des cibles les plus propres du programme.

## 10. Relation avec l'abscisse du zéro le plus à droite [RIG]

Si

\[
\Theta=\sup_\rho\Re\rho,
\qquad
\eta_*:=\frac12\limsup_{L\to\infty}\frac{\log Q(e^L)}L,
\]

alors L6 établit maintenant

\[
\boxed{\eta_*=\Theta-\frac12.}
\]

La borne inférieure vient de la convergence de Laplace et du double pôle de `G` aux zéros. Pour la borne supérieure, la v3 applique Perron tronqué à des demi-entiers `x=N+1/2`, déplace le contour dans le demi-plan sans zéro `Re s>Theta`, et utilise la croissance polylogarithmique standard de `zeta'/zeta` à distance fixe des zéros. Le choix demi-entier supprime le problème de désmoothement près d'un saut de `C`.

Ainsi, pour tout `delta` dans `[0,1/2]`,

\[
Q(X)\ll_\varepsilon X^{2\delta+\varepsilon}
\quad\Longleftrightarrow\quad
\Theta\le\frac12+\delta.
\]

Cette identité rend explicite que tout gain de puissance fixe pour `Q` serait déjà un nouveau résultat de région sans zéro.

---

# V. Prédiction spectrale et constante de Burnol

## 11. Énergie amortie [RIG dans son domaine]

Pour `eta` à droite de toutes les singularités pertinentes,

\[
\mathscr H(\eta)
=
\int_0^\infty |B(t)|^2e^{-2\eta t}\,dt
\]

et Plancherel-Laplace donne

\[
\boxed{
\mathscr H(\eta)
=
\frac1{2\pi}\int_{\mathbb R}
\frac{|G(\frac12+\eta+i\tau)|^2}
{(\frac12+\eta)^2+\tau^2}\,d\tau.
}
\]

Un zéro `rho=beta+i gamma` crée, lorsque la verticale approche `eta=beta-1/2`, une divergence cubique

\[
\mathscr H(\eta)
\asymp
(\eta-(\beta-1/2))^{-3}.
\]

## 12. Échelle `log^3 X` [HEUR / conditionnelle]

Sous RH et en négligeant les interactions fines entre singularités, la somme des contributions diagonales conduit à la constante

\[
\kappa=2+\gamma-\log(4\pi),
\]

et à la prédiction

\[
\boxed{
Q(X)\sim \frac{4\kappa}{3}(\log X)^3.
}
\]

Cette constante est cohérente avec la constante optimale apparaissant dans la théorie Nyman–Beurling/Burnol; la présente asymptotique n'est toutefois pas démontrée ici.

---

# VI. Factorisation Möbius et moment nul

## 13. Nouvelle suite `a(n)` [RIG]

Définissons

\[
\boxed{
a(n)=\mu(n)\big((\log n)^2-2\gamma\log n\big).
}
\]

Comme

\[
\left(\frac1\zeta\right)''
+2\gamma\left(\frac1\zeta\right)'
=
\sum_{n\ge1}\frac{a(n)}{n^s},
\]

on obtient

\[
\boxed{c=1*a.}
\]

Ainsi

\[
C(x)=\sum_{d\le x}a(d)\left\lfloor\frac xd\right\rfloor.
\]

## 14. Moment nul [RIG avec convergence issue du PNT]

Le développement de `1/zeta(s)` au voisinage de `s=1` donne

\[
\boxed{
\sum_{n\ge1}\frac{a(n)}n=0.
}
\]

Ce moment explique l'annulation du mode cohérent principal.

## 15. Forme en parties fractionnaires [RIG après justification de convergence]

Puisque pour `d>x`, `{x/d}=x/d`, on obtient

\[
\boxed{
C(x)=-\sum_{d\ge1}a(d)\left\{\frac xd\right\}.
}
\]

Le problème devient donc une combinaison très structurée de dilatations de dents de scie, reconnectant directement l'observable `C` au monde Nyman–Beurling.

---

# VII. Décomposition hyperbolique et phases réciproques

## 16. Somme de Mertens pondérée [RIG]

Posons

\[
A(u)=\sum_{n\le u}a(n).
\]

Comme `c=1*a`, une décomposition hyperbolique à seuil `D` donne une représentation de `C(x)` combinant:

1. une partie `d<=D` en dents de scie;
2. des valeurs `A(x/k)`;
3. un terme frontière.

Le choix `D≈sqrt(X)` rend la partie petits diviseurs contrôlable trivialement à l'échelle `X^{o(1)}` dans la norme pondérée recherchée. Le verrou se concentre dans la queue.

## 17. Phase réciproque [RIG comme expansion de carré]

La partie haute conduit aux sommes

\[
S_{N,h}(x)=
\sum_{n\asymp N}
\mu(n)P(\log n)e\!\left(\frac{hx}{n}\right).
\]

Développer le carré donne un noyau

\[
\left|\int_X^{2X}
e\!\left(hx\left(\frac1m-\frac1n\right)\right)dx\right|
\ll
\min\left(X,\frac{N^2}{h|m-n|}\right).
\]

La zone `N<=X^{2/3}` est compatible avec un contrôle géométrique de grand-crible à la bonne échelle, tandis que `N>X^{2/3}` est la zone critique.

## 18. Fourier locale [HEUR → GAP]

Après linéarisation de `1/n` sur un bloc, le problème ressemble à une concentration locale de l'énergie Fourier de Möbius:

\[
\int_I
\left|\sum_{n\asymp N}\mu(n)e(\alpha n)\right|^2d\alpha.
\]

À la résolution extrême `|I|≈1/N`, une borne uniforme très forte serait déjà proche d'un contrôle RH de Mertens; il faut donc exploiter la structure particulière de `a(n)` et son moment nul, pas une estimation générique.

---

# VIII. “GPS analytique”: covariance, innovations, information

## 19. Ce que signifie réellement l'analogie [RIG comme algèbre Hilbert]

Soit un résidu `R` et une innovation `U`. La meilleure correction scalaire en norme quadratique est

\[
R_{new}=R-KU,
\qquad
K=\frac{\langle R,U\rangle}{\|U\|^2}.
\]

Alors

\[
\|R_{new}\|^2
=
\|R\|^2(1-\rho^2),
\qquad
\rho=\frac{\langle R,U\rangle}{\|R\|\|U\|}.
\]

L'information accumulée est

\[
\boxed{
\mathcal I=\sum_j-\log(1-\rho_j^2).
}
\]

Ceci est exactement un algorithme d'innovations / projection séquentielle. **Il ne constitue pas une nouvelle preuve à lui seul.** Il organise les covariances et permet de voir où un théorème arithmétique devrait produire un gain.

## 20. Covariance exacte des dents de scie [RIG]

Pour

\[
\psi_d(x)=\left\{\frac xd\right\}-\frac12,
\]

la moyenne sur une période commune est

\[
\boxed{
\langle\psi_d,\psi_e\rangle
=
\frac{\gcd(d,e)^2}{12de}.
}
\]

C'est notre “matrice de covariance” arithmétique exacte.

## 21. Factorisation par canaux de diviseurs [RIG]

L'identité de Jordan

\[
\gcd(d,e)^2=\sum_{q\mid d,e}J_2(q)
\]

donne, pour un bloc `I`,

\[
H_I(q)=\sum_{\substack{d\in I\\q\mid d}}\frac{a(d)}d,
\]

et

\[
\boxed{
\Sigma(I,J)
=\frac1{12}
\sum_{q\ge1}J_2(q)H_I(q)H_J(q).
}
\]

Ainsi la covariance est le Gram ordinaire des vecteurs

\[
v_I(q)=\sqrt{J_2(q)}H_I(q).
\]

Le canal commun `q=1` est précisément affecté par le moment nul

\[
\sum a(n)/n=0.
\]

Cette factorisation est l'un des résultats structurels les plus propres de la version actuelle.

---

# IX. Résultats numériques consolidés

## 22. Annulation énergie complète / diagonale [NUM]

Les calculs tronqués montrent une très forte annulation entre termes diagonaux et hors-diagonaux. Par exemple autour de `X=5e5`, le rapport énergie complète / proxy diagonal varie d'environ `1.4%` à `6%` selon `eta` dans les tests réalisés.

Le script reproductible est `weighted_energy_vs_diagonal.csv`.

> **Mise en garde v3.** Le proxy diagonal `Σc(n)^2 n^{-1-2η}` est dominé par la taille brute de `c(n)` (~`log²n`) ; l'annulation de 94–98 % reflète surtout la régularité exacte de `G` en `s=1` (L4), qui supprime les termes principaux par construction. Ce n'est pas un indice de structure supplémentaire.

## 23. Trajectoire “Apollo” [NUM]

On compare

\[
Q(X)
\]

à la trajectoire de référence

\[
Q_{ref}(X)=\frac{4\kappa}{3}(\log X)^3.
\]

Sur les tailles testées, le ratio à la seule référence dominante augmente grossièrement de `0.44` vers `0.72`; cette observation ne doit pas être extrapolée comme une preuve. Avec les 300 zéros disponibles (jusqu'à `gamma≈541.85`), la formule explicite temporelle reproduit directement `Q` à quelques pourcents. La diagonale corrigée de sa queue donne un rapport mesure/diagonale généralement autour de `0.90–0.96` aux tailles les plus grandes, avec des effets de petite taille plus forts. L'écart restant est compatible en ordre de grandeur avec des zéros omis, mais **ce point n'est pas démontré**.

## 24. Fourier locale de Möbius [NUM]

Sur des blocs `N<=8192`, l'énergie locale dans une fenêtre de largeur `1/N`, normalisée par sa moyenne de Parseval, possède des maxima observés autour de `5–8` et des percentiles 99% autour de `3.6–4.1`.

Ce comportement est compatible avec une concentration sous-polynomiale, mais les tailles sont trop petites et le diagnostic trop faible pour conclure.

## 25. Validation de la covariance PGCD [NUM + formule RIG]

La formule

\[
\gcd(d,e)^2/(12de)
\]

reproduit les covariances mesurées des blocs de dents de scie avec des erreurs relatives typiquement de l'ordre de `1e-3` dans le test fourni.

## 26. Information multiscale [NUM]

Les expériences Kalman/projection montrent une réduction de variance mesurable et une information positive, mais

\[
\mathcal I(X)/\log X
\]

ne montre pas de stabilisation (0,09 / 0,11 / 0,10 / 0,07 sur X=5·10³…5·10⁴). La piste est suspendue (P4).

---

# X. Pistes abandonnées ou rétrogradées

1. **Hilbert–Pólya seul**: trop peu contraignant sans opérateur arithmétique explicite.
2. **Spectre positif du dissipateur seul**: peut perdre une composante sombre.
3. **Slepian / rang effectif global**: insuffisant pour contrôler l'inverse au niveau d'epsilon requis.
4. **Type I/II de Möbius appliqué naïvement au mollificateur**: les plages de paramètres ne ferment pas l'estimation désirée.
5. **Fenêtre à plateau long**: déplace l'obstruction vers `M_N(1)`.
6. **Optimisation de noyau de contour**: risque de reformuler simplement l'obstruction Hardy/Nyman.
7. **Barban–Davenport–Halberstam brut**: moyenne dans la mauvaise géométrie pour l'observable hyperbolique.
8. **Parseval locale uniforme à résolution `1/N`**: probablement aussi difficile que RH si formulée génériquement.
9. **Kalman sans modèle arithmétique**: projection utile mais aucun contenu nouveau de preuve.

---

# XI. Verrou actuel et plan suivant

## 27. Verrou minimal après v3

Le verrou `Q(X)=X^{o(1)}` est désormais identifié exactement à RH par L6. Il ne doit plus être traité comme un palier intermédiaire. Les véritables questions de calibration sont :

- le formalisme distingue-t-il `zeta` d'une fonction de Davenport–Heilbronn sans produit d'Euler ?
- contient-il une positivité spécifique comparable au mécanisme de Weil sur les corps de fonctions ?
- surtout, peut-il produire une borne **non triviale de densité de zéros** avant d'attaquer le zéro extrême ?

## 28. Prochaine attaque recommandée : `Q(X,T)`

La v3 introduit l'énergie spectrale fenêtrée

\[
Q_{w,W}(L;T,\Delta)
=\frac1{2\pi}\int W\!\left(\frac{\tau-T}{\Delta}\right)
|\mathcal B_{L,w}(\tau)|^2d\tau,
\qquad L=\log X.
\]

Elle conserve à la fois la croissance horizontale des contributions de zéros et leur hauteur `gamma`. Le benchmark scientifique est désormais :

1. établir une minoration spectrale en fonction des zéros dans une boîte `beta>=sigma`, `|gamma-T|<=Delta`;
2. majorer la même énergie par des polynômes de Dirichlet / outils classiques;
3. en déduire une borne de `N(sigma,T)`;
4. comparer quantitativement à une borne de densité connue;
5. arrêter la route directe si aucune densité non triviale n'en sort.

Les canaux terminaux, Kalman et la Fourier locale restent disponibles comme diagnostics secondaires, mais ne pilotent plus la stratégie de preuve.

---

# XII. Conclusion

Le programme a progressé de “chercher un opérateur dont le spectre ressemble aux zéros” vers une cible beaucoup plus concrète:

\[
\boxed{
 c(n)=(\Lambda*\Lambda)(n)-\Lambda(n)\log n+2\gamma\Lambda(n)
}
\]

et

\[
\boxed{
Q(X)=\int_1^X\frac{|\sum_{n\le x}c(n)|^2}{x^2}\,dx.
}
\]

Les progrès réellement solides sont:

- la factorisation `c=1*a`;
- le moment nul `sum a(n)/n=0`;
- le double pôle universel de `G` aux zéros;
- la covariance exacte des dents de scie;
- sa factorisation en canaux de diviseurs;
- l'identification précise des endroits où les estimations génériques réintroduisent RH.

Le principal travail restant est toujours un gain d'annulation quadratique de niveau RH. Le package doit donc être lu comme une **carte de navigation analytique avec instruments reproductibles**, pas comme une preuve achevée.


---

# XIII. Mise à jour finale de cette version: canaux terminaux

La dernière évolution est archivée dans `notes/LATEST_GPS_ANALYTIC.md`.

Pour

\[
H_\infty(q)=\sum_{q\mid d}\frac{a(d)}d,
\]

on obtient, pour `q` sans carré,

\[
\boxed{
H_\infty(q)=
-\frac{2\mu(q)}{\varphi(q)}
\left(\log q+\sum_{p\mid q}\frac{\log p}{p-1}\right)
=-\frac{2\mu(q)}{\varphi(q)}\sum_{p\mid q}\frac{p\log p}{p-1}
\quad\text{(preuve : L7).}
}
\]

et `H_infty(q)=0` pour `q` non sans carré, avec `H_infty(1)=0`.

Cette formule fournit un “cap terminal” exact à chaque canal du modèle de covariance. Elle suggère une stratégie biais/variance: traiter analytiquement les petits canaux et contrôler en moyenne la queue `H_infty(q)-H_D(q)`. Le verrou devient une estimation pondérée de ces résidus de queue, et non une simple optimisation numérique du filtre.


---

# XIV. V4.1 — localisation de sources / traitement de signal

La nouvelle branche reformule la formule explicite comme un problème inverse : les données arithmétiques sont les observations et les zéros `rho=beta+i gamma` sont des sources latentes avec modes

\[
e^{(\beta-1/2)t}e^{i\gamma t}.
\]

Le package ajoute moyennage gaussien, Laplacien régularisé, analyse locale de type Morlet, matched filtering / GLS et métriques de visibilité. Le démonstrateur synthétique localise correctement une source hors ligne injectée et estime son taux de croissance.

**Statut scientifique :** aucun résultat A/B/C n'est modifié. Une preuve demanderait une borne uniforme d'observabilité d'une composante `beta>1/2`; aucune borne de ce type n'est obtenue. Voir `docs/SOURCE_LOCALIZATION.md`.


# Extension V4.2 — représentation Schrödinger / flux

La V4.2 ajoute une branche expérimentale inspirée des problèmes de conservation et de flux. En temps logarithmique, le mode d'un zéro `rho=beta+i gamma` s'écrit `exp((beta-1/2)t) exp(i gamma t)` et peut être codé par une énergie complexe `E=-gamma+i(beta-1/2)`. Sous cette convention, RH correspond à la réalité de toutes les énergies **si** un opérateur spectral exact peut être dérivé. L'équation de continuité permet de distinguer flux de bord et source interne : la partie imaginaire d'un potentiel/opérateur produit un taux de création de norme, analogue à `2(beta-1/2)`. Le détail, les garde-fous et le positionnement bibliographique sont dans `docs/SCHRODINGER_FLUX.md`.


# XV. V4.3 — faire émerger le générateur depuis le signal arithmétique

La V4.3 distingue deux démarches : (i) choisir un Hamiltonien/potentiel qui reproduit un spectre fini ; (ii) identifier la loi d'évolution directement depuis des observables arithmétiques. Seule la seconde est retenue comme programme expérimental.

À partir de canaux filtrés `y_j(t)` et de retards, on forme un état `z(t)` et on identifie

\[
z(t+\Delta t)pprox A z(t).
\]

On définit ensuite

\[
H_{m eff}=rac{i}{\Delta t}\log A.
\]

Le mode d'un zéro `rho=beta+i gamma` correspond alors à `E=-gamma+i(beta-1/2)`. La métrique pertinente n'est pas supposée euclidienne : on cherche `M>0` telle que

\[
H_{m eff}^*M=M H_{m eff},\qquad A^*MA=M.
\]

Dans le cas fini diagonalisable, l'existence d'une métrique positive rendant `H` hermitien équivaut à la réalité du spectre. Le package fournit ce diagnostic et un test synthétique RH-like / hors-ligne.

**Limite essentielle :** aucune construction exacte de `(H,M)` depuis l'arithmétique n'est démontrée, aucune coercivité uniforme n'est établie, et aucun lien spectral infini-dimensionnel avec tous les zéros n'est obtenu. La branche ne modifie donc pas le statut de RH ni des résultats A/B/C. Voir `docs/ARITHMETIC_SCHRODINGER_GENERATOR.md`.
