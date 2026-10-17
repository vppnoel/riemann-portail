#!/usr/bin/env python3
"""V6.3d — Le bispectre dans le canal t : la fermeture ternaire EST le défaut multiplicatif.

Dans le signal t -> F(sigma + it), les fréquences sont les log n, et log m + log n = log(mn) est une
résonance exacte. Le coefficient de Bohr mesuré à la fréquence log n redonne a(n) ; le défaut de
fermeture ternaire mesuré coïncide donc avec le défaut multiplicatif des coefficients (tautologie).
(Le canal u = log t, où le signal est une somme de tons aux ordonnées des zéros, est traité par
scripts/run_zero_difference_resonances.py.)
Sortie : data/tomo3_bohr_closure.csv.
"""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from rejection import coeffs
from dark_zeta import steinhaus_completely_multiplicative

# ---------- coefficients de Bohr de t -> F(sigma + it) et fermeture ternaire
NMAX, SIGMA, T, DT = 60, 1.0, 4000.0, 0.02
t = np.arange(-T, T + DT / 2, DT)
win = np.exp(-0.5 * (t / (T / 4)) ** 2); win /= win.sum()     # fenêtre gaussienne normalisée
logn = np.log(np.arange(1, NMAX + 1))
objs = {"zeta": coeffs("zeta", NMAX), "L_chi5": coeffs("L_chi5", NMAX), "DH": coeffs("DH", NMAX),
        "steinhaus": steinhaus_completely_multiplicative(NMAX, seed=0)}
pairs = [(m, n) for m in range(2, NMAX + 1) for n in range(m + 1, NMAX + 1) if m * n <= NMAX and math.gcd(m, n) == 1]
rowsB = []
for name, a in objs.items():
    F = np.zeros(len(t), dtype=complex)
    for n in range(1, NMAX + 1):
        F += a[n] * n ** (-SIGMA) * np.exp(-1j * t * logn[n - 1])
    bohr = np.array([np.sum(win * F * np.exp(1j * t * logn[n - 1])) * n ** SIGMA for n in range(1, NMAX + 1)])
    err = float(np.max(np.abs(bohr - a[1:])))
    def defect(c):
        num = sum(abs(c[m * n - 1] - c[m - 1] * c[n - 1]) ** 2 for m, n in pairs)
        den = sum(abs(c[m * n - 1]) ** 2 + abs(c[m - 1] * c[n - 1]) ** 2 for m, n in pairs)
        return float(num / den) if den > 0 else 0.0
    rowsB.append(dict(objet=name, triades=len(pairs), erreur_max_coefficients_de_Bohr=err,
                      defaut_de_fermeture_mesure=defect(bohr), defaut_multiplicatif_des_coefficients=defect(a[1:])))
dB = pd.DataFrame(rowsB); dB.to_csv(ROOT / "data" / "tomo3_bohr_closure.csv", index=False)
print(dB.to_string(index=False, float_format=lambda v: f"{v:.4g}"))
