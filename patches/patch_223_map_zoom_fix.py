#!/usr/bin/env python3
import sys

path = "/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

errors = []

# ─── FIX 1: genStadionHoeheQ — encode pair in lid so askedLids dedup works ───
OLD1 = 'return{type:"beta_hl",prompt:"Welches Stadion liegt höher über dem Meeresspiegel?",subj:"",opts:[a.name,b.name],ans:higher.name,meta:meta,lid:"stadion_hoehe",cc:higher.cc||"de"};'
NEW1 = 'var _pLid="sh_"+Math.min(ai,sorted.indexOf(b))+"_"+Math.max(ai,sorted.indexOf(b));return{type:"beta_hl",prompt:"Welches Stadion liegt höher über dem Meeresspiegel?",subj:"",opts:[a.name,b.name],ans:higher.name,meta:meta,lid:_pLid,cc:higher.cc||"de"};'

if OLD1 not in content:
    errors.append("FIX1: stadion_hoehe lid pattern not found!")
else:
    content = content.replace(OLD1, NEW1, 1)
    print("OK FIX1: genStadionHoeheQ — pair-encoded lid for askedLids dedup")

# ─── FIX 2: _mapZoom — bind to question lid to prevent wrong-region restore ──
OLD2 = '  const zoom=d3.zoom().scaleExtent([1,10]).translateExtent([[-W,-H],[2*W,2*H]]).on("zoom",ev=>{g.attr("transform",ev.transform);window._mapZoom=ev.transform;});'
NEW2 = '  let _pinMapDragged=false;\n  const zoom=d3.zoom().scaleExtent([1,10]).translateExtent([[-W,-H],[2*W,2*H]]).on("zoom",ev=>{g.attr("transform",ev.transform);window._mapZoom={t:ev.transform,lid:S.q?S.q.lid:null};if(ev.sourceEvent)_pinMapDragged=true;});'

if OLD2 not in content:
    errors.append("FIX2: zoom handler pattern not found!")
else:
    content = content.replace(OLD2, NEW2, 1)
    print("OK FIX2: zoom handler — _mapZoom lid-bound + _pinMapDragged flag")

# ─── FIX 3: _mapZoom restore — check lid matches current question ─────────────
OLD3 = '  if(window._mapZoom&&window._mapZoom.k>1){\n    svg.call(zoom.transform,window._mapZoom);\n  } else if(!readOnly&&S.q&&S.q.targetLat!=null&&S.q.type==="uk_pin"){'
NEW3 = '  const _savedZ=window._mapZoom;\n  if(_savedZ&&_savedZ.t&&_savedZ.t.k>1&&_savedZ.lid===(S.q?S.q.lid:null)){\n    svg.call(zoom.transform,_savedZ.t);\n  } else if(!readOnly&&S.q&&S.q.targetLat!=null&&S.q.type==="uk_pin"){'

if OLD3 not in content:
    errors.append("FIX3: _mapZoom restore pattern not found!")
else:
    content = content.replace(OLD3, NEW3, 1)
    print("OK FIX3: _mapZoom restore gated by question lid match")

# ─── FIX 4: _mapZoom save on auto-zoom — include lid ─────────────────────────
OLD4 = '    window._mapZoom=_tr;\n  }'
NEW4 = '    window._mapZoom={t:_tr,lid:S.q?S.q.lid:null};\n  }'

if OLD4 not in content:
    errors.append("FIX4: auto-zoom _mapZoom save pattern not found!")
else:
    content = content.replace(OLD4, NEW4, 1)
    print("OK FIX4: auto-zoom saves _mapZoom with lid")

# ─── FIX 5: click handler — use svg.node() for consistent coords + drag guard ─
OLD5 = '''    svg.on("click",function(ev){
      if(S.sel!==null)return;
      const [sx,sy]=d3.pointer(ev,g.node());
      /* invert zoom transform */
      const tr=window._mapZoom||d3.zoomIdentity;
      const [mx,my]=[(sx-tr.x)/tr.k,(sy-tr.y)/tr.k];'''
NEW5 = '''    svg.on("pointerdown.pintrack",function(){_pinMapDragged=false;});
    svg.on("click",function(ev){
      if(S.sel!==null)return;
      if(_pinMapDragged){_pinMapDragged=false;return;} /* was a pan, not a tap */
      const [sx,sy]=d3.pointer(ev,svg.node()); /* SVG-space coords — consistent on all mobile browsers */
      const _savedZT=window._mapZoom;const tr=(_savedZT&&_savedZT.t)||d3.zoomIdentity;
      const [mx,my]=[(sx-tr.x)/tr.k,(sy-tr.y)/tr.k];'''

if OLD5 not in content:
    errors.append("FIX5: click handler pointer pattern not found!")
else:
    content = content.replace(OLD5, NEW5, 1)
    print("OK FIX5: click handler — svg.node() coords + drag guard")

if errors:
    print("\nERRORS:")
    for e in errors:
        print(" ", e)
    sys.exit(1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("\nAll 5 fixes applied successfully.")
