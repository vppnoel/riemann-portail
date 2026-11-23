# TAC-012 — Document 80 face à la preuve annoncée : un carré, ou de la multiplicité ?

*Programme Riemann V6.59 · genre : investigation · rôle : explorateur · cycle 1 · statut : assignee*

## Contexte

Corpus de recherche sur l'hypothèse de Riemann (RH). RH n'est pas démontrée et ne doit pas être présentée comme telle. Lire d'abord `README.md` (« À lire d'abord »), puis `2_Methode/Pilotage/CIBLAGE.md`. Méthode : prévision écrite avant, témoins contraires, portée explicite.

## Question

Le document 80 affirme que, dans le modèle réduit (courbes sur 𝔽_q), seule la positivité d'un carré (Rosati) exclut les 119 faux jumeaux, et que c'est cet objet qui manque à ζ. La preuve annoncée suivrait au contraire la voie de Stepanov–Bombieri (comptage avec multiplicité, fonction auxiliaire s'annulant à un ordre élevé). La méthode de Stepanov–Bombieri exclut-elle les 119 faux jumeaux sans utiliser la positivité de Rosati ? Si oui, quelle information du modèle réduit utilise-t-elle que les faux jumeaux n'ont pas ? Formuler la correction à apporter au document 80.

## Entrées (empreintes SHA-256 au moment de la création)

- `1_Presentation/english/80_WHERE_THE_SIGN_COMES_FROM.md` — `4b555e3460df1f12…`
- `1_Presentation/28_MODELE_REDUIT_NECESSITE_DEMONTREE.md` — `f742030ba42df52d…`
- `NOTE_ALPOGE_2026.md` — `055409aad61bb32a…`

**Objet :** les 119 faux jumeaux du document 28 et l'argument de Stepanov–Bombieri · **Domaine :** courbes de petit genre sur 𝔽_q, comme dans le document 28

## Sortie attendue

Exposé de l'argument de Stepanov–Bombieri (référence vérifiée sur l'original, par exemple Bombieri 1973 ou un manuel), application explicite à au moins trois faux jumeaux du document 28 (calcul reproductible dans le dépôt), et énoncé corrigé du document 80 : ce qui manque à ζ était-il un carré, de la multiplicité, ou les deux sous des formes équivalentes ?

## Critère de rejet (écrit avant)

Si Stepanov–Bombieri utilise en fait une positivité équivalente à celle de Rosati (même information sous un autre nom), le document 80 reste correct à une reformulation près : statut « classique ». Si l'argument exclut les faux jumeaux par une information que le document 80 n'a pas identifiée, statut « refute » pour l'énoncé du document 80, avec l'information nommée.

## Témoin

Une vraie courbe du document 28 (RH vraie), qui doit passer l'argument ; un faux jumeau, qui doit échouer.

**Budget déclaré :** 1 lot H

## Contrôles anti-circularité

- Tester l'énoncé sur Davenport–Heilbronn : s'il y fonctionne mot pour mot, il ne peut pas servir pour RH.
- Le confronter à l'analogue des corps de fonctions (RH connue) : une positivité sans image là-bas n'est pas une preuve.
- Aucune donnée qui injecte la réponse (zéros ou modes fabriqués puis retrouvés).
- Exiger un témoin négatif : la méthode doit détecter un défaut connu, au bon endroit.
- Signaler tout énoncé équivalent à RH : une équivalence n'est un progrès que si elle rend un outil nouveau accessible, à nommer.
- Toute constante numérique est donnée avec son erreur et ce qu'elle teste réellement.

## Ce que vous devez faire

1. Avant tout calcul ou raisonnement : `python -B 2_Methode/Pilotage/taches.py prevoir TAC-012 --par ia:chatgpt-sol-6.1-max --texte "…"` (ce que vous attendez, et ce qui vous donnerait tort).
2. N'écrire que dans `2_Methode/Depot/TAC-012/`. Aucun autre fichier du corpus n'est modifié.
3. Y déposer `RAPPORT.md` avec les sections : Prévision, Méthode, Résultat, Portée, Critère de rejet, Statut proposé ; plus les programmes, données et journaux utiles.
4. `python -B 2_Methode/Pilotage/taches.py deposer TAC-012 --par ia:chatgpt-sol-6.1-max --statut-propose STATUT` (statut parmi : demontre, classique, mesure, ouvert, partiel, conditionnel, obstacle, diagnostic, outil, refute ; ajouter `--equivalent-rh` si l'énoncé obtenu entraîne RH).
5. Ne rien affirmer au-delà de la portée établie ; un échec documenté est un résultat.

*La décision (acceptée, rejetée, à reprendre) appartient à l'auteur. L'intégration au corpus suit ensuite le protocole du pilotage : prévision conservée, preuve et portée, bilan, indicateur réexaminé.*
