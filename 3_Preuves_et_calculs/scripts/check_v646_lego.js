const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert'),root=path.resolve(__dirname,'../..');
const html=fs.readFileSync(path.join(root,'1_Presentation/71_LEGO_REUTILISABLE.html'),'utf8'),D=JSON.parse(html.match(/<script id="lego-data" type="application\/json">([\s\S]*?)<\/script>/)[1]),script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const defaults={support:'347/1000',requested:'0.3',norm:'R',unit:'A2'};
class Element{constructor(id){this.value=defaults[id]??'';this.innerHTML='';this.textContent='';this.events={};}addEventListener(t,f){this.events[t]=f;}fire(t){this.events[t]();}}
const elements={},document={getElementById(id){return elements[id]??(elements[id]=new Element(id));}};document.getElementById('lego-data').textContent=JSON.stringify(D);const c={document,window:{}};vm.createContext(c);vm.runInContext(script,c);const el=id=>document.getElementById(id);
assert(el('connection').textContent.includes('valide'));
for(const row of D.supports){el('support').value=row.S;el('support').fire('change');assert(el('numbers').innerHTML.includes(row.certificate.status==='certified_local_all_tests'?'Certifié':'Indéterminé'));}
el('requested').value='0.5';el('connect').fire('click');assert(el('connection').textContent.includes('hors'));
el('requested').value='0.3';el('norm').value='H1';el('connect').fire('click');assert(el('connection').textContent.includes('refusé'));
el('norm').value='R';el('unit').value='A';el('connect').fire('click');assert(el('connection').textContent.includes('refusé'));
el('global').fire('click');assert(el('coverage').textContent.includes('non bornée refusée'));
console.log('V646 : 3 essais, inclusion, normes/unités incompatibles et couverture non bornée vérifiés avec DOM simulé.');
