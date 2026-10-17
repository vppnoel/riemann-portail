"""Contrôles numériques des contours; témoins qui peuvent réellement échouer."""
from pathlib import Path
import json,sys,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from relief_direct import DirectGrid,completed_phase_basis
from euler_archipelago import F_values

def test_direct_contour_agrees_with_known_euler_zero_counts():
    # Sous T=30, ces trois fonctions L ont chacune 24 zéros (±t compris).
    grid=DirectGrid(7,1,30,.02,3)
    total,critical,off,diag=grid.counts(np.eye(3))
    assert total[:,-1].tolist()==[24,24,24]
    assert np.array_equal(total,critical) and np.all(off==0)
    assert diag['unresolved_horizontal_rows']==0 and diag['max_integer_residual']<1e-8

def test_direct_contour_detects_a_pair_without_an_euler_reference():
    sel=json.loads((ROOT/'data/v634_selection_v7.json').read_text())
    c=np.array(next(r['coefficients'] for r in sel if r['id']=='bas_a1_min'))
    coarse=DirectGrid(7,1,12,.02,3);fine=DirectGrid(7,1,12,.01,3)
    t,z,off,diag=coarse.counts(c);tf,zf,offf,df=fine.counts(c)
    assert np.array_equal(t,tf) and np.array_equal(z,zf)
    assert np.flatnonzero(off[0]>0)[0]+1==9
    assert np.all(off>=0) and np.all(off%2==0)
    assert diag['unresolved_horizontal_rows']==df['unresolved_horizontal_rows']==0

def test_direct_completed_symmetry_and_root_partner():
    sel=json.loads((ROOT/'data/v634_selection_v7.json').read_text())
    c=np.array(next(r['coefficients'] for r in sel if r['id']=='col_a1_min'))
    roots=json.loads((ROOT/'data/v634_racines_recoupees.json').read_text())
    r=next(x for x in roots if x['id']=='col_a1_min')
    z=complex(float(r['beta_mp']),float(r['gamma_mp']))
    # Deux points hors droite s'annulent, indépendamment du comptage Hardy.
    vals=F_values(7,1,c,np.array([z,1-z.conjugate()]))
    assert np.max(np.abs(vals))<1e-9 and z.real>.5
    s=.5+1j*np.array([-9.3,2.7,17.2])
    assert np.max(np.abs(completed_phase_basis(7,1,s).imag))<1e-10

def test_dh_arithmetic_support_contains_non_prime_powers():
    from rejection import coeffs,log_derivative_coeffs,KAPPA_DH
    b=log_derivative_coeffs(coeffs('DH',12))
    assert abs(b[6]-(1+KAPPA_DH**2)*np.log(6))<1e-12
    assert abs(b[12])>.7

def test_independent_selection_and_contour_quality_are_preserved():
    s=json.loads((ROOT/'data/v634_selection_v11.json').read_text())
    C=np.array([r['coefficients'] for r in s if not r['euler']])
    rg=np.random.default_rng(6341101);expected=rg.normal(size=(96,5));expected/=np.linalg.norm(expected,axis=1)[:,None]
    assert np.array_equal(C,expected)
    for name,n in (('relief_v7',11),('independant_v11',101)):
        d=json.loads((ROOT/f'data/v634_{name}.json').read_text())
        assert d['nombres_stables_first']==n and d['niveaux_modifies']==0
        assert d['diagnostics']['unresolved_horizontal_rows']==0
        assert d['diagnostics']['max_ecart_enroulement_pas']<1e-8
        assert d['tous_pairs_nonnegatifs'] and d['euler_sans_hors_droite']
