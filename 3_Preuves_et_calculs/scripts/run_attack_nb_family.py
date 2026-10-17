#!/usr/bin/env python3
"""v5.3 — Audit de l'« attaque 2 » : familles d'approximants de Möbius pondérés par des puissances de log n,
projetées orthogonalement dans le cadre de Nyman–Beurling (norme de L^2(0,infini)).

 R_j = sum_{n<=N, n sans carré} mu(n) (log n)^j r_n ,   r_n(x) = {1/(nx)}
 e^2 = || chi + sum_j beta_j R_j ||^2 = 1 + 2 beta.b + beta' Gamma beta,  b_j = <chi,R_j>, Gamma_jk = <R_j,R_k>

Étape 1 (reprenable) : construit la Gram des entiers sans carré <= NMAX (réutilise data/nb_gram_G100.npy).
Étape 2 : calcule, pour N donné,
   (i) mu seul ; (ii) (alpha, beta) libres sur {mu, mu*a} ; (iii) alpha=1, beta projeté (éq. 4-5 du document reçu) ;
   (iv) degré k=1..4 en log n (projection complète) ; (v) optimum d_N^2 sur tous n<=N si N<=100.
"""
from pathlib import Path
import sys, math, time, json
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import nyman_beurling as nb
from rh_core import KAPPA, EULER_GAMMA, mobius_sieve

NMAX = 200
sf = [n for n in range(1, NMAX + 1) if mobius_sieve(NMAX)[n] != 0]
idx = {n: i for i, n in enumerate(sf)}
path = ROOT / "data" / "nb_gram_sqfree200.npy"
M = np.load(path) if path.exists() else np.full((len(sf), len(sf)), np.nan)
G100 = np.load(ROOT / "data" / "nb_gram_G100.npy")
budget = float(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1] != "analyse" else 230.0
mode = "analyse" if "analyse" in sys.argv else "build"
if mode == "build":
    t0 = time.time(); todo = 0
    for j, b in enumerate(sf):
        for i, a in enumerate(sf[: j + 1]):
            if np.isnan(M[i, j]):
                if b <= 100:
                    M[i, j] = M[j, i] = G100[a - 1, b - 1]
                else:
                    if time.time() - t0 > budget:
                        np.save(path, M); rest = int(np.isnan(np.triu(M)).sum())
                        print("temps écoulé ; entrées restantes :", rest); sys.exit(0)
                    M[i, j] = M[j, i] = nb.G(a, b)
    np.save(path, M); print("Gram sans carré complète :", M.shape); mode = "analyse"
# ---------------- analyse
mu = mobius_sieve(NMAX)
chi_rho = {n: nb.chi_rho(n) for n in sf}
gam = EULER_GAMMA
def family(N, powers, alpha_fixed=False):
    ns = [n for n in sf if n <= N]; ii = [idx[n] for n in ns]
    Gm = M[np.ix_(ii, ii)]
    W = np.array([[mu[n] * math.log(n) ** p for n in ns] for p in powers], dtype=float)   # (P, n)
    b = np.array([chi_rho[n] for n in ns])
    Gam = W @ Gm @ W.T; bb = W @ b
    return Gam, bb
def e2(beta, Gam, bb): return float(1 + 2 * beta @ bb + beta @ Gam @ beta)
rows = []
for N in (20, 50, 100, 150, 200):
    L = math.log(N)
    r = dict(N=N, logN=L)
    Gam, bb = family(N, [0]); r["mu_seul"] = e2(np.array([1.0]), Gam, bb)
    # (ii) deux directions mu et a = mu(log^2 - 2 gamma log): libres
    ns = [n for n in sf if n <= N]; ii = [idx[n] for n in ns]; Gm = M[np.ix_(ii, ii)]
    Rmu = np.array([mu[n] for n in ns], float); Ra = np.array([mu[n] * (math.log(n) ** 2 - 2 * gam * math.log(n)) for n in ns])
    V = np.vstack([Rmu, Ra]); Gam2 = V @ Gm @ V.T; bb2 = V @ np.array([chi_rho[n] for n in ns])
    beta = -np.linalg.solve(Gam2, bb2); r["mu_a_libres"] = e2(beta, Gam2, bb2); r["alpha_libre"] = float(beta[0]); r["beta_libre"] = float(beta[1])
    # (iii) alpha = 1, beta projeté
    be = -(bb2[1] + Gam2[0, 1]) / Gam2[1, 1]; r["alpha1_beta"] = e2(np.array([1.0, be]), Gam2, bb2); r["beta_proj"] = float(be)
    for k in (1, 2, 3, 4):
        Gk, bk = family(N, list(range(k + 1))); r[f"deg{k}"] = e2(-np.linalg.solve(Gk, bk), Gk, bk)
    r["opt_N"] = float(pd.read_csv(ROOT / "data" / "nb_gram_dN_ext.csv").set_index("N").d2.get(N, np.nan)) if N in (20, 50, 100) else np.nan
    rows.append(r)
df = pd.DataFrame(rows)
for c in ("mu_seul", "mu_a_libres", "alpha1_beta", "deg1", "deg2", "deg3", "deg4"): df[c + "_logN_sur_kappa"] = df[c] * df.logN / KAPPA
df.to_csv(ROOT / "data" / "attack_nb_family.csv", index=False)
pd.set_option("display.width", 220)
print(df[["N", "mu_seul", "mu_a_libres", "alpha_libre", "beta_libre", "alpha1_beta", "beta_proj", "deg1", "deg2", "deg3", "deg4", "opt_N"]].round(5).to_string(index=False))
print(df[["N"] + [c for c in df.columns if c.endswith("_sur_kappa")]].round(3).to_string(index=False))
