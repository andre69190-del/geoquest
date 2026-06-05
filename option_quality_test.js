#!/usr/bin/env node
/* GeoQuest — Options-Qualitaetstest (Phase 517)
 * Laedt GeoQuest.html, ruft jeden MC-Generator 12x auf und meldet:
 *   - DUP   : dieselbe Option erscheint mehrfach (inkl. Antwort doppelt)
 *   - SINGLE: nur 1 Option bei einem MC-Typ (uk_match etc.) -> unspielbar
 * Pin/Eingabe/Map-Typen ohne opts werden ignoriert.
 * Exit 1 bei DUP oder SINGLE.  ->  node option_quality_test.js
 */
const fs = require('fs'), vm = require('vm');
const html = fs.readFileSync('GeoQuest.html', 'utf8');
let js = [...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)]
  .filter(m => !/\bsrc\s*=/.test(m[1])).map(m => m[2]).join('\n;\n');
js += ";try{globalThis.__G=GEN;globalThis.__M=MODES;}catch(e){}";
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
const GEN = sb.__G, MODES = sb.__M;
if (!GEN || !MODES) { console.error('OPTIONS-TEST konnte nicht starten (GEN/MODES fehlen).'); process.exit(2); }
// Typen, die bewusst keine Auswahl-Optionen haben:
const NOOPT = /^(uk_pin|pin|map_|airport|ds100|.*_input|beta_spotter|letter|word|continent|flag_draw)/;
const dup = {}, single = {};
for (const m of MODES) {
  const fn = GEN[m && m.id]; if (typeof fn !== 'function') continue;
  for (let i = 0; i < 12; i++) {
    let q; try { q = fn(); } catch (e) { break; }
    if (!q || !Array.isArray(q.opts)) continue;
    const o = q.opts.map(String);
    if (new Set(o).size < o.length) dup[m.id] = o;
    if (o.length === 1 && q.type && !NOOPT.test(q.type)) single[m.id] = q.type;
  }
}
const dk = Object.keys(dup), sk = Object.keys(single);
console.log('='.repeat(58));
console.log(' GeoQuest Options-Qualitaetstest');
console.log('='.repeat(58));
console.log(' DUP (doppelte Option): ' + dk.length + ' | SINGLE (1 Option bei MC): ' + sk.length);
if (dk.length) { console.log('\n DUP:'); dk.forEach(id => console.log('  [!!] ' + id + '  ' + JSON.stringify(dup[id]))); }
if (sk.length) { console.log('\n SINGLE:'); sk.forEach(id => console.log('  [!!] ' + id + '  type=' + single[id])); }
process.exit((dk.length || sk.length) ? 1 : 0);
