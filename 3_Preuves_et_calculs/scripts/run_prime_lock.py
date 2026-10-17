#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve()
SRC = HERE.parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from rejection import build, log_derivative_coeffs
from dark_zeta import (
    interpolation_coeffs_chi_to_dh,
    multiplicative_defect,
    steinhaus_completely_multiplicative,
)
from prime_lock import (
    build_prime_lock,
    prime_lock_metrics_from_coefficients,
    channel_gram,
    gram_effective_rank,
)


def rankdata(x):
    x = np.asarray(x, dtype=float)
    order = np.argsort(x, kind="mergesort")
    ranks = np.empty(len(x), dtype=float)
    i = 0
    while i < len(x):
        j = i + 1
        while j < len(x) and x[order[j]] == x[order[i]]:
            j += 1
        r = 0.5 * (i + j - 1) + 1.0
        ranks[order[i:j]] = r
        i = j
    return ranks


def spearman(x, y):
    rx, ry = rankdata(x), rankdata(y)
    rx -= rx.mean(); ry -= ry.mean()
    den = np.linalg.norm(rx) * np.linalg.norm(ry)
    return float(np.dot(rx, ry) / den) if den else 0.0


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)


def main():
    N = int(os.environ.get("PRIME_LOCK_N", "32768"))
    NLOG = int(os.environ.get("PRIME_LOCK_NLOG", "4096"))
    P = int(os.environ.get("PRIME_LOCK_P", "48"))
    data = HERE.parents[1] / "data"

    summary = []
    for kind in ("zeta", "L_chi5", "DH"):
        a, lam, c, lam_e, c_e, m = build_prime_lock(kind, N=N, n_log=NLOG)
        d = multiplicative_defect(a, P=P)
        G = channel_gram(lam, n_log=NLOG)
        row = {"kind": kind, "N": N, "P": P, **m.to_dict(), **d,
               "channel_gram_effective_rank": gram_effective_rank(G)}
        summary.append(row)
    write_csv(data / "prime_lock_summary.csv", summary)

    scaling = []
    for n in (8192, 16384, 32768):
        for kind in ("zeta", "L_chi5", "DH"):
            a, lam, c, lam_e, c_e, m = build_prime_lock(kind, N=n, n_log=min(NLOG, 4096))
            d = multiplicative_defect(a, P=P)
            scaling.append({"kind": kind, "N": n, **m.to_dict(), **d})
    write_csv(data / "prime_lock_scaling.csv", scaling)

    scan = []
    for theta in np.linspace(0.0, 1.0, 11):
        a = interpolation_coeffs_chi_to_dh(N, float(theta))
        m = prime_lock_metrics_from_coefficients(a, pole=False, n_log=NLOG)
        d = multiplicative_defect(a, P=P)
        scan.append({"theta": float(theta), **m.to_dict(), **d})
    write_csv(data / "prime_lock_chi_dh_scan.csv", scan)

    controls = []
    for seed in range(8):
        a = steinhaus_completely_multiplicative(N, seed=seed)
        m = prime_lock_metrics_from_coefficients(a, pole=False, n_log=NLOG)
        d = multiplicative_defect(a, P=P)
        controls.append({"seed": seed, **m.to_dict(), **d})
    write_csv(data / "prime_lock_steinhaus_controls.csv", controls)

    defect = [r["defect_normalized"] for r in scan]
    corr = {
        "rho_defect_support_leakage": spearman(defect, [r["support_leakage"] for r in scan]),
        "rho_defect_tower_defect": spearman(defect, [r["tower_defect"] for r in scan]),
        "rho_defect_q_residual": spearman(defect, [r["q_residual_ratio"] for r in scan]),
        "rho_defect_coherence": spearman(defect, [r["global_signal_coherence"] for r in scan]),
    }
    with (data / "prime_lock_correlations.json").open("w", encoding="utf-8") as f:
        json.dump(corr, f, indent=2)

    protocol = {
        "version": "V6.2",
        "N": N,
        "n_log": NLOG,
        "P_multiplicative_defect": P,
        "main_objects": ["zeta", "L_chi5", "DH"],
        "chi_to_DH_theta": [float(x) for x in np.linspace(0.0, 1.0, 11)],
        "steinhaus_seeds": list(range(8)),
        "definitions": {
            "support_leakage": "L2 energy fraction of -F'/F coefficients outside prime powers",
            "tower_defect": "degree-1 local Euler tower defect Lambda(p^k)/log p - (Lambda(p)/log p)^k",
            "eulerization": "preserve Lambda(p), impose degree-1 tower on p^k, zero non-prime-powers",
            "q_residual_ratio": "Q(c-c_eulerized)/Q(c)",
            "global_signal_coherence": "absolute normalized inner product of log-grid c signals",
        },
    }
    with (data / "prime_lock_protocol.json").open("w", encoding="utf-8") as f:
        json.dump(protocol, f, indent=2)

    print("PRIME-LOCK complete")
    for row in summary:
        print(row["kind"], "leak=", row["support_leakage"],
              "tower=", row["tower_defect"], "Qres=", row["q_residual_ratio"],
              "coh=", row["global_signal_coherence"])
    print(corr)


if __name__ == "__main__":
    main()
