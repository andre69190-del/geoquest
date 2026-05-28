#!/usr/bin/env python3
"""
Phase 259: Data Expansion Sprint — Top-15 Schwachstellen-Modi
==============================================================
Alle 15 schlimmsten Modi (5–8 Items) werden auf 25+ Items aufgefüllt.
Zieldatei: data/kultur.json

14 Match-Modi (format: {n, c})  — je 5 Items → 25 Items:
  begruessung, blumen, brettspiele, entdecker, erfindungen,
  exporte, feiertage, kaese, kaffee, kleidung,
  literatur, sport, suessspeisen, taenze

1 Pin-Modus (format: {n, lat, lng})  — 8 Items → 25 Items:
  canyons
"""

import json, pathlib, sys

BASE = pathlib.Path("/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest")
KULTUR = BASE / "data" / "kultur.json"

def jload(p):  return json.loads(p.read_text(encoding="utf-8"))
def jsave(p, d): p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

# ─────────────────────────────────────────────────────────────────────────────
# NEUE EINTRÄGE — je Format {n, c} für Match-Modi
# ─────────────────────────────────────────────────────────────────────────────

NEW_DATA = {

"kaese": [
    {"n": "Cheddar",          "c": "Großbritannien"},
    {"n": "Stilton",          "c": "Großbritannien"},
    {"n": "Brie",             "c": "Frankreich"},
    {"n": "Camembert",        "c": "Frankreich"},
    {"n": "Comté",            "c": "Frankreich"},
    {"n": "Ossau-Iraty",      "c": "Frankreich"},
    {"n": "Emmentaler",       "c": "Schweiz"},
    {"n": "Gruyère",          "c": "Schweiz"},
    {"n": "Gorgonzola",       "c": "Italien"},
    {"n": "Taleggio",         "c": "Italien"},
    {"n": "Pecorino Romano",  "c": "Italien"},
    {"n": "Asiago",           "c": "Italien"},
    {"n": "Mozzarella",       "c": "Italien"},
    {"n": "Halloumi",         "c": "Zypern"},
    {"n": "Edam",             "c": "Niederlande"},
    {"n": "Jarlsberg",        "c": "Norwegen"},
    {"n": "Havarti",          "c": "Dänemark"},
    {"n": "Limburger",        "c": "Belgien"},
    {"n": "Queso Oaxaca",     "c": "Mexiko"},
    {"n": "Tilsiter",         "c": "Deutschland"},
],

"suessspeisen": [
    {"n": "Mochi",            "c": "Japan"},
    {"n": "Dango",            "c": "Japan"},
    {"n": "Gulab Jamun",      "c": "Indien"},
    {"n": "Rasgolla",         "c": "Indien"},
    {"n": "Kanelbullar",      "c": "Schweden"},
    {"n": "Prinsesstårta",    "c": "Schweden"},
    {"n": "Strudel",          "c": "Österreich"},
    {"n": "Stroopwafel",      "c": "Niederlande"},
    {"n": "Loukoumades",      "c": "Griechenland"},
    {"n": "Galaktoboureko",   "c": "Griechenland"},
    {"n": "Alfajores",        "c": "Argentinien"},
    {"n": "Brigadeiro",       "c": "Brasilien"},
    {"n": "Tres Leches",      "c": "Mexiko"},
    {"n": "Mango Sticky Rice","c": "Thailand"},
    {"n": "Kanafeh",          "c": "Palästina"},
    {"n": "Malva Pudding",    "c": "Südafrika"},
    {"n": "Koeksister",       "c": "Südafrika"},
    {"n": "Turrón",           "c": "Spanien"},
    {"n": "Kkwabaegi",        "c": "Südkorea"},
    {"n": "Bolo de Mel",      "c": "Portugal"},
],

"kaffee": [
    {"n": "Cappuccino",        "c": "Italien"},
    {"n": "Ristretto",         "c": "Italien"},
    {"n": "Latte Macchiato",   "c": "Italien"},
    {"n": "Irish Coffee",      "c": "Irland"},
    {"n": "Kopi Luwak",        "c": "Indonesien"},
    {"n": "Café Cubano",       "c": "Kuba"},
    {"n": "Cortado",           "c": "Spanien"},
    {"n": "Pharisäer",         "c": "Deutschland"},
    {"n": "Eiskaffee",         "c": "Deutschland"},
    {"n": "Wiener Melange",    "c": "Österreich"},
    {"n": "Einspänner",        "c": "Österreich"},
    {"n": "Vietnamese Egg Coffee","c": "Vietnam"},
    {"n": "Dalgona Coffee",    "c": "Südkorea"},
    {"n": "Mazagran",          "c": "Algerien"},
    {"n": "Qahwa",             "c": "Jemen"},
    {"n": "Café Frappé",       "c": "Griechenland"},
    {"n": "Café com Leite",    "c": "Portugal"},
    {"n": "Buna",              "c": "Äthiopien"},
    {"n": "Kopi",              "c": "Singapur"},
    {"n": "Tinto",             "c": "Kolumbien"},
],

"taenze": [
    {"n": "Walzer",          "c": "Österreich"},
    {"n": "Polka",           "c": "Tschechien"},
    {"n": "Salsa",           "c": "Kuba"},
    {"n": "Merengue",        "c": "Dominikanische Republik"},
    {"n": "Cumbia",          "c": "Kolumbien"},
    {"n": "Tinku",           "c": "Bolivien"},
    {"n": "Bharatanatyam",   "c": "Indien"},
    {"n": "Bhangra",         "c": "Indien"},
    {"n": "Haka",            "c": "Neuseeland"},
    {"n": "Kecak",           "c": "Indonesien"},
    {"n": "Morris Dance",    "c": "Großbritannien"},
    {"n": "Irish Step Dance","c": "Irland"},
    {"n": "Mazurka",         "c": "Polen"},
    {"n": "Fandango",        "c": "Portugal"},
    {"n": "Csárdás",         "c": "Ungarn"},
    {"n": "Hopak",           "c": "Ukraine"},
    {"n": "Lezginka",        "c": "Georgien"},
    {"n": "Adumu",           "c": "Kenia"},
    {"n": "Lindy Hop",       "c": "USA"},
    {"n": "Zapateado",       "c": "Mexiko"},
],

"kleidung": [
    {"n": "Dirndl",          "c": "Österreich"},
    {"n": "Thobe",           "c": "Saudi-Arabien"},
    {"n": "Abaya",           "c": "Vereinigte Arabische Emirate"},
    {"n": "Kufiya",          "c": "Palästina"},
    {"n": "Hanbok",          "c": "Südkorea"},
    {"n": "Ao Dai",          "c": "Vietnam"},
    {"n": "Cheongsam",       "c": "China"},
    {"n": "Batik",           "c": "Indonesien"},
    {"n": "Sarong",          "c": "Malaysia"},
    {"n": "Boubou",          "c": "Senegal"},
    {"n": "Kente",           "c": "Ghana"},
    {"n": "Dashiki",         "c": "Nigeria"},
    {"n": "Kanga",           "c": "Kenia"},
    {"n": "Shalwar Kameez",  "c": "Pakistan"},
    {"n": "Gho",             "c": "Bhutan"},
    {"n": "Deel",            "c": "Mongolei"},
    {"n": "Haik",            "c": "Marokko"},
    {"n": "Parka",           "c": "Kanada"},
    {"n": "Kurta",           "c": "Indien"},
    {"n": "Toga",            "c": "Italien"},
],

"literatur": [
    {"n": "Leo Tolstoi",                "c": "Russland"},
    {"n": "Alexander Puschkin",         "c": "Russland"},
    {"n": "Franz Kafka",                "c": "Tschechien"},
    {"n": "James Joyce",                "c": "Irland"},
    {"n": "Victor Hugo",                "c": "Frankreich"},
    {"n": "Miguel de Cervantes",        "c": "Spanien"},
    {"n": "Dante Alighieri",            "c": "Italien"},
    {"n": "William Shakespeare",        "c": "Großbritannien"},
    {"n": "Henrik Ibsen",               "c": "Norwegen"},
    {"n": "Johann Wolfgang von Goethe", "c": "Deutschland"},
    {"n": "Jorge Luis Borges",          "c": "Argentinien"},
    {"n": "Pablo Neruda",               "c": "Chile"},
    {"n": "Chinua Achebe",              "c": "Nigeria"},
    {"n": "Naguib Mahfouz",             "c": "Ägypten"},
    {"n": "Haruki Murakami",            "c": "Japan"},
    {"n": "Rabindranath Tagore",        "c": "Indien"},
    {"n": "Rumi",                       "c": "Iran"},
    {"n": "Ngugi wa Thiong'o",          "c": "Kenia"},
    {"n": "Lu Xun",                     "c": "China"},
    {"n": "Homer",                      "c": "Griechenland"},
],

"begruessung": [
    {"n": "Handkuss",              "c": "Österreich"},
    {"n": "Abrazo",                "c": "Argentinien"},
    {"n": "Mejilla-Kuss",          "c": "Spanien"},
    {"n": "Sawubona",              "c": "Südafrika"},
    {"n": "Kunik (Nasenreiben)",   "c": "Kanada"},
    {"n": "Annyeonghaseyo",        "c": "Südkorea"},
    {"n": "Dumela",                "c": "Botswana"},
    {"n": "Hujambo",               "c": "Tansania"},
    {"n": "Salaam",                "c": "Arabische Welt"},
    {"n": "Besa",                  "c": "Albanien"},
    {"n": "Xin chào",              "c": "Vietnam"},
    {"n": "Pranaama",              "c": "Nepal"},
    {"n": "Mbote",                 "c": "DR Kongo"},
    {"n": "G'day",                 "c": "Australien"},
    {"n": "Knicks",                "c": "Großbritannien"},
    {"n": "Shukrani",              "c": "Kenia"},
    {"n": "Dastbosi",              "c": "Iran"},
    {"n": "Pozdrav (Grüßen)",      "c": "Russland"},
    {"n": "Merhaba",               "c": "Türkei"},
    {"n": "Guten Tag (Handschlag)","c": "Deutschland"},
],

"feiertage": [
    {"n": "Diwali",          "c": "Indien"},
    {"n": "Holi",            "c": "Indien"},
    {"n": "Republic Day",    "c": "Indien"},
    {"n": "Nowruz",          "c": "Iran"},
    {"n": "Inti Raymi",      "c": "Peru"},
    {"n": "Día de los Muertos","c": "Mexiko"},
    {"n": "St. Patrick's Day","c": "Irland"},
    {"n": "Burns Night",     "c": "Schottland"},
    {"n": "Vesak",           "c": "Sri Lanka"},
    {"n": "Australia Day",   "c": "Australien"},
    {"n": "Carnaval",        "c": "Brasilien"},
    {"n": "Sinterklaas",     "c": "Niederlande"},
    {"n": "Koningsdag",      "c": "Niederlande"},
    {"n": "Midsommar",       "c": "Schweden"},
    {"n": "Dragon Boat Festival","c": "China"},
    {"n": "Chuseok",         "c": "Südkorea"},
    {"n": "Loi Krathong",    "c": "Thailand"},
    {"n": "Naadam",          "c": "Mongolei"},
    {"n": "Guy Fawkes Night","c": "Großbritannien"},
    {"n": "Hanami",          "c": "Japan"},
],

"erfindungen": [
    {"n": "Dampfmaschine",     "c": "Großbritannien"},
    {"n": "Impfstoff",         "c": "Großbritannien"},
    {"n": "Penicillin (Entdeckung)","c": "Großbritannien"},
    {"n": "Transistor",        "c": "USA"},
    {"n": "Glühbirne",         "c": "USA"},
    {"n": "Flugzeug",          "c": "USA"},
    {"n": "WWW (Internet)",    "c": "Schweiz"},
    {"n": "Klettverschluss",   "c": "Schweiz"},
    {"n": "Aspirin",           "c": "Deutschland"},
    {"n": "Röntgenstrahlen",   "c": "Deutschland"},
    {"n": "Automobil",         "c": "Deutschland"},
    {"n": "Radio",             "c": "Italien"},
    {"n": "Stethoskop",        "c": "Frankreich"},
    {"n": "Algebra (Grundlagen)","c": "Arabische Welt"},
    {"n": "Dezimalsystem",     "c": "Indien"},
    {"n": "Porzellan",         "c": "China"},
    {"n": "Seide",             "c": "China"},
    {"n": "Schießpulver",      "c": "China"},
    {"n": "Kontaktlinsen",     "c": "Deutschland"},
    {"n": "Destillation",      "c": "Arabische Welt"},
],

"exporte": [
    {"n": "Diamanten",       "c": "Südafrika"},
    {"n": "Erdöl",           "c": "Saudi-Arabien"},
    {"n": "Kaviar",          "c": "Aserbaidschan"},
    {"n": "Bananen",         "c": "Ecuador"},
    {"n": "Wein",            "c": "Frankreich"},
    {"n": "Trüffel",         "c": "Frankreich"},
    {"n": "Lachs",           "c": "Norwegen"},
    {"n": "Whisky",          "c": "Großbritannien"},
    {"n": "Tulpen",          "c": "Niederlande"},
    {"n": "Jade",            "c": "Myanmar"},
    {"n": "Tee",             "c": "Sri Lanka"},
    {"n": "Baumwolle",       "c": "Ägypten"},
    {"n": "Vanille",         "c": "Madagaskar"},
    {"n": "Ingwer",          "c": "Jamaika"},
    {"n": "Mango",           "c": "Indien"},
    {"n": "Quinoa",          "c": "Peru"},
    {"n": "Tequila",         "c": "Mexiko"},
    {"n": "Kakao",           "c": "Ghana"},
    {"n": "Kautschuk",       "c": "Malaysia"},
    {"n": "Sisal",           "c": "Tansania"},
],

"blumen": [
    {"n": "Rose (Rosenöl)",  "c": "Bulgarien"},
    {"n": "Lavendel",        "c": "Frankreich"},
    {"n": "Protea",          "c": "Südafrika"},
    {"n": "Wattle (Akazie)", "c": "Australien"},
    {"n": "Kowhai",          "c": "Neuseeland"},
    {"n": "Jacaranda",       "c": "Argentinien"},
    {"n": "Frangipani",      "c": "Indonesien"},
    {"n": "Magnolia",        "c": "USA"},
    {"n": "Sonnenblume",     "c": "Ukraine"},
    {"n": "Blaubell",        "c": "Schottland"},
    {"n": "Edelweiß",        "c": "Schweiz"},
    {"n": "Kaktusblüte",     "c": "Mexiko"},
    {"n": "Orchidee",        "c": "Singapur"},
    {"n": "Shamrock",        "c": "Irland"},
    {"n": "Mohnblume",       "c": "Belgien"},
    {"n": "Fleur-de-Lis",    "c": "Frankreich"},
    {"n": "Puya raimondii",  "c": "Peru"},
    {"n": "Ylang-Ylang",     "c": "Komoren"},
    {"n": "Erdorchidee",     "c": "Papua-Neuguinea"},
    {"n": "Wisteria",        "c": "China"},
],

"entdecker": [
    {"n": "Christopher Columbus",    "c": "Italien"},
    {"n": "Amerigo Vespucci",        "c": "Italien"},
    {"n": "John Cabot",              "c": "Italien"},
    {"n": "David Livingstone",       "c": "Großbritannien"},
    {"n": "Francis Drake",           "c": "Großbritannien"},
    {"n": "Ernest Shackleton",       "c": "Irland"},
    {"n": "Henry Hudson",            "c": "Großbritannien"},
    {"n": "Bartolomeu Dias",         "c": "Portugal"},
    {"n": "Pedro Álvares Cabral",    "c": "Portugal"},
    {"n": "Zheng He",                "c": "China"},
    {"n": "Leif Eriksson",           "c": "Norwegen"},
    {"n": "Abel Tasman",             "c": "Niederlande"},
    {"n": "Willem Barentsz",         "c": "Niederlande"},
    {"n": "Ibn Battuta",             "c": "Marokko"},
    {"n": "Robert Peary",            "c": "USA"},
    {"n": "Alexander von Humboldt",  "c": "Deutschland"},
    {"n": "Samuel de Champlain",     "c": "Frankreich"},
    {"n": "Hernán Cortés",           "c": "Spanien"},
    {"n": "Mungo Park",              "c": "Großbritannien"},
    {"n": "Meriwether Lewis",        "c": "USA"},
],

"sport": [
    {"n": "Kabaddi",            "c": "Bangladesch"},
    {"n": "Sepak Takraw",       "c": "Malaysia"},
    {"n": "Hurling",            "c": "Irland"},
    {"n": "Pétanque",           "c": "Frankreich"},
    {"n": "Pelota Vasca",       "c": "Spanien"},
    {"n": "Buzkashi",           "c": "Afghanistan"},
    {"n": "Polo",               "c": "Argentinien"},
    {"n": "Vovinam",            "c": "Vietnam"},
    {"n": "Kendo",              "c": "Japan"},
    {"n": "Taekwondo",          "c": "Südkorea"},
    {"n": "Wushu",              "c": "China"},
    {"n": "Pencak Silat",       "c": "Indonesien"},
    {"n": "Curling",            "c": "Schottland"},
    {"n": "Bandy",              "c": "Schweden"},
    {"n": "Pesäpallo",          "c": "Finnland"},
    {"n": "Sambo",              "c": "Russland"},
    {"n": "Yağlı Güreş (Ölringen)","c": "Türkei"},
    {"n": "Naadam-Ringen",      "c": "Mongolei"},
    {"n": "Shinty",             "c": "Schottland"},
    {"n": "Luta Livre",         "c": "Brasilien"},
],

"brettspiele": [
    {"n": "Shogi",             "c": "Japan"},
    {"n": "Yut Nori",          "c": "Südkorea"},
    {"n": "Senet",             "c": "Ägypten"},
    {"n": "Royal Game of Ur",  "c": "Irak"},
    {"n": "Patolli",           "c": "Mexiko"},
    {"n": "Pachisi",           "c": "Indien"},
    {"n": "Oware",             "c": "Ghana"},
    {"n": "Bao",               "c": "Kenia"},
    {"n": "Fanorona",          "c": "Madagaskar"},
    {"n": "Xiangqi",           "c": "China"},
    {"n": "Hnefatafl",         "c": "Norwegen"},
    {"n": "Nine Men's Morris", "c": "Deutschland"},
    {"n": "Alquerque",         "c": "Spanien"},
    {"n": "Shatranj",          "c": "Arabische Welt"},
    {"n": "Tablut",            "c": "Finnland"},
    {"n": "Draughts (Dame)",   "c": "Großbritannien"},
    {"n": "Awale",             "c": "Elfenbeinküste"},
    {"n": "Sugoroku",          "c": "Japan"},
    {"n": "Kriegsspiel",       "c": "Deutschland"},
    {"n": "Ashtapada",         "c": "Indien"},
],

}  # end NEW_DATA

# ─────────────────────────────────────────────────────────────────────────────
# PIN-DATEN — canyons (format: {n, lat, lng})
# ─────────────────────────────────────────────────────────────────────────────

NEW_CANYONS = [
    {"n": "Bryce Canyon",          "lat": 37.63,  "lng": -112.17},
    {"n": "Zion Canyon",           "lat": 37.29,  "lng": -113.03},
    {"n": "Palo Duro Canyon",      "lat": 34.72,  "lng": -101.69},
    {"n": "Black Canyon",          "lat": 38.62,  "lng": -107.72},
    {"n": "Tiger Leaping Gorge",   "lat": 27.21,  "lng": 100.01},
    {"n": "Blyde River Canyon",    "lat": -24.62, "lng": 30.82},
    {"n": "Vikos-Schlucht",        "lat": 39.87,  "lng": 20.73},
    {"n": "Samaria-Schlucht",      "lat": 35.27,  "lng": 23.91},
    {"n": "Itaimbezinho-Canyon",   "lat": -29.10, "lng": -50.07},
    {"n": "Cotahuasi-Canyon",      "lat": -15.21, "lng": -72.89},
    {"n": "Cheddar Gorge",         "lat": 51.29,  "lng": -2.78},
    {"n": "Gorges du Tarn",        "lat": 44.21,  "lng": 3.12},
    {"n": "Dadès-Schluchten",      "lat": 31.48,  "lng": -5.97},
    {"n": "Siq (Petra)",           "lat": 30.33,  "lng": 35.44},
    {"n": "Indus-Schlucht",        "lat": 35.34,  "lng": 74.84},
    {"n": "Kings Canyon (NT)",     "lat": -24.27, "lng": 131.58},
    {"n": "Somoto Canyon",         "lat": 13.49,  "lng": -86.59},
]

# ─────────────────────────────────────────────────────────────────────────────
# PATCH AUSFÜHREN
# ─────────────────────────────────────────────────────────────────────────────

data = jload(KULTUR)
total_added = 0
report = []

# Match-Modi
for key, new_items in NEW_DATA.items():
    existing = data.get(key, [])
    if not isinstance(existing, list):
        print(f"[SKIP] {key} — nicht plain list, manuell prüfen")
        continue
    before = len(existing)
    # Duplikat-Check über Namen
    existing_names = {it.get("n","").lower() for it in existing}
    to_add = [it for it in new_items if it["n"].lower() not in existing_names]
    data[key] = existing + to_add
    after = len(data[key])
    total_added += (after - before)
    report.append(f"  [OK] {key}: {before} → {after} (+{after-before})")
    print(report[-1])

# Canyon Pin-Modus
can_before = len(data.get("canyons", []))
existing_can = data.get("canyons", [])
existing_can_names = {it.get("n","").lower() for it in existing_can}
new_cans = [it for it in NEW_CANYONS if it["n"].lower() not in existing_can_names]
data["canyons"] = existing_can + new_cans
can_after = len(data["canyons"])
total_added += (can_after - can_before)
report.append(f"  [OK] canyons: {can_before} → {can_after} (+{can_after-can_before})")
print(report[-1])

jsave(KULTUR, data)
print(f"\n✅ kultur.json gespeichert — {total_added} neue Einträge total")

# Summary
print("\n=== ZUSAMMENFASSUNG ===")
for r in report:
    print(r)
