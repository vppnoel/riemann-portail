# Instructions pour une relecture indépendante

## But

Un referee externe doit pouvoir lire le package sans accepter les conclusions du programme par défaut. La mission est de vérifier séparément : **correction**, **priorité**, **portée**.

## Bloc A — Théorème A

1. Vérifier L1–L5.
2. Fournir une référence exacte pour la formule de Perron tronquée utilisée en L6.
3. Refaire le calcul du reste pour `x=N+1/2`.
4. Vérifier les bornes uniformes sur `zeta'/zeta` et sa dérivée à droite de `Theta+epsilon`.
5. Traiter séparément `Theta=1/2` et `Theta=1`.
6. Vérifier l'argument de prolongement holomorphe autour d'un zéro supposé.
7. Comparer la priorité avec les critères RH via fonctions de von Mangoldt généralisées.

**Sortie demandée :** `A-valid / A-fixable / A-false`, avec ligne exacte du premier point problématique.

## Bloc B — Théorème B

1. Vérifier l'identité Mellin–Plancherel.
2. Recalculer le facteur local `1/(4 eta^3)` d'un double pôle.
3. Refaire l'estimation de queue sans utiliser le document comme source.
4. Vérifier la sommabilité de `S` avec multiplicités.
5. Vérifier les échanges de limites `eta->0` puis `Y->infinity`.
6. Donner la version exacte de Karamata employée.
7. Rechercher une antériorité de type Cramér / generalized von Mangoldt.

**Sortie demandée :** même classification et bibliographie précise.

## Bloc C — Proposition C

1. Vérifier le calcul à nombre fini de zéros.
2. Identifier les hypothèses minimales pour sommer les termes contenant `b_rho`.
3. Vérifier la condition sur les paires proches.
4. Préciser le sens de « presque périodique » pour la limite infinie.
5. Ne pas utiliser GUE comme résultat prouvé.

## Bloc numérique

1. Installer `requirements.txt` dans un environnement propre.
2. Exécuter `python tests/test_identities.py` : cible actuelle 21/21.
3. Exécuter les scripts explicitement cités dans la synthèse.
4. Vérifier les checksums.
5. Considérer tous les résultats numériques comme des contrôles d'implémentation, pas comme de l'évidence pour RH.

## Bloc bibliographique

Utiliser `docs/SOURCES_RH_PROGRAMME.md` comme liste de départ. Toute entrée marquée « à vérifier » doit être lue dans sa source primaire avant citation technique ou revendication de nouveauté.
