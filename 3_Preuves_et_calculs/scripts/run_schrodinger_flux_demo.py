#!/usr/bin/env python3
"""Small reproducible V4.2 Schrödinger/flux demo."""
from pathlib import Path
import csv
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from schrodinger_flux import (
    energy_from_zero,
    zero_parameters_from_energy,
    schrodinger_matrix_1d,
    self_adjointness_defect,
    stationary_eigenpairs,
    continuity_source_density,
    norm_growth_rate,
)


def main():
    rows = []
    for beta, gamma in [(0.5, 14.1347251417), (0.60, 21.0)]:
        E = energy_from_zero(beta, gamma)
        b2, g2 = zero_parameters_from_energy(E)
        rows.append({
            "case": f"zero_beta_{beta:.2f}_gamma_{gamma:.3f}",
            "beta": beta,
            "gamma": gamma,
            "E_real": E.real,
            "E_imag": E.imag,
            "norm_growth": norm_growth_rate(beta),
            "roundtrip_beta": b2,
            "roundtrip_gamma": g2,
        })

    x = np.linspace(0.0, 1.0, 220)
    H0, xi = schrodinger_matrix_1d(x, 0.0)
    vals0, vecs0 = stationary_eigenpairs(H0, k=3)
    rows.append({
        "case": "real_box_ground",
        "beta": "",
        "gamma": "",
        "E_real": float(vals0[0].real),
        "E_imag": float(vals0[0].imag),
        "norm_growth": 0.0,
        "roundtrip_beta": "",
        "roundtrip_gamma": "",
    })

    eta = 0.075
    Hc, _ = schrodinger_matrix_1d(x, 1j * eta)
    valsc, vecsc = stationary_eigenpairs(Hc, k=1)
    psi = vecsc[:, 0]
    src = continuity_source_density(psi, 1j * eta)
    # With Euclidean-normalized vector, sum source = 2 eta exactly up to roundoff.
    rows.append({
        "case": "complex_potential_gain",
        "beta": 0.5 + eta,
        "gamma": "",
        "E_real": float(valsc[0].real),
        "E_imag": float(valsc[0].imag),
        "norm_growth": float(np.sum(src)),
        "roundtrip_beta": "",
        "roundtrip_gamma": "",
    })

    out = ROOT / "data" / "schrodinger_flux_demo.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)

    print("self-adjoint defect (real box):", self_adjointness_defect(H0))
    print("lowest real-box energies:", vals0.real)
    print("complex potential Im(E):", valsc[0].imag, "expected", eta)
    print("integrated source on normalized state:", np.sum(src), "expected", 2*eta)
    print("wrote", out)


if __name__ == "__main__":
    main()
