"""Exact integer parameters for the proved, deliberately very coarse tail gate."""
from pathlib import Path
import json,sys
from fractions import Fraction as F
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'3_Preuves_et_calculs/data'
def main():
    data=json.loads((D/'v644_family_resultats.json').read_text());out=[]
    with mp.workdps(80):
      for row in data['supports']:
        S=F(row['S']);M=row['prime_power_count'];L=8+2*M;J=8*L;T=1<<J
        z=6*S*T;q=-(-z.numerator//z.denominator)
        assert q>=1 and F(q)>=6*S*T and J>=2 and T%4==0
        out.append(dict(S=str(S),prime_power_count=M,L_upper=L,J=J,T_expression='2^'+str(J),
            q=str(q),q_decimal_digits=len(str(q)),q_expression='ceil(6*S*2^J)',
            epsilon_upper='1/2',r_lower=1+2*L,eta_upper=str(F(2*L,1+2*L)),
            coercivity_lower=str(F(1,1+2*L)),
            status='proved integer tail contract; head dimension q; no head/Schur solved'))
        low,high=row['precisions'];err=max(abs(mp.mpf(a['lambda_min'])-mp.mpf(b['lambda_min'])) for a,b in zip(low['prefixes'],high['prefixes']))
        de=max(abs(mp.mpf(a['normalized_last_schur_debt'])-mp.mpf(b['normalized_last_schur_debt'])) for a,b in zip(low['prefixes'],high['prefixes']))
        assert err<mp.mpf('1e-25') and de<mp.mpf('1e-25')
        row['precision_absolute_eigen_min_difference']=mp.nstr(err,30)
        row['precision_absolute_schur_ratio_difference']=mp.nstr(de,30)
    (D/'v644_family_resultats.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    (D/'v644_contrats_queue_entiers.json').write_text(json.dumps(dict(version='V6.44',
        scope='Explicit analytic corollary after metric construction; not predeclared eigen experiment',contracts=out),ensure_ascii=False,indent=2)+'\n')
    for r in out:print(r['S'],'M',r['prime_power_count'],'T',r['T_expression'],'head q:',r['q_decimal_digits'],'decimal digits; margin ≥',r['coercivity_lower'])
if __name__=='__main__':main()
