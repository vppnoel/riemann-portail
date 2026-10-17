"""Post-decomposition directions: interval sign for fluctuation, exploratory arch/full."""
from pathlib import Path
import sys,json
from fractions import Fraction as F
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'3_Preuves_et_calculs/data';sys.path.insert(0,str(ROOT/'3_Preuves_et_calculs/src'))
import prime_centered_bridge as b
import symbolic_weil_family as w
def main():
    r=json.loads((D/'v645_arithmetique_resultats.json').read_text());old=json.loads((D/'v644_family_resultats.json').read_text());b.setup(400)
    for row,v644 in zip(r['supports'],old['supports']):
        S=F(row['S']);a=v644['precisions'][-1];A=mp.matrix(a['arch']);B=mp.matrix(a['B']);G=mp.matrix(a['G'])
        P0=mp.matrix([[w.mpq(b.seed_energy(S,i,j)) for j in range(8)] for i in range(8)]);L=mp.cholesky(B);inv=L**-1;Z=inv*(A+P0)*inv.T;Z=(Z+Z.T)/2
        ev,V=mp.eigsy(Z);c=inv.T*V[:,0];rat=[F(mp.nstr(x,40)) for x in c];cc=mp.matrix([w.mpq(x) for x in rat]);Bexact=sum((rat[i]*rat[j]*w.metric(S,i,j) for i in range(8) for j in range(8)),F(0));fl=b.I(0)
        for item in row['entries']:
            i,j=item['i'],item['j'];iv=mp.iv.mpf([mp.mpf(tuple(t)) for t in item['residual']['binary']]);fl-=b.I(rat[i]*rat[j]*(1 if i==j else 2))*iv/b.I(Bexact)
        row['compensating_direction']=dict(scope='analysis after matrix decomposition; vector proposed by exploratory base eigenvector',
            coefficients_exact=[str(x) for x in rat],H1_mass_exact=str(Bexact),
            base_quotient_exploratory=mp.nstr(((cc.T*(A+P0)*cc)[0])/w.mpq(Bexact),20),
            fluctuation_quotient_interval=b.pack(fl),
            fluctuation_sign_certified='positive' if b.lo(fl)>0 else 'negative' if b.hi(fl)<0 else 'undetermined',
            full_quotient_exploratory=mp.nstr(((cc.T*G*cc)[0])/w.mpq(Bexact),20),
            full_sign_interval_certified=False)
    (D/'v645_arithmetique_resultats.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    for row in r['supports']:
        x=row['compensating_direction'];print(row['S'],'base',x['base_quotient_exploratory'],'fluctuation',x['fluctuation_quotient_interval']['midpoint'],'full exploratory',x['full_quotient_exploratory'])
if __name__=='__main__':main()
