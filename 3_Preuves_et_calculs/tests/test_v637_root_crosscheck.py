"""Recrossing checks at nonzero points, without a root finder or zero grid."""
from pathlib import Path
import importlib.util
import json
import sys
from unittest.mock import patch

import mpmath as mp
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from euler_archipelago import F_values, primitive_root

SPEC = importlib.util.spec_from_file_location(
    "v637_root_crosscheck_tested", ROOT / "scripts/run_v637_root_crosscheck.py")
RC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RC)


def manifest():
    return json.loads((ROOT / "data/v637_selection_v13.json").read_text(encoding="utf-8"))


def test_root_jobs_are_the_exact_outcome_independent_locked_subset():
    selection = manifest()
    jobs = RC.selected_jobs(selection)
    assert len(jobs) == 24 and len({j["id"] for j in jobs}) == 24
    assert all(j["radius"] == .65 and j["status"] == "pending" for j in jobs)
    assert all(j["root_found"] is None for j in jobs)
    by_id = {p["id"]: p for p in selection["pairs"]}
    for job in jobs:
        pair = by_id[job["pair_id"]]
        assert pair["id"].endswith("_p00")
        assert job["id"] == pair[f"{job['side']}_id"]
        assert job["anchor"] == pair["anchor"] and job["arm"] == pair["arm"]
    assert sorted((j["arm"], j["anchor"], j["side"]) for j in jobs) == sorted(
        (arm, anchor, side) for arm in ("A1", "D")
        for anchor in range(6) for side in ("low", "high"))


def test_aggregated_em_evaluator_matches_actual_selected_functions():
    selection = manifest()
    by_id = {r["id"]: r["coefficients"] for r in selection["selection"]}
    jobs = RC.selected_jobs(selection)
    s = np.array([2.1 + 3.2j, .8 - 4.7j, 1.1 + 11.2j])
    for arm in ("A1", "D"):
        job = next(j for j in jobs if j["arm"] == arm and j["side"] == "low")
        coefficients = np.asarray(by_id[job["id"]])
        aggregated = RC.em_function(13, coefficients)(s)
        reference = F_values(13, 1, coefficients, s)
        assert np.max(np.abs(aggregated - reference)) < 1e-12


def test_mp_aggregate_is_independent_character_sum_and_one_call_per_evaluation():
    selection = manifest()
    job = RC.selected_jobs(selection)[0]
    coefficients = next(r["coefficients"] for r in selection["selection"] if r["id"] == job["id"])
    with mp.workdps(50):
        s = mp.mpc("2.1", "3.2")
        generator = primitive_root(13)
        logarithms = {pow(generator, j, 13): j for j in range(12)}
        reference = mp.mpc(0)
        for coefficient, k in zip(coefficients, range(1, 12, 2)):
            table = [mp.mpc(0)] + [mp.exp(2 * mp.j * mp.pi * logarithms[a] * k / 12)
                                    for a in range(1, 13)]
            tau = sum(table[a] * mp.exp(2 * mp.j * mp.pi * a / 13) for a in range(1, 13))
            phase = mp.exp(-mp.j * mp.arg(tau / (mp.j * mp.sqrt(13))) / 2)
            reference += mp.mpf(str(float(coefficient))) * phase * mp.dirichlet(s, table)
        evaluate = RC.mp_function(13, coefficients)
        original_dirichlet = mp.dirichlet
        with patch.object(mp, "dirichlet", wraps=original_dirichlet) as counted:
            value = evaluate(s)
            assert counted.call_count == 1
        assert abs(value - reference) < mp.mpf("1e-47")
        partner = 1 - mp.conj(s)
        prefactor = lambda z: (mp.mpf(13) / mp.pi) ** ((z + 1) / 2) * mp.gamma((z + 1) / 2)
        assert abs(prefactor(s) * value
                   - mp.conj(prefactor(partner) * evaluate(partner))) < mp.mpf("1e-46")
