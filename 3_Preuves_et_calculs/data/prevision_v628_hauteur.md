# Prévisions V6.28 — Axe A, la Rencontre à n en hauteur (écrites avant le calcul)

Auteur et titulaire des droits : Vincent NOËL. Écrit le 11 octobre 2026 à 23:35 UTC (horloge du conteneur), avant tout calcul.

Doc. 43 : 0 triplet de zéros de ζ dans la zone x, y < 0,5 (écarts dépliés) pour 4,4 attendus par le noyau sinus.
Explication testée : l'effet de hauteur finie de Bogomolny et al., par la formule det[D_N] (doc. 43) prolongée aux N réels,
D_N(s) = sin(πs)/(N sin(πs/N)), avec N = N_eff(γ) = log(γ/2π)/√(12Λ), Λ = 1,57314 (défini pour s < N ; N_eff ≈ 0,4 à 1,25 ici).
- A1 : avec N = N_eff(γ) de chaque origine, la masse attendue de la zone x, y < 0,5 tombe sous 1,5 (contre 4,4), et
  « 0 observé » devient compatible (probabilité de Poisson ≥ 0,2).
- A2 : un N unique ajusté sur les triplets de la zone x + y ≤ 1 vaut entre 1,0 et 1,5, cohérent avec N ≈ 1,2–1,3 tiré des paires
  au doc. 41.
- A3 : le même N, appliqué aux paires (marges < 0,1), redonne le nombre observé (4) à ± 2 près.
