"""TAC-006 — lanceur. Auteur des droits : Vincent NOËL. Producteur : ia:claude, 18 octobre 2026.

Exécute, dans l'ordre fixé par la prévision : construction exacte du chemin sur la fibre, pli (P1) aux plans
50 et 80 décimales, Rouché uniforme (P2), quatre boîtes de racines (P3), témoin négatif (P4).
Usage : python -I run_tac006.py CHEMIN_MPMATH_1_3_0   (écrit resultats_tac006.json, refuse d'écraser)
"""
import sys, os, json, time, datetime
if len(sys.argv) > 1: sys.path.insert(0, sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tac006_pli_fibre import *

OUT = os.path.join(HERE, 'resultats_tac006.json')
if os.path.exists(OUT): raise SystemExit('resultats_tac006.json existe déjà : déplacer le fichier avant de rejouer.')
assert mp.__version__ == '1.3.0', mp.__version__
log = {'producteur': 'ia:claude', 'droits': 'Vincent NOËL', 'mpmath': mp.__version__,
       'debut_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}
T0 = time.time()
def note(k, v): log[k] = v; print(k, json.dumps(v, ensure_ascii=False, default=str)[:600], flush=True)

# --- Objet fixé par la prévision -----------------------------------------------------------------------
geo = json.load(open(os.path.join(ROOT, '3_Preuves_et_calculs', 'data', 'v641_geometrie.json')))
sec = [r for r in geo['jet_sections'] if r['character_k'] == 1 and r['height'] == 5][0]
cand = sec['candidates'][0]['coefficients']
note('objet', {'ancre_k': 1, 'rayon': 'pi/6', 'A': 'cos(pi/6) z_1 (eta=0)', 'hauteur_prescrite_V641': 5,
               'candidat_V641': cand, 'nu_V641': sec['nu']})

# --- Plan 50 décimales : construction du chemin --------------------------------------------------------
J50 = V13Jets(50, 32, 12)
z = J50.z
ustar = [mp.mpf(2 * x) for x in cand[1:]]                    # u*=(c*-cos r e_1)/sin r
Mnum = [[cmid(z[j]).real for j in OFF], [cmid(z[j]).imag for j in OFF]]
best = None
for P0 in range(5):
    for P1 in range(P0 + 1, 5):
        d = abs(Mnum[0][P0] * Mnum[1][P1] - Mnum[0][P1] * Mnum[1][P0])
        if best is None or d > best[0]: best = (d, (P0, P1))
pivots = best[1]
free = tuple(i for i in range(5) if i not in pivots)
a_free = [to_frac(ustar[i], 30) for i in free]
probe = FibrePath(z, a_free, [Fraction(1), Fraction(0), Fraction(0)], pivots=pivots)
p_num = [mid(x) for x in probe.p]
# gradient direction of Z(5) on the fibre: Z_j(5) proportional to Re(B_j conj B_1) (common phase)
B5 = J50.components(mp.iv.mpc(point(Fraction(1, 2)), point(5)), 0)
b1 = cmid(B5[ANCHOR][0])
g = [(cmid(B5[j][0]) * mp.conj(b1)).real / abs(b1) for j in OFF]
Mm = mp.matrix(Mnum); G = Mm * Mm.T; PK = mp.eye(5) - Mm.T * mp.inverse(G) * Mm
gk = PK * mp.matrix(g)
pv = mp.matrix([mp.mpf(x.numerator) / x.denominator for x in p_num])
gk = gk - (pv.T * gk)[0] * pv
b_free = [to_frac(gk[i] / mp.norm(gk), 30) for i in free]
probe2 = FibrePath(z, a_free, b_free, pivots=pivots)
qv = mp.matrix([mp.mpf(mid(x).numerator) / mid(x).denominator for x in probe2.q])
# third orthonormal direction of the kernel (tangent direction orthogonal to q)
cands = []
for e in range(3):
    kv = mp.matrix([mp.mpf(mid(x).numerator) / mid(x).denominator for x in probe2.basis[e]])
    r = kv - (pv.T * kv)[0] * pv - (qv.T * kv)[0] * qv
    cands.append((mp.norm(r), r))
r = max(cands, key=lambda x: x[0])[1]; r = r / mp.norm(r)
n_free = [to_frac(r[i], 30) for i in free]
path50 = FibrePath(z, a_free, b_free, n_free, pivots=pivots)
note('chemin', {'pivots_dans_OFF': pivots, 'libres': free, 'a_libre': [str(x) for x in a_free],
                'b_libre': [str(x) for x in b_free], 'n_libre': [str(x) for x in n_free],
                'det_pivot': enclosure(path50.pivot_det, 18),
                'residus_noyau_p_q_max': float(max(path50.kernel_residual)),
                'p_q_orthogonalite': enclosure(path50.dot(path50.p, path50.q), 12)})

# --- P1 : pli sur la fibre, plan 50 ----------------------------------------------------------------------
omega = mp.iv.mpc(1)
sol = newton(J50, path50, 0, 5, omega)
note('newton_pli_50', None if sol is None else {'lam': float(sol[0]), 't': str(sol[1])[:40], 'iterations': sol[2]})
HW = Fraction(1, 10 ** 12)
lam_c = rounded_midpoint(point(sol[0]), 30); t_c = rounded_midpoint(point(sol[1]), 30)
fold50 = fold_certificate(J50, path50, (lam_c, t_c), HW, omega)
if not fold50['accepted_with_separations']:
    omega = mp.iv.mpc(0, 1); fold50 = fold_certificate(J50, path50, (lam_c, t_c), HW, omega); fold50['omega'] = 'i'
note('P1_pli_50', fold50)

# --- P1 : plan 80 (chemin exact identique : mêmes rationnels) --------------------------------------------
J80 = V13Jets(80, 48, 12)
path80 = FibrePath(J80.z, a_free, b_free, n_free, pivots=pivots)
sol80 = newton(J80, path80, lam_c, t_c, omega, tol=Fraction(1, 10 ** 60))
lam80 = rounded_midpoint(point(sol80[0]), 30); t80 = rounded_midpoint(point(sol80[1]), 30)
fold80 = fold_certificate(J80, path80, (lam80, t80), HW, omega)
note('P1_pli_80', fold80)
_ = V13Jets(50, 32, 12)                                         # back to the 50-digit context
J = J50; path = FibrePath(J.z, a_free, b_free, n_free, pivots=pivots)

# --- P2 : Rouché uniforme sur lam dans [lam*-1e-4, lam*+1e-4], cercle centré sur le pli exact ------------
# Révision du 18 octobre (revue de la PR #18, C2) : le pli exact (lam*, t*) n'est connu que dans la boîte
# certifiée (lam_c, t_c) ± HW du plan 50. On couvre donc lam dans [lam_c - HW - DL, lam_c + HW + DL] et tous
# les centres t dans [t_c - HW, t_c + HW] : l'énoncé vaut pour le pli exact, quelle que soit sa place dans la boîte.
DL = Fraction(1, 10 ** 4)
Lam = interval(lam_c - HW - DL, lam_c + HW + DL)
w0 = interval(t_c - HW, t_c + HW)
c_mid, _ = path.coefficients(point(lam_c))
f2 = combine(J.components(mp.iv.mpc(point(Fraction(1, 2)), point(t_c)), 2), c_mid, 2)[2]
al = -cmid(f2) / 2                                             # second w-derivative of F(1/2+iw) over two
from collections import namedtuple
alpha = namedtuple('Q', 'real imag')(to_frac(al.real, 12), to_frac(al.imag, 12))
rou = None
for R, n in ((Fraction(1, 5), 256), (Fraction(1, 5), 512), (Fraction(1, 5), 1024),
             (Fraction(1, 10), 256), (Fraction(1, 10), 512), (Fraction(1, 10), 1024)):
    rou = rouche(J, path, Lam, w0, R, n, alpha); rou['R'] = str(R); rou['n'] = n
    rou['alpha'] = [str(alpha.real), str(alpha.imag)]
    rou['lam_couvert'] = [str(lam_c - HW - DL), str(lam_c + HW + DL)]; rou['centres_couverts'] = [str(t_c - HW), str(t_c + HW)]
    note('P2_rouche_essai', rou)
    if rou['accepted']: break
log['P2_rouche'] = rou

# --- P3 : quatre boîtes aux paramètres lam_c -/+ 1e-4 -----------------------------------------------------
S = critical_system(J, path, point(lam_c), point(t_c), omega)
Hl, Htt = mid(S['H_lam']), mid(S['H_tt'])
kappa = -2 * Hl / Htt
roots = {}
RB = Fraction(1, 10 ** 9)
for side, lam in (('moins', lam_c - DL), ('plus', lam_c + DL)):
    # local model: Z ~ Z_lam (lam-lam*) + Z_tt/2 (t-t*)^2  ->  (t-t*)^2 = kappa (lam-lam*)
    v = kappa * (lam - lam_c)
    out = []
    if v > 0:
        dt = mp.sqrt(mp.mpf(v.numerator) / v.denominator)
        for sg in (1, -1):
            s = numeric_root(J, path, lam, mp.mpc('0.5', mp.mpf(t_c.numerator) / t_c.denominator + sg * dt))
            y0 = to_frac(s.imag, 18)
            out.append(root_certificate(J, path, lam, (Fraction(1, 2), y0), RB))
    else:
        ds = mp.sqrt(mp.mpf(-v.numerator) / v.denominator)
        for sg in (1, -1):
            s = numeric_root(J, path, lam, mp.mpc(mp.mpf('0.5') + sg * ds, mp.mpf(t_c.numerator) / t_c.denominator))
            out.append(root_certificate(J, path, lam, (to_frac(s.real, 18), to_frac(s.imag, 18)), RB))
    roots[side] = {'lam': str(lam), 'kappa_fois_dlam': float(v), 'boites': out}
    note('P3_' + side, roots[side])
log['kappa_numerique'] = float(kappa)

# --- P4 : témoin négatif, direction tangente orthogonale à q -------------------------------------------
Sn = critical_system(J, path, point(lam_c), point(t_c), omega, second=path.n)
note('P4_H_lam_le_long_de_n_au_pli', {'H_lam_n': float(mid(Sn['H_lam'])), 'H_lam_q': float(Hl)})
soln = newton(J, path, 0, t_c, omega, second=path.n)
if soln is None:
    wit = fold_certificate(J, path, (Fraction(0), t_c), HW, omega, second=path.n); wit['newton'] = 'pas de convergence'
else:
    wit = fold_certificate(J, path, (rounded_midpoint(point(soln[0]), 30), rounded_midpoint(point(soln[1]), 30)),
                           HW, omega, second=path.n)
    wit['newton'] = {'lam': float(soln[0]), 't': str(soln[1])[:40], 'iterations': soln[2]}
note('P4_temoin', wit)

log['fin_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
log['duree_s'] = round(time.time() - T0, 1)
json.dump(log, open(OUT, 'w'), ensure_ascii=False, indent=1, default=str)
print('écrit', OUT)
