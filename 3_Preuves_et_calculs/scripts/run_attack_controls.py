#!/usr/bin/env python3
"""v5.3 — Témoins pour l'attaque 2 : la direction a(n)=mu(n)(log^2 n - 2 gamma log n) est-elle privilégiée ?
Toutes les familles sont projetées orthogonalement (coefficients libres) dans L^2(0,infini) via la Gram sans carré <= 200."""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import nyman_beurling as nb
from rh_core import KAPPA, EULER_GAMMA as g, mobius_sieve
NMAX = 200; mu = mobius_sieve(NMAX)
sf = [n for n in range(1, NMAX + 1) if mu[n] != 0]; idx = {n: i for i, n in enumerate(sf)}
M = np.load(ROOT / "data" / "nb_gram_sqfree200.npy")
def best(N, builders):
    ns = [n for n in sf if n <= N]; ii = [idx[n] for n in ns]; Gm = M[np.ix_(ii, ii)]
    nn = np.array(ns, float); m = np.array([mu[n] for n in ns], float); L = np.log(nn)
    V = np.vstack([f(nn, m, L, N) for f in builders]); b = np.array([nb.chi_rho(n) for n in ns])
    Gam = V @ Gm @ V.T; bb = V @ b
    beta = -np.linalg.solve(Gam, bb); return float(1 + 2 * beta @ bb + beta @ Gam @ beta)
mu_f = lambda n, m, L, N: m
fam = {
 "C0 mu seul (coefficient libre)": [mu_f],
 "C1 {mu, mu log n}": [mu_f, lambda n, m, L, N: m * L],
 "C2 {mu, mu log^2 n}": [mu_f, lambda n, m, L, N: m * L ** 2],
 "C3 {mu, a}  (a = mu(log^2 - 2 gamma log))": [mu_f, lambda n, m, L, N: m * (L ** 2 - 2 * g * L)],
 "C4 {mu, mu log^3 n}": [mu_f, lambda n, m, L, N: m * L ** 3],
 "C5 {mu, mu 1_{n>N/2}} (fenêtre de queue)": [mu_f, lambda n, m, L, N: m * (n > N / 2)],
 "C6 {mu, mu 1_{n>N/2} log n}": [mu_f, lambda n, m, L, N: m * (n > N / 2) * L],
 "S1 lissé {mu(1-n/N)^2}": [lambda n, m, L, N: m * (1 - n / N) ** 2],
 "S2 lissé {mu w, a w}, w=(1-n/N)^2": [lambda n, m, L, N: m * (1 - n / N) ** 2, lambda n, m, L, N: m * (L ** 2 - 2 * g * L) * (1 - n / N) ** 2],
 "S3 lissé {mu w, mu w log, mu w log^2}": [lambda n, m, L, N: m * (1 - n / N) ** 2, lambda n, m, L, N: m * L * (1 - n / N) ** 2, lambda n, m, L, N: m * L ** 2 * (1 - n / N) ** 2],
 "S4 lissé {mu w, mu w log} w=(1-n/N)^2": [lambda n, m, L, N: m * (1 - n / N) ** 2, lambda n, m, L, N: m * L * (1 - n / N) ** 2],
 "R1 {mu, mu log log n}": [mu_f, lambda n, m, L, N: m * np.log(np.maximum(L, 1e-9) + 1)],
 "R2 {mu, mu n^{-1/2}}": [mu_f, lambda n, m, L, N: m / np.sqrt(n)],
}
rows = []
for name, bl in fam.items():
    r = {"famille": name}
    for N in (50, 100, 150, 200): r[f"e2_N{N}"] = best(N, bl); r[f"ratio_kappa_N{N}"] = r[f"e2_N{N}"] * math.log(N) / KAPPA
    rows.append(r)
# référence BCF : coefficients (1 - log n/log N) sur n<N
def ebcf(N):
    ns = [n for n in sf if n < N]; ii = [idx[n] for n in ns]; Gm = M[np.ix_(ii, ii)]
    w = np.array([mu[n] * (1 - math.log(n) / math.log(N)) for n in ns]); b = np.array([nb.chi_rho(n) for n in ns])
    return float(1 + 2 * w @ b + w @ Gm @ w)
r = {"famille": "REF BCF V_N (poids 1 - log n/log N, sans projection)"}
for N in (50, 100, 150, 200): r[f"e2_N{N}"] = ebcf(N); r[f"ratio_kappa_N{N}"] = r[f"e2_N{N}"] * math.log(N) / KAPPA
rows.append(r)
df = pd.DataFrame(rows); df.to_csv(ROOT / "data" / "attack_controls.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 60)
print(df[["famille"] + [f"e2_N{N}" for N in (50, 100, 150, 200)]].round(5).to_string(index=False)); print()
print(df[["famille"] + [f"ratio_kappa_N{N}" for N in (50, 100, 150, 200)]].round(2).to_string(index=False))
