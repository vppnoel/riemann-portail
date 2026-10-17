"""Recompile les six PDF révisés en V6.34 (pandoc, XeLaTeX et pdfLaTeX).

Usage : python 2_Methode/Outils/build_v634_pdfs.py [--only 58|articles|47|51|56]
Les sources Markdown et LaTeX restent les sources éditoriales autoritaires.
"""
from pathlib import Path
import argparse,subprocess,tempfile,shutil
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'1_Presentation'
STEMS={
 '47':'47_LE_RIEMANN_ROCH_VIRTUEL',
 '51':'51_J3B_LE_FROBENIUS_DE_CARACTERISTIQUE_UN',
 '56':'56_LE_RELIEF_DE_L_ARCHIPEL',
 '58':'58_VALIDATION_DIRECTE_DU_RELIEF_ET_LEMME_DES_JETS'}
HEADER=r'''
\usepackage{etoolbox}
\usepackage{microtype}
\setlength{\emergencystretch}{3em}
\AtBeginEnvironment{longtable}{\footnotesize}
\AtBeginDocument{\hypersetup{colorlinks=true,linkcolor=blue!45!black,urlcolor=blue!45!black}}
'''

def main():
 p=argparse.ArgumentParser();p.add_argument('--only',choices=[*STEMS,'articles']);a=p.parse_args()
 with tempfile.TemporaryDirectory(prefix='riemann_v634_pdf_') as tmp:
  tmp=Path(tmp);header=tmp/'header.tex';header.write_text(HEADER)
  for key,stem in STEMS.items():
   if a.only and a.only!=key:continue
   cmd=['pandoc',stem+'.md','--pdf-engine=xelatex','--resource-path=.',
        '--include-in-header='+str(header),'-V','geometry:margin=18mm',
        '-V','papersize=a4','-V','mainfont=DejaVu Sans','-V','monofont=DejaVu Sans Mono',
        '-V','fontsize=10pt','-V','lang=fr-FR','-o',str(tmp/(stem+'.pdf'))]
   if key=='58':cmd+=['--lua-filter='+str(Path(__file__).with_name('layout_v634.lua'))]
   subprocess.run(cmd,cwd=P,check=True)
   shutil.copy2(tmp/(stem+'.pdf'),P/(stem+'.pdf'));print('PDF :',stem,flush=True)
  if not a.only or a.only=='articles':
   for stem in ('article1_mean_square_double_poles','article2_prime_side_weil_forms'):
    for _ in range(2):
     r=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',
            '-output-directory='+str(tmp),stem+'.tex'],cwd=P/'articles',capture_output=True,text=True)
     if r.returncode:raise RuntimeError(r.stdout[-4000:]+r.stderr)
    shutil.copy2(tmp/(stem+'.pdf'),P/'articles'/(stem+'.pdf'));print('PDF :',stem,flush=True)
if __name__=='__main__':main()
