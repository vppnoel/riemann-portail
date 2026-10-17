"""V6.3d — tests du classement des instruments (témoins F6/E2, reconstruction par les zéros, listes de zéros)."""
import csv, math, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
D = ROOT / "data"

def _rows(name):
    return list(csv.DictReader(open(D / name)))

def test_witness_lambda_recurrence_matches_closed_form():
    from lock_witnesses import lambda_witness, lambda_closed_form
    for kind in ("zeta", "F6", "E2"):
        assert np.max(np.abs(lambda_witness(kind, 3000) - lambda_closed_form(kind, 3000))) < 1e-9

def test_witnesses_satisfy_zeta_type_functional_equation():
    """Lambda(s) = q^(s/2) pi^(-s/2) Gamma(s/2) P(s) zeta(s) est invariante par s -> 1 - s (q = 6 pour F6, 4 pour E2)."""
    import cmath
    from scipy.special import loggamma
    from zero_reconstruction import hurwitz_zeta
    P6 = lambda s: 1 + 6 ** (0.5 - s)
    P2 = lambda s: (1 - 2 ** (0.8 - s)) * (1 - 2 ** (0.2 - s))
    def Lam(s, q, P):
        return cmath.exp((s / 2) * math.log(q / math.pi) + loggamma(s / 2)) * P(s) * hurwitz_zeta(s, 1.0)
    for q, P in ((6, P6), (4, P2)):
        for s in (0.3 + 7j, 0.7 + 12.5j, 1.4 + 3.1j):
            assert abs(Lam(s, q, P) - Lam(1 - s, q, P)) / abs(Lam(s, q, P)) < 1e-10

def test_generic_compression_reproduces_dual_lock_for_zeta():
    from lock_witnesses import compression_from_lambda, lambda_witness
    from dual_lock import compression_accurate
    _, M0 = compression_accurate(20.0, "zeta", half_width=2.5, dimension=3, frequency_step=0.6)
    _, M1 = compression_from_lambda(20.0, lambda_witness("zeta", 200), q=1, parity=0, pole=True, dimension=3)
    assert np.max(np.abs(M0 - M1)) < 1e-12

def test_witness_prime_side_equals_zero_side_live():
    """Recalcul direct d'une fenêtre pour chaque témoin (pas seulement lecture du CSV)."""
    from lock_witnesses import SPECS, lambda_witness, compression_from_lambda, polynomial_zero_gammas, zero_side
    from explicit_formula import load_zeros
    gam, _ = load_zeros(); gz = np.concatenate([gam, -gam]).astype(complex)
    for kind, T, sign in (("F6", 31.0, +1), ("E2", 27.0, -1)):
        sp = SPECS[kind]
        fr, M = compression_from_lambda(T, lambda_witness(kind, 400), q=sp["q"], parity=sp["parity"], pole=sp["pole"], dimension=3)
        pz = polynomial_zero_gammas(kind, 20000.0)
        Z = zero_side(fr, 2.5, np.concatenate([gz, pz["on"].astype(complex), pz["off"]]))
        assert np.linalg.norm(M - Z) / np.linalg.norm(Z) < 1e-7
        assert sign * np.linalg.eigvalsh(M)[0] > 0

def test_four_corners_local_lock_and_global_sign_are_independent():
    t = {r["objet"]: r for r in _rows("lock_independence_table.csv")}
    f = lambda k, c: float(t[k][c])
    assert f("F6", "fuite_hors_pk") > 0.01 and f("F6", "defaut_multiplicatif") > 0.01 and f("F6", "lamG_min_fenetres_testees") > 0
    assert f("E2", "fuite_hors_pk") < 1e-20 and f("E2", "defaut_multiplicatif") < 1e-20 and f("E2", "lamG_min_fenetres_testees") < -1
    assert f("zeta", "fuite_hors_pk") < 1e-20 and f("zeta", "lamG_min_fenetres_testees") > 0
    assert f("DH", "fuite_hors_pk") > 0.5 and f("DH", "lamG_min_fenetres_testees") < -1
    assert all(float(r["ecart_rel"]) < 1e-7 for r in _rows("lock_independence_audit.csv"))

def test_numpy_evaluator_against_known_values_and_zero_lists():
    from zero_reconstruction import hurwitz_zeta, F_eval, regular_part_at_zero, nontrivial_zeros
    from explicit_formula import load_zeros
    assert abs(hurwitz_zeta(2, 1.0) - math.pi ** 2 / 6) < 1e-13 and abs(hurwitz_zeta(-1, 1.0) + 1 / 12) < 1e-13
    g, c0 = load_zeros()
    for k in (0, 50, 299):
        a, res = regular_part_at_zero("zeta", 0.5 + 1j * g[k])
        assert res < 1e-10 and abs(a + c0[k]) < 1e-9
    for kind in ("L_chi5", "DH"):
        z = nontrivial_zeros(kind)
        assert max(abs(F_eval(kind, w)) for w in z[::25]) < 1e-9

def test_tomo_signal_is_reconstructed_from_zeros_alone():
    rows = _rows("tomo_zero_reconciliation.csv")
    assert {r["objet"] for r in rows} == {"zeta", "L_chi5", "DH"}
    for r in rows:
        assert float(r["ecart_rel_L2"]) < 1e-6
        assert abs(float(r["entropie_TOMO2_coefficients"]) - float(r["entropie_TOMO2_zeros"])) < 1e-6

def test_tomo_reconstruction_live_small_case():
    from zero_reconstruction import zero_terms, g_from_zeros, g_from_coefficients, coefficients_c
    u = np.linspace(2.0, math.log(2000.0), 200)
    gc = g_from_coefficients(coefficients_c("zeta", 2600), u, 0.04)
    gz = g_from_zeros(zero_terms("zeta"), u, 0.04)
    assert np.linalg.norm(gc - gz) / np.linalg.norm(gc) < 1e-8

def test_dh_offline_zeros_carry_the_entropy_excess_over_L():
    a = [r for r in _rows("tomo_zero_attribution_DH.csv") if abs(float(r["sigma"]) - 0.01) < 1e-9][0]
    L = [r for r in _rows("tomo_zero_reconciliation.csv") if r["objet"] == "L_chi5" and abs(float(r["sigma"]) - 0.01) < 1e-9][0]
    assert float(a["entropie_TOMO2_tous_zeros"]) > float(L["entropie_TOMO2_zeros"]) > float(a["entropie_TOMO2_sans_hors_droite"])

def test_zero_lists_are_complete_by_argument_principle():
    for name, col in (("dh_zero_count_audit.csv", "dans_la_liste"), ("zeros_600_count_audit.csv", "zeros_trouves")):
        rows = _rows(name)
        assert len(rows) >= 10 and all(int(r["comptage_argument"]) == int(r[col]) for r in rows)
    ts = [float(r["t"]) for r in _rows("dh_zeros.csv")]
    assert any(abs(t - 5.0941598) < 1e-5 for t in ts) and any(abs(t - 8.9399144) < 1e-5 for t in ts)

def test_argument_principle_live_low_band():
    sys.path.insert(0, str(ROOT / "scripts"))
    from audit_dh_zero_count import winding
    w, _ = winding("DH", -0.9, 4.0, 0.25, 12.5, h=0.01)
    assert round(w) == 3 and abs(w - round(w)) < 1e-6

def test_zero_differences_avoid_zeta_zeros_for_euler_products_more_than_for_DH():
    rows = [r for r in _rows("zero_difference_resonances.csv") if abs(float(r["delta"]) - 0.15) < 1e-9]
    get = lambda key: [r for r in rows if r["experience"].startswith(key)][0]
    z, L, DH = get("zeta :"), get("L(chi5), t > 0"), get("DH sur la droite, t > 0")
    assert float(z["rapport"]) < 0.8 and float(L["rapport"]) < 0.9
    gap = float(DH["rapport"]) - float(L["rapport"])
    assert gap > 5 * math.hypot(float(DH["incertitude"]), float(L["incertitude"]))
    for r in rows:
        if r["experience"].startswith("témoin"):
            assert abs(float(r["ecart_en_sigma"])) < 3.5

def test_dip_width_is_compatible_with_one_half_and_excludes_0_3():
    """V6.3e : la demi-largeur du creux (attendue 1 - beta = 0,5) reste dans [0,35 ; 0,70] pour tous les réglages,
    et une largeur imposée de 0,3 ajuste toujours moins bien que 0,5 pour zeta et L(chi5)."""
    rows = _rows("zero_difference_dip_width.csv")
    assert len(rows) == 18
    for r in rows:
        assert 0.35 < float(r["largeur"]) < 0.70
        if r["objet"] in ("zeta", "L_chi5"):
            assert float(r["chi2_largeur_0_3"]) > float(r["chi2_largeur_0_5"])

def test_full_dip_model_agrees_for_L_and_not_for_zeta():
    """V6.3e : avec le profil sommé sur les zéros voisins, L(chi5) donne w proche de 0,5 ; zeta donne w nettement plus grand."""
    rows = _rows("zero_difference_width.csv")
    assert len(rows) == 9
    for r in rows:
        w = float(r["largeur_w"])
        if r["objet"] == "L_chi5":
            assert abs(w - 0.5) < 0.1 and abs(float(r["amplitude_A"]) / float(r["amplitude_attendue"]) - 1) < 0.25
        if r["objet"] == "zeta":
            assert 0.6 < w < 0.8 and float(r["chi2_si_w_0.5"]) > float(r["chi2_par_ddl"])

def test_zeta_dip_width_falls_to_one_half_with_height():
    """V6.3f : liste de zéros de zeta jusqu'à t = 1500 complète ; la demi-largeur du creux descend avec la hauteur
    et rejoint 0,5 (largeur et amplitude) dans la tranche la plus haute."""
    audit = _rows("zeta_zeros_1500_count_audit.csv"); zeros = _rows("zeta_zeros_1500.csv")
    assert len(audit) == 75 and all(int(r["comptage_argument"]) == int(r["zeros_trouves"]) for r in audit)
    assert len(zeros) == sum(int(r["zeros_trouves"]) for r in audit) == 1070
    assert all(abs(float(r["sigma"]) - 0.5) < 1e-9 for r in zeros)
    tr = [r for r in _rows("zero_difference_width_heights.csv") if r["role"] == "tranche" and r["objet"] == "zeta"]
    w = [float(r["largeur_w"]) for r in tr]
    assert len(tr) == 5 and w[0] - w[-1] > 0.1 and all(a >= b - 0.02 for a, b in zip(w[:-1], w[1:]))
    top = tr[-1]
    assert abs(float(top["largeur_w"]) - 0.5) < 2 * float(top["incertitude_w"])
    assert abs(float(top["amplitude_A"]) / float(top["amplitude_attendue"]) - 1) < 0.25

def test_bohr_closure_is_the_multiplicative_defect():
    for r in _rows("tomo3_bohr_closure.csv"):
        assert abs(float(r["defaut_de_fermeture_mesure"]) - float(r["defaut_multiplicatif_des_coefficients"])) < 1e-3   # fenêtre finie : coefficients de Bohr à 5e-5 près

if __name__ == "__main__":
    n = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); n += 1; print("OK  ", name)
    print(f"{n}/{n}")
