# V6.26 — J3b : le Frobenius de caractéristique un

**Date :** 11 octobre 2026  
**Statut :** lecture ciblée, portée corrigée en V6.34 après relecture de l'introduction et des sections 2.3 et 3 de *The Arithmetic Site*. Le test ne fournit pas la transplantation directe de Stepanov recherchée. Il laisse ouvertes les autres structures du site et du carré. La route de Weil reste active.  
**Demande de l'auteur :** « Bon, on fait le suivant, J3 ou J3b. »

## 1. La question

Le document 49 a dit ce qu'il faut à une fonction auxiliaire de Stepanov. Il faut, dans l'espace des fonctions, un élément de très haut degré (x^p^) qui coïncide en chaque point avec un élément simple (x), et que les dérivations ne voient pas. Sur les entiers, un tel élément existe pour chaque nombre premier séparément, mais pas pour tous à la fois.

J3b demande : **le Frobenius de « caractéristique un » de Connes–Consani fournit-il cet élément, pour tous les premiers à la fois ?**

**Prévision** (écrite en V6.24, avant la lecture) : « Non sous cette forme : en caractéristique un, les dérivations ne s'annulent pas ; il faudra un autre mécanisme que Stepanov. »

## 2. Ce que disent les sources

| Source | Ce qu'on y lit (résumé, ou extraits lus) |
|---|---|
| Connes–Consani, *The Arithmetic Site* (2014) [CC14] | Le faisceau de structure est le semi-anneau tropical ℕ̄ = (ℕ ∪ {∞}, inf, +), sur le topos dual du monoïde ℕ×. Sur les valeurs et les points, le **Frobenius** est Fr~λ~ ∈ Aut(ℝ₊^max^), **pour tout réel λ > 0** : c'est l'action d'échelle. Les points au-dessus de [0, 1]~max~ forment l'espace des classes d'adèles (quotienté). La distribution de comptage donne ζ complète. Les correspondances de Frobenius sont réalisées **dans le carré du site**, où agissent les endomorphismes Fr~n,m~. |
| Connes–Consani, *Characteristic 1, entropy and the absolute point* (2009) [CC09] | La construction de Witt est adaptée à la caractéristique un. L'addition s'y déforme par l'**entropie**, avec une « température ». |
| Marcolli–Thorngren, *Thermodynamic semirings* (2011) [MT11] | Ce cadre ne définit pas de dérivations. L'analogue de la dérivée y est le **sous-différentiel** de la transformée de Legendre. |
| Connes–Consani, Riemann–Roch pour Spec Z (2022, 2024) [CC22], [CC24] | Riemann–Roch sur la « courbe » Spec Z, sur la base absolue (doc. 47). |

## 3. L'analyse

**En caractéristique p**, le Frobenius x ↦ x^p^ :

- est additif ;
- n'est **pas** inversible comme application de l'algèbre des fonctions, car x^p^ est de degré p ;
- annule les dérivations (p = 0).

C'est cette **perte d'information infinitésimale** qui fait chuter le rang des conditions d'annulation et permet la fonction auxiliaire (docs 48, 49).

**En caractéristique un**, le Frobenius x ↦ x^λ^ :

- est additif ;
- est un **automorphisme pour tout λ > 0 du semi-corps tropical des valeurs et de l'action sur les points** ;
- en coordonnées logarithmiques, est la multiplication par λ. Pour ce modèle élémentaire, les pentes sont dilatées et aucune identité analogue à D(x^p^)=0 n'a été construite.

Cela suffit à constater l'échec de la transplantation directe testée. Cela ne démontre aucune impossibilité générale d'un mécanisme infinitésimal en caractéristique un : l'inversibilité d'une action sur les points ne règle pas la structure des espaces de fonctions. Dans le carré du site, Connes–Consani définissent aussi des **endomorphismes Fr~n,m~ des faisceaux de structure**, puis des correspondances Ψ(λ) (introduction et §3 de [CC14]). Ces objets doivent être distingués des automorphismes sur les valeurs. La prévision est donc tenue seulement dans le modèle d'échelle étudié.

**Ce que font Connes et Consani à la place.** Ils ne prennent pas la route de Bombieri (la courbe seule, avec une fonction auxiliaire). Ils prennent **celle de Weil** : le carré du site, avec ses correspondances de Frobenius pour tout λ, et l'espoir d'y démontrer une positivité, un analogue de l'indice de Hodge. C'est exactement la « surface virtuelle » du document 46. Le corpus y a mesuré une seule direction positive pour ζ, calculée depuis les premiers, et des directions en trop pour DH.

## 4. Décision

- **La transplantation directe de J3 étudiée ici est écartée.** Aucun espace de fonctions et aucun opérateur de jets n'y ont produit l'effondrement de rang nécessaire. La piste peut être rouverte avec un espace, un endomorphisme et un opérateur infinitésimal explicitement définis ; l'action sur les points seule ne suffit pas à trancher.
- **L'axe J revient à la route de Weil.** Le coup suivant est **J6, « Le carré, en continu »**. Le document 46 a établi l'indice de Hodge virtuel avec une seule largeur de fonction-test (a = 0,04) et un seul pas (h = 0,01). J6 vérifie qu'il tient pour toute la famille continue des correspondances de Frobenius (λ = e^t^) : plusieurs largeurs, plusieurs pas, des fenêtres plus longues, avec DH comme témoin. Si la signature tient partout, la forme virtuelle se comporte comme celle d'une vraie surface dans tout le domaine mesurable. Coût : 1.
- J4 (le genre virtuel) reste ouvert.

## 5. Démontré, mesuré, supposé

| | Énoncé |
|---|---|
| **Démontré (connu)** | Automorphismes Fr~λ~ sur les valeurs et les points, endomorphismes Fr~n,m~ sur le carré [CC14] ; en caractéristique p, D(x^p^)=0. |
| **Constaté dans le modèle étudié** | L'action d'échelle élémentaire ne fournit pas les jets invisibles requis par la construction testée. |
| **Ouvert** | Un autre espace de fonctions pourrait-il fournir un mécanisme d'existence ? La route de Weil est poursuivie, sans être déclarée seule possible. |

## 6. Lecture selon l'hypothèse de travail

Dans la construction de Stepanov en caractéristique p, l'annulation des jets d'ordre inférieur à p permet de réduire le rang des conditions. La V6.34 en donne un lemme et une borne explicites dans le document 58. En caractéristique un, aucune structure remplissant ce rôle n'a été construite dans le corpus. La positivité sur le carré reste une autre voie à étudier ; cette décision de travail ne vaut pas théorème d'exclusivité.

<!-- references:debut -->

## Références

Format : [clé] auteurs, *titre*, publication, lien. Fiches complètes et état de vérification : document 42 (registre des sources).

- [CC09] A. Connes, C. Consani. *Characteristic 1, entropy and the absolute point*. arXiv:0911.3537 (2009). <https://arxiv.org/abs/0911.3537> — vérifié en ligne
- [CC14] A. Connes, C. Consani. *The Arithmetic Site*. C. R. Math. Acad. Sci. Paris 352, n° 12 (2014), 971–975 ; arXiv:1405.4527. <https://arxiv.org/abs/1405.4527> — partiellement vérifié
- [CC22] A. Connes, C. Consani. *Riemann–Roch for Spec Z (compactifié d'Arakelov)*. arXiv:2205.01391 (v1 mai 2022, v2 mars 2023). <https://arxiv.org/abs/2205.01391> — vérifié en ligne
- [CC24] A. Connes, C. Consani. *Riemann–Roch for the ring Z*. C. R. Math. Acad. Sci. Paris 362 (2024), 229–235 ; DOI 10.5802/crmath.543. <https://comptes-rendus.academie-sciences.fr/mathematique/articles/10.5802/crmath.543/> — vérifié en ligne
- [MT11] M. Marcolli, R. Thorngren. *Thermodynamic semirings*. arXiv:1108.2874 (2011). <https://arxiv.org/abs/1108.2874> — partiellement vérifié

<!-- references:fin -->
