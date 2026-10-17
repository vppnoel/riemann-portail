"""V6.23 — Axe J5 : le Frobenius qui n'est pas un morphisme."""
from __future__ import annotations
import importlib.util, json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]; CALC = ROOT / "3_Preuves_et_calculs"

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def test_petite_construction():
    F = _load("fng", CALC / "scripts" / "run_frobenius_non_geometrique.py")
    p = 31; phis = {"Frobenius x^p": np.array([0] * p + [1], dtype=np.int64), "identité x": np.array([0, 1], dtype=np.int64)}
    r = F.experiment(p, [1, 1, 0, 1], 3, 4, 2, phis)
    assert r["Frobenius x^p"]["fonctions_auxiliaires"] > r["identité x"]["fonctions_auxiliaires"] == 0
    assert F.rank_mod(np.array([[1, 2], [2, 4]], dtype=np.int64), 7) == 1

def test_resultats_v623():
    R = json.loads((CALC / "data" / "frobenius_non_geometrique.json").read_text(encoding="utf-8-sig"))
    assert sum(r["Frobenius x^p"]["fonctions_auxiliaires"] > 0 for r in R) >= 10
    assert all(r["identité x"]["fonctions_auxiliaires"] == 0 for r in R)
    assert sum(r["permutation aléatoire"]["fonctions_auxiliaires"] == 0 for r in R) >= 10
    assert (CALC / "data" / "prevision_v623_frobenius.md").exists()
