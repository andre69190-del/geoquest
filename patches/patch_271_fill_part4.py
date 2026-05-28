#!/usr/bin/env python3
"""patch_271_fill_part4.py — Final micro-fill for last 11 under-50 arrays"""
import json, os

DATA = os.path.join(os.path.dirname(__file__), '..', 'data')

def load(fn):
    with open(os.path.join(DATA, fn), encoding='utf-8') as f:
        return json.load(f)

def save(fn, d):
    with open(os.path.join(DATA, fn), 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f'{fn}: saved')

def ext_m(d, k, new):
    v = d.get(k)
    if v is None: return
    if isinstance(v, dict) and 'items' in v: lst = v['items']
    elif isinstance(v, list): lst = v
    else: return
    existing = {x['n'] for x in lst}
    added = [x for x in new if x['n'] not in existing]
    lst.extend(added)
    print(f'  {k}: {len(lst)} items (+{len(added)})')

def ext_p(d, k, new):
    v = d.get(k)
    if v is None: return
    if isinstance(v, dict) and 'items' in v: lst = v['items']
    elif isinstance(v, list): lst = v
    else: return
    existing = {x['n'] for x in lst}
    added = [x for x in new if x['n'] not in existing]
    lst.extend(added)
    print(f'  {k}: {len(lst)} items (+{len(added)})')

# ── emob_match.json ───────────────────────────────────────────────────────────
print('\n=== emob_match.json ===')
d = load('emob_match.json')

ext_m(d, 'stecker', [
    {"n": "Wireless Charging Pad (15 kW)", "c": "Induktives Laden ohne Kabel"},
])

ext_m(d, 'port_position', [
    {"n": "MG ZS EV", "c": "Vorne links"},
    {"n": "BYD Atto 3", "c": "Vorne links"},
    {"n": "Ora Funky Cat", "c": "Hinten rechts"},
    {"n": "Xpeng G9", "c": "Hinten links"},
])

ext_m(d, 'startups_match', [
    {"n": "Volta Trucks", "c": "Schweden"},
    {"n": "Aiways", "c": "China"},
])

save('emob_match.json', d)

# ── emob_pin.json ─────────────────────────────────────────────────────────────
print('\n=== emob_pin.json ===')
d = load('emob_pin.json')

ext_p(d, 'ev_dichte_staedte', [
    {"n": "Shenzhen (China)", "lat": 22.54, "lng": 114.06},
    {"n": "Hangzhou (China)", "lat": 30.27, "lng": 120.15},
    {"n": "San Jose (Kalifornien, USA)", "lat": 37.34, "lng": -121.89},
    {"n": "Denver (Colorado, USA)", "lat": 39.74, "lng": -104.98},
    {"n": "Helsinki (Finnland)", "lat": 60.17, "lng": 24.94},
    {"n": "Göteborg (Schweden)", "lat": 57.71, "lng": 11.97},
])

save('emob_pin.json', d)

# ── pflanzen_match.json ───────────────────────────────────────────────────────
print('\n=== pflanzen_match.json ===')
d = load('pflanzen_match.json')

ext_m(d, 'scheinfruchte', [
    {"n": "Vogelbeere (Eberesche)", "c": "Sammelnussfrucht (Apfelfrucht)"},
    {"n": "Quitten", "c": "Apfelfrucht (Scheinfrucht)"},
    {"n": "Birne", "c": "Apfelfrucht (Scheinfrucht)"},
])

ext_m(d, 'vermehrung', [
    {"n": "Ableger (Layering)", "c": "Ast berührt Boden, bildet Wurzeln"},
])

ext_m(d, 'bluetezeit', [
    {"n": "Eibe (Taxus baccata)", "c": "Februar–März"},
])

ext_m(d, 'gewuerze', [
    {"n": "Malabar-Kardamom", "c": "Kerala, Indien"},
    {"n": "Langer Pfeffer (Piper longum)", "c": "Indien/Indonesien"},
])

save('pflanzen_match.json', d)

# ── archaeologie_match.json ───────────────────────────────────────────────────
print('\n=== archaeologie_match.json ===')
d = load('archaeologie_match.json')

ext_m(d, 'schriften', [
    {"n": "Byblos-Schrift", "c": "Libanon, ca. 2000 v. Chr., noch undeutbar"},
])

ext_m(d, 'goetter', [
    {"n": "Poseidon", "c": "Griechischer Meeresgott"},
    {"n": "Aphrodite", "c": "Griechische Göttin der Liebe"},
    {"n": "Xipe Totec", "c": "Aztekischer Gott der Erneuerung"},
])

ext_m(d, 'indus_tal', [
    {"n": "Chanhu-daro", "c": "Handwerkerzentrum der Induskultur"},
    {"n": "Kot Diji", "c": "Frühindus-Phase, Sindh (Pakistan)"},
    {"n": "Amri", "c": "Frühe Keramikkultur vor Indus-Zivilisation"},
    {"n": "Balakot", "c": "Küsten-Indus-Stätte in Baluchistan"},
    {"n": "Sutkagen-dor", "c": "Westlichste Indus-Fundstätte (Makran-Küste)"},
])

save('archaeologie_match.json', d)

print('\nPatch 271 fill part4 COMPLETE.')
