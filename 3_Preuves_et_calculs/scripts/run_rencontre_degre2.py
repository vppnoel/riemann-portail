"""V6.17 — La Rencontre en degré 2, et son pendant dans le Modèle réduit (prévisions : data/prevision_v617.md).

Marge d'un zéro : m = 1 − sinc²(π s), s = écart au plus proche voisin × (2π × densité locale) / 2π (document 40).
Marge d'une paire de racines (premier p de Δ, ou courbe de genre 1 sur F_p) : déterminant normalisé de la métrique 2×2,
    det [[2, λ], [λ, 2]] / 4 = 1 − λ²/4 = sin²θ,   λ = 2 cos θ   (pour une courbe : λ = a_p/√p, et 1 − λ²/4 = 1 − ρ₁²,
    la marge de Castelnuovo du document 28).
A. Référence GUE exacte : matrices unitaires circulaires (CUE) de taille N (Haar, algorithme de Mezzadri), N = 200 et N petit.
B. Δ : zéros de L(Δ, s) jusqu'à 1 500 (data/delta_zeros_contour.csv, Contour tourné).
C. ζ_K = ζ·L(χ5) : réunion des zéros de ζ et de L(χ5) jusqu'à 600 (superposition de deux familles).
D. Δ côté premiers : angles de Satake θ_p, p ≤ 25 000 ; Sato–Tate.
E. Modèle réduit : toutes les courbes y² = x³ + ax + b sur F_p (cinq p) ; étage 2 de la tour (F_{p²}) : changement de base.
Sorties : data/degre2_*.csv, data/degre2_resume.csv ; figure data/degre2.png (et --figure pour la figure seule).
"""
import os, sys, math, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "1")   # sinon les fils BLAS se marchent dessus
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.special import digamma
from scipy import stats
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
D = ROOT / "data"
PS = (101, 211, 307, 401, 503)

def sinc(x): return np.where(np.abs(x) < 1e-12, 1.0, np.sin(x) / np.where(np.abs(x) < 1e-12, 1.0, x))
def margin(s): return 1 - sinc(np.pi * np.asarray(s, dtype=float)) ** 2
def s_of_margin(m): return brentq(lambda s: margin(s) - m, 1e-9, 1.0)
X1, X3 = s_of_margin(0.1), s_of_margin(0.3)

def nn_gaps(g):
    g = np.sort(np.asarray(g)); d = np.diff(g)
    return g, np.minimum(np.r_[np.inf, d], np.r_[d, np.inf])

# ------------------------------------------------------------------ A. CUE
def haar_unitary(N, k, rng):
    Z = (rng.standard_normal((k, N, N)) + 1j * rng.standard_normal((k, N, N))) / math.sqrt(2)
    Q, R = np.linalg.qr(Z); d = np.diagonal(R, axis1=1, axis2=2); return Q * (d / np.abs(d))[:, None, :]

def cue_nn(N, samples, rng, batch=200):
    """Écarts au plus proche voisin (unités : espacement moyen 2π/N) de toutes les valeurs propres."""
    out = []
    for i0 in range(0, samples, batch):
        k = min(batch, samples - i0); th = np.sort(np.angle(np.linalg.eigvals(haar_unitary(N, k, rng))), axis=1)
        d = np.diff(np.concatenate([th, th[:, :1] + 2 * math.pi], axis=1), axis=1)       # écarts sur le cercle
        nn = np.minimum(d, np.roll(d, 1, axis=1)); out.append((nn * N / (2 * math.pi)).ravel())
    return np.concatenate(out)

def part_A(rng):
    rows = []
    for N, samp in ((200, 600), (2, 200000), (3, 150000), (4, 100000), (5, 80000), (6, 60000), (8, 40000), (10, 30000), (15, 20000), (20, 15000), (50, 4000)):
        s = cue_nn(N, samp, rng)
        rows.append(dict(N=N, valeurs=len(s), f01=float(np.mean(s < X1)), f03=float(np.mean(s < X3)), s_moyen_nn=float(s.mean())))
        print(f"  CUE N={N:3d} : f(m<0,1) = {rows[-1]['f01']:.5f}   f(m<0,3) = {rows[-1]['f03']:.5f}", flush=True)
    return pd.DataFrame(rows)

def poisson_f(x): return 1 - math.exp(-2 * x)

# ------------------------------------------------------------------ B. Δ
def omega_delta(t): return 2 * np.real(digamma(6 + 1j * np.asarray(t, dtype=float))) - 2 * math.log(2 * math.pi)

def part_B():
    g = pd.read_csv(D / "delta_zeros_contour.csv").gamma.values; g, gap = nn_gaps(g)
    s = gap * omega_delta(g) / (2 * math.pi); m = margin(s)
    sc = np.diff(g) * omega_delta(g[:-1]) / (2 * math.pi)
    return pd.DataFrame(dict(gamma=g, ecart=gap, s=s, marge=m)), float(sc.mean())

# ------------------------------------------------------------------ C. ζ_K
def part_C():
    z = pd.read_csv(D / "zeta_zeros_1500.csv").t.values; z = z[(z > 0) & (z <= 600)]
    l = pd.read_csv(D / "L_chi5_zeros_600.csv").t.values; l = l[(l > 0) & (l <= 600)]
    g = np.r_[z, l]; lab = np.r_[np.zeros(len(z), int), np.ones(len(l), int)]; o = np.argsort(g); g, lab = g[o], lab[o]
    d = np.diff(g); left = np.r_[np.inf, d]; right = np.r_[d, np.inf]; gap = np.minimum(left, right)
    voisin = np.where(left <= right, np.r_[-1, lab[:-1]], np.r_[lab[1:], -1])
    om = np.log(g / (2 * math.pi)) + np.log(5 * g / (2 * math.pi)); s = gap * om / (2 * math.pi)
    df = pd.DataFrame(dict(gamma=g, famille=np.where(lab == 0, "zeta", "L_chi5"), ecart=gap, s=s, marge=margin(s), mixte=(voisin != lab)))
    cross = np.min(np.abs(z[:, None] - l[None, :]))
    w1 = np.log(g / (2 * math.pi)) / om; theo = float(np.mean(4 * X1 * w1 * (1 - w1)))
    own = {}
    for name, x, f in (("zeta", z, lambda t: np.log(t / (2 * math.pi))), ("L_chi5", l, lambda t: np.log(5 * t / (2 * math.pi)))):
        xs, gx = nn_gaps(x); own[name] = float(np.mean(margin(gx * f(xs) / (2 * math.pi)) < 0.1))
    return df, float(cross), theo, own

# ------------------------------------------------------------------ D. Δ aux premiers
def primes_upto(n):
    sv = np.ones(n + 1, bool); sv[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sv[i]: sv[i * i::i] = False
    return np.nonzero(sv)[0]

def st_cdf(th): return (th - np.sin(th) * np.cos(th)) / math.pi

def part_D(M=25000):
    from delta_ramanujan import tau
    T = tau(M); P = primes_upto(M)
    lam = np.array([T[p] / p ** 5.5 for p in P]); th = np.arccos(np.clip(lam / 2, -1, 1)); m = 1 - lam ** 2 / 4
    # marge exacte (entiers) : 4 p^11 − τ(p)² > 0 ; la plus petite, en valeur relative
    rel = np.array([float(4 * int(p) ** 11 - T[p] ** 2) / float(4 * int(p) ** 11) for p in P])
    ks = stats.kstest(th, st_cdf)
    return pd.DataFrame(dict(p=P, tau_p=[str(T[p]) for p in P], lambda_p=lam, theta_p=th, marge=m, marge_exacte=rel)), ks

# ------------------------------------------------------------------ E. Modèle réduit
def curves_ap(p):
    """a_p de toutes les courbes y² = x³ + ax + b (discriminant non nul), comptées par (a, b)."""
    chi = np.full(p, -1, np.int64); chi[(np.arange(1, p) ** 2) % p] = 1; chi[0] = 0        # symbole de Legendre
    x = np.arange(p); out = []
    for a in range(p):
        base = (x ** 3 + a * x) % p
        vals = chi[(base[None, :] + np.arange(p)[:, None]) % p].sum(axis=1)            # somme sur x, pour chaque b
        b = np.arange(p); disc = (4 * a ** 3 + 27 * b ** 2) % p
        for bb in np.nonzero(disc != 0)[0]: out.append((a, int(bb), int(-vals[bb])))
    return np.array(out)

def part_E():
    rows, per_p = [], []
    for p in PS:
        A = curves_ap(p); ap = A[:, 2]; m1 = 1 - ap ** 2 / (4 * p)
        a2 = ap ** 2 - 2 * p; m2 = 1 - a2 ** 2 / (4 * p ** 2)                               # étage 2 : F_{p²}
        rho2 = np.abs(a2) / (2 * p)
        per_p.append(dict(p=p, courbes=len(ap), hasse_ok=bool(np.all(ap ** 2 <= 4 * p)), f01=float(np.mean(m1 < 0.1)), f03=float(np.mean(m1 < 0.3)),
                          marge_min=float(m1.min()), supersingulieres=int(np.sum(ap == 0)), part_supersing=float(np.mean(ap == 0)),
                          collisions_etage2=int(np.sum(m2 == 0)), rho2_max=float(rho2.max()), f01_etage2=float(np.mean(m2 < 0.1)),
                          ks_p=float(stats.kstest(np.arccos(ap / (2 * math.sqrt(p))), st_cdf).pvalue),
                          moment2=float(np.mean(ap ** 2) / p), moment4=float(np.mean(ap.astype(float) ** 4) / p ** 2), moment6=float(np.mean(ap.astype(float) ** 6) / p ** 3)))
        rows.append(pd.DataFrame(dict(p=p, a_p=ap, theta=np.arccos(ap / (2 * math.sqrt(p))), marge=m1, marge_etage2=m2)))
        print(f"  F_{p} : {len(ap)} courbes, f(m<0,1) = {per_p[-1]['f01']:.4f}, supersingulières {per_p[-1]['supersingulieres']}, collisions à l'étage 2 {per_p[-1]['collisions_etage2']}", flush=True)
    return pd.concat(rows), pd.DataFrame(per_p)

def part_E2():
    """Les 425 courbes du Modèle réduit (V6.6) : métrique de taille N = 2g sur les angles de Frobenius.
    Identités : det G = Π_{l<m} |e^{iθ_l} − e^{iθ_m}|² (densité de Weyl de U(N)) ; marge d'une paire = 1 − D_N(Δ)²."""
    from function_field import roots_alpha
    c = pd.read_csv(D / "reduced_model_curves.csv"); out = []
    for r in c.itertuples():
        coeffs = [int(x) for x in str(r.P).split()]; al = roots_alpha(coeffs) / math.sqrt(r.q); th = np.angle(al); N = len(th)
        j = np.arange(N); G = np.exp(1j * np.subtract.outer(j, j)[:, :, None] * th[None, None, :]).sum(axis=2)
        e = np.exp(1j * th); vd = float(np.prod([abs(e[l] - e[m]) ** 2 for l in range(N) for m in range(l + 1, N)]))
        dG = float(np.linalg.det(G).real); d = np.abs(np.angle(np.exp(1j * np.subtract.outer(th, th))))[np.triu_indices(N, 1)]
        pm = 1 - (np.abs(np.exp(1j * np.outer(j, d)).sum(axis=0)) / N) ** 2                         # marge de chaque paire, fenêtre N
        Dn = np.where(d < 1e-12, 1.0, np.sin(N * d / 2) / (N * np.sin(np.where(d < 1e-12, 1.0, d) / 2)))
        out.append(dict(q=r.q, g=r.g, courbe=r.courbe, N=N, rh=bool(np.all(np.abs(np.abs(al) - 1) < 1e-6)), det_G=dG, weyl=vd,
                        ecart_identite=abs(dG - vd) / max(1.0, abs(vd)), ecart_paires=float(np.max(np.abs(pm - (1 - Dn ** 2)))),
                        marge_paire_min=float(pm.min()), lambda_min_G=float(np.linalg.eigvalsh(G).min() / N)))
    return pd.DataFrame(out)

# ------------------------------------------------------------------ N effectif
def neff_from_ratio(cue, ratio, col="f01"):
    """N (interpolé en 1/N²) tel que f_CUE(N)/f_CUE(200) = ratio ; None hors de la plage simulée."""
    c = cue[cue.N < 200].sort_values("N"); r = (c[col] / float(cue[cue.N == 200][col].iloc[0])).values; x = 1 / c.N.values ** 2
    if ratio < r.min() or ratio > r.max(): return None
    o = np.argsort(r); return float(1 / math.sqrt(np.interp(ratio, r[o], x[o])))

def garwood(k, a=0.05):
    lo = 0.0 if k == 0 else stats.chi2.ppf(a / 2, 2 * k) / 2; hi = stats.chi2.ppf(1 - a / 2, 2 * k + 2) / 2; return lo, hi

def main():
    t0 = time.time(); rng = np.random.default_rng(617)
    print("A. CUE"); cue = part_A(rng); cue.to_csv(D / "degre2_cue.csv", index=False)
    f200 = cue[cue.N == 200].iloc[0]
    print("B. Δ"); dz, mean_sc = part_B(); dz.to_csv(D / "degre2_delta_zeros.csv", index=False)
    zr = pd.read_csv(D / "rencontre_zeros.csv")
    res = dict(seuil_s_01=X1, seuil_s_03=X3, cue200_f01=f200.f01, cue200_f03=f200.f03, poisson_f01=poisson_f(X1), poisson_f03=poisson_f(X3),
               delta_zeros=len(dz), delta_T=float(dz.gamma.max()), delta_ecart_moyen_normalise=mean_sc)
    for lab, frame in (("delta1000", dz[dz.gamma <= 1000]), ("delta", dz), ("zeta", zr)):
        for th, col in ((0.1, "f01"), (0.3, "f03")):
            k = int((frame.marge < th).sum()); n = len(frame); f = k / n; lo, hi = garwood(k)
            res[f"{lab}_n"] = n; res[f"{lab}_k_{col}"] = k; res[f"{lab}_{col}"] = f
            res[f"{lab}_rapport_{col}"] = f / f200[col]; res[f"{lab}_rapport_{col}_lo"] = lo / n / f200[col]; res[f"{lab}_rapport_{col}_hi"] = hi / n / f200[col]
            res[f"{lab}_neff_{col}"] = neff_from_ratio(cue, f / f200[col], col)
            res[f"{lab}_neff_developpement_{col}"] = 1 / math.sqrt(1 - f / f200[col]) if f < f200[col] else None   # 1 − 1/N² = rapport
    res["neff_bogomolny_zeta"] = float(np.mean(np.log(zr.gamma / (2 * math.pi)) / math.sqrt(12 * 1.57314)))
    res["neff_bogomolny_delta_si_meme_Lambda"] = float(np.mean(omega_delta(dz.gamma.values) / math.sqrt(12 * 1.57314)))
    i = int(dz.s.idxmin()); res.update(delta_plus_petit_s=float(dz.s[i]), delta_plus_petit_s_gamma=float(dz.gamma[i]), delta_plus_petite_marge=float(dz.marge[i]))
    print("C. ζ·L(χ5)"); ck, cross, theo, own = part_C(); ck.to_csv(D / "degre2_zetaK.csv", index=False)
    small = ck[ck.marge < 0.1]
    res.update(zetaK_n=len(ck), zetaK_f01=float((ck.marge < 0.1).mean()), zetaK_theorie_f01=theo, zetaK_part_mixtes_f01=float(small.mixte.mean()),
               zetaK_distance_min_croisee=cross, zetaK_f01_zeta_seul=own["zeta"], zetaK_f01_Lchi5_seul=own["L_chi5"])
    print("D. Δ aux premiers"); pr, ks = part_D(); pr.to_csv(D / "degre2_satake.csv", index=False)
    st01 = 2 * (2 / math.pi) * (math.asin(math.sqrt(0.1)) / 2 - math.sin(2 * math.asin(math.sqrt(0.1))) / 4)
    res.update(premiers=len(pr), satake_f01=float((pr.marge < 0.1).mean()), sato_tate_f01=st01, uniforme_f01=2 * math.asin(math.sqrt(0.1)) / math.pi,
               satake_marge_min=float(pr.marge_exacte.min()), satake_p_marge_min=int(pr.p[pr.marge_exacte.idxmin()]), satake_lambda_max=float(np.abs(pr.lambda_p).max()),
               satake_ks_stat=float(ks.statistic), satake_ks_p=float(ks.pvalue),
               satake_moment2=float((pr.lambda_p ** 2).mean()), satake_moment4=float((pr.lambda_p ** 4).mean()), satake_moment6=float((pr.lambda_p ** 6).mean()))
    print("E. Modèle réduit"); cu, per_p = part_E(); per_p.to_csv(D / "degre2_courbes_par_p.csv", index=False)
    cu.groupby(["p", "a_p"]).size().rename("courbes").reset_index().to_csv(D / "degre2_courbes_ap.csv", index=False)
    res.update(courbes=int(per_p.courbes.sum()), courbes_f01=float((cu.marge < 0.1).mean()), courbes_marge_min=float(cu.marge.min()),
               courbes_collisions_etage2=int(per_p.collisions_etage2.sum()), courbes_supersing=int(per_p.supersingulieres.sum()),
               courbes_f01_etage2=float((cu.marge_etage2 < 0.1).mean()))
    e2 = part_E2(); e2.to_csv(D / "degre2_modele_reduit_weyl.csv", index=False)
    fk = pd.read_csv(D / "stability_model_fakes.csv")
    res.update(mr_courbes=len(e2), mr_rh=int(e2.rh.sum()), mr_ecart_identite_max=float(e2.ecart_identite.max()), mr_ecart_paires_max=float(e2.ecart_paires.max()),
               mr_collisions=int((e2.marge_paire_min < 1e-10).sum()), mr_lambda_min_min=float(e2.lambda_min_G.min()),
               mr_faux_jumeaux=len(fk), mr_faux_jumeaux_marge_negative=int((fk.marge_forme_L2g < 0).sum()))
    pd.DataFrame([res]).to_csv(D / "degre2_resume.csv", index=False)
    for k, v in res.items(): print(f"  {k} = {v}")
    figure(); print(f"total {time.time() - t0:.0f} s")

def figure():
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    cue = pd.read_csv(D / "degre2_cue.csv"); r = pd.read_csv(D / "degre2_resume.csv").iloc[0]
    dz = pd.read_csv(D / "degre2_delta_zeros.csv"); zr = pd.read_csv(D / "rencontre_zeros.csv"); ck = pd.read_csv(D / "degre2_zetaK.csv")
    pr = pd.read_csv(D / "degre2_satake.csv"); cu = pd.read_csv(D / "degre2_courbes_ap.csv")
    fig, ax = plt.subplots(2, 2, figsize=(12.5, 9.2))
    # (A) fonction de répartition des écarts au plus proche voisin, petits s
    A = ax[0, 0]; ss = np.linspace(0, 0.6, 300)
    for lab, frame, c in (("ζ (1 070 zéros ≤ 1 500)", zr, "#1f5fa8"), (f"Δ ({int(r.delta_zeros)} zéros ≤ {r.delta_T:.0f})", dz, "#b8452f"), ("ζ·L(χ5) (≤ 600)", ck, "#7a7a7a")):
        x = np.sort(frame.s.values); A.step(x, np.arange(1, len(x) + 1) / len(x), where="post", color=c, lw=1.6, label=lab)
    rng = np.random.default_rng(1); s200 = cue_nn(200, 300, rng); x = np.sort(s200)
    A.plot(x, np.arange(1, len(x) + 1) / len(x), color="k", lw=1, ls="--", label="GUE exact (CUE, N = 200)")
    A.plot(ss, 1 - np.exp(-2 * ss), color="k", lw=1, ls=":", label="Poisson (sans répulsion)")
    A.axvline(r.seuil_s_01, color="#999", lw=0.8); A.text(r.seuil_s_01 + 0.006, 0.012, "marge 0,1", color="#666", fontsize=8, rotation=90)
    A.set_xlim(0, 0.6); A.set_ylim(0, 0.35); A.set_xlabel("écart au plus proche voisin s (unités : espacement moyen)"); A.set_ylabel("proportion des zéros")
    A.set_title("A. Les petites marges : Δ se repousse, ζ·L(χ5) non", fontsize=10.5); A.legend(fontsize=7.8, loc="upper left")
    # (B) taille effective
    B = ax[0, 1]; c = cue[cue.N < 200].sort_values("N"); NN = np.linspace(1.02, 60, 600)
    B.plot(NN, 1 - 1 / NN ** 2, color="#aaa", lw=1, label="développement 1 − 1/N² (Bogomolny et al.)")
    B.plot(c.N, c.f01 / r.cue200_f01, "o-", color="k", ms=4, lw=1, label="CUE de taille N, seuil 0,1")
    B.plot(c.N, c.f03 / r.cue200_f03, "s--", color="#555", ms=3.5, lw=1, label="CUE de taille N, seuil 0,3")
    for lab, col, cc in (("ζ", "zeta", "#1f5fa8"), ("Δ", "delta", "#b8452f")):
        for th, ls in (("f01", "-"), ("f03", "--")):
            v = r[f"{col}_rapport_{th}"]; lo, hi = r[f"{col}_rapport_{th}_lo"], r[f"{col}_rapport_{th}_hi"]
            B.axhspan(lo, hi, color=cc, alpha=0.06 if th == "f01" else 0.11); B.axhline(v, color=cc, ls=ls, lw=1.3, label=f"{lab}, seuil {'0,1' if th == 'f01' else '0,3'} : {v:.2f}".replace(".", ","))
    for nb, cc, lab in ((r.neff_bogomolny_zeta, "#1f5fa8", "N_eff de ζ"), (r.neff_bogomolny_delta_si_meme_Lambda, "#b8452f", "N_eff de Δ si Λ égal")):
        B.plot([nb], [1 - 1 / nb ** 2], marker="v", color=cc, ms=9, ls="none"); B.annotate(lab, (nb, 1 - 1 / nb ** 2), xytext=(4, 6), textcoords="offset points", fontsize=7.5, color=cc)
    B.set_xscale("log"); B.set_xticks([1, 2, 3, 5, 10, 20, 50]); B.set_xticklabels(["1", "2", "3", "5", "10", "20", "50"]); B.minorticks_off(); B.set_xlim(1, 60)
    B.set_xlabel("taille N de la matrice"); B.set_ylabel("petites marges / GUE exact"); B.set_ylim(0, 1.15)
    B.set_title("B. Un déficit de petites marges, en degré 1 comme en degré 2", fontsize=10.5); B.legend(fontsize=6.6, loc="lower right", ncol=2)
    # (C) Satake
    C = ax[1, 0]; th = np.linspace(0, math.pi, 300)
    C.hist(pr.theta_p, bins=40, range=(0, math.pi), density=True, color="#b8452f", alpha=0.55, label=f"Δ : θ_p, {len(pr)} premiers ≤ 25 000")
    C.plot(th, 2 / math.pi * np.sin(th) ** 2, "k-", lw=1.4, label="Sato–Tate (2/π) sin²θ = (2/π) × marge")
    C.axhline(1 / math.pi, color="k", ls=":", lw=1, label="angles uniformes")
    C.set_xlabel("angle de Satake θ_p  (λ(p) = 2 cos θ_p)"); C.set_ylabel("densité"); C.set_title("C. Aux premiers : la rencontre de α_p et β_p est évitée", fontsize=10.5)
    C.legend(fontsize=7.8, loc="upper right"); C.set_ylim(0, 0.9)
    # (D) Modèle réduit : les cinq corps réunis
    Dx = ax[1, 1]; q = cu.p.values.astype(float); theta = np.arccos(cu.a_p / (2 * np.sqrt(q))); w = cu.courbes.values / (cu.p.values.astype(float) ** 2)
    Dx.hist(theta, bins=30, range=(0, math.pi), weights=w, density=True, color="#2f7d4a", alpha=0.5, label="étage 1 (F_p) : angle θ")
    ang2 = np.mod(2 * theta, 2 * math.pi); ang2 = np.where(ang2 > math.pi, 2 * math.pi - ang2, ang2)
    Dx.hist(ang2, bins=30, range=(0, math.pi), weights=w, density=True, histtype="step", color="#6a3d9a", lw=1.6, label="étage 2 (F_p²) : mêmes courbes, angle 2θ")
    Dx.plot(th, 2 / math.pi * np.sin(th) ** 2, "k-", lw=1.2, label="Sato–Tate (2/π) sin²θ")
    Dx.annotate("collisions possibles en π\n(courbes supersingulières)", xy=(3.08, 0.36), xytext=(1.75, 0.82), fontsize=8, color="#6a3d9a", arrowprops=dict(arrowstyle="->", color="#6a3d9a"))
    Dx.set_xlabel(f"angle (a = 2√q cos θ) ; {int(cu.courbes.sum())} courbes sur F_p, p = 101 à 503"); Dx.set_ylabel("densité"); Dx.set_ylim(0, 1.0)
    Dx.set_title("D. Modèle réduit : Sato–Tate à l'étage 1, collisions à l'étage 2", fontsize=10.5); Dx.legend(fontsize=7.6, loc="upper left")
    fig.tight_layout(); fig.savefig(D / "degre2.png", dpi=130); print("figure écrite")

if __name__ == "__main__":
    figure() if "--figure" in sys.argv else main()
