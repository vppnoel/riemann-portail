# TAC-009 — Gram de Nyman–Beurling sur des différences d'échelle

*Programme Riemann V6.59 · genre : investigation · rôle : explorateur · cycle 1 · statut : a_reprendre*

## Contexte

Corpus de recherche sur l'hypothèse de Riemann (RH). RH n'est pas démontrée et ne doit pas être présentée comme telle. Lire d'abord `README.md` (« À lire d'abord »), puis `2_Methode/Pilotage/CIBLAGE.md`. Méthode : prévision écrite avant, témoins contraires, portée explicite.

## Question

Construire K^NB_ij = ⟨C_i, C_j⟩ dans L²(0,1), où C_i est la différence normalisée ρ_{θ_{i+1}} − ρ_{θ_i} sur une grille logarithmique θ_i = e^{−u_i} (critique « tomographie de phase », § 3–4). Son spectre ou son rang effectif voit-il autre chose que la géométrie des dilatations ? Pour un test différentiel, utiliser la version généralisée de Nyman–Beurling aux séries de Dirichlet (à vérifier sur l'original) pour ζ, L(s, χ₅) et un analogue de Davenport–Heilbronn.

## Entrées (empreintes SHA-256 au moment de la création)

- `4_Archives/recus/2026-10-17/critique_tomographie_de_phase_MPT.txt` — `de0b10d829fad9c6…`
- `1_Presentation/12_Annulation_du_pole.pdf` — `a2a71e16cb13a7a5…`
- `1_Presentation/15_TOMO_DH_formalisation.md` — `f6de7d28ef6663df…`

**Objet :** matrice de Gram K^NB et sa version brute G^NB · **Domaine :** grille (u_0, Δu, m) déclarée dans la prévision

## Sortie attendue

Calcul de G^NB et K^NB (formule fermée ou quadrature contrôlée) ; spectre et rang effectif ; comparaison avec un témoin purement géométrique (même construction, partie fractionnaire remplacée par une fonction sans arithmétique) et, si la généralisation est vérifiée, avec L(χ₅) et l'analogue DH ; références vérifiées sur l'original (dont la structure « block-Hankel » citée par la critique).

## Critère de rejet (écrit avant)

Si le spectre de K^NB coïncide (à la précision du calcul) avec celui du témoin géométrique, ou si ζ et l'analogue DH ne se séparent pas plus que deux tirages du témoin, l'observable ne voit que les dilatations : statut « obstacle ». Le document 12 a déjà montré que la projection de Nyman–Beurling se ramène à l'énergie Q : un résultat qui ne fait que la retrouver est classé « classique », pas nouveau.

## Témoin

Témoin géométrique sans arithmétique ; doc. 12 (projection NB = énergie Q).

**Budget déclaré :** 1 lot H

## Contrôles anti-circularité

- Tester l'énoncé sur Davenport–Heilbronn : s'il y fonctionne mot pour mot, il ne peut pas servir pour RH.
- Le confronter à l'analogue des corps de fonctions (RH connue) : une positivité sans image là-bas n'est pas une preuve.
- Aucune donnée qui injecte la réponse (zéros ou modes fabriqués puis retrouvés).
- Exiger un témoin négatif : la méthode doit détecter un défaut connu, au bon endroit.
- Signaler tout énoncé équivalent à RH : une équivalence n'est un progrès que si elle rend un outil nouveau accessible, à nommer.
- Toute constante numérique est donnée avec son erreur et ce qu'elle teste réellement.

## Ce que vous devez faire

1. Avant tout calcul ou raisonnement : `python -B 2_Methode/Pilotage/taches.py prevoir TAC-009 --par ia:chatgpt-sol-6.1-max --texte "…"` (ce que vous attendez, et ce qui vous donnerait tort).
2. N'écrire que dans `2_Methode/Depot/TAC-009/`. Aucun autre fichier du corpus n'est modifié.
3. Y déposer `RAPPORT.md` avec les sections : Prévision, Méthode, Résultat, Portée, Critère de rejet, Statut proposé ; plus les programmes, données et journaux utiles.
4. `python -B 2_Methode/Pilotage/taches.py deposer TAC-009 --par ia:chatgpt-sol-6.1-max --statut-propose STATUT` (statut parmi : demontre, classique, mesure, ouvert, partiel, conditionnel, obstacle, diagnostic, outil, refute ; ajouter `--equivalent-rh` si l'énoncé obtenu entraîne RH).
5. Ne rien affirmer au-delà de la portée établie ; un échec documenté est un résultat.

*La décision (acceptée, rejetée, à reprendre) appartient à l'auteur. L'intégration au corpus suit ensuite le protocole du pilotage : prévision conservée, preuve et portée, bilan, indicateur réexaminé.*
