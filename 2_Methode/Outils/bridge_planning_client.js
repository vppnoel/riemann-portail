/* Finite contract scenario planner. Same semantics as Python, independent code. */
function solveBridge(model,budget,mode='lower') {
  if (!Number.isInteger(budget)||budget<0||!['lower','upper'].includes(mode)) throw Error('budget/mode');
  const has=(f,ps)=>ps.some(p=>p.every(k=>f.has(k)));
  const utility=f=>model.capabilities.reduce((v,c)=>v+(has(f,c.requires_any)?c.weight:0),0);
  const memo=new Map();const idx=mode==='lower'?1:0;
  function visit(f,done,b){
    const key=[Array.from(f).sort().join(','),Array.from(done).sort().join(','),b].join('|');
    if(memo.has(key)) return memo.get(key);
    const vals={STOP:utility(f)};
    for(const a of model.actions){
      const cost=a.duration[idx];
      if(done.has(a.id)||cost>b||!has(f,a.requires_any)||(a.forbids||[]).some(k=>f.has(k))) continue;
      const values=a.outcomes.map(o=>visit(new Set([...f,...o.adds]),new Set([...done,a.id]),b-cost).value);
      vals[a.id]=(mode==='lower'?Math.min:Math.max)(...values);
    }
    const value=Math.max(...Object.values(vals));
    const result={value,first_choices:Object.keys(vals).filter(k=>vals[k]===value).sort()};
    memo.set(key,result);return result;
  }
  return visit(new Set(model.initial_facts),new Set(),budget);
}
if(typeof module!=='undefined')module.exports={solveBridge};
