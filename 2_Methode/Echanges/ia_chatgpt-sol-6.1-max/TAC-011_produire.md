# TAC-011 — Article 1 après l'annonce : théorèmes A et B sans hypothèse

*Programme Riemann V6.59 · genre : redaction · rôle : rapporteur · cycle 1 · statut : assignee*

## Contexte

Corpus de recherche sur l'hypothèse de Riemann (RH). RH n'est pas démontrée et ne doit pas être présentée comme telle. Lire d'abord `README.md` (« À lire d'abord »), puis `2_Methode/Pilotage/CIBLAGE.md`. Méthode : prévision écrite avant, témoins contraires, portée explicite.

## Question

Si l'hypothèse de Riemann est démontrée, que deviennent les énoncés de l'article 1 ? Vérifier ligne à ligne que la preuve du théorème B n'utilise RH que comme hypothèse (pas d'usage caché d'une autre conjecture, par exemple la simplicité des zéros, une borne sur ζ'(ρ) ou une conjecture de corrélation), puis proposer la reformulation : théorème A (exposant 0), théorème B inconditionnel, critère « limite = 4κ/3 si et seulement si tous les zéros sont simples ». Rechercher si ce critère, ou celui de Cramér (c₁ = κ si et seulement si zéros simples), est déjà dans la littérature (zbMATH, MathSciNet si accessible, Google Scholar).

## Entrées (empreintes SHA-256 au moment de la création)

- `1_Presentation/articles/article1_mean_square_double_poles.tex` — `6302ee087ed13a79…`
- `1_Presentation/articles/LISEZMOI_ARTICLES.md` — `ee70c59d08da57cd…`
- `NOTE_ALPOGE_2026.md` — `055409aad61bb32a…`

**Objet :** article1_mean_square_double_poles.tex, théorèmes A, B, B′ · **Domaine :** énoncés et preuves de l'article 1 ; littérature jusqu'à novembre 2026

## Sortie attendue

Liste des endroits où RH intervient dans la preuve, avec ce qui est utilisé exactement. Proposition de résumé et d'énoncés révisés (diff LaTeX dans le dépôt, sans toucher à l'original). Bilan bibliographique : références trouvées, vérifiées sur l'original, ou mention explicite qu'aucune n'a été trouvée avec les requêtes utilisées.

## Critère de rejet (écrit avant)

Si la preuve du théorème B utilise une hypothèse autre que RH, le théorème ne devient pas inconditionnel : statut « conditionnel » avec l'hypothèse nommée. Si le critère de simplicité figure déjà dans la littérature, statut « classique » avec la référence.

## Témoin

Le théorème de Cramér (1922) pour ψ(x) − x, dont l'article 1 est l'analogue à pôles doubles.

**Budget déclaré :** 1 lot H

## Contrôles anti-circularité

- Tester l'énoncé sur Davenport–Heilbronn : s'il y fonctionne mot pour mot, il ne peut pas servir pour RH.
- Le confronter à l'analogue des corps de fonctions (RH connue) : une positivité sans image là-bas n'est pas une preuve.
- Aucune donnée qui injecte la réponse (zéros ou modes fabriqués puis retrouvés).
- Exiger un témoin négatif : la méthode doit détecter un défaut connu, au bon endroit.
- Signaler tout énoncé équivalent à RH : une équivalence n'est un progrès que si elle rend un outil nouveau accessible, à nommer.
- Toute constante numérique est donnée avec son erreur et ce qu'elle teste réellement.

## Ce que vous devez faire

1. Avant tout calcul ou raisonnement : `python -B 2_Methode/Pilotage/taches.py prevoir TAC-011 --par ia:chatgpt-sol-6.1-max --texte "…"` (ce que vous attendez, et ce qui vous donnerait tort).
2. N'écrire que dans `2_Methode/Depot/TAC-011/`. Aucun autre fichier du corpus n'est modifié.
3. Y déposer `RAPPORT.md` avec les sections : Prévision, Méthode, Résultat, Portée, Critère de rejet, Statut proposé ; plus les programmes, données et journaux utiles.
4. `python -B 2_Methode/Pilotage/taches.py deposer TAC-011 --par ia:chatgpt-sol-6.1-max --statut-propose STATUT` (statut parmi : demontre, classique, mesure, ouvert, partiel, conditionnel, obstacle, diagnostic, outil, refute ; ajouter `--equivalent-rh` si l'énoncé obtenu entraîne RH).
5. Ne rien affirmer au-delà de la portée établie ; un échec documenté est un résultat.

*La décision (acceptée, rejetée, à reprendre) appartient à l'auteur. L'intégration au corpus suit ensuite le protocole du pilotage : prévision conservée, preuve et portée, bilan, indicateur réexaminé.*
