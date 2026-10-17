"""V6.11 — la base comme pas de temps : courbes sur F_q vues sur F_q² ; la métrique du générateur selon le pas."""
import math, sys
from pathlib import Path
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
D = ROOT / "data"

def test_curve_seen_over_q2_live():
    from base_change import gns_from_traces, base_q2_traces, real_weil, descents, h_of
    from stability_radius import normalized
    from frobenius_chain import distinct
    c, q = [1, 2, 6, 6, 9], 3
    b = normalized(c, q); beta = 1 / np.roots(b[::-1])
    r, lam, ev = gns_from_traces(base_q2_traces(b, 2 * 2 + 6))      # comptages sur F_9 seulement
    b2 = distinct(beta ** 2); assert r == len(b2)
    assert max(min(abs(l - x) for x in b2) for l in lam) < 1e-10 and np.allclose(np.abs(lam), 1, atol=1e-12) and ev[0] > -1e-12
    btw = normalized([ck * (-1) ** k for k, ck in enumerate(c)], q)  # la tordue P(-u) : mêmes comptages sur F_9
    assert np.allclose(base_q2_traces(b, 10), base_q2_traces(btw, 10), atol=1e-12)
    a = real_weil(c, q); ds = descents(a, q)
    assert h_of(a) in ds and h_of(-a) in ds and len(ds) == 2

def test_base_change_summary():
    d = pd.read_csv(D / "base_change.csv"); cur = d[d.objet == "courbe"]; fk = d[d.objet == "faux jumeau"]
    assert len(cur) == 525 and len(fk) == 220
    assert (cur.rang_q2 == cur.zeros_distincts_q2).all() and (cur.ecart_unitaire_q2 < 1e-8).all()
    assert cur.zeros_q2_egal_q_et_tordue.astype(bool).all()                     # zéros sur F_q² = courbe ∪ tordue
    assert (cur.contient_courbe.astype(bool) & cur.contient_tordue.astype(bool)).all() and (cur.descentes == cur.descentes_par_facteurs).all()
    assert int((cur.descentes == 2).sum()) == 440 and int(cur.descentes.max()) == 12
    assert int(cur.autres_courbes_meme_image.sum()) == 0 and int((cur.descentes > 2).sum()) == 55   # réfutation annoncée : non observée
    assert (fk.ecart_unitaire_q2 > 1e-3).all() and (fk.negatifs_q2 == fk.hors_cercle_q2_distincts // 2).all()   # la métrique survit au changement de base

def test_metric_and_step():
    m = pd.read_csv(D / "base_metric_step.csv")
    x = m[m["mode"] == "X fixé"]
    assert (x[x.objet != "DH"].negatifs == 0).all()                             # ζ et L : positives à tous les pas
    dh = list(x[x.objet == "DH"].sort_values("h").negatifs); assert dh[0] == 10 and dh[-1] == 0 and all(a >= b for a, b in zip(dh, dh[1:]))
    n = list(m[m["mode"] == "N fixé"].sort_values("h").negatifs); assert n[0] == 4 and n[-1] == 10 and all(a <= b for a, b in zip(n, n[1:]))
