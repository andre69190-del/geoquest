#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 431: Kategorien Medizin & Wirtschaft.

Neue JSON-Dateien: medizin_extended.json, wirtschaft_extended.json,
                   medizin_ws.json, wirtschaft_ws.json
Neue Timeline-Keys in timeline.json: med_meilensteine, eco_gruendung

Neue MODES (13):
  Medizin: hl_med_knochen, hl_med_gewicht, med_match_fachbegriff,
           timeline_med_meilensteine, ws_med_stoffwechsel, ws_med_blutkreislauf
  Wirtschaft: hl_eco_umsatz, hl_eco_mitarbeiter, hl_eco_gruendung,
              eco_match_hq_land, eco_match_branche, timeline_eco_gruendung,
              ws_eco_aktie

Zero-Bug-Policy: assert count==1 vor jedem replace.
i18n: alle Prompts via _tc(), DE/EN/PL in _CONTENT_I18N.
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
        print(f'  OK  {tag}')
    open(path, 'w', encoding='utf-8').write(c)


# ─── 1. Python data loading ───────────────────────────────────────────────────
LOAD_OLD = (
    "    with open(os.path.join(os.path.dirname(__file__), 'data/literatur_ws.json'), 'r', encoding='utf-8') as _lwf:\n"
    "        LIT_WS_J = __import__('json').dumps(__import__('json').load(_lwf), ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/robotik_ws.json'), 'r', encoding='utf-8') as _rwf:\n"
    "        ROBOT_WS_J = __import__('json').dumps(__import__('json').load(_rwf), ensure_ascii=False, separators=(',','::'))"
)
# Fix the double-colon typo from the previous patch AND add new loaders
LOAD_NEW = (
    "    with open(os.path.join(os.path.dirname(__file__), 'data/literatur_ws.json'), 'r', encoding='utf-8') as _lwf:\n"
    "        LIT_WS_J = __import__('json').dumps(__import__('json').load(_lwf), ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/robotik_ws.json'), 'r', encoding='utf-8') as _rwf:\n"
    "        ROBOT_WS_J = __import__('json').dumps(__import__('json').load(_rwf), ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/medizin_extended.json'), 'r', encoding='utf-8') as _mef:\n"
    "        MED_J = __import__('json').dumps(__import__('json').load(_mef), ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/wirtschaft_extended.json'), 'r', encoding='utf-8') as _wef:\n"
    "        ECO_J = __import__('json').dumps(__import__('json').load(_wef), ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/medizin_ws.json'), 'r', encoding='utf-8') as _mwf:\n"
    "        MED_WS_J = __import__('json').dumps(__import__('json').load(_mwf), ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/wirtschaft_ws.json'), 'r', encoding='utf-8') as _ewf:\n"
    "        ECO_WS_J = __import__('json').dumps(__import__('json').load(_ewf), ensure_ascii=False, separators=(',','::'))"
)
# Fix double-colon in ECO_WS_J too
LOAD_NEW = LOAD_NEW.replace("separators=(',','::'))", "separators=(',','::'))")
LOAD_NEW = (
    "    with open(os.path.join(os.path.dirname(__file__), 'data/literatur_ws.json'), 'r', encoding='utf-8') as _lwf:\n"
    "        LIT_WS_J = __import__('json').dumps(__import__('json').load(_lwf), ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/robotik_ws.json'), 'r', encoding='utf-8') as _rwf:\n"
    "        ROBOT_WS_J = __import__('json').dumps(__import__('json').load(_rwf), ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/medizin_extended.json'), 'r', encoding='utf-8') as _mef:\n"
    "        MED_J = __import__('json').dumps(__import__('json').load(_mef), ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/wirtschaft_extended.json'), 'r', encoding='utf-8') as _wef:\n"
    "        ECO_J = __import__('json').dumps(__import__('json').load(_wef), ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/medizin_ws.json'), 'r', encoding='utf-8') as _mwf:\n"
    "        MED_WS_J = __import__('json').dumps(__import__('json').load(_mwf), ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/wirtschaft_ws.json'), 'r', encoding='utf-8') as _ewf:\n"
    "        ECO_WS_J = __import__('json').dumps(__import__('json').load(_ewf), ensure_ascii=False, separators=(',',':'))"
)

# ─── 2. JS constants ──────────────────────────────────────────────────────────
CONST_OLD = "const LIT_WS_DATA=PLACEHOLDER_LIT_WS;\nconst ROBOT_WS_DATA=PLACEHOLDER_ROBOT_WS;"
CONST_NEW = (
    "const LIT_WS_DATA=PLACEHOLDER_LIT_WS;\n"
    "const ROBOT_WS_DATA=PLACEHOLDER_ROBOT_WS;\n"
    "const MED_DATA=PLACEHOLDER_MED;\n"
    "const ECO_DATA=PLACEHOLDER_ECO;\n"
    "const MED_WS_DATA=PLACEHOLDER_MED_WS;\n"
    "const ECO_WS_DATA=PLACEHOLDER_ECO_WS;"
)

# ─── 3. _mkWS init ────────────────────────────────────────────────────────────
MKWS_OLD = 'var initLitWS=_mkWS(LIT_WS_DATA,"Lit");\nvar initRobotWS=_mkWS(ROBOT_WS_DATA,"Robot");'
MKWS_NEW = (
    'var initLitWS=_mkWS(LIT_WS_DATA,"Lit");\n'
    'var initRobotWS=_mkWS(ROBOT_WS_DATA,"Robot");\n'
    'var initMedWS=_mkWS(MED_WS_DATA,"Med");\n'
    'var initEcoWS=_mkWS(ECO_WS_DATA,"Eco");'
)

# ─── 4. Generator functions (after genRobotMatchExt) ─────────────────────────
GEN_ANCHOR = 'window.genRobotMatchExt=genRobotMatchExt;'
GEN_NEW = '''window.genRobotMatchExt=genRobotMatchExt;

/* Phase 431: genMedizinHLExt / genMedizinMatchExt */
function genMedizinHLExt(field,opts){var o=opts||{};var items=[];var _MD=MED_DATA;
  var _ks=Object.keys(_MD).filter(function(k){return Object.prototype.hasOwnProperty.call(_MD,k);});
  for(var _i=0;_i<_ks.length;_i++){var _n=_ks[_i],_v=+(_MD[_n][field]);if(!isNaN(_v)&&_v>0)items.push({name:_n,val:_v});}
  if(items.length<4)return null;
  items.sort(function(a,b){return a.val-b.val;});var len=items.length,tries=0;
  while(tries++<40){var ai=~~(rng()*len),W=Math.max(1,Math.floor(len*0.3));
    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);
    var pool=[];for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}if(!pool.length)continue;
    var bi=pool[~~(rng()*pool.length)],a=items[ai],b=items[bi];if(a.val===b.val)continue;
    var winner=o.lowerWins?(a.val<b.val?a:b):(a.val>b.val?a:b);
    var unit=o.unit||"",meta=a.name+": "+a.val+(unit?" "+unit:"")+" · "+b.name+": "+b.val+(unit?" "+unit:"");
    return{type:"beta_hl",prompt:o.prompt||_tc("Welches Organ/K\\u00f6rperteil ist schwerer?"),subj:"",opts:[a.name,b.name],ans:winner.name,meta:meta,lid:"med_"+field+"_"+ai+"_"+bi,cc:"de"};
  }return null;}
window.genMedizinHLExt=genMedizinHLExt;

function genMedizinMatchExt(field,prompt,fixedPool){var _MD=MED_DATA;
  var valid=Object.keys(_MD).filter(function(k){return Object.prototype.hasOwnProperty.call(_MD,k)&&_MD[k][field]!=null&&_MD[k][field]!=="";});
  if(valid.length<4)return null;
  var idx=~~(rng()*valid.length),entry=valid[idx],correct=String(_MD[entry][field]);
  var pool=fixedPool?fixedPool.filter(function(v){return v!==correct;})
    :valid.map(function(n){return String(_MD[n][field]);}).filter(function(v,i,a){return a.indexOf(v)===i&&v!==correct;});
  if(pool.length<3)return null;
  for(var k=pool.length-1;k>0;k--){var t=~~(rng()*(k+1));var tmp=pool[k];pool[k]=pool[t];pool[t]=tmp;}
  var opts=[correct].concat(pool.slice(0,3));
  for(var m=opts.length-1;m>0;m--){var t2=~~(rng()*(m+1));var tm=opts[m];opts[m]=opts[t2];opts[t2]=tm;}
  return{type:"uk_match",prompt:prompt,subj:entry,ans:correct,opts:opts,lid:"med_"+field+"_"+idx,cc:"de"};
}
window.genMedizinMatchExt=genMedizinMatchExt;

/* Phase 431: genWirtschaftHLExt / genWirtschaftMatchExt */
function genWirtschaftHLExt(field,opts){var o=opts||{};var items=[];var _ED=ECO_DATA;
  var _ks=Object.keys(_ED).filter(function(k){return Object.prototype.hasOwnProperty.call(_ED,k);});
  for(var _i=0;_i<_ks.length;_i++){var _n=_ks[_i],_v=+(_ED[_n][field]);if(!isNaN(_v)&&_v>0)items.push({name:_n,val:_v});}
  if(items.length<4)return null;
  items.sort(function(a,b){return a.val-b.val;});var len=items.length,tries=0;
  while(tries++<40){var ai=~~(rng()*len),W=Math.max(1,Math.floor(len*0.25));
    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);
    var pool=[];for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}if(!pool.length)continue;
    var bi=pool[~~(rng()*pool.length)],a=items[ai],b=items[bi];if(a.val===b.val)continue;
    var winner=o.lowerWins?(a.val<b.val?a:b):(a.val>b.val?a:b);
    var unit=o.unit||"Mrd. USD",meta=a.name+": "+a.val+" "+unit+" · "+b.name+": "+b.val+" "+unit;
    return{type:"beta_hl",prompt:o.prompt||_tc("Welches Unternehmen hat h\\u00f6heren Umsatz?"),subj:"",opts:[a.name,b.name],ans:winner.name,meta:meta,lid:"eco_"+field+"_"+ai+"_"+bi,cc:"de"};
  }return null;}
window.genWirtschaftHLExt=genWirtschaftHLExt;

function genWirtschaftMatchExt(field,prompt,fixedPool){var _ED=ECO_DATA;
  var valid=Object.keys(_ED).filter(function(k){return Object.prototype.hasOwnProperty.call(_ED,k)&&_ED[k][field]!=null&&_ED[k][field]!=="";});
  if(valid.length<4)return null;
  var idx=~~(rng()*valid.length),co=valid[idx],correct=String(_ED[co][field]);
  var pool=fixedPool?fixedPool.filter(function(v){return v!==correct;})
    :valid.map(function(n){return String(_ED[n][field]);}).filter(function(v,i,a){return a.indexOf(v)===i&&v!==correct;});
  if(pool.length<3)return null;
  for(var k=pool.length-1;k>0;k--){var t=~~(rng()*(k+1));var tmp=pool[k];pool[k]=pool[t];pool[t]=tmp;}
  var opts=[correct].concat(pool.slice(0,3));
  for(var m=opts.length-1;m>0;m--){var t2=~~(rng()*(m+1));var tm=opts[m];opts[m]=opts[t2];opts[t2]=tm;}
  return{type:"uk_match",prompt:prompt,subj:co,ans:correct,opts:opts,lid:"eco_"+field+"_"+idx,cc:"de"};
}
window.genWirtschaftMatchExt=genWirtschaftMatchExt;'''

# ─── 5. i18n strings ──────────────────────────────────────────────────────────
# PL block: append before closing '},"en"'
I18N_PL_OLD = '"Welcher Fakt beschreibt dieses System am besten?":"Który fakt najlepiej opisuje ten system?"},"en"'
I18N_PL_NEW = (
    '"Welcher Fakt beschreibt dieses System am besten?":"Który fakt najlepiej opisuje ten system?",'
    '"Welcher Knochen kommt öfter vor?":"Która kość występuje częściej?",'
    '"Welches Organ/Körperteil ist schwerer?":"Który narząd/część ciała jest cięższa?",'
    '"Wie lautet der lateinische Fachbegriff?":"Łaciński termin medyczny to:",'
    '"Welches Unternehmen hat höheren Umsatz?":"Które przedsiębiorstwo ma wyższy przychód?",'
    '"Welches Unternehmen hat mehr Mitarbeiter?":"Które przedsiębiorstwo ma więcej pracowników?",'
    '"Welches Unternehmen wurde früher gegründet?":"Które przedsiębiorstwo założono wcześniej?",'
    '"In welchem Land hat dieses Unternehmen seinen Sitz?":"W którym kraju ma siedzibę to przedsiębiorstwo?",'
    '"Welcher Branche gehört dieses Unternehmen an?":"Do jakiej branży należy to przedsiębiorstwo?"'
    '},"en"'
)

# EN block: append before closing '}}'
I18N_EN_OLD = '"Which fact best describes this system?"}};'
I18N_EN_NEW = (
    '"Which fact best describes this system?",'
    '"Welcher Knochen kommt öfter vor?":"Which bone occurs more often?",'
    '"Welches Organ/Körperteil ist schwerer?":"Which organ/body part is heavier?",'
    '"Wie lautet der lateinische Fachbegriff?":"What is the Latin medical term?",'
    '"Welches Unternehmen hat höheren Umsatz?":"Which company has higher revenue?",'
    '"Welches Unternehmen hat mehr Mitarbeiter?":"Which company has more employees?",'
    '"Welches Unternehmen wurde früher gegründet?":"Which company was founded earlier?",'
    '"In welchem Land hat dieses Unternehmen seinen Sitz?":"In which country is this company headquartered?",'
    '"Welcher Branche gehört dieses Unternehmen an?":"Which sector does this company belong to?"'
    '}};'
)

# ─── 6. MODES entries ─────────────────────────────────────────────────────────
MODES_ANCHOR = '    {id:"ws_robot_name",icon:"\\u{1F9E0}",title:"WS: Maschinenlernen",group:"robotik",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus MASCHINENLERNEN!",desc:"Anagramm-R\\u00e4tsel \\u2014 15 Buchstaben",prompt_en:"Form words from MASCHINENLERNEN!"},'
MODES_NEW = MODES_ANCHOR + """
    /* Phase 431: Medizin & Anatomie */
    {id:"hl_med_knochen",icon:"\\u{1F9B4}",title:"Medizin: Knochen",group:"medizin",prompt:"Welcher Knochen kommt \\u00f6fter vor?",desc:"Vergleiche Knochenh\\u00e4ufigkeit im menschlichen K\\u00f6rper.",prompt_en:"Which bone occurs more often?"},
    {id:"hl_med_gewicht",icon:"\\u2764\\uFE0F",title:"Medizin: Organgewicht",group:"medizin",prompt:"Welches Organ/K\\u00f6rperteil ist schwerer?",desc:"Von Schilddr\\u00fcse (25g) bis Haut (5000g).",prompt_en:"Which organ/body part is heavier?"},
    {id:"med_match_fachbegriff",icon:"\\u{1F9EC}",title:"Medizin: Fachbegriff",group:"medizin",prompt:"Wie lautet der lateinische Fachbegriff?",desc:"Cor, Hepar, Femur \\u2014 erkenne die Fachsprache.",prompt_en:"What is the Latin medical term?"},
    {id:"timeline_med_meilensteine",icon:"\\u{1FA7A}",title:"Medizin-Timeline",group:"medizin",prompt:"Welcher Meilenstein kam zuerst?",desc:"Von der Pest bis zur DNA \\u2014 Medizingeschichte sortieren.",prompt_en:"Which milestone came first?"},
    {id:"ws_med_stoffwechsel",icon:"\\u{1F9EA}",title:"WS: Stoffwechsel",group:"medizin",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus STOFFWECHSEL!",desc:"Anagramm-R\\u00e4tsel \\u2014 12 Buchstaben",prompt_en:"Form words from STOFFWECHSEL!"},
    {id:"ws_med_blutkreislauf",icon:"\\u{1F9EA}",title:"WS: Blutkreislauf",group:"medizin",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus BLUTKREISLAUF!",desc:"Anagramm-R\\u00e4tsel \\u2014 13 Buchstaben",prompt_en:"Form words from BLUTKREISLAUF!"},
    /* Phase 431: Wirtschaft & Marken */
    {id:"hl_eco_umsatz",icon:"\\u{1F4B0}",title:"Wirtschaft: Umsatz",group:"wirtschaft",prompt:"Welches Unternehmen hat h\\u00f6heren Umsatz?",desc:"Von CD Projekt bis Amazon \\u2014 globale Konzerne.",prompt_en:"Which company has higher revenue?"},
    {id:"hl_eco_mitarbeiter",icon:"\\u{1F465}",title:"Wirtschaft: Mitarbeiter",group:"wirtschaft",prompt:"Welches Unternehmen hat mehr Mitarbeiter?",desc:"In Tausend \\u2014 von Ferrari bis Amazon.",prompt_en:"Which company has more employees?"},
    {id:"hl_eco_gruendung",icon:"\\u{1F4C5}",title:"Wirtschaft: \\u00c4lteres Unternehmen",group:"wirtschaft",prompt:"Welches Unternehmen wurde fr\\u00fcher gegr\\u00fcndet?",desc:"Von Siemens 1847 bis Stellantis 2021.",prompt_en:"Which company was founded earlier?"},
    {id:"eco_match_hq_land",icon:"\\u{1F30D}",title:"Wirtschaft: Hauptsitz",group:"wirtschaft",prompt:"In welchem Land hat dieses Unternehmen seinen Sitz?",desc:"Von den USA bis D\\u00e4nemark \\u2014 erkenne den Hauptsitz.",prompt_en:"In which country is this company headquartered?"},
    {id:"eco_match_branche",icon:"\\u{1F4CA}",title:"Wirtschaft: Branche",group:"wirtschaft",prompt:"Welcher Branche geh\\u00f6rt dieses Unternehmen an?",desc:"Tech, Pharma, FMCG, Automobil \\u2014 erkenne den Sektor.",prompt_en:"Which sector does this company belong to?"},
    {id:"timeline_eco_gruendung",icon:"\\u{1F4B9}",title:"Wirtschaft-Timeline",group:"wirtschaft",prompt:"Welches Unternehmen wurde fr\\u00fcher gegr\\u00fcndet?",desc:"Von Siemens bis Stellantis \\u2014 Unternehmensgeschichte.",prompt_en:"Which company was founded earlier?"},
    {id:"ws_eco_aktie",icon:"\\u{1F4C8}",title:"WS: Aktiengesellschaft",group:"wirtschaft",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus AKTIENGESELLSCHAFT!",desc:"Anagramm-R\\u00e4tsel \\u2014 18 Buchstaben",prompt_en:"Form words from AKTIENGESELLSCHAFT!"},"""

# ─── 7. MODE_CATS ─────────────────────────────────────────────────────────────
CATS_ANCHOR = 'robotik:{label:"KI, Robotik & Hardware",icon:"\\u{1F916}",modes:["hl_robot_jahr","robot_match_kategorie","robot_match_land","robot_match_entwickler","robot_match_fakt","timeline_robot_jahr","ws_robot_name"],cost:0},'
CATS_NEW = (
    CATS_ANCHOR + '\n'
    '  medizin:{label:"Anatomie & Medizin",icon:"\\u{1FA7A}",modes:["hl_med_knochen","hl_med_gewicht","med_match_fachbegriff","timeline_med_meilensteine","ws_med_stoffwechsel","ws_med_blutkreislauf"],cost:0},\n'
    '  wirtschaft:{label:"Wirtschaft & Marken",icon:"\\u{1F4B9}",modes:["hl_eco_umsatz","hl_eco_mitarbeiter","hl_eco_gruendung","eco_match_hq_land","eco_match_branche","timeline_eco_gruendung","ws_eco_aktie"],cost:0},'
)

# ─── 8. GEN dispatch ──────────────────────────────────────────────────────────
DISP_ANCHOR = '  ws_robot_name:()=>{initRobotWS("maschinenlernen");return null;},'
DISP_NEW = (
    '  ws_robot_name:()=>{initRobotWS("maschinenlernen");return null;},\n'
    '  /* Phase 431: Medizin */\n'
    '  hl_med_knochen:()=>genMedizinHLExt("anzahl_knochen",{unit:"",prompt:_tc("Welcher Knochen kommt \\u00f6fter vor?")}),\n'
    '  hl_med_gewicht:()=>genMedizinHLExt("gewicht_gramm",{unit:"g",prompt:_tc("Welches Organ/K\\u00f6rperteil ist schwerer?")}),\n'
    '  med_match_fachbegriff:()=>genMedizinMatchExt("lateinischer_begriff",_tc("Wie lautet der lateinische Fachbegriff?")),\n'
    '  timeline_med_meilensteine:()=>genTimelineQ("med_meilensteine"),\n'
    '  ws_med_stoffwechsel:()=>{initMedWS("stoffwechsel");return null;},\n'
    '  ws_med_blutkreislauf:()=>{initMedWS("blutkreislauf");return null;},\n'
    '  /* Phase 431: Wirtschaft */\n'
    '  hl_eco_umsatz:()=>genWirtschaftHLExt("umsatz_mrd_usd",{unit:"Mrd. USD",prompt:_tc("Welches Unternehmen hat h\\u00f6heren Umsatz?")}),\n'
    '  hl_eco_mitarbeiter:()=>genWirtschaftHLExt("mitarbeiter_tausend",{unit:"Tsd.",prompt:_tc("Welches Unternehmen hat mehr Mitarbeiter?")}),\n'
    '  hl_eco_gruendung:()=>genWirtschaftHLExt("gruendungsjahr",{lowerWins:true,unit:"",prompt:_tc("Welches Unternehmen wurde fr\\u00fcher gegr\\u00fcndet?")}),\n'
    '  eco_match_hq_land:()=>genWirtschaftMatchExt("hauptsitz_land",_tc("In welchem Land hat dieses Unternehmen seinen Sitz?")),\n'
    '  eco_match_branche:()=>genWirtschaftMatchExt("kategorie",_tc("Welcher Branche geh\\u00f6rt dieses Unternehmen an?"),["Tech","Automobil","FMCG","Pharma","Finanzen","Software"]),\n'
    '  timeline_eco_gruendung:()=>genTimelineQ("eco_gruendung"),\n'
    '  ws_eco_aktie:()=>{initEcoWS("aktiengesellschaft");return null;},'
)

# ─── 9. Placeholder replace chain (MED_WS/ECO_WS before MED/ECO) ─────────────
REPL_OLD = (
    "  .replace('PLACEHOLDER_LIT_WS',         LIT_WS_J)\n"
    "  .replace('PLACEHOLDER_LIT',            LIT_J)\n"
    "  .replace('PLACEHOLDER_ROBOT_WS',       ROBOT_WS_J)\n"
    "  .replace('PLACEHOLDER_ROBOT',          ROBOT_J)"
)
REPL_NEW = (
    "  .replace('PLACEHOLDER_LIT_WS',         LIT_WS_J)\n"
    "  .replace('PLACEHOLDER_LIT',            LIT_J)\n"
    "  .replace('PLACEHOLDER_ROBOT_WS',       ROBOT_WS_J)\n"
    "  .replace('PLACEHOLDER_ROBOT',          ROBOT_J)\n"
    "  .replace('PLACEHOLDER_MED_WS',         MED_WS_J)\n"
    "  .replace('PLACEHOLDER_MED',            MED_J)\n"
    "  .replace('PLACEHOLDER_ECO_WS',         ECO_WS_J)\n"
    "  .replace('PLACEHOLDER_ECO',            ECO_J)"
)

edits = [
    (LOAD_OLD,        LOAD_NEW,        "Python: 4 neue Dateien laden"),
    (CONST_OLD,       CONST_NEW,       "JS: MED/ECO/MED_WS/ECO_WS Konstanten"),
    (MKWS_OLD,        MKWS_NEW,        "JS: initMedWS + initEcoWS"),
    (GEN_ANCHOR,      GEN_NEW,         "JS: Generator-Funktionen Med/Eco"),
    (I18N_PL_OLD,     I18N_PL_NEW,     "i18n PL: 8 neue Strings"),
    (I18N_EN_OLD,     I18N_EN_NEW,     "i18n EN: 8 neue Strings"),
    (MODES_ANCHOR,    MODES_NEW,       "MODES: 13 neue Modi"),
    (CATS_ANCHOR,     CATS_NEW,        "MODE_CATS: medizin + wirtschaft"),
    (DISP_ANCHOR,     DISP_NEW,        "GEN dispatch: 13 neue Eintraege"),
    (REPL_OLD,        REPL_NEW,        "Replace-Kette: MED_WS/ECO_WS/MED/ECO"),
]

print("=== patch_431_med_eco.py ===")
patch(GEN, edits)
print("\nPatch abgeschlossen!")
