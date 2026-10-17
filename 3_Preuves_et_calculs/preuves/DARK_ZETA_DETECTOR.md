# DARK-ZETA / TOMO — note technique du premier détecteur

Cette note accompagne `1_Presentation/17_DARK_ZETA_premier_detecteur_resultats.md`.

## Statut

Diagnostic numérique reproductible. Aucun énoncé ici n'est une preuve de RH ni une implication vers RH.

## Objets

Le pipeline part des coefficients de Dirichlet `a_F(n)` et construit les coefficients de log-dérivée `Lambda_F`, puis

`c_F = Lambda_F * Lambda_F - Lambda_F log n`

avec le terme `+ 2 gamma Lambda` pour ζ en raison du pôle simple en 1. Le signal cumulé est

`C_F(t)=sum_{n<=t} c_F(n)`.

La représentation logarithmique est

`g_F(u)=exp(-u/2) C_F(exp(u))`.

## Contrôle exact TOMO-2

Le Gram de translations circulaires dépend seulement de `|FFT(g)|^2`. Par conséquent un surrogate obtenu par randomisation des phases en conservant le module du FFT doit redonner exactement le même Gram. Le test automatisé impose une erreur maximale < 1e-10 ; les runs principaux donnent ~1e-15.

## TOMO-3

L'estimateur est une bicoherence segmentée :

`|mean(X_k X_l conj(X_{k+l}))|^2 / (mean(|X_k X_l|^2) mean(|X_{k+l}|^2))`.

Le nombre fini de segments induit un niveau nul non nul ; la comparaison significative est donc faite avec 32 surrogats à phases randomisées conservant le spectre de puissance de chaque objet.

## Contrôles

- ζ : multiplicatif + produit d'Euler + pôle ;
- L_chi5 : multiplicatif + produit d'Euler, sans pôle ;
- DH : même voisinage analytique/conducteur, combinaison non multiplicative ;
- Steinhaus : complètement multiplicatif synthétique, sans équation fonctionnelle imposée ;
- chemin chi5 -> DH : dégradation contrôlée de multiplicativité.

## Résultat négatif principal

TOMO-3 ne suit pas de façon stable le défaut multiplicatif sur le chemin chi5 -> DH : la corrélation change de signe ou disparaît avec N. De plus, les observations de ζ, L_chi5 et DH restent proches des distributions obtenues par phase randomisée.

## Résultat positif limité

L'entropie TOMO-2 suit fortement le défaut multiplicatif **sur la famille appariée chi5 -> DH**, avec rho de Spearman ~0.88 à 0.96 selon l'échelle. Ce phénomène n'est pas universel : des suites Steinhaus totalement multiplicatives donnent des entropies très différentes malgré un défaut nul.

## Décision

- conserver TOMO-2 comme diagnostic spectral multiscalaire ;
- rétrograder le bispectre brut de C_F ;
- ne pas escalader automatiquement à des polyspectres supérieurs ;
- changer de canal lors de la prochaine expérience.
