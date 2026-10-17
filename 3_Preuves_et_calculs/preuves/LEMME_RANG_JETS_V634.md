# V6.34 - Lemme de rang des jets et borne pour une courbe cubique

**Statut :** démonstration élémentaire complète dans le modèle fini ; méthode de Stepanov classique. Les certificats polynomiaux du programme sont en arithmétique exacte. Aucun transfert de ce lemme à ζ n'est établi.

## 1. Énoncé

Soit $p\ge5$ premier, $f\in\mathbb F_p[x]$ de degré trois, $e=(p-1)/2$, $g=f^e$, et

$$S=\{a\in\mathbb F_p:f(a)\ne0,\ g(a)=1\}.$$

Pour $J\ge1$, $1\le K\le(p-3)/2$ et $1\le M<p$, considérons l'espace **de polynômes**, sans quotient par $x^p-x$,

$$W=\operatorname{span}\{x^{jp+a},\ x^{jp+a}g:0\le j<J,\ 0\le a<K\}.$$

Soit $\mathcal J_M:W\to\mathbb F_p^{M|S|}$ l'application des dérivées de Hasse d'ordres $0,\ldots,M-1$ aux points de $S$. Alors

$$\dim W=2JK,\qquad
\operatorname{rang}\mathcal J_M\le
\sum_{k=0}^{M-1}\min\{|S|,K+J-1+2k\}.$$

En particulier, si

$$2JK>R:=M(K+J-1)+M(M-1),$$

il existe $A\in W$, non nul comme polynôme, qui s'annule à un ordre au moins $M$ en chaque point de $S$. D'où

$$|S|\le U:=\left\lfloor\frac{(J-1)p+K-1+3(p-1)/2}{M}\right\rfloor.$$

## 2. Preuve du rang

Pour $k<p$, dérivée ordinaire et dérivée de Hasse d'ordre $k$ diffèrent du facteur inversible $k!$. Il suffit donc de travailler avec $D=d/dx$. Posons $P_0=1$ et

$$P_{k+1}=fP'_k+(e-k)f'P_k.$$

Par induction,

$$f^kD^kg=gP_k,\qquad \deg P_k\le2k.$$

Les dérivées positives de $(x^p)^j$ s'annulent jusqu'à l'ordre $p-1$. Aux points de $S$, $(a^p)^j=a^j$ et $g(a)=1$. Après multiplication des lignes de jets d'ordre $k$ par $f(a)^k$, qui est non nul, les jets de $x^{jp+a}$ sont les valeurs du polynôme

$$x^j f^k D^k(x^a),$$

de degré au plus $j+a+2k$. Les jets de $x^{jp+a}g$ sont les valeurs de

$$x^j\sum_{\ell=0}^k\binom{k}{\ell}
 f^{k-\ell}D^{k-\ell}(x^a)P_\ell,$$

du même degré maximal. Chaque bloc d'ordre $k$ se factorise donc par l'évaluation de polynômes de degré au plus $K+J-2+2k$. Son rang est au plus $\min(|S|,K+J-1+2k)$. Le rang de l'empilement est au plus la somme des rangs des blocs, ce qui prouve l'inégalité.

Cette somme n'affirme pas que les blocs sont indépendants ; elle est seulement une borne supérieure. Les rangs exacts peuvent être beaucoup plus petits.

## 3. Preuve de la dimension et de l'existence

Les degrés dominants de la première famille sont $jp+a$. Ceux de la seconde sont

$$jp+a+3(p-1)/2=(j+1)p+(p-3)/2+a.$$

Le domaine $K\le(p-3)/2$ rend tous ces degrés distincts : les intervalles de résidus $[0,K-1]$ et $[(p-3)/2,(p-3)/2+K-1]$ sont disjoints et contenus dans $[0,p-1]$. Les $2JK$ polynômes sont donc linéairement indépendants. Cette vérification exclut les combinaisons qui seraient identiquement nulles.

Si $2JK>R$, le noyau des jets dans $W$ contient un polynôme non nul. Le degré maximal dans $W$ vaut

$$D=(J-1)p+K-1+3(p-1)/2.$$

L'annulation des jets de Hasse d'ordres inférieurs à $M$ équivaut à la divisibilité par $(x-a)^M$. Les facteurs correspondant aux points distincts sont premiers entre eux. Ainsi $M|S|\le\deg A\le D$, ce qui donne la borne annoncée.

## 4. Une famille explicite avec erreur en racine carrée

Prenons $r\ge1$ tel que $6r^2-2r+5\le p$, puis

$$M=2r,\quad J=r+1,\quad K=3r^2-r+1.$$

Le domaine de dimension est respecté et

$$2JK-R=2.$$

Le noyau existe donc **pour toute cubique**, sans connaître ses points. La borne devient

$$U=\left\lfloor\frac p2+\frac{3(p-1)}{4r}+\frac{3r-1}{2}\right\rfloor.$$

Le choix $r=\lfloor\sqrt{(p-5)/6}\rfloor$ est admissible dès que $r\ge1$ et donne $U=p/2+O(\sqrt p)$.

Soit $z$ le nombre de racines de $f$ dans $\mathbb F_p$, et $N=2|S|+z+1$ le nombre de points de $y^2=f(x)$, point à l'infini compris. Pour un non-résidu quadratique $\nu$, la cubique tordue $\nu f$ a $|S_{\nu f}|=p-z-|S|$ ; elle vérifie la même borne $U$. Par conséquent,

$$2p-z-2U+1\le N\le2U+z+1,$$

$$|N-(p+1)|\le2U-p+z=O(\sqrt p),\qquad z\le3.$$

La constante asymptotique donnée par cette famille est $2\sqrt6$ pour l'erreur sur $N$. Cette borne est plus faible que la borne de Hasse $2\sqrt p$ dans le cas lisse. Elle réalise le mécanisme d'existence sans invoquer Hasse ni RH pour les courbes. Une cubique sans racines multiples définit ici une courbe de genre un.

## 5. Optimisation et certificats

À $J,M$ fixés avec $2J>M$, le plus petit $K$ garantissant l'existence est

$$K=\left\lfloor\frac{M(J+M-2)}{2J-M}\right\rfloor+1.$$

Le programme compare ces paramètres dans la fenêtre déclarée $1\le J,M\le256$, avec $M<p$. Il ne revendique pas un optimum hors de cette fenêtre. Les paramètres sont enregistrés avant le comptage des points.

Pour $p=29,61,101$, il construit un vecteur exact du noyau, le polynôme correspondant, puis contrôle ses multiplicités par **division synthétique**, indépendamment des jets utilisés pour le construire. Les degrés, coefficients et vecteurs sont conservés dans `data/v634_jets_certificats.json`. Pour $p=1009,10007$, l'existence est garantie par la preuve et les paramètres ; aucune grande matrice ni aucun témoin explicite ne sont calculés.

Reproduction : `python scripts/run_v634_jet_bound.py`. Source : `src/jet_bound.py`. Tests : `tests/test_v634_jets.py`.

## 6. Ce qui manque pour les entiers

Le lemme fournit trois objets distincts : un espace de polynômes indépendant, un opérateur qui annule les jets, et une borne de degré contrôlant les multiplicités. Donner des unités fictives à ces objets peut accompagner les calculs, mais ne construit pas leur analogue arithmétique. Le transfert à ζ demanderait un espace, un opérateur et un théorème de comptage remplissant ces trois fonctions sans utiliser RH.

La méthode est celle de Stepanov : S. A. Stepanov (1969), *On the number of points of a hyperelliptic curve over a finite prime field*, <https://mathnet.ru/eng/im2197> ; E. Bombieri (1973), *Counting points on curves over finite fields (d'après S. A. Stepanov)*, <https://www.numdam.org/item/SB_1972-1973__15__234_0/>. La variante élémentaire ci-dessus est démontrée intégralement, sans prétention de nouveauté.
