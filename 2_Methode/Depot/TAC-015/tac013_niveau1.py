"""TAC-013 — niveau 1 de l'échelle : rapports de factorielles (Tchebychev), sans multiplicité.
Prévision enregistrée sur main avant ce script (commit 584a519).
Usage : python -I tac013_niveau1.py  (aucune dépendance ; quelques dizaines de secondes)."""
import math, itertools
from fractions import Fraction

X = 10**6
# --- psi(x) exact par crible
lp = bytearray([1]) * (X + 1); lp[0] = lp[1] = 0
for i in range(2, int(X**.5) + 1):
    if lp[i]: lp[i*i::i] = bytearray(len(range(i*i, X + 1, i)))
lam = [0.0] * (X + 1)
for p in range(2, X + 1):
    if lp[p]:
        q = p
        while q <= X: lam[q] = math.log(p); q *= p
psi = [0.0] * (X + 1); s = 0.0
for n in range(X + 1): s += lam[n]; psi[n] = s

def F(a, y):  # F(y) = sum a_k floor(y/k), y réel >= 0
    return sum(c * math.floor(y / k) for k, c in a.items())

def valide(a):
    """Σ a_k/k = 0, 0 <= F <= 1 sur une période, F = 1 sur [1, c) ; renvoie (c, période) ou None."""
    if sum(Fraction(c, k) for k, c in a.items()) != 0: return None
    L = math.lcm(*a.keys())
    vals = [sum(c * (m // k) for k, c in a.items()) for m in range(L)]   # F constante sur [m, m+1)
    if min(vals) < 0 or max(vals) > 1 or vals[1] != 1: return None
    c = 1
    while c < L and vals[c] == 1: c += 1
    return c, L, vals

def constante(a, c):
    A = -sum(cf * math.log(k) / k for k, cf in a.items())
    return A, A * c / (c - 1)

def limite_gaspillage(a, c, L, vals):
    """∫_c^∞ F(y) dy / y² , F constante par morceaux de période L (somme exacte sur 10⁴ périodes + queue moyenne)."""
    tot = 0.0; M = 10**4 * L
    for m in range(c, M):
        v = vals[m % L]
        if v: tot += v * (1 / m - 1 / (m + 1))
    return tot + (sum(vals) / L) / M

def log_N(a, x):
    return sum(c * math.lgamma(x // k + 1) for k, c in a.items())

def mesures(nom, a):
    c, L, vals = valide(a)
    A, K = constante(a, c)
    lim = limite_gaspillage(a, c, L, vals)
    print(f"\n== {nom}  poids {dict(sorted(a.items()))}  c = {c}  A = {A:.5f}  constante psi(x) <= {K:.4f} x  limite W/x = {lim:.4f}")
    for x in (10**4, 10**5, 10**6):
        lN = log_N(a, x); W = lN - (psi[x] - psi[x // c])
        exc = 'EXCEPTION' if psi[x] - psi[x // c] > lN + 1e-6 else 'ok'
        print(f"   x = {x:>7}  W/x = {W/x:.4f}  écart à la limite = {abs(W/x-lim):.4f}  W/sqrt(x) = {W/math.sqrt(x):8.1f}  borne {exc}")
    return dict(nom=nom, c=c, A=A, K=K, lim=lim)

R = []
R.append(mesures("C(2n, n)", {1: 1, 2: -2}))
R.append(mesures("Tchebychev 1852", {1: 1, 2: -1, 3: -1, 5: -1, 30: 1}))

# --- P3 : recherche exhaustive sur les diviseurs composés de 210
div = [d for d in range(1, 211) if 210 % d == 0]
comp = [d for d in div if d not in (1, 2, 3, 5, 7)]
base = {1: 1, 2: -1, 3: -1, 5: -1, 7: -1}
trouves = []
for choix in itertools.product((-1, 0, 1), repeat=len(comp)):
    a = dict(base); a.update({d: e for d, e in zip(comp, choix) if e})
    v = valide(a)
    if v: trouves.append((constante(a, v[0])[1], v[0], a))
trouves.sort(key=lambda t: t[0])
print(f"\n== P3 : {len(trouves)} fonctions F valides parmi 3^{len(comp)} = {3**len(comp)} essais")
for K, c, a in trouves[:5]: print(f"   constante {K:.4f}  c = {c}  poids {dict(sorted(a.items()))}")
if trouves:
    R.append(mesures("meilleure trouvée (diviseurs de 210)", trouves[0][2]))
