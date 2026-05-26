#!/usr/bin/env python3
import sys
path = "/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
errors = []

# ─── FIX 1: lq() — reset _mapZoom at the start of every new question ─────────
# This is the primary fix: ensures both drawWorldMap AND drawAirportPinMap
# start clean on every new question regardless of what happened before.
OLD1 = "function lq(){\n  clearInterval(tIv);"
NEW1 = "function lq(){\n  clearInterval(tIv);\n  window._mapZoom=null; /* Phase 226: reset map zoom on every new question */"
if OLD1 not in content:
    errors.append("FIX1: lq() start pattern not found")
else:
    content = content.replace(OLD1, NEW1, 1)
    print("OK FIX1: lq() resets _mapZoom at start of each question")

# ─── FIX 2: drawWorldMap zoom handler — only write _mapZoom during interactive ─
# The zoom-to-country animation during feedback was OVERWRITING _mapZoom=null
# by firing a zoom event. Guard: only persist zoom if sel===null (pre-answer).
OLD2 = "    .on('zoom',ev=>{\n      g.attr('transform',ev.transform); /* zoom always enabled */\n      window._mapZoom=ev.transform; /* persist for redraw restore */\n    });"
NEW2 = "    .on('zoom',ev=>{\n      g.attr('transform',ev.transform);\n      if(sel===null)window._mapZoom=ev.transform; /* Phase 226: only store zoom in interactive phase, not during feedback animation */\n    });"
if OLD2 not in content:
    errors.append("FIX2: drawWorldMap zoom handler not found")
else:
    content = content.replace(OLD2, NEW2, 1)
    print("OK FIX2: drawWorldMap zoom handler guarded by sel===null")

# ─── FIX 3: drawWorldMap restore — also accept raw ZoomTransform (not just {t,lid}) ─
# drawAirportPinMap now stores {t, lid} but drawWorldMap stores raw ZoomTransform.
# Make the restore check robust to both formats.
OLD3 = "  /* Restore zoom on timer-triggered redraws (sel===null = pre-answer) */\n  if(sel===null&&window._mapZoom&&window._mapZoom.k>1){\n    svg.call(zoom.transform,window._mapZoom);\n  } else if(sel!==null){\n    window._mapZoom=null; /* clear after answer so zoom-to-country starts clean */\n  }"
NEW3 = "  /* Phase 226: Restore zoom only for same question, only in interactive phase */\n  if(sel===null&&window._mapZoom&&window._mapZoom.k>1){\n    svg.call(zoom.transform,window._mapZoom);\n  }"
if OLD3 not in content:
    errors.append("FIX3: drawWorldMap restore block not found")
else:
    content = content.replace(OLD3, NEW3, 1)
    print("OK FIX3: drawWorldMap restore simplified (lq() handles reset)")

if errors:
    for e in errors: print("ERROR:", e)
    sys.exit(1)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("\nAll 3 map zoom fixes applied.")
