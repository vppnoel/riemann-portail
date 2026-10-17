"""V6.22 — Axe J2 : le Riemann–Roch virtuel."""
from __future__ import annotations
import importlib.util, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]; CALC = ROOT / "3_Preuves_et_calculs"

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def test_contraintes_sur_deux_exemples():
    RR = _load("rr", CALC / "scripts" / "run_riemann_roch_virtuel.py")
    ok = RR.floors([1, 2, 3], 3, 1)                                # vraie courbe de genre 1 sur F_3
    assert all(v is None for v in ok.values())
    fake = RR.floors([1, -4, 3], 3, 1)                             # jumeau sans point : h = 0
    assert fake["E"] == 1 and fake["castelnuovo"] == 1
    assert RR.elem_from_power([None, 3, 5], 2) == [1, 3, 2]        # racines 1 et 2

def test_resultats_v622():
    rep = json.loads((CALC / "data" / "riemann_roch_virtuel.json").read_text(encoding="utf-8-sig"))
    assert rep["courbes_violant_E"] == rep["courbes_violant_C"] == rep["courbes_violant_S"] == rep["courbes_violant_tordu"] == 0
    assert rep["jumeaux_attrapes_C"] == 0 and rep["jumeaux_attrapes_S"] < rep["jumeaux"] == rep["jumeaux_attrapes_avec_tordu"] == 220
    assert rep["avec_tordu_avant_castelnuovo"] == 0
    assert (CALC / "data" / "prevision_v622_riemann_roch.md").exists()
