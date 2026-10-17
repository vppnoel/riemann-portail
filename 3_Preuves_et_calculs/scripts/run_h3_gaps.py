#!/usr/bin/env python3
"""v4.7 : statistiques de petits écarts entre les 300 premiers zéros et somme de paires (hypothèse H3 de la Proposition C)."""
from pathlib import Path
import sys, math, csv
import numpy as np
from scipy.integrate import quad
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from explicit_formula import load_zeros
gam, _ = load_zeros(); rho = np.abs(0.5 + 1j * gam)
d = np.diff(gam); sp = 2 * np.pi / np.log(gam[1:] / (2 * np.pi)); r = d / sp
def S(N):
    g = gam[:N]; R = rho[:N]; M = np.abs(g[:, None] - g[None, :]); np.fill_diagonal(M, np.inf)
    return float(np.sum(1.0 / (R[:, None] * R[None, :] * M)))
rows = [dict(N=N, S_pair=S(N)) for N in (25, 50, 100, 200, 300)]
eta = 0.05
kint = quad(lambda x: (8 * eta ** 3 - 6 * eta * x * x) / (4 * eta ** 2 + x * x) ** 3, -np.inf, np.inf)[0]
out = dict(min_ecart=float(d.min()), min_ecart_normalise=float(r.min()), E_inverse_s=float(np.mean(1 / r)),
           fraction_sous_0_3=float(np.mean(r < 0.3)), integrale_noyau_croise=float(kint))
with open(ROOT / "data" / "h3_gaps.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["cle", "valeur"])
    for k, v in out.items(): w.writerow([k, repr(v)])
    for x in rows: w.writerow([f"S_pair_N{x['N']}", repr(x['S_pair'])])
print(out); print(rows)
