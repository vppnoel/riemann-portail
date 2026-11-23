"""TAC-016, reprise (vérification #39) : (1) P3 reformulée, (2) témoin quartique L(s, χ₅), (3) critère commun.
Critère commun proposé à la reprise (définition de Claude, pas du guide) :
  (S) il existe une famille finie naturelle F₁, …, F_r et des poids > 0 tels que les coefficients de
      Σ w_j (−F_j′/F_j) soient de la forme Σ_p e(n, p) log p avec e(n, p) entiers ≥ 0, nuls hors des puissances de p.
  Familles testées : ζ seule ; les 4 puissances de χ₅ (χ₅(2) = i) ; les 4 conjugués de Galois de DH
  (κ ↦ ses 4 racines). Pour DH, la somme sur les conjugués de −F^σ′/F^σ est −N′/N, où N = Π_σ F^σ est la norme :
  ses coefficients sont les traces Tr β(n, p), entières puisque β ∈ Z[κ] et que κ est un entier algébrique.
Usage : python -I tac016_reprise.py   (sans dépendance)."""
import math, cmath
NE = 3000
MIN_E = (-2, -6, 2, 1)                       # e1, e2, e3, e4 de x⁴ + 2x³ − 6x² − 2x + 1
TR = (4, -2, 16, -38)                        # traces de 1, κ, κ², κ³ (identités de Newton)
Z = (0, 0, 0, 0); ONE = (1, 0, 0, 0); K = (0, 1, 0, 0)
def add(x, y): return tuple(a + b for a, b in zip(x, y))
def neg(x): return tuple(-a for a in x)
def mul(x, y):
    r = [0] * 7
    for i, a in enumerate(x):
        if a:
            for j, b in enumerate(y):
                if b: r[i + j] += a * b
    for d in (6, 5, 4):
        t = r[d]; r[d] = 0
        if t: r[d-1] += -2 * t; r[d-2] += 6 * t; r[d-3] += 2 * t; r[d-4] += -t
    return tuple(r[:4])
def tr(x): return sum(c * t for c, t in zip(x, TR))
def rat(x): return x[1] == x[2] == x[3] == 0
KAP = (math.sqrt(10 - 2 * math.sqrt(5)) - 2) / (math.sqrt(5) - 1)
# contrôle des traces par les racines numériques (Durand–Kerner)
rts = [complex(0.4, 0.9) ** k for k in range(4)]
for _ in range(500):
    rts = [r - (r**4 + 2*r**3 - 6*r**2 - 2*r + 1) / math.prod(r - q for q in rts if q is not r) for r in rts]
print("traces numériques de κ^j :", [round(sum(r**j for r in rts).real, 9) for j in range(4)], "attendu", TR)
print("racines :", sorted(round(r.real, 6) for r in rts), "; κ =", round(KAP, 6))
A = {0: Z, 1: ONE, 2: K, 3: neg(K), 4: neg(ONE)}
def a(n): return A[n % 5]
divs = [[] for _ in range(NE + 1)]
for d in range(1, NE + 1):
    for m in range(d, NE + 1, d): divs[m].append(d)
c = [Z] * (NE + 1); c[1] = ONE
for n in range(2, NE + 1):
    s = Z
    for d in divs[n]:
        if d > 1: s = add(s, mul(a(d), c[n // d]))
    c[n] = neg(s)
def fact(n):
    f = {}; p = 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def vp(n, p):
    k = 0
    while n % p == 0: n //= p; k += 1
    return k
beta = {}
for n in range(2, NE + 1):
    for p in fact(n):
        s = Z
        for d in divs[n]:
            v = vp(d, p)
            if v: s = add(s, mul((v, 0, 0, 0), mul(a(d), c[n // d])))
        if s != Z: beta[(n, p)] = s
# (1) P3 reformulée : pour chaque x, existe-t-il un p avec α_p(x) irrationnel ? combien d'exposants rationnels ?
W = {"Tchebychev": {1: 1, 2: -1, 3: -1, 5: -1, 30: 1}, "binomial": {1: 1, 2: -2}}
for nom, w in W.items():
    def Fc(t): return sum(v * math.floor(t / k + 1e-12) for k, v in w.items())
    sans = []; nrat = ntot = 0
    for x in range(2, NE + 1):
        alph = {}
        for (n, p), b in beta.items():
            if n <= x:
                f = Fc(x / n)
                if f: alph[p] = add(alph.get(p, Z), mul((f, 0, 0, 0), b))
        alph = {p: v for p, v in alph.items() if v != Z}
        ntot += len(alph); nrat += sum(1 for v in alph.values() if rat(v))
        if alph and all(rat(v) for v in alph.values()): sans.append(x)
        if not alph: sans.append(x)
    print(f"(1) {nom} : x ∈ [2, {NE}] sans aucun exposant irrationnel : {len(sans)} {sans[:10]} ; exposants rationnels non nuls : {nrat} sur {ntot}")
# (2) et (3) : critère (S)
def check_zeta(): return True
# χ₅ : b(n) = Λ(n) χ(n) ; famille des 4 puissances, poids égaux : Σ_j χ^j(p^r) = 4·[χ(p)^r = 1]
chi = {0: 0, 1: 1, 2: 1j, 3: -1j, 4: -1}
bad_chi = 0
for n in range(2, NE + 1):
    f = fact(n)
    if len(f) != 1: continue
    (p, r), = f.items()
    e = sum((chi[p % 5] ** r) ** j if p % 5 else (1 if j == 0 else 0) for j in range(4))
    if abs(e.imag) > 1e-12 or e.real < -1e-12 or abs(e.real - round(e.real)) > 1e-12: bad_chi += 1
print(f"(2) L(s, χ₅) seul, x = 2 : exposant brut de 2 = χ₅(2)·F(1) = i (non entier) → échec du test naïf")
print(f"(2) famille des 4 puissances de χ₅ : exposants Σ_j χ^j(p^r) ∈ {{0, 4}} (p ∤ 5) ou {{1}} (p = 5, caractère trivial seul) ; cas non entiers ou négatifs : {bad_chi} → (S) satisfait")
# DH : famille des 4 conjugués de Galois → coefficients Tr β(n, p)
neg_n = sorted({n for (n, p), b in beta.items() if tr(b) < 0})
off = sorted({n for (n, p), b in beta.items() if tr(b) != 0 and len(fact(n)) > 1})
print(f"(3) DH, famille des 4 conjugués : Tr β(n, p) entiers ; négatifs pour {len(neg_n)} valeurs de n ≤ {NE} (premiers : {neg_n[:8]}) ; non nuls hors des puissances de premiers pour {len(off)} valeurs (premiers : {off[:8]})")
print("    exemples : Tr β(2, 2) =", tr(beta[(2, 2)]), "; Tr β(6, 2) =", tr(beta[(6, 2)]), "; Tr β(6, 3) =", tr(beta[(6, 3)]), "→ (S) non satisfait pour cette famille")
