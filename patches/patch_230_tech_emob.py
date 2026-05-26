# -*- coding: utf-8 -*-
"""
Phase: 230
Date: 2026-05-26
Scope: MEGA-SPRINT Technologie & E-Mobilität — ~90 neue Modi in 2 neuen Kategorien.
       Fügt hinzu: 8 JSON-Ladebloecke, 8 JS-Konstanten, 8 Generatorfunktionen,
       ~90 MODES-Eintraege, 2 MODE_CATS, ~90 GEN-Dispatch-Eintraege, 8 Placeholder-Substitutionen.
"""
import os

GEN = os.path.join(os.path.dirname(__file__), '..', 'gen.py')
with open(GEN, 'r', encoding='utf-8') as f:
    c = f.read()

# ── helper ────────────────────────────────────────────────────────────
def patch(old, new, label):
    assert c.count(old) == 1, f"Anchor not unique ({c.count(old)}x): {label}"
    return c.replace(old, new)

# ══════════════════════════════════════════════════════════════════════
# 1. Python JSON-Lade-Bloecke
# ══════════════════════════════════════════════════════════════════════
OLD1 = "GASTRO_WS_J = _f.read()"
NEW1 = OLD1 + """
with open(os.path.join(os.path.dirname(__file__), 'data/tech_pin.json'), 'r', encoding='utf-8') as _f: TECH_PIN_J = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/tech_hl.json'), 'r', encoding='utf-8') as _f: TECH_HL_J = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/tech_match.json'), 'r', encoding='utf-8') as _f: TECH_MATCH_J = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/tech_ws.json'), 'r', encoding='utf-8') as _f: TECH_WS_J = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/emob_pin.json'), 'r', encoding='utf-8') as _f: EMOB_PIN_J = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/emob_hl.json'), 'r', encoding='utf-8') as _f: EMOB_HL_J = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/emob_match.json'), 'r', encoding='utf-8') as _f: EMOB_MATCH_J = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/emob_ws.json'), 'r', encoding='utf-8') as _f: EMOB_WS_J = _f.read()"""
c = patch(OLD1, NEW1, "gastro_ws load")

# ══════════════════════════════════════════════════════════════════════
# 2. JS const-Deklarationen
# ══════════════════════════════════════════════════════════════════════
OLD2 = "const GASTRO_WS_DATA=PLACEHOLDER_GASTRO_WS;"
NEW2 = OLD2 + """

/* === Phase 230: Tech & E-Mob Datensaetze === */
const TECH_PIN_DATA=PLACEHOLDER_TECH_PIN;
const TECH_HL_DATA=PLACEHOLDER_TECH_HL;
const TECH_MATCH_DATA=PLACEHOLDER_TECH_MATCH;
const TECH_WS_DATA=PLACEHOLDER_TECH_WS;
const EMOB_PIN_DATA=PLACEHOLDER_EMOB_PIN;
const EMOB_HL_DATA=PLACEHOLDER_EMOB_HL;
const EMOB_MATCH_DATA=PLACEHOLDER_EMOB_MATCH;
const EMOB_WS_DATA=PLACEHOLDER_EMOB_WS;"""
c = patch(OLD2, NEW2, "gastro_ws const")

# ══════════════════════════════════════════════════════════════════════
# 3. Generator-Funktionen (vor genGastroPinQ)
# ══════════════════════════════════════════════════════════════════════
OLD3 = "function genGastroPinQ(cat){"
NEW3 = r"""/* === Phase 230: Technologie & E-Mobilitaet Generatoren === */
function genTechPinQ(cat){
  var d=TECH_PIN_DATA[cat];
  if(!d||!d.items||!d.items.length)return null;
  var idx=~~(rng()*d.items.length);
  var item=d.items[idx];
  return {type:"uk_pin",subj:item.n,lat:item.lat,lng:item.lng,
    prompt:d.prompt,cat:cat,itemIdx:idx};
}
function genTechHL(dataKey){
  var d=TECH_HL_DATA[dataKey];
  if(!d||!d.items||d.items.length<2)return null;
  var len=d.items.length;
  var W=Math.max(1,Math.floor(len*0.1));
  var iA,iB;
  do{iA=~~(rng()*len);iB=~~(rng()*len);}while(iA===iB||Math.abs(iA-iB)<W);
  var a=d.items[iA],b=d.items[iB];
  return {type:"hl",a:{name:a.name,val:a.val},b:{name:b.name,val:b.val},
    unit:d.unit,prompt:d.prompt,higherWins:true};
}
function genTechMatchQ(cat){
  var d=TECH_MATCH_DATA[cat];
  if(!d||!d.items||!d.items.length)return null;
  var items=d.items;
  var idx=~~(rng()*items.length);
  var correct=items[idx];
  var opts;
  if(d.fixedOpts){
    opts=d.fixedOpts.slice();
  } else {
    var pool=items.map(function(x){return x.c;}).filter(function(cc){return cc!==correct.c;});
    var seen=new Set();pool=pool.filter(function(cc){if(seen.has(cc))return false;seen.add(cc);return true;});
    while(pool.length<3)pool.push(pool[~~(rng()*pool.length)]||correct.c);
    pool=pool.sort(function(){return rng()-0.5;}).slice(0,3);
    opts=[correct.c].concat(pool).sort(function(){return rng()-0.5;});
  }
  return {type:"uk_match",subj:correct.n,correct:correct.c,opts:opts,
    prompt:d.prompt||"Ordne richtig zu:"};
}
function initTechWS(key){
  clearInterval(tIv);_wsDetachKb();
  var entry=TECH_WS_DATA[key];
  if(!entry||!entry.validWords){console.warn("[GeoQuest] TechWS missing:"+key);S.ph="menu";render();return;}
  var userLang=S.language||localStorage.getItem("gq_lang")||"en";
  var wsLang=_WS_LANGS.has(userLang)?userLang:"en";
  var raw=entry.validWords[wsLang];
  var hasOwn=Array.isArray(raw)&&raw.length>0;
  var actualLang=hasOwn?wsLang:"en";
  var src2=hasOwn?raw:(entry.validWords["en"]||[]);
  var words=src2.map(function(w){return w.toUpperCase();}).filter(function(w){return w.length>=3;});
  if(!words.length){console.warn("[GeoQuest] TechWS no words:"+key);S.ph="menu";render();return;}
  var usingFallback=actualLang!==userLang;
  S.wsData={tierWsKey:key,city:entry.word,lang:actualLang,usingFallback:usingFallback,
    allWords:words,foundWords:[],input:"",phase:"playing",timeLeft:_WS_TIMER,shakeTs:0};
  S.gameStartTime=Date.now();S.ph="playing";
  tIv=setInterval(function(){
    if(!S.wsData||S.wsData.phase!=="playing"){clearInterval(tIv);return;}
    S.wsData.timeLeft=Math.max(0,(S.wsData.timeLeft||0)-1);
    if(S.wsData.timeLeft<=0){S.wsData.phase="timeout";clearInterval(tIv);_wsDetachKb();}
    render();
  },1000);
  _wsAttachKb();
}
function genEmobPinQ(cat){
  var d=EMOB_PIN_DATA[cat];
  if(!d||!d.items||!d.items.length)return null;
  var idx=~~(rng()*d.items.length);
  var item=d.items[idx];
  return {type:"uk_pin",subj:item.n,lat:item.lat,lng:item.lng,
    prompt:d.prompt,cat:cat,itemIdx:idx};
}
function genEmobHL(dataKey){
  var d=EMOB_HL_DATA[dataKey];
  if(!d||!d.items||d.items.length<2)return null;
  var len=d.items.length;
  var W=Math.max(1,Math.floor(len*0.1));
  var iA,iB;
  do{iA=~~(rng()*len);iB=~~(rng()*len);}while(iA===iB||Math.abs(iA-iB)<W);
  var a=d.items[iA],b=d.items[iB];
  return {type:"hl",a:{name:a.name,val:a.val},b:{name:b.name,val:b.val},
    unit:d.unit,prompt:d.prompt,higherWins:true};
}
function genEmobMatchQ(cat){
  var d=EMOB_MATCH_DATA[cat];
  if(!d||!d.items||!d.items.length)return null;
  var items=d.items;
  var idx=~~(rng()*items.length);
  var correct=items[idx];
  var opts;
  if(d.fixedOpts){
    opts=d.fixedOpts.slice();
  } else {
    var pool=items.map(function(x){return x.c;}).filter(function(cc){return cc!==correct.c;});
    var seen=new Set();pool=pool.filter(function(cc){if(seen.has(cc))return false;seen.add(cc);return true;});
    while(pool.length<3)pool.push(pool[~~(rng()*pool.length)]||correct.c);
    pool=pool.sort(function(){return rng()-0.5;}).slice(0,3);
    opts=[correct.c].concat(pool).sort(function(){return rng()-0.5;});
  }
  return {type:"uk_match",subj:correct.n,correct:correct.c,opts:opts,
    prompt:d.prompt||"Ordne richtig zu:"};
}
function initEmobWS(key){
  clearInterval(tIv);_wsDetachKb();
  var entry=EMOB_WS_DATA[key];
  if(!entry||!entry.validWords){console.warn("[GeoQuest] EmobWS missing:"+key);S.ph="menu";render();return;}
  var userLang=S.language||localStorage.getItem("gq_lang")||"en";
  var wsLang=_WS_LANGS.has(userLang)?userLang:"en";
  var raw=entry.validWords[wsLang];
  var hasOwn=Array.isArray(raw)&&raw.length>0;
  var actualLang=hasOwn?wsLang:"en";
  var src2=hasOwn?raw:(entry.validWords["en"]||[]);
  var words=src2.map(function(w){return w.toUpperCase();}).filter(function(w){return w.length>=3;});
  if(!words.length){console.warn("[GeoQuest] EmobWS no words:"+key);S.ph="menu";render();return;}
  var usingFallback=actualLang!==userLang;
  S.wsData={tierWsKey:key,city:entry.word,lang:actualLang,usingFallback:usingFallback,
    allWords:words,foundWords:[],input:"",phase:"playing",timeLeft:_WS_TIMER,shakeTs:0};
  S.gameStartTime=Date.now();S.ph="playing";
  tIv=setInterval(function(){
    if(!S.wsData||S.wsData.phase!=="playing"){clearInterval(tIv);return;}
    S.wsData.timeLeft=Math.max(0,(S.wsData.timeLeft||0)-1);
    if(S.wsData.timeLeft<=0){S.wsData.phase="timeout";clearInterval(tIv);_wsDetachKb();}
    render();
  },1000);
  _wsAttachKb();
}

""" + OLD3
c = patch(OLD3, NEW3, "genGastroPinQ")

# ══════════════════════════════════════════════════════════════════════
# 4. MODES-Eintraege (anchor = unique closing of MODES array)
#    The MODES array ends with the kaltentsafter entry + newline + ];
# ══════════════════════════════════════════════════════════════════════
# Build the anchor by reading the actual string from gen.py
_kalt_id = '{id:"ws_gastro_kaltentsafter"'
_kalt_idx = c.find(_kalt_id)
assert _kalt_idx != -1, "kaltentsafter not found in MODES"
_kalt_end = c.find('\n];', _kalt_idx)
assert _kalt_end != -1, "end of MODES array not found"
OLD4 = c[_kalt_idx : _kalt_end + 3]   # includes the \n]; 
assert c.count(OLD4) == 1, f"MODES anchor not unique ({c.count(OLD4)}x)"

MODES_NEW_ENTRIES = """,
  /* -- Technologie & Robotik: Pin -- */
  {id:"uk_tech_programmiersprachen",icon:"\\u{1F5A5}\\uFE0F",title:"Tech: Programmiersprachen",group:"technologie",prompt:"Wo wurde diese Programmiersprache erfunden?",desc:"Geburtsorte von Python, Java, Rust & Co."},
  {id:"uk_tech_wettbewerbe",icon:"\\u{1F3C6}",title:"Tech: Wettbewerbe",group:"technologie",prompt:"Wo findet dieser Tech-/Robotikwettbewerb statt?",desc:"FIRST Lego League, WRO und mehr"},
  {id:"uk_tech_halbleiter",icon:"\\u{1F52C}",title:"Tech: Halbleiter-Fabs",group:"technologie",prompt:"Wo befindet sich dieses Halbleiterwerk?",desc:"TSMC, Intel, Samsung & Co."},
  {id:"uk_tech_heimcomputer",icon:"\\u{1F4BB}",title:"Tech: Heimcomputer",group:"technologie",prompt:"Wo wurde dieser Heimcomputer entwickelt?",desc:"C64, ZX Spectrum, Amiga & Co."},
  {id:"uk_tech_rechenzentren",icon:"\\u{1F5C4}\\uFE0F",title:"Tech: Rechenzentren",group:"technologie",prompt:"Wo befindet sich dieses Rechenzentrum?",desc:"Google, AWS, Equinix & Co."},
  {id:"uk_tech_pioniere",icon:"\\u{1F468}\\u200D\\u{1F4BB}",title:"Tech: Pioniere",group:"technologie",prompt:"Wo wurde dieser Tech-Pionier geboren?",desc:"Turing, Lovelace, Torvalds & Co."},
  {id:"uk_tech_tech_museen",icon:"\\u{1F3DB}\\uFE0F",title:"Tech: Technologiemuseen",group:"technologie",prompt:"Wo befindet sich dieses Technologiemuseum?",desc:"Computer History Museum, Deutsches Museum & Co."},
  {id:"uk_tech_supercomputer",icon:"\\u26A1",title:"Tech: Supercomputer",group:"technologie",prompt:"Wo steht dieser Supercomputer?",desc:"Frontier, LUMI, Fugaku & Co."},
  /* -- Technologie & Robotik: H/L -- */
  {id:"hl_tech_transistoren",icon:"\\u{1F9EE}",title:"Tech: Transistorenanzahl",group:"technologie",prompt:"Welcher Chip hat mehr Transistoren?",desc:"Apple M2 vs NVIDIA H100"},
  {id:"hl_tech_taktfrequenz",icon:"\\u23F1\\uFE0F",title:"Tech: Taktfrequenz",group:"technologie",prompt:"Welche CPU hat eine hoehere Taktfrequenz?",desc:"GHz-Battle: i9 vs Ryzen vs Apple"},
  {id:"hl_tech_freiheitsgrade",icon:"\\u{1F9BE}",title:"Tech: Freiheitsgrade",group:"technologie",prompt:"Welcher Roboter hat mehr Freiheitsgrade?",desc:"KUKA, ABB, Atlas"},
  {id:"hl_tech_code_zeilen",icon:"\\u{1F4C4}",title:"Tech: Codezeilen",group:"technologie",prompt:"Welches Projekt hat mehr Codezeilen?",desc:"Linux vs Windows vs Google"},
  {id:"hl_tech_release_jahr",icon:"\\u{1F4C5}",title:"Tech: Release-Jahr",group:"technologie",prompt:"Welche Sprache wurde frueher veroeffentlicht?",desc:"Fortran 1957 bis Zig 2016"},
  {id:"hl_tech_rechenleistung",icon:"\\u{1F4CA}",title:"Tech: Rechenleistung",group:"technologie",prompt:"Welche GPU hat mehr Rechenleistung?",desc:"TFLOPS: RTX 4090 vs H100 vs Frontier"},
  {id:"hl_tech_internet_speed",icon:"\\u{1F310}",title:"Tech: Internetgeschwindigkeit",group:"technologie",prompt:"Welches Land hat schnelleres Internet?",desc:"Singapur, Suedkorea, Deutschland"},
  {id:"hl_tech_tdp",icon:"\\u{1F321}\\uFE0F",title:"Tech: TDP-Wert",group:"technologie",prompt:"Welche CPU/GPU hat einen hoeheren TDP?",desc:"Watt: i9 vs NVIDIA H100 vs Arduino"},
  /* -- Technologie & Robotik: Match -- */
  {id:"uk_tech_sensoren",icon:"\\u{1F4E1}",title:"Tech: Sensoren",group:"technologie",prompt:"Was misst dieser Sensor?",desc:"DHT22, PIR, BMP280 zuordnen"},
  {id:"uk_tech_syntax",icon:"\\u{1F4DD}",title:"Tech: Code-Syntax",group:"technologie",prompt:"In welcher Programmiersprache wird das verwendet?",desc:"Pybricks, JavaScript, Java, C++"},
  {id:"uk_tech_linux",icon:"\\u{1F427}",title:"Tech: Linux-Distros",group:"technologie",prompt:"Fuer welchen Einsatz ist diese Distro bekannt?",desc:"Ubuntu, Kali, Alpine, Yocto"},
  {id:"uk_tech_osi",icon:"\\u{1F4E1}",title:"Tech: OSI-Modell",group:"technologie",prompt:"Auf welchem OSI-Layer arbeitet dieses Protokoll?",desc:"HTTP, TCP, IP, Ethernet"},
  {id:"uk_tech_bigo",icon:"\\u{1F4C8}",title:"Tech: Big-O",group:"technologie",prompt:"Welche Big-O-Komplexitaet hat dieser Algorithmus?",desc:"O(1), O(n), O(n\xb2), O(log n)"},
  {id:"uk_tech_http",icon:"\\u{1F4BB}",title:"Tech: HTTP-Statuscodes",group:"technologie",prompt:"Zu welcher Kategorie gehoert dieser HTTP-Code?",desc:"200, 301, 404, 500 einordnen"},
  {id:"uk_tech_wahrheitstabellen",icon:"\\u{1F9EE}",title:"Tech: Logikgatter",group:"technologie",prompt:"Welches Logikgatter erzeugt diesen Ausgang?",desc:"AND, OR, NOT, XOR"},
  {id:"uk_tech_hardware",icon:"\\u{1F4BE}",title:"Tech: Hardware-Komponenten",group:"technologie",prompt:"Zu welchem Computersystem gehoert diese Komponente?",desc:"CPU, RAM, Speicher, Netzwerk"},
  {id:"uk_tech_erfinder",icon:"\\u{1F4A1}",title:"Tech: Technik-Erfinder",group:"technologie",prompt:"Wer hat diese Technologie erfunden?",desc:"WWW, E-Mail, Linux & Co."},
  {id:"uk_tech_portnummern",icon:"\\u{1F50C}",title:"Tech: Portnummern",group:"technologie",prompt:"Welcher Dienst nutzt diese Portnummer?",desc:"80, 443, 22, 3306 & Co."},
  {id:"uk_tech_dateiendungen",icon:"\\u{1F4C1}",title:"Tech: Dateiendungen",group:"technologie",prompt:"Zu welcher Dateiart gehoert diese Endung?",desc:"Bild, Audio, Video, Dokument"},
  {id:"uk_tech_smart_home",icon:"\\u{1F3E0}",title:"Tech: Smart Home",group:"technologie",prompt:"Zu welchem Smart-Home-System gehoert das?",desc:"Home Assistant, Homematic, Shelly, HomeKit"},
  {id:"uk_tech_akronyme",icon:"\\u{1F524}",title:"Tech: Akronyme",group:"technologie",prompt:"Wofuer steht dieses Technik-Akronym?",desc:"API, GPU, DNS, IoT & Co."},
  {id:"uk_tech_turing_award",icon:"\\u{1F3C5}",title:"Tech: Turing Award",group:"technologie",prompt:"Wofuer erhielt diese Person den Turing Award?",desc:"Dijkstra, Knuth, LeCun & Co."},
  {id:"uk_tech_erste_videospiele",icon:"\\u{1F579}\\uFE0F",title:"Tech: Erste Videospiele",group:"technologie",prompt:"In welchem Jahrzehnt erschien dieses Spiel?",desc:"Pong, Pac-Man, Doom & Co."},
  {id:"uk_tech_malware",icon:"\\u{1F9F9}",title:"Tech: Malware-Typen",group:"technologie",prompt:"Zu welcher Malware-Kategorie gehoert das?",desc:"Virus, Wurm, Trojaner, Ransomware"},
  {id:"uk_tech_tech_ma",icon:"\\u{1F4B0}",title:"Tech: Uebernahmen",group:"technologie",prompt:"Von wem wurde dieses Unternehmen uebernommen?",desc:"GitHub, YouTube, WhatsApp & Co."},
  /* -- Technologie & Robotik: WS -- */
  {id:"ws_tech_mikrocontroller",icon:"\\u{1F9F2}",title:"WS: Mikrocontroller",group:"technologie",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus MIKROCONTROLLER!",desc:"Anagramm-R\\u00e4tsel \\u2014 15 Buchstaben"},
  {id:"ws_tech_datenbankmanagement",icon:"\\u{1F5C4}\\uFE0F",title:"WS: Datenbankmanagement",group:"technologie",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus DATENBANKMANAGEMENT!",desc:"Anagramm-R\\u00e4tsel \\u2014 18 Buchstaben"},
  {id:"ws_tech_algorithmus",icon:"\\u{1F4CA}",title:"WS: Algorithmus",group:"technologie",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus ALGORITHMUS!",desc:"Anagramm-R\\u00e4tsel \\u2014 11 Buchstaben"},
  {id:"ws_tech_quantencomputer",icon:"\\u269B\\uFE0F",title:"WS: Quantencomputer",group:"technologie",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus QUANTENCOMPUTER!",desc:"Anagramm-R\\u00e4tsel \\u2014 14 Buchstaben"},
  {id:"ws_tech_prozessorarchitektur",icon:"\\u{1F4BB}",title:"WS: Prozessorarchitektur",group:"technologie",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus PROZESSORARCHITEKTUR!",desc:"Anagramm-R\\u00e4tsel \\u2014 19 Buchstaben"},
  {id:"ws_tech_grafikprozessor",icon:"\\u{1F3AE}",title:"WS: Grafikprozessor",group:"technologie",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus GRAFIKPROZESSOR!",desc:"Anagramm-R\\u00e4tsel \\u2014 15 Buchstaben"},
  {id:"ws_tech_cybersicherheit",icon:"\\u{1F512}",title:"WS: Cybersicherheit",group:"technologie",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus CYBERSICHERHEIT!",desc:"Anagramm-R\\u00e4tsel \\u2014 15 Buchstaben"},
  {id:"ws_tech_softwareentwicklung",icon:"\\u{1F4BB}",title:"WS: Softwareentwicklung",group:"technologie",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus SOFTWAREENTWICKLUNG!",desc:"Anagramm-R\\u00e4tsel \\u2014 18 Buchstaben"},
  {id:"ws_tech_compilerbau",icon:"\\u{1F527}",title:"WS: Compilerbau",group:"technologie",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus COMPILERBAU!",desc:"Anagramm-R\\u00e4tsel \\u2014 11 Buchstaben"},
  {id:"ws_tech_betriebssystem",icon:"\\u{1F4BB}",title:"WS: Betriebssystem",group:"technologie",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus BETRIEBSSYSTEM!",desc:"Anagramm-R\\u00e4tsel \\u2014 14 Buchstaben"},
  /* -- E-Mobilitaet & Infrastruktur: Pin -- */
  {id:"uk_emob_gigafactories",icon:"\\u{1F50B}",title:"E-Mob: Gigafactories",group:"emobilitaet",prompt:"Wo befindet sich diese EV-Gigafactory?",desc:"Tesla, CATL, Northvolt & Co."},
  {id:"uk_emob_ev_startups",icon:"\\u{1F697}",title:"E-Mob: EV-Startups",group:"emobilitaet",prompt:"Wo hat dieses EV-Startup seinen Hauptsitz?",desc:"Rivian, NIO, Polestar & Co."},
  {id:"uk_emob_ladeparks",icon:"\\u26A1",title:"E-Mob: Ladeparks",group:"emobilitaet",prompt:"Wo befindet sich dieser Ladepark?",desc:"Ionity, EnBW, Tesla & Co."},
  {id:"uk_emob_lithium",icon:"\\u26CF\\uFE0F",title:"E-Mob: Lithiumvorkommen",group:"emobilitaet",prompt:"Wo befindet sich dieses Lithiumvorkommen?",desc:"Atacama, Australien, Serbien & Co."},
  {id:"uk_emob_historische_werke",icon:"\\u{1F3ED}",title:"E-Mob: Historische Werke",group:"emobilitaet",prompt:"Wo fand dieser EV-Meilenstein statt?",desc:"EV1, Leaf, ID.3, Lohner-Porsche"},
  {id:"uk_emob_formel_e",icon:"\\u{1F3CE}\\uFE0F",title:"E-Mob: Formel E",group:"emobilitaet",prompt:"In welcher Stadt findet dieser ePrix statt?",desc:"Berlin, Monaco, NYC, Diriyah"},
  {id:"uk_emob_solarparks",icon:"\\u2600\\uFE0F",title:"E-Mob: Solarparks",group:"emobilitaet",prompt:"Wo befindet sich dieser Solarpark?",desc:"Bhadla, Benban, Mohammed bin Rashid"},
  {id:"uk_emob_autonom_tests",icon:"\\u{1F916}",title:"E-Mob: Autonome Tests",group:"emobilitaet",prompt:"Wo werden autonome Fahrzeuge getestet?",desc:"Waymo, MCity, A9, AstaZero"},
  {id:"uk_emob_batterie_forschung",icon:"\\u{1F9EA}",title:"E-Mob: Batterieforschung",group:"emobilitaet",prompt:"Wo befindet sich dieses Batterie-Institut?",desc:"Argonne, Fraunhofer, MEET & Co."},
  {id:"uk_emob_ev_dichte_staedte",icon:"\\u{1F3D9}\\uFE0F",title:"E-Mob: EV-Dichte-Staedte",group:"emobilitaet",prompt:"Diese Stadt hat eine der hoechsten EV-Dichten — wo liegt sie?",desc:"Oslo, Shenzhen, Amsterdam & Co."},
  {id:"uk_emob_recycling",icon:"\\u267B\\uFE0F",title:"E-Mob: Batterie-Recycling",group:"emobilitaet",prompt:"Wo befindet sich diese Recyclinganlage?",desc:"Redwood Materials, VW Salzgitter & Co."},
  {id:"uk_emob_erste_evs",icon:"\\u{1F4DC}",title:"E-Mob: Erste EVs",group:"emobilitaet",prompt:"Wo fand dieser Meilenstein der fruehen E-Mobilitaet statt?",desc:"La Jamais Contente, Detroit Electric & Co."},
  {id:"uk_emob_roadtrips",icon:"\\u{1F5FA}\\uFE0F",title:"E-Mob: EV-Roadtrips",group:"emobilitaet",prompt:"Welcher EV-Ladekorridor fuehrt durch diesen Ort?",desc:"Route 66, Brenner, E6 Skandinavien"},
  /* -- E-Mobilitaet: H/L -- */
  {id:"hl_emob_kapazitaet",icon:"\\u{1F50B}",title:"E-Mob: Batteriekapazitaet",group:"emobilitaet",prompt:"Welches EV hat eine groessere Batteriekapazitaet?",desc:"kWh: iX3, Mach-E, EQS & Co."},
  {id:"hl_emob_ladeleistung",icon:"\\u26A1",title:"E-Mob: Ladeleistung",group:"emobilitaet",prompt:"Welches EV laedt mit hoeherer Maximalleistung?",desc:"kW DC: Taycan 270 vs Dacia 30"},
  {id:"hl_emob_wltp",icon:"\\u{1F6E3}\\uFE0F",title:"E-Mob: WLTP-Reichweite",group:"emobilitaet",prompt:"Welches EV hat eine groessere WLTP-Reichweite?",desc:"Lucid Air 836 km vs Dacia 225 km"},
  {id:"hl_emob_0_100",icon:"\\u{1F3CE}\\uFE0F",title:"E-Mob: 0–100 km/h",group:"emobilitaet",prompt:"Welches EV beschleunigt schneller auf 100?",desc:"Rimac 1,97s vs Dacia Spring 19s"},
  {id:"hl_emob_gewicht",icon:"\\u2696\\uFE0F",title:"E-Mob: Fahrzeuggewicht",group:"emobilitaet",prompt:"Welches EV ist schwerer?",desc:"Hummer EV 4111 kg vs Smart EQ 975 kg"},
  {id:"hl_emob_ladezeit_10_80",icon:"\\u23F1\\uFE0F",title:"E-Mob: Ladezeit 10–80%",group:"emobilitaet",prompt:"Bei welchem EV dauert das Laden von 10–80% kuerzer?",desc:"Ioniq 6 18 min vs Smart EQ 160 min"},
  {id:"hl_emob_cw_wert",icon:"\\u{1F4A8}",title:"E-Mob: cw-Wert",group:"emobilitaet",prompt:"Welches Fahrzeug hat einen niedrigeren Luftwiderstand?",desc:"EQS 0,20 vs Hummer 0,42"},
  {id:"hl_emob_systemspannung",icon:"\\u{1F50C}",title:"E-Mob: Systemspannung",group:"emobilitaet",prompt:"Welches EV arbeitet mit hoeherer Systemspannung?",desc:"Lucid Air 900V vs Dacia 48V"},
  {id:"hl_emob_ladeanschluesse",icon:"\\u{1F50C}",title:"E-Mob: Ladeanschluesse",group:"emobilitaet",prompt:"Welches EV hat mehr Ladeanschluesse?",desc:"CHAdeMO + CCS + Swap vs nur Typ2"},
  {id:"hl_emob_drehmoment",icon:"\\u{1F527}",title:"E-Mob: Drehmoment",group:"emobilitaet",prompt:"Welches EV hat mehr Systemdrehmoment?",desc:"Hummer EV 15592 Nm vs Dacia 125 Nm"},
  {id:"hl_emob_preis",icon:"\\u{1F4B0}",title:"E-Mob: Basispreis",group:"emobilitaet",prompt:"Welches EV ist teurer?",desc:"Rimac Nevera 2,4 Mio EUR vs Dacia 17T"},
  {id:"hl_emob_zell_anzahl",icon:"\\u{1F9EE}",title:"E-Mob: Zellenanzahl",group:"emobilitaet",prompt:"Welches EV hat mehr Batteriezellen?",desc:"Tesla Model S 8256 vs Dacia 30"},
  /* -- E-Mobilitaet: Match -- */
  {id:"uk_emob_stecker",icon:"\\u{1F50C}",title:"E-Mob: Ladestecker",group:"emobilitaet",prompt:"Welchem Ladestandard entspricht dieser Stecker?",desc:"CCS, CHAdeMO, Typ2, Tesla"},
  {id:"uk_emob_plattformen",icon:"\\u{1F697}",title:"E-Mob: EV-Plattformen",group:"emobilitaet",prompt:"Auf welcher Plattform basiert dieses EV-Modell?",desc:"MEB, E-GMP, J1, CLAR & Co."},
  {id:"uk_emob_zellchemie",icon:"\\u{1F9EA}",title:"E-Mob: Zellchemie",group:"emobilitaet",prompt:"Welcher Vorteil ist typisch fuer diese Batteriechemie?",desc:"NMC, LFP, NCA, Solid-State"},
  {id:"uk_emob_akronyme",icon:"\\u{1F524}",title:"E-Mob: Akronyme",group:"emobilitaet",prompt:"Wofuer steht dieses E-Mobilitaets-Akronym?",desc:"BEV, WLTP, SOC, V2G & Co."},
  {id:"uk_emob_level_autonomy",icon:"\\u{1F916}",title:"E-Mob: Autonomiegrade",group:"emobilitaet",prompt:"Welchem SAE-Autonomiegrad entspricht diese Funktion?",desc:"Level 1–5: Tempomat bis Robotaxi"},
  {id:"uk_emob_motorentypen",icon:"\\u26A1",title:"E-Mob: Motorentypen",group:"emobilitaet",prompt:"Auf welcher Technologie basiert dieser Elektromotor?",desc:"PMSM, Induktion, Reluktanz, DC"},
  {id:"uk_emob_thermomanagement",icon:"\\u{1F321}\\uFE0F",title:"E-Mob: Thermomanagement",group:"emobilitaet",prompt:"Welche Funktion uebernimmt diese TMS-Komponente?",desc:"Kuehlen, Heizen, Isolieren, Regeln"},
  {id:"uk_emob_bidirektional",icon:"\\u{1F501}",title:"E-Mob: V2X-Technologie",group:"emobilitaet",prompt:"Welche V2X-Technologie beschreibt diese Interaktion?",desc:"V2H, V2G, V2L, V2V"},
  {id:"uk_emob_ladekurven",icon:"\\u{1F4CA}",title:"E-Mob: Ladekurven",group:"emobilitaet",prompt:"Welches Fahrzeug zeigt dieses Ladeverhalten?",desc:"Taycan, Ioniq 6, Dacia Spring & Co."},
  {id:"uk_emob_smart_home",icon:"\\u{1F3E0}",title:"E-Mob: EV & Smart Home",group:"emobilitaet",prompt:"Welches Protokoll ermoeglicht diese EV-Smart-Home-Funktion?",desc:"OCPP, ISO 15118, EEBus, OpenADR"},
  {id:"uk_emob_privilegien",icon:"\\u{1F4CB}",title:"E-Mob: EV-Privilegien",group:"emobilitaet",prompt:"In welchem Land gilt dieses EV-Privileg?",desc:"Norwegen, USA, Deutschland & Co."},
  {id:"uk_emob_port_position",icon:"\\u{1F50C}",title:"E-Mob: Ladeanschluss-Position",group:"emobilitaet",prompt:"Wo sitzt der Ladeanschluss bei diesem Fahrzeug?",desc:"iX3 hinten links, Mach-E vorne links"},
  {id:"uk_emob_ev_reifen",icon:"\\u{1F6DE}",title:"E-Mob: EV-Reifen",group:"emobilitaet",prompt:"Welchen Vorteil bietet dieses EV-Reifenmerkmal?",desc:"Geraeusch, Gewicht, Reichweite, Grip"},
  {id:"uk_emob_roaming",icon:"\\u{1F310}",title:"E-Mob: Lade-Roaming",group:"emobilitaet",prompt:"Mit welchem Partner kann dieses Ladenetzwerk roamen?",desc:"Ionity, EnBW, ChargePoint & OCPI"},
  {id:"uk_emob_warnleuchten",icon:"\\u{1F6A8}",title:"E-Mob: Warnleuchten",group:"emobilitaet",prompt:"Was bedeutet diese EV-Warnanzeige?",desc:"Batterie, Schildkroete, Thermometer & Co."},
  {id:"uk_emob_startups_match",icon:"\\u{1F30D}",title:"E-Mob: Startup-Laender",group:"emobilitaet",prompt:"Aus welchem Land stammt dieses EV-Startup?",desc:"Rivian, NIO, Rimac & Co."},
  {id:"uk_emob_reichweiten_killer",icon:"\\u{1F4C9}",title:"E-Mob: Reichweiten-Killer",group:"emobilitaet",prompt:"Welcher Faktor reduziert die EV-Reichweite hier?",desc:"Kaelte, Autobahn, Klima, Gewicht"},
  {id:"uk_emob_avas",icon:"\\u{1F50A}",title:"E-Mob: AVAS-Vorschriften",group:"emobilitaet",prompt:"Was schreibt die AVAS-Vorschrift hier vor?",desc:"Pflichtgeraeusch unter 20 km/h"},
  {id:"uk_emob_subventionen",icon:"\\u{1F4B6}",title:"E-Mob: Subventionen",group:"emobilitaet",prompt:"In welchem Land gilt diese EV-Foerderung?",desc:"Umweltbonus, IRA, Bonus Ecologique"},
  {id:"uk_emob_etikette",icon:"\\u{1F91D}",title:"E-Mob: Ladetikette",group:"emobilitaet",prompt:"Welche Verhaltensregel passt zu dieser Ladesituation?",desc:"Kabel wegraeuumen, nicht blockieren & Co."},
  {id:"uk_emob_konzeptautos",icon:"\\u{1F3CE}\\uFE0F",title:"E-Mob: Konzeptfahrzeuge",group:"emobilitaet",prompt:"Von welchem Hersteller stammt dieses EV-Konzept?",desc:"Vision EQXX, i Vision Dee & Co."},
  {id:"uk_emob_strommix",icon:"\\u{1F4A1}",title:"E-Mob: Strommix",group:"emobilitaet",prompt:"In welche EE-Anteil-Kategorie faellt dieses Land?",desc:"Norwegen >80%, Polen <30%"},
  /* -- E-Mobilitaet: WS -- */
  {id:"ws_emob_schnellladestation",icon:"\\u26A1",title:"WS: Schnellladestation",group:"emobilitaet",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus SCHNELLLADESTATION!",desc:"Anagramm-R\\u00e4tsel \\u2014 18 Buchstaben"},
  {id:"ws_emob_rekuperation",icon:"\\u{1F501}",title:"WS: Rekuperation",group:"emobilitaet",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus REKUPERATION!",desc:"Anagramm-R\\u00e4tsel \\u2014 12 Buchstaben"},
  {id:"ws_emob_reichweitenangst",icon:"\\u{1F628}",title:"WS: Reichweitenangst",group:"emobilitaet",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus REICHWEITENANGST!",desc:"Anagramm-R\\u00e4tsel \\u2014 16 Buchstaben"},
  {id:"ws_emob_fahrassistenzsystem",icon:"\\u{1F916}",title:"WS: Fahrassistenzsystem",group:"emobilitaet",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus FAHRASSISTENZSYSTEM!",desc:"Anagramm-R\\u00e4tsel \\u2014 18 Buchstaben"},
  {id:"ws_emob_bordnetzspannung",icon:"\\u{1F50C}",title:"WS: Bordnetzspannung",group:"emobilitaet",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus BORDNETZSPANNUNG!",desc:"Anagramm-R\\u00e4tsel \\u2014 15 Buchstaben"},
  {id:"ws_emob_elektroantrieb",icon:"\\u{1F697}",title:"WS: Elektroantrieb",group:"emobilitaet",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus ELEKTROANTRIEB!",desc:"Anagramm-R\\u00e4tsel \\u2014 14 Buchstaben"},
  {id:"ws_emob_wechselstromladen",icon:"\\u{1F4A1}",title:"WS: Wechselstromladen",group:"emobilitaet",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus WECHSELSTROMLADEN!",desc:"Anagramm-R\\u00e4tsel \\u2014 17 Buchstaben"},
  {id:"ws_emob_gleichstromladen",icon:"\\u26A1",title:"WS: Gleichstromladen",group:"emobilitaet",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus GLEICHSTROMLADEN!",desc:"Anagramm-R\\u00e4tsel \\u2014 16 Buchstaben"},
  {id:"ws_emob_batteriemanagement",icon:"\\u{1F50B}",title:"WS: Batteriemanagement",group:"emobilitaet",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus BATTERIEMANAGEMENT!",desc:"Anagramm-R\\u00e4tsel \\u2014 18 Buchstaben"},
  {id:"ws_emob_bidirektionalladen",icon:"\\u{1F501}",title:"WS: Bidirektionalladen",group:"emobilitaet",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus BIDIREKTIONALLADEN!",desc:"Anagramm-R\\u00e4tsel \\u2014 18 Buchstaben"}"""

# Replace only the trailing }  with }  + new entries + \n];
_kalt_obj_end = OLD4.rfind('}')       # last } before \n];
OLD4_TRIMMED = OLD4[:_kalt_obj_end+1] # just the object, no \n];
assert c.count(OLD4_TRIMMED + '\n];') == 1
NEW4 = OLD4_TRIMMED + MODES_NEW_ENTRIES + '\n];'
c = c.replace(OLD4_TRIMMED + '\n];', NEW4)
assert c.count(OLD4_TRIMMED + '\n];') == 0  # replaced
print("MODES entries: OK")

# ══════════════════════════════════════════════════════════════════════
# 5. MODE_CATS
# ══════════════════════════════════════════════════════════════════════
OLD5 = '"ws_gastro_kaltentsafter"\n  ],cost:0},\n};'
NEW5 = '''"ws_gastro_kaltentsafter"
  ],cost:0},
  technologie:{label:"Technologie & Robotik",icon:"\\u{1F4BB}",modes:[
    "uk_tech_programmiersprachen","uk_tech_wettbewerbe","uk_tech_halbleiter","uk_tech_heimcomputer",
    "uk_tech_rechenzentren","uk_tech_pioniere","uk_tech_tech_museen","uk_tech_supercomputer",
    "hl_tech_transistoren","hl_tech_taktfrequenz","hl_tech_freiheitsgrade","hl_tech_code_zeilen",
    "hl_tech_release_jahr","hl_tech_rechenleistung","hl_tech_internet_speed","hl_tech_tdp",
    "uk_tech_sensoren","uk_tech_syntax","uk_tech_linux","uk_tech_osi","uk_tech_bigo","uk_tech_http",
    "uk_tech_wahrheitstabellen","uk_tech_hardware","uk_tech_erfinder","uk_tech_portnummern",
    "uk_tech_dateiendungen","uk_tech_smart_home","uk_tech_akronyme","uk_tech_turing_award",
    "uk_tech_erste_videospiele","uk_tech_malware","uk_tech_tech_ma",
    "ws_tech_mikrocontroller","ws_tech_datenbankmanagement","ws_tech_algorithmus",
    "ws_tech_quantencomputer","ws_tech_prozessorarchitektur","ws_tech_grafikprozessor",
    "ws_tech_cybersicherheit","ws_tech_softwareentwicklung","ws_tech_compilerbau","ws_tech_betriebssystem"
  ],cost:0},
  emobilitaet:{label:"E-Mobilit\\u00e4t & Infrastruktur",icon:"\\u26A1",modes:[
    "uk_emob_gigafactories","uk_emob_ev_startups","uk_emob_ladeparks","uk_emob_lithium",
    "uk_emob_historische_werke","uk_emob_formel_e","uk_emob_solarparks","uk_emob_autonom_tests",
    "uk_emob_batterie_forschung","uk_emob_ev_dichte_staedte","uk_emob_recycling",
    "uk_emob_erste_evs","uk_emob_roadtrips",
    "hl_emob_kapazitaet","hl_emob_ladeleistung","hl_emob_wltp","hl_emob_0_100",
    "hl_emob_gewicht","hl_emob_ladezeit_10_80","hl_emob_cw_wert","hl_emob_systemspannung",
    "hl_emob_ladeanschluesse","hl_emob_drehmoment","hl_emob_preis","hl_emob_zell_anzahl",
    "uk_emob_stecker","uk_emob_plattformen","uk_emob_zellchemie","uk_emob_akronyme",
    "uk_emob_level_autonomy","uk_emob_motorentypen","uk_emob_thermomanagement",
    "uk_emob_bidirektional","uk_emob_ladekurven","uk_emob_smart_home","uk_emob_privilegien",
    "uk_emob_port_position","uk_emob_ev_reifen","uk_emob_roaming","uk_emob_warnleuchten",
    "uk_emob_startups_match","uk_emob_reichweiten_killer","uk_emob_avas","uk_emob_subventionen",
    "uk_emob_etikette","uk_emob_konzeptautos","uk_emob_strommix",
    "ws_emob_schnellladestation","ws_emob_rekuperation","ws_emob_reichweitenangst",
    "ws_emob_fahrassistenzsystem","ws_emob_bordnetzspannung","ws_emob_elektroantrieb",
    "ws_emob_wechselstromladen","ws_emob_gleichstromladen","ws_emob_batteriemanagement",
    "ws_emob_bidirektionalladen"
  ],cost:0},
};'''
c = patch(OLD5, NEW5, "MODE_CATS")

# ══════════════════════════════════════════════════════════════════════
# 6. GEN dispatch
# ══════════════════════════════════════════════════════════════════════
OLD6 = 'ws_gastro_kaltentsafter:()=>{initGastroWS("kaltentsafter");return null;},'
NEW6 = OLD6 + """
  /* === Phase 230: Technologie Dispatch === */
  uk_tech_programmiersprachen:()=>genTechPinQ("programmiersprachen"),
  uk_tech_wettbewerbe:()=>genTechPinQ("wettbewerbe"),
  uk_tech_halbleiter:()=>genTechPinQ("halbleiter"),
  uk_tech_heimcomputer:()=>genTechPinQ("heimcomputer"),
  uk_tech_rechenzentren:()=>genTechPinQ("rechenzentren"),
  uk_tech_pioniere:()=>genTechPinQ("pioniere"),
  uk_tech_tech_museen:()=>genTechPinQ("tech_museen"),
  uk_tech_supercomputer:()=>genTechPinQ("supercomputer"),
  hl_tech_transistoren:()=>genTechHL("transistoren"),
  hl_tech_taktfrequenz:()=>genTechHL("taktfrequenz"),
  hl_tech_freiheitsgrade:()=>genTechHL("freiheitsgrade"),
  hl_tech_code_zeilen:()=>genTechHL("code_zeilen"),
  hl_tech_release_jahr:()=>genTechHL("release_jahr"),
  hl_tech_rechenleistung:()=>genTechHL("rechenleistung"),
  hl_tech_internet_speed:()=>genTechHL("internet_speed"),
  hl_tech_tdp:()=>genTechHL("tdp"),
  uk_tech_sensoren:()=>genTechMatchQ("sensoren"),
  uk_tech_syntax:()=>genTechMatchQ("syntax"),
  uk_tech_linux:()=>genTechMatchQ("linux"),
  uk_tech_osi:()=>genTechMatchQ("osi"),
  uk_tech_bigo:()=>genTechMatchQ("bigo"),
  uk_tech_http:()=>genTechMatchQ("http"),
  uk_tech_wahrheitstabellen:()=>genTechMatchQ("wahrheitstabellen"),
  uk_tech_hardware:()=>genTechMatchQ("hardware"),
  uk_tech_erfinder:()=>genTechMatchQ("erfinder"),
  uk_tech_portnummern:()=>genTechMatchQ("portnummern"),
  uk_tech_dateiendungen:()=>genTechMatchQ("dateiendungen"),
  uk_tech_smart_home:()=>genTechMatchQ("smart_home"),
  uk_tech_akronyme:()=>genTechMatchQ("akronyme"),
  uk_tech_turing_award:()=>genTechMatchQ("turing_award"),
  uk_tech_erste_videospiele:()=>genTechMatchQ("erste_videospiele"),
  uk_tech_malware:()=>genTechMatchQ("malware"),
  uk_tech_tech_ma:()=>genTechMatchQ("tech_ma"),
  ws_tech_mikrocontroller:()=>{initTechWS("mikrocontroller");return null;},
  ws_tech_datenbankmanagement:()=>{initTechWS("datenbankmanagement");return null;},
  ws_tech_algorithmus:()=>{initTechWS("algorithmus");return null;},
  ws_tech_quantencomputer:()=>{initTechWS("quantencomputer");return null;},
  ws_tech_prozessorarchitektur:()=>{initTechWS("prozessorarchitektur");return null;},
  ws_tech_grafikprozessor:()=>{initTechWS("grafikprozessor");return null;},
  ws_tech_cybersicherheit:()=>{initTechWS("cybersicherheit");return null;},
  ws_tech_softwareentwicklung:()=>{initTechWS("softwareentwicklung");return null;},
  ws_tech_compilerbau:()=>{initTechWS("compilerbau");return null;},
  ws_tech_betriebssystem:()=>{initTechWS("betriebssystem");return null;},
  /* === Phase 230: E-Mobilitaet Dispatch === */
  uk_emob_gigafactories:()=>genEmobPinQ("gigafactories"),
  uk_emob_ev_startups:()=>genEmobPinQ("ev_startups"),
  uk_emob_ladeparks:()=>genEmobPinQ("ladeparks"),
  uk_emob_lithium:()=>genEmobPinQ("lithium"),
  uk_emob_historische_werke:()=>genEmobPinQ("historische_werke"),
  uk_emob_formel_e:()=>genEmobPinQ("formel_e"),
  uk_emob_solarparks:()=>genEmobPinQ("solarparks"),
  uk_emob_autonom_tests:()=>genEmobPinQ("autonom_tests"),
  uk_emob_batterie_forschung:()=>genEmobPinQ("batterie_forschung"),
  uk_emob_ev_dichte_staedte:()=>genEmobPinQ("ev_dichte_staedte"),
  uk_emob_recycling:()=>genEmobPinQ("recycling"),
  uk_emob_erste_evs:()=>genEmobPinQ("erste_evs"),
  uk_emob_roadtrips:()=>genEmobPinQ("roadtrips"),
  hl_emob_kapazitaet:()=>genEmobHL("kapazitaet"),
  hl_emob_ladeleistung:()=>genEmobHL("ladeleistung"),
  hl_emob_wltp:()=>genEmobHL("wltp"),
  hl_emob_0_100:()=>genEmobHL("0_100"),
  hl_emob_gewicht:()=>genEmobHL("gewicht"),
  hl_emob_ladezeit_10_80:()=>genEmobHL("ladezeit_10_80"),
  hl_emob_cw_wert:()=>genEmobHL("cw_wert"),
  hl_emob_systemspannung:()=>genEmobHL("systemspannung"),
  hl_emob_ladeanschluesse:()=>genEmobHL("ladeanschluesse"),
  hl_emob_drehmoment:()=>genEmobHL("drehmoment"),
  hl_emob_preis:()=>genEmobHL("preis"),
  hl_emob_zell_anzahl:()=>genEmobHL("zell_anzahl"),
  uk_emob_stecker:()=>genEmobMatchQ("stecker"),
  uk_emob_plattformen:()=>genEmobMatchQ("plattformen"),
  uk_emob_zellchemie:()=>genEmobMatchQ("zellchemie"),
  uk_emob_akronyme:()=>genEmobMatchQ("akronyme"),
  uk_emob_level_autonomy:()=>genEmobMatchQ("level_autonomy"),
  uk_emob_motorentypen:()=>genEmobMatchQ("motorentypen"),
  uk_emob_thermomanagement:()=>genEmobMatchQ("thermomanagement"),
  uk_emob_bidirektional:()=>genEmobMatchQ("bidirektional"),
  uk_emob_ladekurven:()=>genEmobMatchQ("ladekurven"),
  uk_emob_smart_home:()=>genEmobMatchQ("smart_home"),
  uk_emob_privilegien:()=>genEmobMatchQ("privilegien"),
  uk_emob_port_position:()=>genEmobMatchQ("port_position"),
  uk_emob_ev_reifen:()=>genEmobMatchQ("ev_reifen"),
  uk_emob_roaming:()=>genEmobMatchQ("roaming"),
  uk_emob_warnleuchten:()=>genEmobMatchQ("warnleuchten"),
  uk_emob_startups_match:()=>genEmobMatchQ("startups_match"),
  uk_emob_reichweiten_killer:()=>genEmobMatchQ("reichweiten_killer"),
  uk_emob_avas:()=>genEmobMatchQ("avas"),
  uk_emob_subventionen:()=>genEmobMatchQ("subventionen"),
  uk_emob_etikette:()=>genEmobMatchQ("etikette"),
  uk_emob_konzeptautos:()=>genEmobMatchQ("konzeptautos"),
  uk_emob_strommix:()=>genEmobMatchQ("strommix"),
  ws_emob_schnellladestation:()=>{initEmobWS("schnellladestation");return null;},
  ws_emob_rekuperation:()=>{initEmobWS("rekuperation");return null;},
  ws_emob_reichweitenangst:()=>{initEmobWS("reichweitenangst");return null;},
  ws_emob_fahrassistenzsystem:()=>{initEmobWS("fahrassistenzsystem");return null;},
  ws_emob_bordnetzspannung:()=>{initEmobWS("bordnetzspannung");return null;},
  ws_emob_elektroantrieb:()=>{initEmobWS("elektroantrieb");return null;},
  ws_emob_wechselstromladen:()=>{initEmobWS("wechselstromladen");return null;},
  ws_emob_gleichstromladen:()=>{initEmobWS("gleichstromladen");return null;},
  ws_emob_batteriemanagement:()=>{initEmobWS("batteriemanagement");return null;},
  ws_emob_bidirektionalladen:()=>{initEmobWS("bidirektionalladen");return null;},"""
c = patch(OLD6, NEW6, "GEN dispatch kaltentsafter")

# ══════════════════════════════════════════════════════════════════════
# 7. Placeholder-Substitutionen im Build-Block
# ══════════════════════════════════════════════════════════════════════
OLD7 = "  .replace('PLACEHOLDER_GASTRO_WS', GASTRO_WS_J)\n)"
NEW7 = """  .replace('PLACEHOLDER_GASTRO_WS', GASTRO_WS_J)
  .replace('PLACEHOLDER_TECH_PIN', TECH_PIN_J)
  .replace('PLACEHOLDER_TECH_HL', TECH_HL_J)
  .replace('PLACEHOLDER_TECH_MATCH', TECH_MATCH_J)
  .replace('PLACEHOLDER_TECH_WS', TECH_WS_J)
  .replace('PLACEHOLDER_EMOB_PIN', EMOB_PIN_J)
  .replace('PLACEHOLDER_EMOB_HL', EMOB_HL_J)
  .replace('PLACEHOLDER_EMOB_MATCH', EMOB_MATCH_J)
  .replace('PLACEHOLDER_EMOB_WS', EMOB_WS_J)
)"""
c = patch(OLD7, NEW7, "placeholder chain")

# ══════════════════════════════════════════════════════════════════════
# Write
# ══════════════════════════════════════════════════════════════════════
with open(GEN, 'w', encoding='utf-8') as f:
    f.write(c)
print("patch_230_tech_emob.py applied successfully.")
