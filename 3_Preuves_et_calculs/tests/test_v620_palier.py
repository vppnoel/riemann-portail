"""V6.20 — Le Palier 4/3 recalculé ; la matrice marque l'origine OpenAI et les redécouvertes."""
from __future__ import annotations
import importlib.util, json, math
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]; CALC = ROOT / "3_Preuves_et_calculs"

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def test_cribles_et_identite_du_palier():
    P = _load("palier", CALC / "scripts" / "run_palier_quatre_tiers.py")
    mu, lam = P.sieves(1000)
    assert list(mu[1:11]) == [1, -1, -1, 0, -1, 1, -1, 0, 0, 1] and abs(lam[8] - math.log(2)) < 1e-15 and lam[6] == 0
    c = P.c_arith(lam, 1000)
    n = np.arange(1, 1001); a = mu[1:].astype(float) * (np.log(n) ** 2 - 2 * P.G * np.log(n))
    c2 = np.zeros(1001)
    for d in range(1, 1001): c2[d::d] += a[d - 1]          # c = 1 * a
    assert np.max(np.abs(c[1:] - c2[1:])) < 1e-9

def test_resultats_v620():
    df = pd.read_csv(CALC / "data" / "palier_quatre_tiers.csv"); rep = json.loads((CALC / "data" / "palier_quatre_tiers.json").read_text(encoding="utf-8-sig"))
    r = df.set_index("N")
    assert abs(r.loc[100000, "total"] - 1.31496) < 2e-3                    # V5.6 retrouvée
    assert abs(r.loc[5000000, "r_Q"] - r.loc[5000000, "r_Q_modele"]) < 0.03 * r.loc[5000000, "r_Q"]
    b = rep["balayage"]; assert 0.95 < b["mediane_rapport"] < 1.0 and b["max_rapport"] > 2
    assert (CALC / "data" / "prevision_v620_palier.md").exists()

def test_matrice_openai_et_redecouvertes():
    M = _load("bm620", ROOT / "2_Methode" / "Matrice" / "build_matrice.py"); mat, S = M.load()
    assert M.check(mat, S) == []
    ids = {n["id"] for n in mat["noeuds"]}; assert {"TAMIS", "ARCH", "LHD"} <= ids
    assert any(n.get("origine", "").startswith("OpenAI") for n in mat["noeuds"]) and len(mat["redecouvertes"]) >= 10
    page = (ROOT / "1_Presentation" / "44_MATRICE_DES_THEORIES.html").read_text(encoding="utf-8-sig")
    assert "p-redecouvert" in page and " oa'" in page and "Ce que le programme a retrouvé" in page
    plan = (ROOT / "1_Presentation" / "43_PLAN_DE_RECHERCHE_LA_RENCONTRE_A_N.md").read_text(encoding="utf-8-sig")
    assert "### Axe H." in plan and "### Axe I." in plan and "4 bis" in plan
