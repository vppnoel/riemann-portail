#!/usr/bin/env python3
"""V6.3d — Le signal TOMO reconstruit à partir des zéros seuls.

Pour zeta, L(s, chi_5) et Davenport–Heilbronn :
  1. g_sigma(u) calculé à partir des coefficients c_F(n) (aucun zéro) ;
  2. g_sigma(u) reconstruit par la somme sur les zéros (non triviaux, triviaux, s = 0) ;
  3. écart relatif ; entropie TOMO-2 des deux signaux ;
  4. pour DH : part d'énergie des zéros hors droite, et entropie TOMO-2 sans eux.
Le lissage gaussien (sigma en u) est appliqué exactement des deux côtés.
Sorties : data/tomo_zero_reconciliation.csv, data/tomo_zero_attribution_DH.csv.
"""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from zero_reconstruction import zero_terms, g_from_zeros, g_from_coefficients, coefficients_c
from dark_zeta import tomo2_gram, tomo2_metrics

N, NLOG, U_MIN, NSHIFT, SHIFT_STEP = 32768, 4096, 2.0, 32, 8
SIGMAS = (0.04, 0.02, 0.01)

def norm(g):
    g = g - np.mean(g); return g / np.sqrt(np.mean(np.abs(g) ** 2))
def entropy(g):
    return tomo2_metrics(tomo2_gram(norm(g), n_shifts=NSHIFT, shift_step=SHIFT_STEP)).entropy

u = np.linspace(U_MIN, math.log(N), NLOG, endpoint=False)
rows, attrib = [], []
for kind in ("zeta", "L_chi5", "DH"):
    c = coefficients_c(kind, int(N * math.exp(6 * max(SIGMAS))) + 10)
    terms = zero_terms(kind)
    nz = int(np.sum(np.isin(terms["family"], ("sur_droite", "hors_droite"))))
    for s in SIGMAS:
        gc = g_from_coefficients(c, u, s); gz = g_from_zeros(terms, u, s)
        rows.append(dict(objet=kind, sigma=s, zeros_utilises=nz,
                         ecart_rel_L2=float(np.linalg.norm(gc - gz) / np.linalg.norm(gc)),
                         ecart_max=float(np.max(np.abs(gc - gz))), amplitude_rms=float(np.sqrt(np.mean(np.abs(gc) ** 2))),
                         entropie_TOMO2_coefficients=entropy(gc), entropie_TOMO2_zeros=entropy(gz)))
        if kind == "DH":
            g_off = g_from_zeros(terms, u, s, families=("hors_droite",))
            g_on = gz - g_off
            E = lambda x: float(np.mean(np.abs(x) ** 2))
            half = u >= 0.5 * (U_MIN + math.log(N))
            attrib.append(dict(sigma=s, energie_totale=E(gz), part_hors_droite=E(g_off) / E(gz),
                               part_reste=E(g_on) / E(gz), terme_croise=1 - (E(g_off) + E(g_on)) / E(gz),
                               part_hors_droite_moitie_haute=E(g_off[half]) / E(gz[half]),
                               entropie_TOMO2_tous_zeros=entropy(gz), entropie_TOMO2_sans_hors_droite=entropy(g_on)))
df = pd.DataFrame(rows); df.to_csv(ROOT / "data" / "tomo_zero_reconciliation.csv", index=False)
da = pd.DataFrame(attrib); da.to_csv(ROOT / "data" / "tomo_zero_attribution_DH.csv", index=False)
pd.set_option("display.width", 250)
print(df.to_string(index=False, float_format=lambda x: f"{x:.6g}")); print(); print(da.T.to_string(float_format=lambda x: f"{x:.5g}"))
