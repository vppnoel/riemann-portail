#!/usr/bin/env python3
"""Horodatage d'une version livrée : preuve d'antériorité sans rien publier.

python -B 2_Methode/Horodatage/horodater_version.py      # à lancer à chaque livraison, APRÈS la mise à jour de CHECKSUMS.sha256

Le script fige une copie de CHECKSUMS.sha256 (qui couvre tout le corpus) sous le nom CHECKSUMS_<version>.sha256
et l'inscrit au registre. Sur GitHub, le flux .github/workflows/horodater.yml envoie ensuite l'empreinte de cette
copie aux calendriers OpenTimestamps (seule l'empreinte part, jamais le contenu) et dépose la preuve
CHECKSUMS_<version>.sha256.ots à côté ; il la complète chaque jour jusqu'à son ancrage dans la chaîne Bitcoin.
Une e-Soleau (INPI) reste à faire à la main aux moments importants ; elle s'inscrit au registre sous « esoleau ».
Idempotent. Auteur et titulaire des droits : Vincent NOËL.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REG = HERE / 'registre_horodatages.json'


def main():
    version = json.loads((ROOT / 'VERSION_LIVRAISON.json').read_text(encoding='utf-8-sig'))['version']
    src = ROOT / 'CHECKSUMS.sha256'
    fige = HERE / f'CHECKSUMS_{version}.sha256'
    reg = json.loads(REG.read_text(encoding='utf-8')) if REG.exists() else dict(
        schema='horodatages_v1', _lisez_moi="Une entrée par version livrée. La copie figée de CHECKSUMS.sha256 couvre tous les fichiers de la version ; "
        "son fichier .ots (OpenTimestamps) prouve qu'elle existait à la date d'ancrage. Vérifier : ots verify CHECKSUMS_<version>.sha256.ots, "
        "puis sha256sum -c CHECKSUMS_<version>.sha256 sur une archive de la version.", versions=[], esoleau=[])
    if any(v['version'] == version for v in reg['versions']):
        e = next(v for v in reg['versions'] if v['version'] == version)
        if hashlib.sha256(fige.read_bytes()).hexdigest() != e['sha256']: raise SystemExit(f'{fige.name} a changé depuis son inscription : refusé.')
        print(json.dumps(dict(deja_inscrite=version, sha256=e['sha256']))); return
    shutil.copyfile(src, fige)
    h = hashlib.sha256(fige.read_bytes()).hexdigest()
    reg['versions'].append(dict(version=version, fichier=fige.name, sha256=h, fichiers_couverts=sum(1 for _ in fige.open(encoding='utf-8')),
                                fige_le=datetime.now(timezone.utc).isoformat(timespec='seconds'), preuve=fige.name + '.ots'))
    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(inscrite=version, sha256=h)))


if __name__ == '__main__':
    main()
