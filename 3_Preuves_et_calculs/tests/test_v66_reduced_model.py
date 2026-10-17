"""V6.6 — tests du Modèle réduit : courbes hyperelliptiques sur F_q, où RH est un théorème (Weil)."""
import csv, math, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
D = ROOT / "data"

def _rows(name):
    return list(csv.DictReader(open(D / name)))
def _b(x):
    return x == "True"

def test_point_counts_live_against_naive_counts_and_recount_of_a_genus_3_curve():
    from function_field import count_points, L_polynomial, power_sums
    q = 3
    def naive_n1(f):                                   # F_3 : critère d'Euler, arithmétique modulaire seule
        n = 1
        for x in range(q):
            v = 0
            for c in f: v = (v * x + c) % q
            n += 1 if v == 0 else (2 if pow(v, (q - 1) // 2, q) == 1 else 0)
        return n
    def naive_n2(f):                                   # F_9 = F_3[i], i^2 = -1 : paires (a, b), indépendant des tables
        mul = lambda u, v: ((u[0] * v[0] - u[1] * v[1]) % q, (u[0] * v[1] + u[1] * v[0]) % q)
        squares = {mul((a, b), (a, b)) for a in range(q) for b in range(q)}
        n = 1
        for a in range(q):
            for b in range(q):
                v = (0, 0)
                for c in f: v = mul(v, (a, b)); v = ((v[0] + c) % q, v[1])
                n += 1 if v == (0, 0) else (2 if v in squares else 0)
        return n
    for f in ([1, 0, 1, 0, 0, 1], [1, 2, 0, 1, 1, 2, 0, 1], [1, 1, 0, 2]):
        assert count_points(f, q, 1) == naive_n1(f) and count_points(f, q, 2) == naive_n2(f)
    f = [1, 2, 0, 1, 1, 2, 0, 1]                        # genre 3 : P(u) depuis N_1..N_3, puis N_4 et N_5 recomptés sur F_81 et F_243
    N = [count_points(f, q, n) for n in range(1, 6)]
    c = L_polynomial(N[:3], q, 3); S = power_sums(c, 5)
    assert [q ** n + 1 - S[n - 1] for n in (4, 5)] == N[3:]
    assert np.allclose(np.abs(1 / np.roots(c[::-1])), math.sqrt(q), atol=1e-7)

def test_all_425_true_curves_recount_exactly_and_satisfy_castelnuovo_to_level_60():
    r = _rows("reduced_model_curves.csv")
    assert len(r) == 425 and all(_b(x["recompte_ok"]) for x in r) and all(_b(x["castelnuovo_exact_ok_n60"]) for x in r)
    assert max(float(x["ecart_RH"]) for x in r) < 1e-6
    plan = {(3, g) for g in range(1, 9)} | {(5, g) for g in range(1, 6)} | {(7, g) for g in range(1, 5)}
    assert {(int(x["q"]), int(x["g"])) for x in r} == plan

def test_integer_fakes_exist_none_is_a_curve_and_castelnuovo_unmasks_them_at_a_finite_level():
    from run_reduced_model import classify
    r = _rows("reduced_model_fakes.csv")
    fakes = {}
    for x in r:
        rh, eu, real = _b(x["RH"]), _b(x["euler_positif"]), _b(x["realise"])
        if real: assert rh and eu                          # toute courbe comptée : RH et comptages positifs
        if eu and not rh: fakes.setdefault((int(x["q"]), int(x["g"])), []).append(x)
    assert {k: len(v) for k, v in fakes.items()} == {(3, 1): 1, (3, 2): 17, (5, 1): 3, (5, 2): 199}
    for (q, g), v in fakes.items():
        lv = [int(float(x["premier_etage_castelnuovo_faux"])) for x in v]
        if g == 2:
            assert 2 <= min(lv) and max(lv) <= 5
            assert all(float(x["rho_1"]) <= 1 for x in v)              # invisibles au premier comptage
            assert all(float(x["alpha_max_sur_q"]) < 1 for x in v)     # niveau de Vallée Poussin : aucun zéro sur Re s = 1
        else:
            assert set(lv) == {1}
    for x in fakes[(5, 2)][::20]:                                      # reclassement en direct
        c1, c2 = int(x["c1"]), int(float(x["c2"]))
        k = classify([1, c1, c2, 5 * c1, 25], 5, 2)
        assert k["euler_positif"] and not k["RH"] and k["premier_etage_castelnuovo_faux"] == int(float(x["premier_etage_castelnuovo_faux"]))

def test_example_fake_twin_has_positive_integer_counts_and_breaks_castelnuovo_at_level_5():
    from function_field import power_sums, closed_points, castelnuovo_ratio
    from run_reduced_model import EXAMPLE
    q, c = EXAMPLE
    S = power_sums(c, 200); a = closed_points(S, q); rho = castelnuovo_ratio(S, q, 2)
    assert all(isinstance(x, int) and x >= 0 for x in a)
    assert all(r < 1 for r in rho[:4]) and rho[4] > 2
    assert all(c[4 - k] == q ** (2 - k) * c[k] for k in range(5))  # équation fonctionnelle
    al = np.abs(1 / np.roots(c[::-1]))
    assert np.max(np.abs(al / math.sqrt(q) - 1)) > 0.1 and np.max(al) < q
    ex = _rows("reduced_model_example.csv")
    assert [int(x["N_n"]) for x in ex[:6]] == [7, 9, 166, 545, 3587, 14742]

def test_tower_positivity_holds_with_margin_shrinking_up_the_tower():
    tw = _rows("reduced_model_tower.csv")
    assert max(float(x["max_rho"]) for x in tw) <= 1 + 1e-12
    r = _rows("reduced_model_curves.csv")
    m = np.array([[float(x[k]) for k in ("marge_tour_n10", "marge_tour_n100", "marge_tour_n1000", "marge_tour_n100000")] for x in r])
    assert np.all(m >= -1e-12) and np.all(np.diff(m, axis=1) <= 1e-15)
    for g in range(1, 9):
        mg = np.median([float(x["marge_tour_n100000"]) for x in r if x["q"] == "3" and int(x["g"]) == g])
        assert mg < 0.1

def test_survival_interval_is_positive_and_shrinks_with_genus():
    r = _rows("reduced_model_curves.csv")
    assert all(float(x["survie_moins"]) < 0 < float(x["survie_plus"]) for x in r)
    med = {g: np.median([float(x["survie_relative"]) for x in r if x["q"] == "3" and int(x["g"]) == g]) for g in range(1, 9)}
    assert med[1] > 5 * med[8] and med[7] < 0.05 and med[8] < 0.05

def test_maximal_curve_saturates_castelnuovo_exactly_at_level_4():
    from function_field import count_points, L_polynomial, power_sums, castelnuovo_ratio
    f = [1, 0, 1, 0, 0, 1]                                         # y^2 = x^5 + x^3 + 1 sur F_3
    N = [count_points(f, 3, n) for n in range(1, 5)]
    assert L_polynomial(N[:2], 3, 2) == [1, 0, 0, 0, 9]
    assert N[3] == 118 == 3 ** 4 + 1 + 2 * 2 * 3 ** 2
    S = power_sums([1, 0, 0, 0, 9], 8)
    assert S[3] == -36 and castelnuovo_ratio(S, 3, 2)[3] == 1.0
