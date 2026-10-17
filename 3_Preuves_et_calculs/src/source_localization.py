"""Signal-processing / inverse-source diagnostics for the RH programme.

This module treats explicit-formula observables as deterministic inverse problems.
It is experimental. It does NOT prove RH and deliberately keeps the distinction
between finite-resolution source localization and a uniform observability theorem.

Core model (schematic):
    y(t) = sum_rho A_rho exp((beta_rho-1/2)t) exp(i gamma_rho t) + deterministic terms.
Under RH every source has beta=1/2.  A source with beta>1/2 is an exponentially
increasing mode.  The difficult analytic question is not finite-height detection,
but a uniform lower visibility bound for all off-line sources.
"""
from __future__ import annotations

import math
import numpy as np


def gaussian_kernel_samples(dt: float, sigma_t: float, nsigma: float = 5.0) -> np.ndarray:
    """Normalized discrete Gaussian averaging kernel."""
    if dt <= 0 or sigma_t <= 0:
        raise ValueError("dt and sigma_t must be positive")
    half = max(1, int(math.ceil(nsigma * sigma_t / dt)))
    x = np.arange(-half, half + 1, dtype=float) * dt
    k = np.exp(-0.5 * (x / sigma_t) ** 2)
    k /= np.sum(k)
    return k


def gaussian_average(y: np.ndarray, dt: float, sigma_t: float) -> np.ndarray:
    """Ensemble-like pre-averaging: Gaussian convolution with same-length output."""
    y = np.asarray(y)
    k = gaussian_kernel_samples(dt, sigma_t)
    return np.convolve(y, k, mode="same")


def regularized_laplacian(y: np.ndarray, dt: float, lam: float = 1e-2) -> np.ndarray:
    """Regularized log-time Laplacian.

    Frequency response H(omega)=omega^2/(1+lam*omega^2).
    It enhances local/high-frequency structure while avoiding the unbounded omega^2
    amplification of a raw second derivative.
    """
    if dt <= 0 or lam < 0:
        raise ValueError("dt must be positive and lam non-negative")
    y = np.asarray(y)
    n = len(y)
    omega = 2.0 * math.pi * np.fft.fftfreq(n, d=dt)
    H = omega * omega / (1.0 + lam * omega * omega)
    return np.fft.ifft(H * np.fft.fft(y))


def steering_vector(t: np.ndarray, beta: float, gamma: float, normalize: bool = True) -> np.ndarray:
    """Complex source atom exp((beta-1/2)t) exp(i gamma t)."""
    t = np.asarray(t, dtype=float)
    a = np.exp((float(beta) - 0.5) * t + 1j * float(gamma) * t)
    if normalize:
        nrm = np.linalg.norm(a)
        if nrm:
            a = a / nrm
    return a


def _whitener_from_covariance(covariance: np.ndarray, ridge: float = 1e-10) -> np.ndarray:
    """Return R^{-1/2} for a symmetric positive semidefinite covariance matrix."""
    R = np.asarray(covariance, dtype=float)
    if R.ndim != 2 or R.shape[0] != R.shape[1]:
        raise ValueError("covariance must be square")
    vals, vecs = np.linalg.eigh((R + R.T) / 2.0)
    scale = max(float(np.max(vals)), 1.0)
    vals = np.maximum(vals, ridge * scale)
    return (vecs / np.sqrt(vals)[None, :]) @ vecs.T


def matched_filter_score(
    y: np.ndarray,
    t: np.ndarray,
    beta: float,
    gamma: float,
    covariance: np.ndarray | None = None,
) -> float:
    """Normalized GLS/matched-filter score in [0,1] for one candidate source.

    This is a localization diagnostic, not a hypothesis test with probabilistic noise.
    The 'noise' in explicit-formula applications is deterministic and correlated.
    """
    y = np.asarray(y, dtype=complex)
    a = steering_vector(t, beta, gamma, normalize=False)
    if len(y) != len(a):
        raise ValueError("y and t must have the same length")
    if covariance is not None:
        W = _whitener_from_covariance(covariance)
        y = W @ y
        a = W @ a
    yy = float(np.vdot(y, y).real)
    aa = float(np.vdot(a, a).real)
    if yy <= 0 or aa <= 0:
        return 0.0
    return float(abs(np.vdot(a, y)) ** 2 / (aa * yy))


def matched_filter_map(
    y: np.ndarray,
    t: np.ndarray,
    betas,
    gammas,
    covariance: np.ndarray | None = None,
) -> np.ndarray:
    """2-D source map P(beta,gamma) using normalized matched-filter scores."""
    betas = np.asarray(list(betas), dtype=float)
    gammas = np.asarray(list(gammas), dtype=float)
    out = np.empty((len(betas), len(gammas)), dtype=float)
    for i, beta in enumerate(betas):
        for j, gamma in enumerate(gammas):
            out[i, j] = matched_filter_score(y, t, beta, gamma, covariance=covariance)
    return out


def morlet_demodulated_envelope(
    y: np.ndarray,
    t: np.ndarray,
    gamma: float,
    sigma_t: float,
) -> np.ndarray:
    """Morlet-like local complex amplitude around angular frequency gamma.

    We demodulate y by exp(-i gamma t) and Gaussian-average the baseband signal.
    For a single mode exp((beta-1/2)t) exp(i gamma t), the logarithmic slope of
    the envelope estimates beta-1/2 away from boundaries.
    """
    t = np.asarray(t, dtype=float)
    y = np.asarray(y, dtype=complex)
    if len(t) < 2:
        raise ValueError("need at least two samples")
    dt = float(t[1] - t[0])
    if not np.allclose(np.diff(t), dt, rtol=1e-10, atol=1e-12):
        raise ValueError("t must be uniformly spaced")
    baseband = y * np.exp(-1j * float(gamma) * t)
    return gaussian_average(baseband, dt, sigma_t)


def envelope_growth_rate(envelope: np.ndarray, t: np.ndarray, trim: float = 0.15) -> float:
    """Least-squares slope of log|envelope| vs t after trimming boundaries."""
    t = np.asarray(t, dtype=float)
    env = np.asarray(envelope)
    n = len(t)
    k = int(max(0, min(n // 3, round(trim * n))))
    sl = slice(k, n - k if k else n)
    x = t[sl]
    z = np.log(np.maximum(np.abs(env[sl]), 1e-300))
    x0 = x - np.mean(x)
    den = float(np.dot(x0, x0))
    if den == 0:
        return 0.0
    return float(np.dot(x0, z - np.mean(z)) / den)


def source_design_matrix(t: np.ndarray, candidates) -> np.ndarray:
    """Columns are normalized steering vectors for (beta,gamma) candidates."""
    cols = [steering_vector(t, b, g, normalize=True) for b, g in candidates]
    if not cols:
        return np.zeros((len(t), 0), dtype=complex)
    return np.column_stack(cols)


def visibility_metrics(
    t: np.ndarray,
    candidates,
    covariance: np.ndarray | None = None,
) -> dict[str, float]:
    """Finite-dimensional observability diagnostics for a candidate source family.

    Returns min singular value, max singular value and condition number after optional
    whitening.  A proof-level RH application would require a uniform lower bound as
    frequency/height and model dimension grow; this routine supplies only finite tests.
    """
    A = source_design_matrix(t, candidates)
    if A.shape[1] == 0:
        return {"sigma_min": 0.0, "sigma_max": 0.0, "condition": math.inf}
    if covariance is not None:
        A = _whitener_from_covariance(covariance) @ A
        # re-normalize columns after whitening
        norms = np.linalg.norm(A, axis=0)
        A = A / np.where(norms > 0, norms, 1.0)
    s = np.linalg.svd(A, compute_uv=False)
    smin = float(np.min(s))
    smax = float(np.max(s))
    cond = smax / smin if smin > 0 else math.inf
    return {"sigma_min": smin, "sigma_max": smax, "condition": cond}


def synthetic_source_signal(t: np.ndarray, sources, amplitudes=None) -> np.ndarray:
    """Deterministic synthetic sum of source modes, useful for rejection tests."""
    t = np.asarray(t, dtype=float)
    sources = list(sources)
    if amplitudes is None:
        amplitudes = [1.0] * len(sources)
    if len(amplitudes) != len(sources):
        raise ValueError("amplitudes and sources must have the same length")
    y = np.zeros(len(t), dtype=complex)
    for amp, (beta, gamma) in zip(amplitudes, sources):
        y += complex(amp) * steering_vector(t, beta, gamma, normalize=False)
    return y
