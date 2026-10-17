#!/usr/bin/env python3
"""V6.9 — Le chaînon : reconstruire le Frobenius à partir des comptages, puis lire les longueurs dans les zéros.

A. Modèle réduit (525 vraies courbes, 220 faux jumeaux, 5 polynômes à zéros confondus) : construction de type GNS
   depuis les traces seules ; dimension, valeurs propres, positivité, symétrie de l'équation fonctionnelle.
B. Spectre des longueurs lu dans les zéros : zeta (|t| <= 1 500), L(s, chi_5) et DH (|t| <= 600), une courbe sur F_3,
   un faux jumeau sur F_5, le produit d'une courbe sur F_3 et d'une courbe sur F_5 (deux bases).
Sorties : data/chain_gns.csv, data/chain_lengths.csv, data/chain_length_spectrum.csv, data/chain.png.
"""
from pathlib import Path
import sys, math, time
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from frobenius_chain import (gns_frobenius, distinct, match_error, inverse_closure, length_spectrum,
                             log_derivative_coefficients, is_prime_power, curve_gammas, traces_from_b)
from stability_radius import normalized
from zero_reconstruction import nontrivial_zeros
from rejection import KAPPA_DH
D = ROOT / "data"
U = np.round(np.arange(0.30, 3.6005, 0.001), 6)
NMAX = 36

def figure():
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    sp = pd.read_csv(D / "chain_length_spectrum.csv"); g = pd.read_csv(D / "chain_gns.csv")
    blue, red, grey, green, orange = "#1f4e79", "#c0392b", "0.55", "#2e8b57", "#d4801a"
    fig = plt.figure(figsize=(11, 10.4), dpi=150); outer = fig.add_gridspec(2, 1, height_ratios=[4, 1.55], hspace=0.22)
    top = outer[0].subgridspec(4, 1, hspace=0.62); bottom = outer[1].subgridspec(1, 2, wspace=0.32)
    rows = (("zeta", "ζ : pics aux puissances de nombres premiers", blue),
            ("DH", "Davenport–Heilbronn : pics aussi en log 6, log 12… (pas de produit d'Euler)", red),
            ("courbe_F3", "Courbe sur F₃ : une seule base, pics en n·log 3", green),
            ("deux_courbes", "Courbe sur F₃ × courbe sur F₅ : deux bases, pics en n·log 3 et n·log 5", orange))
    for k, (obj, title, col) in enumerate(rows):
        ax = fig.add_subplot(top[k, 0]); y = sp[obj].values
        ax.set_ylim(min(y.min(), 0) * 1.15 - 0.05, y.max() * 1.25 + 0.05)
        ax.plot(sp.u, y, color=col, lw=0.9); ax.axhline(0, color="0.75", lw=0.6)
        if obj in ("zeta", "DH"):
            for n in range(2, NMAX + 1):
                if obj == "DH" and n % 5 == 0: continue
                x = math.log(n)
                if x > U[-1]: break
                pp = is_prime_power(n)
                ax.axvline(x, color=("0.82" if pp else "#f2b8b0"), lw=0.6, zorder=0)
                if not pp and obj == "DH" and n <= 26: ax.text(x, ax.get_ylim()[1] * 0.82 if False else 0, "", fontsize=6)
        if obj == "DH":
            for n in (6, 12, 14, 18, 21, 22, 24, 26):
                ax.annotate(str(n), (math.log(n), sp.loc[(sp.u - math.log(n)).abs().idxmin(), obj]), xytext=(0, 6), textcoords="offset points", ha="center", fontsize=7, color=red)
        if obj == "zeta":
            for n in (2, 3, 4, 5, 7, 8, 9, 11, 13):
                ax.annotate(str(n), (math.log(n), sp.loc[(sp.u - math.log(n)).abs().idxmin(), obj]), xytext=(0, 4), textcoords="offset points", ha="center", fontsize=7, color=blue)
        ax.set_title(title, fontsize=9.5, loc="left"); ax.set_xlim(U[0], U[-1]); ax.tick_params(labelsize=8)
        if k == 3: ax.set_xlabel("longueur u (pic en u = log n : une « orbite » de longueur log n)")
    ax = fig.add_subplot(bottom[0, 0])
    for kind, col, lab in (("courbe", blue, "vraies courbes, zéros simples (524)"), ("faux jumeau", red, "faux jumeaux (220)"), ("zéros confondus", green, "zéros confondus (5)")):
        d = g[g.objet == kind]
        ax.scatter(np.sign(d.gram_min_rel) * np.log10(1 + np.abs(d.gram_min_rel) / 1e-12), np.log10(np.maximum(d.ecart_unitaire, 1e-16)), s=9, color=col, alpha=0.7, label=lab)
    ax.axvline(0, color="0.5", lw=0.8, ls="--"); ax.set_xlabel("signe × log₁₀(1 + |λ_min du Gram| / 10⁻¹²)"); ax.set_ylabel("log₁₀ max ||λ| − 1|")
    ax.set_title("Métrique positive ⟺ opérateur unitaire ⟺ RH", fontsize=9.5); ax.legend(frameon=False, fontsize=7.5, loc="center left")
    ax = fig.add_subplot(bottom[0, 1])
    d = g[g.objet != "faux jumeau"]
    ax.scatter(d.dimension_2g, d.rang_gns, s=12, color=blue, alpha=0.6, label="courbes")
    ax.plot([2, 24], [2, 24], color="0.6", lw=0.8, ls="--")
    e = g[g.objet == "zéros confondus"]; ax.scatter(e.dimension_2g, e.rang_gns, s=30, color=green, marker="D", label="zéros confondus : rang < 2g")
    ax.set_xlabel("2g (nombre de zéros, avec multiplicité)"); ax.set_ylabel("dimension reconstruite")
    ax.set_title("L'espace reconstruit : un axe par zéro distinct", fontsize=9.5); ax.legend(frameon=False, fontsize=7.5)
    fig.savefig(D / "chain.png", bbox_inches="tight"); print("figure écrite")

if __name__ == "__main__":
    if "--figure" in sys.argv:
        figure(); sys.exit(0)
    t0 = time.time()
    # ---------------- A : reconstruction GNS
    rows = []
    def record(kind, q, g, c, label):
        b = normalized(c, q); beta = 1 / np.roots(np.asarray(b[::-1], dtype=float)); bd = distinct(beta)
        r, lam, ev = gns_frobenius(b); offc = int(np.sum(np.abs(np.abs(beta) - 1) > 1e-6))
        rows.append(dict(objet=kind, q=q, g=g, P=" ".join(map(str, c)), etiquette=label, dimension_2g=2 * g, zeros_distincts=len(bd), rang_gns=r,
                         ecart_valeurs_propres=match_error(lam, bd) if r == len(bd) else float("nan"),
                         ecart_unitaire=float(np.max(np.abs(np.abs(lam) - 1))), gram_min_rel=float(ev[0] / np.max(np.abs(ev))),
                         gram_negatives=int(np.sum(ev < -1e-9 * np.max(np.abs(ev)))), hors_cercle=offc, symetrie_eq_fonct=inverse_closure(lam)))
    for _, x in pd.read_csv(D / "stability_model_curves.csv").iterrows():
        record("zéros confondus" if x.zeros_confondus else "courbe", int(x.q), int(x.g), list(map(int, x.P.split())), f"courbe {x.courbe}")
    for _, x in pd.read_csv(D / "stability_model_fakes.csv").iterrows():
        q, g = int(x.q), int(x.g); c = [1, int(x.c1), q] if g == 1 else [1, int(x.c1), int(float(x.c2)), q * int(x.c1), q * q]
        record("faux jumeau", q, g, c, f"({int(x.c1)}, {x.c2})")
    for c, lab in (([1, 0, 10, 0, 25], "(1 + 5u²)²"), ([1, -4, 14, -20, 25], "(1 − 2u + 5u²)²"), ([1, 4, 14, 20, 25], "(1 + 2u + 5u²)²"), ([1, 0, -10, 0, 25], "(1 − 5u²)²")):
        record("zéros confondus", 5, 2, c, lab)
    dg = pd.DataFrame(rows); dg.to_csv(D / "chain_gns.csv", index=False)
    for kind, d in dg.groupby("objet"):
        print(f"{kind:16s} n={len(d):3d} ; rang = zéros distincts : {int((d.rang_gns == d.zeros_distincts).sum())} ; écart des valeurs propres max {d.ecart_valeurs_propres.max():.1e} ;"
              f" unitaire (écart < 1e-8) : {int((d.ecart_unitaire < 1e-8).sum())} ; Gram positif : {int((d.gram_negatives == 0).sum())} ;"
              f" négatifs = hors cercle / 2 : {int((d.gram_negatives == d.hors_cercle // 2).sum())} ; symétrie max {d.symetrie_eq_fonct.max():.1e}", flush=True)
    # ---------------- B : spectre des longueurs
    gz = pd.read_csv(D / "zeta_zeros_1500.csv").t.values; zeta = np.concatenate([gz, -gz]).astype(complex)
    gl = -1j * (nontrivial_zeros("L_chi5") - 0.5); gd = -1j * (nontrivial_zeros("DH") - 0.5)
    chi = {1: 1, 2: 1j, 3: -1j, 4: -1, 0: 0}
    aL = np.array([0] + [chi[n % 5] for n in range(1, NMAX + 1)], dtype=complex)
    aD = np.array([0] + [(0.5 * (1 - 1j * KAPPA_DH) * chi[n % 5] + 0.5 * (1 + 1j * KAPPA_DH) * np.conj(chi[n % 5])) for n in range(1, NMAX + 1)], dtype=complex)
    cZ = log_derivative_coefficients(np.ones(NMAX + 1, dtype=complex)); cL = log_derivative_coefficients(aL); cD = log_derivative_coefficients(aD)
    cur = pd.read_csv(D / "stability_model_curves.csv")
    def pick(q):                                           # courbe de genre 2 aux traces les plus marquées aux premiers étages
        d = cur[(cur.q == q) & (cur.g == 2) & (cur.rayon_objet > 0.1)].copy()
        d["force"] = d.P.apply(lambda P: abs(traces_from_b(normalized(list(map(int, P.split())), q), 3)[1:]).sum())
        return d.sort_values(["force", "courbe"], ascending=[False, True]).iloc[0]
    c3, c5 = pick(3), pick(5)
    b3 = normalized(list(map(int, c3.P.split())), 3); b5 = normalized(list(map(int, c5.P.split())), 5); bf = normalized([1, 1, -8, 5, 25], 5)
    objs = {"zeta": (zeta, 500.0), "L_chi5": (gl, 200.0), "DH": (gd, 200.0),
            "courbe_F3": (curve_gammas(b3, 3, 600.0), 200.0), "faux_jumeau_F5": (curve_gammas(bf, 5, 600.0), 200.0),
            "deux_courbes": (np.concatenate([curve_gammas(b3, 3, 600.0), curve_gammas(b5, 5, 600.0)]), 200.0)}
    spec = {"u": U}; peaks = []
    for name, (gam, s) in objs.items():
        S = length_spectrum(gam, U, s); spec[name] = S.real if name != "L_chi5" else np.abs(S)
        at = lambda x: S[int(np.argmin(np.abs(U - x)))]
        if name in ("zeta", "L_chi5", "DH"):
            cc = {"zeta": cZ, "L_chi5": cL, "DH": cD}[name]
            for n in range(2, NMAX + 1):
                if math.log(n) > U[-1] or (name != "zeta" and n % 5 == 0): continue
                peaks.append(dict(objet=name, longueur=math.log(n), n=n, puissance_premiere=is_prime_power(n), mesure=complex(at(math.log(n))),
                                  predit=complex(cc[n] / math.sqrt(n))))
        else:
            for qq, bb in ({"courbe_F3": [(3, b3)], "faux_jumeau_F5": [(5, bf)], "deux_courbes": [(3, b3), (5, b5)]}[name]):
                p = traces_from_b(bb, 12)
                for n in range(1, 12):
                    if n * math.log(qq) > U[-1]: break
                    peaks.append(dict(objet=name, longueur=n * math.log(qq), n=qq ** n, puissance_premiere=True, mesure=complex(at(n * math.log(qq))),
                                      predit=complex(-math.log(qq) * p[n])))
            # hors du réseau : plus grand |S| à distance > 0,05 de toute longueur n log q
            lat = [n * math.log(qq) for qq, _ in {"courbe_F3": [(3, 0)], "faux_jumeau_F5": [(5, 0)], "deux_courbes": [(3, 0), (5, 0)]}[name] for n in range(1, 12)]
            far = np.array([min(abs(x - l) for l in lat) > 0.05 for x in U])
            peaks.append(dict(objet=name, longueur=float("nan"), n=0, puissance_premiere=False, mesure=complex(np.max(np.abs(S[far]))), predit=0j))
        print(f"{name} : {len(gam)} zéros, {time.time() - t0:.0f} s", flush=True)
    pd.DataFrame(spec).to_csv(D / "chain_length_spectrum.csv", index=False)
    dp = pd.DataFrame(peaks)
    dp["mesure_re"] = dp.mesure.apply(lambda z: z.real); dp["mesure_im"] = dp.mesure.apply(lambda z: z.imag)
    dp["predit_re"] = dp.predit.apply(lambda z: z.real); dp["predit_im"] = dp.predit.apply(lambda z: z.imag)
    dp = dp.drop(columns=["mesure", "predit"]); dp.to_csv(D / "chain_lengths.csv", index=False)
    for name in ("zeta", "L_chi5", "DH"):
        d = dp[dp.objet == name]; m = np.abs(d.mesure_re + 1j * d.mesure_im)
        hors = m[~d.puissance_premiere].sum() / m.sum()
        err = np.max(np.abs((d.mesure_re + 1j * d.mesure_im) - (d.predit_re + 1j * d.predit_im)))
        print(f"{name} : part des pics hors puissances de nombres premiers {hors:.3f} ; écart max mesure / prédiction {err:.3f}", flush=True)
    for name in ("courbe_F3", "faux_jumeau_F5", "deux_courbes"):
        d = dp[(dp.objet == name) & (dp.n > 0)]; far = dp[(dp.objet == name) & (dp.n == 0)].mesure_re.iloc[0]
        err = np.max(np.abs((d.mesure_re + 1j * d.mesure_im) - (d.predit_re + 1j * d.predit_im)))
        print(f"{name} : écart max aux longueurs n log q {err:.3f} (pics jusqu'à {np.max(np.abs(d.predit_re)):.2f}) ; plus grand |S| hors du réseau {far:.3f}", flush=True)
    figure(); print(f"total {time.time() - t0:.0f} s")
