"""Validate the frozen Lego construction; keep inconclusive larger supports."""
from pathlib import Path
import sys,json,hashlib
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'3_Preuves_et_calculs/data';sys.path.insert(0,str(ROOT/'3_Preuves_et_calculs/src'))
import certificate_lego as l
import prime_centered_bridge as b
import symbolic_weil_family as w
def main():
    path=D/'v646_protocole_lego.json';p=json.loads(path.read_text());b.setup(p['interval_bits'])
    result=dict(version='V6.46',protocol_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),zero_data_used=False,
        status='interval-certified local templates; global sign still open',supports=[],complete=False)
    result['disjoint_localization']=l.local_disjoint_certificate(F(1,32))
    for s in p['supports']:
        S=F(s);print('Lego intervals S='+s,flush=True)
        layers=l.frequency_layers(S,p['layer_steps'],F(p['layer_step']),p['midpoint_subdivisions'],p['kernel_split'])
        port=l.Port(S);bricks=l.boundary_bricks(port,F(layers['lambda_lower']));certificate=l.assemble_local_certificate(*bricks)
        result['supports'].append(dict(S=s,layers=layers,boundary=bricks[1].payload,constants=bricks[2].payload,certificate=certificate))
        for row in result['supports']:
            for key in ['boundary','constants']:
                row[key]={k:str(v) if isinstance(v,F) else v for k,v in row[key].items()}
        (D/'v646_lego_resultats.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    positive=result['supports'][0];S=F(positive['S']);f=w.test(S,0);mass=w.mass(S,0,0)
    derivative=w.integral_even(w.mul(w.derivative(f),w.derivative(f)))/S
    weight=F(positive['constants']['weight_upper']);q_upper=F(131,8)*derivative/mass-F(25,6)+weight
    eta=F(q_upper.numerator//q_upper.denominator+2)
    shifted=l.assemble_local_certificate(*l.boundary_bricks(l.Port(S,form='Q_W_minus_eta_mass',mass_shift=eta),F(positive['layers']['lambda_lower']),eta))
    result['perturbed_negative_control']=dict(eta=str(eta),Q_original_witness_upper_per_mass=str(q_upper),
        shifted_witness_upper_per_mass=str(q_upper-eta),negative_witness_certified=q_upper-eta<0,
        certificate_response=shifted,scope='modified quadratic form only; never an RH counterexample')
    result['source_projection_example']=l.project_source_gram([[5,2],[2,2]],[[2,1]],[[1]])
    result['rounded_uniform_certificate']=l.rounded_certificate(*l.boundary_bricks(l.Port(S),F(positive['layers']['lambda_lower'])))
    result['complete']=True;(D/'v646_lego_resultats.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('complete; full local certificate',positive['certificate']['status'],'mass floor',float(F(positive['certificate']['mass_floor_lower'])),flush=True)
if __name__=='__main__':main()
