/* Decimal display only. Exact certificate fractions remain authoritative. */
function rationalDisplay(value){
 if(typeof value==='number')return value;
 const parts=String(value).trim().split('/');
 function integer(s){
  if(!/^[+-]?\d+$/.test(s))return null;
  const sign=s.startsWith('-')?-1:1,d=s.replace(/^[+-]/,'').replace(/^0+/,'')||'0';
  if(d==='0')return {m:0,e:0};
  const leading=d.slice(0,16);return {m:sign*Number(leading)/10**(leading.length-1),e:d.length-1};
 }
 const n=integer(parts[0]),d=integer(parts[1]??'1');
 if(parts.length>2||!n||!d||d.m===0)return NaN;
 return n.m/d.m*10**(n.e-d.e);
}
if(typeof module!=='undefined')module.exports={rationalDisplay};
