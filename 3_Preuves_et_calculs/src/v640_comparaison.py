"""Prospective comparison of the unchanged exact V6.39 pairs.

The reported first tranche is a numerical contour-minus-sign deficit, never
a certified first off-line zero. Censored and unresolved members remain visible.
"""
import hashlib
import json


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_protocol(data_directory):
    manifest_path = data_directory / 'v639_couples_fixes.json'
    prediction_path = data_directory / 'prevision_v640_comparaison.md'
    lock = json.loads((data_directory / 'v640_protocole_verrouille.json').read_text())
    manifest = json.loads(manifest_path.read_text())
    payload = {k: v for k, v in manifest.items() if k != 'sha256'}
    payload_hash = hashlib.sha256(json.dumps(payload, sort_keys=True,
        separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
    # The original pre-count bytes remain in 4_Archives/recus/V640. The active
    # readable copy acquired the corpus-wide UTF-8 BOM after an encoding test.
    # Accept only this three-byte presentation prefix, never a content edit.
    prediction_bytes=prediction_path.read_bytes()
    if prediction_bytes.startswith(b'\xef\xbb\xbf'):
        prediction_bytes=prediction_bytes[3:]
    prediction_hash=hashlib.sha256(prediction_bytes).hexdigest()
    original_prediction=data_directory.parents[1]/'4_Archives/recus/V640/prevision_v640_comparaison.md'
    if original_prediction.exists() and digest(original_prediction)!=lock['prediction_file_sha256']:
        raise ValueError('Original prospective prediction archive changed')
    if (digest(manifest_path) != lock['selection_file_sha256']
            or prediction_hash != lock['prediction_file_sha256']
            or payload_hash != manifest['sha256']
            or payload_hash != lock['selection_payload_sha256']):
        raise ValueError('Frozen selection or prediction changed')
    if len(manifest['pairs']) != lock['n_pairs']:
        raise ValueError('Frozen pair count changed')
    return manifest, lock


def compare_members(low, high, ceiling, require_roots=True):
    """Compare the truncated observable, retaining censoring and failures."""
    def member(record):
        if not record['stable']:
            return {'status': 'unresolved', 'first': None}
        first = record['first_detected']
        if first is None or first > ceiling:
            return {'status': 'no_detection_under_ceiling', 'first': None}
        if require_roots and not record.get('root_recrossed', False):
            return {'status': 'root_not_recrossed', 'first': int(first)}
        return {'status': 'detected', 'first': int(first)}
    lo, hi = member(low), member(high)
    if any(x['status'] in ('unresolved', 'root_not_recrossed') for x in (lo, hi)):
        order = 'undetermined'
    elif lo['first'] is None and hi['first'] is None:
        order = 'both_no_detection'
    elif hi['first'] is None:
        order = 'higher_D_later'
    elif lo['first'] is None:
        order = 'higher_D_earlier'
    elif hi['first'] < lo['first']:
        order = 'higher_D_earlier'
    elif hi['first'] > lo['first']:
        order = 'higher_D_later'
    else:
        order = 'same_tranche'
    return {'order': order, 'low': lo, 'high': hi,
            'one_member_censored': sum(x['first'] is None for x in (lo, hi)) == 1
                and order in ('higher_D_earlier', 'higher_D_later'),
            'order_is_for_truncated_numerical_observable': True}


def analyze(manifest, rows, ceilings=(50, 100, 150), require_roots=True):
    by_id = {r['id']: r for r in rows}
    if len(by_id) != len(rows):
        raise ValueError('Duplicate direction ID')
    reports = []
    for ceiling in ceilings:
        pairs = []
        counts = dict(higher_D_earlier=0, higher_D_later=0, same_tranche=0,
                      both_no_detection=0, undetermined=0)
        for pair in manifest['pairs']:
            comparison = compare_members(by_id[pair['id']+'_plus'],
                by_id[pair['id']+'_minus'], ceiling, require_roots)
            counts[comparison['order']] += 1
            pairs.append({**{k:pair[k] for k in ('id','character_k','radius')},
                          **comparison})
        threshold = len(pairs)//2+1
        unresolved = counts['undetermined'] + counts['both_no_detection']
        if counts['higher_D_earlier'] >= threshold:
            prediction = 'observed_for_the_frozen_numerical_observable'
        elif counts['higher_D_earlier'] + unresolved < threshold:
            prediction = 'not_observed_even_if_all_unresolved_orders_were_favorable'
        else:
            prediction = 'undetermined'
        reports.append({'ceiling': ceiling, 'counts': counts, 'pairs': pairs,
            'fixed_denominator': len(pairs), 'majority_threshold': threshold,
            'prediction_status': prediction, 'independent_replications': False,
            'comparable_strict_orders': counts['higher_D_earlier']+counts['higher_D_later']})
    return {'reports': reports, 'causal_inference': False,
            'certified_first_zero': False, 'statistical_significance_test': None}
