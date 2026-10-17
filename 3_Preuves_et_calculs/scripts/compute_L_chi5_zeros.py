#!/usr/bin/env python3
"""V6.3c — Zéros de L(s, chi_5) (chi(2) = i, impair) sur la droite critique, |t| <= TMAX, reprenable par tranches.
Méthode : |L(1/2+it)| sur une grille (pas 0,1), minima locaux, puis Newton complexe (mpmath, Hurwitz)."""
from pathlib import Path
import sys, time
import numpy as np, mpmath as mp
ROOT = Path(__file__).resolve().parents[1]
mp.mp.dps = 15
ch = {1: 1, 2: 1j, 3: -1j, 4: -1}
def L(s):
    return sum(ch[a] * mp.zeta(s, mp.mpf(a) / 5) for a in ch) * mp.mpf(5) ** (-s)
lo, hi = float(sys.argv[1]), float(sys.argv[2])
out = ROOT / "data" / "L_chi5_zeros.csv"
known = [tuple(map(float, l.split(","))) for l in out.read_text().split("\n")[1:] if l.strip()] if out.exists() else []
if not out.exists(): out.write_text("sigma,t\n")
t0 = time.time(); step = 0.1
ts = np.arange(lo, hi, step)
vals = np.array([abs(complex(L(mp.mpc(0.5, t)))) for t in ts])
new = 0
for k in range(1, len(ts) - 1):
    if vals[k] < vals[k - 1] and vals[k] <= vals[k + 1] and vals[k] < 0.6:
        try:
            z = mp.findroot(L, mp.mpc(0.5, ts[k]), tol=1e-12, maxsteps=30)
        except Exception:
            continue
        if abs(L(z)) < 1e-9 and lo - 1 < float(z.imag) < hi + 1:
            zz = (float(z.real), float(z.imag))
            if all(abs(zz[1] - w[1]) > 1e-6 for w in known):
                known.append(zz); new += 1
                with out.open("a") as fh: fh.write(f"{zz[0]!r},{zz[1]!r}\n")
print(f"[{lo},{hi}] : {new} nouveaux zéros, total {len(known)}, {time.time()-t0:.0f} s")
