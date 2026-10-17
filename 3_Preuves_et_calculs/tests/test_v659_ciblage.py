"""V6.59 — ciblage en lecture seule et fiches de tâche : contrôles adverses, registres cohérents, document 82 à jour.

Auteur et titulaire des droits : Vincent NOËL.
"""
import importlib.util, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True


def charger(nom, rel):
    s = importlib.util.spec_from_file_location(nom, ROOT / rel); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


def rd(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8-sig"))


def test_controles_adverses_du_ciblage_et_des_fiches():
    checks = charger("verify_ciblage_t", "2_Methode/Pilotage/verify_ciblage.py").main()
    assert len(checks) >= 46 and all(c["passed"] for c in checks)


def test_registre_unique_des_empreintes():
    c = rd("2_Methode/Pilotage/ciblage_contrats.json"); reviewed = rd("2_Methode/Pilotage/pilotage_recherche.json")["reviewed_source_hashes"]
    assert c["schema"] == "ciblage_contrats_v2"
    for e in c["evidence"].values():
        assert "observed_dependencies" not in e                      # plus de second registre d'empreintes
        assert all(p in reviewed for p in e["lire"])


def test_registre_des_fiches_coherent():
    T = charger("taches_t", "2_Methode/Pilotage/taches.py")
    R = T.Registre(ROOT)
    assert R.controler() == []
    assert R.data["auteurs"] == ["auteur:vincent-noel"]
    assert all(T.ACTEUR.match(e["par"]) for e in R.journal["evenements"])


def test_document_82_et_etat_courant():
    reg = rd("2_Methode/Pilotage/registre_identifiants.json")
    d = next(x for x in reg["documents"] if x["number"] == 82)
    for p in d["paths"]: assert (ROOT / p).is_file(), p
    texte = (ROOT / "1_Presentation/82_CIBLAGE_ET_REPARTITION.md").read_text(encoding="utf-8-sig")
    ref = (ROOT / "2_Methode/Pilotage/CIBLAGE.md").read_text(encoding="utf-8-sig")
    corps = ref[ref.index("## 1."):].rstrip()
    assert corps in texte                                                # le document 82 reprend la référence telle quelle
    for t in rd("2_Methode/Pilotage/taches.json")["taches"]:
        assert t["id"] in texte                                          # et liste les fiches du registre


def test_ciblage_ne_modifie_rien():
    m = charger("ciblage_t", "2_Methode/Pilotage/ciblage.py")
    avant = {p: (ROOT / p).read_bytes() for p in ["2_Methode/Pilotage/pilotage_recherche.json", "2_Methode/Pilotage/taches.json",
                                                  "2_Methode/Indicateur/indicateur_avancement.json"]}
    r = m.analyse(ROOT)
    assert not r["scientific_state_modified"] and not r["proof_promotions"] and r["executable_actions"] == []
    assert all((ROOT / p).read_bytes() == b for p, b in avant.items())


def test_navigateur_affiche_le_ciblage():
    html = (ROOT / "1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html").read_text(encoding="utf-8")
    assert 'id="ciblage"' in html and 'id="ciblage-bellman-live"' in html
    assert "chatgpt.com" not in html and "chatgpt.com" not in (ROOT / "00_PORTAIL.html").read_text(encoding="utf-8")
    assert rd("3_Preuves_et_calculs/data/ciblage_courant.json")["mode"] == "recommandations_en_lecture_seule"
