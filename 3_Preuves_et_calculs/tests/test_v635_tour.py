from pathlib import Path
import json
import math
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from finite_field_jets import (
    FiniteField, certificate, combine, field, hasse_values, jet_matrix,
    multiplicity, poly_pow, spectral_status, square_points, tower_trace,
)


def test_extension_is_a_field_and_not_integer_residues_mod_q():
    F = field(3, 3, [1, 2, 0, 1])
    assert F.q == 27 and F.pow(3, 3) == 5  # u^3 = u+2
    assert 3 != 0 and F.add[F.add[3, 3], 3] == 0
    for a in range(27):
        assert F.pow(a, 27) == a
        if a:
            assert F.mul[a, F.inv[a]] == 1
    for a in range(27):
        for b in range(27):
            c = (a+2*b) % 27
            assert F.mul[a, F.add[b, c]] == F.add[F.mul[a, b], F.mul[a, c]]


def test_field_normalizes_modulus_and_rejects_invalid_domains():
    F = FiniteField(3, [1, 2, 0, 1, 3])
    assert F.n == 3 and F.modulus == (1, 2, 0, 1)
    for p, n, m in ((9, 1, None), (3, 2, [2, 0, 1]),
                    (3, 2, [1, 2, 0, 1]), (3, 7, None)):
        try:
            field(p, n, m)
        except ValueError:
            pass
        else:
            raise AssertionError("Entrée invalide acceptée")


def test_hasse_order_p_survives_and_frobenius_jets_vanish():
    F = field(3, 3, (1, 2, 0, 1))
    xs = list(range(27))
    high = hasse_values([0, 0, 0, 1], xs, 4, F)
    assert np.all(high[:, 3] == 1)
    assert math.factorial(3) % 3 == 0
    frob = hasse_values([0]*27+[1], xs, 27, F)
    assert not np.any(frob[:, 1:])


def test_factored_jet_matrix_matches_direct_full_polynomials():
    F = field(3, 3, (1, 2, 0, 1))
    S, _ = square_points([1, 1, 0, 1], F)
    matrix, g = jet_matrix([1, 1, 0, 1], S, 3, 11, 4, F)
    direct = []
    for j in range(3):
        for a in range(11):
            shift = j*27+a
            for tail in ([1], g.tolist()):
                poly = [0]*shift+tail
                direct.append(hasse_values(poly, S, 4, F).reshape(-1))
    assert np.array_equal(matrix, np.array(direct).T)


def test_f27_exact_kernel_and_independent_multiplicity():
    c = certificate(3, 3, [1, 1, 0, 1], 3, 11, 4, (1, 2, 0, 1))
    assert (c["dimension"], c["rang_majore"], c["rang_exact"]) == (66, 64, 51)
    assert c["noyau_exact"] == 15 and c["degre_temoin"] == 93
    assert c["S"] == 13 and c["multiplicite_minimale"] == 4


def test_empty_square_set_accepts_nonzero_constant_witness():
    c = certificate(5, 1, [0, 2, 0, 1], 1, 1, 1)
    assert c["S"] == 0 and c["degre_temoin"] == 0
    assert c["coefficients_temoin"] == [1]


def test_all_saved_witnesses_reconstruct_and_divide_exactly():
    data = json.loads((ROOT/"data/v635_certificats.json").read_text())
    for c in data["certificats"]:
        F = field(c["p"], c["n"], c["module"])
        g = poly_pow(c["f"], (F.q-1)//2, F)
        poly = combine(np.array(c["vecteur_noyau"]), g, c["J"], c["K"], F)
        assert poly.tolist() == c["coefficients_temoin"] and np.any(poly)
        S, z = square_points(c["f"], F)
        assert S == c["points_S"] and z == c["racines_f"]
        assert min((multiplicity(poly, x, F) for x in S), default=c["M"]) >= c["M"]
        assert not np.any(hasse_values(poly, S, c["M"], F))
        assert c["M"]*len(S) <= len(poly)-1 <= c["degre_max"]
    twist = next(c for c in data["certificats"] if c["torsion"])
    assert (twist["conditions_naives"], twist["dimension"], twist["rang_exact"]) == (560, 450, 400)


def test_saved_tower_is_recounted_before_recurrence_check():
    data = json.loads((ROOT/"data/v635_tour.json").read_text())
    traces = {}
    for c in data["comptages"]:
        F = field(c["p"], c["n"], c["module"])
        S, z = square_points([1, 1, 0, 1], F)
        N = 2*len(S)+z+1
        assert N == c["N_direct"]
        if c["n"] == 1:
            traces[c["p"]] = c["p"]+1-N
        assert N == F.q+1-tower_trace(c["p"], traces[c["p"]], c["n"])


def test_point_count_matches_independent_pair_enumeration():
    F = field(5, 3, (1, 1, 0, 1))
    N = 1+sum(F.mul[y, y] == F.eval([1, 1, 0, 1], x)
              for x in range(F.q) for y in range(F.q))
    assert N == 108


def test_spectral_conclusion_requires_uniformity_and_smoothness():
    assert spectral_status(5, -3)["hasse_exact"]
    assert not spectral_status(5, 6)["hasse_exact"]
    # Le produit 5 ne suffit pas : racines 5 et 1, moments normalisés divergents.
    assert tower_trace(5, 6, 6) == 5**6+1
    assert tower_trace(5, 6, 6) > 10*5**3
    # Cubique singulière x^2(x+2) : sa zêta brute a un zéro de module 1.
    for n in (1, 2, 3):
        F = field(5, n)
        S, z = square_points([0, 0, 2, 1], F)
        assert 2*len(S)+z+1 == F.q+1-(-1)**n
