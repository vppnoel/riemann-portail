#!/usr/bin/env python3
"""v5.5 — Test de l'estimation heuristique sous RH (type Selberg / Bettin–Conrey–Farmer) :
pour des poids w_n = mu(n) P(log n / log N), P(0)=1, P(1)=0,
    || chi + sum w_n r_n ||^2  ~  (kappa / log N) * int_0^1 P'(y)^2 dy     (RH, zéros simples).
On mesure R(P,N) = e^2 log N / (kappa int P'^2) avec la Gram exacte sur les entiers sans carré <= 998."""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import nyman_beurling as nb
from rh_core import KAPPA, EULER_GAMMA as g, mobius_sieve
M = np.load(ROOT / "data" / "nb_gram_sqfree1000.npy"); mu = mobius_sieve(1000); sf = [n for n in range(1, 1001) if mu[n] != 0]
fams = {
 "P1 = 1−x (BCF)": (lambda x: 1 - x, 1.0, -1.0),
 "P2 = (1−x)²": (lambda x: (1 - x) ** 2, 4 / 3, -2.0),
 "P3 = 1−x²": (lambda x: 1 - x ** 2, 4 / 3, 0.0),
 "P4 = 1−3x²+2x³": (lambda x: 1 - 3 * x ** 2 + 2 * x ** 3, 6 / 5, 0.0),
 "P5 = (1−x²)²": (lambda x: (1 - x ** 2) ** 2, 128 / 105, 0.0),
 "P6 = cos(πx/2)": (lambda x: np.cos(np.pi * x / 2), np.pi ** 2 / 8, 0.0),
 "P7 = 1−x³": (lambda x: 1 - x ** 3, 9 / 5, 0.0),
}
rows = []
for N in (100, 200, 400, 700, 998):
    ns = [n for n in sf if n <= N]; k = len(ns); Gm = M[:k, :k]
    nn = np.array(ns, float); m = np.array([mu[n] for n in ns], float); x = np.log(nn) / math.log(N)
    b = np.array([nb.chi_rho(n) for n in ns]); L = math.log(N)
    for name, (P, I, dP0) in fams.items():
        w = m * P(x); e2 = float(1 + 2 * w @ b + w @ Gm @ w)
        rows.append(dict(N=N, famille=name, P_prime_0=dP0, int_P2=I, e2=e2, R=e2 * L / (KAPPA * I), e2_logN_sur_kappa=e2 * L / KAPPA))
df = pd.DataFrame(rows); df.to_csv(ROOT / "data" / "rh_heuristic_test.csv", index=False)
piv = df.pivot(index="famille", columns="N", values="R").round(3)
print("R(P,N) = e² log N / (κ ∫P'²)   [prédiction RH : R → 1]"); print(piv.to_string())
print(); print("e² log N / κ :"); print(df.pivot(index="famille", columns="N", values="e2_logN_sur_kappa").round(3).to_string())
