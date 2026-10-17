"""Document63: decision, quantitative witnesses, complete proof and LaTeX source."""
from pathlib import Path
import json
import subprocess
import tempfile
import shutil

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'1_Presentation'
D=ROOT/'3_Preuves_et_calculs/data'
STEM='63_CONTRAINTES_EXACTES_V13'

def main():
    cert=json.loads((D/'v639_contraintes.json').read_text())
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    fig,ax=plt.subplots(figsize=(9,4.5))
    radii=('9/20','pi/6','13/20','3/4')
    for j,k in enumerate((1,3,5)):
        rows=[next(x for x in cert['minor_witnesses'] if x['character_k']==k and x['radius']==r) for r in radii]
        vals=[(float(x['gap_D']['lower'])+float(x['gap_D']['upper']))/2 for x in rows]
        ax.plot(range(4),vals,'o-',label=f'Ancre χ{k}')
    ax.axhline(.25,color='#9c443c',linestyle='--',label='Ancien seuil0,25')
    ax.set_xticks(range(4),['0,45','π/6','0,65','0,75'])
    ax.set_xlabel('Rayon exact en radians')
    ax.set_ylabel('Écart construit |D− − D+|')
    ax.set_title('Variation de D à coefficient complexe fixé\nTémoins choisis parmi10 triplets ; aucun comptage de zéros')
    ax.set_ylim(0,.28);ax.legend(loc='upper left',fontsize=9);ax.grid(alpha=.2)
    fig.tight_layout();fig.savefig(P/'63_Contrastes_D.png',dpi=170);plt.close(fig)
    lines=['# V6.39 - Contraintes exactes V13 : comparaison faisable','',
           '**Document63. Vincent P. P. NOËL. 12 octobre2026.**','',
           'Type : note de preuve, témoins reproductibles et décision expérimentale. La source LaTeX accompagne le PDF.','',
           '## 1. La décision obtenue','',
           '**La comparaison est faisable.** Pour chacune des six ancres de V13 et pour tout angle0<r<π/4, nous construisons deux fonctions ayant exactement le même coefficient complexe A=a(1), la même ancre et la même distance, mais des défauts de multiplicativité D différents.','',
           'Cela établit un point précis : dans cette famille construite, D n’est pas déterminé par le seul coefficient A, l’ancre et le rayon. C’est un résultat mathématique local qui rend une comparaison contrôlée possible. Il ne dit encore rien sur la hauteur des zéros ni sur une relation causale.','',
           'La valeur fixée est A=cos(r)z_i, avec z_i la phase du caractère de l’ancre. Nous ne démontrons pas la faisabilité pour tout A complexe arbitraire, notamment toutes les anciennes valeurs de V6.37. Le coefficient est constant à l’intérieur de chaque paire, pas entre les strates.','',
           '## 2. Le mécanisme, en quelques lignes','',
           'Les six caractères impairs modulo13 forment trois paires conjuguées. Hors d’une ancre, deux paires restent disponibles. On combine leurs coordonnées pour obtenir une direction u qui vérifie exactement u_i=0, norme(u)=1 et somme_j u_j z_j=0.','',
           r'\[c_\pm=\cos(r)e_i\pm\sin(r)u.\]','',
           'Ces deux directions opposées conservent donc A=cos(r)z_i. Leurs autres coefficients changent : une attribution causale à D seul n’est pas acquise. L’ancre est unique parce que cos(r)>sin(r).','',
           r'\[ D(c_\pm)=D_0(r)\mp2\cos(r)\sin^3(r)P_i(u),\qquad D_0(r)=1+\cos^2r-2\cos^4r.\]','',
           'Le coefficient cubique P_i est démontré non nul. L’écart absolu vaut4cos(r)sin³(r)|P_i|>0. La non-annulation est certifiée par des inégalités rationnelles sur des sommes finies de Gauss, sans consulter de zéro et sans dépendre des fonctions transcendantes flottantes de mpmath.','',
           '## 3. Un exemple lisible, entièrement défini','',
           'À rayon r=π/6, on a cos(r)=√3/2, sin(r)=1/2 et D0=5/8 exactement. Les phases et les directions par mineurs sont algébriques, donc les deux vecteurs de coefficients de cet exemple le sont aussi. Les décimales ci-dessous servent à lire le résultat ; la définition exacte est conservée dans les recettes et l’annexe.','',
           '| Ancre | D bas, encadrement | D haut, encadrement | Écart, encadrement |','|:--|:--|:--|:--|']
    for k in (1,3,5):
        row=next(x for x in cert['minor_witnesses'] if x['character_k']==k and x['radius']=='pi/6')
        box=lambda key:f"[{row[key]['lower']}; {row[key]['upper']}]"
        lines.append(f"| χ{k} | {box('D_plus')} | {box('D_minus')} | {box('gap_D')} |")
    lines+=['','Pour l’ancre χ1, les deux objets ont le même A=(√3/2)z1 mais D≈0,591417 et D≈0,658583. La différence≈0,067166 est contrôlée. Le témoin par mineurs utilise les caractères5,9,11 hors de l’ancre ; sa normalisation et son signe sont définis analytiquement.','',
            '## 4. Contrastes et limites du futur dessin','',
            'Les rayons historiques sont repris sous leurs valeurs nominales exactes9/20,13/20,3/4 ; il ne s’agit pas d’identifier ces réels aux anciens paramètres binary64. Le rayonπ/6 fournit un contrôle algébrique supplémentaire.','',
            '- Témoins par paires conjuguées : écarts entre0,008834 et0,058427 sur les rayons nominaux historiques.',
            '- Témoins sélectionnés parmi10 triplets hors ancre : écarts entre0,029444 et0,143781.',
            '- Les48 paires de témoins calculées (deux familles, six ancres, quatre rayons) sont des constructions ; elles ne sont pas des observations indépendantes de zéros.',
            '- Les six ancres se ramènent à trois classes conjuguées par rayon pour un observable symétrique en valeur absolue de la hauteur.',
            '- Aucun des témoins construits n’atteint l’ancien seuil0,25 ; aucun maximum global sur la sphère admissible n’est démontré.','',
            '![Écarts construits entre les deux scores D. Seules les trois ancres représentatives sont tracées. Le seuil0,25 est celui de V6.37.](63_Contrastes_D.png)','',
            'À petit rayon, l’écart est d’ordre r³ tandis que le centre D0 est d’ordre r². Un seuil de contraste constant masque donc nécessairement cette construction près de l’ancre.','',
            '## 5. Ce qui a été vérifié','',
            'Les identités, le rang exact trois, la sphère admissible de dimension deux et la non-constance sont démontrés dans l’annexe. Les sommes de Gauss sont encadrées par deux méthodes : fractions exactes (Machin, Taylor et racine carrée entière), puis intervalles mpmath à80/120décimales pour les valeurs fines.','',
            'Une lecture indépendante a recoupé618 enclosures par précision, vérifié l’emboîtement120 dans80 avec fractions exactes, puis recalculé96 valeurs de D par la définition originelle sur12×12 classes à160décimales. Cette seconde formule est indépendante de la réduction cubique. Les parties réelles des nombres racines et leurs parties imaginaires ont également été contrôlées par le certificat rationnel.','',
            'Les vecteurs binary64 exportés ne vérifient les égalités qu’à tolérance numérique. Les objets exacts sont ceux définis par les recettes Gauss, paires ou mineurs et normalisation ; les décimales exportées ne remplacent pas cette définition.','',
            '## 6. Prochaine étape concrète','',
            'La prochaine expérience doit comparer des couples à contraintes exactes, avec trois ancres représentatives et un seuil adapté aux écarts disponibles. Un reçu analytique prépare12 couples par mineurs sur quatre rayons, sans aucun résultat de zéros. Le seuil de contraste proposé0,025 est inférieur aux contrastes déjà établis ; il doit être conservé avant de lancer les nouveaux comptages.','',
            'Pour chaque couple, comparer la première tranche où le détecteur relève un déficit, avec contours raffinés, racines recoupées et non-détections conservées. Une détection numérique ne certifie pas l’absence de racines antérieures. Si une relation subsiste, elle restera une association conditionnelle avant toute explication causale ou théorème uniforme.','',
            'Aucun comptage de zéros n’a été effectué dans cette étape1. L’étude des valeurs de A arbitraires, les contrastes maximaux et le mécanisme arithmétique imposant RH restent ouverts.','',
            '## 7. Fichiers et reproduction','',
            '- Recettes et résultats : ../3_Preuves_et_calculs/data/v639_contraintes.json.',
            '- Certificat rationnel : ../3_Preuves_et_calculs/data/v639_certificat_rationnel.json.',
            '- Précision120 : ../3_Preuves_et_calculs/data/v639_contraintes_precision120.json.',
            '- Relecture : ../3_Preuves_et_calculs/preuves/RELECTURE_CONTRAINTES_V13_V639.md.',
            '- Reçu de la future comparaison : ../3_Preuves_et_calculs/data/v639_couples_fixes.json.',
            '- Calcul reproductible : python3_Preuves_et_calculs/scripts/run_v639_contraintes.py.',
            '- Document reproductible : python2_Methode/Outils/build_v639_document.py.','',
            '## Annexe - Démonstration complète','']
    proof=(ROOT/'3_Preuves_et_calculs/preuves/LEMME_CONTRAINTES_V13_V639.md').read_text(encoding='utf-8-sig')
    # Keep the proof complete while making its headings subordinate to the report.
    proof='\n'.join('### '+line[3:] if line.startswith('## ') else line for line in proof.splitlines()[2:])
    text='\n'.join(lines)+'\n'+proof+'\n'
    for a,b in {'Document63':'Document 63','octobre2026':'octobre 2026','angle0':'angle 0','modulo13':'modulo 13',
                'vaut4cos':'vaut 4cos','caractères5,9,11':'caractères 5, 9, 11','exactes9/20':'exactes 9/20',
                'rayonπ/6':'rayon π/6','entre0':'entre 0','et0':'et 0','parmi10':'parmi 10','Les48':'Les 48',
                'seuil0,25':'seuil 0,25','à80/120décimales':'à 80/120 décimales','recoupé618':'recoupé 618',
                'l’emboîtement120 dans80':'l’emboîtement 120 dans 80','recalculé96':'recalculé 96','sur12×12':'sur 12×12',
                'à160décimales':'à 160 décimales','prépare12':'prépare 12','proposé0,025':'proposé 0,025',
                'étape1':'étape 1','Précision120':'Précision 120','python3_':'python 3_','python2_':'python 2_'}.items():text=text.replace(a,b)
    (P/(STEM+'.md')).write_text(text,encoding='utf-8-sig')
    header=r'''\usepackage{etoolbox}
\usepackage{microtype}
\setlength{\emergencystretch}{3em}
\AtBeginEnvironment{longtable}{\small}
\AtBeginDocument{\hypersetup{colorlinks=true,linkcolor=blue!45!black,urlcolor=blue!45!black}}
'''
    with tempfile.TemporaryDirectory(prefix='v639_document_') as directory:
        tmp=Path(directory);(tmp/'header.tex').write_text(header)
        args=['pandoc',STEM+'.md','-s','-f','markdown+tex_math_single_backslash',
              '--resource-path=.','--include-in-header='+str(tmp/'header.tex'),
              '-V','geometry:margin=19mm','-V','papersize=a4','-V','mainfont=DejaVu Sans',
              '-V','monofont=DejaVu Sans Mono','-V','fontsize=10pt','-V','lang=fr-FR',
              '-o',STEM+'.tex']
        run=subprocess.run(args,cwd=P,capture_output=True,text=True)
        logs=run.stdout+run.stderr
        if run.returncode:raise RuntimeError(logs)
        for _ in range(2):
            run=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(tmp),STEM+'.tex'],cwd=P,capture_output=True,text=True)
            logs+=run.stdout+run.stderr
            if run.returncode:
                (D/'v639_pdf_compile.log').write_text(logs);raise RuntimeError(logs[-5000:])
        (D/'v639_pdf_compile.log').write_text(logs)
        shutil.copy2(tmp/(STEM+'.pdf'),P/(STEM+'.pdf'))
    print('Document63 PDF, Markdown and standalone LaTeX generated')

if __name__=='__main__':main()
