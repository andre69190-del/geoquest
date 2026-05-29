"""
Phase: 286
Date:  2026-05-29
Author: Claude / Andre
Scope: 1v1-Online: Auswahl des Gegners sichtbar machen

Description:
  BUG (gemeldet): Im 1v1 sieht man nicht, was der Gegner angetippt/markiert
  hat. Bisher wurde per score_update nur {score,rd,correct} gebroadcastet -
  die konkrete Antwortauswahl wurde nie uebertragen oder angezeigt.

  FIX:
    1. answer(): score_update-Payload um {sel,selOk,lid} erweitert.
    2. score_update-Empfaenger: speichert S.mpOppSel/S.mpOppSelOk/S.mpOppLid.
    3. Resets in mpCountdown + startGame ergaenzt.
    4. Render:
       a) Universelle Zeile unter der Duell-Leiste (alle Modi) - nur bei
          lid-Match (S.mpOppLid===q.lid).
       b) Marker auf dem vom Gegner gewaehlten Options-Button (z.B. BIP).

  HINWEIS: gen.py speichert Symbole als literale \\u-Sequenzen
  (\\u2713 \\u2717 \\u2694). Anker + neue Strings nutzen raw-Strings,
  damit Backslash-u 1:1 zur Datei passt.

Dependencies: patch_285_mp_sync.py
Zero-Bug Policy: jeder patch() prueft Anker-Eindeutigkeit (count==1).
"""

import os
GEN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'gen.py')

with open(GEN, encoding='utf-8') as f:
    content = f.read()

def patch(old, new, label):
    global content
    cnt = content.count(old)
    if cnt == 0:
        print(f'[SKIP] {label}: anchor not found')
        return
    if cnt > 1:
        print(f'[WARN] {label}: anchor {cnt}x - using replace(1)')
    content = content.replace(old, new, 1)
    print(f'[OK]   {label}')


# FIX 1: answer() - Auswahl mitsenden
patch(
    """    window.mpGameCh.send({type:"broadcast",event:"score_update",
      payload:{score:S.sc,rd:S.rd,correct:S.correct}}).then(()=>{},()=>{});""",
    """    window.mpGameCh.send({type:"broadcast",event:"score_update",
      payload:{score:S.sc,rd:S.rd,correct:S.correct,sel:(typeof a==="undefined"?null:a),selOk:ok,lid:(S.q&&S.q.lid)}}).then(()=>{},()=>{});""",
    'answer(): sel/selOk/lid in score_update-Payload'
)

# FIX 2: score_update-Empfaenger - Auswahl speichern
patch(
    'S.mpOppScore=payload.score||0;S.mpOppRd=payload.rd||0;render();',
    'S.mpOppScore=payload.score||0;S.mpOppRd=payload.rd||0;'
    'if("lid" in payload){S.mpOppLid=payload.lid;S.mpOppSel=payload.sel;S.mpOppSelOk=!!payload.selOk;}render();',
    'score_update-Empfaenger: Gegner-Auswahl speichern'
)

# FIX 3: Resets (mpCountdown + startGame)
patch(
    'S.mpOppScore=0;S.mpOppRd=0;S.mpOppFinal=null;',
    'S.mpOppScore=0;S.mpOppRd=0;S.mpOppFinal=null;S.mpOppSel=null;S.mpOppLid=null;S.mpOppSelOk=null;',
    'mpCountdown: Gegner-Auswahl-Reset'
)
patch(
    'mpOpponent:null,mpOppScore:0,mpOppFinal:null,mpOppRd:0});',
    'mpOpponent:null,mpOppScore:0,mpOppFinal:null,mpOppRd:0,mpOppSel:null,mpOppLid:null,mpOppSelOk:null});',
    'startGame: Gegner-Auswahl-Reset'
)

# FIX 4a: Marker auf dem vom Gegner gewaehlten Button
patch(
    r"""const mk=sel?(o===q.ans?`<span>\u2713</span>`:o===sel?`<span>\u2717</span>`:""):"";return`<button class="${cls}""",
    r"""const mk=sel?(o===q.ans?`<span>\u2713</span>`:o===sel?`<span>\u2717</span>`:""):"";const _omk=(S.mpOpponent&&S.mpOppLid===q.lid&&S.mpOppSel!=null&&o===S.mpOppSel)?`<span class="opp-pick" title="Wahl des Gegners" style="margin-left:5px;font-size:.62rem;font-weight:800;color:${S.mpOppSelOk?"#10b981":"#ef4444"}">\u2694</span>`:"";return`<button class="${cls}""",
    'Options-Buttons: Gegner-Marker (Deklaration)'
)
patch(
    r""":displayCountry(o))}${mk}</button>""",
    r""":displayCountry(o))}${mk}${_omk}</button>""",
    'Options-Buttons: Gegner-Marker (Interpolation)'
)

# FIX 4b: Universelle Gegner-Auswahl-Zeile unter der Duell-Leiste
patch(
    r"""    ${st>=3?`<div style="text-align:center;font-size:.76rem;font-weight:700;color:#fb923c;margin-bottom:6px">${_tr.l}</div>`:""}""",
    r"""    ${(S.mpOpponent&&S.mpOppLid===q.lid&&typeof S.mpOppSel!=="undefined")?`<div style="text-align:center;font-size:.72rem;font-weight:800;margin:1px 0 5px;color:${S.mpOppSelOk?"#10b981":"#ef4444"}">\u2694 ${esc(S.mpOpponent.slice(0,10))} ${S.mpOppSel===null?"verpasste die Zeit":"wählte: "+esc(displayCountry(S.mpOppSel)||S.mpOppSel)} ${S.mpOppSelOk?"\u2713":"\u2717"}</div>`:""}
    ${st>=3?`<div style="text-align:center;font-size:.76rem;font-weight:700;color:#fb923c;margin-bottom:6px">${_tr.l}</div>`:""}""",
    'Universelle Gegner-Auswahl-Zeile unter Duell-Leiste'
)


# -- atomic write ------------------------------------------------------
_tmp = GEN + '.tmp'
with open(_tmp, 'w', encoding='utf-8') as f:
    f.write(content)
os.replace(_tmp, GEN)
print('\nPatch complete.')
