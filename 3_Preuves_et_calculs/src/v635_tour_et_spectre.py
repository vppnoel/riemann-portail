"""Reproduit les comptages directs et les certificats exacts de V6.35.

Usage, depuis 3_Preuves_et_calculs : python src/v635_tour_et_spectre.py
Les comptages sont terminés avant toute comparaison à la récurrence.
"""
from pathlib import Path
import csv
import hashlib
import json
import math
import time

from finite_field_jets import (
    certificate, field, parameters, spectral_status, square_points, tower_trace,
)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
MODULI = {
    (3, 2): (1, 0, 1),
    (3, 3): (1, 2, 0, 1),
    (5, 2): (2, 0, 1),
    (5, 3): (1, 1, 0, 1),
    (7, 2): (1, 0, 1),
    (7, 3): (2, 0, 0, 1),
}


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")


def main():
    plan_path = DATA / "v635_controles_avant_execution.json"
    plan = json.loads(plan_path.read_text(encoding="utf-8-sig"))
    rows = []
    for p, last in ((3, 4), (5, 3), (7, 3), (11, 2)):
        for n in range(1, last + 1):
            F = field(p, n, MODULI.get((p, n)))
            S, z = square_points([1, 1, 0, 1], F)
            N = 2 * len(S) + z + 1
            r = math.isqrt(max(0, (F.q - 5) // 6))
            row = dict(p=p, n=n, q=F.q, module=list(F.modulus),
                       S=len(S), racines_f=z, N_direct=N,
                       ecart=N-F.q-1, ecart_normalise=abs(N-F.q-1)/math.sqrt(F.q))
            if r >= 1:
                par = parameters(F.q, r+1, 3*r*r-r+1, 2*r)
                row["borne_jets"] = 2*par["borne_S"]-F.q+z
            else:
                row["borne_jets"] = None
            rows.append(row)
            print(f"Comptage direct : p={p}, n={n}, N={N}", flush=True)

    # Deuxième phase : aucune valeur prédite ne génère le comptage ci-dessus.
    traces = {r["p"]: r["q"]+1-r["N_direct"] for r in rows if r["n"] == 1}
    for row in rows:
        trace = tower_trace(row["p"], traces[row["p"]], row["n"])
        row["trace_recurrence"] = trace
        row["N_recurrence"] = row["q"]+1-trace
        assert row["N_direct"] == row["N_recurrence"]
    for known in plan["controles_connus"]:
        row = next(r for r in rows if (r["p"], r["n"]) == (known["p"], known["n"]))
        assert row["N_direct"] == known["N"]
    write_json(DATA / "v635_tour.json", {
        "version": "V6.35", "limite_implementation_q": 1024,
        "plan_sha256": hashlib.sha256(plan_path.read_bytes()).hexdigest(),
        "comptages": rows,
        "spectres_controles": [spectral_status(p, t) for p, t in traces.items()],
        "methode": "Comptages directs, puis contrôle par récurrence ; la preuve universelle est séparée.",
    })
    csv_keys = ["p", "n", "q", "S", "racines_f", "N_direct", "ecart",
                "ecart_normalise", "borne_jets", "N_recurrence"]
    with (DATA / "v635_tour.csv").open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=csv_keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    certs = []
    for case in plan["certificats"]:
        p, n = case["p"], case["n"]
        F = field(p, n, MODULI.get((p, n)))
        nu = next(a for a in range(1, F.q) if F.pow(a, (F.q-1)//2) != 1)
        f = [1, 1, 0, 1]
        if case["torsion"]:
            f = [int(F.mul[nu, a]) for a in f]
        start = time.perf_counter()
        c = certificate(p, n, f, case["J"], case["K"], case["M"], F.modulus)
        c["torsion"] = case["torsion"]
        c["non_residu"] = nu if case["torsion"] else None
        c["secondes"] = round(time.perf_counter()-start, 3)
        certs.append(c)
        print(f"Certificat q={F.q}, torsion={c['torsion']} : "
              f"rang {c['rang_exact']}, noyau {c['noyau_exact']}, "
              f"degré {c['degre_temoin']}, multiplicité {c['multiplicite_minimale']}",
              flush=True)
    write_json(DATA / "v635_certificats.json", {
        "version": "V6.35",
        "encodage": "a = somme a_i p^i représente somme a_i u^i dans F_p[u]/(module) ; coefficients par degrés croissants.",
        "ordre_colonnes": "j puis a, avec x^(jq+a) puis x^(jq+a) g ; vecteurs par colonnes de la matrice des jets.",
        "certificats": certs,
    })
    return rows, certs


if __name__ == "__main__":
    main()
