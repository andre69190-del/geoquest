#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 442: Geo-Pin-Welle — 13 neue Pin-Modi für Hunde, Brettspiele, Robotik,
Serien, Musik, Webkultur, Literatur, Themeparks, Wirtschaft, Filme, Gaming-Hardware,
Konsolen, Gartenbau.

Neue MODES (13):
  hund_pin_land, boardgame_pin_land, robot_pin_land, serie_pin_land,
  musik_pin_land, web_pin_land, lit_pin_land, park_pin_land,
  eco_pin_land, film_pin_land, hw_pin_land, konsole_pin_land,
  garten_pin_region

Neue JS-Infrastruktur:
  LAND_LATLON  — Lookup-Tabelle DE-Ländername → {lat, lng}
  genExtPinByLand() — universeller Pin-Generator für _extended JSONs
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN  = os.path.join(ROOT, 'gen.py')


def patch(path, edits):
    c = open(path, 'r', encoding='utf-8').read()
    for old, new, tag in edits:
        n = c.count(old)
        assert n == 1, f'Anker "{tag}" count={n} (erwartet 1)'
        c = c.replace(old, new)
        print('  OK  ' + tag)
    open(path, 'w', encoding='utf-8').write(c)


# ─────────────────────────────────────────────────────────────────────────────
# 1. JS: LAND_LATLON Konstante + genExtPinByLand Helper
# ─────────────────────────────────────────────────────────────────────────────
CONST_OLD = 'const GARTEN_WS_DATA=PLACEHOLDER_GARTEN_WS;\nconst GARTEN_DATA=PLACEHOLDER_GARTEN;'
CONST_NEW = (
    'const GARTEN_WS_DATA=PLACEHOLDER_GARTEN_WS;\n'
    'const GARTEN_DATA=PLACEHOLDER_GARTEN;\n'
    '\n'
    '/* Phase 442: Ländername (DE) → Koordinaten */\n'
    'const LAND_LATLON={\n'
    '  "Deutschland":[51.165,10.451],"Vereinigte Staaten":[37.090,-95.712],\n'
    '  "USA":[37.090,-95.712],"Japan":[36.204,138.252],"Vereinigtes Königreich":[55.378,-3.435],\n'
    '  "Grossbritannien":[55.378,-3.435],"Frankreich":[46.227,2.213],"Schweden":[60.128,18.643],\n'
    '  "Italien":[41.871,12.567],"Schweiz":[46.818,8.227],"China":[35.861,104.195],\n'
    '  "Niederlande":[52.132,5.291],"Spanien":[40.463,-3.749],"Österreich":[47.516,14.550],\n'
    '  "Südkorea":[35.907,127.766],"Kanada":[56.130,-106.346],"Dänemark":[56.263,9.501],\n'
    '  "Polen":[51.919,19.145],"Belgien":[50.503,4.469],"Indien":[20.593,78.962],\n'
    '  "Mexiko":[23.634,-102.552],"Russland":[61.524,105.318],"Norwegen":[60.472,8.468],\n'
    '  "Australien":[-25.274,133.775],"Tschechien":[49.817,15.472],"Ungarn":[47.162,19.503],\n'
    '  "Kolumbien":[4.570,-74.297],"Neuseeland":[-40.900,174.885],"Irland":[53.412,-8.243],\n'
    '  "Südafrika":[-30.559,22.937],"Brasilien":[-14.235,-51.925],"Schottland":[56.490,-4.202],\n'
    '  "Island":[64.963,-19.020],"Vereinigte Arabische Emirate":[23.424,53.847],\n'
    '  "Malta":[35.937,14.375],"Finnland":[61.924,25.748],"Türkei":[38.963,35.243],\n'
    '  "Argentinien":[-38.416,-63.616],"Iran":[32.427,53.688],"Nigeria":[9.081,8.675],\n'
    '  "Estland":[58.595,25.013],"Kroatien":[45.100,15.200],"Wales":[52.130,-3.783],\n'
    '  "Kongo":[-4.038,21.758],"Simbabwe":[-19.015,29.154],"Kuba":[21.521,-77.781],\n'
    '  "Afghanistan":[33.939,67.709],"Uruguay":[-32.522,-55.765],"Portugal":[39.399,-8.224],\n'
    '  "Griechenland":[39.074,21.824],"Rumänien":[45.943,24.967],"Slowakei":[48.669,19.699],\n'
    '  "Litauen":[55.169,23.881],"Lettland":[56.879,24.604],"Slowenien":[46.151,14.995],\n'
    '  "Bulgarien":[42.733,25.485],"Serbien":[44.016,21.005],"Ukraine":[48.379,31.165],\n'
    '  "Israel":[31.046,34.851],"Ägypten":[26.820,30.802],"Taiwan":[23.697,120.960],\n'
    '  "Singapur":[1.352,103.819],"Thailand":[15.870,100.992],"Indonesien":[-0.789,113.921],\n'
    '  "Brasilien":[-14.235,-51.925],"Chile":[-35.675,-71.542],"Peru":[-9.189,-75.015],\n'
    '  "Europa":[54.526,15.255],"Ostasien":[35.0,115.0],"Südamerika":[-14.0,-51.0],\n'
    '  "Nordamerika":[48.0,-101.0],"Mittelamerika":[15.0,-90.0],"Mittelmeer":[40.0,18.0],\n'
    '  "Zentralasien":[45.0,65.0],"Asien":[30.0,90.0],"Amerika":[37.0,-95.0],\n'
    '  "Europa/Asien":[50.0,40.0],"Orient":[30.0,45.0],"Tibet":[29.65,91.12],\n'
    '  "Westafrika":[8.0,-2.0],"Ostafrika":[0.0,38.0],"Südostasien":[5.0,115.0],\n'
    '  "Naher Osten":[29.0,42.0],"Karibik":[18.0,-69.0],"Pazifik":[-15.0,-170.0]\n'
    '};\n'
)

GEN_FN_OLD = 'window.genGartenMatchExt=genGartenMatchExt;'
GEN_FN_NEW = (
    'window.genGartenMatchExt=genGartenMatchExt;\n'
    '\n'
    '/* Phase 442: Universeller Pin-Generator via LAND_LATLON */\n'
    'function genExtPinByLand(DATA,landField,cat,prompt,lidPrefix){\n'
    '  var keys=Object.keys(DATA).filter(function(k){\n'
    '    return Object.prototype.hasOwnProperty.call(DATA,k)&&DATA[k][landField]&&LAND_LATLON[DATA[k][landField]];\n'
    '  });\n'
    '  if(keys.length<4)return null;\n'
    '  var idx=~~(rng()*keys.length),name=keys[idx],e=DATA[name];\n'
    '  var ll=LAND_LATLON[e[landField]];\n'
    '  return{type:"uk_pin",cat:cat,prompt:prompt,subj:name,lat:ll[0],lng:ll[1],\n'
    '    lid:lidPrefix+"_"+idx,cc:"de"};\n'
    '}\n'
    'window.genExtPinByLand=genExtPinByLand;\n'
    '\n'
    '/* Phase 442: Literatur Pin (hat eigene lat/lng) */\n'
    'function genLitPinQ(){\n'
    '  var _LD=LIT_DATA;\n'
    '  var keys=Object.keys(_LD).filter(function(k){return Object.prototype.hasOwnProperty.call(_LD,k)&&_LD[k].lat&&_LD[k].lng;});\n'
    '  if(keys.length<4)return null;\n'
    '  var idx=~~(rng()*keys.length),name=keys[idx],e=_LD[name];\n'
    '  return{type:"uk_pin",cat:"literatur",prompt:_tc("Wo kommt dieses Buch / dieser Autor her?"),\n'
    '    subj:name,lat:e.lat,lng:e.lng,lid:"litpin_"+idx,cc:"de"};\n'
    '}\n'
    'window.genLitPinQ=genLitPinQ;'
)

# ─────────────────────────────────────────────────────────────────────────────
# 2. i18n PL — neue Strings anhängen
# ─────────────────────────────────────────────────────────────────────────────
I18N_PL_OLD = (
    '"Aus welcher Region stammt diese Sprache?":"Z jakiego regionu pochodzi ten język?"}'
    ',"en":{"Welche Serie'
)
I18N_PL_NEW = (
    '"Aus welcher Region stammt diese Sprache?":"Z jakiego regionu pochodzi ten język?",'
    '"Wo kommt diese Hunderasse her?":"Skąd pochodzi ta rasa psów?",'
    '"Wo kommt dieses Brettspiel her?":"Skąd pochodzi ta gra planszowa?",'
    '"Wo wurde dieser Roboter entwickelt?":"Gdzie opracowano tego robota?",'
    '"Aus welchem Land stammt diese Serie?":"Z jakiego kraju pochodzi ten serial?",'
    '"Aus welchem Land kommt diese Band / dieser Künstler?":"Z jakiego kraju pochodzi ten zespół/artysta?",'
    '"Aus welchem Land stammt diese Website / Plattform?":"Z jakiego kraju pochodzi ta strona/platforma?",'
    '"Wo kommt dieses Buch / dieser Autor her?":"Skąd pochodzi ta książka/autor?",'
    '"In welchem Land liegt dieser Freizeitpark?":"W jakim kraju znajduje się ten park rozrywki?",'
    '"Wo hat dieses Unternehmen seinen Hauptsitz?":"Gdzie znajduje się siedziba tej firmy?",'
    '"In welchem Land wurde dieser Film gedreht?":"W jakim kraju nakręcono ten film?",'
    '"Aus welchem Land stammt diese Spielekonsole?":"Z jakiego kraju pochodzi ta konsola?",'
    '"Aus welchem Land kommt diese Gaming-Hardware?":"Z jakiego kraju pochodzi ten sprzęt gamingowy?",'
    '"Aus welcher Region der Welt stammt diese Pflanze?":"Z jakiego regionu świata pochodzi ta roślina?"'
    '},"en":{"Welche Serie'
)

# ─────────────────────────────────────────────────────────────────────────────
# 3. i18n EN — neue Strings anhängen
# ─────────────────────────────────────────────────────────────────────────────
I18N_EN_OLD = (
    '"Aus welcher Region stammt diese Sprache?":"Which region does this language come from?"'
    '}};'
)
I18N_EN_NEW = (
    '"Aus welcher Region stammt diese Sprache?":"Which region does this language come from?",'
    '"Wo kommt diese Hunderasse her?":"Where does this dog breed come from?",'
    '"Wo kommt dieses Brettspiel her?":"Where does this board game come from?",'
    '"Wo wurde dieser Roboter entwickelt?":"Where was this robot developed?",'
    '"Aus welchem Land stammt diese Serie?":"Which country does this series come from?",'
    '"Aus welchem Land kommt diese Band / dieser Künstler?":"Which country does this band/artist come from?",'
    '"Aus welchem Land stammt diese Website / Plattform?":"Which country does this website/platform come from?",'
    '"Wo kommt dieses Buch / dieser Autor her?":"Where does this book / author come from?",'
    '"In welchem Land liegt dieser Freizeitpark?":"Which country is this theme park in?",'
    '"Wo hat dieses Unternehmen seinen Hauptsitz?":"Where is this company headquartered?",'
    '"In welchem Land wurde dieser Film gedreht?":"In which country was this film shot?",'
    '"Aus welchem Land stammt diese Spielekonsole?":"Which country does this game console come from?",'
    '"Aus welchem Land kommt diese Gaming-Hardware?":"Which country does this gaming hardware come from?",'
    '"Aus welcher Region der Welt stammt diese Pflanze?":"Which region of the world does this plant come from?"'
    '}};'
)

# ─────────────────────────────────────────────────────────────────────────────
# 4. MODES Array — 13 neue Einträge nach ws_garten_strelitzie
# ─────────────────────────────────────────────────────────────────────────────
MODES_OLD = (
    '{id:"ws_garten_strelitzie",icon:"\\u{1F33A}",title:"WS: Strelitzie",'
    'group:"gartenbau",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus STRELITZIE!",'
    'desc:"Anagramm-R\\u00e4tsel \\u2014 10 Buchstaben",'
    'prompt_en:"Form words from STRELITZIE!"},'
)
MODES_NEW = (
    MODES_OLD +
    '\n    /* Phase 442: Geo-Pin-Welle */\n'
    '    {id:"hund_pin_land",icon:"\\u{1F436}",title:"Hunde: Herkunft pinnen",'
    'group:"hunde",prompt:"Wo kommt diese Hunderasse her?",'
    'desc:"Pinne das Ursprungsland auf der Weltkarte.",'
    'prompt_en:"Where does this dog breed come from?"},\n'
    '    {id:"boardgame_pin_land",icon:"\\u{1F3B2}",title:"Brettspiele: Herkunft pinnen",'
    'group:"boardgames",prompt:"Wo kommt dieses Brettspiel her?",'
    'desc:"Pinne das Ursprungsland auf der Weltkarte.",'
    'prompt_en:"Where does this board game come from?"},\n'
    '    {id:"robot_pin_land",icon:"\\u{1F916}",title:"Robotik: Herkunft pinnen",'
    'group:"robotik",prompt:"Wo wurde dieser Roboter entwickelt?",'
    'desc:"Pinne das Ursprungsland auf der Weltkarte.",'
    'prompt_en:"Where was this robot developed?"},\n'
    '    {id:"serie_pin_land",icon:"\\u{1F4FA}",title:"Serien: Produktionsland pinnen",'
    'group:"serien",prompt:"Aus welchem Land stammt diese Serie?",'
    'desc:"Pinne das Produktionsland auf der Weltkarte.",'
    'prompt_en:"Which country does this series come from?"},\n'
    '    {id:"musik_pin_land",icon:"\\u{1F3B5}",title:"Musik: Herkunftsland pinnen",'
    'group:"musik",prompt:"Aus welchem Land kommt diese Band / dieser K\\u00fcnstler?",'
    'desc:"Pinne das Herkunftsland auf der Weltkarte.",'
    'prompt_en:"Which country does this band/artist come from?"},\n'
    '    {id:"web_pin_land",icon:"\\u{1F310}",title:"Webkultur: Herkunft pinnen",'
    'group:"webkultur",prompt:"Aus welchem Land stammt diese Website / Plattform?",'
    'desc:"Pinne das Ursprungsland auf der Weltkarte.",'
    'prompt_en:"Which country does this website/platform come from?"},\n'
    '    {id:"lit_pin_land",icon:"\\u{1F4DA}",title:"Literatur: Herkunft pinnen",'
    'group:"literatur",prompt:"Wo kommt dieses Buch / dieser Autor her?",'
    'desc:"Pinne das Ursprungsland auf der Weltkarte.",'
    'prompt_en:"Where does this book / author come from?"},\n'
    '    {id:"park_pin_land",icon:"\\u{1F3A2}",title:"Freizeitparks: Land pinnen",'
    'group:"themeparks",prompt:"In welchem Land liegt dieser Freizeitpark?",'
    'desc:"Pinne das Land auf der Weltkarte.",'
    'prompt_en:"Which country is this theme park in?"},\n'
    '    {id:"eco_pin_land",icon:"\\u{1F4BC}",title:"Wirtschaft: Hauptsitz pinnen",'
    'group:"wirtschaft",prompt:"Wo hat dieses Unternehmen seinen Hauptsitz?",'
    'desc:"Pinne das Hauptsitzland auf der Weltkarte.",'
    'prompt_en:"Where is this company headquartered?"},\n'
    '    {id:"film_pin_land",icon:"\\u{1F3AC}",title:"Filme: Drehort pinnen",'
    'group:"filme",prompt:"In welchem Land wurde dieser Film gedreht?",'
    'desc:"Pinne das Drehortland auf der Weltkarte.",'
    'prompt_en:"In which country was this film shot?"},\n'
    '    {id:"konsole_pin_land",icon:"\\u{1F3AE}",title:"Konsolen: Herkunft pinnen",'
    'group:"hardware",prompt:"Aus welchem Land stammt diese Spielekonsole?",'
    'desc:"Pinne das Herkunftsland auf der Weltkarte.",'
    'prompt_en:"Which country does this game console come from?"},\n'
    '    {id:"hw_pin_land",icon:"\\u{1F5A5}\\uFE0F",title:"Gaming-Hardware: Herkunft pinnen",'
    'group:"hardware",prompt:"Aus welchem Land kommt diese Gaming-Hardware?",'
    'desc:"Pinne das Herkunftsland auf der Weltkarte.",'
    'prompt_en:"Which country does this gaming hardware come from?"},\n'
    '    {id:"garten_pin_region",icon:"\\u{1F33F}",title:"Gartenbau: Region pinnen",'
    'group:"gartenbau",prompt:"Aus welcher Region der Welt stammt diese Pflanze?",'
    'desc:"Pinne die Ursprungsregion auf der Weltkarte.",'
    'prompt_en:"Which region of the world does this plant come from?"},'
)

# ─────────────────────────────────────────────────────────────────────────────
# 5. MODE_CATS — Pin-Modi in bestehende Gruppen eintragen
# ─────────────────────────────────────────────────────────────────────────────
CATS_HUNDE_OLD = (
    'hunde:{label:"Hunderassen",icon:"\\u{1F436}",'
    'modes:["hl_hund_gewicht","hl_hund_alter","hl_hund_hoehe","hund_match_land",'
    '"hund_match_kategorie","ws_hund_begleiter","ws_hund_welpe"],cost:0},'
)
CATS_HUNDE_NEW = (
    'hunde:{label:"Hunderassen",icon:"\\u{1F436}",'
    'modes:["hl_hund_gewicht","hl_hund_alter","hl_hund_hoehe","hund_match_land",'
    '"hund_match_kategorie","ws_hund_begleiter","ws_hund_welpe","hund_pin_land"],cost:0},'
)

CATS_GARTEN_OLD = (
    'gartenbau:{label:"Gartenbau & Botanik",icon:"\\u{1F33F}",'
    'modes:["hl_garten_hoehe","hl_garten_bluete","garten_match_wasser","garten_match_boden",'
    '"garten_match_region","ws_garten_rhodo","ws_garten_strelitzie"],cost:0},'
)
CATS_GARTEN_NEW = (
    'gartenbau:{label:"Gartenbau & Botanik",icon:"\\u{1F33F}",'
    'modes:["hl_garten_hoehe","hl_garten_bluete","garten_match_wasser","garten_match_boden",'
    '"garten_match_region","ws_garten_rhodo","ws_garten_strelitzie","garten_pin_region"],cost:0},'
)

# boardgames, robotik, serien, musik, webkultur, literatur, themeparks, wirtschaft, filme, hardware
# Diese haben je einen match_land Eintrag — Pin anhängen
CATS_BOARD_OLD = 'ws_boardgame_spielbrett"],cost:0},'
CATS_BOARD_NEW = 'ws_boardgame_spielbrett","boardgame_pin_land"],cost:0},'

CATS_ROBOT_OLD = 'ws_robot_name"],cost:0},'
CATS_ROBOT_NEW = 'ws_robot_name","robot_pin_land"],cost:0},'

CATS_SERIE_OLD = 'timeline_serie_start"],cost:0},'
CATS_SERIE_NEW = 'timeline_serie_start","serie_pin_land"],cost:0},'

CATS_MUSIK_OLD = 'musik_match_hit"],cost:0},'
CATS_MUSIK_NEW = 'musik_match_hit","musik_pin_land"],cost:0},'

CATS_WEB_OLD = 'ws_web_algorithmus"],cost:0},'
CATS_WEB_NEW = 'ws_web_algorithmus","web_pin_land"],cost:0},'

CATS_LIT_OLD = 'ws_lit_protagonist"],cost:0},'
CATS_LIT_NEW = 'ws_lit_protagonist","lit_pin_land"],cost:0},'

CATS_PARK_OLD = 'ws_park_achterbahn"],cost:0},'
CATS_PARK_NEW = 'ws_park_achterbahn","park_pin_land"],cost:0},'

CATS_ECO_OLD = 'ws_eco_aktie"],cost:0},'
CATS_ECO_NEW = 'ws_eco_aktie","eco_pin_land"],cost:0},'

CATS_FILM_OLD = 'film_match_drehort"],cost:0},'
CATS_FILM_NEW = 'film_match_drehort","film_pin_land"],cost:0},'

# hardware hat konsolen + gaming_hardware
CATS_HW_OLD = 'hl_games_publisher_lng"],cost:0},'
CATS_HW_NEW = 'hl_games_publisher_lng","konsole_pin_land","hw_pin_land"],cost:0},'

# ─────────────────────────────────────────────────────────────────────────────
# 6. GEN Dispatcher — 13 neue Einträge
# ─────────────────────────────────────────────────────────────────────────────
DISP_OLD = (
    'ws_garten_strelitzie:()=>{initGartenWS("strelitzie");return null;},'
)
DISP_NEW = (
    'ws_garten_strelitzie:()=>{initGartenWS("strelitzie");return null;},\n'
    '  /* Phase 442: Geo-Pin-Welle */\n'
    '  hund_pin_land:()=>genExtPinByLand(HUNDE_DATA,"ursprungsland","hunde",_tc("Wo kommt diese Hunderasse her?"),"hundpin"),\n'
    '  boardgame_pin_land:()=>genExtPinByLand(BOARDGAMES_DATA,"ursprungsland","boardgames",_tc("Wo kommt dieses Brettspiel her?"),"bgpin"),\n'
    '  robot_pin_land:()=>genExtPinByLand(ROBOT_DATA,"ursprungsland","robotik",_tc("Wo wurde dieser Roboter entwickelt?"),"robpin"),\n'
    '  serie_pin_land:()=>genExtPinByLand(SERIEN_DATA,"produktionsland","serien",_tc("Aus welchem Land stammt diese Serie?"),"seriepin"),\n'
    '  musik_pin_land:()=>genExtPinByLand(MUSIK_DATA,"herkunftsland","musik",_tc("Aus welchem Land kommt diese Band / dieser K\\u00fcnstler?"),"musikpin"),\n'
    '  web_pin_land:()=>genExtPinByLand(WEBKULTUR_DATA,"ursprungsland","webkultur",_tc("Aus welchem Land stammt diese Website / Plattform?"),"webpin"),\n'
    '  lit_pin_land:()=>genLitPinQ(),\n'
    '  park_pin_land:()=>genExtPinByLand(THEMEPARKS_DATA,"park_land","themeparks",_tc("In welchem Land liegt dieser Freizeitpark?"),"parkpin"),\n'
    '  eco_pin_land:()=>genExtPinByLand(ECO_DATA,"hauptsitz_land","wirtschaft",_tc("Wo hat dieses Unternehmen seinen Hauptsitz?"),"ecopin"),\n'
    '  film_pin_land:()=>genExtPinByLand(FILME_DATA,"drehort_land","filme",_tc("In welchem Land wurde dieser Film gedreht?"),"filmpin"),\n'
    '  konsole_pin_land:()=>genExtPinByLand(KONSOLEN_DATA,"herkunftsland","hardware",_tc("Aus welchem Land stammt diese Spielekonsole?"),"konsolenpin"),\n'
    '  hw_pin_land:()=>genExtPinByLand(HW_DATA,"company_land","hardware",_tc("Aus welchem Land kommt diese Gaming-Hardware?"),"hwpin"),\n'
    '  garten_pin_region:()=>genExtPinByLand(GARTEN_DATA,"ursprungsregion","gartenbau",_tc("Aus welcher Region der Welt stammt diese Pflanze?"),"gartenpin"),'
)

# ─────────────────────────────────────────────────────────────────────────────
# Patch ausführen
# ─────────────────────────────────────────────────────────────────────────────
print('\n-- patch_442: validate_content.py -- (keine Änderungen nötig)')
print('\n-- patch_442: gen.py --')

patch(GEN, [
    (CONST_OLD,        CONST_NEW,        'JS: LAND_LATLON Konstante'),
    (GEN_FN_OLD,       GEN_FN_NEW,       'JS: genExtPinByLand + genLitPinQ'),
    (I18N_PL_OLD,      I18N_PL_NEW,      'i18n PL: 14 neue Strings'),
    (I18N_EN_OLD,      I18N_EN_NEW,      'i18n EN: 14 neue Strings'),
    (MODES_OLD,        MODES_NEW,        'MODES: 13 neue Pin-Modi'),
    (CATS_HUNDE_OLD,   CATS_HUNDE_NEW,   'MODE_CATS: hunde'),
    (CATS_GARTEN_OLD,  CATS_GARTEN_NEW,  'MODE_CATS: gartenbau'),
    (CATS_BOARD_OLD,   CATS_BOARD_NEW,   'MODE_CATS: boardgames'),
    (CATS_ROBOT_OLD,   CATS_ROBOT_NEW,   'MODE_CATS: robotik'),
    (CATS_SERIE_OLD,   CATS_SERIE_NEW,   'MODE_CATS: serien'),
    (CATS_MUSIK_OLD,   CATS_MUSIK_NEW,   'MODE_CATS: musik'),
    (CATS_WEB_OLD,     CATS_WEB_NEW,     'MODE_CATS: webkultur'),
    (CATS_LIT_OLD,     CATS_LIT_NEW,     'MODE_CATS: literatur'),
    (CATS_PARK_OLD,    CATS_PARK_NEW,    'MODE_CATS: themeparks'),
    (CATS_ECO_OLD,     CATS_ECO_NEW,     'MODE_CATS: wirtschaft'),
    (CATS_FILM_OLD,    CATS_FILM_NEW,    'MODE_CATS: filme'),
    (CATS_HW_OLD,      CATS_HW_NEW,      'MODE_CATS: hardware (konsolen+hw)'),
    (DISP_OLD,         DISP_NEW,         'GEN dispatch: 13 neue Pin-Einträge'),
])

print('\nPatch 442 fertig!')
