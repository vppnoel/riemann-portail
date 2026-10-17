#!/usr/bin/env python3
"""V6.3d — Zéros de L(s, chi_5) et de Davenport–Heilbronn jusqu'à |t| <= 600, sans mpmath.

Méthode : minima locaux de |F| sur plusieurs droites verticales, puis Newton ; ajout des partenaires
1 - conj(rho) imposés par l'équation fonctionnelle (DH) ; contrôle de complétude par le principe de
l'argument, bande par bande (rectangle -0,9 <= Re s <= 4). Une bande en désaccord est reprise avec
une grille de départs plus dense.
Sorties : data/L_chi5_zeros_600.csv, data/dh_zeros_600.csv, data/zeros_600_count_audit.csv.
"""
from pathlib import Path
import sys, math, time
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
from zero_reconstruction import F_eval, taylor
from audit_dh_zero_count import winding

TMAX, BAND = 600.0, 20.0

def newton(kind, z, it=40):
    for _ in range(it):
        c0, c1, _ = taylor(kind, z, r=0.01, n=8)
        if c1 == 0: return None
        dz = c0 / c1
        if abs(dz) > 0.5: dz *= 0.5 / abs(dz)
        z -= dz
        if abs(dz) < 1e-13: break
    return z if abs(F_eval(kind, z)) < 1e-9 else None

def add(found, z, y0, y1):
    if z is not None and -0.9 < z.real < 4.0 and y0 < z.imag <= y1 and all(abs(z - w) > 1e-6 for w in found):
        found.append(z); return True
    return False

def search_band(kind, y0, y1, sigmas, dt):
    found = []
    t = np.arange(y0 - 0.5, y1 + 0.5, dt)
    for s0 in sigmas:
        v = np.abs(np.array([F_eval(kind, complex(s0, x)) for x in t]))
        for k in np.flatnonzero((v[1:-1] < v[:-2]) & (v[1:-1] <= v[2:])) + 1:
            z = newton(kind, complex(s0, t[k]))
            if add(found, z, y0, y1) and kind == "DH" and abs(z.real - 0.5) > 1e-7:
                add(found, newton(kind, complex(1 - z.real, z.imag)), y0, y1)
    return found

def run(kind, t_lo, t_hi):
    zeros, audit = [], []
    edges = np.arange(t_lo, t_hi + 1e-9, BAND)
    for y0, y1 in zip(edges[:-1], edges[1:]):
        w, dmax = winding(kind, -0.9, 4.0, y0, y1, h=0.01)
        if dmax > 1.0: w, dmax = winding(kind, -0.9, 4.0, y0, y1, h=0.002)
        target = round(w)
        found = search_band(kind, y0, y1, (0.5, 0.75, 1.02), 0.02)
        if len(found) != target:
            found = search_band(kind, y0, y1, (0.5, 0.3, 0.6, 0.7, 0.8, 0.9, 1.02, 1.15, 1.3), 0.005)
        audit.append(dict(objet=kind, t_min=y0, t_max=y1, comptage_argument=target, zeros_trouves=len(found),
                          pas_de_phase_max=dmax))
        zeros += found
        print(audit[-1], flush=True)
    return zeros, audit

if __name__ == "__main__":
    t0 = time.time(); audits = []
    zl, a = run("L_chi5", -TMAX + 0.5, TMAX + 0.5); audits += a
    pd.DataFrame(dict(sigma=[z.real for z in zl], t=[z.imag for z in zl])).sort_values("t").to_csv(
        ROOT / "data" / "L_chi5_zeros_600.csv", index=False)
    zd, a = run("DH", 0.5, TMAX + 0.5); audits += a
    pd.DataFrame(dict(sigma=[z.real for z in zd], t=[z.imag for z in zd])).sort_values("t").to_csv(
        ROOT / "data" / "dh_zeros_600.csv", index=False)
    pd.DataFrame(audits).to_csv(ROOT / "data" / "zeros_600_count_audit.csv", index=False)
    print(f"L_chi5 : {len(zl)} zéros ; DH : {len(zd)} zéros (t > 0) ; {time.time() - t0:.0f} s")
