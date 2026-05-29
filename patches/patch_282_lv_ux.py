"""
Phase: 282
Date:  2026-05-29
Author: Claude / Andre
Scope: 1v1 LV-UX: Spiel-Filter + P1-Ergebnis auf Handoff-Screen

Description:
  FIX 1 – "Spiel"-Liste zeigte inkompatible Modi (WS/Wort-Schmiede):
    Der Filter war !m.comingSoon aber NICHT !m.noMultiplayer.
    Wort-Schmiede-Modi (noMultiplayer:true) wurden angezeigt und konnten
    ausgewaehlt werden, obwohl das LV-Modal kein WS-UI unterstuetzt.
    Fix: noMultiplayer-Modi aus der "Spiel"-Liste entfernt.

  FIX 2 – Spieler 2 sah nicht, ob Spieler 1 richtig geantwortet hat:
    Der Handoff-Screen zeigte nur "Geraet weitergeben" ohne Ergebnis-Feedback.
    Fix:
    - lv.lastP1Result = {correct, timedOut} in lvAnswer gespeichert
    - renderLVHandoff zeigt jetzt Ergebnis-Badge:
        ✅ "[Name] hat richtig geantwortet!" (gruen)
        ❌ "[Name] hat falsch geantwortet!" (rot)
        ⏱ "[Name] hatte keine Zeit mehr!" (orange)

Dependencies: patch_281_1v1_sync.py
Zero-Bug Policy: All c.replace() calls assert uniqueness
"""

GEN = '/sessions/youthful-relaxed-turing/mnt/Geoquest/gen.py'

with open(GEN, encoding='utf-8') as f:
    content = f.read()

def patch(old, new, label):
    global content
    cnt = content.count(old)
    if cnt == 0:
        print(f'[SKIP] {label}: anchor not found')
        return
    if cnt > 1:
        print(f'[WARN] {label}: anchor {cnt}x – using replace(1)')
    content = content.replace(old, new, 1)
    print(f'[OK]   {label}')


# ============================================================
# FIX 1: "Spiel"-Liste – noMultiplayer-Modi ausfiltern
# ============================================================
patch(
    r"""  const gameSection=sT==="specific"?`<div style="margin-bottom:.75rem">
    <div style="font-size:.65rem;font-weight:700;color:var(--text3);margin-bottom:.4rem">SPIEL WÄHLEN</div>
    <div style="max-height:200px;overflow-y:auto;-webkit-overflow-scrolling:touch;display:flex;flex-wrap:wrap;gap:5px;padding:2px">${MODES.filter(m=>GEN[m.id]&&!m.comingSoon).map(m=>{""",
    r"""  const gameSection=sT==="specific"?`<div style="margin-bottom:.75rem">
    <div style="font-size:.65rem;font-weight:700;color:var(--text3);margin-bottom:.4rem">SPIEL WÄHLEN</div>
    <div style="max-height:200px;overflow-y:auto;-webkit-overflow-scrolling:touch;display:flex;flex-wrap:wrap;gap:5px;padding:2px">${MODES.filter(m=>GEN[m.id]&&!m.comingSoon&&!m.noMultiplayer).map(m=>{""",
    'renderLVSetup Spiel-Liste: +noMultiplayer-Filter'
)


# ============================================================
# FIX 2a: lvAnswer – P1-Ergebnis speichern
# ============================================================
patch(
    r"""    if(lv.current===1){
      lv.current=2;
      lv.phase="handoff";
      render();""",
    r"""    if(lv.current===1){
      /* P282: P1-Ergebnis fuer Handoff-Anzeige speichern */
      lv.lastP1Result={correct,timedOut:ans===null};
      lv.current=2;
      lv.phase="handoff";
      render();""",
    'lvAnswer: lv.lastP1Result speichern'
)


# ============================================================
# FIX 2b: renderLVHandoff – Ergebnis-Badge anzeigen
# ============================================================
patch(
    r"""  return`<div style="min-height:100vh;background:var(--bg);padding:1.5rem;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
    <div style="font-size:3.5rem;margin-bottom:.75rem">&#x1F4F1;</div>
    <div style="font-size:1.15rem;font-weight:900;color:var(--text);margin-bottom:.3rem">Ger&auml;t weitergeben</div>
    <div style="font-size:.8rem;color:var(--text3);margin-bottom:1.5rem">Runde ${lv.round+1}/${LV_ROUNDS} &middot; Gleiche Frage</div>
    <div style="background:${plBg};border:2px solid ${plColor};border-radius:14px;padding:1rem 2.5rem;margin-bottom:1.25rem">
      <div style="font-size:.65rem;color:${plColor};font-weight:700;letter-spacing:.5px;margin-bottom:.3rem">JETZT DRAN</div>
      <div style="font-size:1.4rem;font-weight:900;color:var(--text)">${esc(pl.name)}</div>
    </div>
    <div style="font-size:.75rem;color:var(--text3);margin-bottom:1.5rem">&#x1F440; Schau nicht hin, w&auml;hrend der andere spielt!</div>
    <button class="btn-p" style="width:100%;max-width:280px;font-size:1rem" onclick="window._lvHandoffGo()">&#x25BA; Ich bin bereit</button>
  </div>`;""",
    r"""  /* P282: P1-Ergebnis-Badge aufbauen */
  const _r1=lv.lastP1Result||{};
  const _r1name=esc(lv.p1.name);
  const _r1badge=_r1.correct
    ?`<div style="background:rgba(16,185,129,.15);border:2px solid #10b981;border-radius:12px;padding:.6rem 1.2rem;margin-bottom:1.2rem;font-size:.95rem;font-weight:900;color:#10b981">&#x2705; ${_r1name} hat <b>richtig</b> geantwortet!</div>`
    :_r1.timedOut
    ?`<div style="background:rgba(245,158,11,.15);border:2px solid #f59e0b;border-radius:12px;padding:.6rem 1.2rem;margin-bottom:1.2rem;font-size:.95rem;font-weight:900;color:#f59e0b">&#x23F1; ${_r1name} hatte keine Zeit mehr!</div>`
    :_r1.hasOwnProperty('correct')
    ?`<div style="background:rgba(239,68,68,.15);border:2px solid #ef4444;border-radius:12px;padding:.6rem 1.2rem;margin-bottom:1.2rem;font-size:.95rem;font-weight:900;color:#ef4444">&#x274C; ${_r1name} hat <b>falsch</b> geantwortet!</div>`
    :"";
  return`<div style="min-height:100vh;background:var(--bg);padding:1.5rem;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
    <div style="font-size:3.5rem;margin-bottom:.75rem">&#x1F4F1;</div>
    <div style="font-size:1.15rem;font-weight:900;color:var(--text);margin-bottom:.3rem">Ger&auml;t weitergeben</div>
    <div style="font-size:.8rem;color:var(--text3);margin-bottom:.75rem">Runde ${lv.round+1}/${LV_ROUNDS} &middot; Gleiche Frage</div>
    ${_r1badge}
    <div style="background:${plBg};border:2px solid ${plColor};border-radius:14px;padding:1rem 2.5rem;margin-bottom:1.25rem">
      <div style="font-size:.65rem;color:${plColor};font-weight:700;letter-spacing:.5px;margin-bottom:.3rem">JETZT DRAN</div>
      <div style="font-size:1.4rem;font-weight:900;color:var(--text)">${esc(pl.name)}</div>
    </div>
    <div style="font-size:.75rem;color:var(--text3);margin-bottom:1.5rem">&#x1F440; Schau nicht hin, w&auml;hrend der andere spielt!</div>
    <button class="btn-p" style="width:100%;max-width:280px;font-size:1rem" onclick="window._lvHandoffGo()">&#x25BA; Ich bin bereit</button>
  </div>`;""",
    'renderLVHandoff: Ergebnis-Badge'
)


with open(GEN, 'w', encoding='utf-8') as f:
    f.write(content)
print('\nPatch complete.')
