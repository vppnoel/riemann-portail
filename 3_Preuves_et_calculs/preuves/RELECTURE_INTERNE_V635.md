# V6.35 — Relectures constructive et critique

**Date :** 12 octobre 2026. **Nature :** deux relectures internes par agents ; ce document ne constitue pas une expertise humaine ni une publication.

## Contrôle de la preuve

La lecture constructive a rédigé la preuve complète dans LEMME_TOUR_ET_SPECTRE_V635.md. La lecture critique a contrôlé :

- la définition directe des dérivées de Hasse et la règle du produit, sans coefficient binomial supplémentaire ;
- l'identité polynomiale pour la puissance de la cubique et sa borne de degré ;
- l'indépendance de l'espace sans quotient par x^q−x ;
- la factorisation des blocs de jets, leur borne de rang et l'existence du noyau ;
- le comptage par multiplicité, la torsion et la constante 10 uniforme, petits corps compris ;
- la justification de rationalité par Riemann–Roch indépendamment de Hasse ;
- le produit des deux racines inverses, la domination d'un module trop grand et les zéros dans la variable s ;
- la séparation entre cubiques singulières, courbes elliptiques lisses et zêta des entiers.

Référence vérifiée : Milne, *Elliptic Curves*, deuxième édition (2021), I §4, théorème 4.13 et formule (8), pp. 35–36 ; IV §9, proposition 9.9, théorème 9.10 et remarque 9.11(a), pp. 155–156. La preuve de rationalité n'utilise pas la borne de Hasse présentée plus tôt dans le livre.

La lecture constructive a aussi vérifié les paramètres pour tous les entiers impairs de 29 à 10001. Ce contrôle fini complète l'inégalité universelle écrite ; il ne la remplace pas.

## Contrôle indépendant sur F27

La lecture critique a utilisé sa propre arithmétique par coefficients modulo 3 et réduction par u^3+2u+1, puis une construction directe des jets depuis les 66 polynômes :

| Contrôle | Résultat |
|---|---|
| Toutes les additions et multiplications (729 couples chacune) | Concordantes |
| Inverses et a^27=a | Concordants |
| Matrice directe contre construction factorisée | Identique |
| Élimination indépendante | Rang 51, noyau 15 |
| Reconstruction du témoin | Coefficients identiques, degré 93 |
| Divisions successives par x−a | Multiplicité minimale 4 sur les 13 points |

Les comptages directs F25=27, F125=108, F49=55 et F343=380 ont également été recoupés.

## Deux corrections appliquées

1. Le module du corps est normalisé modulo p et débarrassé des coefficients dominants nuls avant de déterminer sa dimension. Le degré demandé est contrôlé. Cela évite un degré apparent incohérent et une division polynomiale invalide.
2. Lorsque S est vide, un témoin constant non nul est valide. Le certificat vérifie donc sa non-nullité, sans exiger un degré positif.

Ces cas limites sont couverts par les nouveaux tests. Les fichiers de certificats conservent les coefficients complets de chaque témoin et permettent de les reconstruire.

## Conclusion des relectures

Aucune faille restante n'a été trouvée dans les points contrôlés. La méthode est classique ; aucune nouveauté historique n'est revendiquée. La caractéristique 2 et les genres supérieurs ne sont pas traités ici. L'implémentation des tables est limitée à q≤1024, sans limiter la preuve. Les objets nécessaires au transfert vers la zêta de Riemann restent ouverts.
