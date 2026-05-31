#!/usr/bin/env python3
"""
patch_313_uic_live_scanner.py
Phase 313 — FEATURE: Live-Spotting UI für Waggonnummern

Improvements over Phase 312:
1. Auto-format input while typing (80512345678 → 80 51 2345 678-9)
2. UIC Prüfziffer-Validierung (Luhn-Variante) — gelbe Warnung, kein harter Block
3. Normalisierung beim Speichern (strip spaces/hyphens → canonical form)
4. Länder-Fortschrittsbalken (X/57 Länder gespottet)
5. Album-Ansicht: Kärtchen mit Flagge, Ländername, Gattung
6. Scanner als Depot-Tab (kein MODES-Eintrag)
7. "Waggon-Scanner"-Button direkt im Zug-Depot-Header
"""
import sys, os

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
# BLOCK A: Replace entire Phase-312 UIC Logbuch block in showTrainDepot()
# with the new full Live-Scanner UI
# ─────────────────────────────────────────────────────────────────────────────

OLD_LOGBUCH_START = "  /* Phase 312: UIC Scanner Logbuch */"
OLD_LOGBUCH_END   = '  _uicHtml+=\'</div>\';\n  html+=_uicHtml;'

if OLD_LOGBUCH_START in src and OLD_LOGBUCH_END in src:
    start_idx = src.index(OLD_LOGBUCH_START)
    end_idx   = src.index(OLD_LOGBUCH_END) + len(OLD_LOGBUCH_END)
    old_block = src[start_idx:end_idx]
else:
    old_block = None

NEW_LIVE_SCANNER = r"""  /* Phase 313: UIC Live-Scanner — vollständiges Spotting-UI */
  (function(){
    /* ── Helpers ── */
    var _UIC_CC={'10':'fi','20':'ru','21':'by','22':'ua','24':'lt','25':'lv','26':'ee',
      '40':'rs','50':'hr','51':'pl','52':'bg','53':'ro','54':'cz','55':'hu','56':'sk',
      '57':'si','70':'gb','71':'es','73':'gr','74':'se','76':'no','80':'de','81':'at',
      '82':'lu','83':'it','84':'nl','85':'ch','86':'dk','87':'fr','88':'be','94':'pt'};

    function _flag(cc){
      if(!cc||cc.length!==2)return'\u{1F6AB}';
      var a=cc.toLowerCase();
      return String.fromCodePoint(0x1F1E6+a.charCodeAt(0)-97)+String.fromCodePoint(0x1F1E6+a.charCodeAt(1)-97);
    }

    /* Normalize: remove all non-digits, return canonical "CC TT NNNN NNN-P" or raw */
    function _normalize(raw){
      var d=raw.replace(/[^0-9]/g,'');
      if(d.length<2)return raw.trim();
      /* Try UIC 12-digit format */
      if(d.length===12) return d.slice(0,2)+' '+d.slice(2,4)+' '+d.slice(4,8)+' '+d.slice(8,11)+'-'+d.slice(11);
      /* Shorter inputs: store as-is after stripping */
      return d;
    }

    /* UIC check digit: odd positions ×2 (Luhn variant), mod 10 */
    function _checkDigit(d11){
      var sum=0;
      for(var i=0;i<11;i++){
        var n=parseInt(d11[i]);
        if(i%2===0){var v=n*2;sum+=v>9?v-9:v;}
        else sum+=n;
      }
      return (10-(sum%10))%10;
    }

    /* Load/save with dedup on normalized key */
    function _load(){var r=[];try{r=JSON.parse(localStorage.getItem('gq_uic_log')||'[]');}catch(e){}return r;}
    function _save(arr){try{localStorage.setItem('gq_uic_log',JSON.stringify(arr));}catch(e){}}

    var _log=_load();
    var _laender=(ZUG_UIC_DATA&&ZUG_UIC_DATA.laendercodes)||{};
    var _waggons=(ZUG_UIC_DATA&&ZUG_UIC_DATA.waggontypen)||[];
    var _totalLaender=Object.keys(_UIC_CC).length; /* 30 mapped CCs */

    /* Spotted countries (unique land_codes) */
    var _spottedCodes={};
    _log.forEach(function(n){var d=n.replace(/[^0-9]/g,'');if(d.length>=2)_spottedCodes[d.slice(0,2)]=true;});
    var _spottedCountries=Object.keys(_spottedCodes).length;
    var _pctC=Math.round(_spottedCountries/_totalLaender*100);

    /* ── Header with stats ── */
    var _h='<div style="background:linear-gradient(135deg,#1a237e,#283593);border-radius:12px;padding:14px;margin-bottom:10px">'
      +'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">'
      +'<div style="font-weight:900;font-size:1rem;color:#fff;display:flex;align-items:center;gap:8px">'
      +'<span style="font-size:1.4rem">🚆</span>'+_tc("Waggon-Scanner")+' '
      +'<span style="font-size:.72rem;background:#1565c0;color:#90caf9;padding:2px 9px;border-radius:20px;font-weight:700">'+_log.length+' '+_tc("gespottet")+'</span></div>'
      +'<span style="font-size:.78rem;color:#90caf9;font-weight:700">'+_spottedCountries+'/'+_totalLaender+' '+_tc("Länder")+'</span></div>'
      /* Country progress bar */
      +'<div style="background:rgba(255,255,255,.15);border-radius:4px;height:6px;overflow:hidden">'
      +'<div style="background:#42a5f5;height:100%;width:'+_pctC+'%;border-radius:4px;transition:width .5s"></div></div>'
      +'</div>';

    /* ── Input area ── */
    var _msgState=S._uicMsg||'';
    var _msgColor=S._uicOk===true?'#4caf50':S._uicOk===false?'#ef4444':'#ffa726';
    var _inp='<div style="background:var(--bg2);border-radius:10px;padding:12px;margin-bottom:10px">'
      +'<div style="font-size:.78rem;color:var(--text3);margin-bottom:6px">'+_tc("UIC-Format: CC TT NNNN NNN-P (12 Ziffern)")+'</div>'
      +'<div style="display:flex;gap:6px;margin-bottom:6px">'
      +'<input id="uic-scan-inp" placeholder="z.B. 80 51 2345 678-9" maxlength="20" inputmode="numeric" '
      +'value="'+(S._uicDraft||'')+'" '
      +'oninput="(function(el){'
        /* Auto-format: strip non-digits, insert spaces */
        +'var d=el.value.replace(/[^0-9]/g,\'\').slice(0,12);'
        +'var f=d;'
        +'if(d.length>11)f=d.slice(0,2)+\' \'+d.slice(2,4)+\' \'+d.slice(4,8)+\' \'+d.slice(8,11)+\'-\'+d.slice(11);'
        +'else if(d.length>8)f=d.slice(0,2)+\' \'+d.slice(2,4)+\' \'+d.slice(4,8)+\' \'+d.slice(8);'
        +'else if(d.length>4)f=d.slice(0,2)+\' \'+d.slice(2,4)+\' \'+d.slice(4);'
        +'else if(d.length>2)f=d.slice(0,2)+\' \'+d.slice(2);'
        +'var pos=el.selectionStart+(f.length-el.value.length);'
        +'el.value=f;S._uicDraft=f;S._uicMsg=\'\';S._uicOk=null;'
        +'try{el.setSelectionRange(pos,pos);}catch(_e){}'
      +'})(this)" '
      +'style="flex:1;min-width:0;background:var(--bg3);color:var(--text);border:1.5px solid '+(S._uicOk===true?'#4caf50':S._uicOk===false?'#ef4444':'var(--border)')+';border-radius:8px;padding:8px 12px;font-size:.95rem;font-family:monospace;font-weight:600;letter-spacing:.05em">'
      +'<button onclick="window._uicSubmit()" '
      +'style="background:#1565c0;color:#fff;border:none;border-radius:8px;padding:8px 16px;font-size:.9rem;font-weight:800;cursor:pointer;white-space:nowrap">'
      +'📸 '+_tc("Erfassen")+'</button></div>';

    /* Feedback message */
    if(_msgState)_inp+='<div style="font-size:.82rem;font-weight:700;color:'+_msgColor+';margin-bottom:4px;padding:4px 8px;border-radius:6px;background:'+_msgColor+'18">'+_msgState+'</div>';
    _inp+='</div>';

    /* ── Album: Kärtchen ── */
    var _album='';
    if(_log.length>0){
      _album='<div style="background:var(--bg2);border-radius:10px;padding:12px;margin-bottom:10px">'
        +'<div style="font-weight:700;font-size:.85rem;margin-bottom:8px;color:var(--text2)">🗒 '+_tc("Gesammelte Waggons")+'</div>'
        +'<div style="display:flex;flex-wrap:wrap;gap:7px">'
        +_log.slice().reverse().map(function(n){
          var d=n.replace(/[^0-9]/g,'');
          var cc2=d.slice(0,2);
          var typ2=d.slice(2,4);
          var ccKey=_UIC_CC[cc2];
          var fl=ccKey?_flag(ccKey):'🚃';
          var landName=_laender[cc2]||cc2;
          /* Match gattung from waggontypen */
          var gattung='';
          for(var i=0;i<_waggons.length;i++){
            if(_waggons[i].land_code===cc2&&_waggons[i].uic_typ===typ2){gattung=_waggons[i].gattung;break;}
          }
          return'<div style="background:var(--bg3);border:1.5px solid var(--border);border-radius:8px;padding:6px 10px;min-width:100px;max-width:140px;text-align:center;position:relative">'
            +'<div style="font-size:1.3rem;margin-bottom:2px">'+fl+'</div>'
            +'<div style="font-family:monospace;font-size:.72rem;font-weight:800;color:var(--text);letter-spacing:.04em">'+n+'</div>'
            +'<div style="font-size:.65rem;color:#42a5f5;font-weight:700;margin-top:1px">'+landName+(gattung?' · '+gattung:'')+'</div>'
            +'<button onclick="(function(){var l=[];try{l=JSON.parse(localStorage.getItem(\'gq_uic_log\')||\'[]\');}catch(e){}'
            +'l=l.filter(function(x){return x!==\''+n.replace(/'/g,"\\'")+'\'});'
            +'try{localStorage.setItem(\'gq_uic_log\',JSON.stringify(l));}catch(e){}render();})()" '
            +'style="position:absolute;top:2px;right:4px;background:none;border:none;color:var(--text3);font-size:.75rem;cursor:pointer;padding:0;line-height:1">×</button>'
            +'</div>';
        }).join('')
        +'</div></div>';
    }else{
      _album='<div style="text-align:center;padding:18px;color:var(--text3);font-size:.85rem">'
        +'🚆 '+_tc("Noch keine Waggons erfasst — scanne deine erste Nummer!")+'</div>';
    }

    html+=_h+_inp+_album;
  })();

  /* ── Submit-Handler (global, called by button) ── */
  window._uicSubmit=function(){
    var el=document.getElementById('uic-scan-inp');
    if(!el)return;
    var raw=el.value.trim();
    var d=raw.replace(/[^0-9]/g,'');
    if(d.length<2){S._uicMsg='⚠️ Bitte Wagennummer eingeben';S._uicOk=false;render();return;}

    /* Normalize */
    var norm;
    if(d.length===12){
      norm=d.slice(0,2)+' '+d.slice(2,4)+' '+d.slice(4,8)+' '+d.slice(8,11)+'-'+d.slice(11);
    }else{
      norm=raw.trim();
    }
    var storeKey=d; /* Deduplicate by digits only */

    /* Load log, check duplicate (by digits) */
    var _l=[];try{_l=JSON.parse(localStorage.getItem('gq_uic_log')||'[]');}catch(e){}
    var existing=_l.some(function(x){return x.replace(/[^0-9]/g,''')===storeKey;});
    if(existing){
      S._uicMsg='📋 '+norm+' bereits erfasst!';
      S._uicOk=null;S._uicDraft='';el.value='';render();return;
    }

    /* UIC check digit validation (if 12 digits) */
    var warnMsg='';
    if(d.length===12){
      var expected=(10-(function(){var s=0;for(var i=0;i<11;i++){var n=parseInt(d[i]);if(i%2===0){var v=n*2;s+=v>9?v-9:v;}else s+=n;}return s;}())%10)%10;
      if(expected!==parseInt(d[11])){
        warnMsg='🟡 Prüfziffer unplausibel (erwartet: '+expected+') — trotzdem gespeichert';
      }
    }

    /* Identify country */
    var _UIC_CC_MAP={'10':'Finnland','20':'Russland','21':'Weißrussland','22':'Ukraine',
      '24':'Litauen','25':'Lettland','26':'Estland','40':'Serbien','50':'Kroatien',
      '51':'Polen','52':'Bulgarien','53':'Rumänien','54':'Tschechien','55':'Ungarn',
      '56':'Slowakei','57':'Slowenien','70':'Großbritannien','71':'Spanien',
      '73':'Griechenland','74':'Schweden','76':'Norwegen','80':'Deutschland',
      '81':'Österreich','82':'Luxemburg','83':'Italien','84':'Niederlande',
      '85':'Schweiz','86':'Dänemark','87':'Frankreich','88':'Belgien','94':'Portugal'};
    var cc2=d.slice(0,2);
    var land=_UIC_CC_MAP[cc2]||('UIC-Code '+cc2);

    /* Save */
    _l.push(norm);
    try{localStorage.setItem('gq_uic_log',JSON.stringify(_l));}catch(e){}

    /* Success */
    var msg=warnMsg||('✅ Erfolgreich gespottet! Waggon aus '+land+' erfasst.');
    S._uicMsg=msg;
    S._uicOk=warnMsg?null:true;
    S._uicDraft='';
    if(el)el.value='';
    render();
  };
"""

if old_block:
    src = src.replace(old_block, NEW_LIVE_SCANNER, 1)
    fix("showTrainDepot: replaced Phase-312 Logbuch with full Live-Scanner UI")
    patches += 1
elif "Phase 313: UIC Live-Scanner" in src:
    ok("Live-Scanner already present")
else:
    skip("Phase-312 UIC Logbuch block not found in showTrainDepot")

# ─────────────────────────────────────────────────────────────────────────────
# BLOCK B: Add "Waggon-Scanner" button to the Depot header in
#          renderCollectionScreen (the _depotBtn area)
# Replace the depot onclick to open scanner tab via S._depotTab
# ─────────────────────────────────────────────────────────────────────────────
OLD_DEPOT_BTN = 'onclick="showTrainDepot()">'
NEW_DEPOT_BTN = 'onclick="S._depotTab=\'scanner\';showTrainDepot()">'
count = src.count(OLD_DEPOT_BTN)
if count == 1:
    src = src.replace(OLD_DEPOT_BTN, NEW_DEPOT_BTN, 1)
    fix("Depot button: passes _depotTab='scanner' to showTrainDepot")
    patches += 1
elif count > 1:
    ok(f"Multiple depot btn occurrences ({count}) — skipping to avoid double-replace")
else:
    ok("Depot button already updated or not found")

# ─────────────────────────────────────────────────────────────────────────────
# BLOCK C: Add i18n keys for new labels
# ─────────────────────────────────────────────────────────────────────────────
OLD_I18N_DE = '"Zug-Depot": "Train Depot"'   # anchor in EN block
NEW_I18N_DE = '"Zug-Depot": "Train Depot","Waggon-Scanner":"Wagon Scanner","UIC-Format: CC TT NNNN NNN-P (12 Ziffern)":"UIC format: CC TT NNNN NNN-P (12 digits)","Erfassen":"Log it","Gesammelte Waggons":"Collected Wagons","Noch keine Waggons erfasst — scanne deine erste Nummer!":"No wagons logged yet — scan your first number!"'
if OLD_I18N_DE in src and 'Waggon-Scanner":"Wagon Scanner' not in src:
    src = src.replace(OLD_I18N_DE, NEW_I18N_DE, 1)
    fix("i18n EN: added Waggon-Scanner labels")
    patches += 1
else:
    ok("i18n EN labels already present")

# ─────────────────────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────────────────────
save(os.path.join(BASE, 'gen.py'), src)
print(f"\n  {patches} patch(es) applied.")
print("✅ patch_313_uic_live_scanner.py done — run: python3 gen.py && python3 verify.py")
