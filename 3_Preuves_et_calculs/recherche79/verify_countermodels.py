#!/usr/bin/env python3
"""Exact rational checks of the global exponential-reservoir countermodel.

All inequalities below use Fraction and Taylor/geometric remainders; no
floating-point exponential is used. The global proof is strong convexity on
each of the three intervals, as explained in document 79.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import argparse
import json


def exp_bounds(x,N=12):
    assert x>=0 and x<N+2
    low=sum((x**k/F(factorial(k)) for k in range(N+1)),F(0))
    tail=x**(N+1)/F(factorial(N+1))/(1-x/F(N+2))
    return low,low+tail


def run(out):
    requests=[('e2_upper',F(2),None,F(37,5)),
              ('e1p5_interval',F(3,2),F(22,5),F(9,2)),
              ('e1p2_lower',F(6,5),F(3),None),
              ('e2p4_lower',F(12,5),F(10),None),
              ('e2p5_interval',F(5,2),F(12),F(123,10))]
    checks=[]
    for label,x,required_l,required_u in requests:
        l,u=exp_bounds(x)
        passed=((required_l is None or l>required_l)
                and (required_u is None or u<required_u))
        assert passed
        checks.append(dict(label=label,argument=str(x),lower_rational=str(l),upper_rational=str(u),
                           required_lower=None if required_l is None else str(required_l),
                           required_upper=None if required_u is None else str(required_u),passed=True))
    middle=F(68,25)-F(16,5)**2/(2*F(72,5))
    final=F(1608,25)-F(104,5)**2/F(192)
    assert middle==F(532,225)>0
    assert final==F(931,15)>0
    assert 4*F(37,5)-F(156,5)==F(-8,5)
    result=dict(exponential_bounds=checks,
                Q_interval_12over5_to24over5_lower=str(middle),
                Q_interval_24over5_to_infinity_lower=str(final),
                Z_at4_upper_strict='-8/5',
                status='exact rational Taylor bounds, no floating-point dependence',
                artificial_demand=True,RH_counterexample=False)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Exact bounds passed; Q>=532/225 then Q>=931/15, Z(4)<-8/5.')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path('results/countermodels_exact.json'))
    run(parser.parse_args().output)
