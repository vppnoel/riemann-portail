# V6.51 — Reconstruction documentée des contrôles manquants

Date de reconstruction : **15 octobre 2026**. Corpus de recherche de Vincent P. P. NOËL ; programmation et rédaction assistées.

**Ce paquet est séparé du corpus global V6.55. Aucun fichier du ZIP global n’a été remplacé.** Les deux originaux manquants ne sont pas retrouvés. Le programme et son journal portent donc de nouveaux noms explicites.

## Les deux fichiers reconstruits

| Fichier | Rôle |
|---|---|
| `v651_verifier_pistes_globales_RECONSTRUIT.py` | Nouveau programme exécutable reproduisant les témoins finis décrits dans le document76 |
| `v651_pistes_globales_resultats_RECONSTRUITS.json` | Nouveau journal réellement calculé, avec fractions exactes, bornes d’intervalles et provenances |

Ouvrir **`LIRE_D_ABORD.html`** pour le résumé lisible et les liens vers toutes les pièces. Le PDF et la source LaTeX du document76 sont copiés sans modification dans `sources/`.

## Ce qui est attesté et ce qui est reconstruit

Les textes, paramètres et limites proviennent du document76 conservé, notamment les sections1.1, 2.3, 2.4, 3 et5.1. Le protocole et l’état V6.51 conservés sont aussi joints. Les deux modules de calcul originaux `symbolic_weil_family.py` et `prime_centered_bridge.py` sont copiés à l’identique et servent au recoupement optionnel.

**Le code de contrôle, le schéma du journal et les cas de matrices ci-dessous sont nouveaux.** Aucune correspondance avec les octets, le schéma ou la liste complète des tests du programme perdu n’est revendiquée. Le répertoire `4_Archives/recus/V651/` cité par le document76 n’a pas été retrouvé dans le corpus disponible ; ses rapports ne sont pas recréés comme des originaux.

Deux revues parallèles ont été lancées pendant cette reconstruction mais ont été interrompues par la limite d’utilisation. Aucun rapport indépendant achevé n’en est revendiqué. Le recoupement de deux calculs ne remplace pas cette relecture.

## Calculs reproduits et leur sens

### 1. Une liste fixe de puissances premières est insuffisante

On reprend exactement la famille polynomiale du dossier :

\[
w_S(x)=(1-x^2/S^2)^4\quad (|x|\le S),\qquad f_S=(\partial_x^2-1/4)w_S,
\]

prolongée par zéro. Ces tests sont dans H¹ ; on ne les présente pas comme C∞. Les annulations aux bords et l’identité polaire sont contrôlées en arithmétique rationnelle exacte.

Pour la **seule liste fixe** A={2,3,4,5,7}, avec le poids de4 égal à log(2)/2, le programme encadre le majorant

\[
\frac{Q_A(f_S)}{m(f_S)}\le
\frac{(131/8)\|f'_S\|_2^2-(25/6)m(f_S)-2\sum_{q\in A}c_q h_{f_S}(\log q)}{m(f_S)}.
\]

| S | Valeur indicative du majorant calculé | Conclusion rigoureuse du journal |
|---|---:|---|
|4|11,6880897411|Inconclusif : un majorant positif ne prouve pas la positivité de Q_A|
|8|−6,5570931433|Q_A est négatif pour ce test|
|16|−9,4709332978|Q_A est négatif pour ce test|
|32|−9,9042533588|Q_A est négatif pour ce test|
|64|−9,9917771903|Q_A est négatif pour ce test|
|128|−10,0123799578|Q_A est négatif pour ce test|

Les décimales de ce tableau servent à lire le résultat. Les fractions des bornes dans le JSON font autorité. La constante25/6 est un minorant volontairement grossier de C₀ ; rien ne prouve que l’ancien programme utilisait exactement ce choix.

**Ceci ne donne pas un contre-exemple à RH.** Q_A omet les autres puissances premières actives. Leur compensation est précisément l’obligation globale qui reste ouverte. Ces supports ne sont pas un domaine de vérification de RH.

### 2. L’enveloppe de sortie ne ferme pas la voie globale

Le document76 donne alpha_S ≥ c₂/J(S), où c₂=log(2)/√2 et

\[
J(S)=\operatorname{atanh}(e^{-S/2})+\arctan(e^{-S/2}).
\]

| S | c₂/J(S), valeur indicative | Seuil du document76 reproduit |
|---|---:|---:|
|4|1,8106740980|>1,81|
|8|13,3800699959|>13,38|
|16|730,5270855338|>730,52|

Le programme encadre **ce minorant**, pas la valeur exacte du supremum alpha_S ni la norme de l’opérateur arithmétique. Le passage à l’essentiel supremum repose sur la définition analytique de l’enveloppe du document74 : la contribution du premier2 vaut au moins2c₂ dans un voisinage du centre, tandis que le potentiel est continu.

### 3. Contrôles supplémentaires, nouveaux et explicitement limités

- Une matrice Toeplitz hermitienne3×3 a tous ses mineurs principaux2×2 égaux à7/16, mais le vecteur complexe (1,i,−1) donne −3/2. C’est un exemple algébrique générique : **ce n’est pas une matrice de Weil calculée depuis les premiers**. Il montre pourquoi tous les tests à deux paquets ne suffisent pas.
- Un bloc de Schur singulier possède une pseudo-dette1 mais un témoin de valeur−3 lorsque le couplage sort de l’image du bloc. Cela vérifie la nécessité de la garde d’image ; ce n’est pas un certificat de la dette duale du corpus.
- Les annulations polaires du symbole B_p sont vérifiées algébriquement pour p=2,3,5,7. Des coefficients finis de la formule de commutateur sont aussi contrôlés. Aucune limite en norme sur tous les premiers n’en est déduite.

## Pourquoi les bornes sont contrôlées

Le calcul principal n’utilise que Python standard : `Fraction`, entiers et intervalles dyadiques. Chaque opération d’intervalle arrondit sa borne basse vers le bas et sa borne haute vers le haut.

- log(x) est encadré par la série positive2∑r^(2k+1)/(2k+1), r=(x−1)/(x+1), avec une queue géométrique explicite ;220 termes.
- √x est encadré par une racine carrée entière à l’échelle dyadique.
- exp(S/2) est encadré par100 termes de Taylor et une queue géométrique ; on inverse ensuite l’intervalle positif.
- J(S)=2∑z^(4k+1)/(4k+1), z=exp(−S/2), est encadré avec32 termes et une queue explicite.
- L’inégalité d’énergie utilise2∑(2n+1/2)⁻³ ≤16+(1/4)(1+∫₁^∞x⁻³dx)=131/8.
- C₀=log(8π)+γ+π/2 >9/2>25/6 découle de π>3, log24>3 et γ≥1−log2>0. Les bornes numériques nécessaires sont calculées ; la formule de Machin et la comparaison intégrale de la constante d’Euler sont les identités analytiques employées.

Le journal livré utilise160 bits. Les mêmes décisions ont été retrouvées à80 et256 bits. Un calcul `mpmath1.3.0` à320 bits, utilisant les modules originaux pour les polynômes, a été entièrement contenu dans les intervalles livrés. C’est un recoupement de calcul, pas une formalisation logicielle complète ni une relecture indépendante.

## Exécuter

Calcul autonome, Python3 récent, sans installer de bibliothèque :

```bash
python3 -B v651_verifier_pistes_globales_RECONSTRUIT.py
```

Recoupement optionnel après installation de `requirements-optionnels.txt` :

```bash
python3 -B v651_verifier_pistes_globales_RECONSTRUIT.py --cross-check-mpmath
```

Le journal est déterministe pour une même précision et la même option de recoupement. Une exécution sans cette option remplace le champ `cross_check` par `executed:false`. Le programme refuse Python `-O`, car les assertions font partie des contrôles.

## Ce que cela ne remet pas en état

Les preuves analytiques des lemmes d’exhaustion, de couverture Toeplitz et de densité par deux filtres restent celles du document76 : elles ne sont pas certifiées par ces cas finis. L’algorithme du dual restreint, le signe universel des matrices et la compensation de tous les premiers restent ouverts. **Ni preuve de RH, ni nouveau progrès global sur son signe.**

Cette reconstruction rend de nouveau exécutables les témoins finis décrits publiquement. Elle ne permet pas de remplacer l’étiquette « original manquant » par « original retrouvé » dans l’inventaire global.
