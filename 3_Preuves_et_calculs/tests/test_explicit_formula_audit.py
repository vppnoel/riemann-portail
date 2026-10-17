"""V6.3b — audit des conventions de la formule explicite (lit les sorties de run_explicit_formula_audit.py)."""
from pathlib import Path
import csv
D = Path(__file__).resolve().parents[1] / "data"

def test_prime_side_equals_zero_side():
    rows = list(csv.DictReader(open(D / "explicit_formula_audit.csv")))
    for r in rows:
        tol = 1e-7 if r["objet"] == "zeta" else 1e-5
        assert float(r["ecart_rel"]) < tol, r
        assert abs(float(r["lamG_premiers"]) - float(r["lamG_zeros"])) <= 1e-3 * max(1e-6, abs(float(r["lamG_zeros"])))
    assert all(float(r["lamG_zeros"]) > 0 for r in rows if r["objet"] == "zeta")
    assert all(float(r["lamG_zeros"]) < 0 for r in rows if r["objet"] == "DH")
    assert all(float(r["lamG_zeros"]) > 0 for r in rows if r["objet"] == "L_pair_chi5")
    assert sum(r["objet"] == "L_pair_chi5" for r in rows) == 4

def test_each_negative_direction_is_one_offline_quadruplet():
    for r in csv.DictReader(open(D / "explicit_formula_attribution.csv")):
        quads = {k: float(v) for k, v in r.items() if k.startswith("quadruplet_")}
        worst = min(quads.values())
        others = sum(abs(v) for v in quads.values()) - abs(worst)
        assert worst < 0 and others < 1e-3 and float(r["part_zeros_sur_la_droite"]) > 0
        assert abs(float(r["somme_controle"]) - float(r["lamG"])) < 1e-9

def test_L_chi5_zero_count_matches_asymptotics():
    import math
    ts = [float(r["t"]) for r in csv.DictReader(open(D / "L_chi5_zeros.csv"))]
    assert all(abs(float(r["sigma"]) - 0.5) < 1e-9 for r in csv.DictReader(open(D / "L_chi5_zeros.csv")))
    for T in (100, 200, 240):
        n = sum(1 for t in ts if abs(t) <= T)
        expected = (T / math.pi) * math.log(5 * T / (2 * math.pi * math.e))
        assert abs(n - expected) < 3, (T, n, expected)

if __name__ == "__main__":
    n = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); n += 1; print("OK  ", name)
    print(f"{n}/{n}")
