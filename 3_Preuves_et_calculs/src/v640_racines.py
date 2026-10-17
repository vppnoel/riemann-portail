"""V6.40: independent reconstruction and numerical root recrossing.

The analytic Gauss/minor recipe, rather than decimal text describing the
exported floats, defines the primary function. Binary64 inputs are lifted
exactly for a separate sensitivity check. Nothing is evaluated on import.
Small residuals and agreement between precisions are numerical evidence;
this module does not certify existence, uniqueness or absence of zeros.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import mpmath as mp


CHARACTER_INDICES = (1, 3, 5, 7, 9, 11)
RADIUS_FRACTIONS = {"9/20": (9, 20), "13/20": (13, 20), "3/4": (3, 4)}
PRECISION_PLAN = ((80, "1e-50", "1e-45"), (110, "1e-75", "1e-70"))


def _phases():
    """Reconstruct at the caller's mp precision, with the principal half angle."""
    discrete_logs = {pow(2, j, 13): j for j in range(12)}
    phases, tables = [], []
    for k in CHARACTER_INDICES:
        table = [mp.mpc(0)] + [
            mp.exp(2 * mp.j * mp.pi * mp.mpf(k * discrete_logs[a]) / 12)
            for a in range(1, 13)
        ]
        tau = sum(table[a] * mp.exp(2 * mp.j * mp.pi * mp.mpf(a) / 13)
                  for a in range(1, 13))
        epsilon = tau / (mp.j * mp.sqrt(13))
        real = mp.sqrt((1 + epsilon.real) / 2)
        if not real > 0:
            raise ValueError("The principal half-angle branch is unresolved")
        phases.append(mp.mpc(real, -epsilon.imag / (2 * real)))
        tables.append(table)
    return phases, tables


def reconstruct_pair(pair: dict, digits: int = 110) -> dict:
    """Rebuild the frozen pair solely from its anchor, radius and support.

    Returned mp values retain their construction precision. Arithmetic on
    those values must still be performed within the desired mp.workdps.
    There is no search over supports and no use of zero outcomes.
    """
    if digits < 40:
        raise ValueError("At least 40 decimal working digits are required")
    anchor_k = int(pair["character_k"])
    anchor = CHARACTER_INDICES.index(anchor_k)
    support_k = tuple(int(k) for k in pair["support_character_k"])
    if len(support_k) != 3 or len(set(support_k)) != 3 or anchor_k in support_k:
        raise ValueError("A support must have three distinct non-anchor columns")
    support = tuple(CHARACTER_INDICES.index(k) for k in support_k)
    name = pair["radius"]
    with mp.workdps(digits):
        phases, _ = _phases()
        j, k, ell = support

        def determinant(a, b):
            return (mp.conj(phases[a]) * phases[b]).imag

        u = [mp.mpf(0) for _ in CHARACTER_INDICES]
        u[j], u[k], u[ell] = (determinant(k, ell), determinant(ell, j),
                              determinant(j, k))
        normalizer = mp.sqrt(sum(x * x for x in u))
        if not normalizer > 0:
            raise ValueError("The three-column minor is degenerate")
        u = [x / normalizer for x in u]
        cubic = (phases[anchor] * sum(
            u[n] ** 3 * mp.conj(phases[n]) for n in range(6))).real
        if cubic == 0:
            raise ValueError("The cubic coefficient is numerically zero")
        if cubic < 0:
            u = [-x for x in u]
            cubic = -cubic
        if name == "pi/6":
            radius = mp.pi / 6
            t, sine = mp.sqrt(3) / 2, mp.mpf(1) / 2
        elif name in RADIUS_FRACTIONS:
            numerator, denominator = RADIUS_FRACTIONS[name]
            radius = mp.mpf(numerator) / denominator
            t, sine = mp.cos(radius), mp.sin(radius)
        else:
            raise ValueError("Radius absent from the frozen V6.39 manifest")
        plus, minus = [], []
        for sign, destination in ((1, plus), (-1, minus)):
            destination.extend(sign * sine * x for x in u)
            destination[anchor] = t
        target = t * phases[anchor]
        base = 1 + t * t - 2 * t ** 4
        return {"plus": plus, "minus": minus, "phases": phases,
                "direction": u, "cubic_P": cubic, "radius": radius,
                "target_A": target, "D_plus": base - 2 * t * sine ** 3 * cubic,
                "D_minus": base + 2 * t * sine ** 3 * cubic,
                "digits": digits,
                "kernel_residual": abs(sum(u[n] * phases[n] for n in range(6))),
                "plus_norm_residual": abs(sum(x * x for x in plus) - 1),
                "minus_norm_residual": abs(sum(x * x for x in minus) - 1),
                "plus_A_residual": abs(sum(plus[n] * phases[n] for n in range(6)) - target),
                "minus_A_residual": abs(sum(minus[n] * phases[n] for n in range(6)) - target)}


def periodic_function(coefficients, phases=None):
    """Aggregate six phase-rotated characters into one periodic Dirichlet call.

    Call while inside mp.workdps. Passing a float to mp.mpf preserves its exact
    binary value; converting through str(float) would describe another input.
    """
    rebuilt_phases, tables = _phases()
    if phases is None:
        phases = rebuilt_phases
    if len(coefficients) != 6 or len(phases) != 6:
        raise ValueError("V13 requires six real coordinates and phases")
    coordinates = [mp.mpf(x) for x in coefficients]
    aggregate = [mp.mpc(0) for _ in range(13)]
    for c, phase, table in zip(coordinates, phases, tables):
        for a in range(1, 13):
            aggregate[a] += c * phase * table[a]

    def evaluate(s):
        return mp.dirichlet(s, aggregate)

    evaluate.periodic_table = aggregate
    return evaluate


def locate_direction(coefficients_binary64, ceiling: float,
                     sigma_right: float = 3.0) -> dict:
    """Use the fixed historical EM multistarts, with the V6.40 right edge.

    The helper's q13 function evaluations occur only when this is called.
    """
    path = Path(__file__).resolve().parents[1] / "scripts/run_v637_root_crosscheck.py"
    spec = importlib.util.spec_from_file_location("_v640_historical_em", path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("Historical root-localization module has no loader")
    spec.loader.exec_module(module)
    return module.locate(13, coefficients_binary64, ceiling, sigma_right)


def _root_metrics(evaluate, value, seed, ceiling, sigma_right,
                  residual_limit, partner_limit, digits):
    residual = abs(evaluate(value))
    partner = 1 - mp.conj(value)
    partner_residual = abs(evaluate(partner))

    def prefactor(s):
        return (mp.mpf(13) / mp.pi) ** ((s + 1) / 2) * mp.gamma((s + 1) / 2)

    partner_scaled = partner_residual * abs(prefactor(partner) / prefactor(value))
    gap = abs(value - seed)
    in_tranche = bool(mp.mpf(ceiling) - 1 < abs(value.imag) <= mp.mpf(ceiling))
    off_line = bool(mp.mpf(".500001") < value.real < mp.mpf(sigma_right))
    accepted = bool(residual < mp.mpf(residual_limit)
                    and partner_scaled < mp.mpf(partner_limit)
                    and gap < mp.mpf("1e-7") and in_tranche and off_line)
    return {"mp_digits": digits,
            "beta_mp": mp.nstr(value.real, digits),
            "gamma_mp": mp.nstr(value.imag, digits),
            "residual": mp.nstr(residual, 16),
            "residual_limit": residual_limit,
            "partner_beta": mp.nstr(partner.real, digits),
            "partner_gamma": mp.nstr(partner.imag, digits),
            "partner_residual": mp.nstr(partner_residual, 16),
            "partner_fe_scaled_residual": mp.nstr(partner_scaled, 16),
            "partner_fe_scaled_residual_limit": partner_limit,
            "em_mp_gap": mp.nstr(gap, 16),
            "in_detection_tranche": in_tranche,
            "strictly_off_critical_line": off_line,
            "all_stage_checks_pass": accepted}


def confirm_direction(pair: dict, side: str, coefficients_binary64,
                      located: dict, ceiling: float,
                      sigma_right: float = 3.0) -> dict:
    """Recross an EM candidate for the analytic recipe at 80 and 110 digits.

    Failure is returned explicitly. Precision agreement and a binary-input
    perturbation check never imply a certified digit error or earlier absence.
    """
    if side not in ("plus", "minus"):
        raise ValueError("side must be 'plus' (lower D) or 'minus' (higher D)")
    result = {"side": side, "status": "confirmation_ambiguous", "root_found": False,
              "interval_certification": False, "digit_error_certification": False,
              "absence_below_tranche_certification": False,
              "primary_input": "analytic Gauss/minor recipe from the frozen manifest",
              "binary64_lift": "exact mp.mpf(float), never decimal str(float)",
              "precisions": []}
    if not located.get("found", False):
        result["status"] = "localization_failed"
        return result
    roots = []
    for digits, residual_limit, partner_limit in PRECISION_PLAN:
        try:
            with mp.workdps(digits):
                rebuilt = reconstruct_pair(pair, digits)
                evaluate = periodic_function(rebuilt[side], rebuilt["phases"])
                seed = mp.mpc(str(located["beta"]), str(located["gamma"]))
                value = mp.findroot(evaluate, (seed, seed + mp.mpf(".00001")),
                                    tol=mp.power(10, -(digits - 10)), maxsteps=40)
                stage = _root_metrics(evaluate, value, seed, ceiling, sigma_right,
                                      residual_limit, partner_limit, digits)
                roots.append(value)
                result["precisions"].append(stage)
        except (ValueError, ArithmeticError, RuntimeError) as error:
            result["precisions"].append({"mp_digits": digits,
                "all_stage_checks_pass": False, "error_type": type(error).__name__,
                "error": str(error)[:400]})
    if len(roots) != 2:
        result["status"] = "confirmation_failed"
        return result
    with mp.workdps(110):
        agreement = abs(roots[0] - roots[1])
        result["precision_agreement"] = mp.nstr(agreement, 16)
        result["precision_agreement_limit"] = "1e-30"
        result["precision_agreement_accepted"] = bool(agreement < mp.mpf("1e-30"))
        rebuilt = reconstruct_pair(pair, 110)
        lifted = [mp.mpf(float(x)) for x in coefficients_binary64]
        if len(lifted) != 6:
            raise ValueError("The binary64 sensitivity input must have six coordinates")
        result["maximum_coefficient_input_error"] = mp.nstr(
            max(abs(a - b) for a, b in zip(rebuilt[side], lifted)), 16)
    try:
        with mp.workdps(80):
            rebuilt = reconstruct_pair(pair, 80)
            lifted = [mp.mpf(float(x)) for x in coefficients_binary64]
            evaluate = periodic_function(lifted, rebuilt["phases"])
            seed = mp.mpc(roots[0])
            value = mp.findroot(evaluate, (seed, seed + mp.mpf(".00001")),
                                tol=mp.mpf("1e-70"), maxsteps=40)
            # Root metrics use the EM seed so that the original agreement check
            # has the same meaning as for the primary analytic function.
            em_seed = mp.mpc(str(located["beta"]), str(located["gamma"]))
            sensitivity = _root_metrics(evaluate, value, em_seed, ceiling,
                                       sigma_right, "1e-50", "1e-45", 80)
            shift = abs(value - roots[0])
            sensitivity.update(input_shift=mp.nstr(shift, 16), input_shift_limit="1e-9",
                               input_shift_accepted=bool(shift < mp.mpf("1e-9")))
            result["binary64_sensitivity"] = sensitivity
    except (ValueError, ArithmeticError, RuntimeError) as error:
        result["binary64_sensitivity"] = {"all_stage_checks_pass": False,
            "input_shift_accepted": False, "error_type": type(error).__name__,
            "error": str(error)[:400]}
    accepted = (all(stage["all_stage_checks_pass"] for stage in result["precisions"])
                and result["precision_agreement_accepted"]
                and result["binary64_sensitivity"]["all_stage_checks_pass"]
                and result["binary64_sensitivity"]["input_shift_accepted"])
    result.update(root_found=bool(accepted),
                  status="root_recrossed" if accepted else "confirmation_ambiguous")
    if accepted:
        result["beta_mp"] = result["precisions"][-1]["beta_mp"]
        result["gamma_mp"] = result["precisions"][-1]["gamma_mp"]
    return result
