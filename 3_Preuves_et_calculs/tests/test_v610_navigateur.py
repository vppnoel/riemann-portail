"""V6.10 — le navigateur de recherche : carte cohérente avec le registre, l'indicateur et le corpus ; page à jour."""
import importlib.util
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
B = ROOT / "2_Methode" / "Navigateur" / "build_navigateur.py"

def _mod():
    spec = importlib.util.spec_from_file_location("build_navigateur", B); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def test_navigator_map_consistent_and_page_in_sync():
    m = _mod(); carte, ind, ops = m.load()
    assert m.check(carte, ops) == []                                       # opérateurs, prérequis et documents existent
    for c in carte["coups"]:
        assert c["statut"] in ("fait", "ouvert", "humain", "route à construire", "partiel") and c.get("temoin")   # aucun coup sans témoin ; « partiel » depuis V6.42 (étude dont une part reste ouverte)
        if c["statut"] == "fait": assert c.get("document") and c.get("appris")
    for c in carte["coups"]:                                               # pré-enregistrement (V6.11) : chaque coup ouvert garde sa prévision
        if c["statut"] == "ouvert": assert "prevision" in c                      # le maillon est facultatif (ex. préparer la relecture)
        assert c.get("maillon") in (None, *[x["id"] for x in carte["chaine"]])
    assert m.missing_links(carte) and all(x["etat"] in ("acquis", "non nécessaire", "manquant") for x in carte["chaine"])
    route = m.itinerary(carte); assert route                                # un itinéraire proposé
    page = (ROOT / "1_Presentation" / "34_NAVIGATEUR_DE_RECHERCHE.html").read_text(encoding="utf-8-sig")
    assert page == m.build(carte, ind, ops, links=True, standalone=True)
