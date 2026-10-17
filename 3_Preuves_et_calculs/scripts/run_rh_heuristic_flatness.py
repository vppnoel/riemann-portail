#!/usr/bin/env python3
"""v5.5 — Suite du test heuristique : poids plats en 0 à l'ordre k, P(x) = 1 − x^k, et effet de l'amplitude libre."""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import nyman_beurling as nb
from rh_core import KAPPA, mobius_sieve
M = np.load(ROOT / "data" / "nb_gram_sqfree1000.npy"); mu = mobius_sieve(1000); sf = [n for n in range(1, 1001) if mu[n] != 0]
rows = []
for N in (100, 200, 400, 700, 998):
    ns = [n for n in sf if n <= N]; k_ = len(ns); Gm = M[:k_, :k_]
    nn = np.array(ns, float); m = np.array([mu[n] for n in ns], float); x = np.log(nn) / math.log(N); L = math.log(N)
    b = np.array([nb.chi_rho(n) for n in ns])
    for k in (1, 2, 3, 4, 5, 6, 8):
        w = m * (1 - x ** k); I = k * k / (2 * k - 1)
        e2 = float(1 + 2 * w @ b + w @ Gm @ w)
        e2_amp = float(1 - (w @ b) ** 2 / (w @ Gm @ w))          # amplitude libre (projection sur w)
        rows.append(dict(N=N, k=k, int_P2=I, e2_logN_k=e2 * L / KAPPA, R=e2 * L / (KAPPA * I), amp_libre_logN_k=e2_amp * L / KAPPA))
df = pd.DataFrame(rows); df.to_csv(ROOT / "data" / "rh_heuristic_flatness.csv", index=False)
print("e² log N / κ pour P = 1 − x^k (amplitude fixée à 1) :"); print(df.pivot(index="k", columns="N", values="e2_logN_k").round(3).to_string())
print("\nR = e² log N / (κ ∫P'²) :"); print(df.pivot(index="k", columns="N", values="R").round(3).to_string())
print("\namplitude libre, e² log N / κ :"); print(df.pivot(index="k", columns="N", values="amp_libre_logN_k").round(3).to_string())
