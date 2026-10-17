"""V6.12 — Les trois idées rejetées (V4.3), relues avec le dictionnaire des opérateurs.

1. Le Kalman / GPS analytique, relu comme récurrence de Levinson sur les traces des premiers : innovations E_n,
   coefficients de réflexion k_n ; première innovation négative = premier pas où la métrique cesse d'être positive.
2. La localisation de sources, relue avec la masse unité : le mode fantôme de DH (Im ≈ 73,8) porte-t-il une masse ?
3. Le Schrödinger H_eff, relu comme générateur des premiers : le Théorème A (exposant Θ − 1/2) lu au rayon spectral.
Aucun zéro n'entre dans les constructions ; les listes de zéros servent de contrôle.
"""
from __future__ import annotations
from pathlib import Path
import sys, math, time
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); D = ROOT / "data"
from prime_generator import traces_from_primes, traces_from_zeros, metric_and_generator, levinson, g_hat, first_negative_size
TAU = 1e-10           # V6.14 : seuils lus sur les valeurs propres (lambda_min < -TAU lambda_max), pas sur le signe des innovations
from rejection import coeffs, log_derivative_coeffs
from zero_reconstruction import nontrivial_zeros

KINDS = ("zeta", "L_chi5", "DH")
NOISE = 1e-7          # en dessous de |E_n / E_0| = 1e-7, le signe d'une innovation n'est plus fiable en double précision
NAME = {"zeta": "ζ", "L_chi5": "L(s, χ₅)", "DH": "DH"}

def main():
    t0 = time.time(); cc = {k: log_derivative_coeffs(coeffs(k, 200000)) for k in KINDS}
    zd = -1j * (nontrivial_zeros("DH") - 0.5); on = zd[np.abs(zd.imag) < 1e-6]; off = zd[np.abs(zd.imag) >= 1e-6]
    quads = sorted({round(abs(g.real), 3) for g in off})[:5]
    # ---- 1. innovations, fenêtre principale (a = 0,04 ; h = 0,01 ; N = 1000 : premiers jusqu'à 23 862)
    a, h, N = 0.04, 0.01, 1000; rows = []
    for k in KINDS:
        t = traces_from_primes(k, cc[k], N, h, a); K, E = levinson(t, N)
        for n in range(N + 1):
            rows.append(dict(objet=k, n=n, longueur=n * h, X=int(math.exp(n * h + 2 * a)), innovation_rel=E[n] / E[0], reflexion=abs(K[n - 1]) if n else 0.0))
    lv = pd.DataFrame(rows); lv.to_csv(D / "reread_levinson.csv", index=False)
    summ = []
    for k in KINDS:
        x = lv[lv.objet == k]; hz = x[x.innovation_rel.abs() < NOISE]; horizon = int(hz.n.iloc[0]) if len(hz) else int(x.n.max())
        before = x[x.n < horizon]; neg = before[before.innovation_rel < -NOISE]   # avant l'horizon seulement
        summ.append(dict(objet=k, horizon_n=horizon, horizon_longueur=horizon * 0.01, horizon_premiers=int(math.exp(horizon * 0.01 + 0.08)),
                         reflexion_max_avant_horizon=float(before.reflexion.max()), premiere_innovation_negative_n=int(neg.n.iloc[0]) if len(neg) else -1,
                         longueur=float(neg.longueur.iloc[0]) if len(neg) else float("nan"), premiers=int(neg.X.iloc[0]) if len(neg) else 0,
                         innovation=float(neg.innovation_rel.iloc[0]) if len(neg) else float("nan")))
        print(f"{NAME[k]} : horizon numérique n = {horizon} ; |k| max avant l'horizon {before.reflexion.max():.3f} ; première innovation négative au-dessus du bruit : "
              f"{'aucune' if neg.empty else f'n = {int(neg.n.iloc[0])}, longueur {neg.longueur.iloc[0]:.2f}, premiers ≤ {int(neg.X.iloc[0])}, E/E0 = {neg.innovation_rel.iloc[0]:.1e}'}", flush=True)
    pd.DataFrame(summ).to_csv(D / "reread_levinson_summary.csv", index=False)
    # ---- 1b. seuil de détection pour DH selon la fonction test et le pas, et quadruplet par quadruplet
    #      (corrigé en V6.14 : critère des valeurs propres ; le signe des innovations était du bruit au-delà de n ≈ 270, cf. document 38)
    th = []
    for a in (0.3, 0.2, 0.12, 0.08, 0.05, 0.04, 0.03):
        for h in (a / 4, a / 2):
            N = int(round(7.0 / h)); t = traces_from_primes("DH", cc["DH"], N, h, a); n1 = first_negative_size(t, TAU, N + 1)
            q1 = off[np.isclose(np.abs(off.real), quads[0], atol=2e-3)]
            n2 = first_negative_size(traces_from_zeros(np.concatenate([on, q1]), N, h, a), TAU, N + 1)
            th.append(dict(a=a, h=h, N=N, poids_rel_85_7=float(abs(g_hat(q1[0], a)) / g_hat(0.0, a).real),
                           longueur_detection=float((n1 - 1) * h) if n1 else float("nan"), premiers_jusqu_a=int(math.exp((n1 - 1) * h + 2 * a)) if n1 else 0,
                           longueur_seul_quadruplet_85_7=float((n2 - 1) * h) if n2 else float("nan")))
    pd.DataFrame(th).to_csv(D / "reread_threshold.csv", index=False)
    qq = []; onp = np.sort(on.real[on.real > 0]); a, h, N = 0.04, 0.01, 900
    for T in quads:
        q = off[np.isclose(np.abs(off.real), T, atol=2e-3)]
        n1 = first_negative_size(traces_from_zeros(np.concatenate([on, q]), N, h, a), TAU, N + 1); d = np.sort(np.abs(onp - T))[:2]
        qq.append(dict(hauteur=T, ecart_a_la_droite=float(abs(q[0].imag)), ecart_voisin_1=float(d[0]), ecart_voisin_2=float(d[1]),
                       poids_rel=float(abs(g_hat(q[0], a)) / g_hat(0.0, a).real), longueur_detection=float((n1 - 1) * h) if n1 else float("nan")))
    pd.DataFrame(qq).to_csv(D / "reread_quadruplets.csv", index=False)
    print("seuils par quadruplet :", [(r["hauteur"], r["longueur_detection"]) for r in qq], flush=True)
    # ---- 2. le fantôme de V4.3 (Im ≈ 73,80 ; Re s = 0,845) pesé par la masse unité
    a, h, N = 0.04, 0.01, 600
    r = metric_and_generator(traces_from_primes("DH", cc["DH"], N, h, a), N, h); mass = r["weight"] / g_hat(r["gamma"], a)
    src = []
    for g, m in zip(r["gamma"], mass):
        if 70 < g.real < 90:
            j = np.argmin(np.abs(zd - g))
            src.append(dict(re=g.real, im=g.imag, masse=abs(m), zero_re=zd[j].real, zero_im=zd[j].imag, ecart=abs(zd[j] - g)))
    sd = pd.DataFrame(src).sort_values("re"); sd.to_csv(D / "reread_sources.csv", index=False)
    near = sd[(sd.re > 73) & (sd.re < 75)]; print("près du fantôme (73 < Re γ < 75) :", near[["re", "im", "masse"]].round(6).to_dict("records"), flush=True)
    # ---- 3. le Théorème A au rayon spectral : Θ − 1/2 = max |Im γ| des valeurs propres de masse 1
    ta = []
    for k in KINDS:
        r = metric_and_generator(traces_from_primes(k, cc[k], N, h, a), N, h); m = r["weight"] / g_hat(r["gamma"], a); gen = np.abs(m - 1) < 1e-6   # valeurs propres bien déterminées
        zz = nontrivial_zeros(k) if k != "zeta" else None
        theta_true = max(0.0, float(np.max(np.abs((nontrivial_zeros(k).real - 0.5))))) if k != "zeta" else 0.0
        ta.append(dict(objet=k, premiers_jusqu_a=int(math.exp(N * h + 2 * a)), exposant_generateur=float(np.max(np.abs(r["gamma"][gen].imag))),
                       exposant_vrai_jusqu_a_t_248=theta_true if k != "DH" else float(np.max(np.abs(zd[np.abs(zd.real) < 250].imag)))))
    pd.DataFrame(ta).to_csv(D / "reread_theoremA.csv", index=False)
    print("Théorème A (Θ − 1/2) :", [(x["objet"], round(x["exposant_generateur"], 6), round(x["exposant_vrai_jusqu_a_t_248"], 6)) for x in ta])
    print(f"total {time.time() - t0:.0f} s")

def figure():
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#52514e",
                         "xtick.color": "#52514e", "ytick.color": "#52514e", "axes.titlesize": 9.5})
    COL = {"zeta": "#2a78d6", "L_chi5": "#eb6834", "DH": "#1baf7a"}; RED, GREY = "#e34948", "#52514e"
    fig, ax = plt.subplots(1, 2, figsize=(12, 3.9), gridspec_kw=dict(width_ratios=[1.25, 1]))
    lv = pd.read_csv(D / "reread_levinson.csv"); A = ax[0]
    for k in KINDS:
        x = lv[(lv.objet == k) & (lv.n > 0)]
        y = np.sign(x.innovation_rel) * np.log10(1 + np.abs(x.innovation_rel) / 1e-9)
        A.plot(x.longueur, y, color=COL[k], lw=1.5, label=NAME[k])
    A.axhline(0, color=GREY, lw=0.8); neg = lv[(lv.objet == "DH") & (lv.innovation_rel < -NOISE)]
    hz = pd.read_csv(D / "reread_levinson_summary.csv").set_index("objet").horizon_longueur["zeta"]
    A.axvspan(hz, lv.longueur.max(), color="#a3a29f", alpha=0.15, lw=0); A.text(hz + 0.1, 3.2, "au-delà : bruit numérique\npour ζ (|E/E₀| < 10⁻⁷)", fontsize=7.5, color=GREY)
    if not neg.empty:
        x0 = neg.longueur.iloc[0]; A.axvline(x0, color=RED, lw=0.8, ls=(0, (3, 3)))
        A.text(x0 - 0.12, -4.6, f"DH : première innovation\nnégative, fenêtre {x0:.2f}\n(premiers ≤ {int(neg.X.iloc[0])})", color=RED, fontsize=7.5, ha="right")
    A.set_xlabel("longueur de la fenêtre n·h (nombres premiers jusqu'à e^(n·h + 2a))"); A.set_ylabel("signe × log₁₀(1 + |E_n/E_0| / 10⁻⁹)")
    A.set_title("Le Kalman relu : innovations de Levinson sur les traces des premiers", loc="left"); A.legend(frameon=False, fontsize=8, loc="upper right")
    sd = pd.read_csv(D / "reread_sources.csv"); B = ax[1]
    B.scatter(sd.re, sd.masse, s=14, c=[COL["DH"] if m > 0.5 else "#a3a29f" for m in sd.masse], zorder=3)
    B.set_yscale("log"); B.axvline(73.80, color=RED, lw=0.8, ls=(0, (3, 3)))
    B.text(73.95, 1e-5, "fantôme de V4.3\n(Im ≈ 73,80 ; Re s = 0,845)", color=RED, fontsize=7.5)
    off = sd[(sd.masse > 0.5) & (sd.im.abs() > 0.05)]
    for _, r in off.iterrows(): B.annotate("85,699 ± 0,309i\n(zéro hors droite, masse 1)", (r.re, r.masse), xytext=(-150, -40), textcoords="offset points", fontsize=7.5, color=GREY, arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6)); break
    B.set_xlabel("Re γ (valeurs propres de l'opérateur des premiers, DH)"); B.set_ylabel("masse portée (1 = un vrai zéro)")
    B.set_title("Les sources relues : la masse unité pèse le fantôme", loc="left")
    fig.tight_layout(w_pad=2.5); fig.savefig(D / "reread.png", dpi=150, bbox_inches="tight"); print("figure écrite")

if __name__ == "__main__":
    if "--figure" not in sys.argv: main()
    figure()
