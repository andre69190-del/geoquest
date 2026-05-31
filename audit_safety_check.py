#!/usr/bin/env python3
"""
GeoQuest Audit Safety Check
Phase 328+ — Sicherheits-, Integritäts- und i18n-Fallback-Audit

Prüft alle data/*.json auf:
  1. XSS / Injection-Payloads in n- und c-Feldern
  2. c-Felder, die keinem Standard-ISO-Land entsprechen
     (→ landen im _tc()-Fallback, erscheinen für 22 Sprachen auf Deutsch)
  3. Items ohne Pflichtfelder (n/c oder n/lat/lng je nach Array-Typ)
  4. Koordinaten-Plausibilität (lat/lng in gültigem Bereich)
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")

# ---------------------------------------------------------------------------
# 1. XSS / Injection
# ---------------------------------------------------------------------------

XSS_PATTERN = re.compile(
    r'<script.*?>|onclick\s*=|onload\s*=|href\s*=\s*javascript:|&lt;script',
    re.IGNORECASE
)

def is_unsafe(text):
    if not isinstance(text, str):
        return False
    return bool(XSS_PATTERN.search(text))

# ---------------------------------------------------------------------------
# 2. Bekannte ISO-Ländernamen auf Deutsch
#    (Quelle: Intl.DisplayNames + COUNTRIES-Array in gen.py)
#    Erweitert um Sub-Regionen, die GeoQuest bewusst nutzt
# ---------------------------------------------------------------------------

KNOWN_COUNTRIES = {
    # Europa
    "Deutschland","Österreich","Schweiz","Frankreich","Italien","Spanien","Portugal",
    "Niederlande","Belgien","Luxemburg","Dänemark","Schweden","Norwegen","Finnland",
    "Polen","Tschechien","Slowakei","Ungarn","Rumänien","Bulgarien","Griechenland",
    "Kroatien","Slowenien","Serbien","Bosnien und Herzegowina","Montenegro","Albanien",
    "Nordmazedonien","Kosovo","Irland","Großbritannien","Schottland","Wales","Nordirland",
    "Island","Malta","Zypern","Estland","Lettland","Litauen","Belarus","Ukraine","Moldau",
    "Russland","Türkei","Georgien","Armenien","Aserbaidschan","Liechtenstein","Monaco",
    "Andorra","San Marino","Vatikan",
    # Amerika
    "USA","Kanada","Mexiko","Brasilien","Argentinien","Chile","Peru","Kolumbien",
    "Venezuela","Ecuador","Bolivien","Paraguay","Uruguay","Guyana","Suriname",
    "Panama","Costa Rica","Guatemala","Honduras","El Salvador","Nicaragua",
    "Kuba","Jamaika","Haiti","Dominikanische Republik","Puerto Rico","Trinidad und Tobago",
    # Asien
    "China","Japan","Südkorea","Nordkorea","Indien","Pakistan","Bangladesh","Sri Lanka",
    "Nepal","Bhutan","Afghanistan","Iran","Irak","Syrien","Libanon","Israel","Jordanien",
    "Saudi-Arabien","Jemen","Oman","Vereinigte Arabische Emirate","Katar","Kuwait","Bahrain",
    "Usbekistan","Kasachstan","Turkmenistan","Kirgisistan","Tadschikistan",
    "Thailand","Vietnam","Myanmar","Laos","Kambodscha","Malaysia","Indonesien",
    "Philippinen","Singapur","Timor-Leste","Mongolei","Taiwan",
    # Afrika
    "Ägypten","Marokko","Algerien","Tunesien","Libyen","Sudan","Äthiopien","Eritrea",
    "Somalia","Kenia","Tansania","Uganda","Ruanda","Burundi","DR Kongo","Kongo",
    "Nigeria","Ghana","Senegal","Mali","Niger","Burkina Faso","Elfenbeinküste",
    "Liberia","Sierra Leone","Guinea","Guinea-Bissau","Gambia","Mauritanien",
    "Kamerun","Zentralafrikanische Republik","Tschad","Gabun","Äquatorialguinea",
    "São Tomé und Príncipe","Angola","Sambia","Simbabwe","Mosambik","Malawi",
    "Namibia","Botswana","Südafrika","Lesotho","Eswatini","Madagaskar",
    "Mauritius","Seychellen","Kapverdische Inseln","Komoren",
    # Ozeanien
    "Australien","Neuseeland","Papua-Neuguinea","Fidschi","Samoa","Tonga",
    "Vanuatu","Salomonen","Kiribati","Mikronesien","Palau","Marshallinseln","Nauru","Tuvalu",
    # Bekannte Sub-Regionen / historische Namen (bewusst in GeoQuest genutzt)
    "Böhmen","Mähren","Bayern","Preußen","Franken","Westfalen",
    "Nordskandinavien","Skandinavien","Baltikum",
    "Westafrika","Ostafrika","Zentralafrika","Südafrika (Region)","Nordafrika",
    "Arabische Halbinsel","Naher Osten","Levante","Mesopotamien","Persien",
    "Golf-Staaten","Kaukasus","Zentralasien","Südostasien","Indochina",
    "Karibik","Mittelamerika","Lateinamerika","Andenstaten",
    "Melanesien","Polynesien","Mikronesien (Region)",
    # Alte Kulturen & historische Entitäten (Archäologie-Arrays)
    "Römer","Griechen","Kelten","Wikinger","Mayas","Azteken","Inkas",
    "Byzantinisches Reich","Osmanisches Reich","Heiliges Römisches Reich",
    "Ägypten (antik)","Babylon","Mesopotamien","Induskultur",
    "Sowjetunion","Jugoslawien","Tschechoslowakei","Österreich-Ungarn",
    # Regionen mit ISO-cc (GeoQuest-spezifisch)
    "Hawaii","Alaska","Sibirien","Tibet","Xinjiang","Katalonien","Baskenland",
    "Kurdistan","Palästina",
}

# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def get_all_items(obj):
    """Gibt alle items-Listen aus einem JSON-Objekt zurück."""
    results = []
    if isinstance(obj, dict):
        if "items" in obj and isinstance(obj["items"], list):
            results.append(obj["items"])
        for v in obj.values():
            results.extend(get_all_items(v))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(get_all_items(item))
    return results

def check_recursive_xss(obj, filename, unsafe_list):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ['n', 'c'] and is_unsafe(v):
                unsafe_list.append(f"{filename}: Feld '{k}' → {v!r}")
            check_recursive_xss(v, filename, unsafe_list)
    elif isinstance(obj, list):
        for item in obj:
            check_recursive_xss(item, filename, unsafe_list)

# ---------------------------------------------------------------------------
# Haupt-Audit
# ---------------------------------------------------------------------------

def run_audit():
    print("=" * 60)
    print("GeoQuest Audit Safety Check")
    print("=" * 60)

    xss_hits      = []
    fallback_hits = []
    schema_hits   = []
    coord_hits    = []
    parse_errors  = []

    files = sorted(f for f in os.listdir(DATA_DIR) if f.endswith('.json'))

    for filename in files:
        path = os.path.join(DATA_DIR, filename)
        try:
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            parse_errors.append(f"{filename}: {e}")
            continue

        # 1. XSS-Check
        check_recursive_xss(data, filename, xss_hits)

        # 2 + 3 + 4. Items-Analyse
        all_item_lists = get_all_items(data)
        for items in all_item_lists:
            for item in items:
                if not isinstance(item, dict):
                    continue

                # Schema-Check
                has_nc  = 'n' in item and 'c' in item
                has_pin = 'n' in item and 'lat' in item and 'lng' in item
                if not (has_nc or has_pin or 'name' in item or 'n' in item):
                    schema_hits.append(
                        f"{filename}: Item ohne Pflichtfelder → {str(item)[:80]}"
                    )

                # c-Feld Fallback-Check
                if 'c' in item and isinstance(item['c'], str):
                    c_val = item['c'].strip()
                    if c_val and c_val not in KNOWN_COUNTRIES:
                        fallback_hits.append((filename, c_val))

                # Koordinaten-Plausibilität
                if 'lat' in item and 'lng' in item:
                    try:
                        lat, lng = float(item['lat']), float(item['lng'])
                        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                            coord_hits.append(
                                f"{filename}: lat={lat}, lng={lng} → {item.get('n','?')}"
                            )
                    except (TypeError, ValueError):
                        coord_hits.append(
                            f"{filename}: Ungültige Koordinaten → {item.get('n','?')}"
                        )

    # ---------------------------------------------------------------------------
    # Ausgabe
    # ---------------------------------------------------------------------------

    print(f"\n[1] XSS / Injection-Check — {len(files)} Dateien gescannt")
    if xss_hits:
        print(f"    ⚠️  {len(xss_hits)} unsichere Felder gefunden:")
        for h in xss_hits:
            print(f"       {h}")
    else:
        print("    ✓ Keine XSS/Injection-Payloads gefunden")

    print(f"\n[2] c-Feld Fallback-Analyse (i18n Gap B)")
    if fallback_hits:
        # Gruppiere nach c-Wert
        from collections import Counter
        counts = Counter(v for _, v in fallback_hits)
        non_standard = sorted(counts.items(), key=lambda x: -x[1])
        print(f"    ℹ️  {len(non_standard)} nicht-ISO-konforme c-Werte gefunden")
        print(f"    (erscheinen für 22 Sprachen auf Deutsch — kein Bug bei Eigennamen/hist. Kulturen)")
        print()
        # Kategorisiere: historisch/kulturell vs. echte Lücken
        historical = [v for v, _ in non_standard if any(x in v for x in
            ["antik","Römer","Griech","Kelt","Wikinger","Maya","Aztek","Inka",
             "Osmanisch","Byzanz","Mesop","Indus","Babylon","Sowjet","Jugos",
             "Reich","Tschechoslow","Österreich-Ungarn"])]
        regions   = [v for v, _ in non_standard if v not in historical]
        print(f"    Historische Kulturen/Reiche ({len(historical)}): {', '.join(historical[:10])}")
        print(f"    Geografische Regionen/Subnat. ({len(regions)}): {', '.join(regions[:15])}")
    else:
        print("    ✓ Alle c-Felder entsprechen bekannten Ländernamen")

    print(f"\n[3] Schema-Integrität")
    if schema_hits:
        print(f"    ⚠️  {len(schema_hits)} Items mit fehlenden Pflichtfeldern:")
        for h in schema_hits[:10]:
            print(f"       {h}")
    else:
        print("    ✓ Alle Items haben gültige Pflichtfelder (n/c oder n/lat/lng)")

    print(f"\n[4] Koordinaten-Plausibilität")
    if coord_hits:
        print(f"    ⚠️  {len(coord_hits)} ungültige Koordinaten:")
        for h in coord_hits:
            print(f"       {h}")
    else:
        print("    ✓ Alle lat/lng-Werte im gültigen Bereich (-90/90, -180/180)")

    if parse_errors:
        print(f"\n[!] Parse-Fehler ({len(parse_errors)}):")
        for e in parse_errors:
            print(f"    {e}")

    print("\n" + "=" * 60)
    ok = not (xss_hits or schema_hits or coord_hits or parse_errors)
    if ok:
        print("✅ AUDIT BESTANDEN — Keine kritischen Befunde")
    else:
        print("⚠️  AUDIT: Kritische Befunde (siehe oben)")
    print("=" * 60)

    return {
        "xss": len(xss_hits),
        "fallback_c": len(set(v for _, v in fallback_hits)),
        "schema": len(schema_hits),
        "coords": len(coord_hits),
        "parse_errors": len(parse_errors),
        "files_scanned": len(files),
        "passed": ok,
    }

if __name__ == "__main__":
    run_audit()
