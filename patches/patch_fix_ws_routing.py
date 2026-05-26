"""
patch_fix_ws_routing.py
========================
Bug 1: render() only checks `mode==="wort_schmiede"` for the Wort-Schmiede
       render path. All ws_tiere_* and ws_pferde_* modes have different mode
       IDs and miss this check → fall through → render old S.q from previous
       game → user sees wrong game (e.g. Archäologie match instead of WS).

Fix 1: Change the render check to `S.wsData && S.ph==="playing"` — if wsData
       is set (regardless of mode ID), use the WS renderer.

Bug 2: startGame() Object.assign never resets S.q = null. Stale question
       from previous game leaks through if the new mode reaches render()
       before a fresh question is generated (e.g. ws_tiere_* modes).

Fix 2: Add q:null to startGame's Object.assign reset.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GEN  = os.path.join(ROOT, 'gen.py')

with open(GEN, 'r', encoding='utf-8') as fh:
    c = fh.read()

# ── Fix 1: render() — extend WS check to cover all ws_tiere_/ws_pferde_ ──
OLD_WS_RENDER = (
    '    if(mode==="wort_schmiede"&&S.ph==="playing"){\n'
    '    app.innerHTML=renderWortSchmiede(sc);\n'
    '    requestAnimationFrame(()=>{document.getElementById("ws-input")?.focus();});\n'
    '    return;\n'
    '  }'
)
NEW_WS_RENDER = (
    '    if((mode==="wort_schmiede"||S.wsData)&&S.ph==="playing"){\n'
    '    app.innerHTML=renderWortSchmiede(sc);\n'
    '    requestAnimationFrame(()=>{document.getElementById("ws-input")?.focus();});\n'
    '    return;\n'
    '  }'
)
assert c.count(OLD_WS_RENDER) == 1, f"Anchor not unique: WS render check (found {c.count(OLD_WS_RENDER)})"
c = c.replace(OLD_WS_RENDER, NEW_WS_RENDER)
print("  [OK] Fix 1: render() WS check now uses S.wsData (covers ws_tiere_* + ws_pferde_*)")

# ── Fix 2: startGame() — reset S.q = null to prevent stale question leak ──
OLD_RESET = 'slfData:null,wsData:null,lhData:null,airportPinDist:0,airportPinPts:0,'
NEW_RESET = 'q:null,sel:null,ok:null,slfData:null,wsData:null,lhData:null,airportPinDist:0,airportPinPts:0,'

assert c.count(OLD_RESET) == 1, f"Anchor not unique: startGame Object.assign (found {c.count(OLD_RESET)})"
c = c.replace(OLD_RESET, NEW_RESET)
print("  [OK] Fix 2: startGame() now resets q:null and sel:null — no stale question leak")

with open(GEN, 'w', encoding='utf-8') as fh:
    fh.write(c)
print("  [OK] gen.py updated")
