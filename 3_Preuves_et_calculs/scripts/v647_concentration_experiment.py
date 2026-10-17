"""Execute the frozen joint-frequency concentration certificate."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,time
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'3_Preuves_et_calculs/data'
sys.path.insert(0,str(ROOT/'3_Preuves_et_calculs/src'))
import prime_centered_bridge as b
import projected_concentration as c
from certificate_lego import Port

def main():
    source=D/'v647_protocole_concentration.json';p=json.loads(source.read_text());b.setup(p['interval_bits'])
    start=time.monotonic()
    print('V647 frozen outward certificate S='+p['support'],flush=True)
    result=c.certify(Port(F(p['support'])),F(p['frequency_cutoff']),F(p['frequency_step']),
        F(p['value_cutoff']),F(p['value_step']),p['fixed_bits'],lambda s:print(s,flush=True))
    out=dict(version='V6.47',protocol_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        complete=True,global_RH_claim=False,certificate=result,elapsed_seconds=time.monotonic()-start,
        evaluation='analytic proof templates + outward intervals + exact fixed point; no formal proof assistant')
    (D/'v647_concentration_resultats.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(result['status'],'mass floor',float(F(result['mass_floor_lower'])),
        'trace only',float(F(result['trace_only_mass_floor'])),
        'R floor',float(F(result['mu_R_lower'])) if result['mu_R_lower'] else None,flush=True)

if __name__=='__main__':main()
