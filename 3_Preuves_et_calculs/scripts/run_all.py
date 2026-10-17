#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))

from experiments import (
    verify_c_identity, apollo_trajectory, weighted_energy_vs_diagonal,
    local_fourier_energy, gcd_covariance_validation, kalman_information,
)

OUT=ROOT/'data'
OUT.mkdir(exist_ok=True)

jobs={
    'verify_c_identity.csv': verify_c_identity(),
    'apollo_trajectory.csv': apollo_trajectory(),
    'weighted_energy_vs_diagonal.csv': weighted_energy_vs_diagonal(),
    'local_fourier_energy.csv': local_fourier_energy(),
    'gcd_covariance_validation.csv': gcd_covariance_validation(),
    'kalman_information.csv': kalman_information(),
}

for name,df in jobs.items():
    df.to_csv(OUT/name,index=False)
    print(f'Wrote {name}: {len(df)} rows')
