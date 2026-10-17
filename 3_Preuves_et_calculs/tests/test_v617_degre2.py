"""V6.17 — la Rencontre en degré 2 (Contour tourné, trois identités, mesures) et son pendant dans le Modèle réduit."""
import importlib.util, math
from pathlib import Path
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]; R2 = ROOT.parent
D = ROOT / "data"

def _mod(name, rel):
    spec = importlib.util.spec_from_file_location(name, R2 / rel); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def test_rotated_contour_matches_mpmath_and_zeros_are_complete():
    from delta_contour import DeltaBand, theta_delta
    from delta_ramanujan import tau, Lambda_delta_mp
    T = tau(400); taus = np.array([float(x) for x in T])
    for t in (17.0, 61.5):                                  # identité exacte Λ(6+it) = 2 e^{-φt} Re(e^{6iφ} A), contre la série gamma incomplète
        v = DeltaBand(taus, t - 5, t + 5).Lambda(t)[0]; m = float(Lambda_delta_mp(t, T[:int(t) + 200], dps=int(math.pi * t / 2 / math.log(10)) + 30))
        assert abs(v - m) < 1e-11 * abs(m)
    g = pd.read_csv(D / "delta_zeros_contour.csv").gamma.values; assert len(g) == 2139 and np.all(np.diff(g) > 0.05)
    m13 = pd.read_csv(D / "delta_zeros_mpmath.csv").gamma.values; assert np.abs(g[:len(m13)] - m13).max() < 1e-9
    mid = 0.5 * (g[:-1] + g[1:]); S = np.arange(1, len(g)) - theta_delta(mid) / math.pi      # complétude (Turing) : S borné, de moyenne nulle
    assert np.abs(S).max() < 1 and abs(S.mean()) < 0.01
    old = pd.read_csv(D / "delta_zeros_premiers.csv").gamma.values                       # correctif V6.15 : 7 zéros manqués près de 232
    assert (g <= 232.08).sum() == 196 and len(old) == 189 and old.max() < 232.08

def test_three_identities():
    rng = np.random.default_rng(617)
    for N in (2, 3, 6, 11):                                  # det de la métrique = densité de Weyl ; marge d'une paire = R2 du CUE(N)
        th = rng.uniform(-math.pi, math.pi, N); j = np.arange(N)
        G = np.exp(1j * np.subtract.outer(j, j)[:, :, None] * th[None, None, :]).sum(axis=2); e = np.exp(1j * th)
        weyl = np.prod([abs(e[a] - e[b]) ** 2 for a in range(N) for b in range(a + 1, N)])
        assert abs(np.linalg.det(G).real - weyl) < 1e-9 * max(1, weyl)
        d = abs(th[0] - th[1]); s = N * d / (2 * math.pi)
        pair = 1 - (abs(np.exp(1j * j * d).sum()) / N) ** 2
        assert abs(pair - (1 - (math.sin(math.pi * s) / (N * math.sin(math.pi * s / N))) ** 2)) < 1e-12
    s = 0.37; big = 4000; d = 2 * math.pi * s / big                                      # N → ∞ : 1 − sinc²(πs) (document 40)
    assert abs((1 - (abs(np.exp(1j * np.arange(big) * d).sum()) / big) ** 2) - (1 - (math.sin(math.pi * s) / (math.pi * s)) ** 2)) < 1e-6
    for th in rng.uniform(0, math.pi, 5):                     # paire conjuguée : det/4 = 1 − λ²/4 = sin²θ
        lam = 2 * math.cos(th); assert abs(np.linalg.det(np.array([[2, lam], [lam, 2]])) / 4 - math.sin(th) ** 2) < 1e-12

def test_recorded_measurements():
    r = pd.read_csv(D / "degre2_resume.csv").iloc[0]
    assert r.delta_zeros == 2139 and r.delta_k_f01 == 8 and r.delta_f01 < r.poisson_f01 / 10            # P1
    assert abs(r.cue200_f01 - 0.01225) < 1e-6 and r.delta_rapport_f01 < 0.5                             # P2 fausse au seuil 0,1
    assert 0.14 <= r.zetaK_f01 <= 0.20 and r.zetaK_part_mixtes_f01 >= 0.9 and r.zetaK_distance_min_croisee > 1e-6   # P3
    assert abs(r.satake_f01 / r.sato_tate_f01 - 1) < 0.3 and r.satake_f01 < r.uniforme_f01 / 10 and r.satake_marge_min > 0 and r.satake_ks_p > 0.01   # P4
    assert r.satake_lambda_max <= 2 and abs(r.satake_moment2 - 1) < 0.02
    assert abs(r.courbes_f01 / r.sato_tate_f01 - 1) < 0.3 and r.courbes_marge_min > 0 and r.courbes_collisions_etage2 == r.courbes_supersing == 18338   # P5
    pp = pd.read_csv(D / "degre2_courbes_par_p.csv"); assert pp.hasse_ok.all() and (pp.rho2_max == 1).all()
    assert (np.abs(pp.moment2 - 1) < 1e-3).all() and (np.abs(pp.moment4 - 2) < 1e-3).all() and (np.abs(pp.moment6 - 5) < 2e-3).all()
    assert r.mr_courbes == 425 == r.mr_rh and r.mr_ecart_identite_max < 1e-10 and r.mr_collisions == 1 and r.mr_faux_jumeaux_marge_negative == 220

def test_indicator_and_navigator_v617():
    bi = _mod("bi", "2_Methode/Indicateur/build_indicateur.py"); d = bi.load(); assert bi.check_links(d) == []
    e = next(x for x in d["etapes"] if x["id"] == "v617"); assert e["niveaux"]["degre2"] == 4 and e["niveaux"]["croiser"] == 6
    ids = {x["id"] for x in d["croisements"]}; assert {"rencontre_degre2", "rencontre_locale", "familles_etrangeres"} <= ids
    _, zones = bi.crossings(d, True)
    assert not any("Simplicité × Degré 2" in z or "Répulsion × Degré 2" in z for z in zones) and any("Degré 2" in z for z in zones)
    bn = _mod("bn", "2_Methode/Navigateur/build_navigateur.py"); carte, ind, ops = bn.load(); assert bn.check(carte, ops, ind) == []
    M = {m["id"]: m for m in carte["coups"]}
    assert M["repulsion_degre2"]["statut"] == M["rencontre_modele_reduit"]["statut"] == "fait"
    assert {"Le Contour tourné", "La Loi de la marge", "Les Familles étrangères"} <= set(ops)
