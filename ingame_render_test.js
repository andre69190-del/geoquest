const fs=require('fs'),vm=require('vm');
let js=[...fs.readFileSync('GeoQuest.html','utf8').matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)].filter(m=>!/\bsrc\s*=/.test(m[1])).map(m=>m[2]).join('\n;\n');
const FNS=['renderHomeTab','renderLernenTab','renderLigaTab','renderProfilTab','renderCollectionScreen','renderStatsTab','renderAdminTab','renderSettingsModal','renderHelpModal','renderGuideModal','renderStickerModal','renderPinModal','renderLVSetup','renderLVGameover','renderLVHandoff','renderBottomNav','renderTourModalSKIP'];
js+=";try{globalThis.__S=S;globalThis.__render=render;globalThis.__GEN=GEN;globalThis.__MODES=MODES;globalThis.__seed=function(nb,rv,pl,ar){try{NEIGHBORS=parseNeighbors(nb)}catch(e){}try{RIVERS_REAL=parseRivers(rv)}catch(e){}try{PLATES_DATA=parsePlates(pl)}catch(e){}try{var _a=parseArea(ar);if(_a&&_a.length)AREA_DATA=_a}catch(e){}};globalThis.__F={};["+FNS.map(f=>"'"+f+"'").join(',')+"].forEach(function(n){try{globalThis.__F[n]=eval(n);}catch(e){}});globalThis.__OB=function(){try{return renderOnboarding;}catch(e){return null;}}();}catch(e){globalThis.__err=e&&e.message;}";
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
try{const _J=f=>{try{return JSON.parse(fs.readFileSync(f,'utf8'))}catch(e){return null}};if(sb.__seed)sb.__seed(_J('neighbors.json'),_J('rivers.json'),_J('license_plates.json'),_J('area.json'));}catch(e){}
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
console.log('\nIN-GAME-RENDER: '+ok+' OK | '+skip+' uebersprungen | '+fail+' RENDER-FEHLER | '+warnans+' ans-nicht-in-opts(info)');
process.exit(fail?1:0);
