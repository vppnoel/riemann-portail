"""Exact recipes, independent defect definition, branch and negative controls."""
from pathlib import Path
from fractions import Fraction
import json
import numpy as np
import sympy as sp
from euler_archipelago import characters
from v639_contraintes import (exact_phases, antisymmetric_direction, contains,
                             conj, enclosure, endpoint_fraction, lo)
from v639_rational import gauss_enclosures

DATA=Path(__file__).resolve().parents[1]/'data'


def test_gauss_branches_and_historical_convention():
    eps,z=exact_phases(70)
    coarse=((.522,.523),(.289,.291),(-.039,-.038))
    for i,(a,b) in enumerate(coarse):
        assert a<float(eps[i].real.a) and float(eps[i].real.b)<b
    for i,ch in enumerate(characters(13,1)):
        value=complex(float(z[i].real.mid),float(z[i].imag.mid))
        assert abs(value-np.exp(-1j*ch['phi']))<2e-14
        assert lo(z[i].real)>0 and not contains(eps[i].imag)


def test_kernel_rank_dimension_and_exact_recipe():
    eps,z=exact_phases(70)
    for i in range(6):
        u,p,recipe=antisymmetric_direction(z,i)
        j,js=recipe['pairs'][0]
        det=(conj(z[j])*z[js]).imag
        assert not contains(det)
        assert contains(det-eps[j].imag)
        assert contains(u[i]) and not contains(p)
        assert contains(sum(v*v for v in u),1)
        A=sum((z[j]*u[j] for j in range(6)),z[0]*0)
        assert contains(A.real) and contains(A.imag)


def test_three_column_relation_symbolic_without_interval_code():
    x1,x2,x3,y1,y2,y3=sp.symbols('x1 x2 x3 y1 y2 y3')
    M=sp.Matrix([[x1,x2,x3],[y1,y2,y3]])
    v=sp.Matrix([x2*y3-y2*x3,x3*y1-y3*x1,x1*y2-y1*x2])
    assert all(sp.expand(t)==0 for t in M*v)


def test_dimension_three_does_not_alone_imply_variation():
    # Toy phases (1,1,1,i,i,i), anchored at the first coordinate.
    # Kernel u=(0,a,-a,b,c,-b-c) has dimension3 but P=u1^3+u2^3=0.
    a,b,c=sp.symbols('a b c',real=True)
    u=sp.Matrix([0,a,-a,b,c,-b-c])
    M=sp.Matrix([[1,0,0,0,0,0],[1,1,1,0,0,0],[0,0,0,1,1,1]])
    assert M.rank()==3 and M*u==sp.zeros(3,1)
    assert sp.expand(u[1]**3+u[2]**3)==0


def test_defect_from_independent_group_average():
    cert=json.loads((DATA/'v639_contraintes.json').read_text())
    chars=characters(13,1)
    n=np.arange(1,13)
    chi=np.array([[ch['table'][int(k)] for k in n] for ch in chars])
    chi_prod=np.array([[ch['table'][int((m*k)%13)] for m in n for k in n] for ch in chars])
    phase=np.exp(-1j*np.array([ch['phi'] for ch in chars]))
    for row in cert['conjugate_pair_witnesses']+cert['minor_witnesses']:
        for vector,key in zip(row['exported_binary64_vectors'],('D_plus','D_minus')):
            b=np.array(vector)*phase
            A=b.sum();values=b@chi;products=(b@chi_prod).reshape(12,12)
            D=np.mean(abs(A*products-np.outer(values,values))**2)/np.sum(abs(b)**2)**2
            expected=(float(row[key]['lower'])+float(row[key]['upper']))/2
            assert abs(D-expected)<2e-11


def test_outward_decimal_boxes_are_actual_enclosures():
    _,z=exact_phases(70)
    for x in [z[0].real,z[2].imag,z[3].imag]:
        e=enclosure(x,12)
        assert Fraction(e['lower'])<=endpoint_fraction(x._mpi_[0])
        assert Fraction(e['upper'])>=endpoint_fraction(x._mpi_[1])


def test_strata_gaps_scope_and_no_zeros():
    cert=json.loads((DATA/'v639_contraintes.json').read_text())
    assert cert['zero_counting_performed'] is False and cert['causal_inference'] is False
    for family in ('conjugate_pair_witnesses','minor_witnesses'):
        assert len(cert[family])==24
        assert {(x['anchor_index'],x['radius']) for x in cert[family]}=={(i,r) for i in range(6) for r in ('9/20','13/20','3/4','pi/6')}
        for row in cert[family]:
            assert 0<Fraction(row['gap_D']['lower'])<Fraction(row['gap_D']['upper'])<Fraction(1,4)
            C=np.array(row['exported_binary64_vectors'])
            t=C[0,row['anchor_index']]
            assert np.argmax(abs(C[0]))==row['anchor_index']
            assert np.argmax(abs(C[1]))==row['anchor_index']
            assert t>np.max(abs(np.delete(C[0],row['anchor_index'])))


def test_rational_gauss_certificate_without_float_backend():
    pi,root,rows=gauss_enclosures()
    assert Fraction(314159,100000)<pi[0]<pi[1]<Fraction(314160,100000)
    assert root[0]**2<13<root[1]**2
    coarse=((Fraction(522,1000),Fraction(523,1000)),
            (Fraction(289,1000),Fraction(291,1000)),
            (Fraction(-39,1000),Fraction(-38,1000)))
    for i,(a,b) in enumerate(coarse):
        assert a<rows[i]['real'][0]<=rows[i]['real'][1]<b
    for row in rows:
        assert row['imag'][0]>0 or row['imag'][1]<0
