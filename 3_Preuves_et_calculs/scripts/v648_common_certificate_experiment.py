"""Execute the frozen common-operator certificate and its complete budgets."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,time
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'3_Preuves_et_calculs/data'
sys.path.insert(0,str(ROOT/'3_Preuves_et_calculs/src'))
import common_operator_certificate as c
import prime_centered_bridge as b
from certificate_lego import Port
def main():
    path=D/'v648_protocole_operateur_commun.json';p=json.loads(path.read_text());b.setup(p['interval_bits']);start=time.monotonic()
    result=c.certify(Port(F(p['S'])),F(p['T']),F(p['U']),F(p['frequency_step']),F(p['joint_table_step']),
        p['spatial_gauss_nodes'],p['kernel_split'],p['fixed_bits'],lambda s:print(s,flush=True))
    out=dict(version='V6.48',protocol_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        source_sha256=hashlib.sha256((ROOT/'3_Preuves_et_calculs/src/common_operator_certificate.py').read_bytes()).hexdigest(),complete=True,
        global_RH_claim=False,certificate=result,elapsed_seconds=time.monotonic()-start)
    (D/'v648_common_certificate_resultats.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print('Status',result['status'],'mass',float(F(result['mass_floor_lower'])),'R',float(F(result['mu_R_lower'])) if result['mu_R_lower'] else None,flush=True)
if __name__=='__main__':main()
