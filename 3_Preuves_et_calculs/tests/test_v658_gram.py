"""V6.58 — D'où vient le signe : comptage, degré, ou carré (Modèle réduit)."""
from __future__ import annotations
import importlib.util, json
from pathlib import Path

CALC = Path(__file__).resolve().parents[1]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def test_trois_niveaux_v658():
    import sys; sys.path.insert(0, str(CALC / "src")); sys.path.insert(0, str(CALC / "scripts"))
    G = _load("rh658", CALC / "scripts" / "run_gram_modele_reduit.py")
    # faux jumeau de genre 1 : une « isogénie » de degré −1
    r = G.analyse([1, -4, 3], 3, 1)
    assert r["racines_reelles_impaires"] == 2 and r["B_neg"] == 1 and r["u_degre_negatif"]["N"] < 0
    # courbe sur la droite : B définie positive (q = 5, a = 2)
    assert G.analyse([1, -2, 5], 5, 1)["B_neg"] == 0
    rep = json.loads((CALC / "data" / "gram_modele_reduit.json").read_text(encoding="utf-8-sig"))
    assert rep["G1"]["B_sans_negatif"] == 425 and rep["G2"]["r4_sans_racine_reelle_impaire"] == 119
    assert rep["G3"]["r2_avec_u_trouve"] == 101 and rep["G4"]["B_neg_egal_r_sur_2"] == 220
    ldl = json.loads((CALC / "data" / "gram_ldl_exact.json").read_text(encoding="utf-8-sig"))
    assert ldl["courbes_2g_pivots_positifs"] == 424 and ldl["faux_pivot_negatif"] + ldl["faux_pivot_nul"] == 220
    assert (CALC / "data" / "prevision_v658_gram.md").exists()
