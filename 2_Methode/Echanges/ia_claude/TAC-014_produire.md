# TAC-014 — Échelle, témoin : Davenport–Heilbronn échoue-t-il dès l'étage des entiers ?

*Programme Riemann V6.59 · genre : verification_temoin · rôle : auditeur · cycle 1 · statut : assignee*

## Contexte

Corpus de recherche sur l'hypothèse de Riemann (RH). RH n'est pas démontrée et ne doit pas être présentée comme telle. Lire d'abord `README.md` (« À lire d'abord »), puis `2_Methode/Pilotage/CIBLAGE.md`. Méthode : prévision écrite avant, témoins contraires, portée explicite.

## Question

Le document de travail RECOLLER_LES_MORCEAUX_V6_60 (§6.3) prévoit que Davenport–Heilbronn, qui n'a pas de produit d'Euler, n'a pas d'entiers qui encodent ses « premiers », et que le mécanisme échoue dès l'étage 2. Le vérifier : les coefficients de −F′/F pour DH sont-ils positifs et portés par les puissances de premiers ? Existe-t-il, pour DH, une suite d'entiers analogue à C(2n, n) dont la divisibilité encode sa somme « sur les premiers » ? Si non, à quel endroit précis l'analogie casse-t-elle ?

## Entrées (empreintes SHA-256 au moment de la création)

- `1_Presentation/RECOLLER_LES_MORCEAUX_V6_60.md` — `c8ae736df295c02e…`
- `1_Presentation/30_ARCHIPEL_D_EULER.md` — `3604703a05e55f0b…`

**Objet :** la fonction de Davenport–Heilbronn du corpus et ses coefficients · **Domaine :** n ≤ 10⁵

## Sortie attendue

Calcul reproductible des coefficients de −F′/F pour DH (signes, support) ; tentative explicite de construction d'un analogue entier ; énoncé de l'endroit où le mécanisme casse, avec ζ et L(s, χ₅) comme témoins qui passent.

## Critère de rejet (écrit avant)

Si les coefficients de DH sont positifs et portés par les puissances de premiers, ou si un analogue entier existe, la prévision du §6.3 est fausse : statut « refute » pour ce paragraphe.

## Témoin

ζ et L(s, χ₅), qui doivent passer l'étage 2.

**Budget déclaré :** 0,5 lot H

## Contrôles anti-circularité

- Tester l'énoncé sur Davenport–Heilbronn : s'il y fonctionne mot pour mot, il ne peut pas servir pour RH.
- Le confronter à l'analogue des corps de fonctions (RH connue) : une positivité sans image là-bas n'est pas une preuve.
- Aucune donnée qui injecte la réponse (zéros ou modes fabriqués puis retrouvés).
- Exiger un témoin négatif : la méthode doit détecter un défaut connu, au bon endroit.
- Signaler tout énoncé équivalent à RH : une équivalence n'est un progrès que si elle rend un outil nouveau accessible, à nommer.
- Toute constante numérique est donnée avec son erreur et ce qu'elle teste réellement.

## Ce que vous devez faire

1. Avant tout calcul ou raisonnement : `python -B 2_Methode/Pilotage/taches.py prevoir TAC-014 --par ia:claude --texte "…"` (ce que vous attendez, et ce qui vous donnerait tort).
2. N'écrire que dans `2_Methode/Depot/TAC-014/`. Aucun autre fichier du corpus n'est modifié.
3. Y déposer `RAPPORT.md` avec les sections : Prévision, Méthode, Résultat, Portée, Critère de rejet, Statut proposé ; plus les programmes, données et journaux utiles.
4. `python -B 2_Methode/Pilotage/taches.py deposer TAC-014 --par ia:claude --statut-propose STATUT` (statut parmi : demontre, classique, mesure, ouvert, partiel, conditionnel, obstacle, diagnostic, outil, refute ; ajouter `--equivalent-rh` si l'énoncé obtenu entraîne RH).
5. Ne rien affirmer au-delà de la portée établie ; un échec documenté est un résultat.

*La décision (acceptée, rejetée, à reprendre) appartient à l'auteur. L'intégration au corpus suit ensuite le protocole du pilotage : prévision conservée, preuve et portée, bilan, indicateur réexaminé.*
