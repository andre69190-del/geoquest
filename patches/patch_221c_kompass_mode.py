#!/usr/bin/env python3
# Phase 221 Feature 3: Sonnen-Kompass — neuer Spielmodus

import sys
path = "/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. MODES entry (after sunrise_guesser entry) ───────────────────────────
OLD_MODES = '  {id:"sunrise_guesser",     icon:"\\u{1F305}",    title:"Fr\\u00fchere Sonne?",       group:"airports",prompt:"In welcher Stadt geht die Sonne fr\\u00fcher auf?",desc:"L\\u00e4ngsgrad = Sonnenaufgang"},'
NEW_MODES = (
    '  {id:"sunrise_guesser",     icon:"\\u{1F305}",    title:"Fr\\u00fchere Sonne?",       group:"airports",prompt:"In welcher Stadt geht die Sonne fr\\u00fcher auf?",desc:"L\\u00e4ngsgrad = Sonnenaufgang"},\n'
    '  {id:"sonnen_kompass",      icon:"\\u{1F9ED}",    title:"Sonnen-Kompass",             group:"airports",prompt:"Wohin geht die Sonne unter?",                    desc:"Sonnenuntergangs-Richtung nach Datum & Breitengrad"},'
)
if OLD_MODES not in content:
    print("ERROR: MODES sunrise_guesser entry not found")
    sys.exit(1)
content = content.replace(OLD_MODES, NEW_MODES, 1)
print("OK: MODES entry added")

# ── 2. MODE_CATS airports — prepend sonnen_kompass ─────────────────────────
OLD_CATS = '"sunrise_guesser","aequator_magnet"'
NEW_CATS = '"sunrise_guesser","sonnen_kompass","aequator_magnet"'
if OLD_CATS not in content:
    print("ERROR: MODE_CATS airports sunrise_guesser not found")
    sys.exit(1)
content = content.replace(OLD_CATS, NEW_CATS, 1)
print("OK: MODE_CATS entry added")

# ── 3. Data + generator after genSunriseGuesserQ ──────────────────────────
OLD_GEN = '/* -- Phase 204: aequator_magnet -------------------------------------------- */'
NEW_GEN = '''\
/* -- Phase 221: SONNEN_KOMPASS_DATA -- 40 cities lat/lng for sunset quiz -- */
const SONNEN_KOMPASS_DATA=[
  {n:"Oslo",c:"NO",lat:59.9,lng:10.7},{n:"Helsinki",c:"FI",lat:60.2,lng:24.9},
  {n:"Stockholm",c:"SE",lat:59.3,lng:18.1},{n:"Tromso",c:"NO",lat:69.7,lng:18.9},
  {n:"Reykjavik",c:"IS",lat:64.1,lng:-21.9},{n:"London",c:"GB",lat:51.5,lng:-0.1},
  {n:"Berlin",c:"DE",lat:52.5,lng:13.4},{n:"Paris",c:"FR",lat:48.9,lng:2.4},
  {n:"Madrid",c:"ES",lat:40.4,lng:-3.7},{n:"Lissabon",c:"PT",lat:38.7,lng:-9.1},
  {n:"Athen",c:"GR",lat:37.9,lng:23.7},{n:"Rom",c:"IT",lat:41.9,lng:12.5},
  {n:"Warschau",c:"PL",lat:52.2,lng:21.0},{n:"Moskau",c:"RU",lat:55.8,lng:37.6},
  {n:"Istanbul",c:"TR",lat:41.0,lng:28.9},{n:"Kairo",c:"EG",lat:30.1,lng:31.2},
  {n:"Nairobi",c:"KE",lat:-1.3,lng:36.8},{n:"Lagos",c:"NG",lat:6.5,lng:3.4},
  {n:"Casablanca",c:"MA",lat:33.6,lng:-7.6},{n:"Kapstadt",c:"ZA",lat:-33.9,lng:18.4},
  {n:"Johannesburg",c:"ZA",lat:-26.2,lng:28.0},{n:"Daressalam",c:"TZ",lat:-6.8,lng:39.3},
  {n:"Mumbai",c:"IN",lat:19.1,lng:72.9},{n:"Neu-Delhi",c:"IN",lat:28.6,lng:77.2},
  {n:"Peking",c:"CN",lat:39.9,lng:116.4},{n:"Shanghai",c:"CN",lat:31.2,lng:121.5},
  {n:"Tokio",c:"JP",lat:35.7,lng:139.7},{n:"Bangkok",c:"TH",lat:13.8,lng:100.5},
  {n:"Singapur",c:"SG",lat:1.3,lng:103.8},{n:"Jakarta",c:"ID",lat:-6.2,lng:106.8},
  {n:"Sydney",c:"AU",lat:-33.9,lng:151.2},{n:"Melbourne",c:"AU",lat:-37.8,lng:145.0},
  {n:"Auckland",c:"NZ",lat:-36.9,lng:174.8},{n:"New York",c:"US",lat:40.7,lng:-74.0},
  {n:"Los Angeles",c:"US",lat:34.1,lng:-118.2},{n:"Chicago",c:"US",lat:41.9,lng:-87.6},
  {n:"Mexiko-Stadt",c:"MX",lat:19.4,lng:-99.1},{n:"Sao Paulo",c:"BR",lat:-23.5,lng:-46.6},
  {n:"Buenos Aires",c:"AR",lat:-34.6,lng:-58.4},{n:"Lima",c:"PE",lat:-12.1,lng:-77.0}
];
/* genSonnenKompassQ: sunset direction quiz based on solar declination */
function genSonnenKompassQ(){
  const SK=SONNEN_KOMPASS_DATA;if(!SK||!SK.length)return null;
  const DATES=[
    {label:"21. März",doy:80},{label:"21. Juni",doy:172},
    {label:"23. September",doy:266},{label:"21. Dezember",doy:355},
    {label:"21. April",doy:111},{label:"21. Oktober",doy:294},
    {label:"21. Mai",doy:141},{label:"21. November",doy:325}
  ];
  for(var _try=0;_try<30;_try++){
    var item=SK[~~(rng()*SK.length)];
    var scene=DATES[~~(rng()*DATES.length)];
    var lat=item.lat;
    var latRad=lat*Math.PI/180;
    /* Spencer (1971) declination */
    var B=2*Math.PI*(scene.doy-1)/365;
    var decl=(180/Math.PI)*(0.006918-0.399912*Math.cos(B)+0.070257*Math.sin(B)-0.006758*Math.cos(2*B)+0.000907*Math.sin(2*B)-0.002697*Math.cos(3*B)+0.00148*Math.sin(3*B));
    var declRad=decl*Math.PI/180;
    var cosAz=Math.sin(declRad)/Math.cos(latRad);
    if(Math.abs(cosAz)>=1)continue;/* polar skip */
    var azRise=Math.acos(cosAz)*180/Math.PI;
    var azSet=Math.round(360-azRise);
    var dir;
    if(azSet>=265&&azSet<=275)dir="Westen";
    else if(azSet>275&&azSet<=340)dir="Nordwesten";
    else if(azSet>340)dir="Norden";
    else if(azSet>=220&&azSet<265)dir="Südwesten";
    else dir="Süden";
    var allDirs=["Nordwesten","Westen","Südwesten","Süden","Norden"];
    var wrongs=allDirs.filter(function(d){return d!==dir;}).sort(function(){return rng()-.5;}).slice(0,3);
    var opts=[dir].concat(wrongs).sort(function(){return rng()-.5;});
    var latStr=(Math.abs(lat).toFixed(1)+"°")+(lat>=0?"N":"S");
    return{
      type:"sonnen_kompass",
      prompt:"Am <b>"+scene.label+"</b> — wo geht die Sonne in <b>"+esc(item.n)+"</b> ("+latStr+") ungefähr unter?",
      subj:item.n,
      opts:opts,
      ans:dir,
      meta:"☀️ Azimut "+azSet+"° vom Norden (Westen=270°)",
      lid:"sk_"+item.n+"_"+scene.doy,
      cc:item.c
    };
  }
  return null;
}

/* -- Phase 204: aequator_magnet -------------------------------------------- */'''

if OLD_GEN not in content:
    print("ERROR: aequator_magnet comment not found for data insertion")
    sys.exit(1)
content = content.replace(OLD_GEN, NEW_GEN, 1)
print("OK: SONNEN_KOMPASS_DATA + genSonnenKompassQ inserted")

# ── 4. Dispatch table ──────────────────────────────────────────────────────
OLD_DISPATCH = '  sunrise_guesser:genSunriseGuesserQ,'
NEW_DISPATCH = '  sunrise_guesser:genSunriseGuesserQ,\n  sonnen_kompass:genSonnenKompassQ,'
if OLD_DISPATCH not in content:
    print("ERROR: dispatch sunrise_guesser not found")
    sys.exit(1)
content = content.replace(OLD_DISPATCH, NEW_DISPATCH, 1)
print("OK: Dispatch entry added")

# ── 5. qBody render case ──────────────────────────────────────────────────
# The generic else-branch already handles q.prompt + q.subj + q.meta
# But let's add a dedicated case for a nicer compass emoji display
OLD_QBODY = '}else{\n    qBody=`<div class="qprompt">${q.prompt}</div><div class="qmain">${q.subj}</div>${sel!==null?`<div class="qmeta">${q.meta||""}</div>`:""}`;'
NEW_QBODY = (
    '}else if(q.type==="sonnen_kompass"){\n'
    '    qBody=`<div class="qprompt">${q.prompt}</div>`+'
    '`<div style="text-align:center;font-size:2.8rem;margin:8px 0 4px">\\u{1F9ED}</div>`+'
    '`${sel!==null?\'<div class="qmeta" style="text-align:center;font-size:.77rem;color:var(--text3);margin-top:4px">\'+esc(q.meta||"")+\'</div>\':\'\'}`;'
    '\n  }else{\n'
    '    qBody=`<div class="qprompt">${q.prompt}</div><div class="qmain">${q.subj}</div>${sel!==null?`<div class="qmeta">${q.meta||""}</div>`:""}`;'
)
if OLD_QBODY not in content:
    print("WARNING: qBody generic else not found — using fallback (generic render still works)")
else:
    content = content.replace(OLD_QBODY, NEW_QBODY, 1)
    print("OK: qBody render case added")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("DONE: Phase 221 Feature 3 — Sonnen-Kompass complete")
