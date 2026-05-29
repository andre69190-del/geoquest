"""
Phase: 281
Date:  2026-05-29
Author: Claude / Andre
Scope: 1v1 Sync: mpCountdown render-Fix + vollstaendige Math.random->rng() Migration

Description:
  BUG 1 - mpCountdown Countdown zeigt nur "3":
    render() wurde nur einmal am Anfang aufgerufen. Das setInterval
    aktualisierte S.mp.countdown, aber render() wurde nicht erneut
    aufgerufen, daher blieb die Anzeige bei "3" stehen.
    Fix: render() im else-Zweig des Intervalls hinzugefuegt.

  BUG 2 - Unterschiedliche Fragen trotz gleichem Seed:
    8 Fragen-Generatoren nutzten Math.random() statt rng().
    initRng(seed) setzt nur rngState/rngSeed zurueck, aber
    Math.random() laeuft unabhaengig davon. Deshalb bekamen beide
    Spieler mit identischem Seed unterschiedliche Fragen.

    Gefixte Generatoren:
    - getSmartVersusOpponent (comp_* Modi)
    - getVersusCountryPair (comp_* Modi)
    - getVersusCountryPairAdvanced (comp_* Modi)
    - getFlagFusionPairSafe (flag_fusion Modus)
    - renderFlagFusion (askAbout-Auswahl + wrongOptions-Shuffle)
    - initLogikGitter (Grid-Typ + _shuf Funktion)
    - genTravelRoute start/target (travel_route Modus)

Dependencies: patch_280_bugfixes.py
Zero-Bug Policy: All c.replace() calls assert uniqueness before applying
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
# FIX 1: mpCountdown – render() bei jedem Tick
# ============================================================
patch(
    r"""    t--;S.mp.countdown=t;
    if(t<=0){""",
    r"""    t--;S.mp.countdown=t;render();
    if(t<=0){""",
    'mpCountdown: render() bei jedem Tick'
)


# ============================================================
# FIX 2: getSmartVersusOpponent – Math.random() -> rng()
# ============================================================
patch(
    'if(filteredCountries.length<3){return COUNTRIES[Math.floor(Math.random()*COUNTRIES.length)];}',
    'if(filteredCountries.length<3){return COUNTRIES[~~(rng()*COUNTRIES.length)];}',
    'getSmartVersusOpponent: Fallback random'
)
patch(
    'if(currentIdx<0){return filteredCountries[Math.floor(Math.random()*filteredCountries.length)];}',
    'if(currentIdx<0){return filteredCountries[~~(rng()*filteredCountries.length)];}',
    'getSmartVersusOpponent: currentIdx<0 fallback'
)
patch(
    'currentIdx=Math.floor(Math.random()*filteredCountries.length);',
    'currentIdx=~~(rng()*filteredCountries.length);',
    'getSmartVersusOpponent: retry random'
)
patch(
    r"""return filteredCountries[Math.floor(Math.random()*filteredCountries.length)];
}

function setCorrectAnswerObfuscated""",
    r"""return filteredCountries[~~(rng()*filteredCountries.length)];
}

function setCorrectAnswerObfuscated""",
    'getSmartVersusOpponent: final fallback'
)


# ============================================================
# FIX 3: getVersusCountryPair – Math.random() -> rng()
# ============================================================
patch(
    r"""// Pick random country A
const idxA=Math.floor(Math.random()*sorted.length);
const countryA=sorted[idxA];
// Pick country B from neighbors only (Â±1 or Â±2 positions)
let idxB=idxA+Math.floor(Math.random()*3)-1; // -1, 0, or +1""",
    r"""// Pick random country A
const idxA=~~(rng()*sorted.length);
const countryA=sorted[idxA];
// Pick country B from neighbors only (±1 or ±2 positions)
let idxB=idxA+~~(rng()*3)-1; // -1, 0, or +1""",
    'getVersusCountryPair: idxA + idxB initial'
)
patch(
    r"""while(getMetricValue(countryA,metric)===getMetricValue(countryB,metric)&&attempts<5){
idxB=Math.floor(Math.random()*sorted.length);
attempts++;
}
return{countryA,countryB,correctIdx:getMetricValue""",
    r"""while(getMetricValue(countryA,metric)===getMetricValue(countryB,metric)&&attempts<5){
idxB=~~(rng()*sorted.length);
attempts++;
}
return{countryA,countryB,correctIdx:getMetricValue""",
    'getVersusCountryPair: tie-breaker retry'
)


# ============================================================
# FIX 4: getVersusCountryPairAdvanced – Math.random() -> rng()
# ============================================================
patch(
    r"""const idxA=Math.floor(Math.random()*sorted.length);
const countryA=sorted[idxA];
let idxB=idxA+Math.floor(Math.random()*3)-1;""",
    r"""const idxA=~~(rng()*sorted.length);
const countryA=sorted[idxA];
let idxB=idxA+~~(rng()*3)-1;""",
    'getVersusCountryPairAdvanced: idxA + idxB'
)
patch(
    r"""while(getAdvancedMetricValue(countryA,metric)===getAdvancedMetricValue(countryB,metric)&&attempts<5){
idxB=Math.floor(Math.random()*sorted.length);
attempts++;
}""",
    r"""while(getAdvancedMetricValue(countryA,metric)===getAdvancedMetricValue(countryB,metric)&&attempts<5){
idxB=~~(rng()*sorted.length);
attempts++;
}""",
    'getVersusCountryPairAdvanced: tie-breaker retry'
)


# ============================================================
# FIX 5: getFlagFusionPairSafe – Math.random() -> rng()
# ============================================================
patch(
    r"""const idx1=Math.floor(Math.random()*codes.length);
let idx2=Math.floor(Math.random()*codes.length);
while(idx2===idx1)idx2=Math.floor(Math.random()*codes.length);""",
    r"""const idx1=~~(rng()*codes.length);
let idx2=~~(rng()*codes.length);
while(idx2===idx1)idx2=~~(rng()*codes.length);""",
    'getFlagFusionPairSafe: idx1 + idx2'
)


# ============================================================
# FIX 6: renderFlagFusion – Math.random() -> rng()
# ============================================================
patch(
    'const askAbout=Math.random()>0.5?country1:country2;',
    'const askAbout=rng()>0.5?country1:country2;',
    'renderFlagFusion: askAbout selection'
)
patch(
    r"""const wrongOptions=COUNTRIES.filter(c=>c.c!==code1&&c.c!==code2).sort(()=>Math.random()-0.5).slice(0,3);
const allOptions=[askAbout,...wrongOptions].sort(()=>Math.random()-0.5);""",
    r"""const wrongOptions=COUNTRIES.filter(c=>c.c!==code1&&c.c!==code2).sort(()=>rng()-0.5).slice(0,3);
const allOptions=[askAbout,...wrongOptions].sort(()=>rng()-0.5);""",
    'renderFlagFusion: wrongOptions + allOptions shuffle'
)


# ============================================================
# FIX 7: initLogikGitter – _shuf + gtype Math.random() -> rng()
# ============================================================
patch(
    r"""  function _shuf(a){const b=a.slice();for(let i=b.length-1;i>0;i--){const j=~~(Math.random()*(i+1));[b[i],b[j]]=[b[j],b[i]];}return b;}""",
    r"""  function _shuf(a){const b=a.slice();for(let i=b.length-1;i>0;i--){const j=~~(rng()*(i+1));[b[i],b[j]]=[b[j],b[i]];}return b;}""",
    'initLogikGitter: _shuf intern'
)
patch(
    r"""  const gtype=_gtm||_types[~~(Math.random()*_types.length)];""",
    r"""  const gtype=_gtm||_types[~~(rng()*_types.length)];""",
    'initLogikGitter: gtype selection'
)


# ============================================================
# FIX 8: genTravelRoute – start/target Math.random() -> rng()
# ============================================================
patch(
    r"""    start=keys[~~(Math.random()*keys.length)];
    target=keys[~~(Math.random()*keys.length)];""",
    r"""    start=keys[~~(rng()*keys.length)];
    target=keys[~~(rng()*keys.length)];""",
    'genTravelRoute: start + target selection'
)


# ============================================================
# Write + Summary
# ============================================================
with open(GEN, 'w', encoding='utf-8') as f:
    f.write(content)

# Count remaining Math.random() in generator range (sanity check)
import re
gen_section = content[content.find('function getSmartVersusOpponent'):
                      content.find('function _isPortrait')]
remaining = [(m.start(), content[:content.find('function getSmartVersusOpponent')+m.start()].count('\n'))
             for m in re.finditer(r'Math\.random\(\)', gen_section)
             if 'Token' not in content[content.find('function getSmartVersusOpponent'):][max(0,m.start()-50):m.start()+50]
             and '_cSalt' not in content[content.find('function getSmartVersusOpponent'):][max(0,m.start()-50):m.start()+50]]

print(f'\nVerbleibende Math.random() im Generator-Bereich: {len(remaining)}')
print('\nRun: python3 gen.py && python3 verify.py')
