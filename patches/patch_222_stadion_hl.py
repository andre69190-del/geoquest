#!/usr/bin/env python3
import sys

path = "/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

errors = []

# ─── FIX 1: getSmartMatch dynamic windowing ───────────────────────────────────
OLD1 = "  var W=Math.max(2,Math.min(5,Math.floor(sorted.length/5)));"
NEW1 = "  var W=Math.max(1,Math.floor(sorted.length*0.1)); /* Phase 222: 10% window */"

if OLD1 not in content:
    errors.append("FIX1: windowing pattern not found!")
else:
    content = content.replace(OLD1, NEW1, 1)
    print("OK FIX1: getSmartMatch windowing → 10% of array size")

# ─── FIX 2: Insert STADION_HOEHE_DATA + genStadionHoeheQ before genBetaHL ─────
# Target insertion point: the comment for genBetaHL
STADION_INSERT_AFTER = "/* Phase 166: genBetaHL */"

STADION_BLOCK = r"""/* Phase 222: Stadium Altitude dataset + dynamic proximity generator */
const STADION_HOEHE_DATA=[
  {name:"Hernando Siles (La Paz)",alt:3637,cc:"bo"},
  {name:"El Campín (Bogotá)",alt:2600,cc:"co"},
  {name:"Azteca (Mexiko-Stadt)",alt:2210,cc:"mx"},
  {name:"Olímpico Universitario (Mexiko-Stadt)",alt:2240,cc:"mx"},
  {name:"FNB Stadium (Johannesburg)",alt:1753,cc:"za"},
  {name:"Loftus Versfeld (Pretoria)",alt:1344,cc:"za"},
  {name:"Mané Garrincha (Brasília)",alt:1172,cc:"br"},
  {name:"Morumbi (São Paulo)",alt:760,cc:"br"},
  {name:"Stade de Suisse (Bern)",alt:572,cc:"ch"},
  {name:"Monumental (Santiago de Chile)",alt:567,cc:"cl"},
  {name:"Allianz Arena (München)",alt:517,cc:"de"},
  {name:"Türk Telekom Stadyum (Istanbul)",alt:212,cc:"tr"},
  {name:"Estadio Nacional (Lima)",alt:154,cc:"pe"},
  {name:"Luzhniki (Moskau)",alt:145,cc:"ru"},
  {name:"San Siro (Mailand)",alt:121,cc:"it"},
  {name:"Signal Iduna Park (Dortmund)",alt:86,cc:"de"},
  {name:"Camp Nou (Barcelona)",alt:57,cc:"es"},
  {name:"Olympiastadion (Berlin)",alt:37,cc:"de"},
  {name:"Wembley (London)",alt:35,cc:"gb"},
  {name:"Anfield (Liverpool)",alt:26,cc:"gb"},
  {name:"Maracanã (Rio de Janeiro)",alt:11,cc:"br"},
  {name:"Monumental (Buenos Aires)",alt:9,cc:"ar"}
];
function genStadionHoeheQ(){
  if(!STADION_HOEHE_DATA||STADION_HOEHE_DATA.length<2)return null;
  var sorted=STADION_HOEHE_DATA.slice().sort(function(a,b){return a.alt-b.alt;});
  var tries=0;
  while(tries++<40){
    var ai=~~(rng()*sorted.length);
    var W=Math.max(1,Math.floor(sorted.length*0.1));
    var lo=Math.max(0,ai-W),hi=Math.min(sorted.length-1,ai+W);
    var pool=sorted.slice(lo,hi+1).filter(function(x){return x!==sorted[ai];});
    if(!pool.length)continue;
    var b=pool[~~(rng()*pool.length)];
    var a=sorted[ai];
    if(a.alt===b.alt)continue;
    var higher=a.alt>b.alt?a:b;
    var lower=a.alt>b.alt?b:a;
    var diff=higher.alt-lower.alt;
    if(diff<30)continue; /* skip nearly-identical altitudes */
    var meta=a.name+": "+a.alt+" m · "+b.name+": "+b.alt+" m";
    return{type:"beta_hl",prompt:"Welches Stadion liegt höher über dem Meeresspiegel?",subj:"",opts:[a.name,b.name],ans:higher.name,meta:meta,lid:"stadion_hoehe",cc:higher.cc||"de"};
  }
  return null;
}
/* Phase 166: genBetaHL */"""

if STADION_INSERT_AFTER not in content:
    errors.append("FIX2: genBetaHL comment not found!")
else:
    content = content.replace(STADION_INSERT_AFTER, STADION_BLOCK, 1)
    print("OK FIX2: STADION_HOEHE_DATA + genStadionHoeheQ inserted before genBetaHL")

# ─── FIX 3: Remove old b7 hardcoded array ─────────────────────────────────────
OLD_B7 = """b7:[
  {nameA:"Hernando Siles (La Paz)",nameB:"Allianz Arena (München)",prompt:"Welches Stadion liegt höher über dem Meeresspiegel?",ans:"Hernando Siles (La Paz)",metaA:"3.637 m",metaB:"517 m"},
  {nameA:"Estadio Azteca (Mexiko-Stadt)",nameB:"Camp Nou (Barcelona)",prompt:"Welches Stadion liegt höher über dem Meeresspiegel?",ans:"Estadio Azteca (Mexiko-Stadt)",metaA:"2.210 m",metaB:"57 m"},
  {nameA:"Stade de Suisse (Bern)",nameB:"Anfield (Liverpool)",prompt:"Welches Stadion liegt höher über dem Meeresspiegel?",ans:"Stade de Suisse (Bern)",metaA:"572 m",metaB:"26 m"},
  {nameA:"Türk Telekom Stadyum (Istanbul)",nameB:"Wembley (London)",prompt:"Welches Stadion liegt höher über dem Meeresspiegel?",ans:"Türk Telekom Stadyum (Istanbul)",metaA:"212 m",metaB:"35 m"}
],"""
NEW_B7 = "/* b7 replaced by genStadionHoeheQ — see Phase 222 */"

if OLD_B7 not in content:
    errors.append("FIX3: b7 hardcoded array not found!")
else:
    content = content.replace(OLD_B7, NEW_B7, 1)
    print("OK FIX3: b7 hardcoded array removed")

# ─── FIX 4: Dispatch b7 → genStadionHoeheQ ────────────────────────────────────
OLD4 = "b6:()=>genBetaMCQ(6),b7:()=>genBetaHL(7),b9:()=>genBetaMCQ(9),"
NEW4 = "b6:()=>genBetaMCQ(6),b7:()=>genStadionHoeheQ(),b9:()=>genBetaMCQ(9),"

if OLD4 not in content:
    errors.append("FIX4: dispatch b7 pattern not found!")
else:
    content = content.replace(OLD4, NEW4, 1)
    print("OK FIX4: dispatch b7 → genStadionHoeheQ()")

if errors:
    print("\nERRORS:")
    for e in errors:
        print(" ", e)
    sys.exit(1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("\nAll 4 fixes applied successfully.")
