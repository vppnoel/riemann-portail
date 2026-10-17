# Lot 1 — consigne pour ChatGPT (ia:chatgpt-sol-6.1-max)

*Programme Riemann V6.59 · 17 octobre 2026 · préparé par le coordinateur (ia:claude) à la demande de Vincent NOËL. Fiches : TAC-002, TAC-003, TAC-009.*

## À coller en tête de la conversation avec ChatGPT

````text
Tu travailles sur le corpus « Programme Riemann » (archive jointe, V6.59) de Vincent NOËL, qui porte sur l'hypothèse de Riemann (RH). RH n'est pas démontrée et ne doit pas être présentée comme telle. Lis d'abord README.md (« À lire d'abord »), puis 2_Methode/Pilotage/CIBLAGE.md. Ton identifiant d'acteur est ia:chatgpt-sol-6.1-max. Trois fiches te sont assignées ; elles sont données plus bas.

Étape 1 — prévisions, AVANT tout calcul ou raisonnement. Pour chaque fiche, réponds seulement par ta prévision : ce que tu attends, et ce qui te donnerait tort, en quelques lignes. Ne commence pas le travail. L'auteur enregistrera ces prévisions avec leur heure (taches.py prevoir), puis te dira de continuer.

Étape 2 — travail, après le feu vert. Pour chaque fiche, produis un dossier TAC-xxx/ contenant RAPPORT.md avec exactement les sections : ## Prévision, ## Méthode, ## Résultat, ## Portée, ## Critère de rejet, ## Statut proposé. Ajoute les programmes (Python, bibliothèque standard + numpy/mpmath), les données et les journaux utiles. N'écris rien d'autre dans le corpus. Le statut proposé appartient à : demontre, classique, mesure, ouvert, partiel, conditionnel, obstacle, diagnostic, outil, refute. Signale si un énoncé obtenu entraîne RH. Vérifie en ligne toute référence que tu cites et dis ce que tu as vérifié. Un échec documenté est un résultat. Rends une archive zip contenant les dossiers TAC-xxx/.

Ton travail sera vérifié par un autre acteur, puis l'auteur décidera.
````

---

# TAC-002 — Paquets signés : garder premiers, coupures et dette

*Programme Riemann V6.59 · genre : investigation · rôle : explorateur · cycle 1 · statut : assignee*

## Contexte

Corpus de recherche sur l'hypothèse de Riemann (RH). RH n'est pas démontrée et ne doit pas être présentée comme telle. Lire d'abord `README.md` (« À lire d'abord »), puis `2_Methode/Pilotage/CIBLAGE.md`. Méthode : prévision écrite avant, témoins contraires, portée explicite.

## Question

Quelle inégalité locale des vrais paquets pourrait se sommer sans perdre les couplages ?

## Entrées (empreintes SHA-256 au moment de la création)

- `1_Presentation/76_RECONSTRUIRE_LA_PISTE_GLOBALE_DE_WEIL.md` — `8f4585117c1ab7f8…`

**Objet :** — · **Domaine :** celui de la question ; à préciser dans la prévision

## Sortie attendue

Énoncé vérifiable avec bords, norme, dette et critère de rejet ; contre-exemple recevable. Aucun signe universel promis.

## Critère de rejet (écrit avant)

Un paquet admissible réfute la proposition, ou la somme des dettes n’est pas contrôlée.

## Témoin

Modèle continu négatif et blocs à rapport fixe déjà réfutés ; ne pas les reconstruire sans nouvelle hypothèse.

## Contrôles anti-circularité

- Tester l'énoncé sur Davenport–Heilbronn : s'il y fonctionne mot pour mot, il ne peut pas servir pour RH.
- Le confronter à l'analogue des corps de fonctions (RH connue) : une positivité sans image là-bas n'est pas une preuve.
- Aucune donnée qui injecte la réponse (zéros ou modes fabriqués puis retrouvés).
- Exiger un témoin négatif : la méthode doit détecter un défaut connu, au bon endroit.
- Signaler tout énoncé équivalent à RH : une équivalence n'est un progrès que si elle rend un outil nouveau accessible, à nommer.
- Toute constante numérique est donnée avec son erreur et ce qu'elle teste réellement.

## Ce que vous devez faire

1. Avant tout calcul ou raisonnement : `python -B 2_Methode/Pilotage/taches.py prevoir TAC-002 --par ia:chatgpt-sol-6.1-max --texte "…"` (ce que vous attendez, et ce qui vous donnerait tort).
2. N'écrire que dans `2_Methode/Depot/TAC-002/`. Aucun autre fichier du corpus n'est modifié.
3. Y déposer `RAPPORT.md` avec les sections : Prévision, Méthode, Résultat, Portée, Critère de rejet, Statut proposé ; plus les programmes, données et journaux utiles.
4. `python -B 2_Methode/Pilotage/taches.py deposer TAC-002 --par ia:chatgpt-sol-6.1-max --statut-propose STATUT` (statut parmi : demontre, classique, mesure, ouvert, partiel, conditionnel, obstacle, diagnostic, outil, refute ; ajouter `--equivalent-rh` si l'énoncé obtenu entraîne RH).
5. Ne rien affirmer au-delà de la portée établie ; un échec documenté est un résultat.

*La décision (acceptée, rejetée, à reprendre) appartient à l'auteur. L'intégration au corpus suit ensuite le protocole du pilotage : prévision conservée, preuve et portée, bilan, indicateur réexaminé.*


---

# TAC-003 — Dette de Schur dans la norme duale

*Programme Riemann V6.59 · genre : investigation · rôle : explorateur · cycle 1 · statut : assignee*

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


---

# TAC-009 — Gram de Nyman–Beurling sur des différences d'échelle

*Programme Riemann V6.59 · genre : investigation · rôle : explorateur · cycle 1 · statut : assignee*

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


---

## Pour l’auteur : enregistrer les échanges

```sh
# après l’étape 1 (une commande par fiche, avec le texte rendu par ChatGPT) :
python -B 2_Methode/Pilotage/taches.py prevoir TAC-002 --par ia:chatgpt-sol-6.1-max --texte "…"
python -B 2_Methode/Pilotage/taches.py prevoir TAC-003 --par ia:chatgpt-sol-6.1-max --texte "…"
python -B 2_Methode/Pilotage/taches.py prevoir TAC-009 --par ia:chatgpt-sol-6.1-max --texte "…"
# après l’étape 2 : copier chaque dossier rendu dans 2_Methode/Depot/TAC-xxx/, puis
python -B 2_Methode/Pilotage/taches.py deposer TAC-002 --par ia:chatgpt-sol-6.1-max --statut-propose STATUT
python -B 2_Methode/Pilotage/taches.py deposer TAC-003 --par ia:chatgpt-sol-6.1-max --statut-propose STATUT
python -B 2_Methode/Pilotage/taches.py deposer TAC-009 --par ia:chatgpt-sol-6.1-max --statut-propose STATUT
```

La vérification sera confiée à un autre acteur (par exemple ia:claude), avec `taches.py fiche TAC-xxx --verification`.
