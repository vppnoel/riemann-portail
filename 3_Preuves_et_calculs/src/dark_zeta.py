"""DARK-ZETA / TOMO experimental detector for V6.

Purpose
-------
Build a falsifiable multi-observable detector comparing:
  * zeta,
  * a primitive Dirichlet L-function mod 5,
  * the Davenport--Heilbronn linear combination,
  * phase-randomized controls,
  * synthetic completely multiplicative controls.

This module is diagnostic only. It does not prove or assume RH.

The primary signal is the existing V5/V6 arithmetic signal C_F(t) obtained
from the generic logarithmic-derivative pipeline in ``rejection.py``. We map
it to logarithmic coordinates by g_F(u)=exp(-u/2) C_F(exp(u)).

TOMO-2 uses a circular translation Gram matrix and therefore depends only on
the discrete power spectrum. TOMO-3 uses segment-averaged bicoherence and can
retain phase-coupling information that TOMO-2 necessarily discards.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np

try:
    from rejection import (
        build,
        coeffs,
        log_derivative_coeffs,
        c_from_lambda,
    )
except ImportError:  # package-style import
    from .rejection import (
        build,
        coeffs,
        log_derivative_coeffs,
        c_from_lambda,
    )


@dataclass(frozen=True)
class Tomo2Metrics:
    entropy: float
    effective_rank: float
    top_eigen_fraction: float
    condition_number_positive: float


@dataclass(frozen=True)
class Tomo3Metrics:
    mean_bicoherence: float
    median_bicoherence: float
    q90_bicoherence: float
    max_bicoherence: float
    mean_bispectrum_amplitude: float
    n_triads: int
    n_segments: int


def signal_from_c(c: np.ndarray, n_log: int = 4096, t_min: float = 1.0,
                  t_max: float | None = None, normalize: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """Return logarithmic grid u and g(u)=exp(-u/2) C(exp(u)).

    C is the stepwise partial sum of c. Sampling is uniform in log t. The
    returned signal is centered; when ``normalize`` is true it has unit RMS.
    """
    N = len(c) - 1
    if t_max is None:
        t_max = float(N)
    if not (1.0 <= t_min < t_max <= N + 1e-12):
        raise ValueError("Require 1 <= t_min < t_max <= len(c)-1")
    u = np.linspace(math.log(t_min), math.log(t_max), int(n_log), endpoint=False)
    t = np.exp(u)
    idx = np.floor(t).astype(int)
    idx = np.clip(idx, 1, N)
    C = np.cumsum(c)
    g = np.exp(-0.5 * u) * C[idx]
    g = np.asarray(g, dtype=complex)
    g = g - np.mean(g)
    if normalize:
        rms = float(np.sqrt(np.mean(np.abs(g) ** 2)))
        if rms > 0:
            g = g / rms
    return u, g


def phase_randomize_preserve_power(g: np.ndarray, seed: int = 0) -> np.ndarray:
    """Randomize discrete Fourier phases while preserving |FFT(g)| exactly.

    Works for real or complex signals. Since the inverse signal may be complex,
    this is a power-spectrum control rather than a surrogate constrained to be real.
    """
    rng = np.random.default_rng(seed)
    G = np.fft.fft(np.asarray(g, dtype=complex))
    phase = rng.uniform(-math.pi, math.pi, size=G.shape)
    # Keep exact zeros zero. Randomize all nonzero Fourier phases.
    Gr = np.abs(G) * np.exp(1j * phase)
    out = np.fft.ifft(Gr)
    # Match centering/normalization conventions without changing the circular
    # power spectrum materially: DC is set to zero exactly in both original
    # and surrogate because signal_from_c centers first.
    out = out - np.mean(out)
    rms = float(np.sqrt(np.mean(np.abs(out) ** 2)))
    if rms > 0:
        out = out / rms
    return out


def tomo2_gram(g: np.ndarray, n_shifts: int = 32, shift_step: int = 8) -> np.ndarray:
    """Circular translation Gram matrix K_ij=<T_i g,T_j g>/M.

    Circular translation is deliberate: it gives an exact internal control that
    phase-randomized signals with the same power spectrum must produce the same K.
    """
    g = np.asarray(g, dtype=complex)
    M = len(g)
    shifts = np.arange(int(n_shifts), dtype=int) * int(shift_step)
    X = np.column_stack([np.roll(g, int(s) % M) for s in shifts])
    K = (X.conj().T @ X) / M
    # enforce Hermitian symmetry against roundoff
    return 0.5 * (K + K.conj().T)


def tomo2_metrics(K: np.ndarray) -> Tomo2Metrics:
    ev = np.linalg.eigvalsh(np.asarray(K, dtype=complex)).real
    ev[ev < 0] = np.maximum(ev[ev < 0], -1e-14)
    ev = np.clip(ev, 0.0, None)
    total = float(np.sum(ev))
    if total <= 0:
        return Tomo2Metrics(float("nan"), float("nan"), float("nan"), float("nan"))
    p = ev / total
    nz = p[p > 0]
    H = -float(np.sum(nz * np.log(nz)))
    entropy = H / math.log(len(ev)) if len(ev) > 1 else 0.0
    erank = math.exp(H)
    top = float(ev[-1] / total)
    pos = ev[ev > max(1e-12 * ev[-1], 1e-15)]
    cond = float(pos[-1] / pos[0]) if len(pos) else float("inf")
    return Tomo2Metrics(entropy, erank, top, cond)


def _segment_ffts(g: np.ndarray, seg_len: int = 512, hop: int = 256) -> np.ndarray:
    g = np.asarray(g, dtype=complex)
    if seg_len > len(g):
        raise ValueError("seg_len must not exceed signal length")
    starts = list(range(0, len(g) - seg_len + 1, hop))
    if len(starts) < 3:
        raise ValueError("Need at least three segments for TOMO-3")
    win = np.hanning(seg_len)
    arr = []
    for s in starts:
        x = g[s:s + seg_len]
        x = x - np.mean(x)
        xw = x * win
        scale = math.sqrt(float(np.mean(np.abs(xw) ** 2)))
        if scale > 0:
            xw = xw / scale
        arr.append(np.fft.fft(xw))
    return np.asarray(arr)


def tomo3_bicoherence(g: np.ndarray, seg_len: int = 512, hop: int = 256,
                      max_bin: int = 24) -> tuple[np.ndarray, np.ndarray, Tomo3Metrics]:
    """Estimate squared bicoherence over positive-frequency triads.

    For each (k,l), with k,l>=1 and k+l below Nyquist, estimate
      b^2 = |E[X_k X_l conj X_{k+l}]|^2 /
            (E[|X_k X_l|^2] E[|X_{k+l}|^2]).
    Values are clipped to [0,1] against floating-point roundoff.
    """
    X = _segment_ffts(g, seg_len=seg_len, hop=hop)
    nseg = X.shape[0]
    ny = seg_len // 2
    records = []
    vals = []
    amps = []
    for k in range(1, int(max_bin) + 1):
        for l in range(k, int(max_bin) + 1):
            q = k + l
            if q >= ny:
                continue
            z = X[:, k] * X[:, l] * np.conj(X[:, q])
            B = np.mean(z)
            den = float(np.mean(np.abs(X[:, k] * X[:, l]) ** 2) * np.mean(np.abs(X[:, q]) ** 2))
            if den <= 1e-30:
                continue
            b2 = float((abs(B) ** 2) / den)
            b2 = min(1.0, max(0.0, b2))
            records.append((k, l, q, b2, float(abs(B))))
            vals.append(b2)
            amps.append(float(abs(B)))
    if not vals:
        met = Tomo3Metrics(*(float("nan"),) * 5, n_triads=0, n_segments=nseg)
        return np.empty((0, 5)), np.asarray(X), met
    v = np.asarray(vals, dtype=float)
    a = np.asarray(amps, dtype=float)
    met = Tomo3Metrics(
        mean_bicoherence=float(np.mean(v)),
        median_bicoherence=float(np.median(v)),
        q90_bicoherence=float(np.quantile(v, 0.90)),
        max_bicoherence=float(np.max(v)),
        mean_bispectrum_amplitude=float(np.mean(a)),
        n_triads=len(v),
        n_segments=nseg,
    )
    return np.asarray(records, dtype=float), np.asarray(X), met


def multiplicative_defect(a: np.ndarray, P: int = 48) -> dict[str, float]:
    """Coefficient-level defect for coprime pairs m,n <= P.

    Requires coefficients through P^2. Returns raw mean-square defect and a
    scale-normalized defect in [0,~2] for typical bounded coefficient families.
    """
    if P * P >= len(a):
        raise ValueError("Coefficient array must extend beyond P^2")
    num = 0.0
    den = 0.0
    count = 0
    max_def = 0.0
    for m in range(2, P + 1):
        for n in range(2, P + 1):
            if math.gcd(m, n) != 1:
                continue
            d = a[m * n] - a[m] * a[n]
            d2 = float(abs(d) ** 2)
            num += d2
            den += float(abs(a[m * n]) ** 2 + abs(a[m] * a[n]) ** 2)
            max_def = max(max_def, math.sqrt(d2))
            count += 1
    return {
        "defect_mse": num / count if count else float("nan"),
        "defect_normalized": num / den if den > 0 else 0.0,
        "defect_max": max_def,
        "defect_pairs": float(count),
    }


def c_from_coefficients(a: np.ndarray, pole: bool = False) -> np.ndarray:
    lam = log_derivative_coeffs(np.asarray(a, dtype=complex))
    return c_from_lambda(lam, pole=pole)


def interpolation_coeffs_chi_to_dh(N: int, theta: float) -> np.ndarray:
    """Synthetic path from multiplicative chi_5 (theta=0) to DH (theta=1)."""
    achi = coeffs("L_chi5", N)
    adh = coeffs("DH", N)
    return (1.0 - float(theta)) * achi + float(theta) * adh


def _smallest_prime_factor(N: int) -> np.ndarray:
    spf = np.arange(N + 1, dtype=int)
    if N >= 1:
        spf[1] = 1
    for p in range(2, int(math.sqrt(N)) + 1):
        if spf[p] == p:
            start = p * p
            for k in range(start, N + 1, p):
                if spf[k] == k:
                    spf[k] = p
    return spf


def steinhaus_completely_multiplicative(N: int, seed: int = 0) -> np.ndarray:
    """Random completely multiplicative coefficients with prime values on unit circle."""
    rng = np.random.default_rng(seed)
    spf = _smallest_prime_factor(N)
    phase_by_prime: dict[int, complex] = {}
    a = np.zeros(N + 1, dtype=complex)
    a[1] = 1.0
    for n in range(2, N + 1):
        p = int(spf[n])
        if p not in phase_by_prime:
            phase_by_prime[p] = complex(np.exp(1j * rng.uniform(-math.pi, math.pi)))
        a[n] = phase_by_prime[p] * a[n // p]
    return a


def build_signal(kind: str, N: int = 32768, n_log: int = 4096) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return (a,c,u,g) for zeta/L_chi5/DH using the established rejection pipeline."""
    a, _lam, c = build(kind, N)
    u, g = signal_from_c(c, n_log=n_log, t_max=N)
    return a, c, u, g
