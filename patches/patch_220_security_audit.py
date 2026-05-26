#!/usr/bin/env python3
"""Phase 220: Grand Finale — Streak system, BETA cleanup, meta fix, museen coords"""
import re

GEN = '/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py'
content = open(GEN, 'r', encoding='utf-8').read()
changes = []

# ─────────────────────────────────────────────────────────────────────────────
# 1. ADD updateDailyStreak() function after _gqLoad definition
# ─────────────────────────────────────────────────────────────────────────────
STREAK_FN = r"""
/* ===== Phase 220: Daily Streak System ===== */
function updateDailyStreak(){
  try{
    /* Use en-CA locale for reliable YYYY-MM-DD without library */
    const today=new Date().toLocaleDateString('en-CA');
    const lastPlay=_gqLoad('gq_last_play',null);
    let streak=_gqLoad('gq_streak',0)||0;
    if(lastPlay===today)return streak;          /* same day — no change */
    if(lastPlay){
      const diffMs=new Date(today)-new Date(lastPlay);
      const diffDays=Math.round(diffMs/86400000);
      streak=(diffDays===1)?streak+1:1;         /* consecutive = +1, gap = reset */
    }else{
      streak=1;                                 /* first ever game */
    }
    _gqSave('gq_last_play',today);
    _gqSave('gq_streak',streak);
    return streak;
  }catch(e){return 0;}
}
function getStreak(){return _gqLoad('gq_streak',0)||0;}
"""

# Insert after _gqLoad function
insert_after = 'function _gqLoad(key,fallback){'
idx_load = content.find(insert_after)
if idx_load > 0:
    # Find the closing } of _gqLoad
    depth = 0
    i = idx_load
    while i < len(content):
        if content[i] == '{': depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                insert_pos = i + 1
                break
        i += 1
    content = content[:insert_pos] + STREAK_FN + content[insert_pos:]
    changes.append('Added updateDailyStreak() + getStreak() functions')
else:
    print('WARN: _gqLoad not found')

# ─────────────────────────────────────────────────────────────────────────────
# 2. CALL updateDailyStreak() at ALL 4 gameover trigger points
# ─────────────────────────────────────────────────────────────────────────────
GAMEOVER_TRIGGER = 'S.ph="gameover";S.scoreSaved=false;S.convModal=true;soundOver();checkMastery();'
GAMEOVER_WITH_STREAK = 'S.ph="gameover";S.scoreSaved=false;S.convModal=true;soundOver();checkMastery();updateDailyStreak();'

count_replaced = content.count(GAMEOVER_TRIGGER)
if count_replaced > 0:
    content = content.replace(GAMEOVER_TRIGGER, GAMEOVER_WITH_STREAK)
    changes.append(f'Added updateDailyStreak() call to {count_replaced} gameover trigger(s)')
else:
    # Try the variant with newline
    alt = 'S.ph="gameover";S.scoreSaved=false;S.convModal=true;\n  checkMastery();'
    alt_new = 'S.ph="gameover";S.scoreSaved=false;S.convModal=true;\n  checkMastery();updateDailyStreak();'
    if alt in content:
        content = content.replace(alt, alt_new)
        changes.append('Added updateDailyStreak() call (alt variant) to gameover trigger')
    else:
        print('WARN: gameover trigger pattern not found')

# ─────────────────────────────────────────────────────────────────────────────
# 3. ADD STREAK BADGE in renderHomeTab header
# ─────────────────────────────────────────────────────────────────────────────
# The header is built as `_hdr`. We'll add streak reading before _hdr and inject badge.

# Find the line: const _gc=(sbProfile?.geo_coins||0).toLocaleString();
OLD_GC_LINE = "  const _gc=(sbProfile?.geo_coins||0).toLocaleString();"
NEW_GC_LINE = """  const _gc=(sbProfile?.geo_coins||0).toLocaleString();
  const _streakN=getStreak();
  const _streakBadge=_streakN>0?`<div style="display:flex;align-items:center;gap:3px;background:rgba(239,68,68,.13);border-radius:16px;padding:.18rem .55rem;font-size:.78rem;font-weight:700;color:#ef4444;border:1px solid rgba(239,68,68,.22)">\\u{1F525} ${_streakN}${_streakN===1?' Tag':' Tage'}</div>`:'';"""

if OLD_GC_LINE in content:
    content = content.replace(OLD_GC_LINE, NEW_GC_LINE)
    changes.append('Added streak badge variable to renderHomeTab')
else:
    print('WARN: _gc line not found for streak badge injection')

# Inject streak badge into the logged-in header name div
OLD_LOGGED_IN_NAME = '<div style="font-size:1.05rem;font-weight:700;color:var(--text)">${t("home_hi",{name:_un})}</div>'
NEW_LOGGED_IN_NAME = '<div style="display:flex;align-items:center;gap:8px"><div style="font-size:1.05rem;font-weight:700;color:var(--text)">${t("home_hi",{name:_un})}</div>${_streakBadge}</div>'

if OLD_LOGGED_IN_NAME in content:
    content = content.replace(OLD_LOGGED_IN_NAME, NEW_LOGGED_IN_NAME)
    changes.append('Injected streak badge into logged-in header')
else:
    print('WARN: logged-in name div not found for streak badge')

# Inject streak badge into guest header too
OLD_GUEST_NAME = '<div style="font-size:1.05rem;font-weight:700;color:var(--text)">${t("home_guest")}</div>'
NEW_GUEST_NAME = '<div style="display:flex;align-items:center;gap:8px"><div style="font-size:1.05rem;font-weight:700;color:var(--text)">${t("home_guest")}</div>${_streakBadge}</div>'

if OLD_GUEST_NAME in content:
    content = content.replace(OLD_GUEST_NAME, NEW_GUEST_NAME)
    changes.append('Injected streak badge into guest header')
else:
    print('WARN: guest name div not found for streak badge')

# ─────────────────────────────────────────────────────────────────────────────
# 4. REMOVE ALL [BETA] PREFIXES from MODES titles
# ─────────────────────────────────────────────────────────────────────────────
beta_count_before = content.count('[BETA] ')
content = content.replace('[BETA] ', '')
beta_count_after = content.count('[BETA] ')
removed = beta_count_before - beta_count_after
changes.append(f'Removed {removed} [BETA] prefixes from mode titles')

# Also check for "[BETA]" without trailing space
beta2 = content.count('[BETA]')
if beta2 > 0:
    content = content.replace('[BETA]', '')
    changes.append(f'Removed {beta2} additional [BETA] tags (no space)')

# ─────────────────────────────────────────────────────────────────────────────
# 5. FIX VIEWPORT META — add user-scalable=no, maximum-scale=1
# ─────────────────────────────────────────────────────────────────────────────
OLD_VIEWPORT = 'content="width=device-width,initial-scale=1,minimum-scale=1"'
NEW_VIEWPORT = 'content="width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no"'

if OLD_VIEWPORT in content:
    content = content.replace(OLD_VIEWPORT, NEW_VIEWPORT)
    changes.append('Viewport meta: added user-scalable=no, maximum-scale=1')
else:
    print('WARN: viewport meta not found')

# ─────────────────────────────────────────────────────────────────────────────
# WRITE
# ─────────────────────────────────────────────────────────────────────────────
open(GEN, 'w', encoding='utf-8').write(content)
print(f'✓ gen.py written ({len(content)} chars)')
print(f'\nChanges ({len(changes)}):')
for c in changes:
    print(f'  • {c}')
