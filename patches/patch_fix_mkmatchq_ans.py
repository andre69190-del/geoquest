"""
patch_fix_mkmatchq_ans.py
==========================
Bug: _mkMatchQ factory returns {correct: correct.c, ...} but both
     answer() and the render button-highlight code check q.ans.
     Result: q.ans === undefined → every answer is always wrong,
     correct button never turns green, score stays 0.

Affected: ALL Arch/Tech/Emob/Gastro match modes (~60 modes).

Fix: rename field `correct` → `ans` in _mkMatchQ return object,
     matching the contract used by genUniversalMatchQ and the render engine.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GEN  = os.path.join(ROOT, 'gen.py')

with open(GEN, 'r', encoding='utf-8') as fh:
    c = fh.read()

OLD = (
    '    return{type:"uk_match",subj:correct.n,correct:correct.c,opts:opts,\n'
    '      prompt:d.prompt||"Ordne richtig zu:"};'
)
NEW = (
    '    return{type:"uk_match",subj:correct.n,ans:correct.c,opts:opts,\n'
    '      prompt:d.prompt||"Ordne richtig zu:"};'
)

assert c.count(OLD) == 1, f"Anchor not unique: _mkMatchQ return (found {c.count(OLD)})"
c = c.replace(OLD, NEW)
print("  [OK] _mkMatchQ: field renamed correct→ans — correct button now turns green")

with open(GEN, 'w', encoding='utf-8') as fh:
    fh.write(c)
print("  [OK] gen.py updated")
