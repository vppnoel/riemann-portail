"""V6.11.1 — le portail et la carte des idées : pages à jour, liens valides, chaque nœud de la carte a sa fiche."""
import importlib.util, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]

def _mod(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def test_portal_in_sync_and_links_resolve():
    m = _mod("build_portail", "2_Methode/Portail/build_portail.py")
    page = (ROOT / "00_PORTAIL.html").read_text(encoding="utf-8-sig")
    assert page == m.build(standalone=True) and m.check_links(page, ROOT) == []
    docs = m.documents(m.BI.load()); assert len(docs) >= 35 and all(d["files"] for d in docs)

def test_entry_pages_link_each_other_and_map_is_complete():
    pages = {"00_PORTAIL.html": ROOT, "00_Carte_des_idees.html": ROOT,
             "1_Presentation/31_INDICATEUR_D_AVANCEMENT.html": ROOT / "1_Presentation", "1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html": ROOT / "1_Presentation"}
    for rel, base in pages.items():
        t = (ROOT / rel).read_text(encoding="utf-8-sig")
        hrefs = set(re.findall(r'href=["\']([^"\'#]+)["\']', t))
        assert not [h for h in hrefs if not h.startswith("http") and not (base / h).exists()], rel
        for other in ("00_PORTAIL.html", "00_Carte_des_idees.html", "31_INDICATEUR_D_AVANCEMENT.html", "34_NAVIGATEUR_DE_RECHERCHE.html", "README.md"):
            assert any(h.endswith(other) for h in hrefs), (rel, other)          # barre de navigation commune
    carte = (ROOT / "00_Carte_des_idees.html").read_text(encoding="utf-8-sig")
    assert set(re.findall(r'data-k="([^"]+)"', carte)) <= set(re.findall(r'<template id="t-([^"]+)"', carte))
    version = (ROOT / "VERSION.txt").read_text(encoding="utf-8-sig").splitlines()[0].split("— V")[-1].strip()
    version = re.match(r"[0-9.]*[0-9]", version).group(0)                          # V6.58 : « 6.58, livraison du … » → « 6.58 »
    # V6.58 : depuis V6.55, la carte est rendue par le pilotage (data-node, en-tête « Programme Riemann · V… ») ;
    # l'ancienne carte V6.11 (data-k, « Version … . ») n'existe plus. Mêmes exigences, nouvelle grammaire.
    assert (f"Version {version}." in carte or f"Programme Riemann · V{version}" in carte)
    assert ('data-k="generateur"' in carte or 'data-node="generateur"' in carte) and ('data-k="base"' in carte or 'data-node="base"' in carte)
