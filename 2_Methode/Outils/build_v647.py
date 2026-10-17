"""Document72, operator graph, progressive vocabulary and recorded diagnostics."""
from pathlib import Path
import sys,json,importlib.util,base64,csv
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'1_Presentation';D=ROOT/'3_Preuves_et_calculs/data'
STEM='72_CONCENTRATION_PROJETEE_ET_OPERATEUR_COMMUN'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def module(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
def inventory():
    dictionary=read(D/'v646_dictionnaire.json');dictionary['version']='V6.47'
    dictionary['current_article']='document72 ; concentration projetée et opérateur commun'
    write(D/'v647_dictionnaire.json',dictionary)
    data=module('index647',ROOT/'2_Methode/Outils/build_v644_dictionary.py').code_inventory()
    assert not data['parse_errors'];write(D/'v647_index_fonctions.json',data)
    with (D/'v647_index_fonctions.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['path','line','name','kind','signature','docstring','explanation_status']);w.writeheader();w.writerows(data['entries'])
def figure():
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
    nodes={'projection':(0,0,'Moments et projection\nGram commun',False),
        'sublevel':(3,0,'Coût énergie/premier\nSous-niveaux de b',False),
        'common':(6,0,'Opérateur commun\nMême test dans les couches',False),
        'sources':(0,-2,'Gram des sources\nProjection optimale',False),
        'hs':(3,-2,'Concentration Schatten-2\nInteractions des fréquences',False),
        'head':(6,-2,'Tête et sources réelles\nNorme infinie à certifier',True),
        'errors':(0,-4,'Cellules et erreurs C²\nIntervalles + entiers exacts',False),
        'certificate':(3,-4,'Certificat : S ≤ 3/8\nQ ≥ masse/12 et R/100',False),
        'transport':(6,-4,'Couverture non bornée\nTransport + nouveaux premiers',True)}
    edges=[('projection','sublevel',False),('projection','sources',False),('sublevel','hs',False),
        ('sublevel','common',False),('errors','hs',False),('hs','certificate',False),
        ('common','head',True),('sources','head',True),('head','transport',True),('certificate','transport',True)]
    fig,ax=plt.subplots(figsize=(11,7));ax.axis('off');ax.set_xlim(-1.4,7.4);ax.set_ylim(-5.2,1.05)
    hw,hh=1.12,.48
    for a,b,dash in edges:
        x,y,*_=nodes[a];xx,yy,*_=nodes[b];dx,dy=xx-x,yy-y;length=(dx*dx+dy*dy)**.5;ux,uy=dx/length,dy/length
        off=min((hw+.05)/abs(ux) if ux else 1e6,(hh+.05)/abs(uy) if uy else 1e6)
        ax.add_patch(FancyArrowPatch((x+off*ux,y+off*uy),(xx-off*ux,yy-off*uy),arrowstyle='-|>',mutation_scale=14,lw=1.5,color='#526a60',linestyle='--' if dash else '-',shrinkA=0,shrinkB=0,zorder=1))
    for x,y,label,open_ in nodes.values():
        ax.add_patch(FancyBboxPatch((x-hw,y-hh),2*hw,2*hh,boxstyle='round,pad=.05',facecolor='#fff0d8' if open_ else '#e0eee4',edgecolor='#698677',zorder=2))
        ax.text(x,y,label,ha='center',va='center',fontsize=10.8,color='#203b30',zorder=3)
    ax.text(3,.83,'Une projection, plusieurs portes',fontsize=17,weight='bold',ha='center',color='#1d4031')
    ax.text(3,-4.97,'Vert : lemme démontré ou certificat local. Orange : hypothèses à certifier.\nPointillé : raccord conditionnel. Les sources générales et la couverture globale restent ouvertes.',ha='center',fontsize=10.5,color='#465e50')
    fig.tight_layout();fig.savefig(P/'72_GRAPHE_CONCENTRATION.png',dpi=180);fig.savefig(P/'72_GRAPHE_CONCENTRATION.svg');plt.close(fig)
def report():
    r=read(D/'v647_concentration_resultats.json')['certificate'];diag=read(D/'v647_operator_diagnostic.json')
    table='| Quantité encadrée | Valeur décimale indicative |\n|---|---|\n'
    for label,key in [('Énergie jointe, bloc pair','joint_energy_even_odd_lower'),('Énergie jointe, bloc impair','joint_energy_even_odd_lower')]:
        p=0 if label.endswith('pair') and not label.endswith('impair') else 1
        table+='| '+label+' | '+format(float(F(r[key][p])),'.9f')+' |\n'
    for label,key in [('Seuil C₀+2w₂, majorant','threshold_upper'),('Marge massique, minorant','mass_floor_lower'),('Marge dans R, minorant','mu_R_lower'),('Marge avec trace seule, minorant','trace_only_mass_floor')]:
        table+='| '+label+' | '+format(float(F(r[key])),'.9f')+' |\n'
    dt='| Diagnostic uniquement | S=3/8 | S=1/2 |\n|---|---|---|\n'
    for label,key in [('Trace par couches','trace'),('Schatten-2 par couches','schatten2'),('Norme de Nyström par couches','operator'),('Norme de Nyström de l’opérateur commun','common_operator'),('Schatten-2 de l’opérateur commun','common_schatten2')]:
        dt+='| '+label+' | '+' | '.join(format(x['resolutions'][-1]['margins'][key],'+.6f') for x in diag['supports'])+' |\n'
    text=(ROOT/'3_Preuves_et_calculs/preuves/V647_CONCENTRATION_PROJETEE.md').read_text(encoding='utf-8-sig')
    text=text.replace('{{CERTIFICATE_TABLE}}',table).replace('{{DIAGNOSTIC_TABLE}}',dt)
    (P/(STEM+'.md')).write_text(text,encoding='utf-8-sig')
    module('pdf647',ROOT/'2_Methode/Outils/build_v644.py').pdf(STEM)
def dashboard():
    r=read(D/'v647_concentration_resultats.json');diag=read(D/'v647_operator_diagnostic.json');bi=module('nav647',ROOT/'2_Methode/Indicateur/build_indicateur.py')
    pic='data:image/png;base64,'+base64.b64encode((P/'72_GRAPHE_CONCENTRATION.png').read_bytes()).decode()
    css='body{margin:0;background:#f3f5ef;color:#233c30;font:17px/1.65 system-ui}main{max-width:1160px;margin:auto;padding:22px}.topnav{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:18px}header{background:#164234;color:white;border-radius:14px;padding:28px}header a{color:#e1f1de}h1,h2{line-height:1.25}a{color:#226c50}.panel{background:white;border:1px solid #cbdacc;border-radius:12px;padding:22px;margin:18px 0}.math{font-family:Georgia,serif;font-size:27px;background:#e9f3e7;padding:20px;overflow:auto}.guard{padding:14px;border-left:5px solid #bb8336;background:#fff2de}img{width:100%;height:auto}table{border-collapse:collapse;width:100%}td,th{padding:9px;text-align:left;border-bottom:1px solid #dce6da}.scroll{overflow:auto}input,button,select{font:inherit;padding:9px;border:1px solid #9cae9c;border-radius:7px}button{cursor:pointer;background:#e1eddc}.row{display:flex;flex-wrap:wrap;gap:15px}label{display:block}.muted{font-size:14px;color:#526a59}@media(max-width:650px){main{padding:10px}.panel{padding:14px}td,th{padding:5px;font-size:14px}}'
    body=f'''<header><h1>Le Lego des concentrations</h1><p>V6.47 · certificat sur tous les tests jusqu’à S=3/8, et pont vers un opérateur commun.</p><p><a href="{STEM}.pdf">Article et huit lemmes · PDF</a> · <a href="{STEM}.tex">LaTeX</a> · <a href="69_LANGUE_DES_PASSAGES.html">Dictionnaire progressif</a></p></header>
<section class="panel"><h2>Ce qui est démontré</h2><div class="math">0 &lt; S ≤ 3/8 : &nbsp; Q<sub>W</sub>(f) ≥ ‖f‖<sub>2</sub><sup>2</sup>/12 &nbsp; et &nbsp; Q<sub>W</sub>(f) ≥ R(f)/100.</div><p>Les deux moments s’annulent et l’énergie est finie. La preuve couvre toutes les fonctions complexes de ce domaine, de dimension infinie. R est la mesure quadratique masse + énergie ; sa racine est la norme.</p><p class="guard">La couverture est bornée. Les sources des têtes générales et une règle atteignant tous les supports restent à construire. Le certificat ne prouve pas RH.</p></section>
<section class="panel"><h2>Pourquoi les nouvelles pièces servent</h2><p>La phase du premier2 reste dans le coût conjoint. Les fréquences de faible coût peuvent former plusieurs bandes. La concentration tient maintenant compte de leurs accords, avec la même projection que celle des sources. Cela donne une borne plus précise que la trace seule.</p><img src="{pic}" alt="Graphe des lemmes, de la concentration et des deux raccords ouverts"></section>
<section class="panel"><h2>Inspecter une couche du journal exact</h2><label>Niveau de coût u <input id="level" type="range" min="0.02" max="7.2" step="0.02" value="6.8"></label><div id="layer" aria-live="polite"></div><p class="muted">Les décimales servent à la lecture. Les fractions et les intervalles du journal sont les données faisant autorité. Changer le niveau inspecte une borne déjà établie.</p></section>
<section class="panel"><h2>Raccorder un support</h2><div class="row"><label>Support S <input id="support" type="number" value="0.375" min="0" step="0.025"></label><label>Métrique <select id="metric"><option value="R">R = masse + énergie</option><option value="H1">H¹</option></select></label><label>Unité <select id="unit"><option value="A2">A_amp²</option><option value="A">A_amp</option></select></label></div><button id="connect">Vérifier le raccord</button><p id="connection" aria-live="polite"></p><p class="muted">La forme Q_W et les deux moments sont ceux du certificat. Une étiquette seule ne valide pas une autre brique.</p></section>
<section class="panel"><h2>Le pont suivant : un même test dans toutes les couches</h2><p>Chaque couche peut avoir sa propre direction de concentration maximale. Assembler les opérateurs avant leur norme oblige la même fonction à traverser toutes les couches. Le coût devient plus précis ; le même opérateur propose la tête et les sources de ses couplages.</p><div id="diagnostic" class="scroll"></div><p class="guard">Ce tableau est exploratoire : valeurs de Nyström, sans erreur opératoire certifiée. La petite marge à S=1/2 n’établit pas la positivité sur ce support.</p></section>
<section class="panel"><h2>Les quatre portes</h2><div class="scroll"><table><tr><th>Porte</th><th>Acquis</th><th>À construire</th></tr><tr><td>Arithmétique</td><td>Phase et compensation locale</td><td>Coût conjoint multi-premiers et loi de signe</td></tr><tr><td>Tête praticable</td><td>Concentration certifiée sans tête brute</td><td>Compression de l’opérateur commun avec erreur</td></tr><tr><td>Couplages</td><td>Gram commun ; sources du bloc croisé identifiées</td><td>Sources réelles et queue complète certifiées</td></tr><tr><td>Couverture</td><td>Tous les supports jusqu’à3/8</td><td>Transport non borné avec nouveaux premiers</td></tr></table></div><p>Prochaine construction : tête, queue et sources issues de l’opérateur commun. Le critère de choix est le nombre d’obligations réellement reliées ; aucun score de probabilité de RH n’est calculé.</p></section>
<footer><p><a href="../3_Preuves_et_calculs/data/v647_concentration_resultats.json">Journal du certificat</a> · <a href="../3_Preuves_et_calculs/data/v647_protocole_concentration.json">Protocole figé</a> · <a href="../3_Preuves_et_calculs/data/v647_operator_diagnostic.json">Diagnostic séparé</a> · <a href="71_LEGO_REUTILISABLE.html">Construction V6.46 conservée</a></p></footer>'''
    js=r'''const D=JSON.parse(document.getElementById('concentration-data').textContent),A=JSON.parse(document.getElementById('operator-data').textContent),el=id=>document.getElementById(id);const q=x=>{const a=String(x).split('/');return Number(a[0])/(a.length===2?Number(a[1]):1);};
function layer(){const u=Number(el('level').value),rows=D.certificate.rows,r=rows.reduce((a,b)=>Math.abs(q(a.u)-u)<Math.abs(q(b.u)-u)?a:b);el('layer').innerHTML='<p>Niveau '+q(r.u).toFixed(2)+' ; '+r.cell_count+' cellules ; longueur totale '+q(r.measure_upper).toFixed(2)+'.</p><table><tr><th>Majorant</th><th>Pair</th><th>Impair</th></tr>'+[['Trace',r.trace_upper],['Schatten2',r.hs_squared_upper.map(x=>Math.sqrt(q(x)))],['Concentration retenue',r.rho_upper]].map(([n,v])=>'<tr><td>'+n+'</td>'+v.map(x=>'<td>'+(typeof x==='number'?x:q(x)).toFixed(6)+'</td>').join('')+'</tr>').join('')+'</table>';}
function connect(){const s=Number(el('support').value);el('connection').textContent=!(s>0&&Number.isFinite(s))?'Raccord refusé : support positif requis.':el('metric').value!=='R'||el('unit').value!=='A2'?'Raccord refusé : métrique ou unité incompatible.':s<=3/8?'Raccord valide par inclusion : Q_W ≥ masse/12 et R/100.':'Support hors de la couverture certifiée ; positivité indéterminée ici.';}
function diagnostic(){const keys=[['Trace','trace'],['Schatten2 par couches','schatten2'],['Norme de Nyström par couches','operator'],['Opérateur commun : Nyström','common_operator']];el('diagnostic').innerHTML='<table><tr><th>Marge exploratoire</th><th>S=3/8</th><th>S=1/2</th></tr>'+keys.map(([n,k])=>'<tr><td>'+n+'</td>'+A.supports.map(s=>'<td>'+s.resolutions.at(-1).margins[k].toFixed(6)+'</td>').join('')+'</tr>').join('')+'</table>';}
el('level').addEventListener('input',layer);el('connect').addEventListener('click',connect);layer();connect();diagnostic();window.concentrationDashboard={layer,connect,diagnostic};'''
    payload=lambda x:json.dumps(x,ensure_ascii=False).replace('</',r'<\/')
    (P/'72_CONCENTRATION_PROJETEE.html').write_text('<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V6.47 · Lego des concentrations</title><style>'+css+'</style></head><body><main>'+bi.topnav('graphe','../')+body+'</main><script id="concentration-data" type="application/json">'+payload(r)+'</script><script id="operator-data" type="application/json">'+payload(diag)+'</script><script>'+js+'</script></body></html>')
def main():
    sys.path.insert(0,str(ROOT/'2_Methode/Outils'))
    inventory();figure();report()
    module('pedagogy647',ROOT/'2_Methode/Outils/build_v647_pedagogy.py').build();dashboard()
if __name__=='__main__':main()
