"""DARK-RESIDUAL detector for V6.3.

The point is not to invent a new energy, but to quantify how much of the final
quadratic-form value survives after cancellation between independently defined
Archimedean/conductor/pole and local-prime contributions.

No zero locations enter the construction. Zeros may only be compared post hoc.
"""
from __future__ import annotations

import math
import numpy as np

from dual_lock import (
    KINDS,
    _arch_matrix,
    _log_derivative_weights,
    _pole_vector,
    correlation_direct,
)


def compression_components(
    center: float,
    kind: str,
    *,
    half_width: float = 2.5,
    dimension: int = 7,
    frequency_step: float = 0.6,
    arch_dt: float = 0.02,
    correlation_eps: float = 2e-8,
):
    """Return the finite Weil compression split into canonical contributions.

    Components are defined before diagonalization:
      archimedean : gamma/digamma term,
      conductor   : log(q/pi) F(0),
      pole        : zeta pole contribution (zero for non-polar examples),
      local       : logarithmic-derivative / prime-side term,
      total       : exact sum of the four matrices.
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

    arch = _arch_matrix(frequencies, w, spec.parity, dt=arch_dt)

    f0 = np.zeros((m, m), dtype=float)
    for i, xi in enumerate(frequencies):
        for j in range(i + 1):
            v = correlation_direct(0.0, w, xi, frequencies[j], eps=correlation_eps)
            f0[i, j] = f0[j, i] = v
    conductor = math.log(spec.q / math.pi) * f0

    pole = np.zeros((m, m), dtype=float)
    if spec.pole:
        pv = _pole_vector(frequencies, w)
        pole = 2.0 * np.outer(pv, pv)

    local = np.zeros((m, m), dtype=float)
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
            loc = 0.0
            for lx, weight in zip(logs, weights):
                loc += weight * correlation_direct(
                    lx, w, xi, frequencies[j], eps=correlation_eps
                )
            local[i, j] = local[j, i] = -2.0 * loc

    total = arch + conductor + pole + local
    total = 0.5 * (total + total.T)

    return frequencies, {
        "archimedean": arch,
        "conductor": conductor,
        "pole": pole,
        "local": local,
        "total": total,
    }


def residual_metrics(components: dict[str, np.ndarray]):
    """Quantify cancellation along the minimum-eigenvalue direction.

    cancellation_ratio = |q_total| / sum_i |q_i|
    residual_amplification = inverse of that ratio.

    Small cancellation_ratio means a small final value is selected from much
    larger signed contributions. This is an observability/numerical-sensitivity
    diagnostic, not evidence for RH.
    """
    total = np.asarray(components["total"], dtype=float)
    evals, evecs = np.linalg.eigh(total)
    v = evecs[:, 0]

    names = ["archimedean", "conductor", "pole", "local"]
    q = {name: float(v @ np.asarray(components[name]) @ v) for name in names}
    q_total = float(evals[0])
    visible_scale = float(sum(abs(x) for x in q.values()))
    if visible_scale == 0.0:
        cancellation_ratio = 0.0
        amplification = math.inf
    else:
        cancellation_ratio = abs(q_total) / visible_scale
        amplification = visible_scale / max(abs(q_total), 1e-300)

    closure_error = abs(q_total - sum(q.values()))
    return {
        **{f"q_{k}": v for k, v in q.items()},
        "q_total": q_total,
        "visible_scale": visible_scale,
        "cancellation_ratio": float(cancellation_ratio),
        "residual_amplification": float(amplification),
        "closure_error": float(closure_error),
    }


def evaluate_case(center: float, kind: str, **kwargs):
    freqs, comp = compression_components(center, kind, **kwargs)
    return freqs, comp, residual_metrics(comp)
