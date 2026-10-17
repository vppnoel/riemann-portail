#!/usr/bin/env python3
"""Portable entry point: rerun the full V6.50 local certificate in a new folder.

Requires the NumPy/SciPy/mpmath dependencies in requirements.txt. Frozen
archive outputs are never overwritten. No known zeros are used.
"""
from pathlib import Path
import argparse,sys,importlib.util

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'3_Preuves_et_calculs/src'))
ARCHIVE=ROOT/'4_Archives/recus/V650/constructive'


def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s)
    sys.modules[name]=m;s.loader.exec_module(m);return m


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'3_Preuves_et_calculs/data/v650_reproduction')
    args=parser.parse_args();out=args.output.resolve()
    if out==ARCHIVE.resolve() or ARCHIVE.resolve() in out.parents:
        raise ValueError('a new output directory is required')
    out.mkdir(parents=True,exist_ok=True)
    r=load('reconstruction',ARCHIVE/'reconstruction.py');r.ROOT=out
    c=load('integral650',ARCHIVE/'tentative_certificat_integral.py');c.ROOT=out
    c.run()


if __name__=='__main__':main()
