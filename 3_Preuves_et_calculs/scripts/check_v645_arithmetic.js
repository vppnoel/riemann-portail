/* Check interactions with a simulated DOM; this is not browser-render QA. */
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const root=path.resolve(__dirname,'../..');
const html=fs.readFileSync(path.join(root,'1_Presentation/70_PONT_ARITHMETIQUE.html'),'utf8');
const data=JSON.parse(html.match(/<script id="arithmetic-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const defaults={support:'1/2',H:'3',C:'1',beta:'1',mu:'2',delta:'0'};
class Element{constructor(id){this.value=defaults[id]??'';this.innerHTML='';this.textContent='';this.events={};}addEventListener(t,fn){this.events[t]=fn;}fire(t){assert(this.events[t]);this.events[t]();}}
const elements={},document={getElementById(id){return elements[id]??(elements[id]=new Element(id));}};
document.getElementById('arithmetic-data').textContent=JSON.stringify(data);
const context={document,window:{}};vm.createContext(context);vm.runInContext(script,context);
const el=id=>document.getElementById(id);
for(const row of data.supports){el('support').value=row.S;el('support').fire('change');assert(el('numbers').innerHTML.includes(row.tail.q_digits+' chiffres'));assert(el('numbers').innerHTML.includes(row.compensating_direction.full_quotient_exploratory));}
assert(el('verdict').textContent.includes('2.5')&&el('verdict').textContent.includes('prémisses analytiques'));
el('mu').value='0';el('check').fire('click');assert(el('verdict').textContent.includes('refusé'));
el('mu').value='2';el('H').value='0';el('check').fire('click');assert(el('verdict').textContent.includes('ne tranche pas'));
el('C').value='-1';el('check').fire('click');assert(el('verdict').textContent.includes('refusé'));
console.log('V645 : 4 supports, dette conditionnelle, marge invalide et condition inconclusive vérifiés avec DOM simulé.');
