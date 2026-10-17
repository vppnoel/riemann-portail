"""V6.58 — registres V6.44–V6.50 déclarés historiques (décision de l'auteur, 17 octobre 2026).

Auteur et titulaire des droits : Vincent NOËL. Voir 3_Preuves_et_calculs/data/registres_historiques_v650.json.
Un registre historique est vérifié pour lui-même : son fichier n'a pas changé depuis la déclaration, et ses fiches
de sources sont bien formées. Il n'est plus comparé au corpus courant, que le pilotage V6.55+ suit à sa place.
"""
import hashlib, json, re
from pathlib import Path

CALC = Path(__file__).resolve().parents[1]; ROOT = CALC.parent
DECL = json.loads((CALC / "data/registres_historiques_v650.json").read_text(encoding="utf-8"))
SNAP = {s["path"]: s["sha256"] for s in DECL["instantanes"]}


def verifier_instantane(nom):
    """Le fichier data/<nom> est un instantané déclaré et n'a pas changé."""
    rel = "3_Preuves_et_calculs/data/" + nom
    assert rel in SNAP, f"{nom} n'est pas un registre historique déclaré"
    assert hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == SNAP[rel], f"instantané modifié : {nom}"


def verifier_sources_historiques(registry):
    """Fiches de sources bien formées (chemin, empreinte hexadécimale de 64 caractères), sans comparaison au corpus courant."""
    for row in registry["documents"]:
        for s in row.get("sources", []):
            if isinstance(s, dict):
                assert s["path"] and re.fullmatch(r"[0-9a-f]{64}", s["sha256"]), (row.get("numero"), s)


def verifier_etape_indicateur(version_id):
    """L'étape de l'indicateur existe et ses niveaux sont ceux de l'étape précédente (niveaux inchangés)."""
    ind = json.loads((ROOT / "2_Methode/Indicateur/indicateur_avancement.json").read_text(encoding="utf-8-sig"))
    ids = [e["id"] for e in ind["etapes"]]; i = ids.index(version_id)
    assert ind["etapes"][i]["niveaux"] == ind["etapes"][i - 1]["niveaux"]
