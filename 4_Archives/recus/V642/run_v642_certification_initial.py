"""Frozen interval validation of one fold, its contour and four nearby roots."""
from pathlib import Path
from fractions import Fraction
from datetime import datetime,timezone
import json
import sys
import mpmath as mp

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from v642_intervalles import (IntervalFamily,lower,upper,interval,point,serial,
    magnitude,rounded_midpoint,rational_inverse,contraction_certificate)
from v639_contraintes import enclosure

def load(name):return json.loads((ROOT/'data'/name).read_text(encoding='utf-8-sig'))
def encode_certificate(c):
    return {k:([serial(x,24) for x in v] if k in ('K_intervals','box_intervals') else
      serial(v,24) if k=='jacobian_determinant' else
      [[str(x) for x in row] for row in v] if k=='preconditioner' else
      [[serial(x,24) for x in row] for row in v] if k=='remainder_matrix' else v) for k,v in c.items()}

def fold_stage(family,p):
    centre=[Fraction(p['centre_r']),Fraction(p['centre_t'])];half=Fraction(p['fold_box_halfwidth']);box=[interval(c-half,c+half) for c in centre]
    attempts=[];accepted=None
    for ore,oim in p['omega_candidates']:
        omega=mp.iv.mpc(ore,oim);at=family.critical_system(point(centre[0]),point(centre[1]),omega);whole=family.critical_system(*box,omega)
        C=rational_inverse(at['jacobian'],p['preconditioner_quantization_digits']);cert=contraction_certificate(centre,half,at['values'],whole['jacobian'],C)
        projection=whole['anchor_projection'];nonzero=lower(projection)>0 or upper(projection)<0
        transverse=all(lower(whole[k])>0 or upper(whole[k])<0 for k in ('H_r','H_tt'))
        cert['accepted']=cert['accepted'] and nonzero and transverse
        rec=dict(digits=family.digits,N=family.N,M=family.M,omega=[ore,oim],certificate=encode_certificate(cert),anchor_projection=serial(projection,24),H_r=serial(whole['H_r'],24),H_tt=serial(whole['H_tt'],24),phase_factor_nonzero=nonzero,transverse=transverse,point_values=[serial(v,24) for v in at['values']],jacobian=[[serial(v,24) for v in row] for row in whole['jacobian']],remainder_bounds=[[serial(x,40) for x in b] for b in family.remainders])
        if transverse:rec['kappa']=serial(-2*whole['H_r']/whole['H_tt'],18)
        attempts.append(rec)
        print('FOLD',family.digits,'omega',ore,oim,'accepted',cert['accepted'],flush=True)
        if cert['accepted']:accepted=cert;break
    return attempts,accepted

def contour_stage(family,p):
    r0=Fraction(p['centre_r']);t0=Fraction(p['centre_t']);R=Fraction(p['contour_radius']);wide=Fraction(p['radius_offset'])+Fraction(p['fold_box_halfwidth']);rspan=interval(r0-wide,r0+wide)
    central=family.function_jet(point(r0),mp.iv.mpc(point(Fraction(1,2)),point(t0)),2)
    alpha=mp.iv.mpc(point(rounded_midpoint(-central[2].real/2,12)),point(rounded_midpoint(-central[2].imag/2,12)))
    alpha_mod=mp.iv.sqrt(alpha.real**2+alpha.imag**2);q_lower=lower(alpha_mod*point(R)**2)
    if q_lower<=0:raise ValueError('Degenerate comparison polynomial')
    rectangle=mp.iv.mpc(interval(Fraction(1,2)-R,Fraction(1,2)+R),interval(t0-R,t0+R))
    global_jet=family.function_jet(rspan,rectangle,2)
    B2=magnitude(global_jet[2])+2*alpha_mod
    attempts=[]
    for grid in p['contour_grids']:
        distance=2*point(R)*mp.iv.sin(mp.iv.pi/(2*grid));rows=[]
        for j in range(grid):
            theta=mp.iv.pi*point(Fraction(2*j+1,grid))
            v=point(R)*mp.iv.mpc(mp.iv.cos(theta),mp.iv.sin(theta));w=point(t0)+v;s=point(Fraction(1,2))+mp.iv.mpc(0,1)*w
            f=family.function_jet(rspan,s,1)
            g0=f[0]-alpha*v*v;g1=mp.iv.mpc(0,1)*f[1]-2*alpha*v
            bound=magnitude(g0)+magnitude(g1)*distance+B2*distance**2/2
            passed=upper(bound)<q_lower
            rows.append({'arc':j,'defect_upper':str(upper(bound)),'strict_margin_lower':str(q_lower-upper(bound)),'accepted':passed})
            if (j+1)%64==0:print('CONTOUR',grid,j+1,'/',grid,flush=True)
        accepted=all(r['accepted'] for r in rows)
        attempts.append({'grid':grid,'accepted':accepted,'arcs':rows,'maximum_defect_upper':str(max(Fraction(r['defect_upper']) for r in rows)),'minimum_margin_lower':str(min(Fraction(r['strict_margin_lower']) for r in rows))})
        print('ROUCHE',grid,accepted,flush=True)
        if accepted:break
    return {'r_parameter_span':serial(rspan,24),'height_centre':str(t0),'radius':str(R),'alpha':serial(alpha,24),'comparison_modulus_lower':str(q_lower),'global_second_derivative_bound':serial(B2,24),'arc_attempts':attempts,'accepted':any(a['accepted'] for a in attempts),'zero_count_if_accepted':2,'continuous_contour_coverage':True}

def root_stage(family,p,fold):
    result=[];rbox=enclosure(fold['K_intervals'][0],p['fold_parameter_enclosure_digits']);rl,rh=Fraction(rbox['lower']),Fraction(rbox['upper']);half=Fraction(p['root_box_halfwidth'])
    for seed in p['root_seeds']:
        h=Fraction(seed['offset']);rspan=interval(rl+h,rh+h)
        centre=[Fraction(seed['beta_mp']),Fraction(seed['gamma_mp'])]
        centre=[rounded_midpoint(point(x),12) for x in centre]
        if h<0:assert centre[0]==Fraction(1,2),'Critical seed does not round to exact centre 1/2'
        s0=mp.iv.mpc(point(centre[0]),point(centre[1]));sbox=mp.iv.mpc(interval(centre[0]-half,centre[0]+half),interval(centre[1]-half,centre[1]+half))
        value,derivative=family.function_jet(rspan,s0,1);whole=family.function_jet(rspan,sbox,1)[1]
        J=[[whole.real,-whole.imag],[whole.imag,whole.real]];atJ=[[derivative.real,-derivative.imag],[derivative.imag,derivative.real]]
        C=rational_inverse(atJ,12);cert=contraction_certificate(centre,half,[value.real,value.imag],J,C)
        classification='critical_by_uniqueness_and_FE' if h<0 else 'off_critical_box'
        line_excluded=upper(sbox.real)<Fraction(1,2) or lower(sbox.real)>Fraction(1,2)
        inside=(abs(centre[0]-Fraction(1,2))+half)**2+(abs(centre[1]-Fraction(p['centre_t']))+half)**2<Fraction(p['contour_radius'])**2
        rec={'offset':str(h),'root_index':seed['root_index'],'centre':[str(x) for x in centre],'parameter_span':serial(rspan,24),'certificate':encode_certificate(cert),'classification':classification,'box_invariant_under_functional_partner':centre[0]==Fraction(1,2),'critical_line_excluded':line_excluded,'box_inside_contour':inside,'uniform_in_parameter':True}
        rec['accepted']=cert['accepted'] and inside and (centre[0]==Fraction(1,2) if h<0 else line_excluded)
        result.append(rec);print('ROOT',str(h),seed['root_index'],rec['accepted'],flush=True)
    for i,a in enumerate(result):
        for b in result[i+1:]:
            if a['offset']==b['offset']:assert any(abs(Fraction(x)-Fraction(y))>2*half for x,y in zip(a['centre'],b['centre'])),'Root boxes overlap'
    return result

def main():
    import hashlib
    D=ROOT/'data';p=load('v642_protocole_verrouille.json');path=D/'v642_certification.json'
    if path.exists():raise RuntimeError('Move existing output on a copy before replaying')
    for name,digest in p['input_hashes'].items():assert hashlib.sha256((D/name).read_bytes()).hexdigest()==digest,name
    pair=next(x for x in load('v639_couples_fixes.json')['pairs'] if x['id']==p['pair_id'])
    output={'version':'V6.42','execution_started_utc':datetime.now(timezone.utc).isoformat(),'protocol':'v642_protocole_verrouille.json','fold_id':p['fold_id'],'fold_attempts':[],'backend':'mpmath 1.3.0 iv elementary real primitives; explicit complex rectangular arithmetic; analytic EM/Cauchy remainder','independent_backend_verification':False,'global_RH_implication':False}
    fold=None;family=None
    for plan in p['precisions']:
        family=IntervalFamily(pair,p['side'],**plan);attempts,fold=fold_stage(family,p);output['fold_attempts']+=attempts
        (D/'v642_checkpoint.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    output['fold_certified']=all(any(a['certificate']['accepted'] for a in output['fold_attempts'] if a['digits']==plan['digits']) for plan in p['precisions'])
    if output['fold_certified']:
        output['contour']=contour_stage(family,p)
        output['roots']=root_stage(family,p,fold)
        output['four_root_boxes_certified']=all(x['accepted'] for x in output['roots'])
    else:output['next_stages_status']='not executed: chosen fold did not pass all registered validations'
    output['execution_finished_utc']=datetime.now(timezone.utc).isoformat();path.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print('FINAL',json.dumps({k:output.get(k) for k in ('fold_certified','four_root_boxes_certified')}),'contour',output.get('contour',{}).get('accepted'),flush=True)

if __name__=='__main__':main()
