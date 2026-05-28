"""
patch_270b_kultur_fill2.py
Zweiter Pass: deltamuendungen, halbinseln, kaps, meerbusen, seen_match → alle auf 40+
"""
import json, os

DATA = os.path.join(os.path.dirname(__file__), '..', 'data', 'kultur.json')

def kext(lst, new_items, key='n'):
    seen = {it[key] for it in lst}
    added = 0
    for it in new_items:
        if it.get(key) not in seen:
            lst.append(it); seen.add(it[key]); added += 1
    return added

with open(DATA, encoding='utf-8') as f:
    data = json.load(f)

report = {}

# ── DELTAMUENDUNGEN  (30 → 42) ────────────────────────────────────────────
new_delta2 = [
    {"n": "Kafue-Delta",             "c": "Sambia"},
    {"n": "Senegal-Delta",           "c": "Senegal"},
    {"n": "Colorado-Delta",          "c": "Mexiko"},
    {"n": "Cauvery-Delta",           "c": "Indien"},
    {"n": "Krishna-Delta",           "c": "Indien"},
    {"n": "Godavari-Delta",          "c": "Indien"},
    {"n": "Mahanadi-Delta",          "c": "Indien"},
    {"n": "Brahmaputra-Delta",       "c": "Bangladesch"},
    {"n": "Kongo-Delta",             "c": "Demokratische Republik Kongo"},
    {"n": "Copper-River-Delta",      "c": "USA"},
    {"n": "Narmada-Delta",           "c": "Indien"},
    {"n": "Amu-Darya-Delta",         "c": "Usbekistan"},
]
report['deltamuendungen'] = kext(data['deltamuendungen'], new_delta2)

# ── HALBINSELN  (39 → 45) — ohne Duplikat-Varianten ──────────────────────
new_halb2 = [
    {"n": "Gallipoli-Halbinsel",     "c": "Türkei"},
    {"n": "Anatolische Halbinsel",   "c": "Türkei"},
    {"n": "Somali-Halbinsel",        "c": "Somalia"},
    {"n": "Halbinsel Kap York",      "c": "Australien"},
    {"n": "Halbinsel Eyre",          "c": "Australien"},
    {"n": "Halbinsel Banks",         "c": "Kanada"},
]
report['halbinseln'] = kext(data['halbinseln'], new_halb2)

# ── KAPS  (38 → 43) ───────────────────────────────────────────────────────
new_kaps2 = [
    {"n": "Kap Frio",                "c": "Namibia"},
    {"n": "Kap Columbine",           "c": "Südafrika"},
    {"n": "Kap Wrath",               "c": "Vereinigtes Königreich"},
    {"n": "Kap Hatteras",            "c": "USA"},
    {"n": "Kap San Lucas",           "c": "Mexiko"},
]
report['kaps'] = kext(data['kaps'], new_kaps2)

# ── MEERBUSEN  (37 → 43) ──────────────────────────────────────────────────
new_meer2 = [
    {"n": "Golf von Maine",          "c": "USA"},
    {"n": "Golf von Honduras",       "c": "Honduras"},
    {"n": "Golf von Panama",         "c": "Panama"},
    {"n": "Golf von Fonseca",        "c": "Honduras"},
    {"n": "Bucht von Manila",        "c": "Philippinen"},
    {"n": "Bucht von Halong",        "c": "Vietnam"},
]
report['meerbusen'] = kext(data['meerbusen'], new_meer2)

# ── SEEN_MATCH  (35 → 43) ─────────────────────────────────────────────────
new_seen2 = [
    {"n": "Nipigon-See",             "c": "Kanada"},
    {"n": "Huron-See",               "c": "Kanada"},
    {"n": "Tschadsee",               "c": "Tschad"},
    {"n": "Poopo-See",               "c": "Bolivien"},
    {"n": "Vanern",                  "c": "Schweden"},
    {"n": "Vattern",                 "c": "Schweden"},
    {"n": "Siljan",                  "c": "Schweden"},
    {"n": "Inari-See",               "c": "Finnland"},
]
report['seen_match'] = kext(data['seen_match'], new_seen2)

# ── Save ──────────────────────────────────────────────────────────────────
with open(DATA, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("patch_270b — Ergebnis:")
for key, added in sorted(report.items()):
    total = len(data[key])
    status = "✅" if total >= 40 else "⚠️ noch unter 40"
    print(f"  {key:25s}: +{added} → {total} Items  {status}")
