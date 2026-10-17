"""Compile le document 61 V6.37 à partir de son Markdown et de ses figures."""
from pathlib import Path
import subprocess
import tempfile
import shutil

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'1_Presentation'
STEM='61_ANCRAGE_APPARIE_V13'
HEADER=r'''
\usepackage{etoolbox}
\usepackage{microtype}
\setlength{\emergencystretch}{3em}
\AtBeginEnvironment{longtable}{\small}
\AtBeginDocument{\hypersetup{colorlinks=true,linkcolor=blue!45!black,urlcolor=blue!45!black}}
'''
with tempfile.TemporaryDirectory(prefix='riemann_v637_pdf_') as directory:
    tmp=Path(directory)
    (tmp/'header.tex').write_text(HEADER)
    result=subprocess.run(['pandoc',STEM+'.md','-f','markdown+tex_math_single_backslash',
        '--pdf-engine=xelatex','--resource-path=.','--include-in-header='+str(tmp/'header.tex'),
        '-V','geometry:margin=18mm','-V','papersize=a4','-V','mainfont=DejaVu Sans',
        '-V','monofont=DejaVu Sans Mono','-V','fontsize=10pt','-V','lang=fr-FR',
        '-o',str(tmp/(STEM+'.pdf'))],cwd=P,capture_output=True,text=True)
    (ROOT/'3_Preuves_et_calculs/data/v637_pdf_compile.log').write_text(result.stdout+result.stderr)
    if result.returncode:raise RuntimeError(result.stdout+result.stderr)
    shutil.copy2(tmp/(STEM+'.pdf'),P/(STEM+'.pdf'))
    print('PDF :',STEM,flush=True)
