"""
patch_fix_pin_feedback.py
==========================
Fix 1: uk_pin / airport_pin feedback pill shows "0 Pkt." even when pts > 0.
        Points ARE correctly added to S.sc, but the display was hardcoded to 0.
Fix 2: Map label (correct answer text) truncated to max 25 chars to prevent overflow.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GEN  = os.path.join(ROOT, 'gen.py')

with open(GEN, 'r', encoding='utf-8') as fh:
    c = fh.read()

# ── Fix 1: Feedback pill — show actual pts even on wrong (X) answer ──────────
OLD_FB = ('      :S.ok?`<div class="fb ok">\\u2713 ${apDist} km entfernt \\u00b7 +${apPts} Pkt.</div>`\n'
          '      :`<div class="fb ng">\\u2717 ${apDist} km entfernt \\u00b7 0 Pkt.</div>`;')
NEW_FB = ('      :S.ok?`<div class="fb ok">\\u2713 ${apDist} km entfernt \\u00b7 +${apPts} Pkt.</div>`\n'
          '      :`<div class="fb ng">\\u2717 ${apDist} km entfernt${apPts>0?" \\u00b7 +"+apPts+" Pkt.":""}</div>`;')

assert c.count(OLD_FB) == 1, f"Anchor not unique: pin feedback pill"
c = c.replace(OLD_FB, NEW_FB)
print("  [OK] Fix 1: uk_pin feedback pill shows real pts on wrong answer")

# ── Fix 2: Map label — truncate long names to prevent overflow ───────────────
OLD_LBL = ('      .attr("font-size","10px").attr("fill","#10b981")\n'
           '      .attr("font-weight","900").text(S.q.ans);')
NEW_LBL = ('      .attr("font-size","9px").attr("fill","#10b981")\n'
           '      .attr("font-weight","700")\n'
           '      .text((S.q.ans||"").length>22?(S.q.ans||"").slice(0,20)+"\\u2026":S.q.ans||"");')

assert c.count(OLD_LBL) == 1, f"Anchor not unique: map label"
c = c.replace(OLD_LBL, NEW_LBL)
print("  [OK] Fix 2: Map label truncated at 22 chars to prevent overflow")

with open(GEN, 'w', encoding='utf-8') as fh:
    fh.write(c)
print("  [OK] gen.py updated")
