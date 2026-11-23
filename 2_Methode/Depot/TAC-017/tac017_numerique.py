"""TAC-017, P3 (version corrigée lors de la reprise, d'après la vérification #40 §3).
On cherche max |H(y)| / √y sur [10, Y], avec H = G − log 2π et
G(y) = Σ_{n≤y} Λ(n)(y/n − 1) − y(log y − 1 − γ)   (Deduction.G).
Sur [n, n+1) : H(y) = y·Sₙ − Pₙ − y log y + (1+γ)y − log 2π, Sₙ = Σ_{m≤n} Λ(m)/m, Pₙ = ψ(n).
Points critiques de H/√y : 2yH′ − H = 0, soit D(y) = y(Sₙ + γ − 1 − log y) + Pₙ + log 2π = 0.
D′(y) = Sₙ + γ − 2 − log y : D est concave ; on coupe en y_c = exp(Sₙ + γ − 2) si intérieur, puis bissection
sur chaque morceau où D change de signe. On évalue aussi les deux bords exacts de l'intervalle (le bord droit
comme limite à gauche, avec Sₙ, Pₙ). La première version cherchait les zéros de G′, ce qui ne donnait pas le
maximum du rapport (erreur relevée par la vérification) ; la valeur trouvée était néanmoins la bonne.
Usage : python -I tac017_numerique.py [Y]   (défaut Y = 10⁷ ; environ deux minutes)."""
import math, sys
Y = int(sys.argv[1]) if len(sys.argv) > 1 else 10**7
g_e = 0.57721566490153286061; L2P = math.log(2 * math.pi); kappa = 2 + g_e - math.log(4 * math.pi)
lp = bytearray([1]) * (Y + 2); lp[0] = lp[1] = 0
for i in range(2, int((Y + 1)**.5) + 1):
    if lp[i]: lp[i*i::i] = bytearray(len(range(i*i, Y + 2, i)))
lam = {}
for p in range(2, Y + 1):
    if lp[p]:
        q = p; lg = math.log(p)
        while q <= Y: lam[q] = lg; q *= p
def H(y, S, P): return y * S - P - y * math.log(y) + (1 + g_e) * y - L2P
def Dfun(y, S, P): return y * (S + g_e - 1 - math.log(y)) + P + L2P
def roots(a, b, S, P):
    out = []; da, db = Dfun(a, S, P), Dfun(b, S, P)
    if da == 0: out.append(a)
    if da * db < 0:
        lo, hi = a, b
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if Dfun(lo, S, P) * Dfun(mid, S, P) <= 0: hi = mid
            else: lo = mid
        out.append(0.5 * (lo + hi))
    return out
S = 0.0; cS = 0.0; P = 0.0; cP = 0.0
best = (0.0, None, None); bestdec = {}; nroots = 0
for n in range(1, Y):
    l = lam.get(n)
    if l:
        t = l / n - cS; u = S + t; cS = (u - S) - t; S = u
        t = l - cP; u = P + t; cP = (u - P) - t; P = u
    if n < 10: continue
    a, b = float(n), float(n + 1)
    cand = [a, b]
    yc = math.exp(S + g_e - 2)
    parts = [(a, yc), (yc, b)] if a < yc < b else [(a, b)]
    for (x0, x1) in parts:
        r = roots(x0, x1, S, P); nroots += len(r); cand += r
    for y in cand:
        h = H(y, S, P); r = abs(h) / math.sqrt(y)
        if r > best[0]: best = (r, y, h)
        d = min(int(math.log10(y)), 7)
        if r > bestdec.get(d, (0,))[0]: bestdec[d] = (r, y)
print(f"Y = {Y}, kappa = {kappa:.6f}, log 2π = {L2P:.6f} ; points critiques intérieurs trouvés : {nroots}")
print(f"max |G − log 2π|/√y sur [10, {Y}] = {best[0]:.6f}, atteint en y ≈ {best[1]:.4f} (G − log 2π = {best[2]:.4f})")
for d in sorted(bestdec): print(f"  décade [10^{d}, 10^{d+1}) : max = {bestdec[d][0]:.6f} en y ≈ {bestdec[d][1]:.2f}")
print("comparaison : seuil du guide 0,023 ; κ =", round(kappa, 4))
