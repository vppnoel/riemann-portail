"""V6.14 — La loi de seuil des innovations : un quadruplet hors droite s'entend au temps de Heisenberg de sa hauteur.

Question (navigateur, coup « La loi de seuil ») : de quoi dépend la longueur de fenêtre à partir de laquelle la métrique
de Toeplitz des traces cesse d'être positive, quand l'objet a un quadruplet de zéros hors droite ?

1. Correction de la V6.12 : le signe des innovations de Levinson n'est pas fiable dès que G est mal conditionnée,
   même si |E_n/E_0| reste grand. Critère robuste : lambda_min(G_n) < -tau lambda_max(G_n) (dichotomie sur n).
2. Seuils robustes : DH par les premiers ; chaque quadruplet réel de DH isolé (fond complet, calculé par les premiers).
3. Quadruplets synthétiques ajoutés au fond complet de L(s, chi_5) et de zeta (traces des premiers) : hauteur, écart
   à la droite, poids, position entre deux zéros, retrait de zéros, pas h, largeur a.
4. Loi : longueur de détection L_c ≈ temps de Heisenberg log(q gamma0 / 2 pi) (prévision enregistrée avant le calcul
   de zeta, du pas, de la largeur et du « trou »).
5. Lemme d'inertie (complément de Schur) vérifié ; précision étendue (mpmath) sur deux configurations.
Les zéros ne servent qu'aux quadruplets synthétiques, au retrait de zéros et aux contrôles.
"""
from __future__ import annotations
from pathlib import Path
import sys, math, time
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); D = ROOT / "data"
from prime_generator import traces_from_primes, levinson, g_hat, lmin_ratio, first_negative_size, heisenberg_length
from rejection import coeffs, log_derivative_coeffs
from zero_reconstruction import nontrivial_zeros

TAU = 1e-10                      # seuil relatif sur lambda_min / lambda_max (bruit des valeurs propres : ~1e-15)
A0, H0, N0 = 0.04, 0.01, 900     # fenêtre principale
Q = {"zeta": 1, "L_chi5": 5, "DH": 5}

def traces(gam, w, N, h):
    k = np.arange(N + 1); return (np.asarray(w)[None, :] * np.exp(1j * np.outer(k * h, np.asarray(gam, dtype=complex)))).sum(1)

def quad(g0, d):
    return np.array([g0 - 1j * d, g0 + 1j * d, -g0 - 1j * d, -g0 + 1j * d])

def qtr(g0, d, a, h, N, c=1.0):
    q = quad(g0, d); return c * traces(q, g_hat(q, a), N, h)

def zeros_split(kind):
    z = -1j * (nontrivial_zeros(kind) - 0.5); return z[np.abs(z.imag) < 1e-6].real, z[np.abs(z.imag) >= 1e-6]

def L_of(n, h):
    """Taille n de G -> longueur de fenêtre (plus grand décalage) (n - 1) h."""
    return None if n is None else (n - 1) * h

def main():
    t0 = time.time(); CC = {k: log_derivative_coeffs(coeffs(k, 200000)) for k in Q}
    bg = {}
    def B(kind, a=A0, h=H0, N=N0):
        if (kind, a, h, N) not in bg: bg[(kind, a, h, N)] = traces_from_primes(kind, CC[kind], N, h, a)
        return bg[(kind, a, h, N)]
    onL, _ = zeros_split("L_chi5"); posL = np.sort(onL[onL > 0]); onD, offD = zeros_split("DH")
    zz = -1j * (nontrivial_zeros("zeta") - 0.5); posZ = np.sort(zz.real[zz.real > 0])
    mid = lambda pos, T, f=0.5: float(pos[np.searchsorted(pos, T) - 1] + f * (pos[np.searchsorted(pos, T)] - pos[np.searchsorted(pos, T) - 1]))
    quads = sorted({round(abs(g.real), 3) for g in offD})[:5]

    # ---- 1. correction de la V6.12 : innovations et valeurs propres sur le fond de DH (zéros sur la droite seuls)
    tb = traces(onD, g_hat(onD, A0), N0, H0); K, E = levinson(tb, N0); rows = []
    for n in (100, 200, 250, 270, 280, 290, 295, 300, 350, 400):
        rows.append(dict(taille=n + 1, innovation_rel=E[n] / E[0], lmin_sur_lmax=lmin_ratio(tb, n + 1)))
    corr = pd.DataFrame(rows); corr.to_csv(D / "seuil_correction_fond.csv", index=False)
    print("fond de DH sur la droite (aucune direction négative possible) :", corr.round(20).to_dict("records")[4:7], flush=True)

    # ---- 2. seuils robustes : DH complet par les premiers ; ζ et L ; quadruplets réels isolés
    real = []
    for k in Q:
        n = first_negative_size(B(k), TAU, N0 + 1)
        real.append(dict(cas=f"{k} complet (premiers)", hauteur=np.nan, delta=np.nan, n_c=n, L_c=L_of(n, H0), L_H=np.nan))
    for T in quads:
        q = offD[np.isclose(np.abs(offD.real), T, atol=2e-3)]; oth = offD[~np.isclose(np.abs(offD.real), T, atol=2e-3)]
        n = first_negative_size(B("DH") - traces(oth, g_hat(oth, A0), N0, H0), TAU, N0 + 1)
        nz = first_negative_size(tb + traces(q, g_hat(q, A0), N0, H0), TAU, N0 + 1)
        real.append(dict(cas="DH, quadruplet isolé (premiers)", hauteur=T, delta=float(abs(q[0].imag)), n_c=n, L_c=L_of(n, H0),
                         L_H=heisenberg_length(5, T), L_c_modele_zeros=L_of(nz, H0), poids_rel=float(abs(g_hat(q[0], A0)) / g_hat(0.0, A0).real)))
    rd = pd.DataFrame(real); rd.to_csv(D / "seuil_reels.csv", index=False)
    print(rd[["cas", "hauteur", "L_c", "L_H"]].round(3).to_string(index=False), flush=True)

    # ---- 3. quadruplets synthétiques sur les fonds complets
    syn = []
    def add(exp, kind, g0, d=0.2, c=1.0, a=A0, h=H0, N=N0, extra=None, base=None):
        t = (B(kind, a, h, N) if base is None else base) + qtr(g0, d, a, h, N, c)
        n = first_negative_size(t, TAU, N + 1)
        r = dict(experience=exp, fond=kind, hauteur=g0, delta=d, poids_mult=c, a=a, h=h, n_c=n, L_c=L_of(n, h), L_H=heisenberg_length(Q[kind], g0),
                 poids_rel=float(abs(g_hat(g0 - 1j * d, a)) / g_hat(0.0, a).real))
        r.update(extra or {}); r["rapport"] = r["L_c"] / r["L_H"] if r["L_c"] else np.nan; syn.append(r); return r
    for T in (20, 40, 60, 80, 100, 130, 160, 200, 240, 280): add("hauteur", "L_chi5", mid(posL, T))
    for T in (30, 50, 100, 150, 200): add("hauteur", "zeta", mid(posZ, T))
    g100 = mid(posL, 100)
    for d in (0.01, 0.05, 0.1, 0.2, 0.4, 0.8): add("ecart_a_la_droite", "L_chi5", g100, d=d)
    for c in (1e-6, 1e-3, 1.0, 1e3): add("poids", "L_chi5", g100, c=c)
    for f in (0.05, 0.2, 0.35, 0.5, 0.65, 0.8, 0.95): add("position", "L_chi5", mid(posL, 100, f), extra=dict(fraction_entre_zeros=f))
    for cut in (30, 50, 80):
        sub = onL[np.abs(onL) < cut]; add("retrait_zeros_bas", "L_chi5", g100, base=B("L_chi5") - traces(sub, g_hat(sub, A0), N0, H0), extra=dict(retires=int(len(sub))))
    for h, N in ((0.02, 450), (0.005, 1800)): add("pas", "L_chi5", g100, h=h, N=N)
    for a in (0.03, 0.06): add("largeur", "L_chi5", g100, a=a)
    for T in quads:   # analogue synthétique de chaque quadruplet réel : même hauteur, même écart, zéro voisin remplacé
        d = float(abs(offD[np.isclose(np.abs(offD.real), T, atol=2e-3)][0].imag))
        i = np.argmin(np.abs(posL - T)); j = np.argmin(np.abs(onL + T)); rm = np.array([posL[i], onL[j]])
        add("analogue_DH_trou", "L_chi5", T, d=d, base=B("L_chi5") - traces(rm, g_hat(rm, A0), N0, H0))
        add("analogue_DH_ajout", "L_chi5", T, d=d)
    sd = pd.DataFrame(syn); sd.to_csv(D / "seuil_synthetiques.csv", index=False)
    for e, x in sd.groupby("experience", sort=False):
        print(e, x[["fond", "hauteur", "delta", "poids_mult", "h", "a", "L_c", "L_H", "rapport"]].round(3).values.tolist(), flush=True)

    # ---- 4. lemme d'inertie : G = B + U C U*, nombre de valeurs propres négatives = pos(C^-1 + U* B^-1 U) - 2 par paire...
    from scipy.linalg import toeplitz, eigvalsh, solve
    tb5 = B("L_chi5", A0, H0, 300)[:301]; q = quad(g100, 0.2); w = 1000.0 * g_hat(q, A0); tt = tb5 + traces(q, w, 300, H0); inert = []
    for n in range(76, 90):
        G = toeplitz(tt[:n], np.conj(tt[:n])); e = eigvalsh(G); direct = int((e < -1e-10 * e[-1]).sum())
        Bn = toeplitz(tb5[:n], np.conj(tb5[:n])); j = np.arange(n); U = []; C = np.zeros((4, 4), complex)
        for b, (g1, w1) in enumerate(((q[0], w[0]), (q[2], w[2]))):
            U += [np.exp(1j * g1 * j * H0), np.exp(1j * np.conj(g1) * j * H0)]; C[2 * b:2 * b + 2, 2 * b:2 * b + 2] = [[0, w1], [np.conj(w1), 0]]
        U = np.array(U).T; M = np.linalg.inv(C) + U.conj().T @ solve(Bn, U, assume_a="her"); M = (M + M.conj().T) / 2
        inert.append(dict(taille=n, negatives_directes=direct, negatives_par_le_lemme=int((np.linalg.eigvalsh(M) > 0).sum()) - 2,
                          ecart_reconstruction=float(np.max(np.abs(Bn + U @ C @ U.conj().T - G)) / abs(tt[0]))))
    pd.DataFrame(inert).to_csv(D / "seuil_inertie.csv", index=False)
    print("lemme d'inertie :", [(r["taille"], r["negatives_directes"], r["negatives_par_le_lemme"]) for r in inert], flush=True)

    # ---- 5. précision étendue : premier changement de signe exact (modèle à zéros, fond L sur la droite)
    prec = []
    try:
        import mpmath as mp
        W = (mp.mpf(3) / 8, mp.mpf(1) / 2, mp.mpf(1) / 8)
        def ghat(r, a):
            s = 0
            for k, wk in enumerate(W):
                for sg in (1, -1):
                    z = (r + sg * k * mp.pi / a) * a; s += wk * a * (mp.mpf(1) if z == 0 else mp.sin(z) / z)
            return s * s
        for g0, c in ((g100, 1.0), (mid(posL, 20), 1.0)):
            for dps in (30, 80):
                mp.mp.dps = dps; a, h = mp.mpf("0.04"), mp.mpf("0.01"); gam = [mp.mpf(float(x)) for x in onL] + [mp.mpc(z.real, z.imag) for z in quad(g0, 0.2)]
                wts = [ghat(gg, a) for gg in gam]; Nm = 520; t = [mp.mpc(0)] * (Nm + 1)
                for gg, ww in zip(gam, wts):
                    zst = mp.exp(1j * gg * h); p = mp.mpc(ww)
                    for k in range(Nm + 1): t[k] += p; p *= zst
                av = [mp.mpc(1)]; Ev = [t[0].real]; first = None
                for m in range(1, Nm + 1):
                    acc = t[m] + mp.fsum(av[i] * t[m - i] for i in range(1, m)); kk = -acc / Ev[-1]
                    ext = av + [mp.mpc(0)]; av = [ext[i] + kk * mp.conj(ext[m - i]) for i in range(m + 1)]; Ev.append((Ev[-1] * (1 - abs(kk) ** 2)).real)
                    if Ev[-1] < 0: first = m; break
                tz = traces(np.concatenate([onL, quad(g0, 0.2)]), g_hat(np.concatenate([onL, quad(g0, 0.2)]), A0), Nm, H0)
                nd = first_negative_size(tz, TAU, Nm + 1)
                prec.append(dict(hauteur=g0, chiffres=dps, premiere_innovation_negative_n=first, L_exact=None if first is None else first * 0.01,
                                 L_double_valeurs_propres=L_of(nd, H0)))
                print("précision étendue :", prec[-1], flush=True)
    except ImportError:
        print("mpmath absent : contrôle en précision étendue non exécuté")
    pd.DataFrame(prec).to_csv(D / "seuil_precision.csv", index=False)
    print(f"total {time.time() - t0:.0f} s")

def figure():
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#52514e",
                         "xtick.color": "#52514e", "ytick.color": "#52514e", "axes.titlesize": 9.5})
    BLUE, ORANGE, GREEN, RED, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#e34948", "#52514e"
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.2), gridspec_kw=dict(width_ratios=[1.15, 1, 1]))
    # A : le seuil net, et le bruit que la V6.12 prenait pour un signal
    CC = log_derivative_coeffs(coeffs("DH", 200000)); tD = traces_from_primes("DH", CC, 500, H0, A0)
    onD, offD = zeros_split("DH"); tb = traces(onD, g_hat(onD, A0), 500, H0)
    ns = np.arange(150, 451, 5); A = ax[0]
    f = lambda v: np.sign(v) * np.log10(1 + np.abs(v) / 1e-15)
    A.plot((ns - 1) * H0, [f(lmin_ratio(tD, n)) for n in ns], color=GREEN, lw=1.6, label="DH, traces des premiers")
    A.plot((ns - 1) * H0, [f(lmin_ratio(tb, n)) for n in ns], color=GREY, lw=1.2, ls=(0, (4, 2)), label="fond de DH sur la droite seul (modèle à zéros)")
    A.axhspan(-1, 1, color="#a3a29f", alpha=0.25, lw=0); A.text(3.62, 1.4, "bruit des valeurs propres (10⁻¹⁵)", fontsize=7.5, color=GREY)
    A.axhline(f(-1e-10), color=RED, lw=0.7, ls=(0, (2, 2))); A.text(1.55, f(-1e-10) - 1.2, "seuil τ = 10⁻¹⁰", fontsize=7.5, color=RED)
    A.set_xlabel("longueur de la fenêtre (n − 1)·h"); A.set_ylabel("signe × log₁₀(1 + |λ_min/λ_max| / 10⁻¹⁵)")
    A.axvline(2.7, color=GREY, lw=0.7, ls=(0, (1, 2))); A.text(2.72, -7.5, "au-delà, le signe des\ninnovations de Levinson\nn'est plus fiable :\nles seuils V6.12 de\n2,71 à 3,30 étaient du bruit", fontsize=7, color=GREY)
    A.set_title("Un seuil net : λ_min/λ_max passe de +10⁻¹¹ à −10⁻² entre 3,5 et 3,7", loc="left"); A.legend(frameon=False, fontsize=7.5, loc="lower left")
    # B : la loi de Heisenberg
    sd = pd.read_csv(D / "seuil_synthetiques.csv"); rd = pd.read_csv(D / "seuil_reels.csv"); Bx = ax[1]
    h1 = sd[(sd.experience == "hauteur")]
    for kind, col, lab in (("L_chi5", ORANGE, "L(s, χ₅) + quadruplet ajouté"), ("zeta", BLUE, "ζ + quadruplet ajouté")):
        x = h1[h1.fond == kind]; Bx.scatter(x.L_H, x.L_c, s=22, color=col, label=lab, zorder=3)
    x = rd.dropna(subset=["L_H"]); Bx.scatter(x.L_H, x.L_c, s=34, marker="D", color=GREEN, label="DH : quadruplets réels", zorder=4)
    lim = np.array([1.2, 6.0]); Bx.plot(lim, lim, color=GREY, lw=0.8); Bx.fill_between(lim, 0.8 * lim, 1.1 * lim, color="#a3a29f", alpha=0.18, lw=0)
    Bx.text(4.6, 3.55, "0,8 à 1,1 × L_H", fontsize=7.5, color=GREY)
    Bx.annotate("hauteurs 240 et 280 : au-delà du\nlobe principal de ĝ (poids < 10⁻⁵)", (5.33, 6.6), xytext=(1.3, 4.9), fontsize=7, color=GREY, arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    Bx.set_xlabel("temps de Heisenberg L_H = log(q·γ₀ / 2π)"); Bx.set_ylabel("longueur de détection L_c"); Bx.legend(frameon=False, fontsize=7.5, loc="upper left")
    Bx.set_title("Le quadruplet s'entend au temps de Heisenberg de sa hauteur", loc="left")
    # C : ce qui compte peu
    Cx = ax[2]; dd = sd[sd.experience == "ecart_a_la_droite"]; pw = sd[sd.experience == "poids"]
    Cx.plot(dd.delta, dd.rapport, "o-", color=ORANGE, lw=1.4, ms=4, label="écart à la droite δ (axe du bas)")
    Cx.set_xlabel("écart à la droite δ"); Cx.set_ylabel("L_c / L_H"); Cx.set_ylim(0.55, 1.45)
    Cx.text(0.79, 0.58, "c = 10³ : 0,19 ↓", fontsize=7.5, color=BLUE, ha="right"); Cx.axhline(1, color=GREY, lw=0.6)
    C2 = Cx.twiny(); C2.plot(np.log10(pw.poids_mult), pw.rapport, "s--", color=BLUE, lw=1.2, ms=4, label="poids × c (axe du haut, log₁₀ c)")
    C2.set_xlabel("log₁₀ c (poids du quadruplet multiplié par c)", color=BLUE); C2.tick_params(axis="x", colors=BLUE); C2.spines["top"].set_visible(True)
    h1x, l1 = Cx.get_legend_handles_labels(); h2x, l2 = C2.get_legend_handles_labels(); Cx.legend(h1x + h2x, l1 + l2, frameon=False, fontsize=7.5, loc="lower left")
    Cx.set_title("Corrections : δ et poids (hauteur ≈ 100, fond L)", loc="left", pad=28)
    fig.tight_layout(w_pad=2.2); fig.savefig(D / "seuil.png", dpi=150, bbox_inches="tight"); print("figure écrite")

if __name__ == "__main__":
    if "--figure" not in sys.argv: main()
    figure()
