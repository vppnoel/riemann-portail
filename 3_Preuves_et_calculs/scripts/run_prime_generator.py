"""V6.10 — Le générateur des premiers.

A. Audit : traces t_n calculées par les seuls nombres premiers = sommes sur les zéros connus.
B. L'opérateur de translation F_h = e^{hD}, reconstruit depuis les premiers (faisceau de Toeplitz) : valeurs propres,
   masses (une vraie valeur propre porte exactement la masse g^(gamma) : masse 1 = zéro simple), comparaison aux zéros.
C. Convergence : nombre de zéros retrouvés selon la borne X des nombres premiers utilisés.
D. La métrique de DH : directions négatives, attribuées quadruplet par quadruplet aux zéros hors droite.
E. Le pas : repliement quand h grandit ; au pas log 2 (une « base »), la dimension ne sature jamais.
Aucun zéro n'entre dans la construction ; les listes de zéros servent seulement de contrôle.
"""
from __future__ import annotations
from pathlib import Path
import sys, math, time
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); D = ROOT / "data"
from prime_generator import traces_from_primes, traces_from_zeros, metric_and_generator, toeplitz_pencil, g_hat
from rejection import coeffs, log_derivative_coeffs
from zero_reconstruction import nontrivial_zeros

MAIN = dict(a=0.04, h=0.01, N=600)              # nombres premiers jusqu'à exp(N h + 2a) = 439
TOL_MASS = 1e-2                                 # vraie valeur propre : |masse - 1| < 1 %
KINDS = ("zeta", "L_chi5", "DH")

def zeros(kind):
    if kind == "zeta":
        gz = pd.read_csv(D / "zeta_zeros_1500.csv").t.values; return np.concatenate([gz, -gz]).astype(complex)
    return -1j * (nontrivial_zeros(kind) - 0.5)

def coeff_cache(kind, M, _c={}):
    if kind not in _c or len(_c[kind]) - 1 < M: _c[kind] = log_derivative_coeffs(coeffs(kind, max(M, 1000)))
    return _c[kind]

def run(kind, a, h, N, Z, t=None):
    """t (facultatif) : traces déjà calculées pour un N plus grand ; leur préfixe n'utilise que les premiers <= exp(N h + 2a)."""
    M = int(math.exp(N * h + 2 * a)) + 2
    t = traces_from_primes(kind, coeff_cache(kind, M), N, h, a) if t is None else t[:N + 1]
    r = metric_and_generator(t, N, h)
    mass = r["weight"] / g_hat(r["gamma"], a); gen = np.abs(mass - 1) < TOL_MASS
    near = np.array([Z[np.argmin(np.abs(Z - g))] for g in r["gamma"]]); err = np.abs(near - r["gamma"])
    return t, r, mass, gen, near, err, M

def expected(Z, a, h, rel=1e-8):
    """Zéros que la fenêtre peut voir : |Re gamma| < pi/h et poids relatif g^(gamma)/g^(0) >= rel."""
    w = np.abs(g_hat(Z, a)) / g_hat(0.0, a).real
    return (np.abs(Z.real) < math.pi / h) & (w >= rel)

COL = {"zeta": "#2a78d6", "L_chi5": "#eb6834", "DH": "#1baf7a"}; RED = "#e34948"; GREY = "#a8a7a2"
NAME = {"zeta": "ζ", "L_chi5": "L(s, χ₅)", "DH": "Davenport–Heilbronn"}

SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
def sci(x):
    m, e = f"{x:+.1e}".split("e"); return f"{m.replace('.', ',')}·10{str(int(e)).translate(SUP)}"

def figure():
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#52514e",
                         "axes.labelcolor": "#0b0b0b", "xtick.color": "#52514e", "ytick.color": "#52514e", "axes.titlesize": 9.5})
    e = pd.read_csv(D / "generator_eigen.csv"); sm = pd.read_csv(D / "generator_summary.csv")
    met = pd.read_csv(D / "generator_dh_metric.csv"); cv = pd.read_csv(D / "generator_convergence.csv")
    fig, ax = plt.subplots(2, 2, figsize=(11, 7.6)); a = MAIN["a"]
    # A : ζ, masses
    A = ax[0, 0]; z = e[(e.objet == "zeta") & (e.re > 0)]
    r = np.linspace(0.5, 330, 2000); A.semilogy(r, np.abs(g_hat(r, a)), color="#52514e", lw=1, label="ĝ(γ) : masse d'un zéro simple")
    A.scatter(z[~z.vraie].re, z[~z.vraie].poids, s=9, color=GREY, label="valeurs propres sans masse 1", zorder=2)
    A.scatter(z[z.vraie].re, z[z.vraie].poids, s=11, color=COL["zeta"], edgecolor="white", lw=0.4, label="masse 1 : un zéro de ζ", zorder=3)
    A.set_xlim(0, 330); A.set_ylim(1e-13, 1e-1); A.set_xlabel("γ (partie réelle de la valeur propre du générateur)"); A.set_ylabel("masse portée")
    A.set_title("ζ depuis les nombres premiers ≤ 439 : chaque zéro porte exactement ĝ(γ)", loc="left"); A.legend(frameon=False, fontsize=8, loc="upper right")
    # B : DH, plan complexe
    B = ax[0, 1]; d = e[(e.objet == "DH") & (e.re > 0) & e.vraie]
    on = d[d.im.abs() < 0.05]; off = d[d.im.abs() >= 0.05]
    zd = -1j * (nontrivial_zeros("DH") - 0.5); zo = zd[(np.abs(zd.imag) > 1e-6) & (zd.real > 0) & (zd.real < 260)]
    B.axhline(0, color="#d8d7d2", lw=0.8, zorder=0)
    B.scatter(on.re, on.im, s=9, color=COL["DH"], label="valeurs propres sur la droite (masse 1)", zorder=2)
    B.scatter(zo.real, zo.imag, s=70, facecolor="none", edgecolor="#0b0b0b", lw=0.8, label="zéros hors droite connus (contrôle)", zorder=3)
    B.scatter(off.re, off.im, s=26, marker="D", color=RED, edgecolor="white", lw=0.5, label="valeurs propres hors droite (masse 1)", zorder=4)
    for x in sorted({round(v, 1) for v in off.re}):
        y = off[np.isclose(off.re, x, atol=0.2)].im.abs().max(); B.annotate(f"{x:.1f} ± {y:.3f}i".replace(".", ","), (x, y), xytext=(4, 6), textcoords="offset points", fontsize=7.5, color="#0b0b0b")
    B.set_xlim(0, 260); B.set_ylim(-0.45, 0.45); B.set_xlabel("Re γ"); B.set_ylabel("Im γ  (= ½ − β)")
    B.set_title("DH : l'opérateur des premiers fait sortir les zéros hors droite", loc="left"); B.legend(frameon=False, fontsize=7.5, loc="lower right")
    # C : la métrique
    C = ax[1, 0]; row = met[np.isclose(met.a, a)].iloc[0]; mu = np.array([float(x) for x in row.mu_negatifs.split()])
    q = [85.699, 114.163, 166.479, 176.702, 240.405]; mu = np.sort(np.abs(mu))[::-1]
    for k in range(len(mu) // 2):
        C.semilogy([q[k], q[k]], mu[2 * k: 2 * k + 2], "o", color=RED, ms=6, mec="white", mew=0.6, label="directions négatives de la métrique (DH)" if k == 0 else None)
        C.annotate(f"{q[k]:.1f}".replace(".", ","), (q[k], mu[2 * k]), xytext=(5, 2), textcoords="offset points", fontsize=7.5)
    for kind, y in (("zeta", 0.30), ("L_chi5", 0.22)):
        m0 = sm[sm.objet == kind].mu_min.iloc[0]
        C.text(0.20, y, f"{NAME[kind]} : aucune valeur propre négative (la plus petite : {sci(m0)})", transform=C.transAxes, ha="left", fontsize=7.5, color="#0b0b0b")
    C.text(0.20, 0.14, "DH : 10 directions = 2 par quadruplet hors droite (5 quadruplets)", transform=C.transAxes, ha="left", fontsize=7.5)
    C.set_xlim(70, 260); C.set_xlabel("hauteur du quadruplet de zéros hors droite"); C.set_ylabel("|valeur propre négative| de G")
    C.set_title("La métrique : positive pour ζ et L, indéfinie pour DH", loc="left"); C.legend(frameon=False, fontsize=7.5, loc="upper right")
    # D : convergence
    Dx = ax[1, 1]
    for kind in KINDS:
        c = cv[cv.objet == kind]; Dx.plot(c.X, c.vraies_justes, "-o", ms=3.5, lw=1.6, color=COL[kind], label=NAME[kind])
        zk = zeros(kind); nb = int(np.sum(np.abs(zk.real) < math.pi / MAIN["h"]))
        Dx.axhline(nb, color=COL[kind], lw=0.9, ls=(0, (3, 3)))
        Dx.annotate(f"{NAME[kind] if kind != 'DH' else 'DH'} : {nb} zéros dans la bande", (c.X.min(), nb), xytext=(0, {"zeta": 3, "L_chi5": 3, "DH": -10}[kind]),
                    textcoords="offset points", fontsize=7, color="#52514e")
    Dx.set_xscale("log"); Dx.set_xlabel("X : nombres premiers utilisés jusqu'à X"); Dx.set_ylabel("zéros retrouvés à 10⁻³ près")
    Dx.set_title("Plus de nombres premiers, plus de zéros (pas h = 0,01)", loc="left"); Dx.legend(frameon=False, fontsize=8, loc="center left")
    fig.tight_layout(h_pad=2.2, w_pad=2.0); fig.savefig(D / "generator.png", dpi=150); print("figure écrite")

if __name__ == "__main__":
    if "--figure" in sys.argv:
        figure(); sys.exit(0)
    T0 = time.time(); Z = {k: zeros(k) for k in KINDS}
    # ---------------- A + B : fenêtre principale
    summ, eig = [], []
    for kind in KINDS:
        a, h, N = MAIN["a"], MAIN["h"], MAIN["N"]
        t, r, mass, gen, near, err, M = run(kind, a, h, N, Z[kind])
        audit = float(np.max(np.abs(t - traces_from_zeros(Z[kind], N, h, a))))
        exp_mask = expected(Z[kind], a, h); ok = gen & (err < 1e-3)
        for g, w, m, gg, nz, e in zip(r["gamma"], r["weight"], mass, gen, near, err):
            eig.append(dict(objet=kind, re=g.real, im=g.imag, poids=abs(w), masse_re=m.real, masse_im=m.imag, vraie=bool(gg),
                            zero_re=nz.real, zero_im=nz.imag, ecart=e, g_hat=abs(g_hat(nz, a))))
        summ.append(dict(objet=kind, a=a, h=h, N=N, X=M, audit_premiers_zeros=audit, rang=r["rank"], negatifs=r["negatives"],
                         mu_min=float(r["mu"][0]), mu_max=float(r["mu"][-1]), valeurs_propres=len(r["gamma"]), vraies=int(gen.sum()),
                         vraies_justes=int(ok.sum()), vraies_approchees=int((gen & (err >= 1e-3) & (err < 1e-2)).sum()),
                         vraies_fausses=int((gen & (err >= 1e-2)).sum()), attendus=int(exp_mask.sum()),
                         attendus_retrouves=int(sum(np.min(np.abs(r["gamma"][gen] - z)) < 1e-2 for z in Z[kind][exp_mask])) if gen.any() else 0,
                         ecart_max_vraies=float(err[gen].max()), ecart_median_vraies=float(np.median(err[gen])),
                         hauteur_max=float(np.max(np.abs(r["gamma"][gen].real))), masse_max_ecart=float(np.max(np.abs(mass[gen] - 1))),
                         premier_zero_ecart=float(err[gen][np.argmin(np.abs(np.abs(r["gamma"][gen].real) - np.min(np.abs(Z[kind].real))))]),
                         hors_droite_retrouves=int(np.sum(gen & (np.abs(r["gamma"].imag) > 0.05)))))
        print(f"{kind}: X = {M}, audit {audit:.1e}, rang {r['rank']}, négatifs {r['negatives']}, vraies {gen.sum()} (justes {ok.sum()}), "
              f"attendus {exp_mask.sum()} (retrouvés {summ[-1]['attendus_retrouves']}), fausses {summ[-1]['vraies_fausses']}, écart max {err[gen].max():.1e}, hauteur {summ[-1]['hauteur_max']:.1f}", flush=True)
    pd.DataFrame(summ).to_csv(D / "generator_summary.csv", index=False); pd.DataFrame(eig).to_csv(D / "generator_eigen.csv", index=False)
    # ---------------- C : convergence selon X
    conv = []
    for kind in KINDS:
        a, h = MAIN["a"], MAIN["h"]
        tfull = traces_from_primes(kind, coeff_cache(kind, int(math.exp(1000 * h + 2 * a)) + 2), 1000, h, a)
        for N in range(50, 1001, 50):
            t, r, mass, gen, near, err, M = run(kind, a, h, N, Z[kind], tfull)
            ok = gen & (err < 1e-3)
            conv.append(dict(objet=kind, N=N, X=M, logX=N * h + 2 * a, rang=r["rank"], negatifs=r["negatives"], vraies=int(gen.sum()),
                             vraies_justes=int(ok.sum()), vraies_approchees=int((gen & (err >= 1e-3) & (err < 1e-2)).sum()),
                             vraies_fausses=int((gen & (err >= 1e-2)).sum()),
                             ecart_max=float(err[gen].max()) if gen.any() else float("nan"),
                             hauteur_max=float(np.max(np.abs(r["gamma"][ok].real))) if ok.any() else 0.0))
        print(f"{kind}: convergence faite ({time.time() - T0:.0f} s)", flush=True)
    pd.DataFrame(conv).to_csv(D / "generator_convergence.csv", index=False)
    # ---------------- D : la métrique de DH, attribuée quadruplet par quadruplet
    zd = Z["DH"]; on = zd[np.abs(zd.imag) < 1e-6]; off = zd[np.abs(zd.imag) >= 1e-6]
    quads = sorted({round(abs(g.real), 3) for g in off})
    met = []
    for a, h, N in ((0.2, 0.05, 120), (0.12, 0.03, 200), (0.08, 0.02, 300), (0.05, 0.0125, 480), (MAIN["a"], MAIN["h"], MAIN["N"])):
        t, r, mass, gen, near, err, M = run("DH", a, h, N, zd)
        mu = r["mu"]; tol = 1e-11 * np.max(np.abs(mu)); neg = np.sort(mu[mu < -tol])
        row = dict(a=a, h=h, N=N, X=M, negatifs_premiers=int(len(neg)), mu_negatifs=" ".join(f"{x:.3e}" for x in neg))
        tz = traces_from_zeros(on, N, h, a); G, _ = toeplitz_pencil(tz, N); m0 = np.linalg.eigvalsh(0.5 * (G + G.conj().T))
        row["negatifs_zeros_sur_droite"] = int(np.sum(m0 < -tol)); row["mu_min_sur_droite"] = float(m0[0])
        for k in range(1, 7):                           # on ajoute les k premiers quadruplets hors droite
            sel = np.concatenate([on] + [off[np.isclose(np.abs(off.real), q, atol=2e-3)] for q in quads[:k]])
            tz = traces_from_zeros(sel, N, h, a); G, _ = toeplitz_pencil(tz, N); mk = np.linalg.eigvalsh(0.5 * (G + G.conj().T))
            row[f"negatifs_{k}_quadruplets"] = int(np.sum(mk < -tol))
        for k, q in enumerate(quads[:6], 1):
            row[f"poids_rel_quadruplet_{k}"] = float(np.abs(g_hat(off[np.isclose(np.abs(off.real), q, atol=2e-3)][0], a)) / g_hat(0.0, a).real)
        row["hors_droite_retrouves"] = int(np.sum(gen & (np.abs(r["gamma"].imag) > 0.05)))
        met.append(row); print(f"DH a = {a}: négatifs {len(neg)} ; retrouvés hors droite {row['hors_droite_retrouves']}", flush=True)
    pd.DataFrame(met).to_csv(D / "generator_dh_metric.csv", index=False)
    print("quadruplets hors droite (hauteurs) :", quads[:6])
    # ---------------- E : le pas (X fixé, h croissant) : repliement des zéros au-delà de pi / h
    alias = []
    a = 0.08
    for h in (0.02, 0.05, 0.1, 0.2, 0.5, math.log(2)):
        N = int(round(6.0 / h)); t, r, mass, gen, near, err, M = run("zeta", a, h, N, Z["zeta"])
        zz = Z["zeta"]; lam = r["lam"]; strong = np.abs(r["weight"]) > 1e-6 * t[0].real
        fold = np.array([np.min(np.abs(np.exp(1j * zz * h) - l)) for l in lam])  # écart à un zéro replié e^{i gamma h}
        alias.append(dict(h=h, N=N, X=M, nyquist=math.pi / h, rang=r["rank"], zeros_dans_la_bande=int(np.sum(expected(zz, a, h, 1e-6))),
                          zeros_hors_bande_poids=int(np.sum((np.abs(zz.real) >= math.pi / h) & (np.abs(g_hat(zz, a)) >= 1e-6 * g_hat(0.0, a).real))),
                          valeurs_fortes=int(strong.sum()), fortes_sur_un_zero_replie=int(np.sum(strong & (fold < 1e-3))),
                          vraies_sans_repliement=int(np.sum(gen & (err < 1e-3)))))
    pd.DataFrame(alias).to_csv(D / "generator_step.csv", index=False)
    print(pd.DataFrame(alias).to_string(index=False))
    figure(); print(f"total {time.time() - T0:.0f} s")
