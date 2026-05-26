#!/usr/bin/env python3
# enrich_tiere_part1.py — Phase 227 Step 2
# Injects:
#   1. KULTUR_DATA entries for 10 Pin modes (with real lat/lng)
#   2. TIER_HL_DATA object for 11 H/L modes (with real numeric values)
#   3. genTiereHL() generator function (La-Paz windowing + parseFloat)
#   4. GEN dispatch entries for all 21 tiere modes

SRC = "/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py"

with open(SRC, "r", encoding="utf-8") as f:
    content = f.read()

# ══════════════════════════════════════════════════════════════════════════════
# BLOCK A: KULTUR_DATA entries for Pin modes
# Insert BEFORE the closing "  /* === Phase 216: Match-Kategorien" comment
# ══════════════════════════════════════════════════════════════════════════════

KULTUR_ANCHOR = "  /* === Phase 216: Match-Kategorien (Schritt 3) === */"

TIERE_KULTUR_DATA = """  /* === Phase 227: Tiere & Natur — Pin-Datensätze (10 Modi) === */

  /* 1. Endemische Arten (exklusive Lebensräume) */
  tiere_endemisch:[
    {n:"Lemur (Madagaskar)",lat:-19.0,lng:47.0},
    {n:"Kiwi (Neuseeland)",lat:-40.9,lng:174.9},
    {n:"Komodo-Waran",lat:-8.55,lng:119.49},
    {n:"Axolotl (Xochimilco)",lat:19.28,lng:-99.1},
    {n:"Galapagos-Schildkröte",lat:-0.68,lng:-91.0},
    {n:"Kakapo (Neuseeland)",lat:-45.5,lng:167.5},
    {n:"Nasenaffe (Borneo)",lat:1.5,lng:110.3},
    {n:"Schneeleopard (Zentralasien)",lat:40.0,lng:72.0},
    {n:"Quetzal (Guatemala)",lat:15.0,lng:-90.4},
    {n:"Wombat (Australien)",lat:-32.0,lng:147.0},
    {n:"Fossa (Madagaskar)",lat:-20.0,lng:44.5},
    {n:"Tasmanian Devil",lat:-42.0,lng:146.5},
    {n:"Orang-Utan (Borneo)",lat:1.0,lng:114.0},
    {n:"Klippschliefer (Südafrika)",lat:-30.5,lng:23.5},
    {n:"Sumatra-Nashorn",lat:3.6,lng:102.0},
    {n:"Siamang-Gibbon (Sumatra)",lat:-1.5,lng:101.5},
    {n:"Weißkopf-Seeadler (Alaska)",lat:61.0,lng:-149.0},
    {n:"Kondor (Anden)",lat:-15.0,lng:-70.0},
    {n:"Riesenschildkröte (Aldabra)",lat:-9.4,lng:46.3},
    {n:"Kaiman (Pantanal)",lat:-17.0,lng:-57.0}
  ],

  /* 2. Big Five Nationalparks */
  tiere_bigfive:[
    {n:"Serengeti NP (Tansania)",lat:-2.33,lng:34.83},
    {n:"Kruger NP (Südafrika)",lat:-23.99,lng:31.55},
    {n:"Masai Mara (Kenia)",lat:-1.5,lng:35.15},
    {n:"Amboseli NP (Kenia)",lat:-2.65,lng:37.26},
    {n:"Chobe NP (Botswana)",lat:-18.06,lng:24.48},
    {n:"Hwange NP (Simbabwe)",lat:-19.0,lng:26.5},
    {n:"Etosha NP (Namibia)",lat:-18.85,lng:16.33},
    {n:"Kafue NP (Sambia)",lat:-14.5,lng:25.9},
    {n:"South Luangwa (Sambia)",lat:-13.08,lng:31.79},
    {n:"Ruaha NP (Tansania)",lat:-7.5,lng:34.5},
    {n:"Ngorongoro (Tansania)",lat:-3.22,lng:35.5},
    {n:"Okavango Delta (Botswana)",lat:-19.3,lng:22.9},
    {n:"Tsavo NP (Kenia)",lat:-2.98,lng:38.5},
    {n:"Mikumi NP (Tansania)",lat:-7.4,lng:37.1},
    {n:"Gonarezhou (Simbabwe)",lat:-21.5,lng:32.5},
    {n:"Selous GR (Tansania)",lat:-9.0,lng:37.8},
    {n:"Addo Elephant Park (SA)",lat:-33.5,lng:25.75},
    {n:"Moremi GR (Botswana)",lat:-19.15,lng:23.16},
    {n:"Liwonde NP (Malawi)",lat:-14.8,lng:35.3},
    {n:"Kgalagadi TP (Botswana)",lat:-25.5,lng:21.0}
  ],

  /* 3. Großkatzen-Habitate */
  tiere_grosskatzen:[
    {n:"Bengalischer Tiger (Sundarbans)",lat:21.9,lng:89.2},
    {n:"Sibirischer Tiger (Ussuri)",lat:44.5,lng:134.0},
    {n:"Sumatra-Tiger",lat:0.5,lng:102.0},
    {n:"Jaguar (Pantanal)",lat:-16.0,lng:-56.5},
    {n:"Jaguar (Amazonas)",lat:-3.0,lng:-60.0},
    {n:"Schneeleopard (Hindukusch)",lat:37.0,lng:71.0},
    {n:"Schneeleopard (Altai)",lat:49.5,lng:88.5},
    {n:"Afrikanischer Löwe (Serengeti)",lat:-2.5,lng:35.0},
    {n:"Gepard (Namibia)",lat:-22.0,lng:18.0},
    {n:"Gepard (Kenia)",lat:-1.5,lng:37.0},
    {n:"Puma (Patagonien)",lat:-51.0,lng:-73.0},
    {n:"Nebelparder (Borneo)",lat:4.0,lng:117.0},
    {n:"Persischer Leopard (Kaukasus)",lat:41.0,lng:46.0},
    {n:"Amurleopard (Primorje)",lat:43.0,lng:133.0},
    {n:"Löwe (Gir-Wald/Indien)",lat:21.0,lng:70.8},
    {n:"Ozelot (Costa Rica)",lat:10.0,lng:-83.5},
    {n:"Serval (Ostafrika)",lat:0.0,lng:36.0},
    {n:"Irbis (Mongolei)",lat:46.0,lng:102.0},
    {n:"Tigerquoll (Australien)",lat:-37.0,lng:149.0},
    {n:"Cheetah (Namibia, Cheetah Conservation Fund)",lat:-20.5,lng:17.2}
  ],

  /* 4. Invasive Arten — Ursprungsland */
  tiere_invasiv:[
    {n:"Nilkampfkröte (Bufo marinus) → Südamerika",lat:-10.0,lng:-55.0},
    {n:"Mink (Nordamerika) → Nordamerika",lat:50.0,lng:-90.0},
    {n:"Hauskatze → Naher Osten",lat:36.0,lng:36.0},
    {n:"Riesenpython (Everglades) → Südostasien",lat:5.0,lng:103.0},
    {n:"Grauhörnchen → Nordamerika",lat:40.0,lng:-80.0},
    {n:"Nil-Barsch (Victoriasee) → Nil",lat:20.0,lng:32.0},
    {n:"Kudzu-Käfer → China/Japan",lat:35.0,lng:115.0},
    {n:"Asiatische Hornisse → China",lat:30.0,lng:110.0},
    {n:"Riesenschildkröte → Indischer Ozean",lat:-10.0,lng:55.0},
    {n:"Gambusie (Mosquitofish) → USA",lat:32.0,lng:-92.0},
    {n:"Strigops-Papagei (NZ) → Neuseeland",lat:-45.0,lng:168.0},
    {n:"Karibischer Rotfeuerfisch → Atlantik urspr. Pazifik",lat:20.0,lng:135.0},
    {n:"Chinesischer Wollhandkrabbe → Ostasien",lat:32.0,lng:121.0},
    {n:"Nutria → Südamerika",lat:-35.0,lng:-58.0},
    {n:"Stachelschwein (Europa) → Nordafrika/Asien",lat:35.0,lng:10.0},
    {n:"Gelbwange-Schmuckschildkröte → Nordamerika",lat:32.0,lng:-91.0},
    {n:"Asiatischer Marienkäfer → Ostasien",lat:35.0,lng:108.0},
    {n:"Alpenstrandläufer (exot.) → Arktis",lat:72.0,lng:25.0},
    {n:"Karpfen (Asien) → Asien",lat:35.0,lng:110.0},
    {n:"Forelle (Ozeanien) → Europa",lat:47.0,lng:10.0}
  ],

  /* 5. Vogelzug-Knotenpunkte */
  tiere_vogelzug:[
    {n:"Bosphorus (Istanbul)",lat:41.1,lng:29.05},
    {n:"Falsterbo (Schweden)",lat:55.38,lng:12.82},
    {n:"Eilat (Israel)",lat:29.55,lng:34.95},
    {n:"Batumi (Georgien)",lat:41.65,lng:41.63},
    {n:"Gibraltar (Straße)",lat:35.98,lng:-5.47},
    {n:"Point Pelee (Kanada)",lat:41.95,lng:-82.52},
    {n:"Hawk Mountain (Pennsylvania)",lat:40.64,lng:-75.99},
    {n:"Darién (Panama)",lat:8.5,lng:-77.5},
    {n:"Gulf of Suez",lat:29.5,lng:32.6},
    {n:"Qinghai-See (China)",lat:36.9,lng:100.2},
    {n:"Barr al Hikman (Oman)",lat:22.5,lng:59.0},
    {n:"Bay of Fundy (Kanada)",lat:45.1,lng:-66.1},
    {n:"Camargue (Frankreich)",lat:43.5,lng:4.5},
    {n:"Neusiedler See (Österreich)",lat:47.85,lng:16.77},
    {n:"Cerro de la Muerte (Costa Rica)",lat:9.55,lng:-83.75},
    {n:"Veracruz (Mexiko)",lat:19.17,lng:-96.13},
    {n:"Natal (Brasilien)",lat:-5.79,lng:-35.21},
    {n:"Elat-Wüste (Negev)",lat:30.6,lng:35.1},
    {n:"Chittagong (Bangladesch)",lat:22.34,lng:91.83},
    {n:"Nile Delta Wetlands",lat:31.3,lng:31.2}
  ],

  /* 6. Ursprung der Haustiere — Domestizierungsort */
  tiere_haustiere:[
    {n:"Hund (Wolf-Domestizierung, Zentralasien)",lat:45.0,lng:65.0},
    {n:"Katze (Fruchtbarer Halbmond)",lat:35.0,lng:38.0},
    {n:"Pferd (Kasachstan, Botai)",lat:52.5,lng:62.5},
    {n:"Rind (Anatolien/Naher Osten)",lat:37.5,lng:40.0},
    {n:"Schaf (Zagros-Gebirge)",lat:34.0,lng:47.0},
    {n:"Ziege (Zagros-Gebirge)",lat:33.5,lng:46.5},
    {n:"Schwein (Anatolien + China)",lat:36.0,lng:36.0},
    {n:"Huhn (Südostasien/Indochina)",lat:16.0,lng:104.0},
    {n:"Ente (China)",lat:30.0,lng:116.0},
    {n:"Kamel (Arabische Halbinsel)",lat:23.0,lng:46.0},
    {n:"Lama/Alpaka (Anden, Peru)",lat:-14.0,lng:-75.0},
    {n:"Esel (Nordostafrika)",lat:14.0,lng:38.0},
    {n:"Wasserbüffel (Indus-Tal)",lat:26.0,lng:72.0},
    {n:"Yak (Tibet)",lat:30.0,lng:90.0},
    {n:"Truthahn (Mesoamerika)",lat:19.0,lng:-97.0},
    {n:"Rentier (Sibirien)",lat:62.0,lng:100.0},
    {n:"Biene (Naher Osten/Ostafrika)",lat:15.0,lng:36.0},
    {n:"Goldfisch (China)",lat:30.0,lng:118.0},
    {n:"Kanarienvogel (Kanarische Inseln)",lat:28.0,lng:-15.5},
    {n:"Seidenraupe (China)",lat:31.0,lng:108.0}
  ],

  /* 7. Nationaltiere Pin */
  tiere_nationaltier_pin:[
    {n:"Känguru → Australien",lat:-25.0,lng:134.0},
    {n:"Riesenpanda → China",lat:31.0,lng:104.0},
    {n:"Bengal-Tiger → Indien",lat:20.0,lng:80.0},
    {n:"Weißkopfseeadler → USA",lat:40.0,lng:-100.0},
    {n:"Biber → Kanada",lat:60.0,lng:-96.0},
    {n:"Springbok → Südafrika",lat:-29.0,lng:25.0},
    {n:"Schneeleopard → Pakistan",lat:30.0,lng:70.0},
    {n:"Kiwi (Vogel) → Neuseeland",lat:-42.0,lng:172.0},
    {n:"Elch → Norwegen",lat:65.0,lng:14.0},
    {n:"Jaguar → Brasilien",lat:-10.0,lng:-55.0},
    {n:"Löwe → Vereinigtes Königreich",lat:54.0,lng:-2.0},
    {n:"Braunbär → Russland",lat:60.0,lng:80.0},
    {n:"Weißer Elefant → Thailand",lat:15.0,lng:101.0},
    {n:"Adler → Deutschland",lat:51.0,lng:10.0},
    {n:"Hahn (Gaulois) → Frankreich",lat:46.0,lng:2.0},
    {n:"Dhol (Rothund) → Indien (alternativ)",lat:22.0,lng:78.0},
    {n:"Steinadler → Mexiko",lat:23.0,lng:-102.0},
    {n:"Totenkopfäffchen → Bolivien",lat:-16.0,lng:-64.0},
    {n:"Alpensteinbock → Schweiz",lat:47.0,lng:8.0},
    {n:"Stier → Spanien",lat:40.0,lng:-4.0}
  ],

  /* 8. Primaten-Zentren (Regenwald der Menschenaffen) */
  tiere_primaten:[
    {n:"Virunga (Gorilla, Kongo/Ruanda)",lat:-1.5,lng:29.5},
    {n:"Bwindi (Gorilla, Uganda)",lat:-1.1,lng:29.7},
    {n:"Gombe (Schimpanse, Tansania)",lat:-4.67,lng:29.63},
    {n:"Tai Forest (Schimpanse, Elfenbeinküste)",lat:5.85,lng:-7.23},
    {n:"Gunung Leuser (Orang-Utan, Sumatra)",lat:3.9,lng:97.5},
    {n:"Tanjung Puting (Orang-Utan, Borneo)",lat:-2.7,lng:111.9},
    {n:"Danum Valley (Borneo)",lat:4.96,lng:117.8},
    {n:"Atapuerca (Fossil, Spanien)",lat:42.37,lng:-3.52},
    {n:"Amazon Primates (Peru)",lat:-4.0,lng:-73.0},
    {n:"Ranomafana (Lemuren, Madagaskar)",lat:-21.26,lng:47.44},
    {n:"Andasibe (Indri-Lemur, Madagaskar)",lat:-19.0,lng:48.4},
    {n:"Kibale (Schimpanse, Uganda)",lat:0.5,lng:30.36},
    {n:"Mahale Mts (Schimpanse, Tansania)",lat:-6.2,lng:29.8},
    {n:"Lopé NP (Gorilla, Gabun)",lat:-0.2,lng:11.5},
    {n:"Kinabalu (Orang-Utan, Malaysia)",lat:6.08,lng:116.55},
    {n:"Atlantic Forest (Brüllaffe, Brasilien)",lat:-20.0,lng:-43.0},
    {n:"Hainan (Gibbon, China)",lat:19.0,lng:109.5},
    {n:"Afi Mountain (Cross-River-Gorilla, Nigeria)",lat:6.3,lng:9.0},
    {n:"Sichuan (Riesenpanda, China)",lat:30.5,lng:103.0},
    {n:"Mengla (Gibbon, Yunnan/China)",lat:21.5,lng:101.5}
  ],

  /* 9. Hai-Angriff-Hotspots */
  tiere_hai:[
    {n:"New Smyrna Beach (Florida)",lat:29.03,lng:-80.93},
    {n:"Volusia County (Florida)",lat:29.1,lng:-81.05},
    {n:"Reunion Island (Frankreich)",lat:-21.1,lng:55.6},
    {n:"Shark Bay (Australien)",lat:-25.5,lng:113.5},
    {n:"Western Australia (Kalbarri)",lat:-27.7,lng:114.2},
    {n:"KwaZulu-Natal (Südafrika)",lat:-29.5,lng:31.2},
    {n:"Bahamas (Tiger Beach)",lat:25.5,lng:-79.2},
    {n:"Recife (Brasilien)",lat:-8.07,lng:-34.88},
    {n:"Gansbaai (Großer Weißer, SA)",lat:-34.58,lng:19.35},
    {n:"Makena Beach (Hawaii)",lat:20.63,lng:-156.44},
    {n:"Guadalupe Island (Mexiko)",lat:29.0,lng:-118.3},
    {n:"Aliwal Shoal (Südafrika)",lat:-30.3,lng:30.85},
    {n:"Réunion (Saint-Gilles)",lat:-21.05,lng:55.23},
    {n:"Queenscliff (Australien)",lat:-38.27,lng:144.66},
    {n:"Coffin Bay (Australien)",lat:-34.63,lng:135.46},
    {n:"Port St. Johns (Südafrika)",lat:-31.63,lng:29.54},
    {n:"Red Sea (Ägypten/Sharm el-Sheikh)",lat:27.86,lng:34.28},
    {n:"Turks & Caicos",lat:21.8,lng:-72.3},
    {n:"New South Wales (Australien)",lat:-33.5,lng:151.5},
    {n:"Lord Howe Island (Australien)",lat:-31.55,lng:159.08}
  ],

  /* 10. Bären-Verteilung (Reviere) */
  tiere_baeren:[
    {n:"Eisbär (Spitzbergen)",lat:78.5,lng:16.0},
    {n:"Eisbär (Hudson Bay, Kanada)",lat:60.0,lng:-85.0},
    {n:"Eisbär (Alaska/Beaufort Sea)",lat:72.0,lng:-150.0},
    {n:"Grizzly (Yellowstone)",lat:44.5,lng:-110.5},
    {n:"Grizzly (British Columbia)",lat:51.0,lng:-123.0},
    {n:"Braunbär (Sibirien)",lat:58.0,lng:90.0},
    {n:"Braunbär (Kamtschatka)",lat:54.0,lng:160.0},
    {n:"Braunbär (Skandinavien)",lat:65.0,lng:15.0},
    {n:"Braunbär (Karpaten)",lat:46.0,lng:25.0},
    {n:"Riesenpanda (Sichuan, China)",lat:30.5,lng:103.0},
    {n:"Lippenbär (Sri Lanka)",lat:8.0,lng:80.5},
    {n:"Lippenbär (Indien, Deccan)",lat:18.0,lng:78.0},
    {n:"Malaienbär (Borneo)",lat:3.0,lng:115.0},
    {n:"Malaienbär (Sumatra)",lat:0.0,lng:102.0},
    {n:"Brillenbär (Kolumbien)",lat:5.0,lng:-76.0},
    {n:"Brillenbär (Peru, Anden)",lat:-10.0,lng:-75.0},
    {n:"Schwarzbär (Florida)",lat:29.0,lng:-81.5},
    {n:"Schwarzbär (Appalachen)",lat:37.0,lng:-82.0},
    {n:"Asienbär (Japan, Honshu)",lat:35.5,lng:136.5},
    {n:"Kragenbär (Korea)",lat:38.0,lng:128.0}
  ],

  /* === Phase 227 Ende Tiere Pin-Daten === */
  """ + KULTUR_ANCHOR[2:]  # keep the original comment

# Actually just insert before the anchor
TIERE_KULTUR_INSERT = """  /* === Phase 227: Tiere & Natur — Pin-Datensätze (10 Modi) === */

  /* 1. Endemische Arten */
  tiere_endemisch:[
    {n:"Lemur (Madagaskar)",lat:-19.0,lng:47.0},
    {n:"Kiwi (Neuseeland)",lat:-40.9,lng:174.9},
    {n:"Komodo-Waran",lat:-8.55,lng:119.49},
    {n:"Axolotl (Xochimilco)",lat:19.28,lng:-99.1},
    {n:"Galapagos-Schildkröte",lat:-0.68,lng:-91.0},
    {n:"Kakapo (Neuseeland)",lat:-45.5,lng:167.5},
    {n:"Nasenaffe (Borneo)",lat:1.5,lng:110.3},
    {n:"Schneeleopard (Himalaya)",lat:28.5,lng:84.0},
    {n:"Quetzal (Guatemala)",lat:15.0,lng:-90.4},
    {n:"Wombat (Australien)",lat:-32.0,lng:147.0},
    {n:"Fossa (Madagaskar)",lat:-20.0,lng:44.5},
    {n:"Tasmanian Devil",lat:-42.0,lng:146.5},
    {n:"Orang-Utan (Borneo)",lat:1.0,lng:114.0},
    {n:"Sumatra-Nashorn",lat:3.6,lng:102.0},
    {n:"Weißkopf-Seeadler (Alaska)",lat:61.0,lng:-149.0},
    {n:"Kondor (Anden)",lat:-15.0,lng:-70.0},
    {n:"Riesenschildkröte (Aldabra)",lat:-9.4,lng:46.3},
    {n:"Kaiman (Pantanal)",lat:-17.0,lng:-57.0},
    {n:"Nashorn-Chamäleon (Kamerun)",lat:5.0,lng:10.5},
    {n:"Przewalski-Pferd (Mongolei)",lat:47.0,lng:102.0}
  ],

  /* 2. Big Five Nationalparks */
  tiere_bigfive:[
    {n:"Serengeti NP (Tansania)",lat:-2.33,lng:34.83},
    {n:"Kruger NP (Südafrika)",lat:-23.99,lng:31.55},
    {n:"Masai Mara (Kenia)",lat:-1.5,lng:35.15},
    {n:"Amboseli NP (Kenia)",lat:-2.65,lng:37.26},
    {n:"Chobe NP (Botswana)",lat:-18.06,lng:24.48},
    {n:"Hwange NP (Simbabwe)",lat:-19.0,lng:26.5},
    {n:"Etosha NP (Namibia)",lat:-18.85,lng:16.33},
    {n:"South Luangwa (Sambia)",lat:-13.08,lng:31.79},
    {n:"Ruaha NP (Tansania)",lat:-7.5,lng:34.5},
    {n:"Ngorongoro (Tansania)",lat:-3.22,lng:35.5},
    {n:"Okavango Delta (Botswana)",lat:-19.3,lng:22.9},
    {n:"Tsavo NP (Kenia)",lat:-2.98,lng:38.5},
    {n:"Gonarezhou (Simbabwe)",lat:-21.5,lng:32.5},
    {n:"Selous GR (Tansania)",lat:-9.0,lng:37.8},
    {n:"Addo Elephant Park (SA)",lat:-33.5,lng:25.75},
    {n:"Moremi GR (Botswana)",lat:-19.15,lng:23.16},
    {n:"Kgalagadi TP (Botswana/SA)",lat:-25.5,lng:21.0},
    {n:"Kafue NP (Sambia)",lat:-14.5,lng:25.9},
    {n:"Liwonde NP (Malawi)",lat:-14.8,lng:35.3},
    {n:"Mikumi NP (Tansania)",lat:-7.4,lng:37.1}
  ],

  /* 3. Großkatzen-Habitate */
  tiere_grosskatzen:[
    {n:"Bengalischer Tiger (Sundarbans)",lat:21.9,lng:89.2},
    {n:"Sibirischer Tiger (Ussuri-Region)",lat:44.5,lng:134.0},
    {n:"Sumatra-Tiger (Gunung Leuser)",lat:3.9,lng:97.5},
    {n:"Jaguar (Pantanal, Brasilien)",lat:-16.0,lng:-56.5},
    {n:"Jaguar (Amazonas)",lat:-3.0,lng:-60.0},
    {n:"Schneeleopard (Hindukusch)",lat:37.0,lng:71.0},
    {n:"Schneeleopard (Mongolei)",lat:46.0,lng:102.0},
    {n:"Afrikanischer Löwe (Serengeti)",lat:-2.5,lng:35.0},
    {n:"Gepard (Namibia)",lat:-22.0,lng:18.0},
    {n:"Puma (Patagonien)",lat:-51.0,lng:-73.0},
    {n:"Nebelparder (Borneo)",lat:4.0,lng:117.0},
    {n:"Persischer Leopard (Kaukasus)",lat:41.0,lng:46.0},
    {n:"Amurleopard (Primorje, Russland)",lat:43.0,lng:133.0},
    {n:"Asiatischer Löwe (Gir-Wald, Indien)",lat:21.0,lng:70.8},
    {n:"Ozelot (Costa Rica)",lat:10.0,lng:-83.5},
    {n:"Jaguarundi (Mexiko)",lat:20.0,lng:-100.0},
    {n:"Irbis (Altai, Mongolei)",lat:48.0,lng:95.0},
    {n:"Bergpuma (Andes, Kolumbien)",lat:3.0,lng:-74.0},
    {n:"Karakal (Zentralasien)",lat:40.0,lng:60.0},
    {n:"Afrikanischer Leopard (Kongo)",lat:-1.0,lng:24.0}
  ],

  /* 4. Invasive Arten — Ursprungsland */
  tiere_invasiv:[
    {n:"Rohrkröte (Cane Toad) → Südamerika",lat:-10.0,lng:-55.0},
    {n:"Riesenpython (Everglades) → Südostasien",lat:5.0,lng:103.0},
    {n:"Grauhörnchen → Nordamerika",lat:40.0,lng:-80.0},
    {n:"Nil-Barsch (Victoriasee) → Nilregion",lat:20.0,lng:32.0},
    {n:"Asiatische Hornisse → China",lat:30.0,lng:110.0},
    {n:"Rotfeuerfisch → Pazifik/Indischer Ozean",lat:20.0,lng:135.0},
    {n:"Chinesische Wollhandkrabbe → Ostasien",lat:32.0,lng:121.0},
    {n:"Nutria → Südamerika",lat:-35.0,lng:-58.0},
    {n:"Goldfisch (verwilderter) → China",lat:30.0,lng:118.0},
    {n:"Gelbwangen-Schmuckschildkröte → Nordamerika",lat:32.0,lng:-91.0},
    {n:"Hauskatze (Australien) → Naher Osten",lat:36.0,lng:36.0},
    {n:"Europäischer Aal (Neuseeland) → Europa",lat:52.0,lng:9.0},
    {n:"Mink (Großbritannien) → Nordamerika",lat:50.0,lng:-90.0},
    {n:"Asiatischer Marienkäfer → Ostasien",lat:35.0,lng:108.0},
    {n:"Karpfen (Australien) → Zentralasien",lat:42.0,lng:62.0},
    {n:"Forelle (Neuseeland) → Europa",lat:47.0,lng:10.0},
    {n:"Stachelschwanzleguane → Mittelamerika",lat:14.0,lng:-87.0},
    {n:"Amerikanischer Nerz (Europa) → Nordamerika",lat:50.0,lng:-90.0},
    {n:"Springbok (Südaustralien) → Südafrika",lat:-30.0,lng:24.0},
    {n:"Hausratte (Weltweit) → Südasien",lat:25.0,lng:78.0}
  ],

  /* 5. Vogelzug-Knotenpunkte */
  tiere_vogelzug:[
    {n:"Bosphorus (Istanbul, Türkei)",lat:41.1,lng:29.05},
    {n:"Falsterbo (Schweden)",lat:55.38,lng:12.82},
    {n:"Eilat (Israel, Roter See)",lat:29.55,lng:34.95},
    {n:"Batumi (Georgien)",lat:41.65,lng:41.63},
    {n:"Straße von Gibraltar",lat:35.98,lng:-5.47},
    {n:"Point Pelee (Ontario, Kanada)",lat:41.95,lng:-82.52},
    {n:"Hawk Mountain (Pennsylvania)",lat:40.64,lng:-75.99},
    {n:"Darién-Enge (Panama)",lat:8.5,lng:-77.5},
    {n:"Qinghai-See (China)",lat:36.9,lng:100.2},
    {n:"Camargue (Frankreich)",lat:43.5,lng:4.5},
    {n:"Neusiedler See (Österreich)",lat:47.85,lng:16.77},
    {n:"Veracruz (Mexiko, Adlerroute)",lat:19.17,lng:-96.13},
    {n:"Natal (Brasilien, Zugziel)",lat:-5.79,lng:-35.21},
    {n:"Nile Delta Wetlands (Ägypten)",lat:31.3,lng:31.2},
    {n:"Barr al Hikman (Oman)",lat:22.5,lng:59.0},
    {n:"Bay of Fundy (Kanada)",lat:45.1,lng:-66.1},
    {n:"Chukchi-Halbinsel (Russland)",lat:65.0,lng:-173.0},
    {n:"Cerro de la Muerte (Costa Rica)",lat:9.55,lng:-83.75},
    {n:"Wadden Sea (Nordsee)",lat:53.3,lng:8.5},
    {n:"Bretagne (Frankreich, Seevögel)",lat:48.5,lng:-4.0}
  ],

  /* 6. Ursprung der Haustiere */
  tiere_haustiere:[
    {n:"Hund (Wolf-Domestizierung)",lat:45.0,lng:65.0},
    {n:"Katze (Fruchtbarer Halbmond)",lat:35.0,lng:38.0},
    {n:"Pferd (Kasachstan, Botai-Kultur)",lat:52.5,lng:62.5},
    {n:"Rind (Anatolien/Naher Osten)",lat:37.5,lng:40.0},
    {n:"Schaf (Zagros-Gebirge, Iran)",lat:34.0,lng:47.0},
    {n:"Ziege (Zagros-Gebirge, Iran)",lat:33.5,lng:46.5},
    {n:"Schwein (Anatolien)",lat:36.0,lng:36.0},
    {n:"Haushuhn (Südostasien)",lat:16.0,lng:104.0},
    {n:"Ente (China)",lat:30.0,lng:116.0},
    {n:"Dromedar (Arabische Halbinsel)",lat:23.0,lng:46.0},
    {n:"Lama (Peruanische Anden)",lat:-14.0,lng:-75.0},
    {n:"Esel (Nordostafrika)",lat:14.0,lng:38.0},
    {n:"Wasserbüffel (Indus-Tal)",lat:26.0,lng:72.0},
    {n:"Yak (Tibetisches Hochland)",lat:30.0,lng:90.0},
    {n:"Truthahn (Mesoamerika, Mexiko)",lat:19.0,lng:-97.0},
    {n:"Rentier (Sibirien)",lat:62.0,lng:100.0},
    {n:"Hausente (China)",lat:30.0,lng:116.0},
    {n:"Goldfisch (China, Song-Dynastie)",lat:30.0,lng:118.0},
    {n:"Kanarienvogel (Kanarische Inseln)",lat:28.0,lng:-15.5},
    {n:"Seidenraupe (Gelbes-Fluss-Tal, China)",lat:34.0,lng:109.0}
  ],

  /* 7. Nationaltiere Pin */
  tiere_nationaltier_pin:[
    {n:"Känguru → Australien",lat:-25.0,lng:134.0},
    {n:"Riesenpanda → China",lat:31.0,lng:104.0},
    {n:"Bengal-Tiger → Indien",lat:20.0,lng:80.0},
    {n:"Weißkopfseeadler → USA",lat:40.0,lng:-100.0},
    {n:"Biber → Kanada",lat:60.0,lng:-96.0},
    {n:"Springbok → Südafrika",lat:-29.0,lng:25.0},
    {n:"Schneeleopard → Pakistan",lat:30.0,lng:70.0},
    {n:"Kiwi → Neuseeland",lat:-42.0,lng:172.0},
    {n:"Elch → Norwegen",lat:65.0,lng:14.0},
    {n:"Jaguar → Brasilien",lat:-10.0,lng:-55.0},
    {n:"Löwe → Vereinigtes Königreich",lat:54.0,lng:-2.0},
    {n:"Braunbär → Russland",lat:60.0,lng:80.0},
    {n:"Weißer Elefant → Thailand",lat:15.0,lng:101.0},
    {n:"Adler → Deutschland",lat:51.0,lng:10.0},
    {n:"Gaulois-Hahn → Frankreich",lat:46.0,lng:2.0},
    {n:"Steinadler → Mexiko",lat:23.0,lng:-102.0},
    {n:"Alpensteinbock → Schweiz",lat:47.0,lng:8.0},
    {n:"Stier (Osborne) → Spanien",lat:40.0,lng:-4.0},
    {n:"Weißer Falke → UAE",lat:24.0,lng:54.5},
    {n:"Turul-Vogel → Ungarn",lat:47.0,lng:19.0}
  ],

  /* 8. Primaten-Zentren */
  tiere_primaten:[
    {n:"Virunga (Gorilla, Kongo/Ruanda)",lat:-1.5,lng:29.5},
    {n:"Bwindi NP (Berggorilla, Uganda)",lat:-1.1,lng:29.7},
    {n:"Gombe Stream (Schimpanse, Tansania)",lat:-4.67,lng:29.63},
    {n:"Taï Forest (Schimpanse, Elfenbeinküste)",lat:5.85,lng:-7.23},
    {n:"Gunung Leuser (Orang-Utan, Sumatra)",lat:3.9,lng:97.5},
    {n:"Tanjung Puting (Orang-Utan, Borneo)",lat:-2.7,lng:111.9},
    {n:"Danum Valley (Borneo)",lat:4.96,lng:117.8},
    {n:"Ranomafana (Indri-Lemur, Madagaskar)",lat:-21.26,lng:47.44},
    {n:"Kibale NP (Schimpanse, Uganda)",lat:0.5,lng:30.36},
    {n:"Mahale Mts (Schimpanse, Tansania)",lat:-6.2,lng:29.8},
    {n:"Lopé NP (Gorilla, Gabun)",lat:-0.2,lng:11.5},
    {n:"Atlantic Forest (Brüllaffe, Brasilien)",lat:-20.0,lng:-43.0},
    {n:"Hainan (Gibbon, China)",lat:19.0,lng:109.5},
    {n:"Afi Mountain (Cross-River-Gorilla, Nigeria)",lat:6.3,lng:9.0},
    {n:"Sichuan (Riesenpanda, China)",lat:30.5,lng:103.0},
    {n:"Amazon Basin (Brüllaffe, Peru)",lat:-4.0,lng:-73.0},
    {n:"Western Ghats (Löwenschwanzmakak, Indien)",lat:11.0,lng:76.5},
    {n:"Kinabalu (Borneo-Gibbon, Malaysia)",lat:6.08,lng:116.55},
    {n:"Mentawai-Inseln (Mentawai-Gibbon)",lat:-1.5,lng:99.5},
    {n:"Mengla (Hainan-Gibbon, Yunnan, China)",lat:21.5,lng:101.5}
  ],

  /* 9. Hai-Angriff-Hotspots */
  tiere_hai:[
    {n:"New Smyrna Beach (Florida, USA)",lat:29.03,lng:-80.93},
    {n:"Volusia County (Florida, USA)",lat:29.1,lng:-81.05},
    {n:"Réunion Island (Frankreich)",lat:-21.1,lng:55.6},
    {n:"Shark Bay (Westaustralien)",lat:-25.5,lng:113.5},
    {n:"Gansbaai (Weißer Hai, Südafrika)",lat:-34.58,lng:19.35},
    {n:"KwaZulu-Natal (Südafrika)",lat:-29.5,lng:31.2},
    {n:"Tiger Beach (Bahamas)",lat:25.5,lng:-79.2},
    {n:"Recife (Brasilien)",lat:-8.07,lng:-34.88},
    {n:"Makena Beach (Maui, Hawaii)",lat:20.63,lng:-156.44},
    {n:"Guadalupe Island (Mexiko)",lat:29.0,lng:-118.3},
    {n:"Coffin Bay (Südaustralien)",lat:-34.63,lng:135.46},
    {n:"Port St. Johns (Südafrika)",lat:-31.63,lng:29.54},
    {n:"Sharm el-Sheikh (Rotes Meer)",lat:27.86,lng:34.28},
    {n:"Lord Howe Island (Australien)",lat:-31.55,lng:159.08},
    {n:"Neptune Islands (Südaustralien)",lat:-35.3,lng:136.1},
    {n:"Ballina (New South Wales)",lat:-28.87,lng:153.57},
    {n:"Aliwal Shoal (Südafrika)",lat:-30.3,lng:30.85},
    {n:"Turks & Caicos",lat:21.8,lng:-72.3},
    {n:"Oahu (Hawaii, North Shore)",lat:21.6,lng:-158.05},
    {n:"Plettenberg Bay (Südafrika)",lat:-34.05,lng:23.37}
  ],

  /* 10. Bären-Verteilung */
  tiere_baeren:[
    {n:"Eisbär (Spitzbergen, Norwegen)",lat:78.5,lng:16.0},
    {n:"Eisbär (Churchill, Hudson Bay)",lat:58.8,lng:-94.2},
    {n:"Eisbär (Beaufort Sea, Alaska)",lat:72.0,lng:-150.0},
    {n:"Grizzly (Yellowstone, USA)",lat:44.5,lng:-110.5},
    {n:"Grizzly (British Columbia)",lat:51.0,lng:-123.0},
    {n:"Braunbär (Kamtschatka, Russland)",lat:54.0,lng:160.0},
    {n:"Braunbär (Skandinavien)",lat:65.0,lng:15.0},
    {n:"Braunbär (Karpaten, Rumänien)",lat:46.0,lng:25.0},
    {n:"Riesenpanda (Sichuan, China)",lat:30.5,lng:103.0},
    {n:"Lippenbär (Sri Lanka)",lat:8.0,lng:80.5},
    {n:"Lippenbär (Deccan, Indien)",lat:18.0,lng:78.0},
    {n:"Malaienbär (Borneo)",lat:3.0,lng:115.0},
    {n:"Brillenbär (Kolumbien)",lat:5.0,lng:-76.0},
    {n:"Brillenbär (Peru, Anden)",lat:-10.0,lng:-75.0},
    {n:"Schwarzbär (Appalachian Trail)",lat:37.0,lng:-82.0},
    {n:"Schwarzbär (Florida)",lat:29.0,lng:-81.5},
    {n:"Kragenbär (Mandschurei, China)",lat:44.0,lng:128.0},
    {n:"Kragenbär (Honshu, Japan)",lat:35.5,lng:136.5},
    {n:"Braunbär (Sibirien, Westsibirien)",lat:58.0,lng:80.0},
    {n:"Eisbär (Franz-Josef-Land, Russland)",lat:80.5,lng:52.0}
  ],

"""

KULTUR_ANCHOR_CHECK = "  /* === Phase 216: Match-Kategorien (Schritt 3) === */"

if KULTUR_ANCHOR_CHECK not in content:
    print("ERROR: KULTUR_DATA anchor not found – check gen.py")
    exit(1)

content = content.replace(
    KULTUR_ANCHOR_CHECK,
    TIERE_KULTUR_INSERT + "  /* === Phase 216: Match-Kategorien (Schritt 3) === */",
    1
)
print("✓ PATCH A: KULTUR_DATA pin entries added (10 modes × 20 entries)")

# ══════════════════════════════════════════════════════════════════════════════
# BLOCK B: TIER_HL_DATA object + genTiereHL() function
# Insert after the KULTUR_DATA block, before function genUniversalMatchQ
# ══════════════════════════════════════════════════════════════════════════════

GEN_MATCH_ANCHOR = "function genUniversalMatchQ(cat){"

TIER_HL_BLOCK = r"""/* === Phase 227: Tier-H/L Datensätze (11 Modi) === */
const TIER_HL_DATA={
  /* 1. Körpergewicht Landtiere (kg) */
  gewicht_land:{
    prompt:"Welches Landtier ist schwerer? (Körpergewicht)",unit:"kg",
    items:[
      {name:"Afrikanischer Elefant",val:6000},
      {name:"Nilpferd",val:2000},
      {name:"Weißes Nashorn",val:2300},
      {name:"Gaur (Wildrind)",val:1000},
      {name:"Wasserbüffel",val:700},
      {name:"Giraffe",val:800},
      {name:"Flusspferd",val:2000},
      {name:"Eisbär",val:500},
      {name:"Grizzlybär",val:360},
      {name:"Afrikanischer Löwe",val:190},
      {name:"Sibirischer Tiger",val:300},
      {name:"Gepard",val:65},
      {name:"Gorilla (Silberrücken)",val:200},
      {name:"Orang-Utan (Borneo)",val:87},
      {name:"Jaguar",val:100},
      {name:"Wapiti (Rothirsch)",val:330},
      {name:"Europäischer Wisent",val:900},
      {name:"Dromedar",val:600},
      {name:"Elan (Alaskavariante)",val:700},
      {name:"Hausrind",val:700}
    ]
  },
  /* 2. Körpergewicht Meerestiere (kg) */
  gewicht_meer:{
    prompt:"Welches Meerestier ist schwerer? (Körpergewicht)",unit:"kg",
    items:[
      {name:"Blauwal",val:150000},
      {name:"Finnwal",val:70000},
      {name:"Buckelwal",val:30000},
      {name:"Pottwahl",val:45000},
      {name:"Orca (Schwertwahl)",val:6000},
      {name:"Walross",val:1700},
      {name:"Südlicher See-Elefant",val:2500},
      {name:"Weißer Hai",val:1100},
      {name:"Walhai",val:18000},
      {name:"Riesenoktopus",val:15},
      {name:"Atlantischer Blauflossen-Thunfisch",val:450},
      {name:"Schwertfisch",val:540},
      {name:"Beluga-Stör",val:1000},
      {name:"Rochen (Ozeanischer Mantarochen)",val:3000},
      {name:"Sattelrobbe",val:130},
      {name:"Seehund",val:130},
      {name:"Delphin (Tümmler)",val:300},
      {name:"Nilkrokodil",val:750},
      {name:"Riesenkalmar",val:275},
      {name:"Seepferd",val:0.01}
    ]
  },
  /* 3. Höchstgeschwindigkeit Land (km/h) */
  speed_land:{
    prompt:"Welches Tier läuft schneller? (Höchstgeschwindigkeit)",unit:"km/h",
    items:[
      {name:"Gepard",val:120},
      {name:"Pronghorn-Antilope",val:98},
      {name:"Löwe",val:80},
      {name:"Thomson-Gazelle",val:80},
      {name:"Wildhund (Afrika)",val:72},
      {name:"Streifengnu",val:80},
      {name:"Zebra",val:64},
      {name:"Springbock",val:90},
      {name:"Pferd (Vollblut)",val:88},
      {name:"Greyhound",val:72},
      {name:"Elefant",val:40},
      {name:"Grizzlybär",val:56},
      {name:"Polarbär",val:40},
      {name:"Kaninchen",val:56},
      {name:"Krokodil",val:17},
      {name:"Nilpferd",val:30},
      {name:"Nashorn",val:50},
      {name:"Schimpanse",val:40},
      {name:"Mensch (Usain Bolt)",val:44.7},
      {name:"Opossum",val:8}
    ]
  },
  /* 4. Höchstgeschwindigkeit Luft (km/h) */
  speed_luft:{
    prompt:"Welches Tier fliegt schneller? (Höchstgeschwindigkeit)",unit:"km/h",
    items:[
      {name:"Wanderfalke (Sturzflug)",val:389},
      {name:"Mauersegler",val:169},
      {name:"Weißkehl-Spint",val:170},
      {name:"Fregattvogel",val:153},
      {name:"Sakerfalke",val:240},
      {name:"Taube (Renntaube)",val:150},
      {name:"Weißkopfseeadler",val:160},
      {name:"Kolibri (Anna)",val:98},
      {name:"Sperber",val:50},
      {name:"Schwalbe",val:120},
      {name:"Albatros (Wind)",val:130},
      {name:"Bekassine",val:64},
      {name:"Drachen (Segelflug)",val:32},
      {name:"Graugans",val:90},
      {name:"Storch",val:55},
      {name:"Hornisse",val:25},
      {name:"Libelle",val:54},
      {name:"Biene",val:29},
      {name:"Hausfliege",val:8},
      {name:"Schmetterling (Monarch)",val:30}
    ]
  },
  /* 5. Höchstgeschwindigkeit Wasser (km/h) */
  speed_wasser:{
    prompt:"Welches Tier schwimmt schneller? (Höchstgeschwindigkeit)",unit:"km/h",
    items:[
      {name:"Fächerfisch (Sailfish)",val:110},
      {name:"Schwarzer Marlin",val:80},
      {name:"Gelbflossen-Thunfisch",val:74},
      {name:"Blauflossen-Thunfisch",val:70},
      {name:"Wahoo",val:96},
      {name:"Weißer Hai",val:40},
      {name:"Schwertfisch",val:97},
      {name:"Orca",val:55},
      {name:"Mako-Hai",val:70},
      {name:"Delphin (Gemeiner)",val:60},
      {name:"Seelöwe",val:35},
      {name:"Buckelwal",val:27},
      {name:"Leatherback-Schildkröte",val:35},
      {name:"Tintenfisch",val:40},
      {name:"Humboldt-Pinguin",val:36},
      {name:"Kaiserpinguin",val:27},
      {name:"Europäischer Otter",val:12},
      {name:"Nilpferd (Wasser)",val:8},
      {name:"Seehund",val:35},
      {name:"Seepferdchen",val:0.0015}
    ]
  },
  /* 6. Lebenserwartung (Jahre, maximales Alter) */
  lebenserwartung:{
    prompt:"Welches Tier wird älter? (Maximales Lebensalter)",unit:"Jahre",
    items:[
      {name:"Grönlandhai",val:400},
      {name:"Aldabra-Riesenschildkröte",val:255},
      {name:"Afrikanischer Elefant",val:70},
      {name:"Blauwal",val:80},
      {name:"Schimpanse (Gefangenschaft)",val:60},
      {name:"Ara (Hyazinth-Ara)",val:60},
      {name:"Mensch (global Durchschnitt)",val:72},
      {name:"Grizzlybär",val:30},
      {name:"Löwe",val:20},
      {name:"Leopard",val:23},
      {name:"Hund (Labrador)",val:13},
      {name:"Hauskatze",val:20},
      {name:"Wellensittich",val:15},
      {name:"Goldfisch (Rekord)",val:45},
      {name:"Flamingo",val:44},
      {name:"Rotkehlchen",val:13},
      {name:"Ameise (Königin)",val:30},
      {name:"Eintagsfliege (adult)",val:0.003},
      {name:"Wanderratte",val:3},
      {name:"Hausmaus",val:2}
    ]
  },
  /* 7. Trächtigkeitsdauer (Tage) */
  traechtigkeit:{
    prompt:"Welches Tier trägt länger? (Trächtigkeitsdauer in Tagen)",unit:"Tage",
    items:[
      {name:"Afrikanischer Elefant",val:660},
      {name:"Breitmaulnashorn",val:490},
      {name:"Giraffe",val:460},
      {name:"Walross",val:480},
      {name:"Nilpferd",val:240},
      {name:"Gorilla",val:257},
      {name:"Schimpanse",val:230},
      {name:"Pferd",val:340},
      {name:"Esel",val:365},
      {name:"Kuh",val:283},
      {name:"Löwe",val:110},
      {name:"Tiger",val:104},
      {name:"Gepard",val:92},
      {name:"Hund",val:63},
      {name:"Katze",val:65},
      {name:"Kaninchen",val:31},
      {name:"Goldhamster",val:16},
      {name:"Hausmaus",val:20},
      {name:"Opossum (Virginia)",val:13},
      {name:"Beutelratte (Känguru-Rattenähnlich)",val:22}
    ]
  },
  /* 8. Wurfgröße (max. Nachkommen pro Zyklus) */
  wurf:{
    prompt:"Welches Tier hat mehr Nachkommen pro Zyklus? (Maximum)",unit:"Junge",
    items:[
      {name:"Tenrek (Haarschwanztenrek)",val:32},
      {name:"Hauschwein",val:22},
      {name:"Virginia-Opossum",val:20},
      {name:"Europäischer Igel",val:7},
      {name:"Europäischer Feldhase",val:6},
      {name:"Kaninchen",val:14},
      {name:"Hund (Große Rassen)",val:12},
      {name:"Katze",val:8},
      {name:"Hausratte",val:14},
      {name:"Hausmaus",val:10},
      {name:"Löwe",val:6},
      {name:"Gepard",val:8},
      {name:"Gorilla",val:1},
      {name:"Elefant",val:1},
      {name:"Pinguin (Kaiserpinguin)",val:1},
      {name:"Wellensittich",val:6},
      {name:"Fleckhyäne",val:4},
      {name:"Wolf",val:8},
      {name:"Dachs",val:5},
      {name:"Polarfuchs",val:14}
    ]
  },
  /* 9. Giftigkeit — Toxizitätsscore (1000/LD50-mg/kg, invertiert, höher=giftiger) */
  gift:{
    prompt:"Welches Tier ist giftiger? (Toxizitätsscore — höher = giftiger)",unit:"Pkt",
    items:[
      {name:"Inland Taipan (Australien)",val:59000},
      {name:"Schwarze Mamba",val:3300},
      {name:"Königskobra",val:1250},
      {name:"Blaugeringelter Oktopus",val:8330},
      {name:"Würfelqualle",val:10000},
      {name:"Marmorierter Kegelschnecke",val:4500},
      {name:"Tropischer Steinfisch",val:1700},
      {name:"Goldener Giftfrosch",val:500000},
      {name:"Komodo-Waran (Bakterien/Gift)",val:200},
      {name:"Gabunviper",val:120},
      {name:"Braune Einsiedlerspinne",val:660},
      {name:"Schwarze Witwe",val:1300},
      {name:"Skorpion (Deathstalker)",val:5000},
      {name:"Europäische Kreuzotter",val:33},
      {name:"Gila-Krustenechse",val:100},
      {name:"Asiatische Riesenhornis",val:25},
      {name:"Honigbiene",val:12},
      {name:"Wespe",val:5},
      {name:"Feuerameise",val:2},
      {name:"Korallenotter (USA)",val:400}
    ]
  },
  /* 10. Wildpopulation (laut IUCN, Individuen) */
  population:{
    prompt:"Von welchem Tier gibt es mehr Wildtiere? (IUCN-Schätzung)",unit:"Ind.",
    items:[
      {name:"Afrikanische Spitzmaus",val:1000000000},
      {name:"Wanderratte",val:7000000000},
      {name:"Haushuhn (Wildform Bankivahuhn)",val:500000000},
      {name:"Rotfuchs",val:150000000},
      {name:"Großes Streifengnu",val:1300000},
      {name:"Afrikanischer Elefant",val:415000},
      {name:"Afrikanischer Löwe",val:20000},
      {name:"Tiger (alle Unterarten)",val:4500},
      {name:"Amur-Leopard",val:100},
      {name:"Java-Nashorn",val:75},
      {name:"Spix-Ara",val:200},
      {name:"Sumatra-Orang-Utan",val:7500},
      {name:"Berggorilla",val:1063},
      {name:"Schnabeltier",val:300000},
      {name:"Schneeleopard",val:4000},
      {name:"Blauwal",val:10000},
      {name:"Delfin (Tümmler, global)",val:600000},
      {name:"Weißkopfseeadler",val:70000},
      {name:"Weißer Hai",val:3500},
      {name:"Eisbär",val:26000}
    ]
  },
  /* 11. Schlafbedarf (Stunden pro Tag) */
  schlaf:{
    prompt:"Welches Tier schläft länger? (Stunden pro Tag, Durchschnitt)",unit:"Std/Tag",
    items:[
      {name:"Koala",val:22},
      {name:"Faultier (Dreizehen)",val:20},
      {name:"Braune Fledermaus",val:19.9},
      {name:"Opossum",val:18},
      {name:"Löwe",val:16},
      {name:"Katze",val:15},
      {name:"Hund",val:12},
      {name:"Schimpanse",val:11},
      {name:"Hamster",val:14},
      {name:"Nasenbär",val:11},
      {name:"Boa constrictor",val:16},
      {name:"Afrikanischer Elefant",val:2},
      {name:"Pferd",val:3},
      {name:"Kuh",val:4},
      {name:"Giraffe",val:2},
      {name:"Schaf",val:4},
      {name:"Gorilla",val:12},
      {name:"Delfin (Tümmler)",val:8},
      {name:"Mensch (Erwachsener)",val:8},
      {name:"Wanderamsel",val:4}
    ]
  }
};

/* === Phase 227: genTiereHL — La-Paz-Trauma-Safe H/L Generator === */
function genTiereHL(dataKey){
  const cfg=TIER_HL_DATA[dataKey];
  if(!cfg||!cfg.items||cfg.items.length<2)return null;
  const sorted=cfg.items.slice().sort(function(a,b){return parseFloat(a.val)-parseFloat(b.val);});
  const len=sorted.length;
  var tries=0;
  while(tries++<40){
    var ai=~~(rng()*len);
    var W=Math.max(1,Math.floor(len*0.1));
    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);
    var pool=[];
    for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}
    if(!pool.length)continue;
    var bi=pool[~~(rng()*pool.length)];
    var a=sorted[ai],b=sorted[bi];
    var va=parseFloat(a.val),vb=parseFloat(b.val);
    if(va===vb)continue;
    /* reject tiny relative difference — at least 5% spread */
    var span=parseFloat(sorted[len-1].val)-parseFloat(sorted[0].val);
    if(span>0&&Math.abs(va-vb)<span*0.02)continue;
    var higher=va>vb?a:b;
    var unit=cfg.unit||"";
    var meta=a.name+": "+a.val+(unit?" "+unit:"")+" · "+b.name+": "+b.val+(unit?" "+unit:"");
    var _lid="thl_"+dataKey+"_"+Math.min(ai,bi)+"_"+Math.max(ai,bi);
    return{type:"beta_hl",prompt:cfg.prompt||"Welches ist mehr?",subj:"",
      opts:[a.name,b.name],ans:higher.name,meta:meta,lid:_lid,cc:"de"};
  }
  return null;
}

""" + "function genUniversalMatchQ(cat){"

if GEN_MATCH_ANCHOR not in content:
    print("ERROR: genUniversalMatchQ anchor not found – check gen.py")
    exit(1)

content = content.replace(GEN_MATCH_ANCHOR, TIER_HL_BLOCK, 1)
print("✓ PATCH B: TIER_HL_DATA + genTiereHL() injected")

# ══════════════════════════════════════════════════════════════════════════════
# BLOCK C: GEN dispatch entries for all 21 tiere modes
# Insert after the last uk_leichtathletik_wm entry in GEN dispatch
# ══════════════════════════════════════════════════════════════════════════════

GEN_DISPATCH_ANCHOR = "  uk_leichtathletik_wm:()=>genUniversalPinQ(\"leichtathletik_wm\"),"

TIERE_DISPATCH = """  uk_leichtathletik_wm:()=>genUniversalPinQ("leichtathletik_wm"),
  /* === Phase 227: Tiere & Natur GEN dispatch === */
  /* Pin Modi */
  uk_tiere_endemisch:()=>genUniversalPinQ("tiere_endemisch"),
  uk_tiere_bigfive:()=>genUniversalPinQ("tiere_bigfive"),
  uk_tiere_grosskatzen:()=>genUniversalPinQ("tiere_grosskatzen"),
  uk_tiere_invasiv:()=>genUniversalPinQ("tiere_invasiv"),
  uk_tiere_vogelzug:()=>genUniversalPinQ("tiere_vogelzug"),
  uk_tiere_haustiere:()=>genUniversalPinQ("tiere_haustiere"),
  uk_tiere_nationaltier_pin:()=>genUniversalPinQ("tiere_nationaltier_pin"),
  uk_tiere_primaten:()=>genUniversalPinQ("tiere_primaten"),
  uk_tiere_hai:()=>genUniversalPinQ("tiere_hai"),
  uk_tiere_baeren:()=>genUniversalPinQ("tiere_baeren"),
  /* H/L Modi */
  hl_tiere_gewicht_land:()=>genTiereHL("gewicht_land"),
  hl_tiere_gewicht_meer:()=>genTiereHL("gewicht_meer"),
  hl_tiere_speed_land:()=>genTiereHL("speed_land"),
  hl_tiere_speed_luft:()=>genTiereHL("speed_luft"),
  hl_tiere_speed_wasser:()=>genTiereHL("speed_wasser"),
  hl_tiere_lebenserwartung:()=>genTiereHL("lebenserwartung"),
  hl_tiere_traechtigkeit:()=>genTiereHL("traechtigkeit"),
  hl_tiere_wurf:()=>genTiereHL("wurf"),
  hl_tiere_gift:()=>genTiereHL("gift"),
  hl_tiere_population:()=>genTiereHL("population"),
  hl_tiere_schlaf:()=>genTiereHL("schlaf"),"""

if GEN_DISPATCH_ANCHOR not in content:
    print("ERROR: GEN dispatch anchor (uk_leichtathletik_wm) not found – check gen.py")
    exit(1)

content = content.replace(GEN_DISPATCH_ANCHOR, TIERE_DISPATCH, 1)
print("✓ PATCH C: GEN dispatch entries for 21 tiere modes added")

# ══════════════════════════════════════════════════════════════════════════════
# Write result
# ══════════════════════════════════════════════════════════════════════════════
with open(SRC, "w", encoding="utf-8") as f:
    f.write(content)

print("\n✅ enrich_tiere_part1.py complete — all 3 patches applied to gen.py")
print("   Next: python gen.py && verify GeoQuest.html")
