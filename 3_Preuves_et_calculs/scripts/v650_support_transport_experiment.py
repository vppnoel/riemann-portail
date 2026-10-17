#!/usr/bin/env python3
"""Reproduce exact transport algebra and numerical examples, no sign theorem."""
import json, sys, math, hashlib
from pathlib import Path
from fractions import Fraction as F
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import support_transport as tr


def seed(S, odd=False):
    # (S²-x²)^3, optionally times x. k=k'=k''=0 at ±S.
    c = [S**6, 0, -3*S**4, 0, 3*S**2, 0, -1]
    return [F(v) for v in ([0]+c if odd else c)]


def run():
    S=F(1,2); rows=[]
    for odd in (False,True):
        k=seed(S,odd)
        for j in (0,1,2):
            for edge in (-S,S):
                assert tr.evaluate(tr.differentiate(k,j),edge)==0
        f=tr.apply_polar_constructor(k)
        m0=quad(lambda x:float(tr.evaluate(f,x))**2,-float(S),float(S),epsabs=1e-12)[0]
        for r in map(F,['3/4','11/10','2']):
            coefficients=tr.transported_seed_coefficients(k,r)
            scale=float(r)**-.5
            value=lambda x:scale*float(tr.evaluate(coefficients,x))
            edge=float(r*S)
            moments=[quad(lambda x: value(x)*math.exp(sign*x/2),-edge,edge,epsabs=1e-12)[0] for sign in (-1,1)]
            mass=quad(lambda x:value(x)**2,-edge,edge,epsabs=1e-12)[0]
            assert max(map(abs,moments))<1e-11
            bounds=tr.transport_bounds(r)
            assert float(F(bounds['mass_lower']))*m0-1e-12 <= mass <= float(F(bounds['mass_upper']))*m0+1e-12
            # Independent exact identity D_r P_r = r² P_1 D_r,
            # after canceling the common factor r^-1/2.
            dilated=[c/r**j for j,c in enumerate(k)]
            right=[r*r*c for c in tr.apply_polar_constructor(dilated)]
            assert coefficients==right
            rows.append(dict(parity='odd' if odd else 'even',ratio=str(r),
                support=str(r*S),moments_float=moments,mass_ratio_float=mass/m0,
                exact_conjugacy=True,bounds=bounds))
    out=dict(version='V6.50',provenance='new reconstruction after recovery of V6.49',
             analytic_proof='V650_RECUPERATION_TRANSPORT_ET_RH.md',
             numerical_examples_certified=False, exact_rational_conjugacy_checked=True,
             global_RH_claim=False,new_positive_certificate=False,
             zero_data_used=False,examples=rows,
             source_sha256=hashlib.sha256((ROOT/'src/support_transport.py').read_bytes()).hexdigest())
    p=ROOT/'data/v650_support_transport_resultats.json'
    p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print('6 examples; exact rational conjugacy; moments and mass are floating diagnostics; no Q sign claim')


if __name__=='__main__': run()
