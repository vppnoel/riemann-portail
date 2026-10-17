/* Contract-scenario Bellman retained in document 67, sections 1 and 7.
 * Same recursion as solveBridge in 67_GRAPHE_DES_PONTS.html, with explicit
 * current-state and outcome-value reporting. No union-of-tokens pilot.
 */
function validateBridgeModel(model) {
  if(model.schema!=='bridge_contract_scenarios_v1'||Object.hasOwn(model,'tokens'))
    throw Error('Use document 67 contract scenarios, not union of tokens');
  const known=new Set(Object.keys(model.facts)),reserved=new Set(model.reserved_global_claims||[]);
  const factList=(list,label)=>{if(!Array.isArray(list)||list.some(k=>!known.has(k)))throw Error(label+': unknown fact')};
  const alternatives=(ps,label)=>{
    if(!Array.isArray(ps)||!ps.length)throw Error(label+': AND/OR contracts required');
    ps.forEach(p=>factList(p,label));
  };
  const state=f=>{
    factList([...f],'state');
    if([...f].some(k=>reserved.has(k)))throw Error('Reserved global claim in simulated state');
    for(const group of model.exclusive_groups||[])
      if(group.filter(k=>f.has(k)).length>1)throw Error('Mutually exclusive outcomes');
  };
  factList([...reserved],'reserved claim');
  (model.exclusive_groups||[]).forEach(g=>factList(g,'exclusive group'));
  state(new Set(model.initial_facts));
  const ids=model.actions.map(a=>a.id);
  if(new Set(ids).size!==ids.length||ids.includes('STOP'))throw Error('Duplicate/reserved action ID');
  for(const a of model.actions){
    if(!Array.isArray(a.duration)||a.duration.length!==2||
       a.duration.some(x=>!Number.isInteger(x)||x<=0)||a.duration[0]>a.duration[1])throw Error('Positive duration bounds required');
    alternatives(a.requires_any,a.id);factList(a.forbids||[],a.id);
    if(!Array.isArray(a.outcomes)||!a.outcomes.length||new Set(a.outcomes.map(o=>o.id)).size!==a.outcomes.length)
      throw Error('Distinct nonempty outcomes required');
    a.outcomes.forEach(o=>{factList(o.adds,a.id);state(new Set(o.adds))});
  }
  if(new Set(model.capabilities.map(c=>c.id)).size!==model.capabilities.length)throw Error('Duplicate capability ID');
  model.capabilities.forEach(c=>{
    if(typeof c.weight!=='number'||!Number.isFinite(c.weight)||c.weight<0)throw Error('Nonnegative capability weight required');
    alternatives(c.requires_any,c.id);
  });
  return {state};
}

function applyBridgeWeightProfile(model,factors={structural:1,local:1,clarity:1}) {
  const keys=['structural','local','clarity'];
  if(Object.keys(factors).length!==3||keys.some(k=>typeof factors[k]!=='number'||!Number.isFinite(factors[k])||factors[k]<0))
    throw Error('Expected nonnegative structural/local/clarity factors');
  const copy=JSON.parse(JSON.stringify(model));
  const structural=new Set(['contrat_structurel','noyau_resolu','pont_conditionnel','transfert_controle']);
  copy.capabilities.forEach(c=>{c.weight*=factors[structural.has(c.id)?'structural':c.id==='local'?'local':'clarity']});
  validateBridgeModel(copy);return copy;
}

function solveBridge(model,budget,mode='lower',facts=null,completed=[]) {
  const checks=validateBridgeModel(model);
  if(!Number.isInteger(budget)||budget<0||!['lower','upper'].includes(mode))throw Error('budget/mode');
  const initial=new Set(facts===null?model.initial_facts:facts),done=new Set(completed);
  checks.state(initial);
  const ids=new Set(model.actions.map(a=>a.id));
  if([...done].some(k=>!ids.has(k)))throw Error('Unknown completed study');
  const has=(f,ps)=>ps.some(p=>p.every(k=>f.has(k)));
  const utility=f=>model.capabilities.reduce((v,c)=>v+(has(f,c.requires_any)?c.weight:0),0);
  const memo=new Map(),idx=mode==='lower'?1:0;
  function visit(f,executed,b){
    const key=JSON.stringify([[...f].sort(),[...executed].sort(),b]);
    if(memo.has(key))return memo.get(key);
    const choice_values={STOP:utility(f)},outcome_values={};
    for(const a of model.actions){
      const cost=a.duration[idx];
      if(executed.has(a.id)||cost>b||!has(f,a.requires_any)||(a.forbids||[]).some(k=>f.has(k)))continue;
      const values={};
      for(const o of a.outcomes){
        const next=new Set([...f,...o.adds]);checks.state(next);
        values[o.id]=visit(next,new Set([...executed,a.id]),b-cost).value;
      }
      outcome_values[a.id]=values;
      choice_values[a.id]=(mode==='lower'?Math.min:Math.max)(...Object.values(values));
    }
    const value=Math.max(...Object.values(choice_values));
    const result={value,first_choices:Object.keys(choice_values).filter(k=>choice_values[k]===value).sort(),choice_values,outcome_values};
    memo.set(key,result);return result;
  }
  const r=visit(initial,done,budget);
  return {...r,gain:r.value-utility(initial),states:memo.size,mode,
    scope:'Declared finite scenarios only; no RH probability',budget,facts:[...initial].sort(),completed:[...done].sort()};
}

function solveBridgeEnvelopes(model,budget,facts=null,completed=[]) {
  return {lower:solveBridge(model,budget,'lower',facts,completed),upper:solveBridge(model,budget,'upper',facts,completed)};
}
if(typeof module!=='undefined')module.exports={solveBridge,solveBridgeEnvelopes,applyBridgeWeightProfile,validateBridgeModel};
