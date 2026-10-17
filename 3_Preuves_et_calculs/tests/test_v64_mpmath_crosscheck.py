"""V6.4.1 — recoupement, par mpmath, de l'évaluateur maison et des listes de zéros des versions V6.3d à V6.4.

Ces versions ont été produites sans mpmath (évaluation en double précision par Euler-Maclaurin).
Ici mpmath (30 chiffres) sert de seconde source indépendante. Fichier non exécuté si mpmath est absent.
"""
import csv, sys
from pathlib import Path
import mpmath as mp
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
D = ROOT / "data"
mp.mp.dps = 30
CHI = [0, 1, 1j, -1j, -1]
CHIB = [0, 1, -1j, 1j, -1]

def _zeros(name):
    return [mp.mpc(float(r["sigma"]), float(r["t"])) for r in csv.DictReader(open(D / name))]
def _DH(s):
    from rejection import KAPPA_DH
    k = mp.mpf(KAPPA_DH)
    return (1 - 1j * k) / 2 * mp.dirichlet(s, CHI) + (1 + 1j * k) / 2 * mp.dirichlet(s, CHIB)

def test_numpy_evaluator_matches_mpmath():
    from zero_reconstruction import hurwitz_zeta, F_eval
    for s in (0.5 + 14.1j, 0.3 + 250.7j, 1.2 + 599.3j, 0.5 + 1499.0j, -0.9 + 37.0j, 2.5 + 0.3j):
        for a in (1.0, 0.2, 0.8):
            ref = mp.zeta(mp.mpc(s), a)
            assert abs(complex(ref) - hurwitz_zeta(s, a)) < 1e-9 * max(1.0, abs(complex(ref)))
        assert abs(complex(mp.dirichlet(mp.mpc(s), CHI)) - F_eval("L_chi5", s)) < 1e-9
        assert abs(complex(_DH(mp.mpc(s))) - F_eval("DH", s)) < 1e-9

def test_zeta_zero_list_matches_mpmath():
    z = sorted(float(r["t"]) for r in csv.DictReader(open(D / "zeta_zeros_1500.csv")))
    assert len(z) == 1070 == int(mp.nzeros(z[-1] + 0.01)) and int(mp.nzeros(z[-1] - 0.01)) == 1069
    for n in (1, 2, 300, 301, 650, 1000, 1070):
        assert abs(float(mp.zetazero(n).imag) - z[n - 1]) < 1e-9

def test_L_chi5_and_DH_zero_lists_vanish_under_mpmath():
    zl = _zeros("L_chi5_zeros_600.csv"); zd = _zeros("dh_zeros_600.csv")
    assert len(zl) == 988 and len(zd) == 494
    for z in zl[::49]:
        assert abs(mp.dirichlet(z, CHI)) < 1e-9
    off = [z for z in zd if abs(z.real - 0.5) > 1e-6]
    assert len(off) == 30
    for z in zd[::29] + off:
        assert abs(_DH(z)) < 1e-9
    # les deux zéros bas ajoutés en V6.3d
    for t in (5.094159844571096, 8.939914408096524):
        assert abs(_DH(mp.mpc(0.5, t))) < 1e-12

def test_family_mod7_matches_mpmath():
    """V6.5 : L(s, chi_3 mod 7) et le sosie f_7, évaluateur maison contre mpmath.dirichlet."""
    from family_mod7 import F0, F1, CHI1, CHI3, C1, C2
    chi1 = [0] + [mp.mpc(CHI1[a]) for a in range(1, 7)]; chi3 = [0] + [mp.mpc(CHI3[a]) for a in range(1, 7)]
    chi1b = [mp.conj(x) for x in chi1]
    for s in (0.5 + 14.1j, 0.3 + 250.7j, 1.2 + 599.3j, 0.5 + 999.0j):
        z = mp.mpc(s)
        assert abs(complex(mp.dirichlet(z, chi3)) - F0(s)) < 1e-9
        assert abs(complex(mp.mpc(C1) * mp.dirichlet(z, chi1) + mp.mpc(C2) * mp.dirichlet(z, chi1b)) - F1(s)) < 1e-9

def test_f7_has_a_zero_to_the_right_of_one_under_mpmath():
    """V6.5.1 : le zéro de f_7 trouvé à droite de Re s = 1 est confirmé par mpmath."""
    from family_mod7 import CHI1, C1, C2
    chi1 = [0] + [mp.mpc(CHI1[a]) for a in range(1, 7)]; chi1b = [mp.conj(x) for x in chi1]
    f7 = lambda s: mp.mpc(C1) * mp.dirichlet(s, chi1) + mp.mpc(C2) * mp.dirichlet(s, chi1b)
    r = [x for x in csv.DictReader(open(D / "family_mod7_rightmost.csv")) if float(x["theta"]) == 1.0][0]
    z = mp.findroot(f7, mp.mpc(float(r["sigma_max"]), float(r["t"])))
    assert z.real > 1.05 and abs(f7(z)) < 1e-20 and abs(complex(z) - complex(float(r["sigma_max"]), float(r["t"]))) < 1e-8

if __name__ == "__main__":
    n = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); n += 1; print("OK  ", name)
    print(f"{n}/{n}")
