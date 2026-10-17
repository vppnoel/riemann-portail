#!/usr/bin/env python3
"""V6.15 — Zéros de Davenport–Heilbronn au-delà de |t| = 600, par la méthode de la V6.3d (compute_zeros_numpy.py) :
minima de |F| sur des droites verticales, Newton, partenaires 1 - conj(rho), complétude par le principe de l'argument
bande par bande. Sert à attribuer les directions négatives de la métrique des premiers (document 39) : avec h = 0,004,
les fréquences au-delà de π/h ≈ 785 se replient dans la fenêtre, et les lobes secondaires de ĝ leur gardent un poids.
Usage : python scripts/compute_dh_zeros_high.py T_MIN T_MAX  (par défaut 600 1100)
Sorties : data/dh_zeros_<T_MIN>_<T_MAX>.csv, data/dh_zeros_<T_MIN>_<T_MAX>_audit.csv.
"""
from pathlib import Path
import sys, time
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "src"))
from compute_zeros_numpy import run

if __name__ == "__main__":
    lo, hi = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (600, 1100)
    t0 = time.time(); zd, audit = run("DH", lo + 0.5, hi + 0.5)
    pd.DataFrame(dict(sigma=[z.real for z in zd], t=[z.imag for z in zd])).sort_values("t").to_csv(ROOT / "data" / f"dh_zeros_{lo}_{hi}.csv", index=False)
    pd.DataFrame(audit).to_csv(ROOT / "data" / f"dh_zeros_{lo}_{hi}_audit.csv", index=False)
    print(f"DH : {len(zd)} zéros pour {lo},5 < t <= {hi},5 ; hors droite : {sum(abs(z.real - 0.5) > 1e-7 for z in zd)} ; {time.time() - t0:.0f} s")
