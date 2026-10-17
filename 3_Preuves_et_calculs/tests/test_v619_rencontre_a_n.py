"""V6.19 — La Rencontre à n (identité marge = corrélation à n points) et la matrice des théories."""
from __future__ import annotations
import importlib.util, json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
CALC = ROOT / "3_Preuves_et_calculs"

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def test_marge_d_un_n_uplet_est_la_correlation_a_n_points():
    R = _load("run_rencontre_a_n", CALC / "scripts" / "run_rencontre_a_n.py")
    rng = np.random.default_rng(19)
    for n in range(2, 6):
        for _ in range(40):
            N = int(rng.integers(n, 30)); th = rng.uniform(0, 2 * np.pi, n)
            assert abs(R.gram_margin(th, N) - R.kernel_det(th, N)) < 1e-12
    # trois points : formule fermée du noyau sinus = déterminant 3 × 3
    x, y = 0.37, 0.81; s = np.array([0, x, x + y])
    K = R.sinc(np.pi * np.subtract.outer(s, s))
    assert abs(np.linalg.det(K) - R.R3(x, y)) < 1e-12
    # loi de superposition : une seule famille (f = 1) redonne R3
    assert abs(R.R3_melange(1.0)(x, y) - R.R3(x, y)) < 1e-12

def test_resultats_et_previsions_v619():
    rep = json.loads((CALC / "data" / "rencontre_a_n.json").read_text(encoding="utf-8-sig"))
    assert rep["P1_ecart_max_identite"] < 1e-12
    z = rep["zeta"]; assert z["chi2_reduit_R3"] <= 2 and z["chi2_reduit_Poisson"] >= 5
    assert z["masse_zone_obs"] <= z["masse_zone_R2R2"] / 3
    m = rep["zeta_L_chi5"]; assert m["chi2_reduit_melange"] < m["chi2_reduit_R3"]
    assert (CALC / "data" / "prevision_v619.md").exists()

def test_matrice_des_theories_coherente():
    M = _load("build_matrice", ROOT / "2_Methode" / "Matrice" / "build_matrice.py")
    mat, S = M.load()
    assert M.check(mat, S) == []
    C = M.cells(mat)
    assert C[("WEIL", "NB")][0] == "⇔" and C[("WEIL", "NB")][2]          # déduite par RH
    assert C[("WEIL", "LI")][0] == "⇔" and not C[("WEIL", "LI")][2]      # écrite et sourcée en V6.29 [BL99]
    assert C[("RH", "LH")][0] == "⇒" and C[("LH", "RH")][0] == "⇐"
    page = (ROOT / "1_Presentation" / "44_MATRICE_DES_THEORIES.html").read_text(encoding="utf-8-sig")
    assert "à compléter" in page and all(f"data-n='{n['id']}'" in page for n in mat["noeuds"])

def test_matrice_provenance_et_liens_v6191():
    M = _load("build_matrice2", ROOT / "2_Methode" / "Matrice" / "build_matrice.py")
    mat, S = M.load()
    assert {n["apport"] for n in mat["noeuds"]} >= {"litterature", "recalcule", "nouveau"}
    page = (ROOT / "1_Presentation" / "44_MATRICE_DES_THEORIES.html").read_text(encoding="utf-8-sig")
    assert "class='art'" in page and "p-recalcule" in page and "p-nouveau" in page and 'data-mode="prov"' in page
