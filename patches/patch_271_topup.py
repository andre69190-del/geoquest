#!/usr/bin/env python3
"""Final top-up patch: brings all expandable arrays to 50+ items"""
import json, os

DATA = os.path.join(os.path.dirname(__file__), '..', 'data')

def load(fn):
    with open(os.path.join(DATA, fn), encoding='utf-8') as f:
        return json.load(f)

def save(fn, d):
    with open(os.path.join(DATA, fn), 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f'{fn}: saved')

def topup_hl(d, k, new_items):
    existing = {x['name'] for x in d[k]}
    added = [x for x in new_items if x['name'] not in existing]
    needed = max(0, 50 - len(d[k]))
    d[k].extend(added[:max(needed, len(added))])
    print(f'  {k}: {len(d[k])} items')

def topup_nc(d, k, new_items):
    """match format with n/c keys"""
    existing = {x['n'] for x in d[k]}
    added = [x for x in new_items if x['n'] not in existing]
    needed = max(0, 50 - len(d[k]))
    d[k].extend(added[:max(needed, len(added))])
    print(f'  {k}: {len(d[k])} items')

def topup_p(d, k, new_items):
    existing = {x['n'] for x in d[k]}
    added = [x for x in new_items if x['n'] not in existing]
    needed = max(0, 50 - len(d[k]))
    d[k].extend(added[:max(needed, len(added))])
    print(f'  {k}: {len(d[k])} items')

def topup_items_hl(d, k, new_items):
    """For dict-structured keys with items list, hl format"""
    existing = {x['name'] for x in d[k]['items']}
    added = [x for x in new_items if x['name'] not in existing]
    needed = max(0, 50 - len(d[k]['items']))
    d[k]['items'].extend(added[:max(needed, len(added))])
    print(f'  {k}: {len(d[k]["items"])} items')

def topup_items_nc(d, k, new_items):
    """For dict-structured keys with items list, n/c format"""
    existing = {x['n'] for x in d[k]['items']}
    added = [x for x in new_items if x['n'] not in existing]
    needed = max(0, 50 - len(d[k]['items']))
    d[k]['items'].extend(added[:max(needed, len(added))])
    print(f'  {k}: {len(d[k]["items"])} items')

def topup_items_p(d, k, new_items):
    """For dict-structured keys with items list, pin format"""
    existing = {x['n'] for x in d[k]['items']}
    added = [x for x in new_items if x['n'] not in existing]
    needed = max(0, 50 - len(d[k]['items']))
    d[k]['items'].extend(added[:max(needed, len(added))])
    print(f'  {k}: {len(d[k]["items"])} items')

# ─────────────────────────────────────────────
# archaeologie_hl.json
# ─────────────────────────────────────────────
print("\n=== archaeologie_hl.json ===")
d = load('archaeologie_hl.json')

topup_items_hl(d, 'entdeckungsjahr', [
    {"name": "Tollund-Mann (Dänemark)", "val": 1950},
    {"name": "Nag Hammadi-Schriften (Ägypten)", "val": 1945},
])
topup_items_hl(d, 'fundtiefe', [
    {"name": "Herculaneum (unter Vulkanasche)", "val": 20},
])
topup_items_hl(d, 'groesse_ruinen', [
    {"name": "Palmyra Stadtanlage (Syrien)", "val": 720},
])
topup_items_hl(d, 'hoehe_bauwerke', [
    {"name": "Hagia Sophia Kuppel (Istanbul)", "val": 56},
    {"name": "Pantheon (Rom, Kuppelscheitel)", "val": 43},
])
topup_items_hl(d, 'versicherungswert', [
    {"name": "Nofretete-Büste (Schätzung)", "val": 500},
    {"name": "Goldmaske Tutanchamun (Schätzung)", "val": 2000},
    {"name": "Altamira-Höhle (Schätzung)", "val": 3000},
])
save('archaeologie_hl.json', d)

# ─────────────────────────────────────────────
# archaeologie_pin.json
# ─────────────────────────────────────────────
print("\n=== archaeologie_pin.json ===")
d = load('archaeologie_pin.json')

topup_items_p(d, 'hoehlenmalerien', [
    {"n": "Cueva de las Manos (Argentinien)", "lat": -47.15, "lng": -70.67},
])
topup_items_p(d, 'graberfelder', [
    {"n": "Newgrange (Irland)", "lat": 53.695, "lng": -6.476},
    {"n": "Stonehenge (England)", "lat": 51.179, "lng": -1.826},
    {"n": "Cerro Colorado (Argentinien)", "lat": -30.8, "lng": -64.9},
    {"n": "Sedlec Ossuary (Tschechien)", "lat": 49.96, "lng": 15.26},
    {"n": "Saqqara Nekropole (Ägypten)", "lat": 29.87, "lng": 31.22},
    {"n": "Royal Cemetery of Ur (Irak)", "lat": 30.96, "lng": 46.1},
])
topup_items_p(d, 'fossilien', [
    {"n": "Patagonia Fossil Sites (Argentinien)", "lat": -43.0, "lng": -65.0},
    {"n": "Olduvai Gorge (Tansania)", "lat": -2.99, "lng": 35.35},
])
save('archaeologie_pin.json', d)

# ─────────────────────────────────────────────
# astro_hl.json
# ─────────────────────────────────────────────
print("\n=== astro_hl.json ===")
d = load('astro_hl.json')

topup_items_hl(d, 'astro_planet_groesse', [
    {"name": "Erde", "val": 12742},
    {"name": "Venus", "val": 12104},
    {"name": "Mars", "val": 6779},
    {"name": "Merkur", "val": 4879},
    {"name": "Ganymed (Jupitermond)", "val": 5268},
    {"name": "Titan (Saturnmond)", "val": 5150},
    {"name": "Kallisto (Jupitermond)", "val": 4820},
    {"name": "Io (Jupitermond)", "val": 3643},
    {"name": "Mond (Erdmond)", "val": 3474},
    {"name": "Europa (Jupitermond)", "val": 3122},
    {"name": "Triton (Neptunmond)", "val": 2707},
    {"name": "Pluto (Zwergplanet)", "val": 2376},
])
topup_items_hl(d, 'astro_monde_anzahl', [
    {"name": "Uranus", "val": 27},
    {"name": "Neptun", "val": 16},
    {"name": "Mars", "val": 2},
    {"name": "Erde", "val": 1},
    {"name": "Pluto (Zwergplanet)", "val": 5},
    {"name": "Eris (Zwergplanet)", "val": 1},
    {"name": "Haumea (Zwergplanet)", "val": 2},
    {"name": "Makemake (Zwergplanet)", "val": 1},
    {"name": "Merkur", "val": 0},
    {"name": "Venus", "val": 0},
    {"name": "Ceres (Zwergplanet)", "val": 0},
    {"name": "Gonggong (Zwergplanet)", "val": 1},
])
topup_items_hl(d, 'astro_sonnenentfernung', [
    {"name": "Sedna (Transneptunisches Objekt)", "val": 84000},
    {"name": "Eris (Zwergplanet)", "val": 10125},
    {"name": "Haumea (Zwergplanet)", "val": 6452},
    {"name": "Makemake (Zwergplanet)", "val": 6850},
    {"name": "Pluto (Zwergplanet)", "val": 5906},
    {"name": "Ceres (Zwergplanet)", "val": 414},
    {"name": "Pallas (Asteroid)", "val": 414},
    {"name": "Chiron (Zentaur)", "val": 2052},
])
topup_items_hl(d, 'astro_missionsdauer', [
    {"name": "New Horizons (NASA, seit 2006)", "val": 7085},
    {"name": "Cassini-Huygens (NASA/ESA, 1997–2017)", "val": 7180},
])
topup_items_hl(d, 'astro_schwerkraft', [
    {"name": "Saturn", "val": 10.44},
    {"name": "Erde", "val": 9.81},
    {"name": "Venus", "val": 8.87},
    {"name": "Uranus", "val": 8.69},
    {"name": "Mars", "val": 3.72},
    {"name": "Merkur", "val": 3.7},
    {"name": "Mond", "val": 1.62},
    {"name": "Pluto", "val": 0.62},
    {"name": "Ceres", "val": 0.27},
    {"name": "Ganymed", "val": 1.43},
    {"name": "Titan", "val": 1.35},
])
topup_items_hl(d, 'astro_temperaturen', [
    {"name": "Merkur (Nachts)", "val": -180},
    {"name": "Mars (Durchschnitt)", "val": -65},
    {"name": "Jupiter (Wolkenoberfläche)", "val": -110},
    {"name": "Saturn (Wolkenoberfläche)", "val": -140},
    {"name": "Uranus (Wolkenoberfläche)", "val": -197},
])
topup_items_hl(d, 'astro_entdeckungsjahr', [
    {"name": "Ganymed (Galileo Galilei)", "val": 1610},
    {"name": "Titan (Christiaan Huygens)", "val": 1655},
    {"name": "Iapetus (Giovanni Cassini)", "val": 1671},
    {"name": "Uranus (William Herschel)", "val": 1781},
    {"name": "Ceres (Giuseppe Piazzi)", "val": 1801},
    {"name": "Neptun (Le Verrier/Adams)", "val": 1846},
])
topup_items_hl(d, 'astro_exoplaneten_distanz', [
    {"name": "Luyten b (GJ 273b)", "val": 12.36},
    {"name": "Wolf 1061c", "val": 14.0},
])
save('astro_hl.json', d)

# ─────────────────────────────────────────────
# astro_match.json
# ─────────────────────────────────────────────
print("\n=== astro_match.json ===")
d = load('astro_match.json')

topup_items_nc(d, 'astro_planeten', [
    {"n": "Venus", "c": "Heissester Planet (Treibhauseffekt)"},
    {"n": "Mars", "c": "Roter Planet mit Olympus Mons"},
    {"n": "Saturn", "c": "Planet mit ausgeprägten Ringen"},
    {"n": "Uranus", "c": "Kippt auf seiner Seite (97 Grad)"},
    {"n": "Neptun", "c": "Windgeschwindigkeiten bis 2100 km/h"},
    {"n": "Erde", "c": "Einziger bekannter Planet mit Leben"},
    {"n": "Pluto", "c": "Zwergplanet im Kuiper-Gürtel"},
    {"n": "Ceres", "c": "Groeßter Asteroid im Asteroidengürtel"},
    {"n": "Eris", "c": "Massereichster bekannter Zwergplanet"},
    {"n": "Io", "c": "Vulkanisch aktivster Körper im Sonnensystem"},
    {"n": "Europa", "c": "Ozean unter Eisoberfläche vermutet"},
    {"n": "Titan", "c": "Einziger Mond mit dichter Atmosphäre"},
    {"n": "Enceladus", "c": "Wassergeysire entdeckt (Cassini)"},
    {"n": "Triton", "c": "Rückläufige Umlaufbahn um Neptun"},
    {"n": "Ganymed", "c": "Größter Mond im Sonnensystem"},
    {"n": "Kallisto", "c": "Am stärksten kraterierter Körper"},
    {"n": "Ganimed (Jupitermond)", "c": "Hat ein eigenes Magnetfeld"},
])
topup_items_nc(d, 'astro_kosmologie', [
    {"n": "Dunkle Materie", "c": "Unsichtbare Masse, hält Galaxien zusammen"},
    {"n": "Dunkle Energie", "c": "Treibt Beschleunigung der Expansion"},
    {"n": "Gravitationswellen", "c": "Raumzeitkräuselungen (LIGO 2015)"},
])
topup_items_nc(d, 'astro_sonden_ziele', [
    {"n": "Dawn (NASA)", "c": "Vesta und Ceres"},
    {"n": "OSIRIS-REx (NASA)", "c": "Asteroid Bennu"},
])
topup_items_nc(d, 'astro_pioniere', [
    {"n": "Isaac Newton", "c": "Gravitationsgesetz"},
    {"n": "Edwin Hubble", "c": "Expansion des Universums"},
    {"n": "Carl Sagan", "c": "Populärwissenschaftliche Astronomie"},
    {"n": "Nicolaus Copernicus", "c": "Heliozentrisches Weltbild"},
    {"n": "Tycho Brahe", "c": "Präzise Himmelsbeobachtungen (16. Jh.)"},
    {"n": "Friedrich Bessel", "c": "Erste Sternentfernungsmessung (Parallaxe)"},
    {"n": "Vera Rubin", "c": "Beleg für Dunkle Materie durch Galaxienrotation"},
    {"n": "Subrahmanyan Chandrasekhar", "c": "Chandrasekhar-Grenze für Weiße Zwerge"},
    {"n": "Henrietta Swan Leavitt", "c": "Perioden-Leuchtkraft-Beziehung Cepheiden"},
    {"n": "Fritz Zwicky", "c": "Erstmals Dunkle Materie in Galaxienhaufen postuliert"},
    {"n": "Annie Jump Cannon", "c": "Harvard-Spektralklassifikation (OBAFGKM)"},
    {"n": "William Herschel", "c": "Entdeckung von Uranus (1781)"},
])
topup_items_nc(d, 'astro_galaxien_typen', [
    {"n": "Magellanschen Wolken (Grosse)", "c": "Irregulaere Galaxie"},
    {"n": "Kleine Magellansche Wolke", "c": "Irregulaere Galaxie"},
    {"n": "Sombrero-Galaxie (M104)", "c": "Spiralgalaxie"},
    {"n": "Whirlpool-Galaxie (M51)", "c": "Spiralgalaxie"},
    {"n": "Magellansche Wolke (Gross)", "c": "Irregulaere Galaxie"},
    {"n": "Sculptor-Galaxie (NGC 253)", "c": "Spiralgalaxie"},
    {"n": "Bode-Galaxie (M81)", "c": "Spiralgalaxie"},
    {"n": "Cigar-Galaxie (M82)", "c": "Irregulaere Galaxie"},
])
save('astro_match.json', d)

# ─────────────────────────────────────────────
# astro_pin.json
# ─────────────────────────────────────────────
print("\n=== astro_pin.json ===")
d = load('astro_pin.json')

topup_items_p(d, 'astro_observatorien', [
    {"n": "Observatorio del Teide (Teneriffa, Spanien)", "lat": 28.3, "lng": -16.51},
    {"n": "Lowell Observatory (Flagstaff, Arizona)", "lat": 35.2, "lng": -111.66},
])
topup_items_p(d, 'astro_startrampen', [
    {"n": "Jiuquan Satellite Launch Center (China)", "lat": 40.96, "lng": 100.29},
    {"n": "Sriharikota (ISRO, Indien)", "lat": 13.73, "lng": 80.23},
    {"n": "Tanegashima Space Center (JAXA, Japan)", "lat": 30.4, "lng": 130.97},
    {"n": "Guiana Space Centre (ESA, Französisch-Guayana)", "lat": 5.24, "lng": -52.77},
    {"n": "Wenchang Space Launch Site (China)", "lat": 19.61, "lng": 110.95},
])
topup_items_p(d, 'astro_esa_nasa_zentren', [
    {"n": "ESRIN (ESA Earth Observation, Frascati)", "lat": 41.83, "lng": 12.67},
])
topup_items_p(d, 'astro_weltraumteleskope', [
    {"n": "Spitzer Space Telescope (Launch KSC)", "lat": 28.59, "lng": -80.65},
])
topup_items_p(d, 'astro_meteoritenkrater', [
    {"n": "Manicouagan-Krater (Quebec, Kanada)", "lat": 51.38, "lng": -68.72},
    {"n": "Acraman-Krater (Südaustralien)", "lat": -32.02, "lng": 135.45},
    {"n": "Popigai-Krater (Sibirien, Russland)", "lat": 71.65, "lng": 111.4},
])
topup_items_p(d, 'astro_dark_sky', [
    {"n": "Cherry Springs State Park (Pennsylvania, USA)", "lat": 41.66, "lng": -77.82},
])
save('astro_pin.json', d)

# ─────────────────────────────────────────────
# emob_match.json
# ─────────────────────────────────────────────
print("\n=== emob_match.json ===")
d = load('emob_match.json')

topup_items_nc(d, 'bidirektional', [
    {"n": "Fahrzeug versorgt weiteres Fahrzeug (Notladung)", "c": "V2V"},
])
save('emob_match.json', d)

# ─────────────────────────────────────────────
# gastro_hl.json
# ─────────────────────────────────────────────
print("\n=== gastro_hl.json ===")
d = load('gastro_hl.json')

topup_items_hl(d, 'kalorien', [
    {"name": "Macadamia-Nüsse", "val": 718},
    {"name": "Parmesan (Hartkäse)", "val": 431},
    {"name": "Avocado", "val": 160},
    {"name": "Linsen (gekocht)", "val": 116},
    {"name": "Brokkoli (roh)", "val": 34},
    {"name": "Quinoa (gekocht)", "val": 120},
    {"name": "Lachs (geräuchert)", "val": 142},
    {"name": "Tofu (fest)", "val": 76},
    {"name": "Chili con Carne", "val": 185},
    {"name": "Tiramisu", "val": 280},
])
topup_items_hl(d, 'kerntemperatur', [
    {"name": "Hühnerbrust (durchgegart)", "val": 74},
    {"name": "Lammkeule (medium)", "val": 60},
    {"name": "Lachs (medium)", "val": 52},
    {"name": "Thunfisch (medium rare)", "val": 49},
    {"name": "Entenbrust (medium)", "val": 62},
    {"name": "Kalbsfilet (medium)", "val": 58},
    {"name": "Rinderbrust (well done)", "val": 85},
    {"name": "Wildschweingulasch", "val": 80},
    {"name": "Rehfilet (medium)", "val": 55},
    {"name": "Truthahn (durchgegart)", "val": 74},
    {"name": "Innereien (Leber)", "val": 71},
])
topup_items_hl(d, 'zubereitungszeit', [
    {"name": "Boeuf Bourguignon", "val": 210},
    {"name": "Pulled Pork (Smoker)", "val": 900},
    {"name": "Sauerbraten (mit Marinierzeit)", "val": 4320},
    {"name": "Croissant-Teig (mit Gehzeit)", "val": 720},
    {"name": "Rindsrouladen", "val": 150},
    {"name": "Paella Valenciana", "val": 45},
    {"name": "Eggs Benedict", "val": 25},
    {"name": "Kaiserschmarrn", "val": 20},
    {"name": "Beef Wellington", "val": 90},
    {"name": "Soufflé au Chocolat", "val": 40},
])
topup_items_hl(d, 'fermentationsdauer', [
    {"name": "Kefir (Erstgärung)", "val": 1},
    {"name": "Miso (Shiro, weißes Miso)", "val": 30},
    {"name": "Miso (Aka, rotes Miso)", "val": 365},
    {"name": "Sake (Hauptgärung)", "val": 30},
    {"name": "Sojasauce (Shoyu)", "val": 180},
    {"name": "Naturessig (Essiggärung)", "val": 90},
    {"name": "Bier (Lager, Hauptgärung)", "val": 14},
    {"name": "Prosciutto di Parma (Lufttrocknung)", "val": 730},
    {"name": "Roquefort-Käse (Reifung)", "val": 90},
    {"name": "Tempeh (Rohform)", "val": 2},
    {"name": "Worcestershiresauce (traditionell)", "val": 730},
])
topup_items_hl(d, 'scoville', [
    {"name": "Jalapeño", "val": 8000},
    {"name": "Serrano-Chili", "val": 15000},
    {"name": "Habanero", "val": 350000},
    {"name": "Scotch Bonnet", "val": 300000},
    {"name": "Carolina Reaper", "val": 2200000},
    {"name": "Trinidad Moruga Scorpion", "val": 2009231},
    {"name": "Ghost Pepper (Bhut Jolokia)", "val": 1041427},
    {"name": "Cayenne-Pfeffer", "val": 40000},
    {"name": "Thai-Chili (Bird's Eye)", "val": 100000},
    {"name": "Ancho-Chili", "val": 1500},
    {"name": "Pasilla-Chili", "val": 2500},
    {"name": "Wiri Wiri (Guyana)", "val": 100000},
    {"name": "Aji Amarillo", "val": 30000},
    {"name": "Chipotle (geräuchert)", "val": 8000},
    {"name": "New Mexico Green Chili", "val": 1500},
])
topup_items_hl(d, 'preis_kg', [
    {"name": "Edible Gold (24 Karat)", "val": 60000},
    {"name": "Echter Kaviar (Beluga)", "val": 3500},
    {"name": "Matsutake-Pilze (Japan)", "val": 2000},
    {"name": "Kopi Luwak Kaffee", "val": 700},
    {"name": "Manuka-Honig (aktiv 30+)", "val": 250},
    {"name": "Kobe-Rindfleisch (A5)", "val": 500},
    {"name": "Wasabi (frisch, Japan)", "val": 300},
    {"name": "Vanilleschoten (Madagaskar)", "val": 600},
    {"name": "Schwarze Trüffel (Périgord)", "val": 1500},
    {"name": "Dry-Aged Wagyu (A5 Grade)", "val": 800},
])
topup_items_hl(d, 'wasseranteil', [
    {"name": "Sellerie", "val": 95.4},
    {"name": "Radieschen", "val": 95.3},
    {"name": "Tomate", "val": 94.5},
    {"name": "Spinat", "val": 91.4},
    {"name": "Erdbeere", "val": 90.9},
    {"name": "Apfel", "val": 85.6},
    {"name": "Karotte", "val": 88.3},
    {"name": "Banane", "val": 74.9},
    {"name": "Trauben", "val": 80.5},
    {"name": "Mango", "val": 83.5},
    {"name": "Kartoffel (roh)", "val": 79.3},
    {"name": "Brokkoli", "val": 89.3},
    {"name": "Blumenkohl", "val": 92.1},
    {"name": "Pfirsich", "val": 87.7},
    {"name": "Honigmelone", "val": 90.2},
    {"name": "Papaya", "val": 88.1},
    {"name": "Zucchini", "val": 94.6},
    {"name": "Aubergine", "val": 92.0},
])
topup_items_hl(d, 'backtemperatur', [
    {"name": "Pizza Napoletana (Holzofen)", "val": 430},
    {"name": "Meringues (Baiser)", "val": 90},
    {"name": "Shortbread (Mürbeteig)", "val": 160},
    {"name": "Focaccia", "val": 220},
    {"name": "Cannelés (Bordeaux)", "val": 230},
    {"name": "Financiers (Mandelgebäck)", "val": 175},
    {"name": "Blätterteig-Galette", "val": 200},
    {"name": "Pavlova", "val": 120},
    {"name": "Tarte Tatin", "val": 190},
    {"name": "New York Cheesecake", "val": 170},
    {"name": "Macarons (Schalen)", "val": 150},
])
topup_items_hl(d, 'alkoholgehalt', [
    {"name": "Sake (Junmai)", "val": 16},
    {"name": "Mead (Honigwein)", "val": 14},
    {"name": "Tequila Blanco", "val": 40},
    {"name": "Absinthe", "val": 70},
    {"name": "Rum (weiss, Standard)", "val": 40},
    {"name": "Mezcal (Artisanal)", "val": 46},
    {"name": "Shochu (japanisch)", "val": 25},
    {"name": "Lambic-Bier (ungefiltert)", "val": 5},
    {"name": "Slivovitz (Pflaumenbrand)", "val": 52},
    {"name": "Armagnac (Brandy)", "val": 40},
])
topup_items_hl(d, 'zutaten_anzahl', [
    {"name": "Bouillabaisse (Marseille-Original)", "val": 18},
    {"name": "Mole Negro (Oaxaca)", "val": 30},
])
topup_items_hl(d, 'schmelzpunkt', [
    {"name": "Kokosfett (RBD)", "val": 26},
])
topup_items_hl(d, 'prokopf_verbrauch', [
    {"name": "Fleisch (Deutschland, kg/Jahr)", "val": 52.0},
    {"name": "Fisch (Deutschland, kg/Jahr)", "val": 13.7},
    {"name": "Gemüse (Deutschland, kg/Jahr)", "val": 98.0},
    {"name": "Obst (Deutschland, kg/Jahr)", "val": 65.0},
    {"name": "Zucker (Deutschland, kg/Jahr)", "val": 34.8},
    {"name": "Kartoffeln (Deutschland, kg/Jahr)", "val": 58.0},
    {"name": "Eier (Deutschland, Stück/Jahr)", "val": 236.0},
    {"name": "Käse (Deutschland, kg/Jahr)", "val": 25.8},
    {"name": "Speiseöl (Deutschland, kg/Jahr)", "val": 12.7},
    {"name": "Kaffee (Deutschland, kg/Jahr)", "val": 6.4},
])
save('gastro_hl.json', d)

print("Part 1 complete.")

# ─────────────────────────────────────────────
# gastro_match.json
# ─────────────────────────────────────────────
print("\n=== gastro_match.json ===")
d = load('gastro_match.json')

topup_items_nc(d, 'hausmannskost', [
    {"n": "Pierogi (Teigtaschen mit Füllung)", "c": "Polen"},
    {"n": "Moussaka", "c": "Griechenland"},
    {"n": "Bobotie", "c": "Südafrika"},
    {"n": "Bigos (Jägereintopf)", "c": "Polen"},
    {"n": "Feijoada (Bohnen-Fleisch-Eintopf)", "c": "Brasilien"},
    {"n": "Shakshuka", "c": "Israel"},
])
topup_items_nc(d, 'kuechengeraete', [
    {"n": "Mandoline (Gemüsehobel)", "c": "Schneiden"},
    {"n": "Sous-vide-Garer", "c": "Kochen"},
    {"n": "Wok", "c": "Braten"},
    {"n": "Dampfkochtopf", "c": "Kochen"},
    {"n": "Eismaschine", "c": "Gefrieren"},
    {"n": "Pacojet (Küchengerät)", "c": "Mischen"},
    {"n": "Dehydrator (Dörrgerät)", "c": "Trocknen"},
    {"n": "Fleischwolf", "c": "Zerkleinern"},
    {"n": "Spritzgebäck-Aufsatz", "c": "Formen"},
    {"n": "Brotschneidemaschine", "c": "Schneiden"},
])
topup_items_nc(d, 'schnitttechniken', [
    {"n": "Julienne (feine Stifte)", "c": "Gemüse"},
    {"n": "Bâtonnet (dicke Stifte)", "c": "Gemüse"},
    {"n": "Tourner (gedrechselt)", "c": "Gemüse"},
    {"n": "Concassé (grob gehackt)", "c": "Tomaten"},
    {"n": "Emincé (dünn geschnitten)", "c": "Fleisch"},
    {"n": "Escaloper (schräg aufschneiden)", "c": "Fleisch"},
    {"n": "Ciseler (fein würfeln)", "c": "Zwiebeln"},
    {"n": "Zesten reiben", "c": "Zitrusfrüchte"},
    {"n": "Façonner (formen)", "c": "Teig"},
    {"n": "Trancher (tranchieren)", "c": "Fleisch"},
])
topup_items_nc(d, 'teigtaschen', [
    {"n": "Pierogi (Polen)", "c": "Polen"},
    {"n": "Manti (Türkei/Zentralasien)", "c": "Türkei"},
    {"n": "Empanadas (Lateinamerika)", "c": "Argentinien"},
    {"n": "Momo (Tibet/Nepal)", "c": "Nepal"},
    {"n": "Khinkali (Georgien)", "c": "Georgien"},
    {"n": "Buuz (Mongolei)", "c": "Mongolei"},
    {"n": "Jiaozi (China, nordstil)", "c": "China"},
    {"n": "Ravioli (klassisch)", "c": "Italien"},
    {"n": "Kreplach (Jüdisch)", "c": "Osteuropa"},
    {"n": "Pasteles (Puerto Rico)", "c": "Puerto Rico"},
])
topup_items_nc(d, 'gewuerzmischungen', [
    {"n": "Ras el Hanout", "c": "Afrika"},
    {"n": "Za'atar", "c": "Naher Osten"},
    {"n": "Herbes de Provence", "c": "Europa"},
    {"n": "Cajun Spice", "c": "Nordamerika"},
    {"n": "Baharat", "c": "Naher Osten"},
    {"n": "Dukkah", "c": "Afrika"},
    {"n": "Berbere (Äthiopien)", "c": "Afrika"},
    {"n": "Advieh (Iran)", "c": "Asien"},
    {"n": "Tabil (Tunesien)", "c": "Afrika"},
    {"n": "Khmeli-Suneli (Georgien)", "c": "Europa"},
])
topup_items_nc(d, 'fleisch_cuts', [
    {"n": "Entrecôte (Zwischenrippenstück)", "c": "Rind"},
    {"n": "Flank Steak (Flanke)", "c": "Rind"},
    {"n": "Skirt Steak (Zwerchfell)", "c": "Rind"},
    {"n": "Picanha (Hüftdeckel, Brasilien)", "c": "Rind"},
    {"n": "Osso Buco (Beinscheibe)", "c": "Kalb"},
    {"n": "Spare Ribs (Rippchen)", "c": "Schwein"},
    {"n": "Tenderloin (Filet)", "c": "Schwein"},
    {"n": "Lamb Rack (Kotelettkrone)", "c": "Lamm"},
    {"n": "Gigot (Lammkeule)", "c": "Lamm"},
    {"n": "Poularde (gemästetes Huhn)", "c": "Geflügel"},
])
topup_items_nc(d, 'bakterien_pilze', [
    {"n": "Leuconostoc mesenteroides", "c": "Sauerkraut"},
    {"n": "Acetobacter aceti", "c": "Essig"},
    {"n": "Penicillium camemberti", "c": "Camembert"},
    {"n": "Penicillium roqueforti", "c": "Roquefort"},
    {"n": "Aspergillus oryzae (Koji)", "c": "Miso"},
    {"n": "Lactobacillus bulgaricus", "c": "Bulgur-Joghurt"},
    {"n": "Propionibacterium freudenreichii", "c": "Emmentaler"},
    {"n": "Acetobacter xylinum", "c": "Kombucha-Pellicle"},
    {"n": "Oenococcus oeni", "c": "Wein (malolaktische Gärung)"},
    {"n": "Lactobacillus plantarum", "c": "Sauerteig"},
    {"n": "Rhizopus oligosporus", "c": "Tempeh"},
    {"n": "Candida milleri", "c": "San Francisco Sourdough"},
    {"n": "Gluconobacter oxydans", "c": "Glukonsäure in Bier"},
])
topup_items_nc(d, 'kaffeespezialitaeten', [
    {"n": "Ristretto", "c": "Espresso"},
    {"n": "Lungo", "c": "Espresso"},
    {"n": "Macchiato", "c": "Espresso"},
    {"n": "Flat White", "c": "Espresso"},
    {"n": "Cold Brew", "c": "Kaltextraktion"},
    {"n": "Vietnamese Iced Coffee (Ca Phe Da)", "c": "Filterkaffee"},
    {"n": "Dalgona Coffee", "c": "Schaumkaffee"},
    {"n": "Cortado", "c": "Espresso"},
    {"n": "Affogato", "c": "Espresso"},
    {"n": "Mazagran (algerisch)", "c": "Filterkaffee"},
])
topup_items_nc(d, 'pasta_formen', [
    {"n": "Rigatoni", "c": "Tomatensauce"},
    {"n": "Orecchiette", "c": "Gemüsesauce"},
    {"n": "Farfalle", "c": "Sahnesauce"},
    {"n": "Bucatini", "c": "Amatriciana"},
    {"n": "Paccheri", "c": "Meeresfrüchte"},
    {"n": "Maltagliati", "c": "Gemüsesauce"},
    {"n": "Trofie", "c": "Pesto"},
    {"n": "Cavatappi (Spirale)", "c": "Käsesauce"},
    {"n": "Gemelli", "c": "Cremige Saucen"},
    {"n": "Stringozzi", "c": "Trüffelöl"},
])
topup_items_nc(d, 'exotische_fruechte', [
    {"n": "Jackfrucht", "c": "Asien"},
    {"n": "Mangosteen", "c": "Asien"},
    {"n": "Salak (Schlangenfrucht)", "c": "Asien"},
    {"n": "Longan", "c": "Asien"},
    {"n": "Cherimoya (Rahmapfel)", "c": "Südamerika"},
    {"n": "Feijoa", "c": "Südamerika"},
    {"n": "Pitahaya (Drachenfrucht)", "c": "Mittelamerika"},
    {"n": "Tamarillo", "c": "Südamerika"},
    {"n": "Cupuaçu", "c": "Südamerika"},
])
topup_items_nc(d, 'brotsorten', [
    {"n": "Rye Bread (Roggenbrot)", "c": "Deutschland"},
    {"n": "Focaccia", "c": "Italien"},
    {"n": "Naan", "c": "Indien"},
    {"n": "Injera (Teffbrot)", "c": "Äthiopien"},
    {"n": "Pita", "c": "Griechenland"},
    {"n": "Sourdough (San Francisco)", "c": "USA"},
    {"n": "Damper (Buschbrot)", "c": "Australien"},
    {"n": "Tortilla (Maisbrot)", "c": "Mexiko"},
    {"n": "Lavash (dünnes Fladenbrot)", "c": "Armenien"},
    {"n": "Pretzel (Brezel)", "c": "Deutschland"},
])
topup_items_nc(d, 'vegan_alternativen', [
    {"n": "Jackfrucht (pulled)", "c": "Fleisch"},
    {"n": "Erbsenprotein-Patty", "c": "Fleisch"},
    {"n": "Mandeljoghurt", "c": "Joghurt"},
])
topup_items_nc(d, 'fruehstueck_welt', [
    {"n": "Shakshuka", "c": "Israel"},
    {"n": "Congee (Reisbrei)", "c": "China"},
    {"n": "Ful Medames", "c": "Ägypten"},
    {"n": "Gallo Pinto (Bohnen-Reis)", "c": "Costa Rica"},
    {"n": "Chilaquiles", "c": "Mexiko"},
    {"n": "Dosa mit Sambar", "c": "Indien"},
    {"n": "Nasi Lemak", "c": "Malaysia"},
    {"n": "Menemen (Eiergericht)", "c": "Türkei"},
    {"n": "Croque Monsieur", "c": "Frankreich"},
    {"n": "Rösti", "c": "Schweiz"},
])
topup_items_nc(d, 'fachbegriffe_herd', [
    {"n": "Blanchieren", "c": "Kochen"},
    {"n": "Frittieren", "c": "Braten"},
    {"n": "Gratinieren", "c": "Überbacken"},
])
topup_items_nc(d, 'sushi_arten', [
    {"n": "Temaki (Handrolle)", "c": "Reis gerollt"},
    {"n": "Chirashi-Zushi", "c": "Streusushi"},
    {"n": "Onigiri", "c": "Geformter Reis"},
    {"n": "Ura-Maki (Inside-out)", "c": "Reis gerollt"},
    {"n": "Inari-Zushi (Tofutasche)", "c": "Gefüllter Reis"},
    {"n": "Omakase Nigiri", "c": "Nigiri"},
    {"n": "Sashimi (ohne Reis)", "c": "Rohfisch ohne Reis"},
    {"n": "Temari-Zushi (Ballenform)", "c": "Geformter Reis"},
    {"n": "Gunkan-Maki (Schlachtschiff)", "c": "Nigiri"},
    {"n": "Futomaki (dicke Rolle)", "c": "Reis gerollt"},
])
save('gastro_match.json', d)

# ─────────────────────────────────────────────
# gastro_pin.json
# ─────────────────────────────────────────────
print("\n=== gastro_pin.json ===")
d = load('gastro_pin.json')

topup_items_p(d, 'brauereien', [
    {"n": "Trappistes Rochefort (Belgien)", "lat": 50.16, "lng": 5.22},
    {"n": "Sierra Nevada Brewing (Chico, Kalifornien)", "lat": 39.73, "lng": -121.84},
    {"n": "Cantillon Brouwerij (Brüssel, Belgien)", "lat": 50.84, "lng": 4.34},
    {"n": "Anchor Brewing (San Francisco, USA)", "lat": 37.76, "lng": -122.42},
    {"n": "Kirin Brewery (Yokohama, Japan)", "lat": 35.46, "lng": 139.63},
    {"n": "Heineken Brauerei (Amsterdam)", "lat": 52.36, "lng": 4.89},
    {"n": "Dogfish Head Craft Brewery (Milton, Delaware)", "lat": 38.78, "lng": -75.31},
    {"n": "Estrella Damm (Barcelona, Spanien)", "lat": 41.38, "lng": 2.19},
])
topup_items_p(d, 'kaffeehaeuser', [
    {"n": "Gran Caffè Florian (Venedig, Italien)", "lat": 45.434, "lng": 12.338},
    {"n": "Antico Caffè Greco (Rom, Italien)", "lat": 41.904, "lng": 12.481},
    {"n": "Café Tortoni (Buenos Aires, Argentinien)", "lat": -34.609, "lng": -58.376},
    {"n": "Café Schwarzenberg (Wien, Österreich)", "lat": 48.204, "lng": 16.376},
    {"n": "Café A Brasileira (Lissabon, Portugal)", "lat": 38.713, "lng": -9.14},
    {"n": "Café du Commerce (Paris, Frankreich)", "lat": 48.845, "lng": 2.295},
    {"n": "Café Landtmann (Wien, Österreich)", "lat": 48.212, "lng": 16.358},
    {"n": "Algerian Coffee Stores (London, UK)", "lat": 51.513, "lng": -0.131},
    {"n": "Café Procope (ältestes Kaffeehaus Paris, Frankreich)", "lat": 48.852, "lng": 2.341},
    {"n": "Blue Bottle Coffee HQ (Oakland, Kalifornien)", "lat": 37.810, "lng": -122.256},
])
topup_items_p(d, 'weinlagen', [
    {"n": "Penfolds Magill Estate (Südaustralien)", "lat": -34.89, "lng": 138.71},
    {"n": "Vega Sicilia Unico (Ribera del Duero)", "lat": 41.62, "lng": -4.18},
    {"n": "Sassicaia (Bolgheri, Toskana)", "lat": 43.18, "lng": 10.62},
    {"n": "Opus One (Napa Valley)", "lat": 38.42, "lng": -122.41},
    {"n": "Henschke Hill of Grace (Eden Valley)", "lat": -34.45, "lng": 138.86},
    {"n": "Screaming Eagle (Oakville, Napa)", "lat": 38.45, "lng": -122.42},
    {"n": "Pingus (Ribera del Duero)", "lat": 41.62, "lng": -3.72},
    {"n": "Le Pin (Pomerol, Bordeaux)", "lat": 44.92, "lng": -0.19},
    {"n": "Domaine Leflaive Puligny-Montrachet", "lat": 46.96, "lng": 4.77},
    {"n": "Concha y Toro Don Melchor (Chile)", "lat": -33.61, "lng": -70.73},
])
save('gastro_pin.json', d)

print("Part 2 complete.")

# ─────────────────────────────────────────────
# geo_hl.json
# ─────────────────────────────────────────────
print("\n=== geo_hl.json ===")
d = load('geo_hl.json')

topup_items_hl(d, 'geo_berghoehen', [
    {"name": "Kangchenjunga (Indien/Nepal)", "val": 8586},
    {"name": "Lhotse (Nepal/China)", "val": 8516},
    {"name": "Makalu (Nepal/China)", "val": 8485},
    {"name": "Cho Oyu (Nepal/China)", "val": 8188},
    {"name": "Dhaulagiri (Nepal)", "val": 8167},
    {"name": "Manaslu (Nepal)", "val": 8163},
    {"name": "Nanga Parbat (Pakistan)", "val": 8126},
    {"name": "Annapurna I (Nepal)", "val": 8091},
    {"name": "Gasherbrum I (Pakistan/China)", "val": 8080},
])
topup_items_hl(d, 'geo_vulkan_hoehen', [
    {"name": "Kilimandscharo (Tansania)", "val": 5895},
    {"name": "Elbrus (Russland)", "val": 5642},
    {"name": "Popocatépetl (Mexiko)", "val": 5426},
    {"name": "Cotopaxi (Ecuador)", "val": 5897},
    {"name": "Mauna Kea (Hawaii, USA, über Meeresgrund)", "val": 4205},
    {"name": "Mount Erebus (Antarktis)", "val": 3794},
    {"name": "Piton de la Fournaise (Réunion)", "val": 2631},
])
topup_items_hl(d, 'geo_erdbeben_magnitude', [
    {"name": "Kamtschatka 1952 (Russland)", "val": 90},
    {"name": "Maule 2010 (Chile)", "val": 88},
    {"name": "Ecuador 1906", "val": 87},
    {"name": "Rat Islands 1965 (Alaska)", "val": 85},
    {"name": "Assam-Tibet 1950 (Indien/China)", "val": 85},
])
topup_items_hl(d, 'geo_vei_ausbruch', [
    {"name": "Toba 74.000 v. Chr. (Indonesien)", "val": 8},
    {"name": "Pinatubo 1991 (Philippinen)", "val": 6},
    {"name": "Novarupta 1912 (Alaska)", "val": 6},
    {"name": "Santa María 1902 (Guatemala)", "val": 6},
    {"name": "Laki 1783 (Island)", "val": 6},
])
topup_items_hl(d, 'geo_hoehlen_laenge', [
    {"name": "Sac Actun (Mexiko)", "val": 364},
    {"name": "Jewel Cave (South Dakota, USA)", "val": 338},
])
topup_items_hl(d, 'geo_schluchten_tiefe', [
    {"name": "Grand Canyon (Arizona, USA)", "val": 1857},
    {"name": "Yarlung Tsangpo (Tibet, China)", "val": 5382},
    {"name": "Tiger Leaping Gorge (Yunnan, China)", "val": 3900},
    {"name": "Blyde River Canyon (Südafrika)", "val": 750},
])
topup_items_hl(d, 'geo_kontinentaldrift', [
    {"name": "Afrikanische Platte (östlich)", "val": 30},
    {"name": "Juan-de-Fuca-Platte", "val": 29},
    {"name": "Nasca-Platte", "val": 65},
    {"name": "Arabische Platte", "val": 25},
    {"name": "Nordamerikanische Platte", "val": 23},
    {"name": "Eurasische Platte (west)", "val": 21},
    {"name": "Antarktische Platte", "val": 15},
    {"name": "Karibische Platte", "val": 20},
    {"name": "Philippinische Platte", "val": 60},
    {"name": "Somali-Platte", "val": 35},
    {"name": "Kokosplatte", "val": 72},
    {"name": "Südamerikanische Platte", "val": 25},
    {"name": "Afrikanische Platte (gesamt)", "val": 28},
])
topup_items_hl(d, 'geo_schmelztemperatur', [
    {"name": "Korund (Al₂O₃)", "val": 2050},
])
topup_items_hl(d, 'geo_gletscher_volumen', [
    {"name": "Alaska-Gletscher (gesamt)", "val": 75000},
    {"name": "Bering-Gletscher (Alaska)", "val": 1170},
])
topup_items_hl(d, 'geo_tsunami_hoehe', [
    {"name": "Aitape 1998 (Papua-Neuguinea)", "val": 15},
])
save('geo_hl.json', d)

# ─────────────────────────────────────────────
# geo_match.json
# ─────────────────────────────────────────────
print("\n=== geo_match.json ===")
d = load('geo_match.json')

topup_items_nc(d, 'geo_gesteinsarten', [
    {"n": "Basalt", "c": "Magmatisch"},
    {"n": "Obsidian", "c": "Magmatisch"},
    {"n": "Rhyolith", "c": "Magmatisch"},
    {"n": "Gabbro", "c": "Magmatisch"},
    {"n": "Diorit", "c": "Magmatisch"},
    {"n": "Andesit", "c": "Magmatisch"},
    {"n": "Sandstein", "c": "Sedimentär"},
    {"n": "Kalkstein", "c": "Sedimentär"},
    {"n": "Tonschiefer", "c": "Sedimentär"},
    {"n": "Dolomit", "c": "Sedimentär"},
    {"n": "Konglomerat", "c": "Sedimentär"},
    {"n": "Schiefer", "c": "Metamorph"},
    {"n": "Gneis", "c": "Metamorph"},
    {"n": "Phyllit", "c": "Metamorph"},
    {"n": "Quarzit", "c": "Metamorph"},
    {"n": "Serpentinit", "c": "Metamorph"},
])
topup_items_nc(d, 'geo_tektonik', [
    {"n": "Japan", "c": "Pazifische Platte / Eurasische Platte"},
    {"n": "Neuseeland", "c": "Australische Platte"},
    {"n": "Island", "c": "Eurasische Platte / Nordamerikanische Platte"},
    {"n": "Griechenland", "c": "Eurasische Platte"},
    {"n": "Peru", "c": "Südamerikanische Platte"},
    {"n": "Iran", "c": "Arabische Platte / Eurasische Platte"},
    {"n": "Kenia", "c": "Afrikanische Platte"},
])
topup_items_nc(d, 'geo_mineralien', [
    {"n": "Silizium (Quarz)", "c": "Elektronik und Glas"},
    {"n": "Fluorit", "c": "Flusssäure-Herstellung"},
    {"n": "Hämatit", "c": "Eisengewinnung"},
    {"n": "Magnetit", "c": "Eisengewinnung"},
    {"n": "Zinkit", "c": "Zinkgewinnung"},
    {"n": "Cerussit", "c": "Bleigewinnung"},
])
topup_items_nc(d, 'geo_fossil_zeitalter', [
    {"n": "Ammonit", "c": "Mesozoikum"},
    {"n": "Brachiopod", "c": "Paläozoikum"},
    {"n": "Mammut", "c": "Känozoikum"},
    {"n": "Saurier (Tyrannosaurus)", "c": "Mesozoikum"},
    {"n": "Nautiloid", "c": "Paläozoikum"},
])
topup_items_nc(d, 'geo_erdbeben_jahr', [
    {"n": "Kanto-Erdbeben (Japan)", "c": "1923"},
    {"n": "Tangshan-Erdbeben (China)", "c": "1976"},
])
topup_items_nc(d, 'geo_gestein_nutzung', [
    {"n": "Schiefer", "c": "Dachplatten & Wandverkleidung"},
    {"n": "Kalkstein", "c": "Zement-Herstellung"},
    {"n": "Obsidian", "c": "Historische Klingen & Skalpelle"},
])
topup_items_nc(d, 'geo_landschaft_ursprung', [
    {"n": "Fjord", "c": "Gletscher-Erosion"},
    {"n": "Karst-Kavernen", "c": "Lösungsverwitterung Kalkstein"},
])
topup_items_nc(d, 'geo_mineral_farbe', [
    {"n": "Azurit", "c": "Blau"},
    {"n": "Rhodonit", "c": "Rosa-Rot"},
])
topup_items_nc(d, 'geo_kontinent_platte', [
    {"n": "Island", "c": "Eurasische Platte / Nordamerikanische Platte"},
    {"n": "Arabische Halbinsel", "c": "Arabische Platte"},
    {"n": "Karibik", "c": "Karibische Platte"},
    {"n": "Neuseeland (Nordinsel)", "c": "Australische Platte"},
    {"n": "Philippinen", "c": "Philippinische Platte"},
    {"n": "Türkei (Anatolien)", "c": "Anatolische Platte"},
])
topup_items_nc(d, 'geo_hoehlen_land', [
    {"n": "Optymistychna Cave", "c": "Ukraine"},
])
topup_items_nc(d, 'geo_mineral_kristall', [
    {"n": "Quarz", "c": "Trigonal"},
    {"n": "Calcit", "c": "Trigonal"},
    {"n": "Feldspat", "c": "Triklin"},
])
topup_items_nc(d, 'geo_gebirge_entstehung', [
    {"n": "Karpaten", "c": "Kontinent-Kontinent-Kollision"},
    {"n": "Rocky Mountains", "c": "Subduktion"},
    {"n": "Appalachen", "c": "Kontinent-Kontinent-Kollision (alt)"},
])
save('geo_match.json', d)

# ─────────────────────────────────────────────
# geo_pin.json
# ─────────────────────────────────────────────
print("\n=== geo_pin.json ===")
d = load('geo_pin.json')

topup_items_p(d, 'geo_vulkane', [
    {"n": "Piton de la Fournaise (Réunion)", "lat": -21.23, "lng": 55.71},
    {"n": "Nevado del Ruiz (Kolumbien)", "lat": 4.89, "lng": -75.32},
])
topup_items_p(d, 'geo_geothermal', [
    {"n": "Wai-O-Tapu Geothermal Area (Neuseeland)", "lat": -38.36, "lng": 176.37},
])
topup_items_p(d, 'geo_felsformationen', [
    {"n": "Wave Rock (Westaustralien)", "lat": -32.44, "lng": 118.9},
    {"n": "Chocolate Hills (Bohol, Philippinen)", "lat": 9.9, "lng": 124.17},
    {"n": "Pinnacles Desert (Nambung NP, Australien)", "lat": -30.6, "lng": 115.15},
])
topup_items_p(d, 'geo_hoehlensysteme', [
    {"n": "Lechuguilla Cave (New Mexico, USA)", "lat": 32.11, "lng": -104.56},
    {"n": "Waitomo Glowworm Caves (Neuseeland)", "lat": -38.26, "lng": 175.11},
])
topup_items_p(d, 'geo_geysire', [
    {"n": "Geysir Strokkur (Island)", "lat": 64.31, "lng": -20.3},
    {"n": "Steamboat Geyser (Yellowstone, USA)", "lat": 44.73, "lng": -110.71},
    {"n": "Pohutu Geyser (Rotorua, Neuseeland)", "lat": -38.16, "lng": 176.38},
    {"n": "Velikan Geyser (Kamtschatka, Russland)", "lat": 54.44, "lng": 160.65},
    {"n": "Geysir Geysirtal (Chile, El Tatio alt)", "lat": -22.33, "lng": -68.0},
    {"n": "Lady Knox Geyser (Rotorua, NZ)", "lat": -38.24, "lng": 176.38},
])
topup_items_p(d, 'geo_minen_bohrungen', [
    {"n": "Chuquicamata Kupfermine (Chile)", "lat": -22.3, "lng": -68.92},
    {"n": "Carlin Gold Mine (Nevada, USA)", "lat": 40.75, "lng": -116.11},
    {"n": "Grasberg Mine (Papua, Indonesien)", "lat": -4.05, "lng": 137.12},
    {"n": "Jwaneng Diamantmine (Botswana)", "lat": -24.6, "lng": 24.73},
])
save('geo_pin.json', d)

print("Part 3 complete.")

# ─────────────────────────────────────────────
# pflanzen_hl.json
# ─────────────────────────────────────────────
print("\n=== pflanzen_hl.json ===")
d = load('pflanzen_hl.json')

topup_items_hl(d, 'wuchshoehe', [
    {"name": "Sitka-Fichte (groeßte Sitka)", "val": 96.7},
    {"name": "Douglas-Tanne (Doerner Fir)", "val": 99.8},
    {"name": "Sugi (Japanische Zeder, Cryptomeria)", "val": 62.3},
    {"name": "Kauri (Agathis australis, Neuseeland)", "val": 51.5},
    {"name": "Riesenmammutbaum (General Sherman)", "val": 83.8},
    {"name": "Afrikanischer Affenbrotbaum (Baobab)", "val": 25.0},
    {"name": "Bambuspflanze (Phyllostachys)", "val": 35.0},
    {"name": "Königspalme (Roystonea)", "val": 30.0},
    {"name": "Blaue Agave (Agave tequilana)", "val": 2.5},
    {"name": "Riesenseerose (Victoria amazonica)", "val": 0.8},
])
topup_items_hl(d, 'alter', [
    {"name": "Pando (Zitterespe-Klon, Utah)", "val": 80000},
    {"name": "Lomatia tasmanica (Tasmanien)", "val": 43600},
    {"name": "Huon Pine (Tasmanien)", "val": 10500},
    {"name": "Alerce (Fitzroya cupressoides, Chile)", "val": 3622},
    {"name": "Angel Oak (Stieleiche, South Carolina)", "val": 500},
    {"name": "Boab Prison Tree (Australien)", "val": 1500},
    {"name": "Sri Maha Bodhi (Feigenbaum, Sri Lanka)", "val": 2300},
    {"name": "Chestnut of One Hundred Horses (Sizilien)", "val": 4000},
    {"name": "Sarv-e Abarqu (Zypresse, Iran)", "val": 4500},
    {"name": "Gran Abuelo (Alerce, Chile)", "val": 3650},
    {"name": "Olive Tree of Vouves (Kreta)", "val": 3000},
])
topup_items_hl(d, 'fruchtgewicht', [
    {"name": "Riesenkürbis (Atlantik Riese)", "val": 1226000},
    {"name": "Brotfrucht (Artocarpus altilis)", "val": 4000},
    {"name": "Papaya (Carica papaya, groeß)", "val": 9000},
    {"name": "Mango (Tommy Atkins)", "val": 900},
    {"name": "Avocado (Florida-Typ)", "val": 500},
    {"name": "Guave (Psidium guajava)", "val": 200},
    {"name": "Durian (Durio zibethinus)", "val": 3000},
    {"name": "Mangosteen (Garcinia mangostana)", "val": 200},
    {"name": "Longan-Traube (Dimocarpus longan)", "val": 20},
    {"name": "Rambutan (Nephelium lappaceum)", "val": 30},
    {"name": "Lychee (Litchi chinensis)", "val": 20},
    {"name": "Kiwifrucht (Actinidia deliciosa)", "val": 100},
    {"name": "Starfrucht (Averrhoa carambola)", "val": 150},
    {"name": "Cherimoya (Annona cherimola)", "val": 1000},
    {"name": "Cupuaçu (Theobroma grandiflorum)", "val": 1500},
    {"name": "Feijoa (Acca sellowiana)", "val": 80},
])
topup_items_hl(d, 'samenlaenge', [
    {"name": "Vanilleschote (Vanilla planifolia)", "val": 200},
    {"name": "Kakaoschote (Theobroma cacao)", "val": 250},
    {"name": "Strelitzia reginae (Samenhülse)", "val": 50},
    {"name": "Tamarinde (Tamarindus indica)", "val": 150},
])
topup_items_hl(d, 'kaffeeproduktion', [
    {"name": "Kolumbien", "val": 14000},
    {"name": "Indonesien", "val": 11000},
    {"name": "Äthiopien", "val": 8000},
    {"name": "Honduras", "val": 6200},
    {"name": "Peru", "val": 4200},
    {"name": "Uganda", "val": 5700},
    {"name": "Guatemala", "val": 3200},
    {"name": "Mexiko", "val": 2300},
    {"name": "Nicaragua", "val": 1500},
    {"name": "Côte d'Ivoire", "val": 500},
    {"name": "Kamerun", "val": 350},
    {"name": "Papua-Neuguinea", "val": 1100},
    {"name": "Tansania", "val": 900},
    {"name": "Kenia", "val": 720},
])
topup_items_hl(d, 'weinproduktion', [
    {"name": "Spanien", "val": 3981},
    {"name": "USA", "val": 3032},
    {"name": "Australien", "val": 1356},
    {"name": "Argentinien", "val": 1498},
    {"name": "Chile", "val": 1277},
    {"name": "Südafrika", "val": 1051},
    {"name": "Deutschland", "val": 900},
    {"name": "Portugal", "val": 621},
    {"name": "Russland", "val": 440},
    {"name": "Rumänien", "val": 390},
    {"name": "Neuseeland", "val": 311},
    {"name": "Griechenland", "val": 270},
    {"name": "Österreich", "val": 245},
    {"name": "Ungarn", "val": 350},
    {"name": "Schweiz", "val": 100},
    {"name": "Kroatien", "val": 60},
    {"name": "Brasilien", "val": 300},
    {"name": "Moldau", "val": 150},
])
topup_items_hl(d, 'reisproduktion', [
    {"name": "Bangladesch", "val": 57.0},
    {"name": "Vietnam", "val": 43.0},
    {"name": "Indonesien", "val": 55.0},
    {"name": "Thailand", "val": 33.0},
    {"name": "Myanmar", "val": 26.0},
    {"name": "Philippinen", "val": 20.0},
    {"name": "Brasilien", "val": 11.0},
    {"name": "Pakistan", "val": 11.0},
    {"name": "Japan", "val": 10.5},
    {"name": "Kambodscha", "val": 11.0},
    {"name": "USA", "val": 10.0},
    {"name": "Nigeria", "val": 8.0},
    {"name": "Ägypten", "val": 6.5},
    {"name": "Nepal", "val": 5.5},
    {"name": "Korea (Süd)", "val": 5.0},
    {"name": "Sri Lanka", "val": 4.0},
    {"name": "Peru", "val": 3.5},
    {"name": "Kolumbien", "val": 3.0},
    {"name": "Tansania", "val": 3.0},
    {"name": "Iran", "val": 3.5},
    {"name": "Taiwan", "val": 1.5},
])
topup_items_hl(d, 'waldflaeche', [
    {"name": "Guyana", "val": 84.0},
    {"name": "Bhutan", "val": 71.0},
    {"name": "Laos", "val": 68.0},
    {"name": "Papua-Neuguinea", "val": 74.0},
    {"name": "Kongo (Dem. Rep.)", "val": 67.0},
])
topup_items_hl(d, 'stammumfang', [
    {"name": "Baobab (Affenbrotbaum) Senegal", "val": 4000},
])
topup_items_hl(d, 'blattflaeche', [
    {"name": "Monstera deliciosa (Fensterblatt)", "val": 4000},
])
topup_items_hl(d, 'bluehdauer', [
    {"name": "Wüstenrose (Adenium obesum)", "val": 240},
    {"name": "Alpenrose (Rhododendron ferrugineum)", "val": 60},
])
save('pflanzen_hl.json', d)

print("Part 4 complete.")

# ─────────────────────────────────────────────
# pflanzen_match.json
# ─────────────────────────────────────────────
print("\n=== pflanzen_match.json ===")
d = load('pflanzen_match.json')

topup_items_nc(d, 'familien', [
    {"n": "Sonnenblume", "c": "Asteraceae"},
    {"n": "Tulpe", "c": "Liliaceae"},
    {"n": "Orchidee", "c": "Orchidaceae"},
    {"n": "Bambus", "c": "Poaceae"},
    {"n": "Eiche", "c": "Fagaceae"},
    {"n": "Olive", "c": "Oleaceae"},
    {"n": "Tomate", "c": "Solanaceae"},
    {"n": "Kartoffel", "c": "Solanaceae"},
    {"n": "Kamille", "c": "Asteraceae"},
    {"n": "Hanf (Cannabis)", "c": "Cannabaceae"},
])
topup_items_nc(d, 'lebensraum', [
    {"n": "Alpenrose (Rhododendron)", "c": "Hochgebirge"},
    {"n": "Seekiefer (Pinus pinaster)", "c": "Küstenwald"},
    {"n": "Eukalyptus", "c": "Savanne"},
    {"n": "Schilf (Phragmites australis)", "c": "Feuchtgebiet"},
    {"n": "Wüstenrose (Adenium obesum)", "c": "Wüste"},
    {"n": "Torfmoos (Sphagnum)", "c": "Moor"},
    {"n": "Kelp (Macrocystis)", "c": "Ozean"},
    {"n": "Weißtanne (Abies alba)", "c": "Bergwald"},
    {"n": "Zuckerrohr (Saccharum officinarum)", "c": "Tropen"},
    {"n": "Strandhafer (Ammophila)", "c": "Dünen"},
])
topup_items_nc(d, 'bestuaeber', [
    {"n": "Kakaobaum (Theobroma cacao)", "c": "Mücken (Gnitzen)"},
    {"n": "Vanille", "c": "Bienen / manuell"},
    {"n": "Yucca-Palme", "c": "Yucca-Motte (Spezialist)"},
    {"n": "Agave", "c": "Fledermäuse"},
    {"n": "Feigenbaum", "c": "Feigenwespen"},
    {"n": "Passionsblume", "c": "Kolibris"},
    {"n": "Roter Ingwer", "c": "Vögel"},
    {"n": "Eibe (Taxus)", "c": "Wind"},
    {"n": "Buche (Fagus sylvatica)", "c": "Wind"},
    {"n": "Nachtviole (Hesperis)", "c": "Nachtfalter"},
    {"n": "Rafflesia arnoldii", "c": "Fliegen (Aas-Duft)"},
])
topup_items_nc(d, 'herkunft', [
    {"n": "Mais", "c": "Mittelamerika"},
    {"n": "Chili", "c": "Mittelamerika"},
    {"n": "Schokolade (Kakao)", "c": "Mittelamerika"},
    {"n": "Erdnuss", "c": "Südamerika"},
    {"n": "Ananas", "c": "Südamerika"},
    {"n": "Soja", "c": "Asien"},
    {"n": "Banane", "c": "Asien"},
    {"n": "Zuckerrohr", "c": "Asien"},
    {"n": "Weizen", "c": "Naher Osten"},
    {"n": "Gerste", "c": "Naher Osten"},
    {"n": "Olive", "c": "Mittelmeer"},
    {"n": "Feige", "c": "Naher Osten"},
])
topup_items_nc(d, 'nutzung', [
    {"n": "Echinacea purpurea", "c": "Medizin / Pharmazie"},
    {"n": "Hanf (Cannabis sativa)", "c": "Textilfaser"},
    {"n": "Leinen (Flachs)", "c": "Textilfaser"},
    {"n": "Raps (Brassica napus)", "c": "Speiseöl / Treibstoff"},
    {"n": "Weide (Salix alba)", "c": "Medizin (Salicin)"},
    {"n": "Bambus", "c": "Baumaterial"},
    {"n": "Latex (Hevea brasiliensis)", "c": "Gummi-Herstellung"},
    {"n": "Zuckerrohr", "c": "Zucker / Ethanol"},
    {"n": "Quinoa", "c": "Nahrungsmittel (Pseudogetreide)"},
    {"n": "Moringa oleifera", "c": "Nahrung / Wasserreinigung"},
    {"n": "Neem (Azadirachta indica)", "c": "Pestizid / Medizin"},
])
topup_items_nc(d, 'blattform', [
    {"n": "Linde (Tilia)", "c": "Herzförmig"},
    {"n": "Ahorn (Acer)", "c": "Gelappt"},
    {"n": "Wein (Vitis vinifera)", "c": "Gelappt"},
    {"n": "Efeu (Hedera helix)", "c": "Gelappt"},
    {"n": "Rosskastanie (Aesculus)", "c": "Gefiedert"},
    {"n": "Esche (Fraxinus)", "c": "Gefiedert"},
    {"n": "Magnolie", "c": "Oval"},
    {"n": "Eukalyptus (jung)", "c": "Rund"},
    {"n": "Eukalyptus (ausgewachsen)", "c": "Lanzettlich"},
    {"n": "Gras (Poaceae)", "c": "Linealisch"},
    {"n": "Zwiebel (Allium)", "c": "Röhrenförmig"},
    {"n": "Kiefer (Pinus)", "c": "Nadelförmig"},
])
topup_items_nc(d, 'klimazone', [
    {"n": "Pinie (Pinus pinea)", "c": "Mediterran"},
    {"n": "Kaktus (Saguaro, Carnegiea gigantea)", "c": "Trocken"},
    {"n": "Mandschurische Eiche", "c": "Gemässigt"},
    {"n": "Birke (Betula pendula)", "c": "Gemässigt"},
    {"n": "Taiga-Lärche", "c": "Boreal"},
    {"n": "Kokospalme", "c": "Tropisch"},
    {"n": "Araukarie (Monkey Puzzle)", "c": "Gemässigt"},
    {"n": "Alpenenzian (Gentiana acaulis)", "c": "Alpin"},
    {"n": "Mangrove (Rhizophora)", "c": "Tropisch"},
    {"n": "Arktische Weide (Salix arctica)", "c": "Polar"},
])
save('pflanzen_match.json', d)

# ─────────────────────────────────────────────
# pflanzen_pin.json
# ─────────────────────────────────────────────
print("\n=== pflanzen_pin.json ===")
d = load('pflanzen_pin.json')

topup_items_p(d, 'nutzpflanzen', [
    {"n": "Tee-Ursprung (Yunnan, China)", "lat": 23.5, "lng": 100.5},
    {"n": "Weizen-Ursprung (Levante, Naher Osten)", "lat": 36.0, "lng": 37.5},
    {"n": "Kartoffel-Ursprung (Titicacasee-Region)", "lat": -15.5, "lng": -70.0},
    {"n": "Mais-Ursprung (Oaxaca-Tal, Mexiko)", "lat": 17.0, "lng": -96.7},
    {"n": "Tomaten-Ursprung (Westliche Anden)", "lat": -5.0, "lng": -80.0},
    {"n": "Soja-Ursprung (Nordostchina)", "lat": 44.0, "lng": 126.0},
    {"n": "Quinoa-Ursprung (Bolivianische Hochebene)", "lat": -17.0, "lng": -66.5},
    {"n": "Süßkartoffel-Ursprung (Peru/Ecuador)", "lat": -6.0, "lng": -78.0},
    {"n": "Baumwolle-Zentrum (Indus-Tal)", "lat": 27.5, "lng": 68.0},
    {"n": "Vanille-Ursprung (Veracruz, Mexiko)", "lat": 19.5, "lng": -96.9},
])
topup_items_p(d, 'einzelbaeume', [
    {"n": "Angel Oak Tree (Johns Island, South Carolina)", "lat": 32.72, "lng": -80.08},
    {"n": "Lone Cypress (Pebble Beach, Kalifornien)", "lat": 36.57, "lng": -121.97},
    {"n": "Olive Tree of Vouves (Kreta, Griechenland)", "lat": 35.49, "lng": 23.72},
    {"n": "Wawona Tunnel Tree (Yosemite, USA)", "lat": 37.51, "lng": -119.56},
    {"n": "Dragon Blood Tree (Socotra, Jemen)", "lat": 12.51, "lng": 54.0},
    {"n": "Boab Prison Tree (Derby, Australien)", "lat": -17.31, "lng": 123.63},
    {"n": "Árbol del Tule (Oaxaca, Mexiko)", "lat": 17.05, "lng": -96.64},
    {"n": "Bodhi Tree (Bodh Gaya, Indien)", "lat": 24.69, "lng": 84.99},
    {"n": "Ginkgo of Gu Guanyin (China)", "lat": 34.54, "lng": 108.91},
    {"n": "Chandelier Tree (Leggett, Kalifornien)", "lat": 39.86, "lng": -123.72},
])
topup_items_p(d, 'botanische_gaerten', [
    {"n": "Singapore Botanic Gardens", "lat": 1.31, "lng": 103.82},
    {"n": "New York Botanical Garden (Bronx)", "lat": 40.86, "lng": -73.88},
    {"n": "Real Jardín Botánico de Madrid", "lat": 40.41, "lng": -3.69},
    {"n": "Jardín Botánico de Bogotá", "lat": 4.67, "lng": -74.1},
    {"n": "Jardin des Plantes (Paris)", "lat": 48.84, "lng": 2.36},
    {"n": "Botanischer Garten Wien (Belvedere)", "lat": 48.19, "lng": 16.38},
    {"n": "Royal Botanic Gardens Melbourne", "lat": -37.83, "lng": 144.98},
    {"n": "São Paulo Botanical Garden", "lat": -23.65, "lng": -46.62},
    {"n": "Jardim Botânico do Rio de Janeiro", "lat": -22.97, "lng": -43.22},
    {"n": "Botanischer Garten Zürich", "lat": 47.36, "lng": 8.56},
])
topup_items_p(d, 'tropenwald', [
    {"n": "Borneo-Regenwald (Kalimantan)", "lat": 0.5, "lng": 113.5},
    {"n": "Daintree Rainforest (Queensland, Australien)", "lat": -16.17, "lng": 145.42},
    {"n": "Atlantic Forest (Mata Atlântica, Brasilien)", "lat": -20.0, "lng": -41.5},
    {"n": "Valdivianischer Regenwald (Chile)", "lat": -40.5, "lng": -72.5},
    {"n": "Sri Lanka-Regenwald (Sinharaja)", "lat": 6.4, "lng": 80.47},
    {"n": "Cross River Regenwald (Nigeria/Kamerun)", "lat": 5.5, "lng": 9.0},
    {"n": "Western Ghats Regenwald (Indien)", "lat": 11.0, "lng": 76.5},
    {"n": "Papua-Neuguinea Regenwald (Madang)", "lat": -5.2, "lng": 145.8},
    {"n": "Taman Negara Regenwald (Malaysia)", "lat": 4.4, "lng": 102.5},
    {"n": "Darien-Regenwald (Panama/Kolumbien)", "lat": 7.7, "lng": -77.5},
])
save('pflanzen_pin.json', d)

print("Part 5 complete.")

# ─────────────────────────────────────────────
# sport_hl.json
# ─────────────────────────────────────────────
print("\n=== sport_hl.json ===")
d = load('sport_hl.json')

topup_items_hl(d, 'sport_marathon_alter', [
    {"name": "London Marathon (UK)", "val": 1981},
    {"name": "Berlin Marathon (Deutschland)", "val": 1974},
    {"name": "Tokyo Marathon (Japan)", "val": 2007},
    {"name": "Chicago Marathon (USA)", "val": 1977},
    {"name": "Paris Marathon (Frankreich)", "val": 1976},
])
topup_items_hl(d, 'sport_stadien_kapazitaet', [
    {"name": "Camp Nou (FC Barcelona, Spanien)", "val": 99},
])
topup_items_hl(d, 'sport_hochsprung_rekorde', [
    {"name": "Mutaz Essa Barshim (Katar WR indoor)", "val": 243},
    {"name": "Gianmarco Tamberi (Olympiasieger 2020)", "val": 237},
    {"name": "Patrik Sjöberg (Europäischer Rekord)", "val": 242},
    {"name": "Bohdan Bondarenko (Ukr. Outdoor)", "val": 246},
    {"name": "Blanka Vlasic (Kroatien, Frauen)", "val": 208},
])
topup_items_hl(d, 'sport_olympia_goldmedaillen', [
    {"name": "Usain Bolt (Sprint, Jamaika)", "val": 8},
    {"name": "Nadia Comăneci (Turnen, Rumänien)", "val": 5},
    {"name": "Carl Lewis (Sprint/Weitsprung, USA)", "val": 9},
    {"name": "Simone Biles (Turnen, USA)", "val": 7},
    {"name": "Mark Spitz (Schwimmen, USA)", "val": 9},
    {"name": "Jenny Thompson (Schwimmen, USA)", "val": 8},
    {"name": "Birgit Fischer (Kanu, Deutschland)", "val": 8},
])
topup_items_hl(d, 'sport_fussball_marktwert', [
    {"name": "Jude Bellingham (Real Madrid)", "val": 180},
    {"name": "Vinicius Jr. (Real Madrid)", "val": 180},
    {"name": "Pedri (FC Barcelona)", "val": 120},
    {"name": "Phil Foden (Manchester City)", "val": 150},
    {"name": "Lamine Yamal (FC Barcelona)", "val": 200},
    {"name": "Florian Wirtz (Bayer Leverkusen)", "val": 130},
    {"name": "Bukayo Saka (Arsenal FC)", "val": 150},
    {"name": "Rodri (Manchester City)", "val": 120},
])
topup_items_hl(d, 'sport_stadion_baujahr', [
    {"name": "Camp Nou (FC Barcelona, Spanien)", "val": 1957},
])
topup_items_hl(d, 'sport_tore_saison', [
    {"name": "Robert Lewandowski (Bundesliga 2020/21)", "val": 41},
])
save('sport_hl.json', d)

# ─────────────────────────────────────────────
# sport_match.json
# ─────────────────────────────────────────────
print("\n=== sport_match.json ===")
d = load('sport_match.json')

topup_items_nc(d, 'sport_teamgroesse', [
    {"n": "Basketball", "c": "5 Spieler"},
    {"n": "Baseball", "c": "9 Spieler"},
    {"n": "Rugby Union", "c": "15 Spieler"},
    {"n": "Rugby League", "c": "13 Spieler"},
    {"n": "Eishockey", "c": "6 Spieler"},
    {"n": "Volleyball", "c": "6 Spieler"},
    {"n": "Handball", "c": "7 Spieler"},
    {"n": "Polo", "c": "4 Spieler"},
    {"n": "Wasserball", "c": "7 Spieler"},
    {"n": "Cricket", "c": "11 Spieler"},
    {"n": "Curling", "c": "4 Spieler"},
    {"n": "Lacrosse (Feld)", "c": "10 Spieler"},
    {"n": "Korfball", "c": "8 Spieler"},
    {"n": "Netball", "c": "7 Spieler"},
    {"n": "Kabaddi", "c": "7 Spieler"},
])
topup_items_nc(d, 'sport_olympisch', [
    {"n": "Baseball/Softball", "c": "Ja (2020 Los Angeles)"},
    {"n": "Squash", "c": "Nein"},
    {"n": "Cricket", "c": "Nein"},
    {"n": "Polo", "c": "Nein"},
    {"n": "Karate", "c": "Ja (Tokio 2020)"},
    {"n": "Breakdance", "c": "Ja (Paris 2024)"},
    {"n": "Flag Football", "c": "Ja (Los Angeles 2028)"},
    {"n": "Lacrosse", "c": "Ja (Los Angeles 2028)"},
])
topup_items_nc(d, 'sport_nationalsport_match', [
    {"n": "Ice Hockey", "c": "Kanada"},
    {"n": "Hurling", "c": "Irland"},
    {"n": "Gaelic Football", "c": "Irland"},
    {"n": "Sepak Takraw", "c": "Malaysia"},
    {"n": "Muay Thai", "c": "Thailand"},
    {"n": "Taekwondo", "c": "Südkorea"},
    {"n": "Pelota Vasca", "c": "Spanien (Baskenland)"},
    {"n": "Shinty", "c": "Schottland"},
    {"n": "Buzkashi", "c": "Afghanistan"},
    {"n": "Bandy", "c": "Russland"},
    {"n": "Pato", "c": "Argentinien"},
    {"n": "Rodeo", "c": "USA"},
    {"n": "Naadam (Ringen)", "c": "Mongolei"},
])
topup_items_nc(d, 'sport_sportart_kontinent', [
    {"n": "Polo", "c": "Asien (Ursprung)"},
    {"n": "Kabaddi", "c": "Asien"},
    {"n": "Hurling", "c": "Europa (Irland)"},
    {"n": "Buzkashi", "c": "Asien"},
    {"n": "Naadam-Ringen", "c": "Asien"},
    {"n": "Pato", "c": "Südamerika"},
])
save('sport_match.json', d)

# ─────────────────────────────────────────────
# sport_pin.json
# ─────────────────────────────────────────────
print("\n=== sport_pin.json ===")
d = load('sport_pin.json')

topup_items_p(d, 'sport_marathonstrecken', [
    {"n": "Berlin Marathon Ziel (Brandenburger Tor)", "lat": 52.516, "lng": 13.378},
    {"n": "Tokyo Marathon Start (Shinjuku)", "lat": 35.69, "lng": 139.69},
    {"n": "Chicago Marathon Start (Grant Park)", "lat": 41.87, "lng": -87.62},
    {"n": "Paris Marathon Start (Arc de Triomphe)", "lat": 48.874, "lng": 2.295},
    {"n": "London Marathon Ziel (The Mall)", "lat": 51.502, "lng": -0.141},
    {"n": "Athens Classic Marathon Ziel (Panathinaiko-Stadion)", "lat": 37.97, "lng": 23.74},
    {"n": "Stockholm Marathon (Olympiastadion)", "lat": 59.34, "lng": 18.07},
    {"n": "Sydney Marathon Ziel (Opera House)", "lat": -33.86, "lng": 151.21},
    {"n": "Vienna City Marathon Ziel (Heldenplatz)", "lat": 48.205, "lng": 16.361},
])
topup_items_p(d, 'sport_fussballstadien', [
    {"n": "Signal Iduna Park (Borussia Dortmund)", "lat": 51.49, "lng": 7.45},
    {"n": "Estadio Azteca (Mexiko-Stadt)", "lat": 19.3, "lng": -99.15},
])
topup_items_p(d, 'sport_motorsport_strecken', [
    {"n": "Suzuka Circuit (Japan)", "lat": 34.84, "lng": 136.54},
    {"n": "Spa-Francorchamps (Belgien)", "lat": 50.44, "lng": 5.97},
    {"n": "Interlagos (São Paulo, Brasilien)", "lat": -23.7, "lng": -46.7},
    {"n": "Nürburgring Nordschleife (Deutschland)", "lat": 50.33, "lng": 6.94},
    {"n": "Circuit of the Americas (Austin, Texas)", "lat": 30.13, "lng": -97.64},
    {"n": "Silverstone Circuit (England)", "lat": 52.07, "lng": -1.02},
    {"n": "Bahrain International Circuit", "lat": 26.03, "lng": 50.51},
    {"n": "Yas Marina Circuit (Abu Dhabi)", "lat": 24.47, "lng": 54.6},
    {"n": "Mugello Circuit (Italien)", "lat": 43.99, "lng": 11.37},
    {"n": "Road Atlanta (Braselton, Georgia)", "lat": 34.15, "lng": -83.81},
])
topup_items_p(d, 'sport_wintersport_orte', [
    {"n": "Cortina d'Ampezzo (Italien) — Olympia 1956", "lat": 46.54, "lng": 12.14},
    {"n": "Sapporo (Japan) — Olympia 1972", "lat": 43.06, "lng": 141.35},
])
topup_items_p(d, 'sport_ski_pisten', [
    {"n": "Val Thorens (Frankreich) — höchste Skistation Europas", "lat": 45.3, "lng": 6.58},
    {"n": "Zermatt (Schweiz) — Klein Matterhorn", "lat": 45.98, "lng": 7.74},
    {"n": "Niseko (Japan) — bester Pulverschnee", "lat": 42.8, "lng": 140.69},
])
topup_items_p(d, 'sport_golf_platze', [
    {"n": "Pebble Beach Golf Links (Monterey, Kalifornien)", "lat": 36.57, "lng": -121.95},
    {"n": "Royal Birkdale Golf Club (Southport, England)", "lat": 53.63, "lng": -3.03},
    {"n": "Carnoustie Golf Links (Schottland)", "lat": 56.5, "lng": -2.72},
    {"n": "Pinehurst No. 2 (North Carolina, USA)", "lat": 35.19, "lng": -79.47},
])
topup_items_p(d, 'sport_surfspots_welt', [
    {"n": "Jeffreys Bay (Südafrika)", "lat": -34.05, "lng": 24.92},
    {"n": "Hossegor (Frankreich)", "lat": 43.67, "lng": -1.41},
    {"n": "Uluwatu (Bali, Indonesien)", "lat": -8.83, "lng": 115.09},
    {"n": "Snapper Rocks (Gold Coast, Australien)", "lat": -28.17, "lng": 153.55},
    {"n": "Mavericks (Half Moon Bay, Kalifornien)", "lat": 37.49, "lng": -122.5},
    {"n": "Todos Santos (Baja California, Mexiko)", "lat": 23.45, "lng": -110.22},
    {"n": "Mullaghmore Head (Irland)", "lat": 54.47, "lng": -8.45},
    {"n": "Skeleton Bay (Namibia)", "lat": -19.5, "lng": 12.6},
    {"n": "Puerto Escondido (Mexiko)", "lat": 15.86, "lng": -97.07},
    {"n": "Cloudbreak (Fidschi)", "lat": -17.87, "lng": 177.21},
])
topup_items_p(d, 'sport_klettergebiete', [
    {"n": "Kalymnos (Griechenland) — Sportklettern", "lat": 37.0, "lng": 26.98},
])
save('sport_pin.json', d)

print("Part 6 complete.")

# ─────────────────────────────────────────────
# tech_hl.json
# ─────────────────────────────────────────────
print("\n=== tech_hl.json ===")
d = load('tech_hl.json')

topup_items_hl(d, 'transistoren', [
    {"name": "AMD EPYC Genoa (9654)", "val": 90},
    {"name": "Apple M3 Pro", "val": 37},
    {"name": "Intel Meteor Lake (Core Ultra)", "val": 22},
    {"name": "Qualcomm Snapdragon 8 Gen 3", "val": 16},
    {"name": "NVIDIA RTX 4090 (Ada Lovelace)", "val": 76},
])
topup_items_hl(d, 'taktfrequenz', [
    {"name": "Intel Core i7-14700K (Boost)", "val": 5.6},
    {"name": "AMD Ryzen 9 7900X (Boost)", "val": 5.6},
])
topup_items_hl(d, 'code_zeilen', [
    {"name": "Windows 11", "val": 80},
    {"name": "Android AOSP", "val": 15},
    {"name": "Chromium-Browser", "val": 35},
])
topup_items_hl(d, 'release_jahr', [
    {"name": "C", "val": 1972},
    {"name": "Pascal", "val": 1970},
    {"name": "Prolog", "val": 1972},
    {"name": "Ada", "val": 1980},
    {"name": "C++", "val": 1983},
    {"name": "Objective-C", "val": 1984},
    {"name": "Erlang", "val": 1986},
    {"name": "Perl", "val": 1987},
    {"name": "Haskell", "val": 1990},
    {"name": "Python", "val": 1991},
    {"name": "Ruby", "val": 1995},
    {"name": "Java", "val": 1995},
    {"name": "JavaScript", "val": 1995},
    {"name": "PHP", "val": 1994},
    {"name": "Swift", "val": 2014},
    {"name": "Kotlin", "val": 2011},
    {"name": "Rust", "val": 2010},
])
topup_items_hl(d, 'internet_speed', [
    {"name": "Südkorea", "val": 255},
    {"name": "Dänemark", "val": 230},
    {"name": "Norwegen", "val": 220},
    {"name": "Japan", "val": 210},
    {"name": "Schweiz", "val": 195},
    {"name": "Deutschland", "val": 90},
    {"name": "Frankreich", "val": 145},
    {"name": "USA", "val": 167},
    {"name": "Schweden", "val": 185},
    {"name": "Finnland", "val": 175},
])
topup_items_hl(d, 'tdp', [
    {"name": "Apple M3 (Effizienzchip)", "val": 22},
])
save('tech_hl.json', d)

# ─────────────────────────────────────────────
# tech_match.json
# ─────────────────────────────────────────────
print("\n=== tech_match.json ===")
d = load('tech_match.json')

topup_items_nc(d, 'sensoren', [
    {"n": "BMP280", "c": "Luftdruck"},
    {"n": "MPU-6050", "c": "Beschleunigung/Gyroskop"},
    {"n": "HC-SR04", "c": "Ultraschall-Entfernung"},
    {"n": "DS18B20", "c": "Temperatur (wasserdicht)"},
    {"n": "MQ-2", "c": "Rauch/Gas"},
    {"n": "ADXL345", "c": "Beschleunigung"},
    {"n": "AS7262", "c": "Licht/Spektrum"},
    {"n": "HX711", "c": "Gewicht (Wägezelle)"},
    {"n": "MAX30100", "c": "Puls/SpO2"},
    {"n": "VL53L0X", "c": "Laser-Entfernung"},
    {"n": "CCS811", "c": "CO2/VOC-Luft"},
])
topup_items_nc(d, 'syntax', [
    {"n": "console.log('Hello World')", "c": "JavaScript"},
    {"n": "System.out.println('Hello')", "c": "Java"},
    {"n": "printf('Hello\\n')", "c": "C"},
    {"n": "echo 'Hello World'", "c": "PHP"},
    {"n": "puts 'Hello World'", "c": "Ruby"},
    {"n": "print('Hello World')", "c": "Python"},
    {"n": "fmt.Println('Hello')", "c": "Go"},
    {"n": "println!('Hello')", "c": "Rust"},
    {"n": "Console.WriteLine('Hi')", "c": "C#"},
    {"n": "NSLog(@'Hello')", "c": "Objective-C"},
])
topup_items_nc(d, 'osi', [
    {"n": "Ethernet", "c": "2 Sicherung"},
    {"n": "IP (Internet Protocol)", "c": "3 Netz"},
    {"n": "TLS/SSL", "c": "6 Darstellung"},
    {"n": "FTP", "c": "7 Anwendung"},
    {"n": "SMTP", "c": "7 Anwendung"},
    {"n": "DNS", "c": "7 Anwendung"},
    {"n": "PPP", "c": "2 Sicherung"},
    {"n": "ICMP (Ping)", "c": "3 Netz"},
    {"n": "UDP", "c": "4 Transport"},
    {"n": "NetBIOS", "c": "5 Sitzung"},
    {"n": "JPEG/MP3-Kompression", "c": "6 Darstellung"},
    {"n": "ARP", "c": "2 Sicherung"},
    {"n": "Glasfaser (physisch)", "c": "1 Physikalisch"},
    {"n": "Bluetooth (physisch)", "c": "1 Physikalisch"},
    {"n": "SSH", "c": "7 Anwendung"},
    {"n": "SNMP", "c": "7 Anwendung"},
])
topup_items_nc(d, 'bigo', [
    {"n": "Binäre Suche (sortiert)", "c": "O(log n)"},
    {"n": "Quicksort (Durchschnitt)", "c": "O(n log n)"},
    {"n": "Mergesort", "c": "O(n log n)"},
    {"n": "Bubble Sort", "c": "O(n²)"},
    {"n": "Heapsort", "c": "O(n log n)"},
    {"n": "Insertion Sort (Best Case)", "c": "O(n)"},
    {"n": "Fibonacci rekursiv (naiv)", "c": "O(2ⁿ)"},
    {"n": "Matrixmultiplikation (naiv)", "c": "O(n³)"},
    {"n": "Hash-Tabellen-Zugriff", "c": "O(1)"},
    {"n": "Breitensuche (BFS)", "c": "O(V+E)"},
    {"n": "Tiefensuche (DFS)", "c": "O(V+E)"},
])
topup_items_nc(d, 'http', [
    {"n": "400 Bad Request", "c": "4xx Client-Fehler"},
    {"n": "401 Unauthorized", "c": "4xx Client-Fehler"},
    {"n": "403 Forbidden", "c": "4xx Client-Fehler"},
    {"n": "404 Not Found", "c": "4xx Client-Fehler"},
    {"n": "500 Internal Server Error", "c": "5xx Server-Fehler"},
    {"n": "502 Bad Gateway", "c": "5xx Server-Fehler"},
    {"n": "503 Service Unavailable", "c": "5xx Server-Fehler"},
    {"n": "201 Created", "c": "2xx Erfolg"},
    {"n": "204 No Content", "c": "2xx Erfolg"},
    {"n": "302 Found (Redirect)", "c": "3xx Weiterleitung"},
    {"n": "304 Not Modified", "c": "3xx Weiterleitung"},
    {"n": "307 Temporary Redirect", "c": "3xx Weiterleitung"},
    {"n": "101 Switching Protocols", "c": "1xx Information"},
    {"n": "100 Continue", "c": "1xx Information"},
    {"n": "429 Too Many Requests", "c": "4xx Client-Fehler"},
    {"n": "418 I'm a teapot", "c": "4xx Client-Fehler"},
    {"n": "405 Method Not Allowed", "c": "4xx Client-Fehler"},
])
topup_items_nc(d, 'wahrheitstabellen', [
    {"n": "A=1, B=0 → 0", "c": "AND"},
    {"n": "A=1, B=1 → 1", "c": "AND"},
    {"n": "A=0, B=0 → 0", "c": "AND"},
    {"n": "A=0, B=0 → 0", "c": "OR"},
    {"n": "A=1, B=0 → 1", "c": "OR"},
    {"n": "A=1, B=1 → 1", "c": "OR"},
    {"n": "A=0 → 1", "c": "NOT"},
    {"n": "A=1 → 0", "c": "NOT"},
    {"n": "A=0, B=0 → 1", "c": "NAND"},
    {"n": "A=1, B=1 → 0", "c": "NAND"},
    {"n": "A=0, B=1 → 1", "c": "NAND"},
    {"n": "A=1, B=0 → 1", "c": "NAND"},
    {"n": "A=0, B=0 → 1", "c": "NOR"},
    {"n": "A=1, B=0 → 0", "c": "NOR"},
    {"n": "A=1, B=1 → 0", "c": "NOR"},
    {"n": "A=0, B=0 → 0", "c": "XOR"},
    {"n": "A=0, B=1 → 1", "c": "XOR"},
    {"n": "A=1, B=0 → 1", "c": "XOR"},
    {"n": "A=1, B=1 → 0", "c": "XOR"},
    {"n": "A=0, B=0 → 1", "c": "XNOR"},
    {"n": "A=1, B=1 → 1", "c": "XNOR"},
    {"n": "A=0, B=1 → 0", "c": "XNOR"},
    {"n": "A=1, B=0 → 0", "c": "XNOR"},
    {"n": "A=0, B=1 → 0", "c": "AND"},
    {"n": "A=0, B=1 → 0", "c": "AND"},
    {"n": "A=0, B=0 → 1", "c": "NAND"},
    {"n": "A=0, B=1 → 1", "c": "NOR"},
    {"n": "A=0, B=1 → 1", "c": "NOR"},
    {"n": "A=0, B=0 → 0", "c": "NOR"},
    {"n": "A=0, B=1 → 0", "c": "XNOR"},
])
topup_items_nc(d, 'hardware', [
    {"n": "ATX-Netzteil (850W 80+ Gold)", "c": "Stromversorgung"},
    {"n": "PCIe 5.0 x16 Slot", "c": "Erweiterungsbus"},
    {"n": "Thunderbolt 4 Controller", "c": "Schnittstelle"},
    {"n": "ECC RAM DIMM", "c": "RAM"},
    {"n": "ZFS RAIDZ2 Array", "c": "Speicher"},
    {"n": "TPM 2.0 Chip", "c": "Sicherheit"},
    {"n": "BIOS/UEFI Chip", "c": "Firmware"},
    {"n": "PCIe M.2 Heatsink", "c": "Kühlung"},
    {"n": "Fan Hub (PWM)", "c": "Kühlung"},
    {"n": "DDR5 SO-DIMM (Laptop)", "c": "RAM"},
])
topup_items_nc(d, 'erfinder', [
    {"n": "Transistor (1947)", "c": "Shockley / Bardeen / Brattain"},
    {"n": "C-Programmiersprache", "c": "Dennis Ritchie"},
    {"n": "UNIX", "c": "Ken Thompson & Dennis Ritchie"},
    {"n": "Linux-Kernel", "c": "Linus Torvalds"},
    {"n": "Python", "c": "Guido van Rossum"},
    {"n": "Java", "c": "James Gosling"},
    {"n": "iPhone (Smartphone-Ära)", "c": "Steve Jobs / Apple"},
    {"n": "Ethernet", "c": "Robert Metcalfe"},
    {"n": "RSA-Verschlüsselung", "c": "Rivest / Shamir / Adleman"},
    {"n": "PageRank-Algorithmus", "c": "Larry Page"},
    {"n": "Deep Learning (Backprop)", "c": "Geoffrey Hinton"},
])
topup_items_nc(d, 'portnummern', [
    {"n": "Port 21", "c": "FTP"},
    {"n": "Port 22", "c": "SSH"},
    {"n": "Port 23", "c": "Telnet"},
    {"n": "Port 25", "c": "SMTP"},
    {"n": "Port 53", "c": "DNS"},
    {"n": "Port 110", "c": "POP3"},
    {"n": "Port 143", "c": "IMAP"},
    {"n": "Port 3306", "c": "MySQL"},
    {"n": "Port 5432", "c": "PostgreSQL"},
    {"n": "Port 6379", "c": "Redis"},
    {"n": "Port 27017", "c": "MongoDB"},
    {"n": "Port 8080", "c": "HTTP Alternativ"},
    {"n": "Port 3389", "c": "RDP"},
    {"n": "Port 8443", "c": "HTTPS Alternativ"},
    {"n": "Port 1194", "c": "OpenVPN"},
    {"n": "Port 5900", "c": "VNC"},
    {"n": "Port 161", "c": "SNMP"},
    {"n": "Port 500", "c": "IKE/IPSec"},
])
topup_items_nc(d, 'dateiendungen', [
    {"n": ".svg", "c": "Vektorgrafik"},
    {"n": ".webp", "c": "Bild"},
    {"n": ".flac", "c": "Audio"},
    {"n": ".mkv", "c": "Video"},
    {"n": ".json", "c": "Datenaustausch"},
    {"n": ".yaml / .yml", "c": "Konfiguration"},
    {"n": ".toml", "c": "Konfiguration"},
    {"n": ".wasm", "c": "WebAssembly"},
])
topup_items_nc(d, 'smart_home', [
    {"n": "Zigbee2MQTT Koordinator", "c": "Zigbee"},
    {"n": "Philips Hue Bridge", "c": "Zigbee"},
    {"n": "IKEA Trådfri Gateway", "c": "Zigbee"},
    {"n": "Sonos Arc Soundbar", "c": "WLAN"},
    {"n": "Eufy RoboVac (WLAN)", "c": "WLAN"},
    {"n": "Google Nest Hub", "c": "Google Home"},
    {"n": "Amazon Echo Dot", "c": "Amazon Alexa"},
    {"n": "Apple HomePod Mini", "c": "Apple HomeKit"},
    {"n": "Fibaro Z-Wave Controller", "c": "Z-Wave"},
    {"n": "Bosch Smart Home Controller", "c": "Bosch"},
])
topup_items_nc(d, 'akronyme', [
    {"n": "DNS", "c": "Domain Name System"},
    {"n": "VPN", "c": "Virtual Private Network"},
    {"n": "SSH", "c": "Secure Shell"},
    {"n": "HTML", "c": "HyperText Markup Language"},
    {"n": "CSS", "c": "Cascading Style Sheets"},
    {"n": "SQL", "c": "Structured Query Language"},
    {"n": "ORM", "c": "Object-Relational Mapping"},
    {"n": "CDN", "c": "Content Delivery Network"},
])
topup_items_nc(d, 'turing_award', [
    {"n": "Leslie Lamport", "c": "Verteilte Systeme & LaTeX (2013)"},
    {"n": "Yann LeCun / Geoffrey Hinton / Yoshua Bengio", "c": "Deep Learning (2018)"},
    {"n": "Avi Wigderson", "c": "Theoretische Informatik & Pseudozufall (2021)"},
    {"n": "Silvio Micali / Shafi Goldwasser", "c": "Kryptografie (2012)"},
    {"n": "Barbara Liskov", "c": "Abstraktionskonzepte in OOP (2008)"},
    {"n": "Frances E. Allen", "c": "Compileroptimierung (2006)"},
])
topup_items_nc(d, 'erste_videospiele', [
    {"n": "Tennis for Two (Oscilloscope)", "c": "1950er"},
    {"n": "Space Invaders (Taito)", "c": "1970er"},
    {"n": "Asteroids (Atari)", "c": "1970er"},
    {"n": "Donkey Kong (Nintendo)", "c": "1980er"},
    {"n": "Tetris (Pajitnov)", "c": "1980er"},
    {"n": "Super Mario Bros.", "c": "1980er"},
    {"n": "The Legend of Zelda", "c": "1980er"},
    {"n": "Doom (id Software)", "c": "1990er"},
    {"n": "Quake (id Software)", "c": "1990er"},
    {"n": "Half-Life (Valve)", "c": "1990er"},
])
topup_items_nc(d, 'malware', [
    {"n": "Stuxnet (2010)", "c": "Wurm / Cyberwaffe"},
    {"n": "Mirai Botnet (2016)", "c": "Botnet (IoT)"},
    {"n": "NotPetya (2017)", "c": "Wiper / Ransomware"},
    {"n": "CryptoLocker (2013)", "c": "Ransomware"},
    {"n": "Zeus (2007)", "c": "Trojaner (Banking)"},
    {"n": "Conficker (2008)", "c": "Wurm"},
    {"n": "BlackEnergy (2015)", "c": "Trojaner (Infrastruktur)"},
    {"n": "Emotet (2014)", "c": "Trojaner / Downloader"},
    {"n": "Ryuk (2018)", "c": "Ransomware"},
    {"n": "Pegasus (NSO Group)", "c": "Spyware"},
])
topup_items_nc(d, 'tech_ma', [
    {"n": "YouTube", "c": "Google/Alphabet"},
    {"n": "Instagram", "c": "Meta"},
    {"n": "WhatsApp", "c": "Meta"},
    {"n": "Motorola Mobility", "c": "Google/Alphabet"},
    {"n": "Beats Electronics", "c": "Apple"},
    {"n": "Shazam", "c": "Apple"},
    {"n": "Nokia Handysparte", "c": "Microsoft"},
    {"n": "Skype", "c": "Microsoft"},
    {"n": "Twitch", "c": "Amazon"},
    {"n": "Whole Foods Market", "c": "Amazon"},
])
save('tech_match.json', d)

print("Part 7 complete.")

# ─────────────────────────────────────────────
# tech_pin.json
# ─────────────────────────────────────────────
print("\n=== tech_pin.json ===")
d = load('tech_pin.json')

topup_items_p(d, 'programmiersprachen', [
    {"n": "Java (Sun Microsystems, Santa Clara)", "lat": 37.37, "lng": -121.97},
    {"n": "Ruby (Matsumoto, Japan)", "lat": 35.54, "lng": 133.08},
    {"n": "Go (Google, Mountain View)", "lat": 37.42, "lng": -122.08},
    {"n": "Rust (Mozilla, San Francisco)", "lat": 37.77, "lng": -122.42},
    {"n": "Swift (Apple, Cupertino)", "lat": 37.33, "lng": -122.03},
    {"n": "Kotlin (JetBrains, Saint Petersburg)", "lat": 59.95, "lng": 30.32},
])
topup_items_p(d, 'halbleiter', [
    {"n": "Intel Fab 34 (Leixlip, Irland)", "lat": 53.36, "lng": -6.49},
    {"n": "GlobalFoundries Fab 8 (Malta, New York)", "lat": 42.99, "lng": -73.79},
])
topup_items_p(d, 'rechenzentren', [
    {"n": "Equinix NY4 (Secaucus, New Jersey)", "lat": 40.79, "lng": -74.07},
    {"n": "Iron Mountain Data Center (Manassas, Virginia)", "lat": 38.75, "lng": -77.48},
    {"n": "Facebook (Meta) Data Center (Lulea, Schweden)", "lat": 65.58, "lng": 22.16},
    {"n": "Apple Data Center (Viborg, Dänemark)", "lat": 56.45, "lng": 9.4},
    {"n": "Google Data Center (Hamina, Finnland)", "lat": 60.56, "lng": 27.2},
    {"n": "Switch SUPERNAP (Las Vegas, Nevada)", "lat": 36.13, "lng": -115.1},
    {"n": "Yandex Data Center (Mäntsälä, Finnland)", "lat": 60.63, "lng": 25.32},
    {"n": "Amazon AWS (Columbus, Ohio)", "lat": 39.96, "lng": -83.0},
    {"n": "Alibaba Cloud Data Center (Hangzhou)", "lat": 30.27, "lng": 120.15},
])
topup_items_p(d, 'pioniere', [
    {"n": "Tim Berners-Lee (CERN, Genf)", "lat": 46.23, "lng": 6.05},
    {"n": "Dennis Ritchie (Murray Hill, NJ)", "lat": 40.69, "lng": -74.4},
])
topup_items_p(d, 'tech_museen', [
    {"n": "Science Museum London (UK)", "lat": 51.498, "lng": -0.174},
    {"n": "Heinz Nixdorf MuseumsForum (Paderborn)", "lat": 51.72, "lng": 8.76},
    {"n": "Ars Electronica Center (Linz, Österreich)", "lat": 48.31, "lng": 14.29},
    {"n": "Cité des Sciences (Paris, Frankreich)", "lat": 48.89, "lng": 2.39},
    {"n": "National Museum of Computing (Bletchley Park)", "lat": 52.0, "lng": -0.74},
    {"n": "Computer Museum (Boston, Massachusetts)", "lat": 42.36, "lng": -71.05},
    {"n": "Informatik-Sammlung Erlangen (FAU)", "lat": 49.6, "lng": 11.0},
])
topup_items_p(d, 'supercomputer', [
    {"n": "Tianhe-2A (Guangzhou, China)", "lat": 23.13, "lng": 113.26},
    {"n": "Perlmutter (NERSC, Berkeley, Kalifornien)", "lat": 37.88, "lng": -122.25},
    {"n": "Fugaku (RIKEN, Kobe, Japan)", "lat": 34.69, "lng": 135.19},
    {"n": "Summit (Oak Ridge, Tennessee)", "lat": 35.93, "lng": -84.31},
    {"n": "Leonardo (CINECA, Bologna, Italien)", "lat": 44.51, "lng": 11.35},
    {"n": "MareNostrum 5 (Barcelona, Spanien)", "lat": 41.39, "lng": 2.11},
    {"n": "LUMI (CSC, Kajaani, Finnland)", "lat": 64.22, "lng": 27.73},
    {"n": "Jülich Supercomputing Centre (Deutschland)", "lat": 50.91, "lng": 6.41},
    {"n": "MN4 Marenostrum (BSC, Barcelona)", "lat": 41.39, "lng": 2.11},
])
save('tech_pin.json', d)

print("Part 8 complete.")

# ─────────────────────────────────────────────
# tiere_hl.json
# ─────────────────────────────────────────────
print("\n=== tiere_hl.json ===")
d = load('tiere_hl.json')

topup_items_hl(d, 'gewicht_land', [
    {"name": "Afrikanische Elefantenschildkröte", "val": 300},
    {"name": "Gaur (Wildrind)", "val": 1000},
    {"name": "Eisbär", "val": 700},
])
topup_items_hl(d, 'gewicht_meer', [
    {"name": "Walhai", "val": 21500},
    {"name": "Weißer Hai", "val": 2268},
    {"name": "Großer Hammerhai", "val": 580},
    {"name": "Orca (Orcinus orca)", "val": 5600},
    {"name": "Beluga-Wal", "val": 1600},
    {"name": "Narwal", "val": 1600},
    {"name": "Delfin (Großer Tümmler)", "val": 300},
    {"name": "Seehund", "val": 130},
    {"name": "Seelöwe (Kalifornisch)", "val": 300},
    {"name": "Stellersche Seekuh (ausgestorben)", "val": 8000},
])
topup_items_hl(d, 'speed_land', [
    {"name": "Springbock (Antilocapra)", "val": 88},
    {"name": "Löwe", "val": 80},
    {"name": "Thomson-Gazelle", "val": 80},
    {"name": "Gepard (Dauerlauf)", "val": 72},
    {"name": "Wildhund (Afrikanischer)", "val": 70},
])
topup_items_hl(d, 'speed_luft', [
    {"name": "Alpensegler (Apus melba)", "val": 170},
    {"name": "Große Meerente (Somateria)", "val": 76},
    {"name": "Kanada-Gans", "val": 90},
    {"name": "Weißstorch", "val": 80},
    {"name": "Kolibri (Hovering)", "val": 49},
    {"name": "Silbermöwe", "val": 55},
    {"name": "Fischadler (Sturzflug)", "val": 130},
    {"name": "Goldadler (Sturzflug)", "val": 250},
    {"name": "Falke (Sakerfalke)", "val": 200},
    {"name": "Taucher (Sturzflug)", "val": 140},
])
topup_items_hl(d, 'speed_wasser', [
    {"name": "Atlantischer Blaubarsch (Striped Bass)", "val": 40},
    {"name": "Roter Thunfisch", "val": 70},
    {"name": "Dolphin (Tursiops)", "val": 60},
    {"name": "Tigerhai", "val": 53},
    {"name": "Mako-Hai", "val": 74},
])
topup_items_hl(d, 'lebenserwartung', [
    {"name": "Europäische Sumpfschildkröte", "val": 120},
])
topup_items_hl(d, 'traechtigkeit', [
    {"name": "Orca (Schwerwal)", "val": 510},
    {"name": "Gepard", "val": 90},
    {"name": "Tigerin", "val": 104},
    {"name": "Löwin", "val": 110},
    {"name": "Schwein (Sus scrofa)", "val": 114},
    {"name": "Schaf (Ovis aries)", "val": 147},
])
topup_items_hl(d, 'gift', [
    {"name": "Blauring-Oktopus", "val": 10000},
    {"name": "Irukandji-Qualle", "val": 40000},
    {"name": "Kastenqualle (Chironex fleckeri)", "val": 10000},
    {"name": "Kegelschnecke (Conus geographus)", "val": 5000},
    {"name": "Goldener Pfeilgiftfrosch (D. auratus)", "val": 15000},
    {"name": "Steiniger Feuerfisch", "val": 500},
    {"name": "Stonefish (Synanceia)", "val": 700},
    {"name": "Kamm-Krokodil (indirekt gefährlich)", "val": 100},
    {"name": "Braune Einsiedlerspinne", "val": 660},
    {"name": "Kobra (Naja naja)", "val": 350},
])
topup_items_hl(d, 'pferde_stockmass', [
    {"name": "Clydesdale", "val": 165},
    {"name": "Shire Horse", "val": 175},
    {"name": "Thoroughbred (Vollblut)", "val": 163},
    {"name": "Andalusier", "val": 158},
    {"name": "Arabisches Vollblut", "val": 153},
])
topup_items_hl(d, 'pferde_gewicht', [
    {"name": "Fjordpferd", "val": 550},
    {"name": "Lusitano", "val": 540},
    {"name": "Arabisches Vollblut", "val": 450},
    {"name": "Thoroughbred", "val": 500},
    {"name": "Haflinger", "val": 550},
    {"name": "Trakehner", "val": 500},
    {"name": "Appaloosa", "val": 520},
    {"name": "Quarter Horse", "val": 550},
    {"name": "Mustang (Wildpferd)", "val": 400},
    {"name": "Miniaturpferd (Mini)", "val": 90},
    {"name": "Paso Fino", "val": 380},
    {"name": "Percheron (Kaltblut)", "val": 1000},
])
save('tiere_hl.json', d)

# ─────────────────────────────────────────────
# tiere_match.json
# ─────────────────────────────────────────────
print("\n=== tiere_match.json ===")
d = load('tiere_match.json')

topup_items_nc(d, 'ernaehrung', [
    {"n": "Pandabär", "c": "Herbivor"},
])
topup_items_nc(d, 'arktis_antarktis', [
    {"n": "Eisfuchs", "c": "Arktis (Nordpol)"},
    {"n": "Schneelemming", "c": "Arktis (Nordpol)"},
    {"n": "Rentier (Karibu)", "c": "Arktis (Nordpol)"},
])
topup_items_nc(d, 'pelagial', [
    {"n": "Tiefsee-Tintenfisch (Architeuthis)", "c": "Bathypelagial (1000-4000m)"},
])
topup_items_nc(d, 'gift_hotspots', [
    {"n": "Kastenqualle (Chironex fleckeri)", "c": "Australien"},
    {"n": "Kobra (Spectacled Cobra)", "c": "Indien"},
    {"n": "Tödliche Webspinne (Atrax robustus)", "c": "Australien"},
    {"n": "Boomslang (Dispholidus typus)", "c": "Südafrika"},
])
topup_items_nc(d, 'migranten', [
    {"n": "Weißstorch", "c": "Subsahara-Afrika (Überwinterung)"},
    {"n": "Walross (Atlantik)", "c": "Arktis (Sommer)"},
    {"n": "Buckelwal", "c": "Polargewässer (Sommer)"},
    {"n": "Pazifische Lachse (Chinook)", "c": "Pazifik → Süßwasser"},
])
topup_items_nc(d, 'pferde_fachbegriffe', [
    {"n": "Schecke", "c": "Weißfleckiges Pferd"},
    {"n": "Apfelschimmel", "c": "Graues Pferd mit runden Flecken"},
    {"n": "Tigerschecke (Appaloosa)", "c": "Geflecktes Pferd (Appaloosa-Typ)"},
    {"n": "Palomino", "c": "Goldgelbes Pferd"},
    {"n": "Roan (Roano)", "c": "Gemischtfarbiges Fell (weiß + Basisfarbe)"},
])
save('tiere_match.json', d)

print("Part 9 complete.")

# ─────────────────────────────────────────────
# kultur.json  (list-valued keys: n/c or pin or mixed)
# ─────────────────────────────────────────────
print("\n=== kultur.json ===")
d = load('kultur.json')

# n/c format keys
def _n(x):
    return x.get('n', x.get('name', ''))

def ku_nc(k, items):
    existing = {_n(x) for x in d[k]}
    added = [x for x in items if x['n'] not in existing]
    needed = max(0, 50 - len(d[k]))
    d[k].extend(added[:max(needed, len(added))])
    print(f'  {k}: {len(d[k])} items')

# pin format keys (lat/lng)
def ku_pin(k, items):
    existing = {_n(x) for x in d[k]}
    added = [x for x in items if x['n'] not in existing]
    needed = max(0, 50 - len(d[k]))
    d[k].extend(added[:max(needed, len(added))])
    print(f'  {k}: {len(d[k])} items')

# mixed keys (wein_regionen, museen, kunstwerke, filmsets, ruinen, etc. have lat/lng/c)
def ku_mix(k, items):
    existing = {_n(x) for x in d[k]}
    added = [x for x in items if x['n'] not in existing]
    needed = max(0, 50 - len(d[k]))
    d[k].extend(added[:max(needed, len(added))])
    print(f'  {k}: {len(d[k])} items')

# wolkenkratzer has n/c/val
def ku_wolkenkratzer(items):
    existing = {_n(x) for x in d['wolkenkratzer']}
    added = [x for x in items if x['n'] not in existing]
    needed = max(0, 50 - len(d['wolkenkratzer']))
    d['wolkenkratzer'].extend(added[:max(needed, len(added))])
    print(f'  wolkenkratzer: {len(d["wolkenkratzer"])} items')

ku_nc('getraenke', [
    {"n": "Kvas", "c": "Russland"},
    {"n": "Tejuino", "c": "Mexiko"},
    {"n": "Kvass (fermentiert)", "c": "Ukraine"},
    {"n": "Lassi (Mango)", "c": "Indien"},
    {"n": "Tamarindenwasser", "c": "Mexiko"},
    {"n": "Ayran", "c": "Türkei"},
    {"n": "Kvöldmjólk (Buttermilch)", "c": "Island"},
    {"n": "Horchata de Chufa", "c": "Spanien"},
    {"n": "Teh Tarik", "c": "Malaysia"},
])
ku_nc('streetfood', [
    {"n": "Arepas", "c": "Kolumbien"},
    {"n": "Bao Buns", "c": "Taiwan"},
    {"n": "Somtam (Papayasalat)", "c": "Thailand"},
    {"n": "Jerk Chicken", "c": "Jamaika"},
    {"n": "Falafel", "c": "Israel"},
    {"n": "Tostadas", "c": "Mexiko"},
])
ku_nc('kaese', [
    {"n": "Roquefort", "c": "Frankreich"},
    {"n": "Manchego", "c": "Spanien"},
    {"n": "Grana Padano", "c": "Italien"},
    {"n": "Ricotta", "c": "Italien"},
    {"n": "Halloumi", "c": "Zypern"},
    {"n": "Limburger", "c": "Belgien"},
    {"n": "Gruyère", "c": "Schweiz"},
    {"n": "Epoisses", "c": "Frankreich"},
    {"n": "Jarlsberg", "c": "Norwegen"},
    {"n": "Tilsiter", "c": "Deutschland"},
    {"n": "Mimolette", "c": "Frankreich"},
    {"n": "Gjetost (Brunost)", "c": "Norwegen"},
])
ku_nc('suessspeisen', [
    {"n": "Stroopwafel", "c": "Niederlande"},
    {"n": "Pastel de Nata", "c": "Portugal"},
    {"n": "Mochi", "c": "Japan"},
    {"n": "Loukoumades", "c": "Griechenland"},
    {"n": "Sfumato (Rauchige Schokolade)", "c": "Mexiko"},
    {"n": "Gulab Jamun", "c": "Indien"},
    {"n": "Pavlova", "c": "Australien"},
])
ku_nc('kaffee', [
    {"n": "Café de Olla", "c": "Mexiko"},
    {"n": "Bulletproof Coffee", "c": "USA"},
    {"n": "Café Bombón", "c": "Spanien"},
    {"n": "Egg Coffee (Cà Phê Trứng)", "c": "Vietnam"},
    {"n": "Spiced Coffee (Kahwa)", "c": "Jemen"},
    {"n": "Dalgona Coffee", "c": "Südkorea"},
    {"n": "Freddo Espresso", "c": "Griechenland"},
    {"n": "Cafezinho", "c": "Brasilien"},
])
ku_nc('taenze', [
    {"n": "Capoeira", "c": "Brasilien"},
    {"n": "Polka", "c": "Tschechien"},
    {"n": "Tsifteteli", "c": "Griechenland"},
    {"n": "Zorba (Sirtaki)", "c": "Griechenland"},
    {"n": "Cumbia", "c": "Kolumbien"},
    {"n": "Moribayasa", "c": "Guinea"},
    {"n": "Kathak", "c": "Indien"},
    {"n": "Morris Dance", "c": "England"},
])
ku_nc('kleidung', [
    {"n": "Dirndl", "c": "Deutschland"},
    {"n": "Ao Dai", "c": "Vietnam"},
    {"n": "Cheongsam (Qipao)", "c": "China"},
    {"n": "Aso Oke", "c": "Nigeria"},
    {"n": "Leinenhose (Guayabera)", "c": "Kuba"},
    {"n": "Poncho", "c": "Peru"},
    {"n": "Seide-Kimono", "c": "Japan"},
    {"n": "Lederhose (Bayern)", "c": "Deutschland"},
])
ku_nc('instrumente', [
    {"n": "Didgeridoo", "c": "Australien"},
    {"n": "Berimbau", "c": "Brasilien"},
    {"n": "Morin Khuur (Pferdekopfgeige)", "c": "Mongolei"},
    {"n": "Kora", "c": "Westafrika"},
    {"n": "Charango", "c": "Bolivien"},
    {"n": "Duduk", "c": "Armenien"},
    {"n": "Shamisen", "c": "Japan"},
    {"n": "Hang Drum", "c": "Schweiz"},
])
ku_nc('literatur', [
    {"n": "Miguel de Cervantes (Don Quijote)", "c": "Spanien"},
    {"n": "Leo Tolstoi (Krieg und Frieden)", "c": "Russland"},
    {"n": "Fjodor Dostojewski", "c": "Russland"},
    {"n": "Naguib Mahfouz (Nobelpreis)", "c": "Ägypten"},
    {"n": "Gabriel García Márquez", "c": "Kolumbien"},
    {"n": "Chinua Achebe (Okonkwo)", "c": "Nigeria"},
    {"n": "Haruki Murakami", "c": "Japan"},
    {"n": "Jorge Luis Borges", "c": "Argentinien"},
    {"n": "Pablo Neruda (Lyrik)", "c": "Chile"},
    {"n": "Wislawa Szymborska (Nobelpreis)", "c": "Polen"},
])
ku_nc('wahrzeichen', [
    {"n": "Sagrada Família", "c": "Spanien"},
    {"n": "Big Ben (Elizabeth Tower)", "c": "Vereinigtes Königreich"},
    {"n": "Freiheitsstatue", "c": "USA"},
    {"n": "Akropolis", "c": "Griechenland"},
    {"n": "Angkor Wat", "c": "Kambodscha"},
    {"n": "Machu Picchu", "c": "Peru"},
    {"n": "Chichen Itza", "c": "Mexiko"},
    {"n": "Ayers Rock (Uluru)", "c": "Australien"},
    {"n": "Große Mauer von China", "c": "China"},
    {"n": "Kreml (Moskau)", "c": "Russland"},
    {"n": "Neuschwanstein", "c": "Deutschland"},
    {"n": "Hagia Sophia", "c": "Türkei"},
    {"n": "Alhambra", "c": "Spanien"},
])
ku_nc('feste', [
    {"n": "Songkran (Wasserfest)", "c": "Thailand"},
    {"n": "Holi (Farbfest)", "c": "Indien"},
    {"n": "Mardi Gras", "c": "USA"},
    {"n": "Inti Raymi (Sonnenfest)", "c": "Peru"},
    {"n": "Hanami (Kirschblüte)", "c": "Japan"},
    {"n": "Day of the Dead", "c": "Mexiko"},
    {"n": "Nowruz (Persisches Neujahr)", "c": "Iran"},
    {"n": "Onam (Erntedankfest)", "c": "Indien"},
])
ku_nc('begruessung', [
    {"n": "Hongi (Nasen-Stirn-Berührung)", "c": "Neuseeland"},
    {"n": "Knicks (formell)", "c": "Deutschland"},
    {"n": "Wai (Hände falten)", "c": "Thailand"},
])
ku_nc('feiertage', [
    {"n": "Diwali (variabel)", "c": "Indien"},
    {"n": "Nowruz (21. März)", "c": "Iran"},
    {"n": "Eid al-Fitr (variabel)", "c": "Saudi-Arabien"},
    {"n": "Setsubun (3./4. Februar)", "c": "Japan"},
    {"n": "Chuseok (variabel)", "c": "Südkorea"},
    {"n": "Vesak (variabel)", "c": "Sri Lanka"},
    {"n": "Guy Fawkes Night (5. Nov.)", "c": "Vereinigtes Königreich"},
    {"n": "Liberation Day (25. April)", "c": "Italien"},
])
ku_nc('erfindungen', [
    {"n": "Druckmaschine (Gutenberg)", "c": "Deutschland"},
    {"n": "Zeppelin (Luftschiff)", "c": "Deutschland"},
    {"n": "Aspirin", "c": "Deutschland"},
    {"n": "Automobile (Benz Patent-Motorwagen)", "c": "Deutschland"},
    {"n": "Penicillin", "c": "Vereinigtes Königreich"},
    {"n": "Radar", "c": "Vereinigtes Königreich"},
])
ku_nc('exporte', [
    {"n": "Autoteile", "c": "Deutschland"},
    {"n": "Edelsteine / Diamanten", "c": "Botsuana"},
    {"n": "Getreide (Weizen)", "c": "Russland"},
    {"n": "Öl / Erdgas", "c": "Norwegen"},
    {"n": "Lithium", "c": "Chile"},
    {"n": "Kakao", "c": "Côte d'Ivoire"},
    {"n": "Tee", "c": "Kenia"},
    {"n": "Fisch (Lachs)", "c": "Norwegen"},
    {"n": "Vanille", "c": "Madagaskar"},
])
ku_nc('blumen', [
    {"n": "Lavendel", "c": "Frankreich"},
    {"n": "Wattle (Akazie)", "c": "Australien"},
    {"n": "Kamelie", "c": "Japan"},
    {"n": "Sonnenblume", "c": "Ukraine"},
    {"n": "Protea", "c": "Südafrika"},
    {"n": "Bougainvillea", "c": "Brasilien"},
    {"n": "Orchidee (Vanda Miss Joaquim)", "c": "Singapur"},
    {"n": "Lisianthus (Eustoma)", "c": "USA"},
    {"n": "Frangipani (Plumeria)", "c": "Indonesien"},
])
ku_nc('entdecker', [
    {"n": "Vasco da Gama", "c": "Portugal"},
    {"n": "Ferdinand Magellan", "c": "Portugal"},
    {"n": "Christopher Columbus", "c": "Spanien"},
    {"n": "Roald Amundsen", "c": "Norwegen"},
    {"n": "Alexander von Humboldt", "c": "Deutschland"},
    {"n": "David Livingstone", "c": "Vereinigtes Königreich"},
    {"n": "Ibn Battuta", "c": "Marokko"},
    {"n": "Amerigo Vespucci", "c": "Italien"},
    {"n": "Zheng He", "c": "China"},
    {"n": "Leif Eriksson", "c": "Island"},
    {"n": "Pedro Álvares Cabral", "c": "Portugal"},
    {"n": "Willem Barentsz", "c": "Niederlande"},
    {"n": "Hernán Cortés", "c": "Spanien"},
    {"n": "Henry Hudson", "c": "England"},
    {"n": "Bartholomeu Dias", "c": "Portugal"},
    {"n": "Walter Raleigh", "c": "England"},
    {"n": "Bjarni Herjólfsson", "c": "Island"},
    {"n": "Ponce de León", "c": "Spanien"},
])
ku_nc('sport', [
    {"n": "Sepak Takraw", "c": "Malaysia"},
    {"n": "Hurling", "c": "Irland"},
    {"n": "Buzkashi", "c": "Afghanistan"},
    {"n": "Capoeira (Kampfsport)", "c": "Brasilien"},
    {"n": "Pelota Vasca", "c": "Spanien"},
    {"n": "Pato (Polo mit Ball)", "c": "Argentinien"},
    {"n": "Kabaddi (offiziell)", "c": "Indien"},
    {"n": "Korfball", "c": "Niederlande"},
    {"n": "Shinty", "c": "Schottland"},
    {"n": "Muay Thai", "c": "Thailand"},
    {"n": "Wushu", "c": "China"},
    {"n": "Polo", "c": "Pakistan"},
    {"n": "Bodenschwimmen (Bog Snorkelling)", "c": "Wales"},
])
ku_nc('brettspiele', [
    {"n": "Ludo", "c": "Indien"},
    {"n": "Go", "c": "China"},
    {"n": "Mancala", "c": "Afrika"},
    {"n": "Senet", "c": "Ägypten"},
    {"n": "Parchís", "c": "Spanien"},
])
# wein_regionen has lat/lng/c format
ku_mix('wein_regionen', [
    {"n": "Rioja", "lat": 42.44, "lng": -2.7, "c": "Spanien"},
    {"n": "Priorat (Priorat DO)", "lat": 41.2, "lng": 0.86, "c": "Spanien"},
    {"n": "Tuscany (Chianti)", "lat": 43.55, "lng": 11.12, "c": "Italien"},
    {"n": "Barossa Valley", "lat": -34.5, "lng": 139.0, "c": "Australien"},
    {"n": "Mendoza (Malbec)", "lat": -32.89, "lng": -68.83, "c": "Argentinien"},
    {"n": "Mosel (Riesling)", "lat": 49.95, "lng": 7.15, "c": "Deutschland"},
    {"n": "Rhône Valley (Côtes du Rhône)", "lat": 44.5, "lng": 4.8, "c": "Frankreich"},
    {"n": "Champagne (Reims)", "lat": 49.26, "lng": 4.03, "c": "Frankreich"},
    {"n": "Marlborough (Sauvignon Blanc)", "lat": -41.52, "lng": 173.96, "c": "Neuseeland"},
])
# museen: lat/lng/c
ku_mix('museen', [
    {"n": "Metropolitan Museum of Art (New York)", "lat": 40.779, "lng": -73.963, "c": "USA"},
    {"n": "Prado (Madrid)", "lat": 40.414, "lng": -3.692, "c": "Spanien"},
    {"n": "Uffizien (Florenz)", "lat": 43.768, "lng": 11.255, "c": "Italien"},
    {"n": "Vatikanische Museen", "lat": 41.906, "lng": 12.453, "c": "Vatikan"},
    {"n": "National Palace Museum (Taipei)", "lat": 25.102, "lng": 121.548, "c": "Taiwan"},
    {"n": "Guggenheim Bilbao", "lat": 43.268, "lng": -2.934, "c": "Spanien"},
    {"n": "Rijksmuseum (Amsterdam)", "lat": 52.36, "lng": 4.885, "c": "Niederlande"},
    {"n": "Smithsonian National Museum (Washington)", "lat": 38.888, "lng": -77.026, "c": "USA"},
    {"n": "Hermitage (St. Petersburg)", "lat": 59.941, "lng": 30.314, "c": "Russland"},
    {"n": "National Museum of China (Peking)", "lat": 39.906, "lng": 116.394, "c": "China"},
    {"n": "Musée d'Orsay (Paris)", "lat": 48.86, "lng": 2.326, "c": "Frankreich"},
])
# kunstwerke: lat/lng/c
ku_mix('kunstwerke', [
    {"n": "Guernica (Museo Reina Sofía, Madrid)", "lat": 40.408, "lng": -3.694, "c": "Spanien"},
    {"n": "Der Schrei (Oslo)", "lat": 59.928, "lng": 10.727, "c": "Norwegen"},
    {"n": "Sternennacht (MoMA, New York)", "lat": 40.761, "lng": -73.978, "c": "USA"},
    {"n": "Mädchen mit Perlenohrring (Haag)", "lat": 52.08, "lng": 4.295, "c": "Niederlande"},
    {"n": "Sistinische Kapelle (Vatikan)", "lat": 41.903, "lng": 12.454, "c": "Vatikan"},
    {"n": "Nachtwache (Rijksmuseum Amsterdam)", "lat": 52.36, "lng": 4.885, "c": "Niederlande"},
    {"n": "Venus von Milo (Louvre, Paris)", "lat": 48.861, "lng": 2.336, "c": "Frankreich"},
    {"n": "Der Denker (Musée Rodin, Paris)", "lat": 48.856, "lng": 2.316, "c": "Frankreich"},
    {"n": "David (Galleria dell'Accademia, Florenz)", "lat": 43.777, "lng": 11.259, "c": "Italien"},
    {"n": "Die Persistenz der Erinnerung (MoMA)", "lat": 40.761, "lng": -73.978, "c": "USA"},
])
# filmsets: lat/lng/c
ku_mix('filmsets', [
    {"n": "Wadi Rum (Lawrence von Arabien / Dune)", "lat": 29.57, "lng": 35.42, "c": "Jordanien"},
    {"n": "Matamata (Herr der Ringe / Hobbiton)", "lat": -37.87, "lng": 175.68, "c": "Neuseeland"},
    {"n": "Ouarzazate (Gladiator / Babel)", "lat": 30.92, "lng": -6.89, "c": "Marokko"},
    {"n": "Skellig Michael (Star Wars)", "lat": 51.78, "lng": -10.54, "c": "Irland"},
    {"n": "Gozo (Gladiator Inseln)", "lat": 36.05, "lng": 14.27, "c": "Malta"},
    {"n": "Kualoa Ranch (Jurassic Park, Hawaii)", "lat": 21.52, "lng": -157.84, "c": "USA"},
    {"n": "Postojna (James Bond / Spectre)", "lat": 45.78, "lng": 14.2, "c": "Slowenien"},
    {"n": "Île Sainte-Marguerite (The Count of Monte Cristo)", "lat": 43.52, "lng": 7.05, "c": "Frankreich"},
    {"n": "Isle of Skye (Highlander / Stardust)", "lat": 57.27, "lng": -6.2, "c": "Schottland"},
    {"n": "Cappadocia (Star Wars / Bond)", "lat": 38.65, "lng": 34.85, "c": "Türkei"},
])
# ruinen: lat/lng/c
ku_mix('ruinen', [
    {"n": "Teotihuacán", "lat": 19.69, "lng": -98.84, "c": "Mexiko"},
    {"n": "Tikal (Maya-Tempel)", "lat": 17.22, "lng": -89.62, "c": "Guatemala"},
    {"n": "Chichen Itza", "lat": 20.68, "lng": -88.57, "c": "Mexiko"},
    {"n": "Ephesos (antike Stadt)", "lat": 37.94, "lng": 27.34, "c": "Türkei"},
    {"n": "Pompeji", "lat": 40.75, "lng": 14.49, "c": "Italien"},
    {"n": "Babylon (antike Stadt)", "lat": 32.54, "lng": 44.42, "c": "Irak"},
    {"n": "Leptis Magna", "lat": 32.64, "lng": 14.29, "c": "Libyen"},
    {"n": "Palenque (Maya-Stadt)", "lat": 17.49, "lng": -92.05, "c": "Mexiko"},
])
# bruecken: lat/lng/c
ku_mix('bruecken', [
    {"n": "Sydney Harbour Bridge", "lat": -33.853, "lng": 151.211, "c": "Australien"},
    {"n": "Millau Viaduct (Frankreich)", "lat": 44.1, "lng": 3.02, "c": "Frankreich"},
    {"n": "Akashi-Kaikyo Bridge (Japan)", "lat": 34.62, "lng": 135.0, "c": "Japan"},
    {"n": "Øresund Bridge (Schweden-Dänemark)", "lat": 55.57, "lng": 12.87, "c": "Schweden/Dänemark"},
    {"n": "Charles Bridge (Prag)", "lat": 50.086, "lng": 14.411, "c": "Tschechien"},
    {"n": "Rialto Bridge (Venedig)", "lat": 45.438, "lng": 12.336, "c": "Italien"},
    {"n": "Pont du Gard (Römerbrücke)", "lat": 43.947, "lng": 4.535, "c": "Frankreich"},
])
# gotteshaeuser: lat/lng/c
ku_mix('gotteshaeuser', [
    {"n": "Sagrada Família", "lat": 41.404, "lng": 2.174, "c": "Spanien"},
    {"n": "Dome of the Rock (Jerusalem)", "lat": 31.778, "lng": 35.236, "c": "Israel"},
    {"n": "Angkor Wat (Kambodscha)", "lat": 13.413, "lng": 103.867, "c": "Kambodscha"},
    {"n": "Shwedagon Pagoda (Myanmar)", "lat": 16.798, "lng": 96.149, "c": "Myanmar"},
    {"n": "Notre-Dame de Paris", "lat": 48.853, "lng": 2.349, "c": "Frankreich"},
    {"n": "Cologne Cathedral (Köln)", "lat": 50.941, "lng": 6.958, "c": "Deutschland"},
    {"n": "Borobudur (Indonesien)", "lat": -7.607, "lng": 110.204, "c": "Indonesien"},
    {"n": "Golden Temple (Amritsar)", "lat": 31.62, "lng": 74.876, "c": "Indien"},
    {"n": "Taj Mahal (Mausoleum)", "lat": 27.175, "lng": 78.042, "c": "Indien"},
])
# wolkenkratzer: n/c/val
ku_wolkenkratzer([
    {"n": "Shanghai Tower", "c": "China", "val": 632},
    {"n": "Abraj Al-Bait (Mekka)", "c": "Saudi-Arabien", "val": 601},
    {"n": "Ping An Finance Center", "c": "China", "val": 599},
    {"n": "Lotte World Tower (Seoul)", "c": "Südkorea", "val": 555},
    {"n": "One World Trade Center", "c": "USA", "val": 541},
    {"n": "Guangzhou CTF Finance Centre", "c": "China", "val": 530},
    {"n": "Tianjin CTF Finance Centre", "c": "China", "val": 530},
    {"n": "CITIC Tower (Beijing)", "c": "China", "val": 528},
    {"n": "Tianjin Chow Tai Fook Binhai Centre", "c": "China", "val": 530},
    {"n": "Taipei 101", "c": "Taiwan", "val": 508},
])
ku_pin('berggipfel', [
    {"n": "Kangchenjunga", "lat": 27.7, "lng": 88.15},
])
ku_pin('meerengen', [
    {"n": "Strait of Malacca", "lat": 3.0, "lng": 101.0},
    {"n": "Dardanellen", "lat": 40.15, "lng": 26.4},
    {"n": "Strait of Hormuz", "lat": 26.6, "lng": 56.5},
    {"n": "Kanal von Mosambik", "lat": -20.0, "lng": 41.5},
    {"n": "Sund (Öresund)", "lat": 55.9, "lng": 12.7},
    {"n": "Strait of Sicily", "lat": 37.1, "lng": 12.0},
])
ku_pin('wasserfaelle', [
    {"n": "Kaieteur Falls (Guyana)", "lat": 5.17, "lng": -59.48},
    {"n": "Sutherland Falls (Neuseeland)", "lat": -44.81, "lng": 167.74},
])
ku_pin('canyons', [
    {"n": "Bryce Canyon (Utah, USA)", "lat": 37.64, "lng": -112.17},
    {"n": "Slot Canyon (Arizona, USA)", "lat": 36.86, "lng": -111.41},
    {"n": "Verdon-Schlucht (Frankreich)", "lat": 43.73, "lng": 6.32},
    {"n": "Yarlung Tsangpo (Tibet)", "lat": 29.5, "lng": 94.8},
    {"n": "Fish River Canyon (Namibia)", "lat": -27.57, "lng": 17.57},
    {"n": "Tiger Leaping Gorge (Yunnan)", "lat": 27.2, "lng": 100.15},
    {"n": "Blyde River Canyon (Südafrika)", "lat": -24.6, "lng": 30.8},
    {"n": "Waimea Canyon (Kauai, Hawaii)", "lat": 22.07, "lng": -159.66},
    {"n": "Hell's Canyon (Idaho, USA)", "lat": 45.2, "lng": -116.7},
    {"n": "Prokosko Lake Canyon (Bosnien)", "lat": 44.08, "lng": 17.96},
    {"n": "Tara River Canyon (Montenegro)", "lat": 43.14, "lng": 19.14},
])
ku_pin('surf_spots', [
    {"n": "Hossegor (Frankreich)", "lat": 43.67, "lng": -1.41},
    {"n": "Uluwatu (Bali, Indonesien)", "lat": -8.83, "lng": 115.09},
    {"n": "Jeffreys Bay (Südafrika)", "lat": -34.05, "lng": 24.92},
    {"n": "Snapper Rocks (Gold Coast, Australien)", "lat": -28.17, "lng": 153.55},
    {"n": "Mavericks (Kalifornien, USA)", "lat": 37.49, "lng": -122.5},
    {"n": "Skeleton Bay (Namibia)", "lat": -19.5, "lng": 12.6},
    {"n": "Puerto Escondido (Mexiko)", "lat": 15.86, "lng": -97.07},
    {"n": "Cloudbreak (Fidschi)", "lat": -17.87, "lng": 177.21},
])
ku_pin('tiere_bigfive', [
    {"n": "Chobe NP (Botswana)", "lat": -18.0, "lng": 24.5},
    {"n": "Amboseli NP (Kenia)", "lat": -2.65, "lng": 37.26},
    {"n": "Masai Mara (Kenia)", "lat": -1.48, "lng": 35.1},
    {"n": "Hwange NP (Simbabwe)", "lat": -19.0, "lng": 26.5},
    {"n": "Ruaha NP (Tansania)", "lat": -7.5, "lng": 34.8},
])
ku_pin('tiere_grosskatzen', [
    {"n": "Amur-Leopard (Primorsky, Russland)", "lat": 43.2, "lng": 133.0},
    {"n": "Schneeleopard (Tian Shan, Kasachstan)", "lat": 42.5, "lng": 74.5},
    {"n": "Puma (Patagonia, Argentinien)", "lat": -50.5, "lng": -73.0},
    {"n": "Ozelot (Amazon, Brasilien)", "lat": -3.5, "lng": -62.0},
    {"n": "Gepard (Masai Mara, Kenia)", "lat": -1.48, "lng": 35.1},
    {"n": "Nordafrikanischer Gepard (Sahara)", "lat": 22.0, "lng": 8.0},
    {"n": "Borneo-Nebelparder (Sabah)", "lat": 5.0, "lng": 116.5},
    {"n": "Löwin (Serengeti, Tansania)", "lat": -2.33, "lng": 34.83},
    {"n": "Jaguar (Pantanal, Brasilien)", "lat": -17.0, "lng": -57.0},
    {"n": "Indischer Leopard (Ranthambhore NP)", "lat": 26.0, "lng": 76.5},
])
ku_pin('tiere_invasiv', [
    {"n": "Nilgans (heimisch Nil) → Europa", "lat": 47.5, "lng": 8.5},
    {"n": "Japanischer Staudenknöterich → UK", "lat": 51.5, "lng": -1.5},
    {"n": "Asiatische Tigermücke → Südeuropa", "lat": 43.7, "lng": 7.4},
    {"n": "Grauer Eichhörnchen → UK (aus USA)", "lat": 53.0, "lng": -2.0},
    {"n": "Neuseeländischer Falschskorpion → NZ", "lat": -40.0, "lng": 175.0},
    {"n": "Riesenschildkröte → Galapagos (neg.)", "lat": -0.7, "lng": -90.3},
    {"n": "Nilkrokodil → Florida (entflohen)", "lat": 25.5, "lng": -80.5},
])
ku_pin('tiere_vogelzug', [
    {"n": "Gibraltar (Europäischer Engpass)", "lat": 36.13, "lng": -5.35},
    {"n": "Eilat (Israel, Wachteln + Greifvögel)", "lat": 29.56, "lng": 34.95},
    {"n": "Point Pelee NP (Kanada, Warbler)", "lat": 41.97, "lng": -82.52},
    {"n": "Hawk Mountain (Pennsylvania, USA)", "lat": 40.64, "lng": -75.99},
    {"n": "Cape May NJ (USA)", "lat": 38.94, "lng": -74.92},
    {"n": "Ría de Villaviciosa (Spanien, Shorebirds)", "lat": 43.51, "lng": -5.44},
])
ku_pin('tiere_nationaltier_pin', [
    {"n": "Elch → Schweden", "lat": 60.0, "lng": 15.0},
    {"n": "Braunbär → Finnland", "lat": 62.0, "lng": 26.0},
    {"n": "Leopard → Sri Lanka", "lat": 7.87, "lng": 80.77},
    {"n": "Guanaco → Chile", "lat": -33.46, "lng": -70.65},
    {"n": "Nandu (Großer Rhea) → Argentinien", "lat": -34.6, "lng": -58.38},
])
ku_pin('tiere_hai', [
    {"n": "Gansbaai (Weißer Hai, Südafrika)", "lat": -34.58, "lng": 19.35},
    {"n": "Cocos Island (Costa Rica, Hammerhai)", "lat": 5.54, "lng": -87.06},
])
ku_nc('insel_match', [
    {"n": "Falklandinseln (Malvinas)", "c": "Vereinigtes Königreich"},
    {"n": "Madeira", "c": "Portugal"},
    {"n": "Korsika", "c": "Frankreich"},
    {"n": "Réunion", "c": "Frankreich"},
    {"n": "Curaçao", "c": "Niederlande"},
    {"n": "Guam", "c": "USA"},
    {"n": "Grönland (politisch)", "c": "Dänemark"},
])
ku_nc('philosophen', [
    {"n": "Aristoteles", "c": "Griechenland"},
    {"n": "Sokrates", "c": "Griechenland"},
    {"n": "Platon", "c": "Griechenland"},
    {"n": "Friedrich Nietzsche", "c": "Deutschland"},
    {"n": "Baruch Spinoza", "c": "Niederlande"},
    {"n": "David Hume", "c": "Schottland"},
    {"n": "John Locke", "c": "England"},
    {"n": "Voltaire", "c": "Frankreich"},
    {"n": "Jean-Jacques Rousseau", "c": "Frankreich"},
    {"n": "Karl Marx", "c": "Deutschland"},
])
ku_nc('nationalpflanzen', [
    {"n": "Maple Leaf (Zucker-Ahorn)", "c": "Kanada"},
    {"n": "Distel", "c": "Schottland"},
    {"n": "Dreifaltigkeitsblume (Shamrock)", "c": "Irland"},
    {"n": "Wattle (Akazie)", "c": "Australien"},
    {"n": "Proteacee (Protea cynaroides)", "c": "Südafrika"},
    {"n": "Farn (Silberfarn)", "c": "Neuseeland"},
    {"n": "Lilie (Fleur-de-lis)", "c": "Frankreich"},
    {"n": "Schwertlilie (Iris)", "c": "Frankreich"},
    {"n": "Birke (Betula)", "c": "Russland"},
    {"n": "Sonnenblume (Helianthus)", "c": "Ukraine"},
])
ku_nc('nationaltiere', [
    {"n": "Roter Ara", "c": "Honduras"},
    {"n": "Leopard", "c": "Somalia"},
])
ku_nc('nationalsport_off', [
    {"n": "Capoeira (inoffiziell)", "c": "Brasilien"},
    {"n": "Taekwondo", "c": "Südkorea"},
    {"n": "Volleyball (Strand)", "c": "Brasilien"},
    {"n": "Ice Hockey", "c": "Kanada"},
    {"n": "Shinty", "c": "Schottland"},
    {"n": "Gaelic Football", "c": "Irland"},
    {"n": "Kurash (Ringen)", "c": "Usbekistan"},
    {"n": "Muay Thai", "c": "Thailand"},
    {"n": "Judo (traditionell)", "c": "Japan"},
    {"n": "Polo", "c": "Pakistan"},
])
ku_nc('enklave', [
    {"n": "Büsingen am Hochrhein", "c": "Deutschland"},
    {"n": "Melilla", "c": "Spanien"},
    {"n": "Campione d'Italia", "c": "Italien"},
    {"n": "Llívia", "c": "Spanien"},
    {"n": "Lesotho (vollständige Enklave)", "c": "Südafrika"},
    {"n": "San Marino", "c": "Italien"},
    {"n": "Vatikanstadt", "c": "Italien"},
    {"n": "Cooch Behar (historisch)", "c": "Indien"},
    {"n": "Dahagram-Angarpota", "c": "Bangladesch"},
    {"n": "Baarle-Hertog", "c": "Belgien"},
])
ku_nc('grenzfluesse', [
    {"n": "Oder (Quelle in)", "c": "Tschechien"},
    {"n": "Donau (Quelle in)", "c": "Deutschland"},
    {"n": "Pruth (Quelle in)", "c": "Ukraine"},
    {"n": "Mekong (Quelle in)", "c": "China"},
    {"n": "Limpopo (Quelle in)", "c": "Südafrika"},
    {"n": "Orange River (Quelle in)", "c": "Lesotho"},
    {"n": "Amur (Quelle in)", "c": "Russland"},
    {"n": "Sambesi (Quelle in)", "c": "Sambia"},
])
ku_nc('halbinseln', [
    {"n": "Yucatán", "c": "Mexiko"},
    {"n": "Baja California", "c": "Mexiko"},
    {"n": "Sinai", "c": "Ägypten"},
    {"n": "Kola-Halbinsel", "c": "Russland"},
    {"n": "Kamtschatka", "c": "Russland"},
])
ku_nc('deltamuendungen', [
    {"n": "Ganges-Brahmaputra-Delta", "c": "Bangladesch"},
    {"n": "Niger-Delta", "c": "Nigeria"},
    {"n": "Orinoco-Delta", "c": "Venezuela"},
    {"n": "Mississippi-Delta", "c": "USA"},
    {"n": "Irrawaddy-Delta", "c": "Myanmar"},
    {"n": "Indus-Delta", "c": "Pakistan"},
    {"n": "Lena-Delta", "c": "Russland"},
    {"n": "Danube-Delta", "c": "Rumänien"},
])
ku_nc('kaps', [
    {"n": "Kap Nordkinn (nördlichstes Festland-Kap)", "c": "Norwegen"},
    {"n": "Kap Wrangell (Alaska)", "c": "USA"},
    {"n": "Kap Agulhas (südlichstes Afrika)", "c": "Südafrika"},
    {"n": "Kap Palmas (Westafrika)", "c": "Liberia"},
    {"n": "Kap Comorin (Südspitze Indiens)", "c": "Indien"},
    {"n": "Kap Leeuwin (SW-Australien)", "c": "Australien"},
    {"n": "Kap York (NE-Australien)", "c": "Australien"},
])
ku_nc('meerbusen', [
    {"n": "Golf von Bengalen", "c": "Indien"},
    {"n": "Golf von Oman", "c": "Oman"},
    {"n": "Persischer Golf", "c": "Iran"},
    {"n": "Golf von Aden", "c": "Jemen"},
    {"n": "Golf von Thailand", "c": "Thailand"},
    {"n": "Bothnischer Meerbusen", "c": "Schweden"},
    {"n": "Golf von Alaska", "c": "USA"},
])
ku_nc('inselgruppen', [
    {"n": "Galápagos-Inseln", "c": "Ecuador"},
    {"n": "Banda-Inseln", "c": "Indonesien"},
    {"n": "Britische Jungferninseln", "c": "Vereinigtes Königreich"},
    {"n": "Faröer-Inseln", "c": "Dänemark"},
    {"n": "Cook-Inseln", "c": "Neuseeland"},
    {"n": "Bermuda", "c": "Vereinigtes Königreich"},
])
ku_nc('gebirge_match', [
    {"n": "Karpaten", "c": "Slowakei"},
    {"n": "Pyrenäen", "c": "Frankreich"},
    {"n": "Apennin", "c": "Italien"},
    {"n": "Skandinavische Gebirge", "c": "Norwegen"},
    {"n": "Atlas-Gebirge", "c": "Marokko"},
    {"n": "Kaukasus", "c": "Georgien"},
    {"n": "Hindu Kush", "c": "Afghanistan"},
])
ku_nc('seen_match', [
    {"n": "Titicacasee", "c": "Bolivien"},
    {"n": "Malawisee (Nyasa)", "c": "Malawi"},
    {"n": "Tanganjikasee", "c": "Tansania"},
    {"n": "Baikalsee", "c": "Russland"},
    {"n": "Ladogasee", "c": "Russland"},
    {"n": "Onega-See", "c": "Russland"},
    {"n": "Vänern", "c": "Schweden"},
])
ku_nc('automarken', [
    {"n": "Skoda", "c": "Tschechien"},
    {"n": "Volvo", "c": "Schweden"},
    {"n": "Renault", "c": "Frankreich"},
    {"n": "Fiat", "c": "Italien"},
    {"n": "SEAT", "c": "Spanien"},
    {"n": "Kia", "c": "Südkorea"},
    {"n": "Tata Motors", "c": "Indien"},
])
ku_nc('fluggesellschaften', [
    {"n": "Qantas", "c": "Australien"},
    {"n": "Air New Zealand", "c": "Neuseeland"},
])
ku_nc('bahnstrecken', [
    {"n": "Glacier Express (Zermatt–St. Moritz)", "c": "Schweiz"},
    {"n": "El Chepe (Copper Canyon)", "c": "Mexiko"},
    {"n": "Flåm-Bahn (Flåmsbana)", "c": "Norwegen"},
    {"n": "TGV Méditerranée (Paris–Marseille)", "c": "Frankreich"},
    {"n": "Bernina Express", "c": "Schweiz"},
    {"n": "Blue Train (Pretoria–Kapstadt)", "c": "Südafrika"},
    {"n": "Ghan (Adelaide–Darwin)", "c": "Australien"},
])
ku_nc('hafen_world', [
    {"n": "Hafen Singapur", "c": "Singapur"},
    {"n": "Hafen Ningbo-Zhoushan", "c": "China"},
    {"n": "Hafen Guangzhou", "c": "China"},
    {"n": "Hafen Qingdao", "c": "China"},
    {"n": "Hafen Busan", "c": "Südkorea"},
    {"n": "Hafen Tianjin", "c": "China"},
    {"n": "Hafen Antwerpen", "c": "Belgien"},
    {"n": "Hafen Hamburg", "c": "Deutschland"},
])
ku_nc('kanaele', [
    {"n": "Nord-Ostsee-Kanal (Kiel)", "c": "Deutschland"},
    {"n": "Mittellandkanal", "c": "Deutschland"},
    {"n": "Erie Canal (New York)", "c": "USA"},
    {"n": "Canal du Midi", "c": "Frankreich"},
    {"n": "Kanal von Korinth", "c": "Griechenland"},
])
ku_nc('reedereien', [
    {"n": "CMA CGM", "c": "Frankreich"},
    {"n": "COSCO Shipping", "c": "China"},
    {"n": "Hapag-Lloyd", "c": "Deutschland"},
    {"n": "ONE (Ocean Network Express)", "c": "Japan"},
    {"n": "Evergreen Marine", "c": "Taiwan"},
    {"n": "Yang Ming Marine", "c": "Taiwan"},
    {"n": "HMM (Hyundai Merchant Marine)", "c": "Südkorea"},
    {"n": "PIL (Pacific International Lines)", "c": "Singapur"},
    {"n": "Wan Hai Lines", "c": "Taiwan"},
])
ku_nc('autobahnen_beruhmt', [
    {"n": "Route 66 (historisch)", "c": "USA"},
    {"n": "Pan-American Highway", "c": "USA/Mittelamerika"},
    {"n": "Great Ocean Road", "c": "Australien"},
    {"n": "Transsiberian Highway (M58)", "c": "Russland"},
    {"n": "N1 (Kapstadt–Pretoria)", "c": "Südafrika"},
    {"n": "Ring Road (Route 1)", "c": "Island"},
    {"n": "Pacific Coast Highway (CA-1)", "c": "USA"},
    {"n": "Romantische Straße", "c": "Deutschland"},
    {"n": "Karakoram Highway", "c": "Pakistan/China"},
    {"n": "Ruta 40", "c": "Argentinien"},
])
ku_nc('metrostaedte', [
    {"n": "Metro Peking (BJS)", "c": "China"},
    {"n": "U-Bahn Wien", "c": "Österreich"},
    {"n": "Metro Kairo", "c": "Ägypten"},
    {"n": "MRT Singapur", "c": "Singapur"},
    {"n": "Metro Mexico City", "c": "Mexiko"},
    {"n": "CTA Chicago", "c": "USA"},
])
ku_nc('luft_rekorde', [
    {"n": "Größter Passagierjet (A380)", "c": "Frankreich/EU"},
    {"n": "Schnellster Linienflug (SR-71 Blackbird inoffiziell)", "c": "USA"},
    {"n": "Höchster Flughafen (Daocheng Yading)", "c": "China"},
    {"n": "Steilster Anflug weltweit (Paro, Bhutan)", "c": "Bhutan"},
    {"n": "Windigster Flughafen (Wellington)", "c": "Neuseeland"},
    {"n": "Kürzeste Ladenbrücke-Route (BA)", "c": "Vereinigtes Königreich"},
    {"n": "Älteste Airline (KLM)", "c": "Niederlande"},
    {"n": "Längste Nonstop-Route (SIA SQ24 SIN–JFK)", "c": "Singapur"},
    {"n": "Höchste Boardingbrücke (Dubai T3)", "c": "Vereinigte Arabische Emirate"},
])
ku_nc('distanz_schaetzer', [
    {"n": "Sydney → Auckland", "c": "2160 km"},
])
ku_nc('flugzeit_schaetzer', [
    {"n": "Frankfurt → Singapur", "c": "12 Std."},
    {"n": "Paris → Tokio", "c": "12 Std."},
    {"n": "Los Angeles → Sydney", "c": "15 Std."},
    {"n": "New York → London", "c": "7 Std."},
    {"n": "Dubai → New York", "c": "14 Std."},
])

# dict-valued keys in kultur.json
def ku_items_p(k, items):
    existing = {x['n'] for x in d[k]['items']}
    added = [x for x in items if x['n'] not in existing]
    needed = max(0, 50 - len(d[k]['items']))
    d[k]['items'].extend(added[:max(needed, len(added))])
    print(f'  {k}: {len(d[k]["items"])} items')

ku_items_p('tiere_nutztier_rassen', [
    {"n": "Murray Grey-Rind", "lat": -36.5, "lng": 146.0},
    {"n": "Charolais-Rind", "lat": 46.7, "lng": 4.2},
    {"n": "Limousin-Rind", "lat": 45.83, "lng": 1.26},
    {"n": "Duroc-Schwein", "lat": 41.12, "lng": -74.14},
    {"n": "Berkshire-Schwein", "lat": 51.46, "lng": -1.04},
    {"n": "Pietrain-Schwein", "lat": 50.58, "lng": 4.88},
    {"n": "Dorset-Schaf", "lat": 50.75, "lng": -2.43},
    {"n": "Merino-Schaf", "lat": 40.4, "lng": -3.7},
    {"n": "Suffolk-Schaf", "lat": 52.07, "lng": 1.0},
    {"n": "Saanen-Ziege", "lat": 46.49, "lng": 7.19},
])
ku_items_p('tiere_fossilien', [
    {"n": "Hell Creek Formation (Montana, USA)", "lat": 47.39, "lng": -106.52},
    {"n": "Patagonia Fossil Beds (Trelew, Argentinien)", "lat": -43.25, "lng": -65.31},
    {"n": "Cretaceous Park (Kem Kem, Marokko)", "lat": 30.5, "lng": -4.5},
    {"n": "Yixian Formation (Liaoning, China)", "lat": 41.83, "lng": 120.73},
    {"n": "Karoo Basin (Südafrika)", "lat": -32.29, "lng": 24.53},
    {"n": "Tendaguru (Tansania)", "lat": -10.0, "lng": 39.22},
    {"n": "Cerro Ballena (Chile)", "lat": -26.1, "lng": -70.5},
    {"n": "Olduvai Gorge (Tansania)", "lat": -2.99, "lng": 35.35},
    {"n": "Red Beds (San Juan Basin, New Mexico)", "lat": 36.5, "lng": -107.5},
    {"n": "Morrison Formation (Colorado)", "lat": 38.45, "lng": -107.88},
])
ku_items_p('pferde_rassen', [
    {"n": "Lusitano", "lat": 39.0, "lng": -8.5},
    {"n": "Trakehner", "lat": 54.2, "lng": 21.4},
    {"n": "Haflinger", "lat": 46.65, "lng": 11.1},
    {"n": "Appaloosa", "lat": 46.4, "lng": -116.98},
    {"n": "Quarter Horse", "lat": 32.78, "lng": -97.34},
    {"n": "Connemara-Pony", "lat": 53.53, "lng": -9.7},
    {"n": "Mustang (Wildpferd)", "lat": 40.0, "lng": -116.0},
    {"n": "Paso Fino", "lat": 18.47, "lng": -66.1},
    {"n": "Missouri Fox Trotter", "lat": 37.96, "lng": -91.83},
    {"n": "Hanoverian (Hannoveraner)", "lat": 52.37, "lng": 9.73},
])
save('kultur.json', d)
print("Part 10 (kultur.json) complete.")
