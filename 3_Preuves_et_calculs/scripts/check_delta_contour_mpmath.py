"""V6.17 — contrôle du Contour tourné contre la série des gamma incomplètes en haute précision (mpmath).
Usage (depuis 3_Preuves_et_calculs) : python scripts/check_delta_contour_mpmath.py 612.3 1001.7  (t = 1 001,7 : environ 20 minutes)."""
import sys, time, math; sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parents[1] / 'src'))
import numpy as np, mpmath as mp
from delta_contour import DeltaBand
from delta_ramanujan import tau
T = tau(3000); taus = np.array([float(x) for x in T])

def Lam(t, dps):
    with mp.workdps(dps):
        s = mp.mpc(6, t); tot = mp.mpf(0)
        for n in range(1, len(T)):
            x = 2 * mp.pi * n; term = T[n] * (x ** (-s) * mp.gammainc(s, x) + x ** (-(12 - s)) * mp.gammainc(12 - s, x)); tot += term
            if n > 8 and abs(term) < abs(tot) * mp.mpf(10) ** (-dps + 5): break
        return mp.re(tot) / abs((2 * mp.pi) ** (-s) * mp.gamma(s))

for t in (float(a) for a in sys.argv[1:]):
    b = DeltaBand(taus, t - 12.5, t + 12.5); v = b.Z(t)[0]
    t1 = time.time(); dps = int(math.pi * t / 2 / math.log(10)) + 30; m = float(Lam(t, dps))
    print(t, v, m, abs(v - m) / abs(m), f"{time.time() - t1:.0f}s", flush=True)
