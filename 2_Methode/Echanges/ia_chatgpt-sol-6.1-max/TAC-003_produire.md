# TAC-003 — Dette de Schur dans la norme duale

*Programme Riemann V6.59 · genre : investigation · rôle : explorateur · cycle 1 · statut : a_reprendre*

## Contexte

Corpus de recherche sur l'hypothèse de Riemann (RH). RH n'est pas démontrée et ne doit pas être présentée comme telle. Lire d'abord `README.md` (« À lire d'abord »), puis `2_Methode/Pilotage/CIBLAGE.md`. Méthode : prévision écrite avant, témoins contraires, portée explicite.

## Question

Peut-on payer la dette par une norme duale spécifique, sans exiger toutes les sources fortes de Q ?

## Entrées (empreintes SHA-256 au moment de la création)

- `1_Presentation/79_SIGNAL_COUPLAGES_ET_RESOLUTION.md` — `52d09737701c7a55…`

**Objet :** — · **Domaine :** celui de la question ; à préciser dans la prévision

## Sortie attendue

Borne candidate ou obstruction avec domaine et constantes ; bilan de portée local/global. Complément 76 : continuité du candidat, défaut mixte, garde d’image de Schur ; six contrôles abstraits exacts, aucun calcul de Suzuki ni signe global obtenu. Seconde passe : raccord exact et couverture par translation établis ; prolongement pair suspendu ; 12 contrôles abstraits exacts. Pas de minoration arithmétique universelle. V6.57 : diagnostic de phases sur les matrices arithmétiques V644 ; certificat adaptatif 44 cellules sur une fenêtre déjà traitée. Ni certificat infini supplémentaire ni loi universelle.

## Critère de rejet (écrit avant)

Une hypothèse de domaine manque ou l’inégalité duale ne domine pas le vrai couplage.

## Témoin

Matrices positives en tête avec complément ou résidu non contrôlé.

## Contrôles anti-circularité

- Tester l'énoncé sur Davenport–Heilbronn : s'il y fonctionne mot pour mot, il ne peut pas servir pour RH.
- Le confronter à l'analogue des corps de fonctions (RH connue) : une positivité sans image là-bas n'est pas une preuve.
- Aucune donnée qui injecte la réponse (zéros ou modes fabriqués puis retrouvés).
- Exiger un témoin négatif : la méthode doit détecter un défaut connu, au bon endroit.
- Signaler tout énoncé équivalent à RH : une équivalence n'est un progrès que si elle rend un outil nouveau accessible, à nommer.
- Toute constante numérique est donnée avec son erreur et ce qu'elle teste réellement.

## Ce que vous devez faire

1. Avant tout calcul ou raisonnement : `python -B 2_Methode/Pilotage/taches.py prevoir TAC-003 --par ia:chatgpt-sol-6.1-max --texte "…"` (ce que vous attendez, et ce qui vous donnerait tort).
2. N'écrire que dans `2_Methode/Depot/TAC-003/`. Aucun autre fichier du corpus n'est modifié.
3. Y déposer `RAPPORT.md` avec les sections : Prévision, Méthode, Résultat, Portée, Critère de rejet, Statut proposé ; plus les programmes, données et journaux utiles.
4. `python -B 2_Methode/Pilotage/taches.py deposer TAC-003 --par ia:chatgpt-sol-6.1-max --statut-propose STATUT` (statut parmi : demontre, classique, mesure, ouvert, partiel, conditionnel, obstacle, diagnostic, outil, refute ; ajouter `--equivalent-rh` si l'énoncé obtenu entraîne RH).
5. Ne rien affirmer au-delà de la portée établie ; un échec documenté est un résultat.

*La décision (acceptée, rejetée, à reprendre) appartient à l'auteur. L'intégration au corpus suit ensuite le protocole du pilotage : prévision conservée, preuve et portée, bilan, indicateur réexaminé.*
