"""V645 document, arithmetic dashboard and progressive dictionary supplement."""
from pathlib import Path
import sys,json,importlib.util,base64,html
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'1_Presentation';D=ROOT/'3_Preuves_et_calculs/data';STEM='70_PONT_ARITHMETIQUE_ET_DETTE_DE_COUPLAGE'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def endpoint(t):
    sign,man,exp,bc=t;return F((-1 if sign else 1)*man)*F(2)**exp
def decimal_out(q,upper=False,places=4):
    q=F(q);v=q*10**places;n=-(-v.numerator//v.denominator) if upper else v.numerator//v.denominator
    return ('-' if n<0 else '')+str(abs(n)//10**places)+'.'+str(abs(n)%10**places).zfill(places)
def interval_display(v,places=4):return '['+decimal_out(endpoint(v['binary'][0]),False,places)+', '+decimal_out(endpoint(v['binary'][1]),True,places)+']'
def supplement():
    dictionary=read(D/'v644_dictionnaire.json');dictionary['version']='V6.45'
    data=r'''
chebyshev§2§Fonction de Chebyshev Ψ§Ψ(x)=Σₚᵐ≤x log p§On compte les tours de briques premières avec leur poids.§Fonction en escalier sur x≥1 ; unité1 ; nom distinct de la graine ψ et de la digamma.§La borne d’erreur x^(1/2+ε) pour chaque ε est déjà équivalente à RH.
chebyshev_delta§4§Fluctuation couplée des premiers§ΔΨ(t)=Ψ(e^t)−e^t+1§On retire le dessin moyen et on garde les petites différences signées.§ΔΨ(0)=0 ; sa mesure agit sur la corrélation pondérée ; identité exacte de Q_W.§Sa petite taille relative ne permet pas d’oublier son action de signe.
polar_cancellation§4§Annulation polaire de rang deux§e^(|x−y|/2)=2cosh((x−y)/2)−e^(−|x−y|/2)§Deux balances effacent le gros dessin commun.§Les moments ℓ± annulent la partie cosh ; le modèle continu vaut −P₀.§La cancellation ne rend pas tout l’opérateur premier petit en norme L².
seed_energy§4§Énergie de graine P₀§P₀(Pψ)=||ψ′||²+¼||ψ||²§Le moule fait apparaître une pile positive.§Forme du noyau e^(−|x|/2), multiplicateur1/(τ²+¼) ; unité A_amp².§Ce terme positif n’élimine pas la masse soustraite ni la fluctuation.
continuous_base§4§Base continue B₀§B₀=E_arch−C₀||f||²+P₀§Après le gros dessin, la balance peut encore pencher.§Base signée ; dilatations lentes donnent quotient→4−C₀<0 ; témoin polynomial négatif démontré pour tout S≥16.§Sa négativité concerne le modèle continu, pas Q_W complet ni RH.
strong_source§4§Source forte k§q(h,y)=⟨k,y⟩₂§Un dessin devient le capteur de toutes ses attaches.§Pour hH¹, intégrale Bochner archimédienne et translations premières produisent kL² sur le support.§Il faut un encadrement de source en normeL², pas des valeurs sur une grille seulement.
source_residual§4§Résidu de source ρ§ρ=k−p, p annihile Y_N§On retire ce que les balances de la queue ne peuvent lire.§p appartient au span des polynômes0..N et e±x/2 sur I ; q(h,y)=⟨ρ,y⟩₂.§p doit être une vraie fonction du span ; sa projection numérique demande ses erreurs.
source_schur§5§Certificat de dette par résidus§G_eff≥H−(β/μ)Gram₂ρ§Les attaches restantes ont un ticket de poids exact.§Si queueQ≥μR et masse≤βR, PSD de la matrice inférieure certifie le support avec tête complète.§Sources, Gram et tête doivent être contrôlés ; pas de signe global acquis pour tous S.
geometric_norm§4§Chaînes de translations§||Π_I(U_a+U_−a)Π_I||=2cos(π/(ceil(D/a)+1))§Dans la boîte, les sauts dessinent des petites chaînes.§Norme exacte pour support de longueurD ; donne une somme géométrique meilleure.§La norme concerne la compression surI, pas les translations sur toute la droite.
row_budget§4§Budget de sommes de lignes§sup_x[A(x)+A(D−x)]§On compte toutes les attaches qui arrivent à un endroit.§Test de Schur pour translations à poids positifs ; comparaisons logn+logm≤D par produits entiers.§C’est une borne de norme, pas un signe de la forme quadratique.
resonance_obstruction§5§Résonances et moments§moduler puis corriger les moments§Un rythme rapide retrouve toutes les attaches premières.§Un nombre fini de moments ne baisse pas le supremumL² du noyau de translations ; preuveC3.§La métriqueR fait payer ces fréquences ; les moments seuls ne suffisent pas.
multiplier_tail_bound§4§Reste intégral du multiplicateur§A_K+½log(1+T²/b_K²)≤a(T)≤borne+b_Kterme§La pile infinie est entourée par une intégrale simple.§Termes positifs décroissants ; encadrement utilisable à très grande fréquence sans somme immense.§Le budget de queue ne calcule pas la tête ni le signe du Schur.
source_graph_guard§5§Garde de norme de graphe§convergenceR ≠ convergence des sourcesL²§Une règle douce ne lit pas tous les capteurs forts.§Le certificat par résidusL² est suffisant ; terminaison exige régularité ou approximation du domaine de source.§Aucune garantie de finir n’est déduite de la seule densité polynomiale enR.
'''
    for line in data.strip().splitlines():
        i,level,name,symbol,image,exact,guard=line.split('§');dictionary['entries'].append(dict(id='math:'+i,level=int(level),kind='math',name=name,symbol=symbol,image=image,exact=exact,guard=guard,status='identité, borne ou obstruction démontrée dans V645, C1–C5 ; conditions locales',source='Document 70 ; V645_PONT_ARITHMETIQUE.md'))
    assert len({x['id'] for x in dictionary['entries']})==len(dictionary['entries'])
    (D/'v645_dictionnaire.json').write_text(json.dumps(dictionary,ensure_ascii=False,indent=2)+'\n')
    legacy=module('dict645index',ROOT/'2_Methode/Outils/build_v644_dictionary.py');inventory=legacy.code_inventory();(D/'v645_index_fonctions.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
    import csv
    with (D/'v645_index_fonctions.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['path','line','name','kind','signature','docstring','explanation_status']);writer.writeheader();writer.writerows(inventory['entries'])
    print(len(dictionary['entries']),'fiches total ; index',len(inventory['entries']),'déclarations Python')
def figure(result):
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,2,figsize=(9,6));labels=['Base B₀\ndiagnostic','Fluctuation\nencadrée','Total Q\ndiagnostic']
    for ax,r in zip(axes.flat,result['supports']):
        c=r['compensating_direction'];v=[float(c['base_quotient_exploratory']),float(c['fluctuation_quotient_interval']['midpoint']),float(c['full_quotient_exploratory'])]
        bars=ax.bar(range(3),v,color=['#b95350','#44836c','#63839b']);ax.axhline(0,color='#23382f',lw=.8);ax.set_xticks(range(3),labels,fontsize=9);ax.set_title('S = '+r['S']+' · direction proposée, n = 8',fontsize=11)
        ax.set_ylabel('Quotient par la métrique H¹',fontsize=9)
        for p,value in zip(bars,v):ax.annotate(f'{value:.6g}',(p.get_x()+p.get_width()/2,value),xytext=(0,5 if value>=0 else -12),textcoords='offset points',ha='center',fontsize=9)
        ax.margins(y=.25);ax.grid(axis='y',alpha=.18)
    fig.suptitle('La fluctuation est une contribution de signe essentielle',fontsize=14);fig.tight_layout(rect=(0,.03,1,.95));fig.text(.5,.01,'Fluctuation : intervalle validé. Base et total : archimédien exploratoire V644.',ha='center',fontsize=9)
    fig.savefig(P/'70_COMPENSATION_ARITHMETIQUE.png',dpi=180);fig.savefig(P/'70_COMPENSATION_ARITHMETIQUE.svg');plt.close(fig)
def report(result):
    budgets='| S | L brut encadré | L retenu, majorant | chiffres de q : V644 → V645 |\n|---|---|---|---|\n'
    for r in result['supports']:budgets+=f"| {r['S']} | {interval_display(r['budgets']['raw'])} | {decimal_out(F(r['chosen_L_upper']),True)} | {r['tail']['old_q_digits']} → {r['tail']['q_digits']} |\n"
    base='| S | borne supérieure rationnelle de B₀ / masse, affichée vers le haut | signe négatif certifié |\n|---|---|---|\n'
    for r in result['wide_base_rational_certificates']:base+=f"| {r['S']} | {decimal_out(F(r['normalized_upper']),True,6)} | {'oui' if r['negative_certified'] else 'non tranché par cette borne'} |\n"
    comp='| S | B₀, diagnostic | fluctuation, intervalle | Q complet, diagnostic |\n|---|---|---|---|\n'
    for r in result['supports']:
        c=r['compensating_direction'];comp+=f"| {r['S']} | {float(c['base_quotient_exploratory']):.8g} | {interval_display(c['fluctuation_quotient_interval'],8)} | {float(c['full_quotient_exploratory']):.8g} |\n"
    text=(ROOT/'3_Preuves_et_calculs/preuves/V645_PONT_ARITHMETIQUE.md').read_text(encoding='utf-8-sig').replace('{{BUDGET_TABLE}}',budgets).replace('{{BASE_TABLE}}',base).replace('{{COMPENSATION_TABLE}}',comp+'\n\n![Compensation dans les directions proposées.](70_COMPENSATION_ARITHMETIQUE.png)')
    sources=module('refs645',ROOT/'2_Methode/Sources/build_sources.py')
    base=text.split(sources.REF0)[0].rstrip()+'\n'
    text=base+'\n'+sources.doc_refs(base,sources.load())+'\n'
    (P/(STEM+'.md')).write_text(text,encoding='utf-8-sig');module('compiler645',ROOT/'2_Methode/Outils/build_v644.py').pdf(STEM)
def dashboard(result):
    bi=module('bi645dash',ROOT/'2_Methode/Indicateur/build_indicateur.py');payload=json.dumps(result,ensure_ascii=False).replace('</',r'<\/')
    pic='data:image/png;base64,'+base64.b64encode((P/'70_COMPENSATION_ARITHMETIQUE.png').read_bytes()).decode()
    css='body{margin:0;background:#f3f5ef;color:#243b30;font:16px/1.55 system-ui}main{max-width:1100px;margin:auto;padding:22px}header{background:#163f34;color:white;padding:25px;border-radius:14px}header a{color:#d9f2e3}h1{line-height:1.2}a{color:#246959}.panel{background:white;border:1px solid #cddbcc;padding:20px;border-radius:12px;margin:18px 0}.topnav{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:15px}.row{display:flex;gap:15px;flex-wrap:wrap}select,input,button{font:inherit;padding:9px;border:1px solid #9bad9e;border-radius:7px;max-width:100%}label{display:block}button{cursor:pointer;background:#e1eee0}table{border-collapse:collapse;width:100%}th,td{padding:10px;text-align:left;border-bottom:1px solid #dce4d9}.guard{background:#fff2d9;border-left:5px solid #b97a2d;padding:14px}.positive{color:#236649}.formula{font-size:21px;background:#edf4e9;padding:14px;overflow-wrap:anywhere}img{width:100%;height:auto}.muted{font-size:14px;color:#58665c}@media(max-width:680px){main{padding:10px}table{font-size:13px}th,td{padding:5px}}'
    body=f'''<header><h1>Le pont arithmétique</h1><p>V6.45 · retirer le pôle, garder la fluctuation et payer les couplages.</p><p><a href="{STEM}.pdf">Preuves et résultats · PDF</a> · <a href="{STEM}.tex">LaTeX</a> · <a href="69_LANGUE_DES_PASSAGES.html">Dictionnaire et grammaire</a></p></header>
<section class="panel"><h2>La nouvelle phrase</h2><div class="formula">Q_W = énergie archimédienne − C₀·masse + énergie de graine + fluctuation couplée de Chebyshev</div><p>Les deux moments annulent une partie polaire de rang deux. Le modèle continu ne fournit pas le signe à lui seul : la fluctuation peut être une compensation essentielle.</p></section>
<section class="panel"><h2>Inspecter les budgets exécutés</h2><label for="support">Support S</label><select id="support">{''.join('<option value="'+r['S']+'">'+r['S']+'</option>' for r in result['supports'])}</select><div id="numbers" aria-live="polite"></div><p class="guard">Premiers, fluctuation et budget de queue sont encadrés. La base et le total affichés utilisent encore la quadrature archimédienne exploratoire V644. Le Schur effectif de tête n’a pas été calculé.</p><img src="{pic}" alt="Quatre comparaisons de base, fluctuation et total"></section>
<section class="panel"><h2>Jouer avec le contrat scalaire de dette</h2><p>Exemple algébrique : H est une valeur de tête, C le Gram de son résidu, β le contrôle de masse de la queue, μ sa marge. Ces champs illustrent une condition suffisante ; ils ne sont pas les données certifiées d’un support de ζ.</p><div class="row"><label>H <input id="H" type="number" value="3" step="0.1"></label><label>C ≥ 0 <input id="C" type="number" value="1" min="0" step="0.1"></label><label>β ≥ 0 <input id="beta" type="number" value="1" min="0" step="0.1"></label><label>μ > 0 <input id="mu" type="number" value="2" min="0" step="0.1"></label><label>erreur δH ≥ 0 <input id="delta" type="number" value="0" min="0" step="0.1"></label></div><button id="check">Vérifier la condition</button><p id="verdict" aria-live="polite"></p><p class="guard">Pour appliquer la condition à tout X_S, il faut une tête complète, un contrat de queue, de vraies sources et des normes d’erreur encadrées. Une loi pour tous S reste ouverte.</p></section>
<section class="panel"><h2>Les portes restantes</h2><table><tr><th>Porte</th><th>Acquis</th><th>À construire</th></tr><tr><td>Arithmétique</td><td>Annulation polaire et fluctuation exacte</td><td>Loi de signe des corrélations et de leur dette</td></tr><tr><td>Queue</td><td>Bornes géométriques et série/intégrale</td><td>Tête de taille calculable</td></tr><tr><td>Couplages</td><td>Schur ≥ H−β·Gramρ/μ</td><td>Sources et résidus L² certifiés</td></tr><tr><td>Couverture</td><td>Contrat à support fixé</td><td>Tous les supports ; garde de convergence en norme de graphe</td></tr></table></section>
<footer><p><a href="../3_Preuves_et_calculs/data/v645_arithmetique_resultats.json">Journal complet avec bornes binaires</a> · <a href="../3_Preuves_et_calculs/data/v645_protocole_arithmetique.json">Protocole préalable</a></p><p>Le témoin polynomial du modèle continu B₀ est négatif pour tout S≥16. Aucun témoin négatif de Q_W ni preuve de RH n’est annoncé.</p></footer>'''
    js=r'''const data=JSON.parse(document.getElementById('arithmetic-data').textContent);const el=id=>document.getElementById(id);function render(){const r=data.supports.find(x=>x.S===el('support').value),c=r.compensating_direction;el('numbers').innerHTML='<table><tr><th>Quantité</th><th>Valeur</th></tr><tr><td>Budget brut L, centre d’encadrement</td><td>'+r.budgets.raw.midpoint+'</td></tr><tr><td>Budget de lignes, centre d’encadrement</td><td>'+r.budgets.row.midpoint+'</td></tr><tr><td>Queue dyadique</td><td>T='+r.tail.T_expression+' ; q possède '+r.tail.q_digits+' chiffres (avant : '+r.tail.old_q_digits+')</td></tr><tr><td>Base B₀, diagnostic</td><td>'+c.base_quotient_exploratory+'</td></tr><tr><td>Fluctuation, centre d’intervalle</td><td>'+c.fluctuation_quotient_interval.midpoint+' ; signe '+c.fluctuation_sign_certified+'</td></tr><tr><td>Total Q, diagnostic</td><td>'+c.full_quotient_exploratory+'</td></tr></table>';}
function test(){const H=Number(el('H').value),C=Number(el('C').value),b=Number(el('beta').value),m=Number(el('mu').value),d=Number(el('delta').value);if(![H,C,b,m,d].every(Number.isFinite)||C<0||b<0||m<=0||d<0){el('verdict').textContent='Contrat refusé : Gram, erreurs et β non négatifs ; μ strictement positif.';return;}const low=H-d-b*C/m;el('verdict').textContent='Borne inférieure algébrique : '+low+'. '+(low>=0?'Condition scalaire suffisante satisfaite, sous les prémisses analytiques affichées.':'La condition suffisante ne tranche pas le signe du Schur exact.');}
el('support').addEventListener('change',render);el('check').addEventListener('click',test);render();test();window.arithmeticDashboard={render,test};'''
    (P/'70_PONT_ARITHMETIQUE.html').write_text('<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V6.45 · Pont arithmétique</title><style>'+css+'</style></head><body><main>'+bi.topnav('graphe','../')+body+'</main><script id="arithmetic-data" type="application/json">'+payload+'</script><script>'+js+'</script></body></html>')
def main():
    result=read(D/'v645_arithmetique_resultats.json');supplement();figure(result);report(result);dashboard(result)
    print('Document 70, PDF/LaTeX et dashboard arithmétique créés')
if __name__=='__main__':main()
