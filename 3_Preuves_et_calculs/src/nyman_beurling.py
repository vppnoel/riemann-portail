"""Matrice de Gram de Nyman-Beurling-Baez-Duarte (version L^2(0,infty), celle de BCF).

rho_k(x) = {1/(kx)}, chi = indicatrice de (0,1). Mellin : rho_k <-> -zeta(s) k^-s / s, chi <-> 1/s, donc
    (1/2pi) int |1 - zeta(s) A(s)|^2 dt/(1/4+t^2) = || chi + sum a_k rho_k ||^2_{L^2(0,infty)},  A=sum a_k k^-s.
Avec y=1/x :  G(a,b) = <rho_a,rho_b> = int_0^infty {y/a}{y/b} y^-2 dy = 1/(ab) + int_1^infty ...
              <chi,rho_a> = (log a + 1 - gamma)/a      (exact)
              ||chi||^2 = 1.
G(a,b) est calculée par cellules (entre multiples de a et b), exactement, jusqu'à Y=K*lcm, puis queue
M/Y + Fbar/Y^2 par extrapolation de Richardson (M = 1/4 + gcd^2/(12ab) = moyenne du produit).
"""
from __future__ import annotations
import math
from functools import lru_cache
import numpy as np

LD = np.longdouble
Y_TARGET = 3e5     # longueur cible Y=K*lcm de l'intégration exacte (v5.3 : modifiable avant le premier appel de G)
EULER_GAMMA = 0.5772156649015329


def _cell_integral(a: int, b: int, Y: int) -> LD:
    """int_1^Y {t/a}{t/b} t^-2 dt, a,b entiers premiers entre eux ou non, Y entier."""
    ka = np.arange(1, Y // a + 1, dtype=np.int64) * a
    kb = np.arange(1, Y // b + 1, dtype=np.int64) * b
    pts = np.unique(np.concatenate([[1, Y], ka, kb]))
    pts = pts[(pts >= 1) & (pts <= Y)].astype(LD)
    t0, t1 = pts[:-1], pts[1:]
    mid = 0.5 * (t0 + t1)
    i = np.floor(mid / a); j = np.floor(mid / b)
    d = t1 - t0
    val = d / (a * b) - (j / a + i / b) * np.log1p(d / t0) + i * j * d / (t0 * t1)
    return np.sum(val)


@lru_cache(maxsize=None)
def _G_coprime(a: int, b: int) -> float:
    ell = a * b
    K = max(1, int(max(Y_TARGET, 25 * ell) // ell))   # v5.3 : Y >= 25 ell pour garder la queue fiable quand ell est grand
    Y1, Y2 = K * ell, 2 * K * ell
    g1 = _cell_integral(a, b, Y1); g2 = _cell_integral(a, b, Y2)
    M = LD(0.25) + LD(1) / (12 * ell)            # gcd=1
    # g_inf = g1 + M/Y1 + F/Y1^2 = g2 + M/Y2 + F/Y2^2  => F
    F = (g2 - g1 - M * (LD(1) / Y1 - LD(1) / Y2)) / (LD(1) / Y1 ** 2 - LD(1) / Y2 ** 2)
    inf = g2 + M / Y2 + F / Y2 ** 2
    return float(inf + LD(1) / ell)             # + int_0^1 = 1/(ab)


def G(a: int, b: int) -> float:
    g = math.gcd(a, b)
    return _G_coprime(a // g, b // g) / g


def chi_rho(a: int) -> float:
    return (math.log(a) + 1 - EULER_GAMMA) / a


def gram(ks):
    n = len(ks)
    M = np.zeros((n, n))
    for p in range(n):
        for q in range(p, n):
            M[p, q] = M[q, p] = G(ks[p], ks[q])
    return M


def norm2_of_combination(coef: dict[int, float]) -> float:
    """|| chi + sum a_k rho_k ||^2 = (1/2pi) int |1 - zeta A|^2 dt/(1/4+t^2)."""
    ks = sorted(coef)
    a = np.array([coef[k] for k in ks])
    Gm = gram(ks)
    b = np.array([chi_rho(k) for k in ks])
    return float(1.0 + 2 * a @ b + a @ Gm @ a)


def d2_optimal(N: int, dps: int = 60):
    """d_N^2 = 1 - b^T G^-1 b (haute précision mpmath sur le système de Gram, entrées double)."""
    import mpmath as mp
    mp.mp.dps = dps
    ks = list(range(1, N + 1))
    Gm = mp.matrix(gram(ks).tolist()); b = mp.matrix([chi_rho(k) for k in ks])
    x = mp.lu_solve(Gm, b)
    return float(1 - sum(b[i] * x[i] for i in range(N)))
