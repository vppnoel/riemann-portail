"""Ajoute la marque d'ordre des octets UTF-8 (BOM) à tous les fichiers .md du corpus.

Auteur et titulaire des droits : Vincent NOËL.
Pourquoi : un fichier .md ouvert directement dans un navigateur ou un éditeur Windows n'annonce pas son encodage ;
sans BOM, ces programmes supposent souvent l'ancien encodage Windows-1252 et affichent « Ã© » au lieu de « é ».
Avec le BOM, ils reconnaissent l'UTF-8. GitHub, pandoc et les scripts du corpus (lecture en « utf-8-sig ») l'acceptent.
Idempotent. Usage : python 2_Methode/Outils/md_utf8_bom.py [--verifier]
"""
from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]; BOM = b"\xef\xbb\xbf"


def fichiers():
    # 4_Archives/recus : documents reçus, conservés sans aucune modification
    return sorted(p for p in ROOT.rglob("*.md") if "node_modules" not in p.parts and "recus" not in p.parts)


def main():
    sans = [p for p in fichiers() if not p.read_bytes().startswith(BOM)]
    if "--verifier" in sys.argv:
        print(f"{len(sans)} fichier(s) .md sans BOM"); sys.exit(1 if sans else 0)
    for p in sans:
        b = p.read_bytes(); b.decode("utf-8")          # refuse un fichier qui ne serait pas de l'UTF-8 valide
        p.write_bytes(BOM + b)
    print(f"BOM ajouté à {len(sans)} fichier(s) ; {len(fichiers())} fichiers .md au total")


if __name__ == "__main__":
    main()
