"""Audit independent identities, outward bounds and analytic promotion guards."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,importlib.util
import mpmath as mp
from unittest import TestCase
import prime_centered_bridge as b
import symbolic_weil_family as w
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'3_Preuves_et_calculs/data'
def read(name):return json.loads((D/name).read_text(encoding='utf-8-sig'))
def bounds(v):return tuple(b.endpoint_q(t) for t in v['binary'])
def test_uniform_negative_base_uses_independent_exact_dilations():
    certificate=b.uniform_negative_base_certificate();assert certificate['negative_certified']
    assert certificate['scope'].startswith('continuous base B0 only')
    coefficients=list(map(F,certificate['upper_over_S_coefficients']))
    assert F(certificate['uniform_upper_over_S'])==F(-14112607,4704860160)<0
    for S in (F(16),F(17),F(64),F(321,2)):
        row=b.negative_base_bound(S)
        polynomial=sum(coefficients[j]/S**(2*j) for j in range(4))
        assert F(row['rational_upper'])/S==polynomial<=F(certificate['uniform_upper_over_S'])
def test_continuum_and_seed_energy_independent_polynomial_integrals():
    b.setup()
    for S,i in ((F(1,2),0),(F(3),2)):
        p=w.prime_powers(int(mp.floor(mp.exp(2*w.mpq(S)))));v=b.prime_residual_intervals(S,i,i,p)
        energy=w.integral_even(w.mul(w.derivative(w.seed(i)),w.derivative(w.seed(i))))/S+S*w.integral_even(w.mul(w.seed(i),w.seed(i)))/4
        assert v['seed']==energy and b.lo(v['continuum'])<=-energy<=b.hi(v['continuum'])
def test_all_saved_interval_paths_overlap_and_preserve_parity():
    count=0
    for r in read('v645_arithmetique_resultats.json')['supports']:
        for e in r['entries']:
            count+=1;a,z=bounds(e['residual']);c,d=bounds(e['ibp']);assert a<=d and c<=z
            low,up=bounds(e['continuum']);assert low<=-F(e['seed_energy_exact'])<=up
            if (e['i']+e['j'])%2:
                assert bounds(e['prime'])==bounds(e['residual'])==(F(0),F(0))
    assert count==144
def test_budget_recomputes_integer_products_and_geometric_ceilings():
    b.setup()
    for row,old in zip(read('v645_arithmetique_resultats.json')['supports'],read('v644_family_resultats.json')['supports']):
        S=F(row['S']);powers=[tuple(x) for x in old['prime_powers']];r=b.norm_budgets(S,powers,row['cutoff'])
        assert row['chain_lengths']==r['chain_lengths']
        assert F(row['chosen_L_upper'])==r['chosen_upper']
        assert r['chosen_upper']<=b.hi(r['raw']) and b.hi(r['row'])<=b.hi(r['raw'])
        for n,(p,m,power) in zip(r['chain_lengths'],powers):
            t=mp.log(power);assert (n-1)*t<2*w.mpq(S)<=n*t
def test_multiplier_interval_contains_independent_digamma_at_large_T():
    b.setup()
    for T in (2,64,1<<121):
        r=b.multiplier_enclosure(T,64)
        actual=mp.re(mp.digamma(mp.mpf('0.25')+mp.j*T/2))-mp.digamma(mp.mpf('0.25'))
        assert w.mpq(b.lo(r))<=actual<=w.mpq(b.hi(r))
        assert b.hi(r)-b.lo(r)<=F(2*T*T)/(F(257,2)*(F(257,2)**2+T*T))+F(1,10**100)
def test_improved_tail_keeps_every_fraction_and_actual_order():
    for row in read('v645_arithmetique_resultats.json')['supports']:
        t=row['tail'];L=F(t['L_upper']);r=F(t['r_lower']);beta=F(t['beta_upper']);mu=F(t['mu_lower'])
        assert r>2*L and beta==F(12,11)/r and mu==1-L*beta>F(5,11)
        z=6*F(row['S'])*(1<<t['J']);q=int(t['q']);assert q-1<z<=q
        assert len(str(q))==t['q_digits']<t['old_q_digits']
        assert F(t['residual_debt_factor_upper'])==beta/mu
def test_schur_source_contract_survives_nonorthogonal_head_change():
    # Exact two-dimensional form [[3,1],[1,2]], tail R=mass=1.
    # h -> h+tail/2 changes H and source but not the exact Schur 5/2.
    for H,c in ((F(3),F(1)),(F(9,2),F(2))):
        result=b.residual_matrix_contract([[H]],[[c*c]],1,2)
        assert result['lower_matrix']==[['5/2']] and result['algebraic_psd']
        assert result['global_RH_claim'] is False
def test_source_contract_robust_errors_account_for_Gram_and_sources():
    result=b.residual_matrix_contract([[4]],[[1]],1,2,F(1,4),F(1,8),[F(1,2)],1)
    # C_up=2*(1+1/8)+2*(1/2)^2=11/4.
    assert result['lower_matrix']==[['19/8']] and result['algebraic_psd']
    exact=b.residual_matrix_contract([[4]],[[1]],1,2,F(1,4),F(1,8),[0],1)
    assert exact['lower_matrix']==[['51/16']]
def test_invalid_source_Gram_and_tail_contracts_are_rejected():
    for kwargs in ({'mu':0},{'beta':-1},{'delta_H':-1},{'delta_C':-1},{'source_errors':[-1]},{'theta':0}):
        params=dict(beta=1,mu=1);params.update(kwargs)
        with TestCase().assertRaises(ValueError):b.residual_matrix_contract([[1]],[[1]],**params)
    with TestCase().assertRaises(ValueError):b.residual_matrix_contract([[1]],[[-1]],1,1)
    with TestCase().assertRaises(ValueError):b.residual_matrix_contract([[1,1],[0,1]],[[1,0],[0,1]],1,1)
def test_negative_sufficient_bound_is_not_promoted_to_RH_refutation():
    result=b.residual_matrix_contract([[0]],[[1]],1,1)
    assert result['algebraic_psd'] is False and result['global_RH_claim'] is False
def test_protocol_and_labels_separate_validated_and_exploratory_scopes():
    r=read('v645_arithmetique_resultats.json')
    assert r['protocol_sha256']==hashlib.sha256((D/'v645_protocole_arithmetique.json').read_bytes()).hexdigest()
    assert r['complete'] and not r['zero_data_used']
    assert 'no full Schur' in r['exploratory_scope']
    assert all('not computed' in x['tail']['status'] for x in r['supports'])
    assert r['uniform_negative_base_certificate']['scope'].startswith('continuous base B0 only')
def test_current_dictionary_supplements_history_and_index_parses_all_code():
    old=read('v644_dictionnaire.json')['entries'];cur=read('v645_dictionnaire.json')['entries']
    assert cur[:len(old)]==old and len(cur)==len(old)+13
    assert len({r['id'] for r in cur})==len(cur)
    assert {'math:source_schur','math:chebyshev_delta','math:source_graph_guard'}<={r['id'] for r in cur}
    spec=importlib.util.spec_from_file_location('ast645check',ROOT/'2_Methode/Outils/build_v644_dictionary.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    fresh=m.code_inventory();saved=read('v650_index_fonctions.json' if (D/'v650_index_fonctions.json').exists() else 'v649_index_fonctions.json' if (D/'v649_index_fonctions.json').exists() else 'v648_index_fonctions.json' if (D/'v648_index_fonctions.json').exists() else ('v647_index_fonctions.json' if (D/'v647_index_fonctions.json').exists() else ('v646_index_fonctions.json' if (D/'v646_index_fonctions.json').exists() else 'v645_index_fonctions.json')))
    # V6.58 : l'index V6.50 est un instantané historique ; l'index courant doit seulement se lire sans erreur.
    from historique_v650 import verifier_instantane
    assert not fresh['parse_errors'] and saved['parse_errors'] == []
    verifier_instantane('v650_index_fonctions.json' if (D/'v650_index_fonctions.json').exists() else 'v645_index_fonctions.json')
def test_current_registry_and_global_progress_match_research_scope():
    current='v650' if (D/'v650_decisions.json').exists() else 'v649' if (D/'v649_decisions.json').exists() else 'v648' if (D/'v648_decisions.json').exists() else 'v647' if (D/'v647_decisions.json').exists() else 'v646' if (D/'v646_decisions.json').exists() else 'v645'
    registry=read(current+'_decisions.json');assert registry['coverage']['numbers']==list(range(1,registry['coverage']['presentation_documents']+1))
    # V6.58 : registre et état déclarés historiques ; l'étape de l'indicateur est vérifiée à sa place dans l'historique.
    from historique_v650 import verifier_instantane, verifier_sources_historiques, verifier_etape_indicateur
    verifier_instantane(current+'_decisions.json'); verifier_sources_historiques(registry)
    state=read(current+'_etat_recherche.json');assert state['global_sign_certified'] is False and state['maturity_levels_unchanged']
    verifier_instantane(current+'_etat_recherche.json'); verifier_etape_indicateur(current)
