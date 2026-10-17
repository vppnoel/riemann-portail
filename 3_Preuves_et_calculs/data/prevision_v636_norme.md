# V6.36 — Contrôle en norme du cas DH à 25 directions

**Date :** 12 octobre 2026. Écrit avant l'exécution du nouveau calcul.

## Coup repris

Le coup signature_erreur_norme du navigateur fixe DH, a=0,02, h=0,005, L=1115. Le décompte ancien de 25 directions est un contrôle connu, pas une prévision nouvelle.

## Prévisions et critères

1. Le calcul physique du terme archimédien doit coïncider avec le calcul Fourier, en erreur absolue, à un niveau très inférieur aux valeurs propres négatives nettement séparées de zéro.
2. Les directions négatives dominantes doivent persister. Un décompte numérique proche de zéro doit être présenté comme ambigu tant que l'erreur totale n'est pas bornée.
3. Une certification ne sera revendiquée que si les coefficients arithmétiques, la convolution g, la quadrature archimédienne et les arrondis sont tous couverts.
4. Des vecteurs calculés numériquement peuvent proposer un sous-espace. Seule une forme comprimée démontrée négative avec ses erreurs prouve une borne inférieure sur l'inertie. Un résidu isolé ne prouve pas un décompte.

## Procédure fixée

- Reconstruire les coefficients de DH indépendamment avec les radicaux et logarithmes à précision élevée.
- Évaluer g par une formule trigonométrique fermée.
- Employer la représentation intégrale de la fonction digamma pour une quadrature dans la variable physique, avec supports compacts et queue explicite.
- Tenter des intervalles avec majoration analytique de la quadrature ; archiver les traces et leur budget.
- Proposer les sous-espaces formés par les k valeurs propres les plus négatives, k de 25 à 1, et accepter uniquement ceux dont la compression reste négative après majoration de toutes les erreurs.
- Conserver le compte numérique initial, les marges et les résultats négatifs ou partiels.

## Réfutation et portée

Une différence trop grande entre reconstructions réfute la fiabilité précédente. Une marge inférieure au budget interdit le certificat correspondant. Si un poste reste non borné, annoncer un audit numérique partiel, sans le convertir en preuve.

Le résultat concerne une fenêtre de Davenport–Heilbronn. Il ne prouve ni RH, ni l'absence générale de directions négatives pour la zêta.
