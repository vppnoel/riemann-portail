# Variante à raccord initial non minimal

Cette variante consomme exactement tout l'atome source en 0 dès le raccord
en T. Toutes les lignes premières suivantes sont recalculées sur ce nouveau
reliquat, indépendamment des anciens noyaux. Les diagnostics à 60 chiffres
réussissent pour les plafonds 10, 100 et 1000. Ils ne sont pas certifiés par
arrondis dirigés ; la certification du bloc initial par intervalles est traitée
indépendamment par l'agent principal.

## Bloc initial exact et effet sur le potentiel

Prendre

\[
\theta_T=m\delta_0+1_{[l,b]}\beta(u)du,
\quad
\int_l^b\beta(u)du=-a,
\quad
\int_l^bu\beta(u)du=T(m-a).
\]

Le calcul donne

\[
l=0.8409704668464285553678984371418438105074\ldots,
\quad
b=1.0205903181734080949515078483924954445805\ldots<\log3.
\]

Sa masse est `m−a`, son barycentre est T et il retire tout `mδ₀` de μ. Le
reliquat exact est

\[
R_1=1_{(T,l)\cup(b,\infty)}\beta(u)du.
\]

Posons `J_T(t)=P_{θ_T}(t)−(m−a)(t−T)_+`. Jensen donne `J_T≥0`.
Plus précisément, pour `l≤t≤b`,

\[
J_T(t)=\int_t^b(u-t)\beta(u)du,
\qquad J_T(t)=0\quad(t\ge b).
\]

La première égalité vient des conditions de masse et de premier moment, qui
imposent `J_T(b)=J_T'(b)=0`, et de la courbure β sur `[l,b]`. Pour `T≤t≤l`,
le gap est affine de pente a<0 et reste positif ; pour `0≤t≤T`, il vaut mt.
Ainsi `P_{R₁}=P_μ−P_{θ_T}` égale le potentiel initial `S₂` dès b. Avant
log3 aucun atome premier ultérieur n'intervient, et la positivité du potentiel
résiduel est automatique parce que R₁ est une mesure positive. Pour tous les
premiers suivants, le problème de positivité à résoudre après log3 reste
celui du potentiel arithmétique original.

Dans les coordonnées de masse de la source originale μ, le retrait prescrit
est la réunion de `[0,m]` et `[M(l),M(b)]`, avec `M(u)=m+A'(u)−A'(T)`.
Les lignes suivantes sont les blocs quantiles du reliquat, exactement comme
dans le premier script. La ligne artificielle finale reste marquée
`kind=boundary` et `atom=boundary`.

## Comparaison finie

Les largeurs ci-dessous sont les diamètres du support essentiel des noyaux,
raccord compris et bord exclu. Elles n'incluent pas un point de quantile de
masse nulle à la sortie de l'atome en 0.

| Plafond X | Atomes premiers q>2 | Raccords T | Largeur maximale originale | Largeur maximale non minimale | Réserve originale en 0 | Réserve non minimale en 0 |
|---:|---:|---:|---:|---:|---:|---:|
| 10 | 6 | 1 | 2.275156021795 | 1.564702058308 | 0.016177237193 | 0 |
| 100 | 34 | 1 | 4.515697493723 | 3.815500489403 | 0.007194823993 | 0 |
| 1000 | 192 | 1 | 6.277732355497 | 5.580027693932 | 0.004816836603 | 0 |

Il faut ajouter une seule ligne artificielle de bord à chaque test fermé.
Le raccord T a la masse `m−a=0.35684525208127565247…`, distincte de
`c₂=log2/√2`. Le test à 1000 contient donc **192 atomes premiers, un raccord
initial et un atome artificiel de bord**, soit 194 lignes de noyau.

Les noyaux non minimaux communs aux trois plafonds sont identiques chiffre
pour chiffre dans les JSON : même étiquettes, même nombre de morceaux et
écart maximal des extrémités de masse nul au format de sortie à 60 chiffres.
Les lignes de bord sont exclues de cette comparaison. Les arithmétiques
des raccords et des premiers sont donc stables quand on augmente le cap.

La variante laisse une réserve diffuse compacte, commençant à T, avant le
bord. La masse de cette première composante vaut respectivement
`0.0234056405384138`, `0.00850745511060893` et `0.00541691603535970` aux
trois plafonds. La masse en 0 est déjà nulle et aucune ligne après le raccord
initial n'y envoie de masse. Cette réserve diffuse montre ce qui remplace
le budget atomique du premier balayage ; sa présence ne fournit aucune
estimation globale sur les futurs préfixes.

À 1000, masse et premier moment totaux source/demande valent toujours
`62.3162348210272` et `327.113961130607`. Les erreurs maximales observées
par ligne sont `1.83×10^-59` en masse et `4.18×10^-48` en premier moment.
Les morceaux de source forment une partition numérique sans chevauchement ni
lacune, et le résidu après la ligne de bord est nul. La plus petite marge des
tests de disponibilité des 192 lignes premières vaut
`0.0436732617874311`, à q=13. Les marges originales et non minimales diffèrent
de moins de `3×10^-47` sur le diagnostic à 1000, alors que leurs noyaux
diffèrent réellement.

## Coût quadratique : redistribution, conservation totale

| Plafond | Coût hors bord original | Coût hors bord non minimal | Coût du bord original | Coût du bord non minimal |
|---:|---:|---:|---:|---:|
| 10 | 0.105542367898 | 0.131429180397 | 0.089711168463 | 0.063824355964 |
| 100 | 0.249173918234 | 0.271811257733 | 0.158469130942 | 0.135831791443 |
| 1000 | 0.381728513014 | 0.402757858073 | 0.238466738909 | 0.217437393851 |

La somme totale, bord compris, est un invariant exact des marginales finies :

\[
\sum_j\int(u-x_j)^2\theta_j(du)
=\int u^2\mu_U(du)-\sum_jc_jx_j^2.
\]

Il suffit de développer le carré et d'utiliser `∫uθ_j=c_jx_j`. La variante
déplace donc du coût vers les lignes hors bord ; elle ne diminue pas le coût
quadratique total. À 1000 ce total commun vaut `0.620195251923872`, avec un
écart numérique entre les deux calculs inférieur à `4×10^-48`.

## Portée de la variante et fichiers

La réserve radiale `inf S_N(t)/t` du premier rapport caractérise l'ombre
minimale complète, dont le raccord initial est lui-même une ombre. Elle ne
caractérise pas la masse en 0 pour ce raccord non minimal : ici cette masse
est nulle dès la première ligne, tandis que le minimum radial original
reste positif au préfixe 1000. L'obstruction via un atome en 0 laissé à tout
rang fini concernait ce choix minimal précis. La variante retire cet obstacle
initial sans établir de borne uniforme sur les largeurs futures ni résoudre
les tests de disponibilité à tous les rangs.

- `nonminimal_shadow_sweep.py` : script autonome à 60 chiffres, argument X
  facultatif, 1000 par défaut.
- `nonminimal_x10_*`, `nonminimal_x100_*`, `nonminimal_x1000_*` : noyaux JSON,
  résumé JSON et lignes CSV, distinguant raccord, premiers q>2 et bord.
- `compare_nonminimal.py` et `nonminimal_comparison.json` : comparaison des
  résultats historiques préservés, bilan des coûts et stabilité des préfixes.

```sh
PYTHONPATH=/workspace/scratch/72030dde7ad1/v635_runtime_deps \
  "$CODEX_PRIMARY_RUNTIME_PYTHON" nonminimal_shadow_sweep.py 1000
```

Le raccord initial et toutes les lignes ultérieures sont recalculés ; le
script n'importe aucun des anciens noyaux.
