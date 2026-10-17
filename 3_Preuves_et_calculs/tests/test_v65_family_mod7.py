"""V6.5 — tests de la famille modulo 7 : F_theta = (1 - theta) L(s, chi_3) + theta f_7."""
import csv, math, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
D = ROOT / "data"

def _rows(name):
    return list(csv.DictReader(open(D / name)))
def _f(x):
    return float(x) if x not in ("", "nan") else float("nan")

def test_family_keeps_the_functional_equation_and_only_theta_0_is_multiplicative():
    import cmath
    from family_mod7 import F_theta, completed, coefficients, vartheta, EPS
    assert abs(abs(EPS) - 1) < 1e-12
    for th in (0.0, 0.37, 1.0, -0.6):
        F = lambda s: F_theta(s, th)
        for s in (0.3 + 7j, 0.7 + 12.5j, 1.4 + 3.1j):
            assert abs(completed(F, s) - completed(F, 1 - s)) / abs(completed(F, s)) < 1e-10
        for t in (3.3, 88.8, 412.5):                       # fonction de Hardy réelle
            assert abs((cmath.exp(1j * vartheta(t)) * F(0.5 + 1j * t)).imag) < 1e-9
    a0, a1 = coefficients(0.0, 50), coefficients(1.0, 50)
    assert abs(a0[1] - 1) < 1e-12 and abs(a1[1] - 1) < 1e-12 and abs(a0[2] * a0[3] - a0[6]) < 1e-12 and abs(a1[2] * a1[3] - a1[6]) > 0.5

def test_zeros_of_L_chi3_are_all_on_the_line_live_count():
    from run_family_mod7 import winding_theta
    from family_mod7 import hardy
    t = np.arange(0.005, 60.0, 0.01); z = np.array([hardy(float(x))[0] for x in t])
    on_line = int(np.sum(np.sign(z[1:]) * np.sign(z[:-1]) < 0))
    w, _ = winding_theta(0.0, 0.0001, 60.0, h=0.02)
    assert round(w) == on_line and len(_rows("family_mod7_intervals.csv")) == 958

def test_survival_interval_contains_0_and_shrinks_with_height():
    rows = sorted(_rows("family_mod7_survival.csv"), key=lambda r: float(r["T"]))
    plus = [float(r["theta_plus"]) for r in rows]; minus = [float(r["theta_moins"]) for r in rows]
    assert all(m < 0 < p for m, p in zip(minus, plus))
    assert all(a >= b for a, b in zip(plus[:-1], plus[1:])) and all(a <= b for a, b in zip(minus[:-1], minus[1:]))
    assert plus[-1] - minus[-1] < 0.1 and plus[0] - minus[0] > 1.0 and abs(minus[-1]) < plus[-1]

def test_all_zeros_on_the_line_only_near_the_euler_point():
    rows = _rows("family_mod7_proportion.csv"); surv = sorted(_rows("family_mod7_survival.csv"), key=lambda r: float(r["T"]))[-1]
    lo, hi = float(surv["theta_moins"]), float(surv["theta_plus"])
    for r in rows:
        th, on, tot = float(r["theta"]), int(r["sur_la_droite_T1000"]), int(r["total_theta0_T1000"])
        if lo < th < hi: assert on == tot == 958
        if th < lo - 1e-3 or th > hi + 1e-3: assert on < tot
    f7 = [r for r in rows if abs(float(r["theta"]) - 1.0) < 1e-9][0]
    assert int(f7["sur_la_droite_T1000"]) / 958 < 0.9

def test_thresholds_follow_gaps_and_are_one_sided():
    from scipy.stats import spearmanr
    ev = [r for r in _rows("family_mod7_intervals.csv") if r["seuil"] not in ("", "nan")]
    h = np.array([abs(float(r["seuil"])) for r in ev]); g = np.array([float(r["ecart_normalise"]) for r in ev])
    assert len(ev) == 451 and spearmanr(g, h).statistic > 0.6
    assert 1.4 < np.polyfit(np.log(g), np.log(h), 1)[0] < 2.2
    smallest = np.argsort(h)[:100]
    assert sum(float(ev[i]["seuil"]) < 0 for i in smallest) >= 80

def test_pair_leaves_the_line_with_square_root_law():
    rows = _rows("family_mod7_pair.csv"); off = [r for r in rows if r["etat"] == "hors droite"]; on = [r for r in rows if r["etat"] == "sur la droite"]
    thc = max(float(r["theta"]) for r in on)
    assert max(_f(r["residu"]) for r in off) < 1e-10 and all(abs(float(r["sigma_1"]) + float(r["sigma_2"]) - 1) < 1e-9 for r in off)
    e = np.array([float(r["theta"]) / thc - 1 for r in off]); d = np.array([float(r["sigma_1"]) - 0.5 for r in off]); m = e < 0.05
    assert 0.45 < np.polyfit(np.log(e[m]), np.log(d[m]), 1)[0] < 0.55
    gaps = [float(r["t_2"]) - float(r["t_1"]) for r in on]
    assert gaps[0] > 0.5 and gaps[-1] < 1e-3                # les deux zéros se rejoignent

def test_imprint_of_zeta_peaks_at_the_euler_point():
    rows = _rows("family_mod7_imprint.csv"); best = min(rows, key=lambda r: float(r["rapport"]))
    assert float(best["theta"]) == 0.0 and float(best["rapport"]) < 0.9
    r05 = [r for r in rows if float(r["theta"]) == 0.5][0]; r0 = best
    assert float(r05["rapport"]) - float(r0["rapport"]) > 10 * math.hypot(float(r05["incertitude"]), float(r0["incertitude"]))

def test_proved_part_of_rh_also_fails_away_from_the_euler_point():
    """V6.5.1 : aucun zéro à droite de Re s = 1 (ni de 0,75) en theta = 0 ; le sosie f_7 en a à droite de 1."""
    rows = {float(r["theta"]): r for r in _rows("family_mod7_right_count.csv")}
    assert int(rows[0.0]["zeros_a_droite_de_1.0"]) == 0 and int(rows[0.0]["zeros_a_droite_de_0.75"]) == 0
    assert int(rows[1.0]["zeros_a_droite_de_1.0"]) >= 1 and int(rows[-1.0]["zeros_a_droite_de_1.0"]) > int(rows[-0.5]["zeros_a_droite_de_1.0"]) > 0
    assert all(float(r[k]) < 3.0 for r in rows.values() for k in ("pas_de_phase_max_0.75", "pas_de_phase_max_1.0"))
    from family_mod7 import F1
    rm = {float(r["theta"]): r for r in _rows("family_mod7_rightmost.csv")}
    z = complex(float(rm[1.0]["sigma_max"]), float(rm[1.0]["t"]))
    assert z.real > 1.05 and abs(F1(z)) < 1e-9

if __name__ == "__main__":
    n = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); n += 1; print("OK  ", name)
    print(f"{n}/{n}")
