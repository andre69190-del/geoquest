"""
patch_298_train_expansion.py
Phase 298.1 — Trainspotter Expansion: Legendaere Routen, Bahnhofs-Architektur, Zug-Hersteller
"""
import os, json, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def patch(content, old, new, label):
    if old in content:
        print(f"  [OK] {label}")
        return content.replace(old, new, 1)
    print(f"  [SKIP] {label} — Anker nicht gefunden")
    return content

# =============================================================
# TEIL 1: Daten generieren
# =============================================================

# --- zug_routen (kultur.json, {n, c} Format) ---
ZUG_ROUTEN = [
    {"n": "Glacier Express",               "c": "Schweiz"},
    {"n": "Bernina Express",               "c": "Schweiz"},
    {"n": "Golden Pass Express",           "c": "Schweiz"},
    {"n": "GoldenPass Belle Epoque",       "c": "Schweiz"},
    {"n": "Trans-Sibirische Eisenbahn",    "c": "Russland"},
    {"n": "Zarengold",                     "c": "Russland"},
    {"n": "Rocky Mountaineer",             "c": "Kanada"},
    {"n": "VIA Rail Canadian",             "c": "Kanada"},
    {"n": "Indian Pacific",                "c": "Australien"},
    {"n": "The Ghan",                      "c": "Australien"},
    {"n": "Great Southern",                "c": "Australien"},
    {"n": "Blue Train",                    "c": "Suedafrika"},
    {"n": "Rovos Rail",                    "c": "Suedafrika"},
    {"n": "Maharajas' Express",            "c": "Indien"},
    {"n": "Palace on Wheels",              "c": "Indien"},
    {"n": "Deccan Odyssey",                "c": "Indien"},
    {"n": "Eastern & Oriental Express",    "c": "Thailand"},
    {"n": "Venice Simplon Orient Express", "c": "Frankreich"},
    {"n": "Caledonian Sleeper",            "c": "Grossbritannien"},
    {"n": "Eurostar",                      "c": "Grossbritannien"},
    {"n": "Thalys",                        "c": "Belgien"},
    {"n": "AVE Madrid–Sevilla",            "c": "Spanien"},
    {"n": "Talgo Avril",                   "c": "Spanien"},
    {"n": "Renfe S-103",                   "c": "Spanien"},
    {"n": "Frecciarossa 1000",             "c": "Italien"},
    {"n": "Trenitalia Frecciargento",      "c": "Italien"},
    {"n": "TGV Duplex",                    "c": "Frankreich"},
    {"n": "Ouigo",                         "c": "Frankreich"},
    {"n": "ICE 3 (BR 403)",                "c": "Deutschland"},
    {"n": "ICE 4 (BR 412)",                "c": "Deutschland"},
    {"n": "Railjet",                       "c": "Oesterreich"},
    {"n": "NightJet",                      "c": "Oesterreich"},
    {"n": "Shinkansen Nozomi",             "c": "Japan"},
    {"n": "Shinkansen Hayabusa",           "c": "Japan"},
    {"n": "KTX-II Sancheon",               "c": "Suedkorea"},
    {"n": "Fuxing Hao CR400",              "c": "China"},
    {"n": "Maglev Shanghai Transrapid",    "c": "China"},
    {"n": "SJ X2000",                      "c": "Schweden"},
    {"n": "VR Pendolino (Sm3)",            "c": "Finnland"},
    {"n": "Euronight EN 40462",            "c": "Oesterreich"},
    {"n": "Pendolino ETR 450",             "c": "Italien"},
    {"n": "RegioJet Yellow",               "c": "Tschechien"},
    {"n": "Heathrow Express",              "c": "Grossbritannien"},
    {"n": "Thameslink Class 700",          "c": "Grossbritannien"},
    {"n": "NS Intercity Direct",           "c": "Niederlande"},
]

# --- zug_bahnhof_typ (tiere_match.json, fixedOpts) ---
ZUG_BAHNHOF_TYP = {
    "prompt": "Welche Bauform hat dieser Bahnhof?",
    "fixedOpts": ["Kopfbahnhof", "Durchgangsbahnhof", "Turmbahnhof", "Keilbahnhof"],
    "items": [
        {"n": "Frankfurt Hbf",           "c": "Kopfbahnhof"},
        {"n": "Muenchen Hbf",            "c": "Kopfbahnhof"},
        {"n": "Stuttgart Hbf",           "c": "Kopfbahnhof"},
        {"n": "Hamburg Hbf",             "c": "Durchgangsbahnhof"},
        {"n": "Leipzig Hbf",             "c": "Kopfbahnhof"},
        {"n": "Nuernberg Hbf",           "c": "Kopfbahnhof"},
        {"n": "Koeln Hbf",               "c": "Durchgangsbahnhof"},
        {"n": "Duesseldorf Hbf",         "c": "Durchgangsbahnhof"},
        {"n": "Berlin Hbf",              "c": "Turmbahnhof"},
        {"n": "Berlin Ostbahnhof",       "c": "Durchgangsbahnhof"},
        {"n": "Wien Hbf",                "c": "Durchgangsbahnhof"},
        {"n": "Wien Westbahnhof",        "c": "Kopfbahnhof"},
        {"n": "Bern",                    "c": "Durchgangsbahnhof"},
        {"n": "Basel SBB",               "c": "Kopfbahnhof"},
        {"n": "Zuerich HB",              "c": "Durchgangsbahnhof"},
        {"n": "Paris Gare de Lyon",      "c": "Kopfbahnhof"},
        {"n": "Paris Gare du Nord",      "c": "Kopfbahnhof"},
        {"n": "London Waterloo",         "c": "Kopfbahnhof"},
        {"n": "London Victoria",         "c": "Kopfbahnhof"},
        {"n": "London St Pancras",       "c": "Kopfbahnhof"},
        {"n": "Amsterdam Centraal",      "c": "Durchgangsbahnhof"},
        {"n": "Bruessel Midi",           "c": "Durchgangsbahnhof"},
        {"n": "Madrid Atocha",           "c": "Kopfbahnhof"},
        {"n": "Milano Centrale",         "c": "Kopfbahnhof"},
        {"n": "Roma Termini",            "c": "Kopfbahnhof"},
        {"n": "Moskau Jaroslawler Bhf",  "c": "Kopfbahnhof"},
        {"n": "Tokio Shinjuku",          "c": "Durchgangsbahnhof"},
        {"n": "New York Penn Station",   "c": "Durchgangsbahnhof"},
        {"n": "Chicago Union Station",   "c": "Kopfbahnhof"},
        {"n": "Sydney Central",          "c": "Kopfbahnhof"},
        {"n": "Hannover Hbf",            "c": "Durchgangsbahnhof"},
        {"n": "Dresden Hbf",             "c": "Durchgangsbahnhof"},
        {"n": "Mannheim Hbf",            "c": "Durchgangsbahnhof"},
        {"n": "Dortmund Hbf",            "c": "Durchgangsbahnhof"},
        {"n": "Essen Hbf",               "c": "Durchgangsbahnhof"},
        {"n": "Karlsruhe Hbf",           "c": "Keilbahnhof"},
        {"n": "Augsburg Hbf",            "c": "Keilbahnhof"},
        {"n": "Breslau (Wroclaw) Hbf",   "c": "Kopfbahnhof"},
        {"n": "Prag Hlavni Nadrazi",     "c": "Durchgangsbahnhof"},
        {"n": "Warschau Centralny",      "c": "Turmbahnhof"},
        {"n": "Budapest Keleti",         "c": "Kopfbahnhof"},
        {"n": "Lissabon Santa Apolonia", "c": "Kopfbahnhof"},
        {"n": "Genf Cornavin",           "c": "Durchgangsbahnhof"},
        {"n": "Strassburg",              "c": "Kopfbahnhof"},
    ]
}

# --- zug_hersteller (tiere_match.json, fixedOpts) ---
ZUG_HERSTELLER = {
    "prompt": "Von welchem Hersteller stammt dieser Zug?",
    "fixedOpts": ["Alstom", "Siemens Mobility", "Hitachi Rail", "Stadler Rail"],
    "items": [
        {"n": "TGV Duplex",                "c": "Alstom"},
        {"n": "TGV M (Avelia Horizon)",    "c": "Alstom"},
        {"n": "Eurostar e320",             "c": "Siemens Mobility"},
        {"n": "ICE 3 (BR 403)",            "c": "Siemens Mobility"},
        {"n": "ICE 4 (BR 412)",            "c": "Siemens Mobility"},
        {"n": "Velaro E (Renfe S-103)",    "c": "Siemens Mobility"},
        {"n": "Velaro RUS (Sapsan)",       "c": "Siemens Mobility"},
        {"n": "Frecciarossa 1000 (ETR 400)","c": "Hitachi Rail"},
        {"n": "Azuma (Class 800)",         "c": "Hitachi Rail"},
        {"n": "Javelin (Class 395)",       "c": "Hitachi Rail"},
        {"n": "Shinkansen N700",           "c": "Hitachi Rail"},
        {"n": "FLIRT (RABe 523)",          "c": "Stadler Rail"},
        {"n": "KISS (RABe 511)",           "c": "Stadler Rail"},
        {"n": "GTW (Gelenktriebwagen)",    "c": "Stadler Rail"},
        {"n": "EC250 (Swiss CFF)",         "c": "Stadler Rail"},
        {"n": "Pendolino ETR 600",         "c": "Alstom"},
        {"n": "Coradia iLint (H2)",        "c": "Alstom"},
        {"n": "Avelia Liberty (Acela 2)",  "c": "Alstom"},
        {"n": "AGV Italo (ETR 575)",       "c": "Alstom"},
        {"n": "Velaro D (ICE 3 Multi)",    "c": "Siemens Mobility"},
        {"n": "Desiro Classic",            "c": "Siemens Mobility"},
        {"n": "Mireo Plus",                "c": "Siemens Mobility"},
        {"n": "Caravaggio (ETR 700)",      "c": "Hitachi Rail"},
        {"n": "Rock (BI-Mode)",            "c": "Hitachi Rail"},
        {"n": "AT300 (Hitachi)",           "c": "Hitachi Rail"},
        {"n": "TWINDEXX (IC2000)",         "c": "Stadler Rail"},
        {"n": "Traverso (RABe 501)",       "c": "Stadler Rail"},
        {"n": "Dosto (RABDe 502)",         "c": "Stadler Rail"},
        {"n": "Euroduplex (TGV 2N2)",      "c": "Alstom"},
        {"n": "Regiolis CANOPUS",          "c": "Alstom"},
        {"n": "Zefiro V300 (ETR 1000)",    "c": "Hitachi Rail"},
        {"n": "Shinkansen E5/H5",          "c": "Hitachi Rail"},
        {"n": "Class 802 IET",             "c": "Hitachi Rail"},
        {"n": "Velaro Novo",               "c": "Siemens Mobility"},
        {"n": "Charger (ACS-64)",          "c": "Siemens Mobility"},
        {"n": "Vectron Lokomotive",        "c": "Siemens Mobility"},
        {"n": "KISS 3 (OBB Railjet 2)",    "c": "Stadler Rail"},
        {"n": "Mutz (RABe 535)",           "c": "Stadler Rail"},
        {"n": "Love (FLIRT-H2)",           "c": "Stadler Rail"},
        {"n": "TGV POS (BR 408-Analog)",   "c": "Alstom"},
        {"n": "X'Trapolis 2.0",            "c": "Alstom"},
        {"n": "Coradia Continental",       "c": "Alstom"},
        {"n": "Coradia Polyvalent",        "c": "Alstom"},
        {"n": "Scorpio (Italo EVO)",       "c": "Hitachi Rail"},
    ]
}

print("=" * 58)
print(" Patch 298.1 — Trainspotter Expansion")
print("=" * 58)

# =============================================================
# TEIL 1a: kultur.json — zug_routen einfuegen
# =============================================================
print("\n[1] kultur.json — zug_routen")
kultur_path = os.path.join(BASE, "data", "kultur.json")
with open(kultur_path, "r", encoding="utf-8") as f:
    kultur = json.load(f)

if "zug_routen" in kultur:
    print("  [SKIP] zug_routen bereits in kultur.json")
else:
    kultur["zug_routen"] = ZUG_ROUTEN
    with open(kultur_path, "w", encoding="utf-8") as f:
        json.dump(kultur, f, ensure_ascii=False, indent=2)
    print(f"  [OK] zug_routen hinzugefuegt ({len(ZUG_ROUTEN)} Items)")

# =============================================================
# TEIL 1b: tiere_match.json — zug_bahnhof_typ + zug_hersteller
# =============================================================
print("\n[2] tiere_match.json — zug_bahnhof_typ + zug_hersteller")
match_path = os.path.join(BASE, "data", "tiere_match.json")
with open(match_path, "r", encoding="utf-8") as f:
    tiere_match = json.load(f)

changed_match = False
if "zug_bahnhof_typ" in tiere_match:
    print("  [SKIP] zug_bahnhof_typ bereits vorhanden")
else:
    tiere_match["zug_bahnhof_typ"] = ZUG_BAHNHOF_TYP
    print(f"  [OK] zug_bahnhof_typ hinzugefuegt ({len(ZUG_BAHNHOF_TYP['items'])} Items)")
    changed_match = True

if "zug_hersteller" in tiere_match:
    print("  [SKIP] zug_hersteller bereits vorhanden")
else:
    tiere_match["zug_hersteller"] = ZUG_HERSTELLER
    print(f"  [OK] zug_hersteller hinzugefuegt ({len(ZUG_HERSTELLER['items'])} Items)")
    changed_match = True

if changed_match:
    with open(match_path, "w", encoding="utf-8") as f:
        json.dump(tiere_match, f, ensure_ascii=False, indent=2)

# =============================================================
# TEIL 2: gen.py — MODES, GEN dispatch, MODE_CATS, Depot
# =============================================================
print("\n[3] gen.py — MODES, GEN, Depot")
gen_path = os.path.join(BASE, "gen.py")
with open(gen_path, "r", encoding="utf-8") as f:
    content = f.read()

# --- MODES Eintraege nach zug_ds100_input ---
MODES_ANCHOR = '{id:"zug_ds100_input",'
MODES_NEW = '''{id:"zug_routen",       icon:"\\u{1F5FA}\\uFE0F",title:"Legendaere Routen",      group:"zuege",prompt:"Aus welchem Land faehrt dieser beruehmt Zug?",desc:"Glacier Express bis Transsibirische Eisenbahn — kenne deine Strecken"},
    {id:"zug_bahnhof_typ", icon:"\\u{1F3DB}\\uFE0F",title:"Bahnhofs-Architektur",   group:"zuege",prompt:"Welche Bauform hat dieser Bahnhof?",              desc:"Kopfbahnhof, Durchgangsbahnhof, Turmbahnhof — die Typen der grossen Hubs"},
    {id:"zug_hersteller",  icon:"\\u{1F3ED}",      title:"Zug-Hersteller",          group:"zuege",prompt:"Von welchem Hersteller stammt dieser Zug?",        desc:"Alstom, Siemens, Hitachi, Stadler — wer baut die schnellsten Zuege?"},
    {id:"zug_ds100_input",'''

content = patch(content, MODES_ANCHOR, MODES_NEW, "MODES Eintraege (zug_routen, zug_bahnhof_typ, zug_hersteller)")

# --- GEN dispatch ---
GEN_ANCHOR = "zug_ds100_input:()=>genDS100InputQ(),"
GEN_NEW = """zug_routen:()=>genUniversalMatchQ("zug_routen"),
  zug_bahnhof_typ:()=>genTiereMatchQ("zug_bahnhof_typ"),
  zug_hersteller:()=>genTiereMatchQ("zug_hersteller"),
  zug_ds100_input:()=>genDS100InputQ(),"""
content = patch(content, GEN_ANCHOR, GEN_NEW, "GEN dispatch")

# --- genUniversalMatchQ _matchCats: zug_routen hinzufuegen ---
CATS_ANCHOR = '"breitengrad_match"]'
CATS_NEW = '"breitengrad_match","zug_routen"]'
content = patch(content, CATS_ANCHOR, CATS_NEW, "_matchCats pool: zug_routen")

# --- MODE_CATS zuege: neue IDs einfuegen ---
ZUEGE_ANCHOR = '"zug_ds100","zug_ds100_input"]'
ZUEGE_NEW = '"zug_ds100","zug_ds100_input","zug_routen","zug_bahnhof_typ","zug_hersteller"]'
content = patch(content, ZUEGE_ANCHOR, ZUEGE_NEW, "MODE_CATS zuege")

# --- trackTrainDepot: trainModes erweitern ---
TRACK_ANCHOR = 'var trainModes=["zug_vkm","zug_panorama","zug_ds100","zug_ds100_input"];'
TRACK_NEW = 'var trainModes=["zug_vkm","zug_panorama","zug_ds100","zug_ds100_input","zug_routen","zug_bahnhof_typ","zug_hersteller"];'
content = patch(content, TRACK_ANCHOR, TRACK_NEW, "trackTrainDepot trainModes")

# --- showTrainDepot: 3 neue Sektionen hinzufuegen ---
DEPOT_ANCHOR = 'html+=renderSec("Bahnhofskuerzel (DS100)",allDs);'
if DEPOT_ANCHOR not in content:
    # Try the unicode variant
    DEPOT_ANCHOR = 'html+=renderSec("Bahnhofskürzel (DS100)",allDs);'

DEPOT_DATA = '''
  var TMATCH=typeof TIER_MATCH_DATA!=="undefined"?TIER_MATCH_DATA:{};
  var allRouten=(KULT.zug_routen||[]).map(function(i){return i.n||"";}).filter(Boolean);
  var allBahnTyp=(TMATCH.zug_bahnhof_typ&&TMATCH.zug_bahnhof_typ.items||[]).map(function(i){return i.n||"";}).filter(Boolean);
  var allHerst=(TMATCH.zug_hersteller&&TMATCH.zug_hersteller.items||[]).map(function(i){return i.n||"";}).filter(Boolean);
'''
DEPOT_RENDER = '''
  html+=renderSec("Legendaere Routen",allRouten);
  html+=renderSec("Bahnhofs-Architektur",allBahnTyp);
  html+=renderSec("Zug-Hersteller",allHerst);
'''

# Insert after the DS100 line
if DEPOT_ANCHOR in content:
    content = content.replace(
        DEPOT_ANCHOR,
        DEPOT_ANCHOR + DEPOT_RENDER,
        1
    )
    # Also insert the data vars before the unlocked= line
    content = content.replace(
        "var unlocked=loadTrainDepot();",
        "var unlocked=loadTrainDepot();" + DEPOT_DATA,
        1
    )
    print("  [OK] showTrainDepot Sektionen (Routen, Bahnhoftyp, Hersteller)")
else:
    print("  [SKIP] showTrainDepot Anker nicht gefunden")

with open(gen_path, "w", encoding="utf-8") as f:
    f.write(content)

# =============================================================
# TEIL 3: verify.py — Sektion 19f fuer neue Match-Modi
# =============================================================
print("\n[4] verify.py — Sektion 19f")
verify_path = os.path.join(BASE, "verify.py")
with open(verify_path, "r", encoding="utf-8") as f:
    vc = f.read()

VERIFY_ANCHOR = "# =============================================================\nprint(\"\\n\" + \"=\" * 58)"
VERIFY_NEW = """# -- 19f. Neue Match-Modi 298.1 (Routen, Bahnhof, Hersteller) --
section("19f. Trainspotter Expansion (Phase 298.1)")
import json as _json
_kultur298 = _json.load(open(os.path.join(DATA_DIR, "../data/kultur.json"), encoding="utf-8")) if False else _json.load(open("data/kultur.json", encoding="utf-8"))
_match298  = _json.load(open(os.path.join("data", "tiere_match.json"), encoding="utf-8"))
# zug_routen in kultur.json
_routen = _kultur298.get("zug_routen", [])
if len(_routen) >= 40:
    ok(f"kultur.json[zug_routen]: {len(_routen)} Items")
else:
    fail(f"kultur.json[zug_routen]: nur {len(_routen)} Items (min 40)")
# zug_bahnhof_typ in tiere_match.json
_btyp = _match298.get("zug_bahnhof_typ", {})
_btyp_items = _btyp.get("items", [])
_btyp_opts  = _btyp.get("fixedOpts", [])
if len(_btyp_items) >= 40 and len(_btyp_opts) == 4:
    if all(i["c"] in _btyp_opts for i in _btyp_items):
        ok(f"tiere_match[zug_bahnhof_typ]: {len(_btyp_items)} Items, fixedOpts valid")
    else:
        fail("zug_bahnhof_typ: c-Wert ausserhalb fixedOpts")
else:
    fail(f"zug_bahnhof_typ: {len(_btyp_items)} Items (min 40), {len(_btyp_opts)} fixedOpts (braucht 4)")
# zug_hersteller in tiere_match.json
_herst = _match298.get("zug_hersteller", {})
_herst_items = _herst.get("items", [])
_herst_opts  = _herst.get("fixedOpts", [])
if len(_herst_items) >= 40 and len(_herst_opts) == 4:
    if all(i["c"] in _herst_opts for i in _herst_items):
        ok(f"tiere_match[zug_hersteller]: {len(_herst_items)} Items, fixedOpts valid")
    else:
        fail("zug_hersteller: c-Wert ausserhalb fixedOpts")
else:
    fail(f"zug_hersteller: {len(_herst_items)} Items (min 40), {len(_herst_opts)} fixedOpts (braucht 4)")

""" + VERIFY_ANCHOR

if "19f. Trainspotter" not in vc:
    vc = vc.replace(VERIFY_ANCHOR, VERIFY_NEW, 1)
    with open(verify_path, "w", encoding="utf-8") as f:
        f.write(vc)
    print("  [OK] Sektion 19f eingefuegt")
else:
    print("  [SKIP] Sektion 19f bereits vorhanden")

print("\n[DONE] Jetzt: python gen.py && python verify.py")
