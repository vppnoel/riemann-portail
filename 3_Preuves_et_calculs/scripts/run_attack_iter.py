#!/usr/bin/env python3
"""v5.4 — Attaque 2, mode itératif. Chaque appel :
  1) prolonge la Gram de Nyman–Beurling sur les entiers sans carré <= NMAX pendant `budget` secondes (reprenable) ;
  2) analyse le plus grand bloc complet (N_ok) ;
  3) ajoute les nouveaux N à data/attack_iter_results.csv et réécrit preuves/ATTAQUE_JOURNAL.md ;
  4) copie journal et CSV vers /mnt/user-data/outputs (sauvegarde au fur et à mesure).
Usage : python run_attack_iter.py [budget_s] [NMAX]
"""
from pathlib import Path
import sys, math, time, shutil, datetime
import numpy as np, pandas as pd
import scipy.linalg as sla
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import nyman_beurling as nb
from rh_core import KAPPA, EULER_GAMMA as g, mobius_sieve
nb.Y_TARGET = 1e5
budget = float(sys.argv[1]) if len(sys.argv) > 1 else 200.0
NMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
mu = mobius_sieve(NMAX); sf = [n for n in range(1, NMAX + 1) if mu[n] != 0]
D = ROOT / "data"; path = D / f"nb_gram_sqfree{NMAX}.npy"
# ---- 1. construction (amorçage depuis le plus grand fichier plus petit)
if path.exists():
    M = np.load(path)
else:
    M = np.full((len(sf), len(sf)), np.nan)
    for prev in (500, 200):
        pp = D / f"nb_gram_sqfree{prev}.npy"
        if pp.exists():
            old = np.load(pp); k = old.shape[0]; M[:k, :k] = old; break
t0 = time.time(); done = 0; stopped = False
for j in range(len(sf)):
    if np.isnan(M[:j + 1, j]).any():
        for i in range(j + 1):
            if np.isnan(M[i, j]):
                if time.time() - t0 > budget: stopped = True; break
                M[i, j] = M[j, i] = nb.G(sf[i], sf[j]); done += 1
        if stopped: break
np.save(path, M)
J = 0
while J < len(sf) and not np.isnan(M[:J + 1, :J + 1]).any(): J += 1
N_ok = sf[J - 1]
remaining = int(np.isnan(np.triu(M)).sum())
# ---- 2. analyse
def setup(N):
    ns = [n for n in sf if n <= N]; k = len(ns); Gm = M[:k, :k]
    nn = np.array(ns, float); m = np.array([mu[n] for n in ns], float); L = np.log(nn)
    b = np.array([nb.chi_rho(n) for n in ns]); return ns, nn, m, L, Gm, b
def proj(V, Gm, b):
    Gam = V @ Gm @ V.T; bb = V @ b; beta = np.linalg.lstsq(Gam, -bb, rcond=None)[0]
    return float(1 + 2 * beta @ bb + beta @ Gam @ beta), beta
res_path = D / "attack_iter_results.csv"
old = pd.read_csv(res_path) if res_path.exists() else pd.DataFrame()
have = set(old["N"].astype(int)) if len(old) else set()
grid = [N for N in list(range(50, 501, 50)) + list(range(600, NMAX + 1, 100)) + ([N_ok] if remaining == 0 else []) if N <= N_ok and N not in have]
rows = []
for N in grid:
    ns, nn, m, L, Gm, b = setup(N); lN = math.log(N); x = L / lN
    r = dict(N=N, n_sansCarre=len(ns))
    r["mu_fixe"] = float(1 + 2 * m @ b + m @ Gm @ m)
    a = m * (L ** 2 - 2 * g * L)
    r["mu_a"], be = proj(np.vstack([m, a]), Gm, b); r["alpha"] = float(be[0]); r["beta_log2N"] = float(be[1] * lN ** 2)
    r["mu_log"], _ = proj(np.vstack([m, m * L]), Gm, b)
    r["mu_log2"], _ = proj(np.vstack([m, m * L ** 2]), Gm, b)
    r["poly_x_deg3"], _ = proj(np.vstack([m * x ** k for k in range(4)]), Gm, b)
    r["poly_x_deg5"], _ = proj(np.vstack([m * x ** k for k in range(6)]), Gm, b)
    r["bord_1mx_deg2"], _ = proj(np.vstack([m * (1 - x) * x ** k for k in range(3)]), Gm, b)
    r["bord_1mx2_deg2"], _ = proj(np.vstack([m * (1 - x) ** 2 * x ** k for k in range(3)]), Gm, b)
    try:
        c = -sla.solve(Gm, b, assume_a="pos")
    except Exception:
        c = -np.linalg.lstsq(Gm, b, rcond=None)[0]
    r["opt_sansCarre"] = float(1 + b @ c); r["cond_G"] = float(np.linalg.cond(Gm))
    r["accord_signe_mu"] = float(np.mean(np.sign(c) == m))
    y = c * m; X = np.vstack([x ** k for k in range(4)]).T; coef = np.linalg.lstsq(X, y, rcond=None)[0]
    r["R2_profil_deg3"] = float(1 - np.sum((y - X @ coef) ** 2) / np.sum((y - y.mean()) ** 2))
    r["profil_P"] = " ".join(f"{v:+.2f}" for v in coef)
    for k in ("mu_fixe", "mu_a", "mu_log", "mu_log2", "poly_x_deg3", "poly_x_deg5", "bord_1mx_deg2", "bord_1mx2_deg2", "opt_sansCarre"):
        r[k + "_rk"] = r[k] * lN / KAPPA
    r["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    rows.append(r)
allres = pd.concat([old, pd.DataFrame(rows)], ignore_index=True) if rows else old
if len(allres): allres = allres.sort_values("N"); allres.to_csv(res_path, index=False)
# ---- 3. journal
J_md = ROOT / "preuves" / "ATTAQUE_JOURNAL.md"
log = J_md.read_text(encoding="utf-8-sig") if J_md.exists() else ("# Journal de l'attaque 2 (projection de Nyman–Beurling) — v5.4\n\n"
      "Chaque itération prolonge la Gram sans carré et analyse le plus grand bloc complet. Colonnes « × κ/log N » = e²·log N/κ "
      "(1 = constante de Burnol–BCF). Aucune ligne de ce journal n'est une preuve.\n\n## Itérations\n")
log += (f"\n- **{datetime.datetime.now():%Y-%m-%d %H:%M}** — NMAX={NMAX}, entrées calculées ce tour : {done}, restantes : {remaining}, "
        f"bloc complet jusqu'à N = {N_ok}, nouveaux N analysés : {grid if grid else 'aucun'}")
J_md.write_text(log, encoding="utf-8")
tab = allres[["N", "mu_a_rk", "mu_log2_rk", "poly_x_deg3_rk", "poly_x_deg5_rk", "bord_1mx_deg2_rk", "opt_sansCarre_rk", "beta_log2N", "R2_profil_deg3"]].copy() if len(allres) else None
summ = ROOT / "preuves" / "ATTAQUE_RESULTATS_COURANTS.md"
if tab is not None:
    lines = ["# Résultats courants de l'attaque 2 (mis à jour à chaque itération)\n", f"Dernière mise à jour : {datetime.datetime.now():%Y-%m-%d %H:%M} ; bloc complet jusqu'à N = {N_ok}.\n",
             "| N | {μ,a} | {μ,μlog²} | poly x deg 3 | poly x deg 5 | bord (1−x) | optimum sans carré | β·log²N | R² profil |", "|---|---|---|---|---|---|---|---|---|"]
    for _, t in tab.iterrows():
        lines.append(f"| {int(t.N)} | {t.mu_a_rk:.3f} | {t.mu_log2_rk:.3f} | {t.poly_x_deg3_rk:.3f} | {t.poly_x_deg5_rk:.3f} | {t.bord_1mx_deg2_rk:.3f} | {t.opt_sansCarre_rk:.3f} | {t.beta_log2N:.3f} | {t.R2_profil_deg3:.3f} |")
    lines.append("\nValeurs = e²·log N/κ (sauf les deux dernières colonnes). Données complètes : `data/attack_iter_results.csv`.")
    summ.write_text("\n".join(lines), encoding="utf-8")
# ---- 4. sauvegarde au fur et à mesure
out = Path("/mnt/user-data/outputs/attaque_en_cours"); out.mkdir(parents=True, exist_ok=True)
for f in (J_md, summ, res_path):
    if f.exists(): shutil.copy(f, out / f.name)
print(f"NMAX={NMAX} | calculées {done} | restantes {remaining} | bloc complet N={N_ok} | nouveaux N {grid}")
if tab is not None: print(tab.round(3).to_string(index=False))
