#!/usr/bin/env python3
"""patch_269b_fill_sweep.py — Phase 269b: sweep remaining <30-item categories to 40."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, '..', 'data')

def load(f): 
    with open(os.path.join(DATA, f), encoding='utf-8') as fh: return json.load(fh)
def save(f, d):
    with open(os.path.join(DATA, f), 'w', encoding='utf-8') as fh: json.dump(d, fh, ensure_ascii=False, indent=2)
    print(f'  Saved {f}')

def ext(lst, new_items, key='n'):
    seen = {it[key] for it in lst}
    for it in new_items:
        if it.get(key) not in seen:
            lst.append(it); seen.add(it[key])

def exthl(lst, new_items):
    ext(lst, new_items, key='name')

# ── EMOB_HL missing categories ─────────────────────────────────
print('── emob_hl.json ──')
ehl = load('emob_hl.json')

exthl(ehl['gewicht']['items'], [
    {"name": "Tesla Model 3 Standard Range (2023)", "val": 1757},
    {"name": "Volkswagen ID.3 Pro (58 kWh)", "val": 1772},
    {"name": "BMW i4 eDrive40", "val": 2125},
    {"name": "Audi Q8 e-tron 55 quattro", "val": 2585},
    {"name": "Kia EV9 GT-Line (Long Range)", "val": 2610},
    {"name": "Nissan Ariya e-4ORCE 87 kWh", "val": 2202},
    {"name": "Mercedes EQC 400 4MATIC", "val": 2495},
    {"name": "Polestar 2 Long Range Dual Motor", "val": 2123},
    {"name": "Volvo EX90 Twin Motor", "val": 2748},
    {"name": "Ford F-150 Lightning Lariat (Extended)", "val": 3069},
    {"name": "Rivian R1T Dual Motor", "val": 2906},
    {"name": "Lucid Air Grand Touring", "val": 2154},
    {"name": "BYD Han EV AWD", "val": 2175},
    {"name": "BYD Seal AWD", "val": 2150},
    {"name": "Dacia Spring 65 HP (mini)", "val": 979},
    {"name": "MINI Cooper SE 2. Gen (Aceman)", "val": 1615},
    {"name": "Renault Zoe ZE50", "val": 1502},
    {"name": "Cupra Born 77 kWh", "val": 1843},
    {"name": "Skoda Enyaq iV 80", "val": 2019},
    {"name": "Tesla Cybertruck AWD (geschätzt)", "val": 2995},
])
exthl(ehl['ladezeit_10_80']['items'], [
    {"name": "Tesla Model Y (V3 Supercharger)", "val": 30},
    {"name": "Volkswagen ID.4 GTX (135 kW)", "val": 36},
    {"name": "BMW i4 eDrive40 (205 kW)", "val": 31},
    {"name": "Kia EV6 GT (240 kW, 800V)", "val": 18},
    {"name": "Hyundai Ioniq 6 Long Range (240 kW)", "val": 18},
    {"name": "Hyundai Ioniq 5 Long Range (220 kW)", "val": 18},
    {"name": "Mercedes EQC 400 (110 kW)", "val": 40},
    {"name": "Mercedes EQE 350+ (170 kW)", "val": 32},
    {"name": "Nissan Leaf (CHAdeMO 50 kW)", "val": 50},
    {"name": "Nissan Ariya e-4ORCE (130 kW)", "val": 38},
    {"name": "Renault Zoe ZE50 (50 kW max)", "val": 60},
    {"name": "Polestar 2 Long Range (205 kW)", "val": 28},
    {"name": "Volvo EX90 Twin Motor (250 kW)", "val": 28},
    {"name": "Ford F-150 Lightning (150 kW)", "val": 44},
    {"name": "Rivian R1T (DC Combo 220 kW)", "val": 31},
    {"name": "Lucid Air (CCS 300 kW)", "val": 22},
    {"name": "BYD Han EV (120 kW)", "val": 45},
    {"name": "Dacia Spring (30 kW, AC max)", "val": 75},
    {"name": "MINI Cooper SE (95 kW)", "val": 27},
    {"name": "Tesla Cybertruck AWD (250 kW)", "val": 26},
])
exthl(ehl['drehmoment']['items'], [
    {"name": "Pininfarina Battista", "val": 2340},
    {"name": "Lotus Evija", "val": 1700},
    {"name": "Tesla Model S Plaid (AWD)", "val": 1420},
    {"name": "Porsche Taycan Turbo S (Overboost)", "val": 1050},
    {"name": "Hyundai Ioniq 5 N (N Grin Boost)", "val": 740},
    {"name": "BMW i4 M50 xDrive", "val": 795},
    {"name": "Kia EV6 GT (AWD)", "val": 740},
    {"name": "Mercedes AMG EQE 53 4MATIC+", "val": 858},
    {"name": "Audi RS e-tron GT (Launch Control)", "val": 830},
    {"name": "Ford F-150 Lightning Platinum", "val": 1050},
    {"name": "Rivian R1T Adventure (4 Motoren)", "val": 1231},
    {"name": "Tesla Model Y Performance", "val": 493},
    {"name": "Volkswagen ID. Buzz Long Range GTX", "val": 679},
    {"name": "BYD Seal AWD Performance", "val": 670},
    {"name": "Nio ET7 Dual Motor", "val": 850},
    {"name": "Rimac Nevera (4 Motoren)", "val": 2360},
    {"name": "Dacia Spring (Frontmotor)", "val": 113},
    {"name": "Renault Zoe ZE50 (Frontmotor)", "val": 245},
    {"name": "MINI Cooper SE 2. Gen", "val": 200},
    {"name": "Smart #3 Brabus", "val": 440},
])
exthl(ehl['preis']['items'], [
    {"name": "Dacia Spring 65 HP", "val": 21},
    {"name": "Renault Zoe ZE50 (Basispreis)", "val": 31},
    {"name": "MINI Cooper SE 2. Gen", "val": 38},
    {"name": "Volkswagen ID.3 Pro", "val": 40},
    {"name": "Tesla Model 3 Standard Range", "val": 43},
    {"name": "Hyundai Ioniq 6 Long Range RWD", "val": 47},
    {"name": "Kia EV6 Long Range RWD", "val": 50},
    {"name": "Volkswagen ID.4 GTX", "val": 55},
    {"name": "BMW i4 eDrive40", "val": 59},
    {"name": "Polestar 2 Long Range Dual", "val": 60},
    {"name": "Audi Q4 e-tron 50", "val": 62},
    {"name": "Mercedes EQC 400 4MATIC", "val": 80},
    {"name": "BMW iX xDrive50", "val": 95},
    {"name": "Audi Q8 e-tron 55 quattro", "val": 99},
    {"name": "Porsche Taycan 4S", "val": 112},
    {"name": "Mercedes EQS 450+", "val": 120},
    {"name": "Lucid Air Pure", "val": 80},
    {"name": "Lucid Air Grand Touring", "val": 140},
    {"name": "Rivian R1T Adventure", "val": 75},
    {"name": "Rolls-Royce Spectre (EV)", "val": 420},
])
save('emob_hl.json', ehl)

# ── TECH_HL missing categories ─────────────────────────────────
print('── tech_hl.json ──')
thl = load('tech_hl.json')
exthl(thl['freiheitsgrade']['items'], [
    {"name": "ABB YuMi (kollaborativ, 2×7)", "val": 14},
    {"name": "Fanuc CRX-10iA (cobots)", "val": 6},
    {"name": "Boston Dynamics Spot (Bein je 3)", "val": 12},
    {"name": "NASA Robonaut 2 (Torso)", "val": 42},
    {"name": "Shadow Dexterous Hand", "val": 24},
    {"name": "Menschliche Hand (gesamt)", "val": 27},
    {"name": "Stewart-Plattform (Parallelroboter)", "val": 6},
    {"name": "CNC-Fräsmaschine (3-Achs)", "val": 3},
    {"name": "CNC-Fräsmaschine (5-Achs)", "val": 5},
    {"name": "SCARA-Roboter (Montage)", "val": 4},
    {"name": "Delta-Roboter (Pick-and-Place)", "val": 3},
    {"name": "Industrieroboter KUKA KR 6 R700", "val": 6},
    {"name": "Drohne (quadcopter) translatorisch+rotatorisch", "val": 6},
    {"name": "Auto-Räder (Lenkung+Gaspedal)", "val": 2},
    {"name": "Humanoid Agility Digit (v3)", "val": 30},
    {"name": "Exoskelett Ekso GT (Beine)", "val": 6},
    {"name": "Chirurgischer Roboter Da Vinci Xi", "val": 7},
    {"name": "Flugzeug (klassisch, 6 DOF)", "val": 6},
    {"name": "Universal Robots UR10e", "val": 6},
    {"name": "Menschlicher Arm + Schulter", "val": 7},
])
exthl(thl['tdp']['items'], [
    {"name": "AMD Ryzen 9 9950X", "val": 170},
    {"name": "AMD Ryzen 7 7800X3D (Spielen)", "val": 120},
    {"name": "Intel Core i9-14900K", "val": 125},
    {"name": "Intel Core Ultra 9 285K", "val": 125},
    {"name": "AMD EPYC 9654 (Server)", "val": 360},
    {"name": "NVIDIA H100 SXM5 (GPU)", "val": 700},
    {"name": "AMD Instinct MI300X (GPU)", "val": 750},
    {"name": "Apple M4 Ultra (SoC gesamt)", "val": 90},
    {"name": "Qualcomm Snapdragon X Elite (Laptop)", "val": 45},
    {"name": "NVIDIA RTX 4090 (Vollgas)", "val": 450},
    {"name": "AMD Radeon RX 7900 XTX", "val": 355},
    {"name": "Intel Xeon W9-3595X", "val": 350},
    {"name": "IBM z16 Mainframe (Chip gesamt)", "val": 90},
    {"name": "Fujitsu A64FX (Supercomputer-Chip)", "val": 160},
    {"name": "Raspberry Pi 5", "val": 5},
    {"name": "ESP32-S3 (IoT-Chip)", "val": 0.24},
    {"name": "Arduino Uno R4", "val": 0.2},
    {"name": "Samsung Exynos 2400 (Smartphone)", "val": 8},
    {"name": "Apple A17 Pro (iPhone 15 Pro)", "val": 6},
    {"name": "Intel 8086 (1978, historisch)", "val": 2.0},
])
save('tech_hl.json', thl)

# ── GASTRO_HL missing categories ───────────────────────────────
print('── gastro_hl.json ──')
ghl = load('gastro_hl.json')
exthl(ghl['kerntemperatur']['items'], [
    {"name": "Schweinefleisch (Innen, sicher)", "val": 65},
    {"name": "Hühnerbrust (vollgegart)", "val": 74},
    {"name": "Rindfleisch (rare/blutig)", "val": 52},
    {"name": "Rindfleisch (medium)", "val": 60},
    {"name": "Rindfleisch (well done)", "val": 71},
    {"name": "Lammkeule (medium-rare)", "val": 57},
    {"name": "Fisch (Lachs, gegart)", "val": 63},
    {"name": "Thunfisch-Steak (medium-rare)", "val": 50},
    {"name": "Burger-Patty (Hackfleisch, sicher)", "val": 71},
    {"name": "Ente (Ganzes, vollgegart)", "val": 74},
    {"name": "Kaninchen (vollgegart)", "val": 70},
    {"name": "Temperierungsschokolade (dunkle)", "val": 32},
    {"name": "Karamell-Kochpunkt (Soft Ball)", "val": 115},
    {"name": "Karamell-Kochpunkt (Hard Crack)", "val": 149},
    {"name": "Brotteig Innen (fertig gebacken)", "val": 96},
    {"name": "Gelatine-Schmelze (Blatt)", "val": 35},
    {"name": "Hefeteig (Gäroptimum)", "val": 37},
    {"name": "Sous-vide-Ei (64°C-Ei klassisch)", "val": 64},
    {"name": "Pastellfarbener Käsekuchen (Kern)", "val": 66},
    {"name": "Rehfilet (medium-rare)", "val": 55},
])
exthl(ghl['zubereitungszeit']['items'], [
    {"name": "Instant-Nudeln (Ramen, Beutel)", "val": 3},
    {"name": "Rührei (klassisch, Pfanne)", "val": 5},
    {"name": "Toast (Brotröster)", "val": 2},
    {"name": "Pasta (al dente, gekochtes Wasser)", "val": 8},
    {"name": "Steak (Pfanne, medium)", "val": 12},
    {"name": "Pfannkuchen (Crepe, 1 Stück)", "val": 3},
    {"name": "Grillhähnchen (ganzes, Ofen)", "val": 90},
    {"name": "Pizza (Ofen, selbstgemacht)", "val": 15},
    {"name": "Risotto (Klassisch)", "val": 30},
    {"name": "Boeuf Bourguignon (Schmoren)", "val": 180},
    {"name": "Sauerbraten (Marinierung + Braten)", "val": 5760},
    {"name": "Pulled Pork (Low & Slow, Smoker)", "val": 720},
    {"name": "Linsensuppe (Simmern)", "val": 45},
    {"name": "Croissant (Teig + Backen)", "val": 600},
    {"name": "Crème Brûlée (Kühlzeit inkl.)", "val": 120},
    {"name": "Fondue Bourguignonne (Tischzeit)", "val": 60},
    {"name": "Sous-vide-Brust (Hühnchen, 60°C)", "val": 90},
    {"name": "Baguette (Vorteig + Backen)", "val": 300},
    {"name": "Tiramisù (Kühlzeit eingeschlossen)", "val": 240},
    {"name": "Weichgekochtes Ei (ab kochendem Wasser)", "val": 5},
])
exthl(ghl['wasseranteil']['items'], [
    {"name": "Gurke", "val": 96.7},
    {"name": "Eisbergsalat", "val": 96.0},
    {"name": "Sellerie", "val": 95.4},
    {"name": "Tomaten", "val": 94.5},
    {"name": "Spinat", "val": 91.4},
    {"name": "Brokkoli", "val": 90.7},
    {"name": "Karotten", "val": 88.3},
    {"name": "Apfel", "val": 85.6},
    {"name": "Erdbeeren", "val": 91.0},
    {"name": "Wassermelone", "val": 91.5},
    {"name": "Vollmilch", "val": 87.5},
    {"name": "Hühnerei (frisch, gesamt)", "val": 76.0},
    {"name": "Hühnerbrust (roh)", "val": 74.0},
    {"name": "Rindfleisch (mager, roh)", "val": 71.0},
    {"name": "Lachs (roh)", "val": 68.5},
    {"name": "Hartkäse (Parmesan, gereift)", "val": 29.0},
    {"name": "Honig", "val": 17.0},
    {"name": "Butter", "val": 16.0},
    {"name": "Zucker (Kristall)", "val": 0.1},
    {"name": "Sonnenblumenöl", "val": 0.0},
])
exthl(ghl['prokopf_verbrauch']['items'], [
    {"name": "USA — Fleisch (gesamt)", "val": 128.0},
    {"name": "Australien — Fleisch (gesamt)", "val": 121.0},
    {"name": "Argentinien — Rindfleisch", "val": 55.0},
    {"name": "Deutschland — Bier", "val": 87.0},
    {"name": "Tschechien — Bier (Weltspitze)", "val": 135.0},
    {"name": "Frankreich — Wein", "val": 49.0},
    {"name": "Portugal — Wein", "val": 62.0},
    {"name": "Schweiz — Schokolade (Weltspitze)", "val": 10.3},
    {"name": "Deutschland — Schokolade", "val": 7.9},
    {"name": "Österreich — Kaffee", "val": 7.8},
    {"name": "Finnland — Kaffee (Weltspitze)", "val": 12.2},
    {"name": "Island — Fisch (Weltspitze)", "val": 90.0},
    {"name": "Japan — Meeresfrüchte", "val": 62.0},
    {"name": "China — Schweinefleisch", "val": 38.0},
    {"name": "Indien — Getreide (gesamt)", "val": 143.0},
    {"name": "Brasilien — Zucker", "val": 54.0},
    {"name": "USA — Mais (verarbeitet gesamt)", "val": 121.0},
    {"name": "Norwegen — Lachskonsum", "val": 20.0},
    {"name": "Türkei — Tee (Weltspitze)", "val": 3.2},
    {"name": "Griechenland — Olivenöl", "val": 20.0},
])
save('gastro_hl.json', ghl)

# ── GASTRO_MATCH missing categories ────────────────────────────
print('── gastro_match.json ──')
gm = load('gastro_match.json')
def gext(gm, key, items):
    existing = gm[key].get('items', gm[key]) if isinstance(gm[key], dict) else gm[key]
    ext(existing, items)

gext(gm, 'gewuerzmischungen', [
    {"n": "Garam Masala (Kardamom, Cumin, Koriander…)", "c": "Indien"},
    {"n": "Baharat (Piment, Zimt, Muskat…)", "c": "Arabisch"},
    {"n": "Berbere (Chili, Fenugreek, Kurkuma…)", "c": "Äthiopien"},
    {"n": "Dukkah (Koriander, Sesam, Haselnuss)", "c": "Ägypten"},
    {"n": "Cajun Spice (Paprika, Oregano, Cayenne)", "c": "USA (Louisiana)"},
    {"n": "Old Bay (Sellerie, Paprika, Muskat)", "c": "USA (Maryland)"},
    {"n": "Za'atar (Thymian, Sumach, Sesam)", "c": "Levante"},
    {"n": "Harischa / Harissa (Chili-Paste)", "c": "Nordafrika"},
    {"n": "Quatre Épices (Piment, Muskat, Zimt, Nelke)", "c": "Frankreich"},
    {"n": "Advieh (Rose, Kardamom, Kurkuma)", "c": "Iran"},
    {"n": "Shawarma-Gewürz (Kreuzkümmel, Kurkuma)", "c": "Mittlerer Osten"},
    {"n": "Adobo Seco (Knoblauch, Oregano, Cumin)", "c": "Lateinamerika"},
    {"n": "Lemon Pepper (Zitronenschale, Pfeffer)", "c": "USA"},
    {"n": "Panch Phoron (Fenchel, Bockshornklee, Kreuzkümmel, Kalonji, Schwarzkümmel)", "c": "Bengalen"},
    {"n": "Mole-Basis (Chili, Schokolade, Sesam)", "c": "Mexiko"},
    {"n": "Ras el Hanout (>20 Gewürze)", "c": "Marokko"},
    {"n": "Sichuan-Pfeffer + Sternanis", "c": "China"},
    {"n": "Tandoori-Masala (Kurkuma, Kreuzkümmel, Paprika)", "c": "Indien"},
    {"n": "Furikake (Sesam, Nori, Bonito)", "c": "Japan"},
    {"n": "Chili-Lime Salt (Chili, Limette, Salz)", "c": "Mexiko/USA"},
])
gext(gm, 'kuechengeraete', [
    {"n": "Wok (flacher Boden, Stahl)", "c": "Wokbraten"},
    {"n": "Cast Iron Skillet (Gusseisen)", "c": "Anbraten / Backen"},
    {"n": "Springform (abnehmbar)", "c": "Tortenbacken"},
    {"n": "Mandoline (Gemüse-Hobel)", "c": "Schneiden"},
    {"n": "Mortar & Pestle (Mörser)", "c": "Mörsern"},
    {"n": "Sous-vide-Stick (Zirkulator)", "c": "Sous-vide Garen"},
    {"n": "Dampfgarer (Bambus, Dim Sum)", "c": "Dämpfen"},
    {"n": "Tajine (Tondeckel)", "c": "Schmoren (Nordafrika)"},
    {"n": "Paella-Pfanne (flach, breit)", "c": "Paella"},
    {"n": "Kochtopf mit Dampfventil (Schnellkochtopf)", "c": "Druckkochen"},
    {"n": "Brotbackform (Kastenform)", "c": "Brot backen"},
    {"n": "Thermometer (Fleisch)", "c": "Kerntemperatur messen"},
    {"n": "Tortillapresse (Gusseisen)", "c": "Tortillas formen"},
    {"n": "Crêpe-Pfanne (dünn)", "c": "Crêpes"},
    {"n": "Räucherofen (Holzkohle)", "c": "Räuchern"},
    {"n": "Standmixer (Hochleistungs-)", "c": "Pürieren/Emulgieren"},
    {"n": "Küchenmaschine (KitchenAid)", "c": "Rühren/Kneten"},
    {"n": "Eismaschine (mit Kompressor)", "c": "Eis/Sorbet"},
    {"n": "Nudel-Maschine (Pasta Attachment)", "c": "Pasta ausrollen"},
    {"n": "Vakuumiergerät (Foodsaver)", "c": "Vakuumieren"},
])
gext(gm, 'pasta_formen', [
    {"n": "Rigatoni (kurz, gerillt)", "c": "Tomatensauce"},
    {"n": "Tagliatelle (flach, breit)", "c": "Bolognese"},
    {"n": "Linguine (flach, schmal)", "c": "Meeresfrüchte"},
    {"n": "Orecchiette (Öhrchen)", "c": "Broccoli Rabe"},
    {"n": "Fusilli Lunghi (Spiralen, lang)", "c": "Pesto"},
    {"n": "Farfalle / Schmetterling", "c": "Sahnesauce"},
    {"n": "Gnocchi (Kartoffel-Klößchen)", "c": "Butter + Salbei"},
    {"n": "Cavatappi (Korkenzieher)", "c": "Mac and Cheese"},
    {"n": "Paccheri (riesige Röhren)", "c": "Meeresfrüchte"},
    {"n": "Strozzapreti (verdrehte Würste)", "c": "Fleischsugo"},
    {"n": "Castellane (Muschelform)", "c": "Fleischsauce"},
    {"n": "Trofe (Ligurien, gedreht)", "c": "Pesto Genovese"},
    {"n": "Bigoli (dicker Vollkorn-Strang)", "c": "Sardellen + Zwiebeln"},
    {"n": "Maltagliati (unregelmäßig)", "c": "Wildsugo"},
    {"n": "Pizzoccheri (Buchweizen)", "c": "Valtellina (Käse+Kartoffel)"},
    {"n": "Spaghetti alla Chitarra", "c": "Cacio e Pepe"},
    {"n": "Lasagne (Platten, Schicht)", "c": "Bolognese + Béchamel"},
    {"n": "Orzo / Risoni (reisförmig)", "c": "Suppe"},
    {"n": "Ditalini (kurze Röhrchen)", "c": "Minestrone"},
    {"n": "Trofie con Pesto (Ligurien)", "c": "Pesto"},
])
gext(gm, 'fruehstueck_welt', [
    {"n": "Shakshuka (Eier in Tomaten)", "c": "Israel / Nordafrika"},
    {"n": "Congee (Reisporridge)", "c": "China"},
    {"n": "Dim Sum (Früh-Dim-Sum)", "c": "Hongkong / Guangdong"},
    {"n": "Tamago Kake Gohan (Rohei + Reis)", "c": "Japan"},
    {"n": "Natto Gohan (Sojafrühstück)", "c": "Japan"},
    {"n": "Idli + Sambar (gedämpfte Reiskuchen)", "c": "Indien"},
    {"n": "Dosa (fermentiertes Pfannkuchen)", "c": "Indien (Südindien)"},
    {"n": "Ful Medames (Favabohnen)", "c": "Ägypten"},
    {"n": "Taameya (Bohnenbällchen)", "c": "Ägypten"},
    {"n": "Menemen (Ei + Tomate + Paprika)", "c": "Türkei"},
    {"n": "Pastırma + Sucuk (Wurst, Ei)", "c": "Türkei"},
    {"n": "Börek Sabah (Frühstücksbörek)", "c": "Türkei"},
    {"n": "Açaí-Bowl", "c": "Brasilien"},
    {"n": "Tapioca mit Füllung", "c": "Brasilien"},
    {"n": "Fatteh (Brot + Kichererbsen + Joghurt)", "c": "Libanon"},
    {"n": "Manakish (Thymian-Brot)", "c": "Levante"},
    {"n": "Mahluta (Schaf-Joghurt + Honig)", "c": "Albanien"},
    {"n": "Arepas con Queso", "c": "Kolumbien / Venezuela"},
    {"n": "Huevos Rancheros (Tortilla + Egg)", "c": "Mexiko"},
    {"n": "Champurrado (Maisgetränk, Schokolade)", "c": "Mexiko"},
])
save('gastro_match.json', gm)

# ── GASTRO_PIN missing categories ──────────────────────────────
print('── gastro_pin.json ──')
gpn = load('gastro_pin.json')

def gpext(gpn, key, new_items):
    items = gpn[key].get('items', gpn[key]) if isinstance(gpn[key], dict) else gpn[key]
    seen_names = {it['n'] for it in items}
    seen_coords = {(it['lat'], it['lng']) for it in items}
    for it in new_items:
        c = (it['lat'], it['lng'])
        if it['n'] not in seen_names and c not in seen_coords:
            items.append(it); seen_names.add(it['n']); seen_coords.add(c)

gpext(gpn, 'schokoladen', [
    {"n": "Valrhona Schokoladenfabrik (Tain-l'Hermitage, FR)", "lat": 45.0667, "lng": 4.8500},
    {"n": "Barry Callebaut Fabrik (Lebbeke-Wieze, Belgien)", "lat": 50.9986, "lng": 4.1328},
    {"n": "Lindt Schokoladenmuseum (Köln)", "lat": 50.9247, "lng": 6.9650},
    {"n": "Chocolaterie Marcolini (Brüssel)", "lat": 50.8503, "lng": 4.3517},
    {"n": "Hotel Chocolat Plantage (St. Lucia)", "lat": 13.9094, "lng": -61.0678},
    {"n": "Theo Chocolate (Seattle, WA)", "lat": 47.6627, "lng": -122.3765},
    {"n": "Scharffen Berger (San Francisco)", "lat": 37.7749, "lng": -122.4194},
    {"n": "Original Beans Factory (Niederlande)", "lat": 52.3676, "lng": 4.9041},
    {"n": "Kakao-Plantage Kumasi (Ghana)", "lat": 6.6884, "lng": -1.6244},
    {"n": "Kakao-Hafen Abidjan (Côte d'Ivoire)", "lat": 5.3600, "lng": -4.0083},
    {"n": "Kakao Ursprung Mesoamerika (Chiapas, Mexiko)", "lat": 16.7569, "lng": -93.1292},
    {"n": "Schokoladenmesse Salon du Chocolat (Paris)", "lat": 48.8566, "lng": 2.3522},
    {"n": "Maison Cluizel (Damville, Normandie)", "lat": 49.0000, "lng": 0.9333},
    {"n": "Jacques Torres Chocolate (New York)", "lat": 40.7128, "lng": -74.0060},
    {"n": "Dick Taylor Craft Chocolate (Eureka, CA)", "lat": 40.8021, "lng": -124.1637},
    {"n": "Pacari Chocolate (Quito, Ecuador)", "lat": -0.2299, "lng": -78.5249},
    {"n": "Askinosie Chocolate (Springfield, MO)", "lat": 37.2153, "lng": -93.2982},
    {"n": "Ritter Sport Fabrik (Waldenbuch, BW)", "lat": 48.6297, "lng": 9.1197},
    {"n": "Kakao-Museum (Barcelona)", "lat": 41.3795, "lng": 2.1754},
    {"n": "Ferrero Hauptwerk (Alba, Piemont)", "lat": 44.7003, "lng": 8.0337},
])
gpext(gpn, 'kulinarische_feste', [
    {"n": "Oktoberfest (München)", "lat": 48.1302, "lng": 11.5501},
    {"n": "La Tomatina (Buñol, Spanien)", "lat": 39.4167, "lng": -0.8167},
    {"n": "Lopburi-Affenbankett (Thailand)", "lat": 14.7997, "lng": 100.6531},
    {"n": "Gilroy Garlic Festival (Gilroy, CA)", "lat": 37.0057, "lng": -121.5683},
    {"n": "Taste of Chicago (Chicago, IL)", "lat": 41.8781, "lng": -87.6298},
    {"n": "World Gumbo Cookoff (New Orleans)", "lat": 29.9511, "lng": -90.0715},
    {"n": "Covent Garden Apple Harvest (London)", "lat": 51.5120, "lng": -0.1224},
    {"n": "Truffle Festival Périgueux (Frankreich)", "lat": 45.1840, "lng": 0.7214},
    {"n": "Salon de l'Agriculture (Paris)", "lat": 48.8420, "lng": 2.2897},
    {"n": "Slow Food Salone del Gusto (Turin)", "lat": 45.0703, "lng": 7.6869},
    {"n": "Singapore Food Festival", "lat": 1.2808, "lng": 103.8490},
    {"n": "Thai Food Festival Bangkok (Lumpini)", "lat": 13.7308, "lng": 100.5418},
    {"n": "World Pizza Championship (Neapel)", "lat": 40.8518, "lng": 14.2681},
    {"n": "Sapporo Ramen Show (Japan)", "lat": 43.0642, "lng": 141.3469},
    {"n": "Cannes Film Dinner Festival (Cannes)", "lat": 43.5528, "lng": 7.0174},
    {"n": "Glastonbury Farmhouse Feast (UK)", "lat": 51.1557, "lng": -2.7138},
    {"n": "Brest Oyster Festival (Bretagne)", "lat": 48.3905, "lng": -4.4860},
    {"n": "Madrid Fusión (Gastronomiegipfel)", "lat": 40.4168, "lng": -3.7038},
    {"n": "Albacete Garlic-Saffron Fair (Spanien)", "lat": 38.9954, "lng": -1.8585},
    {"n": "Korea Baphomet Kimchi Festival (Seoul)", "lat": 37.5665, "lng": 126.9780},
])
save('gastro_pin.json', gpn)

# ── PFLANZEN_MATCH missing categories ──────────────────────────
print('── pflanzen_match.json ──')
pm = load('pflanzen_match.json')
def pmext(pm, key, items):
    existing = pm[key].get('items', pm[key]) if isinstance(pm[key], dict) else pm[key]
    ext(existing, items)

pmext(pm, 'gewuerze', [
    {"n": "Safran", "c": "Iran (Khorasan)"},
    {"n": "Schwarzer Pfeffer", "c": "Indien (Kerala)"},
    {"n": "Kardamom", "c": "Guatemala / Indien"},
    {"n": "Vanille (Vanilla planifolia)", "c": "Madagaskar"},
    {"n": "Muskatnuss (Myristica fragrans)", "c": "Indonesien (Banda)"},
    {"n": "Nelke (Syzygium aromaticum)", "c": "Indonesien (Maluku)"},
    {"n": "Kurkuma (Curcuma longa)", "c": "Indien"},
    {"n": "Sternanis", "c": "China / Vietnam"},
    {"n": "Sumach (Rhus coriaria)", "c": "Mittlerer Osten"},
    {"n": "Bockshornklee", "c": "Indien / Nordafrika"},
    {"n": "Fenugreek (Blatt)", "c": "Indien"},
    {"n": "Ajowan (Carum copticum)", "c": "Indien"},
    {"n": "Koriandersamen", "c": "Weltweit"},
    {"n": "Kreuzkümmel (Cuminum cyminum)", "c": "Mittelmeer / Indien"},
    {"n": "Paprika (geräuchert, Pimentón)", "c": "Spanien (La Vera)"},
    {"n": "Chili (Capsicum annuum)", "c": "Mittelamerika"},
    {"n": "Piment (Allspice)", "c": "Jamaika / Karibik"},
    {"n": "Asafoetida (Ferula assa-foetida)", "c": "Iran / Afghanistan"},
])
pmext(pm, 'familien', [
    {"n": "Eiche (Quercus)", "c": "Fagaceae"},
    {"n": "Sonnenblume (Helianthus)", "c": "Asteraceae"},
    {"n": "Minze (Mentha)", "c": "Lamiaceae"},
    {"n": "Tomate (Solanum lycopersicum)", "c": "Solanaceae"},
    {"n": "Orchidee (Orchidaceae)", "c": "Orchidaceae"},
    {"n": "Gras (Poa)", "c": "Poaceae"},
    {"n": "Kaktus (Saguaro)", "c": "Cactaceae"},
    {"n": "Lilie (Lilium)", "c": "Liliaceae"},
    {"n": "Palme (Cocos nucifera)", "c": "Arecaceae"},
    {"n": "Mohn (Papaver somniferum)", "c": "Papaveraceae"},
    {"n": "Hanf (Cannabis sativa)", "c": "Cannabaceae"},
    {"n": "Ahorn (Acer)", "c": "Sapindaceae"},
    {"n": "Farn (Pteridium)", "c": "Dennstaedtiaceae"},
    {"n": "Schachtelhalm (Equisetum)", "c": "Equisetaceae"},
    {"n": "Bambus (Bambusoideae)", "c": "Poaceae"},
    {"n": "Klee (Trifolium)", "c": "Fabaceae"},
    {"n": "Gurke (Cucumis sativus)", "c": "Cucurbitaceae"},
    {"n": "Heidelbeere (Vaccinium)", "c": "Ericaceae"},
])
pmext(pm, 'bluetezeit', [
    {"n": "Heidekraut (Calluna)", "c": "Herbst"},
    {"n": "Akelei (Aquilegia)", "c": "Frühjahr/Frühsommer"},
    {"n": "Chrysantheme", "c": "Herbst"},
    {"n": "Weihnachtsstern (Poinsettia)", "c": "Winter"},
    {"n": "Krokus", "c": "Frühling"},
    {"n": "Forsythie", "c": "Frühling"},
    {"n": "Storch-Schnabel (Geranium)", "c": "Sommer"},
    {"n": "Dahlie", "c": "Sommer/Herbst"},
    {"n": "Primel", "c": "Frühling"},
    {"n": "Pfingstrose (Paeonia)", "c": "Frühsommer"},
    {"n": "Gladiole", "c": "Sommer"},
    {"n": "Narzisse", "c": "Frühling"},
    {"n": "Clematis (großblumig)", "c": "Frühsommer"},
    {"n": "Herbstzeitlose (Colchicum)", "c": "Herbst"},
    {"n": "Winterling (Eranthis)", "c": "Winter"},
    {"n": "Immortelle (Helichrysum)", "c": "Sommer"},
    {"n": "Lavatera (Strauchmalve)", "c": "Sommer"},
    {"n": "Bergenia (Bergenien)", "c": "Frühling"},
])
save('pflanzen_match.json', pm)

# ── TIERE_MATCH missing categories ─────────────────────────────
print('── tiere_match.json ──')
tierm = load('tiere_match.json')
def tmext(tierm, key, items):
    existing = tierm[key].get('items', tierm[key]) if isinstance(tierm[key], dict) else tierm[key]
    ext(existing, items)

tmext(tierm, 'tarnung', [
    {"n": "Sandfarbe + flacher Körper", "c": "Scholle / Plattfisch"},
    {"n": "Schneeweißes Fell im Winter", "c": "Polarfuchs"},
    {"n": "Gelbbraun mit dunklen Flecken", "c": "Leopard"},
    {"n": "Dunkelbraun mit weißen Flecken (Rücken)", "c": "Rehkitz"},
    {"n": "Rindenbraun mit Flechtenmuster", "c": "Birkenbläuling / Rindenspinner"},
    {"n": "Wasserblau-silbern (Flanken)", "c": "Thunfisch (Gegenschattierung)"},
    {"n": "Graubraun mit schwarzen Streifen", "c": "Steinmarder"},
    {"n": "Weißes Winterkleid + braun im Sommer", "c": "Schneehuhn / Ptarmigan"},
    {"n": "Fluoreszentes Grün (tropisch)", "c": "Smaragdeidechse"},
    {"n": "Getigertes Muster (senkrechte Streifen)", "c": "Tiger"},
    {"n": "Weiß-schwarz horizontal (im Gras)", "c": "Zebra"},
    {"n": "Farbwechsel nach 0,5 Sek. (Haut)", "c": "Tintenfisch / Oktopus"},
    {"n": "Transparenter Körper (Tiefseefisch)", "c": "Glaswels (Kryptopterus)"},
    {"n": "Bernsteinfarbig + glänzend (Harz?)", "c": "Goldkäfer (Cassis)"},
    {"n": "Schwarz-weiß-rote Warnfarbe", "c": "Schwarze Witwen-Spinne"},
    {"n": "Braun gemischt (Flügel = Baum)", "c": "Waldkauz"},
    {"n": "Orange-blau (Warnung + Tarnung situativ)", "c": "Pfeilgiftfrosch"},
    {"n": "Sandfarbene Iris + Gesicht", "c": "Kameleon (basale Form)"},
    {"n": "Totholz-Muster (Körperstruktur)", "c": "Totes-Blatt-Schmetterlingsmantis"},
    {"n": "Dunkler Rücken, heller Bauch", "c": "Delfin (Gegenschattierung)"},
])
tmext(tierm, 'ernaehrung', [
    {"n": "Bambus (99% der Nahrung)", "c": "Großer Panda"},
    {"n": "Blätter, Früchte, Rinde", "c": "Gorilla"},
    {"n": "Ausschließlich Nektar + Pollen", "c": "Biene"},
    {"n": "Blut (Hämatophagie)", "c": "Vampirfledermaus"},
    {"n": "Nur Fleisch (Raubtier)", "c": "Orca / Killerwal"},
    {"n": "Plankton + Krill (Filterfressen)", "c": "Bartenwal"},
    {"n": "Aas + Knochen", "c": "Beingeier"},
    {"n": "Insekten + kleine Reptilien", "c": "Chamäleon"},
    {"n": "Fisch + Tintenfisch", "c": "Pinguin"},
    {"n": "Krill allein (Milliarden Krebstiere)", "c": "Blauwal"},
    {"n": "Früchte, Insekten, kleine Wirbeltiere", "c": "Schimpanse"},
    {"n": "Eukalyptusblätter (fast ausschließlich)", "c": "Koala"},
    {"n": "Seegras (Seegrasfluss)", "c": "Seekuh / Dugong"},
    {"n": "Insekten (unter Baumrinde)", "c": "Specht"},
    {"n": "Körnerfresser (Samen + Früchte)", "c": "Haussperling"},
    {"n": "Muscheln, Seeigel, Algen", "c": "Seeotter"},
    {"n": "Ratten + Mäuse (obligater Carnivore)", "c": "Hauskatze (Wildform)"},
    {"n": "Zuckerrohr + Früchte", "c": "Breitmaulnashorn"},
    {"n": "Kleinsäuger + Vögel + Reptilien", "c": "Bussard"},
    {"n": "Totholz (Zelluloseabbau)", "c": "Termite"},
])
tmext(tierm, 'metamorphose', [
    {"n": "Ei → Raupe → Puppe → Falter", "c": "Schmetterling (holometabol)"},
    {"n": "Ei → Larve → Puppe → Imago", "c": "Käfer"},
    {"n": "Ei → Larve → Puppe → Imago", "c": "Fliege"},
    {"n": "Ei → Nymphe → Imago (3 Stadien)", "c": "Heuschrecke (hemimetabol)"},
    {"n": "Ei → Nymphe → Imago", "c": "Libelle"},
    {"n": "Ei → Nymphe → Imago", "c": "Wanze"},
    {"n": "Laich → Kaulquappe → Frosch", "c": "Frosch"},
    {"n": "Ei → Larve (Planula) → Polyp → Meduse", "c": "Qualle"},
    {"n": "Ei → Trochophora → Veliger → Muschel", "c": "Muschel (Bivalve)"},
    {"n": "Ei → Nauplius → Copepoda → Ruderfußkrebs", "c": "Copepode"},
    {"n": "Ei → Ammocoetes (Larve) → Neunauge", "c": "Flussneunauge"},
    {"n": "Ei → Larve → Puppe → Imago (aquatisch)", "c": "Mücke"},
    {"n": "Ei → Pediveliger-Larve → Austern-Spat", "c": "Auster"},
    {"n": "Ei → Bipedinaria-Larve → Seestern", "c": "Seestern"},
    {"n": "Ei → Larve → Puppe → Imago", "c": "Ameise"},
    {"n": "Direktentwicklung (kein Larvenstadium)", "c": "Gecko"},
    {"n": "Larve → Metamorphose → Urodele", "c": "Axolotl (neotisch, bleibt Larve)"},
    {"n": "Ei → Zoea → Megalopa → Krabbe", "c": "Krabbe"},
    {"n": "Laich → Kaulquappe → Molch", "c": "Feuersalamander"},
    {"n": "Ei → Wurm → Geschlechtsreif", "c": "Regenwurm (direkte Entwicklung)"},
])
tmext(tierm, 'sinne', [
    {"n": "Echoortung (Ultraschall-Sonar)", "c": "Fledermaus"},
    {"n": "Seitenlinie (Druckwellen spüren)", "c": "Fisch"},
    {"n": "Elektrorezeptoren (Elektroortung)", "c": "Hai / Rochen"},
    {"n": "Infrarot-Grubenorgan (Wärme)", "c": "Grubenottern (Crotalinae)"},
    {"n": "UV-Sicht (kurzwelliges Licht)", "c": "Biene"},
    {"n": "Polarisiertes Licht wahrnehmen", "c": "Tintenfisch"},
    {"n": "Magnetorezeption (Magnetfeld)", "c": "Zugvogel (Rotkehlchen)"},
    {"n": "Infraschall hören (unter 20 Hz)", "c": "Elefant"},
    {"n": "360°-Sehfeld (Augen seitlich)", "c": "Kaninchen"},
    {"n": "Tetrachromates Sehen (4 Farbrezeptoren)", "c": "Fangschreckenkrebs"},
    {"n": "Monokulares Sehen mit Überlappungszone", "c": "Eule (Stirnaugen)"},
    {"n": "Thermorezeptoren (Körperwärme-Jagd)", "c": "Vampirfledermaus"},
    {"n": "Jacobson-Organ (Geruch über Zunge)", "c": "Schlange"},
    {"n": "Spezielles Nähe-Tastsystem (Vibrissen)", "c": "Seehund"},
    {"n": "Seitliche Augen (fast 360°, rotes Zentrum)", "c": "Fliege"},
    {"n": "Chemorezeptoren an Beinen (Geschmack)", "c": "Schmetterling"},
    {"n": "Einzel-Facettenauge (Ommatidien)", "c": "Biene"},
    {"n": "Infrarot-Pit-Organ in Unterschnippe", "c": "Python"},
    {"n": "Strömungssensoren (Cephalopoden)", "c": "Oktopus (Saugnapf-Tastsinn)"},
    {"n": "Magnetit-Kristalle im Schnabel", "c": "Brieftaube"},
])
save('tiere_match.json', tierm)

# ── TIERE_HL missing categories ─────────────────────────────────
print('── tiere_hl.json ──')
thl2 = load('tiere_hl.json')
exthl(thl2['gewicht_meer']['items'], [
    {"name": "Walhai (Rhincodon typus)", "val": 21500},
    {"name": "Riesenmanta (Manta birostris)", "val": 3000},
    {"name": "Weiße Hai (Carcharodon carcharias)", "val": 2250},
    {"name": "Elefantenrobbe (Männchen)", "val": 2300},
    {"name": "Lederschildkröte (Dermochelys)", "val": 916},
    {"name": "Atlantischer Thunfisch (Blauflossentun)", "val": 725},
    {"name": "Stör (Beluga, Huso huso)", "val": 1571},
    {"name": "Schwertwal (Orca, Männchen)", "val": 6000},
    {"name": "Pottwal (Physeter macrocephalus)", "val": 50000},
    {"name": "Buckelwal (Megaptera)", "val": 36000},
    {"name": "Roter Riesenkrake (Dosidicus)", "val": 50},
    {"name": "Riesen-Tintenfisch (Architeuthis)", "val": 275},
    {"name": "Amerikanischer Hummer (Homarus)", "val": 20},
    {"name": "Alaskaseelachs (Pollock, Durchschnitt)", "val": 3},
    {"name": "Atlantischer Lachs (Zucht)", "val": 4},
    {"name": "Großer Barrakuda", "val": 25},
    {"name": "Seehund (Phoca vitulina)", "val": 130},
    {"name": "Atlantischer Delfin (Delphinus, typisch)", "val": 110},
    {"name": "Pazifischer Oktopus (Enteroctopus)", "val": 15},
    {"name": "Kokosnuss-Krabbe (Birgus latro)", "val": 4},
])
exthl(thl2['speed_luft']['items'], [
    {"name": "Mauersegler (Apus apus, Spurt)", "val": 170},
    {"name": "Alpensegler (Apus melba, Horizontal)", "val": 170},
    {"name": "Große Sturmschwalbe (Fregata magnificens)", "val": 153},
    {"name": "Taubenschwanz-Falke (Falco peregrinus, horizontal)", "val": 110},
    {"name": "Goldadler (Aquila chrysaetos, Sturzflug)", "val": 240},
    {"name": "Weißkopf-Seeadler (Haliaeetus, horizontal)", "val": 80},
    {"name": "Gänsesäger (Mergus merganser, Flügelung)", "val": 110},
    {"name": "Hausschwalbe (Delichon urbicum)", "val": 100},
    {"name": "Ente (Stockente, maximal)", "val": 95},
    {"name": "Graugans (Anser anser, Zug)", "val": 85},
    {"name": "Kormoran (Phalacrocorax)", "val": 91},
    {"name": "Steinadler (Horizontal-Schweben)", "val": 48},
    {"name": "Kolibri (Archilochus, normal)", "val": 48},
    {"name": "Schnepfe (Gallinago, Balzflug)", "val": 110},
    {"name": "Sperber (Accipiter nisus, Verfolgung)", "val": 75},
    {"name": "Kuckuck (Cuculus canorus)", "val": 88},
    {"name": "Kranich (Grus grus, Wanderflug)", "val": 75},
    {"name": "Storch (Ciconia, Gleitflug)", "val": 50},
    {"name": "Albatros (Diomedea, Segelflug)", "val": 90},
    {"name": "Bussard (Buteo buteo, sinkend)", "val": 70},
])
exthl(thl2['traechtigkeit']['items'], [
    {"name": "Kaninchen (Hauskaninchen)", "val": 31},
    {"name": "Hauskatze", "val": 65},
    {"name": "Hund (Haushund, mittel)", "val": 63},
    {"name": "Wildschwein (Sus scrofa)", "val": 116},
    {"name": "Hausschaf", "val": 147},
    {"name": "Hausziege", "val": 150},
    {"name": "Reh (Capreolus)", "val": 280},
    {"name": "Braunbär", "val": 210},
    {"name": "Löwe", "val": 110},
    {"name": "Gorilla", "val": 257},
    {"name": "Schimpanse", "val": 243},
    {"name": "Orang-Utan", "val": 245},
    {"name": "Pferd (Vollblut)", "val": 340},
    {"name": "Nashorn (Spitzmaulnashorn)", "val": 450},
    {"name": "Giraffe", "val": 457},
    {"name": "Elch (Alces alces)", "val": 231},
    {"name": "Wal (Blauwal, geschätzt)", "val": 360},
    {"name": "Gürteltier (Neunbinden, 4 Junge)", "val": 120},
    {"name": "Känguru (Rotes, außerhalb Beutel)", "val": 33},
    {"name": "Opossum (Didelphis, kurze Trächtigkeit)", "val": 13},
])
save('tiere_hl.json', thl2)

print()
print('══ Phase 269b — Done ══')
