"""V6.40: locked comparison and independent recrossing of all 24 members."""
from pathlib import Path
import argparse
import csv
import datetime
import json
import math
import sys
import time
import mpmath as mp
import numpy as np
from scipy.special import zeta

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'data'
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'scripts'))
from relief_direct import DirectGrid, completed_phase_basis, a1_and_defect
from euler_archipelago import characters
from run_v637_apparie import boundary_margins, critical_from_basis
from v640_comparaison import verify_protocol, analyze, digest


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def write_rows(rows):
    with (D/'v640_directions.csv').open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)


def reconstruct_inputs(manifest):
    from v640_racines import reconstruct_pair
    sensitivity, audit = [], []
    for pair in manifest['pairs']:
        low = reconstruct_pair(pair, digits=80)
        high = reconstruct_pair(pair, digits=110)
        with mp.workdps(110):
            phase_coordinate_error=max(abs(mp.mpc(np.exp(-1j*x['phi']))-z)
                for x,z in zip(characters(13,1),high['phases']))
            anchor=(pair['character_k']-1)//2
            for j,side in enumerate(('plus','minus')):
                exact=high[side]; binary=[mp.mpf(float(x)) for x in pair['exported_binary64_vectors'][j]]
                reconstruction_error=max(abs(a-b) for a,b in zip(low[side],exact))
                coordinate_error=max(abs(a-b) for a,b in zip(binary,exact))
                norm_error=abs(sum(x*x for x in binary)-1)
                target=mp.cos(high['radius'])*high['phases'][anchor]
                A_error=abs(sum(c*z for c,z in zip(binary,high['phases']))-target)
                sensitivity.append([float(x) for x in exact])
                audit.append({'id':pair['id']+'_'+side,
                    'reconstruction_agreement_80_110':mp.nstr(reconstruction_error,18),
                    'max_binary64_coordinate_error':mp.nstr(coordinate_error,18),
                    'binary64_norm_squared_error':mp.nstr(norm_error,18),
                    'binary64_complex_A_error':mp.nstr(A_error,18),
                    'historical_phase_coordinate_error':mp.nstr(phase_coordinate_error,18),
                    'errors_are_high_precision_estimates_not_interval_bounds':True})
    return np.array(sensitivity),audit


def run(cache_directory):
    manifest,lock=verify_protocol(D)
    if (D/'v640_comptages.npz').exists() or (D/'v640_resultats.json').exists():
        raise RuntimeError('Results already exist; do not overwrite a prospective run')
    cache_directory.mkdir(parents=True,exist_ok=True)
    C=np.asarray([v for pair in manifest['pairs'] for v in pair['exported_binary64_vectors']]+np.eye(6).tolist())
    sensitivity,input_audit=reconstruct_inputs(manifest)
    with mp.workdps(60):
        analytic_margin=mp.cos(mp.mpf(3)/4)-mp.sqrt(6)*(mp.zeta(3)-1)
        assert analytic_margin>0
        margin_text=mp.nstr(analytic_margin,30)
    input_record={'version':'V6.40','digits':[80,110],
        'selection_sha256':lock['selection_file_sha256'],
        'right_boundary':3,'analytic_first_term_margin':margin_text,
        'basis_phase_evaluation':'historical binary64; independently checked on localized roots',
        'rows':input_audit}
    save_json(D/'v640_erreur_entree.json',input_record)
    execution={'version':'V6.40','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'selection_file_sha256':lock['selection_file_sha256'],
        'prediction_file_sha256':lock['prediction_file_sha256'],
        'lock_file_sha256':digest(D/'v640_protocole_verrouille.json')}
    save_json(D/'v640_execution.json',execution)
    started=time.time()
    print('V640 START',execution['started_utc'],'30 directions; R=3; T=150',flush=True)
    grids=[];totals=[];critical=[];diags=[];margins=[]
    sensitivity_total=sensitivity_critical=None
    for dt,ds in ((.02,.05),(.01,.025)):
        print('GRILLE',dt,ds,flush=True)
        grid=DirectGrid(13,1,150,dt,3,ds,cache_directory/f'q13_T150_h{dt:g}_ds{ds:g}_R3.npz')
        all_C=C if dt==.02 else np.vstack([C,sensitivity])
        total,crit,off,diag=grid.counts(all_C)
        if dt==.01:
            sensitivity_total,sensitivity_critical=total[30:],crit[30:]
        grids.append(grid);totals.append(total[:30]);critical.append(crit[:30]);diags.append(diag)
        margins.append(boundary_margins(C,grid))
        print('DIAGNOSTIC',json.dumps(diag),flush=True)
    print('DROITE CRITIQUE 0.005',flush=True)
    t=np.arange(-30000,30001)*.005
    basis=completed_phase_basis(13,1,.5+1j*t)
    critical_all=critical_from_basis(np.vstack([C,sensitivity]),basis.real,t,grids[0].levels)
    crit005=critical_all[:30]
    input_stable=np.r_[np.all(sensitivity_total==totals[-1][:24],axis=1)
        &np.all(sensitivity_critical==critical[-1][:24],axis=1)
        &np.all(critical_all[30:]==crit005[:24],axis=1),np.ones(6,dtype=bool)]
    total=totals[-1];crit=crit005;off=total-crit
    total_stable=np.all(totals[0]==totals[1],axis=1)
    critical_stable=np.all(critical[0]==critical[1],axis=1)&np.all(critical[1]==crit005,axis=1)
    marginH=np.minimum(margins[0][0],margins[1][0]);marginR=np.minimum(margins[0][1],margins[1][1])
    resolved=all(x['unresolved_horizontal_rows']==0 and x['max_integer_residual']<1e-8
        and x['max_phase_vertical']<.8 and x['max_phase_horizontal']<.8 for x in diags)
    a1,defect=a1_and_defect(13,1,C)
    records=[]
    for pair in manifest['pairs']:
        for side in ('plus','minus'):
            records.append({'id':pair['id']+'_'+side,'pair_id':pair['id'],
                'character_k':pair['character_k'],'radius':pair['radius'],'side':side,'euler':False})
    for k in (1,3,5,7,9,11):
        records.append({'id':f'euler_k{k}','pair_id':None,'character_k':k,'radius':'0','side':'control','euler':True})
    rows=[]
    for i,record in enumerate(records):
        hits=np.flatnonzero(off[i]>0);first=int(hits[0]+1) if len(hits) else None
        paired=bool(np.all(off[i]>=0)&np.all(off[i]%2==0))
        monotone=bool(np.all(np.diff(total[i])>=0)&np.all(np.diff(crit[i])>=0)&np.all(np.diff(off[i])>=0))
        stable=bool(total_stable[i] and critical_stable[i] and input_stable[i]
            and paired and monotone and resolved and marginH[i]>=1e-10 and marginR[i]>=1e-10)
        rows.append({**record,'first_detected':first,'previous_level':first-1 if first else 150,
            'stable':stable,'A_modulus':float(a1[i]),'D':float(defect[i]),
            'total_stable':bool(total_stable[i]),'critical_stable':bool(critical_stable[i]),
            'input_sensitivity_stable':bool(input_stable[i]),'paired_nonnegative':paired,
            'all_three_counts_monotone':monotone,'sampled_boundary_horizontal_min':float(marginH[i]),
            'sampled_boundary_vertical_min':float(marginR[i]),'total_T150':int(total[i,-1]),
            'critical_T150':int(crit[i,-1]),'deficit_T150':int(off[i,-1]),
            'no_detection_under150':first is None,'root_recrossed':False})
    euler_ok=all(r['stable'] and r['first_detected'] is None for r in rows if r['euler'])
    if not euler_ok:
        for row in rows: row['stable']=False
    write_rows(rows)
    save_json(D/'v640_directions.json',rows)
    np.savez_compressed(D/'v640_comptages.npz',coefficients=C,levels=grids[0].levels,
        total_coarse=totals[0],total_fine=total,critical_coarse=critical[0],
        critical_fine=critical[1],critical_finest=crit005,deficit=off,
        sensitivity_coefficients=sensitivity,sensitivity_total=sensitivity_total,
        sensitivity_critical_fine=sensitivity_critical,sensitivity_critical_finest=critical_all[30:])
    result={'version':'V6.40','q':13,'parity':1,'dimension':6,'Tmax':150,'sigma_right':3,
        'n_pairs':12,'n_directions':24,'n_controls':6,'selection_sha256':lock['selection_file_sha256'],
        'n_stable':sum(r['stable'] for r in rows),'n_ambiguous':sum(not r['stable'] for r in rows),
        'euler_controls_passed':euler_ok,'n_detected':sum(r['first_detected'] is not None and not r['euler'] for r in rows),
        'diagnostics':diags,'maximum_basis_imaginary_residual':float(np.max(abs(basis.imag))),
        'n_total_changed':int(np.sum(totals[0]!=totals[1])),
        'n_critical_changed_001':int(np.sum(critical[0]!=critical[1])),
        'n_critical_changed_0005':int(np.sum(critical[1]!=crit005)),
        'n_input_sensitivity_changed':int(np.sum(~input_stable)),
        'analysis_before_root_recrossing':analyze(manifest,rows,require_roots=False),
        'analysis':analyze(manifest,rows,require_roots=True),
        'arithmetic':'binary64 EM grids; numerical refinements; no interval certificate',
        'boundary_margins_are_sampled':True,'seconds_counting':time.time()-started,
        'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    save_json(D/'v640_resultats.json',result)
    print('COMPTAGE TERMINE',result['n_stable'],'admissibles,',result['n_detected'],'detections',flush=True)
    for r in result['analysis_before_root_recrossing']['reports']:
        print('BILAN BRUT',r['ceiling'],json.dumps(r['counts']),flush=True)


def roots():
    from v640_racines import locate_direction, confirm_direction
    manifest,lock=verify_protocol(D)
    rows=json.loads((D/'v640_directions.json').read_text())
    result=json.loads((D/'v640_resultats.json').read_text())
    out_path=D/'v640_racines_recoupees.json'
    if out_path.exists():
        raise RuntimeError('Independent recrossing already exists; do not overwrite')
    jobs=[];started=time.time()
    by_id={r['id']:r for r in rows}
    for pair in manifest['pairs']:
        for index,side in enumerate(('plus','minus')):
            row=by_id[pair['id']+'_'+side]
            job={'id':row['id'],'pair_id':pair['id'],'character_k':pair['character_k'],
                'radius':pair['radius'],'side':side,'first_detected':row['first_detected']}
            print('RECOUPEMENT',row['id'],row['first_detected'],flush=True)
            if not row['stable']:
                job.update(status='unresolved_counts',root_found=False)
            elif row['first_detected'] is None:
                job.update(status='no_detection_under_ceiling',root_found=False)
            else:
                try:
                    located=locate_direction(pair['exported_binary64_vectors'][index],row['first_detected'],3)
                    job['localization']=located
                    if located['found']:
                        confirmation=confirm_direction(pair,side,pair['exported_binary64_vectors'][index],
                            located,row['first_detected'],3)
                        job['confirmation']=confirmation
                        job.update(status=confirmation['status'],root_found=bool(confirmation['root_found']))
                    else:
                        job.update(status='localization_failed',root_found=False)
                except Exception as error:
                    job.update(status='recrossing_failed',root_found=False,
                        error_type=type(error).__name__,error=str(error)[:500])
            row['root_recrossed']=bool(job['root_found'])
            jobs.append(job)
            print('STATUT',job['status'],flush=True)
    record={'version':'V6.40','selection_sha256':lock['selection_file_sha256'],
        'n_jobs':len(jobs),'n_roots_recrossed':sum(j['root_found'] for j in jobs),
        'all_jobs_retained':True,'jobs':jobs,'seconds':time.time()-started,
        'interval_certification':False,'certified_absence_before_detection':False}
    save_json(out_path,record)
    save_json(D/'v640_directions.json',rows);write_rows(rows)
    result['analysis']=analyze(manifest,rows,require_roots=True)
    result['n_roots_recrossed']=record['n_roots_recrossed']
    result['root_recrossing_file_sha256']=digest(out_path)
    save_json(D/'v640_resultats.json',result)
    print('RECOUPEMENTS TERMINES',record['n_roots_recrossed'],'/',len(jobs),flush=True)
    for report in result['analysis']['reports']:
        print('BILAN VALIDE',report['ceiling'],json.dumps(report['counts']),report['prediction_status'],flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--run',action='store_true')
    parser.add_argument('--roots',action='store_true')
    parser.add_argument('--cache-directory',type=Path,default=Path('/tmp/riemann_v640_cache'))
    args=parser.parse_args()
    if args.run:run(args.cache_directory)
    if args.roots:roots()
    if not(args.run or args.roots):parser.error('choose --run or --roots')
