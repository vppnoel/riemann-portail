#!/usr/bin/env python3
"""Vérification de TAC-003 (ia:claude) : rejeu numérique de l'algèbre du rapport, qui ne contient aucun programme.
R1 borne duale G_eff = H − B C⁻¹ B* ⪰ H − μ⁻¹ G*, G* = B R⁻¹ B*, μ = λ_min(R^{−1/2} C R^{−1/2}), sur 2000 formes aléatoires ;
R2 optimalité de μ⁻¹ dans le modèle à une dimension (énoncé du rapport) ;
R3 garde de restriction : norme duale ambiante contre norme restreinte à Y ;
R4 confrontation au document d'entrée 79 (dette relative ρ ≈ 0,999999832 à S = 3, partition 4 + 4) : perte relative
   tolérable pour une borne duale à cette marge.
python -B 2_Methode/Depot/TAC-003/verification/rejeu.py  →  rejeu.json (même dossier). Auteur et titulaire des droits : Vincent NOËL.
"""
import json, numpy as np
from pathlib import Path
rng = np.random.default_rng(20261018); out = {}
def herm(n, shift=0.0):
    A = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)); return A.conj().T @ A + shift * np.eye(n)
viol, gap = 0, []
for _ in range(2000):
    h, y = int(rng.integers(1, 5)), int(rng.integers(1, 7))
    H = herm(h) - rng.uniform(0, 2) * np.eye(h); B = rng.normal(size=(h, y)) + 1j * rng.normal(size=(h, y))
    C = herm(y, 0.1); R = herm(y, 0.1)
    Ri = np.linalg.inv(R); w, V = np.linalg.eigh(R); Rmh = V @ np.diag(w ** -0.5) @ V.conj().T
    mu = np.linalg.eigvalsh(Rmh @ C @ Rmh)[0]
    Geff = H - B @ np.linalg.inv(C) @ B.conj().T; Gd = H - B @ Ri @ B.conj().T / mu
    e = np.linalg.eigvalsh(Geff - Gd)[0]; viol += e < -1e-9 * (1 + np.abs(Geff).max()); gap.append(e)
out['R1'] = dict(cas=2000, borne_violee=int(viol), plus_petite_valeur_de_Geff_moins_borne=float(min(gap)))
H, a, mu = 2.0, 1.3, 0.7; ys = np.linspace(-10, 10, 200001); inf = float(np.min(H + 2 * a * ys + mu * ys ** 2))
out['R2'] = dict(H=H, a=a, mu=mu, infimum_numerique=inf, H_moins_a2_sur_mu=H - a * a / mu)
# R3 : espace ambiant R², R = identité, Y = vect(e1) ; c(x) = x1 + 5 x2. Norme ambiante √26, restreinte à Y : 1.
out['R3'] = dict(norme_ambiante=float(np.sqrt(26)), norme_restreinte_a_Y=1.0, rapport_des_dettes=26.0,
                 lecture="La borne ambiante surestime ici la dette d'un facteur 26 : la garde de restriction du rapport est juste, et déjà énoncée au document 76 (§ 2.2, Lemme C).")
rho = 0.999999832
out['R4'] = dict(rho_document_79=rho, marge_relative=1 - rho,
                 lecture="Une borne duale remplace B C⁻¹ B* par μ⁻¹ B R⁻¹ B* ⪰ B C⁻¹ B*. À cette partition, elle ne garde le signe que si elle majore la dette exacte de moins de (1 − ρ)/ρ ≈ 1,7·10⁻⁷ en relatif. Le rapport n'examine pas cette contrainte quantitative, qui est la donnée principale du document d'entrée.")
Path(__file__).with_name('rejeu.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n', encoding='utf-8'); print(json.dumps(out, ensure_ascii=False, indent=1))
