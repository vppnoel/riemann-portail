const fs=require('fs');
const {chromium}=require('playwright');
const {pathToFileURL}=require('url');
const path=require('path'),os=require('os');
const root=path.resolve(__dirname,'../..');
const base=fs.mkdtempSync(path.join(os.tmpdir(),'riemann-qa-'));fs.mkdirSync(base+'/audit');
const S=JSON.parse(fs.readFileSync(root+'/3_Preuves_et_calculs/data/pilotage_courant.json'));
const {solveBridge,applyBridgeWeightProfile}=require(root+'/2_Methode/Pilotage/bellman_contracts.js');
const assert=(x,m)=>{if(!x)throw Error(m)};
(async()=>{
 for(const d of S.decisions){
  const j=solveBridge(applyBridgeWeightProfile(S.bellman,d.weights),d.budget,d.mode,S.bellman_state.facts,S.bellman_state.completed);
  assert(j.value===d.value&&JSON.stringify(j.first_choices)===JSON.stringify(d.first_choices),'Python/JS Bellman disagreement');
 }
 const browser=await chromium.launch({executablePath:process.env.RIEMANN_CHROMIUM||undefined,headless:true,
    args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--no-zygote']});
 const page=await browser.newPage({viewport:{width:1365,height:1000}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const results=[];
 for(const p of S.primary_pages){
  await page.goto(pathToFileURL(root+'/'+p.path).href);await page.waitForFunction(()=>window.steeringReady===true);
  assert(await page.locator('.topnav a[data-primary]').count()===4,'Four primary pages required');
  assert(await page.locator('.topnav a[data-tool-link=bellman]').count()===1,'Direct Bellman missing');
  await page.locator('.nav-documents summary').click();
  assert(await page.locator('.topnav a[data-resource]:visible').count()===7,'Documents menu missing');
  await page.locator('.nav-documents summary').click();
  assert(await page.locator('.topnav a[aria-current=page]').count()===1,'Current page missing');
  assert(await page.locator('meta[name=research-snapshot]').getAttribute('content')===S.fingerprint,'Snapshot mismatch');
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Desktop overflow: '+p.id);
  await page.screenshot({path:base+'/audit/'+p.id+'_desktop.png',fullPage:false});
  if(p.id==='portail'){
   await page.waitForFunction(()=>window.catalogueReady===true);
   const C=JSON.parse(fs.readFileSync(root+'/3_Preuves_et_calculs/data/catalogue_fichiers_v655.json'));
   for(const type of ['html','pdf','tex','md','programmes','donnees','figures','fiches','references']){
    const example=C.entries.find(e=>e.kind===type&&!e.archived);
    await page.locator('[data-catalogue-kind]').selectOption(type);
    await page.locator('[data-catalogue-query]').fill(example.path||example.id);
    assert(await page.locator('[data-catalogue-entry]').count()>0,'Unfindable file type '+type);
    assert(await page.locator('[data-catalogue-entry]').evaluateAll((xs,id)=>xs.some(x=>x.dataset.catalogueEntry===id),example.id),'Missing exact catalogue item '+example.id);
   }
   await page.locator('[data-catalogue-kind]').selectOption('fiches');
   await page.locator('[data-catalogue-query]').fill('');
   const found=new Set();
   while(true){for(const id of await page.locator('[data-catalogue-entry]').evaluateAll(xs=>xs.map(x=>x.dataset.catalogueEntry)))found.add(id);if(await page.locator('[data-catalogue-next]').isDisabled())break;await page.locator('[data-catalogue-next]').click()}
   assert(found.size===69,'Catalogue pagination loses ideas');
   await page.locator('[data-catalogue-kind]').selectOption('');
   const old=C.entries.find(e=>e.archived);
   await page.locator('[data-catalogue-query]').fill(old.path);
   assert(await page.locator('[data-catalogue-entry]').count()===0,'Archive mixed with current');
   await page.locator('[data-catalogue-scope]').selectOption('all');
   assert(await page.locator('[data-catalogue-entry]').count()===1,'Archive cannot be retrieved');
   await page.locator('[data-catalogue-query]').fill('IDE-047');
   await page.locator('[data-catalogue-scope]').selectOption('current');
   assert(await page.locator('[data-catalogue-entry]').count()>1,'Idea does not retrieve its resources');
   await page.locator('#documents').screenshot({path:base+'/audit/catalogue_desktop.png'});
   await page.locator('[data-catalogue-query]').fill('');
  }
  if(p.id==='navigateur'){
   assert(await page.locator('#cv-navigation-chart .cv-rail-svg').count()===7,'Seven navigator rails required');
   await page.locator('#position').screenshot({path:base+'/audit/navigateur_graphiques.png'});
   const first=JSON.parse(await page.locator('#bellman-result').getAttribute('data-first'));
   const expected=S.decisions.find(d=>d.mode==='lower'&&d.budget===6).first_choices;
   assert(JSON.stringify(first)===JSON.stringify(expected),'Initial decision mismatch');
   await page.locator('#budget').fill('0');
   assert((await page.locator('#bellman-result').textContent()).includes('STOP'),'STOP missing');
   await page.locator('#budget').fill('6');
   for(const k of ['structural','local','clarity'])await page.locator('#w-'+k).fill('0');
   assert((await page.locator('#bellman-result').textContent()).includes('STOP'),'Zero-weight STOP missing');
   for(const k of ['structural','local','clarity'])await page.locator('#w-'+k).fill('1');
   await page.locator('#bellman').screenshot({path:base+'/audit/bellman_actif.png'});
  }
  if(p.id==='indicateur'){
   assert(await page.locator('.cv-timeline').count()===7,'Seven original step curves required');
   assert(await page.locator('.cv-rail-svg').count()===7,'Seven comparison rails required');
   const last=S.indicator.etapes.at(-1).id,first=S.indicator.etapes[0].id;
   assert(await page.locator('[data-cv-after]').inputValue()===last,'Current comparison stale');
   await page.locator('[data-cv-before]').selectOption(last);
   for(const row of await page.locator('.cv-rail-value').allTextContents()){
    const sides=row.split(' → ');assert(sides[0]===sides[1],'Comparison not interactive');
   }
   await page.locator('[data-cv-step]').selectOption(first);
   assert((await page.locator('[data-cv-step-title]').textContent())===S.indicator.etapes[0].versions,'Stage selector failed');
   await page.locator('[data-cv-step]').selectOption(last);
   await page.locator('[data-cv-before]').selectOption(S.indicator.comparaison.avant);
   await page.locator('#graphiques-indicateurs').screenshot({path:base+'/audit/indicateurs_graphiques.png'});
  }
  if(p.id==='carte'){
   assert(await page.locator('[data-idea-card]').count()===S.nodes.length,'Graph nodes missing');
   assert(await page.locator('.retained-graph button.node').count()===42,'Claude graph layout missing');
   await page.locator('#graph-search').fill('Kalman');
   assert(await page.locator('[data-idea-card]:visible').count()===1,'Graph search failed');
   await page.locator('[data-idea-card]:visible').click();
   assert(await page.locator('#node-dialog').isVisible(),'Node details did not open');
   assert((await page.locator('#node-body').textContent()).includes('Levinson'),'Updated Kalman evaluation missing');
   await page.locator('#close-dialog').click();await page.waitForFunction(()=>!document.querySelector('dialog').open);await page.locator('#graph-search').fill('');await page.waitForFunction(()=>document.querySelectorAll('[data-idea-card]:not([hidden])').length===69);
   for(const key of ['sources_locales','sources_registre']){
    await page.locator('[data-idea-card][data-node='+key+']').click();
    const text=await page.locator('#node-body').textContent();
    assert(text.includes(key==='sources_locales'?'mode fantôme':'fiche par fiche'),'Source nodes still conflated');
    await page.locator('#close-dialog').click();
   }
   for(const key of ['weil','energie','ponts']){
    await page.locator('[data-map-tab='+key+']').click();
    const current=page.locator('[data-map-panel='+key+']');
    assert(await current.locator('svg').isVisible(),'2D map hidden '+key);
    const overflow=await current.locator('.map-node-title').evaluateAll(ts=>ts.map(t=>({text:t.textContent,width:t.getBBox().width})).filter(x=>x.width>212));
    assert(overflow.length===0,'Map titles exceed their boxes '+JSON.stringify(overflow));
    for(const href of await current.locator('a').evaluateAll(as=>as.map(a=>a.href.baseVal?new URL(a.href.baseVal,document.URL).href:a.href))){
     if(href.startsWith('file:'))assert(fs.existsSync(new URL(href)),'Broken map link '+href);
    }
    await page.locator('[data-map-scale]').fill('75');
    assert(await page.locator('[data-map-percent]').textContent()==='75 %','Zoom failed');
    await page.locator('[data-map-read]').click();
    assert(await current.locator('svg').evaluate(el=>el.getBoundingClientRect().width)===1030,'Readable map size lost');
    await page.locator('#vers-rh').screenshot({path:base+'/audit/carte_'+key+'_desktop.png'});
   }
   const guards=await page.locator('[data-and-guard]').evaluateAll(xs=>xs.map(x=>x.dataset.andGuard));
   assert(guards.includes('global_sign coverage')&&guards.includes('copies head large_q'),'AND guards absent');
   await page.locator('[data-map-tab=weil]').click();
   await page.locator('[data-map-panel=weil] a[data-node=global_sign]').click();
   assert(await page.locator('#node-dialog').isVisible(),'2D node not linked');
   assert(await page.locator('#node-body .node-publications a').count()>0,'Direct node publications missing');
   await page.locator('#close-dialog').click();
   await page.locator('#vers-rh').screenshot({path:base+'/audit/graphe_vers_RH.png'});
  }
  const detailLinks=await page.evaluate(nodes=>{
   const links=[];
   for(const n of nodes){
    const button=document.createElement('button');button.dataset.node=n.id;document.body.appendChild(button);button.click();button.remove();
    links.push(...[...document.querySelectorAll('#node-body a[href]')].map(a=>a.href));
   }
   return links;
  },S.nodes);
  for(const u of detailLinks){if(u.startsWith('file:'))assert(fs.existsSync(new URL(u)),'Broken detail link '+u)}
  if(await page.locator('#node-dialog').isVisible())await page.locator('#close-dialog').click();
  await page.setViewportSize({width:390,height:844});
  await page.evaluate(()=>scrollTo(0,0));
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Mobile overflow: '+p.id);
  await page.locator('.nav-documents summary').click();
  assert(await page.locator('.topnav a[data-resource]:visible').count()===7,'Mobile Documents hidden');
  assert(await page.locator('.nav-documents ul').evaluate(el=>{const r=el.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth}),'Mobile menu outside screen');
  await page.screenshot({path:base+'/audit/'+p.id+'_mobile_menu.png',fullPage:false});
  await page.locator('.nav-documents summary').click();
  if(p.id==='portail'){
   await page.locator('[data-catalogue-kind]').selectOption('programmes');
   await page.locator('[data-catalogue-query]').fill('v642');
   assert(await page.locator('[data-catalogue-entry]').count()>0,'Mobile file search failed');
   await page.locator('#documents').scrollIntoViewIfNeeded();
   await page.screenshot({path:base+'/audit/catalogue_mobile.png',fullPage:false});
  }
  if(p.id==='carte'){
   for(const key of ['weil','energie','ponts']){
    await page.locator('[data-map-tab='+key+']').click();
    const view=page.locator('[data-map-panel='+key+'] .advanced-viewport');
    assert(await view.locator('svg').isVisible(),'Mobile 2D map hidden');
    assert(await view.evaluate(v=>v.scrollWidth>v.clientWidth),'Mobile map cannot pan');
    await page.locator('[data-map-fit]').click();
    assert(Number(await page.locator('[data-map-scale]').inputValue())<100,'Mobile fit failed');
    await page.locator('[data-map-read]').click();
    assert(await view.locator('svg').evaluate(e=>e.getBoundingClientRect().width)===1030,'Mobile readable scale lost');
    await view.evaluate(v=>{v.scrollLeft=0;v.scrollTop=0});
    await page.locator('#vers-rh').scrollIntoViewIfNeeded();
    await page.screenshot({path:base+'/audit/carte_'+key+'_mobile.png',fullPage:false});
    await page.locator('[data-map-goal]').click();await page.waitForTimeout(400);
    assert(await view.evaluate(v=>v.scrollTop>0),'Mobile target navigation failed');
   }
  }
  if(p.id==='indicateur'){
   assert(await page.locator('.cv-timeline:visible').count()===7,'Mobile chronology hidden');
   await page.locator('#graphiques-indicateurs').scrollIntoViewIfNeeded();
   await page.screenshot({path:base+'/audit/indicateurs_graphiques_mobile.png',fullPage:false});
  }
  if(p.id==='navigateur'){
   assert(await page.locator('#cv-navigation-chart .cv-rail-svg:visible').count()===7,'Mobile navigator rails hidden');
   await page.locator('#position').scrollIntoViewIfNeeded();
   await page.screenshot({path:base+'/audit/navigateur_graphiques_mobile.png',fullPage:false});
  }
  await page.evaluate(()=>scrollTo(0,0));
  await page.screenshot({path:base+'/audit/'+p.id+'_mobile.png',fullPage:false});
  await page.setViewportSize({width:1365,height:1000});results.push({page:p.id,desktop:true,mobile:true});
 }
 let legacyCases=0;
 for(const c of S.graph_cases.filter(c=>c.view.endsWith('.html'))){
  await page.goto(pathToFileURL(root+'/'+c.view).href+'#case='+encodeURIComponent(c.id));
  const ref=page.locator('aside[data-worked-reference="'+c.id+'"]');
  assert(await ref.count()===1,'Graph detail routing failed '+c.id);
  assert((await ref.locator('a').first().getAttribute('href')).includes('#node='+c.ideas[0]),'Wrong main idea '+c.id);
  if(c.id.startsWith('G66.')&&c.original_source)assert((await page.getByText('Ouvrir la preuve ou les données',{exact:true}).getAttribute('href')).endsWith(c.original_source),'Recovered proof link not restored '+c.id);
  legacyCases++;
 }
 await page.goto(pathToFileURL(root+'/1_Presentation/42_REGISTRE_DES_SOURCES.html').href);
 await page.locator('#reference-search').fill('Weil');
 assert(await page.locator('tr[id^=ref-]:visible').count()>0,'Reference search fails');
 await page.locator('.nav-documents summary').click();await page.locator('[data-resource=dossiers]').click();
 await page.waitForFunction(()=>window.catalogueReady===true);
 assert(await page.locator('#resource-catalogue').isVisible(),'Shared menu fails from reference registry');
 assert(errors.length===0,'Browser errors: '+errors.join(';'));
 await browser.close();
 const report={chromium:true,views:results,python_js_bellman_cases:S.decisions.length,interactions:true,original_details_checked:4*S.nodes.length,legacy_case_routes:legacyCases,compact_documents_menu:true,direct_bellman:true,all_file_types_searchable:true,catalogue_pagination_ideas:69,archive_filter:true,advanced_2d_maps:3,advanced_maps_mobile_visible:true,original_indicator_charts:7,original_navigator_rails:7,pdf_links_from_ideas:true,console_errors:errors};
 fs.writeFileSync(base+'/audit/browser_validation.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
})().catch(e=>{console.error(e.stack);process.exit(1)});
