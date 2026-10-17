"""V6.28 — Axe A : la Rencontre à n en hauteur (taille effective de Bogomolny et al., formule det[D_N] à N réel).

Prévisions écrites avant le calcul : data/prevision_v628_hauteur.md (23 h 35 UTC).
D_N(s) = sin(πs)/(N sin(πs/N)) (s en écarts dépliés), R2_N = 1 − D_N², R3_N = det 3×3 ; N_eff(γ) = log(γ/2π)/√(12Λ), Λ = 1,57314.
La formule n'a de sens que pour s < N : on garde les origines avec N_eff ≥ 1 (γ ≥ 2π e^{√(12Λ)} ≈ 486).
"""
from __future__ import annotations
from pathlib import Path
import json, math, sys
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; D = ROOT / "data"; sys.path.insert(0, str(ROOT / "scripts"))
from run_rencontre_a_n import unfold_zeta, R3 as R3_sinus, sinc

LAM = 1.57314
def neff(g): return np.log(g / (2 * np.pi)) / math.sqrt(12 * LAM)
def DN(s, N):
    s = np.asarray(s, float); out = np.ones_like(s); m = np.abs(s) > 1e-12
    out[m] = np.sin(np.pi * s[m]) / (N * np.sin(np.pi * s[m] / N)); return out
def R3N(x, y, N):
    a, b, c = DN(x, N), DN(y, N), DN(x + y, N); return 1 - a * a - b * b - c * c + 2 * a * b * c
def R2N(s, N): return 1 - DN(s, N) ** 2

def zone_obs(u, idx, X=0.5):
    n = 0
    for i in idx:
        j = i + 1
        while j < len(u) and u[j] - u[i] < X:
            k = j + 1
            while k < len(u) and u[k] - u[j] < X: n += 1; k += 1
            j += 1
    return n

def tri_hist(u, idx, h=0.1, top=1.0):
    k = int(round(top / h)); H = np.zeros((k, k))
    for i in idx:
        j = i + 1
        while j < len(u) and u[j] - u[i] < top:
            x = u[j] - u[i]; kk = j + 1
            while kk < len(u) and (u[kk] - u[j]) < top:
                y = u[kk] - u[j]
                if x + y <= top: H[int(x / h), int(y / h)] += 1
                kk += 1
            j += 1
    return H

def expected_grid(fun_list, h=0.1, top=1.0, sub=10):
    """Σ sur les origines de ∫_bin R ; fun_list : liste de fonctions R(x, y) (une par origine)."""
    k = int(round(top / h)); off = (np.arange(sub) + 0.5) / sub * h; E = np.zeros((k, k))
    for a_ in range(k):
        for b_ in range(k):
            Xg, Yg = np.meshgrid(a_ * h + off, b_ * h + off, indexing="ij"); msk = (Xg + Yg) <= top
            if not msk.any(): continue
            E[a_, b_] = sum(float(np.mean(np.where(msk, f(Xg, Yg), 0.0))) for f in fun_list) * h * h
    return E

def main():
    g = np.sort(pd.read_csv(D / "zeta_zeros_1500.csv").t.values); g = g[g > 0]; u = unfold_zeta(g); Ne = neff(g)
    idx = np.nonzero((Ne >= 1.0) & (np.arange(len(g)) < len(g) - 5))[0]
    rep = dict(origines=int(len(idx)), N_eff_min=float(Ne[idx].min()), N_eff_max=float(Ne[idx].max()), N_eff_moyen=float(Ne[idx].mean()))
    # A1 : zone x, y < 0,5
    obs = zone_obs(u, idx); off = (np.arange(40) + 0.5) / 40 * 0.5; Xg, Yg = np.meshgrid(off, off, indexing="ij")
    e_sin = len(idx) * float(np.mean(R3_sinus(Xg, Yg))) * 0.25
    e_neff = sum(float(np.mean(R3N(Xg, Yg, N))) for N in Ne[idx]) * 0.25
    rep["A1"] = dict(observe=obs, attendu_sinus=e_sin, attendu_N_eff=e_neff, proba_poisson_0_N_eff=math.exp(-e_neff), proba_poisson_0_sinus=math.exp(-e_sin))
    # A2 : N unique ajusté sur la zone x + y ≤ 1 (vraisemblance de Poisson par cases de 0,1)
    H = tri_hist(u, idx); n0 = len(idx); best = None; prof = []
    for N in np.arange(1.0, 3.01, 0.05):
        E = expected_grid([lambda x, y, N=N: R3N(x, y, N)], 0.1, 1.0) * n0
        m = E > 0; ll = float(np.sum(H[m] * np.log(np.maximum(E[m], 1e-12)) - E[m])); prof.append((round(float(N), 2), ll))
        if best is None or ll > best[1]: best = (float(N), ll)
    Es = expected_grid([R3_sinus], 0.1, 1.0) * n0; m = Es > 0
    ll_sin = float(np.sum(H[m] * np.log(np.maximum(Es[m], 1e-12)) - Es[m]))
    rep["A2"] = dict(N_ajuste=best[0], logvrais_N=best[1], logvrais_sinus=ll_sin, profil=prof, triplets_zone=int(H.sum()))
    # A3 : paires, marges < 0,1 (écart au plus proche voisin s < s*, m = 1 − sinc²(πs) = 0,1)
    sstar = 0.1866
    gap = np.minimum(np.r_[np.inf, np.diff(u)], np.r_[np.diff(u), np.inf])
    obs_p = int((gap[idx] < sstar).sum())
    ss = (np.arange(200) + 0.5) / 200 * sstar
    e_p_sin = len(idx) * 2 * float(np.mean(1 - sinc(np.pi * ss) ** 2)) * sstar
    e_p_N = lambda N: len(idx) * 2 * float(np.mean(R2N(ss, N))) * sstar
    rep["A3"] = dict(observe=obs_p, attendu_sinus=e_p_sin, attendu_N_eff=sum(2 * float(np.mean(R2N(ss, N))) * sstar for N in Ne[idx]), attendu_N_ajuste=e_p_N(best[0]))
    (D / "rencontre_hauteur.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: v for k, v in rep.items() if k != "A2"}, indent=1, ensure_ascii=False)); print({k: v for k, v in rep["A2"].items() if k != "profil"})

def portees():
    """Triples consécutifs de portée < 1 (écarts dépliés) : ζ, L(χ5), Δ, et contrôle CUE (Mezzadri)."""
    def stats(t, name):
        t = np.sort(t); r = np.arange(1, len(t) + 1); A = np.c_[t * np.log(t), t, np.ones_like(t)]
        u = A @ np.linalg.lstsq(A, r, rcond=None)[0]; w = u[2:] - u[:-2]; gp = np.diff(u)
        return dict(objet=name, zeros=int(len(t)), portee_min=float(w.min()), triples_lt1=int((w < 1).sum()), attendu_sinus=0.014574 * len(w),
                    paires_lt_0_1866=int((gp < 0.1866).sum()), paires_attendu_sinus=float(len(gp) * 0.0118))
    g = pd.read_csv(D / "zeta_zeros_1500.csv").t.values; L = pd.read_csv(D / "L_chi5_zeros_600.csv").t.values
    dz = pd.read_csv(D / "delta_zeros_contour.csv"); col = [c for c in dz.columns if c.lower() in ("t", "gamma")][0]
    rows = [stats(g[g > 0], "zeta (t ≤ 1 500)"), stats(L[L > 0], "L(chi5) (t ≤ 600)"), stats(dz[col].values[dz[col].values > 1], "Delta (t ≤ 1 500)")]
    rng = np.random.default_rng(628); cue = []
    for N, reps in ((20, 4000), (60, 1500)):
        c = tt = 0
        for _ in range(reps):
            Z = (rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))) / np.sqrt(2); Q, R = np.linalg.qr(Z); Q = Q * (np.diag(R) / np.abs(np.diag(R)))
            th = np.sort(np.angle(np.linalg.eigvals(Q))); th = np.r_[th, th[:2] + 2 * np.pi]; u = th * N / (2 * np.pi); w = u[2:] - u[:-2]
            c += (w[:N] < 1).sum(); tt += N
        cue.append(dict(N=N, fraction_triples_lt1=c / tt))
    return rows, cue

if __name__ == "__main__":
    main()
    rows, cue = portees()
    rep = json.loads((D / "rencontre_hauteur.json").read_text(encoding="utf-8-sig")); rep["portees"] = rows; rep["CUE"] = cue
    (D / "rencontre_hauteur.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(rows, indent=1, ensure_ascii=False)); print(cue)
