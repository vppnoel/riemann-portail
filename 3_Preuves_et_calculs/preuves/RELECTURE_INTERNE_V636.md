# V6.36 — Relecture constructive, critique et synthèse

**Date :** 12 octobre 2026. Deux lectures internes par agents ont été confrontées. Aucune expertise humaine indépendante ni acceptation éditoriale n'est revendiquée.

## 1. Le troisième article

**Thèse constructive.** La chaîne jets, rang, multiplicités, tour et spectre mérite une note autonome, accompagnée de certificats exacts.

**Antithèse critique.** La méthode de Stepanov et la borne de Hasse sont classiques. Le texte ne peut pas être présenté comme une découverte de ces résultats ou comme un progrès démontré vers RH pour les entiers. Le cas F27 teste les jets élevés mais son noyau existe déjà par le simple nombre de conditions ; le cas F125 tordu montre la baisse de rang malgré 560 conditions pour 450 dimensions.

**Synthèse retenue.** Article expositif de huit pages, preuve autonome, hypothèses explicites, cinq certificats et douze comptages. La rationalité est justifiée avant la déduction spectrale, indépendamment de Hasse. La lissité et le genre un ne sont pas omis. La date de l'édition de Milne est corrigée en 2021.

## 2. Les articles existants

Les deux lectures ont recoupé les erreurs de formulation dans l'article 1 : approximation de l'exposant fini sans son terme constant, normalisation de beta déduite à tort d'une médiane, affirmation asymptotique de non-convergence à partir d'un échantillon, minimum des écarts lorsque J<2 et portée excessive des calibrations.

La preuve du théorème B a été relue : queue uniforme dans eta, analyse locale à hauteur fixée, ordre des limites, convergence de la somme avec multiplicités et facteur taubérien S/3. Aucune faille n'a été trouvée dans ces points contrôlés. Les références numérotées non vérifiées dans les originaux restent à faire contrôler.

Dans l'article 2, les tolérances sont maintenant annoncées dès le résumé et le tableau. L'effectivité des faux jumeaux est limitée au domaine effectivement testé, jusqu'au degré 200. La phrase ancienne annonçant que le cas impair n'avait pas été étudié renvoie désormais au certificat.

## 3. Le coup en norme

**Thèse constructive.** Deux calculs indépendants doivent confirmer les directions négatives nettement séparées de zéro.

**Antithèse critique.** Leur différence mesurée ne borne pas l'erreur par rapport à la matrice exacte. Un résidu de vecteur propre isolé ne prouve pas une inertie. Il faut encadrer les traces et contrôler une forme sur un sous-espace indépendant.

**Synthèse exécutée.** Le programme reconstruit les traces DH sans zéro, avec coefficients en intervalles et quadrature physique. Le candidat de 25 colonnes est traité comme une matrice dyadique exacte. Les deux produits de sa compression sont majorés dans le modèle standard d'arrondi ; Gershgorin valide leur signe.

La lecture critique a vérifié :

- la formule fermée de g par intégration des harmoniques ;
- les majorants complexes et la séparation des branches ;
- le quotient amovible près de zéro et le majorant 1000 ;
- la constante du reste de Gauss–Legendre combinée à Cauchy ;
- les encadrements disjoints des seize noeuds, leurs poids et le cutoff des coefficients ;
- le budget des deux produits positifs et son inflation d'arrondi ;
- le passage de la négativité de la compression à une borne inférieure d'inertie.

Elle a également contrôlé, par fractions dyadiques exactes, les 1115 centres et rayons, la somme de Frobenius des rayons et les 25 normes carrées des colonnes. Leur maximum est voisin de 1,000000000000001, donc inférieur à 2.

**Conclusion recevable :** au moins 25 directions négatives, sous le modèle d'arithmétique annoncé. La borne supérieure de Gershgorin est inférieure à −6,087×10⁻⁹. Le nombre total exact reste non certifié.

## 4. Vérification éditoriale et suite

La compilation des sources et l'inspection des PDF complètent ces relectures. La commande de reproduction de l'article 3 emploie le lanceur réel des tests du corpus, et non une découverte unittest qui n'exécuterait pas ses fonctions de test.

Le prochain coup classé par le navigateur est l'ancrage V13 avec directions appariées. La construction d'un espace auxiliaire pour les entiers reste une route à construire. Aucun envoi ni aucune soumission externe n'a été effectué.
