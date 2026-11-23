#!/usr/bin/env python3
"""TAC-007, P1 : marge mesurée du noyau des moments à L = 0,8 quand le nombre de modes N augmente.

Réutilise noyau_des_moments() de 3_Preuves_et_calculs/scripts/run_zhu_reproduction.py (document 81, non certifié).
Contrôles : quadrature archimédienne K = 48 puis 96 ; précision 60 puis 80 chiffres.
python -B 2_Methode/Depot/TAC-007/p1_mesure_noyau_08.py  →  p1_resultats.json (même dossier)
Auteur et titulaire des droits : Vincent NOËL. Producteur : ia:claude.
"""
from pathlib import Path
import importlib.util, json, sys, time
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
s = importlib.util.spec_from_file_location('zhu', ROOT / '3_Preuves_et_calculs/scripts/run_zhu_reproduction.py')
z = importlib.util.module_from_spec(s); s.loader.exec_module(z); mp = z.mp
OUT = HERE / 'p1_resultats.json'
res = json.loads(OUT.read_text()) if OUT.exists() else {}
plan = [(40, 48, 60), (48, 48, 60), (56, 48, 60), (64, 48, 60), (48, 96, 60), (64, 96, 60), (56, 48, 80), (64, 96, 80), (48, 48, 60, 1)]
t0 = time.time()
for item in plan:
    N, K, dps = item[:3]; par = item[3] if len(item) > 3 else 0
    key = f'N={N} K={K} dps={dps} {"impair" if par else "pair"}'
    if key in res: continue
    mp.mp.dps = dps
    v = z.noyau_des_moments(0.8, N, K, par)
    res[key] = dict(marge=mp.nstr(v, 12), secondes=round(time.time() - t0))
    OUT.write_text(json.dumps(res, indent=1, ensure_ascii=False) + '\n')
    print(key, res[key], flush=True)
