"""Exhaustive file inventory; it records coverage, not independent mathematical validation."""
from pathlib import Path
import hashlib
import json
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '3_Preuves_et_calculs/data/v638_inventaire.json'

def main():
    rows = []
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or '__pycache__' in p.parts or p.suffix == '.pyc' or p == OUT:
            continue
        rel = str(p.relative_to(ROOT))
        if p.name == 'CHECKSUMS.sha256':
            continue
        rows.append({'path': rel, 'size_bytes': p.stat().st_size,
                     'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
                     'family': rel.split('/')[0] if '/' in rel else 'entrees',
                     'extension': p.suffix})
    out = {'version': 'V6.38', 'scope': 'File inventory of the delivered corpus, excluding this self-referential inventory and checksum file.',
           'file_count': len(rows), 'family_counts': dict(Counter(x['family'] for x in rows)),
           'semantic_review': '61 presentation documents plus selected proof/review annexes; see v638_decisions.json.',
           'limitations': ['Hashes and inventory do not constitute independent verification of all mathematics or all external citations.',
                           'Machine-readable numerical data were inventoried; calculations are verified through the appropriate test suite.'],
           'files': rows}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
    print('Inventory:', len(rows), 'files')

if __name__ == '__main__':
    main()
