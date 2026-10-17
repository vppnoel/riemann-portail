"""V6.15 — Δ de Ramanujan (degré 2) et recensement des quadruplets de DH par la métrique des premiers."""
import math, sys
from pathlib import Path
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
D = ROOT / "data"

def test_tau_exact():
    from delta_ramanujan import tau, MODULI
    from sympy import isprime, primerange
    assert all(isprime(m) for m in MODULI)
    T = tau(600)
    assert T[1:12] == [1, -24, 252, -1472, 4830, -6048, -16744, 84480, -113643, -115920, 534612] and T[23] == 18643272
    assert all(T[p * p] == T[p] ** 2 - p ** 11 for p in primerange(2, 25))                      # relation de Hecke
    assert all(abs(T[p]) <= 2 * p ** 5.5 for p in primerange(2, 600))                             # borne de Deligne

def test_delta_from_primes_live():
    from delta_ramanujan import tau, delta_coeffs, traces_delta, Lambda_delta_mp
    from rejection import log_derivative_coeffs
    from prime_generator import g_hat, first_negative_size
    zm = pd.read_csv(D / "delta_zeros_mpmath.csv").gamma.values; assert len(zm) == 13 and abs(zm[0] - 9.2223794) < 1e-6
    T = tau(60); assert Lambda_delta_mp(9.20, T, 30) * Lambda_delta_mp(9.25, T, 30) < 0      # changement de signe au premier zéro
    c = log_derivative_coeffs(delta_coeffs(400)); a, h, N = 0.5, 0.05, 40
    tp = traces_delta(c, N, h, a); zz = np.concatenate([zm, -zm])
    tz = np.array([np.sum(g_hat(zz, a) * np.exp(1j * zz * k * h)) for k in range(N + 1)])
    assert np.max(np.abs(tp - tz)) / abs(tz[0]) < 1e-6                                           # formule explicite : premiers = zéros
    t = traces_delta(c, 300, 0.01, 0.04); assert first_negative_size(t, 1e-10, 301) is None      # métrique positive (pas de zéro hors droite vu)

def test_degree2_heisenberg_recorded():
    d = pd.read_csv(D / "delta_heisenberg.csv"); d = d[d.delta.isna()] if "delta" in d else d
    dl = d[d.objet == "L(Δ, s)"].sort_values("hauteur_visee"); z = d[d.objet == "ζ"].sort_values("hauteur_visee")
    assert len(dl) == 5 and dl.rapport.between(0.9, 1.15).all()                                   # P1
    r = dl.L_c.values / z.L_c.values; assert (np.abs(r - 2) < 0.3).all()                          # P2 : la longueur double
    w = pd.read_csv(D / "delta_weyl.csv"); assert (np.abs(w.comptes - w.weyl) < 2).all()
    m = pd.read_csv(D / "delta_zeros_mpmath.csv"); assert np.max(np.abs(m.ecart_au_generateur)) < 1e-7

def test_census_recorded():
    rc = pd.read_csv(D / "hauteur_recensement.csv").set_index("cas").negatives
    assert rc["DH (premiers)"] == 50 and rc["L(s, χ5) (premiers), témoin"] == 0
    assert rc["DH sans les quadruplets ≤ 600"] == 20 and rc["DH sans les quadruplets ≤ 1700"] == 0  # chaque direction négative est attribuée
    al = pd.read_csv(D / "hauteur_allumage.csv"); lit = al.dropna(subset=["L_c"]); assert len(lit) == 25 and 2 * len(lit) == rc["DH (premiers)"]
    b = al[al.hauteur <= 600]; assert len(b) == 15 and b.rapport.between(0.74, 1.05).all() and (b.rapport.between(0.75, 1.05)).sum() == 14
    g = pd.read_csv(D / "hauteur_generateur.csv"); assert g[g.hauteur <= 600].retrouve.sum() == 14
    st = pd.read_csv(D / "hauteur_escalier.csv"); assert (np.diff(st.negatives_DH) >= 0).all() and (st.negatives_L == 0).all()
