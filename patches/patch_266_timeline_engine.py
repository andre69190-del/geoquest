"""
patch_266_timeline_engine.py
Phase 266 — Timeline-Modus Engine

Adds a brand-new drag-and-drop chronological sorting game mechanic.
4 new modes: timeline_geo_erdbeben, timeline_sport_stadien,
              timeline_astro_entdeckung, timeline_tech_release

CRLF RULE: gen.py is edited with str.replace() on text read/written
           via the Read/Write tools (Windows CRLF). This script uses
           Python str replacements only — no shell sed.
"""

import os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN  = os.path.join(BASE, 'gen.py')

with open(GEN, 'r', encoding='utf-8') as f:
    src = f.read()

original_len = len(src)
changes = []

# ─────────────────────────────────────────────────────────────────────────────
# 1. Python file-reading: add timeline.json after sport_ws.json
# ─────────────────────────────────────────────────────────────────────────────
OLD1 = "with open(os.path.join(os.path.dirname(__file__), 'data/sport_ws.json'),    'r', encoding='utf-8') as _f: SPORT_WS_J    = _f.read()"
NEW1 = OLD1 + "\nwith open(os.path.join(os.path.dirname(__file__), 'data/timeline.json'),   'r', encoding='utf-8') as _f: TIMELINE_J    = _f.read()"
assert OLD1 in src, "ANCHOR1 not found"
src = src.replace(OLD1, NEW1, 1)
changes.append("1. Added TIMELINE_J file reading")

# ─────────────────────────────────────────────────────────────────────────────
# 2. JS data constant: add TIMELINE_DATA after SPORT_WS_DATA
# ─────────────────────────────────────────────────────────────────────────────
OLD2 = "const SPORT_WS_DATA=PLACEHOLDER_SPORT_WS;"
NEW2 = OLD2 + "\nconst TIMELINE_DATA=PLACEHOLDER_TIMELINE;"
assert OLD2 in src, "ANCHOR2 not found"
src = src.replace(OLD2, NEW2, 1)
changes.append("2. Added TIMELINE_DATA constant")

# ─────────────────────────────────────────────────────────────────────────────
# 3. MODES array: add 4 new timeline mode entries
# ─────────────────────────────────────────────────────────────────────────────
OLD3 = '  {id:"ws_sportwissen_sportgeist",icon:"\\u{1F4AA}",title:"WS: Sportgeist",group:"sport_wissen",noMultiplayer:true,prompt:"Bilde Woerter aus SPORTGEIST!",desc:"Anagramm-Raetsel -- 10 Buchstaben"}\n];'
NEW3 = ('  {id:"ws_sportwissen_sportgeist",icon:"\\u{1F4AA}",title:"WS: Sportgeist",group:"sport_wissen",noMultiplayer:true,prompt:"Bilde Woerter aus SPORTGEIST!",desc:"Anagramm-Raetsel -- 10 Buchstaben"},\n'
        '  /* === Phase 266 Timeline-Modi === */\n'
        '  {id:"timeline_geo_erdbeben",  icon:"\\u{1F30D}",title:"Erdbeben-Zeitleiste", group:"geologie",    prompt:"Ordne die Erdbeben chronologisch!",     desc:"Historische Erdbeben nach Jahr sortieren"},\n'
        '  {id:"timeline_sport_stadien", icon:"\\u{1F3DF}\\uFE0F",title:"Stadion-Zeitleiste",  group:"sport_wissen",prompt:"Ordne die Stadien nach Er\\u00f6ffnungsjahr!", desc:"Stadien chronologisch sortieren"},\n'
        '  {id:"timeline_astro_entdeckung",icon:"\\u{1F52D}",title:"Entdeckungs-Zeitleiste",group:"astronomie", prompt:"Ordne die Himmelsk\\u00f6rper nach Entdeckungsjahr!",desc:"Astronomische Entdeckungen sortieren"},\n'
        '  {id:"timeline_tech_release",  icon:"\\u{1F4BB}",title:"Tech-Zeitleiste",    group:"technologie", prompt:"Ordne die Technologien nach Release-Jahr!",desc:"Tech-Releases chronologisch sortieren"}\n'
        '];')
assert OLD3 in src, "ANCHOR3 (MODES end) not found"
src = src.replace(OLD3, NEW3, 1)
changes.append("3. Added 4 timeline MODES entries")

# ─────────────────────────────────────────────────────────────────────────────
# 4a. MODE_CATS geologie: append timeline_geo_erdbeben
# ─────────────────────────────────────────────────────────────────────────────
OLD4A = '    "ws_geo_erdkruste","ws_geo_mineralien"\n  ],cost:0},\n  sport_wissen:'
NEW4A = '    "ws_geo_erdkruste","ws_geo_mineralien","timeline_geo_erdbeben"\n  ],cost:0},\n  sport_wissen:'
assert OLD4A in src, "ANCHOR4A (geologie MODE_CATS) not found"
src = src.replace(OLD4A, NEW4A, 1)
changes.append("4a. Added timeline_geo_erdbeben to geologie MODE_CATS")

# ─────────────────────────────────────────────────────────────────────────────
# 4b. MODE_CATS sport_wissen: append timeline_sport_stadien
# ─────────────────────────────────────────────────────────────────────────────
OLD4B = '    "ws_sportwissen_startschuss","ws_sportwissen_athletik","ws_sportwissen_sportgeist"\n  ],cost:0},\n};'
NEW4B = '    "ws_sportwissen_startschuss","ws_sportwissen_athletik","ws_sportwissen_sportgeist","timeline_sport_stadien"\n  ],cost:0},\n};'
assert OLD4B in src, "ANCHOR4B (sport_wissen MODE_CATS) not found"
src = src.replace(OLD4B, NEW4B, 1)
changes.append("4b. Added timeline_sport_stadien to sport_wissen MODE_CATS")

# ─────────────────────────────────────────────────────────────────────────────
# 4c. MODE_CATS astronomie: append timeline_astro_entdeckung
# ─────────────────────────────────────────────────────────────────────────────
OLD4C = '    "ws_astro_schwarzesloch"\n  ],cost:0},\n  geologie:'
NEW4C = '    "ws_astro_schwarzesloch","timeline_astro_entdeckung"\n  ],cost:0},\n  geologie:'
assert OLD4C in src, "ANCHOR4C (astronomie MODE_CATS) not found"
src = src.replace(OLD4C, NEW4C, 1)
changes.append("4c. Added timeline_astro_entdeckung to astronomie MODE_CATS")

# ─────────────────────────────────────────────────────────────────────────────
# 4d. MODE_CATS technologie: append timeline_tech_release
# ─────────────────────────────────────────────────────────────────────────────
OLD4D = '    "ws_tech_cybersicherheit","ws_tech_softwareentwicklung","ws_tech_compilerbau","ws_tech_betriebssystem"\n  ],cost:0},\n  emobilitaet:'
NEW4D = '    "ws_tech_cybersicherheit","ws_tech_softwareentwicklung","ws_tech_compilerbau","ws_tech_betriebssystem","timeline_tech_release"\n  ],cost:0},\n  emobilitaet:'
assert OLD4D in src, "ANCHOR4D (technologie MODE_CATS) not found"
src = src.replace(OLD4D, NEW4D, 1)
changes.append("4d. Added timeline_tech_release to technologie MODE_CATS")

# ─────────────────────────────────────────────────────────────────────────────
# 5. JS functions: genTimelineQ + drag helpers + checkTimeline (before const GEN)
# ─────────────────────────────────────────────────────────────────────────────
OLD5 = '}\n\nconst GEN={'
NEW5 = '''}

/* === Phase 266: Timeline-Engine === */
var _tlDrag=null;
function _tlDragStart(n){_tlDrag=n;}
function _tlDragOver(e){e.preventDefault();if(e.dataTransfer)e.dataTransfer.dropEffect='move';}
function _tlDrop(e,n){
  e.preventDefault();
  if(!_tlDrag||_tlDrag===n)return;
  var list=document.getElementById('tl-list');
  if(!list)return;
  var items=Array.from(list.children);
  var draggedEl=null,targetEl=null;
  for(var _i=0;_i<items.length;_i++){
    if(items[_i].getAttribute('data-tn')===_tlDrag)draggedEl=items[_i];
    if(items[_i].getAttribute('data-tn')===n)targetEl=items[_i];
  }
  if(!draggedEl||!targetEl)return;
  var di=items.indexOf(draggedEl),ti=items.indexOf(targetEl);
  if(di<ti)list.insertBefore(draggedEl,targetEl.nextSibling);
  else list.insertBefore(draggedEl,targetEl);
  _tlDrag=null;
}
var _tlTouchN=null;
function _tlTouchStart(e,n){_tlTouchN=n;e.preventDefault();}
function _tlTouchMove(e){e.preventDefault();}
function _tlTouchEnd(e){
  if(!_tlTouchN)return;
  var touch=e.changedTouches[0];
  var list=document.getElementById('tl-list');
  if(!list){_tlTouchN=null;return;}
  var items=Array.from(list.children);
  var targetEl=null;
  for(var _i=0;_i<items.length;_i++){
    var rect=items[_i].getBoundingClientRect();
    if(touch.clientY>=rect.top&&touch.clientY<=rect.bottom){targetEl=items[_i];break;}
  }
  var n=_tlTouchN;_tlTouchN=null;
  if(targetEl){
    var tn=targetEl.getAttribute('data-tn');
    if(tn&&tn!==n){_tlDrag=n;_tlDrop({preventDefault:function(){}},tn);}
  }
}
function checkTimeline(){
  if(!S.q||S.q.type!=='timeline')return;
  var list=document.getElementById('tl-list');
  if(!list)return;
  var tiles=Array.from(list.children);
  var userOrder=tiles.map(function(t){return t.getAttribute('data-tn');});
  S.q._tlUserOrder=userOrder;
  var correct=S.q.ans;
  S.ok=JSON.stringify(userOrder)===JSON.stringify(correct);
  answer(S.ok);
}
function genTimelineQ(dataKey,promptOverride,unit){
  var data=TIMELINE_DATA[dataKey];
  if(!data||!data.items||data.items.length<4)return null;
  var pool=data.items.slice().sort(function(){return rng()-.5;});
  var seen={},picked=[];
  for(var _i=0;_i<pool.length&&picked.length<5;_i++){
    var yr=pool[_i].year;
    if(!seen[yr]){seen[yr]=1;picked.push(pool[_i]);}
  }
  if(picked.length<4)return null;
  var items=picked.slice(0,rng()<.4&&picked.length>=5?5:4);
  var sorted=items.slice().sort(function(a,b){return a.year-b.year;});
  var ans=sorted.map(function(it){return it.n;});
  var lid='tl_'+dataKey+'_'+ans.join('|').replace(/[^a-zA-Z0-9_|]/g,'').slice(0,40);
  return{type:'timeline',prompt:promptOverride||data.prompt||'Chronologisch sortieren!',
    items:items,ans:ans,unit:unit||data.unit||'Jahr',lid:lid,cc:null};
}

const GEN={'''
assert OLD5 in src, "ANCHOR5 (before const GEN) not found"
src = src.replace(OLD5, NEW5, 1)
changes.append("5. Added genTimelineQ + drag helpers + checkTimeline before GEN")

# ─────────────────────────────────────────────────────────────────────────────
# 6. GEN object: add 4 timeline mode generators
# ─────────────────────────────────────────────────────────────────────────────
OLD6 = '  uk_breitengrad_match:()=>genUniversalMatchQ("breitengrad_match"),\n};'
NEW6 = ('  uk_breitengrad_match:()=>genUniversalMatchQ("breitengrad_match"),\n'
        '  /* Phase 266 Timeline */\n'
        '  timeline_geo_erdbeben:   ()=>genTimelineQ("geo_erdbeben"),\n'
        '  timeline_sport_stadien:  ()=>genTimelineQ("sport_stadien"),\n'
        '  timeline_astro_entdeckung:()=>genTimelineQ("astro_entdeckung"),\n'
        '  timeline_tech_release:   ()=>genTimelineQ("tech_release"),\n'
        '};')
assert OLD6 in src, "ANCHOR6 (GEN end) not found"
src = src.replace(OLD6, NEW6, 1)
changes.append("6. Added 4 timeline GEN entries")

# ─────────────────────────────────────────────────────────────────────────────
# 7. _TRUSTED_FNS: add checkTimeline
# ─────────────────────────────────────────────────────────────────────────────
OLD7 = '"lvAnswer","syncOfflineData","submitRouteResult"];'
NEW7 = '"lvAnswer","syncOfflineData","submitRouteResult","checkTimeline"];'
assert OLD7 in src, "ANCHOR7 (_TRUSTED_FNS) not found"
src = src.replace(OLD7, NEW7, 1)
changes.append("7. Added checkTimeline to _TRUSTED_FNS")

# ─────────────────────────────────────────────────────────────────────────────
# 8. render(): add timeline type block after sonnen_kompass
# ─────────────────────────────────────────────────────────────────────────────
OLD8 = ('}else if(q.type==="sonnen_kompass"){\n'
        '    qBody=`<div class="qprompt">${q.prompt}</div>`'
        '+`<div style="text-align:center;font-size:2.8rem;margin:8px 0 4px">\\u{1F9ED}</div>`'
        '+`${sel!==null?\'<div class="qmeta" style="text-align:center;font-size:.77rem;color:var(--text3);margin-top:4px">\'+esc(q.meta||"")+\'</div>\':\'\'}`;\n'
        '  }else{')

NEW8 = ('}else if(q.type==="sonnen_kompass"){\n'
        '    qBody=`<div class="qprompt">${q.prompt}</div>`'
        '+`<div style="text-align:center;font-size:2.8rem;margin:8px 0 4px">\\u{1F9ED}</div>`'
        '+`${sel!==null?\'<div class="qmeta" style="text-align:center;font-size:.77rem;color:var(--text3);margin-top:4px">\'+esc(q.meta||"")+\'</div>\':\'\'}`;\n'
        '  }else if(q.type==="timeline"){\n'
        '    /* Phase 266: Timeline drag-and-drop */\n'
        '    var _tlShowItems=sel!==null&&q._tlUserOrder\n'
        '      ?q._tlUserOrder.map(function(n){var f=null;for(var _j=0;_j<q.items.length;_j++){if(q.items[_j].n===n){f=q.items[_j];break;}}return f||{n:n,year:\'?\',hint:\'\'};}) \n'
        '      :q.items;\n'
        '    var _tlTilesHtml=_tlShowItems.map(function(it,_i){\n'
        '      var bg=sel!==null&&q._tlUserOrder?(q._tlUserOrder[_i]===q.ans[_i]?\'#d1fae5\':\'#fee2e2\'):\'var(--bg2)\';\n'
        '      var brd=sel!==null&&q._tlUserOrder?(q._tlUserOrder[_i]===q.ans[_i]?\'2px solid #10b981\':\'2px solid #ef4444\'):\'2px solid var(--border)\';\n'
        '      var esc_n=esc(it.n);\n'
        '      var raw_n=it.n.replace(/"/g,\'&quot;\').replace(/\'/g,\'&#39;\');\n'
        '      var drag_attr=sel===null?\'draggable="true"\':\'\' ;\n'
        '      var drag_evts=sel===null\n'
        '        ?\'ondragstart="_tlDragStart(\\\\\'\'+ raw_n +\'\\\\\')" ondragover="_tlDragOver(event)" ondrop="_tlDrop(event,\\\\\'\'+ raw_n +\'\\\\\')" ontouchstart="_tlTouchStart(event,\\\\\'\'+ raw_n +\'\\\\\')" ontouchmove="_tlTouchMove(event)" ontouchend="_tlTouchEnd(event)"\'\n'
        '        :\'\';\n'
        '      var icon_part=sel===null?\'<span style="font-size:1.1rem;opacity:.4;flex-shrink:0">\\u2630</span>\'\n'
        '        :(q._tlUserOrder&&q._tlUserOrder[_i]===q.ans[_i]?\'<span style="color:#10b981;font-weight:700;flex-shrink:0">\\u2713</span>\':\'<span style="color:#ef4444;font-weight:700;flex-shrink:0">\\u2717</span>\');\n'
        '      var year_part=sel!==null&&it.year?\'<span style="font-size:.73rem;color:var(--text3);margin-left:6px">(\'+it.year+\')</span>\':\'\' ;\n'
        '      var hint_part=sel!==null&&it.hint?\'<br><span style="font-size:.7rem;color:var(--text3);font-style:italic">\'+esc(it.hint)+\'</span>\':\'\' ;\n'
        '      return \'<div class="tl-tile" data-tn="\'+raw_n+\'" \'+drag_attr+\' \'+drag_evts\n'
        '        +\' style="background:\'+bg+\';border:\'+brd+\';border-radius:10px;padding:10px 12px;cursor:\'+(sel===null?\'grab\':\'default\')+\';user-select:none;display:flex;align-items:center;gap:10px;touch-action:none">\'\n'
        '        +icon_part\n'
        '        +\'<div style="flex:1"><span style="font-weight:700;font-size:.93rem;color:var(--text)">\'+esc_n+\'</span>\'+year_part+hint_part+\'</div></div>\';\n'
        '    }).join(\'\');\n'
        '    var _tlFb=sel!==null\n'
        '      ?(ok?\'<div class="fb ok" style="text-align:center;margin-bottom:6px">\\u2713 Perfekte Reihenfolge!</div>\'\n'
        '          :\'<div class="fb ng" style="text-align:center;margin-bottom:6px">\\u2717 Falsch &mdash; Korrekt: \'+q.ans.map(function(n,i){return(i+1)+\'. \'+esc(n);}).join(\' \\u2192 \')+\'</div>\')\n'
        '      :\'\';\n'
        '    qBody=\'<div class="qprompt">\'+q.prompt+\'</div>\'\n'
        '      +_tlFb\n'
        '      +\'<div id="tl-list" style="display:flex;flex-direction:column;gap:8px;margin:8px 0 10px">\'\n'
        '      +_tlTilesHtml\n'
        '      +\'</div>\'\n'
        '      +(sel===null?\'<button onclick="checkTimeline()" style="width:100%;padding:13px;background:var(--accent);color:#fff;border:none;border-radius:12px;font-weight:700;font-size:1rem;cursor:pointer">\\u2714 Pr\\u00fcfen</button>\':\'\')\n'
        '      +(sel!==null?\'<div style="text-align:center;font-size:.71rem;color:var(--text3);margin-top:4px">Sortierung nach \'+esc(q.unit||\'Jahr\')+\'</div>\':\'\')+\'\';\n'
        '  }else{')

assert OLD8 in src, "ANCHOR8 (render sonnen_kompass->else) not found"
src = src.replace(OLD8, NEW8, 1)
changes.append("8. Added timeline render block after sonnen_kompass")

# ─────────────────────────────────────────────────────────────────────────────
# 9. .replace() chain: add TIMELINE placeholder
# ─────────────────────────────────────────────────────────────────────────────
OLD9 = "  .replace('PLACEHOLDER_SPORT_WS',    SPORT_WS_J)"
NEW9 = "  .replace('PLACEHOLDER_SPORT_WS',    SPORT_WS_J)\n  .replace('PLACEHOLDER_TIMELINE',     TIMELINE_J)"
assert OLD9 in src, "ANCHOR9 (.replace chain) not found"
src = src.replace(OLD9, NEW9, 1)
changes.append("9. Added PLACEHOLDER_TIMELINE to .replace() chain")

# ─────────────────────────────────────────────────────────────────────────────
# Write back
# ─────────────────────────────────────────────────────────────────────────────
with open(GEN, 'w', encoding='utf-8') as f:
    f.write(src)

new_len = len(src)
print(f"patch_266_timeline_engine.py applied successfully!")
print(f"  gen.py: {original_len:,} → {new_len:,} bytes (+{new_len-original_len:,})")
print(f"  Changes applied ({len(changes)}):")
for c in changes:
    print(f"    ✓ {c}")
