"""V6.8 — tests de l'Archipel d'Euler : espaces V_q de fonctions à équation fonctionnelle commune, îles autour des points d'Euler."""
import csv, math, cmath, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
D = ROOT / "data"

def _rows(name):
    return list(csv.DictReader(open(D / name)))
def _f(x):
    return float(x) if x not in ("", "nan", "None") else float("nan")

def test_spaces_root_numbers_and_hardy_reality():
    from euler_archipelago import characters, hardy_grid, hurwitz_vec
    from zero_reconstruction import hurwitz_zeta
    s = 0.5 + 1j * np.array([0.7, 33.3, 287.1, -199.9])
    assert np.max(np.abs(hurwitz_vec(s, 0.41) - np.array([hurwitz_zeta(x, 0.41) for x in s]))) < 1e-11
    dims = {(int(r["q"]), r["parite"]): int(r["dimension"]) for r in _rows("archipelago_spaces.csv")}
    assert dims == {(3, "impaire"): 1, (5, "paire"): 1, (5, "impaire"): 2, (7, "paire"): 2, (7, "impaire"): 3,
                    (11, "paire"): 4, (11, "impaire"): 5, (13, "paire"): 5, (13, "impaire"): 6}
    for q, par in ((5, 1), (7, 0), (11, 1), (13, 0)):
        ch = characters(q, par); assert all(abs(abs(c["eps"]) - 1) < 1e-12 for c in ch)
        Z, defect, _ = hardy_grid(q, par, np.array([-123.4, 3.21, 77.7, 250.05]))
        assert defect < 1e-9

def test_first_order_rigidity_closed_form():
    """Défaut de multiplicativité au premier ordre dans la direction de chi' en chi : u u' (chi' - chi)(m) (chi' - chi)(n)."""
    from euler_archipelago import characters, dirichlet_coefficients
    q, par = 7, 1; ch = characters(q, par); d = len(ch)
    a = dirichlet_coefficients(q, par, np.eye(d)[0], 400); b = dirichlet_coefficients(q, par, np.eye(d)[1], 400)
    u, up = cmath.exp(-1j * ch[0]["phi"]), cmath.exp(-1j * ch[1]["phi"])
    for m, n in ((2, 3), (3, 5), (4, 9), (2, 13), (6, 11)):
        lhs = a[1] * b[m * n] + b[1] * a[m * n] - a[m] * b[n] - b[m] * a[n]
        rhs = u * up * (ch[1]["table"][m % q] - ch[0]["table"][m % q]) * (ch[1]["table"][n % q] - ch[0]["table"][n % q])
        assert abs(lhs - rhs) < 1e-12
    rg = _rows("archipelago_rigidity.csv")
    assert len(rg) == 27 and min(_f(r["defaut_min_directions_orthogonales"]) for r in rg) > 1.0
    assert max(abs(_f(r["defaut_direction_propre"])) for r in rg) < 1e-12

def test_island_radius_live_for_mod5():
    from euler_archipelago import refine_wronskian, hardy_grid
    r = [x for x in _rows("archipelago_radius.csv") if x["q"] == "5" and x["k"] == "1" and x["T"] == "300"][0]
    ts = _f(r["t_sortie"]); rad, tt, c = refine_wronskian(5, 1, 0, ts - 0.01, ts + 0.01)
    assert abs(rad - _f(r["rayon"])) < 1e-6 and abs(tt - ts) < 1e-6
    e = np.array([1.0, 0.0]); alpha = math.asin(rad); u = np.array([0.0, 1.0]) * np.sign(c[1])
    t = np.arange(ts - 2, ts + 2, 0.0005); Z, _, _ = hardy_grid(5, 1, t)
    cnt = lambda cv: int(np.sum(np.sign((cv @ Z)[1:]) * np.sign((cv @ Z)[:-1]) < 0))
    inside = math.cos(0.9 * alpha) * e + math.sin(0.9 * alpha) * u; outside = math.cos(1.1 * alpha) * e + math.sin(1.1 * alpha) * u
    assert cnt(inside) == cnt(e) and cnt(outside) == cnt(e) - 2

def test_validation_counts_and_mirror_symmetry():
    v = _rows("archipelago_validation.csv"); assert len(v) == 27
    assert all(x["a_095_meme_compte"] == "True" and x["perte_locale_a_105"] == "2" and int(x["directions_au_hasard_ok"]) == 100 for x in v)
    assert max(abs(_f(x["ecart_au_lisse"])) for x in v) < 2.0                 # comptage sur la droite = comptage lisse (GRH jusqu'à 300)
    r300 = {(int(x["q"]), int(x["parite"]), int(x["k"])): (_f(x["rayon"]), _f(x["t_sortie"])) for x in _rows("archipelago_radius.csv") if x["T"] == "300"}
    for (q, par, k), (rad, ts) in r300.items():                                # chi et son conjugué : même île, sortie en miroir
        r2, t2 = r300[(q, par, q - 1 - k)]; assert abs(rad - r2) < 1e-6 and (abs(ts + t2) < 1e-4 or 2 * k == q - 1)   # caractère réel : sorties en +-t*, égales

def test_islands_shrink_with_height_and_exit_at_tightest_pairs():
    rows = _rows("archipelago_radius.csv"); keys = {(x["q"], x["parite"], x["k"]) for x in rows}
    for key in keys:
        rr = [_f(x["rayon"]) for x in sorted((x for x in rows if (x["q"], x["parite"], x["k"]) == key), key=lambda x: int(x["T"]))]
        assert all(b <= a + 1e-15 for a, b in zip(rr[:-1], rr[1:])) and rr[-1] < 0.3 * rr[0]
    sl = [_f(x["pente"]) for x in _rows("archipelago_scaling.csv")]
    assert -1.0 < np.median(sl) < -0.55
    ex = [_f(x["rang_de_l_ecart"]) for x in _rows("archipelago_exits.csv")]
    assert np.median(ex) < 0.01 and np.mean(np.array(ex) < 0.05) > 0.9

def test_map_islands_separate_and_proved_part_fails_off_euler_points():
    mp = _rows("archipelago_map_q7.csv")
    share = {T: np.mean([int(x["deficit"]) <= 0 for x in mp if x["T"] == str(T)]) for T in (50, 150, 300)}
    assert share[50] > 0.25 and share[300] < 0.02 and share[150] < share[50]
    rt = _rows("archipelago_right_of_1.csv")
    assert all(int(x["zeros_Re_s_sup_1.0"]) == 0 and int(x["zeros_Re_s_sup_0.75"]) == 0 for x in rt if x["point"].startswith("point d'Euler"))
    assert sum(int(x["zeros_Re_s_sup_1.0"]) >= 40 for x in rt if x["point"].startswith("milieu")) >= 4
    assert all(_f(x["saut_max_1.0"]) < 1.0 and _f(x["saut_max_0.75"]) < 1.0 for x in rt)
