#!/usr/bin/env python3
"""V4.3 finite-dimensional generator/metric demonstration."""
from pathlib import Path
import csv, sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from arithmetic_generator import modal_state_matrix, generator_diagnostics


def one_case(name, modes):
    dt = 0.002
    t = np.arange(0.0, 0.42, dt)
    mix = np.array([[1.0, 0.35+0.10j], [0.20-0.15j, 1.0]], dtype=complex)
    Z = modal_state_matrix(t, modes, mixing=mix)
    d = generator_diagnostics(Z, dt)
    ev = sorted(d["eigenvalues"], key=lambda z: z.real)
    return {
        "case": name,
        "metric_found": int(d["metric_found"]),
        "eig0_real": ev[0].real,
        "eig0_imag": ev[0].imag,
        "eig1_real": ev[1].real,
        "eig1_imag": ev[1].imag,
        "H_metric_defect": d["self_adjointness_defect"],
        "A_metric_defect": d["unitarity_defect"],
        "eigvec_condition": d["eigenvector_condition"],
    }


rows = [
    one_case("RH_like", [(0.5, 14.0), (0.5, 21.0)]),
    one_case("off_line", [(0.5, 14.0), (0.60, 21.0)]),
]
out = ROOT / "data" / "arithmetic_generator_demo.csv"
with out.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader(); w.writerows(rows)
for r in rows:
    print(r)
print("wrote", out)
