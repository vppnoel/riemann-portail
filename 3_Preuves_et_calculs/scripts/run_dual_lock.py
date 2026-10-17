from __future__ import annotations

import csv, json, math, sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dual_lock import (
    compression_accurate, matrix_metrics, scan_centers, negative_intervals,
    load_offline_dh_zeros, nearest_interval_match,
)

DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)

protocol = {
    "version": "V6.3",
    "construction_uses_zeros": False,
    "basis": "f_j(x)=(1-|x|/w)_+ cos(xi_j x)",
    "dimension": 7,
    "frequency_step": 0.6,
    "screen_centers": [0, 200, 1],
    "apertures": [2.5, 3.5],
    "negative_screen_threshold": -1e-5,
    "positive_control": "average explicit form of chi mod 5 and conjugate chi",
    "adversarial_target": "Davenport-Heilbronn",
    "posthoc_zero_file": "dh_zeros.csv",
    "note": "Zeros are used only after the arithmetic/archimedean scan for validation.",
}
(DATA / "dual_lock_protocol.json").write_text(json.dumps(protocol, indent=2), encoding="utf-8")

centers = np.arange(0.0, 201.0, 1.0)
all_rows = []
all_intervals = []
for width in (2.5, 3.5):
    rows = scan_centers(centers, "DH", half_width=width,
                        dimension=7, frequency_step=0.6)
    all_rows.extend(rows)
    all_intervals.extend(negative_intervals(rows, threshold=-1e-5))

with (DATA / "dual_lock_scan_DH.csv").open("w", newline="") as f:
    cols = list(all_rows[0].keys())
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(all_rows)

# Post-hoc only: compare screen intervals with independently computed DH zeros.
offline = load_offline_dh_zeros(DATA / "dh_zeros.csv", tmax=200.0)
matched = [nearest_interval_match(it, offline) for it in all_intervals]
with (DATA / "dual_lock_negative_intervals.csv").open("w", newline="") as f:
    cols = list(matched[0].keys()) if matched else ["start","end"]
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(matched)

# Merge overlapping negative intervals across apertures, then choose the smallest
# aperture that already gives a robust screen witness.  This selection rule uses
# only the arithmetic/archimedean scan, not the post-hoc zero file.
intervals_sorted = sorted(all_intervals, key=lambda r: (float(r["start"]), float(r["end"])))
clusters = []
for it in intervals_sorted:
    if not clusters or float(it["start"]) > max(float(x["end"]) for x in clusters[-1]) + 2.0:
        clusters.append([it])
    else:
        clusters[-1].append(it)

selected = []
for group in clusters:
    robust = [it for it in group if float(it["best_lambda_min_fast"]) < -1e-3]
    pool = robust if robust else group
    # smallest support first; within the same support choose strongest screen witness
    pool = sorted(pool, key=lambda it: (float(it["half_width"]), float(it["best_lambda_min_fast"])))
    selected.append(pool[0])

confirm_rows = []
for it in selected:
    c = float(it["best_center"])
    width = float(it["half_width"])
    for kind in ("DH", "L_pair_chi5"):
        _, M = compression_accurate(c, kind, half_width=width,
                                    dimension=7, frequency_step=0.6,
                                    correlation_eps=3e-7)
        confirm_rows.append({
            "center": c, "half_width": width, "kind": kind,
            **matrix_metrics(M),
        })

with (DATA / "dual_lock_confirmed.csv").open("w", newline="") as f:
    cols = list(confirm_rows[0].keys())
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(confirm_rows)

# Plot both aperture scans.
fig, ax = plt.subplots(figsize=(10, 5.5))
for width in (2.5, 3.5):
    rr = [r for r in all_rows if abs(float(r["half_width"]) - width) < 1e-12]
    ax.plot([r["center"] for r in rr], [r["lambda_min"] for r in rr],
            label=f"DH, demi-largeur {width}")
ax.axhline(0.0, linewidth=1)
for sigma, t in offline:
    ax.axvline(t, linewidth=0.7, alpha=0.25)
ax.set_xlabel("fréquence centrale T")
ax.set_ylabel("plus petite valeur propre (screening)")
ax.set_title("DUAL-LOCK — compression de Weil calculée sans les zéros")
ax.legend()
fig.tight_layout()
fig.savefig(DATA / "dual_lock_scan.png", dpi=180)
plt.close(fig)

# Compact summary JSON.
summary = {
    "offline_DH_zeros_posthoc": [{"sigma": s, "t": t} for s, t in offline],
    "screen_negative_intervals": matched,
    "accurate_confirmations": confirm_rows,
    "n_screen_rows": len(all_rows),
}
(DATA / "dual_lock_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print(json.dumps(summary, indent=2))
