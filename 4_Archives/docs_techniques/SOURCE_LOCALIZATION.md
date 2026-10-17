# V4.1 — Localisation de sources et traitement de signal appliqués aux zéros de zeta

**Statut : [EXP]/[NUM]/[GAP].** Ce module ne modifie aucun théorème A/B/C et ne constitue pas une nouvelle preuve de RH. Il formalise une branche expérimentale issue des méthodes de localisation de sources : moyennage préalable, filtrage spatial/spectral, ondelettes, covariance et problème inverse.

## 1. Modèle direct

Dans la variable logarithmique `t=log x`, une forme schématique de la formule explicite est

\[
r(t)=e^{-t/2}(\psi(e^t)-e^t-\text{termes connus})
   \simeq -\sum_\rho \frac{e^{(\rho-1/2)t}}{\rho}.
\]

Pour `rho=beta+i gamma`, un zéro agit comme une source modale

\[
s_{\beta,\gamma}(t)=e^{(\beta-1/2)t}e^{i\gamma t}.
\]

Sous RH, `beta=1/2` et le mode n'a pas d'enveloppe exponentiellement croissante. Une source avec `beta>1/2` possède une croissance `exp((beta-1/2)t)`.

**Interprétation inverse :** les nombres premiers / coefficients arithmétiques constituent les données observées ; les zéros sont les paramètres latents ; la formule explicite est le modèle direct.

## 2. Analogie avec la localisation de sources de potentiels évoqués

| Localisation de sources | Programme zeta |
|---|---|
| capteurs / potentiels de surface | coefficients premiers / signal explicite |
| sources corticales | zéros `rho=beta+i gamma` |
| matrice de lead field | dictionnaire `s_{beta,gamma}(t)` |
| bruit physiologique / instrumental | troncature + zéros hors bande + bords + interférences |
| moyennage des essais | lissage par fonctions tests / filtres multiples |
| CSD / Laplacien | dérivation / Laplacien régularisé en `t=log x` |
| ondelettes temps-fréquence | localisation de `gamma`, estimation de croissance `beta-1/2` |
| GLS / minimum norm / MVDR | inversion pondérée par covariance |
| résolution / identifiabilité | constante d'observabilité / plus petite valeur singulière |

Le terme « bruit » doit être utilisé avec prudence : il est ici essentiellement **déterministe, coloré et corrélé**, et contient une partie du signal spectral que l'on cherche justement à identifier.

## 3. Prétraitement multicanal

Le module `src/source_localization.py` implémente trois briques simples :

1. `gaussian_average` — moyennage/lissage préalable ;
2. `regularized_laplacian` — réponse `omega^2/(1+lambda omega^2)`, analogue d'un Laplacien régularisé ;
3. `morlet_demodulated_envelope` — analyse locale autour d'une fréquence `gamma`, puis `envelope_growth_rate` pour estimer `beta-1/2` sur un modèle simple.

L'objectif n'est pas de lisser arbitrairement le signal : plusieurs résolutions doivent être conservées afin de ne pas détruire les hautes fréquences, comme dans une analyse multirésolution de potentiels évoqués.

## 4. Carte de localisation `(beta,gamma)`

On introduit un dictionnaire de sources

\[
a_{\beta,\gamma}(t)=e^{(\beta-1/2)t}e^{i\gamma t}.
\]

Pour des données `y`, le score de matched filtering / GLS est

\[
P(\beta,\gamma)
 = \frac{|a^*R^{-1}y|^2}
 {(a^*R^{-1}a)(y^*R^{-1}y)}.
\]

`R` joue le rôle de covariance des résidus. Dans ce programme, `R` n'est pas supposée provenir d'un bruit probabiliste blanc : elle peut être une covariance déterministe construite à partir des résidus de troncature, de fenêtres ou d'un modèle nul.

Le module fournit `matched_filter_map` pour produire une carte `P(beta,gamma)`.

## 5. Critère analytique réellement intéressant

Une détection numérique de `beta=1/2` jusqu'à une hauteur finie ne prouve rien sur RH. Le passage d'un outil de localisation à une preuve demanderait une **visibilité uniforme** :

\[
\|A s\|_{\mathrm{obs}} \ge c\,\|s_{\mathrm{off}}\|,
\qquad c>0,
\]

pour toute composante correspondant à `beta>1/2`, avec une constante qui ne s'effondre pas lorsque la hauteur `|gamma|`, la dimension du dictionnaire et la fenêtre d'observation augmentent.

Équivalents possibles :

- borne de frame ;
- constante d'observabilité ;
- borne inférieure sur une plus petite valeur singulière ;
- propriété de stabilité d'un problème de super-résolution ;
- positivité spécifique au produit d'Euler.

`visibility_metrics` calcule seulement la version **finie** de ce diagnostic. Elle ne fournit pas la borne uniforme requise.

## 6. Ce qui existe déjà dans la littérature

Cette direction n'est pas vierge :

- Main, Mandelshtam, Wunner et Taylor (1997) utilisent l'**harmonic inversion / filter diagonalization** sur le signal associé à zeta et récupèrent des milliers de zéros ;
- la formule explicite de Guinand–Weil est déjà un banc de filtres rigoureux : le choix de la fonction test règle la localisation entre côté premiers et côté zéros ;
- Connes interprète les zéros critiques comme un **spectre d'absorption**, les éventuels zéros non critiques comme des résonances ;
- Connes–Moscovici (2022) étudient un opérateur prolate dont le comportement spectral ultraviolet reproduit celui des carrés des zéros.

La proposition V4.1 n'est donc pas « inventer l'analyse spectrale des zéros ». Le point potentiellement distinct est de réunir explicitement dans un même protocole :

\[
\text{moyennage multicanal}
+\text{analyse temps-fréquence}
+\text{covariance}
+\text{localisation }(\beta,\gamma)
+\text{test d'observabilité uniforme}.
\]

La nouveauté éventuelle de cette combinaison reste à vérifier bibliographiquement.

## 7. Tests de rejet obligatoires

Avant toute interprétation :

1. **Davenport–Heilbronn** — contrôle positif : la carte doit pouvoir localiser des sources avec `beta != 1/2` sur une fonction possédant effectivement des zéros hors ligne.
2. **Injection synthétique** — ajouter un mode artificiel `(beta0,gamma0)` et mesurer le seuil de détection en fonction de la fenêtre et du filtrage.
3. **Résolution** — rapprocher deux `gamma` et suivre la plus petite valeur singulière du dictionnaire.
4. **Croissance en hauteur** — vérifier si la visibilité décroît avec `gamma`, comme le suggère déjà le rapport signal/bruit observé dans V3.9.
5. **Robustesse aux filtres** — une « source » ne doit pas être un artefact d'une seule fenêtre ou d'un seul Laplacien.

## 8. Décision scientifique

Ce module est conservé comme **nouveau banc expérimental** et non comme reprise de l'attaque directe de RH. Il ne doit être promu en priorité analytique que si l'un des tests suivants réussit :

- découverte d'une borne d'observabilité non triviale qui exploite irréversiblement le produit d'Euler ;
- connexion avec une positivité de type Weil ;
- amélioration démontrable d'un benchmark de densité / grandes valeurs ;
- formulation inverse donnant un résultat intermédiaire nouveau, plus faible que RH.

Sinon, la localisation de sources reste un excellent outil de diagnostic et de visualisation, mais pas un mécanisme de preuve.

## 9. Références de départ

- J. Main, V. A. Mandelshtam, G. Wunner, H. S. Taylor, *Harmonic inversion as a general method for periodic orbit quantization*, arXiv:chao-dyn/9709009 (1997). Le papier utilise explicitement la fonction zeta comme exemple et annonce la récupération de plusieurs milliers de zéros par filter diagonalization.
- E. Bombieri, *Remarks on Weil's quadratic functional in the theory of prime numbers, I*, avec une formulation de la formule explicite de Guinand–Weil par fonctions tests.
- A. Connes, *Trace formula in noncommutative geometry and the zeros of the Riemann zeta function*, arXiv:math/9811068 / Selecta Mathematica : zéros critiques comme spectre d'absorption, zéros non critiques éventuels comme résonances.
- A. Connes, H. Moscovici, *The UV prolate spectrum matches the zeros of zeta*, PNAS 119 (2022), e2123174119.

Voir aussi `docs/SOURCES_RH_PROGRAMME.md`.
