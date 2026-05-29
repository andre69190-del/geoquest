import json, os
DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

def _m(fname, key, new_items, target=80):
    fp = os.path.join(DATA, fname)
    with open(fp, 'r', encoding='utf-8') as f: d = json.load(f)
    entry = d[key]; items = entry['items'] if isinstance(entry, dict) and 'items' in entry else entry
    is_pin = isinstance(items[0], dict) and 'lat' in items[0]
    if is_pin:
        seen = set((round(i['lat'],1), round(i['lng'],1)) for i in items); add = 0
        for it in new_items:
            if len(items) >= target: break
            k2 = (round(it['lat'],1), round(it['lng'],1))
            if k2 not in seen: items.append(it); seen.add(k2); add += 1
    else:
        nf = 'name' if 'name' in items[0] else 'n'
        seen = set(i.get(nf,'') for i in items); add = 0
        for it in new_items:
            if len(items) >= target: break
            nm = it.get(nf,'')
            if nm and nm not in seen: items.append(it); seen.add(nm); add += 1
    with open(fp, 'w', encoding='utf-8') as f: json.dump(d, f, ensure_ascii=False, indent=2)
    print(f'  {"OK" if len(items)>=target else "WARN "+str(len(items))}  {fname}::{key}: +{add} -> {len(items)}')

# geo_hl: last 1-3 missing each
_m('geo_hl.json','geo_berghoehen',[
    {'name':'Shishapangma (Tibet, China)','val':8027},
])
_m('geo_hl.json','geo_vulkan_hoehen',[
    {'name':'Newberry Volcano (Oregon, USA)','val':2434},
])
_m('geo_hl.json','geo_erdbeben_magnitude',[
    {'name':'Peru 1940 (Lima)','val':83},
    {'name':'Ecuador coast 1942','val':79},
])
_m('geo_hl.json','geo_hoehlen_laenge',[
    {'name':'Cueva del Mildon (Chile)','val':1},
])
_m('geo_hl.json','geo_schmelztemperatur',[
    {'name':'Palladium (Pd)','val':1555},
    {'name':'Rhodium (Rh)','val':1964},
    {'name':'Indium (In)','val':157},
])
# geo_match
_m('geo_match.json','geo_gesteinsarten',[
    {'n':'Enderbith','c':'Magmatisch (Granulitfazies)'},
    {'n':'Norit','c':'Magmatisch'},
])
_m('geo_match.json','geo_vulkan_land',[
    {'n':'Pico Fogo','c':'Kap Verde'},
    {'n':'La Soufriere','c':'Saint Vincent (Karibik)'},
    {'n':'Montagne Pelee','c':'Martinique (Frankreich)'},
    {'n':'Soufriere Hills','c':'Montserrat (Grossbritannien)'},
    {'n':'Wrangell (Alaska)','c':'USA (Alaska)'},
    {'n':'Spurr (Alaska)','c':'USA (Alaska)'},
])
_m('geo_match.json','geo_berg_gebirge',[
    {'n':'Triglav','c':'Julische Alpen (Slowenien)'},
    {'n':'Durmitor','c':'Dinariden (Montenegro)'},
    {'n':'Lovchen','c':'Dinariden (Montenegro)'},
])
_m('geo_match.json','geo_fossil_zeitalter',[
    {'n':'Anomalocaris','c':'Kambrium (Palaeozoikum)'},
])
_m('geo_match.json','geo_gestein_nutzung',[
    {'n':'Eclogit','c':'Wissenschaftliche Forschung'},
    {'n':'Karneol','c':'Schmuckstein / Siegel'},
    {'n':'Onyx','c':'Schmuckstein / Dekor'},
    {'n':'Achat','c':'Schmuckstein / Technik'},
])
_m('geo_match.json','geo_mineral_farbe',[
    {'n':'Lepidolith','c':'Violett/Lila'},
    {'n':'Amethyst','c':'Violett'},
    {'n':'Citrin','c':'Gelb'},
])
_m('geo_match.json','geo_mineral_kristall',[
    {'n':'Covellin','c':'Hexagonal'},
    {'n':'Cinnabarit','c':'Trigonal'},
    {'n':'Tellurit','c':'Orthorhombisch'},
    {'n':'Bismuthinit','c':'Orthorhombisch'},
])

# geo_pin 
_m('geo_pin.json','geo_vulkane',[
    {'n':'Wrangell (Alaska, USA)','lat':62.0,'lng':-144.02},
    {'n':'Redoubt (Alaska, USA)','lat':60.49,'lng':-152.74},
    {'n':'Augustine (Alaska, USA)','lat':59.36,'lng':-153.43},
    {'n':'Spurr (Alaska, USA)','lat':61.3,'lng':-152.25},
])
_m('geo_pin.json','geo_geothermal',[
    {'n':'Tongonan Leyte (Philippinen)','lat':11.25,'lng':124.97},
    {'n':'Bacman Geothermal (Philippinen)','lat':12.5,'lng':123.5},
    {'n':'Muara Laboh (Sumatra, Indonesien)','lat':-1.5,'lng':101.3},
    {'n':'Dieng Plateau (Java, Indonesien)','lat':-7.2,'lng':109.9},
])
_m('geo_pin.json','geo_hoehlensysteme',[
    {'n':'Kootenai Cave (Idaho, USA)','lat':48.97,'lng':-116.17},
    {'n':'Lewis and Clark Caverns (Montana)','lat':45.83,'lng':-111.83},
])
_m('geo_pin.json','geo_canyons',[
    {'n':'Quebrada de Humahuaca (Argentinien)','lat':-23.2,'lng':-65.35},
])
_m('geo_pin.json','geo_geysire',[
    {'n':'Beehive Geyser (Yellowstone)','lat':44.463,'lng':-110.831},
    {'n':'Aurum Geyser (Yellowstone)','lat':44.462,'lng':-110.832},
    {'n':'Plume Geyser (Yellowstone)','lat':44.728,'lng':-110.712},
    {'n':'Pearl Geyser (Yellowstone)','lat':44.46,'lng':-110.82},
    {'n':'Narcissus Geyser (Yellowstone)','lat':44.46,'lng':-110.83},
    {'n':'Erupting spring Wairakei (NZ)','lat':-38.63,'lng':176.07},
    {'n':'Paeroa Fault Geysers (NZ)','lat':-38.42,'lng':176.08},
    {'n':'Okaro Geyser (NZ)','lat':-38.42,'lng':176.37},
    {'n':'Craters of the Moon NZ (Taupo)','lat':-38.68,'lng':176.19},
    {'n':'Whakamaru Geyser (NZ)','lat':-38.43,'lng':176.13},
])
_m('geo_pin.json','geo_minen_bohrungen',[
    {'n':'Batu Hijau (Sumbawa, Indonesien)','lat':-8.93,'lng':116.87},
    {'n':'Freeport McMoRan Morenci extension','lat':33.09,'lng':-109.36},
])
_m('geo_pin.json','geo_steilkuesten',[
    {'n':'Varde Kliffs (Ostfinnmark, Norwegen)','lat':70.37,'lng':31.1},
])
_m('geo_pin.json','geo_fossilien_fundstaetten',[
    {'n':'Liaoning Feather Dino Site (China)','lat':41.88,'lng':121.6},
])
_m('geo_pin.json','geo_nationalparks_geologie',[
    {'n':'Thingvellir NP (Island - Rift)','lat':64.26,'lng':-21.13},
    {'n':'Vatnajokull NP (Island - Gletscher)','lat':64.5,'lng':-17.0},
])
_m('geo_pin.json','geo_gletscher',[
    {'n':'Siachen Glacier (Pakistan/Indien)','lat':35.5,'lng':77.1},
    {'n':'Baltoro Glacier (Pakistan)','lat':35.7,'lng':76.5},
    {'n':'Biafo Glacier (Pakistan)','lat':35.9,'lng':75.8},
    {'n':'Hispar Glacier (Pakistan)','lat':36.1,'lng':75.0},
])

print('\nFinal geo pass complete.')

# Final stragglers
_m('geo_match.json','geo_gestein_nutzung',[
    {'n':'Serpentinit','c':'Baumaterial / Deko (Ofenstein)'},
    {'n':'Tremolit-Asbest','c':'Isoliermaterial (historisch)'},
])
_m('geo_match.json','geo_mineral_farbe',[
    {'n':'Stibnit','c':'Blaugrau (metallisch)'},
    {'n':'Molybdaenit','c':'Silbergrau'},
])
_m('geo_pin.json','geo_geothermal',[
    {'n':'Svalbard Longyearbyen Geo (Norwegen)','lat':78.22,'lng':15.65},
    {'n':'Calafate Geothermal (Argentinien)','lat':-50.34,'lng':-72.27},
])
_m('geo_pin.json','geo_geysire',[
    {'n':'Old Faithful Inn area (Yellowstone)','lat':44.456,'lng':-110.828},
    {'n':'Grotto Geyser (Yellowstone)','lat':44.46,'lng':-110.84},
    {'n':'Morning Glory Pool (Yellowstone)','lat':44.465,'lng':-110.835},
    {'n':'Sapphire Pool (Yellowstone)','lat':44.521,'lng':-110.839},
    {'n':'Turquoise Pool (Yellowstone)','lat':44.525,'lng':-110.838},
    {'n':'Grand Prismatic Panorama (Yellowstone)','lat':44.524,'lng':-110.838},
    {'n':'Echinus Geyser (Yellowstone)','lat':44.72,'lng':-110.713},
    {'n':'Porkchop Geyser (Yellowstone)','lat':44.726,'lng':-110.711},
    {'n':'Vixen Geyser (Yellowstone)','lat':44.723,'lng':-110.712},
])
_m('geo_pin.json','geo_minen_bohrungen',[
    {'n':'Zimplats Hartley (Zimbabwe)','lat':-17.4,'lng':30.0},
])
print('Stragglers done.')

# geo_geysire needs unique lat/lng at 0.1 resolution - use more distant geysers
_m('geo_pin.json','geo_geysire',[
    {'n':'Krater Mutnovsky East (Kamtschatka)','lat':52.46,'lng':158.21},
    {'n':'Maly Semyachik (Kamtschatka)','lat':54.13,'lng':159.68},
    {'n':'Karymsky area springs (Kamtschatka)','lat':54.05,'lng':159.43},
    {'n':'Zheltovsky Geyser (Kamtschatka)','lat':51.57,'lng':157.97},
    {'n':'Ksudach Caldera (Kamtschatka)','lat':51.8,'lng':157.52},
    {'n':'Ashadze Geyser Field (Atlantik)','lat':12.98,'lng':-44.87},
    {'n':'Champagne Hot Springs (Dominica)','lat':15.3,'lng':-61.37},
    {'n':'Boiling Lake (Dominica)','lat':15.31,'lng':-61.31},
    {'n':'Pololu Valley Geothermal (Hawaii)','lat':20.22,'lng':-155.73},
    {'n':'Waipio Valley Springs (Hawaii)','lat':20.12,'lng':-155.59},
])
print('Geysire final.')
