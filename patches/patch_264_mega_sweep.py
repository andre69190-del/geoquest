#!/usr/bin/env python3
"""
patch_264_mega_sweep.py — Phase 264: Mega-Sweep Expansion
Erweitert alle kritisch dünnen Modi auf 40+ Items.

Prioritäten:
  1. tiere_pin: 10 Modi von 7-8 auf 40+ (mit Koordinaten-Dedup-Guard)
  2. archaeologie_match: 11 Low-Count-Modi (14-19) auf 40+
  3. emob_pin / archaeologie_pin / tech_pin / gastro_pin / pflanzen_pin:
     Top-Modi von 20 auf 40+ Items
  4. tiere HL/Match: Pferde + weitere auf 40+

Architektur-Regeln Phase 264+:
  - Pin-Modi: Koordinaten-Dedup-Guard (lat/lng gerundet auf 1 Dezimale)
  - Match-Modi: min. 6-8 einzigartige c-Werte pro Modus
"""

import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")

# ─── Hilfsfunktionen ────────────────────────────────────────────────────────

def load_json(filename):
    path = os.path.join(DATA, filename)
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save_json(filename, data):
    path = os.path.join(DATA, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extend_key(data, key, new_items, name_field="n"):
    """Name-basierte Dedup + Erweiterung."""
    block = data[key]
    existing = block.get("items", []) if isinstance(block, dict) else block
    ex_names = {it.get(name_field, "").lower() for it in existing}
    added = [it for it in new_items if it.get(name_field, "").lower() not in ex_names]
    if isinstance(block, dict):
        block["items"] = existing + added
    else:
        data[key] = existing + added
    return len(added)

def extend_pin_key(data, key, new_items):
    """
    Doppelte Dedup für Pin-Modi:
      1. Name-basiert (case-insensitive)
      2. Koordinaten-basiert (gerundet auf 1 Dezimalstelle → ~11km Raster)
    """
    block = data[key]
    existing = block.get("items", [])
    ex_names  = {it["n"].lower() for it in existing}
    ex_coords = {(round(it["lat"], 1), round(it["lng"], 1)) for it in existing}

    added = []
    for it in new_items:
        name  = it["n"].lower()
        coord = (round(it["lat"], 1), round(it["lng"], 1))
        if name in ex_names or coord in ex_coords:
            continue
        ex_names.add(name)
        ex_coords.add(coord)
        added.append(it)

    block["items"] = existing + added
    return len(added)

# ─── 1. tiere_pin.json ───────────────────────────────────────────────────────

def patch_tiere_pin(data):
    total = 0

    # tiere_bigfive (Big Five Safarigebiete)
    total += extend_pin_key(data, "tiere_bigfive", [
        {"n": "Amboseli National Park (Kenia)", "lat": -2.65, "lng": 37.26},
        {"n": "Chobe National Park (Botswana)", "lat": -18.8, "lng": 24.5},
        {"n": "Hwange National Park (Zimbabwe)", "lat": -18.9, "lng": 26.9},
        {"n": "Etosha National Park (Namibia)", "lat": -18.86, "lng": 16.33},
        {"n": "Okavango Delta (Botswana)", "lat": -19.3, "lng": 23.0},
        {"n": "Ruaha National Park (Tansania)", "lat": -7.65, "lng": 35.0},
        {"n": "Selous Game Reserve (Tansania)", "lat": -9.0, "lng": 37.8},
        {"n": "Kafue National Park (Sambia)", "lat": -14.5, "lng": 25.8},
        {"n": "South Luangwa NP (Sambia)", "lat": -13.0, "lng": 31.8},
        {"n": "Queen Elizabeth NP (Uganda)", "lat": -0.2, "lng": 30.0},
        {"n": "Murchison Falls NP (Uganda)", "lat": 2.28, "lng": 31.65},
        {"n": "Tsavo National Park (Kenia)", "lat": -2.5, "lng": 38.5},
        {"n": "Samburu National Reserve (Kenia)", "lat": 0.6, "lng": 37.53},
        {"n": "Ngorongoro Crater (Tansania)", "lat": -3.18, "lng": 35.49},
        {"n": "Moremi Game Reserve (Botswana)", "lat": -19.1, "lng": 23.6},
        {"n": "Savute (Botswana)", "lat": -18.6, "lng": 24.1},
        {"n": "Hluhluwe-iMfolozi Park (Südafrika)", "lat": -28.1, "lng": 31.9},
        {"n": "Pilanesberg NP (Südafrika)", "lat": -25.25, "lng": 27.08},
        {"n": "Addo Elephant NP (Südafrika)", "lat": -33.4, "lng": 25.7},
        {"n": "Tembe Elephant Park (Südafrika)", "lat": -27.03, "lng": 32.47},
        {"n": "Mikumi National Park (Tansania)", "lat": -7.3, "lng": 36.8},
        {"n": "Tarangire National Park (Tansania)", "lat": -4.0, "lng": 36.0},
        {"n": "Kidepo Valley NP (Uganda)", "lat": 3.9, "lng": 33.8},
        {"n": "Gonarezhou NP (Zimbabwe)", "lat": -21.5, "lng": 31.9},
        {"n": "Greater Limpopo Transfrontier Park", "lat": -23.5, "lng": 31.7},
        {"n": "Bwabwata NP (Namibia/Botswana)", "lat": -18.2, "lng": 23.6},
        {"n": "Liuwa Plain NP (Sambia)", "lat": -14.8, "lng": 22.5},
        {"n": "Niassa Reserve (Mosambik)", "lat": -12.5, "lng": 36.5},
        {"n": "Gorongosa NP (Mosambik)", "lat": -18.7, "lng": 34.2},
        {"n": "Lewa Conservancy (Kenia)", "lat": 0.23, "lng": 37.45},
        {"n": "Maasai Mara Conservancy (Kenia)", "lat": -1.3, "lng": 35.5},
        {"n": "Kalahari Transfrontier Park", "lat": -26.5, "lng": 20.3},
        {"n": "Central Kalahari Game Reserve", "lat": -21.7, "lng": 23.5},
    ])

    # tiere_grosskatzen (Großkatzen-Habitate)
    total += extend_pin_key(data, "tiere_grosskatzen", [
        {"n": "Bengalischer Tiger (Sundarbans)", "lat": 22.0, "lng": 89.2},
        {"n": "Sibirischer Tiger (Bikin-Fluss)", "lat": 46.1, "lng": 134.1},
        {"n": "Sumatra-Tiger (Gunung Leuser)", "lat": 3.7, "lng": 97.5},
        {"n": "Löwe (Tsavo West, Kenia)", "lat": -3.0, "lng": 38.0},
        {"n": "Löwe (Hwange, Zimbabwe)", "lat": -18.85, "lng": 26.85},
        {"n": "Gepard (Serengeti-Ebene)", "lat": -2.0, "lng": 35.0},
        {"n": "Gepard (Etosha-Savanne)", "lat": -19.2, "lng": 15.8},
        {"n": "Leopard (Okavango-Wälder)", "lat": -19.2, "lng": 23.0},
        {"n": "Leopard (Kruger-Lowveld)", "lat": -24.5, "lng": 31.5},
        {"n": "Jaguar (Belize-Regenwald)", "lat": 16.8, "lng": -88.5},
        {"n": "Jaguar (Corcovado NP, Costa Rica)", "lat": 8.5, "lng": -83.5},
        {"n": "Jaguar (Madidi NP, Bolivien)", "lat": -13.5, "lng": -68.0},
        {"n": "Schneeleopard (Khunjerab, Pakistan)", "lat": 36.8, "lng": 75.4},
        {"n": "Schneeleopard (Hemis NP, Indien)", "lat": 33.8, "lng": 77.7},
        {"n": "Schneeleopard (Tian Shan, Kirgisistan)", "lat": 42.0, "lng": 78.0},
        {"n": "Irbis (Altai-Gebirge, Mongolei)", "lat": 48.5, "lng": 88.5},
        {"n": "Nebelparder (Borneo-Regenwald)", "lat": 4.0, "lng": 117.0},
        {"n": "Nebelparder (Sumatra-Bergwald)", "lat": 1.5, "lng": 101.5},
        {"n": "Puma (Patagonien, Chile)", "lat": -50.5, "lng": -73.0},
        {"n": "Puma (Yellowstone, USA)", "lat": 44.5, "lng": -110.3},
        {"n": "Ozelot (Amazon-Becken, Brasilien)", "lat": -5.0, "lng": -65.0},
        {"n": "Ozelot (Yucatán, Mexiko)", "lat": 20.0, "lng": -89.0},
        {"n": "Luchs (Białowieża-Wald, Polen)", "lat": 52.7, "lng": 23.9},
        {"n": "Eurasischer Luchs (Harz, Deutschland)", "lat": 51.7, "lng": 10.5},
        {"n": "Iberischer Luchs (Doñana, Spanien)", "lat": 37.0, "lng": -6.5},
        {"n": "Persischer Leopard (Golestan NP)", "lat": 37.5, "lng": 55.7},
        {"n": "Indischer Leopard (Kabini, Karnataka)", "lat": 11.9, "lng": 76.4},
        {"n": "Afrikanischer Löwe (Kgalagadi, SA)", "lat": -26.4, "lng": 20.6},
        {"n": "Gepard (Maasai Mara, Kenia)", "lat": -1.45, "lng": 35.22},
        {"n": "Sumatranischer Tiger (Kerinci Seblat)", "lat": -1.6, "lng": 101.2},
        {"n": "Jaguar (Pantanal Nord, Brasilien)", "lat": -16.0, "lng": -56.5},
        {"n": "Nordamerikanischer Puma (Banff, Kanada)", "lat": 51.5, "lng": -116.1},
    ])

    # tiere_invasiv (Invasive Arten — Einschleppungsregion)
    total += extend_pin_key(data, "tiere_invasiv", [
        {"n": "Nilbarsch (Viktoriasee)", "lat": -1.0, "lng": 33.0},
        {"n": "Grauhörnchen (Südengland)", "lat": 51.5, "lng": -0.5},
        {"n": "Mink (Schottland)", "lat": 57.5, "lng": -4.0},
        {"n": "Amerikanischer Ochsenfrosch (Europa)", "lat": 44.0, "lng": 2.0},
        {"n": "Karpfen (Mississippi, USA)", "lat": 39.0, "lng": -90.0},
        {"n": "Kuhreiherfrosch (Australien)", "lat": -16.0, "lng": 145.5},
        {"n": "Aga-Kröte (Queensland, Australien)", "lat": -20.0, "lng": 146.0},
        {"n": "Hauskatze (Australien, invasiv)", "lat": -25.0, "lng": 133.0},
        {"n": "Kaninchen (Südaustralien)", "lat": -32.0, "lng": 139.0},
        {"n": "Fuchsratte (Neuseeland)", "lat": -37.5, "lng": 175.5},
        {"n": "Schwarzer Ratten (Galapagos)", "lat": -0.5, "lng": -90.3},
        {"n": "Hauskatze (Galápagos-Inseln)", "lat": -0.9, "lng": -89.6},
        {"n": "Rotfuchs (Tasmanien)", "lat": -42.0, "lng": 146.5},
        {"n": "Amerikanischer Nerz (Schottland)", "lat": 57.0, "lng": -3.5},
        {"n": "Rotwang-Schmuckschildkröte (Südeuropa)", "lat": 40.0, "lng": 3.0},
        {"n": "Gelbbauchunke (Apennin)", "lat": 43.5, "lng": 11.0},
        {"n": "Taiwanischer Mungo (Japan)", "lat": 26.2, "lng": 127.7},
        {"n": "Springbock-Mungo (Hawaii)", "lat": 21.3, "lng": -157.8},
        {"n": "Asiatische Hornisse (Frankreich)", "lat": 46.0, "lng": 1.5},
        {"n": "Tigermücke (Oberitalien)", "lat": 44.5, "lng": 11.3},
        {"n": "Staudenlupine (Skandinavien)", "lat": 62.0, "lng": 10.0},
        {"n": "Japanischer Staudenknöterich (Rheintal)", "lat": 50.5, "lng": 7.0},
        {"n": "Harlekinkäfer (Belgien)", "lat": 50.8, "lng": 4.3},
        {"n": "Braunmarmorierte Stinkwanze (USA)", "lat": 40.5, "lng": -75.5},
        {"n": "Nilkrokodil (Everglades, USA)", "lat": 25.5, "lng": -80.7},
        {"n": "Boa constrictor (Florida Keys)", "lat": 25.0, "lng": -80.5},
        {"n": "Goldfisch (Colorado River, USA)", "lat": 36.0, "lng": -114.0},
        {"n": "Zebrafisch (Großer Salzsee, USA)", "lat": 41.2, "lng": -112.5},
        {"n": "Wandermuschel (Schwarzes Meer)", "lat": 45.0, "lng": 31.0},
        {"n": "Amerikanischer Biber (Feuerland)", "lat": -54.5, "lng": -68.5},
        {"n": "Hausschaf (Subantarktische Inseln)", "lat": -49.5, "lng": 69.5},
        {"n": "Maulwurfsgrille (Azoren)", "lat": 38.7, "lng": -27.2},
    ])

    # tiere_haustiere (Domestizierungsorte)
    total += extend_pin_key(data, "tiere_haustiere", [
        {"n": "Rind (Anatolien, Türkei)", "lat": 38.5, "lng": 36.0},
        {"n": "Schaf (Zagros-Gebirge, Iran)", "lat": 33.5, "lng": 47.5},
        {"n": "Ziege (Zagros-Gebirge, Iran)", "lat": 33.8, "lng": 46.8},
        {"n": "Schwein (Anatolien/China)", "lat": 32.0, "lng": 115.0},
        {"n": "Huhn (Südostasien)", "lat": 20.0, "lng": 102.0},
        {"n": "Ente (China, Südostasien)", "lat": 25.0, "lng": 108.0},
        {"n": "Kamel (Arabische Halbinsel)", "lat": 23.0, "lng": 45.0},
        {"n": "Dromedar (Arabien/Nordafrika)", "lat": 25.0, "lng": 50.0},
        {"n": "Lama (Anden, Peru)", "lat": -14.0, "lng": -75.0},
        {"n": "Alpaka (Andes, Peru)", "lat": -13.5, "lng": -76.0},
        {"n": "Jak (Tibetisches Hochland)", "lat": 32.0, "lng": 90.0},
        {"n": "Büffel (Südostasien, Indus)", "lat": 28.0, "lng": 73.0},
        {"n": "Rentier (Sibirien, Nordskandinavien)", "lat": 65.0, "lng": 87.0},
        {"n": "Esel (Nordostafrika)", "lat": 15.0, "lng": 38.0},
        {"n": "Maultier (Mediterranraum)", "lat": 38.0, "lng": 22.0},
        {"n": "Truthahn (Mexiko, Mesoamerika)", "lat": 19.0, "lng": -99.5},
        {"n": "Meerschweinchen (Anden, Ecuador)", "lat": -1.5, "lng": -78.5},
        {"n": "Kaninchen (Iberische Halbinsel)", "lat": 40.5, "lng": -3.5},
        {"n": "Taube (Naher Osten)", "lat": 32.0, "lng": 36.0},
        {"n": "Gans (Europa/Ägypten)", "lat": 31.0, "lng": 30.0},
        {"n": "Honigbiene (Naher Osten)", "lat": 33.0, "lng": 37.0},
        {"n": "Seidenraupe (China, Gelbes Meer)", "lat": 32.0, "lng": 118.0},
        {"n": "Goldfisch (China, Song-Dynastie)", "lat": 30.3, "lng": 120.2},
        {"n": "Pute (Südwestmexiko)", "lat": 17.0, "lng": -96.7},
        {"n": "Biene (Anatolien)", "lat": 39.0, "lng": 33.0},
        {"n": "Strauß (Südafrika, Oudtshoorn)", "lat": -33.6, "lng": 22.2},
        {"n": "Lachsforelle (Atlantik-Aquakultur, Norwegen)", "lat": 62.0, "lng": 6.0},
        {"n": "Tilapia (Niltal, Ägypten)", "lat": 25.5, "lng": 32.0},
        {"n": "Hauskanarienvogel (Kanarische Inseln)", "lat": 28.5, "lng": -16.2},
        {"n": "Hausmaus (Orient, Mesopotamien)", "lat": 34.0, "lng": 43.0},
        {"n": "Wellensittich (Australien → Europa)", "lat": 22.0, "lng": 130.0},
        {"n": "Stör (Kaspisches Meer, Aquakultur)", "lat": 42.0, "lng": 52.0},
    ])

    # tiere_primaten (Primaten-Habitate)
    total += extend_pin_key(data, "tiere_primaten", [
        {"n": "Westlicher Flachlandgorilla (Kamerun)", "lat": 4.0, "lng": 11.5},
        {"n": "Bonobo (Demokratische Republik Kongo)", "lat": -2.5, "lng": 23.5},
        {"n": "Sumatra-Orang-Utan (Leuser-Ökosystem)", "lat": 3.2, "lng": 97.8},
        {"n": "Siamang (Malaysia-Hochland)", "lat": 4.5, "lng": 103.0},
        {"n": "Weißhand-Gibbon (Nordthailand)", "lat": 18.5, "lng": 99.5},
        {"n": "Javaneraffe (Java, Indonesien)", "lat": -7.0, "lng": 110.0},
        {"n": "Rhesusaffe (Nordindien-Gangesebene)", "lat": 26.0, "lng": 81.0},
        {"n": "Pavian (Amboseli, Kenia)", "lat": -2.7, "lng": 37.3},
        {"n": "Mandrill (Lopé NP, Gabun)", "lat": -0.2, "lng": 11.5},
        {"n": "Goldener Stumpfnasenaffe (Sichuan, China)", "lat": 31.0, "lng": 103.0},
        {"n": "Japanischer Makak (Jigokudani, Japan)", "lat": 36.75, "lng": 138.47},
        {"n": "Roter Colobus (Tiwai Island, Sierra Leone)", "lat": 7.5, "lng": -11.3},
        {"n": "Guereza-Colobus (Kilimanjarogebiet)", "lat": -3.1, "lng": 37.4},
        {"n": "Proboscisaffe (Kinabatangan-Fluss)", "lat": 5.4, "lng": 118.1},
        {"n": "Schwarzkopfuakari (Amazonas, Peru)", "lat": -3.5, "lng": -73.0},
        {"n": "Brüllaffe (Tikal NP, Guatemala)", "lat": 17.2, "lng": -89.6},
        {"n": "Weißbüschelaffe (Mata Atlântica, Brasilien)", "lat": -8.0, "lng": -35.0},
        {"n": "Klammeraffe (Corcovado NP, Costa Rica)", "lat": 8.5, "lng": -83.5},
        {"n": "Totenkopfäffchen (Surinam-Regenwald)", "lat": 5.0, "lng": -55.5},
        {"n": "Loris (Sri Lanka-Bergwald)", "lat": 7.0, "lng": 80.8},
        {"n": "Indri (Nordost-Madagaskar)", "lat": -16.5, "lng": 49.3},
        {"n": "Aye-Aye (Mananara, Madagaskar)", "lat": -16.2, "lng": 49.7},
        {"n": "Nashorn-Makak (Sulawesi, Indonesien)", "lat": -1.0, "lng": 123.0},
        {"n": "Diademmeerkatze (Uganda-Wald)", "lat": 0.5, "lng": 32.0},
        {"n": "Hamadryas-Pavian (Äthiopien-Hochland)", "lat": 9.0, "lng": 39.0},
        {"n": "Gelada-Pavian (Semien Mountains)", "lat": 13.2, "lng": 38.5},
        {"n": "Berberaffe (Marokko-Atlas)", "lat": 33.5, "lng": -5.0},
        {"n": "Drill (Bioko-Insel, Äquatorialguinea)", "lat": 3.6, "lng": 8.7},
        {"n": "Anubis-Pavian (Murchison Falls NP)", "lat": 2.3, "lng": 31.6},
        {"n": "Kapuzineraffe (Amazônia NP, Brasilien)", "lat": -4.5, "lng": -62.0},
        {"n": "Bärenmakak (Arunachal Pradesh, Indien)", "lat": 27.5, "lng": 93.5},
        {"n": "Zwerggalago (Westkenia)", "lat": 0.5, "lng": 35.0},
    ])

    # tiere_hai (Hai-Hotspots weltweit)
    total += extend_pin_key(data, "tiere_hai", [
        {"n": "Bullenhai (Zambezi-Mündung, Mosambik)", "lat": -18.8, "lng": 36.0},
        {"n": "Hammerhai (Cocos Island, Costa Rica)", "lat": 5.55, "lng": -87.07},
        {"n": "Zitronenhai (Bimini, Bahamas)", "lat": 25.7, "lng": -79.3},
        {"n": "Riffhai (Great Barrier Reef, Australien)", "lat": -18.3, "lng": 147.7},
        {"n": "Schwarzspitzenhai (Malediven)", "lat": 4.2, "lng": 73.5},
        {"n": "Weißspitzenhai (Rotes Meer, Ägypten)", "lat": 24.0, "lng": 37.0},
        {"n": "Schalotthai (Kalimantan, Indonesien)", "lat": 0.5, "lng": 117.0},
        {"n": "Ammenhai (Florida-Schlüssel, USA)", "lat": 24.7, "lng": -81.3},
        {"n": "Katzenhai (Mittelmeer, Sardinien)", "lat": 39.5, "lng": 9.0},
        {"n": "Makohai (Neuseeland, Cook Strait)", "lat": -41.2, "lng": 174.5},
        {"n": "Grauhai (Fakarava-Atoll, Polynesien)", "lat": -16.0, "lng": -145.6},
        {"n": "Riffhai (Palau-Inseln, Mikronesien)", "lat": 7.35, "lng": 134.48},
        {"n": "Weißer Hai (Guadalupe, Mexiko)", "lat": 28.87, "lng": -118.3},
        {"n": "Weißer Hai (Farallon Islands, USA)", "lat": 37.7, "lng": -123.0},
        {"n": "Walhai (Djibouti, Golf von Aden)", "lat": 11.8, "lng": 43.15},
        {"n": "Walhai (Isla Holbox, Mexiko)", "lat": 21.5, "lng": -87.4},
        {"n": "Hammerhai (Wolf Island, Galápagos)", "lat": 1.4, "lng": -91.8},
        {"n": "Tigerhai (Tiger Beach, Bahamas)", "lat": 27.0, "lng": -78.7},
        {"n": "Bullenhai (Brisbane River, Australien)", "lat": -27.5, "lng": 153.0},
        {"n": "Weißer Hai (Dyer Island, Südafrika)", "lat": -34.7, "lng": 19.5},
        {"n": "Seidenhai (Cuba, Karibik)", "lat": 21.5, "lng": -79.5},
        {"n": "Riffhai (Elphinstone, Ägypten)", "lat": 25.0, "lng": 35.2},
        {"n": "Hammerhai (Malpelo, Kolumbien)", "lat": 3.98, "lng": -81.6},
        {"n": "Ammenhai (Komodo NP, Indonesien)", "lat": -8.54, "lng": 119.49},
        {"n": "Makohai (Azoren, Atlantik)", "lat": 38.5, "lng": -28.5},
        {"n": "Brauner Hai (Nordnordsee)", "lat": 58.5, "lng": 1.5},
        {"n": "Hornhai (Baja California, Mexiko)", "lat": 26.0, "lng": -111.5},
        {"n": "Teppichhai (Queensland, Australien)", "lat": -24.5, "lng": 151.5},
        {"n": "Stierkopfhai (Oahu, Hawaii)", "lat": 21.4, "lng": -158.0},
        {"n": "Schwarzspitzenhai (Mozambique-Kanal)", "lat": -15.0, "lng": 41.0},
        {"n": "Weißer Hai (Neptune Islands, Australien)", "lat": -35.3, "lng": 136.1},
        {"n": "Riffhai (Tubbataha NP, Philippinen)", "lat": 8.95, "lng": 120.0},
    ])

    # tiere_baeren (Bären-Habitate)
    total += extend_pin_key(data, "tiere_baeren", [
        {"n": "Braunbär (Kamtschatka, Russland)", "lat": 52.5, "lng": 160.0},
        {"n": "Braunbär (Bialowieza Primärwald, Polen)", "lat": 52.7, "lng": 23.9},
        {"n": "Europäischer Braunbär (Cantabrien, Spanien)", "lat": 43.1, "lng": -5.5},
        {"n": "Amerikanischer Schwarzbär (Appalachian Trail)", "lat": 37.5, "lng": -81.0},
        {"n": "Grizzly (Katmai NP, Alaska)", "lat": 58.7, "lng": -154.9},
        {"n": "Eisbär (Hudson Bay, Kanada)", "lat": 63.0, "lng": -88.0},
        {"n": "Malaiischer Sonnenbär (Danum Valley, Borneo)", "lat": 5.02, "lng": 117.8},
        {"n": "Lippenbär (Panna NP, Indien)", "lat": 24.7, "lng": 80.0},
        {"n": "Andenbär (Manu NP, Peru)", "lat": -11.9, "lng": -71.3},
        {"n": "Eisbär (Franz-Josef-Land)", "lat": 80.0, "lng": 55.0},
        {"n": "Eisbär (Wrangelinsel, Sibirien)", "lat": 71.0, "lng": -178.5},
        {"n": "Grizzly (Brooks Range, Alaska)", "lat": 68.0, "lng": -156.0},
        {"n": "Amerikanischer Schwarzbär (Smoky Mountains, USA)", "lat": 35.6, "lng": -83.5},
        {"n": "Grizzly (Glacier NP, Montana)", "lat": 48.7, "lng": -113.8},
        {"n": "Andenbär (Sangay NP, Ecuador)", "lat": -2.0, "lng": -78.0},
        {"n": "Andenbär (Cotacachi-Cayapas, Ecuador)", "lat": 0.3, "lng": -78.8},
        {"n": "Sonnenbär (Kinabalu NP, Borneo)", "lat": 6.0, "lng": 116.5},
        {"n": "Lippenbär (Tadoba NP, Maharashtra)", "lat": 20.3, "lng": 79.3},
        {"n": "Braunbär (Trentino, Italien)", "lat": 46.2, "lng": 11.2},
        {"n": "Braunbär (Karpaten, Rumänien)", "lat": 45.5, "lng": 25.5},
        {"n": "Braunbär (Bayerischer Wald)", "lat": 48.9, "lng": 13.4},
        {"n": "Großer Panda (Wolong NP, Sichuan)", "lat": 31.0, "lng": 102.9},
        {"n": "Großer Panda (Bifengxia, Sichuan)", "lat": 30.1, "lng": 103.1},
        {"n": "Eisbär (Barentsee, Norwegen)", "lat": 76.5, "lng": 22.0},
        {"n": "Grizzly (Denali NP, Alaska)", "lat": 63.5, "lng": -150.8},
        {"n": "Amerikanischer Schwarzbär (Yosemite NP)", "lat": 37.8, "lng": -119.6},
        {"n": "Malaiischer Sonnenbär (Sabah, Borneo)", "lat": 4.5, "lng": 116.5},
        {"n": "Lippenbär (Sri Lanka Hochland)", "lat": 7.5, "lng": 80.7},
        {"n": "Andenbär (Bosque de Polylepis, Bolivien)", "lat": -16.5, "lng": -67.8},
        {"n": "Eisbär (Nunavut, Kanada)", "lat": 68.0, "lng": -85.0},
        {"n": "Braunbär (Selous, Schweden)", "lat": 62.0, "lng": 15.5},
        {"n": "Grizzly (British Columbia, Kanada)", "lat": 55.0, "lng": -127.5},
    ])

    # tiere_vogelzug (Vogelzug-Rastplätze & Routen)
    total += extend_pin_key(data, "tiere_vogelzug", [
        {"n": "Doñana NP (Südspanien Überwinterung)", "lat": 37.0, "lng": -6.3},
        {"n": "Point Pelee (Großer-Seen-Zugvogel, Kanada)", "lat": 41.96, "lng": -82.52},
        {"n": "Hawk Mountain (Pennsylvanien, USA)", "lat": 40.6, "lng": -75.9},
        {"n": "Cape May (USA Greifvogelzug)", "lat": 38.93, "lng": -74.9},
        {"n": "Falsterbo (Schweden Herbstzug)", "lat": 55.38, "lng": 12.83},
        {"n": "Gibraltar Straße (Zugvogelengpass)", "lat": 36.15, "lng": -5.35},
        {"n": "Messina Straße (Sicilien-Engpass)", "lat": 38.2, "lng": 15.6},
        {"n": "Hongkong (Ostasiatischer Flyway)", "lat": 22.3, "lng": 114.2},
        {"n": "Chilika Lake (Indien Wintergäste)", "lat": 19.7, "lng": 85.3},
        {"n": "Bharatpur (Keoladeo NP, Indien)", "lat": 27.15, "lng": 77.5},
        {"n": "Tungabhadra (Zugvögel Deccan, Indien)", "lat": 15.3, "lng": 76.3},
        {"n": "Banc d'Arguin (Mauretanien Wattenmeer)", "lat": 19.5, "lng": -16.5},
        {"n": "Manambolo-Delta (Madagaskar Rastplatz)", "lat": -19.5, "lng": 44.0},
        {"n": "Djoudj NP (Senegal Delta)", "lat": 16.5, "lng": -16.2},
        {"n": "Coto Doñana (Zugvogel-Rastplatz Spanien)", "lat": 37.1, "lng": -6.4},
        {"n": "Bodensee (Zugvogel-Rastplatz Mitteleuropa)", "lat": 47.7, "lng": 9.3},
        {"n": "Neusiedler See (Zugvogel Österreich)", "lat": 47.8, "lng": 16.8},
        {"n": "Prespa-See (Griechenland Überwinterung)", "lat": 40.8, "lng": 21.0},
        {"n": "Walvis Bay (Namibia Küstenzug)", "lat": -22.96, "lng": 14.52},
        {"n": "Patagonia Salt Lake (Chile Flamingo)", "lat": -23.5, "lng": -68.0},
        {"n": "James Bay (Kanada Arktiszug)", "lat": 53.5, "lng": -80.5},
        {"n": "Copper River Delta (Alaska Schilfsänger)", "lat": 60.5, "lng": -145.0},
        {"n": "Izumi (Japan Kranich-Überwinterung)", "lat": 32.1, "lng": 130.4},
        {"n": "Bhigwan (Maharashtra Flamingo)", "lat": 18.3, "lng": 74.9},
        {"n": "Sivash-See (Ukraine Zugvogel)", "lat": 45.8, "lng": 34.5},
        {"n": "Chabarovsk (Sibirischer Kranichzug)", "lat": 48.5, "lng": 135.1},
        {"n": "Merzouga (Marokko Sahara-Zugvögel)", "lat": 31.1, "lng": -4.0},
        {"n": "Ecuador (Kolibri-Zugachse Anden)", "lat": -1.5, "lng": -78.5},
        {"n": "Chittagong-Küste (Bangladesh Delta)", "lat": 22.3, "lng": 91.8},
        {"n": "Lake Natron (Tansania Flamingo)", "lat": -2.4, "lng": 36.1},
        {"n": "Laguna de Términos (Mexiko Zugvogel)", "lat": 18.7, "lng": -91.5},
        {"n": "Prince Edward Island (Kanada Herbst)", "lat": 46.5, "lng": -63.5},
    ])

    # tiere_endemisch (Endemische Tierarten — Herkunftsregion)
    total += extend_pin_key(data, "tiere_endemisch", [
        {"n": "Axolotl (Xochimilco, Mexiko)", "lat": 19.26, "lng": -99.1},
        {"n": "Quetzal (Guatemala Cloud Forest)", "lat": 14.8, "lng": -90.7},
        {"n": "Kakapo (Fiordland, Neuseeland)", "lat": -45.4, "lng": 167.6},
        {"n": "Tuatara (Stephens Island, NZ)", "lat": -40.67, "lng": 174.0},
        {"n": "Wombat (Tasmanien, Australien)", "lat": -42.0, "lng": 147.0},
        {"n": "Schnabeltier (Queenslandflüsse, Australien)", "lat": -27.5, "lng": 153.0},
        {"n": "Echidna (Südaustralien)", "lat": -34.0, "lng": 140.5},
        {"n": "Tasmanischer Teufel (Tasmanien)", "lat": -42.5, "lng": 146.5},
        {"n": "Humboldt-Pinguin (Punta Tombo, Argentinien)", "lat": -44.0, "lng": -65.3},
        {"n": "Galapagos-Pinguin (Fernandina, Ecuador)", "lat": -0.35, "lng": -91.55},
        {"n": "Galapagos-Leguan (Fernandina-Insel)", "lat": -0.45, "lng": -91.6},
        {"n": "Galapagos-Schildkröte (Santa Cruz-Insel)", "lat": -0.57, "lng": -90.55},
        {"n": "Tapir (Borneo-Urwald)", "lat": 4.5, "lng": 117.0},
        {"n": "Okapia (Ituri-Urwald, DRK)", "lat": 1.5, "lng": 27.5},
        {"n": "Bongo (Aberdare NP, Kenia)", "lat": -0.5, "lng": 36.6},
        {"n": "Markhor (Kaschmir-Gebirge)", "lat": 34.0, "lng": 74.0},
        {"n": "Sitatunga (Okavango-Sumpf, Botswana)", "lat": -19.0, "lng": 23.2},
        {"n": "Klippspringer (Drakensberg, SA)", "lat": -30.0, "lng": 29.5},
        {"n": "Nashorn-Chamäleon (Kamerunhochland)", "lat": 5.9, "lng": 10.2},
        {"n": "Aye-Aye (Ostküste Madagaskar)", "lat": -18.9, "lng": 48.2},
        {"n": "Fossa (Kirindy Wald, Madagaskar)", "lat": -20.1, "lng": 44.6},
        {"n": "Babirusa (Sulawesi, Indonesien)", "lat": -1.5, "lng": 120.0},
        {"n": "Hirscheber (Beringei, DRK)", "lat": -1.0, "lng": 28.8},
        {"n": "Saiga-Antilope (Kazachstanische Steppe)", "lat": 48.5, "lng": 63.0},
        {"n": "Vicuña (Atacamahochland, Chile)", "lat": -23.5, "lng": -67.5},
        {"n": "Solenodon (Haiti-Bergwald)", "lat": 19.0, "lng": -72.3},
        {"n": "Karibik-Dugong (Belize Barrier Reef)", "lat": 16.8, "lng": -88.0},
        {"n": "Dugong (Shark Bay, Australien)", "lat": -25.5, "lng": 113.8},
        {"n": "Indischer Einhorn-Nashorn (Kaziranga NP)", "lat": 26.6, "lng": 93.15},
        {"n": "Japanisches Riesensalamander (Hiroshima)", "lat": 34.5, "lng": 132.5},
        {"n": "Komodo-Waran (Komodo-Insel)", "lat": -8.55, "lng": 119.45},
        {"n": "Stump-Tail Macaque (Assam, Indien)", "lat": 26.5, "lng": 92.5},
    ])

    # tiere_nationaltier_pin (Nationaltier → Land)
    total += extend_pin_key(data, "tiere_nationaltier_pin", [
        {"n": "Weißkopfseeadler (USA)", "lat": 40.0, "lng": -100.0},
        {"n": "Kondor (Argentinien)", "lat": -34.0, "lng": -64.0},
        {"n": "Jaguar (Mexiko)", "lat": 23.0, "lng": -102.0},
        {"n": "Quetzal (Guatemala)", "lat": 15.5, "lng": -90.2},
        {"n": "Tapir (Malaysia)", "lat": 4.0, "lng": 109.5},
        {"n": "Komodo-Waran (Indonesien)", "lat": -5.0, "lng": 120.0},
        {"n": "Gaur (Indien, Nationaltier)", "lat": 21.0, "lng": 80.0},
        {"n": "Binturong (Philippinen)", "lat": 12.8, "lng": 122.0},
        {"n": "Emu (Australien)", "lat": -25.0, "lng": 133.0},
        {"n": "Kiwi (Neuseeland)", "lat": -40.9, "lng": 174.9},
        {"n": "Biber (Kanada)", "lat": 56.0, "lng": -96.0},
        {"n": "Grizzlybär (USA, Kalifornien)", "lat": 37.0, "lng": -120.0},
        {"n": "Stier (Spanien)", "lat": 40.4, "lng": -3.7},
        {"n": "Hahn (Frankreich)", "lat": 46.2, "lng": 2.2},
        {"n": "Bär (Russland)", "lat": 60.0, "lng": 100.0},
        {"n": "Elch (Schweden)", "lat": 62.0, "lng": 16.0},
        {"n": "Fuchs (Wales)", "lat": 52.1, "lng": -3.8},
        {"n": "Einhorn (Schottland)", "lat": 56.5, "lng": -4.0},
        {"n": "Hirsch (Schottland)", "lat": 57.1, "lng": -4.2},
        {"n": "Löwe (England)", "lat": 52.0, "lng": -1.5},
        {"n": "Chamäleon (Madagaskar)", "lat": -20.0, "lng": 47.0},
        {"n": "Phönix-Vogel (China)", "lat": 35.0, "lng": 104.0},
        {"n": "Panda (China)", "lat": 30.0, "lng": 104.0},
        {"n": "Springbok (Südafrika)", "lat": -29.0, "lng": 25.0},
        {"n": "Schimmel-Pferd (Deutschland)", "lat": 51.0, "lng": 10.0},
        {"n": "Wisent (Polen)", "lat": 52.2, "lng": 20.0},
        {"n": "Adler (Deutschland)", "lat": 51.2, "lng": 10.5},
        {"n": "Vogel Strauß (Algerien)", "lat": 28.0, "lng": 2.5},
        {"n": "Berberlöwe (Marokko)", "lat": 31.8, "lng": -7.1},
        {"n": "Phönix-Adler (Ägypten)", "lat": 26.0, "lng": 30.0},
        {"n": "Oryx (Oman)", "lat": 23.5, "lng": 57.5},
        {"n": "Falke (Qatar/UAE)", "lat": 25.3, "lng": 51.5},
    ])

    return total


# ─── 2. archaeologie_match.json — Low-Count Modi ────────────────────────────

def patch_archaeologie_match(data):
    total = 0

    # epochen (17 → 40+)
    total += extend_key(data, "epochen", [
        {"n": "Çatalhöyük", "c": "Jungsteinzeit"},
        {"n": "Göbekli Tepe", "c": "Steinzeit"},
        {"n": "Stonehenge", "c": "Jungsteinzeit"},
        {"n": "Knossos", "c": "Bronzezeit"},
        {"n": "Mykene", "c": "Bronzezeit"},
        {"n": "Troja", "c": "Bronzezeit"},
        {"n": "Uruk (Mesopotamien)", "c": "Frühbronzezeit"},
        {"n": "Memphis (Ägypten)", "c": "Frühbronzezeit"},
        {"n": "Mohenjo-daro", "c": "Bronzezeit"},
        {"n": "Teotihuacán", "c": "Antike"},
        {"n": "Tiwanaku", "c": "Antike"},
        {"n": "Angkor Wat", "c": "Mittelalter"},
        {"n": "Machu Picchu", "c": "Spätmittelalter"},
        {"n": "Chichen Itza", "c": "Mittelalter"},
        {"n": "Mesa Verde", "c": "Mittelalter"},
        {"n": "Cahokia", "c": "Mittelalter"},
        {"n": "Pompeji", "c": "Antike"},
        {"n": "Skara Brae", "c": "Jungsteinzeit"},
        {"n": "Altamira (Höhle)", "c": "Steinzeit"},
        {"n": "Lascaux (Höhle)", "c": "Steinzeit"},
        {"n": "Chauvet-Höhle", "c": "Altsteinzeit"},
        {"n": "Solutrée", "c": "Altsteinzeit"},
        {"n": "Grotte de Font-de-Gaume", "c": "Altsteinzeit"},
        {"n": "Jericho (Tell es-Sultan)", "c": "Jungsteinzeit"},
    ])

    # archaeologen (18 → 40+)
    total += extend_key(data, "archaeologen", [
        {"n": "Machu Picchu (1911)", "c": "Hiram Bingham"},
        {"n": "Pompeji (Ausgrabung 1748)", "c": "Karl Jakob Weber"},
        {"n": "Nabatäa/Petra", "c": "Johann Ludwig Burckhardt"},
        {"n": "Mesopotamien-Forschung", "c": "Leonard Woolley"},
        {"n": "Ausgrabung Knossos", "c": "Arthur Evans"},
        {"n": "Stonehenge (Forschung)", "c": "William Stukeley"},
        {"n": "Ausgrabung Jericho", "c": "Kathleen Kenyon"},
        {"n": "Harappa-Ausgrabung", "c": "Daya Ram Sahni"},
        {"n": "Chichen Itza Forschung", "c": "Edward Thompson"},
        {"n": "Çatalhöyük Ausgrabung", "c": "James Mellaart"},
        {"n": "Angkor (erster Bericht)", "c": "Henri Mouhot"},
        {"n": "Nabatäa/Petra Ausgrabung", "c": "Diana Kirkbride"},
        {"n": "Skara Brae (Ausgrabung)", "c": "Gordon Childe"},
        {"n": "Göbekli Tepe Ausgrabung", "c": "Klaus Schmidt"},
        {"n": "Fundort Lascaux", "c": "Marcel Ravidat"},
        {"n": "Mesa Verde (Ausgrabung)", "c": "Gustaf Nordenskiöld"},
        {"n": "Minos-Tempel (Forschung)", "c": "Minos Kalokairinos"},
        {"n": "Elam-Zivilisation (Susa)", "c": "Jacques de Morgan"},
        {"n": "Tempel des Hephaistos Athen", "c": "William Bell Dinsmoor"},
        {"n": "Amarna-Ausgrabungen", "c": "Flinders Petrie"},
        {"n": "Tell Halaf Ausgrabungen", "c": "Max von Oppenheim"},
        {"n": "Avebury Forschung", "c": "John Aubrey"},
    ])

    # goetter (16 → 40+)
    total += extend_key(data, "goetter", [
        {"n": "Ra", "c": "Ägypten"},
        {"n": "Horus", "c": "Ägypten"},
        {"n": "Isis", "c": "Ägypten"},
        {"n": "Anubis", "c": "Ägypten"},
        {"n": "Thoth", "c": "Ägypten"},
        {"n": "Zeus", "c": "Griechenland"},
        {"n": "Apollo", "c": "Griechenland"},
        {"n": "Athene", "c": "Griechenland"},
        {"n": "Poseidon", "c": "Griechenland"},
        {"n": "Artemis", "c": "Griechenland"},
        {"n": "Jupiter", "c": "Rom"},
        {"n": "Mars", "c": "Rom"},
        {"n": "Minerva", "c": "Rom"},
        {"n": "Venus", "c": "Rom"},
        {"n": "Enlil", "c": "Mesopotamien"},
        {"n": "Anu", "c": "Mesopotamien"},
        {"n": "Inanna", "c": "Mesopotamien"},
        {"n": "Shamash", "c": "Mesopotamien"},
        {"n": "Teshub", "c": "Hethitisch"},
        {"n": "Arinna", "c": "Hethitisch"},
        {"n": "Tlaloc", "c": "Azteken"},
        {"n": "Quetzalcoatl", "c": "Azteken"},
        {"n": "Huitzilopochtli", "c": "Azteken"},
        {"n": "Inti", "c": "Inka"},
        {"n": "Pachamama", "c": "Inka"},
        {"n": "Perun", "c": "Slawisch"},
        {"n": "Veles", "c": "Slawisch"},
        {"n": "Loki", "c": "Nordisch"},
        {"n": "Thor", "c": "Nordisch"},
        {"n": "Odin", "c": "Nordisch"},
    ])

    # museen (16 → 40+)
    total += extend_key(data, "museen", [
        {"n": "Terrakottaarmee", "c": "Xi'an"},
        {"n": "Nefertiti-Büste (Original)", "c": "Berlin"},
        {"n": "Elgin Marbles", "c": "London"},
        {"n": "Venus von Milo", "c": "Paris"},
        {"n": "Tutanchamun-Maske", "c": "Kairo"},
        {"n": "Laokoon-Gruppe", "c": "Rom"},
        {"n": "Nike von Samothrake", "c": "Paris"},
        {"n": "Pergamon-Altar", "c": "Berlin"},
        {"n": "Hammurabi-Stele", "c": "Paris"},
        {"n": "Samarra-Keramik", "c": "Baghdad"},
        {"n": "Benin-Bronzen", "c": "London"},
        {"n": "Olmekenkopf (Riesen)", "c": "Mexiko-Stadt"},
        {"n": "Machu Picchu-Funde", "c": "Cusco"},
        {"n": "Inka-Sonnenscheibe", "c": "Lima"},
        {"n": "Tollund-Mann", "c": "Kopenhagen"},
        {"n": "Ötzis Ausrüstung", "c": "Bozen"},
        {"n": "Lindow Man", "c": "London"},
        {"n": "Gundestrup-Kessel", "c": "Kopenhagen"},
        {"n": "Nebra-Himmelsscheibe", "c": "Halle"},
        {"n": "Goldener Hut von Schifferstadt", "c": "Speyer"},
        {"n": "Mschatta-Fassade", "c": "Berlin"},
        {"n": "Megiddo-Elfenbein", "c": "Jerusalem"},
        {"n": "Koh-i-Noor (Diamant)", "c": "London"},
        {"n": "Phaistos-Scheibe", "c": "Heraklion"},
    ])

    # wikinger (16 → 40+)
    total += extend_key(data, "wikinger", [
        {"n": "Oseberg-Schiff", "c": "Norwegen"},
        {"n": "Gokstad-Schiff", "c": "Norwegen"},
        {"n": "Lindisfarne (Überfall 793)", "c": "England"},
        {"n": "Noirmoutier (Überfall 799)", "c": "Frankreich"},
        {"n": "Hedeby (Handelszentrum)", "c": "Deutschland"},
        {"n": "Ribe (älteste Stadt)", "c": "Dänemark"},
        {"n": "Birka (Handelszentrum)", "c": "Schweden"},
        {"n": "Trelleborg (Ringburg)", "c": "Dänemark"},
        {"n": "Jelling-Runensteine", "c": "Dänemark"},
        {"n": "Reykjavík (Gründung 874)", "c": "Island"},
        {"n": "Vinland-Siedlung", "c": "Kanada"},
        {"n": "Grönland-Siedlung", "c": "Grönland"},
        {"n": "Staraja Ladoga (Nowgorod)", "c": "Russland"},
        {"n": "Kyjiw (Wikingergründung)", "c": "Ukraine"},
        {"n": "Paris-Belagerung 885", "c": "Frankreich"},
        {"n": "Konstantinopel (Wäringerttrade)", "c": "Türkei"},
        {"n": "Jorvik/York (Wikingersiedlung)", "c": "England"},
        {"n": "Dublin (Gründung ca. 841)", "c": "Irland"},
        {"n": "Danegeld (England)", "c": "England"},
        {"n": "Danelaw (Gebiet)", "c": "England"},
        {"n": "Normandie-Gründung 911", "c": "Frankreich"},
        {"n": "Shetland-Inseln (Siedlung)", "c": "Schottland"},
        {"n": "Isle of Man (Wikinger)", "c": "Isle of Man"},
        {"n": "Sizilien (Normannen)", "c": "Italien"},
    ])

    # indus_tal (14 → 40+)
    total += extend_key(data, "indus_tal", [
        {"n": "Rakhigarhi", "c": "Indien"},
        {"n": "Dholavira", "c": "Indien"},
        {"n": "Ganweriwala", "c": "Pakistan"},
        {"n": "Lothal", "c": "Indien"},
        {"n": "Kalibangan", "c": "Indien"},
        {"n": "Surkotada", "c": "Indien"},
        {"n": "Banawali", "c": "Indien"},
        {"n": "Chanhudaro", "c": "Pakistan"},
        {"n": "Amri", "c": "Pakistan"},
        {"n": "Kot Diji", "c": "Pakistan"},
        {"n": "Balakot", "c": "Pakistan"},
        {"n": "Sutkagan Dor", "c": "Pakistan"},
        {"n": "Shortugai", "c": "Afghanistan"},
        {"n": "Desalpur", "c": "Indien"},
        {"n": "Diamabad", "c": "Indien"},
        {"n": "Manda (Akhnoor)", "c": "Indien"},
        {"n": "Mitathal", "c": "Indien"},
        {"n": "Sindhu-Desha (Konzept)", "c": "Pakistan"},
        {"n": "Nausharo", "c": "Pakistan"},
        {"n": "Mehrgarh (Vorläuferkultur)", "c": "Pakistan"},
        {"n": "Kot Bala", "c": "Pakistan"},
        {"n": "Allahdino", "c": "Pakistan"},
        {"n": "Judeirjo-daro", "c": "Pakistan"},
        {"n": "Rangpur", "c": "Indien"},
        {"n": "Kunal", "c": "Indien"},
        {"n": "Farmana", "c": "Indien"},
    ])

    return total


# ─── 3. emob_pin.json (Auswahl: Top-Modi 20 → 40+) ──────────────────────────

def patch_emob_pin(data):
    total = 0

    # gigafactories (20 → 40+)
    total += extend_pin_key(data, "gigafactories", [
        {"n": "Tesla Gigafactory Nevada", "lat": 39.53, "lng": -118.98},
        {"n": "Tesla Gigafactory Shanghai", "lat": 31.02, "lng": 121.47},
        {"n": "Tesla Gigafactory Berlin (Grünheide)", "lat": 52.37, "lng": 13.79},
        {"n": "Tesla Gigafactory Texas (Austin)", "lat": 30.22, "lng": -97.62},
        {"n": "CATL Ningde (Hauptwerk)", "lat": 26.65, "lng": 119.55},
        {"n": "CATL Sichuan", "lat": 30.7, "lng": 104.1},
        {"n": "CATL Deutschland (Erfurt)", "lat": 50.97, "lng": 11.03},
        {"n": "BYD Shenzhen Hauptwerk", "lat": 22.55, "lng": 114.1},
        {"n": "LG Energy Solution Polen (Wrocław)", "lat": 51.2, "lng": 16.9},
        {"n": "Samsung SDI Ungarn (Göd)", "lat": 47.68, "lng": 19.14},
        {"n": "SK On Ungarn (Komárom)", "lat": 47.74, "lng": 18.12},
        {"n": "Northvolt Sverige (Skellefteå)", "lat": 64.75, "lng": 20.95},
        {"n": "Northvolt Deutschland (Heide)", "lat": 54.19, "lng": 9.1},
        {"n": "Freyr Norway (Mo i Rana)", "lat": 66.3, "lng": 14.1},
        {"n": "Envision AESC UK (Sunderland)", "lat": 54.9, "lng": -1.4},
        {"n": "SVOLT Deutschland (Überherrn)", "lat": 49.25, "lng": 6.71},
        {"n": "QuantumScape San José USA", "lat": 37.33, "lng": -121.89},
        {"n": "Solid Power Louisville, USA", "lat": 39.77, "lng": -104.99},
        {"n": "Factorial Energy Massachusetts, USA", "lat": 42.5, "lng": -71.5},
        {"n": "AESC Tennessee USA (Smyrna)", "lat": 35.98, "lng": -86.52},
    ])

    # ladeparks (20 → 40+)
    total += extend_pin_key(data, "ladeparks", [
        {"n": "Supercharger Hub Amsterdam", "lat": 52.37, "lng": 4.9},
        {"n": "Fastned Rotterdam", "lat": 51.92, "lng": 4.48},
        {"n": "Ionity München", "lat": 48.14, "lng": 11.58},
        {"n": "Ionity Berlin", "lat": 52.52, "lng": 13.40},
        {"n": "Ionity Frankfurt Hub", "lat": 50.11, "lng": 8.68},
        {"n": "ChargePoint Hub San Francisco", "lat": 37.78, "lng": -122.42},
        {"n": "EVgo Hub Los Angeles", "lat": 34.05, "lng": -118.24},
        {"n": "Blink Network Chicago", "lat": 41.88, "lng": -87.63},
        {"n": "State Grid Beijing Fast Charge", "lat": 39.91, "lng": 116.39},
        {"n": "TELD Shenzhen Schnelllader", "lat": 22.54, "lng": 114.06},
        {"n": "Volkswagen HPC Hamburg", "lat": 53.55, "lng": 9.99},
        {"n": "Shell Recharge Köln", "lat": 50.94, "lng": 6.96},
        {"n": "APCOA Stuttgart Parkhaus EV", "lat": 48.78, "lng": 9.18},
        {"n": "BP Pulse Birmingham Hub", "lat": 52.49, "lng": -1.9},
        {"n": "Pod Point London Fleet", "lat": 51.5, "lng": -0.12},
        {"n": "Mer Charging Oslo Hub", "lat": 59.91, "lng": 10.74},
        {"n": "Recharge Stockholm", "lat": 59.33, "lng": 18.07},
        {"n": "Greenwheels Den Haag", "lat": 52.08, "lng": 4.31},
        {"n": "Plugsurfing Madrid", "lat": 40.42, "lng": -3.7},
        {"n": "Enel X Roma Hub", "lat": 41.89, "lng": 12.49},
    ])

    return total


# ─── 4. gastro_pin.json (Auswahl: Top-Modi 20 → 40+) ────────────────────────

def patch_gastro_pin(data):
    total = 0

    # nationalgerichte — Pinnable locations (Herkunftsorte)
    total += extend_pin_key(data, "nationalgerichte", [
        {"n": "Wiener Schnitzel (Wien, Österreich)", "lat": 48.21, "lng": 16.37},
        {"n": "Paella (Valencia, Spanien)", "lat": 39.47, "lng": -0.38},
        {"n": "Pad Thai (Bangkok, Thailand)", "lat": 13.75, "lng": 100.52},
        {"n": "Kimchi (Seoul, Südkorea)", "lat": 37.57, "lng": 126.98},
        {"n": "Pho (Hanoi, Vietnam)", "lat": 21.03, "lng": 105.85},
        {"n": "Feijoada (Rio de Janeiro, Brasilien)", "lat": -22.91, "lng": -43.17},
        {"n": "Jerk Chicken (Jamaika)", "lat": 18.1, "lng": -77.3},
        {"n": "Borscht (Kyjiw, Ukraine)", "lat": 50.45, "lng": 30.52},
        {"n": "Moussaka (Athen, Griechenland)", "lat": 37.98, "lng": 23.73},
        {"n": "Shakshuka (Tunis, Tunesien)", "lat": 36.82, "lng": 10.17},
        {"n": "Bunny Chow (Durban, Südafrika)", "lat": -29.85, "lng": 31.0},
        {"n": "Jollof Rice (Dakar, Senegal)", "lat": 14.69, "lng": -17.44},
        {"n": "Tagine (Marrakesch, Marokko)", "lat": 31.63, "lng": -7.99},
        {"n": "Mezze (Beirut, Libanon)", "lat": 33.89, "lng": 35.5},
        {"n": "Biryani (Hyderabad, Indien)", "lat": 17.38, "lng": 78.47},
        {"n": "Dal Makhani (Neu-Delhi, Indien)", "lat": 28.61, "lng": 77.21},
        {"n": "Khachapuri (Tiflis, Georgien)", "lat": 41.69, "lng": 44.83},
        {"n": "Pierogi (Krakau, Polen)", "lat": 50.06, "lng": 19.94},
        {"n": "Boeuf Bourguignon (Dijon, Frankreich)", "lat": 47.32, "lng": 5.04},
        {"n": "Cassoulet (Carcassonne, Frankreich)", "lat": 43.21, "lng": 2.35},
    ])

    # brauereien (20 → 40+)
    total += extend_pin_key(data, "brauereien", [
        {"n": "Weihenstephaner (Freising, Bayern)", "lat": 48.4, "lng": 11.74},
        {"n": "Hofbräuhaus (München)", "lat": 48.14, "lng": 11.58},
        {"n": "Paulaner Brauerei (München)", "lat": 48.12, "lng": 11.56},
        {"n": "Guinness Storehouse (Dublin)", "lat": 53.34, "lng": -6.29},
        {"n": "Heineken Stammhaus (Amsterdam)", "lat": 52.36, "lng": 4.89},
        {"n": "Stella Artois (Leuven, Belgien)", "lat": 50.88, "lng": 4.7},
        {"n": "Chimay Abbaye (Belgien)", "lat": 50.06, "lng": 4.32},
        {"n": "Rochefort Abbaye (Belgien)", "lat": 50.16, "lng": 5.22},
        {"n": "Duvel Moortgat (Breendonk)", "lat": 51.06, "lng": 4.34},
        {"n": "Carlsberg (Kopenhagen)", "lat": 55.66, "lng": 12.54},
        {"n": "Tuborg (Hellerup, Dänemark)", "lat": 55.73, "lng": 12.59},
        {"n": "Pilsner Urquell (Pilsen, Tschechien)", "lat": 49.75, "lng": 13.38},
        {"n": "Budvar (České Budějovice)", "lat": 48.97, "lng": 14.47},
        {"n": "Kozel (Velké Popovice, Tschechien)", "lat": 49.93, "lng": 14.62},
        {"n": "Corona (Mexiko-Stadt)", "lat": 19.43, "lng": -99.13},
        {"n": "Modelo (Mexico City)", "lat": 19.44, "lng": -99.2},
        {"n": "Asahi Brauerei (Osaka)", "lat": 34.7, "lng": 135.5},
        {"n": "Sapporo (Sapporo, Hokkaido)", "lat": 43.06, "lng": 141.35},
        {"n": "Tsingtao (Qingdao, China)", "lat": 36.07, "lng": 120.38},
        {"n": "Kingfisher (Bangalore, Indien)", "lat": 12.97, "lng": 77.59},
    ])

    return total


# ─── 5. archaeologie_pin.json (Auswahl: Top-Modi 20 → 40+) ──────────────────

def patch_archaeologie_pin(data):
    total = 0

    # artefakte (Herkunftsorte bedeutender Artefakte)
    total += extend_pin_key(data, "artefakte", [
        {"n": "Löwenmensch (Ulm, Deutschland)", "lat": 48.4, "lng": 10.0},
        {"n": "Venus von Willendorf (Österreich)", "lat": 48.3, "lng": 15.42},
        {"n": "Nefertiti-Büste Fundort (Amarna)", "lat": 27.65, "lng": 30.9},
        {"n": "Tutanchamun-Grab (Luxor)", "lat": 25.74, "lng": 32.6},
        {"n": "Stein von Rosette (Fundort Rashid)", "lat": 31.4, "lng": 30.42},
        {"n": "Dendera-Zodiak Fundort (Dendera)", "lat": 26.14, "lng": 32.67},
        {"n": "Terrakottaarmee Fundort (Xi'an)", "lat": 34.38, "lng": 109.27},
        {"n": "Ötzi-Fundort (Ötztal-Alpen)", "lat": 46.77, "lng": 10.85},
        {"n": "Lindow Man Fundort (Cheshire)", "lat": 53.37, "lng": -2.13},
        {"n": "Tollund-Mann (Jütland, Dänemark)", "lat": 56.0, "lng": 9.4},
        {"n": "Çatalhöyük (Konya, Türkei)", "lat": 37.67, "lng": 32.82},
        {"n": "Nebra Himmelsscheibe (Mittelberg, D.)", "lat": 51.32, "lng": 11.49},
        {"n": "Troia Goldschatz Fundort", "lat": 39.96, "lng": 26.24},
        {"n": "Nimrud Ivories (Irak)", "lat": 36.1, "lng": 43.32},
        {"n": "Sutton Hoo Helm (Suffolk, UK)", "lat": 52.09, "lng": 1.34},
        {"n": "Gundestrup-Kessel Fundort (Dänemark)", "lat": 57.1, "lng": 9.1},
        {"n": "Lascaux-Höhle (Dordogne, Frankreich)", "lat": 45.05, "lng": 1.07},
        {"n": "Altamira-Höhle (Kantabrien, Spanien)", "lat": 43.38, "lng": -4.12},
        {"n": "Chauvet-Höhle (Ardèche, Frankreich)", "lat": 44.38, "lng": 4.42},
        {"n": "Vogelherd-Höhle (Lone Valley, D.)", "lat": 48.56, "lng": 10.15},
    ])

    # megalithanlagen (20 → 40+)
    total += extend_pin_key(data, "megalithanlagen", [
        {"n": "Avebury (Wiltshire, UK)", "lat": 51.43, "lng": -1.85},
        {"n": "Carnac (Bretagne, Frankreich)", "lat": 47.58, "lng": -3.08},
        {"n": "Newgrange (Irland)", "lat": 53.69, "lng": -6.48},
        {"n": "Knowth (Boyne Valley, Irland)", "lat": 53.7, "lng": -6.49},
        {"n": "Callanish (Outer Hebrides, UK)", "lat": 58.2, "lng": -6.74},
        {"n": "Maes Howe (Orkney, UK)", "lat": 58.99, "lng": -3.19},
        {"n": "Göbekli Tepe (Şanlıurfa, Türkei)", "lat": 37.22, "lng": 38.92},
        {"n": "Skara Brae (Orkney, UK)", "lat": 59.04, "lng": -3.34},
        {"n": "Laos Steinerne Krüge (Plain of Jars)", "lat": 19.45, "lng": 103.15},
        {"n": "Baalbek Megalithen (Libanon)", "lat": 34.0, "lng": 36.22},
        {"n": "Rujm el-Hiri (Golan, Israel)", "lat": 32.9, "lng": 35.81},
        {"n": "Mnajdra (Malta)", "lat": 35.82, "lng": 14.44},
        {"n": "Ħaġar Qim (Malta)", "lat": 35.83, "lng": 14.44},
        {"n": "Tarxien (Malta)", "lat": 35.87, "lng": 14.51},
        {"n": "Poulnabrone (Clare, Irland)", "lat": 53.05, "lng": -9.14},
        {"n": "Cromlechs de Moussan (Portugal)", "lat": 38.57, "lng": -7.97},
        {"n": "Senegambian Stone Circles", "lat": 13.67, "lng": -15.55},
        {"n": "Mzora (Marokko)", "lat": 35.08, "lng": -5.78},
        {"n": "Anta de Menga (Andalusien)", "lat": 37.02, "lng": -4.55},
        {"n": "Dolmen de Menga (Antequera)", "lat": 37.02, "lng": -4.56},
    ])

    return total


# ─── 6. pflanzen_pin.json (Auswahl: Top-Modi 20 → 40+) ──────────────────────

def patch_pflanzen_pin(data):
    total = 0

    # nutzpflanzen (22 → 40+)
    total += extend_pin_key(data, "nutzpflanzen", [
        {"n": "Weizen (Fruchtbarer Halbmond, Türkei)", "lat": 37.0, "lng": 38.5},
        {"n": "Mais (Tehuacán, Mexiko)", "lat": 18.46, "lng": -97.39},
        {"n": "Kartoffel (Titicaca-Hochland, Peru)", "lat": -15.8, "lng": -70.0},
        {"n": "Tomaten (Mesoamerika, Mexiko)", "lat": 19.5, "lng": -99.0},
        {"n": "Chili (Bolivien/Peru-Grenzregion)", "lat": -17.0, "lng": -64.0},
        {"n": "Süßkartoffel (Papua-Neuguinea)", "lat": -6.5, "lng": 145.0},
        {"n": "Quinoa (Altiplano, Bolivien)", "lat": -16.5, "lng": -68.2},
        {"n": "Banane (Papua-Neuguinea)", "lat": -5.5, "lng": 145.5},
        {"n": "Zuckerrohr (Papua-Neuguinea/Indien)", "lat": 22.5, "lng": 89.0},
        {"n": "Kaffeepflanze (Kaffa, Äthiopien)", "lat": 7.3, "lng": 36.2},
        {"n": "Kakao (Maya-Tiefland, Guatemala)", "lat": 15.4, "lng": -89.5},
        {"n": "Tabak (Yucatan, Mexiko)", "lat": 20.0, "lng": -89.0},
        {"n": "Baumwolle (Indus-Tal, Pakistan)", "lat": 27.3, "lng": 68.5},
        {"n": "Soja (Mandschurei, China)", "lat": 45.0, "lng": 125.0},
        {"n": "Erdnuss (Westafrika/Südamerika)", "lat": -15.0, "lng": -55.0},
        {"n": "Ananas (Paranágebiet, Brasilien)", "lat": -25.0, "lng": -51.0},
        {"n": "Kokosnuss (Südostasien)", "lat": 5.0, "lng": 105.0},
        {"n": "Maniok (Amazonasbecken)", "lat": -5.0, "lng": -60.0},
    ])

    # botanische_gaerten (20 → 40+)
    total += extend_pin_key(data, "botanische_gaerten", [
        {"n": "Kew Gardens (London)", "lat": 51.48, "lng": -0.3},
        {"n": "Royal Botanic Garden Edinburgh", "lat": 55.97, "lng": -3.21},
        {"n": "Jardin des Plantes (Paris)", "lat": 48.84, "lng": 2.36},
        {"n": "Berlin Botanischer Garten", "lat": 52.45, "lng": 13.3},
        {"n": "Botanischer Garten Wien", "lat": 48.19, "lng": 16.33},
        {"n": "Padua Botanischer Garten (ältester)", "lat": 45.4, "lng": 11.88},
        {"n": "Leiden Hortus Botanicus", "lat": 52.16, "lng": 4.48},
        {"n": "Singapore Botanic Gardens", "lat": 1.31, "lng": 103.82},
        {"n": "Descanso Gardens (Los Angeles)", "lat": 34.2, "lng": -118.2},
        {"n": "Brooklyn Botanic Garden (New York)", "lat": 40.67, "lng": -73.96},
        {"n": "Missouri Botanical Garden (St. Louis)", "lat": 38.61, "lng": -90.26},
        {"n": "Royal Botanic Gardens Melbourne", "lat": -37.83, "lng": 144.98},
        {"n": "National Botanical Garden (Pretoria)", "lat": -25.74, "lng": 28.27},
        {"n": "Jardín Botánico Madrid", "lat": 40.41, "lng": -3.69},
        {"n": "Ботанічний сад (Kyjiw)", "lat": 50.43, "lng": 30.56},
        {"n": "Komarov Botanical Institute (St. Petersburg)", "lat": 59.97, "lng": 30.3},
        {"n": "Jardim Botânico Rio de Janeiro", "lat": -22.97, "lng": -43.22},
        {"n": "Botanischer Garten Zürich", "lat": 47.36, "lng": 8.56},
        {"n": "Jardin Exotique Monaco", "lat": 43.73, "lng": 7.41},
        {"n": "Descanso National Arboretum (Washington)", "lat": 38.89, "lng": -77.07},
    ])

    return total


# ─── 7. tech_pin.json (Auswahl: Top-Modi 20 → 40+) ──────────────────────────

def patch_tech_pin(data):
    total = 0

    # rechenzentren (20 → 40+)
    total += extend_pin_key(data, "rechenzentren", [
        {"n": "Google Data Center The Dalles, Oregon", "lat": 45.6, "lng": -121.17},
        {"n": "Amazon AWS Frankfurt", "lat": 50.12, "lng": 8.68},
        {"n": "Microsoft Azure Dublin", "lat": 53.33, "lng": -6.25},
        {"n": "Facebook Luleå Data Center", "lat": 65.57, "lng": 22.15},
        {"n": "Apple Data Center Maiden, NC", "lat": 35.57, "lng": -81.39},
        {"n": "Google Data Center Hamina, Finland", "lat": 60.57, "lng": 27.2},
        {"n": "Microsoft Azure Singapore", "lat": 1.35, "lng": 103.82},
        {"n": "Alibaba Cloud Hangzhou", "lat": 30.27, "lng": 120.15},
        {"n": "Tencent Cloud Beijing", "lat": 39.91, "lng": 116.39},
        {"n": "Baidu Data Center Yangquan", "lat": 37.86, "lng": 113.58},
        {"n": "Equinix LD4 Slough UK", "lat": 51.51, "lng": -0.58},
        {"n": "Interxion AMS1 Amsterdam", "lat": 52.38, "lng": 4.89},
        {"n": "CyrusOne Dallas, Texas", "lat": 32.78, "lng": -96.8},
        {"n": "Digital Realty Atlanta, GA", "lat": 33.75, "lng": -84.39},
        {"n": "NTT Osaka Data Center", "lat": 34.68, "lng": 135.5},
        {"n": "T-Systems München RZ", "lat": 48.14, "lng": 11.58},
        {"n": "Lefdal Mine Datacenter, Norwegen", "lat": 61.87, "lng": 5.28},
        {"n": "EcoDataCenter Falun, Schweden", "lat": 60.6, "lng": 15.6},
        {"n": "Verne Global Keflavik, Island", "lat": 63.99, "lng": -22.61},
        {"n": "Green Mountain Rennesøy, Norwegen", "lat": 59.15, "lng": 5.73},
    ])

    # supercomputer (20 → 40+)
    total += extend_pin_key(data, "supercomputer", [
        {"n": "Frontier (Oak Ridge, USA)", "lat": 35.93, "lng": -84.31},
        {"n": "Aurora (Argonne, USA)", "lat": 41.72, "lng": -87.98},
        {"n": "Eagle (Microsoft Azure)", "lat": 47.63, "lng": -122.12},
        {"n": "HPC6 (Eni, Italien)", "lat": 44.3, "lng": 11.7},
        {"n": "Tianhe-3 (Guangzhou, China)", "lat": 23.13, "lng": 113.26},
        {"n": "Wuwei (Beijing, China)", "lat": 39.91, "lng": 116.39},
        {"n": "Selene (NVIDIA, USA)", "lat": 40.43, "lng": -79.96},
        {"n": "Perlmutter (Berkeley Lab, USA)", "lat": 37.88, "lng": -122.25},
        {"n": "Lumi (Kajaani, Finnland)", "lat": 64.22, "lng": 27.73},
        {"n": "Leonardo (Bologna, Italien)", "lat": 44.5, "lng": 11.34},
        {"n": "Fugaku (RIKEN, Kobe Japan)", "lat": 34.66, "lng": 135.21},
        {"n": "Summit (Oak Ridge, USA)", "lat": 35.92, "lng": -84.31},
        {"n": "MareNostrum 5 (Barcelona)", "lat": 41.39, "lng": 2.11},
        {"n": "JUWELS (Jülich, Deutschland)", "lat": 50.91, "lng": 6.41},
        {"n": "Hawk (Stuttgart, Deutschland)", "lat": 48.78, "lng": 9.18},
        {"n": "Shaheen (KAUST, Saudi-Arabien)", "lat": 22.32, "lng": 39.1},
        {"n": "Tianhe-2A (Guangzhou, China)", "lat": 23.16, "lng": 113.26},
        {"n": "Sunway TaihuLight (Wuxi, China)", "lat": 31.57, "lng": 120.29},
        {"n": "K Computer (Kobe, Japan)", "lat": 34.69, "lng": 135.22},
        {"n": "Mira (Argonne, USA)", "lat": 41.72, "lng": -87.98},
    ])

    return total


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("\n🚀 patch_264_mega_sweep.py — Phase 264")
    print("   Koordinaten-Dedup Guard aktiv (11km Raster)\n")

    grand_total = 0

    # 1. tiere_pin.json
    print("🦁 tiere_pin.json — 10 Modi erweitern...")
    d = load_json("tiere_pin.json")
    n = patch_tiere_pin(d)
    save_json("tiere_pin.json", d)
    print(f"   +{n} neue Pin-Einträge (tiere_pin)")
    grand_total += n

    # 2. archaeologie_match.json
    print("🏛️  archaeologie_match.json — Low-Count Modi...")
    d = load_json("archaeologie_match.json")
    n = patch_archaeologie_match(d)
    save_json("archaeologie_match.json", d)
    print(f"   +{n} neue Match-Einträge (archaeologie)")
    grand_total += n

    # 3. emob_pin.json
    print("⚡ emob_pin.json — gigafactories + ladeparks...")
    d = load_json("emob_pin.json")
    n = patch_emob_pin(d)
    save_json("emob_pin.json", d)
    print(f"   +{n} neue Pin-Einträge (emob)")
    grand_total += n

    # 4. gastro_pin.json
    print("🍽️  gastro_pin.json — nationalgerichte + brauereien...")
    d = load_json("gastro_pin.json")
    n = patch_gastro_pin(d)
    save_json("gastro_pin.json", d)
    print(f"   +{n} neue Pin-Einträge (gastro)")
    grand_total += n

    # 5. archaeologie_pin.json
    print("⛏️  archaeologie_pin.json — artefakte + megalithen...")
    d = load_json("archaeologie_pin.json")
    n = patch_archaeologie_pin(d)
    save_json("archaeologie_pin.json", d)
    print(f"   +{n} neue Pin-Einträge (archaeologie)")
    grand_total += n

    # 6. pflanzen_pin.json
    print("🌿 pflanzen_pin.json — nutzpflanzen + botanische_gaerten...")
    d = load_json("pflanzen_pin.json")
    n = patch_pflanzen_pin(d)
    save_json("pflanzen_pin.json", d)
    print(f"   +{n} neue Pin-Einträge (pflanzen)")
    grand_total += n

    # 7. tech_pin.json
    print("💻 tech_pin.json — rechenzentren + supercomputer...")
    d = load_json("tech_pin.json")
    n = patch_tech_pin(d)
    save_json("tech_pin.json", d)
    print(f"   +{n} neue Pin-Einträge (tech)")
    grand_total += n

    print(f"\n✅ patch_264 fertig: +{grand_total} Einträge gesamt")

    # Übersicht der finalen Zählungen
    print("\n📊 Finale Zählungen (Auswahl):")
    checks = [
        ("tiere_pin.json", ["tiere_bigfive","tiere_grosskatzen","tiere_invasiv",
                            "tiere_haustiere","tiere_primaten","tiere_hai","tiere_baeren",
                            "tiere_vogelzug","tiere_endemisch","tiere_nationaltier_pin"]),
        ("archaeologie_match.json", ["epochen","archaeologen","goetter","museen","wikinger","indus_tal"]),
        ("emob_pin.json", ["gigafactories","ladeparks"]),
        ("gastro_pin.json", ["nationalgerichte","brauereien"]),
        ("archaeologie_pin.json", ["artefakte","megalithanlagen"]),
        ("pflanzen_pin.json", ["nutzpflanzen","botanische_gaerten"]),
        ("tech_pin.json", ["rechenzentren","supercomputer"]),
    ]
    for fn, keys in checks:
        d = load_json(fn)
        for key in keys:
            val = d[key]
            items = val.get("items", val) if isinstance(val, dict) else val
            flag = "✓" if len(items) >= 40 else "⚠"
            print(f"  {flag} {key}: {len(items)}")


if __name__ == "__main__":
    main()
