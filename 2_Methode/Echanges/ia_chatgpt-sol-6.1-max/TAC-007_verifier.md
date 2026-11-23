# TAC-007 — Certificat du noyau des moments à S = 0,8

*Programme Riemann V6.59 · genre : investigation · rôle : explorateur · cycle 1 · statut : deposee*

## Contexte

Corpus de recherche sur l'hypothèse de Riemann (RH). RH n'est pas démontrée et ne doit pas être présentée comme telle. Lire d'abord `README.md` (« À lire d'abord »), puis `2_Methode/Pilotage/CIBLAGE.md`. Méthode : prévision écrite avant, témoins contraires, portée explicite.

## Énoncé à vérifier

Certifier un minorant de Q_W sur les tests à moments nuls de support [−0,8 ; 0,8], où agissent 2, 3 et 4.

*Relecture à l'aveugle : l'identité du producteur n'est pas donnée. Lire les pièces et les données avant la conclusion du rapport.*

## Entrées (empreintes SHA-256 au moment de la création)

- `1_Presentation/81_ZHU_REPRODUIT.md` — `319a04eef847f0dc…`

**Objet :** — · **Domaine :** celui de la question ; à préciser dans la prévision

## Sortie attendue

Certificat local ou obstacle documenté. Renforce une marge déjà positive (Zhu) ; aucune fenêtre nouvelle ni conséquence globale : la positivité sur toutes les fenêtres est RH.

## Critère de rejet (écrit avant)

Marge mesurée sous 10⁻¹³ avec plus de modes, ou tête irréalisable en intervalles : la voie par fenêtres s’arrête à 11/20.

## Témoin

Marge mesurée ≈ 5·10⁻¹² (doc. 81), non certifiée ; certificat existant jusqu’à 11/20 (doc. 75).

## Contrôles anti-circularité

- Tester l'énoncé sur Davenport–Heilbronn : s'il y fonctionne mot pour mot, il ne peut pas servir pour RH.
- Le confronter à l'analogue des corps de fonctions (RH connue) : une positivité sans image là-bas n'est pas une preuve.
- Aucune donnée qui injecte la réponse (zéros ou modes fabriqués puis retrouvés).
- Exiger un témoin négatif : la méthode doit détecter un défaut connu, au bon endroit.
- Signaler tout énoncé équivalent à RH : une équivalence n'est un progrès que si elle rend un outil nouveau accessible, à nommer.
- Toute constante numérique est donnée avec son erreur et ce qu'elle teste réellement.

## Pièces déposées

- `2_Methode/Depot/TAC-007/RAPPORT.md`
- `2_Methode/Depot/TAC-007/p1_mesure_noyau_08.py`
- `2_Methode/Depot/TAC-007/p1_resultats.json`
- `2_Methode/Depot/TAC-007/p2_budgets_architecture_doc75.py`
- `2_Methode/Depot/TAC-007/p2_resultats.json`
- `2_Methode/Depot/TAC-007/p3_controles_adverses.py`
- `2_Methode/Depot/TAC-007/p3_resultats.json`

**Statut proposé :** partiel · **Équivalent à RH déclaré :** non

## Ce que vous devez faire

1. Rejouer ce qui peut l’être (programmes, calculs) et confronter le résultat au critère de rejet écrit avant.
2. Appliquer les contrôles anti-circularité ci-dessus ; chercher circularités, équivalences à RH déguisées, erreurs de signe, hypothèses cachées.
3. Vérifier que la portée annoncée n'excède pas ce qui est établi, et que le statut proposé est le bon.
4. Écrire `2_Methode/Depot/TAC-007/verification/VERIFICATION.md` (ce qui a été rejoué, ce qui ne l'a pas été, écarts).
5. `python -B 2_Methode/Pilotage/taches.py verifier TAC-007 --par ia:chatgpt-sol-6.1-max --verdict conforme|non_conforme --note "…"`. Vous ne pouvez pas être le producteur.

*La décision (acceptée, rejetée, à reprendre) appartient à l'auteur. L'intégration au corpus suit ensuite le protocole du pilotage : prévision conservée, preuve et portée, bilan, indicateur réexaminé.*
