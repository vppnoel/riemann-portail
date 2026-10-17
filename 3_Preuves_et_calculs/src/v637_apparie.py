"""V6.37: covariate-only selection and censored paired comparisons in V_13.

No zero finder or zero cache is used by this module. Save ``build_selection()``
and its hash before supplying outcomes to ``analysis``. The optimized finite
design supports descriptive comparisons, not causal or population inference.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from typing import Iterable, Mapping

import numpy as np

from euler_archipelago import characters
from relief_direct import a1_and_defect


@dataclass(frozen=True)
class SelectionConfig:
    q: int = 13
    parity: int = 1
    seed: int = 6371301
    radii: tuple[float, ...] = (0.45, 0.65, 0.75)
    candidates_per_stratum: int = 512
    pairs_per_arm_stratum: int = 2
    a1_caliper_D: float = 0.04
    a1_minimum_gap: float = 0.20
    D_caliper_a1: float = 0.03
    D_minimum_gap: float = 0.25
    ceiling: int = 150
    reporting_ceilings: tuple[int, ...] = (50, 100, 150)


def canonical_bytes(value: Mapping) -> bytes:
    """Canonical UTF-8 JSON, rejecting NaN/Infinity and excluding top hash."""
    content = {k: v for k, v in value.items() if k != "sha256"}
    return json.dumps(content, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def manifest_sha256(manifest: Mapping) -> str:
    return hashlib.sha256(canonical_bytes(manifest)).hexdigest()


def _validate_config(cfg: SelectionConfig) -> int:
    if cfg.q != 13 or cfg.parity != 1:
        raise ValueError("This prespecified design is restricted to odd V_13")
    d = len(characters(cfg.q, cfg.parity))
    if d != 6:
        raise ValueError("Expected six character coordinates in odd V_13")
    if not cfg.radii or any(not 0 < x < math.pi / 4 for x in cfg.radii):
        raise ValueError("Each projective radius must lie strictly between 0 and pi/4")
    if len(set(cfg.radii)) != len(cfg.radii):
        raise ValueError("Duplicate radii are not allowed")
    if cfg.candidates_per_stratum < 2 or cfg.pairs_per_arm_stratum < 1:
        raise ValueError("Positive candidate and pair counts are required")
    if min(cfg.a1_caliper_D, cfg.a1_minimum_gap,
           cfg.D_caliper_a1, cfg.D_minimum_gap) <= 0:
        raise ValueError("All calipers and gaps must be positive")
    if cfg.ceiling < 1 or any(t < 1 or t > cfg.ceiling
                             for t in cfg.reporting_ceilings):
        raise ValueError("Reporting ceilings must belong to [1, ceiling]")
    return d


def _rank_pairs(values: np.ndarray, nuisance: np.ndarray,
                minimum_gap: float, caliper: float):
    """Rank eligible edges by largest exposure contrast, then closest match."""
    i, j = np.triu_indices(len(values), 1)
    gap = np.abs(values[j] - values[i])
    mismatch = np.abs(nuisance[j] - nuisance[i])
    valid = (gap >= minimum_gap) & (mismatch <= caliper)
    i, j, gap, mismatch = i[valid], j[valid], gap[valid], mismatch[valid]
    order = np.lexsort((j, i, mismatch, -gap))
    return i[order], j[order], gap[order], mismatch[order]


def build_selection(config: SelectionConfig | None = None) -> dict:
    """Return a deterministic, outcome-blind manifest ready to freeze on disk.

    Each candidate is cos(radius)*e_anchor + sin(radius)*u with unit u
    orthogonal to e_anchor. Hence its projective distance to its unique nearest
    Euler axis is exactly radius. Pairs have identical anchor and radius.
    Candidates are never reused, including between the two arms.
    """
    cfg = config or SelectionConfig()
    d = _validate_config(cfg)
    chars = characters(cfg.q, cfg.parity)
    specification = asdict(cfg)
    specification.update({
        "version": "V6.37",
        "dimension": d,
        "character_indices": [ch["k"] for ch in chars],
        "character_phases": [float(ch["phi"]) for ch in chars],
        "numpy_version": np.__version__,
        "generator": "numpy.PCG64(SeedSequence([seed, anchor, radius_index]))",
        "candidate_rule": "cos(radius)*e_anchor + sin(radius)*unit_Gaussian_in_anchor_perp",
        "radius_definition": "arccos(max(abs(coordinates))); angle, not its sine",
        "selection_rule": "descending exposure gap, ascending nuisance gap, ascending candidate indices",
        "arm_order": ["A1", "D"],
        "disjoint_rule": "no candidate reused within or between arms",
        "missing_rule": "retain infeasible strata; no post-outcome threshold relaxation",
        "A1_prediction": "higher a1 has later first numerical detection",
        "D_prediction": "no stable residual direction is predicted; report both signs by stratum",
        "D_diagnostic_sign": "higher D has earlier detection (descriptive directional diagnostic)",
        "outcome": "first positive total-minus-critical numerical count at integer levels",
        "censoring": "no detection up to ceiling; never replaced by ceiling+1",
        "status": "selection frozen before zero counting",
        "inference": "optimized finite design; descriptive, no confirmatory p-value or causal claim",
    })
    selection, pairs, feasibility = [], [], []
    for anchor in range(d):
        c = np.eye(d)[anchor]
        a1, defect = a1_and_defect(cfg.q, cfg.parity, c)
        selection.append({"id": f"euler_{anchor:02d}", "coefficients": c.tolist(),
                          "euler": True, "anchor": anchor, "radius": 0.0,
                          "arm": "control", "a1": float(a1[0]), "D": float(defect[0])})
    pool_hash = hashlib.sha256()
    for anchor in range(d):
        for rindex, radius in enumerate(cfg.radii):
            rng = np.random.Generator(np.random.PCG64(
                np.random.SeedSequence([cfg.seed, anchor, rindex])))
            u = rng.standard_normal((cfg.candidates_per_stratum, d))
            u[:, anchor] = 0.0
            lengths = np.linalg.norm(u, axis=1)
            if np.any(lengths == 0):
                raise RuntimeError("A zero tangent candidate must not be silently resampled")
            u /= lengths[:, None]
            C = math.sin(radius) * u
            C[:, anchor] = math.cos(radius)
            if not np.all(np.argmax(np.abs(C), axis=1) == anchor):
                raise AssertionError("Generated candidates lost their prescribed anchor")
            pool_hash.update(np.asarray(C, dtype="<f8").tobytes(order="C"))
            a1, defect = a1_and_defect(cfg.q, cfg.parity, C)
            used = set()
            for arm, exposure, nuisance, gap_min, caliper in (
                ("A1", a1, defect, cfg.a1_minimum_gap, cfg.a1_caliper_D),
                ("D", defect, a1, cfg.D_minimum_gap, cfg.D_caliper_a1),
            ):
                ii, jj, gaps, mismatches = _rank_pairs(exposure, nuisance, gap_min, caliper)
                taken = 0
                for i, j, gap, mismatch in zip(ii, jj, gaps, mismatches):
                    i, j = int(i), int(j)
                    if i in used or j in used:
                        continue
                    low, high = (i, j) if exposure[i] < exposure[j] else (j, i)
                    ids = []
                    for candidate in (low, high):
                        pid = f"a{anchor:02d}_r{rindex:02d}_c{candidate:05d}"
                        ids.append(pid)
                        selection.append({"id": pid, "coefficients": C[candidate].tolist(),
                                          "euler": False, "anchor": anchor, "radius": radius,
                                          "arm": arm, "candidate": candidate,
                                          "a1": float(a1[candidate]), "D": float(defect[candidate])})
                    pairs.append({"id": f"{arm}_a{anchor:02d}_r{rindex:02d}_p{taken:02d}",
                                  "arm": arm, "low_id": ids[0], "high_id": ids[1],
                                  "anchor": anchor, "radius": radius,
                                  "exposure": "a1" if arm == "A1" else "D",
                                  "nuisance": "D" if arm == "A1" else "a1",
                                  "gap": float(gap), "nuisance_gap": float(mismatch),
                                  "minimum_gap": gap_min, "caliper": caliper})
                    used.update((i, j))
                    taken += 1
                    if taken == cfg.pairs_per_arm_stratum:
                        break
                feasibility.append({"arm": arm, "anchor": anchor, "radius": radius,
                                    "eligible_edges_before_disjoint_selection": len(ii),
                                    "requested_pairs": cfg.pairs_per_arm_stratum,
                                    "selected_pairs": taken,
                                    "missing_pairs": cfg.pairs_per_arm_stratum - taken,
                                    "complete": taken == cfg.pairs_per_arm_stratum})
    manifest = {"specification": specification, "selection": selection,
                "pairs": pairs, "feasibility": feasibility,
                "candidate_pool_sha256": pool_hash.hexdigest()}
    manifest["sha256"] = manifest_sha256(manifest)
    return manifest


def selected_coefficients(manifest: Mapping) -> tuple[list[str], np.ndarray]:
    """Return IDs and coefficients in manifest order, including Euler controls."""
    if manifest.get("sha256") != manifest_sha256(manifest):
        raise ValueError("Selection manifest hash mismatch")
    return ([row["id"] for row in manifest["selection"]],
            np.asarray([row["coefficients"] for row in manifest["selection"]], dtype=float))


def detection_interval(row: Mapping, ceiling: float) -> dict:
    """Translate a stable first-detection row to an interval at a fixed ceiling.

    Required fields: id; first_detected (None for no detection at study ceiling).
    ``stable`` must be explicitly True. An optional ``previous_level`` supplies
    the lower endpoint (otherwise integer first_detected-1). These are numerical
    instrument intervals, not certified locations of the first genuine zero.
    """
    if row.get("stable") is not True:
        return {"status": "unresolved", "lower": None, "upper": None}
    if "first_detected" not in row:
        raise ValueError("Stable observation is missing first_detected")
    first = row["first_detected"]
    if first is None:
        return {"status": "censored", "lower": float(ceiling), "upper": None}
    first = float(first)
    if not math.isfinite(first) or first <= 0:
        raise ValueError("Detected level must be finite and strictly positive")
    if first > ceiling:
        return {"status": "censored", "lower": float(ceiling), "upper": None}
    lower = float(row.get("previous_level", max(0.0, first - 1.0)))
    if not math.isfinite(lower) or not 0 <= lower < first:
        raise ValueError("Invalid lower endpoint for first detection")
    return {"status": "detected", "lower": lower, "upper": first}


def compare_detection_rows(low: Mapping, high: Mapping, ceiling: float) -> dict:
    """Classify high-vs-low detection order without assigning censored heights."""
    lo, hi = detection_interval(low, ceiling), detection_interval(high, ceiling)
    if "unresolved" in (lo["status"], hi["status"]):
        order, reason = "indeterminate", "unresolved"
    elif lo["status"] == hi["status"] == "censored":
        order, reason = "indeterminate", "two_censures"
    elif lo["upper"] is not None and hi["lower"] >= lo["upper"]:
        order, reason = "high_later", "ordered_intervals"
    elif hi["upper"] is not None and lo["lower"] >= hi["upper"]:
        order, reason = "high_earlier", "ordered_intervals"
    elif lo["status"] == hi["status"] == "detected" and lo["upper"] == hi["upper"]:
        order, reason = "same_bin", "same_detection_level_not_true_zero_equality"
    else:
        order, reason = "indeterminate", "overlapping_intervals"
    return {"order": order, "reason": reason, "low_interval": lo, "high_interval": hi}


def _summarize(comparisons: list[dict], arm: str) -> dict:
    n = len(comparisons)
    counts = {name: sum(row["order"] == name for row in comparisons)
              for name in ("high_later", "high_earlier", "same_bin", "indeterminate")}
    reasons = {name: sum(row["reason"] == name for row in comparisons)
               for name in ("unresolved", "two_censures", "overlapping_intervals")}
    favorable = counts["high_later"] if arm == "A1" else counts["high_earlier"]
    contrary = counts["high_earlier"] if arm == "A1" else counts["high_later"]
    ordered = favorable + contrary
    uncertain = counts["same_bin"] + counts["indeterminate"]
    return {"pairs": n, **counts, "indeterminate_reasons": reasons,
            "diagnostic_favorable_sign": "high_later" if arm == "A1" else "high_earlier",
            "favorable": favorable, "contrary": contrary, "ordered": ordered,
            "favorable_fraction_among_ordered": favorable / ordered if ordered else None,
            "favorable_fraction_bounds_all_pairs":
                [favorable / n, (favorable + uncertain) / n] if n else None,
            "bound_meaning": "possible strict interval order; same-bin and unresolved orders unknown",
            "inference": "descriptive selected-design comparison; no confirmatory p-value"}


def analysis(manifest: Mapping, rows: Iterable[Mapping],
             ceilings: Iterable[float] | None = None) -> dict:
    """Analyze frozen pairs at preset ceilings; retain all missing/unclear pairs.

    ``rows`` are dictionaries {id, first_detected, stable, previous_level?}.
    A missing row is unresolved. Neither non-detection nor a missing row is
    given a fabricated numeric height. The D arm reports its directional
    diagnostic and all signs by anchor/radius, without inferring 'no effect'
    from a pooled rate near one half.
    """
    if manifest.get("sha256") != manifest_sha256(manifest):
        raise ValueError("Selection manifest changed after it was frozen")
    row_list = list(rows)
    indexed = {row["id"]: row for row in row_list}
    if len(indexed) != len(row_list):
        raise ValueError("Duplicate outcome IDs")
    allowed_ids = {row["id"] for row in manifest["selection"]}
    if set(indexed) - allowed_ids:
        raise ValueError("Outcome ID absent from frozen selection")
    if ceilings is None:
        ceilings = manifest["specification"]["reporting_ceilings"]
    ceiling_list = [float(t) for t in ceilings]
    study_ceiling = manifest["specification"]["ceiling"]
    if any(not 0 < t <= study_ceiling for t in ceiling_list):
        raise ValueError("Analysis ceiling exceeds the frozen study ceiling")
    reports = []
    for ceiling in ceiling_list:
        comparisons = []
        for pair in manifest["pairs"]:
            low = indexed.get(pair["low_id"], {"stable": False})
            high = indexed.get(pair["high_id"], {"stable": False})
            comparison = compare_detection_rows(low, high, ceiling)
            comparisons.append({"pair_id": pair["id"], "arm": pair["arm"],
                                "anchor": pair["anchor"], "radius": pair["radius"],
                                **comparison})
        arms = {arm: _summarize([c for c in comparisons if c["arm"] == arm], arm)
                for arm in ("A1", "D")}
        strata = []
        for design_stratum in manifest["feasibility"]:
            group = [c for c in comparisons if c["arm"] == design_stratum["arm"]
                     and c["anchor"] == design_stratum["anchor"]
                     and c["radius"] == design_stratum["radius"]]
            strata.append({**design_stratum,
                           "outcomes": _summarize(group, design_stratum["arm"])})
        reports.append({"ceiling": ceiling, "arms": arms, "strata": strata,
                        "comparisons": comparisons})
    return {"selection_sha256": manifest["sha256"],
            "missing_outcome_ids": sorted(allowed_ids - set(indexed)),
            "reports": reports,
            "caveat": "Numerical detection intervals and non-detections are not certified first-zero intervals or zero-free regions."}
