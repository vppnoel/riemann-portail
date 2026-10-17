"""V6.10 — tests du générateur des premiers : l'opérateur de translation de ζ reconstruit sans aucun zéro."""
import math, sys
from pathlib import Path
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
D = ROOT / "data"

def test_primes_give_zeta_operator_live():
    from prime_generator import traces_from_primes, traces_from_zeros, metric_and_generator, g_hat
    from rejection import coeffs, log_derivative_coeffs
    a, h, N = 0.2, 0.05, 100
    c = log_derivative_coeffs(coeffs("zeta", 300))
    t = traces_from_primes("zeta", c, N, h, a)                            # nombres premiers <= 223, aucun zéro
    gz = pd.read_csv(D / "zeta_zeros_1500.csv").t.values
    assert np.max(np.abs(t - traces_from_zeros(np.concatenate([gz, -gz]).astype(complex), N, h, a))) < 1e-12
    r = metric_and_generator(t, N, h)
    k = np.argmin(np.abs(r["gamma"] - 14.134725141734693))
    assert abs(r["gamma"][k] - 14.134725141734693) < 1e-8 and abs(r["weight"][k] / g_hat(r["gamma"][k], a) - 1) < 1e-6
    assert r["negatives"] == 0

def test_dh_off_line_zero_and_negative_metric_live():
    from prime_generator import traces_from_primes, metric_and_generator, g_hat
    from rejection import coeffs, log_derivative_coeffs
    a, h, N = 0.08, 0.02, 300
    c = log_derivative_coeffs(coeffs("DH", 500))
    r = metric_and_generator(traces_from_primes("DH", c, N, h, a), N, h)
    assert r["negatives"] == 4                                            # quadruplets 85,7 et 114,2
    for target in (85.699348 - 0.308517j, 85.699348 + 0.308517j):
        k = np.argmin(np.abs(r["gamma"] - target)); assert abs(r["gamma"][k] - target) < 1e-5
        assert abs(r["weight"][k] / g_hat(r["gamma"][k], a) - 1) < 1e-4

def test_summary_metric_attribution_and_convergence():
    s = pd.read_csv(D / "generator_summary.csv").set_index("objet")
    assert list(s.negatifs[["zeta", "L_chi5", "DH"]]) == [0, 0, 10]
    assert (s.vraies_fausses == 0).all() and (s.ecart_max_vraies < 1e-2).all() and (s.audit_premiers_zeros < 1e-9).all()
    assert s.loc["DH", "hors_droite_retrouves"] == 16
    m = pd.read_csv(D / "generator_dh_metric.csv")
    assert (m.negatifs_zeros_sur_droite == 0).all()                       # zéros sur la droite seuls : métrique positive
    for _, r in m.iterrows():                                             # chaque direction négative vient d'un quadruplet hors droite
        assert any(r.negatifs_premiers == r[f"negatifs_{k}_quadruplets"] for k in range(1, 7)) and r.negatifs_premiers % 2 == 0
    c = pd.read_csv(D / "generator_convergence.csv"); z = c[(c.objet == "zeta") & (c.N == 1000)].iloc[0]
    assert z.vraies_justes == 284 and z.vraies_fausses == 0 and z.ecart_max < 2e-4

def test_step_folds_zeros():
    e = pd.read_csv(D / "generator_step.csv")
    small, large = e.iloc[0], e[np.isclose(e.h, 0.2)].iloc[0]
    assert small.vraies_sans_repliement >= 80 and large.vraies_sans_repliement == 0 and large.zeros_dans_la_bande == 2
