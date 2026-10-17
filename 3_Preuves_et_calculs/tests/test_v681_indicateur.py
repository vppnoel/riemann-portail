"""V6.8.1 — l'indicateur d'avancement : documents cités présents, page à jour avec ses données."""
import importlib.util, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
B = ROOT / "2_Methode" / "Indicateur" / "build_indicateur.py"

def _mod():
    spec = importlib.util.spec_from_file_location("build_indicateur", B); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def test_indicator_links_levels_and_page_in_sync():
    m = _mod(); d = m.load()
    assert m.check_links(d) == []                                         # chaque document cité existe dans le corpus
    ids = [e["id"] for e in d["etapes"]]; dims = [x["id"] for x in d["dimensions"]]
    assert len(set(ids)) == len(ids) and d["comparaison"]["avant"] in ids and d["comparaison"]["apres"] in ids
    for e in d["etapes"]:
        assert set(e["niveaux"]) == set(dims) and all(0 <= v <= 9 for v in e["niveaux"].values()) and e["documents"]
    assert all(lvl < 7 for e in d["etapes"] for lvl in e["niveaux"].values())   # aucun niveau « relu » revendiqué
    page = (ROOT / "1_Presentation" / "31_INDICATEUR_D_AVANCEMENT.html").read_text(encoding="utf-8-sig")
    assert page == m.build(d, links=True, standalone=True)                # la page publiée correspond aux données
