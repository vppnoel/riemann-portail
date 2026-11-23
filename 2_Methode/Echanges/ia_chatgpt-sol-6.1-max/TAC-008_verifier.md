# TAC-008 — Décomposer la cohérence K : diagonale, même premier, premiers distincts

*Programme Riemann V6.59 · genre : investigation · rôle : numerique · cycle 1 · statut : deposee*

## Contexte

Corpus de recherche sur l'hypothèse de Riemann (RH). RH n'est pas démontrée et ne doit pas être présentée comme telle. Lire d'abord `README.md` (« À lire d'abord »), puis `2_Methode/Pilotage/CIBLAGE.md`. Méthode : prévision écrite avant, témoins contraires, portée explicite.

## Énoncé à vérifier

Pour la matrice de cohérence inter-échelles du canal de la dérivée logarithmique (critique « tomographie de phase », § 8–9 : K^A_ij = ∫ C_F(u_i,t) conj(C_F(u_j,t)) ψ(t/T) dt, normalisée R^A), écrire K = K_diag + K_chaîne (n = p^k, m = p^l, même p) + K_croisé (premiers distincts ou n, m hors puissances de premiers) et mesurer la part de chaque terme pour ζ, L(s, χ₅), Davenport–Heilbronn et les témoins standard (phases randomisées sur les premiers, suites multiplicatives aléatoires). Où apparaît le surplus de cohérence du produit d'Euler ?

*Relecture à l'aveugle : l'identité du producteur n'est pas donnée. Lire les pièces et les données avant la conclusion du rapport.*

## Entrées (empreintes SHA-256 au moment de la création)

- `4_Archives/recus/2026-10-17/critique_tomographie_de_phase_MPT.txt` — `de0b10d829fad9c6…`
- `1_Presentation/18_PRIME_LOCK_premier_verrou_local.md` — `66a3d0a5af526ce1…`
- `1_Presentation/15_TOMO_DH_formalisation.md` — `f6de7d28ef6663df…`
- `1_Presentation/17_DARK_ZETA_premier_detecteur_resultats.md` — `2c42baf423bb412a…`

**Objet :** matrice de cohérence K^A et ses trois composantes · **Domaine :** grille d'échelles u_1..u_m et fenêtre ψ(t/T) déclarées dans la prévision ; mêmes témoins que les docs 15 à 18

## Sortie attendue

Formule exacte de la décomposition ; tableau des parts de K_diag, K_chaîne et K_croisé pour ζ, L(χ₅), DH et témoins, avec incertitude sur les tirages aléatoires ; verdict : la séparation est-elle portée par K_chaîne (structure eulérienne, comme PRIME-LOCK) ou par K_diag (énergie) ?

## Critère de rejet (écrit avant)

Si K_chaîne ne sépare pas {ζ, L(χ₅)} de DH plus que les témoins à phases randomisées (au-delà de deux écarts-types des tirages), ou si toute la séparation vient de K_diag, la décomposition n'apporte rien au-delà de PRIME-LOCK (doc. 18) : statut « obstacle » ou « diagnostic ». Aucune conclusion sur le signe de Weil ni sur RH dans tous les cas (docs 21 à 24 : verrou local et signe global indépendants).

## Témoin

PRIME-LOCK (doc. 18) détecte déjà Λ_F(p^k) = α_p^k log p ; DH, sans produit d'Euler, doit échouer au test de la chaîne.

**Budget déclaré :** 1 lot H

## Contrôles anti-circularité

- Tester l'énoncé sur Davenport–Heilbronn : s'il y fonctionne mot pour mot, il ne peut pas servir pour RH.
- Le confronter à l'analogue des corps de fonctions (RH connue) : une positivité sans image là-bas n'est pas une preuve.
- Aucune donnée qui injecte la réponse (zéros ou modes fabriqués puis retrouvés).
- Exiger un témoin négatif : la méthode doit détecter un défaut connu, au bon endroit.
- Signaler tout énoncé équivalent à RH : une équivalence n'est un progrès que si elle rend un outil nouveau accessible, à nommer.
- Toute constante numérique est donnée avec son erreur et ce qu'elle teste réellement.

## Pièces déposées

- `2_Methode/Depot/TAC-008/RAPPORT.md`
- `2_Methode/Depot/TAC-008/decomposition_K.py`
- `2_Methode/Depot/TAC-008/resultats.json`
- `2_Methode/Depot/TAC-008/temoin_negatif.json`
- `2_Methode/Depot/TAC-008/temoin_negatif.py`

**Statut proposé :** diagnostic · **Équivalent à RH déclaré :** non

## Ce que vous devez faire

1. Rejouer ce qui peut l’être (programmes, calculs) et confronter le résultat au critère de rejet écrit avant.
2. Appliquer les contrôles anti-circularité ci-dessus ; chercher circularités, équivalences à RH déguisées, erreurs de signe, hypothèses cachées.
3. Vérifier que la portée annoncée n'excède pas ce qui est établi, et que le statut proposé est le bon.
4. Écrire `2_Methode/Depot/TAC-008/verification/VERIFICATION.md` (ce qui a été rejoué, ce qui ne l'a pas été, écarts).
5. `python -B 2_Methode/Pilotage/taches.py verifier TAC-008 --par ia:chatgpt-sol-6.1-max --verdict conforme|non_conforme --note "…"`. Vous ne pouvez pas être le producteur.

*La décision (acceptée, rejetée, à reprendre) appartient à l'auteur. L'intégration au corpus suit ensuite le protocole du pilotage : prévision conservée, preuve et portée, bilan, indicateur réexaminé.*
