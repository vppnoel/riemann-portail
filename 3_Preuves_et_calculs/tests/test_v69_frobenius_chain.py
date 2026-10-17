"""V6.9 — tests du chaînon : Frobenius reconstruit depuis les comptages ; spectre des longueurs lu dans les zéros."""
import csv, math, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
D = ROOT / "data"

def _rows(name):
    return list(csv.DictReader(open(D / name)))
def _f(x):
    return float(x) if x not in ("", "nan") else float("nan")

def test_frobenius_rebuilt_from_counts_live():
    from frobenius_chain import gns_frobenius
    from stability_radius import normalized
    r, lam, ev = gns_frobenius(normalized([1, 0, 0, 0, 9], 3))           # y^2 = x^5 + x^3 + 1 sur F_3
    assert r == 4 and np.allclose(np.sort(np.angle(lam)), np.sort(np.angle(np.exp(1j * math.pi * (2 * np.arange(4) + 1) / 4))), atol=1e-10)
    assert np.allclose(np.abs(lam), 1, atol=1e-12) and ev[0] > -1e-12
    r, lam, ev = gns_frobenius(normalized([1, 1, -8, 5, 25], 5))         # faux jumeau : opérateur reconstruit, mais pas unitaire
    assert r == 4 and np.sum(ev < -1e-9) == 1 and sorted(np.round(np.abs(lam), 4))[-1] == 1.4393 and sorted(np.round(np.abs(lam), 4))[0] == 0.6948
    r, lam, ev = gns_frobenius(normalized([1, 0, 10, 0, 25], 5))         # (1 + 5u^2)^2 : les comptages ne voient que 2 zéros distincts
    assert r == 2 and np.allclose(np.sort(lam.imag), [-1, 1], atol=1e-8)
    from frobenius_chain import spectral_masses                          # la multiplicité reparaît comme masse
    assert np.allclose(spectral_masses(normalized([1, 0, 10, 0, 25], 5), lam), [2, 2], atol=1e-7)
    r, lam, ev = gns_frobenius(normalized([1, 1, 7, -2, 35, 25, 125], 5))  # vraie courbe de genre 3 sur F_5, zéros confondus
    assert r == 4 and np.allclose(np.sort(spectral_masses(normalized([1, 1, 7, -2, 35, 25, 125], 5), lam).real), [1, 1, 2, 2], atol=1e-6)

def test_reconstruction_summary_over_all_objects():
    g = _rows("chain_gns.csv")
    for kind, n in (("courbe", 524), ("faux jumeau", 220), ("zéros confondus", 5)):
        d = [x for x in g if x["objet"] == kind]; assert len(d) == n
        assert all(int(x["rang_gns"]) == int(x["zeros_distincts"]) for x in d)
        assert all(int(x["gram_negatives"]) == int(x["hors_cercle"]) // 2 for x in d)
        assert max(_f(x["symetrie_eq_fonct"]) for x in d) < 1e-10           # symétrie de l'équation fonctionnelle
        unit = [_f(x["ecart_unitaire"]) < 1e-8 for x in d]
        assert all(unit) if kind != "faux jumeau" else not any(unit)
    assert all(int(x["rang_gns"]) < int(x["dimension_2g"]) for x in g if x["objet"] == "zéros confondus")

def test_length_spectrum_reads_primes_in_zeta_zeros():
    import pandas as pd
    from frobenius_chain import length_spectrum, log_derivative_coefficients
    c = log_derivative_coefficients(np.ones(13, dtype=complex))
    assert abs(c[8] - math.log(2)) < 1e-12 and abs(c[6]) < 1e-12 and abs(c[7] - math.log(7)) < 1e-12
    gz = pd.read_csv(D / "zeta_zeros_1500.csv").t.values; gam = np.concatenate([gz, -gz]).astype(complex)
    S = length_spectrum(gam, np.array([math.log(2), math.log(6), math.log(5)]), 500.0)
    assert abs(S[0].real - math.log(2) / math.sqrt(2)) < 0.03 and abs(S[1]) < 0.03 and abs(S[2].real - math.log(5) / math.sqrt(5)) < 0.04

def test_euler_product_visible_in_lengths_and_single_base_lattice():
    p = _rows("chain_lengths.csv")
    def share(obj):
        d = [x for x in p if x["objet"] == obj]; m = [math.hypot(_f(x["mesure_re"]), _f(x["mesure_im"])) for x in d]
        return sum(mm for mm, x in zip(m, d) if x["puissance_premiere"] == "False") / sum(m)
    assert share("L_chi5") < 0.01 and share("zeta") < 0.06 and share("DH") > 0.4
    for obj in ("courbe_F3", "faux_jumeau_F5", "deux_courbes"):
        d = [x for x in p if x["objet"] == obj]
        assert max(abs(_f(x["mesure_re"]) - _f(x["predit_re"])) for x in d if x["n"] != "0") < 0.03
        assert [abs(_f(x["mesure_re"])) for x in d if x["n"] == "0"][0] < 0.01      # rien hors des longueurs n log q
