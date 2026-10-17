#!/usr/bin/env python3
"""Niveau abélien du théorème : Q_eta = int_1^inf |C|^2 x^{-2-2eta} dx = lambda int U(L) e^{-lambda L} dL, lambda=2 eta.
Compare Q_eta mesurée (reste extrapolé) à la prédiction diagonale exacte des 300 zéros et à kappa/eta^3."""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from rh_core import KAPPA
from explicit_formula import load_zeros, _coeffs, Q_measured_cumulative

N = 4_000_000
C, Qc = Q_measured_cumulative(N)
gam, c0 = load_zeros()
A, u = _coeffs(gam, c0)
s3 = np.sum(np.abs(A) ** 2) / 3.0
miss = KAPPA / 2.0 - np.sum(1.0 / np.abs(0.5 + 1j * gam) ** 2)
s3c = s3 + 4.0 * miss / 3.0
s2 = np.sum(np.real(A * np.conj(u))); s1 = np.sum(np.abs(u) ** 2)

def Q_eta_measured(eta):
    m = np.arange(1, N, dtype=float)
    w = (m ** (-1 - 2 * eta) - (m + 1) ** (-1 - 2 * eta)) / (1 + 2 * eta)   # int_m^{m+1} x^{-2-2eta} dx
    body = float(np.sum(C[1:N] ** 2 * w))
    # reste au-delà de N : U(L)~ U(L0)*(L/L0)^3 (loi cubique), intégré exactement
    lam = 2 * eta; L0 = math.log(N); U0 = Qc[N - 2]
    tail = lam * U0 * L0 ** -3 * sum(math.comb(3, k) * L0 ** (3 - k) * math.factorial(k) / lam ** (k + 1) * 0 for k in range(1)) if False else None
    # intégrale analytique de lam * U0 (L/L0)^3 e^{-lam L} de L0 à l'infini
    from scipy.special import gammaincc, gamma
    tail = lam * U0 * L0 ** -3 * gamma(4) * gammaincc(4, lam * L0) / lam ** 4
    return body, tail

def Q_eta_diag(eta, corr=True):
    lam = 2 * eta
    S3 = s3c if corr else s3
    return 2 * (6 * S3 / lam ** 3 + 2 * s2 / lam ** 2 + s1 / lam)

rows = []
for eta in [0.2, 0.25, 0.3, 0.4, 0.5, 0.7]:
    body, tail = Q_eta_measured(eta)
    qm = body + tail; qd = Q_eta_diag(eta)
    rows.append(dict(eta=eta, Q_eta_mesuree=qm, reste_extrapole=tail, Q_eta_diag_300_zeros_corr=qd,
                     ratio=qm / qd, eta3_Q_eta=eta ** 3 * qm, kappa=KAPPA))
df = pd.DataFrame(rows); df.to_csv(ROOT / "data" / "abelian_check.csv", index=False)
print(df.round(4).to_string(index=False))
