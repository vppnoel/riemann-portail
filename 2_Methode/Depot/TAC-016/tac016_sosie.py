"""TAC-016 — le Sosie (Davenport–Heilbronn) face aux étapes 1 et 2 de l'échelle.
Prévision enregistrée sur main avant ce script (commit b371f4a).
F(s) = Σ a(n) n^(−s), a(n) = 1, κ, −κ, −1, 0 selon n mod 5 (src/family_mod5.py, src/rejection.py).
−F′/F = Σ b(n) n^(−s), b = (a·log) ∗ a^(−1). Écriture b(n) = Σ_p β(n, p) log p, β(n, p) = Σ_{d|n} v_p(d) a(d) c(n/d), c = a^(−1).
Arithmétique exacte dans Z[κ] modulo κ⁴ + 2κ³ − 6κ² − 2κ + 1 (polynôme minimal de κ, établi à la main, vérifié ici).
Usage : python -I tac016_sosie.py   (sans dépendance ; environ une minute)."""
import math
KAPPA = (math.sqrt(10 - 2 * math.sqrt(5)) - 2) / (math.sqrt(5) - 1)
MIN = (1, 2, -6, -2, 1)                                   # x⁴ + 2x³ − 6x² − 2x + 1, coefficients de haut en bas
print(f"κ = {KAPPA:.15f} ; valeur du polynôme minimal en κ : {sum(c * KAPPA**(4-i) for i, c in enumerate(MIN)):.2e}")
print("racines rationnelles possibles ±1 :", [sum(c * r**(4-i) for i, c in enumerate(MIN)) for r in (1, -1)],
      "; κ − 1/κ =", round(KAPPA - 1/KAPPA, 12), "= −1 − √5 =", round(-1 - math.sqrt(5), 12), "→ irréductible sur Q (voir RAPPORT)")

# --- éléments de Z[κ] : tuples de 4 entiers (c0, c1, c2, c3) pour c0 + c1 κ + c2 κ² + c3 κ³
Z = (0, 0, 0, 0); ONE = (1, 0, 0, 0); K = (0, 1, 0, 0)
def add(x, y): return tuple(a + b for a, b in zip(x, y))
def neg(x): return tuple(-a for a in x)
def mul(x, y):
    r = [0] * 7
    for i, a in enumerate(x):
        if a:
            for j, b in enumerate(y):
                if b: r[i + j] += a * b
    for d in (6, 5, 4):                                   # κ⁴ = −2κ³ + 6κ² + 2κ − 1
        t = r[d]; r[d] = 0
        if t: r[d-1] += -2 * t; r[d-2] += 6 * t; r[d-3] += 2 * t; r[d-4] += -t
    return tuple(r[:4])
def val(x): return sum(c * KAPPA**i for i, c in enumerate(x))
def rationnel(x): return x[1] == x[2] == x[3] == 0
A = {0: Z, 1: ONE, 2: K, 3: neg(K), 4: neg(ONE)}
def a(n): return A[n % 5]

# --- P1 et P3 : exact jusqu'à NE
NE = 3000
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
def bval(n): return sum(val(beta[(n, p)]) * math.log(p) for p in fact(n) if (n, p) in beta)
ppow = lambda n: len(fact(n)) == 1
neg_n = [n for n in range(2, 31) if bval(n) < -1e-12]
hors = [n for n in range(2, 31) if not ppow(n) and abs(bval(n)) > 1e-12]
print(f"\nP1 : n ≤ 30 avec b(n) < 0 : {neg_n}")
print(f"P1 : n ≤ 30 non puissances de premiers avec b(n) ≠ 0 : {hors} ; premier : {hors[0] if hors else None}")
print("     b(2) =", beta.get((2, 2)), "· log 2  (coefficients en base 1, κ, κ², κ³)")
nb_nonrat = sum(1 for v in beta.values() if not rationnel(v))
print(f"P3 : sur {len(beta)} coefficients β(n, p) non nuls, n ≤ {NE} : {nb_nonrat} ne sont pas rationnels")
# P3, version « sac » : α_p(x) = Σ_{n ≤ x, p | n} β(n, p) F(x/n) pour le rapport de Tchebychev
W = {1: 1, 2: -1, 3: -1, 5: -1, 30: 1}
def Fc(t): return sum(w * math.floor(t / k + 1e-12) for k, w in W.items())
def alpha(x, p):
    s = Z
    for n in range(p, x + 1, p):
        if (n, p) in beta:
            f = Fc(x / n)
            if f: s = add(s, mul((f, 0, 0, 0), beta[(n, p)]))
    return s
tests = [(x, p) for x in (60, 300, 1000, 3000) for p in (2, 3, 7)]
nr = [(x, p) for x, p in tests if not rationnel(alpha(x, p))]
print(f"P3 : exposant α_p(x) du « sac » de Tchebychev pour DH, {len(tests)} cas (x ∈ {{60, 300, 1000, 3000}}, p ∈ {{2, 3, 7}}) : {len(nr)} irrationnels")
# témoin ζ : a = 1 → c = μ, β(n, p) = 1 si n est une puissance de p, 0 sinon
print("témoin ζ : β(n, p) = [n puissance de p] (Λ = log p) : α_p entier, le sac existe ; vérifié par construction")

# --- P2 : non-annulation pour Re s ≥ 2 et abscisse de convergence absolue de 1/F
def tail(sig, N=200000): return sum(abs(val(a(n))) * n**(-sig) for n in range(2, N)) + 0.6 * N**(1 - sig) / (sig - 1)
print(f"\nP2 : Σ_(n≥2) |a(n)| n^(−2) ≈ {tail(2.0):.5f}  (< 1 ⇒ F ≠ 0 et 1/F absolument convergente pour Re s ≥ 2)")
lo, hi = 1.05, 3.0
for _ in range(40):
    mid = (lo + hi) / 2
    if tail(mid, 20000) > 1: lo = mid
    else: hi = mid
print(f"P2 : Σ_(n≥2) |a(n)| n^(−σ) = 1 pour σ* ≈ {hi:.3f} : 1/F et −F′/F convergent absolument pour Re s > {hi:.3f}")

# --- P4 et croissance : flottants jusqu'à NF
NF = 10**5
af = [0.0] + [val(a(n)) for n in range(1, NF + 1)]
cf = [0.0] * (NF + 1); cf[1] = 1.0
for n in range(1, NF + 1):
    if n > 1: cf[n] = -cf[n]
    for m in range(2 * n, NF + 1, n): cf[m] += af[m // n] * cf[n]   # c(m) = −Σ_{d|m, d>1} a(d) c(m/d)
bf = [0.0] * (NF + 1)
for d in range(2, NF + 1):
    ad = af[d] * math.log(d)
    if ad:
        for m in range(d, NF + 1, d): bf[m] += ad * cf[m // d]
for n in (2, 3, 6, 10, 30, 1000):
    if n <= NE: assert abs(bf[n] - bval(n)) < 1e-6 * max(1, abs(bf[n])), (n, bf[n], bval(n))
print(f"\ncontrôle : b(n) flottant = b(n) exact pour n ∈ {{2, 3, 6, 10, 30, 1000}}")
# F(1) et F′(1) par sommes partielles moyennées sur une période
def F1():
    Nm = 10**6; s0 = s1 = 0.0; acc0 = []; acc1 = []
    for n in range(1, Nm + 6):
        v = val(a(n))
        if v: s0 += v / n; s1 -= v * math.log(n) / n
        if n > Nm: acc0.append(s0); acc1.append(s1)
    return sum(acc0) / 5, sum(acc1) / 5
f1, fp1 = F1(); LD1 = fp1 / f1
print(f"F(1) ≈ {f1:.8f} ; F′(1) ≈ {fp1:.8f} ; F′/F(1) ≈ {LD1:.8f}")
S1 = S0 = 0.0; mr = 0.0; my = None; mg2 = 0.0; marks = {}
for y in range(2, NF + 1):
    S1 += bf[y] / y; S0 += bf[y]
    G = y * S1 - S0 + y * LD1                             # Σ b(n)(y/n − 1) + y F′/F(1), à une constante bornée près
    r = abs(G) / math.sqrt(y)
    if r > mr: mr, my = r, y
    mg2 = max(mg2, abs(G) / y**2)
    for t in (10**3, 10**4, 10**5):
        if y == t: marks[t] = (r, mr)
print(f"P4 : max |G_DH(y)|/√y sur [2, {NF}] = {mr:.3f} (en y = {my}) ; ζ : 0,0227")
for t, (r, m) in sorted(marks.items()): print(f"     y = {t:>6} : |G_DH|/√y = {r:.3f} ; max jusque-là {m:.3f}")
print(f"P2 : max |G_DH(y)|/y² sur [2, {NF}] = {mg2:.3e} (croissance PoleData : |G| ≤ C y²)")
