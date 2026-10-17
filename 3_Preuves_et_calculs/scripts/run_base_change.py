"""V6.10, suite 2 — La base comme pas de temps : courbes sur F_q vues sur F_q².

Pour chaque courbe du Modèle réduit (525) et chaque faux jumeau (220) :
- reconstruction GNS depuis les comptages sur F_q² (p'_n = p_2n) : valeurs propres = beta², rang, unitarité, négatifs ;
- générateur : zéros sur F_q² = zéros sur F_q, plus les mêmes décalés de pi / log q (période divisée par deux) ;
- descentes : polynômes de Weil réels entiers qui ont la même image sur F_q² (la courbe, sa tordue, et d'autres éventuels).
Puis, pour ζ, L(s, χ₅) et DH (générateur des premiers, document 33) : la métrique selon le pas, à nombres premiers fixés
(X ≈ 440 : moins d'échantillons quand h grandit) et à nombre d'échantillons fixé (N = 300 : premiers plus loin).
"""
from __future__ import annotations
from pathlib import Path
import sys, math, time
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); D = ROOT / "data"
from stability_radius import normalized
from frobenius_chain import distinct, match_error, curve_gammas
from base_change import gns_from_traces, base_q2_traces, real_weil, descents, h_of, descents_by_factors

def zeros_mod(gam, period):
    return np.sort(np.mod(gam.real, period))

def main():
    t0 = time.time(); rows = []
    cur = pd.read_csv(D / "stability_model_curves.csv"); fak = pd.read_csv(D / "stability_model_fakes.csv")
    objs = [("courbe", int(x.q), int(x.g), list(map(int, x.P.split())), bool(x.zeros_confondus)) for _, x in cur.iterrows()]
    for _, x in fak.iterrows():
        q, g = int(x.q), int(x.g); c = [1, int(x.c1), q] if g == 1 else [1, int(x.c1), int(float(x.c2)), q * int(x.c1), q * q]
        objs.append(("faux jumeau", q, g, c, False))
    for kind, q, g, c, conf in objs:
        b = normalized(c, q); beta = 1 / np.roots(b[::-1]); L = 2 * g + 4
        p2 = base_q2_traces(b, L + 2)
        r2, lam2, ev2 = gns_from_traces(p2)
        bd, b2d = distinct(beta), distinct(beta ** 2)
        row = dict(objet=kind, q=q, g=g, P=" ".join(map(str, c)), zeros_confondus=conf, zeros_distincts_q=len(bd), zeros_distincts_q2=len(b2d), rang_q2=r2,
                   ecart_beta2=match_error(lam2, b2d) if r2 == len(b2d) else float("nan"), ecart_unitaire_q2=float(np.max(np.abs(np.abs(lam2) - 1))),
                   negatifs_q2=int(np.sum(ev2 < -1e-9 * np.max(np.abs(ev2)))), hors_cercle=int(np.sum(np.abs(np.abs(beta) - 1) > 1e-6)),
                   hors_cercle_q2_distincts=int(np.sum(np.abs(np.abs(b2d) - 1) > 1e-6)))
        if kind == "courbe":
            # générateur : les zéros sur F_q² sont ceux de F_q et de la tordue, période pi / log q
            lq = math.log(q); T = 40.0
            g1 = curve_gammas(b, q, T); gtw = curve_gammas(normalized([ck * (-1) ** k for k, ck in enumerate(c)], q), q, T)
            # zéros de P_q²(q^-2s) : périodiques de période 2 pi / (2 log q)
            gam2 = []
            for be2 in beta ** 2:
                for k in range(-60, 61):
                    x = (np.angle(be2) + 2 * math.pi * k) / (2 * lq)
                    if abs(x) <= T: gam2.append(x)
            per = math.pi / lq
            A = zeros_mod(np.concatenate([g1, gtw]), per); B = zeros_mod(np.array(gam2), per)
            row["zeros_q2_egal_q_et_tordue"] = bool(len(A) == len(B) and np.max(np.abs(A - B)) < 1e-9) if len(A) == len(B) else False
            # descentes
            if g <= 12:
                a = real_weil(c, q); ds = descents(a, q); hv = h_of(a); htw = h_of(-a)
                nf, nd = descents_by_factors(hv)
                row.update(descentes=len(ds), contient_courbe=hv in ds, contient_tordue=htw in ds, tordue_egale=(hv == htw),
                           facteurs_irreductibles=nf, descentes_par_facteurs=nd)
        rows.append(row)
    d = pd.DataFrame(rows)
    # réfutation annoncée par le navigateur : deux courbes non tordues du corpus auraient-elles les mêmes comptages sur F_q² ?
    H = {}
    for kind, q, g, c, conf in objs:
        if kind == "courbe": H.setdefault((q, g), set()).add(h_of(real_weil(c, q)))
    other = []
    for kind, q, g, c, conf in objs:
        if kind != "courbe" or g > 12: other.append(float("nan")); continue
        a = real_weil(c, q); own = {h_of(a), h_of(-a)}
        other.append(int(sum(1 for x in descents(a, q) if x not in own and x in H[(q, g)])))
    d["autres_courbes_meme_image"] = other
    d.to_csv(D / "base_change.csv", index=False)
    for kind, x in d.groupby("objet"):
        print(f"{kind}: n = {len(x)} ; rang sur F_q² = zéros distincts de beta² : {int((x.rang_q2 == x.zeros_distincts_q2).sum())} ; "
              f"écart max {x.ecart_beta2.max():.1e} ; unitaire : {int((x.ecart_unitaire_q2 < 1e-8).sum())} ; négatifs = hors cercle / 2 : {int((x.negatifs_q2 == x.hors_cercle // 2).sum())} ; "
              f"négatifs = hors cercle distincts / 2 : {int((x.negatifs_q2 == x.hors_cercle_q2_distincts // 2).sum())} ; rang qui baisse : {int((x.zeros_distincts_q2 < x.zeros_distincts_q).sum())}")
    c = d[d.objet == "courbe"]
    print("zéros sur F_q² = zéros de la courbe et de sa tordue :", int(c.zeros_q2_egal_q_et_tordue.sum()), "/", len(c))
    print("descentes : courbe et tordue toujours présentes :", int((c.contient_courbe & c.contient_tordue).sum()), "/", len(c),
          "; distribution :", c.descentes.value_counts().sort_index().to_dict(), "; tordue = courbe :", int(c.tordue_egale.sum()))
    print("descentes = signes des facteurs irréductibles :", int((c.descentes == c.descentes_par_facteurs).sum()), "/", len(c),
          "; facteurs :", c.facteurs_irreductibles.value_counts().sort_index().to_dict())
    print("autres courbes du corpus (ni elle ni sa tordue) avec les mêmes comptages sur F_q² :", int(c.autres_courbes_meme_image.sum()),
          "; courbes ayant d'autres descentes que la tordue :", int((c.descentes > 2).sum()))
    metric_step()
    print(f"total {time.time() - t0:.0f} s")

def metric_step():
    """La métrique du générateur des premiers selon le pas h (aucun zéro utilisé)."""
    from prime_generator import traces_from_primes, toeplitz_pencil
    from rejection import coeffs, log_derivative_coeffs
    a = 0.04; rows = []; cc = {}
    def run(kind, h, N):
        M = int(math.exp(N * h + 2 * a)) + 3
        if kind not in cc or len(cc[kind]) - 1 < M: cc[kind] = log_derivative_coeffs(coeffs(kind, max(M, 3000)))
        t = traces_from_primes(kind, cc[kind], N, h, a); G, _ = toeplitz_pencil(t, N)
        mu = np.linalg.eigvalsh(0.5 * (G + G.conj().T)); tol = 1e-11 * np.max(np.abs(mu))
        return M, int(np.sum(mu < -tol)), float(mu[0])
    for h in (0.01, 0.02, 0.05, 0.1, 0.2, 0.5, math.log(2)):
        N = int(round(6.0 / h))
        for kind in ("zeta", "L_chi5", "DH"):
            M, neg, m0 = run(kind, h, N); rows.append(dict(mode="X fixé", objet=kind, h=h, N=N, X=M, negatifs=neg, mu_min=m0))
    for h in (0.02, 0.03, 0.04, 0.05):
        M, neg, m0 = run("DH", h, 300); rows.append(dict(mode="N fixé", objet="DH", h=h, N=300, X=M, negatifs=neg, mu_min=m0))
    d = pd.DataFrame(rows); d.to_csv(D / "base_metric_step.csv", index=False)
    for (mode, kind), x in d.groupby(["mode", "objet"], sort=False):
        print(f"métrique, {mode}, {kind} : négatifs {list(x.negatifs)} pour h = {[round(v, 3) for v in x.h]}", flush=True)

def figure():
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#52514e",
                         "xtick.color": "#52514e", "ytick.color": "#52514e", "axes.titlesize": 9.5})
    BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#52514e"
    fig, ax = plt.subplots(1, 3, figsize=(16.5, 3.8), gridspec_kw=dict(width_ratios=[1, 1.3, 0.9]))
    st = pd.read_csv(D / "generator_step.csv")
    A = ax[0]
    A.plot(st.h, st.vraies_sans_repliement, "-o", color=BLUE, ms=4, lw=1.8, label="zéros retrouvés à leur place")
    A.plot(st.h, st.fortes_sur_un_zero_replie - st.vraies_sans_repliement.clip(upper=st.fortes_sur_un_zero_replie), "-s", color=ORANGE, ms=4, lw=1.8, label="zéros vus repliés (γ modulo 2π/h)")
    A.set_xscale("log"); A.set_xticks([0.02, 0.05, 0.1, 0.2, 0.5]); A.set_xticklabels(["0,02", "0,05", "0,1", "0,2", "0,5"]); A.minorticks_off(); A.axvline(math.log(2), color=GREY, lw=0.8, ls=(0, (3, 3))); A.text(math.log(2), A.get_ylim()[1] * 0.92, " pas log 2\n (une « base »)", fontsize=7.5, color=GREY, va="top")
    A.set_xlabel("pas h (nombres premiers ≤ 475 dans tous les cas)"); A.set_ylabel("valeurs propres de ζ")
    A.set_title("ζ : plus le pas grandit, plus les zéros se replient", loc="left"); A.legend(frameon=False, fontsize=8, loc="upper right", bbox_to_anchor=(0.86, 1.0))
    B = ax[1]; cur = pd.read_csv(D / "stability_model_curves.csv")
    bc = pd.read_csv(D / "base_change.csv"); ok = bc[(bc.objet == "courbe") & (bc.q == 3) & (bc.g == 2) & (bc.descentes == 2) & (~bc.tordue_egale.astype(bool))]
    x = ok.iloc[0]; c = list(map(int, x.P.split())); q = 3; lq = math.log(q)
    b = normalized(c, q); btw = normalized([ck * (-1) ** k for k, ck in enumerate(c)], q); T = 2 * 2 * math.pi / lq
    g1 = curve_gammas(b, q, T).real; gt = curve_gammas(btw, q, T).real
    g1 = g1[(g1 >= 0) & (g1 <= T)]; gt = gt[(gt >= 0) & (gt <= T)]
    B.scatter(g1, np.full_like(g1, 1.0), marker="|", s=260, color=BLUE, lw=2, label=f"zéros de la courbe (P = {x.P.replace(' ', ', ')})")
    B.scatter(g1, np.full_like(g1, 0.12), marker="|", s=160, color=BLUE, lw=2)
    B.scatter(gt, np.full_like(gt, -0.12), marker="|", s=160, color=ORANGE, lw=2, label="zéros de sa tordue (P(−u))")
    for k in range(0, 3): B.axvline(k * 2 * math.pi / lq, ymin=0.55, ymax=0.95, color=GREY, lw=0.8, ls=(0, (2, 2)))
    for k in range(0, 5): B.axvline(k * math.pi / lq, ymin=0.05, ymax=0.45, color=GREY, lw=0.8, ls=(0, (2, 2)))
    B.set_yticks([0, 1]); B.set_yticklabels(["vus sur F₉\n(pas 2·log 3)", "vus sur F₃\n(pas log 3)"]); B.set_ylim(-0.6, 1.6); B.set_xlim(-0.2, T + 0.2)
    B.set_xlabel("γ (hauteur) ; pointillés : période 2π/log 3 en haut, π/log 3 en bas")
    B.set_title("Une courbe sur F₃ vue sur F₉ : la période se divise par deux, la tordue se superpose", loc="left")
    B.legend(frameon=False, fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=2)
    C = ax[2]; ms = pd.read_csv(D / "base_metric_step.csv")
    x1 = ms[(ms["mode"] == "X fixé") & (ms.objet == "DH")]; x2 = ms[ms["mode"] == "N fixé"]
    C.plot(x1.h, x1.negatifs, "-o", color=BLUE, ms=4, lw=1.8, label="premiers fixés (X ≈ 440)")
    C.plot(x2.h, x2.negatifs, "-s", color=ORANGE, ms=4, lw=1.8, label="échantillons fixés (N = 300)")
    C.set_xscale("log"); C.set_xticks([0.01, 0.02, 0.05, 0.1, 0.2, 0.5]); C.set_xticklabels(["0,01", "0,02", "0,05", "0,1", "0,2", "0,5"]); C.minorticks_off()
    C.set_xlabel("pas h"); C.set_ylabel("directions négatives (DH)"); C.set_ylim(-0.5, 11.5)
    C.set_title("DH : la métrique se noie quand les échantillons manquent", loc="left")
    C.legend(frameon=False, fontsize=7.5, loc="upper right", bbox_to_anchor=(1.0, 1.0))
    C.text(0.085, 4.6, "ζ et L(s, χ₅) : aucune\ndirection négative, à tous les pas", fontsize=7.5, color=GREY)
    fig.tight_layout(w_pad=2.5); fig.savefig(D / "base_step.png", dpi=150, bbox_inches="tight"); print("figure écrite")

if __name__ == "__main__":
    if "--figure" not in sys.argv: main()
    figure()
