#!/usr/bin/env python3
"""Activité 9 : (A) coefficient en eta^-2 de I(eta) pour le modèle local à 300 zéros ;
(B) l'amplitude des oscillations du coefficient de L^2 dans U(L) (formule explicite)."""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from rh_core import EULER_GAMMA as g
from explicit_formula import load_zeros, _coeffs, Q_explicit_numeric, Q_diag_exact

gam, c0 = load_zeros()
rho = 0.5 + 1j * gam
b = 2 * c0 - 2 * g
# ---------- (A) modèle local : G_N(s) = sum_{rho, rhobar} [2/(s-rho)^2 + b/(s-rho)]
allrho = np.concatenate([rho, np.conj(rho)]); allb = np.concatenate([b, np.conj(b)])
kappa_N = float(np.sum(1 / np.abs(allrho) ** 2))
s2_N = float(np.sum(allb.real / np.abs(allrho) ** 2 - 1 / np.abs(allrho) ** 4))
rows = []
for eta in [0.01, 0.015, 0.02, 0.03, 0.04]:
    sig = 0.5 + eta
    dt = eta / 8
    tmax = gam[-1] + 40
    t = np.arange(0, tmax, dt) + dt / 2
    acc = 0.0
    for ch in range(0, len(t), 200_000):
        tt = t[ch : ch + 200_000]; s = sig + 1j * tt
        G = np.zeros_like(s)
        for r, bb in zip(allrho, allb):
            d = s - r
            G += 2 / d ** 2 + bb / d
        acc += np.sum(np.abs(G) ** 2 / np.abs(s) ** 2) * dt
    I = 2 * acc / (2 * math.pi)          # t>0 et t<0 (symétrie)
    rows.append(dict(eta=eta, eta3_I=eta ** 3 * I, kappa_N=kappa_N, pred_ordre1=kappa_N + s2_N * eta,
                     reste_sur_eta2=(eta ** 3 * I - kappa_N - s2_N * eta) / eta ** 2))
dfA = pd.DataFrame(rows); dfA.to_csv(ROOT / "data" / "eta_expansion_model.csv", index=False)
print("(A) kappa_N =", kappa_N, " s2_N =", s2_N, "  [coefficient eta^-2 prédit]"); print(dfA.round(5).to_string(index=False))
# ---------- (B) oscillations du coefficient de L^2
Lmax = 15.2
t, Un = Q_explicit_numeric(Lmax, gam, c0, dt=0.002)
rowsB = []
for L in np.arange(6.0, 15.0, 0.25):
    i = int(L / 0.002)
    ud = Q_diag_exact(L, gam, c0, tail_correct=False)
    rowsB.append(dict(L=L, U_num=Un[i], U_diag=ud, ecart_sur_L2=(Un[i] - ud) / L ** 2))
dfB = pd.DataFrame(rowsB); dfB.to_csv(ROOT / "data" / "L2_oscillation.csv", index=False)
e = dfB.ecart_sur_L2.values
print("(B) (U_num - U_diag)/L^2 : min %.4f  max %.4f  moyenne %.4f ; |alpha| = %.4f" %
      (e.min(), e.max(), e.mean(), abs(2 * np.sum(np.real(_coeffs(gam, c0)[0] * np.conj(_coeffs(gam, c0)[1]))))))
