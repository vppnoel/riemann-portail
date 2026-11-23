# TAC-006 — Pli sur une fibre à coefficient A fixé

*Programme Riemann V6.59 · genre : investigation · rôle : explorateur · cycle 1 · statut : deposee*

## Contexte

Corpus de recherche sur l'hypothèse de Riemann (RH). RH n'est pas démontrée et ne doit pas être présentée comme telle. Lire d'abord `README.md` (« À lire d'abord »), puis `2_Methode/Pilotage/CIBLAGE.md`. Méthode : prévision écrite avant, témoins contraires, portée explicite.

## Énoncé à vérifier

Une direction candidate porte-t-elle un vrai pli transversal sur la fibre qui conserve A ?

*Relecture à l'aveugle : l'identité du producteur n'est pas donnée. Lire les pièces et les données avant la conclusion du rapport.*

## Entrées (empreintes SHA-256 au moment de la création)

- `1_Presentation/66_UN_PLI_CERTIFIE_ET_SA_PAIRE.md` — `c11bef23320d92f9…`

**Objet :** — · **Domaine :** celui de la question ; à préciser dans la prévision

## Sortie attendue

Certificat local ou obstacle documenté. Cette branche ne garantit pas la loi globale de Weil.

## Critère de rejet (écrit avant)

Un jet nul non certifié ne donne pas un zéro double ; préserver les pertes et les indéterminations.

## Témoin

Fibre vide, rang perdu, ou dérivée paramétrique nulle.

## Contrôles anti-circularité

- Tester l'énoncé sur Davenport–Heilbronn : s'il y fonctionne mot pour mot, il ne peut pas servir pour RH.
- Le confronter à l'analogue des corps de fonctions (RH connue) : une positivité sans image là-bas n'est pas une preuve.
- Aucune donnée qui injecte la réponse (zéros ou modes fabriqués puis retrouvés).
- Exiger un témoin négatif : la méthode doit détecter un défaut connu, au bon endroit.
- Signaler tout énoncé équivalent à RH : une équivalence n'est un progrès que si elle rend un outil nouveau accessible, à nommer.
- Toute constante numérique est donnée avec son erreur et ce qu'elle teste réellement.

## Pièces déposées

- `2_Methode/Depot/TAC-006/RAPPORT.md`
- `2_Methode/Depot/TAC-006/journaux/essai1_arret_newton80.txt`
- `2_Methode/Depot/TAC-006/journaux/essai2.txt`
- `2_Methode/Depot/TAC-006/journaux/essai3.txt`
- `2_Methode/Depot/TAC-006/journaux/essai4_revision.txt`
- `2_Methode/Depot/TAC-006/journaux/verification_rationnelle.txt`
- `2_Methode/Depot/TAC-006/resultats_tac006.json`
- `2_Methode/Depot/TAC-006/run_tac006.py`
- `2_Methode/Depot/TAC-006/tac006_pli_fibre.py`
- `2_Methode/Depot/TAC-006/verifier_tac006.py`

**Statut proposé :** demontre · **Équivalent à RH déclaré :** non

## Ce que vous devez faire

1. Rejouer ce qui peut l’être (programmes, calculs) et confronter le résultat au critère de rejet écrit avant.
2. Appliquer les contrôles anti-circularité ci-dessus ; chercher circularités, équivalences à RH déguisées, erreurs de signe, hypothèses cachées.
3. Vérifier que la portée annoncée n'excède pas ce qui est établi, et que le statut proposé est le bon.
4. Écrire `2_Methode/Depot/TAC-006/verification/VERIFICATION.md` (ce qui a été rejoué, ce qui ne l'a pas été, écarts).
5. `python -B 2_Methode/Pilotage/taches.py verifier TAC-006 --par ia:chatgpt-sol-6.1-max --verdict conforme|non_conforme --note "…"`. Vous ne pouvez pas être le producteur.

*La décision (acceptée, rejetée, à reprendre) appartient à l'auteur. L'intégration au corpus suit ensuite le protocole du pilotage : prévision conservée, preuve et portée, bilan, indicateur réexaminé.*
