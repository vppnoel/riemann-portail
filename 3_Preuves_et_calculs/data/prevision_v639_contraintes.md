# V6.39 - Prévision du test de contraintes exactes V13

12 octobre2026. Écrit avant le calcul des nouveaux témoins.

But : décider si le défaut D peut varier à même coefficient complexe A=a(1), ancre et rayon dans l’espace V13 impair.

Construction à tester : c_plus=t e_i+s u et c_minus=t e_i−s u, avec u_i=0, somme_j z_j u_j=0 et norme(u)=1, t=cos(r),s=sin(r),0<r<pi/4. Le noyau de ces trois contraintes réelles doit être de dimension au moins3 ; ce fait seul ne garantit pas la variation de D.

Contrat : chercher une relation exacte de trois colonnes z_j, normalisée analytiquement par sa norme, et encadrer son coefficient cubique P_i=Re[z_i somme_j u_j^3 bar(z_j)]. Si un intervalle exclut0, la paire varie strictement en D sous contraintes EXACTES. Les nombres flottants ne sont que des approximations de ce témoin défini par les constantes algébriques.

Domaines : six ancres ; rayons0.45,0.65,0.75 de V6.37 et rayon exactpi/6. Refaire les encadrements à80 et120 chiffres. Toutes les20 triples par ancre sont examinées ; choix de témoin après calcul annoncé comme recherche constructive, sans statistique confirmatoire.

Réfutation/arrêt : matrice de contraintes dégénérée, formule de D incompatible avec codehistorique, intervalle de P contenant0, ou branche de phase ambiguë. Un échec de la recherche de témoins ne démontre pas l’impossibilité de toute variation ; il impose un autre argument.

Aucun comptage de zéros dans cette étape. Aucune causalité ou conséquence RH inférée. Si variation prouvée, prochaineétape = figer un plan de comparaison sur les contraintes exactes avant toute nouvelle recherche de zéros.


## Notes de réalisation, conservant la prévision précédente
- Erratum de dénombrement :10 triplets hors ancre, pas20 ;20 est le nombre de triplets dans les six coordonnées avant exclusion de l’ancre. La recherche constructive a traité10 triplets pour chaque ancre.
- Deux témoins sont retenus : paires conjuguées pour une preuve lisible, et sélection parmi les10 mineurs pour des contrastes supplémentaires. Aucune optimalité globale ni confirmation statistique n’est revendiquée.
- Un contrôle supplémentaire purement rationnel des sommes de Gauss a été ajouté après le premier calcul. Il vérifie les constantes nécessaires à la non-annulation ; il ne constitue pas une prévision de zéros.
