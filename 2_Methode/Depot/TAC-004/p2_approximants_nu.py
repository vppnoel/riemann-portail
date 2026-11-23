# -*- coding: utf-8 -*-
"""TAC-004, partie 2 : approximants à deux filtres en norme ν, contrat d'erreur et témoins.

Programme Riemann V6.59. Producteur : ia:claude. Code sous licence MIT (voir LICENSE à la racine).

Algorithme (RAPPORT, § 4) : pour une cible polaire f = Pψ, ψ ∈ C_c^∞(-1, 1), chercher g_p dans des splines
cubiques nulles au bord, sur des boîtes FIXÉES (ch supp f + [-log 3, log 3] pour g_2, + [-log 2, log 2] pour g_3),
et minimiser ν(f - B_2 g_2 - B_3 g_3), avec ν(u)² = ∫ e^{2|x|}(|u|² + |u'|²) dx.
Le résidu ε_h = ν(f - f_h) est recalculé A POSTERIORI sur une seconde quadrature, indépendante de celle de la
résolution. Les nombres de ce programme sont MESURÉS (quadratures en double précision), non certifiés.

Témoins (doivent échouer là où la théorie le prévoit, avec un minorant rigoureux du résidu) :
  N1  filtre seul B_2 ;  N2  paire commensurable (B_2, B_4) ;  N3  cible à moments non nuls ;
  N4  schéma de Neumann à un filtre : converge en L², diverge en ν, support croissant ;
  N5  coût des commas : ν(g_3) ≥ (|F(λ_k)| - √2 ε)/(√2 |b_3(λ_k)|) pour toute décomposition.
Exécution : python -B p2_approximants_nu.py   (numpy, scipy). Durée : quelques minutes.
"""
import json
import math
import os
import time

import numpy as np
from scipy import integrate, special

ICI = os.path.dirname(os.path.abspath(__file__))
R = {"programme": "p2_approximants_nu.py", "controles": [], "essais": []}
LOG2, LOG3 = math.log(2), math.log(3)
C_W = json.load(open(os.path.join(ICI, "p1_resultats.json"), encoding="utf-8"))["constantes"]["C_W"]


def controle(nom, ok, detail):
    R["controles"].append({"nom": nom, "ok": bool(ok), "detail": detail})
    print(("OK   " if ok else "ECHEC"), nom, "-", detail, flush=True)
    return ok


# ------------------------------------------------------------------ cibles (valeur et dérivée exactes)
def bosse(x):
    """ψ(x) = exp(-1/(1-x²)) sur (-1,1) et ses trois dérivées."""
    x = np.asarray(x, float)
    out = np.zeros((4,) + x.shape)
    m = np.abs(x) < 1
    y = x[m]
    w = 1 - y * y
    u1 = -2 * y / w ** 2
    u2 = -(2 + 6 * y * y) / w ** 3
    u3 = -24 * y * (1 + y * y) / w ** 4
    p0 = np.exp(-1 / w)
    out[0][m] = p0
    out[1][m] = u1 * p0
    out[2][m] = (u2 + u1 ** 2) * p0
    out[3][m] = (u3 + 3 * u1 * u2 + u1 ** 3) * p0
    return out


def module(y):
    """Fabrique ψ_y = ψ·cos(y x) (y = 0 : ψ)."""
    def psi(x):
        b0, b1, b2, b3 = bosse(x)
        if y == 0:
            return b0, b1, b2, b3
        c, s = np.cos(y * x), np.sin(y * x)
        c1, c2, c3 = -y * s, -y * y * c, y ** 3 * s
        return (b0 * c, b1 * c + b0 * c1, b2 * c + 2 * b1 * c1 + b0 * c2,
                b3 * c + 3 * b2 * c1 + 3 * b1 * c2 + b0 * c3)
    return psi


def cible_polaire(psi):
    """f = Pψ = ψ'' - ψ/4 et f' = ψ''' - ψ'/4."""
    def f(x):
        p0, p1, p2, p3 = psi(x)
        return p2 - p0 / 4, p3 - p1 / 4
    return f


def cible_brute(psi):
    """f = ψ (moments non nuls) : témoin N3."""
    def f(x):
        p0, p1, _, _ = psi(x)
        return p0, p1
    return f


def laplace(f, lam):
    re = integrate.quad(lambda x: (f(np.array([x]))[0][0] * np.exp(lam * x)).real, -1, 1, limit=400, epsabs=1e-14)[0]
    im = integrate.quad(lambda x: (f(np.array([x]))[0][0] * np.exp(lam * x)).imag, -1, 1, limit=400, epsabs=1e-14)[0]
    return re + 1j * im


# ------------------------------------------------------------------ B-splines cubiques cardinales
def N4(t):
    t = np.asarray(t, float)
    v = np.zeros_like(t)
    d = np.zeros_like(t)
    a = (t >= 0) & (t < 1); v[a] = t[a] ** 3 / 6; d[a] = t[a] ** 2 / 2
    a = (t >= 1) & (t < 2); tt = t[a]; v[a] = (-3 * tt ** 3 + 12 * tt ** 2 - 12 * tt + 4) / 6; d[a] = (-9 * tt ** 2 + 24 * tt - 12) / 6
    a = (t >= 2) & (t < 3); tt = t[a]; v[a] = (3 * tt ** 3 - 24 * tt ** 2 + 60 * tt - 44) / 6; d[a] = (9 * tt ** 2 - 48 * tt + 60) / 6
    a = (t >= 3) & (t < 4); tt = t[a]; v[a] = (4 - tt) ** 3 / 6; d[a] = -(4 - tt) ** 2 / 2
    return v, d


class Base:
    """Splines cubiques à support dans [a, b] (nulles avec deux dérivées au bord)."""
    def __init__(self, a, b, h_cible):
        self.a, self.b = a, b
        self.m = max(4, int(math.ceil((b - a) / h_cible)))
        self.h = (b - a) / self.m
        self.n = self.m - 3

    def eval(self, x):                       # matrices (len(x), n) : valeurs et dérivées
        t = (np.asarray(x)[:, None] - self.a) / self.h - np.arange(self.n)[None, :]
        v, d = N4(t)
        return v, d / self.h


def filtre_colonnes(base, p, x):
    """Colonnes de B_p appliqué à la base, valeurs et dérivées aux points x."""
    L = math.log(p)
    v0, d0 = base.eval(x)
    vm, dm = base.eval(x - L)
    vp, dp = base.eval(x + L)
    c = p ** -0.5
    return (1 + 1 / p) * v0 - c * (vm + vp), (1 + 1 / p) * d0 - c * (dm + dp)


def noeuds(X0, X1, largeur, ordre):
    n = int(math.ceil((X1 - X0) / largeur))
    bords = np.linspace(X0, X1, n + 1)
    g, w = np.polynomial.legendre.leggauss(ordre)
    mil, dem = (bords[:-1] + bords[1:]) / 2, (bords[1:] - bords[:-1]) / 2
    return (mil[:, None] + dem[:, None] * g[None, :]).ravel(), (dem[:, None] * w[None, :]).ravel()


def resoudre(f, filtres, h, seuil=1e-13):
    """filtres : liste de (p, a, b). Moindres carrés en ν ; renvoie coefficients et bases."""
    bases = [Base(a, b, h) for (_, a, b) in filtres]
    X = max(max(abs(a), abs(b)) + math.log(p) for (p, a, b) in filtres) + 1e-9
    x, w = noeuds(-X, X, min(B.h for B in bases) / 2, 6)
    n = sum(B.n for B in bases)
    G = np.zeros((n, n)); rhs = np.zeros(n)
    for i0 in range(0, len(x), 4000):
        xs, ws = x[i0:i0 + 4000], w[i0:i0 + 4000] * np.exp(2 * np.abs(x[i0:i0 + 4000]))
        V = np.hstack([filtre_colonnes(B, p, xs)[0] for B, (p, _, _) in zip(bases, filtres)])
        D = np.hstack([filtre_colonnes(B, p, xs)[1] for B, (p, _, _) in zip(bases, filtres)])
        fv, fd = f(xs)
        G += (V * ws[:, None]).T @ V + (D * ws[:, None]).T @ D
        rhs += (V * ws[:, None]).T @ fv + (D * ws[:, None]).T @ fd
    ev, Q = np.linalg.eigh(G)
    garde = ev > seuil * ev.max()
    c = Q[:, garde] @ ((Q[:, garde].T @ rhs) / ev[garde])
    return c, bases, X, int((~garde).sum()), float(ev.max() / ev[garde].min())


def evaluer(c, bases, filtres, x):
    fv = np.zeros_like(x); fd = np.zeros_like(x); i = 0
    for B, (p, _, _) in zip(bases, filtres):
        V, D = filtre_colonnes(B, p, x)
        fv += V @ c[i:i + B.n]; fd += D @ c[i:i + B.n]; i += B.n
    return fv, fd


def nu(fv, fd, x, w):
    return math.sqrt(float(np.sum(w * np.exp(2 * np.abs(x)) * (fv ** 2 + fd ** 2))))


def a_posteriori(f, c, bases, filtres, X):
    """Seconde quadrature (largeur et ordre différents) : résidu ν et L², ν(f), moments de f_h, ν(g_p)."""
    x, w = noeuds(-X, X, min(B.h for B in bases) / 3, 7)
    fv, fd = f(x)
    hv, hd = evaluer(c, bases, filtres, x)
    eps = nu(fv - hv, fd - hd, x, w)
    l2 = math.sqrt(float(np.sum(w * (fv - hv) ** 2)))
    nuf = nu(fv, fd, x, w)
    mom = [float(abs(np.sum(w * hv * np.exp(sg * x / 2)))) for sg in (1, -1)]
    ng = []; i = 0
    for B in bases:
        xb, wb = noeuds(B.a, B.b, B.h / 3, 7)
        V, D = B.eval(xb)
        ng.append(nu(V @ c[i:i + B.n], D @ c[i:i + B.n], xb, wb)); i += B.n
    return eps, l2, nuf, mom, ng


def essai(nom, f, filtres, hs):
    lignes = []
    for h in hs:
        t0 = time.time()
        c, bases, X, nnul, cond = resoudre(f, filtres, h)
        eps, l2, nuf, mom, ng = a_posteriori(f, c, bases, filtres, X)
        lignes.append({"h": h, "inconnues": int(sum(B.n for B in bases)), "eps_nu": eps, "eps_rel": eps / nuf,
                       "residu_L2": l2, "nu_f": nuf, "moments_f_h": mom, "nu_g": ng,
                       "supports_g": [[B.a, B.b] for B in bases], "directions_ecartees": nnul,
                       "conditionnement_retenu": cond, "secondes": round(time.time() - t0, 1)})
        print(f"  {nom} h={h:.4f} eps_rel={eps / nuf:.3e} L2={l2:.2e} ν(g)={[round(v, 2) for v in ng]} "
              f"mom={max(mom):.1e} ({lignes[-1]['secondes']} s)", flush=True)
    R["essais"].append({"nom": nom, "filtres": [p for (p, _, _) in filtres], "lignes": lignes})
    return lignes


# ------------------------------------------------------------------ 0. contrôle des dérivées de la bosse
xx = np.linspace(-0.95, 0.95, 41); hh = 1e-5
for k, nomd in ((1, "ψ'"), (2, "ψ''"), (3, "ψ'''")):
    num = (bosse(xx + hh)[k - 1] - bosse(xx - hh)[k - 1]) / (2 * hh)
    e = float(np.max(np.abs(num - bosse(xx)[k])) / np.max(np.abs(bosse(xx)[k])))
    controle(f"D0 dérivée analytique {nomd} contre différence finie", e < 1e-6, f"écart relatif {e:.1e}")

T1 = cible_polaire(module(0.0))
for sg in (1, -1):
    m = abs(laplace(T1, sg * 0.5))
    controle(f"D1 cible T1 = Pψ polaire : |l_{'+' if sg > 0 else '-'}(f)|", m < 1e-12, f"{m:.1e}")

BOITE = lambda A: (-1 - A, 1 + A)
F23 = [(2,) + BOITE(LOG3), (3,) + BOITE(LOG2)]

# ------------------------------------------------------------------ 1. deux filtres, cible lisse : convergence
print("Essai 1 : deux filtres (2,3), T1", flush=True)
L1 = essai("deux_filtres_T1", T1, F23, [1 / 4, 1 / 8, 1 / 16, 1 / 32, 1 / 64, 1 / 128])
e = [l["eps_rel"] for l in L1]
# Passe 2 (seuil révisé après la passe 1, voir RAPPORT § 5.4) : décroissance stricte et ε_rel < 1e-2 au pas le plus fin.
controle("E1 convergence en ν à support fixé (deux filtres, T1)",
         all(e[i + 1] < e[i] for i in range(len(e) - 1)) and e[-1] < 1e-2,
         "ε_rel = " + ", ".join(f"{v:.2e}" for v in e))
# Les moments de f_h sont nuls algébriquement (b_p(±1/2) = 0) ; la valeur lue est l'erreur de quadrature,
# proportionnelle à la taille des coefficients : critère relatif à ν(g_2) + ν(g_3).
rel = max(max(l["moments_f_h"]) / sum(l["nu_g"]) for l in L1)
controle("E2 moments de f_h nuls à l'erreur de quadrature près (relatif à ν(g))", rel < 1e-9,
         f"max |l_±(f_h)| / (ν(g_2)+ν(g_3)) = {rel:.1e}")
pentes = [math.log(e[i] / e[i + 1]) / math.log(2) for i in range(len(e) - 1)]
R["pentes_T1"] = pentes

# Raffinement : boîtes agrandies (le résidu ne doit pas dépendre d'un support croissant)
L1b = essai("deux_filtres_T1_boites_x2", T1, [(2,) + BOITE(2 * LOG3), (3,) + BOITE(2 * LOG2)], [1 / 32])

# ------------------------------------------------------------------ 2. témoins négatifs à minorant rigoureux
zeros_b2 = [sg * 0.5 + 2j * math.pi * k / LOG2 for sg in (1, -1) for k in range(1, 41)] + \
           [sg * 0.5 - 2j * math.pi * k / LOG2 for sg in (1, -1) for k in range(1, 41)]
FZ = np.array([abs(laplace(T1, l)) for l in zeros_b2])
LB_b2 = float(FZ.max() / math.sqrt(2))
R["minorant_zeros_b2_T1"] = {"max_F_lambda": float(FZ.max()), "minorant_nu": LB_b2,
                            "lambda_argmax": str(zeros_b2[int(FZ.argmax())])}

print("Témoin N1 : filtre seul B_2", flush=True)
N1 = essai("temoin_N1_filtre_seul", T1, [(2,) + BOITE(math.log(6))], [1 / 8, 1 / 16, 1 / 32])
print("Témoin N2 : paire commensurable (2,4)", flush=True)
N2 = essai("temoin_N2_paire_2_4", T1, [(2,) + BOITE(math.log(4)), (4,) + BOITE(LOG2)], [1 / 8, 1 / 16, 1 / 32])
for nom, L in (("N1 filtre seul", N1), ("N2 paire (2,4)", N2)):
    ok = all(l["eps_nu"] >= LB_b2 * (1 - 1e-6) for l in L) and L[-1]["eps_nu"] > 0.5 * L[0]["eps_nu"]
    controle(f"{nom} : résidu ν ≥ max_λ∈Z(b_2) |F(λ)|/√2 et stagnation", ok,
             f"minorant {LB_b2:.3e} ; ε = " + ", ".join(f"{l['eps_nu']:.3e}" for l in L))

T3 = cible_brute(module(0.0))
mom3 = max(abs(laplace(T3, 0.5)), abs(laplace(T3, -0.5)))
print("Témoin N3 : cible à moments non nuls", flush=True)
N3 = essai("temoin_N3_moments", T3, F23, [1 / 8, 1 / 16, 1 / 32])
controle("N3 cible non polaire : résidu ν ≥ max |l_±(f)|/√2 et stagnation",
         all(l["eps_nu"] >= mom3 / math.sqrt(2) * (1 - 1e-6) for l in N3) and N3[-1]["eps_nu"] > 0.5 * N3[0]["eps_nu"],
         f"minorant {mom3 / math.sqrt(2):.3e} ; ε = " + ", ".join(f"{l['eps_nu']:.3e}" for l in N3))

# ------------------------------------------------------------------ 3. témoin N4 : Neumann à un filtre
# g_J = N_J N_J^* f, N_J = Σ_{j<J} 2^{-j/2} U_{j log 2} ; f - B_2 g_J = a^J (U^J + U^{-J}) f - a^{2J} f, a = 2^{-1/2}
neu = []
for J in range(1, 13):
    a = 2 ** -0.5
    X = 1 + J * LOG2 + 1e-9
    x, w = noeuds(-X, X, 1 / 200, 6)
    def res(x):
        fv, fd = T1(x); pv, pd = T1(x - J * LOG2); mv, md = T1(x + J * LOG2)
        return a ** J * (pv + mv) - a ** (2 * J) * fv, a ** J * (pd + md) - a ** (2 * J) * fd
    rv, rd = res(x)
    neu.append({"J": J, "residu_L2": math.sqrt(float(np.sum(w * rv ** 2))), "residu_nu": nu(rv, rd, x, w),
                "support_g": [-1 - (J - 1) * LOG2, 1 + (J - 1) * LOG2]})
R["temoin_N4_neumann"] = neu
l2 = [d["residu_L2"] for d in neu]; nn = [d["residu_nu"] for d in neu]
# Théorie : pour J grand, résidu L² ∝ 2^{-J/2} et résidu ν ∝ 2^{+J/2} (poids e^{2|x|} sur un support translaté de J log 2).
rl = [l2[i + 1] / l2[i] for i in range(5, 11)]; rn = [nn[i + 1] / nn[i] for i in range(5, 11)]
controle("N4 Neumann : L² ∝ 2^{-J/2} → 0, ν ∝ 2^{J/2} → ∞, support ∝ J (le critère de rejet le refuse)",
         all(abs(v - 2 ** -0.5) < 0.02 for v in rl) and all(abs(v - 2 ** 0.5) < 0.03 for v in rn),
         f"L² : {l2[0]:.2e} → {l2[-1]:.2e} ; ν : {nn[0]:.2e} → {nn[-1]:.2e} ; demi-support {neu[-1]['support_g'][1]:.2f}")

# ------------------------------------------------------------------ 4. coût des commas (N5)
for k, hs in ((5, [1 / 64, 1 / 128]), (12, [1 / 128, 1 / 256])):
    y = 2 * math.pi * k / LOG2
    Tk = cible_polaire(module(y))
    lam = 0.5 + 1j * y
    Fl = abs(laplace(Tk, lam))
    b3 = abs((1 - 3 ** (lam - 0.5)) * (1 - 3 ** (-lam - 0.5)))
    print(f"Essai commas k={k} (y={y:.2f}, |b_3(λ_k)|={b3:.3e})", flush=True)
    Lk = essai(f"commas_k{k}", Tk, F23, hs)
    fin = Lk[-1]
    mino = (Fl - math.sqrt(2) * fin["eps_nu"]) / (math.sqrt(2) * b3)
    R.setdefault("commas_cout", []).append({"k": k, "y": y, "abs_F_lambda": Fl, "abs_b3": b3, "nu_f": fin["nu_f"],
                                            "eps_nu": fin["eps_nu"], "nu_g3": fin["nu_g"][1], "minorant_nu_g3": mino,
                                            "rapport_nu_g3_sur_nu_f": fin["nu_g"][1] / fin["nu_f"]})
    if mino > 0:
        controle(f"N5 commas k={k} : ν(g_3) ≥ (|F(λ_k)| - √2ε)/(√2|b_3(λ_k)|) (toute décomposition)",
                 fin["nu_g"][1] >= mino, f"ν(g_3) = {fin['nu_g'][1]:.3e} ≥ {mino:.3e} ; ε_rel = {fin['eps_rel']:.2e}")
    else:   # résidu encore trop grand : le minorant est vide, le test n'est pas concluant (ce n'est pas un succès)
        R.setdefault("non_concluants", []).append({"nom": f"N5 commas k={k}", "minorant": mino, "eps_rel": fin["eps_rel"]})
        print(f"NONC  N5 commas k={k} : minorant {mino:.3e} ≤ 0 (ε_rel = {fin['eps_rel']:.2e}), non concluant", flush=True)

# ------------------------------------------------------------------ 5. contrat de forme sur T1
def Q_W(fun, X):
    """Forme de Weil du document 76 (Fourier unitaire), mesurée. fun : x -> valeurs."""
    dx = 1 / 512
    xg = np.arange(-X, X + dx / 2, dx)
    v = fun(xg)
    n = 1 << 17
    F = np.fft.fft(v, n) * dx / math.sqrt(2 * math.pi)
    t = 2 * math.pi * np.fft.fftfreq(n, dx)
    a = special.psi(0.25 + 0.5j * t).real - special.psi(0.25)
    dt = 2 * math.pi / (n * dx)
    E = float(np.sum(a * np.abs(F) ** 2) * dt)
    m = float(np.sum(v * v) * dx)
    C0 = math.log(8 * math.pi) + 0.57721566490153286 + math.pi / 2
    # puissances de premiers q < e^{2X}
    Q = 0.0
    qmax = int(math.exp(2 * X)) + 1
    crible = np.ones(qmax + 1, bool); crible[:2] = False
    for i in range(2, int(qmax ** 0.5) + 1):
        if crible[i]:
            crible[i * i::i] = False
    for p in np.flatnonzero(crible):
        q = p
        while q <= qmax:
            d = math.log(q)
            corr = float(np.sum(v * fun(xg - d)) * dx)
            Q += math.log(p) / math.sqrt(q) * corr
            q *= p
    return E - C0 * m - 2 * Q, E, m


fin = L1[-1]
c, bases, X, _, _ = resoudre(T1, F23, fin["h"])
qf = Q_W(lambda x: T1(x)[0], X)
qh = Q_W(lambda x: evaluer(c, bases, F23, x)[0], X)
borne = C_W * fin["eps_nu"] * (2 * fin["nu_f"] + fin["eps_nu"])
R["contrat_forme_T1"] = {"Q_W_f": qf[0], "Q_W_f_h": qh[0], "ecart": abs(qf[0] - qh[0]), "borne_C_W": borne,
                         "E_f": qf[1], "m_f": qf[2], "h": fin["h"], "C_W": C_W}
controle("F1 contrat |Q_W(f) - Q_W(f_h)| ≤ C_W ε (2ν(f) + ε) (mesuré)", abs(qf[0] - qh[0]) <= borne,
         f"écart {abs(qf[0] - qh[0]):.3e} ≤ borne {borne:.3e} ; Q_W(f) = {qf[0]:.6f} (mesure, sans valeur de certificat)")

R["bilan"] = {"controles": len(R["controles"]), "echecs": sum(not c["ok"] for c in R["controles"]),
            "non_concluants": len(R.get("non_concluants", []))}
with open(os.path.join(ICI, "p2_resultats.json"), "w", encoding="utf-8") as fh:
    json.dump(R, fh, ensure_ascii=False, indent=1)
print(R["bilan"])
