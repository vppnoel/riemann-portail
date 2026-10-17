"""V6.30 — Les articles présentables : les chiffres des articles sont ceux des données du corpus."""
from __future__ import annotations
import json, math
from pathlib import Path
import pandas as pd

CALC = Path(__file__).resolve().parents[1]
ART = CALC.parent / "1_Presentation" / "articles"


def test_articles_v630():
    t1 = (ART / "article1_mean_square_double_poles.tex").read_text(encoding="utf-8-sig")
    t2 = (ART / "article2_prime_side_weil_forms.tex").read_text(encoding="utf-8-sig")
    assert (ART / "article1_mean_square_double_poles.pdf").exists() and (ART / "article2_prime_side_weil_forms.pdf").exists()
    kappa = 2 + 0.5772156649015329 - math.log(4 * math.pi)
    assert "0.0461914179" in t1 and abs(kappa - 0.0461914179) < 1e-10
    # Tableau de l'article 1 : Q(10^4), Q(10^5) recoupés avec le crible du palier (V6.20)
    pal = pd.read_csv(CALC / "data" / "palier_quatre_tiers.csv").set_index("N")
    assert abs(pal.loc[10000, "Q"] - 27.03) < 0.005 and abs(pal.loc[100000, "Q"] - 60.49) < 0.005
    assert "27.03" in t1 and "60.49" in t1
    # Médiane de la famille de Nyman–Beurling (74 valeurs) : 1,313
    b = pd.read_csv(CALC / "data" / "palier_balayage.csv"); d = pd.concat([b[["N", "total"]], pal.reset_index()[["N", "total"]]]).drop_duplicates("N")
    assert len(d) == 74 and abs(d.total.median() - 1.313) < 0.001
    # Article 2 : décomptes de DH (correctif du seuil)
    c = pd.read_csv(CALC / "data" / "carre_continu.csv"); h = c[c.objet == "DH"]
    assert (h[h.X <= 20.3].en_trop == 0).all() and len(h[h.X <= 20.3]) == 12
    assert int((h[h.X >= 55.7].en_trop > 0).sum()) == 47 and len(h[h.X >= 55.7]) == 48
    assert "47$ of the $48" in t2
    assert "Cher Professeur," in (ART / "lettre_FR.txt").read_text(encoding="utf-8-sig")
    assert "Dear Professor," in (ART / "letter_EN.txt").read_text(encoding="utf-8-sig")
