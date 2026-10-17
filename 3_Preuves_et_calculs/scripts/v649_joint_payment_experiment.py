from pathlib import Path
import sys,json,hashlib
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import multi_prime_compensation as c
import prime_centered_bridge as b

def main():
    b.setup(240)
    supports=['1/2','11/20','3/5','7/10','4/5','1','2']
    cases=[]
    for s in supports:
        x=c.joint_edge_payment(F(s));x['derivative_budgets']=c.derivative_budgets(s)
        separate=[c.joint_edge_payment(s,[q]) for q in x['active_q']]
        x['separate_alpha_sum_upper']=str(sum((F(z['alpha_upper']) for z in separate),F(0)))
        x['separate_alpha_sum_lower']=str(sum((F(z['alpha_lower']) for z in separate),F(0)))
        if s=='1':assert F(x['alpha_upper'])<F(796,1000) and F(x['separate_alpha_sum_lower'])>F(124,100)
        cases.append(x);print(s,x['active_q'],'joint',float(F(x['alpha_upper'])),'separate',float(F(x['separate_alpha_sum_upper'])),flush=True)
    near=[]
    d=b.hi(c.mp.iv.log(b.I(3)))
    for k in [2,4,8,16,32]:
        s=d/2+F(1,2**k);z=c.joint_edge_payment(s,[3]);near.append(dict(S=str(s),excess_width=str(2*s-d),alpha_upper=z['alpha_upper']))
    output=dict(version='V6.49',status='joint_arithmetic_payment_certified_only',
        source_sha256=hashlib.sha256((ROOT/'src/multi_prime_compensation.py').read_bytes()).hexdigest(),
        supports=cases,prime3_threshold_relative_payment=near,global_RH_claim=False,
        extended_positive_support_certificate=False)
    (ROOT/'data/v649_joint_payment_resultats.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
