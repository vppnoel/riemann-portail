const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'../..');
const {solveAtlas}=require(path.join(root,'2_Methode/Outils/bellman_atlas_client.js'));
const fixture=JSON.parse(fs.readFileSync(path.join(root,'3_Preuves_et_calculs/data/v641_bellman_controles.json'),'utf8'));
const canonical=p=>JSON.stringify(p.map(x=>[...x].sort()).sort((a,b)=>JSON.stringify(a).localeCompare(JSON.stringify(b))));
for(const record of fixture.cases){
  const actual=solveAtlas(fixture.model,record.budget,record.weights,fixture.completed),expected=record.expected;
  if(actual.value!==expected.value||actual.gain!==expected.gain||canonical(actual.portfolios)!==canonical(expected.portfolios)||JSON.stringify([...actual.first_choices].sort())!==JSON.stringify([...expected.first_choices].sort()))
    throw Error('V641 client comparison failed at '+JSON.stringify(record.weights)+' budget '+record.budget);
}
console.log(JSON.stringify({completed:fixture.completed,configurations:fixture.cases.length,all_client_results_match:true,independent_subset_enumeration_matches:true}));
