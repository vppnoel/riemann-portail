#!/usr/bin/env python3
"""Diagnostics for the energy-dimension / generalized-fractal-string module."""
from pathlib import Path
import sys, math
import numpy as np
import pandas as pd
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from energy_dimension import (
    effective_dimension_from_Q, dimension_from_log_slope,
    finite_energy_zeta, finite_complex_dimensions, finite_model_B,
    signed_rh_modes,
)
from explicit_formula import load_zeros, _coeffs
from rh_core import KAPPA

OUT = ROOT / 'data'

# 1) Finite-scale dimension estimator on measured zeta energy.
df = pd.read_csv(OUT / 'explicit_vs_measured.csv')
df2 = df[['X','Q_mesuree']].copy()
df2['D_E_effective'] = effective_dimension_from_Q(df2['X'].to_numpy(), df2['Q_mesuree'].to_numpy())
Qref = (4*KAPPA/3.0) * np.log(df2['X'].to_numpy())**3
df2['D_E_RH_leading_reference'] = effective_dimension_from_Q(df2['X'].to_numpy(), Qref)
df2.to_csv(OUT / 'energy_dimension_zeta.csv', index=False)

# 2) Reinterpret existing rejection-growth slopes as effective dimensions.
r = pd.read_csv(OUT / 'rejection_growth.csv')
r2 = r[['objet','N','pente_logQ_logX_derniere_decade']].copy()
r2['D_from_slope'] = dimension_from_log_slope(r2['pente_logQ_logX_derniere_decade'])
r2.to_csv(OUT / 'energy_dimension_rejection.csv', index=False)

# 3) Exact finite-zero meromorphic model vs numerical quadrature.
gam, c0 = load_zeros(3)
A, u = _coeffs(gam, c0)
rho, Avec, uvec = signed_rh_modes(gam, A, u)
s = 0.84 + 0.17j
exact = finite_energy_zeta(s, rho, Avec, uvec)

def fpart(t, imag=False):
    B = finite_model_B(np.array([t]), rho, Avec, uvec)[0]
    val = B*B*np.exp(-2*(s-0.5)*t)
    return float(val.imag if imag else val.real)

num = quad(lambda t: fpart(t, False), 0, np.inf, limit=400)[0] + 1j*quad(lambda t: fpart(t, True), 0, np.inf, limit=400)[0]
pd.DataFrame([{
    's_re': s.real, 's_im': s.imag,
    'exact_re': exact.real, 'exact_im': exact.imag,
    'quad_re': num.real, 'quad_im': num.imag,
    'abs_error': abs(exact-num),
}]).to_csv(OUT / 'energy_zeta_finite_validation.csv', index=False)

# 4) Sample complex dimensions of the finite RH model and one synthetic off-line pair.
poles = finite_complex_dimensions(rho)
samp = pd.DataFrame({'model':'RH_3zeros','pole_re':poles.real,'pole_im':poles.imag})
beta, gamma = 0.63, 7.0
rho_off = np.array([beta+1j*gamma, beta-1j*gamma])
poles_off = finite_complex_dimensions(rho_off)
samp2 = pd.DataFrame({'model':'synthetic_offline','pole_re':poles_off.real,'pole_im':poles_off.imag})
pd.concat([samp,samp2], ignore_index=True).to_csv(OUT/'energy_complex_dimensions_sample.csv', index=False)

print('energy_dimension_zeta.csv')
print(df2.to_string(index=False))
print('\nenergy_dimension_rejection.csv')
print(r2.to_string(index=False))
print('\nfinite model validation error:', abs(exact-num))
print('RH finite pole real-part range:', poles.real.min(), poles.real.max())
print('off-line synthetic poles:', poles_off)
