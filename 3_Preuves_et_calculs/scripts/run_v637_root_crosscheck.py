"""Representative V13 off-line roots: EM localization and mpmath recrossing.

The 24 jobs follow the already frozen V6.37 prediction: both members of the
first pair of each arm/anchor at the median radius. All jobs, including
non-detections, unstable inputs and failed localizations, remain in the output.
No absence claim or certified error of 50 decimal digits is made.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import math
import sys
import time

import mpmath as mp
import numpy as np
from scipy.optimize import root

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "data"
sys.path.insert(0, str(ROOT / "src"))
from euler_archipelago import characters, hurwitz_vec, primitive_root
from v637_apparie import manifest_sha256


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selected_jobs(manifest: dict) -> list[dict]:
    """Select the frozen covariate-only jobs, without reading any outcomes."""
    if manifest.get("sha256") != manifest_sha256(manifest):
        raise ValueError("Selection manifest hash mismatch")
    radii = sorted(manifest["specification"]["radii"])
    median = radii[len(radii) // 2]
    jobs = []
    for arm in ("A1", "D"):
        for anchor in range(manifest["specification"]["dimension"]):
            pairs = sorted((p for p in manifest["pairs"]
                            if p["arm"] == arm and p["anchor"] == anchor
                            and p["radius"] == median), key=lambda p: p["id"])
            if not pairs:
                jobs.append({"id": None, "arm": arm, "anchor": anchor,
                             "radius": median, "status": "missing_selected_pair",
                             "root_found": None})
                continue
            pair = pairs[0]
            for side in ("low", "high"):
                jobs.append({"id": pair[f"{side}_id"], "pair_id": pair["id"],
                             "arm": arm, "anchor": anchor, "radius": median,
                             "side": side, "status": "pending", "root_found": None})
    return jobs


def mp_function(q: int, coefficients):
    """Rebuild phases/characters at current mp.dps and call one mp.dirichlet.

    The six character contributions are aggregated into one length-q periodic
    coefficient table. Coefficients are the manifest float coordinates lifted
    from their decimal representation, not recomputed random directions.
    """
    generator = primitive_root(q)
    logarithms = {pow(generator, j, q): j for j in range(q - 1)}
    coefficient_mp = [mp.mpf(str(float(x))) for x in coefficients]
    aggregate = [mp.mpc(0) for _ in range(q)]
    for coefficient, k in zip(coefficient_mp, range(1, q - 1, 2)):
        table = [mp.mpc(0)] + [mp.exp(2 * mp.j * mp.pi * logarithms[a] * k / (q - 1))
                                 for a in range(1, q)]
        tau = sum(table[a] * mp.exp(2 * mp.j * mp.pi * a / q) for a in range(1, q))
        epsilon = tau / (mp.j * mp.sqrt(q))
        weight = mp.exp(-mp.j * mp.arg(epsilon) / 2)
        for a in range(1, q):
            aggregate[a] += coefficient * weight * table[a]

    def evaluate(s):
        return mp.dirichlet(s, aggregate)

    evaluate.periodic_table = aggregate
    return evaluate


def em_function(q: int, coefficients):
    """Aggregate periodic coefficients once for the double-precision evaluator."""
    chars = characters(q, 1)
    aggregate = np.asarray([
        sum(float(c) * np.exp(-1j * ch["phi"]) * ch["table"][a]
            for c, ch in zip(coefficients, chars)) for a in range(1, q)], dtype=complex)

    def evaluate(s):
        values = np.asarray(s, dtype=complex).reshape(-1)
        h = np.asarray([hurwitz_vec(values, a / q) for a in range(1, q)])
        return np.exp(-values * math.log(q)) * (aggregate @ h)

    return evaluate


def locate(q: int, coefficients, ceiling: float, sigma_right: float = 9.0) -> dict:
    """Find one numerical off-line root in the indicated |t| tranche.

    Fixed multistarts are searched in a fixed order. Returning one root does
    not assert uniqueness, that it is the first true root, or interval accuracy.
    """
    evaluate = em_function(q, coefficients)

    def equations(x):
        if not np.isfinite(x).all() or abs(x[1]) > ceiling + 20 or abs(x[0]) > sigma_right + 10:
            return np.array([1e100, 1e100])
        value = evaluate([x[0] + 1j * x[1]])[0]
        return np.array([value.real, value.imag])

    starts = []
    betas = tuple(b for b in (.53, .6, .8, 1.1, 1.6, 2.5, 4.0, 6.0, 8.0)
                  if b < sigma_right)
    for sign in (1, -1):
        for height in np.linspace(ceiling - .95, ceiling - .05, 7):
            for beta in betas:
                starts.append((beta, sign * height))
    failures = 0
    for attempted, start in enumerate(starts, 1):
        try:
            candidate = root(equations, start, tol=1e-11,
                             options={"maxfev": 120})
            beta, gamma = (float(x) for x in candidate.x)
            residual = float(np.linalg.norm(equations(candidate.x)))
        except (ValueError, FloatingPointError, OverflowError):
            failures += 1
            continue
        if (.500001 < beta < sigma_right
                and ceiling - 1 - 1e-7 < abs(gamma) <= ceiling + 1e-7
                and math.isfinite(residual) and residual < 1e-8):
            return {"found": True, "beta": beta, "gamma": gamma,
                    "residual": residual, "multistarts_attempted": attempted,
                    "multistart_exceptions": failures,
                    "solver_reported_success": bool(candidate.success)}
    return {"found": False, "multistarts_attempted": len(starts),
            "multistart_exceptions": failures,
            "reason": "no accepted off-line EM root in the fixed tranche"}


def confirm(q: int, coefficients, located: dict, ceiling: float,
            sigma_right: float = 9.0, digits: int = 50) -> dict:
    """Compute a high-precision residual and recross the critical partner."""
    with mp.workdps(digits):
        evaluate = mp_function(q, coefficients)
        seed = mp.mpc(str(located["beta"]), str(located["gamma"]))
        value = mp.findroot(evaluate, (seed, seed + mp.mpf(".00001")),
                            tol=mp.mpf("1e-44"), maxsteps=40)
        residual = abs(evaluate(value))
        partner = 1 - mp.conj(value)
        partner_residual = abs(evaluate(partner))
        # Scale the partner's uncompleted residual by its gamma factor relative
        # to the located root. This avoids treating amplification far left as
        # proof that the functional-equation partner failed.
        def prefactor(s):
            return (mp.mpf(q) / mp.pi) ** ((s + 1) / 2) * mp.gamma((s + 1) / 2)

        partner_scaled = partner_residual * abs(prefactor(partner) / prefactor(value))
        gap = abs(complex(value) - complex(located["beta"], located["gamma"]))
        in_tranche = bool(mp.mpf(str(ceiling - 1)) < abs(value.imag)
                          <= mp.mpf(str(ceiling)))
        off_line = bool(value.real > mp.mpf(".50000001")
                        and value.real < mp.mpf(str(sigma_right)))
        root_ok = bool(residual < mp.mpf("1e-40") and gap < 1e-7
                       and in_tranche and off_line)
        partner_ok = bool(partner_scaled < mp.mpf("1e-38"))
        return {"root_found": root_ok, "mp_digits": digits,
                "beta_mp": mp.nstr(value.real, 45),
                "gamma_mp": mp.nstr(value.imag, 45),
                "residual": mp.nstr(residual, 12),
                "em_mp_gap": gap, "in_detection_tranche": in_tranche,
                "strictly_off_critical_line": off_line,
                "partner_beta": mp.nstr(partner.real, 45),
                "partner_gamma": mp.nstr(partner.imag, 45),
                "partner_residual": mp.nstr(partner_residual, 12),
                "partner_fe_scaled_residual": mp.nstr(partner_scaled, 12),
                "partner_residual_accepted": partner_ok,
                "interval_certification": False,
                "digit_error_certification": False,
                "status": "root_recrossed" if root_ok and partner_ok else "confirmation_ambiguous"}


def read_rows(path: Path) -> dict[str, dict]:
    with path.open(newline="", encoding="utf-8") as stream:
        content = list(csv.DictReader(stream))
    rows = {}
    for row in content:
        if row["id"] in rows:
            raise ValueError("Duplicate outcome ID")
        stable_text = row["stable"].strip().lower()
        if stable_text not in ("true", "false", "1", "0"):
            raise ValueError("Cannot parse stable outcome field")
        first_text = row["first_detected"].strip()
        first = float(first_text) if first_text else None
        if first is not None and (not math.isfinite(first) or first <= 0):
            raise ValueError("Invalid first detection")
        rows[row["id"]] = {**row, "stable": stable_text in ("true", "1"),
                            "first_detected": first}
    return rows


def run(selection_path: Path, rows_path: Path, output_path: Path,
        lock_path: Path) -> dict:
    manifest = json.loads(selection_path.read_text(encoding="utf-8"))
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    prediction_path = ROOT.parent / "4_Archives/recus/V637/prevision_v637_apparie.md"
    if (digest(selection_path) != lock["selection_sha256"]
            or digest(prediction_path) != lock["prevision_sha256"]):
        raise ValueError("Selection or prediction changed after locking")
    jobs = selected_jobs(manifest)  # Selected before inspecting outcomes.
    indexed_selection = {row["id"]: row for row in manifest["selection"]}
    indexed_rows = read_rows(rows_path)
    sigma_right = 9.0  # Covariate-only right edge used in the frozen V13 study.
    report = {"q": 13, "parity": 1, "selection_sha256": digest(selection_path),
              "manifest_sha256": manifest["sha256"],
              "prediction_sha256": digest(prediction_path),
              "outcomes_sha256": digest(rows_path), "status": "running",
              "selection_rule": "first pair of each arm/anchor at median radius; both members",
              "mp_digits": 50, "sigma_right": sigma_right,
              "interval_certification": False, "digit_error_certification": False,
              "caveat": "A root in a representative detection tranche is confirmed numerically; neither the first genuine zero nor absence below it is certified.",
              "jobs": jobs}

    def save():
        output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2,
                                         allow_nan=False), encoding="utf-8")

    save()
    started = time.time()
    for job in jobs:
        if job["id"] is None:
            continue
        outcome = indexed_rows.get(job["id"])
        if outcome is None:
            job["status"] = "missing_outcome"
        elif not outcome["stable"]:
            job.update(status="unstable_outcome", first_detected=outcome["first_detected"])
        elif outcome["first_detected"] is None:
            job.update(status="non_detection", first_detected=None,
                       non_detection_ceiling=manifest["specification"]["ceiling"])
        else:
            first = outcome["first_detected"]
            job.update(first_detected=first, detection_tranche=[first - 1, first])
            coefficients = indexed_selection[job["id"]]["coefficients"]
            try:
                located = locate(13, coefficients, first, sigma_right)
                job["em_localization"] = located
                if not located["found"]:
                    job.update(status="localization_failed", root_found=False)
                else:
                    job.update(confirm(13, coefficients, located, first, sigma_right))
            except (ValueError, ArithmeticError, RuntimeError) as error:
                job.update(status="confirmation_failed", root_found=False,
                           error_type=type(error).__name__, error=str(error)[:400])
        print(json.dumps(job, ensure_ascii=False), flush=True)
        save()
    report.update(status="completed", seconds=time.time() - started,
                  n_jobs=len(jobs), n_root_found=sum(job["root_found"] is True for job in jobs),
                  n_recrossed=sum(job["status"] == "root_recrossed" for job in jobs))
    save()
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection", type=Path, default=D / "v637_selection_v13.json")
    parser.add_argument("--rows", type=Path, default=D / "v637_v13.csv")
    parser.add_argument("--lock", type=Path, default=D / "v637_protocole_verrouille.json")
    parser.add_argument("--output", type=Path, default=D / "v637_racines_recoupees.json")
    args = parser.parse_args()
    report = run(args.selection, args.rows, args.output, args.lock)
    print("ROOT CROSSCHECK COMPLETED", report["n_recrossed"], "/", report["n_jobs"], flush=True)


if __name__ == "__main__":
    main()
