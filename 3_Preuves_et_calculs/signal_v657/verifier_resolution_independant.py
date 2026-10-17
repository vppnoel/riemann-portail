from pathlib import Path
from fractions import Fraction as F
import json,mpmath as mp
p=Path(__file__).with_name('resolution_resultats.json')
r=json.loads(p.read_text());mp.iv.prec=320;iv=mp.iv

def I(x):
 x=F(x);return iv.mpf(x.numerator)/x.denominator

def Q(t):
 sign,man,exp,bc=t;assert bc>=0
 return F((-1 if sign else 1)*man)*F(2)**exp

def lo(v):return Q(v._mpi_[0])
def hi(v):return Q(v._mpi_[1])
def primes_power(n):
 for q in range(2,n+1):
  for d in range(2,int(q**.5)+1):
   if q%d==0:break
  else:d=q
  m=q
  while m%d==0:m//=d
  if m==1:yield q,d
atoms=[(q,iv.log(I(q)),iv.log(I(d))/iv.sqrt(I(q))) for q,d in primes_power(r['cutoff'])]
assert len(atoms)==r['prime_power_count']
t0=iv.log(I(2));t1=iv.log(I(r['cutoff']));span=t1-t0
kappa=iv.log(8*iv.pi)+iv.euler+iv.pi/2
total=iv.pi**2/4+2*iv.catalan
cache={}
def S(u):
 u=F(u)
 if u not in cache:
  t=t0+I(u)*span
  # Independent forward summation, same explicit tail bound.
  rem=iv.exp(-I(F(257,2))*t)/(I(F(257,2)**2)*(1-iv.exp(-2*t)))
  a=4*(iv.exp(t/2)+iv.exp(-t/2)-2)-kappa*t/2+total
  a-=sum((iv.exp(-I(F(2*k)+F(1,2))*t)/I((F(2*k)+F(1,2))**2) for k in range(64)),I(0))
  a-=iv.mpf([0,hi(rem).numerator])/hi(rem).denominator
  for q,x,c in atoms:
   z=t-x
   a-=c*iv.mpf([I(max(F(0),lo(z))),I(max(F(0),hi(z)))])
  cache[u]=(t,a)
 return cache[u]
accepted=r['leaves'];accepted.sort(key=lambda z:F(z['u_a']))
assert F(accepted[0]['u_a'])==0 and F(accepted[-1]['u_b'])==1
assert all(F(a['u_b'])==F(b['u_a']) for a,b in zip(accepted,accepted[1:]))
smallest=None
for row in accepted:
 ta,sa=S(row['u_a']);tb,sb=S(row['u_b'])
 for key,v in [('S_a',sa),('S_b',sb)]:
  ll,uu=map(Q,row[key]['binary']);assert ll<=lo(v)<=hi(v)<=uu
 m=F(row['endpoint_margin_exact']);B=F(row['B_upper_exact']);w=F(row['width_upper_exact']);g=F(row['lower_bound_exact'])
 assert m<=lo(sa) and m<=lo(sb)
 assert hi(iv.exp(tb/2))<=B
 assert hi(I(F(row['u_b'])-F(row['u_a']))*span)<=w
 assert g==m-B*w*w/8
 assert g>0
 if r.get('uniform_lower_bound_one_thousandth_certified'):assert g>F(1,1000)
 smallest=g if smallest is None else min(g,smallest)
print('Independent 320-bit check passed:',len(accepted),'cells,',len(cache),'points; min bound',float(smallest),'sourcepointenclosuresallcontainindependentbounds; zero unresolved=',not r['unresolved'])
