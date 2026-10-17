# Lemmes — énoncés et preuves (v3)

Statuts : **[RIG]** = preuve complète dans ce document, à des faits classiques explicitement
énoncés près ; **[RIG/PNT]** = utilise le théorème des nombres premiers ; **[NUM]** = test
numérique seulement. Notation :

\[
f=\frac1\zeta,\qquad q=-\frac{\zeta'}\zeta=\frac{f'}f,
\qquad \gamma_E=0.57721\ldots
\]

La v3 ferme l'ancien **GAP-2** : le passage entre l'exposant de `Q` et le zéro le plus à
droite est rédigé sans étape de « désmoothement » séparée, en appliquant Perron aux
demi-entiers.

---

## L1 [RIG] — Série génératrice

Soit

\[
c=\Lambda*\Lambda-\Lambda\log+2\gamma_E\Lambda.
\]

Alors sa série de Dirichlet est

\[
G(s)=q(s)^2+q'(s)+2\gamma_E q(s).
\]

**Preuve.** Pour `Re s>1`,

\[
q(s)=\sum_{n\ge1}\frac{\Lambda(n)}{n^s},
\]

donc `q²` correspond à `Λ*Λ` et

\[
q'(s)=-\sum_{n\ge1}\frac{\Lambda(n)\log n}{n^s}.
\]

Enfin `f'=fq` et `f''=fq²+fq'`, donc

\[
G=\zeta(f''+2\gamma_E f').\qquad\square
\]

---

## L2 [RIG] — Factorisation `c=1*a`

Avec

\[
a(n)=\mu(n)\big((\log n)^2-2\gamma_E\log n\big),
\]

on a

\[
\boxed{c=1*a.}
\]

**Preuve.** Pour `Re s>1`,

\[
f'(s)=-\sum\frac{\mu(n)\log n}{n^s},\qquad
f''(s)=\sum\frac{\mu(n)(\log n)^2}{n^s}.
\]

La série de `f''+2γ_E f'` est donc celle de `a`; multiplier par
`ζ(s)=\sum n^{-s}` donne `c=1*a`. \(\square\)

---

## L3 [RIG] — Support de `c`

- si `n=p^k`,
  \[
  c(n)=-(\log p)^2+2\gamma_E\log p;
  \]
- si `n=p^a q^b`, `p\ne q`,
  \[
  c(n)=2\log p\log q;
  \]
- si `n` possède au moins trois facteurs premiers distincts,
  \[
  c(n)=0.
  \]

En particulier

\[
\boxed{|c(n)|\ll (\log n)^2.}
\]

**Preuve.** Sur une puissance première,
`(Λ*Λ)(p^k)=(k-1)(log p)^2` et `Λ(p^k)log(p^k)=k(log p)^2`.
Pour deux premiers distincts seules les deux factorisations ordonnées contribuent à
`Λ*Λ`; pour trois premiers distincts ou plus aucune factorisation en deux puissances
premières n'existe. \(\square\)

---

## L4 [RIG] — Régularité de `G` en `s=1`

L'expansion

\[
\frac1{\zeta(s)}=(s-1)-\gamma_E(s-1)^2+O((s-1)^3)
\]

donne

\[
f'(1)=1,\qquad f''(1)=-2\gamma_E.
\]

Ainsi `f''+2γ_E f'` s'annule en `1`. Comme `ζ` possède un pôle simple en `1`,

\[
\boxed{G\text{ est holomorphe en }s=1.}
\]

Le test numérique de v3 vérifie en outre la valeur limite

\[
G(1)=2\gamma_E^2+6\gamma_1,
\]

où `γ_1` est la première constante de Stieltjes (convention
`ζ(1+z)=z^{-1}+γ_E-γ_1 z+\cdots`). \(\square\)

---

## L5 [RIG] — Double pôle aux zéros

Si `ρ` est un zéro de `ζ` de multiplicité `m`, alors

\[
q(s)=-\frac{m}{s-\rho}+q_0+O(s-\rho),
\]

donc

\[
\boxed{
G(s)=\frac{m(m+1)}{(s-\rho)^2}
+O\!\left(\frac1{s-\rho}\right).
}
\]

Pour un zéro simple,

\[
G(s)=\frac{2}{(s-\rho)^2}
+\frac{2c_0(\rho)-2\gamma_E}{s-\rho}+O(1),
\qquad
c_0(\rho)=\frac{\zeta''(\rho)}{2\zeta'(\rho)}.
\]

\(\square\)

---

## L6 [RIG] — Exposant d'énergie et zéro le plus à droite

Posons

\[
C(x)=\sum_{n\le x}c(n),\qquad
Q(X)=\int_1^X\frac{|C(x)|^2}{x^2}\,dx,
\]

et

\[
\Theta=\sup_{\rho}\Re\rho,
\]

le supremum portant sur les zéros non triviaux de `ζ` (on a toujours `1/2\le\Theta\le1`). Comme `Q(X)=0` pour `X<2`, on écrit `\log(1+Q(X))` ; cela ne change ni les exposants ni la limite supérieure. Alors

\[
\boxed{
\frac12\limsup_{X\to\infty}\frac{\log(1+Q(X))}{\log X}
=\Theta-\frac12.
}
\tag{L6}
\]

En particulier

\[
\boxed{Q(X)=X^{o(1)}\iff RH.}
\]

### L6.1 — Identité de Mellin

Pour `Re s>1`, la sommation d'Abel donne

\[
\boxed{
\frac{G(s)}s=\int_1^\infty C(x)x^{-s-1}\,dx.
}
\tag{6.1}
\]

### L6.2 — L'énergie impose une région sans zéro

Supposons

\[
\limsup_{X\to\infty}\frac{\log(1+Q(X))}{2\log X}<a.
\]

Alors `Q(X)\ll X^{2a}` pour tout `X\ge1`. Sur le bloc `[2^k,2^{k+1}]`, Cauchy–Schwarz donne, pour
`σ>1/2+a`,

\[
\begin{aligned}
\int_{2^k}^{2^{k+1}}|C(x)|x^{-\sigma-1}\,dx
&\le
\left(\int_{2^k}^{2^{k+1}}\frac{|C(x)|^2}{x^2}\,dx\right)^{1/2}
\left(\int_{2^k}^{2^{k+1}}x^{-2\sigma}\,dx\right)^{1/2}\\
&\ll 2^{k(a+1/2-\sigma)}.
\end{aligned}
\]

La série dyadique converge. Le membre droit de (6.1) définit donc une fonction holomorphe
pour `Re s>1/2+a` et prolonge `G(s)/s` depuis `Re s>1`. Par L5 aucun zéro de `ζ` ne peut
se trouver dans ce demi-plan. Ainsi

\[
\Theta-\frac12\le
\frac12\limsup\frac{\log(1+Q(X))}{\log X}.
\tag{6.2}
\]

### L6.3 — Un demi-plan sans zéro borne `C(x)`

*Correctif V6.13 (pré-relecture) : les bornes (6.3)–(6.4) sont utilisées plus bas en `Θ+ε/2`, et le cercle de Cauchy qui borne `q'` sort de la région où la borne sur `q` est énoncée. Il suffit de les énoncer pour `σ ≥ Θ+ε/4` (même preuve). Voir `1_Presentation/relecture/RELECTURE_THEOREME_A_EN.md`.*

Nous utilisons le fait classique suivant pour le logarithmic derivative de `ζ` : si
`σ\ge\Theta+\varepsilon` et `|t|\ge2`, alors

\[
q(\sigma+it)=O_\varepsilon(\log(|t|+2)),
\qquad
q'(\sigma+it)=O_\varepsilon(\log^2(|t|+2)),
\tag{6.3}
\]

uniformément sur toute bande verticale bornée à droite. Une preuve standard part de

\[
\frac{\zeta'}\zeta(s)
=\sum_{|\gamma-t|\le1}\frac1{s-\rho}+O(\log(|t|+2))
\]

pour `-1\le Re s\le2`, utilise l'écart horizontal `Re s-Re ρ\ge\varepsilon`, puis
Cauchy pour la dérivée. Par L4 le point `s=1` est régulier pour `G`; ainsi

\[
G(\sigma+it)=O_\varepsilon(\log^2(|t|+2))
\tag{6.4}
\]

sur `σ\ge\Theta+\varepsilon` dans la bande nécessaire au déplacement de contour.

Supposons d'abord `Θ<1` et fixons `ε>0`. Il suffit de traiter `ε<1-Θ`; posons

\[
\sigma_0=\Theta+\varepsilon/2<1,
\quad
b=1+1/\log x,
\quad
T=x^4,
\]

avec `x=N+1/2`. Le Perron tronqué standard, joint à `|c(n)|\ll\log^2 n` (L3), donne

\[
C(x)=\frac1{2\pi i}\int_{b-iT}^{b+iT}G(s)\frac{x^s}{s}\,ds
+O\!\left(\frac{x\log^3 x}{T}+\log^2x\right).
\tag{6.5}
\]

Le choix demi-entier assure `|x-n|\ge1/2` et élimine le seul problème de
« désmoothement » près du saut. Déplaçons le contour jusqu'à `Re s=σ_0`. Aucun pôle
n'est franchi : par définition de `Θ`, il n'existe aucun zéro à droite de cette ligne, et
`s=1` est régulier par L4. Avec (6.4), la nouvelle verticale vaut

\[
\ll_\varepsilon x^{\sigma_0}
\int_2^T\frac{\log^2 t}{t}\,dt
\ll_\varepsilon x^{\Theta+\varepsilon/2}\log^3x,
\]

et les horizontales valent

\[
\ll_\varepsilon \frac{x^{1+o(1)}\log^2T}{T}=o(1).
\]

Par absorption du facteur logarithmique,

\[
\boxed{C(x)\ll_\varepsilon x^{\Theta+\varepsilon}.}
\tag{6.6}
\]

Comme `C` est constante entre deux entiers, le passage des demi-entiers à tout réel `x`
ne coûte rien. Si `Θ=1`, la borne triviale tirée de L3,

\[
C(x)\ll x\log^2x,
\]

suffit au même calcul d'exposant.

On en déduit

\[
Q(X)\ll_\varepsilon
\int_1^X x^{2\Theta+2\varepsilon-2}\,dx
\ll_\varepsilon X^{2\Theta-1+3\varepsilon}
\]

(avec une puissance logarithmique absorbable lorsque `Θ=1/2`). Donc

\[
\frac12\limsup\frac{\log(1+Q(X))}{\log X}
\le\Theta-\frac12.
\tag{6.7}
\]

(6.2) et (6.7) donnent (L6). \(\square\)

### Corollaire quantitatif

Pour tout `0\le\delta\le1/2`,

\[
\boxed{
Q(X)\ll_\varepsilon X^{2\delta+\varepsilon}\ \forall\varepsilon>0
\quad\Longleftrightarrow\quad
\Theta\le\frac12+\delta.
}
\tag{6.8}
\]

Ceci formalise la critique centrale de la v2 : **tout gain de puissance fixe dans `Q` est
déjà un gain de région sans zéro fixe.**

---

## L7 [RIG/PNT] — Canaux terminaux

Pour `q` sans carré,

\[
H_\infty(q):=\sum_{q\mid d}\frac{a(d)}d
=-\frac{2\mu(q)}{\varphi(q)}
\sum_{p\mid q}\frac{p\log p}{p-1}.
\]

Si `q` n'est pas sans carré, `H_∞(q)=0`, et `H_∞(1)=0`.

**Preuve courte.** Pour `q` sans carré,

\[
\Phi_q(s):=\sum_{q\mid d}\frac{\mu(d)}{d^s}
=\frac{\mu(q)h_q(s)}{\zeta(s)},
\qquad
h_q(s)=\prod_{p\mid q}(p^s-1)^{-1}.
\]

Comme

\[
H_\infty(q)=\Phi_q''(1)+2\gamma_E\Phi_q'(1),
\]

et `f(1)=0`, `f'(1)=1`, `f''(1)=-2γ_E`, les termes en `γ_E` s'annulent et

\[
H_\infty(q)=2\mu(q)h_q'(1).
\]

Or

\[
h_q(1)=\varphi(q)^{-1},\qquad
\frac{h_q'}{h_q}(1)
=-\sum_{p\mid q}\frac{p\log p}{p-1},
\]

d'où la formule. La convergence au bord `s=1` utilise le PNT. \(\square\)

Forme équivalente :

\[
\log q+\sum_{p\mid q}\frac{\log p}{p-1}
=\sum_{p\mid q}\frac{p\log p}{p-1}.
\]

---

## L8 [RIG, classique] — Covariance des dents de scie

Pour

\[
\psi_d(x)=\{x/d\}-\tfrac12,
\]

la moyenne sur une période commune vérifie

\[
\boxed{
\langle\psi_d,\psi_e\rangle
=\frac{\gcd(d,e)^2}{12de}.
}
\]

C'est l'identité classique de Franel–Landau/Vasyunin.

---

## L9 [RIG] — Factorisation par canaux de diviseurs

Comme

\[
\sum_{q\mid n}J_2(q)=n^2,
\]

on a

\[
\gcd(d,e)^2=\sum_{q\mid d,\ q\mid e}J_2(q).
\]

Par conséquent, si

\[
H_I(q)=\sum_{\substack{d\in I\\q\mid d}}\frac{a(d)}d,
\]

alors

\[
\boxed{
\Sigma(I,J)=\frac1{12}\sum_qJ_2(q)H_I(q)H_J(q).
}
\]

\(\square\)

---

## L10 [RIG/PNT] — Lien exact avec Nyman–Beurling tronqué

Le moment nul

\[
\sum_{d\ge1}\frac{a(d)}d=0
\]

suit de `f'(1)=1`, `f''(1)=-2γ_E`. Avec

\[
\rho_d(u)=\left\{\frac1{du}\right\},
\]

on obtient

\[
C(x)=-\sum_{d\ge1}a(d)\left\{\frac xd\right\},
\]

au sens de la limite fournie par le PNT, puis par `u=1/x`,

\[
\boxed{
Q(X)=\int_{1/X}^{1}
\left|\sum_{d\ge1}a(d)\rho_d(u)\right|^2du.
}
\]

Le programme est donc explicitement dans la géométrie Nyman–Beurling/Báez-Duarte ; ceci
interdit de présenter cette réécriture comme une nouveauté sans comparaison bibliographique
préalable. \(\square\)

---

## L11 [RIG] — Énergie spectrale fenêtrée à deux paramètres

Posons

\[
B(t)=e^{-t/2}C(e^t),\qquad 0\le t\le L,
\]

et soit `w\in C_c^\infty((0,1))`. Définissons

\[
\mathcal B_{L,w}(\tau)
=\int_0^L B(t)w(t/L)e^{-i\tau t}\,dt.
\]

Pour toute fenêtre fréquentielle non négative `W\in L^\infty\cap L^1`, on définit

\[
\boxed{
Q_{w,W}(L;T,\Delta)
=\frac1{2\pi}\int_{\mathbb R}
W\!\left(\frac{\tau-T}{\Delta}\right)
|\mathcal B_{L,w}(\tau)|^2\,d\tau.
}
\tag{11.1}
\]

Cette quantité est positive et, par Plancherel, égale à une forme quadratique explicite
sur `B(t)w(t/L)` dont le noyau est la transformée inverse de la fenêtre
`W((\tau-T)/\Delta)`. Elle conserve simultanément une échelle horizontale `L=log X` et une
hauteur spectrale `T`.

**Important.** L11 ne donne **aucune** borne de densité de zéros. Il fournit seulement
l'observable à deux paramètres nécessaire au benchmark P2.3 de la v3. \(\square\)

---

# Ce qui n'est toujours pas prouvé

1. `Q(X)=O((log X)^3)` inconditionnellement, ou même `Q(X)\ll X^{1-\delta}` pour un
   `\delta>0` fixe. Par L6, ce dernier résultat donnerait déjà une bande sans zéro fixe
   `\Theta<1`.
2. Le théorème conditionnel complet
   `Q(e^L)=(4\kappa/3)L^3+\alpha L^2+\beta L+o(L)` : le terme diagonal est explicite,
   mais les sommes hors diagonale doivent être contrôlées.
3. Une borne non triviale de densité `N(\sigma,T)` tirée de L11.
4. Une positivité arithmétique analogue à celle qui ferme RH sur les corps de fonctions.
5. Tout contrôle nouveau de la queue des canaux terminaux ou de la concentration Fourier
   locale qui batte les résultats standards existants.


## L11 [conditionnel à RH, v3.4] — Terme dominant de Q
Sous RH : Q(X) ∼ (S/3)(log X)³ avec S=Σ_{ρ distincts} m²(m+1)²/|ρ|² (=4κ si zéros simples). Preuve complète modulo faits classiques F1–F5 dans `THEOREME_TERME_DOMINANT.md`.
