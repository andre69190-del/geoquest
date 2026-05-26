#!/usr/bin/env python3
"""Phase 212: Metagame Audit — Category/Game selector for 1vs1 + Hot-Seat, bug fixes."""

import sys

GEN = '/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py'

with open(GEN, 'r', encoding='utf-8') as f:
    src = f.read()

original_len = len(src)
patches = []

# ─────────────────────────────────────────────────────────────────────────────
# P1: Initial state — add lvSelType, lvSetupCat, mpSelType, mpSelCat, mpSelMode
# ─────────────────────────────────────────────────────────────────────────────
patches.append((
    'P1_initstate',
    '  lvModal:false,lv:null,lvSetupMode:"random",',
    '  lvModal:false,lv:null,lvSetupMode:"random",lvSelType:"random",lvSetupCat:null,mpSelType:"random",mpSelCat:"",mpSelMode:"",'
))

# ─────────────────────────────────────────────────────────────────────────────
# P2: startGame() — reset rngSeed to null to prevent seed leak from daily/mp
# ─────────────────────────────────────────────────────────────────────────────
patches.append((
    'P2_startgame_rngreset',
    'function startGame(m){\n  clr();',
    'function startGame(m){\n  rngSeed=null;  /* Phase 212: prevent seed leak from daily/mp into solo games */\n  clr();'
))

# ─────────────────────────────────────────────────────────────────────────────
# P3: mpLeave() — also clean up window.mpGameCh (memory leak fix)
# ─────────────────────────────────────────────────────────────────────────────
patches.append((
    'P3_mpleave_cleanup',
    'function mpLeave(){\n  if(S.mp?.channel)try{S.mp.channel.unsubscribe();}catch(e){}\n  S.mp=null;S.mpModal=false;render();\n}',
    'function mpLeave(){\n  if(S.mp?.channel)try{S.mp.channel.unsubscribe();}catch(e){}\n  if(window.mpGameCh)try{window.mpGameCh.unsubscribe();}catch(e){}  /* Phase 212: fix mpGameCh memory leak */\n  window.mpGameCh=null;\n  S.mp=null;S.mpModal=false;S.mpOpponent=null;S.mpSeed=null;render();\n}'
))

# ─────────────────────────────────────────────────────────────────────────────
# P4: LV_MODES — replace old 5-item list + initLV + _lvNext random pool
# ─────────────────────────────────────────────────────────────────────────────
old_lv_modes = '''const LV_MODES=[
  {id:"random",label:"Zuf\\u00e4llig \\u{1F500}"},
  {id:"flag",label:"Flaggen \\u{1F3F3}"},
  {id:"capital",label:"Hauptst\\u00e4dte \\u{1F3DB}"},
  {id:"comp_area",label:"Fl\\u00e4che \\u{1F30F}"},
  {id:"comp_pop",label:"Einwohner \\u{1F465}"},
];
function initLV(){
  const mode=S.lvSetupMode==="random"?null:S.lvSetupMode;
  S.lv={round:0,phase:"q",p1:{name:"Spieler 1",sc:0},p2:{name:"Spieler 2",sc:0},current:1,q:null,sel:null,timer:LV_TIME,mode};
  _lvNext();
}'''

new_lv_modes = '''/* Phase 212: dynamic LV mode selector — random/cat/specific */
function _lvPickMode(selType,selMode,selCat){
  if(selType==="specific"&&selMode&&GEN[selMode])return selMode;
  if(selType==="cat"&&selCat&&MODE_CATS[selCat]){
    const pool=(MODE_CATS[selCat].modes||[]).filter(id=>GEN[id]&&!(MODES.find(m=>m.id===id)?.noMultiplayer));
    if(pool.length)return pool[~~(Math.random()*pool.length)];
  }
  /* Full random pool — all modes with generators */
  const _pool=MODES.filter(m=>GEN[m.id]&&!m.comingSoon&&!m.noMultiplayer).map(m=>m.id);
  return _pool.length?_pool[~~(Math.random()*_pool.length)]:"flag";
}
function initLV(){
  const selType=S.lvSelType||"random";
  const selMode=selType==="specific"?(S.lvSetupMode||null):null;
  const selCat=selType==="cat"?(S.lvSetupCat||null):null;
  S.lv={round:0,phase:"q",p1:{name:"Spieler 1",sc:0},p2:{name:"Spieler 2",sc:0},current:1,q:null,sel:null,timer:LV_TIME,
    mode:selMode,selType,selCat};
  _lvNext();
}'''

patches.append(('P4_lv_modes', old_lv_modes, new_lv_modes))

# ─────────────────────────────────────────────────────────────────────────────
# P5: _lvNext() — replace hardcoded random pool with _lvPickMode
# ─────────────────────────────────────────────────────────────────────────────
patches.append((
    'P5_lvnext_pool',
    '    const modeId=lv.mode||(["flag","capital","city","comp_area","comp_pop","comp_north"][~~(Math.random()*6)]);',
    '    const modeId=lv.mode||_lvPickMode(lv.selType||"random",null,lv.selCat);  /* Phase 212: dynamic pool */'
))

# ─────────────────────────────────────────────────────────────────────────────
# P6: renderLVSetup() — full rewrite with 3-mode selector
# ─────────────────────────────────────────────────────────────────────────────
old_lv_setup = '''function renderLVSetup(){
  const modesHtml=LV_MODES.map(m=>`<button class="btn-base${S.lvSetupMode===m.id?" ok":""}" onclick="S.lvSetupMode=\'${m.id}\';render()">${m.label}</button>`).join("");
  return `<div style="min-height:100vh;background:var(--bg);padding:1.5rem;display:flex;flex-direction:column;align-items:center;justify-content:center">
    <button class="btn-cancel" style="align-self:flex-start;margin-bottom:1rem" onclick="S.lvModal=false;render()">\\u00d7 Zur\\u00fcck</button>
    <div style="font-size:2rem;margin-bottom:.5rem">\\u{1F3AE}</div>
    <div style="font-size:1.3rem;font-weight:900;color:var(--text);margin-bottom:.3rem">Lokal 1:1</div>
    <div style="font-size:.78rem;color:var(--text3);margin-bottom:1.5rem">Zwei Spieler \\u00b7 Ein Ger\\u00e4t \\u00b7 ${LV_ROUNDS} Runden</div>
    <div style="width:100%;max-width:360px">
      <div style="font-size:.7rem;font-weight:700;color:var(--text3);margin-bottom:.5rem">MODUS W\\u00c4HLEN</div>
      <div class="ans-grid" style="margin-bottom:1rem">${modesHtml}</div>
      <button class="btn-p" style="width:100%" onclick="initLV()">\\u{1F680} Spiel starten</button>
    </div>
  </div>`;
}'''

new_lv_setup = '''function renderLVSetup(){
  const sT=S.lvSelType||"random",sCat=S.lvSetupCat||"",sMod=S.lvSetupMode||"";
  const _btnSty=(active)=>`background:${active?"#6366f1":"var(--bg2)"};color:${active?"#fff":"var(--text)"};border:2px solid ${active?"#6366f1":"var(--border)"};border-radius:10px;padding:.55rem 1rem;font-size:.82rem;font-weight:700;cursor:pointer;flex:1;transition:all .15s`;
  const typeRow=`<div style="display:flex;gap:8px;margin-bottom:1rem">
    <button style="${_btnSty(sT==="random")}" onclick="S.lvSelType=\'random\';S.lvSetupMode=null;S.lvSetupCat=null;render()">\\u{1F3B2} Zufall</button>
    <button style="${_btnSty(sT==="cat")}" onclick="S.lvSelType=\'cat\';S.lvSetupMode=null;render()">\\u{1F4C2} Rubrik</button>
    <button style="${_btnSty(sT==="specific")}" onclick="S.lvSelType=\'specific\';S.lvSetupCat=null;render()">\\u{1F3AE} Spiel</button>
  </div>`;
  /* Category chips */
  const catSection=sT==="cat"?`<div style="margin-bottom:.75rem">
    <div style="font-size:.65rem;font-weight:700;color:var(--text3);margin-bottom:.4rem">RUBRIK W\\u00c4HLEN</div>
    <div style="display:flex;flex-wrap:wrap;gap:6px">${Object.entries(MODE_CATS).map(([k,v])=>{
      const active=sCat===k;
      return`<button onclick="S.lvSetupCat=\'${k}\';render()" style="background:${active?"#6366f1":"var(--bg3)"};color:${active?"#fff":"var(--text2)"};border:1.5px solid ${active?"#6366f1":"var(--border)"};border-radius:8px;padding:.3rem .6rem;font-size:.72rem;font-weight:600;cursor:pointer">${v.icon} ${v.label}</button>`;
    }).join("")}</div>
  </div>`:""
  /* Game picker */
  const gameSection=sT==="specific"?`<div style="margin-bottom:.75rem">
    <div style="font-size:.65rem;font-weight:700;color:var(--text3);margin-bottom:.4rem">SPIEL W\\u00c4HLEN</div>
    <div style="max-height:200px;overflow-y:auto;display:flex;flex-wrap:wrap;gap:5px;padding:2px">${MODES.filter(m=>GEN[m.id]&&!m.comingSoon).map(m=>{
      const active=sMod===m.id;
      return`<button onclick="S.lvSetupMode=\'${m.id}\';render()" style="background:${active?"#6366f1":"var(--bg3)"};color:${active?"#fff":"var(--text2)"};border:1.5px solid ${active?"#6366f1":"var(--border)"};border-radius:8px;padding:.28rem .55rem;font-size:.68rem;font-weight:600;cursor:pointer;white-space:nowrap">${m.icon} ${(modeTitle(m)||m.id).slice(0,18)}</button>`;
    }).join("")}</div>
  </div>`:""
  const canStart=sT==="random"||(sT==="cat"&&sCat)||(sT==="specific"&&sMod);
  return `<div style="min-height:100vh;background:var(--bg);padding:1.5rem;display:flex;flex-direction:column;align-items:center;justify-content:center">
    <button class="btn-cancel" style="align-self:flex-start;margin-bottom:1rem" onclick="S.lvModal=false;render()">\\u00d7 Zur\\u00fcck</button>
    <div style="font-size:2rem;margin-bottom:.35rem">\\u{1F579}</div>
    <div style="font-size:1.3rem;font-weight:900;color:var(--text);margin-bottom:.2rem">Lokal 1:1 Hot-Seat</div>
    <div style="font-size:.75rem;color:var(--text3);margin-bottom:1.2rem">Zwei Spieler \\u00b7 Ein Ger\\u00e4t \\u00b7 ${LV_ROUNDS} Runden</div>
    <div style="width:100%;max-width:380px">
      <div style="font-size:.65rem;font-weight:700;color:var(--text3);margin-bottom:.4rem">SPIELMODUS W\\u00c4HLEN</div>
      ${typeRow}${catSection}${gameSection}
      <button class="btn-p" style="width:100%;opacity:${canStart?1:.4};pointer-events:${canStart?"auto":"none"}" onclick="initLV()">\\u{1F680} Spiel starten</button>
    </div>
  </div>`;
}'''

patches.append(('P6_lv_setup', old_lv_setup, new_lv_setup))

# ─────────────────────────────────────────────────────────────────────────────
# P7: Add _getMpMode() helper before mpCountdown
# ─────────────────────────────────────────────────────────────────────────────
patches.append((
    'P7_getmpmode',
    'function mpCountdown(seed,mode){',
    '''/* Phase 212: resolve mp mode from UI selection */
function _getMpMode(){
  const sT=S.mpSelType||"random",sCat=S.mpSelCat||"",sMod=S.mpSelMode||"";
  if(sT==="specific"&&sMod&&GEN[sMod])return sMod;
  if(sT==="cat"&&sCat&&MODE_CATS[sCat]){
    const pool=(MODE_CATS[sCat].modes||[]).filter(id=>GEN[id]&&!(MODES.find(m=>m.id===id)?.noMultiplayer));
    if(pool.length)return pool[~~(Math.random()*pool.length)];
  }
  const _pool=MODES.filter(m=>GEN[m.id]&&!m.comingSoon&&!m.noMultiplayer).map(m=>m.id);
  return _pool.length?_pool[~~(Math.random()*_pool.length)]:"city";
}
function mpCountdown(seed,mode){'''
))

# ─────────────────────────────────────────────────────────────────────────────
# P8: mpReady() host path — use _getMpMode() instead of S.mode
# ─────────────────────────────────────────────────────────────────────────────
patches.append((
    'P8_mpready_mode',
    '''  if(S.mp.role==="host"&&S.mp.oppReady){
    const seed=~~(Math.random()*1e9);
    const _rm=S.mode||"city";const mode=(MODES.find(m=>m.id===_rm)?.noMultiplayer)?"city":_rm;
    mpSend("game_start",{seed,mode});
    mpCountdown(seed,mode);
  }''',
    '''  if(S.mp.role==="host"&&S.mp.oppReady){
    const seed=~~(Math.random()*1e9);
    const mode=_getMpMode();  /* Phase 212: use UI-selected mode */
    mpSend("game_start",{seed,mode});
    mpCountdown(seed,mode);
  }'''
))

# ─────────────────────────────────────────────────────────────────────────────
# P9: mpCreate() ready handler — also use _getMpMode()
# ─────────────────────────────────────────────────────────────────────────────
patches.append((
    'P9_mpcreate_mode',
    '''      if(S.mp.myReady&&S.mp.oppReady){
        const seed=~~(Math.random()*1e9);
        const _rm=S.mode||"city";const mode=(MODES.find(m=>m.id===_rm)?.noMultiplayer)?"city":_rm;
        mpSend("game_start",{seed,mode});
        mpCountdown(seed,mode);
      }''',
    '''      if(S.mp.myReady&&S.mp.oppReady){
        const seed=~~(Math.random()*1e9);
        const mode=_getMpMode();  /* Phase 212: use UI-selected mode */
        mpSend("game_start",{seed,mode});
        mpCountdown(seed,mode);
      }'''
))

# ─────────────────────────────────────────────────────────────────────────────
# P10: renderMultiplayerLobby() initial screen — add mode selector block
# ─────────────────────────────────────────────────────────────────────────────
old_mp_initial = '''  if(\\!mp){
    const joinInput=S._mpJoinCode||"";
    return`<div class="scr">
      <div style="text-align:center;margin-bottom:1.4rem;padding-top:.5rem">
        <div class="mp-lobby-title">\\u2694\\ufe0f Live 1vs1 Duell</div>
        <div style="color:var(--text3);font-size:.8rem;margin-top:.25rem">Spiele live gegen einen Freund</div>
      </div>
      <div style="background:var(--bg2);border:1.5px solid var(--border);border-radius:16px;padding:1.4rem;margin-bottom:1rem;text-align:center">
        <div style="font-size:2.5rem;margin-bottom:.5rem">\\u{1F3E0}</div>
        <div style="font-weight:900;font-size:1rem;color:var(--text);margin-bottom:.35rem">Spiel erstellen</div>
        <div style="color:var(--text3);font-size:.78rem;margin-bottom:.9rem">Generiere einen Code und lade einen Freund ein</div>
        <button class="btn-p" style="width:100%" onclick="mpCreate()">\\u2795 Neues Spiel erstellen</button>
      </div>
      <div style="background:var(--bg2);border:1.5px solid var(--border);border-radius:16px;padding:1.4rem;text-align:center">
        <div style="font-size:2.5rem;margin-bottom:.5rem">\\u{1F517}</div>
        <div style="font-weight:900;font-size:1rem;color:var(--text);margin-bottom:.35rem">Mit Code beitreten</div>
        <div style="color:var(--text3);font-size:.78rem;margin-bottom:.9rem">Gib den 4-stelligen Code deines Freundes ein</div>
        <div style="display:flex;gap:8px">
          <input type="text" maxlength="4" placeholder="z.B. A7B2" value="${esc(joinInput)}"
            oninput="S._mpJoinCode=this.value.toUpperCase();this.value=this.value.toUpperCase()"
            style="flex:1;font-size:1.2rem;font-weight:900;text-align:center;letter-spacing:4px;text-transform:uppercase">
          <button class="btn-p" style="width:auto;padding:.6rem 1.2rem" onclick="mpJoin(S._mpJoinCode)">&rarr;</button>
        </div>
      </div>
      <button class="mp-back-btn" onclick="S.mpModal=false;render()">\\u2b05\\ufe0f Zur\\u00fcck zum Hauptmen\\u00fc</button>
    </div>`;
  }'''

new_mp_initial = '''  if(\\!mp){
    const joinInput=S._mpJoinCode||"";
    const mpST=S.mpSelType||"random",mpSC=S.mpSelCat||"",mpSM=S.mpSelMode||"";
    const _mBtnSty=(a)=>`background:${a?"#6366f1":"var(--bg3)"};color:${a?"#fff":"var(--text2)"};border:1.5px solid ${a?"#6366f1":"var(--border)"};border-radius:8px;padding:.32rem .65rem;font-size:.75rem;font-weight:700;cursor:pointer;transition:all .15s`;
    const mpCatSec=mpST==="cat"?`<div style="display:flex;flex-wrap:wrap;gap:5px;margin-top:.5rem">${Object.entries(MODE_CATS).map(([k,v])=>`<button onclick="S.mpSelCat=\'${k}\';render()" style="${_mBtnSty(mpSC===k)}">${v.icon} ${v.label}</button>`).join("")}</div>`:"";
    const mpGameSec=mpST==="specific"?`<div style="max-height:130px;overflow-y:auto;display:flex;flex-wrap:wrap;gap:4px;margin-top:.5rem;padding:2px">${MODES.filter(m=>GEN[m.id]&&!m.comingSoon&&!m.noMultiplayer).map(m=>`<button onclick="S.mpSelMode=\'${m.id}\';render()" style="${_mBtnSty(mpSM===m.id)}">${m.icon} ${(modeTitle(m)||m.id).slice(0,16)}</button>`).join("")}</div>`:"";
    const mpModeBlock=`<div style="background:var(--bg2);border:1.5px solid var(--border);border-radius:14px;padding:1rem;margin-bottom:.85rem">
      <div style="font-size:.65rem;font-weight:700;color:var(--text3);margin-bottom:.5rem">\\u{1F3AE} SPIELMODUS W\\u00c4HLEN</div>
      <div style="display:flex;gap:6px">
        <button onclick="S.mpSelType=\'random\';S.mpSelMode=\\'\\';S.mpSelCat=\\'\\';render()" style="${_mBtnSty(mpST===\\'random\\')}">\\u{1F3B2} Zufall</button>
        <button onclick="S.mpSelType=\'cat\';S.mpSelMode=\\'\\';render()" style="${_mBtnSty(mpST===\\'cat\\')}">\\u{1F4C2} Rubrik</button>
        <button onclick="S.mpSelType=\'specific\';S.mpSelCat=\\'\\';render()" style="${_mBtnSty(mpST===\\'specific\\')}">\\u{1F3AE} Spiel</button>
      </div>${mpCatSec}${mpGameSec}
    </div>`;
    return`<div class="scr">
      <div style="text-align:center;margin-bottom:1rem;padding-top:.5rem">
        <div class="mp-lobby-title">\\u2694\\ufe0f Live 1vs1 Duell</div>
        <div style="color:var(--text3);font-size:.8rem;margin-top:.25rem">Spiele live gegen einen Freund</div>
      </div>
      ${mpModeBlock}
      <div style="background:var(--bg2);border:1.5px solid var(--border);border-radius:16px;padding:1.2rem;margin-bottom:.85rem;text-align:center">
        <div style="font-size:2rem;margin-bottom:.35rem">\\u{1F3E0}</div>
        <div style="font-weight:900;font-size:.95rem;color:var(--text);margin-bottom:.3rem">Spiel erstellen</div>
        <div style="color:var(--text3);font-size:.76rem;margin-bottom:.75rem">Generiere einen Code und lade einen Freund ein</div>
        <button class="btn-p" style="width:100%" onclick="mpCreate()">\\u2795 Neues Spiel erstellen</button>
      </div>
      <div style="background:var(--bg2);border:1.5px solid var(--border);border-radius:16px;padding:1.2rem;text-align:center">
        <div style="font-size:2rem;margin-bottom:.35rem">\\u{1F517}</div>
        <div style="font-weight:900;font-size:.95rem;color:var(--text);margin-bottom:.3rem">Mit Code beitreten</div>
        <div style="color:var(--text3);font-size:.76rem;margin-bottom:.75rem">Gib den 4-stelligen Code deines Freundes ein</div>
        <div style="display:flex;gap:8px">
          <input type="text" maxlength="4" placeholder="z.B. A7B2" value="${esc(joinInput)}"
            oninput="S._mpJoinCode=this.value.toUpperCase();this.value=this.value.toUpperCase()"
            style="flex:1;font-size:1.2rem;font-weight:900;text-align:center;letter-spacing:4px;text-transform:uppercase">
          <button class="btn-p" style="width:auto;padding:.6rem 1.2rem" onclick="mpJoin(S._mpJoinCode)">&rarr;</button>
        </div>
      </div>
      <button class="mp-back-btn" onclick="S.mpModal=false;render()">\\u2b05\\ufe0f Zur\\u00fcck zum Hauptmen\\u00fc</button>
    </div>`;
  }'''

patches.append(('P10_mp_initial', old_mp_initial, new_mp_initial))

# ─────────────────────────────────────────────────────────────────────────────
# Apply all patches
# ─────────────────────────────────────────────────────────────────────────────
results = []
for name, old, new in patches:
    count = src.count(old)
    if count == 1:
        src = src.replace(old, new, 1)
        results.append(f"  {name}: ✓ OK")
    elif count == 0:
        results.append(f"  {name}: ✗ NOT FOUND")
    else:
        results.append(f"  {name}: ✗ AMBIGUOUS ({count})")

print(f"Phase 212 patch results ({original_len} → {len(src)} chars, +{len(src)-original_len}):")
for r in results:
    print(r)

with open(GEN, 'w', encoding='utf-8') as f:
    f.write(src)
print("Written OK")
