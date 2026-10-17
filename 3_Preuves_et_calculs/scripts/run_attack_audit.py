#!/usr/bin/env python3
"""v5.3 — Audit des deux « attaques » reçues (énergie transverse / dissipation ; projection de Nyman–Beurling).

 A. identité E_perp = 1/2 ||u - R u||^2 = sum 1/|rho|^2 - kappa (algèbre, vérifiée sur zéros aléatoires et sur les 300 zéros)
 B. K(L) = (1/L) int_1^L |F(u)/u|^2 du pour zeta (limite attendue S = 4 kappa) et pour Davenport-Heilbronn (témoin négatif)
 C. décomposition exacte de la forme quadratique de Nyman–Beurling :
      G(a,b) = 1/(ab) + 1/4 + gcd(a,b)^2/(12 ab) + Delta(a,b)
    pour w = mu et w = mu + beta_proj * a ; part de chaque morceau dans ||chi + sum w r||^2 .
 D. lois d'échelle de Gamma_00, Gamma_01, Gamma_11 et de beta_N en puissance de log N.
"""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from rh_core import KAPPA, EULER_GAMMA as g, mobius_sieve
import nyman_beurling as nb
from explicit_formula import load_zeros, Q_measured_cumulative
out = {}
# ---------------- A
rng = np.random.default_rng(5)
rho = 0.3 + 0.5 * rng.random(2000) + 1j * (10 + 90 * rng.random(2000))
lhs = 0.5 * np.abs(1 / rho - 1 / (1 - np.conj(rho))) ** 2
rhs = 0.5 * (2 * rho.real - 1) ** 2 / (np.abs(rho) ** 2 * np.abs(1 - rho) ** 2)
out["A_identite_max_ecart"] = float(np.max(np.abs(lhs - rhs)))
gam, _ = load_zeros(); rz = 0.5 + 1j * gam
out["A_E_perp_300_zeros_sur_ligne"] = float(np.sum(0.5 * np.abs(1 / rz - 1 / (1 - np.conj(rz))) ** 2))
sum_inv = 2 * np.sum(1 / np.abs(rz) ** 2); sum_cross = 2 * np.sum((1 / (rz * (1 - rz))).real)
out["A_sum_1_over_rho2_300zeros"] = float(sum_inv); out["A_sum_1_over_rho_1minusrho_300zeros"] = float(sum_cross); out["A_kappa"] = KAPPA
# ---------------- B
def K_curve(Cfun, Lmax, du=0.002):
    u = np.arange(1.0, Lmax, du)
    F = np.exp(-u / 2) * Cfun(np.floor(np.exp(u)).astype(np.int64))
    integ = np.cumsum((F / u) ** 2) * du
    return u, integ / u
Nz = 4_000_000
Cz, _ = Q_measured_cumulative(Nz)
u, Kz = K_curve(lambda i: Cz[i], math.log(Nz) - 0.01)
S = 4 * KAPPA
rowsK = [dict(objet="zeta", L=L, K=float(Kz[int((L - 1) / 0.002)]), S=S) for L in (6, 9, 12, 15)]
from rejection import build
Nd = 300_000
_, _, cd = build("DH", Nd); Cd = np.cumsum(cd).real if np.iscomplexobj(cd) else np.cumsum(cd)
ud, Kd = K_curve(lambda i: Cd[i], math.log(Nd) - 0.01)
rowsK += [dict(objet="DH", L=L, K=float(Kd[int((L - 1) / 0.002)]), S=np.nan) for L in (6, 9, 11, 12)]
pd.DataFrame(rowsK).to_csv(ROOT / "data" / "attack_K_of_L.csv", index=False)
# ---------------- C, D
NMAX = 200; mu = mobius_sieve(NMAX)
sf = [n for n in range(1, NMAX + 1) if mu[n] != 0]; idx = {n: i for i, n in enumerate(sf)}
M = np.load(ROOT / "data" / "nb_gram_sqfree200.npy")
rowsC, rowsD = [], []
for N in (20, 50, 100, 150, 200):
    ns = [n for n in sf if n <= N]; ii = [idx[n] for n in ns]; Gm = M[np.ix_(ii, ii)]
    nn = np.array(ns, float)
    A1 = 1 / np.outer(nn, nn)
    gcd = np.array([[math.gcd(a, b) for b in ns] for a in ns], float)
    Gcd = gcd ** 2 / (12 * np.outer(nn, nn))
    Delta = Gm - A1 - 0.25 - Gcd
    b = (np.log(nn) + 1 - g) / nn
    mus = np.array([mu[n] for n in ns], float); a_ = mus * (np.log(nn) ** 2 - 2 * g * np.log(nn))
    V = np.vstack([mus, a_]); Gam = V @ Gm @ V.T; bb = V @ b
    beta = -(bb[1] + Gam[0, 1]) / Gam[1, 1]
    for name, w in (("mu", mus), ("mu+beta*a", mus + beta * a_)):
        parts = dict(N=N, vecteur=name, un=1.0, croise=2 * float(w @ b), rang1_1_sur_ab=float((w / nn).sum() ** 2),
                     rang1_quart=0.25 * float(w.sum() ** 2), canal_gcd=float(w @ Gcd @ w), delta=float(w @ Delta @ w))
        parts["total"] = parts["un"] + parts["croise"] + parts["rang1_1_sur_ab"] + parts["rang1_quart"] + parts["canal_gcd"] + parts["delta"]
        parts["somme_w"] = float(w.sum()); parts["somme_w_sur_n"] = float((w / nn).sum()); parts["norm_delta_fro"] = float(np.linalg.norm(Delta))
        rowsC.append(parts)
    rowsD.append(dict(N=N, logN=math.log(N), G00=float(Gam[0, 0]), G01=float(Gam[0, 1]), G11=float(Gam[1, 1]), beta_proj=float(beta),
                      beta_log2N=float(beta * math.log(N) ** 2), b0=float(bb[0]), b1=float(bb[1])))
dfC = pd.DataFrame(rowsC); dfC.to_csv(ROOT / "data" / "attack_decomposition.csv", index=False)
dfD = pd.DataFrame(rowsD); dfD.to_csv(ROOT / "data" / "attack_scaling.csv", index=False)
pd.Series(out).to_csv(ROOT / "data" / "attack_identities.csv", header=["valeur"])
pd.set_option("display.width", 220)
print(pd.Series(out).to_string()); print(); print(pd.DataFrame(rowsK).round(4).to_string(index=False)); print()
print(dfC.round(5).to_string(index=False)); print(); print(dfD.round(5).to_string(index=False))
