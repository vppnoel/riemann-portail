# Simulation de referee B — Théorème B

## Énoncé audité

Sous RH,

\[
Q(X)\sim \frac{S}{3}(\log X)^3,
\qquad
S=\sum_{\rho\ \mathrm{distincts}}\frac{m(\rho)^2(m(\rho)+1)^2}{|\rho|^2}.
\]

Pour des zéros simples, `S=4 kappa` et le coefficient dominant est `4 kappa/3`.

## Verdict provisoire

**Plausible, structure cohérente, mais c'est le résultat qui exige le plus une lecture indépendante.** Aucun facteur `2`, `pi` ou `eta` incohérent n'a été trouvé dans l'audit interne. Les risques principaux sont l'uniformité de la queue, le passage de la somme locale à tous les zéros et l'usage exact du théorème taubérien.

## B1. Mellin–Plancherel

Sous RH, le Théorème A donne `C(x)<<x^{1/2+epsilon}`. Pour `sigma=1/2+eta`, ceci rend

\[
Q_\eta=\int_1^\infty |C(x)|^2x^{-2-2\eta}dx
\]

fini et permet d'identifier la transformée de Mellin à `G(s)/s`. La formule

\[
Q_\eta=\frac1{2\pi}\int_{\mathbb R}\frac{|G(\sigma+it)|^2}{|\sigma+it|^2}dt
\]

est cohérente.

### À citer précisément

- version de Mellin–Plancherel utilisée ;
- argument `L1 ∩ L2` ou approximation permettant d'identifier la transformée sur la droite.

## B2. Contribution locale d'un double pôle

Pour

\[
G(s)\sim \frac{A_\rho}{(s-\rho)^2},
\]

on utilise

\[
\int_{\mathbb R}\frac{du}{(u^2+\eta^2)^2}=\frac{\pi}{2\eta^3}.
\]

Après le facteur `1/(2pi)` et le poids `1/|rho|^2`, la contribution est

\[
\frac{|A_\rho|^2}{4|\rho|^2\eta^3}.
\]

La constante `S/4` dans `eta^3 Q_eta` est donc correcte.

Les termes croisés entre deux zéros distincts sont d'ordre inférieur pour un nombre fini de zéros fixé ; le terme simple au même zéro produit au plus `O(eta^{-2})`.

## B3. Queue haute

La construction

\[
W(t)=\sum_{|\gamma-t|<1}\frac1{(t-\gamma)^2+\eta^2}
\]

et l'estimation

\[
\int_T^{2T}W(t)^2dt\ll T(\log T)^2\eta^{-3}
\]

sont compatibles avec `N(T+1)-N(T)<<log T`. Combinées à

\[
|G|\ll (\log T)W+(\log T)^2,
\]

elles donnent la queue annoncée

\[
\int_{|t|\ge Y}\frac{|G|^2}{|s|^2}dt
\ll \frac{(\log Y)^4}{Y\eta^3}.
\]

### Point de referee majeur

Il faut fournir une dérivation complète de `|G|<<(log T)W+(log T)^2` à partir des faits F1–F2, en particulier le traitement des zéros éloignés dans `q'`. Une citation exacte ou un lemme autonome est préférable.

## B4. Somme S et multiplicités

Avec `m(rho)<<log |gamma|`, on obtient `A_rho^2<<log^4 T`. Sur une coquille dyadique, le nombre de zéros est `O(T log T)` et le poids `1/|rho|^2` vaut `O(T^{-2})`, soit `O(log^5 T/T)` par coquille ; la somme sur `T=2^k` converge.

## B5. Taubérien

Avec `U(L)=Q(e^L)`,

\[
Q_\eta=\int_0^\infty e^{-2\eta L}\,dU(L).
\]

Si `eta^3 Q_eta -> S/4`, alors pour `lambda=2eta`,

\[
\int e^{-\lambda L}dU(L)\sim 2S\lambda^{-3}.
\]

Karamata donne

\[
U(L)\sim \frac{2S}{\Gamma(4)}L^3=\frac{S}{3}L^3.
\]

La constante est cohérente. Il faut cependant citer la version exacte de Karamata pour une fonction croissante / mesure positive.

## B6. Priorité

Le résultat est présenté comme analogue de Cramér. Avant publication, il faut rechercher explicitement :

- moyens quadratiques de fonctions de von Mangoldt généralisées ;
- séries de Dirichlet dont le logarithmic derivative possède des pôles d'ordre supérieur ;
- extensions de Cramér donnant des équivalents à partir des ordres de pôles.

## Recommandation

**Major revision / external check required.** Je ne vois pas de contradiction interne, mais B ne doit pas être qualifié de nouveau avant une recherche bibliographique approfondie et une vérification indépendante des étapes B3–B5.
