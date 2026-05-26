# -*- coding: utf-8 -*-
"""
Phase: 229
Date: 2026-05-26
Scope: Das Gastronomie-Update — Kulinarische Weltreise
       45 neue Modi in neuer Kategorie 'gastronomie'
       Säule 1: 9 Pin-Modi (IDs uk_gastro_*)
       Säule 2: 15 H/L-Modi (IDs hl_gastro_*)
       Säule 3: 20 Match-Modi (IDs uk_gastro_* Match)
       Säule 4: 7 WS-Modi (IDs ws_gastro_*)
       Spezial: 4 Modi (in Pin + Match)
       Neue MODE_CATS-Kategorie: gastronomie
       4 neue Generator-Funktionen
       4 neue JSON-Datenquellen
"""

import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GEN  = os.path.join(ROOT, 'gen.py')

print("[229] Reading gen.py ...")
with open(GEN, 'r', encoding='utf-8') as f:
    c = f.read()

print(f"[229] gen.py size: {len(c)} bytes")

# ── Validate JSON data files ──────────────────────────────────────────────────
data_files = {
    'gastro_pin':   os.path.join(ROOT, 'data', 'gastro_pin.json'),
    'gastro_hl':    os.path.join(ROOT, 'data', 'gastro_hl.json'),
    'gastro_match': os.path.join(ROOT, 'data', 'gastro_match.json'),
    'gastro_ws':    os.path.join(ROOT, 'data', 'gastro_ws.json'),
}
for key, path in data_files.items():
    if not os.path.isfile(path):
        print(f"[FAIL] Missing data file: {path}")
        sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        try:
            json.load(f)
            print(f"[OK]   {key}.json valid JSON")
        except json.JSONDecodeError as e:
            print(f"[FAIL] {key}.json invalid JSON: {e}")
            sys.exit(1)

# ── A. Python data loading ────────────────────────────────────────────────────
print("[229] A: Adding Python data loading lines ...")
OLD_A = "with open(os.path.join(os.path.dirname(__file__), 'data/pflanzen_ws.json'), 'r', encoding='utf-8') as _f: PFLANZEN_WS_J = _f.read()"
NEW_A = OLD_A + """
with open(os.path.join(os.path.dirname(__file__), 'data/gastro_pin.json'), 'r', encoding='utf-8') as _f: GASTRO_PIN_J = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/gastro_hl.json'), 'r', encoding='utf-8') as _f: GASTRO_HL_J = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/gastro_match.json'), 'r', encoding='utf-8') as _f: GASTRO_MATCH_J = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/gastro_ws.json'), 'r', encoding='utf-8') as _f: GASTRO_WS_J = _f.read()"""
assert c.count(OLD_A) == 1, f"Anchor not unique: {OLD_A[:80]!r}"
c = c.replace(OLD_A, NEW_A)
print("[OK]   A done")

# ── B. PLACEHOLDER chain ──────────────────────────────────────────────────────
print("[229] B: Extending PLACEHOLDER chain ...")
OLD_B = "  .replace('PLACEHOLDER_PFLANZEN_WS', PFLANZEN_WS_J)\n)"
NEW_B = """  .replace('PLACEHOLDER_PFLANZEN_WS', PFLANZEN_WS_J)
  .replace('PLACEHOLDER_GASTRO_PIN', GASTRO_PIN_J)
  .replace('PLACEHOLDER_GASTRO_HL', GASTRO_HL_J)
  .replace('PLACEHOLDER_GASTRO_MATCH', GASTRO_MATCH_J)
  .replace('PLACEHOLDER_GASTRO_WS', GASTRO_WS_J)
)"""
assert c.count(OLD_B) == 1, f"Anchor not unique: {OLD_B[:80]!r}"
c = c.replace(OLD_B, NEW_B)
print("[OK]   B done")

# ── C. JS const declarations ──────────────────────────────────────────────────
print("[229] C: Adding JS const declarations ...")
OLD_C = "const PFLANZEN_WS_DATA=PLACEHOLDER_PFLANZEN_WS;"
NEW_C = """const PFLANZEN_WS_DATA=PLACEHOLDER_PFLANZEN_WS;

/* === Phase 229: Gastronomie-Datensaetze === */
const GASTRO_PIN_DATA=PLACEHOLDER_GASTRO_PIN;
const GASTRO_HL_DATA=PLACEHOLDER_GASTRO_HL;
const GASTRO_MATCH_DATA=PLACEHOLDER_GASTRO_MATCH;
const GASTRO_WS_DATA=PLACEHOLDER_GASTRO_WS;"""
assert c.count(OLD_C) == 1, f"Anchor not unique: {OLD_C[:80]!r}"
c = c.replace(OLD_C, NEW_C)
print("[OK]   C done")

# ── D. Generator functions ────────────────────────────────────────────────────
print("[229] D: Adding generator functions ...")
OLD_D = "function genUniversalMatchQ(cat){"
NEW_D = """function genGastroPinQ(cat){
  var d=GASTRO_PIN_DATA[cat];
  if(!d||!d.items||!d.items.length)return null;
  var idx=~~(rng()*d.items.length);
  var item=d.items[idx];
  return {type:"uk_pin",subj:item.n,lat:item.lat,lng:item.lng,
    prompt:d.prompt,cat:cat,itemIdx:idx};
}
function genGastroHL(dataKey){
  var d=GASTRO_HL_DATA[dataKey];
  if(!d||!d.items||d.items.length<2)return null;
  var len=d.items.length;
  var W=Math.max(1,Math.floor(len*0.1));
  var iA,iB;
  do{iA=~~(rng()*len);iB=~~(rng()*len);}while(iA===iB||Math.abs(iA-iB)<W);
  var a=d.items[iA],b=d.items[iB];
  return {type:"hl",a:{name:a.name,val:a.val},b:{name:b.name,val:b.val},
    unit:d.unit,prompt:d.prompt,higherWins:true};
}
function genGastroMatchQ(cat){
  var d=GASTRO_MATCH_DATA[cat];
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
function initGastroWS(key){
  clearInterval(tIv);_wsDetachKb();
  var entry=GASTRO_WS_DATA[key];
  if(!entry||!entry.validWords){console.warn("[GeoQuest] GastroWS missing:"+key);S.ph="menu";render();return;}
  var userLang=S.language||localStorage.getItem("gq_lang")||"en";
  var wsLang=_WS_LANGS.has(userLang)?userLang:"en";
  var raw=entry.validWords[wsLang];
  var hasOwn=Array.isArray(raw)&&raw.length>0;
  var actualLang=hasOwn?wsLang:"en";
  var src2=hasOwn?raw:(entry.validWords["en"]||[]);
  var words=src2.map(function(w){return w.toUpperCase();}).filter(function(w){return w.length>=3;});
  if(!words.length){console.warn("[GeoQuest] GastroWS no words:"+key);S.ph="menu";render();return;}
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
function genUniversalMatchQ(cat){"""
assert c.count(OLD_D) == 1, f"Anchor not unique: {OLD_D[:80]!r}"
c = c.replace(OLD_D, NEW_D)
print("[OK]   D done")

# ── E. MODES entries ──────────────────────────────────────────────────────────
print("[229] E: Adding MODES entries ...")
OLD_E = '{id:"ws_pflanzen_ginkgobaum",icon:"\\u{1F333}",title:"[BETA] WS: Ginkgobaum",group:"tiere",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus GINKGOBAUM!",desc:"Anagramm-R\\u00e4tsel \\u2014 10 Buchstaben"}\n];'
NEW_E = '''{id:"ws_pflanzen_ginkgobaum",icon:"\\u{1F333}",title:"[BETA] WS: Ginkgobaum",group:"tiere",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus GINKGOBAUM!",desc:"Anagramm-R\\u00e4tsel \\u2014 10 Buchstaben"},
  /* === Phase 229: Gastronomie-Update === */
  /* -- Pin Modi -- */
  {id:"uk_gastro_nationalgerichte",icon:"\\u{1F37D}",title:"[BETA] Nationalgerichte pinnen",group:"gastronomie",prompt:"\\u{1F4CD} Wo entstand dieses Nationalgericht?",desc:"Wiener Schnitzel, Paella, Kimchi und mehr"},
  {id:"uk_gastro_kaffee_anbau",icon:"\\u2615",title:"[BETA] Kaffee-Anbaugebiete",group:"gastronomie",prompt:"\\u{1F4CD} Wo liegt dieses Kaffee-Anbaugebiet?",desc:"Von Äthiopien bis Hawaii"},
  {id:"uk_gastro_brauereien",icon:"\\u{1F37A}",title:"[BETA] Brauereien pinnen",group:"gastronomie",prompt:"\\u{1F4CD} Wo liegt diese berühmte Brauerei?",desc:"Guinness, Weihenstephan, Pilsner Urquell"},
  {id:"uk_gastro_gewuerze_selten",icon:"\\u{1F33F}",title:"[BETA] Seltene Gewürze orten",group:"gastronomie",prompt:"\\u{1F4CD} Wo liegt der Ursprungsort dieses Gewürzes?",desc:"Seltene Gewürze aus aller Welt"},
  {id:"uk_gastro_kaffeehaeuser",icon:"\\u{1F375}",title:"[BETA] Historische Kaffeehäuser",group:"gastronomie",prompt:"\\u{1F4CD} Wo liegt dieses historische Kaffeehaus?",desc:"Café Central, Café de Flore und mehr"},
  {id:"uk_gastro_schokoladen",icon:"\\u{1F36B}",title:"[BETA] Schokoladenfabriken",group:"gastronomie",prompt:"\\u{1F4CD} Wo liegt dieser Schokoladenproduzent?",desc:"Lindt, Valrhona, Hershey's und mehr"},
  {id:"uk_gastro_weinlagen",icon:"\\u{1F377}",title:"[BETA] Weinlagen & Châteaux",group:"gastronomie",prompt:"\\u{1F4CD} Wo liegt dieses berühmte Weingut?",desc:"Romanée-Conti, Sassicaia, Opus One"},
  {id:"uk_gastro_fermentation_orte",icon:"\\u{1F9AB}",title:"[BETA] Fermentations-Orte",group:"gastronomie",prompt:"\\u{1F4CD} Wo ist dieser Ort für sein fermentiertes Produkt bekannt?",desc:"Kimchi, Miso, Sauerkraut, Sake"},
  {id:"uk_gastro_kulinarische_feste",icon:"\\u{1F389}",title:"[BETA] Kulinarische Festivals",group:"gastronomie",prompt:"\\u{1F4CD} Wo findet dieses kulinarische Festival statt?",desc:"Oktoberfest, La Tomatina und mehr"},
  /* -- H/L Modi -- */
  {id:"hl_gastro_kalorien",icon:"\\u{1F525}",title:"[BETA] HL: Kalorien",group:"gastronomie",prompt:"Welches Gericht hat mehr Kalorien pro 100g?",desc:"Kalorienvergleich bekannter Speisen"},
  {id:"hl_gastro_kerntemperatur",icon:"\\u{1F321}",title:"[BETA] HL: Kerntemperatur",group:"gastronomie",prompt:"Welches Fleisch benötigt eine höhere Kerntemperatur?",desc:"Ziel-Kerntemperaturen beim Garen"},
  {id:"hl_gastro_zubereitungszeit",icon:"\\u23F1",title:"[BETA] HL: Zubereitungszeit",group:"gastronomie",prompt:"Welches Gericht dauert länger?",desc:"Von Instant-Nudeln bis Sauerbraten"},
  {id:"hl_gastro_fermentationsdauer",icon:"\\u{1F9F4}",title:"[BETA] HL: Fermentationsdauer",group:"gastronomie",prompt:"Welches Produkt fermentiert länger?",desc:"Von Joghurt bis Balsamico"},
  {id:"hl_gastro_scoville",icon:"\\u{1F336}",title:"[BETA] HL: Scoville-Skala",group:"gastronomie",prompt:"Welche Chilischote ist schärfer?",desc:"Von Paprika bis Carolina Reaper"},
  {id:"hl_gastro_preis_kg",icon:"\\u{1F4B0}",title:"[BETA] HL: Preis pro Kilo",group:"gastronomie",prompt:"Was kostet mehr pro Kilogramm?",desc:"Von Salz bis Safran"},
  {id:"hl_gastro_wasseranteil",icon:"\\u{1F4A7}",title:"[BETA] HL: Wasseranteil",group:"gastronomie",prompt:"Welches Lebensmittel enthält mehr Wasser?",desc:"Wassergehalt verschiedener Lebensmittel"},
  {id:"hl_gastro_backtemperatur",icon:"\\u{1F525}",title:"[BETA] HL: Backtemperatur",group:"gastronomie",prompt:"Bei welcher Temperatur wird das gebacken?",desc:"Vom Baiser bis zur Neapolitanischen Pizza"},
  {id:"hl_gastro_rezept_alter",icon:"\\u{1F4DC}",title:"[BETA] HL: Rezept-Alter",group:"gastronomie",prompt:"Welches Rezept ist älter?",desc:"Von ägyptischem Brot bis zum Big Mac"},
  {id:"hl_gastro_alkoholgehalt",icon:"\\u{1F37E}",title:"[BETA] HL: Alkoholgehalt",group:"gastronomie",prompt:"Welches Getränk hat mehr Alkohol?",desc:"Von Kombucha bis Absinthe"},
  {id:"hl_gastro_zutaten_anzahl",icon:"\\u{1F9C9}",title:"[BETA] HL: Zutaten-Anzahl",group:"gastronomie",prompt:"Welches Rezept hat mehr Zutaten?",desc:"Von Pasta Aglio bis Mole Poblano"},
  {id:"hl_gastro_schmelzpunkt",icon:"\\u{1F321}",title:"[BETA] HL: Schmelzpunkt",group:"gastronomie",prompt:"Welches Produkt hat einen höheren Schmelzpunkt?",desc:"Schokolade, Fette, Zucker"},
  {id:"hl_gastro_prokopf_verbrauch",icon:"\\u{1F4CA}",title:"[BETA] HL: Pro-Kopf-Verbrauch",group:"gastronomie",prompt:"Welches Nahrungsmittel wird pro Kopf mehr gegessen?",desc:"Jahresverbrauch weltweit im Vergleich"},
  {id:"hl_gastro_haltbarkeit",icon:"\\u{1F4C5}",title:"[BETA] HL: Haltbarkeit",group:"gastronomie",prompt:"Welches Lebensmittel hält sich länger?",desc:"Von frischem Baguette bis Honig"},
  {id:"hl_gastro_rekord_gewicht",icon:"\\u{1F3C6}",title:"[BETA] HL: Rekord-Gewicht",group:"gastronomie",prompt:"Welches Nahrungsmittel hält den schwereren Weltrekord?",desc:"Rekordgemüse, Rekordkäse und mehr"},
  /* -- Match Modi -- */
  {id:"uk_gastro_hausmannskost",icon:"\\u{1F372}",title:"[BETA] Hausmannskost zuordnen",group:"gastronomie",prompt:"Aus welchem Land stammt dieses Gericht?",desc:"Gerichte aus aller Welt ihren Ländern zuordnen"},
  {id:"uk_gastro_kuechengeraete",icon:"\\u{1F374}",title:"[BETA] Küchengeräte sortieren",group:"gastronomie",prompt:"Welcher Kategorie gehört dieses Küchengerät an?",desc:"Schneiden, Mischen, Garen oder Messen?"},
  {id:"uk_gastro_schnitttechniken",icon:"\\u{1F52A}",title:"[BETA] Schnitttechniken",group:"gastronomie",prompt:"Für welche Lebensmittelgruppe wird diese Technik genutzt?",desc:"Profi-Schnitttechniken aus der Küche"},
  {id:"uk_gastro_originalrezept",icon:"\\u{1F4CD}",title:"[BETA] Geburtsort-Rezept",group:"gastronomie",prompt:"Aus welcher Stadt stammt dieses Gericht?",desc:"Originalrezepte ihren Ursprungsorten zuordnen"},
  {id:"uk_gastro_teigtaschen",icon:"\\u{1F95F}",title:"[BETA] Teigtaschen der Welt",group:"gastronomie",prompt:"Aus welchem Land stammt diese Teigtasche?",desc:"Von Gyoza bis Pierogi"},
  {id:"uk_gastro_gewuerzmischungen",icon:"\\u{1F9C2}",title:"[BETA] Gewürzmischungen",group:"gastronomie",prompt:"Welcher Küche gehört diese Gewürzmischung an?",desc:"Garam Masala, Za'atar, Cajun und mehr"},
  {id:"uk_gastro_fleisch_cuts",icon:"\\u{1F969}",title:"[BETA] Fleischzuschnitte",group:"gastronomie",prompt:"Von welchem Tier stammt dieser Fleischzuschnitt?",desc:"Ribeye, Gigot, Rack of Lamb und mehr"},
  {id:"uk_gastro_bakterien_pilze",icon:"\\u{1F9AB}",title:"[BETA] Mikroorganismen & Fermentation",group:"gastronomie",prompt:"Bei welchem Produkt ist dieser Mikroorganismus beteiligt?",desc:"Hefen, Bakterien und Schimmelpilze"},
  {id:"uk_gastro_kaffeespezialitaeten",icon:"\\u2615",title:"[BETA] Kaffeespezialitäten",group:"gastronomie",prompt:"Auf welcher Basis basiert dieser Kaffeedrink?",desc:"Espresso, Filter, Cold Brew oder Mokka?"},
  {id:"uk_gastro_pasta_formen",icon:"\\u{1F35D}",title:"[BETA] Pasta & Saucen",group:"gastronomie",prompt:"Mit welcher Sauce wird diese Pasta kombiniert?",desc:"Die perfekte Pasta-Sauce-Kombination"},
  {id:"uk_gastro_exotische_fruechte",icon:"\\u{1F34D}",title:"[BETA] Exotische Früchte",group:"gastronomie",prompt:"Von welchem Kontinent stammt diese exotische Frucht?",desc:"Durian, Açaí, Marula und mehr"},
  {id:"uk_gastro_brotsorten",icon:"\\u{1F35E}",title:"[BETA] Brotsorten der Welt",group:"gastronomie",prompt:"Aus welchem Land stammt diese Brotsorte?",desc:"Baguette, Injera, Naan und mehr"},
  {id:"uk_gastro_vegan_alternativen",icon:"\\u{1F331}",title:"[BETA] Vegane Alternativen",group:"gastronomie",prompt:"Was ersetzt dieses vegane Produkt?",desc:"Fleisch-, Milch-, Ei- oder Käseersatz?"},
  {id:"uk_gastro_fruehstueck_welt",icon:"\\u{1F373}",title:"[BETA] Frühstück der Welt",group:"gastronomie",prompt:"Aus welchem Land stammt dieses Frühstücksgericht?",desc:"Full English bis Shakshuka"},
  {id:"uk_gastro_fachbegriffe_herd",icon:"\\u{1F9D1}\\u200D\\u{1F373}",title:"[BETA] Kochfachbegriffe",group:"gastronomie",prompt:"Welcher Kochtechnik-Kategorie gehört dieser Begriff an?",desc:"Braten, Kochen, Backen oder Fermentieren?"},
  {id:"uk_gastro_sushi_arten",icon:"\\u{1F363}",title:"[BETA] Sushi-Stile",group:"gastronomie",prompt:"Welcher Sushi-Stil beschreibt diese Form?",desc:"Nigiri, Maki, Temaki, Chirashi"},
  {id:"uk_gastro_ess_etikette",icon:"\\u{1F91D}",title:"[BETA] Ess-Etikette weltweit",group:"gastronomie",prompt:"In welchem Land gilt diese Tischetikette-Regel?",desc:"Tischmanieren aus aller Welt"},
  {id:"uk_gastro_tabus",icon:"\\u{1F6AB}",title:"[BETA] Nahrungstabus",group:"gastronomie",prompt:"Welcher Religion ist dieses Nahrungstabu zugeordnet?",desc:"Islam, Hinduismus, Judentum, Buddhismus"},
  {id:"uk_gastro_film_food",icon:"\\u{1F3AC}",title:"[BETA] Essen im Film",group:"gastronomie",prompt:"Zu welchem Franchise gehört dieses ikonische Filmessen?",desc:"Disney, Pixar, Marvel oder Kultkino?"},
  {id:"uk_gastro_seidenstrasse",icon:"\\u{1F30F}",title:"[BETA] Seidenstraße & Gewürze",group:"gastronomie",prompt:"Aus welcher Region der Seidenstraße stammt dies?",desc:"China, Indien, Persien oder Europa?"},
  /* -- WS Modi -- */
  {id:"ws_gastro_zitruspresse",icon:"\\u{1F34B}",title:"[BETA] WS: Zitruspresse",group:"gastronomie",noMultiplayer:true,prompt:"Bilde Wörter aus ZITRUSPRESSE!",desc:"Anagramm-Rätsel — 12 Buchstaben"},
  {id:"ws_gastro_kuechenmaschine",icon:"\\u{1F374}",title:"[BETA] WS: Küchenmaschine",group:"gastronomie",noMultiplayer:true,prompt:"Bilde Wörter aus KUECHENMASCHINE!",desc:"Anagramm-Rätsel — 14 Buchstaben"},
  {id:"ws_gastro_sauerteigbrot",icon:"\\u{1F35E}",title:"[BETA] WS: Sauerteigbrot",group:"gastronomie",noMultiplayer:true,prompt:"Bilde Wörter aus SAUERTEIGBROT!",desc:"Anagramm-Rätsel — 13 Buchstaben"},
  {id:"ws_gastro_fermentation",icon:"\\u{1F9AB}",title:"[BETA] WS: Fermentation",group:"gastronomie",noMultiplayer:true,prompt:"Bilde Wörter aus FERMENTATION!",desc:"Anagramm-Rätsel — 12 Buchstaben"},
  {id:"ws_gastro_wurzelgemuese",icon:"\\u{1F955}",title:"[BETA] WS: Wurzelgemüse",group:"gastronomie",noMultiplayer:true,prompt:"Bilde Wörter aus WURZELGEMUESE!",desc:"Anagramm-Rätsel — 13 Buchstaben"},
  {id:"ws_gastro_schwarzwaelder",icon:"\\u{1F370}",title:"[BETA] WS: Schwarzwälder",group:"gastronomie",noMultiplayer:true,prompt:"Bilde Wörter aus SCHWARZWAELDER!",desc:"Anagramm-Rätsel — 14 Buchstaben"},
  {id:"ws_gastro_kaltentsafter",icon:"\\u{1F34A}",title:"[BETA] WS: Kaltentsafter",group:"gastronomie",noMultiplayer:true,prompt:"Bilde Wörter aus KALTENTSAFTER!",desc:"Anagramm-Rätsel — 13 Buchstaben"}
];'''
assert c.count(OLD_E) == 1, f"Anchor not unique: {OLD_E[:80]!r}"
c = c.replace(OLD_E, NEW_E)
print("[OK]   E done")

# ── F. MODE_CATS gastronomie entry ────────────────────────────────────────────
print("[229] F: Adding MODE_CATS gastronomie entry ...")
OLD_F = '    "ws_pflanzen_kaffeebohne","ws_pflanzen_weihnachtsstern","ws_pflanzen_ginkgobaum"\n  ],cost:0},\n};'
NEW_F = '''    "ws_pflanzen_kaffeebohne","ws_pflanzen_weihnachtsstern","ws_pflanzen_ginkgobaum"
  ],cost:0},
  gastronomie:{label:"Kulinarische Weltreise",icon:"\\u{1F373}",modes:[
    "uk_gastro_nationalgerichte","uk_gastro_kaffee_anbau","uk_gastro_brauereien",
    "uk_gastro_gewuerze_selten","uk_gastro_kaffeehaeuser","uk_gastro_schokoladen",
    "uk_gastro_weinlagen","uk_gastro_fermentation_orte","uk_gastro_kulinarische_feste",
    "hl_gastro_kalorien","hl_gastro_kerntemperatur","hl_gastro_zubereitungszeit",
    "hl_gastro_fermentationsdauer","hl_gastro_scoville","hl_gastro_preis_kg",
    "hl_gastro_wasseranteil","hl_gastro_backtemperatur","hl_gastro_rezept_alter",
    "hl_gastro_alkoholgehalt","hl_gastro_zutaten_anzahl","hl_gastro_schmelzpunkt",
    "hl_gastro_prokopf_verbrauch","hl_gastro_haltbarkeit","hl_gastro_rekord_gewicht",
    "uk_gastro_hausmannskost","uk_gastro_kuechengeraete","uk_gastro_schnitttechniken",
    "uk_gastro_originalrezept","uk_gastro_teigtaschen","uk_gastro_gewuerzmischungen",
    "uk_gastro_fleisch_cuts","uk_gastro_bakterien_pilze","uk_gastro_kaffeespezialitaeten",
    "uk_gastro_pasta_formen","uk_gastro_exotische_fruechte","uk_gastro_brotsorten",
    "uk_gastro_vegan_alternativen","uk_gastro_fruehstueck_welt","uk_gastro_fachbegriffe_herd",
    "uk_gastro_sushi_arten","uk_gastro_ess_etikette","uk_gastro_tabus",
    "uk_gastro_film_food","uk_gastro_seidenstrasse",
    "ws_gastro_zitruspresse","ws_gastro_kuechenmaschine","ws_gastro_sauerteigbrot",
    "ws_gastro_fermentation","ws_gastro_wurzelgemuese","ws_gastro_schwarzwaelder",
    "ws_gastro_kaltentsafter"
  ],cost:0},
};'''
assert c.count(OLD_F) == 1, f"Anchor not unique: {OLD_F[:80]!r}"
c = c.replace(OLD_F, NEW_F)
print("[OK]   F done")

# ── G. GEN dispatch entries ───────────────────────────────────────────────────
print("[229] G: Adding GEN dispatch entries ...")
OLD_G = "  ws_pflanzen_ginkgobaum:()=>{initPflanzenWS(\"ginkgobaum\");return null;},\n  uk_surf_spots:()=>genUniversalPinQ(\"surf_spots\"),"
NEW_G = """  ws_pflanzen_ginkgobaum:()=>{initPflanzenWS("ginkgobaum");return null;},
  /* Phase 229: Gastronomie dispatch */
  uk_gastro_nationalgerichte:()=>genGastroPinQ("nationalgerichte"),
  uk_gastro_kaffee_anbau:()=>genGastroPinQ("kaffee_anbau"),
  uk_gastro_brauereien:()=>genGastroPinQ("brauereien"),
  uk_gastro_gewuerze_selten:()=>genGastroPinQ("gewuerze_selten"),
  uk_gastro_kaffeehaeuser:()=>genGastroPinQ("kaffeehaeuser"),
  uk_gastro_schokoladen:()=>genGastroPinQ("schokoladen"),
  uk_gastro_weinlagen:()=>genGastroPinQ("weinlagen"),
  uk_gastro_fermentation_orte:()=>genGastroPinQ("fermentation_orte"),
  uk_gastro_kulinarische_feste:()=>genGastroPinQ("kulinarische_feste"),
  hl_gastro_kalorien:()=>genGastroHL("kalorien"),
  hl_gastro_kerntemperatur:()=>genGastroHL("kerntemperatur"),
  hl_gastro_zubereitungszeit:()=>genGastroHL("zubereitungszeit"),
  hl_gastro_fermentationsdauer:()=>genGastroHL("fermentationsdauer"),
  hl_gastro_scoville:()=>genGastroHL("scoville"),
  hl_gastro_preis_kg:()=>genGastroHL("preis_kg"),
  hl_gastro_wasseranteil:()=>genGastroHL("wasseranteil"),
  hl_gastro_backtemperatur:()=>genGastroHL("backtemperatur"),
  hl_gastro_rezept_alter:()=>genGastroHL("rezept_alter"),
  hl_gastro_alkoholgehalt:()=>genGastroHL("alkoholgehalt"),
  hl_gastro_zutaten_anzahl:()=>genGastroHL("zutaten_anzahl"),
  hl_gastro_schmelzpunkt:()=>genGastroHL("schmelzpunkt"),
  hl_gastro_prokopf_verbrauch:()=>genGastroHL("prokopf_verbrauch"),
  hl_gastro_haltbarkeit:()=>genGastroHL("haltbarkeit"),
  hl_gastro_rekord_gewicht:()=>genGastroHL("rekord_gewicht"),
  uk_gastro_hausmannskost:()=>genGastroMatchQ("hausmannskost"),
  uk_gastro_kuechengeraete:()=>genGastroMatchQ("kuechengeraete"),
  uk_gastro_schnitttechniken:()=>genGastroMatchQ("schnitttechniken"),
  uk_gastro_originalrezept:()=>genGastroMatchQ("originalrezept"),
  uk_gastro_teigtaschen:()=>genGastroMatchQ("teigtaschen"),
  uk_gastro_gewuerzmischungen:()=>genGastroMatchQ("gewuerzmischungen"),
  uk_gastro_fleisch_cuts:()=>genGastroMatchQ("fleisch_cuts"),
  uk_gastro_bakterien_pilze:()=>genGastroMatchQ("bakterien_pilze"),
  uk_gastro_kaffeespezialitaeten:()=>genGastroMatchQ("kaffeespezialitaeten"),
  uk_gastro_pasta_formen:()=>genGastroMatchQ("pasta_formen"),
  uk_gastro_exotische_fruechte:()=>genGastroMatchQ("exotische_fruechte"),
  uk_gastro_brotsorten:()=>genGastroMatchQ("brotsorten"),
  uk_gastro_vegan_alternativen:()=>genGastroMatchQ("vegan_alternativen"),
  uk_gastro_fruehstueck_welt:()=>genGastroMatchQ("fruehstueck_welt"),
  uk_gastro_fachbegriffe_herd:()=>genGastroMatchQ("fachbegriffe_herd"),
  uk_gastro_sushi_arten:()=>genGastroMatchQ("sushi_arten"),
  uk_gastro_ess_etikette:()=>genGastroMatchQ("ess_etikette"),
  uk_gastro_tabus:()=>genGastroMatchQ("tabus"),
  uk_gastro_film_food:()=>genGastroMatchQ("film_food"),
  uk_gastro_seidenstrasse:()=>genGastroMatchQ("seidenstrasse"),
  ws_gastro_zitruspresse:()=>{initGastroWS("zitruspresse");return null;},
  ws_gastro_kuechenmaschine:()=>{initGastroWS("kuechenmaschine");return null;},
  ws_gastro_sauerteigbrot:()=>{initGastroWS("sauerteigbrot");return null;},
  ws_gastro_fermentation:()=>{initGastroWS("fermentation");return null;},
  ws_gastro_wurzelgemuese:()=>{initGastroWS("wurzelgemuese");return null;},
  ws_gastro_schwarzwaelder:()=>{initGastroWS("schwarzwaelder");return null;},
  ws_gastro_kaltentsafter:()=>{initGastroWS("kaltentsafter");return null;},
  uk_surf_spots:()=>genUniversalPinQ("surf_spots"),"""
assert c.count(OLD_G) == 1, f"Anchor not unique: {OLD_G[:80]!r}"
c = c.replace(OLD_G, NEW_G)
print("[OK]   G done")

# ── Write out ─────────────────────────────────────────────────────────────────
print("[229] Writing gen.py ...")
with open(GEN, 'w', encoding='utf-8') as f:
    f.write(c)
print(f"[229] gen.py written: {len(c)} bytes")
print("[229] Patch 229 complete!")
