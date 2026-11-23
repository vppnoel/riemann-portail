# Vérification indépendante — TAC-007, deuxième dépôt

*Codex — `ia:chatgpt-sol-6.1-max` · 18 octobre 2026 · producteur : `ia:claude`.*

**Verdict : conforme au statut proposé `partiel`, comme étude numérique et diagnostic d'architecture. Aucun certificat sur tout l'espace n'est obtenu.**

## Révision, intégrité et reprise

Dépôt enregistré le 18 octobre à 00:12:58 UTC, lu sur `main` au commit `5fae60de138d63a4e75649b8dcc2b33cdfe14ea9`. Le fil #3 est lu en entier. Les sept pièces et le document d'entrée 81 correspondent aux empreintes SHA-256 enregistrées. Le premier avis, conservé dans `VERIFICATION_PREMIER_DEPOT.md`, portait sur le dépôt précédent ; il n'est pas le verdict sur cette reprise.

Les contrôles manquants lors du premier examen ont été ajoutés : forme de DH, corps de fonctions, témoins négatifs. La présente revue les exécute et ajoute des contrôles indépendants. Elle n'est pas une acceptation par Vincent NOËL.

## Rejeu effectif

Les trois programmes du producteur sont exécutés sans modification dans une copie de travail. **Le fichier p1_resultats.json a été supprimé dans cette copie avant lancement**, car le programme ignore les calculs déjà enregistrés. Les neuf cas de P1 sont donc recalculés, pas simplement relus.

Les résultats effectifs sont conservés dans `rejeu_codex.json`. `audit_codex.py` compare tous les champs mathématiques ; seules les durées sont exclues. Les tolérances y sont déclarées. Les résidus proches de zéro des calculs multiprécision ne sont pas traités comme des bornes dirigées.

Environnement : Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, pandas 2.2.3, mpmath 1.3.0, SymPy 1.14.0. Les versions de Python/NumPy/pandas diffèrent de la CI du dépôt. Le backend multiprécision reste mpmath : ce n'est pas une validation croisée par Arb ou par une bibliothèque d'intervalles indépendante.

## P1 — Une mesure reproduite, pas un minorant

Les neuf valeurs déposées sont retrouvées aux chiffres affichés. La marge paire à N = 64 vaut 5,34694614142·10⁻¹² pour K = 48, et 5,35029972448·10⁻¹² pour K = 96. La marge impaire N = 48 vaut 9,85526381624·10⁻¹⁰. Le critère de rejet « marge mesurée sous 10⁻¹³ » n'est pas atteint dans les cas calculés.

L'audit vérifie indépendamment la projection en éliminant une coordonnée du moment, puis en résolvant un problème généralisé avec sa matrice de Gram. À N = 12, L = 4/5, K = 64 et 70 chiffres, il retrouve la projection Householder à mieux que 10⁻⁵⁵ ; le résidu spectral est inférieur à 10⁻⁶⁰.

**Limites obligatoires :** les valeurs sont celles de matrices de Galerkin avec quadrature non certifiée. Dans le problème idéal, une restriction de Rayleigh–Ritz fournit un majorant de l'infimum ; les nombres calculés n'en deviennent pas des bornes rigoureuses sans contrôle de quadrature et d'arrondi. La stabilité jusqu'à N = 64 ne certifie ni la limite en N ni une coercivité de la queue.

**Cache de Gauss.** Le module du corpus mémorise ses nœuds par n, sans la précision. Les passages de 60 à 80 chiffres réutilisent donc certains nœuds calculés à 60 chiffres. L'audit compare ces nœuds à des nœuds recalculés à 80 chiffres : écart maximal 4,77·10⁻⁶² pour K = 48, très inférieur à la marge. Cela ne change pas les chiffres reproduits ; la future construction d'un certificat devra vider le cache ou l'indexer par précision. Le test actuel ne constitue pas un rejeu intégral de toutes les quadratures à 80 chiffres.

## P2 — Budget du schéma fixé

Le programme P2 et son résultat sont reproduits à partir du JSON V6.50. Le code source cité confirme les formules des budgets : erreur de quadrature proportionnelle à T·h² à paramètres fixés, modèle γ_n d'assemblage, table linéaire et erreur de poids.

Avec la cible 5·10⁻¹², la loi posée donne 3,861616053·10⁹ cellules et un budget d'assemblage de 0,0611431. **Ces budgets ne permettent pas de certifier la marge visée dans ce schéma d'estimation.** Ce constat ne démontre pas une impossibilité pour toute implémentation binary64, toute sommation ou toute autre architecture.

L'affirmation de taille de tête « au moins 100 modes » reste une prévision non vérifiée. La route tête–queue et son complément de Schur n'ont pas été construits. La fiche ne devient pas un certificat par cette proposition de suite.

## C1 — Formule générale et contrôle DH

Le rejeu retrouve la validation sur les 988 zéros de L(χ₅), aux deux fenêtres, ainsi que l'échec net du mauvais facteur archimédien. Les zéros servent à cette validation séparée ; ils n'alimentent ni les matrices de ζ/DH ni le calcul de leur marge.

Pour DH, les matrices paires calculées à N = 32 et 48 sont positives. À N = 48, leurs plus petites valeurs sont 0,00659256787208 sur le secteur fini entier et 1,62217358554 sur le noyau du moment.

**La formulation « DH reste positif à 0,8 » doit être lue ici au niveau de ces matrices finies.** Leur positivité, seule, ne prouve pas celle de la forme de DH sur tout L²[−0,8,0,8]. Le contrôle établit que cette expérience finie ne discrimine pas ζ et DH par le signe ; il ne fournit pas un certificat DH. C'est la portée retenue par cet avis et celle à conserver lors d'une éventuelle intégration.

## C2 — Corps de fonctions : signe recoupé exactement

Le comptage des points et les comparaisons arithmétique/spectral sont rejoués. Les comptes 9, 27, 108, 675, 3069, 15552 sont cohérents avec le compte direct N₁ = 9 et la récurrence du polynôme de Frobenius. Le calcul géométrique du producteur précède la comparaison spectrale ; la vraie courbe n'est plus alimentée par ses valeurs propres.

L'audit ajoute un contrôle **rationnel exact** du signe, sans valeurs propres approchées : base redimensionnée q^(k/2)(δ_k ± δ_−k), élimination de la contrainte du pôle, puis tous les mineurs principaux de la forme restreinte. Les matrices et mineurs sont joints au JSON d'audit.

- Vraie courbe : forme positive ou semi-définie positive, pour M = 1, 2, 3 et les deux parités ; les petits nombres négatifs ~10⁻⁵⁰ du JSON sont des erreurs numériques autour de zéro.
- Faux genre 1, a = 5 : positif dans le secteur pair, négatif dans le secteur impair dès M = 2.
- Faux genre 2, P(T) = 1 + 11T² + 25T⁴ : négatif dans le secteur pair dès M = 2, et dans le secteur impair à M = 3.

Les faux polynômes sont des contrôles fabriqués déclarés comme tels, pas des courbes existantes. Leur rôle est de vérifier une capacité de détection ; ils ne servent pas de données de départ à une preuve sur ζ.

## C3 — Défauts injectés

Le rejeu retrouve la positivité pour δ = 0, la négativité pour δ = 0,1, 0,01 et 0,001, et le seuil mesuré δ ≈ 2,11215·10⁻⁵. Pour la perturbation de Λ(2), le seuil observé est 1,490231·10⁻¹⁰ contre 1,4928154·10⁻¹⁰ au premier ordre : écart 0,173 %, inférieur aux 5 % prévus.

Ce sont des résultats du modèle fini testé, sans encadrement d'un seuil du problème infini. Ils montrent la sensibilité du calcul à ces deux défauts. Ils ne démontrent pas que tout certificat, quelle que soit son organisation, devrait imposer la même précision relative à chacun des termes premiers.

## Verdict, portée acceptée par la vérification et suite

Les motifs de non-conformité du premier dépôt sont levés. **Conforme comme résultat `partiel`**, avec la portée explicitée ci-dessus : mesure stable sur les cas finis testés, incompatibilité des budgets du schéma fixé avec la cible, et contrôles adverses reproduits. Ni certificat nouveau sur tout l'espace, ni preuve de positivité infinie pour DH, ni obstruction universelle, ni conséquence RH.

Une acceptation de l'auteur peut porter sur **cette étude partielle**, en conservant ces limites dans le texte intégré. Pour poursuivre vers un certificat, ouvrir une fiche distincte ; annoncer la borne de queue et le mécanisme de certification avant calcul. Cette ouverture n'est pas nécessaire pour accepter l'étude déjà réalisée.
