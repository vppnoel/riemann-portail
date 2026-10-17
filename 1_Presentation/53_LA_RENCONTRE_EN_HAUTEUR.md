# V6.28 — Axe A : la Rencontre à n en hauteur

**Date :** 11 octobre 2026  
**Statut :** calcul fait, avec des prévisions écrites avant (`data/prevision_v628_hauteur.md`, 23 h 35 UTC). Les trois sont fausses. Le modèle testé, la formule de taille effective prolongée aux N réels, donne des densités négatives : il est inutilisable à ces hauteurs. Un fait mesuré, net, le remplace.  
**Demande de l'auteur :** « Go » (premier coup du navigateur).

## 1. La question

Au document 43, aucun triplet de zéros de ζ ne tombait dans la zone serrée (deux écarts consécutifs sous 0,5), là où le noyau sinus en attend 4,4. L'axe A devait vérifier si cet écart vient de l'effet de hauteur finie de Bogomolny et al. [BBLM06]. L'outil était la formule det[D~N~] du doc. 43, prise à la taille effective N~eff~(γ) = log(γ/2π)/√(12Λ), avec Λ = 1,57314.

## 2. Le modèle ne tient pas

La formule n'a de sens que pour des écarts plus petits que N. J'ai donc gardé les origines où N~eff~ ≥ 1 : 806 zéros entre 486 et 1 500, avec N~eff~ entre 1,00 et 1,26.

| | Prévision | Résultat | Verdict |
|---|---|---|---|
| A1 | avec N = N~eff~, la masse attendue de la zone serrée tombe sous 1,5 | la formule donne une masse **négative** (−2,2) : à N non entier proche de 1, det[D~N~] n'est pas une densité | **fausse** (modèle invalide) |
| A2 | un N unique ajusté sur la zone x + y ≤ 1 vaut 1,0 à 1,5 | **aucun** triplet dans cette zone : l'ajustement n'a rien à ajuster | **fausse** (mal posée) |
| A3 | le même N redonne le nombre de paires serrées | 6 observées ; noyau sinus 11,2 ; N~eff~ 2,8 ; N ajusté 0 | **fausse** |

C'est la confirmation de ce que le doc. 41 signalait déjà : le développement de Bogomolny et al. est utilisé ici **hors de son domaine**. Il vaut pour N~eff~ grand, c'est-à-dire à des hauteurs bien supérieures. Le prolonger à N ≈ 1 ne donne pas un modèle.

## 3. Le fait mesuré : le trou à trois

Le calcul a fait apparaître une chose plus simple et plus nette. On compte les **triples de zéros consécutifs qui tiennent dans moins d'un écart moyen** (portée u~i+2~ − u~i~ < 1, en unités dépliées) :

| Objet | Zéros | Triples de portée < 1 | Attendu (noyau sinus) | Plus petite portée | Paires d'écart < 0,19 (attendu) |
|---|---|---|---|---|---|
| ζ (t ≤ 1 500) | 1 070 | **0** | 15,6 | 1,009 | 3 (12,6) |
| L(χ5) (t ≤ 600) | 494 | **0** | 7,2 | 1,166 | 0 (5,8) |
| L(Δ) (t ≤ 1 500) | 2 139 | **3** | 31,1 | 0,789 | 4 (25,2) |
| contrôle : CUE(20), CUE(60), simulés | — | fraction 0,0152 et 0,0142 | 0,0146 | — | — |

**Ce que montre le tableau.**

- Les matrices aléatoires de taille finie (20 ou 60) suivent le noyau sinus. **La taille finie seule ne crée pas le trou.**
- Les zéros des trois fonctions L, à ces hauteurs, sont **beaucoup plus rigides** que le noyau sinus.
  - ζ : aucun triple serré sur 1 070 zéros, pour 15,6 attendus. La probabilité de Poisson de ne rien voir est d'environ 2·10^−7^.
  - L(χ5) : aucun sur 7,2 attendus.
  - Δ, en degré 2 : 3 sur 31.
- C'est le même sens que le déficit de paires des docs 40 et 41, en plus marqué.

**Ce que cela n'est pas.** Ce n'est pas une contradiction avec le noyau sinus, qui est une loi limite à grande hauteur. Les calculs à très grande hauteur, ceux d'Odlyzko, le retrouvent (cité de mémoire). C'est une mesure à basse hauteur, où les zéros des fonctions L se comportent comme un réseau presque cristallin. Le corpus ne sait pas encore quelle loi la décrit.

## 4. Suite

- **Lire Bogomolny et al. pour de vrai** (coût 1). Il s'agit de prendre leur correction effective, pour la corrélation de paires et pour les écarts consécutifs, plutôt que la formule prolongée, et de vérifier si elle prévoit ce trou à trois aux hauteurs du corpus.
- **Prévoir le trou à trois de Δ à partir de celui de ζ.** Le degré 2 a un conducteur analytique plus grand, donc une hauteur « effective » plus grande. Si la rigidité est un effet de hauteur effective, Δ doit être moins rigide que ζ, ce qu'on voit (3 contre 0). La loi exacte reste à trouver.

## 5. Démontré, mesuré, supposé

| | Énoncé |
|---|---|
| **Démontré** | Pour N non entier, det[D~N~] n'est pas toujours positif : ce n'est pas une densité (constaté ici, −2,2 sur la zone). |
| **Mesuré** | Triples serrés : ζ 0 pour 15,6 ; L(χ5) 0 pour 7,2 ; Δ 3 pour 31,1. Le CUE de taille 20 ou 60 suit le noyau sinus. |
| **Supposé** | Que le trou à trois soit un effet de hauteur (ou de conducteur), qui disparaît quand la hauteur croît. |

## 6. Lecture selon l'hypothèse de travail

Les zéros les plus bas se tiennent à distance les uns des autres plus fermement que le hasard le plus ordonné qu'on connaisse, celui des matrices unitaires. Ce surplus d'ordre est le plus fort là où les nombres premiers sont encore peu nombreux. L'hypothèse de l'auteur y trouverait une piste : la structure qui « rend RH nécessaire » se voit mieux là où elle a le moins de matière pour se cacher.

<!-- references:debut -->

## Références

Format : [clé] auteurs, *titre*, publication, lien. Fiches complètes et état de vérification : document 42 (registre des sources).

- [BBLM06] E. Bogomolny, O. Bohigas, P. Leboeuf, A. G. Monastra. *On the spacing distribution of the Riemann zeros: corrections to the asymptotic result*. J. Phys. A 39 (2006), 10743–10754 ; arXiv:math/0602270. <https://arxiv.org/abs/math/0602270> — vérifié en ligne

<!-- references:fin -->
