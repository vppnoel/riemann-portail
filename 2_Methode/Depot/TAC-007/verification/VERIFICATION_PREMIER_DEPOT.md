# Vérification indépendante — TAC-007

*Vérificateur : ia:chatgpt-sol-6.1-max · 18 octobre 2026 · verdict : non conforme au protocole de vérification, sans réfutation numérique de P1 ni de P2.*

## Pièces et intégrité examinées

- Fiche TAC-007, dépôt et rapport ; registre et journal de tâches.
- `p1_mesure_noyau_08.py` et `p1_resultats.json`.
- `p2_budgets_architecture_doc75.py`, `p2_resultats.json` et la source V6.50 citée.
- `run_zhu_reproduction.py` : formule, construction du noyau à moment exponentiel nul, projection de Householder et calcul spectral.

Le dépôt est distinct de la présente vérification. Le producteur enregistré est `ia:claude`, le vérificateur est un autre acteur.

## Ce qui a été contrôlé

### P1 — mesure du noyau

La table est cohérente avec le programme lu :

- secteur pair : (5.39923299611,10^{-12}) à (N=40), puis (5.37876479342,10^{-12}), (5.35725706389,10^{-12}) et (5.34694614142,10^{-12}) à (N=64,K=48) ;
- à (N=64), passer de (K=48) à (K=96) donne (5.35029972448,10^{-12}), soit un écart relatif d’environ (6.3,10^{-4}) ;
- passer de 60 à 80 chiffres ne modifie pas les chiffres affichés ;
- secteur impair : (9.85526381624,10^{-10}) à (N=48), donc il n’est pas limitant pour cette troncature.

La baisse avec (N) est conforme au sens variationnel attendu pour une compression de Rayleigh–Ritz : elle ne fournit **pas** un minorant sur tout l’espace. Le rapport le dit correctement. Le calcul de P1 n’appelle pas les données de zéros : le module importé en contient un contrôle séparé, mais `noyau_des_moments` n’y recourt pas.

Je n’ai pas pu réexécuter le programme dans cet environnement : l’accès au dépôt est fourni par le connecteur GitHub, sans exécution locale authentifiée. Les chiffres ci-dessus sont donc inspectés et confrontés aux sources, non reproduits sur un second environnement pendant cette vérification.

### P2 — budget de l’architecture V6.50

L’arithmétique du rapport est cohérente avec les données déposées :

[
  1.5216406675922078,10^{-4}/(5,10^{-12})
  =3.0432813351844,10^7.
]

Sous la loi explicitement posée pour les trapèzes, le nombre de cellules vaut bien

[
  7,10^5sqrt{3.0432813351844,10^7}
  =3.861616053,10^9,
]

et le modèle d’assemblage binary64 donne alors

[
  1.1083479345842718,10^{-5}sqrt{3.0432813351844,10^7}
  =6.11430597,10^{-2}.
]

Cela établit un obstacle pour **cette architecture et ces lois d’erreur**. Cela n’établit pas une impossibilité mathématique d’un certificat à (S=0.8), ni même d’une autre implémentation intervallaire. Le rapport le dit correctement.

## Contrôles anti-circularité et écarts

- Aucune conclusion RH n’est tirée ; l’énoncé local n’est pas présenté comme équivalent à RH.
- La distinction mesure / certificat est correcte.
- En revanche, les deux contrôles explicitement demandés dans la fiche ne sont pas documentés : test adversarial sur Davenport–Heilbronn et confrontation à l’analogue des corps de fonctions.
- Aucun témoin négatif exécutable n’est déposé pour vérifier que la chaîne « calcul de la forme → projection → plus petite valeur propre » signale effectivement un défaut contrôlé.
- La route « tête–queue, intervalles multiprécision, complément de Schur » reste une proposition. Elle ne peut pas être invoquée comme certificat, et elle doit être ouverte comme une nouvelle fiche avec majoration de queue formulée avant calcul.

## Verdict et portée

**Verdict : non conforme**, pour incomplétude des contrôles adverses requis par la fiche, non parce que P1 ou P2 seraient contredites.

Le statut scientifique proposé **partiel** est approprié pour le contenu mathématique effectivement établi : mesure numérique stable et obstacle d’architecture documenté ; aucun certificat nouveau. Pour redevenir vérifiable, TAC-007 doit ajouter les deux contrôles adverses et un témoin négatif, ou justifier formellement pourquoi ils ne s’appliquent pas à cet énoncé local.

*Fiche déposée pour enregistrement du verdict.*
