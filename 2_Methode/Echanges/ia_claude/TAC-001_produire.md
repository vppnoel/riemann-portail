# TAC-001 — Auditer noyaux et couplages du candidat

*Programme Riemann V6.59 · genre : lier_instance · rôle : coordinateur · cycle 1 · statut : assignee*

## Contexte

Corpus de recherche sur l'hypothèse de Riemann (RH). RH n'est pas démontrée et ne doit pas être présentée comme telle. Lire d'abord `README.md` (« À lire d'abord »), puis `2_Methode/Pilotage/CIBLAGE.md`. Méthode : prévision écrite avant, témoins contraires, portée explicite.

## Question

Lier une instance exécutable à l'étude Bellman « Auditer noyaux et couplages du candidat » : objet, domaine, entrées avec empreintes, commande bornée, issues possibles et vérificateur.

## Entrées (empreintes SHA-256 au moment de la création)

- `2_Methode/Pilotage/bellman_contrats_v643.json` — `5ab0ffb2575117c3…`

**Objet :** contrat d’étude · **Domaine :** Proposed bounded study; an assessed candidate is not a uniform sign theorem

## Sortie attendue

Contrat d’exécution complet, soumis à l’auteur ; aucun lancement.

## Critère de rejet (écrit avant)

Aucune instance réalisable dans la durée déclarée ([1, 2] lots H) : l'étude reste hors exécution.

**Budget déclaré :** [1, 2]

## Contrôles anti-circularité

- Tester l'énoncé sur Davenport–Heilbronn : s'il y fonctionne mot pour mot, il ne peut pas servir pour RH.
- Le confronter à l'analogue des corps de fonctions (RH connue) : une positivité sans image là-bas n'est pas une preuve.
- Aucune donnée qui injecte la réponse (zéros ou modes fabriqués puis retrouvés).
- Exiger un témoin négatif : la méthode doit détecter un défaut connu, au bon endroit.
- Signaler tout énoncé équivalent à RH : une équivalence n'est un progrès que si elle rend un outil nouveau accessible, à nommer.
- Toute constante numérique est donnée avec son erreur et ce qu'elle teste réellement.

## Ce que vous devez faire

1. Avant tout calcul ou raisonnement : `python -B 2_Methode/Pilotage/taches.py prevoir TAC-001 --par ia:claude --texte "…"` (ce que vous attendez, et ce qui vous donnerait tort).
2. N'écrire que dans `2_Methode/Depot/TAC-001/`. Aucun autre fichier du corpus n'est modifié.
3. Y déposer `RAPPORT.md` avec les sections : Prévision, Méthode, Résultat, Portée, Critère de rejet, Statut proposé ; plus les programmes, données et journaux utiles.
4. `python -B 2_Methode/Pilotage/taches.py deposer TAC-001 --par ia:claude --statut-propose STATUT` (statut parmi : demontre, classique, mesure, ouvert, partiel, conditionnel, obstacle, diagnostic, outil, refute ; ajouter `--equivalent-rh` si l'énoncé obtenu entraîne RH).
5. Ne rien affirmer au-delà de la portée établie ; un échec documenté est un résultat.

*La décision (acceptée, rejetée, à reprendre) appartient à l'auteur. L'intégration au corpus suit ensuite le protocole du pilotage : prévision conservée, preuve et portée, bilan, indicateur réexaminé.*
