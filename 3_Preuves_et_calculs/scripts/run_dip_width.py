#!/usr/bin/env python3
"""V6.3e — La largeur du creux mesure-t-elle la distance du zéro à la droite Re s = 1 ?

Heuristique (terme diagonal de la corrélation de paires, proportionnel à Re (zeta'/zeta)'(1 + ir)) :
un zéro rho = beta + i gamma de zeta creuse, dans la densité des différences de zéros autour de gamma,
un profil  -depth * w^2 (w^2 - x^2) / (w^2 + x^2)^2  de demi-largeur w = 1 - beta.
Sur la droite critique : w = 1/2. On ajuste w sur les différences des zéros de zeta, de L(s, chi_5)
et de Davenport–Heilbronn (zéros de la droite), en faisant varier le pas et la fenêtre d'ajustement.
Sorties : data/zero_difference_dip_width.csv.
"""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
from scipy.optimize import curve_fit
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from explicit_formula import load_zeros
from zero_reconstruction import nontrivial_zeros

gz = np.sort(load_zeros()[0])
zl = nontrivial_zeros("L_chi5"); zd = nontrivial_zeros("DH")
SETS = {"zeta": gz, "L_chi5": np.sort(zl.imag[zl.imag > 0]),
        "DH": np.sort(zd[(np.abs(zd.real - 0.5) < 1e-6) & (zd.imag > 0)].imag)}

def diffs(S):
    i, j = np.triu_indices(len(S), k=1); return np.sort(S[j] - S[i])
def profile(S, bw, X):
    D = diffs(S); rmax = min(D[-1], gz.max()) - 8.0; Zc = gz[(gz > 10) & (gz < rmax)]
    edges = np.arange(-X, X + bw / 2, bw); xc = 0.5 * (edges[1:] + edges[:-1]); h = np.zeros(len(xc)); bg = 0.0
    for z in Zc:
        h += np.histogram(D[np.searchsorted(D, z - X - 1):np.searchsorted(D, z + X + 1)] - z, bins=edges)[0]
        bg += (np.searchsorted(D, z + 8) - np.searchsorted(D, z - 8)) / 16.0 * bw
    return xc, h / bg, np.sqrt(np.maximum(h, 1)) / bg
def model(x, depth, w, c):
    return c - depth * w * w * (w * w - x * x) / (w * w + x * x) ** 2
def chi2_fixed(x, y, e, wf):
    q, _ = curve_fit(lambda x, d, c: model(x, d, wf, c), x, y, p0=(0.3, 1.0), sigma=e, absolute_sigma=True)
    return float(np.sum(((y - model(x, q[0], wf, q[1])) / e) ** 2) / (len(x) - 2))

rows = []
for name, S in SETS.items():
    for bw in (0.05, 0.1):
        for X in (1.2, 1.6, 2.0):
            x, y, e = profile(S, bw, X)
            p, cov = curve_fit(model, x, y, p0=(0.3, 0.5, 1.0), sigma=e, absolute_sigma=True,
                               bounds=([0.0, 0.05, 0.5], [2.0, 2.0, 1.5]))
            rows.append(dict(objet=name, pas=bw, fenetre=X, largeur=float(p[1]), incertitude_stat=float(math.sqrt(cov[1, 1])),
                             profondeur=float(p[0]), chi2_par_ddl=float(np.sum(((y - model(x, *p)) / e) ** 2) / (len(x) - 3)),
                             chi2_largeur_0_3=chi2_fixed(x, y, e, 0.3), chi2_largeur_0_5=chi2_fixed(x, y, e, 0.5),
                             chi2_largeur_0_7=chi2_fixed(x, y, e, 0.7)))
df = pd.DataFrame(rows); df.to_csv(ROOT / "data" / "zero_difference_dip_width.csv", index=False)
pd.set_option("display.width", 250)
print(df.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
print(df.groupby("objet").largeur.agg(["min", "max", "mean"]).round(3))
