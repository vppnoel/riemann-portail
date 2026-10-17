"""Energy-dimension / generalized-fractal-string reformulation.

Definitions
-----------
For C(x)=sum_{n<=x} c(n), define

    Z_E(s) = int_1^infty |C(x)|^2 x^(-1-2s) dx.

For s=1/2+eta this is exactly the damped energy Q_eta used in Theorem B.
If U(L)=Q(e^L), then

    Z_E(s) = int_0^infty exp(-2(s-1/2)L) dU(L).

Hence the abscissa of convergence is Theta, by Theorem A.  Equivalently,
Z_E is the geometric zeta function of the positive generalized fractal string
obtained by pushing |C(x)|^2 dx/x forward under y=x^2.

The finite-zero functions below implement the exact meromorphic model.  They
are diagnostics, not a proof for the infinite zeta zero set.
"""
from __future__ import annotations

import math
import numpy as np


def effective_dimension_from_Q(X, Q):
    """Finite-scale estimator D_Q(X)=1/2+1/2 log(1+Q)/log X."""
    X = np.asarray(X, dtype=float)
    Q = np.asarray(Q, dtype=float)
    if np.any(X <= 1):
        raise ValueError("X must be > 1")
    if np.any(Q < 0):
        raise ValueError("Q must be nonnegative")
    return 0.5 + 0.5 * np.log1p(Q) / np.log(X)


def dimension_from_log_slope(alpha):
    """If Q(X) grows like X^alpha, the corresponding zero-abscissa is 1/2+alpha/2."""
    return 0.5 + 0.5 * np.asarray(alpha, dtype=float)


def energy_zeta_truncated(C: np.ndarray, s: complex, X: int) -> complex:
    """Exact integral int_1^X |C(x)|^2 x^(-1-2s) dx for stepwise C.

    C[m] is interpreted as sum_{n<=m}c(n), constant on [m,m+1).
    """
    s = complex(s)
    if X <= 1:
        return 0.0 + 0.0j
    if X > len(C):
        raise ValueError("X exceeds available C array")
    m = np.arange(1, X, dtype=float)
    if abs(s) < 1e-14:
        weights = np.log((m + 1.0) / m)
    else:
        weights = (m ** (-2.0 * s) - (m + 1.0) ** (-2.0 * s)) / (2.0 * s)
    return np.sum(np.abs(C[1:X]) ** 2 * weights)


def signed_rh_modes(gam: np.ndarray, A: np.ndarray, u: np.ndarray):
    """Return signed RH zeros and coefficients for B(t)=sum (A_j t+u_j)e^{(rho_j-1/2)t}."""
    gam = np.asarray(gam, dtype=float)
    A = np.asarray(A, dtype=complex)
    u = np.asarray(u, dtype=complex)
    rpos = 0.5 + 1j * gam
    rho = np.concatenate([rpos, np.conj(rpos)])
    Avec = np.concatenate([A, np.conj(A)])
    uvec = np.concatenate([u, np.conj(u)])
    return rho, Avec, uvec


def finite_energy_zeta(s: complex, rho: np.ndarray, A: np.ndarray, u: np.ndarray) -> complex:
    """Exact energy-zeta transform for a finite exponential-polynomial model.

    B(t)=sum_j (A_j t+u_j) exp((rho_j-1/2)t).
    Z(s)=int_0^infty B(t)^2 exp(-2(s-1/2)t) dt.

    The formula is valid when Re(2s-rho_j-rho_k)>0 for all j,k and then
    defines the meromorphic continuation elsewhere.
    """
    rho = np.asarray(rho, dtype=complex)
    A = np.asarray(A, dtype=complex)
    u = np.asarray(u, dtype=complex)
    if not (len(rho) == len(A) == len(u)):
        raise ValueError("rho, A, u must have the same length")
    s = complex(s)
    out = 0.0 + 0.0j
    for j in range(len(rho)):
        for k in range(len(rho)):
            d = 2.0 * s - rho[j] - rho[k]
            out += 2.0 * A[j] * A[k] / d**3
            out += (A[j] * u[k] + u[j] * A[k]) / d**2
            out += u[j] * u[k] / d
    return out


def finite_complex_dimensions(rho: np.ndarray) -> np.ndarray:
    """Candidate pole locations (rho_j+rho_k)/2 of the finite energy model."""
    rho = np.asarray(rho, dtype=complex)
    return ((rho[:, None] + rho[None, :]) / 2.0).reshape(-1)


def principal_real_dimension(rho: np.ndarray) -> float:
    """Rightmost real part among finite-model pair-average poles."""
    poles = finite_complex_dimensions(rho)
    return float(np.max(poles.real))


def finite_model_B(t: np.ndarray, rho: np.ndarray, A: np.ndarray, u: np.ndarray) -> np.ndarray:
    """Evaluate B(t) for a generic finite model."""
    t = np.asarray(t, dtype=float)
    rho = np.asarray(rho, dtype=complex)
    A = np.asarray(A, dtype=complex)
    u = np.asarray(u, dtype=complex)
    out = np.zeros_like(t, dtype=complex)
    for r, a, b in zip(rho, A, u):
        out += (a * t + b) * np.exp((r - 0.5) * t)
    return out
