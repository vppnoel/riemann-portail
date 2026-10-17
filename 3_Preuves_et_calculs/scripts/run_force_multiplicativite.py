"""V6.33 — La force qui abaisse le relief : le défaut de multiplicativité sur la carte de V_7 impair.

Auteur et titulaire des droits : Vincent NOËL.
Prévisions écrites avant le calcul : data/prevision_v633_force.md.
Entrée : data/archipel_relief.csv (doc. 56). Sorties : data/force_multiplicativite.csv/.json,
1_Presentation/57_La_force_du_relief.png.
"""
from __future__ import annotations
from pathlib import Path
import json, math, sys
import numpy as np, pandas as pd
from scipy.stats import spearmanr, rankdata

ROOT = Path(__file__).resolve().parents[1]; D = ROOT / "data"; sys.path.insert(0, str(ROOT / "src"))
from euler_archipelago import characters


def coeffs_from_uv(u, v):
    nvec = np.ones(3) / math.sqrt(3); a = np.array([1.0, -1.0, 0.0]) / math.sqrt(2); b = np.cross(nvec, a)
    P = nvec[None, :] + u[:, None] * a[None, :] + v[:, None] * b[None, :]
    return P / np.linalg.norm(P, axis=1)[:, None]


def defect(P, q=7, par=1):
    ch = characters(q, par); R = list(range(1, q))
    X = np.array([[cmath_e(c["phi"]) * c["table"][r] for r in R] for c in ch])   # 3 x 6 : e^{-i phi} chi(r)
    A = P @ X                                                                      # N x 6 : A(r)
    idx = {r: k for k, r in enumerate(R)}
    A1 = A[:, idx[1]]
    num = np.zeros(len(P))
    for r in R:
        for s in R:
            num += np.abs(A1 * A[:, idx[(r * s) % q]] - A[:, idx[r]] * A[:, idx[s]]) ** 2
    return num / (np.sum(np.abs(A) ** 2, axis=1) ** 2)


def cmath_e(phi):
    return complex(math.cos(-phi), math.sin(-phi))


def partial_spearman(x, y, z):
    rx, ry, rz = rankdata(x), rankdata(y), rankdata(z)
    ex = rx - np.polyval(np.polyfit(rz, rx, 1), rz); ey = ry - np.polyval(np.polyfit(rz, ry, 1), rz)
    return float(np.corrcoef(ex, ey)[0, 1])


def main():
    r = pd.read_csv(D / "archipel_relief.csv"); u, v = r.u.values, r.v.values
    T = np.minimum(r.T_premiere_paire.values, 400.0)                                # sommets : au-delà de 300
    P = coeffs_from_uv(u, v); Dm = defect(P); d = np.arccos(np.clip(np.max(np.abs(P), axis=1), 0, 1))
    rep = {}
    rep["D1_spearman_T_D"] = float(spearmanr(T, Dm).correlation)
    rep["spearman_T_distance"] = float(spearmanr(T, d).correlation)
    rep["spearman_D_distance"] = float(spearmanr(Dm, d).correlation)
    rep["D2_partielle_T_D_sachant_d"] = partial_spearman(T, Dm, d)
    col = np.flatnonzero(r.T_premiere_paire.values == 145)
    below = []
    for i in col:
        same = np.abs(d - d[i]) < 0.02
        below.append(bool(Dm[i] < np.median(Dm[same])))
    rep["D3_points_du_col"] = int(len(col)); rep["D3_part_sous_la_mediane"] = float(np.mean(below)) if below else None
    rep["defaut_aux_points_d_Euler"] = float(defect(np.eye(3)).max())
    rep["defaut_max"] = float(Dm.max())
    # exploratoire, ajouté après avoir vu D2 et D3 : le premier coefficient a(1) = A(1), rapporté à ‖c‖
    w = np.array([cmath_e(c["phi"]) for c in characters(7, 1)]); A1 = np.abs(P @ w)
    rz = np.c_[rankdata(d), rankdata(A1), np.ones(len(T))]
    res = lambda x: rankdata(x) - rz @ np.linalg.lstsq(rz, rankdata(x), rcond=None)[0]
    rep["exploratoire_apres_coup"] = dict(partielle_T_A1_sachant_d=partial_spearman(T, A1, d), partielle_D_A1_sachant_d=partial_spearman(Dm, A1, d),
                                          partielle_T_D_sachant_d_et_A1=float(np.corrcoef(res(T), res(Dm))[0, 1]),
                                          A1_aux_points_d_Euler=1.0, A1_max_sur_la_carte=float(A1.max()))
    pd.DataFrame(dict(u=u, v=v, T_premiere_paire=r.T_premiere_paire.values, defaut=Dm, distance=d, a1=A1)).to_csv(D / "force_multiplicativite.csv", index=False)
    (D / "force_multiplicativite.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    figure(u, v, T, Dm, d, col, A1, ROOT.parent / "1_Presentation" / "57_La_force_du_relief.png")
    print(json.dumps(rep, indent=1, ensure_ascii=False))


def figure(u, v, T, Dm, d, col, A1, out):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    n = int(round(math.sqrt(len(u)))); U, V = u.reshape(n, n), v.reshape(n, n)
    fig, ax = plt.subplots(1, 3, figsize=(17, 4.9))
    im = ax[0].pcolormesh(U, V, Dm.reshape(n, n), cmap="magma_r", shading="auto")
    ax[0].contour(U, V, np.log10(T.reshape(n, n)), levels=[math.log10(145)], colors=["#1f77b4"], linewidths=1.1)
    ax[0].set_aspect("equal"); fig.colorbar(im, ax=ax[0], label="défaut de multiplicativité D")
    ax[0].set_title("Défaut D sur la carte de V₇ impair\n(trait bleu : rivage au niveau T = 145 du relief)", fontsize=10)
    sc = ax[1].scatter(d, Dm, c=np.log10(T), s=3, cmap="viridis")
    ax[1].scatter(d[col], Dm[col], s=14, facecolors="none", edgecolors="#d62728", lw=0.8, label="points du col (T* = 145)")
    fig.colorbar(sc, ax=ax[1], label="log₁₀ T*"); ax[1].set_xlabel("distance au point d'Euler le plus proche (radians)")
    ax[1].set_ylabel("défaut D"); ax[1].legend(fontsize=8); ax[1].set_title("À distance égale, plus de défaut va avec plus de hauteur\n(prévision D2 fausse)", fontsize=10)
    sc2 = ax[2].scatter(d, A1, c=np.log10(T), s=3, cmap="viridis"); fig.colorbar(sc2, ax=ax[2], label="log₁₀ T*")
    ax[2].set_xlabel("distance au point d'Euler le plus proche (radians)"); ax[2].set_ylabel("|a(1)| / ‖c‖ (premier coefficient)")
    ax[2].set_title("Ce qui ordonne la hauteur à distance égale :\nle premier coefficient a(1) (exploratoire)", fontsize=10)
    fig.text(0.99, 0.01, "Programme Riemann V6.33 — © Vincent NOËL", ha="right", fontsize=7, color="#777")
    fig.tight_layout(); fig.savefig(out, dpi=130); plt.close(fig)


if __name__ == "__main__":
    main()
