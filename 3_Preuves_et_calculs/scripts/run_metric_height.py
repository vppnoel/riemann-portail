"""V6.15, coup 2 — La métrique des premiers, plus haut : recenser les quadruplets hors droite de DH jusqu'à |t| = 600.

Plan donné par la loi de seuil (document 38), écrit avant le calcul (data/prevision_v615.md) :
a = 0,012 (lobe principal de ĝ jusqu'à 3π/a ≈ 785), h = 0,004 (fréquence de Nyquist π/h ≈ 785), fenêtre jusqu'à 7,2
(premiers ≤ 1 370). Témoin : L(s, χ5), mêmes paramètres.

1. Nombre de directions négatives de la métrique des premiers (λ < -1e-10 λmax) : DH, L, et DH dont on retire les
   quadruplets hors droite connus (V6.3d jusqu'à 600 ; V6.15 de 600 à 1 100, data/dh_zeros_600_1100.csv).
2. Escalier : nombre de directions négatives selon la longueur de fenêtre.
3. Chaque quadruplet isolé (les autres retirés) : longueur d'allumage, comparée au temps de Heisenberg log(5 γ0 / 2π).
4. Attribution par le générateur : valeurs propres complexes de masse 1 contre la liste des zéros.
Au-delà de la fréquence de Nyquist, une fréquence γ se replie en γ - 2π/h : les zéros de 785 à 1 100 entrent dans la fenêtre.
"""
from __future__ import annotations
from pathlib import Path
import sys, math, time
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); D = ROOT / "data"
from prime_generator import traces_from_primes, g_hat, first_negative_size, metric_and_generator
from rejection import coeffs, log_derivative_coeffs
from zero_reconstruction import nontrivial_zeros
from scipy.linalg import toeplitz, eigvalsh

A, H, N, TAU = 0.012, 0.004, 1800, 1e-10

def traces(gam, w, N, h):
    k = np.arange(N + 1); return (np.asarray(w)[None, :] * np.exp(1j * np.outer(k * h, np.asarray(gam, dtype=complex)))).sum(1)

def negatives(t, n):
    e = eigvalsh(toeplitz(t[:n], np.conj(t[:n]))); return int((e < -TAU * e[-1]).sum())

def offline_list():
    z = -1j * (nontrivial_zeros("DH") - 0.5); off = list(z[np.abs(z.imag) >= 1e-6])
    hi = pd.concat([pd.read_csv(f) for f in sorted(D.glob("dh_zeros_*_*.csv")) if "audit" not in f.name and f.stem.split("_")[-1].isdigit()])
    hi = hi[(hi.sigma - 0.5).abs() > 1e-7]
    for s, t in zip(hi.sigma, hi.t):
        rho = complex(s, t)
        for r in (rho, rho.conjugate()): off.append(-1j * (r - 0.5))
    off = np.array(off); heights = sorted({round(abs(g.real), 3) for g in off})
    return off, heights

def main():
    t0 = time.time()
    tD = traces_from_primes("DH", log_derivative_coeffs(coeffs("DH", 2000)), N, H, A)
    tL = traces_from_primes("L_chi5", log_derivative_coeffs(coeffs("L_chi5", 2000)), N, H, A)
    off, heights = offline_list(); tq = {T: traces(off[np.isclose(np.abs(off.real), T, atol=2e-3)], g_hat(off[np.isclose(np.abs(off.real), T, atol=2e-3)], A), N, H) for T in heights}
    print(f"traces : {time.time() - t0:.0f} s ; quadruplets hors droite connus jusqu'à 1 700 : {len(heights)}", flush=True)
    # ---- 1. recensement à la fenêtre complète
    tZ = traces_from_primes("zeta", log_derivative_coeffs(coeffs("zeta", 2000)), N, H, A)     # contrôle supplémentaire (non pré-enregistré)
    rec = [dict(cas="DH (premiers)", negatives=negatives(tD, N + 1)), dict(cas="L(s, χ5) (premiers), témoin", negatives=negatives(tL, N + 1)),
           dict(cas="ζ (premiers), contrôle non pré-enregistré", negatives=negatives(tZ, N + 1))]
    for cut in (600, 785, 1100, 1700):
        rec.append(dict(cas=f"DH sans les quadruplets ≤ {cut}", negatives=negatives(tD - sum(tq[T] for T in heights if T <= cut), N + 1)))
    pd.DataFrame(rec).to_csv(D / "hauteur_recensement.csv", index=False); print(rec, flush=True)
    # ---- 2. escalier
    ns = list(range(100, N + 2, 25)) + [N + 1]
    st = pd.DataFrame(dict(taille=ns, longueur=[(n - 1) * H for n in ns], negatives_DH=[negatives(tD, n) for n in ns], negatives_L=[negatives(tL, n) for n in ns]))
    st.to_csv(D / "hauteur_escalier.csv", index=False); print("escalier :", st.negatives_DH.tolist(), flush=True)
    # ---- 3. allumage de chaque quadruplet isolé
    tot = sum(tq[T] for T in heights); al = []
    for T in heights:
        n = first_negative_size(tD - tot + tq[T], TAU, N + 1); q = off[np.isclose(np.abs(off.real), T, atol=2e-3)]
        LH = math.log(5 * T / (2 * math.pi)); Lc = None if n is None else (n - 1) * H
        al.append(dict(hauteur=T, delta=float(np.max(np.abs(q.imag))), poids_rel=float(abs(g_hat(q[0], A)) / g_hat(0.0, A).real), replie=T > 785,
                       frequence_vue=float(T if T <= math.pi / H else T - 2 * math.pi / H),
                       L_c=Lc, L_H=LH, rapport=None if Lc is None else Lc / LH))
        print(al[-1], flush=True)
    pd.DataFrame(al).to_csv(D / "hauteur_allumage.csv", index=False)
    # ---- 4. attribution par le générateur
    r = metric_and_generator(tD, N, H); g = r["gamma"]; m = r["weight"] / g_hat(g, A); gen = []
    for T in heights:
        if T > 785: continue
        q = off[np.isclose(np.abs(off.real), T, atol=2e-3)]
        cand = g[(np.abs(m - 1) < 1e-2) & (np.abs(g.imag) > 5e-3)]
        dist = [float(np.min(np.abs(cand - z))) if len(cand) else np.inf for z in q]
        gen.append(dict(hauteur=T, retrouve=bool(max(dist) < 1e-3), ecart_max=max(dist)))
    pd.DataFrame(gen).to_csv(D / "hauteur_generateur.csv", index=False)
    print("générateur :", [(x["hauteur"], x["retrouve"], f"{x['ecart_max']:.0e}") for x in gen], flush=True)
    print(f"total {time.time() - t0:.0f} s")

def figure():
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#52514e",
                         "xtick.color": "#52514e", "ytick.color": "#52514e", "axes.titlesize": 9.5})
    GREEN, ORANGE, BLUE, GREY, RED = "#1baf7a", "#eb6834", "#2a78d6", "#52514e", "#e34948"
    st = pd.read_csv(D / "hauteur_escalier.csv"); al = pd.read_csv(D / "hauteur_allumage.csv")
    fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.1), gridspec_kw=dict(width_ratios=[1.15, 1]))
    A_ = ax[0]; A_.step(st.longueur, st.negatives_DH, where="post", color=GREEN, lw=1.6, label="DH : directions négatives (premiers)")
    A_.step(st.longueur, st.negatives_L, where="post", color=ORANGE, lw=1.2, label="L(s, χ₅) : témoin")
    x = al.dropna(subset=["L_c"]).sort_values("L_c"); A_.step(x.L_c, 2 * np.arange(1, len(x) + 1), where="post", color=GREY, lw=0.9, ls=(0, (3, 2)), label="somme des allumages isolés (2 par quadruplet)")
    A_.set_xlabel("longueur de la fenêtre (n − 1)·h  (h = 0,004 ; premiers jusqu'à e^(L + 0,024))"); A_.set_ylabel("nombre de directions négatives")
    A_.set_title("Le recensement : deux directions négatives par quadruplet", loc="left"); A_.legend(frameon=False, fontsize=7.5, loc="upper left")
    B = ax[1]; v = al.dropna(subset=["L_c"])
    for rep, col, lab in ((False, GREEN, "quadruplets de DH, |t| ≤ 785"), (True, BLUE, "repliés (785 < |t| ≤ 1 700)")):
        y = v[v.replie == rep]; B.scatter(y.hauteur, y.rapport, s=24, color=col, label=lab, zorder=3)
    B.axhspan(0.8, 0.9, color="#a3a29f", alpha=0.25, lw=0); B.text(110, 0.905, "0,80–0,89 (V6.14, a = 0,04)", fontsize=7.5, color=GREY)
    B.axhline(1, color=GREY, lw=0.6); B.set_xlabel("hauteur γ₀ du quadruplet"); B.set_ylabel("allumage / log(5γ₀ / 2π)")
    for yv in (0.75, 1.05): B.axhline(yv, color=GREY, lw=0.7, ls=(0, (3, 3)))
    B.text(1520, 1.055, "bande pré-enregistrée", fontsize=7, color=GREY, ha="right")
    B.set_title("Chaque quadruplet s'allume près de son temps de Heisenberg", loc="left"); B.set_ylim(0.70, 1.08); B.legend(frameon=False, fontsize=7.5, loc="lower right", bbox_to_anchor=(1.0, 0.18))
    fig.tight_layout(w_pad=2.5); fig.savefig(D / "hauteur.png", dpi=150, bbox_inches="tight"); print("figure écrite")

if __name__ == "__main__":
    if "--figure" not in sys.argv: main()
    figure()
