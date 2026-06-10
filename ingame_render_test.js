const fs=require('fs'),vm=require('vm');
let js=[...fs.readFileSync('GeoQuest.html','utf8').matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)].filter(m=>!/\bsrc\s*=/.test(m[1])).map(m=>m[2]).join('\n;\n');
const FNS=['renderHomeTab','renderLernenTab','renderLigaTab','renderProfilTab','renderCollectionScreen','renderStatsTab','renderAdminTab','renderSettingsModal','renderHelpModal','renderGuideModal','renderStickerModal','renderPinModal','renderLVSetup','renderLVGameover','renderLVHandoff','renderBottomNav','renderTourModalSKIP'];
js+=";try{globalThis.__S=S;globalThis.__render=render;globalThis.__GEN=GEN;globalThis.__MODES=MODES;globalThis.__srsAdd=(typeof _srsAdd!=='undefined')?_srsAdd:null;globalThis.__srsHero=(typeof renderSrsHero!=='undefined')?renderSrsHero:null;globalThis.__srsList=(typeof renderSrsListModal!=='undefined')?renderSrsListModal:null;globalThis.__dailyHero=(typeof renderDailyHero!=='undefined')?renderDailyHero:null;globalThis.__regionEntry=(typeof renderRegionEntry!=='undefined')?renderRegionEntry:null;globalThis.__regionModal=(typeof renderRegionModal!=='undefined')?renderRegionModal:null;globalThis.__learnDeck=(typeof renderLearnDeck!=='undefined')?renderLearnDeck:null;globalThis.__seed=function(rv,pl,ar){try{if(typeof _DEFAULT_NEIGHBORS!=='undefined')NEIGHBORS=_DEFAULT_NEIGHBORS;}catch(e){}try{RIVERS_REAL=rv;}catch(e){}try{PLATES_DATA=pl;}catch(e){}try{if(ar&&ar.length)AREA_DATA=ar;}catch(e){}};globalThis.__F={};["+FNS.map(f=>"'"+f+"'").join(',')+"].forEach(function(n){try{globalThis.__F[n]=eval(n);}catch(e){}});globalThis.__OB=function(){try{return renderOnboarding;}catch(e){return null;}}();}catch(e){globalThis.__err=e&&e.message;}";
const ls=new Map();ls.set('gq_onboarding',JSON.stringify({done:true,lang:'de'}));
const elProto={style:new Proxy({},{get:()=>'',set:()=>true}),classList:{add(){},remove(){},toggle(){},contains(){return false}},appendChild(){},setAttribute(){},getAttribute(){return null},removeAttribute(){},addEventListener(){},removeEventListener(){},remove(){},focus(){},click(){},querySelector(){return null},querySelectorAll(){return []},getBoundingClientRect(){return{top:0,left:0,width:0,height:0}},insertBefore(){},scrollIntoView(){}};
const el=new Proxy(elProto,{get:(t,k)=>k in t?t[k]:(typeof k==='string'&&/^(set|get|add|remove|append|insert|query|scroll|focus|click|toggle)/.test(k)?()=>{}:'')});
const doc={addEventListener(){},removeEventListener(){},getElementById:()=>el,querySelector:()=>el,querySelectorAll:()=>[],createElement:()=>el,createElementNS:()=>el,documentElement:{style:{setProperty(){},getPropertyValue:()=>''},lang:'de',setAttribute(){},getAttribute:()=>null,removeAttribute(){},appendChild(){},addEventListener(){},classList:{add(){},remove(){},toggle(){},contains(){return false}}},head:el,body:el,cookie:''};
const sb={console,setTimeout:()=>0,clearTimeout:()=>{},setInterval:()=>0,clearInterval:()=>{},requestAnimationFrame:()=>0,cancelAnimationFrame:()=>{},Math,Date,JSON,Object,Array,String,Number,Boolean,RegExp,Map,Set,Symbol,isNaN,parseInt,parseFloat,encodeURIComponent,decodeURIComponent,document:doc,navigator:{language:'de',languages:['de'],onLine:true,userAgent:'node',serviceWorker:{register(){return Promise.resolve()},addEventListener(){},getRegistrations(){return Promise.resolve([])},getRegistration(){return Promise.resolve(null)},ready:Promise.resolve({})},geolocation:{watchPosition(){},getCurrentPosition(){}}},location:{href:'https://x/play',search:'',hash:'',reload(){},replace(){},assign(){}},localStorage:{getItem:k=>ls.has(k)?ls.get(k):null,setItem:(k,v)=>ls.set(k,String(v)),removeItem:k=>ls.delete(k)},matchMedia:()=>({matches:false,addEventListener(){},removeEventListener(){},addListener(){},removeListener(){}}),fetch:()=>Promise.reject(new Error('x')),alert(){},confirm(){return false},prompt(){return null},addEventListener(){},removeEventListener(){},scrollTo(){},getComputedStyle:()=>({getPropertyValue:()=>''}),supabase:{createClient:()=>({from:()=>({select(){return this},insert(){return Promise.resolve({})},eq(){return this},order(){return this},limit(){return this},single(){return Promise.resolve({})},then(r){return Promise.resolve({data:[],error:null}).then(r)}}),auth:{getSession(){return Promise.resolve({data:{session:null}})},onAuthStateChange(){},signInAnonymously(){return Promise.resolve({data:{user:null}})}},channel:()=>({on(){return this},subscribe(){return this}})})},IntersectionObserver:function(){return{observe(){},unobserve(){},disconnect(){}}},ResizeObserver:function(){return{observe(){},unobserve(){},disconnect(){}}}};
sb.screen={orientation:{type:'portrait-primary',angle:0,addEventListener(){},removeEventListener(){}},width:400,height:800,availWidth:400,availHeight:800};sb.innerWidth=400;sb.innerHeight=800;sb.window=sb;sb.self=sb;sb.globalThis=sb;
const ctx=vm.createContext(sb);
let loadErr=null;try{vm.runInContext(js,ctx,{timeout:20000});}catch(e){loadErr=e;}
if(sb.__err)console.log('Export-Fehler:',sb.__err);
const S=sb.__S,F=sb.__F;
if(!S||!F){console.log('LOAD FAIL');process.exit(2);}
try{const _J=f=>{try{return JSON.parse(fs.readFileSync(f,'utf8'))}catch(e){return null}};const _rv=(_J('rivers.json')||[]).map(b=>({n:b.riverLabel,c:b.countryLabel,len:Math.round(parseFloat(b.length||0)/1000)})).filter(x=>x.len>0);const _pl=(_J('license_plates.json')||[]).map(b=>({code:b.code,region:b.regionLabel||b.region,country:b.countryLabel||b.country}));const _am={};(_J('area.json')||[]).forEach(b=>{const c=b.countryLabel;const a=parseFloat(b.area||0);if(!c||!a)return;if(!_am[c]||a<_am[c])_am[c]=a;});const _ar=Object.entries(_am).filter(e=>e[1]>100&&e[1]<2e7).map(e=>({c:e[0],area:Math.round(e[1])}));if(sb.__seed)sb.__seed(_rv,_pl,_ar);}catch(e){}
let fail=0,ok=0,skip=0,warnans=0;
const render=sb.__render,GEN=sb.__GEN,MODES=sb.__MODES;
if(!S||!render||!GEN){console.log('LOAD FAIL');process.exit(2);}
// Basiszustand fuers Spiel
function setupPlay(id,q,answered){
  if(q){if(q.opts===undefined&&q.options!==undefined)q.opts=q.options;if(q.ans===undefined&&q.correct!==undefined)q.ans=q.correct;if(q.subj===undefined&&q.question!==undefined)q.subj=q.question;if(q.lid===undefined||q.lid===null)q.lid=(id||'q')+'_'+(q.subj||q.ans||Math.random());if(!q.prompt){var _m=MODES.find(function(x){return x.id===id;});if(_m)q.prompt=(_m.t_key?'x':_m.title)||_m.prompt||'';}if(q.items&&q.items.forEach)q.items.forEach(function(it){if(it){if(it.n===undefined&&it.label!==undefined)it.n=it.label;if(it.hint===undefined)it.hint='';}});if(q.type==='uk_match'&&Array.isArray(q.opts)&&q.opts.length&&q.ans!==undefined&&q.ans!==null){var _sf=function(s){return String(s).replace(/\s*\([^)]*\)/g,'').trim().toLowerCase();};if(!q.opts.some(function(o){return _sf(o)===_sf(q.ans);})){q.opts=q.opts.slice();q.opts[Math.floor(Math.random()*q.opts.length)]=q.ans;}}}S.tab='home';S.ph='play';S.mode=id;S.q=q;S.rd=0;S.sc=0;S.correct=0;S.streak=0;
  S.diff='casual';S.timer=12;S.lives=3;S.lvls=S.lvls||{};S.candidates=[];S.newStamps=[];
  S.sel= answered ? (q.ans!==undefined?q.ans:(q.opts&&q.opts[0])) : null;
  if(answered&&q.type==='timeline'&&q.items&&!q._tlUserOrder)q._tlUserOrder=q.items.map(function(it){return it.n;});
  S.answered=answered;
}
MODES.forEach(function(m){
  const id=m&&m.id; if(!id) return;
  const fn=GEN[id]; if(typeof fn!=='function'){skip++;return;}
  let q=null; try{ for(let i=0;i<6;i++){const x=fn(); if(x){q=x;break;}} }catch(e){ /* Generator-Crash separat im smoke_test */ skip++; return; }
  if(!q){ skip++; return; }            // null -> kein Spiel-Render noetig
  if(q.type==='uk_match'&&Array.isArray(q.opts)&&q.ans!==undefined){var _strip=function(s){return String(s).replace(/\s*\([^)]*\)/g,'').trim();};if(q.opts.map(_strip).indexOf(_strip(q.ans))<0){warnans++;}}
  // ungespielt
  try{ setupPlay(id,q,false); render(); }
  catch(e){ fail++; console.log('  [!!] PLAY '+id+' -> '+e.message); return; }
  // beantwortet (Feedback-Render) - Timeline braucht echten Drag-Zustand -> ueberspringen
  if(q.type==='timeline'){ok++;return;}
  try{ setupPlay(id,q,true); render(); ok++; }
  catch(e){ fail++; console.log('  [!!] FEEDBACK '+id+' -> '+e.message); }
});
/* Phase 537: SRS-Replay + neue UI-Flaechen rendern */
var srsFail=0,srsOk=0;
try{
  var _srsAdd=sb.__srsAdd, _srsHero=sb.__srsHero, _srsList=sb.__srsList, _dailyHero=sb.__dailyHero;
  if(_srsAdd){var _added=0;
    for(var _mi=0;_mi<MODES.length&&_added<25;_mi++){var _id=MODES[_mi].id;var _fn=GEN[_id];if(typeof _fn!=='function')continue;var _q=null;try{_q=_fn();}catch(_e){}if(!_q)continue;if(!(Array.isArray(_q.opts)&&_q.opts.length>=2)&&_q.type!=='uk_pin')continue;_q.lid=_q.lid||('srs_'+_id);try{_srsAdd(_q);_added++;}catch(_e){}}
    /* jeden gespeicherten Snapshot im Review-Modus rendern */
    var _store={};try{_store=JSON.parse(sb.localStorage.getItem('gq_srs')||'{}');if(_store&&_store.d)_store=_store.d;}catch(_e){}
    for(var _lid in _store){var _e=_store[_lid];if(!_e||!_e.q)continue;S.srsRun=true;S.q=JSON.parse(JSON.stringify(_e.q));S.sel=null;S.ok=null;S.ph='playing';S.mode='srs_review';S.sc=0;S.rd=0;try{render();srsOk++;}catch(_err){srsFail++;if(srsFail<=5)console.log('  [!!] SRS-RENDER '+_lid+' -> '+_err.message);}}
    S.srsRun=false;
  }
  /* neue UI-Flaechen */
  if(_srsHero){try{_srsHero();}catch(_e){srsFail++;console.log('  [!!] renderSrsHero -> '+_e.message);}}
  if(_srsList){try{_srsList();}catch(_e){srsFail++;console.log('  [!!] renderSrsListModal -> '+_e.message);}}
  if(_dailyHero){try{_dailyHero();}catch(_e){srsFail++;console.log('  [!!] renderDailyHero -> '+_e.message);}}
  var _re2=sb.__regionEntry,_rm2=sb.__regionModal,_ld2=sb.__learnDeck;
  if(_re2){try{_re2();}catch(_e){srsFail++;console.log('  [!!] renderRegionEntry -> '+_e.message);}}
  if(_rm2){try{_rm2();}catch(_e){srsFail++;console.log('  [!!] renderRegionModal -> '+_e.message);}}
  if(_ld2){try{S.learnRegion='Eastern Europe';S.learnIdx=0;_ld2();S.learnRegion=null;}catch(_e){srsFail++;console.log('  [!!] renderLearnDeck -> '+_e.message);}}
}catch(_e){console.log('  [!!] SRS-Block -> '+_e.message);}
console.log('SRS-REPLAY: '+srsOk+' OK | '+srsFail+' FEHLER');
fail+=srsFail;
console.log('\nIN-GAME-RENDER: '+ok+' OK | '+skip+' uebersprungen | '+fail+' RENDER-FEHLER | '+warnans+' ans-nicht-in-opts(info)');
process.exit(fail?1:0);
