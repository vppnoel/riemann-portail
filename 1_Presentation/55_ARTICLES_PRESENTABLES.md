# V6.30 — Les articles présentables

**Date :** 11 octobre 2026  
**Statut :** deux articles en anglais, au format standard (LaTeX, classe amsart), avec la lettre d'accompagnement. Aucun n'a encore été relu par un spécialiste.  
**Demande de l'auteur :** « Prépare les articles présentables. » La lettre commence par « Cher Professeur », sans nom.

## 1. Pourquoi ce format

Un article de mathématiques suit une forme fixe :

- un résumé ;
- des énoncés numérotés (théorème, proposition, corollaire), chacun suivi de sa preuve ;
- une section numérique reproductible ;
- des figures 2D standard ;
- une bibliographie.

Le vocabulaire de travail du corpus n'y figure pas : métaphores, navigateur, indicateur. Le contenu est celui du corpus, et rien n'y est ajouté.

## 2. Les deux articles

| | Article 1 | Article 2 |
|---|---|---|
| Titre | *A mean square with double poles at the zeros of ζ: the rightmost zero, a Cramér-type asymptotic, and a criterion for simple zeros* | *Prime-side Weil forms in finite windows: a numerical Hodge-index test with a Davenport–Heilbronn control* |
| Longueur | 10 pages | 6 pages |
| Contenu | Théorème A (méthode standard, sans revendication de nouveauté) ; Théorème B (Cramér pour un pôle double) ; corollaire B′ (sous RH : constante = 4κ/3 ⟺ zéros simples) ; identité exacte avec la famille de Nyman–Beurling ; tableau de Q(X) jusqu'à 10⁸ | Dictionnaire C × C ↔ formule explicite, en dimension finie ; proposition d'inertie pour les faux polynômes (1 + r/2 directions positives), vérifiée sur 425 courbes et 220 faux ; 180 réglages pour ζ, L(χ5) et DH, chacun vérifié côté zéros |
| Corpus | docs 12, 37, 45 ; dossiers de relecture A et B | docs 46, 52 |
| Valeur | le candidat sérieux | une note expérimentale ; apport modeste, dit dans le texte |

Les figures ont été refaites à partir des données du corpus. Pour l'article 1, Q(X) a été recalculé jusqu'à 10⁷ par un crible indépendant : il concorde avec le corpus sur tous les chiffres imprimés. Les scripts sont dans `articles/figures/`.

## 3. Une correction trouvée en préparant l'article 2

Le document 52 dit : « DH : directions en trop dès X ≥ 61 (39/39) ». C'est exact, mais ce n'est pas un seuil.

- Dès X ≈ 56, 8 des 9 réglages montrent déjà 2 directions en trop.
- Le seuil se situe donc entre X ≈ 20 et X ≈ 56, intervalle qui n'a pas été échantillonné.

Décompte exact : aucune direction en trop dans les 12 réglages où X ≤ 20,3 ; des directions en trop dans 47 des 48 réglages où X ≥ 55,7.

## 4. Ce qu'il reste à faire

1. Vérifier les références citées de mémoire, sur les originaux. La liste est dans `articles/LISEZMOI_ARTICLES.md`.
2. Compléter l'adresse électronique si vous le souhaitez.
3. Envoyer la lettre et les deux PDF à un spécialiste. C'est la relecture humaine que le navigateur exige pour tout gain de niveau 7 ou plus.

## 5. Démontré, mesuré, supposé

| | Énoncé |
|---|---|
| **Démontré (relu en interne)** | Théorèmes A et B ; corollaire B′ ; identité de Nyman–Beurling ; propositions de l'article 2 (dictionnaire, inertie, congruence). |
| **Mesuré** | Tableaux et figures des deux articles. |
| **Supposé** | Que B et B′ soient nouveaux sous cette forme. La recherche s'est limitée au web. |

## 6. Lecture selon l'hypothèse de travail

L'idée de l'auteur devient ici un énoncé que d'autres peuvent vérifier. Une seule fonctionnelle, construite sur les entiers qui ont au plus deux facteurs premiers, lit à la fois la position des zéros, par son exposant, et leur simplicité, par sa constante. Le « plus grand » qui rendrait RH nécessaire n'est pas démontré. Ce qui l'est, c'est que les nombres premiers portent déjà ces deux informations sur les zéros.
