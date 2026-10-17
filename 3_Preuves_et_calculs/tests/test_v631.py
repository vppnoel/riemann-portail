"""V6.31 — Relief de l'archipel, formules de la matrice, liste des figures, fichiers de publication."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np, pandas as pd

CALC = Path(__file__).resolve().parents[1]; ROOT = CALC.parent


def test_v631():
    rep = json.loads((CALC / "data" / "archipel_relief.json").read_text(encoding="utf-8-sig"))
    p = rep["critere_persistant"]
    assert set(p["cols"].values()) == {144} and abs(p["part_au_dessus"]["300"] - 0.0102) < 0.001
    assert rep["part_des_points_a_deficit_transitoire"] > 0.7
    r = pd.read_csv(CALC / "data" / "archipel_relief.csv"); assert len(r) == 141 * 141
    M = json.loads((ROOT / "2_Methode" / "Matrice" / "matrice_theories.json").read_text(encoding="utf-8-sig"))
    assert all(n.get("formule") and "<math" in n.get("formule_mathml", "") for n in M["noeuds"])
    page = (ROOT / "1_Presentation" / "44_MATRICE_DES_THEORIES.html").read_text(encoding="utf-8-sig")
    assert "mx-pop" in page and "<math" in page
    figs = (ROOT / "00_Liste_des_figures.html").read_text(encoding="utf-8-sig")
    assert all(f.name in figs for f in (ROOT / "1_Presentation").glob("*.png"))
    for f in ("LICENSE", "LICENSE-CC-BY-4.0.md", "CITATION.cff", "requirements.txt", ".gitignore"):
        assert (ROOT / f).exists()
    assert (CALC / "data" / "prevision_v631_relief.md").exists()
