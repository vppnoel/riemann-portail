"""V6.23 — Axe J5 : le Frobenius qui n'est pas un morphisme.

Prévisions écrites avant le calcul : data/prevision_v623_frobenius.md (22 h 12 UTC).
La construction de Stepanov faite pour de vrai, en algèbre linéaire sur F_p, pour y² = f(x) :
S = {x ∈ F_p : f(x) carré non nul}, g = f^{(p−1)/2} (g = 1 sur S),
A(x) = Σ_{j<J} Σ_{a<K} (r_{ja} x^a + s_{ja} x^a g(x)) φ(x)^j, conditions : A^{[k]}(x) = 0 (dérivées de Hasse, k < M) pour x ∈ S.
φ = x^p (Frobenius), φ = x (identité), φ = permutation aléatoire de F_p (polynôme d'interpolation).
Nombre de fonctions auxiliaires = dim(espace engendré) − rang(conditions sur cet espace).
"""
from __future__ import annotations
from pathlib import Path
import json, math, random
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; D = ROOT / "data"

def pmul(a, b, p):
    return np.convolve(a, b) % p

def ppow(a, e, p):
    r = np.array([1], dtype=np.int64); b = a.copy()
    while e:
        if e & 1: r = pmul(r, b, p)
        b = pmul(b, b, p); e >>= 1
    return r

def interp(vals, p):
    """Polynôme (degré < p) qui prend les valeurs vals[x] en x ∈ F_p (Lagrange)."""
    poly = np.zeros(p, dtype=np.int64)
    for x0 in range(p):
        if vals[x0] == 0: continue
        num = np.array([1], dtype=np.int64); den = 1
        for x1 in range(p):
            if x1 != x0: num = pmul(num, np.array([-x1 % p, 1], dtype=np.int64), p); den = den * (x0 - x1) % p
        poly[:len(num)] = (poly[:len(num)] + vals[x0] * pow(den, p - 2, p) * num) % p
    return poly

def rank_mod(Mx, p):
    A = Mx.copy() % p; r = 0; rows, cols = A.shape
    for c in range(cols):
        piv = next((i for i in range(r, rows) if A[i, c]), None)
        if piv is None: continue
        A[[r, piv]] = A[[piv, r]]; A[r] = A[r] * pow(int(A[r, c]), p - 2, p) % p
        nz = np.nonzero(A[:, c])[0]
        for i in nz:
            if i != r: A[i] = (A[i] - A[i, c] * A[r]) % p
        r += 1
        if r == rows: break
    return r

def hasse_eval(poly, xs, M, p):
    """Lignes : pour chaque x ∈ xs et k < M, la valeur de la dérivée de Hasse d'ordre k de poly en x."""
    n = len(poly); i = np.arange(n); out = []
    for x in xs:
        pw = np.array([pow(int(x), int(t), p) for t in range(n)], dtype=np.int64)
        for k in range(M):
            c = np.array([math.comb(int(t), k) % p for t in i], dtype=np.int64)
            sh = np.zeros(n, dtype=np.int64); sh[k:] = pw[:n - k]
            out.append(int(np.sum(c * poly % p * sh % p) % p))
    return out

def experiment(p, f, J, K, M, phis):
    g = ppow(np.array(f, dtype=np.int64), (p - 1) // 2, p)
    fx = [sum(int(c) * pow(x, i, p) for i, c in enumerate(f)) % p for x in range(p)]
    S = [x for x in range(p) if fx[x] and pow(fx[x], (p - 1) // 2, p) == 1]
    res = {}
    for name, phi in phis.items():
        basis = []
        for j in range(J):
            pj = ppow(phi, j, p)
            for a in range(K):
                xa = np.zeros(a + 1, dtype=np.int64); xa[a] = 1
                basis.append(pmul(xa, pj, p)); basis.append(pmul(pmul(xa, g, p), pj, p))
        L = max(len(b) for b in basis)
        B = np.array([np.pad(b, (0, L - len(b))) for b in basis], dtype=np.int64)
        C = np.array([hasse_eval(b, S, M, p) for b in basis], dtype=np.int64).T     # conditions × base
        rB, rC = rank_mod(B, p), rank_mod(C, p)
        res[name] = dict(dim_espace=rB, rang_conditions=rC, fonctions_auxiliaires=rB - rC, degre_max=int(L - 1))
    return dict(p=p, f=f, J=J, K=K, M=M, S=len(S), inconnues=2 * J * K, conditions_naives=M * len(S), **res)

def main():
    rng = random.Random(623); out = []
    for p, f in ((61, [1, 1, 0, 1]), (101, [1, 1, 0, 1])):                      # y² = x³ + x + 1
        perm = list(range(p)); rng.shuffle(perm)
        phis = {"Frobenius x^p": np.array([0] * p + [1], dtype=np.int64), "identité x": np.array([0, 1], dtype=np.int64),
                "permutation aléatoire": interp(perm, p)}
        for M in (2, 3, 4):
            for J in (2, 3):
                S_est = p // 2
                K = max(2, int(math.ceil(M * S_est / (2 * J) * 0.8)))              # 2JK ≈ 0,8 M|S| : moins d'inconnues que de conditions naïves
                r = experiment(p, f, J, K, M, phis); out.append(r)
                print(json.dumps({k: v for k, v in r.items()}, ensure_ascii=False), flush=True)
    (D / "frobenius_non_geometrique.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")

def figure(out):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    R = json.loads((D / "frobenius_non_geometrique.json").read_text(encoding="utf-8-sig"))
    lab = [f"p={r['p']}\nM={r['M']} J={r['J']}" for r in R]; x = np.arange(len(R)); w = 0.27
    fig, ax = plt.subplots(figsize=(12, 4.2))
    for i, (k, col) in enumerate((("Frobenius x^p", "#2b7a57"), ("identité x", "#8c96a4"), ("permutation aléatoire", "#c0392b"))):
        ax.bar(x + (i - 1) * w, [r[k]["fonctions_auxiliaires"] for r in R], w, color=col, label=k)
    ax.set_xticks(x); ax.set_xticklabels(lab, fontsize=8); ax.set_ylabel("fonctions auxiliaires (dimension)")
    ax.set_title("La fonction de Stepanov n'existe qu'avec le Frobenius (même valeurs aux points que l'identité)"); ax.legend()
    fig.tight_layout(); fig.savefig(out, dpi=130); plt.close(fig)

if __name__ == "__main__":
    main(); figure(ROOT.parent / "1_Presentation" / "48_Le_frobenius.png")
