"""Core arithmetic utilities for the RH research package.

The module is deliberately self-contained and uses only numpy/math.
Nothing here should be interpreted as a proof of RH.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
import numpy as np

EULER_GAMMA = 0.5772156649015328606
KAPPA = 2.0 + EULER_GAMMA - math.log(4.0 * math.pi)


def mobius_sieve(N: int) -> np.ndarray:
    """Linear sieve for mu(0..N)."""
    mu = np.zeros(N + 1, dtype=np.int8)
    lp = np.zeros(N + 1, dtype=np.int64)
    primes: list[int] = []
    if N >= 1:
        mu[1] = 1
    for i in range(2, N + 1):
        if lp[i] == 0:
            lp[i] = i
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if p > lp[i] or i * p > N:
                break
            lp[i * p] = p
            if p == lp[i]:
                mu[i * p] = 0
            else:
                mu[i * p] = -mu[i]
    return mu


def von_mangoldt_sieve(N: int) -> np.ndarray:
    """Return Lambda(n), 0 <= n <= N."""
    isprime = np.ones(N + 1, dtype=bool)
    isprime[:2] = False
    for p in range(2, int(N**0.5) + 1):
        if isprime[p]:
            isprime[p * p :: p] = False
    lam = np.zeros(N + 1, dtype=float)
    for p in np.flatnonzero(isprime):
        lp = math.log(int(p))
        q = int(p)
        while q <= N:
            lam[q] = lp
            if q > N // p:
                break
            q *= int(p)
    return lam


def dirichlet_convolution(f: np.ndarray, g: np.ndarray, N: int | None = None) -> np.ndarray:
    """Dirichlet convolution up to N (O(N log N) on dense arrays)."""
    if N is None:
        N = min(len(f), len(g)) - 1
    out = np.zeros(N + 1, dtype=float)
    for d in range(1, N + 1):
        if f[d] == 0:
            continue
        maxm = N // d
        out[d * np.arange(1, maxm + 1)] += f[d] * g[1 : maxm + 1]
    return out


def arithmetic_a(N: int) -> np.ndarray:
    """a(n)=mu(n)((log n)^2-2 gamma log n)."""
    mu = mobius_sieve(N).astype(float)
    n = np.arange(N + 1, dtype=float)
    L = np.log(np.maximum(n, 1.0))
    a = mu * (L * L - 2.0 * EULER_GAMMA * L)
    a[0] = 0.0
    return a


def arithmetic_c_via_lambda(N: int) -> np.ndarray:
    """c(n)=(Lambda*Lambda)(n)-Lambda(n)log n+2 gamma Lambda(n)."""
    lam = von_mangoldt_sieve(N)
    conv = dirichlet_convolution(lam, lam, N)
    n = np.arange(N + 1, dtype=float)
    c = conv - lam * np.log(np.maximum(n, 1.0)) + 2.0 * EULER_GAMMA * lam
    c[0] = 0.0
    return c


def arithmetic_c_via_a(N: int) -> np.ndarray:
    """c=1*a; independent check of arithmetic_c_via_lambda."""
    a = arithmetic_a(N)
    ones = np.ones(N + 1, dtype=float)
    ones[0] = 0.0
    return dirichlet_convolution(ones, a, N)


def C_partial(c: np.ndarray) -> np.ndarray:
    return np.cumsum(c)


def Q_truncated(C: np.ndarray, X: int) -> float:
    """Exact integral int_1^X |C(x)|^2/x^2 dx for stepwise C(x)=sum_{n<=x}c(n)."""
    if X <= 1:
        return 0.0
    m = np.arange(1, X, dtype=float)
    return float(np.sum(C[1:X] ** 2 * (1.0 / m - 1.0 / (m + 1.0))))


def H_eta_truncated(C: np.ndarray, eta: float, X: int) -> float:
    """Truncated weighted energy int_1^X |C(x)|^2 x^(-2-2eta) dx."""
    m = np.arange(1, X, dtype=float)
    p = 1.0 + 2.0 * eta
    weights = (m ** (-p) - (m + 1.0) ** (-p)) / p
    return float(np.sum(C[1:X] ** 2 * weights))


def diagonal_proxy(c: np.ndarray, eta: float, X: int) -> float:
    """Positive diagonal proxy for the weighted quadratic form."""
    m = np.arange(1, X + 1, dtype=float)
    return float(np.sum(c[1:X+1] ** 2 * m ** (-1.0 - 2.0 * eta)) / (1.0 + 2.0 * eta))


def rho(u: np.ndarray) -> np.ndarray:
    return u - np.floor(u)


def fractional_representation_truncated(x: np.ndarray, a: np.ndarray, D: int) -> np.ndarray:
    """-sum_{d<=D} a(d) {x/d}; finite truncation only."""
    out = np.zeros_like(x, dtype=float)
    for d in range(1, D + 1):
        if a[d] != 0.0:
            out -= a[d] * rho(x / d)
    return out


def sawtooth_covariance_exact(d: int, e: int) -> float:
    """Mean covariance of centered sawteeth over a common period."""
    g = math.gcd(d, e)
    return (g * g) / (12.0 * d * e)


def jordan_J2_sieve(N: int) -> np.ndarray:
    """Jordan totient J_2(n)."""
    J = np.arange(N + 1, dtype=float) ** 2
    J[0] = 0.0
    if N >= 1:
        J[1] = 1.0
    isprime = np.ones(N + 1, dtype=bool)
    isprime[:2] = False
    for p in range(2, N + 1):
        if isprime[p]:
            J[p::p] *= (1.0 - 1.0 / (p * p))
            if p * p <= N:
                isprime[p * p :: p] = False
    return J


def gcd_gram_from_coeffs(coeff: np.ndarray, lo: int, hi: int) -> float:
    """Variance of sum_{lo<d<=hi} coeff[d]({x/d}-1/2) under period averaging."""
    s = 0.0
    for d in range(lo + 1, hi + 1):
        if coeff[d] == 0.0:
            continue
        for e in range(lo + 1, hi + 1):
            if coeff[e] == 0.0:
                continue
            s += coeff[d] * coeff[e] * sawtooth_covariance_exact(d, e)
    return s


def channel_vectors(a: np.ndarray, intervals: list[tuple[int, int]], qmax: int) -> np.ndarray:
    """H_I(q)=sum_{d in I, q|d} a(d)/d for divisor channels q."""
    H = np.zeros((len(intervals), qmax + 1), dtype=float)
    for j, (lo, hi) in enumerate(intervals):
        for q in range(1, qmax + 1):
            start = ((lo // q) + 1) * q
            if start > hi:
                continue
            ds = np.arange(start, hi + 1, q)
            H[j, q] = np.sum(a[ds] / ds)
    return H


def covariance_from_channels(H: np.ndarray) -> np.ndarray:
    qmax = H.shape[1] - 1
    J2 = jordan_J2_sieve(qmax)
    V = H[:, 1:] * np.sqrt(J2[1:])[None, :]
    return (V @ V.T) / 12.0


def kappa_reference_Q(X: float) -> float:
    return (4.0 * KAPPA / 3.0) * math.log(X) ** 3


@dataclass
class KalmanStep:
    rho: float
    gain: float
    var_before: float
    var_after: float


def scalar_projection_step(residual: np.ndarray, innovation: np.ndarray, weights: np.ndarray) -> tuple[np.ndarray, KalmanStep]:
    """One exact weighted L2 projection step (Kalman-like scalar innovation)."""
    vr = float(np.sum(weights * residual * residual))
    vu = float(np.sum(weights * innovation * innovation))
    cov = float(np.sum(weights * residual * innovation))
    if vu == 0.0 or vr == 0.0:
        return residual.copy(), KalmanStep(0.0, 0.0, vr, vr)
    gain = cov / vu
    rho = cov / math.sqrt(vr * vu)
    new = residual - gain * innovation
    vn = float(np.sum(weights * new * new))
    return new, KalmanStep(rho, gain, vr, vn)
