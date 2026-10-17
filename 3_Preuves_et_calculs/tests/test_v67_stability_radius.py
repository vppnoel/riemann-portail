"""V6.7 — tests de STABILITY-RADIUS : marge de la forme contre marge de l'objet (Modèle réduit, zeta, L, DH)."""
import csv, math, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
D = ROOT / "data"

def _rows(name):
    return list(csv.DictReader(open(D / name)))
def _f(x):
    return float(x) if x not in ("", "nan", "None") else float("nan")

def test_chebyshev_writing_and_closed_form_gram():
    from stability_radius import from_free, H_poly
    from dual_lock_audit import gram_matrix, gram_matrix_closed
    rng = np.random.default_rng(3)
    for g in (1, 2, 4, 7):
        b = from_free(rng.normal(size=g)); h = H_poly(b)
        for u in (0.4 + 0.3j, -1.3, 0.2 - 0.9j):
            assert abs(np.polyval(b[::-1], u) - u ** g * np.polynomial.polynomial.polyval(u + 1 / u, h)) < 1e-9 * max(1, abs(np.polyval(b[::-1], u)))
    for T, W, m in ((20.0, 2.5, 5), (86.0, 5.0, 9), (176.0, 10.0, 7)):
        fr = T + 0.6 * (np.arange(m) - (m - 1) / 2)
        Gq, Gc = gram_matrix(fr, W), gram_matrix_closed(fr, W)
        assert np.max(np.abs(Gq - Gc)) / np.max(np.abs(Gc)) < 1e-12

def test_form_margin_is_positive_up_to_2g_then_exactly_zero():
    from stability_radius import normalized, form_margin
    for c, q in (([1, 0, 0, 0, 9], 3), ([1, 1, 3], 3), ([1, -1, 2, -5, 25], 5)):
        g = (len(c) - 1) // 2; b = normalized(c, q)
        assert all(form_margin(b, L) > 1e-6 for L in range(1, 2 * g + 1))
        assert all(abs(form_margin(b, L)) < 1e-12 for L in range(2 * g + 1, 2 * g + 5))
    r = _rows("stability_model_curves.csv")
    assert len(r) == 525 and max(abs(_f(x["marge_forme_L2g1"])) for x in r) < 1e-13
    assert all(x == "True" for x in (y["recompte_ok"] for y in _rows("stability_model_new_curves.csv")))

def test_inertia_law_counts_off_circle_zeros():
    from run_stability_model import exact_inertia, exact_off_circle
    from stability_radius import normalized
    from run_reduced_model import EXAMPLE
    q, c = EXAMPLE; b = normalized(c, q)
    assert exact_off_circle(b) == 2 and exact_inertia(b, 4) == 1 and exact_inertia(b, 3) == 0   # une paire réelle hors du cercle : 1 direction négative à la fenêtre 2g
    ri = _rows("stability_model_inertia.csv")
    assert len(ri) == 900 and all(int(x["negatives_L2g_60chiffres"]) == int(x["hors_cercle"]) // 2 for x in ri)
    assert sum(x["rh_decide_L2gm1"] == "True" for x in ri) < 900
    rf = _rows("stability_model_fakes.csv")
    assert len(rf) == 220 and all(int(x["negatives_L2g"]) == int(x["hors_cercle"]) // 2 > 0 for x in rf)

def test_structured_radius_is_the_true_minimal_exit():
    from stability_radius import normalized, structured_radius, perturbed, off_circle, from_free
    rng = np.random.default_rng(11)
    rows = _rows("stability_model_curves.csv")
    picks = [next(x for x in rows if x["q"] == q and x["g"] == g and _f(x["rayon_objet"]) > 0.05) for q, g in (("3", "1"), ("3", "2"), ("5", "3"), ("3", "5"))]
    for x in picks:
        c, q = list(map(int, x["P"].split())), int(x["q"])
        g = (len(c) - 1) // 2; b = normalized(c, q); sr = structured_radius(b); w = np.r_[np.full(g - 1, 2.0), 1.0]
        assert abs(sr["rayon"] - _f(x["rayon_objet"])) < 1e-9
        assert off_circle(perturbed(b, sr["delta"], 0.999)) == 0 and off_circle(perturbed(b, sr["delta"], 1.001)) > 0
        assert abs(math.sqrt(float(np.sum(w * sr["delta"] ** 2))) - sr["rayon"]) < 1e-9
        best = np.inf
        for _ in range(300):                              # aucune direction au hasard ne sort plus près que le rayon
            d = rng.normal(size=g); d /= math.sqrt(float(np.sum(w * d * d))); lo, hi = 0.0, 10.0
            if off_circle(from_free(b[1: g + 1] + hi * d)) == 0: continue
            for _ in range(50):
                mid = 0.5 * (lo + hi)
                if off_circle(from_free(b[1: g + 1] + mid * d)) == 0: lo = mid
                else: hi = mid
            best = min(best, hi)
        assert best >= sr["rayon"] * (1 - 1e-6)

def test_object_margin_can_be_exactly_zero_for_true_curves():
    from stability_radius import normalized, structured_radius
    for c in ([1, 0, 10, 0, 25], [1, -4, 14, -20, 25], [1, 0, -10, 0, 25]):     # (1 + 5u^2)^2, (1 - 2u + 5u^2)^2, (1 - 5u^2)^2
        assert structured_radius(normalized(c, 5))["rayon"] < 1e-6
    fk = [x for x in _rows("reduced_model_fakes.csv") if x["realise"] == "True" and x["q"] == "5" and x["g"] == "2"]
    real = {(int(float(x["c1"])), int(float(x["c2"]))) for x in fk}
    assert {(0, 10), (-4, 14), (4, 14), (0, -10)} <= real
    r = _rows("stability_model_curves.csv")
    assert sum(x["zeros_confondus"] == "True" for x in r) == 1
    pos = [x for x in r if x["zeros_confondus"] != "True"]
    assert all(int(x["hors_cercle_a_1001"]) > 0 and x["rh_a_0999"] == "True" for x in pos)
    med = {g: np.median([_f(x["rayon_objet"]) for x in r if x["q"] == "3" and int(x["g"]) == g]) for g in range(1, 13)}
    assert med[1] > 5 * med[12] > 0

def test_form_threshold_collapses_at_2g_plus_1_but_object_threshold_does_not():
    rp = _rows("stability_model_paths.csv"); rf = _rows("stability_model_fakes.csv")
    last = [x for x in rp if int(x["L"]) == 2 * int(x["g"]) + 1]
    assert len(last) == 220 and all(_f(x["seuil_forme"]) == 0.0 for x in last)
    obj = np.array([_f(x["seuil_objet"]) for x in rf if x["g"] == "2"])
    assert 0.1 < np.median(obj) < 0.25 and np.sum(obj > 1e-6) >= 160
    from stability_radius import normalized, object_threshold
    b0, b1 = normalized([1, -4, 14, -20, 25], 5), normalized([1, -4, 15, -20, 25], 5)
    assert object_threshold(b0, b1) < 1e-9                                      # départ d'une courbe à marge nulle : sortie immédiate
    b0 = normalized([1, 0, 10, 0, 25], 5); b1 = normalized([1, 1, -8, 5, 25], 5)
    assert object_threshold(b0, b1) > 0.01                                      # marge nulle n'est pas sortie dans toutes les directions

def test_rank_law_true_objects_stop_at_zero_fakes_go_below():
    r = _rows("rank_law.csv")
    on = [x for x in r if x["objet"] in ("zeta", "L_chi5", "F6")]
    assert len(on) > 200 and min(_f(x["lam_rel"]) for x in on) > -1e-13
    for T in ("85.7", "114.2", "166.5", "176.7"):
        assert any(x["objet"] == "DH" and x["T"] == T and x["m"] == "3" and _f(x["lam_rel"]) < 0 for x in r)
    fits = {(x["objet"], x["W"]): _f(x["pente_log10_par_dimension"]) for x in _rows("rank_law_fits.csv")}
    assert all(-1.0 < fits[(k, "5.0")] < -0.7 for k in ("zeta", "L_chi5", "F6"))
    reach = [x for x in _rows("rank_law_reach.csv") if x["T"] == "100.0" and x["W"] == "10.0"][0]
    assert _f(reach["distance_au_zero_hors_droite"]) > 14 and int(float(reach["premiere_dimension_negative"])) > int(float(reach["zeros_atteints_a_ce_m"]))

def test_object_path_L_to_DH_creates_exactly_the_four_off_line_pairs():
    from family_mod5 import hardy, PHI, EPS
    import cmath
    assert abs(abs(EPS) - 1) < 1e-12
    for t in (7.7, 85.0, 199.3):
        assert hardy(t)[2] < 1e-10
    iv = [x for x in _rows("family_mod5_intervals.csv") if x["trajet"] == "+" and x.get("seuil") not in ("", None)]
    lost = sorted((_f(x["t_rencontre"]), _f(x["seuil"])) for x in iv if 0 < _f(x["seuil"]) < 1 and _f(x["t_droite"]) <= 200)
    assert len(lost) == 4
    for (t, s), (t0, s0) in zip(lost, ((85.90, 0.602), (114.34, 0.646), (166.50, 0.937), (176.97, 0.280))):
        assert abs(t - t0) < 0.01 and abs(s - s0) < 0.001
    dh_off = (85.699, 114.163, 166.479, 176.702)
    assert all(min(abs(t - u) for u in dh_off) < 0.3 for t, _ in lost)
    of = _rows("object_vs_form.csv")
    f114 = {float(x["W"]): _f(x["seuil_forme"]) for x in of if abs(float(x["t_zero_DH"]) - 114.163) < 0.01}
    f857 = {float(x["W"]): _f(x["seuil_forme"]) for x in of if abs(float(x["t_zero_DH"]) - 85.699) < 0.01}
    assert f857[10.0] < 1e-3 and min(f114.values()) < 0.05 and f114[10.0] > 0.5           # la forme dépend de la fenêtre
