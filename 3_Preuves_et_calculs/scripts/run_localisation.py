#!/usr/bin/env python3
"""Q_{w,W}(L;T,Delta) localise-t-elle les zéros de zeta ? Pics de l'énergie de bande vs gamma_k."""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from rh_core import arithmetic_c_via_lambda, C_partial
from spectral_calibration import B_grid_from_C, windowed_fourier
from explicit_formula import load_zeros

N = 300_000
C = C_partial(arithmetic_c_via_lambda(N))
t, B = B_grid_from_C(C, math.log(N), dt=0.01)
m = t >= 4.0                       # on écarte les petits t (autres pôles de G dominants)
omega, F, _ = windowed_fourier(t[m], B[m], window="hann")
E = np.abs(F) ** 2
gam, _ = load_zeros()
sel = (omega > 8) & (omega < 80)
om, en = omega[sel], E[sel]
peaks = [i for i in range(1, len(en) - 1) if en[i] > en[i - 1] and en[i] > en[i + 1]]
peaks = sorted(peaks, key=lambda i: -en[i])[:20]
rows = []
for i in sorted(peaks, key=lambda i: om[i]):
    d = np.min(np.abs(gam - om[i]))
    rows.append(dict(pic_omega=om[i], energie=en[i], zero_le_plus_proche=gam[np.argmin(np.abs(gam - om[i]))], ecart=d))
df = pd.DataFrame(rows)
res = 2 * math.pi / (t[m][-1] - t[m][0])
print(df.round(3).to_string(index=False))
print("résolution 2pi/L =", round(res, 3), "| part des 20 plus gros pics à < 0.5 d'un zéro :", float((df.ecart < 0.5).mean()))
df.to_csv(ROOT / "data" / "localisation_zeta.csv", index=False)
