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

# geo_hl second pass
_m('geo_hl.json','geo_berghoehen',[
    {'name':'Monte Bianco (Italien/Frankreich)','val':4808},
    {'name':'Weisshorn (Schweiz)','val':4505},
    {'name':'Dom (Schweiz)','val':4545},
    {'name':'Lyskamm (Schweiz/Italien)','val':4527},
    {'name':'Matterhorn (Schweiz/Italien)','val':4478},
    {'name':'Finsteraarhorn (Schweiz)','val':4274},
    {'name':'Aletschhorn (Schweiz)','val':4193},
    {'name':'Elbrus Ost (Russland)','val':5621},
    {'name':'Shkhara (Georgien/Russland)','val':5201},
    {'name':'Dykh-Tau (Russland)','val':5205},
])
_m('geo_hl.json','geo_vulkan_hoehen',[
    {'name':'Llaima (Chile)','val':3125},
    {'name':'Villarrica (Chile)','val':2847},
    {'name':'Lanin (Chile/Argentinien)','val':3747},
    {'name':'Osorno (Chile)','val':2652},
    {'name':'Puyehue (Chile)','val':2236},
    {'name':'Copahue (Chile/Argentinien)','val':2953},
    {'name':'Oraefajokull (Island)','val':2110},
    {'name':'Snaefellsjokull (Island)','val':1446},
    {'name':'Pico do Fogo (Kap Verde)','val':2829},
    {'name':'Klyuchevskaya Sopka (Kamtschatka)','val':4754},
    {'name':'Shiveluch (Kamtschatka)','val':3283},
    {'name':'Bezymianny (Kamtschatka)','val':2882},
    {'name':'Tolbachik (Kamtschatka)','val':3682},
    {'name':'Avachinsky (Kamtschatka)','val':2741},
    {'name':'Rincon de la Vieja (Costa Rica)','val':1916},
    {'name':'Irazu (Costa Rica)','val':3432},
])
_m('geo_hl.json','geo_erdbeben_magnitude',[
    {'name':'Central Chile 1943','val':82},
    {'name':'Banda Sea 1938 (Indonesien)','val':85},
    {'name':'Aleutian Islands 1965','val':85},
    {'name':'Colombia 1970','val':80},
    {'name':'Oaxaca 1931 (Mexiko)','val':80},
    {'name':'Kenai Peninsula 1943 (Alaska)','val':81},
    {'name':'Fox Islands 1957 (Alaska)','val':93},
    {'name':'Rat Islands 1965 (Alaska)','val':85},
    {'name':'Andreanof Islands 1957','val':93},
    {'name':'Sumatra 2012 (Offshorependung)','val':82},
])
_m('geo_hl.json','geo_hoehlen_laenge',[
    {'name':'Mammoth Cave System (Kentucky, USA)','val':676},
    {'name':'Sistema Ox Bel Ha (Quintana Roo, Mexiko)','val':368},
    {'name':'Cueva Sac Actun (Mexiko, verbunden)','val':368},
    {'name':'Jewel Cave (South Dakota, USA)','val':338},
    {'name':'Fisher Ridge Cave System (USA)','val':200},
    {'name':'Ozernaya (Ukraine)','val':117},
    {'name':'Cueva del Sapo (Venezuela)','val':2},
    {'name':'Cueva de la Pileta (Spanien)','val':3},
])
_m('geo_hl.json','geo_gesteins_alter',[
    {'name':'Qiangtang Block Granit (Tibet)','val':2500},
    {'name':'Dharwar Craton (Indien)','val':3100},
    {'name':'Singhbhum Craton (Indien)','val':3100},
    {'name':'Yilgarn Craton (Australien)','val':3600},
    {'name':'Slave Province (Kanada)','val':2700},
    {'name':'Barberton Greenstone Belt (Suedafrika)','val':3500},
])
_m('geo_hl.json','geo_schluchten_tiefe',[
    {'name':'Indus-Himalaya Gorge (Pakistan)','val':4500},
    {'name':'Bramaputra Grand Canyon (Indien)','val':5500},
    {'name':'Canon del Sumidero (Mexiko)','val':1000},
    {'name':'Wadi Bani Auf (Oman)','val':1500},
    {'name':'Colca South Canyon (Peru)','val':3354},
    {'name':'El Hierro Barranco (Spanien)','val':300},
    {'name':'Azib n\'Ikkis Canyon (Marokko)','val':500},
    {'name':'Vorotan Gorge (Armenien)','val':700},
    {'name':'Debed Canyon (Armenien)','val':600},
    {'name':'Mtkvari Canyon (Georgien)','val':800},
    {'name':'Rhodopen Canyon (Bulgarien)','val':400},
    {'name':'Uvac Canyon (Serbien)','val':400},
    {'name':'Ovcar-Kablar Canyon (Serbien)','val':300},
])
_m('geo_hl.json','geo_schmelztemperatur',[
    {'name':'Molybdaen (Mo)','val':2623},
    {'name':'Iridium (Ir)','val':2446},
    {'name':'Osmium (Os)','val':3033},
    {'name':'Rhenium (Re)','val':3186},
    {'name':'Tantal (Ta)','val':3017},
    {'name':'Niob (Nb)','val':2477},
    {'name':'Vanadium (V)','val':1910},
    {'name':'Zirkon (Zr)','val':1855},
    {'name':'Hafnium (Hf)','val':2233},
    {'name':'Scandium (Sc)','val':1541},
    {'name':'Andalusit (Al2SiO5)','val':1400},
    {'name':'Wollastonit (CaSiO3)','val':1540},
    {'name':'Forsterit (Mg2SiO4)','val':1890},
    {'name':'Anorthit (Plagioklas)','val':1553},
])
_m('geo_hl.json','geo_tsunami_hoehe',[
    {'name':'Alaska 1946 Unimak Island','val':35},
    {'name':'Kamtschatka 1959','val':7},
    {'name':'Aleutian 1964 (Crescent City)','val':6},
    {'name':'Chile 1922 (Atacama)','val':9},
    {'name':'Japan Meiji 1896 (Sanriku)','val':38},
    {'name':'Chile 1877 (Iquique)','val':24},
    {'name':'Peru 1868 (Arica)','val':21},
    {'name':'Alaska 1958 Lituya supplement','val':30},
    {'name':'Sicily 1908 Messina (detail)','val':12},
    {'name':'Banda Sea 1938','val':5},
    {'name':'Vanuatu 1999','val':5},
    {'name':'Papua New Guinea 1998 Sissano','val':15},
    {'name':'Java 1883 Krakatau supplement','val':37},
    {'name':'Greece 1956 Amorgos','val':25},
])

# geo_match second pass
_m('geo_match.json','geo_gesteinsarten',[
    {'n':'Pechstein','c':'Magmatisch'},
    {'n':'Kersantit','c':'Magmatisch'},
    {'n':'Syenit','c':'Magmatisch'},
    {'n':'Diorit','c':'Magmatisch'},
    {'n':'Monzonit','c':'Magmatisch'},
    {'n':'Alkalifeldspat','c':'Magmatisch'},
    {'n':'Subgrauwacke','c':'Sedimentaer'},
    {'n':'Wackestone','c':'Sedimentaer'},
    {'n':'Flyschwacke','c':'Sedimentaer'},
    {'n':'Graptolithen-Schiefer','c':'Sedimentaer'},
    {'n':'Chalzedon','c':'Sedimentaer/Kiesel'},
    {'n':'Schwarzschiefer','c':'Metamorph'},
    {'n':'Blauschiefer','c':'Metamorph'},
    {'n':'Kalkmarmor','c':'Metamorph'},
    {'n':'Granulitgruppenstein','c':'Metamorph'},
    {'n':'Whiteschist','c':'Metamorph'},
    {'n':'Suevit','c':'Impaktgestein'},
    {'n':'Moldavit','c':'Impaktgestein'},
    {'n':'Kataklasit','c':'Impaktgestein/Bruchzone'},
    {'n':'Mylonit','c':'Metamorph (Bruchzone)'},
    {'n':'Tonalith','c':'Magmatisch'},
    {'n':'Trondhjemit','c':'Magmatisch'},
])
_m('geo_match.json','geo_tektonik',[
    {'n':'Suedatlantischer Ruecken','c':'Suedamerikanische & Afrikanische Platte'},
])
_m('geo_match.json','geo_mineralien',[
    {'n':'Coltan (Niobit-Tantalit)','c':'Tantal/Niob-Gewinnung'},
    {'n':'Loellingit','c':'Arsen-Mineral'},
    {'n':'Arsenopyrit','c':'Arsen-Sulfid'},
    {'n':'Tennantit','c':'Kupfer-Arsen-Sulfid'},
    {'n':'Tetraedrit','c':'Kupfer-Antimon-Sulfid'},
    {'n':'Antimonit','c':'Antimon-Gewinnung'},
    {'n':'Bismuthinit','c':'Bismut-Gewinnung'},
    {'n':'Molybdaenit','c':'Molybdaen-Gewinnung'},
    {'n':'Nickelin','c':'Nickel-Arsenid'},
])
_m('geo_match.json','geo_vulkan_land',[
    {'n':'Piton de la Fournaise','c':'Frankreich (Reunion)'},
    {'n':'Klyuchevskaya Sopka','c':'Russland (Kamtschatka)'},
    {'n':'Shiveluch','c':'Russland (Kamtschatka)'},
    {'n':'Tolbachik','c':'Russland (Kamtschatka)'},
    {'n':'Avachinsky','c':'Russland (Kamtschatka)'},
    {'n':'Erebus','c':'Antarktis'},
    {'n':'Deception Island Vulkan','c':'Antarktis'},
    {'n':'Fogo','c':'Kap Verde'},
    {'n':'Cameroon Mountain','c':'Kamerun'},
    {'n':'Ol Doinyo Lengai','c':'Tansania'},
    {'n':'Nyiragongo','c':'DR Kongo'},
    {'n':'Erta Ale','c':'Aethiopien'},
    {'n':'Irazu','c':'Costa Rica'},
])
_m('geo_match.json','geo_berg_gebirge',[
    {'n':'Shkhara','c':'Kaukasus (Georgien/Russland)'},
    {'n':'Dykh-Tau','c':'Kaukasus (Russland)'},
    {'n':'Koshtan-Tau','c':'Kaukasus (Russland)'},
    {'n':'Pushkin Peak','c':'Kaukasus (Russland)'},
    {'n':'Djanga-Tau','c':'Kaukasus (Georgien)'},
    {'n':'Kazbek','c':'Kaukasus (Georgien)'},
    {'n':'Weisshorn','c':'Alpen (Schweiz)'},
    {'n':'Dent Blanche','c':'Alpen (Schweiz)'},
    {'n':'Grandes Jorasses','c':'Alpen (Frankreich)'},
    {'n':'Aiguille du Geant','c':'Alpen (Frankreich)'},
    {'n':'Grosses Wiesbachhorn','c':'Alpen (Oesterreich)'},
    {'n':'Korab','c':'Dinariden (Nordmazedonien)'},
    {'n':'Musala','c':'Rhodopengebirge (Bulgarien)'},
])
_m('geo_match.json','geo_wunder_entstehung',[
    {'n':'Camargue (Frankreich)','c':'Flussdelta + Gezeitenwirkung'},
    {'n':'Watt (Nordsee)','c':'Gezeitenablagerung + Sediment'},
])
_m('geo_match.json','geo_fossil_zeitalter',[
    {'n':'Archaeocyatha','c':'Kambrium (Palaeozoikum)'},
    {'n':'Chitinozoen','c':'Ordovizium-Devon (Palaeozoikum)'},
    {'n':'Conodonten','c':'Kambrium-Trias (Palaeozoikum-Mesozoikum)'},
    {'n':'Belemniten','c':'Jura-Kreide (Mesozoikum)'},
    {'n':'Rudisten','c':'Kreide (Mesozoikum)'},
    {'n':'Inoceramiden','c':'Kreide (Mesozoikum)'},
    {'n':'Nannofossilien (Coccolith)','c':'Trias-Heute'},
    {'n':'Diatomeen','c':'Jura-Heute'},
    {'n':'Radiolaria','c':'Kambrium-Heute'},
    {'n':'Foraminiferen','c':'Kambrium-Heute'},
    {'n':'Nautiloid','c':'Kambrium-Heute'},
    {'n':'Crinoiden','c':'Ordovizium-Heute'},
])
_m('geo_match.json','geo_gestein_nutzung',[
    {'n':'Jaspis','c':'Schmuckstein / Siegel'},
    {'n':'Feuerstein','c':'Steinzeit-Werkzeug'},
    {'n':'Feuerfestton','c':'Hochofenauskleidung'},
    {'n':'Bentonit','c':'Bohrspuelung / Abdichtung'},
    {'n':'Kaolin','c':'Porzellan / Papier'},
    {'n':'Feldspat','c':'Glas / Keramik'},
    {'n':'Rohpumice','c':'Leichtbeton'},
    {'n':'Perlit','c':'Daemmstoff / Gaertnererde'},
    {'n':'Vermiculit','c':'Daemmstoff / Gaertnererde'},
    {'n':'Montmorillonit','c':'Katzenstreu / Abdichtung'},
    {'n':'Vermiculit Mineral','c':'Daemmstoff / Brandschutz'},
    {'n':'Celestin','c':'Strontium-Gewinnung'},
    {'n':'Wulfenit','c':'Blei-/Molybdaen-Erz'},
    {'n':'Scheelite','c':'Wolfram-Gewinnung'},
    {'n':'Columbite','c':'Niob-Gewinnung'},
])
_m('geo_match.json','geo_landschaft_ursprung',[
    {'n':'Camargue (Frankreich)','c':'Flussdelta + Brackwasser'},
])
_m('geo_match.json','geo_mineral_farbe',[
    {'n':'Fluorit','c':'Violett/Gruen/Farblos'},
    {'n':'Celestin','c':'Blassblau'},
    {'n':'Baryt','c':'Weiss/Farblos'},
    {'n':'Calcit','c':'Weiss/Farblos'},
    {'n':'Quarz','c':'Farblos/Weiss'},
    {'n':'Gips','c':'Weiss/Farblos'},
    {'n':'Aragonit','c':'Weiss/Gelblich'},
    {'n':'Dolomit','c':'Weiss/Grau'},
    {'n':'Enargit','c':'Dunkelgrau/Schwarz'},
    {'n':'Bornit','c':'Pfauenschwanz-Irisierend'},
    {'n':'Idokras','c':'Gelbgruen/Braun'},
    {'n':'Sugilith','c':'Violett/Pink'},
    {'n':'Tanzanit','c':'Blauviolett'},
])
_m('geo_match.json','geo_kontinent_platte',[
    {'n':'Kanarische Inseln','c':'Afrikanische Platte'},
    {'n':'Kap Verde','c':'Afrikanische Platte'},
    {'n':'Falklandinseln','c':'Suedamerikanische Platte'},
    {'n':'Suedsandwichinseln','c':'Scotia-Platte'},
    {'n':'Kerguelen','c':'Indo-Australische Platte'},
    {'n':'Heard Island','c':'Indo-Australische Platte'},
    {'n':'South Georgia','c':'Scotia-Platte'},
    {'n':'Bouvetinsel','c':'Afrikanische Platte'},
    {'n':'Macquarie Island','c':'Australische & Pazifische Platte'},
    {'n':'Pitcairn','c':'Pazifische Platte'},
])
_m('geo_match.json','geo_hoehlen_land',[
    {'n':'Cueva de Aitzbitarte','c':'Spanien (Baskenland)'},
    {'n':'Phong Nha Cave','c':'Vietnam'},
    {'n':'Wookey Hole','c':'England'},
    {'n':'Cox\'s Cave Cheddar','c':'England'},
    {'n':'Grotte de Font-de-Gaume','c':'Frankreich'},
    {'n':'Grotte de Niaux','c':'Frankreich'},
    {'n':'Cueva de La Pileta','c':'Spanien'},
    {'n':'Grotta del Gelo','c':'Italien (Sizilien)'},
])
_m('geo_match.json','geo_mineral_kristall',[
    {'n':'Wollastonit','c':'Triklin'},
    {'n':'Kyanit','c':'Triklin'},
    {'n':'Anorthit','c':'Triklin'},
    {'n':'Mikroklin','c':'Triklin'},
    {'n':'Chrysoberyll','c':'Orthorhombisch'},
    {'n':'Staurolith','c':'Monoklin'},
    {'n':'Cassiterit','c':'Tetragonal'},
    {'n':'Anatas','c':'Tetragonal'},
    {'n':'Rutil','c':'Tetragonal'},
    {'n':'Zirkon (Mineral)','c':'Tetragonal'},
])
_m('geo_match.json','geo_gebirge_entstehung',[
    {'n':'Armorica (Bretagne)','c':'Variszische Kollision'},
    {'n':'Massif Central (Frankreich)','c':'Variszische Heraushebung'},
    {'n':'Stara Planina (Bulgarien)','c':'Alpidische Orogenese'},
    {'n':'Balkangebirge','c':'Alpidische Orogenese'},
    {'n':'Rhodopen','c':'Alpidische Extension + Metamorphose'},
    {'n':'Rila-Pirion (Bulgarien)','c':'Alpidische Orogenese'},
    {'n':'Transylvania Alpen','c':'Alpidische Kollision'},
])

# geo_pin second pass
_m('geo_pin.json','geo_vulkane',[
    {'n':'Llaima (Chile)','lat':-38.69,'lng':-71.73},
    {'n':'Villarrica (Chile)','lat':-39.42,'lng':-71.94},
    {'n':'Lanin (Chile/Argentinien)','lat':-39.63,'lng':-71.5},
    {'n':'Osorno (Chile)','lat':-41.1,'lng':-72.49},
    {'n':'Hudson (Chile)','lat':-45.9,'lng':-72.97},
    {'n':'Klyuchevskaya Sopka (Kamtschatka)','lat':56.06,'lng':160.64},
    {'n':'Shiveluch (Kamtschatka)','lat':56.65,'lng':161.36},
    {'n':'Tolbachik (Kamtschatka)','lat':55.83,'lng':160.33},
    {'n':'Puyehue (Chile)','lat':-40.59,'lng':-72.12},
    {'n':'Turrialba (Costa Rica)','lat':10.03,'lng':-83.77},
    {'n':'Irazu (Costa Rica)','lat':9.98,'lng':-83.85},
    {'n':'Rincon de la Vieja (Costa Rica)','lat':10.83,'lng':-85.32},
    {'n':'Cerro Azul (Galapagos)','lat':-0.92,'lng':-91.41},
])
_m('geo_pin.json','geo_geothermal',[
    {'n':'Kizildere Geothermal (Tuerkei)','lat':37.9,'lng':28.7},
    {'n':'Tuzla (Tuerkei)','lat':40.0,'lng':29.3},
    {'n':'Germencik (Tuerkei)','lat':37.9,'lng':27.6},
    {'n':'Kozakli (Tuerkei)','lat':38.95,'lng':34.83},
    {'n':'Momotombo (Nicaragua)','lat':12.43,'lng':-86.54},
    {'n':'Platanares (Honduras)','lat':14.5,'lng':-88.9},
    {'n':'Tongonan (Philippinen)','lat':11.25,'lng':124.98},
    {'n':'Makiling-Banahaw (Philippinen)','lat':14.0,'lng':121.5},
    {'n':'Sorik Merapi (Indonesien)','lat':0.68,'lng':99.54},
    {'n':'Wayang Windu (Java, Indonesien)','lat':-7.2,'lng':107.7},
    {'n':'Sarulla (Sumatra, Indonesien)','lat':2.05,'lng':98.87},
    {'n':'Tendaho (Aethiopien)','lat':11.8,'lng':40.96},
])
_m('geo_pin.json','geo_felsformationen',[
    {'n':'Brimham Rocks (North Yorkshire, England)','lat':54.08,'lng':-1.68},
    {'n':'Stranraer Stacks (Schottland)','lat':54.9,'lng':-5.0},
    {'n':'Dades Gorge Felsen (Marokko)','lat':31.52,'lng':-6.0},
    {'n':'Jebel Akhdar Kalkstein (Oman)','lat':23.13,'lng':57.65},
    {'n':'Khao Sok Karst (Thailand)','lat':8.92,'lng':98.53},
    {'n':'Guilin Karstgipfel (Guangxi, China)','lat':25.27,'lng':110.29},
    {'n':'Hunan Wuling Karstpfeiler (China)','lat':28.5,'lng':109.5},
    {'n':'Phang Nga Bay Karst (Thailand)','lat':8.28,'lng':98.53},
    {'n':'Limestone Pinnacles (Sarawak, Malaysia)','lat':4.05,'lng':114.82},
    {'n':'Salar de Tara Felsformationen (Chile)','lat':-23.0,'lng':-67.3},
    {'n':'Quebrada de Humahuaca (Argentinien)','lat':-23.2,'lng':-65.35},
    {'n':'Valle de la Luna (Chile)','lat':-22.9,'lng':-68.26},
    {'n':'Roque de los Muchachos (La Palma)','lat':28.76,'lng':-17.88},
    {'n':'Lune Lake Sandstone (Australien)','lat':-34.0,'lng':148.0},
])
_m('geo_pin.json','geo_hoehlensysteme',[
    {'n':'Font-de-Gaume Hoehle (Frankreich)','lat':44.97,'lng':1.07},
])
_m('geo_pin.json','geo_canyons',[
    {'n':'Guadalupe Canyon (Mexiko/USA)','lat':31.9,'lng':-108.7},
    {'n':'Palouse Falls Canyon (Washington, USA)','lat':46.66,'lng':-118.22},
    {'n':'Letchworth Gorge (New York, USA)','lat':42.57,'lng':-77.98},
    {'n':'Ausable Chasm (New York, USA)','lat':44.52,'lng':-73.48},
    {'n':'Quebrada de Cafayate (Argentinien)','lat':-26.0,'lng':-65.97},
    {'n':'Colca Canyon North Rim (Peru)','lat':-15.4,'lng':-71.9},
    {'n':'Cotahuasi upper (Peru)','lat':-15.2,'lng':-72.9},
    {'n':'Wadi Ghul (Oman)','lat':23.23,'lng':57.35},
    {'n':'Wadi Shab (Oman)','lat':22.88,'lng':59.28},
    {'n':'Wadi Nakhr (Oman - Grand Canyon)','lat':23.22,'lng':57.36},
])
_m('geo_pin.json','geo_geysire',[
    {'n':'Norris Geyser Basin (Yellowstone)','lat':44.72,'lng':-110.71},
    {'n':'Midway Geyser Basin (Yellowstone)','lat':44.52,'lng':-110.83},
    {'n':'Lower Geyser Basin (Yellowstone)','lat':44.54,'lng':-110.84},
    {'n':'Upper Geyser Basin (Yellowstone)','lat':44.46,'lng':-110.84},
    {'n':'Rotorua Wai-O-Tapu Park (NZ)','lat':-38.33,'lng':176.37},
    {'n':'Wairakei Tourist Park (NZ)','lat':-38.63,'lng':176.09},
    {'n':'Orakei Korako (NZ)','lat':-38.47,'lng':176.17},
    {'n':'Tatio North Field (Chile)','lat':-22.3,'lng':-67.9},
    {'n':'Pululu Geysers (Kamtschatka)','lat':54.0,'lng':159.5},
    {'n':'Isluga Geysers (Chile)','lat':-19.2,'lng':-68.8},
    {'n':'Seltun field detail (Island)','lat':63.89,'lng':-22.07},
    {'n':'Geysir Great (Island)','lat':64.31,'lng':-20.302},
    {'n':'Bjarnarflag (Island)','lat':65.63,'lng':-16.87},
    {'n':'Namaskard Mud Pots (Island)','lat':65.64,'lng':-16.83},
    {'n':'Hvitholar Fumaroles (Island)','lat':63.95,'lng':-21.53},
    {'n':'Viti Crater Lake (Island)','lat':65.74,'lng':-16.78},
    {'n':'Askja Caldera (Island)','lat':65.0,'lng':-16.75},
])
_m('geo_pin.json','geo_minen_bohrungen',[
    {'n':'Cerro Matoso Nickel (Kolumbien)','lat':7.89,'lng':-75.53},
    {'n':'Yanacocha Gold (Peru)','lat':-6.88,'lng':-78.5},
    {'n':'Antamina Copper (Peru)','lat':-9.56,'lng':-77.05},
    {'n':'Cerro Verde (Peru)','lat':-16.55,'lng':-71.56},
    {'n':'Toquepala (Peru)','lat':-17.25,'lng':-70.62},
    {'n':'Lomas Bayas (Chile)','lat':-23.67,'lng':-69.83},
    {'n':'Andina Los Bronces (Chile)','lat':-33.1,'lng':-70.28},
    {'n':'Goro Nickel (Neukaledonien)','lat':-22.27,'lng':166.96},
    {'n':'Ramu Nickel (Papua-Neuguinea)','lat':-5.72,'lng':145.6},
    {'n':'Porgera Gold (Papua-Neuguinea)','lat':-5.47,'lng':143.09},
])
_m('geo_pin.json','geo_steilkuesten',[
    {'n':'Nordkapp Kliff (Norwegen)','lat':71.17,'lng':25.78},
    {'n':'Svolvaer Kliffs (Lofoten, Norwegen)','lat':68.23,'lng':14.57},
    {'n':'Runde Island Kliffs (Norwegen)','lat':62.4,'lng':5.63},
    {'n':'Sorvagsvatn Cliff (Faeroeer)','lat':62.07,'lng':-7.28},
    {'n':'Stapafell (Island)','lat':64.77,'lng':-23.53},
    {'n':'Kilnsey Crag (Yorkshire, England)','lat':54.07,'lng':-1.99},
    {'n':'Sonastreten (Norwegen)','lat':60.2,'lng':5.1},
    {'n':'Acapulco Cliff (La Quebrada, Mexiko)','lat':16.84,'lng':-99.91},
])
_m('geo_pin.json','geo_fossilien_fundstaetten',[
    {'n':'Wadi El-Hitan (Aegypten - Archaeoceti)','lat':29.27,'lng':30.02},
    {'n':'Triassic Fauna Canada (BC)','lat':50.0,'lng':-120.0},
    {'n':'Devonian Miguasha Cliffs (Kanada)','lat':48.12,'lng':-66.34},
    {'n':'Permian Karoo Formation (Suedafrika)','lat':-32.0,'lng':24.0},
])
_m('geo_pin.json','geo_nationalparks_geologie',[
    {'n':'Tsingy de Bemaraha NP (Madagaskar)','lat':-18.97,'lng':44.79},
    {'n':'Al-Ahsa Oasis (Saudi-Arabien)','lat':25.37,'lng':49.59},
    {'n':'Sundarbans Mangrove (Bangladesch)','lat':21.97,'lng':89.18},
    {'n':'Socotra Archipelago (Jemen)','lat':12.46,'lng':53.82},
    {'n':'Pico Island Volcanic (Azoren)','lat':38.47,'lng':-28.4},
    {'n':'Lanzarote Timanfaya NP (Spanien)','lat':29.02,'lng':-13.76},
    {'n':'Gran Canaria Caldera (Spanien)','lat':27.97,'lng':-15.6},
    {'n':'Teide NP (Teneriffa, Spanien)','lat':28.27,'lng':-16.64},
    {'n':'Los Volcanes NP (Lanzarote)','lat':29.02,'lng':-13.76},
    {'n':'Ordesa Monte Perdido NP (Spanien)','lat':42.62,'lng':-0.04},
])
_m('geo_pin.json','geo_rifts',[
    {'n':'Lake Tanganyika North End (Burundi)','lat':-4.0,'lng':29.3},
    {'n':'Gulf of Aden Spreading (Yemen)','lat':12.0,'lng':46.0},
    {'n':'Eger Rift Cheb Basin (Tschechien)','lat':50.1,'lng':12.4},
])
_m('geo_pin.json','geo_gletscher',[
    {'n':'Werenskioldbreen (Svalbard)','lat':77.0,'lng':15.5},
    {'n':'Scott Turnerbreen (Svalbard)','lat':78.0,'lng':16.5},
    {'n':'Perito Moreno (Argentinien)','lat':-50.5,'lng':-73.03},
    {'n':'Tasman Glacier (Neuseeland)','lat':-43.5,'lng':170.2},
    {'n':'Franz Josef Glacier (Neuseeland)','lat':-43.45,'lng':170.18},
])
_m('geo_pin.json','geo_wuesten',[
    {'n':'Etosha Pan (Namibia - Salzpfanne)','lat':-18.8,'lng':16.5},
    {'n':'Makgadikgadi Pan (Botswana)','lat':-21.0,'lng':25.0},
    {'n':'Taudeni Basin (Mali)','lat':22.5,'lng':-4.0},
    {'n':'Libyan Desert Erg (Libyen/Aegypten)','lat':25.0,'lng':25.0},
    {'n':'Erg Oriental (Algerien/Tunesien)','lat':32.0,'lng':7.5},
    {'n':'Qaidam Basin (China - Wueste)','lat':37.0,'lng':95.0},
    {'n':'Gashun Gobi (Mongolei/China)','lat':41.0,'lng':105.0},
])

print('\nAll geo second pass complete.')
