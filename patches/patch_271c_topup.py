#!/usr/bin/env python3
"""patch_271c_topup.py — third-pass fill for remaining 67 arrays under 50"""
import json, os

DATA = '/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/data'

def load(fname):
    with open(os.path.join(DATA, fname), encoding='utf-8') as f:
        return json.load(f)

def save(fname, d):
    with open(os.path.join(DATA, fname), 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def thl(d, k, items):
    ex = {x['name'] for x in d[k]['items']}
    add = [x for x in items if x['name'] not in ex]
    needed = max(0, 50 - len(d[k]['items']))
    d[k]['items'].extend(add[:max(needed, len(add))])

def tnc(d, k, items):
    ex = {x['n'] for x in d[k]['items']}
    add = [x for x in items if x['n'] not in ex]
    needed = max(0, 50 - len(d[k]['items']))
    d[k]['items'].extend(add[:max(needed, len(add))])

def tp(d, k, items):
    ex = {x['n'] for x in d[k]['items']}
    add = [x for x in items if x['n'] not in ex]
    needed = max(0, 50 - len(d[k]['items']))
    d[k]['items'].extend(add[:max(needed, len(add))])

# ── archaeologie_pin ─────────────────────────────────
print("archaeologie_pin.json")
d = load('archaeologie_pin.json')
tp(d,'hoehlenmalerien',[
    {"n":"Altamira-Höhle (Kantabrien, Spanien)","lat":43.38,"lng":-4.12},
])
for k in d: print(f"  {k}: {len(d[k]['items'])}")
save('archaeologie_pin.json', d)

# ── astro_hl ─────────────────────────────────────────
print("astro_hl.json")
d = load('astro_hl.json')
thl(d,'astro_monde_anzahl',[
    {"name":"Uranus","val":28},
    {"name":"Neptun","val":16},
    {"name":"Mars","val":2},
    {"name":"Erde","val":1},
    {"name":"Pluto","val":5},
    {"name":"Eris","val":1},
    {"name":"Haumea","val":2},
])
thl(d,'astro_schwerkraft',[
    {"name":"Merkur","val":3.7},
    {"name":"Venus","val":8.87},
    {"name":"Erde","val":9.81},
    {"name":"Mars","val":3.71},
    {"name":"Uranus","val":8.69},
    {"name":"Neptun","val":11.15},
    {"name":"Pluto","val":0.62},
    {"name":"Mond","val":1.62},
])
thl(d,'astro_sonnenentfernung',[
    {"name":"Eris (Zwergplanet)","val":10120},
    {"name":"Sedna (Zwergplanet)","val":84000},
    {"name":"Makemake (Zwergplanet)","val":6800},
    {"name":"Haumea (Zwergplanet)","val":6450},
])
thl(d,'astro_entdeckungsjahr',[
    {"name":"Pluto (Clyde Tombaugh)","val":1930},
    {"name":"Eris (Brown/Trujillo/Rabinowitz)","val":2005},
    {"name":"Haumea (Brown et al.)","val":2004},
    {"name":"Makemake (Brown/Trujillo/Rabinowitz)","val":2005},
])
thl(d,'astro_temperaturen',[
    {"name":"Merkur (Tag)","val":430},
])
thl(d,'astro_exoplaneten_distanz',[
    {"name":"Tau Ceti e","val":11.9},
])
for k in d: print(f"  {k}: {len(d[k]['items'])}")
save('astro_hl.json', d)

# ── astro_match ──────────────────────────────────────
print("astro_match.json")
d = load('astro_match.json')
tnc(d,'astro_kosmologie',[
    {"n":"Gamma-Strahlen-Burst","c":"Hellste elektromagnetische Explosion im Universum"},
    {"n":"Magnetar","c":"Extrem starkes magnetisches Neutronenstern-Objekt"},
])
tnc(d,'astro_sonden_ziele',[
    {"n":"Cassini-Huygens (NASA/ESA)","c":"Saturn"},
])
tnc(d,'astro_pioniere',[
    {"n":"Johannes Kepler","c":"Planetenbewegungsgesetze"},
    {"n":"Edwin Hubble","c":"Nachweis extragalaktischer Nebel"},
    {"n":"Carl Sagan","c":"Popularisierung der Astronomie"},
    {"n":"Neil Armstrong","c":"Erster Mensch auf dem Mond"},
    {"n":"Vera Rubin","c":"Nachweis dunkler Materie durch Galaxienrotation"},
])
tnc(d,'astro_galaxien_typen',[
    {"n":"NGC 1300 (Virgo-Supercluster)","c":"Balkenspiralgalaxie"},
    {"n":"Sombrero-Galaxie (M104)","c":"Spiralgalaxie (edge-on)"},
    {"n":"Sculptor-Galaxie (NGC 253)","c":"Spiralgalaxie"},
    {"n":"Ursa-Major-Zwerggalaxie","c":"Zwerggalaxie"},
])
for k in d: print(f"  {k}: {len(d[k]['items'])}")
save('astro_match.json', d)

# ── astro_pin ─────────────────────────────────────────
print("astro_pin.json")
d = load('astro_pin.json')
tp(d,'astro_startrampen',[
    {"n":"Jiuquan Satellite Launch Center (China)","lat":40.96,"lng":100.29},
])
tp(d,'astro_meteoritenkrater',[
    {"n":"Barringer-Krater (Arizona, USA)","lat":35.03,"lng":-111.02},
])
for k in d: print(f"  {k}: {len(d[k]['items'])}")
save('astro_pin.json', d)

# ── gastro_hl ─────────────────────────────────────────
print("gastro_hl.json")
d = load('gastro_hl.json')
thl(d,'wasseranteil',[
    {"name":"Wassermelone","val":92.0},
    {"name":"Sellerie","val":95.4},
])
for k in d: print(f"  {k}: {len(d[k]['items'])}")
save('gastro_hl.json', d)

# ── gastro_match ─────────────────────────────────────
print("gastro_match.json")
d = load('gastro_match.json')
tnc(d,'bakterien_pilze',[
    {"n":"Aspergillus oryzae","c":"Miso & Sake"},
    {"n":"Saccharomyces cerevisiae","c":"Bier & Brot"},
    {"n":"Penicillium camemberti","c":"Camembert"},
    {"n":"Acetobacter aceti","c":"Essig"},
])
tnc(d,'exotische_fruechte',[
    {"n":"Salak (Schlangenfrucht)","c":"Indonesien"},
])
tnc(d,'fruehstueck_welt',[
    {"n":"Nasi Lemak","c":"Malaysia"},
    {"n":"Shakshuka","c":"Nordafrika / Israel"},
    {"n":"Huevos Rancheros","c":"Mexiko"},
])
tnc(d,'kaffeespezialitaeten',[
    {"n":"Affogato","c":"Espresso"},
])
for k in d: print(f"  {k}: {len(d[k]['items'])}")
save('gastro_match.json', d)

# ── geo_hl ────────────────────────────────────────────
print("geo_hl.json")
d = load('geo_hl.json')
thl(d,'geo_berghoehen',[
    {"name":"Kangchenjunga (Indien/Nepal)","val":8586},
    {"name":"Lhotse (Nepal/China)","val":8516},
    {"name":"Makalu (Nepal/China)","val":8485},
])
thl(d,'geo_vulkan_hoehen',[
    {"name":"Pico de Orizaba (Mexiko)","val":5636},
    {"name":"Popocatépetl (Mexiko)","val":5426},
    {"name":"Nevado del Ruiz (Kolumbien)","val":5321},
])
thl(d,'geo_kontinentaldrift',[
    {"name":"Arabische Platte","val":21},
    {"name":"Afrikanische Platte","val":21},
    {"name":"Australische Platte","val":70},
    {"name":"Nazca-Platte","val":79},
])
thl(d,'geo_vei_ausbruch',[
    {"name":"Pinatubo 1991 (Philippinen)","val":6},
])
thl(d,'geo_gletscher_volumen',[
    {"name":"Grönländisches Eisschild","val":2850000},
])
for k in d: print(f"  {k}: {len(d[k]['items'])}")
save('geo_hl.json', d)

# ── geo_match ─────────────────────────────────────────
print("geo_match.json")
d = load('geo_match.json')
tnc(d,'geo_gesteinsarten',[
    {"n":"Obsidian","c":"Magmatisch"},
    {"n":"Diorit","c":"Magmatisch"},
    {"n":"Andesit","c":"Magmatisch"},
    {"n":"Gneiss","c":"Metamorph"},
    {"n":"Quarzit","c":"Metamorph"},
    {"n":"Konglomerat","c":"Sedimentär"},
])
tnc(d,'geo_tektonik',[
    {"n":"Island","c":"Eurasische & Nordamerikanische Platte"},
    {"n":"Ostafrika","c":"Afrikanische Platte (Ostafrikanischer Graben)"},
    {"n":"Türkei","c":"Eurasische Platte"},
])
tnc(d,'geo_fossil_zeitalter',[
    {"n":"Ichthyosaurus","c":"Mesozoikum"},
])
tnc(d,'geo_erdbeben_jahr',[
    {"n":"Haitian-Erdbeben (Haiti)","c":"2010"},
])
tnc(d,'geo_gestein_nutzung',[
    {"n":"Bimsstein","c":"Schleifmittel & Leichtbeton"},
])
tnc(d,'geo_kontinent_platte',[
    {"n":"Australien","c":"Australische Platte"},
])
tnc(d,'geo_mineral_kristall',[
    {"n":"Schwefel","c":"Orthorhombisch"},
])
for k in d: print(f"  {k}: {len(d[k]['items'])}")
save('geo_match.json', d)

# ── pflanzen_hl ───────────────────────────────────────
print("pflanzen_hl.json")
d = load('pflanzen_hl.json')
thl(d,'kaffeeproduktion',[
    {"name":"Peru","val":380},
    {"name":"Guatemala","val":280},
    {"name":"Mexiko","val":234},
    {"name":"Uganda","val":370},
    {"name":"Tansania","val":108},
    {"name":"Dominikanische Republik","val":45},
    {"name":"Bolivien","val":22},
    {"name":"Ruanda","val":75},
    {"name":"Burundi","val":35},
])
thl(d,'weinproduktion',[
    {"name":"Portugal","val":762},
    {"name":"Rumänien","val":395},
    {"name":"Ungarn","val":346},
    {"name":"Österreich","val":259},
])
thl(d,'reisproduktion',[
    {"name":"Myanmar","val":25.7},
    {"name":"Philippinen","val":19.8},
    {"name":"Kambodscha","val":11.4},
    {"name":"Laos","val":4.1},
])
thl(d,'waldflaeche',[
    {"name":"Gabun","val":89.0},
    {"name":"Salomonen","val":78.0},
])
for k in d: print(f"  {k}: {len(d[k]['items'])}")
save('pflanzen_hl.json', d)

# ── pflanzen_match ────────────────────────────────────
print("pflanzen_match.json")
d = load('pflanzen_match.json')
tnc(d,'bestuaeber',[
    {"n":"Passionsblume","c":"Bienen"},
])
tnc(d,'familien',[
    {"n":"Lärche","c":"Pinaceae"},
    {"n":"Orchidee","c":"Orchidaceae"},
])
tnc(d,'herkunft',[
    {"n":"Kakao","c":"Mittel-/Südamerika"},
    {"n":"Mango","c":"Südasien"},
])
for k in d: print(f"  {k}: {len(d[k]['items'])}")
save('pflanzen_match.json', d)

# ── pflanzen_pin ──────────────────────────────────────
print("pflanzen_pin.json")
d = load('pflanzen_pin.json')
tp(d,'tropenwald',[
    {"n":"Tongass-Regenwald (Alaska, USA)","lat":57.0,"lng":-133.0},
])
for k in d: print(f"  {k}: {len(d[k]['items'])}")
save('pflanzen_pin.json', d)

# ── sport_hl ──────────────────────────────────────────
print("sport_hl.json")
d = load('sport_hl.json')
thl(d,'sport_olympia_goldmedaillen',[
    {"name":"Larisa Latynina (Turnen, UdSSR)","val":9},
    {"name":"Paavo Nurmi (Leichtathletik, Finnland)","val":9},
    {"name":"Mark Spitz (Schwimmen, USA)","val":9},
    {"name":"Carl Lewis (Leichtathletik, USA)","val":9},
    {"name":"Bjørn Dæhlie (Ski, Norwegen)","val":8},
    {"name":"Birgit Fischer (Kanu, DDR/Deutschland)","val":8},
])
thl(d,'sport_marathon_alter',[
    {"name":"Tokyo Marathon (Japan)","val":2007},
    {"name":"Mumbai Marathon (Indien)","val":2004},
    {"name":"Athen-Marathon (Griechenland)","val":1896},
])
thl(d,'sport_fussball_marktwert',[
    {"name":"Erling Haaland (Hoechstwert ca. 2023)","val":180},
    {"name":"Jude Bellingham (Hoechstwert ca. 2024)","val":180},
])
for k in d: print(f"  {k}: {len(d[k]['items'])}")
save('sport_hl.json', d)

# ── sport_match ───────────────────────────────────────
print("sport_match.json")
d = load('sport_match.json')
tnc(d,'sport_olympisch',[
    {"n":"Skateboarden","c":"Ja"},
    {"n":"Klettern","c":"Ja"},
    {"n":"Karate","c":"Nein (nach Tokio 2020 gestrichen)"},
    {"n":"Schach","c":"Nein"},
    {"n":"Softball","c":"Ja"},
    {"n":"Lacrosse","c":"Ja (ab LA 2028)"},
])
tnc(d,'sport_nationalsport_match',[
    {"n":"Sumo","c":"Japan"},
    {"n":"Eishockey","c":"Kanada"},
    {"n":"Polo","c":"Argentinien"},
    {"n":"Hurling","c":"Irland"},
    {"n":"Kabaddi","c":"Bangladesch"},
    {"n":"Sepak Takraw","c":"Thailand"},
    {"n":"Bandy","c":"Russland"},
])
tnc(d,'sport_sportart_kontinent',[
    {"n":"Australian Football","c":"Ozeanien"},
    {"n":"Lacrosse","c":"Nordamerika"},
    {"n":"Pelota Vasca","c":"Europa"},
])
tnc(d,'sport_teamgroesse',[
    {"n":"Polo","c":"4 Spieler"},
    {"n":"Baseball","c":"9 Spieler"},
    {"n":"Softball","c":"9 Spieler"},
])
for k in d: print(f"  {k}: {len(d[k]['items'])}")
save('sport_match.json', d)

# ── sport_pin ─────────────────────────────────────────
print("sport_pin.json")
d = load('sport_pin.json')
tp(d,'sport_fussballstadien',[
    {"n":"Fisht Stadium (Sotschi, Russland)","lat":43.41,"lng":39.96},
])
tp(d,'sport_motorsport_strecken',[
    {"n":"Circuit of the Americas (Austin, USA)","lat":30.13,"lng":-97.64},
    {"n":"Hungaroring (Budapest, Ungarn)","lat":47.58,"lng":19.25},
])
for k in d: print(f"  {k}: {len(d[k]['items'])}")
save('sport_pin.json', d)

# ── tech_hl ───────────────────────────────────────────
print("tech_hl.json")
d = load('tech_hl.json')
thl(d,'internet_speed',[
    {"name":"Hongkong","val":248},
    {"name":"Dänemark","val":213},
    {"name":"Luxemburg","val":208},
    {"name":"Schweiz","val":200},
    {"name":"Chile","val":192},
    {"name":"Niederlande","val":185},
    {"name":"Schweden","val":175},
    {"name":"Belgien","val":163},
    {"name":"Österreich","val":148},
    {"name":"Japan","val":185},
])
thl(d,'release_jahr',[
    {"name":"Ruby","val":1995},
    {"name":"JavaScript","val":1995},
    {"name":"PHP","val":1994},
])
thl(d,'transistoren',[
    {"name":"Apple M1 Pro","val":33600},
    {"name":"Intel Core i9-14900K","val":22000},
])
for k in d: print(f"  {k}: {len(d[k]['items'])}")
save('tech_hl.json', d)

# ── tech_match ────────────────────────────────────────
print("tech_match.json")
d = load('tech_match.json')
tnc(d,'akronyme',[
    {"n":"GUI","c":"Graphical User Interface"},
    {"n":"ORM","c":"Object-Relational Mapping"},
])
tnc(d,'bigo',[
    {"n":"Tiefensuche (DFS)","c":"O(V+E)"},
    {"n":"Dijkstra (binärer Heap)","c":"O((V+E) log V)"},
])
tnc(d,'dateiendungen',[
    {"n":".svg","c":"Vektorgrafik"},
])
tnc(d,'erfinder',[
    {"n":"UNIX","c":"Ken Thompson & Dennis Ritchie"},
])
tnc(d,'http',[
    {"n":"301 Moved Permanently","c":"3xx Weiterleitung"},
    {"n":"502 Bad Gateway","c":"5xx Serverfehler"},
    {"n":"451 Unavailable For Legal Reasons","c":"4xx Client-Fehler"},
    {"n":"100 Continue","c":"1xx Informativ"},
    {"n":"304 Not Modified","c":"3xx Weiterleitung"},
])
tnc(d,'osi',[
    {"n":"SSL/TLS","c":"6 Darstellung"},
])
tnc(d,'portnummern',[
    {"n":"Port 110","c":"POP3"},
    {"n":"Port 143","c":"IMAP"},
    {"n":"Port 8080","c":"HTTP Alternativ"},
    {"n":"Port 3306","c":"MySQL"},
    {"n":"Port 5432","c":"PostgreSQL"},
    {"n":"Port 27017","c":"MongoDB"},
    {"n":"Port 6379","c":"Redis"},
    {"n":"Port 9200","c":"Elasticsearch"},
])
tnc(d,'tech_ma',[
    {"n":"Instagram","c":"Facebook (Meta)"},
    {"n":"WhatsApp","c":"Facebook (Meta)"},
    {"n":"Oculus VR","c":"Facebook (Meta)"},
    {"n":"Twitch","c":"Amazon"},
])
tnc(d,'turing_award',[
    {"n":"Vinton Cerf & Robert Kahn","c":"TCP/IP-Protokoll (2004)"},
    {"n":"Geoffrey Hinton","c":"Deep Learning (2018)"},
])
for k in d: print(f"  {k}: {len(d[k]['items'])}")
save('tech_match.json', d)

# ── tech_pin ──────────────────────────────────────────
print("tech_pin.json")
d = load('tech_pin.json')
tp(d,'halbleiter',[
    {"n":"Intel Fab D1X (Hillsboro, Oregon, USA)","lat":45.53,"lng":-122.99},
    {"n":"Infineon Dresden Fab (Deutschland)","lat":51.05,"lng":13.74},
])
tp(d,'programmiersprachen',[
    {"n":"Ruby (Kyoto, Japan)","lat":35.01,"lng":135.77},
    {"n":"C++ (Bell Labs, Murray Hill, USA)","lat":40.69,"lng":-74.4},
])
tp(d,'supercomputer',[
    {"n":"El Capitan (Lawrence Livermore Lab, Kalifornien)","lat":37.69,"lng":-121.7},
])
tp(d,'tech_museen',[
    {"n":"Heinz Nixdorf MuseumsForum (Paderborn, Deutschland)","lat":51.72,"lng":8.75},
])
for k in d: print(f"  {k}: {len(d[k]['items'])}")
save('tech_pin.json', d)

# ── tiere_hl ──────────────────────────────────────────
print("tiere_hl.json")
d = load('tiere_hl.json')
thl(d,'pferde_gewicht',[
    {"name":"Clydesdale","val":900},
    {"name":"Percheron","val":950},
    {"name":"Haflinger","val":550},
    {"name":"Tinker","val":650},
    {"name":"Shetland-Pony","val":200},
])
thl(d,'pferde_stockmass',[
    {"name":"Lusitano","val":158},
    {"name":"Trakehner","val":165},
])
thl(d,'speed_land',[
    {"name":"Strauß","val":70},
])
thl(d,'traechtigkeit',[
    {"name":"Nashornvogel","val":40},
])
for k in d: print(f"  {k}: {len(d[k]['items'])}")
save('tiere_hl.json', d)

print("\nAll done.")
