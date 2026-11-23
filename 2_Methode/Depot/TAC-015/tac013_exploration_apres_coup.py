"""TAC-013 — EXPLORATION APRÈS COUP (non prévue). La prévision P3 (base a_2=a_3=a_5=a_7=−1) a échoué : 0 F valide.
Ici : poids a_k ∈ {−1,0,1} sur tous les diviseurs de 210 (a_1 = 1), sans base imposée. Résultat à lire comme exploratoire."""
import math, itertools
div = [d for d in range(2, 211) if 210 % d == 0]
L = 210
best = []; nval = 0
for ch in itertools.product((-1, 0, 1), repeat=len(div)):
    if 210 + sum(e * (210 // d) for d, e in zip(div, ch)) != 0: continue      # Σ a_k/k = 0
    a = {1: 1}; a.update({d: e for d, e in zip(div, ch) if e})
    vals = [sum(c * (m // k) for k, c in a.items()) for m in range(L)]
    if min(vals) < 0 or max(vals) > 1 or vals[1] != 1: continue
    nval += 1
    c = 1
    while c < L and vals[c] == 1: c += 1
    A = -sum(cf * math.log(k) / k for k, cf in a.items())
    best.append((A * c / (c - 1), c, A, A - 1 + 1 / c, dict(sorted(a.items()))))
best.sort()
print(f"{nval} fonctions F valides (poids ±1 sur les diviseurs de 210)")
for K, c, A, w, a in best[:6]:
    print(f"  constante {K:.4f}  c = {c}  A = {A:.5f}  gaspillage limite W/x = A − 1 + 1/c = {w:.4f}  poids {a}")
