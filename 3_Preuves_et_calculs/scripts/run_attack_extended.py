#!/usr/bin/env python3
"""v5.4 — Attaque étendue : la famille (mu, a) tient-elle quand N grandit ?  Gram des entiers sans carré <= NMAX=500 (reprenable).

 build   : python run_attack_extended.py build [budget_s]     (relancer jusqu'à « complète »)
 analyse : python run_attack_extended.py analyse
Familles (coefficients libres, projection orthogonale dans L^2(0,infini)), x = log n / log N :
 F1 {mu, a}            F2 {mu, mu x, mu x^2}            F3 {mu(1-x) x^j, j<=2} (poids nuls au bord n=N)
 F4 {mu(1-x)^2 x^j, j<=2}            P  prédiction hors échantillon : w = mu [1 - c (log^2 n - 2 gamma log n)/log^2 N] sans projection
"""
from pathlib import Path
import sys, math, time
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import nyman_beurling as nb
from rh_core import KAPPA, EULER_GAMMA as g, mobius_sieve
NMAX = 500; mu = mobius_sieve(NMAX)
sf = [n for n in range(1, NMAX + 1) if mu[n] != 0]; idx = {n: i for i, n in enumerate(sf)}
path = ROOT / "data" / "nb_gram_sqfree500.npy"
mode = sys.argv[1] if len(sys.argv) > 1 else "analyse"
if mode == "build":
    nb.Y_TARGET = 1e5   # écart relatif mesuré <= 2e-11 par rapport à 3e5, trois fois plus rapide
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 230.0
    M = np.load(path) if path.exists() else np.full((len(sf), len(sf)), np.nan)
    old = np.load(ROOT / "data" / "nb_gram_sqfree200.npy"); sf200 = [n for n in range(1, 201) if mu[n] != 0]
    for j, b in enumerate(sf200):
        for i, a in enumerate(sf200[: j + 1]):
            M[idx[a], idx[b]] = M[idx[b], idx[a]] = old[i, j]
    t0 = time.time()
    for j, b in enumerate(sf):
        for i, a in enumerate(sf[: j + 1]):
            if np.isnan(M[i, j]):
                if time.time() - t0 > budget:
                    np.save(path, M); print("temps écoulé ; entrées restantes :", int(np.isnan(np.triu(M)).sum())); sys.exit(0)
                M[i, j] = M[j, i] = nb.G(a, b)
    np.save(path, M); print("Gram sans carré 500 complète :", M.shape); sys.exit(0)
M = np.load(path); assert not np.isnan(M).any(), "Gram incomplète : relancer build"
def best(N, blist):
    ns = [n for n in sf if n <= N]; ii = [idx[n] for n in ns]; Gm = M[np.ix_(ii, ii)]
    nn = np.array(ns, float); m = np.array([mu[n] for n in ns], float); L = np.log(nn); x = L / math.log(N)
    V = np.vstack([f(nn, m, L, x, N) for f in blist]); b = np.array([nb.chi_rho(n) for n in ns])
    Gam = V @ Gm @ V.T; bb = V @ b; beta = -np.linalg.solve(Gam, bb)
    return float(1 + 2 * beta @ bb + beta @ Gam @ beta), beta
def fixed(N, wfun):
    ns = [n for n in sf if n < N]; ii = [idx[n] for n in ns]; Gm = M[np.ix_(ii, ii)]
    nn = np.array(ns, float); m = np.array([mu[n] for n in ns], float); L = np.log(nn)
    w = wfun(nn, m, L, N); b = np.array([nb.chi_rho(n) for n in ns]); return float(1 + 2 * w @ b + w @ Gm @ w)
mu_ = lambda n, m, L, x, N: m
a_ = lambda n, m, L, x, N: m * (L ** 2 - 2 * g * L)
fams = {"F1 {mu, a}": [mu_, a_],
        "F2 {mu, mu x, mu x^2}": [mu_, lambda n, m, L, x, N: m * x, lambda n, m, L, x, N: m * x ** 2],
        "F3 {mu(1-x) x^j, j<=2}": [lambda n, m, L, x, N: m * (1 - x) * x ** j for j in range(3)],
        "F4 {mu(1-x)^2 x^j, j<=2}": [lambda n, m, L, x, N: m * (1 - x) ** 2 * x ** j for j in range(3)]}
fams["F3 {mu(1-x) x^j, j<=2}"] = [(lambda j: (lambda n, m, L, x, N: m * (1 - x) * x ** j))(j) for j in range(3)]
fams["F4 {mu(1-x)^2 x^j, j<=2}"] = [(lambda j: (lambda n, m, L, x, N: m * (1 - x) ** 2 * x ** j))(j) for j in range(3)]
rows = []; Ns = (100, 150, 200, 300, 400, 500)
betas = {}
for name, bl in fams.items():
    r = {"famille": name}
    for N in Ns:
        e, bt = best(N, bl); r[f"e2_N{N}"] = e; r[f"ratio_N{N}"] = e * math.log(N) / KAPPA
        if name.startswith("F1"): betas[N] = float(bt[1])
    rows.append(r)
# prédiction hors échantillon : c ajusté sur N<=200 (moyenne de -beta log^2 N), testé sur 300..500
c_fit = float(np.mean([-betas[N] * math.log(N) ** 2 for N in (100, 150, 200)]))
r = {"famille": f"P prédiction c={c_fit:.3f} (sans projection)"}
for N in Ns:
    e = fixed(N, lambda n, m, L, N_: m * (1 - c_fit * (L ** 2 - 2 * g * L) / math.log(N_) ** 2)); r[f"e2_N{N}"] = e; r[f"ratio_N{N}"] = e * math.log(N) / KAPPA
rows.append(r)
df = pd.DataFrame(rows); df.to_csv(ROOT / "data" / "attack_extended.csv", index=False)
pd.DataFrame([dict(N=N, beta=betas[N], beta_log2N=betas[N] * math.log(N) ** 2) for N in Ns]).to_csv(ROOT / "data" / "attack_extended_beta.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 50)
print(df[["famille"] + [f"e2_N{N}" for N in Ns]].round(5).to_string(index=False)); print()
print(df[["famille"] + [f"ratio_N{N}" for N in Ns]].round(2).to_string(index=False)); print()
print(pd.DataFrame([dict(N=N, beta_log2N=betas[N] * math.log(N) ** 2) for N in Ns]).round(3).to_string(index=False))
