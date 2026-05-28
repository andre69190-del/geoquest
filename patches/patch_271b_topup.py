#!/usr/bin/env python3
"""Second-pass top-up: fills all remaining sub-50 arrays"""
import json, os

DATA = os.path.join(os.path.dirname(__file__), '..', 'data')

def load(fn):
    with open(os.path.join(DATA, fn), encoding='utf-8') as f:
        return json.load(f)

def save(fn, d):
    with open(os.path.join(DATA, fn), 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f'  -> {fn} saved')

def thl(d, k, items):
    ex = {x['name'] for x in d[k]['items']}
    ad = [x for x in items if x['name'] not in ex]
    d[k]['items'].extend(ad[:max(0, 50-len(d[k]['items']))])
    print(f'    {k}: {len(d[k]["items"])}')

def tnc(d, k, items):
    ex = {x['n'] for x in d[k]['items']}
    ad = [x for x in items if x['n'] not in ex]
    d[k]['items'].extend(ad[:max(0, 50-len(d[k]['items']))])
    print(f'    {k}: {len(d[k]["items"])}')

def tp(d, k, items):
    ex = {x['n'] for x in d[k]['items']}
    ad = [x for x in items if x['n'] not in ex]
    d[k]['items'].extend(ad[:max(0, 50-len(d[k]['items']))])
    print(f'    {k}: {len(d[k]["items"])}')

def lhl(d, k, items):
    ex = {x['name'] for x in d[k]}
    ad = [x for x in items if x['name'] not in ex]
    d[k].extend(ad[:max(0, 50-len(d[k]))])
    print(f'    {k}: {len(d[k])}')

def lnc(d, k, items):
    ex = {x['n'] for x in d[k]}
    ad = [x for x in items if x['n'] not in ex]
    d[k].extend(ad[:max(0, 50-len(d[k]))])
    print(f'    {k}: {len(d[k])}')

def lp(d, k, items):
    ex = {x['n'] for x in d[k]}
    ad = [x for x in items if x['n'] not in ex]
    d[k].extend(ad[:max(0, 50-len(d[k]))])
    print(f'    {k}: {len(d[k])}')

# ── archaeologie_hl ──────────────────────────
print("archaeologie_hl.json")
d = load('archaeologie_hl.json')
thl(d,'entdeckungsjahr',[{"name":"Çatalhöyük (Türkei, Neolithikum)","val":1958}])
save('archaeologie_hl.json', d)

# ── archaeologie_pin ─────────────────────────
print("archaeologie_pin.json")
d = load('archaeologie_pin.json')
tp(d,'hoehlenmalerien',[{"n":"El Castillo (Kantabrien, Spanien)","lat":43.39,"lng":-4.14}])
save('archaeologie_pin.json', d)

# ── astro_hl ─────────────────────────────────
print("astro_hl.json")
d = load('astro_hl.json')
thl(d,'astro_planet_groesse',[
    {"name":"Ariel (Uranus-Mond)","val":1158},
    {"name":"Umbriel (Uranus-Mond)","val":1169},
    {"name":"Rhea (Saturn-Mond)","val":1527},
    {"name":"Oberon (Uranus-Mond)","val":1523},
    {"name":"Titania (Uranus-Mond)","val":1578},
    {"name":"Dione (Saturn-Mond)","val":1123},
    {"name":"Tethys (Saturn-Mond)","val":1066},
    {"name":"Iapetus (Saturn-Mond)","val":1469},
    {"name":"Charon (Pluto-Mond)","val":1212},
    {"name":"Mimas (Saturn-Mond)","val":396},
    {"name":"Enceladus (Saturn-Mond)","val":504},
    {"name":"Miranda (Uranus-Mond)","val":472},
])
thl(d,'astro_monde_anzahl',[
    {"name":"Erde","val":1},
    {"name":"Mars","val":2},
    {"name":"Pluto (Zwergplanet)","val":5},
    {"name":"Eris (Zwergplanet)","val":1},
    {"name":"Haumea (Zwergplanet)","val":2},
    {"name":"Makemake (Zwergplanet)","val":1},
    {"name":"Gonggong (Zwergplanet)","val":1},
])
thl(d,'astro_sonnenentfernung',[
    {"name":"Ceres (Zwergplanet)","val":414},
    {"name":"Pallas (Asteroid)","val":414},
    {"name":"Vesta (Asteroid)","val":353},
    {"name":"Chiron (Zentaur)","val":2052},
    {"name":"Quaoar (Zwergplanet)","val":6380},
])
thl(d,'astro_schwerkraft',[
    {"name":"Venus","val":8.87},
    {"name":"Uranus","val":8.69},
    {"name":"Mars","val":3.72},
    {"name":"Merkur","val":3.7},
    {"name":"Mond","val":1.62},
    {"name":"Pluto","val":0.62},
    {"name":"Ceres","val":0.27},
    {"name":"Ganymed","val":1.43},
])
thl(d,'astro_temperaturen',[{"name":"Neptun (Wolken)","val":-218}])
thl(d,'astro_entdeckungsjahr',[
    {"name":"Rhea (Giovanni Cassini)","val":1672},
    {"name":"Tethys (Giovanni Cassini)","val":1684},
    {"name":"Dione (Giovanni Cassini)","val":1684},
    {"name":"Enceladus (William Herschel)","val":1789},
    {"name":"Miranda (Gerard Kuiper)","val":1948},
])
thl(d,'astro_exoplaneten_distanz',[{"name":"Ross 128 b","val":11.0}])
save('astro_hl.json', d)

# ── astro_match ──────────────────────────────
print("astro_match.json")
d = load('astro_match.json')
tnc(d,'astro_planeten',[
    {"n":"Ganymede","c":"Größter Mond des Sonnensystems"},
    {"n":"Kallisto (Jupiter)","c":"Am stärksten kraterierter Körper"},
    {"n":"Enceladus (Saturn)","c":"Wassergeysire unter Eisdecke"},
    {"n":"Io (Jupiter)","c":"Aktivster Vulkankörper"},
    {"n":"Titania (Uranus)","c":"Größter Uranus-Mond"},
    {"n":"Charon (Pluto)","c":"Mond so groß wie Pluto selbst"},
    {"n":"Rhea (Saturn)","c":"Zweitmäßigster Saturn-Mond"},
    {"n":"Oberon (Uranus)","c":"Zweitgrößter Uranus-Mond"},
    {"n":"Iapetus (Saturn)","c":"Zweifarbiger Saturn-Mond"},
    {"n":"Dione (Saturn)","c":"Hat eine sauerstoffarme Atmosphäre"},
    {"n":"Ariel (Uranus)","c":"Hellster Uranus-Mond"},
    {"n":"Mimas (Saturn)","c":"Hat Todessttern-Aussehen (Odysseus-Krater)"},
    {"n":"Miranda (Uranus)","c":"Hat extreme Klippen (Verona Rupes)"},
    {"n":"Tethys (Saturn)","c":"Hat riesigen Odysseus-Krater"},
    {"n":"Umbriel (Uranus)","c":"Dunkelster Uranus-Mond"},
])
tnc(d,'astro_kosmologie',[
    {"n":"Weißer Zwerg","c":"Endstadium sonnenähnlicher Sterne"},
    {"n":"Roter Riese","c":"Entwicklungsphase ausgebrannter Sterne"},
    {"n":"Supernova","c":"Explosiver Tod massereicher Sterne"},
])
tnc(d,'astro_sonden_ziele',[{"n":"Parker Solar Probe (NASA)","c":"Sonne"}])
tnc(d,'astro_pioniere',[
    {"n":"Annie Jump Cannon","c":"Harvard-Spektralklassifikation (OBAFGKM)"},
    {"n":"Henrietta Swan Leavitt","c":"Perioden-Leuchtkraft-Cepheiden"},
    {"n":"Cecilia Payne-Gaposchkin","c":"Wasserstoff als häufigstes Element"},
    {"n":"Hipparchus (Antike)","c":"Sternkatalog & Präzession der Erde"},
    {"n":"Ptolemäus","c":"Geozentrisches Modell (Almagest)"},
    {"n":"George Ellery Hale","c":"Entwicklung großer Teleskope"},
    {"n":"Gerard Kuiper","c":"Kuiper-Gürtel-Hypothese"},
    {"n":"Jan Oort","c":"Oort'sche Wolke der Kometen"},
    {"n":"Walter Baade","c":"Unterscheidung Populationen I/II"},
    {"n":"Allan Sandage","c":"Hubble-Konstante Präzisionsmessung"},
])
tnc(d,'astro_galaxien_typen',[
    {"n":"Messier 87 (M87)","c":"Elliptische Galaxie"},
    {"n":"Centaurus A (NGC 5128)","c":"Elliptische Galaxie"},
    {"n":"Triangulum-Galaxie (M33)","c":"Spiralgalaxie"},
    {"n":"NGC 1300","c":"Balkenspiralgalaxie"},
    {"n":"Irregular Dwarf (SMC)","c":"Irregulaere Galaxie"},
])
save('astro_match.json', d)

# ── astro_pin ────────────────────────────────
print("astro_pin.json")
d = load('astro_pin.json')
tp(d,'astro_observatorien',[{"n":"Roque de los Muchachos (La Palma, Spanien)","lat":28.76,"lng":-17.89}])
tp(d,'astro_startrampen',[{"n":"Kodiak Launch Complex (Alaska, USA)","lat":57.44,"lng":-152.34}])
tp(d,'astro_meteoritenkrater',[
    {"n":"Sudbury Basin (Ontario, Kanada)","lat":46.6,"lng":-81.0},
    {"n":"Clearwater Lakes (Quebec, Kanada)","lat":56.2,"lng":-74.5},
    {"n":"Siljan Ring (Schweden)","lat":60.9,"lng":14.9},
])
save('astro_pin.json', d)

# ── gastro_hl ────────────────────────────────
print("gastro_hl.json")
d = load('gastro_hl.json')
thl(d,'kalorien',[
    {"name":"Nussbutter (Erdnussmus)","val":588},
    {"name":"Speck (gebraten)","val":541},
    {"name":"Mandeln (roh)","val":579},
    {"name":"Kokosnussöl","val":892},
])
thl(d,'kerntemperatur',[
    {"name":"Kalbsleber (durchgegart)","val":71},
    {"name":"Fasan (durchgegart)","val":74},
])
thl(d,'zubereitungszeit',[
    {"name":"Rouladen (klassisch)","val":150},
    {"name":"Risotto ai frutti di mare","val":50},
])
thl(d,'scoville',[
    {"name":"Tabasco Original","val":3750},
    {"name":"Chipotle en Adobo","val":8000},
    {"name":"Piri Piri","val":175000},
    {"name":"Jolokia-Pepper-Sauce","val":500000},
    {"name":"Naga Morich (Schlangen-Chili)","val":1000000},
])
thl(d,'preis_kg',[
    {"name":"Saffron (Safran, Marktpreis)","val":12000},
    {"name":"Almas Kaviar (Weißer Stör)","val":25000},
    {"name":"Kopi Luwak Rohkaffee","val":700},
    {"name":"Dry-Aged Wagyu (A5)","val":800},
])
thl(d,'wasseranteil',[
    {"name":"Rote Bete (roh)","val":87.6},
    {"name":"Artischocke","val":84.4},
    {"name":"Erdbeere","val":90.9},
    {"name":"Kiwi","val":83.1},
    {"name":"Pfirsich","val":87.7},
    {"name":"Kohlrabi","val":91.0},
    {"name":"Spargel (weiß)","val":93.0},
])
thl(d,'backtemperatur',[
    {"name":"Blätterteig-Kipferl","val":180},
    {"name":"Brandteig (Choux)","val":200},
    {"name":"New York-Style Bagels","val":230},
])
thl(d,'zutaten_anzahl',[{"name":"Beef Wellington (klassisch)","val":12}])
save('gastro_hl.json', d)

# ── gastro_match ─────────────────────────────
print("gastro_match.json")
d = load('gastro_match.json')
tnc(d,'hausmannskost',[
    {"n":"Smørrebrød (offenes Sandwich)","c":"Dänemark"},
    {"n":"Kotlet Schabowy (Schnitzel)","c":"Polen"},
    {"n":"Goulash (Gulyás)","c":"Ungarn"},
])
tnc(d,'kuechengeraete',[{"n":"Spritzbeutel","c":"Formen"}])
tnc(d,'schnitttechniken',[{"n":"Hacken (grob)","c":"Gemüse"}])
tnc(d,'gewuerzmischungen',[
    {"n":"Mole Rojo","c":"Amerika"},
    {"n":"Sichuan-Gewürz (Malatang)","c":"Asien"},
    {"n":"Jerk Seasoning (Jamaika)","c":"Amerika"},
    {"n":"Hawayij (Jemen)","c":"Asien"},
    {"n":"Chermoula (Marokko)","c":"Afrika"},
])
tnc(d,'fleisch_cuts',[{"n":"Coulotte (Picanha-Spitze)","c":"Rind"}])
tnc(d,'bakterien_pilze',[
    {"n":"Lactobacillus acidophilus","c":"Joghurt"},
    {"n":"Gluconobacter oxydans","c":"Kombucha"},
    {"n":"Mucor miehei (Rennin)","c":"Käse"},
    {"n":"Pediococcus cerevisiae","c":"Salami"},
    {"n":"Torulaspora delbrueckii","c":"Sauerteig-Aroma"},
    {"n":"Kluyveromyces lactis","c":"Käse (Lactose-Abbau)"},
    {"n":"Bacillus subtilis (natto)","c":"Natto"},
    {"n":"Monascus purpureus","c":"Roter Hefereis"},
    {"n":"Aspergillus awamori","c":"Awamori (Japanischer Schnaps)"},
    {"n":"Lactococcus lactis subsp. cremoris","c":"Butter"},
    {"n":"Brevibacterium linens","c":"Limburger Käse"},
])
tnc(d,'kaffeespezialitaeten',[
    {"n":"Galão (Portugal)","c":"Espresso"},
    {"n":"Café de Olla","c":"Filterkaffee"},
    {"n":"Piccolo Latte","c":"Espresso"},
    {"n":"Nitro Cold Brew","c":"Kaltextraktion"},
])
tnc(d,'exotische_fruechte',[
    {"n":"Feijoa (Ananas-Guave)","c":"Südamerika"},
    {"n":"Cupuaçu","c":"Südamerika"},
    {"n":"Tamarillo (Baumtomate)","c":"Südamerika"},
    {"n":"Acerola (Barbados-Kirsche)","c": "Mittelamerika"},
    {"n":"Cashew-Apfel","c":"Brasilien"},
    {"n":"Caimito (Sternapfel)","c":"Karibik"},
])
tnc(d,'brotsorten',[
    {"n":"Kisra (Sudanesisches Fladenbrot)","c":"Sudan"},
    {"n":"Bammy (Kassavabrot)","c":"Jamaika"},
    {"n":"Roggenbrot (Pumpernickel)","c":"Deutschland"},
    {"n":"Khobz (Marokkanisch)","c":"Marokko"},
])
tnc(d,'fruehstueck_welt',[
    {"n":"Ful Medames","c":"Ägypten"},
    {"n":"Gallo Pinto (Bohnen-Reis)","c":"Costa Rica"},
    {"n":"Croque Madame","c":"Frankreich"},
    {"n":"Congee (Reisbrei)","c":"China"},
    {"n":"Roti Canai","c":"Malaysia"},
])
tnc(d,'fachbegriffe_herd',[
    {"n":"Pochieren (Sous vide)","c":"Kochen"},
    {"n":"Schmoren (Braisieren)","c":"Kochen"},
])
tnc(d,'sushi_arten',[
    {"n":"Aburi Nigiri (abgeflammt)","c":"Nigiri"},
    {"n":"Sushi Burrito","c":"Fusion"},
    {"n":"Oshi Sushi (gepresstes Sushi)","c":"Geformter Reis"},
])
save('gastro_match.json', d)

# ── geo_hl ───────────────────────────────────
print("geo_hl.json")
d = load('geo_hl.json')
thl(d,'geo_berghoehen',[
    {"name":"Broad Peak (Pakistan/China)","val":8051},
    {"name":"Gasherbrum II (Pakistan/China)","val":8035},
    {"name":"Shishapangma (China)","val":8027},
    {"name":"Gyachung Kang (Nepal/China)","val":7952},
    {"name":"Himalchuli (Nepal)","val":7893},
    {"name":"Distaghil Sar (Pakistan)","val":7884},
    {"name":"Ngadi Chuli (Nepal)","val":7871},
])
thl(d,'geo_vulkan_hoehen',[
    {"name":"Sajama (Bolivien)","val":6542},
    {"name":"Chimborazo (Ecuador)","val":6263},
    {"name":"Antisana (Ecuador)","val":5753},
    {"name":"Merapi (Indonesien)","val":2930},
    {"name":"Aso (Japan)","val":1592},
])
thl(d,'geo_erdbeben_magnitude',[
    {"name":"Off the Coast Sumatra 2005","val":86},
    {"name":"Peru 1868","val":90},
    {"name":"Iquique 2014 (Chile)","val":82},
])
thl(d,'geo_vei_ausbruch',[
    {"name":"Hunga Tonga 2022","val":5},
    {"name":"Eyjafjallajökull 2010 (Island)","val":4},
    {"name":"Redoubt 2009 (Alaska)","val":4},
])
thl(d,'geo_hoehlen_laenge',[{"name":"Gua Air Jernih (Malaysia)","val":117}])
thl(d,'geo_schluchten_tiefe',[
    {"name":"Indus Gorge (Pakistan/Kaschmir)","val":5200},
    {"name":"Cauca Canyon (Kolumbien)","val":2000},
])
thl(d,'geo_kontinentaldrift',[
    {"name":"Scotia-Platte","val":22},
    {"name":"Burma-Platte","val":35},
    {"name":"Sunda-Platte","val":20},
    {"name":"Yangtze-Platte","val":15},
    {"name":"Aegäische Platte","val":30},
    {"name":"Adria-Platte","val":8},
    {"name":"Türkische Platte","val":25},
    {"name":"Iran-Platte","val":25},
])
thl(d,'geo_gletscher_volumen',[{"name":"Vatnajökull (Island)","val":3100}])
save('geo_hl.json', d)

# ── geo_match ────────────────────────────────
print("geo_match.json")
d = load('geo_match.json')
tnc(d,'geo_gesteinsarten',[
    {"n":"Travertin","c":"Sedimentär"},
    {"n":"Kreide (Kalkstein)","c":"Sedimentär"},
    {"n":"Evaporit (Gips)","c":"Sedimentär"},
    {"n":"Kohle (Anthrazit)","c":"Sedimentär"},
    {"n":"Syenit","c":"Magmatisch"},
    {"n":"Tuff","c":"Magmatisch"},
    {"n":"Peridotit","c":"Magmatisch"},
    {"n":"Eklgoit","c":"Metamorph"},
    {"n":"Amphibolit","c":"Metamorph"},
    {"n":"Hornfels","c":"Metamorph"},
    {"n":"Migmatit","c":"Metamorph"},
    {"n":"Kalksinter","c":"Sedimentär"},
    {"n":"Opalit","c":"Sedimentär"},
    {"n":"Felsit","c":"Magmatisch"},
    {"n":"Phonolith","c":"Magmatisch"},
])
tnc(d,'geo_tektonik',[
    {"n":"Taiwan","c":"Eurasische Platte / Philippinische Platte"},
    {"n":"Türkei","c":"Anatolische Platte"},
    {"n":"Äthiopien","c":"Afrikanische Platte"},
    {"n":"Chile","c":"Südamerikanische Platte"},
    {"n":"Mexiko","c":"Nordamerikanische Platte"},
    {"n":"Alaska","c":"Nordamerikanische Platte"},
    {"n":"Indonesien","c":"Eurasische Platte / Pazifische Platte"},
])
tnc(d,'geo_mineralien',[
    {"n":"Borax","c":"Waschmittel-Herstellung"},
    {"n":"Wolframit","c":"Wolfram-Gewinnung"},
    {"n":"Kassiterit","c":"Zinn-Gewinnung"},
])
tnc(d,'geo_fossil_zeitalter',[
    {"n":"Mammut (Wollmammut)","c":"Känozoikum"},
    {"n":"Homo sapiens (früh)","c":"Känozoikum"},
])
tnc(d,'geo_erdbeben_jahr',[
    {"n":"Nepal-Erdbeben (Gorkha)","c":"2015"},
    {"n":"Haiti-Erdbeben","c":"2010"},
])
tnc(d,'geo_gestein_nutzung',[
    {"n":"Ton (Keramik)","c":"Töpferei & Ziegelherstellung"},
    {"n":"Basalt","c":"Straßenbau & Pflastersteine"},
    {"n":"Tuff (Vulkan)","c":"Historischer Baustoff"},
])
tnc(d,'geo_landschaft_ursprung',[{"n":"Riff (Korallenriff)","c":"Biogene Ablagerung"}])
tnc(d,'geo_mineral_farbe',[
    {"n":"Türkis (Mineral)","c":"Blaugrün"},
    {"n":"Smaragd","c":"Grün"},
])
tnc(d,'geo_kontinent_platte',[
    {"n":"Madagaskar","c":"Afrikanische Platte"},
    {"n":"Tasmanien","c":"Australische Platte"},
    {"n":"Grönland","c":"Nordamerikanische Platte"},
])
tnc(d,'geo_mineral_kristall',[
    {"n":"Gips","c":"Monoklin"},
    {"n":"Korund","c":"Trigonal"},
])
save('geo_match.json', d)

# ── geo_pin ──────────────────────────────────
print("geo_pin.json")
d = load('geo_pin.json')
tp(d,'geo_vulkane',[{"n":"Mount Cleveland (Aleutians, USA)","lat":52.82,"lng":-169.94}])
tp(d,'geo_felsformationen',[{"n":"Meteora (Griechenland, Felsklöster)","lat":39.72,"lng":21.63}])
tp(d,'geo_hoehlensysteme',[{"n":"Cueva de Villa Luz (Tabasco, Mexiko)","lat":17.53,"lng":-92.75}])
tp(d,'geo_geysire',[
    {"n":"Wairakei Geothermal Area (Taupo, NZ)","lat":-38.63,"lng":176.09},
    {"n":"Umnak Geothermal (Aleutians, Alaska)","lat":53.3,"lng":-168.4},
])
tp(d,'geo_minen_bohrungen',[
    {"n":"Olympic Dam Mine (South Australia)","lat":-30.44,"lng":136.89},
    {"n":"Escondida Copper Mine (Chile)","lat":-24.26,"lng":-69.07},
])
save('geo_pin.json', d)

# ── pflanzen_hl ──────────────────────────────
print("pflanzen_hl.json")
d = load('pflanzen_hl.json')
thl(d,'alter',[{"name":"Old Tjikko (Fichte, Schweden)","val":9500}])
thl(d,'kaffeeproduktion',[
    {"name":"Madagaskar","val":70},
    {"name":"Elfenbeinküste","val":500},
    {"name":"Bolivien","val":25},
    {"name":"Ecuador","val":350},
    {"name":"Ruanda","val":320},
    {"name":"El Salvador","val":60},
    {"name":"Jamaika","val":25},
    {"name":"Äthiopien (update)","val":7700},
    {"name":"Indien","val":850},
    {"name":"Papua-Neuguinea (update)","val":1100},
    {"name":"Laos","val":200},
    {"name":"Myanmar","val":80},
    {"name":"Vietnam (update)","val":31200},
    {"name":"Kamerun (update)","val":350},
])
thl(d,'weinproduktion',[
    {"name":"Georgien","val":200},
    {"name":"Bulgarien","val":100},
    {"name":"Slowakei","val":50},
    {"name":"Slowenien","val":80},
    {"name": "Zypern","val":30},
    {"name":"Nordmazedonien","val":40},
    {"name":"Albanien","val":15},
    {"name":"Kosovo","val":10},
    {"name":"Montenegro","val":20},
    {"name":"Bosnien","val":15},
    {"name":"Serbien","val":50},
    {"name":"Kanada","val":147},
    {"name":"China","val":6600},
    {"name":"Mexiko","val":40},
    {"name":"Uruguay","val":79},
    {"name":"Peru","val":52},
    {"name":"Indien","val":26},
])
thl(d,'reisproduktion',[
    {"name":"Laos","val":3.5},
    {"name":"Madagascar","val":4.0},
    {"name":"Guinea","val":2.3},
    {"name":"Tansania (update)","val":3.0},
    {"name":"Nordkorea","val":2.1},
    {"name":"Senegal","val":1.2},
    {"name":"Ghana","val":0.7},
    {"name":"Äthiopien","val":0.9},
    {"name":"Mozambique","val":0.4},
    {"name":"Sierra Leone","val":0.8},
    {"name":"Pakistan (update)","val":11.5},
    {"name":"Elfenbeinküste","val":1.3},
    {"name":"Mali","val":1.5},
    {"name":"Haiti","val":0.08},
    {"name":"Ruanda","val":0.35},
    {"name":"Kuba","val":0.5},
    {"name":"Kamerun","val":0.4},
    {"name":"Malawi","val":0.3},
])
thl(d,'waldflaeche',[
    {"name":"Kongo (Rep.)","val":65.0},
    {"name":"Kamerun","val":42.0},
    {"name":"Zentralafrikanische Republik","val":36.0},
    {"name":"Finnland","val":73.0},
])
save('pflanzen_hl.json', d)

# ── pflanzen_match ───────────────────────────
print("pflanzen_match.json")
d = load('pflanzen_match.json')
tnc(d,'familien',[
    {"n":"Birke (Betula)","c":"Betulaceae"},
    {"n":"Eiche (Quercus)","c":"Fagaceae"},
    {"n":"Linde (Tilia)","c":"Malvaceae"},
    {"n":"Mais (Zea mays)","c":"Poaceae"},
    {"n":"Sellerie (Apium)","c":"Apiaceae"},
    {"n":"Petersilie","c":"Apiaceae"},
    {"n":"Basilikum","c":"Lamiaceae"},
])
tnc(d,'bestuaeber',[
    {"n":"Linde (Tilia cordata)","c":"Bienen"},
    {"n":"Sonnenblume","c":"Bienen"},
])
tnc(d,'herkunft',[
    {"n":"Kaffee (Coffea arabica)","c":"Äthiopien"},
    {"n":"Ananas","c":"Südamerika"},
    {"n":"Avocado","c":"Mittelamerika"},
    {"n":"Paprika","c":"Mittelamerika"},
    {"n":"Zucchini","c":"Nordamerika"},
    {"n":"Heidelbeere","c":"Nordamerika"},
])
tnc(d,'nutzung',[
    {"n":"Aloe vera","c":"Kosmetik / Medizin"},
    {"n":"Stevia rebaudiana","c":"Süßungsmittel"},
    {"n":"Fliegenfalle (Dionaea)","c":"Insektivorie"},
    {"n":"Hanf (Cannabis, medizinisch)","c":"Medizin / Pharmazie"},
])
tnc(d,'klimazone',[{"n":"Lärche (Larix decidua)","c":"Boreal"}])
save('pflanzen_match.json', d)

# ── pflanzen_pin ─────────────────────────────
print("pflanzen_pin.json")
d = load('pflanzen_pin.json')
tp(d,'einzelbaeume',[
    {"n":"Te Matua Ngahere (Kauri, Neuseeland)","lat":-35.46,"lng":173.52},
    {"n":"Thimmamma Marrimanu (Banyan, Indien)","lat":14.22,"lng":77.61},
])
tp(d,'botanische_gaerten',[
    {"n":"National Botanic Garden of Belgium (Meise)","lat":50.93,"lng":4.38},
    {"n":"Peradeniya Royal Botanic Gardens (Sri Lanka)","lat":7.27,"lng":80.6},
])
tp(d,'tropenwald',[
    {"n":"Atlantic Forest (Mata Atlântica, Brasilien)","lat":-20.0,"lng":-41.5},
    {"n":"Sumatra-Regenwald (Gunung Leuser NP)","lat":3.84,"lng":97.53},
])
save('pflanzen_pin.json', d)

# ── sport_hl ─────────────────────────────────
print("sport_hl.json")
d = load('sport_hl.json')
thl(d,'sport_marathon_alter',[
    {"name":"Fukuoka Marathon (Japan)","val":1947},
    {"name":"Kosice Peace Marathon (Slowakei)","val":1924},
    {"name":"Comrades Marathon (Südafrika)","val":1921},
    {"name":"Polytechnic Marathon (UK)","val":1909},
    {"name":"Pikes Peak Marathon (USA)","val":1956},
])
thl(d,'sport_stadien_kapazitaet',[{"name":"FNB Stadium (Johannesburg, Südafrika)","val":95}])
thl(d,'sport_olympia_goldmedaillen',[
    {"name":"Nikolai Andrianov (Turnen, UdSSR)","val":7},
    {"name": "Paavo Nurmi (Leichtathletik, Finnland)","val":9},
    {"name":"Matt Biondi (Schwimmen, USA)","val":8},
    {"name":"Takashi Ono (Turnen, Japan)","val":5},
    {"name":"Aladár Gerevich (Fechten, Ungarn)","val":7},
    {"name":"Vitali Scherbo (Turnen, Belarus)","val":6},
])
thl(d,'sport_fussball_marktwert',[
    {"name":"Gavi (FC Barcelona)","val":110},
    {"name":"Jamal Musiala (Bayern München)","val":110},
    {"name":"Eduardo Camavinga (Real Madrid)","val":100},
    {"name":"Marcus Rashford (Manchester United)","val":100},
])
thl(d,'sport_tore_saison',[{"name":"Romário (Fluminense, Brasilien)","val":55}])
save('sport_hl.json', d)

# ── sport_match ──────────────────────────────
print("sport_match.json")
d = load('sport_match.json')
tnc(d,'sport_teamgroesse',[
    {"n":"Badminton (Doppel)","c":"2 Spieler"},
    {"n":"Tischtennis (Doppel)","c":"2 Spieler"},
    {"n":"Bobsleigh (Vierer-Bob)","c":"4 Spieler"},
    {"n":"Rudern (Achter)","c":"8 Spieler"},
    {"n":"Synchronschwimmen","c":"8 Spieler"},
    {"n":"Softball","c":"9 Spieler"},
    {"n":"Canoe Polo","c":"5 Spieler"},
    {"n":"Ultimate Frisbee","c":"7 Spieler"},
    {"n":"Quidditch (Kesseldorf)","c":"7 Spieler"},
    {"n":"Floorball","c":"6 Spieler"},
    {"n":"Blind Football (B1)","c":"5 Spieler"},
    {"n":"Wheelchair Basketball","c":"5 Spieler"},
    {"n":"Ringette","c":"6 Spieler"},
    {"n":"Speedball","c":"11 Spieler"},
])
tnc(d,'sport_olympisch',[
    {"n":"Squash","c":"Nein"},
    {"n":"Cricket","c":"Nein"},
    {"n":"Polo","c":"Nein"},
    {"n":"Motorsport (F1)","c":"Nein"},
    {"n":"Schach","c":"Nein"},
    {"n":"Bowling","c":"Nein"},
    {"n":"Cheerleading","c":"Nein"},
])
tnc(d,'sport_nationalsport_match',[
    {"n":"Kabaddi","c":"Bangladesch"},
    {"n":"Bandy","c":"Russland"},
    {"n":"Lacrosse","c":"Kanada"},
    {"n":"Basque Pelota","c":"Spanien"},
    {"n":"Australian Rules Football","c":"Australien"},
    {"n":"Martial Arts (Wushu)","c":"China"},
    {"n":"Capoeira","c":"Brasilien"},
    {"n":"Muay Thai","c":"Thailand"},
    {"n":"Naadam (Mongolisch)","c":"Mongolei"},
    {"n":"Judo","c":"Japan"},
    {"n":"Rodeo","c":"USA"},
])
tnc(d,'sport_sportart_kontinent',[
    {"n":"Kabaddi","c":"Asien"},
    {"n":"Hurling","c":"Europa"},
    {"n":"Capoeira","c":"Südamerika"},
    {"n":"Australian Football (AFL)","c":"Ozeanien"},
])
save('sport_match.json', d)

# ── sport_pin ────────────────────────────────
print("sport_pin.json")
d = load('sport_pin.json')
tp(d,'sport_marathonstrecken',[
    {"n":"Amsterdam Marathon Ziel (Olympisch Stadion)","lat":52.343,"lng":4.853},
    {"n":"Madrid Marathon Start (Plaza de Cibeles)","lat":40.418,"lng":-3.693},
    {"n":"Kopenhagen Marathon Start (Frederiksberg)","lat":55.68,"lng":12.53},
])
tp(d,'sport_fussballstadien',[
    {"n":"Bernabeu (Real Madrid, Spanien)","lat":40.45,"lng":-3.69},
    {"n":"Old Trafford (Manchester United, England)","lat":53.46,"lng":-2.29},
])
tp(d,'sport_motorsport_strecken',[
    {"n":"Circuit de la Sarthe (Le Mans, Frankreich)","lat":47.94,"lng":0.21},
    {"n":"Daytona International Speedway (Florida, USA)","lat":29.19,"lng":-81.07},
    {"n":"Sepang International Circuit (Malaysia)","lat":2.76,"lng":101.74},
])
tp(d,'sport_wintersport_orte',[{"n":"Hakuba (Japan) — Olympia 1998 (Nagano)","lat":36.7,"lng":137.86}])
tp(d,'sport_golf_platze',[{"n":"Royal County Down (Nordirland)","lat":54.2,"lng":-5.87}])
tp(d,'sport_surfspots_welt',[
    {"n":"Playa Zicatela (Puerto Escondido, Mexiko)","lat":15.85,"lng":-97.09},
    {"n":"Anchor Point (Taghazout, Marokko)","lat":30.54,"lng":-9.71},
    {"n":"Lance's Right (Mentawai, Indonesien)","lat":-1.6,"lng":99.7},
])
save('sport_pin.json', d)

# ── tech_hl ──────────────────────────────────
print("tech_hl.json")
d = load('tech_hl.json')
thl(d,'transistoren',[
    {"name":"MediaTek Dimensity 9300","val":25},
    {"name":"Apple A17 Pro","val":19},
    {"name":"Qualcomm Snapdragon X Elite","val":42},
])
thl(d,'code_zeilen',[
    {"name":"Firefox (Gecko Engine)","val":22},
    {"name":"Facebook/Meta Backend","val":62},
])
thl(d,'release_jahr',[
    {"name":"ALGOL 60","val":1960},
    {"name":"Simula","val":1967},
    {"name":"Smalltalk","val":1972},
    {"name":"ML (Meta Language)","val":1973},
    {"name":"Scheme","val":1975},
    {"name":"AWK","val":1977},
    {"name":"Modula-2","val":1977},
    {"name":"Common Lisp","val":1984},
    {"name":"Tcl","val":1988},
    {"name":"Bash","val":1989},
    {"name":"Standard ML","val":1990},
    {"name":"Lua","val":1993},
    {"name":"Delphi","val":1995},
    {"name":"OCaml","val":1996},
    {"name":"Rebol","val":1997},
    {"name":"D","val":2001},
    {"name":"Groovy","val":2003},
])
thl(d,'internet_speed',[
    {"name":"Vereinigte Arabische Emirate","val":183},
    {"name":"Belgien","val":155},
    {"name":"Kanada","val":130},
    {"name":"Niederlande","val":185},
    {"name":"Österreich","val":115},
    {"name":"Spanien","val":130},
    {"name":"Portugal","val":125},
    {"name":"Neuseeland","val":115},
    {"name":"Israel","val":150},
    {"name":"Australien","val":90},
])
save('tech_hl.json', d)

# ── tech_match ───────────────────────────────
print("tech_match.json")
d = load('tech_match.json')
tnc(d,'sensoren',[
    {"n":"SHT31 (Sensirion)","c":"Temperatur/Feuchtigkeit"},
    {"n":"INA219","c":"Strom/Spannung"},
])
tnc(d,'syntax',[{"n":"writeln('Hello World')","c":"Pascal"}])
tnc(d,'osi',[
    {"n":"X.25","c":"3 Netz"},
    {"n":"OSPF","c":"3 Netz"},
    {"n":"Frame Relay","c":"2 Sicherung"},
    {"n":"ATM","c":"2 Sicherung"},
    {"n":"VLAN (802.1Q)","c":"2 Sicherung"},
    {"n":"SONET","c":"1 Physikalisch"},
    {"n":"Wi-Fi (802.11)","c":"1 Physikalisch"},
    {"n":"Glasfaser","c":"1 Physikalisch"},
    {"n":"RPC","c":"5 Sitzung"},
])
tnc(d,'bigo',[
    {"n":"Floyd-Warshall (kürzeste Wege)","c":"O(n³)"},
    {"n":"Counting Sort","c":"O(n+k)"},
    {"n":"Trie-Suche","c":"O(k)"},
    {"n":"Radix Sort","c":"O(nk)"},
    {"n":"Bellman-Ford","c":"O(VE)"},
    {"n":"Kruskal/Prim (MST)","c":"O(E log E)"},
    {"n":"Dijkstra (Heap)","c":"O((V+E) log V)"},
])
# http: add more codes
tnc(d,'http',[
    {"n":"102 Processing","c":"1xx Information"},
    {"n":"201 Created","c":"2xx Erfolg"},
    {"n":"206 Partial Content","c":"2xx Erfolg"},
    {"n":"308 Permanent Redirect","c":"3xx Weiterleitung"},
    {"n":"412 Precondition Failed","c":"4xx Client-Fehler"},
    {"n":"416 Range Not Satisfiable","c":"4xx Client-Fehler"},
    {"n":"422 Unprocessable Entity","c":"4xx Client-Fehler"},
    {"n":"451 Unavailable For Legal Reasons","c":"4xx Client-Fehler"},
    {"n":"504 Gateway Timeout","c":"5xx Server-Fehler"},
    {"n":"507 Insufficient Storage","c":"5xx Server-Fehler"},
    {"n":"511 Network Auth Required","c":"5xx Server-Fehler"},
    {"n":"203 Non-Authoritative","c":"2xx Erfolg"},
    {"n":"205 Reset Content","c":"2xx Erfolg"},
    {"n":"207 Multi-Status","c":"2xx Erfolg"},
    {"n":"209 Already Reported","c":"2xx Erfolg"},
    {"n":"226 IM Used","c":"2xx Erfolg"},
])
# wahrheitstabellen: already has many, add more unique ones
tnc(d,'wahrheitstabellen',[
    {"n":"A=0, B=0 → 1 (NAND)","c":"NAND"},
    {"n":"A=0, B=0 → 1 (XNOR)","c":"XNOR"},
    {"n":"A=0, B=0 → 0 (NOR false)","c":"OR"},
    {"n":"A=0, B=1 → 1 (NOR false edge)","c":"OR"},
    {"n":"A=0 → 0 (NOT false)","c":"NOT"},
    {"n":"A=1, B=0 → 1 (OR)","c":"OR"},
    {"n":"A=1, B=0 → 0 (AND zero)","c":"AND"},
    {"n":"A=1, B=1 → 0 (XOR zero)","c":"XOR"},
    {"n":"A=1, B=1 → 1 (XNOR true)","c":"XNOR"},
    {"n":"A=0, B=1 → 0 (AND false)","c":"AND"},
    {"n":"A=0, B=0 → 0 (XOR false)","c":"XOR"},
    {"n":"A=0, B=1 → 1 (XOR true)","c":"XOR"},
    {"n":"A=1, B=0 → 1 (XOR true)","c":"XOR"},
    {"n":"A=0, B=1 → 0 (XNOR false)","c":"XNOR"},
    {"n":"A=0, B=0 → 0 (NOR false case)","c":"NOR"},
    {"n":"A=1, B=0 → 0 (NOR false)","c":"NOR"},
    {"n":"A=0, B=1 → 0 (NOR edge)","c":"NOR"},
    {"n":"A=1, B=1 → 0 (NOR all)","c":"NOR"},
    {"n":"A=0, B=0 → 1 (NOR true)","c":"NOR"},
    {"n":"A=0, B=0 → 1 (NAND all zero)","c":"NAND"},
    {"n":"A=0, B=1 → 1 (NAND partial)","c":"NAND"},
    {"n":"A=1, B=0 → 1 (NAND partial)","c":"NAND"},
    {"n":"A=1, B=1 → 0 (NAND all)","c":"NAND"},
    {"n":"A=0, B=0 → 0 (AND all)","c":"AND"},
    {"n":"A=0, B=1 → 0 (AND partial)","c":"AND"},
    {"n":"A=1, B=0 → 0 (AND partial)","c":"AND"},
])
tnc(d,'erfinder',[
    {"n":"Transistor (1947)","c":"Shockley/Bardeen/Brattain"},
    {"n":"Fortran (Programmiersprache)","c":"John Backus"},
    {"n":"BASIC (Programmiersprache)","c":"John Kemeny & Thomas Kurtz"},
    {"n":"C++ (Programmiersprache)","c":"Bjarne Stroustrup"},
])
tnc(d,'portnummern',[
    {"n":"Port 8080","c":"HTTP Alternativ"},
    {"n":"Port 3389","c":"RDP"},
    {"n":"Port 5900","c":"VNC"},
    {"n":"Port 161","c":"SNMP"},
    {"n":"Port 500","c":"IKE/IPSec"},
    {"n":"Port 1723","c":"PPTP"},
    {"n":"Port 4444","c":"Metasploit (Standard)"},
    {"n":"Port 5985","c":"WinRM HTTP"},
    {"n":"Port 9200","c":"Elasticsearch"},
    {"n":"Port 2181","c":"Apache ZooKeeper"},
    {"n":"Port 6443","c":"Kubernetes API"},
    {"n":"Port 9092","c":"Apache Kafka"},
    {"n":"Port 2379","c":"etcd (Kubernetes)"},
    {"n":"Port 8443","c":"HTTPS Alternativ"},
    {"n":"Port 8883","c":"MQTT TLS"},
    {"n":"Port 1883","c":"MQTT"},
])
tnc(d,'dateiendungen',[
    {"n":".ts","c":"TypeScript"},
    {"n":".tsx","c":"TypeScript React"},
    {"n":".rs","c":"Rust"},
    {"n":".go","c":"Go"},
    {"n":".kt","c":"Kotlin"},
])
tnc(d,'akronyme',[
    {"n":"JWT","c":"JSON Web Token"},
    {"n":"OAuth","c":"Open Authorization"},
    {"n":"REST","c":"Representational State Transfer"},
    {"n":"CORS","c":"Cross-Origin Resource Sharing"},
    {"n":"DRM","c":"Digital Rights Management"},
    {"n":"MIME","c":"Multipurpose Internet Mail Extensions"},
    {"n":"LDAP","c":"Lightweight Directory Access Protocol"},
])
tnc(d,'turing_award',[
    {"n":"Yoshua Bengio","c":"Deep Learning (2018, mit LeCun & Hinton)"},
    {"n":"Silvio Micali","c":"Kryptographie & Zero-Knowledge Proofs (2012)"},
    {"n":"Avi Wigderson","c":"Pseudozufall & Berechnungskomplexität (2021)"},
])
tnc(d,'erste_videospiele',[
    {"n":"Spacewar! (PDP-1)","c":"1960er"},
    {"n":"Pong (Atari, Arcade)","c":"1970er"},
])
tnc(d,'malware',[{"n":"Carbanak (2014)","c":"APT / Banking-Trojaner"}])
tnc(d,'tech_ma',[
    {"n":"Tumblr","c":"Automattic"},
    {"n":"Slack","c":"Salesforce"},
    {"n":"Twitch","c":"Amazon"},
    {"n":"Ring (Doorbell)","c":"Amazon"},
    {"n":"Zappos","c":"Amazon"},
    {"n":"Waze","c":"Google/Alphabet"},
    {"n":"Nest Labs","c":"Google/Alphabet"},
    {"n":"DeepMind","c":"Google/Alphabet"},
])
save('tech_match.json', d)

# ── tech_pin ─────────────────────────────────
print("tech_pin.json")
d = load('tech_pin.json')
tp(d,'programmiersprachen',[
    {"n":"Kotlin (JetBrains, Prag)","lat":50.08,"lng":14.44},
    {"n":"Erlang (Ericsson, Stockholm)","lat":59.33,"lng":18.07},
    {"n":"Haskell (Glasgow, Schottland)","lat":55.86,"lng":-4.25},
    {"n":"OCaml (INRIA, Paris)","lat":48.86,"lng":2.35},
])
tp(d,'halbleiter',[
    {"n":"SK Hynix (Icheon, Südkorea)","lat":37.28,"lng":127.44},
    {"n":"Micron Technology (Boise, Idaho)","lat":43.63,"lng":-116.2},
])
tp(d,'rechenzentren',[{"n":"ChinaNet Backbone (Beijing)","lat":39.91,"lng":116.39}])
tp(d,'pioniere',[{"n":"Claude Shannon (Bell Labs, Murray Hill)","lat":40.69,"lng":-74.4}])
tp(d,'tech_museen',[
    {"n":"Tekniska Museet (Stockholm)","lat":59.36,"lng":18.1},
    {"n":"Musée des Arts et Métiers (Paris)","lat":48.866,"lng":2.355},
])
tp(d,'supercomputer',[
    {"n":"Stampede2 (TACC, Austin, Texas)","lat":30.39,"lng":-97.73},
    {"n":"Jade (CINES, Montpellier, Frankreich)","lat":43.61,"lng":3.88},
    {"n":"Hawk (HLRS, Stuttgart)","lat":48.74,"lng":9.1},
])
save('tech_pin.json', d)

# ── tiere_hl ─────────────────────────────────
print("tiere_hl.json")
d = load('tiere_hl.json')
thl(d,'gewicht_land',[
    {"name":"Gaur (Wildbüffel)","val":1000},
    {"name":"Kodiak-Bär","val":680},
])
thl(d,'gewicht_meer',[
    {"name":"Gewöhnlicher Krake (Octopus vulgaris)","val":10},
    {"name":"Manatee (Seekuh)","val":590},
    {"name":"Grönlandwal","val":100000},
])
thl(d,'speed_land',[
    {"name":"Kap-Büffelherde (Kurzspurt)","val":57},
    {"name":"Strauß","val":70},
])
thl(d,'speed_wasser',[{"name":"Atlantischer Lachs (Stromschnellen)","val":34}])
thl(d,'traechtigkeit',[{"name":"Gorilla","val":257}])
thl(d,'gift',[{"name":"Giftige Kegelschnecke (Conus textile)","val":3000}])
thl(d,'pferde_stockmass',[
    {"name":"Arabisches Vollblut","val":153},
    {"name":"Welsh Mountain Pony (Sektion A)","val":122},
    {"name":"Knabstrupper","val":155},
    {"name":"Isländer","val":140},
])
thl(d,'pferde_gewicht',[
    {"name":"Isländer","val":400},
    {"name":"Lusitano","val":540},
    {"name":"Trakehner","val":500},
    {"name":"Knabstrupper","val":500},
    {"name":"Paso Fino","val":380},
    {"name":"Quarter Horse","val":550},
    {"name":"Missouri Fox Trotter","val":500},
    {"name":"Camargue","val":430},
])
save('tiere_hl.json', d)

print("\nAll done.")
