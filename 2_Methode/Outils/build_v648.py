"""Publish the bounded common-operator certificate and its reusable interfaces."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,csv,base64,importlib.util
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'1_Presentation';D=ROOT/'3_Preuves_et_calculs/data'
STEM='73_OPERATEUR_COMMUN_TETE_SOURCES_ET_QUEUE'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def module(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
def inventory():
    dictionary=read(D/'v647_dictionnaire.json');dictionary.update(version='V6.48',current_article='Document73 ; opérateur commun certifié')
    (D/'v648_dictionnaire.json').write_text(json.dumps(dictionary,ensure_ascii=False,indent=2)+'\n')
    data=module('index648',ROOT/'2_Methode/Outils/build_v644_dictionary.py').code_inventory();assert not data['parse_errors']
    (D/'v648_index_fonctions.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    with (D/'v648_index_fonctions.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['path','line','name','kind','signature','docstring','explanation_status']);w.writeheader();w.writerows(data['entries'])
def figure():
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
    nodes={'Q':(0,0,'Forme originale Q\nDomaine énergétique',False),
        'B':(3,0,'Minorant A = ηI − B\nB positif compact',False),
        'global':(6,0,'Multi-premiers et transport\nCouverture non bornée',True),
        'W':(0,-2,'Moments et Gram\nProjection exacte',False),
        'frame':(3,-2,'Cadre cardinal de Gauss\n80 directions ; reste contrôlé',False),
        'sources':(6,-2,'Même erreur δ\nSources + queue de A',False),
        'errors':(0,-4,'Intervalles et erreurs\nPoids, ondes, matrices',False),
        'head':(3,-4,'Tête en deux blocs 40 × 40\nBareiss en entiers exacts',False),
        'sign':(6,-4,'Certificat sur tous Xₛ\nS ≤ 1/2 ; Q ≥ m/250',False)}
    edges=[('Q','B',False),('W','frame',False),('B','frame',False),('frame','sources',False),
        ('frame','head',False),('errors','head',False),('head','sign',False),('sources','sign',False),('sign','global',True)]
    fig,ax=plt.subplots(figsize=(11,7));ax.set_xlim(-1.4,7.4);ax.set_ylim(-5.25,1.05);ax.axis('off');hw,hh=1.12,.48
    for a,b,dashed in edges:
        x,y,*_=nodes[a];xx,yy,*_=nodes[b];dx,dy=xx-x,yy-y;length=(dx*dx+dy*dy)**.5;ux,uy=dx/length,dy/length
        off=min((hw+.05)/abs(ux) if ux else 1e6,(hh+.05)/abs(uy) if uy else 1e6)
        ax.add_patch(FancyArrowPatch((x+off*ux,y+off*uy),(xx-off*ux,yy-off*uy),arrowstyle='-|>',mutation_scale=14,lw=1.5,color='#516b5e',linestyle='--' if dashed else '-',shrinkA=0,shrinkB=0,zorder=1))
    for x,y,label,open_ in nodes.values():
        ax.add_patch(FancyBboxPatch((x-hw,y-hh),2*hw,2*hh,boxstyle='round,pad=.05',facecolor='#fff0d9' if open_ else '#e0eee4',edgecolor='#668674',zorder=2));ax.text(x,y,label,ha='center',va='center',fontsize=10.7,color='#213d2f',zorder=3)
    ax.text(3,.84,'Une approximation certifie trois blocs',ha='center',fontsize=17,weight='bold',color='#1c4031')
    ax.text(3,-4.98,'Vert : raccord ou certificat local démontré. Orange : construction ouverte.\nSources certifiées : celles du minorant A. Sources fortes de Q : une autre obligation.',ha='center',fontsize=10.4,color='#435d4e')
    fig.tight_layout();fig.savefig(P/'73_GRAPHE_OPERATEUR_COMMUN.png',dpi=180);fig.savefig(P/'73_GRAPHE_OPERATEUR_COMMUN.svg');plt.close(fig)
def report():
    r=read(D/'v648_common_certificate_resultats.json')['certificate']
    error='| Erreur opératoire certifiée | Majorant décimal indicatif |\n|---|---|\n'
    for label,key in [('Poids conjoint et cellules','weight_error'),('Milieux du noyau','kernel_midpoint_error'),('Interpolation spatiale','spatial_operator_error'),('Arrondis matriciels','matrix_roundoff_norm_upper')]:error+='| '+label+' | '+format(float(F(r[key])),'.9g')+' |\n'
    error+='| Vecteurs pondérés, bloc pair | '+format(float(F(r['sample_operator_error'][0])),'.9g')+' |\n'
    error+='| Total, bloc pair | '+format(float(F(r['total_operator_errors'][0])),'.9g')+' |\n'
    table='| Quantité certifiée | Pair | Impair |\n|---|---|---|\n'
    for label,key in [('Norme B, majorant','norm_even_odd_upper'),('Erreur totale δ','total_operator_errors')]:table+='| '+label+' | '+' | '.join(format(float(F(v)),'.9f') for v in r[key])+' |\n'
    table+='| Marge massique sur les deux blocs | '+format(float(F(r['mass_floor_lower'])),'.9f')+' | même borne |\n'
    table+='| Marge dans R sur les deux blocs | '+format(float(F(r['mu_R_lower'])),'.9f')+' | même borne |\n'
    schur='| Contrat du minorant A | Pair | Impair |\n|---|---|---|\n'
    for label,key in [('Plancher de queue L²','tail_floor'),('Dette opératoire de Schur','debt_operator_upper'),('Marge de Schur','schur_floor')]:schur+='| '+label+' | '+' | '.join(format(float(F(x['assembly'][key])),'.9f') for x in r['head_source_tail_contracts'])+' |\n'
    text=(ROOT/'3_Preuves_et_calculs/preuves/V648_OPERATEUR_COMMUN_CERTIFIE.md').read_text(encoding='utf-8-sig')
    text=text.replace('{{ERROR_TABLE}}',error).replace('{{CERTIFICATE_TABLE}}',table).replace('{{SCHUR_TABLE}}',schur)
    (P/(STEM+'.md')).write_text(text,encoding='utf-8-sig');module('pdf648',ROOT/'2_Methode/Outils/build_v644.py').pdf(STEM)
def dashboard():
    r=read(D/'v648_common_certificate_resultats.json');bi=module('nav648',ROOT/'2_Methode/Indicateur/build_indicateur.py')
    pic='data:image/png;base64,'+base64.b64encode((P/'73_GRAPHE_OPERATEUR_COMMUN.png').read_bytes()).decode()
    css='body{margin:0;background:#f3f5ee;color:#223c30;font:17px/1.65 system-ui}main{max-width:1160px;margin:auto;padding:22px}.topnav{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:18px}header{background:#174334;color:white;padding:28px;border-radius:14px}header a{color:#dff1dd}h1,h2{line-height:1.25}a{color:#236c50}.panel{background:white;border:1px solid #cbdacc;border-radius:12px;padding:22px;margin:18px 0}.formula{font:27px/1.5 Georgia,serif;background:#e9f3e7;padding:20px;overflow:auto}.guard{padding:14px;border-left:5px solid #b88335;background:#fff2de}img{width:100%;height:auto}table{width:100%;border-collapse:collapse}td,th{padding:9px;border-bottom:1px solid #dae5d8;text-align:left}.row{display:flex;flex-wrap:wrap;gap:16px}input,select,button{font:inherit;padding:9px;border:1px solid #9daf9b;border-radius:7px}button{background:#e0edda;cursor:pointer}label{display:block}.muted{font-size:14px;color:#526b58}.scroll{overflow:auto}details{margin:16px 0}@media(max-width:650px){main{padding:10px}.panel{padding:14px}th,td{padding:5px;font-size:14px}}'
    body=f'''<header><h1>Un opérateur commun certifié</h1><p>V6.48 · une même approximation fournit la tête, les sources croisées et la queue du minorant.</p><p><a href="{STEM}.pdf">Article : huit lemmes et certificat · PDF</a> · <a href="{STEM}.tex">LaTeX</a> · <a href="69_LANGUE_DES_PASSAGES.html">Comprendre les briques</a></p></header>
<section class="panel"><h2>La couverture obtenue</h2><div class="formula">0 &lt; S ≤ 1/2 : Q<sub>W</sub>(f) ≥ ‖f‖<sub>2</sub><sup>2</sup>/250 &nbsp; et &nbsp; Q<sub>W</sub>(f) ≥ R(f)/2000.</div><p>Pour tous les tests complexes admissibles : support, deux moments nuls et énergie finie. R est la mesure quadratique masse + énergie. La couverture comprend l’espace infini entier.</p><p>Les bornes plus fortes de V6.47 sur S≤3/8 sont conservées. Le nouveau certificat couvre une boîte plus grande.</p><p class="guard">La famille de supports reste bornée. Multi-premiers, transport non borné et sources fortes de la forme originale restent à construire.</p></section>
<section class="panel"><h2>Le coup double devient un raccord exécuté</h2><p>Le Gram des moments donne les ondes projetées. Le cadre de Gauss conserve leurs accords polynomiaux. Une erreur sur tout l’opérateur borne aussi la queue et ses attaches à la tête. Le signe du minorant se transporte vers Q_W.</p><img src="{pic}" alt="Graphe de l’opérateur, du cadre, de l’erreur et des trois blocs certifiés"></section>
<section class="panel"><h2>Inspecter les deux blocs</h2><label>Parité <select id="parity"><option value="0">Paire</option><option value="1">Impaire</option></select></label><div id="budgets" aria-live="polite" class="scroll"></div><p class="muted">Les décimales sont indicatives. Matrices entières, intervalles, fractions et déterminants principaux sont conservés dans le journal.</p></section>
<section class="panel"><h2>Quelles sources sont certifiées ?</h2><label>Objet étudié <select id="source-form"><option value="A">Minorant borné A_U</option><option value="Q">Forme originale Q_W</option></select></label><p id="source-status" aria-live="polite"></p><p>La différence Q_W−A_U est positive, généralement non bornée. Une implication de signe conserve son sens ; elle ne transforme pas les sources de A_U en sources exactes de Q_W.</p></section>
<section class="panel"><h2>Raccorder un support et une métrique</h2><div class="row"><label>Support S <input id="support" type="number" value="0.5" step="0.025" min="0"></label><label>Métrique finale <select id="metric"><option value="R">R = masse + énergie</option><option value="H1">H¹</option></select></label><label>Unité de la forme <select id="unit"><option value="A2">A_amp²</option><option value="A">A_amp</option></select></label></div><button id="connect">Vérifier le raccord</button><p id="connection" aria-live="polite"></p></section>
<section class="panel"><h2>Comment la matrice devient une preuve</h2><p>Le solveur numérique propose un plafond. Bareiss vérifie en entiers exacts que ce plafond moins la matrice est strictement positif. Les restes d’interpolation et les erreurs du poids, du noyau et du calcul matriciel étendent ensuite le majorant à l’espace infini.</p><details><summary>Le modèle d’arithmétique et ses gardes</summary><p>Intervalles scalaires, opérations binaire64 arrondies vers l’extérieur et budgets de produits matriciels sont déclarés. Aucun sinus de NumPy ni digamma flottante ne participe au certificat. Les nœuds et les poids de Gauss sont eux-mêmes encadrés. Ce dispositif n’est pas un assistant de preuve formelle.</p></details></section>
<section class="panel"><h2>Prochaine construction</h2><p>Construire le coût conjoint multi-premiers, puis une règle qui transporte les garanties entre supports. La brique réutilisable reçoit une approximation finie et son erreur globale ; elle fournit ensemble tête, Gram des sources, queue et dette.</p><p><a href="72_CONCENTRATION_PROJETEE.html">Étape V6.47 : concentration et pont commun</a> · <a href="71_LEGO_REUTILISABLE.html">Étape V6.46 : premier assemblage</a></p></section>
<footer><p><a href="../3_Preuves_et_calculs/data/v648_common_certificate_resultats.json">Journal complet</a> · <a href="../3_Preuves_et_calculs/data/v648_protocole_operateur_commun.json">Protocole figé</a> · <a href="../3_Preuves_et_calculs/data/v648_common_operator_diagnostic.json">Diagnostic distinct</a></p></footer>'''
    js=r'''const D=JSON.parse(document.getElementById('common-data').textContent),el=id=>document.getElementById(id);const q=rationalDisplay;
function budgets(){const p=Number(el('parity').value),r=D.certificate,c=r.head_source_tail_contracts[p].assembly;const rows=[['Dimension de tête',r.parity_head_dimensions[p]],['Plafond de matrice τ',q(r.finite_matrix_certificates[p].tau)],['Erreur totale δ',q(r.total_operator_errors[p])],['Norme entière B, majorant',q(r.norm_even_odd_upper[p])],['Queue du minorant, plancher',q(c.tail_floor)],['Gram source, majorant opératoire',q(c.source_gram_operator_upper)],['Dette de Schur, majorant',q(c.debt_operator_upper)],['Marge de Schur, minorant',q(c.schur_floor)]];el('budgets').innerHTML='<table><tr><th>Quantité</th><th>Valeur indicative</th></tr>'+rows.map(([n,v])=>'<tr><td>'+n+'</td><td>'+(Number.isInteger(v)?v:v.toFixed(9))+'</td></tr>').join('')+'</table>';}
function sources(){el('source-status').textContent=el('source-form').value==='A'?'Certifié : sources croisées du minorant A_U dans son cadre orthonormal L², Gram ≤ δ²I.':'Sources fortes de Q_W non calculées ici. Le signe de Q_W est néanmoins certifié par son minorant A_U.';}
function connect(){const s=Number(el('support').value);el('connection').textContent=!(s>0&&Number.isFinite(s))?'Raccord refusé : support strictement positif requis.':el('metric').value!=='R'||el('unit').value!=='A2'?'Raccord refusé : métrique ou unité incompatible.':s<=.5?'Raccord valide par inclusion : Q_W ≥ masse/250 et R/2000.':'Support hors de la couverture certifiée ; nouveau contrat nécessaire.';}
el('parity').addEventListener('change',budgets);el('source-form').addEventListener('change',sources);el('connect').addEventListener('click',connect);budgets();sources();connect();window.commonOperatorDashboard={budgets,sources,connect};'''
    js=(ROOT/'2_Methode/Outils/rational_display.js').read_text()+js
    payload=json.dumps(r,ensure_ascii=False).replace('</',r'<\/')
    (P/'73_OPERATEUR_COMMUN.html').write_text('<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V6.48 · Opérateur commun certifié</title><style>'+css+'</style></head><body><main>'+bi.topnav('graphe','../')+body+'</main><script id="common-data" type="application/json">'+payload+'</script><script>'+js+'</script></body></html>')
def main():
    sys.path.insert(0,str(ROOT/'2_Methode/Outils'));inventory();figure();report();module('pedagogy648',ROOT/'2_Methode/Outils/build_v648_pedagogy.py').build();dashboard()
if __name__=='__main__':main()
