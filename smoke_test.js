#!/usr/bin/env node
/* GeoQuest — Generator-Rauchtest (Phase 484)
 * Laedt GeoQuest.html, stubt Browser-APIs, ruft jeden GEN[id]() einmal auf
 * und meldet Modi, die werfen (THROW) oder leer zurueckkommen (NULL).
 * Exit 1, wenn THROWs auftreten.  ->  node smoke_test.js
 */
const fs = require('fs');
const vm = require('vm');
const html = fs.readFileSync('GeoQuest.html', 'utf8');
const scripts = [];
const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
let m;
while ((m = re.exec(html))) { if (/\bsrc\s*=/.test(m[1])) continue; scripts.push(m[2]); }
let js = scripts.join('\n;\n');
js += "\n;try{ if(typeof GEN!=='undefined') globalThis.__GEN=GEN; if(typeof MODES!=='undefined') globalThis.__MODES=MODES; if(typeof S!=='undefined') globalThis.__S=S; }catch(e){ globalThis.__exportErr=e; }";

const lsMap = new Map();
const elStub = new Proxy({}, { get: (t, k) => {
  if (k === 'style') return new Proxy({}, { get: () => () => {}, set: () => true });
  if (k === 'classList') return { add(){}, remove(){}, contains(){return false;}, toggle(){} };
  if (k === 'getBoundingClientRect') return () => ({top:0,left:0,right:0,bottom:0,width:0,height:0});
  if (['appendChild','removeChild','insertBefore','setAttribute','getAttribute','removeAttribute','addEventListener','removeEventListener','remove','focus','blur','click','scrollIntoView','setProperty'].indexOf(k)>=0) return () => {};
  if (k === 'querySelector') return () => null;
  if (k === 'querySelectorAll') return () => [];
  return '';
}});
const documentStub = {
  addEventListener(){}, removeEventListener(){}, getElementById(){return null;},
  querySelector(){return null;}, querySelectorAll(){return [];}, createElement(){return elStub;}, createElementNS(){return elStub;},
  documentElement: { style:{setProperty(){},getPropertyValue(){return '';}}, lang:'de',
    classList:{add(){},remove(){},toggle(){},contains(){return false;}},
    setAttribute(){}, getAttribute(){return null;}, removeAttribute(){}, appendChild(){}, addEventListener(){} },
  head: elStub, body: elStub, cookie: '',
};
const sandbox = {
  console, setTimeout:()=>0, clearTimeout:()=>{}, setInterval:()=>0, clearInterval:()=>{},
  requestAnimationFrame:()=>0, cancelAnimationFrame:()=>{},
  Math, Date, JSON, Object, Array, String, Number, Boolean, RegExp, Map, Set, Symbol, isNaN, parseInt, parseFloat, encodeURIComponent, decodeURIComponent,
  document: documentStub,
  navigator: { language:'de', languages:['de'], onLine:true, userAgent:'node',
    geolocation:{ watchPosition(){}, getCurrentPosition(){} },
    serviceWorker:{ register(){return Promise.resolve();}, addEventListener(){}, getRegistrations(){return Promise.resolve([]);}, getRegistration(){return Promise.resolve(null);}, ready:Promise.resolve({}) } },
  location: { href:'https://geoquest-web.vercel.app/play', search:'', hash:'', reload(){}, replace(){}, assign(){} },
  localStorage: { getItem:k=>(lsMap.has(k)?lsMap.get(k):null), setItem:(k,v)=>lsMap.set(k,String(v)), removeItem:k=>lsMap.delete(k), clear:()=>lsMap.clear() },
  matchMedia: () => ({ matches:false, addEventListener(){}, removeEventListener(){}, addListener(){}, removeListener(){} }),
  fetch: () => Promise.reject(new Error('no-net')),
  alert(){}, confirm(){return false;}, prompt(){return null;}, addEventListener(){}, removeEventListener(){},
  scrollTo(){}, scroll(){}, getComputedStyle:()=>({getPropertyValue:()=>''}),
  supabase: { createClient: () => ({ from:()=>({select(){return this;},insert(){return Promise.resolve({});},eq(){return this;},order(){return this;},limit(){return this;},single(){return Promise.resolve({});},then(r){return Promise.resolve({data:[],error:null}).then(r);}}), auth:{getSession(){return Promise.resolve({data:{session:null}});},onAuthStateChange(){},signInWithPassword(){return Promise.resolve({});}}, channel:()=>({on(){return this;},subscribe(){return this;}}) }) },
  IntersectionObserver: function(){ return {observe(){},unobserve(){},disconnect(){}}; },
  ResizeObserver: function(){ return {observe(){},unobserve(){},disconnect(){}}; },
};
sandbox.window = sandbox; sandbox.self = sandbox; sandbox.globalThis = sandbox;
const ctx = vm.createContext(sandbox);
let loadErr = null;
try { vm.runInContext(js, ctx, { filename:'GeoQuest.inline.js', timeout:20000 }); } catch (e) { loadErr = e; }
const GEN = sandbox.__GEN, MODES = sandbox.__MODES;
if (!GEN || !MODES) {
  console.error('RAUCHTEST KONNTE NICHT STARTEN - GEN/MODES nicht exportiert.');
  if (loadErr) console.error('Load-Fehler:', loadErr.message);
  process.exit(2);
}
// minimalen Spielzustand seeden (Generatoren erwarten teils S.askedLids etc.)
try { const S = sandbox.__S; if (S) { S.askedLids = new Set(); S.mode = S.mode||''; S.diff = S.diff||'casual'; S.lvls = S.lvls||{}; } } catch(_e){}
const EXPECTED_NULL = new Set(['river_real','plate_casual','plate_hard','hl_area','neighbor','neighbor_fake','neighbor_count','border_q','logic_grid','travel_route','slf']);
const throwsArr = [], nullsArr = [], unexpectedNull = [];
let okCount = 0, tested = 0, wsNull = 0;
for (const mode of MODES) {
  const id = mode && mode.id; if (!id) continue;
  const fn = GEN[id]; if (typeof fn !== 'function') continue;
  tested++;
  let got = null, threw = null;
  for (let i = 0; i < 6; i++) {       // mehrfach: NULL nur, wenn IMMER leer
    try { const q = fn(); if (q !== null && q !== undefined) { got = q; break; } }
    catch (e) { threw = e; break; }
  }
  if (threw) { throwsArr.push(id + '  ->  ' + threw.message); continue; }
  if (got) { okCount++; continue; }
  // leer geblieben: ws_* geben absichtlich null zurueck (initWS-Pattern)
  if (/^ws_/.test(id) || /_ws_/.test(id)) { wsNull++; continue; }
  nullsArr.push(id);
  if (!EXPECTED_NULL.has(id)) unexpectedNull.push(id);
}
console.log('='.repeat(58));
console.log(' GeoQuest Generator-Rauchtest');
console.log('='.repeat(58));
console.log(' Getestet: ' + tested + ' | OK: ' + okCount + ' | NULL: ' + nullsArr.length + ' | THROW: ' + throwsArr.length + ' | ws_null(ok): ' + wsNull);
if (throwsArr.length) { console.log('\n THROW (Crash) - MUSS gefixt werden:'); throwsArr.forEach(s => console.log('  [!!] ' + s)); }
if (nullsArr.length) { console.log('\n NULL (leer zurueck):'); console.log('  ' + nullsArr.join(', ')); }
if (unexpectedNull.length) { console.log('\n UNERWARTET NULL - MUSS gefixt/allowlisted werden:'); unexpectedNull.forEach(function(s){console.log('  [!!] ' + s);}); }
if (loadErr) console.log('\n (Top-Level-Load warf: ' + loadErr.message + ' - Generatoren trotzdem getestet.)');
process.exit((throwsArr.length || unexpectedNull.length) ? 1 : 0);
