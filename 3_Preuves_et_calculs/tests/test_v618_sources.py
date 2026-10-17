"""V6.18 — registre des sources, carte des croisements (colonne Modèle réduit, liens), coups « lecture »."""
import importlib.util, json
from pathlib import Path
R2 = Path(__file__).resolve().parents[2]

def _mod(name, rel):
    spec = importlib.util.spec_from_file_location(name, R2 / rel); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def test_sources_registry():
    bs = _mod("bs", "2_Methode/Sources/build_sources.py"); S = bs.load()
    assert len(S) >= 130 and bs.check(S) == []                    # clés bien formées, uniques ; toute clé citée existe
    assert (R2 / "1_Presentation/42_REGISTRE_DES_SOURCES.md").read_text(encoding="utf-8-sig") == bs.build()
    assert all(s.get("ce_qui_a_ete_verifie") and s.get("verdict") for s in S)
    assert len(bs.lectures(S, 3)) == 3
    figes = {Path(f["path"]).name for f in json.loads((R2 / "2_Methode/Pilotage/originaux_figes.json").read_text(encoding="utf-8"))["fichiers"]}
    assert [d for d in bs.sync_docs(S, write=False) if d not in figes] == []   # V6.18.1 : « Références » à jour (V6.58 : sauf originaux figés)

def test_crossing_map_and_navigator():
    bi = _mod("bi", "2_Methode/Indicateur/build_indicateur.py"); d = bi.load(); assert bi.check_links(d) == []
    h, zones = bi.crossings(d, True)
    assert "Modèle réduit</th>" in h and "class='sdot'" in h and "<a class='chip up' href=" in h
    assert any("Modèle réduit" in z for z in zones)
    bn = _mod("bn", "2_Methode/Navigateur/build_navigateur.py"); carte, ind, ops = bn.load(); assert bn.check(carte, ops, ind) == []
    assert sum(1 for c in carte["coups"] if c.get("type") == "lecture") >= 3   # V6.19 : + lire_proportions_2026
    assert any(c.get("origine", "").startswith("OpenAI") for c in carte["coups"])
