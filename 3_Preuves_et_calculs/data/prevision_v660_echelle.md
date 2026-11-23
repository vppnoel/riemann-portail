# Prévision V6.60 (document 83) — écrite avant le calcul (19:59 UTC, 22 novembre 2026)

Niveau 0 de l'échelle : le mécanisme « un entier ne peut pas être à la fois petit et trop divisible », sans multiplicité.

- P1. Pour tout n ≤ 200 000, l'entier C(2n, n) est divisible par chaque premier de ]n, 2n], donc θ(2n) − θ(n) ≤ log C(2n, n) < 2n log 2. Aucune exception (c'est le théorème de Tchebychev ; le calcul vérifie le code).
- P2. Majoration de θ qui en découle : θ(x) ≤ 2 log 2 · x pour tout x ≤ 400 000. Rapport maximal θ(x)/x observé entre 1,0 et 1,1, donc loin de la borne 1,386 : sans multiplicité, la borne est grossière, l'erreur est d'ordre x et non √x.
- P3. Le « gaspillage » log C(2n,n) − (θ(2n) − θ(n)), c'est-à-dire la part de divisibilité qui ne vient pas des premiers de ]n,2n], est d'ordre n (et non √n) : rapport gaspillage / n entre 0,3 et 0,7 pour n ≥ 10 000.

Critère de rejet : une exception à P1 signale une erreur de code. Si P3 donnait un gaspillage d'ordre √n, le niveau 0 serait déjà presque optimal, et ma lecture de « il faut fabriquer de la multiplicité » serait fausse.


*Note ajoutée après le calcul : le document visé est `1_Presentation/RECOLLER_LES_MORCEAUX_V6_60.md` (numéro 83 proposé). le titre portait « V6.83 » par erreur ; seul ce numéro a été corrigé. L'heure et le texte des prévisions sont inchangés.*
