"""Independent checks for the paired design, its scores and censored ordering."""
from pathlib import Path
import copy
import json
import math
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from euler_archipelago import F_values, dirichlet_coefficients
from relief_direct import a1_and_defect
from v637_apparie import (
    analysis, build_selection, compare_detection_rows, detection_interval,
    manifest_sha256, selected_coefficients,
)


def saved_manifest():
    return json.loads((ROOT / "data/v637_selection_v13.json").read_text(encoding="utf-8"))


def residue_scores(c):
    """Original multiplicativity residual definition, not the closed formula."""
    values = dirichlet_coefficients(13, 1, np.asarray(c), 12)
    residues = np.arange(1, 13)
    products = values[(residues[:, None] * residues[None, :]) % 13]
    A = values[residues]
    norm = np.sum(np.abs(A) ** 2)
    residual = values[1] * products - A[:, None] * A[None, :]
    defect = np.sum(np.abs(residual) ** 2) / norm ** 2
    a1 = abs(values[1]) / np.linalg.norm(c)
    return float(a1), float(defect)


def rejected(fn):
    try:
        fn()
    except ValueError:
        return
    raise AssertionError("Invalid data was silently accepted")


def observation(first, stable=True, previous=None):
    row = {"first_detected": first, "stable": stable}
    if previous is not None:
        row["previous_level"] = previous
    return row


def test_frozen_design_reproduces_without_any_zero_data():
    manifest = saved_manifest()
    rebuilt = build_selection()
    # V6.58 : seule la version de NumPy consignée diffère d'un environnement à l'autre ; la sélection doit être identique.
    rebuilt = json.loads(json.dumps(rebuilt)); rebuilt["specification"]["numpy_version"] = manifest["specification"]["numpy_version"]
    assert manifest_sha256(rebuilt) == manifest["sha256"]
    assert rebuilt["candidate_pool_sha256"] == manifest["candidate_pool_sha256"]
    assert len(manifest["selection"]) == 150 and len(manifest["pairs"]) == 72
    assert all(row["complete"] for row in manifest["feasibility"])


def test_actual_pair_geometry_and_calipers_match_residue_scores():
    manifest = saved_manifest()
    ids, C = selected_coefficients(manifest)
    lookup = dict(zip(ids, C))
    scores = {}
    for row in manifest["selection"]:
        c = lookup[row["id"]]
        assert abs(np.linalg.norm(c) - 1) < 1e-13
        assert np.argmax(np.abs(c)) == row["anchor"]
        angle = math.acos(float(np.clip(np.max(np.abs(c)), 0, 1)))
        assert abs(angle - row["radius"]) < 1e-13
        scores[row["id"]] = residue_scores(c)
        assert abs(scores[row["id"]][0] - row["a1"]) < 1e-12
        assert abs(scores[row["id"]][1] - row["D"]) < 1e-12
    used = []
    for pair in manifest["pairs"]:
        lo, hi = scores[pair["low_id"]], scores[pair["high_id"]]
        exposure, nuisance = (0, 1) if pair["arm"] == "A1" else (1, 0)
        assert hi[exposure] - lo[exposure] >= pair["minimum_gap"] - 1e-12
        assert abs(hi[nuisance] - lo[nuisance]) <= pair["caliper"] + 1e-12
        used.extend((pair["low_id"], pair["high_id"]))
    assert len(set(used)) == len(used)


def test_defect_identity_and_scale_invariance_have_independent_witnesses():
    rng = np.random.default_rng(6371391)
    for c in np.r_[np.eye(6), rng.normal(size=(4, 6))]:
        expected = residue_scores(c)
        for factor in (1.0, -3.2):
            a1, D = a1_and_defect(13, 1, factor * c)
            assert abs(a1[0] - expected[0]) < 1e-12
            assert abs(D[0] - expected[1]) < 1e-12
    assert max(residue_scores(c)[1] for c in np.eye(6)) < 1e-25


def test_conjugate_character_permutation_preserves_scores_and_reflects_values():
    c = np.array([.21, -.34, .55, .19, -.62, .31])
    c /= np.linalg.norm(c)
    conjugated = c[::-1]
    assert np.max(np.abs(np.array(residue_scores(c)) - residue_scores(conjugated))) < 1e-12
    s = np.array([1.4 + 2.3j, .8 - 4.7j, 2.1 + 11.8j])
    left = F_values(13, 1, conjugated, s)
    right = F_values(13, 1, c, s.conjugate()).conjugate()
    assert np.max(np.abs(left - right)) < 1e-12


def test_ambiguity_and_nonfinite_data_are_not_reclassified_as_censure():
    assert detection_interval(observation(None, stable=False), 150)["status"] == "unresolved"
    assert detection_interval(observation(None), 150) == {
        "status": "censored", "lower": 150.0, "upper": None}
    assert detection_interval(observation(151), 150)["status"] == "censored"
    assert detection_interval(observation(150), 150)["status"] == "detected"
    for bad in (float("inf"), float("nan"), -1.0, 0.0):
        rejected(lambda bad=bad: detection_interval(observation(bad), 150))
    rejected(lambda: detection_interval(observation(50, previous=50), 150))
    rejected(lambda: detection_interval({"stable": True}, 150))


def test_censored_and_interval_orders_are_distinct_from_true_height_equalities():
    cases = [
        (observation(20), observation(None), "high_later", "ordered_intervals"),
        (observation(None), observation(20), "high_earlier", "ordered_intervals"),
        (observation(None), observation(None), "indeterminate", "two_censures"),
        (observation(20), observation(20), "same_bin", "same_detection_level_not_true_zero_equality"),
        (observation(20), observation(21), "high_later", "ordered_intervals"),
        (observation(20, previous=18), observation(21, previous=19), "indeterminate", "overlapping_intervals"),
        (observation(20), observation(None, stable=False), "indeterminate", "unresolved"),
    ]
    for lo, hi, order, reason in cases:
        result = compare_detection_rows(lo, hi, 150)
        assert result["order"] == order and result["reason"] == reason


def test_partial_outcomes_remain_unresolved_and_ceilings_do_not_impute_heights():
    manifest = saved_manifest()
    pair = next(p for p in manifest["pairs"] if p["arm"] == "A1")
    rows = [dict(id=pair["low_id"], first_detected=80, stable=True),
            dict(id=pair["high_id"], first_detected=None, stable=True)]
    report = analysis(manifest, rows)
    for ceiling_report in report["reports"]:
        comparison = next(c for c in ceiling_report["comparisons"] if c["pair_id"] == pair["id"])
        if ceiling_report["ceiling"] == 50:
            assert comparison["reason"] == "two_censures"
        else:
            assert comparison["order"] == "high_later"
            assert comparison["high_interval"]["upper"] is None
        summary = ceiling_report["arms"]["A1"]
        assert summary["indeterminate_reasons"]["unresolved"] == 35
    assert len(report["missing_outcome_ids"]) == 148


def test_manifest_integrity_and_outcome_identity_reject_wrong_data():
    manifest = saved_manifest()
    altered = copy.deepcopy(manifest)
    altered["selection"][7]["coefficients"][0] += 1e-5
    assert manifest_sha256(altered) != manifest["sha256"]
    rejected(lambda: selected_coefficients(altered))
    rejected(lambda: analysis(altered, []))
    unknown = [dict(id="unknown", stable=True, first_detected=None)]
    rejected(lambda: analysis(manifest, unknown))
    duplicate = dict(id=manifest["selection"][0]["id"], stable=True, first_detected=None)
    rejected(lambda: analysis(manifest, [duplicate, duplicate]))
