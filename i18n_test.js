#!/usr/bin/env node
/* GeoQuest — i18n-Vollstaendigkeitstest (Phase 519)
 * Laedt GeoQuest.html, sammelt alle tatsaechlich genutzten uebersetzbaren Strings
 * (_tc("..")/_tcc("..")-Literale + MODES.prompt) und prueft, ob jeder einen
 * Eintrag in _CONTENT_I18N.en UND .pl hat. Fehlt einer, sehen EN/PL-Spieler Deutsch.
 * Exit 1 bei Luecken.  ->  node i18n_test.js
 */
const fs = require('fs'), vm = require('vm');
const html = fs.readFileSync('GeoQuest.html', 'utf8');
let js = [...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)]
  .filter(m => !/\bsrc\s*=/.test(m[1])).map(m => m[2]).join('\n;\n');
js += ";try{globalThis.__C=_CONTENT_I18N;globalThis.__M=MODES;}catch(e){}";
const el = new Proxy({}, { get: () => () => {} });
const doc = { addEventListener(){}, getElementById:()=>null, querySelector:()=>null, querySelectorAll:()=>[], createElement:()=>el,
  documentElement:{ style:{setProperty(){}}, lang:'de', setAttribute(){}, classList:{add(){},remove(){}} }, head:el, body:el };
const ls = new Map();
const sb = { console, setTimeout:()=>0, clearTimeout:()=>{}, setInterval:()=>0, Math, Date, JSON, Object, Array, String, Number, Boolean, RegExp, Map, Set, Symbol, isNaN, parseInt, parseFloat, encodeURIComponent, decodeURIComponent,
  document:doc, navigator:{ language:'de', serviceWorker:{ register(){return Promise.resolve();}, getRegistrations(){return Promise.resolve([]);} }, geolocation:{} },
  location:{ href:'', search:'' },
  localStorage:{ getItem:k=>ls.has(k)?ls.get(k):null, setItem:(k,v)=>ls.set(k,String(v)), removeItem:k=>ls.delete(k) },
  matchMedia:()=>({matches:false,addEventListener(){}}), fetch:()=>Promise.reject(), addEventListener(){},
  supabase:{ createClient:()=>({ from:()=>({select(){return this;},eq(){return this;},then(r){return Promise.resolve({data:[]}).then(r);}}),
    auth:{ getSession(){return Promise.resolve({data:{session:null}});}, onAuthStateChange(){}, signInAnonymously(){return Promise.resolve({data:{user:null}});} } }) } };
sb.window = sb; sb.self = sb; sb.globalThis = sb;
try { vm.runInContext(js, vm.createContext(sb), { timeout:20000 }); } catch (e) {}
const C = sb.__C || {}, MODES = sb.__M;
if (!C.en || !C.pl || !MODES) { console.error('i18n-TEST konnte nicht starten (_CONTENT_I18N/MODES fehlen).'); process.exit(2); }
const en = new Set(Object.keys(C.en)), pl = new Set(Object.keys(C.pl));
function dec(raw){ try { return JSON.parse(raw); } catch(e){ return null; } }
const used = new Set();
let m; const reTc = /_tcc?\((\"(?:[^\"\\]|\\.)*\")\)/g;
while ((m = reTc.exec(js))) { const s = dec(m[1]); if (s && /[A-Za-zÄÖÜäöü]/.test(s)) used.add(s); }
MODES.forEach(mo => { if (mo && mo.prompt && /[A-Za-zÄÖÜäöü]/.test(mo.prompt)) used.add(mo.prompt); });
const missEn = [], missPl = [];
used.forEach(s => { if (!en.has(s)) missEn.push(s); if (!pl.has(s)) missPl.push(s); });
console.log('='.repeat(58));
console.log(' GeoQuest i18n-Vollstaendigkeitstest');
console.log('='.repeat(58));
console.log(' CONTENT_I18N: en=' + en.size + ' pl=' + pl.size + ' | genutzt=' + used.size);
console.log(' FEHLT in EN: ' + missEn.length + ' | FEHLT in PL: ' + missPl.length);
if (missEn.length) { console.log('\n FEHLT EN (max 30):'); missEn.slice(0,30).forEach(s => console.log('  [!!] ' + s)); }
if (missPl.length) { console.log('\n FEHLT PL (max 30):'); missPl.slice(0,30).forEach(s => console.log('  [!!] ' + s)); }
process.exit((missEn.length || missPl.length) ? 1 : 0);
