"""Finite numerical certificates lift through explicit whole-domain lemmas."""
from pathlib import Path
from fractions import Fraction as F
from unittest import TestCase
import json,hashlib,importlib.util
import mpmath as mp
import certificate_lego as l
import prime_centered_bridge as b
from schur_bridge import psd
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'3_Preuves_et_calculs/data'
def read(n):return json.loads((D/n).read_text(encoding='utf-8-sig'))
def first():return read('v646_lego_resultats.json')['supports'][0]
def module(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_protocol_hash_and_support_scope_remain_explicit():
    r=read('v646_lego_resultats.json');assert r['complete'] and not r['zero_data_used']
    assert r['protocol_sha256']==hashlib.sha256((D/'v646_protocole_lego.json').read_bytes()).hexdigest()
    c=r['supports'][0]['certificate'];assert c['status']=='certified_local_all_tests' and c['head_dimension']==0 and not c['global_RH_claim']
    assert c['support_range']=='0 < S <= 347/1000'
def test_projected_norm_formulas_against_independent_integrals():
    b.setup(160);S=F(347,1000);s=b.midpoint(b.I(S))
    for t in (F(0),F(3,8),F(6),F(12)):
        pair=l.projection_diagonal(S,t);tt=b.midpoint(b.I(t))
        cosnorm=mp.quad(lambda x:mp.cos(tt*x)**2,[-s,s]);sinnorm=mp.quad(lambda x:mp.sin(tt*x)**2,[-s,s])
        cp=mp.quad(lambda x:mp.cosh(x/2)*mp.cos(tt*x),[-s,s]);sp=mp.quad(lambda x:mp.sinh(x/2)*mp.sin(tt*x),[-s,s])
        actual=[cosnorm-cp**2/(s+mp.sinh(s)),sinnorm-sp**2/(mp.sinh(s)-s)]
        for v,a in zip(pair,actual):assert b.midpoint(v)-a<mp.mpf('1e-40') and a-b.midpoint(v)<mp.mpf('1e-40')
def test_frequency_traces_enclose_independent_quadrature():
    row=first();S=mp.mpf(347)/1000
    with mp.workdps(55):
        def d(t,p):
            z=mp.mpf('.5')+mp.j*t;v=2*mp.sinh(z*S)/z
            si=mp.sin(2*t*S)/(2*t) if t else S
            return S+(si if p==0 else -si)-(v.real**2/(S+mp.sinh(S)) if p==0 else v.imag**2/(mp.sinh(S)-S))
        for r in (row['layers']['rows'][0],row['layers']['rows'][15],row['layers']['rows'][-1]):
            T=F(r['T']);tt=mp.mpf(T.numerator)/T.denominator
            for p in range(2):
                actual=mp.quad(lambda x:d(x,p),[0,tt])/mp.pi
                assert actual<=mp.mpf(F(r['kappa_upper'][p]).numerator)/F(r['kappa_upper'][p]).denominator
def test_multiplier_increments_bound_independent_digamma():
    b.setup(160)
    for r in first()['layers']['rows']:
        T=F(r['T']);lower,upper=l.multiplier_increment(T-F(3,8),T)
        actual=mp.re(mp.digamma(mp.mpf('.25')+mp.j*b.midpoint(b.I(T))/2)-mp.digamma(mp.mpf('.25')+mp.j*b.midpoint(b.I(T-F(3,8)))/2))
        assert b.midpoint(b.I(b.lo(lower)))<=actual<=b.midpoint(b.I(b.hi(upper)))
def test_layer_assembly_keeps_quadrature_error_and_every_term():
    for r in read('v646_lego_resultats.json')['supports']:
        f=r['layers'];S=F(r['S']);M=4*S*S;h=F(f['microstep']);acc=[F(0),F(0)]
        assert F(f['lipschitz_upper'])==M
        for j,e in enumerate(f['rows'],1):
            assert F(e['T'])==j*F(3,8) and F(e['quadrature_error_numerator'])==M*F(e['T'])*h/4
            dl=F(e['increment_lower']);assert dl>=0
            for p in range(2):acc[p]+=dl*(1-min(F(1),F(e['kappa_upper'][p])))
            assert list(map(F,e['lambda_cumulative_lower']))==acc
        assert F(f['lambda_lower'])==min(acc)
def test_boundary_potential_and_prime_cutoff_are_correct():
    b.setup(160);S=F(347,1000);a=mp.log(2);delta=2*b.midpoint(b.I(S))-a
    assert 0<delta<b.midpoint(b.I(S)) and 2*b.midpoint(b.I(S))<mp.log(3)
    for d in (b.midpoint(b.I(S)),delta,a):
        closed=l.J_interval(mp.iv.mpf([d,d]));actual=mp.quad(lambda t:mp.exp(-t/2)/(1-mp.exp(-2*t)),[d,1,mp.inf])
        assert abs(b.midpoint(closed)-actual)<mp.mpf('1e-40')
def test_readable_five_inequalities_give_exact_positive_theorem():
    r=read('v646_lego_resultats.json')['rounded_uniform_certificate']
    alpha=F(r['alpha']);la=F(r['lambda_lower']);v0=F(r['v0_lower']);v1=F(r['v1_lower']);w=F(r['weight_upper']);c0=F(r['c0_upper'])
    assert alpha*(v1-v0)-w==F(133,16000)>0
    c=(1-alpha)*la+alpha*v0-c0;assert c==F(321,8000)>F(1,25)
    assert c/(c+c0+w+1)==F(107,18411)>F(1,200)
    assert 1/(1+la)==F(40,271)<F(3,20)
def test_joint_blend_succeeds_where_independent_penalty_fails():
    c=first()['certificate'];assert F(c['independent_floor_lower'])<0<F(c['mass_floor_lower'])
    assert F(c['mu_R_lower'])>0 and F(c['beta_R_upper'])>0
def test_larger_supports_are_inconclusive_not_refutations():
    for r in read('v646_lego_resultats.json')['supports'][1:]:
        assert r['certificate']['status']=='inconclusive' and not r['certificate']['global_RH_claim']
def test_ports_refuse_wrong_forms_shifts_units_and_sample_scope():
    b.setup(160);port=l.Port(F(347,1000));bricks=l.boundary_bricks(port,F(first()['layers']['lambda_lower']))
    for kwargs in ({'form':'arbitrary'},{'mass_shift':1},{'form':'Q_W_minus_eta_mass','mass_shift':0}):
        with TestCase().assertRaises(ValueError):l.Port(port.S,**kwargs)
    bad=l.Brick('energy',l.Port(F(348,1000)),bricks[0].payload)
    with TestCase().assertRaises(ValueError):l.assemble_local_certificate(bad,*bricks[1:])
    bad=l.Brick('energy',port,bricks[0].payload,all_tests=False)
    with TestCase().assertRaises(ValueError):l.assemble_local_certificate(bad,*bricks[1:])
    with TestCase().assertRaises(ValueError):l.boundary_bricks(port,F(6),eta=1)
    for kwargs in ({'unit':'A_amp'},{'metric':'H1'},{'annihilators':('1',)}):
        with TestCase().assertRaises(ValueError):l.assemble_local_certificate(*l.boundary_bricks(l.Port(port.S,**kwargs),F(6)))
    with TestCase().assertRaises(ValueError):l.assemble_local_certificate(l.Brick('source',port,bricks[0].payload),*bricks[1:])
def test_bounded_family_never_promoted_to_unbounded_coverage():
    with TestCase().assertRaises(ValueError):l.request_unbounded_coverage(first()['certificate'])
def test_source_projection_is_joint_Loewner_optimal_algebra():
    r=l.project_source_gram([[5,2],[2,2]],[[2,1]],[[1]])
    assert r['residual_gram']==[['1','0'],['0','1']]
    assert r['removed_gram']==[['4','2'],['2','1']] and psd(r['removed_gram'])
    # A different correction adds the rank-one Gram of [1,-1].
    other=[[F(2),F(-1)],[F(-1),F(2)]]
    assert psd([[other[i][j]-F(r['residual_gram'][i][j]) for j in range(2)] for i in range(2)])
    with TestCase().assertRaises(ValueError):l.project_source_gram([[1]],[[2]],[[1]])
    with TestCase().assertRaises(ValueError):l.project_source_gram([[1]],[[1]],[[0]])
def test_negative_control_is_a_declared_modified_model():
    r=read('v646_lego_resultats.json')['perturbed_negative_control']
    assert r['negative_witness_certified'] and F(r['shifted_witness_upper_per_mass'])<0
    assert r['certificate_response']['status']=='inconclusive' and r['certificate_response']['form']=='Q_W_minus_eta_mass'
    assert F(r['certificate_response']['mass_shift'])==F(r['eta']) and not r['certificate_response']['global_RH_claim']
def test_joint_Fourier_diagnostic_stays_exploratory_with_actual_refinement():
    r=read('v646_fourier_joint_diagnostic.json');assert not r['certified'] and not r['new_positive_certificate'] and not r['global_RH_claim']
    last=r['supports'][-1];assert last['S']=='1/2' and [x['Nfrequency'] for x in last['resolutions']]==[40000,80000]
    q=last['resolutions'][-1];assert q['monotone_envelope_margin']<q['separate_geometric_margin']<q['sublevel_joint_margin']<0
def test_progressive_dictionary_has_readable_math_and_acyclic_prerequisites():
    p=read('v646_parcours_pedagogique.json');assert len(p['lessons'])==32 and len(p['stages'])==5
    seen=set()
    for r in p['lessons']:
        assert set(r['prerequisites'])<=seen;seen.add(r['id'])
        assert r['meaning'] and r['example'] and r['purpose'] and r['guard']
        assert (ROOT/r['math_file']).exists() and r['math_svg'] and r['math_height']>0 and r['math_width']>0
    assert all(x['input'] and x['output'] and x['execution'] and x['limit'] for x in p['tools'])
def test_current_registry_index_and_four_doors_are_consistent():
    current='v650' if (D/'v650_decisions.json').exists() else 'v649' if (D/'v649_decisions.json').exists() else 'v648' if (D/'v648_decisions.json').exists() else 'v647' if (D/'v647_decisions.json').exists() else 'v646'
    registry=read(current+'_decisions.json');assert registry['coverage']['numbers']==list(range(1,registry['coverage']['presentation_documents']+1))
    # V6.58 : registre et index déclarés historiques (data/registres_historiques_v650.json).
    from historique_v650 import verifier_instantane, verifier_sources_historiques
    verifier_instantane(current+'_decisions.json'); verifier_instantane(current+'_index_fonctions.json'); verifier_sources_historiques(registry)
    fresh=module('index646check',ROOT/'2_Methode/Outils/build_v644_dictionary.py').code_inventory()
    assert not fresh['parse_errors']
    state=read(current+'_etat_recherche.json');assert len(state['next_actions'])==len(state['four_doors'])==4 and not state['global_sign_certified']
