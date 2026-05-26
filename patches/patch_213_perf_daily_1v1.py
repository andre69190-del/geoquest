"""
Phase 213: Performance Polish, Daily Archive, 1vs1 Selector UI Hardening
Patches applied to gen.py in order: Prio3 → Prio2 → Prio1
"""
import subprocess, sys

src = open('/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py','r',encoding='utf-8').read()
orig_len = len(src)
patches_ok = []

def patch(label, old, new):
    global src
    count = src.count(old)
    if count == 0:
        print(f"MISS  [{label}] — string not found")
        return False
    if count > 1:
        print(f"WARN  [{label}] — {count} occurrences, replacing first only")
    src = src.replace(old, new, 1)
    patches_ok.append(label)
    print(f"OK    [{label}]")
    return True

# ─── PRIO 3: Performance / Map zoom reset ─────────────────────────────────────

patch(
    "P1: mapZoom reset in startGame",
    'function startGame(m){\n  rngSeed=null;  /* Phase 212: prevent seed leak from daily/mp into solo games */',
    'function startGame(m){\n  rngSeed=null;  /* Phase 212: prevent seed leak from daily/mp into solo games */\n  window._mapZoom=null; /* Phase 213: reset D3 map zoom on each new game */'
)

# ─── PRIO 2: Daily history archive display ────────────────────────────────────

patch(
    "P2a: getDailyHistory() helper",
    'function getDailySeed(){',
    (
        'function getDailyHistory(){\n'
        '  const hist=[];\n'
        '  for(let i=0;i<7;i++){\n'
        '    const d=new Date();d.setDate(d.getDate()-i);\n'
        '    const key="gq_daily_"+d.toISOString().slice(0,10);\n'
        '    const raw=localStorage.getItem(key);\n'
        '    if(raw){try{const o=JSON.parse(raw);hist.push({date:d.toISOString().slice(0,10),score:o.score||0});}catch(_){}}\n'
        '  }\n'
        '  return hist;\n'
        '}\n'
        'function getDailySeed(){'
    )
)

# Inject history HTML into the done-branch of renderDailyHero
patch(
    "P2b: history display in renderDailyHero done-branch",
    (
        'if(done){\n'
        '    return`<div class="daily-hero done">\n'
        '      <div style="display:flex;align-items:center;gap:12px">\n'
        '        <div style="font-size:2rem">\\u{1F3C6}</div>\n'
        '        <div>\n'
        '          <div class="dh-title">Daily Challenge erledigt\\!</div>\n'
        '          <div class="dh-sub" style="color:var(--text2)">Score: <b>${stored?.score?.toLocaleString()||"?"}</b> \\u00b7 Neue Challenge in <span style="font-family:monospace;color:#f59e0b">${cd}</span></div>\n'
        '        </div>\n'
        '      </div>\n'
        '    </div>`;\n'
        '  }'
    ),
    (
        'if(done){\n'
        '    const _hist=getDailyHistory();\n'
        '    const _today=new Date().toISOString().slice(0,10);\n'
        '    const _histHtml=_hist.length>1?`<div style="margin-top:.75rem;border-top:1px solid var(--border);padding-top:.6rem">'
        '<div style="font-size:.68rem;font-weight:700;color:var(--text3);letter-spacing:.05em;margin-bottom:.35rem">\\u{1F4CA} LETZTE 7 TAGE</div>'
        '${_hist.map(_h=>`<div style="display:flex;justify-content:space-between;font-size:.78rem;padding:.12rem 0">'
        '<span style="color:var(--text2)">${_h.date.slice(5).replace(\'-\',\'.\')}</span>'
        '<span style="font-weight:700;color:${_h.date===_today?\'#6366f1\':\'var(--text)\'}">${_h.score.toLocaleString()}</span>'
        '</div>`).join("")}'
        '</div>`:"";'
        '\n'
        '    return`<div class="daily-hero done">\n'
        '      <div style="display:flex;align-items:center;gap:12px">\n'
        '        <div style="font-size:2rem">\\u{1F3C6}</div>\n'
        '        <div>\n'
        '          <div class="dh-title">Daily Challenge erledigt\\!</div>\n'
        '          <div class="dh-sub" style="color:var(--text2)">Score: <b>${stored?.score?.toLocaleString()||"?"}</b> \\u00b7 Neue Challenge in <span style="font-family:monospace;color:#f59e0b">${cd}</span></div>\n'
        '        </div>\n'
        '      </div>\n'
        '      ${_histHtml}\n'
        '    </div>`;\n'
        '  }'
    )
)

# ─── PRIO 1: 1vs1 Selector UI hardening ───────────────────────────────────────

# _mBtnSty in renderMultiplayerLobby: bigger tap targets
patch(
    "P3a: _mBtnSty min-height tap target",
    'const _mBtnSty=(a)=>`background:${a?"#6366f1":"var(--bg3)"};color:${a?"#fff":"var(--text2)"};border:1.5px solid ${a?"#6366f1":"var(--border)"};border-radius:8px;padding:.3rem .6rem;font-size:.73rem;font-weight:700;cursor:pointer`;',
    'const _mBtnSty=(a)=>`background:${a?"#6366f1":"var(--bg3)"};color:${a?"#fff":"var(--text2)"};border:1.5px solid ${a?"#6366f1":"var(--border)"};border-radius:8px;padding:.35rem .7rem;font-size:.73rem;font-weight:700;cursor:pointer;min-height:36px;display:inline-flex;align-items:center`;'
)

# mpGameSec: increase max-height + touch scroll
patch(
    "P3b: mpGameSec max-height 120→180px + webkit scroll",
    'style="max-height:120px;overflow-y:auto;display:flex;flex-wrap:wrap;gap:4px;margin-top:.5rem;padding:2px"',
    'style="max-height:180px;overflow-y:auto;-webkit-overflow-scrolling:touch;display:flex;flex-wrap:wrap;gap:4px;margin-top:.5rem;padding:2px"'
)

# LV gameSection: add webkit touch scroll (already has max-height:200px)
patch(
    "P3c: LV gameSection webkit touch scroll",
    'style="max-height:200px;overflow-y:auto;display:flex;flex-wrap:wrap;gap:5px;padding:2px"',
    'style="max-height:200px;overflow-y:auto;-webkit-overflow-scrolling:touch;display:flex;flex-wrap:wrap;gap:5px;padding:2px"'
)

# LV catSection buttons: add min-height tap target
patch(
    "P3d: LV catSection button min-height",
    'padding:.3rem .6rem;font-size:.72rem;font-weight:600;cursor:pointer">${v.icon} ${v.label}</button>`;',
    'padding:.35rem .7rem;font-size:.72rem;font-weight:600;cursor:pointer;min-height:36px;display:inline-flex;align-items:center">${v.icon} ${v.label}</button>`;'
)

# ─── Write result ──────────────────────────────────────────────────────────────
print(f"\nPatches applied: {len(patches_ok)}/6")
print(f"Size delta: {len(src)-orig_len:+d} chars")
with open('/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py','w',encoding='utf-8') as f:
    f.write(src)
print("Written OK")
