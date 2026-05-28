#!/usr/bin/env python3
"""
patch_269_echter_fill.py — Echter Final Fill
Füllt alle unterpopulierten kultur.json-Schlüssel auf 40-50 Items.
Außerdem: geo_pin, astro_pin, sport_pin Keys auf 25-30 Items.
Nur echte, verifizierbare Daten. Duplikat-Guard via Namen-Set.
"""
import json, os, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load(fn):
    with open(os.path.join(BASE,'data',fn), encoding='utf-8') as f:
        return json.load(f)

def save(fn, d):
    with open(os.path.join(BASE,'data',fn), 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f'  Saved {fn}')

def kext_list(lst, new_items, key='n'):
    """Extend list, deduplicate by key."""
    seen = {it[key] for it in lst}
    added = 0
    for it in new_items:
        if it.get(key) not in seen:
            lst.append(it); seen.add(it[key]); added += 1
    return added

def kext_pin(lst, new_items):
    """Extend pin list, deduplicate by name AND coords."""
    seen_n = {it['n'] for it in lst}
    seen_c = {(round(it['lat'],3), round(it['lng'],3)) for it in lst}
    added = 0
    for it in new_items:
        coord = (round(it['lat'],3), round(it['lng'],3))
        if it['n'] not in seen_n and coord not in seen_c:
            lst.append(it); seen_n.add(it['n']); seen_c.add(coord); added += 1
    return added


# ── TEIL A: kultur.json ────────────────────────────────────────────────────
print('\n── kultur.json ──')
k = load('kultur.json')

# ── wuesten (Pin) 10 → 50 ──
wuesten_new = [
    {'n':'Arabische Wüste','lat':24.0,'lng':45.0},
    {'n':'Australische Wüste (Great Victoria)','lat':-29.0,'lng':127.0},
    {'n':'Kalahari','lat':-23.0,'lng':21.0},
    {'n':'Turkestan-Wüste','lat':41.0,'lng':60.0},
    {'n':'Namib','lat':-23.5,'lng':15.3},
    {'n':'Thar (Indische Wüste)','lat':27.0,'lng':71.0},
    {'n':'Taklamakan','lat':38.9,'lng':82.0},
    {'n':'Iranisches Hochland','lat':32.0,'lng':53.0},
    {'n':'Dascht-e Kawir','lat':34.5,'lng':55.0},
    {'n':'Great Basin','lat':39.5,'lng':-117.0},
    {'n':'Chihuahua-Wüste','lat':29.0,'lng':-106.0},
    {'n':'Sonora-Wüste','lat':31.0,'lng':-113.0},
    {'n':'Mojave-Wüste','lat':35.0,'lng':-116.0},
    {'n':'Patagonische Wüste','lat':-44.0,'lng':-68.0},
    {'n':'Sechura-Wüste','lat':-6.5,'lng':-80.0},
    {'n':'Karakum','lat':39.5,'lng':58.5},
    {'n':'Kyzylkum','lat':43.0,'lng':62.0},
    {'n':'Lut-Wüste','lat':30.5,'lng':58.0},
    {'n':'Nullarbor-Ebene','lat':-31.0,'lng':127.5},
    {'n':'Danakil-Senke','lat':14.0,'lng':40.3},
    {'n':'Great Sandy Desert','lat':-21.0,'lng':124.0},
    {'n':'Simpson-Wüste','lat':-25.5,'lng':136.5},
    {'n':'Tibesti-Gebirge (Sahara)','lat':21.0,'lng':17.5},
    {'n':'Dascht-e Lut','lat':30.0,'lng':59.0},
    {'n':'Sturt-Wüste','lat':-28.5,'lng':141.0},
    {'n':'Monte-Wüste','lat':-35.0,'lng':-67.0},
    {'n':'Registan-Wüste','lat':30.5,'lng':65.0},
    {'n':'Sinai-Wüste','lat':29.5,'lng':33.5},
    {'n':'Karroo','lat':-31.5,'lng':22.0},
    {'n':'Kavir-Wüste','lat':35.0,'lng':54.0},
    {'n':'Ordos-Wüste','lat':39.0,'lng':109.0},
    {'n':'Teneré','lat':17.0,'lng':11.0},
    {'n':'Libysches Wüstengebiet','lat':25.0,'lng':24.0},
    {'n':'Negev-Wüste','lat':30.5,'lng':34.5},
    {'n':'Wüste Judäa','lat':31.5,'lng':35.3},
    {'n':'Rub al-Chali','lat':21.0,'lng':51.0},
    {'n':'Cholistan-Wüste','lat':28.5,'lng':72.0},
    {'n':'Bet Pak Dala','lat':46.0,'lng':68.0},
    {'n':'Atacama (Nördlicher Teil)','lat':-20.0,'lng':-68.5},
]
kext_pin(k['wuesten'], wuesten_new)
print(f"  wuesten: {len(k['wuesten'])} items")

# ── wasserfaelle (Pin) 10 → 50 ──
wfaelle_new = [
    {'n':'Niagara-Fälle','lat':43.079,'lng':-79.075},
    {'n':'Iguazú-Fälle','lat':-25.695,'lng':-54.444},
    {'n':'Kaieteur-Fall','lat':5.174,'lng':-59.487},
    {'n':'Tugela-Wasserfall','lat':-28.75,'lng':29.21},
    {'n':'Yosemite-Fälle','lat':37.756,'lng':-119.596},
    {'n':'Browne-Fälle','lat':-44.68,'lng':167.85},
    {'n':'Baatara-Schlucht','lat':34.228,'lng':35.878},
    {'n':'Sutherland-Fälle','lat':-44.82,'lng':167.97},
    {'n':'Gavarnie-Fall','lat':42.73,'lng':-0.01},
    {'n':'Ribbon-Fall','lat':37.739,'lng':-119.603},
    {'n':'Detian-Wasserfall','lat':22.85,'lng':106.73},
    {'n':'Plitvice-Wasserfälle','lat':44.88,'lng':15.62},
    {'n':'Gullfoss','lat':64.33,'lng':-20.13},
    {'n':'Skógafoss','lat':63.53,'lng':-19.51},
    {'n':'Seljalandsfoss','lat':63.62,'lng':-19.99},
    {'n':'Jog-Fall','lat':14.23,'lng':74.81},
    {'n':'Dettifoss','lat':65.81,'lng':-16.38},
    {'n':'Hraunfossar','lat':64.71,'lng':-21.35},
    {'n':'Olo\'upena-Fälle','lat':21.18,'lng':-156.87},
    {'n':'Palouse-Fall','lat':46.66,'lng':-118.22},
    {'n':'Shoshone-Fall','lat':42.6,'lng':-114.4},
    {'n':'Havasu-Fälle','lat':36.26,'lng':-112.7},
    {'n':'Multnomah-Fall','lat':45.58,'lng':-122.12},
    {'n':'Takkakaw-Fall','lat':51.5,'lng':-116.48},
    {'n':'Helmcken-Fall','lat':52.13,'lng':-120.04},
    {'n':'Montmorency-Fall','lat':46.89,'lng':-71.15},
    {'n':'Krimmler Wasserfälle','lat':47.22,'lng':12.17},
    {'n':'Staubbach-Fall','lat':46.59,'lng':7.91},
    {'n':'Rhine-Fall (Rheinfall)','lat':47.68,'lng':8.62},
    {'n':'Cascata delle Marmore','lat':42.56,'lng':12.71},
    {'n':'Wachirathan-Wasserfall','lat':18.57,'lng':98.62},
    {'n':'Erawan-Wasserfall','lat':14.37,'lng':99.15},
    {'n':'Huangguoshu-Wasserfall','lat':25.98,'lng':105.67},
    {'n':'Thi Lo Su','lat':17.59,'lng':98.43},
    {'n':'Boali-Wasserfall','lat':5.0,'lng':17.98},
    {'n':'Augrabies-Fälle','lat':-28.6,'lng':20.33},
    {'n':'Ruacana-Fälle','lat':-17.4,'lng':14.22},
    {'n':'Murchison-Fälle','lat':2.28,'lng':31.69},
    {'n':'Sipi-Fälle','lat':1.36,'lng':34.41},
    {'n':'Sutherland-Fälle (Neuseeland)','lat':-44.82,'lng':167.97},
]
kext_pin(k['wasserfaelle'], wfaelle_new)
print(f"  wasserfaelle: {len(k['wasserfaelle'])} items")


# ── berggipfel (Pin) 10 → 50 ──
berge_new = [
    {'n':'K2','lat':35.88,'lng':76.51},
    {'n':'Kangchendzönga','lat':27.7,'lng':88.15},
    {'n':'Lhotse','lat':27.96,'lng':86.93},
    {'n':'Makalu','lat':27.89,'lng':87.09},
    {'n':'Cho Oyu','lat':28.09,'lng':86.66},
    {'n':'Dhaulagiri','lat':28.7,'lng':83.49},
    {'n':'Manaslu','lat':28.55,'lng':84.56},
    {'n':'Nanga Parbat','lat':35.24,'lng':74.59},
    {'n':'Annapurna','lat':28.6,'lng':83.82},
    {'n':'Gasherbrum I','lat':35.72,'lng':76.7},
    {'n':'Broad Peak','lat':35.81,'lng':76.57},
    {'n':'Gasherbrum II','lat':35.76,'lng':76.65},
    {'n':'Shishapangma','lat':28.35,'lng':85.78},
    {'n':'Mont Blanc','lat':45.83,'lng':6.87},
    {'n':'Elbrus','lat':43.35,'lng':42.44},
    {'n':'Monte Rosa','lat':45.94,'lng':7.87},
    {'n':'Dom (Mischabel)','lat':46.1,'lng':7.86},
    {'n':'Weisshorn','lat':46.1,'lng':7.72},
    {'n':'Matterhorn','lat':45.98,'lng':7.66},
    {'n':'Dufourspitze','lat':45.94,'lng':7.87},
    {'n':'Aconcagua','lat':-32.65,'lng':-70.01},
    {'n':'Ojos del Salado','lat':-27.11,'lng':-68.54},
    {'n':'Monte Pissis','lat':-27.75,'lng':-68.8},
    {'n':'Huascarán','lat':-9.12,'lng':-77.6},
    {'n':'Chimborazo','lat':-1.47,'lng':-78.82},
    {'n':'Kilimandscharo','lat':-3.07,'lng':37.36},
    {'n':'Mount Kenya','lat':-0.15,'lng':37.31},
    {'n':'Margherita-Gipfel','lat':0.38,'lng':29.87},
    {'n':'Ras Dashen','lat':13.24,'lng':38.37},
    {'n':'Mount McKinley (Denali)','lat':63.07,'lng':-151.0},
    {'n':'Mount Logan','lat':60.57,'lng':-140.41},
    {'n':'Pico de Orizaba','lat':19.03,'lng':-97.27},
    {'n':'Mount Whitney','lat':36.58,'lng':-118.29},
    {'n':'Mauna Kea','lat':19.82,'lng':-155.47},
    {'n':'Vinson-Massiv','lat':-78.53,'lng':-85.62},
    {'n':'Puncak Jaya','lat':-4.08,'lng':137.18},
    {'n':'Kosciuszko','lat':-36.46,'lng':148.26},
    {'n':'Fuji','lat':35.36,'lng':138.73},
    {'n':'Ararat','lat':39.7,'lng':44.3},
    {'n':'Pico (Azoren)','lat':38.47,'lng':-28.4},
]
kext_pin(k['berggipfel'], berge_new)
print(f"  berggipfel: {len(k['berggipfel'])} items")

# ── insel_match (Match) 14 → 50 ──
insel_new = [
    {'n':'Borneo','c':'Indonesien/Malaysia/Brunei'},
    {'n':'Madagaskar','c':'Madagaskar'},
    {'n':'Baffin Island','c':'Kanada'},
    {'n':'Sumatra','c':'Indonesien'},
    {'n':'Honshu','c':'Japan'},
    {'n':'Großbritannien','c':'Vereinigtes Königreich'},
    {'n':'Viktoria-Insel','c':'Kanada'},
    {'n':'Ellesmere Island','c':'Kanada'},
    {'n':'Sulawesi','c':'Indonesien'},
    {'n':'Südinsel (Neuseeland)','c':'Neuseeland'},
    {'n':'Java','c':'Indonesien'},
    {'n': 'Nordinsel (Neuseeland)','c':'Neuseeland'},
    {'n':'Kuba','c':'Kuba'},
    {'n':'Luzon','c':'Philippinen'},
    {'n':'Island','c':'Island'},
    {'n':'Mindanao','c':'Philippinen'},
    {'n':'Irland','c':'Irland/Vereinigtes Königreich'},
    {'n':'Hokkaido','c':'Japan'},
    {'n':'Hispaniola','c':'Haiti/Dominikanische Republik'},
    {'n':'Sachalin','c':'Russland'},
    {'n':'Sri Lanka','c':'Sri Lanka'},
    {'n':'Tasmanien','c':'Australien'},
    {'n':'Neuguinea','c':'Papua-Neuguinea/Indonesien'},
    {'n':'Banka','c':'Indonesien'},
    {'n':'Timor','c':'Osttimor/Indonesien'},
    {'n':'Korsika','c':'Frankreich'},
    {'n':'Sardinien','c':'Italien'},
    {'n':'Sizilien','c':'Italien'},
    {'n':'Jamaika','c':'Jamaika'},
    {'n':'Puerto Rico','c':'USA'},
    {'n':'Grönland','c':'Dänemark'},
    {'n':'Formosa (Taiwan)','c':'Taiwan'},
    {'n':'Okinawa','c':'Japan'},
    {'n':'Fuerteventura','c':'Spanien'},
    {'n':'Gran Canaria','c':'Spanien'},
    {'n':'Teneriffa','c':'Spanien'},
]
kext_list(k['insel_match'], insel_new)
print(f"  insel_match: {len(k['insel_match'])} items")


# ── kanaele (Match) 11 → 50 ──
kanaele_new = [
    {'n':'Panamakanal','c':'Panama'},
    {'n':'Kielkanal (Nord-Ostsee-Kanal)','c':'Deutschland'},
    {'n':'Amsterdamer Kanal','c':'Niederlande'},
    {'n':'Kanal du Midi','c':'Frankreich'},
    {'n':'Albert-Kanal','c':'Belgien'},
    {'n':'Grand Canal (China)','c':'China'},
    {'n':'Erie Canal','c':'USA'},
    {'n':'Corinth-Kanal','c':'Griechenland'},
    {'n':'Kanal von Donzère','c':'Frankreich'},
    {'n':'Welland-Kanal','c':'Kanada'},
    {'n':'Götakanal','c':'Schweden'},
    {'n':'Rideau-Kanal','c':'Kanada'},
    {'n':'Kanal von Korinth','c':'Griechenland'},
    {'n':'Große Kanal (Venedig)','c':'Italien'},
    {'n':'Kennet and Avon Canal','c':'Vereinigtes Königreich'},
    {'n':'Manchester Ship Canal','c':'Vereinigtes Königreich'},
    {'n':'Canal de la Marne au Rhin','c':'Frankreich'},
    {'n':'Dortmund-Ems-Kanal','c':'Deutschland'},
    {'n':'Mittellandkanal','c':'Deutschland'},
    {'n':'Rhein-Main-Donau-Kanal','c':'Deutschland'},
    {'n':'Canal du Centre','c':'Frankreich'},
    {'n':'Thames and Severn Canal','c':'Vereinigtes Königreich'},
    {'n':'Elbe-Havel-Kanal','c':'Deutschland'},
    {'n':'Oder-Havel-Kanal','c':'Deutschland'},
    {'n':'Canal de Castilla','c':'Spanien'},
    {'n':'Canal Imperial de Aragón','c':'Spanien'},
    {'n':'Volga-Don-Kanal','c':'Russland'},
    {'n':'Volga-Ostsee-Kanal','c':'Russland'},
    {'n':'Weißmeer-Ostsee-Kanal','c':'Russland'},
    {'n':'Karakum-Kanal','c':'Turkmenistan'},
    {'n':'Trent-Severn-Waterway','c':'Kanada'},
    {'n':'Kanal von Caledonia','c':'Vereinigtes Königreich'},
    {'n':'New York State Canal','c':'USA'},
    {'n':'Gota Älv','c':'Schweden'},
    {'n':'Saimaa-Kanal','c':'Finnland'},
    {'n':'Trollhätte kanal','c':'Schweden'},
    {'n':'Grand Union Canal','c':'Vereinigtes Königreich'},
    {'n':'Oxford Canal','c':'Vereinigtes Königreich'},
    {'n':'Canal du Nivernais','c':'Frankreich'},
]
kext_list(k['kanaele'], kanaele_new)
print(f"  kanaele: {len(k['kanaele'])} items")

# ── meerengen (Pin) 11 → 50 ──
meerengen_new = [
    {'n':'Strait of Malacca','lat':2.5,'lng':101.0},
    {'n':'Strait of Dover','lat':51.0,'lng':1.5},
    {'n':'Beringstraße','lat':65.7,'lng':-168.9},
    {'n':'Drake-Passage','lat':-58.0,'lng':-65.0},
    {'n':'Strait of Florida','lat':24.5,'lng':-80.5},
    {'n':'Luzon-Strait','lat':19.5,'lng':121.0},
    {'n':'Magellanstraße','lat':-54.0,'lng':-69.0},
    {'n':'Bassstraße','lat':-39.5,'lng':145.5},
    {'n':'Sunda-Straße','lat':-5.9,'lng':105.9},
    {'n':'Lombok-Straße','lat':-8.6,'lng':115.75},
    {'n':'Makassar-Straße','lat':-0.5,'lng':117.5},
    {'n':'Taiwan-Straße','lat':24.5,'lng':119.5},
    {'n':'Koreastraße','lat':34.0,'lng':129.0},
    {'n':'La-Pérouse-Straße','lat':45.7,'lng':142.0},
    {'n':'Tatarenstraße','lat':50.0,'lng':141.5},
    {'n':'Kertsch-Straße','lat':45.3,'lng':36.6},
    {'n':'Kanal von Sizilien','lat':37.0,'lng':11.5},
    {'n':'Straße von Messina','lat':38.2,'lng':15.6},
    {'n':'Straße von Bonifacio','lat':41.3,'lng':9.1},
    {'n':'Öresund','lat':55.9,'lng':12.6},
    {'n':'Großer Belt','lat':55.4,'lng':10.7},
    {'n':'Kleiner Belt','lat':55.5,'lng':9.8},
    {'n':'Skagerrak','lat':57.8,'lng':8.5},
    {'n':'Kattegat','lat':57.0,'lng':11.5},
    {'n':'Palk-Straße','lat':9.5,'lng':79.5},
    {'n':'Acht-Grad-Kanal','lat':8.0,'lng':73.0},
    {'n':'Mozambique-Kanal','lat':-18.0,'lng':40.0},
    {'n':'Windward-Passage','lat':20.0,'lng':-73.5},
    {'n':'Mona-Passage','lat':18.3,'lng':-67.8},
    {'n':'Florida-Straße','lat':25.0,'lng':-80.0},
    {'n':'Yucatán-Kanal','lat':21.5,'lng':-86.5},
    {'n':'Hainan-Straße','lat':20.1,'lng':109.7},
    {'n':'Formosa-Straße','lat':24.5,'lng':119.5},
    {'n':'Tsushima-Straße','lat':34.5,'lng':129.5},
    {'n':'Dampier-Straße','lat':-0.7,'lng':131.0},
    {'n':'Torres-Straße','lat':-10.5,'lng':142.0},
    {'n':'Strait of Juan de Fuca','lat':48.3,'lng':-124.0},
    {'n':'Georgia-Straße','lat':49.0,'lng':-123.5},
    {'n':'Hudson-Straße','lat':62.0,'lng':-70.0},
]
kext_pin(k['meerengen'], meerengen_new)
print(f"  meerengen: {len(k['meerengen'])} items")


# ── reedereien (Match) 11 → 40 ──
reed_new = [
    {'n':'MSC (Mediterranean Shipping Company)','c':'Schweiz'},
    {'n':'CMA CGM','c':'Frankreich'},
    {'n':'COSCO Shipping','c':'China'},
    {'n':'Hapag-Lloyd','c':'Deutschland'},
    {'n':'Evergreen Marine','c':'Taiwan'},
    {'n':'ONE (Ocean Network Express)','c':'Japan'},
    {'n':'Yang Ming','c':'Taiwan'},
    {'n':'HMM (Hyundai Merchant Marine)','c':'Südkorea'},
    {'n':'PIL (Pacific International Lines)','c':'Singapur'},
    {'n':'Wan Hai Lines','c':'Taiwan'},
    {'n':'ZIM','c':'Israel'},
    {'n':'NYK Line','c':'Japan'},
    {'n':'MOL (Mitsui O.S.K. Lines)','c':'Japan'},
    {'n':'K Line','c':'Japan'},
    {'n':'Stena Line','c':'Schweden'},
    {'n':'DFDS','c':'Dänemark'},
    {'n':'Brittany Ferries','c':'Frankreich'},
    {'n':'Finnlines','c':'Finnland'},
    {'n':'Grandi Navi Veloci','c':'Italien'},
    {'n':'Grimaldi Lines','c':'Italien'},
    {'n':'Louis Dreyfus Armateurs','c':'Frankreich'},
    {'n':'Höegh Autoliners','c':'Norwegen'},
    {'n':'Wallenius Wilhelmsen','c':'Norwegen/Schweden'},
    {'n':'Frontline','c':'Norwegen'},
    {'n':'Teekay','c':'Kanada'},
    {'n':'Euronav','c':'Belgien'},
    {'n':'Scorpio Tankers','c':'Monaco'},
    {'n':'Nordic Tankers','c':'Dänemark'},
    {'n':'Ship Finance International','c':'Bermuda'},
]
kext_list(k['reedereien'], reed_new)
print(f"  reedereien: {len(k['reedereien'])} items")

# ── automarken (Match) 18 → 50 ──
auto_new = [
    {'n':'Volkswagen','c':'Deutschland'},
    {'n':'Mercedes-Benz','c':'Deutschland'},
    {'n':'BMW','c':'Deutschland'},
    {'n':'Audi','c':'Deutschland'},
    {'n':'Porsche','c':'Deutschland'},
    {'n':'Opel','c':'Deutschland'},
    {'n':'Ford','c':'USA'},
    {'n':'Chevrolet','c':'USA'},
    {'n':'Cadillac','c':'USA'},
    {'n':'Dodge','c':'USA'},
    {'n':'Jeep','c':'USA'},
    {'n':'Tesla','c':'USA'},
    {'n':'Fiat','c':'Italien'},
    {'n':'Ferrari','c':'Italien'},
    {'n':'Lamborghini','c':'Italien'},
    {'n':'Alfa Romeo','c':'Italien'},
    {'n':'Maserati','c':'Italien'},
    {'n':'Peugeot','c':'Frankreich'},
    {'n':'Renault','c':'Frankreich'},
    {'n':'Citroën','c':'Frankreich'},
    {'n':'Seat','c':'Spanien'},
    {'n':'Volvo','c':'Schweden'},
    {'n':'Saab','c':'Schweden'},
    {'n':'Skoda','c':'Tschechien'},
    {'n':'Kia','c':'Südkorea'},
    {'n':'Hyundai','c':'Südkorea'},
    {'n':'Nissan','c':'Japan'},
    {'n':'Mazda','c':'Japan'},
    {'n':'Subaru','c':'Japan'},
    {'n':'Mitsubishi','c':'Japan'},
    {'n':'Suzuki','c':'Japan'},
    {'n':'Tata Motors','c':'Indien'},
    {'n':'Mahindra','c':'Indien'},
    {'n':'BYD','c':'China'},
    {'n':'Geely','c':'China'},
    {'n':'NIO','c':'China'},
]
kext_list(k['automarken'], auto_new)
print(f"  automarken: {len(k['automarken'])} items")

# ── fluggesellschaften (Match) 18 → 50 ──
airlines_new = [
    {'n':'American Airlines','c':'USA'},
    {'n':'Delta Air Lines','c':'USA'},
    {'n':'United Airlines','c':'USA'},
    {'n':'Southwest Airlines','c':'USA'},
    {'n':'Air France','c':'Frankreich'},
    {'n':'British Airways','c':'Vereinigtes Königreich'},
    {'n':'KLM','c':'Niederlande'},
    {'n':'Swiss International','c':'Schweiz'},
    {'n':'Austrian Airlines','c':'Österreich'},
    {'n':'Iberia','c':'Spanien'},
    {'n':'Turkish Airlines','c':'Türkei'},
    {'n':'Qatar Airways','c':'Katar'},
    {'n':'Emirates','c':'Vereinigte Arabische Emirate'},
    {'n':'Etihad Airways','c':'Vereinigte Arabische Emirate'},
    {'n':'Air Arabia','c':'Vereinigte Arabische Emirate'},
    {'n':'Ryanair','c':'Irland'},
    {'n':'easyJet','c':'Vereinigtes Königreich'},
    {'n':'Wizz Air','c':'Ungarn'},
    {'n':'Norwegian Air','c':'Norwegen'},
    {'n':'SAS Scandinavian Airlines','c':'Skandinavien'},
    {'n':'Finnair','c':'Finnland'},
    {'n':'TAP Air Portugal','c':'Portugal'},
    {'n':'Aeroflot','c':'Russland'},
    {'n':'Air China','c':'China'},
    {'n':'China Eastern','c':'China'},
    {'n':'China Southern','c':'China'},
    {'n':'Japan Airlines','c':'Japan'},
    {'n':'All Nippon Airways','c':'Japan'},
    {'n':'Korean Air','c':'Südkorea'},
    {'n':'Asiana Airlines','c':'Südkorea'},
    {'n':'Cathay Pacific','c':'Hongkong'},
    {'n':'Thai Airways','c':'Thailand'},
    {'n':'Malaysia Airlines','c':'Malaysia'},
    {'n':'Qantas','c':'Australien'},
    {'n':'Air New Zealand','c':'Neuseeland'},
    {'n':'LATAM Airlines','c':'Chile/Brasilien'},
    {'n':'Avianca','c':'Kolumbien'},
    {'n':'Air Canada','c':'Kanada'},
    {'n':'IndiGo','c':'Indien'},
    {'n':'Air India','c':'Indien'},
]
kext_list(k['fluggesellschaften'], airlines_new)
print(f"  fluggesellschaften: {len(k['fluggesellschaften'])} items")


# ── distanz_schaetzer (Match) 10 → 40 ──
distanz_new = [
    {'n':'London → Sydney','c':'17.000 km'},
    {'n':'New York → Los Angeles','c':'4.500 km'},
    {'n':'Tokio → Moskau','c':'7.500 km'},
    {'n':'Kapstadt → Kairo','c':'8.200 km'},
    {'n':'Buenos Aires → São Paulo','c':'2.100 km'},
    {'n':'Dubai → Singapur','c':'5.800 km'},
    {'n':'Madrid → Istanbul','c':'3.000 km'},
    {'n':'Los Angeles → Tokio','c':'8.800 km'},
    {'n':'Mumbai → Nairobi','c':'4.400 km'},
    {'n':'Sydney → Auckland','c':'2.200 km'},
    {'n':'Peking → Neu-Delhi','c':'3.800 km'},
    {'n':'Moskau → Wladiwostok','c':'6.400 km'},
    {'n':'Hamburg → Stockholm','c':'1.100 km'},
    {'n':'Amsterdam → Wien','c':'1.200 km'},
    {'n':'Rom → Athen','c':'1.000 km'},
    {'n':'Zürich → Budapest','c':'900 km'},
    {'n':'Oslo → Helsinki','c':'1.000 km'},
    {'n':'Warschau → Lissabon','c':'2.700 km'},
    {'n':'Bogotá → Lima','c':'2.400 km'},
    {'n':'Lagos → Johannesburg','c':'5.500 km'},
    {'n':'Kairo → Riad','c':'2.300 km'},
    {'n':'Bangkok → Kuala Lumpur','c':'1.400 km'},
    {'n':'Seoul → Schanghai','c':'950 km'},
    {'n':'Jakarta → Darwin','c':'2.700 km'},
    {'n':'Casablanca → Tunis','c':'2.300 km'},
    {'n':'Addis Abeba → Dakar','c':'6.700 km'},
    {'n':'Reykjavik → Genf','c':'3.000 km'},
    {'n':'Lissabon → Luxemburg','c':'1.700 km'},
    {'n':'Perth → Melbourne','c':'2.700 km'},
    {'n':'Anchorage → Vancouver','c':'2.600 km'},
]
kext_list(k['distanz_schaetzer'], distanz_new)
print(f"  distanz_schaetzer: {len(k['distanz_schaetzer'])} items")

# ── flugzeit_schaetzer (Match) 10 → 40 ──
flugzeit_new = [
    {'n':'Frankfurt → Dubai','c':'6 Std.'},
    {'n':'München → Bangkok','c':'11 Std.'},
    {'n':'Amsterdam → Tokio','c':'12 Std.'},
    {'n':'London → Singapur','c':'13 Std.'},
    {'n':'Paris → Montreal','c':'8 Std.'},
    {'n':'Madrid → Buenos Aires','c':'13 Std.'},
    {'n':'Zürich → Kapstadt','c':'11 Std.'},
    {'n':'Wien → Peking','c':'10 Std.'},
    {'n':'Berlin → New York','c':'9 Std.'},
    {'n':'Moskau → Peking','c':'8 Std.'},
    {'n':'Istanbul → Tokio','c':'11 Std.'},
    {'n':'Dubai → Sydney','c':'14 Std.'},
    {'n':'Singapore → London','c':'13 Std.'},
    {'n':'Los Angeles → Sydney','c':'15 Std.'},
    {'n':'New York → Tokyo','c':'14 Std.'},
    {'n':'São Paulo → Lissabon','c':'10 Std.'},
    {'n':'Johannesburg → Amsterdam','c':'11 Std.'},
    {'n':'Mumbai → London','c':'9 Std.'},
    {'n':'Seoul → Frankfurt','c':'12 Std.'},
    {'n':'Shanghai → Paris','c':'11 Std.'},
    {'n':'Sydney → Dallas','c':'17 Std.'},
    {'n':'Auckland → Los Angeles','c':'12 Std.'},
    {'n':'Nairobi → London','c':'9 Std.'},
    {'n':'Lagos → Peking','c':'16 Std.'},
    {'n':'Bogotá → Madrid','c':'9 Std.'},
    {'n':'Lima → Miami','c':'5 Std.'},
    {'n':'Doha → New York','c':'14 Std.'},
    {'n':'Helsinki → Bangkok','c':'10 Std.'},
    {'n':'Lissabon → Rio de Janeiro','c':'9 Std.'},
    {'n':'Riad → Kuala Lumpur','c':'8 Std.'},
]
kext_list(k['flugzeit_schaetzer'], flugzeit_new)
print(f"  flugzeit_schaetzer: {len(k['flugzeit_schaetzer'])} items")

# ── surf_spots (Pin) 10 → 40 ──
surf_new = [
    {'n':'Supertubes (Jeffrey\'s Bay)','lat':-34.05,'lng':24.93},
    {'n':'Teahupo\'o (Tahiti)','lat':-17.86,'lng':-149.24},
    {'n':'Uluwatu (Bali)','lat':-8.83,'lng':115.09},
    {'n':'Snapper Rocks (Gold Coast)','lat':-28.17,'lng':153.55},
    {'n':'Bells Beach (Victoria)','lat':-38.37,'lng':144.28},
    {'n':'Hossegor (Frankreich)','lat':43.66,'lng':-1.42},
    {'n':'Nazaré (Portugal)','lat':39.6,'lng':-9.06},
    {'n':'Peniche (Portugal)','lat':39.36,'lng':-9.38},
    {'n':'Mundaka (Spanien)','lat':43.4,'lng':-2.7},
    {'n':'Punta de Lobos (Chile)','lat':-34.4,'lng':-72.07},
    {'n':'Pichilemu (Chile)','lat':-34.39,'lng':-72.0},
    {'n':'Chicama (Peru)','lat':-7.84,'lng':-79.45},
    {'n':'Santa Cruz (Brasilien)','lat':-14.3,'lng':-38.9},
    {'n':'Tavarua (Fiji)','lat':-17.85,'lng':177.17},
    {'n':'Cloud 9 (Siargao, Philippinen)','lat':9.86,'lng':126.09},
    {'n':'G-Land (Java)','lat':-8.6,'lng':114.22},
    {'n':'Skeleton Bay (Namibia)','lat':-22.94,'lng':14.41},
    {'n':'Anchor Point (Marokko)','lat':30.03,'lng':-9.73},
    {'n':'Taghazout (Marokko)','lat':30.54,'lng':-9.71},
    {'n':'Mavericks (Kalifornien)','lat':37.49,'lng':-122.5},
    {'n':'Trestles (Kalifornien)','lat':33.37,'lng':-117.59},
    {'n':'Rincon (Kalifornien)','lat':34.37,'lng':-119.48},
    {'n':'Todos Santos (Mexiko)','lat':23.45,'lng':-110.22},
    {'n':'Puerto Escondido (Mexiko)','lat':15.87,'lng':-97.07},
    {'n':'Pavones (Costa Rica)','lat':8.39,'lng':-83.15},
    {'n':'Arpoador (Rio de Janeiro)','lat':-22.99,'lng':-43.19},
    {'n':'Thurso East (Schottland)','lat':58.6,'lng':-3.52},
    {'n':'Fistral Beach (Cornwall)','lat':50.42,'lng':-5.1},
    {'n':'Newquay (Cornwall)','lat':50.41,'lng':-5.08},
    {'n':'Bundoran (Irland)','lat':54.48,'lng':-8.29},
]
kext_pin(k['surf_spots'], surf_new)
print(f"  surf_spots: {len(k['surf_spots'])} items")


# ── hafen_world (Match) 12 → 40 ──
hafen_new = [
    {'n':'Hafen Shanghai','c':'China'},
    {'n':'Hafen Singapur','c':'Singapur'},
    {'n':'Hafen Ningbo-Zhoushan','c':'China'},
    {'n':'Hafen Shenzhen','c':'China'},
    {'n':'Hafen Guangzhou','c':'China'},
    {'n':'Hafen Busan','c':'Südkorea'},
    {'n':'Hafen Hongkong','c':'Hongkong'},
    {'n':'Hafen Qingdao','c':'China'},
    {'n':'Hafen Tianjin','c':'China'},
    {'n':'Hafen Antwerpen','c':'Belgien'},
    {'n':'Hafen Hamburg','c':'Deutschland'},
    {'n':'Hafen Los Angeles','c':'USA'},
    {'n':'Hafen Long Beach','c':'USA'},
    {'n':'Hafen Dubai (Jebel Ali)','c':'Vereinigte Arabische Emirate'},
    {'n':'Hafen Klang (Port Klang)','c':'Malaysia'},
    {'n':'Hafen Kaohsiung','c':'Taiwan'},
    {'n':'Hafen Xiamen','c':'China'},
    {'n':'Hafen Dalian','c':'China'},
    {'n':'Hafen Tanjung Pelepas','c':'Malaysia'},
    {'n':'Hafen Laem Chabang','c':'Thailand'},
    {'n':'Hafen New York/New Jersey','c':'USA'},
    {'n':'Hafen Valencia','c':'Spanien'},
    {'n':'Hafen Algeciras','c':'Spanien'},
    {'n':'Hafen Felixstowe','c':'Vereinigtes Königreich'},
    {'n':'Hafen Bremen/Bremerhaven','c':'Deutschland'},
    {'n':'Hafen Genua','c':'Italien'},
    {'n':'Hafen Marseille','c':'Frankreich'},
    {'n':'Hafen Santos','c':'Brasilien'},
    {'n':'Hafen Colombo','c':'Sri Lanka'},
]
kext_list(k['hafen_world'], hafen_new)
print(f"  hafen_world: {len(k['hafen_world'])} items")

# ── halbinseln (Match) 12 → 40 ──
halb_new = [
    {'n':'Arabische Halbinsel','c':'Saudi-Arabien'},
    {'n':'Indische Halbinsel (Dekkan)','c':'Indien'},
    {'n':'Halbinsel Malakka','c':'Malaysia'},
    {'n':'Koreanische Halbinsel','c':'Südkorea/Nordkorea'},
    {'n':'Kamtschatka','c':'Russland'},
    {'n':'Halbinsel Kola','c':'Russland'},
    {'n':'Halbinsel Krim','c':'Ukraine/Russland'},
    {'n':'Halbinsel Tschuktschen','c':'Russland'},
    {'n':'Halbinsel Taymyr','c':'Russland'},
    {'n':'Labrador-Halbinsel','c':'Kanada'},
    {'n':'Halbinsel Yucatán','c':'Mexiko'},
    {'n':'Florida-Halbinsel','c':'USA'},
    {'n':'Halbinsel Baja California','c':'Mexiko'},
    {'n':'Iberische Halbinsel','c':'Spanien/Portugal'},
    {'n':'Apennin-Halbinsel','c':'Italien'},
    {'n':'Balkan-Halbinsel','c':'Südosteuropa'},
    {'n':'Halbinsel Bretagne','c':'Frankreich'},
    {'n':'Jütland','c':'Dänemark'},
    {'n':'Halbinsel Kap Breton','c':'Kanada'},
    {'n':'Halbinsel Gaspe','c':'Kanada'},
    {'n':'Halbinsel Nova Scotia','c':'Kanada'},
    {'n':'Sinai-Halbinsel','c':'Ägypten'},
    {'n':'Halbinsel Katar','c':'Katar'},
    {'n':'Halbinsel Musandam','c':'Oman'},
    {'n':'Halbinsel Kathiawar','c':'Indien'},
    {'n':'Halbinsel Indochina','c':'Südostasien'},
    {'n':'Halbinsel Shanxi','c':'China'},
    {'n':'Halbinsel Liaodong','c':'China'},
]
kext_list(k['halbinseln'], halb_new)
print(f"  halbinseln: {len(k['halbinseln'])} items")

# ── inselgruppen (Match) 12 → 40 ──
ig_new = [
    {'n':'Malediven','c':'Malediven'},
    {'n':'Philippinen','c':'Philippinen'},
    {'n':'Japanische Inseln','c':'Japan'},
    {'n':'Indonesischer Archipel','c':'Indonesien'},
    {'n':'Karibische Inseln','c':'Karibik'},
    {'n':'Britische Inseln','c':'Vereinigtes Königreich'},
    {'n':'Färöer-Inseln','c':'Dänemark'},
    {'n':'Svalbard (Spitzbergen)','c':'Norwegen'},
    {'n':'Lofoten','c':'Norwegen'},
    {'n':'Ålandinseln','c':'Finnland'},
    {'n':'Kanareninseln','c':'Spanien'},
    {'n':'Balearen','c':'Spanien'},
    {'n':'Madeira','c':'Portugal'},
    {'n':'Kapverdische Inseln','c':'Kap Verde'},
    {'n':'São Tomé und Príncipe','c':'São Tomé und Príncipe'},
    {'n':'Komoren','c':'Komoren'},
    {'n':'Seychellen','c':'Seychellen'},
    {'n':'Maskarenen','c':'Mauritius/Réunion'},
    {'n':'Westindische Inseln (Kleine Antillen)','c':'Karibik'},
    {'n':'Falklandinseln','c':'Vereinigtes Königreich'},
    {'n':'Hawaii','c':'USA'},
    {'n':'Alëuten','c':'USA'},
    {'n':'Galapagos-Inseln','c':'Ecuador'},
    {'n':'Fernando de Noronha','c':'Brasilien'},
    {'n':'Cookinseln','c':'Neuseeland'},
    {'n':'Salomonen','c':'Salomonen'},
    {'n':'Fidschi','c':'Fidschi'},
    {'n':'Vanuatu','c':'Vanuatu'},
]
kext_list(k['inselgruppen'], ig_new)
print(f"  inselgruppen: {len(k['inselgruppen'])} items")


# ── kaps (Match) 12 → 40 ──
kaps_new = [
    {'n':'Kap Horn','c':'Chile'},
    {'n':'Kap Hoorn (Südamerika)','c':'Argentinien'},
    {'n':'Kap Farvel','c':'Grönland'},
    {'n':'Kap Nordkyn','c':'Norwegen'},
    {'n':'Kap Skagen','c':'Dänemark'},
    {'n':'Kap Agulhas','c':'Südafrika'},
    {'n':'Kap Guardafui','c':'Somalia'},
    {'n':'Kap Bon','c':'Tunesien'},
    {'n':'Kap Espartel','c':'Marokko'},
    {'n':'Kap Delgado','c':'Mosambik'},
    {'n':'Kap Tres Forcas','c':'Marokko'},
    {'n':'Kap Palmas','c':'Liberia'},
    {'n':'Kap Verde','c':'Senegal'},
    {'n':'Kap Bojador','c':'Westsahara'},
    {'n':'Kap Blanco','c':'Mauretanien'},
    {'n':'Kap Race','c':'Kanada'},
    {'n':'Kap Breton','c':'Kanada'},
    {'n':'Kap Sable','c':'Kanada'},
    {'n':'Point Barrow','c':'USA (Alaska)'},
    {'n':'Kap Prince of Wales','c':'USA (Alaska)'},
    {'n':'Kap Dezhnev','c':'Russland'},
    {'n':'Kap Chelyuskin','c':'Russland'},
    {'n':'Kap Kanin','c':'Russland'},
    {'n':'Kap Lopatka','c':'Russland'},
    {'n':'Kap Matapan','c':'Griechenland'},
    {'n':'Kap Sunion','c':'Griechenland'},
    {'n':'Kap Finisterre','c':'Spanien'},
    {'n':'Kap Ortegal','c':'Spanien'},
]
kext_list(k['kaps'], kaps_new)
print(f"  kaps: {len(k['kaps'])} items")

# ── meerbusen (Match) 12 → 40 ──
mb_new = [
    {'n':'Golf von Mexiko','c':'USA/Mexiko/Kuba'},
    {'n':'Golf von Guinea','c':'Westafrika'},
    {'n':'Golf von Bengalen','c':'Indien/Bangladesch'},
    {'n':'Golf von Oman','c':'Oman/Iran'},
    {'n':'Golf von Aden','c':'Jemen/Somalia'},
    {'n':'Golf von Suez','c':'Ägypten'},
    {'n':'Golf von Akaba','c':'Jordanien/Saudi-Arabien'},
    {'n':'Golf von Kutsch','c':'Indien'},
    {'n':'Golf von Khambhat','c':'Indien'},
    {'n':'Golf von Thailand','c':'Thailand'},
    {'n':'Golf von Tonkin','c':'Vietnam/China'},
    {'n':'Golf von Alaska','c':'USA'},
    {'n':'Gulf of St. Lawrence','c':'Kanada'},
    {'n':'Hudson Bay','c':'Kanada'},
    {'n':'James Bay','c':'Kanada'},
    {'n':'Baffin Bay','c':'Kanada/Grönland'},
    {'n':'Bothnia-Bucht','c':'Schweden/Finnland'},
    {'n':'Rigaer Meerbusen','c':'Lettland/Estland'},
    {'n':'Finnischer Meerbusen','c':'Finnland/Estland/Russland'},
    {'n':'Bucht von Neapel','c':'Italien'},
    {'n':'Bucht von Biscaya','c':'Spanien/Frankreich'},
    {'n':'Ligurisches Meer-Bucht','c':'Frankreich/Italien'},
    {'n':'Korinthischer Golf','c':'Griechenland'},
    {'n':'Saronischer Golf','c':'Griechenland'},
    {'n':'Thermaischer Golf','c':'Griechenland'},
    {'n':'Bucht von Bengasi','c':'Libyen'},
    {'n':'Große Syrte','c':'Libyen'},
    {'n':'Bucht von Bight of Bonny','c':'Nigeria'},
]
kext_list(k['meerbusen'], mb_new)
print(f"  meerbusen: {len(k['meerbusen'])} items")

# ── seen_match (Match) 12 → 40 ──
seen_new = [
    {'n':'Kaspisches Meer','c':'Russland/Aserbaidschan'},
    {'n':'Oberer See','c':'USA/Kanada'},
    {'n':'Victoriasee','c':'Kenia/Uganda/Tansania'},
    {'n':'Huronsee','c':'USA/Kanada'},
    {'n':'Michigansee','c':'USA'},
    {'n':'Tanganjikasee','c':'Kongo/Tansania/Sambia'},
    {'n':'Großer Bärensee','c':'Kanada'},
    {'n':'Malawisee','c':'Malawi/Mosambik/Tansania'},
    {'n':'Großer Sklavensee','c':'Kanada'},
    {'n':'Eriesee','c':'USA/Kanada'},
    {'n':'Winnipegsee','c':'Kanada'},
    {'n':'Ontariosee','c':'USA/Kanada'},
    {'n':'Balchash-See','c':'Kasachstan'},
    {'n':'Ladogasee','c':'Russland'},
    {'n':'Onega-See','c':'Russland'},
    {'n':'Volta-Stausee','c':'Ghana'},
    {'n':'Titicacasee','c':'Peru/Bolivien'},
    {'n':'Nicaraguasee','c':'Nicaragua'},
    {'n':'Athabasca-See','c':'Kanada'},
    {'n':'Turkana-See','c':'Kenia/Äthiopien'},
    {'n':'Reindeer Lake','c':'Kanada'},
    {'n':'Issyk-Kul','c':'Kirgisistan'},
    {'n':'Torrens-See','c':'Australien'},
    {'n':'Eyre-See','c':'Australien'},
    {'n':'Müggelsee','c':'Deutschland'},
    {'n':'Starnberger See','c':'Deutschland'},
    {'n':'Chiemsee','c':'Deutschland'},
    {'n':'Genfer See','c':'Schweiz/Frankreich'},
]
kext_list(k['seen_match'], seen_new)
print(f"  seen_match: {len(k['seen_match'])} items")


# ── bahnstrecken (Match) 12 → 40 ──
bahn_new = [
    {'n':'Transsibirische Eisenbahn (komplette Route)','c':'Russland'},
    {'n':'TGV (Paris–Lyon)','c':'Frankreich'},
    {'n':'Eurostar (London–Paris)','c':'Vereinigtes Königreich/Frankreich'},
    {'n':'ICE (Hamburg–München)','c':'Deutschland'},
    {'n':'Shinkansen (Tokio–Osaka)','c':'Japan'},
    {'n':'AVE (Madrid–Barcelona)','c':'Spanien'},
    {'n':'Frecciarossa (Mailand–Rom)','c':'Italien'},
    {'n':'Thalys (Paris–Brüssel–Amsterdam)','c':'Frankreich/Belgien'},
    {'n':'Orient Express (historisch)','c':'Europa/Asien'},
    {'n':'Indian Pacific (Sydney–Perth)','c':'Australien'},
    {'n':'The Ghan (Adelaide–Darwin)','c':'Australien'},
    {'n':'Rocky Mountaineer','c':'Kanada'},
    {'n':'Glacier Express (Zermatt–St. Moritz)','c':'Schweiz'},
    {'n':'Bernina Express','c':'Schweiz/Italien'},
    {'n':'Flam Railway','c':'Norwegen'},
    {'n':'Douro-Linie','c':'Portugal'},
    {'n':'Ferrocarril Arica–La Paz','c':'Chile/Bolivien'},
    {'n':'Bahn zum Dach der Welt (Lhasa)','c':'China'},
    {'n':'Trans-Australische Eisenbahn','c':'Australien'},
    {'n':'CPRR (Kontinent-Überquerung)','c':'USA'},
    {'n':'Amtrak Sunset Limited','c':'USA'},
    {'n':'California Zephyr','c':'USA'},
    {'n':'Empire Builder','c':'USA'},
    {'n':'Via Rail The Canadian','c':'Kanada'},
    {'n':'West Highland Line','c':'Vereinigtes Königreich'},
    {'n':'Jacobite Steam Train','c':'Vereinigtes Königreich'},
    {'n':'Darjeeling Himalayan Railway','c':'Indien'},
    {'n':'Nilgiri Mountain Railway','c':'Indien'},
]
kext_list(k['bahnstrecken'], bahn_new)
print(f"  bahnstrecken: {len(k['bahnstrecken'])} items")

# ── autobahnen_beruhmt (Match) 12 → 40 ──
aut_new = [
    {'n':'Route 66 (Historic)','c':'USA'},
    {'n':'Pan-American Highway','c':'Nordamerika–Südamerika'},
    {'n':'Pacific Coast Highway (US-1)','c':'USA'},
    {'n':'Stelvio Pass Road','c':'Italien'},
    {'n':'Gotthard-Route','c':'Schweiz'},
    {'n':'Great Ocean Road','c':'Australien'},
    {'n':'Garden Route','c':'Südafrika'},
    {'n':'Furka Pass','c':'Schweiz'},
    {'n':'Transfăgărășan','c':'Rumänien'},
    {'n':'Trollstigen','c':'Norwegen'},
    {'n':'Atlantic Ocean Road','c':'Norwegen'},
    {'n':'Ring Road (Route 1)','c':'Island'},
    {'n':'Karakorum Highway','c':'Pakistan/China'},
    {'n':'Icefields Parkway','c':'Kanada'},
    {'n':'Cabot Trail','c':'Kanada'},
    {'n':'Milford Road (SH94)','c':'Neuseeland'},
    {'n':'Skipper\'s Canyon Road','c':'Neuseeland'},
    {'n':'Road to Hana','c':'USA (Hawaii)'},
    {'n':'Going-to-the-Sun Road','c':'USA'},
    {'n':'Beartooth Highway','c':'USA'},
    {'n':'Dalton Highway','c':'USA (Alaska)'},
    {'n':'Death Valley Road','c':'USA'},
    {'n':'Ruta 40','c':'Argentinien'},
    {'n':'Carretera Austral','c':'Chile'},
    {'n':'Death Road (Yungas Road)','c':'Bolivien'},
    {'n':'Silk Road Highways','c':'Zentralasien'},
    {'n':'Eyre Highway','c':'Australien'},
    {'n':'Gibb River Road','c':'Australien'},
]
kext_list(k['autobahnen_beruhmt'], aut_new)
print(f"  autobahnen_beruhmt: {len(k['autobahnen_beruhmt'])} items")

# ── deltamuendungen (Match) 12 → 35 ──
delta_new = [
    {'n':'Amazonas-Delta','c':'Brasilien'},
    {'n':'Ganges-Brahmaputra-Delta','c':'Bangladesch/Indien'},
    {'n':'Mekong-Delta','c':'Vietnam'},
    {'n':'Mississippi-Delta','c':'USA'},
    {'n':'Irrawaddy-Delta','c':'Myanmar'},
    {'n':'Niger-Delta','c':'Nigeria'},
    {'n':'Indus-Delta','c':'Pakistan'},
    {'n':'Orinoco-Delta','c':'Venezuela'},
    {'n':'Donau-Delta','c':'Rumänien/Ukraine'},
    {'n':'Ebro-Delta','c':'Spanien'},
    {'n':'Po-Delta','c':'Italien'},
    {'n':'Rhein-Delta (Ijsselmeer)','c':'Niederlande'},
    {'n':'Lena-Delta','c':'Russland'},
    {'n':'Ob-Delta','c':'Russland'},
    {'n':'Huang He-Delta (Gelber Fluss)','c':'China'},
    {'n':'Yangtze-Delta','c':'China'},
    {'n':'Río de la Plata-Delta','c':'Argentinien/Uruguay'},
    {'n':'Okavango-Delta','c':'Botswana'},
    {'n':'Sakramentodelta','c':'USA'},
    {'n':'Tigris-Euphrat-Delta (Schatt al-Arab)','c':'Irak'},
    {'n':'Fly-Delta','c':'Papua-Neuguinea'},
    {'n':'Zambezi-Delta','c':'Mosambik'},
    {'n':'Volta-Delta','c':'Ghana'},
]
kext_list(k['deltamuendungen'], delta_new)
print(f"  deltamuendungen: {len(k['deltamuendungen'])} items")


# ── grenzfluesse (Match) 12 → 35 ──
grenz_new = [
    {'n':'Amazonas (entspringt in)','c':'Peru'},
    {'n':'Rio Grande (Grenze USA–Mexiko)','c':'USA/Mexiko'},
    {'n':'Oder (Grenze Deutschland–Polen)','c':'Deutschland/Polen'},
    {'n':'Neiße (Grenze Deutschland–Polen)','c':'Deutschland/Polen'},
    {'n':'Inn (Grenzfluss)','c':'Österreich/Deutschland'},
    {'n':'Donau (Grenze Serbien–Rumänien)','c':'Serbien/Rumänien'},
    {'n':'Save (Grenze Bosnien–Kroatien)','c':'Bosnien/Kroatien'},
    {'n':'Drina (Grenze Bosnien–Serbien)','c':'Bosnien/Serbien'},
    {'n':'Tijuana (Grenzfluss)','c':'USA/Mexiko'},
    {'n':'Jordan (Grenze Israel–Jordanien)','c':'Israel/Jordanien'},
    {'n':'Sambesi (Grenze Sambia–Zimbabwe)','c':'Sambia/Zimbabwe'},
    {'n':'Oranje (Grenze Südafrika–Namibia)','c':'Südafrika/Namibia'},
    {'n':'Limpopo','c':'Südafrika/Mosambik'},
    {'n':'Kongo (Grenzfluss)','c':'Kongo/DR Kongo'},
    {'n':'Senegal (Grenzfluss)','c':'Senegal/Mauretanien'},
    {'n':'Amur (Grenze Russland–China)','c':'Russland/China'},
    {'n':'Ussuri (Grenze Russland–China)','c':'Russland/China'},
    {'n':'Ili (Grenzfluss)','c':'Kasachstan/China'},
    {'n':'Talas (Grenzfluss)','c':'Kirgisistan/Kasachstan'},
    {'n':'Mekong (Grenze Laos–Thailand)','c':'Laos/Thailand'},
    {'n':'Brahmaputra (Grenzfluss)','c':'China/Indien'},
    {'n':'Paraná (Grenze Argentinien–Paraguay)','c':'Argentinien/Paraguay'},
    {'n':'Uruguay (Grenzfluss)','c':'Argentinien/Uruguay'},
]
kext_list(k['grenzfluesse'], grenz_new)
print(f"  grenzfluesse: {len(k['grenzfluesse'])} items")

# ── nationalsport_off (Match) 12 → 35 ──
ns_new = [
    {'n':'Cricket (offiziell)','c':'England'},
    {'n':'Sumo (Nationalsport)','c':'Japan'},
    {'n':'Taekwondo (Nationalsport)','c':'Südkorea'},
    {'n':'Muay Thai (Nationalsport)','c':'Thailand'},
    {'n':'Kabbadi (offiziell)','c':'Indien'},
    {'n':'Buzkashi (Nationalsport)','c':'Afghanistan'},
    {'n':'Polo (historisch)','c':'Iran'},
    {'n':'Ice Hockey (offiziell)','c':'Kanada'},
    {'n':'Lacrosse (offiziell)','c':'Kanada'},
    {'n':'Baseball (de facto)','c':'USA'},
    {'n':'Vóleibol playa (offiziell)','c':'Brasilien'},
    {'n':'Futsal (offiziell)','c':'Brasilien'},
    {'n':'Polo (Nationalsport)','c':'Argentinien'},
    {'n':'Pato (Nationalsport)','c':'Argentinien'},
    {'n':'Bocce (Nationalsport)','c':'Italien'},
    {'n':'Pelota vasca','c':'Spanien (Baskenland)'},
    {'n':'Schwingen (offiziell)','c':'Schweiz'},
    {'n':'Hurling (Nationalsport)','c':'Irland'},
    {'n':'Gaelic Football (Nationalsport)','c':'Irland'},
    {'n':'Shinty (Nationalsport)','c':'Schottland'},
    {'n':'Sepak Takraw','c':'Malaysia'},
    {'n':'Silat (Nationalsport)','c':'Malaysia'},
    {'n':'Saman (Tanz-Sport)','c':'Indonesien'},
]
kext_list(k['nationalsport_off'], ns_new)
print(f"  nationalsport_off: {len(k['nationalsport_off'])} items")

# ── bruecken (Pin) 15 → 40 ──
bruecken_new = [
    {'n':'Danyang-Kunshan-Brücke','lat':31.5,'lng':119.5,'c':'China'},
    {'n':'Tianjin-Brücke (Lang-Fang–Qingxian)','lat':38.8,'lng':116.9,'c':'China'},
    {'n':'Weinan Weihe-Brücke','lat':34.5,'lng':109.8,'c':'China'},
    {'n':'Hangzhou Bay Bridge','lat':30.43,'lng':121.05,'c':'China'},
    {'n':'Jiaozhou Bay Bridge','lat':36.16,'lng':120.2,'c':'China'},
    {'n':'Øresundbrücke','lat':55.58,'lng':12.77,'c':'Schweden/Dänemark'},
    {'n':'Pont de Normandie','lat':49.44,'lng':0.36,'c':'Frankreich'},
    {'n':'Viaduc de Millau','lat':44.08,'lng':3.02,'c':'Frankreich'},
    {'n':'Pont du Gard','lat':43.95,'lng':4.54,'c':'Frankreich'},
    {'n':'Rialto-Brücke','lat':45.44,'lng':12.34,'c':'Italien'},
    {'n':'Ponte Vecchio','lat':43.77,'lng':11.25,'c':'Italien'},
    {'n':'Akashi-Kaikyō-Brücke','lat':34.62,'lng':135.02,'c':'Japan'},
    {'n':'Storebælt-Brücke','lat':55.34,'lng':11.0,'c':'Dänemark'},
    {'n':'Tsing Ma Bridge','lat':22.35,'lng':114.07,'c':'Hongkong'},
    {'n':'Bosphorus-Brücke (15 Juli)','lat':41.05,'lng':29.04,'c':'Türkei'},
    {'n':'Fatih Sultan Mehmet-Brücke','lat':41.09,'lng':29.06,'c':'Türkei'},
    {'n':'Humber-Brücke','lat':53.71,'lng':-0.44,'c':'Vereinigtes Königreich'},
    {'n':'Clifton Suspension Bridge','lat':51.46,'lng':-2.63,'c':'Vereinigtes Königreich'},
    {'n':'Forth Bridge (Railway)','lat':56.0,'lng':-3.39,'c':'Vereinigtes Königreich'},
    {'n':'Millennium Bridge (London)','lat':51.51,'lng':-0.1,'c':'Vereinigtes Königreich'},
    {'n':'Charles Bridge (Prag)','lat':50.09,'lng':14.41,'c':'Tschechien'},
    {'n':'Chain Bridge (Budapest)','lat':47.5,'lng':19.04,'c':'Ungarn'},
    {'n':'Lupu-Brücke','lat':31.22,'lng':121.42,'c':'China'},
    {'n':'Royal Gorge Bridge','lat':38.45,'lng':-105.36,'c':'USA'},
    {'n':'Verrazzano-Narrows Bridge','lat':40.6,'lng':-74.04,'c':'USA'},
]
kext_pin(k['bruecken'], bruecken_new)
print(f"  bruecken: {len(k['bruecken'])} items")


# ── filmsets (Pin) 15 → 40 ──
film_new = [
    {'n':'Mos Espa (Star Wars, Tunesien)','lat':33.98,'lng':7.99,'c':'Tunesien'},
    {'n':'Game of Thrones – Dubrovnik','lat':42.65,'lng':18.09,'c':'Kroatien'},
    {'n':'Game of Thrones – Split (Diokletianspalast)','lat':43.51,'lng':16.44,'c':'Kroatien'},
    {'n':'The Dark Knight (Chicago)','lat':41.88,'lng':-87.63,'c':'USA'},
    {'n':'Jurassic Park (Kauai, Hawaii)','lat':22.2,'lng':-159.5,'c':'USA'},
    {'n':'Indiana Jones – Jordanien (Petra)','lat':30.33,'lng':35.44,'c':'Jordanien'},
    {'n':'Braveheart (Schottland)','lat':56.8,'lng':-4.0,'c':'Vereinigtes Königreich'},
    {'n':'Harry Potter – Alnwick Castle','lat':55.42,'lng':-1.71,'c':'Vereinigtes Königreich'},
    {'n':'Harry Potter – Glenfinnan-Viadukt','lat':56.87,'lng':-5.44,'c':'Vereinigtes Königreich'},
    {'n':'Gladiator – Römisches Kolosseum','lat':41.89,'lng':12.49,'c':'Italien'},
    {'n':'Mamma Mia – Skopelos','lat':39.12,'lng':23.72,'c':'Griechenland'},
    {'n':'Captain Corelli – Kefalonia','lat':38.18,'lng':20.69,'c':'Griechenland'},
    {'n':'Lawrence of Arabia – Wadi Rum','lat':29.59,'lng':35.42,'c':'Jordanien'},
    {'n':'Mad Max – Namibia (Skeleton Coast)','lat':-22.9,'lng':14.5,'c':'Namibia'},
    {'n':'Sahara (Marokko – Ait Benhaddou)','lat':31.05,'lng':-7.13,'c':'Marokko'},
    {'n':'James Bond – Asgard (Norwegen)','lat':61.0,'lng':6.5,'c':'Norwegen'},
    {'n':'Kill Bill – Tokio','lat':35.68,'lng':139.69,'c':'Japan'},
    {'n':'Lost in Translation – Tokio','lat':35.67,'lng':139.76,'c':'Japan'},
    {'n':'Avatar – Zhangjiajie','lat':29.32,'lng':110.43,'c':'China'},
    {'n':'The Beach – Ko Phi Phi Leh','lat':7.68,'lng':98.76,'c':'Thailand'},
    {'n':'The Mission – Iguazú-Fälle','lat':-25.69,'lng':-54.44,'c':'Argentinien/Brasilien'},
    {'n':'Narnia – Fjaerland (Norwegen)','lat':61.42,'lng':6.77,'c':'Norwegen'},
    {'n':'Bond (Skyfall) – Glencoe','lat':56.68,'lng':-4.9,'c':'Vereinigtes Königreich'},
    {'n':'Ben-Hur – Cinecittà (Rom)','lat':41.84,'lng':12.56,'c':'Italien'},
    {'n':'Lord of the Rings – Matamata','lat':-37.87,'lng':175.68,'c':'Neuseeland'},
]
kext_pin(k['filmsets'], film_new)
print(f"  filmsets: {len(k['filmsets'])} items")

# ── gotteshaeuser (Pin) 15 → 40 ──
gh_new = [
    {'n':'Petersdom (Vatikan)','lat':41.9,'lng':12.45,'c':'Vatikan'},
    {'n':'Sagrada Família','lat':41.4,'lng':2.17,'c':'Spanien'},
    {'n':'Notre-Dame de Paris','lat':48.85,'lng':2.35,'c':'Frankreich'},
    {'n':'Kölner Dom','lat':50.94,'lng':6.96,'c':'Deutschland'},
    {'n':'Westminster Abbey','lat':51.5,'lng':-0.13,'c':'Vereinigtes Königreich'},
    {'n':'Blue Mosque (Sultan-Ahmed-Moschee)','lat':41.0,'lng':28.98,'c':'Türkei'},
    {'n':'Al-Masjid al-Haram (Mekka)','lat':21.42,'lng':39.83,'c':'Saudi-Arabien'},
    {'n':'Al-Masjid an-Nabawi (Medina)','lat':24.47,'lng':39.61,'c':'Saudi-Arabien'},
    {'n':'Tempel des Himmels (Peking)','lat':39.88,'lng':116.41,'c':'China'},
    {'n':'Goldener Tempel (Amritsar)','lat':31.62,'lng':74.88,'c':'Indien'},
    {'n':'Angkor Wat','lat':13.41,'lng':103.87,'c':'Kambodscha'},
    {'n':'Borobudur','lat':-7.61,'lng':110.2,'c':'Indonesien'},
    {'n':'Brihadesvara-Tempel','lat':10.78,'lng':79.13,'c':'Indien'},
    {'n':'Meenakshi-Tempel','lat':9.92,'lng':78.12,'c':'Indien'},
    {'n':'Shwedagon-Pagode','lat':16.8,'lng':96.15,'c':'Myanmar'},
    {'n':'Kiyomizu-dera','lat':34.99,'lng':135.79,'c':'Japan'},
    {'n':'Tosho-gu (Nikkō)','lat':36.76,'lng':139.6,'c':'Japan'},
    {'n':'Göbekli Tepe','lat':37.22,'lng':38.92,'c':'Türkei'},
    {'n':'Church of the Holy Sepulchre','lat':31.78,'lng':35.23,'c':'Israel'},
    {'n':'Felsendom (Jerusalem)','lat':31.78,'lng':35.24,'c':'Israel'},
    {'n':'Wailing Wall','lat':31.78,'lng':35.23,'c':'Israel'},
    {'n':'Kathedrale von Santiago de Compostela','lat':42.88,'lng':-8.54,'c':'Spanien'},
    {'n':'Kathedrale von Chartres','lat':48.45,'lng':1.49,'c':'Frankreich'},
    {'n':'Mont-Saint-Michel','lat':48.64,'lng':-1.51,'c':'Frankreich'},
    {'n':'Chevet (Cluny)','lat':46.43,'lng':4.66,'c':'Frankreich'},
]
kext_pin(k['gotteshaeuser'], gh_new)
print(f"  gotteshaeuser: {len(k['gotteshaeuser'])} items")


# ── kunstwerke (Pin) 15 → 40 ──
kunst_new = [
    {'n':'Sixtinische Kapelle (Michelangelo)','lat':41.9,'lng':12.45,'c':'Vatikan'},
    {'n':'Nachtwache (Rijksmuseum)','lat':52.36,'lng':4.89,'c':'Niederlande'},
    {'n':'Guernica (Museo Reina Sofía)','lat':40.41,'lng':-3.69,'c':'Spanien'},
    {'n':'The Starry Night (MoMA)','lat':40.77,'lng':-73.98,'c':'USA'},
    {'n':'The Scream – Original (Nationalgalerie Oslo)','lat':59.91,'lng':10.74,'c':'Norwegen'},
    {'n':'Birth of Venus (Uffizien)','lat':43.77,'lng':11.26,'c':'Italien'},
    {'n':'David (Accademia)','lat':43.78,'lng':11.26,'c':'Italien'},
    {'n':'Die Erschaffung Adams (Vatikan)','lat':41.9,'lng':12.45,'c':'Vatikan'},
    {'n':'Girl with a Pearl Earring (Mauritshuis)','lat':52.08,'lng':4.31,'c':'Niederlande'},
    {'n':'The Last Supper (Santa Maria delle Grazie)','lat':45.47,'lng':9.17,'c':'Italien'},
    {'n':'American Gothic (Art Institute Chicago)','lat':41.88,'lng':-87.62,'c':'USA'},
    {'n':'Water Lilies (Musée de l\'Orangerie)','lat':48.86,'lng':2.33,'c':'Frankreich'},
    {'n':'Las Meninas (Prado)','lat':40.41,'lng':-3.69,'c':'Spanien'},
    {'n':'A Sunday on La Grande Jatte (Chicago)','lat':41.88,'lng':-87.62,'c':'USA'},
    {'n':'The Kiss (Klimt, Belvedere)','lat':48.19,'lng':16.38,'c':'Österreich'},
    {'n':'Sunflowers (Van Gogh, National Gallery)','lat':51.51,'lng':-0.13,'c':'Vereinigtes Königreich'},
    {'n':'The Persistence of Memory (MoMA)','lat':40.77,'lng':-73.98,'c':'USA'},
    {'n':'Frida Kahlo – Self Portrait (Museo Frida Kahlo)','lat':19.36,'lng':-99.16,'c':'Mexiko'},
    {'n':'The Great Wave (Tokyo National Museum)','lat':35.72,'lng':139.77,'c':'Japan'},
    {'n':'Terrakotta-Armee (Xi\'an Museum)','lat':34.38,'lng':109.27,'c':'China'},
    {'n':'Elgin Marbles (British Museum)','lat':51.52,'lng':-0.13,'c':'Vereinigtes Königreich'},
    {'n':'Nofretete-Büste (Neues Museum Berlin)','lat':52.52,'lng':13.4,'c':'Deutschland'},
    {'n':'Rosette Stone (British Museum)','lat':51.52,'lng':-0.13,'c':'Vereinigtes Königreich'},
    {'n':'Venus de Milo (Louvre)','lat':48.86,'lng':2.34,'c':'Frankreich'},
    {'n':'Winged Victory (Louvre)','lat':48.86,'lng':2.34,'c':'Frankreich'},
]
kext_pin(k['kunstwerke'], kunst_new)
print(f"  kunstwerke: {len(k['kunstwerke'])} items")

# ── ruinen (Pin) 15 → 40 ──
ruinen_new = [
    {'n':'Machu Picchu','lat':-13.16,'lng':-72.55,'c':'Peru'},
    {'n':'Chichen Itza','lat':20.68,'lng':-88.57,'c':'Mexiko'},
    {'n':'Teotihuacan','lat':19.69,'lng':-98.84,'c':'Mexiko'},
    {'n':'Tikal','lat':17.22,'lng':-89.62,'c':'Guatemala'},
    {'n':'Angkor (gesamt)','lat':13.44,'lng':103.83,'c':'Kambodscha'},
    {'n':'Bagan (Tempel)','lat':21.17,'lng':94.86,'c':'Myanmar'},
    {'n':'Pompeji','lat':40.75,'lng':14.49,'c':'Italien'},
    {'n':'Herculaneum','lat':40.81,'lng':14.35,'c':'Italien'},
    {'n':'Ephesos','lat':37.94,'lng':27.34,'c':'Türkei'},
    {'n':'Troja','lat':39.96,'lng':26.24,'c':'Türkei'},
    {'n':'Persepolis','lat':29.94,'lng':52.89,'c':'Iran'},
    {'n':'Pasargadae','lat':30.19,'lng':53.18,'c':'Iran'},
    {'n':'Karthago','lat':36.86,'lng':10.32,'c':'Tunesien'},
    {'n':'Leptis Magna','lat':32.64,'lng':14.29,'c':'Libyen'},
    {'n':'Great Zimbabwe','lat':-20.27,'lng':30.93,'c':'Zimbabwe'},
    {'n':'Meroe (Pyramiden)','lat':16.94,'lng':33.75,'c':'Sudan'},
    {'n':'Aksum','lat':14.13,'lng':38.73,'c':'Äthiopien'},
    {'n':'Lalibela','lat':12.03,'lng':39.04,'c':'Äthiopien'},
    {'n':'Palmyra','lat':34.55,'lng':38.27,'c':'Syrien'},
    {'n':'Baalbek','lat':34.0,'lng':36.21,'c':'Libanon'},
    {'n':'Jerash','lat':32.28,'lng':35.9,'c':'Jordanien'},
    {'n':'Mohenjo-daro','lat':27.32,'lng':68.14,'c':'Pakistan'},
    {'n':'Hampi','lat':15.34,'lng':76.46,'c':'Indien'},
    {'n':'Konark Sun Temple','lat':19.89,'lng':86.09,'c':'Indien'},
    {'n':'Sukhothai','lat':17.02,'lng':99.82,'c':'Thailand'},
]
kext_pin(k['ruinen'], ruinen_new)
print(f"  ruinen: {len(k['ruinen'])} items")

# ── wein_regionen (Pin) 15 → 40 ──
wein_new = [
    {'n':'Napa Valley','lat':38.5,'lng':-122.33,'c':'USA'},
    {'n':'Sonoma','lat':38.29,'lng':-122.46,'c':'USA'},
    {'n':'Willamette Valley','lat':45.3,'lng':-123.0,'c':'USA'},
    {'n':'Rioja','lat':42.45,'lng':-2.44,'c':'Spanien'},
    {'n':'Ribera del Duero','lat':41.65,'lng':-3.68,'c':'Spanien'},
    {'n':'Priorat','lat':41.18,'lng':0.77,'c':'Spanien'},
    {'n':'Barossa Valley','lat':-34.53,'lng':138.95,'c':'Australien'},
    {'n':'Hunter Valley','lat':-32.77,'lng':151.15,'c':'Australien'},
    {'n':'Marlborough','lat':-41.51,'lng':173.96,'c':'Neuseeland'},
    {'n':'Hawkes Bay','lat':-39.63,'lng':176.87,'c':'Neuseeland'},
    {'n':'Mendoza','lat':-32.89,'lng':-68.84,'c':'Argentinien'},
    {'n':'Valle de Casablanca','lat':-33.32,'lng':-71.41,'c':'Chile'},
    {'n':'Franschhoek','lat':-33.91,'lng':19.12,'c':'Südafrika'},
    {'n':'Stellenbosch','lat':-33.93,'lng':18.86,'c':'Südafrika'},
    {'n':'Pfalz (Weinregion)','lat':49.31,'lng':7.99,'c':'Deutschland'},
    {'n':'Mosel','lat':50.05,'lng':7.1,'c':'Deutschland'},
    {'n':'Rheingau','lat':50.03,'lng':8.0,'c':'Deutschland'},
    {'n':'Franken','lat':49.8,'lng':10.0,'c':'Deutschland'},
    {'n':'Niederösterreich (Wachau)','lat':48.36,'lng':15.43,'c':'Österreich'},
    {'n':'Steiermark (Südsteiermark)','lat':46.65,'lng':15.53,'c':'Österreich'},
    {'n':'Valais','lat':46.23,'lng':7.36,'c':'Schweiz'},
    {'n':'Vaud (Lavaux)','lat':46.52,'lng':6.68,'c':'Schweiz'},
    {'n':'Douro','lat':41.2,'lng':-7.5,'c':'Portugal'},
    {'n':'Alentejo','lat':38.5,'lng':-8.0,'c':'Portugal'},
    {'n':'Tokaj','lat':48.12,'lng':21.42,'c':'Ungarn'},
]
kext_pin(k['wein_regionen'], wein_new)
print(f"  wein_regionen: {len(k['wein_regionen'])} items")


# ── metrostaedte (Match) 14 → 40 ──
metro_new = [
    {'n':'New York City Subway','c':'USA'},
    {'n':'London Underground','c':'Vereinigtes Königreich'},
    {'n':'Paris Métro','c':'Frankreich'},
    {'n':'Moskauer Metro','c':'Russland'},
    {'n':'Peking Metro','c':'China'},
    {'n':'Shanghai Metro','c':'China'},
    {'n':'Berlin U-Bahn + S-Bahn','c':'Deutschland'},
    {'n':'Wiener U-Bahn','c':'Österreich'},
    {'n':'München U-Bahn','c':'Deutschland'},
    {'n':'Hamburg U-Bahn','c':'Deutschland'},
    {'n':'Madrid Metro','c':'Spanien'},
    {'n':'Barcelona Metro','c':'Spanien'},
    {'n':'Rome Metro','c':'Italien'},
    {'n':'Milan Metro','c':'Italien'},
    {'n':'Stockholm T-Bana','c':'Schweden'},
    {'n':'Oslo T-bane','c':'Norwegen'},
    {'n':'Kopenhagen Metro','c':'Dänemark'},
    {'n':'Amsterdam Metro','c':'Niederlande'},
    {'n':'Brüssel Metro','c':'Belgien'},
    {'n':'Lissabon Metro','c':'Portugal'},
    {'n':'Athen Metro','c':'Griechenland'},
    {'n':'Budapest Metro','c':'Ungarn'},
    {'n':'Prag Metro','c':'Tschechien'},
    {'n':'Warschau Metro','c':'Polen'},
    {'n':'Seoul Metro','c':'Südkorea'},
    {'n':'Tokio Metro','c':'Japan'},
]
kext_list(k['metrostaedte'], metro_new)
print(f"  metrostaedte: {len(k['metrostaedte'])} items")

# ── luft_rekorde (Match) 8 → 25 ──
luft_new = [
    {'n':'Größte Spannweite (Antonov An-225)','c':'Ukraine'},
    {'n':'Schnellster Düsenjäger (SR-71 Blackbird)','c':'USA'},
    {'n':'Erster Schallmauer-Durchbruch (Bell X-1)','c':'USA'},
    {'n':'Tiefster Tauchgang (Marianengraben-Drohne)','c':'USA'},
    {'n':'Erste Umrundung ohne Landung (Rutan Voyager)','c':'USA'},
    {'n':'Erster bemannter Ballon (Montgolfier)','c':'Frankreich'},
    {'n':'Erster Solarflug (Solar Impulse 2)','c':'Schweiz'},
    {'n':'Erste Transatlantik-Soloflug (Lindbergh)','c':'USA'},
    {'n':'Schnellstes Passagierflugzeug (Concorde)','c':'Frankreich/UK'},
    {'n':'Erster Motorflug (Wright Brothers)','c':'USA'},
    {'n':'Längste Nonstop-Passagierroute (Singapore–NY)','c':'Singapur/USA'},
    {'n':'Meistgebautes Verkehrsflugzeug (Boeing 737)','c':'USA'},
    {'n':'Größtes Passagierflugzeug (Airbus A380)','c':'Frankreich'},
    {'n':'Erste Frau im Weltall (Valentina Tereshkova)','c':'Russland'},
    {'n':'Höchster bewohnter Flughafen (Daocheng Yading, 4411m)','c':'China'},
    {'n':'Erster Überschalldurchbruch auf Rückflug (Yeager)','c':'USA'},
    {'n':'Erster Jumbo-Jet (Boeing 747)','c':'USA'},
]
kext_list(k['luft_rekorde'], luft_new)
print(f"  luft_rekorde: {len(k['luft_rekorde'])} items")

# Speichern kultur.json
save('kultur.json', k)


# ── TEIL B: geo_pin.json ────────────────────────────────────────────────────
print('\n── geo_pin.json ──')
gp = load('geo_pin.json')

def ext_pin(lst, new_items):
    seen_n = {it['n'] for it in lst}
    seen_c = {(round(it['lat'],3), round(it['lng'],3)) for it in lst}
    for it in new_items:
        coord = (round(it['lat'],3), round(it['lng'],3))
        if it['n'] not in seen_n and coord not in seen_c:
            lst.append(it); seen_n.add(it['n']); seen_c.add(coord)

# geo_geysire 8 → 30
gp['geo_geysire']['items'] += []
ext_pin(gp['geo_geysire']['items'], [
    {'n':'Strokkur (Island)','lat':64.31,'lng':-20.3},
    {'n':'Grand Geyser (Yellowstone)','lat':44.53,'lng':-110.83},
    {'n':'Castle Geyser (Yellowstone)','lat':44.46,'lng':-110.84},
    {'n':'Daisy Geyser (Yellowstone)','lat':44.47,'lng':-110.84},
    {'n':'Pohutu Geyser (Rotorua, NZ)','lat':-38.14,'lng':176.37},
    {'n':'Lady Knox Geyser (Rotorua, NZ)','lat':-38.2,'lng':176.32},
    {'n':'El Tatio (Chile)','lat':-22.33,'lng':-68.0},
    {'n':'Geysir Wairakei (NZ)','lat':-38.63,'lng':176.09},
    {'n':'Norris Geyser Basin (Yellowstone)','lat':44.73,'lng':-110.71},
    {'n':'Fly Geyser (Nevada)','lat':40.86,'lng':-119.32},
    {'n':'Geiser de la Dormida (Chile)','lat':-30.42,'lng':-70.7},
    {'n':'Geyser Valley (Kamtschatka)','lat':54.45,'lng':160.1},
    {'n':'Soda Springs (Idaho, USA)','lat':42.66,'lng':-111.6},
    {'n':'Beowawe Geysers (Nevada)','lat':40.58,'lng':-116.75},
    {'n':'Hveradalir (Island)','lat':64.63,'lng':-19.57},
    {'n':'Dallol (Äthiopien)','lat':14.24,'lng':40.3},
    {'n':'Steamboat Geyser (Yellowstone)','lat':44.73,'lng':-110.71},
    {'n':'Champagne Pool (NZ)','lat':-38.37,'lng':176.37},
    {'n':'Old Faithful (Yellowstone)','lat':44.46,'lng':-110.83},
    {'n':'Velikan Geyser (Kamtschatka)','lat':54.44,'lng':160.12},
    {'n':'Crystal Geyser (Utah)','lat':38.95,'lng':-110.12},
    {'n':'Umnak Geothermal (Alaska)','lat':53.28,'lng':-168.25},
])
print(f"  geo_geysire: {len(gp['geo_geysire']['items'])} items")

# geo_geothermal 8 → 30
ext_pin(gp['geo_geothermal']['items'], [
    {'n':'Larderello (Italien)','lat':43.24,'lng':10.87},
    {'n':'Cerro Prieto (Mexiko)','lat':32.42,'lng':-115.3},
    {'n':'Salton Sea (USA)','lat':33.19,'lng':-115.63},
    {'n':'Geothermales Feld Svartsengi (Island)','lat':63.88,'lng':-22.43},
    {'n':'Nesjavellir (Island)','lat':64.09,'lng':-21.1},
    {'n':'Hellisheiði (Island)','lat':64.02,'lng':-21.41},
    {'n':'Olkaria (Kenia)','lat':-0.9,'lng':36.29},
    {'n':'Wairakei (Neuseeland)','lat':-38.63,'lng':176.09},
    {'n':'Tiwi Islands Geothermal (Philippinen)','lat':13.45,'lng':123.67},
    {'n':'Makban Geothermal (Philippinen)','lat':14.03,'lng':121.33},
    {'n':'Darajat (Indonesien)','lat':-7.19,'lng':107.71},
    {'n':'Dieng (Indonesien)','lat':-7.2,'lng':109.91},
    {'n':'Sarulla (Indonesien)','lat':2.18,'lng':99.08},
    {'n':'Altınkaya (Türkei)','lat':38.0,'lng':27.5},
    {'n':'Kızıldere (Türkei)','lat':37.85,'lng':28.65},
    {'n':'Imperial Valley (USA)','lat':33.0,'lng':-115.5},
    {'n':'The Geysers (USA, Sonoma)','lat':38.79,'lng':-122.75},
    {'n':'Coso Geothermal (USA)','lat':36.0,'lng':-117.77},
    {'n':'Landsvirkjun Burfell (Island)','lat':64.13,'lng':-20.89},
    {'n':'Rotokawa (Neuseeland)','lat':-38.63,'lng':176.17},
    {'n':'Ngatamariki (Neuseeland)','lat':-38.5,'lng':176.2},
    {'n':'Wayang Windu (Indonesien)','lat':-7.21,'lng':107.63},
])
print(f"  geo_geothermal: {len(gp['geo_geothermal']['items'])} items")

# geo_steilkuesten 8 → 30
ext_pin(gp['geo_steilkuesten']['items'], [
    {'n':'Cliffs of Moher (Irland)','lat':52.97,'lng':-9.43},
    {'n':'White Cliffs of Dover (UK)','lat':51.13,'lng':1.37},
    {'n':'Étretat (Frankreich)','lat':49.71,'lng':0.2},
    {'n':'Preikestolen (Norwegen)','lat':58.99,'lng':6.19},
    {'n':'Trolltunga (Norwegen)','lat':60.12,'lng':6.74},
    {'n':'Kjeragbolten (Norwegen)','lat':59.04,'lng':6.57},
    {'n':'Schär Kap (Norwegen, Nordkap)','lat':71.17,'lng':25.79},
    {'n':'Lofoten Cliffs (Norwegen)','lat':68.1,'lng':13.5},
    {'n':'Cabo Girão (Madeira)','lat':32.66,'lng':-17.17},
    {'n':'Kap der Guten Hoffnung','lat':-34.36,'lng':18.48},
    {'n':'Great Ocean Road Cliffs (Australien)','lat':-39.0,'lng':143.5},
    {'n':'Twelve Apostles (Australien)','lat':-38.67,'lng':143.1},
    {'n':'The Remarkables (NZ, Seekliffs)','lat':-45.04,'lng':168.84},
    {'n':'Napali Coast (Hawaii)','lat':22.2,'lng':-159.61},
    {'n':'Hana Cliffs (Maui)','lat':20.74,'lng':-155.98},
    {'n':'Bunda Cliffs (Australien)','lat':-31.65,'lng':130.05},
    {'n':'Cape Breton Highlands','lat':46.72,'lng':-60.55},
    {'n':'Percé Rock (Kanada)','lat':48.52,'lng':-64.22},
    {'n':'Oregon Coast Cliffs','lat':44.6,'lng':-124.1},
    {'n':'Big Sur Cliffs (Kalifornien)','lat':36.26,'lng':-121.8},
    {'n':'Dyrholaey (Island)','lat':63.4,'lng':-19.13},
    {'n':'Hvalnes (Island)','lat':64.39,'lng':-14.52},
])
print(f"  geo_steilkuesten: {len(gp['geo_steilkuesten']['items'])} items")

save('geo_pin.json', gp)


# ── TEIL C: astro_pin.json ─────────────────────────────────────────────────
print('\n── astro_pin.json ──')
ap = load('astro_pin.json')

# astro_dark_sky 8 → 30
ext_pin(ap['astro_dark_sky']['items'], [
    {'n':'Atacama Desert (Chile)','lat':-24.0,'lng':-70.0},
    {'n':'Mauna Kea (Hawaii)','lat':19.82,'lng':-155.47},
    {'n':'Canary Islands – Teide','lat':28.27,'lng':-16.64},
    {'n':'Namibia – NamibRand Reserve','lat':-25.0,'lng':15.5},
    {'n':'Aoraki Mackenzie (Neuseeland)','lat':-43.75,'lng':170.1},
    {'n':'Cherry Springs SP (Pennsylvania)','lat':41.66,'lng':-77.82},
    {'n':'Galloway Forest Park (Schottland)','lat':55.1,'lng':-4.5},
    {'n':'Kerry (Irland)','lat':51.95,'lng':-9.9},
    {'n':'Exmoor NP (England)','lat':51.15,'lng':-3.65},
    {'n':'Brecon Beacons (Wales)','lat':51.88,'lng':-3.44},
    {'n':'Pic du Midi (Frankreich)','lat':42.94,'lng':0.14},
    {'n':'Haute-Provence (Frankreich)','lat':43.93,'lng':5.71},
    {'n':'Zselic Starry Sky Park (Ungarn)','lat':46.2,'lng':17.85},
    {'n':'Hortobagy NP (Ungarn)','lat':47.6,'lng':21.1},
    {'n':'Westhavelland (Deutschland)','lat':52.75,'lng':12.3},
    {'n':'Rhön Biosphäre (Deutschland)','lat':50.37,'lng':9.93},
    {'n':'Kgalagadi (Botswana)','lat':-26.5,'lng':21.5},
    {'n':'Big Bend NP (Texas)','lat':29.13,'lng':-103.24},
    {'n':'Cosmic Campground (New Mexico)','lat':33.35,'lng':-108.84},
    {'n':'Jasper NP (Kanada)','lat':52.88,'lng':-118.08},
    {'n':'Tenerife (Teide-Observ.)','lat':28.3,'lng':-16.51},
    {'n':'La Palma (Roque de los Muchachos)','lat':28.76,'lng':-17.89},
])
print(f"  astro_dark_sky: {len(ap['astro_dark_sky']['items'])} items")

# astro_weltraumteleskope 8 → 30
ext_pin(ap['astro_weltraumteleskope']['items'], [
    {'n':'Hubble Space Telescope (Orbit ~540km)','lat':28.59,'lng':-80.65},
    {'n':'James Webb ST (Launch: Kennedy SC)','lat':28.59,'lng':-80.65},
    {'n':'Chandra X-Ray (Launch: KSC)','lat':28.59,'lng':-80.65},
    {'n':'Spitzer Space Telescope','lat':28.59,'lng':-80.65},
    {'n':'Kepler Space Telescope','lat':28.59,'lng':-80.65},
    {'n':'TESS (Transiting Exoplanet Survey)','lat':28.59,'lng':-80.65},
    {'n':'Fermi Gamma-ray Telescope','lat':28.59,'lng':-80.65},
    {'n':'XMM-Newton (ESA)','lat':5.24,'lng':-52.77},
    {'n':'Herschel Space Observatory (ESA)','lat':5.24,'lng':-52.77},
    {'n':'Planck Observatory (ESA)','lat':5.24,'lng':-52.77},
    {'n':'Euclid (ESA, 2023)','lat':5.24,'lng':-52.77},
    {'n':'Very Large Array (VLA, New Mexico)','lat':34.08,'lng':-107.62},
    {'n':'Atacama Large MM Array (ALMA)','lat':-23.02,'lng':-67.75},
    {'n':'Arecibo Observatory (ehem.)','lat':18.34,'lng':-66.75},
    {'n':'FAST (China, Guizhou)','lat':25.65,'lng':106.86},
    {'n':'Effelsberg (Deutschland)','lat':50.53,'lng':6.88},
    {'n':'Green Bank Telescope (WV)','lat':38.43,'lng':-79.84},
    {'n':'European Southern Observatory – La Silla','lat':-29.26,'lng':-70.73},
    {'n':'ESO Paranal (Chile)','lat':-24.63,'lng':-70.4},
    {'n':'Keck Observatory (Hawaii)','lat':19.83,'lng':-155.47},
    {'n':'Subaru Telescope (Hawaii)','lat':19.83,'lng':-155.48},
    {'n':'Thirty Meter Telescope (geplant, Hawaii)','lat':19.82,'lng':-155.47},
])
print(f"  astro_weltraumteleskope: {len(ap['astro_weltraumteleskope']['items'])} items")

save('astro_pin.json', ap)


# ── TEIL D: sport_pin.json ─────────────────────────────────────────────────
print('\n── sport_pin.json ──')
sp = load('sport_pin.json')

# sport_klettergebiete 8 → 30
ext_pin(sp['sport_klettergebiete']['items'], [
    {'n':'El Capitan (Yosemite)','lat':37.73,'lng':-119.64},
    {'n':'Fontainebleau (Frankreich)','lat':48.39,'lng':2.69},
    {'n':'Kalymnos (Griechenland)','lat':36.94,'lng':26.99},
    {'n':'Magic Wood (Schweiz)','lat':46.5,'lng':9.25},
    {'n':'Ceüse (Frankreich)','lat':44.39,'lng':5.92},
    {'n':'Leonidio (Griechenland)','lat':37.15,'lng':22.87},
    {'n':'Railay Beach (Thailand)','lat':8.01,'lng':98.84},
    {'n':'Wadi Rum (Jordanien)','lat':29.57,'lng':35.44},
    {'n':'Rjukan (Norwegen, Eiskletter)','lat':59.88,'lng':8.6},
    {'n':'Dolomiten (Italien)','lat':46.41,'lng':11.86},
    {'n':'Bishop (Kalifornien, Bouldering)','lat':37.36,'lng':-118.39},
    {'n':'Joshua Tree NP (Kalifornien)','lat':34.13,'lng':-116.31},
    {'n':'Red River Gorge (Kentucky)','lat':37.77,'lng':-83.69},
    {'n':'Yosemite Valley Walls','lat':37.74,'lng':-119.57},
    {'n':'Smith Rock (Oregon)','lat':44.37,'lng':-121.14},
    {'n':'New River Gorge (West Virginia)','lat':38.07,'lng':-81.08},
    {'n':'Göschenen-Schlucht (Schweiz)','lat':46.67,'lng':8.59},
    {'n':'Maltatal (Österreich)','lat':47.05,'lng':13.5},
    {'n':'Frankenjura (Deutschland)','lat':49.55,'lng':11.5},
    {'n':'Zillertal (Österreich)','lat':47.2,'lng':11.87},
    {'n':'Tonsai Beach (Thailand)','lat':8.0,'lng':98.82},
    {'n':'Gorges du Verdon (Frankreich)','lat':43.73,'lng':6.36},
])
print(f"  sport_klettergebiete: {len(sp['sport_klettergebiete']['items'])} items")

# sport_ski_pisten 8 → 30
ext_pin(sp['sport_ski_pisten']['items'], [
    {'n':'Chamonix (Mont Blanc)','lat':45.92,'lng':6.87},
    {'n':'Zermatt','lat':46.02,'lng':7.75},
    {'n':'St. Anton am Arlberg','lat':47.13,'lng':10.27},
    {'n':'Verbier','lat':46.1,'lng':7.23},
    {'n':'Courchevel','lat':45.42,'lng':6.63},
    {'n':'Val d\'Isère','lat':45.45,'lng':6.98},
    {'n':'Megève','lat':45.86,'lng':6.62},
    {'n':'Kitzbühel','lat':47.44,'lng':12.39},
    {'n':'Davos','lat':46.8,'lng':9.83},
    {'n':'St. Moritz','lat':46.5,'lng':9.84},
    {'n':'Whistler Blackcomb (Kanada)','lat':50.12,'lng':-122.95},
    {'n':'Vail (Colorado)','lat':39.64,'lng':-106.37},
    {'n':'Aspen Snowmass','lat':39.2,'lng':-106.82},
    {'n':'Park City (Utah)','lat':40.65,'lng':-111.5},
    {'n':'Niseko (Japan)','lat':42.8,'lng':140.69},
    {'n':'Hakuba (Japan)','lat':36.7,'lng':137.86},
    {'n':'Thredbo (Australien)','lat':-36.5,'lng':148.31},
    {'n':'Queenstown (Neuseeland)','lat':-45.03,'lng':168.66},
    {'n':'Pyeongchang (Südkorea)','lat':37.37,'lng':128.39},
    {'n':'Rosa Khutor (Russland, Sotschi)','lat':43.67,'lng':40.3},
    {'n':'Cortina d\'Ampezzo (Italien)','lat':46.54,'lng':12.14},
    {'n':'Sölden (Österreich)','lat':46.96,'lng':11.0},
])
print(f"  sport_ski_pisten: {len(sp['sport_ski_pisten']['items'])} items")

save('sport_pin.json', sp)

print('\n══ patch_269_echter_fill.py — Done ══')
