"""PRIME-LOCK detector for V6.2.

PRIME-LOCK changes the observation channel after the first DARK-ZETA/TOMO run.
Instead of asking higher-order statistics to recover multiplicativity from one
aggregated signal, it resolves the logarithmic derivative into three arithmetic
channels:

  * prime channel: n = p,
  * higher prime-power channel: n = p^k, k >= 2,
  * leakage channel: n not a prime power.

For an Euler product, the logarithmic derivative is supported on prime powers.
For a degree-1 Euler factor (1-alpha_p p^{-s})^{-1}, the stronger tower law holds

    Lambda_F(p^k) / log p = (Lambda_F(p) / log p)^k.

The module measures both facts and then performs a controlled intervention:
"Eulerize" the observed prime data by enforcing the degree-1 tower law and zero
leakage, then quantify how much the established global c/C signal changes.

This is a diagnostic of Euler-product structure, not a criterion for RH.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import math
import numpy as np

try:
    from rejection import build, log_derivative_coeffs, c_from_lambda
    from dark_zeta import signal_from_c
except ImportError:
    from .rejection import build, log_derivative_coeffs, c_from_lambda
    from .dark_zeta import signal_from_c


@dataclass(frozen=True)
class PrimeLockMetrics:
    support_leakage: float
    tower_defect: float
    q_residual_ratio: float
    global_signal_coherence: float
    prime_energy_fraction: float
    higher_prime_power_energy_fraction: float
    leakage_energy_fraction: float

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


def smallest_prime_factor(N: int) -> np.ndarray:
    spf = np.zeros(N + 1, dtype=np.int64)
    for n in range(2, N + 1):
        if spf[n] == 0:
            spf[n] = n
            if n * n <= N:
                for k in range(n * n, N + 1, n):
                    if spf[k] == 0:
                        spf[k] = n
    return spf


def prime_power_tables(N: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return arrays base[n], exponent[n], is_prime_power[n]."""
    spf = smallest_prime_factor(N)
    base = np.zeros(N + 1, dtype=np.int64)
    exponent = np.zeros(N + 1, dtype=np.int64)
    is_pp = np.zeros(N + 1, dtype=bool)
    for n in range(2, N + 1):
        p = int(spf[n])
        x = n
        k = 0
        while x % p == 0:
            x //= p
            k += 1
        if x == 1:
            base[n] = p
            exponent[n] = k
            is_pp[n] = True
    return base, exponent, is_pp


def decompose_lambda(lam: np.ndarray) -> dict[str, np.ndarray]:
    """Split logarithmic-derivative coefficients into prime / pp-tail / leakage."""
    N = len(lam) - 1
    base, exponent, is_pp = prime_power_tables(N)
    prime = np.zeros_like(lam, dtype=complex)
    higher = np.zeros_like(lam, dtype=complex)
    leakage = np.zeros_like(lam, dtype=complex)
    for n in range(2, N + 1):
        if not is_pp[n]:
            leakage[n] = lam[n]
        elif exponent[n] == 1:
            prime[n] = lam[n]
        else:
            higher[n] = lam[n]
    return {
        "prime": prime,
        "higher_prime_power": higher,
        "leakage": leakage,
        "base": base,
        "exponent": exponent,
        "is_prime_power": is_pp,
    }


def support_leakage(lam: np.ndarray) -> float:
    parts = decompose_lambda(lam)
    total = float(np.sum(np.abs(np.asarray(lam)[2:]) ** 2))
    leak = float(np.sum(np.abs(parts["leakage"][2:]) ** 2))
    return leak / total if total > 0 else 0.0


def degree1_tower_defect(lam: np.ndarray) -> float:
    """Normalized defect in Lambda(p^k)/log p = (Lambda(p)/log p)^k.

    This is exact for degree-1 local Euler factors, including zeta and primitive
    Dirichlet L-functions. It is not intended as a universal identity for all
    higher-degree L-functions.
    """
    N = len(lam) - 1
    base, exponent, is_pp = prime_power_tables(N)
    num = 0.0
    den = 0.0
    for n in range(2, N + 1):
        if not is_pp[n] or exponent[n] < 2:
            continue
        p = int(base[n])
        k = int(exponent[n])
        lp = math.log(p)
        alpha = lam[p] / lp
        x = lam[n] / lp
        y = alpha ** k
        num += float(abs(x - y) ** 2)
        den += float(abs(x) ** 2 + abs(y) ** 2)
    return num / den if den > 0 else 0.0


def eulerize_lambda_degree1(lam: np.ndarray) -> np.ndarray:
    """Preserve prime values and impose a degree-1 Euler tower at all p^k.

    Non-prime-power logarithmic-derivative coefficients are set to zero.
    """
    N = len(lam) - 1
    base, exponent, is_pp = prime_power_tables(N)
    out = np.zeros_like(lam, dtype=complex)
    for n in range(2, N + 1):
        if not is_pp[n]:
            continue
        p = int(base[n])
        k = int(exponent[n])
        lp = math.log(p)
        alpha = lam[p] / lp
        out[n] = (alpha ** k) * lp
    return out


def q_energy(c: np.ndarray) -> float:
    N = len(c) - 1
    C = np.cumsum(c)
    m = np.arange(1, N, dtype=float)
    w = 1.0 / m - 1.0 / (m + 1.0)
    return float(np.sum(np.abs(C[1:N]) ** 2 * w))


def global_signal_coherence(c1: np.ndarray, c2: np.ndarray, n_log: int = 4096) -> float:
    N = min(len(c1), len(c2)) - 1
    _, g1 = signal_from_c(np.asarray(c1)[: N + 1], n_log=n_log, t_max=N)
    _, g2 = signal_from_c(np.asarray(c2)[: N + 1], n_log=n_log, t_max=N)
    den = float(np.linalg.norm(g1) * np.linalg.norm(g2))
    if den == 0:
        return 0.0
    return float(abs(np.vdot(g1, g2)) / den)


def prime_lock_metrics_from_lambda(lam: np.ndarray, pole: bool = False,
                                   n_log: int = 4096) -> PrimeLockMetrics:
    parts = decompose_lambda(lam)
    total = float(np.sum(np.abs(lam[2:]) ** 2))
    ep = float(np.sum(np.abs(parts["prime"][2:]) ** 2))
    eh = float(np.sum(np.abs(parts["higher_prime_power"][2:]) ** 2))
    el = float(np.sum(np.abs(parts["leakage"][2:]) ** 2))

    lam_e = eulerize_lambda_degree1(lam)
    c = c_from_lambda(lam, pole=pole)
    c_e = c_from_lambda(lam_e, pole=pole)
    q = q_energy(c)
    qr = q_energy(c - c_e)
    coh = global_signal_coherence(c, c_e, n_log=n_log)

    return PrimeLockMetrics(
        support_leakage=(el / total if total > 0 else 0.0),
        tower_defect=degree1_tower_defect(lam),
        q_residual_ratio=(qr / q if q > 0 else 0.0),
        global_signal_coherence=coh,
        prime_energy_fraction=(ep / total if total > 0 else 0.0),
        higher_prime_power_energy_fraction=(eh / total if total > 0 else 0.0),
        leakage_energy_fraction=(el / total if total > 0 else 0.0),
    )


def prime_lock_metrics_from_coefficients(a: np.ndarray, pole: bool = False,
                                         n_log: int = 4096) -> PrimeLockMetrics:
    lam = log_derivative_coeffs(np.asarray(a, dtype=complex))
    return prime_lock_metrics_from_lambda(lam, pole=pole, n_log=n_log)


def build_prime_lock(kind: str, N: int = 32768, n_log: int = 4096):
    """Return a, lambda, c, eulerized_lambda, eulerized_c, metrics."""
    a, lam, c = build(kind, N)
    lam_e = eulerize_lambda_degree1(lam)
    c_e = c_from_lambda(lam_e, pole=(kind == "zeta"))
    metrics = prime_lock_metrics_from_lambda(lam, pole=(kind == "zeta"), n_log=n_log)
    return a, lam, c, lam_e, c_e, metrics


def channel_cumulative_signals(lam: np.ndarray, n_log: int = 4096) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    """Log-grid cumulative signals of prime, higher-pp, and leakage channels."""
    N = len(lam) - 1
    parts = decompose_lambda(lam)
    u = np.linspace(0.0, math.log(N), int(n_log), endpoint=False)
    t = np.exp(u)
    idx = np.clip(np.floor(t).astype(int), 1, N)
    out: dict[str, np.ndarray] = {}
    total_coeff_norm = float(np.linalg.norm(np.asarray(lam)[2:]))
    for key in ("prime", "higher_prime_power", "leakage"):
        coeff_norm = float(np.linalg.norm(parts[key][2:]))
        if total_coeff_norm > 0 and coeff_norm <= 1e-12 * total_coeff_norm:
            out[key] = np.zeros_like(u, dtype=complex)
            continue
        s = np.cumsum(parts[key])
        g = np.exp(-0.5 * u) * s[idx]
        g = np.asarray(g, dtype=complex)
        g = g - np.mean(g)
        rms = float(np.sqrt(np.mean(np.abs(g) ** 2)))
        if rms > 0:
            g = g / rms
        out[key] = g
    return u, out


def channel_gram(lam: np.ndarray, n_log: int = 4096) -> np.ndarray:
    """3x3 Gram matrix of normalized arithmetic channels.

    Zero channels remain zero. Order: prime, higher prime powers, leakage.
    """
    _, ch = channel_cumulative_signals(lam, n_log=n_log)
    keys = ("prime", "higher_prime_power", "leakage")
    G = np.zeros((3, 3), dtype=complex)
    for i, ki in enumerate(keys):
        for j, kj in enumerate(keys):
            G[i, j] = np.vdot(ch[ki], ch[kj]) / len(ch[ki])
    return 0.5 * (G + G.conj().T)


def gram_effective_rank(G: np.ndarray) -> float:
    ev = np.clip(np.linalg.eigvalsh(G).real, 0.0, None)
    s = float(np.sum(ev))
    if s <= 0:
        return 0.0
    p = ev / s
    p = p[p > 0]
    return float(math.exp(-np.sum(p * np.log(p))))
