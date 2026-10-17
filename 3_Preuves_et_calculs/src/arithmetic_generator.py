"""Experimental state-space / quasi-Hermitian diagnostics for RH programme V4.3.

This module identifies a discrete propagator from snapshots, converts it into an
effective Schrödinger generator, and tests metric self-adjointness.  It has no
proof content by itself; it is a finite-dimensional diagnostic scaffold.
"""
from __future__ import annotations

import numpy as np
from scipy.linalg import logm


def fit_propagator(states: np.ndarray, ridge: float = 0.0) -> np.ndarray:
    """Least-squares A in z_{k+1} ~= A z_k.

    `states` has shape (dimension, n_snapshots).  A small ridge can regularize
    nearly dependent channels.
    """
    Z = np.asarray(states, dtype=complex)
    if Z.ndim != 2 or Z.shape[1] < 2:
        raise ValueError("states must have shape (dimension, >=2 snapshots)")
    X = Z[:, :-1]
    Y = Z[:, 1:]
    gram = X @ X.conj().T
    if ridge < 0:
        raise ValueError("ridge must be nonnegative")
    reg = float(ridge) * np.eye(gram.shape[0], dtype=complex)
    return Y @ X.conj().T @ np.linalg.pinv(gram + reg)


def effective_generator(A: np.ndarray, dt: float, hbar: float = 1.0) -> np.ndarray:
    """H=(i*hbar/dt) log(A), so A=exp(-i H dt/hbar) on the chosen branch."""
    if dt <= 0 or hbar <= 0:
        raise ValueError("dt and hbar must be positive")
    A = np.asarray(A, dtype=complex)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A must be square")
    return (1j * hbar / float(dt)) * logm(A)


def metric_self_adjointness_defect(H: np.ndarray, M: np.ndarray) -> float:
    """Relative defect ||H* M - M H||_F / max(||MH||_F,tiny)."""
    H = np.asarray(H, dtype=complex)
    M = np.asarray(M, dtype=complex)
    R = H.conj().T @ M - M @ H
    den = max(float(np.linalg.norm(M @ H)), 1e-300)
    return float(np.linalg.norm(R) / den)


def metric_unitarity_defect(A: np.ndarray, M: np.ndarray) -> float:
    """Relative defect ||A* M A-M||_F/||M||_F."""
    A = np.asarray(A, dtype=complex)
    M = np.asarray(M, dtype=complex)
    R = A.conj().T @ M @ A - M
    den = max(float(np.linalg.norm(M)), 1e-300)
    return float(np.linalg.norm(R) / den)


def spectral_metric(H: np.ndarray, imag_tol: float = 1e-9, cond_max: float = 1e12, metric_cond_max: float | None = None):
    """Construct M=(V^{-1})* V^{-1} when H is diagonalizable with real spectrum.

    Returns (M, eigenvalues, condition_number).  Returns (None, eig, cond) if the
    finite-dimensional quasi-Hermitian certificate fails the reality/conditioning
    checks.  This is a diagnostic, not an infinite-dimensional theorem.
    """
    H = np.asarray(H, dtype=complex)
    vals, V = np.linalg.eig(H)
    cond = float(np.linalg.cond(V))
    if np.max(np.abs(vals.imag)) > imag_tol or not np.isfinite(cond) or cond > cond_max:
        return None, vals, cond
    Vinv = np.linalg.inv(V)
    M = Vinv.conj().T @ Vinv
    M = (M + M.conj().T) / 2.0
    evM = np.linalg.eigvalsh(M)
    if np.min(evM) <= 0:
        return None, vals, cond
    # v4.4 : cond(M) ~ cond(V)^2 ; un bloc de Jordan numérique passe le test cond(V) mais donne une métrique dégénérée.
    if metric_cond_max is not None and np.max(evM) / np.min(evM) > metric_cond_max:
        return None, vals, cond
    return M, vals, cond


def modal_state_matrix(
    t: np.ndarray,
    modes,
    mixing: np.ndarray | None = None,
) -> np.ndarray:
    """Synthetic multichannel state from modes (beta,gamma,complex amplitude).

    Hidden modal coordinates are a_j exp(((beta_j-1/2)+i gamma_j)t).  A fixed
    invertible mixing matrix may be supplied to make the observed generator
    non-normal while preserving its spectrum.
    """
    t = np.asarray(t, dtype=float)
    coords = []
    for mode in modes:
        if len(mode) == 2:
            beta, gamma = mode
            amp = 1.0 + 0j
        else:
            beta, gamma, amp = mode
        lam = (float(beta) - 0.5) + 1j * float(gamma)
        coords.append(complex(amp) * np.exp(lam * t))
    Z = np.vstack(coords)
    if mixing is not None:
        mixing = np.asarray(mixing, dtype=complex)
        if mixing.shape != (Z.shape[0], Z.shape[0]):
            raise ValueError("mixing must be square with size equal to number of modes")
        Z = mixing @ Z
    return Z


def generator_diagnostics(states: np.ndarray, dt: float, ridge: float = 0.0) -> dict:
    """Fit A/H and report whether a finite positive spectral metric is found."""
    A = fit_propagator(states, ridge=ridge)
    H = effective_generator(A, dt)
    M, eig, cond = spectral_metric(H)
    out = {
        "A": A,
        "H": H,
        "eigenvalues": eig,
        "eigenvector_condition": cond,
        "metric": M,
        "metric_found": M is not None,
    }
    if M is not None:
        out["self_adjointness_defect"] = metric_self_adjointness_defect(H, M)
        out["unitarity_defect"] = metric_unitarity_defect(A, M)
        out["metric_condition"] = float(np.linalg.cond(M))
    else:
        out["self_adjointness_defect"] = np.nan
        out["unitarity_defect"] = np.nan
        out["metric_condition"] = np.inf
    return out
