"""Prototype fini : droites premières et dual convexe archimédien.

N'utilise aucun zéro. Les fractions et intervalles encadrent les minima des
droites préfixes présentes. La positivité de préfixes finis ne prouve pas RH.
Les calculs sont conditionnés au modèle d'arrondi mpmath.iv déclaré.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse
import json
import sys
import mpmath as mp

ap=argparse.ArgumentParser()
ap.add_argument('--corpus',type=Path,required=True)
ap.add_argument('--cutoff',type=int,default=1000)
ap.add_argument('--output',type=Path,required=True)
args=ap.parse_args()
sys.path.insert(0,str(args.corpus/'3_Preuves_et_calculs/src'))
import prime_centered_bridge as pc
import symbolic_weil_family as w

pc.setup(400)
K=64
n=1024
hn=sum((F(1,k) for k in range(1,n+1)),F(0))
gamma_up=pc.I(hn)-mp.iv.log(pc.I(n))-pc.I(F(1,2*n))+pc.I(F(1,12*n*n))
gamma=mp.iv.mpf([w.mpq(pc.lo(pc.I(pc.lo(gamma_up)-F(1,120*n**4)))),w.mpq(pc.hi(gamma_up))])
c0=mp.iv.log(8*mp.iv.pi)+gamma+mp.iv.pi/2
tail_total=mp.iv.pi**2/4+2*mp.iv.catalan
T=mp.iv.log(pc.I(2))

def A(t):
    t=mp.iv.mpf(t)
    series=sum((mp.iv.exp(-pc.I(F(2*k)+F(1,2))*t)/pc.I((F(2*k)+F(1,2))**2)
                for k in range(K)),pc.I(0))
    b=F(2*K)+F(1,2)
    tail=mp.iv.exp(-pc.I(b)*t)/(pc.I(b*b)*(1-mp.iv.exp(-2*t)))
    exp_tail=series+mp.iv.mpf([0,w.mpq(pc.hi(tail))])
    return 4*(mp.iv.exp(t/2)+mp.iv.exp(-t/2)-2)-c0*t/2+tail_total-exp_tail

def A_prime(t):
    t=mp.iv.mpf(t);r=mp.iv.exp(-t/2)
    J=mp.iv.log((1+r)/(1-r))/2+mp.iv.atan2(r,pc.I(1))
    return 2*(mp.iv.exp(t/2)-mp.iv.exp(-t/2))-c0/2+J

def numeric_prime(t):
    r=mp.exp(-t/2)
    return 2*(mp.exp(t/2)-mp.exp(-t/2))-(mp.log(8*mp.pi)+mp.euler+mp.pi/2)/2+mp.atanh(r)+mp.atan(r)

rows=[];C=pc.I(0);L=pc.I(0)
powers=[None]+w.prime_powers(args.cutoff)
for item in powers:
    if item is not None:
        p,j,q=item;d=mp.iv.log(pc.I(q));c=mp.iv.log(pc.I(p))/mp.iv.sqrt(pc.I(q))
        C+=c;L+=c*d
    if pc.hi(C)<=pc.lo(A_prime(T)):
        position=T;kind='bord T=log2'
    else:
        assert pc.lo(C)>pc.hi(A_prime(T))
        Cnum=w.mpq((pc.lo(C)+pc.hi(C))/2)
        guess=2*mp.log((Cnum+mp.mpf('2.7'))/2)
        root=mp.findroot(lambda t:numeric_prime(t)-Cnum,(max(mp.log(2),guess-.1),guess+.1))
        delta=mp.mpf(2)**-30
        low=w.mpq(F(str(root-delta)));high=w.mpq(F(str(root+delta)))
        assert pc.hi(A_prime(low)-C)<0 and pc.lo(A_prime(high)-C)>0
        for _ in range(38):
            mid=(low+high)/2;diff=A_prime(mid)-C
            if pc.hi(diff)<0:low=mid
            elif pc.lo(diff)>0:high=mid
            else:break
        assert pc.hi(A_prime(low)-C)<0 and pc.lo(A_prime(high)-C)>0
        position=mp.iv.mpf([low,high]);kind='unique racine A_prime=C'
    defect=A(position)-C*position+L
    assert pc.lo(defect)>0,('préfixe non certifié',item,pc.pack(defect))
    rows.append(dict(last_prime_power=item,weighted_mass=pc.pack(C),log_moment=pc.pack(L),
                     minimizer=pc.pack(position),minimizer_kind=kind,fenchel_defect=pc.pack(defect),
                     finite_prefix_positive=True))

smallest=min(rows,key=lambda r:pc.endpoint_q(tuple(r['fenchel_defect']['binary'][0])))
result=dict(source='Suzuki 2023/2025; Fenchel reconstruction',cutoff=args.cutoff,
            prefix_count=len(rows),signal_domain_certified='log2 <= t <= log(cutoff)',
            all_selected_prefix_lines_below_arch_curve=True,
            smallest_midpoint_defect=smallest['fenchel_defect']['midpoint'],
            smallest_lower_defect=str(pc.endpoint_q(tuple(smallest['fenchel_defect']['binary'][0]))),
            smallest_prefix=smallest['last_prime_power'],
            arithmetic_model='exact rational sieve, mpmath.iv 400 bits, Euler remainder, geometric tail',
            RH_proved=False,universal_prefix_law_proved=False,rows=rows)
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Préfixes encadrés:',len(rows),'plafond entier:',args.cutoff)
print('Plus petite marge affichée:',smallest['fenchel_defect']['midpoint'])
print('Portée : intervalle fini du signal, pas positivité universelle de Weil.')
