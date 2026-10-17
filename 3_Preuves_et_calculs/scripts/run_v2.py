#!/usr/bin/env python3
"""Compare Q(X) mesurée (jusqu'à 4e6) à la formule explicite (RH conditionnelle)."""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from rh_core import KAPPA
from explicit_formula import load_zeros, Q_diag_exact, Q_explicit_numeric, Q_measured_cumulative

N = 4_000_000
C, Qc = Q_measured_cumulative(N)
gam, c0 = load_zeros()
t, Qnum = Q_explicit_numeric(math.log(N), gam, c0)
rows = []
for X in [300, 1000, 3000, 10000, 30000, 100000, 300000, 1000000, N - 1]:
    L = math.log(X)
    qm = Qc[X - 1]
    qn = Qnum[min(int(L / 0.002), len(t) - 1)]
    qd = Q_diag_exact(L, gam, c0, tail_correct=True)
    qd_raw = Q_diag_exact(L, gam, c0, tail_correct=False)
    rows.append(dict(X=X, Q_mesuree=qm, Q_formule_explicite_numerique=qn,
                     Q_diag_exacte_300_zeros=qd_raw, Q_diag_exacte_corr_queue=qd,
                     ref_ancienne_4k3_L3=4 * KAPPA / 3 * L ** 3,
                     ratio_mesure_sur_diag_corr=qm / qd,
                     ratio_mesure_sur_ancienne_ref=qm / (4 * KAPPA / 3 * L ** 3)))
df = pd.DataFrame(rows)
df.to_csv(ROOT / "data" / "explicit_vs_measured.csv", index=False)
print(df.round(3).to_string(index=False))
