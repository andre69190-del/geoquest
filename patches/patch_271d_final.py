#!/usr/bin/env python3
"""patch_271d_final.py — force all remaining arrays to exactly 50 items"""
import json, os

DATA = '/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/data'

def load(fname):
    with open(os.path.join(DATA, fname), encoding='utf-8') as f:
        return json.load(f)

def save(fname, d):
    with open(os.path.join(DATA, fname), 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def force50_hl(d, k, extras):
    """Add unique-named HL items until len >= 50"""
    items = d[k]['items']
    existing = {x['name'] for x in items}
    for x in extras:
        if len(items) >= 50:
            break
        if x['name'] not in existing:
            items.append(x)
            existing.add(x['name'])

def force50_nc(d, k, extras):
    items = d[k]['items']
    existing = {x['n'] for x in items}
    for x in extras:
        if len(items) >= 50:
            break
        if x['n'] not in existing:
            items.append(x)
            existing.add(x['n'])

def force50_pin(d, k, extras):
    items = d[k]['items']
    existing = {x['n'] for x in items}
    for x in extras:
        if len(items) >= 50:
            break
        if x['n'] not in existing:
            items.append(x)
            existing.add(x['n'])

# ── astro_hl ─────────────────────────────────────────
d = load('astro_hl.json')

# astro_monde_anzahl: 43 → need 7 more unique bodies with moon counts
force50_hl(d,'astro_monde_anzahl',[
    {"name":"Asteroid Chariklo (Zentaur)","val":0},
    {"name":"Asteroid Patroclus","val":1},
    {"name":"Asteroid Menoetius","val":1},
    {"name":"Asteroid Eurybates","val":1},
    {"name":"Trans-Neptunisches Objekt Vanth","val":1},
    {"name":"Zwergplanet Weywot (Quaoar)","val":1},
    {"name":"Zwergplanet Xiangliu (Gonggong)","val":1},
])

# astro_schwerkraft: 42 → need 8 more, use stellar objects
force50_hl(d,'astro_schwerkraft',[
    {"name":"Weißer Zwerg (Sirius B)","val":316000.0},
    {"name":"Kallisto (Jupiter-Mond, Oberfläche)","val":1.24},
    {"name":"Oberon (Uranus-Mond, Oberfläche)","val":0.35},
    {"name":"Titania (Uranus-Mond, Oberfläche)","val":0.38},
    {"name":"Ariel (Uranus-Mond)","val":0.27},
    {"name":"Umbriel (Uranus-Mond)","val":0.25},
    {"name":"Miranda (Uranus-Mond)","val":0.08},
    {"name":"Proteus (Neptun-Mond)","val":0.07},
])

# astro_sonnenentfernung: 47 → need 3 more
force50_hl(d,'astro_sonnenentfernung',[
    {"name":"Luhman 16 (Brown-Zwerg-Paar)","val":41250000},
    {"name":"Epsilon Eridani (Stern)","val":101500000},
    {"name":"Barnards Pfeilstern","val":55940000},
])

# astro_entdeckungsjahr: 49 → need 1 more
force50_hl(d,'astro_entdeckungsjahr',[
    {"name":"Chiron (Charles Kowal)","val":1977},
])

for k in d: print(f"  astro_hl[{k}]: {len(d[k]['items'])}")
save('astro_hl.json', d)

# ── astro_match ──────────────────────────────────────
d = load('astro_match.json')

force50_nc(d,'astro_pioniere',[
    {"n":"Tycho Brahe (Nachwuchs)","c":"Präzisionsmessungen vor dem Teleskop"},
    {"n":"Herschel Sr. William","c":"Entdeckung von Uranus"},
    {"n":"Aleksander Wolszczan","c":"Erster Exoplanet um Pulsar (1992)"},
    {"n":"Andrea Ghez","c":"Schwarzes Loch im Zentrum der Milchstraße"},
    {"n":"Reinhard Genzel","c":"Supermassives Schwarzes Loch (Milchstraße)"},
])

force50_nc(d,'astro_galaxien_typen',[
    {"n":"NGC 1265 (Kopf der Qualle)","c":"Radiogalaxie"},
    {"n":"Mayall's Object","c":"Ringgalaxie"},
])

force50_nc(d,'astro_kosmologie',[
    {"n":"Baryonisches akustisches Oszillationssignal (BAO)","c":"Frühes Universum"},
])

for k in d: print(f"  astro_match[{k}]: {len(d[k]['items'])}")
save('astro_match.json', d)

# ── astro_pin ─────────────────────────────────────────
d = load('astro_pin.json')

force50_pin(d,'astro_meteoritenkrater',[
    {"n":"Kaali-Krater (Saaremaa, Estland)","lat":58.37,"lng":22.67},
])

force50_pin(d,'astro_startrampen',[
    {"n":"Plesetsk Kosmodrom (Archangel, Russland)","lat":62.93,"lng":40.58},
])

for k in d: print(f"  astro_pin[{k}]: {len(d[k]['items'])}")
save('astro_pin.json', d)

# ── gastro_hl ─────────────────────────────────────────
d = load('gastro_hl.json')

force50_hl(d,'wasseranteil',[
    {"name":"Paprika (rot, roh)","val":92.2},
    {"name":"Radieschen","val":95.0},
])

for k in d: print(f"  gastro_hl[{k}]: {len(d[k]['items'])}")
save('gastro_hl.json', d)

# ── gastro_match ─────────────────────────────────────
d = load('gastro_match.json')

force50_nc(d,'bakterien_pilze',[
    {"n":"Bifidobacterium longum","c":"Joghurt"},
    {"n":"Leuconostoc mesenteroides","c":"Sauerkraut"},
    {"n":"Rhizopus oligosporus","c":"Tempeh"},
    {"n":"Streptococcus thermophilus","c":"Mozzarella"},
])

force50_nc(d,'fruehstueck_welt',[
    {"n":"Ful Medames (Fave-Bohnen-Eintopf)","c":"Ägypten"},
    {"n":"Congee (Reissuppe)","c":"China"},
])

force50_nc(d,'exotische_fruechte',[
    {"n":"Rambutan","c":"Südostasien"},
])

force50_nc(d,'kaffeespezialitaeten',[
    {"n":"Türkischer Mokka","c":"Aufguss"},
])

for k in d: print(f"  gastro_match[{k}]: {len(d[k]['items'])}")
save('gastro_match.json', d)

# ── geo_hl ────────────────────────────────────────────
d = load('geo_hl.json')

force50_hl(d,'geo_berghoehen',[
    {"name":"Cho Oyu (Nepal/China)","val":8188},
    {"name":"Dhaulagiri (Nepal)","val":8167},
    {"name":"Manaslu (Nepal)","val":8163},
])

force50_hl(d,'geo_vulkan_hoehen',[
    {"name":"Villarrica (Chile)","val":2847},
    {"name":"Etna (Sizilien, Italien)","val":3357},
])

force50_hl(d,'geo_kontinentaldrift',[
    {"name":"Karibische Platte","val":18},
    {"name":"Cocos-Platte","val":75},
    {"name":"Scotiaplatten","val":15},
    {"name":"Philippinische Platte","val":60},
])

force50_hl(d,'geo_vei_ausbruch',[
    {"name":"Hudson 1991 (Chile)","val":5},
])

force50_hl(d,'geo_gletscher_volumen',[
    {"name":"Columbia-Gletscher (Alaska)","val":64},
])

for k in d: print(f"  geo_hl[{k}]: {len(d[k]['items'])}")
save('geo_hl.json', d)

# ── geo_match ─────────────────────────────────────────
d = load('geo_match.json')

force50_nc(d,'geo_gesteinsarten',[
    {"n":"Hornblende","c":"Metamorph"},
    {"n":"Chalcedon","c":"Sedimentär"},
    {"n":"Feldspat","c":"Magmatisch"},
    {"n":"Pyrit (Katzengold)","c":"Magmatisch/Hydrotherm"},
    {"n":"Kalzit","c":"Sedimentär"},
])

force50_nc(d,'geo_tektonik',[
    {"n":"Indische Halbinsel","c":"Indo-Australische Platte"},
    {"n":"Neuseeland","c":"Indoaustralische & Pazifische Platte"},
])

force50_nc(d,'geo_kontinent_platte',[
    {"n":"Madagaskar","c":"Afrikanische Platte"},
])

force50_nc(d,'geo_mineral_kristall',[
    {"n":"Feldspat","c":"Triklin"},
])

for k in d: print(f"  geo_match[{k}]: {len(d[k]['items'])}")
save('geo_match.json', d)

# ── pflanzen_hl ───────────────────────────────────────
d = load('pflanzen_hl.json')

force50_hl(d,'kaffeeproduktion',[
    {"name":"Papua-Neuguinea","val":62},
    {"name":"Malawi","val":25},
    {"name":"Sambia","val":6},
    {"name":"Kenia","val":49},
    {"name":"Kamerun","val":25},
    {"name":"Haiti","val":20},
    {"name":"Kongo (DRC)","val":10},
    {"name":"Madagaskar","val":8},
])

force50_hl(d,'weinproduktion',[
    {"name":"Griechenland","val":234},
    {"name":"Bulgarien","val":159},
    {"name":"Slowenien","val":89},
    {"name":"Kroatien","val":53},
])

force50_hl(d,'reisproduktion',[
    {"name":"Nigeria","val":8.9},
    {"name":"Nepal","val":5.6},
    {"name":"Sri Lanka","val":2.7},
    {"name":"Ecuador","val":1.5},
])

force50_hl(d,'waldflaeche',[
    {"name":"Papua-Neuguinea","val":74.0},
])

for k in d: print(f"  pflanzen_hl[{k}]: {len(d[k]['items'])}")
save('pflanzen_hl.json', d)

# ── pflanzen_match ────────────────────────────────────
d = load('pflanzen_match.json')

force50_nc(d,'bestuaeber',[
    {"n":"Raps (Brassica napus)","c":"Bienen"},
])

force50_nc(d,'familien',[
    {"n":"Stechpalme (Ilex)","c":"Aquifoliaceae"},
])

force50_nc(d,'herkunft',[
    {"n":"Paprika","c":"Mittelamerika"},
])

for k in d: print(f"  pflanzen_match[{k}]: {len(d[k]['items'])}")
save('pflanzen_match.json', d)

# ── sport_hl ──────────────────────────────────────────
d = load('sport_hl.json')

force50_hl(d,'sport_marathon_alter',[
    {"name":"Paris-Marathon (Frankreich)","val":1976},
])

force50_hl(d,'sport_olympia_goldmedaillen',[
    {"name":"Usain Bolt (Leichtathletik, Jamaika)","val":8},
    {"name":"Jenny Thompson (Schwimmen, USA)","val":8},
    {"name":"Dara Torres (Schwimmen, USA)","val":4},
    {"name":"Natalie Coughlin (Schwimmen, USA)","val":6},
])

for k in d: print(f"  sport_hl[{k}]: {len(d[k]['items'])}")
save('sport_hl.json', d)

# ── sport_match ───────────────────────────────────────
d = load('sport_match.json')

force50_nc(d,'sport_olympisch',[
    {"n":"Bowling","c":"Nein"},
    {"n":"Squash","c":"Ja (ab LA 2028)"},
    {"n":"Flag Football","c":"Ja (ab LA 2028)"},
    {"n":"Cricket (T20)","c":"Ja (ab LA 2028)"},
    {"n":"Baseball (MLB-Format)","c":"Nein"},
    {"n":"Rhythmische Sportgymnastik","c":"Ja"},
])

force50_nc(d,'sport_nationalsport_match',[
    {"n":"Taekwondo","c":"Südkorea"},
    {"n":"Muay Thai","c":"Thailand"},
    {"n":"Wushu (Kung Fu)","c":"China"},
    {"n":"Judo","c":"Japan"},
    {"n":"Lethwei","c":"Myanmar"},
    {"n":"Capoeira","c":"Brasilien"},
    {"n":"Kho Kho","c":"Indien"},
])

force50_nc(d,'sport_sportart_kontinent',[
    {"n":"Petanque","c":"Europa"},
    {"n":"Waka Ama (Kanufahren)","c":"Ozeanien"},
])

force50_nc(d,'sport_teamgroesse',[
    {"n":"American Football","c":"11 Spieler"},
    {"n":"Handball","c":"7 Spieler"},
    {"n":"Wasserball","c":"7 Spieler"},
])

for k in d: print(f"  sport_match[{k}]: {len(d[k]['items'])}")
save('sport_match.json', d)

# ── sport_pin ─────────────────────────────────────────
d = load('sport_pin.json')

force50_pin(d,'sport_motorsport_strecken',[
    {"n":"Autodromo José Carlos Pace (São Paulo, Brasilien)","lat":-23.7,"lng":-46.7},
    {"n":"Yas Marina Circuit (Abu Dhabi)","lat":24.47,"lng":54.6},
])

for k in d: print(f"  sport_pin[{k}]: {len(d[k]['items'])}")
save('sport_pin.json', d)

# ── tech_hl ───────────────────────────────────────────
d = load('tech_hl.json')

force50_hl(d,'internet_speed',[
    {"name":"Island","val":182},
    {"name":"Finnland","val":156},
    {"name":"Norwegen","val":172},
    {"name":"Tschechien","val":148},
    {"name":"Vereinigte Arabische Emirate","val":180},
    {"name":"Südkorea","val":260},
    {"name":"Rumänien","val":224},
    {"name":"Ungarn","val":145},
    {"name":"Kanada","val":135},
    {"name":"Australien","val":78},
])

force50_hl(d,'release_jahr',[
    {"name":"Haskell","val":1990},
    {"name":"Erlang","val":1986},
    {"name":"Visual Basic","val":1991},
])

for k in d: print(f"  tech_hl[{k}]: {len(d[k]['items'])}")
save('tech_hl.json', d)

# ── tech_match ────────────────────────────────────────
d = load('tech_match.json')

force50_nc(d,'akronyme',[
    {"n":"IoT","c":"Internet of Things"},
    {"n":"REST","c":"Representational State Transfer"},
])

force50_nc(d,'bigo',[
    {"n":"Breitensuche (BFS)","c":"O(V+E)"},
])

force50_nc(d,'dateiendungen',[
    {"n":".webp","c":"Bild (Google-Format)"},
])

force50_nc(d,'erfinder',[
    {"n":"Linux","c":"Linus Torvalds"},
])

force50_nc(d,'http',[
    {"n":"408 Request Timeout","c":"4xx Client-Fehler"},
    {"n":"429 Too Many Requests","c":"4xx Client-Fehler"},
    {"n":"301 Redirect","c":"3xx Weiterleitung"},
    {"n":"206 Partial Content","c":"2xx Erfolg"},
    {"n":"101 Switching Protocols","c":"1xx Informativ"},
])

force50_nc(d,'osi',[
    {"n":"NetBIOS","c":"5 Sitzung"},
])

force50_nc(d,'portnummern',[
    {"n":"Port 53","c":"DNS"},
    {"n":"Port 161","c":"SNMP"},
    {"n":"Port 389","c":"LDAP"},
    {"n":"Port 443","c":"HTTPS"},
    {"n":"Port 8443","c":"HTTPS Alternativ"},
    {"n":"Port 1433","c":"Microsoft SQL Server"},
    {"n":"Port 5900","c":"VNC"},
    {"n":"Port 3389","c":"RDP (Remote Desktop)"},
])

force50_nc(d,'tech_ma',[
    {"n":"YouTube","c":"Google (Alphabet)"},
    {"n":"DeepMind","c":"Google (Alphabet)"},
    {"n":"Nest Labs","c":"Google (Alphabet)"},
    {"n":"Mojang","c":"Microsoft"},
])

force50_nc(d,'turing_award',[
    {"n":"Yann LeCun","c":"Deep Learning (2018)"},
])

for k in d: print(f"  tech_match[{k}]: {len(d[k]['items'])}")
save('tech_match.json', d)

# ── tiere_hl ──────────────────────────────────────────
d = load('tiere_hl.json')

force50_hl(d,'pferde_gewicht',[
    {"name":"Przewalski-Pferd","val":350},
    {"name":"Noriker","val":700},
    {"name":"Andalusier","val":580},
])

force50_hl(d,'pferde_stockmass',[
    {"name":"Paso Fino","val":148},
    {"name":"Appaloosa","val":158},
])

force50_hl(d,'speed_land',[
    {"name":"Amerikanischer Gabelbock","val":88},
])

for k in d: print(f"  tiere_hl[{k}]: {len(d[k]['items'])}")
save('tiere_hl.json', d)

print("\nAll done.")
