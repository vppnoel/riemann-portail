#!/usr/bin/env python3
"""Finite source-localization rejection demo for V4.1.

1) Synthetic two-source signal with one off-line source.
2) Matched-filter map over (beta,gamma).
3) Morlet-like envelope slope estimates beta-1/2 for the off-line mode.
4) Visibility diagnostics for separated and nearly-colliding sources.

This is deliberately synthetic: it validates the inverse-problem machinery, not RH.
"""
from pathlib import Path
import sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from source_localization import (
    synthetic_source_signal,
    matched_filter_map,
    morlet_demodulated_envelope,
    envelope_growth_rate,
    visibility_metrics,
)

rng = np.random.default_rng(20261004)
t = np.linspace(0.0, 18.0, 900)
true_sources = [(0.5, 14.0), (0.60, 21.0)]
y = synthetic_source_signal(t, true_sources, amplitudes=[1.0, 0.22])
y = y + 0.03 * (rng.normal(size=len(t)) + 1j * rng.normal(size=len(t)))

betas = np.linspace(0.48, 0.64, 17)
gammas = np.linspace(12.0, 23.0, 111)
P = matched_filter_map(y, t, betas, gammas)
flat = np.argsort(P.ravel())[::-1]
rows = []
used = []
for idx in flat:
    i, j = np.unravel_index(idx, P.shape)
    b, g = float(betas[i]), float(gammas[j])
    if all(abs(g-g0) > 0.8 for _, g0 in used):
        rows.append(dict(beta=b, gamma=g, score=float(P[i, j])))
        used.append((b, g))
    if len(rows) == 4:
        break

env = morlet_demodulated_envelope(y, t, gamma=21.0, sigma_t=0.8)
growth = envelope_growth_rate(env, t, trim=0.20)

sep = visibility_metrics(t, [(0.5, 14.0), (0.6, 21.0)])
close = visibility_metrics(t, [(0.5, 14.0), (0.5, 14.2)])

out = pd.DataFrame(rows)
out["estimated_growth_at_gamma21"] = growth
out.to_csv(ROOT / "data" / "source_localization_demo.csv", index=False)
print(out.to_string(index=False))
print("true off-line growth beta-1/2 =", 0.10, "estimated =", round(growth, 4))
print("visibility separated:", sep)
print("visibility close frequencies:", close)
