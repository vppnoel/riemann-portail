"""DUAL-LOCK finite Weil-compression detector (V6.3).

This module builds finite compressions of the arithmetic/archimedean side of
Guinand--Weil-type explicit formulas using compactly supported, frequency-
modulated tent test functions.  No zero locations enter the construction.

The main adversarial pair is:
  * L_pair_chi5: the average of the explicit forms for the primitive order-4
    Dirichlet character mod 5 and its conjugate.  It has the same conductor
    and odd archimedean gamma factor as Davenport--Heilbronn, while retaining
    Euler-product local coefficients.
  * DH: Davenport--Heilbronn.  It has the same type of global functional
    symmetry but generalized logarithmic-derivative coefficients that leak
    away from prime powers.

A negative eigenvalue of a finite compression is an inertia witness for that
chosen test subspace.  For zeta, positivity of all admissible test functions
is Weil's criterion and is equivalent to RH; this code is therefore a
structural/adversarial experiment, not a proof method.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import math
from pathlib import Path
import warnings

import numpy as np
from scipy.integrate import quad, IntegrationWarning
from scipy.signal import fftconvolve
from scipy.special import digamma

try:
    from rejection import build
except ImportError:
    from .rejection import build


@dataclass(frozen=True)
class DualKind:
    q: int
    parity: int       # gamma factor Gamma((s+parity)/2)
    pole: bool
    source_kind: str  # key understood by rejection.build
    take_real_pair: bool = False


KINDS: dict[str, DualKind] = {
    "zeta": DualKind(q=1, parity=0, pole=True, source_kind="zeta"),
    # Average the chi and conjugate-chi explicit forms.  Same q/parity as DH.
    "L_pair_chi5": DualKind(q=5, parity=1, pole=False,
                            source_kind="L_chi5", take_real_pair=True),
    "DH": DualKind(q=5, parity=1, pole=False, source_kind="DH"),
}


def _sinc(z):
    z = np.asarray(z, dtype=complex)
    out = np.ones_like(z)
    mask = np.abs(z) > 1e-12
    out[mask] = np.sin(z[mask]) / z[mask]
    if np.ndim(out) == 0:
        return complex(out)
    return out


def tent_fourier(t, half_width: float, frequency: float):
    """Fourier transform of (1-|x|/w)_+ cos(frequency*x).

    Convention: H(t)=int f(x) exp(i t x) dx.
    """
    w = float(half_width)
    t = np.asarray(t, dtype=complex)

    def h0(z):
        return w * _sinc(0.5 * w * z) ** 2

    out = 0.5 * (h0(t - frequency) + h0(t + frequency))
    if np.ndim(out) == 0:
        return complex(out)
    return out


def _tri(x: float, w: float) -> float:
    return max(0.0, 1.0 - abs(x) / w)


def _basis_value(x: float, w: float, xi: float) -> float:
    return _tri(x, w) * math.cos(xi * x)


def correlation_direct(x: float, w: float, xi: float, xj: float,
                       eps: float = 2e-8) -> float:
    """(f_i * f_j)(x) for real even modulated-tent basis functions.

    Since each f_j is even, this is also the autocorrelation-type kernel used
    in the Weil quadratic form.  Breakpoints of the piecewise-linear envelope
    are supplied explicitly; oscillatory integration is numerical.
    """
    lo = max(-w, x - w)
    hi = min(w, x + w)
    if hi <= lo:
        return 0.0
    pts = [lo, hi]
    for p in (0.0, x):
        if lo < p < hi:
            pts.append(p)
    pts = sorted(set(pts))
    total = 0.0
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", IntegrationWarning)
        for a, b in zip(pts[:-1], pts[1:]):
            val, _ = quad(
                lambda y: _basis_value(y, w, xi)
                * _basis_value(x - y, w, xj),
                a, b, epsabs=eps, epsrel=eps, limit=350,
            )
            total += val
    return float(total)


def _log_derivative_weights(kind: str, nmax: int) -> np.ndarray:
    spec = KINDS[kind]
    _, lam, _ = build(spec.source_kind, int(nmax))
    if spec.take_real_pair:
        # Average of chi and conjugate-chi explicit forms.
        return np.real(lam)
    # zeta and DH are real to numerical precision in this implementation.
    return np.real(lam)


def _arch_matrix(frequencies: np.ndarray, w: float, parity: int,
                 tmax: float = 350.0, dt: float = 0.02) -> np.ndarray:
    """Archimedean digamma contribution by high-resolution trapezoid rule.

    For the present modulated tents the integrand decays as O(t^-4 log t).
    Cross-checks against adaptive quadrature are at ~1e-8 absolute scale for
    the frequency range used in the V6.3 scan.
    """
    tmax = max(float(tmax), float(np.max(np.abs(frequencies))) + 80.0)
    t = np.arange(0.0, tmax + 0.5 * dt, dt)
    arg0 = (0.5 + parity) / 2.0
    psi = np.real(digamma(arg0 + 0.5j * t))
    H = np.array([np.real(tent_fourier(t, w, xi)) for xi in frequencies])
    wt = np.ones_like(t)
    wt[[0, -1]] = 0.5
    wt *= dt / math.pi
    return (H * (psi * wt)) @ H.T


def _pole_vector(frequencies: np.ndarray, w: float) -> np.ndarray:
    return np.array([
        float(np.real(tent_fourier(0.5j, w, xi))) for xi in frequencies
    ])


def compression_accurate(
    center: float,
    kind: str,
    *,
    half_width: float = 2.5,
    dimension: int = 7,
    frequency_step: float = 0.6,
    arch_dt: float = 0.02,
    correlation_eps: float = 2e-8,
) -> tuple[np.ndarray, np.ndarray]:
    """Accurate finite compression from primes/generalized local data + gamma.

    The basis is fixed before looking at zeros:
        f_j(x)=(1-|x|/w)_+ cos(xi_j x),
        xi_j=center + frequency_step*(j-(m-1)/2).

    The convolution support is [-2w,2w], so the local sum is finite and only
    uses n <= exp(2w).  No zeros are loaded or used.
    """
    if kind not in KINDS:
        raise ValueError(f"unknown kind {kind!r}")
    spec = KINDS[kind]
    m = int(dimension)
    w = float(half_width)
    frequencies = float(center) + frequency_step * (
        np.arange(m, dtype=float) - (m - 1) / 2.0
    )
    nmax = int(math.floor(math.exp(2.0 * w))) + 2
    b = _log_derivative_weights(kind, nmax)

    M = _arch_matrix(frequencies, w, spec.parity, dt=arch_dt)

    # Conductor term F_ij(0) log(q/pi)
    F0 = np.zeros((m, m), dtype=float)
    for i, xi in enumerate(frequencies):
        for j in range(i + 1):
            xj = frequencies[j]
            v = correlation_direct(0.0, w, xi, xj, eps=correlation_eps)
            F0[i, j] = F0[j, i] = v
    M += math.log(spec.q / math.pi) * F0

    # Pole at s=1 for zeta; for even test kernels this is 2 h(i/2).
    if spec.pole:
        pv = _pole_vector(frequencies, w)
        M += 2.0 * np.outer(pv, pv)

    # Local/generalized logarithmic derivative contribution.
    logs = []
    weights = []
    for n in range(2, nmax + 1):
        if abs(b[n]) <= 1e-14:
            continue
        lx = math.log(n)
        if lx <= 2.0 * w + 1e-12:
            logs.append(lx)
            weights.append(float(b[n]) / math.sqrt(n))

    for i, xi in enumerate(frequencies):
        for j in range(i + 1):
            xj = frequencies[j]
            local = 0.0
            for lx, weight in zip(logs, weights):
                local += weight * correlation_direct(
                    lx, w, xi, xj, eps=correlation_eps
                )
            M[i, j] -= 2.0 * local
            if i != j:
                M[j, i] = M[i, j]

    M = 0.5 * (M + M.T)
    return frequencies, M


def compression_fast(
    center: float,
    kind: str,
    *,
    half_width: float = 2.5,
    dimension: int = 7,
    frequency_step: float = 0.6,
    dx: float = 0.004,
    arch_dt: float = 0.03,
) -> tuple[np.ndarray, np.ndarray]:
    """Fast screening version; candidate negatives must be accurately refined."""
    if kind not in KINDS:
        raise ValueError(f"unknown kind {kind!r}")
    spec = KINDS[kind]
    m = int(dimension)
    w = float(half_width)
    frequencies = float(center) + frequency_step * (
        np.arange(m, dtype=float) - (m - 1) / 2.0
    )
    nmax = int(math.floor(math.exp(2.0 * w))) + 2
    b = _log_derivative_weights(kind, nmax)

    # Basis sampling in x for FFT correlations.
    x = np.arange(-w, w + 0.5 * dx, dx)
    envelope = np.maximum(0.0, 1.0 - np.abs(x) / w)
    basis = np.array([envelope * np.cos(xi * x) for xi in frequencies])
    wx = np.ones_like(x)
    wx[[0, -1]] = 0.5
    wx *= dx
    F0 = (basis * wx) @ basis.T

    M = _arch_matrix(frequencies, w, spec.parity, dt=arch_dt)
    M += math.log(spec.q / math.pi) * F0
    if spec.pole:
        pv = _pole_vector(frequencies, w)
        M += 2.0 * np.outer(pv, pv)

    n = np.arange(2, nmax + 1)
    mask = np.abs(b[2:]) > 1e-14
    n = n[mask]
    logs = np.log(n.astype(float))
    weights = b[n] / np.sqrt(n.astype(float))
    support_mask = logs <= 2.0 * w + 1e-12
    logs = logs[support_mask]
    weights = weights[support_mask]

    for i in range(m):
        for j in range(i + 1):
            conv = fftconvolve(basis[i], basis[j], mode="full") * dx
            xv = np.linspace(-2.0 * w, 2.0 * w, len(conv))
            vals = np.interp(logs, xv, conv) if len(logs) else np.array([])
            local = float(np.dot(weights, vals)) if len(vals) else 0.0
            M[i, j] -= 2.0 * local
            if i != j:
                M[j, i] = M[i, j]
    M = 0.5 * (M + M.T)
    return frequencies, M


def inertia(M: np.ndarray, tol: float = 1e-10) -> tuple[int, int, int]:
    ev = np.linalg.eigvalsh(np.asarray(M, dtype=float))
    return (
        int(np.sum(ev > tol)),
        int(np.sum(ev < -tol)),
        int(np.sum(np.abs(ev) <= tol)),
    )


def matrix_metrics(M: np.ndarray) -> dict[str, float | int]:
    ev = np.linalg.eigvalsh(np.asarray(M, dtype=float))
    scale = max(float(np.max(np.abs(ev))), 1e-300)
    pos, neg, zero = inertia(M)
    return {
        "lambda_min": float(ev[0]),
        "lambda_max": float(ev[-1]),
        "lambda_min_scaled": float(ev[0] / scale),
        "trace": float(np.trace(M)),
        "n_positive": pos,
        "n_negative": neg,
        "n_near_zero": zero,
    }


def scan_centers(
    centers: np.ndarray,
    kind: str,
    *,
    half_width: float = 2.5,
    dimension: int = 7,
    frequency_step: float = 0.6,
) -> list[dict[str, float | int]]:
    rows = []
    for c in np.asarray(centers, dtype=float):
        _, M = compression_fast(
            float(c), kind,
            half_width=half_width,
            dimension=dimension,
            frequency_step=frequency_step,
        )
        row = {
            "center": float(c),
            "half_width": float(half_width),
            "dimension": int(dimension),
            "frequency_step": float(frequency_step),
            **matrix_metrics(M),
        }
        rows.append(row)
    return rows


def negative_intervals(rows: list[dict], threshold: float = -1e-5) -> list[dict]:
    groups: list[list[dict]] = []
    current: list[dict] = []
    for row in rows:
        if float(row["lambda_min"]) < threshold:
            if current and float(row["center"]) > float(current[-1]["center"]) + 1.01:
                groups.append(current)
                current = []
            current.append(row)
        elif current:
            groups.append(current)
            current = []
    if current:
        groups.append(current)

    out = []
    for g in groups:
        best = min(g, key=lambda r: float(r["lambda_min"]))
        out.append({
            "start": float(g[0]["center"]),
            "end": float(g[-1]["center"]),
            "best_center": float(best["center"]),
            "best_lambda_min_fast": float(best["lambda_min"]),
            "half_width": float(best["half_width"]),
        })
    return out


def load_offline_dh_zeros(path: str | Path, sigma_tol: float = 1e-3,
                          tmax: float | None = None) -> list[tuple[float, float]]:
    """Post-hoc validation only.  Never called by compression construction."""
    import csv
    rows = list(csv.DictReader(Path(path).open()))
    pts: list[tuple[float, float]] = []
    for r in rows:
        sigma = float(r["sigma"])
        t = float(r["t"])
        if abs(sigma - 0.5) <= sigma_tol:
            continue
        if tmax is not None and t > tmax:
            continue
        if all(abs(t - u[1]) > 1e-5 or abs(sigma - u[0]) > 1e-5 for u in pts):
            pts.append((sigma, t))
    return sorted(pts, key=lambda z: z[1])


def nearest_interval_match(interval: dict, offline: list[tuple[float, float]]) -> dict:
    a, b = float(interval["start"]), float(interval["end"])
    if not offline:
        return {**interval, "nearest_sigma": math.nan, "nearest_t": math.nan,
                "distance_to_interval": math.nan}
    def dist(t):
        return 0.0 if a <= t <= b else min(abs(t - a), abs(t - b))
    sigma, t = min(offline, key=lambda z: dist(z[1]))
    return {
        **interval,
        "nearest_sigma": float(sigma),
        "nearest_t": float(t),
        "distance_to_interval": float(dist(t)),
    }
