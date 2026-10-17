#!/usr/bin/env python3
"""v5.4 — Attaque 2 poursuivie : familles de projection jusqu'au plus grand N disponible (Gram sans carré),
optimum sur tout le support sans carré, et forme du poids optimal c_n / mu(n) en fonction de x = log n / log N."""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
import scipy.linalg as sla
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import nyman_beurling as nb
from rh_core import KAPPA, EULER_GAMMA as g, mobius_sieve
M = np.load(ROOT / "data" / "nb_gram_sqfree500.npy"); mu = mobius_sieve(500)
sf = [n for n in range(1, 501) if mu[n] != 0]
J = 0
while J < len(sf) and not np.isnan(M[:J + 1, :J + 1]).any(): J += 1
NMAX_OK = sf[J - 1]
Ns = [N for N in (50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000) if N <= NMAX_OK]
def setup(N):
    ns = [n for n in sf if n <= N]; k = len(ns); Gm = M[:k, :k]
    nn = np.array(ns, float); m = np.array([mu[n] for n in ns], float); L = np.log(nn)
    b = np.array([nb.chi_rho(n) for n in ns]); return ns, nn, m, L, Gm, b
def proj(V, Gm, b):
    Gam = V @ Gm @ V.T; bb = V @ b; beta = -np.linalg.solve(Gam, bb); return float(1 + 2 * beta @ bb + beta @ Gam @ beta), beta
rows, prof = [], []
for N in Ns:
    ns, nn, m, L, Gm, b = setup(N); lN = math.log(N)
    r = dict(N=N, logN=lN, n_sansCarre=len(ns))
    r["mu_fixe"] = float(1 + 2 * m @ b + m @ Gm @ m)
    a = m * (L ** 2 - 2 * g * L)
    r["mu_a"], be = proj(np.vstack([m, a]), Gm, b); r["alpha"] = float(be[0]); r["beta"] = float(be[1]); r["beta_log2N"] = float(be[1] * lN ** 2)
    r["mu_log"], _ = proj(np.vstack([m, m * L]), Gm, b)
    r["mu_log2"], _ = proj(np.vstack([m, m * L ** 2]), Gm, b)
    r["deg3"], _ = proj(np.vstack([m * L ** k for k in range(4)]), Gm, b)
    r["deg5"], _ = proj(np.vstack([m * (L / lN) ** k for k in range(6)]), Gm, b)
    # optimum sur tout le support sans carré
    cnd = np.linalg.cond(Gm); r["cond_G"] = float(cnd)
    c = -sla.solve(Gm, b, assume_a="pos"); r["opt_sansCarre"] = float(1 + b @ c)
    r["somme_c"] = float(c.sum()); r["somme_c_sur_n"] = float((c / nn).sum())
    r["accord_signe_mu"] = float(np.mean(np.sign(c) == m))
    # profil P(x) = c_n mu(n), x = log n / log N : ajustement polynomial de degré 3, R^2
    x = L / lN; y = c * m
    X = np.vstack([x ** k for k in range(4)]).T; coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ coef; r["R2_profil_deg3"] = float(1 - np.sum((y - yhat) ** 2) / np.sum((y - y.mean()) ** 2))
    r["profil_coef"] = " ".join(f"{v:+.3f}" for v in coef)
    rows.append(r)
    if N in (200, NMAX_OK if NMAX_OK in Ns else Ns[-1]):
        for n_, xx, yy in zip(ns, x, y): prof.append(dict(N=N, n=n_, x=xx, c_mu=yy))
df = pd.DataFrame(rows)
for col in ("mu_fixe", "mu_a", "mu_log", "mu_log2", "deg3", "deg5", "opt_sansCarre"): df[col + "_rk"] = df[col] * df.logN / KAPPA
df.to_csv(ROOT / "data" / "attack_v54_families.csv", index=False); pd.DataFrame(prof).to_csv(ROOT / "data" / "attack_v54_profile.csv", index=False)
pd.set_option("display.width", 250)
print("Gram complète jusqu'à n =", NMAX_OK)
print(df[["N", "n_sansCarre", "mu_fixe", "mu_a", "mu_log", "mu_log2", "deg3", "deg5", "opt_sansCarre", "cond_G"]].to_string(index=False, float_format=lambda v: f"{v:.5g}"))
print(df[["N"] + [c for c in df.columns if c.endswith("_rk")]].round(3).to_string(index=False))
print(df[["N", "alpha", "beta", "beta_log2N", "somme_c", "somme_c_sur_n", "accord_signe_mu", "R2_profil_deg3", "profil_coef"]].to_string(index=False, float_format=lambda v: f"{v:.4g}"))
