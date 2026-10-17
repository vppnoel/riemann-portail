"""Exact polynomial identities, typed guards, prospective results and integer tail."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,importlib.util
import mpmath as mp
import symbolic_weil_family as w
from domain_grammar import Word,translate,assert_admissible,allow_global_sign
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'3_Preuves_et_calculs/data'
def read(name):return json.loads((D/name).read_text(encoding='utf-8-sig'))
def reject(fn):
    try:fn()
    except (ValueError,TypeError):return
    raise AssertionError('invalid contract accepted')
def test_exact_metric_all_predeclared_supports_and_degrees():
    for s in read('v644_protocole_traductions.json')['supports']:
      for i in range(8):
       for j in range(8):assert w.metric(F(s),i,j)==w.seed_metric(F(s),i,j)
def test_correlation_parity_is_symmetrized_not_raw():
    for s in (F(1,2),F(3)):
        assert w.correlation(s,0,1)!=[F(0)]
        assert w.symmetric_correlation(s,0,1)==[F(0)]
        for i in range(4):
            h=w.correlation(s,i,i)
            assert w.evalq(h,0)==w.mass(s,i,i) and w.evalq(h,2)==0 and h[1]==0
            dg=w.integral_even(w.mul(w.derivative(w.test(s,i)),w.derivative(w.test(s,i))))/s
            assert -2*h[2]/s**2==dg
def test_exact_jet_boundary_and_distributed_derivatives():
    for k in range(8):
      for j in range(4):
        p=w.derivative(w.seed(k),j);assert w.evalq(p,1)==w.evalq(p,-1)==0
      assert w.evalq(w.derivative(w.seed(k),4),1)!=0 # polynomial cutoff generally not C4
def test_prime_cutoff_certificates_and_complete_power_lists():
    for row in read('v644_family_resultats.json')['supports']:
        c=row['cutoff_certificate'];lo=F(c['lower']);hi=F(c['upper']);x=c['cutoff']
        assert lo<hi and lo.numerator//lo.denominator==hi.numerator//hi.denominator==x
        assert [list(a) for a in w.prime_powers(x)]==row['prime_powers']
def test_typed_arithmetic_preserves_distinct_jet_points_and_units():
    f=Word(F(1),jets=2,origin_jets=3);g=Word(F(2),jets=1,origin_jets=4)
    v=translate('convolve',f,g);assert (v.S,v.jets,v.origin_jets,v.unit)==(F(3),3,7,2)
    assert translate('P',f).jets==3 and translate('P',f).origin_jets==3
    assert translate('derivative',f).jets==2 and translate('derivative',f).origin_jets==4
    assert translate('rescale',f,parameter=F(2)).origin_jets==3
    v=translate('multiply',f,g);assert v.jets==v.origin_jets==0 and v.unit==2
    reject(lambda:assert_admissible(v))
def test_units_domains_modulation_and_global_promotion_are_guarded():
    f=Word(F(1),jets=1)
    reject(lambda:translate('add',f,Word(F(1),unit=2)))
    reject(lambda:translate('P',Word(F(1),smooth=False)))
    reject(lambda:assert_admissible(translate('modulate',f,parameter=F(1))))
    assert assert_admissible(translate('phase',f))
    reject(lambda:allow_global_sign(tail_certified=True,schur_psd_certified=True))
    reject(lambda:allow_global_sign(all_supports=True,tail_certified=True))
def test_commutator_dx_and_position_independent_exact_polynomial_algebra():
    p=w.seed(3);xp=[F(0)]+p
    difference=w.add(w.derivative(xp),w.scale([F(0)]+w.derivative(p),-1))
    assert difference==p
    P=lambda a:w.add(w.derivative(a,2),w.scale(a,F(-1,4)))
    assert w.add(P(xp),w.scale([F(0)]+P(p),-1))==w.scale(w.derivative(p),2)
def test_protocol_is_frozen_and_numeric_labels_never_claim_interval_certificate():
    data=read('v644_family_resultats.json');p=D/'v644_protocole_traductions.json'
    assert data['protocol_sha256']==hashlib.sha256(p.read_bytes()).hexdigest() and data['complete'] and not data['zero_data_used']
    assert data['status']=='numerical_exploration_not_interval_certificate'
    with mp.workdps(80):
      for r in data['supports']:
        assert mp.mpf(r['precision_relative_matrix_difference'])<mp.mpf('1e-25')
        assert mp.mpf(r['precision_absolute_eigen_min_difference'])<mp.mpf('1e-25')
        assert mp.mpf(r['precision_absolute_schur_ratio_difference'])<mp.mpf('1e-25')
def test_integer_tail_is_computed_with_exact_ceil_and_valid_budget():
    for r in read('v644_contrats_queue_entiers.json')['contracts']:
        assert r['L_upper']==8+2*r['prime_power_count'] and r['J']==8*r['L_upper']
        q=int(r['q']);z=6*F(r['S'])*(1<<r['J']);assert F(q-1)<z<=q
        assert F(r['coercivity_lower'])==F(1,1+2*r['L_upper'])
        assert F(r['eta_upper'])+F(r['coercivity_lower'])==1
        assert q>=1 and r['r_lower']==1+2*r['L_upper']
def test_dictionary_register_coverage_distinct_symbols_and_provenance():
    data=read('v644_dictionnaire.json');rows=data['entries'];assert len({r['id'] for r in rows})==len(rows)
    spec=importlib.util.spec_from_file_location('navigator_for_dictionary',ROOT/'2_Methode/Navigateur/build_navigateur.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    legacy=[r for r in rows if r['kind']=='metaphor'];assert len(legacy)==95 and {r['name'] for r in legacy}==set(m.operators())
    assert all(r['image'] and r['exact'] and r['guard'] and r['source'] for r in rows)
    ids={r['id'] for r in rows};assert {'math:g_symbols','math:p_operator','math:projector','math:polynomial','math:origin_jets','math:quotient_jets'}<=ids
def test_current_registry_covers_69_documents_and_matches_sources():
    # A later phase may update active pages; inspect the current source registry.
    r=read('v650_decisions.json' if (D/'v650_decisions.json').exists() else 'v649_decisions.json' if (D/'v649_decisions.json').exists() else 'v648_decisions.json' if (D/'v648_decisions.json').exists() else ('v647_decisions.json' if (D/'v647_decisions.json').exists() else ('v646_decisions.json' if (D/'v646_decisions.json').exists() else ('v645_decisions.json' if (D/'v645_decisions.json').exists() else 'v644_decisions.json'))))
    assert r['coverage']['presentation_documents']>=69
    assert sorted(x['numero'] for x in r['documents'])==list(range(1,r['coverage']['presentation_documents']+1))
    # V6.58 : registre déclaré historique (data/registres_historiques_v650.json) ; plus de comparaison au corpus courant.
    from historique_v650 import verifier_instantane, verifier_sources_historiques
    verifier_instantane('v650_decisions.json' if (D/'v650_decisions.json').exists() else 'v644_decisions.json'); verifier_sources_historiques(r)
