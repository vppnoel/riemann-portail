#!/usr/bin/env python3
"""V6.5.1 — Le morceau PROUVÉ de RH tient-il ailleurs qu'au point d'Euler ?

Théorème (Hadamard, de la Vallée Poussin, 1896, étendu aux fonctions L de Dirichlet) : un produit d'Euler de
ce type n'a aucun zéro pour Re s >= 1. La preuve utilise le produit d'Euler et une positivité : 3 + 4 cos x + cos 2x >= 0.
Dans la famille F_theta (même équation fonctionnelle partout, produit d'Euler seulement en theta = 0), on compte
par le principe de l'argument les zéros à droite de Re s = sigma_0, pour 0 < t <= 1000.
Sorties : data/family_mod7_right_count.csv, data/family_mod7_rightmost.csv.
"""
from pathlib import Path
import sys, math, time
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from family_mod7 import coefficients
from zero_reconstruction import hurwitz_zeta

TMAX, BAND = 1000.0, 50.0

def make_F(theta):
    w = coefficients(theta, 6)[1:]                      # F_theta(s) = 7^-s somme_a a_theta(a) zeta(s, a/7)
    def F(s):
        s = complex(s); return 7.0 ** (-s) * sum(w[a - 1] * hurwitz_zeta(s, a / 7.0) for a in range(1, 7))
    return F
def winding(F, x0, x1, y0, y1, h):
    pts = []
    for a, b in ((complex(x0, y0), complex(x1, y0)), (complex(x1, y0), complex(x1, y1)), (complex(x1, y1), complex(x0, y1)), (complex(x0, y1), complex(x0, y0))):
        n = max(8, int(abs(b - a) / h)); pts += [a + (b - a) * k / n for k in range(n)]
    v = np.array([F(p) for p in pts]); v = np.append(v, v[0]); d = np.angle(v[1:] / v[:-1])
    return float(np.sum(d) / (2 * math.pi)), float(np.max(np.abs(d)))
def count_right(F, sigma0):
    tot, worst = 0, 0.0
    for y0 in np.arange(0.0001, TMAX, BAND):
        h = 0.02
        w, dmax = winding(F, sigma0, 4.0, y0, min(y0 + BAND, TMAX), h)
        while dmax > 1.2 and h > 0.0015:               # un zéro proche du bord : resserrer le pas
            h /= 4; w, dmax = winding(F, sigma0, 4.0, y0, min(y0 + BAND, TMAX), h)
        assert abs(w - round(w)) < 1e-6
        tot += round(w); worst = max(worst, dmax)
    return tot, worst
def newton(F, s, it=80, h=1e-5):
    for _ in range(it):
        ds = F(s) / ((F(s + h) - F(s - h)) / (2 * h))
        if abs(ds) > 0.2: ds *= 0.2 / abs(ds)
        s -= ds
        if abs(ds) < 1e-13: break
    return s

if __name__ == "__main__":
    t0 = time.time(); rows, right = [], []
    for theta in (0.0, 0.5, 1.0, -0.5, -1.0):
        F = make_F(theta); row = dict(theta=theta)
        for sigma0 in (0.75, 1.0):
            n, worst = count_right(F, sigma0); row[f"zeros_a_droite_de_{sigma0}"] = n; row[f"pas_de_phase_max_{sigma0}"] = worst
        rows.append(row); print(row, f"{time.time() - t0:.0f} s", flush=True)
        # zéro le plus à droite : départs de Newton sur une grille, à droite de 0,6
        best = None
        for t in np.arange(2.0, TMAX, 2.0):
            for sg in (0.8, 1.1):
                z = newton(F, complex(sg, t))
                if abs(F(z)) < 1e-10 and 0.5 + 1e-6 < z.real < 4 and 0 < z.imag < TMAX and (best is None or z.real > best.real): best = z
        right.append(dict(theta=theta, sigma_max=(best.real if best is not None else 0.5), t=(best.imag if best is not None else float("nan"))))
        print(right[-1], f"{time.time() - t0:.0f} s", flush=True)
    pd.DataFrame(rows).to_csv(ROOT / "data" / "family_mod7_right_count.csv", index=False)
    pd.DataFrame(right).to_csv(ROOT / "data" / "family_mod7_rightmost.csv", index=False)
