"""V6.29 — Le trou à trois, lu ; les deux tiers comme recensement de marges ; la matrice complétée."""
from __future__ import annotations
import importlib.util, json
from pathlib import Path
import numpy as np

CALC = Path(__file__).resolve().parents[1]
ROOT = CALC.parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def test_trou_a_trois_et_recensement_v629():
    B = _load("rh629", CALC / "scripts" / "run_bblm_trou_a_trois.py")
    # rapport d'écarts : insensible à l'échelle
    s = np.array([0.5, 1.2, 0.9, 1.4]); assert np.allclose(B.ratios(s[:-1], s[1:]), B.ratios(3 * s[:-1], 3 * s[1:]))
    rep = json.loads((CALC / "data" / "bblm_trou_a_trois.json").read_text(encoding="utf-8-sig"))
    c3 = rep["cue3"]; assert 0.004 < c3["mesure"] < 0.010 and abs(c3["mesure"] - c3["fit_prolonge"]) < 0.001   # B1
    assert abs(rep["reference_sinus"]["r_moyen"] - 0.5996) < 0.002
    z = rep["objets"][0]; assert z["triples_lt1"] == 0 and z["ecart_en_sigma"] > 2 and abs(z["r_moyen"] - z["r_moyen_sans_depliage"]) < 1e-3
    # identité : (tr G)²/tr G² = n / (1 + (1/n) Σ_{i≠j} (1 − m_ij)), m_ij = 1 − |G_ij|²
    rng = np.random.default_rng(0); g = np.sort(rng.uniform(0, 30, 12)); t = np.linspace(0, 1, 400)
    V = np.exp(1j * np.outer(g, t)); G = V @ V.conj().T; d = np.sqrt(np.real(np.diag(G))); G = G / np.outer(d, d)
    n = len(g); m = 1 - np.abs(G) ** 2; off = ~np.eye(n, dtype=bool)
    assert abs(np.real(np.trace(G)) ** 2 / np.real(np.trace(G @ G)) - n / (1 + (1 - m[off]).sum() / n)) < 1e-9
    # matrice : Mertens sourcé, DH ✗ proportion présent
    M = json.loads((ROOT / "2_Methode" / "Matrice" / "matrice_theories.json").read_text(encoding="utf-8-sig"))
    rel = {(r["de"], r["vers"]): r for r in M["relations"]}
    assert rel[("MERT", "RH")]["sources"] and rel[("DH", "PROP")]["type"] == "✗"
    assert (CALC / "data" / "prevision_v629_bblm.md").exists()
