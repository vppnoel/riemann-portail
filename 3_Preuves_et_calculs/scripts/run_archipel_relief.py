"""V6.31 — Le relief de l'archipel : la carte de V_7 impair (doc. 30) vue en une seule représentation 3D.

Auteur et titulaire des droits : Vincent NOËL.
Prévisions écrites avant le calcul : data/prevision_v631_relief.md.

En chaque point (u, v) de la carte, T*(u, v) est le premier seuil entier à partir duquel le déficit sur la droite,
par rapport au point d'Euler le plus proche, reste au moins égal à 2 jusqu'à 300. C'est un indicateur relatif,
dont la V6.34 distingue la première paire hors droite (doc. 58). Les îles sont les composantes de {T* > T}.
La colonne historique T_premiere_paire garde son nom pour la compatibilité, mais stocke ce seuil relatif.
Sorties : data/archipel_relief.csv, data/archipel_relief.json, 1_Presentation/56_Le_relief_de_l_archipel.png.
"""
from __future__ import annotations
from pathlib import Path
import json, math, sys, time
import numpy as np, pandas as pd
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]; D = ROOT / "data"; sys.path.insert(0, str(ROOT / "src"))
from euler_archipelago import characters, hardy_grid

TMAX, H = 300.0, 0.01
LEVELS = np.arange(1, 301)


def relief():
    q, par = 7, 1
    t = np.arange(-TMAX, TMAX + H / 2, H); Z, defect, ch = hardy_grid(q, par, t)
    nvec = np.ones(3) / math.sqrt(3); a = np.array([1.0, -1.0, 0.0]) / math.sqrt(2); b = np.cross(nvec, a)
    n = 141; us = np.linspace(-1.75, 1.75, n); UU, VV = np.meshgrid(us, us)
    P = nvec[None, :] + UU.ravel()[:, None] * a[None, :] + VV.ravel()[:, None] * b[None, :]; P /= np.linalg.norm(P, axis=1)[:, None]
    near = np.argmax(np.abs(P), axis=1)
    tm = np.abs(0.5 * (t[1:] + t[:-1])); order = np.argsort(tm, kind="stable"); tms = tm[order]
    cut = np.searchsorted(tms, LEVELS, side="right")            # nombre de milieux de pas avec |t| <= T

    def counts(Zrows):
        c = (np.sign(Zrows[:, 1:]) * np.sign(Zrows[:, :-1]) < 0)[:, order].astype(np.int32)
        cs = np.cumsum(c, axis=1); return np.where(cut[None, :] > 0, cs[:, np.maximum(cut - 1, 0)], 0)

    Nref = counts(Z)                                            # 3 x 300 : points d'Euler
    DEF = np.empty((len(P), len(LEVELS)), dtype=np.int16)
    for i0 in range(0, len(P), 150):
        DEF[i0:i0 + 150] = Nref[near[i0:i0 + 150]] - counts(P[i0:i0 + 150] @ Z)
    hit = DEF >= 2
    T_first = np.where(hit.any(axis=1), LEVELS[np.argmax(hit, axis=1)], 10 ** 6)          # critère prévu
    # Déficit relatif persistant jusqu'au plafond ; sa persistance ne prouve
    # pas que T soit la hauteur d'une première paire hors droite.
    ok_after = np.flip(np.cumprod(np.flip(hit, axis=1), axis=1), axis=1).astype(bool)
    Tstar = np.where(ok_after.any(axis=1), LEVELS[np.argmax(ok_after, axis=1)], 10 ** 6)
    transitoires = float(np.mean([(h.any() and not h[np.argmax(h):].all()) for h in hit]))
    eu = []
    for i in range(3):
        e = np.eye(3)[i]; e = e / (e @ nvec); eu.append(dict(nom=f"L(s, chi_{ch[i]['k']})", u=float(e @ a), v=float(e @ b)))
    return UU, VV, Tstar.reshape(n, n), eu, float(defect), T_first.reshape(n, n), transitoires


def analyse(UU, VV, TS, eu):
    n = TS.shape[0]; us = UU[0]
    pk = [(int(np.argmin(np.abs(us - e["v"]))), int(np.argmin(np.abs(us - e["u"])))) for e in eu]   # (ligne, colonne)
    rep = dict(points=int(TS.size), sommets_au_dessus_de_300=int((TS > 300).sum()),
               sommets_hauteur=[float(TS[r, c]) for r, c in pk],
               part_au_dessus={str(T): float((TS > T).mean()) for T in (25, 50, 100, 150, 200, 300)})
    cols = {}
    for i in range(3):
        for j in range(i + 1, 3):
            h = 0
            for T in LEVELS:
                lab, _ = ndimage.label(TS > T)
                if lab[pk[i]] and lab[pk[i]] == lab[pk[j]]: h = int(T)
                else: break
            cols[f"{eu[i]['nom']} / {eu[j]['nom']}"] = h
    rep["cols"] = cols
    comp = {}
    for T in (25, 50, 75, 100, 150, 200, 300):
        lab, k = ndimage.label(TS > T); comp[str(T)] = int(k)
    rep["composantes"] = comp
    return rep


def figure(UU, VV, TS, eu, out):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from matplotlib import cm
    from matplotlib.colors import LightSource, Normalize
    top = math.log10(400); Z = np.log10(np.minimum(TS, 400)); floor = -0.9
    fig = plt.figure(figsize=(10.5, 7.6)); ax = fig.add_subplot(111, projection="3d")
    norm = Normalize(0, top); ls = LightSource(azdeg=315, altdeg=40)
    rgb = ls.shade(Z, cmap=cm.gist_earth, norm=norm, blend_mode="soft", vert_exag=0.4)
    ax.plot_surface(UU, VV, Z, facecolors=rgb, rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False)
    levels = [(50, "#1f77b4", "T = 50"), (145, "#d62728", "T = 145 (les îles se séparent)"), (300, "#111111", "T = 300")]
    for T, col, lab in levels:
        ax.contour(UU, VV, Z, levels=[math.log10(T)], colors=[col], linewidths=1.0, offset=floor)
        ax.contour(UU, VV, Z, levels=[math.log10(T)], colors=[col], linewidths=0.9)
        ax.plot([], [], color=col, label=f"rivage au niveau {lab}")
    ax.set_zlim(floor, top + 0.3); ax.view_init(elev=34, azim=-100)
    from mpl_toolkits.mplot3d import proj3d
    fig.canvas.draw()
    for e in eu:
        ax.plot([e["u"], e["u"]], [e["v"], e["v"]], [floor, top], color="#a01818", lw=0.6, ls=":")
        x2, y2, _ = proj3d.proj_transform(e["u"], e["v"], top + 0.1, ax.get_proj())
        ax.annotate(e["nom"].replace("chi_", "χ"), (x2, y2), xytext=(0, 8), textcoords="offset points", color="#a01818", fontsize=9, ha="center",
                    bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8), zorder=10)
    ax.set_zticks([0, 1, math.log10(50), 2, top]); ax.set_zticklabels(["1", "10", "50", "100", ">300"])
    ax.set_zlabel("T* : seuil de déficit persistant"); ax.set_xlabel("u"); ax.set_ylabel("v")
    ax.legend(loc="upper left", fontsize=8, frameon=False)
    ax.set_title("V₇ impair : relief du déficit persistant ; sommets censurés à 300.\n"
                 "Sous T = 145, un seul continent relie les trois points d'Euler ; au-dessus, trois îles. Rivages reportés au sol.", fontsize=10)
    fig.text(0.99, 0.01, "Données V6.31, légende corrigée V6.34 — © Vincent NOËL", ha="right", fontsize=7, color="#777")
    fig.tight_layout(); fig.savefig(out, dpi=130); plt.close(fig)


def main():
    t0 = time.time(); UU, VV, TS, eu, defect, TF, tr = relief()
    rep = dict(critere_persistant=analyse(UU, VV, TS, eu), critere_prevu_premier_deficit=analyse(UU, VV, TF, eu),
               part_des_points_a_deficit_transitoire=tr); rep["defaut_imaginaire_max"] = defect; rep["secondes"] = round(time.time() - t0, 1)
    pd.DataFrame(dict(u=UU.ravel(), v=VV.ravel(), T_premiere_paire=TS.ravel(), T_premier_deficit=TF.ravel())).to_csv(D / "archipel_relief.csv", index=False)
    (D / "archipel_relief.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    figure(UU, VV, TS, eu, ROOT.parent / "1_Presentation" / "56_Le_relief_de_l_archipel.png")
    print(json.dumps(rep, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
