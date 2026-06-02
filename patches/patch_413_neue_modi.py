#!/usr/bin/env python3
"""Phase 413: 8 neue Spielmodi aus ungenutzten Datenfeldern"""
import sys, os
GEN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'gen.py')

with open(GEN, 'r', encoding='utf-8') as f:
    c = f.read()

def rep(old, new, label):
    n = c.count(old)
    assert n == 1, f'{label}: count={n}'
    return c.replace(old, new)

# ── 1. MODES: neue Konsolen-Modi nach hl_hw_units ───────────────────────────
ANCHOR1 = 'id:"hl_hw_units",icon:"\U0001F4B0"'
c = rep(ANCHOR1,
    ANCHOR1[:-1] + ''',title:"Hardware-Quartett: Verkaufszahlen",group:"hardware",prompt:"Welche Konsole verkaufte sich häufiger?",desc:"Von 0.3 Mio. (Odyssey) bis 155 Mio. (PS2)",prompt_en:"Which console sold more units?"},
    {id:"hl_konsolen_erscheinungsjahr",icon:"\u{1F4C5}",title:"Konsolen-Quartett: Erscheinungsjahr",group:"games",prompt:"Welche Konsole erschien später?",desc:"Von 1972 (Odyssey) bis 2020 — wann kam die Konsole?",prompt_en:"Which console was released later?"},
    {id:"hl_konsolen_eingestellt",icon:"⚰️",title:"Konsolen-Quartett: Produktionsende",group:"games",prompt:"Welche Konsole wurde später eingestellt?",desc:"Das offizielle Ende der Produktion — manche laufen jahrzehntelang.",prompt_en:"Which console was discontinued later?"},
    {id:"konsolen_match_spiel",icon:"\u{1F3AE}",title:"Konsolen-Quiz: Welche Konsole?",group:"games",prompt:"Für welche Konsole ist dieses Spiel bekannt?",desc:"89 Klassiker — erkenne die Heimkonsole anhand des Spiels.",prompt_en:"Which console is this game known for?"},
    {id:"konsolen_match_aufloesung",icon:"\u{1F5A5}️",title:"Konsolen-Quiz: Auflösung",group:"games",prompt:"Welche maximale Auflösung unterstützt diese Konsole?",desc:"Von 240p bis 4K — die Evolution der Grafik.",prompt_en:"What is the maximum resolution of this console?''',
    'MODES hw_units')

print('Step 1 OK')

# ── 2. MODES: neue Auto/Games-Modi nach auto_generationen_match ───────────────
ANCHOR2 = 'prompt_en:"When did this generation of the model line appear?"}'
c = rep(ANCHOR2, ANCHOR2 + ''',
    {id:"hl_auto_nordschleife",icon:"\u{1F3C1}",title:"Auto-Quartett: Nordschleife",group:"autos",prompt:"Wer war schneller auf der Nürburgring-Nordschleife?",desc:"Rundenzeiten in Sekunden — niedrigere Zeit gewinnt.",prompt_en:"Which car was faster at the Nürburgring Nordschleife?"},
    {id:"hl_auto_baujahr_ende",icon:"\u{1F4C5}",title:"Auto-Quartett: Produktionsende",group:"autos",prompt:"Welches Auto wurde später eingestellt?",desc:"Das Jahr, in dem das letzte Exemplar das Band verließ.",prompt_en:"Which car had a later production end year?"},
    {id:"games_match_publisher_land",icon:"\u{1F30D}",title:"Games: Publisher-Land",group:"games",prompt:"Aus welchem Land kommt der Publisher dieses Spiels?",desc:"Von den USA bis Finnland — wo sitzen die großen Publisher?",prompt_en:"Which country is this game\'s publisher from?"},
    {id:"hl_games_publisher_lng",icon:"\u{1F9ED}",title:"Games: Publisher — Wer liegt östlicher?",group:"games",prompt:"Welcher Publisher sitzt weiter östlich?",desc:"Vom Silicon Valley bis Tokio — Längengrade der Spielebranche.",prompt_en:"Which game publisher is located further east?"}''',
    'MODES auto_gen')

print('Step 2 OK')

# ── 3. MODE_CATS: neue Konsolen/Games-Modi ────────────────────────────────────
ANCHOR3 = '"hl_hw_year","hl_hw_units"]'
c = rep(ANCHOR3,
    '"hl_hw_year","hl_hw_units","hl_konsolen_erscheinungsjahr","hl_konsolen_eingestellt","konsolen_match_spiel","konsolen_match_aufloesung","games_match_publisher_land","hl_games_publisher_lng"]',
    'MODE_CATS games')

print('Step 3 OK')

# ── 4. MODE_CATS: neue Auto-Modi ──────────────────────────────────────────────
ANCHOR4 = '"auto_match_dekade","auto_generationen_match"]'
c = rep(ANCHOR4,
    '"auto_match_dekade","auto_generationen_match","hl_auto_nordschleife","hl_auto_baujahr_ende"]',
    'MODE_CATS autos')

print('Step 4 OK')

# ── 5. Generator genKonsolenSpielQ ────────────────────────────────────────────
ANCHOR5 = 'window.renderRecentBar=renderRecentBar;'
NEW_FN = r"""/* Phase 413: genKonsolenSpielQ -- Reverse: Spiel -> Konsole */
function genKonsolenSpielQ(){
  var _KD=KONSOLEN_DATA;
  var keys=Object.keys(_KD).filter(function(k){return Object.prototype.hasOwnProperty.call(_KD,k);});
  var pairs=[];
  for(var i=0;i<keys.length;i++){
    var cn=keys[i];
    var gs=_KD[cn].bekannteste_spiele;
    if(!gs||!gs.length)continue;
    for(var j=0;j<gs.length;j++){pairs.push({game:gs[j],console:cn});}
  }
  if(pairs.length<4)return null;
  var idx=~~(rng()*pairs.length);
  var correct=pairs[idx].console;
  var game=pairs[idx].game;
  var others=keys.filter(function(n){return n!==correct;});
  for(var k=others.length-1;k>0;k--){var t=~~(rng()*(k+1));var tmp=others[k];others[k]=others[t];others[t]=tmp;}
  if(others.length<3)return null;
  var opts=[correct].concat(others.slice(0,3));
  for(var m=opts.length-1;m>0;m--){var t2=~~(rng()*(m+1));var tmp2=opts[m];opts[m]=opts[t2];opts[t2]=tmp2;}
  return{type:"uk_match",prompt:_tc("Für welche Konsole ist dieses Spiel bekannt?"),
    subj:game,ans:correct,opts:opts,lid:"kspiel_"+idx,cc:"de"};
}
window.genKonsolenSpielQ=genKonsolenSpielQ;

""" + ANCHOR5
c = rep(ANCHOR5, NEW_FN, 'genKonsolenSpielQ fn')

print('Step 5 OK')

# ── 6. GEN-Dispatch ───────────────────────────────────────────────────────────
ANCHOR6 = 'match_konsolen_land:()=>genKonsolenMatch("herkunftsland",_tc("Aus welchem Land stammt diese Konsole?"),["Japan","USA"]),'
c = rep(ANCHOR6, ANCHOR6 + """
  hl_konsolen_erscheinungsjahr:()=>genKonsolenHL("erscheinungsjahr",{unit:"",prompt:_tc("Welche Konsole erschien später?")}),
  hl_konsolen_eingestellt:()=>genKonsolenHL("eingestellt_jahr",{unit:"",prompt:_tc("Welche Konsole wurde später eingestellt?")}),
  konsolen_match_spiel:()=>genKonsolenSpielQ(),
  konsolen_match_aufloesung:()=>genKonsolenMatch("aufloesung_max",_tc("Welche maximale Auflösung unterstützt diese Konsole?"),["240p","480i","480p","1080p","4K"]),
  hl_auto_nordschleife:()=>genAutosHLExt("nordschleife",{lowerWins:true,unit:"s",prompt:_tc("Wer war schneller auf der Nürburgring-Nordschleife?")}),
  hl_auto_baujahr_ende:()=>genAutosHLExt("baujahr_ende",{unit:"",prompt:_tc("Welches Auto wurde später eingestellt?")}),
  games_match_publisher_land:()=>genGamesMatchExt("publisher_land",_tc("Aus welchem Land kommt der Publisher?"),["Vereinigte Staaten","Japan","Finnland","China","Schweden","Frankreich","Vereinigtes Königreich","Polen","Kanada","Südkorea"]),
  hl_games_publisher_lng:()=>genGamesHLExt("publisher_lng",{unit:"°",prompt:_tc("Welcher Publisher sitzt weiter östlich?")}),""",
    'GEN dispatch')

print('Step 6 OK')

with open(GEN, 'w', encoding='utf-8') as f:
    f.write(c)

print('Patch 413 applied -- 8 neue Modi')
