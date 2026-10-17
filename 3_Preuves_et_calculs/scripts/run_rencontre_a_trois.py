"""V6.16 — La Rencontre à trois : RH, simplicité des zéros et répulsion lues sur les mêmes paires de zéros de ζ.

Prévisions écrites avant le calcul : data/prevision_v616.md.

Pour chaque zéro ρ_k = 1/2 + iγ_k de ζ (1 070 zéros jusqu'à t = 1 500, plus la paire de Lehmer près de 7 005) :
- écart normalisé au plus proche voisin s_k = g_k · log(γ_k/2π) / 2π ;
- marge locale de la métrique à la fenêtre de Heisenberg : m_k = 1 − sinc²(π s_k), sinc(x) = sin x / x.
  C'est le déterminant normalisé du Gram des deux exponentielles e^{iγ j h} de la paire sur une fenêtre de longueur
  L_H = log(γ/2π) (limite h → 0), et c'est aussi la densité de corrélation de paires de Montgomery R2(s) ;
- part dans le coefficient β de Q : β_k = 2|u_k|², u_k = (b_ρ − 2/ρ)/ρ, b_ρ = ζ''/ζ'(ρ) − 2γ_E,
  avec ζ''/ζ'(ρ) = −i Z''/Z'(γ) − 2θ'(γ) (fonction Z de Hardy), calculée par mpmath, sans les premiers.
Comparaisons : surmise de Wigner (GUE) et Poisson ; sommes par blocs dyadiques de Σ 4/(g²|ρ|²) pour des suites simulées.
Exploratoire : la marge locale lue sur la métrique des premiers (fenêtre de Heisenberg) pour les paires les plus serrées.
"""
from __future__ import annotations
from pathlib import Path
import sys, math, time
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); D = ROOT / "data"

EULER_GAMMA = 0.5772156649015329

def sinc(x): return np.where(np.abs(x) < 1e-12, 1.0, np.sin(x) / np.where(np.abs(x) < 1e-12, 1.0, x))

def margin(s): return 1 - sinc(np.pi * np.asarray(s, dtype=float)) ** 2

def wigner_cdf(s):                    # surmise GUE (β = 2), écarts consécutifs
    from scipy.integrate import quad
    return quad(lambda x: 32 / math.pi ** 2 * x * x * math.exp(-4 * x * x / math.pi), 0, s)[0]

def nn_fraction_wigner(s):            # plus proche voisin = min de deux écarts consécutifs, supposés indépendants (approximation)
    F = wigner_cdf(s); return 1 - (1 - F) ** 2

def zeros_data(gam, mp, dps=20):
    rows = []
    with mp.workdps(dps):
        for g in gam:
            z1 = mp.siegelz(g, derivative=1); z2 = mp.siegelz(g, derivative=2); th = mp.siegeltheta(g, derivative=1)
            rows.append((float(z2 / z1), float(th)))
    zz = np.array(rows); r, thp = zz[:, 0], zz[:, 1]
    rho = 0.5 + 1j * np.asarray(gam)
    b = -2 * thp - 2 * EULER_GAMMA - 1j * r
    u = (b - 2 / rho) / rho
    return r, thp, 2 * np.abs(u) ** 2

def main():
    import mpmath as mp
    t0 = time.time()
    g = np.sort(pd.read_csv(D / "zeta_zeros_1500.csv").t.values); g = g[g > 0]
    gap_l = np.r_[np.inf, np.diff(g)]; gap_r = np.r_[np.diff(g), np.inf]; gap = np.minimum(gap_l, gap_r)
    s = gap * np.log(g / (2 * math.pi)) / (2 * math.pi); m = margin(s)
    r, thp, beta = zeros_data(g, mp)
    beta_e = 2 * r ** 2 / (0.25 + g ** 2)       # part de β_k sensible aux écarts : 2 (Z''/Z')² / |ρ|²
    z = pd.DataFrame(dict(gamma=g, ecart=gap, s=s, marge=m, ZppZp=r, theta_p=thp, beta_k=beta, beta_ecart=beta_e, voisin_droite=gap_r < gap_l))
    z.to_csv(D / "rencontre_zeros.csv", index=False); print(f"{len(g)} zéros : Z''/Z' et β_k en {time.time() - t0:.0f} s ; Σβ_k = {beta.sum():.4f}", flush=True)

    # ---- P1 : répulsion (proportion de marges < 0,1)
    s_star = float(mp.findroot(lambda x: 1 - (mp.sin(mp.pi * x) / (mp.pi * x)) ** 2 - mp.mpf("0.1"), 0.18))
    sc = np.diff(g) * np.log(g[:-1] / (2 * math.pi)) / (2 * math.pi)        # écarts consécutifs normalisés
    rep = dict(seuil_marge=0.1, seuil_s=s_star, fraction_zeros=float((m < 0.1).mean()), fraction_gue_wigner=nn_fraction_wigner(s_star),
               fraction_poisson=1 - math.exp(-2 * s_star), paires_consecutives=float((sc < s_star).mean()),
               paires_gue_wigner=wigner_cdf(s_star), paires_poisson=1 - math.exp(-s_star))
    # ---- P2, P3 : β lit les paires serrées
    o = np.argsort(s); k10 = len(g) // 10
    slope = float(np.polyfit(np.log(s[o[:k10]]), np.log(beta[o[:k10]]), 1)[0])
    om = np.argsort(m); share = float(beta[om[:k10]].sum() / beta.sum())
    nn = np.where(gap_l < gap_r, -1.0, 1.0); approx = -2 / (nn * gap)
    rep.update(somme_beta_ecart=float(beta_e.sum()), part_ecart_dans_beta=float(beta_e.sum() / beta.sum()),
               part_beta_ecart_10pc=float(beta_e[o[:k10]].sum() / beta_e.sum()), pente_logbetaecart_logs_10pc=float(np.polyfit(np.log(s[o[:k10]]), np.log(beta_e[o[:k10]]), 1)[0]))
    rep.update(pente_logbeta_logs_10pc=slope, part_beta_10pc_marges=share, somme_beta=float(beta.sum()),
               corr_ZppZp_moins2_sur_g_10pc=float(np.corrcoef(r[o[:k10]], approx[o[:k10]])[0, 1]))
    # ---- P5 : la paire de Lehmer près de 7 005, et les zéros de 6 900 à 7 100
    n1, n2 = int(mp.nzeros(6900)) + 1, int(mp.nzeros(7100))
    gl = np.array([float(mp.zetazero(n).imag) for n in range(n1 - 1, n2 + 2)])
    rl, thl, bl = zeros_data(gl, mp)
    gapl = np.minimum(np.r_[np.inf, np.diff(gl)], np.r_[np.diff(gl), np.inf]); sl = gapl * np.log(gl / (2 * math.pi)) / (2 * math.pi)
    inner = (gl >= 6900) & (gl <= 7100); med = float(np.median(bl[inner]))
    j = int(np.argmin(np.abs(gl - 7005.06)))
    ble = 2 * rl ** 2 / (0.25 + gl ** 2); mede = float(np.median(ble[inner]))
    leh = pd.DataFrame(dict(gamma=gl, s=sl, marge=margin(sl), ZppZp=rl, theta_p=thl, beta_k=bl, rapport_a_la_mediane=bl / med, beta_ecart=ble, rapport_ecart_a_la_mediane=ble / mede))
    leh.to_csv(D / "rencontre_lehmer.csv", index=False)
    rep.update(lehmer_gamma_1=float(gl[j]), lehmer_gamma_2=float(gl[j + 1]), lehmer_s=float(sl[j]), lehmer_marge=float(margin(sl[j])),
               lehmer_beta_sur_mediane_1=float(bl[j] / med), lehmer_beta_sur_mediane_2=float(bl[j + 1] / med), zeros_6900_7100=int(inner.sum()),
               lehmer_ecart_sur_mediane_1=float(ble[j] / mede), lehmer_ecart_sur_mediane_2=float(ble[j + 1] / mede), lehmer_part_ecart=float(ble[j] / bl[j]))
    print("Lehmer :", {k: rep[k] for k in rep if k.startswith("lehmer")}, flush=True)
    # ---- heuristique : Σ 4/(g²|ρ|²) par blocs dyadiques, suites simulées (Poisson, Wigner) contre ζ
    rng = np.random.default_rng(616); T0, T1 = 50.0, 2.0e6; blocks = []
    for law in ("poisson", "wigner"):     # écarts indépendants : exponentiels (Poisson) ou surmise de Wigner (loi de Maxwell, moyenne 1)
        tl, gl_, t = [], [], T0
        while t < T1:
            dens = math.log(t / (2 * math.pi)) / (2 * math.pi); k = 200000
            sp = rng.exponential(1.0, k) if law == "poisson" else math.sqrt(math.pi / 8) * np.sqrt((rng.standard_normal((k, 3)) ** 2).sum(1))
            gg = sp / dens; tt = t + np.cumsum(gg); tl.append(tt); gl_.append(gg); t = float(tt[-1])
        tt = np.concatenate(tl); gg = np.concatenate(gl_); keep = tt < T1; tt, gg = tt[keep], gg[keep]
        gmin = np.minimum(gg, np.r_[gg[1:], np.inf])      # plus proche voisin (écart à gauche ou à droite)
        for e in range(int(math.log2(T0)), int(math.log2(T1))):
            sel = (tt >= 2 ** e) & (tt < 2 ** (e + 1))
            blocks.append(dict(loi=law, bloc_debut=2 ** e, somme=float(np.sum(4 / (gmin[sel] ** 2 * tt[sel] ** 2))), zeros=int(sel.sum()),
                               plus_petit_s=float(np.min(gmin[sel] * np.log(tt[sel] / (2 * math.pi)) / (2 * math.pi)))))
    for e in range(int(math.log2(T0)), int(math.log2(1500))):
        sel = (g >= 2 ** e) & (g < 2 ** (e + 1))
        blocks.append(dict(loi="zeta", bloc_debut=2 ** e, somme=float(np.sum(4 / (gap[sel] ** 2 * g[sel] ** 2))), zeros=int(sel.sum()), plus_petit_s=float(s[sel].min())))
    pd.DataFrame(blocks).to_csv(D / "rencontre_blocs.csv", index=False)
    # ---- exploratoire : la marge lue sur la métrique des premiers (fenêtre de Heisenberg), paires les plus serrées sous 550
    try:
        from prime_generator import traces_from_primes, g_hat
        from rejection import coeffs, log_derivative_coeffs
        from scipy.linalg import toeplitz, eigh
        A, H = 0.012, 0.004; Nmax = int(math.log(550 / (2 * math.pi)) / H) + 2
        tz = traces_from_primes("zeta", log_derivative_coeffs(coeffs("zeta", 2000)), Nmax, H, A); ex = []
        low = np.where(g < 550)[0]; cand = low[np.argsort(s[low])][:24]; seen = set()
        for k in cand:
            kk = k if gap_r[k] <= gap_l[k] else k - 1
            if kk in seen or kk + 1 >= len(g): continue
            seen.add(kk); g1, g2 = g[kk], g[kk + 1]; LH = math.log(0.5 * (g1 + g2) / (2 * math.pi)); n = int(round(LH / H)) + 1
            G = toeplitz(tz[:n], np.conj(tz[:n])); j = np.arange(n)
            X = np.stack([np.exp(1j * g1 * j * H), np.exp(1j * g2 * j * H)], 1)
            M = X.conj().T @ G @ X                                       # la métrique des premiers, comprimée sur la paire
            dm = float((np.linalg.det(M) / (M[0, 0] * M[1, 1])).real)
            sp = (g2 - g1) * math.log(0.5 * (g1 + g2) / (2 * math.pi)) / (2 * math.pi)
            sig = abs(np.vdot(X[:, 0], X[:, 1])) / n; w1, w2 = g_hat(g1, A).real, g_hat(g2, A).real
            two = (w1 * w2 * (1 - sig ** 2) ** 2) / ((w1 + w2 * sig ** 2) * (w2 + w1 * sig ** 2))   # modèle à deux atomes
            ex.append(dict(gamma_1=g1, gamma_2=g2, s=sp, marge_heisenberg=float(margin(sp)), marge_gram=1 - sig ** 2, det_premiers=dm, det_deux_atomes=float(two)))
        pd.DataFrame(ex).to_csv(D / "rencontre_premiers.csv", index=False)
        print("exploratoire (premiers) :", pd.DataFrame(ex)[["gamma_1", "s", "marge_heisenberg", "marge_gram", "det_premiers", "det_deux_atomes"]].round(3).head(8).to_dict("records"), flush=True)
    except Exception as e:
        print("exploratoire non exécuté :", e)
    pd.DataFrame([rep]).to_csv(D / "rencontre_resume.csv", index=False)
    print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in rep.items()})
    print(f"total {time.time() - t0:.0f} s")

def figure():
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#52514e",
                         "xtick.color": "#52514e", "ytick.color": "#52514e", "axes.titlesize": 9.5})
    BLUE, ORANGE, VIOLET, GREY, RED = "#2a78d6", "#eb6834", "#4a3aa8", "#52514e", "#e34948"
    z = pd.read_csv(D / "rencontre_zeros.csv"); L = pd.read_csv(D / "rencontre_lehmer.csv"); b = pd.read_csv(D / "rencontre_blocs.csv")
    g = z.gamma.values; sc = np.diff(g) * np.log(g[:-1] / (2 * math.pi)) / (2 * math.pi)
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))
    A = ax[0]; x = np.linspace(0, 3, 400)
    A.hist(sc, bins=np.linspace(0, 3, 31), density=True, color="#a3a29f", alpha=0.55, label="écarts consécutifs de ζ (1 069)")
    A.plot(x, 32 / np.pi ** 2 * x ** 2 * np.exp(-4 * x ** 2 / np.pi), color=BLUE, lw=1.5, label="GUE (surmise de Wigner)")
    A.plot(x, np.exp(-x), color=ORANGE, lw=1.2, ls=(0, (4, 2)), label="Poisson (sans répulsion)")
    A.plot(x, margin(x), color=VIOLET, lw=1.8, label="marge locale 1 − sinc²(πs) = R₂(s)")
    j = int(np.argmin(np.abs(L.gamma.values - 7005.06))); sl = float(L.s.values[j])
    A.scatter([sl], [float(margin(sl))], s=40, marker="*", color=RED, zorder=4)
    A.annotate(f"paire de Lehmer (7 005) :\ns = {sl:.3f}, marge {float(margin(sl)):.4f}", (sl, float(margin(sl))), xytext=(1.7, 0.45), fontsize=7.5, color=RED, arrowprops=dict(arrowstyle="-", color=RED, lw=0.7))
    A.set_xlabel("écart normalisé s"); A.set_ylabel("densité / marge"); A.set_ylim(0, 1.35); A.legend(frameon=False, fontsize=7.2, loc="upper right")
    A.set_title("La marge de la métrique est la corrélation de Montgomery", loc="left")
    B = ax[1]   # quantités normalisées par l'écart moyen Δ = 2π / log(γ/2π) : la hauteur disparaît
    for frame, mk, sz in ((z, "o", 6), (L, "*", 60)):
        dl = 2 * math.pi / np.log(frame.gamma.values / (2 * math.pi))
        yl = ((2 * frame.theta_p.values + 2 * EULER_GAMMA) * dl / 2) ** 2; ye = (frame.ZppZp.values * dl / 2) ** 2
        if mk == "o":
            B.scatter(frame.s, yl, s=sz, color="#a3a29f", label="terme lisse de β (θ′), normalisé"); B.scatter(frame.s, ye, s=sz, color=VIOLET, label="part d'écart (Z″/Z′)², normalisée")
        else:
            jj = int(np.argmin(np.abs(frame.gamma.values - 7005.06))); B.scatter(frame.s.values[jj:jj + 2], ye[jj:jj + 2], s=sz, marker="*", color=RED, zorder=4, label="paire de Lehmer (7 005)")
    xx = np.array([0.03, 1.5]); B.plot(xx, xx ** -2.0, color=GREY, lw=0.9, ls=(0, (3, 2))); B.text(0.05, 700, "1 / s²", fontsize=8, color=GREY)
    B.set_xscale("log"); B.set_yscale("log"); B.set_ylim(1e-6, 2e3); B.set_xlabel("écart normalisé s (plus proche voisin)"); B.set_ylabel("(· × Δ/2)²")
    B.set_title("β : sa part d'écart suit 1/s² et ne domine que sous s ≈ 0,3", loc="left"); B.legend(frameon=False, fontsize=7.2, loc="lower left")
    C = ax[2]
    for law, col, lab in (("poisson", ORANGE, "écarts de Poisson (simulés)"), ("wigner", BLUE, "écarts de Wigner (simulés)"), ("zeta", VIOLET, "zéros de ζ")):
        y = b[b.loi == law]; C.plot(y.bloc_debut, y.somme, "o-", color=col, lw=1.3, ms=3.5, label=lab)
    C.set_xscale("log"); C.set_yscale("log"); C.set_xlabel("bloc dyadique [T, 2T)"); C.set_ylabel("Σ 4 / (g² γ²) sur le bloc")
    C.set_title("Heuristique : sans répulsion, la somme ne décroît pas", loc="left"); C.legend(frameon=False, fontsize=7.2, loc="lower left")
    fig.tight_layout(w_pad=2.2); fig.savefig(D / "rencontre.png", dpi=150, bbox_inches="tight"); print("figure écrite")

if __name__ == "__main__":
    if "--figure" not in sys.argv: main()
    figure()
