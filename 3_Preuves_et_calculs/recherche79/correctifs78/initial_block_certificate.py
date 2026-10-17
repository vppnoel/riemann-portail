"""Brique initiale non minimale : une vraie ligne qui épuise l'atome zéro.

L'existence du couple (l,b) suit de deux changements de signe encadrés et de
la stricte monotonie. Les intervalles portent sur les racines exactes, et non
sur un noyau dont les décimales seraient prises comme des coefficients exacts.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse
import json
import sys
import mpmath as mp


def run(corpus):
    sys.path.insert(0, str(Path(corpus)/"3_Preuves_et_calculs/src"))
    import prime_centered_bridge as pc
    import symbolic_weil_family as w
    pc.setup(400)
    n = 1024
    h = sum((F(1,k) for k in range(1,n+1)), F(0))
    up = pc.I(h)-mp.iv.log(pc.I(n))-pc.I(F(1,2*n))+pc.I(F(1,12*n*n))
    gamma = mp.iv.mpf([w.mpq(pc.lo(pc.I(pc.lo(up)-F(1,120*n**4)))),w.mpq(pc.hi(up))])
    constant = mp.iv.log(8*mp.iv.pi)+gamma+mp.iv.pi/2
    total = mp.iv.pi**2/4+2*mp.iv.catalan
    count = 64

    def A(t):
        t = mp.iv.mpf(t)
        s = sum((mp.iv.exp(-pc.I(F(2*k)+F(1,2))*t)/
                 pc.I((F(2*k)+F(1,2))**2) for k in range(count)),pc.I(0))
        b = F(2*count)+F(1,2)
        tail = mp.iv.exp(-pc.I(b)*t)/(pc.I(b*b)*(1-mp.iv.exp(-2*t)))
        return (4*(mp.iv.exp(t/2)+mp.iv.exp(-t/2)-2)-constant*t/2+total
                -s-mp.iv.mpf([0,w.mpq(pc.hi(tail))]))

    def Ap(t):
        t = mp.iv.mpf(t)
        r = mp.iv.exp(-t/2)
        return (2*(mp.iv.exp(t/2)-mp.iv.exp(-t/2))-constant/2
                +mp.iv.log((1+r)/(1-r))/2+mp.iv.atan2(r,pc.I(1)))

    def H(t):
        t = mp.iv.mpf(t)
        return t*Ap(t)-A(t)

    threshold = mp.iv.log(pc.I(2))
    next_atom = mp.iv.log(pc.I(3))
    origin_mass = A(threshold)/threshold
    slope = Ap(threshold)-mp.iv.log(pc.I(2))/mp.iv.sqrt(pc.I(2))
    diffuse_mass = -slope
    demand_mass = origin_mass-slope
    demand_moment = demand_mass*threshold
    assert pc.lo(origin_mass)>0 and pc.hi(slope)<0
    left_low = F("0.84097046")
    left_high = F("0.84097048")
    assert pc.hi(threshold)<left_low<left_high<pc.lo(next_atom)

    def solve_right(left):
        lo,hi = F("1.0205"),F("1.0207")
        def equation(right):
            return Ap(pc.I(right))-Ap(pc.I(left))-diffuse_mass
        assert pc.hi(equation(lo))<0 and pc.lo(equation(hi))>0
        for _ in range(80):
            middle = (lo+hi)/2
            v = equation(middle)
            if pc.hi(v)<0:
                lo = middle
            elif pc.lo(v)>0:
                hi = middle
            else:
                break
        lo_gap,hi_gap = equation(lo),equation(hi)
        assert pc.hi(lo_gap)<0 and pc.lo(hi_gap)>0
        return mp.iv.mpf([w.mpq(lo),w.mpq(hi)]),lo_gap,hi_gap

    b_low,low_minus,low_plus = solve_right(left_low)
    b_high,high_minus,high_plus = solve_right(left_high)
    moment_low = H(b_low)-H(pc.I(left_low))-demand_moment
    moment_high = H(b_high)-H(pc.I(left_high))-demand_moment
    assert pc.hi(moment_low)<0 and pc.lo(moment_high)>0
    right = mp.iv.mpf([w.mpq(pc.lo(b_low)),w.mpq(pc.hi(b_high))])
    assert pc.lo(right)>left_high and pc.hi(right)<pc.lo(next_atom)
    return dict(
        initial_row_existence_verified=True,
        RH_used=False,
        kernel="eta=m*delta_0+beta(u)*1_[l,b](u)du; K_T=eta/(m-a)",
        equations=["A_prime(b)-A_prime(l)=-a",
                   "b*A_prime(b)-A(b)-l*A_prime(l)+A(l)=T*(m-a)"],
        monotonicity_proof="For fixed diffuse mass, b'(l)=beta(l)/beta(b); moment derivative=(b-l)*beta(l)>0",
        threshold=pc.pack(threshold),next_atom=pc.pack(next_atom),
        origin_mass=pc.pack(origin_mass),initial_slope=pc.pack(slope),
        demand_mass=pc.pack(demand_mass),diffuse_mass=pc.pack(diffuse_mass),
        left_interval=pc.pack(mp.iv.mpf([w.mpq(left_low),w.mpq(left_high)])),
        right_interval=pc.pack(right),
        sign_guards={
            "mass_at_left_low_right_low":pc.pack(low_minus),
            "mass_at_left_low_right_high":pc.pack(low_plus),
            "mass_at_left_high_right_low":pc.pack(high_minus),
            "mass_at_left_high_right_high":pc.pack(high_plus),
            "moment_at_left_low":pc.pack(moment_low),
            "moment_at_left_high":pc.pack(moment_high)},
        consequences=["The initial line consumes all of the genuine atom at zero.",
                      "Its Jensen gap is zero for t>=b.",
                      "The residual put inequality is automatic for t<log3 and is the original S(t)>=0 for t>=log3."],
        global_sign_certified=False,
        numerical_model="mpmath.iv 400 bits, exact rational brackets, Euler remainder, geometric exponential tail")


if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args = ap.parse_args()
    result = run(args.corpus)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Existence de la ligne initiale vérifiée dans le modèle déclaré.")
    print("l :",result["left_interval"]["midpoint"],"b :",result["right_interval"]["midpoint"])
    print("L'origine est entièrement consommée ; le signe global reste ouvert.")
