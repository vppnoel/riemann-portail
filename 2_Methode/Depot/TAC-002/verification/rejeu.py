#!/usr/bin/env python3
"""Vérification de TAC-002 (ia:claude) : rejeu numérique de l'algèbre du rapport, qui ne contient aucun programme.
R1 identité de polarisation et minoration Q(Σh) ≥ Σb − Σd, sur 2000 formes hermitiennes aléatoires ;
R2 contre-modèle à deux paquets : diagonale (1, 1), terme croisé −a, coefficients (1, 1) ;
R3 lien avec la voie Toeplitz du document 76 (§ 2.3 et « Ce que les diagnostics peuvent décider ») : le contre-modèle
   est exactement la violation |k(d)| > k(0) à deux paquets que le document 76 décrit déjà.
python -B 2_Methode/Depot/TAC-002/verification/rejeu.py  →  rejeu.json (même dossier). Auteur et titulaire des droits : Vincent NOËL.
"""
import json, numpy as np
from pathlib import Path
rng = np.random.default_rng(20261018); out = {}
pires = []
for _ in range(2000):
    n = int(rng.integers(2, 9)); A = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)); Q = A.conj().T @ A - rng.uniform(0, 3) * np.eye(n)
    z = rng.normal(size=n) + 1j * rng.normal(size=n)
    total = np.real(z.conj() @ Q @ z)
    diag = sum(np.real(np.conj(z[j]) * Q[j, j] * z[j]) for j in range(n))
    croise = 2 * sum(np.real(np.conj(z[i]) * Q[i, j] * z[j]) for i in range(n) for j in range(i + 1, n))
    d = [sum(abs(np.conj(z[i]) * Q[i, j] * z[j]) for i in range(n) if i != j) for j in range(n)]
    pires.append(dict(polarisation=abs(total - diag - croise), marge=total - (diag - sum(d))))
out['R1'] = dict(cas=2000, ecart_polarisation_max=float(max(p['polarisation'] for p in pires)), minoration_violee=int(sum(p['marge'] < -1e-9 for p in pires)))
R2 = {}
for a in (0.5, 1.0, 1.5):
    M = np.array([[1, -a], [-a, 1]]); R2[str(a)] = dict(bilans_individuels=[1, 1], bilan_somme=float(np.array([1, 1]) @ M @ np.array([1, 1])), lambda_min=float(np.linalg.eigvalsh(M)[0]))
out['R2'] = R2
out['R3'] = "Matrice de Gram de deux paquets traduits : T = [[k(0), k(d)], [k(d), k(0)]]. Le contre-modèle est T avec k(0) = 1, k(d) = −a : négatif si et seulement si |k(d)| > k(0), le témoin négatif à deux paquets déjà décrit au document 76."
Path(__file__).with_name('rejeu.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n', encoding='utf-8'); print(json.dumps(out, ensure_ascii=False, indent=1))
