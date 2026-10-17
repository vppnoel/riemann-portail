# Branche expérimentale V4.2 — Schrödinger, densité d'énergie et flux

**Statut : [HEUR/NUM/GAP].** Cette branche ne modifie ni le Théorème A, ni le Théorème B, ni la Proposition C. Elle explore une représentation opératorielle et de flux compatible avec le programme Hilbert–Pólya et avec le module de localisation de sources de la V4.1.

## 1. Motivation

Le programme travaille naturellement en temps logarithmique

\[
t=\log x.
\]

Un zéro non trivial

\[
\rho=\beta+i\gamma
\]

contribue, dans les formules explicites normalisées, un mode de la forme

\[
\psi_\rho(t)\propto e^{(\beta-1/2)t}e^{i\gamma t}.
\]

Avec la convention d'évolution de Schrödinger

\[
i\hbar\partial_t\psi=H\psi,\qquad \psi(t)=e^{-iEt/\hbar}\psi(0),
\]

ce mode correspond formellement à l'énergie complexe

\[
\boxed{E_\rho=-\hbar\gamma+i\hbar(\beta-1/2).}
\]

Par conséquent :

\[
\boxed{\mathrm{RH}\iff \operatorname{Im}E_\rho=0\ \text{pour tous les modes zêta}}
\]

**si** l'on réussit d'abord à dériver rigoureusement un opérateur dont les modes spectraux sont exactement ceux de la formule explicite. Cette dernière condition est le problème difficile : sans elle, l'identification n'est qu'un dictionnaire.

## 2. Deux lectures distinctes

### 2.1 Hilbert–Pólya / Hamiltonien fermé

Chercher un opérateur auto-adjoint \(H\) tel que les ordonnées \(\gamma\) des zéros apparaissent dans son spectre. L'auto-adjointeté force alors la réalité du spectre. C'est la philosophie Hilbert–Pólya.

### 2.2 Système ouvert / résonances

Conserver aussi \(\beta-1/2\). Un zéro hors ligne est représenté par un mode avec gain ou perte exponentielle. Un opérateur effectif non auto-adjoint peut alors avoir

\[
H=H_{\rm sa}+iK,
\]

avec \(K=K^*\). La partie \(K\) contrôle la création/destruction de norme. RH correspondrait à l'absence de composante anti-hermitienne sur le sous-espace arithmétique pertinent.

Cette lecture est proche de l'interprétation de Connes : zéros critiques comme spectre d'absorption, zéros non critiques éventuels comme résonances.

## 3. Équation de continuité — lien avec flux de surface

Pour un Hamiltonien de Schrödinger spatial

\[
i\hbar\partial_t\Psi=\left(-\frac{\hbar^2}{2m}\Delta+V\right)\Psi,
\]

avec potentiel éventuellement complexe, définissons

\[
\varrho=|\Psi|^2,
\qquad
J=\frac{\hbar}{m}\operatorname{Im}(\overline\Psi\nabla\Psi).
\]

Alors

\[
\boxed{
\partial_t\varrho+\nabla\cdot J
=\frac{2}{\hbar}\operatorname{Im}V\,\varrho.
}
\]

Sur un domaine \(\Omega\), le théorème de la divergence donne

\[
\boxed{
\frac{d}{dt}\int_\Omega\varrho
+\int_{\partial\Omega}J\cdot n
=\frac{2}{\hbar}\int_\Omega\operatorname{Im}V\,\varrho.
}
\]

C'est le point de contact le plus direct avec l'intuition « surface cellulaire » :

- \(\int_\Omega\varrho\) : contenu énergétique / masse de probabilité ;
- \(\int_{\partial\Omega}J\cdot n\) : flux traversant la surface ;
- \(\operatorname{Im}V\) : source/sink interne ;
- opérateur auto-adjoint / potentiel réel : **pas de création interne**, seulement redistribution et flux de bord.

Dans le dictionnaire zêta, un mode \(e^{(\beta-1/2)t}\) a

\[
\frac{d}{dt}|\psi_\rho|^2=2(\beta-1/2)|\psi_\rho|^2.
\]

Ainsi un zéro hors ligne à droite joue exactement le rôle d'un mode à gain positif.

## 4. Ce qu'il ne faut pas identifier abusivement

Le fonctionnel arithmétique

\[
Q(X)=\int_1^X|C(x)|^2\frac{dx}{x^2}
\]

est une **énergie de mesure** au sens \(L^2\), pas automatiquement l'énergie hamiltonienne

\[
\langle\Psi,H\Psi\rangle.
\]

Une formulation sûre consiste à introduire un opérateur d'observation \(M\) et écrire

\[
y=M\Psi,
\qquad
Q\sim\|y\|^2.
\]

Le problème de preuve devient alors : dériver \((H,M)\) depuis l'arithmétique et démontrer que la dynamique cachée est auto-adjointe / conservative sur le sous-espace observable.

## 5. Relation avec la localisation de sources V4.1

Le module V4.1 utilise les atomes

\[
e^{(\beta-1/2)t}e^{i\gamma t}.
\]

La V4.2 leur donne une interprétation dynamique :

\[
(\beta,\gamma)
\longleftrightarrow
E=-\hbar\gamma+i\hbar(\beta-1/2).
\]

On peut donc combiner :

1. **prétraitement** : moyennage, ondelettes, Laplacien régularisé ;
2. **localisation** : estimation de \((\beta,\gamma)\) ;
3. **interprétation opératorielle** : énergie complexe / résonance ;
4. **test de conservation** : flux de bord versus source interne ;
5. **test de stabilité** : observabilité uniforme des composantes \(\operatorname{Im}E\ne0\).

## 6. Ce qui existe déjà

Cette branche doit être positionnée par rapport à plusieurs programmes connus.

### Wu–Sprung (1993)

H. Wu et D. W. L. Sprung ont construit numériquement un potentiel local unidimensionnel reproduisant les premiers zéros non triviaux comme niveaux d'énergie ; le potentiel présente une structure fractale apparente. Cela montre qu'une reconstruction inverse de potentiel est possible numériquement, mais **ne dérive pas le potentiel depuis l'arithmétique** et ne prouve pas RH.

Référence : *Riemann zeros and a fractal potential*, Phys. Rev. E 48 (1993), 2595–2598, DOI 10.1103/PhysRevE.48.2595.

### Berry–Keating

Le programme \(H=xp\) compare la loi de comptage des zéros avec une quantification semi-classique et cherche un Hamiltonien dont le spectre corresponde aux ordonnées des zéros. C'est une réalisation centrale de l'idée Hilbert–Pólya, mais l'opérateur recherché n'est pas obtenu comme un Schrödinger local standard.

Références : Berry–Keating, *H = xp and the Riemann zeros* (1997/1999) ; Berry–Keating, *The Riemann Zeros and Eigenvalue Asymptotics*, SIAM Review 41 (1999), 236–266.

### Sierra–Rodríguez-Laguna

Des régularisations / variantes de \(xp\) donnent des spectres correspondant à la partie moyenne du comptage des zéros et discutent les extensions auto-adjointes.

Référence : G. Sierra, J. Rodríguez-Laguna, *The H=xp model revisited and the Riemann zeros*, Phys. Rev. Lett. 106 (2011), 200201.

### Connes

Connes interprète les zéros critiques comme un spectre d'absorption et d'éventuels zéros non critiques comme des résonances dans une formule de trace non commutative.

Référence : A. Connes, *Trace formula in noncommutative geometry and the zeros of the Riemann zeta function*, Selecta Math. 5 (1999), 29–106, arXiv:math/9811068.

### Hamiltoniens non hermitiens / PT

Il existe également des constructions d'Hamiltoniens non hermitiens ou PT-symétriques liées formellement aux zéros. Elles illustrent le lien « réalité du spectre ↔ RH », mais l'auto-adjointeté / choix d'espace de Hilbert y constitue précisément le point délicat.

## 7. Ce que V4.2 ajoute comme question de recherche

La nouveauté recherchée n'est **pas** : « peut-on ajuster un potentiel aux premiers zéros ? » — cela existe déjà.

La question spécifique au programme est :

> Peut-on dériver à partir des observables arithmétiques \(C,Q\), ou du signal de nombres premiers, un couple opérateur–observation \((H,M)\) pour lequel la formule explicite devient une véritable formule de propagation / flux, puis démontrer que toute composante anti-hermitienne est impossible ?

Une cible abstraite serait :

\[
i\partial_t\Psi=H\Psi,
\qquad y=M\Psi,
\]

avec

\[
Q(e^L)=\int_0^L\|y(t)\|^2dt,
\]

et une identité de dissipation

\[
\frac{d}{dt}\|\Psi\|^2
=2\langle\Psi,K\Psi\rangle,
\qquad H=H_{\rm sa}+iK.
\]

RH serait alors obtenue si l'arithmétique imposait

\[
\boxed{K=0\quad\text{sur le sous-espace cyclique engendré par les données premières}.}
\]

## 8. Tests de rejet obligatoires

Toute construction doit satisfaire :

1. **Davenport–Heilbronn** : elle doit autoriser une partie anti-hermitienne / des résonances puisque des zéros hors ligne existent sans produit d'Euler.
2. **Corps de fonctions** : elle doit expliquer où entre la positivité géométrique qui force la conservation / réalité spectrale dans le cas de Weil.
3. **Spectre fini** : ajuster les premiers \(N\) zéros doit être explicitement reconnu comme non probant.
4. **Troncature** : la stabilité doit être uniforme quand hauteur, fenêtre temporelle et dimension augmentent.
5. **Produit d'Euler** : le passage de « thermomètre spectral » à « interdiction des modes à gain » doit utiliser une structure absente de Davenport–Heilbronn.

## 9. GAP V4.2 — verrou principal

**GAP-SCHR.** Aucun opérateur de Schrödinger / Hamiltonien \(H\) n'est actuellement dérivé du signal arithmétique avec les trois propriétés simultanées :

1. spectre ou résonances exactement liés aux zéros de \(\zeta\) ;
2. domaine et conditions aux bords suffisamment explicites pour prouver l'auto-adjointeté ;
3. opérateur d'observation \(M\) reproduisant quantitativement \(C,Q\) ou la formule explicite.

Sans ces trois propriétés, le module reste un cadre de modélisation et de falsification.

## 10. Expériences numériques incluses

`src/schrodinger_flux.py` fournit :

- le dictionnaire \((\beta,\gamma)\leftrightarrow E\) ;
- un Hamiltonien de Schrödinger 1D par différences finies ;
- le défaut d'auto-adjointeté ;
- le courant de probabilité ;
- le terme source associé à un potentiel complexe ;
- des métriques simples de comparaison spectrale.

`scripts/run_schrodinger_flux_demo.py` vérifie sur un modèle jouet qu'un potentiel réel conserve la norme tandis qu'une partie imaginaire constante produit exactement le taux de source attendu.

---

**Conclusion.** Cette branche est conceptuellement compatible avec Hilbert–Pólya mais enrichit le programme d'un langage de **flux, conservation et système ouvert**. La formulation la plus féconde n'est pas de chercher « le beau potentiel qui reproduit les zéros », mais de chercher une identité arithmétique qui force la disparition de la partie dissipative \(K\).


## 10. Extension V4.3 : générateur identifié et métrique positive

La V4.3 formalise le passage du dictionnaire modal à un problème d'identification d'état. Voir `docs/ARITHMETIC_SCHRODINGER_GENERATOR.md`. Le propagateur est estimé depuis des snapshots multicanaux, puis converti en `H_eff=(i/dt)log A`. La conservation est testée dans une métrique positive `M`, non nécessairement euclidienne, via `H_eff^* M=M H_eff` et `A^* M A=M`. Le verrou analytique est l'existence d'une telle métrique avec coercivité uniforme et lien spectral exact avec les zéros.
