"""V6.16 — la Rencontre à trois (marge locale = corrélation de Montgomery) et les croisements dans l'indicateur et le navigateur."""
import importlib.util, json, math, sys
from pathlib import Path
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]; R2 = ROOT.parent
D = ROOT / "data"

def _mod(name, rel):
    spec = importlib.util.spec_from_file_location(name, R2 / rel); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def test_margin_is_montgomery_pair_correlation():
    # marge = 1 − |<x1, x2>/n|² pour deux exponentielles e^{iγ j h}, fenêtre L = log(γ/2π) : tend vers 1 − sinc²(πs)
    rng = np.random.default_rng(616)
    for _ in range(20):
        g0 = rng.uniform(50, 2000); s = rng.uniform(0.02, 2.5); LH = math.log(g0 / (2 * math.pi)); gap = s * 2 * math.pi / LH
        h = 1e-4; n = int(round(LH / h)); j = np.arange(n)
        sig = abs(np.sum(np.exp(1j * gap * j * h))) / n
        assert abs((1 - sig ** 2) - (1 - (math.sin(math.pi * s) / (math.pi * s)) ** 2)) < 2e-3
    # signe : paire sur la droite (poids réels positifs) -> forme définie positive ; paire hors droite -> signature (1, 1)
    w = 0.7 - 0.2j; assert np.linalg.det(np.array([[0, w], [np.conj(w), 0]])).real < 0

def test_rencontre_recorded():
    r = pd.read_csv(D / "rencontre_resume.csv").iloc[0]
    assert abs(r.somme_beta - 0.5405) < 0.005                                            # P4 : contrôle de β (relecture B)
    assert r.fraction_zeros < r.fraction_poisson / 10                                     # répulsion nette
    assert r.lehmer_marge < 0.01 and r.lehmer_ecart_sur_mediane_1 > 500                  # la paire de Lehmer
    assert r.part_ecart_dans_beta < 0.1 and 0.25 < r.part_beta_ecart_10pc < 0.45          # β lisse ; sa part d'écart lit les paires serrées
    z = pd.read_csv(D / "rencontre_zeros.csv"); assert len(z) == 1070
    k = z.nsmallest(len(z) // 10, "s"); assert np.corrcoef(k.ZppZp, -2 / (np.where(k.voisin_droite, 1, -1) * k.ecart))[0, 1] > 0.95   # Z''/Z' ≈ −2/écart

def test_crossings_in_indicator_and_navigator():
    bi = _mod("bi", "2_Methode/Indicateur/build_indicateur.py"); d = bi.load()
    assert "croiser" in [x["id"] for x in d["dimensions"]] and bi.check_links(d) == []
    conj = {c["id"] for c in d["conjectures"]}; order = [e["id"] for e in d["etapes"]]
    for x in d["croisements"]: assert set(x["conjectures"]) <= conj and (x["statut"] != "corpus" or x["etape"] in order)
    for e in d["etapes"]:                                  # règle : le niveau est le plus haut croisement produit par le corpus jusque-là
        k = order.index(e["id"])
        best = max([x["niveau"] for x in d["croisements"] if x["statut"] == "corpus" and order.index(x["etape"]) <= k] or [0])
        assert e["niveaux"]["croiser"] == best
    html_, zones = bi.crossings(d, True); assert "Les croisements" in html_ and len(zones) > 0
    bn = _mod("bn", "2_Methode/Navigateur/build_navigateur.py"); carte, ind, ops = bn.load()
    assert bn.check(carte, ops, ind) == []
    c = next(m for m in carte["coups"] if m["id"] == "repulsion_degre2")
    assert bn.score(c, carte, set())["croisement"] == carte["poids_croisement"] * 2
    v = {x["titre"]: x for x in bn.veille(carte, ops)}; assert v["Kalman, GPS analytique"]["a_relire"]
