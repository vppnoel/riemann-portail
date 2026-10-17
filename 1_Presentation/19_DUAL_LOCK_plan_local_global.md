# V6 — DUAL-LOCK : plan de verrouillage local / global

**Statut :** prochaine branche, non encore testée  
**Origine :** conclusion de PRIME-LOCK

## 1. Le problème désormais isolé

PRIME-LOCK sépare proprement deux classes :

- Davenport–Heilbronn [DH36b] [DH36a] possède une symétrie fonctionnelle de type Riemann mais échoue au verrou eulérien local ;
- les témoins Steinhaus possèdent un verrou multiplicatif local exact mais aucune structure fonctionnelle/archimédienne canonique comparable n'est fournie par le protocole.

Zeta et le Dirichlet \(L(s,\chi_5)\) possèdent les deux.

La prochaine question est donc une question **d'interaction** :

\[
\boxed{
\text{structure locale aux premiers}
\quad\leftrightarrow\quad
\text{symétrie globale de la complétion}.
}
\]

## 2. Ce que DUAL-LOCK ne doit pas faire

Il ne suffit pas de multiplier deux scores :

\[
\text{score Euler}\times\text{score fonctionnel}.
\]

Ce serait une classification fabriquée par construction.

Il faut chercher un objet où les deux structures interviennent dans **la même identité** ou dans **le même opérateur**.

## 3. Candidats admissibles

### A. Canal explicite local–archimédien

Construire deux termes à partir d'une même fonction test :

- côté local : poids des nombres premiers / puissances de premiers issus de \(-F'/F\) ;
- côté archimédien : terme gamma/conducteur imposé par la complétion.

Puis rechercher une contrainte de balance ou de signature qui ne se réduit pas à une somme séparée de deux défauts.

### B. Compression d'une formule explicite sans injecter les zéros

Utiliser une forme test dont le côté « premiers + archimédien » est calculable directement, puis étudier une matrice de compressions ou une inertie. Toute utilisation implicite de la positivité équivalente à RH doit être signalée immédiatement.

### C. Déformation adversariale

Partir d'un objet verrouillé localement et déformer progressivement la structure globale, ou inversement, afin d'identifier quel terme d'interaction réagit en premier.

## 4. Matrice de témoins

| objet | verrou local | verrou global | rôle |
|---|---:|---:|---|
| zeta | oui | oui | cible de calibration |
| \(L(s,\chi_5)\) | oui | oui | contrôle positif non-zeta |
| Davenport–Heilbronn | non | oui | témoin « global sans local » |
| Steinhaus | oui | non défini/canonique | témoin « local sans global » |

## 5. Règle de succès

Une construction DUAL-LOCK ne survit que si elle produit un **terme d'interaction intrinsèque** qui :

1. est calculable sans supposer RH ;
2. n'est pas nul par définition ;
3. distingue les deux contrôles croisés ;
4. ne se réduit pas simplement à « Euler-produit oui/non » ;
5. possède une interprétation mathématique indépendante de la métaphore.

## 6. Première tâche

Chercher dans la formule explicite, la dérivée logarithmique complétée et les compressions de Weil un candidat minimal où **prime powers et terme archimédien apparaissent dans la même forme bilinéaire**.

Ce document est un plan de branche, pas un résultat.

## 7. Premier candidat concret : compression arithmétique de la formule explicite

La formule de Guinand–Weil [Gui48] fournit déjà exactement le type d'objet recherché : pour une même fonction test, elle additionne

- un terme **archimédien** provenant du facteur gamma et du conducteur ;
- un terme **local** provenant de \(\Lambda_F(n)\), donc des nombres premiers et puissances de premiers lorsque l'Euler-produit existe ;
- et elle est égale à un terme spectral sur les zéros.

Pour zeta, une forme schématique est

\[
\mathcal W(h)
=
A_\infty(h)
-2\sum_{n\ge1}\frac{\Lambda(n)}{\sqrt n}g(\log n)
+\text{termes de pôle},
\]

avec \(g\) transformée de Fourier/Mellin de \(h\).

C'est donc un **objet local–global intrinsèque**, pas la juxtaposition de deux scores.

### Candidat D0

Choisir une famille finie de fonctions test \(g_1,\dots,g_m\) et construire la compression hermitienne

\[
M_{ij}^{(F)}
=
\mathcal W_F(g_i*\widetilde g_j)
\]

calculée **uniquement côté arithmétique + archimédien**, sans introduire les zéros dans le calcul.

Comparer ensuite l'inertie et le rang effectif pour :

- zeta ;
- \(L(s,\chi_5)\) ;
- Davenport–Heilbronn.

### Garde-fou

La positivité complète de la forme de Weil [Wei52] est déjà équivalente à RH. DUAL-LOCK ne gagnerait donc rien à « redémontrer » ce critère.

La seule question V6 admissible est plus petite :

> **Une compression finie choisie indépendamment des zéros possède-t-elle un invariant d'inertie ou de rang qui sépare les structures locales/globales avant la limite complète ?**

Cette question rejoint directement le mécanisme de compression/inertie mis en avant par les travaux de 2026, mais doit être traitée comme une expérience de structure, pas comme une nouvelle voie de preuve annoncée.

---

## Mise à jour V6.3 — branche exécutée

Le plan ci-dessus a été implémenté. La compression finie côté arithmétique + archimédien produit des témoins d'inertie négatifs pour Davenport–Heilbronn sans utiliser ses zéros dans la construction ; le contrôle eulérien apparié reste positif sur les témoins confirmés. Voir `21_DUAL_LOCK_RESIDU_SOMBRE_resultats.md`.

L'analyse des composantes a en outre isolé le mécanisme **Résidu sombre** : le signe négatif final est un reliquat de cancellation local/global, avec des facteurs d'amplification de l'ordre de 10 à 70 sur les témoins confirmés. Le statut de DUAL-LOCK passe donc de `PLAN` à `TESTÉ / SURVIT COMME DÉTECTEUR D'INERTIE`.

<!-- references:debut -->

## Références

Format : [clé] auteurs, *titre*, publication, lien. Fiches complètes et état de vérification : document 42 (registre des sources).

- [DH36a] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series*. J. London Math. Soc. 11 (1936), no. 3, 181–185. <https://doi.org/10.1112/jlms/s1-11.3.181> — partiellement vérifié
- [DH36b] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series. II*. J. London Math. Soc. 11 (1936), no. 4, 307–312. <https://doi.org/10.1112/jlms/s1-11.4.307> — partiellement vérifié
- [Gui48] A. P. Guinand. *A summation formula in the theory of prime numbers*. Proc. London Math. Soc. (2) 50 (1948), 107–119. — non vérifié
- [Wei52] A. Weil. *Sur les « formules explicites » de la théorie des nombres premiers*. Comm. Sém. Math. Univ. Lund, vol. suppl. dédié à M. Riesz (1952), 252–265. <https://en.wikipedia.org/wiki/Weil%27s_criterion> — partiellement vérifié

<!-- references:fin -->
