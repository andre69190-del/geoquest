# -*- coding: utf-8 -*-
"""
Phase: 289
Date:  2026-05-29
Scope: comparisons-Kategorie (comp_*) Frage-Prompts de/en/pl

Die comp_*-Generatoren hatten hartkodierte deutsche Prompts (nur DE).
Jetzt laufen sie ueber _tc() (aus Phase 288) -> de unveraendert, en+pl ergaenzt.
  - _compQ(): ein zentrales prompt=_tc(prompt)  (deckt 11 Vergleiche ab)
  - 5 Spezial-Generatoren (comp_airports/flight/mountain/nsextent/olympics):
    prompt:"..." -> prompt:_tc("...")
_CONTENT_I18N wird auf gueltiges JSON normalisiert (Top-Level-Sprachkeys
quoted), damit Folge-Phasen (290/291) sauber per json.loads erweitern koennen.

Dependencies: patch_288_pl_content_i18n.py
"""
import os, re, json

GEN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'gen.py')
content = open(GEN, encoding='utf-8').read()

# ---------------------------------------------------------------
# 1) _compQ zentral wrappen
# ---------------------------------------------------------------
anchor = 'function _compQ(type,prompt,a,b,aVal,bVal,fmtFn){'
assert content.count(anchor) == 1, ('_compQ anchor', content.count(anchor))
content = content.replace(anchor, anchor + 'prompt=_tc(prompt);', 1)
print('[OK]   _compQ: prompt=_tc(prompt)')

# 11 _compQ-Prompts (deutsche Schluessel -> en/pl)
COMP_EN = {
"Welches Land ist größer?": "Which country is larger?",
"Welches Land hat mehr Einwohner?": "Which country has more inhabitants?",
"Welches Land liegt weiter nördlich?": "Which country lies further north?",
"Welches Land hat ein höheres BIP pro Kopf?": "Which country has a higher GDP per capita?",
"Welches Land ist dichter besiedelt?": "Which country is more densely populated?",
"Welches Land hat den höheren Gipfel?": "Which country has the higher peak?",
"Welches Land hat die längere Küste?": "Which country has the longer coastline?",
"Welches Land hat mehr Nachbarländer?": "Which country has more neighbouring countries?",
"In welchem Land lebt man länger?": "In which country do people live longer?",
"Welches Land hat ein höheres Medianalter?": "Which country has a higher median age?",
"Welches Land hat mehr Waldfläche?": "Which country has more forest area?",
}
COMP_PL = {
"Welches Land ist größer?": "Który kraj jest większy?",
"Welches Land hat mehr Einwohner?": "Który kraj ma więcej mieszkańców?",
"Welches Land liegt weiter nördlich?": "Który kraj leży dalej na północ?",
"Welches Land hat ein höheres BIP pro Kopf?": "Który kraj ma wyższe PKB na mieszkańca?",
"Welches Land ist dichter besiedelt?": "Który kraj jest gęściej zaludniony?",
"Welches Land hat den höheren Gipfel?": "Który kraj ma wyższy szczyt?",
"Welches Land hat die längere Küste?": "Który kraj ma dłuższą linię brzegową?",
"Welches Land hat mehr Nachbarländer?": "Który kraj ma więcej krajów sąsiednich?",
"In welchem Land lebt man länger?": "W którym kraju żyje się dłużej?",
"Welches Land hat ein höheres Medianalter?": "Który kraj ma wyższą medianę wieku?",
"Welches Land hat mehr Waldfläche?": "Który kraj ma większą powierzchnię lasów?",
}

# ---------------------------------------------------------------
# 2) 5 Spezial-Generatoren wrappen (prompt aus Datei kapseln, Emoji exakt)
# ---------------------------------------------------------------
def _decode(s):
    s = re.sub(r'\\u\{([0-9A-Fa-f]+)\}', lambda m: chr(int(m.group(1), 16)), s)
    s = re.sub(r'\\u([0-9A-Fa-f]{4})', lambda m: chr(int(m.group(1), 16)), s)
    return s

# typ -> (englischer Text, polnischer Text)  ohne Emoji; Emoji wird aus dem
# Original-Prompt automatisch vorangestellt.
SPECIAL = {
"comp_airports": ("Which country has more airports?", "Który kraj ma więcej lotnisk?"),
"comp_flight":   ("In which country is the longest domestic flight farther?", "W którym kraju najdłuższy lot krajowy jest dalszy?"),
"comp_mountain": ("Which country has the higher peak?", "Który kraj ma wyższy szczyt?"),
"comp_nsextent": ("Which country is longer from north to south?", "Który kraj jest dłuższy z północy na południe?"),
"comp_olympics": ("Which country has more Olympic gold (Summer)?", "Który kraj ma więcej złotych medali olimpijskich (lato)?"),
}
for typ, (en, pl) in SPECIAL.items():
    m = re.search(r'type:"' + typ + r'",[\s\S]{0,300}?prompt:"([^"]*)"', content)
    assert m, ('special prompt not found: ' + typ)
    src = m.group(1)
    old = 'prompt:"' + src + '"'
    new = 'prompt:_tc("' + src + '")'
    assert content.count(old) == 1, ('special prompt anchor', typ, content.count(old))
    content = content.replace(old, new, 1)
    key = _decode(src)                          # Laufzeit-Schluessel (mit Emoji)
    prefix = key.split(' ', 1)[0] + ' '         # Emoji + Space
    COMP_EN[key] = prefix + en
    COMP_PL[key] = prefix + pl
    print(f'[OK]   {typ}: prompt -> _tc')

# ---------------------------------------------------------------
# 3) _CONTENT_I18N normalisieren + en/pl ergaenzen
# ---------------------------------------------------------------
s_idx = content.index('const _CONTENT_I18N=') + len('const _CONTENT_I18N=')
# brace-match
d = 0; k = s_idx; ins = None; esc = False
while k < len(content):
    c = content[k]
    if ins:
        if esc: esc = False
        elif c == '\\': esc = True
        elif c == ins: ins = None
    else:
        if c in '"\'`': ins = c
        elif c == '{': d += 1
        elif c == '}':
            d -= 1
            if d == 0: k += 1; break
    k += 1
obj_src = content[s_idx:k]
try:
    data = json.loads(obj_src)                  # falls schon normalisiert
except json.JSONDecodeError:
    inner = obj_src[obj_src.index('{pl:') + len('{pl:'):-1]
    data = {'pl': json.loads(inner)}
data.setdefault('en', {}).update(COMP_EN)
data['pl'].update(COMP_PL)
new_obj = json.dumps(data, ensure_ascii=False)
content = content[:s_idx] + new_obj + content[k:]
print(f'[OK]   _CONTENT_I18N normalisiert; +{len(COMP_EN)} en, +{len(COMP_PL)} pl (comp_*)')

# ---------------------------------------------------------------
_tmp = GEN + '.tmp'
with open(_tmp, 'w', encoding='utf-8') as f:
    f.write(content)
os.replace(_tmp, GEN)
print('\nPatch complete.')
