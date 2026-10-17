#!/usr/bin/env python3
"""Adaptive endpoint-to-interval sign certificates for the actual scalar Suzuki signal.

Uses existing corpus interval primitives and exact sieve, without zeta zeros.
Certifies only the declared finite scalar window, not all Weil test functions.
Run from any directory: python certifier_resolution.py [--cutoff 1000].
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,sys
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'3_Preuves_et_calculs/src'))
sys.path.insert(0,str(ROOT/'3_Preuves_et_calculs/recherche79'))
import prime_centered_bridge as pc
import symbolic_weil_family as w
from compensation_blocks import prime_powers

def run(cutoff=1000):
 pc.setup(240);iv=mp.iv;I=pc.I
 n=1024;h=sum((F(1,k) for k in range(1,n+1)),F(0))
 gu=I(h)-iv.log(I(n))-I(F(1,2*n))+I(F(1,12*n*n))
 gamma=iv.mpf([w.mpq(pc.lo(I(pc.lo(gu)-F(1,120*n**4)))),w.mpq(pc.hi(gu))])
 kappa=iv.log(8*iv.pi)+gamma+iv.pi/2
 total=iv.pi**2/4+2*iv.catalan
 t0,t1=iv.log(I(2)),iv.log(I(cutoff));span=t1-t0
 atoms=[(q,iv.log(I(q)),iv.log(I(p))/iv.sqrt(I(q))) for q,p,k in prime_powers(cutoff)]
 assert pc.hi(t1)<pc.lo(iv.log(I(cutoff+1)))
 def A(t):
  z=iv.exp(-2*t);s=I(0)
  for k in reversed(range(64)):s=s*z+I(1/F(2*k+F(1,2))**2)
  b=F(257,2);tail=iv.exp(-I(b)*t)/(I(b*b)*(1-iv.exp(-2*t)))
  return 4*(iv.exp(t/2)+iv.exp(-t/2)-2)-kappa*t/2+total-iv.exp(-t/2)*s-iv.mpf([0,w.mpq(pc.hi(tail))])
 cache={}
 def endpoint(u):
  u=F(u)
  if u not in cache:
   t=t0+I(u)*span;s=A(t)
   for q,x,c in atoms:
    d=t-x
    if pc.hi(d)>0:
     hinge=iv.mpf([w.mpq(max(F(0),pc.lo(d))),w.mpq(max(F(0),pc.hi(d)))])
     s-=c*hinge
   cache[u]=(t,s)
  return cache[u]
 def guard(a,b):
  ta,sa=endpoint(a);tb,sb=endpoint(b)
  width=pc.hi(tb-ta);curv=pc.hi(iv.exp(tb/2))
  margin=min(pc.lo(sa),pc.lo(sb));debt=curv*width**2/8
  return margin-debt,margin,debt,curv,width
 uniform=[]
 for pieces in [8,16,32,64,128,256]:
  g=[guard(F(j,pieces),F(j+1,pieces))[0] for j in range(pieces)]
  uniform.append(dict(endpoint_minimum_lower_float=float(min(pc.lo(endpoint(F(j,pieces))[1]) for j in range(pieces+1))),intervals=pieces,positive_intervals=sum(v>0 for v in g),inconclusive_intervals=sum(v<=0 for v in g),minimum_sufficient_bound=str(min(g)),minimum_sufficient_bound_float=float(min(g))))
 uniform_endpoint_evaluations=len(cache);cache.clear()
 # Independent adaptive run; comparison-grid values are not reused.
 accepted=[];unresolved=[];attempts=0;negative=[]
 def split(a,b,depth):
  nonlocal attempts
  attempts+=1;g,m,d,B,width=guard(a,b)
  if g>0:
   accepted.append(dict(u_a=str(a),u_b=str(b),t_a=pc.pack(endpoint(a)[0]),t_b=pc.pack(endpoint(b)[0]),S_a=pc.pack(endpoint(a)[1]),S_b=pc.pack(endpoint(b)[1]),lower_bound_exact=str(g),lower_bound_float=float(g),endpoint_margin_exact=str(m),curvature_debt_exact=str(d),B_upper_exact=str(B),width_upper_exact=str(width),depth=depth))
  elif pc.hi(endpoint(a)[1])<0 or pc.hi(endpoint(b)[1])<0:
   negative.append([str(a),str(b)])
  elif depth<20:split(a,(a+b)/2,depth+1);split((a+b)/2,b,depth+1)
  else:unresolved.append([str(a),str(b)])
 split(F(0),F(1),0)
 accepted.sort(key=lambda r:F(r['u_a']))
 if not unresolved and not negative:
  assert F(accepted[0]['u_a'])==0 and F(accepted[-1]['u_b'])==1
  assert all(x['u_b']==y['u_a'] for x,y in zip(accepted,accepted[1:]))
  assert all(F(row['lower_bound_exact'])>0 for row in accepted)
 result=dict(version='V6.57',cutoff=cutoff,window='log(2) <= t <= log(cutoff)',scalar_signal='A(t) - sum_(p^k <= exp(t)) log(p)/sqrt(p^k)*(t-log(p^k))',prime_power_count=len(atoms),precision_bits=iv.prec,arch_tail_terms=64,euler_harmonic_n=n,uniform_grid_comparison=uniform,uniform_endpoint_evaluations=uniform_endpoint_evaluations,adaptive_intervals=len(accepted),adaptive_attempts=attempts,adaptive_evaluated_endpoints=len(set([r['u_a'] for r in accepted]+[r['u_b'] for r in accepted])),adaptive_minimum_bound=min(r['lower_bound_float'] for r in accepted),leaves=accepted,unresolved=unresolved,negative_witnesses=negative,uniform_lower_bound_one_thousandth_certified=not unresolved and not negative and all(F(r['lower_bound_exact'])>F(1,1000) for r in accepted),finite_scalar_window_certified=not unresolved and not negative,all_Weil_tests_on_support_certified=False,global_scalar_sign_certified=False,RH_proved=False,limitations=['Same finite scalar window already covered in document79; new adaptive representation, no new global range.','Negative sufficient bounds are inconclusive, not negative signal values.','Mpmath interval arithmetic and existing corpus gamma/archimedean tail enclosures are trusted primitives; binary endpoint/rational guards retained.'])
 out=Path(__file__).with_name('resolution_resultats.json');out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ['leaves']},ensure_ascii=False,indent=2))
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--cutoff',type=int,default=1000);a=p.parse_args()
 if a.cutoff<3:p.error('cutoff >=3 required')
 run(a.cutoff)
