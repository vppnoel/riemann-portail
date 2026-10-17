#!/usr/bin/env python3
"""Extension de d_N^2 optimal à N<=100 (calcul reprenable : data/nb_gram_G100.npy, relancer jusqu'à complétion)."""
from pathlib import Path
import sys, math, time
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from nyman_beurling import G, chi_rho
from rh_core import KAPPA

NMAX = 100
path = ROOT / "data" / "nb_gram_G100.npy"
M = np.load(path) if path.exists() else np.full((NMAX, NMAX), np.nan)
budget = float(sys.argv[1]) if len(sys.argv) > 1 else 240.0
t0 = time.time(); done = 0
# ordre : par taille croissante du bloc (q jusqu'à N), afin que les petits N soient complets d'abord
for q in range(NMAX):
    for p in range(q + 1):
        if np.isnan(M[p, q]):
            if time.time() - t0 > budget:
                np.save(path, M); print("temps écoulé ; entrées restantes :", int(np.isnan(np.triu(M)).sum())); sys.exit(0)
            M[p, q] = M[q, p] = G(p + 1, q + 1); done += 1
np.save(path, M)
print("Gram complète", NMAX, "x", NMAX, "calculées:", done)
import mpmath as mp
mp.mp.dps = 80
rows = []
for N in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
    Gm = mp.matrix(M[:N, :N].tolist()); b = mp.matrix([chi_rho(k) for k in range(1, N + 1)])
    x = mp.lu_solve(Gm, b); d2 = float(1 - sum(b[i] * x[i] for i in range(N)))
    ev = np.linalg.eigvalsh(M[:N, :N])
    rows.append(dict(N=N, logN=math.log(N), d2=d2, d2_logN=d2 * math.log(N), ratio_a_kappa=d2 * math.log(N) / KAPPA, cond=ev.max() / ev.min()))
df = pd.DataFrame(rows); df.to_csv(ROOT / "data" / "nb_gram_dN_ext.csv", index=False)
print(df.round(5).to_string(index=False))
