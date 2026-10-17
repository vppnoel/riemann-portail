#!/usr/bin/env python3
"""Finite, reproducible diagnostics for block compensation. No zeta zeros.

Numbers returned by this program are high-precision diagnostics, not directed
interval certificates. All global claims are explicitly false in the metadata.
The exact rational countermodels have a different status: their checks are exact.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse
import csv
import json
import mpmath as mp


def prime_powers(bound):
    sieve = bytearray(b'\x01') * (bound + 1)
    sieve[:2] = b'\x00\x00'
    for p in range(2, int(bound**0.5) + 1):
        if sieve[p]:
            sieve[p*p:bound+1:p] = b'\x00' * ((bound-p*p)//p + 1)
    out = []
    for p in range(2, bound + 1):
        if sieve[p]:
            n, k = p, 1
            while n <= bound:
                out.append((n, p, k))
                n *= p
                k += 1
    return sorted(out)


class Arch:
    def __init__(self):
        self.T = mp.log(2)
        self.C0 = mp.log(8*mp.pi) + mp.euler + mp.pi/2
        self.total = mp.pi**2/4 + 2*mp.catalan
        self.lams = [2*k + mp.mpf('.5') for k in range(140)]
        self.apt = self.Ap(self.T)
        self.cache = {}

    def A(self, t):
        z = mp.exp(-2*t)
        s = mp.mpf(0)
        for lam in reversed(self.lams):
            s = s*z + 1/lam**2
        return (4*(mp.exp(t/2)+mp.exp(-t/2)-2)-self.C0*t/2
                + self.total - mp.exp(-t/2)*s)

    def Ap(self, t):
        r = mp.exp(-t/2)
        return 2*(1/r-r)-self.C0/2 + mp.atanh(r)+mp.atan(r)

    def beta(self, t):
        return mp.exp(t/2)-mp.exp(-mp.mpf('2.5')*t)/(1-mp.exp(-2*t))

    def dual(self, mass):
        key = mp.nstr(mass, mp.mp.dps)
        if key in self.cache:
            return self.cache[key]
        if mass <= self.apt:
            t = self.T
        else:
            t = max(self.T, 2*mp.log((mass+self.C0/2)/2))
            for _ in range(60):
                err = self.Ap(t)-mass
                new = t-err/self.beta(t)
                if new <= self.T:
                    new = (t+self.T)/2
                if abs(new-t) < mp.mpf(10)**(-mp.mp.dps+8):
                    t = new
                    break
                t = new
            else:
                raise ArithmeticError('dual root did not converge')
            assert abs(self.Ap(t)-mass) < mp.mpf(10)**(-mp.mp.dps+7)*max(1,mass)
        value = mass*t-self.A(t)
        self.cache[key] = (t, value)
        return t, value


def exact_models():
    def put(measure, t):
        return sum((m*max(t-x, Q(0)) for x,m in measure), Q(0))

    alpha = [(Q(1),Q(10)),(Q(9,2),Q(11))]
    nu = [(Q(2),Q(15))]
    residual = alpha+[(x,-m) for x,m in nu]
    signed = {}
    def add(x,m):
        signed[x] = signed.get(x,Q(0))+m
    for x,m in residual:
        add(x,x*m)
    for x,m in alpha:
        for y,n in alpha:
            add(x+y,m*n)
    for x,m in nu:
        for y,n in nu:
            add(x+y,-m*n)
    D = sorted(signed.items())
    breaks = sorted({Q(0)}|set(signed))
    checks = [(str(t),str(put(D,t))) for t in breaks]
    assert all(put(D,t)>=0 for t in breaks)
    assert sum((m for x,m in D),Q(0)) > 0
    assert put(residual,Q(9,2)) == Q(-5,2)
    # Linear on each interval: endpoint checks plus final positive slope
    # establish nonnegative forcing potential on the entire half-line.
    return {
        'endpoint_trap': {
            'A':'t^2/2 on [0,3], Lebesgue source',
            'demand':[['1/4','3/2'],['11/4','3/2']],
            'start_defect':'0','end_defect':'0',
            'first_prefix_defect':str(Q(3,2)*Q(1,4)-Q(3,2)**2/2),
            'signal_at_t_1':str(Q(1,2)-Q(3,2)*Q(3,4)),
            'proof_status':'exact rational algebra; abstract model, not zeta',
        },
        'selberg_inverse_trap':{
            'source':[[str(x),str(m)] for x,m in alpha],
            'demand':[[str(x),str(m)] for x,m in nu],
            'forcing_measure':[[str(x),str(m)] for x,m in D],
            'forcing_potential_at_breaks':checks,
            'forcing_potential_globally_nonnegative':True,
            'residual_negative_interval':['4','59/12'],
            'residual_at_9_over_2':'-5/2',
            'proof_status':'exact rational algebra; abstract model, not zeta',
        }
    }


def run(bound, digits, out):
    mp.mp.dps = digits
    arch = Arch()
    rows = []
    C = L = mp.mpf(0)
    theta0, G0 = arch.dual(C)
    H0 = -G0
    prevH, prevG = H0, G0
    credit_sum = phase_sum = mp.mpf(0)
    max_identity_error = mp.mpf(0)
    for n,p,k in prime_powers(bound):
        x, c = mp.log(n), mp.log(p)/mp.sqrt(n)
        C += c
        L += c*x
        theta,G = arch.dual(C)
        H = L-G
        credit = c*theta-(G-prevG)
        phase = c*(x-theta)
        error = abs((H-prevH)-(credit+phase))
        max_identity_error = max(max_identity_error,error)
        assert credit > 0
        credit_sum += credit
        phase_sum += phase
        rows.append(dict(q=n,p=p,k=k,x=x,c=c,C=C,L=L,theta=theta,G=G,H=H,
                         credit=credit,phase=phase,increment=H-prevH))
        prevH,prevG = H,G

    zero = dict(C=mp.mpf(0),L=mp.mpf(0),H=H0,G=G0)
    edge_tol = mp.mpf(10)**(-digits+12)
    def prefix_before(t):
        selected = [r for r in rows if r['x'] <= t+edge_tol]
        return selected[-1] if selected else zero

    def guard(a,b):
        before, after = prefix_before(a), prefix_before(b)
        picked = [r for r in rows if a+edge_tol < r['x'] <= b+edge_tol]
        if not picked:
            return None
        D,M = after['C']-before['C'], after['L']-before['L']
        dstar = (b*D-M)/(b-a)
        assert -edge_tol <= dstar <= D+edge_tol
        dstar = max(mp.mpf(0),min(D,dstar))
        _,gstar = arch.dual(before['C']+dstar)
        corner = before['H']+a*dstar-(gstar-before['G'])
        actual = min([before['H']]+[r['H'] for r in picked])
        return dict(left=mp.exp(a),right=mp.exp(b),count=len(picked),
                    start=before['H'],end=after['H'],D=D,M=M,dstar=dstar,
                    corner=corner,guard=min(before['H'],after['H'],corner),
                    actual_min=actual)

    blocks = []
    lower = 2
    while lower < bound:
        upper = min(2*lower,bound)
        block = guard(mp.log(lower),mp.log(upper))
        if block is not None:
            blocks.append(block)
        lower = upper

    refinements = []
    for pieces in [1,2,4,8,16,32,64]:
        guards = []
        for block in blocks:
            a,b = mp.log(block['left']),mp.log(block['right'])
            for j in range(pieces):
                g = guard(a+(b-a)*j/pieces,a+(b-a)*(j+1)/pieces)
                if g:
                    guards.append(g)
        refinements.append(dict(parts_per_block=pieces,
                                nonempty_parts=len(guards),
                                failures=sum(g['guard']<0 for g in guards),
                                minimum_guard=min(g['guard'] for g in guards)))

    def fmt(value):
        if isinstance(value,mp.mpf):
            return mp.nstr(value,40)
        if isinstance(value,dict):
            return {k:fmt(v) for k,v in value.items()}
        if isinstance(value,list):
            return [fmt(v) for v in value]
        return value
    z = 2*(mp.sqrt(2)-1)/mp.log(2)-1
    result = dict(
        purpose='Falsify or refine a compensation rule at an existing finite ceiling',
        cutoff=bound,digits=digits,prefix_count=len(rows),
        arithmetic_model='mpmath, finite exponential series (140 terms), no directed interval rounding',
        diagnostic_boundary_tolerance=edge_tol,
        exponential_tail_bound_at_T=str(mp.exp(-(280+mp.mpf('.5'))*arch.T)
                                        /((280+mp.mpf('.5'))**2*(1-mp.exp(-2*arch.T)))),
        initial_defect=H0,final_defect=rows[-1]['H'],
        smallest_prefix=min(rows,key=lambda r:r['H'])['q'],
        minimum_prefix_defect=min(r['H'] for r in rows),
        negative_increments=sum(r['increment']<0 for r in rows),
        positive_increments=sum(r['increment']>0 for r in rows),
        total_dispersion_credit=credit_sum,total_phase=phase_sum,
        recurrence_max_absolute_error=max_identity_error,
        dyadic_asymptotic_corner_coefficient=-4*((1+z)*mp.log(1+z)-z),
        blocks=blocks,refinements=refinements,exact_countermodels=exact_models(),
        RH_proved=False,global_sign_proved=False,
        guards_are_sufficient_not_necessary=True,
        universal_arithmetic_guard_proved=False,
    )
    out.mkdir(parents=True,exist_ok=True)
    (out/'compensation_diagnostics.json').write_text(json.dumps(fmt(result),ensure_ascii=False,indent=2)+'\n')
    with (out/'prime_power_increments.csv').open('w',newline='') as f:
        writer = csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow(fmt(row))
    print(json.dumps(fmt({k:v for k,v in result.items() if k not in ['exact_countermodels']}),
                     ensure_ascii=False,indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cutoff',type=int,default=1000)
    parser.add_argument('--digits',type=int,default=60)
    parser.add_argument('--output',type=Path,default=Path('results'))
    args = parser.parse_args()
    if not 35 <= args.digits <= 75:
        parser.error('140 exponential terms are chosen for 35..75 diagnostic digits')
    if args.cutoff < 4:
        parser.error('cutoff must be at least 4')
    run(args.cutoff,args.digits,args.output)
