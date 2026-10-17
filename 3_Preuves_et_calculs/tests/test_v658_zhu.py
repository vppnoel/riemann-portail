"""V6.58 — Zhu reproduit : forme de Weil en variable x, contrôle par les zéros, valeurs de Galerkin."""
from __future__ import annotations
import importlib.util, json
from pathlib import Path

CALC = Path(__file__).resolve().parents[1]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def test_zhu_v658():
    Z = _load("rh658z", CALC / "scripts" / "run_zhu_reproduction.py")
    c = Z.controle_zeros(); assert c["ecart_relatif"] < 1e-9                       # formule en x = somme sur les zéros
    M = Z.weil_matrix(0.5, 0, 12); v = float(Z.lam_min(M, 12))
    assert 9.3e-7 < v < 9.6e-7                                                   # majorant proche du plancher de Zhu (9,34e-7)
    d = json.loads((CALC / "data" / "zhu_reproduction.json").read_text(encoding="utf-8-sig"))
    assert 8.9e-18 < float(d["valeurs"]["L=0.8 pair"]["40"]) < 2.27e-17
    for L, z in d["zhu_planchers_tableau1"].items():
        assert abs(float(d["valeurs"][f"L={L} pair"]["40"]) / z - 1) < 0.15
    k = json.loads((CALC / "data" / "zhu_noyau_des_moments.json").read_text(encoding="utf-8-sig"))
    assert float(k["0.5|32"]) > 1 / 250                                          # cohérent avec le théorème du document 73
    assert float(k["0.347|32"]) > 1 / 25 and float(k["0.55|32"]) > 3 / 10000      # docs 71 et 75
    assert float(k["0.8|40"]) <= float(k["0.8|32"]) <= float(k["0.8|24"])          # variationnel : décroît avec N
    assert all(float(k[f"{L}|24|impair"]) > float(k[f"{L}|24"]) for L in ("0.347", "0.5", "0.55", "0.8"))
    v = float(Z.noyau_des_moments(0.5, 10)); assert 0.0119 < v < 0.0125         # recalcul direct (10 modes)
    assert (CALC / "data" / "prevision_v658_zhu.md").exists()
