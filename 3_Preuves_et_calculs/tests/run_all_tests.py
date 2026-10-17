#!/usr/bin/env python3
"""Lanceur de toute la suite sans pytest : python tests/run_all_tests.py (depuis 3_Preuves_et_calculs).

Un fichier de tests dont une dépendance n'est pas installée (par exemple mpmath) est signalé
« NON EXÉCUTÉ » : il n'est compté ni comme réussi ni comme échoué, et le code de sortie vaut 2.
"""
import sys, importlib.util, inspect, time, glob
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(HERE))
tot = ok = 0; skipped = []
for f in sorted(glob.glob(str(HERE / "test_*.py"))):
    spec = importlib.util.spec_from_file_location(Path(f).stem, f); m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except ModuleNotFoundError as e:
        skipped.append((Path(f).stem, e.name)); print(f"NON EXÉCUTÉ {Path(f).stem} : module « {e.name} » absent"); continue
    for name, fn in inspect.getmembers(m, inspect.isfunction):
        if name.startswith("test_") and fn.__module__ == m.__name__:
            tot += 1; t = time.time()
            try:
                fn(); ok += 1; print(f"OK   {Path(f).stem}.{name} ({time.time()-t:.1f} s)")
            except Exception as e:
                print(f"FAIL {Path(f).stem}.{name} : {type(e).__name__} {str(e)[:150]}")
print(f"{ok}/{tot} tests OK" + (f" ; {len(skipped)} fichier(s) non exécuté(s) : " + ", ".join(f"{a} ({b})" for a, b in skipped) if skipped else ""))
sys.exit(1 if ok != tot else (2 if skipped else 0))
