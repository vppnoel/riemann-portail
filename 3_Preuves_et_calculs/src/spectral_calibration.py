"""Two-parameter spectral calibration utilities for v3.

These routines define and compute windowed spectral energies of
    B(t) = exp(-t/2) C(exp(t)).
They are diagnostics / calibration tools. They do NOT prove zero-density estimates.
"""
from __future__ import annotations

import math
import numpy as np


def B_grid_from_C(C: np.ndarray, L: float, dt: float = 0.01) -> tuple[np.ndarray, np.ndarray]:
    """Sample B(t)=e^{-t/2} C(e^t) on a uniform log-time grid.

    C[k] is interpreted as the step function sum_{n<=x} c(n) for k<=x<k+1.
    The grid stops before exp(t) exceeds the available C array.
    """
    Lmax = min(float(L), math.log(max(1, len(C) - 1)))
    t = np.arange(0.0, Lmax, dt, dtype=float)
    x = np.floor(np.exp(t)).astype(np.int64)
    x = np.clip(x, 0, len(C) - 1)
    B = np.exp(-0.5 * t) * C[x]
    return t, B


def hann_window(n: int) -> np.ndarray:
    """A deterministic Hann window, including the n<=1 edge cases."""
    if n <= 0:
        return np.zeros(0, dtype=float)
    if n == 1:
        return np.ones(1, dtype=float)
    j = np.arange(n, dtype=float)
    return 0.5 - 0.5 * np.cos(2.0 * math.pi * j / (n - 1))


def windowed_fourier(t: np.ndarray, B: np.ndarray, window: str = "hann") -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return angular frequencies omega and continuous-FT approximation F(omega).

    F(omega_k) ~= int B(t) w(t) exp(-i omega_k t) dt.
    Full FFT frequencies are returned, sorted increasingly.
    """
    if len(t) != len(B):
        raise ValueError("t and B must have the same length")
    if len(t) < 2:
        raise ValueError("need at least two samples")
    dt = float(t[1] - t[0])
    if not np.allclose(np.diff(t), dt, rtol=1e-10, atol=1e-12):
        raise ValueError("t must be uniformly spaced")
    if window == "hann":
        w = hann_window(len(t))
    elif window == "none":
        w = np.ones(len(t), dtype=float)
    else:
        raise ValueError(f"unknown window: {window}")
    signal = np.asarray(B, dtype=float) * w
    F = dt * np.fft.fft(signal)
    omega = 2.0 * math.pi * np.fft.fftfreq(len(t), d=dt)
    order = np.argsort(omega)
    return omega[order], F[order], signal


def parseval_energies(t: np.ndarray, B: np.ndarray, window: str = "hann") -> tuple[float, float]:
    """Return time energy and spectral energy; they agree up to discretization."""
    omega, F, signal = windowed_fourier(t, B, window=window)
    dt = float(t[1] - t[0])
    domega = float(omega[1] - omega[0])
    e_time = float(np.sum(np.abs(signal) ** 2) * dt)
    e_freq = float(np.sum(np.abs(F) ** 2) * domega / (2.0 * math.pi))
    return e_time, e_freq


def gaussian_band_energy(
    t: np.ndarray,
    B: np.ndarray,
    T: float,
    Delta: float,
    window: str = "hann",
) -> float:
    """Compute a positive Gaussian-band version of Q_{w,W}(L;T,Delta).

    W(u)=exp(-u^2/2). This is a calibration observable, not a theorem about zeros.
    """
    if Delta <= 0:
        raise ValueError("Delta must be positive")
    omega, F, _ = windowed_fourier(t, B, window=window)
    domega = float(omega[1] - omega[0])
    W = np.exp(-0.5 * ((omega - float(T)) / float(Delta)) ** 2)
    return float(np.sum(W * np.abs(F) ** 2) * domega / (2.0 * math.pi))


def band_table(t: np.ndarray, B: np.ndarray, centers, Delta: float, window: str = "hann"):
    """Return rows (T,Delta,energy) for several spectral centers."""
    return [
        (float(T), float(Delta), gaussian_band_energy(t, B, float(T), float(Delta), window=window))
        for T in centers
    ]
