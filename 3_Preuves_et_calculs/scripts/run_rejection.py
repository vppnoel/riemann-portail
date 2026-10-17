#!/usr/bin/env python3
"""Banc de rejet : croissance de Q(X) et parcimonie de c pour zeta, L(s,chi5), DH."""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from rejection import build, Q_curve

N = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
rows = []
for kind in ["zeta", "L_chi5", "DH"]:
    a, lam, c = build(kind, N)
    C, Q = Q_curve(c)
    nz = np.count_nonzero(np.abs(c[1:]) > 1e-9) / N
    def q(X): return float(Q[X - 1])
    X1, X2 = N // 100, N - 1
    slope = math.log(q(X2) / q(X1)) / math.log(X2 / X1)
    rows.append(dict(objet=kind, N=N, Q_1e4=q(10_000), Q_1e5=q(100_000), Q_fin=q(X2),
                     pente_logQ_logX_derniere_decade=slope,
                     implique_Theta_eff=0.5 + slope / 2,
                     densite_support_c=nz, max_abs_c=float(np.max(np.abs(c[1:])))))
    print(rows[-1], flush=True)
df = pd.DataFrame(rows)
df.to_csv(ROOT / "data" / "rejection_growth.csv", index=False)
print(df.round(4).to_string(index=False))
