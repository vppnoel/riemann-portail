"""Compile les trois articles et les documents 59 et 60 de V6.36."""
from pathlib import Path
import subprocess
import tempfile
import shutil

ROOT=Path(__file__).resolve().parents[2]
PRES=ROOT/"1_Presentation"
HEADER=r"""
\usepackage{etoolbox}
\usepackage{microtype}
\setlength{\emergencystretch}{3em}
\AtBeginEnvironment{longtable}{\small}
\AtBeginDocument{\hypersetup{colorlinks=true,linkcolor=blue!45!black,urlcolor=blue!45!black}}
"""
with tempfile.TemporaryDirectory(prefix="riemann_v636_pdf_") as folder:
    tmp=Path(folder)
    header=tmp/"header.tex"
    header.write_text(HEADER)
    for stem in ("59_DE_LA_TOUR_FINIE_A_LA_BORNE_SPECTRALE",
                 "60_ARTICLES_ET_CERTIFICAT_DE_NEGATIVITE"):
        subprocess.run(["pandoc",stem+".md","-f","markdown+tex_math_single_backslash",
            "--pdf-engine=xelatex","--resource-path=.","--include-in-header="+str(header),
            "-V","geometry:margin=18mm","-V","papersize=a4",
            "-V","mainfont=DejaVu Sans","-V","monofont=DejaVu Sans Mono",
            "-V","fontsize=10pt","-V","lang=fr-FR","-o",str(tmp/(stem+".pdf"))],
            cwd=PRES,check=True)
        shutil.copy2(tmp/(stem+".pdf"),PRES/(stem+".pdf"))
        print("PDF :",stem,flush=True)
    for stem in ("article1_mean_square_double_poles",
                 "article2_prime_side_weil_forms",
                 "article3_hasse_jets_and_spectral_bound"):
        for _ in range(3):
            res=subprocess.run(["pdflatex","-interaction=nonstopmode","-halt-on-error",
                "-output-directory="+str(tmp),stem+".tex"],cwd=PRES/"articles",
                capture_output=True,text=True)
            if res.returncode:
                raise RuntimeError(res.stdout[-4000:]+res.stderr)
        shutil.copy2(tmp/(stem+".pdf"),PRES/"articles"/(stem+".pdf"))
        (tmp/(stem+".log")).replace(ROOT/"3_Preuves_et_calculs/data"/(stem+"_v636_compile.log"))
        print("PDF :",stem,flush=True)
