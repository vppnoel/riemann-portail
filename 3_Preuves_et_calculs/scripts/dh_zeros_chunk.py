#!/usr/bin/env python3
"""Zéros de DH par Newton sur une tranche de hauteurs : dh_zeros_chunk.py t_min t_max (ajoute à data/dh_zeros.csv)."""
import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import mpmath as mp
from rejection import KAPPA_DH
mp.mp.dps = 15
k = mp.mpf(KAPPA_DH); c1, c2 = (1 - 1j * k) / 2, (1 + 1j * k) / 2
ch = {1: 1, 2: 1j, 3: -1j, 4: -1}
def f(s):
    z = [mp.zeta(s, mp.mpf(a) / 5) for a in ch]
    Lc = sum(ch[a] * z[i] for i, a in enumerate(ch)); Lb = sum(ch[a].conjugate() * z[i] for i, a in enumerate(ch))
    return (c1 * Lc + c2 * Lb) * mp.mpf(5) ** (-s)
lo, hi = float(sys.argv[1]), float(sys.argv[2]); STEP = float(sys.argv[3]) if len(sys.argv) > 3 else 3.0
_f0 = f
def f(s):
    if not (-1 < s.real < 3 and abs(s.imag) < hi + 20 and s.imag > lo - 20):
        raise ValueError('hors zone')
    return _f0(s)
path = ROOT / "data" / "dh_zeros.csv"
known = []
if path.exists():
    known = [tuple(map(float, l.split(","))) for l in path.read_text().split("\n")[1:] if l.strip()]
else:
    path.write_text("sigma,t\n")
t0 = lo; t_start = time.time()
while t0 < hi and time.time() - t_start < 230:
    for s0 in (0.5, 0.85, 1.15):
        try:
            z = mp.findroot(f, mp.mpc(s0, t0), tol=1e-9, maxsteps=10)
        except Exception:
            continue
        if abs(f(z)) < 1e-7 and lo - 3 < z.imag < hi + 3 and -0.5 < z.real < 2:
            zz = (float(z.real), float(z.imag))
            if all(abs(zz[0] - w[0]) + abs(zz[1] - w[1]) > 1e-4 for w in known):
                known.append(zz)
                with path.open("a") as fh: fh.write(f"{zz[0]!r},{zz[1]!r}\n")
    t0 += STEP
print("atteint t0 =", t0, "zéros connus:", len(known), "durée", round(time.time() - t_start, 1))
