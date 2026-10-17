"""V6.28 — Axe A : la Rencontre à n en hauteur."""
from __future__ import annotations
import importlib.util, json
from pathlib import Path
import numpy as np

CALC = Path(__file__).resolve().parents[1]

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def test_formule_et_resultats_v628():
    H = _load("rh628", CALC / "scripts" / "run_rencontre_hauteur.py")
    s = np.array([0.3]); assert abs(H.DN(s, 1000.0)[0] - np.sin(np.pi * 0.3) / (np.pi * 0.3)) < 1e-6   # N grand : noyau sinus
    rep = json.loads((CALC / "data" / "rencontre_hauteur.json").read_text(encoding="utf-8-sig"))
    assert rep["A1"]["attendu_N_eff"] < 0                                                       # densité négative : modèle invalide
    z = rep["portees"][0]; assert z["triples_lt1"] == 0 and z["attendu_sinus"] > 15
    assert all(abs(c["fraction_triples_lt1"] - 0.0146) < 0.002 for c in rep["CUE"])
    assert (CALC / "data" / "prevision_v628_hauteur.md").exists()
