"""V6.58 — intégrité : originaux figés à l'octet près, pilotage intégré, entrée du corpus cohérente.

Auteur et titulaire des droits : Vincent NOËL.
"""
import hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def rd(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8-sig"))


def test_originaux_figes_intacts():
    figes = rd("2_Methode/Pilotage/originaux_figes.json")["fichiers"]
    assert len(figes) >= 20
    for f in figes:
        b = (ROOT / f["path"]).read_bytes()
        assert hashlib.sha256(b).hexdigest() == f["sha256"], f["path"]
        assert not b.startswith(b"\xef\xbb\xbf")
        inv = "".join((ROOT / i).read_text(encoding="utf-8-sig") for i in f["inventaires"])
        assert f["sha256"] in inv                                                  # l'empreinte vient bien d'un inventaire d'intégrité


def test_documents_80_81_integres():
    reg = rd("2_Methode/Pilotage/registre_identifiants.json")
    nums = {d["number"] for d in reg["documents"]}
    assert {80, 81} <= nums and nums == set(range(1, max(nums) + 1))
    for d in reg["documents"]:
        if d["number"] in (80, 81): assert all((ROOT / p).is_file() for p in d["paths"])
    nav = rd("2_Methode/Navigateur/carte_navigation.json")
    ids = {c["id"]: c for c in nav["coups"]}
    assert ids["v658_trois_niveaux"]["statut"] == "fait" and ids["v658_zhu_reproduit"]["statut"] == "fait"
    assert ids["v658_certificat_noyau_S08"]["statut"] == "route à construire" and ids["v658_certificat_noyau_S08"]["prevision"]["texte"]
    ind = rd("2_Methode/Indicateur/indicateur_avancement.json")
    ids_e = [e["id"] for e in ind["etapes"]]; k = ids_e.index("v658")                 # V6.59 : l'étape V6.58 n'est plus la dernière
    assert ind["etapes"][k]["niveaux"] == ind["etapes"][k - 1]["niveaux"]                # niveaux inchangés en V6.58
    p = rd("2_Methode/Pilotage/pilotage_recherche.json")
    assert tuple(map(int, p["version"][1:].split("."))) >= (6, 58) and any(i["id"] == "noyau_S08" for i in p["investigations"])
    st = {n["id"]: n["status"] for n in p["nodes"]}
    assert all(st[k] == "ouvert" for k in ("RH", "global_sign", "weil_all"))


def test_entree_du_corpus():
    att = rd("2_Methode/Pilotage/points_d_attention.json")
    readme = (ROOT / "README.md").read_text(encoding="utf-8-sig")
    portail = (ROOT / "00_PORTAIL.html").read_text(encoding="utf-8")
    assert "## À lire d’abord" in readme and 'id="a-lire-d-abord"' in portail
    for pt in att["points"]:
        assert pt["titre"] in readme
        for _, rel in pt["liens"]: assert (ROOT / rel).exists(), rel
    for _, rel in att["outils"]: assert (ROOT / rel).exists(), rel
    plan = (ROOT / "PLAN_DU_CORPUS.md").read_text(encoding="utf-8-sig")
    nums = {f.name[:2] for f in (ROOT / "1_Presentation").glob("[0-9][0-9]_*") if f.suffix in (".md", ".pdf", ".docx", ".html")}
    assert all(re.search(rf"^\| {n} \|", plan, re.M) for n in nums)                # chaque numéro est rangé
    for rel in re.findall(r"\]\(([^)#]+)\)", readme + plan):
        if not rel.startswith("http"): assert (ROOT / rel).exists(), rel
    hist = (ROOT / "HISTORIQUE_DES_LIVRAISONS.md").read_text(encoding="utf-8-sig")
    assert "Livraison courante : V6.57" in hist and "# Programme Riemann - V6.54" in hist


def test_outils_de_lecture_synchronises():
    import importlib.util
    spec = importlib.util.spec_from_file_location("ol658", ROOT / "2_Methode/Outils/build_outils_de_lecture.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    fichiers = ("TABLE_LOGIQUE.md", "REFERENCES_HIERARCHISEES.md", "GUIDE_POUR_UNE_IA.md", "LOGICAL_TABLE.md", "REFERENCES_RANKED.md", "GUIDE_FOR_AN_AI.md")
    avant = {f: (ROOT / f).read_bytes() for f in fichiers}
    g, prio = m.tout()
    for f, b in avant.items():
        assert (ROOT / f).read_bytes() == b, f"{f} n'est plus à jour : relancer build_outils_de_lecture.py"
        t = b.decode("utf-8-sig")
        for rel in re.findall(r"\]\(([^)#\s]+)\)", t):
            if not rel.startswith("http"): assert (ROOT / rel).exists(), (f, rel)
    T = rd("2_Methode/Pilotage/table_logique.json"); N = {n["id"] for n in rd("2_Methode/Pilotage/pilotage_recherche.json")["nodes"]}
    S = {s["cle"] for s in rd("2_Methode/Sources/sources.json")}
    items = [e for r in T["routes"] for e in r["enonces"]] + T["temoins"] + T["obstructions"]
    assert all(i["noeud"] in N and (ROOT / i["piece"]).is_file() and set(i.get("refs", [])) <= S for i in items)
    assert sum(len(v) for v in g.values()) == len(S)                               # chaque fiche a un rang
    assert "RH reste ouverte" in avant["TABLE_LOGIQUE.md"].decode("utf-8-sig")


def test_couche_anglaise():
    att = rd("2_Methode/Pilotage/points_d_attention.json")
    assert set(att["en"]["points"]) == {p["id"] for p in att["points"]}
    readme = (ROOT / "README_EN.md").read_text(encoding="utf-8-sig")
    assert "## Read first" in readme and "RH remains open" in readme
    for rel in re.findall(r"\]\(([^)#\s]+)\)", readme):
        if not rel.startswith("http"): assert (ROOT / rel).exists(), rel
    T = rd("2_Methode/Pilotage/table_logique.json")
    assert all("en" in e for r in T["routes"] for e in r["enonces"]) and all("en" in r for r in T["routes"])
    for f in ("01_SYNTHESIS_EN", "07_READING_GUIDE_EN"):                      # synthèse et guide, en anglais (V6.58)
        assert (ROOT / "1_Presentation/english" / (f + ".pdf")).is_file() and "V6.58" in (ROOT / "1_Presentation/english" / (f + ".md")).read_text(encoding="utf-8-sig")
    for f in ("01_SYNTHESE_FR", "07_GUIDE_DE_LECTURE_INTUITIF"):
        assert "Mis à jour en V6.58" in (ROOT / "1_Presentation" / (f + ".md")).read_text(encoding="utf-8-sig")
        assert (ROOT / "4_Archives/historique" / (f + "_V6_24.md")).is_file()
    for f in ("80_WHERE_THE_SIGN_COMES_FROM", "81_ZHU_REPRODUCED"):
        assert (ROOT / "1_Presentation/english" / (f + ".pdf")).is_file()
        assert "French text prevails" in (ROOT / "1_Presentation/english" / (f + ".md")).read_text(encoding="utf-8-sig")
