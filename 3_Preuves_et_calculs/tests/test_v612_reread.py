"""V6.12 — les trois idées rejetées relues : innovations de Levinson, fantôme pesé, Théorème A au rayon spectral."""
import math, sys
from pathlib import Path
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
D = ROOT / "data"

def test_levinson_live():
    from prime_generator import traces_from_primes, levinson, toeplitz_pencil
    from rejection import coeffs, log_derivative_coeffs
    a, h, N = 0.08, 0.02, 200
    for kind, expect_neg in (("zeta", False), ("DH", True)):
        t = traces_from_primes(kind, log_derivative_coeffs(coeffs(kind, 400)), N, h, a)
        K, E = levinson(t, N); rel = E / E[0]
        G, _ = toeplitz_pencil(t, 120); assert abs(np.prod(np.sign(rel[:120]))) == 1   # E_n = det G_{n+1} / det G_n : contrôle de cohérence
        neg = np.where(rel < -1e-7)[0]
        if expect_neg: assert 170 <= neg[0] <= 180                       # DH : première innovation négative, premiers <= 40 environ
        else: assert len(neg) == 0 and np.max(np.abs(K)) < 1               # ζ : |k_n| < 1, toutes les innovations positives

def test_reread_summaries():
    s = pd.read_csv(D / "reread_levinson_summary.csv").set_index("objet")
    assert s.loc["zeta", "premiere_innovation_negative_n"] == -1 and s.loc["L_chi5", "premiere_innovation_negative_n"] == -1
    assert s.loc["zeta", "reflexion_max_avant_horizon"] < 1 and s.loc["L_chi5", "reflexion_max_avant_horizon"] < 1
    assert s.loc["DH", "premiere_innovation_negative_n"] == 352 and s.loc["DH", "premiers"] == 36
    q = pd.read_csv(D / "reread_quadruplets.csv"); assert q.longueur_detection.between(3.4, 4.5).all() and len(q) == 5   # V6.14 : valeurs propres (2,7–3,5 en V6.12 : bruit)
    src = pd.read_csv(D / "reread_sources.csv")
    ph = src[(src.re > 73.5) & (src.re < 74.2)]; assert len(ph) >= 1 and (ph.masse < 1e-6).all()     # le fantôme ne pèse rien
    tz = src[(src.re - 74.324982).abs() < 1e-5]; assert len(tz) == 1 and abs(tz.masse.iloc[0] - 1) < 1e-6
    ta = pd.read_csv(D / "reread_theoremA.csv").set_index("objet")
    assert abs(ta.loc["DH", "exposant_generateur"] - 0.308517) < 1e-6 and ta.loc["zeta", "exposant_generateur"] < 1e-6 and ta.loc["L_chi5", "exposant_generateur"] < 1e-6
