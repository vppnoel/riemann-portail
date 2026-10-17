"""V6.27 — J6 : le carré, en continu."""
from __future__ import annotations
import json
from pathlib import Path

CALC = Path(__file__).resolve().parents[1]

def test_resultats_v627():
    rep = json.loads((CALC / "data" / "carre_continu.json").read_text(encoding="utf-8-sig"))
    assert rep["fiables"] == rep["reglages"] == 180
    assert rep["zeta_une_seule_positive"] == rep["zeta_fiables"] == 60 and rep["L_sans_positive"] == rep["L_fiables"] == 60
    assert rep["DH_en_trop_des_X61"] == rep["DH_X_ge_61"] > 0
    assert (CALC / "data" / "prevision_v627_carre.md").exists()
