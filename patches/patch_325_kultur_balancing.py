#!/usr/bin/env python3
"""
Phase: 325
Date:  2026-05-31
Author: Claude / Andre
Scope: Kultur-Finale — kleidung, instrumente, taenze geografisch ausbalancieren

Description:
  Erweitert drei Arrays in data/kultur.json um Einträge für die 16 Ziel-Länder
  des Heimvorteil-Algorithmus. Schema aller drei Arrays: {"n": "...", "c": "..."}.
  Fehlende Länder je Array (ermittelt per Schema-Analyse):

  kleidung   → Polen, Tschechien, Ungarn, Rumänien, Schweden, Finnland,
                Dänemark, Kroatien, Bulgarien, Griechenland, Portugal,
                Niederlande, Belgien, Slowakei  (Norwegen bereits vorhanden)
  instrumente→ Polen, Tschechien, Ungarn, Rumänien, Norwegen, Finnland,
                Dänemark, Kroatien, Bulgarien, Portugal, Niederlande,
                Belgien, Slowakei  (Schweden + Griechenland bereits vorhanden)
  taenze     → Rumänien, Schweden, Norwegen, Finnland, Dänemark, Kroatien,
                Niederlande, Belgien, Slowakei  (die übrigen bereits vorhanden)

Dependencies: keine (reine Daten-Erweiterung, kein gen.py-Patch)
Zero-Bug Policy: N/A — kein content.replace()-Aufruf, nur JSON-Append
"""

import json
import subprocess
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KULTUR_PATH = os.path.join(ROOT, "data", "kultur.json")


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Gespeichert: {os.path.basename(path)}")

def detect_schema(items):
    return set(items[0].keys()) if items else set()

def add_dedup(items, new_entries, key="n"):
    existing = {e[key].lower() for e in items}
    added = 0
    for entry in new_entries:
        if entry[key].lower() not in existing:
            items.append(entry)
            existing.add(entry[key].lower())
            added += 1
        else:
            print(f"    Duplikat übersprungen: {entry[key]}")
    return added

def run(cmd, cwd=ROOT):
    print(f"\n$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode


# ---------------------------------------------------------------------------
# Neue Einträge — kleidung  Schema: {n, c}
# ---------------------------------------------------------------------------

NEW_KLEIDUNG = [
    # Polen
    {"n": "Strój łowicki",          "c": "Polen"},
    {"n": "Krakowiak-Tracht",       "c": "Polen"},
    # Tschechien
    {"n": "Mährische Volkstracht",  "c": "Tschechien"},
    {"n": "Kroj (böhmisch)",        "c": "Tschechien"},
    # Ungarn
    {"n": "Magyar Szűr (Schafwollmantel)", "c": "Ungarn"},
    {"n": "Kalocsa-Stickereikleid", "c": "Ungarn"},
    # Rumänien
    {"n": "Ie (rumänische Bluse)",  "c": "Rumänien"},
    {"n": "Cojoc (Schafspelzweste)","c": "Rumänien"},
    # Schweden
    {"n": "Folkdräkt (Schweden)",   "c": "Schweden"},
    {"n": "Dalarna-Tracht",         "c": "Schweden"},
    # Finnland
    {"n": "Kansallispuku",          "c": "Finnland"},
    {"n": "Sámi-Gákti",             "c": "Finnland"},
    # Dänemark
    {"n": "Amager-Tracht",          "c": "Dänemark"},
    {"n": "Hedebo-Tracht",          "c": "Dänemark"},
    # Kroatien
    {"n": "Šokačka Nošnja",         "c": "Kroatien"},
    {"n": "Lijerica-Tracht (Dubrovnik)", "c": "Kroatien"},
    # Bulgarien
    {"n": "Saya (bulgar. Volkskleid)", "c": "Bulgarien"},
    {"n": "Shayak-Wollmantel",      "c": "Bulgarien"},
    # Griechenland
    {"n": "Fustanella",             "c": "Griechenland"},
    {"n": "Evzone-Uniform",         "c": "Griechenland"},
    # Portugal
    {"n": "Traje à Vianesa",        "c": "Portugal"},
    {"n": "Capote Alentejano",      "c": "Portugal"},
    # Niederlande
    {"n": "Volendam-Tracht",        "c": "Niederlande"},
    {"n": "Zeeland-Haube",          "c": "Niederlande"},
    # Belgien
    {"n": "Brügger Spitzentracht",  "c": "Belgien"},
    {"n": "Antwerpener Sonntagstracht", "c": "Belgien"},
    # Slowakei
    {"n": "Čičmany-Tracht",         "c": "Slowakei"},
    {"n": "Detva-Volkstracht",      "c": "Slowakei"},
]

# ---------------------------------------------------------------------------
# Neue Einträge — instrumente  Schema: {n, c}
# ---------------------------------------------------------------------------

NEW_INSTRUMENTE = [
    # Polen
    {"n": "Mazanki (Geige)",        "c": "Polen"},
    {"n": "Suka biłgorajska",       "c": "Polen"},
    # Tschechien
    {"n": "Fujara (Hirtenflöte)",   "c": "Tschechien"},
    {"n": "Dudy (böhmischer Dudelsack)", "c": "Tschechien"},
    # Ungarn
    {"n": "Tárogató",               "c": "Ungarn"},
    {"n": "Koboz (Laute)",          "c": "Ungarn"},
    # Rumänien
    {"n": "Nai (Panflöte)",         "c": "Rumänien"},
    {"n": "Cobza (Laute)",          "c": "Rumänien"},
    # Norwegen
    {"n": "Hardingfele",            "c": "Norwegen"},
    {"n": "Langeleik",              "c": "Norwegen"},
    # Finnland
    {"n": "Kantele",                "c": "Finnland"},
    {"n": "Jouhikko",               "c": "Finnland"},
    # Dänemark
    {"n": "Lur (Bronzehorn)",       "c": "Dänemark"},
    {"n": "Humle (Tischzither)",    "c": "Dänemark"},
    # Kroatien
    {"n": "Lijerica",               "c": "Kroatien"},
    {"n": "Tamburica",              "c": "Kroatien"},
    # Bulgarien
    {"n": "Gaida (bulgar. Sackpfeife)", "c": "Bulgarien"},
    {"n": "Gadulka",                "c": "Bulgarien"},
    # Portugal
    {"n": "Guitarra Portuguesa",    "c": "Portugal"},
    {"n": "Cavaquinho",             "c": "Portugal"},
    # Niederlande
    {"n": "Boerenfluit",            "c": "Niederlande"},
    {"n": "Klompenklapper",         "c": "Niederlande"},
    # Belgien
    {"n": "Carillon (Glockenspiel)","c": "Belgien"},
    {"n": "Vlaamse Doedelzak",      "c": "Belgien"},
    # Slowakei
    {"n": "Fujara (Slowakei)",      "c": "Slowakei"},
    {"n": "Gajdy (slowak. Dudelsack)", "c": "Slowakei"},
]

# ---------------------------------------------------------------------------
# Neue Einträge — taenze  Schema: {n, c}
# ---------------------------------------------------------------------------

NEW_TAENZE = [
    # Rumänien
    {"n": "Hora",                   "c": "Rumänien"},
    {"n": "Căluș",                  "c": "Rumänien"},
    # Schweden
    {"n": "Hambo",                  "c": "Schweden"},
    {"n": "Polska (Tanz)",          "c": "Schweden"},
    # Norwegen
    {"n": "Halling",                "c": "Norwegen"},
    {"n": "Springar",               "c": "Norwegen"},
    # Finnland
    {"n": "Jenkka",                 "c": "Finnland"},
    {"n": "Polska (Finnland)",      "c": "Finnland"},
    # Dänemark
    {"n": "Sekstur",                "c": "Dänemark"},
    {"n": "Masurka (Dänemark)",     "c": "Dänemark"},
    # Kroatien
    {"n": "Kolo",                   "c": "Kroatien"},
    {"n": "Linđo",                  "c": "Kroatien"},
    # Niederlande
    {"n": "Klompendans",            "c": "Niederlande"},
    {"n": "Driekusman",             "c": "Niederlande"},
    # Belgien
    {"n": "Ballo del Fiocco",       "c": "Belgien"},
    {"n": "Vlaamse Bal Folklorique","c": "Belgien"},
    # Slowakei
    {"n": "Odzemok",                "c": "Slowakei"},
    {"n": "Verbunk (Slowakei)",     "c": "Slowakei"},
]


# ---------------------------------------------------------------------------
# Patch ausführen
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("PATCH 325 – Kultur-Finale: kleidung / instrumente / taenze")
    print("=" * 60)

    d = load(KULTUR_PATH)

    totals = {}
    for key, new_data in [
        ("kleidung",    NEW_KLEIDUNG),
        ("instrumente", NEW_INSTRUMENTE),
        ("taenze",      NEW_TAENZE),
    ]:
        arr = d[key]
        schema = detect_schema(arr)
        print(f"\n[kultur.json] {key} — Schema erkannt: {schema}")
        n = add_dedup(arr, new_data)
        totals[key] = (n, len(arr))
        print(f"  → {n} neue Einträge hinzugefügt (gesamt: {len(arr)})")

    save(KULTUR_PATH, d)

    print("\n" + "=" * 60)
    print("Zusammenfassung:")
    for key, (added, total) in totals.items():
        print(f"  {key:14s}  +{added:2d} neu  →  {total} gesamt")

    print("\n" + "=" * 60)
    print("Verifizierung …")
    print("=" * 60)

    rc1 = run([sys.executable, "verify.py"])
    rc2 = run([sys.executable, "validate_content.py"])

    if rc1 != 0 or rc2 != 0:
        print("\n✗ Verifikation fehlgeschlagen — post_phase wird NICHT ausgeführt.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Post-Phase …")
    print("=" * 60)
    rc3 = run([sys.executable, "post_phase.py",
               "--phase", "325",
               "--patch", "patches/patch_325_kultur_balancing.py",
               "--summary",
               "Kultur-Finale: kleidung (+28), instrumente (+26), taenze (+18) "
               "— alle 16 Ziel-Länder EU-Ost/Nord/West vollständig abgedeckt"])
    sys.exit(rc3)
