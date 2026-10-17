"""Prédiction CONDITIONNELLE (RH + zéros simples) de B(t)=e^{-t/2}C(e^t) et de Q.

Résidu de G(s)x^s/s en un zéro simple rho (double pôle de G, coeff. 2):
    x^rho/rho * [ 2(log x - 1/rho) + b ],   b = 2*c0 - 2*gamma_E,
    c0 = zeta''(rho) / (2 zeta'(rho))      (partie régulière de zeta'/zeta en rho).
Ceci est la formule explicite ; elle teste la COHÉRENCE des calculs avec la
théorie, pas RH elle-même (voir docs/PRIORITES.md, §P0).
"""
from __future__ import annotations
import csv, math
from pathlib import Path
import numpy as np
from rh_core import EULER_GAMMA, KAPPA

ROOT = Path(__file__).resolve().parents[1]


def load_zeros(n: int | None = None):
    """gamma_k>0 et c0_k ; lit data/zeros_300.csv, sinon recalcule avec mpmath."""
    p = ROOT / "data" / "zeros_300.csv"
    if p.exists():
        rows = list(csv.DictReader(p.open()))
        g = np.array([float(r["gamma"]) for r in rows])
        c0 = np.array([complex(float(r["c0_re"]), float(r["c0_im"])) for r in rows])
    else:
        import mpmath as mp
        mp.mp.dps = 20
        N = n or 300
        g, c0 = [], []
        for k in range(1, N + 1):
            rho = mp.zetazero(k)
            z1, z2 = mp.zeta(rho, derivative=1), mp.zeta(rho, derivative=2)
            g.append(float(rho.imag)); c0.append(complex(z2 / (2 * z1)))
        g, c0 = np.array(g), np.array(c0)
    if n:
        g, c0 = g[:n], c0[:n]
    return g, c0


def _coeffs(gam, c0):
    rho = 0.5 + 1j * gam
    A = 2.0 / rho                                   # coefficient de t
    u = (2 * c0 - 2 * EULER_GAMMA - 2.0 / rho) / rho   # terme constant
    return A, u


def B_explicit(t: np.ndarray, gam, c0) -> np.ndarray:
    A, u = _coeffs(gam, c0)
    out = np.zeros_like(t, dtype=float)
    for k in range(len(gam)):
        out += 2 * np.real(np.exp(1j * gam[k] * t) * (A[k] * t + u[k]))
    return out


def Q_diag_exact(L: float, gam, c0, tail_correct: bool = True) -> float:
    """Intégrale exacte de la partie diagonale 2*sum|A t + u|^2 sur [0,L].
    tail_correct : complète le coefficient en L^3 par l'identité (RH, zéros simples)
    sum_{gamma>0} 1/|rho|^2 = KAPPA/2 (zéros manquants, gamma > gamma_max)."""
    A, u = _coeffs(gam, c0)
    s3 = np.sum(np.abs(A) ** 2) / 3.0
    s2 = np.sum(np.real(A * np.conj(u)))
    s1 = np.sum(np.abs(u) ** 2)
    if tail_correct:
        missing = KAPPA / 2.0 - np.sum(1.0 / np.abs(0.5 + 1j * gam) ** 2)
        s3 += 4.0 * missing / 3.0
    return 2.0 * (s3 * L ** 3 + s2 * L ** 2 + s1 * L)


def Q_explicit_numeric(L: float, gam, c0, dt: float = 0.002) -> np.ndarray:
    t = np.arange(0, L, dt)
    B = B_explicit(t, gam, c0)
    return t, np.cumsum(B * B) * dt


def Q_measured_cumulative(N: int):
    """Q(X) exacte pour tout X<=N, via c = Lambda*Lambda - Lambda log + 2 gamma Lambda."""
    from rh_core import von_mangoldt_sieve
    lam = von_mangoldt_sieve(N)
    conv = np.zeros(N + 1)
    for d in np.flatnonzero(lam[: N // 2 + 1]):
        m = N // d
        conv[d : d * m + 1 : d] += lam[d] * lam[1 : m + 1]
    n = np.arange(N + 1, dtype=float)
    c = conv - lam * np.log(np.maximum(n, 1)) + 2 * EULER_GAMMA * lam
    c[0] = 0.0
    C = np.cumsum(c)
    m = np.arange(1, N, dtype=float)
    Qc = np.concatenate([[0.0], np.cumsum(C[1:N] ** 2 * (1 / m - 1 / (m + 1)))])
    return C, Qc   # Q(X) = Qc[X-1]
