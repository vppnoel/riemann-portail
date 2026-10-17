"""Compile le document 59 ; la preuve complète reste une annexe Markdown."""
from pathlib import Path
import subprocess
import tempfile
import shutil

ROOT = Path(__file__).resolve().parents[2]
PRES = ROOT / "1_Presentation"
STEM = "59_DE_LA_TOUR_FINIE_A_LA_BORNE_SPECTRALE"
HEADER = r"""
\usepackage{etoolbox}
\usepackage{microtype}
\setlength{\emergencystretch}{3em}
\AtBeginEnvironment{longtable}{\small}
\AtBeginDocument{\hypersetup{colorlinks=true,linkcolor=blue!45!black,urlcolor=blue!45!black}}
"""

with tempfile.TemporaryDirectory(prefix="riemann_v635_pdf_") as tmp:
    tmp = Path(tmp)
    header = tmp / "header.tex"
    header.write_text(HEADER)
    cmd = ["pandoc", STEM+".md", "-f", "markdown+tex_math_single_backslash",
           "--pdf-engine=xelatex", "--resource-path=.",
           "--include-in-header="+str(header), "-V", "geometry:margin=18mm",
           "-V", "papersize=a4", "-V", "mainfont=DejaVu Sans",
           "-V", "monofont=DejaVu Sans Mono", "-V", "fontsize=10pt",
           "-V", "lang=fr-FR", "-o", str(tmp/(STEM+".pdf"))]
    subprocess.run(cmd, cwd=PRES, check=True)
    shutil.copy2(tmp/(STEM+".pdf"), PRES/(STEM+".pdf"))
    print("PDF :", STEM)
