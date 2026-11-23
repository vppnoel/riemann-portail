# -*- coding: utf-8 -*-
"""TAC-004, partie 1 : symboles des deux filtres, noyaux r_p, données diophantiennes, constantes.

Programme Riemann V6.59. Producteur : ia:claude. Code sous licence MIT (voir LICENSE à la racine).

Conventions (document 76) : U_d g(x) = g(x - d) ; transformée de Laplace G(s) = ∫ g(x) e^{s x} dx ;
moments l_±(f) = F(±1/2) ; B_p = (1+1/p) I - p^{-1/2}(U_{log p} + U_{-log p}) de symbole
b_p(s) = (1 - p^{s-1/2})(1 - p^{-s-1/2}) ; P = ∂² - 1/4 de symbole s² - 1/4.

Ce programme ne calcule aucun zéro de zêta et n'utilise aucune donnée qui contient la réponse.
Tout contrôle est écrit pour pouvoir échouer : chaque assertion compare deux calculs indépendants.
Exécution : python -B p1_bezout_diophantien.py   (numpy, scipy ; bibliothèque standard decimal).
"""
import json
import math
import os
from decimal import Decimal, getcontext

import numpy as np
from scipy import integrate, special

ICI = os.path.dirname(os.path.abspath(__file__))
R = {"programme": "p1_bezout_diophantien.py", "controles": []}


def controle(nom, ok, detail):
    R["controles"].append({"nom": nom, "ok": bool(ok), "detail": detail})
    print(("OK   " if ok else "ECHEC"), nom, "-", detail)
    return ok


# ---------------------------------------------------------------- A. symboles et noyaux
def b(p, s):
    """Symbole de B_p, forme développée."""
    return (1 + 1 / p) - p ** -0.5 * (p ** s + p ** (-s))


def b_fact(p, s):
    """Symbole de B_p, forme factorisée."""
    return (1 - p ** (s - 0.5)) * (1 - p ** (-s - 0.5))


def r(p, x):
    """Noyau r_p à support [-log p, log p] : B_p = P ∘ (r_p *). Formule obtenue à la main (RAPPORT, § 3.1)."""
    L = math.log(p)
    x = np.asarray(x, dtype=float)
    val = (2 / p) * np.cosh(x / 2) - (1 + 1 / p) * np.exp(-np.abs(x) / 2)
    return np.where(np.abs(x) <= L, val, 0.0)


rng = np.random.default_rng(20261018)
S_test = rng.uniform(-3, 3, 12) + 1j * rng.uniform(-40, 40, 12)
for p in (2, 3, 5):
    e = max(abs(b(p, s) - b_fact(p, s)) / (1 + abs(b(p, s))) for s in S_test)
    controle(f"A1 factorisation du symbole b_{p}", e < 1e-12, f"écart relatif max {e:.2e}")

for p in (2, 3):
    L = math.log(p)
    # continuité et nullité aux bords du support
    bord = float(r(p, [L - 1e-12])[0])
    controle(f"A2 r_{p} continu et nul en ±log {p}", abs(bord) < 1e-11, f"r_{p}(log {p}^-) = {bord:.2e}")
    # transformée de Laplace de r_p comparée à b_p(s)/(s²-1/4), par quadrature indépendante
    pire = 0.0
    for s in S_test[:8] / np.array([1, 1, 1, 1, 4, 4, 4, 4]):
        fr = lambda x, part: (r(p, x) * np.exp(s * x)).real if part == 0 else (r(p, x) * np.exp(s * x)).imag
        re = integrate.quad(fr, -L, L, args=(0,), limit=400, epsabs=1e-13, epsrel=1e-13)[0]
        im = integrate.quad(fr, -L, L, args=(1,), limit=400, epsabs=1e-13, epsrel=1e-13)[0]
        cible = b(p, s) / (s * s - 0.25)
        pire = max(pire, abs(re + 1j * im - cible) / (1 + abs(cible)))
    controle(f"A3 Laplace(r_{p}) = b_{p}/(s²-1/4)", pire < 1e-9, f"écart relatif max {pire:.2e} sur 8 points complexes")

# dérivées aux zéros λ = ±1/2 + 2πik/log p (zéros simples, valeurs constantes ∓ log p / 2 · (1 - 1/p)·… )
for p in (2, 3):
    L = math.log(p)
    for sig in (+1, -1):
        for k in (1, 7, -13):
            lam = sig * 0.5 + 2j * math.pi * k / L
            hh = 1e-6
            d = (b(p, lam + hh) - b(p, lam - hh)) / (2 * hh)
            attendu = -sig * L * (1 - 1 / p)
            ok = abs(b(p, lam)) < 1e-12 and abs(d - attendu) < 1e-6
            if not ok:
                break
    controle(f"A4 zéros simples de b_{p}, b_{p}'(±1/2+2πik/log {p}) = ∓(1-1/{p}) log {p}", ok,
             f"dernier écart {abs(d - attendu):.1e}")

# ---------------------------------------------------------------- B. diophantien : θ = log 3 / log 2
getcontext().prec = 120
TH = Decimal(3).ln() / Decimal(2).ln()
th = float(TH)


def fraction_continue(x, n):
    a = []
    for _ in range(n):
        q = int(x)
        a.append(q)
        x = 1 / (x - q)
    return a


A = fraction_continue(TH, 40)
pq = []
p0, q0, p1, q1 = 1, 0, A[0], 1
pq.append((p1, q1))
for a in A[1:]:
    p0, q0, p1, q1 = p1, q1, a * p1 + p0, a * q1 + q0
    pq.append((p1, q1))


def dist_entier(d):
    return abs(d - round(d))


commas = []
for (pp, qq), a_next in zip(pq, A[1:] + [None]):
    if qq < 1:
        continue
    ecart = TH * qq - pp                      # q log2(3) - p, en octaves
    cents = float(ecart * 1200)
    nq = float(abs(ecart))
    commas.append({"k": qq, "l": pp, "rapport": f"3^{qq}/2^{pp}", "cents": cents,
                   "dist_k_theta": nq, "q_fois_dist": qq * nq, "quotient_suivant": a_next})
R["theta"] = str(TH)[:50]
R["fraction_continue"] = A
R["commas"] = commas[:22]

# Balayage k = 1..K : records successifs de ||kθ|| (meilleures approximations) = dénominateurs des réduites
K = 2_000_000
k = np.arange(1, K + 1, dtype=np.float64)
# réduction exacte modulo 1 en deux morceaux pour limiter l'erreur d'arrondi
th_hi = float(TH)
th_lo = float(TH - Decimal(th_hi))
frac = (k * th_hi) % 1.0
frac = (frac + k * th_lo) % 1.0
dk = np.minimum(frac, 1 - frac)
records = []
m = 1.0
for i in np.flatnonzero(dk < np.minimum.accumulate(np.concatenate(([1.0], dk[:-1])))):
    if dk[i] < m:
        m = dk[i]
        records.append(int(i + 1))
denoms = [qq for (_, qq) in pq if 1 <= qq <= K]
controle("B1 records de ||kθ|| = dénominateurs des réduites (k ≤ 2·10^6)",
         records == sorted(set(denoms)) or records == sorted(set(denoms))[1:],
         f"records {records[:14]}… ; réduites {sorted(set(denoms))[:14]}…")
# contrôle haute précision aux records
pire = max(abs(float(abs(TH * q - round(TH * q))) - dk[q - 1]) for q in records)
controle("B2 ||kθ|| en double précision confirmé en précision 120 chiffres aux records", pire < 1e-9, f"écart max {pire:.1e}")

# Exposant empirique : ||kθ|| ≈ k^{-τ}
tau = [math.log(1 / float(abs(TH * q - round(TH * q)))) / math.log(q) for q in records if q >= 5]
R["exposant_empirique_records"] = {"k": [q for q in records if q >= 5], "tau": tau, "tau_max": max(tau)}

# |b_3| aux zéros de b_2 (et symétriquement) : c'est la quantité qui fixe les coefficients de Bézout
def mod_b3_aux_zeros_b2(kk):
    e = np.exp(2j * np.pi * kk * th)
    plus = np.abs(1 - e) * np.abs(1 - np.conj(e) / 3)    # λ = 1/2 + 2πik/log 2
    moins = np.abs(1 - e / 3) * np.abs(1 - np.conj(e))   # λ = -1/2 + 2πik/log 2
    return plus, moins


def mod_b2_aux_zeros_b3(kk):
    e = np.exp(2j * np.pi * kk / th)
    return np.abs(1 - e) * np.abs(1 - np.conj(e) / 2), np.abs(1 - e / 2) * np.abs(1 - np.conj(e))


kk = np.array(records, dtype=float)
p_, m_ = mod_b3_aux_zeros_b2(kk)
lam = 0.5 + 2j * np.pi * kk / math.log(2)
coef = np.abs(lam * lam - 0.25) / p_                     # |v_λ| = |λ²-1/4| / |b_3(λ)|
R["bezout_coefficients_aux_records"] = [
    {"k": int(q), "Im_lambda": float(2 * math.pi * q / math.log(2)), "abs_b3": float(x), "abs_v": float(c),
     "k_fois_abs_b3": float(q * x)} for q, x, c in zip(records, p_, coef)]
# encadrement élémentaire : 4||kθ||·(2/3) ≤ |b_3(λ_k)| ≤ 2π||kθ||·(4/3)
bas = 4 * dk[kk.astype(int) - 1] * (2 / 3)
haut = 2 * math.pi * dk[kk.astype(int) - 1] * (4 / 3)
controle("B3 encadrement |b_3(λ_k)| par ||kθ|| (constantes 8/3 et 8π/3)",
         bool(np.all(bas <= p_ + 1e-15) and np.all(p_ <= haut + 1e-15)),
         "vérifié à tous les records ; c'est le lien commas ↔ coût de Bézout")

# minimum global de |b2|+|b3| sur les droites Re s = ±1/2 hors de ±1/2 : grille + zéros
for sig in (1, -1):
    y = np.linspace(0.5, 4000, 4_000_001)
    s = sig * 0.5 + 1j * y
    v = np.abs(b_fact(2, s)) + np.abs(b_fact(3, s))
    i = int(np.argmin(v))
    R.setdefault("min_somme_sur_droites", []).append({"Re_s": sig * 0.5, "y_argmin": float(y[i]), "min": float(v[i]),
                                                       "y_max": 4000})
controle("B4 aucun zéro commun de b_2, b_3 sur Re s = ±1/2, 0.5 ≤ Im s ≤ 4000 (grille 1e-3)",
         all(d["min"] > 1e-4 for d in R["min_somme_sur_droites"]),
         "; ".join(f"Re={d['Re_s']}: min {d['min']:.3e} en y={d['y_argmin']:.3f}" for d in R["min_somme_sur_droites"]))

# ---------------------------------------------------------------- B'. témoins négatifs (paires commensurables)
# (2,4) : tout zéro de b_2 annule b_4 ; la méthode doit le voir comme zéro commun.
lam24 = 0.5 + 2j * np.pi * np.arange(1, 6) / math.log(2)
v24 = np.abs(b_fact(4, lam24))
controle("W1 témoin (2,4) : b_4 s'annule aux zéros de b_2 (zéros communs infinis)", float(v24.max()) < 1e-12,
         f"max |b_4(λ)| = {v24.max():.1e} pour k = 1..5")
# (2,3) au contraire : |b_3| ne s'annule pas en un zéro de b_2 (irrationalité de θ)
controle("W2 contrôle positif (2,3) : min_k≤2·10^6 |b_3(λ_k)| > 0",
         float(min(p_.min(), m_.min())) > 0, f"min aux records {min(p_.min(), m_.min()):.3e}")
# Analogue des corps de fonctions : normes q^deg, fréquences commensurables -> zéros communs pour toute paire.
q = 5
la = 0.5 + 2j * np.pi * np.arange(1, 4) / (math.log(q))           # zéros du filtre de degré 1
vf = np.abs(1 - (q ** 2) ** (la - 0.5))                            # facteur du filtre de degré 2
controle("W3 corps de fonctions (q=5) : filtres de degrés 1 et 2 ont des zéros communs", float(vf.max()) < 1e-12,
         f"max |1 - q^(2(λ-1/2))| = {vf.max():.1e}")

# ---------------------------------------------------------------- C. constantes du contrat de forme
CE = special.zeta(3, 0.25) / 4                          # sup a(t)/t² = (1/4) ζ(3,1/4)
gamma = 0.57721566490153286
C0 = math.log(8 * math.pi) + gamma + math.pi / 2
h = 1e-5
D = -(special.zeta(1.5 + h, 1) - special.zeta(1.5 - h, 1)) / (2 * h) / special.zeta(1.5, 1)   # Σ Λ(n) n^{-3/2}
# contrôle indépendant de D par somme directe (crible) + queue majorée
N = 2_000_000
crible = np.ones(N + 1, bool); crible[:2] = False
for i in range(2, int(N ** 0.5) + 1):
    if crible[i]:
        crible[i * i::i] = False
ps = np.flatnonzero(crible)
somme = 0.0
for pr in ps:
    pk = pr
    while pk <= N:
        somme += math.log(pr) * pk ** -1.5
        pk *= pr
queue = 2 / math.sqrt(N) * 1.04        # Σ_{n>N} Λ(n) n^{-3/2} ≤ ~ ∫ x^{-3/2} (1+ε) : ordre 2/√N
controle("C1 Σ Λ(n) n^{-3/2} : dérivée de ζ contre crible", abs(somme - D) < queue + 1e-6,
         f"ζ'/ζ : {D:.6f} ; crible N=2·10^6 : {somme:.6f} (+ queue ≲ {queue:.4f})")
# a(t) = Re ψ(1/4 + it/2) - ψ(1/4) contre la série du document 76
t = np.array([0.3, 1.0, 7.0, 40.0])
serie = np.array([sum(2 * tt ** 2 / ((2 * n + 0.5) * ((2 * n + 0.5) ** 2 + tt ** 2)) for n in range(200000)) for tt in t])
digam = special.psi(0.25 + 0.5j * t).real - special.psi(0.25)
controle("C2 a(t) = Re ψ(1/4+it/2) - ψ(1/4)", float(np.max(np.abs(serie - digam))) < 1e-4,
         f"écart max {np.max(np.abs(serie - digam)):.1e} (série tronquée à 2·10^5 termes)")
CW = CE + C0 + 2 * D
R["constantes"] = {"C_E=zeta(3,1/4)/4": CE, "C0": C0, "D=sum Lambda n^-3/2": D, "C_W": CW,
                   "norme_nu_B2_majorant": 1 + 1 / 2 + 2 * math.sqrt(2), "norme_nu_B3_majorant": 1 + 1 / 3 + 2 * math.sqrt(3)}
controle("C3 C_W = C_E + C0 + 2D < 25", CW < 25, f"C_W = {CW:.4f}")

R["bilan"] = {"controles": len(R["controles"]), "echecs": sum(not c["ok"] for c in R["controles"])}
with open(os.path.join(ICI, "p1_resultats.json"), "w", encoding="utf-8") as fh:
    json.dump(R, fh, ensure_ascii=False, indent=1)
print(R["bilan"])
