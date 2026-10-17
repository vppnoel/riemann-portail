"""Prospective V6.41: six continuations, critical folds, pair moments and fibres."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import math
import sys
import time
import mpmath as mp
import numpy as np
from scipy.optimize import root,brentq

ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data'
sys.path.insert(0,str(ROOT/'src'))
from euler_archipelago import characters,hurwitz_vec
from relief_direct import completed_phase_basis
from v640_racines import reconstruct_pair
from v641_collisions import make_family
from v641_fibres import phase_values,fibre_geometry,defect_polynomial,constancy_residual,interval_certificate
from v641_blocs import pair_from_moments,jet_section


def load(name):return json.loads((D/name).read_text(encoding='utf-8-sig'))
def save(name,value):(D/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def verify():
    lock=load('v641_protocole_verrouille.json')
    for name,key in [('v639_couples_fixes.json','selection_sha256'),('v640_racines_recoupees.json','prior_roots_sha256'),('prevision_v641_fibres_et_plis.md','prediction_sha256')]:
        if digest(D/name)!=lock[key]:raise ValueError('Frozen input changed: '+name)
    original=ROOT.parent/'4_Archives/recus/V641/prevision_v641_fibres_et_plis.md'
    assert digest(original)==lock['original_prediction_sha256']
    return lock,load('v639_couples_fixes.json')


def radius(key):
    if key=='pi/6':return math.pi/6
    if '/' in key:
        a,b=key.split('/');return int(a)/int(b)
    return float(key)


def mp_radius(key):
    if key=='pi/6':return mp.pi/6
    if '/' in key:
        a,b=key.split('/');return mp.mpf(a)/mp.mpf(b)
    return mp.mpf(key)


class EMFamily:
    def __init__(self,pair,side):
        rebuilt=reconstruct_pair(pair,60)
        self.u=np.array([float(x) for x in rebuilt['direction']]);self.anchor=(pair['character_k']-1)//2
        self.sign=1 if side=='plus' else -1
        self.ch=characters(13,1)
        self.weight=np.array([np.exp(-1j*c['phi']) for c in self.ch])
        tables=np.array([[ch['table'][a] for a in range(1,13)] for ch in self.ch])
        self.aggregate=np.stack((self.weight[self.anchor]*tables[self.anchor],(self.u*self.weight)@tables))
    def parts(self,s):
        s=np.asarray(s,dtype=complex).reshape(-1)
        h=np.array([hurwitz_vec(s,a/13) for a in range(1,13)])
        return np.exp(-s*math.log(13))*(self.aggregate@h)
    def evaluate(self,s,r):
        x,y=self.parts(s);return math.cos(r)*x+self.sign*math.sin(r)*y
    def derivative(self,s,r,h=1e-4):
        vals=self.evaluate(np.array([s-2*h,s-h,s+h,s+2*h]),r)
        return (vals[0]-8*vals[1]+8*vals[2]-vals[3])/(12*h)
    def critical_parts(self,t,dh=1e-4):
        t=np.asarray(t,dtype=float).reshape(-1)
        b=completed_phase_basis(13,1,.5+1j*t).real
        bp=completed_phase_basis(13,1,.5+1j*(t+dh)).real
        bm=completed_phase_basis(13,1,.5+1j*(t-dh)).real
        z=np.stack((b[self.anchor],self.u@b))
        dz=np.stack(((bp-bm)[self.anchor]/(2*dh),self.u@(bp-bm)/(2*dh)))
        return z,dz
    def wronskian(self,t,dh=1e-4):
        z,dz=self.critical_parts([t],dh);return float(z[0,0]*dz[1,0]-dz[0,0]*z[1,0])


def continue_path(family,seed,denominator,direction):
    r0=radius(seed['radius']);s0=complex(float(seed['beta']),float(seed['gamma']))
    grid={j/denominator:f'{j}/{denominator}' for j in range(3*denominator//4+1)}
    grid[r0]=seed['radius'];grid[math.pi/6]='pi/6'
    targets=sorted((r for r in grid if (r-r0)*direction>1e-12),reverse=direction<0)
    points=[{'radius':r0,'radius_key':seed['radius'],'beta':s0.real,'gamma':s0.imag,'residual':0.,'kind':'inherited_seed'}]
    previous_r,previous_s=r0,s0;stop=None
    for r in targets:
        x,y=family.parts([previous_s]);fr=-math.sin(previous_r)*x[0]+family.sign*math.cos(previous_r)*y[0]
        fs=family.derivative(previous_s,previous_r)
        predictor=previous_s-fr/fs*(r-previous_r) if abs(fs)>1e-12 else previous_s
        if abs(predictor-previous_s)>.2:predictor=previous_s
        def equations(v):
            if not np.all(np.isfinite(v)) or abs(v[0])>13 or abs(v[1])>45:return [1e80,1e80]
            f=family.evaluate([complex(*v)],r)[0];return [f.real,f.imag]
        try:
            found=root(equations,[predictor.real,predictor.imag],tol=1e-11,options={'maxfev':100})
            s=complex(*found.x)
            if s.real<.5:s=1-s.conjugate()
            x,y=family.parts([s]);scale=max(1.,abs(math.cos(r)*x[0])+abs(math.sin(r)*y[0]))
            residual=float(abs(family.evaluate([s],r)[0])/scale)
            move=abs(s-previous_s)
            admissible=bool(np.isfinite([s.real,s.imag,residual]).all() and residual<1e-8 and move<=.2 and -.000001<=s.real<=3 and abs(s.imag)<=25)
            point={'radius':r,'radius_key':grid[r],'beta':s.real,'gamma':s.imag,'residual':residual,'movement':move,'solver_success':bool(found.success),'kind':'corrected' if admissible else 'lost'}
            points.append(point)
            if not admissible:stop={**point,'reason':'lost_or_outside_registered_domain'};break
            if abs(s.real-.5)<.02:stop={**point,'reason':'critical_neighbourhood'};break
            previous_r,previous_s=r,s
        except Exception as error:
            stop={'radius':r,'radius_key':grid[r],'reason':'correction_failed','error':type(error).__name__+': '+str(error)[:200]};break
    return {'direction':'increasing' if direction>0 else 'decreasing','points':points,'stop':stop,'reached_endpoint':stop is None}


def branch_scan():
    lock,manifest=verify()
    if (D/'v641_branches.json').exists():raise RuntimeError('Do not overwrite prospective branch data')
    started=time.time();families={}
    for k in (1,5):
        pair=next(p for p in manifest['pairs'] if p['character_k']==k and p['radius']=='pi/6')
        for side in ('plus','minus'):families[(k,side)]=EMFamily(pair,side)
    rows=[]
    for seed in lock['seeds']:
        for denominator in (200,400):
            print('BRANCH',seed['id'],denominator,flush=True)
            f=families[(seed['character_k'],seed['side'])]
            paths=[continue_path(f,seed,denominator,d) for d in (-1,1)]
            row={'id':seed['id'],'character_k':seed['character_k'],'side':seed['side'],'denominator':denominator,'paths':paths}
            rows.append(row)
            print('BRANCH STATUS',[(p['direction'],len(p['points']),p['stop']['reason'] if p['stop'] else 'endpoint') for p in paths],flush=True)
    save('v641_branches.json',{'version':'V6.41','rows':rows,'seconds':time.time()-started,'exhaustive_branch_coverage':False,'zero_counts_certified':False})


def wronskian_scan():
    lock,manifest=verify()
    if (D/'v641_wronskiens.json').exists():raise RuntimeError('Do not overwrite prospective scan')
    candidates=[];diagnostics=[]
    for k in (1,5):
        pair=next(p for p in manifest['pairs'] if p['character_k']==k and p['radius']=='pi/6')
        f=EMFamily(pair,'plus')
        for dt in (.01,.005):
            print('WRONSKIAN',k,dt,flush=True)
            t=np.arange(-int(25/dt),int(25/dt)+1)*dt;dh=1e-4 if dt==.01 else 5e-5
            z,dz=f.critical_parts(t,dh);w=z[0]*dz[1]-dz[0]*z[1]
            crossings=np.flatnonzero(w[:-1]*w[1:]<0)
            this=[]
            for j in crossings:
                try:
                    gamma=brentq(lambda h:f.wronskian(h,dh),t[j],t[j+1],xtol=1e-10)
                    values,_=f.critical_parts([gamma],dh)
                    for side,sign in [('plus',1),('minus',-1)]:
                        r=math.atan2(-values[0,0],sign*values[1,0])%math.pi
                        item={'character_k':k,'side':side,'height':gamma,'radius':r,'step':dt,'accepted_radius':0<r<.75,'status':'candidate' if 0<r<.75 else 'outside_radius'}
                        candidates.append(item);this.append(item)
                except Exception as error:
                    candidates.append({'character_k':k,'step':dt,'bracket':[float(t[j]),float(t[j+1])],'status':'localization_failed','error':str(error)[:200]})
            diagnostics.append({'character_k':k,'step':dt,'sign_changes':len(crossings),'candidate_in_radius':sum(x['accepted_radius'] for x in this)})
            print('WRONSKIAN STATUS',diagnostics[-1],flush=True)
    unique=[]
    for c in candidates:
        if not c.get('accepted_radius'):continue
        match=next((u for u in unique if u['character_k']==c['character_k'] and u['side']==c['side'] and abs(u['height']-c['height'])<1e-5),None)
        if match:match['seen_steps'].append(c['step'])
        else:unique.append({**c,'seen_steps':[c['step']]})
    for n,c in enumerate(unique):c['id']=f"fold_k{c['character_k']}_{c['side']}_{n+1}"
    save('v641_wronskiens.json',{'version':'V6.41','diagnostics':diagnostics,'all_candidates_including_rejections':candidates,'selected':unique,'scanner_is_not_exhaustive':True})


def refine_collisions():
    lock,manifest=verify()
    if (D/'v641_collisions.json').exists():raise RuntimeError('Do not overwrite collisions')
    scan=load('v641_wronskiens.json');jobs=[];started=time.time()
    for c in scan['selected']:
        print('FOLD MP',c['id'],c['radius'],c['height'],flush=True)
        stages=[];values=[]
        pair=next(p for p in manifest['pairs'] if p['character_k']==c['character_k'] and p['radius']=='pi/6')
        for digits,limit in [(40,'1e-25'),(70,'1e-50')]:
            try:
                with mp.workdps(digits):
                    f=make_family(pair,c['side'],digits)
                    seed=mp.mpf(str(c['height']))
                    t=mp.findroot(f.wronskian,(seed-mp.mpf('.001'),seed+mp.mpf('.001')),tol=mp.power(10,-digits+8),maxsteps=30)
                    r=f.radius_from_height(t)
                    jet=f.jet(r,t)
                    residual=max(abs(jet['Z']),abs(jet['Z_t']))
                    transverse=abs(jet['Z_r'])>mp.mpf('1e-12') and abs(jet['Z_tt'])>mp.mpf('1e-12')
                    ok=bool(residual<mp.mpf(limit) and 0<r<mp.mpf(3)/4 and abs(t)<=25 and transverse and jet['reality_defect']<mp.mpf(limit))
                    values.append((r,t))
                    stages.append({'digits':digits,'radius':mp.nstr(r,digits),'height':mp.nstr(t,digits),'residual':mp.nstr(residual,12),'Z_r':mp.nstr(jet['Z_r'],18),'Z_tt':mp.nstr(jet['Z_tt'],18),'kappa':mp.nstr(-2*jet['Z_r']/jet['Z_tt'],18),'reality_defect':mp.nstr(jet['reality_defect'],12),'accepted':ok})
            except Exception as error:stages.append({'digits':digits,'accepted':False,'error':type(error).__name__+': '+str(error)[:300]})
        with mp.workdps(70):agreement=max(abs(values[0][j]-values[1][j]) for j in (0,1)) if len(values)==2 else mp.inf
        job={**c,'precisions':stages,'precision_agreement':mp.nstr(agreement,12),'accepted':all(x['accepted'] for x in stages) and agreement<mp.mpf('1e-20'),'interval_certification':False}
        jobs.append(job);save('v641_collisions_checkpoint.json',{'jobs':jobs})
        print('FOLD STATUS',job['accepted'],flush=True)
    branches=load('v641_branches.json');attributions=[]
    for row in branches['rows']:
        for path in row['paths']:
            stop=path['stop']
            if not stop or stop['reason']!='critical_neighbourhood':continue
            choices=[j for j in jobs if j['accepted'] and j['character_k']==row['character_k'] and j['side']==row['side'] and abs(float(j['precisions'][-1]['height'])-stop['gamma'])<.5 and abs(float(j['precisions'][-1]['radius'])-stop['radius'])<.05]
            best=min(choices,key=lambda j:abs(float(j['precisions'][-1]['height'])-stop['gamma'])) if choices else None
            attributions.append({'branch_id':row['id'],'denominator':row['denominator'],'direction':path['direction'],'stop':stop,'fold_id':best['id'] if best else None,'status':'attributed' if best else 'unresolved'})
    save('v641_collisions.json',{'version':'V6.41','jobs':jobs,'n_candidates':len(jobs),'n_accepted':sum(j['accepted'] for j in jobs),'attributions':attributions,'seconds':time.time()-started,'interval_certification':False})


def contour_moments(em,r,tcentre,n,h):
    a=np.arange(n)*2*math.pi/n;v=.2*np.exp(1j*a);w=tcentre+v;s=.5+1j*w
    f=em.evaluate(s,r)
    shifts=[em.evaluate(s+k*h,r) for k in (-2,-1,1,2)]
    fs=(shifts[0]-8*shifts[1]+8*shifts[2]-shifts[3])/(12*h)
    integrand=v*1j*fs/f
    moments=np.array([np.mean(w**k*integrand) for k in range(3)])
    x,y=em.parts(s);scale=np.abs(math.cos(r)*x)+np.abs(math.sin(r)*y)
    return moments,float(np.min(np.abs(f)/np.maximum(scale,1e-300)))


def pair_blocks():
    lock,manifest=verify()
    if (D/'v641_blocs_paires.json').exists():raise RuntimeError('Do not overwrite pair blocks')
    folds=load('v641_collisions.json');ids={a['fold_id'] for a in folds['attributions'] if a['fold_id']};records=[]
    for job in folds['jobs']:
        if job['id'] not in ids:continue
        pair=next(p for p in manifest['pairs'] if p['character_k']==job['character_k'] and p['radius']=='pi/6');em=EMFamily(pair,job['side'])
        stage=job['precisions'][-1];rstar=float(stage['radius']);tstar=float(stage['height']);kappa=float(stage['kappa'])
        for offset in (-1e-4,0,1e-4):
            print('PAIR BLOCK',job['id'],offset,flush=True)
            r=rstar+offset;m1,b1=contour_moments(em,r,tstar,128,1e-3);m2,b2=contour_moments(em,r,tstar,256,5e-4)
            agreement=float(np.max(abs(m1-m2)))
            admissible=bool(max(abs(m1[0]-2),abs(m2[0]-2))<1e-5 and agreement<1e-6 and min(b1,b2)>1e-8)
            moments=[{'real':float(x.real),'imag':float(x.imag)} for x in m2]
            row={'fold_id':job['id'],'character_k':job['character_k'],'side':job['side'],'offset':offset,'radius':r,'moments':moments,'moment_agreement':agreement,'sampled_boundary_margin':min(b1,b2),'accepted_numerical_block':admissible,'interval_certification':False}
            if admissible:
                block=pair_from_moments(*m2);delta=block['discriminant'];mu=block['mu']
                reality=max(abs(block['centre'].imag),abs(delta.imag))
                if reality>1e-6:
                    row['accepted_numerical_block']=False
                row.update(centre_real=block['centre'].real,centre_imag=block['centre'].imag,discriminant_real=delta.real,discriminant_imag=delta.imag,mu_real=mu.real,mu_linear=kappa*offset,reality_residual=reality,
                    numerical_signature='two_critical_roots' if delta.real>1e-6 else 'off_line_pair' if delta.real<-1e-6 else 'near_collision')
                confirmations=[]
                if offset and row['accepted_numerical_block']:
                    for index,seed in enumerate(block['roots']):
                        vals=[];stages=[]
                        for digits,limit in [(40,'1e-25'),(70,'1e-50')]:
                            try:
                                with mp.workdps(digits):
                                    family=make_family(pair,job['side'],digits)
                                    rr=mp.mpf(stage['radius'])+mp.mpf(str(offset))
                                    sseed=mp.mpc('.5')+mp.j*mp.mpc(str(seed.real),str(seed.imag))
                                    value=mp.findroot(lambda s:family.evaluate(s,rr),(sseed,sseed+mp.mpf('.00001')),tol=mp.power(10,-digits+8),maxsteps=40)
                                    residual=abs(family.evaluate(value,rr));vals.append(value)
                                    stages.append({'digits':digits,'beta':mp.nstr(value.real,digits),'gamma':mp.nstr(value.imag,digits),'residual':mp.nstr(residual,12),'accepted':bool(residual<mp.mpf(limit) and abs(value-sseed)<mp.mpf('.01'))})
                            except Exception as error:stages.append({'digits':digits,'accepted':False,'error':str(error)[:250]})
                        with mp.workdps(70):gap=abs(vals[0]-vals[1]) if len(vals)==2 else mp.inf
                        confirmations.append({'root_index':index,'precisions':stages,'precision_agreement':mp.nstr(gap,12),'accepted':all(s['accepted'] for s in stages) and gap<mp.mpf('1e-20')})
                row['root_confirmations']=confirmations
            records.append(row);save('v641_blocs_checkpoint.json',{'rows':records})
    save('v641_blocs_paires.json',{'version':'V6.41','rows':records,'n_folds':len(ids),'n_accepted_blocks':sum(r['accepted_numerical_block'] for r in records),'n_roots_recrossed':sum(j['accepted'] for r in records for j in r.get('root_confirmations',[])),'certified_two_zero_contours':False})


def geometry():
    lock,manifest=verify()
    if (D/'v641_geometrie.json').exists():raise RuntimeError('Do not overwrite geometry')
    z=phase_values(90);rows=[]
    for k in (1,3,5):
        i=(k-1)//2
        for key in ('9/20','pi/6','13/20','3/4'):
            r=radius(key);centre=math.cos(r)*z[i];base=fibre_geometry(z,i,r,centre)
            ev,V=np.linalg.eigh(base.gram)
            for axis in (0,1):
                for eta in (0,.25,.81,1,1.21):
                    b=V[:,axis]*math.sqrt(ev[axis]*eta);A=centre+math.sin(r)*complex(*b);f=fibre_geometry(z,i,r,A)
                    rows.append({'character_k':k,'radius':key,'axis':axis,'eta_target':eta,'eta_computed':f.eta,'status':f.status,'A_real':A.real,'A_imag':A.imag,'fibre_radius':f.rho,'constancy_diagnostic':constancy_residual(defect_polynomial(f)) if f.status!='outside' else None})
    certificate=interval_certificate(80);save('v641_certificat_fibres.json',certificate)
    sections=[]
    for t in (5,10,15,20):
        h=1e-4;b0=completed_phase_basis(13,1,[.5+1j*t]).real[:,0]
        bp=completed_phase_basis(13,1,[.5+1j*(t+h)]).real[:,0];bm=completed_phase_basis(13,1,[.5+1j*(t-h)]).real[:,0]
        bt=(bp-bm)/(2*h);btt=(bp-2*b0+bm)/h**2
        for k in (1,3,5):
            i=(k-1)//2;r=math.pi/6;centre=math.cos(r)*z[i];base=fibre_geometry(z,i,r,centre);ev,V=np.linalg.eigh(base.gram)
            for eta in (0,.25,1):
                b=V[:,0]*math.sqrt(ev[0]*eta);A=centre+math.sin(r)*complex(*b)
                e=np.eye(6)[i];C=np.stack((e,z.real,z.imag,b0,bt));rhs=np.array([math.cos(r),A.real,A.imag,0,0]);section=jet_section(C,rhs)
                item={'height':t,'character_k':k,'eta_target':eta,'A_real':A.real,'A_imag':A.imag,'rank':section['rank'],'singular_values':section['singular_values'].tolist(),'nu':section['nu'],'status':section['status'],'compatibility_residual':section['compatibility_residual'],'candidates':[]}
                for c in section['solutions']:
                    item['candidates'].append({'coefficients':c.tolist(),'constraint_residual':float(np.linalg.norm(C@c-rhs)),'norm_error':float(abs(c@c-1)),'Z_tt_EM':float(c@btt),'exact_multiplicity_certified':False})
                sections.append(item)
    save('v641_geometrie.json',{'version':'V6.41','target_examples':rows,'jet_sections':sections,'A_feasibility_theorem':'Ellipse with S2 fibres in the interior, singleton on boundary, empty outside','universal_defect_variation':False,'jet_ranks_are_numerical':True})


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--phase',choices=['branches','scan','collisions','blocks','geometry'],required=True);args=p.parse_args()
    {'branches':branch_scan,'scan':wronskian_scan,'collisions':refine_collisions,'blocks':pair_blocks,'geometry':geometry}[args.phase]()
