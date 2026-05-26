"""
Phase 231: Archäologie & Verlorene Welten
60 new modes, new MODE_CAT archaeologie
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GEN  = os.path.join(ROOT, 'gen.py')

with open(GEN, 'r', encoding='utf-8') as f:
    c = f.read()

# ─── STEP 1: Python file loaders ─────────────────────────────────────────────
OLD1 = "with open(os.path.join(os.path.dirname(__file__), 'data/emob_ws.json'), 'r', encoding='utf-8') as _f: EMOB_WS_J = _f.read()"
assert c.count(OLD1) == 1, f"STEP1 anchor not found or not unique: {c.count(OLD1)}"
NEW1 = OLD1 + """
with open(os.path.join(os.path.dirname(__file__), 'data/archaeologie_pin.json'), 'r', encoding='utf-8') as _f: ARCH_PIN_J = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/archaeologie_hl.json'), 'r', encoding='utf-8') as _f: ARCH_HL_J = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/archaeologie_match.json'), 'r', encoding='utf-8') as _f: ARCH_MATCH_J = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/archaeologie_ws.json'), 'r', encoding='utf-8') as _f: ARCH_WS_J = _f.read()"""
c = c.replace(OLD1, NEW1)

# ─── STEP 2: Placeholder chain ────────────────────────────────────────────────
OLD2 = "  .replace('PLACEHOLDER_EMOB_WS', EMOB_WS_J)\n)"
assert c.count(OLD2) == 1, f"STEP2 anchor not found or not unique: {c.count(OLD2)}"
NEW2 = """  .replace('PLACEHOLDER_EMOB_WS', EMOB_WS_J)
  .replace('PLACEHOLDER_ARCH_PIN', ARCH_PIN_J)
  .replace('PLACEHOLDER_ARCH_HL', ARCH_HL_J)
  .replace('PLACEHOLDER_ARCH_MATCH', ARCH_MATCH_J)
  .replace('PLACEHOLDER_ARCH_WS', ARCH_WS_J)
)"""
c = c.replace(OLD2, NEW2)

# ─── STEP 3: JS const declarations ────────────────────────────────────────────
OLD3 = "const EMOB_WS_DATA=PLACEHOLDER_EMOB_WS;"
assert c.count(OLD3) == 1, f"STEP3 anchor not found or not unique: {c.count(OLD3)}"
NEW3 = """const EMOB_WS_DATA=PLACEHOLDER_EMOB_WS;

/* === Phase 231: Archaeologie-Datensaetze === */
const ARCH_PIN_DATA=PLACEHOLDER_ARCH_PIN;
const ARCH_HL_DATA=PLACEHOLDER_ARCH_HL;
const ARCH_MATCH_DATA=PLACEHOLDER_ARCH_MATCH;
const ARCH_WS_DATA=PLACEHOLDER_ARCH_WS;"""
c = c.replace(OLD3, NEW3)

# ─── STEP 4: Generator functions ──────────────────────────────────────────────
OLD4 = "/* === Phase 228: Pflanzen-Generatoren === */\nfunction genPflanzenPinQ(cat){"
assert c.count(OLD4) == 1, f"STEP4 anchor not found or not unique: {c.count(OLD4)}"
NEW4 = """/* === Phase 231: Archaeologie-Generatoren === */
function genArchPinQ(cat){
  var d=ARCH_PIN_DATA[cat];
  if(!d||!d.items||!d.items.length)return null;
  var idx=~~(rng()*d.items.length);
  var item=d.items[idx];
  return {type:"uk_pin",subj:item.n,lat:item.lat,lng:item.lng,
    prompt:d.prompt,cat:cat,itemIdx:idx};
}
function genArchHL(dataKey){
  var d=ARCH_HL_DATA[dataKey];
  if(!d||!d.items||d.items.length<2)return null;
  var len=d.items.length;
  var W=Math.max(1,Math.floor(len*0.1));
  var iA,iB;
  do{iA=~~(rng()*len);iB=~~(rng()*len);}while(iA===iB||Math.abs(iA-iB)<W);
  var a=d.items[iA],b=d.items[iB];
  return {type:"hl",a:{name:a.name,val:a.val},b:{name:b.name,val:b.val},
    unit:d.unit,prompt:d.prompt,higherWins:true};
}
function genArchMatchQ(cat){
  var d=ARCH_MATCH_DATA[cat];
  if(!d||!d.items||!d.items.length)return null;
  var items=d.items;
  var idx=~~(rng()*items.length);
  var correct=items[idx];
  var opts;
  if(d.fixedOpts){
    opts=d.fixedOpts.slice();
  } else {
    var pool=items.map(function(x){return x.c;}).filter(function(c){return c!==correct.c;});
    var seen=new Set();pool=pool.filter(function(c){if(seen.has(c))return false;seen.add(c);return true;});
    while(pool.length<3)pool.push(pool[~~(rng()*pool.length)]||correct.c);
    pool=pool.sort(function(){return rng()-0.5;}).slice(0,3);
    opts=[correct.c].concat(pool).sort(function(){return rng()-0.5;});
  }
  return {type:"uk_match",subj:correct.n,correct:correct.c,opts:opts,
    prompt:d.prompt||"Ordne richtig zu:"};
}
function initArchWS(key){
  clearInterval(tIv);_wsDetachKb();
  var entry=ARCH_WS_DATA[key];
  if(!entry||!entry.validWords){console.warn("[GeoQuest] ArchWS missing:"+key);S.ph="menu";render();return;}
  var userLang=S.language||localStorage.getItem("gq_lang")||"en";
  var wsLang=_WS_LANGS.has(userLang)?userLang:"en";
  var raw=entry.validWords[wsLang];
  var hasOwn=Array.isArray(raw)&&raw.length>0;
  var actualLang=hasOwn?wsLang:"en";
  var src2=hasOwn?raw:(entry.validWords["en"]||[]);
  var words=src2.map(function(w){return w.toUpperCase();}).filter(function(w){return w.length>=3;});
  if(!words.length){console.warn("[GeoQuest] ArchWS no words:"+key);S.ph="menu";render();return;}
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

/* === Phase 228: Pflanzen-Generatoren === */
function genPflanzenPinQ(cat){"""
c = c.replace(OLD4, NEW4)

# ─── STEP 5: MODES array — append 60 arch modes ───────────────────────────────
OLD5 = '  {id:"ws_emob_bidirektionalladen",icon:"\\u{1F501}",title:"WS: Bidirektionalladen",group:"emobilitaet",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus BIDIREKTIONALLADEN!",desc:"Anagramm-R\\u00e4tsel \\u2014 18 Buchstaben"}\n];'
assert c.count(OLD5) == 1, f"STEP5 anchor not found or not unique: {c.count(OLD5)}"
NEW5 = '''  {id:"ws_emob_bidirektionalladen",icon:"\\u{1F501}",title:"WS: Bidirektionalladen",group:"emobilitaet",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus BIDIREKTIONALLADEN!",desc:"Anagramm-R\\u00e4tsel \\u2014 18 Buchstaben"},
  /* === Phase 231: Arch\\u00e4ologie & Verlorene Welten === */
  {id:"uk_arch_artefakte",icon:"\\u{1F3FA}",title:"Artefakt-Standorte",group:"archaeologie",prompt:"Wo wird dieses Artefakt aufbewahrt?",desc:"Ber\\u00fchmte Artefakte & ihre Museen"},
  {id:"uk_arch_megalithanlagen",icon:"\\u{1FAA8}",title:"Megalith-Anlagen",group:"archaeologie",prompt:"Wo liegt diese Megalithanlage?",desc:"Steinkreise & Menhire weltweit"},
  {id:"uk_arch_versunkene_staedte",icon:"\\u{1F30A}",title:"Versunkene St\\u00e4dte",group:"archaeologie",prompt:"Wo liegt diese versunkene Stadt?",desc:"Unterwasserfunde & verlorene Orte"},
  {id:"uk_arch_hoehlenmalerien",icon:"\\u{1F5BC}",title:"H\\u00f6hlenmalereien",group:"archaeologie",prompt:"Wo befinden sich diese H\\u00f6hlenmalereien?",desc:"Pr\\u00e4historische Kunst weltweit"},
  {id:"uk_arch_digitalprojekte",icon:"\\u{1F4BB}",title:"Digital-Arch\\u00e4ologie",group:"archaeologie",prompt:"Wo hat diese Institution ihren Sitz?",desc:"3D-Scanning & digitales Erbe"},
  {id:"uk_arch_graberfelder",icon:"\\u26B0",title:"Nekropolen",group:"archaeologie",prompt:"Wo liegt diese Nekropole?",desc:"Ber\\u00fchmte Gr\\u00e4berfelder & Gr\\u00e4ber"},
  {id:"uk_arch_schiffswracks",icon:"\\u{1F6A2}",title:"Schiffswracks",group:"archaeologie",prompt:"Wo liegt dieses Schiffswrack?",desc:"Ber\\u00fchmte Wracks weltweit"},
  {id:"uk_arch_maya_inka",icon:"\\u{1F333}",title:"Maya & Inka-Ruinen",group:"archaeologie",prompt:"Wo liegt diese Ruine?",desc:"Pr\\u00e4kolumbische Kulturst\\u00e4tten"},
  {id:"uk_arch_roemische_limes",icon:"\\u{1F6E1}",title:"R\\u00f6mischer Limes",group:"archaeologie",prompt:"Wo liegt dieses Grenzkastell?",desc:"R\\u00f6mische Grenzanlagen & Castra"},
  {id:"uk_arch_pfahlbauten",icon:"\\u{1F3DA}",title:"Pfahlbauten",group:"archaeologie",prompt:"Wo befinden sich diese Pfahlbauten?",desc:"Pr\\u00e4historische Seesiedlungen"},
  {id:"uk_arch_wuestenstaedte",icon:"\\u{1F3DC}",title:"W\\u00fcstenkulturen",group:"archaeologie",prompt:"Wo liegt diese Ruinenstadt?",desc:"Verlassene Karawanenstationen"},
  {id:"uk_arch_fossilien",icon:"\\u{1F9B4}",title:"Fossilienfundst\\u00e4tten",group:"archaeologie",prompt:"Wo liegt diese Fossilienst\\u00e4tte?",desc:"Dinosaurier & Fossilien weltweit"},
  {id:"uk_arch_sensationsfunde",icon:"\\u2728",title:"Sensationsfunde",group:"archaeologie",prompt:"Wo wurde dieser Sensationsfund gemacht?",desc:"Zuf\\u00e4llige Entdeckungen der Geschichte"},
  {id:"hl_arch_alter_artefakte",icon:"\\u23F3",title:"H/L: Alter von Artefakten",group:"archaeologie",prompt:"Welches Artefakt ist \\u00e4lter?",desc:"H\\u00f6her/Niedriger: Alter in Jahren v. Chr."},
  {id:"hl_arch_gewicht_megalithen",icon:"\\u2696\\uFE0F",title:"H/L: Megalith-Gewicht",group:"archaeologie",prompt:"Welcher Megalith ist schwerer?",desc:"H\\u00f6her/Niedriger: Gewicht in Tonnen"},
  {id:"hl_arch_entdeckungsjahr",icon:"\\u{1F4C5}",title:"H/L: Entdeckungsjahr",group:"archaeologie",prompt:"Welche Entdeckung ist j\\u00fcnger?",desc:"H\\u00f6her/Niedriger: Jahr der Entdeckung"},
  {id:"hl_arch_fundtiefe",icon:"\\u{1F4CF}",title:"H/L: Fundtiefe",group:"archaeologie",prompt:"Welcher Fund liegt tiefer?",desc:"H\\u00f6her/Niedriger: Tiefe in Metern"},
  {id:"hl_arch_groesse_ruinen",icon:"\\u{1F4D0}",title:"H/L: Gr\\u00f6\\u00dfe von Ruinen",group:"archaeologie",prompt:"Welche Ruine ist gr\\u00f6\\u00dfer?",desc:"H\\u00f6her/Niedriger: Fl\\u00e4che in Hektar"},
  {id:"hl_arch_grabbeigaben",icon:"\\u{1FAF4}",title:"H/L: Grabbeigaben",group:"archaeologie",prompt:"Wo wurden mehr Grabbeigaben gefunden?",desc:"H\\u00f6her/Niedriger: Anzahl Objekte"},
  {id:"hl_arch_strassenlaenge",icon:"\\u{1F6E3}",title:"H/L: Antike Stra\\u00dfenl\\u00e4nge",group:"archaeologie",prompt:"Welches Stra\\u00dfennetz ist l\\u00e4nger?",desc:"H\\u00f6her/Niedriger: Kilometer Netzl\\u00e4nge"},
  {id:"hl_arch_c14_alter",icon:"\\u269B\\uFE0F",title:"H/L: C14-Alter",group:"archaeologie",prompt:"Welches Objekt ist laut C14 \\u00e4lter?",desc:"H\\u00f6her/Niedriger: Jahre BP"},
  {id:"hl_arch_scandatenvolumen",icon:"\\u{1F4BE}",title:"H/L: 3D-Scan-Daten",group:"archaeologie",prompt:"Welches Scan-Projekt hat mehr Daten?",desc:"H\\u00f6her/Niedriger: GB Scandaten"},
  {id:"hl_arch_bauzeit",icon:"\\u{1F3D7}",title:"H/L: Bauzeit",group:"archaeologie",prompt:"Wessen Bau dauerte l\\u00e4nger?",desc:"H\\u00f6her/Niedriger: Jahre Bauzeit"},
  {id:"hl_arch_hoehe_bauwerke",icon:"\\u{1F5FC}",title:"H/L: H\\u00f6he antiker Bauwerke",group:"archaeologie",prompt:"Welches Bauwerk ist h\\u00f6her?",desc:"H\\u00f6her/Niedriger: Meter H\\u00f6he"},
  {id:"hl_arch_versicherungswert",icon:"\\u{1F4B0}",title:"H/L: Artefakt-Wert",group:"archaeologie",prompt:"Welches Artefakt ist wertvoller?",desc:"H\\u00f6her/Niedriger: Sch\\u00e4tzwert in Mio. EUR"},
  {id:"uk_arch_epochen",icon:"\\u{1F4DC}",title:"Artefakt-Epochen",group:"archaeologie",prompt:"Welcher Epoche geh\\u00f6rt dieses Artefakt an?",desc:"Stein-, Bronze-, Eisenzeit oder Antike"},
  {id:"uk_arch_werkzeuge",icon:"\\u{1FA93}",title:"Antike Werkzeuge",group:"archaeologie",prompt:"Aus welcher Zeit stammt dieses Werkzeug?",desc:"Werkzeuge & ihre Epochen"},
  {id:"uk_arch_archaeologen",icon:"\\u{1F9D1}\\u200D\\u{1F52C}",title:"Ber\\u00fchmte Arch\\u00e4ologen",group:"archaeologie",prompt:"Wer entdeckte diese Fundst\\u00e4tte?",desc:"Entdeckungen & ihre Entdecker"},
  {id:"uk_arch_datierungsmethoden",icon:"\\u{1F9EA}",title:"Datierungsmethoden",group:"archaeologie",prompt:"Welche Methode passt hier?",desc:"C14, Dendro, TL, Stratigraphie"},
  {id:"uk_arch_3d_methoden",icon:"\\u{1F4F7}",title:"3D-Dokumentation",group:"archaeologie",prompt:"F\\u00fcr welche Anwendung am besten?",desc:"Photogrammetrie, LiDAR & Co"},
  {id:"uk_arch_schriften",icon:"\\u270D\\uFE0F",title:"Antike Schriften",group:"archaeologie",prompt:"Welcher Kultur entstammt diese Schrift?",desc:"Keilschrift, Hieroglyphen & mehr"},
  {id:"uk_arch_goetter",icon:"\\u26E9\\uFE0F",title:"Antike G\\u00f6tter",group:"archaeologie",prompt:"Zu welcher Kultur geh\\u00f6rt diese Gottheit?",desc:"G\\u00f6tter der Antike"},
  {id:"uk_arch_bestattungsriten",icon:"\\u26B0\\uFE0F",title:"Bestattungsr\\u00e4ten",group:"archaeologie",prompt:"Welcher Kultur geh\\u00f6rt dieser Ritus?",desc:"Begr\\u00e4bnispraktiken weltweit"},
  {id:"uk_arch_stratigraphie",icon:"\\u{1F4CA}",title:"Stratigraphie-Prinzipien",group:"archaeologie",prompt:"Welches Prinzip wird beschrieben?",desc:"Grundlagen der Schichtenlehre"},
  {id:"uk_arch_keramikstile",icon:"\\u{1FAD9}",title:"Keramikstile",group:"archaeologie",prompt:"Welcher Kultur geh\\u00f6rt dieser Stil?",desc:"T\\u00f6pferei durch die Epochen"},
  {id:"uk_arch_numismatik",icon:"\\u{1FA99}",title:"Antike M\\u00fcnzen",group:"archaeologie",prompt:"Welcher Zivilisation geh\\u00f6rt diese M\\u00fcnze?",desc:"M\\u00fcnzkunde der Antike"},
  {id:"uk_arch_isotopenanalyse",icon:"\\u269B\\uFE0F",title:"Isotopenanalyse",group:"archaeologie",prompt:"Was verr\\u00e4t diese Analyse?",desc:"Was Isotope \\u00fcber die Vergangenheit sagen"},
  {id:"uk_arch_museen",icon:"\\u{1F3DB}",title:"Artefakte & Museen",group:"archaeologie",prompt:"In welcher Stadt wird das aufbewahrt?",desc:"Ber\\u00fchmte Sammlungen & ihr Standort"},
  {id:"uk_arch_archaeobotanik",icon:"\\u{1F33F}",title:"Arch\\u00e4obotanik",group:"archaeologie",prompt:"Was verr\\u00e4t dieser Pflanzenfund?",desc:"Pflanzenreste als historische Quellen"},
  {id:"uk_arch_handelsrouten",icon:"\\u{1F9ED}",title:"Antike Handelsrouten",group:"archaeologie",prompt:"\\u00dcber welche Route kam dieses Gut?",desc:"Seidenstra\\u00dfe, Bernstein & mehr"},
  {id:"uk_arch_waehrungen",icon:"\\u{1FA99}",title:"Antike W\\u00e4hrungen",group:"archaeologie",prompt:"Welcher Zivilisation geh\\u00f6rte diese W\\u00e4hrung?",desc:"Geldgeschichte der Antike"},
  {id:"uk_arch_faelschungen",icon:"\\u{1F575}\\uFE0F",title:"Arch\\u00e4ologische F\\u00e4lschungen",group:"archaeologie",prompt:"Was behauptete diese F\\u00e4lschung zu sein?",desc:"Ber\\u00fchmte Betrugsf\\u00e4lle"},
  {id:"uk_arch_tempel_ordnungen",icon:"\\u{1F3DB}\\uFE0F",title:"Griechische Tempelordnungen",group:"archaeologie",prompt:"Welcher Ordnung geh\\u00f6rt dieser Tempel?",desc:"Dorisch, Ionisch, Korinthisch"},
  {id:"uk_arch_indus_tal",icon:"\\u{1F30F}",title:"Indus-Tal-Kulturst\\u00e4tten",group:"archaeologie",prompt:"In welchem Land liegt diese Fundst\\u00e4tte?",desc:"Indus-Zivilisation & ihre Orte"},
  {id:"uk_arch_wikinger",icon:"\\u2694\\uFE0F",title:"Wikinger-Siedlungen",group:"archaeologie",prompt:"Wo liegt diese Wikinger-Siedlung heute?",desc:"Nordm\\u00e4nner & ihre Orte"},
  {id:"uk_arch_repatriierung",icon:"\\u{1F3F3}\\uFE0F",title:"Repatriierung",group:"archaeologie",prompt:"Welches Land fordert dieses Artefakt zur\\u00fcck?",desc:"Kulturgutr\\u00fcckgabe weltweit"},
  {id:"uk_arch_popkultur_vs_realitaet",icon:"\\u{1F3AC}",title:"Popkultur vs. Realit\\u00e4t",group:"archaeologie",prompt:"Wie korrekt ist diese Darstellung?",desc:"Hollywood-Arch\\u00e4ologie unter der Lupe"},
  {id:"uk_arch_welterbe_gefahr",icon:"\\u26A0\\uFE0F",title:"UNESCO: Bedrohte Welterbe",group:"archaeologie",prompt:"Welche Bedrohung gef\\u00e4hrdet diese St\\u00e4tte?",desc:"Krieg, Klima, Tourismus, Urbanisierung"},
  {id:"uk_arch_zufallsfunde",icon:"\\u{1F4A5}",title:"Zufallsfunde",group:"archaeologie",prompt:"Wie wurde diese Entdeckung gemacht?",desc:"Sensationen durch Zufall"},
  {id:"uk_arch_digifund_epochen",icon:"\\u{1F5A5}\\uFE0F",title:"Digitalprojekte nach Epoche",group:"archaeologie",prompt:"Welche Epoche deckt dieses Projekt ab?",desc:"Digitale Arch\\u00e4ologie & Zeitr\\u00e4ume"},
  {id:"uk_arch_antike_medizin",icon:"\\u{1FA7A}",title:"Antike Medizin",group:"archaeologie",prompt:"Welcher Kultur entstammt diese Praxis?",desc:"Heilkunde in der Antike"},
  {id:"uk_arch_schatzsuche_methoden",icon:"\\u{1F4E1}",title:"Surveymethoden",group:"archaeologie",prompt:"Was erkennt diese Methode?",desc:"Magnetometrie, Radar, LiDAR & mehr"},
  {id:"uk_arch_antike_astronomie",icon:"\\u2604\\uFE0F",title:"Antike Astronomie",group:"archaeologie",prompt:"Welcher Kultur geh\\u00f6rt diese Beobachtung?",desc:"Sternkunde & astronomische Kultst\\u00e4tten"},
  {id:"ws_arch_ausgrabungsstaette",icon:"\\u26CF\\uFE0F",title:"WS: Ausgrabungsst\\u00e4tte",group:"archaeologie",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus AUSGRABUNGSSTAETTE!",desc:"Anagramm-R\\u00e4tsel \\u2014 18 Buchstaben"},
  {id:"ws_arch_antiquitaet",icon:"\\u{1F3FA}",title:"WS: Antiquit\\u00e4t",group:"archaeologie",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus ANTIQUITAET!",desc:"Anagramm-R\\u00e4tsel \\u2014 11 Buchstaben"},
  {id:"ws_arch_dendrochronologie",icon:"\\u{1F332}",title:"WS: Dendrochronologie",group:"archaeologie",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus DENDROCHRONOLOGIE!",desc:"Anagramm-R\\u00e4tsel \\u2014 17 Buchstaben"},
  {id:"ws_arch_hieroglyphen",icon:"\\u{1F4DC}",title:"WS: Hieroglyphen",group:"archaeologie",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus HIEROGLYPHEN!",desc:"Anagramm-R\\u00e4tsel \\u2014 12 Buchstaben"},
  {id:"ws_arch_photogrammetrie",icon:"\\u{1F4F8}",title:"WS: Photogrammetrie",group:"archaeologie",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus PHOTOGRAMMETRIE!",desc:"Anagramm-R\\u00e4tsel \\u2014 15 Buchstaben"},
  {id:"ws_arch_stratigraphie",icon:"\\u{1F4CA}",title:"WS: Stratigraphie",group:"archaeologie",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus STRATIGRAPHIE!",desc:"Anagramm-R\\u00e4tsel \\u2014 13 Buchstaben"},
  {id:"ws_arch_radiocarbondatierung",icon:"\\u269B\\uFE0F",title:"WS: Radiocarbondatierung",group:"archaeologie",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus RADIOCARBONDATIERUNG!",desc:"Anagramm-R\\u00e4tsel \\u2014 20 Buchstaben"}
];'''
c = c.replace(OLD5, NEW5)

# ─── STEP 6: MODE_CATS — add archaeologie category ─────────────────────────────
OLD6 = '    "ws_emob_bidirektionalladen"\n  ],cost:0},\n};'
assert c.count(OLD6) == 1, f"STEP6 anchor not found or not unique: {c.count(OLD6)}"
NEW6 = '''    "ws_emob_bidirektionalladen"
  ],cost:0},
  archaeologie:{label:"Arch\\u00e4ologie & Historie",icon:"\\u{1F3FA}",modes:[
    "uk_arch_artefakte","uk_arch_megalithanlagen","uk_arch_versunkene_staedte",
    "uk_arch_hoehlenmalerien","uk_arch_digitalprojekte","uk_arch_graberfelder",
    "uk_arch_schiffswracks","uk_arch_maya_inka","uk_arch_roemische_limes",
    "uk_arch_pfahlbauten","uk_arch_wuestenstaedte","uk_arch_fossilien",
    "uk_arch_sensationsfunde",
    "hl_arch_alter_artefakte","hl_arch_gewicht_megalithen","hl_arch_entdeckungsjahr",
    "hl_arch_fundtiefe","hl_arch_groesse_ruinen","hl_arch_grabbeigaben",
    "hl_arch_strassenlaenge","hl_arch_c14_alter","hl_arch_scandatenvolumen",
    "hl_arch_bauzeit","hl_arch_hoehe_bauwerke","hl_arch_versicherungswert",
    "uk_arch_epochen","uk_arch_werkzeuge","uk_arch_archaeologen",
    "uk_arch_datierungsmethoden","uk_arch_3d_methoden","uk_arch_schriften",
    "uk_arch_goetter","uk_arch_bestattungsriten","uk_arch_stratigraphie",
    "uk_arch_keramikstile","uk_arch_numismatik","uk_arch_isotopenanalyse",
    "uk_arch_museen","uk_arch_archaeobotanik","uk_arch_handelsrouten",
    "uk_arch_waehrungen","uk_arch_faelschungen","uk_arch_tempel_ordnungen",
    "uk_arch_indus_tal","uk_arch_wikinger","uk_arch_repatriierung",
    "uk_arch_popkultur_vs_realitaet","uk_arch_welterbe_gefahr","uk_arch_zufallsfunde",
    "uk_arch_digifund_epochen","uk_arch_antike_medizin","uk_arch_schatzsuche_methoden",
    "uk_arch_antike_astronomie",
    "ws_arch_ausgrabungsstaette","ws_arch_antiquitaet","ws_arch_dendrochronologie",
    "ws_arch_hieroglyphen","ws_arch_photogrammetrie","ws_arch_stratigraphie",
    "ws_arch_radiocarbondatierung"
  ],cost:0},
};'''
c = c.replace(OLD6, NEW6)

# ─── STEP 7: GEN dispatch ─────────────────────────────────────────────────────
OLD7 = "  ws_emob_bidirektionalladen:()=>{initEmobWS(\"bidirektionalladen\");return null;},"
assert c.count(OLD7) == 1, f"STEP7 anchor not found or not unique: {c.count(OLD7)}"
NEW7 = '''  ws_emob_bidirektionalladen:()=>{initEmobWS("bidirektionalladen");return null;},
  /* Phase 231: Arch\\u00e4ologie */
  uk_arch_artefakte:()=>genArchPinQ("artefakte"),
  uk_arch_megalithanlagen:()=>genArchPinQ("megalithanlagen"),
  uk_arch_versunkene_staedte:()=>genArchPinQ("versunkene_staedte"),
  uk_arch_hoehlenmalerien:()=>genArchPinQ("hoehlenmalerien"),
  uk_arch_digitalprojekte:()=>genArchPinQ("digitalprojekte"),
  uk_arch_graberfelder:()=>genArchPinQ("graberfelder"),
  uk_arch_schiffswracks:()=>genArchPinQ("schiffswracks"),
  uk_arch_maya_inka:()=>genArchPinQ("maya_inka"),
  uk_arch_roemische_limes:()=>genArchPinQ("roemische_limes"),
  uk_arch_pfahlbauten:()=>genArchPinQ("pfahlbauten"),
  uk_arch_wuestenstaedte:()=>genArchPinQ("wuestenstaedte"),
  uk_arch_fossilien:()=>genArchPinQ("fossilien"),
  uk_arch_sensationsfunde:()=>genArchPinQ("sensationsfunde"),
  hl_arch_alter_artefakte:()=>genArchHL("alter_artefakte"),
  hl_arch_gewicht_megalithen:()=>genArchHL("gewicht_megalithen"),
  hl_arch_entdeckungsjahr:()=>genArchHL("entdeckungsjahr"),
  hl_arch_fundtiefe:()=>genArchHL("fundtiefe"),
  hl_arch_groesse_ruinen:()=>genArchHL("groesse_ruinen"),
  hl_arch_grabbeigaben:()=>genArchHL("grabbeigaben"),
  hl_arch_strassenlaenge:()=>genArchHL("strassenlaenge"),
  hl_arch_c14_alter:()=>genArchHL("c14_alter"),
  hl_arch_scandatenvolumen:()=>genArchHL("scandatenvolumen"),
  hl_arch_bauzeit:()=>genArchHL("bauzeit"),
  hl_arch_hoehe_bauwerke:()=>genArchHL("hoehe_bauwerke"),
  hl_arch_versicherungswert:()=>genArchHL("versicherungswert"),
  uk_arch_epochen:()=>genArchMatchQ("epochen"),
  uk_arch_werkzeuge:()=>genArchMatchQ("werkzeuge"),
  uk_arch_archaeologen:()=>genArchMatchQ("archaeologen"),
  uk_arch_datierungsmethoden:()=>genArchMatchQ("datierungsmethoden"),
  uk_arch_3d_methoden:()=>genArchMatchQ("3d_methoden"),
  uk_arch_schriften:()=>genArchMatchQ("schriften"),
  uk_arch_goetter:()=>genArchMatchQ("goetter"),
  uk_arch_bestattungsriten:()=>genArchMatchQ("bestattungsriten"),
  uk_arch_stratigraphie:()=>genArchMatchQ("stratigraphie"),
  uk_arch_keramikstile:()=>genArchMatchQ("keramikstile"),
  uk_arch_numismatik:()=>genArchMatchQ("numismatik"),
  uk_arch_isotopenanalyse:()=>genArchMatchQ("isotopenanalyse"),
  uk_arch_museen:()=>genArchMatchQ("museen"),
  uk_arch_archaeobotanik:()=>genArchMatchQ("archaeobotanik"),
  uk_arch_handelsrouten:()=>genArchMatchQ("handelsrouten"),
  uk_arch_waehrungen:()=>genArchMatchQ("waehrungen"),
  uk_arch_faelschungen:()=>genArchMatchQ("faelschungen"),
  uk_arch_tempel_ordnungen:()=>genArchMatchQ("tempel_ordnungen"),
  uk_arch_indus_tal:()=>genArchMatchQ("indus_tal"),
  uk_arch_wikinger:()=>genArchMatchQ("wikinger"),
  uk_arch_repatriierung:()=>genArchMatchQ("repatriierung"),
  uk_arch_popkultur_vs_realitaet:()=>genArchMatchQ("popkultur_vs_realitaet"),
  uk_arch_welterbe_gefahr:()=>genArchMatchQ("welterbe_gefahr"),
  uk_arch_zufallsfunde:()=>genArchMatchQ("zufallsfunde"),
  uk_arch_digifund_epochen:()=>genArchMatchQ("digifund_epochen"),
  uk_arch_antike_medizin:()=>genArchMatchQ("antike_medizin"),
  uk_arch_schatzsuche_methoden:()=>genArchMatchQ("schatzsuche_methoden"),
  uk_arch_antike_astronomie:()=>genArchMatchQ("antike_astronomie"),
  ws_arch_ausgrabungsstaette:()=>{initArchWS("ausgrabungsstaette");return null;},
  ws_arch_antiquitaet:()=>{initArchWS("antiquitaet");return null;},
  ws_arch_dendrochronologie:()=>{initArchWS("dendrochronologie");return null;},
  ws_arch_hieroglyphen:()=>{initArchWS("hieroglyphen");return null;},
  ws_arch_photogrammetrie:()=>{initArchWS("photogrammetrie");return null;},
  ws_arch_stratigraphie:()=>{initArchWS("stratigraphie");return null;},
  ws_arch_radiocarbondatierung:()=>{initArchWS("radiocarbondatierung");return null;},'''
c = c.replace(OLD7, NEW7)

# ─── Write output ─────────────────────────────────────────────────────────────
with open(GEN, 'w', encoding='utf-8') as f:
    f.write(c)

print("patch_231_archaeologie.py: all 7 steps applied OK")
