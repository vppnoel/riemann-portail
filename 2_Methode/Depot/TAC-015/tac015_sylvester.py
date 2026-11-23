"""TAC-015, reprise : le schéma ν₈ de Sylvester (1892), troisième exemple demandé par la vérification.
Poids (d'après l'exposé arXiv:2512.02466, qui l'attribue à Sylvester, Messenger Math. 21 (1892)) :
+1 en 1, 6, 10, 14, 105 ; −1 en 2, 3, 5, 7, 11, 13, 385, 1001.
On calcule : Σ ν(k)/k, la période, les valeurs prises par F(y) = Σ ν(k)⌊y/k⌋, le premier c où F quitte 1,
A = −Σ ν(k) log k / k, la limite A − 1 + 1/c du « gaspillage » W(x)/x et sa mesure jusqu'à 10⁶.
Différence avec les deux autres rapports : F prend des valeurs négatives, donc N_F(x) = Π ⌊x/k⌋!^ν(k) n'est pas un entier.
Usage : python -I tac015_sylvester.py   (sans dépendance ; quelques secondes)."""
import math
from fractions import Fraction
NU = {1: 1, 6: 1, 10: 1, 14: 1, 105: 1, 2: -1, 3: -1, 5: -1, 7: -1, 11: -1, 13: -1, 385: -1, 1001: -1}
print("Σ ν(k)/k =", sum(Fraction(v, k) for k, v in NU.items()))
L = math.lcm(*NU)
vals = [sum(v * (m // k) for k, v in NU.items()) for m in range(L)]
print(f"période {L} ; valeurs de F sur une période : min {min(vals)}, max {max(vals)} ; F < 0 sur {sum(1 for x in vals if x < 0)} des {L} pas")
c = 1
while vals[c] == 1: c += 1
print(f"F = 1 sur [1, {c}), F({c}) = {vals[c]}")
A = -sum(v * math.log(k) / k for k, v in NU.items())
lim = A - 1 + 1 / c
print(f"A = {A:.6f} ; constante naïve A·c/(c−1) = {A*c/(c-1):.5f} (sans sens si F change de signe) ; limite W/x = A − 1 + 1/c = {lim:.6f}")
# vérification par somme directe de ∫_c^∞ F(y) dy / y² sur 30 périodes + queue moyenne
M = 30 * L; tot = sum(vals[m % L] * (1 / m - 1 / (m + 1)) for m in range(c, M)) + (sum(vals) / L) / M
print(f"∫_c^∞ F/y² (30 périodes + queue) = {tot:.6f}")
X = 10**6
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
for x in (10**4, 10**5, 10**6):
    lN = sum(v * math.lgamma(x // k + 1) for k, v in NU.items())
    W = lN - (psi[x] - psi[x // c])
    print(f"x = {x:>7} : log N_F(x)/x = {lN/x:.5f} ; W/x = {W/x:.5f} ; écart à la limite {abs(W/x-lim):.5f} ; W/√x = {W/math.sqrt(x):.1f}")
