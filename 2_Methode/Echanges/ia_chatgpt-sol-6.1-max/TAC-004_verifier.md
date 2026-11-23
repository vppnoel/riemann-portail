# TAC-004 — Deux filtres : approximants et norme de forme

*Programme Riemann V6.59 · genre : investigation · rôle : explorateur · cycle 1 · statut : deposee*

## Contexte

Corpus de recherche sur l'hypothèse de Riemann (RH). RH n'est pas démontrée et ne doit pas être présentée comme telle. Lire d'abord `README.md` (« À lire d'abord »), puis `2_Methode/Pilotage/CIBLAGE.md`. Méthode : prévision écrite avant, témoins contraires, portée explicite.

## Énoncé à vérifier

Comment construire effectivement les approximants de la grammaire déjà démontrée, avec leur erreur de forme ?

*Relecture à l'aveugle : l'identité du producteur n'est pas donnée. Lire les pièces et les données avant la conclusion du rapport.*

## Entrées (empreintes SHA-256 au moment de la création)

- `1_Presentation/76_COMPLEMENT_COUP_DOUBLE.md` — `33b0c9d1fcf3d160…`

**Objet :** — · **Domaine :** celui de la question ; à préciser dans la prévision

## Sortie attendue

Algorithme d’approximation et contrat d’erreur, ou obstruction précise. Cette tâche ne prouve pas le signe. Complément 76 : continuité du candidat, défaut mixte, garde d’image de Schur ; six contrôles abstraits exacts, aucun calcul de Suzuki ni signe global obtenu. Seconde passe : raccord exact et couverture par translation établis ; prolongement pair suspendu ; 12 contrôles abstraits exacts. Pas de minoration arithmétique universelle. V6.57 : diagnostic de phases sur les matrices arithmétiques V644 ; certificat adaptatif 44 cellules sur une fenêtre déjà traitée. Ni certificat infini supplémentaire ni loi universelle.

## Critère de rejet (écrit avant)

La suite ne converge pas dans la topologie exigée ; le transfert de signe est alors refusé.

## Témoin

Convergence L² seule, moments perdus, ou contrôle qui dépend du support sans borne.

## Contrôles anti-circularité

- Tester l'énoncé sur Davenport–Heilbronn : s'il y fonctionne mot pour mot, il ne peut pas servir pour RH.
- Le confronter à l'analogue des corps de fonctions (RH connue) : une positivité sans image là-bas n'est pas une preuve.
- Aucune donnée qui injecte la réponse (zéros ou modes fabriqués puis retrouvés).
- Exiger un témoin négatif : la méthode doit détecter un défaut connu, au bon endroit.
- Signaler tout énoncé équivalent à RH : une équivalence n'est un progrès que si elle rend un outil nouveau accessible, à nommer.
- Toute constante numérique est donnée avec son erreur et ce qu'elle teste réellement.

## Pièces déposées

- `2_Methode/Depot/TAC-004/RAPPORT.md`
- `2_Methode/Depot/TAC-004/p1_bezout_diophantien.py`
- `2_Methode/Depot/TAC-004/p1_resultats.json`
- `2_Methode/Depot/TAC-004/p2_approximants_nu.py`
- `2_Methode/Depot/TAC-004/p2_resultats.json`
- `2_Methode/Depot/TAC-004/p2_resultats_passe1.json`

**Statut proposé :** partiel · **Équivalent à RH déclaré :** non

## Ce que vous devez faire

1. Rejouer ce qui peut l’être (programmes, calculs) et confronter le résultat au critère de rejet écrit avant.
2. Appliquer les contrôles anti-circularité ci-dessus ; chercher circularités, équivalences à RH déguisées, erreurs de signe, hypothèses cachées.
3. Vérifier que la portée annoncée n'excède pas ce qui est établi, et que le statut proposé est le bon.
4. Écrire `2_Methode/Depot/TAC-004/verification/VERIFICATION.md` (ce qui a été rejoué, ce qui ne l'a pas été, écarts).
5. `python -B 2_Methode/Pilotage/taches.py verifier TAC-004 --par ia:chatgpt-sol-6.1-max --verdict conforme|non_conforme --note "…"`. Vous ne pouvez pas être le producteur.

*La décision (acceptée, rejetée, à reprendre) appartient à l'auteur. L'intégration au corpus suit ensuite le protocole du pilotage : prévision conservée, preuve et portée, bilan, indicateur réexaminé.*
