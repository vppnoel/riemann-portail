#!/usr/bin/env python3
"""Moment de Gonek-Hughes-Keating-O'Connell : S(T)=sum_{|gamma|<=T} 1/|zeta'(rho)|^2 vs (6/pi^3) T.
Condition (2) de Bettin-Conrey-Farmer : S(T) << T^{3/2-delta}. Test numérique sur les 300 premiers zéros."""
from pathlib import Path
import sys, math, csv
import numpy as np, mpmath as mp
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from explicit_formula import load_zeros
mp.mp.dps = 20
gam, _ = load_zeros()
vals = []
for g in gam:
    rho = mp.mpc(0.5, g)
    vals.append(float(abs(mp.zeta(rho, derivative=1))))
vals = np.array(vals)
with open(ROOT / "data" / "zeta_prime_at_zeros.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["gamma", "abs_zeta_prime"])
    for g, v in zip(gam, vals): w.writerow([repr(float(g)), repr(float(v))])
rows = []
for n in [30, 60, 100, 150, 200, 250, 300]:
    T = gam[n - 1]
    S = 2 * np.sum(1 / vals[:n] ** 2)                     # zéros +/- gamma
    rows.append((n, T, S, 6 / math.pi ** 3 * T, S / (6 / math.pi ** 3 * T)))
print("n_zéros   T        S(T)     (6/pi^3)T   ratio")
for r in rows: print("%5d %8.2f %9.3f %10.3f %7.3f" % r)
# exposant effectif entre T=100 et T=gam[-1]
i100 = int(np.searchsorted(gam, 100.0))
S100 = 2 * np.sum(1 / vals[:i100] ** 2); Smax = 2 * np.sum(1 / vals ** 2)
print("exposant effectif de S(T) entre T=%.1f et T=%.1f : %.3f (condition (2) exige < 3/2)" %
      (gam[i100 - 1], gam[-1], math.log(Smax / S100) / math.log(gam[-1] / gam[i100 - 1])))
print("plus petit |zeta'(rho)| :", vals.min(), "à gamma =", gam[np.argmin(vals)])
with open(ROOT / "data" / "gonek_moment.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["n_zeros", "T", "S_T", "gonek_6_over_pi3_T", "ratio"])
    for r in rows: w.writerow(r)
