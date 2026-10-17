"""V6.17 — zéros de L(Δ, s) sur la droite critique jusqu'à T (défaut 1 500), par le Contour tourné (src/delta_contour.py).

1. Grille de pas dt (0,005) par bandes de largeur 25 ; changements de signe de Λ(6+it), raffinés par la méthode de Brent.
2. Paires serrées manquées : tout minimum local de |Z| entre deux valeurs de même signe, s'il est petit devant ses voisins,
   est réexaminé sur une grille 100 fois plus fine.
3. Complétude (méthode de Turing, forme simple) : S(t) = N(t) − θ(t)/π doit rester borné et de moyenne nulle par fenêtres ;
   une paire manquée décalerait durablement S de −2.
Sorties : data/delta_zeros_contour.csv (gamma), data/delta_zeros_contour_audit.csv (S par fenêtres de 50 zéros).
"""
import sys, math, time
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.special import loggamma
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from delta_contour import DeltaBand, theta_delta
from delta_ramanujan import tau

def main(T: float = 1500.0, dt: float = 0.005, width: float = 25.0):
    t0 = time.time(); taus = np.array([float(x) for x in tau(3000)])
    zeros, refined = [], 0
    a = 0.5
    while a < T - 1e-9:
        b = min(a + width, T); band = DeltaBand(taus, a, b)
        n = int(round((b - a) / dt)) + 1; tt = a + dt * np.arange(n); v = band.reA_grid(a, dt, n)
        f = lambda t: band.reA(t)[0]
        for i in np.nonzero(np.sign(v[:-1]) * np.sign(v[1:]) < 0)[0]:
            zeros.append(brentq(f, tt[i], tt[i + 1], xtol=1e-12, rtol=1e-15))
        # minima locaux de |Z| sans changement de signe : examen fin (Z = ±|L(Δ, 6+it)|, à partir des mêmes valeurs)
        Zt = 2 * v * np.exp(-band.phi * tt - loggamma(6 + 1j * tt).real + 6 * math.log(2 * math.pi)); aZ = np.abs(Zt)
        for i in range(1, n - 1):
            if aZ[i] < aZ[i - 1] and aZ[i] < aZ[i + 1] and np.sign(Zt[i - 1]) == np.sign(Zt[i]) == np.sign(Zt[i + 1]) \
               and aZ[i] < 0.05 * max(aZ[max(0, i - 40):i + 40].max(), 1e-300):
                fine = tt[i - 1] + (2 * dt / 200) * np.arange(201); vf = band.reA(fine); refined += 1
                for j in np.nonzero(np.sign(vf[:-1]) * np.sign(vf[1:]) < 0)[0]:
                    zeros.append(brentq(f, fine[j], fine[j + 1], xtol=1e-12, rtol=1e-15))
        a = b
        print(f"  bande {a:7.1f}  zéros {len(zeros):5d}  nœuds {band.nodes:6d}  {time.time() - t0:6.0f} s", flush=True)
    g = np.unique(np.round(np.array(zeros), 10))
    pd.DataFrame({"gamma": g}).to_csv(ROOT / "data/delta_zeros_contour.csv", index=False)
    # complétude : S aux milieux entre zéros consécutifs
    mid = 0.5 * (g[:-1] + g[1:]); S = np.arange(1, len(g)) - theta_delta(mid) / math.pi
    rows = [{"k_debut": k, "t_debut": mid[k], "t_fin": mid[min(k + 49, len(mid) - 1)], "S_moyen": S[k:k + 50].mean(),
             "S_min": S[k:k + 50].min(), "S_max": S[k:k + 50].max()} for k in range(0, len(mid), 50)]
    pd.DataFrame(rows).to_csv(ROOT / "data/delta_zeros_contour_audit.csv", index=False)
    print(f"{len(g)} zéros jusqu'à {T} ; minima réexaminés : {refined} ; S moyen global {S.mean():+.3f}, min {S.min():+.3f}, max {S.max():+.3f} ;"
          f" {time.time() - t0:.0f} s")

if __name__ == "__main__":
    main(*(float(x) for x in sys.argv[1:]))
