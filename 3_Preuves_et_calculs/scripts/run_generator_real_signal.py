#!/usr/bin/env python3
"""Audit v4.4 de la branche V4.3 : identification de modes (ESPRIT/Prony, forme la plus favorable de A -> H_eff)
sur le VRAI signal arithmétique, pas sur des exponentielles injectées.

 zeta : y(t) = e^{-t/2}(psi(e^t) - e^t + log 2pi) = -sum_rho e^{(rho-1/2)t}/rho + (petits termes)   [X <= 4e6]
 DH   : y(t) = e^{-t/2} Psi_f(e^t),  Psi_f = sum_{n<=x} Lambda_f(n)                                   [X <= 3e5]
Sortie : data/generator_real_signal.csv (Im, Re = beta-1/2 estimés, zéro le plus proche).
"""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))

def esprit(y, dt, r):
    n = len(y); L = n // 2
    H = np.array([y[i:i + L] for i in range(n - L + 1)]).T
    U, s, Vh = np.linalg.svd(H, full_matrices=False)
    Us = U[:, :r]; A = np.linalg.pinv(Us[:-1]) @ Us[1:]
    return np.log(np.linalg.eigvals(A).astype(complex)) / dt

def modes(y, dt, r):
    lm = esprit(y, dt, r); pos = lm[lm.imag > 0]
    return pos[np.argsort(pos.imag)]

rows = []
# ---------- zeta
from rh_core import von_mangoldt_sieve
from explicit_formula import load_zeros
N = 4_000_000
psi = np.cumsum(von_mangoldt_sieve(N)); gam, _ = load_zeros()
dt = 0.02; t = np.arange(3.0, math.log(N) - 0.01, dt); x = np.exp(t); i = np.floor(x).astype(int)
y = np.exp(-t / 2) * (psi[i] - x + math.log(2 * math.pi))
for K in (7, 14):
    for z in modes(y, dt, 2 * K):
        j = np.argmin(abs(gam - z.imag))
        rows.append(dict(objet="zeta", ordre=2 * K, Im=z.imag, Re_beta_moins_demi=z.real, zero_proche=gam[j],
                         ecart_Im=z.imag - gam[j], beta_moins_demi_vrai=0.0))
# ---------- DH
from rejection import build
N2 = 300_000
a, lam, c = build("DH", N2); Psi = np.cumsum(lam.real)
zd = pd.read_csv(ROOT / "data" / "dh_zeros.csv").drop_duplicates().sort_values("t")
t2 = np.arange(3.0, math.log(N2) - 0.01, dt); x2 = np.exp(t2); i2 = np.floor(x2).astype(int)
y2 = np.exp(-t2 / 2) * Psi[i2]
for r in (20, 30):
    for z in modes(y2, dt, r):
        j = np.argmin(abs(zd.t.values - z.imag))
        rows.append(dict(objet="DH", ordre=r, Im=z.imag, Re_beta_moins_demi=z.real, zero_proche=zd.t.values[j],
                         ecart_Im=z.imag - zd.t.values[j], beta_moins_demi_vrai=zd.sigma.values[j] - 0.5))
df = pd.DataFrame(rows); df.to_csv(ROOT / "data" / "generator_real_signal.csv", index=False)
z14 = df[(df.objet == "zeta") & (df.ordre == 28)]
print("zeta, ordre 28 : biais de Re(lambda) sur les 12 premiers modes (vrai = 0) :")
print(z14.head(12)[["Im", "Re_beta_moins_demi", "ecart_Im"]].round(4).to_string(index=False))
d = df[(df.objet == "DH") & (df.ordre == 30)].sort_values("Re_beta_moins_demi", ascending=False).head(4)
print("\nDH, ordre 30 : 4 modes de plus grande partie réelle (zéro DH hors droite connu : 0.8085+85.699i, β-1/2=+0.3085) :")
print(d[["Im", "Re_beta_moins_demi", "zero_proche", "beta_moins_demi_vrai"]].round(4).to_string(index=False))
