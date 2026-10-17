"""Encadrement fini de la réserve radiale du signal arithmétique de Suzuki.

Le calcul porte sur des préfixes finis de puissances premières. La réserve
globale non négative pour tous les préfixes reste une obligation ouverte.
Le solveur approché propose les positions ; les intervalles les encadrent.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse
import json
import sys
import mpmath as mp


def run(corpus, cutoff):
    sys.path.insert(0, str(Path(corpus) / "3_Preuves_et_calculs/src"))
    import prime_centered_bridge as pc
    import symbolic_weil_family as w
    pc.setup(400)
    count = 64
    n = 1024
    hn = sum((F(1, k) for k in range(1, n + 1)), F(0))
    gamma_up = pc.I(hn) - mp.iv.log(pc.I(n)) - pc.I(F(1, 2*n)) + pc.I(F(1, 12*n*n))
    gamma = mp.iv.mpf([w.mpq(pc.lo(pc.I(pc.lo(gamma_up) - F(1, 120*n**4)))), w.mpq(pc.hi(gamma_up))])
    constant = mp.iv.log(8*mp.iv.pi) + gamma + mp.iv.pi/2
    total = mp.iv.pi**2/4 + 2*mp.iv.catalan
    threshold = mp.iv.log(pc.I(2))

    def arch_zero_linear(t):
        """A(t)+C0*t/2, avec la queue exponentielle encadrée."""
        t = mp.iv.mpf(t)
        series = sum((mp.iv.exp(-pc.I(F(2*k)+F(1, 2))*t) /
                      pc.I((F(2*k)+F(1, 2))**2) for k in range(count)), pc.I(0))
        b = F(2*count)+F(1, 2)
        tail = mp.iv.exp(-pc.I(b)*t)/(pc.I(b*b)*(1-mp.iv.exp(-2*t)))
        exp_series = series + mp.iv.mpf([0, w.mpq(pc.hi(tail))])
        return 4*(mp.iv.exp(t/2)+mp.iv.exp(-t/2)-2)+total-exp_series

    def arch_prime_zero_linear(t):
        t = mp.iv.mpf(t)
        r = mp.iv.exp(-t/2)
        j = mp.iv.log((1+r)/(1-r))/2 + mp.iv.atan2(r, pc.I(1))
        return 2*(mp.iv.exp(t/2)-mp.iv.exp(-t/2))+j

    def radial_equation(t):
        # Le coefficient C0 s'annule ici exactement.
        t = mp.iv.mpf(t)
        return t*arch_prime_zero_linear(t)-arch_zero_linear(t)

    def numeric_equation(t):
        r = mp.exp(-t/2)
        ap0 = 2*(mp.exp(t/2)-mp.exp(-t/2))+mp.atanh(r)+mp.atan(r)
        a0 = 4*(mp.exp(t/2)+mp.exp(-t/2)-2)+mp.pi**2/4+2*mp.catalan
        a0 -= sum(mp.exp(-(2*k+mp.mpf(".5"))*t)/(2*k+mp.mpf(".5"))**2
                  for k in range(count))
        return t*ap0-a0

    rows = []
    mass = pc.I(0)
    moment = pc.I(0)
    for item in [None]+w.prime_powers(cutoff):
        if item is not None:
            p, degree, q = item
            c = mp.iv.log(pc.I(p))/mp.iv.sqrt(pc.I(q))
            mass += c
            moment += c*mp.iv.log(pc.I(q))
        if pc.hi(moment) < pc.lo(radial_equation(threshold)):
            position = threshold
            kind = "bord T=log2"
        else:
            assert pc.lo(moment) > pc.hi(radial_equation(threshold))
            goal = w.mpq((pc.lo(moment)+pc.hi(moment))/2)
            low_guess = mp.log(2)
            high_guess = mp.mpf(2)
            while numeric_equation(high_guess) < goal:
                high_guess *= 2
            root = mp.findroot(lambda t: numeric_equation(t)-goal,
                               (low_guess, high_guess), solver="bisect",
                               tol=mp.mpf(2)**-170, maxsteps=240)
            delta = mp.mpf(2)**-30
            low = w.mpq(F(str(root-delta)))
            high = w.mpq(F(str(root+delta)))
            assert pc.hi(radial_equation(low)-moment) < 0
            assert pc.lo(radial_equation(high)-moment) > 0
            for _ in range(38):
                middle = (low+high)/2
                difference = radial_equation(middle)-moment
                if pc.hi(difference) < 0:
                    low = middle
                elif pc.lo(difference) > 0:
                    high = middle
                else:
                    break
            assert pc.hi(radial_equation(low)-moment) < 0
            assert pc.lo(radial_equation(high)-moment) > 0
            position = mp.iv.mpf([low, high])
            kind = "unique racine t*A_prime-A=L"
        reserve = arch_zero_linear(position)/position-constant/2-mass+moment/position
        assert pc.lo(reserve) > 0, ("réserve non certifiée", item, pc.pack(reserve))
        rows.append(dict(last_prime_power=item, weighted_mass=pc.pack(mass),
                         log_moment=pc.pack(moment), radial_minimizer=pc.pack(position),
                         minimizer_kind=kind, radial_reserve=pc.pack(reserve)))
    lower = min(pc.endpoint_q(tuple(row["radial_reserve"]["binary"][0])) for row in rows)
    upper = min(pc.endpoint_q(tuple(row["radial_reserve"]["binary"][1])) for row in rows)
    best = min(rows, key=lambda row: pc.endpoint_q(tuple(row["radial_reserve"]["binary"][0])))
    best_upper = pc.endpoint_q(tuple(best["radial_reserve"]["binary"][1]))
    identity_certified = all(best_upper < pc.endpoint_q(tuple(row["radial_reserve"]["binary"][0]))
                             for row in rows if row is not best)
    return dict(version="research78", cutoff=cutoff, prefix_count=len(rows),
                prime_power_count=len(rows)-1, minimum_reserve=pc.pack(mp.iv.mpf([w.mpq(lower), w.mpq(upper)])),
                minimizing_prefix=best["last_prime_power"],
                minimizing_prefix_certified=identity_certified,
                truncated_signal_lower_bound="S_cutoff(t) >= reserve*t for t>=log2 only for the truncated arithmetic sum",
                exact_signal_domain_certified="log2 <= t <= log(cutoff)",
                conditional_transport_link="Initial mass left at zero in the canonical shadow equals inf S_cutoff(t)/t, with linear boundary continuation before log2",
                numerical_model="mpmath.iv 400 bits; rational prime sieve; Euler remainder; geometric exponential tail",
                RH_proved=False, universal_sign_law_proved=False, rows=rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--cutoff", type=int, default=1000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.corpus, args.cutoff)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("Préfixes :", result["prefix_count"])
    print("Réserve minimale encadrée :", result["minimum_reserve"]["midpoint"])
    print("Préfixe minimisant :", result["minimizing_prefix"])
    print("Portée : somme arithmétique tronquée ; aucune preuve globale de RH.")
