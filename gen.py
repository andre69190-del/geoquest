import json, os, re

# â”€â”€ CITIES â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
cities_raw = json.load(open('cities_clean.json', 'r', encoding='utf-8'))
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

LANDMARKS = [
  {"name":"Eiffelturm","country":"France","cc":"fr","continent":"Europe","subregion":"Western Europe"},
  {"name":"Kolosseum","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Big Ben","country":"United Kingdom","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Sagrada Familia","country":"Spain","cc":"es","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Akropolis","country":"Greece","cc":"gr","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Stonehenge","country":"United Kingdom","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Schiefer Turm von Pisa","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Brandenburger Tor","country":"Germany","cc":"de","continent":"Europe","subregion":"Western Europe"},
  {"name":"Trevi-Brunnen","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Tower Bridge","country":"United Kingdom","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Alhambra","country":"Spain","cc":"es","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Schloss Neuschwanstein","country":"Germany","cc":"de","continent":"Europe","subregion":"Western Europe"},
  {"name":"Atomium","country":"Belgium","cc":"be","continent":"Europe","subregion":"Western Europe"},
  {"name":"Louvre","country":"France","cc":"fr","continent":"Europe","subregion":"Western Europe"},
  {"name":"Vatikan","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Hagia Sophia","country":"Turkey","cc":"tr","continent":"Europe","subregion":"Western Asia"},
  {"name":"Blaue Moschee","country":"Turkey","cc":"tr","continent":"Europe","subregion":"Western Asia"},
  {"name":"Kappadokien","country":"Turkey","cc":"tr","continent":"Europe","subregion":"Western Asia"},
  {"name":"Freiheitsstatue","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Grand Canyon","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Golden Gate Bridge","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Mount Rushmore","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"CN Tower","country":"Canada","cc":"ca","continent":"North America","subregion":"Northern America"},
  {"name":"Chichen Itza","country":"Mexico","cc":"mx","continent":"North America","subregion":"Central America"},
  {"name":"Teotihuacan","country":"Mexico","cc":"mx","continent":"North America","subregion":"Central America"},
  {"name":"Christus der Erloser","country":"Brazil","cc":"br","continent":"South America","subregion":"South America"},
  {"name":"Machu Picchu","country":"Peru","cc":"pe","continent":"South America","subregion":"South America"},
  {"name":"Galapagos-Inseln","country":"Ecuador","cc":"ec","continent":"South America","subregion":"South America"},
  {"name":"Iguazu-Wasserfaelle","country":"Argentina","cc":"ar","continent":"South America","subregion":"South America"},
  {"name":"Osterinsel","country":"Chile","cc":"cl","continent":"South America","subregion":"South America"},
  {"name":"Grosse Mauer","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Verbotene Stadt","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Terrakotta-Armee","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Mount Fuji","country":"Japan","cc":"jp","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Fushimi Inari","country":"Japan","cc":"jp","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Angkor Wat","country":"Cambodia","cc":"kh","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Taj Mahal","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Rotes Fort","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Borobudur","country":"Indonesia","cc":"id","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Petronas Towers","country":"Malaysia","cc":"my","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Burj Khalifa","country":"UAE","cc":"ae","continent":"Asia","subregion":"Western Asia"},
  {"name":"Burj Al Arab","country":"UAE","cc":"ae","continent":"Asia","subregion":"Western Asia"},
  {"name":"Petra","country":"Jordan","cc":"jo","continent":"Asia","subregion":"Western Asia"},
  {"name":"Pyramiden von Gizeh","country":"Egypt","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Abu Simbel","country":"Egypt","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Kilimandscharo","country":"Tanzania","cc":"tz","continent":"Africa","subregion":"Eastern Africa"},
  {"name":"Victoriafaelle","country":"Zimbabwe","cc":"zw","continent":"Africa","subregion":"Eastern Africa"},
  {"name":"Tafelberg","country":"South Africa","cc":"za","continent":"Africa","subregion":"Southern Africa"},
  {"name":"Grosse Barriereriff","country":"Australia","cc":"au","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"name":"Oper von Sydney","country":"Australia","cc":"au","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"name":"Uluru","country":"Australia","cc":"au","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"name":"Milford Sound","country":"New Zealand","cc":"nz","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"name":"Niagara-Faelle","country":"Canada","cc":"ca","continent":"North America","subregion":"Northern America"},
  {"name":"Bagan-Tempel","country":"Myanmar","cc":"mm","continent":"Asia","subregion":"Southeast Asia"},
]
LMJ = json.dumps(LANDMARKS, separators=(',',':'), ensure_ascii=False)

NATIONAL_PARKS = [
  {"name":"Yellowstone","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Yosemite","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Everglades","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Banff","country":"Canada","cc":"ca","continent":"North America","subregion":"Northern America"},
  {"name":"Jasper","country":"Canada","cc":"ca","continent":"North America","subregion":"Northern America"},
  {"name":"Kruger","country":"South Africa","cc":"za","continent":"Africa","subregion":"Southern Africa"},
  {"name":"Serengeti-Nationalpark","country":"Tanzania","cc":"tz","continent":"Africa","subregion":"Eastern Africa"},
  {"name":"Masai Mara","country":"Kenya","cc":"ke","continent":"Africa","subregion":"Eastern Africa"},
  {"name":"Virunga","country":"DR Congo","cc":"cd","continent":"Africa","subregion":"Middle Africa"},
  {"name":"Bwindi Impenetrable Forest","country":"Uganda","cc":"ug","continent":"Africa","subregion":"Eastern Africa"},
  {"name":"Pantanal","country":"Brazil","cc":"br","continent":"South America","subregion":"South America"},
  {"name":"Torres del Paine","country":"Chile","cc":"cl","continent":"South America","subregion":"South America"},
  {"name":"Los Glaciares","country":"Argentina","cc":"ar","continent":"South America","subregion":"South America"},
  {"name":"Galapagos-Nationalpark","country":"Ecuador","cc":"ec","continent":"South America","subregion":"South America"},
  {"name":"Manu","country":"Peru","cc":"pe","continent":"South America","subregion":"South America"},
  {"name":"Kakadu","country":"Australia","cc":"au","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"name":"Blue Mountains","country":"Australia","cc":"au","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"name":"Fiordland","country":"New Zealand","cc":"nz","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"name":"Tongariro","country":"New Zealand","cc":"nz","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"name":"Jim Corbett","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Kaziranga","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Komodo","country":"Indonesia","cc":"id","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Zhangjiajie","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Jiuzhaigou","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Sagarmatha","country":"Nepal","cc":"np","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Sundarbans","country":"Bangladesh","cc":"bd","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Pyrenaaen-Nationalpark","country":"France","cc":"fr","continent":"Europe","subregion":"Western Europe"},
  {"name":"Bayerischer Wald","country":"Germany","cc":"de","continent":"Europe","subregion":"Western Europe"},
  {"name":"Lake District","country":"United Kingdom","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Bialowieza-Wald","country":"Poland","cc":"pl","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Plitvicer Seen","country":"Croatia","cc":"hr","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Teide","country":"Spain","cc":"es","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Donana","country":"Spain","cc":"es","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Gran Paradiso","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Sarek","country":"Sweden","cc":"se","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Thingvellir","country":"Iceland","cc":"is","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Rwenzori-Berge","country":"Uganda","cc":"ug","continent":"Africa","subregion":"Eastern Africa"},
  {"name":"Etosha","country":"Namibia","cc":"na","continent":"Africa","subregion":"Southern Africa"},
  {"name":"Goreme","country":"Turkey","cc":"tr","continent":"Europe","subregion":"Western Asia"},
  {"name":"Khao Yai","country":"Thailand","cc":"th","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Chitwan","country":"Nepal","cc":"np","continent":"Asia","subregion":"Southern Asia"},
]
NPJ = json.dumps(NATIONAL_PARKS, separators=(',',':'), ensure_ascii=False)

UNESCO_SITES = [
  {"name":"Altstadt von Dubrovnik","country":"Croatia","cc":"hr","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Meteora","country":"Greece","cc":"gr","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Delphi","country":"Greece","cc":"gr","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Venedig und Lagune","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Pompeji","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Cinque Terre","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Amalfikueste","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Dolomiten","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Altstadt von Toledo","country":"Spain","cc":"es","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Altamira-Hoehle","country":"Spain","cc":"es","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Historisches Zentrum von Prag","country":"Czech Republic","cc":"cz","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Krakauer Altstadt","country":"Poland","cc":"pl","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Wieliczka-Salzbergwerk","country":"Poland","cc":"pl","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Auschwitz-Birkenau","country":"Poland","cc":"pl","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Historisches Tallinn","country":"Estonia","cc":"ee","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Historisches Riga","country":"Latvia","cc":"lv","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Altstadt von Bruegge","country":"Belgium","cc":"be","continent":"Europe","subregion":"Western Europe"},
  {"name":"Koelner Dom","country":"Germany","cc":"de","continent":"Europe","subregion":"Western Europe"},
  {"name":"Bamberger Altstadt","country":"Germany","cc":"de","continent":"Europe","subregion":"Western Europe"},
  {"name":"Schloss Sanssouci","country":"Germany","cc":"de","continent":"Europe","subregion":"Western Europe"},
  {"name":"Wachau","country":"Austria","cc":"at","continent":"Europe","subregion":"Western Europe"},
  {"name":"Hallstatt","country":"Austria","cc":"at","continent":"Europe","subregion":"Western Europe"},
  {"name":"Palast von Versailles","country":"France","cc":"fr","continent":"Europe","subregion":"Western Europe"},
  {"name":"Mont-Saint-Michel","country":"France","cc":"fr","continent":"Europe","subregion":"Western Europe"},
  {"name":"Pont du Gard","country":"France","cc":"fr","continent":"Europe","subregion":"Western Europe"},
  {"name":"Timbuktu","country":"Mali","cc":"ml","continent":"Africa","subregion":"Western Africa"},
  {"name":"Felsenkirchen von Lalibela","country":"Ethiopia","cc":"et","continent":"Africa","subregion":"Eastern Africa"},
  {"name":"Historisches Kairo","country":"Egypt","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Tal der Koenige","country":"Egypt","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Medina von Fes","country":"Morocco","cc":"ma","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Medina von Marrakesch","country":"Morocco","cc":"ma","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Potala-Palast","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Lijiang-Altstadt","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Altstadt von Kyoto","country":"Japan","cc":"jp","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Horyu-ji-Tempel","country":"Japan","cc":"jp","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Historisches Hoi An","country":"Vietnam","cc":"vn","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Ajanta-Hoehlen","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Hampi","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Bagan","country":"Myanmar","cc":"mm","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Chan Chan","country":"Peru","cc":"pe","continent":"South America","subregion":"South America"},
  {"name":"Historisches Cartagena","country":"Colombia","cc":"co","continent":"South America","subregion":"South America"},
  {"name":"Chaco Culture","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
]
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
FOOD = [{'dish': 'Sushi', 'country': 'Japan', 'cc': 'jp', 'emoji': 'ðŸ£'}, {'dish': 'Pizza', 'country': 'Italy', 'cc': 'it', 'emoji': 'ðŸ•'}, {'dish': 'Tacos', 'country': 'Mexico', 'cc': 'mx', 'emoji': 'ðŸŒ®'}, {'dish': 'Croissant', 'country': 'France', 'cc': 'fr', 'emoji': 'ðŸ¥'}, {'dish': 'Paella', 'country': 'Spain', 'cc': 'es', 'emoji': 'ðŸ¥˜'}, {'dish': 'Kimchi', 'country': 'South Korea', 'cc': 'kr', 'emoji': 'ðŸ¥¬'}, {'dish': 'Pho', 'country': 'Vietnam', 'cc': 'vn', 'emoji': 'ðŸœ'}, {'dish': 'Pad Thai', 'country': 'Thailand', 'cc': 'th', 'emoji': 'ðŸœ'}, {'dish': 'Peking Duck', 'country': 'China', 'cc': 'cn', 'emoji': 'ðŸ¦†'}, {'dish': 'Biryani', 'country': 'India', 'cc': 'in', 'emoji': 'ðŸ›'}, {'dish': 'Samosa', 'country': 'India', 'cc': 'in', 'emoji': 'ðŸ§†'}, {'dish': 'Rendang', 'country': 'Indonesia', 'cc': 'id', 'emoji': 'ðŸ–'}, {'dish': 'Nasi Goreng', 'country': 'Indonesia', 'cc': 'id', 'emoji': 'ðŸš'}, {'dish': 'Jollof Rice', 'country': 'Nigeria', 'cc': 'ng', 'emoji': 'ðŸš'}, {'dish': 'Injera', 'country': 'Ethiopia', 'cc': 'et', 'emoji': 'ðŸ§‡'}, {'dish': 'Tagine', 'country': 'Morocco', 'cc': 'ma', 'emoji': 'ðŸ²'}, {'dish': 'Borscht', 'country': 'Ukraine', 'cc': 'ua', 'emoji': 'ðŸ±'}, {'dish': 'Pierogi', 'country': 'Poland', 'cc': 'pl', 'emoji': 'ðŸ¥Ÿ'}, {'dish': 'Goulash', 'country': 'Hungary', 'cc': 'hu', 'emoji': 'ðŸ²'}, {'dish': 'Moussaka', 'country': 'Greece', 'cc': 'gr', 'emoji': 'ðŸ•'}, {'dish': 'Fish and Chips', 'country': 'United Kingdom', 'cc': 'gb', 'emoji': 'ðŸŸ'}, {'dish': 'Poutine', 'country': 'Canada', 'cc': 'ca', 'emoji': 'ðŸŸ'}, {'dish': 'Ceviche', 'country': 'Peru', 'cc': 'pe', 'emoji': 'ðŸŸ'}, {'dish': 'Empanada', 'country': 'Argentina', 'cc': 'ar', 'emoji': 'ðŸ¥ª'}, {'dish': 'Feijoada', 'country': 'Brazil', 'cc': 'br', 'emoji': 'ðŸ²'}, {'dish': 'Fondue', 'country': 'Switzerland', 'cc': 'ch', 'emoji': 'ðŸ§€'}, {'dish': 'Wiener Schnitzel', 'country': 'Austria', 'cc': 'at', 'emoji': 'ðŸ–'}, {'dish': 'Bacalhau', 'country': 'Portugal', 'cc': 'pt', 'emoji': 'ðŸŸ'}, {'dish': 'Shakshuka', 'country': 'Israel', 'cc': 'il', 'emoji': 'ðŸ³'}, {'dish': 'Bibimbap', 'country': 'South Korea', 'cc': 'kr', 'emoji': 'ðŸ±'}, {'dish': 'Stroganoff', 'country': 'Russia', 'cc': 'ru', 'emoji': 'ðŸ¥©'}, {'dish': 'Bobotie', 'country': 'South Africa', 'cc': 'za', 'emoji': 'ðŸ–'}, {'dish': 'Tom Yum', 'country': 'Thailand', 'cc': 'th', 'emoji': 'ðŸ§…'}, {'dish': 'Churros', 'country': 'Spain', 'cc': 'es', 'emoji': 'ðŸ©'}, {'dish': 'Smorgasbord', 'country': 'Sweden', 'cc': 'se', 'emoji': 'ðŸ¥ª'}]
FJ  = json.dumps(FOOD,   separators=(',',':'), ensure_ascii=False)

BRANDS = [{'brand': 'Samsung', 'country': 'South Korea', 'cc': 'kr', 'industry': 'Elektronik', 'sub': 'Eastern Asia'}, {'brand': 'LG', 'country': 'South Korea', 'cc': 'kr', 'industry': 'Elektronik', 'sub': 'Eastern Asia'}, {'brand': 'Hyundai', 'country': 'South Korea', 'cc': 'kr', 'industry': 'Autos', 'sub': 'Eastern Asia'}, {'brand': 'Kia', 'country': 'South Korea', 'cc': 'kr', 'industry': 'Autos', 'sub': 'Eastern Asia'}, {'brand': 'Nintendo', 'country': 'Japan', 'cc': 'jp', 'industry': 'Gaming', 'sub': 'Eastern Asia'}, {'brand': 'Sony', 'country': 'Japan', 'cc': 'jp', 'industry': 'Elektronik', 'sub': 'Eastern Asia'}, {'brand': 'Toyota', 'country': 'Japan', 'cc': 'jp', 'industry': 'Autos', 'sub': 'Eastern Asia'}, {'brand': 'Honda', 'country': 'Japan', 'cc': 'jp', 'industry': 'Autos', 'sub': 'Eastern Asia'}, {'brand': 'Yamaha', 'country': 'Japan', 'cc': 'jp', 'industry': 'Musik/Autos', 'sub': 'Eastern Asia'}, {'brand': 'Lenovo', 'country': 'China', 'cc': 'cn', 'industry': 'Elektronik', 'sub': 'Eastern Asia'}, {'brand': 'Alibaba', 'country': 'China', 'cc': 'cn', 'industry': 'E-Commerce', 'sub': 'Eastern Asia'}, {'brand': 'Xiaomi', 'country': 'China', 'cc': 'cn', 'industry': 'Elektronik', 'sub': 'Eastern Asia'}, {'brand': 'Huawei', 'country': 'China', 'cc': 'cn', 'industry': 'Telekommunikation', 'sub': 'Eastern Asia'}, {'brand': 'IKEA', 'country': 'Sweden', 'cc': 'se', 'industry': 'Moebel', 'sub': 'Northern Europe'}, {'brand': 'H&M', 'country': 'Sweden', 'cc': 'se', 'industry': 'Mode', 'sub': 'Northern Europe'}, {'brand': 'Volvo', 'country': 'Sweden', 'cc': 'se', 'industry': 'Autos', 'sub': 'Northern Europe'}, {'brand': 'Spotify', 'country': 'Sweden', 'cc': 'se', 'industry': 'Streaming', 'sub': 'Northern Europe'}, {'brand': 'LEGO', 'country': 'Denmark', 'cc': 'dk', 'industry': 'Spielzeug', 'sub': 'Northern Europe'}, {'brand': 'Bang & Olufsen', 'country': 'Denmark', 'cc': 'dk', 'industry': 'Elektronik', 'sub': 'Northern Europe'}, {'brand': 'Nokia', 'country': 'Finland', 'cc': 'fi', 'industry': 'Telekommunikation', 'sub': 'Northern Europe'}, {'brand': 'Volkswagen', 'country': 'Germany', 'cc': 'de', 'industry': 'Autos', 'sub': 'Western Europe'}, {'brand': 'BMW', 'country': 'Germany', 'cc': 'de', 'industry': 'Autos', 'sub': 'Western Europe'}, {'brand': 'Porsche', 'country': 'Germany', 'cc': 'de', 'industry': 'Autos', 'sub': 'Western Europe'}, {'brand': 'ALDI', 'country': 'Germany', 'cc': 'de', 'industry': 'Einzelhandel', 'sub': 'Western Europe'}, {'brand': 'Airbus', 'country': 'France', 'cc': 'fr', 'industry': 'Luftfahrt', 'sub': 'Western Europe'}, {'brand': 'Renault', 'country': 'France', 'cc': 'fr', 'industry': 'Autos', 'sub': 'Western Europe'}, {'brand': 'Louis Vuitton', 'country': 'France', 'cc': 'fr', 'industry': 'Luxus', 'sub': 'Western Europe'}, {'brand': 'Ferrari', 'country': 'Italy', 'cc': 'it', 'industry': 'Autos', 'sub': 'Southern Europe'}, {'brand': 'Maserati', 'country': 'Italy', 'cc': 'it', 'industry': 'Autos', 'sub': 'Southern Europe'}, {'brand': 'Zara', 'country': 'Spain', 'cc': 'es', 'industry': 'Mode', 'sub': 'Southern Europe'}, {'brand': 'Shell', 'country': 'Netherlands', 'cc': 'nl', 'industry': 'Energie', 'sub': 'Western Europe'}, {'brand': 'Philips', 'country': 'Netherlands', 'cc': 'nl', 'industry': 'Elektronik', 'sub': 'Western Europe'}, {'brand': 'Heineken', 'country': 'Netherlands', 'cc': 'nl', 'industry': 'Bier', 'sub': 'Western Europe'}, {'brand': 'Nestle', 'country': 'Switzerland', 'cc': 'ch', 'industry': 'Lebensmittel', 'sub': 'Western Europe'}, {'brand': 'Rolex', 'country': 'Switzerland', 'cc': 'ch', 'industry': 'Uhren', 'sub': 'Western Europe'}, {'brand': 'Skoda', 'country': 'Czech Republic', 'cc': 'cz', 'industry': 'Autos', 'sub': 'Eastern Europe'}, {'brand': 'Emirates', 'country': 'UAE', 'cc': 'ae', 'industry': 'Luftfahrt', 'sub': 'Western Asia'}, {'brand': 'Petronas', 'country': 'Malaysia', 'cc': 'my', 'industry': 'Energie', 'sub': 'Southeast Asia'}, {'brand': 'Tata', 'country': 'India', 'cc': 'in', 'industry': 'Konglomerat', 'sub': 'Southern Asia'}, {'brand': 'Corona', 'country': 'Mexico', 'cc': 'mx', 'industry': 'Bier', 'sub': 'Central America'}, {'brand': 'Embraer', 'country': 'Brazil', 'cc': 'br', 'industry': 'Luftfahrt', 'sub': 'South America'}, {'brand': 'MTN', 'country': 'South Africa', 'cc': 'za', 'industry': 'Telekommunikation', 'sub': 'Southern Africa'}]
BJ  = json.dumps(BRANDS, separators=(',',':'), ensure_ascii=False)

CURRENCIES = [{'currency': 'Yen', 'symbol': 'Â¥', 'country': 'Japan', 'cc': 'jp', 'sub': 'Eastern Asia'}, {'currency': 'Won', 'symbol': 'â‚©', 'country': 'South Korea', 'cc': 'kr', 'sub': 'Eastern Asia'}, {'currency': 'Renminbi', 'symbol': 'Â¥', 'country': 'China', 'cc': 'cn', 'sub': 'Eastern Asia'}, {'currency': 'Rupee', 'symbol': 'â‚¹', 'country': 'India', 'cc': 'in', 'sub': 'Southern Asia'}, {'currency': 'Taka', 'symbol': 'à§³', 'country': 'Bangladesh', 'cc': 'bd', 'sub': 'Southern Asia'}, {'currency': 'Baht', 'symbol': 'à¸¿', 'country': 'Thailand', 'cc': 'th', 'sub': 'Southeast Asia'}, {'currency': 'Dong', 'symbol': 'â‚«', 'country': 'Vietnam', 'cc': 'vn', 'sub': 'Southeast Asia'}, {'currency': 'Ringgit', 'symbol': 'RM', 'country': 'Malaysia', 'cc': 'my', 'sub': 'Southeast Asia'}, {'currency': 'Peso', 'symbol': 'â‚±', 'country': 'Philippines', 'cc': 'ph', 'sub': 'Southeast Asia'}, {'currency': 'Pound', 'symbol': 'Â£', 'country': 'United Kingdom', 'cc': 'gb', 'sub': 'Northern Europe'}, {'currency': 'Krone', 'symbol': 'kr', 'country': 'Denmark', 'cc': 'dk', 'sub': 'Northern Europe'}, {'currency': 'Krone', 'symbol': 'kr', 'country': 'Norway', 'cc': 'no', 'sub': 'Northern Europe'}, {'currency': 'Krona', 'symbol': 'kr', 'country': 'Sweden', 'cc': 'se', 'sub': 'Northern Europe'}, {'currency': 'Forint', 'symbol': 'Ft', 'country': 'Hungary', 'cc': 'hu', 'sub': 'Eastern Europe'}, {'currency': 'Zloty', 'symbol': 'zÅ‚', 'country': 'Poland', 'cc': 'pl', 'sub': 'Eastern Europe'}, {'currency': 'Koruna', 'symbol': 'KÄ', 'country': 'Czech Republic', 'cc': 'cz', 'sub': 'Eastern Europe'}, {'currency': 'Hryvnia', 'symbol': 'â‚´', 'country': 'Ukraine', 'cc': 'ua', 'sub': 'Eastern Europe'}, {'currency': 'Leu', 'symbol': 'lei', 'country': 'Romania', 'cc': 'ro', 'sub': 'Eastern Europe'}, {'currency': 'Ruble', 'symbol': 'â‚½', 'country': 'Russia', 'cc': 'ru', 'sub': 'Eastern Europe'}, {'currency': 'Lira', 'symbol': 'â‚º', 'country': 'Turkey', 'cc': 'tr', 'sub': 'Western Asia'}, {'currency': 'Shekel', 'symbol': 'â‚ª', 'country': 'Israel', 'cc': 'il', 'sub': 'Western Asia'}, {'currency': 'Riyal', 'symbol': 'SAR', 'country': 'Saudi Arabia', 'cc': 'sa', 'sub': 'Western Asia'}, {'currency': 'Dirham', 'symbol': 'AED', 'country': 'UAE', 'cc': 'ae', 'sub': 'Western Asia'}, {'currency': 'Dinar', 'symbol': 'RSD', 'country': 'Serbia', 'cc': 'rs', 'sub': 'Southern Europe'}, {'currency': 'Tenge', 'symbol': 'â‚¸', 'country': 'Kazakhstan', 'cc': 'kz', 'sub': 'Central Asia'}, {'currency': 'Real', 'symbol': 'R$', 'country': 'Brazil', 'cc': 'br', 'sub': 'South America'}, {'currency': 'Peso', 'symbol': '$', 'country': 'Mexico', 'cc': 'mx', 'sub': 'Central America'}, {'currency': 'Peso', 'symbol': '$', 'country': 'Argentina', 'cc': 'ar', 'sub': 'South America'}, {'currency': 'Sol', 'symbol': 'S/', 'country': 'Peru', 'cc': 'pe', 'sub': 'South America'}, {'currency': 'Rand', 'symbol': 'R', 'country': 'South Africa', 'cc': 'za', 'sub': 'Southern Africa'}, {'currency': 'Naira', 'symbol': 'â‚¦', 'country': 'Nigeria', 'cc': 'ng', 'sub': 'Western Africa'}, {'currency': 'Birr', 'symbol': 'Br', 'country': 'Ethiopia', 'cc': 'et', 'sub': 'Eastern Africa'}, {'currency': 'Shilling', 'symbol': 'Sh', 'country': 'Kenya', 'cc': 'ke', 'sub': 'Eastern Africa'}, {'currency': 'Pound', 'symbol': 'EÂ£', 'country': 'Egypt', 'cc': 'eg', 'sub': 'Northern Africa'}, {'currency': 'Dirham', 'symbol': 'MAD', 'country': 'Morocco', 'cc': 'ma', 'sub': 'Northern Africa'}]
CUJ = json.dumps(CURRENCIES, separators=(',',':'), ensure_ascii=False)
print('Lifestyle data: Food', len(FOOD), '| Brands', len(BRANDS), '| Currencies', len(CURRENCIES))


# â”€â”€ LICENSE PLATES (Phase 23B) â”€â”€ loaded at runtime via fetch()
import os as _os

# CSS
_css_path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'geoquest_css.txt')
CSS = open(_css_path,'r',encoding='utf-8').read()

# Phase 28 data payloads â€” loaded at runtime via fetch()
print('CSS ready:', len(CSS), 'chars')
# JS TEMPLATE
JS = r'''
/* === BETA FEATURES JS (Phase 157) === */

/* ===== TEIL 1: KENNZEICHEN-BINGO ===== */
function generateBingoGrid() {
  const coll = S.collectedPlates || [];
  const collSet = new Set(coll);

  // Verwende alle verfÃ¼gbaren Kennzeichen (aus Datenbank)
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

  return bingoItems.slice(0, 9); // Nur 9 Zellen fÃ¼r 3x3
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

  const fire = 'ðŸ”¥';
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
html+='<h2>Wahrzeichen & SehenswÃ¼rdigkeiten</h2>';
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
html+='<h2>Welches Land ist grÃ¶ÃŸer?</h2>';
html+='<div style="display:flex;justify-content:space-around;margin:20px 0;">';

// Country A
html+='<div style="flex:1;margin-right:10px;">';
html+='<div style="background:#f0f0f0;padding:20px;border-radius:8px;margin-bottom:10px;">';
html+='<strong>'+countryA.country+'</strong><br>';
html+='<span style="color:#666;font-size:14px;">'+formatMetricDisplay(countryA,'area')+'</span>';
html+='</div>';
html+='<button style="padding:12px;width:100%;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;" data-quiz-type="versus" data-quiz-answer="0">';
html+='GrÃ¶ÃŸer';
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
html+='GrÃ¶ÃŸer';
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
html+='<h2>Welches Land hat mehr NachbarlÃ¤nder?</h2>';
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
html+='<h2>Welches Land hat die lÃ¤ngere KÃ¼stenlinie?</h2>';
html+='<div style="display:flex;justify-content:space-around;margin:20px 0;">';

html+='<div style="flex:1;margin-right:10px;">';
html+='<div style="background:#f0f0f0;padding:20px;border-radius:8px;margin-bottom:10px;">';
html+='<strong>'+countryA.country+'</strong><br>';
html+='<span style="color:#666;font-size:14px;">'+formatAdvancedMetricDisplay(countryA,'coast')+'</span>';
html+='</div>';
html+='<button style="padding:12px;width:100%;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;" data-quiz-type="versus" data-quiz-answer="0">';
html+='LÃ¤nger';
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
html+='LÃ¤nger';
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
html+='<h2>Welches Land hat den hÃ¶heren Gipfel?</h2>';
html+='<div style="display:flex;justify-content:space-around;margin:20px 0;">';

html+='<div style="flex:1;margin-right:10px;">';
html+='<div style="background:#f0f0f0;padding:20px;border-radius:8px;margin-bottom:10px;">';
html+='<strong>'+countryA.country+'</strong><br>';
html+='<span style="color:#666;font-size:14px;">'+formatAdvancedMetricDisplay(countryA,'elevation')+'</span>';
html+='</div>';
html+='<button style="padding:12px;width:100%;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;" data-quiz-type="versus" data-quiz-answer="0">';
html+='HÃ¶her';
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
html+='HÃ¶her';
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
html+='<h2>Welches Land hat das hÃ¶here BIP?</h2>';
html+='<p style="color:#666;font-size:14px;">(BIP pro Kopf)</p>';
html+='<div style="display:flex;justify-content:space-around;margin:20px 0;">';

html+='<div style="flex:1;margin-right:10px;">';
html+='<div style="background:#f0f0f0;padding:20px;border-radius:8px;margin-bottom:10px;">';
html+='<strong>'+countryA.country+'</strong><br>';
html+='<span style="color:#666;font-size:14px;">'+formatAdvancedMetricDisplay(countryA,'gdp')+'</span>';
html+='</div>';
html+='<button style="padding:12px;width:100%;font-size:16px;cursor:pointer;border:2px solid #ccc;border-radius:6px;background:#fff;" data-quiz-type="versus" data-quiz-answer="0">';
html+='HÃ¶her';
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
html+='HÃ¶her';
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
  html += '<p style="font-size:0.9rem;color:var(--text2)">VerfÃ¼gbare Buchstaben:</p>';
  html += '<div class="available-letters">' + lettersHtml + '</div>';
  html += '<input type="text" class="word-generator-input" placeholder="Wort bilden..." />';
  html += '<button onclick="checkWord(this.previousElementSibling.value)" style="width:100%;margin-top:8px">ÃœberprÃ¼fen</button>';
  html += '</div>';

  return html;
}

/* ===== TEIL 2: SIZE GUESSER ===== */
function startSizeGuesserMode() {
  // WÃ¤hle zwei zufÃ¤llige LÃ¤nder
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

/* Helper: Sicherheit fÃ¼r localStorage */
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

/* Fehlerbehandlung fÃ¼r alle Beta-Features */
try {
  // Alle Beta-Features sind mit try/catch geschÃ¼tzt
} catch (e) {
  console.error('[GQ] Beta-Feature Fehler:', e);
}


/* === MAP-MODE TIMER & TRANSLATION (Phase 155) === */

/**
 * Render die Ãœberschrift fÃ¼r Map-Mode mit Ã¼bersetztem LÃ¤nder-Namen
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

  // Render den Titel mit Ã¼bersetztem Land
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
 * Patch der Haupt-Timer-Funktion um Map-Mode zu unterstÃ¼tzen
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
 * Ersetze die alte tick()-Logik fÃ¼r Map-Mode
 * Diese Funktion wird vom Haupt-Render() aufgerufen
 */
const oldTick = typeof tick !== 'undefined' ? tick : null;

function tick() {
  if (oldTick) oldTick();

  // ZusÃ¤tzliche Map-Mode-spezifische Updates
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
 * Zeige das Popup fÃ¼r ein Land mit Ã¼bersetztem Titel
 * @param {string} cc - Country Code (z.B. "DE")
 * @param {string} name - Country Name (z.B. "Germany")
 * @param {number} x - X-Position fÃ¼r Popup
 * @param {number} y - Y-Position fÃ¼r Popup
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

  // Entferne Popup nach 5 Sekunden oder bei Click auÃŸerhalb
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
 * Initialisiere alle Karten-Marker mit Ãœbersetzungen
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

  // Setze initiale 'found'-Klassen fÃ¼r alle gesammelten LÃ¤nder
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
 * Extrahiere Country Code aus Kennzeichen-Key (z.B. "DE::CODE" â†’ "DE")
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
/* ADMIN_EMAIL removed â€” use Supabase trigger instead */

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
/* â”€â”€ Phase 47/48: i18n â€” DE / EN / PL â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
const LANG={
de:{
  play:"SPIELEN",again:"NOCHMAL",menu:"HauptmenÃ¼",board:"Bestenliste",pass:"Reisepass",
  profile:"Profil",stats:"Statistik",casual:"Casual",hardcore:"Hardcore",rounds:"Runden",
  btn_collect:"Sammeln",btn_back:"ZurÃ¼ck zum HauptmenÃ¼",btn_next:"Weiter â†’",
  btn_again:"Nochmal",btn_menu:"HauptmenÃ¼",btn_adapt:"Anpassen",
  spotter_title:"\u{1F697} Roadtrip-Spotter",
  spotter_hint:"Kennzeichen gesehen? Sofort eintragen!",
  spotter_all:"Alle LÃ¤nder",spotter_unknown:"Unbekanntes Kennzeichen",
  spotter_not_in:"nicht in",spotter_but_in:"aber in",spotter_no_region:"hat keine Regionen â€” gib \"{code}\" ein\!",
  album_title:"\u{1F4D4} Kennzeichen-Album",album_list:"\u{1F4DD} Liste",album_map:"\u{1F5FA} Karte",
  album_empty_country:"Noch nichts aus {country} gesammelt â€” nutze den Spotter!",
  album_empty:"Noch nichts gesammelt!\nSpiele EU-Kennzeichen oder benutze den Spotter.",
  album_codes:"KÃ¼rzel",
  hl_higher:"â¬†ï¸ Mehr / LÃ¤nger / GrÃ¶ÃŸer",hl_lower:"â¬‡ï¸ Weniger / KÃ¼rzer / Kleiner",
  hl_more:"â¬†ï¸ Mehr Einwohner",hl_less:"â¬‡ï¸ Weniger Einwohner",
  hl_longer:"â¬†ï¸ LÃ¤nger",hl_shorter:"â¬‡ï¸ KÃ¼rzer",hl_bigger:"â¬†ï¸ GrÃ¶ÃŸer (FlÃ¤che)",hl_smaller:"â¬‡ï¸ Kleiner (FlÃ¤che)",
  loc_detected:"Du bist in {country}",loc_adapt:"Anpassen",
  q_city:"In welchem Land liegt diese Stadt?",q_flag:"Welches Land zeigt diese Flagge?",
  q_capital:"Zu welchem Land gehÃ¶rt diese Hauptstadt?",q_river:"In welchem Land liegt dieser Fluss?",
  q_landmark:"In welchem Land liegt dieses Wahrzeichen?",q_park:"In welchem Land liegt dieser Nationalpark?",
  q_unesco:"In welchem Land liegt dieses UNESCO-Welterbe?",q_citymark:"Zu welcher Stadt gehÃ¶rt dieses Wahrzeichen?",
  q_subway:"In welcher Stadt ist diese U-Bahn?",q_flagsel:"Welche Flagge gehÃ¶rt zu â€¦",
  q_rcapital:"Was ist die Hauptstadt von â€¦?",q_rcity:"Welche Stadt liegt in â€¦?",
  q_rriver:"Welcher Fluss flieÃŸt durch â€¦?",q_outline:"Welches Land hat diese Form?",
  q_food:"Aus welchem Land kommt dieses Gericht?",q_brand:"Aus welchem Land kommt diese Marke?",
  q_currency:"Zu welchem Land gehÃ¶rt diese WÃ¤hrung?",q_curr_real:"Welche WÃ¤hrung hat â€¦",
  q_pop_compare:"Mehr oder weniger Einwohner?",
  q_hl_pop:"Mehr Einwohner als {a}?",q_hl_river:"LÃ¤nger als {a}?",q_hl_area:"GrÃ¶ÃŸer als {a}?",
  q_neighbor:"Welches Land grenzt anâ€¦?",q_neighbor_not:"Grenzt NICHT anâ€¦?",
  q_plates_casual:"Woher kommt dieses Kennzeichen?",q_plates_hard:"Region erkennen â€” kein Tipp!",
  q_river_real:"Durch welches Land flieÃŸt dieser Fluss?",q_map_guess:"Finde das Land auf der Karte",
  fb_correct:"âœ“ Richtig! +{pts}",fb_wrong:"âœ— Falsch â†’ {ans}",fb_time:"â± Zeit! â†’ {ans}",
  plates_more:"+{n} weitere",pct_complete:"{pct}% vollstÃ¤ndig",
  spotter_dup:"ðŸ“‹ {code} ({country}) bereits gesammelt!",
  map_unavail:"Karte nicht verfÃ¼gbar",map_loading:"Kartendaten werden geladenâ€¦",
  q_subway_km:"Wie lang ist das U-Bahn-Netz â€¦ (km)?",q_subway_lines:"Wie viele U-Bahn-Linien hat â€¦?",
  ob_welcome:"Willkommen bei GeoQuest",ob_sub1:"Das Geografie-Quiz â€” sammle Stempel, steige in der Liga auf!",ob_difficulty:"Schwierigkeitsgrad",ob_diff_sub:"W\u00e4hle deinen Stil. \u00c4nderbar jederzeit.",
  ob_diff_casual_desc:"Gro\u00dfe St\u00e4dte \u2022 12 Sek.",ob_diff_hc_desc:"Alle St\u00e4dte \u2022 8 Sek.",ob_back:"\u2190 Zur\u00fcck",ob_modes_title:"Spielmodi",
  ob_modes_sub:"19 Modi, ein Ziel: Die Welt kennenlernen.",ob_more_modes:"\u2026 und 16 weitere Modi",ob_start:"\u{1F680} Los geht's!",ob_have_account:"Ich habe bereits einen Account",ob_register:"Neu hier? Registrieren",
  home_hi:"Hallo, {name} \u{1F44B}",home_guest:"Willkommen, Gast \u{1F30D}",home_save:"\u{1F510} Fortschritt sichern",home_pvp_sub:"Echtzeit gegen einen Freund spielen",
  ob_mode1_name:"Stadt â†’ Land",ob_mode1_desc:"Welchem Land gehÃ¶rt diese Stadt?",ob_mode2_name:"EU-Kennzeichen",ob_mode2_desc:"Woher kommt dieses Kennzeichen?",ob_mode3_name:"U-Bahn-Netz",ob_mode3_desc:"Linien und km der Metros.",
  language_select:"SPRACHE",
  badge_beta:"Beta",beta_warning:"Spielbar, aber es k\u00f6nnen noch Fehler auftreten.",
  rotate_device:"Bitte drehe dein Ger\u00e4t ins Querformat \u{1F4F1}\u27A1\u{1F5FA}",
  diff_desc_casual:"\u{1F7E2} Casual: Entspannt \u00b7 Kein Zeitlimit \u00b7 \u221e Leben",diff_desc_hc:"\u{1F525} Hardcore: Der Klassiker \u00b7 Kein Zeitlimit \u00b7 3 Leben",diff_desc_surv:"\u{1F480} Survival: Gegen die Uhr \u00b7 8 Sekunden \u00b7 3 Leben",
  hud_lives:"LEBEN",score_mult_max:"Max-Multiplikator",score_time_bonus:"Zeit-Bonus",pts_abbr:"Pkt.",score_correct_lbl:"richtig",mode_wappen:"Wappen-Meister",mode_slf:"Land & Hauptstadt",mode_euro:"Euro-M\u00fcnzen"
},
en:{
  play:"PLAY",again:"PLAY AGAIN",menu:"Main Menu",board:"Leaderboard",pass:"Passport",
  profile:"Profile",stats:"Stats",casual:"Casual",hardcore:"Hardcore",rounds:"Rounds",
  btn_collect:"Collect",btn_back:"Back to Main Menu",btn_next:"Next â†’",
  btn_again:"Play Again",btn_menu:"Main Menu",btn_adapt:"Adapt",
  spotter_title:"\u{1F697} Road Trip Spotter",
  spotter_hint:"Spotted a plate? Log it now!",
  spotter_all:"All Countries",spotter_unknown:"Unknown plate",
  spotter_not_in:"not in",spotter_but_in:"but found in",spotter_no_region:"has no regions â€” enter \"{code}\" to collect\!",
  album_title:"\u{1F4D4} Plate Collection",album_list:"\u{1F4DD} List",album_map:"\u{1F5FA} Map",
  album_empty_country:"Nothing from {country} yet â€” use the Spotter!",
  album_empty:"Nothing collected yet!\nPlay EU plates or use the Spotter above.",
  album_codes:"codes",
  hl_higher:"â¬†ï¸ More / Longer / Larger",hl_lower:"â¬‡ï¸ Less / Shorter / Smaller",
  hl_more:"â¬†ï¸ More Population",hl_less:"â¬‡ï¸ Less Population",
  hl_longer:"â¬†ï¸ Longer",hl_shorter:"â¬‡ï¸ Shorter",hl_bigger:"â¬†ï¸ Larger (Area)",hl_smaller:"â¬‡ï¸ Smaller (Area)",
  loc_detected:"You are in {country}",loc_adapt:"Adapt",
  q_city:"In which country is this city?",q_flag:"Which country does this flag belong to?",
  q_capital:"Which country has this capital?",q_river:"In which country is this river?",
  q_landmark:"In which country is this landmark?",q_park:"In which country is this national park?",
  q_unesco:"In which country is this UNESCO site?",q_citymark:"Which city has this landmark?",
  q_subway:"Which city has this metro?",q_flagsel:"Which flag belongs toâ€¦",
  q_rcapital:"What is the capital ofâ€¦?",q_rcity:"Which city is inâ€¦?",
  q_rriver:"Which river flows throughâ€¦?",q_outline:"Which country has this shape?",
  q_food:"Which country does this dish come from?",q_brand:"Which country does this brand come from?",
  q_currency:"Which country uses this currency?",q_curr_real:"What currency doesâ€¦",
  q_pop_compare:"More or fewer inhabitants?",
  q_hl_pop:"More inhabitants than {a}?",q_hl_river:"Longer than {a}?",q_hl_area:"Larger than {a}?",
  q_neighbor:"Which country bordersâ€¦?",q_neighbor_not:"Does NOT borderâ€¦?",
  q_plates_casual:"Which country has this plate?",q_plates_hard:"Identify the region â€” no hint!",
  q_river_real:"Which country does this river flow through?",q_map_guess:"Find the country on the map",
  fb_correct:"âœ“ Correct! +{pts}",fb_wrong:"âœ— Wrong â†’ {ans}",fb_time:"â± Time! â†’ {ans}",
  plates_more:"+{n} more",pct_complete:"{pct}% complete",
  spotter_dup:"ðŸ“‹ {code} ({country}) already collected!",
  map_unavail:"Map not available",map_loading:"Loading map dataâ€¦",
  q_subway_km:"How long is the metro network â€¦ (km)?",q_subway_lines:"How many metro lines does â€¦ have?",
  ob_welcome:"Welcome to GeoQuest",ob_sub1:"The geography quiz â€” collect stamps, climb the league!",ob_difficulty:"Difficulty",ob_diff_sub:"Choose your style. Changeable at any time.",
  ob_diff_casual_desc:"Major cities \u2022 12 sec.",ob_diff_hc_desc:"All cities \u2022 8 sec.",ob_back:"\u2190 Back",ob_modes_title:"Game Modes",
  ob_modes_sub:"19 modes, one goal: know the world.",ob_more_modes:"\u2026 and 16 more modes",ob_start:"\u{1F680} Let's go!",ob_have_account:"I already have an account",ob_register:"New here? Register",
  home_hi:"Hi, {name} \u{1F44B}",home_guest:"Welcome, Guest \u{1F30D}",home_save:"\u{1F510} Save progress",home_pvp_sub:"Play in real time against a friend",
  ob_mode1_name:"City â†’ Country",ob_mode1_desc:"Which country does this city belong to?",ob_mode2_name:"EU Licence Plates",ob_mode2_desc:"Where does this number plate come from?",ob_mode3_name:"Metro Networks",ob_mode3_desc:"Lines and km of metro systems.",
  language_select:"LANGUAGE",
  badge_beta:"Beta",beta_warning:"Playable, but may still contain bugs.",
  rotate_device:"Please rotate your device to landscape mode \u{1F4F1}\u27A1\u{1F5FA}",
  diff_desc_casual:"\u{1F7E2} Casual: Relaxed \u00b7 No time limit \u00b7 \u221e Lives",diff_desc_hc:"\u{1F525} Hardcore: Classic \u00b7 No time limit \u00b7 3 Lives",diff_desc_surv:"\u{1F480} Survival: Against the clock \u00b7 8s \u00b7 3 Lives",
  hud_lives:"LIVES",score_mult_max:"Max Multiplier",score_time_bonus:"Time Bonus",pts_abbr:"pts.",score_correct_lbl:"correct",mode_wappen:"Coat of Arms",mode_slf:"City-Country-River",mode_euro:"Euro Coins"
},
pl:{
  play:"GRAJ",again:"ZAGRAJ PONOWNIE",menu:"Menu",board:"Ranking",pass:"Paszport",
  profile:"Profil",stats:"Statystyki",casual:"ZwykÅ‚y",hardcore:"Trudny",rounds:"Rundy",
  btn_collect:"Zbierz",btn_back:"PowrÃ³t do menu",btn_next:"Dalej â†’",
  btn_again:"Zagraj ponownie",btn_menu:"Menu",btn_adapt:"Dostosuj",
  spotter_title:"\u{1F697} Spotter PodrÃ³Å¼nika",
  spotter_hint:"Widzisz tablicÄ™? Zapisz jÄ… od razu!",
  spotter_all:"Wszystkie kraje",spotter_unknown:"Nieznana tablica",
  spotter_not_in:"nie ma w",spotter_but_in:"ale jest w",
  album_title:"\u{1F4D4} Album Tablic",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Mapa",
  album_empty_country:"Nic z {country} jeszcze â€” uÅ¼yj Spottera!",
  album_empty:"Nic jeszcze nie zebrano!\nGraj w tablice EU lub uÅ¼yj Spottera.",
  album_codes:"kodÃ³w",
  hl_higher:"â¬†ï¸ WiÄ™cej / DÅ‚uÅ¼ej / WiÄ™kszy",hl_lower:"â¬‡ï¸ Mniej / KrÃ³cej / Mniejszy",
  hl_more:"â¬†ï¸ WiÄ™cej mieszkaÅ„cÃ³w",hl_less:"â¬‡ï¸ Mniej mieszkaÅ„cÃ³w",
  loc_detected:"JesteÅ› w {country}",loc_adapt:"Dostosuj",
  q_city:"W jakim kraju leÅ¼y to miasto?",q_flag:"Jakie paÅ„stwo ma tÄ™ flagÄ™?",
  q_capital:"Do jakiego kraju naleÅ¼y ta stolica?",q_river:"W jakim kraju pÅ‚ynie ta rzeka?",
  q_landmark:"W jakim kraju jest ta atrakcja?",q_park:"W jakim kraju jest ten park narodowy?",
  q_unesco:"W jakim kraju jest to dziedzictwo UNESCO?",q_citymark:"Do jakiego miasta naleÅ¼y ta atrakcja?",
  q_subway:"W jakim mieÅ›cie jest to metro?",q_flagsel:"KtÃ³ra flaga naleÅ¼y doâ€¦",
  q_rcapital:"Jaka jest stolica â€¦?",q_rcity:"KtÃ³re miasto leÅ¼y w â€¦?",
  q_rriver:"KtÃ³ra rzeka pÅ‚ynie przez â€¦?",q_outline:"KtÃ³re paÅ„stwo ma ten ksztaÅ‚t?",
  q_food:"Z jakiego kraju pochodzi to danie?",q_brand:"Z jakiego kraju pochodzi ta marka?",
  q_currency:"Do jakiego kraju naleÅ¼y ta waluta?",q_curr_real:"JakÄ… walutÄ™ maâ€¦",
  q_pop_compare:"WiÄ™cej czy mniej mieszkaÅ„cÃ³w?",
  q_hl_pop:"WiÄ™cej mieszkaÅ„cÃ³w niÅ¼ {a}?",q_hl_river:"DÅ‚uÅ¼sza niÅ¼ {a}?",q_hl_area:"WiÄ™kszy niÅ¼ {a}?",
  q_neighbor:"KtÃ³ry kraj graniczy zâ€¦?",q_neighbor_not:"NIE graniczy zâ€¦?",
  q_plates_casual:"Do jakiego kraju naleÅ¼y ta tablica?",q_plates_hard:"Jaki region ma tÄ™ tablicÄ™?",
  q_river_real:"Przez jaki kraj pÅ‚ynie ta rzeka?",q_map_guess:"ZnajdÅº kraj na mapie",
  fb_correct:"âœ“ Dobrze! +{pts}",fb_wrong:"âœ— BÅ‚Ä…d â†’ {ans}",fb_time:"â± Czas! â†’ {ans}",
  plates_more:"+{n} wiÄ™cej",pct_complete:"{pct}% ukoÅ„czono",
  spotter_dup:"ðŸ“‹ {code} ({country}) juÅ¼ zebrane!",
  map_unavail:"Mapa niedostÄ™pna",map_loading:"Åadowanie mapyâ€¦",
  q_subway_km:"Jak dÅ‚uga jest sieÄ‡ metra â€¦ (km)?",q_subway_lines:"Ile linii metra ma â€¦?",
  hl_longer:"â¬†ï¸ DÅ‚uÅ¼szy",hl_shorter:"â¬‡ï¸ KrÃ³tszy",hl_bigger:"â¬†ï¸ WiÄ™kszy (obszar)",hl_smaller:"â¬‡ï¸ Mniejszy (obszar)",
  ob_welcome:"Witaj w GeoQuest",ob_sub1:"Quiz geograficzny â€” zbieraj stemple, awansuj w lidze!",ob_difficulty:"Poziom trudnoÅ›ci",ob_diff_sub:"Wybierz swÃ³j styl. ZmieÅ„ w dowolnym momencie.",
  ob_diff_casual_desc:"DuÅ¼e miasta â€¢ 12 sek.",ob_diff_hc_desc:"Wszystkie miasta â€¢ 8 sek.",ob_back:"â† WrÃ³Ä‡",ob_modes_title:"Tryby gry",
  ob_modes_sub:"19 trybÃ³w, jeden cel: poznaÄ‡ Å›wiat.",ob_more_modes:"â€¦ i 16 kolejnych trybÃ³w",ob_start:"\u{1F680} Zaczynamy!",ob_have_account:"Mam juÅ¼ konto",ob_register:"Nowy? Zarejestruj siÄ™",
  home_hi:"CzeÅ›Ä‡, {name} \u{1F44B}",home_guest:"Witaj, GoÅ›ciu \u{1F30D}",home_save:"\u{1F510} Zapisz postÄ™p",home_pvp_sub:"Graj w czasie rzeczywistym z przyjacielem",
  ob_mode1_name:"Miasto â†’ Kraj",ob_mode1_desc:"Do jakiego kraju naleÅ¼y to miasto?",ob_mode2_name:"Tablice UE",ob_mode2_desc:"SkÄ…d pochodzi ta tablica?",ob_mode3_name:"Sieci metra",ob_mode3_desc:"Linie i km metra.",
  language_select:"JÄ˜ZYK",
  badge_beta:"Beta",beta_warning:"Grywalny, ale mogÄ… wystÄ…piÄ‡ bÅ‚Ä™dy.",
  rotate_device:"ObrÃ³Ä‡ urzÄ…dzenie poziomo \u{1F4F1}\u27A1\u{1F5FA}",
  diff_desc_casual:"\u{1F7E2} Casual: Relaks Â· Bez limitu czasu Â· âˆž Å¼ycia",
  diff_desc_hc:"\u{1F525} Hardcore: Klasyk Â· Bez limitu czasu Â· 3 Å»ycia",
  diff_desc_surv:"\u{1F480} Survival: Na czas Â· 8 sekund Â· 3 Å¼ycia",
  hud_lives:"Å»YCIA",
  score_mult_max:"Maks MnoÅ¼nik",
  score_time_bonus:"Bonus Czasu",
  pts_abbr:"pkt.",
  score_correct_lbl:"poprawnie",
  mode_wappen:"Herby",
  mode_slf:"Miasto-Kraj-Rzeka",
  mode_euro:"Monety Euro"
},
fr:{
  play:"JOUER",again:"REJOUER",menu:"Menu principal",board:"Classement",pass:"Passeport",
  profile:"Profil",stats:"Statistiques",casual:"Casual",hardcore:"Hardcore",rounds:"Manches",
  btn_collect:"Collecter",btn_back:"Retour au menu",btn_next:"Suivant â†’",
  btn_again:"Rejouer",btn_menu:"Menu principal",btn_adapt:"Adapter",
  spotter_title:"\u{1F697} Spotter de voyage",
  spotter_hint:"Vu une plaque ? Notez-la !",
  spotter_all:"Tous les pays",spotter_unknown:"Plaque inconnue",
  spotter_not_in:"pas dans",spotter_but_in:"mais dans",
  album_title:"\u{1F4D4} Collection de plaques",album_list:"\u{1F4DD} Liste",album_map:"\u{1F5FA} Carte",
  album_empty_country:"Rien de {country} encore â€” utilisez le Spotter !",
  album_empty:"Rien collectÃ© encore !\nJouez aux plaques UE ou utilisez le Spotter.",
  album_codes:"codes",
  hl_higher:"â¬†ï¸ Plus / Plus long / Plus grand",hl_lower:"â¬‡ï¸ Moins / Plus court / Plus petit",
  hl_more:"â¬†ï¸ Plus d'habitants",hl_less:"â¬‡ï¸ Moins d'habitants",
  loc_detected:"Vous Ãªtes en {country}",loc_adapt:"Adapter",
  q_city:"Dans quel pays se trouve cette ville ?",q_flag:"Quel pays a ce drapeau ?",
  q_capital:"Ã€ quel pays appartient cette capitale ?",q_river:"Dans quel pays coule ce fleuve ?",
  q_landmark:"Dans quel pays se trouve ce monument ?",q_park:"Dans quel pays se trouve ce parc national ?",
  q_unesco:"Dans quel pays se trouve ce site UNESCO ?",q_citymark:"Ã€ quelle ville appartient ce monument ?",
  q_subway:"Dans quelle ville se trouve ce mÃ©tro ?",q_flagsel:"Quel drapeau appartient Ã â€¦",
  q_rcapital:"Quelle est la capitale deâ€¦ ?",q_rcity:"Quelle ville est dansâ€¦ ?",
  q_rriver:"Quel fleuve traverseâ€¦ ?",q_outline:"Quel pays a cette forme ?",
  q_food:"De quel pays vient ce plat ?",q_brand:"De quel pays vient cette marque ?",
  q_currency:"Ã€ quel pays appartient cette monnaie ?",q_curr_real:"Quelle monnaie aâ€¦",
  q_pop_compare:"Plus ou moins d'habitants ?",
  q_hl_pop:"Plus d'habitants que {a} ?",q_hl_river:"Plus long que {a} ?",q_hl_area:"Plus grand que {a} ?",
  q_neighbor:"Quel pays bordeâ€¦ ?",q_neighbor_not:"Ne borde PASâ€¦ ?",
  q_plates_casual:"De quel pays est cette plaque ?",q_plates_hard:"Identifier la rÃ©gion â€” aucun indice !",
  q_river_real:"Dans quel pays coule ce fleuve ?",q_map_guess:"Trouver le pays sur la carte",
  fb_correct:"âœ“ Correct ! +{pts}",fb_wrong:"âœ— Faux â†’ {ans}",fb_time:"â± Temps ! â†’ {ans}",
  plates_more:"+{n} de plus",pct_complete:"{pct}% terminÃ©",
  spotter_dup:"ðŸ“‹ {code} ({country}) dÃ©jÃ  collectÃ© !",
  map_unavail:"Carte non disponible",map_loading:"Chargement de la carteâ€¦",
  q_subway_km:"Quelle longueur a le rÃ©seau mÃ©tro â€¦ (km)?",q_subway_lines:"Combien de lignes de mÃ©tro a â€¦ ?",
  hl_longer:"â¬†ï¸ Plus long",hl_shorter:"â¬‡ï¸ Plus court",hl_bigger:"â¬†ï¸ Plus grand (superficie)",hl_smaller:"â¬‡ï¸ Plus petit (superficie)",
  ob_welcome:"Bienvenue sur GeoQuest",ob_sub1:"Le quiz de gÃ©ographie â€” collectez des tampons, montez en ligueÂ !",ob_difficulty:"Niveau de difficultÃ©",ob_diff_sub:"Choisissez votre style. Modifiable Ã  tout moment.",
  ob_diff_casual_desc:"Grandes villes â€¢ 12 sec.",ob_diff_hc_desc:"Toutes les villes â€¢ 8 sec.",ob_back:"â† Retour",ob_modes_title:"Modes de jeu",
  ob_modes_sub:"19 modes, un objectifÂ : connaÃ®tre le monde.",ob_more_modes:"â€¦ et 16 autres modes",ob_start:"\u{1F680} C'est partiÂ !",ob_have_account:"J'ai dÃ©jÃ  un compte",ob_register:"NouveauÂ ? S'inscrire",
  home_hi:"Salut, {name} \u{1F44B}",home_guest:"Bienvenue, invitÃ© \u{1F30D}",home_save:"\u{1F510} Sauvegarder la progression",home_pvp_sub:"Jouer en temps rÃ©el contre un ami",
  ob_mode1_name:"Ville â†’ Pays",ob_mode1_desc:"Ã€ quel pays appartient cette villeÂ ?",ob_mode2_name:"Plaques UE",ob_mode2_desc:"D'oÃ¹ vient cette plaqueÂ ?",ob_mode3_name:"RÃ©seaux de mÃ©tro",ob_mode3_desc:"Lignes et km des mÃ©tros.",
  language_select:"LANGUE",
  badge_beta:"B\u00eata",beta_warning:"Jouable, mais peut contenir des bugs.",
  rotate_device:"Veuillez faire pivoter votre appareil \u{1F4F1}\u27A1\u{1F5FA}",
  diff_desc_casual:"\u{1F7E2} Casual: DÃ©tendu Â· Sans limite de temps Â· âˆž Vies",
  diff_desc_hc:"\u{1F525} Hardcore: Classique Â· Sans limite de temps Â· 3 Vies",
  diff_desc_surv:"\u{1F480} Survival: Contre la montre Â· 8s Â· 3 Vies",
  hud_lives:"VIES",
  score_mult_max:"Multiplicateur Max",
  score_time_bonus:"Bonus Temps",
  pts_abbr:"pts.",
  score_correct_lbl:"correct",
  mode_wappen:"Armoiries",
  mode_slf:"Ville-Pays-Fleuve",
  mode_euro:"PiÃ¨ces Euro"
},
es:{
  play:"JUGAR",again:"JUGAR DE NUEVO",menu:"MenÃº principal",board:"ClasificaciÃ³n",pass:"Pasaporte",
  profile:"Perfil",stats:"EstadÃ­sticas",casual:"Casual",hardcore:"Hardcore",rounds:"Rondas",
  btn_collect:"Coleccionar",btn_back:"Volver al menÃº",btn_next:"Siguiente â†’",
  btn_again:"Jugar de nuevo",btn_menu:"MenÃº principal",btn_adapt:"Adaptar",
  spotter_title:"\u{1F697} Spotter de viaje",
  spotter_hint:"Â¿Has visto una matrÃ­cula? Â¡AnÃ³tala!",
  spotter_all:"Todos los paÃ­ses",spotter_unknown:"MatrÃ­cula desconocida",
  spotter_not_in:"no en",spotter_but_in:"pero en",
  album_title:"\u{1F4D4} ColecciÃ³n de matrÃ­culas",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Mapa",
  album_empty_country:"Nada de {country} aÃºn â€” Â¡usa el Spotter!",
  album_empty:"Â¡Nada recopilado aÃºn!\nJuega a matrÃ­culas UE o usa el Spotter.",
  album_codes:"cÃ³digos",
  hl_higher:"â¬†ï¸ MÃ¡s / MÃ¡s largo / MÃ¡s grande",hl_lower:"â¬‡ï¸ Menos / MÃ¡s corto / MÃ¡s pequeÃ±o",
  hl_more:"â¬†ï¸ MÃ¡s habitantes",hl_less:"â¬‡ï¸ Menos habitantes",
  loc_detected:"EstÃ¡s en {country}",loc_adapt:"Adaptar",
  q_city:"Â¿En quÃ© paÃ­s estÃ¡ esta ciudad?",q_flag:"Â¿QuÃ© paÃ­s tiene esta bandera?",
  q_capital:"Â¿A quÃ© paÃ­s pertenece esta capital?",q_river:"Â¿En quÃ© paÃ­s estÃ¡ este rÃ­o?",
  q_landmark:"Â¿En quÃ© paÃ­s estÃ¡ este monumento?",q_park:"Â¿En quÃ© paÃ­s estÃ¡ este parque nacional?",
  q_unesco:"Â¿En quÃ© paÃ­s estÃ¡ este sitio UNESCO?",q_citymark:"Â¿A quÃ© ciudad pertenece este monumento?",
  q_subway:"Â¿En quÃ© ciudad estÃ¡ este metro?",q_flagsel:"Â¿QuÃ© bandera pertenece aâ€¦",
  q_rcapital:"Â¿CuÃ¡l es la capital deâ€¦?",q_rcity:"Â¿QuÃ© ciudad estÃ¡ enâ€¦?",
  q_rriver:"Â¿QuÃ© rÃ­o atraviesaâ€¦?",q_outline:"Â¿QuÃ© paÃ­s tiene esta forma?",
  q_food:"Â¿De quÃ© paÃ­s viene este plato?",q_brand:"Â¿De quÃ© paÃ­s viene esta marca?",
  q_currency:"Â¿A quÃ© paÃ­s pertenece esta moneda?",q_curr_real:"Â¿QuÃ© moneda tieneâ€¦",
  q_pop_compare:"Â¿MÃ¡s o menos habitantes?",
  q_hl_pop:"Â¿MÃ¡s habitantes que {a}?",q_hl_river:"Â¿MÃ¡s largo que {a}?",q_hl_area:"Â¿MÃ¡s grande que {a}?",
  q_neighbor:"Â¿QuÃ© paÃ­s limita conâ€¦?",q_neighbor_not:"Â¿NO limita conâ€¦?",
  q_plates_casual:"Â¿De quÃ© paÃ­s es esta matrÃ­cula?",q_plates_hard:"Identificar la regiÃ³n â€” Â¡sin pista!",
  q_river_real:"Â¿Por quÃ© paÃ­s pasa este rÃ­o?",q_map_guess:"Encuentra el paÃ­s en el mapa",
  fb_correct:"âœ“ Â¡Correcto! +{pts}",fb_wrong:"âœ— Incorrecto â†’ {ans}",fb_time:"â± Â¡Tiempo! â†’ {ans}",
  plates_more:"+{n} mÃ¡s",pct_complete:"{pct}% completado",
  spotter_dup:"ðŸ“‹ {code} ({country}) ya coleccionado!",
  map_unavail:"Mapa no disponible",map_loading:"Cargando mapaâ€¦",
  q_subway_km:"Â¿CuÃ¡nto mide la red de metro â€¦ (km)?",q_subway_lines:"Â¿CuÃ¡ntas lÃ­neas de metro tiene â€¦?",
  hl_longer:"â¬†ï¸ MÃ¡s largo",hl_shorter:"â¬‡ï¸ MÃ¡s corto",hl_bigger:"â¬†ï¸ MÃ¡s grande (Ã¡rea)",hl_smaller:"â¬‡ï¸ MÃ¡s pequeÃ±o (Ã¡rea)",
  ob_welcome:"Bienvenido a GeoQuest",ob_sub1:"El quiz de geografÃ­a â€” colecciona sellos, sube en la liga.",ob_difficulty:"Nivel de dificultad",ob_diff_sub:"Elige tu estilo. Cambiable en cualquier momento.",
  ob_diff_casual_desc:"Ciudades grandes â€¢ 12 seg.",ob_diff_hc_desc:"Todas las ciudades â€¢ 8 seg.",ob_back:"â† Volver",ob_modes_title:"Modos de juego",
  ob_modes_sub:"19 modos, un objetivo: conocer el mundo.",ob_more_modes:"â€¦ y 16 modos mÃ¡s",ob_start:"\u{1F680} Â¡Vamos!",ob_have_account:"Ya tengo una cuenta",ob_register:"Â¿Nuevo? RegsÃ­strate",
  home_hi:"Hola, {name} \u{1F44B}",home_guest:"Bienvenido, invitado \u{1F30D}",home_save:"\u{1F510} Guardar progreso",home_pvp_sub:"Jugar en tiempo real contra un amigo",
  ob_mode1_name:"Ciudad â†’ PaÃ­s",ob_mode1_desc:"Â¿A quÃ© paÃ­s pertenece esta ciudad?",ob_mode2_name:"MatrÃ­culas UE",ob_mode2_desc:"Â¿De dÃ³nde viene esta matrÃ­cula?",ob_mode3_name:"Redes de metro",ob_mode3_desc:"LÃ­neas y km de los metros.",
  language_select:"IDIOMA",
  badge_beta:"Beta",beta_warning:"Jugable, pero puede contener errores.",
  rotate_device:"Por favor, gira tu dispositivo al modo horizontal \u{1F4F1}\u27A1\u{1F5FA}",
  diff_desc_casual:"\u{1F7E2} Casual: Relajado Â· Sin lÃ­mite Â· âˆž Vidas",
  diff_desc_hc:"\u{1F525} Hardcore: ClÃ¡sico Â· Sin lÃ­mite Â· 3 Vidas",
  diff_desc_surv:"\u{1F480} Survival: Contrarreloj Â· 8s Â· 3 Vidas",
  hud_lives:"VIDAS",
  score_mult_max:"Multiplicador MÃ¡x.",
  score_time_bonus:"Bono de Tiempo",
  pts_abbr:"pts.",
  score_correct_lbl:"correctas",
  mode_wappen:"Escudos",
  mode_slf:"Ciudad-PaÃ­s-RÃ­o",
  mode_euro:"Monedas Euro"
},
it:{
  play:"GIOCA",again:"GIOCA ANCORA",menu:"Menu principale",board:"Classifica",pass:"Passaporto",
  profile:"Profilo",stats:"Statistiche",casual:"Casual",hardcore:"Hardcore",rounds:"Round",
  btn_collect:"Colleziona",btn_back:"Torna al menu",btn_next:"Avanti â†’",
  btn_again:"Gioca ancora",btn_menu:"Menu principale",btn_adapt:"Adatta",
  spotter_title:"\u{1F697} Spotter di viaggio",
  spotter_hint:"Hai visto una targa? Registrala subito!",
  spotter_all:"Tutti i paesi",spotter_unknown:"Targa sconosciuta",
  spotter_not_in:"non in",spotter_but_in:"ma in",
  album_title:"\u{1F4D4} Raccolta targhe",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Mappa",
  album_empty_country:"Niente da {country} ancora â€” usa lo Spotter!",
  album_empty:"Niente ancora raccolto!\nGioca alle targhe UE o usa lo Spotter.",
  album_codes:"codici",
  hl_higher:"â¬†ï¸ Di piÃ¹ / PiÃ¹ lungo / PiÃ¹ grande",hl_lower:"â¬‡ï¸ Di meno / PiÃ¹ corto / PiÃ¹ piccolo",
  hl_more:"â¬†ï¸ PiÃ¹ abitanti",hl_less:"â¬‡ï¸ Meno abitanti",
  loc_detected:"Sei in {country}",loc_adapt:"Adatta",
  q_city:"In quale paese si trova questa cittÃ ?",q_flag:"Quale paese ha questa bandiera?",
  q_capital:"A quale paese appartiene questa capitale?",q_river:"In quale paese scorre questo fiume?",
  q_landmark:"In quale paese si trova questo monumento?",q_park:"In quale paese si trova questo parco nazionale?",
  q_unesco:"In quale paese si trova questo sito UNESCO?",q_citymark:"A quale cittÃ  appartiene questo monumento?",
  q_subway:"In quale cittÃ  si trova questa metro?",q_flagsel:"Quale bandiera appartiene aâ€¦",
  q_rcapital:"Qual Ã¨ la capitale diâ€¦?",q_rcity:"Quale cittÃ  si trova inâ€¦?",
  q_rriver:"Quale fiume scorre attraversoâ€¦?",q_outline:"Quale paese ha questa forma?",
  q_food:"Da quale paese viene questo piatto?",q_brand:"Da quale paese viene questo marchio?",
  q_currency:"A quale paese appartiene questa valuta?",q_curr_real:"Quale valuta haâ€¦",
  q_pop_compare:"PiÃ¹ o meno abitanti?",
  q_hl_pop:"PiÃ¹ abitanti di {a}?",q_hl_river:"PiÃ¹ lungo di {a}?",q_hl_area:"PiÃ¹ grande di {a}?",
  q_neighbor:"Quale paese confina conâ€¦?",q_neighbor_not:"NON confina conâ€¦?",
  q_plates_casual:"Da quale paese viene questa targa?",q_plates_hard:"Identificare la regione â€” nessun indizio!",
  q_river_real:"Attraverso quale paese scorre questo fiume?",q_map_guess:"Trova il paese sulla mappa",
  fb_correct:"âœ“ Corretto! +{pts}",fb_wrong:"âœ— Sbagliato â†’ {ans}",fb_time:"â± Tempo! â†’ {ans}",
  plates_more:"+{n} altri",pct_complete:"{pct}% completato",
  spotter_dup:"ðŸ“‹ {code} ({country}) giÃ  raccolto!",
  map_unavail:"Mappa non disponibile",map_loading:"Caricamento mappaâ€¦",
  q_subway_km:"Quanto Ã¨ lungo il metrÃ² â€¦ (km)?",q_subway_lines:"Quante linee metro ha â€¦?",
  hl_longer:"â¬†ï¸ PiÃ¹ lungo",hl_shorter:"â¬‡ï¸ PiÃ¹ corto",hl_bigger:"â¬†ï¸ PiÃ¹ grande (superficie)",hl_smaller:"â¬‡ï¸ PiÃ¹ piccolo (superficie)",
  ob_welcome:"Benvenuto su GeoQuest",ob_sub1:"Il quiz di geografia â€” colleziona timbri, sali in classifica!",ob_difficulty:"Livello di difficoltÃ ",ob_diff_sub:"Scegli il tuo stile. Modificabile in qualsiasi momento.",
  ob_diff_casual_desc:"CittÃ  principali â€¢ 12 sec.",ob_diff_hc_desc:"Tutte le cittÃ  â€¢ 8 sec.",ob_back:"â† Indietro",ob_modes_title:"ModalitÃ  di gioco",
  ob_modes_sub:"19 modalitÃ , un obiettivo: conoscere il mondo.",ob_more_modes:"â€¦ e altre 16 modalitÃ ",ob_start:"\u{1F680} Andiamo!",ob_have_account:"Ho giÃ  un account",ob_register:"Nuovo? Registrati",
  home_hi:"Ciao, {name} \u{1F44B}",home_guest:"Benvenuto, ospite \u{1F30D}",home_save:"\u{1F510} Salva i progressi",home_pvp_sub:"Gioca in tempo reale contro un amico",
  ob_mode1_name:"CittÃ  â†’ Paese",ob_mode1_desc:"A quale paese appartiene questa cittÃ ?",ob_mode2_name:"Targhe UE",ob_mode2_desc:"Da dove viene questa targa?",ob_mode3_name:"Reti metro",ob_mode3_desc:"Linee e km delle metropolitane.",
  language_select:"LINGUA",
  badge_beta:"Beta",beta_warning:"Giocabile, ma potrebbe contenere bug.",
  rotate_device:"Ruota il dispositivo in modalit\u00e0 orizzontale \u{1F4F1}\u27A1\u{1F5FA}",
  diff_desc_casual:"\u{1F7E2} Casual: Rilassato Â· Senza limite Â· âˆž Vite",
  diff_desc_hc:"\u{1F525} Hardcore: Classico Â· Senza limite Â· 3 Vite",
  diff_desc_surv:"\u{1F480} Survival: Contro il tempo Â· 8s Â· 3 Vite",
  hud_lives:"VITE",
  score_mult_max:"Moltiplicatore Max",
  score_time_bonus:"Bonus Tempo",
  pts_abbr:"pt.",
  score_correct_lbl:"corrette",
  mode_wappen:"Stemmi",
  mode_slf:"CittÃ -Paese-Fiume",
  mode_euro:"Monete Euro"
},
nl:{
  play:"SPELEN",again:"OPNIEUW SPELEN",menu:"Hoofdmenu",board:"Ranglijst",pass:"Paspoort",
  profile:"Profiel",stats:"Statistieken",casual:"Casual",hardcore:"Hardcore",rounds:"Rondes",
  btn_collect:"Verzamelen",btn_back:"Terug naar menu",btn_next:"Volgende â†’",
  btn_again:"Opnieuw spelen",btn_menu:"Hoofdmenu",btn_adapt:"Aanpassen",
  spotter_title:"\u{1F697} Reisspotter",
  spotter_hint:"Kenteken gezien? Noteer het nu!",
  spotter_all:"Alle landen",spotter_unknown:"Onbekend kenteken",
  spotter_not_in:"niet in",spotter_but_in:"maar in",
  album_title:"\u{1F4D4} Kentekenalbum",album_list:"\u{1F4DD} Lijst",album_map:"\u{1F5FA} Kaart",
  album_empty_country:"Nog niets uit {country} â€” gebruik de Spotter!",
  album_empty:"Nog niets verzameld!\nSpeel EU-kentekens of gebruik de Spotter.",
  album_codes:"codes",
  hl_higher:"â¬†ï¸ Meer / Langer / Groter",hl_lower:"â¬‡ï¸ Minder / Korter / Kleiner",
  hl_more:"â¬†ï¸ Meer inwoners",hl_less:"â¬‡ï¸ Minder inwoners",
  loc_detected:"Je bent in {country}",loc_adapt:"Aanpassen",
  q_city:"In welk land ligt deze stad?",q_flag:"Welk land heeft deze vlag?",
  q_capital:"Bij welk land hoort deze hoofdstad?",q_river:"In welk land ligt deze rivier?",
  q_landmark:"In welk land staat dit monument?",q_park:"In welk land ligt dit nationaal park?",
  q_unesco:"In welk land ligt dit UNESCO-erfgoed?",q_citymark:"Bij welke stad hoort dit monument?",
  q_subway:"In welke stad is deze metro?",q_flagsel:"Welke vlag hoort bijâ€¦",
  q_rcapital:"Wat is de hoofdstad vanâ€¦?",q_rcity:"Welke stad ligt inâ€¦?",
  q_rriver:"Welke rivier stroomt doorâ€¦?",q_outline:"Welk land heeft deze vorm?",
  q_food:"Uit welk land komt dit gerecht?",q_brand:"Uit welk land komt dit merk?",
  q_currency:"Bij welk land hoort deze munt?",q_curr_real:"Welke munt heeftâ€¦",
  q_pop_compare:"Meer of minder inwoners?",
  q_hl_pop:"Meer inwoners dan {a}?",q_hl_river:"Langer dan {a}?",q_hl_area:"Groter dan {a}?",
  q_neighbor:"Welk land grenst aanâ€¦?",q_neighbor_not:"Grenst NIET aanâ€¦?",
  q_plates_casual:"Uit welk land komt dit kenteken?",q_plates_hard:"Identificeer de regio â€” geen hint!",
  q_river_real:"Door welk land stroomt deze rivier?",q_map_guess:"Vind het land op de kaart",
  fb_correct:"âœ“ Correct! +{pts}",fb_wrong:"âœ— Fout â†’ {ans}",fb_time:"â± Tijd! â†’ {ans}",
  plates_more:"+{n} meer",pct_complete:"{pct}% voltooid",
  spotter_dup:"ðŸ“‹ {code} ({country}) al verzameld!",
  map_unavail:"Kaart niet beschikbaar",map_loading:"Kaart ladenâ€¦",
  q_subway_km:"Hoe lang is het metronetwerk â€¦ (km)?",q_subway_lines:"Hoeveel metrolijnen heeft â€¦?",
  diff_desc_casual:"\u{1F7E2} Casual: Ontspannen Â· Geen tijdslimiet Â· âˆž Levens",diff_desc_hc:"\u{1F525} Hardcore: Klassiek Â· Geen tijdslimiet Â· 3 Levens",diff_desc_surv:"\u{1F480} Survival: Tegen de klok Â· 8s Â· 3 Levens",hud_lives:"LEVENS",score_mult_max:"Max Vermenigvuldiger",score_time_bonus:"Tijdbonus",pts_abbr:"pt.",score_correct_lbl:"correct",mode_wappen:"Wapens",mode_slf:"Stad-Land-Rivier",mode_euro:"Euromunt"
},
pt:{
  play:"JOGAR",again:"JOGAR NOVAMENTE",menu:"Menu principal",board:"ClassificaÃ§Ã£o",pass:"Passaporte",
  profile:"Perfil",stats:"EstatÃ­sticas",casual:"Casual",hardcore:"Hardcore",rounds:"Rodadas",
  btn_collect:"Coletar",btn_back:"Voltar ao menu",btn_next:"PrÃ³ximo â†’",
  btn_again:"Jogar novamente",btn_menu:"Menu principal",btn_adapt:"Adaptar",
  spotter_title:"\u{1F697} Spotter de viagem",
  spotter_hint:"Viu uma placa? Registre agora!",
  spotter_all:"Todos os paÃ­ses",spotter_unknown:"Placa desconhecida",
  spotter_not_in:"nÃ£o em",spotter_but_in:"mas em",
  album_title:"\u{1F4D4} ColeÃ§Ã£o de placas",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Mapa",
  album_empty_country:"Nada de {country} ainda â€” use o Spotter!",
  album_empty:"Nada coletado ainda!\nJogue placas UE ou use o Spotter.",
  album_codes:"cÃ³digos",
  hl_higher:"â¬†ï¸ Mais / Mais longo / Maior",hl_lower:"â¬‡ï¸ Menos / Mais curto / Menor",
  hl_more:"â¬†ï¸ Mais habitantes",hl_less:"â¬‡ï¸ Menos habitantes",
  loc_detected:"VocÃª estÃ¡ em {country}",loc_adapt:"Adaptar",
  q_city:"Em qual paÃ­s fica esta cidade?",q_flag:"Qual paÃ­s tem esta bandeira?",
  q_capital:"A qual paÃ­s pertence esta capital?",q_river:"Em qual paÃ­s fica este rio?",
  q_landmark:"Em qual paÃ­s fica este monumento?",q_park:"Em qual paÃ­s fica este parque nacional?",
  q_unesco:"Em qual paÃ­s fica este sÃ­tio UNESCO?",q_citymark:"A qual cidade pertence este monumento?",
  q_subway:"Em qual cidade fica este metrÃ´?",q_flagsel:"Qual bandeira pertence aâ€¦",
  q_rcapital:"Qual Ã© a capital deâ€¦?",q_rcity:"Qual cidade fica emâ€¦?",
  q_rriver:"Qual rio corre porâ€¦?",q_outline:"Qual paÃ­s tem esta forma?",
  q_food:"De qual paÃ­s vem este prato?",q_brand:"De qual paÃ­s vem esta marca?",
  q_currency:"A qual paÃ­s pertence esta moeda?",q_curr_real:"Qual moeda temâ€¦",
  q_pop_compare:"Mais ou menos habitantes?",
  q_hl_pop:"Mais habitantes que {a}?",q_hl_river:"Mais longo que {a}?",q_hl_area:"Maior que {a}?",
  q_neighbor:"Qual paÃ­s faz fronteira comâ€¦?",q_neighbor_not:"NÃƒO faz fronteira comâ€¦?",
  q_plates_casual:"De qual paÃ­s Ã© esta placa?",q_plates_hard:"Identificar a regiÃ£o â€” sem dica!",
  q_river_real:"Por qual paÃ­s corre este rio?",q_map_guess:"Encontre o paÃ­s no mapa",
  fb_correct:"âœ“ Correto! +{pts}",fb_wrong:"âœ— Errado â†’ {ans}",fb_time:"â± Tempo! â†’ {ans}",
  plates_more:"+{n} mais",pct_complete:"{pct}% completo",
  spotter_dup:"ðŸ“‹ {code} ({country}) jÃ¡ coletado!",
  map_unavail:"Mapa nÃ£o disponÃ­vel",map_loading:"Carregando mapaâ€¦",
  q_subway_km:"Qual o comprimento da rede de metro â€¦ (km)?",q_subway_lines:"Quantas linhas de metro tem â€¦?",
  diff_desc_casual:"\u{1F7E2} Casual: Relaxado Â· Sem limite Â· âˆž Vidas",diff_desc_hc:"\u{1F525} Hardcore: ClÃ¡ssico Â· Sem limite Â· 3 Vidas",diff_desc_surv:"\u{1F480} Survival: Contra o relÃ³gio Â· 8s Â· 3 Vidas",hud_lives:"VIDAS",score_mult_max:"Multiplicador MÃ¡x.",score_time_bonus:"BÃ³nus de Tempo",pts_abbr:"pts.",score_correct_lbl:"corretas",mode_wappen:"BrasÃµes",mode_slf:"Cidade-PaÃ­s-Rio",mode_euro:"Moedas Euro"
},
ro:{
  play:"JOACÄ‚",again:"JOACÄ‚ DIN NOU",menu:"Meniu principal",board:"Clasament",pass:"PaÈ™aport",
  profile:"Profil",stats:"Statistici",casual:"Casual",hardcore:"Hardcore",rounds:"Runde",
  btn_collect:"ColecteazÄƒ",btn_back:"ÃŽnapoi la meniu",btn_next:"UrmÄƒtor â†’",
  btn_again:"JoacÄƒ din nou",btn_menu:"Meniu principal",btn_adapt:"AdapteazÄƒ",
  spotter_title:"\u{1F697} Spotter de cÄƒlÄƒtorie",
  spotter_hint:"Ai vÄƒzut o plÄƒcuÈ›Äƒ? ÃŽnregistreaz-o acum!",
  spotter_all:"Toate È›Äƒrile",spotter_unknown:"PlÄƒcuÈ›Äƒ necunoscutÄƒ",
  spotter_not_in:"nu Ã®n",spotter_but_in:"dar Ã®n",
  album_title:"\u{1F4D4} ColecÈ›ie de plÄƒcuÈ›e",album_list:"\u{1F4DD} ListÄƒ",album_map:"\u{1F5FA} HartÄƒ",
  album_empty_country:"Nimic din {country} Ã®ncÄƒ â€” foloseÈ™te Spotter-ul!",
  album_empty:"Nimic colectat Ã®ncÄƒ!\nJoacÄƒ plÄƒcuÈ›e UE sau foloseÈ™te Spotter-ul.",
  album_codes:"coduri",
  hl_higher:"â¬†ï¸ Mai mult / Mai lung / Mai mare",hl_lower:"â¬‡ï¸ Mai puÈ›in / Mai scurt / Mai mic",
  hl_more:"â¬†ï¸ Mai mulÈ›i locuitori",hl_less:"â¬‡ï¸ Mai puÈ›ini locuitori",
  loc_detected:"EÈ™ti Ã®n {country}",loc_adapt:"AdapteazÄƒ",
  q_city:"ÃŽn ce È›arÄƒ se aflÄƒ acest oraÈ™?",q_flag:"Ce È›arÄƒ are acest steag?",
  q_capital:"CÄƒrui È›Äƒri aparÈ›ine aceastÄƒ capitalÄƒ?",q_river:"ÃŽn ce È›arÄƒ curge acest rÃ¢u?",
  q_landmark:"ÃŽn ce È›arÄƒ se aflÄƒ acest monument?",q_park:"ÃŽn ce È›arÄƒ se aflÄƒ acest parc naÈ›ional?",
  q_unesco:"ÃŽn ce È›arÄƒ se aflÄƒ acest sit UNESCO?",q_citymark:"CÄƒrui oraÈ™ aparÈ›ine acest monument?",
  q_subway:"ÃŽn ce oraÈ™ se aflÄƒ acest metrou?",q_flagsel:"Ce steag aparÈ›ine luiâ€¦",
  q_rcapital:"Care este capitala luiâ€¦?",q_rcity:"Ce oraÈ™ se aflÄƒ Ã®nâ€¦?",
  q_rriver:"Ce rÃ¢u curge prinâ€¦?",q_outline:"Ce È›arÄƒ are aceastÄƒ formÄƒ?",
  q_food:"Din ce È›arÄƒ vine acest preparat?",q_brand:"Din ce È›arÄƒ vine acest brand?",
  q_currency:"CÄƒrui È›Äƒri aparÈ›ine aceastÄƒ monedÄƒ?",q_curr_real:"Ce monedÄƒ areâ€¦",
  q_pop_compare:"Mai mulÈ›i sau mai puÈ›ini locuitori?",
  q_hl_pop:"Mai mulÈ›i locuitori decÃ¢t {a}?",q_hl_river:"Mai lung decÃ¢t {a}?",q_hl_area:"Mai mare decÃ¢t {a}?",
  q_neighbor:"Ce È›arÄƒ se Ã®nvecineazÄƒ cuâ€¦?",q_neighbor_not:"NU se Ã®nvecineazÄƒ cuâ€¦?",
  q_plates_casual:"Din ce È›arÄƒ este aceastÄƒ plÄƒcuÈ›Äƒ?",q_plates_hard:"IdentificaÈ›i regiunea â€” fÄƒrÄƒ indiciu!",
  q_river_real:"Prin ce È›arÄƒ curge acest rÃ¢u?",q_map_guess:"GÄƒseÈ™te È›ara pe hartÄƒ",
  fb_correct:"âœ“ Corect! +{pts}",fb_wrong:"âœ— GreÈ™it â†’ {ans}",fb_time:"â± Timp! â†’ {ans}",
  plates_more:"+{n} mai mult",pct_complete:"{pct}% complet",
  spotter_dup:"ðŸ“‹ {code} ({country}) deja colectat!",
  map_unavail:"HartÄƒ indisponibilÄƒ",map_loading:"Se ÃªncarcÄƒ hartaâ€¦",
  q_subway_km:"CÃ¢t de lungÄƒ este reÈ›eaua de metrou â€¦ (km)?",q_subway_lines:"CÃ¢te linii de metrou are â€¦?",
  diff_desc_casual:"\u{1F7E2} Casual: Relaxat Â· FÄƒrÄƒ limitÄƒ Â· âˆž VieÈ›i",diff_desc_hc:"\u{1F525} Hardcore: Clasic Â· FÄƒrÄƒ limitÄƒ Â· 3 VieÈ›i",diff_desc_surv:"\u{1F480} Survival: Contra cronometru Â· 8s Â· 3 VieÈ›i",hud_lives:"VIEÈžI",score_mult_max:"Multiplicator Max",score_time_bonus:"Bonus Timp",pts_abbr:"pct.",score_correct_lbl:"corecte",mode_wappen:"Steme",mode_slf:"OraÅŸ-ÈšarÄƒ-RÃ¢u",mode_euro:"Monede Euro"
},
hu:{
  play:"JÃTÃ‰K",again:"ÃšJRA JÃTSZANI",menu:"FÅ‘menÃ¼",board:"Rangsor",pass:"ÃštlevÃ©l",
  profile:"Profil",stats:"StatisztikÃ¡k",casual:"KÃ¶nnyÅ±",hardcore:"NehÃ©z",rounds:"KÃ¶rÃ¶k",
  btn_collect:"GyÅ±jt",btn_back:"Vissza a fÅ‘menÃ¼be",btn_next:"TovÃ¡bb â†’",
  btn_again:"Ãšjra jÃ¡tszani",btn_menu:"FÅ‘menÃ¼",btn_adapt:"MÃ³dosÃ­t",
  spotter_title:"\u{1F697} UtazÃ³ Spotter",
  spotter_hint:"RendszÃ¡mot lÃ¡ttÃ¡l? Jegyezd fel azonnal!",
  spotter_all:"Ã–sszes orszÃ¡g",spotter_unknown:"Ismeretlen rendszÃ¡m",
  spotter_not_in:"nem szerepel",spotter_but_in:"de szerepel",
  album_title:"\u{1F4D4} RendszÃ¡m Album",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} TÃ©rkÃ©p",
  album_empty_country:"MÃ©g semmi {country}-bÃ³l â€” hasznÃ¡ld a Spotter-t!",
  album_empty:"MÃ©g semmi Ã¶sszegyÅ±jtve!\nJÃ¡tssz EU rendszÃ¡mokat vagy hasznÃ¡ld a Spotter-t.",
  album_codes:"kÃ³dok",
  hl_higher:"â¬†ï¸ TÃ¶bb / Hosszabb / Nagyobb",hl_lower:"â¬‡ï¸ Kevesebb / RÃ¶videbb / Kisebb",
  hl_more:"â¬†ï¸ TÃ¶bb lakos",hl_less:"â¬‡ï¸ Kevesebb lakos",
  loc_detected:"Jelenleg itt tartÃ³zkodik: {country}",loc_adapt:"MÃ³dosÃ­t",
  q_city:"Melyik orszÃ¡gban van ez a vÃ¡ros?",q_flag:"Melyik orszÃ¡g zÃ¡szlaja ez?",
  q_capital:"Melyik orszÃ¡g fÅ‘vÃ¡rosa ez?",q_river:"Melyik orszÃ¡gban folyik ez a folyÃ³?",
  q_landmark:"Melyik orszÃ¡gban van ez az emlÃ©kmÅ±?",q_park:"Melyik orszÃ¡gban van ez a nemzeti park?",
  q_unesco:"Melyik orszÃ¡gban van ez az UNESCO-helyszÃ­n?",q_citymark:"Melyik vÃ¡roshoz tartozik ez az emlÃ©kmÅ±?",
  q_subway:"Melyik vÃ¡rosban van ez a metrÃ³?",q_flagsel:"Melyik zÃ¡szlÃ³ tartozikâ€¦-hoz",
  q_rcapital:"Mi a fÅ‘vÃ¡rosaâ€¦-nak?",q_rcity:"Melyik vÃ¡ros vanâ€¦-ban?",
  q_rriver:"Melyik folyÃ³ folyik Ã¡tâ€¦-on?",q_outline:"Melyik orszÃ¡g van ebben az alakban?",
  q_food:"Melyik orszÃ¡gbÃ³l szÃ¡rmazik ez az Ã©tel?",q_brand:"Melyik orszÃ¡gbÃ³l szÃ¡rmazik ez a mÃ¡rka?",
  q_currency:"Melyik orszÃ¡g pÃ©nzneme ez?",q_curr_real:"Melyik pÃ©nzneme vanâ€¦-nak",
  q_pop_compare:"TÃ¶bb vagy kevesebb lakos?",
  q_hl_pop:"TÃ¶bb lakos, mint {a}?",q_hl_river:"Hosszabb, mint {a}?",q_hl_area:"Nagyobb, mint {a}?",
  q_neighbor:"Melyik orszÃ¡g hatÃ¡rosâ€¦-val?",q_neighbor_not:"NEM hatÃ¡rosâ€¦-val?",
  q_plates_casual:"Melyik orszÃ¡g rendszÃ¡ma ez?",q_plates_hard:"AzonosÃ­tsa a rÃ©giÃ³t â€” nincs tipp!",
  q_river_real:"Melyik orszÃ¡gon folyik Ã¡t ez a folyÃ³?",q_map_guess:"Keresse meg az orszÃ¡got a tÃ©rkÃ©pen",
  fb_correct:"âœ“ Helyes! +{pts}",fb_wrong:"âœ— Rossz â†’ {ans}",fb_time:"â± IdÅ‘! â†’ {ans}",
  plates_more:"+{n} tÃ¶bb",pct_complete:"{pct}% kÃ©sz",
  spotter_dup:"ðŸ“‹ {code} ({country}) mÃ¡r Ã¶sszegyÅ±jtve!",
  map_unavail:"TÃ©rkÃ©p nem elÃ©rhetÅ‘",map_loading:"TÃ©rkÃ©p betÃ¶ltÃ©seâ€¦",
  q_subway_km:"Milyen hosszÃº a metrÃ³hÃ¡lÃ³zat â€¦ (km)?",q_subway_lines:"HÃ¡ny metrÃ³vonal van â€¦?",
  diff_desc_casual:"\u{1F7E2} Casual: LazulÃ¡s Â· Nincs idÅ‘limit Â· âˆž Ã‰let",diff_desc_hc:"\u{1F525} Hardcore: Klasszikus Â· Nincs idÅ‘limit Â· 3 Ã‰let",diff_desc_surv:"\u{1F480} Survival: Verseny az idÅ‘vel Â· 8mp Â· 3 Ã‰let",hud_lives:"Ã‰LETEK",score_mult_max:"Max SzorzÃ³",score_time_bonus:"IdÅ‘bÃ³nusz",pts_abbr:"pt.",score_correct_lbl:"helyes",mode_wappen:"CÃ­merek",mode_slf:"VÃ¡ros-OrszÃ¡g-FolyÃ³",mode_euro:"EurÃ³Ã©rmÃ©k"
},
cs:{
  play:"HRÃT",again:"HRÃT ZNOVU",menu:"HlavnÃ­ menu",board:"Å½ebÅ™Ã­Äek",pass:"Pas",
  profile:"Profil",stats:"Statistiky",casual:"Casual",hardcore:"Hardcore",rounds:"Kola",
  btn_collect:"SbÃ­rat",btn_back:"ZpÄ›t do menu",btn_next:"DalÅ¡Ã­ â†’",
  btn_again:"HrÃ¡t znovu",btn_menu:"HlavnÃ­ menu",btn_adapt:"PÅ™izpÅ¯sobit",
  spotter_title:"\u{1F697} CestovnÃ­ Spotter",
  spotter_hint:"VidÄ›l jsi SPZ? ZapiÅ¡ ji hned!",
  spotter_all:"VÅ¡echny zemÄ›",spotter_unknown:"NeznÃ¡mÃ¡ SPZ",
  spotter_not_in:"nenÃ­ v",spotter_but_in:"ale je v",
  album_title:"\u{1F4D4} Album SPZ",album_list:"\u{1F4DD} Seznam",album_map:"\u{1F5FA} Mapa",
  album_empty_country:"ZatÃ­m nic z {country} â€” pouÅ¾ij Spotter!",
  album_empty:"ZatÃ­m nic neshromÃ¡Å¾dÄ›no!\nHraj EU SPZ nebo pouÅ¾ij Spotter.",
  album_codes:"kÃ³dy",
  hl_higher:"â¬†ï¸ VÃ­ce / DelÅ¡Ã­ / VÄ›tÅ¡Ã­",hl_lower:"â¬‡ï¸ MÃ©nÄ› / KratÅ¡Ã­ / MenÅ¡Ã­",
  hl_more:"â¬†ï¸ VÃ­ce obyvatel",hl_less:"â¬‡ï¸ MÃ©nÄ› obyvatel",
  loc_detected:"Jsi v {country}",loc_adapt:"PÅ™izpÅ¯sobit",
  q_city:"Ve kterÃ© zemi leÅ¾Ã­ toto mÄ›sto?",q_flag:"KterÃ¡ zemÄ› mÃ¡ tuto vlajku?",
  q_capital:"KterÃ© zemi patÅ™Ã­ toto hlavnÃ­ mÄ›sto?",q_river:"Ve kterÃ© zemi teÄe tato Å™eka?",
  q_landmark:"Ve kterÃ© zemi se nachÃ¡zÃ­ tato pamÃ¡tka?",q_park:"Ve kterÃ© zemi se nachÃ¡zÃ­ tento nÃ¡rodnÃ­ park?",
  q_unesco:"Ve kterÃ© zemi se nachÃ¡zÃ­ toto UNESCO dÄ›dictvÃ­?",q_citymark:"Ke kterÃ©mu mÄ›stu patÅ™Ã­ tato pamÃ¡tka?",
  q_subway:"Ve kterÃ©m mÄ›stÄ› je toto metro?",q_flagsel:"KterÃ¡ vlajka patÅ™Ã­ kâ€¦",
  q_rcapital:"JakÃ© je hlavnÃ­ mÄ›stoâ€¦?",q_rcity:"KterÃ© mÄ›sto leÅ¾Ã­ vâ€¦?",
  q_rriver:"KterÃ¡ Å™eka protÃ©kÃ¡â€¦?",q_outline:"KterÃ¡ zemÄ› mÃ¡ tento tvar?",
  q_food:"Ze kterÃ© zemÄ› pochÃ¡zÃ­ toto jÃ­dlo?",q_brand:"Ze kterÃ© zemÄ› pochÃ¡zÃ­ tato znaÄka?",
  q_currency:"KterÃ© zemi patÅ™Ã­ tato mÄ›na?",q_curr_real:"Jakou mÄ›nu mÃ¡â€¦",
  q_pop_compare:"VÃ­ce nebo mÃ©nÄ› obyvatel?",
  q_hl_pop:"VÃ­ce obyvatel neÅ¾ {a}?",q_hl_river:"DelÅ¡Ã­ neÅ¾ {a}?",q_hl_area:"VÄ›tÅ¡Ã­ neÅ¾ {a}?",
  q_neighbor:"KterÃ¡ zemÄ› sousedÃ­ sâ€¦?",q_neighbor_not:"NESOUSEDÃ sâ€¦?",
  q_plates_casual:"Ze kterÃ© zemÄ› je tato SPZ?",q_plates_hard:"UrÄete region â€” Å¾Ã¡dnÃ¡ nÃ¡povÄ›da!",
  q_river_real:"PÅ™es kterou zemi teÄe tato Å™eka?",q_map_guess:"Najdi zemi na mapÄ›",
  fb_correct:"âœ“ SprÃ¡vnÄ›! +{pts}",fb_wrong:"âœ— ChybnÄ› â†’ {ans}",fb_time:"â± ÄŒas! â†’ {ans}",
  plates_more:"+{n} dalÅ¡Ã­ch",pct_complete:"{pct}% hotovo",
  spotter_dup:"ðŸ“‹ {code} ({country}) jiÅ¾ sbÃ­rÃ¡no!",
  map_unavail:"Mapa nenÃ­ k dispozici",map_loading:"NaÄÃ­tÃ¡nÃ­ mapyâ€¦",
  q_subway_km:"Jak dlouhÃ© je metro â€¦ (km)?",q_subway_lines:"Kolik metrovÃ½ch linek mÃ¡ â€¦?",
  diff_desc_casual:"\u{1F7E2} Casual: UvolnÄ›nÃ½ Â· Bez ÄasovÃ©ho limitu Â· âˆž Å½ivotÅ¯",diff_desc_hc:"\u{1F525} Hardcore: Klasika Â· Bez limitu Â· 3 Å½ivoty",diff_desc_surv:"\u{1F480} Survival: Proti Äasu Â· 8s Â· 3 Å½ivoty",hud_lives:"Å½IVOTY",score_mult_max:"Max MultiplikÃ¡tor",score_time_bonus:"ÄŒasovÃ½ Bonus",pts_abbr:"bd.",score_correct_lbl:"sprÃ¡vnÄ›",mode_wappen:"Erby",mode_slf:"MÄ›sto-StÃ¡t-Å˜eka",mode_euro:"Euromince"
},
sk:{
  play:"HRAÅ¤",again:"HRAÅ¤ ZNOVA",menu:"HlavnÃ© menu",board:"RebrÃ­Äek",pass:"Pas",
  profile:"Profil",stats:"Å tatistiky",casual:"Casual",hardcore:"Hardcore",rounds:"KolÃ¡",
  btn_collect:"ZbieraÅ¥",btn_back:"SpÃ¤Å¥ do menu",btn_next:"ÄŽalej â†’",
  btn_again:"HraÅ¥ znova",btn_menu:"HlavnÃ© menu",btn_adapt:"PrispÃ´sobiÅ¥",
  spotter_title:"\u{1F697} CestovnÃ½ Spotter",
  spotter_hint:"Videl si EÄŒV? ZaznaÄ ju hneÄ!",
  spotter_all:"VÅ¡etky krajiny",spotter_unknown:"NeznÃ¡ma EÄŒV",
  spotter_not_in:"nie je v",spotter_but_in:"ale je v",
  album_title:"\u{1F4D4} Album EÄŒV",album_list:"\u{1F4DD} Zoznam",album_map:"\u{1F5FA} Mapa",
  album_empty_country:"ZatiaÄ¾ niÄ z {country} â€” pouÅ¾i Spotter!",
  album_empty:"ZatiaÄ¾ niÄ nezbierane!\nHraj EÃš EÄŒV alebo pouÅ¾i Spotter.",
  album_codes:"kÃ³dy",
  hl_higher:"â¬†ï¸ Viac / DlhÅ¡Ã­ / VÃ¤ÄÅ¡Ã­",hl_lower:"â¬‡ï¸ Menej / KratÅ¡Ã­ / MenÅ¡Ã­",
  hl_more:"â¬†ï¸ Viac obyvateÄ¾ov",hl_less:"â¬‡ï¸ Menej obyvateÄ¾ov",
  loc_detected:"Si v {country}",loc_adapt:"PrispÃ´sobiÅ¥",
  q_city:"V ktorej krajine leÅ¾Ã­ toto mesto?",q_flag:"KtorÃ¡ krajina mÃ¡ tÃºto vlajku?",
  q_capital:"Ktorej krajine patrÃ­ toto hlavnÃ© mesto?",q_river:"V ktorej krajine teÄie tÃ¡to rieka?",
  q_landmark:"V ktorej krajine sa nachÃ¡dza tÃ¡to pamiatka?",q_park:"V ktorej krajine sa nachÃ¡dza tento nÃ¡rodnÃ½ park?",
  q_unesco:"V ktorej krajine sa nachÃ¡dza toto UNESCO dediÄstvo?",q_citymark:"KtorÃ©mu mestu patrÃ­ tÃ¡to pamiatka?",
  q_subway:"V ktorom meste je toto metro?",q_flagsel:"KtorÃ¡ vlajka patrÃ­ kâ€¦",
  q_rcapital:"AkÃ© je hlavnÃ© mestoâ€¦?",q_rcity:"KtorÃ© mesto leÅ¾Ã­ vâ€¦?",
  q_rriver:"KtorÃ¡ rieka pretekÃ¡ cezâ€¦?",q_outline:"KtorÃ¡ krajina mÃ¡ tento tvar?",
  q_food:"Z ktorej krajiny pochÃ¡dza toto jedlo?",q_brand:"Z ktorej krajiny pochÃ¡dza tÃ¡to znaÄka?",
  q_currency:"Ktorej krajine patrÃ­ tÃ¡to mena?",q_curr_real:"AkÃº menu mÃ¡â€¦",
  q_pop_compare:"Viac alebo menej obyvateÄ¾ov?",
  q_hl_pop:"Viac obyvateÄ¾ov ako {a}?",q_hl_river:"DlhÅ¡Ã­ ako {a}?",q_hl_area:"VÃ¤ÄÅ¡Ã­ ako {a}?",
  q_neighbor:"KtorÃ¡ krajina susedÃ­ sâ€¦?",q_neighbor_not:"NESUSEDÃ sâ€¦?",
  q_plates_casual:"Z ktorej krajiny je tÃ¡to EÄŒV?",q_plates_hard:"Identifikujte regiÃ³n â€” Å¾iadna nÃ¡poveda!",
  q_river_real:"Cez ktorÃº krajinu teÄie tÃ¡to rieka?",q_map_guess:"NÃ¡jdi krajinu na mape",
  fb_correct:"âœ“ SprÃ¡vne! +{pts}",fb_wrong:"âœ— NesprÃ¡vne â†’ {ans}",fb_time:"â± ÄŒas! â†’ {ans}",
  plates_more:"+{n} ÄalÅ¡Ã­ch",pct_complete:"{pct}% hotovo",
  spotter_dup:"ðŸ“‹ {code} ({country}) uÅ¾ zozbieranÃ©!",
  map_unavail:"Mapa nie je dostupnÃ¡",map_loading:"NaÄÃ­tÃ¡vanie mapyâ€¦",
  q_subway_km:"AkÃ¡ dlhÃ¡ je sieÅ¥ metra â€¦ (km)?",q_subway_lines:"KoÄ¾ko liniek metra mÃ¡ â€¦?",
  diff_desc_casual:"\u{1F7E2} Casual: UvolnÄ›nÃ½ Â· Bez ÄasovÃ©ho limitu Â· âˆž Å½ivotov",diff_desc_hc:"\u{1F525} Hardcore: Klasika Â· Bez limitu Â· 3 Å½ivoty",diff_desc_surv:"\u{1F480} Survival: Proti Äasu Â· 8s Â· 3 Å½ivoty",hud_lives:"Å½IVOTY",score_mult_max:"Max MultiplikÃ¡tor",score_time_bonus:"ÄŒasovÃ½ Bonus",pts_abbr:"b.",score_correct_lbl:"sprÃ¡vne",mode_wappen:"Erby",mode_slf:"Mesto-Krajina-Rieka",mode_euro:"Euromince"
},
hr:{
  play:"IGRAJ",again:"IGRAJ PONOVO",menu:"Glavni izbornik",board:"Ljestvica",pass:"Putovnica",
  profile:"Profil",stats:"Statistike",casual:"Casual",hardcore:"Hardcore",rounds:"Runde",
  btn_collect:"Sakupi",btn_back:"Natrag na izbornik",btn_next:"SljedeÄ‡e â†’",
  btn_again:"Igraj ponovo",btn_menu:"Glavni izbornik",btn_adapt:"Prilagodi",
  spotter_title:"\u{1F697} Putni Spotter",
  spotter_hint:"Vidio registraciju? ZabiljeÅ¾i odmah!",
  spotter_all:"Sve drÅ¾ave",spotter_unknown:"Nepoznata registracija",
  spotter_not_in:"nije u",spotter_but_in:"ali je u",
  album_title:"\u{1F4D4} Album registracija",album_list:"\u{1F4DD} Popis",album_map:"\u{1F5FA} Karta",
  album_empty_country:"JoÅ¡ niÅ¡ta iz {country} â€” koristi Spotter!",
  album_empty:"JoÅ¡ niÅ¡ta skupljeno!\nIgraj EU registracije ili koristi Spotter.",
  album_codes:"kodovi",
  hl_higher:"â¬†ï¸ ViÅ¡e / DuÅ¾e / VeÄ‡e",hl_lower:"â¬‡ï¸ Manje / KraÄ‡e / Manje",
  hl_more:"â¬†ï¸ ViÅ¡e stanovnika",hl_less:"â¬‡ï¸ Manje stanovnika",
  loc_detected:"Nalazite se u {country}",loc_adapt:"Prilagodi",
  q_city:"U kojoj se drÅ¾avi nalazi ovaj grad?",q_flag:"Koja drÅ¾ava ima ovu zastavu?",
  q_capital:"Kojoj drÅ¾avi pripada ovaj glavni grad?",q_river:"U kojoj drÅ¾avi teÄe ova rijeka?",
  q_landmark:"U kojoj se drÅ¾avi nalazi ovaj spomenik?",q_park:"U kojoj se drÅ¾avi nalazi ovaj nacionalni park?",
  q_unesco:"U kojoj se drÅ¾avi nalazi ovo UNESCO nasljeÄ‘e?",q_citymark:"Kojemu gradu pripada ovaj spomenik?",
  q_subway:"U kojemu gradu je ovaj metro?",q_flagsel:"Koja zastava pripadaâ€¦",
  q_rcapital:"Koji je glavni gradâ€¦?",q_rcity:"Koji grad se nalazi uâ€¦?",
  q_rriver:"Koja rijeka teÄe krozâ€¦?",q_outline:"Koja drÅ¾ava ima ovaj oblik?",
  q_food:"Iz koje drÅ¾ave dolazi ovo jelo?",q_brand:"Iz koje drÅ¾ave dolazi ovaj brand?",
  q_currency:"Kojoj drÅ¾avi pripada ova valuta?",q_curr_real:"Koju valutu imaâ€¦",
  q_pop_compare:"ViÅ¡e ili manje stanovnika?",
  q_hl_pop:"ViÅ¡e stanovnika od {a}?",q_hl_river:"DuÅ¾e od {a}?",q_hl_area:"VeÄ‡e od {a}?",
  q_neighbor:"Koja drÅ¾ava graniÄi sâ€¦?",q_neighbor_not:"NE graniÄi sâ€¦?",
  q_plates_casual:"Iz koje drÅ¾ave je ova registracija?",q_plates_hard:"Identificirajte regiju â€” nema naznake!",
  q_river_real:"Kroz koju drÅ¾avu teÄe ova rijeka?",q_map_guess:"PronaÄ‘i drÅ¾avu na karti",
  fb_correct:"âœ“ ToÄno! +{pts}",fb_wrong:"âœ— PogreÅ¡no â†’ {ans}",fb_time:"â± Kraj vremena! â†’ {ans}",
  plates_more:"+{n} viÅ¡e",pct_complete:"{pct}% dovrÅ¡eno",
  spotter_dup:"ðŸ“‹ {code} ({country}) veÄ‡ skupljeno!",
  map_unavail:"Karta nije dostupna",map_loading:"UÄitavanje karteâ€¦",
  q_subway_km:"Koliko duga je mreÅ¾a metroa â€¦ (km)?",q_subway_lines:"Koliko linija metroa ima â€¦?",
  diff_desc_casual:"\u{1F7E2} Casual: OpuÅ¡teno Â· Bez vremenskog limita Â· âˆž Å½ivota",diff_desc_hc:"\u{1F525} Hardcore: Klasik Â· Bez limita Â· 3 Å½ivota",diff_desc_surv:"\u{1F480} Survival: Protiv sata Â· 8s Â· 3 Å½ivota",hud_lives:"Å½IVOTI",score_mult_max:"Maks MnoÅ¾itelj",score_time_bonus:"Vremenski Bonus",pts_abbr:"bod.",score_correct_lbl:"toÄno",mode_wappen:"Grbovi",mode_slf:"Grad-Zemlja-Rijeka",mode_euro:"Euro Kovanice"
},
sl:{
  play:"IGRAJ",again:"IGRAJ ZNOVA",menu:"Glavni meni",board:"Lestvica",pass:"Potni list",
  profile:"Profil",stats:"Statistike",casual:"Casual",hardcore:"Hardcore",rounds:"Runde",
  btn_collect:"Zberi",btn_back:"Nazaj v meni",btn_next:"Naprej â†’",
  btn_again:"Igraj znova",btn_menu:"Glavni meni",btn_adapt:"Prilagodi",
  spotter_title:"\u{1F697} Potovalni Spotter",
  spotter_hint:"Si videl tablico? ZapiÅ¡i jo takoj!",
  spotter_all:"Vse drÅ¾ave",spotter_unknown:"Neznana tablica",
  spotter_not_in:"ni v",spotter_but_in:"ampak je v",
  album_title:"\u{1F4D4} Album tablic",album_list:"\u{1F4DD} Seznam",album_map:"\u{1F5FA} Karta",
  album_empty_country:"Å e niÄ iz {country} â€” uporabi Spotter!",
  album_empty:"Å e niÄ zbrano!\nIgraj EU tablice ali uporabi Spotter.",
  album_codes:"kode",
  hl_higher:"â¬†ï¸ VeÄ / DaljÅ¡i / VeÄji",hl_lower:"â¬‡ï¸ Manj / KrajÅ¡i / ManjÅ¡i",
  hl_more:"â¬†ï¸ VeÄ prebivalcev",hl_less:"â¬‡ï¸ Manj prebivalcev",
  loc_detected:"Ste v {country}",loc_adapt:"Prilagodi",
  q_city:"V kateri drÅ¾avi leÅ¾i to mesto?",q_flag:"Katera drÅ¾ava ima to zastavo?",
  q_capital:"Kateri drÅ¾avi pripada to glavno mesto?",q_river:"V kateri drÅ¾avi teÄe ta reka?",
  q_landmark:"V kateri drÅ¾avi se nahaja ta znamenitost?",q_park:"V kateri drÅ¾avi se nahaja ta narodni park?",
  q_unesco:"V kateri drÅ¾avi se nahaja ta UNESCO dediÅ¡Äina?",q_citymark:"Kateremu mestu pripada ta znamenitost?",
  q_subway:"V katerem mestu je ta metro?",q_flagsel:"Katera zastava pripadaâ€¦",
  q_rcapital:"KakÅ¡no je glavno mestoâ€¦?",q_rcity:"Katero mesto leÅ¾i vâ€¦?",
  q_rriver:"Katera reka teÄe skoziâ€¦?",q_outline:"Katera drÅ¾ava ima to obliko?",
  q_food:"Iz katere drÅ¾ave prihaja ta jed?",q_brand:"Iz katere drÅ¾ave prihaja ta znamka?",
  q_currency:"Kateri drÅ¾avi pripada ta valuta?",q_curr_real:"KakÅ¡no valuto imaâ€¦",
  q_pop_compare:"VeÄ ali manj prebivalcev?",
  q_hl_pop:"VeÄ prebivalcev kot {a}?",q_hl_river:"DaljÅ¡i kot {a}?",q_hl_area:"VeÄji kot {a}?",
  q_neighbor:"Katera drÅ¾ava meji naâ€¦?",q_neighbor_not:"NE meji naâ€¦?",
  q_plates_casual:"Iz katere drÅ¾ave je ta tablica?",q_plates_hard:"Identificirajte regijo â€” brez namiga!",
  q_river_real:"Skozi katero drÅ¾avo teÄe ta reka?",q_map_guess:"PoiÅ¡Äi drÅ¾avo na karti",
  fb_correct:"âœ“ Pravilno! +{pts}",fb_wrong:"âœ— NapaÄno â†’ {ans}",fb_time:"â± ÄŒas! â†’ {ans}",
  plates_more:"+{n} veÄ",pct_complete:"{pct}% dokonÄano",
  spotter_dup:"ðŸ“‹ {code} ({country}) Å¾e zbrano!",
  map_unavail:"Karta ni na voljo",map_loading:"Nalaganje karteâ€¦",
  q_subway_km:"Kako dolgo je metrojsko omreÅ¾je â€¦ (km)?",q_subway_lines:"Koliko metrojskih linij ima â€¦?",
  diff_desc_casual:"\u{1F7E2} Casual: Sprostitveno Â· Brez Äasovne omejitve Â· âˆž Å½ivljenj",diff_desc_hc:"\u{1F525} Hardcore: KlasiÄno Â· Brez omejitve Â· 3 Å½ivljenja",diff_desc_surv:"\u{1F480} Survival: Dirka s Äasom Â· 8s Â· 3 Å½ivljenja",hud_lives:"Å½IVLJENJA",score_mult_max:"Maks MnoÅ¾itelj",score_time_bonus:"ÄŒasovni Bonus",pts_abbr:"t.",score_correct_lbl:"pravilno",mode_wappen:"Grbi",mode_slf:"Mesto-DeÅ¾ela-Reka",mode_euro:"Eurokovanice"
},
bg:{
  play:"Ð˜Ð“Ð ÐÐ™",again:"Ð˜Ð“Ð ÐÐ™ ÐžÐ¢ÐÐžÐ’Ðž",menu:"Ð“Ð»Ð°Ð²Ð½Ð¾ Ð¼ÐµÐ½ÑŽ",board:"ÐšÐ»Ð°ÑÐ°Ñ†Ð¸Ñ",pass:"ÐŸÐ°ÑÐ¿Ð¾Ñ€Ñ‚",
  profile:"ÐŸÑ€Ð¾Ñ„Ð¸Ð»",stats:"Ð¡Ñ‚Ð°Ñ‚Ð¸ÑÑ‚Ð¸ÐºÐ¸",casual:"Ð›ÐµÑÐµÐ½",hardcore:"Ð¢Ñ€ÑƒÐ´ÐµÐ½",rounds:"Ð ÑƒÐ½Ð´Ð¸",
  btn_collect:"Ð¡ÑŠÐ±ÐµÑ€Ð¸",btn_back:"ÐžÐ±Ñ€Ð°Ñ‚Ð½Ð¾ Ð² Ð¼ÐµÐ½ÑŽÑ‚Ð¾",btn_next:"ÐÐ°Ð¿Ñ€ÐµÐ´ â†’",
  btn_again:"Ð˜Ð³Ñ€Ð°Ð¹ Ð¾Ñ‚Ð½Ð¾Ð²Ð¾",btn_menu:"Ð“Ð»Ð°Ð²Ð½Ð¾ Ð¼ÐµÐ½ÑŽ",btn_adapt:"ÐÐ´Ð°Ð¿Ñ‚Ð¸Ñ€Ð°Ð¹",
  spotter_title:"\u{1F697} ÐŸÑŠÑ‚ÐµÐ½ Ð¡Ð¿Ð¾Ñ‚ÑŠÑ€",
  spotter_hint:"Ð’Ð¸Ð´ÑÐ» Ñ‚Ð°Ð±ÐµÐ»Ð°? Ð—Ð°Ð¿Ð¸ÑˆÐ¸ Ñ Ð²ÐµÐ´Ð½Ð°Ð³Ð°!",
  spotter_all:"Ð’ÑÐ¸Ñ‡ÐºÐ¸ ÑÑ‚Ñ€Ð°Ð½Ð¸",spotter_unknown:"ÐÐµÐ¿Ð¾Ð·Ð½Ð°Ñ‚Ð° Ñ‚Ð°Ð±ÐµÐ»Ð°",
  spotter_not_in:"Ð½Ðµ Ðµ Ð²",spotter_but_in:"Ð½Ð¾ Ðµ Ð²",
  album_title:"\u{1F4D4} ÐÐ»Ð±ÑƒÐ¼ Ñ Ñ‚Ð°Ð±ÐµÐ»Ð¸",album_list:"\u{1F4DD} Ð¡Ð¿Ð¸ÑÑŠÐº",album_map:"\u{1F5FA} ÐšÐ°Ñ€Ñ‚Ð°",
  album_empty_country:"ÐÐ¸Ñ‰Ð¾ Ð¾Ñ‚ {country} Ð²ÑÐµ Ð¾Ñ‰Ðµ â€” Ð¸Ð·Ð¿Ð¾Ð»Ð·Ð²Ð°Ð¹ Ð¡Ð¿Ð¾Ñ‚ÑŠÑ€Ð°!",
  album_empty:"Ð’ÑÐµ Ð¾Ñ‰Ðµ Ð½Ð¸Ñ‰Ð¾ ÑÑŠÐ±Ñ€Ð°Ð½Ð¾!\nÐ˜Ð³Ñ€Ð°Ð¹ Ð•Ð¡ Ñ‚Ð°Ð±ÐµÐ»Ð¸ Ð¸Ð»Ð¸ Ð¸Ð·Ð¿Ð¾Ð»Ð·Ð²Ð°Ð¹ Ð¡Ð¿Ð¾Ñ‚ÑŠÑ€Ð°.",
  album_codes:"ÐºÐ¾Ð´Ð¾Ð²Ðµ",
  hl_higher:"â¬†ï¸ ÐŸÐ¾Ð²ÐµÑ‡Ðµ / ÐŸÐ¾-Ð´ÑŠÐ»Ð³Ð¾ / ÐŸÐ¾-Ð³Ð¾Ð»ÑÐ¼Ð¾",hl_lower:"â¬‡ï¸ ÐŸÐ¾-Ð¼Ð°Ð»ÐºÐ¾ / ÐŸÐ¾-ÐºÑ€Ð°Ñ‚ÐºÐ¾ / ÐŸÐ¾-Ð¼Ð°Ð»ÐºÐ¾",
  hl_more:"â¬†ï¸ ÐŸÐ¾Ð²ÐµÑ‡Ðµ Ð¶Ð¸Ñ‚ÐµÐ»Ð¸",hl_less:"â¬‡ï¸ ÐŸÐ¾-Ð¼Ð°Ð»ÐºÐ¾ Ð¶Ð¸Ñ‚ÐµÐ»Ð¸",
  loc_detected:"ÐÐ°Ð¼Ð¸Ñ€Ð°Ñ‚Ðµ ÑÐµ Ð² {country}",loc_adapt:"ÐÐ´Ð°Ð¿Ñ‚Ð¸Ñ€Ð°Ð¹",
  q_city:"Ð’ ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° ÑÐµ Ð½Ð°Ð¼Ð¸Ñ€Ð° Ñ‚Ð¾Ð·Ð¸ Ð³Ñ€Ð°Ð´?",q_flag:"ÐšÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ð¸Ð¼Ð° Ñ‚Ð¾Ð²Ð° Ð·Ð½Ð°Ð¼Ðµ?",
  q_capital:"ÐÐ° ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ð¿Ñ€Ð¸Ð½Ð°Ð´Ð»ÐµÐ¶Ð¸ Ñ‚Ð°Ð·Ð¸ ÑÑ‚Ð¾Ð»Ð¸Ñ†Ð°?",q_river:"Ð’ ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ñ‚ÐµÑ‡Ðµ Ñ‚Ð°Ð·Ð¸ Ñ€ÐµÐºÐ°?",
  q_landmark:"Ð’ ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° ÑÐµ Ð½Ð°Ð¼Ð¸Ñ€Ð° Ñ‚Ð°Ð·Ð¸ Ð·Ð°Ð±ÐµÐ»ÐµÐ¶Ð¸Ñ‚ÐµÐ»Ð½Ð¾ÑÑ‚?",q_park:"Ð’ ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° ÑÐµ Ð½Ð°Ð¼Ð¸Ñ€Ð° Ñ‚Ð¾Ð·Ð¸ Ð½Ð°Ñ†Ð¸Ð¾Ð½Ð°Ð»ÐµÐ½ Ð¿Ð°Ñ€Ðº?",
  q_unesco:"Ð’ ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° ÑÐµ Ð½Ð°Ð¼Ð¸Ñ€Ð° Ñ‚Ð¾Ð²Ð° Ð®ÐÐ•Ð¡ÐšÐž Ð½Ð°ÑÐ»ÐµÐ´ÑÑ‚Ð²Ð¾?",q_citymark:"ÐÐ° ÐºÐ¾Ð¹ Ð³Ñ€Ð°Ð´ Ð¿Ñ€Ð¸Ð½Ð°Ð´Ð»ÐµÐ¶Ð¸ Ñ‚Ð°Ð·Ð¸ Ð·Ð°Ð±ÐµÐ»ÐµÐ¶Ð¸Ñ‚ÐµÐ»Ð½Ð¾ÑÑ‚?",
  q_subway:"Ð’ ÐºÐ¾Ð¹ Ð³Ñ€Ð°Ð´ Ðµ Ñ‚Ð¾Ð²Ð° Ð¼ÐµÑ‚Ñ€Ð¾?",q_flagsel:"ÐšÐ¾Ðµ Ð·Ð½Ð°Ð¼Ðµ Ð¿Ñ€Ð¸Ð½Ð°Ð´Ð»ÐµÐ¶Ð¸ Ð½Ð°â€¦",
  q_rcapital:"ÐšÐ°ÐºÐ²Ð° Ðµ ÑÑ‚Ð¾Ð»Ð¸Ñ†Ð°Ñ‚Ð° Ð½Ð°â€¦?",q_rcity:"ÐšÐ¾Ð¹ Ð³Ñ€Ð°Ð´ ÑÐµ Ð½Ð°Ð¼Ð¸Ñ€Ð° Ð²â€¦?",
  q_rriver:"ÐšÐ¾Ñ Ñ€ÐµÐºÐ° Ñ‚ÐµÑ‡Ðµ Ð¿Ñ€ÐµÐ·â€¦?",q_outline:"ÐšÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ð¸Ð¼Ð° Ñ‚Ð°Ð·Ð¸ Ñ„Ð¾Ñ€Ð¼Ð°?",
  q_food:"ÐžÑ‚ ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ð¸Ð´Ð²Ð° Ñ‚Ð¾Ð²Ð° ÑÑÑ‚Ð¸Ðµ?",q_brand:"ÐžÑ‚ ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ð¸Ð´Ð²Ð° Ñ‚Ð°Ð·Ð¸ Ð¼Ð°Ñ€ÐºÐ°?",
  q_currency:"ÐÐ° ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ð¿Ñ€Ð¸Ð½Ð°Ð´Ð»ÐµÐ¶Ð¸ Ñ‚Ð°Ð·Ð¸ Ð²Ð°Ð»ÑƒÑ‚Ð°?",q_curr_real:"ÐšÐ°ÐºÐ²Ð° Ð²Ð°Ð»ÑƒÑ‚Ð° Ð¸Ð¼Ð°â€¦",
  q_pop_compare:"ÐŸÐ¾Ð²ÐµÑ‡Ðµ Ð¸Ð»Ð¸ Ð¿Ð¾-Ð¼Ð°Ð»ÐºÐ¾ Ð¶Ð¸Ñ‚ÐµÐ»Ð¸?",
  q_hl_pop:"ÐŸÐ¾Ð²ÐµÑ‡Ðµ Ð¶Ð¸Ñ‚ÐµÐ»Ð¸ Ð¾Ñ‚ {a}?",q_hl_river:"ÐŸÐ¾-Ð´ÑŠÐ»Ð³Ð° Ð¾Ñ‚ {a}?",q_hl_area:"ÐŸÐ¾-Ð³Ð¾Ð»ÑÐ¼Ð° Ð¾Ñ‚ {a}?",
  q_neighbor:"ÐšÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ð³Ñ€Ð°Ð½Ð¸Ñ‡Ð¸ Ñâ€¦?",q_neighbor_not:"ÐÐ• Ð³Ñ€Ð°Ð½Ð¸Ñ‡Ð¸ Ñâ€¦?",
  q_plates_casual:"ÐžÑ‚ ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ðµ Ñ‚Ð°Ð·Ð¸ Ñ‚Ð°Ð±ÐµÐ»Ð°?",q_plates_hard:"Ð˜Ð´ÐµÐ½Ñ‚Ð¸Ñ„Ð¸Ñ†Ð¸Ñ€Ð°Ð¹Ñ‚Ðµ Ñ€ÐµÐ³Ð¸Ð¾Ð½Ð° â€” Ð±ÐµÐ· Ð¿Ð¾Ð´ÑÐºÐ°Ð·ÐºÐ°!",
  q_river_real:"ÐŸÑ€ÐµÐ· ÐºÐ¾Ñ ÑÑ‚Ñ€Ð°Ð½Ð° Ñ‚ÐµÑ‡Ðµ Ñ‚Ð°Ð·Ð¸ Ñ€ÐµÐºÐ°?",q_map_guess:"ÐÐ°Ð¼ÐµÑ€Ð¸ ÑÑ‚Ñ€Ð°Ð½Ð°Ñ‚Ð° Ð½Ð° ÐºÐ°Ñ€Ñ‚Ð°Ñ‚Ð°",
  fb_correct:"âœ“ ÐŸÑ€Ð°Ð²Ð¸Ð»Ð½Ð¾! +{pts}",fb_wrong:"âœ— Ð“Ñ€ÐµÑˆÐ½Ð¾ â†’ {ans}",fb_time:"â± Ð’Ñ€ÐµÐ¼ÐµÑ‚Ð¾ Ð¸Ð·Ñ‚ÐµÑ‡Ðµ! â†’ {ans}",
  plates_more:"+{n} oÑ‰e",pct_complete:"{pct}% Ð·Ð°Ð²ÑŠÑ€ÑˆÐµÐ½Ð¾",
  spotter_dup:"ðŸ“‹ {code} ({country}) Ð²ÐµÑ‡e ÑÑŠÐ±Ñ€Ð°Ð½Ð¾!",
  map_unavail:"ÐšÐ°Ñ€Ñ‚Ð°Ñ‚Ð° Ð½Ðµ Ðµ Ð´Ð¾ÑÑ‚ÑŠÐ¿Ð½Ð°",map_loading:"Ð—Ð°Ñ€ÐµÐ¶Ð´Ð°Ð½Ðµ Ð½Ð° ÐºÐ°Ñ€Ñ‚Ð°Ñ‚Ð°â€¦",
  q_subway_km:"ÐšÐ¾Ð»ÐºÐ¾ Ð´ÑŠÐ»Ð³Ð° Ðµ Ð¼ÐµÑ‚Ñ€Ð¾Ñ‚Ð¾ â€¦ (km)?",q_subway_lines:"ÐšÐ¾Ð»ÐºÐ¾ Ð¼ÐµÑ‚Ñ€Ð¾Ð»Ð¸Ð½Ð¸Ð¸ Ð¸Ð¼Ð° â€¦?",
  diff_desc_casual:"\u{1F7E2} Casual: Ð Ð°Ð·Ñ…Ð¾Ð´ÐµÐ½ Â· Ð‘ÐµÐ· Ð»Ð¸Ð¼Ð¸Ñ‚ Â· âˆž Ð–Ð¸Ð²Ð¾Ñ‚Ð°",diff_desc_hc:"\u{1F525} Hardcore: ÐšÐ»Ð°ÑÐ¸Ðº Â· Ð‘ÐµÐ· Ð»Ð¸Ð¼Ð¸Ñ‚ Â· 3 Ð–Ð¸Ð²Ð¾Ñ‚Ð°",diff_desc_surv:"\u{1F480} Survival: Ð¡Ñ€ÐµÑ‰Ñƒ Ð²Ñ€ÐµÐ¼ÐµÑ‚Ð¾ Â· 8Ñ Â· 3 Ð–Ð¸Ð²Ð¾Ñ‚Ð°",hud_lives:"Ð–Ð˜Ð’ÐžÐ¢Ð",score_mult_max:"ÐœÐ°ÐºÑ ÐœÐ½Ð¾Ð¶Ð¸Ñ‚ÐµÐ»",score_time_bonus:"Ð’Ñ€ÐµÐ¼ÐµÐ² Ð‘Ð¾Ð½ÑƒÑ",pts_abbr:"Ñ‚.",score_correct_lbl:"Ð¿Ñ€Ð°Ð²Ð¸Ð»Ð½Ð¾",mode_wappen:"Ð“ÐµÑ€Ð±Ð¾Ð²Ðµ",mode_slf:"Ð“Ñ€Ð°Ð´-Ð¡Ñ‚Ñ€Ð°Ð½Ð°-Ð ÐµÐºÐ°",mode_euro:"Ð•Ð²Ñ€Ð¾Ð¼Ð¾Ð½ÐµÑ‚Ð¸"
},
el:{
  play:"Î Î‘Î™ÎžÎ•",again:"Î Î‘Î™ÎžÎ• ÎžÎ‘ÎÎ‘",menu:"ÎšÏÏÎ¹Î¿ Î¼ÎµÎ½Î¿Ï",board:"ÎšÎ±Ï„Î¬Ï„Î±Î¾Î·",pass:"Î”Î¹Î±Î²Î±Ï„Î®ÏÎ¹Î¿",
  profile:"Î ÏÎ¿Ï†Î¯Î»",stats:"Î£Ï„Î±Ï„Î¹ÏƒÏ„Î¹ÎºÎ¬",casual:"Î•ÏÎºÎ¿Î»Î¿",hardcore:"Î”ÏÏƒÎºÎ¿Î»Î¿",rounds:"Î“ÏÏÎ¿Î¹",
  btn_collect:"Î£Ï…Î»Î»Î¿Î³Î®",btn_back:"Î Î¯ÏƒÏ‰ ÏƒÏ„Î¿ Î¼ÎµÎ½Î¿Ï",btn_next:"Î•Ï€ÏŒÎ¼ÎµÎ½Î¿ â†’",
  btn_again:"Î Î±Î¯Î¾Îµ Î¾Î±Î½Î¬",btn_menu:"ÎšÏÏÎ¹Î¿ Î¼ÎµÎ½Î¿Ï",btn_adapt:"Î ÏÎ¿ÏƒÎ±ÏÎ¼Î¿Î³Î®",
  spotter_title:"\u{1F697} Spotter Î¤Î±Î¾Î¹Î´Î¹Î¿Ï",
  spotter_hint:"Î•Î¯Î´ÎµÏ‚ Ï€Î¹Î½Î±ÎºÎ¯Î´Î±; ÎšÎ±Ï„Î±Ï‡ÏŽÏÎ·ÏƒÎ­ Ï„Î·Î½ Ï„ÏŽÏÎ±!",
  spotter_all:"ÎŒÎ»ÎµÏ‚ Î¿Î¹ Ï‡ÏŽÏÎµÏ‚",spotter_unknown:"Î†Î³Î½Ï‰ÏƒÏ„Î· Ï€Î¹Î½Î±ÎºÎ¯Î´Î±",
  spotter_not_in:"Î´ÎµÎ½ ÎµÎ¯Î½Î±Î¹ ÏƒÎµ",spotter_but_in:"Î±Î»Î»Î¬ ÏƒÎµ",
  album_title:"\u{1F4D4} Î£Ï…Î»Î»Î¿Î³Î® Ï€Î¹Î½Î±ÎºÎ¯Î´Ï‰Î½",album_list:"\u{1F4DD} Î›Î¯ÏƒÏ„Î±",album_map:"\u{1F5FA} Î§Î¬ÏÏ„Î·Ï‚",
  album_empty_country:"Î¤Î¯Ï€Î¿Ï„Î± Î±Ï€ÏŒ {country} Î±ÎºÏŒÎ¼Î± â€” Ï‡ÏÎ·ÏƒÎ¹Î¼Î¿Ï€Î¿Î¯Î·ÏƒÎµ Ï„Î¿ Spotter!",
  album_empty:"Î”ÎµÎ½ Î­Ï‡ÎµÎ¹Ï‚ ÏƒÏ…Î»Î»Î­Î¾ÎµÎ¹ Ï„Î¯Ï€Î¿Ï„Î± Î±ÎºÏŒÎ¼Î±!\nÎ Î±Î¯Î¾Îµ Ï€Î¹Î½Î±ÎºÎ¯Î´ÎµÏ‚ Î•Î• Î® Ï‡ÏÎ·ÏƒÎ¹Î¼Î¿Ï€Î¿Î¯Î·ÏƒÎµ Ï„Î¿ Spotter.",
  album_codes:"ÎºÏ‰Î´Î¹ÎºÎ¿Î¯",
  hl_higher:"â¬†ï¸ Î ÎµÏÎ¹ÏƒÏƒÏŒÏ„ÎµÏÎ¿ / ÎœÎµÎ³Î±Î»ÏÏ„ÎµÏÎ¿ / ÎœÎµÎ³Î±Î»ÏÏ„ÎµÏÎ¿",hl_lower:"â¬‡ï¸ Î›Î¹Î³ÏŒÏ„ÎµÏÎ¿ / ÎœÎ¹ÎºÏÏŒÏ„ÎµÏÎ¿ / ÎœÎ¹ÎºÏÏŒÏ„ÎµÏÎ¿",
  hl_more:"â¬†ï¸ Î ÎµÏÎ¹ÏƒÏƒÏŒÏ„ÎµÏÎ¿Î¹ ÎºÎ¬Ï„Î¿Î¹ÎºÎ¿Î¹",hl_less:"â¬‡ï¸ Î›Î¹Î³ÏŒÏ„ÎµÏÎ¿Î¹ ÎºÎ¬Ï„Î¿Î¹ÎºÎ¿Î¹",
  loc_detected:"Î’ÏÎ¯ÏƒÎºÎµÏƒÏ„Îµ ÏƒÏ„Î·Î½/ÏƒÏ„Î¿ {country}",loc_adapt:"Î ÏÎ¿ÏƒÎ±ÏÎ¼Î¿Î³Î®",
  q_city:"Î£Îµ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Î²ÏÎ¯ÏƒÎºÎµÏ„Î±Î¹ Î±Ï…Ï„Î® Î· Ï€ÏŒÎ»Î·;",q_flag:"Î Î¿Î¹Î± Ï‡ÏŽÏÎ± Î­Ï‡ÎµÎ¹ Î±Ï…Ï„Î® Ï„Î· ÏƒÎ·Î¼Î±Î¯Î±;",
  q_capital:"Î£Îµ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Î±Î½Î®ÎºÎµÎ¹ Î±Ï…Ï„Î® Î· Ï€ÏÏ‰Ï„ÎµÏÎ¿Ï…ÏƒÎ±;",q_river:"Î£Îµ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Î²ÏÎ¯ÏƒÎºÎµÏ„Î±Î¹ Î±Ï…Ï„ÏŒ Ï„Î¿ Ï€Î¿Ï„Î¬Î¼Î¹;",
  q_landmark:"Î£Îµ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Î²ÏÎ¯ÏƒÎºÎµÏ„Î±Î¹ Î±Ï…Ï„ÏŒ Ï„Î¿ Î¼Î½Î·Î¼ÎµÎ¯Î¿;",q_park:"Î£Îµ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Î²ÏÎ¯ÏƒÎºÎµÏ„Î±Î¹ Î±Ï…Ï„ÏŒ Ï„Î¿ ÎµÎ¸Î½Î¹ÎºÏŒ Ï€Î¬ÏÎºÎ¿;",
  q_unesco:"Î£Îµ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Î²ÏÎ¯ÏƒÎºÎµÏ„Î±Î¹ Î±Ï…Ï„ÏŒ Ï„Î¿ Î¼Î½Î·Î¼ÎµÎ¯Î¿ UNESCO;",q_citymark:"Î£Îµ Ï€Î¿Î¹Î± Ï€ÏŒÎ»Î· Î±Î½Î®ÎºÎµÎ¹ Î±Ï…Ï„ÏŒ Ï„Î¿ Î¼Î½Î·Î¼ÎµÎ¯Î¿;",
  q_subway:"Î£Îµ Ï€Î¿Î¹Î± Ï€ÏŒÎ»Î· Î²ÏÎ¯ÏƒÎºÎµÏ„Î±Î¹ Î±Ï…Ï„ÏŒ Ï„Î¿ Î¼ÎµÏ„ÏÏŒ;",q_flagsel:"Î Î¿Î¹Î± ÏƒÎ·Î¼Î±Î¯Î± Î±Î½Î®ÎºÎµÎ¹ ÏƒÏ„Î·â€¦",
  q_rcapital:"Î Î¿Î¹Î± ÎµÎ¯Î½Î±Î¹ Î· Ï€ÏÏ‰Ï„ÎµÏÎ¿Ï…ÏƒÎ± Ï„Î·Ï‚/Ï„Î¿Ï…â€¦;",q_rcity:"Î Î¿Î¹Î± Ï€ÏŒÎ»Î· Î²ÏÎ¯ÏƒÎºÎµÏ„Î±Î¹ ÏƒÏ„Î·/ÏƒÏ„Î¿â€¦;",
  q_rriver:"Î Î¿Î¹Î¿ Ï€Î¿Ï„Î¬Î¼Î¹ Î´Î¹Î±ÏÏÎ­ÎµÎ¹ Ï„Î·/Ï„Î¿â€¦;",q_outline:"Î Î¿Î¹Î± Ï‡ÏŽÏÎ± Î­Ï‡ÎµÎ¹ Î±Ï…Ï„ÏŒ Ï„Î¿ ÏƒÏ‡Î®Î¼Î±;",
  q_food:"Î‘Ï€ÏŒ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Ï€ÏÎ¿Î­ÏÏ‡ÎµÏ„Î±Î¹ Î±Ï…Ï„ÏŒ Ï„Î¿ Ï€Î¹Î¬Ï„Î¿;",q_brand:"Î‘Ï€ÏŒ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Ï€ÏÎ¿Î­ÏÏ‡ÎµÏ„Î±Î¹ Î±Ï…Ï„Î® Î· Î¼Î¬ÏÎºÎ±;",
  q_currency:"Î£Îµ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Î±Î½Î®ÎºÎµÎ¹ Î±Ï…Ï„ÏŒ Ï„Î¿ Î½ÏŒÎ¼Î¹ÏƒÎ¼Î±;",q_curr_real:"Î Î¿Î¹Î¿ Î½ÏŒÎ¼Î¹ÏƒÎ¼Î± Î­Ï‡ÎµÎ¹ Î·/Î¿â€¦",
  q_pop_compare:"Î ÎµÏÎ¹ÏƒÏƒÏŒÏ„ÎµÏÎ¿Î¹ Î® Î»Î¹Î³ÏŒÏ„ÎµÏÎ¿Î¹ ÎºÎ¬Ï„Î¿Î¹ÎºÎ¿Î¹;",
  q_hl_pop:"Î ÎµÏÎ¹ÏƒÏƒÏŒÏ„ÎµÏÎ¿Î¹ ÎºÎ¬Ï„Î¿Î¹ÎºÎ¿Î¹ Î±Ï€ÏŒ Ï„Î·/Ï„Î¿Î½ {a};",q_hl_river:"ÎœÎµÎ³Î±Î»ÏÏ„ÎµÏÎ¿ Î±Ï€ÏŒ Ï„Î·/Ï„Î¿Î½ {a};",q_hl_area:"ÎœÎµÎ³Î±Î»ÏÏ„ÎµÏÎ· Î±Ï€ÏŒ Ï„Î·/Ï„Î¿Î½ {a};",
  q_neighbor:"Î Î¿Î¹Î± Ï‡ÏŽÏÎ± ÏƒÏ…Î½Î¿ÏÎµÏÎµÎ¹ Î¼Îµ Ï„Î·/Ï„Î¿â€¦;",q_neighbor_not:"Î”Î•Î ÏƒÏ…Î½Î¿ÏÎµÏÎµÎ¹ Î¼Îµ Ï„Î·/Ï„Î¿â€¦;",
  q_plates_casual:"Î‘Ï€ÏŒ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± ÎµÎ¯Î½Î±Î¹ Î±Ï…Ï„Î® Î· Ï€Î¹Î½Î±ÎºÎ¯Î´Î±;",q_plates_hard:"Î‘Î½Î±Î³Î½Ï‰ÏÎ¯ÏƒÏ„Îµ Ï„Î·Î½ Ï€ÎµÏÎ¹Î¿Ï‡Î® â€” Ï‡Ï‰ÏÎ¯Ï‚ Ï…Ï€ÏŒÎ´ÎµÎ¹Î¾Î·!",
  q_river_real:"ÎœÎ­ÏƒÎ± Î±Ï€ÏŒ Ï€Î¿Î¹Î± Ï‡ÏŽÏÎ± Î´Î¹Î±ÏÏÎ­ÎµÎ¹ Î±Ï…Ï„ÏŒ Ï„Î¿ Ï€Î¿Ï„Î¬Î¼Î¹;",q_map_guess:"Î’ÏÎµÏ‚ Ï„Î· Ï‡ÏŽÏÎ± ÏƒÏ„Î¿Î½ Ï‡Î¬ÏÏ„Î·",
  fb_correct:"âœ“ Î£Ï‰ÏƒÏ„ÏŒ! +{pts}",fb_wrong:"âœ— Î›Î¬Î¸Î¿Ï‚ â†’ {ans}",fb_time:"â± Î¤Î­Î»Î¿Ï‚ Ï‡ÏÏŒÎ½Î¿Ï…! â†’ {ans}",
  plates_more:"+{n} Î±ÎºÏŒÎ¼Î±",pct_complete:"{pct}% Î¿Î»Î¿ÎºÎ»Î·ÏÏŽÎ¸Î·ÎºÎµ",
  spotter_dup:"ðŸ“‹ {code} ({country}) Î®Î´Î· ÏƒÏ…Î»Î»Î­Ï‡Î¸Î·ÎºÎµ!",
  map_unavail:"Î§Î¬ÏÏ„Î·Ï‚ Î¼Î· Î´Î¹Î±Î¸Î­ÏƒÎ¹Î¼Î¿Ï‚",map_loading:"Î¦ÏŒÏÏ„Ï‰ÏƒÎ· Ï‡Î¬ÏÏ„Î·â€¦",
  q_subway_km:"Î ÏŒÏƒÎ¿ Î¼Î±ÎºÏÏ ÎµÎ¯Î½Î±Î¹ Ï„Î¿ Î¼ÎµÏ„ÏÏŒ â€¦ (km)?",q_subway_lines:"Î ÏŒÏƒÎµÏ‚ Î³ÏÎ±Î¼Î¼Î­Ï‚ Î¼ÎµÏ„ÏÏŒ Î­Ï‡ÎµÎ¹ â€¦?",
  diff_desc_casual:"\u{1F7E2} Casual: Î‘Î½ÎµÏ„Î¿ Â· Î§Ï‰ÏÎ¯Ï‚ ÏŒÏÎ¹Î¿ Â· âˆž Î–Ï‰Î­Ï‚",diff_desc_hc:"\u{1F525} Hardcore: ÎšÎ»Î±ÏƒÎ¹ÎºÏŒ Â· Î§Ï‰ÏÎ¯Ï‚ ÏŒÏÎ¹Î¿ Â· 3 Î–Ï‰Î­Ï‚",diff_desc_surv:"\u{1F480} Survival: Î•Î½Î±Î½Ï„Î¯Î¿Î½ Ï‡ÏÏŒÎ½Î¿Ï… Â· 8Î´Î» Â· 3 Î–Ï‰Î­Ï‚",hud_lives:"Î–Î©Î•Î£",score_mult_max:"ÎœÎ­Î³Î¹ÏƒÏ„Î¿Ï‚ Î Î¿Î»Î»Î±Ï€Î»Î±ÏƒÎ¹Î±ÏƒÏ„Î®Ï‚",score_time_bonus:"ÎœÏ€ÏŒÎ½Î¿Ï…Ï‚ Î§ÏÏŒÎ½Î¿Ï…",pts_abbr:"Î¼ÏŒÏ.",score_correct_lbl:"ÏƒÏ‰ÏƒÏ„Î¬",mode_wappen:"Î•Î¸Î½ÏŒÏƒÎ·Î¼Î±",mode_slf:"Î ÏŒÎ»Î·-Î§ÏŽÏÎ±-Î Î¿Ï„Î¬Î¼Î¹",mode_euro:"ÎšÎ­ÏÎ¼Î±Ï„Î± Î•Ï…ÏÏŽ"
},
da:{
  play:"SPIL",again:"SPIL IGEN",menu:"Hovedmenu",board:"Rangliste",pass:"Pas",
  profile:"Profil",stats:"Statistik",casual:"Casual",hardcore:"Hardcore",rounds:"Runder",
  btn_collect:"Samle",btn_back:"Tilbage til menu",btn_next:"NÃ¦ste â†’",
  btn_again:"Spil igen",btn_menu:"Hovedmenu",btn_adapt:"Tilpas",
  spotter_title:"\u{1F697} Rejse-Spotter",
  spotter_hint:"Set en nummerplade? NotÃ©r den nu!",
  spotter_all:"Alle lande",spotter_unknown:"Ukendt nummerplade",
  spotter_not_in:"ikke i",spotter_but_in:"men i",
  album_title:"\u{1F4D4} Nummerplade-album",album_list:"\u{1F4DD} Liste",album_map:"\u{1F5FA} Kort",
  album_empty_country:"Intet fra {country} endnu â€” brug Spotter!",
  album_empty:"Intet indsamlet endnu!\nSpil EU-nummerplader eller brug Spotter.",
  album_codes:"koder",
  hl_higher:"â¬†ï¸ Mere / LÃ¦ngere / StÃ¸rre",hl_lower:"â¬‡ï¸ Mindre / Kortere / Mindre",
  hl_more:"â¬†ï¸ Flere indbyggere",hl_less:"â¬‡ï¸ FÃ¦rre indbyggere",
  loc_detected:"Du er i {country}",loc_adapt:"Tilpas",
  q_city:"I hvilket land ligger denne by?",q_flag:"Hvilket land har dette flag?",
  q_capital:"Hvilke land tilhÃ¸rer denne hovedstad?",q_river:"I hvilket land lÃ¸ber denne flod?",
  q_landmark:"I hvilket land ligger dette monument?",q_park:"I hvilket land ligger denne nationalpark?",
  q_unesco:"I hvilket land ligger dette UNESCO-sted?",q_citymark:"Hvilken by tilhÃ¸rer dette monument?",
  q_subway:"I hvilken by er denne metro?",q_flagsel:"Hvilket flag tilhÃ¸rerâ€¦",
  q_rcapital:"Hvad er hovedstaden iâ€¦?",q_rcity:"Hvilken by ligger iâ€¦?",
  q_rriver:"Hvilken flod lÃ¸ber gennemâ€¦?",q_outline:"Hvilket land har denne form?",
  q_food:"Fra hvilket land kommer denne ret?",q_brand:"Fra hvilket land kommer dette mÃ¦rke?",
  q_currency:"Hvilket land tilhÃ¸rer denne valuta?",q_curr_real:"Hvilken valuta harâ€¦",
  q_pop_compare:"Flere eller fÃ¦rre indbyggere?",
  q_hl_pop:"Flere indbyggere end {a}?",q_hl_river:"LÃ¦ngere end {a}?",q_hl_area:"StÃ¸rre end {a}?",
  q_neighbor:"Hvilket land grÃ¦nser op tilâ€¦?",q_neighbor_not:"GrÃ¦nser IKKE op tilâ€¦?",
  q_plates_casual:"Fra hvilket land er denne nummerplade?",q_plates_hard:"IdentificÃ©r regionen â€” ingen hint!",
  q_river_real:"Gennem hvilket land lÃ¸ber denne flod?",q_map_guess:"Find landet pÃ¥ kortet",
  fb_correct:"âœ“ Korrekt! +{pts}",fb_wrong:"âœ— Forkert â†’ {ans}",fb_time:"â± Tid! â†’ {ans}",
  plates_more:"+{n} mere",pct_complete:"{pct}% fuldfÃ¸rt",
  spotter_dup:"ðŸ“‹ {code} ({country}) allerede indsamlet!",
  map_unavail:"Kort ikke tilgÃ¦ngeligt",map_loading:"IndlÃ¦ser kortâ€¦",
  q_subway_km:"Hvor lang er metronetvÃ¦rket â€¦ (km)?",q_subway_lines:"Hvor mange metrolinjer har â€¦?",
  diff_desc_casual:"\u{1F7E2} Casual: Afslappet Â· Ingen tidsgrÃ¦nse Â· âˆž Liv",diff_desc_hc:"\u{1F525} Hardcore: Klassisk Â· Ingen tidsgrÃ¦nse Â· 3 Liv",diff_desc_surv:"\u{1F480} Survival: Mod uret Â· 8s Â· 3 Liv",hud_lives:"LIV",score_mult_max:"Maks Multiplikator",score_time_bonus:"Tidsbonus",pts_abbr:"pt.",score_correct_lbl:"korrekt",mode_wappen:"VÃ¥benskjolde",mode_slf:"By-Land-Flod",mode_euro:"EuromÃ¸nter"
},
sv:{
  play:"SPELA",again:"SPELA IGEN",menu:"Huvudmeny",board:"Rankningslista",pass:"Pass",
  profile:"Profil",stats:"Statistik",casual:"Casual",hardcore:"Hardcore",rounds:"Rundor",
  btn_collect:"Samla",btn_back:"Tillbaka till menyn",btn_next:"NÃ¤sta â†’",
  btn_again:"Spela igen",btn_menu:"Huvudmeny",btn_adapt:"Anpassa",
  spotter_title:"\u{1F697} Resespotter",
  spotter_hint:"Sett en skylt? Notera den nu!",
  spotter_all:"Alla lÃ¤nder",spotter_unknown:"OkÃ¤nd skylt",
  spotter_not_in:"inte i",spotter_but_in:"men i",
  album_title:"\u{1F4D4} Skyltalbum",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Karta",
  album_empty_country:"Inget frÃ¥n {country} Ã¤nnu â€” anvÃ¤nd Spotter!",
  album_empty:"Inget samlat Ã¤nnu!\nSpela EU-skyltar eller anvÃ¤nd Spotter.",
  album_codes:"koder",
  hl_higher:"â¬†ï¸ Mer / LÃ¤ngre / StÃ¶rre",hl_lower:"â¬‡ï¸ Mindre / Kortare / Mindre",
  hl_more:"â¬†ï¸ Fler invÃ¥nare",hl_less:"â¬‡ï¸ FÃ¤rre invÃ¥nare",
  loc_detected:"Du Ã¤r i {country}",loc_adapt:"Anpassa",
  q_city:"I vilket land ligger den hÃ¤r staden?",q_flag:"Vilket land har den hÃ¤r flaggan?",
  q_capital:"Vilket land tillhÃ¶r den hÃ¤r huvudstaden?",q_river:"I vilket land flÃ¶dar den hÃ¤r floden?",
  q_landmark:"I vilket land finns det hÃ¤r monumentet?",q_park:"I vilket land finns den hÃ¤r nationalparken?",
  q_unesco:"I vilket land finns det hÃ¤r UNESCO-arvet?",q_citymark:"Vilken stad tillhÃ¶r det hÃ¤r monumentet?",
  q_subway:"I vilken stad finns den hÃ¤r tunnelbanan?",q_flagsel:"Vilken flagga tillhÃ¶râ€¦",
  q_rcapital:"Vad Ã¤r huvudstaden iâ€¦?",q_rcity:"Vilken stad finns iâ€¦?",
  q_rriver:"Vilken flod rinner genomâ€¦?",q_outline:"Vilket land har den hÃ¤r formen?",
  q_food:"FrÃ¥n vilket land kommer den hÃ¤r rÃ¤tten?",q_brand:"FrÃ¥n vilket land kommer det hÃ¤r mÃ¤rket?",
  q_currency:"Vilket land tillhÃ¶r den hÃ¤r valutan?",q_curr_real:"Vilken valuta harâ€¦",
  q_pop_compare:"Fler eller fÃ¤rre invÃ¥nare?",
  q_hl_pop:"Fler invÃ¥nare Ã¤n {a}?",q_hl_river:"LÃ¤ngre Ã¤n {a}?",q_hl_area:"StÃ¶rre Ã¤n {a}?",
  q_neighbor:"Vilket land grÃ¤nsar tillâ€¦?",q_neighbor_not:"GrÃ¤nsar INTE tillâ€¦?",
  q_plates_casual:"FrÃ¥n vilket land Ã¤r den hÃ¤r skylten?",q_plates_hard:"Identifiera regionen â€” inget tips!",
  q_river_real:"Genom vilket land flÃ¶dar den hÃ¤r floden?",q_map_guess:"Hitta landet pÃ¥ kartan",
  fb_correct:"âœ“ RÃ¤tt! +{pts}",fb_wrong:"âœ— Fel â†’ {ans}",fb_time:"â± Tid! â†’ {ans}",
  plates_more:"+{n} till",pct_complete:"{pct}% klart",
  spotter_dup:"ðŸ“‹ {code} ({country}) redan insamlat!",
  map_unavail:"Karta ej tillgÃ¤nglig",map_loading:"Laddar kartaâ€¦",
  q_subway_km:"Hur lÃ¥ng Ã¤r tunnelbanenÃ¤tet â€¦ (km)?",q_subway_lines:"Hur mÃ¥nga tunnelbanelinjer har â€¦?",
  diff_desc_casual:"\u{1F7E2} Casual: Avslappnad Â· Ingen tidsgrÃ¤ns Â· âˆž Liv",diff_desc_hc:"\u{1F525} Hardcore: Klassisk Â· Ingen tidsgrÃ¤ns Â· 3 Liv",diff_desc_surv:"\u{1F480} Survival: Mot klockan Â· 8s Â· 3 Liv",hud_lives:"LIV",score_mult_max:"Max Multiplikator",score_time_bonus:"Tidsbonus",pts_abbr:"pt.",score_correct_lbl:"rÃ¤tt",mode_wappen:"Vapen",mode_slf:"Stad-Land-Flod",mode_euro:"Euromynt"
},
fi:{
  play:"PELAA",again:"PELAA UUDELLEEN",menu:"PÃ¤Ã¤valikko",board:"Tulostaulukko",pass:"Passi",
  profile:"Profiili",stats:"Tilastot",casual:"Helppo",hardcore:"Vaikea",rounds:"Kierrokset",
  btn_collect:"KerÃ¤Ã¤",btn_back:"Takaisin pÃ¤Ã¤valikkoon",btn_next:"Seuraava â†’",
  btn_again:"Pelaa uudelleen",btn_menu:"PÃ¤Ã¤valikko",btn_adapt:"Muokkaa",
  spotter_title:"\u{1F697} Matkaspotter",
  spotter_hint:"NÃ¤itkÃ¶ rekisterikilven? Kirjaa se heti!",
  spotter_all:"Kaikki maat",spotter_unknown:"Tuntematon rekisterikilpi",
  spotter_not_in:"ei kohteessa",spotter_but_in:"mutta kohteessa",
  album_title:"\u{1F4D4} Rekisterikilpialbumi",album_list:"\u{1F4DD} Luettelo",album_map:"\u{1F5FA} Kartta",
  album_empty_country:"Ei vielÃ¤ mitÃ¤Ã¤n kohteesta {country} â€” kÃ¤ytÃ¤ Spotteria!",
  album_empty:"Ei vielÃ¤ kerÃ¤tty mitÃ¤Ã¤n!\nPelaa EU-rekisterikilpiÃ¤ tai kÃ¤ytÃ¤ Spotteria.",
  album_codes:"koodit",
  hl_higher:"â¬†ï¸ EnemmÃ¤n / Pidempi / Suurempi",hl_lower:"â¬‡ï¸ VÃ¤hemmÃ¤n / Lyhyempi / Pienempi",
  hl_more:"â¬†ï¸ EnemmÃ¤n asukkaita",hl_less:"â¬‡ï¸ VÃ¤hemmÃ¤n asukkaita",
  loc_detected:"Olet kohteessa {country}",loc_adapt:"Muokkaa",
  q_city:"MissÃ¤ maassa tÃ¤mÃ¤ kaupunki sijaitsee?",q_flag:"MinkÃ¤ maan tÃ¤mÃ¤ lippu on?",
  q_capital:"Mille maalle tÃ¤mÃ¤ pÃ¤Ã¤kaupunki kuuluu?",q_river:"MissÃ¤ maassa tÃ¤mÃ¤ joki sijaitsee?",
  q_landmark:"MissÃ¤ maassa tÃ¤mÃ¤ nÃ¤htÃ¤vyys sijaitsee?",q_park:"MissÃ¤ maassa tÃ¤mÃ¤ kansallispuisto sijaitsee?",
  q_unesco:"MissÃ¤ maassa tÃ¤mÃ¤ UNESCO-kohde sijaitsee?",q_citymark:"Mille kaupungille tÃ¤mÃ¤ nÃ¤htÃ¤vyys kuuluu?",
  q_subway:"MissÃ¤ kaupungissa tÃ¤mÃ¤ metro on?",q_flagsel:"MikÃ¤ lippu kuuluuâ€¦",
  q_rcapital:"MikÃ¤ onâ€¦ pÃ¤Ã¤kaupunki?",q_rcity:"MikÃ¤ kaupunki sijaitseeâ€¦?",
  q_rriver:"MikÃ¤ joki virtaa lÃ¤piâ€¦?",q_outline:"MinkÃ¤ maan muoto tÃ¤mÃ¤ on?",
  q_food:"MistÃ¤ maasta tÃ¤mÃ¤ ruoka tulee?",q_brand:"MistÃ¤ maasta tÃ¤mÃ¤ merkki tulee?",
  q_currency:"MinkÃ¤ maan valuutta tÃ¤mÃ¤ on?",q_curr_real:"MikÃ¤ valuutta onâ€¦",
  q_pop_compare:"EnemmÃ¤n vai vÃ¤hemmÃ¤n asukkaita?",
  q_hl_pop:"EnemmÃ¤n asukkaita kuin {a}?",q_hl_river:"Pidempi kuin {a}?",q_hl_area:"Suurempi kuin {a}?",
  q_neighbor:"MikÃ¤ maa rajoittuuâ€¦?",q_neighbor_not:"EI rajoituâ€¦?",
  q_plates_casual:"MinkÃ¤ maan rekisterikilpi tÃ¤mÃ¤ on?",q_plates_hard:"Tunnista alue â€” ei vihjettÃ¤!",
  q_river_real:"MinkÃ¤ maan lÃ¤pi tÃ¤mÃ¤ joki virtaa?",q_map_guess:"Etsi maa kartalta",
  fb_correct:"âœ“ Oikein! +{pts}",fb_wrong:"âœ— VÃ¤Ã¤rin â†’ {ans}",fb_time:"â± Aika! â†’ {ans}",
  plates_more:"+{n} lisÃ¤Ã¤",pct_complete:"{pct}% valmis",
  spotter_dup:"ðŸ“‹ {code} ({country}) jo kerÃ¤tty!",
  map_unavail:"Kartta ei saatavilla",map_loading:"Ladataan karttaaâ€¦",
  q_subway_km:"Kuinka pitkÃ¤ on metroverkosto â€¦ (km)?",q_subway_lines:"Kuinka monta metrolinjaa on â€¦?",
  diff_desc_casual:"\u{1F7E2} Casual: Rento Â· Ei aikarajaa Â· âˆž ElÃ¤mÃ¤Ã¤",diff_desc_hc:"\u{1F525} Hardcore: Klassinen Â· Ei aikarajaa Â· 3 ElÃ¤mÃ¤Ã¤",diff_desc_surv:"\u{1F480} Survival: Aikaa vastaan Â· 8s Â· 3 ElÃ¤mÃ¤Ã¤",hud_lives:"ELÃ„MÃ„T",score_mult_max:"Maks Kerroin",score_time_bonus:"Aikabonus",pts_abbr:"p.",score_correct_lbl:"oikein",mode_wappen:"Vaakunat",mode_slf:"Kaupunki-Maa-Joki",mode_euro:"Eurokolikot"
},
et:{
  play:"MÃ„NGI",again:"MÃ„NGI UUESTI",menu:"PeamenÃ¼Ã¼",board:"Edetabel",pass:"Pass",
  profile:"Profiil",stats:"Statistika",casual:"Lihtne",hardcore:"Raske",rounds:"Voorud",
  btn_collect:"Kogu",btn_back:"Tagasi menÃ¼Ã¼sse",btn_next:"JÃ¤rgmine â†’",
  btn_again:"MÃ¤ngi uuesti",btn_menu:"PeamenÃ¼Ã¼",btn_adapt:"Kohanda",
  spotter_title:"\u{1F697} Reisispotter",
  spotter_hint:"NÃ¤gid numbrimÃ¤rki? Kirjuta kohe Ã¼les!",
  spotter_all:"KÃµik riigid",spotter_unknown:"Tundmatu numbrimÃ¤rk",
  spotter_not_in:"ei ole",spotter_but_in:"aga on",
  album_title:"\u{1F4D4} NumbrimÃ¤rkide album",album_list:"\u{1F4DD} Nimekiri",album_map:"\u{1F5FA} Kaart",
  album_empty_country:"Veel midagi {country} â€” kasuta Spotterit!",
  album_empty:"Veel midagi kogutud!\nMÃ¤ngi EL-i numbrimÃ¤rke vÃµi kasuta Spotterit.",
  album_codes:"koodid",
  hl_higher:"â¬†ï¸ Rohkem / Pikem / Suurem",hl_lower:"â¬‡ï¸ VÃ¤hem / LÃ¼hem / VÃ¤iksem",
  hl_more:"â¬†ï¸ Rohkem elanikke",hl_less:"â¬‡ï¸ VÃ¤hem elanikke",
  loc_detected:"Oled {country}",loc_adapt:"Kohanda",
  q_city:"Millises riigis see linn asub?",q_flag:"Millise riigi lipp see on?",
  q_capital:"Millisele riigile see pealinn kuulub?",q_river:"Millises riigis see jÃµgi voolab?",
  q_landmark:"Millises riigis see vaatamisvÃ¤Ã¤rsus asub?",q_park:"Millises riigis see rahvuspark asub?",
  q_unesco:"Millises riigis see UNESCO objekt asub?",q_citymark:"Millisele linnale see vaatamisvÃ¤Ã¤rsus kuulub?",
  q_subway:"Millises linnas see metroo on?",q_flagsel:"Milline lipp kuulubâ€¦",
  q_rcapital:"Mis onâ€¦ pealinn?",q_rcity:"Milline linn asubâ€¦?",
  q_rriver:"Milline jÃµgi voolab lÃ¤biâ€¦?",q_outline:"Millisel riigil on see kuju?",
  q_food:"Millisest riigist see roog pÃ¤rineb?",q_brand:"Millisest riigist see brÃ¤nd pÃ¤rineb?",
  q_currency:"Millisele riigile see valuuta kuulub?",q_curr_real:"Mis valuuta onâ€¦",
  q_pop_compare:"Rohkem vÃµi vÃ¤hem elanikke?",
  q_hl_pop:"Rohkem elanikke kui {a}?",q_hl_river:"Pikem kui {a}?",q_hl_area:"Suurem kui {a}?",
  q_neighbor:"Milline riik piirnebâ€¦?",q_neighbor_not:"EI piirneâ€¦?",
  q_plates_casual:"Millisest riigist see numbrimÃ¤rk on?",q_plates_hard:"Tuvasta piirkond â€” vihjeta!",
  q_river_real:"LÃ¤bi millise riigi see jÃµgi voolab?",q_map_guess:"Leia riik kaardilt",
  fb_correct:"âœ“ Ã•ige! +{pts}",fb_wrong:"âœ— Vale â†’ {ans}",fb_time:"â± Aeg! â†’ {ans}",
  plates_more:"+{n} veel",pct_complete:"{pct}% tÃ¤idetud",
  spotter_dup:"ðŸ“‹ {code} ({country}) juba kogutud!",
  map_unavail:"Kaart pole saadaval",map_loading:"Kaardi laadimineâ€¦",
  q_subway_km:"Kui pikk on metroovÃµrk â€¦ (km)?",q_subway_lines:"Kui palju metroliine on â€¦?",
  diff_desc_casual:"\u{1F7E2} Casual: LÃµÃµgastav Â· Pole ajalimiiti Â· âˆž Elu",diff_desc_hc:"\u{1F525} Hardcore: Klassikaline Â· Pole limiiti Â· 3 Elu",diff_desc_surv:"\u{1F480} Survival: Aja vastu Â· 8s Â· 3 Elu",hud_lives:"ELUD",score_mult_max:"Max Kordaja",score_time_bonus:"Ajaboonus",pts_abbr:"pt.",score_correct_lbl:"Ãµige",mode_wappen:"Vapid",mode_slf:"Linn-Maa-JÃµgi",mode_euro:"EuromÃ¼ndid"
},
lv:{
  play:"SPÄ’LÄ’T",again:"SPÄ’LÄ’T VÄ’LREIZ",menu:"GalvenÄ izvÄ“lne",board:"VÄ“rtÄ“jums",pass:"Pase",
  profile:"Profils",stats:"Statistika",casual:"Viegls",hardcore:"GrÅ«ts",rounds:"KÄrtas",
  btn_collect:"SavÄkt",btn_back:"AtpakaÄ¼ uz izvÄ“lni",btn_next:"TÄlÄk â†’",
  btn_again:"SpÄ“lÄ“t vÄ“lreiz",btn_menu:"GalvenÄ izvÄ“lne",btn_adapt:"PielÄgot",
  spotter_title:"\u{1F697} CeÄ¼ojuma Spotter",
  spotter_hint:"RedzÄ“ji numura zÄ«mi? ReÄ£istrÄ“ to tagad!",
  spotter_all:"Visas valstis",spotter_unknown:"NezinÄma numura zÄ«me",
  spotter_not_in:"nav",spotter_but_in:"bet ir",
  album_title:"\u{1F4D4} Numuru zÄ«mju albums",album_list:"\u{1F4DD} Saraksts",album_map:"\u{1F5FA} Karte",
  album_empty_country:"VÄ“l nekas no {country} â€” izmanto Spotter!",
  album_empty:"VÄ“l nekas savÄkts!\nSpÄ“lÄ“ ES numura zÄ«mes vai izmanto Spotter.",
  album_codes:"kodi",
  hl_higher:"â¬†ï¸ VairÄk / GarÄks / LielÄks",hl_lower:"â¬‡ï¸ MazÄk / ÄªsÄks / MazÄks",
  hl_more:"â¬†ï¸ VairÄk iedzÄ«votÄju",hl_less:"â¬‡ï¸ MazÄk iedzÄ«votÄju",
  loc_detected:"Atrodaties {country}",loc_adapt:"PielÄgot",
  q_city:"KurÄ valstÄ« atrodas Å¡Ä« pilsÄ“ta?",q_flag:"Kuras valsts Å¡is karogs?",
  q_capital:"Kurai valstij pieder Å¡Ä« galvaspilsÄ“ta?",q_river:"KurÄ valstÄ« tek Å¡Ä« upe?",
  q_landmark:"KurÄ valstÄ« atrodas Å¡is piemineklis?",q_park:"KurÄ valstÄ« atrodas Å¡is nacionÄlais parks?",
  q_unesco:"KurÄ valstÄ« atrodas Å¡is UNESCO mantojums?",q_citymark:"Kurai pilsÄ“tai pieder Å¡is piemineklis?",
  q_subway:"KurÄ pilsÄ“tÄ atrodas Å¡is metro?",q_flagsel:"KurÅ¡ karogs piederâ€¦",
  q_rcapital:"KÄda irâ€¦ galvaspilsÄ“ta?",q_rcity:"KurÄ pilsÄ“tÄ atrodasâ€¦?",
  q_rriver:"Kura upe tek caurâ€¦?",q_outline:"Kurai valstij ir Å¡Äda forma?",
  q_food:"No kuras valsts nÄk Å¡is Ä“diens?",q_brand:"No kuras valsts nÄk Å¡is zÄ«mols?",
  q_currency:"Kurai valstij pieder Å¡Ä« valÅ«ta?",q_curr_real:"KÄda valÅ«ta irâ€¦",
  q_pop_compare:"VairÄk vai mazÄk iedzÄ«votÄju?",
  q_hl_pop:"VairÄk iedzÄ«votÄju nekÄ {a}?",q_hl_river:"GarÄka nekÄ {a}?",q_hl_area:"LielÄka nekÄ {a}?",
  q_neighbor:"Kura valsts robeÅ¾ojas arâ€¦?",q_neighbor_not:"NAV robeÅ¾as arâ€¦?",
  q_plates_casual:"No kuras valsts ir Å¡Ä« numura zÄ«me?",q_plates_hard:"IdentificÄ“t reÄ£ionu â€” bez padoma!",
  q_river_real:"Caur kuru valsti tek Å¡Ä« upe?",q_map_guess:"Atrodi valsti kartÄ“",
  fb_correct:"âœ“ Pareizi! +{pts}",fb_wrong:"âœ— Nepareizi â†’ {ans}",fb_time:"â± Laiks beidzies! â†’ {ans}",
  plates_more:"+{n} vairÄk",pct_complete:"{pct}% pabeigts",
  spotter_dup:"ðŸ“‹ {code} ({country}) jau savÄkts!",
  map_unavail:"Karte nav pieejama",map_loading:"Karte ielÄdÄ“â€¦",
  q_subway_km:"Cik garÅ¡ ir metro tÄ«kls â€¦ (km)?",q_subway_lines:"Cik metro lÄ«niju ir â€¦?",
  diff_desc_casual:"\u{1F7E2} Casual: RelaksÄ“joÅ¡s Â· Nav laika ierobeÅ¾ojuma Â· âˆž DzÄ«ves",diff_desc_hc:"\u{1F525} Hardcore: KlasÄ«kais Â· Nav ierobeÅ¾ojuma Â· 3 DzÄ«ves",diff_desc_surv:"\u{1F480} Survival: Pret laiku Â· 8s Â· 3 DzÄ«ves",hud_lives:"DZÄªBVES",score_mult_max:"Maks ReizinÄtÄjs",score_time_bonus:"Laika Bonuss",pts_abbr:"pts.",score_correct_lbl:"pareizi",mode_wappen:"Ä¢erboÅ†i",mode_slf:"PilsÄ“ta-Valsts-Upe",mode_euro:"Eiro MonÄ“tas"
},
lt:{
  play:"Å½AISTI",again:"Å½AISTI IÅ  NAUJO",menu:"Pagrindinis meniu",board:"Reitingas",pass:"Pasas",
  profile:"Profilis",stats:"Statistika",casual:"Lengvas",hardcore:"Sunkus",rounds:"Raundai",
  btn_collect:"Rinkti",btn_back:"Atgal Ä¯ meniu",btn_next:"Kitas â†’",
  btn_again:"Å½aisti iÅ¡ naujo",btn_menu:"Pagrindinis meniu",btn_adapt:"Pritaikyti",
  spotter_title:"\u{1F697} KelionÄ—s Spotter",
  spotter_hint:"Matei numerÄ¯? UÅ¾raÅ¡yk dabar!",
  spotter_all:"Visos Å¡alys",spotter_unknown:"NeÅ¾inomas numeris",
  spotter_not_in:"nÄ—ra",spotter_but_in:"bet yra",
  album_title:"\u{1F4D4} NumeriÅ³ albumas",album_list:"\u{1F4DD} SÄ…raÅ¡as",album_map:"\u{1F5FA} Å½emÄ—lapis",
  album_empty_country:"Dar nieko iÅ¡ {country} â€” naudok Spotter!",
  album_empty:"Dar nieko surinkta!\nÅ½aisk ES numerius arba naudok Spotter.",
  album_codes:"kodai",
  hl_higher:"â¬†ï¸ Daugiau / Ilgesnis / Didesnis",hl_lower:"â¬‡ï¸ MaÅ¾iau / Trumpesnis / MaÅ¾esnis",
  hl_more:"â¬†ï¸ Daugiau gyventojÅ³",hl_less:"â¬‡ï¸ MaÅ¾iau gyventojÅ³",
  loc_detected:"Esate {country}",loc_adapt:"Pritaikyti",
  q_city:"Kurioje Å¡alyje yra Å¡is miestas?",q_flag:"Kurios Å¡alies Å¡i vÄ—liava?",
  q_capital:"Kuriai Å¡aliai priklauso Å¡i sostinÄ—?",q_river:"Kurioje Å¡alyje teka Å¡i upÄ—?",
  q_landmark:"Kurioje Å¡alyje yra Å¡is paminklas?",q_park:"Kurioje Å¡alyje yra Å¡is nacionalinis parkas?",
  q_unesco:"Kurioje Å¡alyje yra Å¡is UNESCO paveldas?",q_citymark:"Kuriam miestui priklauso Å¡is paminklas?",
  q_subway:"Kuriame mieste yra Å¡is metro?",q_flagsel:"Kuri vÄ—liava priklausoâ€¦",
  q_rcapital:"Kokia yraâ€¦ sostinÄ—?",q_rcity:"Koks miestas yraâ€¦?",
  q_rriver:"Kuri upÄ— teka perâ€¦?",q_outline:"Kuri Å¡alis turi Å¡iÄ… formÄ…?",
  q_food:"IÅ¡ kurios Å¡alies yra Å¡is patiekalas?",q_brand:"IÅ¡ kurios Å¡alies yra Å¡is prekÄ—s Å¾enklas?",
  q_currency:"Kuriai Å¡aliai priklauso Å¡i valiuta?",q_curr_real:"Kokia valiuta yraâ€¦",
  q_pop_compare:"Daugiau ar maÅ¾iau gyventojÅ³?",
  q_hl_pop:"Daugiau gyventojÅ³ nei {a}?",q_hl_river:"Ilgesnis nei {a}?",q_hl_area:"Didesnis nei {a}?",
  q_neighbor:"Kuri Å¡alis ribojasi suâ€¦?",q_neighbor_not:"NERIBOJASI suâ€¦?",
  q_plates_casual:"IÅ¡ kurios Å¡alies yra Å¡is numeris?",q_plates_hard:"Nustatyti regionÄ… â€” be uÅ¾uominos!",
  q_river_real:"Per kuriÄ… Å¡alÄ¯ teka Å¡i upÄ—?",q_map_guess:"Rask Å¡alÄ¯ Å¾emÄ—lapyje",
  fb_correct:"âœ“ Teisingai! +{pts}",fb_wrong:"âœ— Neteisingai â†’ {ans}",fb_time:"â± Laikas! â†’ {ans}",
  plates_more:"+{n} daugiau",pct_complete:"{pct}% baigta",
  spotter_dup:"ðŸ“‹ {code} ({country}) jau surinkta!",
  map_unavail:"Å½emÄ—lapis neprieinamas",map_loading:"Kraunamas Å¾emÄ—lapisâ€¦",
  q_subway_km:"Kiek ilgas metro tinklas â€¦ (km)?",q_subway_lines:"Kiek metro linijÅ³ yra â€¦?",
  diff_desc_casual:"\u{1F7E2} Casual: AtsipalaidavÄ™s Â· Be laiko limito Â· âˆž GyvybiÅ³",diff_desc_hc:"\u{1F525} Hardcore: Klasikinis Â· Be limito Â· 3 GyvybÄ—s",diff_desc_surv:"\u{1F480} Survival: PrieÅ¡ laikÄ… Â· 8s Â· 3 GyvybÄ—s",hud_lives:"GYVYBÄ–S",score_mult_max:"Maks Daugintojas",score_time_bonus:"Laiko Premija",pts_abbr:"tÅ¡k.",score_correct_lbl:"teisingai",mode_wappen:"Herbai",mode_slf:"Miestas-Å alis-UpÄ—",mode_euro:"Euro Monetos"
},
mt:{
  play:"ILGÄ¦AB",again:"ILGÄ¦AB MILL-Ä DID",menu:"Menu PrinÄ‹ipali",board:"Klassifika",pass:"Passaport",
  profile:"Profil",stats:"StatistiÄ‹i",casual:"Casual",hardcore:"Hardcore",rounds:"Rawnd",
  btn_collect:"IÄ¡bor",btn_back:"Lura gÄ§all-menu",btn_next:"Li Jmiss â†’",
  btn_again:"IlgÄ§ab mill-Ä¡did",btn_menu:"Menu PrinÄ‹ipali",btn_adapt:"Adatta",
  spotter_title:"\u{1F697} Spotter tal-VjaÄ¡Ä¡",
  spotter_hint:"Rajt pjanÄ‹a? IrreÄ¡istraha issa!",
  spotter_all:"PajjiÅ¼i kollha",spotter_unknown:"PjanÄ‹a mhux magÄ§rufa",
  spotter_not_in:"mhux fi",spotter_but_in:"imma fi",
  album_title:"\u{1F4D4} Kollezzjoni tal-PjanÄ‹i",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Mappa",
  album_empty_country:"Xejn minn {country} s'issa â€” uÅ¼a s-Spotter!",
  album_empty:"Xejn miÄ¡bur s'issa!\nIlgÄ§ab il-pjanÄ‹i tal-UE jew uÅ¼a s-Spotter.",
  album_codes:"kodiÄ‹i",
  hl_higher:"â¬†ï¸ Aktar / Itwal / Akbar",hl_lower:"â¬‡ï¸ Inqas / Iqsar / IÅ¼gÄ§ar",
  hl_more:"â¬†ï¸ Aktar abitanti",hl_less:"â¬‡ï¸ Inqas abitanti",
  loc_detected:"QiegÄ§ed fi {country}",loc_adapt:"Adatta",
  q_city:"F'liema pajjiÅ¼ tinsab din il-belt?",q_flag:"Liema pajjiÅ¼ gÄ§andu din il-bandiera?",
  q_capital:"Lil liema pajjiÅ¼ tappartjeni din il-kapitali?",q_river:"F'liema pajjiÅ¼ jgÄ§addi dan ix-xmara?",
  q_landmark:"F'liema pajjiÅ¼ tinsab din il-wieqfa?",q_park:"F'liema pajjiÅ¼ jinsab dan il-park nazzjonali?",
  q_unesco:"F'liema pajjiÅ¼ jinsab dan is-sit UNESCO?",q_citymark:"Lil liema belt tappartjeni din il-wieqfa?",
  q_subway:"F'liema belt jinsab dan il-metro?",q_flagsel:"Liema bandiera tappartjeni lilâ€¦",
  q_rcapital:"X'inhi l-kapitali ta'â€¦?",q_rcity:"Liema belt tinsab fiâ€¦?",
  q_rriver:"Liema xmara tgÄ§addi minnâ€¦?",q_outline:"Liema pajjiÅ¼ gÄ§andu din il-forma?",
  q_food:"Minn liema pajjiÅ¼ Ä¡ej dan l-ikel?",q_brand:"Minn liema pajjiÅ¼ Ä¡ej dan il-brand?",
  q_currency:"Lil liema pajjiÅ¼ tappartjeni din il-munita?",q_curr_real:"X'munita gÄ§anduâ€¦",
  q_pop_compare:"Aktar jew inqas abitanti?",
  q_hl_pop:"Aktar abitanti minn {a}?",q_hl_river:"Itwal minn {a}?",q_hl_area:"Akbar minn {a}?",
  q_neighbor:"Liema pajjiÅ¼ jibbordjja ma'â€¦?",q_neighbor_not:"MA jibbordjjax ma'â€¦?",
  q_plates_casual:"Minn liema pajjiÅ¼ hija din il-pjanÄ‹a?",q_plates_hard:"Identifika r-reÄ¡jun â€” l-ebda indikazzjoni!",
  q_river_real:"Minn liema pajjiÅ¼ jgÄ§addi dan ix-xmara?",q_map_guess:"Sib il-pajjiÅ¼ fuq il-mappa",
  fb_correct:"âœ“ Korretti! +{pts}",fb_wrong:"âœ— Ä¦aÅ¼in â†’ {ans}",fb_time:"â± Ä¦in! â†’ {ans}",
  plates_more:"+{n} aktar",pct_complete:"{pct}% lest",
  spotter_dup:"ðŸ“‹ {code} ({country}) diÄ¡Ã  miÄ¡bur!",
  map_unavail:"Mappa mhux disponibbli",map_loading:"Qed jÄ¡Ä§abbi l-mappaâ€¦",
  q_subway_km:"Kemm hi twila n-netwerk tal-metro â€¦ (km)?",q_subway_lines:"Kemm gÄ§andha linji tal-metro â€¦?",
  diff_desc_casual:"\u{1F7E2} Casual: Rilassat Â· Ebda limitu ta' Ä§in Â· âˆž Ä¦ajjiet",diff_desc_hc:"\u{1F525} Hardcore: Klassiku Â· Ebda limitu Â· 3 Ä¦ajjiet",diff_desc_surv:"\u{1F480} Survival: Kontra l-Ä§in Â· 8s Â· 3 Ä¦ajjiet",hud_lives:"Ä¦AJJIET",score_mult_max:"Multiplikatur Massimu",score_time_bonus:"Bonus tal-Ä¦in",pts_abbr:"pt.",score_correct_lbl:"korretti",mode_wappen:"Armi",mode_slf:"Belt-PajÄ§iÅ¼-Xmara",mode_euro:"Muniti Ewro"
},
ga:{
  play:"IMIR",again:"IMIR ARÃS",menu:"PrÃ­omh-roghchlÃ¡r",board:"ClÃ¡r na mBuaiteoirÃ­",pass:"Pas",
  profile:"PrÃ³ifÃ­l",stats:"StaitisticÃ­",casual:"Ã‰asca",hardcore:"Deacair",rounds:"BabhtaÃ­",
  btn_collect:"Bailigh",btn_back:"Ar ais go dtÃ­ an roghchlÃ¡r",btn_next:"Ar Aghaidh â†’",
  btn_again:"Imir arÃ­s",btn_menu:"PrÃ­omh-roghchlÃ¡r",btn_adapt:"OiriÃºnaigh",
  spotter_title:"\u{1F697} Spotter Taistil",
  spotter_hint:"Chonaic tÃº plÃ¡ta? Taifeadaigh anois Ã©!",
  spotter_all:"Gach tÃ­r",spotter_unknown:"PlÃ¡ta anaithnid",
  spotter_not_in:"nÃ­l i",spotter_but_in:"ach tÃ¡ i",
  album_title:"\u{1F4D4} Cnuasach PlÃ¡ta",album_list:"\u{1F4DD} Liosta",album_map:"\u{1F5FA} LÃ©arscÃ¡il",
  album_empty_country:"FÃ³s aon rud Ã³ {country} â€” ÃºsÃ¡id an Spotter!",
  album_empty:"FÃ³s aon rud bailithe!\nImir plÃ¡ta AE nÃ³ ÃºsÃ¡id an Spotter.",
  album_codes:"cÃ³id",
  hl_higher:"â¬†ï¸ NÃ­os mÃ³ / NÃ­os faide / NÃ­os mÃ³",hl_lower:"â¬‡ï¸ NÃ­os lÃº / NÃ­os giorra / NÃ­os lÃº",
  hl_more:"â¬†ï¸ NÃ­os mÃ³ cÃ³naitheoirÃ­",hl_less:"â¬‡ï¸ NÃ­os lÃº cÃ³naitheoirÃ­",
  loc_detected:"TÃ¡ tÃº i {country}",loc_adapt:"OiriÃºnaigh",
  q_city:"CÃ©n tÃ­r ina bhfuil an chathair seo?",q_flag:"CÃ©n tÃ­r a bhfuil an bhratach seo aige?",
  q_capital:"CÃ©n tÃ­r ar leis an phrÃ­omhchathair seo?",q_river:"CÃ©n tÃ­r ina ritheann an abhainn seo?",
  q_landmark:"CÃ©n tÃ­r ina bhfuil an sÃ©adchomhartha seo?",q_park:"CÃ©n tÃ­r ina bhfuil an pÃ¡irc nÃ¡isiÃºnta seo?",
  q_unesco:"CÃ©n tÃ­r ina bhfuil an suÃ­omh UNESCO seo?",q_citymark:"CÃ©n chathair ar leis an sÃ©adchomhartha seo?",
  q_subway:"CÃ©n chathair ina bhfuil an meitreal seo?",q_flagsel:"CÃ©n bhratach a bhaineann leâ€¦",
  q_rcapital:"Cad is prÃ­omhchathair deâ€¦?",q_rcity:"CÃ©n chathair atÃ¡ iâ€¦?",
  q_rriver:"CÃ©n abhainn a ritheann trÃ­â€¦?",q_outline:"CÃ©n tÃ­r a bhfuil an cruth seo aige?",
  q_food:"CÃ©n tÃ­r as ar thÃ¡inig an mias seo?",q_brand:"CÃ©n tÃ­r as ar thÃ¡inig an branda seo?",
  q_currency:"CÃ©n tÃ­r ar leis an airgeadra seo?",q_curr_real:"CÃ©n airgeadra atÃ¡ agâ€¦",
  q_pop_compare:"NÃ­os mÃ³ nÃ³ nÃ­os lÃº cÃ³naitheoirÃ­?",
  q_hl_pop:"NÃ­os mÃ³ cÃ³naitheoirÃ­ nÃ¡ {a}?",q_hl_river:"NÃ­os faide nÃ¡ {a}?",q_hl_area:"NÃ­os mÃ³ nÃ¡ {a}?",
  q_neighbor:"CÃ©n tÃ­r a bhfuil teorainn leâ€¦?",q_neighbor_not:"NÃL teorainn leâ€¦?",
  q_plates_casual:"CÃ©n tÃ­r ar as an plÃ¡ta seo?",q_plates_hard:"Aithin an rÃ©igiÃºn â€” gan leid!",
  q_river_real:"TrÃ­ cÃ©n tÃ­r a ritheann an abhainn seo?",q_map_guess:"Aimsigh an tÃ­r ar an lÃ©arscÃ¡il",
  fb_correct:"âœ“ Ceart! +{pts}",fb_wrong:"âœ— MÃ­cheart â†’ {ans}",fb_time:"â± Am! â†’ {ans}",
  plates_more:"+{n} nÃ­os mÃ³",pct_complete:"{pct}% crÃ­ochnaithe",
  spotter_dup:"ðŸ“‹ {code} ({country}) bailithe cheana!",
  map_unavail:"LÃ©arscÃ¡il nach bhfuil ar fÃ¡il",map_loading:"Ag lÃ³dÃ¡il lÃ©arscÃ¡ilâ€¦",
  q_subway_km:"CÃ© chomh fada leis an ngrÃ©asÃ¡n meitreÃ³ â€¦ (km)?",q_subway_lines:"CÃ© mhÃ©ad lÃ­ne meitreÃ³ atÃ¡ ag â€¦?",
  diff_desc_casual:"\u{1F7E2} Casual: Socair Â· Gan teorainn ama Â· âˆž Saol",diff_desc_hc:"\u{1F525} Hardcore: ClÃ¡sach Â· Gan teorainn Â· 3 Saol",diff_desc_surv:"\u{1F480} Survival: In aghaidh an chloig Â· 8s Â· 3 Saol",hud_lives:"SAOLTA",score_mult_max:"Iolraitheoir UasmÃ©id",score_time_bonus:"BÃ³nas Ama",pts_abbr:"p.",score_correct_lbl:"ceart",mode_wappen:"Armas",mode_slf:"Cathair-TÃ­r-Abhainn",mode_euro:"Boinn Euro"
}
};
/* t(key, vars) â€” translate + interpolate */
function t(key,vars){
  const lang=(typeof S!=='undefined'&&S.language)||localStorage.getItem('gq_lang')||'de';
  let s=(LANG[lang]&&LANG[lang][key])||(LANG.en&&LANG.en[key])||(LANG.de&&LANG.de[key])||key;
  if(!s)return key;  /* never return undefined */
  if(vars)Object.keys(vars).forEach(k=>{const rv=vars[k]??"-";s=s.replace(new RegExp('\\{'+k+'\\}','g'),String(rv));});
  return s;
}
/* Backwards-compat alias */
function T(k){return t(k);}
/* setLanguage â€” persists choice, marks as manual override */
function setLanguage(lang){
  if(typeof S!=='undefined')S.language=lang;
  localStorage.setItem('gq_lang',lang);
  localStorage.setItem('geoquest_lang_manual','1');
  render();
}
/* getCountryName(cc, lang) â€” Intl.DisplayNames for all 25 locales */
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
/* displayCountry(name) â€” translate country display name for current language */
function displayCountry(name){
  if(!name||typeof name!=="string")return name||"";
  const lang=(typeof S!=='undefined'&&S.language)||localStorage.getItem('gq_lang')||'de';
  const co=COUNTRIES.find(c=>c.c===name);
  if(!co)return name;
  return getCountryName(co.cc,lang);
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

const globalCities = ['Aachen', 'Aarhus', 'Abilene', 'Accra', 'Adamstown', 'Adelaide', 'Aden', 'Ã…land', 'Ã…lesund', 'Algiers', 'Alicante', 'Amsterdam', 'Anchorage', 'Andorra la Vella', 'Ankara', 'Antalya', 'Antofagasta', 'Antwerp', 'Apia', 'Aracaju', 'Arad', 'AraÃ§atuba', 'Arequipa', 'Arica', 'Arkhangelsk', 'Arlington', 'Arnhem', 'Arta', 'Arupukottai', 'Asgabat', 'Ashdod', 'Ashford', 'Asmara', 'Aspen', 'Astana', 'Astrakhan', 'Asturias', 'Aswan', 'Asyut', 'Atacama', 'Athens', 'Atlanta', 'Atlantic City', 'Atlas Mountains', 'Atsugi', 'Auckland', 'Augsburg', 'Augusta', 'Aulnay-sous-Bois', 'Auroville', 'Austin', 'Australind', 'Autun', 'Auxerre', 'Avallon', 'Aveiro', 'Avellino', 'Avenches', 'Avesnes', 'Avignon', 'Avila', 'Avilon', 'Avitus', 'Avoch', 'Avola', 'Avore', 'Avoriaz', 'Avosnes', 'Avranches', 'Avricourt', 'Avrigney', 'Avrilly', 'Avron', 'Avropolis', 'Avroy', 'Avry-Devant-Pont', 'Avvenevoli', 'Avvenne', 'Avy', 'Avye', 'Avyeston', 'Awal', 'Aware', 'Awaroa', 'Awakuni', 'Awangaroa', 'Awar', 'Awara', 'Awardak', 'Awareton', 'Awari', 'Awar-ka', 'Awarma', 'Awarna', 'Aware-po', 'Awart', 'Awarto', 'Awas', 'Awasa', 'Awasacho', 'Awase', 'Awatawara', 'Awatagaki', 'Awatara', 'Awatare', 'Awataroa', 'Awataru', 'Awatasa', 'Awatauta', 'Awata-Zaka', 'Awate', 'Awatecho', 'Awate-no-Sho', 'Awatere', 'Awatesa', 'Awateshio', 'Awatesia', 'Awateso', 'Awatesta', 'Awatete', 'Awateu', 'Awateuchi', 'Awatewa', 'Awatewara', 'Awatewari', 'Awatex', 'Awateza', 'Awatezo', 'Awatezuka', 'Awatica', 'Awatida', 'Awatide', 'Awatidori', 'Awatiebori', 'Awatief', 'Awatiego', 'Awatieji', 'Awatigami', 'Awatiga-no-koshi', 'Awatigariba', 'Awatiga-ura', 'Awatighembo', 'Awatigi', 'Awatiji', 'Awatije', 'Awatigishi', 'Awatigu', 'Awatih', 'Awatiha', 'Awatihata', 'Awatihave', 'Awatihide', 'Awatihiji', 'Awatihira', 'Awatihise', 'Awatihisi', 'Awatihocu', 'Awatihoji', 'Awatihokai', 'Awatihoku', 'Awatihotaka', 'Awatihun', 'Awatii', 'Awatiichiga', 'Awatiichiyo', 'Awatiijiyo', 'Awatiikami', 'Awatiikitaya', 'Awatiiko', 'Awatiikoku', 'Awatiikoku-mura', 'Awatiikonya', 'Awatiikosa', 'Awatiikotatsuya', 'Awatiikoyo', 'Awatii-kuchiya', 'Awatiikumagaya', 'Awatiikunabasi', 'Awatiikunada', 'Awatii-kunadere', 'Awatiikunagaya', 'Awatiikuna-Gata', 'Awatii-kunagataya', 'Awatii-kunahata', 'Awatiikuna-hoiji', 'Awatiikunaka', 'Awatiikunakamata', 'Awatiikuna-kamata', 'Awatiikuna-kamiyama', 'Awatiikunamiyama', 'Awatiikuna-shidai', 'Awatiikunasi', 'Awatiikuno', 'Awatiikuo', 'Awatiikoura', 'Awatiikura', 'Awatiikurano', 'Awatiiis', 'Awalijir', 'Awalibah', 'Awalibih', 'Awalib-i-Kul', 'Awalijir', 'Awalijah', 'Baghdad', 'Bangkok', 'Barcelona', 'Beijing', 'Beirut', 'Belfast', 'Belgrade', 'Berlin', 'Bern', 'Bilbao', 'Birmingham', 'Blankenburg', 'Bogota', 'Bologna', 'Bombay', 'Bonn', 'Bordeaux', 'Boston', 'Boulogne', 'Bradford', 'Braga', 'BrÄƒila', 'Braintree', 'Brampton', 'Brandenburg', 'BrasÃ­lia', 'Braunschweig', 'Bremen', 'Bremerhaven', 'Brescia', 'Breslau', 'Brest', 'Brianza', 'Bridgetown', 'Brighton', 'Brindisi', 'Brisbane', 'Bristol', 'Brixen', 'Brno', 'Bron', 'Bronx', 'Brooklyn', 'Brugge', 'Bruges', 'Brugherio', 'Brummana', 'Brunei', 'Brunette', 'Brunswick', 'Brussels', 'BrÄko', 'BrÄko', 'Bucharest', 'Budapest', 'Buenos Aires', 'Buffalo', 'Bugulma', 'Bukhara', 'Bukoba', 'Bulawayo', 'BÃ¼lach', 'Burgenland', 'Burgos', 'Burgund', 'Burgundy', 'Burhaniye', 'Burias', 'Burk', 'Burlingame', 'Burlington', 'Burmarrad', 'Burney', 'Burpengary', 'Burr', 'Bursa', 'Burton', 'Bushe', 'Bushehr', 'Bushmills', 'Bushrod', 'Bushy', 'Busingen', 'BÃ¼singen', 'Busnes', 'Busque', 'Bussac-sur-Charente', 'Bussang', 'Busschoten', 'BussÃ©', 'Busselton', 'Bussies', 'Bussy-Saint-Georges', 'Busta', 'Bustier', 'Bustle', 'Bustomi', 'Bustus', 'Busy', 'Busybody', 'Butyra', 'Buyala', 'Buyanka', 'Buyanunga', 'Buyatsi', 'Buye', 'Buyer', 'Buyerside', 'Buyfritz', 'Buykichi', 'Buyokuocho', 'Buyomi', 'Buyomichi', 'Buyomi-Fushicho', 'Buyomi-Fushiya', 'Buyomi-Fushiyama', 'Buyomicho', 'Buyomi-Shukugawara', 'Buyomicho-Kawauchi', 'Buyomicho-Shukugawa', 'Buyomicho-Yodo', 'Buyomicho-Shimoshibugahara', 'Buyomicho-Shimohamacho', 'Buyomicho-Shimonakagawara', 'Buyomicho-Yodogawa', 'Buyomidai', 'Buyomidori', 'Buyomiji', 'Buyomiji-Naguno', 'Buyomiji-Yodo', 'Buyomijicho', 'Buyomikita', 'Buyomikitadori', 'BuyomikitachÅ', 'BuyomikÅ', 'Buyomisaku', 'Buyomizaka', 'BuyomizakachÅ', 'Buyomizakashita', 'Buyomizakitsu', 'Buyomizakunosuke', 'Buyomizakumisawa', 'Buyomizakushichidaiji', 'Buyomizan', 'Buyomizanzaka', 'Buyomizashita', 'Buyomizocho', 'Buyomizori', 'Buyra', 'Buyrum', 'Buyrulyuk', 'Buyryuka', 'Buys', 'Buysbag', 'Buysberg', 'Buyscop', 'Buyse', 'Buyserd', 'Buysenaar', 'Buyseriez', 'Buysin', 'Buyskamp', 'Buyskova', 'Buysloot', 'Buysman', 'Buysmans', 'Buysmeester', 'Buysmeleerders', 'Buysmelters', 'Buysmith', 'Buysnerf', 'Buysner', 'Buysnick', 'Buysohann', 'Buysoort', 'Buyspath', 'Buyspath', 'Buyspiel', 'Buysques', 'Buysquets', 'Buysradour', 'Buysraul', 'Buysreef', 'Buysregning', 'Buysrehn', 'Buysreich', 'Buysreka', 'Buysrell', 'Buyeren', 'Buyeres', 'Buyergol', 'Buyeric', 'Buyeries', 'Buyerinckhaus', 'Buyering', 'Buyerini', 'Buyerinkhuis', 'Buyerinkhuizen', 'Buyerinkij', 'Buyerinkske', 'Buyerinkstra', 'Buyerink-Tandjung', 'Buyerink-Tanjong', 'Buyerinne', 'Buyerinnent', 'Buyerinnental', 'Buyerins', 'Buyerins-aux-Tours', 'Cairo', 'Calcutta', 'Calgary', 'Cali', 'Calicut', 'Callao', 'Caltanissetta', 'Cambridge', 'Camdenton', 'Camden', 'Camerino', 'Campbelltown', 'Campechuela', 'Campinas', 'Campione', 'Campolide', 'Camponotis', 'Campos', 'Campuchia', 'Canaries', 'Canary Islands', 'Canby', 'Cancale', 'Cancalon', 'Cancas', 'Cancentra', 'Canchellor', 'Cancianita', 'Canciello', 'Cancina', 'Cancini', 'Cancino', 'Canciones', 'Cancipani', 'Cancipelle', 'Cancisi', 'Cancisse', 'Cancistes', 'Cancita', 'Cancizales', 'Cancizane', 'Cancizano', 'Canckelmach', 'Canclano', 'Canclas', 'Canclasa', 'Canclaw', 'Cancles', 'Canclew', 'Cancleys', 'Cancleza', 'Cancoce', 'Cancochou', 'Cancoine', 'Cancola', 'Cancombe', 'Cancelace', 'Cancelacio', 'Cancelacion', 'CancelaÃ§ao', 'CancelaciÃ³n', 'Cancelada', 'Canceladas', 'Cancelado', 'Cancelados', 'Cancelador', 'Canceladora', 'Canceladoras', 'Canceladores', 'Canceladura', 'Canceladurs', 'Canceladurse', 'Canceladurso', 'Cancelae', 'CancelaciÃ³n', 'Cancelaera', 'Cancelafia', 'Cancelago', 'Cancelai', 'Cancelaia', 'Cancelaida', 'Cancelaile', 'Cancelailles', 'Cancelain', 'Cancelained', 'Cancelaina', 'Cancelaines', 'Cancelair', 'Cancelaise', 'Cancelaiset', 'Cancelaisia', 'Cancelait', 'Cancelaja', 'Cancelaje', 'Cancelajo', 'Cancelala', 'Cancelala', 'Cancelalaleria', 'Cancelalachot', 'Cancelachos', 'CancelaciÃ³n', 'Cancelacione', 'Cancelaciones', 'Cancelalada', 'Cancelado', 'Canceladora', 'Canceladorao', 'Canceladorash', 'Canceladoras', 'Canceladorash', 'Canceladores', 'Canceladoresh', 'Canceladorez', 'CanceladorÃ­a', 'CanceladorÃ­as', 'Canceladura', 'Canceladuras', 'Canceladureia', 'Canceladureza', 'CanceladurÃ­a', 'CanceladurÃ­a', 'CanceladurÃ­as', 'Canceladuza', 'Cancelaeas', 'Cancelaebo', 'Cancelaela', 'Cancelaeles', 'Cancelaelo', 'Cancelaena', 'Cancelaene', 'Cancelaeno', 'Cancelaenor', 'Cancelaenque', 'Cancelaep', 'Cancelaera', 'Cancelaeracio', 'CancelaeraciÃ³n', 'Cancelaeraciones', 'Cancelaerade', 'Cancelaerador', 'Cancelaeradora', 'Cancelaeradoras', 'Cancelaeradores', 'Cancelaeradura', 'Cancelaeradura', 'Cancelaeradura', 'Cancelaeradura', 'Cancelaerador', 'Cancelaeradura', 'Cancelaeradura', 'Cancelaeradura', 'Cancelaeradura', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaerador', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora', 'Cancelaeradora'];


const globalRivers = ['Amazonas', 'Amur', 'Anadir', 'Amundsen Gulf', 'Angara', 'Anadyr', 'Ankara', 'Anuy', 'Apalachicola', 'Apure', 'AraranguÃ¡', 'Arauca', 'Arawak', 'Archimedes', 'ArdÃ¨che', 'Arequipa', 'Areuse', 'Argandabrujas', 'ArgaÃ±Ã³n', 'Arganya', 'Argar', 'Argaricus', 'Argari', 'Argarilo', 'Argamasa', 'Argamasso', 'Argan', 'ArganedÃ³n', 'Argania', 'Arganot', 'ArganyÃ³s', 'ArgaÃ±Ã³s', 'ArgaÃ±uela', 'Arganza', 'ArgapajÃ³n', 'Argapalomos', 'Argapalos', 'Argapas', 'Argapaz', 'Argarago', 'Argaragon', 'Argarana', 'ArgÃ¡ramo', 'ArgaramÃ³n', 'Argaramone', 'Argapapa', 'Argarapalos', 'Argarapaz', 'Argarapazos', 'Argarapazuelos', 'Argarapazuela', 'Argarapazuelas', 'ArgÃ¡pedo', 'ArgÃ¡pela', 'ArgÃ¡peles', 'ArgÃ¡pelo', 'ArgÃ¡pena', 'ArgÃ¡penas', 'ArgÃ¡pena', 'ArgÃ¡penes', 'ArgÃ¡peno', 'ArgÃ¡peÃ±o', 'ArgÃ¡peÃ±os', 'ArgÃ¡pere', 'ArgÃ¡peres', 'ArgÃ¡peria', 'ArgÃ¡perilla', 'ArgÃ¡perio', 'ArgÃ¡pero', 'ArgÃ¡perola', 'ArgÃ¡perone', 'ArgÃ¡perones', 'ArgÃ¡peronÃ­a', 'ArgÃ¡perosa', 'ArgÃ¡peroso', 'ArgÃ¡perota', 'ArgÃ¡perote', 'ArgÃ¡perotes', 'ArgÃ¡peruana', 'ArgÃ¡peruanas', 'ArgÃ¡peruania', 'ArgÃ¡peruanÃ­a', 'ArgÃ¡peruano', 'ArgÃ¡peruanos', 'ArgÃ¡peruanÃ­a', 'ArgÃ¡peruanina', 'ArgÃ¡peruanina', 'ArgÃ¡peruanina', 'ArgÃ¡peruanina', 'ArgÃ¡peruanina', 'ArgÃ¡peruanina', 'ArgÃ¡peruanina', 'ArgÃ¡peruanina', 'ArgÃ¡peruanina', 'ArgÃ¡peruanina', 'ArgÃ¡peruanina', 'ArgÃ¡peruanina', 'ArgÃ¡peruanina', 'ArgÃ¡peruanina', 'ArgÃ¡peruanina', 'ArgÃ¡peruanina', 'ArganÃ¡x', 'Argandabrujas', 'Argandel', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandenacho', 'Argandenacho', 'Argandenacho', 'Argandenacho', 'Argandenachuela', 'Argandenachuela', 'Argandenachuela', 'Argandenachuela', 'Argandenacho', 'Argandenacho', 'Argandenacho', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Argandena', 'Baganza', 'Baghlan', 'Baghmashy', 'Bahamas', 'Bahia', 'Bahram', 'Bahr El', 'Bahrein', 'BahrÄ«yÄt', 'Baia', 'Baicalus', 'Baident', 'BailÃ©n', 'BailÃ©ndola', 'Bailenta', 'BailentÃ­n', 'Bailentola', 'Baileo', 'BaileÃ³grafo', 'Baileoide', 'Baileote', 'BaileonÃ­a', 'BaileÃ³nico', 'Baileonida', 'Baileonide', 'Baileonides', 'Baileonidio', 'Baileonino', 'Baileonita', 'Baileonito', 'BaileoÃ±o', 'BaileoÃ±a', 'BaileoÃ±ada', 'BaileoÃ±adÃ­a', 'BaileoÃ±al', 'BaileoÃ±alidad', 'BaileoÃ±alismo', 'BaileoÃ±alista', 'BaileoÃ±alizador', 'BaileoÃ±alizaciÃ³n', 'BaileoÃ±alizar', 'BaileoÃ±almente', 'BaileoÃ±ancia', 'BaileoÃ±andÃ­a', 'BaileoÃ±andÃ­o', 'BaileoÃ±andizal', 'BaileoÃ±andizo', 'BaileoÃ±andÃ­a', 'BaileoÃ±andÃ­o', 'BaileoÃ±andizal', 'BaileoÃ±andizo', 'BaileoÃ±andizaciÃ³n', 'BaileoÃ±andizador', 'BaileoÃ±andizar', 'BaileoÃ±ante', 'BaileoÃ±ancia', 'BaileoÃ±andor', 'BaileoÃ±andora', 'BaileoÃ±anderÃ­a', 'BaileoÃ±andÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±andera', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'BaileoÃ±anderÃ­a', 'Caladay', 'Calabarza', 'Calabaca', 'Calabacera', 'CalabacerÃ­a', 'Calabacerina', 'CalabacerÃ­o', 'Calabacerina', 'CalabacerÃ­o', 'CalabacerÃ­o', 'CalabacerÃ­o', 'CalabacerÃ­a', 'CalabacerÃ­a', 'CalabacerÃ­a', 'CalabacerÃ­a', 'Calabaceril', 'Calabacerilla', 'Calabacerilla', 'Calabacerilla', 'Calabacerilla', 'Calabacerilla', 'Calabacerilla', 'Calabacerilla', 'Calabacerilla', 'Calabacerilla', 'Calabacerilla', 'Danube', 'Daugava', 'Delaware', 'Delft', 'Delta', 'Demavend', 'Demetrio', 'Denbigh', 'Dendermond', 'Denfert', 'Dengie', 'Denia', 'Deniliquin', 'Denkmal', 'Denmark', 'Denman', 'Dennett', 'Denning', 'Denningite', 'Dennis', 'Dennison', 'Dennisonipora', 'Dennisoniporidae', 'Dennisoniporida', 'Dennisoniporid', 'Dennisoniporida', 'Dennisoniporidae', 'Dennisoniporid', 'Dennisoniporidae', 'Dennisoniporida', 'Dennisoniporidae', 'Dennisoniporid', 'Dennisoniporidae', 'Elbe', 'Eldorado', 'Elevated Railway', 'Eleusis', 'Elevon', 'Elgin', 'Eli', 'Eliberis', 'Elice', 'Elidwen', 'Eligius', 'Elijah', 'Elikhof', 'Eliledontas', 'Elimbergetis', 'Elimbergetium', 'Eliminator', 'Elinborg', 'Elinea', 'Elinea', 'Elineae', 'Elineales', 'Elinealesales', 'Elinealesales', 'Elinealesales', 'Elinealesales', 'Elinealesales', 'Elinealesales', 'Elinealesales', 'Flahault', 'Flakstad', 'Flamand', 'Flambeaux', 'Flambeau', 'Flambeaux', 'Flambeau', 'Flambeaux', 'Flambeau', 'Flambeaux', 'Flambeau', 'Flambeaux', 'Flambeaux', 'Flambeau', 'Flambeaux', 'Flambeau', 'Flambeaux', 'Flambeau', 'Gagnoa', 'Gaibandha', 'Gaidai', 'Gaidani', 'Gaidania', 'Gaidanias', 'Gaidanidai', 'Gaidanidia', 'Gaidanidiae', 'Gaidanidian', 'Gaidanidians', 'Gaidanididae', 'Gaidanidian', 'Gaidanidians', 'Gaidanidida', 'Gaidanididae', 'Gaidanidian', 'Hallelujah', 'Hallelu', 'Hallelujahs', 'Hallelujah', 'Hallelujahed', 'Hallelujahing', 'Hallelujahs', 'Hallelujahed', 'Hallelujahing', 'Hallelujahs', 'Hallelu', 'Hallelujahs', 'Hallelujah', 'Hallelujahs', 'Hallelujah', 'Hallelujahs', 'Ialisos', 'Iambes', 'Iambic', 'Iambics', 'Iambidae', 'Iambid', 'Iambidae', 'Iambidae', 'Iambidae', 'Iambidae', 'Iambidae', 'Iambidae', 'Iambidae', 'Jabaquara', 'Jaguara', 'Jaguari', 'JaguarÃ©', 'Jaguarete', 'Jaguari', 'Jaguaribara', 'Jaguaribara', 'Jaguaribaras', 'Jaguaribara', 'Jaguaribaras', 'Jaguari', 'Kabardin', 'Kabardino', 'Kabardino-Balkar', 'Kabardino-Balkarian', 'Kabardino-Balkarians', 'Kabard', 'Kabardinsk', 'Kabardinslye', 'Kabardinskoe', 'Kabardovsk', 'Kabaret', 'Kabaretka', 'Kabaretki', 'Kabaretnika', 'Kabaretnikov', 'Kabaretniki', 'Kabaretnik', 'Labrador', 'Lac', 'Lacador', 'Lacalc', 'Lacan', 'LacandÃ³n', 'Lacandon', 'Lacandona', 'Lacandone', 'Lacandones', 'Lacandonia', 'Lacandonian', 'Lacandonians', 'Macedo', 'Macedonia', 'Macedonian', 'Macedonians', 'Macedonise', 'Macedonize', 'Macedonized', 'Macedonizer', 'Macedonizers', 'Macedonizes', 'Macedonizing', 'MaceiÃ³', 'Macedonian', 'Macedonians', 'Macedonise', 'Macedonized', 'Macedonizer', 'Nil', 'Nilgai', 'Nilgai', 'Nilgais', 'Nile', 'Nilers', 'Nilescient', 'Nilesco', 'Nileshwar', 'Niliads', 'Niliadic', 'Niliads', 'Niliads', 'Niliads', 'Niliads', 'Odense', 'Odo', 'Odoacer', 'Odoacre', 'Odoaber', 'Odoacris', 'Odoaks', 'Odoaks', 'Odoalk', 'Odoacre', 'Odoacris', 'Odoacre', 'Odoacris', 'Odoacre', 'ParanÃ¡', 'ParanÃ¡ do Sul', 'ParanÃ ', 'ParanaguÃ¡', 'Paranaguaze', 'Paranahiba', 'Paranajuba', 'Paranapanema', 'Paranapanema', 'ParanÃ¡pe', 'ParanÃ¡', 'Paranaense', 'ParanÃ¡juba', 'ParanÃ¡juba', 'ParanÃ¡ Mirim', 'ParanÃ¡juba', 'ParanÃ¡juba', 'Quincy', 'QuindÃ­o', 'Quinta', 'Quintanal', 'Quintanales', 'Quintanales', 'Quintanales', 'Quintanales', 'Quintanales', 'Quintanales', 'Quintanales', 'Quintanales', 'Raab', 'Raba', 'RÃ¡bade', 'RabadÃ¡n', 'Rabadans', 'Rabadeal', 'Rabadeales', 'RabadeaÃ±', 'Rabader', 'Rabadero', 'Rabaderol', 'Rabaderola', 'Rabaderse', 'Sabash', 'Sabass', 'Sabaton', 'Sabatons', 'Sabaud', 'Sabaudia', 'Sabaudians', 'Tage', 'Tagel', 'Tagen', 'Tagens', 'Tagera', 'Tageras', 'Tagere', 'Tageres', 'Udal', 'Udala', 'Udalas', 'Udalar', 'Udalaria', 'Udalarias', 'Udalaria', 'Vaal', 'Vaalaakra', 'Vaalaandra', 'Vaalandra', 'Vaalandra', 'Vaalandra', 'Waal', 'Waalaander', 'Waalaandra', 'Waalaandra', 'Waalaandra', 'Waalaandra', 'Xingu', 'Xinya', 'Xinyuan', 'Xinyuandi', 'Xinyuanjiazi', 'Xinyuanjiao', 'Yalu', 'Yalu River', 'Yalue', 'Yaluen', 'Yaluer', 'Yalues', 'Yalueing', 'Zaire', 'Zaireicho', 'Zaireibad', 'Zaireibag', 'Zaireibagak', 'Zaireibak', 'Zambezi', 'Zambesia', 'Zambesians', 'Zambesia', 'Zambesians', 'Zambesi'];

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
  {id:"landmark",icon:"\u{1F5FD}",title:"SehenswÃ¼rdigkeit",        group:"pure_geo",prompt:"In welchem Land liegt diese SehenswÃ¼rdigkeit?",desc:"Erkenne SehenswÃ¼rdigkeiten weltweit"},
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
  {id:"curr_real",  icon:"\u{1F4B5}",title:"Land \u2192 W\u00e4hrung",group:"lifestyle",prompt:"Welche W\u00e4hrung hat â€¦",     desc:"Nenne die W\u00e4hrung eines Landes"},
  {id:"pop_compare",icon:"\u{1F465}",title:"Mehr Einwohner?",      group:"lifestyle",prompt:"Hat [Land B] mehr oder weniger Einwohner?",desc:"Vergleiche Einwohnerzahlen zweier L\u00e4nder"},
  /* ---- EU Plates ---- */
  {id:"plate_casual",icon:"\u{1F697}",title:"EU-Kennzeichen",      group:"eu_plates",prompt:"Woher kommt dieses Kennzeichen?",          desc:"EU-Kennzeichen mit Hinweisen erkennen"},
  {id:"plate_hard",  icon:"\u{1F6A6}",title:"Kennzeichen Pro",     group:"eu_plates",prompt:"Region erkennen â€” kein Tipp\!",    desc:"EU-Kennzeichen ohne Hinweise â€” Profi-Level"},
  /* ---- Higher / Lower (existing) ---- */
  {id:"hl_pop",   icon:"\u{1F465}",title:"H/L Einwohner",  group:"hl_compare",prompt:"Mehr Einwohner?",   desc:"Welches Land hat mehr Einwohner?"},
  {id:"hl_river", icon:"\u{1F30A}",title:"H/L Flussl\u00e4nge", group:"hl_compare",prompt:"L\u00e4ngerer Fluss?",desc:"Welcher Fluss ist l\u00e4nger?"},
  {id:"hl_area",  icon:"\u{1F5FA}",title:"H/L Landfl\u00e4che",  group:"hl_compare",prompt:"Gr\u00f6\u00dferes Land?",desc:"Welches Land ist gr\u00f6\u00dfer?"},
  /* ---- Higher / Lower (coming soon) ---- */
  {id:"hl_gdp",       icon:"\u{1F4B0}",title:"H/L BIP",              group:"hl_compare",prompt:"H\u00f6heres BIP?",         desc:"Welches Land hat ein h\u00f6heres BIP?",           comingSoon:true},
  {id:"hl_density",   icon:"\u{1F3D8}",title:"H/L Bev\u00f6lkerungsdichte",group:"hl_compare",prompt:"Dichter besiedelt?",    desc:"Welches Land ist dichter besiedelt?",              comingSoon:true},
  {id:"hl_elevation", icon:"\u{26F0}",title:"H/L H\u00f6chster Punkt",group:"hl_compare",prompt:"H\u00f6herer Gipfel?",      desc:"Welches Land hat den h\u00f6heren Gipfel?",        comingSoon:true},
  {id:"hl_coastline", icon:"\u{1F3D6}",title:"H/L K\u00fcstÐµÐ½l\u00e4nge",group:"hl_compare",prompt:"L\u00e4ngere K\u00fcste?",desc:"Welches Land hat die l\u00e4ngere K\u00fcste?",   comingSoon:true},
  {id:"hl_borders",   icon:"\u{1F30F}",title:"H/L Nachbarl\u00e4nder",group:"hl_compare",prompt:"Mehr Nachbarn?",             desc:"Welches Land hat mehr Nachbarl\u00e4nder?",        comingSoon:true},
  {id:"hl_lifeexp",   icon:"\u2764",title:"H/L Lebenserwartung",   group:"hl_compare",prompt:"L\u00e4nger leben?",            desc:"In welchem Land lebt man l\u00e4nger?",            comingSoon:true},
  {id:"hl_median_age",icon:"\u{1F4C5}",title:"H/L Medianalter",    group:"hl_compare",prompt:"H\u00f6heres Medianalter?",     desc:"Welches Land hat ein h\u00f6heres Medianalter?",   comingSoon:true},
  {id:"hl_forest",    icon:"\u{1F333}",title:"H/L Waldf\u00e4che",  group:"hl_compare",prompt:"Mehr Wald?",                   desc:"Welches Land hat mehr Wald?",                      comingSoon:true},
  /* ---- Neighbors ---- */
  {id:"neighbor", icon:"\u{1F91D}",title:"Grenzg\u00e4nger",     group:"neighbors", prompt:"Grenzt an\u2026?",               desc:"Grenzt dieses Land an jenes?"},
  /* ---- Map ---- */
  {id:"map_guess",icon:"\u{1F5FA}",title:"Finde das Land",group:"map_mode",prompt:"Klick auf das gesuchte Land",             desc:"Klicke das gesuchte Land auf der Weltkarte",beta:true},
  /* ---- New Game Modes (coming soon) ---- */
  {id:"logic_grid",    icon:"\u{1F9E9}",title:"Logik-Gitter",          group:"new_modes",prompt:"L\u00f6se das R\u00e4tsel",                desc:"L\u00f6se geografische Logik-R\u00e4tsel",       beta:true},
  {id:"travel_route",  icon:"\u{1F5FA}",title:"Reiseroute",            group:"new_modes",prompt:"K\u00fcrzeste Route?",                      desc:"Plane die k\u00fcrzeste Route zwischen St\u00e4dten",beta:true},
  {id:"flag_fusion",   icon:"\u{1F3C1}",title:"Flaggen-Fusion",        group:"new_modes",prompt:"Welche zwei L\u00e4nder?",                  desc:"Erkenne L\u00e4nder aus verschmolzenen Flaggen",beta:true},
  {id:"climate_mystery",icon:"\u{1F326}",title:"Klima-Krimi",          group:"new_modes",prompt:"[BETA] Welches Land versteckt sich hinter diesen Klima-Hinweisen?",                             desc:"Land anhand von Klima-Clues erraten",                  beta:true},
  {id:"alpha_sprint",  icon:"ðŸ“",title:"Alphabet-Sprint",       group:"new_modes",prompt:"L\u00e4nder von A\u2013Z",                 desc:"Nenne L\u00e4nder f\u00fcr jeden Buchstaben",     comingSoon:true},
  {id:"wappen_meister",icon:"\u{1F6E1}",title:"Wappen-Meister",t_key:"mode_wappen",    group:"pure_geo",prompt:"Welchem Land geh\u00f6rt dieses Wappen?",desc:"Erkenne L\u00e4nder an ihrem Wappen",beta:true},
  {id:"slf",           icon:"ðŸ“",title:"Land & Hauptstadt",t_key:"mode_slf",noMultiplayer:true,  group:"pure_geo",prompt:"Nenne Land und Hauptstadt\u2026",    desc:"Kenne die HauptstÃ¤dte",  beta:true},
  {id:"timezone_jumper",icon:"\u23F0",title:"Zeitzonen-Jumper",       group:"new_modes",prompt:"Welche Zeitzone?",                            desc:"Meistere die Zeitzonen der Welt",beta:true},
  /* ---- Vergleiche / Comparisons (Phase 91+92) ---- */
  {id:"comp_area",      icon:"\u{1F5FA}",title:"Gr\u00f6\u00dferes Land?",      group:"comparisons",prompt:"Welches Land ist gr\u00f6\u00dfer?",       desc:"Fl\u00e4che zweier L\u00e4nder vergleichen",beta:true},
  {id:"comp_pop",       icon:"\u{1F465}",title:"Mehr Einwohner?",               group:"comparisons",prompt:"Welches Land hat mehr Einwohner?",       desc:"Bev\u00f6lkerung zweier L\u00e4nder vergleichen",beta:true},
  {id:"comp_north",     icon:"\u2b06\ufe0f",title:"Weiter n\u00f6rdlich?",     group:"comparisons",prompt:"Welches Land liegt n\u00f6rdlicher?",    desc:"Zwei L\u00e4nder nach Breitengrad",beta:true},
  {id:"comp_gdp",       icon:"\u{1F4B0}",title:"H\u00f6heres BIP?",            group:"comparisons",prompt:"H\u00f6heres BIP pro Kopf?",              desc:"BIP pro Kopf vergleichen",beta:true},
  {id:"comp_density",   icon:"\u{1F3D8}",title:"Dichter besiedelt?",            group:"comparisons",prompt:"Welches Land ist dichter besiedelt?",    desc:"Bev\u00f6lkerungsdichte vergleichen",beta:true},
  {id:"comp_elevation", icon:"\u26F0",   title:"H\u00f6herer Gipfel?",         group:"comparisons",prompt:"Welches Land hat den h\u00f6heren Gipfel?",desc:"H\u00f6chste Erhebung vergleichen",beta:true},
  {id:"comp_coast",     icon:"\u{1F3D6}",title:"L\u00e4ngere K\u00fcste?",    group:"comparisons",prompt:"Welches Land hat die l\u00e4ngere K\u00fcste?",desc:"K\u00fcstenl\u00e4nge vergleichen",beta:true},
  {id:"comp_borders",   icon:"\u{1F30F}",title:"Mehr Nachbarn?",               group:"comparisons",prompt:"Welches Land hat mehr Nachbarl\u00e4nder?",desc:"Anzahl der Nachbarn vergleichen",beta:true},
  {id:"comp_life",      icon:"\u2764",   title:"L\u00e4nger leben?",           group:"comparisons",prompt:"In welchem Land lebt man l\u00e4nger?",  desc:"Lebenserwartung vergleichen",beta:true},
  {id:"comp_age",       icon:"\u{1F4C5}",title:"H\u00f6heres Medianalter?",   group:"comparisons",prompt:"H\u00f6heres Medianalter?",               desc:"Medianalter zweier L\u00e4nder",beta:true},
  {id:"comp_forest",    icon:"\u{1F333}",title:"Mehr Wald?",                   group:"comparisons",prompt:"Welches Land hat mehr Waldfl\u00e4che?",  desc:"Waldfl\u00e4che vergleichen",beta:true},
  /* Phase 129+130 BETA modes */
  {id:"comp_airports",  icon:"\u2708\uFE0F",title:"Mehr Flugh\u00e4fen?",    group:"comparisons",prompt:"Welches Land hat mehr Flugh\u00e4fen?",             desc:"Flughafenanzahl zweier L\u00e4nder vergleichen"},
  {id:"comp_flight",    icon:"\u{1F5FA}",title:"Gr\u00f6\u00dferes Land?",  group:"comparisons",prompt:"L\u00e4ngster m\u00f6glicher Inlandsflug?",          desc:"Fl\u00e4che als Proxy f\u00fcr Inlandsflugdistanz"},
  {id:"comp_mountain",  icon:"\u26F0",  title:"H\u00f6herer Gipfel?",          group:"comparisons",prompt:"Welches Land hat den h\u00f6heren Gipfel?",        desc:"H\u00f6chste Erhebung (erweiterter Datensatz)"},
  {id:"comp_nsextent",  icon:"\u{1F9ED}",title:"L\u00e4nger Nord-S\u00fcd?", group:"comparisons",prompt:"Welches Land erstreckt sich weiter von Nord nach S\u00fcd?",         desc:"Nord-S\u00fcd-Ausdehnung vergleichen"},
  {id:"comp_olympics",  icon:"\u{1F3C5}",title:"Mehr Olympia-Gold?",           group:"comparisons",prompt:"Welches Land hat mehr Olympia-Goldmedaillen?",         desc:"Sommerolympiade-Goldmedaillen vergleichen"},
  {id:"iata",           icon:"\u2708\uFE0F",title:"IATA-Code?",               group:"airports_beta",prompt:"[BETA] Zu welcher Stadt geh\u00f6rt dieser Flughafen-Code?", desc:"IATA-Codes der gro\u00dfen Flugh\u00e4fen kennen",beta:true},
  {id:"beta_timezone",  icon:"\u23F0",  title:"Welche Uhrzeit?",               group:"airports_beta",prompt:"[BETA] Wie sp\u00e4t ist es gerade in dieser Stadt?", desc:"UTC-Offsets und Zeitzonen",beta:true},
  {id:"beta_climate",   icon:"\u{1F321}\uFE0F",title:"Klima-Krimi?",          group:"airports_beta",prompt:"[BETA] Welches Land versteckt sich hinter diesen Klima-Hinweisen?", desc:"Land anhand von Klima-Clues erraten",beta:true},
  {id:"beta_flagcolor", icon:"\u{1F6A9}",title:"Flaggen-Farben?",              group:"airports_beta",prompt:"[BETA] Welche Farbe fehlt in dieser Flagge?",     desc:"Flaggenfarben auswendig kennen",beta:true},
  {id:"beta_landlocked",icon:"\u{1F30A}",title:"Binnenstaat?",                 group:"airports_beta",prompt:"[BETA] Welches Land hat keinen Meereszugang?",    desc:"Binnenstaaten von K\u00fcstenl\u00e4ndern unterscheiden",beta:true},
];

function modeTitle(m){return m&&m.t_key?t(m.t_key):m?m.title:"";}
const MODE_CATS={
  pure_geo:{label:"Pure Geo",icon:"\u{1F30D}",modes:["city","flag","capital","river","landmark","park","unesco","citymark","subway","flagsel","rcapital","rcity","rriver","river_real","logic_grid","travel_route","flag_fusion","climate_mystery","alpha_sprint","timezone_jumper","wappen_meister","slf"],cost:0},
  lifestyle:{label:"Kultur & Lifestyle",icon:"\u{1F3A8}",modes:["outline","food","brand","currency","curr_real","pop_compare"],cost:1000},
  eu_plates:{label:"EU-Kennzeichen",icon:"\u{1F697}",modes:["plate_casual","plate_hard"],cost:500},
  hl_compare:{label:"Higher / Lower",icon:"\u2b06\ufe0f",modes:["hl_pop","hl_river","hl_area","hl_gdp","hl_density","hl_elevation","hl_coastline","hl_borders","hl_lifeexp","hl_median_age","hl_forest"],cost:0},
  comparisons:{label:"Vergleiche",icon:"\u2696\ufe0f",modes:["comp_area","comp_pop","comp_north","comp_gdp","comp_density","comp_elevation","comp_coast","comp_borders","comp_life","comp_age","comp_forest","comp_airports","comp_flight","comp_mountain","comp_nsextent","comp_olympics"],cost:0},
  airports_beta:{label:"Airports & BETA",icon:"\u2708\uFE0F",modes:["iata","beta_timezone","beta_climate","beta_flagcolor","beta_landlocked"],cost:0},
  neighbors:{label:"Nachbarl\u00e4nder",icon:"\u{1F91D}",modes:["neighbor"],cost:0},
  map_mode:{label:"Weltkarte",icon:"\u{1F5FA}",modes:["map_guess"],cost:0},
};

/* Phase 28: New real-data mode generators */
function genCurrRealQ(){
  if(!CURR_REAL||!CURR_REAL.length)return null;
  const _fcc=_rfilt(COUNTRIES,2);const _ccc=new Set(_fcc.map(x=>x.cc));
  const _crPool=CURR_REAL.filter(x=>_ccc.has(ccFromCountry(x.c)));
  const _crSrc=_crPool.length>=2?_crPool:CURR_REAL;
  const idx=~~(rng()*_crSrc.length);
  const cor=_crSrc[idx];
  /* Show only currency name+ISO â€” NOT country name (would give away the answer) */
  const dis=CURR_REAL.filter((_,i)=>i!==idx).sort(()=>rng()-.5).slice(0,3).map(x=>x.n+" ("+x.iso+")");
  const ans=cor.n+" ("+cor.iso+")";
  return{type:"curr_real",prompt:"Welche W\u00e4hrung hat â€¦",subj:cor.c,ans,opts:sh([ans,...dis]),meta:cor.n,lid:cor.c,cc:ccFromCountry(cor.c)};
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
  return{type:"river_real",prompt:t("q_river_real"),subj:cor.n,ans:cor.c,opts:sh([cor.c,...dis]),meta,lid:cor.n,cc:ccFromCountry(cor.c)};
}

/* Phase 30 â€” Default neighbor map (fallback when neighbors.json is empty/broken) */
/* Phase 91+92: static comparison data â€” 96 countries */
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
  "Deutschland":["Frankreich","Belgien","Niederlande","Luxemburg","Schweiz","Ã–sterreich","Tschechien","Polen","DÃ¤nemark"],
  "Frankreich":["Deutschland","Belgien","Luxemburg","Schweiz","Italien","Spanien","Andorra","Monaco"],
  "Polen":["Deutschland","Tschechien","Slowakei","Ukraine","Belarus","Litauen","Russland"],
  "Ã–sterreich":["Deutschland","Schweiz","Liechtenstein","Italien","Slowenien","Ungarn","Slowakei","Tschechien"],
  "Schweiz":["Deutschland","Frankreich","Italien","Ã–sterreich","Liechtenstein"],
  "Spanien":["Frankreich","Andorra","Portugal"],
  "Portugal":["Spanien"],
  "Italien":["Frankreich","Schweiz","Ã–sterreich","Slowenien","San Marino"],
  "Russland":["Norwegen","Finnland","Estland","Lettland","Belarus","Ukraine","Georgien","Kasachstan","China","Mongolei","Nordkorea"],
  "China":["Russland","Mongolei","Kasachstan","Kirgisistan","Tadschikistan","Afghanistan","Pakistan","Indien","Nepal","Bhutan","Myanmar","Laos","Vietnam","Nordkorea"],
  "Indien":["Pakistan","China","Nepal","Bhutan","Bangladesh","Myanmar"],
  "Brasilien":["Venezuela","Guyana","Kolumbien","Peru","Bolivien","Paraguay","Argentinien","Uruguay"],
  "USA":["Kanada","Mexiko"],
  "Kanada":["USA"],
  "Mexiko":["USA","Guatemala","Belize"],
  "Argentinien":["Chile","Bolivien","Paraguay","Brasilien","Uruguay"],
  "Ukraine":["Russland","Belarus","Polen","Slowakei","Ungarn","RumÃ¤nien","Moldawien"],
  "Belarus":["Russland","Ukraine","Polen","Litauen","Lettland"],
  "TÃ¼rkei":["Griechenland","Bulgarien","Georgien","Armenien","Aserbaidschan","Iran","Irak","Syrien"],
  "Iran":["TÃ¼rkei","Irak","Afghanistan","Pakistan","Turkmenistan","Aserbaidschan","Armenien"],
  "Afghanistan":["Iran","Pakistan","Tadschikistan","Turkmenistan","Usbekistan","China"],
  "Pakistan":["Indien","Afghanistan","Iran","China"],
  "Irak":["TÃ¼rkei","Syrien","Jordanien","Saudi-Arabien","Kuwait","Iran"],
  "Syrien":["TÃ¼rkei","Irak","Jordanien","Libanon","Israel"],
  "Saudi-Arabien":["Jordanien","Irak","Kuwait","Bahrain","Katar","VAE","Oman","Jemen"],
  "Ã„gypten":["Israel","Sudan","Libyen"],
  "Sudan":["Ã„gypten","Libyen","Tschad","Zentralafrikanische Republik","SÃ¼dsudan","Ã„thiopien","Eritrea"],
  "Ã„thiopien":["Eritrea","Dschibuti","Somalia","Kenia","Sudan","SÃ¼dsudan"],
  "Nigeria":["Benin","Niger","Kamerun","Tschad"],
  "Demokratische Republik Kongo":["Republik Kongo","Angola","Sambia","Tansania","Ruanda","Burundi","Uganda","Zentralafrikanische Republik","SÃ¼dsudan"],
  "SÃ¼dafrika":["Namibia","Botswana","Simbabwe","Mosambik","Eswatini","Lesotho"],
  "Kenia":["Ã„thiopien","Somalia","Tansania","Uganda","SÃ¼dsudan"],
  "Ungarn":["Ã–sterreich","Slowakei","Ukraine","RumÃ¤nien","Serbien","Kroatien","Slowenien"],
  "RumÃ¤nien":["Ungarn","Ukraine","Moldawien","Bulgarien","Serbien"],
  "Griechenland":["Albanien","Nordmazedonien","Bulgarien","TÃ¼rkei"],
  "Schweden":["Norwegen","Finnland","DÃ¤nemark"],
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
  "Tschechien":["Deutschland","Polen","Slowakei","Ã–sterreich"],
  "Slowakei":["Tschechien","Polen","Ukraine","Ungarn","Ã–sterreich"],
  "Bulgarien":["RumÃ¤nien","Serbien","Nordmazedonien","Griechenland","TÃ¼rkei"],
  "Serbien":["Ungarn","RumÃ¤nien","Bulgarien","Nordmazedonien","Kosovo","Montenegro","Bosnien","Kroatien"],
  "Kroatien":["Slowenien","Ungarn","Serbien","Bosnien","Montenegro"],
  "Slowenien":["Italien","Ã–sterreich","Ungarn","Kroatien"],
};
/* Phase 86 â€” Grenzkarte (nur Laender aus COUNTRIES) */
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
/* Phase 144 â€” Grid-Kriterien (Diversity Overhaul) */
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
  const ai=~~(rng()*pool.length);let bi=~~(rng()*pool.length);while(bi===ai)bi=~~(rng()*pool.length);
  const a=pool[ai],b=pool[bi];
  const fmt=(p)=>p>=1e9?(p/1e9).toFixed(2)+" Mrd.":p>=1e6?(p/1e6).toFixed(1)+" Mio.":(p/1e3).toFixed(0)+" Tsd.";
  const ans=b.pop>a.pop?"higher":"lower";
  return{type:"hl_pop",prompt:t("q_hl_pop",{a:a.c}),nameA:a.c,valA:fmt(a.pop),nameB:b.c,valB:fmt(b.pop),ans,opts:["higher","lower"],lid:b.c,cc:ccFromCountry(b.c)};
}
function genHLRiverQ(){
  if(\!RIVERS_REAL||RIVERS_REAL.length<2)return null;
  const _fcr=_rfilt(COUNTRIES,4);const _ccr=new Set(_fcr.map(x=>x.cc));
  let pool=RIVERS_REAL.filter(r=>r.len>100&&_ccr.has(ccFromCountry(r.c)));
  if(pool.length<2)pool=RIVERS_REAL.filter(r=>r.len>100);if(pool.length<2)return null;
  const ai=~~(rng()*pool.length);let bi=~~(rng()*pool.length);while(bi===ai)bi=~~(rng()*pool.length);
  const a=pool[ai],b=pool[bi];
  const ans=b.len>a.len?"higher":"lower";
  return{type:"hl_river",prompt:t("q_hl_river",{a:a.n}),nameA:a.n,valA:a.len+" km",nameB:b.n,valB:b.len+" km",ans,opts:["higher","lower"],lid:b.n,cc:ccFromCountry(b.c)};
}
function genHLAreaQ(){
  if(\!AREA_DATA||AREA_DATA.length<2)return null;
  const _fca=_rfilt(COUNTRIES,4);const _cca=new Set(_fca.map(x=>x.cc));
  let pool=AREA_DATA.filter(x=>_cca.has(ccFromCountry(x.c)));
  if(pool.length<2)pool=AREA_DATA.slice();if(pool.length<2)return null;
  const ai=~~(rng()*pool.length);let bi=~~(rng()*pool.length);while(bi===ai)bi=~~(rng()*pool.length);
  const a=pool[ai],b=pool[bi];
  const fmt=(x)=>x>=1e6?(x/1e6).toFixed(2)+" Mio. kmÂ²":(x/1000).toFixed(0)+" Tsd. kmÂ²";
  const ans=b.area>a.area?"higher":"lower";
  return{type:"hl_area",prompt:t("q_hl_area",{a:a.c}),nameA:a.c,valA:fmt(a.area),nameB:b.c,valB:fmt(b.area),ans,opts:["higher","lower"],lid:b.c,cc:ccFromCountry(b.c)};
}
/* Phase 95: inline area (kmÂ²) + population (millions) â€” self-contained, no external files */
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
  const ai=~~(rng()*pool.length);let bi=~~(rng()*pool.length);while(bi===ai)bi=~~(rng()*pool.length);
  return[pool[ai],pool[bi]];
}
function _compQ(type,prompt,a,b,aVal,bVal,fmtFn){
  const ans=bVal>aVal?b:a;
  const meta=displayCountry(a)+': '+fmtFn(aVal)+' Â· '+displayCountry(b)+': '+fmtFn(bVal);
  return{type,prompt,subj:'',opts:[a,b],ans,meta,lid:a+'|'+b,cc:ccFromCountry(ans)};
}
function genCompAreaQ(){
  /* Phase 95: uses inline COMP_AREA â€” no external file needed */
  const keys=Object.keys(COMP_AREA);
  if(keys.length<2)return null;
  const _fc=_rfilt(COUNTRIES,4);const _cc=new Set(_fc.map(x=>x.cc));
  let pool=keys.filter(k=>_cc.has(ccFromCountry(k)));
  if(pool.length<2)pool=keys.slice();if(pool.length<2)return null;
  const ai=~~(rng()*pool.length);let bi=~~(rng()*pool.length);while(bi===ai)bi=~~(rng()*pool.length);
  const a=pool[ai],b=pool[bi];
  const fmt=(x)=>x>=1e6?(x/1e6).toFixed(2)+' Mio. kmÂ²':(x/1000).toFixed(0)+' Tsd. kmÂ²';
  return _compQ('comp_area','Welches Land ist grÃ¶ÃŸer?',a,b,COMP_AREA[a],COMP_AREA[b],fmt);
}
function genCompPopQ(){
  /* Phase 95: uses inline COMP_POP (millions) â€” no external file needed */
  const keys=Object.keys(COMP_POP);
  if(keys.length<2)return null;
  const _fc=_rfilt(COUNTRIES,4);const _cc=new Set(_fc.map(x=>x.cc));
  let pool=keys.filter(k=>COMP_POP[k]>0.5&&_cc.has(ccFromCountry(k)));
  if(pool.length<2)pool=keys.filter(k=>COMP_POP[k]>0.5);if(pool.length<2)return null;
  const ai=~~(rng()*pool.length);let bi=~~(rng()*pool.length);while(bi===ai)bi=~~(rng()*pool.length);
  const a=pool[ai],b=pool[bi];
  const pa=COMP_POP[a]*1e6,pb=COMP_POP[b]*1e6;
  const fmt=(p)=>p>=1e9?(p/1e9).toFixed(2)+' Mrd.':p>=1e6?(p/1e6).toFixed(1)+' Mio.':(p/1e3).toFixed(0)+' Tsd.';
  return _compQ('comp_pop','Welches Land hat mehr Einwohner?',a,b,pa,pb,fmt);
}
function genCompNorthQ(){
  const r=_compPick('lat',null);if(!r)return null;
  const[a,b]=r;
  if(COMP_DATA[a].lat===COMP_DATA[b].lat)return null;
  const fmt=(x)=>Math.abs(x).toFixed(0)+'Â° '+(x>=0?'N':'S');
  return _compQ('comp_north','Welches Land liegt weiter nÃ¶rdlich?',a,b,COMP_DATA[a].lat,COMP_DATA[b].lat,fmt);
}
function genCompGdpQ(){
  const r=_compPick('gdp',null);if(!r)return null;
  const[a,b]=r;
  if(COMP_DATA[a].gdp===COMP_DATA[b].gdp)return null;
  const fmt=(x)=>'$ '+(x>=1000?(x/1000).toFixed(0)+' Tsd.':x);
  return _compQ('comp_gdp','Welches Land hat ein hÃ¶heres BIP pro Kopf?',a,b,COMP_DATA[a].gdp,COMP_DATA[b].gdp,fmt);
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
  return _compQ('comp_elevation','Welches Land hat den hÃ¶heren Gipfel?',a,b,COMP_DATA[a].elev,COMP_DATA[b].elev,fmt);
}
function genCompCoastQ(){
  const r=_compPick('coast',d=>d.coast>0);if(!r)return null;
  const[a,b]=r;
  if(COMP_DATA[a].coast===COMP_DATA[b].coast)return null;
  const fmt=(x)=>x.toLocaleString('de-DE')+' km';
  return _compQ('comp_coast','Welches Land hat die lÃ¤ngere KÃ¼ste?',a,b,COMP_DATA[a].coast,COMP_DATA[b].coast,fmt);
}
function genCompBordersQ(){
  const r=_compPick('bord',d=>d.bord>0);if(!r)return null;
  const[a,b]=r;
  if(COMP_DATA[a].bord===COMP_DATA[b].bord)return null;
  const fmt=(x)=>x+' Nachbarn';
  return _compQ('comp_borders','Welches Land hat mehr NachbarlÃ¤nder?',a,b,COMP_DATA[a].bord,COMP_DATA[b].bord,fmt);
}
function genCompLifeQ(){
  const r=_compPick('life',null);if(!r)return null;
  const[a,b]=r;
  if(COMP_DATA[a].life===COMP_DATA[b].life)return null;
  const fmt=(x)=>x+' Jahre';
  return _compQ('comp_life','In welchem Land lebt man lÃ¤nger?',a,b,COMP_DATA[a].life,COMP_DATA[b].life,fmt);
}
function genCompAgeQ(){
  const r=_compPick('age',null);if(!r)return null;
  const[a,b]=r;
  if(COMP_DATA[a].age===COMP_DATA[b].age)return null;
  const fmt=(x)=>x+' Jahre';
  return _compQ('comp_age','Welches Land hat ein hÃ¶heres Medianalter?',a,b,COMP_DATA[a].age,COMP_DATA[b].age,fmt);
}
function genCompForestQ(){
  const r=_compPick('forest',null);if(!r)return null;
  const[a,b]=r;
  if(COMP_DATA[a].forest===COMP_DATA[b].forest)return null;
  const fmt=(x)=>x+' %';
  return _compQ('comp_forest','Welches Land hat mehr WaldflÃ¤che?',a,b,COMP_DATA[a].forest,COMP_DATA[b].forest,fmt);
}
function genNeighborQ(){
  const nb=NEIGHBORS;const valid=Object.keys(nb).filter(c=>nb[c]&&nb[c].length>=2);if(\!valid.length)return null;
  const country=valid[~~(rng()*valid.length)];const neighborList=nb[country];
  const allC=Object.keys(nb);const nonNb=allC.filter(c=>c\!==country&&\!neighborList.includes(c));if(\!nonNb.length)return null;
  const type2=rng()>.5;
  if(type2&&neighborList.length>=2){
    const ans=nonNb[~~(rng()*nonNb.length)];
    const dis=neighborList.slice().sort(()=>rng()-.5).slice(0,2);
    return{type:"neighbor",prompt:"Grenzt NICHT an\u2026?",subj:country,ans,opts:sh([ans,...dis]),lid:country+'|'+ans,cc:ccFromCountry(country)||''};
  }else{
    const ans=neighborList[~~(rng()*neighborList.length)];
    const dis=nonNb.slice().sort(()=>rng()-.5).slice(0,3);
    return{type:"neighbor",prompt:"Welches Land grenzt an\u2026?",subj:country,ans,opts:sh([ans,...dis.slice(0,3)]),lid:country+'|'+ans,cc:ccFromCountry(country)||''};
  }
}

/* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
   PHASE 33 â€” REALTIME 1vs1 MULTIPLAYER  (Supabase Broadcast)
   â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */

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
      /* Sync start â€” same seed on both sides */
      initRng(seed);
      startGame(mode||"city");
      /* Tag session as multiplayer */
      S.mpSeed=seed;S.mpOpponent=_oppName;
      S.mpOppScore=0;S.mpOppRd=0;S.mpOppFinal=null;
    }else render();
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
  if(\!code||code.length<4){showToast("Bitte gÃ¼ltigen Code eingeben\!");return;}
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
          <button class="btn-p" style="width:auto;padding:.6rem 1.2rem" onclick="mpJoin(S._mpJoinCode)">â–¶</button>
        </div>
      </div>
      <button class="mp-back-btn" onclick="S.mpModal=false;render()">\u2b05\ufe0f ZurÃ¼ck zum HauptmenÃ¼</button>
    </div>`;
  }

  /* â”€â”€ Phase: host waiting for guest â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
  if(mp.phase==="waiting"){
    return`<div class="scr" style="text-align:center">
      <button class="mp-back-btn" style="margin-bottom:.5rem" onclick="mpLeave()">\u2b05\ufe0f Abbrechen</button>
      <div style="clear:both;padding-top:.5rem"></div>
      <div style="font-size:3rem;margin:1rem 0">\u{1F4F1}</div>
      <h2 style="font-size:1.3rem;font-weight:900;color:var(--text);margin-bottom:.5rem">Warte auf Gegnerâ€¦</h2>
      <p style="color:var(--text3);font-size:.82rem;margin-bottom:1.4rem">Gib diesen Code an deinen Freund:</p>
      <div style="display:inline-block;background:var(--bg3);border:3px solid #7c3aed;border-radius:16px;padding:1rem 2rem;font-size:3rem;font-weight:900;letter-spacing:10px;color:#7c3aed;margin-bottom:1rem">${esc(mp.code)}</div>
      <p style="color:var(--text3);font-size:.74rem">Verbunden â€” Channel aktiv</p>
      <div style="margin-top:1.5rem;display:flex;justify-content:center">
        <div class="spinner"></div>
      </div>
    </div>`;
  }

  /* â”€â”€ Phase: guest joining â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
  if(mp.phase==="joining"){
    return`<div class="scr" style="text-align:center">
      <div style="font-size:3rem;margin:2rem 0">\u{1F50D}</div>
      <h2 style="font-size:1.2rem;font-weight:900;color:var(--text)">Verbinde mit Raum ${esc(mp.code)}â€¦</h2>
      <div style="margin-top:1.5rem;display:flex;justify-content:center"><div class="spinner"></div></div>
    </div>`;
  }

  /* â”€â”€ Phase: both in room â€” ready check â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
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
          <div style="font-size:1.3rem">${myR?"âœ…":"â³"}</div>
          <div style="font-size:.72rem;color:var(--text3);margin-top:4px">Du</div>
        </div>
        <div style="font-size:1.4rem;align-self:center;color:var(--text3)">VS</div>
        <div style="background:var(--bg2);border:2px solid ${oppR?"#10b981":"var(--border)"};border-radius:12px;padding:.75rem 1.2rem;min-width:100px">
          <div style="font-size:1.3rem">${oppR?"âœ…":"â³"}</div>
          <div style="font-size:.72rem;color:var(--text3);margin-top:4px">${esc(mp.oppName||"Gegner")}</div>
        </div>
      </div>
      ${myR?`<div style="color:var(--text3);font-size:.82rem">Warte auf ${esc(mp.oppName||"Gegner")}â€¦</div>`
           :`<button class="btn-p" style="width:100%;font-size:1.1rem" onclick="mpReady()">\u{1F3C1} Bereit\!</button>`}
    </div>`;
  }

  /* â”€â”€ Phase: countdown â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
  if(mp.phase==="countdown"){
    return`<div class="scr" style="text-align:center;padding-top:30%">
      <div style="font-size:6rem;font-weight:900;color:#7c3aed;line-height:1">${mp.countdown}</div>
      <div style="color:var(--text2);font-size:1rem;margin-top:.8rem">Spiel startetâ€¦</div>
    </div>`;
  }

  return`<div class="scr"><button onclick="mpLeave()">â† ${t("btn_back")}</button></div>`;
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
function isCategoryUnlocked(catId){return true;/* TEST MODE â€” all categories unlocked */}
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
      if(S.diff==="survival"){tIv=setInterval(()=>{S.tm--;if(S.tm===3)soundWarn();if(S.tm<=0){clearInterval(tIv);if(S.q)answer(null);}else render();},1000);}
    }
  },10000);
}

const ROUNDS=10,BASE=100,TB=10;
/* Phase 81 â€” Titel-Schwellenwerte */
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
  {m:10,x:3.0,l:"\u{1F525}\u{1F525}\u{1F525} LEGEND\u00c4R â€” 3\u00d7"},
  {m:5, x:2.0,l:"\u{1F525}\u{1F525} ON FIRE â€” 2\u00d7"},
  {m:3, x:1.5,l:"\u{1F525} HEISS â€” 1.5\u00d7"},
  {m:0, x:1.0,l:""},
];

/* SUPABASE */
let sb=null,sbUser=null,sbProfile=null,sbStamps=new Set();
/* CURR_REAL, CAPS_POP, RIVERS_REAL populated by loadGameData() */
/* Helper: country name â†’ cc */
function ccFromCountry(name){const c=COUNTRIES.find(x=>x.c===name);return c?c.cc:null;}
function flagOf(name){const cc=ccFromCountry(name);return cc?`<img src="https://flagcdn.com/w40/${cc}.png" style="height:22px;vertical-align:middle;border-radius:2px" alt="${name}" onerror="this.style.display='none'">`:"";}

/* Phase 97-1: Zombie-SW-Killer â€” lÃ¤uft vor Supabase-Init */
/* TÃ¶tet veraltete Service Worker, die Updates blockieren   */
(function _zombieKiller(){
  var SW_VER='gq-v9',LS_KEY='__gq_sw_ver';
  try{
    if(localStorage.getItem(LS_KEY)===SW_VER)return; /* aktuell â€” nichts zu tun */
    if(!('serviceWorker' in navigator)){localStorage.setItem(LS_KEY,SW_VER);return;}
    navigator.serviceWorker.getRegistrations().then(function(regs){
      if(regs.length===0){localStorage.setItem(LS_KEY,SW_VER);return;}
      /* Alter/zombie SW gefunden â†’ nuklearer Reset */
      console.warn('[GQ] Zombie-SW: killing',regs.length,'registration(s) + wiping caches...');
      /* 1. Korrupte Auth-Tokens lÃ¶schen */
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
        location.reload(true); /* Hard-Reload â€” erzwingt frisches HTML vom Server */
      });
    });
  }catch(e){console.warn('[GQ] zombieKiller error:',e);}
})();

const sbOK=SUPABASE_URL.includes("supabase.co");
let sbAuthPending=sbOK; /* Phase 81: true until getSession() resolves */
if(sbOK){
  try{
    /* Phase 100: auth.lock bypass â€” verhindert navigator.locks Deadlock bei _initialize() */
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
  /* Phase 89: interner WÃ¤chter â€” falls getSession()/signInAnonymously() nie settled */
  const _authTO=setTimeout(()=>{
    if(sbAuthPending){
      console.warn("[GQ] initAuth: 4s WÃ¤chter ausgelÃ¶st â€” bereinige Auth-Tokens...");
      /* Phase 93: korrupte Supabase-Tokens aus localStorage lÃ¶schen */
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
      /* Phase 101: loadProfile ohne await â€” sonst blockiert _notifyAllSubscribers */
      if(\!sbUser||sbUser.id\!==session.user.id){sbUser=session.user;loadProfile();}
    }
  });
  try{
    /* Phase 97-2: getSession mit 3s Timeout â€” kein endloses HÃ¤ngen */
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
    clearTimeout(_authTO); /* Phase 89: WÃ¤chter stoppen */
    /* ALWAYS unblock render â€” even if Supabase throws */
    sbAuthPending=false;
    console.log("[GQ] initAuth() finally â€” sbAuthPending=false, calling render()");
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
  /* Phase 93: Smart-Merge Kennzeichen â€” Cloud âˆª Lokal */
  if(data&&typeof data.plates_collected==="string"){
    try{
      const _cp=JSON.parse(data.plates_collected||"[]");
      if(Array.isArray(_cp)&&_cp.length>0){
        const _lp=_gqLoad("gq_coll",[]);
        const _mp=[...new Set([..._lp,..._cp])];
        _gqSave("gq_coll",_mp);
        S.collectedPlates=_mp;
        /* Merged Stand zurÃ¼ck in Cloud pushen wenn gewachsen */
        if(_mp.length>_cp.length){
          sb.from("profiles").update({plates_collected:JSON.stringify(_mp)})
            .eq("id",sbUser.id).then(()=>{},()=>{});
        }
      }else if(!data.plates_collected||data.plates_collected==="[]"){
        /* Noch keine Cloud-Daten â€” lokale Daten hochladen */
        const _lp2=_gqLoad("gq_coll",[]);
        if(_lp2.length>0){
          sb.from("profiles").update({plates_collected:JSON.stringify(_lp2)})
            .eq("id",sbUser.id).then(()=>{},()=>{});
        }
      }
    }catch(_e){console.warn("[GQ] plates-merge Fehler",_e);}
  }else if(data&&!data.plates_collected){
    /* Spalte fehlt noch (vor Migration) â€” lokale Daten sind maÃŸgeblich */
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
  if(pw!==S.authConfirm){S.authError="Die PasswÃ¶rter stimmen nicht Ã¼berein.";render();return;}
  S.authLoading=true;S.authError="";render();
  /* Phase 90: 5s Timeout-Waechter */
  setTimeout(()=>{
    if(S.authLoading){S.authLoading=false;S.authError="Netzwerk-Timeout. Bitte Ã¼berprÃ¼fe deine Verbindung.";render();}
  },5000);
  try{
    const{data,error}=await sb.auth.signUp({email,password:pw,options:{data:{username:uname}}});
    if(error){
      const _em=error.message||"";
      S.authError=
        _em.includes("already registered")||_em.includes("already been registered")?"Diese E-Mail ist bereits registriert.":
        _em.includes("Password should be")||_em.includes("password")?"Passwort zu schwach (mind. 6 Zeichen).":
        _em.includes("valid email")||_em.includes("invalid format")||_em.includes("Unable to validate email")?"Bitte eine gÃ¼ltige E-Mail-Adresse eingeben.":
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
      _em.includes("valid email")||_em.includes("invalid format")?"Bitte eine gÃ¼ltige E-Mail-Adresse eingeben.":
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
    if(S.authLoading){S.authLoading=false;S.authError="Netzwerk-Timeout. Bitte Ã¼berprÃ¼fe deine Verbindung.";render();}
  },5000);
  try{
    const{data,error}=await sb.auth.signInWithPassword({email,password:pw});
    if(error){
      const _m=error.message;
      S.authError=_m==="Invalid login credentials"?"E-Mail oder Passwort falsch.":
        _m.includes("Email not confirmed")?"Bitte bestÃ¤tige zuerst deine E-Mail-Adresse!":
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
  /* Reset UI state â€” prevents stale mid-game or modal views after logout */
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
/* Phase 85 â€” Coming Soon toast */
function showComingSoonToast(name){showToast("\u{1F680} "+name+" kommt bald\! Bleib gespannt.");}
async function saveSession(mode,score,bs,correct,durationMs){
  /* Sanity-cap score before submitting â€” max honest = ROUNDS*(BASE+12*TB)*3*3 */
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
  await sb.from("game_sessions").insert({user_id:sbUser.id,mode,score,best_streak:bs,rounds:ROUNDS,accuracy:Math.round(correct/ROUNDS*100),username:sbProfile?.username||null});
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
/* Phase 81 â€” Titel-System */
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
  activeCategory:"pure_geo",
  fcIdx:0,fcFlipped:false,fcSearch:"",fcCountry:"all",
  darkMode:false,
  authMode:"login",authEmail:"",authPassword:"",authConfirm:"",authUsername:"",authError:"",authLoading:false,
  settingsModal:false,
  convModal:false,
  collectedPlates:loadCollectedPlates(),
  ligaData:[],ligaLoading:false,leagueEvalResult:null,
  titleShop:false,
  language:(()=>{const _sl=localStorage.getItem("gq_lang");if(_sl&&LANG[_sl])return _sl;const _bl=(navigator.language||"de").substring(0,2).toLowerCase();return LANG[_bl]?_bl:"de";})(),spotterInput:"",spotterMsg:"",spotterOk:null,albumView:"list",albumCountry:_smartDefaultCountry(),spotterCountry:_smartDefaultCountry(),
  collFilter:"all",collRarity:"all",collSearch:"",
};
let tIv=null,fTo=null,toastTo=null;

/* â”€â”€ Phase 42: Anti-Cheat â€” Proxy wrapper for S in console â”€â”€ */
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
            "checkMastery","spotterCollect","saveSession","loadData","initAuth"];
          const ok=trusted.some(fn=>stk.includes(fn));
          if(!ok){
            console.warn("%cðŸš« GeoQuest: Schummeln erkannt! Feld '"+k+"' ist geschÃ¼tzt.",
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
  const pf=S.diff==="hardcore"?0:200000;
  const pool=_rfilt(CITIES.filter(c=>c.pop>=pf&&c.id\!==S.lid),3);
  if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.sub===cor.sub||x.cont===cor.cont,x=>x.c===cor.c,x=>x.c);
  return{type:"city",prompt:t("q_city"),subj:cor.n,ans:cor.c,opts:sh([cor.c,...dis]),meta:cor.cont+" \u00b7 "+(cor.pop/1e6).toFixed(1)+" Mio.",lid:cor.id,cc:cor.cc};
}
function genFlagQ(){
  const pool=_rfilt(COUNTRIES.filter(x=>x.cc\!==S.lid),3);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.sr===cor.sr||x.ct===cor.ct,x=>x.c===cor.c,x=>x.c);
  return{type:"flag",prompt:t("q_flag"),subj:cor.cc,ans:cor.c,opts:sh([cor.c,...dis]),meta:cor.ct,lid:cor.cc,cc:cor.cc};
}
function genCapitalQ(){
  const pool=_rfilt(CAPITALS.filter(x=>x.capital\!==S.lid),3);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.subregion===cor.subregion||x.continent===cor.continent,x=>x.country===cor.country,x=>x.country);
  return{type:"capital",prompt:t("q_capital"),subj:cor.capital,ans:cor.country,opts:sh([cor.country,...dis]),meta:cor.continent,lid:cor.capital,cc:cor.cc};
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
  const pool=_rfilt(RIVERS.filter(x=>x.name\!==S.lid),3);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const _cpool=_rfilt(COUNTRIES,4);const dis=distractors(_cpool,x=>x.sr===cor.subregion||x.ct===cor.continent,x=>x.c===cor.country,x=>x.c);
  return{type:"river",prompt:t("q_river"),subj:cor.name,ans:cor.country,opts:sh([cor.country,...dis]),meta:cor.continent,lid:cor.name,cc:cor.cc};
}
function genLandmarkQ(){
  const pool=_rfilt(LANDMARKS.filter(x=>x.name\!==S.lid),3);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const _cpool=_rfilt(COUNTRIES,4);const dis=distractors(_cpool,x=>x.sr===cor.subregion||x.ct===cor.continent,x=>x.c===cor.country,x=>x.c);
  return{type:"landmark",prompt:t("q_landmark"),subj:cor.name,ans:cor.country,opts:sh([cor.country,...dis]),meta:cor.continent,lid:cor.name,cc:cor.cc};
}
function genParkQ(){
  const pool=_rfilt(NATIONAL_PARKS.filter(x=>x.name\!==S.lid),3);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const _cpool=_rfilt(COUNTRIES,4);const dis=distractors(_cpool,x=>x.sr===cor.subregion||x.ct===cor.continent,x=>x.c===cor.country,x=>x.c);
  return{type:"park",prompt:t("q_park"),subj:cor.name,ans:cor.country,opts:sh([cor.country,...dis]),meta:cor.continent,lid:cor.name,cc:cor.cc};
}
function genUnescoQ(){
  const pool=_rfilt(UNESCO_SITES.filter(x=>x.name\!==S.lid),3);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const _cpool=_rfilt(COUNTRIES,4);const dis=distractors(_cpool,x=>x.sr===cor.subregion||x.ct===cor.continent,x=>x.c===cor.country,x=>x.c);
  return{type:"unesco",prompt:t("q_unesco"),subj:cor.name,ans:cor.country,opts:sh([cor.country,...dis]),meta:cor.continent,lid:cor.name,cc:cor.cc};
}
function genCitymarkQ(){
  const pool=_rfilt(CITY_LANDMARKS.filter(x=>x.name\!==S.lid),3);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.subregion===cor.subregion||x.continent===cor.continent,x=>x.city===cor.city,x=>x.city);
  return{type:"citymark",prompt:t("q_citymark"),subj:cor.name,ans:cor.city,opts:sh([cor.city,...dis]),meta:cor.country,lid:cor.name,cc:cor.cc};
}
function genSubwayQ(){
  const pool=_rfilt(SUBWAYS.filter(x=>x.city\!==S.lid),3);if(pool.length<3)return null;
  const t=Math.floor(rng()*2);
  const cor=pool[~~(rng()*pool.length)];
  const dis3=distractors(pool,x=>x.country===cor.country||x.cc===cor.cc,x=>x.city===cor.city,x=>t===0?x.km:x.lines,2);
  const ansVal=t===0?cor.km:cor.lines;
  const prompt=t===0?"Wie lang ist das U-Bahn-Netz in \u2026 (km)?":"Wie viele U-Bahn-Linien hat \u2026?";
  const suffix=t===0?" km":" Linien";
  return{type:"subway",prompt,subj:cor.city,ans:String(ansVal),opts:sh([String(ansVal),...dis3.map(String)]),meta:cor.country+" \u00b7 "+suffix.trim(),lid:cor.city,cc:cor.cc};
}
function genFlagselQ(){
  const pool=_rfilt(COUNTRIES.filter(x=>x.cc\!==S.lid),4);if(pool.length<4)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.sr===cor.sr||x.ct===cor.ct,x=>x.cc===cor.cc,x=>x.cc,3);
  return{type:"flagsel",prompt:t("q_flagsel"),subj:cor.c,ans:cor.cc,opts:sh([cor.cc,...dis]),meta:cor.ct,lid:cor.cc,cc:cor.cc};
}
function genRcapitalQ(){
  const pool=_rfilt(CAPITALS.filter(x=>x.country\!==S.lid),3);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.subregion===cor.subregion||x.continent===cor.continent,x=>x.capital===cor.capital,x=>x.capital);
  return{type:"rcapital",prompt:t("q_rcapital"),subj:cor.country,ans:cor.capital,opts:sh([cor.capital,...dis]),meta:cor.continent,lid:cor.country,cc:cor.cc};
}
function genRcityQ(){
  const pool=_rfilt(COUNTRIES.filter(x=>x.c\!==S.lid),3);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const cc2=CITIES.filter(c=>c.c===cor.c);if(\!cc2.length)return genRcityQ();
  const corCity=cc2[~~(rng()*cc2.length)];
  const _citpool=_rfilt(CITIES,4);const dis=distractors(_citpool,x=>x.sub===corCity.sub||x.cont===corCity.cont,x=>x.c===cor.c,x=>x.n);
  return{type:"rcity",prompt:t("q_rcity"),subj:cor.c,ans:corCity.n,opts:sh([corCity.n,...dis]),meta:cor.ct,lid:cor.c,cc:cor.cc};
}
function genRriverQ(){
  const _rpool=_rfilt(RIVERS,3);
  const ctries=[...new Set(_rpool.map(r=>r.country))].filter(c=>c\!==S.lid);if(\!ctries.length)return null;
  const corC=ctries[~~(rng()*ctries.length)];
  const cRivers=_rpool.filter(r=>r.country===corC);
  const cor=cRivers[~~(rng()*cRivers.length)];
  const dis=distractors(_rpool,x=>x.subregion===cor.subregion||x.continent===cor.continent,x=>x.country===corC,x=>x.name);
  return{type:"rriver",prompt:t("q_rriver"),subj:corC,ans:cor.name,opts:sh([cor.name,...dis]),meta:cor.continent,lid:corC,cc:cor.cc};
}
function genFoodQ(){
  if(\!FOOD_DATA.length)return null;
  const _fp=_rfilt(FOOD_DATA,3);const item=_fp[~~(rng()*_fp.length)];
  const corC=item.country;
  const _fDisR=[...new Set(_fp.filter(f=>f.country\!==corC).map(f=>f.country))];
  const _fDisAll=[...new Set(FOOD_DATA.filter(f=>f.country\!==corC).map(f=>f.country))];
  const picked=sh(_fDisR.length>=3?_fDisR:_fDisAll).slice(0,3);
  return{type:"food",prompt:t("q_food"),subj:item.dish,emoji:item.emoji,ans:corC,opts:sh([corC,...picked]),lid:item.cc,cc:item.cc};
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
  return{type:"brand",prompt:t("q_brand"),subj:item.brand,industry:item.industry,ans:corC,opts:sh([corC,...picked]),lid:item.cc,cc:item.cc};
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
  return{type:"currency",prompt:t("q_currency"),subj:item.currency,symbol:item.symbol,ans:corC,opts:sh([corC,...picked]),lid:item.cc,cc:item.cc};
}
function genOutlineQ(){
  const pool=_rfilt(COUNTRIES.filter(c=>c.cc&&c.cc.length===2),4);
  if(pool.length<4)return null;
  const sh2=arr=>{const a=[...arr];for(let i=a.length-1;i>0;i--){const j=~~(rng()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
  const idx=~~(rng()*pool.length);const item=pool[idx];
  const corC=item.c;const corCC=item.cc;
  const dis=pool.filter(c=>c.cc\!==corCC).map(c=>c.c);
  const picked=sh2(dis).slice(0,3);
  return{type:"outline",prompt:t("q_outline"),subj:corCC,ans:corC,opts:sh2([corC,...picked]),lid:corCC,cc:corCC};
}
/* EU-KENNZEICHEN GENERATORS (Phase 23B) â€” smart same-country distractors */
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
const MAP_COUNTRIES=[{"cc":"fj","name":"Fiji"},{"cc":"tz","name":"Tanzania"},{"cc":"ca","name":"Canada"},{"cc":"us","name":"United States of America"},{"cc":"kz","name":"Kazakhstan"},{"cc":"uz","name":"Uzbekistan"},{"cc":"pg","name":"Papua New Guinea"},{"cc":"id","name":"Indonesia"},{"cc":"ar","name":"Argentina"},{"cc":"cl","name":"Chile"},{"cc":"cd","name":"Dem. Rep. Congo"},{"cc":"so","name":"Somalia"},{"cc":"ke","name":"Kenya"},{"cc":"sd","name":"Sudan"},{"cc":"td","name":"Chad"},{"cc":"ht","name":"Haiti"},{"cc":"do","name":"Dominican Rep."},{"cc":"ru","name":"Russia"},{"cc":"bs","name":"Bahamas"},{"cc":"no","name":"Norway"},{"cc":"za","name":"South Africa"},{"cc":"ls","name":"Lesotho"},{"cc":"mx","name":"Mexico"},{"cc":"uy","name":"Uruguay"},{"cc":"br","name":"Brazil"},{"cc":"bo","name":"Bolivia"},{"cc":"pe","name":"Peru"},{"cc":"co","name":"Colombia"},{"cc":"pa","name":"Panama"},{"cc":"cr","name":"Costa Rica"},{"cc":"ni","name":"Nicaragua"},{"cc":"hn","name":"Honduras"},{"cc":"sv","name":"El Salvador"},{"cc":"gt","name":"Guatemala"},{"cc":"bz","name":"Belize"},{"cc":"ve","name":"Venezuela"},{"cc":"gy","name":"Guyana"},{"cc":"sr","name":"Suriname"},{"cc":"fr","name":"France"},{"cc":"ec","name":"Ecuador"},{"cc":"jm","name":"Jamaica"},{"cc":"cu","name":"Cuba"},{"cc":"zw","name":"Zimbabwe"},{"cc":"bw","name":"Botswana"},{"cc":"na","name":"Namibia"},{"cc":"sn","name":"Senegal"},{"cc":"ml","name":"Mali"},{"cc":"mr","name":"Mauritania"},{"cc":"bj","name":"Benin"},{"cc":"ne","name":"Niger"},{"cc":"ng","name":"Nigeria"},{"cc":"cm","name":"Cameroon"},{"cc":"tg","name":"Togo"},{"cc":"gh","name":"Ghana"},{"cc":"ci","name":"CÃ´te d'Ivoire"},{"cc":"gn","name":"Guinea"},{"cc":"gw","name":"Guinea-Bissau"},{"cc":"lr","name":"Liberia"},{"cc":"sl","name":"Sierra Leone"},{"cc":"bf","name":"Burkina Faso"},{"cc":"cf","name":"Central African Rep."},{"cc":"cg","name":"Congo"},{"cc":"ga","name":"Gabon"},{"cc":"gq","name":"Eq. Guinea"},{"cc":"zm","name":"Zambia"},{"cc":"mw","name":"Malawi"},{"cc":"mz","name":"Mozambique"},{"cc":"sz","name":"eSwatini"},{"cc":"ao","name":"Angola"},{"cc":"bi","name":"Burundi"},{"cc":"il","name":"Israel"},{"cc":"lb","name":"Lebanon"},{"cc":"mg","name":"Madagascar"},{"cc":"ps","name":"Palestine"},{"cc":"gm","name":"Gambia"},{"cc":"tn","name":"Tunisia"},{"cc":"dz","name":"Algeria"},{"cc":"jo","name":"Jordan"},{"cc":"ae","name":"United Arab Emirates"},{"cc":"qa","name":"Qatar"},{"cc":"kw","name":"Kuwait"},{"cc":"iq","name":"Iraq"},{"cc":"om","name":"Oman"},{"cc":"vu","name":"Vanuatu"},{"cc":"kh","name":"Cambodia"},{"cc":"th","name":"Thailand"},{"cc":"la","name":"Laos"},{"cc":"mm","name":"Myanmar"},{"cc":"vn","name":"Vietnam"},{"cc":"kp","name":"North Korea"},{"cc":"kr","name":"South Korea"},{"cc":"mn","name":"Mongolia"},{"cc":"in","name":"India"},{"cc":"bd","name":"Bangladesh"},{"cc":"bt","name":"Bhutan"},{"cc":"np","name":"Nepal"},{"cc":"pk","name":"Pakistan"},{"cc":"af","name":"Afghanistan"},{"cc":"tj","name":"Tajikistan"},{"cc":"kg","name":"Kyrgyzstan"},{"cc":"tm","name":"Turkmenistan"},{"cc":"ir","name":"Iran"},{"cc":"sy","name":"Syria"},{"cc":"am","name":"Armenia"},{"cc":"se","name":"Sweden"},{"cc":"by","name":"Belarus"},{"cc":"ua","name":"Ukraine"},{"cc":"pl","name":"Poland"},{"cc":"at","name":"Austria"},{"cc":"hu","name":"Hungary"},{"cc":"md","name":"Moldova"},{"cc":"ro","name":"Romania"},{"cc":"lt","name":"Lithuania"},{"cc":"lv","name":"Latvia"},{"cc":"ee","name":"Estonia"},{"cc":"de","name":"Germany"},{"cc":"bg","name":"Bulgaria"},{"cc":"gr","name":"Greece"},{"cc":"tr","name":"Turkey"},{"cc":"al","name":"Albania"},{"cc":"hr","name":"Croatia"},{"cc":"ch","name":"Switzerland"},{"cc":"lu","name":"Luxembourg"},{"cc":"be","name":"Belgium"},{"cc":"nl","name":"Netherlands"},{"cc":"pt","name":"Portugal"},{"cc":"es","name":"Spain"},{"cc":"ie","name":"Ireland"},{"cc":"nz","name":"New Zealand"},{"cc":"au","name":"Australia"},{"cc":"lk","name":"Sri Lanka"},{"cc":"cn","name":"China"},{"cc":"tw","name":"Taiwan"},{"cc":"it","name":"Italy"},{"cc":"dk","name":"Denmark"},{"cc":"gb","name":"United Kingdom"},{"cc":"is","name":"Iceland"},{"cc":"az","name":"Azerbaijan"},{"cc":"ge","name":"Georgia"},{"cc":"ph","name":"Philippines"},{"cc":"my","name":"Malaysia"},{"cc":"bn","name":"Brunei"},{"cc":"si","name":"Slovenia"},{"cc":"fi","name":"Finland"},{"cc":"sk","name":"Slovakia"},{"cc":"cz","name":"Czechia"},{"cc":"er","name":"Eritrea"},{"cc":"jp","name":"Japan"},{"cc":"py","name":"Paraguay"},{"cc":"ye","name":"Yemen"},{"cc":"sa","name":"Saudi Arabia"},{"cc":"cy","name":"Cyprus"},{"cc":"ma","name":"Morocco"},{"cc":"eg","name":"Egypt"},{"cc":"ly","name":"Libya"},{"cc":"et","name":"Ethiopia"},{"cc":"dj","name":"Djibouti"},{"cc":"ug","name":"Uganda"},{"cc":"rw","name":"Rwanda"},{"cc":"ba","name":"Bosnia and Herz."},{"cc":"mk","name":"Macedonia"},{"cc":"rs","name":"Serbia"},{"cc":"me","name":"Montenegro"},{"cc":"tt","name":"Trinidad and Tobago"},{"cc":"ss","name":"S. Sudan"}];

function genMapGuessQ(){
  if(\!MAP_COUNTRIES.length)return null;
  const idx=~~(rng()*MAP_COUNTRIES.length);
  const co=MAP_COUNTRIES[idx];if(\!co)return null;
  return{type:"map_guess",prompt:t("q_map_guess"),subj:co.name,
    ans:co.name,opts:[],meta:"",lid:co.cc,cc:co.cc};
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
    prompt:"\u2708\uFE0F [BETA] Welcher Flughafen-Code geh\u00f6rt zu welcher Stadt?",
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
  return{type:"beta_timezone",
    prompt:"[BETA] \u23F0 Wenn es in "+cA+" 12:00 Uhr ist â€” wie sp\u00e4t ist es in "+cB+"?",
    subj:cA+" \u2192 "+cB,ans:correct,opts,meta:"",lid:cA,cc:null,cat:"geo"};
}
function genClimateQ(){
  const keys=Object.keys(_CLIMATE_CLUES);
  if(keys.length<4)return null;
  const ci=~~(rng()*keys.length);
  const correct=keys[ci];
  const clues=_CLIMATE_CLUES[correct];
  const dis=keys.filter(k=>k\!==correct).sort(()=>rng()-.5).slice(0,3);
  if(dis.length<3)return null;
  const opts=sh([correct,...dis]);
  const hint=clues.join(" \u00b7 ");
  return{type:"beta_climate",
    prompt:"[BETA] \U0001F321\uFE0F Klima-Krimi: "+hint,
    subj:"Welches Land?",ans:correct,opts,meta:"",lid:correct,
    cc:ccFromCountry(correct),cat:"geo"};
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
  return{type:"beta_flagcolor",
    prompt:"[BETA] \U0001F3F3\uFE0F Welche Farbe kommt auf der Flagge von "+displayCountry(country)+" NICHT vor?",
    subj:displayCountry(country),ans:correct,opts,meta:flagCols.join(", "),
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
  return{type:"beta_landlocked",
    prompt:"[BETA] \U0001F30A Welches dieser L\u00e4nder hat KEINEN Zugang zum Meer?",
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
    prompt:"\U0001F9ED Welches Land ist von Nord nach S\u00fcd l\u00e4nger?",
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
    prompt:"\U0001F3C5 Welches Land hat mehr Olympia-Gold (Sommer)?",
    subj:"",opts:[a,b],ans,meta,lid:a+"|"+b,cc:ccFromCountry(ans),cat:"stats"};
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
  comp_area:genCompAreaQ,comp_pop:genCompPopQ,comp_north:genCompNorthQ,
  comp_gdp:genCompGdpQ,comp_density:genCompDensityQ,comp_elevation:genCompElevQ,
  comp_coast:genCompCoastQ,comp_borders:genCompBordersQ,
  comp_life:genCompLifeQ,comp_age:genCompAgeQ,comp_forest:genCompForestQ,
  neighbor:genNeighborQ,
  map_guess:genMapGuessQ,
  logic_grid:()=>null,
  travel_route:()=>null,
  wappen_meister:genWappenQ,
  slf:()=>null,
  comp_airports:genAirportCompareQ,
  iata:genIataQ,
  beta_timezone:genTimezoneQ,
  beta_climate:genClimateQ,
  beta_flagcolor:genFlagColorQ,
  comp_flight:genFlightDistanceCompareQ,
  comp_mountain:genHighestPointCompareQ,
  beta_landlocked:genLandlockedQ,
  comp_nsextent:genNorthSouthCompareQ,
  comp_olympics:genOlympicCompareQ,
  /* P139: newly-activated new_modes entries wired to existing generators */
  climate_mystery:genClimateQ,
  flag_fusion:genFlagColorQ,
  timezone_jumper:genTimezoneQ,
};

/* GAME LOOP */
function clr(){clearInterval(tIv);clearTimeout(fTo);clearTimeout(S.freezeTimer);S.freezeTimer=null;}
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
function lq(){
  clearInterval(tIv);
  if(\!S.queueExtra)S.queueExtra=[];
  if(\!S.askedLids)S.askedLids=new Set();
  const dur=S.diff==="survival"?8:12;
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
  tIv=setInterval(()=>{S.tm--;if(S.tm===3)soundWarn();if(S.tm<=0){clearInterval(tIv);if(S.q)answer(null);}else render();},1000);
}

/* â”€â”€ Phase 42: Index-based answer dispatch (hides answer strings from DOM) â”€â”€ */
function answerByIdx(i){
  if(!S.q||!S.q.opts||i<0||i>=S.q.opts.length)return;
  answer(S.q.opts[i]);
}
document.addEventListener("keydown",function(e){
  if(S.ph==="playing"&&S.q&&S.sel===null&&!["INPUT","TEXTAREA","SELECT"].includes(document.activeElement?.tagName)){
    const k=parseInt(e.key);
    if(k>=1&&k<=4){e.preventDefault();answerByIdx(k-1);}
  }
});
function answer(a){
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
        showToast("â­ Neu: "+_code+" â€” "+_pc.region+(_allR.length>1?" +"+(_allR.length-1)+" weitere":"")+"!");
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
  const _fd=(_qt.startsWith("beta_")||_qt==="iata")?2800:1900;
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
'jp':{food:'Sushi',climate:'GemÃ¤ÃŸigt bis subtropisch',landmark:'Mount Fuji',region:'East Asia'},
'th':{food:'Pad Thai',climate:'Tropisch-feuchtes Klima',landmark:'Wat Arun',region:'Southeast Asia'},
'in':{food:'Curry',climate:'Tropisch-Monsun',landmark:'Taj Mahal',region:'South Asia'},
'id':{food:'Gado-Gado',climate:'Tropisches Regenwaldklima',landmark:'Borobudur-Tempel',region:'Southeast Asia'},
'vn':{food:'Pho',climate:'Tropisch',landmark:'Ha-Long-Bucht',region:'Southeast Asia'},
'cn':{food:'Peking-Ente',climate:'VielfÃ¤ltig (subtropisch bis gemÃ¤ÃŸigt)',landmark:'GroÃŸe Mauer',region:'East Asia'},
'kr':{food:'Kimchi',climate:'GemÃ¤ÃŸigt kontinental',landmark:'Gyeongbokgung-Palast',region:'East Asia'},
'tw':{food:'Xiaolongbao',climate:'Subtropisch',landmark:'Chiang Kai-shek Memorial',region:'East Asia'},
'it':{food:'Pasta & Pizza',climate:'Mittelmeerklima',landmark:'Kolosseum',region:'Southern Europe'},
'fr':{food:'Croissant & KÃ¤se',climate:'GemÃ¤ÃŸigt ozeanisch',landmark:'Eiffelturm',region:'Western Europe'},
'es':{food:'Paella',climate:'Mittelmeerklima',landmark:'Sagrada Familia',region:'Southern Europe'},
'de':{food:'Schnitzel & Brezel',climate:'GemÃ¤ÃŸigt kontinental',landmark:'Brandenburger Tor',region:'Central Europe'},
'gr':{food:'Souvlaki',climate:'Mittelmeerklima',landmark:'Parthenon',region:'Southern Europe'},
'ru':{food:'Borschtsch',climate:'Kontinental bis subarktisch',landmark:'Rotes Platz & Kreml',region:'Eastern Europe'},
'uk':{food:'Borschtsch & Pelmeni',climate:'GemÃ¤ÃŸigt kontinental',landmark:'Sophienkathedrale',region:'Eastern Europe'},
'pt':{food:'PastÃ©is de Nata',climate:'Mittelmeerklima',landmark:'Ponte Dom LuÃ­s I',region:'Western Europe'},
'se':{food:'KÃ¶ttbullar',climate:'Kalt-gemÃ¤ÃŸigt',landmark:'Vasamuseum',region:'Northern Europe'},
'no':{food:'Lachssuppe',climate:'Kalt-gemÃ¤ÃŸigt',landmark:'Geirangerfjord',region:'Northern Europe'},
'dk':{food:'SmÃ¸rrebrÃ¸d',climate:'Kalt-gemÃ¤ÃŸigt ozeanisch',landmark:'Schloss Kronborg',region:'Northern Europe'},
'us':{food:'Hamburger & BBQ',climate:'VielfÃ¤ltig',landmark:'Freiheitsstatue',region:'North America'},
'ca':{food:'Poutine',climate:'Kalt-gemÃ¤ÃŸigt',landmark:'NiagarafÃ¤lle',region:'North America'},
'mx':{food:'Tacos & Mole',climate:'Tropisch bis trocken',landmark:'Chichen Itza',region:'Central America'},
'br':{food:'Feijoada',climate:'Tropisch & subtropisch',landmark:'Cristo Redentor',region:'South America'},
'ar':{food:'Asado',climate:'GemÃ¤ÃŸigt',landmark:'Teatro Colon',region:'South America'},
'pe':{food:'Ceviche',climate:'VielfÃ¤ltig (trocken bis tropisch)',landmark:'Machu Picchu',region:'South America'},
'cl':{food:'Empanadas',climate:'Mediterranisch bis kalt-gemÃ¤ÃŸigt',landmark:'Torres del Paine',region:'South America'},
'eg':{food:'Koshari',climate:'WÃ¼ste',landmark:'GroÃŸe Pyramide von Giza',region:'Africa'},
'za':{food:'Braai & Biltong',climate:'GemÃ¤ÃŸigt bis semi-arid',landmark:'KrÃ¼ger-Nationalpark',region:'Africa'},
'ng':{food:'Jollof Rice',climate:'Tropisch-Monsun',landmark:'Lekki Conservation Centre',region:'Africa'},
'sa':{food:'Shawarma',climate:'WÃ¼ste & heiÃŸ-trocken',landmark:'Kaaba in Mekka',region:'Middle East'},
'ae':{food:'Hummus & Falafel',climate:'WÃ¼ste & heiÃŸes KÃ¼stenklima',landmark:'Burj Khalifa',region:'Middle East'},
'il':{food:'Hummus & Falafel',climate:'Mittelmeer & WÃ¼ste',landmark:'Totes Meer',region:'Middle East'},
'au':{food:'Lamingtons',climate:'VielfÃ¤ltig (arid bis tropisch)',landmark:'Uluru',region:'Oceania'},
'nz':{food:'Pavlova',climate:'GemÃ¤ÃŸigt ozeanisch',landmark:'Milford Sound',region:'Oceania'},
'pl':{food:'Pierogi',climate:'GemÃ¤ÃŸigt kontinental',landmark:'Marienkirche Danzig',region:'Eastern Europe'},
'cz':{food:'Goulash',climate:'GemÃ¤ÃŸigt kontinental',landmark:'KarlsbrÃ¼cke Prag',region:'Central Europe'},
'nl':{food:'Stroopwafels',climate:'GemÃ¤ÃŸigt ozeanisch',landmark:'WindmÃ¼hlen von Kinderdijk',region:'Western Europe'},
'be':{food:'Frites & Waffeln',climate:'GemÃ¤ÃŸigt ozeanisch',landmark:'Grote Markt BrÃ¼ssel',region:'Western Europe'},
'at':{food:'Wiener Schnitzel',climate:'GemÃ¤ÃŸigt kontinental',landmark:'Schloss SchÃ¶nbrunn',region:'Central Europe'},
'ch':{food:'Fondue & Raclette',climate:'GemÃ¤ÃŸigt mit alpinem Einfluss',landmark:'Matterhorn',region:'Central Europe'},
'hu':{food:'GulyÃ¡sleves',climate:'GemÃ¤ÃŸigt kontinental',landmark:'ParlamentsgebÃ¤ude Budapest',region:'Eastern Europe'},
'se':{food:'KÃ¶ttbullar & Gravlax',climate:'Kalt-gemÃ¤ÃŸigt',landmark:'Stockholms Schloss',region:'Northern Europe'},
'tr':{food:'Kebab & DÃ¶ner',climate:'Mittelmeer & kontinental',landmark:'Blaue Moschee Istanbul',region:'Middle East'},
'th':{food:'Green Curry',climate:'Tropisch-monsun',landmark:'Wat Phra Kaew',region:'Southeast Asia'},
'my':{food:'Satay',climate:'Tropisch-feuchtes Regenwaldklima',landmark:'Petronas Towers',region:'Southeast Asia'},
'sg':{food:'Laksa',climate:'Tropisch-feuchtes Klima',landmark:'Merlion',region:'Southeast Asia'},
'ph':{food:'Adobo',climate:'Tropisch',landmark:'Reisterrassen von Banaue',region:'Southeast Asia'},
'ie':{food:'Irish Stew',climate:'Kalt-gemÃ¤ÃŸigt ozeanisch',landmark:'Cliffs of Moher',region:'Western Europe'},
'nz':{food:'Lamingtons',climate:'GemÃ¤ÃŸigt ozeanisch',landmark:'Franz Josef Glacier',region:'Oceania'}
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
if(metric==='borders')return val+' LÃ¤nder';
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
if(lower.includes('wÃ¼ste')||lower.includes('desert'))keywords.push('desert');
if(lower.includes('gemÃ¤ÃŸigt')||lower.includes('temperate'))keywords.push('temperate');
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
if(correct.a>others[2].a)constraints.push(correct.country+' ist grÃ¶ÃŸer als '+others[2].country);
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
html+='<p style="color:#666;">Welches Land erfÃ¼llt alle Bedingungen?</p>';
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
const route1={desc:(city1.name||city1.n||'City')+' â†’ '+(city2.name||city2.n||'City'),dist:dist1_2,correct:true};
const route2={desc:(city1.name||city1.n||'City')+' â†’ '+(city3.name||city3.n||'City'),dist:dist1_3,correct:false};
const route3={desc:(city1.name||city1.n||'City')+' â†’ '+(city4.name||city4.n||'City'),dist:dist1_4,correct:false};

const routes=[route1,route2,route3].sort(()=>Math.random()-0.5);
const correctIdx=routes.findIndex(r=>r.correct);

setCorrectAnswerObfuscated(COUNTRIES,correctIdx,correctIdx);

let html='<div style="padding:20px;text-align:center;">';
html+='<h2>Reiseroute-Quiz</h2>';
html+='<p>Welche Route ist kÃ¼rzer?</p>';
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
html+='<div style="opacity:0.7;font-size:60px;">ðŸ‡¹ðŸ‡·</div>';
html+='<div style="font-size:40px;color:#ccc;">+</div>';
html+='<div style="opacity:0.7;font-size:60px;">ðŸ‡¸ðŸ‡ª</div>';
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

function startGame(m){
  clr();
  const survBest=parseInt(localStorage.getItem('gq_surv_best')||'0');
  const _m=m||S.mode;
  Object.assign(S,{sc:0,st:0,bs:0,rd:0,correct:0,lid:null,ph:"playing",mode:_m,
    scoreSaved:false,convModal:false,sessionAnswers:[],newStamps:[],isDailyRun:false,challengeStarted:false,
    half_removed:false,freezeActive:false,queueExtra:[],askedLids:new Set(),
    survivalBest:survBest,gameStartTime:Date.now(),hcMult:1.0,hcMaxMult:1.0,survTimeBonusTotal:0,lives:S.diff==="casual"?999:3});
  /* Phase 86 â€” custom puzzle modes */
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
  const cn=COUNTRIES.find(c=>c.cc===cc)?.c||cc.toUpperCase();
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
/* Phase 60: Ad hook â€” swap in real adsbygoogle.push({}) when AdSense is live */
/* Phase 151: flip to true when AdSense is approved and banners are configured */
const ENABLE_ADS=false;
function loadAd(){
  if(!ENABLE_ADS)return; /* P151: ads off */
  /* adsbygoogle.push({}); */
}
/* Phase 61: Viral share â€” Web Share API with clipboard fallback */
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
  const cn=COUNTRIES.find(c=>c.cc===cc)?.c||cc.toUpperCase();
  return `<div class="stamp-cell" onclick="S.modal='${cc}';render()" title="${cn}"><div class="stamp-ink ${rank}" style="transform:rotate(${rot}deg)"><img class="stamp-flag" src="https://flagcdn.com/w40/${cc}.png" alt="${cn}" onerror="this.style.display='none'"><span>${cc.toUpperCase()}</span></div></div>`;
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
      console.warn("GeoQuest: IntegritÃ¤tsfehler fÃ¼r",key,"â€” Daten zurÃ¼ckgesetzt");
      localStorage.removeItem(key);
      return fallback;
    }
    return w.d;
  }catch(e){return fallback;}
}

function _smartDefaultCountry(){
  /* Priority: new unified pref â†’ old spotter key â†’ navigator.language â†’ fallback */
  const saved=localStorage.getItem("geoquest_pref_country")||localStorage.getItem("gq_spotter_country");
  if(saved&&saved!=="all")return saved;
  const lang=(navigator.language||"de-DE").toLowerCase();
  const langMap={
    "de-de":"Deutschland","de-at":"Ã–sterreich","de-ch":"Schweiz","de-li":"Liechtenstein",
    "fr-fr":"Frankreich","fr-be":"Belgien","fr-ch":"Schweiz","fr-lu":"Luxemburg",
    "nl-nl":"Niederlande","nl-be":"Belgien",
    "pl-pl":"Polen","it-it":"Italien","es-es":"Spanien","pt-pt":"Portugal",
    "cs-cz":"Tschechien","sk-sk":"Slowakei","hu-hu":"Ungarn","ro-ro":"RumÃ¤nien",
    "bg-bg":"Bulgarien","hr-hr":"Kroatien","sl-si":"Slowenien",
    "et-ee":"Estland","lv-lv":"Lettland","lt-lt":"Litauen",
    "fi-fi":"Finnland","sv-se":"Schweden","nb-no":"Norwegen","da-dk":"DÃ¤nemark",
    "el-gr":"Griechenland","tr-tr":"TÃ¼rkei"
  };
  if(langMap[lang])return langMap[lang];
  /* Try just the language prefix (e.g. "de" for de-DE) */
  const prefix=lang.split("-")[0];
  const prefixMap={
    "de":"Deutschland","fr":"Frankreich","nl":"Niederlande","pl":"Polen",
    "it":"Italien","es":"Spanien","pt":"Portugal","cs":"Tschechien",
    "sk":"Slowakei","hu":"Ungarn","ro":"RumÃ¤nien","bg":"Bulgarien",
    "hr":"Kroatien","sl":"Slowenien","et":"Estland","lv":"Lettland",
    "lt":"Litauen","fi":"Finnland","sv":"Schweden","nb":"Norwegen","da":"DÃ¤nemark",
    "el":"Griechenland","tr":"TÃ¼rkei"
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
  /* Phase 93: Dual-Save â€” Kennzeichen auch in Supabase sichern */
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

/* RENDER â€” main dispatcher */
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
  console.log("[GQ] evaluateWeeklyLeague: Starte fÃ¼r Woche",getISOWeek(new Date()));
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

const _MAP_MODES_SET=new Set(["map_guess"]);
function updateOrientationWarning(){
  const ow=document.getElementById("gq-orient-warn");
  if(\!ow)return;
  const isPortrait=window.matchMedia("(orientation:portrait)").matches;
  const isMapMode=_MAP_MODES_SET.has(S.mode)&&S.ph==="playing";
  ow.style.display=(isPortrait&&isMapMode)?"flex":"none";
  const txt=ow.querySelector(".gq-ow-txt");if(txt)txt.textContent=t("rotate_device");
}
function render(){
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
    const cn=COUNTRIES.find(c=>c.cc===S.modal)?.c||S.modal.toUpperCase();
    const rl={gold:"\u{1F947} Gold",silver:"\u{1F948} Silber",bronze:"\u{1F949} Bronze"}[rank]||"Gesperrt";
    const rc={gold:"#d97706",silver:"#94a3b8",bronze:"#c2410c"}[rank]||"var(--text3)";
    app.innerHTML=`<div class="modal-overlay" onclick="if(event.target===this){S.modal=null;render()}"><div class="modal-box">
      <img src="https://flagcdn.com/w80/${S.modal}.png" style="height:44px;width:auto;border-radius:4px;margin-bottom:.75rem" onerror="this.style.display='none'">
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
      ${S.settingsModal?renderSettingsModal():""}${S.adModal?renderAdModal():""}
    </div>${renderBottomNav()}`;
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
      const cn=COUNTRIES.find(c=>c.cc===cc)?.c||cc.toUpperCase();
      const rl={gold:"\u{1F947} Gold-Stempel",silver:"\u{1F948} Silber-Stempel",bronze:"\u{1F949} Bronze-Stempel"}[rank]||"Stempel";
      return`<div class="new-stamp-banner"><img src="https://flagcdn.com/w40/${cc}.png" style="width:28px;height:auto;border-radius:3px" onerror="this.style.display='none'"><div><div style="color:#34d399;font-weight:900;font-size:.88rem">NEUER STEMPEL\!</div><div style="color:var(--text2);font-size:.78rem">${rl} \u2022 ${cn}</div></div></div>`;
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
        ${S.diff==="hardcore"?`<div style="background:var(--bg3);border-radius:10px;padding:.55rem .75rem;margin-bottom:.6rem;text-align:center;font-size:.78rem;color:var(--text2)">âš¡ ${t("score_mult_max")}: <strong style="color:#f59e0b">${(S.hcMaxMult||1).toFixed(1)}Ã—</strong></div>`:S.diff==="survival"?`<div style="background:var(--bg3);border-radius:10px;padding:.55rem .75rem;margin-bottom:.6rem;text-align:center;font-size:.78rem;color:var(--text2)">â± ${t("score_time_bonus")}: <strong style="color:#34d399">+${S.survTimeBonusTotal||0} ${t("pts_abbr")}</strong></div>`:`<div style="background:var(--bg3);border-radius:10px;padding:.55rem .75rem;margin-bottom:.6rem;text-align:center;font-size:.78rem;color:var(--text2)">ðŸ“‹ ${S.correct}/${ROUNDS} ${t("score_correct_lbl")} Ã— 10 ${t("pts_abbr")} = <strong style="color:#60a5fa">${S.sc} ${t("pts_abbr")}</strong></div>`}
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
  const{sc,st,bs,rd,tm,q,sel,ok,pts,mode,diff}=S;
  /* Phase 86 â€” custom puzzle modes */
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
    app.innerHTML=renderStadtLandFluss(sc);
    requestAnimationFrame(()=>{document.getElementById("slf-city")?.focus();});
    return;
  }
  if(!q){S.ph="menu";S.q=null;render();return;}  /* guard: q not yet set */
  const col=tc(),p=pct(),_tr=tier(st);
  let qBody="";
  if(q.type==="flag"){
    qBody=`<div class="qprompt">${q.prompt}</div><div class="qflag"><img src="https://flagcdn.com/w80/${q.subj}.png" alt="Flagge" onerror="this.style.display='none'"></div>${sel!==null?`<div class="qmeta">${q.meta||""}</div>`:""}`;
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
        <button class="hl-btn hl-higher${sel\!==null?(q.ans==="higher"?" ok":(sel==="higher"?" ng":" dm")):""}" ${hlDis} onclick="answer('higher')">${hlBtnH}</button>
        <button class="hl-btn hl-lower${sel\!==null?(q.ans==="lower"?" ok":(sel==="lower"?" ng":" dm")):""}" ${hlDis} onclick="answer('lower')">${hlBtnL}</button>
      </div>`;
  }else if(q.type&&q.type.startsWith('comp_')){
    /* Phase 102-A: Flaggen-Header + Prompt, Werte nach Antwort */
    const _cfA=q.opts&&q.opts[0]?flagOf(q.opts[0]):'\u{1F30D}';
    const _cfB=q.opts&&q.opts[1]?flagOf(q.opts[1]):'\u{1F30D}';
    /* P136: show country names below flags */
    const _cnA=q.opts&&q.opts[0]?displayCountry(q.opts[0]):"";
    const _cnB=q.opts&&q.opts[1]?displayCountry(q.opts[1]):"";
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
    qBody=`<div class="qprompt">${q.prompt}</div><div class="wappen-img-wrap"><img src="${q.img}" alt="Wappen" class="wappen-img" onerror="this.style.opacity='.25'"></div>${sel!==null?`<div class="qmeta">${q.meta||""}</div>`:""}`;
  }else if(q.type==="neighbor"){
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
  /* Phase 34: Map-Guesser â€” early return, D3 map replaces answer buttons */
  if(q.type==="map_guess"){
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
          <button class="btn-cancel" onclick="clr();S.ph='menu';S.tab='home';render()">\u00d7</button>
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
  /* topBar: shared HUD wrapper used by pop_compare early-return */
  const topBar=`<div class="scr"><div class="hud"><div style="display:flex;gap:8px;align-items:center"><div class="pill"><div class="hlbl">SCORE</div><div class="hval">${sc.toLocaleString()}</div></div>${st>0?`<div class="pill-s"><div class="hlbl" style="color:#fb923c">STREAK</div><div class="hval-s">Ã—${st}</div></div>`:""}${(diff==="hardcore"||diff==="survival")?`<div class="pill-s" style="background:rgba(239,68,68,.15)"><div class="hlbl" style="color:#ef4444">${t("hud_lives")}</div><div class="hval-s" style="color:#ef4444">${S.lives||3}</div></div>`:""}</div><div style="display:flex;align-items:center;gap:8px">${diff==="survival"?`<div style="text-align:right"><div class="hlbl" style="color:#ef4444">ðŸ’€ SURVIVAL</div><div style="color:var(--text);font-weight:700;font-size:.9rem">${rd+1}<span style="color:var(--text3)">âˆž</span></div></div>`:`<div style="text-align:right"><div class="hlbl" style="color:var(--text3)">RUNDE</div><div style="color:var(--text);font-weight:700;font-size:.9rem">${rd+1}<span style="color:var(--text3)">/${ROUNDS}</span></div></div>`}<button class="btn-cancel" onclick="clr();S.ph='menu';S.tab='home';render()">Ã—</button></div></div><div class="tbar${S.freezeActive?" frozen":""}"><div class="tfill" style="width:${p}%;background:${col}"></div></div>`;
  let answerHtml="";
  if(q.type==="flagsel"){
    const fb2=q.opts.map(cc=>{let cls="btn-flag";if(sel\!==null){if(cc===q.ans)cls+=" ok";else if(cc===sel)cls+=" ng";else cls+=" dm";}const flagEmoji=cc.toUpperCase().replace(/./g,c=>String.fromCodePoint(c.charCodeAt(0)+127397));return '<button class="'+cls+'" onclick="sel=\''+cc+'\';render()" data-quiz-answer="'+q.opts.indexOf(cc)+'"><img src="https://flagcdn.com/w120/'+cc.toLowerCase()+'.png" style="height:50px;border-radius:8px;" onerror="this.replaceWith(\''+flagEmoji+'\')"></button>';}).join('');
    answerHtml=`<div class="flag-grid">${fb2}</div>`;
  }else{
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
          <button class="${moreCls}" ${pcDis} onclick="answer('more')">${t("hl_more")}</button>
          <button class="${lessCls}" ${pcDis} onclick="answer('less')">${t("hl_less")}</button>
        </div>
        ${sel\!==null?`<div class="meta-line">${q.meta||""}</div>`:""}
        ${sel\!==null?`<button class="btn-p" onclick="nextRound()">Weiter â†’</button>`:""}
      </div>`;
      app.innerHTML=pcHtml;return;
    }
    if(q.type==="hl_pop"||q.type==="hl_river"||q.type==="hl_area"){
      answerHtml="";
    }else{
      const btns=q.opts.map((o,i)=>{let cls="btn-a";const os=o.replace(/'/g,"\'");if(sel\!==null){if(o===q.ans)cls+=" ok";else if(o===sel)cls+=" ng";else cls+=" dm";}const mk=sel?(o===q.ans?`<span>\u2713</span>`:o===sel?`<span>\u2717</span>`:""):"";return`<button class="${cls}" ${sel?"disabled":""} onclick="answerByIdx(${i})">${esc(displayCountry(o))}${mk}</button>`;}).join("");
      const _twoOpts=q.opts&&q.opts.length===2?' two-opts':'';
      answerHtml=`<div class="answers${_twoOpts}">${btns}</div>`;
    }
  }
  let fb="";
  if(S.ph==="feedback"){const cls=ok?"fb ok":"fb ng";let al=q.ans;if(q.type==="flagsel"){const co=COUNTRIES.find(c=>c.cc===q.ans);al=co?co.c:q.ans;}const al_d=displayCountry(al);const msg=ok?t("fb_correct",{pts}):sel==="__t"?t("fb_time",{ans:al_d}):t("fb_wrong",{ans:al_d});fb=`<div class="${cls}">${msg}</div>${plateReveal}`;}
  /* Power-up bar (Phase 26) */
  const pu=loadPU();
  /* P136-fix: 50/50 disabled for comp_ modes -- pre-declared vars, no nested escaping */
  const _is2ans=S.q&&S.q.type&&S.q.type.startsWith('comp_');
  const _j5title=_is2ans?'Kein 50/50 (nur 2 Optionen)':'50/50-Joker ('+(pu.five0||0)+' \u00fcbrig)';
  const _j5label=_is2ans?'â€”':'('+(pu.five0||0)+')';
  const _j5sty=_is2ans?'opacity:.35;pointer-events:none':'';
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
        <button class="btn-cancel" onclick="clr();S.ph='menu';S.tab='home';render()">\u00d7</button>
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


/* Phase 34 â€” D3 World Map component */
function drawWorldMap(targetName,sel,ok){
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
    .style('background','var(--bg2)');

  const proj=d3.geoNaturalEarth1().scale(W/6.2).translate([W/2,H/2]);
  const path=d3.geoPath().projection(proj);
  const countries=topojson.feature(window.WORLD_TOPO,window.WORLD_TOPO.objects.countries);

  const g=svg.append('g');

  /* Zoom + pan */
  const zoom=d3.zoom().scaleExtent([1,10])
    .on('zoom',ev=>{
      if(sel\!==null)return; /* lock zoom during feedback so user sees the result */
      g.attr('transform',ev.transform);
    });
  svg.call(zoom);

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
      return'var(--bg3,#e2e8f0)';
    })
    .attr('stroke','var(--border,#94a3b8)')
    .attr('stroke-width',.35)
    .on('mouseover',function(_,d){
      if(sel\!==null)return;
      d3.select(this).attr('fill','#93c5fd');
    })
    .on('mouseout',function(_,d){
      if(sel\!==null)return;
      d3.select(this).attr('fill','var(--bg3,#e2e8f0)');
    })
    .on('click',function(ev,d){
      if(sel\!==null)return;
      ev.stopPropagation();
      answer(d.properties.name);
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
  ];
  return`<nav class="bottom-nav">${tabs.map(t=>`<button class="bn-item${S.tab===t.id?" active":""}" onclick="S.tab='${t.id}';render()"><span class="bn-icon">${t.icon}</span><span class="bn-lbl">${t.lbl}</span></button>`).join("")}</nav>`;
}


/* â”€â”€â”€ Phase 43: Kennzeichen-Album â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */

/* Country name â†’ English for world-110m matching */
const PLATE_COUNTRY_EN={
  "Deutschland":"Germany","Ã–sterreich":"Austria","Frankreich":"France",
  "Italien":"Italy","Spanien":"Spain","Polen":"Poland","Tschechien":"Czechia",
  "Ungarn":"Hungary","Schweiz":"Switzerland","Belgien":"Belgium",
  "Niederlande":"Netherlands","DÃ¤nemark":"Denmark","Schweden":"Sweden",
  "Norwegen":"Norway","Finnland":"Finland","Portugal":"Portugal",
  "Griechenland":"Greece","RumÃ¤nien":"Romania","Bulgarien":"Bulgaria",
  "Kroatien":"Croatia","Slowenien":"Slovenia","Slowakei":"Slovakia",
  "Luxemburg":"Luxembourg","Irland":"Ireland","Litauen":"Lithuania",
  "Lettland":"Latvia","Estland":"Estonia","Zypern":"Cyprus","Malta":"Malta",
  "Vereinigtes KÃ¶nigreich":"United Kingdom","Russland":"Russia",
  "TÃ¼rkei":"Turkey","Ukraine":"Ukraine","Serbien":"Serbia",
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

/* Migrate old plain-code format â†’ code::country */
function migrateCollectedPlates(){
  if(\!PLATES_DATA.length)return;
  let changed=false;
  S.collectedPlates=S.collectedPlates.map(entry=>{
    if(entry.includes("::"))return entry; /* already new format */
    const code=entry.toUpperCase();
    const matches=[...new Set(PLATES_DATA.filter(p=>p.code===code).map(p=>p.country))];
    if(matches.length===1){changed=true;return collKey(code,matches[0]);}
    if(matches.length>1){changed=true;return collKey(code,matches[0]);} /* take first if ambiguous */
    return null; /* unknown code â€” discard */
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
  /* Returns [{code, mainRegion, extraCount}] â€” one entry per unique code */
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
  /* Phase 104: Fuzzy-Lookup â€” normalisiere zuerst (0â†’O, 1â†’I) */
  const _norm=s=>s.replace(/0/g,'O').replace(/1/g,'I').replace(/Ãœ/g,'UE').replace(/Ã–/g,'OE').replace(/Ã„/g,'AE');
  const codeNorm=_norm(code);
  /* Find matching plates: exact â†’ normalisiert â†’ prefix */
  const _match=(c,p)=>p.code===c&&(country===null||p.country===country);
  let candidates=PLATES_DATA.filter(p=>_match(code,p));
  /* Fallback 1: Normalisierung (0â†”O, Umlaute) */
  if(\!candidates.length&&codeNorm\!==code){
    candidates=PLATES_DATA.filter(p=>_match(codeNorm,p));
    if(candidates.length)S.spotterInput=codeNorm;
  }
  /* Fallback 2: Prefix-Match (min 2 Zeichen) â€” zeige VorschlÃ¤ge */
  let prefixSuggestions=[];
  if(\!candidates.length&&code.length>=2){
    prefixSuggestions=[...new Set(
      PLATES_DATA.filter(p=>(country===null||p.country===country)&&p.code.startsWith(code)&&p.code\!==code)
        .map(p=>p.code).slice(0,8)
    )];
  }
  if(\!candidates.length){
    /* Phase 105b: TYPE_COUNTRY â€” LÃ¤nder ohne Regionen */
    if(country){
      const _cEnt=PLATES_DATA.filter(p=>p.country===country);
      if(_cEnt.length===1&&_cEnt[0].region==='Nationales Kennzeichen'){
        S.spotterMsg="â„¹ï¸ "+displayCountry(country)+" "+t("spotter_no_region",{code:_cEnt[0].code});
        S.spotterOk=false;render();return;
      }
    }
    /* Check if code exists in other countries */
    const elsewhere=PLATES_DATA.filter(p=>p.code===code||p.code===codeNorm);
    if(elsewhere.length){
      const others=[...new Set(elsewhere.map(p=>p.country))].join(", ");
      S.spotterMsg="â“ '"+esc(code)+"' "+t("spotter_not_in")+" "+(country?displayCountry(country):t("spotter_all"))+" â€” "+t("spotter_but_in")+": "+esc(others);
    }else if(prefixSuggestions.length){
      S.spotterMsg="ðŸ” Meintest du: "+prefixSuggestions.join(", ")+"?";
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
    S.spotterMsg="\u{1F389} "+code+(mainPlate.region?" â€” "+esc(mainPlate.region):"")+(" ("+esc(displayCountry(mainCountry))+")")+(extras?" +"+extras+" weitere":"")+"\!";
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
  if(\!PLATES_DATA.length)return`<div class="panel" style="text-align:center;padding:2rem"><div style="font-size:2rem">â³</div><p style="color:var(--text3);margin-top:.5rem">Kennzeichen-Daten werden geladenâ€¦</p></div>`;
  /* Run migration once per session */
  if(\!window._platesMigrated){window._platesMigrated=true;migrateCollectedPlates();}

  const coll=S.collectedPlates;
  const total=totalUniquePlates();
  const pct=Math.round(coll.length/Math.max(total,1)*100);
  const countries=[...new Set(PLATES_DATA.map(p=>p.country))].sort();
  const view=S.albumView||"list";
  /* P126: reset legacy "all" state â€” spotter dropdown no longer has "all" */
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
    'Niederlande':{ph:'NL',info:'Kein Regionalk\u00fcrzel â€” Oval-Code "NL" eingeben',tp:'nat',ex:'NL',lbl:'NL = Niederlande',cc:'NL',nums:''},
    'Belgien':{ph:'B',info:'Kein Regionalk\u00fcrzel â€” Oval-Code "B" eingeben',tp:'nat',ex:'B',lbl:'B = Belgien',cc:'B',nums:''},
    'D\u00e4nemark':{ph:'DK',info:'Kein Regionalk\u00fcrzel â€” Oval-Code "DK" eingeben',tp:'nat',ex:'DK',lbl:'DK = D\u00e4nemark',cc:'DK',nums:''},
    'Schweden':{ph:'S',info:'Kein Regionalk\u00fcrzel â€” Oval-Code "S" eingeben',tp:'nat',ex:'S',lbl:'S = Schweden',cc:'S',nums:''},
    'Norwegen':{ph:'N',info:'Kein Regionalk\u00fcrzel â€” Oval-Code "N" eingeben',tp:'nat',ex:'N',lbl:'N = Norwegen',cc:'N',nums:''},
    'Spanien':{ph:'E',info:'Kein Regionalk\u00fcrzel â€” Oval-Code "E" eingeben',tp:'nat',ex:'E',lbl:'E = Spanien',cc:'E',nums:''},
    'Portugal':{ph:'P',info:'Kein Regionalk\u00fcrzel â€” Oval-Code "P" eingeben',tp:'nat',ex:'P',lbl:'P = Portugal',cc:'P',nums:''},
    'Finnland':{ph:'FIN',info:'Kein Regionalk\u00fcrzel â€” Oval-Code "FIN" eingeben',tp:'nat',ex:'FIN',lbl:'FIN = Finnland',cc:'FIN',nums:''},
    'Irland':{ph:'IRL',info:'Kein Regionalk\u00fcrzel â€” Oval-Code "IRL" eingeben',tp:'nat',ex:'IRL',lbl:'IRL = Irland',cc:'IRL',nums:''},
    'Gro\u00dfbritannien':{ph:'GB',info:'Kein Regionalk\u00fcrzel â€” Oval-Code "GB" eingeben',tp:'nat',ex:'GB',lbl:'GB = Gro\u00dfbritannien',cc:'GB',nums:''},
    'Ungarn':{ph:'H',info:'Kein Regionalk\u00fcrzel â€” Oval-Code "H" eingeben',tp:'nat',ex:'H',lbl:'H = Ungarn',cc:'H',nums:''},
    'Slowakei':{ph:'SK',info:'Kein Regionalk\u00fcrzel â€” Oval-Code "SK" eingeben',tp:'nat',ex:'SK',lbl:'SK = Slowakei',cc:'SK',nums:''},
    'Tschechien':{ph:'CZ',info:'Kein Regionalk\u00fcrzel â€” Oval-Code "CZ" eingeben',tp:'nat',ex:'CZ',lbl:'CZ = Tschechien',cc:'CZ',nums:''},
    'Luxemburg':{ph:'L',info:'Kein Regionalk\u00fcrzel â€” Oval-Code "L" eingeben',tp:'nat',ex:'L',lbl:'L = Luxemburg',cc:'L',nums:''},
    'Litauen':{ph:'LT',info:'Kein Regionalk\u00fcrzel â€” Oval-Code "LT" eingeben',tp:'nat',ex:'LT',lbl:'LT = Litauen',cc:'LT',nums:''},
    'Lettland':{ph:'LV',info:'Kein Regionalk\u00fcrzel â€” Oval-Code "LV" eingeben',tp:'nat',ex:'LV',lbl:'LV = Lettland',cc:'LV',nums:''},
    'Estland':{ph:'EST',info:'Kein Regionalk\u00fcrzel â€” Oval-Code "EST" eingeben',tp:'nat',ex:'EST',lbl:'EST = Estland',cc:'EST',nums:''},
    'Ukraine':{ph:'UA',info:'Kein Regionalk\u00fcrzel â€” Oval-Code "UA" eingeben',tp:'nat',ex:'UA',lbl:'UA = Ukraine',cc:'UA',nums:''},
  };
  const r=M[c]||{ph:'K\u00fcrzel eingeben',info:'',tp:'de',ex:'AB',lbl:'Regionales K\u00fcrzel',cc:'EU',nums:'1234'};
  /* Phase 105b: NAT dynamic ph+info aus PLATES_DATA */
  if(r.tp==='nat'&&typeof PLATES_DATA!='undefined'&&PLATES_DATA.length){
    const _ne=PLATES_DATA.filter(p=>p.country===c);
    if(_ne.length===1){const _nc=_ne[0].code;
      r.ph='"'+_nc+'" eingeben';
      r.info='Keine Regionen â€” "'+_nc+'" eingeben, um das Land zu sammeln';
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
    /* DE / AT / IT / PL ... â€” EU stripe left, yellow box, number right */
    if(tp==='de')return wrap(euStripe+yBox+numsEl);
    /* CH â€” Swiss cross left (red/white), yellow box, number right */
    if(tp==='ch'){
      const chCross='<rect x="2" y="5" width="16" height="28" rx="3" fill="#D00"/>'
        +'<rect x="7" y="8" width="6" height="22" rx="1" fill="white"/>'
        +'<rect x="3" y="16" width="14" height="6" rx="1" fill="white"/>';
      return wrap(chCross+yBox+numsEl);
    }
    /* FR â€” EU stripe [F] left, example centre, dept number right (blue box) */
    if(tp==='fr'){
      const deptBox='<rect x="130" y="0" width="32" height="38" rx="4" fill="#002699" opacity=".9"/>'
        +'<rect x="126" y="4" width="32" height="30" rx="3" fill="none" stroke="#f59e0b" stroke-width="2"/>'
        +'<text x="142" y="26" text-anchor="middle" fill="#fff" font-size="'+fs+'" font-family="Arial" font-weight="bold">'+ex+'</text>';
      const frNums='<text x="76" y="24" text-anchor="middle" fill="#bbb" font-size="9.5" font-family="Arial">'+nums+'</text>';
      return wrap(euStripe+frNums+deptBox);
    }
    /* TR â€” yellow box left, pipe, number right */
    if(tp==='tr'){
      return wrap(
        '<rect x="4" y="5" width="36" height="28" rx="3" fill="#fffacc" stroke="#f59e0b" stroke-width="2"/>'
        +'<text x="22" y="25" text-anchor="middle" fill="#1a1a1a" font-size="'+fs+'" font-family="Arial" font-weight="bold">'+ex+'</text>'
        +'<line x1="45" y1="9" x2="45" y2="29" stroke="#ddd" stroke-width="1"/>'
        +'<text x="104" y="24" text-anchor="middle" fill="#aaa" font-size="9.5" font-family="Arial">'+nums+'</text>');
    }
    /* NAT â€” oval badge */
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
    /* default â€” EU fallback */
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
        const _natOpt='<option value="nat" '+(acF==="nat"?"selected":"")+'>ðŸŒ Andere L\u00e4nder (L\u00e4nderk\u00fcrzel)</option>';
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
    /* FIX: summary must NOT use display:flex or list-style:none â€”        */
    /* those CSS properties break the native toggle in WebKit/iOS.         */
    const showCountries=(acF==="all"||acF==="nat")?countries:[acF];
    const archiveRows=showCountries.map(country=>{
      try{
        const uPlates=getUniquePlatesForCountry(country)||[];
        if(\!uPlates.length)return"";
        const collHere=uPlates.filter(u=>isCollected(u.code,country));
        if(\!collHere.length)return"";
        const cPct=Math.round(collHere.length/Math.max(uPlates.length,1)*100);
        /* Render plates â€” use mainRegion||region fallback so nothing is dropped */
        const plateHtml=collHere
          .map(u=>renderRealPlate(u.code,u.mainRegion||u.region||"",u.count-1||0))
          .join("");
        return`<details style="margin-bottom:.5rem;border:1px solid var(--border);border-radius:10px;overflow:hidden">
          <summary style="padding:.5rem .75rem;cursor:pointer;font-weight:700;font-size:.82rem;user-select:none;background:var(--bg2)">${esc(country)} â€” ${collHere.length}/${uPlates.length} \u00b7 ${cPct}%</summary>
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
  /* Collected countries (EN) â†’ unique codes collected there */
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
          .text("âœ•").on("click",()=>d3.select(el).selectAll(".map-popup").remove());
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
   PHASE 86 â€” Logik-Gitter + Reiseroute
   =================================================================== */

/* Shared: save score and transition to gameover screen */
function finishCustomGame(){
  soundOver();
  S.ph="gameover";S.scoreSaved=false;S.convModal=true;
  checkMastery();
  saveHistory({mode:S.mode,score:S.sc,correct:S.correct,rounds:S.correct,date:Date.now(),answers:[]});
  if(sbOK)saveSession(S.mode,S.sc,S.sc,S.correct,Date.now()-(S.gameStartTime||Date.now())).then(()=>{S.scoreSaved=true;render();});
  render();
}

/* ---- Logik-Gitter ---- */
function checkGridCriterion(name,crit){
  const co=COUNTRIES.find(c=>c.c===name);
  if(!co)return false;
  if(crit.type==="continent")return co.ct===crit.value;
  /* P148: check localized first letter, fall back to English */
  if(crit.type==="letter"){
    const _lang=(typeof S!=="undefined"&&S.language)||"de";
    let _ln=name;
    try{if(co)_ln=getCountryName(co.cc,_lang)||name;}catch(e){}
    return (_ln[0]||"").toUpperCase()===crit.value;
  }
  if(crit.type==="has_border"){const nbs=ROUTE_BORDERS[crit.value]||[];return nbs.includes(name);}
  /* P144: new types */
  if(crit.type==="subregion")return co.sr===crit.value;
  if(crit.type==="island")return _ISLAND_STATES.has(name);
  if(crit.type==="landlocked")return _LANDLOCKED_SET.has(name);
  if(crit.type==="eu_member")return _EU_MEMBERS.has(name);
  return false;
}
function getGridSugg(txt){
  if(!txt||txt.length<1)return[];
  const t=txt.toLowerCase();
  const lang=(typeof S!=="undefined"&&S.language)||localStorage.getItem("gq_lang")||"de";
  /* P147: defensive Set */
  const _uc=S.gridData?S.gridData.usedCountries:null;
  const used=(_uc instanceof Set)?_uc:new Set(_uc?Array.from(_uc):[]);
  /* P147: match English OR localized name */
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
  /* P147: show localized name, keep English key in data-name */
  const _lang=(typeof S!=="undefined"&&S.language)||"de";
  el.innerHTML=(S.gridSugg||[]).slice(0,12).map(s=>{
    const _co=COUNTRIES.find(c=>c.c===s);
    const _dn=_co?getCountryName(_co.cc,_lang):s;
    return `<div class="lg-sugg-item" data-name="${esc(s)}" onclick="handleGridAnswer(S.gridData.activeCell.r,S.gridData.activeCell.c,this.dataset.name)">${flagOf(s)} ${esc(_dn)}</div>`;
  }).join("");
}
function handleGridAnswer(r,c,country){
  const gd=S.gridData;
  if(!gd||gd.solved||gd.failed)return;
  const cell=gd.cells[r*3+c];
  if(cell.country)return;
  const ok=checkGridCriterion(country,gd.rowCrit[r])&&checkGridCriterion(country,gd.colCrit[c]);
  if(ok){
    cell.country=country;
    gd.usedCountries.add(country);
    gd.correctCount++;
    gd.score+=500+gd.lives*50;
    gd.lastMsg="\u2713 Richtig! "+country;
    gd.lastOk=true;
    gd.activeCell=null;
    S.gridInput="";
    S.gridSugg=[];
    if(gd.correctCount>=9)gd.solved=true;
  }else{
    gd.lives--;
    gd.lastMsg="\u2717 "+country+" passt nicht zu beiden Kriterien.";
    gd.lastOk=false;
    if(gd.lives<=0){gd.failed=true;gd.activeCell=null;}
  }
  /* P150: stop timer on game end */
  if(gd.solved||gd.failed)clearInterval(tIv);
  S.sc=gd.score;
  render();
}
function initLogikGitter(){
  const allCo=COUNTRIES.filter(c=>c.ct);
  /* P144: helper -- Fisher-Yates shuffle returning new array */
  function _shuf(a){const b=a.slice();for(let i=b.length-1;i>0;i--){const j=~~(Math.random()*(i+1));[b[i],b[j]]=[b[j],b[i]];}return b;}
  /* P144: check all 9 cells have >=1 valid country */
  function _ok(rc,cc){for(let r=0;r<3;r++)for(let c=0;c<3;c++)if(!allCo.some(co=>checkGridCriterion(co.c,rc[r])&&checkGridCriterion(co.c,cc[c])))return false;return true;}
  let rowCrit,colCrit,found=false;
  /* 60 attempts: each picks 3 random rows + 3 random cols from separate pools */
  for(let t=0;t<60&&!found;t++){
    const rows=_shuf(GRID_ROW_POOL);
    const cols=_shuf(GRID_COL_POOL);
    const rc=[rows[0],rows[1],rows[2]];
    const cc=[cols[0],cols[1],cols[2]];
    if(_ok(rc,cc)){rowCrit=rc;colCrit=cc;found=true;}
  }
  /* P144 fallback: 5 diverse known-good combos (not always EU/AS/AF + A/B/C) */
  if(!found){
    const _fb=[
      {r:["eu","as","af"],  c:["ls","lm","lp"]},
      {r:["eu","af","sa"],  c:["la","li","lt"]},
      {r:["as","af","na"],  c:["lb","ln","ls"]},
      {r:["eu","as","sa"],  c:["la","lc","lm"]},
      {r:["eu","af","as"],  c:["li","ls","lt"]},
    ][~~(Math.random()*5)];
    const byId=id=>GRID_ROW_POOL.find(x=>x.id===id)||GRID_COL_POOL.find(x=>x.id===id);
    rowCrit=_fb.r.map(byId);colCrit=_fb.c.map(byId);
  }
  S.gridData={rowCrit,colCrit,
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
    render();
  },1000);
}
function renderLogikGitter(sc){
  const gd=S.gridData;
  if(!gd)return '<div class="scr"></div>';
  const hearts='\u2764\ufe0f'.repeat(gd.lives)+'\uD83D\uDDA4'.repeat(3-gd.lives);
  /* P136: instruction above grid */
  const _lgInstr='<p style="font-size:.8rem;color:var(--text2);text-align:center;margin-bottom:.6rem;line-height:1.4">Tippe auf ein <b>+</b>-Feld und w\u00e4hle ein Land, das zur <b>Zeile</b> und <b>Spalte</b> passt!</p>';
  let gridHtml=_lgInstr+'<div class="lg-grid" style="display:grid;grid-template-columns:max-content repeat(3,1fr);gap:8px;margin-top:15px;align-items:stretch">';
  gridHtml+='<div class="lg-corner"><span style="font-size:.6rem;color:var(--text3)">\u2193 Zeile / Spalte \u2192</span></div>';
  for(let c=0;c<3;c++)gridHtml+=`<div class="lg-header">${gd.colCrit[c].label}</div>`;
  for(let r=0;r<3;r++){
    gridHtml+=`<div class="lg-header lg-row-hdr">${gd.rowCrit[r].label}</div>`;
    for(let c=0;c<3;c++){
      const cell=gd.cells[r*3+c];
      const isAct=gd.activeCell&&gd.activeCell.r===r&&gd.activeCell.c===c;
      if(cell.country){
        gridHtml+=`<div class="lg-cell lg-filled">${flagOf(cell.country)}<div class="lg-cell-name">${esc(displayCountry(cell.country))}</div></div>`;
      }else if(gd.solved||gd.failed){
        gridHtml+='<div class="lg-cell lg-empty-done">â€”</div>';
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
      <div style="font-size:.75rem;color:var(--text3);margin-bottom:5px"><strong>${esc(gd.rowCrit[r].label)}</strong> + <strong>${esc(gd.colCrit[c].label)}</strong></div>
      <input type="text" id="lg-inp" placeholder="Land eingeben\u2026" value="${esc(S.gridInput||'')}"
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
      <button class="btn-p" onclick="S.sc=S.gridData.score;S.correct=S.gridData.correctCount;S.rd=S.gridData.correctCount;finishCustomGame()">Ergebnis ansehen</button>`
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
        <button class="btn-cancel" onclick="clr();S.ph='menu';S.tab='home';render()">\u00d7</button>
      </div>
    </div>
    <div class="tbar"><div class="tfill" style="width:${pct()}%;background:${tc()}"></div></div>
    <div style="text-align:center;font-size:.92rem;font-weight:900;color:var(--text);padding:.4rem 0 .2rem">\u{1F9E9} Logik-Gitter</div>
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
        <button class="btn-cancel" onclick="clr();S.ph='menu';S.tab='home';render()">\u00d7</button>
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
const WAPPEN_DATA=[
  {cc:"de",c:"Deutschland",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Germany.svg"},
  {cc:"fr",c:"Frankreich",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_France.svg"},
  {cc:"es",c:"Spanien",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Spain.svg"},
  {cc:"it",c:"Italien",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Italy.svg"},
  {cc:"pt",c:"Portugal",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Portugal.svg"},
  {cc:"at",c:"Ã–sterreich",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Austria.svg"},
  {cc:"ch",c:"Schweiz",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Switzerland.svg"},
  {cc:"pl",c:"Polen",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Poland.svg"},
  {cc:"cz",c:"Tschechien",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_the_Czech_Republic.svg"},
  {cc:"hu",c:"Ungarn",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Hungary.svg"},
  {cc:"ro",c:"RumÃ¤nien",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Romania.svg"},
  {cc:"bg",c:"Bulgarien",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Bulgaria.svg"},
  {cc:"gr",c:"Griechenland",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Greece.svg"},
  {cc:"hr",c:"Kroatien",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Croatia.svg"},
  {cc:"sk",c:"Slowakei",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Slovakia.svg"},
  {cc:"si",c:"Slowenien",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Slovenia.svg"},
  {cc:"be",c:"Belgien",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Belgium.svg"},
  {cc:"nl",c:"Niederlande",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_the_Netherlands.svg"},
  {cc:"dk",c:"DÃ¤nemark",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Denmark.svg"},
  {cc:"se",c:"Schweden",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Sweden.svg"},
  {cc:"fi",c:"Finnland",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Finland.svg"},
  {cc:"no",c:"Norwegen",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Norway.svg"},
  {cc:"ie",c:"Irland",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Ireland.svg"},
  {cc:"lu",c:"Luxemburg",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Luxembourg.svg"},
  {cc:"rs",c:"Serbien",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Serbia.svg"},
  {cc:"ua",c:"Ukraine",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Ukraine.svg"},
  {cc:"al",c:"Albanien",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Albania.svg"},
  {cc:"me",c:"Montenegro",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Montenegro.svg"},
  {cc:"ba",c:"Bosnien",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_Bosnia_and_Herzegovina.svg"},
  {cc:"mk",c:"Nordmazedonien",img:"https://commons.wikimedia.org/wiki/Special:FilePath/Coat_of_arms_of_North_Macedonia.svg"},
];
function genWappenQ(){
  if(\!WAPPEN_DATA||WAPPEN_DATA.length<4)return null;
  const _r=arr=>arr[~~(rng()*arr.length)];
  const correct=_r(WAPPEN_DATA.filter(w=>w.c\!==S.lid));
  const others=WAPPEN_DATA.filter(w=>w.cc\!==correct.cc);
  const wrongs=[];const used=new Set([correct.cc]);
  while(wrongs.length<3&&others.length>wrongs.length){const w=_r(others);if(\!used.has(w.cc)){used.add(w.cc);wrongs.push(w);}}
  if(wrongs.length<3)return null;
  const opts=[correct,...wrongs].sort(()=>rng()-.5).map(w=>w.c);
  return{type:"wappen",prompt:"Welchem Land gehÃ¶rt dieses Wappen?",subj:correct.c,img:correct.img,opts,ans:correct.c,lid:correct.cc,cc:correct.cc,meta:"ðŸ›¡ï¸ Wappen von "+correct.c};
}

/* â”€â”€ STADT-LAND-FLUSS (SLF) â”€â”€ (Phase 106) */
const SLF_LETTERS="ABCDEFGHIKLMNOPRSTW";
function initSLF(){
  clearInterval(tIv);
  const letter=SLF_LETTERS[~~(rng()*SLF_LETTERS.length)];
  S.slfData={letter,answers:{city:"",country:"",river:""},phase:"input",timeLeft:30};
  S.gameStartTime=Date.now();
  S.ph="playing";
  tIv=setInterval(()=>{
    if(\!S.slfData||S.slfData.phase\!=="input")return;
    S.slfData.timeLeft--;
    if(S.slfData.timeLeft<=0){clearInterval(tIv);handleSLFSubmit();}
    else render();
  },1000);
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
  const timerCol=timeLeft<=10?"#ef4444":timeLeft<=20?"#f59e0b":"#10b981";
  if(phase==="result"){
    const{cityValid,countryValid,riverValid}=S.slfData.results||{};
    const rowHtml=(label,val,valid)=>`<div class="slf-result-row"><span class="slf-result-label">${label}</span><span class="slf-result-val">${esc(val)||"â€”"}</span><span style="font-size:1rem">${valid?"âœ…":"âŒ"}</span></div>`;
    return`<div class="scr"><div class="panel">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.75rem">
        <div><div style="font-size:.6rem;letter-spacing:1px;color:var(--text3);font-weight:700">ERGEBNIS</div><div style="font-size:1.4rem;font-weight:900">ðŸ“ ${letter}</div></div>
        <div style="text-align:right"><div style="font-size:.6rem;color:var(--text3)">PUNKTE</div><div style="font-size:1.6rem;font-weight:900;color:#10b981">+${(cityValid?10:0)+(countryValid?10:0)+(riverValid?10:0)}</div></div>
      </div>
      ${rowHtml("Stadt",answers.city,cityValid)}
      ${rowHtml("Land",answers.country,countryValid)}
      ${rowHtml("Fluss",answers.river,riverValid)}
      <div style="margin-top:1rem;font-size:.72rem;color:var(--text3);text-align:center">Gesamt: ${sc.toLocaleString()} Punkte</div>
      <button class="btn-p" style="margin-top:.85rem" onclick="initSLF()">ðŸ“ Neue Runde</button>
      <button class="btn-g" style="margin-bottom:0" onclick="clr();S.ph='menu';S.tab='home';render()">Beenden</button>
    </div></div>`;
  }
  return`<div class="scr"><div class="panel">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem">
      <div><div style="font-size:.6rem;letter-spacing:1px;color:var(--text3);font-weight:700">BUCHSTABE</div><div style="font-size:2.6rem;font-weight:900;line-height:1">${letter}</div></div>
      <div style="text-align:right"><div style="font-size:.6rem;color:var(--text3)">ZEIT</div><div style="font-size:2rem;font-weight:900;color:${timerCol}">${timeLeft}s</div></div>
    </div>
    <div class="tbar" style="margin-bottom:1rem"><div class="tfill" style="width:${Math.round(timeLeft/30*100)}%;background:${timerCol}"></div></div>
    <div class="slf-field"><label class="slf-label">\u{1F3D9} STADT</label><input id="slf-city" type="text" dir="ltr" class="slf-input" style="direction:ltr;text-align:left;padding-left:10px" placeholder="Stadt mit ${letter}â€¦" autocomplete="off" autocorrect="off" value="${esc(answers.city)}" oninput="S.slfData.answers.city=this.value;render()" onkeydown="if(event.key==='Enter')document.getElementById('slf-country')?.focus()"></div>
    <div class="slf-field"><label class="slf-label">\u{1F30D} LAND</label><input id="slf-country" type="text" dir="ltr" class="slf-input" style="direction:ltr;text-align:left;padding-left:10px" placeholder="Land mit ${letter}â€¦" autocomplete="off" autocorrect="off" value="${esc(answers.country)}" oninput="S.slfData.answers.country=this.value;render()" onkeydown="if(event.key==='Enter')document.getElementById('slf-river')?.focus()"></div>
    <div class="slf-field"><label class="slf-label">\u{1F4A7} FLUSS</label><input id="slf-river" type="text" dir="ltr" class="slf-input" style="direction:ltr;text-align:left;padding-left:10px" placeholder="Fluss mit ${letter}â€¦" autocomplete="off" autocorrect="off" value="${esc(answers.river)}" oninput="S.slfData.answers.river=this.value;render()" onkeydown="if(event.key==='Enter')handleSLFSubmit()"></div>
    <button class="btn-p" style="margin-top:.85rem" onclick="handleSLFSubmit()">âœ” Auswerten</button>
    <button class="btn-g" style="margin-bottom:0;font-size:.78rem" onclick="clr();S.ph='menu';S.tab='home';render()">Abbrechen</button>
  </div></div>`;
}

/* â”€â”€ ACCOUNT LÃ–SCHEN (DSGVO) â”€â”€ (Phase 106) */
async function doDeleteAccount(){
  if(\!sbUser)return;
  const conf1=confirm("Konto wirklich lÃ¶schen? Alle Daten gehen verloren.");
  if(\!conf1)return;
  const conf2=confirm("Diese Aktion ist NICHT rÃ¼ckgÃ¤ngig zu machen. Fortfahren?");
  if(\!conf2)return;
  try{
    await sb.from("profiles").delete().eq("id",sbUser.id);
    await sb.auth.signOut();
    showToast("\u{1F5D1}ï¸ Konto gelÃ¶scht");
    S.settingsModal=false;
    doLogout();
  }catch(e){showToast("âš ï¸ Fehler: "+e.message);}
}

/* â”€â”€ AD INTERSTITIAL â”€â”€ (Phase 107) */
function showAd(){if(!ENABLE_ADS||\!sbProfile?.is_premium)return; /* P151 */S.adModal=true;render();}
function closeAd(){S.adModal=false;render();}
function renderAdModal(){
  return`<div class="modal-overlay" onclick="closeAd()" style="z-index:500"><div class="modal-box" style="max-width:320px;padding:1.25rem">
    <div style="text-align:center;font-size:.6rem;color:var(--text3);letter-spacing:1.2px;margin-bottom:.6rem">ANZEIGE Â· UNTERSTÃœTZT GEOQUEST</div>
    <div style="min-height:100px;background:var(--bg3);border-radius:12px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:var(--text3);border:1.5px dashed var(--border);margin-bottom:.85rem;padding:1rem">
      <div style="font-size:1.8rem;margin-bottom:.35rem">ðŸ“¢</div>
      <div style="font-size:.8rem;font-weight:700">Werbung</div>
      <div style="font-size:.68rem;margin-top:2px">Hier kÃ¶nnte deine Anzeige stehen</div>
    </div>
    <button class="btn-p" onclick="closeAd()">Weiter spielen â†’</button>
    <button class="btn-g" style="margin-bottom:0;font-size:.76rem;color:#f59e0b;border-color:#f59e0b" onclick="S.payModal=true;closeAd()">ðŸ‘‘ Werbung entfernen (Premium)</button>
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

function renderHomeTab(){
  console.log("[GQ] renderHomeTab() activeCategory=",S.activeCategory);
  function catSection(catId){
    const cat=MODE_CATS[catId];
    if(\!cat){console.warn("[GQ] catSection: unknown catId",catId);return"";}
    const unlocked=isCategoryUnlocked(catId);
    const isOpen=S.activeCategory===catId;
    const catModes=MODES.filter(m=>cat.modes.includes(m.id)&&\!m.comingSoon);
    const cards=catModes.map(m=>{
      const cs=m.comingSoon===true;
      const bt=m.beta===true&&\!cs;
      const active=S.mode===m.id&&\!cs;
      const cardCls="mode-card"+(active?" active":"")+(cs?" coming-soon-card":"")+(bt?" beta-card":"")+(\!unlocked&&\!cs?" locked-card":"");
      const clickAct=cs?"showComingSoonToast('"+m.title+"')":unlocked?"startGame('"+m.id+"')":"S.lockModal='"+catId+"';render()";
      return`<div class="${cardCls}" onclick="${clickAct}" role="button">
        ${cs?`<span class="cs-badge">Bald</span>`:""}
        ${bt?`<span class="beta-badge" title="${t('beta_warning')}">${t('badge_beta')}</span>`:""}
        <span class="mode-icon">${m.icon}</span><div class="mode-title">${modeTitle(m)}</div>
        ${m.desc?`<div class="mode-desc">${m.desc}</div>`:""}
      </div>`;
    }).join("");
    const lockOverlay=\!unlocked?`<div class="cat-lock-overlay" onclick="S.lockModal='${catId}';render()">
      <div style="text-align:center">
        <div style="font-size:2rem;margin-bottom:6px">\u{1F512}</div>
        <div style="color:var(--text);font-weight:900;font-size:.88rem">${cat.label}</div>
        <div style="color:var(--text2);font-size:.75rem;margin:4px 0 10px">\u{1F4B0} ${cat.cost.toLocaleString()} GeoCoins</div>
        <button class="btn-p" style="width:auto;padding:.4rem .9rem;font-size:.78rem;margin-bottom:0" onclick="event.stopPropagation();S.lockModal='${catId}';render()">Freischalten</button>
      </div>
    </div>`:"";
    const chv=`<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" style="transition:transform .22s;transform:${isOpen?"rotate(180deg)":"rotate(0deg)"}"><polyline points="6 9 12 15 18 9"/></svg>`;
    return`<div class="acc-item${isOpen?" acc-open":""}">
      <div class="acc-header" role="button" tabindex="0" onclick="S.activeCategory=S.activeCategory==='${catId}'?null:'${catId}';render()" aria-expanded="${isOpen}">
        <div style="display:flex;align-items:center;gap:8px">
          <span style="font-size:1.15rem;flex-shrink:0">${cat.icon}</span>
          <span class="acc-label">${cat.label}</span>
          ${\!unlocked?`<span class="acc-lock-pill">\u{1F512} ${cat.cost.toLocaleString()} Coins</span>`:""}
        </div>
        <span style="color:var(--text3);display:flex;align-items:center">${chv}</span>
      </div>
      ${isOpen?`<div class="acc-body">
        <div style="position:relative"><div class="mode-grid" style="opacity:${unlocked?1:.4}">${cards}</div>${lockOverlay}</div>
        ${catId==="eu_plates"?`<div style="background:var(--bg2);border:2px solid #3b82f6;border-radius:14px;padding:.8rem;margin-top:.5rem;cursor:pointer;display:flex;align-items:center;gap:12px;box-shadow:0 2px 10px rgba(59,130,246,.12);transition:opacity .15s" onclick="S.tab='album';render()" onmousedown="this.style.opacity='.7'" onmouseup="this.style.opacity='1'">
          <div style="width:38px;height:38px;background:linear-gradient(135deg,#1d4ed8,#3b82f6);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0">\u{1F4D4}</div>
          <div style="flex:1;min-width:0"><div style="font-weight:900;font-size:.83rem;color:var(--text)">Kennzeichen-Album & Spotter</div><div style="font-size:.68rem;color:var(--text3);margin-top:1px">${S.collectedPlates.length} von ${totalUniquePlates()||"?"} gesammelt</div></div>
          <div style="color:#3b82f6;font-size:1rem;font-weight:700">\u2192</div>
        </div>`:""}
      </div>`:"" }
    </div>`;
  }
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
        <div style="font-size:2.2rem">\u2694\uFE0F</div>
        <div>
          <div style="font-size:1rem;font-weight:900;color:#fff">Live 1vs1 Duell</div>
          <div style="font-size:.74rem;color:rgba(255,255,255,.75);margin-top:2px">${t("home_pvp_sub")}</div>
        </div>
        <div style="margin-left:auto;background:#7c3aed;color:#fff;border-radius:20px;padding:.3rem .85rem;font-size:.76rem;font-weight:700">\u25ba Spielen</div>
      </div>
    </div>
    <div class="acc-list">
      ${catSection("pure_geo")}
      ${catSection("lifestyle")}
      ${catSection("eu_plates")}
      ${catSection("comparisons")}
      ${catSection("neighbors")}
      ${catSection("map_mode")}
    </div>
    <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px"><span style="font-size:.65rem;color:var(--text3);font-weight:700;letter-spacing:.8px">SCHWIERIGKEIT</span><span title="Casual: Entspannt, kein Zeitlimit, unendlich Leben&#10;Hardcore: Kein Zeitlimit, 3 Leben (Game Over nach 3 Fehlern)&#10;Survival: 8 Sek. pro Frage, 3 Leben" style="font-size:.72rem;cursor:help;color:var(--text3)">â„¹ï¸</span></div>
    <div class="diff-toggle">
      <button class="diff-btn ${S.diff==="casual"?"active":""}" onclick="S.diff='casual';render()">Casual</button>
      <button class="diff-btn ${S.diff==="hardcore"?"active":""}" onclick="S.diff='hardcore';render()">Hardcore</button>
      <button class="diff-btn ${S.diff==="survival"?"active":""}" onclick="S.diff='survival';render()">\ud83d\udc80 Survival</button>
    </div>
    <p style="text-align:center;color:var(--text2);font-size:.72rem;font-weight:600;margin:.3rem 0 .5rem">${
      t(S.diff==="casual"?"diff_desc_casual":S.diff==="hardcore"?"diff_desc_hc":"diff_desc_surv")
    }</p>
    <div style="height:5rem"></div>`;
  console.log("[GQ] renderHomeTab() returning length:",_homeHTML.length);
  return _homeHTML;
}

/* LERNEN TAB â€” Flashcards (Phase 23C) */
function renderLernenTab(){
  const pool=(()=>{
    let p=PLATES_DATA;
    if(S.fcCountry\!=="all")p=p.filter(x=>x.country===S.fcCountry);
    if(S.fcSearch.trim())p=p.filter(x=>x.code.toLowerCase().includes(S.fcSearch.toLowerCase())||x.region.toLowerCase().includes(S.fcSearch.toLowerCase()));
    return p;
  })();
  if(\!pool.length)return`<div class="panel" style="text-align:center;padding:2rem"><div style="font-size:2rem">\u{1F50D}</div><p style="color:var(--text3);margin-top:.5rem">Keine Karten gefunden.</p></div>`;
  const idx=Math.min(S.fcIdx,pool.length-1);
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
      <button class="btn-p" style="margin-bottom:0;flex:1" onclick="S.fcIdx=Math.min(pool.length-1,S.fcIdx+1);S.fcFlipped=false;render()" ${idx>=pool.length-1?"disabled":""}>Weiter \u2192</button>
    </div>
    <button class="btn-g" style="margin-top:.5rem" onclick="S.fcIdx=~~(Math.random()*pool.length);S.fcFlipped=false;render()">\u{1F500} Zuf\u00e4llig</button>
  </div>`;
}

/* LIGA TAB â€” Leaderboard */
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

/* PROFIL TAB â€” Auth + Passport + Stats */
function promptNameChange(){
  if(!sbUser?.email){showToast("Nur fÃ¼r angemeldete Nutzer.");return;}
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
      ()=>showToast("\u2713 Name geÃ¤ndert!"),
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
    const _aIcon=isReg?"ðŸŒ±":"ðŸ”‘";
    const _aTitle=isReg?"Konto erstellen":isForgot?"Passwort vergessen":isNewPw?"Neues Passwort":"Anmelden";
    const _aSub=isReg?"Dein Fortschritt wird gesichert.":isForgot?"Wir senden dir einen Reset-Link.":isNewPw?"WÃ¤hle ein neues Passwort.":"Willkommen zurÃ¼ck!";
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
        <div class="auth-field"><label>PASSWORT BESTÃ„TIGEN</label><div style="position:relative"><input id="pw-confirm" type="password" style="padding-right:2.4rem" placeholder="Passwort wiederholen" value="${S.authConfirm}" oninput="S.authConfirm=this.value" onkeydown="if(event.key==='Enter')doSetNewPassword();"><button type="button" onclick="togglePw('pw-confirm',this)" style="position:absolute;right:.55rem;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;color:var(--text3);font-size:1.1rem;padding:0;line-height:1">\u{1F441}</button></div></div>
        <button class="btn-p" onclick="doSetNewPassword()" ${S.authLoading?"disabled":""}>${S.authLoading?"Bitte warten â€¦":"ðŸ”‘ Passwort setzen"}</button>
        <button class="btn-g" style="margin-bottom:0;background:transparent;border:none;color:var(--text3);font-size:.78rem;text-decoration:underline;cursor:pointer" onclick="S.authMode='login';S.authError='';render()">ZurÃ¼ck zum Login</button>
      `:isForgot?`
        <div class="auth-field"><label>E-MAIL</label><input type="email" placeholder="deine@email.de" value="${S.authEmail}" oninput="S.authEmail=this.value" onkeydown="if(event.key==='Enter')doForgotPassword()"></div>
        <button class="btn-p" onclick="doForgotPassword()" ${S.authLoading?"disabled":""}>${S.authLoading?"Bitte warten â€¦":"ðŸ“§ Reset-Link senden"}</button>
        <button class="btn-g" style="margin-bottom:0;background:transparent;border:none;color:var(--text3);font-size:.78rem;text-decoration:underline;cursor:pointer" onclick="S.authMode='login';S.authError='';render()">ZurÃ¼ck zum Login</button>
      `:`
        ${isReg?`<div class="auth-field"><label>BENUTZERNAME</label><input type="text" placeholder="Dein Spielername" maxlength="20" value="${S.authUsername}" oninput="S.authUsername=this.value"></div>`:""}
        <div class="auth-field"><label>E-MAIL</label><input type="email" placeholder="deine@email.de" value="${S.authEmail}" oninput="S.authEmail=this.value"></div>
        <div class="auth-field"><label>PASSWORT</label><div style="position:relative"><input id="pw-main" type="password" style="padding-right:2.4rem" placeholder="${isReg?"Mind. 6 Zeichen":"â€¢â€¢â€¢â€¢â€¢â€¢"}" value="${S.authPassword}" oninput="S.authPassword=this.value" onkeydown="if(event.key==='Enter'){${isReg?"doRegister":"doLogin"}();}"><button type="button" onclick="togglePw('pw-main',this)" style="position:absolute;right:.55rem;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;color:var(--text3);font-size:1.1rem;padding:0;line-height:1">\u{1F441}</button></div></div>
        ${isReg?`<div class="auth-field"><label>PASSWORT BESTÃ„TIGEN</label><div style="position:relative"><input id="pw-confirm" type="password" style="padding-right:2.4rem" placeholder="Passwort wiederholen" value="${S.authConfirm}" oninput="S.authConfirm=this.value" onkeydown="if(event.key==='Enter')doRegister();"><button type="button" onclick="togglePw('pw-confirm',this)" style="position:absolute;right:.55rem;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;color:var(--text3);font-size:1.1rem;padding:0;line-height:1">\u{1F441}</button></div></div>`:""}
        <button class="btn-p" onclick="${isReg?"doRegister":"doLogin"}()" ${S.authLoading?"disabled":""}>
          ${S.authLoading?"Bitte warten â€¦":isReg?"ðŸŒ± Konto erstellen &amp; Fortschritt sichern":"ðŸ”‘ Anmelden"}
        </button>
        ${isAnon&&isReg&&totalStamps>0?`<div style="background:rgba(16,185,129,.08);border:1px solid #10b981;border-radius:8px;padding:.5rem .75rem;font-size:.74rem;color:#10b981;margin-top:.25rem">ðŸ’¾ ${totalStamps} Stempel &amp; deine Punkte werden Ã¼bernommen.</div>`:""}
        ${\!isReg?`<button class="btn-g" style="margin-top:.25rem;margin-bottom:0;background:transparent;border:none;color:var(--text3);font-size:.78rem;text-decoration:underline;cursor:pointer" onclick="S.authMode='forgot';S.authError='';render()">Passwort vergessen?</button>`:""}
      `}
    </div>`;
  } else {
    const name=getDisplayName();
    const _lg=getLeague(sbProfile?.current_league||"Bronze");
    block1=`<div class="auth-card">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:1rem">
        <div style="width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#10b981,#0891b2);display:flex;align-items:center;justify-content:center;font-size:1.3rem;font-weight:900;color:#fff;flex-shrink:0">${name?name[0].toUpperCase():"ðŸ‘¤"}</div>
        <div><div style="font-size:1rem;font-weight:900;color:var(--text);display:flex;align-items:center;gap:6px">${name||"Spieler"}<button onclick="promptNameChange()" title="Namen Ã¤ndern" style="background:none;border:none;cursor:pointer;font-size:.8rem;color:var(--text3);padding:0;line-height:1;vertical-align:middle;opacity:.65;transition:opacity .15s" onmouseenter="this.style.opacity='1'" onmouseleave="this.style.opacity='.65'">âœï¸</button></div><div style="font-size:.72rem;color:var(--text3)">${sbUser?.email||"Gast-Konto"}</div>${sbProfile?.current_title&&sbProfile.current_title\!=="Erkunder"?`<div style="display:inline-block;margin-top:3px;background:rgba(167,139,250,.15);border:1px solid #a78bfa;border-radius:20px;padding:1px 8px;font-size:.68rem;color:#a78bfa;font-weight:700">${sbProfile.current_title}</div>`:""}</div>
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
      ${sbProfile?.is_premium?`<div style="background:rgba(16,185,129,.1);border:1px solid #10b981;border-radius:8px;padding:.45rem .7rem;font-size:.74rem;color:#34d399;margin-top:.65rem">ðŸ‘‘ Premium aktiv</div>`:""}
    </div>`;
  }

  /* â”€â”€ Block 2: Economy & Inventory â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
  const block2=`<div class="panel" style="padding:.85rem">
    <div style="margin-bottom:.75rem">
      <div style="color:var(--text);font-weight:700;font-size:.85rem">ðŸ’° GeoCoins</div>
      <div style="color:#fbbf24;font-size:1.4rem;font-weight:900">${(sbProfile?.geo_coins||0).toLocaleString()}</div>
    </div>
    <div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin-bottom:.55rem">JOKER</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
      <div class="joker-card">
        <div style="font-size:1.4rem">âœ‚</div>
        <div style="font-weight:900;font-size:.82rem;color:var(--text)">50/50</div>
        <div style="color:#34d399;font-size:.75rem;font-weight:700">${pu.five0||0} Ã¼brig</div>
        <button class="joker-buy-btn" onclick="buyJoker('five0')">+3 fÃ¼r 50 ðŸ’°</button>
      </div>
      <div class="joker-card">
        <div style="font-size:1.4rem">\u{1F9CA}</div>
        <div style="font-weight:900;font-size:.82rem;color:var(--text)">Freeze</div>
        <div style="color:#60a5fa;font-size:.75rem;font-weight:700">${pu.freeze||0} Ã¼brig</div>
        <button class="joker-buy-btn" onclick="buyJoker('freeze')">+3 fÃ¼r 75 ðŸ’°</button>
      </div>
    </div>
  </div>`;

  /* â”€â”€ Block 3: Stats & Career (collapsibles) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
  /* 3a: Mastery map + accuracy + history (for details section) */
  let detailStats="";
  const modeAcc={};
  history.forEach(g=>{if(\!modeAcc[g.mode])modeAcc[g.mode]={c:0,t:0};modeAcc[g.mode].c+=g.correct;modeAcc[g.mode].t+=g.rounds;});
  const modeBars=MODES.map(m=>{const s=modeAcc[m.id];if(\!s||\!s.t)return"";const p=Math.round(s.c/s.t*100);return`<div class="stat-bar-row"><div class="stat-bar-lbl">${m.icon} ${modeTitle(m).slice(0,11)}</div><div class="stat-bar-track"><div class="stat-bar-fill ${p<50?"low":p<80?"mid":""}" style="width:${p}%"></div></div><div class="stat-bar-pct">${p}%</div></div>`;}).filter(Boolean).join("");
  const tileHtml=COUNTRIES.map(co=>{const m=mastery[co.cc]||{v:0,p:0};const r=getMasteryRank(m.v,m.p);const cls=r==="gold"?"mc-done":r==="silver"?"mc-learn":r==="bronze"?"mc-new":"";return`<div class="mc-tile${cls?" "+cls:""}" title="${co.c} Â· ${m.v} richtig" onclick="S.modal='${co.cc}';render()"></div>`;}).join("");
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
        <span>ðŸ“” Reisepass &amp; Regionen</span>
        <span style="color:var(--text3);font-size:.75rem">${totalStamps} Stempel Â· ${rank} â–¾</span></div>
      </summary>
      <div style="padding:0 .85rem .85rem">
        <div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin-bottom:.65rem">REGIONEN-FORTSCHRITT</div>
        ${regionBars}
        <div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin:.75rem 0 .5rem">ALLE LÃ„NDER</div>
        <div class="stamp-grid">${passGrid}</div>
      </div>
    </details>
    <details style="background:var(--bg2);border-radius:14px;border:1px solid var(--border);overflow:hidden;margin-bottom:.5rem">
      <summary style="padding:.75rem 1rem;font-weight:900;font-size:.88rem;cursor:pointer;user-select:none"><div style="display:flex;align-items:center;justify-content:space-between">
        <span>ðŸ† Erfolge &amp; Achievements</span>
        <span style="color:var(--text3);font-size:.75rem">â–¾</span></div>
      </summary>
      <div style="padding:0 .85rem .85rem">
        <div class="ach-grid">${achHtml}</div>
      </div>
    </details>
    <details style="background:var(--bg2);border-radius:14px;border:1px solid var(--border);overflow:hidden">
      <summary style="padding:.75rem 1rem;font-weight:900;font-size:.88rem;cursor:pointer;user-select:none"><div style="display:flex;align-items:center;justify-content:space-between">
        <span>ðŸ“Š Detaillierte Statistiken</span>
        <span style="color:var(--text3);font-size:.75rem">â–¾</span></div>
      </summary>
      <div style="padding:0 .85rem .85rem">
        <div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin-bottom:.5rem">MASTERY MAP â€” ${totalStamps} LÃ¤nder</div>
        <div style="font-size:.62rem;color:var(--text3);margin-bottom:.5rem"><span style="color:#10b981">â– </span> Gold Â· <span style="color:#3b82f6">â– </span> Silber Â· <span style="color:#f59e0b">â– </span> Bronze</div>
        <div class="mastery-tiles">${tileHtml}</div>
        ${modeBars?`<div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin:.75rem 0 .55rem">GENAUIGKEIT PRO MODUS</div>${modeBars}`:""}
        ${detailStats}
      </div>
    </details>
  </div>`;

  /* â”€â”€ Block 4: Settings & Footer â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
  const langSelect=`<select onchange="setLanguage(this.value)" style="font-size:.82rem;padding:.28rem .5rem;border-radius:8px;border:1.5px solid var(--border);background:var(--bg3);color:var(--text);cursor:pointer">
    ${[["de","Deutsch"],["en","English"],["fr","FranÃ§ais"],["es","EspaÃ±ol"],["it","Italiano"],["nl","Nederlands"],["pt","PortuguÃªs"],["pl","Polski"],["ro","RomÃ¢nÄƒ"],["hu","Magyar"],["cs","ÄŒeÅ¡tina"],["sk","SlovenÄina"],["hr","Hrvatski"],["sl","SlovensÄÃ­na"],["bg","Ð‘ÑŠÐ»Ð³Ð°Ñ€ÑÐºÐ¸"],["el","Î•Î»Î»Î·Î½Î¹ÎºÎ¬"],["da","Dansk"],["sv","Svenska"],["fi","Suomi"],["et","Eesti"],["lv","LatvieÅ¡u"],["lt","LietuviÅ³"],["mt","Malti"],["ga","Gaeilge"]].map(([l,n])=>`<option value="${l}" ${S.language===l?"selected":""}>${n}</option>`).join("")}
  </select>`;

  const block4=`<div class="panel" style="padding:.85rem;margin-top:.15rem">
    <div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin-bottom:.75rem">EINSTELLUNGEN</div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.65rem">
      <div style="color:var(--text);font-size:.88rem;font-weight:700">${S.darkMode?"ðŸŒ™ Dunkles Design":"â˜€ï¸ Helles Design"}</div>
      <button onclick="S.darkMode=\!S.darkMode;applyTheme();render()" class="btn-g" style="width:auto;padding:.4rem .85rem;margin-bottom:0;font-size:.8rem">Wechseln</button>
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.75rem">
      <div style="color:var(--text);font-size:.88rem;font-weight:700">ðŸŒ ${t("language_select")}</div>
      ${langSelect}
    </div>
    <hr style="border:none;border-top:1px solid var(--border);margin:.65rem 0 .75rem">
    <div style="text-align:center;font-size:.62rem;color:var(--text3);line-height:1.9;margin-bottom:.75rem">
      <strong style="color:var(--text2)">GeoQuest</strong> &mdash; Das Geografie-Quiz<br>
      <a href="mailto:kontakt@geoquest.app" style="color:var(--text3);text-decoration:none">kontakt@geoquest.app</a><br>
      <span style="cursor:pointer;text-decoration:underline" onclick="showToast('Impressum folgt in KÃ¼rze')">Impressum</span> &middot; <span style="cursor:pointer;text-decoration:underline" onclick="showToast('Datenschutz: Keine Weitergabe persÃ¶nlicher Daten an Dritte.')">Datenschutz</span>
    </div>
    ${sbUser?.email?`
    <hr style="border:none;border-top:1px solid rgba(239,68,68,.25);margin:.1rem 0 .75rem">
    <div style="color:var(--text3);font-size:.62rem;font-weight:700;letter-spacing:1px;margin-bottom:.6rem">GEFAHRENZONE</div>
    <button class="btn-g" style="margin-bottom:.5rem;color:#f87171;border-color:#f87171" onclick="if(confirm('Wirklich abmelden?'))doLogout()">ðŸšª Abmelden</button>
    <button class="btn-g" style="margin-bottom:0;font-size:.75rem;background:#dc3545;color:#fff;border-color:#dc3545" onclick="doDeleteAccount()">ðŸ—‘ï¸ Konto lÃ¶schen (DSGVO)</button>
    `:""}
  </div>`;

  return '<div style="padding-bottom:100px">'+block1+block2+block3+block4+'</div>';
}

/* SETTINGS MODAL */
function renderSettingsModal(){
  return`<div class="modal-overlay" onclick="if(event.target===this){S.settingsModal=false;render()}"><div class="modal-box" style="max-width:320px">
    <div style="font-size:1.1rem;font-weight:900;margin-bottom:1rem">\u2699\ufe0f Einstellungen</div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.4rem">
      <div style="font-weight:700">\u{1F310} Sprache / Language</div>
      <select onchange="setLanguage(this.value)" style="font-size:.82rem;padding:.25rem .4rem;border-radius:8px;border:1.5px solid var(--border);background:var(--bg3);color:var(--text);cursor:pointer">
        ${[["de","Deutsch"],["en","English"],["fr","FranÃ§ais"],["es","EspaÃ±ol"],["it","Italiano"],["nl","Nederlands"],["pt","PortuguÃªs"],["pl","Polski"],["ro","RomÃ¢nÄƒ"],["hu","Magyar"],["cs","ÄŒeÅ¡tina"],["sk","SlovenÄina"],["hr","Hrvatski"],["sl","SlovenÅ¡Äina"],["bg","Ð‘ÑŠÐ»Ð³Ð°Ñ€ÑÐºÐ¸"],["el","Î•Î»Î»Î·Î½Î¹ÎºÎ¬"],["da","Dansk"],["sv","Svenska"],["fi","Suomi"],["et","Eesti"],["lv","LatvieÅ¡u"],["lt","LietuviÅ³"],["mt","Malti"],["ga","Gaeilge"]].map(([l,n])=>`<option value="${l}" ${S.language===l?"selected":""}>${n}</option>`).join("")}
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
    <button class="btn-g" onclick="S.challenge=null;rngSeed=null;S.ph='menu';S.tab='home';render()">Zum MenÃ¼</button>
  </div></div>`;
}

/* PAYMENT (Phase 17) */
async function processMockPayment(productId){
  const p=PAY_PRODUCTS.find(x=>x.id===productId);if(\!p)return;
  if(p.pu&&p.pu_qty){addPU(p.pu,p.pu_qty);S.payModal=false;render();showToast("âœ“ "+p.name+" hinzugefÃ¼gt\!");return;}
  if(sbOK&&sbUser){
    if(p.coins>0){const _cr=await sb.rpc("add_coins",{p_user_id:sbUser.id,p_amount:p.coins});
      if(_cr.data!=null&&sbProfile)sbProfile.geo_coins=_cr.data;
      else if(sbProfile)sbProfile.geo_coins=(sbProfile.geo_coins||0)+p.coins;}
    if(p.premium){const u=new Date();u.setMonth(u.getMonth()+(p.months||1));
      const _upd={is_premium:true,premium_until:u.toISOString()};
      await sb.from("profiles").update(_upd).eq("id",sbUser.id);
      if(sbProfile)Object.assign(sbProfile,_upd);}
  }
  S.payModal=false;render();showToast("âœ“ "+p.name+" aktiviert\!");
}
function renderPayModal(){
  const prem=sbProfile?.is_premium;
  const until=prem&&sbProfile?.premium_until?new Date(sbProfile.premium_until).toLocaleDateString("de-DE"):"";
  return`<div class="modal-overlay" onclick="if(event.target===this){S.payModal=false;render()}"><div class="modal-box" style="max-width:360px">
    <div style="font-size:1.2rem;font-weight:900;color:var(--text);margin-bottom:.35rem">\u{1F4B3} Shop</div>
    ${prem?`<div style="background:rgba(16,185,129,.1);border:1px solid #10b981;border-radius:8px;padding:.45rem .7rem;font-size:.74rem;color:#34d399;margin-bottom:.6rem">\u{1F451} Premium aktiv${until?" â€¢ bis "+until:""}</div>`:""}
    <div style="color:var(--text3);font-size:.7rem;margin-bottom:.7rem">${STRIPE_PK?"Stripe aktiv":"Testmodus â€” kein echtes Geld"}</div>
    ${PAY_PRODUCTS.map(p=>`<div class="pay-product${p.featured?" featured":""}" onclick="processMockPayment('${p.id}')"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2px"><div class="pay-product-name">${p.name}${p.featured?" â­":""}</div><div class="pay-product-price">${p.price}</div></div><div class="pay-product-desc">${p.desc}</div></div>`).join("")}
    <button class="btn-g" style="margin-bottom:0;margin-top:.35rem" onclick="S.payModal=false;render()">SchlieÃŸen</button>
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
    +'<div id="gq-ld-msg" style="font-size:.82rem;color:var(--text2,#64748b);margin-bottom:1rem">Lade globale Datenbankâ€¦</div>'
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
  const pRaw  =await safeFetch('./license_plates.json',  'Lade Kennzeichenâ€¦',  18)||[];
  const cRaw  =await safeFetch('./currencies.json',       'Lade WÃ¤hrungenâ€¦', 32)||[];
  const capRaw=await safeFetch('./capitals_population.json','Lade HauptstÃ¤dteâ€¦',48)||[];
  const rRaw  =await safeFetch('./rivers.json',           'Lade FlÃ¼sseâ€¦',    62)||[];
  const nbRaw =await safeFetch('./neighbors.json',        'Lade NachbarlÃ¤nderâ€¦',78)||[];
  const arRaw =await safeFetch('./area.json',             'Lade LÃ¤nderfÃ¤chenâ€¦',92)||[];
  const topoRaw=await safeFetch('./world-110m.json',       'Lade Weltkarteâ€¦',98);
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
    /* core files missing â€” show toast after render but still render */
    setTimeout(()=>showToast('Fehler beim Laden einiger DatensÃ¤tze.'),800);
  }
  await new Promise(r=>setTimeout(r,120));
  ov.remove();
}

if("serviceWorker"in navigator){
  try{
    const swSrc=`const CACHE='gq-v9';
/* Phase 99: passiver SW â€” kein fetch-Handler, blockt NIE Netzwerk-Requests */
self.addEventListener('install',function(){self.skipWaiting();});
self.addEventListener('activate',function(e){e.waitUntil(caches.keys().then(function(ks){return Promise.all(ks.map(function(k){return caches.delete(k);}));}).then(function(){return self.clients.claim();}));});`;
    const blob=new Blob([swSrc],{type:"application/javascript"});
    navigator.serviceWorker.register(URL.createObjectURL(blob),{scope:"./"}).catch(()=>{});
  }catch(e){}
  window.addEventListener("beforeinstallprompt",e=>{e.preventDefault();S.pwaPrompt=e;const b=document.getElementById("pwa-banner");if(b)b.style.display="flex";});
}
/* Phase 32: Tab-focus anti-cheat â€” timer keeps running in background */
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
    if(S.tm<=0){clearInterval(tIv);if(S.q)answer(null);}else render();
  }
});


/* â”€â”€ Phase 46: Smart Location Detection (IP-based, silent) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
const _GQ_IP_DE_MAP={
  "Germany":"Deutschland","Austria":"Ã–sterreich","Switzerland":"Schweiz",
  "Liechtenstein":"Liechtenstein","France":"Frankreich","Belgium":"Belgien",
  "Netherlands":"Niederlande","Luxembourg":"Luxemburg","Italy":"Italien",
  "Spain":"Spanien","Portugal":"Portugal","Poland":"Polen",
  "Czech Republic":"Tschechien","Czechia":"Tschechien","Slovakia":"Slowakei",
  "Hungary":"Ungarn","Romania":"RumÃ¤nien","Bulgaria":"Bulgarien",
  "Croatia":"Kroatien","Slovenia":"Slowenien","Serbia":"Serbien",
  "Bosnia and Herzegovina":"Bosnien","Albania":"Albanien","Montenegro":"Montenegro",
  "North Macedonia":"Nordmazedonien","Greece":"Griechenland","Turkey":"TÃ¼rkei",
  "Estonia":"Estland","Latvia":"Lettland","Lithuania":"Litauen",
  "Finland":"Finnland","Sweden":"Schweden","Norway":"Norwegen","Denmark":"DÃ¤nemark",
  "Iceland":"Island","Ireland":"Irland","United Kingdom":"Vereinigtes KÃ¶nigreich",
  "Russia":"Russland","Ukraine":"Ukraine","Belarus":"WeiÃŸrussland",
  "Moldova":"Moldau","Georgia":"Georgien","Armenia":"Armenien","Azerbaijan":"Aserbaidschan"
};
function locationBannerYes(c){
  localStorage.setItem('geoquest_pref_country',c);
  S.spotterCountry=c;S.albumCountry=c;
  showToast('âœ“ Region auf '+c+' gesetzt');
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
    if(!res.ok){console.warn('[GQ] ipapi.co HTTP '+res.status+' â€” LÃ¤ndererkennung Ã¼bersprungen');return;}
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
  /* Phase 89: Hard-Override â€” falls initAuth() nach 1s noch hÃ¤ngt */
  setTimeout(()=>{
    if(sbAuthPending){
      console.warn("[GQ] 4.5s Kill-Switch: sbAuthPending noch true â€” erzwinge render()");
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
<title>GeoQuest â€” Das Geografie-Quiz</title>
<meta name="description" content="GeoQuest â€” Das Geografie-Quiz. Erkenne LÃ¤nder an Flaggen, Kennzeichen und HauptstÃ¤dten. Sammle Stempel und steige in der Liga auf!">
<meta property="og:title" content="GeoQuest â€” Das Geografie-Quiz">
<meta property="og:description" content="Flags, Kennzeichen, HauptstÃ¤dte â€” teste dein Geografie-Wissen kostenlos!">
<meta property="og:type" content="website">
<meta name="theme-color" content="#10b981">
<meta name="keywords" content="Geografie Quiz, LÃ¤nder Quiz, Flaggen Quiz, Kennzeichen Quiz, GeoQuest">
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
.scr{width:100%;max-width:420px}
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
.btn-cancel{background:transparent;border:1.5px solid var(--border);color:var(--text3);border-radius:8px;padding:3px 10px;font-size:.78rem;font-weight:700;cursor:pointer}
.btn-cancel:hover{color:#f87171;border-color:#f87171}
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
/* Phase 86 â€” Logik-Gitter */
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
/* Phase 86 â€” Reiseroute */
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

/* Phase 27 â€” Auth Card */
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

/* Phase 30 â€” Higher/Lower cards */
.hl-wrap{display:flex;align-items:center;justify-content:center;gap:10px;margin:10px 0 6px;flex-wrap:nowrap}
.hl-card{background:var(--bg3);border:2px solid var(--border);border-radius:14px;padding:.7rem .9rem;text-align:center;min-width:110px;max-width:180px;flex:1;transition:border-color .25s}
.hl-card.hl-known{border-color:#10b981}
.hl-card.hl-hidden{border-color:var(--border);opacity:.85}
.hl-card.hl-revealed{border-color:#3b82f6;opacity:1}
.hl-name{font-weight:900;font-size:1.35rem;color:var(--text);margin-bottom:.3rem;word-break:break-word;overflow-wrap:break-word;line-height:1.2}
.hl-val{color:#10b981;font-size:1.05rem;font-weight:700}
.hl-hidden .hl-val{color:var(--text3);font-size:1.4rem}
.hl-vs{font-size:1.5rem;flex-shrink:0;color:var(--text3)}
/* Phase 30 â€” Survival diff button */
.diff-btn.active[onclick*="survival"]{background:#7f1d1d;color:#fca5a5;border-color:#ef4444}

/* Phase 33 â€” Multiplayer */
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
  touch-action:pan-x pan-y;margin-bottom:.5rem}
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
  /* 4 Antworten â†’ 2Ã—2 Grid auf PC */
  .answers:not(.two-opts):not(.flag-grid){display:grid;grid-template-columns:1fr 1fr;gap:9px}
  /* 2 Antworten â†’ nebeneinander */
  .answers.two-opts{display:flex;flex-direction:row;gap:9px}
  .hud{max-width:840px;margin-left:auto;margin-right:auto}
  .tbar{max-width:840px;margin-left:auto;margin-right:auto}
  .pu-bar{max-width:840px;margin-left:auto;margin-right:auto}
  /* Karte: volle HÃ¶he */
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
print(f'Written: {len(HTML):,} chars â†’ {out}')
# Also write index.html for Netlify / direct hosting
with open('index.html', 'w', encoding='utf-8') as _f:
    _f.write(HTML)
print('Also written \u2192 index.html (Netlify deploy target)')



