#!/usr/bin/env python3
"""Directed-interval checks of the three-point guard, at a finite ceiling.

The bin assignment is exact integer arithmetic: n**P <= lo**(P-j)*hi**j.
Euler enclosure, exponential tail and root brackets are retained in JSON.
This certificate does not cover the uncomputed prime powers above the ceiling.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse
import json
import sys
import mpmath as mp
from compensation_blocks import prime_powers, Arch


def run(bound, corpus, out):
    sys.path.insert(0,str(corpus/'3_Preuves_et_calculs/src'))
    import prime_centered_bridge as pc
    import symbolic_weil_family as w
    pc.setup(400)
    iv = mp.iv
    I = pc.I
    n = 1024
    hn = sum((F(1,k) for k in range(1,n+1)),F(0))
    gu = I(hn)-iv.log(I(n))-I(F(1,2*n))+I(F(1,12*n*n))
    gamma_lower_rational = pc.lo(gu)-F(1,120*n**4)
    gamma_lower_directed = I(gamma_lower_rational)
    gamma = iv.mpf([w.mpq(pc.lo(gamma_lower_directed)),w.mpq(pc.hi(gu))])
    c0 = iv.log(8*iv.pi)+gamma+iv.pi/2
    total = iv.pi**2/4+2*iv.catalan
    T = iv.log(I(2))
    numeric = Arch()
    def A(t):
        s = sum((iv.exp(-I(F(2*k)+F(1,2))*t)/I((F(2*k)+F(1,2))**2)
                 for k in range(64)),I(0))
        b = F(257,2)
        tail = iv.exp(-I(b)*t)/(I(b*b)*(1-iv.exp(-2*t)))
        return 4*(iv.exp(t/2)+iv.exp(-t/2)-2)-c0*t/2+total-s-iv.mpf([0,w.mpq(pc.hi(tail))])
    def Ap(t):
        r = iv.exp(-t/2)
        return 2*(1/r-r)-c0/2+iv.log((1+r)/(1-r))/2+iv.atan2(r,I(1))
    apt = Ap(T)
    root_cache = {}
    root_witnesses = []
    def dual(C):
        key = tuple(map(tuple,C._mpi_))
        if key in root_cache:
            return root_cache[key]
        if pc.hi(C) <= pc.lo(apt):
            theta = T
            witness = dict(kind='boundary T',mass=pc.pack(C),position=pc.pack(theta))
        else:
            assert pc.lo(C) > pc.hi(apt)
            guess,_ = numeric.dual(w.mpq((pc.lo(C)+pc.hi(C))/2))
            radius = mp.mpf('1e-8')
            low,high = guess-radius,guess+radius
            assert pc.hi(Ap(low)-C)<0 and pc.lo(Ap(high)-C)>0
            for _ in range(60):
                middle = (low+high)/2
                v = Ap(middle)-C
                if pc.hi(v)<0:
                    low = middle
                elif pc.lo(v)>0:
                    high = middle
                else:
                    lm,hm = (low+middle)/2,(middle+high)/2
                    if pc.hi(Ap(lm)-C)<0 and pc.lo(Ap(hm)-C)>0:
                        low,high = lm,hm
                    else:
                        break
            assert pc.hi(Ap(low)-C)<0 and pc.lo(Ap(high)-C)>0
            theta = iv.mpf([low,high])
            witness = dict(kind='interior root',mass=pc.pack(C),position=pc.pack(theta),
                           left_residual=pc.pack(Ap(low)-C),right_residual=pc.pack(Ap(high)-C),
                           strict_bracket_verified=True)
        g = C*theta-A(theta)
        root_cache[key] = (theta,g)
        witness['dual_value'] = pc.pack(g)
        root_witnesses.append(witness)
        return theta,g
    rows = []
    C,L = I(0),I(0)
    _,g0 = dual(C)
    zero = dict(q=0,C=C,L=L,G=g0,H=-g0)
    for q,p,k in prime_powers(bound):
        c = iv.log(I(p))/iv.sqrt(I(q))
        C += c
        L += c*iv.log(I(q))
        rows.append(dict(q=q,C=C,L=L))
    def state(row):
        if 'H' not in row:
            theta,g = dual(row['C'])
            row.update(G=g,H=row['L']-g,theta=theta)
        return row
    first = state(rows[0])
    assert pc.lo(first['H'])>0
    def before(lo,hi,p,j):
        # log boundary = [(p-j)*log(lo)+j*log(hi)]/p.
        threshold = lo**(p-j)*hi**j
        picked = [r for r in rows if r['q']**p <= threshold]
        return state(picked[-1] if picked else zero)
    results = []
    for pieces in [1,8]:
        guards = []
        lo = 2
        while lo < bound:
            hi = min(2*lo,bound)
            al,bl = iv.log(I(lo)),iv.log(I(hi))
            for j in range(pieces):
                st = before(lo,hi,pieces,j)
                en = before(lo,hi,pieces,j+1)
                if st['q']==en['q']:
                    continue
                a = ((pieces-j)*al+j*bl)/pieces
                b = ((pieces-j-1)*al+(j+1)*bl)/pieces
                D,M = en['C']-st['C'],en['L']-st['L']
                dstar = (b*D-M)/(b-a)
                # The exact support constraints prove 0<=dstar<=D.
                dl,dh = max(F(0),pc.lo(dstar)),min(pc.hi(D),pc.hi(dstar))
                assert dl<=dh
                dstar = iv.mpf([w.mpq(dl),w.mpq(dh)])
                theta,gstar = dual(st['C']+dstar)
                K = st['H']+a*dstar-(gstar-st['G'])
                low = min(pc.lo(st['H']),pc.lo(en['H']),pc.lo(K))
                high = min(pc.hi(st['H']),pc.hi(en['H']),pc.hi(K))
                guard = iv.mpf([w.mpq(low),w.mpq(high)])
                guards.append(dict(integer_block=[lo,hi],subdivision=j+1,
                                   last_before=st['q'],last_after=en['q'],
                                   corner=pc.pack(K),guard=pc.pack(guard),
                                   guard_positive_certified=pc.lo(guard)>0,
                                   guard_negative_certified=pc.hi(guard)<0))
            lo=hi
        ml = min(pc.endpoint_q(tuple(g['guard']['binary'][0])) for g in guards)
        mu = min(pc.endpoint_q(tuple(g['guard']['binary'][1])) for g in guards)
        results.append(dict(parts_per_block=pieces,nonempty_parts=len(guards),
                            positive_count=sum(g['guard_positive_certified'] for g in guards),
                            negative_count=sum(g['guard_negative_certified'] for g in guards),
                            minimum_guard=pc.pack(iv.mpf([w.mpq(ml),w.mpq(mu)])),guards=guards))
    if bound==1000:
        assert results[0]['negative_count']==len(results[0]['guards'])
        assert results[1]['positive_count']==len(results[1]['guards'])
    result = dict(cutoff=bound,prefix_count=len(rows),first_prime_defect=pc.pack(first['H']),
                  model='mpmath.iv 400 bits; exact integer sieve/bin assignment; Euler remainder n=1024; geometric archimedean tail after 64 terms',
                  euler_gamma=pc.pack(gamma),results=results,
                  euler_lower_rational_exact=str(gamma_lower_rational),
                  gamma_lower_binary_not_above_rational=pc.lo(gamma)<=gamma_lower_rational,
                  archimedean_tail_at_T=pc.pack(iv.exp(-I(F(257,2))*T)/(I(F(257,2)**2)*(1-iv.exp(-2*T)))),
                  root_witnesses=root_witnesses,
                  finite_truncated_prefix_sign_certified=results[1]['positive_count']==len(results[1]['guards']),
                  original_signal_window='log(2) <= t <= log(cutoff)',
                  all_Weil_test_functions_certified=False,
                  global_original_sign_certified=False,RH_proved=False)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['results','root_witnesses']},ensure_ascii=False,indent=2))
    print('guard summary:',[(r['parts_per_block'],r['nonempty_parts'],r['positive_count'],r['negative_count'],r['minimum_guard']['midpoint']) for r in results])


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--cutoff',type=int,default=1000)
    parser.add_argument('--corpus',type=Path,default=Path('mini_corpus'))
    parser.add_argument('--output',type=Path,default=Path('results/block_guard_certificate.json'))
    args=parser.parse_args()
    if args.cutoff<4:
        parser.error('cutoff must be at least 4')
    run(args.cutoff,args.corpus,args.output)
