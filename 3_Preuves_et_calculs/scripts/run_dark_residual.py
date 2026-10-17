from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dark_residual import evaluate_case

DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)

cases = [
    (86.0, 2.5),
    (113.0, 2.5),
    (167.0, 3.5),
    (176.0, 2.5),
]

rows = []
for center, width in cases:
    for kind in ("DH", "L_pair_chi5"):
        _, _, m = evaluate_case(
            center, kind, half_width=width, dimension=7,
            frequency_step=0.6, arch_dt=0.02, correlation_eps=2e-8,
        )
        rows.append({"center": center, "half_width": width, "kind": kind, **m})

with (DATA / "dark_residual_cases.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

# Precision/discretization sweep at the strongest first witness, deliberately
# varying the Archimedean integration mesh and correlation tolerance.
stability = []
for arch_dt in (0.04, 0.03, 0.02, 0.01):
    for kind in ("DH", "L_pair_chi5"):
        _, _, m = evaluate_case(
            86.0, kind, half_width=2.5, dimension=5,
            frequency_step=0.6, arch_dt=arch_dt, correlation_eps=5e-7,
        )
        stability.append({
            "center": 86.0,
            "half_width": 2.5,
            "dimension": 5,
            "arch_dt": arch_dt,
            "correlation_eps": 5e-7,
            "kind": kind,
            **m,
        })

with (DATA / "dark_residual_stability.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(stability[0].keys()))
    w.writeheader(); w.writerows(stability)

# Compact summary.
summary = {
    "construction_uses_zeros": False,
    "definition": "minimum-eigenvector residual after Archimedean+conductor+pole+local cancellation",
    "cases": rows,
    "stability": stability,
}
(DATA / "dark_residual_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

# Figure: amplification factor for adversarial and matched positive control.
fig, ax = plt.subplots(figsize=(8.5, 5.2))
for kind, marker in (("DH", "o"), ("L_pair_chi5", "s")):
    rr = [r for r in rows if r["kind"] == kind]
    ax.plot([r["center"] for r in rr], [r["residual_amplification"] for r in rr],
            marker=marker, label=kind)
ax.set_yscale("log")
ax.set_xlabel("fréquence centrale T")
ax.set_ylabel("amplification = somme |composantes| / |résidu|")
ax.set_title("RÉSIDU SOMBRE — intensité de la cancellation locale/globale")
ax.legend()
fig.tight_layout()
fig.savefig(DATA / "dark_residual_amplification.png", dpi=180)
plt.close(fig)

print(json.dumps(summary, indent=2))
