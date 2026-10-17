"""Experimental Schrödinger / flux diagnostics for the RH programme (V4.2).

This module is deliberately modest.  It provides a dictionary between an explicit-
formula mode exp((beta-1/2)t) exp(i gamma t) and a complex Schrödinger energy,
plus finite-difference tools for 1-D Hamiltonians and continuity-equation checks.
It does NOT construct a Hilbert--Polya operator and does NOT prove RH.
"""
from __future__ import annotations

import math
import numpy as np


def energy_from_zero(beta: float, gamma: float, hbar: float = 1.0) -> complex:
    """Map rho=beta+i gamma to E for exp(-i E t/hbar).

    exp(-i E t/hbar) = exp((beta-1/2)t) exp(i gamma t)
    when E = -hbar*gamma + i*hbar*(beta-1/2).
    """
    return complex(-hbar * float(gamma), hbar * (float(beta) - 0.5))


def zero_parameters_from_energy(E: complex, hbar: float = 1.0) -> tuple[float, float]:
    """Inverse of energy_from_zero: returns (beta,gamma)."""
    E = complex(E)
    return 0.5 + E.imag / hbar, -E.real / hbar


def amplitude_growth_rate(beta: float) -> float:
    """Growth rate of modal amplitude in log-time."""
    return float(beta) - 0.5


def norm_growth_rate(beta: float) -> float:
    """Growth rate of |psi|^2 for a single explicit-formula mode."""
    return 2.0 * amplitude_growth_rate(beta)


def schrodinger_matrix_1d(
    x: np.ndarray,
    potential,
    mass: float = 1.0,
    hbar: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Dirichlet finite-difference Hamiltonian on the interior of a uniform grid.

    H = -(hbar^2/2m) d^2/dx^2 + V(x).
    `potential` may be a scalar, an array on the full grid, or a callable.
    Returns (H, x_interior).  Complex V is allowed for source/sink diagnostics.
    """
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or len(x) < 4:
        raise ValueError("x must be a one-dimensional grid with at least 4 points")
    dx = float(x[1] - x[0])
    if dx <= 0 or not np.allclose(np.diff(x), dx, rtol=1e-10, atol=1e-12):
        raise ValueError("x must be uniformly increasing")
    if mass <= 0 or hbar <= 0:
        raise ValueError("mass and hbar must be positive")
    xi = x[1:-1]
    n = len(xi)
    coeff = hbar * hbar / (2.0 * mass * dx * dx)
    H = np.diag(np.full(n, 2.0 * coeff, dtype=complex))
    if n > 1:
        off = np.full(n - 1, -coeff, dtype=complex)
        H += np.diag(off, 1) + np.diag(off, -1)
    if callable(potential):
        V = np.asarray(potential(xi), dtype=complex)
    elif np.isscalar(potential):
        V = np.full(n, complex(potential), dtype=complex)
    else:
        Vfull = np.asarray(potential, dtype=complex)
        if Vfull.shape == x.shape:
            V = Vfull[1:-1]
        elif Vfull.shape == xi.shape:
            V = Vfull
        else:
            raise ValueError("potential array must match x or x[1:-1]")
    H += np.diag(V)
    return H, xi


def self_adjointness_defect(H: np.ndarray) -> float:
    """Relative Frobenius defect ||H-H*||/max(||H||,tiny)."""
    H = np.asarray(H, dtype=complex)
    den = max(float(np.linalg.norm(H)), 1e-300)
    return float(np.linalg.norm(H - H.conj().T) / den)


def probability_current(
    psi: np.ndarray,
    x: np.ndarray,
    mass: float = 1.0,
    hbar: float = 1.0,
) -> np.ndarray:
    """1-D probability current j=(hbar/m) Im(conj(psi) dpsi/dx)."""
    psi = np.asarray(psi, dtype=complex)
    x = np.asarray(x, dtype=float)
    if psi.shape != x.shape:
        raise ValueError("psi and x must have identical shapes")
    dpsi = np.gradient(psi, x, edge_order=2)
    return (hbar / mass) * np.imag(np.conj(psi) * dpsi)


def continuity_source_density(
    psi: np.ndarray,
    potential,
    hbar: float = 1.0,
) -> np.ndarray:
    """Source term s=(2/hbar) Im(V)|psi|^2 for complex potential V."""
    psi = np.asarray(psi, dtype=complex)
    if np.isscalar(potential):
        Vim = float(np.imag(potential))
        return (2.0 * Vim / hbar) * np.abs(psi) ** 2
    V = np.asarray(potential, dtype=complex)
    if V.shape != psi.shape:
        raise ValueError("potential and psi must have identical shapes")
    return (2.0 / hbar) * np.imag(V) * np.abs(psi) ** 2


def stationary_eigenpairs(H: np.ndarray, k: int | None = None):
    """Eigenpairs sorted by real part, then imaginary part.

    For Hermitian H this agrees with ascending energy.  Dense linear algebra is used
    because this module is a diagnostic scaffold, not a large-scale eigensolver.
    """
    H = np.asarray(H, dtype=complex)
    if self_adjointness_defect(H) < 1e-12:
        vals, vecs = np.linalg.eigh((H + H.conj().T) / 2.0)
    else:
        vals, vecs = np.linalg.eig(H)
        order = np.lexsort((vals.imag, vals.real))
        vals, vecs = vals[order], vecs[:, order]
    if k is not None:
        vals, vecs = vals[: int(k)], vecs[:, : int(k)]
    return vals, vecs


def spectral_mismatch(eigenvalues, target_gammas, scale: float = 1.0) -> float:
    """Simple finite-spectrum diagnostic against target ordinates gamma.

    It intentionally compares only a finite list and therefore has no proof content.
    """
    ev = np.asarray(eigenvalues)
    tg = np.asarray(target_gammas, dtype=float)
    n = min(len(ev), len(tg))
    if n == 0:
        return math.nan
    pred = np.sort(np.abs(np.real(ev[:n]))) * float(scale)
    tar = np.sort(tg[:n])
    return float(np.sqrt(np.mean((pred - tar) ** 2)))
