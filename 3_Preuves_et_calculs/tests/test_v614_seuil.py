"""V6.14 — la loi de seuil : signe des innovations fragile, critère des valeurs propres, temps de Heisenberg, lemme d'inertie."""
import math, sys
from pathlib import Path
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
D = ROOT / "data"

def _traces(gam, w, N, h):
    k = np.arange(N + 1); return (np.asarray(w)[None, :] * np.exp(1j * np.outer(k * h, np.asarray(gam, dtype=complex)))).sum(1)

def _quad(g0, d):
    return np.array([g0 - 1j * d, g0 + 1j * d, -g0 - 1j * d, -g0 + 1j * d])

def test_innovation_sign_is_fragile_eigenvalue_criterion_is_not():
    from prime_generator import g_hat, levinson, lmin_ratio, first_negative_size
    from zero_reconstruction import nontrivial_zeros
    z = -1j * (nontrivial_zeros("DH") - 0.5); on = z[np.abs(z.imag) < 1e-6].real       # fond de DH sur la droite : G >= 0 exactement
    t = _traces(on, g_hat(on, 0.04), 400, 0.01); K, E = levinson(t, 400)
    assert E[295] / E[0] < -1e-3 and lmin_ratio(t, 296) > -1e-14       # innovation « négative » de 2e-3 ; aucune valeur propre négative
    assert first_negative_size(t, 1e-10, 401) is None

def test_prime_thresholds_and_heisenberg_law_live():
    from prime_generator import traces_from_primes, g_hat, first_negative_size, heisenberg_length
    from rejection import coeffs, log_derivative_coeffs
    a, h, N = 0.04, 0.01, 520
    tb = {k: traces_from_primes(k, log_derivative_coeffs(coeffs(k, 20000)), N, h, a) for k in ("zeta", "L_chi5", "DH")}
    assert first_negative_size(tb["DH"], 1e-10, N + 1) == 354                                  # DH par les premiers : fenêtre 3,53
    assert first_negative_size(tb["zeta"], 1e-10, N + 1) is None and first_negative_size(tb["L_chi5"], 1e-10, N + 1) is None
    Lc = {}
    for k, g0, q in (("zeta", 100.0745, 1), ("L_chi5", 99.7970, 5)):                           # quadruplet synthétique entre deux zéros
        qq = _quad(g0, 0.2); n = first_negative_size(tb[k] + _traces(qq, g_hat(qq, a), N, h), 1e-10, N + 1)
        Lc[k] = (n - 1) * h; assert 0.9 < Lc[k] / heisenberg_length(q, g0) < 1.12
    assert abs(Lc["L_chi5"] / Lc["zeta"] - math.log(5 * 99.797 / (2 * math.pi)) / math.log(100.0745 / (2 * math.pi))) < 0.15   # le conducteur compte

def test_inertia_lemma_and_recorded_law():
    ine = pd.read_csv(D / "seuil_inertie.csv")
    assert (ine.negatives_directes == ine.negatives_par_le_lemme).all() and ine.negatives_directes.max() == 2 and (ine.ecart_reconstruction < 1e-12).all()
    s = pd.read_csv(D / "seuil_synthetiques.csv"); hz = s[(s.experience == "hauteur") & (s.hauteur <= 210)]
    assert len(hz) == 13 and hz.rapport.between(0.9, 1.1).all()                                 # ζ et L, hauteurs 20 à 200
    r = pd.read_csv(D / "seuil_reels.csv").dropna(subset=["L_H"]); assert len(r) == 5 and (r.L_c / r.L_H).between(0.78, 0.92).all()
    p = pd.read_csv(D / "seuil_precision.csv").set_index(["hauteur", "chiffres"])
    assert p.loc[(p.index.get_level_values(0).max(), 80), "L_exact"] == 4.08 and p.loc[(p.index.get_level_values(0).max(), 30), "L_exact"] != 4.08
