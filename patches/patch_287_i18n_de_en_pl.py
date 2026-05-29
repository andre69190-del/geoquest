# -*- coding: utf-8 -*-
"""
Phase: 287
Date:  2026-05-29
Author: Claude / Andre
Scope: i18n de/en/pl - hartkodierte deutsche Prompts lokalisieren + Polnisch UI vervollstaendigen

Description:
  Befund (Audit): Nur de/en waren durchgaengig vollstaendig. Zwei Luecken behoben:

  TEIL A - 15 hartkodierte deutsche Frage-Prompts auf t() umgestellt:
    Generatoren gaben prompt:"<deutsch>" direkt zurueck -> allen Sprachen Deutsch.
    Jetzt prompt:t("q_..."). Der deutsche Wert wird 1:1 aus dem Original uebernommen
    (kein Risiko einer de-Regression), en + pl werden ergaenzt. Andere Sprachen
    fallen wie gewuenscht auf Englisch zurueck.

  TEIL B - 31 fehlende LANG.pl-Schluessel ergaenzt (inkl. Wort-Schmiede):
    Bisher fielen diese auf Englisch zurueck. Jetzt echte polnische Uebersetzungen.

  Bewusst NICHT angefasst: weitere Sprachen ausser de/en/pl (laut Vorgabe nicht noetig).

  Robustheit: Prompt-Ersetzung via Regex auf ASCII-Anker type:"..." (haengt nicht
  von exakten Umlaut-/Emoji-Bytes ab). LANG-Inserts via ASCII-Anker (erste Keys).

Dependencies: patch_286_mp_show_opp_answer.py
"""

import os, re

GEN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'gen.py')
with open(GEN, encoding='utf-8') as f:
    content = f.read()

errors = []

# =====================================================================
# TEIL A: 15 hartkodierte Prompts -> t("key")
#   (regex_pattern, key, en_value, pl_value)
#   de-Wert wird aus dem Original-Match uebernommen.
# =====================================================================
PROMPT_FIXES = [
    (r'(return\{type:"curr_real",)prompt:"([^"]*)"', 'q_curr_real',
        'Which currency does … use?', 'Jakiej waluty używa …?'),
    (r'(return\{type:"neighbor",)prompt:"(Grenzt[^"]*)"', 'q_neighbor_not',
        'Does NOT border…?', 'NIE graniczy z…?'),
    (r'(return\{type:"neighbor",)prompt:"(Welches Land grenzt an[^"]*)"', 'q_neighbor',
        'Which country borders…?', 'Który kraj graniczy z…?'),
    (r'(return\{type:"neighbor_fake",)prompt:"([^"]*)"', 'q_neighbor_fake',
        'Which country does NOT border …?', 'Który kraj NIE graniczy z …?'),
    (r'(return\{type:"neighbor_count",)prompt:"([^"]*)"', 'q_neighbor_count',
        'How many neighbouring countries does this country have?', 'Ile sąsiadów ma ten kraj?'),
    (r'(return\{type:"border_q",)prompt:"([^"]*)"', 'q_border_shared',
        'Do these countries share a border?', 'Czy te kraje mają wspólną granicę?'),
    (r'(return\{type:"de_plate",)prompt:"([^"]*)"', 'q_de_plate',
        'Which city/region has this licence plate?', 'Które miasto/region ma tę tablicę rejestracyjną?'),
    (r'(return\{type:"map_reverse",)prompt:"([^"]*)"', 'q_map_reverse',
        'Which country is highlighted?', 'Który kraj jest podświetlony?'),
    (r'(return\{type:"stadium",)prompt:"([^"]*)"', 'q_stadium',
        '⚽ In which country is this stadium?', '⚽ W którym kraju jest ten stadion?'),
    (r'(return\{type:"jersey",)prompt:"([^"]*)"', 'q_jersey',
        '👕 Which country wears this jersey?', '👕 Który kraj nosi tę koszulkę?'),
    (r'(return\{type:"crest",)prompt:"([^"]*)"', 'q_crest',
        '🛡 Which country does this crest belong to?', '🛡 Do którego kraju należy ten herb?'),
    (r'(return\{type:"beta_hl",)prompt:"([^"]*)"', 'q_beta_hl_stadium',
        'Which stadium is higher above sea level?', 'Który stadion leży wyżej nad poziomem morza?'),
    (r'(return\{type:"beta_spotter",)prompt:"([^"]*)"', 'q_beta_spotter',
        'World map', 'Mapa świata'),
    (r'(return\{type:"sport_poi",)prompt:"([^"]*)"', 'q_sport_poi',
        'In which country is this?', 'W którym kraju to się znajduje?'),
    (r'(return\{type:"wappen",)prompt:"([^"]*)"', 'q_wappen',
        'Which country does this coat of arms belong to?', 'Do którego kraju należy ten herb?'),
]

new_de, new_en, new_pl = {}, {}, {}

for pat, key, en, pl in PROMPT_FIXES:
    matches = list(re.finditer(pat, content))
    if len(matches) != 1:
        errors.append(f'PROMPT {key}: expected 1 match, found {len(matches)}')
        continue
    m = matches[0]
    de_original = m.group(2)            # exakter Original-Prompt (de)
    new_de[key] = de_original
    new_en[key] = en
    new_pl[key] = pl
    content = content[:m.start()] + m.group(1) + f'prompt:t("{key}")' + content[m.end():]
    print(f'[OK]   prompt -> t("{key}")')

# Diese 3 t()-Keys existieren bereits in LANG (de/en/pl) - nur die Prompt-Umstellung
# auf t() war noetig; erneutes Einfuegen wuerde Duplicate-Keys erzeugen.
for _k in ('q_curr_real', 'q_neighbor_not', 'q_neighbor'):
    new_de.pop(_k, None); new_en.pop(_k, None); new_pl.pop(_k, None)

# =====================================================================
# TEIL B: 31 fehlende LANG.pl-Keys (de/en existieren bereits)
# =====================================================================
pl_only = {
    # H/L Vergleichs-Prompts
    'q_hl_gdp': 'Wyższe PKB/os. niż {a}?',
    'q_hl_density': 'Gęściej zaludnione niż {a}?',
    'q_hl_elevation': 'Wyższy szczyt niż {a}?',
    'q_hl_coastline': 'Dłuższe wybrzeże niż {a}?',
    'q_hl_borders': 'Więcej sąsiadów niż {a}?',
    'q_hl_lifeexp': 'Dłuższe życie niż w {a}?',
    'q_hl_median_age': 'Wyższy wiek mediany niż {a}?',
    'q_hl_forest': 'Więcej lasów niż {a}?',
    # Modus-Titel
    'mode_hauptstadt_dist': 'Odległość stolic',
    'mode_flugrouten_duell': 'Pojedynek tras lotniczych',
    'mode_insel_festland': 'Wyspa czy ląd stały',
    'mode_aequator': 'Na północ czy na południe?',
    'mode_wort_schmiede': 'Kuźnia Słów',
    # Schwierigkeit
    'diff_desc_blitz': '⚡ Blitz: 60 sekund · Jak najwięcej pytań',
    # Karten / Pin / UK
    'q_airport_pin': 'Gdzie leży to lotnisko?',
    'click_map': 'Dotknij mapy',
    'q_uk_match': 'Z jakiego kraju pochodzi:',
    'q_uk_pin': 'Gdzie to jest na mapie?',
    'uk_hl_higher': 'Wyżej ↑',
    'uk_hl_lower': 'Niżej ↓',
    'uk_hl_prompt': 'Który budynek jest wyższy?',
    # Spotter
    'spotter_no_region': r'nie ma regionów – wpisz \"{code}\"!',
    # Wort-Schmiede UI
    'ws_found': 'Znalezione',
    'ws_enter_word': 'Wpisz słowo…',
    'ws_check': 'Sprawdź',
    'ws_all_found': 'Znaleziono wszystkie słowa!',
    'ws_next_city': 'Następne miasto',
    'ws_duplicate': '✓ Już znalezione!',
    'ws_invalid': '✕ Nieprawidłowe słowo',
    'ws_lang_label': 'Język',
    'ws_letters_hint': 'Twórz słowa z liter miasta',
}

def build_obj(d):
    # d: key -> JS-string-content (inner quotes already escaped)
    return ''.join(f'{k}:"{v}",' for k, v in d.items())

# --- in de-Block einfuegen (neue Prompt-Keys, de=Original) ---
anchor_de = 'play:"SPIELEN",again:"NOCHMAL",'
if content.count(anchor_de) == 1:
    content = content.replace(anchor_de, anchor_de + build_obj(new_de), 1)
    print(f'[OK]   de: +{len(new_de)} Prompt-Keys')
else:
    errors.append(f'de anchor count = {content.count(anchor_de)}')

# --- in en-Block einfuegen (neue Prompt-Keys) ---
anchor_en = 'play:"PLAY",again:"PLAY AGAIN",'
if content.count(anchor_en) == 1:
    content = content.replace(anchor_en, anchor_en + build_obj(new_en), 1)
    print(f'[OK]   en: +{len(new_en)} Prompt-Keys')
else:
    errors.append(f'en anchor count = {content.count(anchor_en)}')

# --- in pl-Block einfuegen (neue Prompt-Keys + 31 fehlende Keys) ---
anchor_pl = 'play:"GRAJ",again:"ZAGRAJ PONOWNIE",'
pl_all = {}
pl_all.update(new_pl)     # 15 neue Prompt-Keys auf pl
pl_all.update(pl_only)    # 31 fehlende UI/WS-Keys auf pl
if content.count(anchor_pl) == 1:
    content = content.replace(anchor_pl, anchor_pl + build_obj(pl_all), 1)
    print(f'[OK]   pl: +{len(pl_all)} Keys ({len(new_pl)} Prompts + {len(pl_only)} UI/WS)')
else:
    errors.append(f'pl anchor count = {content.count(anchor_pl)}')

# =====================================================================
if errors:
    print('\n[ABORT] Fehler - gen.py NICHT geschrieben:')
    for e in errors:
        print('   -', e)
    raise SystemExit(1)

_tmp = GEN + '.tmp'
with open(_tmp, 'w', encoding='utf-8') as f:
    f.write(content)
os.replace(_tmp, GEN)
print('\nPatch complete.')
