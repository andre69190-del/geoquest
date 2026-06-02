"""
Phase 413 — Regionale Kultur & Kulinarik (D-A-CH)
- data/regional_extended.json (30 Einträge, bereits erstellt)
- validate_content.py: check_regional_extended()
- gen.py:
    - Python-Loader + PLACEHOLDER_REGIONAL
    - const REGIONAL_DATA=PLACEHOLDER_REGIONAL
    - Neue Kategorie "regional" in MODE_CATS
    - 6 MODES: regional_pin, match_regional_kategorie, match_regional_land,
               match_regional_region, hl_regional_alkohol, hl_regional_saison
    - Generatoren: genRegionalPinQ, genRegionalMatchQ, genRegionalHLQ
    - i18n DE/EN/PL
    - Replace-Chain
"""
import os, json, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def r(p): return open(p,'r',encoding='utf-8').read()
def w(p,c): open(p,'w',encoding='utf-8').write(c)
def rpl(c, old, new, label):
    assert c.count(old)==1, f"ANCHOR {c.count(old)}x: {label!r}"
    return c.replace(old, new)

# ─────────────────────────────────────────────────────────────────────────
# 1. validate_content.py
# ─────────────────────────────────────────────────────────────────────────
vc = r(os.path.join(ROOT,'validate_content.py'))

CHECK_REGIONAL = '''
def check_regional_extended(filename, data):
    REQUIRED = ["kategorie","land","region","ort","lat","lng",
                "saison_start_monat","basis_zutat","alkoholgehalt","brauchtum_monat"]
    KAT  = {"Speise","Getränk","Wein","Brauchtum"}
    LAND = {"Deutschland","Österreich","Schweiz"}
    for name, entry in data.items():
        for f in REQUIRED:
            if f not in entry:
                warn(filename, name, f, "Pflichtfeld fehlt")
        k = entry.get("kategorie")
        if k and k not in KAT:
            warn(filename, name, "kategorie", f"Unbekannte kategorie: {k!r}")
        l = entry.get("land")
        if l and l not in LAND:
            warn(filename, name, "land", f"Unbekanntes land: {l!r}")
        m = entry.get("saison_start_monat")
        if m is not None and not (1 <= m <= 12):
            warn(filename, name, "saison_start_monat", f"Außerhalb 1-12: {m}")
        bm = entry.get("brauchtum_monat")
        if k == "Brauchtum" and bm is None:
            warn(filename, name, "brauchtum_monat", "Brauchtum braucht brauchtum_monat")
        lat = entry.get("lat",0)
        lng = entry.get("lng",0)
        if lat == 0.0 or lng == 0.0:
            warn(filename, name, "lat/lng", "Koordinaten sind 0.0")

'''

vc = rpl(vc,
    "def check_konsolen(filename, data):",
    CHECK_REGIONAL + "def check_konsolen(filename, data):",
    "check_regional_extended insertion")

vc = rpl(vc,
    '    elif name == "konsolen.json":\n        check_konsolen(filename, data)',
    '    elif name == "konsolen.json":\n        check_konsolen(filename, data)\n'
    '    elif name == "regional_extended.json":\n        check_regional_extended(filename, data)',
    "regional elif call")

w(os.path.join(ROOT,'validate_content.py'), vc)
print("OK 1: validate_content.py (check_regional_extended)")

# ─────────────────────────────────────────────────────────────────────────
# 2. gen.py
# ─────────────────────────────────────────────────────────────────────────
c = r(os.path.join(ROOT,'gen.py'))

# 2a. Python loader
c = rpl(c,
    "with open(os.path.join(os.path.dirname(__file__), 'data/games_extended.json'), 'r', encoding='utf-8') as _gf:",
    "with open(os.path.join(os.path.dirname(__file__), 'data/regional_extended.json'), 'r', encoding='utf-8') as _rf:\n"
    "        REGIONAL_J = __import__('json').dumps(__import__('json').load(_rf), ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/games_extended.json'), 'r', encoding='utf-8') as _gf:",
    "py loader regional")

# 2b. JS constant
c = rpl(c,
    "const KONSOLEN_DATA=PLACEHOLDER_KONSOLEN;\n",
    "const KONSOLEN_DATA=PLACEHOLDER_KONSOLEN;\nconst REGIONAL_DATA=PLACEHOLDER_REGIONAL;\n",
    "js const REGIONAL_DATA")

# 2c. MODE_CATS — new category before closing };
c = rpl(c,
    'generationen_match"],cost:0},\n};',
    'generationen_match"],cost:0},\n'
    '  regional:{label:"Regionale Kultur & Kulinarik",icon:"\\u{1F35E}",modes:['
    '"regional_pin","match_regional_kategorie","match_regional_land",'
    '"match_regional_region","hl_regional_alkohol","hl_regional_saison"],cost:0},\n};',
    "regional MODE_CATS")

# 2d. MODES entries — insert before uk_hafen_world
NEW_MODES = (
    '\n    {id:"regional_pin",'
    'icon:"\\u{1F35E}",'
    'title:"Regionale Kultur: Heimat-Pin",'
    'group:"regional",'
    'prompt:"Wo ist diese Spezialit\\u00e4t oder dieses Fest zuhause?",'
    'desc:"D-A-CH Spezialit\\u00e4ten, Weine und Br\\u00e4uche auf der Karte pinnen.",'
    'prompt_en:"Where is this speciality or festival at home?"},'
    '\n    {id:"match_regional_kategorie",'
    'icon:"\\u{1F4CB}",'
    'title:"Regionale Kultur: Kategorie",'
    'group:"regional",'
    'prompt:"Was ist das \\u2014 Speise, Getr\\u00e4nk, Wein oder Brauchtum?",'
    'desc:"Speise, Getr\\u00e4nk, Wein oder Brauchtum?",'
    'prompt_en:"What is it \\u2014 food, drink, wine or tradition?"},'
    '\n    {id:"match_regional_land",'
    'icon:"\\u{1F1E9}\\u{1F1EA}",'
    'title:"Regionale Kultur: Land",'
    'group:"regional",'
    'prompt:"Aus welchem D-A-CH-Land stammt das?",'
    'desc:"Deutschland, \\u00d6sterreich oder Schweiz?",'
    'prompt_en:"From which D-A-CH country does this come?"},'
    '\n    {id:"match_regional_region",'
    'icon:"\\u{1F5FA}\\uFE0F",'
    'title:"Regionale Kultur: Region",'
    'group:"regional",'
    'prompt:"Aus welcher Region stammt diese Spezialit\\u00e4t?",'
    'desc:"Bayern, Schwaben, Wallis, Tirol \\u2014 welche Region passt?",'
    'prompt_en:"From which region does this speciality come?"},'
    '\n    {id:"hl_regional_alkohol",'
    'icon:"\\u{1F37A}",'
    'title:"Regionale Kultur: Alkoholgehalt",'
    'group:"regional",'
    'prompt:"Welches Getr\\u00e4nk hat mehr Alkohol?",'
    'desc:"In Volumenprozent \\u2014 von 0 bis \\u00fcber 13 %.",'
    'prompt_en:"Which drink has a higher alcohol content?"},'
    '\n    {id:"hl_regional_saison",'
    'icon:"\\u{1F4C5}",'
    'title:"Regionale Kultur: Saison",'
    'group:"regional",'
    'prompt:"Was hat den sp\\u00e4teren Saisonstart (h\\u00f6herer Monat)?",'
    'desc:"Monat 1 = Januar, Monat 12 = Dezember.",'
    'prompt_en:"Which has the later season start (higher month number)?"},'
)
c = rpl(c,
    '\n\n    {id:"uk_hafen_world"',
    NEW_MODES + '\n\n    {id:"uk_hafen_world"',
    "regional MODES entries")

# 2e. Generator functions
GEN_REGIONAL = r"""
/* Phase 413: Regionale Kultur & Kulinarik Generatoren */
function genRegionalPinQ(){
  var _RD=REGIONAL_DATA;
  var keys=Object.keys(_RD).filter(function(k){return Object.prototype.hasOwnProperty.call(_RD,k)});
  if(keys.length<4)return null;
  var idx=~~(rng()*keys.length);
  var name=keys[idx];
  var entry=_RD[name];
  if(!entry.lat||!entry.lng)return null;
  return{type:"uk_pin",cat:"regional",
    prompt:_tc("Wo ist diese Spezialität oder dieses Fest zuhause?"),
    subj:name,targetLat:entry.lat,targetLng:entry.lng,ans:entry.ort,
    lid:"rpin_"+idx,cc:null};
}
function genRegionalMatchQ(field,prompt,fixedPool){
  var _RD=REGIONAL_DATA;
  var valid=Object.keys(_RD).filter(function(k){
    return Object.prototype.hasOwnProperty.call(_RD,k)&&_RD[k][field]!==null&&_RD[k][field]!==undefined;
  });
  if(valid.length<4)return null;
  var idx=~~(rng()*valid.length);
  var name=valid[idx];
  var correct=String(_RD[name][field]);
  var pool=fixedPool
    ?fixedPool.filter(function(v){return v!==correct;})
    :valid.map(function(n){return String(_RD[n][field]);}).filter(function(v,i,a){return a.indexOf(v)===i;}).filter(function(v){return v!==correct;});
  if(pool.length<3)return null;
  var p=pool.slice();
  for(var j=p.length-1;j>0;j--){var k=~~(rng()*(j+1));var t=p[j];p[j]=p[k];p[k]=t;}
  var dis=p.slice(0,3);
  var opts=[correct].concat(dis);
  for(var j2=opts.length-1;j2>0;j2--){var k2=~~(rng()*(j2+1));var t2=opts[j2];opts[j2]=opts[k2];opts[k2]=t2;}
  return{type:"uk_match",prompt:prompt||"Welche Eigenschaft?",
    subj:name,ans:correct,opts:opts,lid:"rmatch_"+field+"_"+idx,cc:"de"};
}
function genRegionalHLQ(field,opts){
  var o=opts||{};
  var items=[];
  var _RD=REGIONAL_DATA;
  var _ks=Object.keys(_RD).filter(function(k){return Object.prototype.hasOwnProperty.call(_RD,k);});
  for(var _i=0;_i<_ks.length;_i++){
    var _n=_ks[_i];
    var _v=+(_RD[_n][field]);
    if(isNaN(_v)||_v<=0)continue;
    items.push({name:_n,val:_v});
  }
  if(items.length<4)return null;
  items.sort(function(a,b){return a.val-b.val;});
  var len=items.length;
  var tries=0;
  while(tries++<40){
    var ai=~~(rng()*len);
    var W=Math.max(1,Math.floor(len*(S.diff==='hardcore'?0.04:0.15)));
    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);
    var pool=[];
    for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}
    if(!pool.length)continue;
    var bi=pool[~~(rng()*pool.length)];
    var a=items[ai],b=items[bi];
    if(a.val===b.val)continue;
    var winner=o.lowerWins?(a.val<b.val?a:b):(a.val>b.val?a:b);
    var unit=o.unit||"";
    var meta=a.name+": "+a.val+(unit?" "+unit:"")+" · "+b.name+": "+b.val+(unit?" "+unit:"");
    return{type:"beta_hl",prompt:o.prompt||"Welches ist höher?",subj:"",
      opts:[a.name,b.name],ans:winner.name,meta:meta,
      lid:"rhl_"+field+"_"+ai+"_"+bi,cc:"de"};
  }
  return null;
}
"""
c = rpl(c,
    "/* === Phase 228: Pflanzen-Generatoren === */",
    GEN_REGIONAL + "/* === Phase 228: Pflanzen-Generatoren === */",
    "regional gen fns")

# 2f. Dispatch
DISPATCH = (
    '  regional_pin:()=>genRegionalPinQ(),\n'
    '  match_regional_kategorie:()=>genRegionalMatchQ("kategorie",'
    '_tc("Was ist das — Speise, Getränk, Wein oder Brauchtum?"),'
    '["Speise","Getränk","Wein","Brauchtum"]),\n'
    '  match_regional_land:()=>genRegionalMatchQ("land",'
    '_tc("Aus welchem D-A-CH-Land stammt das?"),'
    '["Deutschland","Österreich","Schweiz"]),\n'
    '  match_regional_region:()=>genRegionalMatchQ("region",'
    '_tc("Aus welcher Region stammt diese Spezialität?")),\n'
    '  hl_regional_alkohol:()=>genRegionalHLQ("alkoholgehalt",{unit:"%vol",'
    'prompt:_tc("Welches Getränk hat mehr Alkohol?")}),\n'
    '  hl_regional_saison:()=>genRegionalHLQ("saison_start_monat",{unit:"Monat",'
    'prompt:_tc("Was hat den späteren Saisonstart?")}),\n'
)
c = rpl(c,
    '  match_konsolen_handheld:()=>genKonsolenHandheldQ(),\n',
    '  match_konsolen_handheld:()=>genKonsolenHandheldQ(),\n' + DISPATCH,
    "regional dispatch")

# 2g. i18n EN
EN = (
    '"Was ist das — Speise, Getränk, Wein oder Brauchtum?":'
    '"What is it — food, drink, wine or tradition?",'
    '"Aus welchem D-A-CH-Land stammt das?":"From which D-A-CH country does this come?",'
    '"Aus welcher Region stammt diese Spezialität?":"From which region does this speciality come?",'
    '"Welches Getränk hat mehr Alkohol?":"Which drink has a higher alcohol content?",'
    '"Was hat den späteren Saisonstart?":"Which has the later season start?",'
    '"Wo ist diese Spezialität oder dieses Fest zuhause?":"Where is this speciality or festival at home?",'
)
c = rpl(c,
    '"Welche Konsole hat mehr Einheiten verkauft?":"Which console sold more units?"',
    EN + '"Welche Konsole hat mehr Einheiten verkauft?":"Which console sold more units?"',
    "i18n EN regional")

# 2h. i18n PL
PL = (
    '"Was ist das — Speise, Getränk, Wein oder Brauchtum?":'
    '"Co to jest — potrawa, napój, wino czy tradycja?",'
    '"Aus welchem D-A-CH-Land stammt das?":"Z którego kraju D-A-CH pochodzi?",'
    '"Aus welcher Region stammt diese Spezialität?":"Z którego regionu pochodzi ta specjałność?",'
    '"Welches Getränk hat mehr Alkohol?":"Który napój ma więcej alkoholu?",'
    '"Was hat den späteren Saisonstart?":"Co ma późniejszy początek sezonu?",'
    '"Wo ist diese Spezialität oder dieses Fest zuhause?":"Gdzie jest dom tej specjałności lub festiwalu?",'
)
c = rpl(c,
    '"Welche Konsole hat mehr Einheiten verkauft?":"Która konsola sprzedała się w większej liczbie egzemplarzy?"',
    PL + '"Welche Konsole hat mehr Einheiten verkauft?":"Która konsola sprzedała się w większej liczbie egzemplarzy?"',
    "i18n PL regional")

# 2i. Replace chain
c = rpl(c,
    ".replace('PLACEHOLDER_KONSOLEN',         KONSOLEN_J)",
    ".replace('PLACEHOLDER_REGIONAL',         REGIONAL_J)\n  .replace('PLACEHOLDER_KONSOLEN',         KONSOLEN_J)",
    "replace chain regional")

w(os.path.join(ROOT,'gen.py'), c)
print("OK 2: gen.py (9 Patches)")
