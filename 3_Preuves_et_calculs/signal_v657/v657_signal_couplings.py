#!/usr/bin/env python3
"""Diagnose retained/lost couplings in the existing arithmetic Weil matrices.

This REUSES V644 point quadratures; it does not certify them or recompute primes.
No zeros are used.  Every output concerns an eight-dimensional parent space.
The finite complement below is not the infinite functional-analytic tail.
"""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

import mpmath as mp


def sym(M):
    return (M + M.T) / 2


def eig(M):
    return mp.eigsy(sym(M))


def spectral_norm(M):
    if M.rows == M.cols and M == M.T:
        vals, _ = eig(M)
        return max(abs(v) for v in vals)
    vals, _ = eig(M.T * M)
    return mp.sqrt(max(mp.mpf(0), vals[vals.rows-1]))


def dumpnum(x):
    return mp.nstr(x, 28)


def scalar(v, M):
    return (v.T * M * v)[0]


def numerical_record(record, metric_override=None, metric_label=None):
    G = mp.matrix(record['G'])
    metric = mp.matrix(record['B']) if metric_override is None else metric_override
    L = mp.cholesky(metric)
    Linv = L ** -1
    Q = sym(Linv * G * Linv.T)
    values, vectors = eig(Q)
    n = Q.rows
    diag = mp.diag([Q[i, i] for i in range(n)])
    off = Q - diag
    outputs = {
        'input_digits': record['digits'],
        'parent_dimension': n,
        'metric': metric_label or 'B(f,g)=integral(conj(f)*g+conj(fprime)*gprime)',
        'whitening': 'B=L L^T; phi_j=sum_i (L^(-T))_ij f_i; Q=L^(-1) G L^(-T)',
        'full_eigenvalues': [dumpnum(v) for v in values],
        'diagonal_minimum': dumpnum(min(Q[i, i] for i in range(n))),
        'offdiagonal_operator_norm': dumpnum(spectral_norm(off)),
        'diagonal_minus_offdiagonal_floor': dumpnum(min(Q[i, i] for i in range(n)) - spectral_norm(off)),
        'whitened_matrix': [[dumpnum(Q[i,j]) for j in range(n)] for i in range(n)],
        'partitions': [],
    }
    for k in [2, 4, 6]:
        A = Q[:k, :k]
        B = Q[:k, k:]
        C = Q[k:, k:]
        ca, _ = eig(C)
        aa, _ = eig(A)
        assert ca[0] > 0 and aa[0] > 0
        debt = sym(B * (C ** -1) * B.T)
        schur = sym(A - debt)
        ss, _ = eig(schur)
        LA = mp.cholesky(A)
        LiA = LA ** -1
        relative_debt = sym(LiA * debt * LiA.T)
        rr, _ = eig(relative_debt)
        normB = spectral_norm(B)
        completed_tail = mp.matrix([mp.mpf(0)] * (n - k))
        # On each head fibre the omitted coordinates attain the Schur envelope.
        # Use the smallest Schur eigenvector as a reproducible witness.
        _, sv = eig(schur)
        h = sv[:, 0]
        completed_tail = -(C ** -1) * B.T * h
        witness = mp.matrix(list(h) + list(completed_tail))
        identity_residual = abs(scalar(witness, Q) - scalar(h, schur))
        outputs['partitions'].append({
            'head_dimension': k,
            'finite_complement_dimension': n-k,
            'head_minimum': dumpnum(aa[0]),
            'complement_minimum': dumpnum(ca[0]),
            'coupling_norm': dumpnum(normB),
            'schur_minimum': dumpnum(ss[0]),
            'debt_norm': dumpnum(spectral_norm(debt)),
            'scalar_debt_bound': dumpnum(normB**2 / ca[0]),
            'relative_debt_maximum': dumpnum(rr[rr.rows-1]),
            'relative_margin': dumpnum(1-rr[rr.rows-1]),
            'schur_completion_identity_residual': dumpnum(identity_residual),
            'status': 'finite-parent numerical diagnostic, not omitted infinite-tail certificate',
        })
    # Deliberately choose a sensitive amplitude profile after inspection.
    # The real sign variants are a subset of all complex phase variants.
    a = mp.matrix([abs(vectors[j,0]) for j in range(n)])
    variants = []
    for tail_signs in itertools.product([-1,1], repeat=n-1):
        signs = (1,) + tail_signs
        c = mp.matrix([signs[j]*a[j] for j in range(n)])
        variants.append((scalar(c,Q), signs, c))
    low = min(variants, key=lambda z: z[0])
    high = max(variants, key=lambda z: z[0])
    observed = scalar(a, diag)
    phase_mean = sum(v[0] for v in variants)/len(variants)
    phase_variance = sum((v[0]-phase_mean)**2 for v in variants)/len(variants)
    coupling_variance = 4*sum(Q[i,j]**2*a[i]**2*a[j]**2
                               for i in range(n) for j in range(i+1,n))
    assert abs(phase_mean-observed) < mp.mpf('1e-70')
    assert abs(phase_variance-coupling_variance) < mp.mpf('1e-70')
    outputs['same_amplitudes_phase_witness'] = {
        'amplitudes': [dumpnum(v) for v in a],
        'low_signs': list(low[1]),
        'high_signs': list(high[1]),
        'coordinate_magnitudes_identical': True,
        'metric_norm_squared_both': dumpnum(sum(v*v for v in a)),
        'diagonal_observable_both': dumpnum(observed),
        'q_low': dumpnum(low[0]),
        'q_high': dumpnum(high[0]),
        'q_high_over_q_low': dumpnum(high[0]/low[0]),
        'q_spread': dumpnum(high[0]-low[0]),
        'phase_mean': dumpnum(phase_mean),
        'phase_standard_deviation': dumpnum(mp.sqrt(phase_variance)),
        'variance_identity_residual': dumpnum(abs(phase_variance-coupling_variance)),
        'variance_identity': 'Var_signs q=4 sum_(i<j) Q_ij^2 a_i^2 a_j^2; E_signs q=sum_i Q_ii a_i^2',
        'number_of_real_sign_variants_tested': len(variants),
        'selection': 'exploratory amplitude profile from smallest eigendirection; signs exhaustively compared',
        'not_claimed': 'not opposite signs, not global extrema over complex phases, not infinite-dimensional bound',
    }
    assert low[0] > 0 and high[0] >= low[0]
    assert abs(low[0] - values[0]) < mp.mpf('1e-60')
    return outputs


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--corpus', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args=parser.parse_args()
    source=args.corpus/'3_Preuves_et_calculs/data/v644_family_resultats.json'
    raw=source.read_bytes()
    data=json.loads(raw.decode('utf-8-sig'))
    modulepath=args.corpus/'3_Preuves_et_calculs/src/symbolic_weil_family.py'
    spec=importlib.util.spec_from_file_location('v644_symbolic_weil', modulepath)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    mp.mp.dps=100
    outputs={
        'version': 'V6.57',
        'source': str(source.relative_to(args.corpus)),
        'source_sha256': hashlib.sha256(raw).hexdigest(),
        'source_status': data['status'],
        'basis': 'f_k(x)=(d_x^2-1/4)[(x/S)^k (1-(x/S)^2)^4], |x|<=S, zero outside; k=0,...,7',
        'scope': 'diagnostic reanalysis of existing arithmetic eight-dimensional Weil matrices',
        'new_arithmetic_coefficients_computed': False,
        'certified': False,
        'global_RH_claim': False,
        'zero_data_used': False,
        'supports': [],
        'limits': [
            'V644 transcendental quadratures have no certified operator error here.',
            'Rechecking at two stored precisions is stability, not an error certificate.',
            'The 8-k dimensional complement is not the infinite-dimensional tail.',
            'Neither positivity of a finite matrix nor its Schur proves the infinite form positive.',
            'Diagonal metric data are retained identically, but no pair with opposite actual Weil signs is asserted.',
            'No new local certificate is claimed; document 73 already proves every test for S<=1/2.',
        ],
    }
    for support in data['supports']:
        records=[numerical_record(p) for p in support['precisions']]
        energy_records=[]
        C0=mp.log(8*mp.pi)+mp.euler+mp.pi/2
        n=records[0]['parent_dimension']
        mass=mp.matrix([[module.mpq(module.mass(support['S'],i,j)) for j in range(n)] for i in range(n)])
        for p in support['precisions']:
            R=mp.matrix(p['arch'])+(C0+1)*mass
            energy_records.append(numerical_record(p, metric_override=R,
                metric_label='R=mass+archimedean_translation_energy; R=arch+(C0+1)*exact_mass'))
        low=records[0];high=records[-1]
        delta=abs(mp.mpf(low['full_eigenvalues'][0])-mp.mpf(high['full_eigenvalues'][0]))
        outputs['supports'].append({
            'S':support['S'],
            'prime_power_count':support['prime_power_count'],
            'resolutions':records,
            'energy_metric_resolutions':energy_records,
            'stored_precision_eigenminimum_difference':dumpnum(delta),
        })
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(outputs,ensure_ascii=False,indent=2)+'\n')
    for row in outputs['supports']:
        r=row['resolutions'][-1]
        p=r['same_amplitudes_phase_witness']
        print('S',row['S'],'lambda_min',r['full_eigenvalues'][0],
              'same-amplitude ratio',p['q_high_over_q_low'],
              'offdiag lower bound',r['diagonal_minus_offdiagonal_floor'])
        for block in r['partitions']:
            print(' head',block['head_dimension'],'relative debt',block['relative_debt_maximum'],
                  'Schur min',block['schur_minimum'])
    print('Saved diagnostic:',args.output)


if __name__=='__main__':
    main()
