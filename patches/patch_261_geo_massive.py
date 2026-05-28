"""
patch_261_geo_massive.py
Phase 261 — Geologie Massive Expansion
Skaliert geo_pin.json, geo_hl.json, geo_match.json von 8 auf 40-70 Items.
"""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")

def jload(fname):
    with open(os.path.join(DATA, fname), encoding="utf-8") as f:
        return json.load(f)

def jsave(fname, data):
    with open(os.path.join(DATA, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extend_key(data, key, new_items, name_field="n"):
    block = data[key]
    if isinstance(block, dict):
        existing = block.get("items", [])
    else:
        existing = block
    ex_names = {it.get(name_field, "").lower() for it in existing}
    added = [it for it in new_items if it.get(name_field, "").lower() not in ex_names]
    if isinstance(block, dict):
        block["items"] = existing + added
    else:
        data[key] = existing + added
    return len(added)

# ============================================================
# geo_pin.json
# ============================================================
pin = jload("geo_pin.json")

# --- geo_vulkane (Ziel: 50+) ---
vulkane_new = [
    {"n": "Stromboli (Äolische Inseln, Italien)", "lat": 38.79, "lng": 15.21},
    {"n": "Piton de la Fournaise (Réunion, Frankreich)", "lat": -21.24, "lng": 55.71},
    {"n": "Kīlauea (Hawaii, USA)", "lat": 19.42, "lng": -155.29},
    {"n": "Sakurajima (Kyushu, Japan)", "lat": 31.58, "lng": 130.66},
    {"n": "Merapi (Java, Indonesien)", "lat": -7.54, "lng": 110.44},
    {"n": "Krakatau (Sunda-Straße, Indonesien)", "lat": -6.10, "lng": 105.42},
    {"n": "Popocatépetl (Mexiko)", "lat": 19.02, "lng": -98.62},
    {"n": "Mount St. Helens (Washington, USA)", "lat": 46.19, "lng": -122.19},
    {"n": "Pinatubo (Luzon, Philippinen)", "lat": 15.14, "lng": 120.35},
    {"n": "Cotopaxi (Ecuador)", "lat": -0.68, "lng": -78.44},
    {"n": "Chimborazo (Ecuador)", "lat": -1.47, "lng": -78.82},
    {"n": "Villarrica (Chile)", "lat": -39.42, "lng": -71.93},
    {"n": "Ruapehu (Neuseeland)", "lat": -39.28, "lng": 175.57},
    {"n": "White Island / Whakaari (Neuseeland)", "lat": -37.52, "lng": 177.18},
    {"n": "Tavurvur (Papua-Neuguinea)", "lat": -4.27, "lng": 152.20},
    {"n": "Nyiragongo (DR Kongo)", "lat": -1.52, "lng": 29.25},
    {"n": "Mount Erebus (Antarktis)", "lat": -77.53, "lng": 167.17},
    {"n": "Erta Ale (Äthiopien)", "lat": 13.60, "lng": 40.67},
    {"n": "Teide (Teneriffa, Spanien)", "lat": 28.27, "lng": -16.64},
    {"n": "Hekla (Island)", "lat": 63.98, "lng": -19.70},
    {"n": "Grímsvötn (Island)", "lat": 64.42, "lng": -17.33},
    {"n": "Bardarbunga (Island)", "lat": 64.63, "lng": -17.53},
    {"n": "Katla (Island)", "lat": 63.63, "lng": -19.05},
    {"n": "Galeras (Kolumbien)", "lat": 1.22, "lng": -77.36},
    {"n": "Nevado del Ruiz (Kolumbien)", "lat": 4.89, "lng": -75.32},
    {"n": "Mount Rainier (Washington, USA)", "lat": 46.85, "lng": -121.74},
    {"n": "Lassen Peak (Kalifornien, USA)", "lat": 40.49, "lng": -121.50},
    {"n": "Soufrière Hills (Montserrat)", "lat": 16.71, "lng": -62.18},
    {"n": "La Palma — Cumbre Vieja (Spanien)", "lat": 28.57, "lng": -17.84},
    {"n": "Colima (Mexiko)", "lat": 19.51, "lng": -103.62},
    {"n": "Semeru (Java, Indonesien)", "lat": -8.11, "lng": 112.92},
    {"n": "Tambora (Sumbawa, Indonesien)", "lat": -8.25, "lng": 117.99},
    {"n": "Sinabung (Sumatra, Indonesien)", "lat": 3.17, "lng": 98.39},
    {"n": "Bezymianny (Kamtschatka, Russland)", "lat": 55.97, "lng": 160.59},
    {"n": "Klyuchevskaya Sopka (Kamtschatka, Russland)", "lat": 56.06, "lng": 160.64},
    {"n": "Yellowstone Caldera (Wyoming, USA)", "lat": 44.43, "lng": -110.59},
    {"n": "Long Valley Caldera (Kalifornien, USA)", "lat": 37.70, "lng": -118.87},
    {"n": "Taal (Luzon, Philippinen)", "lat": 14.00, "lng": 121.00},
    {"n": "Mayon (Luzon, Philippinen)", "lat": 13.26, "lng": 123.69},
    {"n": "Ulawun (Papua-Neuguinea)", "lat": -5.05, "lng": 151.33},
    {"n": "Tungurahua (Ecuador)", "lat": -1.47, "lng": -78.45},
    {"n": "Arenal (Costa Rica)", "lat": 10.46, "lng": -84.70},
]

# --- geo_hoehlensysteme (Ziel: 40+) ---
hoehlen_new = [
    {"n": "Lechuguilla Cave (New Mexico, USA)", "lat": 32.11, "lng": -104.55},
    {"n": "Wind Cave (South Dakota, USA)", "lat": 43.56, "lng": -103.48},
    {"n": "Sac Actun (Mexiko)", "lat": 20.23, "lng": -87.46},
    {"n": "Sistema Sac Actun / Dos Ojos (Mexiko)", "lat": 20.27, "lng": -87.39},
    {"n": "Hölloch (Schweiz)", "lat": 46.96, "lng": 8.67},
    {"n": "Eisriesenwelt (Österreich)", "lat": 47.50, "lng": 13.17},
    {"n": "Škocjan-Höhlen (Slowenien)", "lat": 45.66, "lng": 13.99},
    {"n": "Postojna-Höhle (Slowenien)", "lat": 45.78, "lng": 14.20},
    {"n": "Movile Cave (Rumänien)", "lat": 43.83, "lng": 28.56},
    {"n": "Krubera Cave (Georgien)", "lat": 43.41, "lng": 40.36},
    {"n": "Snezhnaya Cave (Abchasien)", "lat": 43.39, "lng": 40.47},
    {"n": "Son Doong (Vietnam)", "lat": 17.55, "lng": 106.29},
    {"n": "Hang En (Vietnam)", "lat": 17.54, "lng": 106.20},
    {"n": "Phong Nha Cave (Vietnam)", "lat": 17.55, "lng": 106.28},
    {"n": "Mulu-Höhlen (Sarawak, Malaysia)", "lat": 4.05, "lng": 114.81},
    {"n": "Deer Cave (Sarawak, Malaysia)", "lat": 4.03, "lng": 114.82},
    {"n": "Carlsbad Caverns (New Mexico, USA)", "lat": 32.18, "lng": -104.44},
    {"n": "Blue Grotto (Malta)", "lat": 35.83, "lng": 14.43},
    {"n": "Reed Flute Cave (Guilin, China)", "lat": 25.32, "lng": 110.24},
    {"n": "Er Wang Dong Cave System (Chongqing, China)", "lat": 29.57, "lng": 108.45},
    {"n": "Majlis Al Jinn (Oman)", "lat": 22.91, "lng": 59.26},
    {"n": "Tham Khoun Xe (Laos)", "lat": 16.73, "lng": 105.73},
    {"n": "Waitomo Caves (Neuseeland)", "lat": -38.26, "lng": 175.11},
    {"n": "Naracoorte Caves (Australien)", "lat": -36.97, "lng": 140.79},
    {"n": "Jenolan Caves (Australien)", "lat": -33.82, "lng": 150.02},
    {"n": "Cueva de los Cristales (Chihuahua, Mexiko)", "lat": 27.87, "lng": -105.50},
    {"n": "Grotte de Lascaux (Frankreich)", "lat": 45.05, "lng": 1.08},
    {"n": "Cave of Altamira (Spanien)", "lat": 43.38, "lng": -4.12},
    {"n": "Glowworm Caves (Waitomo, Neuseeland)", "lat": -38.26, "lng": 175.10},
    {"n": "Veryovkina Cave (Abchasien)", "lat": 43.43, "lng": 40.36},
    {"n": "Gouffre Mirolda (Frankreich)", "lat": 46.09, "lng": 6.68},
    {"n": "Torca del Cerro (Spanien)", "lat": 43.15, "lng": -4.20},
    {"n": "Sistema Huautla (Mexiko)", "lat": 18.13, "lng": -96.86},
    {"n": "Kazumura Cave (Hawaii, USA)", "lat": 19.56, "lng": -155.07},
    {"n": "Cueva del Viento (Teneriffa, Spanien)", "lat": 28.38, "lng": -16.52},
    {"n": "Sarawak Chamber (Malaysia)", "lat": 4.05, "lng": 114.82},
]

# --- geo_gletscher (Ziel: 40+) ---
gletscher_new = [
    {"n": "Vatnajökull (Island)", "lat": 64.50, "lng": -16.80},
    {"n": "Jostedalsbreen (Norwegen)", "lat": 61.68, "lng": 7.00},
    {"n": "Svalbard-Gletscher (Spitzbergen, Norwegen)", "lat": 78.63, "lng": 16.00},
    {"n": "Malaspina-Gletscher (Alaska, USA)", "lat": 59.87, "lng": -140.52},
    {"n": "Hubbard-Gletscher (Alaska, USA)", "lat": 60.00, "lng": -139.50},
    {"n": "Columbia-Gletscher (Alaska, USA)", "lat": 61.10, "lng": -147.00},
    {"n": "Mer de Glace (Frankreich)", "lat": 45.90, "lng": 6.94},
    {"n": "Gorner-Gletscher (Schweiz)", "lat": 45.97, "lng": 7.78},
    {"n": "Rhône-Gletscher (Schweiz)", "lat": 46.58, "lng": 8.38},
    {"n": "Furtwängler-Gletscher (Kilimanjaro, Tansania)", "lat": -3.07, "lng": 37.35},
    {"n": "Quelccaya-Eiskappe (Peru)", "lat": -13.93, "lng": -70.83},
    {"n": "Batura-Gletscher (Pakistan)", "lat": 36.52, "lng": 74.52},
    {"n": "Fedchenko-Gletscher (Tadschikistan)", "lat": 38.80, "lng": 72.18},
    {"n": "Inylchek-Gletscher (Kirgisistan)", "lat": 42.13, "lng": 80.15},
    {"n": "Siachen-Gletscher (Pakistan/Indien)", "lat": 35.42, "lng": 76.87},
    {"n": "Gangotri-Gletscher (Uttarakhand, Indien)", "lat": 30.93, "lng": 79.07},
    {"n": "Zemu-Gletscher (Sikkim, Indien)", "lat": 27.72, "lng": 88.52},
    {"n": "Baltoro-Gletscher (Pakistan)", "lat": 35.70, "lng": 76.52},
    {"n": "Biafo-Gletscher (Pakistan)", "lat": 35.98, "lng": 75.70},
    {"n": "Fox-Gletscher (Neuseeland)", "lat": -43.47, "lng": 170.19},
    {"n": "Tasman-Gletscher (Neuseeland)", "lat": -43.59, "lng": 170.15},
    {"n": "Upsala-Gletscher (Argentinien)", "lat": -49.87, "lng": -73.35},
    {"n": "Grey-Gletscher (Chile)", "lat": -51.02, "lng": -73.25},
    {"n": "Pasterze (Österreich)", "lat": 47.09, "lng": 12.71},
    {"n": "Mer de Glace — Eisgrotte (Chamonix, Frankreich)", "lat": 45.91, "lng": 6.93},
    {"n": "Athabasca-Gletscher (Alberta, Kanada)", "lat": 52.19, "lng": -117.25},
    {"n": "Saskatchewan-Gletscher (Kanada)", "lat": 52.14, "lng": -117.29},
    {"n": "Emmons-Gletscher (Mount Rainier, USA)", "lat": 46.87, "lng": -121.64},
    {"n": "Khumbu-Gletscher (Nepal)", "lat": 27.97, "lng": 86.83},
    {"n": "Ngozumpa-Gletscher (Nepal)", "lat": 27.96, "lng": 86.64},
    {"n": "Rongbuk-Gletscher (Tibet, China)", "lat": 28.03, "lng": 86.86},
    {"n": "Darwin-Gletscher (Antarktis)", "lat": -79.87, "lng": 156.30},
    {"n": "Sermeq Kujalleq / Jakobshavn (Grönland)", "lat": 69.16, "lng": -49.50},
    {"n": "Helheim-Gletscher (Grönland)", "lat": 66.35, "lng": -37.97},
    {"n": "Pine Island Gletscher (Antarktis)", "lat": -75.17, "lng": -100.43},
    {"n": "Thwaites-Gletscher (Antarktis)", "lat": -75.50, "lng": -107.00},
]

# --- geo_wuesten (Ziel: 40+) ---
wuesten_new = [
    {"n": "Rub al-Chali (Saudi-Arabien)", "lat": 19.00, "lng": 50.00},
    {"n": "Karakum (Turkmenistan)", "lat": 40.00, "lng": 58.00},
    {"n": "Kyzylkum (Usbekistan/Kasachstan)", "lat": 41.00, "lng": 63.00},
    {"n": "Tharparkar-Wüste (Pakistan)", "lat": 25.00, "lng": 70.00},
    {"n": "Thar-Wüste (Indien/Pakistan)", "lat": 27.00, "lng": 71.00},
    {"n": "Taklamakan (Xinjiang, China)", "lat": 38.00, "lng": 83.00},
    {"n": "Gobi (Mongolei/China)", "lat": 42.59, "lng": 103.43},
    {"n": "Patagonia Wüste (Argentinien)", "lat": -42.00, "lng": -67.50},
    {"n": "Sechura-Wüste (Peru)", "lat": -5.93, "lng": -80.70},
    {"n": "Monte-Wüste (Argentinien)", "lat": -33.00, "lng": -67.00},
    {"n": "Chihuahua-Wüste (Mexiko/USA)", "lat": 30.00, "lng": -106.00},
    {"n": "Great Basin Desert (USA)", "lat": 40.00, "lng": -116.50},
    {"n": "Mojave-Wüste (Kalifornien, USA)", "lat": 35.08, "lng": -115.47},
    {"n": "Sonora-Wüste (Mexiko/USA)", "lat": 30.00, "lng": -111.60},
    {"n": "Arabische Wüste (Ägypten)", "lat": 26.40, "lng": 31.60},
    {"n": "Libyen-Wüste (Libyen/Ägypten)", "lat": 25.00, "lng": 25.00},
    {"n": "Nubian Desert (Sudan)", "lat": 20.00, "lng": 33.00},
    {"n": "Chalbi-Wüste (Kenia)", "lat": 3.00, "lng": 37.50},
    {"n": "Danakil-Wüste (Äthiopien)", "lat": 13.50, "lng": 40.80},
    {"n": "Namib (Namibia)", "lat": -23.58, "lng": 15.08},
    {"n": "Kalahari (Botswana)", "lat": -22.00, "lng": 22.00},
    {"n": "Great Victoria Desert (Australien)", "lat": -29.00, "lng": 127.00},
    {"n": "Great Sandy Desert (Australien)", "lat": -21.00, "lng": 124.00},
    {"n": "Simpson Desert (Australien)", "lat": -25.00, "lng": 137.00},
    {"n": "Gibson Desert (Australien)", "lat": -24.00, "lng": 124.00},
    {"n": "Tanami Desert (Australien)", "lat": -20.00, "lng": 132.00},
    {"n": "Puna de Atacama (Argentinien/Chile)", "lat": -24.00, "lng": -67.50},
    {"n": "Dasht-e Kavir (Iran)", "lat": 34.50, "lng": 54.00},
    {"n": "Dasht-e Lut (Iran)", "lat": 30.50, "lng": 58.50},
    {"n": "Syrian Desert (Syrien/Jordanien/Irak)", "lat": 33.00, "lng": 38.50},
    {"n": "Negev-Wüste (Israel)", "lat": 30.65, "lng": 34.90},
    {"n": "Wahiba Sands (Oman)", "lat": 22.30, "lng": 58.80},
    {"n": "Kara Kum Kanal-Region (Turkmenistan)", "lat": 37.50, "lng": 60.00},
]

# --- geo_felsformationen (Ziel: 40+) ---
fels_new = [
    {"n": "Devils Tower (Wyoming, USA)", "lat": 44.59, "lng": -104.72},
    {"n": "Uluru / Ayers Rock (Northern Territory, Australien)", "lat": -25.34, "lng": 131.04},
    {"n": "Kata Tjuta / Die Olgas (Australien)", "lat": -25.30, "lng": 130.74},
    {"n": "Twelve Apostles (Victoria, Australien)", "lat": -38.66, "lng": 143.10},
    {"n": "Giant's Causeway (Nordirland)", "lat": 55.24, "lng": -6.51},
    {"n": "Fingal's Cave (Staffa, Schottland)", "lat": 56.43, "lng": -6.34},
    {"n": "Meteora (Thessalien, Griechenland)", "lat": 39.72, "lng": 21.63},
    {"n": "Cappadocia Feenschornsteine (Türkei)", "lat": 38.64, "lng": 34.85},
    {"n": "Nambung Pinnacles (Westaustralien)", "lat": -30.60, "lng": 115.16},
    {"n": "Bryce Canyon Hoodoos (Utah, USA)", "lat": 37.64, "lng": -112.17},
    {"n": "White Desert / Farafra (Ägypten)", "lat": 27.15, "lng": 27.97},
    {"n": "Zhangjiajie Sandsteinsäulen (Hunan, China)", "lat": 29.32, "lng": 110.44},
    {"n": "Mount Roraima (Tepui, Venezuela)", "lat": 5.14, "lng": -60.76},
    {"n": "El Capitan (Yosemite, USA)", "lat": 37.73, "lng": -119.64},
    {"n": "Half Dome (Yosemite, USA)", "lat": 37.75, "lng": -119.53},
    {"n": "Wave Rock (Westaustralien)", "lat": -32.44, "lng": 118.90},
    {"n": "Bungle Bungle Range (Purnululu, Australien)", "lat": -17.47, "lng": 128.41},
    {"n": "Monument Valley Buttes (Arizona/Utah, USA)", "lat": 36.98, "lng": -110.09},
    {"n": "Delicate Arch (Utah, USA)", "lat": 38.74, "lng": -109.50},
    {"n": "Antelope Canyon (Arizona, USA)", "lat": 36.86, "lng": -111.37},
    {"n": "Vermilion Cliffs (Arizona, USA)", "lat": 36.77, "lng": -111.97},
    {"n": "Trona Pinnacles (Kalifornien, USA)", "lat": 35.61, "lng": -117.37},
    {"n": "Moai auf Easter Island (Chile)", "lat": -27.12, "lng": -109.28},
    {"n": "Preikestolen (Norwegen)", "lat": 58.99, "lng": 6.19},
    {"n": "Kjeragbolten (Norwegen)", "lat": 59.03, "lng": 6.58},
    {"n": "Trolltunga (Norwegen)", "lat": 60.12, "lng": 6.74},
    {"n": "Tre Cime di Lavaredo (Dolomiten, Italien)", "lat": 46.62, "lng": 12.30},
    {"n": "Aiguille du Dru (Frankreich)", "lat": 45.93, "lng": 6.95},
    {"n": "Dolomiti di Brenta (Italien)", "lat": 46.17, "lng": 10.90},
    {"n": "Spitzkoppe (Namibia)", "lat": -21.83, "lng": 15.17},
    {"n": "Brandberg (Namibia)", "lat": -21.13, "lng": 14.57},
    {"n": "Purnululu — Bungle Bungles (Australien)", "lat": -17.48, "lng": 128.38},
    {"n": "Sigiriya Felsenfestung (Sri Lanka)", "lat": 7.95, "lng": 80.76},
    {"n": "Tianmen Mountain (Hunan, China)", "lat": 29.14, "lng": 110.48},
    {"n": "Huangshan Yellow Mountains (Anhui, China)", "lat": 30.14, "lng": 118.17},
    {"n": "Los Glaciares — Torres del Paine (Chile)", "lat": -50.94, "lng": -73.07},
    {"n": "Fitz Roy (Patagonien, Argentinien)", "lat": -49.27, "lng": -72.94},
]

# --- geo_canyons (Ziel: 40+) ---
canyons_new = [
    {"n": "Grand Canyon (Arizona, USA)", "lat": 36.06, "lng": -112.14},
    {"n": "Antelope Canyon (Arizona, USA)", "lat": 36.86, "lng": -111.37},
    {"n": "Zion Canyon (Utah, USA)", "lat": 37.22, "lng": -112.99},
    {"n": "Bryce Canyon (Utah, USA)", "lat": 37.64, "lng": -112.17},
    {"n": "Coyote Buttes / The Wave (Arizona, USA)", "lat": 37.01, "lng": -112.01},
    {"n": "Palo Duro Canyon (Texas, USA)", "lat": 34.87, "lng": -101.67},
    {"n": "Black Canyon of the Gunnison (Colorado, USA)", "lat": 38.57, "lng": -107.72},
    {"n": "Kings Canyon (Kalifornien, USA)", "lat": 36.86, "lng": -118.65},
    {"n": "Yarlung Tsangpo Grand Canyon (Tibet, China)", "lat": 29.61, "lng": 94.88},
    {"n": "Cotahuasi Canyon (Peru)", "lat": -15.22, "lng": -72.89},
    {"n": "Colca Canyon (Peru)", "lat": -15.63, "lng": -71.97},
    {"n": "Tiger Leaping Gorge (Yunnan, China)", "lat": 27.21, "lng": 100.16},
    {"n": "Three Gorges (Yangtze, China)", "lat": 30.83, "lng": 110.99},
    {"n": "Verdon-Schlucht (Frankreich)", "lat": 43.72, "lng": 6.34},
    {"n": "Wadi Rum (Jordanien)", "lat": 29.57, "lng": 35.42},
    {"n": "Wadi Mujib (Jordanien)", "lat": 31.47, "lng": 35.61},
    {"n": "Sesriem Canyon (Namibia)", "lat": -24.53, "lng": 15.77},
    {"n": "Fish River Canyon (Namibia)", "lat": -27.68, "lng": 17.59},
    {"n": "Blue Nile Gorge (Äthiopien)", "lat": 10.13, "lng": 37.43},
    {"n": "Royal Gorge (Colorado, USA)", "lat": 38.44, "lng": -105.36},
    {"n": "Copper Canyon (Chihuahua, Mexiko)", "lat": 27.55, "lng": -107.65},
    {"n": "Sumidero Canyon (Chiapas, Mexiko)", "lat": 16.83, "lng": -93.13},
    {"n": "Cañón del Colca (Peru)", "lat": -15.63, "lng": -71.97},
    {"n": "Siq Schlucht (Petra, Jordanien)", "lat": 30.33, "lng": 35.44},
    {"n": "Samaria Gorge (Kreta, Griechenland)", "lat": 35.27, "lng": 23.97},
    {"n": "Aareschlucht (Schweiz)", "lat": 46.71, "lng": 8.20},
    {"n": "Vintgar Gorge (Slowenien)", "lat": 46.38, "lng": 14.03},
    {"n": "Pancake Rocks — Punakaiki (Neuseeland)", "lat": -42.11, "lng": 171.33},
    {"n": "Geirangerfjord (Norwegen)", "lat": 62.10, "lng": 7.20},
    {"n": "Nærøyfjord (Norwegen)", "lat": 60.87, "lng": 6.67},
    {"n": "Byfjord — Bergen (Norwegen)", "lat": 60.39, "lng": 5.27},
    {"n": "Iron Gates (Donau, Serbien/Rumänien)", "lat": 44.68, "lng": 22.50},
]

# --- geo_minen_bohrungen (Ziel: 40+) ---
minen_new = [
    {"n": "Bingham Canyon Mine (Utah, USA)", "lat": 40.52, "lng": -112.15},
    {"n": "Chuquicamata Kupfermine (Chile)", "lat": -22.30, "lng": -68.93},
    {"n": "Escondida Mine (Chile)", "lat": -24.27, "lng": -69.07},
    {"n": "Grasberg Mine (Papua, Indonesien)", "lat": -4.05, "lng": 137.12},
    {"n": "Cerro Rico Silbermine (Potosí, Bolivien)", "lat": -19.59, "lng": -65.74},
    {"n": "Homestake Gold Mine (South Dakota, USA)", "lat": 44.35, "lng": -103.73},
    {"n": "Witwatersrand Goldfeld (Südafrika)", "lat": -26.18, "lng": 28.04},
    {"n": "Mirny Diamond Mine (Sibirien, Russland)", "lat": 62.53, "lng": 113.96},
    {"n": "Jwaneng Diamond Mine (Botswana)", "lat": -24.60, "lng": 24.73},
    {"n": "Argyle Diamond Mine (Australien)", "lat": -16.71, "lng": 128.39},
    {"n": "Mount Whaleback Iron Ore (Australien)", "lat": -23.36, "lng": 119.68},
    {"n": "Carajás Iron Mine (Pará, Brasilien)", "lat": -6.08, "lng": -50.16},
    {"n": "OK Tedi Gold/Kupfermine (Papua-Neuguinea)", "lat": -5.18, "lng": 141.17},
    {"n": "El Teniente Kupfermine (Chile)", "lat": -34.10, "lng": -70.55},
    {"n": "Highland Valley Copper (British Columbia, Kanada)", "lat": 50.48, "lng": -120.76},
    {"n": "Sullivan Mine (British Columbia, Kanada)", "lat": 49.52, "lng": -115.78},
    {"n": "Norilsk Bergbau (Russland)", "lat": 69.34, "lng": 88.20},
    {"n": "Kimberley Diamond Mine (Südafrika)", "lat": -28.74, "lng": 24.76},
    {"n": "Premier Diamond Mine (Südafrika)", "lat": -25.67, "lng": 28.44},
    {"n": "Driefontein Gold Mine (Südafrika)", "lat": -26.38, "lng": 26.36},
    {"n": "Kennecott Copper Mine (Alaska, USA)", "lat": 61.49, "lng": -142.90},
    {"n": "Morenci Copper Mine (Arizona, USA)", "lat": 33.09, "lng": -109.36},
    {"n": "Collahuasi Kupfermine (Chile)", "lat": -20.98, "lng": -68.72},
    {"n": "Antamina Polymetall (Peru)", "lat": -9.53, "lng": -77.05},
    {"n": "Toquepala Kupfermine (Peru)", "lat": -17.24, "lng": -70.62},
    {"n": "IODP Site 1256 — Tiefseeforschungsbohrung (Pazifik)", "lat": 6.74, "lng": -91.93},
    {"n": "Mohole Pilot (Guadalupe, Mexiko)", "lat": 28.04, "lng": -117.49},
    {"n": "Kalgoorlie Super Pit (Australien)", "lat": -30.77, "lng": 121.50},
    {"n": "Mount Isa Mine (Queensland, Australien)", "lat": -20.73, "lng": 139.49},
    {"n": "Olympic Dam (Südaustralien)", "lat": -30.44, "lng": 136.89},
    {"n": "Yilgarn Kraton Goldfelder (Australien)", "lat": -30.00, "lng": 121.00},
    {"n": "Pechenganikel (Russland)", "lat": 69.56, "lng": 30.29},
    {"n": "Zinkgruvan (Schweden)", "lat": 58.81, "lng": 15.09},
]

n_vul = extend_key(pin, "geo_vulkane", vulkane_new)
n_hoe = extend_key(pin, "geo_hoehlensysteme", hoehlen_new)
n_gla = extend_key(pin, "geo_gletscher", gletscher_new)
n_wue = extend_key(pin, "geo_wuesten", wuesten_new)
n_fel = extend_key(pin, "geo_felsformationen", fels_new)
n_can = extend_key(pin, "geo_canyons", canyons_new)
n_min = extend_key(pin, "geo_minen_bohrungen", minen_new)

jsave("geo_pin.json", pin)
print(f"  [OK] pin/vulkane: +{n_vul}")
print(f"  [OK] pin/hoehlensysteme: +{n_hoe}")
print(f"  [OK] pin/gletscher: +{n_gla}")
print(f"  [OK] pin/wuesten: +{n_wue}")
print(f"  [OK] pin/felsformationen: +{n_fel}")
print(f"  [OK] pin/canyons: +{n_can}")
print(f"  [OK] pin/minen_bohrungen: +{n_min}")

# ============================================================
# geo_hl.json
# ============================================================
hl = jload("geo_hl.json")

# --- geo_hoehlen_laenge (km) —  Ziel: 45+ ---
hoehlen_laenge_new = [
    {"name": "Optymistychna Cave (Ukraine)", "val": 257},
    {"name": "Fisher Ridge Cave System (Kentucky, USA)", "val": 222},
    {"name": "Lechuguilla Cave (New Mexico, USA)", "val": 241},
    {"name": "Siebenhengste-Hohgant Cave (Schweiz)", "val": 157},
    {"name": "Clearwater Cave System (Malaysia)", "val": 224},
    {"name": "Hölloch (Schweiz)", "val": 200},
    {"name": "Friars Hole Cave System (West Virginia, USA)", "val": 78},
    {"name": "Kazumura Cave (Hawaii, USA)", "val": 65},
    {"name": "Son Doong Cave (Vietnam)", "val": 9},
    {"name": "Sistema Ox Bel Ha (Mexiko)", "val": 368},
    {"name": "Wind Cave (South Dakota, USA)", "val": 246},
    {"name": "Cueva de Villa Luz (Mexiko)", "val": 3},
    {"name": "Eisriesenwelt (Österreich)", "val": 42},
    {"name": "Škocjan-Höhlen (Slowenien)", "val": 6},
    {"name": "Veryovkina Cave (Abchasien)", "val": 12},
    {"name": "Krubera Cave (Georgien)", "val": 13},
    {"name": "Blue Spring Cave (Tennessee, USA)", "val": 63},
    {"name": "Lechuguilla — seitl. Äste (USA)", "val": 241},
    {"name": "Tham Khoun Xe (Laos)", "val": 7},
    {"name": "Gouffre Mirolda (Frankreich)", "val": 14},
    {"name": "Snezhnaya Cave (Abchasien)", "val": 19},
    {"name": "Cueva del Agua (Mexiko)", "val": 27},
    {"name": "Mulu — Clearwater (Malaysia)", "val": 109},
    {"name": "Sarawak Chamber (Malaysia)", "val": 0.7},
    {"name": "Waitomo (Neuseeland)", "val": 3},
    {"name": "Reed Flute Cave (China)", "val": 0.24},
    {"name": "Sistema Huautla (Mexiko)", "val": 77},
    {"name": "Cueva de los Cristales (Mexiko)", "val": 1},
    {"name": "Movile Cave (Rumänien)", "val": 3},
    {"name": "Grotte de Lascaux (Frankreich)", "val": 0.2},
    {"name": "Postojna Cave (Slowenien)", "val": 27},
    {"name": "Mururoa Atoll Tunnel (Polynesien)", "val": 2},
    {"name": "Cave of Altamira (Spanien)", "val": 0.27},
    {"name": "Deer Cave (Malaysia)", "val": 2},
    {"name": "Cueva de las Espadas (Mexiko)", "val": 0.5},
    {"name": "Cango Caves (Südafrika)", "val": 4},
    {"name": "Jenolan Caves (Australien)", "val": 40},
    {"name": "Naracoorte Caves (Australien)", "val": 3},
]

# --- geo_gesteins_alter (Mio. Jahre) — Ziel: 45+ ---
gesteins_alter_new = [
    {"name": "Jack Hills Zirkon (Australien)", "val": 4400},
    {"name": "Acasta Gneiss (Kanada)", "val": 4030},
    {"name": "Isua Grünsteingürtel (Grönland)", "val": 3800},
    {"name": "Nuvvuagittuq Grünstein (Kanada)", "val": 3770},
    {"name": "Napier Complex (Antarktis)", "val": 3850},
    {"name": "Kaapvaal Kraton (Südafrika)", "val": 3500},
    {"name": "Superior Province (Kanada)", "val": 2700},
    {"name": "Pilbara Kraton (Australien)", "val": 3500},
    {"name": "Huronian Supergroup (Kanada)", "val": 2400},
    {"name": "Granit Rapakivi (Finnland)", "val": 1650},
    {"name": "Lewisian Complex (Schottland)", "val": 2900},
    {"name": "Penokean Orogen (USA)", "val": 1850},
    {"name": "Rheinisches Schiefergebirge Schiefer (Deutschland)", "val": 380},
    {"name": "Marmor von Carrara (Italien)", "val": 200},
    {"name": "Schwarzwald Granit (Deutschland)", "val": 330},
    {"name": "Muschelkalk (Mitteleuropa)", "val": 240},
    {"name": "Oolith-Kalk Jura (Deutschland)", "val": 155},
    {"name": "Buntsandstein (Europa)", "val": 245},
    {"name": "Kreide (Dover, England)", "val": 85},
    {"name": "Lias Ölschiefer (Deutschland)", "val": 195},
    {"name": "Deccan Traps (Indien)", "val": 66},
    {"name": "Columbia River Basalt (USA)", "val": 17},
    {"name": "Hawaiian Islands Basalt (USA)", "val": 5},
    {"name": "Eifel-Vulkanismus (Deutschland)", "val": 0.01},
    {"name": "Mount St. Helens Tephra (USA)", "val": 0.00004},
    {"name": "Krakatau-Bims (Indonesien)", "val": 0.00014},
    {"name": "Toba-Tuff (Sumatra)", "val": 0.074},
    {"name": "Yellowstone Rhyolith (USA)", "val": 2.1},
    {"name": "Bishop Tuff (Kalifornien, USA)", "val": 0.76},
    {"name": "Ontong Java Plateau (Pazifik)", "val": 122},
    {"name": "Kambrium-Sandstein (Schweden)", "val": 520},
    {"name": "Ordovizium-Kalk (Estland)", "val": 450},
    {"name": "Silur-Riff-Kalk (Gotland)", "val": 430},
    {"name": "Devon-Riff (Australien)", "val": 380},
    {"name": "Karbon-Kohle (Wales, Großbritannien)", "val": 310},
    {"name": "Perm-Rotliegend (Deutschland)", "val": 270},
    {"name": "Trias-Dolomit (Alpen)", "val": 220},
    {"name": "Jura-Granit (Frankreich)", "val": 160},
    {"name": "Tertiärer Sandstein (Paris Becken)", "val": 45},
    {"name": "Quartärer Löss (Deutschland)", "val": 0.02},
]

# --- geo_schluchten_tiefe (Meter) — Ziel: 40+ ---
schluchten_tiefe_new = [
    {"name": "Yarlung Tsangpo Grand Canyon (Tibet)", "val": 6009},
    {"name": "Cotahuasi Canyon (Peru)", "val": 3535},
    {"name": "Colca Canyon (Peru)", "val": 3400},
    {"name": "Grand Canyon (Arizona, USA)", "val": 1800},
    {"name": "Tara River Canyon (Montenegro)", "val": 1300},
    {"name": "Verdon-Schlucht (Frankreich)", "val": 700},
    {"name": "Tiger Leaping Gorge (China)", "val": 3790},
    {"name": "Kali Gandaki Gorge (Nepal)", "val": 5571},
    {"name": "Indus Gorge (Pakistan)", "val": 5200},
    {"name": "Barranca del Cobre (Mexiko)", "val": 1800},
    {"name": "Blyde River Canyon (Südafrika)", "val": 750},
    {"name": "Fish River Canyon (Namibia)", "val": 549},
    {"name": "Hell's Canyon (Idaho, USA)", "val": 2436},
    {"name": "Kings Canyon (Californien, USA)", "val": 1500},
    {"name": "Royal Gorge (Colorado, USA)", "val": 300},
    {"name": "Black Canyon (Colorado, USA)", "val": 825},
    {"name": "Samaria Gorge (Kreta)", "val": 300},
    {"name": "Geirangerfjord Schlucht (Norwegen)", "val": 800},
    {"name": "Zion Canyon (Utah, USA)", "val": 790},
    {"name": "Waimea Canyon (Kauai, USA)", "val": 900},
    {"name": "Lower Antelope Canyon (Arizona, USA)", "val": 37},
    {"name": "Stubaital Schlucht (Österreich)", "val": 200},
    {"name": "Vintgar Gorge (Slowenien)", "val": 100},
    {"name": "Aareschlucht (Schweiz)", "val": 50},
    {"name": "Partnachklamm (Bayern, Deutschland)", "val": 80},
    {"name": "Breitachklamm (Bayern, Deutschland)", "val": 100},
    {"name": "Wadi Mujib (Jordanien)", "val": 900},
    {"name": "Wadi Rum (Jordanien)", "val": 500},
    {"name": "Iron Gates — Donau (Serbien)", "val": 300},
    {"name": "Sumidero Canyon (Mexiko)", "val": 1000},
    {"name": "Canyonlands Maze (Utah, USA)", "val": 600},
    {"name": "Copper Canyon (Mexiko)", "val": 1879},
    {"name": "Siq Schlucht (Petra, Jordanien)", "val": 80},
    {"name": "Provence Calanques (Frankreich)", "val": 400},
]

# --- geo_bohrtiefe (Meter) — Ziel: 40+ ---
bohrtiefe_new = [
    {"name": "SG-3 Kontinentale Tiefbohrung Russland (ICDP)", "val": 12262},
    {"name": "Bertha Rogers No. 1 (Oklahoma, USA)", "val": 9583},
    {"name": "Z-42 (Schachtanlage, Russland)", "val": 9100},
    {"name": "Badami Bohrung (Indien)", "val": 7926},
    {"name": "IODP Site 1256 Ozeanische Kruste (Pazifik)", "val": 1507},
    {"name": "Byrd Ice Core (Antarktis)", "val": 2164},
    {"name": "Vostok Ice Core (Antarktis)", "val": 3623},
    {"name": "EPICA Dome C (Antarktis)", "val": 3270},
    {"name": "NEEM Greenland Core (Grönland)", "val": 2537},
    {"name": "East Rand Mine (Südafrika)", "val": 3585},
    {"name": "Mponeng Mine (Südafrika)", "val": 4000},
    {"name": "TauTona Mine (Südafrika)", "val": 3900},
    {"name": "Savuka Mine (Südafrika)", "val": 3773},
    {"name": "Al Shaheen Oil Well (Katar)", "val": 12289},
    {"name": "Chayvo Well OP-11 (Sakhalin, Russland)", "val": 12376},
    {"name": "Maersk Oil BD-04A (Dänemark)", "val": 12290},
    {"name": "BD-04A Tiefbohrung Nordsee (Dänemark)", "val": 12000},
    {"name": "Attaka-Bohrung (Kalimantan, Indonesien)", "val": 6700},
    {"name": "Lena-Bohrung Sibirien (Russland)", "val": 7000},
    {"name": "Deep Water Horizon — Bohrloch (Golf von Mexiko)", "val": 5608},
    {"name": "Perdido Host Platform (Gulf of Mexico)", "val": 2438},
    {"name": "Jubilee Field Bohrung (Ghana)", "val": 1525},
    {"name": "Prelude FLNG — Bohrung (Australien)", "val": 1500},
    {"name": "Urengoy Gasfeld Bohrung (Russland)", "val": 7000},
    {"name": "Kashagan Ölfeld (Kasachstan)", "val": 5200},
    {"name": "Martin Linge — Nordsee (Norwegen)", "val": 3050},
    {"name": "Troll Plattform (Norwegen)", "val": 303},
    {"name": "Snøhvit Gasfeld (Norwegen)", "val": 2600},
    {"name": "Hassi R'Mel (Algerien)", "val": 3900},
    {"name": "Ghawar Ölfeld (Saudi-Arabien)", "val": 3050},
    {"name": "Rumaila (Irak)", "val": 3800},
    {"name": "Spindletop (Texas, USA)", "val": 1139},
    {"name": "Echo Mine (Ontario, Kanada)", "val": 3600},
    {"name": "Lucky Friday Mine (Idaho, USA)", "val": 2100},
    {"name": "Homestake Gold Mine (South Dakota, USA)", "val": 2440},
    {"name": "Creighton Mine (Ontario, Kanada)", "val": 2440},
    {"name": "Kidd Creek Mine (Ontario, Kanada)", "val": 3105},
]

# --- geo_gletscher_volumen (km³) — Ziel: 40+ ---
gletscher_vol_new = [
    {"name": "Antarktischer Eisschild (gesamt)", "val": 26500000},
    {"name": "Grönländischer Eisschild", "val": 2850000},
    {"name": "Vatnajökull (Island)", "val": 3100},
    {"name": "Svalbard-Gletscher", "val": 6700},
    {"name": "Franz-Josef-Land Eiskappe (Russland)", "val": 2410},
    {"name": "Novaya Zemlya Eiskappe (Russland)", "val": 2900},
    {"name": "Severnaya Zemlya (Russland)", "val": 3890},
    {"name": "Devon Island Ice Cap (Kanada)", "val": 3980},
    {"name": "Ellesmere Island Gletscher (Kanada)", "val": 83500},
    {"name": "Baffin Island Gletscher (Kanada)", "val": 40000},
    {"name": "Penny Ice Cap (Kanada)", "val": 6000},
    {"name": "Barnes Ice Cap (Kanada)", "val": 7350},
    {"name": "St. Elias Mountains (Alaska/Kanada)", "val": 84000},
    {"name": "Columbia Icefield (Kanada)", "val": 213},
    {"name": "Aletschgletscher (Schweiz)", "val": 68},
    {"name": "Gorner-Gletscher (Schweiz)", "val": 17},
    {"name": "Mer de Glace (Frankreich)", "val": 12},
    {"name": "Jostedalsbreen (Norwegen)", "val": 277},
    {"name": "Folgefonna (Norwegen)", "val": 209},
    {"name": "Austfonna (Svalbard)", "val": 1628},
    {"name": "Fedchenko-Gletscher (Tadschikistan)", "val": 144},
    {"name": "Inylchek-Gletscher (Kirgisistan)", "val": 148},
    {"name": "Siachen-Gletscher (Pakistan)", "val": 218},
    {"name": "Baltoro-Gletscher (Pakistan)", "val": 76},
    {"name": "Gangotri-Gletscher (Indien)", "val": 27},
    {"name": "Quelccaya Ice Cap (Peru)", "val": 44},
    {"name": "Perito Moreno (Argentinien)", "val": 30},
    {"name": "Hielo Patagónico Sur (Chile/Argentinien)", "val": 12363},
    {"name": "Hielo Patagónico Norte (Chile)", "val": 3953},
    {"name": "Furtwängler (Kilimanjaro, Tansania)", "val": 0.1},
    {"name": "Lewis Gletscher (Mount Kenya)", "val": 0.02},
    {"name": "Khumbu-Gletscher (Nepal)", "val": 5},
    {"name": "Ngozumpa-Gletscher (Nepal)", "val": 7},
    {"name": "Rongbuk-Gletscher (Tibet)", "val": 5},
    {"name": "Malaspina-Gletscher (Alaska)", "val": 700},
    {"name": "Hubbard-Gletscher (Alaska)", "val": 243},
    {"name": "Pine Island Gletscher (Antarktis)", "val": 180000},
    {"name": "Thwaites-Gletscher (Antarktis)", "val": 192000},
    {"name": "Ross Schelfeis (Antarktis)", "val": 228000},
]

n_hl_hoehlen = extend_key(hl, "geo_hoehlen_laenge", hoehlen_laenge_new, name_field="name")
n_hl_alter = extend_key(hl, "geo_gesteins_alter", gesteins_alter_new, name_field="name")
n_hl_schluchten = extend_key(hl, "geo_schluchten_tiefe", schluchten_tiefe_new, name_field="name")
n_hl_bohrtiefe = extend_key(hl, "geo_bohrtiefe", bohrtiefe_new, name_field="name")
n_hl_glvol = extend_key(hl, "geo_gletscher_volumen", gletscher_vol_new, name_field="name")

jsave("geo_hl.json", hl)
print(f"  [OK] hl/hoehlen_laenge: +{n_hl_hoehlen}")
print(f"  [OK] hl/gesteins_alter: +{n_hl_alter}")
print(f"  [OK] hl/schluchten_tiefe: +{n_hl_schluchten}")
print(f"  [OK] hl/bohrtiefe: +{n_hl_bohrtiefe}")
print(f"  [OK] hl/gletscher_volumen: +{n_hl_glvol}")

# ============================================================
# geo_match.json
# ============================================================
match = jload("geo_match.json")

# --- geo_vulkan_land — Ziel: 60+ ---
vulkan_land_new = [
    {"n": "Merapi", "c": "Indonesien"},
    {"n": "Krakatau", "c": "Indonesien"},
    {"n": "Tambora", "c": "Indonesien"},
    {"n": "Semeru", "c": "Indonesien"},
    {"n": "Sinabung", "c": "Indonesien"},
    {"n": "Bromo", "c": "Indonesien"},
    {"n": "Taal", "c": "Philippinen"},
    {"n": "Mayon", "c": "Philippinen"},
    {"n": "Pinatubo", "c": "Philippinen"},
    {"n": "Popocatépetl", "c": "Mexiko"},
    {"n": "Colima", "c": "Mexiko"},
    {"n": "Paricutin", "c": "Mexiko"},
    {"n": "Mount St. Helens", "c": "USA"},
    {"n": "Mount Rainier", "c": "USA"},
    {"n": "Mauna Kea", "c": "USA (Hawaii)"},
    {"n": "Yellowstone", "c": "USA"},
    {"n": "Cotopaxi", "c": "Ecuador"},
    {"n": "Tungurahua", "c": "Ecuador"},
    {"n": "Chimborazo", "c": "Ecuador"},
    {"n": "Villarrica", "c": "Chile"},
    {"n": "Llaima", "c": "Chile"},
    {"n": "Nevado del Ruiz", "c": "Kolumbien"},
    {"n": "Galeras", "c": "Kolumbien"},
    {"n": "Arenal", "c": "Costa Rica"},
    {"n": "Poas", "c": "Costa Rica"},
    {"n": "Soufrière Hills", "c": "Montserrat (GB)"},
    {"n": "La Soufrière", "c": "Saint Vincent"},
    {"n": "Cumbre Vieja", "c": "Spanien (La Palma)"},
    {"n": "Teide", "c": "Spanien (Teneriffa)"},
    {"n": "Stromboli", "c": "Italien"},
    {"n": "Campi Flegrei", "c": "Italien"},
    {"n": "Piton de la Fournaise", "c": "Frankreich (Réunion)"},
    {"n": "Hekla", "c": "Island"},
    {"n": "Grímsvötn", "c": "Island"},
    {"n": "Bardarbunga", "c": "Island"},
    {"n": "Eyjafjallajökull", "c": "Island"},
    {"n": "Bezymianny", "c": "Russland"},
    {"n": "Klyuchevskaya Sopka", "c": "Russland"},
    {"n": "Shiveluch", "c": "Russland"},
    {"n": "Sakurajima", "c": "Japan"},
    {"n": "Asama", "c": "Japan"},
    {"n": "Unzen", "c": "Japan"},
    {"n": "Mount Ruapehu", "c": "Neuseeland"},
    {"n": "White Island / Whakaari", "c": "Neuseeland"},
    {"n": "Nyiragongo", "c": "DR Kongo"},
    {"n": "Erta Ale", "c": "Äthiopien"},
    {"n": "Mount Erebus", "c": "Antarktis"},
    {"n": "Piton des Neiges", "c": "Frankreich (Réunion)"},
    {"n": "Tavurvur", "c": "Papua-Neuguinea"},
    {"n": "Ulawun", "c": "Papua-Neuguinea"},
]

# --- geo_berg_gebirge — Ziel: 55+ ---
berg_gebirge_new = [
    {"n": "Mont Blanc", "c": "Alpen"},
    {"n": "Monte Rosa", "c": "Alpen"},
    {"n": "Matterhorn", "c": "Alpen"},
    {"n": "Eiger", "c": "Alpen"},
    {"n": "Jungfrau", "c": "Alpen"},
    {"n": "Großglockner", "c": "Alpen"},
    {"n": "Ortler", "c": "Alpen"},
    {"n": "Wildspitze", "c": "Alpen"},
    {"n": "K2", "c": "Karakorum"},
    {"n": "Gasherbrum I", "c": "Karakorum"},
    {"n": "Broad Peak", "c": "Karakorum"},
    {"n": "Gasherbrum II", "c": "Karakorum"},
    {"n": "Masherbrum", "c": "Karakorum"},
    {"n": "Batura Sar", "c": "Karakorum"},
    {"n": "Kangchenjunga", "c": "Himalaya"},
    {"n": "Lhotse", "c": "Himalaya"},
    {"n": "Makalu", "c": "Himalaya"},
    {"n": "Cho Oyu", "c": "Himalaya"},
    {"n": "Dhaulagiri", "c": "Himalaya"},
    {"n": "Manaslu", "c": "Himalaya"},
    {"n": "Annapurna", "c": "Himalaya"},
    {"n": "Nanga Parbat", "c": "Himalaya"},
    {"n": "Tirich Mir", "c": "Hindukusch"},
    {"n": "Nowshak", "c": "Hindukusch"},
    {"n": "Elbrus", "c": "Kaukasus"},
    {"n": "Dykh-Tau", "c": "Kaukasus"},
    {"n": "Shkhara", "c": "Kaukasus"},
    {"n": "Kazbek", "c": "Kaukasus"},
    {"n": "Aconcagua", "c": "Anden"},
    {"n": "Ojos del Salado", "c": "Anden"},
    {"n": "Monte Pissis", "c": "Anden"},
    {"n": "Huascarán", "c": "Anden"},
    {"n": "Sajama", "c": "Anden"},
    {"n": "Chimborazo", "c": "Anden"},
    {"n": "Denali", "c": "Alaska Range"},
    {"n": "Fairweather", "c": "St. Elias Mountains"},
    {"n": "Logan", "c": "St. Elias Mountains"},
    {"n": "Puncak Jaya (Carstensz)", "c": "Sudirman Range"},
    {"n": "Mawson Peak", "c": "Heard Island"},
    {"n": "Kilimanjaro", "c": "Ost-Rift-Berge"},
    {"n": "Mount Kenya", "c": "Ost-Rift-Berge"},
    {"n": "Margherita Peak", "c": "Ruwenzori"},
    {"n": "Ras Dejen", "c": "Äthiopisches Hochland"},
    {"n": "Toubkal", "c": "Atlas"},
    {"n": "Kosciuszko", "c": "Snowy Mountains (Australien)"},
    {"n": "Vinson Massif", "c": "Sentinel Range (Antarktis)"},
    {"n": "Pico (Azoren)", "c": "Azoren"},
    {"n": "Mulhacén", "c": "Sierra Nevada (Spanien)"},
    {"n": "Olympus", "c": "Griechisches Festland"},
    {"n": "Zugspitze", "c": "Bayerische Alpen"},
]

# --- geo_erdbeben_jahr — Ziel: 50+ ---
erdbeben_jahr_new = [
    {"n": "Shaanxi-Erdbeben (China)", "c": "1556"},
    {"n": "Aleppo-Erdbeben (Syrien)", "c": "1138"},
    {"n": "Antiochien-Erdbeben (Türkei)", "c": "526"},
    {"n": "Damghan-Erdbeben (Iran)", "c": "856"},
    {"n": "Ardabil-Erdbeben (Iran)", "c": "893"},
    {"n": "Kanto-Erdbeben (Japan)", "c": "1923"},
    {"n": "Messina-Erdbeben (Italien)", "c": "1908"},
    {"n": "Erdbeben in San Francisco (USA)", "c": "1906"},
    {"n": "Tangshan-Erdbeben (China)", "c": "1976"},
    {"n": "Spitak-Erdbeben (Armenien)", "c": "1988"},
    {"n": "Iran-Erdbeben Bam (Iran)", "c": "2003"},
    {"n": "Sumatra-Andaman (Indien. Ozean)", "c": "2004"},
    {"n": "Kashmir-Erdbeben (Pakistan/Indien)", "c": "2005"},
    {"n": "Sichuan-Erdbeben (China)", "c": "2008"},
    {"n": "Haiti-Erdbeben (Haiti)", "c": "2010"},
    {"n": "Maule-Erdbeben (Chile)", "c": "2010"},
    {"n": "Christchurch-Erdbeben (Neuseeland)", "c": "2011"},
    {"n": "Tōhoku-Erdbeben (Japan)", "c": "2011"},
    {"n": "Nepal-Erdbeben Gorkha (Nepal)", "c": "2015"},
    {"n": "Ecuador-Erdbeben Pedernales (Ecuador)", "c": "2016"},
    {"n": "Puebla-Erdbeben (Mexiko)", "c": "2017"},
    {"n": "Sulawesi-Erdbeben Palu (Indonesien)", "c": "2018"},
    {"n": "Albanien-Erdbeben (Albanien)", "c": "2019"},
    {"n": "Türkei-Erdbeben Elazığ (Türkei)", "c": "2020"},
    {"n": "Kahramanmaraş (Türkei/Syrien)", "c": "2023"},
    {"n": "Valdivia-Erdbeben (Chile)", "c": "1960"},
    {"n": "Anchorage-Erdbeben (Alaska, USA)", "c": "1964"},
    {"n": "Kamtschatka-Erdbeben (Russland)", "c": "1952"},
    {"n": "Assam-Erdbeben (Indien)", "c": "1950"},
    {"n": "Gansu-Erdbeben (China)", "c": "1920"},
    {"n": "Peru-Erdbeben Ancash (Peru)", "c": "1970"},
    {"n": "Guatemala-Erdbeben (Guatemala)", "c": "1976"},
    {"n": "Manjil-Rudbar (Iran)", "c": "1990"},
    {"n": "Izmit-Erdbeben (Türkei)", "c": "1999"},
    {"n": "Chi-Chi-Erdbeben (Taiwan)", "c": "1999"},
    {"n": "Bhuj-Erdbeben (Indien)", "c": "2001"},
    {"n": "Bohol-Erdbeben (Philippinen)", "c": "2013"},
    {"n": "Iquique-Erdbeben (Chile)", "c": "2014"},
    {"n": "Sabah-Erdbeben (Malaysia)", "c": "2015"},
    {"n": "Kumamoto-Erdbeben (Japan)", "c": "2016"},
]

# --- geo_gestein_nutzung — Ziel: 50+ ---
gestein_nutzung_new = [
    {"n": "Basalt", "c": "Straßenbau / Schotter"},
    {"n": "Granit", "c": "Baustein / Pflasterung"},
    {"n": "Marmor", "c": "Bau & Skulptur"},
    {"n": "Sandstein", "c": "Bau & Fassaden"},
    {"n": "Kalkstein", "c": "Zement & Bau"},
    {"n": "Schiefer", "c": "Dachdeckung"},
    {"n": "Quarz", "c": "Elektronik / Glas"},
    {"n": "Feldspat", "c": "Keramik & Glasur"},
    {"n": "Glimmer (Muskovit)", "c": "Elektroisolierung"},
    {"n": "Tuff", "c": "Leichtbau"},
    {"n": "Travertin", "c": "Gebäude & Fliesen"},
    {"n": "Obsidian", "c": "Historische Werkzeuge"},
    {"n": "Feuerstein (Flint)", "c": "Werkzeuge / Feuer"},
    {"n": "Kreide", "c": "Schreibmittel / Kalk"},
    {"n": "Anhydrit", "c": "Gips-Rohmaterial"},
    {"n": "Gips", "c": "Bau & Medizin"},
    {"n": "Asbest", "c": "Feuerhemmung (veraltet)"},
    {"n": "Kaolin", "c": "Porzellan & Papier"},
    {"n": "Bentonit", "c": "Bohrlochverfüllung"},
    {"n": "Dolomit", "c": "Stahl & Baustoff"},
    {"n": "Andesit", "c": "Pflasterung / Bau"},
    {"n": "Porphyr", "c": "Dekorstein"},
    {"n": "Onyx", "c": "Schmuck"},
    {"n": "Lapislazuli", "c": "Farbe & Schmuck"},
    {"n": "Malachit", "c": "Kupfererz & Schmuck"},
    {"n": "Magnetit", "c": "Eisenherstellung"},
    {"n": "Chromit", "c": "Edelstahlherstellung"},
    {"n": "Bauxit", "c": "Aluminiumherstellung"},
    {"n": "Kassiterit (Zinnstein)", "c": "Zinnherstellung"},
    {"n": "Wolframit", "c": "Wolframherstellung"},
    {"n": "Molybdänit", "c": "Stahlhärtung"},
    {"n": "Borax", "c": "Glas & Reinigung"},
    {"n": "Sylvin (Kalisalz)", "c": "Düngemittel"},
    {"n": "Halit (Steinsalz)", "c": "Lebensmittel / Industrie"},
    {"n": "Schwefel", "c": "Schwefelsäure-Produktion"},
    {"n": "Phosphorit", "c": "Phosphatdünger"},
    {"n": "Fluorit", "c": "Optik & Säure"},
    {"n": "Korund (Rubin/Saphir)", "c": "Schmuck & Schleifmittel"},
    {"n": "Diamant", "c": "Schmuck & Schneidwerkzeug"},
    {"n": "Zirkon", "c": "Kerntechnik & Keramik"},
    {"n": "Titaneisenerz (Ilmenit)", "c": "Farbe & Leichtbau"},
    {"n": "Jadeit", "c": "Schmuck & Kunst (Asien)"},
    {"n": "Nephrit", "c": "Schmuck & Kunst"},
    {"n": "Türkis", "c": "Schmuck"},
]

# --- geo_mineral_farbe — Ziel: 50+ ---
mineral_farbe_new = [
    {"n": "Azurit", "c": "Blau"},
    {"n": "Türkis", "c": "Blaugrün"},
    {"n": "Chrysokoll", "c": "Blaugrün"},
    {"n": "Aquamarin", "c": "Hellblau"},
    {"n": "Sodalith", "c": "Dunkelblau"},
    {"n": "Sapphir (Korund)", "c": "Blau"},
    {"n": "Fluorit", "c": "Violett / Lila"},
    {"n": "Amethyst", "c": "Violett"},
    {"n": "Sugilit", "c": "Violett"},
    {"n": "Chaoiit", "c": "Weiß"},
    {"n": "Calcit", "c": "Weiß / Farblos"},
    {"n": "Gips (Alabaster)", "c": "Weiß"},
    {"n": "Dolomit", "c": "Weiß / Grau"},
    {"n": "Feldspat", "c": "Weiß / Rosa"},
    {"n": "Halit", "c": "Farblos / Weiß"},
    {"n": "Quarz (Bergkristall)", "c": "Farblos"},
    {"n": "Topas", "c": "Farblos / Blau / Gelb"},
    {"n": "Diamant", "c": "Farblos"},
    {"n": "Hämatit", "c": "Rot / Silber"},
    {"n": "Rubin (Korund)", "c": "Rot"},
    {"n": "Spessartin", "c": "Orange-Rot"},
    {"n": "Cinnabarit", "c": "Scharlachrot"},
    {"n": "Rosenquarz", "c": "Rosa"},
    {"n": "Rhodonit", "c": "Rosa / Rot"},
    {"n": "Rhodochrosit", "c": "Rosa"},
    {"n": "Smaragd (Beryll)", "c": "Grün"},
    {"n": "Aventurin", "c": "Grün"},
    {"n": "Prehnit", "c": "Hellgrün"},
    {"n": "Olivin (Peridot)", "c": "Olivgrün"},
    {"n": "Serpentin", "c": "Grün"},
    {"n": "Chromit", "c": "Schwarz"},
    {"n": "Magnetit", "c": "Schwarz"},
    {"n": "Turmalin (Schörl)", "c": "Schwarz"},
    {"n": "Obsidian", "c": "Schwarz"},
    {"n": "Pyrit", "c": "Gold / Messing"},
    {"n": "Chalcopyrit", "c": "Gold / Bunt"},
    {"n": "Gold", "c": "Gold / Gelb"},
    {"n": "Bernstein", "c": "Gelb / Orange"},
    {"n": "Topas (imperial)", "c": "Orange-Gelb"},
    {"n": "Schwefelelement", "c": "Schwefelgelb"},
    {"n": "Citrin", "c": "Gelb"},
    {"n": "Larimar", "c": "Hellblau"},
    {"n": "Tsavorit", "c": "Dunkelgrün"},
    {"n": "Alexandrit", "c": "Grün / Rot (Farbwechsel)"},
]

# --- geo_wunder_entstehung — Ziel: 50+ ---
wunder_entstehung_new = [
    {"n": "Diamant (Kimberlit-Pfeiler)", "c": "Metamorphose / Druck"},
    {"n": "Geysir (Old Faithful)", "c": "Geothermie"},
    {"n": "Yellowstone Caldera", "c": "Supervulkanismus"},
    {"n": "Grand Canyon", "c": "Fluss-Erosion"},
    {"n": "Yarlung Tsangpo Canyon", "c": "Plattentektonik & Erosion"},
    {"n": "Ayers Rock / Uluru", "c": "Inselberg-Erosion"},
    {"n": "Cappadocia Feenschornsteine", "c": "Vulkanische Ablagerung & Erosion"},
    {"n": "Delicate Arch (Utah)", "c": "Winderoion & Auflösung"},
    {"n": "Bryce Canyon Hoodoos", "c": "Frost-Erosion"},
    {"n": "Zhangjiajie-Säulen", "c": "Sandstein-Verwitterung"},
    {"n": "Tepui Mount Roraima", "c": "Platten-Hebung & Erosion"},
    {"n": "Mammoth Cave", "c": "Kalk-Auflösung (Karstlösung)"},
    {"n": "Son Doong Cave", "c": "Karstlösung"},
    {"n": "Doline", "c": "Einsturz-Karstphänomen"},
    {"n": "Fiord Geirangerfjord", "c": "Gletschererosion"},
    {"n": "Alpen", "c": "Kollisions-Tektonik"},
    {"n": "Himalaya", "c": "Kollisions-Tektonik"},
    {"n": "Rift Valley", "c": "Dehnungstektonik"},
    {"n": "Mid-Atlantic-Ridge", "c": "Meeresbodenausbreitung"},
    {"n": "Hawaiianische Inseln", "c": "Hotspot-Vulkanismus"},
    {"n": "Galápagos-Inseln", "c": "Hotspot-Vulkanismus"},
    {"n": "Island", "c": "Hotspot & Mittelozeanischer Rücken"},
    {"n": "Basaltsäulen (Giants Causeway)", "c": "Lavakühlung"},
    {"n": "Lonar-Krater (Indien)", "c": "Meteoriten-Einschlag"},
    {"n": "Barringer Crater (Arizona)", "c": "Meteoriten-Einschlag"},
    {"n": "Manicouagan-Krater (Kanada)", "c": "Meteoriten-Einschlag"},
    {"n": "Steinpilze (Steinformat.)", "c": "Sandstrahleroion"},
    {"n": "Rote Sanddünen Namib", "c": "Äolische Ablagerung"},
    {"n": "Barchan-Dünen", "c": "Windablagerung"},
    {"n": "Stalagmiten", "c": "Mineralausfällung"},
    {"n": "Stalagtiten", "c": "Mineralausfällung"},
    {"n": "Travertinterrassen (Pamukkale)", "c": "Mineralausfällung / Thermalquellen"},
    {"n": "Salzwüste Salar de Uyuni", "c": "Verdunstung"},
    {"n": "Badlands (South Dakota)", "c": "Weich-Gesteins-Erosion"},
    {"n": "Pinnacles Desert (Australien)", "c": "Kalkstein-Auflösung"},
    {"n": "Mud Volcanoes (Aserbaidschan)", "c": "Gasaustritt & Sedimentauftrieb"},
    {"n": "Chocolate Hills (Philippinen)", "c": "Karstauflösung"},
    {"n": "Rainbow Mountains (Zhangye, China)", "c": "Oxidation & Ablagerung"},
    {"n": "Antelope Canyon", "c": "Fluss-Erosion"},
    {"n": "Wave (Coyote Buttes, USA)", "c": "Wind & Wassereroison"},
    {"n": "Permafrost-Polygone (Sibirien)", "c": "Frost & Eiskeilwachstum"},
    {"n": "Vulkanische Lavahöhle (Hawaii)", "c": "Lavatunnel-Bildung"},
    {"n": "Korallenriff Great Barrier Reef", "c": "Biogene Bildung"},
]

n_m_vulkan = extend_key(match, "geo_vulkan_land", vulkan_land_new)
n_m_berg = extend_key(match, "geo_berg_gebirge", berg_gebirge_new)
n_m_erdbeben = extend_key(match, "geo_erdbeben_jahr", erdbeben_jahr_new)
n_m_gestein_n = extend_key(match, "geo_gestein_nutzung", gestein_nutzung_new)
n_m_farbe = extend_key(match, "geo_mineral_farbe", mineral_farbe_new)
n_m_wunder = extend_key(match, "geo_wunder_entstehung", wunder_entstehung_new)

jsave("geo_match.json", match)
print(f"  [OK] match/vulkan_land: +{n_m_vulkan}")
print(f"  [OK] match/berg_gebirge: +{n_m_berg}")
print(f"  [OK] match/erdbeben_jahr: +{n_m_erdbeben}")
print(f"  [OK] match/gestein_nutzung: +{n_m_gestein_n}")
print(f"  [OK] match/mineral_farbe: +{n_m_farbe}")
print(f"  [OK] match/wunder_entstehung: +{n_m_wunder}")

# ============================================================
# FINALE ITEMZAHLEN
# ============================================================
print("\n=== FINALE ITEMZAHLEN ===")
print("\ngeo_pin.json")
pin2 = jload("geo_pin.json")
for k, v in pin2.items():
    items = v.get("items", v) if isinstance(v, dict) else v
    print(f"  {k}: {len(items)}")

print("\ngeo_hl.json")
hl2 = jload("geo_hl.json")
for k, v in hl2.items():
    items = v.get("items", v) if isinstance(v, dict) else v
    print(f"  {k}: {len(items)}")

print("\ngeo_match.json")
m2 = jload("geo_match.json")
for k, v in m2.items():
    items = v.get("items", v) if isinstance(v, dict) else v
    print(f"  {k}: {len(items)}")
