"""V6.25 — Unités fictives (document reçu) : le bilan est une sommation par parties, et le script reçu est conservé."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[2]

def test_bilan_sommation_par_parties_et_archive():
    rnd = random.Random(625); N = 80
    c = [F(0), F(0)] + [F(rnd.randint(-9, 9), rnd.randint(1, 5)) for _ in range(N - 1)]
    C = [F(0)] * (N + 1)
    for n in range(1, N + 1): C[n] = C[n - 1] + c[n]
    Q = sum(C[k] ** 2 / (k * (k + 1)) for k in range(1, N)); K = C[N] ** 2 / N
    W = sum((2 * C[n - 1] * c[n] + c[n] ** 2) / n for n in range(2, N + 1))
    assert Q + K == W                                              # identité exacte, pour toute suite
    rec = ROOT / "4_Archives" / "recus" / "Unites_fictives_RH"
    if (ROOT / "4_Archives" / "NON_PUBLIE.md").exists() and not rec.exists(): return   # copie publique : document reçu non publié
    assert (rec / "calcul_unites.py").exists() and (rec / "Unites_fictives_et_bilan_RH.md").exists()
