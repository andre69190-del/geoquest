#!/usr/bin/env python3
"""
Phase 258: Pferde-Erweiterung & Offline-Feedback-Queue
=======================================================
JSON-Dateien:
  - tiere_pin.json  : +pferde_rassen (26 Items — fixiert defekten uk_pferde_rassen-Modus)
  - tiere_hl.json   : +pferde_speed (15 Items), +pferde_gewicht (17 Items)
  - tiere_match.json: +reitsport_disziplinen (20 Items, 5 Kategorien)
  - tiere_ws.json   : +hufeisen (Python-validierte Wortliste)

gen.py-Patches:
  PA: 4 neue MODES nach ws_pferde_fluesterer
  PB: 4 neue GEN-Dispatch-Einträge
  PC: MODE_CATS tiere — 4 neue IDs anhängen
  PD: openFeedback() — Offline-Queue (navigator.onLine guard)
  PE: syncOfflineData() — Feedback-Queue beim Reconnect hochladen
"""

import json, pathlib, sys
from collections import Counter

BASE = pathlib.Path("/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest")
GEN  = BASE / "gen.py"

# ── Hilfsfunktionen ────────────────────────────────────────────────────────────
def jload(p): return json.loads(p.read_text(encoding="utf-8"))
def jsave(p, d): p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

patches_applied = []
def patch_gen(old, new, label):
    global content
    if old not in content:
        print(f"[SKIP] {label} — Anker nicht gefunden!")
        return False
    n = content.count(old)
    if n > 1:
        print(f"[WARN] {label} — {n}x gefunden, ersetze nur erste Stelle")
    content = content.replace(old, new, 1)
    patches_applied.append(label)
    print(f"[OK]   {label}")
    return True

# ══════════════════════════════════════════════════════════════════════════════
# SCHRITT 1: HUFEISEN Wortlisten — Python-Validator
# ══════════════════════════════════════════════════════════════════════════════
MASTER = "HUFEISEN"   # H×1 U×1 F×1 E×2 I×1 S×1 N×1

def can_form(word, source=MASTER):
    s = Counter(source)
    for c in word.upper():
        if s[c] <= 0:
            return False
        s[c] -= 1
    return True

DE_WORDS = [
    "HUFE","HUFEN",                         # Huf, Plural
    "FEIN","FEINE","FEINS","FEINES",        # Adjektiv + Flexion
    "SEIN","SEINE","SEINS",                 # Verb/Pronomen (SEINS: S,E,I,N,S → 2×S ✗!)
    "EINE","EINES","EINS",                  # Artikel/Zahl
    "SEIFE",                                # Soap — S,E,I,F,E (beide E)
    "SENF",                                 # Mustard
    "FIES","FIESE",                         # mean
    "NIES",                                 # Sneeze (imperative)
    "HEIN",                                 # Ausruf / Vorname
]
# SEINS braucht S×2 — entfernen
DE_WORDS = [w for w in DE_WORDS if can_form(w)]

EN_WORDS = [
    "FINE","FINES",         # gut / Geldstrafe
    "FUSE","INFUSE",        # Sicherung / einflößen
    "HUES",                 # Farbtöne
    "SHIN","SHINE",         # Schienbein / scheinen
    "SHEEN",                # Glanz (S,H,E,E,N — beide E)
    "FENS","HENS",          # Sumpf / Hennen
    "SINE",                 # Sinus (trig.)
    "HIES",                 # 3. Pers. Sg. "to hie"
    "SEIF",                 # Seif-Düne (Wüste)
    "NEIFS",                # Plural "neif" (hist. Leibeigene)
]
EN_WORDS = [w for w in EN_WORDS if can_form(w)]

print(f"HUFEISEN DE-Wörter ({len(DE_WORDS)}): {DE_WORDS}")
print(f"HUFEISEN EN-Wörter ({len(EN_WORDS)}): {EN_WORDS}")
assert len(DE_WORDS) >= 10, "Zu wenige DE-Wörter!"
assert len(EN_WORDS) >= 3,  "Zu wenige EN-Wörter!"

# ══════════════════════════════════════════════════════════════════════════════
# SCHRITT 2: JSON-Dateien erweitern
# ══════════════════════════════════════════════════════════════════════════════

# ── 2a: tiere_pin.json → pferde_rassen ──────────────────────────────────────
pin_path = BASE / "data/tiere_pin.json"
pin_data = jload(pin_path)
assert "pferde_rassen" not in pin_data, "pferde_rassen existiert bereits!"

pin_data["pferde_rassen"] = {
    "prompt": "Wo liegt der historische Ursprung oder das Hauptzuchtgebiet dieser Pferderasse?",
    "prompt_en": "Where is the historical origin or main breeding region of this horse breed?",
    "items": [
        # Europa
        {"n": "Islandpferd",           "lat": 64.13,  "lng": -21.95},
        {"n": "Andalusier (PRE)",       "lat": 37.39,  "lng":  -5.99},
        {"n": "Haflinger",              "lat": 46.67,  "lng":  11.36},
        {"n": "Lipizzaner",             "lat": 45.53,  "lng":  13.95},
        {"n": "Friese",                 "lat": 53.10,  "lng":   5.80},
        {"n": "Trakehner",              "lat": 54.60,  "lng":  21.00},
        {"n": "Hannoveraner",           "lat": 52.37,  "lng":   9.73},
        {"n": "Oldenburger",            "lat": 53.14,  "lng":   8.21},
        {"n": "Shetlandpony",           "lat": 60.15,  "lng":  -1.18},
        {"n": "Welsh Mountain Pony",    "lat": 52.13,  "lng":  -3.78},
        {"n": "Connemara-Pony",         "lat": 53.45,  "lng": -10.00},
        {"n": "Camargue-Pferd",         "lat": 43.52,  "lng":   4.48},
        {"n": "Percheron",              "lat": 48.20,  "lng":   0.40},
        {"n": "Lusitano",               "lat": 39.55,  "lng":  -8.00},
        {"n": "Noriker",                "lat": 47.05,  "lng":  13.48},
        {"n": "Fjordpferd",             "lat": 61.18,  "lng":   6.10},
        # Naher Osten / Asien / Afrika
        {"n": "Arabisches Vollblut",    "lat": 24.00,  "lng":  45.00},
        {"n": "Akhal-Teke",             "lat": 37.93,  "lng":  58.38},
        {"n": "Przewalski-Pferd",       "lat": 47.90,  "lng": 106.91},
        {"n": "Berber-Pferd",           "lat": 33.00,  "lng":  -5.00},
        # Amerika
        {"n": "Mustang",                "lat": 39.80,  "lng": -98.60},
        {"n": "Quarter Horse",          "lat": 32.00,  "lng": -97.00},
        {"n": "Appaloosa",              "lat": 46.40,  "lng":-116.90},
        {"n": "Paint Horse",            "lat": 35.47,  "lng": -97.51},
        {"n": "Criollo",                "lat":-34.61,  "lng": -58.39},
        {"n": "Englisches Vollblut",    "lat": 52.00,  "lng":  -1.00},
    ]
}
jsave(pin_path, pin_data)
print(f"[OK] tiere_pin.json: pferde_rassen ({len(pin_data['pferde_rassen']['items'])} Items)")

# ── 2b: tiere_hl.json → pferde_speed + pferde_gewicht ───────────────────────
hl_path = BASE / "data/tiere_hl.json"
hl_data = jload(hl_path)
assert "pferde_speed"   not in hl_data, "pferde_speed existiert bereits!"
assert "pferde_gewicht" not in hl_data, "pferde_gewicht existiert bereits!"

hl_data["pferde_speed"] = {
    "prompt": "Welches Pferd / welche Equide ist im Galopp schneller?",
    "prompt_en": "Which horse or equid is faster at a gallop?",
    "unit": "km/h",
    "items": [
        # Quellen: FEI, American Quarter Horse Association, Wildlife docs
        {"name": "Quarter Horse (¼-Meile Sprint)",  "val": 88.0},
        {"name": "Englisches Vollblut (GWR 2008)",  "val": 70.8},
        {"name": "Arabisches Vollblut",             "val": 65.0},
        {"name": "Grevy-Zebra",                     "val": 64.0},
        {"name": "Steppenzebra",                    "val": 56.0},
        {"name": "Przewalski-Pferd",                "val": 56.0},
        {"name": "Mustang",                         "val": 55.0},
        {"name": "Appaloosa",                       "val": 55.0},
        {"name": "Afrikanischer Wildesel",          "val": 50.0},
        {"name": "Islandpferd",                     "val": 48.0},
        {"name": "Haflinger",                       "val": 45.0},
        {"name": "Fjordpferd",                      "val": 40.0},
        {"name": "Shetlandpony",                    "val": 35.0},
        {"name": "Shire Horse",                     "val": 30.0},
        {"name": "Falabella",                       "val": 20.0},
    ]
}

hl_data["pferde_gewicht"] = {
    "prompt": "Welches Pferd ist im Durchschnitt schwerer?",
    "prompt_en": "Which horse is heavier on average?",
    "unit": "kg",
    "items": [
        {"name": "Shire Horse",              "val": 1100},
        {"name": "Belgisches Kaltblut",      "val": 1000},
        {"name": "Clydesdale",               "val":  900},
        {"name": "Percheron",                "val":  850},
        {"name": "Noriker",                  "val":  750},
        {"name": "Friese",                   "val":  650},
        {"name": "Haflinger",                "val":  550},
        {"name": "Lusitano",                 "val":  520},
        {"name": "Trakehner",                "val":  500},
        {"name": "Appaloosa",                "val":  510},
        {"name": "Arabisches Vollblut",      "val":  440},
        {"name": "Islandpferd",              "val":  380},
        {"name": "Przewalski-Pferd",         "val":  300},
        {"name": "Welsh Mountain Pony",      "val":  200},
        {"name": "Connemara-Pony",           "val":  280},
        {"name": "Shetlandpony",             "val":  180},
        {"name": "Falabella",                "val":   60},
    ]
}
jsave(hl_path, hl_data)
print(f"[OK] tiere_hl.json: pferde_speed ({len(hl_data['pferde_speed']['items'])}), "
      f"pferde_gewicht ({len(hl_data['pferde_gewicht']['items'])})")

# ── 2c: tiere_match.json → reitsport_disziplinen ────────────────────────────
match_path = BASE / "data/tiere_match.json"
match_data = jload(match_path)
assert "reitsport_disziplinen" not in match_data, "reitsport_disziplinen existiert bereits!"

match_data["reitsport_disziplinen"] = {
    "prompt": "Zu welcher Reitdisziplin gehört dieser Begriff oder diese Gangart?",
    "prompt_en": "Which equestrian discipline does this term or gait belong to?",
    "items": [
        # Islandpferdereiten (4 Items)
        {"n": "Tölt",             "c": "Islandpferdereiten"},
        {"n": "Pass",             "c": "Islandpferdereiten"},
        {"n": "Rennpass",         "c": "Islandpferdereiten"},
        {"n": "Fünfgang",         "c": "Islandpferdereiten"},
        # Klassische Dressur (4 Items)
        {"n": "Piaffe",           "c": "Klassische Dressur"},
        {"n": "Passage",          "c": "Klassische Dressur"},
        {"n": "Pirouette",        "c": "Klassische Dressur"},
        {"n": "Levade",           "c": "Klassische Dressur"},
        # Westernreiten (4 Items)
        {"n": "Reining",          "c": "Westernreiten"},
        {"n": "Cutting",          "c": "Westernreiten"},
        {"n": "Barrel Racing",    "c": "Westernreiten"},
        {"n": "Trail",            "c": "Westernreiten"},
        # Springreiten (4 Items)
        {"n": "Oxer",             "c": "Springreiten"},
        {"n": "In-and-Out",       "c": "Springreiten"},
        {"n": "Wassergraben",     "c": "Springreiten"},
        {"n": "Kombination",      "c": "Springreiten"},
        # Voltigieren (4 Items)
        {"n": "Pflichtprogramm",  "c": "Voltigieren"},
        {"n": "Kür",              "c": "Voltigieren"},
        {"n": "Pas de Deux",      "c": "Voltigieren"},
        {"n": "Gruppenvoltigieren","c": "Voltigieren"},
    ]
}
jsave(match_path, match_data)
print(f"[OK] tiere_match.json: reitsport_disziplinen ({len(match_data['reitsport_disziplinen']['items'])} Items, 5 Kategorien)")

# ── 2d: tiere_ws.json → hufeisen ────────────────────────────────────────────
ws_path = BASE / "data/tiere_ws.json"
ws_data = jload(ws_path)
assert "hufeisen" not in ws_data, "hufeisen existiert bereits!"

ws_data["hufeisen"] = {
    "word": "HUFEISEN",
    "validWords": {
        "de": DE_WORDS,
        "en": EN_WORDS
    }
}
jsave(ws_path, ws_data)
print(f"[OK] tiere_ws.json: hufeisen (DE={len(DE_WORDS)}, EN={len(EN_WORDS)})")

# ══════════════════════════════════════════════════════════════════════════════
# SCHRITT 3: gen.py patchen
# ══════════════════════════════════════════════════════════════════════════════
content = GEN.read_text(encoding="utf-8")
original = content

# ── PA: 4 neue MODES nach ws_pferde_fluesterer ───────────────────────────────
patch_gen(
    '{id:"ws_pferde_fluesterer",icon:"\\u{1F40E}",title:"WS: Pferdeüsterer",group:"tiere",noMultiplayer:true,prompt:"Bilde Wörter aus SHIREHORSE!",desc:"Anagramm-Rätsel — 10 Buchstaben"}',
    '{id:"ws_pferde_fluesterer",icon:"\\u{1F40E}",title:"WS: Pferdeflüsterer",group:"tiere",noMultiplayer:true,prompt:"Bilde Wörter aus SHIREHORSE!",desc:"Anagramm-Rätsel — 10 Buchstaben"},\n'
    '    {id:"hl_pferde_speed",icon:"\\u{1F40E}",title:"H/L Galopp-Speed",group:"tiere",prompt:"Welches Pferd ist schneller?",desc:"Von Falabella bis Quarter Horse — Galoppgeschwindigkeiten im Vergleich"},\n'
    '    {id:"hl_pferde_gewicht",icon:"\\u{2696}\\u{FE0F}",title:"H/L Körpergewicht",group:"tiere",prompt:"Welches Pferd ist schwerer?",desc:"60 kg Falabella bis 1100 kg Shire Horse"},\n'
    '    {id:"uk_pferde_reitsport",icon:"\\u{1F3C7}",title:"Reitsport-Disziplinen",group:"tiere",prompt:"Zu welcher Disziplin gehört dieser Begriff?",desc:"Tölt, Piaffe, Reining, Oxer — 5 Disziplinen"},\n'
    '    {id:"ws_pferde_hufeisen",icon:"\\u{1F40E}",title:"WS: Hufeisen",group:"tiere",noMultiplayer:true,prompt:"Bilde Wörter aus HUFEISEN!",desc:"8 Buchstaben — von SEIN bis SEIFE"}',
    "PA: 4 neue MODES (hl_pferde_speed/gewicht, uk_pferde_reitsport, ws_pferde_hufeisen)"
)

# ── PB: GEN-Dispatch nach ws_pferde_fluesterer ───────────────────────────────
patch_gen(
    'ws_pferde_fluesterer:()=>{initTierWortSchmiede("pferde_fluesterer");return null;}',
    'ws_pferde_fluesterer:()=>{initTierWortSchmiede("pferde_fluesterer");return null;},\n'
    '  hl_pferde_speed:()=>genTiereHL("pferde_speed"),\n'
    '  hl_pferde_gewicht:()=>genTiereHL("pferde_gewicht"),\n'
    '  uk_pferde_reitsport:()=>genTiereMatchQ("reitsport_disziplinen"),\n'
    '  ws_pferde_hufeisen:()=>{initTierWortSchmiede("hufeisen");return null;}',
    "PB: GEN-Dispatch für 4 neue Modi"
)

# ── PC: MODE_CATS tiere — 4 IDs am Ende des Pferde-Blocks anhängen ───────────
patch_gen(
    '"uk_pferde_rassen","uk_pferde_fachbegriffe","hl_pferde_stockmass","ws_pferde_fluesterer"',
    '"uk_pferde_rassen","uk_pferde_fachbegriffe","hl_pferde_stockmass","ws_pferde_fluesterer","hl_pferde_speed","hl_pferde_gewicht","uk_pferde_reitsport","ws_pferde_hufeisen"',
    "PC: MODE_CATS tiere — 4 neue IDs"
)

# ── PD: openFeedback() — Offline-Queue + app_version auf 258 ─────────────────
patch_gen(
    "    var _payload={category:_cat,message:_txt,mode:S.mode||null,lang:S.language||'de',app_version:'256',username:(typeof sbProfile!=='undefined'&&sbProfile&&sbProfile.username?sbProfile.username:null)};\n"
    "    if(typeof sbOK!=='undefined'&&sbOK&&typeof sb!=='undefined'&&sb){\n"
    "      var _uid=(typeof sbUser!=='undefined'&&sbUser&&sbUser.id)?sbUser.id:null;\n"
    "      if(_uid)_payload.user_id=_uid;\n"
    "      sb.from('feedback').insert(_payload).then(function(){showToast('\\u2705 Danke f\\u00fcr dein Feedback!');},function(e){console.warn('Feedback-Supabase-Fehler:',e);_sendFeedbackMail(_cat,_txt,_mn);});\n"
    "    }else{_sendFeedbackMail(_cat,_txt,_mn);}",

    "    var _payload={category:_cat,message:_txt,mode:S.mode||null,lang:S.language||'de',app_version:'258',username:(typeof sbProfile!=='undefined'&&sbProfile&&sbProfile.username?sbProfile.username:null)};\n"
    "    /* Phase 258: Offline-Queue */\n"
    "    if(!navigator.onLine){\n"
    "      var _oq=JSON.parse(localStorage.getItem('gq_offline_feedback')||'[]');\n"
    "      _oq.push(_payload);\n"
    "      localStorage.setItem('gq_offline_feedback',JSON.stringify(_oq));\n"
    "      showToast('\\u{1F4E5} Offline gespeichert \\u2014 wird beim n\\u00e4chsten Start gesendet');\n"
    "    }else if(typeof sbOK!=='undefined'&&sbOK&&typeof sb!=='undefined'&&sb){\n"
    "      var _uid=(typeof sbUser!=='undefined'&&sbUser&&sbUser.id)?sbUser.id:null;\n"
    "      if(_uid)_payload.user_id=_uid;\n"
    "      sb.from('feedback').insert(_payload).then(function(){showToast('\\u2705 Danke f\\u00fcr dein Feedback! \\u2764\\uFE0F');},function(e){console.warn('Feedback-Supabase-Fehler:',e);_sendFeedbackMail(_cat,_txt,_mn);});\n"
    "    }else{_sendFeedbackMail(_cat,_txt,_mn);}",
    "PD: openFeedback() Offline-Queue + app_version 258"
)

# ── PE: syncOfflineData() — Feedback-Queue nach Score-Sync hochladen ─────────
patch_gen(
    "    showToast('\\u2705 Offline-Ergebnisse synchronisiert!');\n"
    "    render();\n"
    "  }catch(_se){\n"
    "    console.warn('syncOfflineData failed',_se);\n"
    "  }\n"
    "}",

    "    showToast('\\u2705 Offline-Ergebnisse synchronisiert!');\n"
    "    render();\n"
    "  }catch(_se){\n"
    "    console.warn('syncOfflineData failed',_se);\n"
    "  }\n"
    "  /* Phase 258: Offline-Feedback-Queue hochladen */\n"
    "  try{\n"
    "    const _fbRaw=localStorage.getItem('gq_offline_feedback');\n"
    "    if(_fbRaw&&sb&&sbUser?.id){\n"
    "      const _fbQ=JSON.parse(_fbRaw);\n"
    "      if(_fbQ.length>0){\n"
    "        for(const _fb of _fbQ){if(!_fb.user_id)_fb.user_id=sbUser.id;}\n"
    "        await sb.from('feedback').insert(_fbQ);\n"
    "        localStorage.removeItem('gq_offline_feedback');\n"
    "        showToast('\\u2705 '+_fbQ.length+' Offline-Feedback \\u00fcbermittelt!');\n"
    "      }\n"
    "    }\n"
    "  }catch(_fe){console.warn('Feedback-sync failed',_fe);}\n"
    "}",
    "PE: syncOfflineData() Feedback-Queue"
)

# ── Summary ───────────────────────────────────────────────────────────────────
if content == original:
    print("\n[ERROR] Keine einzige gen.py-Änderung angewendet!")
    sys.exit(1)

GEN.write_text(content, encoding="utf-8")
print(f"\n✅ {len(patches_applied)} gen.py-Patches: {', '.join(patches_applied)}")
print("✅ 4 JSON-Dateien aktualisiert")
print("\nNächster Schritt: python3 verify.py")
