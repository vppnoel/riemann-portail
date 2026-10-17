# V6.42 — Un contrat global arithmétique et une voie de norme fermée

## 1. Fixer la convention

Employer les distributions Mellin de l’appendice B de Connes–Consani [CC21],
(149)–(151). Pour un test additif $f\in C_c^\infty(\mathbb R)$, poser
$k(u)=u^{-1/2}f(\log u)$. Avec $h=f*f^*$ et
$f^*(x)=\overline{f(-x)}$, on a
$k*\overline{k^\#}(u)=u^{-1/2}h(\log u)$, où
$k^\#(u)=u^{-1}k(u^{-1})$.
Les annulations de Mellin en 0 et 1 sont $\int f(x)e^{\pm x/2}dx=0$.
Le critère publié C.1 est une positivité de l’opposée de la somme locale
sur tous ces tests. Les lemmes suivants en déduisent une représentation
arithmétique et ses limites ; le signe requis reste ouvert.

## 2. Lemme A1 — La somme première est finie à support fixé

Si $\operatorname{supp}f\subset[-S,S]$, alors
$\operatorname{supp}h\subset[-2S,2S]$ et $h(-x)=\overline{h(x)}$.
La contribution des places finies vaut

\[
2\sum_{p^m\le e^{2S}}{\log p\over p^{m/2}}\Re h(m\log p).
\]

**Preuve.** Appliquer (150) à $g(u)=u^{-1/2}h(\log u)$.
Le terme $g(p^m)+g^\#(p^m)$ devient
$p^{-m/2}[h(m\log p)+h(-m\log p)]$.
Le support annule les termes $m\log p>2S$. □

Le changement $u=e^x$ dans (151) donne la contribution archimédienne

\[
\mathcal W(h)=(\log(4\pi)+\gamma_E)h(0)
+\int_0^\infty
{e^{-x/2}[h(x)+h(-x)]-2e^{-x}h(0)\over1-e^{-2x}}\,dx.
\]

La singularité à zéro est amovible. Au-delà de 2S, la queue est exactement
$-2h(0)\operatorname{artanh}(e^{-2S})$, par la substitution $v=e^{-x}$.
Cette expression emploie le signe de (151), distinct de l’opérateur de
signe opposé dans (153).

## 3. L’inégalité qui manque

Avec $Q_{\rm arch}(f)=-\mathcal W(f*f^*)$, le contrat est

\[
\boxed{
Q_{\rm arch}(f)\ge
2\sum_{p^m\le e^{2S}}{\log p\over p^{m/2}}\Re(f*f^*)(m\log p)}
\]

pour **chaque S>0** et chaque
$f=(\partial_x^2-1/4)\psi$, $\psi\in C_c^\infty((-S,S))$.
Par G1, tout test admissible possède cette représentation pour un S assez
grand. L’inégalité équivaut donc au signe global exigé, et ses quantités
se définissent depuis les premiers et le terme archimédien.

Les corrélations sont signées. À S fixé, une somme complète n’a pas de
queue de puissances premières au-delà du support. L’obstacle porte sur
tous les supports, tous les tests et les erreurs de compression ; ajouter
des premiers à un seul calcul fini ne remplit pas ce contrat.

## 4. Théorème A2 — Pas de norme uniforme de la partie première sur L²

Sur $L^2(\mathbb R)$, poser

\[
(U_\ell f)(x)=f(x-\ell),\qquad
K_X=\sum_{p^m\le X}{\log p\over p^{m/2}}
(U_{m\log p}+U_{-m\log p}),\qquad X\ge2.
\]

Cet opérateur est borné autoadjoint et

\[
\|K_X\|=2\sum_{p^m\le X}{\log p\over p^{m/2}}
\longrightarrow\infty.
\]

**Preuve.** Les translations sont unitaires et adjointes deux à deux.
L’inégalité triangulaire donne le majorant. Pour
$f_T=(2T)^{-1/2}1_{[-T,T]}$, la corrélation est
$\max(1-|\ell|/(2T),0)$. Son quotient de Rayleigh pour la somme finie
tend vers le majorant quand $T\to\infty$, d’où l’égalité.

La somme $\sum_p1/p$ diverge : sinon les produits finis
$\prod_{p\le X}(1-1/p)^{-1}$ seraient bornés, car
$-\log(1-1/p)\le2/p$. Mais leur développement contient la somme harmonique
jusqu’à X. Enfin $\log p/\sqrt p\ge1/p$ pour $p\ge3$ ; les seuls termes
$m=1$ font donc diverger la norme. □

Le théorème concerne L² avant restriction aux tests admissibles. Il ne
prouve aucune négativité de la forme complète. Il ferme le budget de norme
uniforme de cette seule somme de translations à coefficients positifs.
Le contrôle doit préserver les corrélations signées et la compensation
archimédienne, dans un domaine de forme approprié. Le lemme G4 sur les
opérateurs bornés ne s’applique pas automatiquement à cette limite.

## 5. Bilan de recherche

Le certificat local isole une paire et son changement de signature.
I6 exclut une métrique positive non dégénérée du compagnon au pli.
A1 fixe une forme arithmétique ; A2 exclut une norme uniforme de la seule
partie première. L’inégalité encadrée reste ouverte, comme la borne de
croissance suffisante du théorème A du corpus. Aucun signe global pour ζ
n’est obtenu ici.

Source primaire : A. Connes et C. Consani, *Weil positivity and Trace formula,
the archimedean place*, appendices A–C, (146), (149)–(151), proposition C.1.
[PDF auteur](https://alainconnes.org/wp-content/uploads/Selecta.pdf).
