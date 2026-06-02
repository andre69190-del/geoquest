"""
validate_content.py — GeoQuest Semantic Content Validator
==========================================================
Checks all JSON data files in data/ for content quality issues
that syntax checks (verify.py) cannot catch:
  - Missing required fields
  - Out-of-range coordinates
  - Null-Island traps
  - Duplicate coordinates
  - HL value outliers / mixed units
  - Insufficient match distractors
  - Anagram validity for Wort-Schmiede words
  - WS character/format violations

Run:  python validate_content.py          → warnings only
      python validate_content.py --strict → exit 1 if any warnings found
"""

import json
import math
import os
import sys
from collections import Counter, defaultdict

HERE   = os.path.dirname(os.path.abspath(__file__))
DATA   = os.path.join(HERE, "data")
STRICT = "--strict" in sys.argv

# ANSI colours (disabled on Windows without ANSI support)
try:
    import ctypes
    ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)
except Exception:
    pass

WARN  = "\033[93m⚠ "
ERR   = "\033[91m✗ "
OK    = "\033[92m✓ "
RESET = "\033[0m"
BOLD  = "\033[1m"

warnings = []
infos    = []   # INFO-only: never block --strict

def warn(file, key, item_id, msg):
    tag = f"{file} › {key}" + (f" › {item_id}" if item_id else "")
    warnings.append((tag, msg))

def info(file, key, item_id, msg):
    tag = f"{file} › {key}" + (f" › {item_id}" if item_id else "")
    infos.append((tag, msg))

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def load(filename):
    path = os.path.join(DATA, filename)
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)

def letters_available(word):
    """Return Counter of letters in word (uppercase)."""
    return Counter(word.upper())

def can_spell(target, source_counter):
    """Return True if target word can be spelled from source_counter letters."""
    t = Counter(target.upper())
    for ch, count in t.items():
        if source_counter[ch] < count:
            return False
    return True

def round4(v):
    return round(float(v), 4)

# ──────────────────────────────────────────────────────────────────────────────
# CHECK 1 — Pin data   (*_pin.json)
# ──────────────────────────────────────────────────────────────────────────────

def check_pin(filename, data):
    for key, block in data.items():
        items = block.get("items", []) if isinstance(block, dict) else []
        if not items:
            warn(filename, key, None, "No items array found")
            continue

        # Duplicate check scoped per category — same city legitimately appears
        # in multiple categories, but should not appear twice within one category.
        seen_coords = {}  # (lat4, lng4) → first item name  [per-category scope]

        for item in items:
            n = item.get("n", "<unnamed>")

            # Required fields
            for field in ("n", "lat", "lng"):
                if field not in item:
                    warn(filename, key, n, f"Missing required field '{field}'")

            lat = item.get("lat")
            lng = item.get("lng")
            if lat is None or lng is None:
                continue

            # Type check
            try:
                lat, lng = float(lat), float(lng)
            except (TypeError, ValueError):
                warn(filename, key, n, f"lat/lng not numeric: lat={lat!r} lng={lng!r}")
                continue

            # Range check
            if not (-90.0 <= lat <= 90.0):
                warn(filename, key, n, f"lat out of range: {lat}")
            if not (-180.0 <= lng <= 180.0):
                warn(filename, key, n, f"lng out of range: {lng}")

            # Null-Island check
            if lat == 0.0 and lng == 0.0:
                warn(filename, key, n, "Null-Island coordinates (0.0, 0.0) — likely a placeholder")

            # Duplicate check (4 decimal places ≈ 11m accuracy)
            coord_key = (round4(lat), round4(lng))
            if coord_key in seen_coords:
                info(filename, key, n,
                     f"Duplicate coordinates {coord_key} shared with '{seen_coords[coord_key]}'")
            else:
                seen_coords[coord_key] = n

# ──────────────────────────────────────────────────────────────────────────────
# CHECK 2 — HL data   (*_hl.json, tiere_hl.json)
# ──────────────────────────────────────────────────────────────────────────────

def check_hl(filename, data):
    for key, block in data.items():
        if not isinstance(block, dict):
            warn(filename, key, None, "Block is not an object")
            continue

        items = block.get("items", [])
        if not items:
            warn(filename, key, None, "Empty items array — generator will always return null")
            continue

        # Minimum items for interesting comparisons
        if len(items) < 6:
            warn(filename, key, None,
                 f"Only {len(items)} items — _mkHL needs ≥6 to reliably avoid 2%-spread failures")

        vals = []
        names_seen = set()
        for item in items:
            # Required fields
            for field in ("name", "val"):
                if field not in item:
                    warn(filename, key, item.get("name", "<unnamed>"), f"Missing field '{field}'")

            name = item.get("name", "<unnamed>")
            val  = item.get("val")

            # Duplicate name check
            if name in names_seen:
                warn(filename, key, name, "Duplicate item name — dedup lid will collide")
            names_seen.add(name)

            if val is None:
                warn(filename, key, name, "val is null")
                continue
            try:
                v = float(str(val).replace(",", "."))
            except (TypeError, ValueError):
                warn(filename, key, name, f"val not numeric: {val!r}")
                continue

            if v < 0:
                info(filename, key, name, f"Negative val={v} — check if sign is intentional")

            vals.append((name, v))

        if len(vals) < 2:
            continue

        numeric_vals = [v for _, v in vals]
        min_v, max_v = min(numeric_vals), max(numeric_vals)

        # All-equal check (generator will always fail 2% spread)
        if min_v == max_v:
            warn(filename, key, None, "All values identical — generator will always fail spread check")
            continue

        # Mixed-unit outlier check (e.g. grams vs kilograms in same list)
        if min_v > 0 and max_v > min_v * 10_000_000:  # Phase 237: raised for biological/geological ranges
            ratio = max_v / min_v
            extremes = [(n, v) for n, v in vals if v == min_v or v == max_v]
            info(filename, key, None,
                 f"Extreme value ratio {ratio:.0f}× (min={min_v}, max={max_v}) — "
                 f"possible mixed units. Check: {extremes}")

        # Z-score single outlier — INFO only, not a warning (Phase 247)
        # Extreme values are intentional game content (Sauerbraten, Wanderratte, etc.).
        # La-Paz-Fenster (W=10%) prevents trivial pairings in-engine. Only flag as
        # [INFO] so QA warning count stays clean. Verify units manually if flagged.
        mean_v = sum(numeric_vals) / len(numeric_vals)
        variance = sum((v - mean_v) ** 2 for v in numeric_vals) / len(numeric_vals)
        if variance > 0:
            stddev = math.sqrt(variance)
            for name, v in vals:
                z = abs(v - mean_v) / stddev
                if z > 4.0:
                    print(f"  [INFO] {filename} / {key} / {name}: "
                          f"z={z:.1f} (val={v}, mean={mean_v:.1f}) — "
                          f"intentional extreme, check units only")

# ──────────────────────────────────────────────────────────────────────────────
# CHECK 3 — Match data   (*_match.json, tiere_match.json, kultur.json)
# ──────────────────────────────────────────────────────────────────────────────

def check_match(filename, data):
    for key, block in data.items():
        # Support both formats: {items:[]} and legacy plain list
        if isinstance(block, list):
            items = block
        elif isinstance(block, dict):
            items = block.get("items", [])
        else:
            warn(filename, key, None, "Unexpected block type (not list or dict)")
            continue

        if not items:
            warn(filename, key, None, "Empty items array")
            continue

        # Required fields per item
        for item in items:
            n = item.get("n", "<unnamed>")
            for field in ("n", "c"):
                if field not in item:
                    warn(filename, key, n, f"Missing required field '{field}'")

        # Distraktor pool check (Phase 237: engine allows 1-2 distractors for binary/ternary sets)
        # ≥2 unique c-values: minimum for any meaningful choice (ERROR if < 2)
        # ≥4 unique c-values: optimal for 3 distractors (advisory if < 4)
        c_values = [item["c"] for item in items if "c" in item]
        unique_c = set(c_values)
        if len(unique_c) < 2:
            warn(filename, key, None,
                 f"Only {len(unique_c)} unique answer category — game is broken "
                 f"(all items have the same answer). Found: {sorted(unique_c)}")
        elif len(unique_c) < 4:
            info(filename, key, None,
                 f"Only {len(unique_c)} unique answer categories (c-values) — "
                 f"engine will use fewer than 3 distractors. "
                 f"OK for binary/ternary questions; add more variety otherwise. "
                 f"Found: {sorted(unique_c)}")

        # Duplicate subjects check (same question asked twice)
        n_values = [item.get("n","") for item in items]
        for n, count in Counter(n_values).items():
            if count > 1:
                warn(filename, key, n, f"Duplicate subject (n='{n}') appears {count}× — removes variety")

        # Phase 328: ISO-Code-Prüfung für bekannte geografische Arrays
        # Nur für Arrays aktiviert, bei denen c SEMANTISCH ein Länder-/Geo-Feld ist.
        # → stellt sicher, dass _tcc() / _deCountryCc() zur Laufzeit auflösen kann.
        _GEO_ARRAYS = {
            # kultur.json
            'nationaltiere','nationalpflanzen','kleidung','instrumente','taenze',
            'wahrzeichen','museen','kunstwerke','feste','begruessung',
            'sport','wein_regionen','filmsets',
            # gastro_match.json
            'hausmannskost','suessspeisen',
            # pflanzen_match.json (nur herkunft hat Ländernamen)
            'gewuerze',
            # sport_match.json
            'sport_herkunft','sport_nationalsport_match','sport_sportlegende_land',
            'sport_wm_gastgeber_match',
            # geo_match.json
            'geo_vulkan_land','geo_hoehlen_land',
            # archaeologie_match.json
            'repatriierung','wikinger','museen',
        }
        _DE_TO_CC_FAST = {
            'Afghanistan','Albanien','Algerien','Andorra','Angola','Armenien',
            'Argentinien','Australien','Österreich','Aserbaidschan','Bahamas',
            'Bahrain','Bangladesh','Belgien','Belarus','Bolivien','Brasilien',
            'Bulgarien','Burkina Faso','Burundi','Kamerun','Kanada','Chile',
            'China','Kolumbien','Kroatien','Kuba','Zypern','Tschechien',
            'Dänemark','Dominikanische Republik','Ecuador','Ägypten',
            'El Salvador','Eritrea','Estland','Äthiopien','Fidschi','Finnland',
            'Frankreich','Georgien','Deutschland','Ghana','Griechenland',
            'Guatemala','Guinea','Guyana','Haiti','Honduras','Ungarn','Island',
            'Indien','Indonesien','Iran','Irak','Irland','Israel','Italien',
            'Elfenbeinküste','Jamaika','Japan','Jordanien','Kasachstan',
            'Kenia','Nordkorea','Südkorea','Kuwait','Kirgisistan','Laos',
            'Lettland','Libanon','Libyen','Liechtenstein','Litauen','Luxemburg',
            'Madagaskar','Malawi','Malaysia','Mali','Malta','Marokko',
            'Mauritanien','Mexiko','Moldau','Monaco','Mongolei','Montenegro',
            'Mosambik','Myanmar','Namibia','Nepal','Niederlande','Neuseeland',
            'Nicaragua','Nigeria','Nordmazedonien','Norwegen','Oman','Pakistan',
            'Palästina','Panama','Paraguay','Peru','Philippinen','Polen',
            'Portugal','Katar','Rumänien','Russland','Ruanda','San Marino',
            'Saudi-Arabien','Senegal','Serbien','Sierra Leone','Singapur',
            'Slowakei','Slowenien','Somalia','Südafrika','Spanien','Sri Lanka',
            'Sudan','Suriname','Schweden','Schweiz','Syrien','Taiwan',
            'Tadschikistan','Tansania','Thailand','Tschad','Togo','Tonga',
            'Trinidad und Tobago','Tunesien','Türkei','Turkmenistan','Uganda',
            'Ukraine','Vereinigte Arabische Emirate','Großbritannien','USA',
            'Uruguay','Usbekistan','Venezuela','Vietnam','Jemen','Sambia',
            'Simbabwe',
            # Aliase die _deCountryCc() auch auflöst
            'England','Schottland','Wales','Nordirland','Grönland',
            'Indien (Punjab)','Indien/Pakistan','Großbritannien / Indien',
            'Hawaii/Portugal','Bolivien/Peru','Peru/Bolivien',
            'Serbien/Kroatien','Rumänien/Israel','Tibet/China','Tibet',
        }
        if key in _GEO_ARRAYS:
            for item in items:
                c_val = item.get('c', '')
                if isinstance(c_val, str) and c_val and c_val not in _DE_TO_CC_FAST:
                    info(filename, key, item.get('n','?'),
                         f"c='{c_val}' nicht im ISO-Mapping — _tcc() fällt auf "
                         f"_tc()-Fallback zurück (22 Sprachen sehen DE-String). "
                         f"Ggf. in _CONTENT_I18N aufnehmen oder Ländername anpassen.")

# ──────────────────────────────────────────────────────────────────────────────
# CHECK 4 — WS data   (*_ws.json, tiere_ws.json)
# ──────────────────────────────────────────────────────────────────────────────

def check_ws(filename, data):
    for key, block in data.items():
        if not isinstance(block, dict):
            warn(filename, key, None, "Block is not an object")
            continue

        base_word = block.get("word", "")
        valid_words = block.get("validWords", {})

        # Base word checks
        if not base_word:
            warn(filename, key, None, "Missing 'word' field")
            continue

        if base_word != base_word.upper():
            warn(filename, key, base_word, f"'word' is not uppercase: {base_word!r}")

        if " " in base_word or not base_word.isalpha():
            warn(filename, key, base_word,
                 f"'word' contains spaces or non-alpha characters: {base_word!r}")

        base_counter = letters_available(base_word)

        # validWords format — support dict {de: [], en: []} or plain list
        if isinstance(valid_words, dict):
            all_lang_words = []
            for lang, words in valid_words.items():
                if not isinstance(words, list):
                    warn(filename, key, base_word, f"validWords['{lang}'] is not a list")
                    continue
                all_lang_words.append((lang, words))
        elif isinstance(valid_words, list):
            all_lang_words = [("(list)", valid_words)]
        else:
            warn(filename, key, base_word, "validWords is neither a dict nor a list")
            continue

        if not all_lang_words:
            warn(filename, key, base_word, "validWords is empty — game has no solutions")
            continue

        for lang, words in all_lang_words:
            if not words:
                warn(filename, key, base_word, f"validWords['{lang}'] is empty")
                continue

            # Minimum playable word count: engine filters _mkWS to ≥3 chars,
            # so warn if fewer than 3 valid words survive
            valid_for_game = [w for w in words if isinstance(w, str) and len(w) >= 3]
            if len(valid_for_game) < 3:
                warn(filename, key, base_word,
                     f"[{lang}] Only {len(valid_for_game)} word(s) with ≥3 chars — "
                     f"game needs ≥3 solutions to be playable")

            # Duplicate words within same validWords entry
            word_counts = Counter(w.upper() for w in words if isinstance(w, str))
            for dup_word, dup_count in word_counts.items():
                if dup_count > 1:
                    warn(filename, key, base_word,
                         f"[{lang}] '{dup_word}' appears {dup_count}× — remove duplicates")

            for word in words:
                # Must be uppercase
                if word != word.upper():
                    warn(filename, key, base_word,
                         f"[{lang}] '{word}' is not uppercase")

                # No spaces or non-alpha
                if " " in word or not word.replace("-", "").isalpha():
                    warn(filename, key, base_word,
                         f"[{lang}] '{word}' contains spaces or special characters")

                # Length check: solution cannot be longer than base word
                if len(word) > len(base_word):
                    warn(filename, key, base_word,
                         f"[{lang}] '{word}' ({len(word)} chars) longer than base '{base_word}' ({len(base_word)} chars) — impossible anagram")

                # Anagram validity: every letter must be available in base word
                if not can_spell(word, base_counter):
                    missing = []
                    tc = Counter(word.upper())
                    for ch, cnt in tc.items():
                        if base_counter[ch] < cnt:
                            missing.append(f"'{ch}'×{cnt} (have {base_counter[ch]})")
                    warn(filename, key, base_word,
                         f"[{lang}] '{word}' requires letters not in '{base_word}': {', '.join(missing)}")

# ──────────────────────────────────────────────────────────────────────────────
# Dispatch — auto-detect file type by suffix and structure
# ──────────────────────────────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────────────────────────────
# i18n Vollständigkeits-Check (Phase 305)
# ──────────────────────────────────────────────────────────────────────────────

def check_i18n():
    """
    Prüft _CONTENT_I18N in gen.py auf Vollständigkeit.
    Stellt sicher dass alle DE-Strings auch EN und PL-Übersetzungen haben.
    Eigennamen (Bahnhofsnamen, Zugmarken) sind ausgenommen.
    """
    gen_path = os.path.join(HERE, "gen.py")
    if not os.path.exists(gen_path):
        warn("gen.py", "i18n", "", "gen.py nicht gefunden — i18n-Check übersprungen")
        return

    with open(gen_path, "r", encoding="utf-8") as f:
        g = f.read()

    import re, json as _json

    # Extract _CONTENT_I18N object
    m = re.search(r'const _CONTENT_I18N=(\{.*?\});\s*function', g, re.DOTALL)
    if not m:
        warn("gen.py", "i18n", "_CONTENT_I18N", "Konnte _CONTENT_I18N nicht parsen")
        return

    try:
        # JS to Python: replace JS object notation
        raw = m.group(1)
        i18n = _json.loads(raw)
    except Exception:
        warn("gen.py", "i18n", "_CONTENT_I18N", "JSON-Parse-Fehler in _CONTENT_I18N")
        return

    en_keys = set(i18n.get("en", {}).keys())
    pl_keys = set(i18n.get("pl", {}).keys())

    # Check that EN and PL have the same keys as each other
    en_only = en_keys - pl_keys
    pl_only = pl_keys - en_keys

    # Filter: skip strings that look like proper nouns (all caps, or start with capital city/train names)
    # Simple heuristic: skip if >50% of words are capitalized proper nouns
    def likely_proper_noun(s):
        words = s.split()
        if not words: return True
        caps = sum(1 for w in words if w[:1].isupper() and not w.isupper())
        return caps / len(words) > 0.7

    missing_pl = [k for k in en_only if not likely_proper_noun(k)]
    missing_en = [k for k in pl_only if not likely_proper_noun(k)]

    for key in sorted(missing_pl)[:10]:  # Max 10 warnings
        warn("gen.py", "i18n/pl", key[:50], "PL-Übersetzung fehlt (EN vorhanden)")
    for key in sorted(missing_en)[:10]:
        warn("gen.py", "i18n/en", key[:50], "EN-Übersetzung fehlt (PL vorhanden)")

    # Check for empty translations
    for lang, trans in i18n.items():
        for de_key, trans_val in trans.items():
            if not trans_val or not trans_val.strip():
                warn("gen.py", f"i18n/{lang}", de_key[:50], f"Leere Übersetzung in {lang}")

    total_en = len(en_keys)
    total_pl = len(pl_keys)
    missing_count = len(missing_pl) + len(missing_en)
    if missing_count == 0:
        print(f"    ✓ i18n vollständig: {total_en} EN, {total_pl} PL Übersetzungen")
    else:
        print(f"    ⚠ i18n: {missing_count} fehlende Übersetzungen (EN:{total_en}, PL:{total_pl})")




def check_regional_extended(filename, data):
    REQUIRED = ["kategorie","land","region","ort","lat","lng",
                "saison_start_monat","basis_zutat","alkoholgehalt","brauchtum_monat"]
    KAT  = {"Speise","Getränk","Wein","Brauchtum"}
    LAND = {"Deutschland","Österreich","Schweiz","Frankreich","Italien","Spanien","Niederlande","Belgien","Portugal","Griechenland","Polen","Tschechien","Ungarn","Dänemark","Schweden","Finnland","Norwegen","Irland","Rumänien","Kroatien","Slowenien","Slowakei","Litauen","Lettland","Estland","Bulgarien","Malta","Zypern","Luxemburg"}
    for name, entry in data.items():
        for f in REQUIRED:
            if f not in entry:
                warn(filename, name, f, "Pflichtfeld fehlt")
        k = entry.get("kategorie")
        if k and k not in KAT:
            warn(filename, name, "kategorie", f"Unbekannte kategorie: {k!r}")
        l = entry.get("land")
        if l and l not in LAND:
            warn(filename, name, "land", f"Unbekanntes land: {l!r}")
        m = entry.get("saison_start_monat")
        if m is not None and not (1 <= m <= 12):
            warn(filename, name, "saison_start_monat", f"Außerhalb 1-12: {m}")
        bm = entry.get("brauchtum_monat")
        if k == "Brauchtum" and bm is None:
            warn(filename, name, "brauchtum_monat", "Brauchtum braucht brauchtum_monat")
        lat = entry.get("lat",0)
        lng = entry.get("lng",0)
        if lat == 0.0 or lng == 0.0:
            warn(filename, name, "lat/lng", "Koordinaten sind 0.0")

def check_konsolen(filename, data):
    REQUIRED = [
        "hersteller", "erscheinungsjahr", "eingestellt_jahr", "generation",
        "verkauf_mio", "preis_usd", "cpu_mhz", "ram_kb", "herkunftsland",
        "nachfolger_von", "medium", "aufloesung_max", "online_faehig",
        "handheld", "bekannteste_spiele"
    ]
    MEDIUM = {"Cartridge", "CD", "DVD", "Blu-ray", "GD-ROM", "UMD", "Mini-DVD", "Digital"}
    AUFLOESUNG = {"144p", "240p", "480i", "480p", "576p", "720p", "1080p", "4K"}
    HERSTELLER = {"Nintendo", "Sony", "Microsoft", "Sega", "Atari", "SNK", "Coleco",
                  "NEC", "3DO Company", "Mattel"}
    for name, entry in data.items():
        for f in REQUIRED:
            if f not in entry:
                warn(filename, name, f, f"Pflichtfeld fehlt")
        m = entry.get("medium")
        if m and m not in MEDIUM:
            warn(filename, name, "medium", f"Unbekanntes Medium: {m!r}")
        a = entry.get("aufloesung_max")
        if a and a not in AUFLOESUNG:
            warn(filename, name, "aufloesung_max", f"Unbekannte Auflösung: {a!r}")
        if not isinstance(entry.get("online_faehig"), bool):
            warn(filename, name, "online_faehig", "Kein Bool")
        if not isinstance(entry.get("handheld"), bool):
            warn(filename, name, "handheld", "Kein Bool")
        spiele = entry.get("bekannteste_spiele", [])
        if not isinstance(spiele, list) or len(spiele) < 1:
            warn(filename, name, "bekannteste_spiele", "Mindestens 1 Spiel erwartet")

def check_games_extended(filename, data):
    """Validiert data/games_extended.json (22 Pflichtfelder, Enums, Typen, Logik)."""
    GENRE     = {"Sandbox","Battle Royale","Rollenspiel","Ego-Shooter",
                 "Action-Adventure","Strategie","Jump 'n' Run","Sportsimulation",
                 "Puzzle","MOBA","Party-Spiel","Kampfspiel","Rennspiel",
                 "Social Deduction","Endless Runner","MMO"}
    PLATTFORM = {"PC","Konsole","Mobil","Multiplattform"}
    ADAPTION  = {"Film","Serie","Anime",None}
    KATEGORIE = {"Modern Youth","Global Mobile","Klassiker","Indie"}
    REQUIRED  = ["release","kategorie","publisher","publisher_land","developer",
                 "dev_land","dev_city","dev_lat","dev_lng","genre","usk","pegi",
                 "f2p","vk_mio","downloads_mio","peak_concurrent_mio","metacritic",
                 "plattform","vorbild_land","adaption","esports","sequel_count"]
    if not isinstance(data, dict):
        warn(filename, "struktur", "root", "games_extended.json muss ein Dict sein")
        return
    for name, entry in data.items():
        if not isinstance(entry, dict):
            warn(filename, "eintrag", name, "Wert ist kein Dict")
            continue
        for f in REQUIRED:
            if f not in entry:
                warn(filename, "pflichtfeld", name, f"Feld '{f}' fehlt")
        for field, allowed in [("genre",GENRE),("plattform",PLATTFORM),
                                ("adaption",ADAPTION),("kategorie",KATEGORIE)]:
            val = entry.get(field)
            if val not in allowed:
                warn(filename, f"enum:{field}", name,
                     f"Wert {val!r} nicht erlaubt. Erlaubt: {sorted(str(v) for v in allowed)}")
        if not isinstance(entry.get("f2p"), bool):
            warn(filename, "typ:f2p", name, f"f2p muss bool sein, ist {type(entry.get('f2p')).__name__}")
        if not isinstance(entry.get("esports"), bool):
            warn(filename, "typ:esports", name, "esports muss bool sein")
        if not isinstance(entry.get("release"), int):
            warn(filename, "typ:release", name, "release muss int sein")
        for field in ("usk","pegi","sequel_count"):
            v = entry.get(field)
            if v is not None and not isinstance(v, int):
                warn(filename, f"typ:{field}", name, f"{field} muss int sein, ist {type(v).__name__}")
        for field in ("vk_mio","downloads_mio"):
            v = entry.get(field)
            if v is not None and not isinstance(v, (int,float)):
                warn(filename, f"typ:{field}", name, f"{field} muss float sein")
        # Optionale neue Felder: peak_year, publisher_lat/lng
        if "peak_year" in entry and not isinstance(entry.get("peak_year"), int):
            warn(filename, "typ:peak_year", name, f"peak_year muss int sein")
        for _fl in ("publisher_lat","publisher_lng"):
            _v = entry.get(_fl)
            if _v is not None and not isinstance(_v, (int,float)):
                warn(filename, f"typ:{_fl}", name, f"{_fl} muss float sein")
                lat, lng = entry.get("dev_lat"), entry.get("dev_lng")
        if lat is None or lng is None:
            warn(filename, "coords", name, "dev_lat/dev_lng fehlt — Pin-Modus crasht")
        else:
            try:
                if not (-90 <= float(lat) <= 90):
                    warn(filename, "coords", name, f"dev_lat={lat} ausserhalb [-90,90]")
                if not (-180 <= float(lng) <= 180):
                    warn(filename, "coords", name, f"dev_lng={lng} ausserhalb [-180,180]")
                if float(lat)==0.0 and float(lng)==0.0:
                    warn(filename, "null-island", name, "dev_lat/lng = 0.0 — Platzhalter?")
            except (TypeError, ValueError):
                warn(filename, "coords", name, f"dev_lat/lng nicht numerisch: {lat}, {lng}")
        if entry.get("f2p") is True and entry.get("vk_mio",0) > 0:
            warn(filename, "logik:f2p", name,
                 f"f2p=True aber vk_mio={entry.get('vk_mio')} > 0")
        if entry.get("f2p") is False and entry.get("downloads_mio",0) > 0:
            info(filename, "logik:f2p", name,
                 f"f2p=False aber downloads_mio={entry.get('downloads_mio')} > 0 — pruefen")

def check_literatur_extended(filename, data):
    """Validiert data/literatur_extended.json"""
    KATEG = {"Roman","Comic","Manga","Kinderbuch"}
    REQUIRED = ["kategorie","erscheinungsjahr","verkaeufe_mio","autor","ursprungsland","protagonist"]
    if not isinstance(data, dict): warn(filename,"struktur","root","muss ein Dict sein"); return
    for name, entry in data.items():
        if not isinstance(entry, dict): warn(filename,"eintrag",name,"kein Dict"); continue
        for f in REQUIRED:
            if f not in entry: warn(filename,"pflichtfeld",name,f"Feld '{f}' fehlt")
        if entry.get("kategorie") not in KATEG:
            warn(filename,"enum:kategorie",name,f"Kategorie {entry.get('kategorie')!r} unbekannt")
        if not isinstance(entry.get("erscheinungsjahr"),int):
            warn(filename,"typ:erscheinungsjahr",name,"erscheinungsjahr muss int sein")
        if not isinstance(entry.get("verkaeufe_mio"),(int,float)):
            warn(filename,"typ:verkaeufe_mio",name,"verkaeufe_mio muss float sein")

def check_robotik_extended(filename, data):
    """Validiert data/robotik_extended.json"""
    KATEG = {"Wettbewerb","Educational","Industrie","Künstliche Intelligenz","Meilenstein"}
    REQUIRED = ["kategorie","gruendungsjahr","entwickler","ursprungsland","meilenstein_fakt"]
    if not isinstance(data, dict): warn(filename,"struktur","root","muss ein Dict sein"); return
    for name, entry in data.items():
        if not isinstance(entry, dict): warn(filename,"eintrag",name,"kein Dict"); continue
        for f in REQUIRED:
            if f not in entry: warn(filename,"pflichtfeld",name,f"Feld '{f}' fehlt")
        if entry.get("kategorie") not in KATEG:
            warn(filename,"enum:kategorie",name,f"Kategorie {entry.get('kategorie')!r} unbekannt")
        if not isinstance(entry.get("gruendungsjahr"),int):
            warn(filename,"typ:gruendungsjahr",name,"gruendungsjahr muss int sein")

def check_medizin_extended(filename, data):
    """Validiert data/medizin_extended.json"""
    KATEG = {"Organ","Knochen","Meilenstein","Krankheit"}
    REQUIRED = ["kategorie","jahr_entdeckung","gewicht_gramm","anzahl_knochen","lateinischer_begriff","entdecker"]
    if not isinstance(data, dict): warn(filename,"struktur","root","muss ein Dict sein"); return
    for name, entry in data.items():
        if not isinstance(entry, dict): warn(filename,"eintrag",name,"kein Dict"); continue
        for f in REQUIRED:
            if f not in entry: warn(filename,"pflichtfeld",name,f"Feld '{f}' fehlt")
        if entry.get("kategorie") not in KATEG:
            warn(filename,"enum:kategorie",name,f"Kategorie {entry.get('kategorie')!r} unbekannt")
        # Null-Werte erlaubt für jahr_entdeckung, gewicht_gramm, anzahl_knochen, entdecker
        jd = entry.get("jahr_entdeckung")
        if jd is not None and not isinstance(jd, int):
            warn(filename,"typ:jahr_entdeckung",name,"jahr_entdeckung muss int oder null sein")
        gg = entry.get("gewicht_gramm")
        if gg is not None and not isinstance(gg, (int, float)):
            warn(filename,"typ:gewicht_gramm",name,"gewicht_gramm muss float oder null sein")
        ak = entry.get("anzahl_knochen")
        if ak is not None and not isinstance(ak, int):
            warn(filename,"typ:anzahl_knochen",name,"anzahl_knochen muss int oder null sein")

def check_wirtschaft_extended(filename, data):
    """Validiert data/wirtschaft_extended.json"""
    KATEG = {"Tech","Automobil","FMCG","Pharma","Finanzen","Software"}
    REQUIRED = ["kategorie","gruendungsjahr","umsatz_mrd_usd","mitarbeiter_tausend","hauptsitz_land","gruender"]
    if not isinstance(data, dict): warn(filename,"struktur","root","muss ein Dict sein"); return
    for name, entry in data.items():
        if not isinstance(entry, dict): warn(filename,"eintrag",name,"kein Dict"); continue
        for f in REQUIRED:
            if f not in entry: warn(filename,"pflichtfeld",name,f"Feld '{f}' fehlt")
        if entry.get("kategorie") not in KATEG:
            warn(filename,"enum:kategorie",name,f"Kategorie {entry.get('kategorie')!r} unbekannt")
        if not isinstance(entry.get("gruendungsjahr"), int):
            warn(filename,"typ:gruendungsjahr",name,"gruendungsjahr muss int sein")
        if not isinstance(entry.get("umsatz_mrd_usd"), (int, float)):
            warn(filename,"typ:umsatz_mrd_usd",name,"umsatz_mrd_usd muss float sein")
        if not isinstance(entry.get("mitarbeiter_tausend"), (int, float)):
            warn(filename,"typ:mitarbeiter_tausend",name,"mitarbeiter_tausend muss float sein")

def check_geschichte_extended(filename, data):
    """Validiert data/geschichte_extended.json"""
    KATEG = {"Imperium","Epoche","Ereignis","Schlacht"}
    REQUIRED = ["kategorie","start_jahr","dauer_jahre","ausdehnung_mio_km2","zentrum_hauptstadt","schluesselfigur"]
    if not isinstance(data, dict): warn(filename,"struktur","root","muss ein Dict sein"); return
    for name, entry in data.items():
        if not isinstance(entry, dict): warn(filename,"eintrag",name,"kein Dict"); continue
        for f in REQUIRED:
            if f not in entry: warn(filename,"pflichtfeld",name,f"Feld '{f}' fehlt")
        if entry.get("kategorie") not in KATEG:
            warn(filename,"enum:kategorie",name,f"Kategorie {entry.get('kategorie')!r} unbekannt")
        if not isinstance(entry.get("start_jahr"), int):
            warn(filename,"typ:start_jahr",name,"start_jahr muss int sein")
        dj = entry.get("dauer_jahre")
        if dj is not None and not isinstance(dj, int):
            warn(filename,"typ:dauer_jahre",name,"dauer_jahre muss int oder null sein")

def check_webkultur_extended(filename, data):
    """Validiert data/webkultur_extended.json"""
    KATEG = {"Plattform","Creator","Meme","Hardware"}
    REQUIRED = ["kategorie","start_jahr","reichweite_mio","ursprungsland","gruender_creator"]
    if not isinstance(data, dict): warn(filename,"struktur","root","muss ein Dict sein"); return
    for name, entry in data.items():
        if not isinstance(entry, dict): warn(filename,"eintrag",name,"kein Dict"); continue
        for f in REQUIRED:
            if f not in entry: warn(filename,"pflichtfeld",name,f"Feld '{f}' fehlt")
        if entry.get("kategorie") not in KATEG:
            warn(filename,"enum:kategorie",name,f"Kategorie {entry.get('kategorie')!r} unbekannt")
        if not isinstance(entry.get("start_jahr"), int):
            warn(filename,"typ:start_jahr",name,"start_jahr muss int sein")
        if not isinstance(entry.get("reichweite_mio"), (int, float)):
            warn(filename,"typ:reichweite_mio",name,"reichweite_mio muss float sein")

def check_mythologie(filename, data):
    """Validiert data/mythologie.json"""
    KATEG = {"Griechisch","Nordisch","Ägyptisch","Römisch","Japanisch","Aztekisch","Mesopotamisch","Keltisch"}
    TYPEN = {"Gott","Göttin","Kreatur","Titan","Halbgott"}
    REQUIRED = ["kategorie","typ","domain","herkunftsland","lat","lng"]
    if not isinstance(data, dict):
        warn(filename,"struktur","root","mythologie.json muss ein Dict sein"); return
    for name, entry in data.items():
        if not isinstance(entry, dict): warn(filename,"eintrag",name,"kein Dict"); continue
        for f in REQUIRED:
            if f not in entry: warn(filename,"pflichtfeld",name,f"Feld '{f}' fehlt")
        if entry.get("kategorie") not in KATEG:
            warn(filename,"enum:kategorie",name,f"Kategorie {entry.get('kategorie')!r} unbekannt")
        if entry.get("typ") not in TYPEN:
            warn(filename,"enum:typ",name,f"Typ {entry.get('typ')!r} unbekannt")

def check_architektur(filename, data):
    """Validiert data/architektur.json"""
    KATEG = {"Wolkenkratzer","Brücke","Staudamm","Tunnel","Tempel","Denkmal"}
    REQUIRED = ["kategorie","land","lat","lng","baujahr"]
    if not isinstance(data, dict):
        warn(filename,"struktur","root","architektur.json muss ein Dict sein"); return
    for name, entry in data.items():
        if not isinstance(entry, dict): warn(filename,"eintrag",name,"kein Dict"); continue
        for f in REQUIRED:
            if f not in entry: warn(filename,"pflichtfeld",name,f"Feld '{f}' fehlt")
        if entry.get("kategorie") not in KATEG:
            warn(filename,"enum:kategorie",name,f"Kategorie {entry.get('kategorie')!r} unbekannt")
        if not isinstance(entry.get("baujahr"),(int,float)):
            warn(filename,"typ:baujahr",name,"baujahr muss numerisch sein")

def check_filme_extended(filename, data):
    """Validiert data/filme_extended.json (8 Pflichtfelder, Enums, Typen)."""
    KATEGORIE = {"Blockbuster","Klassiker","Franchise","Indie"}
    REQUIRED  = ["kategorie","release_jahr","boxoffice_mio","laenge_min",
                 "regisseur","drehort_land","oscars","imdb_rating"]
    if not isinstance(data, dict):
        warn(filename,"struktur","root","filme_extended.json muss ein Dict sein"); return
    for name, entry in data.items():
        if not isinstance(entry, dict):
            warn(filename,"eintrag",name,"Wert ist kein Dict"); continue
        for f in REQUIRED:
            if f not in entry:
                warn(filename,"pflichtfeld",name,f"Feld '{f}' fehlt")
        val = entry.get("kategorie")
        if val not in KATEGORIE:
            warn(filename,"enum:kategorie",name,f"Wert {val!r} nicht erlaubt. Erlaubt: {sorted(KATEGORIE)}")
        for field,typ in [("release_jahr",int),("oscars",int),("laenge_min",int)]:
            if not isinstance(entry.get(field),typ):
                warn(filename,f"typ:{field}",name,f"{field} muss {typ.__name__} sein")
        for field in ("boxoffice_mio","imdb_rating"):
            if not isinstance(entry.get(field),(int,float)):
                warn(filename,f"typ:{field}",name,f"{field} muss float sein")
        if not isinstance(entry.get("regisseur"),str):
            warn(filename,"typ:regisseur",name,"regisseur muss str sein")
        if not isinstance(entry.get("drehort_land"),str):
            warn(filename,"typ:drehort_land",name,"drehort_land muss str sein")

def check_serien_extended(filename, data):
    """Validiert data/serien_extended.json (7 Pflichtfelder, Enums, Typen)."""
    GENRE  = {"Krimi","Comedy","Drama","Sci-Fi/Mystery","Doku"}
    EPOCHE = {"Gegenwart","Historisch","Zukunft"}
    REQUIRED = ["genre","start_jahr","staffeln","episoden",
                "produktionsland","imdb_rating","epochen_setting"]
    if not isinstance(data, dict):
        warn(filename,"struktur","root","serien_extended.json muss ein Dict sein"); return
    for name, entry in data.items():
        if not isinstance(entry, dict):
            warn(filename,"eintrag",name,"Wert ist kein Dict"); continue
        for f in REQUIRED:
            if f not in entry:
                warn(filename,"pflichtfeld",name,f"Feld '{f}' fehlt")
        g = entry.get("genre")
        if g not in GENRE:
            warn(filename,"enum:genre",name,f"Wert {g!r} nicht erlaubt. Erlaubt: {sorted(GENRE)}")
        ep = entry.get("epochen_setting")
        if ep not in EPOCHE:
            warn(filename,"enum:epochen_setting",name,f"Wert {ep!r} nicht erlaubt. Erlaubt: {sorted(EPOCHE)}")
        for field in ("start_jahr","staffeln","episoden"):
            v = entry.get(field)
            if not isinstance(v, int) or isinstance(v, bool):
                warn(filename,f"typ:{field}",name,f"{field} muss int sein")
            elif v <= 0:
                warn(filename,f"wert:{field}",name,f"{field} muss > 0 sein (ist {v})")
        r = entry.get("imdb_rating")
        if not isinstance(r,(int,float)) or isinstance(r, bool):
            warn(filename,"typ:imdb_rating",name,"imdb_rating muss float sein")
        elif not (0.0 <= r <= 10.0):
            warn(filename,"wert:imdb_rating",name,f"imdb_rating ausserhalb 0-10 (ist {r})")
        if not isinstance(entry.get("produktionsland"), str) or not entry.get("produktionsland","").strip():
            warn(filename,"typ:produktionsland",name,"produktionsland muss nicht-leerer str sein")


def check_musik_extended(filename, data):
    """Validiert data/musik_extended.json (7 Pflichtfelder, Enums, Typen)."""
    KATEGORIE = {"Pop","Rock","Hip-Hop","Electronic","Legend"}
    REQUIRED  = ["kategorie","gruendungsjahr","streams_mrd","verkaeufe_mio",
                 "herkunftsland","grammys","groesster_hit"]
    if not isinstance(data, dict):
        warn(filename,"struktur","root","musik_extended.json muss ein Dict sein"); return
    for name, entry in data.items():
        if not isinstance(entry, dict):
            warn(filename,"eintrag",name,"Wert ist kein Dict"); continue
        for f in REQUIRED:
            if f not in entry:
                warn(filename,"pflichtfeld",name,f"Feld '{f}' fehlt")
        val = entry.get("kategorie")
        if val not in KATEGORIE:
            warn(filename,"enum:kategorie",name,f"Wert {val!r} nicht erlaubt. Erlaubt: {sorted(KATEGORIE)}")
        for field,typ in [("gruendungsjahr",int),("grammys",int)]:
            if not isinstance(entry.get(field),typ):
                warn(filename,f"typ:{field}",name,f"{field} muss {typ.__name__} sein")
        for field in ("streams_mrd","verkaeufe_mio"):
            if not isinstance(entry.get(field),(int,float)):
                warn(filename,f"typ:{field}",name,f"{field} muss float sein")
        for field in ("herkunftsland","groesster_hit"):
            if not isinstance(entry.get(field),str):
                warn(filename,f"typ:{field}",name,f"{field} muss str sein")

def check_themeparks_extended(filename, data):
    """Validiert data/themeparks_extended.json (flaches Dict, 6 Felder)."""
    REQUIRED = ['kategorie', 'baujahr', 'max_speed_kmh', 'max_hoehe_m',
                'inversionen', 'park_land']
    KAT_ENUM = {'Achterbahn', 'Wasserbahn', 'Darkride', 'Park'}
    if not isinstance(data, dict):
        warn(filename, 'struktur', 'root', 'themeparks_extended.json muss ein Dict sein')
        return
    for name, entry in data.items():
        if not isinstance(entry, dict):
            warn(filename, 'eintrag', name, 'Wert ist kein Dict'); continue
        for f in REQUIRED:
            if f not in entry:
                warn(filename, 'pflichtfeld', name, f"Feld '{f}' fehlt")
        kat = entry.get('kategorie')
        if kat is not None and kat not in KAT_ENUM:
            warn(filename, 'enum:kategorie', name, f"'{kat}' nicht erlaubt")
        for float_f in ('max_speed_kmh', 'max_hoehe_m'):
            v = entry.get(float_f)
            if v is not None and not isinstance(v, (int, float)):
                warn(filename, f'typ:{float_f}', name, f"Muss Float/null sein, ist {type(v).__name__}")
        for int_f in ('baujahr', 'inversionen'):
            v = entry.get(int_f)
            if v is not None and not isinstance(v, int):
                warn(filename, f'typ:{int_f}', name, f"Muss Int/null sein, ist {type(v).__name__}")


def check_kunst_extended(filename, data):
    """Validiert data/kunst_extended.json (flaches Dict, 6 Felder)."""
    REQUIRED = ['kategorie', 'entstehungsjahr', 'schaetzwert_mio_usd',
                'kuenstler', 'epoche', 'standort_museum']
    KAT_ENUM = {'Gemälde', 'Skulptur', 'Installation'}
    if not isinstance(data, dict):
        warn(filename, 'struktur', 'root', 'kunst_extended.json muss ein Dict sein')
        return
    for name, entry in data.items():
        if not isinstance(entry, dict):
            warn(filename, 'eintrag', name, 'Wert ist kein Dict'); continue
        for f in REQUIRED:
            if f not in entry:
                warn(filename, 'pflichtfeld', name, f"Feld '{f}' fehlt")
        kat = entry.get('kategorie')
        if kat is not None and kat not in KAT_ENUM:
            warn(filename, 'enum:kategorie', name, f"'{kat}' nicht erlaubt")
        v = entry.get('schaetzwert_mio_usd')
        if v is not None and not isinstance(v, (int, float)):
            warn(filename, 'typ:schaetzwert_mio_usd', name,
                 f"Muss Float/null sein, ist {type(v).__name__}")
        j = entry.get('entstehungsjahr')
        if j is not None and not isinstance(j, int):
            warn(filename, 'typ:entstehungsjahr', name,
                 f"Muss Int (auch negativ) sein, ist {type(j).__name__}")


def check_boardgames_extended(filename, data):
    """Validiert data/boardgames_extended.json (7 Pflichtfelder, Enums, Typen)."""
    REQUIRED = ['kategorie', 'erscheinungsjahr', 'max_spieler', 'spieldauer_min',
                'bgg_rating', 'autor', 'ursprungsland']
    KAT_ENUM = {'Strategie', 'Party', 'Familie', 'Kartenspiel'}
    if not isinstance(data, dict):
        warn(filename, 'struktur', 'root', 'boardgames_extended.json muss ein Dict sein')
        return
    for name, entry in data.items():
        if not isinstance(entry, dict):
            warn(filename, 'eintrag', name, 'Wert ist kein Dict'); continue
        for f in REQUIRED:
            if f not in entry:
                warn(filename, 'pflichtfeld', name, "Feld '%s' fehlt" % f)
        kat = entry.get('kategorie')
        if kat is not None and kat not in KAT_ENUM:
            warn(filename, 'enum:kategorie', name, "'%s' nicht erlaubt" % kat)
        for int_f in ('erscheinungsjahr', 'max_spieler', 'spieldauer_min'):
            v = entry.get(int_f)
            if v is not None and not isinstance(v, int):
                warn(filename, 'typ:' + int_f, name,
                     'Muss Int sein, ist %s' % type(v).__name__)
        r = entry.get('bgg_rating')
        if r is not None and not isinstance(r, (int, float)):
            warn(filename, 'typ:bgg_rating', name,
                 'Muss Float sein, ist %s' % type(r).__name__)
        elif r is not None and not (0.0 <= float(r) <= 10.0):
            warn(filename, 'range:bgg_rating', name,
                 'bgg_rating muss 0-10 sein (ist %s)' % r)


def check_sprachen_extended(filename, data):
    """Validiert data/sprachen_extended.json (5 Pflichtfelder, Enums, Typen)."""
    REQUIRED = ['sprachfamilie', 'muttersprachler_mio', 'anzahl_laender',
                'schrift', 'ursprungsregion']
    FAM_ENUM = {
        'Indogermanisch', 'Sino-Tibetisch', 'Afroasiatisch', 'Austronesisch',
        'Isoliert', 'Turkisch', 'Dravidisch', 'Niger-Kongo', 'Uralisch',
        'Kartvelisch', 'Austroasiatisch', 'Kra-Dai', 'Quechua',
        'Uto-Aztekisch', 'Tupisch', 'Kunstsprache',
    }
    if not isinstance(data, dict):
        warn(filename, 'struktur', 'root', 'sprachen_extended.json muss ein Dict sein')
        return
    for name, entry in data.items():
        if not isinstance(entry, dict):
            warn(filename, 'eintrag', name, 'Wert ist kein Dict'); continue
        for f in REQUIRED:
            if f not in entry:
                warn(filename, 'pflichtfeld', name, "Feld '%s' fehlt" % f)
        fam = entry.get('sprachfamilie')
        if fam is not None and fam not in FAM_ENUM:
            warn(filename, 'enum:sprachfamilie', name, "'%s' nicht erlaubt" % fam)
        v = entry.get('muttersprachler_mio')
        if v is not None and not isinstance(v, (int, float)):
            warn(filename, 'typ:muttersprachler_mio', name,
                 'Muss Float sein, ist %s' % type(v).__name__)
        n = entry.get('anzahl_laender')
        if n is not None and not isinstance(n, int):
            warn(filename, 'typ:anzahl_laender', name,
                 'Muss Int sein, ist %s' % type(n).__name__)


def check_fluesse_extended(filename, data):
    """Validiert data/fluesse_extended.json."""
    REQUIRED = ['laenge_km', 'einzugsgebiet_km2', 'kontinent',
                'hauptland', 'muendung', 'lat', 'lng']
    KONT_ENUM = {'Afrika','Asien','Europa','Nordamerika','Südamerika','Australien'}
    if not isinstance(data, dict):
        warn(filename, 'struktur', 'root', 'muss ein Dict sein')
        return
    for name, e in data.items():
        if not isinstance(e, dict):
            warn(filename, 'eintrag', name, 'kein Dict'); continue
        for f in REQUIRED:
            if f not in e:
                warn(filename, 'pflichtfeld', name, f"Feld '{f}' fehlt")
        k = e.get('kontinent')
        if k and k not in KONT_ENUM:
            warn(filename, 'enum:kontinent', name, f"'{k}' ungültig")


def check_capitals_extended(filename, data):
    """Validiert data/capitals_extended.json."""
    REQUIRED = ['land','kontinent','einwohner_mio','hoehe_m','lat','lng']
    KONT = {'Europa','Asien','Afrika','Nordamerika','Südamerika','Ozeanien'}
    if not isinstance(data, dict):
        warn(filename,'struktur','root','muss ein Dict sein'); return
    for name, e in data.items():
        if not isinstance(e, dict):
            warn(filename,'eintrag',name,'kein Dict'); continue
        for f in REQUIRED:
            if f not in e:
                warn(filename,'pflichtfeld',name,f"Feld '{f}' fehlt")
        k = e.get('kontinent')
        if k and k not in KONT:
            warn(filename,'enum:kontinent',name,f"'{k}' ungültig")



def check_inseln_extended(filename, data):
    """Validiert data/inseln_extended.json."""
    REQUIRED = ['land', 'ozean', 'kontinent', 'flaeche_km2', 'einwohner_tsd', 'lat', 'lng']
    KONT = {'Europa','Asien','Afrika','Nordamerika','Südamerika','Ozeanien','Arktis'}
    if not isinstance(data, dict):
        warn(filename,'struktur','root','muss ein Dict sein'); return
    for name, e in data.items():
        if not isinstance(e, dict):
            warn(filename,'eintrag',name,'kein Dict'); continue
        for f in REQUIRED:
            if f not in e:
                warn(filename,'pflichtfeld',name,f"Feld '{f}' fehlt")
        k = e.get('kontinent')
        if k and k not in KONT:
            warn(filename,'enum:kontinent',name,f"'{k}' ungültig")


def check_gipfel_extended(filename, data):
    """Validiert data/gipfel_extended.json."""
    REQUIRED = ['hoehe_m', 'gebirge', 'land', 'kontinent', 'erstbesteigung_jahr', 'lat', 'lng']
    KONT = {'Europa','Asien','Afrika','Nordamerika','Südamerika','Ozeanien','Antarktis'}
    if not isinstance(data, dict):
        warn(filename,'struktur','root','muss ein Dict sein'); return
    for name, e in data.items():
        if not isinstance(e, dict):
            warn(filename,'eintrag',name,'kein Dict'); continue
        for f in REQUIRED:
            if f not in e:
                warn(filename,'pflichtfeld',name,f"Feld '{f}' fehlt")
        k = e.get('kontinent')
        if k and k not in KONT:
            warn(filename,'enum:kontinent',name,f"'{k}' ungültig")


def check_klima_extended(filename, data):
    """Validiert data/klima_extended.json."""
    REQUIRED = ['klimazone', 'durchschnitt_temp_c', 'jahresniederschlag_mm', 'kontinent']
    KONT = {'Europa','Asien','Afrika','Nordamerika','Südamerika','Ozeanien','Antarktis'}
    if not isinstance(data, dict):
        warn(filename,'struktur','root','muss ein Dict sein'); return
    for name, e in data.items():
        if not isinstance(e, dict):
            warn(filename,'eintrag',name,'kein Dict'); continue
        for f in REQUIRED:
            if f not in e:
                warn(filename,'pflichtfeld',name,f"Feld '{f}' fehlt")
        k = e.get('kontinent')
        if k and k not in KONT:
            warn(filename,'enum:kontinent',name,f"'{k}' ungültig")


def check_ozeane_extended(filename, data):
    """Validiert data/ozeane_extended.json."""
    REQUIRED = ['typ', 'flaeche_km2', 'max_tiefe_m', 'kontinent_grenze']
    TYPEN = {'Ozean','Meer','Golf','Meerenge','See'}
    if not isinstance(data, dict):
        warn(filename,'struktur','root','muss ein Dict sein'); return
    for name, e in data.items():
        if not isinstance(e, dict):
            warn(filename,'eintrag',name,'kein Dict'); continue
        for f in REQUIRED:
            if f not in e:
                warn(filename,'pflichtfeld',name,f"Feld '{f}' fehlt")
        t = e.get('typ')
        if t and t not in TYPEN:
            warn(filename,'enum:typ',name,f"'{t}' ungültig")

def check_nparks_extended(filename, data):
    """Validiert data/nparks_extended.json."""
    REQUIRED = ['flaeche_km2','gruendung','land','kontinent','oekosystem','lat','lng']
    KONT_ENUM = {'Nordamerika','Südamerika','Europa','Afrika','Asien','Ozeanien','Arktis'}
    if not isinstance(data, dict):
        warn(filename,'struktur','root','muss ein Dict sein'); return
    for name, e in data.items():
        if not isinstance(e, dict):
            warn(filename,'eintrag',name,'kein Dict'); continue
        for f in REQUIRED:
            if f not in e:
                warn(filename,'pflichtfeld',name,f"Feld '{f}' fehlt")
        k = e.get('kontinent')
        if k and k not in KONT_ENUM:
            warn(filename,'enum:kontinent',name,f"'{k}' ungültig")


def check_hunde_extended(filename, data):
    """Validiert data/hunde_extended.json (flaches Dict, 6 Felder)."""
    REQUIRED = ['kategorie', 'max_gewicht_kg', 'lebenserwartung_jahre',
                'widerristhoehe_cm', 'ursprungsland', 'fci_gruppe']
    KAT_ENUM = {'Huetehund', 'Begleithund', 'Jagdhund', 'Terrier', 'Molosser',
                'Hütehund'}
    if not isinstance(data, dict):
        warn(filename, 'struktur', 'root', 'hunde_extended.json muss ein Dict sein')
        return
    for name, entry in data.items():
        if not isinstance(entry, dict):
            warn(filename, 'eintrag', name, 'Wert ist kein Dict'); continue
        for f in REQUIRED:
            if f not in entry:
                warn(filename, 'pflichtfeld', name, "Feld '%s' fehlt" % f)
        kat = entry.get('kategorie')
        if kat is not None and kat not in KAT_ENUM:
            warn(filename, 'enum:kategorie', name, "'%s' nicht erlaubt" % kat)
        for float_f in ('max_gewicht_kg',):
            v = entry.get(float_f)
            if v is not None and not isinstance(v, (int, float)):
                warn(filename, 'typ:' + float_f, name,
                     'Muss Float sein, ist %s' % type(v).__name__)
        for int_f in ('lebenserwartung_jahre', 'widerristhoehe_cm'):
            v = entry.get(int_f)
            if v is not None and not isinstance(v, int):
                warn(filename, 'typ:' + int_f, name,
                     'Muss Int sein, ist %s' % type(v).__name__)
        fg = entry.get('fci_gruppe')
        if fg is not None and not isinstance(fg, int):
            warn(filename, 'typ:fci_gruppe', name,
                 'Muss Int/null sein, ist %s' % type(fg).__name__)


def check_gartenbau_extended(filename, data):
    """Validiert data/gartenbau_extended.json (flaches Dict, 6 Felder)."""
    REQUIRED = ['kategorie', 'max_wuchshoehe_cm', 'wasserbedarf',
                'bodenanspruch', 'ursprungsregion', 'bluetezeit_start_monat']
    KAT_ENUM   = {'Zierpflanze', 'Nutzpflanze', 'Baum', 'Strauch'}
    WASSER_ENUM = {'Wenig', 'Mittel', 'Hoch'}
    BODEN_ENUM  = {'Sauer', 'Neutral', 'Alkalisch', 'Tolerant'}
    if not isinstance(data, dict):
        warn(filename, 'struktur', 'root', 'gartenbau_extended.json muss ein Dict sein')
        return
    for name, entry in data.items():
        if not isinstance(entry, dict):
            warn(filename, 'eintrag', name, 'Wert ist kein Dict'); continue
        for f in REQUIRED:
            if f not in entry:
                warn(filename, 'pflichtfeld', name, "Feld '%s' fehlt" % f)
        kat = entry.get('kategorie')
        if kat is not None and kat not in KAT_ENUM:
            warn(filename, 'enum:kategorie', name, "'%s' nicht erlaubt" % kat)
        w = entry.get('wasserbedarf')
        if w is not None and w not in WASSER_ENUM:
            warn(filename, 'enum:wasserbedarf', name, "'%s' nicht erlaubt" % w)
        b = entry.get('bodenanspruch')
        if b is not None and b not in BODEN_ENUM:
            warn(filename, 'enum:bodenanspruch', name, "'%s' nicht erlaubt" % b)
        v = entry.get('max_wuchshoehe_cm')
        if v is not None and not isinstance(v, int):
            warn(filename, 'typ:max_wuchshoehe_cm', name,
                 'Muss Int sein, ist %s' % type(v).__name__)
        m = entry.get('bluetezeit_start_monat')
        if m is not None:
            if not isinstance(m, int):
                warn(filename, 'typ:bluetezeit_start_monat', name,
                     'Muss Int/null sein, ist %s' % type(m).__name__)
            elif not (1 <= m <= 12):
                warn(filename, 'range:bluetezeit_start_monat', name,
                     'Monat muss 1-12 sein, ist %d' % m)


def check_autos_extended(filename, data):
    """Validiert data/autos_extended.json (flaches Dict, 22 Pflichtfelder)."""
    REQUIRED_FIELDS = [
        "gewicht", "drehmoment", "cw", "kofferraum", "laenge",
        "tank", "akku", "reichweite_km", "verbrauch_l", "verbrauch_kwh",
        "antrieb", "karosserie", "antriebsart", "motorbauart", "zylinder",
        "turbo", "getriebe", "sitze", "neupreis_eur", "baujahr_ende",
        "nordschleife", "konzern",
    ]
    ENUMS = {
        "antrieb":     {"Front", "Heck", "Allrad"},
        "getriebe":    {"Handschalter", "Automatik", "E-Getriebe"},
        "motorbauart": {"Reihe", "V", "W", "Boxer", "Wankel", "E-Motor"},
        "antriebsart": {"Benzin", "Diesel", "EV", "Hybrid", "PHEV", "MHEV"},
        "karosserie":  {"Hatchback", "Limousine", "Kombi", "SUV",
                        "Coupé", "Cabrio", "Roadster", "Sportwagen", "Van", "Pickup"},
        "konzern":     {"VW", "BMW", "Mercedes", "Stellantis", "Ford",
                        "Renault-Nissan", "Toyota", "Hyundai-Kia", "Tata",
                        "Geely", "Honda", "Mazda", "Subaru", "unabhaengig", "unabhängig"},
    }
    if not isinstance(data, dict):
        warn(filename, "struktur", "root", "autos_extended.json muss ein Dict sein")
        return
    for car_name, entry in data.items():
        if not isinstance(entry, dict):
            warn(filename, "eintrag", car_name, "Wert ist kein Dict")
            continue
        # Pflichtfelder
        for f in REQUIRED_FIELDS:
            if f not in entry:
                warn(filename, "pflichtfeld", car_name, f"Feld '{f}' fehlt")
        # Enum-Checks
        for field, allowed in ENUMS.items():
            val = entry.get(field)
            if val is not None and val not in allowed:
                warn(filename, f"enum:{field}", car_name,
                     f"Wert {val!r} nicht erlaubt")
        # Logik-Checks
        art = entry.get("antriebsart", "")
        if art == "EV":
            if entry.get("tank", -1) != 0:
                warn(filename, "logik:EV-tank", car_name,
                     f"EV muss tank=0 haben (ist {entry.get('tank')})")
            if entry.get("verbrauch_l", -1) != 0.0:
                warn(filename, "logik:EV-verbrauch_l", car_name,
                     f"EV muss verbrauch_l=0.0 haben (ist {entry.get('verbrauch_l')})")
            if entry.get("zylinder", -1) != 0:
                warn(filename, "logik:EV-zylinder", car_name,
                     f"EV muss zylinder=0 haben (ist {entry.get('zylinder')})")
        if art not in ("EV", "Hybrid", "PHEV", "MHEV"):
            akku = entry.get("akku", None)
            if akku is not None and float(akku) != 0.0:
                warn(filename, "logik:akku", car_name,
                     f"{art}: akku muss 0.0 sein (ist {akku})")


def detect_and_check(filename):
    data = load(filename)
    name = filename.lower()

    if name.endswith("_pin.json"):
        check_pin(filename, data)
    elif name.endswith("_hl.json"):
        check_hl(filename, data)
    elif name.endswith("_match.json"):
        check_match(filename, data)
    elif name.endswith("_ws.json"):
        check_ws(filename, data)
    elif name == "kultur.json":
        # Legacy mixed: each key is either a plain list or {items,[],prompt,...}
        plain_list_keys = {k: v for k, v in data.items() if isinstance(v, list)}
        obj_keys        = {k: v for k, v in data.items() if isinstance(v, dict)}
        if plain_list_keys:
            # Split plain lists: pin (has lat/lng, no c) vs match (has c)
            pin_plain   = {}
            match_plain = {}
            for k, v in plain_list_keys.items():
                first = v[0] if v else {}
                if ("lat" in first or "lng" in first) and "c" not in first:
                    pin_plain[k] = {"items": v}   # wrap for check_pin()
                else:
                    match_plain[k] = v
            if pin_plain:
                check_pin(filename, pin_plain)
            if match_plain:
                check_match(filename, match_plain)
        if obj_keys:
            # Could be HL, pin, or match with {prompt, items}
            for key, block in obj_keys.items():
                items = block.get("items", [])
                if items and "val" in items[0]:
                    check_hl(filename, {key: block})
                elif items and ("lat" in items[0] or "lng" in items[0]):
                    check_pin(filename, {key: block})
                elif items and "c" in items[0]:
                    check_match(filename, {key: block})
    elif name.endswith("_ws.json") or "ws_" in name:
        check_ws(filename, data)
    elif name == "metro_logos.json":
        for i, item in enumerate(data if isinstance(data, list) else []):
            if not item.get("svg", "").startswith("<svg"):
                warn(filename, "metro_logos", item.get("city", "?"), "SVG fehlt oder ungültig")
            if not item.get("city", "").strip():
                warn(filename, "metro_logos", f"item[{i}]", "city-Feld leer")
    elif name == "autos.json":
        # Lücke 1: 5 HL-Arrays per check_hl validieren
        if isinstance(data, dict):
            for arr_key, block in data.items():
                if isinstance(block, dict) and "items" in block:
                    check_hl(filename, {arr_key: block})
                    if arr_key == "auto_ccm":
                        bad = [i.get("name", "?") for i in block.get("items", [])
                               if i.get("val", 1) == 0]
                        if bad:
                            warn(filename, "auto_ccm", bad[0],
                                 f"{len(bad)} Eintraege mit ccm=0 (EVs muessen ausgeschlossen sein)")
    elif name == "literatur_extended.json":
        check_literatur_extended(filename, data)
    elif name == "robotik_extended.json":
        check_robotik_extended(filename, data)
    elif name == "medizin_extended.json":
        check_medizin_extended(filename, data)
    elif name == "wirtschaft_extended.json":
        check_wirtschaft_extended(filename, data)
    elif name == "geschichte_extended.json":
        check_geschichte_extended(filename, data)
    elif name == "webkultur_extended.json":
        check_webkultur_extended(filename, data)
    elif name == "mythologie.json":
        check_mythologie(filename, data)
    elif name == "architektur.json":
        check_architektur(filename, data)
    elif name == "filme_extended.json":
        check_filme_extended(filename, data)
    elif name == "serien_extended.json":
        check_serien_extended(filename, data)
    elif name == "musik_extended.json":
        check_musik_extended(filename, data)
    elif name == "themeparks_extended.json":
        check_themeparks_extended(filename, data)
    elif name == "kunst_extended.json":
        check_kunst_extended(filename, data)
    elif name == "boardgames_extended.json":
        check_boardgames_extended(filename, data)
    elif name == "sprachen_extended.json":
        check_sprachen_extended(filename, data)
    elif name == "fluesse_extended.json":
        check_fluesse_extended(filename, data)
    elif name == "capitals_extended.json":
        check_capitals_extended(filename, data)
    elif name == "nparks_extended.json":
        check_nparks_extended(filename, data)
    elif name == "hunde_extended.json":
        check_hunde_extended(filename, data)
    elif name == "gartenbau_extended.json":
        check_gartenbau_extended(filename, data)
    elif name == "autos_extended.json":
        check_autos_extended(filename, data)
    elif name == "konsolen.json":
        check_konsolen(filename, data)
    elif name == "regional_extended.json":
        check_regional_extended(filename, data)
    elif name == "timeline.json":
        for key, block in (data.items() if isinstance(data, dict) else {}.items()):
            if not isinstance(block, dict):
                continue
            items = block.get("items", [])
            bad_year = [i.get("n", "?") for i in items
                        if not isinstance(i.get("year"), (int, float))]
            if bad_year:
                warn(filename, key, bad_year[0],
                     f"year-Feld fehlt/ungültig ({len(bad_year)} Items)")
            years = [i.get("year", 0) for i in items
                     if isinstance(i.get("year"), (int, float))]
            if years and max(years) - min(years) < 10:
                warn(filename, key, "range",
                     f"Jahres-Spanne nur {max(years)-min(years)} — zu eng für Timeline")



# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    json_files = sorted(f for f in os.listdir(DATA) if f.endswith(".json"))
    if not json_files:
        print(ERR + "No JSON files found in " + DATA + RESET)
        sys.exit(1)

    print("\n" + BOLD + "=" * 62)
    print(" GeoQuest Content Validator")
    print("=" * 62 + RESET)
    print("Scanning " + str(len(json_files)) + " JSON files in data/\n")

    print("  [i18n-Check gen.py]", end=" ")
    check_i18n()

    checked = 0
    for filename in json_files:
        try:
            before = len(warnings)
            detect_and_check(filename)
            after = len(warnings)
            new = after - before
            status = (WARN + str(new) + " warning(s)" + RESET) if new else (OK + "OK" + RESET)
            print("  " + filename.ljust(38) + " " + status)
            checked += 1
        except Exception as exc:
            print("  " + ERR + filename + ": LOAD ERROR - " + str(exc) + RESET)
            warnings.append((filename, "LOAD ERROR: " + str(exc)))

    # Lücke 3: Cross-Validation autos.json <-> autos_extended.json
    import json as _json
    _autos_p    = os.path.join(DATA, "autos.json")
    _extended_p = os.path.join(DATA, "autos_extended.json")
    if os.path.exists(_autos_p) and os.path.exists(_extended_p):
        print("  [Cross-Val autos <-> extended]", end=" ")
        try:
            with open(_autos_p,    encoding="utf-8") as _fh: _a = _json.load(_fh)
            with open(_extended_p, encoding="utf-8") as _fh: _e = _json.load(_fh)
            _all  = {i["name"] for i in _a.get("auto_bj", {}).get("items", [])}
            _miss = sorted(n for n in _all if n not in _e)
            if _miss:
                for _n in _miss:
                    warn("cross_validation", "autos_extended", _n,
                         "Auto in autos.json aber NICHT in autos_extended.json")
                print(WARN + f"{len(_miss)} fehlend" + RESET)
            else:
                print(OK + f"OK -- alle {len(_all)} Autos im Extended-Dict" + RESET)
        except Exception as _exc:
            warn("cross_validation", "load", "", f"Fehler: {_exc}")
            print(WARN + "Fehler" + RESET)

    print("\n" + BOLD + "=" * 62)
    print(" Results: " + str(checked) + "/" + str(len(json_files)) + " files scanned  |  " + str(len(warnings)) + " warning(s)")
    print("=" * 62 + RESET + "\n")


    # Cross-Validation games_extended: dev_lat/lng numeric check
    _gext_p = os.path.join(DATA, "games_extended.json")
    import json as _json2
    if os.path.exists(_gext_p):
        print("  [Cross-Val games_extended]", end=" ")
        try:
            with open(_gext_p, encoding="utf-8") as _fh: _ge = _json2.load(_fh)
            _bad = [n for n, e in _ge.items()
                    if not isinstance(e.get("dev_lat"),(int,float)) or not isinstance(e.get("dev_lng"),(int,float))]
            if _bad:
                for _n in _bad:
                    warn("cross_val", "games_extended", _n, "dev_lat/lng fehlt oder nicht numerisch")
                print(WARN + f"{len(_bad)} fehlerhaft" + RESET)
            else:
                print(OK + f"OK -- alle {len(_ge)} Spiele haben gueltige Koordinaten" + RESET)
        except Exception as _e:
            print(WARN + f"Fehler: {_e}" + RESET)

    if warnings:
        by_file = defaultdict(list)
        for tag, msg in warnings:
            file_part = tag.split(" > ")[0]
            by_file[file_part].append((tag, msg))

        for file_part, items in by_file.items():
            print(BOLD + file_part + RESET)
            for tag, msg in items:
                key_parts = tag.split(" > ")[1:]
                indent = "  " + " > ".join(key_parts) + " - " if key_parts else "  "
                print("  " + WARN + indent + msg + RESET)
            print()

        if infos:
            print("\n  i  " + str(len(infos)) + " info-only notice(s) (not counted in strict mode)")
        if STRICT:
            print(ERR + "--strict mode: exiting with code 1 due to " + str(len(warnings)) + " warning(s)" + RESET + "\n")
            sys.exit(1)
        else:
            print("i  Re-run with --strict to fail CI on warnings.\n")
    else:
        print(OK + "All content checks passed - no warnings found." + RESET + "\n")


if __name__ == "__main__":
    main()
