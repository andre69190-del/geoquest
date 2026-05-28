"""
patch_271_beta_jersey_crest.py — Phase 271
1. Entfernt alle 🧪-BETA-Prefixe aus Modustitel in GeoQuest.html
2. Erweitert jerseys: 15 → 50 Einträge
3. Erweitert crests: 10 → 50 Einträge
4. Aktualisiert generate_spieluebersicht.py Hardcodes für jersey/crest
"""
import re, os

BASE = os.path.join(os.path.dirname(__file__), '..')
HTML_PATH = os.path.join(BASE, 'GeoQuest.html')
GEN_SUEBERSICHT = os.path.join(BASE, 'generate_spieluebersicht.py')

with open(HTML_PATH, encoding='utf-8') as f:
    content = f.read()

# ══════════════════════════════════════════════════════════════
# STEP 1: Remove 🧪 BETA prefixes from titles
# Both literal 🧪 and unicode escape \u{1F9EA}
# ══════════════════════════════════════════════════════════════
beta_literal = '\U0001F9EA '   # 🧪 + space
beta_escaped = r'\u{1F9EA} '   # unicode escape + space

count_lit = content.count(beta_literal)
count_esc = content.count(beta_escaped)

content = content.replace(beta_literal, '')
content = content.replace(beta_escaped, '')

print(f'BETA removal: {count_lit} literal + {count_esc} escaped = {count_lit+count_esc} total stripped')

# ══════════════════════════════════════════════════════════════
# STEP 2: Expand jerseys: 15 → 50
# ══════════════════════════════════════════════════════════════
JERSEY_35_NEW = [
    '{country:"Belgien",cc:"be",color:"#FF0000",style:"classic"}',
    '{country:"USA",cc:"us",color:"#002868",style:"classic"}',
    '{country:"Dänemark",cc:"dk",color:"#C8102E",style:"classic"}',
    '{country:"Schweiz",cc:"ch",color:"#FF0000",style:"classic"}',
    '{country:"Schweden",cc:"se",color:"#006AA7",style:"classic"}',
    '{country:"Polen",cc:"pl",color:"#FFFFFF",style:"classic"}',
    '{country:"Ukraine",cc:"ua",color:"#0057B8",style:"classic"}',
    '{country:"Türkei",cc:"tr",color:"#E30A17",style:"classic"}',
    '{country:"Australien",cc:"au",color:"#003399",style:"classic"}',
    '{country:"Senegal",cc:"sn",color:"#009A44",style:"classic"}',
    '{country:"Nigeria",cc:"ng",color:"#008751",style:"classic"}',
    '{country:"Kamerun",cc:"cm",color:"#007A5E",style:"classic"}',
    '{country:"Ghana",cc:"gh",color:"#006B3F",style:"classic"}',
    '{country:"Kolumbien",cc:"co",color:"#FCD116",style:"classic"}',
    '{country:"Chile",cc:"cl",color:"#D52B1E",style:"classic"}',
    '{country:"Uruguay",cc:"uy",color:"#5AAAFA",style:"classic"}',
    '{country:"Ecuador",cc:"ec",color:"#FFD100",style:"classic"}',
    '{country:"Südkorea",cc:"kr",color:"#C9353F",style:"classic"}',
    '{country:"Iran",cc:"ir",color:"#239F40",style:"classic"}',
    '{country:"Saudi-Arabien",cc:"sa",color:"#006C35",style:"classic"}',
    '{country:"Österreich",cc:"at",color:"#ED2939",style:"classic"}',
    '{country:"Tschechien",cc:"cz",color:"#D7141A",style:"classic"}',
    '{country:"Serbien",cc:"rs",color:"#C6363C",style:"classic"}',
    '{country:"Ungarn",cc:"hu",color:"#436F4D",style:"classic"}',
    '{country:"Griechenland",cc:"gr",color:"#0D5EAF",style:"classic"}',
    '{country:"Algerien",cc:"dz",color:"#006233",style:"classic"}',
    '{country:"Marokko 2",cc:"ma",color:"#FFFFFF",style:"classic"}',
    '{country:"Ägypten",cc:"eg",color:"#CC1F1F",style:"classic"}',
    '{country:"Costa Rica",cc:"cr",color:"#002B7F",style:"classic"}',
    '{country:"Kanada",cc:"ca",color:"#FF0000",style:"classic"}',
    '{country:"Elfenbeinküste",cc:"ci",color:"#FF6900",style:"classic"}',
    '{country:"Tunesien",cc:"tn",color:"#E70013",style:"classic"}',
    '{country:"Katar",cc:"qa",color:"#8D1B3D",style:"classic"}',
    '{country:"Rumänien",cc:"ro",color:"#002B7F",style:"stripes_v"}',
    '{country:"Norwegen",cc:"no",color:"#EF2B2D",style:"classic"}',
]

old_jerseys = '''jerseys:[
    {country:"Deutschland",cc:"de",color:"#FFFFFF",style:"classic"},
    {country:"Brasilien",cc:"br",color:"#FDEF42",style:"classic"},
    {country:"Argentinien",cc:"ar",color:"#74ACDF",style:"stripes_v"},
    {country:"Niederlande",cc:"nl",color:"#FF6600",style:"classic"},
    {country:"Portugal",cc:"pt",color:"#CC0000",style:"classic"},
    {country:"Frankreich",cc:"fr",color:"#003399",style:"classic"},
    {country:"England",cc:"gb",color:"#FFFFFF",style:"classic"},
    {country:"Spanien",cc:"es",color:"#CC0000",style:"classic"},
    {country:"Italien",cc:"it",color:"#003399",style:"classic"},
    {country:"Kroatien",cc:"hr",color:"#FF0000",style:"checkered"},
    {country:"Jamaika",cc:"jm",color:"#009B3A",style:"split"},
    {country:"Mexiko",cc:"mx",color:"#006847",style:"classic"},
    {country:"Japan",cc:"jp",color:"#00235D",style:"classic"},
    {country:"Marokko",cc:"ma",color:"#C1272D",style:"classic"},
    {country:"Argentinien 2",cc:"ar",color:"#003366",style:"stripes_v"},
  ],'''

new_jersey_lines = [
    '    {country:"Deutschland",cc:"de",color:"#FFFFFF",style:"classic"},',
    '    {country:"Brasilien",cc:"br",color:"#FDEF42",style:"classic"},',
    '    {country:"Argentinien",cc:"ar",color:"#74ACDF",style:"stripes_v"},',
    '    {country:"Niederlande",cc:"nl",color:"#FF6600",style:"classic"},',
    '    {country:"Portugal",cc:"pt",color:"#CC0000",style:"classic"},',
    '    {country:"Frankreich",cc:"fr",color:"#003399",style:"classic"},',
    '    {country:"England",cc:"gb",color:"#FFFFFF",style:"classic"},',
    '    {country:"Spanien",cc:"es",color:"#CC0000",style:"classic"},',
    '    {country:"Italien",cc:"it",color:"#003399",style:"classic"},',
    '    {country:"Kroatien",cc:"hr",color:"#FF0000",style:"checkered"},',
    '    {country:"Jamaika",cc:"jm",color:"#009B3A",style:"split"},',
    '    {country:"Mexiko",cc:"mx",color:"#006847",style:"classic"},',
    '    {country:"Japan",cc:"jp",color:"#00235D",style:"classic"},',
    '    {country:"Marokko",cc:"ma",color:"#C1272D",style:"classic"},',
    '    {country:"Argentinien 2",cc:"ar",color:"#003366",style:"stripes_v"},',
]
for e in JERSEY_35_NEW:
    new_jersey_lines.append(f'    {e},')

new_jerseys = 'jerseys:[\n' + '\n'.join(new_jersey_lines) + '\n  ],'

if old_jerseys in content:
    content = content.replace(old_jerseys, new_jerseys)
    print(f'Jerseys expanded: 15 → {15 + len(JERSEY_35_NEW)} items')
else:
    print('ERROR: old_jerseys not found - check whitespace!')

# ══════════════════════════════════════════════════════════════
# STEP 3: Expand crests: 10 → 50
# ══════════════════════════════════════════════════════════════
CREST_40_NEW = [
    '{country:"Belgien",cc:"be",shape:"lion",color:"#FF0000"}',
    '{country:"USA",cc:"us",shape:"shield",color:"#002868"}',
    '{country:"Uruguay",cc:"uy",shape:"sun",color:"#5AAAFA"}',
    '{country:"Mexiko",cc:"mx",shape:"eagle",color:"#006847"}',
    '{country:"Kanada",cc:"ca",shape:"maple",color:"#FF0000"}',
    '{country:"Australien",cc:"au",shape:"shield",color:"#003399"}',
    '{country:"Südkorea",cc:"kr",shape:"shield",color:"#C9353F"}',
    '{country:"Japan",cc:"jp",shape:"shield",color:"#BC002D"}',
    '{country:"Dänemark",cc:"dk",shape:"crown",color:"#C8102E"}',
    '{country:"Schweiz",cc:"ch",shape:"cross",color:"#FF0000"}',
    '{country:"Österreich",cc:"at",shape:"eagle",color:"#ED2939"}',
    '{country:"Polen",cc:"pl",shape:"eagle",color:"#DC143C"}',
    '{country:"Türkei",cc:"tr",shape:"moon",color:"#E30A17"}',
    '{country:"Ukraine",cc:"ua",shape:"trident",color:"#0057B8"}',
    '{country:"Schweden",cc:"se",shape:"crown",color:"#006AA7"}',
    '{country:"Norwegen",cc:"no",shape:"lion",color:"#EF2B2D"}',
    '{country:"Irland",cc:"ie",shape:"harp",color:"#009A44"}',
    '{country:"Griechenland",cc:"gr",shape:"cross",color:"#0D5EAF"}',
    '{country:"Nigeria",cc:"ng",shape:"eagle",color:"#008751"}',
    '{country:"Senegal",cc:"sn",shape:"star",color:"#009A44"}',
    '{country:"Kamerun",cc:"cm",shape:"lion",color:"#007A5E"}',
    '{country:"Ghana",cc:"gh",shape:"star",color:"#006B3F"}',
    '{country:"Ägypten",cc:"eg",shape:"eagle",color:"#CC1F1F"}',
    '{country:"Algerien",cc:"dz",shape:"moon",color:"#006233"}',
    '{country:"Marokko",cc:"ma",shape:"star",color:"#C1272D"}',
    '{country:"Tunesien",cc:"tn",shape:"moon",color:"#E70013"}',
    '{country:"Kolumbien",cc:"co",shape:"shield",color:"#FCD116"}',
    '{country:"Chile",cc:"cl",shape:"star",color:"#D52B1E"}',
    '{country:"Ecuador",cc:"ec",shape:"condor",color:"#FFD100"}',
    '{country:"Peru",cc:"pe",shape:"shield",color:"#D91023"}',
    '{country:"Katar",cc:"qa",shape:"shield",color:"#8D1B3D"}',
    '{country:"Saudi-Arabien",cc:"sa",shape:"palm",color:"#006C35"}',
    '{country:"Iran",cc:"ir",shape:"shield",color:"#239F40"}',
    '{country:"Serbien",cc:"rs",shape:"eagle",color:"#C6363C"}',
    '{country:"Tschechien",cc:"cz",shape:"lion",color:"#D7141A"}',
    '{country:"Ungarn",cc:"hu",shape:"shield",color:"#436F4D"}',
    '{country:"Rumänien",cc:"ro",shape:"eagle",color:"#002B7F"}',
    '{country:"Russland",cc:"ru",shape:"eagle",color:"#003153"}',
    '{country:"China",cc:"cn",shape:"shield",color:"#DE2910"}',
    '{country:"Südafrika",cc:"za",shape:"shield",color:"#007A4D"}',
]

old_crests = '''crests:[
    {country:"Deutschland",cc:"de",shape:"eagle",color:"#000000"},
    {country:"Frankreich",cc:"fr",shape:"rooster",color:"#003399"},
    {country:"England",cc:"gb",shape:"lion",color:"#CC0000"},
    {country:"Spanien",cc:"es",shape:"shield",color:"#CC0000"},
    {country:"Italien",cc:"it",shape:"shield",color:"#003399"},
    {country:"Brasilien",cc:"br",shape:"diamond",color:"#009C3B"},
    {country:"Argentinien",cc:"ar",shape:"sun",color:"#74ACDF"},
    {country:"Portugal",cc:"pt",shape:"cross",color:"#006600"},
    {country:"Niederlande",cc:"nl",shape:"lion",color:"#FF6600"},
    {country:"Kroatien",cc:"hr",shape:"checker",color:"#FF0000"},
  ],'''

new_crest_lines = [
    '    {country:"Deutschland",cc:"de",shape:"eagle",color:"#000000"},',
    '    {country:"Frankreich",cc:"fr",shape:"rooster",color:"#003399"},',
    '    {country:"England",cc:"gb",shape:"lion",color:"#CC0000"},',
    '    {country:"Spanien",cc:"es",shape:"shield",color:"#CC0000"},',
    '    {country:"Italien",cc:"it",shape:"shield",color:"#003399"},',
    '    {country:"Brasilien",cc:"br",shape:"diamond",color:"#009C3B"},',
    '    {country:"Argentinien",cc:"ar",shape:"sun",color:"#74ACDF"},',
    '    {country:"Portugal",cc:"pt",shape:"cross",color:"#006600"},',
    '    {country:"Niederlande",cc:"nl",shape:"lion",color:"#FF6600"},',
    '    {country:"Kroatien",cc:"hr",shape:"checker",color:"#FF0000"},',
]
for e in CREST_40_NEW:
    new_crest_lines.append(f'    {e},')

new_crests = 'crests:[\n' + '\n'.join(new_crest_lines) + '\n  ],'

if old_crests in content:
    content = content.replace(old_crests, new_crests)
    print(f'Crests expanded: 10 → {10 + len(CREST_40_NEW)} items')
else:
    print('ERROR: old_crests not found - check whitespace!')

# ══════════════════════════════════════════════════════════════
# STEP 4: Write back GeoQuest.html
# ══════════════════════════════════════════════════════════════
with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)
print('GeoQuest.html written.')

# ══════════════════════════════════════════════════════════════
# STEP 5: Update generate_spieluebersicht.py hardcodes
# ══════════════════════════════════════════════════════════════
with open(GEN_SUEBERSICHT, encoding='utf-8') as f:
    gs = f.read()

gs = gs.replace("'jersey':(15,'Trikots'),'crest':(10,'Wappen')",
                 "'jersey':(50,'Trikots'),'crest':(50,'Wappen')")
gs = gs.replace("return ('15 Trikots', 15) if key == 'jersey' else ('10 Wappen', 10)",
                 "return ('50 Trikots', 50) if key == 'jersey' else ('50 Wappen', 50)")

with open(GEN_SUEBERSICHT, 'w', encoding='utf-8') as f:
    f.write(gs)
print('generate_spieluebersicht.py updated: jersey=50, crest=50')
