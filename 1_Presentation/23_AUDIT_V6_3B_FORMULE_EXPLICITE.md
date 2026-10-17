# V6.3b/c — Audit des conventions de la formule explicite (DUAL-LOCK)

**Date :** 5 octobre 2026
**Statut :** audit numérique — conventions validées ; aucune revendication nouvelle sur RH

## 1. La question
La V6.3a (§8, point 6) demandait, avant toute interprétation, d'auditer les conventions de la formule explicite utilisées par DUAL-LOCK : normalisation de Fourier, facteurs 2π, facteur gamma, coefficients de Davenport–Heilbronn [DH36b] [DH36a] (DH).

## 2. Le test
La compression construite **côté premiers** par `compression_accurate`

- archimédien : (1/2π) ∫ H_i(t) H_j(t) Re ψ((1/2 + a + it)/2) dt, avec a la parité ;
- conducteur : log(q/π) · (f_i ∗ f_j)(0) ;
- pôle (ζ seulement) : 2 H_i(i/2) H_j(i/2) ;
- local : −2 Σ_n Re Λ_f(n) n^{−1/2} (f_i ∗ f_j)(log n), avec H(t) = ∫ f(x) e^{itx} dx

doit coïncider avec la **somme directe sur les zéros**

  Z_ij = Σ_ρ H_i(γ_ρ) H_j(γ_ρ),  γ_ρ = −i(ρ − 1/2).

Zéros utilisés : les 300 premiers zéros de ζ (et leurs opposés) ; pour DH, `data/dh_zeros.csv` (t ≤ 200), complété par les partenaires 1 − σ des zéros hors droite et par les conjugués. Script : `3_Preuves_et_calculs/scripts/run_explicit_formula_audit.py`.

## 3. Résultat : les deux côtés coïncident

| Objet | T | demi-largeur | écart relatif ‖M − Z‖/‖Z‖ | λ_G côté premiers | λ_G côté zéros |
|---|---:|---:|---:|---:|---:|
| ζ | 20 | 2,5 | 5,3·10⁻⁹ | +1,3728·10⁻⁵ | +1,3735·10⁻⁵ |
| ζ | 40 | 2,5 | 5,1·10⁻⁹ | +1,9474·10⁻⁴ | +1,9475·10⁻⁴ |
| DH | 86 | 2,5 | 5,3·10⁻⁷ | −1,51596 | −1,51596 |
| DH | 113 | 2,5 | 2,7·10⁻⁷ | −0,30364 | −0,30364 |
| DH | 167 | 3,5 | 2,4·10⁻⁷ | −0,17525 | −0,17525 |
| DH | 176 | 2,5 | 1,4·10⁻⁶ | −0,55085 | −0,55126 |

(dimension 5, pas de fréquence 0,6, λ_G = plus petite valeur propre généralisée M v = λ G v.)

**Les conventions sont correctes** pour ζ (5·10⁻⁹) et pour DH (≤ 1,4·10⁻⁶ ; l'écart le plus grand, à T = 176, suit le conditionnement de G signalé en V6.3a ; **précision V6.4 :** il vient en fait de la quadrature adaptative, Gauss–Legendre y coïncide avec les zéros à 2·10⁻⁹ près, voir le document 26).

## 4. Attribution exacte de chaque direction négative
Avec le vecteur propre généralisé v (vᵀGv = 1), λ_G = vᵀZv se répartit entre les zéros :

| T | λ_G | zéros sur la droite (≥ 0) | quadruplet hors droite responsable | autres quadruplets |
|---:|---:|---:|---|---:|
| 86 | −1,516 | +0,103 | 0,8085 + 85,699i : **−1,619** | < 10⁻⁴ |
| 113 | −0,304 | +0,045 | 0,6508 + 114,163i : **−0,348** | < 10⁻⁴ |
| 167 | −0,175 | +0,010 | 0,5744 + 166,479i : **−0,186** | < 2·10⁻⁴ |
| 176 | −0,551 | +0,255 | 0,7243 + 176,702i : **−0,807** | < 10⁻⁴ |

Chaque témoin négatif est expliqué, à 10⁻⁴ près, par **un seul quadruplet de zéros hors de la droite** (ρ, 1 − ρ̄ et leurs conjugués) ; les zéros sur la droite apportent une masse positive qui compense en partie.

## 5. Conséquences
1. **L'instrument DUAL-LOCK calcule exactement une compression de la forme de Weil [Wei52].** Ses directions négatives pour DH sont les zéros hors droite de DH, comme le prédit le critère de Weil. Il ne contient pas d'information au-delà des zéros.
2. **Le « Résidu sombre » reçoit une lecture exacte côté zéros** : masse positive des zéros sur la droite contre contribution négative du quadruplet hors droite (rapports 0,06 ; 0,13 ; 0,06 ; 0,32). Les facteurs d'amplification côté premiers (V6.3a §7) sont une autre façon de mesurer cette compensation.
3. **Correction d'un ancien constat (v3.3)** : la liste DH comptait 125 zéros pour ≈ 129,5 attendus jusqu'à t = 200. Les 4 « manquants » étaient les partenaires 1 − σ des zéros hors droite, que la recherche par Newton n'avait pas visés. Avec eux : 129 zéros, en accord avec la formule asymptotique.
   **Correction V6.3d :** ce comptage était encore faux. Deux zéros bas (t = 5,0942 et t = 8,9399) manquaient aussi, la recherche d'origine partant de t = 10. Comptage exact par le principe de l'argument : 130 zéros pour 0 < t ≤ 200,5. Les fenêtres de cet audit (T ≥ 86) ne voient pas ces zéros : les tableaux ci-dessus sont inchangés (variation ≤ 7·10⁻⁷). Voir `24_CLASSEMENT_DES_INSTRUMENTS_V6_3D.md`, §6.
4. Pour ζ, la forme est positive aux hauteurs testées, ce qui est attendu : RH y est vérifiée numériquement. L'instrument ne peut rien dire au-delà.

## 6. Limites
- (V6.3c) Le contrôle L(s, χ₅) est maintenant audité contre ses propres zéros (§8).
- Dimension 5 et quatre témoins seulement ; zéros de DH limités à t ≤ 200 (suffisant pour ces fenêtres : contribution des zéros plus hauts négligeable).
- Audit de cohérence : aucune information nouvelle sur RH.

## 7. Décision proposée
DUAL-LOCK passe du statut « instrument à auditer » à **« instrument validé et entièrement expliqué »** : c'est le critère de Weil, comprimé et rendu visible. Le garder comme détecteur pédagogique et comme entrée du banc d'audit ; ne pas l'interpréter au-delà de ce qu'il mesure.


## 8. Complément V6.3c : le contrôle eulérien L(s, χ₅)

Zéros calculés : 334 zéros de L(s, χ₅) pour |t| ≤ 245, tous sur la droite critique (script `compute_L_chi5_zeros.py`, fichier `data/L_chi5_zeros.csv`). Comptage contre la formule asymptotique : 107 (attendu 107,5) pour |t| ≤ 100 ; 258 (259,1) pour |t| ≤ 200 ; 325 (324,8) pour |t| ≤ 240.

| T | demi-largeur | écart relatif ‖M − Z‖/‖Z‖ | λ_G côté premiers | λ_G côté zéros |
|---:|---:|---:|---:|---:|
| 86 | 2,5 | 1,1·10⁻⁸ | +1,96003 | +1,96003 |
| 113 | 2,5 | 1,7·10⁻⁸ | +2,41599 | +2,41598 |
| 167 | 3,5 | 2,7·10⁻⁸ | +2,37046 | +2,37045 |
| 176 | 2,5 | 9,3·10⁻⁸ | +3,13857 | +3,13857 |

**Le contrôle est validé** : côté premiers et côté zéros coïncident, et la forme est positive parce que tous les zéros trouvés sont sur la droite.

**L'audit attrape aussi les listes de zéros incomplètes.** Un premier passage donnait un écart de 5·10⁻⁵ à T = 113 et 4·10⁻⁴ à T = 116, toujours dans le même sens (côté premiers plus grand). Un comptage par changements de signe d'une fonction réelle de type Hardy a montré qu'un zéro manquait à t = −119,999 (perdu à la frontière entre deux tranches de recherche). Une fois ajouté, l'écart retombe à 2·10⁻⁸. La réconciliation premiers/zéros sert donc aussi de test de complétude d'une liste de zéros.

## 9. Positionnement

Le calcul de formes de Weil tronquées est un domaine actif : Connes–Consani–Moscovici [CCM25] (arXiv:2511.22755), Connes–van Suijlekom [CvS25] (arXiv:2511.23257), l'opérateur de Suzuki [Suz26] (arXiv:2606.09096) et sa réalisation numérique (Kim et al., arXiv:2607.24830), dont le point R6 est très proche de DUAL-LOCK. DUAL-LOCK doit être présenté comme une réalisation pédagogique de ce mécanisme, sans revendication de nouveauté. Ces références sont lues sur résumés et pages.

<!-- references:debut -->

## Références

Format : [clé] auteurs, *titre*, publication, lien. Fiches complètes et état de vérification : document 42 (registre des sources).

- [CCM25] A. Connes, C. Consani, H. Moscovici. *Zeta spectral triples*. arXiv:2511.22755 (27 nov. 2025). <https://arxiv.org/abs/2511.22755> — vérifié en ligne. **Correctif V6.18 :** Le titre est « Zeta spectral triples » ; le résumé parle d'une réalisation spectrale des zéros, pas explicitement de formes de Weil tronquées.
- [CvS25] A. Connes, W. D. van Suijlekom. *Quadratic forms, real zeros and echoes of the spectral action*. arXiv:2511.23257 (28 nov. 2025). <https://arxiv.org/abs/2511.23257> — vérifié en ligne
- [DH36a] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series*. J. London Math. Soc. 11 (1936), no. 3, 181–185. <https://doi.org/10.1112/jlms/s1-11.3.181> — partiellement vérifié
- [DH36b] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series. II*. J. London Math. Soc. 11 (1936), no. 4, 307–312. <https://doi.org/10.1112/jlms/s1-11.4.307> — partiellement vérifié
- [Suz26] M. Suzuki. *Weil's quadratic form via the screw function*. arXiv:2606.09096 (juin 2026 ; v3 du 23 sept. 2026). <https://arxiv.org/abs/2606.09096> — vérifié en ligne
- [Wei52] A. Weil. *Sur les « formules explicites » de la théorie des nombres premiers*. Comm. Sém. Math. Univ. Lund, vol. suppl. dédié à M. Riesz (1952), 252–265. <https://en.wikipedia.org/wiki/Weil%27s_criterion> — partiellement vérifié

<!-- references:fin -->
