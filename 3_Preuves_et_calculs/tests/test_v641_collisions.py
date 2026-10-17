"""Derivative correctness, exact-input reuse and local operator limitations."""
from pathlib import Path
import json
import mpmath as mp

from v640_racines import periodic_function, reconstruct_pair
from v641_collisions import make_family, periodic_jet, companion_form, operator_certificate


def _pair():
    return json.loads((Path(__file__).resolve().parents[1]
                       / "data/v639_couples_fixes.json").read_text())["pairs"][0]


def test_hurwitz_second_derivative_is_really_a_second_derivative():
    # An independent closed formula avoids dirichlet(...,derivative=2), which
    # is outside mpmath 1.3.0's implemented derivative contract.
    with mp.workdps(60):
        s = mp.mpc(".7", "2.3")
        eta = lambda z: (1 - mp.power(2, 1 - z)) * mp.zeta(z)
        values = periodic_jet([-1, 1], s, 2)
        for n, value in enumerate(values):
            assert abs(value - mp.diff(eta, s, n)) < mp.mpf("1e-52")
        assert abs(values[2] - values[0]) > mp.mpf(".001")


def test_family_reuses_the_frozen_analytic_input_not_exported_floats():
    pair = _pair()
    with mp.workdps(70):
        rebuilt = reconstruct_pair(pair, 70)
        s = mp.mpc("1.7", "3.2")
        for side in ("plus", "minus"):
            family = make_family(pair, side, 70)
            direct = periodic_function(rebuilt[side], rebuilt["phases"])
            assert abs(family.evaluate(s, rebuilt["radius"]) - direct(s)) < mp.mpf("1e-62")


def test_phase_derivatives_and_completion_give_the_same_zero_geometry():
    pair = _pair()
    with mp.workdps(65):
        r, t = mp.mpf(".21"), mp.mpf("-3.4")
        hardy = make_family(pair, "plus", 65)
        completed = make_family(pair, "plus", 65, normalization="completed")
        jets = hardy.jet(r, t)
        assert jets["reality_defect"] < mp.mpf("1e-58")
        for name, order in (("Z", 0), ("Z_t", 1), ("Z_tt", 2)):
            independently = mp.diff(lambda x: hardy.completed(x, r), t, order)
            assert abs(jets[name] - independently) < mp.mpf("1e-55")
        assert abs(jets["Z_r"] - mp.diff(lambda x: hardy.critical(x, t), r)) < mp.mpf("1e-55")
        assert abs(hardy.completed(t, r).imag) < mp.mpf("1e-58")
        assert abs(completed.completed(t, r).imag) < mp.mpf("1e-58")
        # Both normalizations differ by the positive Gamma modulus at real t.
        s = mp.mpf(".5") + mp.j * t
        modulus = abs(mp.power(13 / mp.pi, (s + 1) / 2) * mp.gamma((s + 1) / 2))
        assert abs(completed.completed(t, r) - modulus * hardy.completed(t, r)) < mp.mpf("1e-55")


def test_wronskian_elimination_and_positive_constant_rescaling():
    pair = _pair()
    with mp.workdps(60):
        t = mp.mpf("2.1")
        family = make_family(pair, "minus", 60)
        scaled = make_family(pair, "minus", 60, normalization_height=8)
        x, y = family.parts(t, 1)
        radius = family.radius_from_height(t)
        assert abs(family.critical(radius, t)) < mp.mpf("1e-51")
        # This selected radius kills Z alone; W nonzero means it must not be
        # silently accepted as a collision.
        assert abs(family.wronskian(t)) > mp.mpf("1e-8")
        assert abs(family.jet(radius, t)["Z_t"]) > mp.mpf("1e-8")
        assert abs(scaled.wronskian(t) - scaled.scale ** 2 * family.wronskian(t)) < mp.mpf("1e-48")


def test_companion_has_a_positive_metric_only_on_the_real_branch_side():
    with mp.workdps(40):
        for mu in (mp.mpf(4), mp.mpf(-4), mp.mpf(0)):
            cert = operator_certificate(mu)
            h, j, g = cert["H"], cert["J"], cert["JH"]
            assert h * h == mu * mp.eye(2)
            assert g == mp.matrix([[mu, 0], [0, 1]])
            assert cert["J_self_adjoint_residual"] == mp.zeros(2)
            assert cert["G_self_adjoint_residual"] == mp.zeros(2)
            assert cert["positive_metric"] == (mu > 0)
            assert cert["global_RH_implication"] is False
        assert operator_certificate(0)["H"] != mp.zeros(2)


def test_degenerate_jets_are_not_promoted_to_transverse_collisions():
    for zr, ztt in ((0, 2), (2, 0)):
        try:
            companion_form(zr, ztt, ".001")
        except ValueError:
            pass
        else:
            raise AssertionError("A vanishing unfolding derivative was accepted")
    model = companion_form(2, 4, "-.001")
    assert model["kappa"] == -1
    assert model["mu_linear"] > 0
    assert model["exact_prepared_discriminant"] is False
