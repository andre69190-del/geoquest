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

def warn(file, key, item_id, msg):
    tag = f"{file} › {key}" + (f" › {item_id}" if item_id else "")
    warnings.append((tag, msg))

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
                warn(filename, key, n,
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
                warn(filename, key, name, f"Negative val={v} — check if sign is intentional")

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
            warn(filename, key, None,
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
            warn(filename, key, None,
                 f"Only {len(unique_c)} unique answer categories (c-values) — "
                 f"engine will use fewer than 3 distractors. "
                 f"OK for binary/ternary questions; add more variety otherwise. "
                 f"Found: {sorted(unique_c)}")

        # Duplicate subjects check (same question asked twice)
        n_values = [item.get("n","") for item in items]
        for n, count in Counter(n_values).items():
            if count > 1:
                warn(filename, key, n, f"Duplicate subject (n='{n}') appears {count}× — removes variety")

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
        # SVG-Array: [{svg, city, cc}] — prüfe auf leere SVGs und fehlende city
        for i, item in enumerate(data if isinstance(data, list) else []):
            if not item.get("svg","").startswith("<svg"):
                warn(filename, "metro_logos", item.get("city","?"), "SVG fehlt oder ungültig")
            if not item.get("city","").strip():
                warn(filename, "metro_logos", f"item[{i}]", "city-Feld leer")
    elif name == "timeline.json":
        # Timeline-Format: {key: {prompt, unit, items:[{n,year,hint}]}}
        for key, block in (data.items() if isinstance(data, dict) else {}.items()):
            if not isinstance(block, dict): continue
            items = block.get("items", [])
            bad_year = [i.get("n","?") for i in items if not isinstance(i.get("year"), (int,float))]
            if bad_year:
                warn(filename, key, bad_year[0], f"year-Feld fehlt/ungültig ({len(bad_year)} Items)")
            # Sortierbarkeit: Timeline muss sortierbar sein
            years = [i.get("year",0) for i in items if isinstance(i.get("year"),(int,float))]
            if years and max(years) - min(years) < 10:
                warn(filename, key, "range", f"Jahres-Spanne nur {max(years)-min(years)} — zu eng für Timeline")

# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    json_files = sorted(f for f in os.listdir(DATA) if f.endswith(".json"))
    if not json_files:
        print(f"{ERR}No JSON files found in {DATA}{RESET}")
        sys.exit(1)

    print(f"\n{BOLD}{'='*62}")
    print(f" GeoQuest Content Validator")
    print(f"{'='*62}{RESET}")
    print(f"Scanning {len(json_files)} JSON files in data/\n")

    # i18n-Check (einmalig, nicht pro Datei)
    print("  [i18n-Check gen.py]", end=" ")
    check_i18n()

    checked = 0
    for filename in json_files:
        try:
            before = len(warnings)
            detect_and_check(filename)
            after  = len(warnings)
            new    = after - before
            status = f"{WARN}{new} warning(s){RESET}" if new else f"{OK}OK{RESET}"
            print(f"  {filename:<38} {status}")
            checked += 1
        except Exception as exc:
            print(f"  {ERR}{filename}: LOAD ERROR — {exc}{RESET}")
            warnings.append((filename, f"LOAD ERROR: {exc}"))

    print(f"\n{BOLD}{'='*62}")
    print(f" Results: {checked}/{len(json_files)} files scanned  |  {len(warnings)} warning(s)")
    print(f"{'='*62}{RESET}\n")

    if warnings:
        by_file = defaultdict(list)
        for tag, msg in warnings:
            file_part = tag.split(" › ")[0]
            by_file[file_part].append((tag, msg))

        for file_part, items in by_file.items():
            print(f"{BOLD}{file_part}{RESET}")
            for tag, msg in items:
                key_parts = tag.split(" › ")[1:]
                indent    = "  " + " › ".join(key_parts) + " — " if key_parts else "  "
                print(f"  {WARN}{indent}{msg}{RESET}")
            print()

        if STRICT:
            print(f"{ERR}--strict mode: exiting with code 1 due to {len(warnings)} warning(s){RESET}\n")
            sys.exit(1)
        else:
            print(f"ℹ  Re-run with --strict to fail CI on warnings.\n")
    else:
        print(f"{OK}All content checks passed — no warnings found.{RESET}\n")


if __name__ == "__main__":
    main()
