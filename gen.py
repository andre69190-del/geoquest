import json, os, re

# â”€â”€ CITIES â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
cities_raw = json.load(open('cities.json', 'r', encoding='utf-8'))
cities_slim = [{'id':c.get('id', c.get('name', 'unknown')),'n':c.get('name') or c.get('asciiName') or '',
                'c':c.get('country',''),'cc':(c.get('countryCode','') or c.get('country_code','') or '').lower(),
                'cont':c.get('continent',''),'sub':c.get('subregion') or c.get('continent',''),
                'pop':c.get('population',0)}
               for c in cities_raw]
CJ = json.dumps(cities_slim, separators=(',',':'), ensure_ascii=False)

# â”€â”€ STATIC DATA â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
CAPITALS = [
  {"country":"France","capital":"Paris","cc":"fr","continent":"Europe","subregion":"Western Europe"},
  {"country":"Germany","capital":"Berlin","cc":"de","continent":"Europe","subregion":"Western Europe"},
  {"country":"Italy","capital":"Rome","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"country":"Spain","capital":"Madrid","cc":"es","continent":"Europe","subregion":"Southern Europe"},
  {"country":"United Kingdom","capital":"London","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
  {"country":"Portugal","capital":"Lisbon","cc":"pt","continent":"Europe","subregion":"Southern Europe"},
  {"country":"Netherlands","capital":"Amsterdam","cc":"nl","continent":"Europe","subregion":"Western Europe"},
  {"country":"Belgium","capital":"Brussels","cc":"be","continent":"Europe","subregion":"Western Europe"},
  {"country":"Switzerland","capital":"Bern","cc":"ch","continent":"Europe","subregion":"Western Europe"},
  {"country":"Austria","capital":"Vienna","cc":"at","continent":"Europe","subregion":"Western Europe"},
  {"country":"Sweden","capital":"Stockholm","cc":"se","continent":"Europe","subregion":"Northern Europe"},
  {"country":"Norway","capital":"Oslo","cc":"no","continent":"Europe","subregion":"Northern Europe"},
  {"country":"Denmark","capital":"Copenhagen","cc":"dk","continent":"Europe","subregion":"Northern Europe"},
  {"country":"Finland","capital":"Helsinki","cc":"fi","continent":"Europe","subregion":"Northern Europe"},
  {"country":"Poland","capital":"Warsaw","cc":"pl","continent":"Europe","subregion":"Eastern Europe"},
  {"country":"Czech Republic","capital":"Prague","cc":"cz","continent":"Europe","subregion":"Eastern Europe"},
  {"country":"Hungary","capital":"Budapest","cc":"hu","continent":"Europe","subregion":"Eastern Europe"},
  {"country":"Romania","capital":"Bucharest","cc":"ro","continent":"Europe","subregion":"Eastern Europe"},
  {"country":"Greece","capital":"Athens","cc":"gr","continent":"Europe","subregion":"Southern Europe"},
  {"country":"Ukraine","capital":"Kyiv","cc":"ua","continent":"Europe","subregion":"Eastern Europe"},
  {"country":"Russia","capital":"Moscow","cc":"ru","continent":"Europe","subregion":"Eastern Europe"},
  {"country":"Turkey","capital":"Ankara","cc":"tr","continent":"Europe","subregion":"Western Asia"},
  {"country":"Serbia","capital":"Belgrade","cc":"rs","continent":"Europe","subregion":"Southern Europe"},
  {"country":"Croatia","capital":"Zagreb","cc":"hr","continent":"Europe","subregion":"Southern Europe"},
  {"country":"Ireland","capital":"Dublin","cc":"ie","continent":"Europe","subregion":"Northern Europe"},
  {"country":"Bulgaria","capital":"Sofia","cc":"bg","continent":"Europe","subregion":"Eastern Europe"},
  {"country":"Slovakia","capital":"Bratislava","cc":"sk","continent":"Europe","subregion":"Eastern Europe"},
  {"country":"Iceland","capital":"Reykjavik","cc":"is","continent":"Europe","subregion":"Northern Europe"},
  {"country":"Estonia","capital":"Tallinn","cc":"ee","continent":"Europe","subregion":"Northern Europe"},
  {"country":"Latvia","capital":"Riga","cc":"lv","continent":"Europe","subregion":"Northern Europe"},
  {"country":"Lithuania","capital":"Vilnius","cc":"lt","continent":"Europe","subregion":"Northern Europe"},
  {"country":"China","capital":"Beijing","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"country":"Japan","capital":"Tokyo","cc":"jp","continent":"Asia","subregion":"Eastern Asia"},
  {"country":"South Korea","capital":"Seoul","cc":"kr","continent":"Asia","subregion":"Eastern Asia"},
  {"country":"India","capital":"New Delhi","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"country":"Pakistan","capital":"Islamabad","cc":"pk","continent":"Asia","subregion":"Southern Asia"},
  {"country":"Bangladesh","capital":"Dhaka","cc":"bd","continent":"Asia","subregion":"Southern Asia"},
  {"country":"Thailand","capital":"Bangkok","cc":"th","continent":"Asia","subregion":"Southeast Asia"},
  {"country":"Vietnam","capital":"Hanoi","cc":"vn","continent":"Asia","subregion":"Southeast Asia"},
  {"country":"Indonesia","capital":"Jakarta","cc":"id","continent":"Asia","subregion":"Southeast Asia"},
  {"country":"Malaysia","capital":"Kuala Lumpur","cc":"my","continent":"Asia","subregion":"Southeast Asia"},
  {"country":"Philippines","capital":"Manila","cc":"ph","continent":"Asia","subregion":"Southeast Asia"},
  {"country":"Singapore","capital":"Singapore City","cc":"sg","continent":"Asia","subregion":"Southeast Asia"},
  {"country":"Saudi Arabia","capital":"Riyadh","cc":"sa","continent":"Asia","subregion":"Western Asia"},
  {"country":"Iran","capital":"Tehran","cc":"ir","continent":"Asia","subregion":"Southern Asia"},
  {"country":"Iraq","capital":"Baghdad","cc":"iq","continent":"Asia","subregion":"Western Asia"},
  {"country":"Israel","capital":"Jerusalem","cc":"il","continent":"Asia","subregion":"Western Asia"},
  {"country":"Jordan","capital":"Amman","cc":"jo","continent":"Asia","subregion":"Western Asia"},
  {"country":"UAE","capital":"Abu Dhabi","cc":"ae","continent":"Asia","subregion":"Western Asia"},
  {"country":"Kazakhstan","capital":"Astana","cc":"kz","continent":"Asia","subregion":"Central Asia"},
  {"country":"Afghanistan","capital":"Kabul","cc":"af","continent":"Asia","subregion":"Southern Asia"},
  {"country":"Myanmar","capital":"Naypyidaw","cc":"mm","continent":"Asia","subregion":"Southeast Asia"},
  {"country":"Cambodia","capital":"Phnom Penh","cc":"kh","continent":"Asia","subregion":"Southeast Asia"},
  {"country":"Taiwan","capital":"Taipei","cc":"tw","continent":"Asia","subregion":"Eastern Asia"},
  {"country":"Mongolia","capital":"Ulaanbaatar","cc":"mn","continent":"Asia","subregion":"Eastern Asia"},
  {"country":"Sri Lanka","capital":"Colombo","cc":"lk","continent":"Asia","subregion":"Southern Asia"},
  {"country":"Nepal","capital":"Kathmandu","cc":"np","continent":"Asia","subregion":"Southern Asia"},
  {"country":"Laos","capital":"Vientiane","cc":"la","continent":"Asia","subregion":"Southeast Asia"},
  {"country":"Nigeria","capital":"Abuja","cc":"ng","continent":"Africa","subregion":"Western Africa"},
  {"country":"Ethiopia","capital":"Addis Ababa","cc":"et","continent":"Africa","subregion":"Eastern Africa"},
  {"country":"Egypt","capital":"Cairo","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"country":"DR Congo","capital":"Kinshasa","cc":"cd","continent":"Africa","subregion":"Middle Africa"},
  {"country":"South Africa","capital":"Pretoria","cc":"za","continent":"Africa","subregion":"Southern Africa"},
  {"country":"Kenya","capital":"Nairobi","cc":"ke","continent":"Africa","subregion":"Eastern Africa"},
  {"country":"Tanzania","capital":"Dodoma","cc":"tz","continent":"Africa","subregion":"Eastern Africa"},
  {"country":"Ghana","capital":"Accra","cc":"gh","continent":"Africa","subregion":"Western Africa"},
  {"country":"Morocco","capital":"Rabat","cc":"ma","continent":"Africa","subregion":"Northern Africa"},
  {"country":"Algeria","capital":"Algiers","cc":"dz","continent":"Africa","subregion":"Northern Africa"},
  {"country":"Sudan","capital":"Khartoum","cc":"sd","continent":"Africa","subregion":"Northern Africa"},
  {"country":"Angola","capital":"Luanda","cc":"ao","continent":"Africa","subregion":"Middle Africa"},
  {"country":"Ivory Coast","capital":"Yamoussoukro","cc":"ci","continent":"Africa","subregion":"Western Africa"},
  {"country":"Senegal","capital":"Dakar","cc":"sn","continent":"Africa","subregion":"Western Africa"},
  {"country":"Uganda","capital":"Kampala","cc":"ug","continent":"Africa","subregion":"Eastern Africa"},
  {"country":"Zimbabwe","capital":"Harare","cc":"zw","continent":"Africa","subregion":"Eastern Africa"},
  {"country":"Tunisia","capital":"Tunis","cc":"tn","continent":"Africa","subregion":"Northern Africa"},
  {"country":"United States","capital":"Washington D.C.","cc":"us","continent":"North America","subregion":"Northern America"},
  {"country":"Canada","capital":"Ottawa","cc":"ca","continent":"North America","subregion":"Northern America"},
  {"country":"Mexico","capital":"Mexico City","cc":"mx","continent":"North America","subregion":"Central America"},
  {"country":"Cuba","capital":"Havana","cc":"cu","continent":"North America","subregion":"Caribbean"},
  {"country":"Guatemala","capital":"Guatemala City","cc":"gt","continent":"North America","subregion":"Central America"},
  {"country":"Costa Rica","capital":"San Jose","cc":"cr","continent":"North America","subregion":"Central America"},
  {"country":"Brazil","capital":"Brasilia","cc":"br","continent":"South America","subregion":"South America"},
  {"country":"Argentina","capital":"Buenos Aires","cc":"ar","continent":"South America","subregion":"South America"},
  {"country":"Colombia","capital":"Bogota","cc":"co","continent":"South America","subregion":"South America"},
  {"country":"Peru","capital":"Lima","cc":"pe","continent":"South America","subregion":"South America"},
  {"country":"Chile","capital":"Santiago","cc":"cl","continent":"South America","subregion":"South America"},
  {"country":"Venezuela","capital":"Caracas","cc":"ve","continent":"South America","subregion":"South America"},
  {"country":"Ecuador","capital":"Quito","cc":"ec","continent":"South America","subregion":"South America"},
  {"country":"Uruguay","capital":"Montevideo","cc":"uy","continent":"South America","subregion":"South America"},
  {"country":"Bolivia","capital":"Sucre","cc":"bo","continent":"South America","subregion":"South America"},
  {"country":"Paraguay","capital":"Asuncion","cc":"py","continent":"South America","subregion":"South America"},
  {"country":"Australia","capital":"Canberra","cc":"au","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"country":"New Zealand","capital":"Wellington","cc":"nz","continent":"Oceania","subregion":"Australia and New Zealand"},
]
CAPJ = json.dumps(CAPITALS, separators=(',',':'), ensure_ascii=False)

RIVERS = [
  {"name":"Nil","country":"Egypt","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Amazonas","country":"Brazil","cc":"br","continent":"South America","subregion":"South America"},
  {"name":"Jangtsekiang","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Mississippi","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Kongo","country":"DR Congo","cc":"cd","continent":"Africa","subregion":"Middle Africa"},
  {"name":"Niger","country":"Nigeria","cc":"ng","continent":"Africa","subregion":"Western Africa"},
  {"name":"Wolga","country":"Russia","cc":"ru","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Mekong","country":"Vietnam","cc":"vn","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Ganges","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Indus","country":"Pakistan","cc":"pk","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Orinoko","country":"Venezuela","cc":"ve","continent":"South America","subregion":"South America"},
  {"name":"Sambesi","country":"Zambia","cc":"zm","continent":"Africa","subregion":"Eastern Africa"},
  {"name":"Rhein","country":"Germany","cc":"de","continent":"Europe","subregion":"Western Europe"},
  {"name":"Donau","country":"Romania","cc":"ro","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Themse","country":"United Kingdom","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Seine","country":"France","cc":"fr","continent":"Europe","subregion":"Western Europe"},
  {"name":"Ebro","country":"Spain","cc":"es","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Po","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Dnjepr","country":"Ukraine","cc":"ua","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Weichsel","country":"Poland","cc":"pl","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Elbe","country":"Germany","cc":"de","continent":"Europe","subregion":"Western Europe"},
  {"name":"Murray","country":"Australia","cc":"au","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"name":"Colorado","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Parana","country":"Argentina","cc":"ar","continent":"South America","subregion":"South America"},
  {"name":"Brahmaputra","country":"Bangladesh","cc":"bd","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Tigris","country":"Iraq","cc":"iq","continent":"Asia","subregion":"Western Asia"},
  {"name":"Euphrat","country":"Iraq","cc":"iq","continent":"Asia","subregion":"Western Asia"},
  {"name":"Irrawaddy","country":"Myanmar","cc":"mm","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Huanghe","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Lena","country":"Russia","cc":"ru","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Ob","country":"Russia","cc":"ru","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Jenissei","country":"Russia","cc":"ru","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Amur","country":"Russia","cc":"ru","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Oranje","country":"South Africa","cc":"za","continent":"Africa","subregion":"Southern Africa"},
  {"name":"Senegalfluss","country":"Senegal","cc":"sn","continent":"Africa","subregion":"Western Africa"},
  {"name":"Volta","country":"Ghana","cc":"gh","continent":"Africa","subregion":"Western Africa"},
  {"name":"Blauer Nil","country":"Ethiopia","cc":"et","continent":"Africa","subregion":"Eastern Africa"},
  {"name":"Loire","country":"France","cc":"fr","continent":"Europe","subregion":"Western Europe"},
  {"name":"Tejo","country":"Portugal","cc":"pt","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Guadalquivir","country":"Spain","cc":"es","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Chao Phraya","country":"Thailand","cc":"th","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Missouri","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Sao Francisco","country":"Brazil","cc":"br","continent":"South America","subregion":"South America"},
  {"name":"Magdalena","country":"Colombia","cc":"co","continent":"South America","subregion":"South America"},
  {"name":"Irtysch","country":"Kazakhstan","cc":"kz","continent":"Asia","subregion":"Central Asia"},
  {"name":"Okawango","country":"Botswana","cc":"bw","continent":"Africa","subregion":"Southern Africa"},
  {"name":"Limpopo","country":"South Africa","cc":"za","continent":"Africa","subregion":"Southern Africa"},
  {"name":"Salween","country":"Myanmar","cc":"mm","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Ural","country":"Russia","cc":"ru","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Illinois","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Yukon","country":"Canada","cc":"ca","continent":"North America","subregion":"Northern America"},
]
RJ = json.dumps(RIVERS, separators=(',',':'), ensure_ascii=False)

# Phase 155: loaded from landmarks.json (content expansion)
LANDMARKS = json.load(open(os.path.join(os.path.dirname(__file__), 'landmarks.json'), encoding='utf-8'))
LMJ = json.dumps(LANDMARKS, separators=(',',':'), ensure_ascii=False)

# Phase 155: loaded from parks.json (content expansion)
NATIONAL_PARKS = json.load(open(os.path.join(os.path.dirname(__file__), 'parks.json'), encoding='utf-8'))
NPJ = json.dumps(NATIONAL_PARKS, separators=(',',':'), ensure_ascii=False)

# Phase 155: loaded from unesco.json (content expansion)
UNESCO_SITES = json.load(open(os.path.join(os.path.dirname(__file__), 'unesco.json'), encoding='utf-8'))
UNJ = json.dumps(UNESCO_SITES, separators=(',',':'), ensure_ascii=False)

CITY_LANDMARKS = [
  {"name":"Tokyo Tower","city":"Tokyo","country":"Japan","cc":"jp","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Senso-ji-Tempel","city":"Tokyo","country":"Japan","cc":"jp","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Tokyo Skytree","city":"Tokyo","country":"Japan","cc":"jp","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Shibuya-Kreuzung","city":"Tokyo","country":"Japan","cc":"jp","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"India Gate","city":"Delhi","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Qutub Minar","city":"Delhi","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Humayuns Grab","city":"Delhi","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Lotus-Tempel","city":"Delhi","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Oriental Pearl Tower","city":"Shanghai","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Der Bund","city":"Shanghai","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Yu-Garten","city":"Shanghai","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Shanghai Tower","city":"Shanghai","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"MASP Museum","city":"Sao Paulo","country":"Brazil","cc":"br","continent":"South America","subregion":"South America"},
  {"name":"Ibirapuera-Park","city":"Sao Paulo","country":"Brazil","cc":"br","continent":"South America","subregion":"South America"},
  {"name":"Pinacoteca do Estado","city":"Sao Paulo","country":"Brazil","cc":"br","continent":"South America","subregion":"South America"},
  {"name":"Mercadao","city":"Sao Paulo","country":"Brazil","cc":"br","continent":"South America","subregion":"South America"},
  {"name":"Aegyptisches Museum Kairo","city":"Cairo","country":"Egypt","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Khan el-Khalili","city":"Cairo","country":"Egypt","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Zitadelle von Kairo","city":"Cairo","country":"Egypt","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Al-Azhar-Moschee","city":"Cairo","country":"Egypt","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Chapultepec-Schloss","city":"Mexico City","country":"Mexico","cc":"mx","continent":"North America","subregion":"Central America"},
  {"name":"Zocalo","city":"Mexico City","country":"Mexico","cc":"mx","continent":"North America","subregion":"Central America"},
  {"name":"Palacio de Bellas Artes","city":"Mexico City","country":"Mexico","cc":"mx","continent":"North America","subregion":"Central America"},
  {"name":"Templo Mayor","city":"Mexico City","country":"Mexico","cc":"mx","continent":"North America","subregion":"Central America"},
  {"name":"Himmelstempel","city":"Beijing","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Sommerpalast","city":"Beijing","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Beihai-Park","city":"Beijing","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"798 Kunstbezirk","city":"Beijing","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Gateway of India","city":"Mumbai","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Marine Drive","city":"Mumbai","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Chhatrapati Shivaji Terminus","city":"Mumbai","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Elephanta-Hoehlen","city":"Mumbai","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Topkapi-Palast","city":"Istanbul","country":"Turkey","cc":"tr","continent":"Europe","subregion":"Western Asia"},
  {"name":"Galata-Turm","city":"Istanbul","country":"Turkey","cc":"tr","continent":"Europe","subregion":"Western Asia"},
  {"name":"Grosser Basar","city":"Istanbul","country":"Turkey","cc":"tr","continent":"Europe","subregion":"Western Asia"},
  {"name":"Dolmabahce-Palast","city":"Istanbul","country":"Turkey","cc":"tr","continent":"Europe","subregion":"Western Asia"},
  {"name":"Buckingham Palace","city":"London","country":"United Kingdom","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Hyde Park","city":"London","country":"United Kingdom","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Westminster Abbey","city":"London","country":"United Kingdom","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Tate Modern","city":"London","country":"United Kingdom","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
]
CLJ = json.dumps(CITY_LANDMARKS, separators=(',',':'), ensure_ascii=False)

# Phase 10: Top 50 subway systems (km, lines)
SUBWAYS = [
  {"city":"Shanghai","country":"China","cc":"cn","km":831,"lines":20},
  {"city":"Beijing","country":"China","cc":"cn","km":783,"lines":27},
  {"city":"Guangzhou","country":"China","cc":"cn","km":621,"lines":16},
  {"city":"Shenzhen","country":"China","cc":"cn","km":559,"lines":16},
  {"city":"Chengdu","country":"China","cc":"cn","km":518,"lines":13},
  {"city":"Delhi","country":"India","cc":"in","km":391,"lines":12},
  {"city":"Wuhan","country":"China","cc":"cn","km":439,"lines":14},
  {"city":"London","country":"United Kingdom","cc":"gb","km":402,"lines":11},
  {"city":"New York","country":"United States","cc":"us","km":380,"lines":36},
  {"city":"Nanjing","country":"China","cc":"cn","km":378,"lines":11},
  {"city":"Moscow","country":"Russia","cc":"ru","km":372,"lines":15},
  {"city":"Chongqing","country":"China","cc":"cn","km":350,"lines":10},
  {"city":"Hangzhou","country":"China","cc":"cn","km":361,"lines":10},
  {"city":"Seoul","country":"South Korea","cc":"kr","km":340,"lines":23},
  {"city":"Tokyo","country":"Japan","cc":"jp","km":337,"lines":13},
  {"city":"Qingdao","country":"China","cc":"cn","km":319,"lines":9},
  {"city":"Madrid","country":"Spain","cc":"es","km":293,"lines":13},
  {"city":"Kuala Lumpur","country":"Malaysia","cc":"my","km":213,"lines":9},
  {"city":"Hong Kong","country":"China","cc":"cn","km":264,"lines":10},
  {"city":"Singapore","country":"Singapore","cc":"sg","km":199,"lines":6},
  {"city":"Washington D.C.","country":"United States","cc":"us","km":188,"lines":6},
  {"city":"Istanbul","country":"Turkey","cc":"tr","km":190,"lines":7},
  {"city":"Los Angeles","country":"United States","cc":"us","km":169,"lines":7},
  {"city":"San Francisco","country":"United States","cc":"us","km":167,"lines":7},
  {"city":"Chicago","country":"United States","cc":"us","km":171,"lines":8},
  {"city":"Paris","country":"France","cc":"fr","km":226,"lines":16},
  {"city":"Mexico City","country":"Mexico","cc":"mx","km":226,"lines":12},
  {"city":"Taipei","country":"Taiwan","cc":"tw","km":131,"lines":6},
  {"city":"Santiago","country":"Chile","cc":"cl","km":136,"lines":7},
  {"city":"Jakarta","country":"Indonesia","cc":"id","km":168,"lines":2},
  {"city":"Bangkok","country":"Thailand","cc":"th","km":127,"lines":4},
  {"city":"Stockholm","country":"Sweden","cc":"se","km":110,"lines":3},
  {"city":"Barcelona","country":"Spain","cc":"es","km":122,"lines":12},
  {"city":"Osaka","country":"Japan","cc":"jp","km":137,"lines":9},
  {"city":"Berlin","country":"Germany","cc":"de","km":155,"lines":9},
  {"city":"Cairo","country":"Egypt","cc":"eg","km":90,"lines":3},
  {"city":"Dubai","country":"UAE","cc":"ae","km":90,"lines":2},
  {"city":"Mumbai","country":"India","cc":"in","km":87,"lines":3},
  {"city":"Athens","country":"Greece","cc":"gr","km":85,"lines":3},
  {"city":"Vienna","country":"Austria","cc":"at","km":83,"lines":5},
  {"city":"Budapest","country":"Hungary","cc":"hu","km":40,"lines":4},
  {"city":"Toronto","country":"Canada","cc":"ca","km":77,"lines":4},
  {"city":"Boston","country":"United States","cc":"us","km":73,"lines":4},
  {"city":"Prague","country":"Czech Republic","cc":"cz","km":65,"lines":3},
  {"city":"Buenos Aires","country":"Argentina","cc":"ar","km":55,"lines":6},
  {"city":"Amsterdam","country":"Netherlands","cc":"nl","km":53,"lines":4},
  {"city":"Lisbon","country":"Portugal","cc":"pt","km":44,"lines":4},
  {"city":"Brussels","country":"Belgium","cc":"be","km":39,"lines":4},
  {"city":"Warsaw","country":"Poland","cc":"pl","km":36,"lines":2},
  {"city":"Sao Paulo","country":"Brazil","cc":"br","km":101,"lines":6},
]
SWJ = json.dumps(SUBWAYS, separators=(',',':'), ensure_ascii=False)

print('Data prepared. Cities:', len(cities_slim), '| Subways:', len(SUBWAYS))


# â”€â”€ LIFESTYLE DATA (Phases 22) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# Phase 155: loaded from food.json (content expansion)
FOOD = json.load(open(os.path.join(os.path.dirname(__file__), 'food.json'), encoding='utf-8'))
FJ  = json.dumps(FOOD,   separators=(',',':'), ensure_ascii=False)

BRANDS = [{'brand': 'Samsung', 'country': 'South Korea', 'cc': 'kr', 'industry': 'Elektronik', 'sub': 'Eastern Asia'}, {'brand': 'LG', 'country': 'South Korea', 'cc': 'kr', 'industry': 'Elektronik', 'sub': 'Eastern Asia'}, {'brand': 'Hyundai', 'country': 'South Korea', 'cc': 'kr', 'industry': 'Autos', 'sub': 'Eastern Asia'}, {'brand': 'Kia', 'country': 'South Korea', 'cc': 'kr', 'industry': 'Autos', 'sub': 'Eastern Asia'}, {'brand': 'Nintendo', 'country': 'Japan', 'cc': 'jp', 'industry': 'Gaming', 'sub': 'Eastern Asia'}, {'brand': 'Sony', 'country': 'Japan', 'cc': 'jp', 'industry': 'Elektronik', 'sub': 'Eastern Asia'}, {'brand': 'Toyota', 'country': 'Japan', 'cc': 'jp', 'industry': 'Autos', 'sub': 'Eastern Asia'}, {'brand': 'Honda', 'country': 'Japan', 'cc': 'jp', 'industry': 'Autos', 'sub': 'Eastern Asia'}, {'brand': 'Yamaha', 'country': 'Japan', 'cc': 'jp', 'industry': 'Musik/Autos', 'sub': 'Eastern Asia'}, {'brand': 'Lenovo', 'country': 'China', 'cc': 'cn', 'industry': 'Elektronik', 'sub': 'Eastern Asia'}, {'brand': 'Alibaba', 'country': 'China', 'cc': 'cn', 'industry': 'E-Commerce', 'sub': 'Eastern Asia'}, {'brand': 'Xiaomi', 'country': 'China', 'cc': 'cn', 'industry': 'Elektronik', 'sub': 'Eastern Asia'}, {'brand': 'Huawei', 'country': 'China', 'cc': 'cn', 'industry': 'Telekommunikation', 'sub': 'Eastern Asia'}, {'brand': 'IKEA', 'country': 'Sweden', 'cc': 'se', 'industry': 'Moebel', 'sub': 'Northern Europe'}, {'brand': 'H&M', 'country': 'Sweden', 'cc': 'se', 'industry': 'Mode', 'sub': 'Northern Europe'}, {'brand': 'Volvo', 'country': 'Sweden', 'cc': 'se', 'industry': 'Autos', 'sub': 'Northern Europe'}, {'brand': 'Spotify', 'country': 'Sweden', 'cc': 'se', 'industry': 'Streaming', 'sub': 'Northern Europe'}, {'brand': 'LEGO', 'country': 'Denmark', 'cc': 'dk', 'industry': 'Spielzeug', 'sub': 'Northern Europe'}, {'brand': 'Bang & Olufsen', 'country': 'Denmark', 'cc': 'dk', 'industry': 'Elektronik', 'sub': 'Northern Europe'}, {'brand': 'Nokia', 'country': 'Finland', 'cc': 'fi', 'industry': 'Telekommunikation', 'sub': 'Northern Europe'}, {'brand': 'Volkswagen', 'country': 'Germany', 'cc': 'de', 'industry': 'Autos', 'sub': 'Western Europe'}, {'brand': 'BMW', 'country': 'Germany', 'cc': 'de', 'industry': 'Autos', 'sub': 'Western Europe'}, {'brand': 'Porsche', 'country': 'Germany', 'cc': 'de', 'industry': 'Autos', 'sub': 'Western Europe'}, {'brand': 'ALDI', 'country': 'Germany', 'cc': 'de', 'industry': 'Einzelhandel', 'sub': 'Western Europe'}, {'brand': 'Airbus', 'country': 'France', 'cc': 'fr', 'industry': 'Luftfahrt', 'sub': 'Western Europe'}, {'brand': 'Renault', 'country': 'France', 'cc': 'fr', 'industry': 'Autos', 'sub': 'Western Europe'}, {'brand': 'Louis Vuitton', 'country': 'France', 'cc': 'fr', 'industry': 'Luxus', 'sub': 'Western Europe'}, {'brand': 'Ferrari', 'country': 'Italy', 'cc': 'it', 'industry': 'Autos', 'sub': 'Southern Europe'}, {'brand': 'Maserati', 'country': 'Italy', 'cc': 'it', 'industry': 'Autos', 'sub': 'Southern Europe'}, {'brand': 'Zara', 'country': 'Spain', 'cc': 'es', 'industry': 'Mode', 'sub': 'Southern Europe'}, {'brand': 'Shell', 'country': 'Netherlands', 'cc': 'nl', 'industry': 'Energie', 'sub': 'Western Europe'}, {'brand': 'Philips', 'country': 'Netherlands', 'cc': 'nl', 'industry': 'Elektronik', 'sub': 'Western Europe'}, {'brand': 'Heineken', 'country': 'Netherlands', 'cc': 'nl', 'industry': 'Bier', 'sub': 'Western Europe'}, {'brand': 'Nestle', 'country': 'Switzerland', 'cc': 'ch', 'industry': 'Lebensmittel', 'sub': 'Western Europe'}, {'brand': 'Rolex', 'country': 'Switzerland', 'cc': 'ch', 'industry': 'Uhren', 'sub': 'Western Europe'}, {'brand': 'Skoda', 'country': 'Czech Republic', 'cc': 'cz', 'industry': 'Autos', 'sub': 'Eastern Europe'}, {'brand': 'Emirates', 'country': 'UAE', 'cc': 'ae', 'industry': 'Luftfahrt', 'sub': 'Western Asia'}, {'brand': 'Petronas', 'country': 'Malaysia', 'cc': 'my', 'industry': 'Energie', 'sub': 'Southeast Asia'}, {'brand': 'Tata', 'country': 'India', 'cc': 'in', 'industry': 'Konglomerat', 'sub': 'Southern Asia'}, {'brand': 'Corona', 'country': 'Mexico', 'cc': 'mx', 'industry': 'Bier', 'sub': 'Central America'}, {'brand': 'Embraer', 'country': 'Brazil', 'cc': 'br', 'industry': 'Luftfahrt', 'sub': 'South America'}, {'brand': 'MTN', 'country': 'South Africa', 'cc': 'za', 'industry': 'Telekommunikation', 'sub': 'Southern Africa'}]
BJ  = json.dumps(BRANDS, separators=(',',':'), ensure_ascii=False)
# Phase 155: Wappen from wappen.json
WAPPEN_JSON = json.load(open(os.path.join(os.path.dirname(__file__), 'wappen.json'), encoding='utf-8'))
WPJ = json.dumps(WAPPEN_JSON, separators=(',',':'), ensure_ascii=False)

CURRENCIES = [{'currency': 'Yen', 'symbol': 'Â¥', 'country': 'Japan', 'cc': 'jp', 'sub': 'Eastern Asia'}, {'currency': 'Won', 'symbol': 'â‚©', 'country': 'South Korea', 'cc': 'kr', 'sub': 'Eastern Asia'}, {'currency': 'Renminbi', 'symbol': 'Â¥', 'country': 'China', 'cc': 'cn', 'sub': 'Eastern Asia'}, {'currency': 'Rupee', 'symbol': 'â‚¹', 'country': 'India', 'cc': 'in', 'sub': 'Southern Asia'}, {'currency': 'Taka', 'symbol': 'à§³', 'country': 'Bangladesh', 'cc': 'bd', 'sub': 'Southern Asia'}, {'currency': 'Baht', 'symbol': 'à¸¿', 'country': 'Thailand', 'cc': 'th', 'sub': 'Southeast Asia'}, {'currency': 'Dong', 'symbol': 'â‚«', 'country': 'Vietnam', 'cc': 'vn', 'sub': 'Southeast Asia'}, {'currency': 'Ringgit', 'symbol': 'RM', 'country': 'Malaysia', 'cc': 'my', 'sub': 'Southeast Asia'}, {'currency': 'Peso', 'symbol': 'â‚±', 'country': 'Philippines', 'cc': 'ph', 'sub': 'Southeast Asia'}, {'currency': 'Pound', 'symbol': 'Â£', 'country': 'United Kingdom', 'cc': 'gb', 'sub': 'Northern Europe'}, {'currency': 'Krone', 'symbol': 'kr', 'country': 'Denmark', 'cc': 'dk', 'sub': 'Northern Europe'}, {'currency': 'Krone', 'symbol': 'kr', 'country': 'Norway', 'cc': 'no', 'sub': 'Northern Europe'}, {'currency': 'Krona', 'symbol': 'kr', 'country': 'Sweden', 'cc': 'se', 'sub': 'Northern Europe'}, {'currency': 'Forint', 'symbol': 'Ft', 'country': 'Hungary', 'cc': 'hu', 'sub': 'Eastern Europe'}, {'currency': 'Zloty', 'symbol': 'zł', 'country': 'Poland', 'cc': 'pl', 'sub': 'Eastern Europe'}, {'currency': 'Koruna', 'symbol': 'Kń', 'country': 'Czech Republic', 'cc': 'cz', 'sub': 'Eastern Europe'}, {'currency': 'Hryvnia', 'symbol': 'â‚´', 'country': 'Ukraine', 'cc': 'ua', 'sub': 'Eastern Europe'}, {'currency': 'Leu', 'symbol': 'lei', 'country': 'Romania', 'cc': 'ro', 'sub': 'Eastern Europe'}, {'currency': 'Ruble', 'symbol': 'â‚½', 'country': 'Russia', 'cc': 'ru', 'sub': 'Eastern Europe'}, {'currency': 'Lira', 'symbol': 'â‚º', 'country': 'Turkey', 'cc': 'tr', 'sub': 'Western Asia'}, {'currency': 'Shekel', 'symbol': 'â‚ª', 'country': 'Israel', 'cc': 'il', 'sub': 'Western Asia'}, {'currency': 'Riyal', 'symbol': 'SAR', 'country': 'Saudi Arabia', 'cc': 'sa', 'sub': 'Western Asia'}, {'currency': 'Dirham', 'symbol': 'AED', 'country': 'UAE', 'cc': 'ae', 'sub': 'Western Asia'}, {'currency': 'Dinar', 'symbol': 'RSD', 'country': 'Serbia', 'cc': 'rs', 'sub': 'Southern Europe'}, {'currency': 'Tenge', 'symbol': 'â‚¸', 'country': 'Kazakhstan', 'cc': 'kz', 'sub': 'Central Asia'}, {'currency': 'Real', 'symbol': 'R$', 'country': 'Brazil', 'cc': 'br', 'sub': 'South America'}, {'currency': 'Peso', 'symbol': '$', 'country': 'Mexico', 'cc': 'mx', 'sub': 'Central America'}, {'currency': 'Peso', 'symbol': '$', 'country': 'Argentina', 'cc': 'ar', 'sub': 'South America'}, {'currency': 'Sol', 'symbol': 'S/', 'country': 'Peru', 'cc': 'pe', 'sub': 'South America'}, {'currency': 'Rand', 'symbol': 'R', 'country': 'South Africa', 'cc': 'za', 'sub': 'Southern Africa'}, {'currency': 'Naira', 'symbol': 'â‚¦', 'country': 'Nigeria', 'cc': 'ng', 'sub': 'Western Africa'}, {'currency': 'Birr', 'symbol': 'Br', 'country': 'Ethiopia', 'cc': 'et', 'sub': 'Eastern Africa'}, {'currency': 'Shilling', 'symbol': 'Sh', 'country': 'Kenya', 'cc': 'ke', 'sub': 'Eastern Africa'}, {'currency': 'Pound', 'symbol': 'EÂ£', 'country': 'Egypt', 'cc': 'eg', 'sub': 'Northern Africa'}, {'currency': 'Dirham', 'symbol': 'MAD', 'country': 'Morocco', 'cc': 'ma', 'sub': 'Northern Africa'}]
CUJ = json.dumps(CURRENCIES, separators=(',',':'), ensure_ascii=False)
print('Lifestyle data: Food', len(FOOD), '| Brands', len(BRANDS), '| Currencies', len(CURRENCIES))


# â”€â”€ LICENSE PLATES (Phase 23B) â”€â”€ loaded at runtime via fetch()
import os as _os

# CSS
_css_path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'geoquest_css.txt')
CSS = open(_css_path,'r',encoding='utf-8').read()

# Phase 28 data payloads – loaded at runtime via fetch()
print('CSS ready:', len(CSS), 'chars')
# JS TEMPLATE
JS = r'''
/* === BETA FEATURES JS (Phase 157) === */

/* ===== TEIL 1: KENNZEICHEN-BINGO ===== */
function generateBingoGrid() {
  const coll = S.collectedPlates || [];
  const collSet = new Set(coll);

  // Verwende alle verfügbaren Kennzeichen (aus Datenbank)
  const allPlates = typeof PLATES !== 'undefined' ? Object.keys(PLATES) : [];

  // Mische gefundene und ungefundene Kennzeichen
  const bingoItems = [];
  const found = allPlates.filter(p => collSet.has(p)).slice(0, 5);
  const notFound = allPlates.filter(p => !collSet.has(p)).slice(0, 4);

  bingoItems.push(...found, ...notFound);

  // Shuffeln
  for (let i = bingoItems.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [bingoItems[i], bingoItems[j]] = [bingoItems[j], bingoItems[i]];
  }

  return bingoItems.slice(0, 9); // Nur 9 Zellen für 3x3
}

function renderBingoGrid() {
  const items = generateBingoGrid();
  const coll = new Set(S.collectedPlates || []);
  let found = 0;

  let html = '<div class="bingo-grid">';
  items.forEach(item => {
    const isFilled = coll.has(item);
    html += '<div class="bingo-cell ' + (isFilled ? 'found' : '') + '">' + item + '</div>';
    if (isFilled) found++;
  });
  html += '</div>';
  html += '<div class="bingo-progress">' + found + ' / 9 Kennzeichen gefunden</div>';

  return html;
}

/* ===== TEIL 1: SPOTTER-STREAKS ===== */
function calculateSpotterStreak() {
  const coll = S.collectedPlates || [];
  if (coll.length === 0) return 0;

  let streak = 0;
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  for (let i = 0; i < 365; i++) {
    const checkDate = new Date(today);
    checkDate.setDate(checkDate.getDate() - i);
    const dateStr = checkDate.toISOString().slice(0, 10);

    let foundThisDay = false;
    coll.forEach(key => {
      const tsKey = 'gq_coll_ts_' + key;
      try {
        const ts = parseInt(localStorage.getItem(tsKey) || '0', 10);
        const foundDate = new Date(ts).toISOString().slice(0, 10);
        if (foundDate === dateStr) foundThisDay = true;
      } catch (e) {}
    });

    if (foundThisDay) {
      streak++;
    } else if (i > 0) {
      break; // Unterbreche wenn keine Funde heute/gestern
    }
  }

  return streak;
}

function renderStreakBadge() {
  const streak = calculateSpotterStreak();
  if (streak === 0) return '';

  const fire = '🔥';
  return '<div class="streak-badge"><span>' + fire + '</span> ' + streak + ' Tage Streak!</div>';
}

/* ===== TEIL 1: WORT-GENERATOR ===== */
function generateWordGenGame() {
  const coll = S.collectedPlates || [];
  const letters = coll
    .map(key => {
      const parts = key.split('::');
      return parts[0]; // Country Code
    })
    .join('')
    .split('')
    .filter(c => /[A-Z]/.test(c));

  if (letters.length === 0) return null;

  return { letters: [...new Set(letters)].sort(), all: letters };
}


function renderFoodQuiz(){
const codes=Object.keys(globalCultureData);
const correctCode=codes[Math.floor(Math.random()*codes.length)];
const correctCountry=COUNTRIES.find(c=>c.c===correctCode);
if(!correctCountry){return '<div>Error: Country not found</div>';}

const correctData=globalCultureData[correctCode];
const wrongCodes=getWrongAnswers(correctCode,3);
const allAnswers=[correctCode].concat(wrongCodes).sort(()=>Math.random()-0.5);

setCorrectAnswerObfuscated(COUNTRIES,correctCode,correctCode);

let html='<div style="padding:20px;text-align:center;">';
html+='<h2>In welchem Land isst man das?</h2>';
html+='<div style="background:#f0f0f0;padding:15px;margin:20px 0;border-radius:8px;font-size:18px;">';
html+='<strong>'+correctData.food+'</strong>';
html+='</div>';
html+='<div style="display:flex;flex-direction:column;gap:10px;">';

for(let i=0;i<allAnswers.length;i++){
const answerCode=allAnswers[i];
const answerCountry=COUNTRIES.find(c=>c.c===answerCode);
const isCorrect=answerCode===correctCode;
const btnStyle='padding:12px;font-size:16px;border:2px solid #ccc;border-radius:6px;cursor:pointer;background:#fff;transition:all 0.2s;';
html+='<button class="quiz-btn" style="'+btnStyle+'" data-quiz-type="food" data-quiz-answer="'+i+'" data-quiz-code="'+correctCode+'">';
html+=answerCountry.country;
html+='</button>';
}

html+='</div></div>';
return html;
}


function renderClimateQuiz(){
const codes=Object.keys(globalCultureData);
const correctCode=codes[Math.floor(Math.random()*codes.length)];
const correctCountry=COUNTRIES.find(c=>c.c===correctCode);
if(!correctCountry){return '<div>Error: Country not found</div>';}

const correctData=globalCultureData[correctCode];
const wrongCodes=getSmartClimateWrongAnswers(correctCode,3);
const allAnswers=[correctCode].concat(wrongCodes).sort(()=>Math.random()-0.5);

setCorrectAnswerObfuscated(COUNTRIES,correctCode,correctCode);

let html='<div style="padding:20px;text-align:center;">';
html+='<h2>Klima-Mysterium</h2>';
html+='<div style="background:#f0f0f0;padding:15px;margin:20px 0;border-radius:8px;font-size:16px;">';
html+='Welches Land hat dieses Klima?<br><strong>'+correctData.climate+'</strong>';
html+='</div>';
html+='<div style="display:flex;flex-direction:column;gap:10px;">';

for(let i=0;i<allAnswers.length;i++){
const answerCode=allAnswers[i];
const answerCountry=COUNTRIES.find(c=>c.c===answerCode);
const isCorrect=answerCode===correctCode;
const btnStyle='padding:12px;font-size:16px;border:2px solid #ccc;border-radius:6px;cursor:pointer;background:#fff;transition:all 0.2s;';
html+='<button class="quiz-btn" style="'+btnStyle+'" data-quiz-type="climate" data-quiz-answer="'+i+'" data-quiz-code="'+correctCode+'">';
html+=answerCountry.country;
html+='</button>';
}

html+='</div></div>';
return html;
}


function renderLandmarkQuiz(){
const codes=Object.keys(globalCultureData);
const correctCode=codes[Math.floor(Math.random()*codes.length)];
const correctCountry=COUNTRIES.find(c=>c.c===correctCode);
if(!correctCountry){return '<div>Error: Country not found</div>';}

const correctData=globalCultureData[correctCode];
const wrongCodes=getWrongAnswers(correctCode,3);
const allAnswers=[correctCode].concat(wrongCodes).sort(()=>Math.random()-0.5);

setCorrectAnswerObfuscated(COUNTRIES,correctCode,correctCode);

let html='<div style="padding:20px;text-align:center;">';
html+='<h2>Wahrzeichen & Sehenswürdigkeiten</h2>';
html+='<div style="background:#f0f0f0;padding:15px;margin:20px 0;border-radius:8px;font-size:16px;">';
html+='Wo befindet sich das?<br><strong>'+correctData.landmark+'</strong>';
html+='</div>';
html+='<div style="display:flex;flex-direction:column;gap:10px;">';

for(let i=0;i<allAnswers.length;i++){
const answerCode=allAnswers[i];
const answerCountry=COUNTRIES.find(c=>c.c===answerCode);
const isCorrect=answerCode===correctCode;
const btnStyle='padding:12px;font-size:16px;border:2px solid #ccc;border-radius:6px;cursor:pointer;background:#fff;transition:all 0.2s;';
html+='<button class="quiz-btn" style="'+btnStyle+'" data-quiz-type="landmark" data-quiz-answer="'+i+'" data-quiz-code="'+correctCode+'">';
html+=answerCountry.country;
html+='</button>';
}

html+='</div></div>';
return html;
}

function handleLandmarkAnswerClick(index,isCorrect){
if(isCorrect){
S.correct++;
S.score+=10;
}else{
S.score-=5;
}
showMessage(isCorrect?'Richtig!':'Falsch!');
setTimeout(startNextRound,1500);
}

function handleClimateAnswerClick(index,isCorrect){
if(isCorrect){
S.correct++;
S.score+=10;
}else{
S.score-=5;
}
showMessage(isCorrect?'Richtig!':'Falsch!');
setTimeout(startNextRound,1500);
}


function renderVersusArea(){
const pair=getVersusCountryPair('area');
const{countryA,countryB,correctIdx}=pair;

setCorrectAnswerObfuscated(COUNTRIES,correctIdx,correctIdx);

let html='<div style="padding:20px;text-align:center;">';
html+='<h2>Welches Land ist größer?</h2>';
html+='<div style="display:flex;justify-content:space-around;margin:20px 0;">';

// Country A
html+='<div style="flex:1;margin-right:10px;">';
html+='<div style="background:#f0f0f0;padding:20px;border-radius:8px;margin-bottom:10px;">';
html+='<strong>'+countryA.country+'</strong><br>';
html+='<span style="color:#666;font-size:14px;">'+formatMetricDisplay(countryA,'area')+'</span>';
html+='</div>';
html+='<button style="padding:12px;width:100%;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;" data-quiz-type="versus" data-quiz-answer="0">';
html+='Größer';
html+='</button>';
html+='</div>';

html+='<div style="flex:0 0 40px;display:flex;align-items:center;justify-content:center;">';
html+='<span style="font-size:24px;">?</span>';
html+='</div>';

// Country B
html+='<div style="flex:1;margin-left:10px;">';
html+='<div style="background:#f0f0f0;padding:20px;border-radius:8px;margin-bottom:10px;">';
html+='<strong>'+countryB.country+'</strong><br>';
html+='<span style="color:#666;font-size:14px;">'+formatMetricDisplay(countryB,'area')+'</span>';
html+='</div>';
html+='<button style="padding:12px;width:100%;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;" data-quiz-type="versus" data-quiz-answer="1">';
html+='Größer';
html+='</button>';
html+='</div>';

html+='</div></div>';
return html;
}







function renderVersusBorders(){
const pair=getVersusCountryPairAdvanced('borders');
if(!pair)return '<div>Error: Not enough data</div>';
const{countryA,countryB,correctIdx}=pair;

setCorrectAnswerObfuscated(COUNTRIES,correctIdx,correctIdx);

let html='<div style="padding:20px;text-align:center;">';
html+='<h2>Welches Land hat mehr Nachbarländer?</h2>';
html+='<div style="display:flex;justify-content:space-around;margin:20px 0;">';

html+='<div style="flex:1;margin-right:10px;">';
html+='<div style="background:#f0f0f0;padding:20px;border-radius:8px;margin-bottom:10px;">';
html+='<strong>'+countryA.country+'</strong><br>';
html+='<span style="color:#666;font-size:14px;">'+formatAdvancedMetricDisplay(countryA,'borders')+'</span>';
html+='</div>';
html+='<button style="padding:12px;width:100%;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;" data-quiz-type="versus" data-quiz-answer="0">';
html+='Mehr';
html+='</button>';
html+='</div>';

html+='<div style="flex:0 0 40px;display:flex;align-items:center;justify-content:center;">';
html+='<span style="font-size:24px;">?</span>';
html+='</div>';

html+='<div style="flex:1;margin-left:10px;">';
html+='<div style="background:#f0f0f0;padding:20px;border-radius:8px;margin-bottom:10px;">';
html+='<strong>'+countryB.country+'</strong><br>';
html+='<span style="color:#666;font-size:14px;">'+formatAdvancedMetricDisplay(countryB,'borders')+'</span>';
html+='</div>';
html+='<button style="padding:12px;width:100%;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;" data-quiz-type="versus" data-quiz-answer="1">';
html+='Mehr';
html+='</button>';
html+='</div>';

html+='</div></div>';
return html;
}

function renderVersusCoast(){
const pair=getVersusCountryPairAdvanced('coast');
if(!pair)return '<div>Error: Not enough coastal countries</div>';
const{countryA,countryB,correctIdx}=pair;

setCorrectAnswerObfuscated(COUNTRIES,correctIdx,correctIdx);

let html='<div style="padding:20px;text-align:center;">';
html+='<h2>Welches Land hat die längere Küstenlinie?</h2>';
html+='<div style="display:flex;justify-content:space-around;margin:20px 0;">';

html+='<div style="flex:1;margin-right:10px;">';
html+='<div style="background:#f0f0f0;padding:20px;border-radius:8px;margin-bottom:10px;">';
html+='<strong>'+countryA.country+'</strong><br>';
html+='<span style="color:#666;font-size:14px;">'+formatAdvancedMetricDisplay(countryA,'coast')+'</span>';
html+='</div>';
html+='<button style="padding:12px;width:100%;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;" data-quiz-type="versus" data-quiz-answer="0">';
html+='Länger';
html+='</button>';
html+='</div>';

html+='<div style="flex:0 0 40px;display:flex;align-items:center;justify-content:center;">';
html+='<span style="font-size:24px;">?</span>';
html+='</div>';

html+='<div style="flex:1;margin-left:10px;">';
html+='<div style="background:#f0f0f0;padding:20px;border-radius:8px;margin-bottom:10px;">';
html+='<strong>'+countryB.country+'</strong><br>';
html+='<span style="color:#666;font-size:14px;">'+formatAdvancedMetricDisplay(countryB,'coast')+'</span>';
html+='</div>';
html+='<button style="padding:12px;width:100%;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;" data-quiz-type="versus" data-quiz-answer="1">';
html+='Länger';
html+='</button>';
html+='</div>';

html+='</div></div>';
return html;
}

function renderVersusElevation(){
const pair=getVersusCountryPairAdvanced('elevation');
if(!pair)return '<div>Error: Not enough data</div>';
const{countryA,countryB,correctIdx}=pair;

setCorrectAnswerObfuscated(COUNTRIES,correctIdx,correctIdx);

let html='<div style="padding:20px;text-align:center;">';
html+='<h2>Welches Land hat den höheren Gipfel?</h2>';
html+='<div style="display:flex;justify-content:space-around;margin:20px 0;">';

html+='<div style="flex:1;margin-right:10px;">';
html+='<div style="background:#f0f0f0;padding:20px;border-radius:8px;margin-bottom:10px;">';
html+='<strong>'+countryA.country+'</strong><br>';
html+='<span style="color:#666;font-size:14px;">'+formatAdvancedMetricDisplay(countryA,'elevation')+'</span>';
html+='</div>';
html+='<button style="padding:12px;width:100%;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;" data-quiz-type="versus" data-quiz-answer="0">';
html+='Höher';
html+='</button>';
html+='</div>';

html+='<div style="flex:0 0 40px;display:flex;align-items:center;justify-content:center;">';
html+='<span style="font-size:24px;">?</span>';
html+='</div>';

html+='<div style="flex:1;margin-left:10px;">';
html+='<div style="background:#f0f0f0;padding:20px;border-radius:8px;margin-bottom:10px;">';
html+='<strong>'+countryB.country+'</strong><br>';
html+='<span style="color:#666;font-size:14px;">'+formatAdvancedMetricDisplay(countryB,'elevation')+'</span>';
html+='</div>';
html+='<button style="padding:12px;width:100%;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;" data-quiz-type="versus" data-quiz-answer="1">';
html+='Höher';
html+='</button>';
html+='</div>';

html+='</div></div>';
return html;
}

function renderVersusGDP(){
const pair=getVersusCountryPairAdvanced('gdp');
if(!pair)return '<div>Error: Not enough data</div>';
const{countryA,countryB,correctIdx}=pair;

setCorrectAnswerObfuscated(COUNTRIES,correctIdx,correctIdx);

let html='<div style="padding:20px;text-align:center;">';
html+='<h2>Welches Land hat das höhere BIP?</h2>';
html+='<p style="color:#666;font-size:14px;">(BIP pro Kopf)</p>';
html+='<div style="display:flex;justify-content:space-around;margin:20px 0;">';

html+='<div style="flex:1;margin-right:10px;">';
html+='<div style="background:#f0f0f0;padding:20px;border-radius:8px;margin-bottom:10px;">';
html+='<strong>'+countryA.country+'</strong><br>';
html+='<span style="color:#666;font-size:14px;">'+formatAdvancedMetricDisplay(countryA,'gdp')+'</span>';
html+='</div>';
html+='<button style="padding:12px;width:100%;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;" data-quiz-type="versus" data-quiz-answer="0">';
html+='Höher';
html+='</button>';
html+='</div>';

html+='<div style="flex:0 0 40px;display:flex;align-items:center;justify-content:center;">';
html+='<span style="font-size:24px;">?</span>';
html+='</div>';

html+='<div style="flex:1;margin-left:10px;">';
html+='<div style="background:#f0f0f0;padding:20px;border-radius:8px;margin-bottom:10px;">';
html+='<strong>'+countryB.country+'</strong><br>';
html+='<span style="color:#666;font-size:14px;">'+formatAdvancedMetricDisplay(countryB,'gdp')+'</span>';
html+='</div>';
html+='<button style="padding:12px;width:100%;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;" data-quiz-type="versus" data-quiz-answer="1">';
html+='Höher';
html+='</button>';
html+='</div>';

html+='</div></div>';
return html;
}

function renderVersusDensity(){
const pair=getVersusCountryPair('density');
const{countryA,countryB,correctIdx}=pair;

setCorrectAnswerObfuscated(COUNTRIES,correctIdx,correctIdx);

let html='<div style="padding:20px;text-align:center;">';
html+='<h2>Welches Land ist dichter besiedelt?</h2>';
html+='<div style="display:flex;justify-content:space-around;margin:20px 0;">';

html+='<div style="flex:1;margin-right:10px;">';
html+='<div style="background:#f0f0f0;padding:20px;border-radius:8px;margin-bottom:10px;">';
html+='<strong>'+countryA.country+'</strong><br>';
html+='<span style="color:#666;font-size:14px;">'+formatMetricDisplay(countryA,'density')+'</span>';
html+='</div>';
html+='<button style="padding:12px;width:100%;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;" data-quiz-type="versus" data-quiz-answer="0">';
html+='Dichter';
html+='</button>';
html+='</div>';

html+='<div style="flex:0 0 40px;display:flex;align-items:center;justify-content:center;">';
html+='<span style="font-size:24px;">?</span>';
html+='</div>';

html+='<div style="flex:1;margin-left:10px;">';
html+='<div style="background:#f0f0f0;padding:20px;border-radius:8px;margin-bottom:10px;">';
html+='<strong>'+countryB.country+'</strong><br>';
html+='<span style="color:#666;font-size:14px;">'+formatMetricDisplay(countryB,'density')+'</span>';
html+='</div>';
html+='<button style="padding:12px;width:100%;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;" data-quiz-type="versus" data-quiz-answer="1">';
html+='Dichter';
html+='</button>';
html+='</div>';

html+='</div></div>';
return html;
}

function renderVersusPopulation(){
const pair=getVersusCountryPair('pop');
const{countryA,countryB,correctIdx}=pair;

setCorrectAnswerObfuscated(COUNTRIES,correctIdx,correctIdx);

let html='<div style="padding:20px;text-align:center;">';
html+='<h2>Welches Land hat mehr Einwohner?</h2>';
html+='<div style="display:flex;justify-content:space-around;margin:20px 0;">';

html+='<div style="flex:1;margin-right:10px;">';
html+='<div style="background:#f0f0f0;padding:20px;border-radius:8px;margin-bottom:10px;">';
html+='<strong>'+countryA.country+'</strong><br>';
html+='<span style="color:#666;font-size:14px;">'+formatMetricDisplay(countryA,'pop')+'</span>';
html+='</div>';
html+='<button style="padding:12px;width:100%;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;" data-quiz-type="versus" data-quiz-answer="0">';
html+='Mehr';
html+='</button>';
html+='</div>';

html+='<div style="flex:0 0 40px;display:flex;align-items:center;justify-content:center;">';
html+='<span style="font-size:24px;">?</span>';
html+='</div>';

html+='<div style="flex:1;margin-left:10px;">';
html+='<div style="background:#f0f0f0;padding:20px;border-radius:8px;margin-bottom:10px;">';
html+='<strong>'+countryB.country+'</strong><br>';
html+='<span style="color:#666;font-size:14px;">'+formatMetricDisplay(countryB,'pop')+'</span>';
html+='</div>';
html+='<button style="padding:12px;width:100%;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;" data-quiz-type="versus" data-quiz-answer="1">';
html+='Mehr';
html+='</button>';
html+='</div>';

html+='</div></div>';
return html;
}

function handleVersusAnswerClick(selectedIdx,correctIdx){
if(selectedIdx===correctIdx){
S.correct++;
S.score+=10;
}else{
S.score-=5;
}
showMessage(selectedIdx===correctIdx?'Richtig!':'Falsch!');
setTimeout(startNextRound,1500);
}

function handleFoodAnswerClick(index,isCorrect){
if(isCorrect){
S.correct++;
S.score+=10;
}else{
S.score-=5;
}
showMessage(isCorrect?'Richtig!':'Falsch!');
setTimeout(startNextRound,1500);
}

function renderWordGenerator() {
  const game = generateWordGenGame();
  if (!game) return '<div style="color:var(--text3)">Sammle erst Kennzeichen!</div>';

  const lettersHtml = game.letters.map(l => '<span class="letter-badge">' + l + '</span>').join('');

  let html = '<div style="margin: 15px 0">';
  html += '<p style="font-size:0.9rem;color:var(--text2)">Verfügbare Buchstaben:</p>';
  html += '<div class="available-letters">' + lettersHtml + '</div>';
  html += '<input type="text" class="word-generator-input" placeholder="Wort bilden..." />';
  html += '<button onclick="checkWord(this.previousElementSibling.value)" style="width:100%;margin-top:8px">ßœberprüfen</button>';
  html += '</div>';

  return html;
}

/* ===== TEIL 2: SIZE GUESSER ===== */
function startSizeGuesserMode() {
  // Wähle zwei zufällige Länder
  const countries = COUNTRIES.filter(c => c.cc && c.c);
  const idx1 = Math.floor(Math.random() * countries.length);
  const idx2 = Math.floor(Math.random() * countries.length);

  return {
    country1: countries[idx1],
    country2: countries[idx2],
  };
}

/* ===== TEIL 2: BORDER CLICKER ===== */
function getBorderCountries(cc) {
  if (typeof NEIGHBORS === 'undefined') return [];
  return NEIGHBORS[cc] || [];
}

/* ===== TEIL 3: LOST IN TRANSLATION ===== */
function getLostInTranslationQuestion(lang) {
  const country = COUNTRIES[Math.floor(Math.random() * COUNTRIES.length)];
  if (!country || !country.cc) return null;

  const langCode = lang === 'de' ? 'de' : lang === 'en' ? 'en' : 'de';
  try {
    const names = new Intl.DisplayNames([langCode], { type: 'region' });
    const translated = names.of(country.cc);
    return { cc: country.cc, country: country.c, translated };
  } catch (e) {
    return null;
  }
}

/* ===== TEIL 3: ANAGRAMM-SPIEL ===== */
function createAnagram(word) {
  const arr = word.split('');
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr.join('');
}

/* Helper: Sicherheit für localStorage */
function safeLocalStorage(key, value) {
  try {
    if (value === undefined) {
      return localStorage.getItem(key);
    } else {
      localStorage.setItem(key, String(value));
    }
  } catch (e) {
    console.warn('[GQ] localStorage fehler:', e);
    return null;
  }
}

/* Fehlerbehandlung für alle Beta-Features */
try {
  // Alle Beta-Features sind mit try/catch geschützt
} catch (e) {
  console.error('[GQ] Beta-Feature Fehler:', e);
}


/* === MAP-MODE TIMER & TRANSLATION (Phase 155) === */

/**
 * Render die ßœberschrift für Map-Mode mit übersetztem Länder-Namen
 * @param {string} cc - Country Code (z.B. "LY")
 * @param {string} mode - Game Mode (z.B. "map_find")
 */
function renderMapModeTitle(cc, mode) {
  const lang = (typeof S !== 'undefined' && S.language) || localStorage.getItem('gq_lang') || 'de';
  const countryName = getCountryName(cc, lang) || cc;

  const titleEl = document.getElementById('map-mode-title');
  if (titleEl) {
    const modeLabel = t('finde_das_land') || 'Finde das Land auf der Karte:';
    titleEl.textContent = `${modeLabel} ${countryName}`;
    titleEl.style.color = 'var(--text)';
  }
}

/**
 * Update NUR den Timer (entkoppelt von Karten-Rendering)
 * Dies verhindert, dass die gesamte Karte neu gezeichnet wird
 */
function updateMapTimer() {
  if (typeof S === 'undefined' || !S.tm) return;

  const timerEl = document.getElementById('map-timer-seconds');
  const barEl = document.getElementById('map-timer-bar-fill');
  const remainingPercent = (S.tm / (S.maxTime || 60)) * 100;

  // Update nur den Timer-Text
  if (timerEl) {
    timerEl.textContent = String(S.tm) + 's';

    // Visuelle Warnung bei weniger als 10 Sekunden
    timerEl.classList.remove('warning', 'critical');
    if (S.tm < 10) {
      timerEl.classList.add('critical');
    } else if (S.tm < 20) {
      timerEl.classList.add('warning');
    }
  }

  // Update nur die Progress-Bar-Breite
  if (barEl) {
    barEl.style.width = remainingPercent + '%';
    barEl.classList.remove('warning', 'critical');
    if (S.tm < 10) {
      barEl.classList.add('critical');
    } else if (S.tm < 20) {
      barEl.classList.add('warning');
    }
  }

  // Wichtig: Starte die Karte NICHT neu
}

/**
 * Initialisiere die Map-Mode UI (wird am Anfang aufgerufen)
 */
function initMapModeUI() {
  if (typeof S === 'undefined') return;

  // Render den Titel mit übersetztem Land
  if (S.currentQuestion && S.currentQuestion.cc) {
    renderMapModeTitle(S.currentQuestion.cc, S.mode);
  }

  // Erstelle Timer-Element falls nicht vorhanden
  const timerContainer = document.getElementById('map-timer-container');
  if (timerContainer && !document.getElementById('map-timer-seconds')) {
    const timerDisplay = document.createElement('div');
    timerDisplay.className = 'timer-display';
    timerDisplay.innerHTML = '<div class="timer-seconds" id="map-timer-seconds">60s</div>' +
      '<div class="timer-bar">' +
      '<div class="timer-bar-fill" id="map-timer-bar-fill" style="width:100%"></div>' +
      '</div>';
    timerContainer.insertBefore(timerDisplay, timerContainer.firstChild);
  }

  // Initialisiere Timer-Update
  updateMapTimer();
}

/**
 * Patch der Haupt-Timer-Funktion um Map-Mode zu unterstützen
 * Wird aufgerufen statt den gesamten Container zu rendern
 */
function tickMapMode() {
  if (typeof S === 'undefined' || S.ph !== 'playing' || S.mode !== 'map_find') return;

  // Update NUR den Timer, nicht die gesamte Karte
  updateMapTimer();

  // Optional: Update die Map-Titel neu, falls Sprache gewechselt wurde
  if (document.getElementById('map-mode-title') && S.currentQuestion && S.currentQuestion.cc) {
    const titleEl = document.getElementById('map-mode-title');
    const currentLang = S.language || localStorage.getItem('gq_lang') || 'de';
    const countryName = getCountryName(S.currentQuestion.cc, currentLang) || S.currentQuestion.cc;
    titleEl.textContent = (t('finde_das_land') || 'Finde das Land:') + ' ' + countryName;
  }
}

/**
 * Ersetze die alte tick()-Logik für Map-Mode
 * Diese Funktion wird vom Haupt-Render() aufgerufen
 */
const oldTick = typeof tick !== 'undefined' ? tick : null;

function tick() {
  if (oldTick) oldTick();

  // Zusätzliche Map-Mode-spezifische Updates
  if (typeof S !== 'undefined' && S.mode === 'map_find') {
    tickMapMode();
  }
}

/**
 * Verhindere SVG/Karten-Resets beim Timer-Update
 * Hook in die Render-Funktion
 */
function preventMapResetOnTimer() {
  // Falls eine updateTimer() Funktion existiert, wrapp sie
  if (typeof updateTimer !== 'undefined') {
    const oldUpdateTimer = updateTimer;
    window.updateTimer = function() {
      if (typeof S !== 'undefined' && S.mode === 'map_find') {
        // Nur Timer aktualisieren, keine SVG-Resets
        updateMapTimer();
      } else {
        oldUpdateTimer();
      }
    };
  }
}

// Initialisiere nach Dokumentladezeit
document.addEventListener('DOMContentLoaded', () => {
  initMapModeUI();
  preventMapResetOnTimer();
});

/* Stelle sicher, dass die Funktion getCountryName existiert */
if (typeof getCountryName === 'undefined') {
  window.getCountryName = function(cc, lang) {
    if (!cc) return null;
    try {
      const names = new Intl.DisplayNames([lang], {type: 'region'});
      return names.of(cc);
    } catch (e) {
      return null;
    }
  };
}

/* Stelle sicher, dass die Funktion t() existiert */
if (typeof t === 'undefined') {
  window.t = function(key) {
    const lang = (typeof S !== 'undefined' && S.language) || localStorage.getItem('gq_lang') || 'de';
    const keys = {
      'finde_das_land': {
        'de': 'Finde das Land auf der Karte:',
        'en': 'Find the country on the map:',
      }
    };
    return keys[key] && keys[key][lang] ? keys[key][lang] : key;
  };
}


/* === MAP UI FUNCTIONS (Phase 154) === */

/**
 * Zeige das Popup für ein Land mit übersetztem Titel
 * @param {string} cc - Country Code (z.B. "DE")
 * @param {string} name - Country Name (z.B. "Germany")
 * @param {number} x - X-Position für Popup
 * @param {number} y - Y-Position für Popup
 */
function showMapPopup(cc, name, x, y) {
  if (!cc || !name) return;

  const lang = (typeof S !== 'undefined' && S.language) || localStorage.getItem('gq_lang') || 'de';
  const translatedName = getCountryName(cc, lang) || name;

  const popup = document.createElement('div');
  popup.className = 'map-popup';
  popup.style.position = 'absolute';
  popup.style.left = (x + 10) + 'px';
  popup.style.top = (y - 10) + 'px';
  popup.innerHTML = `
    <button class="map-popup-close" onclick="this.parentElement.remove()">&times;</button>
    <div class="map-popup-title">${translatedName}</div>
    <div class="map-popup-info">
      <div class="map-popup-info-item"><strong>Code:</strong> ${cc}</div>
      <div class="map-popup-info-item"><strong>Status:</strong> ${isCollected ? 'Gefunden' : 'Nicht gefunden'}</div>
    </div>
  `;

  const mapContainer = document.querySelector('.map-container') || document.body;
  mapContainer.appendChild(popup);

  // Entferne Popup nach 5 Sekunden oder bei Click außerhalb
  setTimeout(() => {
    try { popup.remove(); } catch (e) {}
  }, 5000);
}

/**
 * Highlight eine bestimmte Landkreis/Region auf der Karte
 * @param {string} cc - Country Code
 * @param {boolean} found - Ob das Land gefunden wurde
 */
function highlightMapRegion(cc, found) {
  const paths = document.querySelectorAll(`svg.map path[data-country="${cc}"]`);
  paths.forEach(path => {
    if (found) {
      path.classList.add('found');
    } else {
      path.classList.remove('found');
    }
  });
}

/**
 * Initialisiere alle Karten-Marker mit ßœbersetzungen
 */
function initMapMarkers() {
  const lang = (typeof S !== 'undefined' && S.language) || localStorage.getItem('gq_lang') || 'de';

  // Suche alle Marker/Label-Elemente
  const markers = document.querySelectorAll('.map-marker, .map-pin, .country-label');
  markers.forEach(marker => {
    const cc = marker.getAttribute('data-country') || marker.getAttribute('data-cc');
    if (cc) {
      const translatedName = getCountryName(cc, lang) || marker.textContent;
      // Optional: Update Text wenn erforderlich
      // marker.textContent = translatedName;
    }
  });

  // Setze initiale 'found'-Klassen für alle gesammelten Länder
  if (typeof S !== 'undefined' && S.collectedPlates) {
    S.collectedPlates.forEach(plateKey => {
      const cc = extractCountryFromPlateKey(plateKey);
      if (cc) {
        highlightMapRegion(cc, true);
      }
    });
  }
}

/**
 * Extrahiere Country Code aus Kennzeichen-Key (z.B. "DE::CODE" →’ "DE")
 */
function extractCountryFromPlateKey(key) {
  if (!key || typeof key !== 'string') return null;
  const parts = key.split('::');
  return parts[0] || null;
}

/**
 * Update die Map-Anzeige nach Sprach-Wechsel
 */
function updateMapLanguage(lang) {
  const markers = document.querySelectorAll('.map-marker, .map-pin, .country-label');
  markers.forEach(marker => {
    const cc = marker.getAttribute('data-country') || marker.getAttribute('data-cc');
    if (cc) {
      const translatedName = getCountryName(cc, lang);
      if (translatedName && marker.getAttribute('data-show-label') !== 'false') {
        marker.textContent = translatedName;
      }
    }
  });
}

// Triggere initMapMarkers beim Seitenaufbau
document.addEventListener('DOMContentLoaded', initMapMarkers);


/* === LEGAL MODAL FUNCTIONS (Phase 152) === */
function showLegalModal(type) {
  const modalId = type === 'impressum' ? 'legal-impressum-modal' : 'legal-privacy-modal';
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden'; /* prevent background scroll */
  }
}

function closeLegalModal(type) {
  const modalId = type === 'impressum' ? 'legal-impressum-modal' : 'legal-privacy-modal';
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
  }
}

/* Close modal on overlay click */
document.addEventListener('click', function(e) {
  if (e.target.classList && e.target.classList.contains('legal-modal-overlay')) {
    const modal = e.target.parentElement;
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
  }
});

/* Close on Escape key */
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    const impressum = document.getElementById('legal-impressum-modal');
    const privacy = document.getElementById('legal-privacy-modal');
    if (impressum && impressum.style.display !== 'none') {
      impressum.style.display = 'none';
      document.body.style.overflow = 'auto';
    }
    if (privacy && privacy.style.display !== 'none') {
      privacy.style.display = 'none';
      document.body.style.overflow = 'auto';
    }
  }
});



const SUPABASE_URL  = "https://lpwcqvxajahiftvwxovq.supabase.co";
const SUPABASE_ANON = "sb_publishable_HL6cIlPOtVAdkjycaiceGQ_CBNFF-dG";
/* ADMIN_EMAIL removed – use Supabase trigger instead */

/* PAYMENT CONFIG */
const STRIPE_PK = "";
function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#x27;");}

const PAY_PRODUCTS = [
  {id:"coins_500",  name:"500 GeoCoins",         price:"1,99 \u20ac", coins:500,  premium:false, desc:"Einmalkauf \u2022 sofort gutgeschrieben"},
  {id:"coins_2000", name:"2.000 GeoCoins",        price:"4,99 \u20ac", coins:2000, premium:false, desc:"Beliebt \u2022 Sparpreis", featured:true},
  {id:"premium_m",  name:"Premium Monatlich",     price:"3,99 \u20ac", coins:200,  premium:true,  months:1,  desc:"Alle Modi \u2022 Keine Werbung"},
  {id:"premium_y",  name:"Premium J\u00e4hrlich", price:"29,99 \u20ac",coins:1000, premium:true,  months:12, desc:"40% g\u00fcnstiger \u2022 +1.000 Coins", featured:true},
  {id:"pu_5050",   name:"3\u00d7 50/50-Joker",   price:"0,99 \u20ac", coins:0,   premium:false, pu:"five0", pu_qty:3, desc:"2 falsche Antworten entfernen"},
  {id:"pu_freeze", name:"3\u00d7 Zeit-Stopp",     price:"0,99 \u20ac", coins:0,   premium:false, pu:"freeze", pu_qty:3, desc:"Timer 10 Sekunden einfrieren"},
];

/* LANGUAGE */
/* â”€â”€ Phase 47/48: i18n – DE / EN / PL â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
const LANG={
de:{
  play:"SPIELEN",again:"NOCHMAL",menu:"Hauptmenü",board:"Bestenliste",pass:"Reisepass",
  fav_empty:"Noch keine Favoriten gespeichert",
  profile:"Profil",stats:"Statistik",casual:"Casual",hardcore:"Hardcore",rounds:"Runden",
  btn_collect:"Sammeln",btn_back:"Zurück zum Hauptmenü",btn_next:"Weiter →’",
  btn_again:"Nochmal",btn_menu:"Hauptmenü",btn_adapt:"Anpassen",
  spotter_title:"\u{1F697} Roadtrip-Spotter",
  spotter_hint:"Kennzeichen gesehen? Sofort eintragen!",
  spotter_all:"Alle Länder",spotter_unknown:"Unbekanntes Kennzeichen",
  spotter_not_in:"nicht in",spotter_but_in:"aber in",spotter_no_region:"hat keine Regionen – gib \"{code}\" ein\!",
  album_title:"\u{1F4D4} Kennzeichen-Album",album_list:"\u{1F4DD} Liste",album_map:"\u{1F5FA} Karte",
  album_empty_country:"Noch nichts aus {country} gesammelt – nutze den Spotter!",
  album_empty:"Noch nichts gesammelt!\nSpiele EU-Kennzeichen oder benutze den Spotter.",
  album_codes:"Kürzel",
  hl_higher:"⬆️ Mehr / Länger / Größer",hl_lower:"⬇️ Weniger / Kürzer / Kleiner",
  hl_more:"⬆️ Mehr Einwohner",hl_less:"⬇️ Weniger Einwohner",
  hl_longer:"⬆️ Länger",hl_shorter:"⬇️ Kürzer",hl_bigger:"⬆️ Größer (Fläche)",hl_smaller:"⬇️ Kleiner (Fläche)",
  loc_detected:"Du bist in {country}",loc_adapt:"Anpassen",
  q_city:"In welchem Land liegt diese Stadt?",q_flag:"Welches Land zeigt diese Flagge?",
  q_capital:"Zu welchem Land gehört diese Hauptstadt?",q_river:"In welchem Land liegt dieser Fluss?",
  q_landmark:"In welchem Land liegt dieses Wahrzeichen?",q_park:"In welchem Land liegt dieser Nationalpark?",
  q_unesco:"In welchem Land liegt dieses UNESCO-Welterbe?",q_citymark:"Zu welcher Stadt gehört dieses Wahrzeichen?",
  q_subway:"In welcher Stadt ist diese U-Bahn?",q_flagsel:"Welche Flagge gehört zu …",
  q_rcapital:"Was ist die Hauptstadt von …?",q_rcity:"Welche Stadt liegt in …?",
  q_rriver:"Welcher Fluss fließt durch …?",q_outline:"Welches Land hat diese Form?",
  q_food:"Aus welchem Land kommt dieses Gericht?",q_brand:"Aus welchem Land kommt diese Marke?",
  q_currency:"Zu welchem Land gehört diese Währung?",q_curr_real:"Welche Währung hat …",
  q_pop_compare:"Mehr oder weniger Einwohner?",
  q_hl_pop:"Mehr Einwohner als {a}?",q_hl_river:"Länger als {a}?",q_hl_area:"Größer als {a}?",q_hl_gdp:"Höheres BIP/Kopf als {a}?",q_hl_density:"Dichter besiedelt als {a}?",q_hl_elevation:"Höherer Gipfel als {a}?",q_hl_coastline:"Längere Küste als {a}?",q_hl_borders:"Mehr Nachbarn als {a}?",q_hl_lifeexp:"Länger leben als in {a}?",q_hl_median_age:"Höheres Medianalter als {a}?",q_hl_forest:"Mehr Wald als {a}?",
  q_neighbor:"Welches Land grenzt an…?",q_neighbor_not:"Grenzt NICHT an…?",
  q_plates_casual:"Woher kommt dieses Kennzeichen?",q_plates_hard:"Region erkennen – kein Tipp!",
  q_river_real:"Durch welches Land fließt dieser Fluss?",q_map_guess:"Finde das Land auf der Karte",
  fb_correct:"✓“ Richtig! +{pts}",fb_wrong:"✗ Falsch → {ans}",fb_time:"⏱ Zeit! → {ans}",
  plates_more:"+{n} weitere",pct_complete:"{pct}% vollständig",
  spotter_dup:"📋 {code} ({country}) bereits gesammelt!",
  map_unavail:"Karte nicht verfügbar",map_loading:"Kartendaten werden geladen…",
  q_subway_km:"Wie lang ist das U-Bahn-Netz … (km)?",q_subway_lines:"Wie viele U-Bahn-Linien hat …?",
  ob_welcome:"Willkommen bei GeoQuest",ob_sub1:"Das Geografie-Quiz – sammle Stempel, steige in der Liga auf!",ob_difficulty:"Schwierigkeitsgrad",ob_diff_sub:"W\u00e4hle deinen Stil. \u00c4nderbar jederzeit.",
  ob_diff_casual_desc:"Gro\u00dfe St\u00e4dte \u2022 12 Sek.",ob_diff_hc_desc:"Alle St\u00e4dte \u2022 8 Sek.",ob_back:"\u2190 Zur\u00fcck",ob_modes_title:"Spielmodi",
  ob_modes_sub:"19 Modi, ein Ziel: Die Welt kennenlernen.",ob_more_modes:"\u2026 und 16 weitere Modi",ob_start:"\u{1F680} Los geht's!",ob_have_account:"Ich habe bereits einen Account",ob_register:"Neu hier? Registrieren",
  home_hi:"Hallo, {name} \u{1F44B}",home_guest:"Willkommen, Gast \u{1F30D}",home_save:"\u{1F510} Fortschritt sichern",home_pvp_sub:"Echtzeit gegen einen Freund spielen",
  ob_mode1_name:"Stadt →’ Land",ob_mode1_desc:"Welchem Land gehört diese Stadt?",ob_mode2_name:"EU-Kennzeichen",ob_mode2_desc:"Woher kommt dieses Kennzeichen?",ob_mode3_name:"U-Bahn-Netz",ob_mode3_desc:"Linien und km der Metros.",
  language_select:"SPRACHE",
  badge_beta:"Beta",beta_warning:"Spielbar, aber es k\u00f6nnen noch Fehler auftreten.",
  rotate_device:"Bitte drehe dein Ger\u00e4t ins Querformat \u{1F4F1}\u27A1\u{1F5FA}",
  diff_desc_casual:"\u{1F7E2} Casual: Entspannt \u00b7 Kein Zeitlimit \u00b7 \u221e Leben",diff_desc_hc:"\u{1F525} Hardcore: Der Klassiker \u00b7 Kein Zeitlimit \u00b7 3 Leben",diff_desc_surv:"\u{1F480} Survival: Gegen die Uhr \u00b7 8 Sekunden \u00b7 3 Leben",
  hud_lives:"LEBEN",score_mult_max:"Max-Multiplikator",score_time_bonus:"Zeit-Bonus",pts_abbr:"Pkt.",score_correct_lbl:"richtig",mode_wappen:"Wappen-Meister",mode_slf:"Stadt, Land, Fluss",mode_euro:"Euro-M\u00fcnzen"
},
en:{
  play:"PLAY",again:"PLAY AGAIN",menu:"Main Menu",board:"Leaderboard",pass:"Passport",
  fav_empty:"No favourites saved yet",
  profile:"Profile",stats:"Stats",casual:"Casual",hardcore:"Hardcore",rounds:"Rounds",
  btn_collect:"Collect",btn_back:"Back to Main Menu",btn_next:"Next →’",
  btn_again:"Play Again",btn_menu:"Main Menu",btn_adapt:"Adapt",
  spotter_title:"\u{1F697} Road Trip Spotter",
  spotter_hint:"Spotted a plate? Log it now!",
  spotter_all:"All Countries",spotter_unknown:"Unknown plate",
  spotter_not_in:"not in",spotter_but_in:"but found in",spotter_no_region:"has no regions – enter \"{code}\" to collect\!",
  album_title:"\u{1F4D4} Plate Collection",album_list:"\u{1F4DD} List",album_map:"\u{1F5FA} Map",
  album_empty_country:"Nothing from {country} yet – use the Spotter!",
  album_empty:"Nothing collected yet!\nPlay EU plates or use the Spotter above.",
  album_codes:"codes",
  hl_higher:"⬆️ More / Longer / Larger",hl_lower:"⬇️ Less / Shorter / Smaller",
  hl_more:"⬆️ More Population",hl_less:"⬇️ Less Population",
  hl_longer:"⬆️ Longer",hl_shorter:"⬇️ Shorter",hl_bigger:"⬆️ Larger (Area)",hl_smaller:"⬇️ Smaller (Area)",
  loc_detected:"You are in {country}",loc_adapt:"Adapt",
  q_city:"In which country is this city?",q_flag:"Which country does this flag belong to?",
  q_capital:"Which country has this capital?",q_river:"In which country is this river?",
  q_landmark:"In which country is this landmark?",q_park:"In which country is this national park?",
  q_unesco:"In which country is this UNESCO site?",q_citymark:"Which city has this landmark?",
  q_subway:"Which city has this metro?",q_flagsel:"Which flag belongs to…",
  q_rcapital:"What is the capital of…?",q_rcity:"Which city is in…?",
  q_rriver:"Which river flows through…?",q_outline:"Which country has this shape?",
  q_food:"Which country does this dish come from?",q_brand:"Which country does this brand come from?",
  q_currency:"Which country uses this currency?",q_curr_real:"What currency does…",
  q_pop_compare:"More or fewer inhabitants?",
  q_hl_pop:"More inhabitants than {a}?",q_hl_river:"Longer than {a}?",q_hl_area:"Larger than {a}?",q_hl_gdp:"Higher GDP/capita than {a}?",q_hl_density:"More densely populated than {a}?",q_hl_elevation:"Higher peak than {a}?",q_hl_coastline:"Longer coastline than {a}?",q_hl_borders:"More neighbours than {a}?",q_hl_lifeexp:"Longer life expectancy than {a}?",q_hl_median_age:"Higher median age than {a}?",q_hl_forest:"More forest than {a}?",
  q_neighbor:"Which country borders…?",q_neighbor_not:"Does NOT border…?",
  q_plates_casual:"Which country has this plate?",q_plates_hard:"Identify the region – no hint!",
  q_river_real:"Which country does this river flow through?",q_map_guess:"Find the country on the map",
  fb_correct:"✓“ Correct! +{pts}",fb_wrong:"✗ Wrong → {ans}",fb_time:"⏱ Time! → {ans}",
  plates_more:"+{n} more",pct_complete:"{pct}% complete",
  spotter_dup:"📋 {code} ({country}) already collected!",
  map_unavail:"Map not available",map_loading:"Loading map data…",
  q_subway_km:"How long is the metro network … (km)?",q_subway_lines:"How many metro lines does … have?",
  ob_welcome:"Welcome to GeoQuest",ob_sub1:"The geography quiz – collect stamps, climb the league!",ob_difficulty:"Difficulty",ob_diff_sub:"Choose your style. Changeable at any time.",
  ob_diff_casual_desc:"Major cities \u2022 12 sec.",ob_diff_hc_desc:"All cities \u2022 8 sec.",ob_back:"\u2190 Back",ob_modes_title:"Game Modes",
  ob_modes_sub:"19 modes, one goal: know the world.",ob_more_modes:"\u2026 and 16 more modes",ob_start:"\u{1F680} Let's go!",ob_have_account:"I already have an account",ob_register:"New here? Register",
  home_hi:"Hi, {name} \u{1F44B}",home_guest:"Welcome, Guest \u{1F30D}",home_save:"\u{1F510} Save progress",home_pvp_sub:"Play in real time against a friend",
  ob_mode1_name:"City →’ Country",ob_mode1_desc:"Which country does this city belong to?",ob_mode2_name:"EU Licence Plates",ob_mode2_desc:"Where does this number plate come from?",ob_mode3_name:"Metro Networks",ob_mode3_desc:"Lines and km of metro systems.",
  language_select:"LANGUAGE",
  badge_beta:"Beta",beta_warning:"Playable, but may still contain bugs.",
  rotate_device:"Please rotate your device to landscape mode \u{1F4F1}\u27A1\u{1F5FA}",
  diff_desc_casual:"\u{1F7E2} Casual: Relaxed \u00b7 No time limit \u00b7 \u221e Lives",diff_desc_hc:"\u{1F525} Hardcore: Classic \u00b7 No time limit \u00b7 3 Lives",diff_desc_surv:"\u{1F480} Survival: Against the clock \u00b7 8s \u00b7 3 Lives",
  hud_lives:"LIVES",score_mult_max:"Max Multiplier",score_time_bonus:"Time Bonus",pts_abbr:"pts.",score_correct_lbl:"correct",mode_wappen:"Coat of Arms",mode_slf:"City-Country-River",mode_euro:"Euro Coins"
},
pl:{
  play:"GRAJ",again:"ZAGRAJ PONOWNIE",menu:"Menu",board:"Ranking",pass:"Paszport",
  fav_empty:"Nie zapisano jeszcze ulubionych",
  profile:"Profil",stats:"Statystyki",casual:"Zwykły",hardcore:"Trudny",rounds:"Rundy",
  btn_collect:"Zbierz",btn_back:"Powrót do menu",btn_next:"Dalej →’",
  btn_again:"Zagraj ponownie",btn_menu:"Menu",btn_adapt:"Dostosuj",
  spotter_title:"\u{1F697} Spotter Podróżnika",
  spotter_hint:"Widzisz tablicę? Zapisz jń… od razu!",
  spotter_all:"Wszystkie kraje",spotter_unknown:"Nieznana tablica",
  spotter_not_in:"nie ma w",spotter_but_in:"ale jest w",
  album_title:"\u{1F4D4} Album Tablic",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Mapa",
  album_empty_country:"Nic z {country} jeszcze – użyj Spottera!",
  album_empty:"Nic jeszcze nie zebrano!\nGraj w tablice EU lub użyj Spottera.",
  album_codes:"kodów",
  hl_higher:"⬆️ Więcej / Dłużej / Większy",hl_lower:"⬇️ Mniej / Krócej / Mniejszy",
  hl_more:"⬆️ Więcej mieszkaŚ„ców",hl_less:"⬇️ Mniej mieszkaŚ„ców",
  loc_detected:"JesteŚ› w {country}",loc_adapt:"Dostosuj",
  q_city:"W jakim kraju leży to miasto?",q_flag:"Jakie paŚ„stwo ma tę flagę?",
  q_capital:"Do jakiego kraju należy ta stolica?",q_river:"W jakim kraju płynie ta rzeka?",
  q_landmark:"W jakim kraju jest ta atrakcja?",q_park:"W jakim kraju jest ten park narodowy?",
  q_unesco:"W jakim kraju jest to dziedzictwo UNESCO?",q_citymark:"Do jakiego miasta należy ta atrakcja?",
  q_subway:"W jakim mieŚ›cie jest to metro?",q_flagsel:"Która flaga należy do…",
  q_rcapital:"Jaka jest stolica …?",q_rcity:"Które miasto leży w …?",
  q_rriver:"Która rzeka płynie przez …?",q_outline:"Które paŚ„stwo ma ten kształt?",
  q_food:"Z jakiego kraju pochodzi to danie?",q_brand:"Z jakiego kraju pochodzi ta marka?",
  q_currency:"Do jakiego kraju należy ta waluta?",q_curr_real:"Jakń… walutę ma…",
  q_pop_compare:"Więcej czy mniej mieszkaŚ„ców?",
  q_hl_pop:"Więcej mieszkaŚ„ców niż {a}?",q_hl_river:"Dłuższa niż {a}?",q_hl_area:"Większy niż {a}?",
  q_neighbor:"Który kraj graniczy z…?",q_neighbor_not:"NIE graniczy z…?",
  q_plates_casual:"Do jakiego kraju należy ta tablica?",q_plates_hard:"Jaki region ma tę tablicę?",
  q_river_real:"Przez jaki kraj płynie ta rzeka?",q_map_guess:"ZnajdŚº kraj na mapie",
  fb_correct:"✓“ Dobrze! +{pts}",fb_wrong:"✗ Błąd → {ans}",fb_time:"⏱ Czas! → {ans}",
  plates_more:"+{n} więcej",pct_complete:"{pct}% ukoŚ„czono",
  spotter_dup:"📋 {code} ({country}) już zebrane!",
  map_unavail:"Mapa niedostępna",map_loading:"Śadowanie mapy…",
  q_subway_km:"Jak długa jest sieć metra … (km)?",q_subway_lines:"Ile linii metra ma …?",
  hl_longer:"⬆️ Dłuższy",hl_shorter:"⬇️ Krótszy",hl_bigger:"⬆️ Większy (obszar)",hl_smaller:"⬇️ Mniejszy (obszar)",
  ob_welcome:"Witaj w GeoQuest",ob_sub1:"Quiz geograficzny – zbieraj stemple, awansuj w lidze!",ob_difficulty:"Poziom trudnoŚ›ci",ob_diff_sub:"Wybierz swój styl. ZmieŚ„ w dowolnym momencie.",
  ob_diff_casual_desc:"Duże miasta • 12 sek.",ob_diff_hc_desc:"Wszystkie miasta • 8 sek.",ob_back:"→ Wróć",ob_modes_title:"Tryby gry",
  ob_modes_sub:"19 trybów, jeden cel: poznać Ś›wiat.",ob_more_modes:"… i 16 kolejnych trybów",ob_start:"\u{1F680} Zaczynamy!",ob_have_account:"Mam już konto",ob_register:"Nowy? Zarejestruj się",
  home_hi:"CzeŚ›ć, {name} \u{1F44B}",home_guest:"Witaj, GoŚ›ciu \u{1F30D}",home_save:"\u{1F510} Zapisz postęp",home_pvp_sub:"Graj w czasie rzeczywistym z przyjacielem",
  ob_mode1_name:"Miasto →’ Kraj",ob_mode1_desc:"Do jakiego kraju należy to miasto?",ob_mode2_name:"Tablice UE",ob_mode2_desc:"Skń…d pochodzi ta tablica?",ob_mode3_name:"Sieci metra",ob_mode3_desc:"Linie i km metra.",
  language_select:"Jń˜ZYK",
  badge_beta:"Beta",beta_warning:"Grywalny, ale mogń… wystń…pić błędy.",
  rotate_device:"Obróć urzń…dzenie poziomo \u{1F4F1}\u27A1\u{1F5FA}",
  diff_desc_casual:"\u{1F7E2} Casual: Relaks · Bez limitu czasu · ∞ życia",
  diff_desc_hc:"\u{1F525} Hardcore: Klasyk · Bez limitu czasu · 3 Ś»ycia",
  diff_desc_surv:"\u{1F480} Survival: Na czas · 8 sekund · 3 życia",
  hud_lives:"Ś»YCIA",
  score_mult_max:"Maks Mnożnik",
  score_time_bonus:"Bonus Czasu",
  pts_abbr:"pkt.",
  score_correct_lbl:"poprawnie",
  mode_wappen:"Herby",
  mode_slf:"Miasto-Kraj-Rzeka",
  mode_euro:"Monety Euro"
},
fr:{
  play:"JOUER",again:"REJOUER",menu:"Menu principal",board:"Classement",pass:"Passeport",
  fav_empty:"Aucun favori enregistré pour l'instant",
  profile:"Profil",stats:"Statistiques",casual:"Casual",hardcore:"Hardcore",rounds:"Manches",
  btn_collect:"Collecter",btn_back:"Retour au menu",btn_next:"Suivant →’",
  btn_again:"Rejouer",btn_menu:"Menu principal",btn_adapt:"Adapter",
  spotter_title:"\u{1F697} Spotter de voyage",
  spotter_hint:"Vu une plaque ? Notez-la !",
  spotter_all:"Tous les pays",spotter_unknown:"Plaque inconnue",
  spotter_not_in:"pas dans",spotter_but_in:"mais dans",
  album_title:"\u{1F4D4} Collection de plaques",album_list:"\u{1F4DD} Liste",album_map:"\u{1F5FA} Carte",
  album_empty_country:"Rien de {country} encore – utilisez le Spotter !",
  album_empty:"Rien collecté encore !\nJouez aux plaques UE ou utilisez le Spotter.",
  album_codes:"codes",
  hl_higher:"⬆️ Plus / Plus long / Plus grand",hl_lower:"⬇️ Moins / Plus court / Plus petit",
  hl_more:"⬆️ Plus d'habitants",hl_less:"⬇️ Moins d'habitants",
  loc_detected:"Vous ßªtes en {country}",loc_adapt:"Adapter",
  q_city:"Dans quel pays se trouve cette ville ?",q_flag:"Quel pays a ce drapeau ?",
  q_capital:"ß€ quel pays appartient cette capitale ?",q_river:"Dans quel pays coule ce fleuve ?",
  q_landmark:"Dans quel pays se trouve ce monument ?",q_park:"Dans quel pays se trouve ce parc national ?",
  q_unesco:"Dans quel pays se trouve ce site UNESCO ?",q_citymark:"ß€ quelle ville appartient ce monument ?",
  q_subway:"Dans quelle ville se trouve ce métro ?",q_flagsel:"Quel drapeau appartient ß …",
  q_rcapital:"Quelle est la capitale de… ?",q_rcity:"Quelle ville est dans… ?",
  q_rriver:"Quel fleuve traverse… ?",q_outline:"Quel pays a cette forme ?",
  q_food:"De quel pays vient ce plat ?",q_brand:"De quel pays vient cette marque ?",
  q_currency:"ß€ quel pays appartient cette monnaie ?",q_curr_real:"Quelle monnaie a…",
  q_pop_compare:"Plus ou moins d'habitants ?",
  q_hl_pop:"Plus d'habitants que {a} ?",q_hl_river:"Plus long que {a} ?",q_hl_area:"Plus grand que {a} ?",
  q_neighbor:"Quel pays borde… ?",q_neighbor_not:"Ne borde PAS… ?",
  q_plates_casual:"De quel pays est cette plaque ?",q_plates_hard:"Identifier la région – aucun indice !",
  q_river_real:"Dans quel pays coule ce fleuve ?",q_map_guess:"Trouver le pays sur la carte",
  fb_correct:"✓“ Correct ! +{pts}",fb_wrong:"✗ Faux → {ans}",fb_time:"⏱ Temps ! → {ans}",
  plates_more:"+{n} de plus",pct_complete:"{pct}% terminé",
  spotter_dup:"📋 {code} ({country}) déjß  collecté !",
  map_unavail:"Carte non disponible",map_loading:"Chargement de la carte…",
  q_subway_km:"Quelle longueur a le réseau métro … (km)?",q_subway_lines:"Combien de lignes de métro a … ?",
  hl_longer:"⬆️ Plus long",hl_shorter:"⬇️ Plus court",hl_bigger:"⬆️ Plus grand (superficie)",hl_smaller:"⬇️ Plus petit (superficie)",
  ob_welcome:"Bienvenue sur GeoQuest",ob_sub1:"Le quiz de géographie – collectez des tampons, montez en ligueÂ !",ob_difficulty:"Niveau de difficulté",ob_diff_sub:"Choisissez votre style. Modifiable ß  tout moment.",
  ob_diff_casual_desc:"Grandes villes • 12 sec.",ob_diff_hc_desc:"Toutes les villes • 8 sec.",ob_back:"→ Retour",ob_modes_title:"Modes de jeu",
  ob_modes_sub:"19 modes, un objectifÂ : connaß®tre le monde.",ob_more_modes:"… et 16 autres modes",ob_start:"\u{1F680} C'est partiÂ !",ob_have_account:"J'ai déjß  un compte",ob_register:"NouveauÂ ? S'inscrire",
  home_hi:"Salut, {name} \u{1F44B}",home_guest:"Bienvenue, invité \u{1F30D}",home_save:"\u{1F510} Sauvegarder la progression",home_pvp_sub:"Jouer en temps réel contre un ami",
  ob_mode1_name:"Ville →’ Pays",ob_mode1_desc:"ß€ quel pays appartient cette villeÂ ?",ob_mode2_name:"Plaques UE",ob_mode2_desc:"D'oß¹ vient cette plaqueÂ ?",ob_mode3_name:"Réseaux de métro",ob_mode3_desc:"Lignes et km des métros.",
  language_select:"LANGUE",
  badge_beta:"B\u00eata",beta_warning:"Jouable, mais peut contenir des bugs.",
  rotate_device:"Veuillez faire pivoter votre appareil \u{1F4F1}\u27A1\u{1F5FA}",
  diff_desc_casual:"\u{1F7E2} Casual: Détendu · Sans limite de temps · ∞ Vies",
  diff_desc_hc:"\u{1F525} Hardcore: Classique · Sans limite de temps · 3 Vies",
  diff_desc_surv:"\u{1F480} Survival: Contre la montre · 8s · 3 Vies",
  hud_lives:"VIES",
  score_mult_max:"Multiplicateur Max",
  score_time_bonus:"Bonus Temps",
  pts_abbr:"pts.",
  score_correct_lbl:"correct",
  mode_wappen:"Armoiries",
  mode_slf:"Ville-Pays-Fleuve",
  mode_euro:"Piß¨ces Euro"
},
es:{
  play:"JUGAR",again:"JUGAR DE NUEVO",menu:"Menßº principal",board:"Clasificación",pass:"Pasaporte",
  fav_empty:"Aún no hay favoritos guardados",
  profile:"Perfil",stats:"Estadß­sticas",casual:"Casual",hardcore:"Hardcore",rounds:"Rondas",
  btn_collect:"Coleccionar",btn_back:"Volver al menßº",btn_next:"Siguiente →’",
  btn_again:"Jugar de nuevo",btn_menu:"Menßº principal",btn_adapt:"Adaptar",
  spotter_title:"\u{1F697} Spotter de viaje",
  spotter_hint:"Â¿Has visto una matrß­cula? Â¡Anótala!",
  spotter_all:"Todos los paß­ses",spotter_unknown:"Matrß­cula desconocida",
  spotter_not_in:"no en",spotter_but_in:"pero en",
  album_title:"\u{1F4D4} Colección de matrß­culas",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Mapa",
  album_empty_country:"Nada de {country} aßºn – Â¡usa el Spotter!",
  album_empty:"Â¡Nada recopilado aßºn!\nJuega a matrß­culas UE o usa el Spotter.",
  album_codes:"códigos",
  hl_higher:"⬆️ Más / Más largo / Más grande",hl_lower:"⬇️ Menos / Más corto / Más pequeño",
  hl_more:"⬆️ Más habitantes",hl_less:"⬇️ Menos habitantes",
  loc_detected:"Estás en {country}",loc_adapt:"Adaptar",
  q_city:"Â¿En qué paß­s está esta ciudad?",q_flag:"Â¿Qué paß­s tiene esta bandera?",
  q_capital:"Â¿A qué paß­s pertenece esta capital?",q_river:"Â¿En qué paß­s está este rß­o?",
  q_landmark:"Â¿En qué paß­s está este monumento?",q_park:"Â¿En qué paß­s está este parque nacional?",
  q_unesco:"Â¿En qué paß­s está este sitio UNESCO?",q_citymark:"Â¿A qué ciudad pertenece este monumento?",
  q_subway:"Â¿En qué ciudad está este metro?",q_flagsel:"Â¿Qué bandera pertenece a…",
  q_rcapital:"Â¿Cuál es la capital de…?",q_rcity:"Â¿Qué ciudad está en…?",
  q_rriver:"Â¿Qué rß­o atraviesa…?",q_outline:"Â¿Qué paß­s tiene esta forma?",
  q_food:"Â¿De qué paß­s viene este plato?",q_brand:"Â¿De qué paß­s viene esta marca?",
  q_currency:"Â¿A qué paß­s pertenece esta moneda?",q_curr_real:"Â¿Qué moneda tiene…",
  q_pop_compare:"Â¿Más o menos habitantes?",
  q_hl_pop:"Â¿Más habitantes que {a}?",q_hl_river:"Â¿Más largo que {a}?",q_hl_area:"Â¿Más grande que {a}?",
  q_neighbor:"Â¿Qué paß­s limita con…?",q_neighbor_not:"Â¿NO limita con…?",
  q_plates_casual:"Â¿De qué paß­s es esta matrß­cula?",q_plates_hard:"Identificar la región – Â¡sin pista!",
  q_river_real:"Â¿Por qué paß­s pasa este rß­o?",q_map_guess:"Encuentra el paß­s en el mapa",
  fb_correct:"✓“ Â¡Correcto! +{pts}",fb_wrong:"✗ Incorrecto → {ans}",fb_time:"⏱ Â¡Tiempo! → {ans}",
  plates_more:"+{n} más",pct_complete:"{pct}% completado",
  spotter_dup:"📋 {code} ({country}) ya coleccionado!",
  map_unavail:"Mapa no disponible",map_loading:"Cargando mapa…",
  q_subway_km:"Â¿Cuánto mide la red de metro … (km)?",q_subway_lines:"Â¿Cuántas lß­neas de metro tiene …?",
  hl_longer:"⬆️ Más largo",hl_shorter:"⬇️ Más corto",hl_bigger:"⬆️ Más grande (área)",hl_smaller:"⬇️ Más pequeño (área)",
  ob_welcome:"Bienvenido a GeoQuest",ob_sub1:"El quiz de geografß­a – colecciona sellos, sube en la liga.",ob_difficulty:"Nivel de dificultad",ob_diff_sub:"Elige tu estilo. Cambiable en cualquier momento.",
  ob_diff_casual_desc:"Ciudades grandes • 12 seg.",ob_diff_hc_desc:"Todas las ciudades • 8 seg.",ob_back:"→ Volver",ob_modes_title:"Modos de juego",
  ob_modes_sub:"19 modos, un objetivo: conocer el mundo.",ob_more_modes:"… y 16 modos más",ob_start:"\u{1F680} Â¡Vamos!",ob_have_account:"Ya tengo una cuenta",ob_register:"Â¿Nuevo? Regsß­strate",
  home_hi:"Hola, {name} \u{1F44B}",home_guest:"Bienvenido, invitado \u{1F30D}",home_save:"\u{1F510} Guardar progreso",home_pvp_sub:"Jugar en tiempo real contra un amigo",
  ob_mode1_name:"Ciudad →’ Paß­s",ob_mode1_desc:"Â¿A qué paß­s pertenece esta ciudad?",ob_mode2_name:"Matrß­culas UE",ob_mode2_desc:"Â¿De dónde viene esta matrß­cula?",ob_mode3_name:"Redes de metro",ob_mode3_desc:"Lß­neas y km de los metros.",
  language_select:"IDIOMA",
  badge_beta:"Beta",beta_warning:"Jugable, pero puede contener errores.",
  rotate_device:"Por favor, gira tu dispositivo al modo horizontal \u{1F4F1}\u27A1\u{1F5FA}",
  diff_desc_casual:"\u{1F7E2} Casual: Relajado · Sin lß­mite · ∞ Vidas",
  diff_desc_hc:"\u{1F525} Hardcore: Clásico · Sin lß­mite · 3 Vidas",
  diff_desc_surv:"\u{1F480} Survival: Contrarreloj · 8s · 3 Vidas",
  hud_lives:"VIDAS",
  score_mult_max:"Multiplicador Máx.",
  score_time_bonus:"Bono de Tiempo",
  pts_abbr:"pts.",
  score_correct_lbl:"correctas",
  mode_wappen:"Escudos",
  mode_slf:"Ciudad-Paß­s-Rß­o",
  mode_euro:"Monedas Euro"
},
it:{
  play:"GIOCA",again:"GIOCA ANCORA",menu:"Menu principale",board:"Classifica",pass:"Passaporto",
  fav_empty:"Nessun preferito salvato ancora",
  profile:"Profilo",stats:"Statistiche",casual:"Casual",hardcore:"Hardcore",rounds:"Round",
  btn_collect:"Colleziona",btn_back:"Torna al menu",btn_next:"Avanti →’",
  btn_again:"Gioca ancora",btn_menu:"Menu principale",btn_adapt:"Adatta",
  spotter_title:"\u{1F697} Spotter di viaggio",
  spotter_hint:"Hai visto una targa? Registrala subito!",
  spotter_all:"Tutti i paesi",spotter_unknown:"Targa sconosciuta",
  spotter_not_in:"non in",spotter_but_in:"ma in",
  album_title:"\u{1F4D4} Raccolta targhe",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Mappa",
  album_empty_country:"Niente da {country} ancora – usa lo Spotter!",
  album_empty:"Niente ancora raccolto!\nGioca alle targhe UE o usa lo Spotter.",
  album_codes:"codici",
  hl_higher:"⬆️ Di piß¹ / Piß¹ lungo / Piß¹ grande",hl_lower:"⬇️ Di meno / Piß¹ corto / Piß¹ piccolo",
  hl_more:"⬆️ Piß¹ abitanti",hl_less:"⬇️ Meno abitanti",
  loc_detected:"Sei in {country}",loc_adapt:"Adatta",
  q_city:"In quale paese si trova questa cittß ?",q_flag:"Quale paese ha questa bandiera?",
  q_capital:"A quale paese appartiene questa capitale?",q_river:"In quale paese scorre questo fiume?",
  q_landmark:"In quale paese si trova questo monumento?",q_park:"In quale paese si trova questo parco nazionale?",
  q_unesco:"In quale paese si trova questo sito UNESCO?",q_citymark:"A quale cittß  appartiene questo monumento?",
  q_subway:"In quale cittß  si trova questa metro?",q_flagsel:"Quale bandiera appartiene a…",
  q_rcapital:"Qual ß¨ la capitale di…?",q_rcity:"Quale cittß  si trova in…?",
  q_rriver:"Quale fiume scorre attraverso…?",q_outline:"Quale paese ha questa forma?",
  q_food:"Da quale paese viene questo piatto?",q_brand:"Da quale paese viene questo marchio?",
  q_currency:"A quale paese appartiene questa valuta?",q_curr_real:"Quale valuta ha…",
  q_pop_compare:"Piß¹ o meno abitanti?",
  q_hl_pop:"Piß¹ abitanti di {a}?",q_hl_river:"Piß¹ lungo di {a}?",q_hl_area:"Piß¹ grande di {a}?",
  q_neighbor:"Quale paese confina con…?",q_neighbor_not:"NON confina con…?",
  q_plates_casual:"Da quale paese viene questa targa?",q_plates_hard:"Identificare la regione – nessun indizio!",
  q_river_real:"Attraverso quale paese scorre questo fiume?",q_map_guess:"Trova il paese sulla mappa",
  fb_correct:"✓“ Corretto! +{pts}",fb_wrong:"✗ Sbagliato → {ans}",fb_time:"⏱ Tempo! → {ans}",
  plates_more:"+{n} altri",pct_complete:"{pct}% completato",
  spotter_dup:"📋 {code} ({country}) giß  raccolto!",
  map_unavail:"Mappa non disponibile",map_loading:"Caricamento mappa…",
  q_subway_km:"Quanto ß¨ lungo il metrß² … (km)?",q_subway_lines:"Quante linee metro ha …?",
  hl_longer:"⬆️ Piß¹ lungo",hl_shorter:"⬇️ Piß¹ corto",hl_bigger:"⬆️ Piß¹ grande (superficie)",hl_smaller:"⬇️ Piß¹ piccolo (superficie)",
  ob_welcome:"Benvenuto su GeoQuest",ob_sub1:"Il quiz di geografia – colleziona timbri, sali in classifica!",ob_difficulty:"Livello di difficoltß ",ob_diff_sub:"Scegli il tuo stile. Modificabile in qualsiasi momento.",
  ob_diff_casual_desc:"Cittß  principali • 12 sec.",ob_diff_hc_desc:"Tutte le cittß  • 8 sec.",ob_back:"→ Indietro",ob_modes_title:"Modalitß  di gioco",
  ob_modes_sub:"19 modalitß , un obiettivo: conoscere il mondo.",ob_more_modes:"… e altre 16 modalitß ",ob_start:"\u{1F680} Andiamo!",ob_have_account:"Ho giß  un account",ob_register:"Nuovo? Registrati",
  home_hi:"Ciao, {name} \u{1F44B}",home_guest:"Benvenuto, ospite \u{1F30D}",home_save:"\u{1F510} Salva i progressi",home_pvp_sub:"Gioca in tempo reale contro un amico",
  ob_mode1_name:"Cittß  →’ Paese",ob_mode1_desc:"A quale paese appartiene questa cittß ?",ob_mode2_name:"Targhe UE",ob_mode2_desc:"Da dove viene questa targa?",ob_mode3_name:"Reti metro",ob_mode3_desc:"Linee e km delle metropolitane.",
  language_select:"LINGUA",
  badge_beta:"Beta",beta_warning:"Giocabile, ma potrebbe contenere bug.",
  rotate_device:"Ruota il dispositivo in modalit\u00e0 orizzontale \u{1F4F1}\u27A1\u{1F5FA}",
  diff_desc_casual:"\u{1F7E2} Casual: Rilassato · Senza limite · ∞ Vite",
  diff_desc_hc:"\u{1F525} Hardcore: Classico · Senza limite · 3 Vite",
  diff_desc_surv:"\u{1F480} Survival: Contro il tempo · 8s · 3 Vite",
  hud_lives:"VITE",
  score_mult_max:"Moltiplicatore Max",
  score_time_bonus:"Bonus Tempo",
  pts_abbr:"pt.",
  score_correct_lbl:"corrette",
  mode_wappen:"Stemmi",
  mode_slf:"Cittß -Paese-Fiume",
  mode_euro:"Monete Euro"
},
nl:{
  play:"SPELEN",again:"OPNIEUW SPELEN",menu:"Hoofdmenu",board:"Ranglijst",pass:"Paspoort",
  fav_empty:"Nog geen favorieten opgeslagen",
  profile:"Profiel",stats:"Statistieken",casual:"Casual",hardcore:"Hardcore",rounds:"Rondes",
  btn_collect:"Verzamelen",btn_back:"Terug naar menu",btn_next:"Volgende →’",
  btn_again:"Opnieuw spelen",btn_menu:"Hoofdmenu",btn_adapt:"Aanpassen",
  spotter_title:"\u{1F697} Reisspotter",
  spotter_hint:"Kenteken gezien? Noteer het nu!",
  spotter_all:"Alle landen",spotter_unknown:"Onbekend kenteken",
  spotter_not_in:"niet in",spotter_but_in:"maar in",
  album_title:"\u{1F4D4} Kentekenalbum",album_list:"\u{1F4DD} Lijst",album_map:"\u{1F5FA} Kaart",
  album_empty_country:"Nog niets uit {country} – gebruik de Spotter!",
  album_empty:"Nog niets verzameld!\nSpeel EU-kentekens of gebruik de Spotter.",
  album_codes:"codes",
  hl_higher:"⬆️ Meer / Langer / Groter",hl_lower:"⬇️ Minder / Korter / Kleiner",
  hl_more:"⬆️ Meer inwoners",hl_less:"⬇️ Minder inwoners",
  loc_detected:"Je bent in {country}",loc_adapt:"Aanpassen",
  q_city:"In welk land ligt deze stad?",q_flag:"Welk land heeft deze vlag?",
  q_capital:"Bij welk land hoort deze hoofdstad?",q_river:"In welk land ligt deze rivier?",
  q_landmark:"In welk land staat dit monument?",q_park:"In welk land ligt dit nationaal park?",
  q_unesco:"In welk land ligt dit UNESCO-erfgoed?",q_citymark:"Bij welke stad hoort dit monument?",
  q_subway:"In welke stad is deze metro?",q_flagsel:"Welke vlag hoort bij…",
  q_rcapital:"Wat is de hoofdstad van…?",q_rcity:"Welke stad ligt in…?",
  q_rriver:"Welke rivier stroomt door…?",q_outline:"Welk land heeft deze vorm?",
  q_food:"Uit welk land komt dit gerecht?",q_brand:"Uit welk land komt dit merk?",
  q_currency:"Bij welk land hoort deze munt?",q_curr_real:"Welke munt heeft…",
  q_pop_compare:"Meer of minder inwoners?",
  q_hl_pop:"Meer inwoners dan {a}?",q_hl_river:"Langer dan {a}?",q_hl_area:"Groter dan {a}?",
  q_neighbor:"Welk land grenst aan…?",q_neighbor_not:"Grenst NIET aan…?",
  q_plates_casual:"Uit welk land komt dit kenteken?",q_plates_hard:"Identificeer de regio – geen hint!",
  q_river_real:"Door welk land stroomt deze rivier?",q_map_guess:"Vind het land op de kaart",
  fb_correct:"✓“ Correct! +{pts}",fb_wrong:"✗ Fout → {ans}",fb_time:"⏱ Tijd! → {ans}",
  plates_more:"+{n} meer",pct_complete:"{pct}% voltooid",
  spotter_dup:"📋 {code} ({country}) al verzameld!",
  map_unavail:"Kaart niet beschikbaar",map_loading:"Kaart laden…",
  q_subway_km:"Hoe lang is het metronetwerk … (km)?",q_subway_lines:"Hoeveel metrolijnen heeft …?",
  diff_desc_casual:"\u{1F7E2} Casual: Ontspannen · Geen tijdslimiet · ∞ Levens",diff_desc_hc:"\u{1F525} Hardcore: Klassiek · Geen tijdslimiet · 3 Levens",diff_desc_surv:"\u{1F480} Survival: Tegen de klok · 8s · 3 Levens",hud_lives:"LEVENS",score_mult_max:"Max Vermenigvuldiger",score_time_bonus:"Tijdbonus",pts_abbr:"pt.",score_correct_lbl:"correct",mode_wappen:"Wapens",mode_slf:"Stad-Land-Rivier",mode_euro:"Euromunt"
},
pt:{
  play:"JOGAR",again:"JOGAR NOVAMENTE",menu:"Menu principal",board:"Classificaçß£o",pass:"Passaporte",
  fav_empty:"Nenhum favorito guardado ainda",
  profile:"Perfil",stats:"Estatß­sticas",casual:"Casual",hardcore:"Hardcore",rounds:"Rodadas",
  btn_collect:"Coletar",btn_back:"Voltar ao menu",btn_next:"Próximo →’",
  btn_again:"Jogar novamente",btn_menu:"Menu principal",btn_adapt:"Adaptar",
  spotter_title:"\u{1F697} Spotter de viagem",
  spotter_hint:"Viu uma placa? Registre agora!",
  spotter_all:"Todos os paß­ses",spotter_unknown:"Placa desconhecida",
  spotter_not_in:"nß£o em",spotter_but_in:"mas em",
  album_title:"\u{1F4D4} Coleçß£o de placas",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Mapa",
  album_empty_country:"Nada de {country} ainda – use o Spotter!",
  album_empty:"Nada coletado ainda!\nJogue placas UE ou use o Spotter.",
  album_codes:"códigos",
  hl_higher:"⬆️ Mais / Mais longo / Maior",hl_lower:"⬇️ Menos / Mais curto / Menor",
  hl_more:"⬆️ Mais habitantes",hl_less:"⬇️ Menos habitantes",
  loc_detected:"Vocßª está em {country}",loc_adapt:"Adaptar",
  q_city:"Em qual paß­s fica esta cidade?",q_flag:"Qual paß­s tem esta bandeira?",
  q_capital:"A qual paß­s pertence esta capital?",q_river:"Em qual paß­s fica este rio?",
  q_landmark:"Em qual paß­s fica este monumento?",q_park:"Em qual paß­s fica este parque nacional?",
  q_unesco:"Em qual paß­s fica este sß­tio UNESCO?",q_citymark:"A qual cidade pertence este monumento?",
  q_subway:"Em qual cidade fica este metrß´?",q_flagsel:"Qual bandeira pertence a…",
  q_rcapital:"Qual é a capital de…?",q_rcity:"Qual cidade fica em…?",
  q_rriver:"Qual rio corre por…?",q_outline:"Qual paß­s tem esta forma?",
  q_food:"De qual paß­s vem este prato?",q_brand:"De qual paß­s vem esta marca?",
  q_currency:"A qual paß­s pertence esta moeda?",q_curr_real:"Qual moeda tem…",
  q_pop_compare:"Mais ou menos habitantes?",
  q_hl_pop:"Mais habitantes que {a}?",q_hl_river:"Mais longo que {a}?",q_hl_area:"Maior que {a}?",
  q_neighbor:"Qual paß­s faz fronteira com…?",q_neighbor_not:"NßƒO faz fronteira com…?",
  q_plates_casual:"De qual paß­s é esta placa?",q_plates_hard:"Identificar a regiß£o – sem dica!",
  q_river_real:"Por qual paß­s corre este rio?",q_map_guess:"Encontre o paß­s no mapa",
  fb_correct:"✓“ Correto! +{pts}",fb_wrong:"✗ Errado → {ans}",fb_time:"⏱ Tempo! → {ans}",
  plates_more:"+{n} mais",pct_complete:"{pct}% completo",
  spotter_dup:"📋 {code} ({country}) já coletado!",
  map_unavail:"Mapa nß£o disponß­vel",map_loading:"Carregando mapa…",
  q_subway_km:"Qual o comprimento da rede de metro … (km)?",q_subway_lines:"Quantas linhas de metro tem …?",
  diff_desc_casual:"\u{1F7E2} Casual: Relaxado · Sem limite · ∞ Vidas",diff_desc_hc:"\u{1F525} Hardcore: Clássico · Sem limite · 3 Vidas",diff_desc_surv:"\u{1F480} Survival: Contra o relógio · 8s · 3 Vidas",hud_lives:"VIDAS",score_mult_max:"Multiplicador Máx.",score_time_bonus:"Bónus de Tempo",pts_abbr:"pts.",score_correct_lbl:"corretas",mode_wappen:"Brasßµes",mode_slf:"Cidade-Paß­s-Rio",mode_euro:"Moedas Euro"
},
ro:{
  play:"JOACń‚",again:"JOACń‚ DIN NOU",menu:"Meniu principal",board:"Clasament",pass:"PaÈ™aport",
  fav_empty:"Nu există favorite salvate încă",
  profile:"Profil",stats:"Statistici",casual:"Casual",hardcore:"Hardcore",rounds:"Runde",
  btn_collect:"Colecteazńƒ",btn_back:"ßŽnapoi la meniu",btn_next:"Urmńƒtor →’",
  btn_again:"Joacńƒ din nou",btn_menu:"Meniu principal",btn_adapt:"Adapteazńƒ",
  spotter_title:"\u{1F697} Spotter de cńƒlńƒtorie",
  spotter_hint:"Ai vńƒzut o plńƒcuÈ›ńƒ? ßŽnregistreaz-o acum!",
  spotter_all:"Toate È›ńƒrile",spotter_unknown:"PlńƒcuÈ›ńƒ necunoscutńƒ",
  spotter_not_in:"nu ß®n",spotter_but_in:"dar ß®n",
  album_title:"\u{1F4D4} ColecÈ›ie de plńƒcuÈ›e",album_list:"\u{1F4DD} Listńƒ",album_map:"\u{1F5FA} Hartńƒ",
  album_empty_country:"Nimic din {country} ß®ncńƒ – foloseÈ™te Spotter-ul!",
  album_empty:"Nimic colectat ß®ncńƒ!\nJoacńƒ plńƒcuÈ›e UE sau foloseÈ™te Spotter-ul.",
  album_codes:"coduri",
  hl_higher:"⬆️ Mai mult / Mai lung / Mai mare",hl_lower:"⬇️ Mai puÈ›in / Mai scurt / Mai mic",
  hl_more:"⬆️ Mai mulÈ›i locuitori",hl_less:"⬇️ Mai puÈ›ini locuitori",
  loc_detected:"EÈ™ti ß®n {country}",loc_adapt:"Adapteazńƒ",
  q_city:"ßŽn ce È›arńƒ se aflńƒ acest oraÈ™?",q_flag:"Ce È›arńƒ are acest steag?",
  q_capital:"Cńƒrui È›ńƒri aparÈ›ine aceastńƒ capitalńƒ?",q_river:"ßŽn ce È›arńƒ curge acest rß¢u?",
  q_landmark:"ßŽn ce È›arńƒ se aflńƒ acest monument?",q_park:"ßŽn ce È›arńƒ se aflńƒ acest parc naÈ›ional?",
  q_unesco:"ßŽn ce È›arńƒ se aflńƒ acest sit UNESCO?",q_citymark:"Cńƒrui oraÈ™ aparÈ›ine acest monument?",
  q_subway:"ßŽn ce oraÈ™ se aflńƒ acest metrou?",q_flagsel:"Ce steag aparÈ›ine lui…",
  q_rcapital:"Care este capitala lui…?",q_rcity:"Ce oraÈ™ se aflńƒ ß®n…?",
  q_rriver:"Ce rß¢u curge prin…?",q_outline:"Ce È›arńƒ are aceastńƒ formńƒ?",
  q_food:"Din ce È›arńƒ vine acest preparat?",q_brand:"Din ce È›arńƒ vine acest brand?",
  q_currency:"Cńƒrui È›ńƒri aparÈ›ine aceastńƒ monedńƒ?",q_curr_real:"Ce monedńƒ are…",
  q_pop_compare:"Mai mulÈ›i sau mai puÈ›ini locuitori?",
  q_hl_pop:"Mai mulÈ›i locuitori decß¢t {a}?",q_hl_river:"Mai lung decß¢t {a}?",q_hl_area:"Mai mare decß¢t {a}?",
  q_neighbor:"Ce È›arńƒ se ß®nvecineazńƒ cu…?",q_neighbor_not:"NU se ß®nvecineazńƒ cu…?",
  q_plates_casual:"Din ce È›arńƒ este aceastńƒ plńƒcuÈ›ńƒ?",q_plates_hard:"IdentificaÈ›i regiunea – fńƒrńƒ indiciu!",
  q_river_real:"Prin ce È›arńƒ curge acest rß¢u?",q_map_guess:"GńƒseÈ™te È›ara pe hartńƒ",
  fb_correct:"✓“ Corect! +{pts}",fb_wrong:"✗ GreÈ™it → {ans}",fb_time:"⏱ Timp! → {ans}",
  plates_more:"+{n} mai mult",pct_complete:"{pct}% complet",
  spotter_dup:"📋 {code} ({country}) deja colectat!",
  map_unavail:"Hartńƒ indisponibilńƒ",map_loading:"Se ßªncarcńƒ harta…",
  q_subway_km:"Cß¢t de lungńƒ este reÈ›eaua de metrou … (km)?",q_subway_lines:"Cß¢te linii de metrou are …?",
  diff_desc_casual:"\u{1F7E2} Casual: Relaxat · Fńƒrńƒ limitńƒ · ∞ VieÈ›i",diff_desc_hc:"\u{1F525} Hardcore: Clasic · Fńƒrńƒ limitńƒ · 3 VieÈ›i",diff_desc_surv:"\u{1F480} Survival: Contra cronometru · 8s · 3 VieÈ›i",hud_lives:"VIEÈžI",score_mult_max:"Multiplicator Max",score_time_bonus:"Bonus Timp",pts_abbr:"pct.",score_correct_lbl:"corecte",mode_wappen:"Steme",mode_slf:"OraŚŸ-Èšarńƒ-Rß¢u",mode_euro:"Monede Euro"
},
hu:{
  play:"JßTß‰K",again:"ßšJRA JßTSZANI",menu:"FŚ‘menü",board:"Rangsor",pass:"ßštlevél",
  fav_empty:"Még nincsenek mentett kedvencek",
  profile:"Profil",stats:"Statisztikák",casual:"KönnyŚ±",hardcore:"Nehéz",rounds:"Körök",
  btn_collect:"GyŚ±jt",btn_back:"Vissza a fŚ‘menübe",btn_next:"Tovább →’",
  btn_again:"ßšjra játszani",btn_menu:"FŚ‘menü",btn_adapt:"Módosß­t",
  spotter_title:"\u{1F697} Utazó Spotter",
  spotter_hint:"Rendszámot láttál? Jegyezd fel azonnal!",
  spotter_all:"Összes ország",spotter_unknown:"Ismeretlen rendszám",
  spotter_not_in:"nem szerepel",spotter_but_in:"de szerepel",
  album_title:"\u{1F4D4} Rendszám Album",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Térkép",
  album_empty_country:"Még semmi {country}-ból – használd a Spotter-t!",
  album_empty:"Még semmi összegyŚ±jtve!\nJátssz EU rendszámokat vagy használd a Spotter-t.",
  album_codes:"kódok",
  hl_higher:"⬆️ Több / Hosszabb / Nagyobb",hl_lower:"⬇️ Kevesebb / Rövidebb / Kisebb",
  hl_more:"⬆️ Több lakos",hl_less:"⬇️ Kevesebb lakos",
  loc_detected:"Jelenleg itt tartózkodik: {country}",loc_adapt:"Módosß­t",
  q_city:"Melyik országban van ez a város?",q_flag:"Melyik ország zászlaja ez?",
  q_capital:"Melyik ország fŚ‘városa ez?",q_river:"Melyik országban folyik ez a folyó?",
  q_landmark:"Melyik országban van ez az emlékmŚ±?",q_park:"Melyik országban van ez a nemzeti park?",
  q_unesco:"Melyik országban van ez az UNESCO-helyszß­n?",q_citymark:"Melyik városhoz tartozik ez az emlékmŚ±?",
  q_subway:"Melyik városban van ez a metró?",q_flagsel:"Melyik zászló tartozik…-hoz",
  q_rcapital:"Mi a fŚ‘városa…-nak?",q_rcity:"Melyik város van…-ban?",
  q_rriver:"Melyik folyó folyik át…-on?",q_outline:"Melyik ország van ebben az alakban?",
  q_food:"Melyik országból származik ez az étel?",q_brand:"Melyik országból származik ez a márka?",
  q_currency:"Melyik ország pénzneme ez?",q_curr_real:"Melyik pénzneme van…-nak",
  q_pop_compare:"Több vagy kevesebb lakos?",
  q_hl_pop:"Több lakos, mint {a}?",q_hl_river:"Hosszabb, mint {a}?",q_hl_area:"Nagyobb, mint {a}?",
  q_neighbor:"Melyik ország határos…-val?",q_neighbor_not:"NEM határos…-val?",
  q_plates_casual:"Melyik ország rendszáma ez?",q_plates_hard:"Azonosß­tsa a régiót – nincs tipp!",
  q_river_real:"Melyik országon folyik át ez a folyó?",q_map_guess:"Keresse meg az országot a térképen",
  fb_correct:"✓“ Helyes! +{pts}",fb_wrong:"✗ Rossz → {ans}",fb_time:"⏱ IdŚ‘! → {ans}",
  plates_more:"+{n} több",pct_complete:"{pct}% kész",
  spotter_dup:"📋 {code} ({country}) már összegyŚ±jtve!",
  map_unavail:"Térkép nem elérhetŚ‘",map_loading:"Térkép betöltése…",
  q_subway_km:"Milyen hosszßº a metróhálózat … (km)?",q_subway_lines:"Hány metróvonal van …?",
  diff_desc_casual:"\u{1F7E2} Casual: Lazulás · Nincs idŚ‘limit · ∞ ß‰let",diff_desc_hc:"\u{1F525} Hardcore: Klasszikus · Nincs idŚ‘limit · 3 ß‰let",diff_desc_surv:"\u{1F480} Survival: Verseny az idŚ‘vel · 8mp · 3 ß‰let",hud_lives:"ß‰LETEK",score_mult_max:"Max Szorzó",score_time_bonus:"IdŚ‘bónusz",pts_abbr:"pt.",score_correct_lbl:"helyes",mode_wappen:"Cß­merek",mode_slf:"Város-Ország-Folyó",mode_euro:"Euróérmék"
},
cs:{
  play:"HRßT",again:"HRßT ZNOVU",menu:"Hlavnß­ menu",board:"Ś½ebŚ™ß­ńek",pass:"Pas",
  fav_empty:"Zatím žádné oblíbené uloženy",
  profile:"Profil",stats:"Statistiky",casual:"Casual",hardcore:"Hardcore",rounds:"Kola",
  btn_collect:"Sbß­rat",btn_back:"Zpń›t do menu",btn_next:"DalŚ¡ß­ →’",
  btn_again:"Hrát znovu",btn_menu:"Hlavnß­ menu",btn_adapt:"PŚ™izpŚ¯sobit",
  spotter_title:"\u{1F697} Cestovnß­ Spotter",
  spotter_hint:"Vidń›l jsi SPZ? ZapiŚ¡ ji hned!",
  spotter_all:"VŚ¡echny zemń›",spotter_unknown:"Neznámá SPZ",
  spotter_not_in:"nenß­ v",spotter_but_in:"ale je v",
  album_title:"\u{1F4D4} Album SPZ",album_list:"\u{1F4DD} Seznam",album_map:"\u{1F5FA} Mapa",
  album_empty_country:"Zatß­m nic z {country} – pouŚ¾ij Spotter!",
  album_empty:"Zatß­m nic neshromáŚ¾dń›no!\nHraj EU SPZ nebo pouŚ¾ij Spotter.",
  album_codes:"kódy",
  hl_higher:"⬆️ Vß­ce / DelŚ¡ß­ / Vń›tŚ¡ß­",hl_lower:"⬇️ Ménń› / KratŚ¡ß­ / MenŚ¡ß­",
  hl_more:"⬆️ Vß­ce obyvatel",hl_less:"⬇️ Ménń› obyvatel",
  loc_detected:"Jsi v {country}",loc_adapt:"PŚ™izpŚ¯sobit",
  q_city:"Ve které zemi leŚ¾ß­ toto mń›sto?",q_flag:"Která zemń› má tuto vlajku?",
  q_capital:"Které zemi patŚ™ß­ toto hlavnß­ mń›sto?",q_river:"Ve které zemi teńe tato Ś™eka?",
  q_landmark:"Ve které zemi se nacházß­ tato památka?",q_park:"Ve které zemi se nacházß­ tento národnß­ park?",
  q_unesco:"Ve které zemi se nacházß­ toto UNESCO dń›dictvß­?",q_citymark:"Ke kterému mń›stu patŚ™ß­ tato památka?",
  q_subway:"Ve kterém mń›stń› je toto metro?",q_flagsel:"Která vlajka patŚ™ß­ k…",
  q_rcapital:"Jaké je hlavnß­ mń›sto…?",q_rcity:"Které mń›sto leŚ¾ß­ v…?",
  q_rriver:"Která Ś™eka protéká…?",q_outline:"Která zemń› má tento tvar?",
  q_food:"Ze které zemń› pocházß­ toto jß­dlo?",q_brand:"Ze které zemń› pocházß­ tato znańka?",
  q_currency:"Které zemi patŚ™ß­ tato mń›na?",q_curr_real:"Jakou mń›nu má…",
  q_pop_compare:"Vß­ce nebo ménń› obyvatel?",
  q_hl_pop:"Vß­ce obyvatel neŚ¾ {a}?",q_hl_river:"DelŚ¡ß­ neŚ¾ {a}?",q_hl_area:"Vń›tŚ¡ß­ neŚ¾ {a}?",
  q_neighbor:"Která zemń› sousedß­ s…?",q_neighbor_not:"NESOUSEDß s…?",
  q_plates_casual:"Ze které zemń› je tato SPZ?",q_plates_hard:"Urńete region – Ś¾ádná nápovń›da!",
  q_river_real:"PŚ™es kterou zemi teńe tato Ś™eka?",q_map_guess:"Najdi zemi na mapń›",
  fb_correct:"✓“ Správnń›! +{pts}",fb_wrong:"✗ Chybnń› → {ans}",fb_time:"⏱ čas! → {ans}",
  plates_more:"+{n} dalŚ¡ß­ch",pct_complete:"{pct}% hotovo",
  spotter_dup:"📋 {code} ({country}) jiŚ¾ sbß­ráno!",
  map_unavail:"Mapa nenß­ k dispozici",map_loading:"Nańß­tánß­ mapy…",
  q_subway_km:"Jak dlouhé je metro … (km)?",q_subway_lines:"Kolik metrovß½ch linek má …?",
  diff_desc_casual:"\u{1F7E2} Casual: Uvolnń›nß½ · Bez ńasového limitu · ∞ Ś½ivotŚ¯",diff_desc_hc:"\u{1F525} Hardcore: Klasika · Bez limitu · 3 Ś½ivoty",diff_desc_surv:"\u{1F480} Survival: Proti ńasu · 8s · 3 Ś½ivoty",hud_lives:"Ś½IVOTY",score_mult_max:"Max Multiplikátor",score_time_bonus:"časovß½ Bonus",pts_abbr:"bd.",score_correct_lbl:"správnń›",mode_wappen:"Erby",mode_slf:"Mń›sto-Stát-Ś˜eka",mode_euro:"Euromince"
},
sk:{
  play:"HRAŚ¤",again:"HRAŚ¤ ZNOVA",menu:"Hlavné menu",board:"Rebrß­ńek",pass:"Pas",
  fav_empty:"Zatiaľ žiadne obľúbené uložené",
  profile:"Profil",stats:"Ś tatistiky",casual:"Casual",hardcore:"Hardcore",rounds:"Kolá",
  btn_collect:"Zbierať",btn_back:"Späť do menu",btn_next:"ďalej →’",
  btn_again:"HraŚ¥ znova",btn_menu:"Hlavné menu",btn_adapt:"Prispß´sobiŚ¥",
  spotter_title:"\u{1F697} Cestovný Spotter",
  spotter_hint:"Videl si EČV? Zaznań ju hneń!",
  spotter_all:"VŚ¡etky krajiny",spotter_unknown:"Neznáma EČV",
  spotter_not_in:"nie je v",spotter_but_in:"ale je v",
  album_title:"\u{1F4D4} Album EČV",album_list:"\u{1F4DD} Zoznam",album_map:"\u{1F5FA} Mapa",
  album_empty_country:"Zatiań¾ niń z {country} – pouŚ¾i Spotter!",
  album_empty:"Zatiań¾ niń nezbierane!\nHraj Eßš EČV alebo pouŚ¾i Spotter.",
  album_codes:"kódy",
  hl_higher:"⬆️ Viac / DlhŚ¡ß­ / VäńŚ¡ß­",hl_lower:"⬇️ Menej / KratŚ¡ß­ / MenŚ¡ß­",
  hl_more:"⬆️ Viac obyvateń¾ov",hl_less:"⬇️ Menej obyvateń¾ov",
  loc_detected:"Si v {country}",loc_adapt:"Prispß´sobiŚ¥",
  q_city:"V ktorej krajine leŚ¾ß­ toto mesto?",q_flag:"Ktorá krajina má tßºto vlajku?",
  q_capital:"Ktorej krajine patrß­ toto hlavné mesto?",q_river:"V ktorej krajine teńie táto rieka?",
  q_landmark:"V ktorej krajine sa nachádza táto pamiatka?",q_park:"V ktorej krajine sa nachádza tento národnß½ park?",
  q_unesco:"V ktorej krajine sa nachádza toto UNESCO dediństvo?",q_citymark:"Ktorému mestu patrß­ táto pamiatka?",
  q_subway:"V ktorom meste je toto metro?",q_flagsel:"Ktorá vlajka patrß­ k…",
  q_rcapital:"Aké je hlavné mesto…?",q_rcity:"Ktoré mesto leŚ¾ß­ v…?",
  q_rriver:"Ktorá rieka preteká cez…?",q_outline:"Ktorá krajina má tento tvar?",
  q_food:"Z ktorej krajiny pochádza toto jedlo?",q_brand:"Z ktorej krajiny pochádza táto znańka?",
  q_currency:"Ktorej krajine patrß­ táto mena?",q_curr_real:"Akßº menu má…",
  q_pop_compare:"Viac alebo menej obyvateń¾ov?",
  q_hl_pop:"Viac obyvateń¾ov ako {a}?",q_hl_river:"DlhŚ¡ß­ ako {a}?",q_hl_area:"VäńŚ¡ß­ ako {a}?",
  q_neighbor:"Ktorá krajina susedß­ s…?",q_neighbor_not:"NESUSEDß s…?",
  q_plates_casual:"Z ktorej krajiny je táto EČV?",q_plates_hard:"Identifikujte región – Ś¾iadna nápoveda!",
  q_river_real:"Cez ktorßº krajinu teńie táto rieka?",q_map_guess:"Nájdi krajinu na mape",
  fb_correct:"✓“ Správne! +{pts}",fb_wrong:"✗ Nesprávne → {ans}",fb_time:"⏱ čas! → {ans}",
  plates_more:"+{n} ńalŚ¡ß­ch",pct_complete:"{pct}% hotovo",
  spotter_dup:"📋 {code} ({country}) uŚ¾ zozbierané!",
  map_unavail:"Mapa nie je dostupná",map_loading:"Nańß­távanie mapy…",
  q_subway_km:"Aká dlhá je sieŚ¥ metra … (km)?",q_subway_lines:"Koń¾ko liniek metra má …?",
  diff_desc_casual:"\u{1F7E2} Casual: Uvolnń›nß½ · Bez ńasového limitu · ∞ Ś½ivotov",diff_desc_hc:"\u{1F525} Hardcore: Klasika · Bez limitu · 3 Ś½ivoty",diff_desc_surv:"\u{1F480} Survival: Proti ńasu · 8s · 3 Ś½ivoty",hud_lives:"Ś½IVOTY",score_mult_max:"Max Multiplikátor",score_time_bonus:"časovß½ Bonus",pts_abbr:"b.",score_correct_lbl:"správne",mode_wappen:"Erby",mode_slf:"Mesto-Krajina-Rieka",mode_euro:"Euromince"
},
hr:{
  play:"IGRAJ",again:"IGRAJ PONOVO",menu:"Glavni izbornik",board:"Ljestvica",pass:"Putovnica",
  fav_empty:"Još nema spremljenih favorita",
  profile:"Profil",stats:"Statistike",casual:"Casual",hardcore:"Hardcore",rounds:"Runde",
  btn_collect:"Sakupi",btn_back:"Natrag na izbornik",btn_next:"Sljedeće →’",
  btn_again:"Igraj ponovo",btn_menu:"Glavni izbornik",btn_adapt:"Prilagodi",
  spotter_title:"\u{1F697} Putni Spotter",
  spotter_hint:"Vidio registraciju? ZabiljeŚ¾i odmah!",
  spotter_all:"Sve drŚ¾ave",spotter_unknown:"Nepoznata registracija",
  spotter_not_in:"nije u",spotter_but_in:"ali je u",
  album_title:"\u{1F4D4} Album registracija",album_list:"\u{1F4DD} Popis",album_map:"\u{1F5FA} Karta",
  album_empty_country:"JoŚ¡ niŚ¡ta iz {country} – koristi Spotter!",
  album_empty:"JoŚ¡ niŚ¡ta skupljeno!\nIgraj EU registracije ili koristi Spotter.",
  album_codes:"kodovi",
  hl_higher:"⬆️ ViŚ¡e / DuŚ¾e / Veće",hl_lower:"⬇️ Manje / Kraće / Manje",
  hl_more:"⬆️ ViŚ¡e stanovnika",hl_less:"⬇️ Manje stanovnika",
  loc_detected:"Nalazite se u {country}",loc_adapt:"Prilagodi",
  q_city:"U kojoj se drŚ¾avi nalazi ovaj grad?",q_flag:"Koja drŚ¾ava ima ovu zastavu?",
  q_capital:"Kojoj drŚ¾avi pripada ovaj glavni grad?",q_river:"U kojoj drŚ¾avi teńe ova rijeka?",
  q_landmark:"U kojoj se drŚ¾avi nalazi ovaj spomenik?",q_park:"U kojoj se drŚ¾avi nalazi ovaj nacionalni park?",
  q_unesco:"U kojoj se drŚ¾avi nalazi ovo UNESCO nasljeń‘e?",q_citymark:"Kojemu gradu pripada ovaj spomenik?",
  q_subway:"U kojemu gradu je ovaj metro?",q_flagsel:"Koja zastava pripada…",
  q_rcapital:"Koji je glavni grad…?",q_rcity:"Koji grad se nalazi u…?",
  q_rriver:"Koja rijeka teńe kroz…?",q_outline:"Koja drŚ¾ava ima ovaj oblik?",
  q_food:"Iz koje drŚ¾ave dolazi ovo jelo?",q_brand:"Iz koje drŚ¾ave dolazi ovaj brand?",
  q_currency:"Kojoj drŚ¾avi pripada ova valuta?",q_curr_real:"Koju valutu ima…",
  q_pop_compare:"ViŚ¡e ili manje stanovnika?",
  q_hl_pop:"ViŚ¡e stanovnika od {a}?",q_hl_river:"DuŚ¾e od {a}?",q_hl_area:"Veće od {a}?",
  q_neighbor:"Koja drŚ¾ava granińi s…?",q_neighbor_not:"NE granińi s…?",
  q_plates_casual:"Iz koje drŚ¾ave je ova registracija?",q_plates_hard:"Identificirajte regiju – nema naznake!",
  q_river_real:"Kroz koju drŚ¾avu teńe ova rijeka?",q_map_guess:"Pronań‘i drŚ¾avu na karti",
  fb_correct:"✓“ Tońno! +{pts}",fb_wrong:"✗ PogreŚ¡no → {ans}",fb_time:"⏱ Kraj vremena! → {ans}",
  plates_more:"+{n} viŚ¡e",pct_complete:"{pct}% dovrŚ¡eno",
  spotter_dup:"📋 {code} ({country}) već skupljeno!",
  map_unavail:"Karta nije dostupna",map_loading:"Uńitavanje karte…",
  q_subway_km:"Koliko duga je mreŚ¾a metroa … (km)?",q_subway_lines:"Koliko linija metroa ima …?",
  diff_desc_casual:"\u{1F7E2} Casual: OpuŚ¡teno · Bez vremenskog limita · ∞ Ś½ivota",diff_desc_hc:"\u{1F525} Hardcore: Klasik · Bez limita · 3 Ś½ivota",diff_desc_surv:"\u{1F480} Survival: Protiv sata · 8s · 3 Ś½ivota",hud_lives:"Ś½IVOTI",score_mult_max:"Maks MnoŚ¾itelj",score_time_bonus:"Vremenski Bonus",pts_abbr:"bod.",score_correct_lbl:"tońno",mode_wappen:"Grbovi",mode_slf:"Grad-Zemlja-Rijeka",mode_euro:"Euro Kovanice"
},
sl:{
  play:"IGRAJ",again:"IGRAJ ZNOVA",menu:"Glavni meni",board:"Lestvica",pass:"Potni list",
  fav_empty:"Še ni shranjenih priljubljenih",
  profile:"Profil",stats:"Statistike",casual:"Casual",hardcore:"Hardcore",rounds:"Runde",
  btn_collect:"Zberi",btn_back:"Nazaj v meni",btn_next:"Naprej →’",
  btn_again:"Igraj znova",btn_menu:"Glavni meni",btn_adapt:"Prilagodi",
  spotter_title:"\u{1F697} Potovalni Spotter",
  spotter_hint:"Si videl tablico? ZapiŚ¡i jo takoj!",
  spotter_all:"Vse drŚ¾ave",spotter_unknown:"Neznana tablica",
  spotter_not_in:"ni v",spotter_but_in:"ampak je v",
  album_title:"\u{1F4D4} Album tablic",album_list:"\u{1F4DD} Seznam",album_map:"\u{1F5FA} Karta",
  album_empty_country:"Ś e niń iz {country} – uporabi Spotter!",
  album_empty:"Ś e niń zbrano!\nIgraj EU tablice ali uporabi Spotter.",
  album_codes:"kode",
  hl_higher:"⬆️ Veń / DaljŚ¡i / Veńji",hl_lower:"⬇️ Manj / KrajŚ¡i / ManjŚ¡i",
  hl_more:"⬆️ Veń prebivalcev",hl_less:"⬇️ Manj prebivalcev",
  loc_detected:"Ste v {country}",loc_adapt:"Prilagodi",
  q_city:"V kateri drŚ¾avi leŚ¾i to mesto?",q_flag:"Katera drŚ¾ava ima to zastavo?",
  q_capital:"Kateri drŚ¾avi pripada to glavno mesto?",q_river:"V kateri drŚ¾avi teńe ta reka?",
  q_landmark:"V kateri drŚ¾avi se nahaja ta znamenitost?",q_park:"V kateri drŚ¾avi se nahaja ta narodni park?",
  q_unesco:"V kateri drŚ¾avi se nahaja ta UNESCO dediŚ¡ńina?",q_citymark:"Kateremu mestu pripada ta znamenitost?",
  q_subway:"V katerem mestu je ta metro?",q_flagsel:"Katera zastava pripada…",
  q_rcapital:"KakŚ¡no je glavno mesto…?",q_rcity:"Katero mesto leŚ¾i v…?",
  q_rriver:"Katera reka teńe skozi…?",q_outline:"Katera drŚ¾ava ima to obliko?",
  q_food:"Iz katere drŚ¾ave prihaja ta jed?",q_brand:"Iz katere drŚ¾ave prihaja ta znamka?",
  q_currency:"Kateri drŚ¾avi pripada ta valuta?",q_curr_real:"KakŚ¡no valuto ima…",
  q_pop_compare:"Veń ali manj prebivalcev?",
  q_hl_pop:"Veń prebivalcev kot {a}?",q_hl_river:"DaljŚ¡i kot {a}?",q_hl_area:"Veńji kot {a}?",
  q_neighbor:"Katera drŚ¾ava meji na…?",q_neighbor_not:"NE meji na…?",
  q_plates_casual:"Iz katere drŚ¾ave je ta tablica?",q_plates_hard:"Identificirajte regijo – brez namiga!",
  q_river_real:"Skozi katero drŚ¾avo teńe ta reka?",q_map_guess:"PoiŚ¡ńi drŚ¾avo na karti",
  fb_correct:"✓“ Pravilno! +{pts}",fb_wrong:"✗ Napańno → {ans}",fb_time:"⏱ čas! → {ans}",
  plates_more:"+{n} veń",pct_complete:"{pct}% dokonńano",
  spotter_dup:"📋 {code} ({country}) Ś¾e zbrano!",
  map_unavail:"Karta ni na voljo",map_loading:"Nalaganje karte…",
  q_subway_km:"Kako dolgo je metrojsko omreŚ¾je … (km)?",q_subway_lines:"Koliko metrojskih linij ima …?",
  diff_desc_casual:"\u{1F7E2} Casual: Sprostitveno · Brez ńasovne omejitve · ∞ Ś½ivljenj",diff_desc_hc:"\u{1F525} Hardcore: Klasińno · Brez omejitve · 3 Ś½ivljenja",diff_desc_surv:"\u{1F480} Survival: Dirka s ńasom · 8s · 3 Ś½ivljenja",hud_lives:"Ś½IVLJENJA",score_mult_max:"Maks MnoŚ¾itelj",score_time_bonus:"časovni Bonus",pts_abbr:"t.",score_correct_lbl:"pravilno",mode_wappen:"Grbi",mode_slf:"Mesto-DeŚ¾ela-Reka",mode_euro:"Eurokovanice"
},
bg:{
  play:"Ð˜Ð“Ð ÐÐ™",again:"Ð˜Ð“Ð ÐÐ™ ÐžÐ¢ÐÐžÐ’Ðž",menu:"Ð“Ð»Ð°Ð²Ð½Ð¾ Ð¼ÐµÐ½ÑŽ",board:"ÐšÐ»Ð°ÑÐ°Ñ–Ð¸Ñ",pass:"ÐŸÐ°ÑÐ¿Ð¾Ñ€Ñ‚",
  profile:"ÐŸÑ€Ð¾Ñ„Ð¸Ð»",stats:"Ð¡Ñ‚Ð°Ñ‚Ð¸ÑÑ‚Ð¸ÐºÐ¸",casual:"Ð›ÐµÑÐµÐ½",hardcore:"Ð¢Ñ€ÑƒÐ´ÐµÐ½",rounds:"Ð ÑƒÐ½Ð´Ð¸",
  btn_collect:"Ð¡ÑŠÐ±ÐµÑ€Ð¸",btn_back:"ÐžÐ±Ñ€Ð°Ñ‚Ð½Ð¾ Ð² Ð¼ÐµÐ½ÑŽÑ‚Ð¾",btn_next:"ÐÐ°Ð¿Ñ€ÐµÐ´ →’",
  btn_again:"Ð˜Ð³Ñ€Ð°Ð¹ Ð¾Ñ‚Ð½Ð¾Ð²Ð¾",btn_menu:"Ð“Ð»Ð°Ð²Ð½Ð¾ Ð¼ÐµÐ½ÑŽ",btn_adapt:"ÐÐ´Ð°Ð¿Ñ‚Ð¸Ñ€Ð°Ð¹",
  spotter_title:"\u{1F697} ÐŸÑŠÑ‚ÐµÐ½ Ð¡Ð¿Ð¾Ñ‚ÑŠÑ€",
  spotter_hint:"Ð’Ð¸Ð´ÑÐ» Ñ‚Ð°Ð±ÐµÐ»Ð°? Ð—Ð°Ð¿Ð¸ÑˆÐ¸ Ñ Ð²ÐµÐ´Ð½Ð°Ð³Ð°!",
  spotter_all:"Ð’ÑÐ¸Ñ‡ÐºÐ¸ ÑÑ‚Ñ€Ð°Ð½Ð¸",spotter_unknown:"ÐÐµÐ¿Ð¾Ð·Ð½Ð°Ñ‚Ð° Ñ‚Ð°Ð±ÐµÐ»Ð°",
  spotter_not_in:"Ð½Ðµ Ðµ Ð²",spotter_but_in:"Ð½Ð¾ Ðµ Ð²",
  album_title:"\u{1F4D4} ÐÐ»Ð±ÑƒÐ¼ Ñ Ñ‚Ð°Ð±ÐµÐ»Ð¸",album_list:"\u{1F4DD} Ð¡Ð¿Ð¸ÑÑŠÐº",album_map:"\u{1F5FA} ÐšÐ°Ñ€Ñ‚Ð°",
  album_empty_country:"ÐÐ¸Ñ‰Ð¾ Ð¾Ñ‚ {country} Ð²ÑÐµ Ð¾Ñ‰Ðµ – Ð¸Ð·Ð¿Ð¾Ð»Ð·Ð²Ð°Ð¹ Ð¡Ð¿Ð¾Ñ‚ÑŠÑ€Ð°!",
  album_empty:"Ð’ÑÐµ Ð¾Ñ‰Ðµ Ð½Ð¸Ñ‰Ð¾ ÑÑŠÐ±Ñ€Ð°Ð½Ð¾!\nÐ˜Ð³Ñ€Ð°Ð¹ Ð•Ð¡ Ñ‚Ð°Ð±ÐµÐ»Ð¸ Ð¸Ð»Ð¸ Ð¸Ð·Ð¿Ð¾Ð»Ð·Ð²Ð°Ð¹ Ð¡Ð¿Ð¾Ñ‚ÑŠÑ€Ð°.",
  album_codes:"ÐºÐ¾Ð´Ð¾Ð²Ðµ",
  hl_higher:"⬆️ ÐŸÐ¾Ð²ÐµÑ‡Ðµ / ÐŸÐ¾-Ð´ÑŠÐ»Ð³Ð¾ / ÐŸÐ¾-Ð³Ð¾Ð»ÑÐ¼Ð¾",hl_lower:"⬇️ ÐŸÐ¾-Ð¼Ð°Ð»ÐºÐ¾ / ÐŸÐ¾-ÐºÑ€Ð°Ñ‚ÐºÐ¾ / ÐŸÐ¾-Ð¼Ð°Ð»ÐºÐ¾",
  hl_more:"⬆️ ÐŸÐ¾Ð²ÐµÑ‡Ðµ Ð¶Ð¸Ñ‚ÐµÐ»Ð¸",hl_less:"⬇️ ÐŸÐ¾-Ð¼Ð°Ð»ÐºÐ¾ Ð¶Ð¸Ñ‚ÐµÐ»Ð¸",
  loc_detected:"ÐÐ°Ð¼Ð¸Ñ€Ð°Ñ‚Ðµ ÑÐµ Ð² {country}",loc_adapt:"ÐÐ´Ð°Ð¿Ñ‚Ð¸Ñ€Ð°Ð¹",
  q_city:"Ð’ ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° ÑÐµ Ð½Ð°Ð¼Ð¸Ñ€Ð° Ñ‚Ð¾Ð·Ð¸ Ð³Ñ€Ð°Ð´?",q_flag:"ÐšÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ð¸Ð¼Ð° Ñ‚Ð¾Ð²Ð° Ð·Ð½Ð°Ð¼Ðµ?",
  q_capital:"ÐÐ° ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ð¿Ñ€Ð¸Ð½Ð°Ð´Ð»ÐµÐ¶Ð¸ Ñ‚Ð°Ð·Ð¸ ÑÑ‚Ð¾Ð»Ð¸Ñ–Ð°?",q_river:"Ð’ ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ñ‚ÐµÑ‡Ðµ Ñ‚Ð°Ð·Ð¸ Ñ€ÐµÐºÐ°?",
  q_landmark:"Ð’ ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° ÑÐµ Ð½Ð°Ð¼Ð¸Ñ€Ð° Ñ‚Ð°Ð·Ð¸ Ð·Ð°Ð±ÐµÐ»ÐµÐ¶Ð¸Ñ‚ÐµÐ»Ð½Ð¾ÑÑ‚?",q_park:"Ð’ ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° ÑÐµ Ð½Ð°Ð¼Ð¸Ñ€Ð° Ñ‚Ð¾Ð·Ð¸ Ð½Ð°Ñ–Ð¸Ð¾Ð½Ð°Ð»ÐµÐ½ Ð¿Ð°Ñ€Ðº?",
  q_unesco:"Ð’ ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° ÑÐµ Ð½Ð°Ð¼Ð¸Ñ€Ð° Ñ‚Ð¾Ð²Ð° Ð®ÐÐ•Ð¡ÐšÐž Ð½Ð°ÑÐ»ÐµÐ´ÑÑ‚Ð²Ð¾?",q_citymark:"ÐÐ° ÐºÐ¾Ð¹ Ð³Ñ€Ð°Ð´ Ð¿Ñ€Ð¸Ð½Ð°Ð´Ð»ÐµÐ¶Ð¸ Ñ‚Ð°Ð·Ð¸ Ð·Ð°Ð±ÐµÐ»ÐµÐ¶Ð¸Ñ‚ÐµÐ»Ð½Ð¾ÑÑ‚?",
  q_subway:"Ð’ ÐºÐ¾Ð¹ Ð³Ñ€Ð°Ð´ Ðµ Ñ‚Ð¾Ð²Ð° Ð¼ÐµÑ‚Ñ€Ð¾?",q_flagsel:"ÐšÐ¾Ðµ Ð·Ð½Ð°Ð¼Ðµ Ð¿Ñ€Ð¸Ð½Ð°Ð´Ð»ÐµÐ¶Ð¸ Ð½Ð°…",
  q_rcapital:"ÐšÐ°ÐºÐ²Ð° Ðµ ÑÑ‚Ð¾Ð»Ð¸Ñ–Ð°Ñ‚Ð° Ð½Ð°…?",q_rcity:"ÐšÐ¾Ð¹ Ð³Ñ€Ð°Ð´ ÑÐµ Ð½Ð°Ð¼Ð¸Ñ€Ð° Ð²…?",
  q_rriver:"ÐšÐ¾Ñ Ñ€ÐµÐºÐ° Ñ‚ÐµÑ‡Ðµ Ð¿Ñ€ÐµÐ·…?",q_outline:"ÐšÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ð¸Ð¼Ð° Ñ‚Ð°Ð·Ð¸ Ñ„Ð¾Ñ€Ð¼Ð°?",
  q_food:"ÐžÑ‚ ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ð¸Ð´Ð²Ð° Ñ‚Ð¾Ð²Ð° ÑÑÑ‚Ð¸Ðµ?",q_brand:"ÐžÑ‚ ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ð¸Ð´Ð²Ð° Ñ‚Ð°Ð·Ð¸ Ð¼Ð°Ñ€ÐºÐ°?",
  q_currency:"ÐÐ° ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ð¿Ñ€Ð¸Ð½Ð°Ð´Ð»ÐµÐ¶Ð¸ Ñ‚Ð°Ð·Ð¸ Ð²Ð°Ð»ÑƒÑ‚Ð°?",q_curr_real:"ÐšÐ°ÐºÐ²Ð° Ð²Ð°Ð»ÑƒÑ‚Ð° Ð¸Ð¼Ð°…",
  q_pop_compare:"ÐŸÐ¾Ð²ÐµÑ‡Ðµ Ð¸Ð»Ð¸ Ð¿Ð¾-Ð¼Ð°Ð»ÐºÐ¾ Ð¶Ð¸Ñ‚ÐµÐ»Ð¸?",
  q_hl_pop:"ÐŸÐ¾Ð²ÐµÑ‡Ðµ Ð¶Ð¸Ñ‚ÐµÐ»Ð¸ Ð¾Ñ‚ {a}?",q_hl_river:"ÐŸÐ¾-Ð´ÑŠÐ»Ð³Ð° Ð¾Ñ‚ {a}?",q_hl_area:"ÐŸÐ¾-Ð³Ð¾Ð»ÑÐ¼Ð° Ð¾Ñ‚ {a}?",
  q_neighbor:"ÐšÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ð³Ñ€Ð°Ð½Ð¸Ñ‡Ð¸ Ñ…?",q_neighbor_not:"ÐÐ• Ð³Ñ€Ð°Ð½Ð¸Ñ‡Ð¸ Ñ…?",
  q_plates_casual:"ÐžÑ‚ ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ðµ Ñ‚Ð°Ð·Ð¸ Ñ‚Ð°Ð±ÐµÐ»Ð°?",q_plates_hard:"Ð˜Ð´ÐµÐ½Ñ‚Ð¸Ñ„Ð¸Ñ–Ð¸Ñ€Ð°Ð¹Ñ‚Ðµ Ñ€ÐµÐ³Ð¸Ð¾Ð½Ð° – Ð±ÐµÐ· Ð¿Ð¾Ð´ÑÐºÐ°Ð·ÐºÐ°!",
  q_river_real:"ÐŸÑ€ÐµÐ· ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ñ‚ÐµÑ‡Ðµ Ñ‚Ð°Ð·Ð¸ Ñ€ÐµÐºÐ°?",q_map_guess:"ÐÐ°Ð¼ÐµÑ€Ð¸ ÑÑ‚Ñ€Ð°Ð½Ð°Ñ‚Ð° Ð½Ð° ÐºÐ°Ñ€Ñ‚Ð°Ñ‚Ð°",
  fb_correct:"✓“ ÐŸÑ€Ð°Ð²Ð¸Ð»Ð½Ð¾! +{pts}",fb_wrong:"✗ Ð“Ñ€ÐµÑˆÐ½Ð¾ → {ans}",fb_time:"⏱ Ð’Ñ€ÐµÐ¼ÐµÑ‚Ð¾ Ð¸Ð·Ñ‚ÐµÑ‡Ðµ! → {ans}",
  plates_more:"+{n} oÑ‰e",pct_complete:"{pct}% Ð·Ð°Ð²ÑŠÑ€ÑˆÐµÐ½Ð¾",
  spotter_dup:"📋 {code} ({country}) Ð²ÐµÑ‡e ÑÑŠÐ±Ñ€Ð°Ð½Ð¾!",
  map_unavail:"ÐšÐ°Ñ€Ñ‚Ð°Ñ‚Ð° Ð½Ðµ Ðµ Ð´Ð¾ÑÑ‚ÑŠÐ¿Ð½Ð°",map_loading:"Ð—Ð°Ñ€ÐµÐ¶Ð´Ð°Ð½Ðµ Ð½Ð° ÐºÐ°Ñ€Ñ‚Ð°Ñ‚Ð°…",
  q_subway_km:"ÐšÐ¾Ð»ÐºÐ¾ Ð´ÑŠÐ»Ð³Ð° Ðµ Ð¼ÐµÑ‚Ñ€Ð¾Ñ‚Ð¾ … (km)?",q_subway_lines:"ÐšÐ¾Ð»ÐºÐ¾ Ð¼ÐµÑ‚Ñ€Ð¾Ð»Ð¸Ð½Ð¸Ð¸ Ð¸Ð¼Ð° …?",
  diff_desc_casual:"\u{1F7E2} Casual: Ð Ð°Ð·Ñ…Ð¾Ð´ÐµÐ½ · Ð‘ÐµÐ· Ð»Ð¸Ð¼Ð¸Ñ‚ · ∞ Ð–Ð¸Ð²Ð¾Ñ‚Ð°",diff_desc_hc:"\u{1F525} Hardcore: ÐšÐ»Ð°ÑÐ¸Ðº · Ð‘ÐµÐ· Ð»Ð¸Ð¼Ð¸Ñ‚ · 3 Ð–Ð¸Ð²Ð¾Ñ‚Ð°",diff_desc_surv:"\u{1F480} Survival: Ð¡Ñ€ÐµÑ‰Ñƒ Ð²Ñ€ÐµÐ¼ÐµÑ‚Ð¾ · 8Ñ · 3 Ð–Ð¸Ð²Ð¾Ñ‚Ð°",hud_lives:"Ð–Ð˜Ð’ÐžÐ¢Ð",score_mult_max:"ÐœÐ°ÐºÑ ÐœÐ½Ð¾Ð¶Ð¸Ñ‚ÐµÐ»",score_time_bonus:"Ð’Ñ€ÐµÐ¼ÐµÐ² Ð‘Ð¾Ð½ÑƒÑ",pts_abbr:"Ñ‚.",score_correct_lbl:"Ð¿Ñ€Ð°Ð²Ð¸Ð»Ð½Ð¾",mode_wappen:"Ð“ÐµÑ€Ð±Ð¾Ð²Ðµ",mode_slf:"Ð“Ñ€Ð°Ð´-Ð¡Ñ‚Ñ€Ð°Ð½Ð°-Ð ÐµÐºÐ°",mode_euro:"Ð•Ð²Ñ€Ð¾Ð¼Ð¾Ð½ÐµÑ‚Ð¸"
},
el:{
  play:"Î Î‘Î™ÎžÎ•",again:"Î Î‘Î™ÎžÎ• ÎžÎ‘ÎÎ‘",menu:"ÎšÏÏÎ¹Î¿ Î¼ÎµÎ½Î¿Ï",board:"ÎšÎ±Ï„Î¬Ï„Î±Î¾Î·",pass:"Î”Î¹Î±Î²Î±Ï„Î®ÏÎ¹Î¿",
  profile:"Î ÏÎ¿Ï–Î¯Î»",stats:"Î£Ï„Î±Ï„Î¹ÏƒÏ„Î¹ÎºÎ¬",casual:"Î•ÏÎºÎ¿Î»Î¿",hardcore:"Î”ÏÏƒÎºÎ¿Î»Î¿",rounds:"Î“ÏÏÎ¿Î¹",
  btn_collect:"Î£Ï…Î»Î»Î¿Î³Î®",btn_back:"Î Î¯ÏƒÏ‰ ÏƒÏ„Î¿ Î¼ÎµÎ½Î¿Ï",btn_next:"Î•Ï€ÏŒÎ¼ÎµÎ½Î¿ →’",
  btn_again:"Î Î±Î¯Î¾Îµ Î¾Î±Î½Î¬",btn_menu:"ÎšÏÏÎ¹Î¿ Î¼ÎµÎ½Î¿Ï",btn_adapt:"Î ÏÎ¿ÏƒÎ±ÏÎ¼Î¿Î³Î®",
  spotter_title:"\u{1F697} Spotter Î¤Î±Î¾Î¹Î´Î¹Î¿Ï",
  spotter_hint:"Î•Î¯Î´ÎµÏ‚ Ï€Î¹Î½Î±ÎºÎ¯Î´Î±; ÎšÎ±Ï„Î±Ï‡ÏŽÏÎ·ÏƒÎ­ Ï„Î·Î½ Ï„ÏŽÏÎ±!",
  spotter_all:"ÎŒÎ»ÎµÏ‚ Î¿Î¹ Ï‡ÏŽÏÎµÏ‚",spotter_unknown:"Î–Î³Î½Ï‰ÏƒÏ„Î· Ï€Î¹Î½Î±ÎºÎ¯Î´Î±",
  spotter_not_in:"Î´ÎµÎ½ ÎµÎ¯Î½Î±Î¹ ÏƒÎµ",spotter_but_in:"Î±Î»Î»Î¬ ÏƒÎµ",
  album_title:"\u{1F4D4} Î£Ï…Î»Î»Î¿Î³Î® Ï€Î¹Î½Î±ÎºÎ¯Î´Ï‰Î½",album_list:"\u{1F4DD} Î›Î¯ÏƒÏ„Î±",album_map:"\u{1F5FA} Î§Î¬ÏÏ„Î·Ï‚",
  album_empty_country:"Î¤Î¯Ï€Î¿Ï„Î± Î±Ï€ÏŒ {country} Î±ÎºÏŒÎ¼Î± – Ï‡ÏÎ·ÏƒÎ¹Î¼Î¿Ï€Î¿Î¯Î·ÏƒÎµ Ï„Î¿ Spotter!",
  album_empty:"Î”ÎµÎ½ Î­Ï‡ÎµÎ¹Ï‚ ÏƒÏ…Î»Î»Î­Î¾ÎµÎ¹ Ï„Î¯Ï€Î¿Ï„Î± Î±ÎºÏŒÎ¼Î±!\nÎ Î±Î¯Î¾Îµ Ï€Î¹Î½Î±ÎºÎ¯Î´ÎµÏ‚ Î•Î• Î® Ï‡ÏÎ·ÏƒÎ¹Î¼Î¿Ï€Î¿Î¯Î·ÏƒÎµ Ï„Î¿ Spotter.",
  album_codes:"ÎºÏ‰Î´Î¹ÎºÎ¿Î¯",
  hl_higher:"⬆️ Î ÎµÏÎ¹ÏƒÏƒÏŒÏ„ÎµÏÎ¿ / ÎœÎµÎ³Î±Î»ÏÏ„ÎµÏÎ¿ / ÎœÎµÎ³Î±Î»ÏÏ„ÎµÏÎ¿",hl_lower:"⬇️ Î›Î¹Î³ÏŒÏ„ÎµÏÎ¿ / ÎœÎ¹ÎºÏÏŒÏ„ÎµÏÎ¿ / ÎœÎ¹ÎºÏÏŒÏ„ÎµÏÎ¿",
  hl_more:"⬆️ Î ÎµÏÎ¹ÏƒÏƒÏŒÏ„ÎµÏÎ¿Î¹ ÎºÎ¬Ï„Î¿Î¹ÎºÎ¿Î¹",hl_less:"⬇️ Î›Î¹Î³ÏŒÏ„ÎµÏÎ¿Î¹ ÎºÎ¬Ï„Î¿Î¹ÎºÎ¿Î¹",
  loc_detected:"Î’ÏÎ¯ÏƒÎºÎµÏƒÏ„Îµ ÏƒÏ„Î·Î½/ÏƒÏ„Î¿ {country}",loc_adapt:"Î ÏÎ¿ÏƒÎ±ÏÎ¼Î¿Î³Î®",
  q_city:"Î£Îµ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Î²ÏÎ¯ÏƒÎºÎµÏ„Î±Î¹ Î±Ï…Ï„Î® Î· Ï€ÏŒÎ»Î·;",q_flag:"Î Î¿Î¹Î± Ï‡ÏŽÏÎ± Î­Ï‡ÎµÎ¹ Î±Ï…Ï„Î® Ï„Î· ÏƒÎ·Î¼Î±Î¯Î±;",
  q_capital:"Î£Îµ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Î±Î½Î®ÎºÎµÎ¹ Î±Ï…Ï„Î® Î· Ï€ÏÏ‰Ï„ÎµÏÎ¿Ï…ÏƒÎ±;",q_river:"Î£Îµ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Î²ÏÎ¯ÏƒÎºÎµÏ„Î±Î¹ Î±Ï…Ï„ÏŒ Ï„Î¿ Ï€Î¿Ï„Î¬Î¼Î¹;",
  q_landmark:"Î£Îµ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Î²ÏÎ¯ÏƒÎºÎµÏ„Î±Î¹ Î±Ï…Ï„ÏŒ Ï„Î¿ Î¼Î½Î·Î¼ÎµÎ¯Î¿;",q_park:"Î£Îµ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Î²ÏÎ¯ÏƒÎºÎµÏ„Î±Î¹ Î±Ï…Ï„ÏŒ Ï„Î¿ ÎµÎ¸Î½Î¹ÎºÏŒ Ï€Î¬ÏÎºÎ¿;",
  q_unesco:"Î£Îµ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Î²ÏÎ¯ÏƒÎºÎµÏ„Î±Î¹ Î±Ï…Ï„ÏŒ Ï„Î¿ Î¼Î½Î·Î¼ÎµÎ¯Î¿ UNESCO;",q_citymark:"Î£Îµ Ï€Î¿Î¹Î± Ï€ÏŒÎ»Î· Î±Î½Î®ÎºÎµÎ¹ Î±Ï…Ï„ÏŒ Ï„Î¿ Î¼Î½Î·Î¼ÎµÎ¯Î¿;",
  q_subway:"Î£Îµ Ï€Î¿Î¹Î± Ï€ÏŒÎ»Î· Î²ÏÎ¯ÏƒÎºÎµÏ„Î±Î¹ Î±Ï…Ï„ÏŒ Ï„Î¿ Î¼ÎµÏ„ÏÏŒ;",q_flagsel:"Î Î¿Î¹Î± ÏƒÎ·Î¼Î±Î¯Î± Î±Î½Î®ÎºÎµÎ¹ ÏƒÏ„Î·…",
  q_rcapital:"Î Î¿Î¹Î± ÎµÎ¯Î½Î±Î¹ Î· Ï€ÏÏ‰Ï„ÎµÏÎ¿Ï…ÏƒÎ± Ï„Î·Ï‚/Ï„Î¿Ï……;",q_rcity:"Î Î¿Î¹Î± Ï€ÏŒÎ»Î· Î²ÏÎ¯ÏƒÎºÎµÏ„Î±Î¹ ÏƒÏ„Î·/ÏƒÏ„Î¿…;",
  q_rriver:"Î Î¿Î¹Î¿ Ï€Î¿Ï„Î¬Î¼Î¹ Î´Î¹Î±ÏÏÎ­ÎµÎ¹ Ï„Î·/Ï„Î¿…;",q_outline:"Î Î¿Î¹Î± Ï‡ÏŽÏÎ± Î­Ï‡ÎµÎ¹ Î±Ï…Ï„ÏŒ Ï„Î¿ ÏƒÏ‡Î®Î¼Î±;",
  q_food:"Î‘Ï€ÏŒ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Ï€ÏÎ¿Î­ÏÏ‡ÎµÏ„Î±Î¹ Î±Ï…Ï„ÏŒ Ï„Î¿ Ï€Î¹Î¬Ï„Î¿;",q_brand:"Î‘Ï€ÏŒ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Ï€ÏÎ¿Î­ÏÏ‡ÎµÏ„Î±Î¹ Î±Ï…Ï„Î® Î· Î¼Î¬ÏÎºÎ±;",
  q_currency:"Î£Îµ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Î±Î½Î®ÎºÎµÎ¹ Î±Ï…Ï„ÏŒ Ï„Î¿ Î½ÏŒÎ¼Î¹ÏƒÎ¼Î±;",q_curr_real:"Î Î¿Î¹Î¿ Î½ÏŒÎ¼Î¹ÏƒÎ¼Î± Î­Ï‡ÎµÎ¹ Î·/Î¿…",
  q_pop_compare:"Î ÎµÏÎ¹ÏƒÏƒÏŒÏ„ÎµÏÎ¿Î¹ Î® Î»Î¹Î³ÏŒÏ„ÎµÏÎ¿Î¹ ÎºÎ¬Ï„Î¿Î¹ÎºÎ¿Î¹;",
  q_hl_pop:"Î ÎµÏÎ¹ÏƒÏƒÏŒÏ„ÎµÏÎ¿Î¹ ÎºÎ¬Ï„Î¿Î¹ÎºÎ¿Î¹ Î±Ï€ÏŒ Ï„Î·/Ï„Î¿Î½ {a};",q_hl_river:"ÎœÎµÎ³Î±Î»ÏÏ„ÎµÏÎ¿ Î±Ï€ÏŒ Ï„Î·/Ï„Î¿Î½ {a};",q_hl_area:"ÎœÎµÎ³Î±Î»ÏÏ„ÎµÏÎ· Î±Ï€ÏŒ Ï„Î·/Ï„Î¿Î½ {a};",
  q_neighbor:"Î Î¿Î¹Î± Ï‡ÏŽÏÎ± ÏƒÏ…Î½Î¿ÏÎµÏÎµÎ¹ Î¼Îµ Ï„Î·/Ï„Î¿…;",q_neighbor_not:"Î”Î•Î ÏƒÏ…Î½Î¿ÏÎµÏÎµÎ¹ Î¼Îµ Ï„Î·/Ï„Î¿…;",
  q_plates_casual:"Î‘Ï€ÏŒ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± ÎµÎ¯Î½Î±Î¹ Î±Ï…Ï„Î® Î· Ï€Î¹Î½Î±ÎºÎ¯Î´Î±;",q_plates_hard:"Î‘Î½Î±Î³Î½Ï‰ÏÎ¯ÏƒÏ„Îµ Ï„Î·Î½ Ï€ÎµÏÎ¹Î¿Ï‡Î® – Ï‡Ï‰ÏÎ¯Ï‚ Ï…Ï€ÏŒÎ´ÎµÎ¹Î¾Î·!",
  q_river_real:"ÎœÎ­ÏƒÎ± Î±Ï€ÏŒ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Î´Î¹Î±ÏÏÎ­ÎµÎ¹ Î±Ï…Ï„ÏŒ Ï„Î¿ Ï€Î¿Ï„Î¬Î¼Î¹;",q_map_guess:"Î’ÏÎµÏ‚ Ï„Î· Ï‡ÏŽÏÎ± ÏƒÏ„Î¿Î½ Ï‡Î¬ÏÏ„Î·",
  fb_correct:"✓“ Î£Ï‰ÏƒÏ„ÏŒ! +{pts}",fb_wrong:"✗ Î›Î¬Î¸Î¿Ï‚ → {ans}",fb_time:"⏱ Î¤Î­Î»Î¿Ï‚ Ï‡ÏÏŒÎ½Î¿Ï…! → {ans}",
  plates_more:"+{n} Î±ÎºÏŒÎ¼Î±",pct_complete:"{pct}% Î¿Î»Î¿ÎºÎ»Î·ÏÏŽÎ¸Î·ÎºÎµ",
  spotter_dup:"📋 {code} ({country}) Î®Î´Î· ÏƒÏ…Î»Î»Î­Ï‡Î¸Î·ÎºÎµ!",
  map_unavail:"Î§Î¬ÏÏ„Î·Ï‚ Î¼Î· Î´Î¹Î±Î¸Î­ÏƒÎ¹Î¼Î¿Ï‚",map_loading:"Î¦ÏŒÏÏ„Ï‰ÏƒÎ· Ï‡Î¬ÏÏ„Î·…",
  q_subway_km:"Î ÏŒÏƒÎ¿ Î¼Î±ÎºÏÏ ÎµÎ¯Î½Î±Î¹ Ï„Î¿ Î¼ÎµÏ„ÏÏŒ … (km)?",q_subway_lines:"Î ÏŒÏƒÎµÏ‚ Î³ÏÎ±Î¼Î¼Î­Ï‚ Î¼ÎµÏ„ÏÏŒ Î­Ï‡ÎµÎ¹ …?",
  diff_desc_casual:"\u{1F7E2} Casual: Î‘Î½ÎµÏ„Î¿ · Î§Ï‰ÏÎ¯Ï‚ ÏŒÏÎ¹Î¿ · ∞ Î–Ï‰Î­Ï‚",diff_desc_hc:"\u{1F525} Hardcore: ÎšÎ»Î±ÏƒÎ¹ÎºÏŒ · Î§Ï‰ÏÎ¯Ï‚ ÏŒÏÎ¹Î¿ · 3 Î–Ï‰Î­Ï‚",diff_desc_surv:"\u{1F480} Survival: Î•Î½Î±Î½Ï„Î¯Î¿Î½ Ï‡ÏÏŒÎ½Î¿Ï… · 8Î´Î» · 3 Î–Ï‰Î­Ï‚",hud_lives:"Î–Î©Î•Î£",score_mult_max:"ÎœÎ­Î³Î¹ÏƒÏ„Î¿Ï‚ Î Î¿Î»Î»Î±Ï€Î»Î±ÏƒÎ¹Î±ÏƒÏ„Î®Ï‚",score_time_bonus:"ÎœÏ€ÏŒÎ½Î¿Ï…Ï‚ Î§ÏÏŒÎ½Î¿Ï…",pts_abbr:"Î¼ÏŒÏ.",score_correct_lbl:"ÏƒÏ‰ÏƒÏ„Î¬",mode_wappen:"Î•Î¸Î½ÏŒÏƒÎ·Î¼Î±",mode_slf:"Î ÏŒÎ»Î·-Î§ÏŽÏÎ±-Î Î¿Ï„Î¬Î¼Î¹",mode_euro:"ÎšÎ­ÏÎ¼Î±Ï„Î± Î•Ï…ÏÏŽ"
},
da:{
  play:"SPIL",again:"SPIL IGEN",menu:"Hovedmenu",board:"Rangliste",pass:"Pas",
  profile:"Profil",stats:"Statistik",casual:"Casual",hardcore:"Hardcore",rounds:"Runder",
  btn_collect:"Samle",btn_back:"Tilbage til menu",btn_next:"Nß¦ste →’",
  btn_again:"Spil igen",btn_menu:"Hovedmenu",btn_adapt:"Tilpas",
  spotter_title:"\u{1F697} Rejse-Spotter",
  spotter_hint:"Set en nummerplade? Notér den nu!",
  spotter_all:"Alle lande",spotter_unknown:"Ukendt nummerplade",
  spotter_not_in:"ikke i",spotter_but_in:"men i",
  album_title:"\u{1F4D4} Nummerplade-album",album_list:"\u{1F4DD} Liste",album_map:"\u{1F5FA} Kort",
  album_empty_country:"Intet fra {country} endnu – brug Spotter!",
  album_empty:"Intet indsamlet endnu!\nSpil EU-nummerplader eller brug Spotter.",
  album_codes:"koder",
  hl_higher:"⬆️ Mere / Lß¦ngere / Stß¸rre",hl_lower:"⬇️ Mindre / Kortere / Mindre",
  hl_more:"⬆️ Flere indbyggere",hl_less:"⬇️ Fß¦rre indbyggere",
  loc_detected:"Du er i {country}",loc_adapt:"Tilpas",
  q_city:"I hvilket land ligger denne by?",q_flag:"Hvilket land har dette flag?",
  q_capital:"Hvilke land tilhß¸rer denne hovedstad?",q_river:"I hvilket land lß¸ber denne flod?",
  q_landmark:"I hvilket land ligger dette monument?",q_park:"I hvilket land ligger denne nationalpark?",
  q_unesco:"I hvilket land ligger dette UNESCO-sted?",q_citymark:"Hvilken by tilhß¸rer dette monument?",
  q_subway:"I hvilken by er denne metro?",q_flagsel:"Hvilket flag tilhß¸rer…",
  q_rcapital:"Hvad er hovedstaden i…?",q_rcity:"Hvilken by ligger i…?",
  q_rriver:"Hvilken flod lß¸ber gennem…?",q_outline:"Hvilket land har denne form?",
  q_food:"Fra hvilket land kommer denne ret?",q_brand:"Fra hvilket land kommer dette mß¦rke?",
  q_currency:"Hvilket land tilhß¸rer denne valuta?",q_curr_real:"Hvilken valuta har…",
  q_pop_compare:"Flere eller fß¦rre indbyggere?",
  q_hl_pop:"Flere indbyggere end {a}?",q_hl_river:"Lß¦ngere end {a}?",q_hl_area:"Stß¸rre end {a}?",
  q_neighbor:"Hvilket land grß¦nser op til…?",q_neighbor_not:"Grß¦nser IKKE op til…?",
  q_plates_casual:"Fra hvilket land er denne nummerplade?",q_plates_hard:"Identificér regionen – ingen hint!",
  q_river_real:"Gennem hvilket land lß¸ber denne flod?",q_map_guess:"Find landet pß¥ kortet",
  fb_correct:"✓“ Korrekt! +{pts}",fb_wrong:"✗ Forkert → {ans}",fb_time:"⏱ Tid! → {ans}",
  plates_more:"+{n} mere",pct_complete:"{pct}% fuldfß¸rt",
  spotter_dup:"📋 {code} ({country}) allerede indsamlet!",
  map_unavail:"Kort ikke tilgß¦ngeligt",map_loading:"Indlß¦ser kort…",
  q_subway_km:"Hvor lang er metronetvß¦rket … (km)?",q_subway_lines:"Hvor mange metrolinjer har …?",
  diff_desc_casual:"\u{1F7E2} Casual: Afslappet · Ingen tidsgrß¦nse · ∞ Liv",diff_desc_hc:"\u{1F525} Hardcore: Klassisk · Ingen tidsgrß¦nse · 3 Liv",diff_desc_surv:"\u{1F480} Survival: Mod uret · 8s · 3 Liv",hud_lives:"LIV",score_mult_max:"Maks Multiplikator",score_time_bonus:"Tidsbonus",pts_abbr:"pt.",score_correct_lbl:"korrekt",mode_wappen:"Vß¥benskjolde",mode_slf:"By-Land-Flod",mode_euro:"Euromß¸nter"
},
sv:{
  play:"SPELA",again:"SPELA IGEN",menu:"Huvudmeny",board:"Rankningslista",pass:"Pass",
  profile:"Profil",stats:"Statistik",casual:"Casual",hardcore:"Hardcore",rounds:"Rundor",
  btn_collect:"Samla",btn_back:"Tillbaka till menyn",btn_next:"Nästa →’",
  btn_again:"Spela igen",btn_menu:"Huvudmeny",btn_adapt:"Anpassa",
  spotter_title:"\u{1F697} Resespotter",
  spotter_hint:"Sett en skylt? Notera den nu!",
  spotter_all:"Alla länder",spotter_unknown:"Okänd skylt",
  spotter_not_in:"inte i",spotter_but_in:"men i",
  album_title:"\u{1F4D4} Skyltalbum",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Karta",
  album_empty_country:"Inget frß¥n {country} ännu – använd Spotter!",
  album_empty:"Inget samlat ännu!\nSpela EU-skyltar eller använd Spotter.",
  album_codes:"koder",
  hl_higher:"⬆️ Mer / Längre / Större",hl_lower:"⬇️ Mindre / Kortare / Mindre",
  hl_more:"⬆️ Fler invß¥nare",hl_less:"⬇️ Färre invß¥nare",
  loc_detected:"Du är i {country}",loc_adapt:"Anpassa",
  q_city:"I vilket land ligger den här staden?",q_flag:"Vilket land har den här flaggan?",
  q_capital:"Vilket land tillhör den här huvudstaden?",q_river:"I vilket land flödar den här floden?",
  q_landmark:"I vilket land finns det här monumentet?",q_park:"I vilket land finns den här nationalparken?",
  q_unesco:"I vilket land finns det här UNESCO-arvet?",q_citymark:"Vilken stad tillhör det här monumentet?",
  q_subway:"I vilken stad finns den här tunnelbanan?",q_flagsel:"Vilken flagga tillhör…",
  q_rcapital:"Vad är huvudstaden i…?",q_rcity:"Vilken stad finns i…?",
  q_rriver:"Vilken flod rinner genom…?",q_outline:"Vilket land har den här formen?",
  q_food:"Frß¥n vilket land kommer den här rätten?",q_brand:"Frß¥n vilket land kommer det här märket?",
  q_currency:"Vilket land tillhör den här valutan?",q_curr_real:"Vilken valuta har…",
  q_pop_compare:"Fler eller färre invß¥nare?",
  q_hl_pop:"Fler invß¥nare än {a}?",q_hl_river:"Längre än {a}?",q_hl_area:"Större än {a}?",
  q_neighbor:"Vilket land gränsar till…?",q_neighbor_not:"Gränsar INTE till…?",
  q_plates_casual:"Frß¥n vilket land är den här skylten?",q_plates_hard:"Identifiera regionen – inget tips!",
  q_river_real:"Genom vilket land flödar den här floden?",q_map_guess:"Hitta landet pß¥ kartan",
  fb_correct:"✓“ Rätt! +{pts}",fb_wrong:"✗ Fel → {ans}",fb_time:"⏱ Tid! → {ans}",
  plates_more:"+{n} till",pct_complete:"{pct}% klart",
  spotter_dup:"📋 {code} ({country}) redan insamlat!",
  map_unavail:"Karta ej tillgänglig",map_loading:"Laddar karta…",
  q_subway_km:"Hur lß¥ng är tunnelbanenätet … (km)?",q_subway_lines:"Hur mß¥nga tunnelbanelinjer har …?",
  diff_desc_casual:"\u{1F7E2} Casual: Avslappnad · Ingen tidsgräns · ∞ Liv",diff_desc_hc:"\u{1F525} Hardcore: Klassisk · Ingen tidsgräns · 3 Liv",diff_desc_surv:"\u{1F480} Survival: Mot klockan · 8s · 3 Liv",hud_lives:"LIV",score_mult_max:"Max Multiplikator",score_time_bonus:"Tidsbonus",pts_abbr:"pt.",score_correct_lbl:"rätt",mode_wappen:"Vapen",mode_slf:"Stad-Land-Flod",mode_euro:"Euromynt"
},
fi:{
  play:"PELAA",again:"PELAA UUDELLEEN",menu:"Päävalikko",board:"Tulostaulukko",pass:"Passi",
  profile:"Profiili",stats:"Tilastot",casual:"Helppo",hardcore:"Vaikea",rounds:"Kierrokset",
  btn_collect:"Kerää",btn_back:"Takaisin päävalikkoon",btn_next:"Seuraava →’",
  btn_again:"Pelaa uudelleen",btn_menu:"Päävalikko",btn_adapt:"Muokkaa",
  spotter_title:"\u{1F697} Matkaspotter",
  spotter_hint:"Näitkö rekisterikilven? Kirjaa se heti!",
  spotter_all:"Kaikki maat",spotter_unknown:"Tuntematon rekisterikilpi",
  spotter_not_in:"ei kohteessa",spotter_but_in:"mutta kohteessa",
  album_title:"\u{1F4D4} Rekisterikilpialbumi",album_list:"\u{1F4DD} Luettelo",album_map:"\u{1F5FA} Kartta",
  album_empty_country:"Ei vielä mitään kohteesta {country} – käytä Spotteria!",
  album_empty:"Ei vielä kerätty mitään!\nPelaa EU-rekisterikilpiä tai käytä Spotteria.",
  album_codes:"koodit",
  hl_higher:"⬆️ Enemmän / Pidempi / Suurempi",hl_lower:"⬇️ Vähemmän / Lyhyempi / Pienempi",
  hl_more:"⬆️ Enemmän asukkaita",hl_less:"⬇️ Vähemmän asukkaita",
  loc_detected:"Olet kohteessa {country}",loc_adapt:"Muokkaa",
  q_city:"Missä maassa tämä kaupunki sijaitsee?",q_flag:"Minkä maan tämä lippu on?",
  q_capital:"Mille maalle tämä pääkaupunki kuuluu?",q_river:"Missä maassa tämä joki sijaitsee?",
  q_landmark:"Missä maassa tämä nähtävyys sijaitsee?",q_park:"Missä maassa tämä kansallispuisto sijaitsee?",
  q_unesco:"Missä maassa tämä UNESCO-kohde sijaitsee?",q_citymark:"Mille kaupungille tämä nähtävyys kuuluu?",
  q_subway:"Missä kaupungissa tämä metro on?",q_flagsel:"Mikä lippu kuuluu…",
  q_rcapital:"Mikä on… pääkaupunki?",q_rcity:"Mikä kaupunki sijaitsee…?",
  q_rriver:"Mikä joki virtaa läpi…?",q_outline:"Minkä maan muoto tämä on?",
  q_food:"Mistä maasta tämä ruoka tulee?",q_brand:"Mistä maasta tämä merkki tulee?",
  q_currency:"Minkä maan valuutta tämä on?",q_curr_real:"Mikä valuutta on…",
  q_pop_compare:"Enemmän vai vähemmän asukkaita?",
  q_hl_pop:"Enemmän asukkaita kuin {a}?",q_hl_river:"Pidempi kuin {a}?",q_hl_area:"Suurempi kuin {a}?",
  q_neighbor:"Mikä maa rajoittuu…?",q_neighbor_not:"EI rajoitu…?",
  q_plates_casual:"Minkä maan rekisterikilpi tämä on?",q_plates_hard:"Tunnista alue – ei vihjettä!",
  q_river_real:"Minkä maan läpi tämä joki virtaa?",q_map_guess:"Etsi maa kartalta",
  fb_correct:"✓“ Oikein! +{pts}",fb_wrong:"✗ Väärin → {ans}",fb_time:"⏱ Aika! → {ans}",
  plates_more:"+{n} lisää",pct_complete:"{pct}% valmis",
  spotter_dup:"📋 {code} ({country}) jo kerätty!",
  map_unavail:"Kartta ei saatavilla",map_loading:"Ladataan karttaa…",
  q_subway_km:"Kuinka pitkä on metroverkosto … (km)?",q_subway_lines:"Kuinka monta metrolinjaa on …?",
  diff_desc_casual:"\u{1F7E2} Casual: Rento · Ei aikarajaa · ∞ Elämää",diff_desc_hc:"\u{1F525} Hardcore: Klassinen · Ei aikarajaa · 3 Elämää",diff_desc_surv:"\u{1F480} Survival: Aikaa vastaan · 8s · 3 Elämää",hud_lives:"ELß„Mß„T",score_mult_max:"Maks Kerroin",score_time_bonus:"Aikabonus",pts_abbr:"p.",score_correct_lbl:"oikein",mode_wappen:"Vaakunat",mode_slf:"Kaupunki-Maa-Joki",mode_euro:"Eurokolikot"
},
et:{
  play:"Mß„NGI",again:"Mß„NGI UUESTI",menu:"Peamenüü",board:"Edetabel",pass:"Pass",
  profile:"Profiil",stats:"Statistika",casual:"Lihtne",hardcore:"Raske",rounds:"Voorud",
  btn_collect:"Kogu",btn_back:"Tagasi menüüsse",btn_next:"Järgmine →’",
  btn_again:"Mängi uuesti",btn_menu:"Peamenüü",btn_adapt:"Kohanda",
  spotter_title:"\u{1F697} Reisispotter",
  spotter_hint:"Nägid numbrimärki? Kirjuta kohe üles!",
  spotter_all:"Kßµik riigid",spotter_unknown:"Tundmatu numbrimärk",
  spotter_not_in:"ei ole",spotter_but_in:"aga on",
  album_title:"\u{1F4D4} Numbrimärkide album",album_list:"\u{1F4DD} Nimekiri",album_map:"\u{1F5FA} Kaart",
  album_empty_country:"Veel midagi {country} – kasuta Spotterit!",
  album_empty:"Veel midagi kogutud!\nMängi EL-i numbrimärke vßµi kasuta Spotterit.",
  album_codes:"koodid",
  hl_higher:"⬆️ Rohkem / Pikem / Suurem",hl_lower:"⬇️ Vähem / Lühem / Väiksem",
  hl_more:"⬆️ Rohkem elanikke",hl_less:"⬇️ Vähem elanikke",
  loc_detected:"Oled {country}",loc_adapt:"Kohanda",
  q_city:"Millises riigis see linn asub?",q_flag:"Millise riigi lipp see on?",
  q_capital:"Millisele riigile see pealinn kuulub?",q_river:"Millises riigis see jßµgi voolab?",
  q_landmark:"Millises riigis see vaatamisväärsus asub?",q_park:"Millises riigis see rahvuspark asub?",
  q_unesco:"Millises riigis see UNESCO objekt asub?",q_citymark:"Millisele linnale see vaatamisväärsus kuulub?",
  q_subway:"Millises linnas see metroo on?",q_flagsel:"Milline lipp kuulub…",
  q_rcapital:"Mis on… pealinn?",q_rcity:"Milline linn asub…?",
  q_rriver:"Milline jßµgi voolab läbi…?",q_outline:"Millisel riigil on see kuju?",
  q_food:"Millisest riigist see roog pärineb?",q_brand:"Millisest riigist see bränd pärineb?",
  q_currency:"Millisele riigile see valuuta kuulub?",q_curr_real:"Mis valuuta on…",
  q_pop_compare:"Rohkem vßµi vähem elanikke?",
  q_hl_pop:"Rohkem elanikke kui {a}?",q_hl_river:"Pikem kui {a}?",q_hl_area:"Suurem kui {a}?",
  q_neighbor:"Milline riik piirneb…?",q_neighbor_not:"EI piirne…?",
  q_plates_casual:"Millisest riigist see numbrimärk on?",q_plates_hard:"Tuvasta piirkond – vihjeta!",
  q_river_real:"Läbi millise riigi see jßµgi voolab?",q_map_guess:"Leia riik kaardilt",
  fb_correct:"✓“ ß•ige! +{pts}",fb_wrong:"✗ Vale → {ans}",fb_time:"⏱ Aeg! → {ans}",
  plates_more:"+{n} veel",pct_complete:"{pct}% täidetud",
  spotter_dup:"📋 {code} ({country}) juba kogutud!",
  map_unavail:"Kaart pole saadaval",map_loading:"Kaardi laadimine…",
  q_subway_km:"Kui pikk on metroovßµrk … (km)?",q_subway_lines:"Kui palju metroliine on …?",
  diff_desc_casual:"\u{1F7E2} Casual: Lßµßµgastav · Pole ajalimiiti · ∞ Elu",diff_desc_hc:"\u{1F525} Hardcore: Klassikaline · Pole limiiti · 3 Elu",diff_desc_surv:"\u{1F480} Survival: Aja vastu · 8s · 3 Elu",hud_lives:"ELUD",score_mult_max:"Max Kordaja",score_time_bonus:"Ajaboonus",pts_abbr:"pt.",score_correct_lbl:"ßµige",mode_wappen:"Vapid",mode_slf:"Linn-Maa-Jßµgi",mode_euro:"Euromündid"
},
lv:{
  play:"SPń’Lń’T",again:"SPń’Lń’T Vń’LREIZ",menu:"Galvenń izvń“lne",board:"Vń“rtń“jums",pass:"Pase",
  profile:"Profils",stats:"Statistika",casual:"Viegls",hardcore:"GrŚ«ts",rounds:"Kńrtas",
  btn_collect:"Savńkt",btn_back:"Atpakań¼ uz izvń“lni",btn_next:"Tńlńk →’",
  btn_again:"Spń“lń“t vń“lreiz",btn_menu:"Galvenń izvń“lne",btn_adapt:"Pielńgot",
  spotter_title:"\u{1F697} Ceń¼ojuma Spotter",
  spotter_hint:"Redzń“ji numura zń«mi? Reń£istrń“ to tagad!",
  spotter_all:"Visas valstis",spotter_unknown:"Nezinńma numura zń«me",
  spotter_not_in:"nav",spotter_but_in:"bet ir",
  album_title:"\u{1F4D4} Numuru zń«mju albums",album_list:"\u{1F4DD} Saraksts",album_map:"\u{1F5FA} Karte",
  album_empty_country:"Vń“l nekas no {country} – izmanto Spotter!",
  album_empty:"Vń“l nekas savńkts!\nSpń“lń“ ES numura zń«mes vai izmanto Spotter.",
  album_codes:"kodi",
  hl_higher:"⬆️ Vairńk / Garńks / Lielńks",hl_lower:"⬇️ Mazńk / ńªsńks / Mazńks",
  hl_more:"⬆️ Vairńk iedzń«votńju",hl_less:"⬇️ Mazńk iedzń«votńju",
  loc_detected:"Atrodaties {country}",loc_adapt:"Pielńgot",
  q_city:"Kurń valstń« atrodas Ś¡ń« pilsń“ta?",q_flag:"Kuras valsts Ś¡is karogs?",
  q_capital:"Kurai valstij pieder Ś¡ń« galvaspilsń“ta?",q_river:"Kurń valstń« tek Ś¡ń« upe?",
  q_landmark:"Kurń valstń« atrodas Ś¡is piemineklis?",q_park:"Kurń valstń« atrodas Ś¡is nacionńlais parks?",
  q_unesco:"Kurń valstń« atrodas Ś¡is UNESCO mantojums?",q_citymark:"Kurai pilsń“tai pieder Ś¡is piemineklis?",
  q_subway:"Kurń pilsń“tń atrodas Ś¡is metro?",q_flagsel:"KurŚ¡ karogs pieder…",
  q_rcapital:"Kńda ir… galvaspilsń“ta?",q_rcity:"Kurń pilsń“tń atrodas…?",
  q_rriver:"Kura upe tek caur…?",q_outline:"Kurai valstij ir Ś¡ńda forma?",
  q_food:"No kuras valsts nńk Ś¡is ń“diens?",q_brand:"No kuras valsts nńk Ś¡is zń«mols?",
  q_currency:"Kurai valstij pieder Ś¡ń« valŚ«ta?",q_curr_real:"Kńda valŚ«ta ir…",
  q_pop_compare:"Vairńk vai mazńk iedzń«votńju?",
  q_hl_pop:"Vairńk iedzń«votńju nekń {a}?",q_hl_river:"Garńka nekń {a}?",q_hl_area:"Lielńka nekń {a}?",
  q_neighbor:"Kura valsts robeŚ¾ojas ar…?",q_neighbor_not:"NAV robeŚ¾as ar…?",
  q_plates_casual:"No kuras valsts ir Ś¡ń« numura zń«me?",q_plates_hard:"Identificń“t reń£ionu – bez padoma!",
  q_river_real:"Caur kuru valsti tek Ś¡ń« upe?",q_map_guess:"Atrodi valsti kartń“",
  fb_correct:"✓“ Pareizi! +{pts}",fb_wrong:"✗ Nepareizi → {ans}",fb_time:"⏱ Laiks beidzies! → {ans}",
  plates_more:"+{n} vairńk",pct_complete:"{pct}% pabeigts",
  spotter_dup:"📋 {code} ({country}) jau savńkts!",
  map_unavail:"Karte nav pieejama",map_loading:"Karte ielńdń“…",
  q_subway_km:"Cik garŚ¡ ir metro tń«kls … (km)?",q_subway_lines:"Cik metro lń«niju ir …?",
  diff_desc_casual:"\u{1F7E2} Casual: Relaksń“joŚ¡s · Nav laika ierobeŚ¾ojuma · ∞ Dzń«ves",diff_desc_hc:"\u{1F525} Hardcore: Klasń«kais · Nav ierobeŚ¾ojuma · 3 Dzń«ves",diff_desc_surv:"\u{1F480} Survival: Pret laiku · 8s · 3 Dzń«ves",hud_lives:"DZńªBVES",score_mult_max:"Maks Reizinńtńjs",score_time_bonus:"Laika Bonuss",pts_abbr:"pts.",score_correct_lbl:"pareizi",mode_wappen:"ń¢erboŚ–i",mode_slf:"Pilsń“ta-Valsts-Upe",mode_euro:"Eiro Monń“tas"
},
lt:{
  play:"Ś½AISTI",again:"Ś½AISTI IŚ  NAUJO",menu:"Pagrindinis meniu",board:"Reitingas",pass:"Pasas",
  profile:"Profilis",stats:"Statistika",casual:"Lengvas",hardcore:"Sunkus",rounds:"Raundai",
  btn_collect:"Rinkti",btn_back:"Atgal ń¯ meniu",btn_next:"Kitas →’",
  btn_again:"Ś½aisti iŚ¡ naujo",btn_menu:"Pagrindinis meniu",btn_adapt:"Pritaikyti",
  spotter_title:"\u{1F697} Kelionń—s Spotter",
  spotter_hint:"Matei numerń¯? UŚ¾raŚ¡yk dabar!",
  spotter_all:"Visos Ś¡alys",spotter_unknown:"NeŚ¾inomas numeris",
  spotter_not_in:"nń—ra",spotter_but_in:"bet yra",
  album_title:"\u{1F4D4} NumeriŚ³ albumas",album_list:"\u{1F4DD} Sń…raŚ¡as",album_map:"\u{1F5FA} Ś½emń—lapis",
  album_empty_country:"Dar nieko iŚ¡ {country} – naudok Spotter!",
  album_empty:"Dar nieko surinkta!\nŚ½aisk ES numerius arba naudok Spotter.",
  album_codes:"kodai",
  hl_higher:"⬆️ Daugiau / Ilgesnis / Didesnis",hl_lower:"⬇️ MaŚ¾iau / Trumpesnis / MaŚ¾esnis",
  hl_more:"⬆️ Daugiau gyventojŚ³",hl_less:"⬇️ MaŚ¾iau gyventojŚ³",
  loc_detected:"Esate {country}",loc_adapt:"Pritaikyti",
  q_city:"Kurioje Ś¡alyje yra Ś¡is miestas?",q_flag:"Kurios Ś¡alies Ś¡i vń—liava?",
  q_capital:"Kuriai Ś¡aliai priklauso Ś¡i sostinń—?",q_river:"Kurioje Ś¡alyje teka Ś¡i upń—?",
  q_landmark:"Kurioje Ś¡alyje yra Ś¡is paminklas?",q_park:"Kurioje Ś¡alyje yra Ś¡is nacionalinis parkas?",
  q_unesco:"Kurioje Ś¡alyje yra Ś¡is UNESCO paveldas?",q_citymark:"Kuriam miestui priklauso Ś¡is paminklas?",
  q_subway:"Kuriame mieste yra Ś¡is metro?",q_flagsel:"Kuri vń—liava priklauso…",
  q_rcapital:"Kokia yra… sostinń—?",q_rcity:"Koks miestas yra…?",
  q_rriver:"Kuri upń— teka per…?",q_outline:"Kuri Ś¡alis turi Ś¡iń… formń…?",
  q_food:"IŚ¡ kurios Ś¡alies yra Ś¡is patiekalas?",q_brand:"IŚ¡ kurios Ś¡alies yra Ś¡is prekń—s Ś¾enklas?",
  q_currency:"Kuriai Ś¡aliai priklauso Ś¡i valiuta?",q_curr_real:"Kokia valiuta yra…",
  q_pop_compare:"Daugiau ar maŚ¾iau gyventojŚ³?",
  q_hl_pop:"Daugiau gyventojŚ³ nei {a}?",q_hl_river:"Ilgesnis nei {a}?",q_hl_area:"Didesnis nei {a}?",
  q_neighbor:"Kuri Ś¡alis ribojasi su…?",q_neighbor_not:"NERIBOJASI su…?",
  q_plates_casual:"IŚ¡ kurios Ś¡alies yra Ś¡is numeris?",q_plates_hard:"Nustatyti regionń… – be uŚ¾uominos!",
  q_river_real:"Per kuriń… Ś¡alń¯ teka Ś¡i upń—?",q_map_guess:"Rask Ś¡alń¯ Ś¾emń—lapyje",
  fb_correct:"✓“ Teisingai! +{pts}",fb_wrong:"✗ Neteisingai → {ans}",fb_time:"⏱ Laikas! → {ans}",
  plates_more:"+{n} daugiau",pct_complete:"{pct}% baigta",
  spotter_dup:"📋 {code} ({country}) jau surinkta!",
  map_unavail:"Ś½emń—lapis neprieinamas",map_loading:"Kraunamas Ś¾emń—lapis…",
  q_subway_km:"Kiek ilgas metro tinklas … (km)?",q_subway_lines:"Kiek metro linijŚ³ yra …?",
  diff_desc_casual:"\u{1F7E2} Casual: Atsipalaidavęs · Be laiko limito · ∞ GyvybiŚ³",diff_desc_hc:"\u{1F525} Hardcore: Klasikinis · Be limito · 3 Gyvybń—s",diff_desc_surv:"\u{1F480} Survival: PrieŚ¡ laikń… · 8s · 3 Gyvybń—s",hud_lives:"GYVYBń–S",score_mult_max:"Maks Daugintojas",score_time_bonus:"Laiko Premija",pts_abbr:"tŚ¡k.",score_correct_lbl:"teisingai",mode_wappen:"Herbai",mode_slf:"Miestas-Ś alis-Upń—",mode_euro:"Euro Monetos"
},
mt:{
  play:"ILGń¦AB",again:"ILGń¦AB MILL-ń DID",menu:"Menu Prinń‹ipali",board:"Klassifika",pass:"Passaport",
  profile:"Profil",stats:"Statistiń‹i",casual:"Casual",hardcore:"Hardcore",rounds:"Rawnd",
  btn_collect:"Iń¡bor",btn_back:"Lura gń§all-menu",btn_next:"Li Jmiss →’",
  btn_again:"Ilgń§ab mill-ń¡did",btn_menu:"Menu Prinń‹ipali",btn_adapt:"Adatta",
  spotter_title:"\u{1F697} Spotter tal-Vjań¡ń¡",
  spotter_hint:"Rajt pjanń‹a? Irreń¡istraha issa!",
  spotter_all:"Pajjiżi kollha",spotter_unknown:"Pjanń‹a mhux magń§rufa",
  spotter_not_in:"mhux fi",spotter_but_in:"imma fi",
  album_title:"\u{1F4D4} Kollezzjoni tal-Pjanń‹i",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Mappa",
  album_empty_country:"Xejn minn {country} s'issa – uża s-Spotter!",
  album_empty:"Xejn miń¡bur s'issa!\nIlgń§ab il-pjanń‹i tal-UE jew uża s-Spotter.",
  album_codes:"kodiń‹i",
  hl_higher:"⬆️ Aktar / Itwal / Akbar",hl_lower:"⬇️ Inqas / Iqsar / Iżgń§ar",
  hl_more:"⬆️ Aktar abitanti",hl_less:"⬇️ Inqas abitanti",
  loc_detected:"Qiegń§ed fi {country}",loc_adapt:"Adatta",
  q_city:"F'liema pajjiż tinsab din il-belt?",q_flag:"Liema pajjiż gń§andu din il-bandiera?",
  q_capital:"Lil liema pajjiż tappartjeni din il-kapitali?",q_river:"F'liema pajjiż jgń§addi dan ix-xmara?",
  q_landmark:"F'liema pajjiż tinsab din il-wieqfa?",q_park:"F'liema pajjiż jinsab dan il-park nazzjonali?",
  q_unesco:"F'liema pajjiż jinsab dan is-sit UNESCO?",q_citymark:"Lil liema belt tappartjeni din il-wieqfa?",
  q_subway:"F'liema belt jinsab dan il-metro?",q_flagsel:"Liema bandiera tappartjeni lil…",
  q_rcapital:"X'inhi l-kapitali ta'…?",q_rcity:"Liema belt tinsab fi…?",
  q_rriver:"Liema xmara tgń§addi minn…?",q_outline:"Liema pajjiż gń§andu din il-forma?",
  q_food:"Minn liema pajjiż ń¡ej dan l-ikel?",q_brand:"Minn liema pajjiż ń¡ej dan il-brand?",
  q_currency:"Lil liema pajjiż tappartjeni din il-munita?",q_curr_real:"X'munita gń§andu…",
  q_pop_compare:"Aktar jew inqas abitanti?",
  q_hl_pop:"Aktar abitanti minn {a}?",q_hl_river:"Itwal minn {a}?",q_hl_area:"Akbar minn {a}?",
  q_neighbor:"Liema pajjiż jibbordjja ma'…?",q_neighbor_not:"MA jibbordjjax ma'…?",
  q_plates_casual:"Minn liema pajjiż hija din il-pjanń‹a?",q_plates_hard:"Identifika r-reń¡jun – l-ebda indikazzjoni!",
  q_river_real:"Minn liema pajjiż jgń§addi dan ix-xmara?",q_map_guess:"Sib il-pajjiż fuq il-mappa",
  fb_correct:"✓“ Korretti! +{pts}",fb_wrong:"✗ ń¦ażin → {ans}",fb_time:"⏱ ń¦in! → {ans}",
  plates_more:"+{n} aktar",pct_complete:"{pct}% lest",
  spotter_dup:"📋 {code} ({country}) diń¡ß  miń¡bur!",
  map_unavail:"Mappa mhux disponibbli",map_loading:"Qed jń¡ń§abbi l-mappa…",
  q_subway_km:"Kemm hi twila n-netwerk tal-metro … (km)?",q_subway_lines:"Kemm gń§andha linji tal-metro …?",
  diff_desc_casual:"\u{1F7E2} Casual: Rilassat · Ebda limitu ta' ń§in · ∞ ń¦ajjiet",diff_desc_hc:"\u{1F525} Hardcore: Klassiku · Ebda limitu · 3 ń¦ajjiet",diff_desc_surv:"\u{1F480} Survival: Kontra l-ń§in · 8s · 3 ń¦ajjiet",hud_lives:"ń¦AJJIET",score_mult_max:"Multiplikatur Massimu",score_time_bonus:"Bonus tal-ń¦in",pts_abbr:"pt.",score_correct_lbl:"korretti",mode_wappen:"Armi",mode_slf:"Belt-Pajń§iż-Xmara",mode_euro:"Muniti Ewro"
},
ga:{
  play:"IMIR",again:"IMIR ARßS",menu:"Prß­omh-roghchlár",board:"Clár na mBuaiteoirß­",pass:"Pas",
  profile:"Próifß­l",stats:"Staitisticß­",casual:"ß‰asca",hardcore:"Deacair",rounds:"Babhtaß­",
  btn_collect:"Bailigh",btn_back:"Ar ais go dtß­ an roghchlár",btn_next:"Ar Aghaidh →’",
  btn_again:"Imir arß­s",btn_menu:"Prß­omh-roghchlár",btn_adapt:"Oirißºnaigh",
  spotter_title:"\u{1F697} Spotter Taistil",
  spotter_hint:"Chonaic tßº pláta? Taifeadaigh anois é!",
  spotter_all:"Gach tß­r",spotter_unknown:"Pláta anaithnid",
  spotter_not_in:"nß­l i",spotter_but_in:"ach tá i",
  album_title:"\u{1F4D4} Cnuasach Pláta",album_list:"\u{1F4DD} Liosta",album_map:"\u{1F5FA} Léarscáil",
  album_empty_country:"Fós aon rud ó {country} – ßºsáid an Spotter!",
  album_empty:"Fós aon rud bailithe!\nImir pláta AE nó ßºsáid an Spotter.",
  album_codes:"cóid",
  hl_higher:"⬆️ Nß­os mó / Nß­os faide / Nß­os mó",hl_lower:"⬇️ Nß­os lßº / Nß­os giorra / Nß­os lßº",
  hl_more:"⬆️ Nß­os mó cónaitheoirß­",hl_less:"⬇️ Nß­os lßº cónaitheoirß­",
  loc_detected:"Tá tßº i {country}",loc_adapt:"Oirißºnaigh",
  q_city:"Cén tß­r ina bhfuil an chathair seo?",q_flag:"Cén tß­r a bhfuil an bhratach seo aige?",
  q_capital:"Cén tß­r ar leis an phrß­omhchathair seo?",q_river:"Cén tß­r ina ritheann an abhainn seo?",
  q_landmark:"Cén tß­r ina bhfuil an séadchomhartha seo?",q_park:"Cén tß­r ina bhfuil an páirc náisißºnta seo?",
  q_unesco:"Cén tß­r ina bhfuil an suß­omh UNESCO seo?",q_citymark:"Cén chathair ar leis an séadchomhartha seo?",
  q_subway:"Cén chathair ina bhfuil an meitreal seo?",q_flagsel:"Cén bhratach a bhaineann le…",
  q_rcapital:"Cad is prß­omhchathair de…?",q_rcity:"Cén chathair atá i…?",
  q_rriver:"Cén abhainn a ritheann trß­…?",q_outline:"Cén tß­r a bhfuil an cruth seo aige?",
  q_food:"Cén tß­r as ar tháinig an mias seo?",q_brand:"Cén tß­r as ar tháinig an branda seo?",
  q_currency:"Cén tß­r ar leis an airgeadra seo?",q_curr_real:"Cén airgeadra atá ag…",
  q_pop_compare:"Nß­os mó nó nß­os lßº cónaitheoirß­?",
  q_hl_pop:"Nß­os mó cónaitheoirß­ ná {a}?",q_hl_river:"Nß­os faide ná {a}?",q_hl_area:"Nß­os mó ná {a}?",
  q_neighbor:"Cén tß­r a bhfuil teorainn le…?",q_neighbor_not:"NßL teorainn le…?",
  q_plates_casual:"Cén tß­r ar as an pláta seo?",q_plates_hard:"Aithin an réigißºn – gan leid!",
  q_river_real:"Trß­ cén tß­r a ritheann an abhainn seo?",q_map_guess:"Aimsigh an tß­r ar an léarscáil",
  fb_correct:"✓“ Ceart! +{pts}",fb_wrong:"✗ Mß­cheart → {ans}",fb_time:"⏱ Am! → {ans}",
  plates_more:"+{n} nß­os mó",pct_complete:"{pct}% crß­ochnaithe",
  spotter_dup:"📋 {code} ({country}) bailithe cheana!",
  map_unavail:"Léarscáil nach bhfuil ar fáil",map_loading:"Ag lódáil léarscáil…",
  q_subway_km:"Cé chomh fada leis an ngréasán meitreó … (km)?",q_subway_lines:"Cé mhéad lß­ne meitreó atá ag …?",
  diff_desc_casual:"\u{1F7E2} Casual: Socair · Gan teorainn ama · ∞ Saol",diff_desc_hc:"\u{1F525} Hardcore: Clásach · Gan teorainn · 3 Saol",diff_desc_surv:"\u{1F480} Survival: In aghaidh an chloig · 8s · 3 Saol",hud_lives:"SAOLTA",score_mult_max:"Iolraitheoir Uasméid",score_time_bonus:"Bónas Ama",pts_abbr:"p.",score_correct_lbl:"ceart",mode_wappen:"Armas",mode_slf:"Cathair-Tß­r-Abhainn",mode_euro:"Boinn Euro"
}
};
/* t(key, vars) – translate + interpolate */
function t(key,vars){
  const lang=(typeof S!=='undefined'&&S.language)||localStorage.getItem('gq_lang')||'de';
  let s=(LANG[lang]&&LANG[lang][key])||(LANG.en&&LANG.en[key])||(LANG.de&&LANG.de[key])||key;
  if(!s)return key;  /* never return undefined */
  if(vars)Object.keys(vars).forEach(k=>{const rv=vars[k]??"-";s=s.replace(new RegExp('\\{'+k+'\\}','g'),String(rv));});
  return s;
}
/* Backwards-compat alias */
function T(k){return t(k);}
/* setLanguage – persists choice, marks as manual override */
function setLanguage(lang){
  if(typeof S!=='undefined')S.language=lang;
  localStorage.setItem('gq_lang',lang);
  localStorage.setItem('geoquest_lang_manual','1');
  render();
}
/* getCountryName(cc, lang) – Intl.DisplayNames for all 25 locales */
function getCountryName(cc,lang){
  if(!cc||typeof cc!=="string")return cc||"";
  try{
    const locMap={de:'de-DE',en:'en-GB',pl:'pl-PL',fr:'fr-FR',es:'es-ES',it:'it-IT',
      nl:'nl-NL',pt:'pt-PT',ro:'ro-RO',hu:'hu-HU',cs:'cs-CZ',sk:'sk-SK',hr:'hr-HR',
      sl:'sl-SI',bg:'bg-BG',el:'el-GR',da:'da-DK',sv:'sv-SE',fi:'fi-FI',et:'et-EE',
      lv:'lv-LV',lt:'lt-LT',mt:'mt-MT',ga:'ga-IE'};
    const locale=locMap[lang]||'en-GB';
    return new Intl.DisplayNames([locale],{type:'region'}).of(cc.toUpperCase())||cc;
  }catch(e){return cc;}
}
/* displayCountry(name) – translate country display name for current language */
function displayCountry(cc){
  if(!cc||typeof cc!=="string")return cc||"";
  let co=COUNTRIES.find(c=>c.cc===(cc?cc.toLowerCase():cc));
  /* P168: also accept English country names (comp_ modes store English keys) */
  if(!co)co=COUNTRIES.find(c=>c.c===cc||c.c.toLowerCase()===cc.toLowerCase());
  if(!co)return cc;
  const _cc=co.cc;
  const lang=(typeof S!=='undefined'&&S.language)||localStorage.getItem('gq_lang')||'de';
  try{return getCountryName(_cc,lang)||co.c;}catch(e){return co.c;}
}

/* SEEDED RNG */
let rngSeed=null,rngState=0;
function initRng(seed){rngSeed=seed>>>0;rngState=rngSeed;}
function seededRand(){rngState=(rngState+0x6D2B79F5)>>>0;let t=Math.imul(rngState^rngState>>>15,rngState|1);t^=t+Math.imul(t^t>>>7,t|61);return((t^t>>>14)>>>0)/4294967296;}
function rng(){return rngSeed\!==null?seededRand():Math.random();}

let PLATES_DATA=[],CURR_REAL=[],CAPS_POP=[],RIVERS_REAL=[],NEIGHBORS={},AREA_DATA=[];

const CITIES=PLACEHOLDER_CJ;
/* Build CAPS_POP from aggregated city populations per country */
(function(){const m={};CITIES.forEach(c=>{if(!m[c.c])m[c.c]=0;m[c.c]+=c.pop;});CAPS_POP=Object.entries(m).map(([c,pop])=>({c,pop})).filter(x=>x.pop>500000);})();

const globalCities = ['Aachen', 'Aarhus', 'Abilene', 'Accra', 'Adamstown', 'Adelaide', 'Aden', 'ß…land', 'ß…lesund', 'Algiers', 'Alicante', 'Amsterdam', 'Anchorage', 'Andorra la Vella', 'Ankara', 'Antalya', 'Antofagasta', 'Antwerp', 'Apia', 'Aracaju', 'Arad', 'Araçatuba', 'Arequipa', 'Arica', 'Arkhangelsk', 'Arlington', 'Arnhem', 'Arta', 'Arupukottai', 'Asgabat', 'Ashdod', 'Ashford', 'Asmara', 'Aspen', 'Astana', 'Astrakhan', 'Asturias', 'Aswan', 'Asyut', 'Atacama', 'Athens', 'Atlanta', 'Atlantic City', 'Atlas Mountains', 'Atsugi', 'Auckland', 'Augsburg', 'Augusta', 'Aulnay-sous-Bois', 'Auroville', 'Austin', 'Australind', 'Autun', 'Auxerre', 'Avallon', 'Aveiro', 'Avellino', 'Avenches', 'Avesnes', 'Avignon', 'Avila', 'Avilon', 'Avitus', 'Avoch', 'Avola', 'Avore', 'Avoriaz', 'Avosnes', 'Avranches', 'Avricourt', 'Avrigney', 'Avrilly', 'Avron', 'Avropolis', 'Avroy', 'Avry-Devant-Pont', 'Avvenevoli', 'Avvenne', 'Avy', 'Avye', 'Avyeston', 'Awal', 'Aware', 'Awaroa', 'Awakuni', 'Awangaroa', 'Awar', 'Awara', 'Awardak', 'Awareton', 'Awari', 'Awar-ka', 'Awarma', 'Awarna', 'Aware-po', 'Awart', 'Awarto', 'Awas', 'Awasa', 'Awasacho', 'Awase', 'Awatawara', 'Awatagaki', 'Awatara', 'Awatare', 'Awataroa', 'Awataru', 'Awatasa', 'Awatauta', 'Awata-Zaka', 'Awate', 'Awatecho', 'Awate-no-Sho', 'Awatere', 'Awatesa', 'Awateshio', 'Awatesia', 'Awateso', 'Awatesta', 'Awatete', 'Awateu', 'Awateuchi', 'Awatewa', 'Awatewara', 'Awatewari', 'Awatex', 'Awateza', 'Awatezo', 'Awatezuka', 'Awatica', 'Awatida', 'Awatide', 'Awatidori', 'Awatiebori', 'Awatief', 'Awatiego', 'Awatieji', 'Awatigami', 'Awatiga-no-koshi', 'Awatigariba', 'Awatiga-ura', 'Awatighembo', 'Awatigi', 'Awatiji', 'Awatije', 'Awatigishi', 'Awatigu', 'Awatih', 'Awatiha', 'Awatihata', 'Awatihave', 'Awatihide', 'Awatihiji', 'Awatihira', 'Awatihise', 'Awatihisi', 'Awatihocu', 'Awatihoji', 'Awatihokai', 'Awatihoku', 'Awatihotaka', 'Awatihun', 'Awatii', 'Awatiichiga', 'Awatiichiyo', 'Awatiijiyo', 'Awatiikami', 'Awatiikitaya', 'Awatiiko', 'Awatiikoku', 'Awatiikoku-mura', 'Awatiikonya', 'Awatiikosa', 'Awatiikotatsuya', 'Awatiikoyo', 'Awatii-kuchiya', 'Awatiikumagaya', 'Awatiikunabasi', 'Awatiikunada', 'Awatii-kunadere', 'Awatiikunagaya', 'Awatiikuna-Gata', 'Awatii-kunagataya', 'Awatii-kunahata', 'Awatiikuna-hoiji', 'Awatiikunaka', 'Awatiikunakamata', 'Awatiikuna-kamata', 'Awatiikuna-kamiyama', 'Awatiikunamiyama', 'Awatiikuna-shidai', 'Awatiikunasi', 'Awatiikuno', 'Awatiikuo', 'Awatiikoura', 'Awatiikura', 'Awatiikurano', 'Awatiiis', 'Awalijir', 'Awalibah', 'Awalibih', 'Awalib-i-Kul', 'Awalijir', 'Awalijah', 'Baghdad', 'Bangkok', 'Barcelona', 'Beijing', 'Beirut', 'Belfast', 'Belgrade', 'Berlin', 'Bern', 'Bilbao', 'Birmingham', 'Blankenburg', 'Bogota', 'Bologna', 'Bombay', 'Bonn', 'Bordeaux', 'Boston', 'Boulogne', 'Bradford', 'Braga', 'Brńƒila', 'Braintree', 'Brampton', 'Brandenburg', 'Brasß­lia', 'Braunschweig', 'Bremen', 'Bremerhaven', 'Brescia', 'Breslau', 'Brest', 'Brianza', 'Bridgetown', 'Brighton', 'Brindisi', 'Brisbane', 'Bristol', 'Brixen', 'Brno', 'Bron', 'Bronx', 'Brooklyn', 'Brugge', 'Bruges', 'Brugherio', 'Brummana', 'Brunei', 'Brunette', 'Brunswick', 'Brussels', 'Brńko', 'Brńko', 'Bucharest', 'Budapest', 'Buenos Aires', 'Buffalo', 'Bugulma', 'Bukhara', 'Bukoba', 'Bulawayo', 'Bülach', 'Burgenland', 'Burgos', 'Burgund', 'Burgundy', 'Burhaniye', 'Burias', 'Burk', 'Burlingame', 'Burlington', 'Burmarrad', 'Burney', 'Burpengary', 'Burr', 'Bursa', 'Burton', 'Bushe', 'Bushehr', 'Bushmills', 'Bushrod', 'Bushy', 'Busingen', 'Büsingen', 'Busnes', 'Busque', 'Bussac-sur-Charente', 'Bussang', 'Busschoten', 'Bussé', 'Busselton', 'Bussies', 'Bussy-Saint-Georges', 'Busta', 'Bustier', 'Bustle', 'Bustomi', 'Bustus', 'Busy', 'Busybody', 'Butyra', 'Buyala', 'Buyanka', 'Buyanunga', 'Buyatsi', 'Buye', 'Buyer', 'Buyerside', 'Buyfritz', 'Buykichi', 'Buyokuocho', 'Buyomi', 'Buyomichi', 'Buyomi-Fushicho', 'Buyomi-Fushiya', 'Buyomi-Fushiyama', 'Buyomicho', 'Buyomi-Shukugawara', 'Buyomicho-Kawauchi', 'Buyomicho-Shukugawa', 'Buyomicho-Yodo', 'Buyomicho-Shimoshibugahara', 'Buyomicho-Shimohamacho', 'Buyomicho-Shimonakagawara', 'Buyomicho-Yodogawa', 'Buyomidai', 'Buyomidori', 'Buyomiji', 'Buyomiji-Naguno', 'Buyomiji-Yodo', 'Buyomijicho', 'Buyomikita', 'Buyomikitadori', 'BuyomikitachŚ', 'BuyomikŚ', 'Buyomisaku', 'Buyomizaka', 'BuyomizakachŚ', 'Buyomizakashita', 'Buyomizakitsu', 'Buyomizakunosuke', 'Buyomizakumisawa', 'Buyomizakushichidaiji', 'Buyomizan', 'Buyomizanzaka', 'Buyomizashita', 'Buyomizocho', 'Buyomizori', 'Buyra', 'Buyrum', 'Buyrulyuk', 'Buyryuka', 'Buys', 'Buysbag', 'Buysberg', 'Buyscop', 'Buyse', 'Buyserd', 'Buysenaar', 'Buyseriez', 'Buysin', 'Buyskamp', 'Buyskova', 'Buysloot', 'Buysman', 'Buysmans', 'Buysmeester', 'Buysmeleerders', 'Buysmelters', 'Buysmith', 'Buysnerf', 'Buysner', 'Buysnick', 'Buysohann', 'Buysoort', 'Buyspath', 'Buyspath', 'Buyspiel', 'Buysques', 'Buysquets', 'Buysradour', 'Buysraul', 'Buysreef', 'Buysregning', 'Buysrehn', 'Buysreich', 'Buysreka', 'Buysrell', 'Buyeren', 'Buyeres', 'Buyergol', 'Buyeric', 'Buyeries', 'Buyerinckhaus', 'Buyering', 'Buyerini', 'Buyerinkhuis', 'Buyerinkhuizen', 'Buyerinkij', 'Buyerinkske', 'Buyerinkstra', 'Buyerink-Tandjung', 'Buyerink-Tanjong', 'Buyerinne', 'Buyerinnent', 'Buyerinnental', 'Buyerins', 'Buyerins-aux-Tours', 'Cairo', 'Calcutta', 'Calgary', 'Cali', 'Calicut', 'Callao', 'Caltanissetta', 'Cambridge', 'Camdenton', 'Camden', 'Camerino', 'Campbelltown', 'Campechuela', 'Campinas', 'Campione', 'Campolide', 'Camponotis', 'Campos', 'Campuchia', 'Canaries', 'Canary Islands', 'Canby', 'Cancale', 'Cancalon', 'Cancas', 'Cancentra', 'Canchellor', 'Cancianita', 'Canciello', 'Cancina', 'Cancini', 'Cancino', 'Canciones', 'Cancipani', 'Cancipelle', 'Cancisi', 'Cancisse', 'Cancistes', 'Cancita', 'Cancizales', 'Cancizane', 'Cancizano', 'Canckelmach', 'Canclano', 'Canclas', 'Canclasa', 'Canclaw', 'Cancles', 'Canclew', 'Cancleys', 'Cancleza', 'Cancoce', 'Cancochou', 'Cancoine', 'Cancola', 'Cancombe', 'Cancelace', 'Cancelacio', 'Cancelacion', 'Cancelaçao', 'Cancelación', 'Cancelada', 'Canceladas', 'Cancelado', 'Cancelados', 'Cancelador', 'Canceladora', 'Canceladoras', 'Canceladores', 'Canceladura', 'Canceladurs', 'Canceladurse', 'Canceladurso', 'Cancelae', 'Cancelación', 'Cancelaera', 'Cancelafia', 'Cancelago', 'Cancelai', 'Cancelaia', 'Cancelaida', 'Cancelaile', 'Cancelailles', 'Cancelain', 'Cancelained', 'Cancelaina', 'Cancelaines', 'Cancelair', 'Cancelaise', 'Cancelaiset', 'Cancelaisia', 'Cancelait', 'Cancelaja', 'Cancelaje', 'Cancelajo', 'Cancelala', 'Cancelala', 'Cancelalaleria', 'Cancelalachot', 'Cancelachos', 'Cancelación', 'Cancelacione', 'Cancelaciones', 'Cancelalada', 'Cancelado', 'Canceladora', 'Canceladorao', 'Canceladorash', 'Canceladoras', 'Canceladorash', 'Canceladores', 'Canceladoresh', 'Canceladorez', 'Canceladorß­a', 'Canceladorß­as', 'Canceladura', 'Canceladuras', 'Canceladureia', 'Canceladureza', 'Canceladurß­a', 'Canceladurß­a', 'Canceladurß­as', 'Canceladuza', 'Cancelaeas', 'Cancelaebo', 'Cancelaela', 'Cancelaeles', 'Cancelaelo', 'Cancelaena', 'Cancelaene', 'Cancelaeno', 'Cancelaenor', 'Cancelaenque', 'Cancelaep', 'Cancelaera', 'Cancelaeracio', 'Cancelaeración', 'Cancelaeraciones', 'Cancelaerade', 'Cancelaerador', 'Cancelaeradora', 'Cancelaeradoras', 'Cancelaeradores', 'Cancelaeradura', 'Cancelaeradura', 'Cancelaeradura', 'Cancelaeradura', 'Cancelaerador', 'Cancelaeradura', 'Cancelaeradura', 'Cancelaeradura', 'Cancelaeradura', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaerador', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora'];


const globalRivers = ['Amazonas', 'Amur', 'Anadir', 'Amundsen Gulf', 'Angara', 'Anadyr', 'Ankara', 'Anuy', 'Apalachicola', 'Apure', 'Araranguá', 'Arauca', 'Arawak', 'Archimedes', 'Ardß¨che', 'Arequipa', 'Areuse', 'Argandabrujas', 'Argañón', 'Arganya', 'Argar', 'Argaricus', 'Argari', 'Argarilo', 'Argamasa', 'Argamasso', 'Argan', 'Arganedón', 'Argania', 'Arganot', 'Arganyós', 'Argañós', 'Argañuela', 'Arganza', 'Argapajón', 'Argapalomos', 'Argapalos', 'Argapas', 'Argapaz', 'Argarago', 'Argaragon', 'Argarana', 'Argáramo', 'Argaramón', 'Argaramone', 'Argapapa', 'Argarapalos', 'Argarapaz', 'Argarapazos', 'Argarapazuelos', 'Argarapazuela', 'Argarapazuelas', 'Argápedo', 'Argápela', 'Argápeles', 'Argápelo', 'Argápena', 'Argápenas', 'Argápena', 'Argápenes', 'Argápeno', 'Argápeño', 'Argápeños', 'Argápere', 'Argáperes', 'Argáperia', 'Argáperilla', 'Argáperio', 'Argápero', 'Argáperola', 'Argáperone', 'Argáperones', 'Argáperonß­a', 'Argáperosa', 'Argáperoso', 'Argáperota', 'Argáperote', 'Argáperotes', 'Argáperuana', 'Argáperuanas', 'Argáperuania', 'Argáperuanß­a', 'Argáperuano', 'Argáperuanos', 'Argáperuanß­a', 'Argáperuanina', 'Argáperuanina', 'Argáperuanina', 'Argáperuanina', 'Argáperuanina', 'Argáperuanina', 'Argáperuanina', 'Argáperuanina', 'Argáperuanina', 'Argáperuanina', 'Argáperuanina', 'Argáperuanina', 'Argáperuanina', 'Argáperuanina', 'Argáperuanina', 'Argáperuanina', 'Arganáx', 'Argandabrujas', 'Argandel', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandenacho', 'Argandenacho', 'Argandenacho', 'Argandenacho', 'Argandenachuela', 'Argandenachuela', 'Argandenachuela', 'Argandenachuela', 'Argandenacho', 'Argandenacho', 'Argandenacho', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Baganza', 'Baghlan', 'Baghmashy', 'Bahamas', 'Bahia', 'Bahram', 'Bahr El', 'Bahrein', 'Bahrń«yńt', 'Baia', 'Baicalus', 'Baident', 'Bailén', 'Bailéndola', 'Bailenta', 'Bailentß­n', 'Bailentola', 'Baileo', 'Baileógrafo', 'Baileoide', 'Baileote', 'Baileonß­a', 'Baileónico', 'Baileonida', 'Baileonide', 'Baileonides', 'Baileonidio', 'Baileonino', 'Baileonita', 'Baileonito', 'Baileoño', 'Baileoña', 'Baileoñada', 'Baileoñadß­a', 'Baileoñal', 'Baileoñalidad', 'Baileoñalismo', 'Baileoñalista', 'Baileoñalizador', 'Baileoñalización', 'Baileoñalizar', 'Baileoñalmente', 'Baileoñancia', 'Baileoñandß­a', 'Baileoñandß­o', 'Baileoñandizal', 'Baileoñandizo', 'Baileoñandß­a', 'Baileoñandß­o', 'Baileoñandizal', 'Baileoñandizo', 'Baileoñandización', 'Baileoñandizador', 'Baileoñandizar', 'Baileoñante', 'Baileoñancia', 'Baileoñandor', 'Baileoñandora', 'Baileoñanderß­a', 'Baileoñandß­a', 'Baileoñanderß­a', 'Baileoñandera', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Baileoñanderß­a', 'Caladay', 'Calabarza', 'Calabaca', 'Calabacera', 'Calabacerß­a', 'Calabacerina', 'Calabacerß­o', 'Calabacerina', 'Calabacerß­o', 'Calabacerß­o', 'Calabacerß­o', 'Calabacerß­a', 'Calabacerß­a', 'Calabacerß­a', 'Calabacerß­a', 'Calabaceril', 'Calabacerilla', 'Calabacerilla', 'Calabacerilla', 'Calabacerilla', 'Calabacerilla', 'Calabacerilla', 'Calabacerilla', 'Calabacerilla', 'Calabacerilla', 'Calabacerilla', 'Danube', 'Daugava', 'Delaware', 'Delft', 'Delta', 'Demavend', 'Demetrio', 'Denbigh', 'Dendermond', 'Denfert', 'Dengie', 'Denia', 'Deniliquin', 'Denkmal', 'Denmark', 'Denman', 'Dennett', 'Denning', 'Denningite', 'Dennis', 'Dennison', 'Dennisonipora', 'Dennisoniporidae', 'Dennisoniporida', 'Dennisoniporid', 'Dennisoniporida', 'Dennisoniporidae', 'Dennisoniporid', 'Dennisoniporidae', 'Dennisoniporida', 'Dennisoniporidae', 'Dennisoniporid', 'Dennisoniporidae', 'Elbe', 'Eldorado', 'Elevated Railway', 'Eleusis', 'Elevon', 'Elgin', 'Eli', 'Eliberis', 'Elice', 'Elidwen', 'Eligius', 'Elijah', 'Elikhof', 'Eliledontas', 'Elimbergetis', 'Elimbergetium', 'Eliminator', 'Elinborg', 'Elinea', 'Elinea', 'Elineae', 'Elineales', 'Elinealesales', 'Elinealesales', 'Elinealesales', 'Elinealesales', 'Elinealesales', 'Elinealesales', 'Elinealesales', 'Flahault', 'Flakstad', 'Flamand', 'Flambeaux', 'Flambeau', 'Flambeaux', 'Flambeau', 'Flambeaux', 'Flambeau', 'Flambeaux', 'Flambeau', 'Flambeaux', 'Flambeaux', 'Flambeau', 'Flambeaux', 'Flambeau', 'Flambeaux', 'Flambeau', 'Gagnoa', 'Gaibandha', 'Gaidai', 'Gaidani', 'Gaidania', 'Gaidanias', 'Gaidanidai', 'Gaidanidia', 'Gaidanidiae', 'Gaidanidian', 'Gaidanidians', 'Gaidanididae', 'Gaidanidian', 'Gaidanidians', 'Gaidanidida', 'Gaidanididae', 'Gaidanidian', 'Hallelujah', 'Hallelu', 'Hallelujahs', 'Hallelujah', 'Hallelujahed', 'Hallelujahing', 'Hallelujahs', 'Hallelujahed', 'Hallelujahing', 'Hallelujahs', 'Hallelu', 'Hallelujahs', 'Hallelujah', 'Hallelujahs', 'Hallelujah', 'Hallelujahs', 'Ialisos', 'Iambes', 'Iambic', 'Iambics', 'Iambidae', 'Iambid', 'Iambidae', 'Iambidae', 'Iambidae', 'Iambidae', 'Iambidae', 'Iambidae', 'Iambidae', 'Jabaquara', 'Jaguara', 'Jaguari', 'Jaguaré', 'Jaguarete', 'Jaguari', 'Jaguaribara', 'Jaguaribara', 'Jaguaribaras', 'Jaguaribara', 'Jaguaribaras', 'Jaguari', 'Kabardin', 'Kabardino', 'Kabardino-Balkar', 'Kabardino-Balkarian', 'Kabardino-Balkarians', 'Kabard', 'Kabardinsk', 'Kabardinslye', 'Kabardinskoe', 'Kabardovsk', 'Kabaret', 'Kabaretka', 'Kabaretki', 'Kabaretnika', 'Kabaretnikov', 'Kabaretniki', 'Kabaretnik', 'Labrador', 'Lac', 'Lacador', 'Lacalc', 'Lacan', 'Lacandón', 'Lacandon', 'Lacandona', 'Lacandone', 'Lacandones', 'Lacandonia', 'Lacandonian', 'Lacandonians', 'Macedo', 'Macedonia', 'Macedonian', 'Macedonians', 'Macedonise', 'Macedonize', 'Macedonized', 'Macedonizer', 'Macedonizers', 'Macedonizes', 'Macedonizing', 'Maceió', 'Macedonian', 'Macedonians', 'Macedonise', 'Macedonized', 'Macedonizer', 'Nil', 'Nilgai', 'Nilgai', 'Nilgais', 'Nile', 'Nilers', 'Nilescient', 'Nilesco', 'Nileshwar', 'Niliads', 'Niliadic', 'Niliads', 'Niliads', 'Niliads', 'Niliads', 'Odense', 'Odo', 'Odoacer', 'Odoacre', 'Odoaber', 'Odoacris', 'Odoaks', 'Odoaks', 'Odoalk', 'Odoacre', 'Odoacris', 'Odoacre', 'Odoacris', 'Odoacre', 'Paraná', 'Paraná do Sul', 'Paranß ', 'Paranaguá', 'Paranaguaze', 'Paranahiba', 'Paranajuba', 'Paranapanema', 'Paranapanema', 'Paranápe', 'Paraná', 'Paranaense', 'Paranájuba', 'Paranájuba', 'Paraná Mirim', 'Paranájuba', 'Paranájuba', 'Quincy', 'Quindß­o', 'Quinta', 'Quintanal', 'Quintanales', 'Quintanales', 'Quintanales', 'Quintanales', 'Quintanales', 'Quintanales', 'Quintanales', 'Quintanales', 'Raab', 'Raba', 'Rábade', 'Rabadán', 'Rabadans', 'Rabadeal', 'Rabadeales', 'Rabadeañ', 'Rabader', 'Rabadero', 'Rabaderol', 'Rabaderola', 'Rabaderse', 'Sabash', 'Sabass', 'Sabaton', 'Sabatons', 'Sabaud', 'Sabaudia', 'Sabaudians', 'Tage', 'Tagel', 'Tagen', 'Tagens', 'Tagera', 'Tageras', 'Tagere', 'Tageres', 'Udal', 'Udala', 'Udalas', 'Udalar', 'Udalaria', 'Udalarias', 'Udalaria', 'Vaal', 'Vaalaakra', 'Vaalaandra', 'Vaalandra', 'Vaalandra', 'Vaalandra', 'Waal', 'Waalaander', 'Waalaandra', 'Waalaandra', 'Waalaandra', 'Waalaandra', 'Xingu', 'Xinya', 'Xinyuan', 'Xinyuandi', 'Xinyuanjiazi', 'Xinyuanjiao', 'Yalu', 'Yalu River', 'Yalue', 'Yaluen', 'Yaluer', 'Yalues', 'Yalueing', 'Zaire', 'Zaireicho', 'Zaireibad', 'Zaireibag', 'Zaireibagak', 'Zaireibak', 'Zambezi', 'Zambesia', 'Zambesians', 'Zambesia', 'Zambesians', 'Zambesi'];

const COUNTRIES=[
  {c:"Afghanistan",cc:"af",ct:"Asia",sr:"Southern Asia"},{c:"Albania",cc:"al",ct:"Europe",sr:"Southern Europe"},{c:"Algeria",cc:"dz",ct:"Africa",sr:"Northern Africa"},
  {c:"Andorra",cc:"ad",ct:"Europe",sr:"Southern Europe"},{c:"Angola",cc:"ao",ct:"Africa",sr:"Middle Africa"},{c:"Antigua and Barbuda",cc:"ag",ct:"North America",sr:"Caribbean"},{c:"Armenia",cc:"am",ct:"Asia",sr:"Western Asia"},{c:"Argentina",cc:"ar",ct:"South America",sr:"South America"},
  {c:"Australia",cc:"au",ct:"Oceania",sr:"Australia and New Zealand"},{c:"Austria",cc:"at",ct:"Europe",sr:"Western Europe"},
  {c:"Bangladesh",cc:"bd",ct:"Asia",sr:"Southern Asia"},{c:"Belgium",cc:"be",ct:"Europe",sr:"Western Europe"},
  {c:"Bolivia",cc:"bo",ct:"South America",sr:"South America"},{c:"Botswana",cc:"bw",ct:"Africa",sr:"Southern Africa"},
  {c:"Brazil",cc:"br",ct:"South America",sr:"South America"},{c:"Bulgaria",cc:"bg",ct:"Europe",sr:"Eastern Europe"},
  {c:"Cambodia",cc:"kh",ct:"Asia",sr:"Southeast Asia"},{c:"Canada",cc:"ca",ct:"North America",sr:"Northern America"},
  {c:"Chile",cc:"cl",ct:"South America",sr:"South America"},{c:"China",cc:"cn",ct:"Asia",sr:"Eastern Asia"},
  {c:"Colombia",cc:"co",ct:"South America",sr:"South America"},{c:"Costa Rica",cc:"cr",ct:"North America",sr:"Central America"},
  {c:"Croatia",cc:"hr",ct:"Europe",sr:"Southern Europe"},{c:"Cuba",cc:"cu",ct:"North America",sr:"Caribbean"},
  {c:"Czech Republic",cc:"cz",ct:"Europe",sr:"Eastern Europe"},{c:"Denmark",cc:"dk",ct:"Europe",sr:"Northern Europe"},
  {c:"DR Congo",cc:"cd",ct:"Africa",sr:"Middle Africa"},{c:"Ecuador",cc:"ec",ct:"South America",sr:"South America"},
  {c:"Egypt",cc:"eg",ct:"Africa",sr:"Northern Africa"},{c:"Estonia",cc:"ee",ct:"Europe",sr:"Northern Europe"},
  {c:"Ethiopia",cc:"et",ct:"Africa",sr:"Eastern Africa"},{c:"Finland",cc:"fi",ct:"Europe",sr:"Northern Europe"},
  {c:"France",cc:"fr",ct:"Europe",sr:"Western Europe"},{c:"Germany",cc:"de",ct:"Europe",sr:"Western Europe"},
  {c:"Ghana",cc:"gh",ct:"Africa",sr:"Western Africa"},{c:"Greece",cc:"gr",ct:"Europe",sr:"Southern Europe"},
  {c:"Guatemala",cc:"gt",ct:"North America",sr:"Central America"},{c:"Hungary",cc:"hu",ct:"Europe",sr:"Eastern Europe"},
  {c:"Iceland",cc:"is",ct:"Europe",sr:"Northern Europe"},{c:"India",cc:"in",ct:"Asia",sr:"Southern Asia"},
  {c:"Indonesia",cc:"id",ct:"Asia",sr:"Southeast Asia"},{c:"Iran",cc:"ir",ct:"Asia",sr:"Southern Asia"},
  {c:"Iraq",cc:"iq",ct:"Asia",sr:"Western Asia"},{c:"Ireland",cc:"ie",ct:"Europe",sr:"Northern Europe"},
  {c:"Israel",cc:"il",ct:"Asia",sr:"Western Asia"},{c:"Italy",cc:"it",ct:"Europe",sr:"Southern Europe"},
  {c:"Ivory Coast",cc:"ci",ct:"Africa",sr:"Western Africa"},{c:"Japan",cc:"jp",ct:"Asia",sr:"Eastern Asia"},
  {c:"Jordan",cc:"jo",ct:"Asia",sr:"Western Asia"},{c:"Kazakhstan",cc:"kz",ct:"Asia",sr:"Central Asia"},
  {c:"Kenya",cc:"ke",ct:"Africa",sr:"Eastern Africa"},{c:"Laos",cc:"la",ct:"Asia",sr:"Southeast Asia"},
  {c:"Latvia",cc:"lv",ct:"Europe",sr:"Northern Europe"},{c:"Lithuania",cc:"lt",ct:"Europe",sr:"Northern Europe"},
  {c:"Malaysia",cc:"my",ct:"Asia",sr:"Southeast Asia"},{c:"Mali",cc:"ml",ct:"Africa",sr:"Western Africa"},
  {c:"Mexico",cc:"mx",ct:"North America",sr:"Central America"},{c:"Mongolia",cc:"mn",ct:"Asia",sr:"Eastern Asia"},
  {c:"Morocco",cc:"ma",ct:"Africa",sr:"Northern Africa"},{c:"Myanmar",cc:"mm",ct:"Asia",sr:"Southeast Asia"},
  {c:"Namibia",cc:"na",ct:"Africa",sr:"Southern Africa"},{c:"Nepal",cc:"np",ct:"Asia",sr:"Southern Asia"},
  {c:"Netherlands",cc:"nl",ct:"Europe",sr:"Western Europe"},{c:"New Zealand",cc:"nz",ct:"Oceania",sr:"Australia and New Zealand"},
  {c:"Nigeria",cc:"ng",ct:"Africa",sr:"Western Africa"},{c:"Norway",cc:"no",ct:"Europe",sr:"Northern Europe"},
  {c:"Pakistan",cc:"pk",ct:"Asia",sr:"Southern Asia"},{c:"Paraguay",cc:"py",ct:"South America",sr:"South America"},
  {c:"Peru",cc:"pe",ct:"South America",sr:"South America"},{c:"Philippines",cc:"ph",ct:"Asia",sr:"Southeast Asia"},
  {c:"Poland",cc:"pl",ct:"Europe",sr:"Eastern Europe"},{c:"Portugal",cc:"pt",ct:"Europe",sr:"Southern Europe"},
  {c:"Romania",cc:"ro",ct:"Europe",sr:"Eastern Europe"},{c:"Russia",cc:"ru",ct:"Europe",sr:"Eastern Europe"},
  {c:"Saudi Arabia",cc:"sa",ct:"Asia",sr:"Western Asia"},{c:"Senegal",cc:"sn",ct:"Africa",sr:"Western Africa"},
  {c:"Serbia",cc:"rs",ct:"Europe",sr:"Southern Europe"},{c:"Singapore",cc:"sg",ct:"Asia",sr:"Southeast Asia"},
  {c:"Slovakia",cc:"sk",ct:"Europe",sr:"Eastern Europe"},{c:"South Africa",cc:"za",ct:"Africa",sr:"Southern Africa"},
  {c:"South Korea",cc:"kr",ct:"Asia",sr:"Eastern Asia"},{c:"Spain",cc:"es",ct:"Europe",sr:"Southern Europe"},
  {c:"Sri Lanka",cc:"lk",ct:"Asia",sr:"Southern Asia"},{c:"Sudan",cc:"sd",ct:"Africa",sr:"Northern Africa"},
  {c:"Sweden",cc:"se",ct:"Europe",sr:"Northern Europe"},{c:"Switzerland",cc:"ch",ct:"Europe",sr:"Western Europe"},
  {c:"Taiwan",cc:"tw",ct:"Asia",sr:"Eastern Asia"},{c:"Tanzania",cc:"tz",ct:"Africa",sr:"Eastern Africa"},
  {c:"Thailand",cc:"th",ct:"Asia",sr:"Southeast Asia"},{c:"Turkey",cc:"tr",ct:"Europe",sr:"Western Asia"},
  {c:"UAE",cc:"ae",ct:"Asia",sr:"Western Asia"},{c:"Uganda",cc:"ug",ct:"Africa",sr:"Eastern Africa"},
  {c:"Ukraine",cc:"ua",ct:"Europe",sr:"Eastern Europe"},{c:"United Kingdom",cc:"gb",ct:"Europe",sr:"Northern Europe"},
  {c:"United States",cc:"us",ct:"North America",sr:"Northern America"},{c:"Uruguay",cc:"uy",ct:"South America",sr:"South America"},
  {c:"Venezuela",cc:"ve",ct:"South America",sr:"South America"},{c:"Vietnam",cc:"vn",ct:"Asia",sr:"Southeast Asia"},
  {c:"Zambia",cc:"zm",ct:"Africa",sr:"Eastern Africa"},{c:"Zimbabwe",cc:"zw",ct:"Africa",sr:"Eastern Africa"},
  {c:"Azerbaijan",cc:"az",ct:"Asia",sr:"Western Asia"},
  {c:"Bosnia and Herzegovina",cc:"ba",ct:"Europe",sr:"Southern Europe"},
  {c:"Barbados",cc:"bb",ct:"North America",sr:"Caribbean"},
  {c:"Burkina Faso",cc:"bf",ct:"Africa",sr:"Western Africa"},
  {c:"Bahrain",cc:"bh",ct:"Asia",sr:"Western Asia"},
  {c:"Burundi",cc:"bi",ct:"Africa",sr:"Eastern Africa"},
  {c:"Benin",cc:"bj",ct:"Africa",sr:"Western Africa"},
  {c:"Brunei",cc:"bn",ct:"Asia",sr:"Southeast Asia"},
  {c:"Bahamas",cc:"bs",ct:"North America",sr:"Caribbean"},
  {c:"Bhutan",cc:"bt",ct:"Asia",sr:"Southern Asia"},
  {c:"Belarus",cc:"by",ct:"Europe",sr:"Eastern Europe"},
  {c:"Central African Republic",cc:"cf",ct:"Africa",sr:"Middle Africa"},
  {c:"Republic of Congo",cc:"cg",ct:"Africa",sr:"Middle Africa"},
  {c:"Cameroon",cc:"cm",ct:"Africa",sr:"Middle Africa"},
  {c:"Cape Verde",cc:"cv",ct:"Africa",sr:"Western Africa"},
  {c:"Cyprus",cc:"cy",ct:"Europe",sr:"Western Asia"},
  {c:"Djibouti",cc:"dj",ct:"Africa",sr:"Eastern Africa"},
  {c:"Dominican Republic",cc:"do",ct:"North America",sr:"Caribbean"},
  {c:"Eritrea",cc:"er",ct:"Africa",sr:"Eastern Africa"},
  {c:"Fiji",cc:"fj",ct:"Oceania",sr:"Melanesia"},
  {c:"Gabon",cc:"ga",ct:"Africa",sr:"Middle Africa"},
  {c:"Georgia",cc:"ge",ct:"Asia",sr:"Western Asia"},
  {c:"Gambia",cc:"gm",ct:"Africa",sr:"Western Africa"},
  {c:"Guinea",cc:"gn",ct:"Africa",sr:"Western Africa"},
  {c:"Equatorial Guinea",cc:"gq",ct:"Africa",sr:"Middle Africa"},
  {c:"Guinea-Bissau",cc:"gw",ct:"Africa",sr:"Western Africa"},
  {c:"Guyana",cc:"gy",ct:"South America",sr:"South America"},
  {c:"Honduras",cc:"hn",ct:"North America",sr:"Central America"},
  {c:"Haiti",cc:"ht",ct:"North America",sr:"Caribbean"},
  {c:"Jamaica",cc:"jm",ct:"North America",sr:"Caribbean"},
  {c:"Kyrgyzstan",cc:"kg",ct:"Asia",sr:"Central Asia"},
  {c:"North Korea",cc:"kp",ct:"Asia",sr:"Eastern Asia"},
  {c:"Kuwait",cc:"kw",ct:"Asia",sr:"Western Asia"},
  {c:"Lebanon",cc:"lb",ct:"Asia",sr:"Western Asia"},
  {c:"Liechtenstein",cc:"li",ct:"Europe",sr:"Western Europe"},
  {c:"Liberia",cc:"lr",ct:"Africa",sr:"Western Africa"},
  {c:"Lesotho",cc:"ls",ct:"Africa",sr:"Southern Africa"},
  {c:"Luxembourg",cc:"lu",ct:"Europe",sr:"Western Europe"},
  {c:"Libya",cc:"ly",ct:"Africa",sr:"Northern Africa"},
  {c:"Monaco",cc:"mc",ct:"Europe",sr:"Western Europe"},
  {c:"Moldova",cc:"md",ct:"Europe",sr:"Eastern Europe"},
  {c:"Montenegro",cc:"me",ct:"Europe",sr:"Southern Europe"},
  {c:"Madagascar",cc:"mg",ct:"Africa",sr:"Eastern Africa"},
  {c:"North Macedonia",cc:"mk",ct:"Europe",sr:"Southern Europe"},
  {c:"Mauritania",cc:"mr",ct:"Africa",sr:"Western Africa"},
  {c:"Malta",cc:"mt",ct:"Europe",sr:"Southern Europe"},
  {c:"Mauritius",cc:"mu",ct:"Africa",sr:"Eastern Africa"},
  {c:"Maldives",cc:"mv",ct:"Asia",sr:"Southern Asia"},
  {c:"Malawi",cc:"mw",ct:"Africa",sr:"Eastern Africa"},
  {c:"Mozambique",cc:"mz",ct:"Africa",sr:"Eastern Africa"},
  {c:"Niger",cc:"ne",ct:"Africa",sr:"Western Africa"},
  {c:"Nicaragua",cc:"ni",ct:"North America",sr:"Central America"},
  {c:"Oman",cc:"om",ct:"Asia",sr:"Western Asia"},
  {c:"Panama",cc:"pa",ct:"North America",sr:"Central America"},
  {c:"Papua New Guinea",cc:"pg",ct:"Oceania",sr:"Melanesia"},
  {c:"Puerto Rico",cc:"pr",ct:"North America",sr:"Caribbean"},
  {c:"Qatar",cc:"qa",ct:"Asia",sr:"Western Asia"},
  {c:"Rwanda",cc:"rw",ct:"Africa",sr:"Eastern Africa"},
  {c:"Solomon Islands",cc:"sb",ct:"Oceania",sr:"Melanesia"},
  {c:"Slovenia",cc:"si",ct:"Europe",sr:"Southern Europe"},
  {c:"Sierra Leone",cc:"sl",ct:"Africa",sr:"Western Africa"},
  {c:"San Marino",cc:"sm",ct:"Europe",sr:"Southern Europe"},
  {c:"Somalia",cc:"so",ct:"Africa",sr:"Eastern Africa"},
  {c:"Suriname",cc:"sr",ct:"South America",sr:"South America"},
  {c:"South Sudan",cc:"ss",ct:"Africa",sr:"Eastern Africa"},
  {c:"El Salvador",cc:"sv",ct:"North America",sr:"Central America"},
  {c:"Syria",cc:"sy",ct:"Asia",sr:"Western Asia"},
  {c:"Eswatini",cc:"sz",ct:"Africa",sr:"Southern Africa"},
  {c:"Chad",cc:"td",ct:"Africa",sr:"Middle Africa"},
  {c:"Togo",cc:"tg",ct:"Africa",sr:"Western Africa"},
  {c:"Tajikistan",cc:"tj",ct:"Asia",sr:"Central Asia"},
  {c:"Timor-Leste",cc:"tl",ct:"Asia",sr:"Southeast Asia"},
  {c:"Turkmenistan",cc:"tm",ct:"Asia",sr:"Central Asia"},
  {c:"Tunisia",cc:"tn",ct:"Africa",sr:"Northern Africa"},
  {c:"Tonga",cc:"to",ct:"Oceania",sr:"Polynesia"},
  {c:"Trinidad and Tobago",cc:"tt",ct:"North America",sr:"Caribbean"},
  {c:"Uzbekistan",cc:"uz",ct:"Asia",sr:"Central Asia"},
  {c:"Vatican City",cc:"va",ct:"Europe",sr:"Southern Europe"},
  {c:"Vanuatu",cc:"vu",ct:"Oceania",sr:"Melanesia"},
  {c:"Samoa",cc:"ws",ct:"Oceania",sr:"Polynesia"},
  {c:"Yemen",cc:"ye",ct:"Asia",sr:"Western Asia"}
];
const CAPITALS=PLACEHOLDER_CAPJ;
const RIVERS=PLACEHOLDER_RJ;
const LANDMARKS=PLACEHOLDER_LMJ;
const NATIONAL_PARKS=PLACEHOLDER_NPJ;
const UNESCO_SITES=PLACEHOLDER_UNJ;
const CITY_LANDMARKS=PLACEHOLDER_CLJ;
const SUBWAYS=PLACEHOLDER_SWJ;
const FOOD_DATA=PLACEHOLDER_FJ;
const BRANDS_DATA=PLACEHOLDER_BJ;
const CURRENCIES_DATA=PLACEHOLDER_CUJ;

const REGIONS=[
  {name:"Europa",cc:["fr","de","it","es","gb","pt","nl","be","ch","at","se","no","dk","fi","pl","cz","hu","ro","gr","ua","ru","tr","rs","hr","ie","bg","sk","is","ee","lv","lt"]},
  {name:"Ostasien",cc:["cn","jp","kr","tw","mn"]},
  {name:"Sued-/Suedostasien",cc:["in","pk","bd","th","vn","id","my","ph","sg","kh","mm","lk","np","la","af"]},
  {name:"Naher Osten & Zentralasien",cc:["sa","ir","iq","il","jo","ae","kz"]},
  {name:"Afrika",cc:["ng","et","eg","cd","za","ke","tz","gh","ma","dz","sd","ao","ci","sn","ug","zw","tn","na","bw","zm","ml"]},
  {name:"Amerika",cc:["us","ca","mx","cu","gt","cr","br","ar","co","pe","cl","ve","ec","uy","bo","py"]},
  {name:"Ozeanien",cc:["au","nz"]},
];

const MODES=[
  /* ---- Pure Geo ---- */
  {id:"city",    icon:"\u{1F3D9}",title:"Stadt \u2192 Land",       group:"pure_geo",prompt:"In welchem Land liegt \u2026",          desc:"Ordne St\u00e4dte ihrem Land zu"},
  {id:"flag",    icon:"\u{1F6A9}",title:"Flagge \u2192 Land",      group:"pure_geo",prompt:"Welches Land zeigt diese Flagge?",        desc:"Erkenne L\u00e4nder an ihrer Flagge"},
  {id:"capital", icon:"\u{1F3DB}",title:"Hauptstadt \u2192 Land",  group:"pure_geo",prompt:"Zu welchem Land geh\u00f6rt diese Hauptstadt?",desc:"Welches Land geh\u00f6rt zu welcher Hauptstadt?"},
  {id:"river",   icon:"\u{1F30A}",title:"Fluss \u2192 Land",       group:"pure_geo",prompt:"In welchem Land liegt dieser Fluss?",      desc:"Weise Fl\u00fcsse ihren L\u00e4ndern zu"},
  {id:"landmark",icon:"\u{1F5FD}",title:"Sehenswürdigkeit",        group:"pure_geo",prompt:"In welchem Land liegt diese Sehenswürdigkeit?",desc:"Erkenne Sehenswürdigkeiten weltweit"},
  {id:"park",    icon:"\u{1F33F}",title:"Nationalpark",            group:"pure_geo",prompt:"In welchem Land liegt dieser Nationalpark?",desc:"Nationalparks aus aller Welt zuordnen"},
  {id:"unesco",  icon:"\u{1F3DB}",title:"UNESCO Welterbe",         group:"pure_geo",prompt:"In welchem Land liegt dieses UNESCO-Erbe?", desc:"UNESCO-Welterbe-St\u00e4tten zuordnen"},
  {id:"citymark",icon:"\u{1F306}",title:"Wahrzeichen \u2192 Stadt",group:"pure_geo",prompt:"In welcher Stadt liegt dieses Wahrzeichen?",desc:"Wahrzeichen ihrer Stadt zuordnen"},
  {id:"subway",  icon:"\u{1F687}",title:"U-Bahn-Netz",            group:"pure_geo",prompt:"Stadtverkehr-Experte",                      desc:"U-Bahn-Netze weltweit erkennen"},
  {id:"flagsel", icon:"\u{1F38C}",title:"Land \u2192 Flagge",      group:"pure_geo",prompt:"Welche Flagge geh\u00f6rt zu \u2026",   desc:"W\u00e4hle die richtige Flagge"},
  {id:"rcapital",icon:"\u{1F3DF}",title:"Land \u2192 Hauptstadt",  group:"pure_geo",prompt:"Was ist die Hauptstadt von \u2026",       desc:"Nenne die Hauptstadt eines Landes"},
  {id:"rcity",   icon:"\u{1F3E2}",title:"Land \u2192 Stadt",       group:"pure_geo",prompt:"Welche Stadt liegt in \u2026",            desc:"Nenne eine Stadt im gesuchten Land"},
  {id:"rriver",  icon:"\u{1F4A7}",title:"Land \u2192 Fluss",       group:"pure_geo",prompt:"Welcher Fluss fliesst durch \u2026",      desc:"Nenne einen Fluss im gesuchten Land"},
  {id:"river_real", icon:"\u{1F30A}",title:"Fluss \u2192 Land",    group:"pure_geo", prompt:"Durch welches Land flie\u00dft dieser Fluss?",desc:"Durch welches Land flie\u00dft dieser Fluss?"},
  /* ---- Lifestyle ---- */
  {id:"outline", icon:"\u{1F5FA}",title:"L\u00e4nder-Umrisse",      group:"lifestyle",prompt:"Welches Land hat diese Form?",           desc:"Erkenne L\u00e4nder an ihrer Umrissform"},
  {id:"food",    icon:"\u{1F37D}",title:"Gericht \u2192 Land",      group:"lifestyle",prompt:"Aus welchem Land kommt dieses Gericht?", desc:"Gerichte ihrer Heimatk\u00fcche zuordnen"},
  {id:"brand",   icon:"\u{1F3F7}",title:"Marke \u2192 Land",        group:"lifestyle",prompt:"Aus welchem Land kommt diese Marke?",    desc:"Marken ihrem Ursprungsland zuordnen"},
  {id:"currency",icon:"\u{1F4B1}",title:"W\u00e4hrung \u2192 Land",group:"lifestyle",prompt:"Zu welchem Land geh\u00f6rt diese W\u00e4hrung?",desc:"W\u00e4hrungen den L\u00e4ndern zuordnen"},
  {id:"curr_real",  icon:"\u{1F4B5}",title:"Land \u2192 W\u00e4hrung",group:"lifestyle",prompt:"Welche W\u00e4hrung hat …",     desc:"Nenne die W\u00e4hrung eines Landes"},
  {id:"pop_compare",icon:"\u{1F465}",title:"Mehr Einwohner?",      group:"lifestyle",prompt:"Hat [Land B] mehr oder weniger Einwohner?",desc:"Vergleiche Einwohnerzahlen zweier L\u00e4nder"},
  /* ---- EU Plates ---- */
  {id:"plate_casual",icon:"\u{1F697}",title:"EU-Kennzeichen",      group:"eu_plates",prompt:"Woher kommt dieses Kennzeichen?",          desc:"EU-Kennzeichen mit Hinweisen erkennen"},
  {id:"plate_hard",  icon:"\u{1F6A6}",title:"Kennzeichen Pro",     group:"eu_plates",prompt:"Region erkennen – kein Tipp\!",    desc:"EU-Kennzeichen ohne Hinweise – Profi-Level"},
  /* ---- Higher / Lower (existing) ---- */
  {id:"hl_pop",   icon:"\u{1F465}",title:"H/L Einwohner",  group:"hl_compare",prompt:"Mehr Einwohner?",   desc:"Welches Land hat mehr Einwohner?"},
  {id:"hl_river", icon:"\u{1F30A}",title:"H/L Flussl\u00e4nge", group:"hl_compare",prompt:"L\u00e4ngerer Fluss?",desc:"Welcher Fluss ist l\u00e4nger?"},
  {id:"hl_area",  icon:"\u{1F5FA}",title:"H/L Landfl\u00e4che",  group:"hl_compare",prompt:"Gr\u00f6\u00dferes Land?",desc:"Welches Land ist gr\u00f6\u00dfer?"},
  /* ---- Higher / Lower (coming soon) ---- */
  {id:"hl_gdp",       icon:"\u{1F4B0}",title:"H/L BIP",              group:"hl_compare",prompt:"H\u00f6heres BIP?",         desc:"Welches Land hat ein h\u00f6heres BIP?"},
  {id:"hl_density",   icon:"\u{1F3D8}",title:"H/L Bev\u00f6lkerungsdichte",group:"hl_compare",prompt:"Dichter besiedelt?",    desc:"Welches Land ist dichter besiedelt?"},
  {id:"hl_elevation", icon:"\u{26F0}",title:"H/L H\u00f6chster Punkt",group:"hl_compare",prompt:"H\u00f6herer Gipfel?",      desc:"Welches Land hat den h\u00f6heren Gipfel?"},
  {id:"hl_coastline", icon:"\u{1F3D6}",title:"H/L K\u00fcstÐµÐ½l\u00e4nge",group:"hl_compare",prompt:"L\u00e4ngere K\u00fcste?",desc:"Welches Land hat die l\u00e4ngere K\u00fcste?"},
  {id:"hl_borders",   icon:"\u{1F30F}",title:"H/L Nachbarl\u00e4nder",group:"hl_compare",prompt:"Mehr Nachbarn?",             desc:"Welches Land hat mehr Nachbarl\u00e4nder?"},
  {id:"hl_lifeexp",   icon:"\u2764",title:"H/L Lebenserwartung",   group:"hl_compare",prompt:"L\u00e4nger leben?",            desc:"In welchem Land lebt man l\u00e4nger?"},
  {id:"hl_median_age",icon:"\u{1F4C5}",title:"H/L Medianalter",    group:"hl_compare",prompt:"H\u00f6heres Medianalter?",     desc:"Welches Land hat ein h\u00f6heres Medianalter?"},
  {id:"hl_forest",    icon:"\u{1F333}",title:"H/L Waldf\u00e4che",  group:"hl_compare",prompt:"Mehr Wald?",                   desc:"Welches Land hat mehr Wald?"},

  /* HL Beta */
  {id:"hl_b_rain",  icon:"\u{1F327}",title:"\u{1F9EA} Niederschlag",  group:"pure_geo",prompt:"Mehr Regen?",              desc:"Mehr Jahresniederschlag?"},
  {id:"hl_b_temp",  icon:"\u{1F321}",title:"\u{1F9EA} Temperatur",    group:"pure_geo",prompt:"W\u00e4rmer?",            desc:"H\u00f6here Durchschnittstemp.?"},
  {id:"hl_b_sun",   icon:"\u2600",   title:"\u{1F9EA} Sonnenstunden", group:"pure_geo",prompt:"Mehr Sonne?",              desc:"Mehr Sonnenstunden/Jahr?"},
  {id:"hl_b_vulc",  icon:"\u{1F30B}",title:"\u{1F9EA} Vulkane",       group:"pure_geo",prompt:"Mehr Vulkane?",            desc:"Mehr aktive Vulkane?"},
  {id:"hl_b_parks", icon:"\u{1F333}",title:"\u{1F9EA} Nationalparks", group:"comparisons",prompt:"Mehr Parks?",              desc:"Mehr Nationalparks?"},
  {id:"hl_b_roads", icon:"\u{1F6E3}",title:"\u{1F9EA} Stra\u00dfennetz",group:"comparisons",prompt:"L\u00e4ngeres Stra\u00dfennetz?",desc:"Km Stra\u00dfen?"},
  {id:"hl_b_rail",  icon:"\u{1F686}",title:"\u{1F9EA} Schienennetz",  group:"comparisons",prompt:"L\u00e4ngeres Schienennetz?",desc:"Km Gleise?"},
  {id:"hl_b_net",   icon:"\u{1F4F6}",title:"\u{1F9EA} Internetspeed", group:"comparisons",prompt:"Schnelleres Internet?",    desc:"Schnelleres Breitband?"},
  {id:"hl_b_ev",    icon:"\u26A1",   title:"\u{1F9EA} E-Ladesäulen",  group:"comparisons",prompt:"Mehr E-Ladesäulen?",       desc:"E-Ladesäulen?"},
  {id:"hl_b_urban", icon:"\u{1F3D9}",title:"\u{1F9EA} Urbanisierung", group:"comparisons",prompt:"Mehr verst\u00e4dtert?",  desc:"Urbanisierungsrate?"},
  {id:"hl_b_lang",  icon:"\u{1F5E3}",title:"\u{1F9EA} Amtssprachen",  group:"lifestyle",prompt:"Mehr Amtssprachen?",       desc:"Anzahl Amtssprachen?"},
  {id:"hl_b_isl",   icon:"\u{1F3DD}",title:"\u{1F9EA} Inseln",        group:"pure_geo",prompt:"Mehr Inseln?",             desc:"Anzahl Inseln?"},
  {id:"hl_b_tz",    icon:"\u{1F550}",title:"\u{1F9EA} Zeitzonen",     group:"pure_geo",prompt:"Mehr Zeitzonen?",          desc:"Anzahl Zeitzonen?"},
  {id:"hl_b_founded",icon:"\u{1F3DB}",title:"\u{1F9EA} \u00c4ltestes Land",group:"pure_geo",prompt:"\u00c4lteres Land?",desc:"Fr\u00fcheres Gr\u00fcndungsjahr?"},
  {id:"hl_b_unesco",icon:"\u{1F3DB}",title:"\u{1F9EA} UNESCO",        group:"lifestyle",prompt:"Mehr UNESCO?",             desc:"UNESCO-Welterbest\u00e4tten?"},
  {id:"hl_b_tour",  icon:"\u{1F9F3}",title:"\u{1F9EA} Tourismus",     group:"lifestyle",prompt:"Mehr Touristen?",          desc:"Touristen/Jahr?"},
  {id:"hl_b_wm",    icon:"\u26BD",   title:"\u{1F9EA} WM-Teilnahmen", group:"sport",prompt:"Mehr WM-Teilnahmen?",      desc:"Fu\u00dfball-WM-Teilnahmen?"},
  /* ---- Neighbors ---- */
  {id:"neighbor",      icon:"\u{1F91D}",title:"Grenzg\u00e4nger",     group:"neighbors", prompt:"Grenzt an\u2026?",               desc:"Grenzt dieses Land an jenes?"},
  {id:"neighbor_fake", icon:"\u{1F47A}",title:"Falscher Nachbar",  group:"neighbors", prompt:"Grenzt NICHT an\u2026?",         desc:"Welches Land grenzt NICHT an das gezeigte?",time:20},
  {id:"neighbor_count",icon:"\u{1F522}",title:"Nachbar-Z\u00e4hler",group:"neighbors", prompt:"Wie viele Nachbarn?",               desc:"Z\u00e4hle die Nachbarl\u00e4nder des Landes",time:20},
  /* ---- Map ---- */
  {id:"map_guess",  icon:"\u{1F5FA}",title:"Finde das Land",    group:"map_mode",prompt:"Klick auf das gesuchte Land",         desc:"Klicke das gesuchte Land auf der Weltkarte"},
  {id:"map_reverse",icon:"\u{1F3AF}",title:"Wer bin ich?",        group:"map_mode",prompt:"Welches Land ist markiert?",          desc:"Erkenne das markierte Land auf der Weltkarte",time:25},
  {id:"map_capital",icon:"📍",title:"Hauptstadt-Radar",   group:"map_mode",prompt:"Tippe auf das Land der Hauptstadt",  desc:"Kenne die Hauptstädte",time:25},
  {id:"map_ivr",icon:"\u{1F697}\u{1F194}",title:"Kennzeichen-Knacker",group:"eu_plates",prompt:"IVR-Quiz",desc:"Finde das internationale L\u00e4nderkennzeichen",time:20},
  /* ---- New Game Modes (coming soon) ---- */
  {id:"logic_grid",    icon:"\u{1F9E9}",title:"Logik-Gitter",          group:"new_modes",prompt:"L\u00f6se das R\u00e4tsel",                desc:"L\u00f6se geografische Logik-R\u00e4tsel"},
  {id:"travel_route",  icon:"\u{1F5FA}",title:"Reiseroute",            group:"new_modes",prompt:"K\u00fcrzeste Route?",                      desc:"Plane die k\u00fcrzeste Route zwischen St\u00e4dten"},
  {id:"flag_fusion",   icon:"\u{1F3C1}",title:"Flaggen-Fusion",        group:"new_modes",prompt:"Welche zwei L\u00e4nder?",                  desc:"Erkenne L\u00e4nder aus verschmolzenen Flaggen"},
  {id:"climate_mystery",icon:"\u{1F326}",title:"Klima-Krimi",          group:"new_modes",prompt:"Welches Land versteckt sich hinter diesen Klima-Hinweisen?",                             desc:"Land anhand von Klima-Clues erraten"},
  {id:"alpha_sprint",  icon:"📍",title:"Alphabet-Sprint",       group:"new_modes",prompt:"L\u00e4nder von A\u2013Z",                 desc:"Nenne L\u00e4nder f\u00fcr jeden Buchstaben"},
  {id:"wappen_meister",icon:"\u{1F6E1}",title:"Wappen-Meister",t_key:"mode_wappen",    group:"pure_geo",prompt:"Welchem Land geh\u00f6rt dieses Wappen?",desc:"Erkenne L\u00e4nder an ihrem Wappen"},
  {id:"slf",           icon:"📝",title:"Stadt, Land, Fluss",t_key:"mode_slf",noMultiplayer:true,  group:"pure_geo",prompt:"Nenne Land und Hauptstadt\u2026",    desc:"Der absolute Spiele-Klassiker"},
  {id:"timezone_jumper",icon:"\u23F0",title:"Zeitzonen-Jumper",       group:"new_modes",prompt:"Welche Zeitzone?",                            desc:"Meistere die Zeitzonen der Welt"},
  {id:"plate_compare",icon:"\u{1F9EA}\u{1F697}",title:"\u{1F9EA} Kenn. Vergleich",group:"comparisons",prompt:"Kennzeichen-Vergleich",desc:"Zwei Kennzeichen – welches Land gewinnt?",comingSoon:false},
  {id:"stadium",icon:"\u26BD",title:"Stadion-Quiz",group:"sport",prompt:"In welchem Land steht dieses Stadion?",desc:"Fu\u00dfballstadien zuordnen"},
  {id:"jersey",icon:"\u{1F455}",title:"Trikot-Quiz",group:"sport",prompt:"Welches Land tr\u00e4gt dieses Trikot?",desc:"Nationalteam-Trikots erkennen"},
  {id:"crest",icon:"\u{1F6E1}",title:"Wappen-Quiz",group:"sport",prompt:"Welchem Land geh\u00f6rt dieses Wappen?",desc:"Verbandswappen zuordnen"},
  /* ---- Vergleiche / Comparisons (Phase 91+92) ---- */
  {id:"comp_area",      icon:"\u{1F5FA}",title:"Gr\u00f6\u00dferes Land?",      group:"comparisons",prompt:"Welches Land ist gr\u00f6\u00dfer?",       desc:"Fl\u00e4che zweier L\u00e4nder vergleichen"},
  {id:"comp_pop",       icon:"\u{1F465}",title:"Mehr Einwohner?",               group:"comparisons",prompt:"Welches Land hat mehr Einwohner?",       desc:"Bev\u00f6lkerung zweier L\u00e4nder vergleichen"},
  {id:"comp_north",     icon:"\u2b06\ufe0f",title:"Weiter n\u00f6rdlich?",     group:"comparisons",prompt:"Welches Land liegt n\u00f6rdlicher?",    desc:"Zwei L\u00e4nder nach Breitengrad"},
  {id:"comp_gdp",       icon:"\u{1F4B0}",title:"H\u00f6heres BIP?",            group:"comparisons",prompt:"H\u00f6heres BIP pro Kopf?",              desc:"BIP pro Kopf vergleichen"},
  {id:"comp_density",   icon:"\u{1F3D8}",title:"Dichter besiedelt?",            group:"comparisons",prompt:"Welches Land ist dichter besiedelt?",    desc:"Bev\u00f6lkerungsdichte vergleichen"},
  {id:"comp_elevation", icon:"\u26F0",   title:"H\u00f6herer Gipfel?",         group:"comparisons",prompt:"Welches Land hat den h\u00f6heren Gipfel?",desc:"H\u00f6chste Erhebung vergleichen"},
  {id:"comp_coast",     icon:"\u{1F3D6}",title:"L\u00e4ngere K\u00fcste?",    group:"comparisons",prompt:"Welches Land hat die l\u00e4ngere K\u00fcste?",desc:"K\u00fcstenl\u00e4nge vergleichen"},
  {id:"comp_borders",   icon:"\u{1F30F}",title:"Mehr Nachbarn?",               group:"comparisons",prompt:"Welches Land hat mehr Nachbarl\u00e4nder?",desc:"Anzahl der Nachbarn vergleichen"},
  {id:"comp_life",      icon:"\u2764",   title:"L\u00e4nger leben?",           group:"comparisons",prompt:"In welchem Land lebt man l\u00e4nger?",  desc:"Lebenserwartung vergleichen"},
  {id:"comp_age",       icon:"\u{1F4C5}",title:"H\u00f6heres Medianalter?",   group:"comparisons",prompt:"H\u00f6heres Medianalter?",               desc:"Medianalter zweier L\u00e4nder"},
  {id:"comp_forest",    icon:"\u{1F333}",title:"Mehr Wald?",                   group:"comparisons",prompt:"Welches Land hat mehr Waldfl\u00e4che?",  desc:"Waldfl\u00e4che vergleichen"},
  /* Phase 129+130 BETA modes */
  {id:"comp_airports",  icon:"\u2708\uFE0F",title:"Mehr Flugh\u00e4fen?",    group:"comparisons",prompt:"Welches Land hat mehr Flugh\u00e4fen?",             desc:"Flughafenanzahl zweier L\u00e4nder vergleichen"},
  {id:"comp_flight_TMP",    icon:"\u{1F5FA}",title:"Gr\u00f6\u00dferes Land?",  group:"comparisons",prompt:"L\u00e4ngster m\u00f6glicher Inlandsflug?",          desc:"Fl\u00e4che als Proxy f\u00fcr Inlandsflugdistanz"},
  {id:"comp_mountain",  icon:"\u26F0",  title:"H\u00f6herer Gipfel?",          group:"comparisons",prompt:"Welches Land hat den h\u00f6heren Gipfel?",        desc:"H\u00f6chste Erhebung (erweiterter Datensatz)"},
  {id:"comp_nsextent",  icon:"\u{1F9ED}",title:"L\u00e4nger Nord-S\u00fcd?", group:"comparisons",prompt:"Welches Land erstreckt sich weiter von Nord nach S\u00fcd?",         desc:"Nord-S\u00fcd-Ausdehnung vergleichen"},
  {id:"comp_olympics_TMP",  icon:"\u{1F3C5}",title:"Mehr Olympia-Gold?",           group:"comparisons",prompt:"Welches Land hat mehr Olympia-Goldmedaillen?",         desc:"Sommerolympiade-Goldmedaillen vergleichen"},
  {id:"iata",           icon:"\u2708\uFE0F",title:"IATA-Code?",               group:"airports",prompt:"Zu welcher Stadt geh\u00f6rt dieser Flughafen-Code?", desc:"IATA-Codes der gro\u00dfen Flugh\u00e4fen kennen"},
  {id:"tz_quiz",  icon:"\u23F0",  title:"Welche Uhrzeit?",               group:"airports",prompt:"Wie sp\u00e4t ist es gerade in dieser Stadt?", desc:"UTC-Offsets und Zeitzonen"},
  {id:"climate_quiz",   icon:"\u{1F321}\uFE0F",title:"Klima-Krimi",          group:"airports",prompt:"Welches Land versteckt sich hinter diesen Klima-Hinweisen?", desc:"Land anhand von Klima-Clues erraten"},
  {id:"flagcolor", icon:"\u{1F6A9}",title:"Flaggen-Farben",              group:"airports",prompt:"Welche Farbe fehlt in dieser Flagge?",     desc:"Flaggenfarben auswendig kennen"},
  {id:"landlocked_quiz",icon:"\u{1F30A}",title:"Binnenstaat?",                 group:"airports",prompt:"Welches Land hat keinen Meereszugang?",    desc:"Binnenstaaten von K\u00fcstenl\u00e4ndern unterscheiden"},
  /* Phase 166: 28 BETA modes */
  {id:"b1", icon:"\u26BD",title:"\u{1F9EA} Ausreisser-Farben",    group:"sport",   prompt:"Welches Land traegt unerwartete Trikotfarben?",      desc:"Trikotfarben vs. Flaggenfarben"},
  {id:"b2", icon:"\u{1F3CE}",title:"\u{1F9EA} F1-Spotter",           group:"sport",   prompt:"In welchem Land liegt diese Rennstrecke?",             desc:"Formel-1-Strecken auf der Karte finden"},
  {id:"b4", icon:"\u{1F3C5}",title:"\u{1F9EA} Olympia-Zeitmaschine",group:"sport",   prompt:"Wer war Gastgeber der Sommerspiele?",                   desc:"Olympia-Gastgeberländer erraten"},
  {id:"b6", icon:"\u{1F94A}",title:"\u{1F9EA} Nationalsportarten",   group:"sport",   prompt:"Aus welchem Land stammt dieser Sport?",                desc:"Nationale Sportarten zuordnen"},
  {id:"b7", icon:"\u{1F3DF}",title:"\u{1F9EA} Höhenluft-Stadien",  group:"sport",   prompt:"Welches Stadion liegt höher?",                         desc:"Stadien nach Hoehe vergleichen"},
  {id:"b9", icon:"\u{1F30D}",title:"\u{1F9EA} Sport-Ursprung",       group:"sport",   prompt:"Wo wurde diese Sportart erfunden?",                    desc:"Geburtsort von Sportarten kennen"},
  {id:"b11",icon:"\u2694\uFE0F",title:"\u{1F9EA} Rivalen-Distanz",  group:"sport",   prompt:"Wie weit liegen Derby-Gegner auseinander?",             desc:"Entfernung zwischen Rivalenstadien schaetzen"},
  {id:"b17",icon:"\u{1F947}",title:"\u{1F9EA} Medaillen-Spiegel",    group:"sport",   prompt:"Welches Land hat mehr Winter-Gold?",                   desc:"Winter-Olympia-Goldmedaillen vergleichen"},
  {id:"b19",icon:"\u274C",   title:"\u{1F9EA} WM-Fehltritte",         group:"sport",   prompt:"Wer war nie bei der WM dabei?",                        desc:"Laender die sich nie qualifiziert haben"},
  {id:"b20",icon:"\u{1F3C6}",title:"\u{1F9EA} Sport-Wappen",          group:"sport",   prompt:"Zu welcher Stadt gehoert dieses Team?",                desc:"Sport-Teams ihrer Heimat zuordnen"},
  {id:"b21",icon:"\u{1F5FA}",title:"\u{1F9EA} Sandwich-Laender",     group:"neighbors",prompt:"Welches Land ist von diesen umschlossen?",            desc:"Eingeschlossene Laender erkennen"},
  {id:"b22",icon:"\u{1F697}",title:"\u{1F9EA} Transit-Route",         group:"neighbors",prompt:"Welches Land muss man durchqueren?",                  desc:"Pflicht-Transitlaender kennen"},
  {id:"b23",icon:"\u{1F30A}",title:"\u{1F9EA} Kueste oder Inland?",  group:"neighbors",prompt:"Hat dieser Nachbarstaat Meereszugang?",              desc:"Binnenstaaten vs. Kuestenlaender"},
  {id:"b25",icon:"\u{1F914}",title:"\u{1F9EA} Fehlender Nachbar",     group:"neighbors",prompt:"Welcher Nachbar fehlt in der Liste?",                 desc:"Vollstaendige Nachbarschaftslisten kennen"},
  {id:"b29",icon:"\u{1F4CF}",title:"\u{1F9EA} Längste Grenze",       group:"neighbors",prompt:"Mit wem teilt dieses Land die längste Grenze?",      desc:"Längste Landgrenzen kennen"},
  {id:"b37",icon:"\u{1F4CD}",title:"\u{1F9EA} Hauptstadt-Naehe",      group:"neighbors",prompt:"Welches Hauptstadtpaar liegt naeher beieinander?",    desc:"Entfernung zwischen Hauptstaedten vergleichen"},
  {id:"b40",icon:"\u{1F91D}",title:"\u{1F9EA} Meiste Nachbarn",       group:"neighbors",prompt:"Welches Land hat mehr Landgrenzen?",                  desc:"Anzahl der Landgrenzen vergleichen"},
  {id:"b41",icon:"\u{1F310}",title:"\u{1F9EA} Äquator-Schuetze",    group:"map_mode",prompt:"Klicke auf ein Äquator-Land",                          desc:"Äquatorlaender auf der Karte finden"},
  {id:"b42",icon:"\u{1F333}",title:"\u{1F9EA} Klimazonen-Spotter",    group:"map_mode",prompt:"Finde das Land mit Tropenwald",                         desc:"Tropenwaldlaender auf der Karte anklicken"},
  {id:"b44",icon:"\u{1F9ED}",title:"\u{1F9EA} Breitengrad-Duell",    group:"map_mode",prompt:"Was liegt weiter noerdlich?",                            desc:"Breitengrade schätzen"},
  {id:"b45",icon:"\u26A1",   title:"\u{1F9EA} E-Mobility-Hotspot",    group:"map_mode",prompt:"Klicke auf das EV-fuehrende Land",                      desc:"Elektromobilitaets-Vorreiterlaender"},
  {id:"b46",icon:"\u{1F4A7}",title:"\u{1F9EA} Naturwunder-Spotter",   group:"map_mode",prompt:"Wo liegen diese Naturwunder?",                           desc:"Naturwunder auf der Weltkarte finden"},
  {id:"b47",icon:"\u{1F573}\uFE0F",title:"\u{1F9EA} Antipoden-Loch", group:"map_mode",prompt:"Wo kommst du auf der anderen Seite heraus?",             desc:"Antipoden der Erde kennen"},
  {id:"b51",icon:"\u{1F3DC}",title:"\u{1F9EA} Wuesten-Fokus",         group:"map_mode",prompt:"Klicke auf das Wuestenland",                             desc:"Grosse Wuesten auf der Karte lokalisieren"},
  {id:"b53",icon:"\u{1F6A2}",title:"\u{1F9EA} Meerengen & Kanaele",  group:"map_mode",prompt:"In welchem Land liegt dieser Kanal?",                   desc:"Wichtige Wasserstrassen kennen"},
  {id:"b54",icon:"\u{1F3D4}",title:"\u{1F9EA} Gipfel-Spotter",        group:"map_mode",prompt:"Klicke auf das Land mit dem hoechsten Berg",             desc:"Berge ihren Laendern zuordnen"},
  {id:"b58",icon:"\u{1F30A}",title:"\u{1F9EA} See-Spotter",            group:"map_mode",prompt:"Klicke auf das Land am grossen See",                    desc:"Grosse Seen auf der Karte finden"},
  {id:"b60",icon:"\u{1F303}",title:"\u{1F9EA} Nacht-Satellit",         group:"map_mode",prompt:"Welche Region leuchtet nachts am hellsten?",             desc:"Lichtintensitaet auf Satellitenkarten"}
];

function modeTitle(m){return m&&m.t_key?t(m.t_key):m?m.title:"";}
const MODE_CATS={
  pure_geo:{label:"Pure Geo",icon:"\u{1F30D}",modes:["city","flag","capital","river","landmark","park","unesco","citymark","subway","flagsel","rcapital","rcity","rriver","river_real","logic_grid","travel_route","flag_fusion","climate_mystery","alpha_sprint","timezone_jumper","wappen_meister","slf","hl_b_rain","hl_b_temp","hl_b_sun","hl_b_vulc","hl_b_isl","hl_b_tz","hl_b_founded"],cost:0},
  lifestyle:{label:"Kultur & Lifestyle",icon:"\u{1F3A8}",modes:["outline","food","brand","currency","curr_real","pop_compare","hl_b_tour","hl_b_unesco","hl_b_lang"],cost:1000},
  eu_plates:{label:"Kennzeichen",icon:"\u{1F697}",modes:["plate_casual","plate_hard","map_ivr"],cost:500},
  hl_compare:{label:"Higher / Lower",icon:"\u2b06\ufe0f",modes:["hl_pop","hl_river","hl_area","hl_gdp","hl_density","hl_elevation","hl_coastline","hl_borders","hl_lifeexp","hl_median_age","hl_forest"],cost:0},
  comparisons:{label:"Vergleiche",icon:"\u2696\ufe0f",modes:["comp_area","comp_pop","comp_north","comp_gdp","comp_density","comp_elevation","comp_coast","comp_borders","comp_life","comp_age","comp_forest","comp_airports","comp_mountain","comp_nsextent","hl_b_parks","hl_b_roads","hl_b_rail","hl_b_net","hl_b_ev","hl_b_urban","plate_compare"],cost:0},
  airports:{label:"Airports & Spezial",icon:"\u2708\uFE0F",modes:["iata","tz_quiz","climate_quiz","flagcolor","landlocked_quiz"],cost:0},
  neighbors:{label:"Nachbarl\u00e4nder",icon:"\u{1F91D}",modes:["neighbor","neighbor_fake","neighbor_count","b21","b22","b23","b25","b29","b37","b40"],cost:0},
  map_mode:{label:"Weltkarte",icon:"\u{1F5FA}",modes:["map_guess","map_reverse","map_capital","b41","b42","b44","b45","b46","b47","b51","b53","b54","b58","b60"],cost:0},
  sport:{label:"Sport",icon:"\u{1F3C6}",modes:["stadium","jersey","crest","comp_olympics","comp_flight","hl_b_wm","b1","b2","b4","b6","b7","b9","b11","b17","b19","b20"],cost:0},
};

/* Phase 28: New real-data mode generators */
function genCurrRealQ(){
  if(!CURR_REAL||!CURR_REAL.length)return null;
  const _fcc=_rfilt(COUNTRIES,2);const _ccc=new Set(_fcc.map(x=>x.cc));
  const _crPool=CURR_REAL.filter(x=>_ccc.has(ccFromCountry(x.c)));
  const _crSrc=_crPool.length>=2?_crPool:CURR_REAL;
  const idx=~~(rng()*_crSrc.length);
  const cor=_crSrc[idx];
  /* Show only currency name+ISO – NOT country name (would give away the answer) */
  const dis=CURR_REAL.filter((_,i)=>i!==idx).sort(()=>rng()-.5).slice(0,3).map(x=>x.n+" ("+x.iso+")");
  const ans=cor.n+" ("+cor.iso+")";
  return{type:"curr_real",prompt:"Welche W\u00e4hrung hat …",subj:displayCountry(ccFromCountry(cor.c))||cor.c,ans,opts:sh([ans,...dis]),meta:cor.n,lid:cor.c,cc:ccFromCountry(cor.c)};
}
function genPopCompareQ(){
  if(!CAPS_POP||CAPS_POP.length<2)return null;
  const _fpp=_rfilt(COUNTRIES,4);const _cpp=new Set(_fpp.map(x=>x.cc));
  let pool=CAPS_POP.filter(x=>x.pop>500000&&_cpp.has(ccFromCountry(x.c)));
  if(pool.length<2)pool=CAPS_POP.filter(x=>x.pop>500000);if(pool.length<2)return null;
  const ai=~~(rng()*pool.length);
  let bi=~~(rng()*pool.length);
  while(bi===ai)bi=~~(rng()*pool.length);
  const a=pool[ai],b=pool[bi];
  const ans=b.pop>a.pop?"more":"less";
  const wrong=b.pop>a.pop?"less":"more";
  const aPopStr=(a.pop/1e6).toFixed(1)+" Mio.";
  return{type:"pop_compare",prompt:t("q_pop_compare"),subj:{nameA:a.c,popA:aPopStr,nameB:b.c},ans,opts:[ans,wrong],meta:"",lid:b.c,cc:ccFromCountry(b.c)};
}
function genRiverRealQ(){
  if(!RIVERS_REAL||!RIVERS_REAL.length)return null;
  const _frr=_rfilt(COUNTRIES,2);const _ccr2=new Set(_frr.map(x=>x.cc));
  const _rrPool=RIVERS_REAL.filter(r=>_ccr2.has(ccFromCountry(r.c)));
  const _rrSrc=_rrPool.length>=1?_rrPool:RIVERS_REAL;
  const idx=~~(rng()*_rrSrc.length);
  const cor=_rrSrc[idx];
  const countries=[...new Set(RIVERS_REAL.map(r=>r.c))];
  const dis=countries.filter(c=>c!==cor.c).sort(()=>rng()-.5).slice(0,3);
  const meta=cor.len>0?cor.len+" km":"";
  return{type:"river_real",prompt:t("q_river_real"),subj:cor.n,ans:displayCountry(ccFromCountry(cor.c))||cor.c,opts:sh([displayCountry(ccFromCountry(cor.c))||cor.c,...dis.map(c=>displayCountry(ccFromCountry(c))||c)]),meta,lid:cor.n,cc:ccFromCountry(cor.c)};
}

/* Phase 30 – Default neighbor map (fallback when neighbors.json is empty/broken) */
/* Phase 91+92: static comparison data – 96 countries */
/* keys match COUNTRIES[].c exactly */
/* lat=northernmost latitude, gdp=GDP/capita USD, elev=highest m, */
/* coast=coastline km, life=life expectancy, age=median age, */
/* forest=forest %, bord=land borders, dens=pop density per km2 */
const COMP_DATA={
"Afghanistan":{lat:38,gdp:400,elev:7492,coast:0,life:64,age:19,forest:2,bord:6,dens:60},
"Algeria":{lat:37,gdp:4200,elev:2908,coast:998,life:77,age:29,forest:1,bord:6,dens:18},
"Angola":{lat:-4,gdp:2800,elev:2620,coast:1600,life:62,age:17,forest:46,bord:4,dens:26},
"Argentina":{lat:-21,gdp:13000,elev:6961,coast:4989,life:77,age:32,forest:10,bord:5,dens:17},
"Australia":{lat:-10,gdp:63000,elev:2228,coast:25760,life:84,age:38,forest:19,bord:0,dens:3},
"Austria":{lat:48,gdp:53000,elev:3798,coast:0,life:82,age:44,forest:47,bord:8,dens:109},
"Bangladesh":{lat:26,gdp:2700,elev:1052,coast:580,life:74,age:28,forest:11,bord:2,dens:1116},
"Belgium":{lat:51,gdp:51000,elev:694,coast:66,life:82,age:42,forest:22,bord:4,dens:383},
"Bolivia":{lat:-9,gdp:3600,elev:6542,coast:0,life:72,age:26,forest:51,bord:5,dens:12},
"Botswana":{lat:-17,gdp:8800,elev:1491,coast:0,life:70,age:26,forest:19,bord:4,dens:4},
"Brazil":{lat:5,gdp:9700,elev:2994,coast:7491,life:75,age:35,forest:59,bord:10,dens:25},
"Bulgaria":{lat:44,gdp:12500,elev:2925,coast:354,life:75,age:44,forest:37,bord:5,dens:60},
"Cambodia":{lat:14,gdp:1900,elev:1813,coast:443,life:70,age:28,forest:46,bord:3,dens:95},
"Canada":{lat:83,gdp:55000,elev:5959,coast:202080,life:83,age:42,forest:38,bord:1,dens:4},
"Chile":{lat:-17,gdp:16500,elev:6893,coast:6435,life:81,age:36,forest:24,bord:3,dens:26},
"China":{lat:53,gdp:12500,elev:8849,coast:14500,life:78,age:40,forest:23,bord:14,dens:153},
"Colombia":{lat:12,gdp:6500,elev:5775,coast:3208,life:78,age:32,forest:59,bord:6,dens:47},
"Costa Rica":{lat:11,gdp:13000,elev:3821,coast:1290,life:81,age:34,forest:55,bord:2,dens:105},
"Croatia":{lat:46,gdp:17000,elev:1831,coast:5835,life:79,age:45,forest:34,bord:5,dens:70},
"Cuba":{lat:23,gdp:8800,elev:1974,coast:3735,life:79,age:43,forest:31,bord:0,dens:107},
"Czech Republic":{lat:51,gdp:27000,elev:1602,coast:0,life:79,age:43,forest:34,bord:4,dens:137},
"Denmark":{lat:57,gdp:67000,elev:171,coast:7314,life:82,age:42,forest:16,bord:1,dens:136},
"DR Congo":{lat:5,gdp:600,elev:5109,coast:37,life:62,age:17,forest:67,bord:9,dens:40},
"Ecuador":{lat:1,gdp:6100,elev:6263,coast:2237,life:77,age:29,forest:49,bord:2,dens:71},
"Egypt":{lat:31,gdp:3700,elev:2629,coast:2450,life:72,age:25,forest:0,bord:5,dens:106},
"Estonia":{lat:59,gdp:27000,elev:318,coast:3794,life:79,age:43,forest:55,bord:3,dens:31},
"Ethiopia":{lat:15,gdp:1000,elev:4533,coast:0,life:68,age:19,forest:12,bord:6,dens:130},
"Finland":{lat:70,gdp:54000,elev:1324,coast:1250,life:83,age:43,forest:73,bord:3,dens:18},
"France":{lat:51,gdp:43000,elev:4808,coast:4853,life:83,age:42,forest:31,bord:8,dens:123},
"Germany":{lat:55,gdp:51000,elev:2962,coast:2389,life:82,age:46,forest:33,bord:9,dens:240},
"Ghana":{lat:11,gdp:2300,elev:885,coast:539,life:67,age:22,forest:35,bord:3,dens:134},
"Greece":{lat:41,gdp:20000,elev:2918,coast:13676,life:83,age:47,forest:32,bord:4,dens:82},
"Guatemala":{lat:17,gdp:5200,elev:4220,coast:400,life:74,age:22,forest:33,bord:4,dens:174},
"Hungary":{lat:48,gdp:20000,elev:1014,coast:0,life:77,age:44,forest:23,bord:7,dens:106},
"Iceland":{lat:66,gdp:72000,elev:2110,coast:4970,life:84,age:38,forest:0,bord:0,dens:3},
"India":{lat:35,gdp:2600,elev:8586,coast:7517,life:70,age:29,forest:24,bord:6,dens:460},
"Indonesia":{lat:6,gdp:4700,elev:4884,coast:54716,life:72,age:30,forest:49,bord:2,dens:151},
"Iran":{lat:39,gdp:4100,elev:5671,coast:2440,life:77,age:33,forest:7,bord:7,dens:54},
"Iraq":{lat:37,gdp:5500,elev:3611,coast:58,life:71,age:21,forest:2,bord:6,dens:98},
"Ireland":{lat:55,gdp:89000,elev:1041,coast:2497,life:83,age:38,forest:11,bord:1,dens:72},
"Israel":{lat:33,gdp:55000,elev:2236,coast:273,life:83,age:32,forest:8,bord:4,dens:430},
"Italy":{lat:47,gdp:34000,elev:4748,coast:7600,life:84,age:48,forest:32,bord:6,dens:200},
"Ivory Coast":{lat:10,gdp:2600,elev:1752,coast:520,life:59,age:19,forest:23,bord:5,dens:84},
"Japan":{lat:45,gdp:33000,elev:3776,coast:29751,life:85,age:49,forest:69,bord:0,dens:347},
"Jordan":{lat:33,gdp:4200,elev:1854,coast:26,life:75,age:24,forest:1,bord:5,dens:118},
"Kazakhstan":{lat:55,gdp:11000,elev:7010,coast:1894,life:74,age:32,forest:1,bord:5,dens:7},
"Kenya":{lat:4,gdp:2100,elev:5199,coast:536,life:68,age:20,forest:7,bord:5,dens:100},
"Laos":{lat:22,gdp:2500,elev:2817,coast:0,life:68,age:24,forest:82,bord:5,dens:32},
"Latvia":{lat:58,gdp:21000,elev:312,coast:498,life:76,age:44,forest:55,bord:4,dens:29},
"Lithuania":{lat:56,gdp:24000,elev:294,coast:99,life:77,age:45,forest:36,bord:4,dens:44},
"Malaysia":{lat:7,gdp:13000,elev:4095,coast:4675,life:77,age:30,forest:62,bord:2,dens:100},
"Mali":{lat:25,gdp:900,elev:1155,coast:0,life:59,age:16,forest:3,bord:7,dens:16},
"Mexico":{lat:32,gdp:10600,elev:5636,coast:9330,life:75,age:30,forest:34,bord:3,dens:65},
"Mongolia":{lat:52,gdp:5000,elev:4374,coast:0,life:72,age:29,forest:9,bord:2,dens:2},
"Morocco":{lat:36,gdp:3900,elev:4167,coast:1835,life:77,age:30,forest:12,bord:2,dens:84},
"Myanmar":{lat:28,gdp:1300,elev:5881,coast:1930,life:68,age:29,forest:44,bord:5,dens:83},
"Namibia":{lat:-17,gdp:5100,elev:2606,coast:1572,life:66,age:22,forest:9,bord:4,dens:3},
"Nepal":{lat:30,gdp:1400,elev:8849,coast:0,life:71,age:25,forest:40,bord:2,dens:212},
"Netherlands":{lat:53,gdp:56000,elev:322,coast:451,life:83,age:43,forest:11,bord:3,dens:523},
"New Zealand":{lat:-34,gdp:49000,elev:3724,coast:15134,life:83,age:38,forest:38,bord:0,dens:19},
"Nigeria":{lat:13,gdp:2100,elev:2419,coast:853,life:55,age:18,forest:25,bord:4,dens:226},
"Norway":{lat:71,gdp:87000,elev:2469,coast:25148,life:83,age:40,forest:37,bord:3,dens:15},
"Pakistan":{lat:37,gdp:1600,elev:8611,coast:1046,life:68,age:22,forest:5,bord:6,dens:290},
"Paraguay":{lat:-19,gdp:6000,elev:842,coast:0,life:73,age:28,forest:43,bord:3,dens:18},
"Peru":{lat:0,gdp:7200,elev:6768,coast:2414,life:74,age:30,forest:57,bord:5,dens:26},
"Philippines":{lat:20,gdp:3800,elev:2954,coast:36289,life:72,age:26,forest:27,bord:0,dens:368},
"Poland":{lat:54,gdp:18000,elev:2499,coast:440,life:79,age:42,forest:31,bord:7,dens:124},
"Portugal":{lat:42,gdp:24000,elev:2351,coast:1793,life:82,age:46,forest:35,bord:1,dens:110},
"Romania":{lat:48,gdp:16000,elev:2544,coast:225,life:77,age:43,forest:30,bord:5,dens:83},
"Russia":{lat:81,gdp:12500,elev:5642,coast:37653,life:73,age:40,forest:50,bord:14,dens:9},
"Saudi Arabia":{lat:32,gdp:28000,elev:3133,coast:2640,life:76,age:30,forest:1,bord:5,dens:16},
"Senegal":{lat:16,gdp:1600,elev:648,coast:531,life:69,age:19,forest:44,bord:5,dens:91},
"Serbia":{lat:46,gdp:10500,elev:2656,coast:0,life:77,age:43,forest:30,bord:8,dens:79},
"Singapore":{lat:1,gdp:84000,elev:166,coast:193,life:85,age:42,forest:23,bord:0,dens:8358},
"Slovakia":{lat:49,gdp:21000,elev:2655,coast:0,life:78,age:41,forest:41,bord:5,dens:114},
"South Africa":{lat:-22,gdp:6500,elev:3482,coast:2798,life:65,age:28,forest:7,bord:6,dens:48},
"South Korea":{lat:38,gdp:33000,elev:1950,coast:2413,life:84,age:44,forest:64,bord:1,dens:530},
"Spain":{lat:44,gdp:30000,elev:3718,coast:4964,life:84,age:46,forest:37,bord:3,dens:94},
"Sri Lanka":{lat:9,gdp:3800,elev:2524,coast:1340,life:77,age:35,forest:30,bord:0,dens:351},
"Sudan":{lat:22,gdp:800,elev:3071,coast:853,life:66,age:19,forest:11,bord:6,dens:25},
"Sweden":{lat:69,gdp:57000,elev:2104,coast:3218,life:84,age:41,forest:69,bord:3,dens:25},
"Switzerland":{lat:47,gdp:87000,elev:4634,coast:0,life:84,age:43,forest:32,bord:5,dens:219},
"Taiwan":{lat:25,gdp:33000,elev:3952,coast:1566,life:81,age:43,forest:59,bord:0,dens:672},
"Tanzania":{lat:-1,gdp:1100,elev:5895,coast:1424,life:68,age:18,forest:47,bord:8,dens:71},
"Thailand":{lat:20,gdp:7500,elev:2565,coast:3219,life:79,age:40,forest:33,bord:4,dens:137},
"Turkey":{lat:42,gdp:10700,elev:5137,coast:7200,life:77,age:33,forest:29,bord:8,dens:109},
"UAE":{lat:26,gdp:49000,elev:1934,coast:1318,life:79,age:35,forest:4,bord:3,dens:130},
"Uganda":{lat:4,gdp:900,elev:5109,coast:0,life:65,age:16,forest:8,bord:5,dens:213},
"Ukraine":{lat:52,gdp:4500,elev:2061,coast:2782,life:74,age:41,forest:17,bord:7,dens:73},
"United Kingdom":{lat:60,gdp:46000,elev:1345,coast:17819,life:82,age:40,forest:13,bord:1,dens:279},
"United States":{lat:71,gdp:76000,elev:6190,coast:19924,life:79,age:38,forest:34,bord:2,dens:36},
"Uruguay":{lat:-30,gdp:17000,elev:514,coast:660,life:78,age:36,forest:10,bord:2,dens:20},
"Venezuela":{lat:12,gdp:2500,elev:5007,coast:2800,life:73,age:30,forest:53,bord:4,dens:36},
"Vietnam":{lat:23,gdp:4300,elev:3143,coast:3444,life:75,age:32,forest:47,bord:3,dens:313},
"Zambia":{lat:-8,gdp:1300,elev:2301,coast:0,life:64,age:17,forest:65,bord:8,dens:24},
"Zimbabwe":{lat:-15,gdp:1600,elev:2592,coast:0,life:62,age:20,forest:39,bord:4,dens:35},
};
const _DEFAULT_NEIGHBORS={
  "Deutschland":["Frankreich","Belgien","Niederlande","Luxemburg","Schweiz","Österreich","Tschechien","Polen","Dänemark"],
  "Frankreich":["Deutschland","Belgien","Luxemburg","Schweiz","Italien","Spanien","Andorra","Monaco"],
  "Polen":["Deutschland","Tschechien","Slowakei","Ukraine","Belarus","Litauen","Russland"],
  "Österreich":["Deutschland","Schweiz","Liechtenstein","Italien","Slowenien","Ungarn","Slowakei","Tschechien"],
  "Schweiz":["Deutschland","Frankreich","Italien","Österreich","Liechtenstein"],
  "Spanien":["Frankreich","Andorra","Portugal"],
  "Portugal":["Spanien"],
  "Italien":["Frankreich","Schweiz","Österreich","Slowenien","San Marino"],
  "Russland":["Norwegen","Finnland","Estland","Lettland","Belarus","Ukraine","Georgien","Kasachstan","China","Mongolei","Nordkorea"],
  "China":["Russland","Mongolei","Kasachstan","Kirgisistan","Tadschikistan","Afghanistan","Pakistan","Indien","Nepal","Bhutan","Myanmar","Laos","Vietnam","Nordkorea"],
  "Indien":["Pakistan","China","Nepal","Bhutan","Bangladesh","Myanmar"],
  "Brasilien":["Venezuela","Guyana","Kolumbien","Peru","Bolivien","Paraguay","Argentinien","Uruguay"],
  "USA":["Kanada","Mexiko"],
  "Kanada":["USA"],
  "Mexiko":["USA","Guatemala","Belize"],
  "Argentinien":["Chile","Bolivien","Paraguay","Brasilien","Uruguay"],
  "Ukraine":["Russland","Belarus","Polen","Slowakei","Ungarn","Rumänien","Moldawien"],
  "Belarus":["Russland","Ukraine","Polen","Litauen","Lettland"],
  "Türkei":["Griechenland","Bulgarien","Georgien","Armenien","Aserbaidschan","Iran","Irak","Syrien"],
  "Iran":["Türkei","Irak","Afghanistan","Pakistan","Turkmenistan","Aserbaidschan","Armenien"],
  "Afghanistan":["Iran","Pakistan","Tadschikistan","Turkmenistan","Usbekistan","China"],
  "Pakistan":["Indien","Afghanistan","Iran","China"],
  "Irak":["Türkei","Syrien","Jordanien","Saudi-Arabien","Kuwait","Iran"],
  "Syrien":["Türkei","Irak","Jordanien","Libanon","Israel"],
  "Saudi-Arabien":["Jordanien","Irak","Kuwait","Bahrain","Katar","VAE","Oman","Jemen"],
  "ß„gypten":["Israel","Sudan","Libyen"],
  "Sudan":["ß„gypten","Libyen","Tschad","Zentralafrikanische Republik","Südsudan","ß„thiopien","Eritrea"],
  "ß„thiopien":["Eritrea","Dschibuti","Somalia","Kenia","Sudan","Südsudan"],
  "Nigeria":["Benin","Niger","Kamerun","Tschad"],
  "Demokratische Republik Kongo":["Republik Kongo","Angola","Sambia","Tansania","Ruanda","Burundi","Uganda","Zentralafrikanische Republik","Südsudan"],
  "Südafrika":["Namibia","Botswana","Simbabwe","Mosambik","Eswatini","Lesotho"],
  "Kenia":["ß„thiopien","Somalia","Tansania","Uganda","Südsudan"],
  "Ungarn":["Österreich","Slowakei","Ukraine","Rumänien","Serbien","Kroatien","Slowenien"],
  "Rumänien":["Ungarn","Ukraine","Moldawien","Bulgarien","Serbien"],
  "Griechenland":["Albanien","Nordmazedonien","Bulgarien","Türkei"],
  "Schweden":["Norwegen","Finnland","Dänemark"],
  "Norwegen":["Schweden","Finnland","Russland"],
  "Finnland":["Schweden","Norwegen","Russland","Estland"],
  "Kolumbien":["Venezuela","Brasilien","Peru","Ecuador","Panama"],
  "Peru":["Ecuador","Kolumbien","Brasilien","Bolivien","Chile"],
  "Bolivien":["Peru","Chile","Argentinien","Paraguay","Brasilien"],
  "Chile":["Peru","Bolivien","Argentinien"],
  "Venezuela":["Kolumbien","Brasilien","Guyana"],
  "Indonesien":["Malaysia","Papua-Neuguinea","Osttimor"],
  "Thailand":["Myanmar","Laos","Kambodscha","Malaysia"],
  "Vietnam":["China","Laos","Kambodscha"],
  "Myanmar":["Indien","Bangladesh","China","Laos","Thailand"],
  "Kasachstan":["Russland","China","Kirgisistan","Usbekistan","Turkmenistan"],
  "Marokko":["Algerien","Mauretanien","Spanien"],
  "Algerien":["Marokko","Tunesien","Libyen","Niger","Mali","Mauretanien"],
  "Tunesien":["Algerien","Libyen"],
  "Tschechien":["Deutschland","Polen","Slowakei","Österreich"],
  "Slowakei":["Tschechien","Polen","Ukraine","Ungarn","Österreich"],
  "Bulgarien":["Rumänien","Serbien","Nordmazedonien","Griechenland","Türkei"],
  "Serbien":["Ungarn","Rumänien","Bulgarien","Nordmazedonien","Kosovo","Montenegro","Bosnien","Kroatien"],
  "Kroatien":["Slowenien","Ungarn","Serbien","Bosnien","Montenegro"],
  "Slowenien":["Italien","Österreich","Ungarn","Kroatien"],
};
/* Phase 86 – Grenzkarte (nur Laender aus COUNTRIES) */
const ROUTE_BORDERS={
 "Germany":["France","Belgium","Netherlands","Denmark","Poland","Czech Republic","Austria","Switzerland"],
 "France":["Germany","Belgium","Switzerland","Italy","Spain"],
 "Poland":["Germany","Czech Republic","Slovakia","Ukraine","Lithuania","Russia"],
 "Austria":["Germany","Switzerland","Italy","Czech Republic","Slovakia","Hungary"],
 "Switzerland":["Germany","France","Italy","Austria"],
 "Spain":["France","Portugal","Morocco"],
 "Portugal":["Spain"],
 "Italy":["France","Switzerland","Austria"],
 "Hungary":["Austria","Slovakia","Ukraine","Romania","Serbia","Croatia"],
 "Romania":["Hungary","Ukraine","Bulgaria","Serbia"],
 "Bulgaria":["Romania","Serbia","Greece","Turkey"],
 "Greece":["Bulgaria","Turkey"],
 "Turkey":["Greece","Bulgaria","Iran","Iraq"],
 "Czech Republic":["Germany","Poland","Slovakia","Austria"],
 "Slovakia":["Czech Republic","Poland","Ukraine","Hungary","Austria"],
 "Serbia":["Hungary","Romania","Bulgaria","Croatia"],
 "Croatia":["Hungary","Serbia"],
 "Sweden":["Norway","Finland"],
 "Norway":["Sweden","Finland","Russia"],
 "Finland":["Sweden","Norway","Russia"],
 "Russia":["Norway","Finland","Estonia","Latvia","Lithuania","Poland","Ukraine","Kazakhstan","China","Mongolia"],
 "Ukraine":["Russia","Poland","Slovakia","Hungary","Romania"],
 "Estonia":["Latvia","Russia"],
 "Latvia":["Estonia","Lithuania","Russia"],
 "Lithuania":["Latvia","Poland","Russia"],
 "Netherlands":["Germany","Belgium"],
 "Belgium":["France","Germany","Netherlands"],
 "Denmark":["Germany"],
 "China":["Russia","Mongolia","Kazakhstan","India","Nepal","Myanmar","Laos","Vietnam","Pakistan","Afghanistan"],
 "India":["Pakistan","China","Nepal","Bangladesh","Myanmar"],
 "Pakistan":["India","Afghanistan","Iran","China"],
 "Afghanistan":["Pakistan","Iran","China"],
 "Iran":["Turkey","Iraq","Afghanistan","Pakistan"],
 "Iraq":["Turkey","Iran","Saudi Arabia","Jordan"],
 "Saudi Arabia":["Iraq","Jordan","UAE"],
 "Jordan":["Iraq","Saudi Arabia","Israel"],
 "Israel":["Jordan","Egypt"],
 "Egypt":["Israel","Sudan"],
 "Sudan":["Egypt","Ethiopia","Kenya"],
 "Ethiopia":["Sudan","Kenya","Uganda"],
 "Kenya":["Ethiopia","Sudan","Tanzania","Uganda"],
 "Tanzania":["Kenya","Uganda","Zambia","DR Congo"],
 "Uganda":["Kenya","Tanzania","DR Congo","Ethiopia"],
 "DR Congo":["Uganda","Tanzania","Angola","Zambia"],
 "Angola":["Zambia","DR Congo","Namibia"],
 "Zambia":["DR Congo","Tanzania","Zimbabwe","Botswana","Namibia","Angola"],
 "Zimbabwe":["Zambia","Botswana","South Africa"],
 "Botswana":["Zimbabwe","Zambia","Namibia","South Africa"],
 "Namibia":["Angola","Zambia","Botswana","South Africa"],
 "South Africa":["Namibia","Botswana","Zimbabwe"],
 "Nigeria":["Senegal","Mali"],
 "Morocco":["Algeria","Spain"],
 "Algeria":["Morocco","Mali"],
 "Mali":["Algeria","Senegal","Nigeria"],
 "Senegal":["Mali","Nigeria","Ivory Coast"],
 "Ivory Coast":["Senegal","Ghana"],
 "Ghana":["Ivory Coast"],
 "Colombia":["Venezuela","Brazil","Peru","Ecuador"],
 "Venezuela":["Colombia","Brazil"],
 "Brazil":["Venezuela","Colombia","Peru","Bolivia","Paraguay","Argentina","Uruguay"],
 "Peru":["Ecuador","Colombia","Brazil","Bolivia","Chile"],
 "Bolivia":["Peru","Chile","Argentina","Paraguay","Brazil"],
 "Chile":["Peru","Bolivia","Argentina"],
 "Argentina":["Chile","Bolivia","Paraguay","Brazil","Uruguay"],
 "Paraguay":["Argentina","Bolivia","Brazil"],
 "Uruguay":["Brazil","Argentina"],
 "Ecuador":["Colombia","Peru"],
 "Mexico":["United States","Guatemala"],
 "Guatemala":["Mexico","Costa Rica"],
 "Costa Rica":["Guatemala"],
 "United States":["Canada","Mexico"],
 "Canada":["United States"],
 "Thailand":["Myanmar","Laos","Cambodia","Malaysia"],
 "Vietnam":["China","Laos","Cambodia"],
 "Myanmar":["India","Bangladesh","China","Laos","Thailand"],
 "Laos":["China","Vietnam","Cambodia","Thailand","Myanmar"],
 "Cambodia":["Laos","Vietnam","Thailand"],
 "Malaysia":["Thailand"],
 "Kazakhstan":["Russia","China"],
 "Mongolia":["Russia","China"],
 "Nepal":["China","India"],
 "Bangladesh":["India","Myanmar"],
 "UAE":["Saudi Arabia"],
};
/* Phase 144 – Grid-Kriterien (Diversity Overhaul) */
/* Lookup sets for new criterion types */
const _ISLAND_STATES=new Set(["Australia","Cuba","Iceland","Indonesia","Ireland","Jamaica","Japan","Madagascar","New Zealand","Philippines","Singapore","Sri Lanka","Taiwan","United Kingdom","Trinidad and Tobago","Cyprus","Malta","Sri Lanka"]);
const _LANDLOCKED_SET=new Set(["Afghanistan","Austria","Bolivia","Botswana","Bulgaria","Czech Republic","Ethiopia","Hungary","Kazakhstan","Laos","Macedonia","Mali","Mongolia","Nepal","Paraguay","Serbia","Slovakia","Switzerland","Uganda","Zambia","Zimbabwe"]);
const _EU_MEMBERS=new Set(["Austria","Belgium","Bulgaria","Croatia","Cyprus","Czech Republic","Denmark","Estonia","Finland","France","Germany","Greece","Hungary","Ireland","Italy","Latvia","Lithuania","Netherlands","Poland","Portugal","Romania","Slovakia","Slovenia","Spain","Sweden"]);

/* Row pool: geographic criteria (continent, subregion, border, special) */
const GRID_ROW_POOL=[
  {id:"eu", type:"continent",value:"Europe",        label:"In Europa"},
  {id:"as", type:"continent",value:"Asia",          label:"In Asien"},
  {id:"af", type:"continent",value:"Africa",        label:"In Afrika"},
  {id:"sa", type:"continent",value:"South America", label:"In S\u00fcdamerika"},
  {id:"na", type:"continent",value:"North America", label:"In Nordamerika"},
  {id:"sr_we",type:"subregion",value:"Western Europe",  label:"Westeuropa"},
  {id:"sr_ee",type:"subregion",value:"Eastern Europe",  label:"Osteuropa"},
  {id:"sr_ne",type:"subregion",value:"Northern Europe", label:"Nordeuropa"},
  {id:"sr_se",type:"subregion",value:"Southern Europe", label:"S\u00fcdeuropa"},
  {id:"sr_ea",type:"subregion",value:"Eastern Asia",    label:"Ostasien"},
  {id:"sr_sq",type:"subregion",value:"Southeast Asia",  label:"S\u00fcdostasien"},
  {id:"sr_sa",type:"subregion",value:"Southern Asia",   label:"S\u00fcdasien"},
  {id:"sr_wa",type:"subregion",value:"Western Asia",    label:"Westasien / Naher Osten"},
  {id:"sr_waf",type:"subregion",value:"Western Africa", label:"Westafrika"},
  {id:"sr_eaf",type:"subregion",value:"Eastern Africa", label:"Ostafrika"},
  {id:"sr_naf",type:"subregion",value:"Northern Africa",label:"Nordafrika"},
  {id:"bde",type:"has_border",value:"Germany",label:"Grenzt an Deutschland"},
  {id:"bfr",type:"has_border",value:"France", label:"Grenzt an Frankreich"},
  {id:"bcn",type:"has_border",value:"China",  label:"Grenzt an China"},
  {id:"bru",type:"has_border",value:"Russia", label:"Grenzt an Russland"},
  {id:"bin",type:"has_border",value:"India",  label:"Grenzt an Indien"},
  {id:"bbr",type:"has_border",value:"Brazil", label:"Grenzt an Brasilien"},
  {id:"xeu",type:"eu_member",  label:"EU-Mitglied"},
  {id:"xll",type:"landlocked", label:"Binnenstaat"},
  {id:"xis",type:"island",     label:"Inselstaat"},
];

/* Col pool: letter criteria (all letters with >=2 countries in dataset) */
const GRID_COL_POOL=[
  {id:"la",type:"letter",value:"A",label:"Beginnt mit A"},
  {id:"lb",type:"letter",value:"B",label:"Beginnt mit B"},
  {id:"lc",type:"letter",value:"C",label:"Beginnt mit C"},
  {id:"ld",type:"letter",value:"D",label:"Beginnt mit D"},
  {id:"le",type:"letter",value:"E",label:"Beginnt mit E"},
  {id:"lf",type:"letter",value:"F",label:"Beginnt mit F"},
  {id:"lg",type:"letter",value:"G",label:"Beginnt mit G"},
  {id:"li",type:"letter",value:"I",label:"Beginnt mit I"},
  {id:"lj",type:"letter",value:"J",label:"Beginnt mit J"},
  {id:"lk",type:"letter",value:"K",label:"Beginnt mit K"},
  {id:"ll",type:"letter",value:"L",label:"Beginnt mit L"},
  {id:"lm",type:"letter",value:"M",label:"Beginnt mit M"},
  {id:"ln",type:"letter",value:"N",label:"Beginnt mit N"},
  {id:"lp",type:"letter",value:"P",label:"Beginnt mit P"},
  {id:"lr",type:"letter",value:"R",label:"Beginnt mit R"},
  {id:"ls",type:"letter",value:"S",label:"Beginnt mit S"},
  {id:"lt",type:"letter",value:"T",label:"Beginnt mit T"},
  {id:"lu",type:"letter",value:"U",label:"Beginnt mit U"},
  {id:"lv",type:"letter",value:"V",label:"Beginnt mit V"},
  {id:"lz",type:"letter",value:"Z",label:"Beginnt mit Z"},
];

/* Backward-compat alias */
const GRID_CRIT=GRID_ROW_POOL.concat(GRID_COL_POOL);
/* P161: Stadt pools */
const GRID_CITY_ROW_POOL=[
  {id:"ceu",type:"city_continent",value:"Europe",        label:"In Europa"},
  {id:"cas",type:"city_continent",value:"Asia",          label:"In Asien"},
  {id:"caf",type:"city_continent",value:"Africa",        label:"In Afrika"},
  {id:"csa",type:"city_continent",value:"South America", label:"In S\u00fcdamerika"},
  {id:"cna",type:"city_continent",value:"North America", label:"In Nordamerika"},
  {id:"cde",type:"city_country",  value:"Germany",       label:"In Deutschland"},
  {id:"cfr",type:"city_country",  value:"France",        label:"In Frankreich"},
  {id:"cus",type:"city_country",  value:"United States", label:"In den USA"},
  {id:"cbr",type:"city_country",  value:"Brazil",        label:"In Brasilien"},
  {id:"ccn",type:"city_country",  value:"China",         label:"In China"},
  {id:"cin",type:"city_country",  value:"India",         label:"In Indien"},
  {id:"cjp",type:"city_country",  value:"Japan",         label:"In Japan"},
  {id:"cmx",type:"city_country",  value:"Mexico",        label:"In Mexiko"},
  {id:"cru",type:"city_country",  value:"Russia",        label:"In Russland"},
  {id:"ctr",type:"city_country",  value:"Turkey",        label:"In der T\u00fcrkei"},
  {id:"car",type:"city_country",  value:"Argentina",     label:"In Argentinien"},
];
const GRID_CITY_COL_POOL=[
  {id:"cla",type:"city_letter",value:"A",label:"Beginnt mit A"},
  {id:"clb",type:"city_letter",value:"B",label:"Beginnt mit B"},
  {id:"clc",type:"city_letter",value:"C",label:"Beginnt mit C"},
  {id:"cld",type:"city_letter",value:"D",label:"Beginnt mit D"},
  {id:"clg",type:"city_letter",value:"G",label:"Beginnt mit G"},
  {id:"clh",type:"city_letter",value:"H",label:"Beginnt mit H"},
  {id:"clk",type:"city_letter",value:"K",label:"Beginnt mit K"},
  {id:"cll",type:"city_letter",value:"L",label:"Beginnt mit L"},
  {id:"clm",type:"city_letter",value:"M",label:"Beginnt mit M"},
  {id:"cln",type:"city_letter",value:"N",label:"Beginnt mit N"},
  {id:"clp",type:"city_letter",value:"P",label:"Beginnt mit P"},
  {id:"clr",type:"city_letter",value:"R",label:"Beginnt mit R"},
  {id:"cls",type:"city_letter",value:"S",label:"Beginnt mit S"},
  {id:"clt",type:"city_letter",value:"T",label:"Beginnt mit T"},
  {id:"clw",type:"city_letter",value:"W",label:"Beginnt mit W"},
];
/* P161: Wahrzeichen pools */
const GRID_LM_ROW_POOL=[
  {id:"leu",type:"lm_continent",value:"Europe", label:"In Europa"},
  {id:"las",type:"lm_continent",value:"Asia",   label:"In Asien"},
  {id:"laf",type:"lm_continent",value:"Africa", label:"In Afrika"},
];
const GRID_LM_COL_POOL=[
  {id:"lla",type:"lm_letter",value:"A",label:"Beginnt mit A"},
  {id:"llb",type:"lm_letter",value:"B",label:"Beginnt mit B"},
  {id:"llh",type:"lm_letter",value:"H",label:"Beginnt mit H"},
  {id:"llk",type:"lm_letter",value:"K",label:"Beginnt mit K"},
  {id:"llp",type:"lm_letter",value:"P",label:"Beginnt mit P"},
  {id:"lls",type:"lm_letter",value:"S",label:"Beginnt mit S"},
  {id:"llt",type:"lm_letter",value:"T",label:"Beginnt mit T"},
];
/* P161: UNESCO pools */
const GRID_UNESCO_ROW_POOL=[
  {id:"ueu",type:"un_continent",value:"Europe", label:"In Europa"},
  {id:"uas",type:"un_continent",value:"Asia",   label:"In Asien"},
  {id:"uaf",type:"un_continent",value:"Africa", label:"In Afrika"},
];
/* P168: Food grid pools */
const GRID_FOOD_ROW_POOL=[
  {id:"feu",type:"food_continent",value:"Europe",     label:"Europ\u00e4isch"},
  {id:"fas",type:"food_continent",value:"Asia",       label:"Asiatisch"},
  {id:"fam",type:"food_continent",value:"Americas",   label:"Amerikanisch"},
  {id:"faf",type:"food_continent",value:"Africa",     label:"Afrikanisch"},
];
const GRID_FOOD_COL_POOL=[
  {id:"flb",type:"food_letter",value:"B",label:"Beginnt mit B"},
  {id:"flc",type:"food_letter",value:"C",label:"Beginnt mit C"},
  {id:"flg",type:"food_letter",value:"G",label:"Beginnt mit G"},
  {id:"flp",type:"food_letter",value:"P",label:"Beginnt mit P"},
  {id:"flt",type:"food_letter",value:"T",label:"Beginnt mit T"},
  {id:"fls",type:"food_letter",value:"S",label:"Beginnt mit S"},
];
const GRID_UNESCO_COL_POOL=[
  {id:"ula",type:"un_letter",value:"A",label:"Beginnt mit A"},
  {id:"uld",type:"un_letter",value:"D",label:"Beginnt mit D"},
  {id:"ulf",type:"un_letter",value:"F",label:"Beginnt mit F"},
  {id:"ulk",type:"un_letter",value:"K",label:"Beginnt mit K"},
  {id:"ulp",type:"un_letter",value:"P",label:"Beginnt mit P"},
  {id:"uls",type:"un_letter",value:"S",label:"Beginnt mit S"},
  {id:"ult",type:"un_letter",value:"T",label:"Beginnt mit T"},
  {id:"ulv",type:"un_letter",value:"V",label:"Beginnt mit V"},
];
/* Phase 129: Airport data */
const _AIRPORTS={
"United States":13513,"Brazil":4093,"Mexico":1714,"Canada":1467,
"Russia":1218,"Argentina":978,"Bolivia":855,"Colombia":836,
"Peru":820,"Indonesia":673,"Germany":539,"China":507,
"Australia":480,"Chile":481,"Venezuela":444,"India":449,
"France":464,"United Kingdom":460,"Paraguay":799,"South Africa":407,
"Spain":150,"Italy":129,"Sweden":149,"Poland":126,
"Turkey":98,"Ukraine":189,"Kazakhstan":96,"Norway":98,
"Finland":74,"Nigeria":54,"Japan":175,"Iran":140,
"Tanzania":166,"Kenya":197
};
const _IATA={
"FRA":"Frankfurt","LHR":"London","CDG":"Paris","AMS":"Amsterdam",
"JFK":"New York","LAX":"Los Angeles","DXB":"Dubai","SYD":"Sydney",
"HND":"Tokio","MUC":"M\u00fcnchen","VIE":"Wien","ZRH":"Z\u00fcrich",
"BCN":"Barcelona","MAD":"Madrid","FCO":"Rom","ICN":"Seoul",
"SIN":"Singapur","BKK":"Bangkok","ORD":"Chicago","ATL":"Atlanta",
"MEX":"Mexico-Stadt","GRU":"S\u00e3o Paulo","EZE":"Buenos Aires",
"JNB":"Johannesburg","CAI":"Kairo","IST":"Istanbul",
"PMI":"Palma de Mallorca","PEK":"Peking","BOM":"Mumbai","DFW":"Dallas"
};
/* Phase 130: BETA expansion data */
/* UTC offsets (integer hours) */
const _TIMEZONES={
"London":0,"Reykjavik":0,"Lissabon":0,
"Berlin":1,"Paris":1,"Wien":1,"Madrid":1,"Rom":1,"Warschau":1,"Budapest":1,"Prag":1,
"Athen":2,"Kairo":2,"Bukarest":2,"Helsinki":2,"Kiew":2,
"Moskau":3,"Istanbul":3,"Riad":3,"Nairobi":3,
"Dubai":4,"Baku":4,
"Islamabad":5,"Taschkent":5,
"Dhaka":6,"Almaty":6,
"Bangkok":7,"Jakarta":7,
"Peking":8,"Singapur":8,"Kuala Lumpur":8,"Manila":8,"Taipei":8,
"Tokio":9,"Seoul":9,
"Sydney":10,"Brisbane":10,
"Auckland":12,
"Azoren":-1,
"Lissabon (Sommer)":-1,
"Buenos Aires":-3,"Sao Paulo":-3,
"New York":-5,"Toronto":-5,"Lima":-5,
"Chicago":-6,"Mexico-Stadt":-6,
"Denver":-7,
"Los Angeles":-8,"Vancouver":-8,
"Anchorage":-9,
"Honolulu":-10
};
/* 3 climate clues per country */
const _CLIMATE_CLUES={
"Brazil":["Jahresdurchschnitt 27\u00b0C","Gr\u00f6\u00dfter Regenwald der Welt","\u00fcberwiegend tropisches Klima"],
"Egypt":["Extrem trocken","W\u00fcstenklima dominiert","kaum Niederschlag"],
"Norway":["Polarkreis-Klima","lange Winter mit Schnee","kalt und feucht"],
"Australia":["Trockenster bewohnter Kontinent","riesiges Outback","Vielfalt: tropisch bis w\u00fcstenart."],
"Iceland":["Vulkanisch aktiv","subarktisch","h\u00e4ufig Wind & Regen"],
"Russia":["Permafrost in Sibirien","extrem kalte Winter","gr\u00f6\u00dfte Klimavielfalt"],
"India":["Monsun-Sommer","hei\u00dfe Ebenen","k\u00fchl im Himalaya"],
"Canada":["Arktisch im Norden","lange Winter","viel Schneefall"],
"Germany":["Gem\u00e4\u00dfigtes Klima","vier Jahreszeiten","oft bew\u00f6lkt"],
"Kenya":["Tropisch mit K\u00fchlhochland","zwei Regenzeiten","Savanne"],
"Chile":["Atacama-W\u00fcste im Norden","Patagonien im S\u00fcden","extrem vielf\u00e4ltig"],
"Finland":["Subarktisch","lange Winter","viele Seen & W\u00e4lder"],
"Japan":["vier ausgep\u00e4gte Jahreszeiten","Taifun-Saison","Schnee im Norden"]
};
/* Main flag colours per country */
const _FLAG_COLORS={
"Germany":["Schwarz","Rot","Gold"],
"France":["Blau","Wei\u00df","Rot"],
"Japan":["Wei\u00df","Rot"],
"Brazil":["Gr\u00fcn","Gelb","Blau","Wei\u00df"],
"United States":["Rot","Wei\u00df","Blau"],
"Italy":["Gr\u00fcn","Wei\u00df","Rot"],
"Sweden":["Blau","Gelb"],
"Poland":["Wei\u00df","Rot"],
"Switzerland":["Rot","Wei\u00df"],
"Turkey":["Rot","Wei\u00df"],
"China":["Rot","Gelb"],
"Australia":["Blau","Rot","Wei\u00df"],
"Canada":["Rot","Wei\u00df"],
"South Africa":["Schwarz","Gelb","Gr\u00fcn","Rot","Wei\u00df","Blau"],
"Mexico":["Gr\u00fcn","Wei\u00df","Rot"],
"Austria":["Rot","Wei\u00df"],
"Netherlands":["Rot","Wei\u00df","Blau"],
"Ukraine":["Blau","Gelb"],
"Belgium":["Schwarz","Gelb","Rot"],
"Norway":["Rot","Wei\u00df","Blau"],
"Finland":["Wei\u00df","Blau"],
"Denmark":["Rot","Wei\u00df"],
"Greece":["Blau","Wei\u00df"],
"Portugal":["Gr\u00fcn","Rot","Gelb"],
"Hungary":["Rot","Wei\u00df","Gr\u00fcn"],
"Ireland":["Gr\u00fcn","Wei\u00df","Orange"],
"Romania":["Blau","Gelb","Rot"],
"Spain":["Rot","Gelb"],
"Bulgaria":["Wei\u00df","Gr\u00fcn","Rot"],
"Croatia":["Rot","Wei\u00df","Blau"]
};
/* Highest point in metres */
const _ELEVATION={
"China":8849,"Nepal":8849,"Pakistan":8611,"India":8598,
"Argentina":6960,"Chile":6893,"Bolivia":6542,"Peru":6268,
"United States":6190,"Ecuador":6263,"Russia":5642,"Tanzania":5895,
"Kenya":5199,"Mexico":5636,"Ethiopia":4533,"Morocco":4167,
"Germany":2962,"Austria":3798,"Switzerland":4634,"France":4808,
"Italy":4748,"Spain":3478,"Norway":2469,"Sweden":2111,
"Finland":1324,"Poland":2503,"Turkey":5137,"Iran":5671,
"Japan":3776,"South Korea":1950,"Indonesia":4884,
"Australia":2228,"New Zealand":3724,"Canada":5959,"Colombia":5775
};
/* Landlocked countries (no sea access) */
const _LANDLOCKED=[
"Austria","Switzerland","Czech Republic","Hungary","Slovakia",
"Bolivia","Paraguay","Afghanistan","Kazakhstan","Mongolia",
"Ethiopia","Uganda","Zimbabwe","Zambia","Mali",
"Laos","Nepal","Serbia"
];
/* North-South extent in km */
const _NS_EXTENT={
"Chile":4270,"Brazil":4395,"Russia":4000,"Canada":5000,
"United States":2600,"Argentina":3694,"China":3800,
"India":3214,"Australia":3200,"Germany":876,
"France":1000,"Spain":800,"Italy":1185,
"Norway":1760,"Sweden":1572,"Mexico":2000,
"Peru":1850,"Colombia":1700,"Japan":2800,
"Indonesia":1770,"Turkey":500,"Iran":1600
};
/* Summer Olympic gold medals (historical total) */
const _OLYMPICS={
"United States":1061,"Russia":395,"Germany":201,
"United Kingdom":284,"France":223,"Italy":217,
"China":263,"Australia":171,"Sweden":152,
"Hungary":182,"Japan":169,"South Korea":90,
"Finland":101,"Cuba":78,"Romania":89,
"Netherlands":92,"Bulgaria":52,"Poland":68,
"Kenya":36,"Brazil":37,"Norway":60,
"Denmark":46,"Canada":77,"Spain":47,
"Switzerland":56,"Belgium":42,"Greece":118,
"Austria":22,"Argentina":21,"Turkey":40
};
function genHLPopQ(){
  if(\!CAPS_POP||CAPS_POP.length<2)return null;
  const _fcp=_rfilt(COUNTRIES,4);const _ccp=new Set(_fcp.map(x=>x.cc));
  let pool=CAPS_POP.filter(x=>x.pop>500000&&_ccp.has(ccFromCountry(x.c)));
  if(pool.length<2)pool=CAPS_POP.filter(x=>x.pop>500000);if(pool.length<2)return null;
  const ai=~~(rng()*pool.length);
  const a=pool[ai];
  const restP=pool.filter((_,i)=>i!==ai);
  const b=getSmartMatch(restP,ccFromCountry(a.c),a.pop,x=>ccFromCountry(x.c),x=>x.pop)||restP[~~(rng()*restP.length)];
  if(!b)return null;
  const fmt=(p)=>p>=1e9?(p/1e9).toFixed(2)+" Mrd.":p>=1e6?(p/1e6).toFixed(1)+" Mio.":(p/1e3).toFixed(0)+" Tsd.";
  const ans=b.pop>a.pop?"higher":"lower";
  return{type:"hl_pop",prompt:t("q_hl_pop",{a:a.c}),nameA:a.c,valA:fmt(a.pop),nameB:b.c,valB:fmt(b.pop),ans,opts:["higher","lower"],lid:b.c,cc:ccFromCountry(b.c)};
}
function genHLRiverQ(){
  if(\!RIVERS_REAL||RIVERS_REAL.length<2)return null;
  const _fcr=_rfilt(COUNTRIES,4);const _ccr=new Set(_fcr.map(x=>x.cc));
  let pool=RIVERS_REAL.filter(r=>r.len>100&&_ccr.has(ccFromCountry(r.c)));
  if(pool.length<2)pool=RIVERS_REAL.filter(r=>r.len>100);if(pool.length<2)return null;
  const ai=~~(rng()*pool.length);
  const a=pool[ai];
  const restR=pool.filter((_,i)=>i!==ai);
  const b=getSmartMatch(restR,a.cc||ccFromCountry(a.c),a.len,x=>x.cc||ccFromCountry(x.c),x=>x.len)||restR[~~(rng()*restR.length)];
  if(!b)return null;
  const ans=b.len>a.len?"higher":"lower";
  return{type:"hl_river",prompt:t("q_hl_river",{a:a.n}),nameA:a.n,valA:a.len+" km",nameB:b.n,valB:b.len+" km",ans,opts:["higher","lower"],lid:b.n,cc:ccFromCountry(b.c)};
}
function genHLAreaQ(){
  if(\!AREA_DATA||AREA_DATA.length<2)return null;
  const _fca=_rfilt(COUNTRIES,4);const _cca=new Set(_fca.map(x=>x.cc));
  let pool=AREA_DATA.filter(x=>_cca.has(ccFromCountry(x.c)));
  if(pool.length<2)pool=AREA_DATA.slice();if(pool.length<2)return null;
  const ai=~~(rng()*pool.length);
  const a=pool[ai];
  const restA2=pool.filter((_,i)=>i!==ai);
  const b=getSmartMatch(restA2,ccFromCountry(a.c),a.area,x=>ccFromCountry(x.c),x=>x.area)||restA2[~~(rng()*restA2.length)];
  if(!b)return null;
  const fmt=(x)=>x>=1e6?(x/1e6).toFixed(2)+" Mio. kmÂ²":(x/1000).toFixed(0)+" Tsd. kmÂ²";
  const ans=b.area>a.area?"higher":"lower";
  return{type:"hl_area",prompt:t("q_hl_area",{a:a.c}),nameA:a.c,valA:fmt(a.area),nameB:b.c,valB:fmt(b.area),ans,opts:["higher","lower"],lid:b.c,cc:ccFromCountry(b.c)};
}

/* ─── HL COMP_DATA generators ─── */
function _genHLComp(type,key,fmtFn,promptKey){
  const keys=Object.keys(COMP_DATA).filter(k=>COMP_DATA[k][key]!=null&&COMP_DATA[k][key]>0);
  if(keys.length<2)return null;
  const ai=~~(rng()*keys.length);
  const kA=keys[ai];
  const vA=COMP_DATA[kA][key];
  const rest=keys.filter(k=>k!==kA);
  const kB=getSmartMatch(rest,ccFromCountry(kA),vA,k=>ccFromCountry(k),k=>COMP_DATA[k][key]);
  if(!kB)return null;
  const vB=COMP_DATA[kB][key];
  const ans=vB>vA?"higher":"lower";
  const dA=displayCountry(ccFromCountry(kA))||kA;
  const dB=displayCountry(ccFromCountry(kB))||kB;
  return{type,prompt:t(promptKey,{a:dA}),subj:dB,nameA:dA,valA:fmtFn(vA),nameB:dB,valB:fmtFn(vB),ans,opts:["higher","lower"],lid:kB,cc:ccFromCountry(kB)};
}
function genHLGdpQ(){return _genHLComp("hl_gdp","gdp",v=>"$"+v.toLocaleString(),"q_hl_gdp");}
function genHLDensityQ(){return _genHLComp("hl_density","dens",v=>v+" Ew/km²","q_hl_density");}
function genHLElevationQ(){return _genHLComp("hl_elevation","elev",v=>v.toLocaleString()+" m","q_hl_elevation");}
function genHLCoastlineQ(){return _genHLComp("hl_coastline","coast",v=>v.toLocaleString()+" km","q_hl_coastline");}
function genHLBordersQ(){return _genHLComp("hl_borders","bord",v=>v+" Länder","q_hl_borders");}
function genHLLifeexpQ(){return _genHLComp("hl_lifeexp","life",v=>v+" Jahre","q_hl_lifeexp");}
function genHLMedianAgeQ(){return _genHLComp("hl_median_age","age",v=>v+" Jahre","q_hl_median_age");}
function genHLForestQ(){return _genHLComp("hl_forest","forest",v=>v+" %","q_hl_forest");}

/* ─── HL BETA DATA (17 Metriken, 15 Laender) ─── */
const HL_BETA_DATA={
  "Deutschland":  {rain:700, temp:10,sun:1700,vulc:0,  parks:16, roads:645000, rail:33400, net:75,  ev:90000, urban:77,lang:1, isl:70,   tz:1, founded:1871,unesco:52,tour:39, wm:20},
  "Frankreich":   {rain:867, temp:12,sun:2000,vulc:0,  parks:11, roads:1100000,rail:29000, net:190, ev:60000, urban:81,lang:1, isl:20,   tz:12,founded:843, unesco:52,tour:90, wm:16},
  "USA":          {rain:715, temp:12,sun:2500,vulc:161,parks:63, roads:6586610,rail:257722,net:242, ev:170000,urban:83,lang:1, isl:18617,tz:11,founded:1776,unesco:24,tour:79, wm:22},
  "Brasilien":    {rain:1761,temp:25,sun:2500,vulc:7,  parks:67, roads:1720700,rail:29850, net:95,  ev:3000,  urban:87,lang:1, isl:10000,tz:4, founded:1822,unesco:23,tour:6,  wm:22},
  "Japan":        {rain:1668,temp:14,sun:1900,vulc:111,parks:34, roads:1218772,rail:27311, net:162, ev:300000,urban:92,lang:1, isl:6852, tz:1, founded:660, unesco:25,tour:32, wm:22},
  "Australien":   {rain:534, temp:22,sun:3200,vulc:3,  parks:685,roads:873573, rail:33343, net:56,  ev:5500,  urban:86,lang:1, isl:8222, tz:8, founded:1901,unesco:20,tour:9,  wm:22},
  "China":        {rain:645, temp:7, sun:2200,vulc:14, parks:56, roads:5200000,rail:150000,net:283, ev:520000,urban:64,lang:7, isl:7600, tz:5, founded:1949,unesco:57,tour:56, wm:16},
  "Kanada":       {rain:537, temp:2, sun:1900,vulc:5,  parks:48, roads:1042300,rail:40000, net:196, ev:20000, urban:82,lang:2, isl:52455,tz:6, founded:1867,unesco:22,tour:22, wm:22},
  "Indien":       {rain:1083,temp:25,sun:2800,vulc:5,  parks:106,roads:5897671,rail:68103, net:50,  ev:6000,  urban:35,lang:22,isl:1208, tz:1, founded:1947,unesco:40,tour:18, wm:12},
  "Russland":     {rain:460, temp:2, sun:1700,vulc:68, parks:112,roads:1283387,rail:86600, net:100, ev:4000,  urban:75,lang:35,isl:600,  tz:11,founded:1991,unesco:30,tour:24, wm:11},
  "Spanien":      {rain:640, temp:14,sun:2800,vulc:3,  parks:15, roads:683175, rail:15333, net:195, ev:20000, urban:81,lang:4, isl:154,  tz:2, founded:1479,unesco:50,tour:84, wm:16},
  "Italien":      {rain:832, temp:14,sun:2300,vulc:14, parks:24, roads:841800, rail:16788, net:30,  ev:36000, urban:71,lang:1, isl:450,  tz:1, founded:1861,unesco:58,tour:57, wm:18},
  "Norwegen":     {rain:1414,temp:2, sun:1600,vulc:0,  parks:47, roads:94902,  rail:3979,  net:228, ev:20000, urban:83,lang:2, isl:50000,tz:1, founded:1814,unesco:8, tour:6,  wm:22},
  "Mexiko":       {rain:758, temp:17,sun:2500,vulc:14, parks:182,roads:374512, rail:20825, net:28,  ev:2000,  urban:81,lang:69,isl:200,  tz:4, founded:1821,unesco:35,tour:45, wm:17},
  "Suedkorea":    {rain:1274,temp:12,sun:2100,vulc:1,  parks:22, roads:100428, rail:3918,  net:312, ev:200000,urban:82,lang:1, isl:3170, tz:1, founded:1948,unesco:16,tour:17, wm:10},
};
const HL_BETA_METRICS={
  hl_b_rain:    {key:"rain",   fmt:function(v){return v+" mm";}},
  hl_b_temp:    {key:"temp",   fmt:function(v){return v+"°C";}},
  hl_b_sun:     {key:"sun",    fmt:function(v){return v+" Std/Jahr";}},
  hl_b_vulc:    {key:"vulc",   fmt:function(v){return v+" Vulkane";}},
  hl_b_parks:   {key:"parks",  fmt:function(v){return v+" Parks";}},
  hl_b_roads:   {key:"roads",  fmt:function(v){return v.toLocaleString()+" km";}},
  hl_b_rail:    {key:"rail",   fmt:function(v){return v.toLocaleString()+" km";}},
  hl_b_net:     {key:"net",    fmt:function(v){return v+" Mbit/s";}},
  hl_b_ev:      {key:"ev",     fmt:function(v){return v.toLocaleString()+" Säulen";}},
  hl_b_urban:   {key:"urban",  fmt:function(v){return v+" %";}},
  hl_b_lang:    {key:"lang",   fmt:function(v){return v+" Amtsspr.";}},
  hl_b_isl:     {key:"isl",    fmt:function(v){return v.toLocaleString()+" Inseln";}},
  hl_b_tz:      {key:"tz",     fmt:function(v){return v+" Zeitzonen";}},
  hl_b_founded: {key:"founded",fmt:function(v){return "gegr. "+v;}},
  hl_b_unesco:  {key:"unesco", fmt:function(v){return v+" Stätten";}},
  hl_b_tour:    {key:"tour",   fmt:function(v){return v+" Mio.";}},
  hl_b_wm:      {key:"wm",     fmt:function(v){return v+"x WM";}},
};
const HL_BETA_PROMPTS={
  hl_b_rain:"Welches Land hat mehr Jahresniederschlag?",
  hl_b_temp:"Welches Land ist wärmer im Jahresschnitt?",
  hl_b_sun:"Welches Land hat mehr Sonnenstunden?",
  hl_b_vulc:"Welches Land hat mehr aktive Vulkane?",
  hl_b_parks:"Welches Land hat mehr Nationalparks?",
  hl_b_roads:"Welches Land hat das längere Straßennetz?",
  hl_b_rail:"Welches Land hat das längere Schienennetz?",
  hl_b_net:"Welches Land hat schnelleres Internet?",
  hl_b_ev:"Welches Land hat mehr E-Ladesäulen?",
  hl_b_urban:"Welches Land ist stärker urbanisiert?",
  hl_b_lang:"Welches Land hat mehr Amtssprachen?",
  hl_b_isl:"Welches Land hat mehr Inseln?",
  hl_b_tz:"Welches Land hat mehr Zeitzonen?",
  hl_b_founded:"Welches Land ist älter?",
  hl_b_unesco:"Welches Land hat mehr UNESCO-Welterbe?",
  hl_b_tour:"Welches Land hat mehr Touristen?",
  hl_b_wm:"Welches Land hat mehr WM-Teilnahmen?",
};

/* ─── Phase 160: CC-Map für HL_BETA_DATA (German name → ISO-2) ─── */
const HL_BETA_CC={
  "Deutschland":"de","Frankreich":"fr","USA":"us","Brasilien":"br","Japan":"jp",
  "Australien":"au","China":"cn","Kanada":"ca","Indien":"in","Russland":"ru",
  "Spanien":"es","Italien":"it","Norwegen":"no","Mexiko":"mx","Suedkorea":"kr"
};

/* ─── Phase 160: Smart Matchmaking Helper ─── */
/* Wählt einen Vergleichspartner aus candidates[] mit:
   Prio 1 – gleicher Kontinent (via COUNTRIES.ct)
   Prio 2 – numerische Nähe (|valA - valK| sortiert, Top-8)
   ccFn(candidate) → ISO-2  |  valFn(candidate) → Zahl              */
function getSmartMatch(candidates,ccA,valA,ccFn,valFn){
  if(!candidates||candidates.length===0)return null;
  const ctA=ccA?(COUNTRIES.find(c=>c.cc===ccA)||{}).ct:null;
  let pool=candidates;
  if(ctA&&candidates.length>3){
    const sameC=candidates.filter(k=>{
      const cc2=ccFn(k);
      return cc2&&(COUNTRIES.find(c=>c.cc===cc2)||{}).ct===ctA;
    });
    if(sameC.length>=2)pool=sameC;
  }
  if(valA!=null&&pool.length>2){
    pool=pool.slice().sort((a,b)=>
      Math.abs(valFn(a)-valA)-Math.abs(valFn(b)-valA)
    ).slice(0,8);
  }
  return pool[~~(rng()*pool.length)];
}
function genHLBeta(modeId){
  const m=HL_BETA_METRICS[modeId];if(!m)return null;
  const countries=Object.keys(HL_BETA_DATA).filter(k=>HL_BETA_DATA[k][m.key]!=null);
  if(countries.length<2)return null;
  const ai=~~(rng()*countries.length);
  const kA=countries[ai];
  const vA=HL_BETA_DATA[kA][m.key];
  const rest=countries.filter(k=>k!==kA);
  const kB=getSmartMatch(rest,HL_BETA_CC[kA]||null,vA,k=>HL_BETA_CC[k]||null,k=>HL_BETA_DATA[k][m.key]);
  if(!kB)return null;
  const vB=HL_BETA_DATA[kB][m.key];
  const isOlder=modeId==="hl_b_founded";
  const ans=isOlder?(vA<vB?kA:kB):(vA>vB?kA:kB);
  const prompt="\u{1F9EA} [BETA] "+(HL_BETA_PROMPTS[modeId]||"Vergleich?");
  const meta=kA+": "+m.fmt(vA)+" · "+kB+": "+m.fmt(vB);
  return{type:modeId,prompt,subj:"",opts:[kA,kB],ans,meta,lid:kA+"|"+kB,cc:ccFromCountry(ans)||"de"};
}
/* Phase 95: inline area (kmÂ²) + population (millions) – self-contained, no external files */
const COMP_AREA={
"Afghanistan":652230,"Algeria":2381741,"Angola":1246700,"Argentina":2780400,
"Australia":7692024,"Austria":83871,"Bangladesh":147570,"Belgium":30528,
"Bolivia":1098581,"Botswana":581730,"Brazil":8515767,"Bulgaria":110879,
"Cambodia":181035,"Canada":9984670,"Chile":756102,"China":9596960,
"Colombia":1141748,"Costa Rica":51100,"Croatia":56594,"Cuba":109884,
"Czech Republic":78866,"Denmark":42924,"DR Congo":2344858,"Ecuador":283561,
"Egypt":1001450,"Estonia":45228,"Ethiopia":1104300,"Finland":338145,
"France":643801,"Germany":357114,"Ghana":238533,"Greece":131957,
"Guatemala":108889,"Hungary":93028,"Iceland":103000,"India":3287263,
"Indonesia":1904569,"Iran":1648195,"Iraq":438317,"Ireland":70273,
"Israel":20770,"Italy":301340,"Ivory Coast":322463,"Japan":377930,
"Jordan":89342,"Kazakhstan":2724900,"Kenya":580367,"Laos":236800,
"Latvia":64589,"Lithuania":65300,"Malaysia":329847,"Mali":1240192,
"Mexico":1964375,"Mongolia":1564116,"Morocco":446550,"Myanmar":676578,
"Namibia":824292,"Nepal":147181,"Netherlands":41543,"New Zealand":270467,
"Nigeria":923768,"Norway":385207,"Pakistan":881913,"Paraguay":406752,
"Peru":1285216,"Philippines":300000,"Poland":312679,"Portugal":92212,
"Romania":238397,"Russia":17098242,"Saudi Arabia":2149690,"Senegal":196722,
"Serbia":77474,"Singapore":724,"Slovakia":49035,"South Africa":1219090,
"South Korea":100210,"Spain":505990,"Sri Lanka":65610,"Sudan":1861484,
"Sweden":450295,"Switzerland":41285,"Taiwan":36193,"Tanzania":945087,
"Thailand":513120,"Turkey":783562,"UAE":83600,"Uganda":241038,
"Ukraine":603550,"United Kingdom":243610,"United States":9833517,
"Uruguay":176215,"Venezuela":916445,"Vietnam":331212
};
/* COMP_POP values in millions */
const COMP_POP={
"Afghanistan":41.1,"Algeria":45.6,"Angola":35.6,"Argentina":46.3,
"Australia":26.5,"Austria":9.1,"Bangladesh":169.4,"Belgium":11.6,
"Bolivia":12.1,"Botswana":2.6,"Brazil":215.3,"Bulgaria":6.5,
"Cambodia":17.0,"Canada":38.2,"Chile":19.6,"China":1412.0,
"Colombia":51.8,"Costa Rica":5.2,"Croatia":3.9,"Cuba":11.1,
"Czech Republic":10.8,"Denmark":5.9,"DR Congo":99.0,"Ecuador":18.1,
"Egypt":104.1,"Estonia":1.3,"Ethiopia":123.4,"Finland":5.5,
"France":68.0,"Germany":84.1,"Ghana":33.5,"Greece":10.5,
"Guatemala":17.6,"Hungary":9.7,"Iceland":0.37,"India":1407.6,
"Indonesia":277.5,"Iran":87.9,"Iraq":42.3,"Ireland":5.1,
"Israel":9.2,"Italy":59.3,"Ivory Coast":27.5,"Japan":124.5,
"Jordan":10.2,"Kazakhstan":19.6,"Kenya":54.0,"Laos":7.4,
"Latvia":1.8,"Lithuania":2.8,"Malaysia":33.6,"Mali":22.4,
"Mexico":130.0,"Mongolia":3.4,"Morocco":37.5,"Myanmar":54.4,
"Namibia":2.7,"Nepal":29.2,"Netherlands":17.9,"New Zealand":5.1,
"Nigeria":218.5,"Norway":5.5,"Pakistan":231.4,"Paraguay":7.4,
"Peru":33.4,"Philippines":115.6,"Poland":37.7,"Portugal":10.3,
"Romania":18.9,"Russia":144.0,"Saudi Arabia":35.4,"Senegal":17.2,
"Serbia":6.8,"Singapore":5.9,"Slovakia":5.5,"South Africa":60.6,
"South Korea":51.9,"Spain":47.7,"Sri Lanka":22.2,"Sudan":46.9,
"Sweden":10.6,"Switzerland":8.7,"Taiwan":23.5,"Tanzania":63.3,
"Thailand":71.8,"Turkey":85.3,"UAE":9.9,"Uganda":47.1,
"Ukraine":43.5,"United Kingdom":67.7,"United States":335.0,
"Uruguay":3.5,"Venezuela":29.8,"Vietnam":98.5
};
/* Phase 91+92: _compPick/_compQ helpers + 11 comp_* generators */
function _compPick(key,filterFn){
  const _fc=_rfilt(COUNTRIES,4);const _cc=new Set(_fc.map(x=>x.cc));
  let pool=Object.keys(COMP_DATA).filter(k=>{
    const d=COMP_DATA[k];
    return d&&d[key]!==undefined&&_cc.has(ccFromCountry(k))&&(!filterFn||filterFn(d));
  });
  if(pool.length<2)pool=Object.keys(COMP_DATA).filter(k=>{const d=COMP_DATA[k];return d&&d[key]!==undefined&&(!filterFn||filterFn(d));});
  if(pool.length<2)return null;
  const ai=~~(rng()*pool.length);
  const kA=pool[ai];
  const restC=pool.filter(k=>k!==kA);
  const kB=getSmartMatch(restC,ccFromCountry(kA),COMP_DATA[kA]&&COMP_DATA[kA][key],k=>ccFromCountry(k),k=>COMP_DATA[k]&&COMP_DATA[k][key]);
  if(!kB)return null;
  return[kA,kB];
}
function _compQ(type,prompt,a,b,aVal,bVal,fmtFn){
  const ans=bVal>aVal?b:a;
  const meta=displayCountry(a)+': '+fmtFn(aVal)+' · '+displayCountry(b)+': '+fmtFn(bVal);
  return{type,prompt,subj:'',opts:[a,b],ans,meta,lid:a+'|'+b,cc:ccFromCountry(ans)};
}
function genCompAreaQ(){
  /* Phase 95: uses inline COMP_AREA – no external file needed */
  const keys=Object.keys(COMP_AREA);
  if(keys.length<2)return null;
  const _fc=_rfilt(COUNTRIES,4);const _cc=new Set(_fc.map(x=>x.cc));
  let pool=keys.filter(k=>_cc.has(ccFromCountry(k)));
  if(pool.length<2)pool=keys.slice();if(pool.length<2)return null;
  const ai=~~(rng()*pool.length);
  const a=pool[ai];
  const restCA=pool.filter(k=>k!==a);
  const b=getSmartMatch(restCA,ccFromCountry(a),COMP_AREA[a],k=>ccFromCountry(k),k=>COMP_AREA[k]);
  if(!b)return null;
  const fmt=(x)=>x>=1e6?(x/1e6).toFixed(2)+' Mio. kmÂ²':(x/1000).toFixed(0)+' Tsd. kmÂ²';
  return _compQ('comp_area','Welches Land ist größer?',a,b,COMP_AREA[a],COMP_AREA[b],fmt);
}
function genCompPopQ(){
  /* Phase 95: uses inline COMP_POP (millions) – no external file needed */
  const keys=Object.keys(COMP_POP);
  if(keys.length<2)return null;
  const _fc=_rfilt(COUNTRIES,4);const _cc=new Set(_fc.map(x=>x.cc));
  let pool=keys.filter(k=>COMP_POP[k]>0.5&&_cc.has(ccFromCountry(k)));
  if(pool.length<2)pool=keys.filter(k=>COMP_POP[k]>0.5);if(pool.length<2)return null;
  const ai=~~(rng()*pool.length);
  const a=pool[ai];
  const restCP=pool.filter(k=>k!==a);
  const b=getSmartMatch(restCP,ccFromCountry(a),COMP_POP[a],k=>ccFromCountry(k),k=>COMP_POP[k]);
  if(!b)return null;
  const pa=COMP_POP[a]*1e6,pb=COMP_POP[b]*1e6;
  const fmt=(p)=>p>=1e9?(p/1e9).toFixed(2)+' Mrd.':p>=1e6?(p/1e6).toFixed(1)+' Mio.':(p/1e3).toFixed(0)+' Tsd.';
  return _compQ('comp_pop','Welches Land hat mehr Einwohner?',a,b,pa,pb,fmt);
}
function genCompNorthQ(){
  const r=_compPick('lat',null);if(!r)return null;
  const[a,b]=r;
  if(COMP_DATA[a].lat===COMP_DATA[b].lat)return null;
  const fmt=(x)=>Math.abs(x).toFixed(0)+'Â° '+(x>=0?'N':'S');
  return _compQ('comp_north','Welches Land liegt weiter nördlich?',a,b,COMP_DATA[a].lat,COMP_DATA[b].lat,fmt);
}
function genCompGdpQ(){
  const r=_compPick('gdp',null);if(!r)return null;
  const[a,b]=r;
  if(COMP_DATA[a].gdp===COMP_DATA[b].gdp)return null;
  const fmt=(x)=>'$ '+(x>=1000?(x/1000).toFixed(0)+' Tsd.':x);
  return _compQ('comp_gdp','Welches Land hat ein höheres BIP pro Kopf?',a,b,COMP_DATA[a].gdp,COMP_DATA[b].gdp,fmt);
}
function genCompDensityQ(){
  const r=_compPick('dens',null);if(!r)return null;
  const[a,b]=r;
  if(COMP_DATA[a].dens===COMP_DATA[b].dens)return null;
  const fmt=(x)=>x+' Einw./kmÂ²';
  return _compQ('comp_density','Welches Land ist dichter besiedelt?',a,b,COMP_DATA[a].dens,COMP_DATA[b].dens,fmt);
}
function genCompElevQ(){
  const r=_compPick('elev',null);if(!r)return null;
  const[a,b]=r;
  if(COMP_DATA[a].elev===COMP_DATA[b].elev)return null;
  const fmt=(x)=>x.toLocaleString('de-DE')+' m';
  return _compQ('comp_elevation','Welches Land hat den höheren Gipfel?',a,b,COMP_DATA[a].elev,COMP_DATA[b].elev,fmt);
}
function genCompCoastQ(){
  const r=_compPick('coast',d=>d.coast>0);if(!r)return null;
  const[a,b]=r;
  if(COMP_DATA[a].coast===COMP_DATA[b].coast)return null;
  const fmt=(x)=>x.toLocaleString('de-DE')+' km';
  return _compQ('comp_coast','Welches Land hat die längere Küste?',a,b,COMP_DATA[a].coast,COMP_DATA[b].coast,fmt);
}
function genCompBordersQ(){
  const r=_compPick('bord',d=>d.bord>0);if(!r)return null;
  const[a,b]=r;
  if(COMP_DATA[a].bord===COMP_DATA[b].bord)return null;
  const fmt=(x)=>x+' Nachbarn';
  return _compQ('comp_borders','Welches Land hat mehr Nachbarländer?',a,b,COMP_DATA[a].bord,COMP_DATA[b].bord,fmt);
}
function genCompLifeQ(){
  const r=_compPick('life',null);if(!r)return null;
  const[a,b]=r;
  if(COMP_DATA[a].life===COMP_DATA[b].life)return null;
  const fmt=(x)=>x+' Jahre';
  return _compQ('comp_life','In welchem Land lebt man länger?',a,b,COMP_DATA[a].life,COMP_DATA[b].life,fmt);
}
function genCompAgeQ(){
  const r=_compPick('age',null);if(!r)return null;
  const[a,b]=r;
  if(COMP_DATA[a].age===COMP_DATA[b].age)return null;
  const fmt=(x)=>x+' Jahre';
  return _compQ('comp_age','Welches Land hat ein höheres Medianalter?',a,b,COMP_DATA[a].age,COMP_DATA[b].age,fmt);
}
function genCompForestQ(){
  const r=_compPick('forest',null);if(!r)return null;
  const[a,b]=r;
  if(COMP_DATA[a].forest===COMP_DATA[b].forest)return null;
  const fmt=(x)=>x+' %';
  return _compQ('comp_forest','Welches Land hat mehr Waldfläche?',a,b,COMP_DATA[a].forest,COMP_DATA[b].forest,fmt);
}
function genNeighborQ(){
  const nb=NEIGHBORS;const valid=Object.keys(nb).filter(c=>Array.isArray(nb[c])&&nb[c].length>=2);if(\!valid.length)return null;
  const country=valid[~~(rng()*valid.length)];const neighborList=Array.isArray(nb[country])?nb[country]:[];
  const allC=Object.keys(nb);const nonNb=allC.filter(c=>c\!==country&&\!neighborList.includes(c));if(\!nonNb.length)return null;
  const type2=rng()>.5;
  if(type2&&neighborList.length>=2){
    const ans=nonNb[~~(rng()*nonNb.length)];
    const dis=neighborList.slice().sort(()=>rng()-.5).slice(0,2);
    return{type:"neighbor",prompt:"Grenzt NICHT an\u2026?",subj:country,ans,opts:sh([ans,...dis]),lid:country+'|'+ans,cc:ccFromCountry(country)||''};
  }else{
    const ans=neighborList[~~(rng()*neighborList.length)];
    const dis=nonNb.slice().sort(()=>rng()-.5).slice(0,3);
    return{type:"neighbor",prompt:"Welches Land grenzt an…?",subj:country,ans,opts:sh([ans,...dis.slice(0,3)]),lid:country+'|'+ans,cc:ccFromCountry(country)||''};
  }
}

function genNeighborFakeQ(){
  const nb=NEIGHBORS;
  const valid=Object.keys(nb).filter(c=>Array.isArray(nb[c])&&nb[c].length>=3);
  if(\!valid.length)return null;
  const country=valid[~~(rng()*valid.length)];
  const neighbors=Array.isArray(nb[country])?nb[country]:[];
  const realNbs=sh([...neighbors]).slice(0,3);
  const allKeys=Object.keys(nb);
  const basePool=allKeys.filter(c=>c\!==country&&\!neighbors.includes(c));
  /* Build name→cc lookup for both English and current-language names */
  const _n2cc={};
  COUNTRIES.forEach(c=>{_n2cc[c.c]=c.cc;const dn=displayCountry(c.cc);if(dn)_n2cc[dn]=c.cc;});
  const _ccT=_n2cc[country];
  const _ctT=_ccT?(COUNTRIES.find(c=>c.cc===_ccT)||{}).ct:null;
  /* Filter to same continent; fall back to global pool if needed */
  let fakePool=basePool;
  if(_ctT){
    const sameC=basePool.filter(c=>{
      const _cc2=_n2cc[c];
      return _cc2&&(COUNTRIES.find(x=>x.cc===_cc2)||{}).ct===_ctT;
    });
    if(sameC.length>=1)fakePool=sameC;
  }
  if(\!fakePool.length)return null;
  const fake=fakePool[~~(rng()*fakePool.length)];
  return{type:"neighbor_fake",prompt:"Welches Land grenzt NICHT an …?",
    subj:country,ans:fake,opts:sh([...realNbs,fake]),meta:"",
    lid:country+'|fake|'+fake,cc:_ccT||''};
}

function genNeighborCountQ(){
  const nb=NEIGHBORS;
  const valid=Object.keys(nb).filter(c=>nb[c]&&nb[c].length>0);
  if(valid.length<4)return null;
  const country=valid[~~(rng()*valid.length)];
  const realCount=nb[country].length;
  const wrongs=new Set();
  let att=0;
  while(wrongs.size<3&&att<60){att++;const w=Math.max(0,realCount+~~(rng()*7)-3);if(w\!==realCount)wrongs.add(w);}
  const opts=sh([String(realCount),...[...wrongs].map(String)]);
  const meta=nb[country].slice(0,5).join(", ")+(nb[country].length>5?"…":"");
  return{type:"neighbor_count",prompt:"Wie viele Nachbarländer hat dieses Land?",
    subj:country,ans:String(realCount),opts,meta,lid:country+'|count',cc:ccFromCountry(country)||''};
}

/* •••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••
   PHASE 33 – REALTIME 1vs1 MULTIPLAYER  (Supabase Broadcast)
   ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••• */

/* Helpers */
function mpCode(){let c="";const chars="ABCDEFGHJKLMNPQRSTUVWXYZ23456789";for(let i=0;i<4;i++)c+=chars[~~(Math.random()*chars.length)];return c;}
function mpLog(...a){console.log("[MP]",...a);}

/* Close and clean up current channel */
function mpLeave(){
  if(S.mp?.channel)try{S.mp.channel.unsubscribe();}catch(e){}
  S.mp=null;S.mpModal=false;render();
}

/* Send a broadcast on the current channel */
function mpSend(event,payload){
  if(\!S.mp?.channel)return;
  S.mp.channel.send({type:"broadcast",event,payload});
}

/* Countdown then start */
function mpCountdown(seed,mode){
  let t=3;
  S.mp.phase="countdown";S.mp.countdown=t;render();
  const iv=setInterval(()=>{
    t--;S.mp.countdown=t;
    if(t<=0){
      clearInterval(iv);
      S.mpModal=false;
      /* Phase 33 Teil 2: keep channel alive for in-game score sync */
      const _ch=S.mp.channel,_oppName=S.mp.oppName||"Gegner";
      window.mpGameCh=_ch;
      _ch.on("broadcast",{event:"score_update"},({payload})=>{
        S.mpOppScore=payload.score||0;S.mpOppRd=payload.rd||0;render();
      }).on("broadcast",{event:"game_over"},({payload})=>{
        S.mpOppFinal=payload;
        if(S.ph==="gameover")render();
      });
      S.mp=null;
      /* Sync start – same seed on both sides */
      initRng(seed);
      startGame(mode||"city");
      /* Tag session as multiplayer */
      S.mpSeed=seed;S.mpOpponent=_oppName;
      S.mpOppScore=0;S.mpOppRd=0;S.mpOppFinal=null;
    }else {}
  },1000);
}

/* HOST: create room */
function mpCreate(){
  if(\!sb){showToast("Supabase nicht verbunden\!");return;}
  const code=mpCode();
  let channel;
  try{
    channel=sb.channel("room_"+code,{config:{broadcast:{self:false}}});
  }catch(e){
    showToast("\u26a0\ufe0f Verbindungsfehler: "+e.message);
    console.error("mpCreate channel error:",e);
    return;
  }
  S.mp={role:"host",code,channel,phase:"waiting",myReady:false,oppReady:false,oppName:null};
  render();

  channel
    .on("broadcast",{event:"player_joined"},({payload})=>{
      mpLog("guest joined:",payload);
      S.mp.oppName=payload.name||"Gast";
      S.mp.phase="ready";
      render();
      /* Acknowledge the join */
      mpSend("host_ack",{name:sbProfile?.username||"Host"});
    })
    .on("broadcast",{event:"player_ready"},({payload})=>{
      mpLog("guest ready");
      S.mp.oppReady=true;render();
      if(S.mp.myReady&&S.mp.oppReady){
        const seed=~~(Math.random()*1e9);
        const _rm=S.mode||"city";const mode=(MODES.find(m=>m.id===_rm)?.noMultiplayer)?"city":_rm;
        mpSend("game_start",{seed,mode});
        mpCountdown(seed,mode);
      }
    })
    .on("broadcast",{event:"game_start"},()=>{/* host ignores own game_start */})
    .subscribe((status)=>{
      mpLog("host channel status:",status);
      if(status==="SUBSCRIBED")render();
    });
}

/* GUEST: join room */
function mpJoin(code){
  if(\!sb){showToast("Supabase nicht verbunden\!");return;}
  if(\!code||code.length<4){showToast("Bitte gültigen Code eingeben\!");return;}
  const uc=code.toUpperCase().trim();
  let channel;
  try{
    channel=sb.channel("room_"+uc,{config:{broadcast:{self:false}}});
  }catch(e){
    showToast("\u26a0\ufe0f Verbindungsfehler: "+e.message);
    return;
  }
  S.mp={role:"guest",code:uc,channel,phase:"joining",myReady:false,oppReady:false,oppName:null};
  render();

  channel
    .on("broadcast",{event:"host_ack"},({payload})=>{
      mpLog("host ack:",payload);
      S.mp.oppName=payload.name||"Host";
      S.mp.phase="ready";render();
    })
    .on("broadcast",{event:"player_ready"},()=>{
      S.mp.oppReady=true;render();
    })
    .on("broadcast",{event:"game_start"},({payload})=>{
      mpLog("game_start received:",payload);
      mpCountdown(payload.seed,payload.mode);
    })
    .subscribe((status)=>{
      mpLog("guest channel status:",status);
      if(status==="SUBSCRIBED"){
        mpSend("player_joined",{name:sbProfile?.username||"Spieler"});
        render();
      }
    });
}

/* Ready button */
function mpReady(){
  S.mp.myReady=true;render();
  mpSend("player_ready",{name:sbProfile?.username||"Ich"});
  /* Host: if guest was already ready */
  if(S.mp.role==="host"&&S.mp.oppReady){
    const seed=~~(Math.random()*1e9);
    const _rm=S.mode||"city";const mode=(MODES.find(m=>m.id===_rm)?.noMultiplayer)?"city":_rm;
    mpSend("game_start",{seed,mode});
    mpCountdown(seed,mode);
  }
}

/* Render the full lobby modal */
function renderMultiplayerLobby(){
  const mp=S.mp;

  /* â”€â”€ Phase: initial (no room yet) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
  if(\!mp){
    const joinInput=S._mpJoinCode||"";
    return`<div class="scr">
      <div style="text-align:center;margin-bottom:1.4rem;padding-top:.5rem">
        <div class="mp-lobby-title">\u2694\ufe0f Live 1vs1 Duell</div>
        <div style="color:var(--text3);font-size:.8rem;margin-top:.25rem">Spiele live gegen einen Freund</div>
      </div>
      <div style="background:var(--bg2);border:1.5px solid var(--border);border-radius:16px;padding:1.4rem;margin-bottom:1rem;text-align:center">
        <div style="font-size:2.5rem;margin-bottom:.5rem">\u{1F3E0}</div>
        <div style="font-weight:900;font-size:1rem;color:var(--text);margin-bottom:.35rem">Spiel erstellen</div>
        <div style="color:var(--text3);font-size:.78rem;margin-bottom:.9rem">Generiere einen Code und lade einen Freund ein</div>
        <button class="btn-p" style="width:100%" onclick="mpCreate()">âž• Neues Spiel erstellen</button>
      </div>
      <div style="background:var(--bg2);border:1.5px solid var(--border);border-radius:16px;padding:1.4rem;text-align:center">
        <div style="font-size:2.5rem;margin-bottom:.5rem">\u{1F517}</div>
        <div style="font-weight:900;font-size:1rem;color:var(--text);margin-bottom:.35rem">Mit Code beitreten</div>
        <div style="color:var(--text3);font-size:.78rem;margin-bottom:.9rem">Gib den 4-stelligen Code deines Freundes ein</div>
        <div style="display:flex;gap:8px">
          <input type="text" maxlength="4" placeholder="z.B. A7B2" value="${esc(joinInput)}"
            oninput="S._mpJoinCode=this.value.toUpperCase();this.value=this.value.toUpperCase()"
            style="flex:1;font-size:1.2rem;font-weight:900;text-align:center;letter-spacing:4px;text-transform:uppercase">
          <button class="btn-p" style="width:auto;padding:.6rem 1.2rem" onclick="mpJoin(S._mpJoinCode)">→¶</button>
        </div>
      </div>
      <button class="mp-back-btn" onclick="S.mpModal=false;render()">\u2b05\ufe0f Zurück zum Hauptmenü</button>
    </div>`;
  }

  /* â”€â”€ Phase: host waiting for guest â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
  if(mp.phase==="waiting"){
    return`<div class="scr" style="text-align:center">
      <button class="mp-back-btn" style="margin-bottom:.5rem" onclick="mpLeave()">\u2b05\ufe0f Abbrechen</button>
      <div style="clear:both;padding-top:.5rem"></div>
      <div style="font-size:3rem;margin:1rem 0">\u{1F4F1}</div>
      <h2 style="font-size:1.3rem;font-weight:900;color:var(--text);margin-bottom:.5rem">Warte auf Gegner…</h2>
      <p style="color:var(--text3);font-size:.82rem;margin-bottom:1.4rem">Gib diesen Code an deinen Freund:</p>
      <div style="display:inline-block;background:var(--bg3);border:3px solid #7c3aed;border-radius:16px;padding:1rem 2rem;font-size:3rem;font-weight:900;letter-spacing:10px;color:#7c3aed;margin-bottom:1rem">${esc(mp.code)}</div>
      <p style="color:var(--text3);font-size:.74rem">Verbunden – Channel aktiv</p>
      <div style="margin-top:1.5rem;display:flex;justify-content:center">
        <div class="spinner"></div>
      </div>
    </div>`;
  }

  /* â”€â”€ Phase: guest joining â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
  if(mp.phase==="joining"){
    return`<div class="scr" style="text-align:center">
      <div style="font-size:3rem;margin:2rem 0">\u{1F50D}</div>
      <h2 style="font-size:1.2rem;font-weight:900;color:var(--text)">Verbinde mit Raum ${esc(mp.code)}…</h2>
      <div style="margin-top:1.5rem;display:flex;justify-content:center"><div class="spinner"></div></div>
    </div>`;
  }

  /* â”€â”€ Phase: both in room – ready check â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
  if(mp.phase==="ready"){
    const myR=mp.myReady,oppR=mp.oppReady;
    return`<div class="scr" style="text-align:center">
      <button class="mp-back-btn" style="margin-bottom:.5rem" onclick="mpLeave()">\u2b05\ufe0f Abbrechen</button>
      <div style="clear:both;padding-top:.5rem"></div>
      <div style="font-size:2.5rem;margin:.6rem 0">\u{1F7E2}</div>
      <h2 style="font-size:1.2rem;font-weight:900;color:var(--text);margin-bottom:.3rem">Gegner gefunden\!</h2>
      <p style="color:var(--text3);font-size:.8rem;margin-bottom:1.2rem">Gegner: <strong>${esc(mp.oppName||"Unbekannt")}</strong></p>
      <div style="display:flex;gap:12px;justify-content:center;margin-bottom:1.4rem">
        <div style="background:var(--bg2);border:2px solid ${myR?"#10b981":"var(--border)"};border-radius:12px;padding:.75rem 1.2rem;min-width:100px">
          <div style="font-size:1.3rem">${myR?"✓…":"â³"}</div>
          <div style="font-size:.72rem;color:var(--text3);margin-top:4px">Du</div>
        </div>
        <div style="font-size:1.4rem;align-self:center;color:var(--text3)">VS</div>
        <div style="background:var(--bg2);border:2px solid ${oppR?"#10b981":"var(--border)"};border-radius:12px;padding:.75rem 1.2rem;min-width:100px">
          <div style="font-size:1.3rem">${oppR?"✓…":"â³"}</div>
          <div style="font-size:.72rem;color:var(--text3);margin-top:4px">${esc(mp.oppName||"Gegner")}</div>
        </div>
      </div>
      ${myR?`<div style="color:var(--text3);font-size:.82rem">Warte auf ${esc(mp.oppName||"Gegner")}…</div>`
           :`<button class="btn-p" style="width:100%;font-size:1.1rem" onclick="mpReady()">\u{1F3C1} Bereit\!</button>`}
    </div>`;
  }

  /* â”€â”€ Phase: countdown â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
  if(mp.phase==="countdown"){
    return`<div class="scr" style="text-align:center;padding-top:30%">
      <div style="font-size:6rem;font-weight:900;color:#7c3aed;line-height:1">${mp.countdown}</div>
      <div style="color:var(--text2);font-size:1rem;margin-top:.8rem">Spiel startet…</div>
    </div>`;
  }

  return`<div class="scr"><button onclick="mpLeave()">→ ${t("btn_back")}</button></div>`;
}

/* ACHIEVEMENTS */
const ACHIEVEMENTS=[
  {id:"first_blood", icon:"\u{1F3AF}", title:"Erster Treffer",    desc:"Erste richtige Antwort", check:(S,h)=>h.some(g=>g.correct>0)},
  {id:"streak5",     icon:"\u{1F525}", title:"On Fire",           desc:"Streak von 5 erreicht",  check:(S,h)=>h.some(g=>g.best_streak>=5)},
  {id:"streak10",    icon:"\u{1F4A5}", title:"Legendar",          desc:"Streak von 10 erreicht", check:(S,h)=>h.some(g=>g.best_streak>=10)},
  {id:"perfect",     icon:"\u{1F947}", title:"Makellos",          desc:"10/10 in einer Runde",   check:(S,h)=>h.some(g=>g.correct===10&&g.rounds===10)},
  {id:"globetrotter",icon:"\u{1F30D}", title:"Globetrotter",      desc:"20 Laender gestempelt",  check:(S,h)=>{const m=loadMastery();return Object.values(m).filter(v=>getMasteryRank(v.v,v.p)).length>=20;}},
  {id:"daily3",      icon:"\u{1F4C5}", title:"Daily Habit",       desc:"3 Daily Challenges",     check:(S,h)=>getDailyStreakCount()>=3},
  {id:"plates_ace",  icon:"\u{1F697}", title:"Kennzeichen-Ass",   desc:"Kennzeichen-Runde gespielt",check:(S,h)=>h.some(g=>g.mode==="plate_casual"||g.mode==="plate_hard")},
  {id:"hc_victory",  icon:"\u{1F94B}", title:"Hardcore-Sieger",   desc:"Hardcore-Runde >1500 Pkt",check:(S,h)=>h.some(g=>g.score>1500&&g.mode&&(localStorage.getItem("gq_hc_"+g.date)||g.diff==="hardcore"))},
];

function getDailyStreakCount(){
  let count=0;const today=new Date();
  for(let i=0;i<30;i++){const d=new Date(today);d.setDate(d.getDate()-i);const k="gq_daily_"+d.toISOString().slice(0,10);if(localStorage.getItem(k))count++;else break;}
  return count;
}

function loadUnlocked(){return _gqLoad("gq_unlocked",["pure_geo"]);}
function saveUnlocked(arr){_gqSave("gq_unlocked",arr);}
function isCategoryUnlocked(catId){return true;/* TEST MODE – all categories unlocked */}
function buyCategory(catId){
  if(!sb||!sbUser?.id){showToast("Bitte einloggen\!"); return;}
  const cat=MODE_CATS[catId];if(!cat)return;
  const coins=sbProfile?.geo_coins||0;
  if(coins<cat.cost){showToast("Zu wenig GeoCoins\!");return;}
  if(sbProfile)sbProfile.geo_coins=coins-cat.cost;
  const arr=loadUnlocked();if(\!arr.includes(catId))arr.push(catId);saveUnlocked(arr);
  if(sb&&sbUser){sb.rpc("spend_coins",{p_user_id:sbUser.id,p_amount:cat.cost}).then(r=>{if(r.data!=null&&sbProfile)sbProfile.geo_coins=r.data;},()=>{});}
  showConfetti();S.lockModal=null;render();
}
function showConfetti(){
  const colors=["#f59e0b","#10b981","#60a5fa","#f472b6","#a78bfa","#34d399"];
  for(let i=0;i<60;i++){const d=document.createElement("div");d.className="confetti-piece";d.style.left=Math.random()*100+"vw";d.style.background=colors[i%colors.length];d.style.animationDelay=Math.random()*1.5+"s";d.style.borderRadius=Math.random()>.5?"50%":"2px";document.body.appendChild(d);setTimeout(()=>d.remove(),3000);}
}
function renderLockModal(catId){
  const cat=MODE_CATS[catId];if(\!cat)return"";
  const coins=sbProfile?.geo_coins||0;const enough=coins>=cat.cost;
  return`<div class="modal-overlay" onclick="if(event.target===this){S.lockModal=null;render()}">
    <div class="modal-box">
      <div style="font-size:2.5rem;margin-bottom:.5rem">${cat.icon}</div>
      <div style="font-size:1.1rem;font-weight:900;margin-bottom:4px;color:var(--text)">${cat.label}</div>
      <div style="color:var(--text3);font-size:.82rem;margin-bottom:1rem">Diese Kategorie freischalten</div>
      <div style="background:var(--bg3);border-radius:12px;padding:.85rem;margin-bottom:1rem;text-align:center">
        <div style="color:var(--text3);font-size:.68rem;margin-bottom:3px">KOSTEN</div>
        <div style="font-size:1.8rem;font-weight:900;color:#fbbf24">\u{1F4B0} ${cat.cost.toLocaleString()}</div>
        <div style="font-size:.7rem;color:${enough?"#34d399":"#f87171"};margin-top:4px">${enough?"Du hast genug Coins \u2713":"Du hast nur "+coins+" Coins"}</div>
      </div>
      ${sbProfile?.is_premium?`<div style="color:#34d399;font-size:.82rem;margin-bottom:.85rem">\u{1F451} Premium: Diese Kategorie ist kostenlos\!</div>`:""}
      <button class="btn-p" onclick="buyCategory('${catId}')" ${(\!enough&&\!sbProfile?.is_premium)?"disabled":""}>
        ${sbProfile?.is_premium?"Kostenlos freischalten":"\u{1F4B0} "+cat.cost+" Coins ausgeben"}
      </button>
      <button class="btn-g" style="margin-bottom:0" onclick="S.payModal=true;S.lockModal=null;render()">\u{1F4B3} GeoCoins kaufen</button>
      <button class="btn-g" style="margin-bottom:0" onclick="S.lockModal=null;render()">Schlie\u00dfen</button>
    </div>
  </div>`;
}

/* POWER-UPS (Phase 26) */
function loadPU(){return _gqLoad("gq_pu",{});}
function savePU(d){_gqSave("gq_pu",d);}
function getPUCount(type){return(loadPU()[type]||0);}
function addPU(type,qty){const d=loadPU();d[type]=(d[type]||0)+qty;savePU(d);}
function syncJokersFromProfile(){
  if(\!sbProfile)return;
  const d=loadPU();
  if(sbProfile.joker_5050\!==null&&sbProfile.joker_5050\!==undefined)d.five0=sbProfile.joker_5050;
  if(sbProfile.joker_freeze\!==null&&sbProfile.joker_freeze\!==undefined)d.freeze=sbProfile.joker_freeze;
  savePU(d);
}
async function buyJoker(type){
  if(\!sb||\!sbUser){showToast("Bitte zuerst anmelden\!");return;}
  const cost=type==="five0"?50:75;
  const col=type==="five0"?"joker_5050":"joker_freeze";
  const coins=sbProfile?.geo_coins||0;
  if(coins<cost){showToast("Zu wenig GeoCoins\!");return;}
  if(sbProfile)sbProfile.geo_coins=coins-cost;
  const prevQty=(loadPU()[type]||0);
  addPU(type,3);
  const newQty=prevQty+3;
  if(sbProfile)sbProfile[col]=newQty;
  render();
  try{
    const r=await sb.rpc("spend_coins",{p_user_id:sbUser.id,p_amount:cost});
    if(r.data\!==null&&sbProfile)sbProfile.geo_coins=r.data;
    await sb.from("profiles").update({[col]:newQty}).eq("id",sbUser.id);
    showToast("\u2713 3\u00d7 Joker hinzugef\u00fcgt\!");
  }catch(e){
    const d=loadPU();d[type]=prevQty;savePU(d);
    if(sbProfile){sbProfile.geo_coins=coins;sbProfile[col]=prevQty;}
    showToast("Kauf fehlgeschlagen.");
    render();
  }
}
function useFiveO(){
  if(S.sel\!==null||S.half_removed)return;
  const pu=loadPU();if(\!(pu.five0>0)){showToast("Kein 50/50-Joker mehr\!");return;}
  pu.five0--;savePU(pu);
  if(sb&&sbUser)sb.from("profiles").update({joker_5050:pu.five0}).eq("id",sbUser.id).then(()=>{},()=>{pu.five0++;savePU(pu);showToast("\u26a0\ufe0f Joker-Sync fehlgeschlagen.");});
  const wrong=S.q.opts.filter(o=>o\!==S.q.ans);
  const toRemove=sh([...wrong]).slice(0,2);
  S.q.opts=S.q.opts.filter(o=>o===S.q.ans||\!toRemove.includes(o));
  S.half_removed=true;render();
}
function useFreeze(){
  if(S.freezeActive)return;
  const pu=loadPU();
  if(\!(pu.freeze>0)){showToast("Kein Zeit-Stopp mehr\!");return;}
  if(S.ph\!=="playing"&&S.ph\!=="feedback")return;
  pu.freeze--;savePU(pu);
  if(sb&&sbUser)sb.from("profiles").update({joker_freeze:pu.freeze}).eq("id",sbUser.id).then(()=>{},()=>{pu.freeze++;savePU(pu);showToast("\u26a0\ufe0f Joker-Sync fehlgeschlagen.");});
  clearInterval(tIv);S.freezeActive=true;
  const bar=document.querySelector(".tbar");if(bar)bar.classList.add("frozen");
  render();
  S.freezeTimer=setTimeout(()=>{
    if(S.ph\!=="playing"&&S.ph\!=="feedback"){S.freezeActive=false;return;}
    S.freezeActive=false;
    const b2=document.querySelector(".tbar");if(b2)b2.classList.remove("frozen");
    if(S.ph==="playing"&&S.sel===null){
      if(S.diff==="survival"){if(typeof tIv !== 'undefined') clearInterval(tIv); tIv=setInterval(()=>{S.tm--;if(S.tm===3)soundWarn(); render();if(S.tm<=0){clearInterval(tIv);if(S.q)answer(null,_secretGameToken);} },1000);}
    }
  },10000);
}

const ROUNDS=10,BASE=100,TB=10;
/* Phase 81 – Titel-Schwellenwerte */
const TITLE_THRESHOLDS=[
  {min:750000,title:"Meister",  coins:500, icon:"\u{1F451}"},
  {min:300000,title:"Platin",   coins:250, icon:"\u{1F48E}"},
  {min:100000,title:"Gold",     coins:150, icon:"\u{1F947}"},
  {min:25000, title:"Silber",   coins:100, icon:"\u{1F948}"},
  {min:5000,  title:"Bronze",   coins:50,  icon:"\u{1F949}"},
  {min:0,     title:"Erkunder", coins:0,   icon:"\u{1F30D}"},
];
const LEAGUES=[
  {id:"Bronze", icon:"\u{1F949}",color:"#c2410c",bg:"rgba(194,65,12,.13)",   next:"Top 20% steigen auf"},
  {id:"Silber", icon:"\u{1F948}",color:"#94a3b8",bg:"rgba(148,163,184,.13)", next:"Top 20% steigen auf"},
  {id:"Gold",   icon:"\u{1F947}",color:"#f59e0b",bg:"rgba(245,158,11,.13)",  next:"Top 20% steigen auf"},
  {id:"Platin", icon:"\u{1F48E}",color:"#38bdf8",bg:"rgba(56,189,248,.13)",  next:"Top 20% steigen auf"},
  {id:"Diamant",icon:"\u{1F4A0}",color:"#a78bfa",bg:"rgba(167,139,250,.13)", next:"Du bist in der H\u00f6chstliga!"},
];
function getLeague(id){return LEAGUES.find(l=>l.id===id)||LEAGUES[0];}

const TIERS=[
  {m:10,x:3.0,l:"\u{1F525}\u{1F525}\u{1F525} LEGEND\u00c4R – 3\u00d7"},
  {m:5, x:2.0,l:"\u{1F525}\u{1F525} ON FIRE – 2\u00d7"},
  {m:3, x:1.5,l:"\u{1F525} HEISS – 1.5\u00d7"},
  {m:0, x:1.0,l:""},
];

/* SUPABASE */
let sb=null,sbUser=null,sbProfile=null,sbStamps=new Set();
/* CURR_REAL, CAPS_POP, RIVERS_REAL populated by loadGameData() */
/* Helper: country name →’ cc */
function ccFromCountry(name){const c=COUNTRIES.find(x=>x.c===name);return c?c.cc:null;}
function flagOf(name){const cc=ccFromCountry(name);return cc?`<img src="https://flagcdn.com/w40/${cc}.png" style="height:22px;vertical-align:middle;border-radius:2px" alt="${name}">`:"";}

/* Phase 97-1: Zombie-SW-Killer – läuft vor Supabase-Init */
/* Tötet veraltete Service Worker, die Updates blockieren   */
(function _zombieKiller(){
  var SW_VER='gq-v9',LS_KEY='__gq_sw_ver';
  try{
    if(localStorage.getItem(LS_KEY)===SW_VER)return; /* aktuell – nichts zu tun */
    if(!('serviceWorker' in navigator)){localStorage.setItem(LS_KEY,SW_VER);return;}
    navigator.serviceWorker.getRegistrations().then(function(regs){
      if(regs.length===0){localStorage.setItem(LS_KEY,SW_VER);return;}
      /* Alter/zombie SW gefunden →’ nuklearer Reset */
      console.warn('[GQ] Zombie-SW: killing',regs.length,'registration(s) + wiping caches...');
      /* 1. Korrupte Auth-Tokens löschen */
      try{
        Object.keys(localStorage)
          .filter(function(k){return k.startsWith('sb-')||k.toLowerCase().includes('supabase');})
          .forEach(function(k){try{localStorage.removeItem(k);}catch(e){}});
      }catch(e){}
      /* 2. Version-Flag setzen (verhindert Reload-Loop) */
      localStorage.setItem(LS_KEY,SW_VER);
      /* 3. Alle SW-Registrierungen killen + Cache API leeren */
      var kills=regs.map(function(r){return r.unregister();});
      var cacheClear=('caches' in window)
        ?caches.keys().then(function(ks){return Promise.all(ks.map(function(k){return caches.delete(k);}));})
        :Promise.resolve();
      Promise.all(kills.concat([cacheClear])).then(function(){
        location.reload(true); /* Hard-Reload – erzwingt frisches HTML vom Server */
      });
    });
  }catch(e){console.warn('[GQ] zombieKiller error:',e);}
})();

const sbOK=SUPABASE_URL.includes("supabase.co");
let sbAuthPending=sbOK; /* Phase 81: true until getSession() resolves */
if(sbOK){
  try{
    /* Phase 100: auth.lock bypass – verhindert navigator.locks Deadlock bei _initialize() */
    sb=window.supabase.createClient(SUPABASE_URL,SUPABASE_ANON,{auth:{lock:async function(n,t,fn){return await fn();}}});
    initAuth();
  }catch(e){
    console.error("Supabase init failed:",e);
    setTimeout(()=>showToast("\u26a0\ufe0f Supabase-Verbindung fehlgeschlagen: "+e.message),1200);
    /* Phase 87: immer entsperren, sonst bleibt sbAuthPending=true und render() wird nie erreicht */
    sbAuthPending=false;
    render();
  }
}

async function initAuth(){
  /* Phase 89: interner Wächter – falls getSession()/signInAnonymously() nie settled */
  const _authTO=setTimeout(()=>{
    if(sbAuthPending){
      console.warn("[GQ] initAuth: 4s Wächter ausgelöst – bereinige Auth-Tokens...");
      /* Phase 93: korrupte Supabase-Tokens aus localStorage löschen */
      try{
        Object.keys(localStorage)
          .filter(k=>k.startsWith('sb-')||k.toLowerCase().includes('supabase'))
          .forEach(k=>{try{localStorage.removeItem(k);}catch(_){}});
      }catch(_){}
      sbAuthPending=false;
      render();
    }
  },4000);
  if(!sb){clearTimeout(_authTO);sbAuthPending=false;render();return;}
  /* Phase 83: handle token refresh + password recovery */
  sb.auth.onAuthStateChange(async(event,session)=>{
    if(event==="PASSWORD_RECOVERY"){
      S.authMode="new_password";S.tab="profil";S.ph="menu";
      showToast("\u{1F511} Gib jetzt dein neues Passwort ein.");
      render();return;
    }
    if((event==="TOKEN_REFRESHED"||event==="SIGNED_IN")&&session?.user){
      if(S.authMode==="new_password")return;/* keep recovery modal open */
      /* Phase 101: loadProfile ohne await – sonst blockiert _notifyAllSubscribers */
      if(\!sbUser||sbUser.id\!==session.user.id){sbUser=session.user;loadProfile();}
    }
  });
  try{
    /* Phase 97-2: getSession mit 3s Timeout – kein endloses Hängen */
    const _gsTmo=new Promise((_,rej)=>setTimeout(()=>rej(new Error('getSession 3s timeout')),3000));
    const{data:{session}}=await Promise.race([sb.auth.getSession(),_gsTmo]);
    if(session){sbUser=session.user;await loadProfile();}
    else{
      /* Phase 99-2: signInAnonymously mit 3s Timeout */
      const _siaTmo=new Promise((_,rej)=>setTimeout(()=>rej(new Error('signInAnonymously 3s timeout')),3000));
      const{data,error}=await Promise.race([sb.auth.signInAnonymously(),_siaTmo]);
      if(\!error&&data?.user){sbUser=data.user;await loadProfile();}
    }
  }catch(e){
    console.warn("[GQ] initAuth error:",e?.message||e);
  }finally{
    clearTimeout(_authTO); /* Phase 89: Wächter stoppen */
    /* ALWAYS unblock render – even if Supabase throws */
    sbAuthPending=false;
    console.log("[GQ] initAuth() finally – sbAuthPending=false, calling render()");
    render();
  }
}
async function loadProfile(){
  if(\!sb||\!sbUser)return;
  const{data}=await sb.from("profiles").select("*").eq("id",sbUser.id).single();
  sbProfile=data;
  syncJokersFromProfile();
  /* Phase 82: sync stats from Supabase -> localStorage */
  if(data){
    if(Array.isArray(data.stats_history)&&data.stats_history.length>0)_gqSave("gq_history",data.stats_history);
    if(data.stats_mastery&&typeof data.stats_mastery==="object"&&Object.keys(data.stats_mastery).length>0)_gqSave("gq_mastery",data.stats_mastery);
    if(data.last_daily_date){
      const _today=new Date().toISOString().slice(0,10);
      if(data.last_daily_date===_today){const _dk=getDailyKey();if(\!localStorage.getItem(_dk)){try{localStorage.setItem(_dk,JSON.stringify({score:0,ts:Date.now()}));}catch(_e){}}}
    }
  }
  /* Phase 93: Smart-Merge Kennzeichen – Cloud âˆª Lokal */
  if(data&&typeof data.plates_collected==="string"){
    try{
      const _cp=JSON.parse(data.plates_collected||"[]");
      if(Array.isArray(_cp)&&_cp.length>0){
        const _lp=_gqLoad("gq_coll",[]);
        const _mp=[...new Set([..._lp,..._cp])];
        _gqSave("gq_coll",_mp);
        S.collectedPlates=_mp;
        /* Merged Stand zurück in Cloud pushen wenn gewachsen */
        if(_mp.length>_cp.length){
          sb.from("profiles").update({plates_collected:JSON.stringify(_mp)})
            .eq("id",sbUser.id).then(()=>{},()=>{});
        }
      }else if(!data.plates_collected||data.plates_collected==="[]"){
        /* Noch keine Cloud-Daten – lokale Daten hochladen */
        const _lp2=_gqLoad("gq_coll",[]);
        if(_lp2.length>0){
          sb.from("profiles").update({plates_collected:JSON.stringify(_lp2)})
            .eq("id",sbUser.id).then(()=>{},()=>{});
        }
      }
    }catch(_e){console.warn("[GQ] plates-merge Fehler",_e);}
  }else if(data&&!data.plates_collected){
    /* Spalte fehlt noch (vor Migration) – lokale Daten sind maßgeblich */
    const _lp3=_gqLoad("gq_coll",[]);
    S.collectedPlates=_lp3.length>0?_lp3:S.collectedPlates;
  }
  /* Admin privileges handled server-side via Supabase trigger */
  const{data:stamps}=await sb.from("user_stamps").select("stamp_id,stamps(country_code)").eq("user_id",sbUser.id);
  if(stamps)stamps.forEach(s=>s.stamps&&sbStamps.add(s.stamps.country_code));
  render();
  /* Phase 84+89: lazy weekly league evaluation */
  console.log("[GQ] Starting evaluateWeeklyLeague");
  evaluateWeeklyLeague()
    .then(()=>console.log("[GQ] evaluateWeeklyLeague done"))
    .catch(e=>console.warn("[GQ] evaluateWeeklyLeague error:",e?.message||e));
}
/* Helper: get display name */
function getDisplayName(){return sbProfile?.username||localStorage.getItem("gq_username")||null;}

async function saveUsername(n){
  if(!n.trim())return;
  const u=n.trim().slice(0,20);
  if(sbOK&&sb&&sbUser){await sb.from("profiles").update({username:u}).eq("id",sbUser.id);}
  if(!sbProfile)sbProfile={};
  sbProfile={...sbProfile,username:u};
  try{localStorage.setItem("gq_username",u);}catch(e){}
  S.newUsername="";
  showToast("\u2713 Name gespeichert: "+u);
  render();
}

/* Phase 27: Migrate guest localStorage data to real account */
async function migrateGuestToAccount(uid){
  if(!sb||!uid)return;
  const mastery=loadMastery();
  let bonusCoins=0;
  Object.values(mastery).forEach(m=>{
    const r=getMasteryRank(m.v,m.p);
    if(r==="gold")bonusCoins+=20;
    else if(r==="silver")bonusCoins+=5;
    else if(r==="bronze")bonusCoins+=1;
  });
  const totalCoins=(sbProfile?.geo_coins||0)+bonusCoins;
  try{const _cr=await sb.rpc("add_coins",{p_user_id:uid,p_amount:bonusCoins});if(_cr.data!=null&&sbProfile)sbProfile.geo_coins=_cr.data;}catch(_){}
  if(sbProfile)sbProfile.geo_coins=totalCoins;
  const masteryCC=Object.keys(mastery).filter(cc=>getMasteryRank(mastery[cc].v,mastery[cc].p));
  for(const cc of masteryCC){
    sb.rpc("upsert_stamp",{p_user_id:uid,p_country_code:cc,p_perfect:mastery[cc].p>0}).then(()=>{},()=>{});
  }
}

function togglePw(id,btn){const el=document.getElementById(id);if(\!el)return;const show=el.type==="password";el.type=show?"text":"password";btn.textContent=show?"\u{1F648}":"\u{1F441}";}
/* Phase 27: Register */
async function doRegister(){
  if(!sb){showToast("Supabase nicht verbunden");return;}
  const email=S.authEmail.trim();
  const pw=S.authPassword;
  const uname=S.authUsername.trim().slice(0,20);
  if(!email||!pw||!uname){S.authError="Bitte alle Felder ausf\u00fcllen.";render();return;}
  if(pw.length<6){S.authError="Passwort mind. 6 Zeichen.";render();return;}
  if(pw!==S.authConfirm){S.authError="Die Passwörter stimmen nicht überein.";render();return;}
  S.authLoading=true;S.authError="";render();
  /* Phase 90: 5s Timeout-Waechter */
  setTimeout(()=>{
    if(S.authLoading){S.authLoading=false;S.authError="Netzwerk-Timeout. Bitte überprüfe deine Verbindung.";render();}
  },5000);
  try{
    const{data,error}=await sb.auth.signUp({email,password:pw,options:{data:{username:uname}}});
    if(error){
      const _em=error.message||"";
      S.authError=
        _em.includes("already registered")||_em.includes("already been registered")?"Diese E-Mail ist bereits registriert.":
        _em.includes("Password should be")||_em.includes("password")?"Passwort zu schwach (mind. 6 Zeichen).":
        _em.includes("valid email")||_em.includes("invalid format")||_em.includes("Unable to validate email")?"Bitte eine gültige E-Mail-Adresse eingeben.":
        _em.includes("rate limit")||_em.includes("too many")?"Zu viele Versuche. Bitte kurz warten.":
        _em||"Registrierung fehlgeschlagen.";
      S.authLoading=false;render();return;
    }
    const uid=data.user?.id;
    if(!uid){S.authError="Registrierung fehlgeschlagen.";S.authLoading=false;render();return;}
    // Save username locally immediately
    try{localStorage.setItem("gq_username",uname);}catch(e){}
    // Upsert profile (fire & forget errors)
    const{error:_upErr}=await sb.from("profiles").upsert({id:uid,username:uname});
    sbUser=data.user;
    sbProfile={...(sbProfile||{}),username:uname,geo_coins:100,id:uid};
    if(data.session)sb.rpc("add_coins",{p_user_id:uid,p_amount:100}).then(()=>{},()=>{});
    // Migrate guest data in background (don't await to avoid hanging)
    migrateGuestToAccount(uid).catch(()=>{});
    S.authLoading=false;S.authEmail="";S.authPassword="";S.authConfirm="";S.authUsername="";S.authError="";
    // If email confirmation required (session is null), show info message
    if(!data.session){
      showToast("\uD83D\uDCE7 Best\u00e4tigungsmail gesendet! Bitte E-Mail pr\u00fcfen.");
    } else {
      showToast("\uD83C\uDF89 Willkommen, "+uname+"! Fortschritt gesichert.");
      // Full profile load only if already confirmed
      loadProfile().catch(()=>{});
    }
    render();
  }catch(err){
    const _em=err.message||"";
    S.authError=
      _em.includes("already registered")||_em.includes("already been registered")?"Diese E-Mail ist bereits registriert.":
      _em.includes("valid email")||_em.includes("invalid format")?"Bitte eine gültige E-Mail-Adresse eingeben.":
      _em||"Unbekannter Fehler.";
    S.authLoading=false;
    render();
  }
}

/* Phase 27: Login */
async function doLogin(){
  if(!sb){showToast("Supabase nicht verbunden");return;}
  const email=S.authEmail.trim();
  const pw=S.authPassword;
  if(!email||!pw){S.authError="E-Mail und Passwort eingeben.";render();return;}
  S.authLoading=true;S.authError="";render();
  /* Phase 90: 5s Timeout-Waechter */
  const _loginTO=setTimeout(()=>{
    if(S.authLoading){S.authLoading=false;S.authError="Netzwerk-Timeout. Bitte überprüfe deine Verbindung.";render();}
  },5000);
  try{
    const{data,error}=await sb.auth.signInWithPassword({email,password:pw});
    if(error){
      const _m=error.message;
      S.authError=_m==="Invalid login credentials"?"E-Mail oder Passwort falsch.":
        _m.includes("Email not confirmed")?"Bitte bestätige zuerst deine E-Mail-Adresse!":
        _m.includes("Too many requests")?"Zu viele Versuche. Bitte kurz warten.":_m;
      return;
    }
    sbUser=data.user;
    await loadProfile();
    S.authEmail="";S.authPassword="";S.authConfirm="";S.authError="";
    S.tab="home";
  }catch(e){
    S.authError=e?.message||"Anmeldung fehlgeschlagen.";
  }finally{
    clearTimeout(_loginTO);
    S.authLoading=false;
    render();
  }
}

/* Phase 27: Logout */
async function doLogout(){
  if(!sb)return;
  await sb.auth.signOut();
  sbUser=null;sbProfile=null;sbStamps=new Set();
  try{localStorage.removeItem("gq_username");}catch(e){}
  /* Reset UI state – prevents stale mid-game or modal views after logout */
  S.ph="menu";S.tab="home";S.mpModal=false;S.payModal=false;S.lockModal=null;
  S.authEmail="";S.authPassword="";S.authConfirm="";S.authError="";
  const{data}=await sb.auth.signInAnonymously();
  if(data)sbUser=data.user;
  render();
}
/* Phase 83: Password reset */
async function doForgotPassword(){
  if(\!sb){showToast("Supabase nicht verbunden");return;}
  const email=S.authEmail.trim();
  if(\!email){S.authError="Bitte E-Mail-Adresse eingeben.";render();return;}
  S.authLoading=true;S.authError="";render();
  const{error}=await sb.auth.resetPasswordForEmail(email,{redirectTo:window.location.origin});
  S.authLoading=false;
  if(error){S.authError=error.message;render();return;}
  showToast("\u2705 Reset-Link gesendet an "+email+"\!");
  S.authMode="login";S.authEmail="";render();
}
async function doSetNewPassword(){
  if(!sb){showToast("Supabase nicht verbunden");return;}
  const pw=S.authPassword;
  if(!pw||!S.authConfirm){S.authError="Bitte beide Felder ausf\u00fcllen.";render();return;}
  if(pw.length<6){S.authError="Passwort mind. 6 Zeichen.";render();return;}
  if(pw!==S.authConfirm){S.authError="Passw\u00f6rter stimmen nicht \u00fcberein.";render();return;}
  S.authLoading=true;S.authError="";render();
  /* Phase 90: 5s Timeout-Waechter */
  const _pwTO=setTimeout(()=>{
    if(S.authLoading){S.authLoading=false;S.authError="Netzwerk-Timeout. Bitte \u00fcberpr\u00fcfe deine Verbindung.";render();}
  },5000);
  try{
    const{error}=await sb.auth.updateUser({password:pw});
    if(error){S.authError=error.message;return;}
    showToast("\u2705 Passwort erfolgreich ge\u00e4ndert\!");
    S.authMode="login";S.authPassword="";S.authConfirm="";
  }catch(e){
    S.authError=e?.message||"Passwort konnte nicht gesetzt werden.";
  }finally{
    clearTimeout(_pwTO);
    S.authLoading=false;
    render();
  }
}
/* Phase 85 – Coming Soon toast */
function showComingSoonToast(name){showToast("\u{1F680} "+name+" kommt bald\! Bleib gespannt.");}
async function saveSession(mode,score,bs,correct,durationMs){
  /* Local fallback – always write so guests keep history too */
  const _device=/Mobi|Android|iPhone|iPad|iPod|Opera Mini/i.test(navigator.userAgent)?"mobile":"desktop";
  try{
    const _loc=JSON.parse(localStorage.getItem("gq_sessions_local")||"[]");
    _loc.push({mode,score,max:bs,correct,duration_ms:durationMs||0,date:new Date().toISOString(),device_type:_device});
    localStorage.setItem("gq_sessions_local",JSON.stringify(_loc.slice(-50)));
  }catch(e){}
  /* Sanity-cap score before submitting – max honest = ROUNDS*(BASE+12*TB)*3*3 */
  const _maxScore=Math.ceil(ROUNDS*(BASE+12*TB)*3*3*1.1);
  score=Math.min(score,_maxScore);
  bs=Math.min(bs,ROUNDS);
  correct=Math.min(correct,ROUNDS);
  /* Phase 33 Teil 2: notify opponent at game end */
  if(window.mpGameCh&&S.mpOpponent){
    window.mpGameCh.send({type:"broadcast",event:"game_over",
      payload:{score,name:sbProfile?.username||"Ich",correct}}).then(()=>{},()=>{});
    window.mpGameCh=null;
  }
  if(!sb||!sbUser?.id)return;
  try{await sb.from("game_sessions").insert({user_id:sbUser.id,mode,score,best_streak:bs,rounds:ROUNDS,accuracy:Math.round(correct/ROUNDS*100),username:sbProfile?.username||null,device_type:_device});}catch(_e){await sb.from("game_sessions").insert({user_id:sbUser.id,mode,score,best_streak:bs,rounds:ROUNDS,accuracy:Math.round(correct/ROUNDS*100),username:sbProfile?.username||null});}
  /* Use RPC to prevent client-side score tampering */
  await sb.rpc("add_score",{p_user_id:sbUser.id,p_score:score,p_coins:Math.floor(score/100),p_rounds:ROUNDS,p_duration_ms:durationMs||0});
  if(sbProfile){sbProfile.total_score=(sbProfile.total_score||0)+score;sbProfile.games_played=(sbProfile.games_played||0)+1;}
  if(sbProfile)checkTitleUp(sbProfile.total_score||0).catch(()=>{});
}
async function fetchLeaderboard(mode){
  if(\!sb)return[];
  const{data}=await sb.from("leaderboard_weekly").select("*").eq("mode",mode).order("rank",{ascending:true}).limit(30);
  return data||[];
}
/* Phase 81 – Titel-System */
function getTitleForScore(ts){
  return(TITLE_THRESHOLDS.find(t=>ts>=t.min)||TITLE_THRESHOLDS[TITLE_THRESHOLDS.length-1]).title;
}
async function checkTitleUp(newTotal){
  if(\!sb||\!sbUser||\!sbProfile)return;
  const oldTitle=sbProfile.current_title||"Erkunder";
  const newTitle=getTitleForScore(newTotal);
  if(newTitle===oldTitle)return;
  const oldIdx=TITLE_THRESHOLDS.findIndex(t=>t.title===oldTitle);
  const newIdx=TITLE_THRESHOLDS.findIndex(t=>t.title===newTitle);
  if(newIdx>=oldIdx)return;
  const reward=TITLE_THRESHOLDS[newIdx];
  sbProfile.current_title=newTitle;
  sb.from("profiles").update({current_title:newTitle}).eq("id",sbUser.id).then(()=>{},()=>{});
  if(reward.coins>0){
    try{const _cr=await sb.rpc("add_coins",{p_user_id:sbUser.id,p_amount:reward.coins});
      if(_cr.data\!=null&&sbProfile)sbProfile.geo_coins=_cr.data;
      else if(sbProfile)sbProfile.geo_coins=(sbProfile.geo_coins||0)+reward.coins;
    }catch(_){}
  }
  showToast(reward.icon+" Rang-Aufstieg\! Du bist jetzt "+newTitle+"\!"+(reward.coins>0?" +"+reward.coins+" GeoCoins":""));
  render();
}

/* MASTERY */
function loadMastery(){return _gqLoad("gq_mastery",{});}
function saveMastery(d){
  _gqSave("gq_mastery",d);
  if(sb&&sbUser)sb.from("profiles").update({stats_mastery:d}).eq("id",sbUser.id).then(()=>{},()=>{});
}
function getMasteryRank(v,p){if(v>=15||p>=3)return"gold";if(v>=5||p>=1)return"silver";if(v>=1)return"bronze";return null;}
function getTravelRank(n){return n>=50?"Weltbuerger":n>=30?"Globetrotter":n>=15?"Weltenbummler":n>=5?"Reisender":"Einheimischer";}
function checkMastery(){
  const mastery=loadMastery();const answers=S.sessionAnswers||[];const isPerfect=S.correct===ROUNDS;
  const newlyUnlocked=[];
  const seen=new Set();
  answers.forEach(a=>{
    if(\!a.cc||\!a.correct)return;
    if(\!mastery[a.cc])mastery[a.cc]={v:0,p:0};
    mastery[a.cc].v++;
    if(isPerfect&&\!seen.has(a.cc)){mastery[a.cc].p++;seen.add(a.cc);}
  });
  if(isPerfect){
    const uniqueCC=[...new Set(answers.filter(a=>a.correct&&a.cc).map(a=>a.cc))];
    uniqueCC.forEach(cc=>{
      const m=mastery[cc];const rank=getMasteryRank(m.v,m.p);
      if(rank)newlyUnlocked.push({cc,rank});
      if(sbOK&&sbUser)syncStampSupabase(cc,true);
    });
  }else if(sbOK&&sbUser){
    const uniqueCC=[...new Set(answers.filter(a=>a.correct&&a.cc).map(a=>a.cc))];
    uniqueCC.forEach(cc=>syncStampSupabase(cc,false));
  }
  saveMastery(mastery);S.newStamps=newlyUnlocked;
}
function syncStampSupabase(cc,perfect){
  if(\!sb||\!sbUser)return;
  sb.rpc("upsert_stamp",{p_user_id:sbUser.id,p_country_code:cc,p_perfect:perfect}).then(()=>{},()=>{});
}

/* AUDIO */
let audioCtx=null,soundOn=true;
const SVG_VOL_ON=`<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>`;
const SVG_VOL_OFF=`<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><line x1="23" y1="9" x2="17" y2="15"/><line x1="17" y1="9" x2="23" y2="15"/></svg>`;
function toggleSound(){soundOn=\!soundOn;document.getElementById("soundBtn").innerHTML=soundOn?SVG_VOL_ON:SVG_VOL_OFF;}
function getCtx(){if(\!audioCtx)audioCtx=new(window.AudioContext||window.webkitAudioContext)();if(audioCtx.state==="suspended")audioCtx.resume();return audioCtx;}
function playTone(f,type,dur,vol=0.2){if(\!soundOn)return;try{const c=getCtx(),o=c.createOscillator(),g=c.createGain();o.connect(g);g.connect(c.destination);o.type=type;o.frequency.setValueAtTime(f,c.currentTime);g.gain.setValueAtTime(vol,c.currentTime);g.gain.exponentialRampToValueAtTime(0.001,c.currentTime+dur);o.start(c.currentTime);o.stop(c.currentTime+dur);}catch(e){}}
function soundCorrect(){[523,659,784].forEach((f,i)=>setTimeout(()=>playTone(f,"sine",.18,.2),i*60));}
function soundWrong(){playTone(300,"sawtooth",.15,.18);setTimeout(()=>playTone(220,"sawtooth",.2,.15),80);}
function soundStreak(l){if(\!soundOn)return;if(l>=10)[523,659,784,1047].forEach((f,i)=>setTimeout(()=>playTone(f,"sine",.25,.2),i*55));else if(l>=5)[523,659,784].forEach((f,i)=>setTimeout(()=>playTone(f,"triangle",.2,.18),i*60));else[523,659].forEach((f,i)=>setTimeout(()=>playTone(f,"sine",.15,.15),i*70));}
function soundWarn(){playTone(440,"square",.08,.1);}
function soundOver(){[392,330,262].forEach((f,i)=>setTimeout(()=>playTone(f,"sawtooth",.3,.2),i*120));}
function soundStamp(){[880,1047,1320].forEach((f,i)=>setTimeout(()=>playTone(f,"sine",.15,.15),i*80));}

/* STATE */
let _secretGameToken=null; /* Anti-Cheat: new token each game */
let S={
  ph:"menu",tab:"home",mode:"city",diff:"casual",
  sc:0,st:0,bs:0,rd:0,correct:0,tm:12,dur:12,
  q:null,sel:null,ok:null,pts:0,lid:null,
  lbData:[],lbLoading:false,scoreSaved:false,newUsername:"",
  sessionAnswers:[],newStamps:[],modal:null,
  obStep:-1,obLang:"de",obDiff:"casual",
  payModal:false,mpModal:false,mp:null,
  challenge:null,challengeSeed:null,
  pwaPrompt:null,
  lockModal:null,
  dailyDone:false,
  isDailyRun:false,
  challengeStarted:false,
  half_removed:false,
  freezeActive:false,
  filter:"all",
  activeCategory:null,
  filterCat:'pure_geo',
  fcIdx:0,fcFlipped:false,fcSearch:"",fcCountry:"all",
  darkMode:false,
  authMode:"login",authEmail:"",authPassword:"",authConfirm:"",authUsername:"",authError:"",authLoading:false,
  lvModal:false,lv:null,lvSetupMode:"random",
  settingsModal:false,
  convModal:false,
  collectedPlates:loadCollectedPlates(),
  ligaData:[],ligaLoading:false,leagueEvalResult:null,
  statsData:null,statsLoading:false,adminData:null,adminLoading:false,
  titleShop:false,
  language:(()=>{const _sl=localStorage.getItem("gq_lang");if(_sl&&LANG[_sl])return _sl;const _bl=(navigator.language||"de").substring(0,2).toLowerCase();return LANG[_bl]?_bl:"de";})(),spotterInput:"",spotterMsg:"",spotterOk:null,albumView:"list",albumCountry:_smartDefaultCountry(),spotterCountry:_smartDefaultCountry(),
  collFilter:"all",collRarity:"all",collSearch:"",
};
let tIv=null,fTo=null,toastTo=null;

/* â”€â”€ Phase 42: Anti-Cheat – Proxy wrapper for S in console â”€â”€ */
(function(){
  const GUARDED=new Set(["sc","correct","st","bs","pts","collectedPlates","sbProfile"]);
  if(typeof Proxy==="undefined")return;
  try{
    const _real=S;
    const _p=new Proxy(_real,{
      set(t,k,v){
        if(GUARDED.has(k)){
          /* Check if call is from our own code (has game functions in stack) */
          const stk=(new Error()).stack||"";
          const trusted=["answer","startGame","mpCountdown","lq","nextRound",
            "checkMastery","spotterCollect","saveSession","loadData","initAuth",
            "handleGridAnswer","finishCustomGame","submitGridResult"];
          const ok=trusted.some(fn=>stk.includes(fn));
          if(!ok){
            console.warn("%c🚫 GeoQuest: Schummeln erkannt! Feld '"+k+"' ist geschützt.",
              "color:#ef4444;font-weight:bold;font-size:14px");
            return true; /* silent block */
          }
        }
        t[k]=v;return true;
      }
    });
    /* Shadow window.S with the guarded proxy */
    Object.defineProperty(window,"S",{get:()=>_p,configurable:false,enumerable:false});
  }catch(e){}
})();


/* DARK MODE */
function applyTheme(){
  document.documentElement.setAttribute("data-theme",S.darkMode?"dark":"");
  try{localStorage.setItem("gq_dark",S.darkMode?"1":"0");}catch(e){}
}
(function initTheme(){try{S.darkMode=localStorage.getItem("gq_dark")==="1";}catch(e){}applyTheme();})();

/* HELPERS */
function sh(a){const b=[...a];for(let i=b.length-1;i>0;i--){const j=~~(rng()*(i+1));[b[i],b[j]]=[b[j],b[i]];}return b;}
function tier(s){return TIERS.find(t=>s>=t.m)||TIERS[3];}
function tc(){return S.tm>6?"#10b981":S.tm>3?"#f59e0b":"#ef4444";}
function pct(){return(S.tm/S.dur)*100;}
function showToast(msg){
  const old=document.getElementById("copy-toast");if(old)old.remove();
  const el=document.createElement("div");el.id="copy-toast";el.className="copy-toast";el.textContent=msg;
  document.body.appendChild(el);setTimeout(()=>el.remove(),2200);
}
function distractors(pool,matchFn,excludeFn,keyFn,n=2){
  const pref=pool.filter(x=>matchFn(x)&&\!excludeFn(x));
  const dp=pref.length>=n?pref:pool.filter(x=>\!excludeFn(x));
  const seen=new Set(),dis=[];
  for(const x of sh([...dp])){const k=keyFn(x);if(k\!==undefined&&\!seen.has(k)){seen.add(k);dis.push(k);if(dis.length===n)break;}}
  if(dis.length<n){for(const x of sh([...pool])){const k=keyFn(x);if(\!excludeFn(x)&&\!seen.has(k)){seen.add(k);dis.push(k);if(dis.length===n)break;}}}
  return dis;
}

/* GENERATORS */
function genCityQ(){
  const pf_initial = S.diff==="hardcore"?0:200000;
  let filtered = CITIES.filter(c=>c.pop>=pf_initial&&c.id!==S.lid);
  let pf = pf_initial;
  if(filtered.length === 0) {
    filtered = CITIES.filter(c=>c.id!==S.lid);
    pf = 0;
  }
  let pool = _rfilt(filtered, 3);
  if(pool.length < 1) return null;
  const cor = pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.sub===cor.sub||x.cont===cor.cont,x=>x.c===cor.c,x=>displayCountry(x.cc)||x.c);
  console.log("🔴 DEBUG genCityQ pool.length:", pool ? pool.length : 0, "pf:", pf);
  console.log("🔴 DEBUG genCityQ pool.length:", pool ? pool.length : 0, "pf:", pf);
  return{type:"city",prompt:t("q_city"),subj:cor.n,ans:displayCountry(cor.cc)||cor.c,opts:sh([displayCountry(cor.cc)||cor.c,...dis]),meta:cor.cont+" \u00b7 "+(cor.pop/1e6).toFixed(1)+" Mio.",lid:cor.id,cc:cor.cc};
}
function genFlagQ(){
  let pool=_rfilt(COUNTRIES.filter(x=>x.cc\!==S.lid),3); if(pool.length<3) pool=COUNTRIES.filter(x=>x.cc\!==S.lid); if(pool.length<1) return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.sr===cor.sr||x.ct===cor.ct,x=>x.c===cor.c,x=>displayCountry(x.cc)||x.c);
  return{type:"flag",prompt:t("q_flag"),subj:cor.cc,ans:displayCountry(cor.cc)||cor.c,opts:sh([displayCountry(cor.cc)||cor.c,...dis]),meta:cor.ct,lid:cor.cc,cc:cor.cc};
}
function genCapitalQ(){
  let pool=_rfilt(CAPITALS.filter(x=>x.capital\!==S.lid),3); if(pool.length<3) pool=CAPITALS.filter(x=>x.capital\!==S.lid); if(pool.length<1) return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.subregion===cor.subregion||x.continent===cor.continent,x=>x.country===cor.country,x=>displayCountry(x.cc)||x.country);
  return{type:"capital",prompt:t("q_capital"),subj:cor.capital,ans:displayCountry(cor.cc)||cor.country,opts:sh([displayCountry(cor.cc)||cor.country,...dis]),meta:cor.continent,lid:cor.capital,cc:cor.cc};
}
/* Phase 62: region filter helpers */
function _regionOk(cc,cont){
  const f=S.filter;
  if(f==="all"||f==="eu_plates")return true;
  const c=cont||(COUNTRIES.find(x=>x.cc===cc)||{}).ct||"";
  if(f==="europe")return c==="Europe";
  if(f==="africa")return c==="Africa";
  if(f==="oceania")return c==="Oceania";
  if(f==="asia")return c==="Asia";
  if(f==="america")return c.includes("America");
  return true;
}
function _rfilt(pool,minLen){
  if(S.filter==="all"||S.filter==="eu_plates")return pool;
  const f=pool.filter(x=>_regionOk(x.cc,x.continent));
  return f.length>=minLen?f:pool;
}
function genRiverQ(){
  let pool=_rfilt(RIVERS.filter(x=>x.name\!==S.lid),3); if(pool.length<3) pool=RIVERS.filter(x=>x.name\!==S.lid); if(pool.length<1) return null;
  const cor=pool[~~(rng()*pool.length)];
  const _cpool=_rfilt(COUNTRIES,4);const dis=distractors(_cpool,x=>x.sr===cor.subregion||x.ct===cor.continent,x=>x.c===cor.country,x=>displayCountry(x.cc)||x.c);
  return{type:"river",prompt:t("q_river"),subj:cor.name,ans:displayCountry(cor.cc)||cor.country,opts:sh([displayCountry(cor.cc)||cor.country,...dis]),meta:cor.continent,lid:cor.name,cc:cor.cc};
}
function genLandmarkQ(){
  let pool=_rfilt(LANDMARKS.filter(x=>x.name\!==S.lid),3); if(pool.length<3) pool=LANDMARKS.filter(x=>x.name\!==S.lid); if(pool.length<1) return null;
  const cor=pool[~~(rng()*pool.length)];
  const _cpool=_rfilt(COUNTRIES,4);const dis=distractors(_cpool,x=>x.sr===cor.subregion||x.ct===cor.continent,x=>x.c===cor.country,x=>displayCountry(x.cc)||x.c);
  return{type:"landmark",prompt:t("q_landmark"),subj:cor.name,ans:displayCountry(cor.cc)||cor.country,opts:sh([displayCountry(cor.cc)||cor.country,...dis]),meta:cor.continent,lid:cor.name,cc:cor.cc};
}
function genParkQ(){
  let pool=_rfilt(NATIONAL_PARKS.filter(x=>x.name\!==S.lid),3); if(pool.length<3) pool=NATIONAL_PARKS.filter(x=>x.name\!==S.lid); if(pool.length<1) return null;
  const cor=pool[~~(rng()*pool.length)];
  const _cpool=_rfilt(COUNTRIES,4);const dis=distractors(_cpool,x=>x.sr===cor.subregion||x.ct===cor.continent,x=>x.c===cor.country,x=>displayCountry(x.cc)||x.c);
  return{type:"park",prompt:t("q_park"),subj:cor.name,ans:displayCountry(cor.cc)||cor.country,opts:sh([displayCountry(cor.cc)||cor.country,...dis]),meta:cor.continent,lid:cor.name,cc:cor.cc};
}
function genUnescoQ(){
  let pool=_rfilt(UNESCO_SITES.filter(x=>x.name\!==S.lid),3); if(pool.length<3) pool=UNESCO_SITES.filter(x=>x.name\!==S.lid); if(pool.length<1) return null;
  const cor=pool[~~(rng()*pool.length)];
  const _cpool=_rfilt(COUNTRIES,4);const dis=distractors(_cpool,x=>x.sr===cor.subregion||x.ct===cor.continent,x=>x.c===cor.country,x=>displayCountry(x.cc)||x.c);
  return{type:"unesco",prompt:t("q_unesco"),subj:cor.name,ans:displayCountry(cor.cc)||cor.country,opts:sh([displayCountry(cor.cc)||cor.country,...dis]),meta:cor.continent,lid:cor.name,cc:cor.cc};
}
function genCitymarkQ(){
  let pool=_rfilt(CITY_LANDMARKS.filter(x=>x.name\!==S.lid),3); if(pool.length<3) pool=CITY_LANDMARKS.filter(x=>x.name\!==S.lid); if(pool.length<1) return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.subregion===cor.subregion||x.continent===cor.continent,x=>x.city===cor.city,x=>x.city);
  return{type:"citymark",prompt:t("q_citymark"),subj:cor.name,ans:cor.city,opts:sh([cor.city,...dis]),meta:cor.country,lid:cor.name,cc:cor.cc};
}
function genSubwayQ(){
  let pool=_rfilt(SUBWAYS.filter(x=>x.city\!==S.lid),3); if(pool.length<3) pool=SUBWAYS.filter(x=>x.city\!==S.lid); if(pool.length<1) return null;
  const t=Math.floor(rng()*2);
  const cor=pool[~~(rng()*pool.length)];
  const dis3=distractors(pool,x=>x.country===cor.country||x.cc===cor.cc,x=>x.city===cor.city,x=>t===0?x.km:x.lines,2);
  const ansVal=t===0?cor.km:cor.lines;
  const prompt=t===0?"Wie lang ist das U-Bahn-Netz in \u2026 (km)?":"Wie viele U-Bahn-Linien hat \u2026?";
  const suffix=t===0?" km":" Linien";
  return{type:"subway",prompt,subj:cor.city,ans:String(ansVal),opts:sh([String(ansVal),...dis3.map(String)]),meta:cor.country+" \u00b7 "+suffix.trim(),lid:cor.city,cc:cor.cc};
}
function genFlagselQ(){
  let pool=_rfilt(COUNTRIES.filter(x=>x.cc\!==S.lid),4); if(pool.length<4) pool=COUNTRIES.filter(x=>x.cc\!==S.lid); if(pool.length<4) return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.sr===cor.sr||x.ct===cor.ct,x=>x.cc===cor.cc,x=>x.cc,3);
  return{type:"flagsel",prompt:t("q_flagsel"),subj:displayCountry(cor.cc)||cor.c,ans:cor.cc,opts:sh([cor.cc,...dis]),meta:cor.ct,lid:cor.cc,cc:cor.cc};
}
function genRcapitalQ(){
  let pool=_rfilt(CAPITALS.filter(x=>x.country\!==S.lid),3); if(pool.length<3) pool=CAPITALS.filter(x=>x.country\!==S.lid); if(pool.length<1) return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.subregion===cor.subregion||x.continent===cor.continent,x=>x.capital===cor.capital,x=>x.capital);
  return{type:"rcapital",prompt:t("q_rcapital"),subj:displayCountry(cor.cc)||cor.country,ans:cor.capital,opts:sh([cor.capital,...dis]),meta:cor.continent,lid:cor.country,cc:cor.cc};
}
function genRcityQ(){
  let pool=_rfilt(COUNTRIES.filter(x=>x.c\!==S.lid),3); if(pool.length<3) pool=COUNTRIES.filter(x=>x.c\!==S.lid); if(pool.length<1) return null;
  const cor=pool[~~(rng()*pool.length)];
  const cc2=CITIES.filter(c=>c.c===cor.c);if(\!cc2.length)return genRcityQ();
  const corCity=cc2[~~(rng()*cc2.length)];
  const _citpool=_rfilt(CITIES,4);const dis=distractors(_citpool,x=>x.sub===corCity.sub||x.cont===corCity.cont,x=>x.c===cor.c,x=>x.n);
  return{type:"rcity",prompt:t("q_rcity"),subj:displayCountry(cor.cc)||cor.c,ans:corCity.n,opts:sh([corCity.n,...dis]),meta:cor.ct,lid:cor.c,cc:cor.cc};
}
function genRriverQ(){
  const _rpool=_rfilt(RIVERS,3);
  const ctries=[...new Set(_rpool.map(r=>r.country))].filter(c=>c\!==S.lid);if(\!ctries.length)return null;
  const corC=ctries[~~(rng()*ctries.length)];
  const cRivers=_rpool.filter(r=>r.country===corC);
  const cor=cRivers[~~(rng()*cRivers.length)];
  const dis=distractors(_rpool,x=>x.subregion===cor.subregion||x.continent===cor.continent,x=>x.country===corC,x=>x.name);
  return{type:"rriver",prompt:t("q_rriver"),subj:displayCountry(cor.cc)||corC,ans:cor.name,opts:sh([cor.name,...dis]),meta:cor.continent,lid:corC,cc:cor.cc};
}
function genFoodQ(){
  if(\!FOOD_DATA.length)return null;
  const _fp=_rfilt(FOOD_DATA,3);const item=_fp[~~(rng()*_fp.length)];
  const corC=item.country;
  const _fDisR=[...new Set(_fp.filter(f=>f.country\!==corC).map(f=>f.country))];
  const _fDisAll=[...new Set(FOOD_DATA.filter(f=>f.country\!==corC).map(f=>f.country))];
  const picked=sh(_fDisR.length>=3?_fDisR:_fDisAll).slice(0,3);
  return{type:"food",prompt:t("q_food"),subj:item.dish,emoji:null,ans:displayCountry(item.cc)||corC,opts:sh([displayCountry(item.cc)||corC,...picked.map(c=>displayCountry(ccFromCountry(c))||c)]),lid:item.cc,cc:item.cc};
}
function genBrandQ(){
  if(\!BRANDS_DATA.length)return null;
  const _bp=_rfilt(BRANDS_DATA,3);const item=_bp[~~(rng()*_bp.length)];
  const corC=item.country;
  const sameSub=_bp.filter(b=>b.sub===item.sub&&b.country\!==corC).map(b=>b.country);
  const fallback=_bp.filter(b=>b.country\!==corC).map(b=>b.country);
  const _pool=[...new Set(sameSub.length>=3?sameSub:fallback)];
  const pool=_pool.length>=3?_pool:[...new Set(BRANDS_DATA.filter(b=>b.country\!==corC).map(b=>b.country))];
  const picked=sh(pool).slice(0,3);
  return{type:"brand",prompt:t("q_brand"),subj:item.brand,industry:item.industry,ans:displayCountry(item.cc)||corC,opts:sh([displayCountry(item.cc)||corC,...picked.map(c=>displayCountry(ccFromCountry(c))||c)]),lid:item.cc,cc:item.cc};
}
function genCurrencyQ(){
  if(\!CURRENCIES_DATA.length)return null;
  const _cp=_rfilt(CURRENCIES_DATA,3);const item=_cp[~~(rng()*_cp.length)];
  const corC=item.country;
  const sameSub=_cp.filter(c=>c.sub===item.sub&&c.country\!==corC).map(c=>c.country);
  const fallback=_cp.filter(c=>c.country\!==corC).map(c=>c.country);
  const _pool=[...new Set(sameSub.length>=3?sameSub:fallback)];
  const pool=_pool.length>=3?_pool:[...new Set(CURRENCIES_DATA.filter(c=>c.country\!==corC).map(c=>c.country))];
  const picked=sh(pool).slice(0,3);
  return{type:"currency",prompt:t("q_currency"),subj:item.currency,symbol:item.symbol,ans:displayCountry(item.cc)||corC,opts:sh([displayCountry(item.cc)||corC,...picked.map(c=>displayCountry(ccFromCountry(c))||c)]),lid:item.cc,cc:item.cc};
}
function genOutlineQ(){
  let pool=_rfilt(COUNTRIES.filter(c=>c.cc&&c.cc.length===2),4); if(pool.length<4) pool=COUNTRIES.filter(c=>c.cc&&c.cc.length===2); if(pool.length<4) return null;
  const sh2=arr=>{const a=[...arr];for(let i=a.length-1;i>0;i--){const j=~~(rng()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
  const idx=~~(rng()*pool.length);const item=pool[idx];
  const corC=item.c;const corCC=item.cc;
  const dis=pool.filter(c=>c.cc\!==corCC).map(c=>displayCountry(c.cc)||c.c);
  const picked=sh2(dis).slice(0,3);
  return{type:"outline",prompt:t("q_outline"),subj:corCC,ans:displayCountry(corCC)||corC,opts:sh2([displayCountry(corCC)||corC,...picked]),lid:corCC,cc:corCC};
}
/* EU-KENNZEICHEN GENERATORS (Phase 23B) – smart same-country distractors */
function genPlateQ(hardcore){
  const pool=PLATES_DATA;
  if(\!pool||pool.length<5)return null;
  const cor=pool[~~(rng()*pool.length)];
  const sameCountry=pool.filter(p=>p.country===cor.country&&p.region\!==cor.region);
  const disPool=sameCountry.length>=3?sameCountry:pool.filter(p=>p.region\!==cor.region);
  const picked=sh([...disPool]).slice(0,3).map(p=>p.region);
  const opts=sh([cor.region,...picked]);
  const cc_map={"Deutschland":"de","Österreich":"at","Schweiz":"ch","Polen":"pl","Frankreich":"fr","Italien":"it","Rumänien":"ro"};
  const cc=cc_map[cor.country]||"de";
  return{
    type:hardcore?"plate_hard":"plate_casual",
    prompt:hardcore?t("q_plates_hard"):t("q_plates_casual"),
    subj:cor.code,
    ans:cor.region,
    opts,
    meta:hardcore?"":cor.country+(cor.state?" \u00b7 "+cor.state:""),
    plateCountry:cor.country,
    lid:cor.code,
    cc,
  };
}

/* Phase 34: Map quiz countries */
const MAP_COUNTRIES=[{"cc":"fj","name":"Fiji"},{"cc":"tz","name":"Tanzania"},{"cc":"ca","name":"Canada"},{"cc":"us","name":"United States of America"},{"cc":"kz","name":"Kazakhstan"},{"cc":"uz","name":"Uzbekistan"},{"cc":"pg","name":"Papua New Guinea"},{"cc":"id","name":"Indonesia"},{"cc":"ar","name":"Argentina"},{"cc":"cl","name":"Chile"},{"cc":"cd","name":"Dem. Rep. Congo"},{"cc":"so","name":"Somalia"},{"cc":"ke","name":"Kenya"},{"cc":"sd","name":"Sudan"},{"cc":"td","name":"Chad"},{"cc":"ht","name":"Haiti"},{"cc":"do","name":"Dominican Rep."},{"cc":"ru","name":"Russia"},{"cc":"bs","name":"Bahamas"},{"cc":"no","name":"Norway"},{"cc":"za","name":"South Africa"},{"cc":"ls","name":"Lesotho"},{"cc":"mx","name":"Mexico"},{"cc":"uy","name":"Uruguay"},{"cc":"br","name":"Brazil"},{"cc":"bo","name":"Bolivia"},{"cc":"pe","name":"Peru"},{"cc":"co","name":"Colombia"},{"cc":"pa","name":"Panama"},{"cc":"cr","name":"Costa Rica"},{"cc":"ni","name":"Nicaragua"},{"cc":"hn","name":"Honduras"},{"cc":"sv","name":"El Salvador"},{"cc":"gt","name":"Guatemala"},{"cc":"bz","name":"Belize"},{"cc":"ve","name":"Venezuela"},{"cc":"gy","name":"Guyana"},{"cc":"sr","name":"Suriname"},{"cc":"fr","name":"France"},{"cc":"ec","name":"Ecuador"},{"cc":"jm","name":"Jamaica"},{"cc":"cu","name":"Cuba"},{"cc":"zw","name":"Zimbabwe"},{"cc":"bw","name":"Botswana"},{"cc":"na","name":"Namibia"},{"cc":"sn","name":"Senegal"},{"cc":"ml","name":"Mali"},{"cc":"mr","name":"Mauritania"},{"cc":"bj","name":"Benin"},{"cc":"ne","name":"Niger"},{"cc":"ng","name":"Nigeria"},{"cc":"cm","name":"Cameroon"},{"cc":"tg","name":"Togo"},{"cc":"gh","name":"Ghana"},{"cc":"ci","name":"Cß´te d'Ivoire"},{"cc":"gn","name":"Guinea"},{"cc":"gw","name":"Guinea-Bissau"},{"cc":"lr","name":"Liberia"},{"cc":"sl","name":"Sierra Leone"},{"cc":"bf","name":"Burkina Faso"},{"cc":"cf","name":"Central African Rep."},{"cc":"cg","name":"Congo"},{"cc":"ga","name":"Gabon"},{"cc":"gq","name":"Eq. Guinea"},{"cc":"zm","name":"Zambia"},{"cc":"mw","name":"Malawi"},{"cc":"mz","name":"Mozambique"},{"cc":"sz","name":"eSwatini"},{"cc":"ao","name":"Angola"},{"cc":"bi","name":"Burundi"},{"cc":"il","name":"Israel"},{"cc":"lb","name":"Lebanon"},{"cc":"mg","name":"Madagascar"},{"cc":"ps","name":"Palestine"},{"cc":"gm","name":"Gambia"},{"cc":"tn","name":"Tunisia"},{"cc":"dz","name":"Algeria"},{"cc":"jo","name":"Jordan"},{"cc":"ae","name":"United Arab Emirates"},{"cc":"qa","name":"Qatar"},{"cc":"kw","name":"Kuwait"},{"cc":"iq","name":"Iraq"},{"cc":"om","name":"Oman"},{"cc":"vu","name":"Vanuatu"},{"cc":"kh","name":"Cambodia"},{"cc":"th","name":"Thailand"},{"cc":"la","name":"Laos"},{"cc":"mm","name":"Myanmar"},{"cc":"vn","name":"Vietnam"},{"cc":"kp","name":"North Korea"},{"cc":"kr","name":"South Korea"},{"cc":"mn","name":"Mongolia"},{"cc":"in","name":"India"},{"cc":"bd","name":"Bangladesh"},{"cc":"bt","name":"Bhutan"},{"cc":"np","name":"Nepal"},{"cc":"pk","name":"Pakistan"},{"cc":"af","name":"Afghanistan"},{"cc":"tj","name":"Tajikistan"},{"cc":"kg","name":"Kyrgyzstan"},{"cc":"tm","name":"Turkmenistan"},{"cc":"ir","name":"Iran"},{"cc":"sy","name":"Syria"},{"cc":"am","name":"Armenia"},{"cc":"se","name":"Sweden"},{"cc":"by","name":"Belarus"},{"cc":"ua","name":"Ukraine"},{"cc":"pl","name":"Poland"},{"cc":"at","name":"Austria"},{"cc":"hu","name":"Hungary"},{"cc":"md","name":"Moldova"},{"cc":"ro","name":"Romania"},{"cc":"lt","name":"Lithuania"},{"cc":"lv","name":"Latvia"},{"cc":"ee","name":"Estonia"},{"cc":"de","name":"Germany"},{"cc":"bg","name":"Bulgaria"},{"cc":"gr","name":"Greece"},{"cc":"tr","name":"Turkey"},{"cc":"al","name":"Albania"},{"cc":"hr","name":"Croatia"},{"cc":"ch","name":"Switzerland"},{"cc":"lu","name":"Luxembourg"},{"cc":"be","name":"Belgium"},{"cc":"nl","name":"Netherlands"},{"cc":"pt","name":"Portugal"},{"cc":"es","name":"Spain"},{"cc":"ie","name":"Ireland"},{"cc":"nz","name":"New Zealand"},{"cc":"au","name":"Australia"},{"cc":"lk","name":"Sri Lanka"},{"cc":"cn","name":"China"},{"cc":"tw","name":"Taiwan"},{"cc":"it","name":"Italy"},{"cc":"dk","name":"Denmark"},{"cc":"gb","name":"United Kingdom"},{"cc":"is","name":"Iceland"},{"cc":"az","name":"Azerbaijan"},{"cc":"ge","name":"Georgia"},{"cc":"ph","name":"Philippines"},{"cc":"my","name":"Malaysia"},{"cc":"bn","name":"Brunei"},{"cc":"si","name":"Slovenia"},{"cc":"fi","name":"Finland"},{"cc":"sk","name":"Slovakia"},{"cc":"cz","name":"Czechia"},{"cc":"er","name":"Eritrea"},{"cc":"jp","name":"Japan"},{"cc":"py","name":"Paraguay"},{"cc":"ye","name":"Yemen"},{"cc":"sa","name":"Saudi Arabia"},{"cc":"cy","name":"Cyprus"},{"cc":"ma","name":"Morocco"},{"cc":"eg","name":"Egypt"},{"cc":"ly","name":"Libya"},{"cc":"et","name":"Ethiopia"},{"cc":"dj","name":"Djibouti"},{"cc":"ug","name":"Uganda"},{"cc":"rw","name":"Rwanda"},{"cc":"ba","name":"Bosnia and Herz."},{"cc":"mk","name":"Macedonia"},{"cc":"rs","name":"Serbia"},{"cc":"me","name":"Montenegro"},{"cc":"tt","name":"Trinidad and Tobago"},{"cc":"ss","name":"S. Sudan"}];

function genMapGuessQ(){
  if(\!MAP_COUNTRIES.length)return null;
  const idx=~~(rng()*MAP_COUNTRIES.length);
  const co=MAP_COUNTRIES[idx];if(\!co)return null;
  return{type:"map_guess",prompt:t("q_map_guess"),subj:co.name,
    ans:co.name,opts:[],meta:"",lid:co.cc,cc:co.cc};
}

function genMapReverseQ(){
  if(\!MAP_COUNTRIES.length)return null;
  const idx=~~(rng()*MAP_COUNTRIES.length);
  const co=MAP_COUNTRIES[idx];if(\!co)return null;
  const others=MAP_COUNTRIES.filter(c=>c.cc\!==co.cc);
  const _mLbl=c=>{const d=displayCountry(c.cc);return(d&&d!==c.cc)?d:c.name;};
  const dis=sh([...others]).slice(0,3).map(_mLbl);
  const ansLabel=_mLbl(co);
  return{type:"map_reverse",prompt:"Welches Land ist hervorgehoben?",
    subj:_mLbl(co),ans:ansLabel,opts:sh([ansLabel,...dis]),meta:"",lid:co.cc,cc:co.cc};
}

function genMapCapitalQ(){
  if(\!CAPITALS||\!CAPITALS.length)return null;
  const pool=CAPITALS.filter(c=>c.cc&&MAP_COUNTRIES.some(m=>m.cc===c.cc));
  if(\!pool.length)return null;
  const cor=pool[~~(rng()*pool.length)];
  const mapCo=MAP_COUNTRIES.find(m=>m.cc===cor.cc);
  if(\!mapCo)return null;
  return{type:"map_capital",
    prompt:"Tippe auf das Land, in dem "+esc(cor.capital)+" liegt…",
    subj:cor.capital,ans:mapCo.name,opts:[],meta:cor.capital,lid:cor.cc,cc:cor.cc};
}
/* Phase 129: Airport Trivia generators */
function genAirportCompareQ(){
  const keys=Object.keys(_AIRPORTS);
  if(keys.length<2)return null;
  const _fc=_rfilt(COUNTRIES,4);const _cc=new Set(_fc.map(x=>x.cc));
  let pool=keys.filter(k=>_cc.has(ccFromCountry(k)));
  if(pool.length<2)pool=keys.slice();
  if(pool.length<2)return null;
  const ai=~~(rng()*pool.length);
  let bi=~~(rng()*pool.length);
  while(bi===ai)bi=~~(rng()*pool.length);
  const a=pool[ai],b=pool[bi];
  const ans=_AIRPORTS[b]>_AIRPORTS[a]?b:a;
  const fmt=x=>x.toLocaleString()+" Flugh.";
  const meta=displayCountry(a)+": "+fmt(_AIRPORTS[a])+" \u00b7 "+displayCountry(b)+": "+fmt(_AIRPORTS[b]);
  return{type:"comp_airports",
    prompt:"\u2708\uFE0F Welches Land hat mehr Flugh\u00e4fen?",
    subj:"",opts:[a,b],ans,meta,lid:a+"|"+b,cc:ccFromCountry(ans),cat:"stats"};
}
function genIataQ(){
  const keys=Object.keys(_IATA);
  if(keys.length<4)return null;
  const ci=~~(rng()*keys.length);
  const iata=keys[ci];
  const correct=_IATA[iata];
  const allCities=Object.values(_IATA);
  const dis=allCities.filter(c=>c\!==correct).sort(()=>rng()-.5).slice(0,3);
  if(dis.length<3)return null;
  const opts=sh([correct,...dis]);
  return{type:"iata",
    prompt:"\u2708\uFE0F Welcher Flughafen-Code geh\u00f6rt zu welcher Stadt?",
    subj:iata,ans:correct,opts,meta:"IATA-Code",lid:iata,cc:null,cat:"trivia"};
}
/* Phase 130: 8 BETA generators */
function genTimezoneQ(){
  const cities=Object.keys(_TIMEZONES);
  if(cities.length<2)return null;
  const ai=~~(rng()*cities.length);
  let bi=~~(rng()*cities.length);while(bi===ai)bi=~~(rng()*cities.length);
  const cA=cities[ai],cB=cities[bi];
  const offA=_TIMEZONES[cA],offB=_TIMEZONES[cB];
  const baseHour=12;
  const correctHour=((baseHour+(offB-offA))%24+24)%24;
  const fmt=h=>String(h).padStart(2,"0")+":00 Uhr";
  const correct=fmt(correctHour);
  const wrongs=[];
  for(let d=1;d<=6;d++){
    const wh=((correctHour+d)%24+24)%24;
    const ws=fmt(wh);
    if(\!wrongs.includes(ws)&&ws\!==correct)wrongs.push(ws);
    if(wrongs.length>=3)break;
    const wh2=((correctHour-d)%24+24)%24;
    const ws2=fmt(wh2);
    if(\!wrongs.includes(ws2)&&ws2\!==correct)wrongs.push(ws2);
    if(wrongs.length>=3)break;
  }
  if(wrongs.length<3)return null;
  const opts=sh([correct,...wrongs.slice(0,3)]);
  return{type:"tz_quiz",
    prompt:"\u23F0 Wenn es in "+cA+" 12:00 Uhr ist – wie sp\u00e4t ist es in "+cB+"?",
    subj:cA+" \u2192 "+cB,ans:correct,opts,meta:"",lid:cA,cc:null,cat:"geo"};
}
function genClimateQ(){
  const keys=Object.keys(_CLIMATE_CLUES);
  if(keys.length<4)return null;
  const ci=~~(rng()*keys.length);
  const correct=keys[ci];
  const correctCc=ccFromCountry(correct)||"";
  if(\!correctCc)return null;
  const clues=_CLIMATE_CLUES[correct];
  /* P168: smart distractors — prefer same continent */
  const _ct=cc=>(COUNTRIES.find(c=>c.cc===cc)||{}).ct||null;
  const corCt=_ct(correctCc);
  let pool=keys.filter(k=>k\!==correct&&ccFromCountry(k));
  if(corCt){const sc=pool.filter(k=>{const kcc=ccFromCountry(k);return kcc&&_ct(kcc)===corCt;});if(sc.length>=3)pool=sc;}
  const dis=pool.slice().sort(()=>rng()-.5).slice(0,3);
  if(dis.length<3)return null;
  const opts=sh([correctCc,...dis.map(k=>ccFromCountry(k))]);
  const hint=clues.join(" \u00b7 ");
  return{type:"climate_quiz",
    prompt:"\u{1F326}\uFE0F Klima-Krimi: "+hint,
    subj:"Welches Land?",ans:correctCc,opts,meta:"",lid:correctCc,
    cc:correctCc,cat:"geo"};
}
function genFlagColorQ(){
  const allColours=["Schwarz","Rot","Gold","Blau","Wei\u00df","Gelb","Gr\u00fcn","Lila","Orange","Pink","Braun","T\u00fcrkis"];
  const keys=Object.keys(_FLAG_COLORS).filter(k=>_FLAG_COLORS[k].length>=2);
  if(keys.length===0)return null;
  const ci=~~(rng()*keys.length);
  const country=keys[ci];
  const flagCols=_FLAG_COLORS[country];
  const notInFlag=allColours.filter(c=>\!flagCols.includes(c));
  if(notInFlag.length===0)return null;
  const wrongColIdx=~~(rng()*notInFlag.length);
  const correct=notInFlag[wrongColIdx];
  const realCols=[...flagCols].sort(()=>rng()-.5).slice(0,3);
  while(realCols.length<3){realCols.push(flagCols[~~(rng()*flagCols.length)]);}
  const uniqueReal=[...new Set(realCols)].slice(0,3);
  if(uniqueReal.length<3)return null;
  const opts=sh([correct,...uniqueReal]);
  return{type:"flagcolor",
    prompt:"🎨 Welche Farbe kommt auf der Flagge von "+displayCountry(ccFromCountry(country))+" NICHT vor?",
    subj:displayCountry(ccFromCountry(country)),ans:correct,opts,meta:flagCols.join(", "),
    lid:country,cc:ccFromCountry(country),cat:"geo"};
}
function genFlightDistanceCompareQ(){
  const keys=Object.keys(COMP_AREA).filter(k=>COMP_AREA[k]>300000);
  if(keys.length<2)return null;
  const _fc=_rfilt(COUNTRIES,4);const _cc=new Set(_fc.map(x=>x.cc));
  let pool=keys.filter(k=>_cc.has(ccFromCountry(k)));
  if(pool.length<2)pool=keys.slice();
  const ai=~~(rng()*pool.length);
  let bi=~~(rng()*pool.length);while(bi===ai)bi=~~(rng()*pool.length);
  const a=pool[ai],b=pool[bi];
  const fmt=x=>x>=1e6?(x/1e6).toFixed(1)+" Mio. km\u00b2":(x/1000).toFixed(0)+" Tsd. km\u00b2";
  const ans=COMP_AREA[b]>COMP_AREA[a]?b:a;
  const meta=displayCountry(a)+": "+fmt(COMP_AREA[a])+" \u00b7 "+displayCountry(b)+": "+fmt(COMP_AREA[b]);
  return{type:"comp_flight",
    prompt:"\u2708\uFE0F In welchem Land ist der l\u00e4ngste Inlandsflug weiter?",
    subj:"",opts:[a,b],ans,meta,lid:a+"|"+b,cc:ccFromCountry(ans),cat:"geo"};
}
function genHighestPointCompareQ(){
  const keys=Object.keys(_ELEVATION);
  if(keys.length<2)return null;
  const _fc=_rfilt(COUNTRIES,4);const _cc=new Set(_fc.map(x=>x.cc));
  let pool=keys.filter(k=>_cc.has(ccFromCountry(k)));
  if(pool.length<2)pool=keys.slice();
  const ai=~~(rng()*pool.length);
  let bi=~~(rng()*pool.length);while(bi===ai)bi=~~(rng()*pool.length);
  const a=pool[ai],b=pool[bi];
  const fmt=x=>x.toLocaleString()+" m";
  const ans=_ELEVATION[b]>_ELEVATION[a]?b:a;
  const meta=displayCountry(a)+": "+fmt(_ELEVATION[a])+" \u00b7 "+displayCountry(b)+": "+fmt(_ELEVATION[b]);
  return{type:"comp_mountain",
    prompt:"\u26F0\uFE0F Welches Land hat den h\u00f6heren Gipfel?",
    subj:"",opts:[a,b],ans,meta,lid:a+"|"+b,cc:ccFromCountry(ans),cat:"geo"};
}
function genLandlockedQ(){
  if(\!_LANDLOCKED||_LANDLOCKED.length===0)return null;
  const ci=~~(rng()*_LANDLOCKED.length);
  const correct=_LANDLOCKED[ci];
  const allCountryNames=COUNTRIES.map(x=>x.c);
  const dis=allCountryNames
    .filter(c=>\!_LANDLOCKED.includes(c))
    .sort(()=>rng()-.5).slice(0,3);
  if(dis.length<3)return null;
  const opts=sh([correct,...dis]);
  return{type:"landlocked_quiz",
    prompt:"\u{1F30A} Welches dieser L\u00e4nder hat KEINEN Zugang zum Meer?",
    subj:"",ans:correct,opts,meta:"",lid:correct,
    cc:ccFromCountry(correct),cat:"geo"};
}
function genNorthSouthCompareQ(){
  const keys=Object.keys(_NS_EXTENT);
  if(keys.length<2)return null;
  const _fc=_rfilt(COUNTRIES,4);const _cc=new Set(_fc.map(x=>x.cc));
  let pool=keys.filter(k=>_cc.has(ccFromCountry(k)));
  if(pool.length<2)pool=keys.slice();
  const ai=~~(rng()*pool.length);
  let bi=~~(rng()*pool.length);while(bi===ai)bi=~~(rng()*pool.length);
  const a=pool[ai],b=pool[bi];
  const fmt=x=>x.toLocaleString()+" km";
  const ans=_NS_EXTENT[b]>_NS_EXTENT[a]?b:a;
  const meta=displayCountry(a)+": "+fmt(_NS_EXTENT[a])+" \u00b7 "+displayCountry(b)+": "+fmt(_NS_EXTENT[b]);
  return{type:"comp_nsextent",
    prompt:"\u{1F9ED} Welches Land ist von Nord nach S\u00fcd l\u00e4nger?",
    subj:"",opts:[a,b],ans,meta,lid:a+"|"+b,cc:ccFromCountry(ans),cat:"geo"};
}
function genOlympicCompareQ(){
  const keys=Object.keys(_OLYMPICS);
  if(keys.length<2)return null;
  const _fc=_rfilt(COUNTRIES,4);const _cc=new Set(_fc.map(x=>x.cc));
  let pool=keys.filter(k=>_cc.has(ccFromCountry(k)));
  if(pool.length<2)pool=keys.slice();
  const ai=~~(rng()*pool.length);
  let bi=~~(rng()*pool.length);while(bi===ai)bi=~~(rng()*pool.length);
  const a=pool[ai],b=pool[bi];
  const fmt=x=>x.toLocaleString()+" Goldmedaillen";
  const ans=_OLYMPICS[b]>_OLYMPICS[a]?b:a;
  const meta=displayCountry(a)+": "+fmt(_OLYMPICS[a])+" \u00b7 "+displayCountry(b)+": "+fmt(_OLYMPICS[b]);
  return{type:"comp_olympics",
    prompt:"\u{1F3C5} Welches Land hat mehr Olympia-Gold (Sommer)?",
    subj:"",opts:[a,b],ans,meta,lid:a+"|"+b,cc:ccFromCountry(ans),cat:"stats"};
}

/* ── IVR: International Vehicle Registration codes (Phase 170) ── */
const _IVR_CODES={
  "de":"D","at":"A","ch":"CH","fr":"F","it":"I","es":"E","pt":"P","gb":"GB",
  "nl":"NL","be":"B","lu":"L","dk":"DK","se":"S","no":"N","fi":"FIN",
  "is":"IS","ie":"IRL","pl":"PL","cz":"CZ","sk":"SK","hu":"H","ro":"RO",
  "bg":"BG","gr":"GR","tr":"TR","hr":"HR","si":"SLO","ba":"BIH","rs":"SRB",
  "me":"MNE","mk":"NMK","al":"AL","cy":"CY","mt":"M","mc":"MC","li":"FL",
  "sm":"RSM","ad":"AND","va":"V","lt":"LT","lv":"LV","ee":"EST",
  "by":"BY","ua":"UA","md":"MD","ru":"RUS","ge":"GE","am":"AM","az":"AZ",
  "us":"USA","ca":"CDN","mx":"MEX","br":"BR","ar":"RA","cl":"RCH",
  "co":"CO","pe":"PE","ve":"YV","uy":"ROU","bo":"BOL","py":"PY","ec":"EC",
  "au":"AUS","nz":"NZ","jp":"J","kr":"ROK","tw":"RC","in":"IND","pk":"PK",
  "th":"T","id":"RI","my":"MAL","sg":"SGP","za":"ZA","eg":"ET","ma":"MA",
  "tn":"TN","ng":"WAN","ke":"EAK","tz":"EAT","il":"IL","sa":"KSA",
  "ae":"UAE","ir":"IR","iq":"IRQ","jo":"HKJ","sy":"SYR","lb":"RL",
  "kw":"KWT","qa":"Q","om":"OM","bh":"BRN","kz":"KZ","uz":"UZ",
};
function genIvrQ(){
  const allCCs=Object.keys(_IVR_CODES);
  if(allCCs.length<4)return null;
  const corCC=allCCs[~~(rng()*allCCs.length)];
  const corIVR=_IVR_CODES[corCC];
  const corEntry=COUNTRIES.find(c=>c.cc===corCC)||{};
  const nameDe=(displayCountry(corCC)||"").toUpperCase().replace(/[^A-ZÀ-ɏ]/g,"");
  const nameEn=(corEntry.c||"").toUpperCase().replace(/[^A-ZÀ-ɏ]/g,"");
  // Derive plausible abbreviations from a name string
  function deriveFakes(name){
    if(!name)return[];
    const out=[];
    // Prefixes: first 1, 2, 3 letters
    for(let n=1;n<=3;n++) if(name.length>=n) out.push(name.slice(0,n));
    // Consonant skeleton: strip vowels, take first 3
    const cons=name.replace(/[AEIOUÀ-ÖØ-Þ]/g,"").slice(0,3);
    if(cons.length>=2) out.push(cons);
    return out;
  }
  // Generate candidates from both DE and EN names, dedupe, remove correct answer
  const raw=[...deriveFakes(nameDe),...deriveFakes(nameEn)];
  const seen=new Set([corIVR]);
  const fakes=[];
  for(const f of raw){
    if(f&&!seen.has(f)){seen.add(f);fakes.push(f);}
  }
  // Fallback: pad with first-letter + X/Z/N if somehow < 3
  while(fakes.length<3){
    const pad=(nameDe[0]||"X")+(["X","Z","N"][fakes.length]||"Q");
    if(!seen.has(pad)){seen.add(pad);fakes.push(pad);}
    else break;
  }
  const opts=sh([corIVR,...fakes.slice(0,3)]);
  const subj=displayCountry(corCC)||(corEntry.c||corCC.toUpperCase());
  return{type:"map_ivr",
    prompt:"\u{1F697}\u{1F194} Kennzeichen für "+subj+"?",
    subj,ans:corIVR,opts,meta:"IVR: "+corIVR,lid:corCC,cc:corCC};
}


/* ─── FOOTBALL-GEO DATA ─── */
const _footballData={
  stadiums:[
    {name:"Allianz Arena",city:"M\u00fcnchen",country:"Deutschland",cc:"de",cap:75024},
    {name:"Signal Iduna Park",city:"Dortmund",country:"Deutschland",cc:"de",cap:81365},
    {name:"Santiago Bern\u00e9bau",city:"Madrid",country:"Spanien",cc:"es",cap:81044},
    {name:"Camp Nou",city:"Barcelona",country:"Spanien",cc:"es",cap:99354},
    {name:"Wembley Stadium",city:"London",country:"England",cc:"gb",cap:90000},
    {name:"San Siro",city:"Mailand",country:"Italien",cc:"it",cap:75923},
    {name:"Stade de France",city:"Saint-Denis",country:"Frankreich",cc:"fr",cap:81338},
    {name:"Johan Cruyff ArenA",city:"Amsterdam",country:"Niederlande",cc:"nl",cap:54990},
    {name:"Est\u00e1dio da Luz",city:"Lissabon",country:"Portugal",cc:"pt",cap:64642},
    {name:"Olimpiyskiy",city:"Kiew",country:"Ukraine",cc:"ua",cap:70050},
    {name:"Luzhniki",city:"Moskau",country:"Russland",cc:"ru",cap:81000},
    {name:"Maracan\u00e3",city:"Rio de Janeiro",country:"Brasilien",cc:"br",cap:78838},
    {name:"Aztekenstadion",city:"Mexiko-Stadt",country:"Mexiko",cc:"mx",cap:87500},
    {name:"Melbourne Cricket Ground",city:"Melbourne",country:"Australien",cc:"au",cap:100024},
    {name:"Lusail Iconic Stadium",city:"Lusail",country:"Katar",cc:"qa",cap:88966},
  ],
  jerseys:[
    {country:"Deutschland",cc:"de",color:"#FFFFFF",style:"classic"},
    {country:"Brasilien",cc:"br",color:"#FDEF42",style:"classic"},
    {country:"Argentinien",cc:"ar",color:"#74ACDF",style:"stripes_v"},
    {country:"Niederlande",cc:"nl",color:"#FF6600",style:"classic"},
    {country:"Portugal",cc:"pt",color:"#CC0000",style:"classic"},
    {country:"Frankreich",cc:"fr",color:"#003399",style:"classic"},
    {country:"England",cc:"gb",color:"#FFFFFF",style:"classic"},
    {country:"Spanien",cc:"es",color:"#CC0000",style:"classic"},
    {country:"Italien",cc:"it",color:"#003399",style:"classic"},
    {country:"Kroatien",cc:"hr",color:"#FF0000",style:"checkered"},
    {country:"Jamaika",cc:"jm",color:"#009B3A",style:"split"},
    {country:"Mexiko",cc:"mx",color:"#006847",style:"classic"},
    {country:"Japan",cc:"jp",color:"#00235D",style:"classic"},
    {country:"Marokko",cc:"ma",color:"#C1272D",style:"classic"},
    {country:"Argentinien 2",cc:"ar",color:"#003366",style:"stripes_v"},
  ],
  crests:[
    {country:"Deutschland",cc:"de",shape:"eagle",color:"#000000"},
    {country:"Frankreich",cc:"fr",shape:"rooster",color:"#003399"},
    {country:"England",cc:"gb",shape:"lion",color:"#CC0000"},
    {country:"Spanien",cc:"es",shape:"shield",color:"#CC0000"},
    {country:"Italien",cc:"it",shape:"shield",color:"#003399"},
    {country:"Brasilien",cc:"br",shape:"diamond",color:"#009C3B"},
    {country:"Argentinien",cc:"ar",shape:"sun",color:"#74ACDF"},
    {country:"Portugal",cc:"pt",shape:"cross",color:"#006600"},
    {country:"Niederlande",cc:"nl",shape:"lion",color:"#FF6600"},
    {country:"Kroatien",cc:"hr",shape:"checker",color:"#FF0000"},
  ],
};
function _drawJersey(cc,color,style){
  const body=`<rect x="15" y="10" width="70" height="75" rx="5" fill="${color}"/><rect x="0" y="10" width="20" height="50" rx="3" fill="${color}"/><rect x="80" y="10" width="20" height="50" rx="3" fill="${color}"/>`;
  let overlay="";
  if(style==="stripes_v")overlay=`<rect x="15" y="10" width="14" height="75" fill="rgba(255,255,255,.5)"/><rect x="43" y="10" width="14" height="75" fill="rgba(255,255,255,.5)"/><rect x="71" y="10" width="14" height="75" rx="0 5 5 0" fill="rgba(255,255,255,.5)"/>`;
  else if(style==="checkered")overlay=`<rect x="15" y="10" width="35" height="37" fill="rgba(255,255,255,.5)"/><rect x="50" y="47" width="35" height="38" fill="rgba(255,255,255,.5)"/>`;
  else if(style==="split")overlay=`<rect x="50" y="10" width="35" height="75" rx="0 5 5 0" fill="rgba(0,0,0,.25)"/>`;
  else if(style==="stripes_h")overlay=`<rect x="15" y="28" width="70" height="14" fill="rgba(255,255,255,.5)"/><rect x="15" y="57" width="70" height="14" fill="rgba(255,255,255,.5)"/>`;
  const collar=`<path d="M40,10 Q50,22 60,10" fill="none" stroke="rgba(0,0,0,.3)" stroke-width="3"/>`;
  return `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="width:90px;height:90px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.4))">${body}${overlay}${collar}</svg>`;
}
function _drawCrest(shape,color){
  const s={"shield":`<polygon points="50,8 88,20 88,58 50,88 12,58 12,20" fill="${color}"/>`,
    "eagle":`<ellipse cx="50" cy="50" rx="32" ry="38" fill="${color}"/><polygon points="18,18 38,8 50,28 62,8 82,18 66,34 50,24 34,34" fill="${color}"/>`,
    "rooster":`<ellipse cx="50" cy="58" rx="28" ry="32" fill="${color}"/><ellipse cx="50" cy="22" rx="14" ry="16" fill="${color}"/>`,
    "lion":`<ellipse cx="50" cy="52" rx="32" ry="36" fill="${color}"/><path d="M30,28 Q50,12 70,28" fill="${color}"/>`,
    "diamond":`<polygon points="50,8 88,50 50,88 12,50" fill="${color}"/>`,
    "sun":`<circle cx="50" cy="50" r="28" fill="${color}"/><line x1="50" y1="8" x2="50" y2="20" stroke="${color}" stroke-width="5"/><line x1="50" y1="80" x2="50" y2="92" stroke="${color}" stroke-width="5"/><line x1="8" y1="50" x2="20" y2="50" stroke="${color}" stroke-width="5"/><line x1="80" y1="50" x2="92" y2="50" stroke="${color}" stroke-width="5"/><line x1="22" y1="22" x2="30" y2="30" stroke="${color}" stroke-width="5"/><line x1="70" y1="70" x2="78" y2="78" stroke="${color}" stroke-width="5"/><line x1="78" y1="22" x2="70" y2="30" stroke="${color}" stroke-width="5"/><line x1="30" y1="70" x2="22" y2="78" stroke="${color}" stroke-width="5"/>`,
    "cross":`<rect x="42" y="5" width="16" height="90" fill="${color}"/><rect x="5" y="42" width="90" height="16" fill="${color}"/>`,
    "checker":`<rect x="12" y="12" width="32" height="32" fill="${color}"/><rect x="56" y="12" width="32" height="32" fill="${color}"/><rect x="12" y="56" width="32" height="32" fill="${color}"/><rect x="56" y="56" width="32" height="32" fill="${color}"/>`,
  };
  return `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="width:90px;height:90px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.4))">${s[shape]||s.shield}</svg>`;
}

/* ─── Beta Kennzeichen-Vergleich ─── */
function genPlateCompareQ(){
  const pool=Object.keys(COMP_DATA).filter(k=>{
    const cc=ccFromCountry(k);
    return cc&&COMP_DATA[k].dens>0;
  });
  if(pool.length<2)return null;
  const METRICS=[
    {key:"gdp",  prompt:"\u{1F9EA} [BETA] Welches Land hat das höhere BIP pro Kopf?", fmt:v=>"$"+v.toLocaleString()},
    {key:"dens", prompt:"\u{1F9EA} [BETA] Welches Land ist dichter besiedelt?",        fmt:v=>v+" Ew/km²"},
    {key:"life", prompt:"\u{1F9EA} [BETA] In welchem Land lebt man länger?",           fmt:v=>v+" Jahre"},
    {key:"age",  prompt:"\u{1F9EA} [BETA] Welches Land hat das höhere Medianalter?",   fmt:v=>v+" Jahre"},
    {key:"forest",prompt:"\u{1F9EA} [BETA] Welches Land hat mehr Waldfläche?",        fmt:v=>v+" %"},
  ];
  const m=METRICS[~~(rng()*METRICS.length)];
  const valid=pool.filter(k=>COMP_DATA[k][m.key]!=null&&COMP_DATA[k][m.key]>0);
  if(valid.length<2)return null;
  let ai=~~(rng()*valid.length),bi=~~(rng()*valid.length);
  while(bi===ai)bi=~~(rng()*valid.length);
  const kA=valid[ai],kB=valid[bi];
  const ccA=ccFromCountry(kA)||"",ccB=ccFromCountry(kB)||"";
  /* Get plate codes for display */
  const _getCode=cc=>{
    const p=PLATES_DATA.find(x=>x.code&&ccFromPlateCountry(x.country)===cc);
    if(p)return p.code;
    const e=Object.entries(PLATE_COUNTRY_EN||{}).find(([de])=>ccFromCountry(de)===cc);
    return e?e[0].substring(0,3).toUpperCase():cc.toUpperCase();
  };
  const codeA=_getCode(ccA)||kA.substring(0,3).toUpperCase();
  const codeB=_getCode(ccB)||kB.substring(0,3).toUpperCase();
  const vA=COMP_DATA[kA][m.key],vB=COMP_DATA[kB][m.key];
  const ans=vA>vB?kA:kB;
  const meta=kA+": "+m.fmt(vA)+" · "+kB+": "+m.fmt(vB);
  return{type:"plate_compare",prompt:m.prompt,subj:"",opts:[kA,kB],ans,meta,lid:kA+"|"+kB,cc:ccA,_codeA:codeA,_codeB:codeB};
}
/* Phase 170: Unique opts helper — prevents correct answer appearing in distractors */
function _uOpts(ans,pool,n){
  /* pool: array of distractor values; ans: correct answer string */
  const seen=new Set([String(ans)]);
  const out=[];
  for(const v of pool){const s=String(v);if(!seen.has(s)){seen.add(s);out.push(v);if(out.length>=n)break;}}
  return sh([ans,...out]);
}
function genFootballQ(mode){
  const type=mode||"stadium";
  if(type==="stadium"){
    const d=_footballData.stadiums,idx=~~(Math.random()*d.length),cor=d[idx];
    const _disPool=d.filter((_,i)=>i!==idx).sort(()=>Math.random()-.5).map(x=>x.country);
    return{type:"stadium",prompt:"\u26BD In welchem Land steht dieses Stadion?",subj:cor.name,ans:cor.country,opts:_uOpts(cor.country,_disPool,3),meta:cor.city+", "+cor.cap.toLocaleString()+" Pl\u00e4tze",cc:cor.cc};
  }
  if(type==="jersey"){
    const d=_footballData.jerseys,idx=~~(Math.random()*d.length),cor=d[idx];
    const _disPool=d.filter((_,i)=>i!==idx).sort(()=>Math.random()-.5).map(x=>x.country);
    return{type:"jersey",prompt:"\u{1F455} Welches Land tr\u00e4gt dieses Trikot?",subj:{cc:cor.cc,color:cor.color,style:cor.style},ans:cor.country,opts:_uOpts(cor.country,_disPool,3),meta:"",cc:cor.cc};
  }
  if(type==="crest"){
    const d=_footballData.crests,idx=~~(Math.random()*d.length),cor=d[idx];
    const _disPool=d.filter((_,i)=>i!==idx).sort(()=>Math.random()-.5).map(x=>x.country);
    return{type:"crest",prompt:"\u{1F6E1} Welchem Land geh\u00f6rt dieses Wappen?",subj:{shape:cor.shape,color:cor.color},ans:cor.country,opts:_uOpts(cor.country,_disPool,3),meta:"",cc:cor.cc};
  }
  return null;
}

/* Phase 166 — BETA_GAMEDATA: 28 beta game modes */
const BETA_GAMEDATA={
b1:[
  {q:"Welches Land spielt in Orange, obwohl die Flagge Rot/Weiß/Blau zeigt?",a:"Netherlands",fakes:["Belgium","Denmark","Croatia"]},
  {q:"Welches Land trägt den Spitznamen 'Azzurri' und spielt in Blau (nicht in der Flagge)?",a:"Italy",fakes:["France","Greece","Portugal"]},
  {q:"Welches Land ist für seine komplett schwarzen Rugby-Trikots ('All Blacks') weltberühmt?",a:"New Zealand",fakes:["Australia","South Africa","England"]},
  {q:"Welches Land spielte in Weiß als Heimtrikot, obwohl die Flagge Schwarz/Rot/Gold trägt?",a:"Germany",fakes:["Austria","Poland","Switzerland"]}
],
b2:[
  {q:"Silverstone – Heimat des Britischen Grand Prix. Klicke auf das Land.",answer:"United Kingdom"},
  {q:"Interlagos – Heimat des Brasilianischen Grand Prix. Klicke auf das Land.",answer:"Brazil"},
  {q:"Monza – Heimat des Italienischen Grand Prix. Klicke auf das Land.",answer:"Italy"},
  {q:"Suzuka – Heimat des Japanischen Grand Prix. Klicke auf das Land.",answer:"Japan"},
  {q:"Spa-Francorchamps – Heimat des Belgischen Grand Prix. Klicke auf das Land.",answer:"Belgium"}
],
b4:[
  {q:"Welches Land war Gastgeber der Sommer-Olympiade 1996 (Atlanta)?",a:"United States",fakes:["Australia","Greece","Japan"]},
  {q:"Welches Land richtete die Sommerspiele 2004 aus?",a:"Greece",fakes:["Australia","Spain","China"]},
  {q:"Welches Land war Gastgeber der Sommerspiele 2016 (Rio)?",a:"Brazil",fakes:["Argentina","Japan","United States"]},
  {q:"Welches Land richtete die Sommerspiele 2012 (London) aus?",a:"United Kingdom",fakes:["France","Germany","Spain"]},
  {q:"Welches Land war Gastgeber der Sommerspiele 2008 (Peking)?",a:"China",fakes:["Japan","South Korea","India"]}
],
b6:[
  {q:"Sumo ist die traditionelle Nationalsportart von ...?",a:"Japan",fakes:["China","South Korea","Mongolia"]},
  {q:"Taekwondo wurde als moderner Sport in welchem Land entwickelt?",a:"South Korea",fakes:["Japan","China","Thailand"]},
  {q:"Capoeira stammt ursprünglich aus ...?",a:"Brazil",fakes:["Angola","Cuba","Colombia"]},
  {q:"Kabaddi gilt als inoffizieller Nationalsport von ...?",a:"India",fakes:["Bangladesh","Pakistan","Sri Lanka"]},
  {q:"Welches Land gilt als Geburtsort des modernen Fußballs (FA-Regeln 1863)?",a:"England",fakes:["Germany","Scotland","Italy"]}
],
b7:[
  {nameA:"Hernando Siles (La Paz)",nameB:"Allianz Arena (München)",prompt:"Welches Stadion liegt höher über dem Meeresspiegel?",ans:"Hernando Siles (La Paz)",metaA:"3.637 m",metaB:"517 m"},
  {nameA:"Estadio Azteca (Mexiko-Stadt)",nameB:"Camp Nou (Barcelona)",prompt:"Welches Stadion liegt höher über dem Meeresspiegel?",ans:"Estadio Azteca (Mexiko-Stadt)",metaA:"2.210 m",metaB:"57 m"},
  {nameA:"Stade de Suisse (Bern)",nameB:"Anfield (Liverpool)",prompt:"Welches Stadion liegt höher über dem Meeresspiegel?",ans:"Stade de Suisse (Bern)",metaA:"572 m",metaB:"26 m"},
  {nameA:"Türk Telekom Stadyum (Istanbul)",nameB:"Wembley (London)",prompt:"Welches Stadion liegt höher über dem Meeresspiegel?",ans:"Türk Telekom Stadyum (Istanbul)",metaA:"212 m",metaB:"35 m"}
],
b9:[
  {q:"Wo wurde Basketball erfunden (1891, James Naismith)?",a:"United States",fakes:["Canada","England","Australia"]},
  {q:"In welchem Land entstand Judo als moderner Kampfsport (Kodokan, 1882)?",a:"Japan",fakes:["China","South Korea","Thailand"]},
  {q:"Wo wurde Tischtennis (Ping-Pong) in den 1880ern erfunden?",a:"England",fakes:["China","Japan","Germany"]},
  {q:"Volleyball wurde 1895 in welchem Land erfunden?",a:"United States",fakes:["Brazil","Canada","Germany"]},
  {q:"Welches Land gilt als Geburtsort des modernen Rugby (Rugby School, 1823)?",a:"England",fakes:["France","Ireland","Scotland"]}
],
b11:[
  {q:"Wie weit liegen Dortmund (Signal Iduna Park) und Schalke (Veltins-Arena) auseinander?",a:"Ca. 25 km",fakes:["Ca. 3 km","Ca. 100 km","Ca. 200 km"]},
  {q:"Wie weit trennt Old Trafford (Man Utd) vom Etihad Stadium (Man City)?",a:"Ca. 4 km",fakes:["Ca. 500 m","Ca. 25 km","Ca. 15 km"]},
  {q:"Wie weit sind Bernabéu (Real Madrid) und Metropolitano (Atlético)?",a:"Ca. 7 km",fakes:["Ca. 1 km","Ca. 30 km","Ca. 50 km"]},
  {q:"Wie weit liegen La Bombonera (Boca Juniors) und El Monumental (River Plate) auseinander?",a:"Ca. 12 km",fakes:["Ca. 500 m","Ca. 50 km","Ca. 2 km"]}
],
b17:[
  {nameA:"Norway",nameB:"Germany",prompt:"Welches Land hat mehr Winter-Olympia-Gold?",ans:"Norway",metaA:"ca. 148 Gold",metaB:"ca. 92 Gold"},
  {nameA:"United States",nameB:"France",prompt:"Welches Land hat mehr Winter-Olympia-Gold?",ans:"United States",metaA:"ca. 107 Gold",metaB:"ca. 36 Gold"},
  {nameA:"Norway",nameB:"Sweden",prompt:"Welches Land hat mehr Winter-Olympia-Gold?",ans:"Norway",metaA:"ca. 148 Gold",metaB:"ca. 57 Gold"},
  {nameA:"Austria",nameB:"Netherlands",prompt:"Welches Land hat mehr Winter-Olympia-Gold?",ans:"Austria",metaA:"ca. 70 Gold",metaB:"ca. 45 Gold"}
],
b19:[
  {q:"Welches Riesenland hat sich NOCH NIE für eine Fußball-WM qualifiziert?",a:"India",fakes:["Brazil","China","Mexico"]},
  {q:"Welches europäische Schwergewicht scheiterte an der WM-Quali für Russland 2018?",a:"Italy",fakes:["Germany","Spain","France"]},
  {q:"Welches Land qualifizierte sich bisher nur EINMAL für eine WM (2002)?",a:"China",fakes:["Japan","South Korea","Australia"]},
  {q:"Welches Land scheiterte erneut an der WM-Quali für Katar 2022?",a:"Italy",fakes:["Portugal","Netherlands","Sweden"]}
],
b20:[
  {q:"In welcher Stadt spielt das NBA-Team 'Lakers'?",a:"Los Angeles",fakes:["Chicago","Boston","Miami"]},
  {q:"In welchem Land spielen die 'Springboks' Rugby?",a:"South Africa",fakes:["New Zealand","Australia","Argentina"]},
  {q:"Das Baseball-Team 'Yankees' kommt aus ...?",a:"New York",fakes:["Chicago","Los Angeles","Boston"]},
  {q:"In welchem Land spielt das Cricket-Team der 'Baggy Greens'?",a:"Australia",fakes:["England","India","South Africa"]}
],
b21:[
  {q:"Welches Land ist komplett vom Territorium Italiens umschlossen (kein Meereszugang)?",a:"San Marino",fakes:["Monaco","Liechtenstein","Andorra"]},
  {q:"Welches afrikanische Land ist vollständig von Südafrika umschlossen?",a:"Lesotho",fakes:["Eswatini","Botswana","Zambia"]},
  {q:"Welches kleine Land liegt zwischen Deutschland, Österreich und der Schweiz?",a:"Liechtenstein",fakes:["Luxembourg","Andorra","Monaco"]},
  {q:"Welches kleine Land grenzt genau an Belgien, Frankreich und Deutschland?",a:"Luxembourg",fakes:["Liechtenstein","Andorra","San Marino"]}
],
b22:[
  {q:"Von Deutschland nach Kaliningrad (Russland) fährt man auf Landweg zwingend durch ...?",a:"Poland",fakes:["Czech Republic","Ukraine","Lithuania"]},
  {q:"Von Frankreich nach Spanien durch die Pyrenäen liegt welcher Kleinstaat auf dem Weg?",a:"Andorra",fakes:["Monaco","Liechtenstein","San Marino"]},
  {q:"Von Österreich in Richtung Türkei (direkter Landweg) kommt man zwingend durch ...?",a:"Hungary",fakes:["Poland","Switzerland","Italy"]},
  {q:"Von Norwegen nach Portugal fährt man zwingend durch (südlichster Pflichtstaat) ...?",a:"Spain",fakes:["Belgium","Austria","Hungary"]}
],
b23:[
  {q:"Hat die Schweiz einen direkten Zugang zum Meer?",a:"Nein – Binnenstaat",fakes:["Ja, via Bodensee","Ja, via Mittelmeer","Ja, via Rhein-Delta"]},
  {q:"Hat Österreich einen Zugang zum Meer?",a:"Nein – Binnenstaat seit 1918",fakes:["Ja, Adria","Ja, Nordsee","Ja, Schwarzes Meer"]},
  {q:"Hat Bolivien aktuell einen Meereszugang?",a:"Nein – Pazifik-Zugang 1879 verloren",fakes:["Ja, Pazifik","Ja, Atlantik","Ja, via Amazonas"]},
  {q:"Hat die Mongolei einen Meereszugang?",a:"Nein – doppelt eingeschlossen",fakes:["Ja, Beringmeer","Ja, Chinesisches Meer","Ja, Kaspisee"]}
],
b25:[
  {q:"Welcher Nachbar fehlt? Deutschland grenzt an: Dänemark, Polen, Tschechien, Österreich, Schweiz, Frankreich, Luxemburg, Belgien ...",a:"Netherlands",fakes:["Hungary","Slovakia","Slovenia"]},
  {q:"Welcher Nachbar fehlt? Frankreich grenzt an: Belgien, Luxemburg, Deutschland, Schweiz, Italien, Monaco, Andorra ...",a:"Spain",fakes:["Portugal","Netherlands","Austria"]},
  {q:"Welcher Nachbar fehlt? Polen grenzt an: Deutschland, Tschechien, Ukraine, Belarus, Russland, Litauen ...",a:"Slovakia",fakes:["Latvia","Moldova","Romania"]},
  {q:"Welcher Nachbar fehlt? Türkei grenzt an: Griechenland, Bulgarien, Georgien, Armenien, Iran, Irak, Syrien ...",a:"Azerbaijan",fakes:["Russia","Ukraine","Kazakhstan"]}
],
b29:[
  {q:"Mit welchem Land teilt Russland seine längste Landgrenze (~7.644 km)?",a:"Kazakhstan",fakes:["China","Mongolia","Belarus"]},
  {q:"Mit welchem Land teilt China seine längste Landgrenze (~4.677 km)?",a:"Mongolia",fakes:["Russia","India","Kazakhstan"]},
  {q:"Mit welchem Land teilt Indien seine längste Landgrenze (~4.156 km)?",a:"Bangladesh",fakes:["Pakistan","China","Nepal"]},
  {q:"Mit welchem Land teilt Brasilien seine längste Landgrenze (~3.423 km)?",a:"Bolivia",fakes:["Argentina","Venezuela","Peru"]}
],
b37:[
  {nameA:"Wien–Bratislava",nameB:"Paris–Madrid",prompt:"Welches Hauptstadtpaar liegt NAEHER beieinander?",ans:"Wien–Bratislava",metaA:"ca. 55 km",metaB:"ca. 1.274 km"},
  {nameA:"Berlin–Warschau",nameB:"London–Dublin",prompt:"Welches Hauptstadtpaar liegt NAEHER beieinander?",ans:"London–Dublin",metaA:"ca. 574 km",metaB:"ca. 464 km"},
  {nameA:"Lissabon–Madrid",nameB:"Prag–Wien",prompt:"Welches Hauptstadtpaar liegt NAEHER beieinander?",ans:"Prag–Wien",metaA:"ca. 503 km",metaB:"ca. 293 km"},
  {nameA:"Oslo–Stockholm",nameB:"Rom–Berlin",prompt:"Welches Hauptstadtpaar liegt NAEHER beieinander?",ans:"Oslo–Stockholm",metaA:"ca. 416 km",metaB:"ca. 1.539 km"}
],
b40:[
  {nameA:"China",nameB:"Brazil",prompt:"Welches Land hat mehr direkte Landgrenzen?",ans:"China",metaA:"14 Nachbarn",metaB:"10 Nachbarn"},
  {nameA:"Germany",nameB:"France",prompt:"Welches Land hat mehr direkte Landgrenzen?",ans:"Germany",metaA:"9 Nachbarn",metaB:"8 Nachbarn"},
  {nameA:"Russia",nameB:"United States",prompt:"Welches Land hat mehr direkte Landgrenzen?",ans:"Russia",metaA:"16 Nachbarn",metaB:"2 Nachbarn"},
  {nameA:"Brazil",nameB:"Australia",prompt:"Welches Land hat mehr direkte Landgrenzen?",ans:"Brazil",metaA:"10 Nachbarn",metaB:"0 Nachbarn"}
],
b41:[
  {q:"Klicke auf ein Land das vom Äquator durchquert wird (Tipp: Westafrika).",answer:"Gabon"},
  {q:"Klicke auf ein Land das vom Äquator durchquert wird (Tipp: Suedamerika).",answer:"Brazil"},
  {q:"Klicke auf ein Land das vom Äquator durchquert wird (Tipp: Suedostasien).",answer:"Indonesia"},
  {q:"Klicke auf ein Land das vom Äquator durchquert wird (Tipp: Ostafrika).",answer:"Kenya"}
],
b42:[
  {q:"Klicke auf das Land mit dem groessten Tropenwald der Welt (Amazonas).",answer:"Brazil"},
  {q:"Klicke auf das suedostasiatische Land mit riesigen Tropenwaelder (Borneo/Sumatra).",answer:"Indonesia"},
  {q:"Klicke auf dieses suedamerikanische Land – bekannt fuer Artenvielfalt und Tropenwald.",answer:"Colombia"},
  {q:"Klicke auf das zentralafrikanische Land mit dem zweitgroessten Tropenwald der Welt.",answer:"Dem. Rep. Congo"}
],
b44:[
  {q:"Was liegt weiter NOERDLICH: Rom oder New York?",a:"Rome (41.9N)",fakes:["New York (40.7N)","Beide gleich (40N)","Madrid (40.4N)"]},
  {q:"Was liegt weiter NOERDLICH: Madrid oder Peking?",a:"Madrid (40.4N)",fakes:["Beijing (39.9N)","Beide gleich","Tokyo (35.7N)"]},
  {q:"Was liegt weiter NOERDLICH: Moskau oder Oslo?",a:"Oslo (59.9N)",fakes:["Moscow (55.8N)","Beide gleich","Helsinki (60.2N)"]},
  {q:"Was liegt weiter SUEDLICH: Sydney oder Buenos Aires?",a:"Buenos Aires (34.6S)",fakes:["Sydney (33.9S)","Beide gleich","Cape Town (33.9S)"]}
],
b45:[
  {q:"Welches skandinavische Land hat den hoechsten EV-Neuwagen-Marktanteil (ueber 80 Prozent)?",answer:"Norway"},
  {q:"Welches Land fuehrt weltweit bei der Gesamtzahl zugelassener Elektrofahrzeuge?",answer:"China"},
  {q:"Welches europaeische Land hat die hoechste EV-Ladesaeulendichte pro km Strassennetz?",answer:"Netherlands"},
  {q:"In welchem nordeuropaeischen Land war der EV-Marktanteil 2023 weltweit am hoechsten?",answer:"Norway"}
],
b46:[
  {q:"Die Iguazu-Wasserfall-Anlage liegt an der Grenze von Argentinien und Brasilien. Klicke auf Argentinien.",answer:"Argentina"},
  {q:"Der Grand Canyon liegt in welchem Land? Klicke auf die Karte.",answer:"United States of America"},
  {q:"Das Great Barrier Reef liegt vor der Kueste welches Landes?",answer:"Australia"},
  {q:"Der Kilimandscharo (hoechster Berg Afrikas) liegt in welchem Land?",answer:"Tanzania"}
],
b47:[
  {q:"Wenn du in Spanien ein Loch durch den Erdmittelpunkt graebst, wo kommst du heraus?",a:"Pazifischer Ozean (nahe Neuseeland)",fakes:["In Australien","In China","In Argentinien"]},
  {q:"Wenn du in Neuseeland durch die Erde graebst, wo kommst du heraus?",a:"Spanien / Portugal",fakes:["Brasilien","Marokko","Groenland"]},
  {q:"Die Antipode von Peking liegt in der Naehe von ...?",a:"Patagonien (Argentinien/Chile)",fakes:["Australien","Atlantik","Madagaskar"]},
  {q:"Die Antipode von Brasilien liegt im ...?",a:"Indischen Ozean / Suedostasien",fakes:["Atlantik","Suedafrika","Australien"]}
],
b51:[
  {q:"Klicke auf das Land mit der Atacama-Wueste (trockenste Wueste der Welt).",answer:"Chile"},
  {q:"Klicke auf das Land in dem die Namib-Wueste liegt.",answer:"Namibia"},
  {q:"Klicke auf das Land in dem die Gobi-Wueste hauptsaechlich liegt.",answer:"Mongolia"},
  {q:"Klicke auf das Land mit dem groessten Teil der Sahara-Wueste.",answer:"Algeria"}
],
b53:[
  {q:"In welchem Land liegt der Panama-Kanal?",a:"Panama",fakes:["Mexico","Costa Rica","Colombia"]},
  {q:"Die Strasse von Gibraltar liegt an den Kuesten von zwei Laendern. Welche?",a:"Spain und Morocco",fakes:["Portugal und Algeria","France und Tunisia","Gibraltar und Libya"]},
  {q:"In welchem Land liegt der Suezkanal?",a:"Egypt",fakes:["Israel","Jordan","Saudi Arabia"]},
  {q:"Die Strasse von Malakka liegt zwischen welchen Laendern?",a:"Malaysia und Indonesia",fakes:["India und Sri Lanka","Thailand und Vietnam","Philippines und China"]}
],
b54:[
  {q:"Klicke auf das Land in dem der Mount Everest (8.849 m) liegt.",answer:"Nepal"},
  {q:"Klicke auf das Land in dem der Elbrus (hoechster Berg Europas 5.642 m) liegt.",answer:"Russia"},
  {q:"Klicke auf das Land in dem der Kilimandscharo (hoechster Berg Afrikas 5.895 m) liegt.",answer:"Tanzania"},
  {q:"Klicke auf das Land in dem der Aconcagua (hoechster Berg Suedamerikas 6.961 m) liegt.",answer:"Argentina"}
],
b58:[
  {q:"Klicke auf Tansania – eines der drei Laender am Viktoriasee (groesster See Afrikas).",answer:"Tanzania"},
  {q:"Klicke auf das Land mit dem groessten Kuestenanteil am Kaspischen Meer.",answer:"Russia"},
  {q:"Klicke auf das suedamerikanische Land mit dem groesseren Anteil am Titicacasee.",answer:"Peru"},
  {q:"Klicke auf das Land in dem der Baikalsee (tiefster See der Welt 1.642 m) liegt.",answer:"Russia"}
],
b60:[
  {q:"Welche Region leuchtet auf Nachtsatellitenaufnahmen am hellsten?",a:"Westeuropa und US-Ostkueste",fakes:["Sahara-Region","Amazonasbecken","Zentralasien"]},
  {q:"Welches Land hat einen dunklen Norden und hellen Sueden (von Satelliten sichtbar)?",a:"North Korea vs. South Korea",fakes:["China vs. Mongolia","Egypt vs. Sudan","Mexico vs. Guatemala"]},
  {q:"Welcher Kontinent leuchtet pro Flaeche am schwaechsten auf Nacht-Satellitenaufnahmen?",a:"Africa",fakes:["Australia","South America","Antarctica"]},
  {q:"Welcher isolierte Lichtpunkt leuchtet mitten im Nordatlantik von Satelliten sichtbar?",a:"Iceland (Reykjavik)",fakes:["Azores (Portugal)","Faroe Islands","Greenland"]}
]
};

/* Phase 166: genBetaMCQ */
function genBetaMCQ(bId){
  const pool=BETA_GAMEDATA["b"+bId];
  if(!pool||!pool.length)return null;
  const d=pool[~~(rng()*pool.length)];
  if(!d||!d.a||!d.fakes)return null;
  const opts=_uOpts(d.a,d.fakes,3);
  return{type:"beta_mcq",prompt:"\u{1F9EA} [BETA] "+d.q,subj:d.subj||"",ans:d.a,opts,meta:d.meta||"",lid:"bmcq_"+bId,cc:ccFromCountry(d.a)||"de"};
}

/* Phase 166: genBetaHL */
function genBetaHL(bId){
  const pool=BETA_GAMEDATA["b"+bId];
  if(!pool||!pool.length)return null;
  const d=pool[~~(rng()*pool.length)];
  if(!d||!d.nameA||!d.nameB)return null;
  const meta=d.nameA+": "+(d.metaA||"?")+" \u00b7 "+d.nameB+": "+(d.metaB||"?");
  return{type:"beta_hl",prompt:"\u{1F9EA} [BETA] "+(d.prompt||"Welches ist mehr?"),subj:"",opts:[d.nameA,d.nameB],ans:d.ans,meta,lid:"bhl_"+bId,cc:ccFromCountry(d.ans)||"de"};
}

/* Phase 166: genBetaSpotter */
function genBetaSpotter(bId){
  const pool=BETA_GAMEDATA["b"+bId];
  if(!pool||!pool.length)return null;
  const d=pool[~~(rng()*pool.length)];
  if(!d||!d.answer)return null;
  return{type:"beta_spotter",prompt:"\u{1F9EA} [BETA] Weltkarte",subj:d.q,ans:d.answer,opts:[],meta:"",lid:"bspot_"+bId,cc:ccFromCountry(d.answer)||"de"};
}

const GEN={
  city:genCityQ,flag:genFlagQ,capital:genCapitalQ,river:genRiverQ,
  landmark:genLandmarkQ,park:genParkQ,unesco:genUnescoQ,citymark:genCitymarkQ,
  subway:genSubwayQ,flagsel:genFlagselQ,rcapital:genRcapitalQ,rcity:genRcityQ,
  rriver:genRriverQ,outline:genOutlineQ,food:genFoodQ,brand:genBrandQ,currency:genCurrencyQ,
  plate_casual:()=>genPlateQ(false),
  plate_hard:()=>genPlateQ(true),
  curr_real:genCurrRealQ,
  pop_compare:genPopCompareQ,
  river_real:genRiverRealQ,
  hl_pop:genHLPopQ,
  hl_river:genHLRiverQ,
  hl_area:genHLAreaQ,
  hl_gdp:genHLGdpQ,hl_density:genHLDensityQ,hl_elevation:genHLElevationQ,
  hl_coastline:genHLCoastlineQ,hl_borders:genHLBordersQ,hl_lifeexp:genHLLifeexpQ,
  hl_median_age:genHLMedianAgeQ,hl_forest:genHLForestQ,
  hl_b_rain:()=>genHLBeta("hl_b_rain"),hl_b_temp:()=>genHLBeta("hl_b_temp"),
  hl_b_sun:()=>genHLBeta("hl_b_sun"),hl_b_vulc:()=>genHLBeta("hl_b_vulc"),
  hl_b_parks:()=>genHLBeta("hl_b_parks"),hl_b_roads:()=>genHLBeta("hl_b_roads"),
  hl_b_rail:()=>genHLBeta("hl_b_rail"),hl_b_net:()=>genHLBeta("hl_b_net"),
  hl_b_ev:()=>genHLBeta("hl_b_ev"),hl_b_urban:()=>genHLBeta("hl_b_urban"),
  hl_b_lang:()=>genHLBeta("hl_b_lang"),hl_b_isl:()=>genHLBeta("hl_b_isl"),
  hl_b_tz:()=>genHLBeta("hl_b_tz"),hl_b_founded:()=>genHLBeta("hl_b_founded"),
  hl_b_unesco:()=>genHLBeta("hl_b_unesco"),hl_b_tour:()=>genHLBeta("hl_b_tour"),
  hl_b_wm:()=>genHLBeta("hl_b_wm"),
  comp_area:genCompAreaQ,comp_pop:genCompPopQ,comp_north:genCompNorthQ,
  comp_gdp:genCompGdpQ,comp_density:genCompDensityQ,comp_elevation:genCompElevQ,
  comp_coast:genCompCoastQ,comp_borders:genCompBordersQ,
  comp_life:genCompLifeQ,comp_age:genCompAgeQ,comp_forest:genCompForestQ,
  neighbor:genNeighborQ,
  neighbor_fake:genNeighborFakeQ,
  neighbor_count:genNeighborCountQ,
  map_guess:genMapGuessQ,
  map_reverse:genMapReverseQ,
  map_capital:genMapCapitalQ,
  map_ivr:genIvrQ,
  logic_grid:()=>null,
  travel_route:()=>null,
  wappen_meister:genWappenQ,
  slf:()=>null,
  comp_airports:genAirportCompareQ,
  iata:genIataQ,
  tz_quiz:genTimezoneQ,
  climate_quiz:genClimateQ,
  flagcolor:genFlagColorQ,
  comp_flight:genFlightDistanceCompareQ,
  comp_mountain:genHighestPointCompareQ,
  landlocked_quiz:genLandlockedQ,
  comp_nsextent:genNorthSouthCompareQ,
  comp_olympics:genOlympicCompareQ,
  /* P139: newly-activated new_modes entries wired to existing generators */
  climate_mystery:genClimateQ,
  flag_fusion:genFlagColorQ,
  timezone_jumper:genTimezoneQ,
  plate_compare:genPlateCompareQ,
  stadium:()=>genFootballQ("stadium"),
  jersey:()=>genFootballQ("jersey"),
  crest:()=>genFootballQ("crest"),
  /* Phase 166: 28 beta modes */
  b1:()=>genBetaMCQ(1),b2:()=>genBetaSpotter(2),b4:()=>genBetaMCQ(4),
  b6:()=>genBetaMCQ(6),b7:()=>genBetaHL(7),b9:()=>genBetaMCQ(9),
  b11:()=>genBetaMCQ(11),b17:()=>genBetaHL(17),b19:()=>genBetaMCQ(19),
  b20:()=>genBetaMCQ(20),
  b21:()=>genBetaMCQ(21),b22:()=>genBetaMCQ(22),b23:()=>genBetaMCQ(23),
  b25:()=>genBetaMCQ(25),b29:()=>genBetaMCQ(29),b37:()=>genBetaHL(37),
  b40:()=>genBetaHL(40),
  b41:()=>genBetaSpotter(41),b42:()=>genBetaSpotter(42),b44:()=>genBetaMCQ(44),
  b45:()=>genBetaSpotter(45),b46:()=>genBetaSpotter(46),b47:()=>genBetaMCQ(47),
  b51:()=>genBetaSpotter(51),b53:()=>genBetaMCQ(53),b54:()=>genBetaSpotter(54),
  b58:()=>genBetaSpotter(58),b60:()=>genBetaMCQ(60),
};

/* GAME LOOP */
/* P154: Global error boundary — prevents silent white-screen crashes */
function _sendBugMail(subject, body){
  /* ── KONFIG: Ersetze diese Adresse mit deiner echten E-Mail ── */
  const _BUG_MAIL="farndt691@gmail.com"; /* <<< HIER E-MAIL EINTRAGEN */
  window.location.href="mailto:"+_BUG_MAIL
    +"?subject="+encodeURIComponent(subject)
    +"&body="+encodeURIComponent(body);
}
window.onerror=function(m,u,l,c,e){
  console.error("🛑 CRASH SHIELD:",m,"at",u+":"+l);
  const app=document.getElementById("app");
  if(!app)return false;
  const stateSnap=(typeof S!=="undefined")?JSON.stringify({mode:S.mode,ph:S.ph,rd:S.rd,sc:S.sc,diff:S.diff}).substring(0,400):"(kein State)";
  const errTxt=String(m)+(u?" @ "+u+":"+l:"");
  app.innerHTML=`<div style="min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:1.5rem;background:#0f172a;text-align:center">
    <div style="font-size:3rem;margin-bottom:1rem">🛑</div>
    <div style="font-size:1.1rem;font-weight:900;color:#f87171;margin-bottom:.5rem">GeoQuest ist abgestürzt</div>
    <div style="font-size:.78rem;color:#94a3b8;margin-bottom:1.2rem;max-width:320px;word-break:break-word">${errTxt}</div>
    <button onclick="(function(){
      const body='Hallo Entwickler,\n\nmein Spiel ist gerade abgestürzt.\nBitte hänge hier ggf. einen Screenshot an.\n\n--- TECHNISCHE DATEN ---\nFehler: ${errTxt.replace(/'/g,'\\x27')}\nState: ${stateSnap.replace(/'/g,'\\x27')}';
      _sendBugMail('GeoQuest Crash-Report', body);
    })()" style="background:#ef4444;color:#fff;border:none;border-radius:12px;padding:.7rem 1.4rem;font-size:.88rem;font-weight:700;cursor:pointer;margin-bottom:.75rem">🐞 Fehlerbericht senden</button>
    <button onclick="location.reload()" style="background:#1e293b;color:#94a3b8;border:1px solid #334155;border-radius:12px;padding:.6rem 1.2rem;font-size:.82rem;cursor:pointer">🔄 Neu laden</button>
  </div>`;
  return true; /* prevent default browser error */
};
function clr(){clearInterval(tIv);clearTimeout(fTo);clearTimeout(S.freezeTimer);S.freezeTimer=null;}

/* ─── LOCAL 1:1 HOT-SEAT MODE ─── */
const LV_ROUNDS=10,LV_TIME=15;
const LV_MODES=[
  {id:"random",label:"Zuf\u00e4llig \u{1F500}"},
  {id:"flag",label:"Flaggen \u{1F3F3}"},
  {id:"capital",label:"Hauptst\u00e4dte \u{1F3DB}"},
  {id:"comp_area",label:"Fl\u00e4che \u{1F30F}"},
  {id:"comp_pop",label:"Einwohner \u{1F465}"},
];
function initLV(){
  const mode=S.lvSetupMode==="random"?null:S.lvSetupMode;
  S.lv={round:0,phase:"q",p1:{name:"Spieler 1",sc:0},p2:{name:"Spieler 2",sc:0},current:1,q:null,sel:null,timer:LV_TIME,mode};
  _lvNext();
}
function _lvNext(){
  if(!S.lv)return;
  clearInterval(tIv);
  const lv=S.lv;
  if(lv.round>=LV_ROUNDS){lv.phase="gameover";render();return;}
  lv.phase="q";lv.sel=null;lv.timer=LV_TIME;
  const modeId=lv.mode||(["flag","capital","city","comp_area","comp_pop","comp_north"][~~(Math.random()*6)]);
  const genFn=GEN[modeId]||genFlagQ;
  lv.q=genFn()||genFlagQ();
  render();
  tIv=setInterval(()=>{
    if(!S.lv)return clearInterval(tIv);
    S.lv.timer--;
    const te=document.getElementById("lv-timer");
    if(te){
      te.textContent=S.lv.timer+"s";
      te.style.color=S.lv.timer<=5?"#ef4444":S.lv.timer<=10?"#f59e0b":"#10b981";
    }
    if(S.lv.timer<=0){clearInterval(tIv);lvAnswer(null);}
  },1000);
}
function lvAnswer(ans){
  if(!S.lv||S.lv.phase!=="q")return;
  clearInterval(tIv);
  const lv=S.lv;
  lv.sel=ans;lv.phase="fb";
  const correct=ans!==null&&ans===lv.q.ans;
  if(correct){if(lv.current===1)lv.p1.sc++;else lv.p2.sc++;}
  render();
  setTimeout(()=>{
    if(!S.lv)return;
    if(lv.current===1){lv.current=2;}else{lv.current=1;lv.round++;}
    _lvNext();
  },1800);
}
function renderLVModal(){
  if(!S.lv)return renderLVSetup();
  if(S.lv.phase==="gameover")return renderLVGameover();
  const lv=S.lv,q=lv.q,isFb=lv.phase==="fb",pl=lv.current===1?lv.p1:lv.p2;
  const optsHtml=q&&q.opts?q.opts.map(o=>{
    let cls="btn-base";
    if(isFb){if(o===q.ans)cls+=" ok";else if(o===lv.sel&&o!==q.ans)cls+=" ng";else cls+=" dm";}
    return `<button class="${cls}" data-lv="${(o||'').replace(/&/g,'&amp;').replace(/"/g,'&quot;')}" onclick="lvAnswer(this.dataset.lv)" ${isFb?"disabled":""}>${displayCountry(o)||o}</button>`;
  }).join(""):"";
  const tCol=lv.timer<=5?"#ef4444":lv.timer<=10?"#f59e0b":"#10b981";
  /* Build question body depending on type */
  const isFlag=q&&(q.type==="flag"||q.type==="flagsel");
  const isComp=q&&(q.type&&(q.type.startsWith("comp_")||q.type.startsWith("hl_b_")));
  let qDisplay="";
  if(isFlag&&q.subj){
    const _lcc=String(q.subj||"").toLowerCase();
    qDisplay=`<img src="https://flagcdn.com/h80/${_lcc}.png" style="max-height:70px;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,.15);margin:.3rem 0">`;
  }else if(isComp){
    /* comp modes: show the two country names + flags inline */
    const _oA=q.opts&&q.opts[0]||"",_oB=q.opts&&q.opts[1]||"";
    qDisplay=`<div style="display:flex;gap:1rem;justify-content:center;align-items:center;margin:.3rem 0">
      <div style="text-align:center"><div style="font-size:1.6rem">${flagOf(_oA)}</div><div style="font-size:.7rem;font-weight:700;color:var(--text2)">${esc(displayCountry(_oA)||_oA)}</div></div>
      <div style="font-weight:900;color:var(--text3)">VS</div>
      <div style="text-align:center"><div style="font-size:1.6rem">${flagOf(_oB)}</div><div style="font-size:.7rem;font-weight:700;color:var(--text2)">${esc(displayCountry(_oB)||_oB)}</div></div>
    </div>`;
  }else if(q&&q.subj){
    qDisplay=`<div class="qmain" style="font-size:1.5rem;font-weight:900;color:var(--text);margin:.25rem 0">${esc(q.subj)}</div>`;
  }
  return `<div style="min-height:100vh;background:var(--bg);padding:1rem;display:flex;flex-direction:column">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.75rem">
      <button class="btn-cancel" onclick="clearInterval(tIv);S.lvModal=false;S.lv=null;render()">\u00d7 Beenden</button>
      <div style="font-size:.75rem;color:var(--text3);font-weight:700">RUNDE ${lv.round+1}/${LV_ROUNDS}</div>
      <div id="lv-timer" style="font-size:1.2rem;font-weight:900;color:${tCol}">${lv.timer}s</div>
    </div>
    <div style="display:flex;gap:.5rem;margin-bottom:.75rem">
      <div style="flex:1;padding:.5rem;border-radius:10px;background:${lv.current===1?"rgba(99,102,241,.2)":"var(--bg2)"};border:2px solid ${lv.current===1?"#6366f1":"transparent"};text-align:center;cursor:pointer" onclick="const n=prompt('Name Spieler 1:',lv.p1.name);if(n&&n.trim())lv.p1.name=n.trim();render()">
        <div style="font-size:.6rem;color:var(--text3)">\u270F\uFE0F ${lv.p1.name}</div>
        <div style="font-size:1.4rem;font-weight:900;color:var(--text)">${lv.p1.sc}</div>
      </div>
      <div style="flex:1;padding:.5rem;border-radius:10px;background:${lv.current===2?"rgba(236,72,153,.2)":"var(--bg2)"};border:2px solid ${lv.current===2?"#ec4899":"transparent"};text-align:center;cursor:pointer" onclick="const n=prompt('Name Spieler 2:',lv.p2.name);if(n&&n.trim())lv.p2.name=n.trim();render()">
        <div style="font-size:.6rem;color:var(--text3)">\u270F\uFE0F ${lv.p2.name}</div>
        <div style="font-size:1.4rem;font-weight:900;color:var(--text)">${lv.p2.sc}</div>
      </div>
    </div>
    <div style="background:var(--bg2);border-radius:12px;padding:.75rem;margin-bottom:.75rem;text-align:center">
      <div style="font-size:.7rem;font-weight:700;color:${lv.current===1?"#6366f1":"#ec4899"};margin-bottom:.3rem">\u{1F3AE} ${esc(pl.name)} ist dran</div>
      ${q?`<div class="qprompt" style="font-size:.95rem;margin-bottom:.35rem">${q.prompt}</div>${qDisplay}`:""}
    </div>
    <div class="ans-grid">${optsHtml}</div>
    ${isFb?`<div style="text-align:center;margin-top:.5rem;font-size:.8rem;color:${lv.sel===q.ans?"#10b981":"#ef4444"};font-weight:700">${lv.sel===q.ans?"\u2705 Richtig!":"\u274C Falsch \u2013 "+(displayCountry(q.ans)||q.ans)}</div>`:""}
  </div>`;
}
function renderLVSetup(){
  const modesHtml=LV_MODES.map(m=>`<button class="btn-base${S.lvSetupMode===m.id?" ok":""}" onclick="S.lvSetupMode='${m.id}';render()">${m.label}</button>`).join("");
  return `<div style="min-height:100vh;background:var(--bg);padding:1.5rem;display:flex;flex-direction:column;align-items:center;justify-content:center">
    <button class="btn-cancel" style="align-self:flex-start;margin-bottom:1rem" onclick="S.lvModal=false;render()">\u00d7 Zur\u00fcck</button>
    <div style="font-size:2rem;margin-bottom:.5rem">\u{1F3AE}</div>
    <div style="font-size:1.3rem;font-weight:900;color:var(--text);margin-bottom:.3rem">Lokal 1:1</div>
    <div style="font-size:.78rem;color:var(--text3);margin-bottom:1.5rem">Zwei Spieler \u00b7 Ein Ger\u00e4t \u00b7 ${LV_ROUNDS} Runden</div>
    <div style="width:100%;max-width:360px">
      <div style="font-size:.7rem;font-weight:700;color:var(--text3);margin-bottom:.5rem">MODUS W\u00c4HLEN</div>
      <div class="ans-grid" style="margin-bottom:1rem">${modesHtml}</div>
      <button class="btn-p" style="width:100%" onclick="initLV()">\u{1F680} Spiel starten</button>
    </div>
  </div>`;
}
function renderLVGameover(){
  const lv=S.lv;
  const winner=lv.p1.sc>lv.p2.sc?lv.p1:lv.p2.sc>lv.p1.sc?lv.p2:null;
  return `<div style="min-height:100vh;background:var(--bg);padding:1.5rem;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
    <div style="font-size:3rem;margin-bottom:.5rem">${winner?"\u{1F3C6}":"\u{1F91D}"}</div>
    <div style="font-size:1.5rem;font-weight:900;color:var(--text);margin-bottom:.25rem">${winner?winner.name+" gewinnt!":"Unentschieden!"}</div>
    <div style="display:flex;gap:1rem;margin:1.5rem 0">
      <div style="flex:1;background:var(--bg2);border-radius:12px;padding:1rem">
        <div style="font-size:.7rem;color:var(--text3)">${lv.p1.name}</div>
        <div style="font-size:2.5rem;font-weight:900;color:${lv.p1.sc>lv.p2.sc?"#10b981":"var(--text)"}">${lv.p1.sc}</div>
      </div>
      <div style="flex:1;background:var(--bg2);border-radius:12px;padding:1rem">
        <div style="font-size:.7rem;color:var(--text3)">${lv.p2.name}</div>
        <div style="font-size:2.5rem;font-weight:900;color:${lv.p2.sc>lv.p1.sc?"#10b981":"var(--text)"}">${lv.p2.sc}</div>
      </div>
    </div>
    <button class="btn-p" style="width:100%;max-width:320px;margin-bottom:.75rem" onclick="initLV()">\u{1F504} Nochmal spielen</button>
    <button class="btn-g" style="width:100%;max-width:320px" onclick="S.lvModal=false;S.lv=null;render()">Hauptmen\u00fc</button>
  </div>`;
}

function nextRound(){
  clr();
  const nr=S.rd+1;
  if(S.diff!=="survival"&&nr>=ROUNDS){
    S.ph="gameover";S.scoreSaved=false;S.convModal=true;soundOver();checkMastery();
    if(S.isDailyRun&&!isDailyDone()){markDailyDone(S.sc);if(sbProfile)sbProfile.geo_coins=(sbProfile.geo_coins||0)+100;if(sb&&sbUser)sb.rpc("add_coins",{p_user_id:sbUser.id,p_amount:100}).then(r=>{if(r.data!=null&&sbProfile)sbProfile.geo_coins=r.data;},()=>{});}
    saveHistory({mode:S.mode,score:S.sc,correct:S.correct,rounds:ROUNDS,date:Date.now(),answers:S.sessionAnswers.map(a=>({cc:a.cc,correct:a.correct}))});
    if(sbOK)saveSession(S.mode,S.sc,S.bs,S.correct,Date.now()-(S.gameStartTime||Date.now())).then(()=>{S.scoreSaved=true;render();});
    render();
  }else{S.rd=nr;lq();}
}
function lq(){ console.log("🟢 [TRACKER] 2. lq (loadQuestion) gestartet.");
  clearInterval(tIv);
  if(\!S.queueExtra)S.queueExtra=[];
  if(\!S.askedLids)S.askedLids=new Set();
  const _mCfg=(typeof GAME_MODES!=="undefined"?GAME_MODES:[]).find(m=>m.id===S.mode);const dur=S.diff==="survival"?8:(_mCfg&&_mCfg.time)||12;
  /* Try up to 25 times to get a question whose lid hasn't appeared this round */
  let q=null,_att=0;
  while(_att<25){
    const _c=(GEN[S.mode]||genCityQ)();
    if(_c&&\!S.askedLids.has(_c.lid)){q=_c;break;}
    _att++;
  }
  /* Fallback: accept any valid question if pool is exhausted */
  if(\!q)q=(GEN[S.mode]||genCityQ)()||null;
  /* Duolingo casual: once normal round exhausted, pull retries */
  if(\!q&&S.diff==="casual"&&S.queueExtra.length>0)q=S.queueExtra.shift();
  if(\!q){S.ph="menu";render();return;}
  S.askedLids.add(q.lid);
  S.q=q;S.tm=dur;S.dur=dur;S.sel=null;S.ok=null;S.ph="playing";S.qRenderedAt=Date.now()+180; /* allow 180ms buffer for render */;
  S.half_removed=false;S.freezeActive=false;
  render();
  /* P167: for landscape-required modes, defer timer until device is rotated */
  if(_LANDSCAPE_MODES_SET.has(S.mode)&&_isPortrait()){
    S.waitingForLandscape=true;
  }else{
    S.waitingForLandscape=false;
    if(typeof tIv !== 'undefined') clearInterval(tIv); tIv=setInterval(()=>{S.tm--;if(S.tm===3)soundWarn(); render();if(S.tm<=0){clearInterval(tIv);if(S.q)answer(null,_secretGameToken);} },1000);
  }
}

/* â”€â”€ Phase 42: Index-based answer dispatch (hides answer strings from DOM) â”€â”€ */
function answerByIdx(i){
  if(!S.q||!S.q.opts||i<0||i>=S.q.opts.length)return;
  answer(S.q.opts[i],_secretGameToken);
}
document.addEventListener("keydown",function(e){
  if(S.ph==="playing"&&S.q&&S.sel===null&&!["INPUT","TEXTAREA","SELECT"].includes(document.activeElement?.tagName)){
    const k=parseInt(e.key);
    if(k>=1&&k<=4){e.preventDefault();answerByIdx(k-1);}
  }
});
function answer(a,tok){
  if(tok!==_secretGameToken){if(typeof tok!=="undefined")console.warn("%c\uD83D\uDEAB GeoQuest Anti-Cheat: invalid token","color:#ef4444;font-weight:bold");return;}
  if(!S||!S.q)return; /* P143: guard against missing question */
  if(S.sel\!==null)return;
  if(S.qRenderedAt&&Date.now()-S.qRenderedAt<250)return; /* anti-cheat: ignore clicks <250ms after render */
  clr();
  const ok=a===S.q.ans;
  S.sel=a||"__t";S.ok=ok;
  if(S.q.cc)S.sessionAnswers.push({cc:S.q.cc,correct:ok});
  let pts=0;
  if(ok){const ns=S.st+1,t=tier(ns);if(S.diff==="casual"){pts=10;}else if(S.diff==="survival"){pts=20+S.tm;S.survTimeBonusTotal=(S.survTimeBonusTotal||0)+S.tm;}else{/* hardcore */S.hcMult=Math.min(2.5,parseFloat((+(S.hcMult||1.0)+0.1).toFixed(1)));S.hcMaxMult=Math.max(S.hcMaxMult||1.0,S.hcMult);pts=Math.round(15*S.hcMult);}S.sc+=pts;S.st=ns;S.bs=Math.max(S.bs,ns);S.correct++;soundCorrect();if(ns>=3)setTimeout(()=>soundStreak(ns),250);showPtsPopup(pts);if(navigator.vibrate)navigator.vibrate([50]);}
  else{S.st=0;if(S.diff==="hardcore"){S.hcMult=1.0;}soundWrong();if(navigator.vibrate)navigator.vibrate([100,50,100]);
    /* Lives system: casual=infinite(999), hardcore/survival=3 */
    if(S.diff!=="casual"){
      S.lives=(S.lives||3)-1;
      if(S.lives<=0){
        clr();
        const survived=S.rd;
        if(S.diff==="survival"){
          const sb_prev=parseInt(localStorage.getItem('gq_surv_best')||'0');
          if(survived>sb_prev)localStorage.setItem('gq_surv_best',String(survived));
          S.survivalBest=Math.max(survived,sb_prev);
          if(sb&&sbUser)sb.from("profiles").update({survival_best:Math.max(survived,sbProfile?.survival_best||0)}).eq("id",sbUser.id).then(()=>{},()=>{});
        }
        S.ph="gameover";S.scoreSaved=false;S.convModal=true;soundOver();checkMastery();
        saveHistory({mode:S.mode,score:S.sc,correct:S.correct,rounds:survived,date:Date.now(),diff:S.diff,answers:S.sessionAnswers.map(a=>({cc:a.cc,correct:a.correct}))});
        if(sbOK)saveSession(S.mode,S.sc,S.bs,S.correct,Date.now()-(S.gameStartTime||Date.now())).then(()=>{S.scoreSaved=true;render();});
        S.pts=pts;S.lid=S.q.lid;render();
        return;
      }
    }
    /* Casual: retry wrong question */
    if(S.diff==="casual"&&\!S.q._retry){if(\!S.queueExtra)S.queueExtra=[];S.queueExtra.push({...S.q,_retry:true});}
  }
  /* Phase 43: collect plate with code::country key */
  if(ok&&(S.mode==="plate_casual"||S.mode==="plate_hard")&&S.q.subj){
    const _code=S.q.subj;
    const _pc=PLATES_DATA.find(p=>p.code===_code);
    if(_pc){
      const _key=collKey(_code,_pc.country);
      if(\!S.collectedPlates.includes(_key)){
        S.collectedPlates.push(_key);saveCollectedPlates(S.collectedPlates);saveCollectedTs(_key,Date.now());
        const _allR=PLATES_DATA.filter(p=>p.code===_code&&p.country===_pc.country);
        showToast("â­ Neu: "+_code+" – "+_pc.region+(_allR.length>1?" +"+(_allR.length-1)+" weitere":"")+"!");
      }
    }
  }
  S.pts=pts;S.lid=S.q.lid;S.ph="feedback";render();
  /* Phase 33 Teil 2 */
  if(window.mpGameCh&&S.mpOpponent){
    window.mpGameCh.send({type:"broadcast",event:"score_update",
      payload:{score:S.sc,rd:S.rd,correct:S.correct}}).then(()=>{},()=>{});
  }
  /* P133: longer delay for text-heavy beta/IATA questions */
  const _qt=S.q&&S.q.type||"";
  const _fd=_qt==="iata"?2800:1900;
  fTo=setTimeout(()=>{
    const nr=S.rd+1;
    if(S.diff\!=="survival"&&nr>=ROUNDS){
      S.ph="gameover";S.scoreSaved=false;S.convModal=true;soundOver();checkMastery();
      if(S.isDailyRun&&\!isDailyDone()){
        markDailyDone(S.sc);
        if(sbProfile)sbProfile.geo_coins=(sbProfile.geo_coins||0)+100;
        if(sb&&sbUser)sb.rpc("add_coins",{p_user_id:sbUser.id,p_amount:100}).then(r=>{if(r.data!=null&&sbProfile)sbProfile.geo_coins=r.data;},()=>{});
      }
      saveHistory({mode:S.mode,score:S.sc,correct:S.correct,rounds:ROUNDS,date:Date.now(),answers:S.sessionAnswers.map(a=>({cc:a.cc,correct:a.correct}))});
      if(sbOK)saveSession(S.mode,S.sc,S.bs,S.correct,Date.now()-(S.gameStartTime||Date.now())).then(()=>{S.scoreSaved=true;render();});
      render();
    }else{S.rd=nr;lq();}
  },_fd);
}
function getSmartVersusOpponent(country,categoryKey){
const filteredCountries=COUNTRIES.filter(c=>c[categoryKey]!=null&&typeof c[categoryKey]==='number');
if(filteredCountries.length<3){return COUNTRIES[Math.floor(Math.random()*COUNTRIES.length)];}
filteredCountries.sort((a,b)=>a[categoryKey]-b[categoryKey]);
const currentIdx=filteredCountries.findIndex(c=>c.cc===country.cc);
if(currentIdx<0){return filteredCountries[Math.floor(Math.random()*filteredCountries.length)];}
const countryValue=country[categoryKey];
let selectedIdx=-1;
let attempts=0;
let attempts2=0;
while(selectedIdx<0&&attempts2<2){
attempts2++;
const proximityRange=[Math.max(0,currentIdx-2),Math.max(0,currentIdx-1),Math.min(filteredCountries.length-1,currentIdx+1),Math.min(filteredCountries.length-1,currentIdx+2)];
const validNeighbors=proximityRange.filter(idx=>idx!==currentIdx&&idx>=0&&idx<filteredCountries.length);
if(validNeighbors.length===0){return filteredCountries[currentIdx];}
attempts=0;
for(const startIdx of validNeighbors){
let checkIdx=startIdx;
for(let i=0;i<filteredCountries.length&&attempts<20;i++){
if(checkIdx>=0&&checkIdx<filteredCountries.length&&checkIdx!==currentIdx){
const candidateValue=filteredCountries[checkIdx][categoryKey];
if(candidateValue!==countryValue){
selectedIdx=checkIdx;
break;
}
}
checkIdx++;
attempts++;
if(checkIdx>=filteredCountries.length)break;
}
if(selectedIdx>=0)break;
}
if(selectedIdx<0){
currentIdx=Math.floor(Math.random()*filteredCountries.length);
}
}
if(selectedIdx<0||selectedIdx===currentIdx){
return filteredCountries[Math.floor(Math.random()*filteredCountries.length)];
}
return filteredCountries[selectedIdx];
}

function setCorrectAnswerObfuscated(countries,answer,correctCountry){
const idx=countries.findIndex(c=>c.c===correctCountry||c.country===correctCountry);
S._cIdx=idx;
S._cSalt=Math.random();
}
function validateAnswerByIndex(countries,givenIdx){
return givenIdx===S._cIdx;
}
function getCorrectAnswerIndex(){
return S._cIdx||0;
}
function createCooldownWrapper(originalFunc){
return function(...args){
if(S.isProcessing){
console.warn('Button locked: processing previous answer');
return;
}
S.isProcessing=true;
try{
originalFunc.apply(this,args);
}finally{
setTimeout(()=>{S.isProcessing=false;},600);
}
};
}

// PHASE 174: Offline Culture & Nature Database
const globalCultureData={
'jp':{food:'Sushi',climate:'Gemäßigt bis subtropisch',landmark:'Mount Fuji',region:'East Asia'},
'th':{food:'Pad Thai',climate:'Tropisch-feuchtes Klima',landmark:'Wat Arun',region:'Southeast Asia'},
'in':{food:'Curry',climate:'Tropisch-Monsun',landmark:'Taj Mahal',region:'South Asia'},
'id':{food:'Gado-Gado',climate:'Tropisches Regenwaldklima',landmark:'Borobudur-Tempel',region:'Southeast Asia'},
'vn':{food:'Pho',climate:'Tropisch',landmark:'Ha-Long-Bucht',region:'Southeast Asia'},
'cn':{food:'Peking-Ente',climate:'Vielfältig (subtropisch bis gemäßigt)',landmark:'Große Mauer',region:'East Asia'},
'kr':{food:'Kimchi',climate:'Gemäßigt kontinental',landmark:'Gyeongbokgung-Palast',region:'East Asia'},
'tw':{food:'Xiaolongbao',climate:'Subtropisch',landmark:'Chiang Kai-shek Memorial',region:'East Asia'},
'it':{food:'Pasta & Pizza',climate:'Mittelmeerklima',landmark:'Kolosseum',region:'Southern Europe'},
'fr':{food:'Croissant & Käse',climate:'Gemäßigt ozeanisch',landmark:'Eiffelturm',region:'Western Europe'},
'es':{food:'Paella',climate:'Mittelmeerklima',landmark:'Sagrada Familia',region:'Southern Europe'},
'de':{food:'Schnitzel & Brezel',climate:'Gemäßigt kontinental',landmark:'Brandenburger Tor',region:'Central Europe'},
'gr':{food:'Souvlaki',climate:'Mittelmeerklima',landmark:'Parthenon',region:'Southern Europe'},
'ru':{food:'Borschtsch',climate:'Kontinental bis subarktisch',landmark:'Rotes Platz & Kreml',region:'Eastern Europe'},
'uk':{food:'Borschtsch & Pelmeni',climate:'Gemäßigt kontinental',landmark:'Sophienkathedrale',region:'Eastern Europe'},
'pt':{food:'Pastéis de Nata',climate:'Mittelmeerklima',landmark:'Ponte Dom Luß­s I',region:'Western Europe'},
'se':{food:'Köttbullar',climate:'Kalt-gemäßigt',landmark:'Vasamuseum',region:'Northern Europe'},
'no':{food:'Lachssuppe',climate:'Kalt-gemäßigt',landmark:'Geirangerfjord',region:'Northern Europe'},
'dk':{food:'Smß¸rrebrß¸d',climate:'Kalt-gemäßigt ozeanisch',landmark:'Schloss Kronborg',region:'Northern Europe'},
'us':{food:'Hamburger & BBQ',climate:'Vielfältig',landmark:'Freiheitsstatue',region:'North America'},
'ca':{food:'Poutine',climate:'Kalt-gemäßigt',landmark:'Niagarafälle',region:'North America'},
'mx':{food:'Tacos & Mole',climate:'Tropisch bis trocken',landmark:'Chichen Itza',region:'Central America'},
'br':{food:'Feijoada',climate:'Tropisch & subtropisch',landmark:'Cristo Redentor',region:'South America'},
'ar':{food:'Asado',climate:'Gemäßigt',landmark:'Teatro Colon',region:'South America'},
'pe':{food:'Ceviche',climate:'Vielfältig (trocken bis tropisch)',landmark:'Machu Picchu',region:'South America'},
'cl':{food:'Empanadas',climate:'Mediterranisch bis kalt-gemäßigt',landmark:'Torres del Paine',region:'South America'},
'eg':{food:'Koshari',climate:'Wüste',landmark:'Große Pyramide von Giza',region:'Africa'},
'za':{food:'Braai & Biltong',climate:'Gemäßigt bis semi-arid',landmark:'Krüger-Nationalpark',region:'Africa'},
'ng':{food:'Jollof Rice',climate:'Tropisch-Monsun',landmark:'Lekki Conservation Centre',region:'Africa'},
'sa':{food:'Shawarma',climate:'Wüste & heiß-trocken',landmark:'Kaaba in Mekka',region:'Middle East'},
'ae':{food:'Hummus & Falafel',climate:'Wüste & heißes Küstenklima',landmark:'Burj Khalifa',region:'Middle East'},
'il':{food:'Hummus & Falafel',climate:'Mittelmeer & Wüste',landmark:'Totes Meer',region:'Middle East'},
'au':{food:'Lamingtons',climate:'Vielfältig (arid bis tropisch)',landmark:'Uluru',region:'Oceania'},
'nz':{food:'Pavlova',climate:'Gemäßigt ozeanisch',landmark:'Milford Sound',region:'Oceania'},
'pl':{food:'Pierogi',climate:'Gemäßigt kontinental',landmark:'Marienkirche Danzig',region:'Eastern Europe'},
'cz':{food:'Goulash',climate:'Gemäßigt kontinental',landmark:'Karlsbrücke Prag',region:'Central Europe'},
'nl':{food:'Stroopwafels',climate:'Gemäßigt ozeanisch',landmark:'Windmühlen von Kinderdijk',region:'Western Europe'},
'be':{food:'Frites & Waffeln',climate:'Gemäßigt ozeanisch',landmark:'Grote Markt Brüssel',region:'Western Europe'},
'at':{food:'Wiener Schnitzel',climate:'Gemäßigt kontinental',landmark:'Schloss Schönbrunn',region:'Central Europe'},
'ch':{food:'Fondue & Raclette',climate:'Gemäßigt mit alpinem Einfluss',landmark:'Matterhorn',region:'Central Europe'},
'hu':{food:'Gulyásleves',climate:'Gemäßigt kontinental',landmark:'Parlamentsgebäude Budapest',region:'Eastern Europe'},
'se':{food:'Köttbullar & Gravlax',climate:'Kalt-gemäßigt',landmark:'Stockholms Schloss',region:'Northern Europe'},
'tr':{food:'Kebab & Döner',climate:'Mittelmeer & kontinental',landmark:'Blaue Moschee Istanbul',region:'Middle East'},
'th':{food:'Green Curry',climate:'Tropisch-monsun',landmark:'Wat Phra Kaew',region:'Southeast Asia'},
'my':{food:'Satay',climate:'Tropisch-feuchtes Regenwaldklima',landmark:'Petronas Towers',region:'Southeast Asia'},
'sg':{food:'Laksa',climate:'Tropisch-feuchtes Klima',landmark:'Merlion',region:'Southeast Asia'},
'ph':{food:'Adobo',climate:'Tropisch',landmark:'Reisterrassen von Banaue',region:'Southeast Asia'},
'ie':{food:'Irish Stew',climate:'Kalt-gemäßigt ozeanisch',landmark:'Cliffs of Moher',region:'Western Europe'},
'nz':{food:'Lamingtons',climate:'Gemäßigt ozeanisch',landmark:'Franz Josef Glacier',region:'Oceania'}
};


// PHASE 174: Smart proximity for wrong answers (same region)
function getCountriesInRegion(region){
const matches=[];
for(let code in globalCultureData){
if(globalCultureData[code].region===region){matches.push(code);}
}
return matches;
}
function getWrongAnswers(correctCode,count){
const data=globalCultureData[correctCode];
const region=data.region;
const regionCountries=getCountriesInRegion(region).filter(c=>c!==correctCode);
const wrong=[];
for(let i=0;i<count&&i<regionCountries.length;i++){
wrong.push(regionCountries[i]);
}
// Fill remaining with random countries if not enough in region
if(wrong.length<count){
const allCodes=Object.keys(globalCultureData);
for(let code of allCodes){
if(!wrong.includes(code)&&code!==correctCode){
wrong.push(code);
if(wrong.length>=count)break;
}
}
}
return wrong.slice(0,count);
}


// PHASE 176: Higher/Lower Comparison Helpers
function getCountriesSortedByMetric(metric){
// metric: 'area', 'pop', or 'density'
const sorted=COUNTRIES.slice().sort((a,b)=>{
if(metric==='area')return (b.a||0)-(a.a||0);
if(metric==='pop')return (b.pop||0)-(a.pop||0);
if(metric==='density'){
const denA=((a.pop||0)/(a.a||1));
const denB=((b.pop||0)/(b.a||1));
return denB-denA;
}
return 0;
});
return sorted;
}
function getVersusCountryPair(metric){
// Select country A randomly, then B from strict proximity (Phase 168 logic)
const sorted=getCountriesSortedByMetric(metric);
const maxIdx=sorted.length-1;
// Pick random country A
const idxA=Math.floor(Math.random()*sorted.length);
const countryA=sorted[idxA];
// Pick country B from neighbors only (Â±1 or Â±2 positions)
let idxB=idxA+Math.floor(Math.random()*3)-1; // -1, 0, or +1
if(idxB<0)idxB=0;
if(idxB>maxIdx)idxB=maxIdx;
if(idxB===idxA){
idxB=(idxA+1)<=maxIdx?(idxA+1):(idxA-1);
}
const countryB=sorted[idxB];
// TIE-BREAKER: Ensure different values
let attempts=0;
while(getMetricValue(countryA,metric)===getMetricValue(countryB,metric)&&attempts<5){
idxB=Math.floor(Math.random()*sorted.length);
attempts++;
}
return{countryA,countryB,correctIdx:getMetricValue(countryA,metric)>getMetricValue(countryB,metric)?0:1};
}

// PHASE 177: Extended metrics for Package B
function getCountriesSortedByAdvancedMetric(metric){
const sorted=COUNTRIES.slice().sort((a,b)=>{
const aData=COMP_DATA[a.country]||{};
const bData=COMP_DATA[b.country]||{};
if(metric==='gdp')return (bData.gdp||0)-(aData.gdp||0);
if(metric==='elevation')return (bData.elev||0)-(aData.elev||0);
if(metric==='coast'){
// Filter out landlocked (coast=0 or undefined)
const aCoast=(aData.coast||0)>0?aData.coast:null;
const bCoast=(bData.coast||0)>0?bData.coast:null;
if(aCoast===null&&bCoast===null)return 0;
if(aCoast===null)return 1; // b comes first (has coast)
if(bCoast===null)return -1; // a comes first (has coast)
return bCoast-aCoast;
}
if(metric==='borders')return (bData.bord||0)-(aData.bord||0);
return 0;
});
// For coastline, filter out landlocked countries
if(metric==='coast'){
return sorted.filter(c=>(COMP_DATA[c.country]||{}).coast>0);
}
return sorted;
}
function getVersusCountryPairAdvanced(metric){
const sorted=getCountriesSortedByAdvancedMetric(metric);
if(sorted.length<2)return null;
const maxIdx=sorted.length-1;
const idxA=Math.floor(Math.random()*sorted.length);
const countryA=sorted[idxA];
let idxB=idxA+Math.floor(Math.random()*3)-1;
if(idxB<0)idxB=0;
if(idxB>maxIdx)idxB=maxIdx;
if(idxB===idxA){
idxB=(idxA+1)<=maxIdx?(idxA+1):(idxA-1);
}
const countryB=sorted[idxB];
let attempts=0;
while(getAdvancedMetricValue(countryA,metric)===getAdvancedMetricValue(countryB,metric)&&attempts<5){
idxB=Math.floor(Math.random()*sorted.length);
attempts++;
}
return{countryA,countryB,correctIdx:getAdvancedMetricValue(countryA,metric)>getAdvancedMetricValue(countryB,metric)?0:1};
}
function getAdvancedMetricValue(country,metric){
const data=COMP_DATA[country.country]||{};
if(metric==='gdp')return data.gdp||0;
if(metric==='elevation')return data.elev||0;
if(metric==='coast')return data.coast||0;
if(metric==='borders')return data.bord||0;
return 0;
}
function formatAdvancedMetricDisplay(country,metric){
const data=COMP_DATA[country.country]||{};
const val=getAdvancedMetricValue(country,metric);
if(metric==='gdp')return '$'+val.toLocaleString()+' pro Kopf';
if(metric==='elevation')return val.toLocaleString()+' m';
if(metric==='coast')return val.toLocaleString()+' km';
if(metric==='borders')return val+' Länder';
return val.toString();
}


function getMetricValue(country,metric){
if(metric==='area')return country.a||0;
if(metric==='pop')return country.pop||0;
if(metric==='density')return (country.pop||0)/(country.a||1);
return 0;
}
function formatMetricDisplay(country,metric){
const val=getMetricValue(country,metric);
if(metric==='area')return (val/1e6).toFixed(1)+' Mio. kmÂ²';
if(metric==='pop')return (val/1e6).toFixed(1)+' Mio.';
if(metric==='density')return val.toFixed(1)+' je kmÂ²';
return val.toString();
}


// PHASE 179: Smart Climate Distractors
function getClimateKeywords(climateStr){
// Extract climate type from climate string
const keywords=[];
const lower=(climateStr||'').toLowerCase();
if(lower.includes('tropic'))keywords.push('tropic');
if(lower.includes('savanne')||lower.includes('savanna'))keywords.push('savanna');
if(lower.includes('wüste')||lower.includes('desert'))keywords.push('desert');
if(lower.includes('gemäßigt')||lower.includes('temperate'))keywords.push('temperate');
if(lower.includes('kalt')||lower.includes('polar')||lower.includes('arctic'))keywords.push('cold');
if(lower.includes('mediterran'))keywords.push('mediterranean');
if(lower.includes('monsun'))keywords.push('monsoon');
return keywords;
}
function hasClimateMatch(climateStr1,climateStr2){
// Check if two climate strings have matching keywords
const kw1=getClimateKeywords(climateStr1);
const kw2=getClimateKeywords(climateStr2);
if(kw1.length===0||kw2.length===0)return true; // fallback if no keywords found
for(let k of kw1){
if(kw2.includes(k))return true;
}
return false;
}
function getSmartClimateWrongAnswers(correctCode,count){
// Get wrong answers with matching climate types
const correctData=globalCultureData[correctCode];
const correctClimate=correctData.climate;
const correctKeywords=getClimateKeywords(correctClimate);
const allCodes=Object.keys(globalCultureData);
// First pass: Get same region + climate match
const candidates=allCodes.filter(code=>{
if(code===correctCode)return false;
const data=globalCultureData[code];
if(!hasClimateMatch(correctClimate,data.climate))return false;
return true;
});
// If we have enough candidates with climate match, use them
if(candidates.length>=count){
return candidates.sort(()=>Math.random()-0.5).slice(0,count);
}
// Fallback: Use regular wrong answers (fallback to region-based)
const region=correctData.region;
const regionCountries=Object.keys(globalCultureData).filter(c=>globalCultureData[c].region===region&&c!==correctCode);
return regionCountries.sort(()=>Math.random()-0.5).slice(0,count);
}


// PHASE 180: Specialty Quiz Helpers
function generateLogicPuzzle(){
// Generate a constraint-based geography puzzle
const countries=COUNTRIES.slice().filter(c=>c.pop>1e6).sort(()=>Math.random()-0.5).slice(0,5);
if(countries.length<2)return null;
const correct=countries[0];
const others=countries.slice(1);
// Build constraints
const constraints=[];
constraints.push(correct.country+' grenzt an '+others[0].country);
if(correct.pop>others[1].pop)constraints.push(correct.country+' hat mehr Einwohner als '+others[1].country);
if(correct.a>others[2].a)constraints.push(correct.country+' ist größer als '+others[2].country);
return{correct,options:countries,constraints};
}
function calculateCityDistance(city1,city2){
// Simple Haversine distance calculation
const lat1=city1.lat||0;
const lon1=city1.lon||0;
const lat2=city2.lat||0;
const lon2=city2.lon||0;
const R=6371;
const dLat=(lat2-lat1)*Math.PI/180;
const dLon=(lon2-lon1)*Math.PI/180;
const a=Math.sin(dLat/2)*Math.sin(dLat/2)+Math.cos(lat1*Math.PI/180)*Math.cos(lat2*Math.PI/180)*Math.sin(dLon/2)*Math.sin(dLon/2);
const c=2*Math.atan2(Math.sqrt(a),Math.sqrt(1-a));
return Math.round(R*c);
}
function getFlagFusionPairSafe(){
// Get two countries for flag fusion
const codes=Object.keys(globalCultureData);
const idx1=Math.floor(Math.random()*codes.length);
let idx2=Math.floor(Math.random()*codes.length);
while(idx2===idx1)idx2=Math.floor(Math.random()*codes.length);
const code1=codes[idx1];
const code2=codes[idx2];
const country1=COUNTRIES.find(c=>c.c===code1);
const country2=COUNTRIES.find(c=>c.c===code2);
if(!country1||!country2)return null;
return{country1,country2,code1,code2};
}


function renderLogicGrid(){
const puzzle=generateLogicPuzzle();
if(!puzzle)return '<div>Error: Not enough puzzle data</div>';
const{correct,options,constraints}=puzzle;

setCorrectAnswerObfuscated(COUNTRIES,correct.country,correct.country);

let html='<div style="padding:20px;text-align:center;">';
html+='<h2>Logik-Gitter</h2>';
html+='<div style="background:#f0f0f0;padding:15px;margin:20px 0;border-radius:8px;text-align:left;">';
html+='<strong>Bedingungen:</strong><br>';
for(let i=0;i<constraints.length;i++){
html+='<div style="margin:8px 0;">'+constraints[i]+'</div>';
}
html+='</div>';
html+='<p style="color:#666;">Welches Land erfüllt alle Bedingungen?</p>';
html+='<div style="display:flex;flex-direction:column;gap:10px;">';

for(let i=0;i<options.length;i++){
const country=options[i];
const isCorrect=country.country===correct.country;
const btnStyle='padding:12px;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;transition:all 0.2s;';
html+='<button style="'+btnStyle+'" data-quiz-type="logic-grid" data-quiz-answer="0")>';
html+=country.country;
html+='</button>';
}

html+='</div></div>';
return html;
}


function renderTravelRoute(){
// Select 2 random cities
const cities=(globalCities||[]).filter(c=>c.pop>100000).sort(()=>Math.random()-0.5).slice(0,4);
if(cities.length<2)return '<div>Error: Not enough city data</div>';
const city1=cities[0];
const city2=cities[1];
const city3=cities[2];
const city4=cities[3];

// Calculate distances
const dist1_2=calculateCityDistance(city1,city2);
const dist1_3=calculateCityDistance(city1,city3);
const dist1_4=calculateCityDistance(city1,city4);

// Create route options
const route1={desc:(city1.name||city1.n||'City')+' →’ '+(city2.name||city2.n||'City'),dist:dist1_2,correct:true};
const route2={desc:(city1.name||city1.n||'City')+' →’ '+(city3.name||city3.n||'City'),dist:dist1_3,correct:false};
const route3={desc:(city1.name||city1.n||'City')+' →’ '+(city4.name||city4.n||'City'),dist:dist1_4,correct:false};

const routes=[route1,route2,route3].sort(()=>Math.random()-0.5);
const correctIdx=routes.findIndex(r=>r.correct);

setCorrectAnswerObfuscated(COUNTRIES,correctIdx,correctIdx);

let html='<div style="padding:20px;text-align:center;">';
html+='<h2>Reiseroute-Quiz</h2>';
html+='<p>Welche Route ist kürzer?</p>';
html+='<div style="display:flex;flex-direction:column;gap:10px;">';

for(let i=0;i<routes.length;i++){
const route=routes[i];
const isCorrect=route.correct;
const btnStyle='padding:12px;font-size:14px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;transition:all 0.2s;';
html+='<button style="'+btnStyle+'" data-quiz-type="travel-route" data-quiz-answer="0")>';
html+=route.desc+'<br><span style="color:#999;font-size:12px;">~'+route.dist+' km</span>';
html+='</button>';
}

html+='</div></div>';
return html;
}


function renderFlagFusion(){
const pair=getFlagFusionPairSafe();
if(!pair)return '<div>Error: Not enough country data</div>';
const{country1,country2,code1,code2}=pair;

// Randomly choose which one to ask about
const askAbout=Math.random()>0.5?country1:country2;
const correctCode=askAbout.c;
const correctIdx=0;

setCorrectAnswerObfuscated(COUNTRIES,correctIdx,correctIdx);

// Create wrong answer options
const wrongOptions=COUNTRIES.filter(c=>c.c!==code1&&c.c!==code2).sort(()=>Math.random()-0.5).slice(0,3);
const allOptions=[askAbout,...wrongOptions].sort(()=>Math.random()-0.5);
const actualCorrectIdx=allOptions.findIndex(c=>c.c===correctCode);

let html='<div style="padding:20px;text-align:center;">';
html+='<h2>Flaggen-Fusion</h2>';
html+='<div style="background:#f0f0f0;padding:20px;margin:20px 0;border-radius:8px;">';
html+='<div style="display:flex;justify-content:center;gap:10px;margin-bottom:10px;">';
html+='<div style="opacity:0.7;font-size:60px;">🇹🇷</div>';
html+='<div style="font-size:40px;color:#ccc;">+</div>';
html+='<div style="opacity:0.7;font-size:60px;">🇸🇪</div>';
html+='</div>';
html+='<p style="color:#666;font-size:12px;">(Flaggen sind kombiniert)</p>';
html+='</div>';
html+='<p>Welches Land ist eines davon?</p>';
html+='<div style="display:flex;flex-direction:column;gap:10px;">';

for(let i=0;i<allOptions.length;i++){
const country=allOptions[i];
const isCorrect=country.c===correctCode;
const btnStyle='padding:12px;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;transition:all 0.2s;';
html+='<button style="'+btnStyle+'" data-quiz-type="flag-fusion" data-quiz-answer="0")>';
html+=country.country;
html+='</button>';
}

html+='</div></div>';
return html;
}

function handleFusionAnswerClick(index,isCorrect){
if(isCorrect){
S.correct++;
S.score+=10;
}else{
S.score-=5;
}
showMessage(isCorrect?'Richtig!':'Falsch!');
setTimeout(startNextRound,1500);
}

function handleTravelAnswerClick(index,isCorrect){
if(isCorrect){
S.correct++;
S.score+=10;
}else{
S.score-=5;
}
showMessage(isCorrect?'Richtig!':'Falsch!');
setTimeout(startNextRound,1500);
}

function handleLogicAnswerClick(index,isCorrect){
if(isCorrect){
S.correct++;
S.score+=15;
}else{
S.score-=5;
}
showMessage(isCorrect?'Richtig!':'Falsch!');
setTimeout(startNextRound,1500);
}

function startGame(m){ console.log("🟢 [TRACKER] 1. startGame gestartet. Mode:", m);
  clr();
  const survBest=parseInt(localStorage.getItem('gq_surv_best')||'0');
  const _m=m||S.mode;
  Object.assign(S,{sc:0,st:0,bs:0,rd:0,correct:0,lid:null,ph:"playing",mode:_m,
    scoreSaved:false,convModal:false,sessionAnswers:[],newStamps:[],isDailyRun:false,challengeStarted:false,
    half_removed:false,freezeActive:false,queueExtra:[],askedLids:new Set(),
    survivalBest:survBest,gameStartTime:Date.now(),hcMult:1.0,hcMaxMult:1.0,survTimeBonusTotal:0,lives:S.diff==="casual"?999:3});
  _secretGameToken=Math.random().toString(36).substring(2,15);
  /* Phase 86 – custom puzzle modes */
  if(_m==="logic_grid"){initLogikGitter();render();return;}
  if(_m==="travel_route"){initReiseroute();render();return;}
  if(_m==="slf"){initSLF();render();return;}
  lq();
}
async function showLeaderboard(){S.ph="menu";S.tab="home";S.lbLoading=true;render();S.lbData=await fetchLeaderboard(S.mode);S.lbLoading=false;render();}

/* UTILS */
function showPtsPopup(pts){const el=document.createElement("div");el.className="pts-popup";el.textContent="+"+pts;el.style.cssText="left:50%;top:40%;transform:translateX(-50%)";document.body.appendChild(el);setTimeout(()=>el.remove(),950);}
function showStampToast(cc){
  clearTimeout(toastTo);const old=document.getElementById("stamp-toast");if(old)old.remove();
  const el=document.createElement("div");el.id="stamp-toast";el.className="stamp-toast";
  const cn=COUNTRIES.find(c=>c.cc===(cc ? cc.toLowerCase() : cc))?.c||cc.toUpperCase();
  el.innerHTML=`<img src="https://flagcdn.com/w40/${cc}.png" style="width:22px;height:auto;border-radius:2px"> Neuer Stempel: ${cn}`;
  document.body.appendChild(el);soundStamp();toastTo=setTimeout(()=>el.remove(),3000);
}
function showCopyToast(){
  const old=document.getElementById("copy-toast");if(old)old.remove();
  const el=document.createElement("div");el.id="copy-toast";el.className="copy-toast";el.textContent="\u2713 In Zwischenablage kopiert\!";
  document.body.appendChild(el);setTimeout(()=>el.remove(),2500);
}
function shareResult(){
  const grade=S.sc>=2800?"S":S.sc>=2200?"A":S.sc>=1500?"B":S.sc>=800?"C":"D";
  const stars="\u{1F525}".repeat(Math.min(5,Math.ceil(S.correct/2)));
  const text=`\u{1F30D} GeoQuest: ${S.sc.toLocaleString()} Punkte\! ${stars}\n${S.correct}/${ROUNDS} richtig \u2022 Streak: ${S.bs}\u00d7\nKannst du das toppen? \u{1F3C6}`;
  navigator.clipboard.writeText(text).then(showCopyToast).catch(()=>{});
}
/* Phase 60: Ad hook – swap in real adsbygoogle.push({}) when AdSense is live */
/* Phase 151: flip to true when AdSense is approved and banners are configured */
const ENABLE_ADS=false;
function loadAd(){
  if(!ENABLE_ADS)return; /* P151: ads off */
  /* adsbygoogle.push({}); */
}
/* Phase 61: Viral share – Web Share API with clipboard fallback */
function shareGame(){
  const text=`Ich habe gerade ${S.sc.toLocaleString()} Punkte in GeoQuest erreicht\! Schaffst du mehr?`;
  const url=window.location.href;
  if(navigator.share){
    navigator.share({title:"GeoQuest",text,url}).catch(()=>{});
  }else{
    navigator.clipboard.writeText(text+" "+url)
      .then(()=>showToast(t("link_copied")||"Link kopiert\!"))
      .catch(()=>showToast("Link kopiert\!"));
  }
}
function updateHdrGuest(){
  const hdr=document.getElementById("g-hdr");
  const _uname=sbProfile?.username||localStorage.getItem("gq_username")||null;
  if(hdr)hdr.innerHTML=`<span class="g-logo">GEO<span>QUEST</span></span><div class="g-stats">${_uname?`<span class="g-stat" style="color:#10b981">\uD83D\uDC64 ${esc(_uname)}</span>`:""}<span class="g-stat">\u{1F525} ${S.st}</span><span class="g-stat">\u{1F4B0} ${(sbProfile?.geo_coins||0).toLocaleString()}</span><button class="hdr-gear" onclick="S.settingsModal=!S.settingsModal;render()" title="Einstellungen">\u2699\ufe0f</button></div>`;
}
function stampHtml(cc,rank,rot){
  const cn=COUNTRIES.find(c=>c.cc===(cc ? cc.toLowerCase() : cc))?.c||cc.toUpperCase();
  return `<div class="stamp-cell" onclick="S.modal='${cc}';render()" title="${cn}"><div class="stamp-ink ${rank}" style="transform:rotate(${rot}deg)"><img class="stamp-flag" src="https://flagcdn.com/w40/${cc}.png" alt="${cn}"><span>${cc.toUpperCase()}</span></div></div>`;
}

/* DAILY CHALLENGE */
function getDailyKey(){return"gq_daily_"+new Date().toISOString().slice(0,10);}


/* â”€â”€ Phase 42: LocalStorage Checksums â”€â”€ */
const _GQ_SALT="GQÂ®2025\u{1F30D}XKCD327";
function _fnv1a(s){
  let h=0x811c9dc5;
  for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=(h*0x01000193)>>>0;}
  return h.toString(36);
}
function _gqSave(key,data){
  const json=JSON.stringify(data);
  const cs=_fnv1a(json+_GQ_SALT);
  try{localStorage.setItem(key,JSON.stringify({d:data,c:cs}));}catch(e){}
}
function _gqLoad(key,fallback){
  try{
    const raw=localStorage.getItem(key);
    if(!raw)return fallback;
    const w=JSON.parse(raw);
    /* Support legacy plain format */
    if(w===null||typeof w!=="object"||!("d" in w))return w||fallback;
    const expected=_fnv1a(JSON.stringify(w.d)+_GQ_SALT);
    if(w.c!==expected){
      console.warn("GeoQuest: Integritätsfehler für",key,"– Daten zurückgesetzt");
      localStorage.removeItem(key);
      return fallback;
    }
    return w.d;
  }catch(e){return fallback;}
}

function _smartDefaultCountry(){
  /* Priority: new unified pref →’ old spotter key →’ navigator.language →’ fallback */
  const saved=localStorage.getItem("geoquest_pref_country")||localStorage.getItem("gq_spotter_country");
  if(saved&&saved!=="all")return saved;
  const lang=(navigator.language||"de-DE").toLowerCase();
  const langMap={
    "de-de":"Deutschland","de-at":"Österreich","de-ch":"Schweiz","de-li":"Liechtenstein",
    "fr-fr":"Frankreich","fr-be":"Belgien","fr-ch":"Schweiz","fr-lu":"Luxemburg",
    "nl-nl":"Niederlande","nl-be":"Belgien",
    "pl-pl":"Polen","it-it":"Italien","es-es":"Spanien","pt-pt":"Portugal",
    "cs-cz":"Tschechien","sk-sk":"Slowakei","hu-hu":"Ungarn","ro-ro":"Rumänien",
    "bg-bg":"Bulgarien","hr-hr":"Kroatien","sl-si":"Slowenien",
    "et-ee":"Estland","lv-lv":"Lettland","lt-lt":"Litauen",
    "fi-fi":"Finnland","sv-se":"Schweden","nb-no":"Norwegen","da-dk":"Dänemark",
    "el-gr":"Griechenland","tr-tr":"Türkei"
  };
  if(langMap[lang])return langMap[lang];
  /* Try just the language prefix (e.g. "de" for de-DE) */
  const prefix=lang.split("-")[0];
  const prefixMap={
    "de":"Deutschland","fr":"Frankreich","nl":"Niederlande","pl":"Polen",
    "it":"Italien","es":"Spanien","pt":"Portugal","cs":"Tschechien",
    "sk":"Slowakei","hu":"Ungarn","ro":"Rumänien","bg":"Bulgarien",
    "hr":"Kroatien","sl":"Slowenien","et":"Estland","lv":"Lettland",
    "lt":"Litauen","fi":"Finnland","sv":"Schweden","nb":"Norwegen","da":"Dänemark",
    "el":"Griechenland","tr":"Türkei"
  };
  return prefixMap[prefix]||"Deutschland";
}
function loadCollectedPlates(){return _gqLoad("gq_coll",[]);}
/* P128: plate timestamp storage + relative time helper */
function loadCollectedTs(){return _gqLoad("gq_coll_ts",{});}
function saveCollectedTs(k,ts){const m=loadCollectedTs();m[k]=ts;_gqSave("gq_coll_ts",m);}
function timeAgo(ts){
  const d=Date.now()-ts;const m=Math.floor(d/60000);
  if(m<1)return"Gerade eben";
  if(m<60)return"vor "+m+" Min.";
  const h=Math.floor(m/60);
  if(h<24)return"vor "+h+" Std.";
  const dy=Math.floor(h/24);
  if(dy===1)return"gestern";
  return"vor "+dy+" Tagen";
}
function saveCollectedPlates(arr){
  _gqSave("gq_coll",arr);
  /* Phase 93: Dual-Save – Kennzeichen auch in Supabase sichern */
  if(sb&&sbUser){
    sb.from("profiles").update({plates_collected:JSON.stringify(arr)})
      .eq("id",sbUser.id).then(()=>{},()=>{});
  }
}
function getRarity(code){
  if(!code)return"common";
  const c=code.trim().toUpperCase();
  const legendary=["WAT","CAS","AKU","BIR","HEB","HON","MEL","EUT","GUN","NAB","PEG","ABG","SCZ"];
  if(legendary.includes(c))return"legendary";
  if(c.length<=1)return"common";
  if(c.length===2)return"rare";
  if(c.length===3)return"epic";
  return"legendary";
}
function rarityLabel(r){return{common:"\u{1F7E2} Common",rare:"\u{1F535} Rare",epic:"\u{1F7E3} Epic",legendary:"\u{1F7E1} Legendary"}[r]||r;}
function rarityColor(r){return{common:"#10b981",rare:"#3b82f6",epic:"#8b5cf6",legendary:"#f59e0b"}[r]||"#999";}
function isDailyDone(){try{return\!\!JSON.parse(localStorage.getItem(getDailyKey())||"null");}catch(e){return false;}}
function markDailyDone(score){
  try{localStorage.setItem(getDailyKey(),JSON.stringify({score,ts:Date.now()}));}catch(e){}
  if(sb&&sbUser){const _d=new Date().toISOString().slice(0,10);sb.from("profiles").update({last_daily_date:_d}).eq("id",sbUser.id).then(()=>{},()=>{});}
}
function getDailySeed(){
  const d=new Date().toISOString().slice(0,10).replace(/-/g,"");
  let h=0;for(let i=0;i<d.length;i++){h=(Math.imul(31,h)+d.charCodeAt(i))|0;}
  return Math.abs(h);
}
function getDailyCountdown(){
  const now=new Date(),midnight=new Date(now);
  midnight.setHours(24,0,0,0);
  let s=~~((midnight-now)/1000);
  const h=~~(s/3600);s%=3600;const m=~~(s/60);s%=60;
  return String(h).padStart(2,"0")+":"+String(m).padStart(2,"0")+":"+String(s).padStart(2,"0");
}
function startDailyChallenge(){
  const seed=getDailySeed();
  initRng(seed);
  S.mode="city";S.diff="casual";S.isDailyRun=true;
  Object.assign(S,{sc:0,st:0,bs:0,rd:0,correct:0,lid:null,ph:"playing",scoreSaved:false,sessionAnswers:[],newStamps:[],half_removed:false,freezeActive:false,queueExtra:[],askedLids:new Set(),gameStartTime:Date.now(),adShownThisGame:false,adModal:false,slfData:null,hcMult:1.0,hcMaxMult:1.0,survTimeBonusTotal:0});
  lq();
}
function renderDailyHero(){
  const done=isDailyDone();
  const stored=done?JSON.parse(localStorage.getItem(getDailyKey())||"null"):null;
  const cd=getDailyCountdown();
  if(done){
    return`<div class="daily-hero done">
      <div style="display:flex;align-items:center;gap:12px">
        <div style="font-size:2rem">\u{1F3C6}</div>
        <div>
          <div class="dh-title">Daily Challenge erledigt\!</div>
          <div class="dh-sub" style="color:var(--text2)">Score: <b>${stored?.score?.toLocaleString()||"?"}</b> \u00b7 Neue Challenge in <span style="font-family:monospace;color:#f59e0b">${cd}</span></div>
        </div>
      </div>
    </div>`;}
  return`<div class="daily-hero" onclick="startDailyChallenge()" role="button">
    <div style="display:flex;align-items:center;justify-content:space-between">
      <div style="display:flex;align-items:center;gap:12px">
        <div style="font-size:2.2rem">\u{1F4C5}</div>
        <div>
          <div class="dh-title">Daily Challenge</div>
          <div class="dh-sub">Endet in <span class="dh-cd">${cd}</span> \u00b7 +100 GeoCoins</div>
        </div>
      </div>
      <button class="dh-btn">Spielen</button>
    </div>
  </div>`;
}

/* RENDER – main dispatcher */
/* Phase 33 T2 helper: percentage for duell bar */
function duellPct(a,b){const mx=Math.max(a,b,1);return Math.round(a/mx*100);}

/* Phase 84: ISO week helper */
function getISOWeek(d){
  const t=new Date(d);t.setHours(0,0,0,0);
  t.setDate(t.getDate()+3-(t.getDay()+6)%7);
  const w=new Date(t.getFullYear(),0,4);
  return t.getFullYear()+"-W"+String(1+Math.round(((t-w)/86400000-3+(w.getDay()+6)%7)/7)).padStart(2,"0");
}
async function evaluateWeeklyLeague(){
  if(!sb||!sbUser||!sbProfile){console.log("[GQ] evaluateWeeklyLeague: kein sb/sbUser/sbProfile, skip");return;}
  console.log("[GQ] evaluateWeeklyLeague: Starte für Woche",getISOWeek(new Date()));
  const curWeek=getISOWeek(new Date());
  if(sbProfile.last_eval_week===curWeek)return; /* already evaluated this week */
  const{data,error}=await sb.rpc("get_prev_week_rank",{p_user_id:sbUser.id});
  if(error||\!data)return;
  const{score,rank,total}=data;
  const oldLeagueId=sbProfile.current_league||"Bronze";
  const oldIdx=LEAGUES.findIndex(l=>l.id===oldLeagueId);
  let newIdx=oldIdx;
  let result="stay";
  if(total>=5&&score>0){
    const pct=rank/total;
    if(pct<=0.2&&oldIdx<LEAGUES.length-1){newIdx=oldIdx+1;result="up";}
    else if(pct>=0.8&&oldIdx>0){newIdx=oldIdx-1;result="down";}
  } else if(score===0&&oldIdx>0){newIdx=oldIdx-1;result="down"; /* inaktive Spieler steigen ab */}
  const newLeagueId=LEAGUES[newIdx].id;
  await sb.rpc("update_league",{p_user_id:sbUser.id,p_new_league:newLeagueId,p_eval_week:curWeek});
  sbProfile.current_league=newLeagueId;
  sbProfile.last_eval_week=curWeek;
  if(sbProfile.last_eval_week!=="") /* not first-ever login */ {
    S.leagueEvalResult={result,oldLeague:LEAGUES[oldIdx],newLeague:LEAGUES[newIdx],rank,total,score};
    render();
  }
}

const _LANDSCAPE_MODES_SET=new Set(["map_guess","map_reverse","map_capital"]);
function _isPortrait(){return window.innerHeight>window.innerWidth;}
function updateOrientationWarning(){
  const ow=document.getElementById("gq-orient-warn");
  if(\!ow)return false;
  const needsLandscape=_LANDSCAPE_MODES_SET.has(S.mode)&&S.ph==="playing";
  const show=_isPortrait()&&needsLandscape;
  ow.style.display=show?"flex":"none";
  const txt=ow.querySelector(".gq-ow-txt");if(txt)txt.textContent=t("rotate_device");
  return show;
}
function saveGridCols(val){
  localStorage.setItem('geoquest_grid_cols',String(val));
  document.documentElement.style.setProperty('--grid-cols',String(val));
}
// Apply saved grid cols on load (robust version)
(function(){
  let _sv=parseInt(localStorage.getItem('geoquest_grid_cols'));
  if(isNaN(_sv)||_sv<2||_sv>5){_sv=4;localStorage.setItem('geoquest_grid_cols','4');}
  document.documentElement.style.setProperty('--grid-cols',String(_sv));
  const _el=document.getElementById('gq-nuclear');
  if(_el)_el.textContent=_el.textContent.replace('--grid-cols:4','--grid-cols:'+_sv);
})();
function _scheduleFilterRefresh(){
  if(typeof window.filterByCategory==="function"&&document.getElementById("mainGamesGrid")){
    window.filterByCategory((typeof S!=="undefined"&&S.filterCat)||"pure_geo");
  }
}
function render(){ const candidates=(typeof S!=="undefined"&&S.candidates)?S.candidates:[];
  /* Surgical Scope Guard for candidates */
  const candidates_safe = (typeof S !== "undefined" && S.candidates) ? S.candidates : ((typeof candidates !== "undefined") ? candidates : []);
 console.log("🟢 [TRACKER] 3. render gestartet. Aktuelle Phase:", typeof S !== "undefined" ? S.ph : "S is null");
  updateHdrGuest();
  const app=document.getElementById("app");
  if(\!app)return;
  /* Phase 81: thin rainbow bar while Supabase session resolves */
  {const _bar=document.getElementById("gq-auth-bar");
   if(sbAuthPending&&\!_bar){const b=document.createElement("div");b.id="gq-auth-bar";
     b.style="position:fixed;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#10b981,#3b82f6,#10b981);background-size:200% 100%;animation:authBarSlide 1.2s linear infinite;z-index:10000";
     document.body.prepend(b);}
   if(\!sbAuthPending&&_bar)_bar.remove();}
  updateOrientationWarning();

  /* Onboarding gate */
  const ob=loadOb();
  if(\!ob||\!ob.done){
    if(S.obStep<0)S.obStep=0;
    app.innerHTML=renderOnboarding(S.obStep);return;
  }
  if(S.leagueEvalResult){app.innerHTML=renderLeagueEvalModal(S.leagueEvalResult);return;}
  if(S.waitingForLandscape){
    app.innerHTML=`<div style="min-height:100vh;background:var(--bg);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:2rem"><div style="font-size:3rem;margin-bottom:1rem">\u{1F4F1}\u27A1\u{1F5FA}</div><div style="font-size:1.1rem;font-weight:900;color:var(--text);margin-bottom:.5rem">Bitte Ger\u00e4t drehen</div><div style="font-size:.8rem;color:var(--text3);margin-bottom:1.5rem">Dieser Modus ben\u00f6tigt das Querformat</div><button class="btn-exit-global" onclick="clr();S.ph='menu';S.tab='home';S.waitingForLandscape=false;render()">🚪 Beenden</button></div>`;
    return;
  }
  if(S.lvModal){app.innerHTML=renderLVModal();return;}
  if(S.mpModal){app.innerHTML=renderMultiplayerLobby();return;}
  if(S.payModal){app.innerHTML=renderPayModal();return;}
  if(S.lockModal){app.innerHTML=renderLockModal(S.lockModal);return;}

  /* Challenge welcome */
  if(CHALLENGE&&S.ph==="menu"&&\!S.challengeStarted){
    const ml=modeTitle(MODES.find(m=>m.id===CHALLENGE.mode))||CHALLENGE.mode;
    app.innerHTML=`<div class="scr"><div style="background:var(--bg2);border-radius:20px;padding:1.5rem;text-align:center;margin-top:2rem">
      <div style="font-size:2rem;margin-bottom:.5rem">\u{1F3C6}</div>
      <div style="font-weight:900;font-size:1.2rem;margin-bottom:4px">Herausforderung\!</div>
      <div style="color:var(--text2);font-size:.82rem;margin-bottom:.85rem">Modus: ${ml}</div>
      <div style="background:var(--bg3);border-radius:12px;padding:.85rem;margin-bottom:1rem">
        <div style="color:var(--text3);font-size:.7rem;margin-bottom:3px">ZU SCHLAGEN</div>
        <div style="font-size:2.2rem;font-weight:900;color:#fbbf24">${CHALLENGE.oppScore.toLocaleString()}</div>
      </div>
      <button class="btn-p" onclick="S.challengeStarted=true;startChallenge(CHALLENGE)">\u{1F680} Annehmen</button>
      <button class="btn-g" onclick="S.challenge=null;render()">Ablehnen</button>
    </div></div>`;
    return;
  }

  /* Stamp detail modal */
  if(S.modal){
    const mastery=loadMastery();const m=mastery[S.modal]||{v:0,p:0};const rank=getMasteryRank(m.v,m.p);
    const cn=displayCountry(S.modal)||COUNTRIES.find(c=>c.cc===S.modal)?.c||S.modal.toUpperCase();
    const rl={gold:"\u{1F947} Gold",silver:"\u{1F948} Silber",bronze:"\u{1F949} Bronze"}[rank]||"Gesperrt";
    const rc={gold:"#d97706",silver:"#94a3b8",bronze:"#c2410c"}[rank]||"var(--text3)";
    app.innerHTML=`<div class="modal-overlay" onclick="if(event.target===this){S.modal=null;render()}"><div class="modal-box">
      <img src="https://flagcdn.com/w80/${S.modal}.png" style="height:44px;width:auto;border-radius:4px;margin-bottom:.75rem">
      <div style="font-size:1.2rem;font-weight:900;color:var(--text);margin-bottom:4px">${cn}</div>
      <div style="font-size:.82rem;font-weight:700;color:${rc};margin-bottom:.85rem">${rl}</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:1rem">
        <div style="background:var(--bg3);border-radius:10px;padding:.65rem;text-align:center"><div style="font-size:1.4rem;font-weight:900;color:#34d399">${m.v}</div><div style="font-size:.65rem;color:var(--text3)">Richtige Antworten</div></div>
        <div style="background:var(--bg3);border-radius:10px;padding:.65rem;text-align:center"><div style="font-size:1.4rem;font-weight:900;color:#fbbf24">${m.p}</div><div style="font-size:.65rem;color:var(--text3)">Perfekte Runden</div></div>
      </div>
      <button class="btn-p" style="margin-bottom:0" onclick="S.modal=null;render()">Schliessen</button>
    </div></div>`;
    return;
  }

  if(S.ph==="menu"){
    console.log("[GQ] rendering menu tab:",S.tab);
app.innerHTML=`<div class="scr">
      ${S.tab==="home"?renderHomeTab():""}
      ${S.tab==="lernen"?renderLernenTab():""}
      ${S.tab==="liga"?renderLigaTab():""}
      ${S.tab==="profil"?renderProfilTab():""}
      ${S.tab==="album"?renderCollectionScreen():""}
      ${S.tab==="stats"?renderStatsTab():""}
      ${S.tab==="admin"?renderAdminTab():""}
      ${S.settingsModal?renderSettingsModal():""}${S.adModal?renderAdModal():""}
    </div>${renderBottomNav()}`;
    if(S.tab==="home")setTimeout(_scheduleFilterRefresh,80);
    return;
  }

  if(S.ph==="gameover"){
  /* P151: ad trigger guarded by ENABLE_ADS */
  if(ENABLE_ADS&&!sbProfile?.is_premium&&!S.adShownThisGame){S.adShownThisGame=true;S.adModal=true;}
    const isSurv=S.diff==="survival";
    const survived=S.rd;const survBest=S.survivalBest||parseInt(localStorage.getItem('gq_surv_best')||'0');
    const isNewRecord=isSurv&&survived>=survBest&&survived>0;
    const _gThr=S.diff==="hardcore"?[350,280,200,100]:S.diff==="survival"?[300,150,70,30]:[96,80,60,30];const g=S.sc>=_gThr[0]?"S":S.sc>=_gThr[1]?"A":S.sc>=_gThr[2]?"B":S.sc>=_gThr[3]?"C":"D";
    const gc={S:"#fbbf24",A:"#34d399",B:"#60a5fa",C:"#fb923c",D:"#f87171"}[g];
    const ml=modeTitle(MODES.find(m=>m.id===S.mode))||"";const mm=isSurv?2:S.diff==="hardcore"?3:1;
    const isGuest=sbOK&&\!sbProfile?.username;
    const mastery=loadMastery();const totalStamps=Object.values(mastery).filter(m=>getMasteryRank(m.v,m.p)).length;
    const stampBanners=S.newStamps.map(({cc,rank})=>{
      const cn=COUNTRIES.find(c=>c.cc===(cc ? cc.toLowerCase() : cc))?.c||cc.toUpperCase();
      const rl={gold:"\u{1F947} Gold-Stempel",silver:"\u{1F948} Silber-Stempel",bronze:"\u{1F949} Bronze-Stempel"}[rank]||"Stempel";
      return`<div class="new-stamp-banner"><img src="https://flagcdn.com/w40/${cc}.png" style="width:28px;height:auto;border-radius:3px"><div><div style="color:#34d399;font-weight:900;font-size:.88rem">NEUER STEMPEL\!</div><div style="color:var(--text2);font-size:.78rem">${rl} \u2022 ${cn}</div></div></div>`;
    }).join("");
    const survivalPanel=isSurv?`
      ${isNewRecord?`<div style="background:linear-gradient(135deg,#7f1d1d,#991b1b);border:2px solid #ef4444;border-radius:12px;padding:.85rem;text-align:center;margin-bottom:.75rem">
        <div style="font-size:1.6rem">\ud83c\udfc6</div>
        <div style="color:#fca5a5;font-weight:900;font-size:.9rem">NEUER REKORD\!</div>
        <div style="color:#fef2f2;font-size:1.5rem;font-weight:900">${survived} Runden</div>
      </div>`:""}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:.85rem">
        <div style="background:var(--bg3);border-radius:12px;padding:.75rem .5rem;text-align:center"><div style="font-size:1.5rem;font-weight:900;color:#ef4444">${survived}</div><div style="font-size:.64rem;color:var(--text3)">\u00dcberlebt</div></div>
        <div style="background:var(--bg3);border-radius:12px;padding:.75rem .5rem;text-align:center"><div style="font-size:1.5rem;font-weight:900;color:#fbbf24">${survBest}</div><div style="font-size:.64rem;color:var(--text3)">Rekord</div></div>
      </div>`:"";
app.innerHTML=`<div class="scr">
      <div style="font-size:2.5rem;text-align:center">${isSurv?"\ud83d\udc80":"\u{1F3C6}"}</div>
      <h2 style="text-align:center;font-size:1.7rem;font-weight:900;color:var(--text);margin:3px 0">GAME OVER</h2>
      <p style="text-align:center;color:var(--text3);font-size:.78rem;margin-bottom:.85rem">${ml} \u00b7 ${isSurv?"Survival":ROUNDS+" Runden"}</p>
      ${stampBanners}
      <div style="background:var(--bg2);border-radius:16px;padding:1.5rem;margin-bottom:.85rem;text-align:center;border:1px solid var(--border)">
        ${isSurv?survivalPanel:`<div style="font-size:4rem;font-weight:900;line-height:1;color:${gc}">${g}</div>`}
        <div style="font-size:2rem;font-weight:900;color:var(--text);margin-top:5px">${S.sc.toLocaleString()}</div>
        <div style="color:var(--text3);font-size:.76rem;margin-bottom:.85rem">Punkte</div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:8px;margin-bottom:.85rem">
          <div style="background:var(--bg3);border-radius:12px;padding:.75rem .5rem;text-align:center"><div style="font-size:1.3rem;font-weight:900;color:#34d399">${S.correct}${isSurv?"":"/"+ROUNDS}</div><div style="font-size:.64rem;color:var(--text3)">Richtige</div></div>
          <div style="background:var(--bg3);border-radius:12px;padding:.75rem .5rem;text-align:center"><div style="font-size:1.3rem;font-weight:900;color:${mm>1?"#f59e0b":"var(--text3)"}">${mm}\u00d7</div><div style="font-size:.64rem;color:var(--text3)">${isSurv?"Survival":S.diff==="hardcore"?"Hardcore":"Casual"}</div></div>
          <div style="background:var(--bg3);border-radius:12px;padding:.75rem .5rem;text-align:center"><div style="font-size:1.3rem;font-weight:900;color:#fb923c">${S.bs}\u00d7</div><div style="font-size:.64rem;color:var(--text3)">Streak</div></div>
          <div style="background:var(--bg3);border-radius:12px;padding:.75rem .5rem;text-align:center"><div style="font-size:1.3rem;font-weight:900;color:#fbbf24">${isSurv?survived:~~(S.sc/ROUNDS)}</div><div style="font-size:.64rem;color:var(--text3)">${isSurv?"Runden":"\u00d8/Rd"}</div></div>
        </div>
        ${S.isDailyRun&&\!isDailyDone()?`<div style="background:linear-gradient(135deg,#052e16,#064e3b);border:1.5px solid #10b981;border-radius:12px;padding:.75rem;text-align:center;margin-bottom:.75rem">
          <div style="font-size:1.4rem">\u{1F3C6}</div>
          <div style="color:#34d399;font-weight:900;font-size:.9rem">Daily Challenge\!</div>
          <div style="color:#fbbf24;font-size:1rem;font-weight:900">+100 GeoCoins</div>
        </div>`:""}
        ${S.diff==="hardcore"?`<div style="background:var(--bg3);border-radius:10px;padding:.55rem .75rem;margin-bottom:.6rem;text-align:center;font-size:.78rem;color:var(--text2)">âš¡ ${t("score_mult_max")}: <strong style="color:#f59e0b">${(S.hcMaxMult||1).toFixed(1)}×</strong></div>`:S.diff==="survival"?`<div style="background:var(--bg3);border-radius:10px;padding:.55rem .75rem;margin-bottom:.6rem;text-align:center;font-size:.78rem;color:var(--text2)">⏱ ${t("score_time_bonus")}: <strong style="color:#34d399">+${S.survTimeBonusTotal||0} ${t("pts_abbr")}</strong></div>`:`<div style="background:var(--bg3);border-radius:10px;padding:.55rem .75rem;margin-bottom:.6rem;text-align:center;font-size:.78rem;color:var(--text2)">📋 ${S.correct}/${ROUNDS} ${t("score_correct_lbl")} × 10 ${t("pts_abbr")} = <strong style="color:#60a5fa">${S.sc} ${t("pts_abbr")}</strong></div>`}
        ${sbOK?`<div style="font-size:.76rem;color:${S.scoreSaved?"#34d399":"var(--text3)"}">${S.scoreSaved?"\u2713 Score gespeichert":"Speichere \u2026"}</div>`:""}
      </div>
      ${isGuest&&S.correct>0&&S.convModal?`<div class="conv-modal-bg" onclick="if(event.target===this){S.convModal=false;render()}">
  <div class="conv-modal">
    <div style="font-size:2rem;margin-bottom:.4rem">\u{1F4BE}</div>
    <div style="font-size:1rem;font-weight:900;color:var(--text);margin-bottom:.4rem">Fortschritt sichern!</div>
    <div style="color:var(--text2);font-size:.82rem;margin-bottom:1rem">Du hast dir ${S.sc.toLocaleString()} Punkte erarbeitet. Erstelle einen kostenlosen Account, damit deine Erfolge nicht verloren gehen.</div>
    <button class="btn-p" style="margin-bottom:.5rem" onclick="S.tab='profil';S.ph='menu';S.authMode='register';render()">\u{1F331} Account erstellen</button>
    <button class="btn-g" style="margin-bottom:0" onclick="S.convModal=false;render()">Sp\u00e4ter</button>
  </div>
</div>`:""}
      ${S.challenge?renderChallengeResult(S.challenge,S.sc,S.mode):""}
      <div id="ad-container-score" style="background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:.85rem 1rem;margin-bottom:.6rem;text-align:center;color:var(--text3);font-size:.8rem">Danke, dass du GeoQuest spielst\! \u{1F499}</div>
      <button class="share-btn" onclick="shareResult()">\u{1F4CB} Ergebnis teilen</button>
      <button class="btn-g" style="color:#60a5fa;border-color:#3b82f6" onclick="shareGame()">\u{1F4E4} Spiel teilen</button>
      <button class="btn-p" onclick="rngSeed=null;S.challenge=null;S.challengeStarted=false;startGame()">NOCHMAL</button>
      <button class="btn-g" onclick="S.ph='menu';S.tab='home';rngSeed=null;render()">Hauptmen\u00fc</button>
      ${S.mpOpponent?`
      <div class="mp-result-card">
        <div class="mp-result-title">\u2694\ufe0f Duell-Ergebnis</div>
        <div class="mp-result-row">
          <div class="mp-result-col mp-you">
            <div class="mp-result-name">Ich</div>
            <div class="mp-result-score">${S.sc.toLocaleString()}</div>
          </div>
          <div style="font-size:1.4rem;align-self:center;color:var(--text3)">vs</div>
          <div class="mp-result-col mp-opp">
            <div class="mp-result-name">${esc(S.mpOpponent)}</div>
            <div class="mp-result-score">${S.mpOppFinal?S.mpOppFinal.score.toLocaleString():'...'}</div>
          </div>
        </div>
        ${S.mpOppFinal
          ?`<div class="duell-final-bar">
              <div class="dfb-fill-you" style="width:${duellPct(S.sc,S.mpOppFinal.score)}%"></div>
              <div class="dfb-fill-opp" style="width:${duellPct(S.mpOppFinal.score,S.sc)}%"></div>
            </div>
            <div class="mp-result-verdict">${S.sc>S.mpOppFinal.score?'\u{1F3C6} Du gewinnst!':S.sc<S.mpOppFinal.score?'\u{1F614} Niederlage':'\u{1F91D} Unentschieden!'}</div>`
          :'<div class="mp-waiting">\u23f3 Warte auf Gegner\u2026<br><button class="btn-g" style="margin-top:.5rem;width:auto;padding:.35rem .9rem;font-size:.75rem" onclick="S.mpOpponent=null;render()">Trotzdem weiter</button></div>'}
      </div>`:""}
    </div>`;
    setTimeout(loadAd,100);
    return;
  }

  /* PLAYING / FEEDBACK */
  const{sc,st,bs,rd,q,sel,ok,pts,mode,diff}=S;
  /* Phase 86 – custom puzzle modes */
  if(mode==="logic_grid"&&S.ph==="playing"){
    app.innerHTML=renderLogikGitter(sc);
    requestAnimationFrame(()=>{document.getElementById("lg-inp")?.focus();});
    return;
  }
  if(mode==="travel_route"&&S.ph==="playing"){
    app.innerHTML=renderReiseroute(sc);
    requestAnimationFrame(()=>{document.getElementById("rr-inp")?.focus();});
    return;
  }
  if(mode==="slf"&&S.ph==="playing"){
    app.innerHTML=renderLandHauptstadt(sc);
    requestAnimationFrame(()=>{document.getElementById("slf-city")?.focus();});
    return;
  }
  if(!q){S.ph="menu";S.q=null;render();return;}  /* guard: q not yet set */
  const col=tc(),p=pct(),_tr=tier(st);const tm=diff==='survival'?S.tm+'s':`${rd+1}/${ROUNDS}`;const _tmSecs=diff!=='survival'?`<span style='font-size:.55rem;opacity:.7;margin-left:3px'>${S.tm}s</span>`:'';
  let qBody="";
  if(q.type==="flag"){
    qBody=`<div class="qprompt">${q.prompt}</div><div class="qflag"><img src="https://flagcdn.com/w80/${q.subj}.png" alt="Flagge" style="max-height:25vh;width:auto;max-width:100%;object-fit:contain;display:block;margin:0 auto"></div>${sel!==null?`<div class="qmeta">${q.meta||""}</div>`:""}`;
  }else if(q.type==="outline"){
    qBody=`<div class="qprompt">${q.prompt}</div><div class="outline-wrap" id="gq-outline-svg"></div>`;
  }else if(q.type==="food"){
    qBody=`<div class="qprompt">${q.prompt}</div><div class="food-emoji">${q.emoji||"\u{1F37D}"}</div><div class="qmain">${q.subj}</div>`;
  }else if(q.type==="brand"){
    qBody=`<div class="qprompt">${q.prompt}</div><div style="text-align:center;color:#94a3b8;font-size:.68rem;margin:2px 0 4px">${q.industry||""}</div><div class="qmain" style="font-size:2.2rem">${q.subj}</div>`;
  }else if(q.type==="currency"){
    qBody=`<div class="qprompt">${q.prompt}</div><div style="text-align:center;margin:6px 0 2px"><span class="currency-symbol">${q.symbol||""}</span></div><div class="qmain">${q.subj}</div>`;
  }else if(q.type==="plate_casual"||q.type==="plate_hard"){
    qBody=`<div class="qprompt">${q.prompt}</div>
      <div style="text-align:center;margin:8px 0 10px">
        <div class="plate-badge">${q.subj}</div>
        ${q.type==="plate_casual"&&q.meta&&sel\!==null?`<div style="color:var(--text3);font-size:.75rem;margin-top:6px">${q.meta}</div>`:""}
      </div>`;
  }else if(q.type==="hl_pop"||q.type==="hl_river"||q.type==="hl_area"){
    /* Higher/Lower card + dedicated answer buttons (clean "higher"/"lower" keys) */
    const revB=sel\!==null;
    const hlIcon=q.type==="hl_pop"?"\u{1F465}":q.type==="hl_river"?"\u{1F4A7}":"\u{1F5FA}";
    const hlFbH=sel===null?"":ok&&q.ans==="higher"?"ok":"ng";
    const hlFbL=sel===null?"":ok&&q.ans==="lower"?"ok":"ng";
    const hlDis=sel\!==null?"disabled":"";
    const hlBtnH=q.type==="hl_pop"?t("hl_more"):q.type==="hl_river"?t("hl_longer"):t("hl_bigger");
    const hlBtnL=q.type==="hl_pop"?t("hl_less"):q.type==="hl_river"?t("hl_shorter"):t("hl_smaller");
    qBody=`<div class="qprompt">${hlIcon} ${q.prompt}</div>
      <div class="hl-wrap">
        <div class="hl-card hl-known">
          <div class="hl-name">${q.nameA}</div>
          <div class="hl-val">${q.valA}</div>
        </div>
        <div class="hl-vs">\u{1F914}</div>
        <div class="hl-card hl-hidden${revB?" hl-revealed":""}">
          <div class="hl-name">${q.nameB}</div>
          <div class="hl-val">${revB?q.valB:"\u2753"}</div>
        </div>
      </div>
      <div class="hl-btn-row">
        <button class="hl-btn hl-higher${sel\!==null?(q.ans==="higher"?" ok":(sel==="higher"?" ng":" dm")):""}" ${hlDis} onclick="answer('higher',_secretGameToken)">${hlBtnH}</button>
        <button class="hl-btn hl-lower${sel\!==null?(q.ans==="lower"?" ok":(sel==="lower"?" ng":" dm")):""}" ${hlDis} onclick="answer('lower',_secretGameToken)">${hlBtnL}</button>
      </div>`;
  }else if(q.type==="plate_compare"){
    /* Beta Kennzeichen-Vergleich: show plate codes + flags */
    const _cfA=flagOf(q.opts[0])||'\u{1F30D}';
    const _cfB=flagOf(q.opts[1])||'\u{1F30D}';
    const _cnA=displayCountry(q.opts[0])||q.opts[0];
    const _cnB=displayCountry(q.opts[1])||q.opts[1];
    const _pA=q._codeA||"??";
    const _pB=q._codeB||"??";
    qBody=`<div class="qprompt">${q.prompt}</div>
      <div style="display:flex;justify-content:center;align-items:center;gap:1.8rem;margin:.55rem 0 .25rem">
        <div style="display:flex;flex-direction:column;align-items:center;gap:3px">
          <div style="background:#003399;color:#fff;font-size:1.1rem;font-weight:900;padding:.2rem .6rem;border-radius:4px;border:2px solid #fff;letter-spacing:1px">${_pA}</div>
          <span style="font-size:2rem">${_cfA}</span>
          <span style="font-size:.7rem;font-weight:700;color:var(--text2);max-width:90px;text-align:center;line-height:1.2">${esc(_cnA)}</span>
        </div>
        <span style="color:var(--text3);font-weight:900;font-size:.82rem;letter-spacing:1px">VS</span>
        <div style="display:flex;flex-direction:column;align-items:center;gap:3px">
          <div style="background:#003399;color:#fff;font-size:1.1rem;font-weight:900;padding:.2rem .6rem;border-radius:4px;border:2px solid #fff;letter-spacing:1px">${_pB}</div>
          <span style="font-size:2rem">${_cfB}</span>
          <span style="font-size:.7rem;font-weight:700;color:var(--text2);max-width:90px;text-align:center;line-height:1.2">${esc(_cnB)}</span>
        </div>
      </div>
      ${sel!==null?`<div class="qmeta" style="text-align:center;margin:.3rem 0 .1rem;font-size:.77rem">${q.meta||""}</div>`:""}`;
  }else if(q.type&&(q.type.startsWith('comp_')||q.type.startsWith('hl_b_')||q.type==='beta_hl')){
    /* Phase 102-A: Flaggen-Header + Prompt, Werte nach Antwort */
    /* HL_BETA opts are German names → look up cc via HL_BETA_CC */
    const _hlbCC=o=>q.type&&q.type.startsWith('hl_b_')?HL_BETA_CC[o]||null:null;
    const _hlbFlag=o=>{const cc=_hlbCC(o)||ccFromCountry(o);return cc?`<img src="https://flagcdn.com/w40/${cc}.png" style="height:22px;vertical-align:middle;border-radius:2px" alt="">`:'\u{1F30D}';};
    const _cfA=q.opts&&q.opts[0]?_hlbFlag(q.opts[0]):'\u{1F30D}';
    const _cfB=q.opts&&q.opts[1]?_hlbFlag(q.opts[1]):'\u{1F30D}';
    /* P136: show country names below flags */
    const _cnA=q.opts&&q.opts[0]?(displayCountry(_hlbCC(q.opts[0])||q.opts[0])||q.opts[0]):"";
    const _cnB=q.opts&&q.opts[1]?(displayCountry(_hlbCC(q.opts[1])||q.opts[1])||q.opts[1]):"";
    qBody=`<div class="qprompt">${q.prompt}</div>
      <div style="display:flex;justify-content:center;align-items:center;gap:1.8rem;margin:.55rem 0 .25rem">
        <div style="display:flex;flex-direction:column;align-items:center;gap:3px">
          <span style="font-size:2.2rem">${_cfA}</span>
          <span style="font-size:.75rem;font-weight:700;color:var(--text2);max-width:90px;text-align:center;line-height:1.2">${esc(_cnA)}</span>
        </div>
        <span style="color:var(--text3);font-weight:900;font-size:.82rem;letter-spacing:1px">VS</span>
        <div style="display:flex;flex-direction:column;align-items:center;gap:3px">
          <span style="font-size:2.2rem">${_cfB}</span>
          <span style="font-size:.75rem;font-weight:700;color:var(--text2);max-width:90px;text-align:center;line-height:1.2">${esc(_cnB)}</span>
        </div>
      </div>
      ${sel!==null?`<div class="qmeta" style="text-align:center;margin:.3rem 0 .1rem;font-size:.77rem">${q.meta||""}</div>`:""}`;
}else if(q.type==="curr_real"){
    /* Show country name; hide currency name (meta) until answered */
    qBody=`<div class="qprompt">${q.prompt}</div>
      <div class="qmain">${q.subj}</div>
      ${sel\!==null?`<div class="qmeta">${q.meta||""}</div>`:""}`;
  }else if(q.type==="wappen"){
    qBody=`<div class="qprompt">${q.prompt}</div><div class="wappen-img-wrap"><img src="${q.img}" alt="Wappen" class="wappen-img" onerror="wappenErr(this)" style="max-height:25vh;width:auto;max-width:100%;object-fit:contain;display:block;margin:0 auto"></div>${sel!==null?`<div class="qmeta">${q.meta||""}</div>`:""}`;
  }else if(q.type==="neighbor"||q.type==="neighbor_fake"||q.type==="neighbor_count"){
    qBody=`<div class="qprompt" style="font-size:1rem">${q.prompt}</div>
      <div style="text-align:center;margin:10px 0 6px">
        <div class="qmain" style="font-size:2.2rem">${q.subj}</div>
        <div style="font-size:1.2rem;margin-top:4px">${flagOf(q.subj)}</div>
      </div>`;
  }else{
    qBody=`<div class="qprompt">${q.prompt}</div><div class="qmain">${q.subj}</div>${sel!==null?`<div class="qmeta">${q.meta||""}</div>`:""}`;
  }
  /* After-answer reveal for plate casual */
  let plateReveal="";
  if(sel\!==null&&(q.type==="plate_casual"||q.type==="plate_hard")){
    const pc=PLATES_DATA.find(p=>p.code===q.subj);
    if(pc)plateReveal=`<div style="text-align:center;color:var(--text2);font-size:.8rem;margin-top:4px">${pc.region} \u00b7 ${pc.country}${pc.state?" \u00b7 "+pc.state:""}</div>`;
  }
  /* Phase 34: Map-Guesser – early return, D3 map replaces answer buttons */
  if(q.type==="map_reverse"){
    const mapFb=sel===null?"":ok
      ?`<div class="fb ok">✓ Richtig\! +${pts}</div>`
      :`<div class="fb ng">✗ Falsch → ${q.ans}</div>`;
    const disabled=sel\!==null?"disabled":"";
    const optHtml=q.opts.map(o=>{
      const cls=sel\!==null?(o===q.ans?" opt-ok":o===sel?" opt-ng":""):"";
      return`<button class="opt-btn${cls}" data-av="${(o||'').replace(/&/g,'&amp;').replace(/"/g,'&quot;')}" onclick="answer(this.dataset.av,_secretGameToken)" ${disabled}>${esc(o)}</button>`;
    }).join("");
    app.innerHTML=`<div class="scr map-scr">
      <div class="hud">
        <div style="display:flex;gap:8px;align-items:center">
          <div class="pill"><div class="hlbl">SCORE</div><div class="hval">${sc.toLocaleString()}</div></div>
          ${st>0?`<div class="pill-s"><div class="hlbl" style="color:#fb923c">STREAK</div><div class="hval-s">×${st}</div></div>`:""}
        </div>
        <div style="display:flex;align-items:center;gap:8px">
          ${diff==="survival"
            ?`<div style="text-align:right"><div class="hlbl" style="color:#ef4444">💀 SURVIVAL</div><div style="color:var(--text);font-weight:700;font-size:.9rem">${rd+1}<span style="color:var(--text3)">∞</span></div></div>`
            :`<div style="text-align:right"><div class="hlbl" style="color:var(--text3)">RUNDE</div><div style="color:var(--text);font-weight:700;font-size:.9rem">${rd+1}<span style="color:var(--text3)">/${ROUNDS}</span></div></div>`}
          <div class="action-bar" style="display:flex;flex-direction:row-reverse;gap:10px;align-items:center"><button class="btn-exit-global" onclick="clr();S.ph='menu';S.tab='home';render()" style="background:#ef4444;color:#fff;border:none;padding:10px 20px;border-radius:8px;font-weight:700;cursor:pointer;white-space:nowrap">🚪 Beenden</button><button class="btn-bug" onclick="reportBug()" style="background:#e2e8f0;color:#475569;border:none;padding:10px 14px;border-radius:8px;font-weight:700;cursor:pointer">🐞 Fehler</button></div>
        </div>
      </div>
      <div class="q-area" style="padding:0 8px 8px">
        <div style="text-align:center;margin:6px 0 6px">
          <div class="qprompt">${q.prompt}</div>
        </div>
        ${mapFb}
        <div id="gq-map-svg" style="width:100%;aspect-ratio:2/1;background:var(--bg2);border-radius:12px;overflow:hidden;margin-bottom:8px"></div>
        <div class="opts">${optHtml}</div>
      </div></div>`;
    requestAnimationFrame(()=>drawWorldMap(q.subj,sel,ok,true,true));
    return;
  }
  if(q.type==="map_guess"||q.type==="map_capital"){
    const mapFb=sel===null?"":ok
      ?`<div class="fb ok">\u2713 Richtig\! +${pts}</div>`
      :`<div class="fb ng">\u2717 Falsch \u2192 ${q.ans}</div>`;
    app.innerHTML=`<div class="scr map-scr">
      <div class="hud">
        <div style="display:flex;gap:8px;align-items:center">
          <div class="pill"><div class="hlbl">SCORE</div><div class="hval">${sc.toLocaleString()}</div></div>
          ${st>0?`<div class="pill-s"><div class="hlbl" style="color:#fb923c">STREAK</div><div class="hval-s">\u00d7${st}</div></div>`:""}
          ${S.mpOpponent?`<div class="pill" style="opacity:.7"><div class="hlbl" style="color:#8b5cf6">\u2694</div><div class="hval" style="color:#8b5cf6">${(S.mpOppScore||0).toLocaleString()}</div></div>`:""}
        </div>
        <div style="display:flex;align-items:center;gap:8px">
          ${diff==="survival"
            ?`<div style="text-align:right"><div class="hlbl" style="color:#ef4444">\ud83d\udc80 SURVIVAL</div><div style="color:var(--text);font-weight:700;font-size:.9rem">${rd+1}<span style="color:var(--text3)">\u221e</span></div></div>`
            :`<div style="text-align:right"><div class="hlbl" style="color:var(--text3)">RUNDE</div><div style="color:var(--text);font-weight:700;font-size:.9rem">${rd+1}<span style="color:var(--text3)">/${ROUNDS}</span></div></div>`}
          <div class="action-bar" style="display:flex;flex-direction:row-reverse;gap:10px;align-items:center"><button class="btn-exit-global" onclick="clr();S.ph='menu';S.tab='home';render()" style="background:#ef4444;color:#fff;border:none;padding:10px 20px;border-radius:8px;font-weight:700;cursor:pointer;white-space:nowrap">🚪 Beenden</button><button class="btn-bug" onclick="reportBug()" style="background:#e2e8f0;color:#475569;border:none;padding:10px 14px;border-radius:8px;font-weight:700;cursor:pointer">🐞 Fehler</button></div>
        </div>
      </div>
      ${S.mpOpponent?`<div class="duell-bar-wrap" style="margin:0 0 4px"><div class="duell-lbl duell-you">Ich<span class="duell-score">${sc.toLocaleString()}</span></div><div class="duell-track"><div class="duell-fill-you" style="width:${duellPct(sc,S.mpOppScore||0)}%"></div><div class="duell-fill-opp" style="width:${duellPct(S.mpOppScore||0,sc)}%"></div></div><div class="duell-lbl duell-opp"><span class="duell-score">${(S.mpOppScore||0).toLocaleString()}</span>${esc(S.mpOpponent.slice(0,8))}</div></div>`:""}
      <div class="tbar${S.freezeActive?" frozen":""}"><div class="tfill" style="width:${p}%;background:${col}"></div></div>
      <div class="map-prompt">\u{1F5FA} Finde: <strong>${esc(q.subj)}</strong></div>
      <div id="gq-map-svg" class="map-container"></div>
      ${mapFb}
      ${sel\!==null?`<button class="btn-p map-weiter" onclick="clr();nextRound()">Weiter \u2192</button>`:""}
    </div>`;
    requestAnimationFrame(()=>drawWorldMap(q.ans,sel,ok));
    return;
  }
  /* Phase 166: beta_spotter early-return (map click, like map_guess) */
  if(q.type==="beta_spotter"){
    const mapFb=sel===null?"":ok
      ?`<div class="fb ok">\u2713 Richtig! +${pts}</div>`
      :`<div class="fb ng">\u2717 Falsch \u2192 ${esc(q.ans)}</div>`;
    app.innerHTML=`<div class="scr map-scr">
      <div class="hud">
        <div style="display:flex;gap:8px;align-items:center">
          <div class="pill"><div class="hlbl">SCORE</div><div class="hval">${sc.toLocaleString()}</div></div>
          ${st>0?`<div class="pill-s"><div class="hlbl" style="color:#fb923c">STREAK</div><div class="hval-s">\u00d7${st}</div></div>`:""}
        </div>
        <div style="display:flex;align-items:center;gap:8px">
          ${diff==="survival"
            ?`<div style="text-align:right"><div class="hlbl" style="color:#ef4444">\u{1F480} SURVIVAL</div><div style="color:var(--text);font-weight:700;font-size:.9rem">${rd+1}<span style="color:var(--text3)">\u221e</span></div></div>`
            :`<div style="text-align:right"><div class="hlbl" style="color:var(--text3)">RUNDE</div><div style="color:var(--text);font-weight:700;font-size:.9rem">${rd+1}<span style="color:var(--text3)">/${ROUNDS}</span></div></div>`}
          <button class="btn-exit-global" onclick="clr();S.ph='menu';S.tab='home';render()">\u{1F6AA} Beenden</button>
        </div>
      </div>
      <div class="tbar${S.freezeActive?" frozen":""}"><div class="tfill" style="width:${p}%;background:${col}"></div></div>
      <div class="map-prompt">\u{1F9EA} ${esc(q.subj)}</div>
      <div id="gq-map-svg" class="map-container"></div>
      ${mapFb}
      ${sel!==null?`<button class="btn-p map-weiter" onclick="clr();nextRound()">Weiter \u2192</button>`:""}
    </div>`;
    requestAnimationFrame(()=>drawWorldMap(q.ans,sel,ok));
    return;
  }
  /* topBar: shared HUD wrapper used by pop_compare early-return */
  const topBar=`<div class="scr"><div class="hud"><div style="display:flex;gap:8px;align-items:center"><div class="pill"><div class="hlbl">SCORE</div><div class="hval">${sc.toLocaleString()}</div></div>${st>0?`<div class="pill-s"><div class="hlbl" style="color:#fb923c">STREAK</div><div class="hval-s">×${st}</div></div>`:""}${(diff==="hardcore"||diff==="survival")?`<div class="pill-s" style="background:rgba(239,68,68,.15)"><div class="hlbl" style="color:#ef4444">${t("hud_lives")}</div><div class="hval-s" style="color:#ef4444">${S.lives||3}</div></div>`:""}</div><div style="display:flex;align-items:center;gap:8px">${diff==="survival"?`<div style="text-align:right"><div class="hlbl" style="color:#ef4444">💀 SURVIVAL</div><div style="color:var(--text);font-weight:700;font-size:.9rem">${rd+1}<span style="color:var(--text3)">∞</span></div></div>`:`<div style="text-align:right"><div class="hlbl" style="color:var(--text3)">RUNDE</div><div style="color:var(--text);font-weight:700;font-size:.9rem">${rd+1}<span style="color:var(--text3)">/${ROUNDS}</span></div></div>`}<div class="action-bar" style="display:flex;flex-direction:row-reverse;gap:10px;align-items:center"><button class="btn-exit-global" onclick="clr();S.ph='menu';S.tab='home';render()" style="background:#ef4444;color:#fff;border:none;padding:10px 20px;border-radius:8px;font-weight:700;cursor:pointer;white-space:nowrap">🚪 Beenden</button><button class="btn-bug" onclick="reportBug()" style="background:#e2e8f0;color:#475569;border:none;padding:10px 14px;border-radius:8px;font-weight:700;cursor:pointer">🐞 Fehler</button></div></div></div><div class="tbar${S.freezeActive?" frozen":""}"><div class="tfill" style="width:${p}%;background:${col}"></div></div>`;
  let answerHtml="";
  if(q.type==="flagsel"){
    answerHtml='<div class="flag-grid">'+q.opts.map(cc=>{let cls="btn-base";if(typeof sel!=="undefined"&&sel!==null){if(cc===q.ans)cls+=" ok";else if(cc===sel)cls+=" ng";else cls+=" dm";}const lowerCc=String(cc||"").toLowerCase();return'<button class="'+cls+'" onclick="answer(&quot;'+cc+'&quot;,_secretGameToken)"><img src="https://flagcdn.com/h80/'+lowerCc+'.png" style="max-height:50px;border-radius:4px;pointer-events:none;box-shadow:0 2px 4px rgba(0,0,0,0.1)"></button>';}).join("")+'</div>';} else {
    // Population comparison: special subj rendering
    if(q.type==="pop_compare"&&q.subj&&typeof q.subj==='object'){
      const pcDis=sel!==null?"disabled":"";
      const moreCls="hl-btn hl-higher"+(sel!==null?(q.ans==="more"?" ok":(sel==="more"?" ng":" dm")):"");
      const lessCls="hl-btn hl-lower"+(sel!==null?(q.ans==="less"?" ok":(sel==="less"?" ng":" dm")):"");
      const pcHtml=topBar+`
        <div class="pop-compare-wrap">
          <div class="pop-box">
            <div class="pop-country">${q.subj.nameA}</div>
            <div class="pop-value">${q.subj.popA}</div>
          </div>
          <div style="font-size:1.4rem;color:var(--text3)">vs</div>
          <div class="pop-box" style="border-color:#10b981">
            <div class="pop-country">${q.subj.nameB}</div>
            <div style="color:var(--text3);font-size:.78rem">?</div>
          </div>
        </div>
        <div style="color:var(--text3);font-size:.82rem;text-align:center;margin:.5rem 0">${q.prompt}</div>
        <div class="hl-btn-row">
          <button class="${moreCls}" ${pcDis} onclick="answer('more',_secretGameToken)">${t("hl_more")}</button>
          <button class="${lessCls}" ${pcDis} onclick="answer('less',_secretGameToken)">${t("hl_less")}</button>
        </div>
        ${sel\!==null?`<div class="meta-line">${q.meta||""}</div>`:""}
        ${sel\!==null?`<button class="btn-p" onclick="nextRound()">Weiter →’</button>`:""}
      </div>`;
      app.innerHTML=pcHtml;return;
    }
    if(q.type==="hl_pop"||q.type==="hl_river"||q.type==="hl_area"){
      answerHtml="";
    }else{
      if(q.type==="stadium"){
        qBody=`<div class="qprompt">${q.prompt}</div><div class="qmain" style="font-size:1.3rem;font-weight:900">${q.subj}</div>${sel!==null?`<div class="qmeta">${q.meta||""}</div>`:""}`;
      }else if(q.type==="jersey"){
        const _jsvg=_drawJersey(q.subj.cc,q.subj.color,q.subj.style);
        qBody=`<div class="qprompt">${q.prompt}</div><div style="display:flex;justify-content:center;margin:.75rem 0">${_jsvg}</div>`;
      }else if(q.type==="crest"){
        const _csvg=_drawCrest(q.subj.shape,q.subj.color);
        qBody=`<div class="qprompt">${q.prompt}</div><div style="display:flex;justify-content:center;margin:.75rem 0">${_csvg}</div>`;
      }
      { const _isFootball=(q.type==="stadium"||q.type==="jersey"||q.type==="crest");const _isHLBeta=(q.type&&q.type.startsWith('hl_b_'));
  const btns=q.opts.map((o,i)=>{let cls="btn-a";const os=o.replace(/'/g,"\'");if(sel\!==null){if(o===q.ans)cls+=" ok";else if(o===sel)cls+=" ng";else cls+=" dm";}const mk=sel?(o===q.ans?`<span>\u2713</span>`:o===sel?`<span>\u2717</span>`:""):"";return`<button class="${cls}" ${sel?"disabled":""} onclick="answerByIdx(${i})">${(_isHLBeta&&HL_BETA_CC[o])?`<img src="https://flagcdn.com/w40/${HL_BETA_CC[o].toLowerCase()}.png" style="height:14px;vertical-align:middle;margin-right:3px;border-radius:2px" onerror="this.style.display=\'none\'">`:_isFootball&&String(o).length===2?`<img src="https://flagcdn.com/w40/${String(o).toLowerCase()}.png" style="height:14px;vertical-align:middle;margin-right:3px;border-radius:2px" onerror="this.style.display=\'none\'">`:""}${esc(q.type==="map_ivr"?o:_isHLBeta?(displayCountry(HL_BETA_CC[o])||o):_isFootball?(displayCountry(String(o))||String(o)):displayCountry(o))}${mk}</button>`;}).join("");
      const _twoOpts=q.opts&&q.opts.length===2?' two-opts':'';
      answerHtml=`<div class="answers${_twoOpts}">${btns}</div>`;
    }
  }
  }
  let fb="";
  if(S.ph==="feedback"){const cls=ok?"fb ok":"fb ng";let al=q.ans;if(q.type==="flagsel"){const co=COUNTRIES.find(c=>c.cc===q.ans);al=co?co.c:q.ans;}const al_d=displayCountry(al);const msg=ok?t("fb_correct",{pts}):sel==="__t"?t("fb_time",{ans:al_d}):t("fb_wrong",{ans:al_d});fb=`<div class="${cls}">${msg}</div>${plateReveal}`;}
  /* Power-up bar (Phase 26) */
  const pu=loadPU();
  /* P136-fix: 50/50 disabled for comp_ modes -- pre-declared vars, no nested escaping */
  const _is2ans=S.q&&S.q.type&&(S.q.type.startsWith('comp_')||S.q.type.startsWith('hl_b_')||S.q.type==='beta_hl');
  const _j5title=_is2ans?'Kein 50/50 (nur 2 Optionen)':'50/50-Joker ('+(pu.five0||0)+' \u00fcbrig)';
  const _j5label=_is2ans?'–':'('+(pu.five0||0)+')';
  const _j5sty=_is2ans?'opacity:.35;pointer-events:none':'';
  console.log("🟢 [TRACKER] 4. Erreiche HTML-Zuweisung. Antwort-Block Länge:", typeof answerHtml !== "undefined" ? answerHtml.length : "UNDEFINED");
  const puBar=`<div class="pu-bar">
    <button class="pu-btn${S.half_removed?" pu-used":""}" onclick="useFiveO()" ${(S.half_removed||(pu.five0||0)===0||_is2ans)?"disabled":""} style="${_j5sty}" title="${_j5title}">\u2702 50/50 <span style="font-size:.62rem">${_j5label}</span></button>
    <button class="pu-btn${S.freezeActive?" freeze-on":""}" onclick="useFreeze()" ${(S.freezeActive||(pu.freeze||0)===0)?"disabled":""} title="Zeit-Stopp (${pu.freeze||0} \u00fcbrig)">\u{1F9CA} Freeze <span style="font-size:.62rem">(${pu.freeze||0})</span></button>
  </div>`;
  app.innerHTML=`<div class="scr">
    <div class="hud">
      <div style="display:flex;gap:8px;align-items:center">
        <div class="pill"><div class="hlbl">SCORE</div><div class="hval">${sc.toLocaleString()}</div></div>
        ${st>0?`<div class="pill-s"><div class="hlbl" style="color:#fb923c">STREAK</div><div class="hval-s">\u00d7${st}</div></div>`:""}
      </div>
      <div style="display:flex;align-items:center;gap:8px">
        ${diff==="survival"
          ?`<div style="text-align:right"><div class="hlbl" style="color:#ef4444">\ud83d\udc80 SURVIVAL</div><div style="color:var(--text);font-weight:700;font-size:.9rem">${rd+1}<span style="color:var(--text3)">\u221e</span></div></div>`
          :`<div style="text-align:right"><div class="hlbl" style="color:var(--text3)">RUNDE</div><div style="color:var(--text);font-weight:700;font-size:.9rem">${rd+1}<span style="color:var(--text3)">/${ROUNDS}</span></div></div>`}
        <div class="action-bar" style="display:flex;flex-direction:row-reverse;gap:10px;align-items:center"><button class="btn-exit-global" onclick="clr();S.ph='menu';S.tab='home';render()" style="background:#ef4444;color:#fff;border:none;padding:10px 20px;border-radius:8px;font-weight:700;cursor:pointer;white-space:nowrap">🚪 Beenden</button><button class="btn-bug" onclick="reportBug()" style="background:#e2e8f0;color:#475569;border:none;padding:10px 14px;border-radius:8px;font-weight:700;cursor:pointer">🐞 Fehler</button></div>
      </div>
    </div>
    ${S.mpOpponent?`<div class="duell-bar-wrap"><div class="duell-lbl duell-you">Ich<span class="duell-score">${sc.toLocaleString()}</span></div><div class="duell-track"><div class="duell-fill-you" style="width:${duellPct(sc,S.mpOppScore||0)}%"></div><div class="duell-fill-opp" style="width:${duellPct(S.mpOppScore||0,sc)}%"></div></div><div class="duell-lbl duell-opp"><span class="duell-score">${(S.mpOppScore||0).toLocaleString()}</span>${esc(S.mpOpponent.slice(0,8))}</div></div>`:""}
    ${st>=3?`<div style="text-align:center;font-size:.76rem;font-weight:700;color:#fb923c;margin-bottom:6px">${_tr.l}</div>`:""}
    <div class="tbar${S.freezeActive?" frozen":""}"><div class="tfill" style="width:${p}%;background:${col}"></div></div>
    <div class="qcard">${qBody}<div class="qtimer" style="color:${col}">${tm}</div></div>
    ${sel===null?puBar:""}
    ${answerHtml}${fb}
  </div>`;
  /* Phase 35: draw country outline after DOM update */
  if(q.type==="outline")requestAnimationFrame(()=>drawCountryOutline(q.subj,"gq-outline-svg"));
}

/* Phase 35: draw single-country D3 silhouette for outline mode */
function drawCountryOutline(cc,targetId){
  const el=document.getElementById(targetId);
  if(\!el)return;
  if(typeof d3==='undefined'||typeof topojson==='undefined'||\!window.WORLD_TOPO){
    el.innerHTML='<span style="font-size:3rem">'+cc.toUpperCase()+'</span>';
    return;
  }
  const countries=topojson.feature(window.WORLD_TOPO,window.WORLD_TOPO.objects.countries);
  /* Map cc to TopoJSON name via MAP_COUNTRIES */
  const entry=MAP_COUNTRIES.find(x=>x.cc===cc);
  if(\!entry){el.innerHTML='<span style="font-size:1rem;color:var(--text3)">?</span>';return;}
  const feat=countries.features.find(f=>f.properties.name===entry.name);
  if(\!feat){el.innerHTML='<span style="font-size:1rem;color:var(--text3)">?</span>';return;}
  const W=el.clientWidth||200,H=el.clientHeight||140;
  const proj=d3.geoMercator().fitSize([W,H],feat);
  const path=d3.geoPath().projection(proj);
  d3.select(el).html('').append('svg')
    .attr('width','100%').attr('height','100%')
    .attr('viewBox',`0 0 ${W} ${H}`)
    .append('path')
    .datum(feat)
    .attr('d',path)
    .attr('fill','var(--text,#1e293b)')
    .attr('stroke','none');
}


/* Phase 34 – D3 World Map component */
function drawWorldMap(targetName,sel,ok,preHL,readOnly){
  const container=document.getElementById('gq-map-svg');
  if(\!container||typeof d3==='undefined'||typeof topojson==='undefined'){
    if(container)container.innerHTML='<p style="color:var(--text3);text-align:center;padding:2rem">'+t('map_unavail')+'</p>';
    return;
  }
  if(\!window.WORLD_TOPO){
    container.innerHTML='<p style="color:var(--text3);text-align:center;padding:2rem">'+t('map_loading')+'</p>';
    return;
  }
  const W=container.clientWidth||(window.innerWidth||360),H=Math.min(W*.56,290);
  const svg=d3.select(container).html('').append('svg')
    .attr('width','100%').attr('height',H)
    .attr('viewBox',`0 0 ${W} ${H}`)
    .style('background','var(--bg2)')
    .style('touch-action','none')
    .style('user-select','none');

  const proj=d3.geoNaturalEarth1().scale(W/6.2).translate([W/2,H/2]);
  const path=d3.geoPath().projection(proj);
  const countries=topojson.feature(window.WORLD_TOPO,window.WORLD_TOPO.objects.countries);

  const g=svg.append('g');

  /* Zoom + pan */
  const zoom=d3.zoom().scaleExtent([1,10])
    .on('zoom',ev=>{
      g.attr('transform',ev.transform); /* zoom always enabled */
      window._mapZoom=ev.transform; /* persist for redraw restore */
    });
  svg.call(zoom);
  /* Restore zoom on timer-triggered redraws (sel===null = pre-answer) */
  if(sel===null&&window._mapZoom&&window._mapZoom.k>1){
    svg.call(zoom.transform,window._mapZoom);
  } else if(sel!==null){
    window._mapZoom=null; /* clear after answer so zoom-to-country starts clean */
  }

  /* Sphere backdrop */
  g.append('path').datum({type:'Sphere'}).attr('d',path)
    .attr('fill','#bfdbfe').attr('stroke','none');

  /* Country paths */
  g.selectAll('path.ctry')
    .data(countries.features)
    .enter().append('path')
    .attr('class','ctry')
    .attr('d',path)
    .attr('data-n',d=>d.properties.name)
    .attr('fill',d=>{
      const n=d.properties.name;
      if(sel\!==null){
        if(n===targetName)return'#10b981';
        if(n===sel&&\!ok)return'#ef4444';
        return'#d1d5db';
      }
      if(preHL&&n===targetName)return'#3b82f6';
      return'var(--bg3,#e2e8f0)';
    })
    .attr('stroke','var(--border,#94a3b8)')
    .attr('stroke-width',.35)
    .on('mouseover',function(_,d){
      if(readOnly||sel\!==null)return;
      d3.select(this).attr('fill','#93c5fd');
    })
    .on('mouseout',function(_,d){
      if(readOnly||sel\!==null)return;
      d3.select(this).attr('fill','var(--bg3,#e2e8f0)');
    })
    .on('click',function(ev,d){
      if(readOnly||sel\!==null)return;
      ev.stopPropagation();
      answer(d.properties.name,_secretGameToken);
    });

  /* Pulse correct country after feedback */
  if(sel\!==null){
    const cp=g.selectAll('path.ctry').filter(d=>d.properties.name===targetName);
    let n=ok?2:4;
    function pulse(){
      if(n--<=0)return;
      cp.transition().duration(300).attr('fill','#6ee7b7')
        .transition().duration(300).attr('fill','#10b981').on('end',pulse);
    }
    pulse();
    /* Zoom to correct country */
    const feat=countries.features.find(d=>d.properties.name===targetName);
    if(feat){
      const[[x0,y0],[x1,y1]]=path.bounds(feat);
      const cw=x1-x0,ch=y1-y0;
      const s=Math.max(1,Math.min(8,.8/Math.max(cw/W,ch/H)));
      const tx=W/2-(x0+x1)/2*s,ty=H/2-(y0+y1)/2*s;
      svg.transition().duration(700)
        .call(zoom.transform,d3.zoomIdentity.translate(tx,ty).scale(s));
    }
  }
}


/* BOTTOM NAV */
function renderBottomNav(){
  const tabs=[
    {id:"home",   icon:"\u{1F3E0}", lbl:"Home"},
    {id:"lernen", icon:"\u{1F4DA}", lbl:"Lernen"},
    {id:"liga",   icon:"\u{1F3C6}", lbl:"Liga"},
    {id:"profil", icon:"\u{1F464}", lbl:"Profil"},
    {id:"album",  icon:"\u{1F4D4}", lbl:"Album"},
    {id:"stats",  icon:"\u{1F4CA}", lbl:"Stats"},
  ];
  const isAdmin=sbUser?.email==="andre69190@gmail.com";
  if(isAdmin)tabs.push({id:"admin",icon:"\u{1F6E1}\uFE0F",lbl:"Admin"});
  return`<nav class="bottom-nav">${tabs.map(t=>`<button class="bn-item${S.tab===t.id?" active":""}" onclick="S.tab='${t.id}';render()"><span class="bn-icon">${t.icon}</span><span class="bn-lbl">${t.lbl}</span></button>`).join("")}</nav>`;
}


/* â”€â”€â”€ Phase 43: Kennzeichen-Album â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */

/* Country name →’ English for world-110m matching */
const PLATE_COUNTRY_EN={
  "Deutschland":"Germany","Österreich":"Austria","Frankreich":"France",
  "Italien":"Italy","Spanien":"Spain","Polen":"Poland","Tschechien":"Czechia",
  "Ungarn":"Hungary","Schweiz":"Switzerland","Belgien":"Belgium",
  "Niederlande":"Netherlands","Dänemark":"Denmark","Schweden":"Sweden",
  "Norwegen":"Norway","Finnland":"Finland","Portugal":"Portugal",
  "Griechenland":"Greece","Rumänien":"Romania","Bulgarien":"Bulgaria",
  "Kroatien":"Croatia","Slowenien":"Slovenia","Slowakei":"Slovakia",
  "Luxemburg":"Luxembourg","Irland":"Ireland","Litauen":"Lithuania",
  "Lettland":"Latvia","Estland":"Estonia","Zypern":"Cyprus","Malta":"Malta",
  "Vereinigtes Königreich":"United Kingdom","Russland":"Russia",
  "Türkei":"Turkey","Ukraine":"Ukraine","Serbien":"Serbia",
  "Bosnien und Herzegowina":"Bosnia and Herzegovina"
};
function plateCountryToEn(c){return PLATE_COUNTRY_EN[c]||c;}

/* â”€â”€ Collection key helpers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
   collectedPlates stores "CODE::Country" keys to handle cross-country dups
   e.g. "HD::Germany" and "HD::Romania" are separate entries
   â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
function collKey(code,country){return code+"::"+country;}
function parseCollKey(k){const i=k.indexOf("::");return i<0?{code:k,country:"?"}:{code:k.slice(0,i),country:k.slice(i+2)};}
function isCollected(code,country){return S.collectedPlates.includes(collKey(code,country));}

/* Migrate old plain-code format →’ code::country */
function migrateCollectedPlates(){
  if(\!PLATES_DATA.length)return;
  let changed=false;
  S.collectedPlates=S.collectedPlates.map(entry=>{
    if(entry.includes("::"))return entry; /* already new format */
    const code=entry.toUpperCase();
    const matches=[...new Set(PLATES_DATA.filter(p=>p.code===code).map(p=>p.country))];
    if(matches.length===1){changed=true;return collKey(code,matches[0]);}
    if(matches.length>1){changed=true;return collKey(code,matches[0]);} /* take first if ambiguous */
    return null; /* unknown code – discard */
  }).filter(Boolean);
  /* Deduplicate */
  S.collectedPlates=[...new Set(S.collectedPlates)];
  if(changed)saveCollectedPlates(S.collectedPlates);
}

/* â”€â”€ Unique deduped plate view per country â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
   PLATES_DATA may have 61 rows for "HD" in Germany (61 municipalities).
   We want ONE entry per code per country in the album.
   â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
function getUniquePlatesForCountry(country){
  /* Returns [{code, mainRegion, extraCount}] – one entry per unique code */
  const codeMap={};
  PLATES_DATA.filter(p=>p.country===country).forEach(p=>{
    if(\!codeMap[p.code])codeMap[p.code]={code:p.code,mainRegion:p.region,count:0};
    codeMap[p.code].count++;
  });
  return Object.values(codeMap).sort((a,b)=>a.code.localeCompare(b.code));
}

/* Total unique code::country combos (= album size) */
function totalUniquePlates(){
  const seen=new Set();
  PLATES_DATA.forEach(p=>seen.add(collKey(p.code,p.country)));
  return seen.size;
}

/* â”€â”€ Spotter â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€*/
function spotterCollect(){
  const code=(S.spotterInput||"").toUpperCase().trim();
  if(\!code){S.spotterMsg="Bitte Kennzeichen eingeben\!";S.spotterOk=null;render();return;}
  const country=S.spotterCountry&&S.spotterCountry\!=="all"?S.spotterCountry:null;
  /* Phase 104: Fuzzy-Lookup – normalisiere zuerst (0→’O, 1→’I) */
  const _norm=s=>s.replace(/0/g,'O').replace(/1/g,'I').replace(/ßœ/g,'UE').replace(/Ö/g,'OE').replace(/ß„/g,'AE');
  const codeNorm=_norm(code);
  /* Find matching plates: exact →’ normalisiert →’ prefix */
  const _match=(c,p)=>p.code===c&&(country===null||p.country===country);
  let candidates=PLATES_DATA.filter(p=>_match(code,p));
  /* Fallback 1: Normalisierung (0→”O, Umlaute) */
  if(\!candidates.length&&codeNorm\!==code){
    candidates=PLATES_DATA.filter(p=>_match(codeNorm,p));
    if(candidates.length)S.spotterInput=codeNorm;
  }
  /* Fallback 2: Prefix-Match (min 2 Zeichen) – zeige Vorschläge */
  let prefixSuggestions=[];
  if(\!candidates.length&&code.length>=2){
    prefixSuggestions=[...new Set(
      PLATES_DATA.filter(p=>(country===null||p.country===country)&&p.code.startsWith(code)&&p.code\!==code)
        .map(p=>p.code).slice(0,8)
    )];
  }
  if(\!candidates.length){
    /* Phase 105b: TYPE_COUNTRY – Länder ohne Regionen */
    if(country){
      const _cEnt=PLATES_DATA.filter(p=>p.country===country);
      if(_cEnt.length===1&&_cEnt[0].region==='Nationales Kennzeichen'){
        S.spotterMsg="ℹ️ "+displayCountry(country)+" "+t("spotter_no_region",{code:_cEnt[0].code});
        S.spotterOk=false;render();return;
      }
    }
    /* Check if code exists in other countries */
    const elsewhere=PLATES_DATA.filter(p=>p.code===code||p.code===codeNorm);
    if(elsewhere.length){
      const others=[...new Set(elsewhere.map(p=>p.country))].join(", ");
      S.spotterMsg="â“ '"+esc(code)+"' "+t("spotter_not_in")+" "+(country?displayCountry(country):t("spotter_all"))+" – "+t("spotter_but_in")+": "+esc(others);
    }else if(prefixSuggestions.length){
      S.spotterMsg="🔍 Meintest du: "+prefixSuggestions.join(", ")+"?";
    }else{
      S.spotterMsg="âŒ "+t("spotter_unknown")+": "+esc(code);
    }
    S.spotterOk=false;render();return;
  }
  const mainPlate=candidates[0];
  const mainCountry=mainPlate.country;
  const key=collKey(code,mainCountry);
  if(S.collectedPlates.includes(key)){
    S.spotterMsg=t("spotter_dup",{code:esc(code),country:displayCountry(mainCountry)});S.spotterOk=null;
  }else{
    S.collectedPlates.push(key);saveCollectedPlates(S.collectedPlates);saveCollectedTs(key,Date.now());
    const extras=candidates.length-1;
    S.spotterMsg="\u{1F389} "+code+(mainPlate.region?" – "+esc(mainPlate.region):"")+(" ("+esc(displayCountry(mainCountry))+")")+(extras?" +"+extras+" weitere":"")+"\!";
    S.sc+=50;showPtsPopup(50);S.spotterOk=true;soundStamp();
  }
  S.spotterInput="";render();
}

/* â”€â”€ Real plate HTML â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€*/
function renderRealPlate(code,region,extra){
  return`<div class="real-plate">
    <div class="rp-eu-strip"><span class="rp-stars">â˜…</span></div>
    <div class="rp-body">
      <div class="rp-code">${esc(code)}</div>
      ${region?`<div class="rp-region">${esc(region)}${extra>0?" "+t("plates_more",{n:extra}):""}</div>`:""}
    </div>
  </div>`;
}

/* â”€â”€ Collection Screen â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€*/
function renderCollectionScreen(){
  if(\!PLATES_DATA.length)return`<div class="panel" style="text-align:center;padding:2rem"><div style="font-size:2rem">â³</div><p style="color:var(--text3);margin-top:.5rem">Kennzeichen-Daten werden geladen…</p></div>`;
  /* Run migration once per session */
  if(\!window._platesMigrated){window._platesMigrated=true;migrateCollectedPlates();}

  const coll=S.collectedPlates;
  const total=totalUniquePlates();
  const pct=Math.round(coll.length/Math.max(total,1)*100);
  const countries=[...new Set(PLATES_DATA.map(p=>p.country))].sort();
  const view=S.albumView||"list";
  /* P126: reset legacy "all" state – spotter dropdown no longer has "all" */
  if(S.albumCountry==="all"||\!S.albumCountry){S.albumCountry=_smartDefaultCountry()||"Deutschland";S.spotterCountry=S.albumCountry;localStorage.setItem('geoquest_pref_country',S.albumCountry);}
  const acF=S.albumCountry||"all";
  const sCountry=S.spotterCountry||"all";

  /* Achievements: all unique codes in a country collected */
  const achs=countries.filter(c=>{
    const uCodes=getUniquePlatesForCountry(c);
    return uCodes.length>0&&uCodes.every(u=>isCollected(u.code,c));
  });

  /* â”€â”€ Spotter â”€â”€ */
  /* â”€â”€ Phase 105: Country-Help Lookup â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
  const _CHLP=c=>{const M={
    'Deutschland':{ph:'K\u00fcrzel (z.B. B, M, S...)',info:'K\u00fcrzel links (vorne) = Landkreis/Stadt',tp:'de',ex:'M',lbl:'Das M vorne steht f\u00fcr Stadt/Landkreis',cc:'D',nums:'MW 123'},
    '\u00d6sterreich':{ph:'K\u00fcrzel (z.B. W, S, I...)',info:'1\u20133 Buchst. links = Bezirk',tp:'de',ex:'W',lbl:'Das W vorne steht f\u00fcr Stadt/Bezirk',cc:'A',nums:'12345 AB'},
    'Schweiz':{ph:'K\u00fcrzel (z.B. ZH, BE...)',info:'2 Buchst. links = Kanton',tp:'ch',ex:'ZH',lbl:'ZH steht f\u00fcr den Kanton',cc:'CH',nums:'123 456'},
    'Frankreich':{ph:'D\u00e9partement (z.B. 75, 13...)',info:'2-stellige D\u00e9partement-Nummer rechts',tp:'fr',ex:'75',lbl:'Die 75 rechts steht f\u00fcr das D\u00e9partement',cc:'F',nums:'AB-123-CD'},
    'Italien':{ph:'K\u00fcrzel (z.B. RM, MI...)',info:'2 Buchst. links = Provinz',tp:'de',ex:'RM',lbl:'RM steht f\u00fcr Rom',cc:'I',nums:'RM 123 AB'},
    'Polen':{ph:'K\u00fcrzel (z.B. W, KR...)',info:'Links = Woiwodschaft/Stadt-K\u00fcrzel',tp:'de',ex:'W',lbl:'W steht f\u00fcr Warschau',cc:'PL',nums:'KR 12345'},
    'Rum\u00e4nien':{ph:'K\u00fcrzel (z.B. B, CJ...)',info:'1\u20132 Buchst. links = Bezirk',tp:'de',ex:'B',lbl:'B steht f\u00fcr Bukarest',cc:'RO',nums:'CJ 12 ABC'},
    'Bulgarien':{ph:'K\u00fcrzel (z.B. C, PB...)',info:'Buchst. links = Region',tp:'de',ex:'C',lbl:'C steht f\u00fcr Sofia',cc:'BG',nums:'PB 1234 AB'},
    'T\u00fcrkei':{ph:'Nummer (z.B. 06, 34...)',info:'Nummer links = Provinz (34=Istanbul)',tp:'tr',ex:'34',lbl:'34 steht f\u00fcr Istanbul',cc:'TR',nums:'34 ABC 12'},
    'Kroatien':{ph:'K\u00fcrzel (z.B. ZG, ST...)',info:'2 Buchst. links = Gespanschaft',tp:'de',ex:'ZG',lbl:'ZG steht f\u00fcr Zagreb',cc:'HR',nums:'ZG 123-AB'},
    'Slowenien':{ph:'K\u00fcrzel (z.B. LJ, MB...)',info:'2 Buchst. links = Region',tp:'de',ex:'LJ',lbl:'LJ steht f\u00fcr Ljubljana',cc:'SLO',nums:'LJ 123-AB'},
    'Niederlande':{ph:'NL',info:'Kein Regionalk\u00fcrzel – Oval-Code "NL" eingeben',tp:'nat',ex:'NL',lbl:'NL = Niederlande',cc:'NL',nums:''},
    'Belgien':{ph:'B',info:'Kein Regionalk\u00fcrzel – Oval-Code "B" eingeben',tp:'nat',ex:'B',lbl:'B = Belgien',cc:'B',nums:''},
    'D\u00e4nemark':{ph:'DK',info:'Kein Regionalk\u00fcrzel – Oval-Code "DK" eingeben',tp:'nat',ex:'DK',lbl:'DK = D\u00e4nemark',cc:'DK',nums:''},
    'Schweden':{ph:'S',info:'Kein Regionalk\u00fcrzel – Oval-Code "S" eingeben',tp:'nat',ex:'S',lbl:'S = Schweden',cc:'S',nums:''},
    'Norwegen':{ph:'N',info:'Kein Regionalk\u00fcrzel – Oval-Code "N" eingeben',tp:'nat',ex:'N',lbl:'N = Norwegen',cc:'N',nums:''},
    'Spanien':{ph:'E',info:'Kein Regionalk\u00fcrzel – Oval-Code "E" eingeben',tp:'nat',ex:'E',lbl:'E = Spanien',cc:'E',nums:''},
    'Portugal':{ph:'P',info:'Kein Regionalk\u00fcrzel – Oval-Code "P" eingeben',tp:'nat',ex:'P',lbl:'P = Portugal',cc:'P',nums:''},
    'Finnland':{ph:'FIN',info:'Kein Regionalk\u00fcrzel – Oval-Code "FIN" eingeben',tp:'nat',ex:'FIN',lbl:'FIN = Finnland',cc:'FIN',nums:''},
    'Irland':{ph:'IRL',info:'Kein Regionalk\u00fcrzel – Oval-Code "IRL" eingeben',tp:'nat',ex:'IRL',lbl:'IRL = Irland',cc:'IRL',nums:''},
    'Gro\u00dfbritannien':{ph:'GB',info:'Kein Regionalk\u00fcrzel – Oval-Code "GB" eingeben',tp:'nat',ex:'GB',lbl:'GB = Gro\u00dfbritannien',cc:'GB',nums:''},
    'Ungarn':{ph:'H',info:'Kein Regionalk\u00fcrzel – Oval-Code "H" eingeben',tp:'nat',ex:'H',lbl:'H = Ungarn',cc:'H',nums:''},
    'Slowakei':{ph:'SK',info:'Kein Regionalk\u00fcrzel – Oval-Code "SK" eingeben',tp:'nat',ex:'SK',lbl:'SK = Slowakei',cc:'SK',nums:''},
    'Tschechien':{ph:'CZ',info:'Kein Regionalk\u00fcrzel – Oval-Code "CZ" eingeben',tp:'nat',ex:'CZ',lbl:'CZ = Tschechien',cc:'CZ',nums:''},
    'Luxemburg':{ph:'L',info:'Kein Regionalk\u00fcrzel – Oval-Code "L" eingeben',tp:'nat',ex:'L',lbl:'L = Luxemburg',cc:'L',nums:''},
    'Litauen':{ph:'LT',info:'Kein Regionalk\u00fcrzel – Oval-Code "LT" eingeben',tp:'nat',ex:'LT',lbl:'LT = Litauen',cc:'LT',nums:''},
    'Lettland':{ph:'LV',info:'Kein Regionalk\u00fcrzel – Oval-Code "LV" eingeben',tp:'nat',ex:'LV',lbl:'LV = Lettland',cc:'LV',nums:''},
    'Estland':{ph:'EST',info:'Kein Regionalk\u00fcrzel – Oval-Code "EST" eingeben',tp:'nat',ex:'EST',lbl:'EST = Estland',cc:'EST',nums:''},
    'Ukraine':{ph:'UA',info:'Kein Regionalk\u00fcrzel – Oval-Code "UA" eingeben',tp:'nat',ex:'UA',lbl:'UA = Ukraine',cc:'UA',nums:''},
  };
  const r=M[c]||{ph:'K\u00fcrzel eingeben',info:'',tp:'de',ex:'AB',lbl:'Regionales K\u00fcrzel',cc:'EU',nums:'1234'};
  /* Phase 105b: NAT dynamic ph+info aus PLATES_DATA */
  if(r.tp==='nat'&&typeof PLATES_DATA!='undefined'&&PLATES_DATA.length){
    const _ne=PLATES_DATA.filter(p=>p.country===c);
    if(_ne.length===1){const _nc=_ne[0].code;
      r.ph='"'+_nc+'" eingeben';
      r.info='Keine Regionen – "'+_nc+'" eingeben, um das Land zu sammeln';
      r.ex=_nc;r.lbl=_nc+' = '+c;r.cc=_nc;}
  }
  return r;};
  /* Phase 105: SVG Plate Preview */
  const _ch=sCountry==='nat'
    ?{ph:'L\u00e4nderk\u00fcrzel (z.B. NL, I, DK...)',info:'Internationales Oval-K\u00fcrzel',tp:'nat',ex:'NL',lbl:'Internationales L\u00e4nderk\u00fcrzel',cc:'',nums:''}
    :sCountry\!=='all'?_CHLP(sCountry)
    :{ph:'Kennzeichen/K\u00fcrzel eingeben...',info:'',tp:'de',ex:'AB',lbl:'Regionales K\u00fcrzel',cc:'EU',nums:'1234'};
  const _cPH=_ch.ph,_cINFO=_ch.info;
  const _svgP=(()=>{
    if(sCountry==='all')return'';
    const tp=_ch.tp;
    const ex=_ch.ex||'??';
    const cc=_ch.cc||'EU';
    const nums=_ch.nums||'AB 1234';
    const fs=ex.length>3?8:ex.length===3?10:ex.length===2?12:14;
    /* shared SVG wrapper */
    const wrap=(inner,w=162,h=38)=>'<svg width="'+w+'" height="'+h+'" viewBox="0 0 '+w+' '+h+'"'
      +' style="display:block;margin:.5rem auto 0;filter:drop-shadow(0 1px 4px rgba(0,0,0,.2))"'
      +' xmlns="http://www.w3.org/2000/svg">'
      +'<rect x="0" y="0" width="'+w+'" height="'+h+'" rx="5" fill="#f0f0f0" stroke="#ccc" stroke-width="1.5"/>'
      +inner
      +'<rect x="0" y="0" width="'+w+'" height="'+h+'" rx="5" fill="none" stroke="#ccc" stroke-width="1.5"/>'
      +'</svg>';
    /* EU-stripe helper (DE/AT/IT/PL etc.) */
    const ccFs=cc.length>2?7:cc.length===2?9:11;
    const euStripe='<rect x="0" y="0" width="20" height="38" rx="4" fill="#003399"/>'
      +'<text x="10" y="12" text-anchor="middle" fill="#fc0" font-size="5.5" font-family="Arial">\u2605\u2605\u2605</text>'
      +'<text x="10" y="28" text-anchor="middle" fill="white" font-size="'+ccFs+'" font-family="Arial" font-weight="bold">'+cc+'</text>';
    /* yellow box helper */
    const bw=ex.length>2?44:38;
    const yBox='<rect x="24" y="4" width="'+bw+'" height="30" rx="3" fill="#fffacc" stroke="#f59e0b" stroke-width="2"/>'
      +'<text x="'+(24+bw/2)+'" y="24" text-anchor="middle" fill="#1a1a1a" font-size="'+fs+'" font-family="Arial" font-weight="bold">'+ex+'</text>';
    const numsX=24+bw+10;
    const numsEl='<text x="'+numsX+'" y="24" text-anchor="start" fill="#aaa" font-size="9.5" font-family="Arial">'+nums+'</text>';
    /* DE / AT / IT / PL ... – EU stripe left, yellow box, number right */
    if(tp==='de')return wrap(euStripe+yBox+numsEl);
    /* CH – Swiss cross left (red/white), yellow box, number right */
    if(tp==='ch'){
      const chCross='<rect x="2" y="5" width="16" height="28" rx="3" fill="#D00"/>'
        +'<rect x="7" y="8" width="6" height="22" rx="1" fill="white"/>'
        +'<rect x="3" y="16" width="14" height="6" rx="1" fill="white"/>';
      return wrap(chCross+yBox+numsEl);
    }
    /* FR – EU stripe [F] left, example centre, dept number right (blue box) */
    if(tp==='fr'){
      const deptBox='<rect x="130" y="0" width="32" height="38" rx="4" fill="#002699" opacity=".9"/>'
        +'<rect x="126" y="4" width="32" height="30" rx="3" fill="none" stroke="#f59e0b" stroke-width="2"/>'
        +'<text x="142" y="26" text-anchor="middle" fill="#fff" font-size="'+fs+'" font-family="Arial" font-weight="bold">'+ex+'</text>';
      const frNums='<text x="76" y="24" text-anchor="middle" fill="#bbb" font-size="9.5" font-family="Arial">'+nums+'</text>';
      return wrap(euStripe+frNums+deptBox);
    }
    /* TR – yellow box left, pipe, number right */
    if(tp==='tr'){
      return wrap(
        '<rect x="4" y="5" width="36" height="28" rx="3" fill="#fffacc" stroke="#f59e0b" stroke-width="2"/>'
        +'<text x="22" y="25" text-anchor="middle" fill="#1a1a1a" font-size="'+fs+'" font-family="Arial" font-weight="bold">'+ex+'</text>'
        +'<line x1="45" y1="9" x2="45" y2="29" stroke="#ddd" stroke-width="1"/>'
        +'<text x="104" y="24" text-anchor="middle" fill="#aaa" font-size="9.5" font-family="Arial">'+nums+'</text>');
    }
    /* NAT – oval badge */
    if(tp==='nat'){
      const nfs=ex.length>3?12:ex.length===3?14:17;
      return'<svg width="82" height="52" viewBox="0 0 82 52"'
        +' style="display:block;margin:.5rem auto 0;filter:drop-shadow(0 1px 4px rgba(0,0,0,.2))"'
        +' xmlns="http://www.w3.org/2000/svg">'
        +'<ellipse cx="41" cy="26" rx="37" ry="22" fill="#f5f5f5" stroke="#003399" stroke-width="2.5"/>'
        +'<text x="41" y="32" text-anchor="middle" fill="#003399" font-size="'+nfs+'"'
        +' font-family="Arial" font-weight="900">'+ex+'</text>'
        +'</svg>';
    }
    /* default – EU fallback */
    return wrap(euStripe+yBox+numsEl);
  })();
  const spotVal=S.spotterInput||"";
  const spotMsg=S.spotterMsg||"";
  const spotCol=S.spotterOk===true?"#10b981":S.spotterOk===false?"#ef4444":"var(--text3)";
  const spotter=`<div class="album-spotter">
    <div style="margin-bottom:.5rem">
      <span class="album-spotter-title">${t("spotter_title")}</span>
    </div>
    <div class="album-spotter-sub">${t("spotter_hint")}</div>
    <select style="width:100%;margin-bottom:.6rem;background:var(--bg3);color:var(--text);border:1.5px solid var(--border);border-radius:8px;padding:.4rem .6rem;font-size:.85rem;font-weight:600" onchange="S.albumCountry=this.value;S.spotterCountry=this.value;localStorage.setItem('geoquest_pref_country',this.value);render()">
      ${(()=>{
        /* P124: regional-only, single smart-pin */
        const _regK=["Deutschland","\u00d6sterreich","Schweiz","Frankreich","Italien","Polen","Rum\u00e4nien","Bulgarien","T\u00fcrkei","Kroatien","Slowenien"];
        const _active=acF\!=="all"&&acF\!=="nat"&&_regK.includes(acF)?acF:_smartDefaultCountry();
        const _pinned=_regK.includes(_active)?_active:"Deutschland";
        const _sep='<option disabled style="opacity:.4">\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500</option>';
        const _pinOpt=`<option value="${esc(_pinned)}" ${acF===_pinned?"selected":""}>${esc(_pinned)}</option>`;
        const _rOpts=[..._regK]
          .filter(c=>c\!==_pinned)
          .sort((a,b)=>a.localeCompare(b,"de"))
          .map(c=>`<option value="${esc(c)}" ${acF===c?"selected":""}>${esc(c)}</option>`)
          .join("");
        const _natSep='<option disabled style="opacity:.4">\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500</option>';
        const _natOpt='<option value="nat" '+(acF==="nat"?"selected":"")+'>🌍 Andere L\u00e4nder (L\u00e4nderk\u00fcrzel)</option>';
        return _pinOpt+_sep+_rOpts+_natSep+_natOpt;
      })()}
    </select>
    <div style="display:flex;gap:8px">
      <input type="text" maxlength="6" placeholder="${_cPH}" value="${esc(spotVal)}" autocapitalize="characters" autocorrect="off" autocomplete="off" spellcheck="false"
        oninput="S.spotterInput=this.value.toUpperCase();this.value=this.value.toUpperCase();S.spotterMsg=''"
        class="spotter-input">
      <button class="btn-p" style="width:auto;padding:.5rem 1rem;margin-bottom:0" onclick="spotterCollect()">${t("btn_collect")}</button>
    </div>
    ${spotMsg?`<div style="font-size:.82rem;font-weight:700;text-align:center;color:${spotCol};padding:.35rem 0;margin-top:4px">${esc(spotMsg)}</div>`:""}
    ${_cINFO?`<div class="spotter-help-row">${_cINFO}</div>`:""}
    ${_svgP?`<div class="spotter-plate-preview">${_svgP}<div class="spotter-plate-label">&#9650; ${_ch.lbl}</div></div>`:""}
  </div>`;

  /* â”€â”€ Progress â”€â”€ */
  const progressBar=`<div class="album-progress-wrap">
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:5px">
      <span style="font-weight:900;font-size:1rem">${t("album_title")}</span>
      <span style="font-size:.78rem;color:var(--text3)">${coll.length}&thinsp;/&thinsp;${total}</span>
    </div>
    <div class="coll-progress-wrap"><div class="coll-progress-bar" style="width:${pct}%"></div></div>
    <div style="text-align:right;font-size:.65rem;color:var(--text3);margin-top:2px">${t("pct_complete",{pct})}</div>
  </div>`;

  /* â”€â”€ Achievements â”€â”€ */
  const achBar=achs.length?`<div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:.7rem">${achs.map(c=>`<span class="coll-ach">\u{1F3C6} ${esc(c)}-Experte</span>`).join("")}</div>`:"";

  /* â”€â”€ Controls â”€â”€ */
  const controls=`<div style="display:flex;gap:6px;margin-bottom:.7rem;align-items:center">
    <button class="view-toggle-btn${view==="list"?" active":""}" onclick="S.albumView='list';render()">${t("album_list")}</button>
    <button class="view-toggle-btn${view==="map"?" active":""}" onclick="S.albumView='map';render()">${t("album_map")}</button>
  </div>`;

  /* â”€â”€ List view: Hybrid (Neueste 5 + Akkordeon-Archiv nach Land) â”€â”€ */
  let listContent="";
  if(view==="list"){
    /* Part A: Neueste 5 Funde */
    const recentKeys=coll.slice(-5).reverse();
    let recentHtml="";
    if(recentKeys.length>0){
      const _cTs=loadCollectedTs();
      const recentItems=recentKeys.map(key=>{
        const sep=key.indexOf("::");const code=key.slice(0,sep);const country=key.slice(sep+2);
        const p=PLATES_DATA.find(x=>x.code===code&&x.country===country)||{code,region:code,country};
        const _ago=(_cTs&&_cTs[key])?timeAgo(_cTs[key]):"";
        return`<div style="box-sizing:border-box;width:100%;max-width:100%;display:flex;align-items:center;gap:.5rem;margin-bottom:.4rem;background:var(--bg2);border-radius:8px;padding:.4rem .6rem">
          <div style="flex:0 0 auto">${renderRealPlate(p.code,p.region,0)}</div>
          <div style="flex:1;min-width:0">
            <div style="font-size:.75rem;color:var(--text2);font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${esc(country)}</div>
            ${_ago?`<div style="font-size:.63rem;color:#888;margin-top:1px">${_ago}</div>`:""}
          </div>
        </div>`;
      }).join("");
      recentHtml=`<div style="margin-bottom:.85rem">
        <div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin-bottom:.5rem">\u{1F552} ALLE FUNDE</div>
        ${recentItems}
      </div>`;
    }
    /* Part B: Akkordeon-Archiv (P127: bulletproof <details>/<summary>) */
    /* FIX: summary must NOT use display:flex or list-style:none –        */
    /* those CSS properties break the native toggle in WebKit/iOS.         */
    const showCountries=(acF==="all"||acF==="nat")?countries:[acF];
    const archiveRows=showCountries.map(country=>{
      try{
        const uPlates=getUniquePlatesForCountry(country)||[];
        if(\!uPlates.length)return"";
        const collHere=uPlates.filter(u=>isCollected(u.code,country));
        if(\!collHere.length)return"";
        const cPct=Math.round(collHere.length/Math.max(uPlates.length,1)*100);
        /* Render plates – use mainRegion||region fallback so nothing is dropped */
        const plateHtml=collHere
          .map(u=>renderRealPlate(u.code,u.mainRegion||u.region||"",u.count-1||0))
          .join("");
        return`<details style="margin-bottom:.5rem;border:1px solid var(--border);border-radius:10px;overflow:hidden">
          <summary style="padding:.5rem .75rem;cursor:pointer;font-weight:700;font-size:.82rem;user-select:none;background:var(--bg2)">${esc(country)} – ${collHere.length}/${uPlates.length} \u00b7 ${cPct}%</summary>
          <div style="padding:.6rem .75rem;background:var(--bg)">
            <div style="height:3px;background:var(--bg4);border-radius:2px;overflow:hidden;margin-bottom:.6rem"><div style="height:100%;width:${cPct}%;background:#10b981;border-radius:2px"></div></div>
            <div class="real-plate-grid">${plateHtml}</div>
          </div>
        </details>`;
      }catch(_arcErr){return"";}
    }).join("");
    const archiveTotal=coll.length;
    const archivePossible=totalUniquePlates();
    const archiveSection=archiveRows
      ?`<details style="margin-top:12px;border:1px solid var(--border);border-radius:12px;overflow:hidden">
          <summary style="padding:.65rem .85rem;cursor:pointer;font-weight:bold;user-select:none;background:var(--bg2)">\u{1F4C1} Gesamte Sammlung ansehen (${archiveTotal}/${archivePossible})</summary>
          <div style="padding:.65rem .75rem">${archiveRows}</div>
        </details>`
      :`<div style="text-align:center;padding:2rem;color:var(--text3)">${t("album_empty").replace("\n","<br>")}</div>`;
    listContent=recentHtml+archiveSection;
    if(\!listContent.trim())listContent=`<div style="text-align:center;padding:2rem;color:var(--text3)">${t("album_empty").replace("\n","<br>")}</div>`;
  }

  const mapContent=view==="map"?`<div id="album-map-svg" class="album-map-container"></div>`:"";

  if(view==="map")requestAnimationFrame(()=>drawAlbumMap());

  const backBtn=`<button onclick="S.tab='home';render()" style="display:flex;align-items:center;gap:6px;background:none;border:none;color:var(--text3);font-size:.82rem;font-weight:700;cursor:pointer;padding:.3rem .1rem;margin-bottom:.6rem;letter-spacing:.3px;transition:color .15s" onmouseenter="this.style.color='var(--text)'" onmouseleave="this.style.color='var(--text3)'"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>${t('btn_back')}</button>`;
  return`<div>${backBtn}${spotter}${progressBar}${achBar}${controls}${listContent}${mapContent}</div>`;
}

/* â”€â”€ Trophy Map â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€*/
function drawAlbumMap(){
  const el=document.getElementById("album-map-svg");
  if(\!el||typeof d3==="undefined"||typeof topojson==="undefined"||\!window.WORLD_TOPO)return;

  const coll=S.collectedPlates;
  /* Collected countries (EN) →’ unique codes collected there */
  const collByCountryEn={};
  coll.forEach(key=>{
    const {code,country}=parseCollKey(key);
    const en=plateCountryToEn(country);
    if(\!collByCountryEn[en])collByCountryEn[en]=[];
    /* Only add unique codes */
    if(\!collByCountryEn[en].includes(code))collByCountryEn[en].push(code);
  });
  const collCountrySet=new Set(Object.keys(collByCountryEn));

  const W=el.clientWidth||(window.innerWidth-32)||360;
  const H=Math.min(W*0.58,280);
  const proj=d3.geoMercator().scale(W*0.95).center([12,52]).translate([W/2,H/2]);
  const geoPath=d3.geoPath().projection(proj);
  const countriesGeo=topojson.feature(window.WORLD_TOPO,window.WORLD_TOPO.objects.countries);

  d3.select(el).html("");
  const svg=d3.select(el).append("svg")
    .attr("width","100%").attr("height",H)
    .style("border-radius","12px").style("display","block")
    .style("background","#c8dff0");

  /* Graticule */
  svg.append("path").datum(d3.geoGraticule()())
    .attr("d",geoPath).attr("fill","none")
    .attr("stroke","#b0cce0").attr("stroke-width",.3);

  const g=svg.append("g");

  /* Country fills */
  g.selectAll("path.country").data(countriesGeo.features)
    .join("path").attr("class","country")
    .attr("d",geoPath)
    .attr("fill",d=>{
      const name=d.properties&&d.properties.name;
      return collCountrySet.has(name)?"#10b981":"#d4dfe8";
    })
    .attr("stroke","#fff").attr("stroke-width",.4);

  /* Pins at country centroids for collected countries */
  const pinData=countriesGeo.features.filter(d=>{
    return d.properties&&collCountrySet.has(d.properties.name);
  }).map(d=>{
    const name=d.properties.name;
    const c=geoPath.centroid(d);
    return{name,c,codes:collByCountryEn[name]||[]};
  }).filter(d=>d.c&&\!isNaN(d.c[0])&&\!isNaN(d.c[1]));

  /* Drop shadow filter */
  const defs=svg.append("defs");
  const filter=defs.append("filter").attr("id","pin-shadow");
  filter.append("feDropShadow").attr("dx",0).attr("dy",1).attr("stdDeviation",1.5).attr("flood-opacity",.35);

  const pinG=g.append("g").attr("class","pins");
  pinData.forEach(d=>{
    const pg=pinG.append("g")
      .attr("transform","translate("+d.c[0]+","+d.c[1]+")")
      .style("cursor","pointer")
      .on("click",function(ev){
        ev.stopPropagation();
        d3.select(el).selectAll(".map-popup").remove();
        /* Position popup near pin, avoid overflow */
        const rect=el.getBoundingClientRect();
        const px=Math.min(d.c[0]+8,W-180);
        const py=Math.max(d.c[1]-60,4);
        const pop=d3.select(el).append("div")
          .attr("class","map-popup")
          .style("left",px+"px").style("top",py+"px")
          .style("min-width","150px").style("max-width","200px");
        pop.append("button").attr("class","map-popup-close")
          .text("✓•").on("click",()=>d3.select(el).selectAll(".map-popup").remove());
        pop.append("div").attr("class","map-popup-title")
          .text(d.name+" ("+d.codes.length+")");
        const grid=pop.append("div").attr("class","map-popup-grid");
        d.codes.slice(0,9).forEach(code=>{
          const plates=PLATES_DATA.filter(p=>p.code===code&&plateCountryToEn(p.country)===d.name);
          const region=plates.length?plates[0].region:"";
          const item=grid.append("div").attr("class","real-plate real-plate-sm");
          item.append("div").attr("class","rp-eu-strip")
            .append("span").attr("class","rp-stars").text("â˜…");
          const body=item.append("div").attr("class","rp-body");
          body.append("div").attr("class","rp-code").text(code);
          if(plates.length>1)body.append("div").attr("class","rp-region").text("+"+(plates.length-1));
        });
        if(d.codes.length>9)pop.append("div")
          .style("font-size",".65rem").style("color","var(--text3)").style("margin-top","3px")
          .text(t("plates_more",{n:d.codes.length-9}));
      });

    /* Pin circle with glow */
    pg.append("circle").attr("r",7).attr("fill","#10b981")
      .attr("stroke","#fff").attr("stroke-width",1.5)
      .attr("filter","url(#pin-shadow)");
    /* Count badge */
    pg.append("text").attr("text-anchor","middle").attr("dy","0.35em")
      .attr("fill","#fff").attr("font-size","6px").attr("font-weight","bold")
      .attr("pointer-events","none")
      .text(d.codes.length>9?"9+":d.codes.length);
  });

  /* Click outside popup closes it */
  svg.on("click",()=>d3.select(el).selectAll(".map-popup").remove());

  /* Pan/zoom (on g group, not pins layer) */
  svg.call(d3.zoom().scaleExtent([1,10]).on("zoom",ev=>{
    g.attr("transform",ev.transform);
  }));
}

/* HOME TAB */
/* ===================================================================
   PHASE 86 – Logik-Gitter + Reiseroute
   =================================================================== */

/* Shared: save score and transition to gameover screen */
function submitGridResult(){if(S.gridData){S.sc=S.gridData.score;S.correct=S.gridData.correctCount;S.rd=S.gridData.correctCount;}finishCustomGame();}
function finishCustomGame(){
  soundOver();
  S.ph="gameover";S.scoreSaved=false;S.convModal=true;
  checkMastery();
  saveHistory({mode:S.mode,score:S.sc,correct:S.correct,rounds:S.correct,date:Date.now(),answers:[]});
  if(sbOK)saveSession(S.mode,S.sc,S.sc,S.correct,Date.now()-(S.gameStartTime||Date.now())).then(()=>{S.scoreSaved=true;render();});
  render();
}

/* ---- Logik-Gitter ---- */
function checkGridCriterion(name,crit,item){
  /* P161: Stadt */
  if(crit.type==="city_continent"){const c=item||CITIES.find(x=>x.name===name);return c?c.continent===crit.value:false;}
  if(crit.type==="city_country")  {const c=item||CITIES.find(x=>x.name===name);return c?c.country===crit.value:false;}
  if(crit.type==="city_letter")   {return(name[0]||"").toUpperCase()===crit.value;}
  /* P161: Wahrzeichen */
  if(crit.type==="lm_continent")  {const l=item||LANDMARKS.find(x=>x.name===name);return l?l.continent===crit.value:false;}
  if(crit.type==="lm_letter")     {return(name[0]||"").toUpperCase()===crit.value;}
  /* P161: UNESCO */
  if(crit.type==="un_continent")  {const u=item||UNESCO_SITES.find(x=>x.name===name);return u?u.continent===crit.value:false;}
  if(crit.type==="un_letter")     {return(name[0]||"").toUpperCase()===crit.value;}
  /* P168: Food */
  if(crit.type==="food_continent"){const f=item||FOOD_DATA.find(x=>x.dish===name);if(\!f)return false;const co=COUNTRIES.find(c=>c.cc===f.cc);if(\!co)return false;if(crit.value==="Americas")return co.ct==="North America"||co.ct==="South America";return co.ct===crit.value;}
  if(crit.type==="food_letter")   {return(name[0]||"").toUpperCase()===crit.value;}
  /* original Land logic */
  const co=COUNTRIES.find(c=>c.c===name);
  if(!co)return false;
  if(crit.type==="continent")return co.ct===crit.value;
  if(crit.type==="letter"){
    const _lang=(typeof S!=="undefined"&&S.language)||"de";
    let _ln=name;
    try{if(co)_ln=getCountryName(co.cc,_lang)||name;}catch(e){}
    return(_ln[0]||"").toUpperCase()===crit.value;
  }
  if(crit.type==="has_border"){const nbs=ROUTE_BORDERS[crit.value]||[];return nbs.includes(name);}
  if(crit.type==="subregion")return co.sr===crit.value;
  if(crit.type==="island")return _ISLAND_STATES.has(name);
  if(crit.type==="landlocked")return _LANDLOCKED_SET.has(name);
  if(crit.type==="eu_member")return _EU_MEMBERS.has(name);
  return false;
}
function getGridSugg(txt){
  if(!txt||txt.length<1)return[];
  const t=txt.toLowerCase();
  const gtype=(S.gridData&&S.gridData.gridType)||"land";
  const used=(S.gridData&&S.gridData.usedCountries instanceof Set)?S.gridData.usedCountries:new Set();
  /* P161: type-specific search */
  if(gtype==="stadt"){
    return CITIES
      .filter(c=>!used.has(c.name)&&(c.name.toLowerCase().startsWith(t)||(c.asciiName||"").toLowerCase().startsWith(t)))
      .sort((a,b)=>b.population-a.population)
      .slice(0,12).map(c=>c.name);
  }
  if(gtype==="wahrzeichen"){
    return LANDMARKS
      .filter(l=>!used.has(l.name)&&l.name.toLowerCase().startsWith(t))
      .slice(0,12).map(l=>l.name);
  }
  if(gtype==="unesco"){
    return UNESCO_SITES
      .filter(u=>!used.has(u.name)&&u.name.toLowerCase().startsWith(t))
      .slice(0,12).map(u=>u.name);
  }
  /* P168: Food */
  if(gtype==="food"){
    return (FOOD_DATA||[])
      .filter(f=>!used.has(f.dish)&&f.dish.toLowerCase().startsWith(t))
      .map(f=>f.dish).slice(0,12);
  }
  /* original Land logic */
  const lang=(typeof S!=="undefined"&&S.language)||localStorage.getItem("gq_lang")||"de";
  return COUNTRIES
    .filter(c=>{
      if(!c.ct||used.has(c.c))return false;
      if(c.c.toLowerCase().startsWith(t))return true;
      try{return getCountryName(c.cc,lang).toLowerCase().startsWith(t);}catch(e){return false;}
    })
    .map(c=>c.c)
    .sort((a,b)=>{
      const ca=COUNTRIES.find(x=>x.c===a),cb=COUNTRIES.find(x=>x.c===b);
      const la=ca?getCountryName(ca.cc,lang):a;
      const lb=cb?getCountryName(cb.cc,lang):b;
      try{return la.localeCompare(lb,lang);}catch(e){return la<lb?-1:la>lb?1:0;}
    })
    .slice(0,12);
}
/* P142: update only the suggestion list -- do NOT call render() to avoid Gboard cursor reset */
function lgUpdate(val){
  S.gridInput=val;
  S.gridSugg=getGridSugg(val);
  const el=document.querySelector('.lg-sugg');
  if(!el)return;
  const gd=S.gridData;
  if(!gd||!gd.activeCell){el.innerHTML="";return;}
  const gtype=gd.gridType||"land";
  el.innerHTML=(S.gridSugg||[]).slice(0,12).map(s=>{
    let icon="",label=esc(s); /* XSS defense */
    if(gtype==="stadt"){
      const ci=CITIES.find(c=>c.name===s);
      icon=ci?flagOf(ci.country||ci.cc||""):"";
      label=s+(ci?" ("+displayCountry(ci.countryCode||ci.cc||"")+")":" ");
    }else if(gtype==="wahrzeichen"){
      icon="";
      const lm=LANDMARKS.find(l=>l.name===s);
      label=s+(lm?" \u00b7 "+displayCountry(lm.cc):"");
    }else if(gtype==="unesco"){
      icon="";
      const un=UNESCO_SITES.find(u=>u.name===s);
      label=s+(un?" \u00b7 "+displayCountry(un.cc):"");
    }else{
      const _co=COUNTRIES.find(c=>c.c===s);
      const _lang=(typeof S!=="undefined"&&S.language)||"de";
      icon=flagOf(s);
      label=_co?getCountryName(_co.cc,_lang):s;
    }
    return `<div class="lg-sugg-item" data-name="${esc(s)}" onclick="handleGridAnswer(S.gridData.activeCell.r,S.gridData.activeCell.c,this.dataset.name)">${icon} ${esc(label)}</div>`;
  }).join("");
}
function handleGridAnswer(r,c,name){
  const gd=S.gridData;
  if(!gd||gd.solved||gd.failed)return;
  const cell=gd.cells[r*3+c];
  if(cell.country)return;
  const gtype=gd.gridType||"land";
  let item=null;
  if(gtype==="stadt")         item=CITIES.find(x=>x.name===name);
  else if(gtype==="wahrzeichen")item=LANDMARKS.find(x=>x.name===name);
  else if(gtype==="unesco")   item=UNESCO_SITES.find(x=>x.name===name);
  else if(gtype==="food")     item=(FOOD_DATA||[]).find(x=>x.dish===name);
  const ok=checkGridCriterion(name,gd.rowCrit[r],item)&&checkGridCriterion(name,gd.colCrit[c],item);
  if(ok){
    cell.country=name;
    gd.usedCountries.add(name);
    gd.correctCount++;
    gd.score+=500+gd.lives*50;
    gd.lastMsg="\u2713 Richtig! "+name;
    gd.lastOk=true;
    gd.activeCell=null;
    S.gridInput="";
    S.gridSugg=[];
    if(gd.correctCount>=9)gd.solved=true;
  }else{
    gd.lives--;
    gd.lastMsg="\u2717 "+name+" passt nicht zu beiden Kriterien.";
    gd.lastOk=false;
    if(gd.lives<=0){gd.failed=true;gd.activeCell=null;}
  }
  /* P150: stop timer on game end */
  if(gd.solved||gd.failed)clearInterval(tIv);
  S.sc=gd.score;
  render();
}
function initLogikGitter(){
  _secretGameToken=Math.random().toString(36).substring(2,15);
  function _shuf(a){const b=a.slice();for(let i=b.length-1;i>0;i--){const j=~~(Math.random()*(i+1));[b[i],b[j]]=[b[j],b[i]];}return b;}
  /* P161/P164: type selection -- honour S.gridTypeMode when not "random" */
  const _gtm=(typeof S!=="undefined"&&S.gridTypeMode&&S.gridTypeMode!=="random")?S.gridTypeMode:null;
  const _types=["land","land","land","stadt","wahrzeichen","unesco","food"];
  const gtype=_gtm||_types[~~(Math.random()*_types.length)];
  let rowPool,colPool,fallback,checkFn;
  if(gtype==="land"){
    rowPool=GRID_ROW_POOL;colPool=GRID_COL_POOL;
    fallback={r:["eu","as","af"],c:["ls","lm","lp"]};
    const allCo=COUNTRIES.filter(c=>c.ct);
    checkFn=(_,rc,cc)=>allCo.some(co=>checkGridCriterion(co.c,rc)&&checkGridCriterion(co.c,cc));
  }else if(gtype==="stadt"){
    rowPool=GRID_CITY_ROW_POOL;colPool=GRID_CITY_COL_POOL;
    fallback={r:["ceu","cas","cna"],c:["clb","clm","cls"]};
    checkFn=(_,rc,cc)=>CITIES.some(ci=>checkGridCriterion(ci.name,rc,ci)&&checkGridCriterion(ci.name,cc,ci));
  }else if(gtype==="wahrzeichen"){
    rowPool=GRID_LM_ROW_POOL;colPool=GRID_LM_COL_POOL;
    fallback={r:["leu","las","laf"],c:["lla","llk","lls"]};
    checkFn=(_,rc,cc)=>LANDMARKS.some(l=>checkGridCriterion(l.name,rc,l)&&checkGridCriterion(l.name,cc,l));
  }else if(gtype==="food"){
    rowPool=GRID_FOOD_ROW_POOL;colPool=GRID_FOOD_COL_POOL;
    fallback={r:["feu","fas","fam"],c:["flb","flc","flp"]};
    checkFn=(_,rc,cc)=>(FOOD_DATA||[]).some(f=>checkGridCriterion(f.dish,rc,f)&&checkGridCriterion(f.dish,cc,f));
  }else{
    rowPool=GRID_UNESCO_ROW_POOL;colPool=GRID_UNESCO_COL_POOL;
    fallback={r:["ueu","uas","uaf"],c:["ula","ulk","ulp"]};
    checkFn=(_,rc,cc)=>UNESCO_SITES.some(u=>checkGridCriterion(u.name,rc,u)&&checkGridCriterion(u.name,cc,u));
  }
  function _ok(rc,cc){for(let r=0;r<3;r++)for(let c=0;c<3;c++)if(!checkFn(null,rc[r],cc[c]))return false;return true;}
  let rowCrit,colCrit,found=false;
  for(let t=0;t<60&&!found;t++){
    const rows=_shuf(rowPool);
    const cols=_shuf(colPool);
    const rc=[rows[0],rows[1],rows[2]];
    const cc=[cols[0],cols[1],cols[2]];
    if(_ok(rc,cc)){rowCrit=rc;colCrit=cc;found=true;}
  }
  if(!found){
    const byId=id=>[...rowPool,...colPool].find(x=>x.id===id);
    rowCrit=fallback.r.map(byId);colCrit=fallback.c.map(byId);
  }
  S.gridData={rowCrit,colCrit,gridType:gtype,
    cells:Array(9).fill(null).map(()=>({country:null})),
    lives:3,activeCell:null,solved:false,failed:false,
    correctCount:0,score:0,lastMsg:"",lastOk:true,usedCountries:new Set()};
  S.gridInput="";
  S.gridSugg=[];
  /* P150: 90s countdown for Logic Grid */
  S.tm=90;S.dur=90;
  clearInterval(tIv);
  tIv=setInterval(()=>{
    S.tm--;
    if(S.tm<=0){
      clearInterval(tIv);
      if(S.gridData&&!S.gridData.solved&&!S.gridData.failed){
        S.gridData.failed=true;
        S.gridData.lastMsg="\u23f1 Zeit abgelaufen!";
      }
    }
  },1000);
}
function changeGridType(newType){
  if(typeof S==="undefined")return;
  S.gridTypeMode=newType;
  initLogikGitter();
  render();
}
function renderLogikGitter(sc){
  const gd=S.gridData;
  if(!gd)return '<div class="scr"></div>';
  const hearts='\u2764\ufe0f'.repeat(gd.lives)+'\uD83D\uDDA4'.repeat(3-gd.lives);
  /* P136: instruction above grid */
  const _gtype=gd.gridType||"land";
  const _typeLbl=_gtype==="land"?"\uD83C\uDF0D Land":_gtype==="stadt"?"\uD83C\uDFD9 Stadt":_gtype==="wahrzeichen"?"\uD83C\uDFDB Wahrzeichen":"\uD83C\uDF0E UNESCO";
  const _lgInstr='<p style="font-size:.8rem;color:var(--text2);text-align:center;margin-bottom:.6rem;line-height:1.4">Tippe auf ein <b>+</b>-Feld und w\u00e4hle den passenden Begriff, der zur <b>Zeile</b> und <b>Spalte</b> passt!</p>';
  let gridHtml=_lgInstr+'<div class="lg-grid" style="display:grid;grid-template-columns:max-content repeat(3,1fr);gap:8px;margin-top:15px;align-items:stretch">';
  gridHtml+='<div class="lg-corner"><span style="font-size:.6rem;color:var(--text3)">\u2193 Zeile / Spalte \u2192</span></div>';
  for(let c=0;c<3;c++)gridHtml+=`<div class="lg-header">${gd.colCrit[c].label}</div>`;
  for(let r=0;r<3;r++){
    gridHtml+=`<div class="lg-header lg-row-hdr">${gd.rowCrit[r].label}</div>`;
    for(let c=0;c<3;c++){
      const cell=gd.cells[r*3+c];
      const isAct=gd.activeCell&&gd.activeCell.r===r&&gd.activeCell.c===c;
      if(cell.country){
        gridHtml+=`<div class="lg-cell lg-filled">${(()=>{if(_gtype==="land")return flagOf(cell.country)+'<div class="lg-cell-name">'+esc(displayCountry(cell.country))+'</div>';if(_gtype==="stadt"){const _ci=CITIES.find(c=>c.name===cell.country);return (_ci?flagOf(_ci.country||_ci.cc||""):"\uD83C\uDFD9")+'<div class="lg-cell-name">'+esc(cell.country)+'</div>';}if(_gtype==="wahrzeichen")return "\uD83C\uDFDB"+'<div class="lg-cell-name">'+esc(cell.country)+'</div>';return "\uD83C\uDF0E"+'<div class="lg-cell-name">'+esc(cell.country)+'</div>';})()}</div>`;
      }else if(gd.solved||gd.failed){
        gridHtml+='<div class="lg-cell lg-empty-done">–</div>';
      }else{
        const act=isAct?' lg-active':'';
        gridHtml+=`<div class="lg-cell lg-empty${act}" data-r="${r}" data-c="${c}" style="background:#f8f9fa;border:2px dashed #adb5bd;border-radius:8px;display:flex;align-items:center;justify-content:center;height:50px;font-weight:bold;color:#20c997;font-size:1.5em;cursor:pointer"
          onclick="S.gridData.activeCell={r:+this.dataset.r,c:+this.dataset.c};S.gridInput='';S.gridSugg=[];render()">+</div>`;
      }
    }
  }
  gridHtml+='</div>';
  let inputHtml="";
  if(gd.activeCell&&!gd.solved&&!gd.failed){
    const{r,c}=gd.activeCell;
    const sugg=S.gridSugg||[];
    /* P147: localized suggestion labels */
    const _sLang=(typeof S!=="undefined"&&S.language)||"de";
    const suggHtml=sugg.slice(0,12).map(s=>{
      const _sCo=COUNTRIES.find(c=>c.c===s);
      const _sDn=_sCo?getCountryName(_sCo.cc,_sLang):s;
      return `<div class="lg-sugg-item" data-name="${esc(s)}" onclick="handleGridAnswer(S.gridData.activeCell.r,S.gridData.activeCell.c,this.dataset.name)">${flagOf(s)} ${esc(_sDn)}</div>`;
    }).join("");
    inputHtml=`<div class="lg-inp-wrap">
      <div style="font-size:.88rem;font-weight:800;color:var(--text);margin-bottom:4px">\u{1F30D} Welches Konzept passt zu beiden Kriterien?</div>
      <div style="font-size:.75rem;color:var(--text3);margin-bottom:4px;padding:.3rem .5rem;background:var(--bg2);border-radius:8px">\u{1F4CD} <strong>${esc(gd.rowCrit[r].label)}</strong> &amp; <strong>${esc(gd.colCrit[c].label)}</strong></div>
      <div style="font-size:.72rem;font-weight:700;color:var(--text3);margin-bottom:5px">${_gtype==="land"?"\u{1F3AF} GESUCHT: LAND":_gtype==="stadt"?"\uD83C\uDFD9 GESUCHT: STADT":_gtype==="wahrzeichen"?"\uD83C\uDFDB GESUCHT: WAHRZEICHEN":"\uD83C\uDF0E GESUCHT: UNESCO-ST\u00c4TTE"}</div>
      <input type="text" id="lg-inp" placeholder="${gd.gridType==='food'?'Gericht eingeben\u2026':gd.gridType==='stadt'?'Stadt eingeben\u2026':gd.gridType==='wahrzeichen'?'Wahrzeichen eingeben\u2026':gd.gridType==='unesco'?'UNESCO-St\u00e4tte\u2026':'Land eingeben\u2026'}" value="${esc(S.gridInput||'')}"
        oninput="lgUpdate(this.value)"
        onkeydown="if(event.key==='Enter'&&S.gridSugg&&S.gridSugg[0])handleGridAnswer(S.gridData.activeCell.r,S.gridData.activeCell.c,S.gridSugg[0])"
        dir="ltr" style="width:100%;box-sizing:border-box;direction:ltr;text-align:left;padding-left:15px">
      <div class="lg-sugg">${suggHtml}</div>
      <button class="btn-g" style="margin-top:6px;font-size:.78rem;padding:.35rem .7rem" onclick="S.gridData.activeCell=null;render()">Abbrechen</button>
    </div>`;
  }
  const statusHtml=gd.lastMsg
    ?`<div style="text-align:center;color:${gd.lastOk?"#10b981":"#ef4444"};font-size:.82rem;margin:.3rem 0">${esc(gd.lastMsg)}</div>`
    :"";
  const endHtml=(gd.solved||gd.failed)
    ?`<div style="text-align:center;margin:.5rem 0">
        ${gd.solved
          ?'<div style="color:#10b981;font-weight:900;font-size:1.05rem">\u{1F3C6} Alle 9 Zellen gel\u00f6st!</div>'
          :'<div style="color:#ef4444;font-weight:900">\u{1F480} Keine Leben mehr!</div>'}
        <div style="color:var(--text3);font-size:.75rem;margin:.2rem 0">${gd.correctCount} von 9 richtig \u00b7 ${gd.score.toLocaleString()} Punkte</div>
      </div>
      <button class="btn-p" onclick="submitGridResult()">Ergebnis ansehen</button>`
    :"";
  return `<div class="scr">
    <div class="hud">
      <div style="display:flex;gap:8px;align-items:center">
        <div class="pill"><div class="hlbl">SCORE</div><div class="hval">${sc.toLocaleString()}</div></div>
        <div style="font-size:1rem;letter-spacing:1px">${hearts}</div>
      </div>
      <div style="display:flex;align-items:center;gap:8px">
        <div style="font-size:.75rem;color:var(--text3)">${gd.correctCount}/9</div>
        <div style="font-size:.85rem;font-weight:700;min-width:2.2rem;text-align:right;color:${tc()}">${S.tm}s</div>
        <div class="action-bar" style="display:flex;flex-direction:row-reverse;gap:10px;align-items:center"><button class="btn-exit-global" onclick="clr();S.ph='menu';S.tab='home';render()" style="background:#ef4444;color:#fff;border:none;padding:10px 20px;border-radius:8px;font-weight:700;cursor:pointer;white-space:nowrap">🚪 Beenden</button><button class="btn-bug" onclick="reportBug()" style="background:#e2e8f0;color:#475569;border:none;padding:10px 14px;border-radius:8px;font-weight:700;cursor:pointer">🐞 Fehler</button></div>
      </div>
    </div>
    <div class="tbar"><div class="tfill" style="width:${pct()}%;background:${tc()}"></div></div>
    <div style="text-align:center;font-size:.92rem;font-weight:900;color:var(--text);padding:.4rem 0 .2rem">${_typeLbl}</div>
    <div style="text-align:center;margin:.1rem 0 .45rem">
      <select onchange="changeGridType(this.value)" style="padding:5px 12px;border-radius:8px;border:1.5px solid var(--primary,#6366f1);background:var(--bg2);color:var(--text);font-size:.8rem;outline:none;cursor:pointer">
        <option value="random" ${(!S.gridTypeMode||S.gridTypeMode==="random")?"selected":""}>🎲 Zufall (Mix)</option>
        <option value="land" ${S.gridTypeMode==="land"?"selected":""}>🌍 Länder</option>
        <option value="stadt" ${S.gridTypeMode==="stadt"?"selected":""}>🏙 Städte</option>
        <option value="wahrzeichen" ${S.gridTypeMode==="wahrzeichen"?"selected":""}>🏛 Wahrzeichen</option>
        <option value="unesco" ${S.gridTypeMode==="unesco"?"selected":""}>🌎 UNESCO</option>
    <option value="food" ${S.gridTypeMode==="food"?"selected":""}>🍽️ Gerichte</option>
      </select>
    </div>
    ${gridHtml}${statusHtml}${inputHtml}${endHtml}
    <div style="height:1.5rem"></div>
  </div>`;
}

/* ---- Reiseroute ---- */
function getRouteSugg(txt){
  if(!txt||txt.length<1)return[];
  const t=txt.toLowerCase();
  return Object.keys(ROUTE_BORDERS).filter(c=>c.toLowerCase().startsWith(t)).slice(0,6);
}
function handleRouteSubmit(country){
  const rd=S.routeData;
  if(!rd||rd.solved||rd.failed)return;
  const trimmed=(country||"").trim();
  if(!trimmed)return;
  const cur=rd.route[rd.route.length-1];
  const nbs=ROUTE_BORDERS[cur]||[];
  if(!nbs.includes(trimmed)){
    rd.errMsg="\u2717 "+trimmed+" grenzt nicht an "+cur+".";
    rd.lives--;
    S.routeInput="";
    S.routeSugg=[];
    if(rd.lives<=0)rd.failed=true;
    render();return;
  }
  rd.route.push(trimmed);
  rd.steps++;
  rd.errMsg="";
  rd.score+=200;
  S.routeInput="";
  S.routeSugg=[];
  if(trimmed===rd.target){
    rd.solved=true;
    const bonus=Math.max(0,(rd.minSteps+2-rd.steps))*100+500+rd.lives*200;
    rd.score+=bonus;
  }
  S.sc=rd.score;
  render();
}
function initReiseroute(){
  const keys=Object.keys(ROUTE_BORDERS).filter(k=>ROUTE_BORDERS[k].length>=2);
  function bfs(s,e){
    const q=[[s,[s]]];const vis=new Set([s]);
    while(q.length){
      const[node,path]=q.shift();
      for(const nb of(ROUTE_BORDERS[node]||[])){
        if(nb===e)return path.concat(nb);
        if(!vis.has(nb)){vis.add(nb);q.push([nb,path.concat(nb)]);}
      }
    }
    return null;
  }
  let start,target,path,tries=0;
  do{
    start=keys[~~(Math.random()*keys.length)];
    target=keys[~~(Math.random()*keys.length)];
    if(start===target){path=null;continue;}
    path=bfs(start,target);
    tries++;
  }while((!path||path.length<4||path.length>8)&&tries<120);
  if(!path||path.length<2){
    start="Germany";target="India";
    path=["Germany","Poland","Russia","China","India"];
  }
  S.routeData={start,target,route:[start],lives:3,solved:false,failed:false,
    score:0,steps:0,errMsg:"",minSteps:path.length-1};
  S.routeInput="";
  S.routeSugg=[];
}
function renderReiseroute(sc){
  const rd=S.routeData;
  if(!rd)return '<div class="scr"></div>';
  const hearts='\u2764\ufe0f'.repeat(rd.lives)+'\uD83D\uDDA4'.repeat(3-rd.lives);
  const routeHtml=rd.route.map((c,i)=>{
    const arr=i<rd.route.length-1?'<span class="rr-arrow">\u2192</span>':''
    return `<div class="rr-step">${flagOf(c)}<span class="rr-sn">${esc(c)}</span>${arr}</div>`;
  }).join("");
  const sugg=S.routeSugg||[];
  const suggHtml=sugg.slice(0,5).map(s=>`<div class="rr-sugg-item" data-name="${esc(s)}" onclick="handleRouteSubmit(this.dataset.name)">${flagOf(s)} ${esc(s)}</div>`).join("");
  const inputHtml=(!rd.solved&&!rd.failed)?`<div class="rr-inp-wrap">
    <div style="font-size:.75rem;color:var(--text3);margin-bottom:5px">Welches Land grenzt an <strong>${esc(rd.route[rd.route.length-1])}</strong>?</div>
    <div style="display:flex;gap:6px;align-items:stretch">
      <input type="text" id="rr-inp" placeholder="N\u00e4chstes Land\u2026" value="${esc(S.routeInput||'')}"
        oninput="S.routeInput=this.value;S.routeSugg=getRouteSugg(this.value);render()"
        onkeydown="if(event.key==='Enter')handleRouteSubmit(S.routeInput)"
        style="flex:1;min-width:0">
      <button class="btn-p" style="padding:.45rem 1rem;margin-bottom:0;width:auto;flex-shrink:0;min-width:2.6rem;font-size:1.1rem" onclick="handleRouteSubmit(S.routeInput)">\u2192</button>
    </div>
    <div class="rr-sugg">${suggHtml}</div>
    ${rd.errMsg?`<div style="color:#ef4444;font-size:.8rem;margin-top:4px">${esc(rd.errMsg)}</div>`:""}
  </div>`:"";
  const endHtml=(rd.solved||rd.failed)?`<div style="text-align:center;margin:.5rem 0">
    ${rd.solved
      ?'<div style="color:#10b981;font-weight:900;font-size:1.05rem">\u{1F389} Ziel erreicht!</div>'
      :'<div style="color:#ef4444;font-weight:900">\u{1F480} Keine Leben mehr!</div>'}
    <div style="color:var(--text3);font-size:.75rem;margin:.25rem 0">${rd.steps} Schritte (Min. ${rd.minSteps}) \u00b7 ${rd.score.toLocaleString()} Punkte</div>
  </div>
  <button class="btn-p" onclick="S.sc=S.routeData.score;S.correct=S.routeData.steps;S.rd=S.routeData.steps;finishCustomGame()">Ergebnis ansehen</button>`
  :"";
  return `<div class="scr">
    <div class="hud">
      <div style="display:flex;gap:8px;align-items:center">
        <div class="pill"><div class="hlbl">SCORE</div><div class="hval">${sc.toLocaleString()}</div></div>
        <div style="font-size:1rem;letter-spacing:1px">${hearts}</div>
      </div>
      <div style="display:flex;align-items:center;gap:8px">
        <div style="font-size:.75rem;color:var(--text3)">${rd.steps} Schr.</div>
        <div class="action-bar" style="display:flex;flex-direction:row-reverse;gap:10px;align-items:center"><button class="btn-exit-global" onclick="clr();S.ph='menu';S.tab='home';render()" style="background:#ef4444;color:#fff;border:none;padding:10px 20px;border-radius:8px;font-weight:700;cursor:pointer;white-space:nowrap">🚪 Beenden</button><button class="btn-bug" onclick="reportBug()" style="background:#e2e8f0;color:#475569;border:none;padding:10px 14px;border-radius:8px;font-weight:700;cursor:pointer">🐞 Fehler</button></div>
      </div>
    </div>
    <div style="background:var(--bg2);border-radius:12px;padding:.6rem .75rem;margin:.3rem 0">
      <div style="display:flex;justify-content:space-between;margin-bottom:.3rem">
        <span style="font-size:.65rem;font-weight:700;color:#10b981">START</span>
        <span style="font-size:.65rem;font-weight:700;color:#8b5cf6">ZIEL</span>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center">
        <div style="font-weight:900;color:var(--text)">${flagOf(rd.start)} ${esc(rd.start)}</div>
        <div style="color:var(--text3)">\u2192</div>
        <div style="font-weight:900;color:#8b5cf6">${flagOf(rd.target)} ${esc(rd.target)}</div>
      </div>
      <div style="font-size:.65rem;color:var(--text3);margin-top:.2rem">Mindestroute: ${rd.minSteps} Schritte</div>
    </div>
    <div style="background:var(--bg2);border-radius:12px;padding:.5rem .75rem;margin-bottom:.3rem;min-height:3rem">
      <div style="font-size:.65rem;color:var(--text3);margin-bottom:.3rem">Deine Route:</div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;align-items:center">${routeHtml}</div>
    </div>
    ${inputHtml}${endHtml}
    <div style="height:1.5rem"></div>
  </div>`;
}


/* â”€â”€ WAPPEN-MEISTER DATA â”€â”€ (Phase 106) */
const WAPPEN_DATA=PLACEHOLDER_WPJ
function genWappenQ(){
  if(\!WAPPEN_DATA||WAPPEN_DATA.length<4)return null;
  const _r=arr=>arr[~~(rng()*arr.length)];
  const correct=_r(WAPPEN_DATA.filter(w=>w.c\!==S.lid));
  const others=WAPPEN_DATA.filter(w=>w.cc\!==correct.cc);
  const wrongs=[];const used=new Set([correct.cc]);
  while(wrongs.length<3&&others.length>wrongs.length){const w=_r(others);if(\!used.has(w.cc)){used.add(w.cc);wrongs.push(w);}}
  if(wrongs.length<3)return null;
  /* P168: fall back to curated w.c when cc not in COUNTRIES */
  const _wdc=w=>{const r=displayCountry(w.cc);return(r&&r!==w.cc)?r:w.c;};
  const opts=[correct,...wrongs].sort(()=>rng()-.5).map(_wdc);
  return{type:"wappen",prompt:"Welchem Land gehört dieses Wappen?",subj:_wdc(correct),img:correct.img,opts,ans:displayCountry(correct.cc)||correct.c,lid:correct.cc,cc:correct.cc,meta:"🛡️ Wappen von "+correct.c};
}

/* P153: Fallback when Wappen SVG fails to load */
function wappenErr(img){
  img.style.display="none";
  const fb=document.createElement("div");
  fb.className="wappen-fallback";
  fb.textContent="🛡 Wappen nicht verfügbar";
  if(img.parentNode)img.parentNode.appendChild(fb);
}
/* â”€â”€ STADT-LAND-FLUSS (SLF) â”€â”€ (Phase 106) */
const SLF_LETTERS="ABCDEFGHIKLMNOPRSTW";
function initSLF(){
  clearInterval(tIv);
  const letter=SLF_LETTERS[~~(rng()*SLF_LETTERS.length)];
  S.slfData={letter,answers:{city:"",country:"",river:""},phase:"input",timeLeft:60};
  S.gameStartTime=Date.now();
  S.ph="playing";
  if(typeof tIv !== 'undefined') clearInterval(tIv); tIv=setInterval(()=>{
    if(\!S.slfData||S.slfData.phase\!=="input")return;
    S.slfData.timeLeft--;
    if(S.slfData.timeLeft<=0){clearInterval(tIv);handleSLFSubmit();}
    else{const _te=document.getElementById("slf-timer-val");if(_te)_te.textContent=S.slfData.timeLeft+"s";}
  },1000);
}
function handleSLFSubmit(){
  clearInterval(tIv);
  if(!S.slfData||S.slfData.phase!=="input")return;
  const{letter,answers}=S.slfData;
  const L=letter.toUpperCase();
  const norm=s=>(s||"").trim().toLowerCase();
  const startsOk=(s,L)=>!!s&&s.charAt(0).toUpperCase()===L;
  /* Stadt: match against CITIES dataset */
  const cityAns=norm(answers.city);
  /* City: accept any answer starting with correct letter (DB is English-only) */
  const cityValid=startsOk(cityAns,L)&&cityAns.length>=2;
  /* Land: match against COUNTRIES with localized names */
  const countryAns=norm(answers.country);
  const countryValid=startsOk(countryAns,L)&&COUNTRIES.some(c=>norm(c.c)===countryAns||norm(displayCountry(c.cc)||"")===countryAns);
  /* Fluss: match against RIVERS dataset */
  const riverAns=norm(answers.river);
  /* River: check DB (uses German labels) + fallback to first-letter-only */
  const riverDbMatch=(typeof RIVERS!=="undefined")&&RIVERS.some(r=>norm(r.riverLabel||r.name||"")===riverAns||norm(r.riverLabel||r.name||"").startsWith(riverAns));
  const riverValid=startsOk(riverAns,L)&&riverAns.length>=2&&(riverDbMatch||true);
  const pts=(cityValid?10:0)+(countryValid?10:0)+(riverValid?10:0);
  S.slfData={...S.slfData,results:{cityValid,countryValid,riverValid},phase:"result"};
  S.sc+=pts;
  S.correct+=(cityValid?1:0)+(countryValid?1:0)+(riverValid?1:0);
  if(window.mpGameCh)mpSend("score_update",{score:S.sc,rd:S.rd||0,correct:S.correct||0});
  render();
}
function handleLandHauptstadtSubmit(){
  clearInterval(tIv);
  if(!S.lhData||S.lhData.phase!=="input")return;
  const{letter,answers}=S.lhData;
  const L=letter.toUpperCase();
  const norm=s=>(s||"").trim().toLowerCase();
  const countryAns=norm(answers.country);
  const capitalAns=norm(answers.capital);
  const startsOk=(s,L)=>s&&s.charAt(0).toUpperCase()===L;
  const countryValid=startsOk(countryAns,L)&&COUNTRIES.some(c=>norm(c.c)===countryAns||norm(displayCountry(c.c))===countryAns);
  const capital=COUNTRIES.find(c=>(norm(c.c)===countryAns||norm(displayCountry(c.c))===countryAns));
  const capitalValid=startsOk(capitalAns,L)&&capital&&(norm(capital.cap)===capitalAns||norm(capital.capAscii||"")===capitalAns);
  const pts=(countryValid?10:0)+(capitalValid?10:0);
  S.lhData={...S.lhData,results:{countryValid,capitalValid},phase:"result"};
  S.sc+=pts;
  S.correct+=(countryValid?1:0)+(capitalValid?1:0);
  if(window.mpGameCh)mpSend("score_update",{score:S.sc,rd:S.rd||0,correct:S.correct||0});
  render();
}
function renderLandHauptstadt(sc){
  if(\!S.slfData)return'<div class="scr"></div>';
  const{letter,answers,phase,timeLeft}=S.slfData;
  const timerCol=timeLeft<=15?"#ef4444":timeLeft<=30?"#f59e0b":"#10b981";
  if(phase==="result"){
    const{cityValid,countryValid,riverValid}=S.slfData.results||{};
    const rowHtml=(label,val,valid)=>`<div class="slf-result-row"><span class="slf-result-label">${label}</span><span class="slf-result-val">${esc(val)||"–"}</span><span style="font-size:1rem">${valid?"✓":"❌"}</span></div>`;
    return`<div class="scr"><div class="panel">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.75rem">
        <div><div style="font-size:.6rem;letter-spacing:1px;color:var(--text3);font-weight:700">ERGEBNIS</div><div style="font-size:1.4rem;font-weight:900">📍 ${letter}</div></div>
        <div style="text-align:right"><div style="font-size:.6rem;color:var(--text3)">PUNKTE</div><div style="font-size:1.6rem;font-weight:900;color:#10b981">+${(cityValid?10:0)+(countryValid?10:0)+(riverValid?10:0)}</div></div>
      </div>
      ${rowHtml("Stadt",answers.city,cityValid)}
      ${rowHtml("Land",answers.country,countryValid)}
      ${rowHtml("Fluss",answers.river,riverValid)}
      <div style="margin-top:1rem;font-size:.72rem;color:var(--text3);text-align:center">Gesamt: ${sc.toLocaleString()} Punkte</div>
      <button class="btn-p" style="margin-top:.85rem" onclick="initSLF();render()">📍 Neue Runde</button>
      <button class="btn-g" style="margin-bottom:0" onclick="clr();S.ph='menu';S.tab='home';render()">Beenden</button>
    </div></div>`;
  }
  return`<div class="scr"><div class="panel">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem">
      <div><div style="font-size:.6rem;letter-spacing:1px;color:var(--text3);font-weight:700">BUCHSTABE</div><div style="font-size:2.6rem;font-weight:900;line-height:1">${letter}</div></div>
      <div style="text-align:right"><div style="font-size:.6rem;color:var(--text3)">ZEIT</div><div id="slf-timer-val" style="font-size:2rem;font-weight:900;color:${timerCol}">${timeLeft}s</div></div>
    </div>
    <div class="tbar" style="margin-bottom:1rem"><div class="tfill" style="width:${Math.round(timeLeft/60*100)}%;background:${timerCol}"></div></div>
    <div class="slf-field"><label class="slf-label">\u{1F3D9} STADT</label><input id="slf-city" type="text" dir="ltr" class="slf-input" style="direction:ltr;text-align:left;padding-left:10px" placeholder="Stadt mit ${letter}…" autocomplete="off" autocorrect="off" value="${esc(answers.city)}" oninput="S.slfData.answers.city=this.value" onkeydown="if(event.key==='Enter')document.getElementById('slf-country')?.focus()"></div>
    <div class="slf-field"><label class="slf-label">\u{1F30D} LAND</label><input id="slf-country" type="text" dir="ltr" class="slf-input" style="direction:ltr;text-align:left;padding-left:10px" placeholder="Land mit ${letter}…" autocomplete="off" autocorrect="off" value="${esc(answers.country)}" oninput="S.slfData.answers.country=this.value" onkeydown="if(event.key==='Enter')document.getElementById('slf-river')?.focus()"></div>
    <div class="slf-field"><label class="slf-label">\u{1F4A7} FLUSS</label><input id="slf-river" type="text" dir="ltr" class="slf-input" style="direction:ltr;text-align:left;padding-left:10px" placeholder="Fluss mit ${letter}…" autocomplete="off" autocorrect="off" value="${esc(answers.river)}" oninput="S.slfData.answers.river=this.value" onkeydown="if(event.key==='Enter')handleSLFSubmit()"></div>
    <button class="btn-p" style="margin-top:.85rem" onclick="handleSLFSubmit()">✓ Auswerten</button>
    <button class="btn-g" style="margin-bottom:0;font-size:.78rem" onclick="clr();S.ph='menu';S.tab='home';render()">✖ Schließen</button>
  </div></div>`;
}

/* â”€â”€ ACCOUNT LÖSCHEN (DSGVO) â”€â”€ (Phase 106) */
async function doDeleteAccount(){
  if(\!sbUser)return;
  const conf1=confirm("Konto wirklich löschen? Alle Daten gehen verloren.");
  if(\!conf1)return;
  const conf2=confirm("Diese Aktion ist NICHT rückgängig zu machen. Fortfahren?");
  if(\!conf2)return;
  try{
    await sb.from("profiles").delete().eq("id",sbUser.id);
    await sb.auth.signOut();
    showToast("\u{1F5D1}ï¸ Konto gelöscht");
    S.settingsModal=false;
    doLogout();
  }catch(e){showToast("âš ï¸ Fehler: "+e.message);}
}

/* â”€â”€ AD INTERSTITIAL â”€â”€ (Phase 107) */
function showAd(){if(!ENABLE_ADS||\!sbProfile?.is_premium)return; /* P151 */S.adModal=true;render();}
function closeAd(){S.adModal=false;render();}
function renderAdModal(){
  return`<div class="modal-overlay" onclick="closeAd()" style="z-index:500"><div class="modal-box" style="max-width:320px;padding:1.25rem">
    <div style="text-align:center;font-size:.6rem;color:var(--text3);letter-spacing:1.2px;margin-bottom:.6rem">ANZEIGE · UNTERSTßœTZT GEOQUEST</div>
    <div style="min-height:100px;background:var(--bg3);border-radius:12px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:var(--text3);border:1.5px dashed var(--border);margin-bottom:.85rem;padding:1rem">
      <div style="font-size:1.8rem;margin-bottom:.35rem">📢</div>
      <div style="font-size:.8rem;font-weight:700">Werbung</div>
      <div style="font-size:.68rem;margin-top:2px">Hier könnte deine Anzeige stehen</div>
    </div>
    <button class="btn-p" onclick="closeAd()">Weiter spielen →’</button>
    <button class="btn-g" style="margin-bottom:0;font-size:.76rem;color:#f59e0b;border-color:#f59e0b" onclick="S.payModal=true;closeAd()">👑 Werbung entfernen (Premium)</button>
  </div></div>`;
}

function renderLeagueEvalModal(ev){
  const{result,oldLeague,newLeague,rank,total,score}=ev;
  const isUp=result==="up",isDown=result==="down";
  const emoji=isUp?"\u{1F389}":isDown?"\u{1F4C9}":"\u{1F6E1}\uFE0F";
  const headline=isUp
    ?`Aufgestiegen\u2197\uFE0F`
    :isDown?`Abgestiegen\u2198\uFE0F`:"Klassenerhalt \u{1F91D}";
  const sub=isUp
    ?`Du hast die ${oldLeague.icon} ${oldLeague.id}-Liga verlassen.`
    :isDown?`Du steigst aus der ${oldLeague.icon} ${oldLeague.id}-Liga ab.`
    :`Du bleibst in der ${newLeague.icon} ${newLeague.id}-Liga.`;
  const rankTxt=total>0
    ?`Vorwoche: Platz ${rank} von ${total} \u00b7 ${score.toLocaleString()} Punkte`
    :`Keine Spiele letzte Woche.`;
  return`<div class="scr" style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;text-align:center;padding:2rem">
    <div style="font-size:3.5rem;margin-bottom:.5rem">${emoji}</div>
    <div style="font-size:1.4rem;font-weight:900;color:var(--text);margin-bottom:.35rem">${headline}</div>
    <div style="font-size:.88rem;color:var(--text2);margin-bottom:1.4rem">${sub}</div>
    <div style="background:${newLeague.bg};border:2px solid ${newLeague.color};border-radius:20px;padding:1.2rem 2.5rem;margin-bottom:1.4rem">
      <div style="font-size:2.6rem">${newLeague.icon}</div>
      <div style="font-size:1.3rem;font-weight:900;color:${newLeague.color}">${newLeague.id}-Liga</div>
    </div>
    <div style="font-size:.76rem;color:var(--text3);margin-bottom:1.5rem">${rankTxt}</div>
    <button class="btn-p" onclick="S.leagueEvalResult=null;render()">\u{1F680} Zur neuen Woche!</button>
  </div>`;
}


/* ─── STATS TAB ──────────────────────────────────────────────────── */
async function loadStatsData(){
  S.statsLoading=true;S.statsData=null;render();
  if(sbUser?.email&&sb){
    const{data}=await sb.from("game_sessions").select("*").eq("user_id",sbUser.id).order("created_at",{ascending:false}).limit(100);
    S.statsData=data||[];
  }else{
    try{S.statsData=JSON.parse(localStorage.getItem("gq_sessions_local")||"[]").reverse();}catch(e){S.statsData=[];}
  }
  S.statsLoading=false;render();
}
function _fmtDur(ms){
  if(!ms||ms<=0)return"–";
  const s=Math.round(ms/1000);
  if(s<60)return s+"s";
  return~~(s/60)+"m "+( s%60)+"s";
}
function _fmtDate(iso){
  if(!iso)return"–";
  const d=new Date(iso);
  return d.toLocaleDateString("de-DE",{day:"2-digit",month:"2-digit"})+" "+d.toLocaleTimeString("de-DE",{hour:"2-digit",minute:"2-digit"});
}
function renderStatsTab(){
  if(S.statsLoading)return`<div style="text-align:center;padding:3rem;color:var(--text3)">Lade Statistiken…</div>`;
  if(!S.statsData){
    /* trigger load, return spinner placeholder */
    setTimeout(loadStatsData,0);
    return`<div style="text-align:center;padding:3rem;color:var(--text3)">Lade…</div>`;
  }
  const rows=S.statsData;
  const totalGames=rows.length;
  const totalScore=rows.reduce((a,r)=>a+(r.score||0),0);
  const avgScore=totalGames?Math.round(totalScore/totalGames):0;
  const bestScore=totalGames?Math.max(...rows.map(r=>r.score||0)):0;
  const avgAcc=totalGames?Math.round(rows.reduce((a,r)=>a+(r.accuracy||0),0)/totalGames):0;
  const modeCount={};
  rows.forEach(r=>{modeCount[r.mode]=(modeCount[r.mode]||0)+1;});
  const favMode=Object.entries(modeCount).sort((a,b)=>b[1]-a[1])[0];
  const favM=favMode?MODES.find(m=>m.id===favMode[0]):null;
  const favLabel=favM?(favM.icon+" "+modeTitle(favM)):favMode?.[0]||"–";
  return`<div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.75rem">
      <div style="font-size:1.1rem;font-weight:900;color:var(--text)">\u{1F4CA} Deine Statistiken</div>
      <button onclick="S.statsData=null;render()" style="background:none;border:1.5px solid var(--border);border-radius:8px;padding:.25rem .6rem;font-size:.72rem;color:var(--text3);cursor:pointer">↺</button>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:.85rem">
      <div class="panel" style="text-align:center;padding:.75rem .5rem"><div style="font-size:1.6rem;font-weight:900;color:#34d399">${totalGames}</div><div style="font-size:.65rem;color:var(--text3)">Spiele gesamt</div></div>
      <div class="panel" style="text-align:center;padding:.75rem .5rem"><div style="font-size:1.6rem;font-weight:900;color:#fbbf24">${bestScore.toLocaleString()}</div><div style="font-size:.65rem;color:var(--text3)">Bester Score</div></div>
      <div class="panel" style="text-align:center;padding:.75rem .5rem"><div style="font-size:1.6rem;font-weight:900;color:#60a5fa">${avgScore.toLocaleString()}</div><div style="font-size:.65rem;color:var(--text3)">Ø Score</div></div>
      <div class="panel" style="text-align:center;padding:.75rem .5rem"><div style="font-size:1.6rem;font-weight:900;color:#a78bfa">${avgAcc}%</div><div style="font-size:.65rem;color:var(--text3)">Ø Genauigkeit</div></div>
    </div>
    ${favMode?`<div class="panel" style="display:flex;align-items:center;gap:10px;margin-bottom:.85rem;padding:.65rem .85rem"><div style="font-size:1.4rem">${favM?.icon||"\u{1F3AE}"}</div><div><div style="font-size:.65rem;color:var(--text3)">LIEBLINGS-MODUS</div><div style="font-weight:700;color:var(--text)">${favLabel}</div><div style="font-size:.68rem;color:var(--text3)">${favMode[1]}× gespielt</div></div></div>`:""}
    ${!rows.length?`<div class="panel" style="text-align:center;padding:2rem;color:var(--text3)">Noch keine Spiele aufgezeichnet.\nSpiele eine Runde!</div>`:
    `<div style="font-size:.72rem;font-weight:700;color:var(--text3);letter-spacing:.5px;margin-bottom:.4rem">LETZTE SPIELE</div>
    <div style="display:flex;flex-direction:column;gap:5px">
    ${rows.slice(0,30).map(r=>{
      const m=MODES.find(x=>x.id===r.mode);
      const icon=m?.icon||"\u{1F3AE}";
      const label=m?modeTitle(m).slice(0,14):r.mode;
      const acc=r.accuracy!=null?r.accuracy+"%":"–";
      const dur=_fmtDur(r.duration_ms);
      const dt=_fmtDate(r.created_at||r.date);
      return`<div class="panel" style="display:flex;align-items:center;gap:8px;padding:.55rem .75rem">
        <span style="font-size:1.3rem;min-width:1.5rem">${icon}</span>
        <div style="flex:1;min-width:0">
          <div style="font-size:.8rem;font-weight:700;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${label}</div>
          <div style="font-size:.65rem;color:var(--text3)">${dt}</div>
        </div>
        <div style="text-align:right;flex-shrink:0">
          <div style="font-weight:900;color:#fbbf24;font-size:.9rem">${(r.score||0).toLocaleString()}</div>
          <div style="font-size:.62rem;color:var(--text3)">${acc} · ${dur}</div>
        </div>
      </div>`;
    }).join("")}
    </div>`}
    ${!sbUser?.email?`<div style="font-size:.72rem;color:var(--text3);text-align:center;margin-top:.85rem">\u{1F4BE} Lokal gespeichert (letzte 50 Spiele). <span style="color:#60a5fa;cursor:pointer" onclick="S.tab='profil';S.authMode='register';render()">Account erstellen</span> um alles zu sichern.</div>`:""}
  </div>`;
}

/* ─── ADMIN TAB ──────────────────────────────────────────────────── */
/* Phase 167B: Global Bug Reporter */
async function reportBug(){
  const msg=window.prompt("\u{1F41E} Was stimmt nicht? (Modus, Frage, Fehler beschreiben)");
  if(msg===null||!msg.trim())return;
  showToast("\u{1F4E4} Sende Fehlermeldung\u2026");
  const ctx={mode:S.mode||"unknown",diff:S.diff,rd:S.rd,ph:S.ph,
    q:S.q?{type:S.q.type,prompt:(S.q.prompt||"").slice(0,200),subj:String(S.q.subj||"").slice(0,100),ans:S.q.ans}:null};
  if(sb){
    try{
      await sb.from("bug_reports").insert({user_id:sbUser?.id||null,mode:S.mode||"unknown",context:JSON.stringify(ctx),message:msg.trim()});
      showToast("\u2705 Danke! Fehler wurde gemeldet.");
    }catch(e){
      _sendBugMail("GeoQuest Bug: "+(S.mode||"?"),msg+"\n\nKontext: "+JSON.stringify(ctx));
      showToast("\u{1F4E7} Per E-Mail gesendet (DB nicht erreichbar).");
    }
  }else{
    _sendBugMail("GeoQuest Bug: "+(S.mode||"?"),msg+"\n\nKontext: "+JSON.stringify(ctx));
    showToast("\u{1F4E7} Per E-Mail gesendet.");
  }
}
async function loadAdminData(){
  if(sbUser?.email!=="andre69190@gmail.com")return;
  S.adminLoading=true;S.adminData=null;render();
  const{data}=await sb.from("game_sessions").select("*").order("created_at",{ascending:false}).limit(2000);
  S.adminData=data||[];
  S.adminLoading=false;render();
}
function renderAdminTab(){
  if(sbUser?.email!=="andre69190@gmail.com")return`<div style="text-align:center;padding:3rem;color:#f87171">⛔ Kein Zugang.</div>`;
  if(S.adminLoading)return`<div style="text-align:center;padding:3rem;color:var(--text3)">Lade Admin-Daten…</div>`;
  if(!S.adminData){setTimeout(loadAdminData,0);return`<div style="text-align:center;padding:3rem;color:var(--text3)">Lade…</div>`;}
  const rows=S.adminData;
  const now=new Date();
  const today=now.toISOString().slice(0,10);
  const d7=new Date(now);d7.setDate(d7.getDate()-6);const d7str=d7.toISOString().slice(0,10);
  const todayRows=rows.filter(r=>(r.created_at||"").startsWith(today));
  const week7Rows=rows.filter(r=>(r.created_at||"").slice(0,10)>=d7str);
  const uidsAll=new Set(rows.map(r=>r.user_id||r.username).filter(Boolean));
  const uidsToday=new Set(todayRows.map(r=>r.user_id||r.username).filter(Boolean));
  const uids7d=new Set(week7Rows.map(r=>r.user_id||r.username).filter(Boolean));
  const modeCount={};rows.forEach(r=>{modeCount[r.mode]=(modeCount[r.mode]||0)+1;});
  const allModes=Object.entries(modeCount).sort((a,b)=>b[1]-a[1]);
  const totalScore=rows.reduce((a,r)=>a+(r.score||0),0);
  const avgScore=rows.length?Math.round(totalScore/rows.length):0;
  const devCount={mobile:0,desktop:0,unknown:0};
  rows.forEach(r=>{const d=(r.device_type||"").toLowerCase();
    if(d==="mobile")devCount.mobile++;else if(d==="desktop")devCount.desktop++;else devCount.unknown++;});
  const devTotal=rows.length||1;
  const mPct=Math.round(devCount.mobile/devTotal*100);
  const dPct=Math.round(devCount.desktop/devTotal*100);
  const uPct=100-mPct-dPct;
  const hourCount=Array(24).fill(0);
  rows.forEach(r=>{if(r.created_at){const h=new Date(r.created_at).getHours();if(h>=0&&h<24)hourCount[h]++;}});
  const maxHour=Math.max(1,...hourCount);
  const dayCounts={};
  for(let i=6;i>=0;i--){const d=new Date();d.setDate(d.getDate()-i);const k=d.toISOString().slice(0,10);dayCounts[k]=0;}
  rows.forEach(r=>{const k=(r.created_at||"").slice(0,10);if(dayCounts[k]!==undefined)dayCounts[k]++;});
  const maxDay=Math.max(1,...Object.values(dayCounts));
  const dayBarsArr=Object.entries(dayCounts);
  const maxDayVal=Math.max(...dayBarsArr.map(([,n])=>n));
  const dayBars=dayBarsArr.map(([d,n])=>{
    const pct=Math.round(n/maxDay*100);
    const label=new Date(d).toLocaleDateString("de-DE",{weekday:"short",day:"2-digit"});
    return`<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px">
      <div style="font-size:.6rem;color:${n===maxDayVal?"#34d399":"var(--text3)"};font-weight:700">${n}</div>
      <div style="width:100%;background:var(--bg3);border-radius:4px;height:50px;display:flex;align-items:flex-end">
        <div style="width:100%;height:${pct}%;background:#10b981;border-radius:4px;min-height:2px"></div>
      </div>
      <div style="font-size:.55rem;color:var(--text3);text-align:center">${label}</div>
    </div>`;
  }).join("");
  const hourBars=hourCount.map((n,h)=>{
    const pct=Math.round(n/maxHour*100);
    const isNight=h<6||h>=22;const isPeak=n===maxHour&&n>0;
    return`<div style="flex:1;display:flex;flex-direction:column;align-items:center" title="${h}:00 — ${n}">
      <div style="width:100%;background:var(--bg3);border-radius:3px;height:40px;display:flex;align-items:flex-end">
        <div style="width:100%;height:${pct}%;background:${isPeak?"#f59e0b":isNight?"#6366f1":"#60a5fa"};border-radius:3px;min-height:${n?2:0}px"></div>
      </div>
      ${h%4===0?`<div style="font-size:.45rem;color:var(--text3)">${h}h</div>`:"<div style='height:.6rem'></div>"}
    </div>`;
  }).join("");
  const adminColors=["#10b981","#60a5fa","#f59e0b","#a78bfa","#f87171","#34d399","#38bdf8","#fb923c","#c084fc","#f43f5e"];
  const modeRows=allModes.map(([mid,cnt],i)=>{
    const m=MODES.find(x=>x.id===mid);
    const pct=Math.round(cnt/rows.length*100);
    const col=adminColors[i%adminColors.length];
    return`<div style="display:flex;align-items:center;gap:8px;margin-bottom:.38rem">
      <span style="min-width:1.1rem;text-align:center;font-size:.82rem">${m?.icon||"\u{1F3AE}"}</span>
      <div style="flex:1;min-width:0">
        <div style="display:flex;justify-content:space-between;font-size:.67rem;color:var(--text);margin-bottom:1px">
          <span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:130px">${m?modeTitle(m):mid}</span>
          <span style="color:var(--text3);flex-shrink:0;margin-left:4px">${cnt} (${pct}%)</span>
        </div>
        <div style="background:var(--bg3);border-radius:3px;height:5px"><div style="background:${col};border-radius:3px;height:5px;width:${pct}%"></div></div>
      </div>
    </div>`;
  }).join("");
  return`<div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.75rem">
      <div style="font-size:1.1rem;font-weight:900;color:var(--text)">\u{1F6E1}️ Admin-Dashboard</div>
      <button onclick="S.adminData=null;render()" style="background:none;border:1.5px solid var(--border);border-radius:8px;padding:.25rem .6rem;font-size:.72rem;color:var(--text3);cursor:pointer">↺</button>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:.85rem">
      <div class="panel" style="text-align:center;padding:.65rem .4rem"><div style="font-size:1.5rem;font-weight:900;color:#34d399">${rows.length.toLocaleString()}</div><div style="font-size:.6rem;color:var(--text3)">Sessions gesamt</div></div>
      <div class="panel" style="text-align:center;padding:.65rem .4rem"><div style="font-size:1.5rem;font-weight:900;color:#f59e0b">${todayRows.length}</div><div style="font-size:.6rem;color:var(--text3)">Sessions heute</div></div>
      <div class="panel" style="text-align:center;padding:.65rem .4rem"><div style="font-size:1.3rem;font-weight:900;color:#60a5fa">${uids7d.size}</div><div style="font-size:.6rem;color:var(--text3)">Unique (7 Tage)</div></div>
      <div class="panel" style="text-align:center;padding:.65rem .4rem"><div style="font-size:1.3rem;font-weight:900;color:#a78bfa">${uidsToday.size}</div><div style="font-size:.6rem;color:var(--text3)">Unique (heute)</div></div>
      <div class="panel" style="text-align:center;padding:.65rem .4rem"><div style="font-size:1.3rem;font-weight:900;color:#fb923c">${uidsAll.size}</div><div style="font-size:.6rem;color:var(--text3)">Unique (gesamt)</div></div>
      <div class="panel" style="text-align:center;padding:.65rem .4rem"><div style="font-size:1.3rem;font-weight:900;color:#f43f5e">${avgScore.toLocaleString()}</div><div style="font-size:.6rem;color:var(--text3)">Ø Score</div></div>
    </div>
    <div class="panel" style="margin-bottom:.85rem;padding:.85rem">
      <div style="font-size:.7rem;font-weight:700;color:var(--text3);letter-spacing:.5px;margin-bottom:.65rem">SPIELE PRO TAG (7 TAGE)</div>
      <div style="display:flex;gap:4px;align-items:flex-end;height:80px">${dayBars}</div>
    </div>
    <div class="panel" style="margin-bottom:.85rem;padding:.85rem">
      <div style="font-size:.7rem;font-weight:700;color:var(--text3);letter-spacing:.5px;margin-bottom:.65rem">AKTIVITÄT PRO STUNDE (0-23h)</div>
      <div style="display:flex;gap:2px;align-items:flex-end;height:52px">${hourBars}</div>
      <div style="font-size:.5rem;color:var(--text3);margin-top:4px">&#x1F4A4; Nacht · &#x1F535; Tag · &#x1F7E1; Peak</div>
    </div>
    <div class="panel" style="margin-bottom:.85rem;padding:.85rem">
      <div style="font-size:.7rem;font-weight:700;color:var(--text3);letter-spacing:.5px;margin-bottom:.65rem">GERÄTE</div>
      <div style="display:flex;flex-direction:column;gap:6px">
        <div style="display:flex;align-items:center;gap:8px">
          <span style="font-size:.8rem;min-width:1.4rem">📱</span>
          <div style="flex:1;background:var(--bg3);border-radius:4px;height:10px"><div style="background:#60a5fa;border-radius:4px;height:10px;width:${mPct}%"></div></div>
          <span style="font-size:.65rem;color:var(--text3);min-width:3rem">${devCount.mobile} (${mPct}%)</span>
        </div>
        <div style="display:flex;align-items:center;gap:8px">
          <span style="font-size:.8rem;min-width:1.4rem">💻</span>
          <div style="flex:1;background:var(--bg3);border-radius:4px;height:10px"><div style="background:#34d399;border-radius:4px;height:10px;width:${dPct}%"></div></div>
          <span style="font-size:.65rem;color:var(--text3);min-width:3rem">${devCount.desktop} (${dPct}%)</span>
        </div>
        ${uPct>0?`<div style="display:flex;align-items:center;gap:8px">
          <span style="font-size:.8rem;min-width:1.4rem">❓</span>
          <div style="flex:1;background:var(--bg3);border-radius:4px;height:10px"><div style="background:#6b7280;border-radius:4px;height:10px;width:${uPct}%"></div></div>
          <span style="font-size:.65rem;color:var(--text3);min-width:3rem">${devCount.unknown} (${uPct}%)</span>
        </div>`:""}
      </div>
    </div>
    <div class="panel" style="margin-bottom:.85rem;padding:.85rem">
      <div style="font-size:.7rem;font-weight:700;color:var(--text3);letter-spacing:.5px;margin-bottom:.65rem">ALLE MODI (${allModes.length})</div>
      <div style="max-height:260px;overflow-y:auto;padding-right:2px">${modeRows}</div>
    </div>
    <div style="font-size:.65rem;color:var(--text3);text-align:center">Letzte 2000 Sessions · Nur sichtbar für dich</div>
  </div>`;
}

function filterGames(){
  var input=document.getElementById('gameSearch');
  var q=input?input.value.toLowerCase().trim():'';
  if(!q){
    filterByCategory((typeof S!=='undefined'&&S.filterCat)||'pure_geo');
    return;
  }
  var catLabels={pure_geo:'pure geo',lifestyle:'lifestyle',eu_plates:'kennzeichen plates',
    sport:'sport',hl_compare:'higher lower',comparisons:'vergleiche',
    airports:'airports flughaefen',neighbors:'nachbarlaender',map_mode:'weltkarte map'};
  // Search: show all sections, auto-expand those with matches
  document.querySelectorAll('.accordion-section').forEach(function(section){
    section.style.removeProperty('display');
    var content=section.querySelector('.accordion-content');
    var arrow=section.querySelector('.acc-arrow');
    var hasMatch=false;
    section.querySelectorAll('.mode-card').forEach(function(card){
      var title=(card.dataset.title||'').toLowerCase();
      var desc=(card.dataset.desc||'').toLowerCase();
      var cat=(card.dataset.category||'').toLowerCase();
      var catLabel=(catLabels[card.dataset.category]||'');
      var match=(title+' '+desc+' '+cat+' '+catLabel).includes(q);
      if(match){card.style.removeProperty('display');hasMatch=true;}
      else{card.style.setProperty('display','none','important');}
    });
    if(hasMatch){
      if(content){content.classList.add('open');}
      if(arrow){arrow.style.transform='rotate(180deg)';}
    } else {
      section.style.setProperty('display','none','important');
    }
  });
}
window.filterGames=filterGames;
function filterByCategory(cat){
  if(typeof S!=='undefined')S.filterCat=cat;
  document.querySelectorAll('.accordion-section').forEach(function(section){
    var sectionCat=section.dataset.cat;
    var content=section.querySelector('.accordion-content');
    var arrow=section.querySelector('.acc-arrow');
    // All section HEADERS always visible — accordion IS the navigation
    section.style.removeProperty('display');
    // Reset all cards visible
    section.querySelectorAll('.mode-card').forEach(function(c){c.style.removeProperty('display');});
    if(cat==='all'||sectionCat===cat){
      // Expand this section
      if(content){
        var gc=(typeof S!=='undefined'&&S.gridCols)||(parseInt(localStorage.getItem('geoquest_grid_cols'))||4);
        content.style.cssText='display:grid;grid-template-columns:repeat('+gc+',1fr);gap:15px;padding:10px 0 15px 0;width:100%;box-sizing:border-box';
        content.classList.add('open');
      }
      if(arrow){arrow.style.transform='rotate(180deg)';}
    } else {
      // Collapse content — but keep header visible
      if(content){content.classList.remove('open');content.style.display='none';}
      if(arrow){arrow.style.transform='rotate(0deg)';}
    }
  });
  var gs=document.getElementById('gameSearch');
  if(gs)gs.value='';
}
window.filterByCategory=filterByCategory;
window.toggleAccordion=function(header,catId){
  var content=header.nextElementSibling;
  var arrow=header.querySelector('.acc-arrow');
  var isOpen=content.classList.contains('open');
  if(isOpen){
    content.classList.remove('open');
    content.style.display='none';
    if(arrow)arrow.style.transform='rotate(0deg)';
  } else {
    var gc=(typeof S!=='undefined'&&S.gridCols)||(parseInt(localStorage.getItem('geoquest_grid_cols'))||4);
    content.style.cssText='display:grid;grid-template-columns:repeat('+gc+',1fr);gap:15px;padding:10px 0 15px 0;width:100%;box-sizing:border-box';
    content.classList.add('open');
    if(arrow)arrow.style.transform='rotate(180deg)';
  }
};

// Apply default filter on DOMContentLoaded
document.addEventListener('DOMContentLoaded',function(){
  setTimeout(function(){
    window.filterByCategory((typeof S!=='undefined'&&S.filterCat)||'pure_geo');
  },200);
});
function toggleFavorite(modeId,ev){
  if(ev){ev.preventDefault();ev.stopPropagation();}
  var favs=JSON.parse(localStorage.getItem('geoquest_favorites')||'[]');
  var idx=favs.indexOf(modeId);
  if(idx>=0){favs.splice(idx,1);}else{favs.push(modeId);}
  localStorage.setItem('geoquest_favorites',JSON.stringify(favs));
  // Update button opacity without re-render
  document.querySelectorAll('[data-fav-id="'+modeId+'"]').forEach(function(btn){
    btn.style.opacity=favs.includes(modeId)?'1':'.35';
  });
}
window.toggleFavorite=toggleFavorite;
function showFavorites(){
  var favs=JSON.parse(localStorage.getItem('geoquest_favorites')||'[]');
  if(!favs.length){
    // Toast: keine Favoriten
    var t=document.createElement('div');
    t.textContent=t('fav_empty')||'No favourites yet';
    t.style.cssText='position:fixed;bottom:90px;left:50%;transform:translateX(-50%);background:#1e293b;color:#fff;padding:10px 18px;border-radius:20px;font-size:.82rem;font-weight:600;z-index:99999;pointer-events:none';
    document.body.appendChild(t);
    setTimeout(function(){t.remove();},2500);
    return;
  }
  document.querySelectorAll('.accordion-section').forEach(function(section){
    section.style.removeProperty('display');
    var content=section.querySelector('.accordion-content');
    var arrow=section.querySelector('.acc-arrow');
    var hasMatch=false;
    section.querySelectorAll('.mode-card').forEach(function(card){
      if(favs.includes(card.dataset.modeId)){
        card.style.removeProperty('display');
        hasMatch=true;
      } else {
        card.style.setProperty('display','none','important');
      }
    });
    if(hasMatch){
      if(content){
        var gc=(typeof S!=='undefined'&&S.gridCols)||(parseInt(localStorage.getItem('geoquest_grid_cols'))||4);
        content.style.cssText='display:grid;grid-template-columns:repeat('+gc+',1fr);gap:15px;padding:10px 0 15px 0;width:100%;box-sizing:border-box';
        content.classList.add('open');
      }
      if(arrow){arrow.style.transform='rotate(180deg)';}
    } else {
      section.style.setProperty('display','none','important');
    }
  });
}
window.showFavorites=showFavorites;
function playRandomGame(){
  const pool=MODES.filter(m=>!m.comingSoon);
  if(!pool.length)return;
  const m=pool[~~(Math.random()*pool.length)];
  startGame(m.id);
}
window.showGameInfo = function(modeId, ev) {
  if (ev) { ev.preventDefault(); ev.stopPropagation(); }
  var m = (typeof MODES !== 'undefined' ? MODES : []).find(function(x) { return x.id === modeId; });
  if (!m) return;
  var existingModal = document.getElementById('game-info-modal');
  if (existingModal) existingModal.remove();
  var overlay = document.createElement('div');
  overlay.id = 'game-info-modal';
  overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.75);z-index:999999;display:flex;justify-content:center;align-items:center;';
  overlay.onclick = function() { overlay.remove(); };
  var box = document.createElement('div');
  box.style.cssText = 'background:var(--bg,#fff);padding:24px;border-radius:16px;max-width:380px;width:90%;max-height:80vh;overflow-y:auto;text-align:center;box-shadow:0 10px 30px rgba(0,0,0,0.4);';
  box.onclick = function(e) { e.stopPropagation(); };
  var iconEl = document.createElement('div');
  iconEl.style.cssText = 'font-size:2.8rem;margin-bottom:.4rem';
  iconEl.textContent = m.icon || '';
  var titleEl = document.createElement('div');
  titleEl.style.cssText = 'font-size:1.05rem;font-weight:900;color:var(--text,#0f172a);margin-bottom:.6rem;line-height:1.3';
  titleEl.textContent = (typeof modeTitle === 'function' ? modeTitle(m) : m.title) || modeId;
  var descEl = document.createElement('div');
  descEl.style.cssText = 'font-size:.82rem;color:var(--text2,#475569);line-height:1.55;margin-bottom:1.1rem;text-align:left';
  descEl.textContent = m.desc || 'Kein Beschreibungstext vorhanden.';
  var btnRow = document.createElement('div');
  btnRow.style.cssText = 'display:flex;gap:8px;';
  var playBtn = document.createElement('button');
  playBtn.className = 'btn-p';
  playBtn.style.cssText = 'flex:1;margin-bottom:0';
  playBtn.textContent = '► Spielen';
  playBtn.onclick = function() { overlay.remove(); if (typeof startGame === 'function') startGame(modeId); };
  var closeBtn = document.createElement('button');
  closeBtn.style.cssText = 'flex:1;background:var(--bg2,#f1f5f9);color:var(--text,#0f172a);border:2px solid var(--border,#e2e8f0);border-radius:10px;padding:.5rem;font-size:.85rem;font-weight:700;cursor:pointer';
  closeBtn.textContent = '✕';
  closeBtn.onclick = function() { overlay.remove(); };
  btnRow.appendChild(playBtn);
  btnRow.appendChild(closeBtn);
  box.appendChild(iconEl);
  box.appendChild(titleEl);
  box.appendChild(descEl);
  box.appendChild(btnRow);
  overlay.appendChild(box);
  document.body.appendChild(overlay);
};
function showGameInfo(modeId, ev) { window.showGameInfo(modeId, ev); }
function closeGameInfo(){
  const el=document.getElementById('game-info-modal');
  if(el)el.remove();
}
function renderHomeTab(){
  console.log("[GQ] renderHomeTab() filterCat=",S.filterCat);
  const _CAT_ORDER=["pure_geo","lifestyle","eu_plates","sport","hl_compare","comparisons","airports","neighbors","map_mode"];

  // Build accordion sections — Pure Geo auto-open, others closed
  const _favs=JSON.parse(localStorage.getItem('geoquest_favorites')||'[]');
  const _accordionHTML=_CAT_ORDER.map(catId=>{
    const cat=MODE_CATS[catId];if(!cat)return'';
    const unlocked=isCategoryUnlocked(catId);
    const isDefault=catId===(S.filterCat||'pure_geo');
    const catModes=MODES.filter(m=>cat.modes.includes(m.id)&&!m.comingSoon);
    const cards=catModes.map(m=>{
      const cs=m.comingSoon===true;
      const active=S.mode===m.id&&!cs;
      const isLocked=!unlocked&&!cs;
      const cardCls='mode-card'+(active?' active':'')+(cs?' coming-soon-card':'')+(isLocked?' locked-card':'');
      const clickAct=cs?"showComingSoonToast('"+m.title+"')":unlocked?"startGame('"+m.id+"')":"S.lockModal='"+catId+"';render()";
      const isFav=_favs.includes(m.id);
      return`<div class="${cardCls}" onclick="${clickAct}" role="button" data-title="${modeTitle(m)}" data-desc="${(m.desc||'')+' '+m.id}" data-category="${catId}" data-mode-id="${m.id}">
        ${cs?`<span class="cs-badge">Bald</span>`:""}
        ${isLocked?`<span style="position:absolute;top:4px;right:4px;font-size:.75rem">\u{1F512}</span>`:""}
        <span class="mode-icon">${m.icon}</span><div class="mode-title">${modeTitle(m)}</div>
        ${!cs&&unlocked?`<button type="button" class="fav-btn" data-fav-id="${m.id}" onclick="event.preventDefault();event.stopPropagation();window.toggleFavorite('${m.id}',event);" onpointerdown="event.stopPropagation();" ontouchstart="event.stopPropagation();" style="position:absolute;bottom:6px;left:6px;z-index:99999;width:22px;height:22px;background:transparent;border:none;font-size:.7rem;cursor:pointer;line-height:1;padding:0;opacity:${isFav?'1':'.35'}">❤️</button>`:""}
        ${!cs&&unlocked?`<button type="button" class="info-btn-fix" onclick="event.preventDefault();event.stopPropagation();window.showGameInfo('${m.id}',event);" onpointerdown="event.stopPropagation();" ontouchstart="event.stopPropagation();" style="position:absolute;bottom:6px;right:6px;z-index:99999;width:22px;height:22px;background:#3b82f6;color:#fff;border:none;border-radius:6px;font-size:.72rem;font-weight:900;cursor:pointer;line-height:1;padding:0">i</button>`:""}
      </div>`;
    }).join('');
    const albumCard=catId==='eu_plates'?`<div class="mode-card" data-category="eu_plates" onclick="S.tab='album';render()" role="button" data-title="Kennzeichen-Album" style="background:linear-gradient(135deg,#1d4ed8,#3b82f6);border-color:#3b82f6">
        <span class="mode-icon">\u{1F4D4}</span>
        <div class="mode-title" style="color:#fff">Album</div>
        <div class="mode-desc" style="color:rgba(255,255,255,.8)">${S.collectedPlates.length} ges.</div>
      </div>`:'';
    const lockPill=!unlocked?`<span style="font-size:.65rem;background:#fef3c7;color:#92400e;padding:2px 6px;border-radius:10px;margin-left:4px">\u{1F512} ${cat.cost?cat.cost.toLocaleString():'?'} Coins</span>`:'';
    return`<div class="accordion-section" data-cat="${catId}">
      <div class="accordion-header" onclick="window.toggleAccordion(this,'${catId}')" style="display:flex;justify-content:space-between;align-items:center;padding:12px 15px;background:var(--bg2);border-radius:10px;cursor:pointer;font-weight:700;font-size:.9rem;border:1px solid var(--border);user-select:none">
        <span style="display:flex;align-items:center;gap:8px">${cat.icon} ${cat.label}${lockPill}</span>
        <span class="acc-arrow" style="transition:transform .2s;display:inline-block;transform:${isDefault?'rotate(180deg)':'rotate(0deg)'}">▼</span>
      </div>
      <div class="accordion-content${isDefault?' open':''}">
        ${cards}${albumCard}
      </div>
    </div>`;
  }).join('');

  /* Dynamic Home Header */
  const _li=sbUser&&sbProfile?.username;
  const _un=sbProfile?.username||(sbUser?.email?.split('@')[0]||'Gast');
  const _gc=(sbProfile?.geo_coins||0).toLocaleString();
  const _hdr=_li
    ?`<div style="display:flex;align-items:center;justify-content:space-between;padding:.85rem 1rem .6rem;margin-bottom:.1rem">
        <div style="font-size:1.05rem;font-weight:700;color:var(--text)">${t("home_hi",{name:_un})}</div>
        <div style="display:flex;align-items:center;gap:5px;background:var(--bg2);border-radius:20px;padding:.28rem .75rem;font-size:.82rem;font-weight:700;color:#f59e0b;border:1px solid rgba(245,158,11,.25)">\u{1FA99} ${_gc}</div>
      </div>`
    :`<div style="display:flex;align-items:center;justify-content:space-between;padding:.85rem 1rem .6rem;margin-bottom:.1rem">
        <div style="font-size:1.05rem;font-weight:700;color:var(--text)">${t("home_guest")}</div>
        <button onclick="S.tab='profil';render()" style="background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;border:none;border-radius:20px;padding:.3rem .8rem;font-size:.72rem;font-weight:700;cursor:pointer;white-space:nowrap;box-shadow:0 2px 8px rgba(99,102,241,.35)">${t("home_save")}</button>
      </div>`;
  const _homeHTML=`${_hdr}${renderDailyHero()}
    <div class="pvp-hero" onclick="S.mpModal=true;render()" role="button" aria-label="Live 1vs1 starten">
      <div style="display:flex;align-items:center;gap:14px">
        <div style="font-size:2.2rem">⚔️</div>
        <div>
          <div style="font-size:1rem;font-weight:900;color:#fff">Live 1vs1 Duell</div>
          <div style="font-size:.74rem;color:rgba(255,255,255,.75);margin-top:2px">${t("home_pvp_sub")}</div>
        </div>
        <div style="margin-left:auto;background:#7c3aed;color:#fff;border-radius:20px;padding:.3rem .85rem;font-size:.76rem;font-weight:700">► Spielen</div>
      </div>
    </div>
    <div style="background:linear-gradient(135deg,#4f46e5,#7c3aed);border-radius:14px;padding:.7rem 1rem;margin-bottom:.55rem;cursor:pointer;display:flex;align-items:center;gap:12px;box-shadow:0 2px 10px rgba(99,102,241,.25)" onclick="S.lvModal=true;S.lv=null;render()" role="button">
      <div style="font-size:2rem">⚔️</div>
      <div style="flex:1"><div style="font-size:.9rem;font-weight:900;color:#fff">Lokal 1:1 Hot-Seat</div><div style="font-size:.7rem;color:rgba(255,255,255,.75)">Zwei Spieler · Ein Gerät · 10 Runden</div></div>
      <div style="background:rgba(255,255,255,.2);color:#fff;border-radius:20px;padding:.25rem .75rem;font-size:.72rem;font-weight:700">► Los</div>
    </div>
    <div class="menu-search-container" style="display:flex;gap:8px;margin:15px 15px 12px;align-items:center;flex-wrap:nowrap">
      <input type="text" id="gameSearch" placeholder="🔍 Spiel suchen..." oninput="window.filterGames()" style="flex:1;padding:12px;border:2px solid #cbd5e1;border-radius:10px;font-size:16px;outline:none;min-width:0">
      <button onclick="window.showFavorites()" style="background:var(--bg2);color:#ef4444;border:2px solid var(--border);padding:8px 11px;border-radius:10px;font-size:1rem;cursor:pointer;flex-shrink:0;line-height:1" title="Favoriten">❤️</button>
      <button onclick="playRandomGame()" style="background:#4f46e5;color:#fff;border:none;padding:12px 18px;border-radius:10px;font-weight:700;cursor:pointer;white-space:nowrap;flex-shrink:0">🎲 Zufall</button>
    </div>
    <div id="mainGamesGrid" style="padding:0 15px">${_accordionHTML}</div>
    <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px"><span style="font-size:.65rem;color:var(--text3);font-weight:700;letter-spacing:.8px">SCHWIERIGKEIT</span><span title="Casual: Entspannt, kein Zeitlimit, unendlich Leben&#10;Hardcore: Kein Zeitlimit, 3 Leben (Game Over nach 3 Fehlern)&#10;Survival: 8 Sek. pro Frage, 3 Leben" style="font-size:.72rem;cursor:help;color:var(--text3)">ℹ️</span></div>
    <div class="diff-toggle">
      <button class="diff-btn ${S.diff==="casual"?"active":""}" onclick="S.diff='casual';render()">Casual</button>
      <button class="diff-btn ${S.diff==="hardcore"?"active":""}" onclick="S.diff='hardcore';render()">Hardcore</button>
      <button class="diff-btn ${S.diff==="survival"?"active":""}" onclick="S.diff='survival';render()">💀 Survival</button>
    </div>
    <p style="text-align:center;color:var(--text2);font-size:.72rem;font-weight:600;margin:.3rem 0 .5rem">${
      t(S.diff==="casual"?"diff_desc_casual":S.diff==="hardcore"?"diff_desc_hc":"diff_desc_surv")
    }</p>
    <div style="margin:.6rem 0 .5rem;text-align:center"><button onclick="reportBug()" style="background:transparent;color:var(--text3);border:none;font-size:.72rem;cursor:pointer;text-decoration:underline;padding:.3rem .5rem">🐞 Fehler melden</button></div>
    <div style="height:5rem"></div>`;
  console.log("[GQ] renderHomeTab() returning length:",_homeHTML.length);
  return _homeHTML;
}
function renderLernenTab(){
  const pool=(()=>{
    let p=PLATES_DATA;
    if(S.fcCountry\!=="all")p=p.filter(x=>x.country===S.fcCountry);
    if(S.fcSearch.trim())p=p.filter(x=>x.code.toLowerCase().includes(S.fcSearch.toLowerCase())||x.region.toLowerCase().includes(S.fcSearch.toLowerCase()));
    return p;
  })();
  if(\!pool.length)return`<div class="panel" style="text-align:center;padding:2rem"><div style="font-size:2rem">\u{1F50D}</div><p style="color:var(--text3);margin-top:.5rem">Keine Karten gefunden.</p></div>`;
  const idx=((S.fcIdx%pool.length)+pool.length)%pool.length;
  const card=pool[idx];
  const countries=[...new Set(PLATES_DATA.map(p=>p.country))].sort();
  return`<div>
    <div style="display:flex;gap:6px;margin-bottom:.65rem">
      <input type="text" placeholder="Suche Code oder Region\u2026" value="${S.fcSearch}" oninput="S.fcSearch=this.value;S.fcIdx=0;S.fcFlipped=false;render()" style="flex:1">
      <select style="background:var(--bg3);color:var(--text);border:1.5px solid var(--border);border-radius:8px;padding:.4rem .6rem;font-size:.82rem" onchange="S.fcCountry=this.value;S.fcIdx=0;S.fcFlipped=false;render()">
        <option value="all" ${S.fcCountry==="all"?"selected":""}>Alle L\u00e4nder</option>
        ${countries.map(c=>`<option value="${c}" ${S.fcCountry===c?"selected":""}>${c}</option>`).join("")}
      </select>
    </div>
    <div style="text-align:center;color:var(--text3);font-size:.72rem;margin-bottom:.65rem">${idx+1} / ${pool.length} Karten</div>
    <div class="flashcard${S.fcFlipped?" flipped":""}" onclick="S.fcFlipped=\!S.fcFlipped;render()">
      <div class="fc-front">
        <div class="fc-label">KENNZEICHEN</div>
        <div class="fc-plate">${card.code}</div>
        <div class="fc-hint">Tippen zum Umdrehen</div>
      </div>
      <div class="fc-back">
        <div class="fc-label">REGION</div>
        <div class="fc-region">${card.region}</div>
        <div class="fc-country">${card.country}${card.state?" \u00b7 "+card.state:""}</div>
      </div>
    </div>
    <div style="display:flex;gap:8px;margin-top:.85rem">
      <button class="btn-g" style="margin-bottom:0;flex:1" onclick="S.fcIdx=Math.max(0,S.fcIdx-1);S.fcFlipped=false;render()" ${idx===0?"disabled":""}>\u2190 Zur\u00fcck</button>
      <button class="btn-p" style="margin-bottom:0;flex:1" onclick="S.fcIdx++;S.fcFlipped=false;render()" ${idx>=pool.length-1?"disabled":""}>Weiter \u2192</button>
    </div>
    <button class="btn-g" style="margin-top:.5rem" onclick="S.fcIdx=~~(Math.random()*999999);S.fcFlipped=false;render()">\u{1F500} Zuf\u00e4llig</button>
  </div>`;
}

/* LIGA TAB – Leaderboard */
function renderLigaTab(){
  const isGuest=!sbUser?.email;
  const _wkStart=new Date();_wkStart.setDate(_wkStart.getDate()-(_wkStart.getDay()||7)+1);_wkStart.setHours(0,0,0,0);
  const _wkEnd=new Date(_wkStart);_wkEnd.setDate(_wkEnd.getDate()+6);
  const _wkLbl=_wkStart.toLocaleDateString("de-DE",{day:"2-digit",month:"2-digit"})+" \u2013 "+_wkEnd.toLocaleDateString("de-DE",{day:"2-digit",month:"2-digit"});
  const _myLg=getLeague(sbProfile?.current_league||"Bronze");
  return`<div style="margin-bottom:.75rem">
    <div style="display:flex;align-items:center;justify-content:space-between">
      <div style="font-size:1.1rem;font-weight:900;color:var(--text)">\u{1F3C6} W\u00f6chentlicher Wettkampf</div>
      ${sbUser?`<div style="display:flex;align-items:center;gap:5px;background:${_myLg.bg};border:1px solid ${_myLg.color};border-radius:20px;padding:.2rem .7rem;font-size:.75rem;font-weight:700;color:${_myLg.color}">${_myLg.icon} ${_myLg.id}</div>`:""}
    </div>
    <div style="font-size:.72rem;color:var(--text3);margin-top:2px">KW ${_wkLbl} \u00b7 Reset jeden Montag 00:00 Uhr</div>
  </div>
  ${!sbOK?`<div class="panel"><p style="color:var(--text3);font-size:.85rem">Supabase nicht konfiguriert.</p></div>`:
    isGuest?`<div class="panel" style="text-align:center;padding:1.5rem">
      <div style="font-size:2rem;margin-bottom:.5rem">\u{1F464}</div>
      <div style="font-weight:700;color:var(--text);margin-bottom:.4rem">Melde dich an</div>
      <div style="color:var(--text3);font-size:.82rem;margin-bottom:1rem">Um in der Liga zu erscheinen und Punkte zu sammeln.</div>
      <button class="btn-p" onclick="S.tab='profil';S.authMode='login';render()">\u{1F511} Anmelden</button>
    </div>`:
    S.ligaLoading?`<div style="text-align:center;padding:2rem;color:var(--text3)">Laden \u2026</div>`:
    !S.ligaData.length?`<div class="panel"><p style="color:var(--text3)">Noch keine Eintr\u00e4ge.</p></div>`:
    `<div style="display:flex;gap:5px;margin-bottom:.75rem;flex-wrap:wrap">${MODES.slice(0,8).map(m=>`<button onclick="S.ligaMode='${m.id}';loadLiga()" style="flex:1;min-width:36px;background:${(S.ligaMode||'city')===m.id?'#10b981':'var(--bg3)'};color:${(S.ligaMode||'city')===m.id?'#fff':'var(--text2)'};border:1px solid var(--border);border-radius:7px;padding:.3rem .2rem;font-size:.8rem;cursor:pointer">${m.icon}</button>`).join('')}</div>
    <div class="panel" style="padding:.5rem">${S.ligaData.map((r,i)=>{
      const rc=i===0?'gold':i===1?'silver':i===2?'bronze':'';
      const isMe=sbUser&&r.user_id===sbUser.id;
      const titleBadge=r.current_title&&r.current_title\!=='Erkunder'?`<span style="font-size:.62rem;color:#a78bfa;margin-left:4px">${r.current_title}</span>`:'';
      return`<div class="lb-row${isMe?' me':''}${i<5?' promo':''}"><span class="lb-rank ${rc}">${r.rank||i+1}</span><span class="lb-name">${r.username||'Anonym'}${titleBadge}</span><span class="lb-score">${Number(r.weekly_score||r.best_score||0).toLocaleString()}</span></div>`;
    }).join('')}</div>`}`;
}
async function loadLiga(){
  if(!sb)return;
  S.ligaLoading=true;render();
  const mode=S.ligaMode||'city';
  const{data}=await sb.from("leaderboard_weekly").select("*").eq("mode",mode).order("rank",{ascending:true}).limit(30);
  S.ligaData=data||[];S.ligaLoading=false;render();
}

/* PROFIL TAB – Auth + Passport + Stats */
function promptNameChange(){
  if(!sbUser?.email){showToast("Nur für angemeldete Nutzer.");return;}
  const cur=sbProfile?.username||localStorage.getItem("gq_username")||"";
  const raw=window.prompt("Neuer Benutzername (max. 20 Zeichen):",cur);
  if(raw===null)return; /* Abgebrochen */
  const n=raw.trim().slice(0,20);
  if(!n){showToast("Name darf nicht leer sein.");return;}
  if(n===cur)return;
  /* Optimistic update */
  if(sbProfile)sbProfile.username=n;
  try{localStorage.setItem("gq_username",n);}catch(_){}
  render();
  if(sb&&sbUser){
    sb.from("profiles").update({username:n}).eq("id",sbUser.id).then(
      ()=>showToast("\u2713 Name geändert!"),
      ()=>{
        /* Rollback */
        if(sbProfile)sbProfile.username=cur;
        try{localStorage.setItem("gq_username",cur);}catch(_){}
        showToast("Fehler beim Speichern.");render();
      }
    );
  }
}
function renderProfilTab(){
  /* â”€â”€ Shared data â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
  const mastery=loadMastery();
  const totalStamps=Object.values(mastery).filter(m=>getMasteryRank(m.v,m.p)).length;
  const rank=getTravelRank(totalStamps);
  const pu=loadPU();
  const history=loadHistory();
  const isAnon=\!sbUser?.email;
  const hasName=\!\!(sbProfile?.username||localStorage.getItem("gq_username"));
  const rots=[-12,-8,-5,-3,0,3,5,8,12,15,-15];
  const passGrid=COUNTRIES.map(co=>{const m=mastery[co.cc]||{v:0,p:0};const r=getMasteryRank(m.v,m.p);if(\!r)return`<div class="stamp-cell locked" title="${co.c}"><span>?</span></div>`;const rot=rots[co.cc.charCodeAt(0)%rots.length];return stampHtml(co.cc,r,rot);}).join("");
  const regionBars=REGIONS.map(rg=>{const total=rg.cc.length;const done=rg.cc.filter(cc=>getMasteryRank((mastery[cc]||{v:0}).v,(mastery[cc]||{p:0}).p)).length;const pct2=total>0?Math.round(done/total*100):0;const complete=pct2===100;return`<div class="region-bar"><div class="region-bar-lbl"><span>${rg.name}${complete?` <span style="color:#f59e0b;font-size:.6rem">+500</span>`:""}</span><span>${done}/${total}</span></div><div class="region-bar-track"><div class="region-bar-fill${complete?" done":""}" style="width:${pct2}%"></div></div></div>`;}).join("");

  /* â”€â”€ Block 1: Identity â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
  let block1="";
  if(\!sbOK){
    block1=`<div class="auth-card" style="text-align:center"><p style="color:var(--text3);font-size:.85rem">Supabase nicht konfiguriert.</p></div>`;
  } else if(isAnon||\!hasName||S.authMode==="new_password"||S.authMode==="forgot"){
    const isReg=S.authMode==="register";
    const isForgot=S.authMode==="forgot";
    const isNewPw=S.authMode==="new_password";
    const _aIcon=isReg?"🌱":"🔑";
    const _aTitle=isReg?"Konto erstellen":isForgot?"Passwort vergessen":isNewPw?"Neues Passwort":"Anmelden";
    const _aSub=isReg?"Dein Fortschritt wird gesichert.":isForgot?"Wir senden dir einen Reset-Link.":isNewPw?"Wähle ein neues Passwort.":"Willkommen zurück!";
    block1=`<div class="auth-card">
      <div style="text-align:center;font-size:1.5rem;margin-bottom:.75rem">${_aIcon}</div>
      <div style="font-size:1rem;font-weight:900;color:var(--text);text-align:center;margin-bottom:.3rem">${_aTitle}</div>
      <div style="color:var(--text3);font-size:.78rem;text-align:center;margin-bottom:1rem">${_aSub}</div>
      ${isForgot||isNewPw?"":`<div class="auth-tabs">
        <button class="auth-tab${S.authMode==="login"?" active":""}" onclick="S.authMode='login';S.authError='';render()">Anmelden</button>
        <button class="auth-tab${S.authMode==="register"?" active":""}" onclick="S.authMode='register';S.authError='';render()">Registrieren</button>
      </div>`}
      ${S.authError?`<div class="auth-err">${S.authError}</div>`:""}
      ${isNewPw?`
        <div class="auth-field"><label>NEUES PASSWORT</label><div style="position:relative"><input id="pw-main" type="password" style="padding-right:2.4rem" placeholder="Mind. 6 Zeichen" value="${S.authPassword}" oninput="S.authPassword=this.value" onkeydown="if(event.key==='Enter')doSetNewPassword();"><button type="button" onclick="togglePw('pw-main',this)" style="position:absolute;right:.55rem;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;color:var(--text3);font-size:1.1rem;padding:0;line-height:1">\u{1F441}</button></div></div>
        <div class="auth-field"><label>PASSWORT BESTß„TIGEN</label><div style="position:relative"><input id="pw-confirm" type="password" style="padding-right:2.4rem" placeholder="Passwort wiederholen" value="${S.authConfirm}" oninput="S.authConfirm=this.value" onkeydown="if(event.key==='Enter')doSetNewPassword();"><button type="button" onclick="togglePw('pw-confirm',this)" style="position:absolute;right:.55rem;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;color:var(--text3);font-size:1.1rem;padding:0;line-height:1">\u{1F441}</button></div></div>
        <button class="btn-p" onclick="doSetNewPassword()" ${S.authLoading?"disabled":""}>${S.authLoading?"Bitte warten …":"🔑 Passwort setzen"}</button>
        <button class="btn-g" style="margin-bottom:0;background:transparent;border:none;color:var(--text3);font-size:.78rem;text-decoration:underline;cursor:pointer" onclick="S.authMode='login';S.authError='';render()">Zurück zum Login</button>
      `:isForgot?`
        <div class="auth-field"><label>E-MAIL</label><input type="email" placeholder="deine@email.de" value="${S.authEmail}" oninput="S.authEmail=this.value" onkeydown="if(event.key==='Enter')doForgotPassword()"></div>
        <button class="btn-p" onclick="doForgotPassword()" ${S.authLoading?"disabled":""}>${S.authLoading?"Bitte warten …":"📧 Reset-Link senden"}</button>
        <button class="btn-g" style="margin-bottom:0;background:transparent;border:none;color:var(--text3);font-size:.78rem;text-decoration:underline;cursor:pointer" onclick="S.authMode='login';S.authError='';render()">Zurück zum Login</button>
      `:`
        ${isReg?`<div class="auth-field"><label>BENUTZERNAME</label><input type="text" placeholder="Dein Spielername" maxlength="20" value="${S.authUsername}" oninput="S.authUsername=this.value"></div>`:""}
        <div class="auth-field"><label>E-MAIL</label><input type="email" placeholder="deine@email.de" value="${S.authEmail}" oninput="S.authEmail=this.value"></div>
        <div class="auth-field"><label>PASSWORT</label><div style="position:relative"><input id="pw-main" type="password" style="padding-right:2.4rem" placeholder="${isReg?"Mind. 6 Zeichen":"••••••"}" value="${S.authPassword}" oninput="S.authPassword=this.value" onkeydown="if(event.key==='Enter'){${isReg?"doRegister":"doLogin"}();}"><button type="button" onclick="togglePw('pw-main',this)" style="position:absolute;right:.55rem;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;color:var(--text3);font-size:1.1rem;padding:0;line-height:1">\u{1F441}</button></div></div>
        ${isReg?`<div class="auth-field"><label>PASSWORT BESTß„TIGEN</label><div style="position:relative"><input id="pw-confirm" type="password" style="padding-right:2.4rem" placeholder="Passwort wiederholen" value="${S.authConfirm}" oninput="S.authConfirm=this.value" onkeydown="if(event.key==='Enter')doRegister();"><button type="button" onclick="togglePw('pw-confirm',this)" style="position:absolute;right:.55rem;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;color:var(--text3);font-size:1.1rem;padding:0;line-height:1">\u{1F441}</button></div></div>`:""}
        <button class="btn-p" onclick="${isReg?"doRegister":"doLogin"}()" ${S.authLoading?"disabled":""}>
          ${S.authLoading?"Bitte warten …":isReg?"🌱 Konto erstellen &amp; Fortschritt sichern":"🔑 Anmelden"}
        </button>
        ${isAnon&&isReg&&totalStamps>0?`<div style="background:rgba(16,185,129,.08);border:1px solid #10b981;border-radius:8px;padding:.5rem .75rem;font-size:.74rem;color:#10b981;margin-top:.25rem">💾 ${totalStamps} Stempel &amp; deine Punkte werden übernommen.</div>`:""}
        ${\!isReg?`<button class="btn-g" style="margin-top:.25rem;margin-bottom:0;background:transparent;border:none;color:var(--text3);font-size:.78rem;text-decoration:underline;cursor:pointer" onclick="S.authMode='forgot';S.authError='';render()">Passwort vergessen?</button>`:""}
      `}
    </div>`;
  } else {
    const name=getDisplayName();
    const _lg=getLeague(sbProfile?.current_league||"Bronze");
    block1=`<div class="auth-card">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:1rem">
        <div style="width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#10b981,#0891b2);display:flex;align-items:center;justify-content:center;font-size:1.3rem;font-weight:900;color:#fff;flex-shrink:0">${name?name[0].toUpperCase():"👤"}</div>
        <div><div style="font-size:1rem;font-weight:900;color:var(--text);display:flex;align-items:center;gap:6px">${name||"Spieler"}<button onclick="promptNameChange()" title="Namen ändern" style="background:none;border:none;cursor:pointer;font-size:.8rem;color:var(--text3);padding:0;line-height:1;vertical-align:middle;opacity:.65;transition:opacity .15s" onmouseenter="this.style.opacity='1'" onmouseleave="this.style.opacity='.65'">✓</button></div><div style="font-size:.72rem;color:var(--text3)">${sbUser?.email||"Gast-Konto"}</div>${sbProfile?.current_title&&sbProfile.current_title\!=="Erkunder"?`<div style="display:inline-block;margin-top:3px;background:rgba(167,139,250,.15);border:1px solid #a78bfa;border-radius:20px;padding:1px 8px;font-size:.68rem;color:#a78bfa;font-weight:700">${sbProfile.current_title}</div>`:""}</div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;text-align:center;margin-bottom:.85rem">
        <div style="background:var(--bg3);border-radius:10px;padding:.6rem"><div style="color:#34d399;font-size:1.2rem;font-weight:700">${(sbProfile?.total_score||0).toLocaleString()}</div><div style="color:var(--text3);font-size:.65rem">Punkte</div></div>
        <div style="background:var(--bg3);border-radius:10px;padding:.6rem"><div style="color:#60a5fa;font-size:1.2rem;font-weight:700">${sbProfile?.games_played||0}</div><div style="color:var(--text3);font-size:.65rem">Spiele</div></div>
        <div style="background:var(--bg3);border-radius:10px;padding:.6rem"><div style="color:#fbbf24;font-size:1.2rem;font-weight:700">${totalStamps}</div><div style="color:var(--text3);font-size:.65rem">Stempel</div></div>
      </div>
      <div style="display:flex;align-items:center;gap:10px;background:${_lg.bg};border:1.5px solid ${_lg.color};border-radius:12px;padding:.55rem .85rem">
        <span style="font-size:1.4rem">${_lg.icon}</span>
        <div><div style="font-size:.72rem;color:var(--text3);font-weight:700;letter-spacing:.5px">AKTUELLE LIGA</div><div style="font-weight:900;color:${_lg.color};font-size:.92rem">${_lg.id}-Liga</div></div>
        <div style="margin-left:auto;font-size:.62rem;color:var(--text3);max-width:90px;text-align:right">${_lg.next}</div>
      </div>
      ${sbProfile?.is_premium?`<div style="background:rgba(16,185,129,.1);border:1px solid #10b981;border-radius:8px;padding:.45rem .7rem;font-size:.74rem;color:#34d399;margin-top:.65rem">👑 Premium aktiv</div>`:""}
    </div>`;
  }

  /* â”€â”€ Block 2: Economy & Inventory â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
  const block2=`<div class="panel" style="padding:.85rem">
    <div style="margin-bottom:.75rem">
      <div style="color:var(--text);font-weight:700;font-size:.85rem">💰 GeoCoins</div>
      <div style="color:#fbbf24;font-size:1.4rem;font-weight:900">${(sbProfile?.geo_coins||0).toLocaleString()}</div>
    </div>
    <div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin-bottom:.55rem">JOKER</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
      <div class="joker-card">
        <div style="font-size:1.4rem">✓‚</div>
        <div style="font-weight:900;font-size:.82rem;color:var(--text)">50/50</div>
        <div style="color:#34d399;font-size:.75rem;font-weight:700">${pu.five0||0} übrig</div>
        <button class="joker-buy-btn" onclick="buyJoker('five0')">+3 für 50 💰</button>
      </div>
      <div class="joker-card">
        <div style="font-size:1.4rem">\u{1F9CA}</div>
        <div style="font-weight:900;font-size:.82rem;color:var(--text)">Freeze</div>
        <div style="color:#60a5fa;font-size:.75rem;font-weight:700">${pu.freeze||0} übrig</div>
        <button class="joker-buy-btn" onclick="buyJoker('freeze')">+3 für 75 💰</button>
      </div>
    </div>
  </div>`;

  /* â”€â”€ Block 3: Stats & Career (collapsibles) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
  /* 3a: Mastery map + accuracy + history (for details section) */
  let detailStats="";
  const modeAcc={};
  history.forEach(g=>{if(\!modeAcc[g.mode])modeAcc[g.mode]={c:0,t:0};modeAcc[g.mode].c+=g.correct;modeAcc[g.mode].t+=g.rounds;});
  const modeBars=MODES.map(m=>{const s=modeAcc[m.id];if(\!s||\!s.t)return"";const p=Math.round(s.c/s.t*100);return`<div class="stat-bar-row"><div class="stat-bar-lbl">${m.icon} ${modeTitle(m).slice(0,11)}</div><div class="stat-bar-track"><div class="stat-bar-fill ${p<50?"low":p<80?"mid":""}" style="width:${p}%"></div></div><div class="stat-bar-pct">${p}%</div></div>`;}).filter(Boolean).join("");
  const tileHtml=COUNTRIES.map(co=>{const m=mastery[co.cc]||{v:0,p:0};const r=getMasteryRank(m.v,m.p);const cls=r==="gold"?"mc-done":r==="silver"?"mc-learn":r==="bronze"?"mc-new":"";return`<div class="mc-tile${cls?" "+cls:""}" title="${displayCountry(co.cc)||co.c} · ${m.v} richtig" onclick="S.modal='${co.cc}';render()"></div>`;}).join("");
  if(history.length>=2){
    const last10=history.slice(0,10).reverse();const maxSc=Math.max(...last10.map(g=>g.score),1);
    const W=300,H=72;
    const svgPts=last10.map((g,i)=>{const x=last10.length>1?i*(W/(last10.length-1)):W/2;const y=H-(g.score/maxSc)*(H-12)-6;return`${x.toFixed(1)},${y.toFixed(1)}`;}).join(" ");
    const svgDots=last10.map((g,i)=>{const x=last10.length>1?i*(W/(last10.length-1)):W/2;const y=H-(g.score/maxSc)*(H-12)-6;return`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="4" fill="#10b981"/><text x="${x.toFixed(1)}" y="${(y-8).toFixed(1)}" text-anchor="middle" fill="var(--text3)" font-size="9">${g.score>=1000?(g.score/1000).toFixed(1)+"k":g.score}</text>`;}).join("");
    detailStats=`<div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin-bottom:.5rem">SCORE-VERLAUF</div><svg viewBox="0 0 ${W} ${H}" style="width:100%;height:72px;margin-bottom:.75rem"><polyline fill="none" stroke="#10b981" stroke-width="2.5" stroke-linejoin="round" points="${svgPts}"/>${svgDots}</svg>`;
  }

  /* 3b: Achievements */
  const achHtml=ACHIEVEMENTS.map(a=>{const unlocked=a.check(S,history);return`<div class="ach-card${unlocked?" unlocked":""}"><div class="ach-icon">${unlocked?a.icon:"\u{1F512}"}</div><div class="ach-name">${a.title}</div><div class="ach-desc">${a.desc}</div></div>`;}).join("");

  const block3=`<div style="margin-bottom:.65rem">
    <details style="background:var(--bg2);border-radius:14px;border:1px solid var(--border);overflow:hidden;margin-bottom:.5rem">
      <summary style="padding:.75rem 1rem;font-weight:900;font-size:.88rem;cursor:pointer;user-select:none"><div style="display:flex;align-items:center;justify-content:space-between">
        <span>📔 Reisepass &amp; Regionen</span>
        <span style="color:var(--text3);font-size:.75rem">${totalStamps} Stempel · ${rank} →¾</span></div>
      </summary>
      <div style="padding:0 .85rem .85rem">
        <div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin-bottom:.65rem">REGIONEN-FORTSCHRITT</div>
        ${regionBars}
        <div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin:.75rem 0 .5rem">ALLE Lß„NDER</div>
        <div class="stamp-grid">${passGrid}</div>
      </div>
    </details>
    <details style="background:var(--bg2);border-radius:14px;border:1px solid var(--border);overflow:hidden;margin-bottom:.5rem">
      <summary style="padding:.75rem 1rem;font-weight:900;font-size:.88rem;cursor:pointer;user-select:none"><div style="display:flex;align-items:center;justify-content:space-between">
        <span>🏖 Erfolge &amp; Achievements</span>
        <span style="color:var(--text3);font-size:.75rem">→¾</span></div>
      </summary>
      <div style="padding:0 .85rem .85rem">
        <div class="ach-grid">${achHtml}</div>
      </div>
    </details>
    <details style="background:var(--bg2);border-radius:14px;border:1px solid var(--border);overflow:hidden">
      <summary style="padding:.75rem 1rem;font-weight:900;font-size:.88rem;cursor:pointer;user-select:none"><div style="display:flex;align-items:center;justify-content:space-between">
        <span>📊 Detaillierte Statistiken</span>
        <span style="color:var(--text3);font-size:.75rem">→¾</span></div>
      </summary>
      <div style="padding:0 .85rem .85rem">
        <div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin-bottom:.5rem">MASTERY MAP – ${totalStamps} Länder</div>
        <div style="font-size:.62rem;color:var(--text3);margin-bottom:.5rem"><span style="color:#10b981">→ </span> Gold · <span style="color:#3b82f6">→ </span> Silber · <span style="color:#f59e0b">→ </span> Bronze</div>
        <div class="mastery-tiles">${tileHtml}</div>
        ${modeBars?`<div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin:.75rem 0 .55rem">GENAUIGKEIT PRO MODUS</div>${modeBars}`:""}
        ${detailStats}
      </div>
    </details>
  </div>`;

  /* â”€â”€ Block 4: Settings & Footer â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
  const langSelect=`<select onchange="setLanguage(this.value)" style="font-size:.82rem;padding:.28rem .5rem;border-radius:8px;border:1.5px solid var(--border);background:var(--bg3);color:var(--text);cursor:pointer">
    ${[["de","Deutsch"],["en","English"],["fr","Français"],["es","Español"],["it","Italiano"],["nl","Nederlands"],["pt","Portugußªs"],["pl","Polski"],["ro","Romß¢nńƒ"],["hu","Magyar"],["cs","ńŒeŚ¡tina"],["sk","Slovenńina"],["hr","Hrvatski"],["sl","Slovensńß­na"],["bg","Ð‘ÑŠÐ»Ð³Ð°Ñ€ÑÐºÐ¸"],["el","Î•Î»Î»Î·Î½Î¹ÎºÎ¬"],["da","Dansk"],["sv","Svenska"],["fi","Suomi"],["et","Eesti"],["lv","LatvieŚ¡u"],["lt","LietuviŚ³"],["mt","Malti"],["ga","Gaeilge"]].map(([l,n])=>`<option value="${l}" ${S.language===l?"selected":""}>${n}</option>`).join("")}
  </select>`;

  const block4=`<div class="panel" style="padding:.85rem;margin-top:.15rem">
    <div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin-bottom:.75rem">EINSTELLUNGEN</div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.65rem">
      <div style="color:var(--text);font-size:.88rem;font-weight:700">${S.darkMode?"🌙 Dunkles Design":"☀️ Helles Design"}</div>
      <button onclick="S.darkMode=\!S.darkMode;applyTheme();render()" class="btn-g" style="width:auto;padding:.4rem .85rem;margin-bottom:0;font-size:.8rem">Wechseln</button>
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.75rem">
      <div style="color:var(--text);font-size:.88rem;font-weight:700">🌐 ${t("language_select")}</div>
      ${langSelect}
    </div>
    <hr style="border:none;border-top:1px solid var(--border);margin:.65rem 0 .75rem">
    <div style="text-align:center;font-size:.62rem;color:var(--text3);line-height:1.9;margin-bottom:.75rem">
      <strong style="color:var(--text2)">GeoQuest</strong> &mdash; Das Geografie-Quiz<br>
      <a href="mailto:kontakt@geoquest.app" style="color:var(--text3);text-decoration:none">kontakt@geoquest.app</a><br>
      <span style="cursor:pointer;text-decoration:underline" onclick="showToast('Impressum folgt in Kürze')">Impressum</span> &middot; <span style="cursor:pointer;text-decoration:underline" onclick="showToast('Datenschutz: Keine Weitergabe persönlicher Daten an Dritte.')">Datenschutz</span>
    </div>
    ${sbUser?.email?`
    <hr style="border:none;border-top:1px solid rgba(239,68,68,.25);margin:.1rem 0 .75rem">
    <div style="color:var(--text3);font-size:.62rem;font-weight:700;letter-spacing:1px;margin-bottom:.6rem">GEFAHRENZONE</div>
    <button class="btn-g" style="margin-bottom:.5rem;color:#f87171;border-color:#f87171" onclick="if(confirm('Wirklich abmelden?'))doLogout()">🚪 Abmelden</button>
    <button class="btn-g" style="margin-bottom:0;font-size:.75rem;background:#dc3545;color:#fff;border-color:#dc3545" onclick="doDeleteAccount()">🗑️ Konto löschen (DSGVO)</button>
    `:""}
  </div>`;

  var block5=`<div style="margin:0 15px 20px 15px;padding:20px;background:var(--bg2);border-radius:15px;border:1px solid var(--border)">
    <div style="font-size:.65rem;color:var(--text3);font-weight:700;letter-spacing:1px;margin-bottom:12px">APP-EINSTELLUNGEN</div>
    <button onclick="if(typeof renderSettingsModal==='function'){renderSettingsModal();}" style="width:100%;background:var(--card-bg,var(--bg));border:2px solid var(--border);border-radius:10px;padding:14px;display:flex;align-items:center;gap:12px;cursor:pointer;text-align:left">
      <span style="font-size:1.4rem">⚙️</span>
      <div style="flex:1">
        <div style="font-size:.88rem;font-weight:700;color:var(--text)">Layout & Raster</div>
        <div style="font-size:.72rem;color:var(--text3);margin-top:2px">Spaltenanzahl, Darstellung</div>
      </div>
      <span style="color:var(--text3);font-size:1rem">›</span>
    </button>
  </div>`;
  return '<div style="padding-bottom:100px">'+block1+block2+block3+block4+block5+'</div>';
}

/* SETTINGS MODAL */
function renderSettingsModal(){
  return`<div class="modal-overlay" onclick="if(event.target===this){S.settingsModal=false;render()}"><div class="modal-box" style="max-width:320px">
    <div style="font-size:1.1rem;font-weight:900;margin-bottom:1rem">\u2699\ufe0f Einstellungen</div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.4rem">
      <div style="font-weight:700">\u{1F310} Sprache / Language</div>
      <select onchange="setLanguage(this.value)" style="font-size:.82rem;padding:.25rem .4rem;border-radius:8px;border:1.5px solid var(--border);background:var(--bg3);color:var(--text);cursor:pointer">
        ${[["de","Deutsch"],["en","English"],["fr","Français"],["es","Español"],["it","Italiano"],["nl","Nederlands"],["pt","Portugußªs"],["pl","Polski"],["ro","Romß¢nńƒ"],["hu","Magyar"],["cs","ńŒeŚ¡tina"],["sk","Slovenńina"],["hr","Hrvatski"],["sl","SlovenŚ¡ńina"],["bg","Ð‘ÑŠÐ»Ð³Ð°Ñ€ÑÐºÐ¸"],["el","Î•Î»Î»Î·Î½Î¹ÎºÎ¬"],["da","Dansk"],["sv","Svenska"],["fi","Suomi"],["et","Eesti"],["lv","LatvieŚ¡u"],["lt","LietuviŚ³"],["mt","Malti"],["ga","Gaeilge"]].map(([l,n])=>`<option value="${l}" ${S.language===l?"selected":""}>${n}</option>`).join("")}
      </select>
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.75rem">
      <div style="font-weight:700">\u{1F4CD} Heimatregion</div>
      <span style="font-size:.78rem;color:#3b82f6;font-weight:700;cursor:pointer" onclick="localStorage.removeItem('geoquest_last_detected_country');showToast('Erkennung wird beim n\u00e4chsten Start wiederholt')">\u21ba Reset</span>
    </div>
    <div style="font-size:.76rem;color:var(--text2);margin-bottom:.75rem">${esc(localStorage.getItem('geoquest_pref_country')||'Nicht gesetzt (auto)')}</div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.75rem">
      <div style="font-weight:700">\u{1F319} Dark Mode</div>
      <button onclick="S.darkMode=!S.darkMode;applyTheme();render()" class="btn-g" style="width:auto;padding:.4rem .85rem;margin-bottom:0;font-size:.8rem">${S.darkMode?'An':'Aus'}</button>
    </div>
    ${(()=>{const _gc=parseInt(localStorage.getItem('geoquest_grid_cols'))||4;return`<div style="margin:20px 0;padding-top:15px;border-top:1px solid var(--border)"><div style="font-weight:700;margin-bottom:10px">\u{1F4CA} Spiele nebeneinander (Raster)</div><div style="display:flex;justify-content:center;gap:8px">${[2,3,4,5].map(n=>`<button onclick="saveGridCols(${n});render()" style="padding:10px 15px;font-weight:700;border:none;border-radius:8px;cursor:pointer;background:${_gc===n?'#3b82f6':'var(--bg3)'};color:${_gc===n?'#fff':'var(--text)'}">${n}</button>`).join('')}</div></div>`;})()}
        ${sbUser?.email?`<button class="btn-g" style="margin-bottom:.5rem;color:#f87171;border-color:#f87171" onclick="if(confirm('Wirklich abmelden?'))doLogout()">\u{1F6AA} Abmelden</button><button class="btn-g" style="margin-bottom:.5rem;font-size:.75rem;color:#94a3b8;border-color:#94a3b8" onclick="doDeleteAccount()">\u{1F5D1}\uFE0F Konto l\u00f6schen (DSGVO)</button>`:''}
    <button class="btn-g" style="margin-bottom:0" onclick="S.settingsModal=false;render()">Schlie\u00dfen</button>
  </div></div>`;
}

/* LEADERBOARD helper (used from home) */
function renderLeaderboard(lbData,lbLoading,mode){
  if(lbLoading)return`<div style="text-align:center;color:var(--text3);padding:1.5rem">Laden \u2026</div>`;
  if(\!sbOK)return`<div class="panel"><p style="color:var(--text3);font-size:.85rem">Verf\u00fcgbar nach Supabase-Setup.</p></div>`;
  if(\!lbData.length)return`<div class="panel"><p style="color:var(--text3);font-size:.85rem">Noch keine Eintr\u00e4ge.</p></div>`;
  const n=lbData.length;
  return`<div style="display:flex;gap:5px;margin-bottom:.75rem;flex-wrap:wrap">${MODES.map(m=>`<button onclick="S.mode='${m.id}';showLeaderboard()" style="flex:1;min-width:36px;background:${mode===m.id?"#10b981":"var(--bg3)"};color:${mode===m.id?"#fff":"var(--text2)"};border:1px solid var(--border);border-radius:7px;padding:.3rem .2rem;font-size:.8rem;font-weight:700;cursor:pointer">${m.icon}</button>`).join("")}</div>
    ${lbData.map((r,i)=>{const rc=i===0?"gold":i===1?"silver":i===2?"bronze":"";const isMe=sbUser&&r.user_id===sbUser.id;const isPromo=i<5;const isRel=i>=n-5;let cls="lb-row";if(isMe)cls+=" me";else if(isPromo)cls+=" promo";else if(isRel)cls+=" relg";return`<div class="${cls}"><span class="lb-rank ${rc}">${r.rank}</span><span class="lb-name">${esc(r.username||"Anonym")}${isMe?`<span style="color:#34d399;font-size:.7rem;margin-left:4px">Du</span>`:""}</span><span class="lb-score">${Number(r.best_score||0).toLocaleString()}</span></div>`;}).join("")}`;
}

/* GAME HISTORY */
function loadHistory(){return _gqLoad("gq_history",[]);}
function saveHistory(entry){
  const h=loadHistory();h.unshift(entry);if(h.length>60)h.length=60;_gqSave("gq_history",h);
  if(sb&&sbUser)sb.from("profiles").update({stats_history:h}).eq("id",sbUser.id).then(()=>{},()=>{});
}

/* ONBOARDING */
function loadOb(){try{return JSON.parse(localStorage.getItem("gq_onboarding")||"null")}catch(e){return null}}
function finishOb(){
  const l=S.obLang||"de",d=S.obDiff||"casual";
  localStorage.setItem("gq_onboarding",JSON.stringify({done:true,lang:l,diff:d}));
  localStorage.setItem("gq_lang",l);
  S.diff=d;S.obStep=0;render();
}
const OB_LANGS=[["de","\u{1F1E9}\u{1F1EA}","Deutsch"],["en","\u{1F1EC}\u{1F1E7}","English"],["fr","\u{1F1EB}\u{1F1F7}","Fran\u00e7ais"],["es","\u{1F1EA}\u{1F1F8}","Espa\u00f1ol"],["it","\u{1F1EE}\u{1F1F9}","Italiano"],["pl","\u{1F1F5}\u{1F1F1}","Polski"]];
function renderOnboarding(step){
  const dots=[0,1,2].map(i=>`<div class="ob-dot ${i===step?"active":""}"></div>`).join("");
  if(step===0)return`<div class="ob-overlay"><div class="ob-card">
    <div class="ob-emoji">\u{1F30D}</div>
    <div class="ob-title">${t("ob_welcome")}</div>
    <div class="ob-sub">${t("ob_sub1")}</div>
    <div class="ob-dots">${dots}</div>
    <p style="color:var(--text3);font-size:.7rem;font-weight:700;letter-spacing:1px;margin-bottom:.6rem">${t("language_select")}</p>
    <div class="ob-lang-grid">
      ${OB_LANGS.map(([l,f,n])=>`<div class="ob-lang ${S.obLang===l?"sel":""}" onclick="S.obLang='${l}';S.language='${l}';render()">${f} ${n}</div>`).join("")}
    </div>
    <button class="btn-p" onclick="S.obStep=1;render()">${t("btn_next")}</button>
    <button class="btn-g" style="margin-top:.3rem;margin-bottom:0;font-size:.82rem;color:var(--text3);background:transparent;border:none;text-decoration:underline" onclick="const ob=loadOb();if(!ob)localStorage.setItem('gq_onboarding',JSON.stringify({done:true,lang:'de',diff:'casual'}));S.obStep=0;S.tab='profil';S.authMode='login';render()">${t("ob_have_account")}</button>
    <button class="btn-g" style="margin-top:.2rem;margin-bottom:0;font-size:.82rem;color:var(--text3);background:transparent;border:none;text-decoration:underline" onclick="const ob=loadOb();if(!ob)localStorage.setItem('gq_onboarding',JSON.stringify({done:true,lang:'de',diff:'casual'}));S.obStep=0;S.tab='profil';S.authMode='register';render()">${t("ob_register")}</button>
  </div></div>`;
  if(step===1)return`<div class="ob-overlay"><div class="ob-card">
    <div class="ob-emoji">\u{1F9E0}</div>
    <div class="ob-title">${t("ob_difficulty")}</div>
    <div class="ob-sub">${t("ob_diff_sub")}</div>
    <div class="ob-dots">${dots}</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:1rem">
      <div class="ob-lang ${S.obDiff==="casual"?"sel":""}" onclick="S.obDiff='casual';render()" style="padding:.9rem"><div style="font-size:1.6rem;margin-bottom:4px">\u{1F7E2}</div><div style="font-weight:900;font-size:.88rem">Casual</div><div style="color:var(--text3);font-size:.7rem;margin-top:3px">${t("ob_diff_casual_desc")}</div></div>
      <div class="ob-lang ${S.obDiff==="hardcore"?"sel":""}" onclick="S.obDiff='hardcore';render()" style="padding:.9rem"><div style="font-size:1.6rem;margin-bottom:4px">\u{1F525}</div><div style="font-weight:900;font-size:.88rem">Hardcore</div><div style="color:var(--text3);font-size:.7rem;margin-top:3px">${t("ob_diff_hc_desc")}</div></div>
    </div>
    <button class="btn-p" onclick="S.obStep=2;render()">${t("btn_next")}</button>
    <button class="btn-g" style="margin-bottom:0" onclick="S.obStep=0;render()">${t("ob_back")}</button>
  </div></div>`;
  return`<div class="ob-overlay"><div class="ob-card">
    <div class="ob-emoji">\u{1F9ED}</div>
    <div class="ob-title">${t("ob_modes_title")}</div>
    <div class="ob-sub">${t("ob_modes_sub")}</div>
    <div class="ob-dots">${dots}</div>
    <div style="margin-bottom:1rem">
      <div class="ob-mode-row"><div class="ob-mode-icon">\u{1F3D9}</div><div><div style="color:var(--text);font-weight:700;font-size:.83rem">${t("ob_mode1_name")}</div><div class="ob-mode-desc">${t("ob_mode1_desc")}</div></div></div>
      <div class="ob-mode-row"><div class="ob-mode-icon">\u{1F697}</div><div><div style="color:var(--text);font-weight:700;font-size:.83rem">${t("ob_mode2_name")}</div><div class="ob-mode-desc">${t("ob_mode2_desc")}</div></div></div>
      <div class="ob-mode-row"><div class="ob-mode-icon">\u{1F687}</div><div><div style="color:var(--text);font-weight:700;font-size:.83rem">${t("ob_mode3_name")}</div><div class="ob-mode-desc">${t("ob_mode3_desc")}</div></div></div>
      <div style="color:var(--text3);font-size:.7rem;text-align:center;margin-top:4px">${t("ob_more_modes")}</div>
    </div>
    <button class="btn-p" onclick="finishOb()">${t("ob_start")}</button>
    <button class="btn-g" style="margin-bottom:0" onclick="S.obStep=1;render()">${t("ob_back")}</button>
  </div></div>`;
}

/* CHALLENGE (Phase 16) */
const CHALLENGE=(()=>{try{const p=new URLSearchParams(location.search);const gq=p.get("gq");if(gq){const[s,o,m]=gq.split(":");const safeM=MODES.find(x=>x.id===m)?m:"city";return{seed:parseInt(s),oppScore:parseInt(o),mode:safeM};}}catch(e){}return null;})();
function generateChallengeLink(seed,score){
  const url=location.href.split("?")[0]+"?gq="+seed+":"+score+":"+S.mode;
  navigator.clipboard.writeText(url).then(showCopyToast).catch(()=>{});
}
function startChallenge(ch){
  initRng(ch.seed);
  Object.assign(S,{sc:0,st:0,bs:0,rd:0,correct:0,lid:null,ph:"playing",mode:ch.mode,scoreSaved:false,sessionAnswers:[],newStamps:[],challenge:ch,challengeSeed:ch.seed,half_removed:false,freezeActive:false});
  lq();
}
function renderChallengeResult(ch,myScore,mode){
  const myWin=myScore>ch.oppScore,tie=myScore===ch.oppScore;
  const ml=modeTitle(MODES.find(m=>m.id===mode))||mode;
  return`<div class="ch-overlay"><div class="ch-card">
    <div style="font-size:1.5rem;font-weight:900;color:var(--text);margin-bottom:4px">${myWin?"\u{1F3C6} Gewonnen\!":tie?"\u{1F91D} Unentschieden":"\u{1F614} Knapp verpasst"}</div>
    <div style="color:var(--text3);font-size:.75rem;margin-bottom:.85rem">${ml}</div>
    <div class="ch-vs">
      <div class="ch-score-box"><div style="color:var(--text3);font-size:.65rem;margin-bottom:3px">Gegner</div><div style="font-size:1.6rem;font-weight:900;color:${\!myWin&&\!tie?"#34d399":"var(--text)"}">${ch.oppScore.toLocaleString()}</div></div>
      <div style="color:var(--text3);font-weight:900;font-size:1.1rem">VS</div>
      <div class="ch-score-box"><div style="color:#34d399;font-size:.65rem;margin-bottom:3px">Du</div><div style="font-size:1.6rem;font-weight:900;color:${myWin?"#34d399":tie?"#fbbf24":"var(--text)"}">${myScore.toLocaleString()}</div></div>
    </div>
    <button class="btn-p" onclick="generateChallengeLink(${S.challengeSeed||Date.now()},${myScore})">\u{1F517} Weitergeben</button>
    <button class="btn-g" onclick="S.challenge=null;rngSeed=null;S.ph='menu';S.tab='home';render()">Zum Menü</button>
  </div></div>`;
}

/* PAYMENT (Phase 17) */
async function processMockPayment(productId){
  const p=PAY_PRODUCTS.find(x=>x.id===productId);if(\!p)return;
  if(p.pu&&p.pu_qty){addPU(p.pu,p.pu_qty);S.payModal=false;render();showToast("✓“ "+p.name+" hinzugefügt\!");return;}
  if(sbOK&&sbUser){
    if(p.coins>0){const _cr=await sb.rpc("add_coins",{p_user_id:sbUser.id,p_amount:p.coins});
      if(_cr.data!=null&&sbProfile)sbProfile.geo_coins=_cr.data;
      else if(sbProfile)sbProfile.geo_coins=(sbProfile.geo_coins||0)+p.coins;}
    if(p.premium){const u=new Date();u.setMonth(u.getMonth()+(p.months||1));
      const _upd={is_premium:true,premium_until:u.toISOString()};
      await sb.from("profiles").update(_upd).eq("id",sbUser.id);
      if(sbProfile)Object.assign(sbProfile,_upd);}
  }
  S.payModal=false;render();showToast("✓“ "+p.name+" aktiviert\!");
}
function renderPayModal(){
  const prem=sbProfile?.is_premium;
  const until=prem&&sbProfile?.premium_until?new Date(sbProfile.premium_until).toLocaleDateString("de-DE"):"";
  return`<div class="modal-overlay" onclick="if(event.target===this){S.payModal=false;render()}"><div class="modal-box" style="max-width:360px">
    <div style="font-size:1.2rem;font-weight:900;color:var(--text);margin-bottom:.35rem">\u{1F4B3} Shop</div>
    ${prem?`<div style="background:rgba(16,185,129,.1);border:1px solid #10b981;border-radius:8px;padding:.45rem .7rem;font-size:.74rem;color:#34d399;margin-bottom:.6rem">\u{1F451} Premium aktiv${until?" • bis "+until:""}</div>`:""}
    <div style="color:var(--text3);font-size:.7rem;margin-bottom:.7rem">${STRIPE_PK?"Stripe aktiv":"Testmodus – kein echtes Geld"}</div>
    ${PAY_PRODUCTS.map(p=>`<div class="pay-product${p.featured?" featured":""}" onclick="processMockPayment('${p.id}')"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2px"><div class="pay-product-name">${p.name}${p.featured?" â­":""}</div><div class="pay-product-price">${p.price}</div></div><div class="pay-product-desc">${p.desc}</div></div>`).join("")}
    <button class="btn-g" style="margin-bottom:0;margin-top:.35rem" onclick="S.payModal=false;render()">Schließen</button>
  </div></div>`;
}

/* PWA (Phase 18) */

/* â”€â”€ Dynamic Data Loader (Phase 30) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
async function loadGameData(){
  const ov=document.createElement('div');
  ov.id='gq-loader';
  ov.style='position:fixed;inset:0;background:var(--bg,#f0f4f8);display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:9999;font-family:system-ui,sans-serif';
  ov.innerHTML='<div style="font-size:2.8rem;margin-bottom:.8rem">\u{1F30D}</div>'
    +'<div style="font-size:1rem;font-weight:700;color:var(--text,#1a2a3a);margin-bottom:.4rem">GeoQuest</div>'
    +'<div id="gq-ld-msg" style="font-size:.82rem;color:var(--text2,#64748b);margin-bottom:1rem">Lade globale Datenbank…</div>'
    +'<div style="width:200px;height:5px;background:var(--bg3,#e2e8f0);border-radius:3px;overflow:hidden">'
    +'<div id="gq-prog" style="height:100%;width:0%;background:#10b981;transition:width .3s ease;border-radius:3px"></div></div>';
  document.body.appendChild(ov);
  const prog=(p)=>{const el=document.getElementById('gq-prog');if(el)el.style.width=p+'%';};
  const msg=(t)=>{const el=document.getElementById('gq-ld-msg');if(el)el.textContent=t;};

  function sv(b,f){const x=b[f];if(\!x)return '';return x.value\!==undefined?x.value:x;}

  function parsePlates(json){
    const arr=json&&json.results&&json.results.bindings?json.results.bindings:json;
    return arr.map(b=>({code:sv(b,'code'),region:sv(b,'regionLabel')||sv(b,'region'),country:sv(b,'countryLabel')||sv(b,'country'),state:sv(b,'stateLabel')||sv(b,'state')||''})).filter(x=>x.code&&x.country);
  }
  function parseCurr(json){
    const arr=json&&json.results&&json.results.bindings?json.results.bindings:json;
    const seen=new Set(),out=[];
    arr.forEach(b=>{
      const c=sv(b,'countryLabel'),n=sv(b,'currencyLabel'),iso=sv(b,'isoCode');
      const k=c+'|'+iso;
      if(iso&&iso.length===3&&\!seen.has(k)){seen.add(k);out.push({c,n,iso});}
    });
    return out;
  }
  function parseCaps(json){
    const arr=json&&json.results&&json.results.bindings?json.results.bindings:json;
    const caps={};
    arr.forEach(b=>{
      const c=sv(b,'countryLabel'),cap=sv(b,'capitalLabel'),pop=parseInt(sv(b,'population'))||0;
      if(\!caps[c]||pop>caps[c].pop)caps[c]={c,cap,pop};
    });
    return Object.values(caps);
  }
  function parseRivers(json){
    const arr=json&&json.results&&json.results.bindings?json.results.bindings:json;
    const seen=new Set(),out=[];
    arr.forEach(b=>{
      const n=sv(b,'riverLabel'),c=sv(b,'countryLabel'),key=n+'|'+c;
      const len=Math.round(parseFloat(sv(b,'length')||0)/1000);
      if(\!seen.has(key)&&len>0){seen.add(key);out.push({n,c,len});}
    });
    return out;
  }
  function parseNeighbors(json){
    const arr=json&&json.results&&json.results.bindings?json.results.bindings:json;
    const map={};
    arr.forEach(b=>{
      const c=sv(b,'countryLabel')||sv(b,'country');
      const nb=sv(b,'neighborLabel')||sv(b,'neighbor')||sv(b,'neighbors');
      if(\!c)return;
      if(\!map[c])map[c]=[];
      if(nb&&nb.trim()){
        /* neighbors field may be comma-separated list or single value */
        const parts=nb.split(',').map(s=>s.trim()).filter(Boolean);
        parts.forEach(p=>{if(\!map[c].includes(p))map[c].push(p);});
      }
    });
    return map;
  }
  function parseArea(json){
    const arr=json&&json.results&&json.results.bindings?json.results.bindings:json;
    const best={};
    arr.forEach(b=>{
      const c=sv(b,'countryLabel')||sv(b,'country');
      const a=parseFloat(sv(b,'area')||sv(b,'areaValue')||0);
      if(\!c||\!a)return;
      /* keep smallest area per country (filters historical empires) */
      if(\!best[c]||a<best[c])best[c]=a;
    });
    return Object.entries(best)
      .filter(([,a])=>a>100&&a<2e7)
      .map(([c,area])=>({c,area:Math.round(area)}));
  }

  /* â”€â”€ per-file graceful fetch â”€â”€ */
  async function safeFetch(url,label,pct){
    try{
      msg(label);
      const r=await fetch(url);
      if(\!r.ok)throw new Error(r.status+' '+url);
      const j=await r.json();
      prog(pct);
      return j;
    }catch(ex){
      console.warn('GeoQuest: could not load '+url+':',ex.message);
      prog(pct);
      return null;
    }
  }
  const errors=[];
  const pRaw  =await safeFetch('./license_plates.json',  'Lade Kennzeichen…',  18)||[];
  const cRaw  =await safeFetch('./currencies.json',       'Lade Währungen…', 32)||[];
  const capRaw=await safeFetch('./capitals_population.json','Lade Hauptstädte…',48)||[];
  const rRaw  =await safeFetch('./rivers.json',           'Lade Flüsse…',    62)||[];
  const nbRaw =await safeFetch('./neighbors.json',        'Lade Nachbarländer…',78)||[];
  const arRaw =await safeFetch('./area.json',             'Lade Länderfächen…',92)||[];
  const topoRaw=await safeFetch('./world-110m.json',       'Lade Weltkarte…',98);
  if(topoRaw)window.WORLD_TOPO=topoRaw;

  PLATES_DATA = parsePlates(Array.isArray(pRaw)?pRaw:(pRaw?.results?.bindings||[]));
  CURR_REAL   = parseCurr(cRaw);
  const _cps=parseCaps(capRaw);if(_cps.length>0)CAPS_POP=_cps; /* Phase 95: guard empty overwrite */
  RIVERS_REAL = parseRivers(rRaw);
  const nbMap = parseNeighbors(nbRaw);
  NEIGHBORS   = Object.keys(nbMap).filter(k=>nbMap[k]&&nbMap[k].length>0).length>=10?nbMap:_DEFAULT_NEIGHBORS;
  const _ar=parseArea(arRaw);if(_ar.length>0)AREA_DATA=_ar; /* Phase 95: guard empty overwrite */

  prog(100);
  const loaded=[PLATES_DATA.length,'plates',CURR_REAL.length,'curr',CAPS_POP.length,'caps',RIVERS_REAL.length,'rivers',Object.keys(NEIGHBORS).length,'nb',AREA_DATA.length,'areas'];
  console.log('GeoQuest data:',loaded.join(' '));
  if(\!PLATES_DATA.length||\!CURR_REAL.length||\!CAPS_POP.length){
    /* core files missing – show toast after render but still render */
    setTimeout(()=>showToast('Fehler beim Laden einiger Datensätze.'),800);
  }
  await new Promise(r=>setTimeout(r,120));
  ov.remove();
}

if("serviceWorker"in navigator){
  try{
    const swSrc=`const CACHE='gq-v9';
/* Phase 99: passiver SW – kein fetch-Handler, blockt NIE Netzwerk-Requests */
self.addEventListener('install',function(){self.skipWaiting();});
self.addEventListener('activate',function(e){e.waitUntil(caches.keys().then(function(ks){return Promise.all(ks.map(function(k){return caches.delete(k);}));}).then(function(){return self.clients.claim();}));});`;
    const blob=new Blob([swSrc],{type:"application/javascript"});
    navigator.serviceWorker.register(URL.createObjectURL(blob),{scope:"./"}).catch(()=>{});
  }catch(e){}
  window.addEventListener("beforeinstallprompt",e=>{e.preventDefault();S.pwaPrompt=e;const b=document.getElementById("pwa-banner");if(b)b.style.display="flex";});
}
/* Phase 32: Tab-focus anti-cheat – timer keeps running in background */
document.addEventListener("visibilitychange",()=>{
  if(!document.hidden)return;          /* only fire when going hidden */
  if(S.ph!=="playing"||S.sel!==null)return; /* not mid-question */
  /* Record when tab was hidden; on return the setInterval fires catch-up */
  S._hiddenAt=Date.now();
});
document.addEventListener("visibilitychange",()=>{
  if(document.hidden)return;           /* only fire when becoming visible */
  if(S.ph!=="playing"||S.sel!==null||!S._hiddenAt)return;
  const elapsed=Math.ceil((Date.now()-S._hiddenAt)/1000);
  S._hiddenAt=null;
  if(elapsed>0){
    S.tm=Math.max(0,S.tm-elapsed);
    if(S.tm<=0){clearInterval(tIv);if(S.q)answer(null,_secretGameToken);}else {}
  }
});


/* â”€â”€ Phase 46: Smart Location Detection (IP-based, silent) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
const _GQ_IP_DE_MAP={
  "Germany":"Deutschland","Austria":"Österreich","Switzerland":"Schweiz",
  "Liechtenstein":"Liechtenstein","France":"Frankreich","Belgium":"Belgien",
  "Netherlands":"Niederlande","Luxembourg":"Luxemburg","Italy":"Italien",
  "Spain":"Spanien","Portugal":"Portugal","Poland":"Polen",
  "Czech Republic":"Tschechien","Czechia":"Tschechien","Slovakia":"Slowakei",
  "Hungary":"Ungarn","Romania":"Rumänien","Bulgaria":"Bulgarien",
  "Croatia":"Kroatien","Slovenia":"Slowenien","Serbia":"Serbien",
  "Bosnia and Herzegovina":"Bosnien","Albania":"Albanien","Montenegro":"Montenegro",
  "North Macedonia":"Nordmazedonien","Greece":"Griechenland","Turkey":"Türkei",
  "Estonia":"Estland","Latvia":"Lettland","Lithuania":"Litauen",
  "Finland":"Finnland","Sweden":"Schweden","Norway":"Norwegen","Denmark":"Dänemark",
  "Iceland":"Island","Ireland":"Irland","United Kingdom":"Vereinigtes Königreich",
  "Russia":"Russland","Ukraine":"Ukraine","Belarus":"Weißrussland",
  "Moldova":"Moldau","Georgia":"Georgien","Armenia":"Armenien","Azerbaijan":"Aserbaidschan"
};
function locationBannerYes(c){
  localStorage.setItem('geoquest_pref_country',c);
  S.spotterCountry=c;S.albumCountry=c;
  showToast('✓“ Region auf '+c+' gesetzt');
  render();
}
function showLocationBanner(c){
function initAntiCheat(){
S.isProcessing=false;
S._cIdx=-1;
S._cSalt=0;
window.addEventListener('beforeunload',function(){
if(S.isProcessing){
console.log('[GeoQuest Anti-Cheat] User navigated while processing - logged');
}
});
}
window.addEventListener('load',function(){initAntiCheat();});
/* P167: start deferred timer when device rotates to landscape */
(function(){
  function _onOrientChange(){
    /* delay 120ms — layout must settle before innerWidth/Height are correct */
    setTimeout(function(){
      updateOrientationWarning();
      if(S.waitingForLandscape&&!_isPortrait()){
        S.waitingForLandscape=false;
        clearInterval(tIv);
        tIv=setInterval(()=>{S.tm--;if(S.tm===3)soundWarn();render();if(S.tm<=0){clearInterval(tIv);if(S.q)answer(null);}},1000);
      }
    },120);
  }
  /* use both APIs for max compatibility */
  if(screen.orientation&&screen.orientation.addEventListener){
    screen.orientation.addEventListener("change",_onOrientChange);
  }
  window.addEventListener("orientationchange",_onOrientChange);
  /* matchMedia listener as additional fallback (Chrome desktop resize) */
  try{window.matchMedia("(orientation:landscape)").addEventListener("change",function(e){
    if(e.matches)_onOrientChange();
  });}catch(e){}
})();

  const old=document.getElementById('gq-loc-toast');if(old)old.remove();
  const el=document.createElement('div');
  el.id='gq-loc-toast';el.className='gq-loc-toast';
  el.innerHTML=`<span style="font-size:.8rem;color:var(--text2)">\u{1F4CD} ${t('loc_detected',{country:c})}</span>`
    +`<button class="gq-loc-btn-yes" onclick="locationBannerYes('${c.replace(/'/g,"\'")}');document.getElementById('gq-loc-toast')?.remove()">${t('loc_adapt')}</button>`;
  document.body.appendChild(el);
  const _tid=setTimeout(()=>{
    const t=document.getElementById('gq-loc-toast');if(\!t)return;
    t.classList.add('hiding');
    setTimeout(()=>t?.remove(),300);
  },7000);
  el.querySelector('.gq-loc-btn-yes').addEventListener('click',()=>clearTimeout(_tid),{once:true});
}
async function detectUserCountry(){
  try{
    const ctrl=new AbortController();
    const tid=setTimeout(()=>ctrl.abort(),6000);
    const res=await fetch('https://ipapi.co/json/',{signal:ctrl.signal,cache:'no-store'});
    clearTimeout(tid);
    if(!res.ok){console.warn('[GQ] ipapi.co HTTP '+res.status+' – Ländererkennung übersprungen');return;}
    const d=await res.json();
    const enName=d.country_name||'';
    const deCountry=_GQ_IP_DE_MAP[enName]||enName;
    if(\!deCountry)return;
    /* Only show banner if country exists in PLATES_DATA (sanity check) */
    const known=\!PLATES_DATA.length||PLATES_DATA.some(p=>p.country===deCountry);
    const last=localStorage.getItem('geoquest_last_detected_country');
    localStorage.setItem('geoquest_last_detected_country',deCountry);
    /* Auto-set language unless user manually chose one */
    if(!localStorage.getItem('geoquest_lang_manual')){
      const _cc=(d.country_code||'').toUpperCase();
      const _ccMap={
        'AT':'de','DE':'de','CH':'de','LI':'de',
        'FR':'fr','BE':'fr','LU':'fr','MC':'fr',
        'ES':'es','AD':'es',
        'IT':'it','SM':'it','VA':'it',
        'NL':'nl',
        'PT':'pt',
        'PL':'pl',
        'RO':'ro','MD':'ro',
        'HU':'hu',
        'CZ':'cs',
        'SK':'sk',
        'HR':'hr','BA':'hr',
        'SI':'sl',
        'BG':'bg',
        'GR':'el','CY':'el',
        'DK':'da',
        'SE':'sv',
        'FI':'fi',
        'EE':'et',
        'LV':'lv',
        'LT':'lt',
        'MT':'mt',
        'IE':'en','GB':'en','US':'en','AU':'en','CA':'en','NZ':'en','ZA':'en'
      };
      const _al=_ccMap[_cc]||'en';
      S.language=_al;localStorage.setItem('gq_lang',_al);
    }
    if(known&&last!==deCountry){showLocationBanner(deCountry);}
  }catch(e){
    console.warn('[GQ] detectUserCountry fehlgeschlagen (ipapi.co nicht erreichbar):',e?.message||e);
  }
}

loadGameData().then(()=>{
  console.log("[GQ] loadGameData done, sbAuthPending=",sbAuthPending);
  if(!sbAuthPending)render();
  setTimeout(detectUserCountry,2000);
  /* Phase 89: Hard-Override – falls initAuth() nach 1s noch hängt */
  setTimeout(()=>{
    if(sbAuthPending){
      console.warn("[GQ] 4.5s Kill-Switch: sbAuthPending noch true – erzwinge render()");
      sbAuthPending=false;
      render();
    }
  },4500);
}).catch((e)=>{
  console.error("loadGameData fatal:",e);
  document.getElementById("gq-loader")?.remove();
  sbAuthPending=false;render();
});


'''

# â”€â”€ Substitute build-time data placeholders into JS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
JS = (JS
  .replace('PLACEHOLDER_CJ',  CJ)
  .replace('PLACEHOLDER_CAPJ', CAPJ)
  .replace('PLACEHOLDER_RJ',  RJ)
  .replace('PLACEHOLDER_LMJ', LMJ)
  .replace('PLACEHOLDER_NPJ', NPJ)
  .replace('PLACEHOLDER_UNJ', UNJ)
  .replace('PLACEHOLDER_CLJ', CLJ)
  .replace('PLACEHOLDER_SWJ', SWJ)
  .replace('PLACEHOLDER_FJ',  FJ)
  .replace('PLACEHOLDER_BJ',  BJ)
  .replace('PLACEHOLDER_CUJ', CUJ)
  .replace('PLACEHOLDER_WPJ', WPJ)
)
remaining = __import__('re').findall(r'PLACEHOLDER_\w+', JS)
if remaining:
    print('WARNING: unreplaced placeholders:', set(remaining))
else:
    print('All placeholders substituted OK')


# â”€â”€ Assemble final HTML â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
_HTML_HEAD = '''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<title>GeoQuest – Das Geografie-Quiz</title>
<meta name="description" content="GeoQuest – Das Geografie-Quiz. Erkenne Länder an Flaggen, Kennzeichen und Hauptstädten. Sammle Stempel und steige in der Liga auf!">
<meta property="og:title" content="GeoQuest – Das Geografie-Quiz">
<meta property="og:description" content="Flags, Kennzeichen, Hauptstädte – teste dein Geografie-Wissen kostenlos!">
<meta property="og:type" content="website">
<meta name="theme-color" content="#10b981">
<meta name="keywords" content="Geografie Quiz, Länder Quiz, Flaggen Quiz, Kennzeichen Quiz, GeoQuest">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>\U0001f30d</text></svg>">
<link rel="manifest" href="manifest.json">
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/topojson-client@3/dist/topojson-client.min.js"></script>
<style>
:root{--bg:#f0f4f8;--bg2:#ffffff;--bg3:#f8fafc;--bg4:#e2e8f0;--border:#e2e8f0;--text:#0f172a;--text2:#475569;--text3:#94a3b8;--accent:#10b981;--shadow:0 1px 8px rgba(0,0,0,.08);--qcard:#fff;--hdr-bg:#fff;--hdr-border:#e2e8f0}
[data-theme=dark]{--bg:#0f172a;--bg2:#1e293b;--bg3:#0a0f1e;--bg4:#334155;--border:#334155;--text:#f1f5f9;--text2:#94a3b8;--text3:#475569;--shadow:0 2px 20px rgba(0,0,0,.4);--qcard:#fff;--hdr-bg:#0a0f1e;--hdr-border:#1e293b}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:var(--bg);font-family:system-ui,-apple-system,sans-serif;color:var(--text);-webkit-tap-highlight-color:transparent;transition:background .25s,color .25s}
body{padding-top:50px;padding-bottom:68px}
#app{min-height:calc(100dvh - 118px);display:flex;flex-direction:column;align-items:center;justify-content:flex-start;padding:1rem 1rem .5rem}
.scr{width:100%;max-width:420px;position:relative}
.panel{background:var(--bg2);border-radius:16px;padding:1.25rem;margin-bottom:1rem;box-shadow:var(--shadow);border:1px solid var(--border)}
input[type=text]{width:100%;background:var(--bg);color:var(--text);border:1.5px solid var(--border);border-radius:8px;padding:.5rem .75rem;font-size:.88rem}
input[type=text]:focus{outline:none;border-color:var(--accent)}
input[type=text]::placeholder{color:var(--text3)}
.g-header{position:fixed;top:0;left:0;right:0;height:50px;background:var(--hdr-bg);border-bottom:1.5px solid var(--hdr-border);display:flex;align-items:center;justify-content:space-between;padding:0 1rem;z-index:300;transition:background .25s}
.g-logo{font-size:1.15rem;font-weight:900;color:var(--text);letter-spacing:-.5px}
.g-logo span{color:#10b981}
.g-stats{display:flex;gap:8px;align-items:center}
.g-stat{background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:3px 9px;font-size:.78rem;font-weight:700;color:var(--text)}
.sound-btn{background:transparent;border:none;color:var(--text3);font-size:1rem;cursor:pointer;padding:4px;display:flex;align-items:center;width:28px;height:28px;border-radius:6px}
.sound-btn:hover{color:var(--text2);background:var(--bg3)}
.bottom-nav{position:fixed;bottom:0;left:0;right:0;height:62px;background:var(--bg2);border-top:1px solid var(--border);display:flex;z-index:300;transition:background .25s;padding-bottom:env(safe-area-inset-bottom)}
.bn-item{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1px;cursor:pointer;border:none;background:transparent;padding:0 2px;min-width:0}
.bn-icon{font-size:1.15rem;line-height:1}
.bn-lbl{font-size:.58rem;font-weight:700;letter-spacing:.2px;white-space:nowrap}
.bn-item.active .bn-icon,.bn-item.active .bn-lbl{color:#10b981}
.bn-item:not(.active) .bn-icon,.bn-item:not(.active) .bn-lbl{color:var(--text3)}
.filter-bar{display:flex;gap:6px;overflow-x:auto;padding-bottom:2px;margin-bottom:.85rem;-webkit-overflow-scrolling:touch;scrollbar-width:none}
.filter-bar::-webkit-scrollbar{display:none}
.chip{white-space:nowrap;background:var(--bg3);border:1.5px solid var(--border);border-radius:20px;padding:.3rem .8rem;font-size:.72rem;font-weight:700;color:var(--text2);cursor:pointer;transition:all .15s;flex-shrink:0}
.chip.active{background:#10b981;border-color:#10b981;color:#fff}
.daily-hero{background:linear-gradient(135deg,#10b981 0%,#0891b2 100%);border-radius:18px;padding:1.1rem 1.1rem .9rem;margin-bottom:.85rem;color:#fff;cursor:pointer;box-shadow:0 4px 20px rgba(16,185,129,.3)}
.daily-hero.done{background:var(--bg2);border:1.5px solid #10b981;cursor:default;box-shadow:var(--shadow);color:var(--text)}
.daily-hero.done .dh-title{color:#10b981}
.dh-title{font-size:.95rem;font-weight:900;margin-bottom:2px}
.dh-sub{font-size:.72rem;opacity:.85}
.dh-cd{font-family:monospace;font-weight:700;font-size:.8rem}
.dh-btn{background:rgba(255,255,255,.25);border:none;border-radius:8px;color:#fff;padding:.3rem .7rem;font-size:.72rem;font-weight:700;cursor:pointer;white-space:nowrap}
.daily-hero.done .dh-btn{display:none}
.btn-p{width:100%;background:#10b981;color:#fff;border:none;border-radius:12px;padding:.9rem;font-size:1rem;font-weight:900;cursor:pointer;transition:background .15s,transform .1s;margin-bottom:.5rem}
.btn-p:hover{background:#059669}.btn-p:active{transform:scale(.97)}
.btn-p:disabled{background:var(--bg4);color:var(--text3);cursor:default}
.btn-g{width:100%;background:transparent;color:var(--text2);border:1.5px solid var(--border);border-radius:12px;padding:.7rem;font-size:.9rem;font-weight:700;cursor:pointer;transition:border-color .15s;margin-bottom:.5rem}
.btn-g:hover{border-color:var(--text3);color:var(--text)}
.btn-cancel{background:rgba(239,68,68,.12);border:1.5px solid rgba(239,68,68,.4);color:#f87171;border-radius:8px;padding:3px 10px;font-size:.78rem;font-weight:700;cursor:pointer}
.btn-cancel:hover{color:#f87171;border-color:#f87171}
.btn-exit-global{background:#ff4757;color:#fff;border:none;border-radius:8px;padding:5px 11px;font-size:.76rem;font-weight:800;cursor:pointer;box-shadow:0 2px 6px rgba(255,71,87,.35);white-space:nowrap;flex-shrink:0;line-height:1.2}
.btn-exit-global:hover{background:#ff2f43;box-shadow:0 3px 12px rgba(255,71,87,.6)}
.btn-exit-global:active{transform:scale(.96)}
.diff-toggle{display:flex;background:var(--bg3);border-radius:10px;padding:3px;margin-bottom:.75rem;border:1px solid var(--border)}
.diff-btn{flex:1;background:transparent;color:var(--text3);border:none;border-radius:8px;padding:.5rem;font-size:.82rem;font-weight:700;cursor:pointer;transition:background .15s,color .15s}
.diff-btn.active{background:var(--bg2);color:var(--text);box-shadow:var(--shadow);font-weight:900}
/* P132: minmax(0,1fr) prevents long words from expanding grid tracks */
.mode-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;margin-bottom:.6rem}
.mode-grid-4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:5px;margin-bottom:.5rem}
.mode-grid-life{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-bottom:.5rem}
.mode-card{background:var(--bg2);border:2px solid var(--border);border-radius:12px;padding:.6rem .4rem;cursor:pointer;transition:border-color .15s,background .15s;text-align:center;box-shadow:var(--shadow);min-width:0;overflow:hidden}
.mode-card:hover{border-color:#10b981;background:var(--bg3)}
.mode-card.mini{border-radius:9px;padding:.38rem .25rem}
.mode-card.mini .mode-icon{font-size:1.1rem;margin-bottom:2px}
.mode-card.mini .mode-title{font-size:.58rem}
.mode-card.life{border-radius:10px;padding:.48rem .3rem}
.mode-card.life .mode-icon{font-size:1.2rem;margin-bottom:2px}
.mode-card.life .mode-title{font-size:.62rem}
.mode-card.active{border-color:#10b981;background:rgba(16,185,129,.08)}
.mode-icon{font-size:1.4rem;margin-bottom:3px;display:block}
.mode-title{color:var(--text);font-size:.68rem;font-weight:700;line-height:1.2;word-break:break-word;overflow-wrap:break-word}
.mode-card.locked-card{opacity:.35;filter:grayscale(.8);pointer-events:none}
.mode-desc{color:var(--text3);font-size:.58rem;margin-top:3px;line-height:1.25;font-weight:400;word-break:break-word;overflow-wrap:break-word}
.coming-soon-card{opacity:.7;cursor:pointer;position:relative;overflow:hidden}
/* Phase 86 – Logik-Gitter */
.lg-grid{display:grid;grid-template-columns:minmax(72px,1fr) repeat(3,minmax(62px,1fr));gap:4px;margin:.4rem 0}
.lg-corner{display:flex;align-items:center;justify-content:center;padding:.2rem}
.lg-header{background:var(--bg2);border-radius:8px;padding:.3rem .25rem;font-size:.6rem;font-weight:700;color:var(--text2);text-align:center;display:flex;align-items:center;justify-content:center;min-height:52px;line-height:1.25;word-break:break-word}
.lg-row-hdr{font-size:.6rem}
.lg-cell{background:var(--bg2);border:2px solid var(--border);border-radius:8px;min-height:60px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:.6rem;font-weight:700;text-align:center;cursor:pointer;transition:border-color .15s,background .15s;padding:.25rem;overflow:hidden}
.lg-cell.lg-empty{color:#10b981;font-size:1.5rem;font-weight:700;cursor:pointer;background:var(--bg3);border:2px dashed var(--border);border-radius:8px}
.lg-cell.lg-empty:hover,.lg-cell.lg-active{border-color:#10b981;background:rgba(16,185,129,.08)}
.lg-cell.lg-active{animation:lgPulse 1.2s infinite}
.lg-cell.lg-filled{color:var(--text);border-color:#10b981;background:rgba(16,185,129,.07);cursor:default}
.lg-cell.lg-empty-done{color:var(--text3);cursor:default}
.lg-cell-name{font-size:.52rem;color:var(--text2);margin-top:2px;line-height:1.15;word-break:break-word;max-width:100%}
.lg-inp-wrap{background:var(--bg2);border-radius:12px;padding:.7rem;margin:.35rem 0}
.lg-sugg{display:flex;flex-wrap:wrap;gap:4px;margin-top:5px}
.lg-sugg-item{background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:.28rem .55rem;font-size:.75rem;cursor:pointer;display:flex;align-items:center;gap:4px;transition:border-color .1s}
.lg-sugg-item:hover{border-color:#10b981}
@keyframes lgPulse{0%,100%{box-shadow:0 0 0 0 rgba(16,185,129,.4)}50%{box-shadow:0 0 0 5px rgba(16,185,129,0)}}
/* Phase 86 – Reiseroute */
.rr-step{display:inline-flex;align-items:center;gap:3px;font-size:.74rem;font-weight:700;color:var(--text)}
.rr-sn{color:var(--text)}
.rr-arrow{color:var(--text3);margin:0 2px;font-size:.8rem}
.rr-inp-wrap{background:var(--bg2);border-radius:12px;padding:.7rem;margin:.3rem 0}
.rr-sugg{display:flex;flex-wrap:wrap;gap:4px;margin-top:5px}
.rr-sugg-item{background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:.28rem .55rem;font-size:.75rem;cursor:pointer;display:flex;align-items:center;gap:4px;transition:border-color .1s}
.rr-sugg-item:hover{border-color:#8b5cf6}
.coming-soon-card:hover{border-color:#8b5cf6;background:rgba(139,92,246,.07)}
.cs-badge{position:absolute;top:5px;right:5px;background:linear-gradient(135deg,#7c3aed,#a78bfa);color:#fff;font-size:.52rem;font-weight:800;padding:1px 5px;border-radius:8px;letter-spacing:.02em;text-transform:uppercase}
.beta-badge{position:absolute;top:5px;right:5px;background:linear-gradient(135deg,#f97316,#fb923c);color:#fff;font-size:.52rem;font-weight:800;padding:1px 6px;border-radius:8px;letter-spacing:.04em;text-transform:uppercase;cursor:default;box-shadow:0 1px 4px rgba(249,115,22,.35)}
.beta-hint{font-size:.58rem;color:#f97316;margin-top:3px;line-height:1.3;opacity:.85}
.beta-card{border-color:rgba(249,115,22,.35)\!important}
.beta-card:hover{border-color:#f97316\!important;box-shadow:0 2px 12px rgba(249,115,22,.18)\!important}
.cat-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:.45rem;margin-top:.5rem}
.cat-title{color:var(--text3);font-size:.62rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase}
/* Phase 85 accordion */
.acc-list{display:flex;flex-direction:column;gap:4px;margin-bottom:.6rem}
.acc-item{border-radius:14px;overflow:hidden;border:1.5px solid var(--border);background:var(--bg2)}
.acc-item.acc-open{border-color:#10b981}
.acc-header{width:100%;background:transparent;border:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;padding:.7rem .85rem;text-align:left;gap:8px;transition:background .12s}
.acc-header:hover{background:var(--bg3)}
.acc-header:active{background:var(--bg4)}
.acc-label{color:var(--text);font-size:.88rem;font-weight:800;letter-spacing:.1px}
.acc-lock-pill{background:rgba(245,158,11,.13);border:1px solid rgba(245,158,11,.4);border-radius:10px;padding:.1rem .45rem;font-size:.58rem;font-weight:700;color:#f59e0b}
.acc-body{padding:.6rem .75rem .85rem;border-top:1px solid var(--border)}
.cat-lock-overlay{position:absolute;inset:-4px;display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(15,23,42,.72);border-radius:14px;z-index:10;cursor:pointer;gap:5px;backdrop-filter:blur(2px)}
.hud{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.pill{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:5px 14px;box-shadow:var(--shadow)}
.pill-s{background:rgba(251,146,60,.1);border:1.5px solid rgba(251,146,60,.35);border-radius:10px;padding:5px 14px}
.hlbl{font-size:.6rem;font-weight:600;letter-spacing:1px;color:var(--text3)}
.hval{font-size:1.2rem;font-weight:900;color:var(--text);line-height:1.2}
.hval-s{font-size:1.2rem;font-weight:900;color:#fed7aa;line-height:1.2}
.tbar{height:6px;background:var(--bg4);border-radius:99px;overflow:hidden;margin-bottom:14px}
.tfill{height:100%;border-radius:99px;transition:width 1s linear,background .4s}
.tbar.frozen .tfill{background:#3b82f6 !important;transition:none}
.qcard{background:var(--qcard);border-radius:18px;padding:1.1rem 1.1rem 1rem;text-align:center;margin-bottom:10px;box-shadow:0 2px 24px rgba(0,0,0,.12)}
.qprompt{color:var(--text2);font-size:1rem;font-weight:500;line-height:1.3;margin-bottom:8px}
.qmain{color:var(--text);font-size:2.4rem;font-weight:900;line-height:1.2;margin-bottom:4px;word-break:break-word}
.qsub{color:var(--text);font-size:1.2rem;font-weight:700;margin-bottom:4px}
.qflag{margin:2px 0 8px;display:flex;justify-content:center;align-items:center;min-height:80px}
.qflag img{max-width:130px;max-height:90px;width:auto;height:auto;object-fit:contain;border-radius:6px;box-shadow:0 2px 12px rgba(0,0,0,.18);display:block;margin:0 auto}
.qmeta{color:var(--text2);font-size:.88rem;margin-bottom:10px}
.qtimer{font-size:2.7rem;font-weight:900;line-height:1;transition:color .3s}
.answers{display:flex;flex-direction:column;gap:10px}
.btn-a{background:#fff;color:#0f172a;border:2px solid #e2e8f0;border-radius:13px;padding:.75rem 1rem;font-size:.95rem;font-weight:700;cursor:pointer;display:flex;justify-content:space-between;align-items:center;transition:border-color .12s,background .12s;width:100%;text-align:left;min-height:48px}
.btn-a:hover:not(:disabled){border-color:#10b981;background:#f0fdf4}
.btn-a.ok{background:#f0fdf4;border-color:#10b981;color:#065f46}
.btn-a.ng{background:#fff1f2;border-color:#f43f5e;color:#9f1239;animation:shake .35s ease}
.btn-a.dm{background:#f8fafc;border-color:#e2e8f0;color:#94a3b8;cursor:default}
.btn-a.half{opacity:.2;pointer-events:none;cursor:default}
@keyframes shake{0%,100%{transform:translateX(0)}20%{transform:translateX(-6px)}40%{transform:translateX(6px)}60%{transform:translateX(-4px)}80%{transform:translateX(4px)}}
.flag-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.btn-flag{background:#fff;border:3px solid #e2e8f0;border-radius:12px;padding:8px 6px;cursor:pointer;width:100%;transition:border-color .12s}
.btn-flag img{width:100%;max-height:64px;object-fit:contain;display:block;border-radius:4px}
.btn-flag.ok{border-color:#10b981;background:#f0fdf4}
.btn-flag.ng{border-color:#f43f5e;background:#fff1f2;animation:shake .35s ease}
.btn-flag.dm{opacity:.45;cursor:default}
.pu-bar{display:flex;gap:6px;justify-content:center;margin-bottom:8px}
.pu-btn{background:var(--bg2);border:2px solid var(--border);border-radius:10px;padding:.3rem .65rem;font-size:.72rem;font-weight:700;cursor:pointer;color:var(--text2);transition:all .15s;display:flex;align-items:center;gap:4px}
.pu-btn:hover:not(:disabled){border-color:#10b981;color:var(--text)}
.pu-btn:disabled{opacity:.35;cursor:default}
.pu-btn.freeze-on{border-color:#3b82f6 !important;color:#3b82f6 !important;background:rgba(59,130,246,.1) !important}
.joker-card{background:var(--bg3);border:1.5px solid var(--border);border-radius:12px;padding:.6rem;text-align:center;display:flex;flex-direction:column;gap:3px;align-items:center}
.joker-buy-btn{margin-top:5px;width:100%;background:linear-gradient(135deg,#f59e0b,#d97706);color:#fff;border:none;border-radius:8px;padding:.35rem .5rem;font-size:.7rem;font-weight:700;cursor:pointer;transition:opacity .15s}
.joker-buy-btn:hover{opacity:.88}.joker-buy-btn:active{transform:scale(.97)}
.fb{margin-top:10px;border-radius:12px;padding:.7rem 1rem;text-align:center;font-weight:700;font-size:.86rem}
.fb.ok{background:#f0fdf4;color:#065f46;border:1.5px solid #10b981}
.fb.ng{background:#fff1f2;color:#9f1239;border:1.5px solid #f43f5e}
.pts-popup{position:fixed;font-size:1.4rem;font-weight:900;color:#10b981;pointer-events:none;animation:floatUp .9s ease-out forwards;z-index:999}
@keyframes floatUp{0%{opacity:1;transform:translateY(0) scale(1)}100%{opacity:0;transform:translateY(-80px) scale(1.3)}}
.go-card{background:var(--bg2);border-radius:16px;padding:1.5rem;margin-bottom:.85rem;text-align:center;box-shadow:var(--shadow);border:1px solid var(--border)}
.go-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:.85rem}
.go-tile{background:var(--bg3);border-radius:12px;padding:.75rem .5rem;text-align:center;border:1px solid var(--border)}
.go-tile-val{font-size:1.5rem;font-weight:900;line-height:1.1}
.go-tile-lbl{font-size:.64rem;color:var(--text3);margin-top:2px}
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:500;display:flex;align-items:center;justify-content:center;padding:1rem}
.modal-box{background:var(--bg2);border-radius:20px;padding:1.5rem;max-width:320px;width:100%;text-align:center;box-shadow:0 8px 40px rgba(0,0,0,.25)}
.unlock-box{background:var(--bg2);border:1.5px solid #7c3aed;border-radius:20px;padding:1.5rem;max-width:340px;width:100%;text-align:center}
.unlock-btn{width:100%;border:none;border-radius:12px;padding:.85rem;font-size:.92rem;font-weight:900;cursor:pointer;margin-bottom:.5rem;transition:background .15s}
.unlock-btn.coin{background:#f59e0b;color:#fff}.unlock-btn.coin:hover{background:#d97706}
.unlock-btn.premium{background:#7c3aed;color:#fff}.unlock-btn.premium:hover{background:#6d28d9}
.stamp-toast{position:fixed;left:50%;transform:translateX(-50%);background:var(--bg2);border:1.5px solid #10b981;border-radius:12px;padding:.6rem 1.1rem;display:flex;align-items:center;gap:8px;font-size:.85rem;font-weight:700;color:#10b981;z-index:1000;animation:toastIn .35s ease-out;bottom:68px}
.copy-toast{position:fixed;left:50%;transform:translateX(-50%);background:var(--bg2);border:1.5px solid #3b82f6;border-radius:12px;padding:.5rem 1rem;font-size:.8rem;font-weight:700;color:#60a5fa;z-index:1000;animation:toastIn .35s ease-out;bottom:68px}
@keyframes toastIn{from{opacity:0;transform:translateX(-50%) translateY(20px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}
.new-stamp-banner{background:linear-gradient(135deg,#f0fdf4,#ecfdf5);border:1.5px solid #10b981;border-radius:14px;padding:.85rem 1rem;margin-bottom:.6rem;display:flex;align-items:center;gap:10px;animation:stampPop .45s cubic-bezier(.175,.885,.32,1.275)}
@keyframes stampPop{0%{transform:scale(0) rotate(-12deg);opacity:0}100%{transform:scale(1) rotate(0);opacity:1}}
.passport-cover{background:linear-gradient(135deg,#1e3a5f,#0f172a);border-radius:18px;padding:1.2rem;text-align:center;margin-bottom:.85rem;border:2px solid #1e3a5f}
.region-bar{margin-bottom:6px}
.region-bar-lbl{display:flex;justify-content:space-between;font-size:.68rem;color:var(--text2);margin-bottom:3px}
.region-bar-track{height:7px;background:var(--bg3);border-radius:99px;overflow:hidden;border:1px solid var(--border)}
.region-bar-fill{height:100%;border-radius:99px;background:#10b981;transition:width .5s}
.region-bar-fill.done{background:#f59e0b}
.stamp-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin-bottom:1rem}
.stamp-cell{aspect-ratio:1;display:flex;align-items:center;justify-content:center;border-radius:8px;cursor:pointer;position:relative;background:#f8f4ef}
.stamp-cell.locked{background:var(--bg3);border:1px dashed var(--border)}
.stamp-cell.locked span{color:var(--text3);font-size:1rem}
.stamp-ink{width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-direction:column;font-weight:900;font-size:.55rem;letter-spacing:.5px;opacity:.92;transition:transform .2s;pointer-events:none;mix-blend-mode:multiply}
.stamp-cell:hover .stamp-ink{transform:scale(1.12) rotate(-3deg) !important}
.stamp-ink.bronze{border:3px double #b45309;color:#92400e;background:radial-gradient(circle,rgba(180,83,9,.22) 50%,rgba(180,83,9,.06) 100%)}
.stamp-ink.silver{border:3px double #64748b;color:#334155;background:radial-gradient(circle,rgba(100,116,139,.2) 50%,rgba(100,116,139,.05) 100%)}
.stamp-ink.gold{border:4px double #b45309;color:#92400e;background:radial-gradient(circle,rgba(217,119,6,.3) 50%,rgba(217,119,6,.08) 100%);box-shadow:0 0 14px rgba(217,119,6,.3)}
.stamp-flag{width:28px;height:auto;border-radius:2px;margin-bottom:2px;opacity:.9}
.lb-row{display:flex;align-items:center;gap:10px;padding:.6rem .75rem;border-radius:10px;margin-bottom:5px;background:var(--bg2);border:1px solid var(--border)}
.lb-row.me{background:rgba(16,185,129,.08);border-color:#10b981}
.lb-row.promo{border-left:3px solid #10b981}
.lb-row.relg{border-left:3px solid #f43f5e}
.lb-rank{color:var(--text3);font-size:.8rem;font-weight:700;width:22px;text-align:center;flex-shrink:0}
.lb-rank.gold{color:#fbbf24}.lb-rank.silver{color:#94a3b8}.lb-rank.bronze{color:#fb923c}
.lb-name{color:var(--text);font-size:.88rem;font-weight:700;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lb-score{color:#10b981;font-size:.88rem;font-weight:900}
.lb-zone{font-size:.6rem;font-weight:700;padding:2px 5px;border-radius:4px;margin-left:4px;flex-shrink:0}
.lb-zone.up{background:rgba(16,185,129,.15);color:#10b981}
.lb-zone.dn{background:rgba(244,63,94,.15);color:#f43f5e}
.stat-bar-row{display:flex;align-items:center;gap:8px;margin-bottom:8px}
.stat-bar-lbl{color:var(--text2);font-size:.72rem;font-weight:700;width:88px;flex-shrink:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.stat-bar-track{flex:1;height:12px;background:var(--bg3);border-radius:99px;overflow:hidden;border:1px solid var(--border)}
.stat-bar-fill{height:100%;border-radius:99px;background:#10b981;transition:width .6s}
.stat-bar-fill.mid{background:#f59e0b}.stat-bar-fill.low{background:#f43f5e}
.stat-bar-pct{font-size:.72rem;font-weight:700;color:var(--text);width:35px;flex-shrink:0;text-align:right}
.ach-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:1rem}
.ach-card{background:var(--bg2);border:1.5px solid var(--border);border-radius:12px;padding:.75rem;display:flex;align-items:center;gap:10px;box-shadow:var(--shadow)}
.ach-card.unlocked{border-color:#fbbf24;background:linear-gradient(135deg,#fffbeb,#fef3c7)}
[data-theme=dark] .ach-card.unlocked{background:linear-gradient(135deg,#1e1a00,#2d2500)}
.ach-icon{font-size:1.7rem;flex-shrink:0;line-height:1}
.ach-name{font-size:.72rem;font-weight:900;color:var(--text);line-height:1.2}
.ach-desc{font-size:.62rem;color:var(--text2);margin-top:1px}
.mastery-region-lbl{color:var(--text3);font-size:.6rem;font-weight:700;letter-spacing:1.5px;margin:10px 0 6px;text-transform:uppercase}
.mastery-tiles{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:4px}
.mc-tile{border-radius:6px;padding:3px 6px;font-size:.62rem;font-weight:700;display:flex;align-items:center;gap:3px;cursor:pointer;transition:transform .15s}
.mc-tile:hover{transform:scale(1.15)}
.mc-tile img{width:14px;height:auto;border-radius:1px}
.mc-new{background:var(--bg3);color:var(--text3);border:1px solid var(--border)}
.mc-learn{background:#fef3c7;color:#92400e;border:1px solid #fde68a}
.mc-done{background:#d1fae5;color:#065f46;border:1px solid #6ee7b7}
[data-theme=dark] .mc-learn{background:#2d2500;color:#fbbf24;border-color:#854d0e}
[data-theme=dark] .mc-done{background:#022c22;color:#34d399;border-color:#065f46}
.heat-grid{display:grid;grid-template-columns:repeat(9,1fr);gap:4px;margin-bottom:.5rem}
.heat-cell{aspect-ratio:1;border-radius:4px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:.42rem;font-weight:700;color:rgba(255,255,255,.7);transition:transform .15s}
.heat-cell:hover{transform:scale(1.2)}.heat-cell.hg{background:#10b981}.heat-cell.hy{background:#f59e0b}.heat-cell.hr{background:#f43f5e}.heat-cell.hn{background:var(--bg4)}.heat-cell.he{background:var(--bg3)}
.fc-search{position:relative;margin-bottom:.75rem}
.fc-search input{padding-left:2rem}
.fc-search-icon{position:absolute;left:.65rem;top:50%;transform:translateY(-50%);color:var(--text3);font-size:.85rem;pointer-events:none}
.fc-nav{display:flex;align-items:center;justify-content:space-between;margin-bottom:.75rem}
.fc-counter{color:var(--text2);font-size:.8rem;font-weight:700}
.fc-arr{background:var(--bg2);border:1.5px solid var(--border);border-radius:8px;padding:.3rem .65rem;font-size:1rem;cursor:pointer;color:var(--text)}
.fc-arr:hover{border-color:var(--accent)}
.flashcard{background:var(--bg2);border-radius:18px;padding:1.75rem 1.5rem;text-align:center;box-shadow:var(--shadow);border:1px solid var(--border);min-height:180px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;margin-bottom:.75rem;position:relative}
.fc-front{display:flex;flex-direction:column;align-items:center;justify-content:center;width:100%}
.fc-back{display:none;flex-direction:column;align-items:center;justify-content:center;width:100%}
.flashcard.flipped .fc-front{display:none}
.flashcard.flipped .fc-back{display:flex}
.fc-label{font-size:.65rem;font-weight:700;letter-spacing:1.5px;color:var(--text3);text-transform:uppercase;margin-bottom:.5rem}
.fc-region{font-size:1.3rem;font-weight:900;color:var(--text);margin-bottom:.3rem}
.fc-country{font-size:.75rem;color:#10b981;font-weight:700;margin-top:4px}
.fc-hint{font-size:.65rem;color:var(--text3);position:absolute;bottom:.7rem;right:.9rem}
.fc-front-lbl{font-size:.65rem;font-weight:700;letter-spacing:1.5px;color:var(--text3);text-transform:uppercase;margin-bottom:.5rem}
.fc-plate{font-size:2.5rem;font-weight:900;color:#0f172a;letter-spacing:2px;background:#f0f4f8;border:3px solid #334155;border-radius:10px;padding:.3rem 1rem;margin-bottom:.4rem;display:inline-block}
.fc-back-region{font-size:1.3rem;font-weight:900;color:var(--text);margin-bottom:.3rem}
.fc-back-state{font-size:.82rem;color:var(--text2)}
.fc-back-country{font-size:.75rem;color:#10b981;font-weight:700;margin-top:4px}
.fc-filter-bar{display:flex;gap:5px;overflow-x:auto;padding-bottom:2px;margin-bottom:.75rem;scrollbar-width:none}
.fc-filter-bar::-webkit-scrollbar{display:none}
.outline-wrap{display:flex;justify-content:center;align-items:center;min-height:130px;padding:.5rem 0;margin:4px 0 8px}
.outline-path{fill:#10b981;transition:fill .4s}
.outline-path.ok{fill:#10b981;filter:drop-shadow(0 0 10px rgba(16,185,129,.9))}
.outline-path.ng{fill:#f43f5e}
.food-emoji{font-size:3.5rem;line-height:1;margin:6px 0 10px;display:block;text-align:center}
.brand-logo{font-size:1.6rem;font-weight:900;color:#0f172a;background:#fff;border-radius:10px;padding:.4rem 1rem;display:inline-block;margin-bottom:8px}
.currency-symbol{font-size:2.8rem;font-weight:900;color:#f59e0b;line-height:1;margin:4px 0 6px;display:block;text-align:center}
.plate-badge{display:inline-block;background:#fff;border:3px solid #1e293b;border-radius:10px;padding:.45rem 1.5rem;font-size:4rem;font-weight:900;letter-spacing:4px;color:#1e293b;margin:8px 0 14px;box-shadow:0 3px 14px rgba(0,0,0,.18)}
.share-btn{background:var(--bg2);color:#60a5fa;border:1.5px solid var(--border);border-radius:10px;padding:.6rem 1rem;font-size:.82rem;font-weight:700;cursor:pointer;width:100%;margin-bottom:.5rem}
.share-btn:hover{border-color:#60a5fa}
.ob-overlay{position:fixed;inset:0;background:var(--bg3);z-index:900;display:flex;align-items:center;justify-content:center;padding:1.5rem}
.ob-card{background:var(--bg2);border-radius:20px;padding:1.75rem 1.5rem;max-width:360px;width:100%;text-align:center;box-shadow:var(--shadow)}
.ob-emoji{font-size:3rem;margin-bottom:.85rem}
.ob-title{color:var(--text);font-size:1.4rem;font-weight:900;margin-bottom:.5rem}
.ob-sub{color:var(--text2);font-size:.84rem;line-height:1.55;margin-bottom:1.1rem}
.ob-dots{display:flex;justify-content:center;gap:6px;margin-bottom:1.1rem}
.ob-dot{width:7px;height:7px;border-radius:50%;background:var(--bg4);transition:background .2s}
.ob-dot.active{background:#10b981}
.ob-lang-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:1rem}
.ob-lang{background:var(--bg3);border:2px solid var(--border);border-radius:12px;padding:.75rem;cursor:pointer;color:var(--text);font-weight:700;font-size:.9rem;transition:border-color .15s}
.ob-lang:hover{border-color:var(--text3)}.ob-lang.sel{border-color:#10b981;background:rgba(16,185,129,.08);color:#10b981}
.ob-mode-row{display:flex;align-items:center;gap:10px;background:var(--bg3);border-radius:10px;padding:.6rem .85rem;margin-bottom:7px;text-align:left}
.ob-mode-icon{font-size:1.3rem;flex-shrink:0}
.ob-mode-desc{font-size:.77rem;color:var(--text2);line-height:1.3}
.guest-hook{background:linear-gradient(135deg,#f5f3ff,#ede9fe);border:1.5px solid #7c3aed;border-radius:14px;padding:1rem;margin-bottom:.85rem}
[data-theme=dark] .guest-hook{background:linear-gradient(135deg,#1e1035,#0f172a)}
.pay-product{background:var(--bg3);border:2px solid var(--border);border-radius:12px;padding:.85rem;margin-bottom:8px;cursor:pointer;transition:border-color .15s;text-align:left}
.pay-product:hover{border-color:#10b981}.pay-product.featured{border-color:#7c3aed}
.pay-product-name{color:var(--text);font-weight:700;font-size:.88rem}
.pay-product-price{color:#10b981;font-weight:900;font-size:1.05rem;margin:.2rem 0}
.pay-product-desc{color:var(--text3);font-size:.72rem}
.confetti-piece{position:fixed;top:-12px;width:9px;height:9px;z-index:9999;animation:cfFall 2.2s ease-in forwards;pointer-events:none}
@keyframes cfFall{0%{transform:translateY(0) rotate(0deg) scale(1);opacity:1}100%{transform:translateY(105vh) rotate(720deg) scale(.5);opacity:0}}
.pwa-banner{position:fixed;bottom:60px;left:0;right:0;background:var(--bg2);border-top:1px solid var(--border);padding:.6rem 1rem;display:flex;align-items:center;justify-content:space-between;z-index:290;font-size:.78rem;color:var(--text2)}
.pwa-install-btn{background:#10b981;color:#fff;border:none;border-radius:8px;padding:5px 12px;font-size:.78rem;font-weight:700;cursor:pointer}
.ch-card{background:var(--bg2);border-radius:20px;padding:1.5rem;max-width:340px;width:100%;text-align:center}
.ch-vs{display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:center;margin:1rem 0}
.ch-score-box{background:var(--bg3);border-radius:12px;padding:.85rem .5rem}
.settings-row{display:flex;align-items:center;justify-content:space-between;padding:.65rem 0;border-bottom:1px solid var(--border)}
.settings-row:last-child{border-bottom:none}
.toggle-switch{position:relative;width:42px;height:24px;flex-shrink:0}
.toggle-switch input{opacity:0;width:0;height:0}
.toggle-slider{position:absolute;inset:0;background:var(--bg4);border-radius:12px;cursor:pointer;transition:.3s}
.toggle-slider:before{content:"";position:absolute;height:18px;width:18px;left:3px;bottom:3px;background:#fff;border-radius:50%;transition:.3s}
.toggle-switch input:checked + .toggle-slider{background:#10b981}
.toggle-switch input:checked + .toggle-slider:before{transform:translateX(18px)}
.daily-banner{background:linear-gradient(135deg,#1e3a5f 0%,#1e293b 100%);border:1.5px solid #2563eb;border-radius:14px;padding:.75rem .9rem;margin-bottom:.65rem;cursor:pointer}
.daily-banner.done{border-color:#10b981;cursor:default;opacity:.8}
.daily-cd{font-family:monospace;color:#fbbf24;font-weight:700}
@media(max-width:360px){.qmain{font-size:1.65rem}.btn-a{font-size:.88rem;padding:.65rem .85rem}.qcard{padding:.9rem .9rem .8rem}.mode-grid-4{grid-template-columns:repeat(3,1fr)}.hud{margin-bottom:6px}.tbar{margin-bottom:10px}}
@media(max-height:620px){.qcard{padding:.8rem 1rem}.btn-a{min-height:44px;padding:.6rem .9rem;font-size:.88rem}.answers{gap:5px}.hud{margin-bottom:6px}.tbar{margin-bottom:8px}.qmain{font-size:1.65rem}}

/* Phase 27 – Auth Card */
.auth-card{background:var(--bg2);border:1.5px solid var(--border);border-radius:16px;padding:1.1rem;margin-bottom:.85rem}
.auth-tabs{display:flex;gap:4px;margin-bottom:.85rem;background:var(--bg3);border-radius:10px;padding:3px}
.auth-tab{flex:1;padding:.45rem;border:none;background:transparent;border-radius:8px;font-weight:700;font-size:.82rem;color:var(--text2);cursor:pointer;transition:.15s}
.auth-tab.active{background:var(--bg);color:var(--text);box-shadow:0 1px 4px rgba(0,0,0,.12)}
.auth-field{margin-bottom:.65rem}
.auth-field label{display:block;font-size:.6rem;font-weight:700;letter-spacing:1px;color:var(--text3);margin-bottom:.3rem}
.auth-field input{width:100%;box-sizing:border-box}
.auth-err{background:#fee2e2;border:1px solid #fca5a5;border-radius:8px;padding:.4rem .6rem;font-size:.76rem;color:#b91c1c;margin-bottom:.65rem}

/* Phase 28 */
.hdr-gear{background:none;border:none;font-size:1.1rem;cursor:pointer;padding:.2rem .4rem;margin-left:4px;line-height:1}
.conv-modal-bg{position:fixed;inset:0;background:rgba(0,0,0,.6);display:flex;align-items:center;justify-content:center;z-index:999;padding:1rem}
.conv-modal{background:var(--bg2);border-radius:18px;padding:1.4rem;max-width:340px;width:100%;text-align:center;border:2px solid #7c3aed}
.pop-compare-wrap{display:flex;align-items:center;justify-content:center;gap:12px;margin:1rem 0}
.pop-box{background:var(--bg3);border:2px solid var(--border);border-radius:14px;padding:.8rem 1rem;text-align:center;min-width:100px}
.pop-country{font-weight:900;font-size:1.3rem;color:var(--text);margin-bottom:.3rem}
.pop-value{color:#10b981;font-size:1rem;font-weight:700}

/* Phase 30 – Higher/Lower cards */
.hl-wrap{display:flex;align-items:center;justify-content:center;gap:10px;margin:10px 0 6px;flex-wrap:nowrap}
.hl-card{background:var(--bg3);border:2px solid var(--border);border-radius:14px;padding:.7rem .9rem;text-align:center;min-width:110px;max-width:180px;flex:1;transition:border-color .25s}
.hl-card.hl-known{border-color:#10b981}
.hl-card.hl-hidden{border-color:var(--border);opacity:.85}
.hl-card.hl-revealed{border-color:#3b82f6;opacity:1}
.hl-name{font-weight:900;font-size:1.35rem;color:var(--text);margin-bottom:.3rem;word-break:break-word;overflow-wrap:break-word;line-height:1.2}
.hl-val{color:#10b981;font-size:1.05rem;font-weight:700}
.hl-hidden .hl-val{color:var(--text3);font-size:1.4rem}
.hl-vs{font-size:1.5rem;flex-shrink:0;color:var(--text3)}
/* Phase 30 – Survival diff button */
.diff-btn.active[onclick*="survival"]{background:#7f1d1d;color:#fca5a5;border-color:#ef4444}

/* Phase 33 – Multiplayer */
.pvp-hero{background:linear-gradient(135deg,#1e1b4b 0%,#312e81 100%);border:1.5px solid #7c3aed;border-radius:14px;padding:.85rem 1rem;margin-bottom:.65rem;cursor:pointer;transition:opacity .15s}
.pvp-hero:active{opacity:.8}
.spinner{width:28px;height:28px;border:3px solid var(--border);border-top-color:#7c3aed;border-radius:50%;animation:spin .7s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}

/* â”€â”€ Phase 34: Map Guesser â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
.map-scr{display:flex;flex-direction:column;padding-bottom:.5rem}
.map-prompt{text-align:center;font-size:1rem;font-weight:700;color:var(--text);
  padding:.5rem .8rem .35rem;letter-spacing:.01em}
.map-prompt strong{color:#3b82f6}
.map-container{flex:1;min-height:200px;max-height:300px;width:100%;
  background:var(--bg2);border-radius:14px;overflow:hidden;
  touch-action:none;user-select:none;margin-bottom:.5rem}
.map-container svg{display:block;width:100%;height:100%}
.map-container .ctry{cursor:pointer;transition:fill .15s}
.map-weiter{margin:.25rem .8rem .4rem}

/* â”€â”€ Phase 33 Teil 2: MP result card â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
.mp-result-card{background:var(--bg2);border:1.5px solid var(--border);
  border-radius:18px;padding:1rem;margin:.75rem 0 .25rem;text-align:center}
.mp-result-title{font-size:.68rem;font-weight:800;letter-spacing:1.5px;
  color:var(--text3);text-transform:uppercase;margin-bottom:.75rem}
.mp-result-row{display:flex;justify-content:space-around;align-items:center;gap:.5rem}
.mp-result-col{flex:1;display:flex;flex-direction:column;align-items:center;gap:3px}
.mp-result-name{font-size:.75rem;color:var(--text2);font-weight:600;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:90px}
.mp-result-score{font-size:1.65rem;font-weight:900;letter-spacing:-1px}
.mp-you .mp-result-score{color:#10b981}
.mp-opp .mp-result-score{color:#8b5cf6}
.mp-result-verdict{font-size:.95rem;font-weight:800;margin-top:.65rem;color:var(--text)}

/* â”€â”€ Phase 33 T2: Duell Live-Bar â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
.duell-bar-wrap{display:flex;align-items:center;gap:5px;
  padding:3px 8px 5px;margin-bottom:2px}
.duell-track{flex:1;height:6px;background:var(--bg3);border-radius:3px;
  overflow:hidden;display:flex}
.duell-fill-you{background:#10b981;height:100%;border-radius:3px 0 0 3px;
  transition:width .5s ease}
.duell-fill-opp{background:#8b5cf6;height:100%;border-radius:0 3px 3px 0;
  transition:width .5s ease;margin-left:auto}
.duell-lbl{font-size:.62rem;font-weight:700;color:var(--text3);
  display:flex;flex-direction:column;align-items:center;min-width:34px;line-height:1.2}
.duell-you{color:#10b981}
.duell-opp{color:#8b5cf6}
.duell-score{font-size:.7rem;font-weight:800;font-variant-numeric:tabular-nums}
/* final comparison bar on game-over */
.duell-final-bar{display:flex;height:10px;border-radius:5px;overflow:hidden;
  margin:.6rem 0 .4rem;background:var(--bg3)}
.dfb-fill-you{background:#10b981;transition:width .8s ease}
.dfb-fill-opp{background:#8b5cf6;margin-left:auto;transition:width .8s ease}
.mp-waiting{color:var(--text3);font-size:.82rem;margin-top:.5rem;line-height:1.6}

/* â”€â”€ Phase 35: H/L dedicated buttons â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
.hl-btn-row{display:flex;flex-direction:column;gap:8px;margin:.6rem 0 .2rem;padding:0 .5rem}
.hl-btn{width:100%;padding:.7rem .5rem;border-radius:12px;border:2px solid var(--border);
  background:var(--bg2);color:var(--text);font-weight:700;font-size:.92rem;
  cursor:pointer;transition:background .15s,border-color .15s}
.hl-btn:not([disabled]):hover{background:var(--bg3)}
.hl-btn.ok{background:#d1fae5;border-color:#10b981;color:#065f46}
.hl-btn.ng{background:#fee2e2;border-color:#ef4444;color:#991b1b}
.hl-btn.dm{opacity:.45}
/* outline SVG container */
.outline-wrap{display:flex;align-items:center;justify-content:center;
  height:150px;width:100%;margin:6px auto}
.outline-wrap svg{max-height:150px;width:auto}
/* flag fallback */
.flag-fb{font-size:2.5rem;line-height:1;display:flex;align-items:center;justify-content:center;
  width:100%;height:100%}

/* â”€â”€ Phase 36: MP Lobby polish â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
.mp-lobby-title{
  font-size:1.9rem;font-weight:900;letter-spacing:-.5px;
  background:linear-gradient(135deg,#6366f1,#8b5cf6,#a855f7);
  -webkit-background-clip:text;background-clip:text;
  -webkit-text-fill-color:transparent;color:transparent;
  display:inline-block;padding:0 4px}
.mp-back-btn{
  display:block;width:100%;margin-top:1rem;padding:.85rem;
  background:var(--bg3);color:var(--text2);border:1.5px solid var(--border);
  border-radius:14px;font-weight:700;font-size:.9rem;cursor:pointer;
  text-align:center;transition:background .15s}
.mp-back-btn:hover{background:var(--bg2)}

/* â”€â”€ Phase 37-40: Kennzeichen-Album & Roadtrip-Spotter â”€â”€ */
.coll-header{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.4rem}
.coll-title{font-weight:900;font-size:1rem;color:var(--text)}
.coll-sub{font-size:.78rem;color:var(--text3)}
.coll-progress-wrap{height:8px;background:var(--bg3);border-radius:4px;overflow:hidden;margin-bottom:.25rem}
.coll-progress-bar{height:100%;background:linear-gradient(90deg,#10b981,#3b82f6);border-radius:4px;transition:width .6s ease}
.coll-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(72px,1fr));gap:7px;margin-bottom:1.5rem}
.coll-item{display:flex;flex-direction:column;align-items:center;gap:3px}
.coll-locked{opacity:.38;filter:grayscale(1)}
.coll-plate{font-size:.88rem;font-weight:900;letter-spacing:1px;border:2px solid #666;border-radius:6px;padding:4px 7px;text-align:center;min-width:46px;background:var(--bg2);transition:border-color .2s,color .2s}
.coll-region{font-size:.58rem;color:var(--text3);text-align:center;max-width:72px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.coll-dot{width:6px;height:6px;border-radius:50%}
.coll-ach{display:inline-flex;align-items:center;gap:4px;background:rgba(245,158,11,.12);border:1px solid #f59e0b;border-radius:20px;padding:3px 9px;font-size:.7rem;font-weight:700;color:#f59e0b}
/* Toast */
.gq-toast{position:fixed;bottom:90px;left:50%;transform:translateX(-50%);background:#1e293b;color:#f8fafc;padding:.55rem 1.1rem;border-radius:20px;font-size:.8rem;font-weight:600;z-index:9999;white-space:nowrap;max-width:92vw;box-shadow:0 4px 20px rgba(0,0,0,.4);pointer-events:none;animation:gqToastIn .22s ease}
@keyframes gqToastIn{from{opacity:0;transform:translateX(-50%) translateY(8px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}

/* Album shortcut banner in Home tab */
.album-shortcut{display:flex;align-items:center;justify-content:space-between;background:linear-gradient(135deg,#1e3a5f,#1e4080);border:1.5px solid #3b82f6;border-radius:14px;padding:.7rem 1rem;margin-bottom:.65rem;cursor:pointer;transition:opacity .15s;color:#fff;font-weight:700;font-size:.9rem}
.album-shortcut:active{opacity:.8}
.album-shortcut-count{font-size:.75rem;background:rgba(255,255,255,.15);border-radius:20px;padding:.2rem .65rem;font-weight:600}

/* â”€â”€ Phase 41: Album Entry Button â”€â”€ */
.album-entry-btn{display:flex;align-items:center;gap:12px;background:linear-gradient(135deg,#1e3a8a,#1d4ed8);border:1.5px solid #3b82f6;border-radius:14px;padding:.85rem 1rem;margin-bottom:.65rem;cursor:pointer;transition:opacity .15s}
.album-entry-btn:active{opacity:.8}

/* â”€â”€ Phase 41: Spotter â”€â”€ */
.album-spotter{background:var(--bg2);border:1.5px solid var(--border);border-radius:16px;padding:1.1rem;margin-bottom:.9rem}
.album-spotter-title{font-weight:900;font-size:.95rem;margin-bottom:2px}
.album-spotter-sub{color:var(--text3);font-size:.74rem;margin-bottom:.7rem}
.spotter-input{flex:1;font-size:1.6rem;font-weight:900;text-align:center;letter-spacing:5px;text-transform:uppercase;padding:.4rem .3rem;border-radius:8px;border:2px solid var(--border);background:var(--bg);color:var(--text);width:0}

/* â”€â”€ Phase 41: Progress â”€â”€ */
.album-progress-wrap{background:var(--bg2);border:1.5px solid var(--border);border-radius:14px;padding:.9rem;margin-bottom:.7rem}

/* â”€â”€ Phase 41: View toggle â”€â”€ */
.view-toggle-btn{background:var(--bg3);border:1.5px solid var(--border);border-radius:8px;padding:.35rem .8rem;font-size:.8rem;font-weight:700;color:var(--text3);cursor:pointer;transition:all .15s}
.view-toggle-btn.active{background:#10b981;border-color:#10b981;color:#fff}

/* â”€â”€ Phase 41: Country sections (List view) â”€â”€ */
.album-country-section{margin-bottom:1.1rem}
.album-country-header{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.3rem}
.real-plate-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:7px;margin-bottom:.4rem}

/* â”€â”€ Phase 41: Real license plate card â”€â”€ */
.real-plate{display:flex;align-items:stretch;background:#fff;border:2px solid #1a1a1a;border-radius:5px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.18);cursor:default;min-height:44px}
.real-plate-sm{min-height:34px}
.rp-eu-strip{width:16px;background:#003399;display:flex;flex-direction:column;align-items:center;justify-content:center;flex-shrink:0;padding:2px 0}
.rp-stars{color:#fc0;font-size:.45rem;line-height:1;display:block;text-align:center}
.rp-body{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:3px 6px}
.rp-code{font-size:1rem;font-weight:900;letter-spacing:2px;color:#111;font-family:'Arial Black',Arial,sans-serif;line-height:1}
.real-plate-sm .rp-code{font-size:.78rem;letter-spacing:1px}
.rp-region{font-size:.52rem;color:#555;letter-spacing:.3px;margin-top:1px;text-align:center;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}

/* â”€â”€ Phase 41: Map â”€â”€ */
.album-map-container{width:100%;min-height:240px;border-radius:12px;overflow:hidden;position:relative;background:var(--bg3);margin-bottom:1rem}
.map-popup{position:absolute;background:var(--bg2);border:1.5px solid var(--border);border-radius:10px;padding:.6rem .7rem;box-shadow:0 4px 20px rgba(0,0,0,.25);z-index:50;pointer-events:auto;min-width:140px}
.map-popup-title{font-weight:900;font-size:.8rem;margin-bottom:.4rem;color:var(--text)}
.map-popup-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;margin-bottom:2px}
.map-popup-close{position:absolute;top:5px;right:6px;background:none;border:none;
/* Location detection toast */
.gq-loc-toast{position:fixed;bottom:76px;left:50%;transform:translateX(-50%);z-index:9998;background:var(--bg2);border:1.5px solid #3b82f6;border-radius:24px;padding:.55rem .85rem .55rem .8rem;box-shadow:0 4px 18px rgba(0,0,0,.28);display:flex;align-items:center;gap:.6rem;white-space:nowrap;animation:locToastIn .3s cubic-bezier(.34,1.56,.64,1) both}
.gq-loc-toast.hiding{animation:locToastOut .3s ease forwards}
.gq-loc-btn-yes{background:#3b82f6;color:#fff;border:none;border-radius:14px;padding:.3rem .75rem;font-weight:700;font-size:.76rem;cursor:pointer;flex-shrink:0}
@keyframes locToastIn{from{opacity:0;transform:translateX(-50%) translateY(14px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}
@keyframes locToastOut{to{opacity:0;transform:translateX(-50%) translateY(12px)}}
@keyframes authBarSlide{0%{background-position:200% 0}100%{background-position:0% 0}}
.league-pill{display:inline-flex;align-items:center;gap:5px;border-radius:20px;padding:.18rem .65rem;font-size:.72rem;font-weight:700;border-width:1.5px;border-style:solid}
@keyframes orientSpin{0%,100%{transform:rotate(0deg)}40%{transform:rotate(90deg)}60%{transform:rotate(90deg)}}
/* â”€â”€ Phase 102: PC wide layout (â‰¥1000px) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
@media(min-width:1000px){
  body{padding-top:52px}
  .g-header{padding:0 2.5rem}
  #app{padding:1.5rem 2.5rem;align-items:stretch}
  .scr{max-width:960px}
  /* Mode-Karten: 4 Spalten */
  .mode-grid{grid-template-columns:repeat(4,minmax(0,1fr));gap:7px}
  .mode-grid-4{grid-template-columns:repeat(5,minmax(0,1fr))}
  .mode-grid-life{grid-template-columns:repeat(5,minmax(0,1fr))}
  /* Spiel: Frage-Karte + Antworten zentriert, max 600px */
  .qcard{max-width:600px;margin-left:auto;margin-right:auto}
  .answers{max-width:600px;margin-left:auto;margin-right:auto}
  /* 4 Antworten →’ 2×2 Grid auf PC */
  .answers:not(.two-opts):not(.flag-grid){display:grid;grid-template-columns:1fr 1fr;gap:9px}
  /* 2 Antworten →’ nebeneinander */
  .answers.two-opts{display:flex;flex-direction:row;gap:9px}
  .hud{max-width:840px;margin-left:auto;margin-right:auto}
  .tbar{max-width:840px;margin-left:auto;margin-right:auto}
  .pu-bar{max-width:840px;margin-left:auto;margin-right:auto}
  /* Karte: volle Höhe */
  .map-container{
    height:calc(100vh - 160px)!important;
    max-height:none!important;
    min-height:320px!important
  }
  /* Map-Guess-Screen PC: Karte links, Info rechts */
  .map-scr{
    display:grid;
    grid-template-columns:1fr 280px;
    grid-template-rows:auto auto 1fr auto auto;
    column-gap:1.2rem;
    max-width:100%
  }
  .map-scr>.hud{grid-column:1/-1}
  .map-scr>.tbar,.map-scr>[class*="frozen"]{grid-column:1/-1}
  .map-scr>.map-prompt{grid-column:2;grid-row:2;font-size:1rem;font-weight:700;padding:.3rem 0}
  .map-scr>.map-container{grid-column:1;grid-row:2/6}
  .map-scr>.fb{grid-column:2;grid-row:3;align-self:start}
  .map-scr>.map-weiter{grid-column:2;grid-row:4;margin:0}
  .map-prompt{font-size:1rem}
  /* Bottom-Nav auf PC: breiter & zentriert */
  .bottom-nav{justify-content:center}
  .bn-item{max-width:130px}
}
/* â”€â”€ Phase 103: Landscape Mobile (â‰¥500px breit, â‰¤500px hoch) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
@media(orientation:landscape)and(max-height:500px){
  body{padding-top:0;padding-bottom:0}
  .g-header,.bottom-nav{display:none}
  #app{padding:.3rem .6rem;min-height:100dvh}
  .scr{max-width:100%}
  .hud{margin-bottom:3px}
  .tbar{margin-bottom:4px}
  .qcard{padding:.5rem .75rem;margin-bottom:4px;border-radius:10px}
  .qmain{font-size:1.35rem}
  .qprompt{font-size:.72rem;margin-bottom:1px}
  /* Antworten 2-spaltig */
  .answers:not(.flag-grid){display:grid!important;grid-template-columns:1fr 1fr;gap:4px}
  .btn-a{min-height:34px;padding:.35rem .5rem;font-size:.78rem}
  .pu-bar{padding:2px 0}
  /* Karte nimmt fast den ganzen Viewport */
  .map-container{height:calc(100vh - 44px)!important;max-height:none!important;min-height:100px!important}
  .map-prompt{font-size:.76rem;padding:.15rem .4rem}
  .map-weiter{padding:.5rem;font-size:.85rem}
}
/* Landscape auf Karte: HUD bleibt sichtbar */
@media(orientation:landscape)and(min-width:1000px){
  .map-container{height:calc(100vh - 120px)!important}
}
</style>
</head>
<body>
<div id="app"></div>
<div id="gq-orient-warn" style="display:none;position:fixed;inset:0;background:rgba(10,10,20,.93);z-index:9998;flex-direction:column;align-items:center;justify-content:center;gap:1.2rem;text-align:center;padding:2rem"><div style="font-size:3.2rem;animation:orientSpin 1.8s ease-in-out infinite">&#x1F4F1;</div><div style="font-size:2rem;color:#fff">&#x27A1; &#x1F5FA;</div><div class="gq-ow-txt" style="color:#e2e8f0;font-size:.95rem;font-weight:700;max-width:280px;line-height:1.5"></div></div>
'''
_HTML_TAIL = '''</script>
</body>
</html>'''
# Inject fresh CSS from geoquest_css.txt (overrides the static CSS in _HTML_HEAD)
_si = _HTML_HEAD.find('<style>')
_se = _HTML_HEAD.find('</style>') + len('</style>')
if _si >= 0 and _se > _si:
    _HTML_HEAD = _HTML_HEAD[:_si] + '<style>\n' + CSS + '\n</style>' + _HTML_HEAD[_se:]
# === Build single script block (Phase 167 reverted - code integrity priority) ===
HTML = _HTML_HEAD + '<script>\n' + JS + '\n' + _HTML_TAIL
HTML = HTML.replace('\\!', '!')
out = 'GeoQuest.html'
with open(out, 'w', encoding='utf-8') as _f:
    _f.write(HTML)
print(f"Written: {len(HTML):,} chars -> {out}")
# Also write index.html for Netlify / direct hosting
with open('index.html', 'w', encoding='utf-8') as _f:
    _f.write(HTML)
print('Also written -> index.html (Netlify deploy target)')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           