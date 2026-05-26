"""
Phase 214: Silent-Fail Bugfix
- P1: Fix distractors() null excludeFn crash (breaks alpha_sprint)
- P2: Fix genAlphaSprintQ: pass x=>false instead of null
- P3: lq() null path: show toast instead of silent redirect
- P4: logic_grid/travel_route/slf → comingSoon:true (show badge + toast, not null redirect)
- P5: Info button tap target: 22px → 32px for Android
"""

src = open('/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py','r',encoding='utf-8').read()
orig_len = len(src)
patches_ok = []

def patch(label, old, new):
    global src
    count = src.count(old)
    if count == 0:
        print(f"MISS  [{label}] — not found")
        return False
    if count > 1:
        print(f"WARN  [{label}] — {count} occurrences, replacing first")
    src = src.replace(old, new, 1)
    patches_ok.append(label)
    print(f"OK    [{label}]")
    return True

# ── P1: distractors null-safety ───────────────────────────────────────────────
patch(
    "P1: distractors null excludeFn guard",
    'function distractors(pool,matchFn,excludeFn,keyFn,n=2){\n  const pref=pool.filter(x=>matchFn(x)&&\\!excludeFn(x));\n  const dp=pref.length>=n?pref:pool.filter(x=>\\!excludeFn(x));',
    'function distractors(pool,matchFn,excludeFn,keyFn,n=2){\n  const _excl=excludeFn||function(){return false;};\n  const pref=pool.filter(x=>matchFn(x)&&\\!_excl(x));\n  const dp=pref.length>=n?pref:pool.filter(x=>\\!_excl(x));'
)

# ── P2: Fix alpha_sprint distractors call ─────────────────────────────────────
patch(
    "P2: alpha_sprint distractors null→x=>false",
    'const dis=distractors(others,x=>x.ct===cor.ct,null,x=>displayCountry(x.cc)||x.c);',
    'const dis=distractors(others,x=>x.ct===cor.ct,x=>false,x=>displayCountry(x.cc)||x.c);'
)

# ── P3: lq() null path — show toast ──────────────────────────────────────────
patch(
    "P3: lq null-path toast",
    'if(!q){S.ph="menu";S.q=null;render();return;}',
    'if(!q){showToast("\\u26A0\\uFE0F Dieser Modus ist gerade nicht verf\\u00FCgbar.");S.ph="menu";S.q=null;render();return;}'
)

# ── P4a: logic_grid → comingSoon:true ────────────────────────────────────────
patch(
    "P4a: logic_grid comingSoon",
    '{id:"logic_grid",    icon:"\\u{1F9E9}",title:"Logik-Gitter",          group:"new_modes",prompt:"L\\u00f6se das R\\u00e4tsel",                desc:"L\\u00f6se geografische Logik-R\\u00e4tsel"}',
    '{id:"logic_grid",    icon:"\\u{1F9E9}",title:"Logik-Gitter",          group:"new_modes",comingSoon:true,prompt:"L\\u00f6se das R\\u00e4tsel",                desc:"L\\u00f6se geografische Logik-R\\u00e4tsel"}'
)

# ── P4b: travel_route → comingSoon:true ──────────────────────────────────────
patch(
    "P4b: travel_route comingSoon",
    '{id:"travel_route",  icon:"\\u{1F5FA}",title:"Reiseroute",            group:"new_modes",prompt:"K\\u00fcrzeste Route?",                      desc:"Plane die k\\u00fcrzeste Route zwischen St\\u00e4dten"}',
    '{id:"travel_route",  icon:"\\u{1F5FA}",title:"Reiseroute",            group:"new_modes",comingSoon:true,prompt:"K\\u00fcrzeste Route?",                      desc:"Plane die k\\u00fcrzeste Route zwischen St\\u00e4dten"}'
)

# ── P4c: slf → comingSoon:true ────────────────────────────────────────────────
patch(
    "P4c: slf comingSoon",
    '{id:"slf",           icon:"\U0001F4DD",title:"Stadt, Land, Fluss",t_key:"mode_slf",noMultiplayer:true,  group:"pure_geo",prompt:"Nenne Land und Hauptstadt\\u2026",    desc:"Der absolute Spiele-Klassiker"}',
    '{id:"slf",           icon:"\U0001F4DD",title:"Stadt, Land, Fluss",t_key:"mode_slf",noMultiplayer:true,  group:"pure_geo",comingSoon:true,prompt:"Nenne Land und Hauptstadt\\u2026",    desc:"Der absolute Spiele-Klassiker"}'
)

# ── P5: info-btn tap target 22px → 32px ──────────────────────────────────────
patch(
    "P5: info-btn tap target 22→32px",
    'style="position:absolute;bottom:6px;right:6px;z-index:99999;width:22px;height:22px;background:#3b82f6;color:#fff;border:none;border-radius:6px;font-size:.72rem;font-weight:900;cursor:pointer;line-height:1;padding:0"',
    'style="position:absolute;bottom:4px;right:4px;z-index:99999;width:32px;height:32px;background:#3b82f6;color:#fff;border:none;border-radius:8px;font-size:.75rem;font-weight:900;cursor:pointer;line-height:1;padding:0;touch-action:manipulation"'
)

# ── P6: fav-btn tap target 22px → 28px ───────────────────────────────────────
patch(
    "P6: fav-btn tap target 22→28px",
    'style="position:absolute;bottom:6px;left:6px;z-index:99999;width:22px;height:22px;background:transparent;border:none;font-size:.7rem;cursor:pointer;line-height:1;padding:0;',
    'style="position:absolute;bottom:4px;left:4px;z-index:99999;width:28px;height:28px;background:transparent;border:none;font-size:.75rem;cursor:pointer;line-height:1;padding:0;touch-action:manipulation;'
)

# ── Result ────────────────────────────────────────────────────────────────────
print(f"\nPatches applied: {len(patches_ok)}/6")
print(f"Size delta: {len(src)-orig_len:+d} chars")
with open('/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py','w',encoding='utf-8') as f:
    f.write(src)
print("Written OK")
