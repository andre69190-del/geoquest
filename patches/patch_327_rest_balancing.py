#!/usr/bin/env python3
"""
Phase: 327
Date:  2026-05-31
Author: Claude / Andre
Scope: Sport, Geologie & Archäologie geografisch ausbalancieren

Description:
  Die Ursprungs-Mission nannte sport_wissen.json, geologie.json, archaeologie.json —
  diese Dateien existieren nicht. Echte Dateinamen: sport_match.json, sport_pin.json,
  geo_match.json, geo_pin.json, archaeologie_match.json, archaeologie_pin.json.

  Semantische Vorab-Prüfung ergab: Die meisten Arrays haben KEIN geographisches c-Feld
  (c = Spielerzahl, Weltverband, Ja/Nein, Gesteinsklasse, Erdzeitalter, Methode etc.).
  Folgende 5 Arrays tragen echte Länderdaten und wurden erweitert:

    sport_match      → sport_herkunft        {n,c}  c=Herkunftsland    15 Länder fehlten
    sport_match      → sport_sportlegende_land{n,c}  c=Land der Legende  9 Länder fehlten
    geo_match        → geo_hoehlen_land       {n,c}  c=Land des Höhlensystems 13 fehlten
    archaeologie_match→ repatriierung         {n,c}  c=forderndes Land  13 Länder fehlten
    archaeologie_pin → megalithanlagen        {n,lat,lng}               viele fehlten

  Bewusst NICHT erweitert (c nicht geographisch):
    sport_teamgroesse, sport_weltverband, sport_olympisch, sport_disziplin_kategorie,
    sport_sportart_kontinent, geo_gesteinsarten, geo_mineralien, geo_fossil_zeitalter,
    geo_wunder_entstehung, geo_landschaft_ursprung, archaeologie epochen/werkzeuge/
    datierungsmethoden/stratigraphie/isotopenanalyse/faelschungen/welterbe_gefahr etc.

Dependencies: keine (reine Daten-Erweiterung, kein gen.py-Patch)
Zero-Bug Policy: N/A — kein content.replace()-Aufruf, nur JSON-Append
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
# 1. sport_match.json / sport_herkunft  {n, c}  c = Herkunftsland der Sportart
#    Fehlend: Polen, Tschechien, Ungarn, Rumänien, Schweden, Finnland,
#             Dänemark, Kroatien, Bulgarien, Griechenland, Portugal,
#             Niederlande, Belgien, Slowakei, Türkei
# ---------------------------------------------------------------------------

NEW_SPORT_HERKUNFT = [
    # Polen — Palant (traditionelles Schlagballspiel, ältester Vorläufer des Baseball)
    {"n": "Palant (Schlagballspiel)", "c": "Polen"},
    # Tschechien — Sokol-Turnbewegung (Ursprung der modernen Massengymnastik)
    {"n": "Sokol-Gymnastik", "c": "Tschechien"},
    # Ungarn — Wasserball (internationale Dominanz seit 1900; frühe Regelentwicklung)
    {"n": "Wasserball (internationale Regelentwicklung)", "c": "Ungarn"},
    # Rumänien — Oina (traditionelles Schlagballspiel, 14. Jh.)
    {"n": "Oina (rumänisches Schlagballspiel)", "c": "Rumänien"},
    # Schweden — Bandy (Eissport, Vorläufer des Eishockeys)
    {"n": "Bandy (Eissport)", "c": "Schweden"},
    {"n": "Orientierungslauf", "c": "Schweden"},
    # Finnland — Pesäpallo (finnisches Baseball)
    {"n": "Pesäpallo (Finnisches Baseball)", "c": "Finnland"},
    # Dänemark — Handball (Feldhandball, frühe Regelgebung 1906)
    {"n": "Handball (Feldhandball)", "c": "Dänemark"},
    # Kroatien — Picigin (Wasserballspiel in den Seichten, Split)
    {"n": "Picigin (Strandwasserspiel)", "c": "Kroatien"},
    # Bulgarien — Kukeri-Kampfsport (traditionelles Ringkampfritual)
    {"n": "Bulgarisches Ringen (Kabakçı güreş)", "c": "Bulgarien"},
    # Griechenland — Antike Olympische Spiele
    {"n": "Antike Olympische Spiele", "c": "Griechenland"},
    {"n": "Diskuswurf (antike Disziplin)", "c": "Griechenland"},
    # Portugal — Jogo do Pau (Stockfechtkunst)
    {"n": "Jogo do Pau (Stockfechten)", "c": "Portugal"},
    # Niederlande — Korfball (einzige gemischtgeschlechtliche Mannschaftssportart)
    {"n": "Korfball", "c": "Niederlande"},
    {"n": "Fierljeppen (Polsstokspringen)", "c": "Niederlande"},
    # Belgien — Pigeon Racing (Brieftaubenrennen, organisierte Wettkämpfe seit 1800)
    {"n": "Brieftaubenrennen (Colombophilie)", "c": "Belgien"},
    # Slowakei — keine eindeutige Sportart-Erfindung; Skirennläufe in der Tatra
    # (bewusst kein Eintrag erzwungen — inhaltliche Qualität vor Vollständigkeit)
    # Türkei — Kırkpınar-Ölringkampf (ältestes noch ausgetragenes Sportturnier der Welt)
    {"n": "Yağlı güreş / Kırkpınar (Öl-Ringen)", "c": "Türkei"},
    {"n": "Cirit (Reiterlanzenspiel)", "c": "Türkei"},
]

# ---------------------------------------------------------------------------
# 2. sport_match.json / sport_sportlegende_land  {n, c}  c = Heimatland
#    Fehlend: Polen, Tschechien, Rumänien, Finnland, Dänemark,
#             Kroatien, Bulgarien, Slowakei, Türkei
# ---------------------------------------------------------------------------

NEW_SPORT_LEGENDEN = [
    # Polen
    {"n": "Robert Lewandowski (Fußball)", "c": "Polen"},
    {"n": "Anita Włodarczyk (Hammerwurf-Weltrekord)", "c": "Polen"},
    # Tschechien
    {"n": "Emil Zátopek (Leichtathletik, 3× Gold Helsinki 1952)", "c": "Tschechien"},
    {"n": "Jaromír Jágr (Eishockey)", "c": "Tschechien"},
    # Rumänien
    {"n": "Nadia Comăneci (Turnen, erste 10,0)", "c": "Rumänien"},
    {"n": "Gheorghe Hagi (Fußball)", "c": "Rumänien"},
    # Finnland
    {"n": "Paavo Nurmi (Leichtathletik, 9× Olympiagold)", "c": "Finnland"},
    {"n": "Mika Häkkinen (Formel 1, 2× Weltmeister)", "c": "Finnland"},
    # Dänemark
    {"n": "Peter Schmeichel (Fußball-Torwart)", "c": "Dänemark"},
    {"n": "Caroline Wozniacki (Tennis, US-Open-Siegerin)", "c": "Dänemark"},
    # Kroatien
    {"n": "Luka Modrić (Fußball, Ballon d'Or 2018)", "c": "Kroatien"},
    {"n": "Janica Kostelić (4× Olympiagold Ski Alpin)", "c": "Kroatien"},
    # Bulgarien
    {"n": "Hristo Stoichkov (Fußball, Ballon d'Or 1994)", "c": "Bulgarien"},
    {"n": "Stefka Kostadinova (Hochsprung-Weltrekord 2,09 m)", "c": "Bulgarien"},
    # Slowakei
    {"n": "Peter Šatan (Eishockey)", "c": "Slowakei"},
    {"n": "Stan Mikita (Eishockey, NHL-Legende)", "c": "Slowakei"},
    # Türkei
    {"n": "Naim Süleymanoğlu (Gewichtheben, 3× Olympiagold)", "c": "Türkei"},
    {"n": "Hicham El Guerrouj", "c": "Türkei"},  # fallback — wird ggf. als Duplikat erkannt
]

# Korrektur: El Guerrouj ist Marokko — ersetzen durch echte türkische Legende
NEW_SPORT_LEGENDEN = [e for e in NEW_SPORT_LEGENDEN
                      if e["n"] != "Hicham El Guerrouj"]
NEW_SPORT_LEGENDEN.append(
    {"n": "Burhan Felek (Leichtathletik-Pionier Türkei)", "c": "Türkei"}
)

# ---------------------------------------------------------------------------
# 3. geo_match.json / geo_hoehlen_land  {n, c}  c = Land des Höhlensystems
#    Fehlend: Polen, Tschechien, Rumänien, Schweden, Norwegen, Finnland,
#             Dänemark, Kroatien, Bulgarien, Griechenland, Niederlande,
#             Belgien, Türkei
# ---------------------------------------------------------------------------

NEW_HOEHLEN = [
    # Polen
    {"n": "Tatra-Höhlensystem (Jaskinia Mroźna)", "c": "Polen"},
    {"n": "Wieliczka Salzbergwerk (Schaubergwerk)", "c": "Polen"},
    # Tschechien
    {"n": "Macocha-Abgrund / Moravský kras", "c": "Tschechien"},
    {"n": "Javoříčské jeskyně (Mährischer Karst)", "c": "Tschechien"},
    # Rumänien
    {"n": "Peștera Scărișoara (Eishöhle)", "c": "Rumänien"},
    {"n": "Peștera Muierilor (Frauenhöhle)", "c": "Rumänien"},
    # Schweden
    {"n": "Lummelundagrottan (Gotland)", "c": "Schweden"},
    # Norwegen
    {"n": "Grønligrotta (Nordlicht-Höhle, Mo i Rana)", "c": "Norwegen"},
    {"n": "Setergrotta (Nordnorwegen)", "c": "Norwegen"},
    # Finnland — wenige Kalksteinhöhlen, keine berühmten Systeme
    # (bewusst kein Eintrag erzwungen)
    # Dänemark — kaum natürliche Höhlen; Møns Klint hat Kalkfelsen, keine Höhlen
    # (bewusst kein Eintrag erzwungen)
    # Kroatien
    {"n": "Baraćeve špilje (Karst-Höhlen, Plitvice)", "c": "Kroatien"},
    {"n": "Modra špilja (Blaue Grotte, Biševo)", "c": "Kroatien"},
    # Bulgarien
    {"n": "Magura-Höhle (Steinzeithöhlenmalerei)", "c": "Bulgarien"},
    {"n": "Devetashka Höhle (Fledermaus-Kolonie)", "c": "Bulgarien"},
    # Griechenland
    {"n": "Diros-Grotten (Mani-Halbinsel)", "c": "Griechenland"},
    {"n": "Petralona-Höhle (Homo heidelbergensis-Fund)", "c": "Griechenland"},
    # Niederlande — Valkenburg-Maastunnel (Mergelhöhlen)
    {"n": "Velvet Cave Valkenburg (Mergelhöhle)", "c": "Niederlande"},
    # Belgien
    {"n": "Grotte de Han (Han-sur-Lesse)", "c": "Belgien"},
    {"n": "Grottes de Remouchamps (Ourthe-Fluss)", "c": "Belgien"},
    # Türkei
    {"n": "İnsuyu Mağarası (Burdur)", "c": "Türkei"},
    {"n": "Damlataş Mağarası (Alanya)", "c": "Türkei"},
]

# ---------------------------------------------------------------------------
# 4. archaeologie_match.json / repatriierung  {n, c}  c = forderndes Land
#    Fehlend: Tschechien, Ungarn, Rumänien, Schweden, Norwegen, Finnland,
#             Dänemark, Kroatien, Bulgarien, Portugal, Niederlande,
#             Belgien, Slowakei
# ---------------------------------------------------------------------------

NEW_REPATRIIERUNG = [
    # Tschechien — Kunst aus der NS-Zeit / Böhmische Kronjuwelen
    {"n": "Böhmische Kunstwerke aus Berliner Museen", "c": "Tschechien"},
    # Ungarn — Seuso-Schatz (spätantike Silberservices)
    {"n": "Seuso-Schatz (spätantike Silberservices)", "c": "Ungarn"},
    # Rumänien — Dakischer Goldschatz (Decebalus-Schatz)
    {"n": "Dakische Goldhelme aus Budapest-Museum", "c": "Rumänien"},
    # Schweden — Samische Kulturgüter
    {"n": "Sámi-Kulturerbe (ethnografische Sammlungen)", "c": "Schweden"},
    # Norwegen — Grönländisches und samisches Erbe
    {"n": "Grönländische Artefakte (Kopenhagener Museen)", "c": "Norwegen"},
    # Finnland — Karelische Kulturgüter nach 1940
    {"n": "Karelische Kulturgüter aus Leningrader Museen", "c": "Finnland"},
    # Dänemark — Grönländische Mumien und Artefakte
    {"n": "Qilakitsoq-Mumien (grönländisches Erbe)", "c": "Dänemark"},
    # Kroatien — Antike Artefakte aus britischen und österreichischen Museen
    {"n": "Illyrische Bronzehelme aus Wien", "c": "Kroatien"},
    # Bulgarien — Thrakischer Goldschatz
    {"n": "Thrakischer Goldschatz von Panagyurischte (Replik-Streit)", "c": "Bulgarien"},
    {"n": "Rogozen-Silberschatz (teilweise in Auslandssammlungen)", "c": "Bulgarien"},
    # Portugal — Koloniale Artefakte aus Angola und Mosambik
    {"n": "Luanda-Kunstobjekte aus portugiesischer Kolonialzeit", "c": "Portugal"},
    # Niederlande — Indonesische Kulturgüter (größte Rückgabe-Aktion 2023)
    {"n": "Indonesische Kulturgüter (700 Objekte, Rückgabe 2023)", "c": "Niederlande"},
    # Belgien — Kongostaat-Artefakte (Tervuren-Museum)
    {"n": "Kongostaat-Artefakte (AfricaMuseum Tervuren)", "c": "Belgien"},
    # Slowakei — Großmährische Kronjuwelen
    {"n": "Großmährische Artefakte aus tschechischen Museen", "c": "Slowakei"},
]

# ---------------------------------------------------------------------------
# 5. archaeologie_pin.json / megalithanlagen  {n, lat, lng}
#    Koordinaten-basiert — Zielländer mit europäischer Megalith-Tradition
# ---------------------------------------------------------------------------

NEW_MEGALITHANLAGEN = [
    # Polen — Kujawische Langhügel (älteste Megalithgräber Polens)
    {"n": "Wietrzychowice Langhügel (Polen)",       "lat": 52.26, "lng": 18.95},
    {"n": "Gaj-Megalith (Kujawy, Polen)",            "lat": 52.5,  "lng": 18.7},
    # Tschechien — Neolithische Langhügelgräber in Böhmen
    {"n": "Mšecké Žehrovice Megalith (Tschechien)", "lat": 50.15, "lng": 13.94},
    # Ungarn — Sopron-Kreis Neolithikum-Zentrum
    {"n": "Ság-hegy Megalith-Areal (Ungarn)",        "lat": 47.53, "lng": 17.19},
    # Rumänien — Hügelgräber der Dakerfürsten
    {"n": "Sarmizegetusa Regia (Dakische Festung, Rumänien)", "lat": 45.62, "lng": 23.31},
    # Schweden — Ales Stenar (1× bereits vorhanden?), Hunnebeds
    {"n": "Ales Stenar (Schiffssetzung, Schweden)",   "lat": 55.38, "lng": 14.05},
    {"n": "Blomsholm Schiffssetzung (Schweden)",      "lat": 58.67, "lng": 11.4},
    # Norwegen
    {"n": "Borre-Grabhügel (Vestfold, Norwegen)",     "lat": 59.38, "lng": 10.46},
    {"n": "Raknehaugen (größter Grabhügel Norwegens)", "lat": 60.09, "lng": 11.35},
    # Dänemark — Dysser (dänische Megalithgräber)
    {"n": "Kong Askers Høj (Dysse, Dänemark)",        "lat": 55.79, "lng": 12.02},
    {"n": "Klekkende Høj (Megalithgrab, Møn)",        "lat": 54.97, "lng": 12.5},
    # Kroatien — Illyrische Grabhügel
    {"n": "Vela Spila Megalith-Gebiet (Korčula)",     "lat": 42.96, "lng": 16.87},
    # Bulgarien — Thrakische Grabhügel (Apollonia-Region)
    {"n": "Thrakische Großgrabhügel Kazanlak (Bulgarien)", "lat": 42.6, "lng": 25.4},
    {"n": "Svetitsata Megalith-Komplex (Bulgarien)",  "lat": 42.39, "lng": 25.64},
    # Griechenland — Neolithische Stätten
    {"n": "Sesklo (älteste Siedlung Europas, Griechenland)", "lat": 39.38, "lng": 22.7},
    # Niederlande — Hunebedden (größte Megalithserie der Niederlande)
    {"n": "Hunebedden D27 (Borger, Niederlande)",     "lat": 52.92, "lng": 6.80},
    {"n": "Hunebed D53 (Drenthe, Niederlande)",       "lat": 52.84, "lng": 6.63},
    # Belgien — Wallonische Megalithen
    {"n": "Dolmen du Pont d'Arcole (Wallonien, Belgien)", "lat": 50.46, "lng": 4.39},
    {"n": "Pierre Brunehault (Menhir, Belgien)",      "lat": 50.56, "lng": 3.85},
    # Slowakei — Neolithische Kreisgrabenanlagen
    {"n": "Svodín Rondell (Neolithikum, Slowakei)",   "lat": 47.88, "lng": 18.42},
    # Türkei — Göbekli Tepe (falls noch nicht vorhanden)
    {"n": "Göbekli Tepe (ältestes Heiligtum der Welt)", "lat": 37.22, "lng": 38.92},
    {"n": "Karahan Tepe (Taş Tepeler, Türkei)",        "lat": 37.05, "lng": 39.27},
]


# ---------------------------------------------------------------------------
# Patch ausführen
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("PATCH 327 – Sport, Geo & Archäologie ausbalancieren")
    print("  (Nur semantisch valide Länder-Arrays)")
    print("=" * 60)

    totals = {}

    # --- sport_match.json ---
    sm_path = os.path.join(DATA, "sport_match.json")
    sm = load(sm_path)

    for key, new_data in [
        ("sport_herkunft",         NEW_SPORT_HERKUNFT),
        ("sport_sportlegende_land",NEW_SPORT_LEGENDEN),
    ]:
        arr = sm[key]["items"]
        schema = detect_schema(arr)
        print(f"\n[sport_match.json] {key} — Schema: {schema}")
        n = add_dedup(arr, new_data)
        totals[key] = (n, len(arr))
        print(f"  → {n} neu (gesamt: {len(arr)})")

    save(sm_path, sm)

    # --- geo_match.json ---
    gm_path = os.path.join(DATA, "geo_match.json")
    gm = load(gm_path)
    arr = gm["geo_hoehlen_land"]["items"]
    schema = detect_schema(arr)
    print(f"\n[geo_match.json] geo_hoehlen_land — Schema: {schema}")
    n = add_dedup(arr, NEW_HOEHLEN)
    totals["geo_hoehlen_land"] = (n, len(arr))
    print(f"  → {n} neu (gesamt: {len(arr)})")
    save(gm_path, gm)

    # --- archaeologie_match.json ---
    am_path = os.path.join(DATA, "archaeologie_match.json")
    am = load(am_path)
    arr = am["repatriierung"]["items"]
    schema = detect_schema(arr)
    print(f"\n[archaeologie_match.json] repatriierung — Schema: {schema}")
    n = add_dedup(arr, NEW_REPATRIIERUNG)
    totals["repatriierung"] = (n, len(arr))
    print(f"  → {n} neu (gesamt: {len(arr)})")
    save(am_path, am)

    # --- archaeologie_pin.json ---
    ap_path = os.path.join(DATA, "archaeologie_pin.json")
    ap = load(ap_path)
    arr = ap["megalithanlagen"]["items"]
    schema = detect_schema(arr)
    print(f"\n[archaeologie_pin.json] megalithanlagen — Schema: {schema}")
    n = add_dedup(arr, NEW_MEGALITHANLAGEN)
    totals["megalithanlagen"] = (n, len(arr))
    print(f"  → {n} neu (gesamt: {len(arr)})")
    save(ap_path, ap)

    print("\n" + "=" * 60)
    print("Zusammenfassung:")
    for key, (added, total) in totals.items():
        print(f"  {key:30s}  +{added:2d} neu  →  {total} gesamt")

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
               "--phase", "327",
               "--patch", "patches/patch_327_rest_balancing.py",
               "--summary",
               "Sport/Geo/Archäologie-Balancing: sport_herkunft, sport_sportlegende_land, "
               "geo_hoehlen_land, repatriierung, megalithanlagen — "
               "nur semantisch valide Länder-Arrays erweitert"])
    sys.exit(rc3)
