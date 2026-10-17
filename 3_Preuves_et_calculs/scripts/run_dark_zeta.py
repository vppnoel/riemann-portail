#!/usr/bin/env python3
"""Run V6 DARK-ZETA / TOMO detector battery and write reproducible outputs."""
from __future__ import annotations

from pathlib import Path
import sys
import json
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dark_zeta import (
    build_signal,
    phase_randomize_preserve_power,
    tomo2_gram,
    tomo2_metrics,
    tomo3_bicoherence,
    multiplicative_defect,
    interpolation_coeffs_chi_to_dh,
    c_from_coefficients,
    signal_from_c,
    steinhaus_completely_multiplicative,
)

OUT = ROOT / "data"
OUT.mkdir(parents=True, exist_ok=True)

N = 32768
NLOG = 4096
PDEF = 48
NSHIFT = 32
SHIFT_STEP = 8
SEG_LEN = 512
HOP = 256
MAX_BIN = 24


def row_for(name, a, g):
    K = tomo2_gram(g, n_shifts=NSHIFT, shift_step=SHIFT_STEP)
    m2 = tomo2_metrics(K)
    rec, _X, m3 = tomo3_bicoherence(g, seg_len=SEG_LEN, hop=HOP, max_bin=MAX_BIN)
    d = multiplicative_defect(a, P=PDEF) if a is not None else {
        "defect_mse": np.nan, "defect_normalized": np.nan,
        "defect_max": np.nan, "defect_pairs": np.nan,
    }
    return {
        "object": name,
        **d,
        "tomo2_entropy": m2.entropy,
        "tomo2_effective_rank": m2.effective_rank,
        "tomo2_top_eigen_fraction": m2.top_eigen_fraction,
        "tomo2_condition_positive": m2.condition_number_positive,
        "tomo3_mean_bicoherence": m3.mean_bicoherence,
        "tomo3_median_bicoherence": m3.median_bicoherence,
        "tomo3_q90_bicoherence": m3.q90_bicoherence,
        "tomo3_max_bicoherence": m3.max_bicoherence,
        "tomo3_mean_bispectrum_amplitude": m3.mean_bispectrum_amplitude,
        "tomo3_n_triads": m3.n_triads,
        "tomo3_n_segments": m3.n_segments,
    }, K, rec


# Core objects
core = {}
rows = []
for kind in ["zeta", "L_chi5", "DH"]:
    a, c, u, g = build_signal(kind, N=N, n_log=NLOG)
    r, K, rec = row_for(kind, a, g)
    rows.append(r)
    core[kind] = (a, c, u, g, K, rec)

# Phase-randomization controls. TOMO-2 must be invariant exactly (circular Gram).
# TOMO-3 is calibrated against 32 surrogates per core object to expose the finite-segment null bias.
pr_rows = []
SURR = 32
for kind in ["zeta", "L_chi5", "DH"]:
    a0, c0, u0, g0, K0, _ = core[kind]
    for seed in range(SURR):
        gr = phase_randomize_preserve_power(g0, seed=1000 * (["zeta","L_chi5","DH"].index(kind)+1) + seed)
        Kpr = tomo2_gram(gr, n_shifts=NSHIFT, shift_step=SHIFT_STEP)
        _, _, m3pr = tomo3_bicoherence(gr, seg_len=SEG_LEN, hop=HOP, max_bin=MAX_BIN)
        pr_rows.append({
            "object": kind,
            "seed": seed,
            "tomo2_max_abs_diff": float(np.max(np.abs(Kpr - K0))),
            "tomo3_mean_bicoherence": m3pr.mean_bicoherence,
            "tomo3_median_bicoherence": m3pr.median_bicoherence,
            "tomo3_q90_bicoherence": m3pr.q90_bicoherence,
            "tomo3_max_bicoherence": m3pr.max_bicoherence,
        })

# Random completely multiplicative controls: multiplicative without functional equation.
stei_rows = []
for seed in range(4):
    a = steinhaus_completely_multiplicative(N, seed=seed)
    c = c_from_coefficients(a, pole=False)
    _u, g = signal_from_c(c, n_log=NLOG, t_max=N)
    r, _K, _rec = row_for(f"steinhaus_{seed}", a, g)
    stei_rows.append(r)
    rows.append(r)

# Controlled path from chi_5 to DH.
scan = []
for theta in np.linspace(0.0, 1.0, 11):
    a = interpolation_coeffs_chi_to_dh(N, float(theta))
    c = c_from_coefficients(a, pole=False)
    _u, g = signal_from_c(c, n_log=NLOG, t_max=N)
    r, _K, _rec = row_for(f"mix_{theta:.1f}", a, g)
    r["theta"] = float(theta)
    scan.append(r)

main_df = pd.DataFrame(rows)
pr_df = pd.DataFrame(pr_rows)
scan_df = pd.DataFrame(scan)
stei_df = pd.DataFrame(stei_rows)

# Surrogate calibration of TOMO-3. Under phase randomization with finitely many segments,
# the squared-bicoherence null is not centered at zero; compare observed values to this null.
cal_rows = []
for kind in ["zeta", "L_chi5", "DH"]:
    obs = main_df.loc[main_df.object == kind].iloc[0]
    sub = pr_df[pr_df.object == kind]
    for metric in ["tomo3_mean_bicoherence", "tomo3_median_bicoherence", "tomo3_q90_bicoherence", "tomo3_max_bicoherence"]:
        vals = sub[metric].to_numpy(float)
        mu = float(np.mean(vals)); sd = float(np.std(vals, ddof=1))
        ov = float(obs[metric])
        z = (ov - mu) / sd if sd > 0 else np.nan
        pct = float((np.sum(vals <= ov) + 1) / (len(vals) + 1))
        cal_rows.append({"object":kind,"metric":metric,"observed":ov,"surrogate_mean":mu,"surrogate_sd":sd,"z_score":z,"empirical_percentile":pct,"n_surrogates":len(vals)})
cal_df = pd.DataFrame(cal_rows)

main_df.to_csv(OUT / "dark_zeta_detector_summary.csv", index=False)
pr_df.to_csv(OUT / "dark_zeta_phase_random_controls.csv", index=False)
cal_df.to_csv(OUT / "dark_zeta_tomo3_surrogate_calibration.csv", index=False)
scan_df.to_csv(OUT / "dark_zeta_chi_dh_scan.csv", index=False)
stei_df.to_csv(OUT / "dark_zeta_steinhaus_controls.csv", index=False)

# Save detailed TOMO-3 triads for core pair L_chi5 vs DH and zeta.
for kind in ["zeta", "L_chi5", "DH"]:
    rec = core[kind][5]
    pd.DataFrame(rec, columns=["k", "l", "k_plus_l", "bicoherence_sq", "bispectrum_abs"]).to_csv(
        OUT / f"dark_zeta_tomo3_triads_{kind}.csv", index=False
    )

# Correlation diagnostics along the controlled nonmultiplicative path.
x = scan_df["defect_normalized"].to_numpy(float)
metrics = ["tomo2_entropy", "tomo3_mean_bicoherence", "tomo3_q90_bicoherence"]
corr = []
for col in metrics:
    y = scan_df[col].to_numpy(float)
    pr = pearsonr(x, y)
    sr = spearmanr(x, y)
    corr.append({
        "metric": col,
        "pearson_r": float(pr.statistic),
        "pearson_p": float(pr.pvalue),
        "spearman_rho": float(sr.statistic),
        "spearman_p": float(sr.pvalue),
    })
pd.DataFrame(corr).to_csv(OUT / "dark_zeta_defect_correlations.csv", index=False)

# Machine-readable protocol metadata.
meta = {
    "N": N,
    "n_log": NLOG,
    "multiplicative_defect_P": PDEF,
    "tomo2_n_shifts": NSHIFT,
    "tomo2_shift_step": SHIFT_STEP,
    "tomo3_segment_length": SEG_LEN,
    "tomo3_hop": HOP,
    "tomo3_max_bin": MAX_BIN,
    "phase_random_surrogates_per_core_object": SURR,
    "steinhaus_seeds": 4,
    "chi_to_DH_theta_grid": [float(x) for x in np.linspace(0.0, 1.0, 11)],
}
(OUT / "dark_zeta_protocol.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

print("=== DARK-ZETA core summary ===")
print(main_df.to_string(index=False))
print("\n=== TOMO-3 surrogate calibration ===")
print(cal_df.to_string(index=False))
print("\n=== TOMO-2 phase-random invariant max error ===")
print(pr_df.groupby("object")["tomo2_max_abs_diff"].max().to_string())
print("\n=== chi -> DH scan ===")
print(scan_df[["theta","defect_normalized","tomo2_entropy","tomo3_mean_bicoherence","tomo3_q90_bicoherence"]].to_string(index=False))
print("\n=== Correlations ===")
print(pd.DataFrame(corr).to_string(index=False))
