"""Frozen inputs, censoring, false deficits and independent numerical evidence."""
from pathlib import Path
import copy
import json
import shutil
import tempfile
import mpmath as mp
import numpy as np
from v640_comparaison import verify_protocol, compare_members, analyze
from v640_racines import reconstruct_pair

D=Path(__file__).resolve().parents[1]/'data'


def test_frozen_manifest_and_prediction_cannot_be_silently_replaced():
    manifest,lock=verify_protocol(D)
    assert len(manifest['pairs'])==12 and lock['majority_threshold']==7
    with tempfile.TemporaryDirectory() as directory:
        out=Path(directory)
        for name in ('v639_couples_fixes.json','prevision_v640_comparaison.md','v640_protocole_verrouille.json'):
            shutil.copy2(D/name,out/name)
        text=(out/'prevision_v640_comparaison.md').read_text()
        (out/'prevision_v640_comparaison.md').write_text(text+'\nChanged after outcome.\n')
        try: verify_protocol(out)
        except ValueError: pass
        else: raise AssertionError('A changed prospective prediction was accepted')


def test_censoring_is_not_an_invented_detection_at151():
    detected={'stable':True,'first_detected':12,'root_recrossed':True}
    censored={'stable':True,'first_detected':None,'root_recrossed':False}
    r=compare_members(censored,detected,150)
    assert r['order']=='higher_D_earlier' and r['one_member_censored']
    assert r['low']['first'] is None
    r=compare_members(censored,censored,150)
    assert r['order']=='both_no_detection'
    r=compare_members(detected,detected,10)
    assert r['order']=='both_no_detection'
    r=compare_members(detected,detected,150)
    assert r['order']=='same_tranche'


def test_a_deficit_without_an_independent_root_remains_undetermined():
    # A double critical zero produces no change of sign: a positive contour
    # deficit alone cannot validate an off-critical-line-root comparison.
    t=np.linspace(-1,1,1001)
    values=(t-.313)**2
    assert np.count_nonzero(values[:-1]*values[1:]<0)==0
    false_deficit={'stable':True,'first_detected':5,'root_recrossed':False}
    confirmed={'stable':True,'first_detected':8,'root_recrossed':True}
    assert compare_members(false_deficit,confirmed,150)['order']=='undetermined'
    unstable={**confirmed,'stable':False}
    assert compare_members(unstable,confirmed,150)['order']=='undetermined'


def test_majority_denominator_is_not_restricted_to_favorable_comparisons():
    manifest={'pairs':[{'id':f'p{i}','character_k':1,'radius':'9/20'} for i in range(12)]}
    rows=[]
    for i,pair in enumerate(manifest['pairs']):
        for side,first in (('plus',10),('minus',5 if i<6 else 12)):
            rows.append({'id':pair['id']+'_'+side,'stable':True,
                         'first_detected':first,'root_recrossed':True})
    report=analyze(manifest,rows,ceilings=(150,))['reports'][0]
    assert report['fixed_denominator']==12 and report['majority_threshold']==7
    assert report['counts']['higher_D_earlier']==6
    assert report['prediction_status'].startswith('not_observed')
    rows[-1]['stable']=False
    report=analyze(manifest,rows,ceilings=(150,))['reports'][0]
    assert report['prediction_status']=='undetermined'


def test_exact_input_reconstruction_preserves_A_and_defect_orientation():
    manifest,lock=verify_protocol(D)
    with mp.workdps(80):
        for pair in manifest['pairs']:
            rebuilt=reconstruct_pair(pair,80)
            assert rebuilt['D_plus']<rebuilt['D_minus']
            assert rebuilt['plus_A_residual']<mp.mpf('1e-70')
            assert rebuilt['minus_A_residual']<mp.mpf('1e-70')
            assert rebuilt['kernel_residual']<mp.mpf('1e-70')
            for side,binary in zip(('plus','minus'),pair['exported_binary64_vectors']):
                assert max(abs(mp.mpf(float(a))-b) for a,b in zip(binary,rebuilt[side]))<mp.mpf('1e-15')


def test_saved_counts_and_all_twentyfour_root_jobs_have_consistent_provenance():
    manifest,lock=verify_protocol(D)
    rows=json.loads((D/'v640_directions.json').read_text())
    roots=json.loads((D/'v640_racines_recoupees.json').read_text())
    result=json.loads((D/'v640_resultats.json').read_text())
    counts=np.load(D/'v640_comptages.npz')
    ids={p['id']+'_'+s for p in manifest['pairs'] for s in ('plus','minus')}
    assert len(rows)==30 and {j['id'] for j in roots['jobs']}==ids
    assert len(roots['jobs'])==24
    assert result['selection_sha256']==roots['selection_sha256']==lock['selection_file_sha256']
    assert np.array_equal(counts['deficit'],counts['total_fine']-counts['critical_finest'])
    by_id={j['id']:j for j in roots['jobs']}
    for row in rows:
        if not row['euler']:
            assert row['root_recrossed']==by_id[row['id']]['root_found']
        if row['root_recrossed']:
            evidence=by_id[row['id']]['confirmation']
            assert evidence['precision_agreement_accepted']
            assert all(x['all_stage_checks_pass'] for x in evidence['precisions'])
            assert evidence['binary64_sensitivity']['input_shift_accepted']
    assert roots['interval_certification'] is False
    assert roots['certified_absence_before_detection'] is False
