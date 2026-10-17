#!/usr/bin/env python3
"""Small v3 calibration run.

Produces data/spectral_calibration.csv and checks discrete Parseval.  This is deliberately
moderate-size: its purpose is reproducibility of the new Q(X,T) observable, not numerical
'evidence' for RH.
"""
from pathlib import Path
import sys, math
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rh_core import arithmetic_c_via_lambda, C_partial
from spectral_calibration import B_grid_from_C, parseval_energies, band_table

N = 200_000
DT = 0.01
c = arithmetic_c_via_lambda(N)
C = C_partial(c)
t, B = B_grid_from_C(C, math.log(N), dt=DT)
e_time, e_freq = parseval_energies(t, B, window="hann")

centers = [0.0, 5.0, 10.0, 20.0, 40.0, 80.0]
Delta = 2.0
rows = []
for T, D, E in band_table(t, B, centers, Delta, window="hann"):
    rows.append({
        "N": N,
        "dt": DT,
        "T": T,
        "Delta": D,
        "band_energy": E,
        "parseval_time": e_time,
        "parseval_freq": e_freq,
        "parseval_rel_error": abs(e_time - e_freq) / max(e_time, 1e-300),
    })

df = pd.DataFrame(rows)
out = ROOT / "data" / "spectral_calibration.csv"
df.to_csv(out, index=False)
print(df.to_string(index=False))
print(f"Wrote {out}")
