"""V6.4 — tests du seuil tau_c (test prioritaire de l'Atlas des métaphores)."""
import csv, math, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
D = ROOT / "data"

def _rows(name):
    return list(csv.DictReader(open(D / name)))
def _f(x):
    return float(x) if x not in ("", "nan") else float("nan")

def test_three_independent_computations_give_the_same_threshold():
    rows = [r for r in _rows("tau_threshold.csv") if r["tau_c_premiers_quad"] not in ("", "nan")]
    assert len(rows) == 9
    for r in rows:
        assert abs(_f(r["tau_c_premiers_quad"]) - _f(r["tau_c_zeros"])) < 1e-3
        if r["tau_c_premiers_gauss"] not in ("", "nan"):
            assert abs(_f(r["tau_c_premiers_gauss"]) - _f(r["tau_c_zeros"])) < 1e-6
        assert abs(_f(r["tau_c_par_attribution"]) - _f(r["tau_c_zeros"])) < 1e-9

def test_lambda_min_is_concave_in_tau():
    cur = {}
    for r in _rows("tau_threshold_curve.csv"):
        cur.setdefault((r["T"], r["dimension"]), []).append((float(r["tau"]), float(r["lam_min"])))
    assert len(cur) == 12
    for pts in cur.values():
        y = np.array([v for _, v in sorted(pts)])
        assert y[0] > 0 > y[-1] and np.diff(y, 2).max() < 1e-9

def test_threshold_never_increases_with_dimension():
    by = {}
    for r in _rows("tau_threshold.csv"):
        by.setdefault(r["T"], []).append((int(r["dimension"]), float(r["tau_c_zeros"])))
    assert len(by) == 4
    for pts in by.values():
        t = [v for _, v in sorted(pts)]
        assert all(a >= b - 1e-9 for a, b in zip(t[:-1], t[1:])) and t[0] > t[-1]

def test_threshold_collapses_when_the_support_widens():
    rows = sorted(_rows("tau_threshold_width.csv"), key=lambda r: float(r["demi_largeur"]))
    assert math.isnan(_f(rows[0]["tau_c"])) and float(rows[0]["lam_DH"]) > 0          # W = 1,5 : DH paraît positif
    t = [_f(r["tau_c"]) for r in rows[1:]]
    assert all(a > b for a, b in zip(t[:-1], t[1:])) and t[0] > 0.8 and t[-1] < 1e-3

def test_two_key_map_is_an_exact_shift_of_the_1d_curve():
    rows = _rows("tau_threshold_2d.csv")
    assert len(rows) == 100 and max(abs(float(r["lam_min_direct"]) - float(r["lam_min_par_translation"])) for r in rows) < 1e-9
    from dual_lock import correlation_direct      # M_q = log(q/pi) F0 et F0 = G : même intégrale, par construction
    from dual_lock_audit import gram_matrix
    fr = 86.0 + 0.6 * (np.arange(3) - 1.0)
    F0 = np.array([[correlation_direct(0.0, 2.5, a, b) for b in fr] for a in fr])
    assert np.max(np.abs(F0 - gram_matrix(fr, 2.5))) < 1e-7

def test_threshold_follows_offline_zeros_not_the_euler_product_and_live_value():
    w = _rows("tau_threshold_witnesses.csv")
    for r in w:
        if r["temoin"] == "E2":
            assert 0 < _f(r["tau_c"]) < 0.1
        else:
            assert math.isnan(_f(r["tau_c"])) and float(r["lam_min_sur_le_trajet"]) > 0
    # recalcul direct (côté zéros) du seuil à T = 86, dimension 5
    from run_tau_threshold import freqs, zero_side, threshold, GL_, GD_
    from dual_lock_audit import gram_matrix
    fr = freqs(86.0, 5); G = gram_matrix(fr, 2.5)
    tc = threshold(zero_side(fr, 2.5, GL_)[0], zero_side(fr, 2.5, GD_)[0], G)
    ref = [float(r["tau_c_zeros"]) for r in _rows("tau_threshold.csv") if float(r["T"]) == 86.0 and int(r["dimension"]) == 5][0]
    assert abs(tc - ref) < 1e-9 and abs(tc - 0.674248) < 1e-5

if __name__ == "__main__":
    n = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); n += 1; print("OK  ", name)
    print(f"{n}/{n}")
