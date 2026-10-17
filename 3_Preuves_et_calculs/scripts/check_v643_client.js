const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'../..');
const {solveBridge}=require(path.join(root,'2_Methode/Outils/bridge_planning_client.js'));
const data=JSON.parse(fs.readFileSync(path.join(root,'3_Preuves_et_calculs/data/v643_clients_controls.json'),'utf8'));
let passed=0;
for(const test of data.cases){
  const m=JSON.parse(JSON.stringify(data.model));
  for(const c of m.capabilities){const i=['contrat_structurel','noyau_resolu','pont_conditionnel','transfert_controle'].includes(c.id)?0:c.id==='local'?1:2;c.weight*=test.profile[i];}
  const r=solveBridge(m,test.budget,test.mode);
  if(JSON.stringify(r)!==JSON.stringify(test.expected))throw Error(JSON.stringify({test,r}));passed++;
}
console.log(passed+' scénarios JavaScript concordent avec Bellman Python et le graphe indépendant.');
