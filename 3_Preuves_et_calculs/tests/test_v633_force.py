"""V6.33 — Défaut de multiplicativité sur la carte de V_7 impair."""
from __future__ import annotations
import importlib.util, json
from pathlib import Path
import numpy as np

CALC = Path(__file__).resolve().parents[1]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def test_force_v633():
    import sys; sys.path.insert(0, str(CALC / "src"))
    F = _load("rh633", CALC / "scripts" / "run_force_multiplicativite.py")
    assert F.defect(np.eye(3)).max() < 1e-20                                   # nul aux points d'Euler
    assert F.defect(np.array([[1.0, 1.0, 0.0]]) / np.sqrt(2))[0] > 0.1           # positif ailleurs
    rep = json.loads((CALC / "data" / "force_multiplicativite.json").read_text(encoding="utf-8-sig"))
    assert rep["D1_spearman_T_D"] > -0.6 and rep["D2_partielle_T_D_sachant_d"] > 0.2 and rep["D3_part_sous_la_mediane"] < 0.5   # prévisions fausses
    ex = rep["exploratoire_apres_coup"]; assert ex["partielle_T_A1_sachant_d"] > 0.7 and ex["partielle_T_D_sachant_d_et_A1"] < 0
    assert (CALC / "data" / "prevision_v633_force.md").exists()
