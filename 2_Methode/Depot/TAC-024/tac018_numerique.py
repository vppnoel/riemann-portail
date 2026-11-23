"""TAC-018, P4 : la statistique en rampe de la Loupe double.
c(n) = (Λ∗Λ)(n) − Λ(n) log n + 2γΛ(n)  (article 1) ;  H(y) = Σ_{n≤y} c(n)(y/n − 1) − G_c(1)·y,
G_c(1) = 2γ² + 6γ₁ (développement de q = −ζ′/ζ en s = 1 : q = 1/t − γ + (γ² + 2γ₁)t + …).
Sur [n, n + 1), H est affine : ses extrêmes sont aux bords (on évalue en n et en (n + 1)⁻).
Usage : python -I tac018_numerique.py [N]  (défaut 10⁶ ; environ 30 s)."""
import math, sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 10**6
g = 0.57721566490153286061; g1 = -0.07281584548367672486
Gc1 = 2 * g * g + 6 * g1; kappa = 2 + g - math.log(4 * math.pi)
lp = bytearray([1]) * (N + 1); lp[0] = lp[1] = 0
for i in range(2, int(N**.5) + 1):
    if lp[i]: lp[i*i::i] = bytearray(len(range(i*i, N + 1, i)))
lam = [0.0] * (N + 1); pp = []
for p in range(2, N + 1):
    if lp[p]:
        q = p; l = math.log(p)
        while q <= N: lam[q] = l; pp.append(q); q *= p
pp.sort()
c = [0.0] * (N + 1)
for i, d in enumerate(pp):                       # (Λ∗Λ)(n) = Σ_{de = n} Λ(d)Λ(e), d et e puissances de premiers
    if d * d > N: break
    for e in pp:
        n = d * e
        if n > N: break
        c[n] += lam[d] * lam[e] * (1 if e == d else (2 if e > d else 0))
for n in range(2, N + 1):
    if lam[n]: c[n] += -lam[n] * math.log(n) + 2 * g * lam[n]
S1 = S0 = 0.0; k1 = k0 = 0.0
best = (0.0, 0); dec = {}; drift = {}
for n in range(1, N):
    t = c[n] / n - k1; u = S1 + t; k1 = (u - S1) - t; S1 = u
    t = c[n] - k0; u = S0 + t; k0 = (u - S0) - t; S0 = u
    if n < 10: continue
    for y in (float(n), n + 1 - 1e-9):
        H = y * S1 - S0 - Gc1 * y
        r = abs(H) / (math.sqrt(y) * math.log(y))
        if r > best[0]: best = (r, y)
        d = int(math.log10(y))
        if r > dec.get(d, (0,))[0]: dec[d] = (r, y)
    if n in (10**3, 10**4, 10**5, 10**6 - 1): drift[n] = (n * S1 - S0 - Gc1 * n) / n
print(f"N = {N} ; G_c(1) = 2γ² + 6γ₁ = {Gc1:.6f} ; 2κ = {2*kappa:.6f}")
print(f"max |H(y)|/(√y log y) sur [10, {N}] = {best[0]:.5f} en y ≈ {best[1]:.0f}")
for d in sorted(dec): print(f"  décade 10^{d} : max {dec[d][0]:.5f} en y ≈ {dec[d][1]:.0f}")
print("dérive H(y)/y (doit tendre vers 0) :", {k: f"{v:.2e}" for k, v in drift.items()})
