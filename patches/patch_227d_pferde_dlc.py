import sys
SRC = "/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py"
with open(SRC,"r",encoding="utf-8") as f: c=f.read()

# ── P1: MODE_CATS tiere — append 4 Pferde IDs ────────────────────────────────
a1 = '"hl_tiere_haustier_dichte"\n  ],cost:0},'
b1 = ('"hl_tiere_haustier_dichte",'
      '"uk_pferde_rassen","uk_pferde_fachbegriffe",'
      '"hl_pferde_stockmass","ws_pferde_fluesterer"\n  ],cost:0},')
assert a1 in c, "P1 not found: "+repr(a1[:80])
c = c.replace(a1, b1, 1); print("P1 done")

# ── P2: MODES entries — append 4 Pferde entries ──────────────────────────────
a2 = 'desc:"Rinder je 100 Einwohner \\u2014 Uruguay bis Japan"}\n];'
b2 = ('desc:"Rinder je 100 Einwohner \\u2014 Uruguay bis Japan"},\n'
      '    {id:"uk_pferde_rassen",icon:"\\u{1F40E}",title:"[BETA] Pferderassen",'
      'group:"tiere",prompt:"Wo wurde diese Pferderasse gez\\u00fcchtet?",'
      'desc:"Von Shire bis Lipizzaner \\u2014 Ursprungsorte der Rassen"},\n'
      '    {id:"uk_pferde_fachbegriffe",icon:"\\u{1F3A8}",title:"[BETA] Pferde-Fachbegriffe",'
      'group:"tiere",prompt:"Was bezeichnet dieser Fachbegriff beim Pferd?",'
      'desc:"Fellfarben und Reitlehre \\u2014 das Pferde-ABC"},\n'
      '    {id:"hl_pferde_stockmass",icon:"\\u{1F4CF}",title:"[BETA] H/L Stockma\\u00df",'
      'group:"tiere",prompt:"Welches Pferd hat ein gr\\u00f6\\u00dferes Stockma\\u00df?",'
      'desc:"Widerristhohe in cm \\u2014 Falabella bis Shire"},\n'
      '    {id:"ws_pferde_fluesterer",icon:"\\u{1F40E}",title:"[BETA] WS: Pferdefl\\u00fcsterer",'
      'group:"tiere",noMultiplayer:true,'
      'prompt:"Bilde W\\u00f6rter aus SHIREHORSE!",'
      'desc:"Anagramm-R\\u00e4tsel \\u2014 10 Buchstaben"}\n];')
assert a2 in c, "P2 not found: "+repr(a2[:80])
c = c.replace(a2, b2, 1); print("P2 done")

# ── P3: Pin data — insert uk_pferde_rassen before Phase 216 comment ──────────
a3 = 'Patagonien-Dino-Canyon",lat:-41.87,lng:-66.70}\n  ]},\n\n  /* === Phase 216: Match-Kategorien (Schritt 3) === */'
b3 = ('Patagonien-Dino-Canyon",lat:-41.87,lng:-66.70}\n  ]},\n\n'
      '  /* === Pferde-DLC: Pin-Daten (1 Modus) === */\n'
      '  pferde_rassen:{prompt:"Wo wurde diese Pferderasse gez\\u00fcchtet?",items:[\n'
      '    {n:"Shire",lat:52.50,lng:-1.50},{n:"Thoroughbred",lat:51.50,lng:-0.10},\n'
      '    {n:"Vollblutaraber",lat:24.00,lng:44.00},{n:"Andalusier",lat:37.80,lng:-5.00},\n'
      '    {n:"Friese",lat:53.10,lng:5.80},{n:"Lipizzaner",lat:45.80,lng:13.88},\n'
      '    {n:"Haflinger",lat:46.68,lng:11.16},{n:"Mustang",lat:39.00,lng:-105.00},\n'
      '    {n:"Appaloosa (Nez Perc\\u00e9)",lat:46.41,lng:-117.00},{n:"Trakehner",lat:54.70,lng:21.10},\n'
      '    {n:"Hannoveraner",lat:52.37,lng:9.73},{n:"Quarter Horse",lat:30.00,lng:-100.00},\n'
      '    {n:"Przewalski-Pferd",lat:47.00,lng:102.00},{n:"Islandpferd",lat:64.00,lng:-19.00},\n'
      '    {n:"Connemara-Pony",lat:53.40,lng:-9.90},{n:"Welsh Pony",lat:52.10,lng:-3.80},\n'
      '    {n:"Shetlandpony",lat:60.14,lng:-1.20},{n:"Clydesdale",lat:55.70,lng:-3.90},\n'
      '    {n:"Camargue-Pferd",lat:43.52,lng:4.56},{n:"Paint Horse",lat:35.50,lng:-97.50}\n'
      '  ]},\n\n'
      '  /* === Phase 216: Match-Kategorien (Schritt 3) === */')
assert a3 in c, "P3 not found: "+repr(a3[:80])
c = c.replace(a3, b3, 1); print("P3 done")

# ── P4: Match data — insert uk_pferde_fachbegriffe before genTiereMatchQ ─────
a4 = 'Okavango-Linyanti-Zyklus"}\n  ]},\n  /* === Phase 227 Part 2: genTiereMatchQ'
b4 = ('Okavango-Linyanti-Zyklus"}\n  ]},\n'
      '  pferde_fachbegriffe:{prompt:"Was bezeichnet dieser Fachbegriff beim Pferd?",items:[\n'
      '    {n:"Rappe",c:"Komplett schwarzes Pferd"},{n:"Fuchs",c:"Rotbraunes Pferd"},\n'
      '    {n:"Schimmel",c:"Wei\\u00dfes oder grauwei\\u00dfes Pferd"},{n:"Brauner",c:"Dunkelbraunes Pferd"},\n'
      '    {n:"Falbe",c:"Sandfarben-graubraunes Pferd"},{n:"Isabelle",c:"Goldgelbes Pferd mit heller M\\u00e4hne"},\n'
      '    {n:"Schecke",c:"Zweifarbig geschecktes Pferd"},{n:"Tigerschecke",c:"Wei\\u00dfes Pferd mit dunklen Flecken"},\n'
      '    {n:"Stockma\\u00df",c:"K\\u00f6rpergr\\u00f6\\u00dfe am Widerrist gemessen"},{n:"Widerrist",c:"H\\u00f6chster Punkt am Pferder\\u00fccken"},\n'
      '    {n:"Blesse",c:"Wei\\u00dfer Streifen \\u00fcber die Pferdenase"},{n:"K\\u00f6tenbehang",c:"Langes Haar \\u00fcber dem Pferdehuf"},\n'
      '    {n:"Kanter",c:"Leichter, langsamer Galopp"},{n:"Piaffee",c:"Trabartiger Bewegung auf der Stelle"},\n'
      '    {n:"Passage",c:"Sehr getragener, federnder Trab"},{n:"Trense",c:"Leichtes Geb\\u00dft am Pferdegebiss"},\n'
      '    {n:"Kandare",c:"Strenges Geb\\u00dft mit zwei Geb\\u00dftst\\u00e4ngen"},{n:"Gurt",c:"Riemen zum Befestigen des Sattels"},\n'
      '    {n:"Streu",c:"Einstreumaterial im Pferdestall"},{n:"Halfter",c:"Kopfzeug ohne Geb\\u00dft"}\n'
      '  ]},\n'
      '  /* === Phase 227 Part 2: genTiereMatchQ')
assert a4 in c, "P4 not found: "+repr(a4[:80])
c = c.replace(a4, b4, 1); print("P4 done")

# ── P5: H/L pferde_stockmass into TIER_HL_DATA ───────────────────────────────
a5 = '  ]}\n};\n\n/* === Phase 227: genTiereHL'
b5 = ('  ]},\n'
      '  pferde_stockmass:{prompt:"Welches Pferd hat ein gr\\u00f6\\u00dferes Stockma\\u00df?",unit:"cm",items:[\n'
      '    {name:"Falabella",val:80},{name:"Shetlandpony",val:100},\n'
      '    {name:"Welsh Pony",val:122},{name:"Connemara-Pony",val:148},\n'
      '    {name:"Islandpferd",val:140},{name:"Haflinger",val:148},\n'
      '    {name:"Appaloosa",val:155},{name:"Quarter Horse",val:157},\n'
      '    {name:"Andalusier",val:160},{name:"Hannoveraner",val:165},\n'
      '    {name:"Trakehner",val:165},{name:"Vollblutaraber",val:160},\n'
      '    {name:"Thoroughbred",val:163},{name:"Friese",val:165},\n'
      '    {name:"Paint Horse",val:157},{name:"Camargue-Pferd",val:148},\n'
      '    {name:"Mustang",val:150},{name:"Lipizzaner",val:158},\n'
      '    {name:"Clydesdale",val:175},{name:"Shire",val:185}\n'
      '  ]}\n'
      '};\n\n/* === Phase 227: genTiereHL')
assert a5 in c, "P5 not found: "+repr(a5[:80])
c = c.replace(a5, b5, 1); print("P5 done")

# ── P6: WS Pferde-Flüsterer entry into TIER_WS_DATA ──────────────────────────
a6 = '"]}}\n};\nfunction initTierWortSchmiede'
b6 = ('"]}},\n'
      '  pferde_fluesterer:{word:"SHIREHORSE",validWords:{\n'
      '    de:["EHRE","EHER","ROSE","HOSE","REISE","RIESE","REIHE","SHIRE","SHORE",\n'
      '        "SERIE","SIRE","HIER","HEER","HERR","IRRE","SEHER","ESSER","EROS","HOSE"],\n'
      '    en:["HORSE","SHORE","ROSE","HOSE","HIRE","SIRE","SHEER","HEROES","SHOE",\n'
      '        "SHIRE","HERE","SERIES","HIRER","SHIRES","SHEERS","HEIR","HEIRS","HIRES","OSIER","ROSHI"]\n'
      '  }}\n'
      '};\nfunction initTierWortSchmiede')
assert a6 in c, "P6 not found: "+repr(a6[:80])
c = c.replace(a6, b6, 1); print("P6 done")

# ── P7: GEN dispatch ──────────────────────────────────────────────────────────
a7 = '  hl_tiere_haustier_dichte:()=>genTiereHL("haustier_dichte"),'
b7 = ('  hl_tiere_haustier_dichte:()=>genTiereHL("haustier_dichte"),\n'
      '  /* Pferde-DLC */\n'
      '  uk_pferde_rassen:()=>genUniversalPinQ("pferde_rassen"),\n'
      '  uk_pferde_fachbegriffe:()=>genTiereMatchQ("pferde_fachbegriffe"),\n'
      '  hl_pferde_stockmass:()=>genTiereHL("pferde_stockmass"),\n'
      '  ws_pferde_fluesterer:()=>{initTierWortSchmiede("pferde_fluesterer");return null;},')
assert a7 in c, "P7 not found: "+repr(a7[:80])
c = c.replace(a7, b7, 1); print("P7 done")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(c)
print("gen.py written OK — size:", len(c))