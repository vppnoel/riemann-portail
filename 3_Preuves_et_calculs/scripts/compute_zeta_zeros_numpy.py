#!/usr/bin/env python3
"""V6.3f — Zéros de zeta jusqu'à t = 1500, sans mpmath (même méthode que compute_zeros_numpy.py).

Complétude contrôlée par le principe de l'argument, bande par bande.
Sorties : data/zeta_zeros_1500.csv, data/zeta_zeros_1500_count_audit.csv.
"""
from pathlib import Path
import sys, time
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
from compute_zeros_numpy import run

if __name__ == "__main__":
    t0 = time.time()
    z, audit = run("zeta", 0.5, 1500.5)
    pd.DataFrame(dict(sigma=[w.real for w in z], t=[w.imag for w in z])).sort_values("t").to_csv(ROOT / "data" / "zeta_zeros_1500.csv", index=False)
    pd.DataFrame(audit).to_csv(ROOT / "data" / "zeta_zeros_1500_count_audit.csv", index=False)
    print(f"zeta : {len(z)} zéros ; {time.time() - t0:.0f} s")
