# TAC-010 — Lecture adverse de la note sur la preuve annoncée de RH (Alpöge, 2026)

*Programme Riemann V6.59 · genre : verification_temoin · rôle : auditeur · cycle 1 · statut : deposee*

## Contexte

Corpus de recherche sur l'hypothèse de Riemann (RH). RH n'est pas démontrée et ne doit pas être présentée comme telle. Lire d'abord `README.md` (« À lire d'abord »), puis `2_Methode/Pilotage/CIBLAGE.md`. Méthode : prévision écrite avant, témoins contraires, portée explicite.

## Énoncé à vérifier

La note NOTE_ALPOGE_2026.md, rédigée par Claude (modèle d'Anthropic, l'employeur d'Alpöge : conflit d'intérêts à garder en tête), résume l'annonce du 20 novembre 2026, l'état de la vérification et une lecture du « pourquoi » de la preuve. Chaque affirmation factuelle est-elle exacte et sourcée sur une source primaire ou de premier rang (code Lean, en particulier src/Statements.lean et les définitions Mathlib RiemannHypothesis, riemannZeta, DirichletCharacter.LFunction ; guide d'architecture ; notes de Rubinstein et de Zhang ; déclarations des communautés Lean et Mathlib) ? La lecture en quatre étapes (borne unilatérale, intégrité, multiplicité fabriquée, équilibre en √x) est-elle fidèle, ou simplifie-t-elle au point de fausser ?

*Relecture à l'aveugle : l'identité du producteur n'est pas donnée. Lire les pièces et les données avant la conclusion du rapport.*

## Entrées (empreintes SHA-256 au moment de la création)

- `NOTE_ALPOGE_2026.md` — `055409aad61bb32a…`
- `README_EN.md` — `89ebe7acd960e22d…`

**Objet :** NOTE_ALPOGE_2026.md, affirmation par affirmation · **Domaine :** faits au 22 novembre 2026 et après ; lecture de la preuve telle que publiée

## Sortie attendue

Tableau : affirmation, source primaire consultée (lien, date de consultation), verdict (exacte, imprécise, fausse, non vérifiable), correction proposée. Liste séparée des points où la lecture du « pourquoi » diverge des expositions publiées. Toute évolution depuis le 22 novembre (réfutation, erreur trouvée, version lisible, relecture humaine) signalée en tête.

## Critère de rejet (écrit avant)

Si une affirmation factuelle de la note est fausse ou non sourçable, ou si la lecture en quatre étapes contredit une exposition publiée sur un point essentiel, la note est à corriger : statut « refute » pour le point concerné. Une vérification qui ne cite que des articles de presse, sans source primaire, n'est pas recevable.

## Témoin

Les sources citées par la note elles-mêmes ; un point volontairement vérifiable (taille de la formalisation, axiomes utilisés).

**Budget déclaré :** 1 lot H

## Contrôles anti-circularité

- Tester l'énoncé sur Davenport–Heilbronn : s'il y fonctionne mot pour mot, il ne peut pas servir pour RH.
- Le confronter à l'analogue des corps de fonctions (RH connue) : une positivité sans image là-bas n'est pas une preuve.
- Aucune donnée qui injecte la réponse (zéros ou modes fabriqués puis retrouvés).
- Exiger un témoin négatif : la méthode doit détecter un défaut connu, au bon endroit.
- Signaler tout énoncé équivalent à RH : une équivalence n'est un progrès que si elle rend un outil nouveau accessible, à nommer.
- Toute constante numérique est donnée avec son erreur et ce qu'elle teste réellement.

## Pièces déposées

- `2_Methode/Depot/TAC-010/RAPPORT.md`

**Statut proposé :** refute · **Équivalent à RH déclaré :** non

## Ce que vous devez faire

1. Rejouer ce qui peut l’être (programmes, calculs) et confronter le résultat au critère de rejet écrit avant.
2. Appliquer les contrôles anti-circularité ci-dessus ; chercher circularités, équivalences à RH déguisées, erreurs de signe, hypothèses cachées.
3. Vérifier que la portée annoncée n'excède pas ce qui est établi, et que le statut proposé est le bon.
4. Écrire `2_Methode/Depot/TAC-010/verification/VERIFICATION.md` (ce qui a été rejoué, ce qui ne l'a pas été, écarts).
5. `python -B 2_Methode/Pilotage/taches.py verifier TAC-010 --par ia:claude --verdict conforme|non_conforme --note "…"`. Vous ne pouvez pas être le producteur.

*La décision (acceptée, rejetée, à reprendre) appartient à l'auteur. L'intégration au corpus suit ensuite le protocole du pilotage : prévision conservée, preuve et portée, bilan, indicateur réexaminé.*
