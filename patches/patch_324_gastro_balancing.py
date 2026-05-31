#!/usr/bin/env python3
"""
Phase: 324
Date:  2026-05-31
Author: Claude / Andre
Scope: Gastronomie-Arrays geografisch ausbalancieren (ATA Balancing Sprint)

Description:
  Erweitert 4 Arrays in gastro_pin.json und gastro_match.json um Einträge
  für die 16 Ziel-Länder des Heimvorteil-Algorithmus. Legt die neuen Arrays
  streetfood (gastro_pin) und suessspeisen (gastro_match) an, falls noch
  nicht vorhanden. Duplikate werden per Lowercase-Abgleich auf dem Feld "n"
  herausgefiltert. Führt verify.py und validate_content.py aus; bei Erfolg
  post_phase.py --phase 324.

Dependencies: keine (reine Daten-Erweiterung, kein gen.py-Patch)
Zero-Bug Policy: N/A — kein content.replace()-Aufruf, nur JSON-Append
"""

# Patch 324 – Gastronomie-Arrays geografisch ausbalancieren
Ziel-Länder: Polen, Tschechien, Ungarn, Rumänien, Schweden, Norwegen, Finnland,
             Dänemark, Kroatien, Bulgarien, Griechenland, Portugal, Niederlande,
             Belgien, Slowakei, Türkei

Erweiterte Arrays:
  1. gastro_pin.json  → nationalgerichte  (Schema: {n, lat, lng})
  2. gastro_pin.json  → streetfood        (neues Array, Schema: {n, lat, lng})
  3. gastro_match.json → hausmannskost    (Schema: {n, c})
  4. gastro_match.json → suessspeisen     (neues Array, Schema: {n, c})
"""

import json
import subprocess
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

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
    """Gibt die Menge der Schlüssel des ersten Eintrags zurück."""
    if not items:
        return set()
    return set(items[0].keys())

def add_dedup(items, new_entries, key="n"):
    """Hängt new_entries an items an, filtert Duplikate nach `key`."""
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

# ---------------------------------------------------------------------------
# Neue Einträge – nationalgerichte (gastro_pin) Schema: {n, lat, lng}
# ---------------------------------------------------------------------------

NEW_NATIONALGERICHTE = [
    # Tschechien
    {"n": "Svíčková (Prag, Tschechien)",        "lat": 50.0755, "lng": 14.4378},
    {"n": "Vepřo-knedlo-zelo (Brünn, Tschechien)", "lat": 49.1951, "lng": 16.6068},
    {"n": "Trdelník (Bratislava / Prag)",         "lat": 50.0755, "lng": 14.4378},
    # Rumänien
    {"n": "Mămăligă (Bukarest, Rumänien)",        "lat": 44.4268, "lng": 26.1025},
    {"n": "Sarmale (Cluj-Napoca, Rumänien)",       "lat": 46.7712, "lng": 23.6236},
    {"n": "Ciorbă de burtă (Bukarest, Rumänien)", "lat": 44.4268, "lng": 26.1025},
    # Schweden
    {"n": "Köttbullar (Stockholm, Schweden)",     "lat": 59.3293, "lng": 18.0686},
    {"n": "Gravlax (Göteborg, Schweden)",         "lat": 57.7089, "lng": 11.9746},
    {"n": "Smörgåsbord (Uppsala, Schweden)",      "lat": 59.8586, "lng": 17.6389},
    # Norwegen
    {"n": "Rakfisk (Valdres, Norwegen)",          "lat": 61.0000, "lng":  9.1000},
    {"n": "Fårikål (Oslo, Norwegen)",             "lat": 59.9139, "lng": 10.7522},
    {"n": "Lutefisk (Bergen, Norwegen)",          "lat": 60.3913, "lng":  5.3221},
    # Finnland
    {"n": "Karjalanpiirakka (Joensuu, Finnland)", "lat": 62.6010, "lng": 29.7636},
    {"n": "Poronkäristys (Rovaniemi, Finnland)",  "lat": 66.5039, "lng": 25.7294},
    {"n": "Kalakukko (Kuopio, Finnland)",         "lat": 62.8924, "lng": 27.6780},
    # Dänemark
    {"n": "Smørrebrød (Kopenhagen, Dänemark)",    "lat": 55.6761, "lng": 12.5683},
    {"n": "Flæskesteg (Odense, Dänemark)",        "lat": 55.4038, "lng": 10.4024},
    {"n": "Æbleskiver (Aarhus, Dänemark)",        "lat": 56.1629, "lng": 10.2039},
    # Kroatien
    {"n": "Peka (Split, Kroatien)",               "lat": 43.5081, "lng": 16.4402},
    {"n": "Štrukli (Zagreb, Kroatien)",           "lat": 45.8150, "lng": 15.9819},
    {"n": "Pasticada (Dubrovnik, Kroatien)",      "lat": 42.6507, "lng": 18.0944},
    # Bulgarien
    {"n": "Banitsa (Sofia, Bulgarien)",           "lat": 42.6977, "lng": 23.3219},
    {"n": "Kavarma (Plovdiv, Bulgarien)",         "lat": 42.1354, "lng": 24.7453},
    {"n": "Shkembe Chorba (Sofia, Bulgarien)",    "lat": 42.6977, "lng": 23.3219},
    # Belgien
    {"n": "Moules-frites (Brüssel, Belgien)",     "lat": 50.8503, "lng":  4.3517},
    {"n": "Stoofvlees (Gent, Belgien)",           "lat": 51.0543, "lng":  3.7174},
    {"n": "Waterzooi (Gent, Belgien)",            "lat": 51.0543, "lng":  3.7174},
    # Slowakei
    {"n": "Bryndzové halušky (Bratislava, Slowakei)", "lat": 48.1486, "lng": 17.1077},
    {"n": "Kapustnica (Košice, Slowakei)",        "lat": 48.7164, "lng": 21.2611},
    {"n": "Lokše (Bratislava, Slowakei)",         "lat": 48.1486, "lng": 17.1077},
]

# ---------------------------------------------------------------------------
# Neue Einträge – streetfood (gastro_pin) Schema: {n, lat, lng}
# ---------------------------------------------------------------------------

NEW_STREETFOOD_PIN = [
    # Polen
    {"n": "Zapiekanka (Krakau, Polen)",           "lat": 50.0647, "lng": 19.9450},
    {"n": "Obwarzanek Krakowski (Krakau, Polen)", "lat": 50.0647, "lng": 19.9450},
    # Tschechien
    {"n": "Párek v rohlíku (Prag, Tschechien)",  "lat": 50.0755, "lng": 14.4378},
    {"n": "Trdelník-Eis (Prag, Tschechien)",     "lat": 50.0755, "lng": 14.4378},
    # Ungarn
    {"n": "Kürtőskalács (Budapest, Ungarn)",      "lat": 47.4979, "lng": 19.0402},
    {"n": "Lángos (Budapest, Ungarn)",            "lat": 47.4979, "lng": 19.0402},
    # Rumänien
    {"n": "Covrigi (Bukarest, Rumänien)",         "lat": 44.4268, "lng": 26.1025},
    {"n": "Mici (Bukarest, Rumänien)",            "lat": 44.4268, "lng": 26.1025},
    # Schweden
    {"n": "Tunnbrödsrulle (Stockholm, Schweden)", "lat": 59.3293, "lng": 18.0686},
    {"n": "Räkmacka (Göteborg, Schweden)",        "lat": 57.7089, "lng": 11.9746},
    # Norwegen
    {"n": "Vafler (Oslo, Norwegen)",              "lat": 59.9139, "lng": 10.7522},
    {"n": "Pølse med lompe (Bergen, Norwegen)",   "lat": 60.3913, "lng":  5.3221},
    # Finnland
    {"n": "Makkara (Tampere, Finnland)",          "lat": 61.4978, "lng": 23.7610},
    {"n": "Munkki (Helsinki, Finnland)",          "lat": 60.1699, "lng": 24.9384},
    # Dänemark
    {"n": "Rød Pølse (Kopenhagen, Dänemark)",    "lat": 55.6761, "lng": 12.5683},
    {"n": "Friturestegt flæsk (Aarhus, Dänemark)", "lat": 56.1629, "lng": 10.2039},
    # Kroatien
    {"n": "Burek (Zagreb, Kroatien)",             "lat": 45.8150, "lng": 15.9819},
    {"n": "Ćevapi (Split, Kroatien)",             "lat": 43.5081, "lng": 16.4402},
    # Bulgarien
    {"n": "Mekitsa (Sofia, Bulgarien)",           "lat": 42.6977, "lng": 23.3219},
    {"n": "Banitsa (Plovdiv, Bulgarien)",         "lat": 42.1354, "lng": 24.7453},
    # Griechenland
    {"n": "Souvlaki (Athen, Griechenland)",       "lat": 37.9838, "lng": 23.7275},
    {"n": "Koulouri (Thessaloniki, Griechenland)","lat": 40.6401, "lng": 22.9444},
    # Portugal
    {"n": "Pastel de Nata (Lissabon, Portugal)",  "lat": 38.7223, "lng": -9.1393},
    {"n": "Bifanas (Porto, Portugal)",            "lat": 41.1579, "lng": -8.6291},
    # Niederlande
    {"n": "Stroopwafel (Gouda, Niederlande)",     "lat": 52.0116, "lng":  4.7083},
    {"n": "Haring (Amsterdam, Niederlande)",      "lat": 52.3676, "lng":  4.9041},
    # Belgien
    {"n": "Gaufre de Liège (Lüttich, Belgien)",  "lat": 50.6326, "lng":  5.5797},
    {"n": "Frieten / Frites (Brüssel, Belgien)",  "lat": 50.8503, "lng":  4.3517},
    # Slowakei
    {"n": "Langoše (Bratislava, Slowakei)",       "lat": 48.1486, "lng": 17.1077},
    {"n": "Trdelník (Bratislava, Slowakei)",      "lat": 48.1486, "lng": 17.1077},
    # Türkei
    {"n": "Simit (Istanbul, Türkei)",             "lat": 41.0082, "lng": 28.9784},
    {"n": "Balık Ekmek (Istanbul, Türkei)",       "lat": 41.0082, "lng": 28.9784},
]

# ---------------------------------------------------------------------------
# Neue Einträge – hausmannskost (gastro_match) Schema: {n, c}
# ---------------------------------------------------------------------------

NEW_HAUSMANNSKOST = [
    # Tschechien
    {"n": "Svíčková na smetaně", "c": "Tschechien"},
    {"n": "Vepřo-knedlo-zelo",   "c": "Tschechien"},
    # Rumänien
    {"n": "Sarmale",             "c": "Rumänien"},
    {"n": "Mămăligă",            "c": "Rumänien"},
    # Schweden
    {"n": "Köttbullar",          "c": "Schweden"},
    {"n": "Janssons Frestelse",  "c": "Schweden"},
    # Norwegen
    {"n": "Fårikål",             "c": "Norwegen"},
    {"n": "Raspeball",           "c": "Norwegen"},
    # Finnland
    {"n": "Karjalanpiirakka",    "c": "Finnland"},
    {"n": "Poronkäristys",       "c": "Finnland"},
    # Kroatien
    {"n": "Peka",                "c": "Kroatien"},
    {"n": "Štrukli",             "c": "Kroatien"},
    # Bulgarien
    {"n": "Kavarma",             "c": "Bulgarien"},
    {"n": "Shkembe Chorba",      "c": "Bulgarien"},
    # Portugal
    {"n": "Bacalhau à Brás",     "c": "Portugal"},
    {"n": "Caldo Verde",         "c": "Portugal"},
    # Belgien
    {"n": "Stoofvlees met friet","c": "Belgien"},
    {"n": "Waterzooi",           "c": "Belgien"},
    # Slowakei
    {"n": "Bryndzové halušky",   "c": "Slowakei"},
    {"n": "Kapustnica",          "c": "Slowakei"},
]

# ---------------------------------------------------------------------------
# Neue Einträge – suessspeisen (gastro_match) Schema: {n, c}
# ---------------------------------------------------------------------------

NEW_SUESSSPEISEN = [
    # Polen
    {"n": "Pączki",              "c": "Polen"},
    {"n": "Makowiec",            "c": "Polen"},
    # Tschechien
    {"n": "Kolache",             "c": "Tschechien"},
    {"n": "Trdelník",            "c": "Tschechien"},
    # Ungarn
    {"n": "Kürtőskalács",        "c": "Ungarn"},
    {"n": "Dobostorte",          "c": "Ungarn"},
    # Rumänien
    {"n": "Cozonac",             "c": "Rumänien"},
    {"n": "Papanași",            "c": "Rumänien"},
    # Schweden
    {"n": "Kanelbulle",          "c": "Schweden"},
    {"n": "Kladdkaka",           "c": "Schweden"},
    # Norwegen
    {"n": "Krumkake",            "c": "Norwegen"},
    {"n": "Rømmegrøt",           "c": "Norwegen"},
    # Finnland
    {"n": "Pulla",               "c": "Finnland"},
    {"n": "Runebergintorttu",    "c": "Finnland"},
    # Dänemark
    {"n": "Æbleskiver",          "c": "Dänemark"},
    {"n": "Wienerbrød",          "c": "Dänemark"},
    # Kroatien
    {"n": "Fritule",             "c": "Kroatien"},
    {"n": "Rožata",              "c": "Kroatien"},
    # Bulgarien
    {"n": "Baklava",             "c": "Bulgarien"},
    {"n": "Tikvenik",            "c": "Bulgarien"},
    # Griechenland
    {"n": "Loukoumades",         "c": "Griechenland"},
    {"n": "Galaktoboureko",      "c": "Griechenland"},
    # Portugal
    {"n": "Pastel de Nata",      "c": "Portugal"},
    {"n": "Arroz Doce",          "c": "Portugal"},
    # Niederlande
    {"n": "Stroopwafel",         "c": "Niederlande"},
    {"n": "Poffertjes",          "c": "Niederlande"},
    # Belgien
    {"n": "Speculoos",           "c": "Belgien"},
    {"n": "Gaufre de Bruxelles", "c": "Belgien"},
    # Slowakei
    {"n": "Medovník",            "c": "Slowakei"},
    {"n": "Šúľance s makom",     "c": "Slowakei"},
    # Türkei
    {"n": "Baklava",             "c": "Türkei"},
    {"n": "Lokum",               "c": "Türkei"},
]

# ---------------------------------------------------------------------------
# Patch ausführen
# ---------------------------------------------------------------------------

def patch_pin():
    path = os.path.join(DATA, "gastro_pin.json")
    d = load(path)

    # --- 1. nationalgerichte ---
    arr = d["nationalgerichte"]
    schema = detect_schema(arr["items"])
    print(f"\n[gastro_pin] nationalgerichte – Schema erkannt: {schema}")
    n = add_dedup(arr["items"], NEW_NATIONALGERICHTE)
    print(f"  → {n} neue Einträge hinzugefügt (gesamt: {len(arr['items'])})")

    # --- 2. streetfood (neu oder vorhanden) ---
    if "streetfood" not in d:
        d["streetfood"] = {
            "prompt": "Wo findet man dieses Street-Food-Gericht?",
            "items": []
        }
        print("\n[gastro_pin] streetfood – Array neu angelegt")
    else:
        print(f"\n[gastro_pin] streetfood – Schema erkannt: {detect_schema(d['streetfood']['items'])}")
    n = add_dedup(d["streetfood"]["items"], NEW_STREETFOOD_PIN)
    print(f"  → {n} neue Einträge hinzugefügt (gesamt: {len(d['streetfood']['items'])})")

    save(path, d)


def patch_match():
    path = os.path.join(DATA, "gastro_match.json")
    d = load(path)

    # --- 3. hausmannskost ---
    arr = d["hausmannskost"]
    schema = detect_schema(arr["items"])
    print(f"\n[gastro_match] hausmannskost – Schema erkannt: {schema}")
    n = add_dedup(arr["items"], NEW_HAUSMANNSKOST)
    print(f"  → {n} neue Einträge hinzugefügt (gesamt: {len(arr['items'])})")

    # --- 4. suessspeisen (neu oder vorhanden) ---
    if "suessspeisen" not in d:
        d["suessspeisen"] = {
            "prompt": "Aus welchem Land stammt diese Süßspeise?",
            "items": []
        }
        print("\n[gastro_match] suessspeisen – Array neu angelegt")
    else:
        print(f"\n[gastro_match] suessspeisen – Schema erkannt: {detect_schema(d['suessspeisen']['items'])}")
    n = add_dedup(d["suessspeisen"]["items"], NEW_SUESSSPEISEN)
    print(f"  → {n} neue Einträge hinzugefügt (gesamt: {len(d['suessspeisen']['items'])})")

    save(path, d)


def run(cmd, cwd=ROOT):
    print(f"\n$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("PATCH 324 – Gastronomie-Arrays balancieren")
    print("=" * 60)

    patch_pin()
    patch_match()

    print("\n" + "=" * 60)
    print("Verifizierung …")
    print("=" * 60)

    rc1 = run([sys.executable, "verify.py"])
    rc2 = run([sys.executable, "validate_content.py"])

    if rc1 != 0 or rc2 != 0:
        print("\n✗ Verifikation fehlgeschlagen – post_phase wird NICHT ausgeführt.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Post-Phase …")
    print("=" * 60)
    rc3 = run([sys.executable, "post_phase.py", "--phase", "324",
               "--patch", "patches/patch_324_gastro_balancing.py",
               "--summary",
               "Gastronomie-Arrays geografisch ausbalanciert: "
               "nationalgerichte (+30), streetfood (neu, 32), "
               "hausmannskost (+20), suessspeisen (neu, 31) — "
               "Fokus Ziel-Länder EU-Ost/Nord/West"])
    sys.exit(rc3)
