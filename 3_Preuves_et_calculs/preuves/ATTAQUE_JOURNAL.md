# Journal de l'attaque 2 (projection de Nyman–Beurling) — v5.4

Chaque itération prolonge la Gram sans carré et analyse le plus grand bloc complet. Colonnes « × κ/log N » = e²·log N/κ (1 = constante de Burnol–BCF). Aucune ligne de ce journal n'est une preuve.

## Itérations

- **2026-10-05 00:49** — NMAX=500, entrées calculées ce tour : 5209, restantes : 2288, bloc complet jusqu'à N = 485, nouveaux N analysés : [50, 100, 150, 200, 250, 300, 350, 400, 450]
- **2026-10-05 00:50** — NMAX=500, entrées calculées ce tour : 2288, restantes : 0, bloc complet jusqu'à N = 499, nouveaux N analysés : aucun
- **2026-10-05 00:52** — NMAX=1000, entrées calculées ce tour : 5359, restantes : 132806, bloc complet jusqu'à N = 527, nouveaux N analysés : [500]
- **2026-10-05 00:56** — NMAX=1000, entrées calculées ce tour : 10316, restantes : 122490, bloc complet jusqu'à N = 579, nouveaux N analysés : aucun
- **2026-10-05 01:00** — NMAX=1000, entrées calculées ce tour : 9566, restantes : 112924, bloc complet jusqu'à N = 619, nouveaux N analysés : [600]
- **2026-10-05 01:04** — NMAX=1000, entrées calculées ce tour : 8755, restantes : 104169, bloc complet jusqu'à N = 658, nouveaux N analysés : aucun
- **2026-10-05 01:08** — NMAX=1000, entrées calculées ce tour : 7992, restantes : 96177, bloc complet jusqu'à N = 689, nouveaux N analysés : aucun
- **2026-10-05 01:12** — NMAX=1000, entrées calculées ce tour : 7825, restantes : 88352, bloc complet jusqu'à N = 717, nouveaux N analysés : [700]
- **2026-10-05 01:13** — *Contrôle avant interprétation* : 30 entrées recalculées avec Y = 3·10⁵ : écart relatif ≤ 1,3·10⁻¹² ; conditionnement ≈ 10⁶ à N = 700. L'optimum sans carré passe **sous** κ/log N (rapports 1,006 ; 1,004 ; 1,005 ; 1,006 ; 0,991 ; 0,978 ; 0,980 pour N = 600…710). Ce n'est pas une contradiction : la borne de Burnol est un liminf et κ/log N n'est que le terme principal (corrections relatives ≈ 1/log N). À ne pas lire comme une borne ponctuelle, dans un sens ou dans l'autre.
- **2026-10-05 01:17** — NMAX=1000, entrées calculées ce tour : 6722, restantes : 81630, bloc complet jusqu'à N = 745, nouveaux N analysés : aucun
- **2026-10-05 05:13** — NMAX=1000, entrées calculées ce tour : 6980, restantes : 74650, bloc complet jusqu'à N = 769, nouveaux N analysés : aucun
- **2026-10-05 05:17** — NMAX=1000, entrées calculées ce tour : 6848, restantes : 67802, bloc complet jusqu'à N = 791, nouveaux N analysés : aucun
- **2026-10-05 05:22** — NMAX=1000, entrées calculées ce tour : 6670, restantes : 61132, bloc complet jusqu'à N = 813, nouveaux N analysés : [800]
- **2026-10-05 05:26** — NMAX=1000, entrées calculées ce tour : 5372, restantes : 55760, bloc complet jusqu'à N = 830, nouveaux N analysés : aucun
- **2026-10-05 05:28** — NMAX=1000, entrées calculées ce tour : 5045, restantes : 56087, bloc complet jusqu'à N = 829, nouveaux N analysés : aucun
- **2026-10-05 05:33** — NMAX=1000, entrées calculées ce tour : 6414, restantes : 49673, bloc complet jusqu'à N = 857, nouveaux N analysés : aucun
- **2026-10-05 05:37** — NMAX=1000, entrées calculées ce tour : 6341, restantes : 43332, bloc complet jusqu'à N = 877, nouveaux N analysés : aucun
- **2026-10-05 05:41** — NMAX=1000, entrées calculées ce tour : 6037, restantes : 37295, bloc complet jusqu'à N = 894, nouveaux N analysés : aucun
- **2026-10-05 05:45** — NMAX=1000, entrées calculées ce tour : 6074, restantes : 31221, bloc complet jusqu'à N = 910, nouveaux N analysés : [900]
- **2026-10-05 05:50** — NMAX=1000, entrées calculées ce tour : 5584, restantes : 25637, bloc complet jusqu'à N = 926, nouveaux N analysés : aucun
- **2026-10-05 05:54** — NMAX=1000, entrées calculées ce tour : 5749, restantes : 19888, bloc complet jusqu'à N = 942, nouveaux N analysés : aucun
- **2026-10-05 05:58** — NMAX=1000, entrées calculées ce tour : 5422, restantes : 14466, bloc complet jusqu'à N = 958, nouveaux N analysés : aucun
- **2026-10-05 07:41** — NMAX=1000, entrées calculées ce tour : 5692, restantes : 8774, bloc complet jusqu'à N = 974, nouveaux N analysés : aucun
- **2026-10-05 07:45** — NMAX=1000, entrées calculées ce tour : 5275, restantes : 3499, bloc complet jusqu'à N = 989, nouveaux N analysés : aucun
- **2026-10-05 07:48** — NMAX=1000, entrées calculées ce tour : 3499, restantes : 0, bloc complet jusqu'à N = 998, nouveaux N analysés : aucun
- **2026-10-05 07:48** — NMAX=1000, entrées calculées ce tour : 0, restantes : 0, bloc complet jusqu'à N = 998, nouveaux N analysés : [998]
- **2026-10-05 08:03** — Test de l'estimation sous RH (terme principal κ∫P′²/log N) : non atteinte pour N ≤ 998 ; 1 − x : (R−1)·log N = 77,3 → 77,1 ; poids plats en 0 ordonnés par |P″(0)| ; 1 − x^k (k ≥ 3) stables mais R = 0,6–0,82. Voir 11_Estimation_sous_RH.
- **2026-10-05 18:08** — Annulation du pôle (document reçu) vérifiée : identité exacte, extension à N = 10⁵ (1,29 → 1,31), b_N → −1 − 2γ/log N jusqu'à 10⁷, retour exact à Q. Branche close. Voir 12_Annulation_du_pole.