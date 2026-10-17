"""V6.29 — Lire Bogomolny et al. pour de vrai : le trou à trois.

Auteur et titulaire des droits : Vincent NOËL.
Prévisions écrites avant le calcul : data/prevision_v629_bblm.md.

1. Fraction de triples consécutifs de portée < 1 (écarts dépliés) dans le CUE(N), N = 3 à 40, et ajustement a + b/N²
   pour N ≥ 4 (forme de la correction de Bogomolny et al. [BBLM06]) ; prolongement à la taille effective de ζ.
2. Test de Nishigaki [Nis25] : le rapport d'écarts r̃ = min/max de deux écarts consécutifs, insensible à l'échelle,
   comparé au noyau sinus (CUE(60)) pour ζ, L(χ5), Δ ; contraste avec la portée w = s_i + s_{i+1}.
"""
from __future__ import annotations
from pathlib import Path
import json, math
import numpy as np, pandas as pd
from scipy.stats import ks_2samp

ROOT = Path(__file__).resolve().parents[1]; D = ROOT / "data"
LAM = 1.57314


def cue_angles(N, reps, rng, batch=2000):
    out = []
    for k in range(0, reps, batch):
        m = min(batch, reps - k)
        Z = (rng.standard_normal((m, N, N)) + 1j * rng.standard_normal((m, N, N))) / np.sqrt(2)
        Q, R = np.linalg.qr(Z); d = np.diagonal(R, axis1=1, axis2=2); Q = Q * (d / np.abs(d))[:, None, :]
        out.append(np.sort(np.angle(np.linalg.eigvals(Q)), axis=1))
    return np.vstack(out)


def cue_spacings(th):
    """Écarts dépliés cycliques (moyenne 1) : tableau (reps, N)."""
    N = th.shape[1]; ext = np.c_[th, th[:, :1] + 2 * np.pi]
    return np.diff(ext, axis=1) * N / (2 * np.pi)


def triples_fraction(s):
    w = s + np.roll(s, -1, axis=1)
    return float((w < 1).mean()), float(np.sqrt((w < 1).mean() * (1 - (w < 1).mean()) / w.size))


def ratios(s1, s2):
    return np.minimum(s1, s2) / np.maximum(s1, s2)


def unfold(t):
    t = np.sort(t); r = np.arange(1, len(t) + 1); A = np.c_[t * np.log(t), t, np.ones_like(t)]
    return A @ np.linalg.lstsq(A, r, rcond=None)[0]


def objets():
    g = pd.read_csv(D / "zeta_zeros_1500.csv").t.values; L = pd.read_csv(D / "L_chi5_zeros_600.csv").t.values
    dz = pd.read_csv(D / "delta_zeros_contour.csv"); col = [c for c in dz.columns if c.lower() in ("t", "gamma")][0]
    return {"zeta (t ≤ 1 500)": g[g > 0], "L(chi5) (t ≤ 600)": L[L > 0], "Delta (t ≤ 1 500)": dz[col].values[dz[col].values > 1]}


def main():
    rng = np.random.default_rng(629)
    # 1. CUE(N)
    cue = []
    for N, reps in ((3, 200000), (4, 100000), (5, 80000), (6, 60000), (8, 40000), (10, 30000), (14, 20000), (20, 15000), (40, 8000)):
        f, e = triples_fraction(cue_spacings(cue_angles(N, reps, rng)))
        cue.append(dict(N=N, fraction=f, erreur=e))
    big = [c for c in cue if c["N"] >= 4]
    X = np.c_[np.ones(len(big)), [1 / c["N"] ** 2 for c in big]]; W = np.array([1 / c["erreur"] for c in big])
    a, b = np.linalg.lstsq(X * W[:, None], np.array([c["fraction"] for c in big]) * W, rcond=None)[0]
    c3 = cue[0]; pred3 = a + b / 9
    # prolongement à ζ
    g = objets()["zeta (t ≤ 1 500)"]; ne = np.log(g / (2 * np.pi)) / math.sqrt(12 * LAM); ne = ne[1:-1]
    prol = np.clip(a + b / ne ** 2, 0, None)
    # 2. référence noyau sinus : CUE(60)
    s = cue_spacings(cue_angles(60, 4000, rng)); s1 = s.ravel(); s2 = np.roll(s, -1, axis=1).ravel()
    r_ref = ratios(s1, s2); w_ref = s1 + s2
    ref = dict(r_moyen=float(r_ref.mean()), r_ecart=float(r_ref.std()), w_lt1=float((w_ref < 1).mean()))
    rows = []
    for name, t in objets().items():
        u = unfold(t); sp = np.diff(u); r = ratios(sp[:-1], sp[1:]); w = sp[:-1] + sp[1:]
        tg = np.sort(t); r_brut = ratios(np.diff(tg)[:-1], np.diff(tg)[1:])
        n = len(r); se = ref["r_ecart"] / math.sqrt(n)
        rows.append(dict(objet=name, rapports=int(n), r_moyen=float(r.mean()), r_moyen_sans_depliage=float(r_brut.mean()),
                         ecart_en_sigma=float((r.mean() - ref["r_moyen"]) / se),
                         ks_r_p=float(ks_2samp(r, r_ref).pvalue), ks_w_p=float(ks_2samp(w, w_ref).pvalue),
                         triples_lt1=int((w < 1).sum()), attendu_sinus=float(ref["w_lt1"] * n),
                         r_lt_0_2=int((r < 0.2).sum()), r_lt_0_2_attendu=float((r_ref < 0.2).mean() * n)))
    rep = dict(cue=cue, fit=dict(a=float(a), b=float(b), domaine="N >= 4"),
               cue3=dict(mesure=c3["fraction"], erreur=c3["erreur"], fit_prolonge=float(pred3)),
               prolongement_zeta=dict(N_eff_min=float(ne.min()), N_eff_max=float(ne.max()), fraction_moyenne=float(prol.mean()),
                                      attendu=float(prol.sum())),
               reference_sinus=ref, objets=rows)
    (D / "bblm_trou_a_trois.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(rep, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
