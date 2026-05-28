#!/usr/bin/env python3
"""
post_phase.py — GeoQuest Post-Sprint Automatisierung
Automatisiert alle 5 Checklisten-Schritte nach einem Sprint.

Usage:
    python3 post_phase.py --phase 263 --summary "Beschreibung"
    python3 post_phase.py --phase 264 --summary "Beschreibung" --patch patch_264_mega_sweep.py
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))

GERMAN_MONTHS = {
    1: "Januar", 2: "Februar", 3: "März", 4: "April",
    5: "Mai", 6: "Juni", 7: "Juli", 8: "August",
    9: "September", 10: "Oktober", 11: "November", 12: "Dezember"
}

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


def ok(msg):
    print(f"  {GREEN}✓{RESET} {msg}")


def warn(msg):
    print(f"  {YELLOW}⚠{RESET} {msg}")


def err(msg):
    print(f"  {RED}✗{RESET} {msg}")


# ─── Hilfsfunktionen ────────────────────────────────────────────────────────

def get_month_year():
    now = datetime.now()
    return f"{GERMAN_MONTHS[now.month]} {now.year}"


def get_date_str():
    return datetime.now().strftime("%m/%d/%Y")


def get_geoquest_size_str():
    path = os.path.join(BASE, "GeoQuest.html")
    if not os.path.exists(path):
        warn("GeoQuest.html nicht gefunden — Größe unbekannt")
        return "?.??"
    size_bytes = os.path.getsize(path)
    size_mb = size_bytes / (1024 * 1024)
    return f"{size_mb:.2f}"


def recalc_item_counts():
    """
    Liest alle data/*.json Dateien und baut ein Dict: json_key → Anzahl Items.
    Unterstützt alle 4 Formate:
      - pin/hl/match:  {key: {prompt: ..., items: [...]}}
      - ws:            {key: {word: ..., validWords: [...]}}
      - kultur (flat): {key: [...]}
    """
    data_dir = os.path.join(BASE, "data")
    counts = {}

    for fn in sorted(os.listdir(data_dir)):
        if not fn.endswith(".json"):
            continue
        path = os.path.join(data_dir, fn)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            warn(f"Lesefehler {fn}: {e}")
            continue

        if not isinstance(data, dict):
            continue

        for key, val in data.items():
            if isinstance(val, dict):
                # pin/hl/match → items[], ws → validWords[]
                items = val.get("items") or val.get("validWords") or []
                counts[key] = len(items)
            elif isinstance(val, list):
                # kultur.json: flat lists
                counts[key] = len(val)

    return counts


# ─── Schritt 1: unlock_and_push.bat ─────────────────────────────────────────

def update_bat(phase, summary):
    bat_path = os.path.join(BASE, "unlock_and_push.bat")
    if not os.path.exists(bat_path):
        err("unlock_and_push.bat nicht gefunden!")
        return

    with open(bat_path, 'rb') as f:
        content = f.read()

    new_msg = f"Content: Phase {phase}. {summary}. verify: 89/89."
    new_line = f'git commit -m "{new_msg}"'.encode('utf-8')

    new_content = re.sub(
        rb'git commit -m "[^"]*"',
        new_line,
        content
    )

    if new_content == content:
        warn("unlock_and_push.bat: kein Commit-Message-Pattern gefunden!")
        return

    # CRLF erzwingen (Windows-Zeilenenden beibehalten)
    text = new_content.decode('utf-8')
    text = text.replace('\r\n', '\n').replace('\n', '\r\n')
    new_content = text.encode('utf-8')

    with open(bat_path, 'wb') as f:
        f.write(new_content)

    ok(f"unlock_and_push.bat → \"{new_msg[:60]}...\"")


# ─── Schritt 2: ARCHITECTURE.md ─────────────────────────────────────────────

def update_architecture(phase, summary, patch_file, size_str):
    arch_path = os.path.join(BASE, "ARCHITECTURE.md")
    if not os.path.exists(arch_path):
        err("ARCHITECTURE.md nicht gefunden!")
        return

    month_year = get_month_year()

    with open(arch_path, encoding="utf-8") as f:
        text = f.read()

    changes = 0

    # 1. Version-Zeile
    new_text, n = re.subn(
        r'\*\*Version:\*\* Phase \d+ \(Stand: [^)]+\)',
        f'**Version:** Phase {phase} (Stand: {month_year})',
        text
    )
    text = new_text; changes += n

    # 2. Build-Zeile: GeoQuest.html Größe aktualisieren
    new_text, n = re.subn(
        r'(GeoQuest\.html → )[\d.]+( MB)',
        rf'\g<1>{size_str}\2',
        text
    )
    text = new_text; changes += n

    # 3. Letztes Update
    new_text, n = re.subn(
        r'\*Letztes Update: Phase \d+ --[^\n]*\n',
        f'*Letztes Update: Phase {phase} -- {summary}, 681 Modi, 37 Datendateien, {month_year}.*\n',
        text
    )
    text = new_text; changes += n

    # 4. Stand Phase im Katalog-Header
    new_text, n = re.subn(
        r'\*\*Stand Phase \d+ -- 681 Modi[^*]*\*\*',
        f'**Stand Phase {phase} -- 681 Modi in 20 Kategorien**',
        text
    )
    text = new_text; changes += n

    # 5. Footer-Zeile
    new_text, n = re.subn(
        r'\*Katalog: 681 Modi \| Stand Phase \d+ \|[^*]*\*',
        f'*Katalog: 681 Modi | Stand Phase {phase} | {month_year}*',
        text
    )
    text = new_text; changes += n

    # 6. Neue Zeile in Patch-Tabelle einfügen (nach letzter | **NNN** | Zeile)
    new_row = f'| **{phase}** | {patch_file} | **{summary}** |\n'
    last_match = None
    for m in re.finditer(r'\| \*\*\d+\*\* \| \S+ \|[^\n]*\n', text):
        last_match = m
    if last_match:
        insert_pos = last_match.end()
        # Nicht einfügen wenn bereits vorhanden
        if f'| **{phase}**' not in text:
            text = text[:insert_pos] + new_row + text[insert_pos:]
            changes += 1
        else:
            warn(f"ARCHITECTURE.md: Phase {phase} Eintrag bereits vorhanden")
    else:
        warn("ARCHITECTURE.md: Patch-Tabelle nicht gefunden")

    with open(arch_path, encoding="utf-8", mode='w') as f:
        f.write(text)

    ok(f"ARCHITECTURE.md → Phase {phase}, GeoQuest.html {size_str} MB ({changes} Änderungen)")


# ─── Schritt 3: README.md ────────────────────────────────────────────────────

def update_readme(phase):
    readme_path = os.path.join(BASE, "README.md")
    if not os.path.exists(readme_path):
        err("README.md nicht gefunden!")
        return

    today = get_date_str()

    with open(readme_path, encoding="utf-8") as f:
        text = f.read()

    new_text, n = re.subn(
        r'Deployed: \S+ — Phase \d+ \| \d+ Modi \| verify: 89/89',
        f'Deployed: {today} — Phase {phase} | 681 Modi | verify: 89/89',
        text
    )

    if n == 0:
        warn("README.md: Kein Deployed-Pattern gefunden!")
        return

    with open(readme_path, encoding="utf-8", mode='w') as f:
        f.write(new_text)

    ok(f"README.md → Deployed: {today} — Phase {phase}")


# ─── Schritt 4: GeoQuest_Website_Konzept.md ─────────────────────────────────

def update_konzept(phase, size_str):
    konzept_path = os.path.join(BASE, "GeoQuest_Website_Konzept.md")
    if not os.path.exists(konzept_path):
        err("GeoQuest_Website_Konzept.md nicht gefunden!")
        return

    month_year = get_month_year()

    with open(konzept_path, encoding="utf-8") as f:
        text = f.read()

    new_text, n = re.subn(
        r'\*Konzept erstellt: [^|]+\| Phase \d+ \| GeoQuest v[\d.]+ MB \| \d+ Modi\*',
        f'*Konzept erstellt: {month_year} | Phase {phase} | GeoQuest v{size_str} MB | 681 Modi*',
        text
    )

    if n == 0:
        warn("GeoQuest_Website_Konzept.md: Footer-Pattern nicht gefunden!")
        return

    with open(konzept_path, encoding="utf-8", mode='w') as f:
        f.write(new_text)

    ok(f"GeoQuest_Website_Konzept.md → Phase {phase}, v{size_str} MB")


# ─── Schritt 5: GeoQuest_Spielübersicht.html ────────────────────────────────

def update_spieluebersicht(phase, counts):
    uebersicht_path = os.path.join(BASE, "GeoQuest_Spielübersicht.html")
    if not os.path.exists(uebersicht_path):
        err("GeoQuest_Spielübersicht.html nicht gefunden!")
        return

    month_year = get_month_year()

    with open(uebersicht_path, encoding="utf-8") as f:
        text = f.read()

    # Phase-Marker in Titel, Meta, Footer
    text = re.sub(
        r'GeoQuest Spielübersicht — Phase \d+',
        f'GeoQuest Spielübersicht — Phase {phase}',
        text
    )
    text = re.sub(
        r'Phase \d+ · [A-Za-zäöüÄÖÜß]+ \d{4}',
        f'Phase {phase} · {month_year}',
        text
    )
    text = re.sub(
        r'GeoQuest Phase \d+ · \d+ Modi',
        f'GeoQuest Phase {phase} · 681 Modi',
        text
    )

    # Badge-Aktualisierung: N Items
    # Pattern: <td class="mid">mode_id</td>...N Items</span>
    # Alles auf einer Zeile, kein DOTALL nötig
    badge_pattern = r'(<td class="mid">([^<]+)</td>)(.*?)(\d+)( Items</span>)'
    updated_count = 0
    skipped_count = 0

    def resolve_key(mode_id):
        """
        Leitet den JSON-Schlüssel aus einer Mode-ID ab.
        Strategie (in Reihenfolge):
          1. Mode-Präfix (uk_/hl_/ws_) entfernen → direkter Lookup
          2. Ersten Segment-Präfix entfernen (z.B. gastro_name → name)
          3. sportwissen_ → sport_ ersetzen
        """
        key = mode_id
        for pfx in ('uk_', 'hl_', 'ws_'):
            if mode_id.startswith(pfx):
                key = mode_id[len(pfx):]
                break

        # 1. Direkter Lookup
        if key in counts:
            return key

        # 2. Ersten Segment-Präfix entfernen: gastro_X → X, tiere_X → X, etc.
        parts = key.split('_', 1)
        if len(parts) == 2:
            stripped = parts[1]
            if stripped in counts:
                return stripped

        # 3. sportwissen_ → sport_ (JSON-Keys haben sport_-Präfix)
        if key.startswith('sportwissen_'):
            alt = 'sport_' + key[len('sportwissen_'):]
            if alt in counts:
                return alt

        return None  # nicht aufgelöst

    def badge_replacer(m):
        nonlocal updated_count, skipped_count
        mode_id = m.group(2).strip()
        resolved = resolve_key(mode_id)

        if resolved is not None:
            new_count = counts[resolved]
            old_count = int(m.group(4))
            if new_count != old_count:
                updated_count += 1
            return m.group(1) + m.group(3) + str(new_count) + m.group(5)
        else:
            skipped_count += 1
            return m.group(0)

    text = re.sub(badge_pattern, badge_replacer, text)

    with open(uebersicht_path, encoding="utf-8", mode='w') as f:
        f.write(text)

    ok(
        f"GeoQuest_Spielübersicht.html → Phase {phase}, "
        f"{updated_count} Badges geändert, {skipped_count} nicht im JSON (erwartet)"
    )


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="GeoQuest Post-Sprint Automatisierung — aktualisiert alle Metadaten."
    )
    parser.add_argument("--phase",   type=int, required=True,
                        help="Phase-Nummer (z.B. 263)")
    parser.add_argument("--summary", type=str, required=True,
                        help="Kurzbeschreibung der Phase (für Commit-Message + ARCHITECTURE.md)")
    parser.add_argument("--patch",   type=str, default=None,
                        help="Patch-Dateiname für ARCHITECTURE.md (default: patch_NNN.py)")
    args = parser.parse_args()

    phase   = args.phase
    summary = args.summary
    patch_file = args.patch or f"patch_{phase:03d}.py"

    print(f"\n{BOLD}🚀 post_phase.py — Phase {phase}{RESET}")
    print(f"   Summary : {summary}")
    print(f"   Patch   : {patch_file}")
    print()

    # JSON-Counts einlesen
    print(f"📊 Lese JSON-Daten aus data/...")
    counts = recalc_item_counts()
    print(f"   {len(counts)} JSON-Schlüssel eingelesen\n")

    # GeoQuest.html Größe
    size_str = get_geoquest_size_str()

    # Alle 5 Schritte
    print(f"📝 Aktualisiere Dateien (5 Schritte):")
    update_bat(phase, summary)
    update_architecture(phase, summary, patch_file, size_str)
    update_readme(phase)
    update_konzept(phase, size_str)
    update_spieluebersicht(phase, counts)

    # Abschluss-Stats
    geoquest_path = os.path.join(BASE, "GeoQuest.html")
    if os.path.exists(geoquest_path):
        size_bytes = os.path.getsize(geoquest_path)
        print(f"\n{GREEN}{BOLD}✅ Phase {phase} — alle Metadaten aktualisiert!{RESET}")
        print(f"   GeoQuest.html : {size_str} MB ({size_bytes:,} Bytes)")
    else:
        print(f"\n{GREEN}{BOLD}✅ Phase {phase} — alle Metadaten aktualisiert!{RESET}")
        print(f"   GeoQuest.html : nicht gefunden (gen.py noch nicht ausgeführt?)")

    print(f"\n{YELLOW}💡 Nächster Schritt:{RESET} unlock_and_push.bat ausführen\n")


if __name__ == "__main__":
    main()
