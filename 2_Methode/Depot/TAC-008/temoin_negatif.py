#!/usr/bin/env python3
"""TAC-008, complément (fil #4) : témoin négatif. La décomposition voit-elle un défaut eulérien injecté, et où ?

Défauts injectés dans ζ (b = Λ), prévision enregistrée avant calcul (journal des tâches, 18 octobre) :
  D_η    : b(p^k) = Λ(p^k)·(1 + η) pour k ≥ 2, η ∈ {0,5 ; 1 ; 2}, premiers inchangés ;
  D_phase: b(p²) = −Λ(p²).
Mesures, à T = 1 et T = 10 : d_X = ‖X(défaut) − X(ζ)‖_F / trace K(ζ) pour X = K_diag, K_chaîne, K_croisé
(trace de ζ fixe : pas d'effet de normalisation), et part relative de K_chaîne (norme de Frobenius).
Mêmes réglages et même code que decomposition_K.py (importé sans modification).
python -B 2_Methode/Depot/TAC-008/temoin_negatif.py  →  temoin_negatif.json
Auteur et titulaire des droits : Vincent NOËL. Producteur : ia:claude.
"""
from pathlib import Path
import importlib.util, json
import numpy as np
HERE = Path(__file__).resolve().parent
s = importlib.util.spec_from_file_location('dk', HERE / 'decomposition_K.py'); dk = importlib.util.module_from_spec(s); s.loader.exec_module(dk)

zeta = dk.b_of('zeta')
def defaut(nom):
    b = zeta.copy()
    if nom.startswith('eta'): eta = float(nom[3:]); b[dk.expo >= 2] *= (1 + eta)
    elif nom == 'phase': b[dk.expo == 2] *= -1
    return b

fro = lambda M: float(np.linalg.norm(M))
out = dict(reglages=dict(NMAX=dk.NMAX, h=dk.H, T=list(dk.TS)), defauts={})
for T in dk.TS:
    tot0, d0, c0, x0 = dk.K_parts(zeta, T); tr0 = float(np.real(np.trace(tot0)))
    part0 = fro(c0) / (fro(d0) + fro(c0) + fro(x0))
    for nom in ('eta0.5', 'eta1', 'eta2', 'phase'):
        tot, d, c, x = dk.K_parts(defaut(nom), T)
        dd, dc, dx = fro(d - d0) / tr0, fro(c - c0) / tr0, fro(x - x0) / tr0
        part = fro(c) / (fro(d) + fro(c) + fro(x))
        out['defauts'][f'T={T} {nom}'] = dict(d_diag=dd, d_chaine=dc, d_croise=dx, chaine_sur_max_autres=dc / max(dd, dx),
                                              part_chaine_zeta=part0, part_chaine_defaut=part, variation_relative_part=(part - part0) / part0)
        print(T, nom, f'diag {dd:.3e}  chaîne {dc:.3e}  croisé {dx:.3e}  part {part0:.2e} → {part:.2e}', flush=True)
(HERE / 'temoin_negatif.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
