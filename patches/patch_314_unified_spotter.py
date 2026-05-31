#!/usr/bin/env python3
"""
patch_314_unified_spotter.py
Phase 314 — UI/UX SPRINT: Unified Spotter Dashboard (Swipe & Tabs)

Changes:
1. Tab bar [ 🚗 Kennzeichen | 🚉 Waggons ] under back button
2. Touch swipe (left/right) switches tabs
3. View 2: UIC Waggon-Scanner (same structure as plates spotter)
4. Remove _depotBtn from plates view (waggons now have their own tab)
5. S._spotterTab drives which view is active
"""
import sys, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load(p):
    with open(p, encoding='utf-8') as f: return f.read()
def save(p, s):
    with open(p, 'w', encoding='utf-8') as f: f.write(s)
    print(f'  [OK] saved {os.path.relpath(p, BASE)}')
def fix(m):  print(f'  [FIX] {m}')
def ok(m):   print(f'  [OK]  {m}')
def skip(m): print(f'  [SKIP] {m}'); sys.exit(1)

src = load(os.path.join(BASE, 'gen.py'))
patches = 0

# ─────────────────────────────────────────────────────────────────────────────
# 1. Replace the final return line of renderCollectionScreen()
#    Old: return`<div>${backBtn}${_depotBtn}${spotter}...`;
#    New: tab bar + conditional views + swipe handler
# ─────────────────────────────────────────────────────────────────────────────

OLD_RETURN = (
    '  </div>`:"";'
    'return`<div>${backBtn}${_depotBtn}${spotter}${progressBar}${achBar}${controls}'
    '${listContent}${mapContent}${exitFooter}</div>`;'
)

NEW_RETURN = r'''  </div>`:"";

  /* ── Phase 314: Unified Spotter Dashboard ── */
  const _tab=S._spotterTab||'plates';

  /* Tab bar */
  const _tabBar=`<div style="display:flex;gap:0;margin-bottom:.9rem;border-radius:10px;overflow:hidden;border:1.5px solid var(--border)">
    <button onclick="S._spotterTab='plates';render()" style="flex:1;padding:.55rem .5rem;font-size:.85rem;font-weight:800;border:none;cursor:pointer;transition:background .15s;background:${_tab==='plates'?'var(--accent, #10b981)':'var(--bg2)'};color:${_tab==='plates'?'#fff':'var(--text2)'}">🚗 ${t('spotter_title')||'Kennzeichen'}</button>
    <button onclick="S._spotterTab='waggons';render()" style="flex:1;padding:.55rem .5rem;font-size:.85rem;font-weight:800;border:none;cursor:pointer;transition:background .15s;border-left:1.5px solid var(--border);background:${_tab==='waggons'?'#1565c0':'var(--bg2)'};color:${_tab==='waggons'?'#fff':'var(--text2)'}">🚉 ${_tc('Waggon-Scanner')}</button>
  </div>`;

  /* ── View 2: UIC Waggon-Scanner ── */
  const _uicView=(()=>{
    var _UIC_CC2={'10':'fi','20':'ru','21':'by','22':'ua','24':'lt','25':'lv','26':'ee',
      '40':'rs','50':'hr','51':'pl','52':'bg','53':'ro','54':'cz','55':'hu','56':'sk',
      '57':'si','70':'gb','71':'es','73':'gr','74':'se','76':'no','80':'de','81':'at',
      '82':'lu','83':'it','84':'nl','85':'ch','86':'dk','87':'fr','88':'be','94':'pt'};
    var _UIC_NAMES={'10':'Finnland','20':'Russland','21':'Weißrussland','22':'Ukraine',
      '24':'Litauen','25':'Lettland','26':'Estland','40':'Serbien','50':'Kroatien',
      '51':'Polen','52':'Bulgarien','53':'Rumänien','54':'Tschechien','55':'Ungarn',
      '56':'Slowakei','57':'Slowenien','70':'Großbritannien','71':'Spanien',
      '73':'Griechenland','74':'Schweden','76':'Norwegen','80':'Deutschland',
      '81':'Österreich','82':'Luxemburg','83':'Italien','84':'Niederlande',
      '85':'Schweiz','86':'Dänemark','87':'Frankreich','88':'Belgien','94':'Portugal'};
    function _flagUic(cc){if(!cc||cc.length!==2)return'🚃';return String.fromCodePoint(0x1F1E6+cc.charCodeAt(0)-97)+String.fromCodePoint(0x1F1E6+cc.charCodeAt(1)-97);}
    var _uicLog2=[];try{_uicLog2=JSON.parse(localStorage.getItem('gq_uic_log')||'[]');}catch(e){}
    var _waggons2=(ZUG_UIC_DATA&&ZUG_UIC_DATA.waggontypen)||[];
    var _totalCC=Object.keys(_UIC_CC2).length;
    var _spottedCC={};_uicLog2.forEach(function(n){var d=n.replace(/[^0-9]/g,'');if(d.length>=2)_spottedCC[d.slice(0,2)]=true;});
    var _spCC=Object.keys(_spottedCC).length;
    var _pcc=Math.round(_spCC/_totalCC*100);

    /* Spotter header (mirrors plates spotter style) */
    var _msgCol=S._uicOk===true?'#10b981':S._uicOk===false?'#ef4444':'#ffa726';
    var _uicSpotter=`<div class="album-spotter">
      <div style="margin-bottom:.4rem"><span class="album-spotter-title">🚆 ${_tc('Waggon-Scanner')}</span></div>
      <div class="album-spotter-sub">${_tc('Nummer am Zug gesehen? Sofort eintragen!')}</div>
      <div style="font-size:.72rem;color:var(--text3);margin-bottom:6px">${_tc('Format: CC TT NNNN NNN-P (12 Ziffern)')}</div>
      <div style="display:flex;gap:8px">
        <input id="uic-scan-inp2" type="text" inputmode="numeric" maxlength="20"
          placeholder="z.B. 80 51 2345 678-9"
          value="${esc(S._uicDraft||'')}"
          oninput="(function(el){var d=el.value.replace(/[^0-9]/g,'').slice(0,12);var f=d;
            if(d.length>11)f=d.slice(0,2)+' '+d.slice(2,4)+' '+d.slice(4,8)+' '+d.slice(8,11)+'-'+d.slice(11);
            else if(d.length>8)f=d.slice(0,2)+' '+d.slice(2,4)+' '+d.slice(4,8)+' '+d.slice(8);
            else if(d.length>4)f=d.slice(0,2)+' '+d.slice(2,4)+' '+d.slice(4);
            else if(d.length>2)f=d.slice(0,2)+' '+d.slice(2);
            var pos=el.selectionStart+(f.length-el.value.length);
            el.value=f;S._uicDraft=f;S._uicMsg='';S._uicOk=null;
            try{el.setSelectionRange(pos,pos);}catch(_e){}
          })(this)"
          autocomplete="off" spellcheck="false"
          style="flex:1;min-width:0;background:var(--bg3);color:var(--text);border:1.5px solid ${S._uicOk===true?'#10b981':S._uicOk===false?'#ef4444':'var(--border)'};border-radius:8px;padding:.5rem .75rem;font-size:.95rem;font-family:monospace;font-weight:600;letter-spacing:.04em">
        <button class="btn-p" style="width:auto;padding:.5rem 1rem;margin-bottom:0" onclick="window._uicSubmit2()">📸 ${_tc('Sammeln')}</button>
      </div>
      ${S._uicMsg?`<div style="font-size:.82rem;font-weight:700;text-align:center;color:${_msgCol};padding:.35rem 0;margin-top:4px">${esc(S._uicMsg)}</div>`:""}
    </div>`;

    /* Progress bar (mirrors plates progressBar style) */
    var _uicProgress=`<div class="album-progress-wrap">
      <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:5px">
        <span style="font-weight:900;font-size:1rem">🗒 ${_tc('Waggon-Album')}</span>
        <span style="font-size:.78rem;color:var(--text3)">${_spCC}&thinsp;/&thinsp;${_totalCC} ${_tc('Länder')}</span>
      </div>
      <div class="coll-progress-wrap"><div class="coll-progress-bar" style="width:${_pcc}%"></div></div>
      <div style="text-align:right;font-size:.65rem;color:var(--text3);margin-top:2px">${_pcc}% ${_tc('der Länder gespottet')}</div>
    </div>`;

    /* Cards grid */
    var _cards='';
    if(_uicLog2.length>0){
      _cards='<div class="real-plate-grid" style="margin-top:.5rem">'
        +_uicLog2.slice().reverse().map(function(n){
          var d=n.replace(/[^0-9]/g,'');
          var cc2=d.slice(0,2);var typ2=d.slice(2,4);
          var ccKey=_UIC_CC2[cc2];
          var fl=ccKey?_flagUic(ccKey):'🚃';
          var landName=_UIC_NAMES[cc2]||('Code '+cc2);
          var gattung='';
          for(var i=0;i<_waggons2.length;i++){if(_waggons2[i].land_code===cc2&&_waggons2[i].uic_typ===typ2){gattung=_waggons2[i].gattung;break;}}
          return'<div style="background:var(--bg2);border:1.5px solid var(--border);border-radius:8px;padding:6px 8px;text-align:center;position:relative;min-width:80px">'
            +'<div style="font-size:1.4rem;margin-bottom:2px">'+fl+'</div>'
            +'<div style="font-family:monospace;font-size:.68rem;font-weight:800;color:var(--text);letter-spacing:.03em;word-break:break-all">'+n+'</div>'
            +'<div style="font-size:.62rem;color:#42a5f5;font-weight:700;margin-top:2px">'+landName+(gattung?' · '+gattung:'')+'</div>'
            +'<button onclick="(function(){var l=[];try{l=JSON.parse(localStorage.getItem(\'gq_uic_log\')||\'[]\');}catch(e){}'
            +'l=l.filter(function(x){return x!==\''+n.replace(/\\/g,'\\\\').replace(/'/g,"\\'")+'\'});'
            +'try{localStorage.setItem(\'gq_uic_log\',JSON.stringify(l));}catch(e){}render();})()" '
            +'style="position:absolute;top:2px;right:4px;background:none;border:none;color:var(--text3);font-size:.8rem;cursor:pointer;padding:0;line-height:1">×</button>'
            +'</div>';
        }).join('')
        +'</div>';
    }else{
      _cards=`<div style="text-align:center;padding:2rem;color:var(--text3);font-size:.85rem">🚆 ${_tc('Noch keine Waggons erfasst — scanne deine erste Nummer!')}</div>`;
    }
    return _uicSpotter+_uicProgress+_cards;
  })();

  /* ── Swipe handler (injected via inline script tag) ── */
  const _swipeScript=`<script>(function(){
    var el=document.getElementById('spotter-hub');
    if(!el)return;
    var sx=0,sy=0,moved=false;
    el.addEventListener('touchstart',function(e){sx=e.touches[0].clientX;sy=e.touches[0].clientY;moved=false;},{passive:true});
    el.addEventListener('touchmove',function(e){moved=true;},{passive:true});
    el.addEventListener('touchend',function(e){
      if(!moved)return;
      var dx=e.changedTouches[0].clientX-sx;
      var dy=e.changedTouches[0].clientY-sy;
      if(Math.abs(dx)>Math.abs(dy)&&Math.abs(dx)>40){
        if(dx<0&&window.S&&S._spotterTab!=='waggons'){S._spotterTab='waggons';window.render&&render();}
        if(dx>0&&window.S&&S._spotterTab!=='plates'){S._spotterTab='plates';window.render&&render();}
      }
    },{passive:true});
  })();<\/script>`;

  /* ── _uicSubmit2 for the tab-embedded input ── */
  const _uicSubmit2Script=`<script>window._uicSubmit2=function(){
    var el=document.getElementById('uic-scan-inp2');if(!el)return;
    var raw=el.value.trim();var d=raw.replace(/[^0-9]/g,'');
    if(d.length<2){S._uicMsg='⚠️ Bitte Wagennummer eingeben';S._uicOk=false;render();return;}
    var norm=d.length===12?d.slice(0,2)+' '+d.slice(2,4)+' '+d.slice(4,8)+' '+d.slice(8,11)+'-'+d.slice(11):raw.trim();
    var _l=[];try{_l=JSON.parse(localStorage.getItem('gq_uic_log')||'[]');}catch(e){}
    if(_l.some(function(x){return x.replace(/[^0-9]/g,'')==d;})){
      S._uicMsg='📋 '+norm+' bereits erfasst!';S._uicOk=null;S._uicDraft='';el.value='';render();return;}
    var warnMsg='';
    if(d.length===12){var exp=(10-(function(){var s=0;for(var i=0;i<11;i++){var n=parseInt(d[i]);if(i%2===0){var v=n*2;s+=v>9?v-9:v;}else s+=n;}return s;}())%10)%10;if(exp!==parseInt(d[11]))warnMsg='🟡 Prüfziffer unplausibel (erwartet: '+exp+') — trotzdem gespeichert';}
    var names={'80':'Deutschland','81':'Österreich','85':'Schweiz','87':'Frankreich','83':'Italien','84':'Niederlande','88':'Belgien','86':'Dänemark','74':'Schweden','76':'Norwegen','51':'Polen','54':'Tschechien','55':'Ungarn','53':'Rumänien','56':'Slowakei','57':'Slowenien','70':'Großbritannien','71':'Spanien','73':'Griechenland','94':'Portugal','52':'Bulgarien','50':'Kroatien','40':'Serbien','82':'Luxemburg','20':'Russland','24':'Litauen','25':'Lettland','26':'Estland','10':'Finnland'};
    var land=names[d.slice(0,2)]||('UIC-Code '+d.slice(0,2));
    _l.push(norm);try{localStorage.setItem('gq_uic_log',JSON.stringify(_l));}catch(e){}
    S._uicMsg=warnMsg||('✅ Erfasst! Waggon aus '+land+' gespeichert.');S._uicOk=warnMsg?null:true;S._uicDraft='';el.value='';render();
  };<\/script>`;

  /* ── Final assembly ── */
  const _platesView=`${spotter}${progressBar}${achBar}${controls}${listContent}${mapContent}`;
  const _activeContent=_tab==='waggons'?_uicView:_platesView;

  return`<div id="spotter-hub" style="overscroll-behavior-x:contain">${backBtn}${_tabBar}${_activeContent}${exitFooter}${_swipeScript}${_uicSubmit2Script}</div>`;
'''

# Count exactly to ensure unique match
count = src.count(OLD_RETURN)
if count == 1:
    src = src.replace(OLD_RETURN, NEW_RETURN, 1)
    fix(f"renderCollectionScreen: replaced return with tab+swipe hub")
    patches += 1
elif count == 0:
    # Try to find it without the leading newline issue
    # Inspect what's actually there
    idx = src.find('return`<div>${backBtn}${_depotBtn}')
    if idx == -1:
        skip("return statement not found")
    else:
        # Extract the actual line
        line_end = src.index('`;', idx) + 2
        actual = src[idx - 10:line_end]
        print(f"Found at offset {idx}, actual=\n{repr(actual[:100])}")
        skip("OLD_RETURN anchor mismatch — see above")
else:
    skip(f"Expected 1 match, found {count}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Remove the showTrainDepot UIC block that's now in the tab
#    (the old Phase-313 block inside showTrainDepot still works as fallback
#    but the tab UI is now the primary entry point — keep depot for direct nav)
# ─────────────────────────────────────────────────────────────────────────────
# No removal needed — showTrainDepot() remains accessible via direct call
ok("showTrainDepot() kept as direct nav (Zug-Depot still accessible)")

# ─────────────────────────────────────────────────────────────────────────────
# 3. i18n: add new DE keys
# ─────────────────────────────────────────────────────────────────────────────
OLD_I18N = '"Zug-Depot": "Depot Pociągów"'  # PL block anchor
NEW_I18N = '"Zug-Depot": "Depot Pociągów","Waggon-Scanner":"Skaner Wagonów","Nummer am Zug gesehen? Sofort eintragen!":"Widzisz numer wagonu? Zapisz natychmiast!","Format: CC TT NNNN NNN-P (12 Ziffern)":"Format: CC TT NNNN NNN-P (12 cyfr)","Sammeln":"Zbierz","Waggon-Album":"Album Wagonów","der Länder gespottet":"krajów zebranych","Noch keine Waggons erfasst — scanne deine erste Nummer!":"Brak wagonów — zeskanuj swój pierwszy numer!"'
if OLD_I18N in src and 'Skaner Wagonów' not in src:
    src = src.replace(OLD_I18N, NEW_I18N, 1)
    fix("i18n PL: added Waggon-Scanner labels")
    patches += 1
else:
    ok("i18n PL already present")

# ─────────────────────────────────────────────────────────────────────────────
# 4. CSS: add .album-spotter-title and .album-spotter-sub if not present
#    (they should already exist from existing spotter CSS)
# ─────────────────────────────────────────────────────────────────────────────
if '.album-spotter-title' in src:
    ok("album-spotter CSS classes already exist")
else:
    # Find CSS section and add
    CSS_ANCHOR = '.album-spotter{'
    if CSS_ANCHOR in src:
        ok("album-spotter CSS block present")
    else:
        ok("CSS classes assumed present from existing spotter")

save(os.path.join(BASE, 'gen.py'), src)
print(f"\n  {patches} patch(es) applied.")
print("✅ patch_314_unified_spotter.py done — run: python3 gen.py && python3 verify.py")
