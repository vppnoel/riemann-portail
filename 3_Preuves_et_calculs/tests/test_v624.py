"""V6.24 — J3 simplifié et le même calcul que les deux tiers."""
from __future__ import annotations
import importlib.util, json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]; CALC = ROOT / "3_Preuves_et_calculs"

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def test_rang_trace_et_theorie():
    V = _load("v624", CALC / "scripts" / "run_v624.py")
    d, s = V.rank_trace(np.arange(200, dtype=float), 1.0)          # points régulièrement espacés : aucun voisin dans la fenêtre
    assert d > 0.99 and abs(s - (2 * d - 1)) < 1e-12
    dt, st = V.theory(1.0); assert 0.74 < dt < 0.76

def test_resultats_v624():
    R = json.loads((CALC / "data" / "v624.json").read_text(encoding="utf-8-sig"))
    B = {r["A"]: r for r in R["B"]}
    assert B[1.0]["zeta_simples"] > B[1.0]["melange_simples"] and B[4.0]["zeta_distincts"] > 0.95
    a = R["A"][-1]; assert a["x^p + x (additif, dérivée 1)"]["fonctions_auxiliaires"] == a["x^p (additif, dérivée nulle)"]["fonctions_auxiliaires"] > 0
    assert (CALC / "data" / "prevision_v624.md").exists()
