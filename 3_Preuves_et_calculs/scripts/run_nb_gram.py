#!/usr/bin/env python3
"""Reproduction numérique de d_N^2 log N vs kappa (Bettin-Conrey-Farmer / Burnol) par la matrice de Gram NB."""
from pathlib import Path
import sys, math, time
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from nyman_beurling import norm2_of_combination, d2_optimal
from rh_core import KAPPA, mobius_sieve

rows = []
mu = mobius_sieve(400)
t0 = time.time()
for N in [5, 10, 20, 30, 50, 80, 120, 200]:
    lN = math.log(N)
    coef = {k: float(mu[k]) * (1 - math.log(k) / lN) for k in range(1, N + 1) if mu[k] != 0 and k < N}
    EV = norm2_of_combination(coef)
    d2 = d2_optimal(N) if N <= 30 else float("nan")
    rows.append(dict(N=N, logN=lN, E_VN=EV, E_VN_logN=EV * lN, d2_opt=d2, d2_opt_logN=d2 * lN if d2 == d2 else float("nan"),
                     kappa_sur_logN=KAPPA / lN, kappa=KAPPA))
    print(rows[-1], round(time.time() - t0, 1), "s", flush=True)
df = pd.DataFrame(rows); df.to_csv(ROOT / "data" / "nb_gram_dN.csv", index=False)
print(df.round(5).to_string(index=False))
