"""V6.32 — Les fichiers .md portent la marque UTF-8 (BOM) ; les scripts la lisent sans dommage."""
from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]; BOM = b"\xef\xbb\xbf"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def test_md_bom_et_lecture():
    import json                                                                   # V6.58 : les originaux archivés et figés restent à l'octet près
    figes = {f["path"] for f in json.loads((ROOT / "2_Methode/Pilotage/originaux_figes.json").read_text(encoding="utf-8"))["fichiers"]}
    md = [p for p in ROOT.rglob("*.md") if p.parts[len(ROOT.parts)] != "4_Archives" and str(p.relative_to(ROOT)) not in figes]
    assert md and all(p.read_bytes().startswith(BOM) for p in md)
    for p in md: p.read_bytes()[3:].decode("utf-8")                               # UTF-8 valide après la marque
    recus = ROOT / "4_Archives" / "recus"
    if recus.exists(): assert not any(p.read_bytes().startswith(BOM) for p in recus.rglob("*.md"))   # documents reçus intacts
    F = _load("bf", ROOT / "2_Methode" / "Figures" / "build_figures.py")
    assert F.title_of(ROOT / "1_Presentation" / "56_LE_RELIEF_DE_L_ARCHIPEL.md").startswith("V6.31 — Le relief")
    page = (ROOT / "00_PORTAIL.html").read_text(encoding="utf-8-sig")
    assert "﻿" not in page and "Programme Riemann — Synthèse" in page
