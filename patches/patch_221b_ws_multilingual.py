#!/usr/bin/env python3
import sys
path = "/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

OLD = (
  "  S.wsData.foundWords.push(inp);\n"
  "  const pts=inp.length>=6?60:inp.length>=5?40:inp.length>=4?20:10;\n"
  "  S.sc+=pts;S.correct+=1;\n"
  "  if(window.mpGameCh)mpSend(\"score_update\",{score:S.sc,rd:S.rd||0,correct:S.correct||0});"
)

NEW = (
  "  S.wsData.foundWords.push(inp);\n"
  "  const pts=inp.length>=6?60:inp.length>=5?40:inp.length>=4?20:10;\n"
  "  /* Phase 221: Multilingual Bonus +10 when word valid in both DE & EN */\n"
  "  let _wsBonusPts=0;\n"
  "  try{const _cL=S.wsData.lang===\"de\"?\"en\":\"de\";const _cE=(WORTSCHMIEDE_DATA[S.wsData.cityIdx]||{}).validWords;const _cW=_cE&&Array.isArray(_cE[_cL])?_cE[_cL].map(function(w){return w.toUpperCase();}):[];if(_cW.includes(inp))_wsBonusPts=10;}catch(e){}\n"
  "  S.sc+=pts+_wsBonusPts;S.correct+=1;\n"
  "  if(_wsBonusPts>0)showToast(\"\\uD83C\\uDF0D \"+esc(inp)+\" — Multilingual! +\"+pts+\" +\"+_wsBonusPts+\" Bonus\");\n"
  "  if(window.mpGameCh)mpSend(\"score_update\",{score:S.sc,rd:S.rd||0,correct:S.correct||0});"
)

if OLD not in content:
    print("ERROR: OLD pattern not found in handleWsCheck!")
    idx = content.find("S.wsData.foundWords.push(inp)")
    print(repr(content[idx:idx+300]))
    sys.exit(1)

content = content.replace(OLD, NEW, 1)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("OK: Wort-Schmiede multilingual bonus (+10) implemented")
