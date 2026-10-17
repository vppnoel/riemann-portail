"""V6.21 — Axe J : la surface virtuelle."""
from __future__ import annotations
import importlib.util, json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]; CALC = ROOT / "3_Preuves_et_calculs"

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def test_indice_de_hodge_modele_reduit():
    SV = _load("sv", CALC / "scripts" / "run_surface_virtuelle.py")
    c, q, g = [1, 2, 3], 3, 1                                      # courbe de genre 1 sur F_3 (RH vraie)
    assert SV.inertia(SV.intersection_gram(c, q, g, 2 * g + 1))[0] == 1
    tw = [1, -4, 3]                                                # faux jumeau de genre 1 (racines réelles 1 et 3)
    assert SV.inertia(SV.intersection_gram(tw, q, g, 2 * g + 1))[0] == 2
    # orthogonalement aux fibres : opposé de la métrique des zéros (Toeplitz des e^{i d θ})
    al = SV.roots_alpha(c) / np.sqrt(q); K = 4
    T = np.array([[np.sum(al ** (i - j) if i >= j else np.conj(al) ** (j - i)).real for j in range(K + 1)] for i in range(K + 1)])
    assert np.max(np.abs(SV.perp_block(c, q, g, K) + T)) < 1e-9

def test_resultats_v621():
    rep = json.loads((CALC / "data" / "surface_virtuelle.json").read_text(encoding="utf-8-sig"))
    A = rep["A"]; assert A["courbes_une_seule_positive"] == A["courbes"] == 425
    assert A["jumeaux_surplus_egal_hors_cercle_sur_2"] == A["faux_jumeaux"] == 220
    z = [r["positives"] for r in rep["B"]["zeta"]]; dh = [r["positives"] for r in rep["B"]["DH"]]
    assert set(z) == {1} and max(dh) >= 2 and all(r["positives"] == 0 for r in rep["B"]["L_chi5"])
    assert (CALC / "data" / "prevision_v621_surface.md").exists()
