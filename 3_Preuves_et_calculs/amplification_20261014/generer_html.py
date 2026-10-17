#!/usr/bin/env python3
"""Rebuild the integrated V6.55 note with native, offline MathML."""
from pathlib import Path
import subprocess
import tempfile
import importlib.util


DOSSIER = Path(__file__).resolve().parent
ROOT = DOSSIER.parents[1]
PRESENTATION = ROOT / "1_Presentation"
BASE = "ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55"

CSS = """
<style>
:root { color-scheme: light; }
html { background:#edf2f5; color:#172d3d; font-family:system-ui,-apple-system,"Segoe UI",sans-serif; line-height:1.7; }
body { max-width:1020px; margin:28px auto; padding:32px 44px 60px; background:#fff; border-radius:16px; }
h1,h2,h3 { color:#124f68; line-height:1.3; scroll-margin-top:24px; }
h1 { font-size:1.7rem; margin-top:2.6rem; }
h2 { font-size:1.3rem; margin-top:2rem; }
h3 { font-size:1.12rem; }
header .title { margin-top:1.1rem; font-size:2rem; }
header .subtitle { color:#526c7b; font-size:1.15rem; }
a { color:#075c83; text-underline-offset:.15em; overflow-wrap:anywhere; }
p,li { overflow-wrap:break-word; }
.resource-nav { display:flex; flex-wrap:wrap; gap:8px 18px; padding:14px 18px; background:#eaf3f7; border-radius:10px; }
.research-status { margin:18px 0 24px; padding:16px 18px; border-left:5px solid #9a5d16; background:#fff6e8; }
.research-status p { margin:.3em 0; }
#TOC { border:1px solid #d4e0e7; padding:18px 24px; background:#f5f8fa; border-radius:10px; margin:24px 0; }
#TOC ul { padding-left:1.25em; }
table { border-collapse:collapse; width:100%; margin:1.5rem 0; font-size:.95rem; }
th,td { padding:.7rem .8rem; border-bottom:1px solid #d3dfe6; text-align:left; vertical-align:top; }
th { background:#eaf3f7; }
pre { overflow-x:auto; padding:1rem; border:1px solid #d5e0e8; border-radius:8px; background:#f4f7fa; line-height:1.5; }
code { font-size:.92em; white-space:pre-wrap; }
blockquote { margin-left:0; padding:.4rem 1.2rem; border-left:4px solid #b4cbd5; background:#f4f8fa; }
math { font-family:"Cambria Math","STIX Two Math","Latin Modern Math",serif; }
math[display="block"] { display:block; max-width:100%; overflow-x:auto; overflow-y:hidden; margin:1.35rem 0; padding:.4rem .1rem; font-size:1.1em; }
math[display="inline"] { font-size:1.02em; }
img { max-width:100%; height:auto; }
.note-footer { border-top:1px solid #d3dfe6; margin-top:3rem; padding-top:1rem; color:#536b79; font-size:.93rem; }
@media (max-width:720px) {
  body { margin:0; padding:18px 16px 40px; border-radius:0; }
  header .title { font-size:1.7rem; }
  h1 { font-size:1.45rem; }
  table { display:block; max-width:100%; overflow-x:auto; }
  th,td { min-width:10rem; padding:.6rem; }
  math[display="block"] { font-size:1.02em; }
}
@media print {
  html { background:white; }
  body { max-width:none; margin:0; padding:0; }
  .resource-nav { display:none; }
  h1,h2,h3 { break-after:avoid; }
  table,pre,math[display="block"] { break-inside:avoid; }
}
</style>
"""

BEFORE = f"""
<nav class="resource-nav" aria-label="Documents et ressources">
<a href="../00_PORTAIL.html">Portail global V6.55</a>
<a href="{BASE}.pdf">PDF</a>
<a href="{BASE}.tex">Source LaTeX</a>
<a href="{BASE}.md">Source Markdown</a>
<a href="../3_Preuves_et_calculs/amplification_20261014/README.md">Programmes et résultats</a>
<a href="CORRELATIONS_IDENTITE_ET_ENERGIE.html">Base V6.54 : corrélations et énergie</a>
</nav>

"""

AFTER = """
<footer class="note-footer">
<p>Les programmes et résultats de l’essai se trouvent dans
<a href="../3_Preuves_et_calculs/amplification_20261014/README.md">le dossier d’amplification</a>.
Les calculs finis ne constituent pas une preuve de la borne à l’infini.</p>
<p>Cette page utilise MathML natif et un style intégré ; sa lecture mathématique ne dépend d’aucun CDN.</p>
</footer>
"""


def main():
    spec = importlib.util.spec_from_file_location("indicateur_amp", ROOT / "2_Methode/Indicateur/build_indicateur.py")
    bi = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bi)
    before = bi.topnav("amplification", "../") + BEFORE
    with tempfile.TemporaryDirectory(prefix="amplification_html_") as tmp:
        tmp = Path(tmp)
        for name, value in (("header.html", CSS), ("before.html", before), ("after.html", AFTER)):
            (tmp / name).write_text(value, encoding="utf-8")
        cmd = [
            "pandoc", str(PRESENTATION / f"{BASE}.md"),
            "--from", "markdown+tex_math_single_backslash", "--standalone", "--mathml",
            "--toc", "--toc-depth=2", "--metadata", "header-includes=",
            "--include-in-header", str(tmp / "header.html"),
            "--include-before-body", str(tmp / "before.html"),
            "--include-after-body", str(tmp / "after.html"),
            "--output", str(PRESENTATION / f"{BASE}.html"),
        ]
        subprocess.run(cmd, check=True)
    print(PRESENTATION / f"{BASE}.html")


if __name__ == "__main__":
    main()
