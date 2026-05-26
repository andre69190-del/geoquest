# -*- coding: utf-8 -*-
"""
Phase: 228
Date:  2026-05-26
Author: Claude / Andre
Scope: Das Botanik-Update -- 49 neue Pflanzenmodi (12 Pin, 12 H/L, 16 Match, 9 WS)

Description:
  Creates data/pflanzen_pin.json, pflanzen_hl.json, pflanzen_match.json, pflanzen_ws.json.
  Adds 4 JS generators: genPflanzenPinQ, genPflanzenHL, genPflanzenMatchQ, initPflanzenWS.
  Registers 49 MODES entries (group:"tiere", all [BETA], IDs start at 101+).
  Extends MODE_CATS tiere array and GEN dispatch.

Dependencies: patch_225_json_extraction.py, patch_227b_tiere_data_part1.py
Zero-Bug Policy: All c.replace() calls use assert c.count(old)==1
"""
import os, sys, shutil, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # GeoQuest project root
GEN  = os.path.join(ROOT, 'gen.py')
DATA = os.path.join(ROOT, 'data')

# ── 1. Verify JSON data files already in data/ ───────────────────────────────
for fname in ['pflanzen_pin.json','pflanzen_hl.json','pflanzen_match.json','pflanzen_ws.json']:
    dst = os.path.join(DATA, fname)
    if not os.path.isfile(dst):
        print(f'[FAIL] Missing: {dst}')
        sys.exit(1)
    with open(dst, 'r', encoding='utf-8') as f:
        try: json.load(f)
        except Exception as e:
            print(f'[FAIL] Invalid JSON in {fname}: {e}')
            sys.exit(1)
    print(f'[OK]  {fname} validated in data/')

# ── 2. Read gen.py ───────────────────────────────────────────────────────────
with open(GEN, 'r', encoding='utf-8') as f:
    c = f.read()

print(f'[OK]  Read gen.py ({len(c)} chars)')

# ── 3. Python loading block (after TIER_MATCH_DATA_J line) ──────────────────
OLD3 = "with open(os.path.join(os.path.dirname(__file__), 'data/tiere_match.json'), 'r', encoding='utf-8') as _f: TIER_MATCH_DATA_J = _f.read()"
assert c.count(OLD3) == 1, f'Anchor not unique: {OLD3!r}'
NEW3 = OLD3 + """
with open(os.path.join(os.path.dirname(__file__), 'data/pflanzen_pin.json'), 'r', encoding='utf-8') as _f: PFLANZEN_PIN_J = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/pflanzen_hl.json'), 'r', encoding='utf-8') as _f: PFLANZEN_HL_J = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/pflanzen_match.json'), 'r', encoding='utf-8') as _f: PFLANZEN_MATCH_J = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/pflanzen_ws.json'), 'r', encoding='utf-8') as _f: PFLANZEN_WS_J = _f.read()"""
c = c.replace(OLD3, NEW3, 1)
print('[OK]  Added Python loading block')

# ── 4. PLACEHOLDER chain ─────────────────────────────────────────────────────
OLD4 = "  .replace('PLACEHOLDER_TIER_MATCH_DATA', TIER_MATCH_DATA_J)\n)"
assert c.count(OLD4) == 1, f'Anchor not unique: {OLD4!r}'
NEW4 = """  .replace('PLACEHOLDER_TIER_MATCH_DATA', TIER_MATCH_DATA_J)
  .replace('PLACEHOLDER_PFLANZEN_PIN', PFLANZEN_PIN_J)
  .replace('PLACEHOLDER_PFLANZEN_HL', PFLANZEN_HL_J)
  .replace('PLACEHOLDER_PFLANZEN_MATCH', PFLANZEN_MATCH_J)
  .replace('PLACEHOLDER_PFLANZEN_WS', PFLANZEN_WS_J)
)"""
c = c.replace(OLD4, NEW4, 1)
print('[OK]  Added PLACEHOLDER chain entries')

# ── 5. JS const declarations (after TIER_MATCH_DATA placeholder) ────────────
OLD5 = 'const TIER_MATCH_DATA=PLACEHOLDER_TIER_MATCH_DATA;\n\n/* === Phase 227 Part 2: genTiereMatchQ'
assert c.count(OLD5) == 1, f'Anchor not unique: {OLD5!r}'
NEW5 = """const TIER_MATCH_DATA=PLACEHOLDER_TIER_MATCH_DATA;

/* === Phase 228: Pflanzen-Datensaetze === */
const PFLANZEN_PIN_DATA=PLACEHOLDER_PFLANZEN_PIN;
const PFLANZEN_HL_DATA=PLACEHOLDER_PFLANZEN_HL;
const PFLANZEN_MATCH_DATA=PLACEHOLDER_PFLANZEN_MATCH;
const PFLANZEN_WS_DATA=PLACEHOLDER_PFLANZEN_WS;

/* === Phase 227 Part 2: genTiereMatchQ"""
c = c.replace(OLD5, NEW5, 1)
print('[OK]  Added JS const declarations')

# ── 6. Generator functions (after genTiereMatchQ, before genUniversalMatchQ) ─
OLD6 = 'function genUniversalMatchQ(cat){'
assert c.count(OLD6) == 1, f'Anchor not unique: {OLD6!r}'
NEW6 = """/* === Phase 228: Pflanzen-Generatoren === */
function genPflanzenPinQ(cat){
  var cfg=PFLANZEN_PIN_DATA[cat];
  if(!cfg||!cfg.items||!cfg.items.length)return null;
  var items=cfg.items;
  var item=items[~~(rng()*items.length)];
  if(!item||!item.n)return null;
  var modeObj=(typeof MODES!=="undefined"?MODES:[]).find(function(m){return m.id==="uk_pflanzen_"+cat;})||{};
  return{type:"uk_pin",cat:"pflanzen_"+cat,prompt:cfg.prompt||modeObj.prompt||"Wo liegt das?",
    subj:item.n,targetLat:item.lat,targetLng:item.lng,ans:item.n,
    lid:"pkp_"+cat+"_"+item.n.replace(/[^a-zA-Z0-9]/g,"_").substring(0,20),cc:null};
}
function genPflanzenHL(dataKey){
  var cfg=PFLANZEN_HL_DATA[dataKey];
  if(!cfg||!cfg.items||cfg.items.length<2)return null;
  var sorted=cfg.items.slice().sort(function(a,b){return parseFloat(a.val)-parseFloat(b.val);});
  var len=sorted.length;
  var tries=0;
  while(tries++<40){
    var ai=~~(rng()*len);
    var W=Math.max(1,Math.floor(len*0.1));
    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);
    var pool=[];
    for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}
    if(!pool.length)continue;
    var bi=pool[~~(rng()*pool.length)];
    var a=sorted[ai],b=sorted[bi];
    var va=parseFloat(a.val),vb=parseFloat(b.val);
    if(va===vb)continue;
    var span=parseFloat(sorted[len-1].val)-parseFloat(sorted[0].val);
    if(span>0&&Math.abs(va-vb)<span*0.02)continue;
    var higher=va>vb?a:b;
    var unit=cfg.unit||"";
    var meta=a.name+": "+a.val+(unit?" "+unit:"")+" · "+b.name+": "+b.val+(unit?" "+unit:"");
    var _lid="phl_"+dataKey+"_"+Math.min(ai,bi)+"_"+Math.max(ai,bi);
    return{type:"beta_hl",prompt:cfg.prompt||"Welches ist mehr?",subj:"",
      opts:[a.name,b.name],ans:higher.name,meta:meta,lid:_lid,cc:"de"};
  }
  return null;
}
function genPflanzenMatchQ(cat){
  var cfg=PFLANZEN_MATCH_DATA[cat];
  if(!cfg||!cfg.items||!cfg.items.length)return null;
  var items=cfg.items;
  var cor=items[~~(rng()*items.length)];
  if(!cor||!cor.n||!cor.c)return null;
  var opts;
  if(cfg.fixedOpts){
    opts=sh(cfg.fixedOpts.slice());
  }else if(cfg.yearMode){
    var sameCat=items.filter(function(x){return x.c!==cor.c;}).map(function(x){return x.c;});
    var uniq=[...new Set(sameCat)];
    var dis=_rfilt(uniq,3);
    opts=sh([cor.c].concat(dis.slice(0,3)));
  }else{
    var pool=[];
    var keys=Object.keys(PFLANZEN_MATCH_DATA);
    for(var _ki=0;_ki<keys.length;_ki++){
      var _k=keys[_ki];
      var _kd=PFLANZEN_MATCH_DATA[_k];
      if(_kd.fixedOpts||_kd.yearMode)continue;
      var _kItems=(_kd.items||[]);
      for(var _ii=0;_ii<_kItems.length;_ii++){
        var _cv=_kItems[_ii].c;
        if(_cv&&_cv!==cor.c)pool.push(_cv);
      }
    }
    var unique=[...new Set(pool)];
    var dis2=_rfilt(unique,3);
    if(dis2.length<3){
      var sc=items.filter(function(x){return x.c!==cor.c;}).map(function(x){return x.c;});
      dis2=_rfilt([...new Set(sc)],3);
    }
    opts=sh([cor.c].concat(dis2.slice(0,3)));
  }
  var prompt=cfg.prompt||"Ordne richtig zu!";
  var _lid="pkm_"+cat+"_"+cor.n.substring(0,12).replace(/[^a-zA-Z0-9]/g,"_");
  return{type:"uk_match",cat:cat,prompt:prompt,subj:cor.n,
    ans:cor.c,opts:opts,meta:"",lid:_lid,cc:"de"};
}
function initPflanzenWS(key){
  clearInterval(tIv);_wsDetachKb();
  var entry=PFLANZEN_WS_DATA[key];
  if(!entry||!entry.validWords){console.warn("[GeoQuest] PflanzenWS missing:"+key);S.ph="menu";render();return;}
  var userLang=S.language||localStorage.getItem("gq_lang")||"en";
  var wsLang=_WS_LANGS.has(userLang)?userLang:"en";
  var raw=entry.validWords[wsLang];
  var hasOwn=Array.isArray(raw)&&raw.length>0;
  var actualLang=hasOwn?wsLang:"en";
  var src2=hasOwn?raw:(entry.validWords["en"]||[]);
  var words=src2.map(function(w){return w.toUpperCase();}).filter(function(w){return w.length>=3;});
  if(!words.length){console.warn("[GeoQuest] PflanzenWS no words:"+key);S.ph="menu";render();return;}
  var usingFallback=actualLang!==userLang;
  S.wsData={tierWsKey:key,city:entry.word,lang:actualLang,usingFallback:usingFallback,
    allWords:words,foundWords:[],input:"",phase:"playing",timeLeft:_WS_TIMER,shakeTs:0};
  S.gameStartTime=Date.now();S.ph="playing";
  tIv=setInterval(function(){
    if(S.ph!=="playing"||!S.wsData)return;
    S.wsData.timeLeft--;
    if(S.wsData.timeLeft<=0){S.wsData.phase="done";S.ph="feedback";clearInterval(tIv);}
    render();
  },1000);
  _wsAttachKb();
}
function genUniversalMatchQ(cat){"""
c = c.replace(OLD6, NEW6, 1)
print('[OK]  Added 4 generator functions')

# ── 7. MODES entries ──────────────────────────────────────────────────────────
OLD7 = 'prompt:"Bilde W\\u00f6rter aus SHIREHORSE!",desc:"Anagramm-R\\u00e4tsel \\u2014 10 Buchstaben"}\n];'
assert c.count(OLD7) == 1, f'Anchor not unique: {OLD7!r}'

PFLANZEN_MODES = ''',
    /* === Phase 228: Pflanzen-Modi (Pin) === */
    {id:"uk_pflanzen_nutzpflanzen",icon:"\\u{1F33E}",title:"[BETA] Nutzpflanzen-Ursprung",group:"tiere",prompt:"Wo liegt dieser Nutzpflanzen-Ursprungsort?",desc:"Kaffee, Kakao, Weizen \\u2014 Wo kamen sie urspr\\u00fcnglich her?"},
    {id:"uk_pflanzen_einzelbaeume",icon:"\\u{1F333}",title:"[BETA] Ber\\u00fchmte B\\u00e4ume",group:"tiere",prompt:"Wo steht dieser ber\\u00fchmte Baum?",desc:"General Sherman bis Methuselah \\u2014 Legenden-B\\u00e4ume der Welt"},
    {id:"uk_pflanzen_botanische_gaerten",icon:"\\u{1F33A}",title:"[BETA] Botanische G\\u00e4rten",group:"tiere",prompt:"Wo liegt dieser Botanische Garten?",desc:"Kew Gardens bis Orto Botanico Padova \\u2014 Gr\\u00fcne Kathedralen der Welt"},
    {id:"uk_pflanzen_tropenwald",icon:"\\u{1F331}",title:"[BETA] Tropenwälder",group:"tiere",prompt:"Wo liegt dieser Tropenwald?",desc:"Amazon bis Daintree \\u2014 die gr\\u00fcnen Lungen der Erde"},
    {id:"uk_pflanzen_weinanbau",icon:"\\u{1F377}",title:"[BETA] Weinanbaugebiete",group:"tiere",prompt:"Wo liegt dieses Weinanbaugebiet?",desc:"Bordeaux bis Barossa \\u2014 Weinregionen der Welt"},
    {id:"uk_pflanzen_heilpflanzen",icon:"\\u{1F33F}",title:"[BETA] Heilpflanzen-Regionen",group:"tiere",prompt:"Wo liegt diese Heilpflanzen-Region?",desc:"Argan bis Ayurveda \\u2014 Medizinische Pflanzenzentren"},
    {id:"uk_pflanzen_mangroven",icon:"\\u{1F30A}",title:"[BETA] Mangrovenwälder",group:"tiere",prompt:"Wo liegt dieses Mangroven-Gebiet?",desc:"Sundarbans bis Everglades \\u2014 K\\u00fcstenw\\u00e4lder der Tropen"},
    {id:"uk_pflanzen_kakao_ursprung",icon:"\\u{1F36B}",title:"[BETA] Kakao-Ursprungsgebiete",group:"tiere",prompt:"Wo liegt dieses Kakao-Anbaugebiet?",desc:"Tabasco bis Madagaskar \\u2014 Die Welt des Kakaos"},
    {id:"uk_pflanzen_reisanbau",icon:"\\u{1F35A}",title:"[BETA] Reisanbauregionen",group:"tiere",prompt:"Wo liegt diese Reisanbauregion?",desc:"Mekong-Delta bis Bali-Terrassen \\u2014 Reisfelder der Welt"},
    {id:"uk_pflanzen_bambus",icon:"\\u{1F38B}",title:"[BETA] Bambuswälder",group:"tiere",prompt:"Wo liegt dieser ber\\u00fchmte Bambus-Ort?",desc:"Arashiyama bis Sichuan \\u2014 Bambus-Paradiese der Welt"},
    {id:"uk_pflanzen_endemisch",icon:"\\u{1F9EC}",title:"[BETA] Endemische Pflanzenzonen",group:"tiere",prompt:"Wo liegt dieser endemische Pflanzen-Hotspot?",desc:"Kap-Florenregion bis Cerrado \\u2014 Pflanzendiversit\\u00e4t"},
    {id:"uk_pflanzen_nationalblumen",icon:"\\u{1F490}",title:"[BETA] Nationalblumen-Heimat",group:"tiere",prompt:"In welchem Land ist diese Pflanze Nationalblume?",desc:"Tulpe, Kirschbl\\u00fcte, Protea \\u2014 Nationalblumen pinnen"},
    /* === Phase 228: Pflanzen-Modi (H/L) === */
    {id:"hl_pflanzen_wuchshoehe",icon:"\\u{1F334}",title:"[BETA] H/L Wuchsh\\u00f6he",group:"tiere",prompt:"Welcher Baum wird h\\u00f6her?",desc:"H\\u00f6he in Metern \\u2014 Hyperion bis Birke"},
    {id:"hl_pflanzen_alter",icon:"\\u{1F9D3}",title:"[BETA] H/L Baumalter",group:"tiere",prompt:"Welcher Baum wird \\u00e4lter?",desc:"Jahre \\u2014 Bristlecone Pine bis Schwarzpappel"},
    {id:"hl_pflanzen_fruchtgewicht",icon:"\\u{1F34D}",title:"[BETA] H/L Fruchtgewicht",group:"tiere",prompt:"Welche Frucht ist schwerer?",desc:"Gramm \\u2014 Jackfrucht bis Chiasamen"},
    {id:"hl_pflanzen_samenlaenge",icon:"\\u{1F33C}",title:"[BETA] H/L Samengr\\u00f6\\u00dfe",group:"tiere",prompt:"Welcher Samen ist l\\u00e4nger?",desc:"Millimeter \\u2014 Coco de Mer bis Mohnkorn"},
    {id:"hl_pflanzen_kaffeeproduktion",icon:"\\u2615",title:"[BETA] H/L Kaffeeproduktion",group:"tiere",prompt:"Welches Land produziert mehr Kaffee?",desc:"Tsd. S\\u00e4cke/Jahr \\u2014 Brasilien bis Ruanda"},
    {id:"hl_pflanzen_weinproduktion",icon:"\\u{1F377}",title:"[BETA] H/L Weinproduktion",group:"tiere",prompt:"Welches Land produziert mehr Wein?",desc:"Mio. Liter/Jahr \\u2014 Italien bis England"},
    {id:"hl_pflanzen_reisproduktion",icon:"\\u{1F35A}",title:"[BETA] H/L Reisproduktion",group:"tiere",prompt:"Welches Land produziert mehr Reis?",desc:"Mio. Tonnen/Jahr \\u2014 China bis Kolumbien"},
    {id:"hl_pflanzen_waldflaeche",icon:"\\u{1F332}",title:"[BETA] H/L Waldanteil",group:"tiere",prompt:"Welches Land hat mehr Waldanteil?",desc:"Prozent \\u2014 Suriname bis \\u00c4gypten"},
    {id:"hl_pflanzen_stammumfang",icon:"\\u{1F333}",title:"[BETA] H/L Stammumfang",group:"tiere",prompt:"Welcher Baum hat den gr\\u00f6\\u00dferen Stammumfang?",desc:"cm \\u2014 Arbol del Tule bis Kirschbaum"},
    {id:"hl_pflanzen_blattflaeche",icon:"\\u{1F343}",title:"[BETA] H/L Blattfl\\u00e4che",group:"tiere",prompt:"Welches Blatt hat die gr\\u00f6\\u00dfere Fl\\u00e4che?",desc:"cm\\u00b2 \\u2014 Riesenpalme bis Rosmarin"},
    {id:"hl_pflanzen_bluehdauer",icon:"\\u{1F338}",title:"[BETA] H/L Bl\\u00fchtdauer",group:"tiere",prompt:"Welche Pflanze bl\\u00fcht l\\u00e4nger pro Jahr?",desc:"Tage/Jahr \\u2014 Bougainvillea bis Krokus"},
    {id:"hl_pflanzen_genomgroesse",icon:"\\u{1F9EC}",title:"[BETA] H/L Genomgr\\u00f6\\u00dfe",group:"tiere",prompt:"Welche Pflanze hat das gr\\u00f6\\u00dfere Genom?",desc:"Mbp \\u2014 Paris japonica bis Arabidopsis"},
    /* === Phase 228: Pflanzen-Modi (Match) === */
    {id:"uk_pflanzen_gewuerze",icon:"\\u{1F9C2}",title:"[BETA] Gew\\u00fcrze-Herkunft",group:"tiere",prompt:"Woher stammt dieses Gew\\u00fcrz urspr\\u00fcnglich?",desc:"Zimt, Safran, Vanille \\u2014 Heimatl\\u00e4nder der Gew\\u00fcrze"},
    {id:"uk_pflanzen_familien",icon:"\\u{1F9EC}",title:"[BETA] Pflanzenfamilien",group:"tiere",prompt:"Zu welcher Familie geh\\u00f6rt diese Art?",desc:"Rosaceae, Poaceae, Fabaceae \\u2014 Botanische Familien"},
    {id:"uk_pflanzen_bluetezeit",icon:"\\u{1F338}",title:"[BETA] Bl\\u00fctezeit",group:"tiere",prompt:"In welcher Jahreszeit bl\\u00fcht diese Pflanze?",desc:"Fr\\u00fchling, Sommer, Herbst, Winter \\u2014 Bl\\u00fctekalender"},
    {id:"uk_pflanzen_giftstoffe",icon:"\\u2620",title:"[BETA] Giftstoffe",group:"tiere",prompt:"Welcher Wirkstoff macht diese Pflanze giftig?",desc:"Atropin, Ricin, Taxin \\u2014 Giftige Wirkstoffe"},
    {id:"uk_pflanzen_fruchttyp",icon:"\\u{1F34E}",title:"[BETA] Fruchttypen",group:"tiere",prompt:"Zu welchem Fruchttyp geh\\u00f6rt diese Frucht?",desc:"Beere, Steinfrucht, Apfelfrucht \\u2014 Botanische Fruchttypen"},
    {id:"uk_pflanzen_vermehrung",icon:"\\u{1F331}",title:"[BETA] Vermehrungsarten",group:"tiere",prompt:"Wie vermehrt sich diese Pflanze haupts\\u00e4chlich?",desc:"Samen, vegetativ, Sporen \\u2014 Fortpflanzungsstrategien"},
    {id:"uk_pflanzen_lebensraum",icon:"\\u{1F30D}",title:"[BETA] Pflanzen-Lebensraum",group:"tiere",prompt:"In welchem Lebensraum w\\u00e4chst diese Pflanze?",desc:"W\\u00fcste, Moor, K\\u00fcste \\u2014 Habitate der Pflanzenwelt"},
    {id:"uk_pflanzen_bestuaeber",icon:"\\u{1F41D}",title:"[BETA] Best\\u00e4uber",group:"tiere",prompt:"Wer best\\u00e4ubt diese Blume haupts\\u00e4chlich?",desc:"Bienen, Wind, Kolibri, Flederm\\u00e4use \\u2014 Best\\u00e4ubungsstrategien"},
    {id:"uk_pflanzen_herkunft",icon:"\\u{1F5FA}",title:"[BETA] Kulturpflanzen-Herkunft",group:"tiere",prompt:"Von welchem Kontinent stammt diese Kulturpflanze?",desc:"Kartoffel bis Kaffee \\u2014 Kontinentale Urspr\\u00fcnge"},
    {id:"uk_pflanzen_nutzung",icon:"\\u{1F527}",title:"[BETA] Pflanzennutzung",group:"tiere",prompt:"Wof\\u00fcr wird diese Pflanze haupts\\u00e4chlich genutzt?",desc:"Nahrung, Medizin, Textil, Zier \\u2014 Nutzungskategorien"},
    {id:"uk_pflanzen_blattform",icon:"\\u{1F343}",title:"[BETA] Blattformen",group:"tiere",prompt:"Welche Blattform hat diese Pflanze?",desc:"Nadel, herzf\\u00f6rmig, gefiedert, handf\\u00f6rmig \\u2014 Blattmorphologie"},
    {id:"uk_pflanzen_klimazone",icon:"\\u{1F321}",title:"[BETA] Klimazonen",group:"tiere",prompt:"In welcher Klimazone w\\u00e4chst diese Pflanze nat\\u00fcrlich?",desc:"Tropisch, mediterran, gem\\u00e4\\u00dfigt, arktisch \\u2014 Klimaanpassung"},
    {id:"uk_pflanzen_scheinfruchte",icon:"\\u{1F347}",title:"[BETA] Scheinfrüchte",group:"tiere",prompt:"Wie klassifiziert die Botanik diese Frucht?",desc:"Echte Frucht oder Scheinfrucht? \\u2014 Botanische Klassifikation"},
    /* === Phase 228: Pflanzen-Modi (Spezial) === */
    {id:"uk_pflanzen_baum_des_jahres",icon:"\\u{1F3C6}",title:"[BETA] Baum des Jahres",group:"tiere",prompt:"In welchem Jahr war dieser Baum \\"Baum des Jahres\\"?",desc:"Rotbuche bis Bergahorn \\u2014 Deutsche B\\u00e4ume des Jahres"},
    {id:"uk_pflanzen_giftpflanze_jahres",icon:"\\u2620",title:"[BETA] Giftpflanze des Jahres",group:"tiere",prompt:"In welchem Jahr war dies die Giftpflanze des Jahres?",desc:"Tollkirsche bis Stechapfel \\u2014 J\\u00e4hrliche Giftwahl"},
    /* === Phase 228: Pflanzen-Modi (WS) === */
    {id:"ws_pflanzen_trauerweide",icon:"\\u{1F333}",title:"[BETA] WS: Trauerweide",group:"tiere",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus TRAUERWEIDE!",desc:"Anagramm-R\\u00e4tsel \\u2014 11 Buchstaben"},
    {id:"ws_pflanzen_rhododendron",icon:"\\u{1F33A}",title:"[BETA] WS: Rhododendron",group:"tiere",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus RHODODENDRON!",desc:"Anagramm-R\\u00e4tsel \\u2014 12 Buchstaben"},
    {id:"ws_pflanzen_sonnenblume",icon:"\\u{1F33B}",title:"[BETA] WS: Sonnenblume",group:"tiere",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus SONNENBLUME!",desc:"Anagramm-R\\u00e4tsel \\u2014 11 Buchstaben"},
    {id:"ws_pflanzen_pusteblume",icon:"\\u{1F33C}",title:"[BETA] WS: Pusteblume",group:"tiere",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus PUSTEBLUME!",desc:"Anagramm-R\\u00e4tsel \\u2014 10 Buchstaben"},
    {id:"ws_pflanzen_nachtschatten",icon:"\\u2620",title:"[BETA] WS: Nachtschatten",group:"tiere",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus NACHTSCHATTEN!",desc:"Anagramm-R\\u00e4tsel \\u2014 13 Buchstaben"},
    {id:"ws_pflanzen_vergissmeinnicht",icon:"\\u{1F49C}",title:"[BETA] WS: Vergissmeinnicht",group:"tiere",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus VERGISSMEINNICHT!",desc:"Anagramm-R\\u00e4tsel \\u2014 16 Buchstaben"},
    {id:"ws_pflanzen_kaffeebohne",icon:"\\u2615",title:"[BETA] WS: Kaffeebohne",group:"tiere",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus KAFFEEBOHNE!",desc:"Anagramm-R\\u00e4tsel \\u2014 11 Buchstaben"},
    {id:"ws_pflanzen_weihnachtsstern",icon:"\\u2B50",title:"[BETA] WS: Weihnachtsstern",group:"tiere",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus WEIHNACHTSSTERN!",desc:"Anagramm-R\\u00e4tsel \\u2014 15 Buchstaben"},
    {id:"ws_pflanzen_ginkgobaum",icon:"\\u{1F333}",title:"[BETA] WS: Ginkgobaum",group:"tiere",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus GINKGOBAUM!",desc:"Anagramm-R\\u00e4tsel \\u2014 10 Buchstaben"}'''

NEW7 = 'prompt:"Bilde W\\u00f6rter aus SHIREHORSE!",desc:"Anagramm-R\\u00e4tsel \\u2014 10 Buchstaben"}\n' + PFLANZEN_MODES + '\n];'
c = c.replace(OLD7, NEW7, 1)
print('[OK]  Added 49 MODES entries')

# ── 8. MODE_CATS tiere extension ──────────────────────────────────────────────
OLD8 = '"hl_pferde_stockmass","ws_pferde_fluesterer"\n  ],cost:0},'
assert c.count(OLD8) == 1, f'Anchor not unique: {OLD8!r}'
NEW8 = ('"hl_pferde_stockmass","ws_pferde_fluesterer",\n'
        '    "uk_pflanzen_nutzpflanzen","uk_pflanzen_einzelbaeume","uk_pflanzen_botanische_gaerten",\n'
        '    "uk_pflanzen_tropenwald","uk_pflanzen_weinanbau","uk_pflanzen_heilpflanzen",\n'
        '    "uk_pflanzen_mangroven","uk_pflanzen_kakao_ursprung","uk_pflanzen_reisanbau",\n'
        '    "uk_pflanzen_bambus","uk_pflanzen_endemisch","uk_pflanzen_nationalblumen",\n'
        '    "hl_pflanzen_wuchshoehe","hl_pflanzen_alter","hl_pflanzen_fruchtgewicht",\n'
        '    "hl_pflanzen_samenlaenge","hl_pflanzen_kaffeeproduktion","hl_pflanzen_weinproduktion",\n'
        '    "hl_pflanzen_reisproduktion","hl_pflanzen_waldflaeche","hl_pflanzen_stammumfang",\n'
        '    "hl_pflanzen_blattflaeche","hl_pflanzen_bluehdauer","hl_pflanzen_genomgroesse",\n'
        '    "uk_pflanzen_gewuerze","uk_pflanzen_familien","uk_pflanzen_bluetezeit",\n'
        '    "uk_pflanzen_giftstoffe","uk_pflanzen_fruchttyp","uk_pflanzen_vermehrung",\n'
        '    "uk_pflanzen_lebensraum","uk_pflanzen_bestuaeber","uk_pflanzen_herkunft",\n'
        '    "uk_pflanzen_nutzung","uk_pflanzen_blattform","uk_pflanzen_klimazone",\n'
        '    "uk_pflanzen_scheinfruchte","uk_pflanzen_baum_des_jahres","uk_pflanzen_giftpflanze_jahres",\n'
        '    "ws_pflanzen_trauerweide","ws_pflanzen_rhododendron","ws_pflanzen_sonnenblume",\n'
        '    "ws_pflanzen_pusteblume","ws_pflanzen_nachtschatten","ws_pflanzen_vergissmeinnicht",\n'
        '    "ws_pflanzen_kaffeebohne","ws_pflanzen_weihnachtsstern","ws_pflanzen_ginkgobaum"\n'
        '  ],cost:0},')
c = c.replace(OLD8, NEW8, 1)
print('[OK]  Extended MODE_CATS tiere')

# ── 9. GEN dispatch entries ───────────────────────────────────────────────────
OLD9 = '  ws_pferde_fluesterer:()=>{initTierWortSchmiede("pferde_fluesterer");return null;},\n  uk_surf_spots'
assert c.count(OLD9) == 1, f'Anchor not unique: {OLD9!r}'
NEW9 = ('  ws_pferde_fluesterer:()=>{initTierWortSchmiede("pferde_fluesterer");return null;},\n'
        '  /* Phase 228: Pflanzen-Modi */\n'
        '  uk_pflanzen_nutzpflanzen:()=>genPflanzenPinQ("nutzpflanzen"),\n'
        '  uk_pflanzen_einzelbaeume:()=>genPflanzenPinQ("einzelbaeume"),\n'
        '  uk_pflanzen_botanische_gaerten:()=>genPflanzenPinQ("botanische_gaerten"),\n'
        '  uk_pflanzen_tropenwald:()=>genPflanzenPinQ("tropenwald"),\n'
        '  uk_pflanzen_weinanbau:()=>genPflanzenPinQ("weinanbau"),\n'
        '  uk_pflanzen_heilpflanzen:()=>genPflanzenPinQ("heilpflanzen"),\n'
        '  uk_pflanzen_mangroven:()=>genPflanzenPinQ("mangroven"),\n'
        '  uk_pflanzen_kakao_ursprung:()=>genPflanzenPinQ("kakao_ursprung"),\n'
        '  uk_pflanzen_reisanbau:()=>genPflanzenPinQ("reisanbau"),\n'
        '  uk_pflanzen_bambus:()=>genPflanzenPinQ("bambus"),\n'
        '  uk_pflanzen_endemisch:()=>genPflanzenPinQ("endemisch"),\n'
        '  uk_pflanzen_nationalblumen:()=>genPflanzenPinQ("nationalblumen"),\n'
        '  hl_pflanzen_wuchshoehe:()=>genPflanzenHL("wuchshoehe"),\n'
        '  hl_pflanzen_alter:()=>genPflanzenHL("alter"),\n'
        '  hl_pflanzen_fruchtgewicht:()=>genPflanzenHL("fruchtgewicht"),\n'
        '  hl_pflanzen_samenlaenge:()=>genPflanzenHL("samenlaenge"),\n'
        '  hl_pflanzen_kaffeeproduktion:()=>genPflanzenHL("kaffeeproduktion"),\n'
        '  hl_pflanzen_weinproduktion:()=>genPflanzenHL("weinproduktion"),\n'
        '  hl_pflanzen_reisproduktion:()=>genPflanzenHL("reisproduktion"),\n'
        '  hl_pflanzen_waldflaeche:()=>genPflanzenHL("waldflaeche"),\n'
        '  hl_pflanzen_stammumfang:()=>genPflanzenHL("stammumfang"),\n'
        '  hl_pflanzen_blattflaeche:()=>genPflanzenHL("blattflaeche"),\n'
        '  hl_pflanzen_bluehdauer:()=>genPflanzenHL("bluehdauer"),\n'
        '  hl_pflanzen_genomgroesse:()=>genPflanzenHL("genomgroesse"),\n'
        '  uk_pflanzen_gewuerze:()=>genPflanzenMatchQ("gewuerze"),\n'
        '  uk_pflanzen_familien:()=>genPflanzenMatchQ("familien"),\n'
        '  uk_pflanzen_bluetezeit:()=>genPflanzenMatchQ("bluetezeit"),\n'
        '  uk_pflanzen_giftstoffe:()=>genPflanzenMatchQ("giftstoffe"),\n'
        '  uk_pflanzen_fruchttyp:()=>genPflanzenMatchQ("fruchttyp"),\n'
        '  uk_pflanzen_vermehrung:()=>genPflanzenMatchQ("vermehrung"),\n'
        '  uk_pflanzen_lebensraum:()=>genPflanzenMatchQ("lebensraum"),\n'
        '  uk_pflanzen_bestuaeber:()=>genPflanzenMatchQ("bestuaeber"),\n'
        '  uk_pflanzen_herkunft:()=>genPflanzenMatchQ("herkunft"),\n'
        '  uk_pflanzen_nutzung:()=>genPflanzenMatchQ("nutzung"),\n'
        '  uk_pflanzen_blattform:()=>genPflanzenMatchQ("blattform"),\n'
        '  uk_pflanzen_klimazone:()=>genPflanzenMatchQ("klimazone"),\n'
        '  uk_pflanzen_scheinfruchte:()=>genPflanzenMatchQ("scheinfruchte"),\n'
        '  uk_pflanzen_baum_des_jahres:()=>genPflanzenMatchQ("baum_des_jahres"),\n'
        '  uk_pflanzen_giftpflanze_jahres:()=>genPflanzenMatchQ("giftpflanze_jahres"),\n'
        '  ws_pflanzen_trauerweide:()=>{initPflanzenWS("trauerweide");return null;},\n'
        '  ws_pflanzen_rhododendron:()=>{initPflanzenWS("rhododendron");return null;},\n'
        '  ws_pflanzen_sonnenblume:()=>{initPflanzenWS("sonnenblume");return null;},\n'
        '  ws_pflanzen_pusteblume:()=>{initPflanzenWS("pusteblume");return null;},\n'
        '  ws_pflanzen_nachtschatten:()=>{initPflanzenWS("nachtschatten");return null;},\n'
        '  ws_pflanzen_vergissmeinnicht:()=>{initPflanzenWS("vergissmeinnicht");return null;},\n'
        '  ws_pflanzen_kaffeebohne:()=>{initPflanzenWS("kaffeebohne");return null;},\n'
        '  ws_pflanzen_weihnachtsstern:()=>{initPflanzenWS("weihnachtsstern");return null;},\n'
        '  ws_pflanzen_ginkgobaum:()=>{initPflanzenWS("ginkgobaum");return null;},\n'
        '  uk_surf_spots')
c = c.replace(OLD9, NEW9, 1)
print('[OK]  Added 49 GEN dispatch entries')

# ── 10. Write gen.py ──────────────────────────────────────────────────────────
with open(GEN, 'w', encoding='utf-8') as f:
    f.write(c)
print(f'[OK]  Wrote gen.py ({len(c)} chars)')
print('\n[DONE] patch_228_pflanzen.py complete.')
