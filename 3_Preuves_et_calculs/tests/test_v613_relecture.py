"""V6.13 — pré-relecture : le dossier de relecture est complet, les identités ajoutées au corpus sont justes, le navigateur et l'indicateur sont à jour."""
import cmath, json, math, random, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
REL = ROOT / "1_Presentation" / "relecture"

def test_dossier_complete_and_self_linked():
    notes = ["RELECTURE_THEOREME_A_EN.md", "RELECTURE_THEOREME_B_EN.md", "RELECTURE_ARCHIPEL_EN.md"]
    for n in notes + [n.replace("_EN.md", "_RESUME_FR.md") for n in notes] + ["00_READ_ME_FIRST_EN.md"]:
        assert (REL / n).is_file(), n
    cover = (REL / "00_READ_ME_FIRST_EN.md").read_text(encoding="utf-8-sig")
    assert all(f"]({n})" in cover for n in notes) and "No proof of the Riemann Hypothesis is claimed" in cover
    for f in REL.glob("*.md"):                                     # dossier publiable : aucune adresse électronique
        assert not re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", f.read_text(encoding="utf-8-sig")), f.name
    b = (REL / "RELECTURE_THEOREME_B_EN.md").read_text(encoding="utf-8-sig")
    assert "Corollary B′" in b and "−0.3074" in b

def test_corollary_B_prime_and_rigidity_identity():
    # B′ : S − 4κ = Σ (m²(m+1)² − 4m)/|ρ|², chaque terme ≥ 0, nul exactement pour m = 1
    assert all((m * m * (m + 1) ** 2 - 4 * m > 0) == (m > 1) for m in range(1, 60))
    # Archipel, identité (ii) : moyenne sur G×G de |dD_a(b)|² = λ²(3Σβ² + |Σβu|²), sommes sur χ' ≠ χ
    rng = random.Random(613)
    for q in (5, 7, 11, 13):
        g = next(x for x in range(2, q) if len({pow(x, k, q) for k in range(q - 1)}) == q - 1)
        log = {pow(g, j, q): j for j in range(q - 1)}
        for kappa in (0, 1):
            X = [k for k in range(1, q - 1) if k % 2 == kappa]     # χ_k(−1) = (−1)^k ; caractère principal exclu
            if len(X) < 2: continue
            chi = {k: (lambda r, k=k: cmath.exp(2j * math.pi * k * log[r % q] / (q - 1))) for k in X}
            u = {}
            for k in X:                                          # phase de Hardy : ε = τ(χ)/(i^κ √q) = e^{2iφ}, u = e^{−iφ}
                tau = sum(chi[k](r) * cmath.exp(2j * math.pi * r / q) for r in range(1, q))
                eps = tau / (1j ** kappa * math.sqrt(q)); u[k] = cmath.exp(-0.5j * cmath.phase(eps))
                assert abs(abs(eps) - 1) < 1e-12
            for k0 in X:
                lam = rng.uniform(0.5, 2); beta = {k: rng.gauss(0, 1) for k in X}
                a = lambda r: lam * u[k0] * chi[k0](r)
                b = lambda r: sum(beta[k] * u[k] * chi[k](r) for k in X)
                mean = sum(abs(a(1) * b(r * s) + b(1) * a(r * s) - a(r) * b(s) - b(r) * a(s)) ** 2
                           for r in range(1, q) for s in range(1, q)) / (q - 1) ** 2
                other = [k for k in X if k != k0]
                pred = lam ** 2 * (3 * sum(beta[k] ** 2 for k in other) + abs(sum(beta[k] * u[k] for k in other)) ** 2)
                assert abs(mean - pred) < 1e-9 * pred and mean >= 3 * lam ** 2 * sum(beta[k] ** 2 for k in other) - 1e-9

def test_navigator_and_indicator_record_the_pre_review():
    carte = json.loads((ROOT / "2_Methode/Navigateur/carte_navigation.json").read_text(encoding="utf-8-sig"))
    c = {m["id"]: m for m in carte["coups"]}
    assert c["preparer_relecture"]["statut"] == "fait" and c["preparer_relecture"]["version"] == "V6.13"
    assert c["preparer_relecture"]["refutation_tenue"].startswith("Tenue") and "preparer_relecture" in c["relecture"]["prerequis"]
    assert "Booker–Thorne" in c["degre2_archipel"]["these"]
    ind = json.loads((ROOT / "2_Methode/Indicateur/indicateur_avancement.json").read_text(encoding="utf-8-sig"))
    e = {s["id"]: s for s in ind["etapes"]}
    same = lambda k: {d: v for d, v in e[k]["niveaux"].items() if d != "croiser"}          # « croiser » : dimension comptée rétroactivement en V6.16
    assert same("v613") == same("v612") and e["v613"]["niveaux"]["demontrer"] == 6   # pré-relecture ≠ relecture
    doc30 = (ROOT / "1_Presentation/30_ARCHIPEL_D_EULER.md").read_text(encoding="utf-8-sig")
    assert "correctif V6.13" in doc30 and "ce n'est pas nouveau" in doc30
