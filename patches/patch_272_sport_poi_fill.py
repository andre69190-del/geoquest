#!/usr/bin/env python3
"""Phase 272: SPORT_POI expansion + geo/kultur fill + BETA removal"""
import json, re, os

GEN  = '/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py'
DATA = '/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/data'

with open(GEN, encoding='utf-8') as f:
    content = f.read()

def patch(old, new, label):
    global content
    if old not in content:
        print(f'[SKIP] {label}: anchor not found')
        return
    result = content.replace(old, new, 1)
    if result == content:
        print(f'[SKIP] {label}: no change')
    else:
        content = result
        print(f'[OK]   {label}')

# ============================================================
# PART 1: SPORT_POI_GAMES expansions
# ============================================================

# --- derby_hotspots: 14 -> 50 (+36) ---
OLD_DERBY = (
    "', 'lat': -34.6357, 'lng': -58.3643, 'cc': 'ar'}]}"
    # The full key is used via the name prefix below
)
# Use more precise anchor including name
OLD_DERBY = "'Clásico de Clasicos: Boca Juniors Stadion La Bombonera', 'lat': -34.6357, 'lng': -58.3643, 'cc': 'ar'}]}"
NEW_DERBY_TAIL = [
    "{'name': 'Klassieker: Feyenoord vs. Ajax (Rotterdam)', 'lat': 51.8934, 'lng': 4.5231, 'cc': 'nl'}",
    "{'name': 'Superderby: Peñarol vs. Nacional (Montevideo)', 'lat': -34.8941, 'lng': -56.1832, 'cc': 'uy'}",
    "{'name': 'Cairo Derby: Al Ahly vs. Zamalek (Kairo)', 'lat': 30.0626, 'lng': 31.2222, 'cc': 'eg'}",
    "{'name': 'El Clásico Portugués: Benfica vs. Sporting CP (Lissabon)', 'lat': 38.7526, 'lng': -9.1847, 'cc': 'pt'}",
    "{'name': 'Celtic Park Derby (Celtic vs. Rangers, Glasgow)', 'lat': 55.8490, 'lng': -4.2057, 'cc': 'gb'}",
    "{'name': 'Rhine Derby: 1. FC Köln vs. Borussia Mönchengladbach', 'lat': 50.9333, 'lng': 6.8749, 'cc': 'de'}",
    "{'name': 'Hamburger Derby: HSV vs. St. Pauli', 'lat': 53.5877, 'lng': 9.8986, 'cc': 'de'}",
    "{'name': 'Derby di Milano: San Siro (Inter vs. AC Milan)', 'lat': 45.4781, 'lng': 9.1240, 'cc': 'it'}",
    "{'name': 'Derby de Madrid: Atletico vs. Real Madrid (Metropolitano)', 'lat': 40.4361, 'lng': -3.5990, 'cc': 'es'}",
    "{'name': 'Manchester Derby: Man United vs. Man City (Etihad)', 'lat': 53.4831, 'lng': -2.2004, 'cc': 'gb'}",
    "{'name': 'Clasico Colombiano: Millonarios vs. Santa Fe (Bogota)', 'lat': 4.6486, 'lng': -74.0853, 'cc': 'co'}",
    "{'name': 'Clasico Limeño: Alianza Lima vs. Universitario', 'lat': -12.0923, 'lng': -77.0169, 'cc': 'pe'}",
    "{'name': 'Santiago Derby: Colo-Colo vs. Universidad de Chile', 'lat': -33.4569, 'lng': -70.6483, 'cc': 'cl'}",
    "{'name': 'São Paulo Derby: Corinthians vs. Palmeiras', 'lat': -23.5489, 'lng': -46.5270, 'cc': 'br'}",
    "{'name': 'Fla-Flu: Flamengo vs. Fluminense (Rio de Janeiro)', 'lat': -22.9122, 'lng': -43.2302, 'cc': 'br'}",
    "{'name': 'Buenos Aires Derby: Racing vs. Independiente (Avellaneda)', 'lat': -34.6602, 'lng': -58.3687, 'cc': 'ar'}",
    "{'name': 'Bundesliga-Topspiel: Bayern München vs. Borussia Dortmund', 'lat': 48.2188, 'lng': 11.6248, 'cc': 'de'}",
    "{'name': 'Derby de Lyon: Olympique Lyon vs. AS Saint-Etienne', 'lat': 45.7676, 'lng': 4.9823, 'cc': 'fr'}",
    "{'name': 'Clasico Vasco: Athletic Bilbao vs. Real Sociedad', 'lat': 43.2644, 'lng': -2.9497, 'cc': 'es'}",
    "{'name': 'Derby della Mole: Juventus vs. Torino FC (Turin)', 'lat': 45.1096, 'lng': 7.6413, 'cc': 'it'}",
    "{'name': 'Derby de Athen: Panathinaikos vs. Olympiakos', 'lat': 37.9838, 'lng': 23.7275, 'cc': 'gr'}",
    "{'name': 'Istanbul Derby: Galatasaray vs. Besiktas', 'lat': 41.0386, 'lng': 29.0049, 'cc': 'tr'}",
    "{'name': 'Superderby NL: PSV vs. Ajax (Eindhoven)', 'lat': 51.4416, 'lng': 5.4676, 'cc': 'nl'}",
    "{'name': 'Edinburgh Derby: Hearts vs. Hibernian', 'lat': 55.9334, 'lng': -3.1725, 'cc': 'gb'}",
    "{'name': 'Bucharest Derby: Dinamo vs. Steaua', 'lat': 44.4268, 'lng': 26.1025, 'cc': 'ro'}",
    "{'name': 'Australian Derby: Wanderers vs. Sydney FC', 'lat': -33.8731, 'lng': 151.0649, 'cc': 'au'}",
    "{'name': 'Clasico Azteca: America vs. Guadalajara / Chivas', 'lat': 19.3031, 'lng': -99.1506, 'cc': 'mx'}",
    "{'name': 'Korean Derby: FC Seoul vs. Jeonbuk', 'lat': 37.5772, 'lng': 126.9005, 'cc': 'kr'}",
    "{'name': 'Derby de Paris: PSG vs. Olympique de Marseille', 'lat': 48.8414, 'lng': 2.2531, 'cc': 'fr'}",
    "{'name': 'East Midlands Derby: Nottingham Forest vs. Derby County', 'lat': 52.9400, 'lng': -1.1325, 'cc': 'gb'}",
    "{'name': 'Moscow Derby: CSKA vs. Spartak', 'lat': 55.7161, 'lng': 37.5619, 'cc': 'ru'}",
    "{'name': 'Superclasico Paraguayo: Olimpia vs. Cerro Porteno (Asuncion)', 'lat': -25.2867, 'lng': -57.6470, 'cc': 'py'}",
    "{'name': 'Cape Town Derby: Cape Town City vs. Ajax Cape Town', 'lat': -33.9249, 'lng': 18.4241, 'cc': 'za'}",
    "{'name': 'Al-Ittihad vs. Al-Hilal (Riad, Saudi Arabien)', 'lat': 24.6877, 'lng': 46.7219, 'cc': 'sa'}",
    "{'name': 'Taipei Derby: Tatung vs. Taichung (Taiwan)', 'lat': 25.0330, 'lng': 121.5654, 'cc': 'tw'}",
    "{'name': 'Superderby Iran: Esteghlal vs. Persepolis (Teheran)', 'lat': 35.6892, 'lng': 51.3890, 'cc': 'ir'}",
]
NEW_DERBY = (
    "'Clásico de Clasicos: Boca Juniors Stadion La Bombonera', 'lat': -34.6357, 'lng': -58.3643, 'cc': 'ar'}, "
    + ", ".join(NEW_DERBY_TAIL) + "]}"
)
patch(OLD_DERBY, NEW_DERBY, "derby_hotspots +36")

# --- eishockey_nationen: 12 -> 50 (+38) ---
OLD_EISHOCKEY = "'Zürich (Swiss Life Arena – ZSC Lions)', 'lat': 47.3769, 'lng': 8.5417, 'cc': 'ch'}]}"
NEW_EISHOCKEY_TAIL = [
    "{'name': 'Vancouver (Rogers Arena – Canucks)', 'lat': 49.2778, 'lng': -123.1088, 'cc': 'ca'}",
    "{'name': 'Chicago (United Center – Blackhawks Original Six)', 'lat': 41.8806, 'lng': -87.6742, 'cc': 'us'}",
    "{'name': 'New York (Madison Square Garden – Rangers)', 'lat': 40.7505, 'lng': -73.9934, 'cc': 'us'}",
    "{'name': 'Pittsburgh (PPG Paints Arena – Penguins)', 'lat': 40.4396, 'lng': -79.9892, 'cc': 'us'}",
    "{'name': 'Innsbruck (Tiroler Wasserkraft Arena – EBEL)', 'lat': 47.3769, 'lng': 11.3418, 'cc': 'at'}",
    "{'name': 'Wien (Wiener Stadthalle – WM-Gastgeber 1996)', 'lat': 48.1978, 'lng': 16.3353, 'cc': 'at'}",
    "{'name': 'Riga (Arena Riga – WM-Gastgeber 2006 & 2021)', 'lat': 56.9550, 'lng': 24.0957, 'cc': 'lv'}",
    "{'name': 'Nur-Sultan (Barys Arena – KHL Kasachstan)', 'lat': 51.0882, 'lng': 71.3962, 'cc': 'kz'}",
    "{'name': 'Omsk (Arena Omsk – Avangard KHL)', 'lat': 54.9923, 'lng': 73.3682, 'cc': 'ru'}",
    "{'name': 'Edmonton (Rogers Place – Oilers)', 'lat': 53.5461, 'lng': -113.4938, 'cc': 'ca'}",
    "{'name': 'Calgary (Scotiabank Saddledome – Flames)', 'lat': 51.0374, 'lng': -114.0519, 'cc': 'ca'}",
    "{'name': 'Tampere (Nokia Arena – WM-Gastgeber 2023)', 'lat': 61.4980, 'lng': 23.7608, 'cc': 'fi'}",
    "{'name': 'Ostrava (Ostravar Arena – WM-Gastgeber 2004)', 'lat': 49.8209, 'lng': 18.2625, 'cc': 'cz'}",
    "{'name': 'Paris (Bercy Arena – WM-Gastgeber 2017)', 'lat': 48.8393, 'lng': 2.3790, 'cc': 'fr'}",
    "{'name': 'Köln (Lanxess Arena – DEL-Hochburg)', 'lat': 50.9667, 'lng': 6.9776, 'cc': 'de'}",
    "{'name': 'Berlin (Mercedes-Benz Arena – Eisbären DEL)', 'lat': 52.4822, 'lng': 13.4702, 'cc': 'de'}",
    "{'name': 'München (Olympiahalle – WM-Gastgeber 1975)', 'lat': 48.1735, 'lng': 11.5461, 'cc': 'de'}",
    "{'name': 'Göteborg (Scandinavium – WM-Gastgeber 2002)', 'lat': 57.6964, 'lng': 11.9796, 'cc': 'se'}",
    "{'name': 'Oslo (Jordal Amfi – Eishockey-Traditionsort)', 'lat': 59.9139, 'lng': 10.7522, 'cc': 'no'}",
    "{'name': 'Davos (Vaillant Arena – Spengler Cup Heimat)', 'lat': 46.8047, 'lng': 9.8396, 'cc': 'ch'}",
    "{'name': 'Peking (National Aquatics Center – Olympia 2022)', 'lat': 39.9842, 'lng': 116.3915, 'cc': 'cn'}",
    "{'name': 'Sochi (Bolshoy Ice Dome – Olympia 2014)', 'lat': 43.4081, 'lng': 39.9527, 'cc': 'ru'}",
    "{'name': 'Turin (Palavela – Olympia 2006)', 'lat': 45.0510, 'lng': 7.6680, 'cc': 'it'}",
    "{'name': 'Salt Lake City (Olympia 2002 Eishockey)', 'lat': 40.7608, 'lng': -111.8910, 'cc': 'us'}",
    "{'name': 'Nagano (Big Hat Arena – Olympia 1998)', 'lat': 36.6485, 'lng': 138.1947, 'cc': 'jp'}",
    "{'name': 'Lillehammer (Hakons Hall – Olympia 1994)', 'lat': 61.1153, 'lng': 10.4662, 'cc': 'no'}",
    "{'name': 'Katowice (Spodek – WM-Gastgeber 1976)', 'lat': 50.2649, 'lng': 19.0238, 'cc': 'pl'}",
    "{'name': 'Garmisch-Partenkirchen (Olympia-Eissportzentrum)', 'lat': 47.4912, 'lng': 11.0948, 'cc': 'de'}",
    "{'name': 'Reykjavik (Laugardalsholl – Island)', 'lat': 64.1335, 'lng': -21.8977, 'cc': 'is'}",
    "{'name': 'Kosice (Steel Arena – WM-Gastgeber 2019)', 'lat': 48.6980, 'lng': 21.2547, 'cc': 'sk'}",
    "{'name': 'Buffalo (KeyBank Center – Sabres)', 'lat': 42.8745, 'lng': -78.8762, 'cc': 'us'}",
    "{'name': 'Washington DC (Capital One Arena – Capitals)', 'lat': 38.8981, 'lng': -77.0209, 'cc': 'us'}",
    "{'name': 'Philadelphia (Wells Fargo Center – Flyers)', 'lat': 39.9012, 'lng': -75.1719, 'cc': 'us'}",
    "{'name': 'Denver (Ball Arena – Avalanche)', 'lat': 39.7487, 'lng': -105.0076, 'cc': 'us'}",
    "{'name': 'Winnipeg (Canada Life Centre – Jets)', 'lat': 49.8928, 'lng': -97.1437, 'cc': 'ca'}",
    "{'name': 'Ottawa (Canadian Tire Centre – Senators)', 'lat': 45.2969, 'lng': -75.9277, 'cc': 'ca'}",
    "{'name': 'Genf (Patinoire des Vernets – Servette HC)', 'lat': 46.1884, 'lng': 6.1263, 'cc': 'ch'}",
    "{'name': 'Lugano (Cornèr Arena – HC Lugano)', 'lat': 46.0026, 'lng': 8.9726, 'cc': 'ch'}",
]
NEW_EISHOCKEY = (
    "'Zürich (Swiss Life Arena – ZSC Lions)', 'lat': 47.3769, 'lng': 8.5417, 'cc': 'ch'}, "
    + ", ".join(NEW_EISHOCKEY_TAIL) + "]}"
)
patch(OLD_EISHOCKEY, NEW_EISHOCKEY, "eishockey_nationen +38")

# --- f1_historisch: 20 -> 50 (+30) ---
OLD_F1 = "{'name':'Albert Park Circuit (Melbourne, Australien)','lat':-37.8497,'lng':144.9683,'cc':'au'}]}"
NEW_F1_TAIL = [
    "{'name':'Circuito de Pedralbes (Barcelona, Spanien – GP 1950-1954)','lat':41.3886,'lng':2.1340,'cc':'es'}",
    "{'name':'Bremgarten Circuit (Bern, Schweiz – GP 1950-1954)','lat':46.9480,'lng':7.4170,'cc':'ch'}",
    "{'name':'Pescara Circuit (Pescara, Italien – GP 1957)','lat':42.4617,'lng':14.2150,'cc':'it'}",
    "{'name':'Sebring International Raceway (Florida, USA – GP 1959)','lat':27.4567,'lng':-81.3473,'cc':'us'}",
    "{'name':'Riverside International Raceway (Kalifornien, USA – GP 1960)','lat':33.9019,'lng':-117.2437,'cc':'us'}",
    "{'name':'Mosport Park (Ontario, Kanada – GP 1967-1977)','lat':44.0589,'lng':-78.6769,'cc':'ca'}",
    "{'name':'Circuit de Jarama (Madrid, Spanien – GP 1968-1981)','lat':40.6186,'lng':-3.5851,'cc':'es'}",
    "{'name':'Zeltweg Airfield (Österreich – erster GP 1964)','lat':47.2031,'lng':14.7399,'cc':'at'}",
    "{'name':'Circuit de Dijon-Prenois (Frankreich – GP 1974-1984)','lat':47.3625,'lng':4.8994,'cc':'fr'}",
    "{'name':'Long Beach Street Circuit (Kalifornien, USA – GP 1976-1983)','lat':33.7701,'lng':-118.1937,'cc':'us'}",
    "{'name':'Detroit Street Circuit (Michigan, USA – GP 1982-1988)','lat':42.3314,'lng':-83.0458,'cc':'us'}",
    "{'name':'Dallas Street Circuit (Texas, USA – GP 1984)','lat':32.7767,'lng':-96.7970,'cc':'us'}",
    "{'name':'Circuit Gilles Villeneuve (Montreal, Kanada)','lat':45.5058,'lng':-73.5228,'cc':'ca'}",
    "{'name':'Phoenix Street Circuit (Arizona, USA – GP 1989-1991)','lat':33.4484,'lng':-112.0740,'cc':'us'}",
    "{'name':'Buenos Aires Grand Prix Circuit (Argentinien – GP 1953-1998)','lat':-34.6850,'lng':-58.4594,'cc':'ar'}",
    "{'name':'Buddh International Circuit (Indien – GP 2011-2013)','lat':28.3487,'lng':77.5330,'cc':'in'}",
    "{'name':'Korean International Circuit (Yeongam – GP 2010-2013)','lat':34.7330,'lng':126.4158,'cc':'kr'}",
    "{'name':'Valencia Street Circuit (Spanien – GP 2008-2012)','lat':39.4699,'lng':-0.3763,'cc':'es'}",
    "{'name':'Istanbul Park (Türkei – GP 2005-2021)','lat':40.9517,'lng':29.4050,'cc':'tr'}",
    "{'name':'Donington Park (England – GP 1993)','lat':52.8299,'lng':-1.3754,'cc':'gb'}",
    "{'name':'Fuji Speedway (Japan – GP 1976-1977, 2007-2008)','lat':35.3710,'lng':138.9247,'cc':'jp'}",
    "{'name':'Jerez Circuit (Spanien – GP 1986-1997)','lat':36.7082,'lng':-6.0341,'cc':'es'}",
    "{'name':'Mugello Circuit (Italien – GP 2020)','lat':43.9975,'lng':11.3719,'cc':'it'}",
    "{'name':'Autodromo Jose Carlos Pace (Interlagos, Brasilien)','lat':-23.7036,'lng':-46.6997,'cc':'br'}",
    "{'name':'Circuit de Nevers Magny-Cours (Frankreich – GP 1991-2008)','lat':46.8633,'lng':3.1633,'cc':'fr'}",
    "{'name':'Hockenheimring (Deutschland – GP 1970-2019)','lat':49.3278,'lng':8.5656,'cc':'de'}",
    "{'name':'Yas Marina Circuit (Abu Dhabi – seit 2009)','lat':24.4672,'lng':54.6031,'cc':'ae'}",
    "{'name':'Bahrain International Circuit (Sakhir – seit 2004)','lat':26.0325,'lng':50.5106,'cc':'bh'}",
    "{'name':'Circuit de Spa-Francorchamps alt (Belgien – Full Circuit pre-1979)','lat':50.4372,'lng':5.9714,'cc':'be'}",
    "{'name':'Circuito Permanente de Jerez (Spanien – historischer F1-Test)','lat':36.7082,'lng':-6.0341,'cc':'es'}",
]
NEW_F1 = (
    "{'name':'Albert Park Circuit (Melbourne, Australien)','lat':-37.8497,'lng':144.9683,'cc':'au'}, "
    + ", ".join(NEW_F1_TAIL) + "]}"
)
patch(OLD_F1, NEW_F1, "f1_historisch +30")

# --- tdf_paesse: 12 -> 50 (+38) ---
OLD_TDF = "'Col de la Loze (Courchevel – neuester Super-Pass)', 'lat': 45.4167, 'lng': 6.6333, 'cc': 'fr'}]}"
NEW_TDF_TAIL = [
    "{'name': 'Col du Galibier (2642m – TdF-Klassiker)', 'lat': 45.0638, 'lng': 6.4080, 'cc': 'fr'}",
    "{'name': 'Col du Tourmalet (2115m – meistgefahrener TdF-Pass)', 'lat': 42.9083, 'lng': 0.1456, 'cc': 'fr'}",
    "{'name': \"Alpe d'Huez (1860m – 21 Kehren)\", 'lat': 45.0900, 'lng': 6.0700, 'cc': 'fr'}",
    "{'name': 'Mont Ventoux (1909m – Gigant der Provence)', 'lat': 44.1742, 'lng': 5.2783, 'cc': 'fr'}",
    "{'name': \"Col d'Aubisque (1709m – TdF-Pyrenäen)\", 'lat': 42.9716, 'lng': -0.3371, 'cc': 'fr'}",
    "{'name': 'Col de la Croix de Fer (2067m – Alpen)', 'lat': 45.2286, 'lng': 6.1824, 'cc': 'fr'}",
    "{'name': 'Col du Glandon (1924m)', 'lat': 45.2211, 'lng': 6.1600, 'cc': 'fr'}",
    "{'name': \"Col d'Izoard (2360m)\", 'lat': 44.8222, 'lng': 6.7344, 'cc': 'fr'}",
    "{'name': 'Col de Vars (2109m – Hautes-Alpes)', 'lat': 44.5372, 'lng': 6.7025, 'cc': 'fr'}",
    "{'name': 'Passo dello Stelvio (2758m – König der Giro-Pässe)', 'lat': 46.5289, 'lng': 10.4536, 'cc': 'it'}",
    "{'name': 'Passo di Mortirolo (1852m – Härtester Giro-Anstieg)', 'lat': 46.2231, 'lng': 10.3328, 'cc': 'it'}",
    "{'name': 'Passo Gavia (2621m – Giro d\\'Italia)', 'lat': 46.3433, 'lng': 10.4942, 'cc': 'it'}",
    "{'name': 'Passo Pordoi (2239m – Dolomiten, Giro)', 'lat': 46.4877, 'lng': 11.8113, 'cc': 'it'}",
    "{'name': 'Passo di Giau (2233m – Dolomiten)', 'lat': 46.4786, 'lng': 12.0540, 'cc': 'it'}",
    "{'name': 'Colle delle Finestre (2178m – Giro Schotter-Pass)', 'lat': 45.0497, 'lng': 7.0503, 'cc': 'it'}",
    "{'name': 'Alto de l\\'Angliru (1573m – Vuelta, steilster Radanstieg)', 'lat': 43.2347, 'lng': -5.9769, 'cc': 'es'}",
    "{'name': 'Alto de la Covatilla (1979m – Vuelta a España)', 'lat': 40.2869, 'lng': -5.8483, 'cc': 'es'}",
    "{'name': 'Lagos de Covadonga (1134m – Vuelta Wallfahrtsort)', 'lat': 43.2625, 'lng': -4.9722, 'cc': 'es'}",
    "{'name': 'Pico de Veleta (3398m – höchster Radgipfel Europas)', 'lat': 37.0539, 'lng': -3.3667, 'cc': 'es'}",
    "{'name': 'Sa Calobra (Mallorca – Radlegende)', 'lat': 39.8520, 'lng': 2.7950, 'cc': 'es'}",
    "{'name': 'Col de Peyresourde (1569m – Pyrenäen)', 'lat': 42.7950, 'lng': 0.4450, 'cc': 'fr'}",
    "{'name': \"Col de Porté d'Aspet (1069m)\", 'lat': 42.9806, 'lng': 0.9522, 'cc': 'fr'}",
    "{'name': 'Passo San Pellegrino (1918m – Dolomiten)', 'lat': 46.3731, 'lng': 11.7989, 'cc': 'it'}",
    "{'name': 'Grosse Scheidegg (1962m – Schweizer Alpen)', 'lat': 46.6622, 'lng': 8.1047, 'cc': 'ch'}",
    "{'name': 'Col des Aravis (1498m – Haute-Savoie)', 'lat': 45.8828, 'lng': 6.3678, 'cc': 'fr'}",
    "{'name': 'Col de la Madeleine (2000m – Savoie)', 'lat': 45.4258, 'lng': 6.3528, 'cc': 'fr'}",
    "{'name': 'Col de Joux Plane (1691m – Haute-Savoie)', 'lat': 46.0597, 'lng': 6.7061, 'cc': 'fr'}",
    "{'name': \"Col de l'Iseran (2764m – höchster asphaltierter Alpenpass)\", 'lat': 45.4197, 'lng': 7.0311, 'cc': 'fr'}",
    "{'name': 'Col Agnel (2744m – Queyras-Alpen)', 'lat': 44.6831, 'lng': 6.9767, 'cc': 'fr'}",
    "{'name': 'Cime de la Bonette (2802m – höchste TdF-Passstrasse)', 'lat': 44.3272, 'lng': 6.8119, 'cc': 'fr'}",
    "{'name': 'Cormet de Roselend (1968m – Savoie)', 'lat': 45.6564, 'lng': 6.6153, 'cc': 'fr'}",
    "{'name': 'Col de la Colombière (1618m – Haute-Savoie)', 'lat': 46.0133, 'lng': 6.4483, 'cc': 'fr'}",
    "{'name': 'Col du Petit Saint-Bernard (2188m – Grenze It/Fr)', 'lat': 45.6764, 'lng': 6.8831, 'cc': 'fr'}",
    "{'name': 'Passo Tre Cime di Lavaredo (2320m – Dolomiten-Ikone)', 'lat': 46.6183, 'lng': 12.3010, 'cc': 'it'}",
    "{'name': 'Colle del Nivolet (2612m – Aosta-Tal, Giro)', 'lat': 45.4667, 'lng': 7.1333, 'cc': 'it'}",
    "{'name': 'Passo del Furlo (257m – Giro-Klassiker Marken)', 'lat': 43.6833, 'lng': 12.6833, 'cc': 'it'}",
    "{'name': 'Puerto de la Ragua (2041m – Sierra Nevada, Vuelta)', 'lat': 37.1500, 'lng': -3.0500, 'cc': 'es'}",
    "{'name': 'Passo Fedaia (2057m – Marmolada, Giro)', 'lat': 46.4478, 'lng': 11.8828, 'cc': 'it'}",
]
NEW_TDF = (
    "'Col de la Loze (Courchevel – neuester Super-Pass)', 'lat': 45.4167, 'lng': 6.6333, 'cc': 'fr'}, "
    + ", ".join(NEW_TDF_TAIL) + "]}"
)
patch(OLD_TDF, NEW_TDF, "tdf_paesse +38")

# --- fussball_legenden: 13 -> 50 (+37) ---
OLD_FLEG = "'Lev Yashin (Geburtsort: Moskau, Russland)', 'lat': 55.7558, 'lng': 37.6173, 'cc': 'ru'}]}"
NEW_FLEG_TAIL = [
    "{'name': 'Johan Cruyff (Geburtsort: Amsterdam, Niederlande)', 'lat': 52.3676, 'lng': 4.9041, 'cc': 'nl'}",
    "{'name': 'Zinedine Zidane (Geburtsort: Marseille, Frankreich)', 'lat': 43.2965, 'lng': 5.3698, 'cc': 'fr'}",
    "{'name': 'Ronaldo Nazário (Geburtsort: Rio de Janeiro, Brasilien)', 'lat': -22.9068, 'lng': -43.1729, 'cc': 'br'}",
    "{'name': 'Ronaldinho (Geburtsort: Porto Alegre, Brasilien)', 'lat': -30.0346, 'lng': -51.2177, 'cc': 'br'}",
    "{'name': 'Romário (Geburtsort: Rio de Janeiro, Brasilien)', 'lat': -22.9068, 'lng': -43.1729, 'cc': 'br'}",
    "{'name': 'Eusébio (Geburtsort: Maputo / Lourenço Marques, Mosambik)', 'lat': -25.9692, 'lng': 32.5732, 'cc': 'mz'}",
    "{'name': 'Franz Beckenbauer (Geburtsort: München, Deutschland)', 'lat': 48.1351, 'lng': 11.5820, 'cc': 'de'}",
    "{'name': 'Gerd Müller (Geburtsort: Nördlingen, Deutschland)', 'lat': 48.8516, 'lng': 10.4898, 'cc': 'de'}",
    "{'name': 'Marco van Basten (Geburtsort: Utrecht, Niederlande)', 'lat': 52.0907, 'lng': 5.1214, 'cc': 'nl'}",
    "{'name': 'Ruud Gullit (Geburtsort: Amsterdam, Niederlande)', 'lat': 52.3676, 'lng': 4.9041, 'cc': 'nl'}",
    "{'name': 'Michel Platini (Geburtsort: Joeuf, Frankreich)', 'lat': 49.2333, 'lng': 6.0167, 'cc': 'fr'}",
    "{'name': 'Thierry Henry (Geburtsort: Pontoise, Frankreich)', 'lat': 49.0508, 'lng': 2.0992, 'cc': 'fr'}",
    "{'name': 'Cristiano Ronaldo (Geburtsort: Funchal, Madeira, Portugal)', 'lat': 32.6669, 'lng': -16.9241, 'cc': 'pt'}",
    "{'name': 'Lionel Messi (Geburtsort: Rosario, Argentinien)', 'lat': -32.9468, 'lng': -60.6393, 'cc': 'ar'}",
    "{'name': 'Neymar Jr. (Geburtsort: Mogi das Cruzes, Brasilien)', 'lat': -23.5226, 'lng': -46.1855, 'cc': 'br'}",
    "{'name': 'Roberto Baggio (Geburtsort: Caldogno, Italien)', 'lat': 45.6333, 'lng': 11.5167, 'cc': 'it'}",
    "{'name': 'Paolo Maldini (Geburtsort: Mailand, Italien)', 'lat': 45.4654, 'lng': 9.1866, 'cc': 'it'}",
    "{'name': 'Zlatan Ibrahimović (Geburtsort: Malmö, Schweden)', 'lat': 55.6050, 'lng': 13.0038, 'cc': 'se'}",
    "{'name': 'Luka Modrić (Geburtsort: Zadar, Kroatien)', 'lat': 44.1194, 'lng': 15.2314, 'cc': 'hr'}",
    "{'name': 'Kylian Mbappé (Geburtsort: Paris, Frankreich)', 'lat': 48.8566, 'lng': 2.3522, 'cc': 'fr'}",
    "{'name': 'Erling Haaland (Geburtsort: Leeds, England)', 'lat': 53.8008, 'lng': -1.5491, 'cc': 'gb'}",
    "{'name': 'Sadio Mané (Geburtsort: Sédhiou, Senegal)', 'lat': 12.7079, 'lng': -15.5567, 'cc': 'sn'}",
    "{'name': 'Mohamed Salah (Geburtsort: Nagrig, Ägypten)', 'lat': 31.0040, 'lng': 30.9500, 'cc': 'eg'}",
    "{'name': 'Didier Drogba (Geburtsort: Abidjan, Elfenbeinküste)', 'lat': 5.3600, 'lng': -4.0083, 'cc': 'ci'}",
    "{'name': \"Samuel Eto'o (Geburtsort: Nkon, Kamerun)\", 'lat': 3.8480, 'lng': 11.5021, 'cc': 'cm'}",
    "{'name': 'Riyad Mahrez (Geburtsort: Sarcelles, Frankreich)', 'lat': 48.9952, 'lng': 2.3752, 'cc': 'fr'}",
    "{'name': 'Park Ji-sung (Geburtsort: Goheung-gun, Südkorea)', 'lat': 34.6037, 'lng': 127.2738, 'cc': 'kr'}",
    "{'name': 'Son Heung-min (Geburtsort: Chuncheon, Südkorea)', 'lat': 37.8813, 'lng': 127.7298, 'cc': 'kr'}",
    "{'name': 'Hidetoshi Nakata (Geburtsort: Kofu, Japan)', 'lat': 35.6639, 'lng': 138.5686, 'cc': 'jp'}",
    "{'name': 'Cafu (Geburtsort: Sao Paulo, Brasilien)', 'lat': -23.5505, 'lng': -46.6333, 'cc': 'br'}",
    "{'name': 'Kaka (Geburtsort: Brasília, Brasilien)', 'lat': -15.7801, 'lng': -47.9292, 'cc': 'br'}",
    "{'name': 'Xavi Hernández (Geburtsort: Terrassa, Spanien)', 'lat': 41.5638, 'lng': 2.0090, 'cc': 'es'}",
    "{'name': 'Andrés Iniesta (Geburtsort: Fuentealbilla, Spanien)', 'lat': 39.3358, 'lng': -1.7158, 'cc': 'es'}",
    "{'name': 'Gareth Bale (Geburtsort: Cardiff, Wales)', 'lat': 51.4816, 'lng': -3.1791, 'cc': 'gb'}",
    "{'name': 'Wayne Rooney (Geburtsort: Liverpool/Croxteth, England)', 'lat': 53.4308, 'lng': -2.9608, 'cc': 'gb'}",
    "{'name': 'David Beckham (Geburtsort: Leytonstone, London)', 'lat': 51.5689, 'lng': 0.0055, 'cc': 'gb'}",
    "{'name': 'George Best (Geburtsort: Belfast, Nordirland)', 'lat': 54.5973, 'lng': -5.9301, 'cc': 'gb'}",
]
NEW_FLEG = (
    "'Lev Yashin (Geburtsort: Moskau, Russland)', 'lat': 55.7558, 'lng': 37.6173, 'cc': 'ru'}, "
    + ", ".join(NEW_FLEG_TAIL) + "]}"
)
patch(OLD_FLEG, NEW_FLEG, "fussball_legenden +37")

# --- olympische_rekorde: 12 -> 50 (+38) ---
OLD_OLY = "'Katarina Witt (2x Gold Eiskunstlauf – Geburtsort: Staaken, DDR/Deutschland)', 'lat': 52.5312, 'lng': 13.1208, 'cc': 'de'}]}"
NEW_OLY_TAIL = [
    "{'name': 'Usain Bolt (100m/200m Weltrekord – Geburtsort: Sherwood Content, Jamaika)', 'lat': 18.3588, 'lng': -77.6890, 'cc': 'jm'}",
    "{'name': 'Michael Phelps (23x Olympiagold Schwimmen – Geburtsort: Baltimore, USA)', 'lat': 39.2904, 'lng': -76.6122, 'cc': 'us'}",
    "{'name': 'Carl Lewis (9x Olympiagold Leichtathletik – Geburtsort: Birmingham, USA)', 'lat': 33.5207, 'lng': -86.8025, 'cc': 'us'}",
    "{'name': 'Jesse Owens (4x Gold Berlin 1936 – Geburtsort: Oakville, Alabama, USA)', 'lat': 33.2148, 'lng': -87.3903, 'cc': 'us'}",
    "{'name': 'Nadia Comaneci (erste Zehn in der Turngeschichte – Geburtsort: Onesti, Rumänien)', 'lat': 46.2483, 'lng': 26.7289, 'cc': 'ro'}",
    "{'name': 'Simone Biles (7x Olympiagold Turnen – Geburtsort: Columbus, USA)', 'lat': 39.9612, 'lng': -82.9988, 'cc': 'us'}",
    "{'name': 'Eliud Kipchoge (Marathon-Weltrekord – Geburtsort: Kapsisiywa, Kenia)', 'lat': 0.5167, 'lng': 35.4000, 'cc': 'ke'}",
    "{'name': 'Haile Gebrselassie (10.000m Weltrekord – Geburtsort: Asela, Äthiopien)', 'lat': 7.9500, 'lng': 39.1333, 'cc': 'et'}",
    "{'name': 'Kenenisa Bekele (5000m/10000m WR – Geburtsort: Bekoji, Äthiopien)', 'lat': 7.9281, 'lng': 39.2364, 'cc': 'et'}",
    "{'name': 'Marit Bjørgen (15x Olympia-Ski-Nordisch – Geburtsort: Trondheim, Norwegen)', 'lat': 63.4305, 'lng': 10.3951, 'cc': 'no'}",
    "{'name': 'Ole Einar Bjørndalen (8x Biathlon-Gold – Geburtsort: Drammen, Norwegen)', 'lat': 59.7440, 'lng': 10.2044, 'cc': 'no'}",
    "{'name': 'Bjørn Dählie (8x Ski-Nordisch-Gold – Geburtsort: Elverum, Norwegen)', 'lat': 60.8800, 'lng': 11.5600, 'cc': 'no'}",
    "{'name': 'Paavo Nurmi (9x Olympiagold Laufen – Geburtsort: Turku, Finnland)', 'lat': 60.4518, 'lng': 22.2666, 'cc': 'fi'}",
    "{'name': 'Emil Zátopek (4x Gold 1948/1952 – Geburtsort: Koprivnice, Tschechien)', 'lat': 49.5996, 'lng': 18.1396, 'cc': 'cz'}",
    "{'name': 'Fanny Blankers-Koen (4x Gold 1948 – Geburtsort: Lisse, Niederlande)', 'lat': 52.2558, 'lng': 4.5573, 'cc': 'nl'}",
    "{'name': 'Greg Louganis (4x Springturm-Gold – Geburtsort: El Cajon, USA)', 'lat': 32.7948, 'lng': -116.9625, 'cc': 'us'}",
    "{'name': 'Mark Spitz (9x Schwimmgold 1968/72 – Geburtsort: Modesto, USA)', 'lat': 37.6391, 'lng': -120.9969, 'cc': 'us'}",
    "{'name': 'Larisa Latynina (9x Turnergold – Geburtsort: Cherson, Ukraine)', 'lat': 46.6354, 'lng': 32.6169, 'cc': 'ua'}",
    "{'name': 'Vera Caslavska (7x Turnergold – Geburtsort: Prag, Tschechien)', 'lat': 50.0755, 'lng': 14.4378, 'cc': 'cz'}",
    "{'name': 'Oksana Baiul (Eiskunstlauf Gold 1994 – Geburtsort: Dnipro, Ukraine)', 'lat': 48.4647, 'lng': 35.0462, 'cc': 'ua'}",
    "{'name': 'Eric Heiden (5x Eisschnelllauf-Gold 1980 – Geburtsort: Madison, USA)', 'lat': 43.0731, 'lng': -89.4012, 'cc': 'us'}",
    "{'name': 'Ireen Wüst (6x Eisschnelllauf-Gold – Geburtsort: Goirle, Niederlande)', 'lat': 51.5186, 'lng': 5.0700, 'cc': 'nl'}",
    "{'name': 'Mikaela Shiffrin (3x Ski-Alpin-Gold – Geburtsort: Vail, Colorado, USA)', 'lat': 39.6433, 'lng': -106.3781, 'cc': 'us'}",
    "{'name': 'Hermann Maier (2x Ski-Alpin-Gold – Geburtsort: Altenmarkt, Österreich)', 'lat': 47.3783, 'lng': 13.4533, 'cc': 'at'}",
    "{'name': 'Roger Federer (Tennis 2008 Gold – Geburtsort: Basel, Schweiz)', 'lat': 47.5596, 'lng': 7.5886, 'cc': 'ch'}",
    "{'name': 'Serena Williams (4x Tennis-Gold – Geburtsort: Saginaw, Michigan, USA)', 'lat': 43.4195, 'lng': -83.9508, 'cc': 'us'}",
    "{'name': 'Steffi Graf (Golden Slam 1988 – Geburtsort: Brühl, Deutschland)', 'lat': 49.3997, 'lng': 8.5280, 'cc': 'de'}",
    "{'name': 'Naim Süleymanoglu (3x Gewichtheben-Gold – Geburtsort: Pitchar, Bulgarien)', 'lat': 41.6858, 'lng': 25.3229, 'cc': 'bg'}",
    "{'name': 'Deng Yaping (4x Tischtennis-Gold – Geburtsort: Zhengzhou, China)', 'lat': 34.7466, 'lng': 113.6253, 'cc': 'cn'}",
    "{'name': 'Li Ning (6x Turnergold 1984 – Geburtsort: Liuzhou, China)', 'lat': 24.3258, 'lng': 109.4229, 'cc': 'cn'}",
    "{'name': 'Yelena Isinbayeva (2x Stabhochsprung-Gold – Geburtsort: Wolgograd, Russland)', 'lat': 48.7086, 'lng': 44.5147, 'cc': 'ru'}",
    "{'name': 'Yulimar Rojas (Dreisprung-Weltrekordhalterin – Geburtsort: Caracas, Venezuela)', 'lat': 10.4806, 'lng': -66.9036, 'cc': 've'}",
    "{'name': 'Eliud Kipchoge Trainingsort (Kaptagat, Kenia – Hochhöhentraining 2400m)', 'lat': 0.4800, 'lng': 35.5300, 'cc': 'ke'}",
    "{'name': 'Sydney Van Dyck (Schwimm-Goldmedaille – Cape Town, Südafrika)', 'lat': -33.9249, 'lng': 18.4241, 'cc': 'za'}",
    "{'name': 'Luvo Manyonga (Weitsprung-Gold – Geburtsort: Mbekweni, Südafrika)', 'lat': -33.8792, 'lng': 18.9622, 'cc': 'za'}",
    "{'name': 'Almaz Ayana (10.000m Weltrekord – Geburtsort: Arsi Zone, Äthiopien)', 'lat': 7.5500, 'lng': 39.5000, 'cc': 'et'}",
    "{'name': 'Tirunesh Dibaba (3x Gold Laufen – Geburtsort: Bekoji, Äthiopien)', 'lat': 7.9281, 'lng': 39.2364, 'cc': 'et'}",
    "{'name': 'Derartu Tulu (2x Gold 10.000m – Geburtsort: Bekoji, Äthiopien)', 'lat': 7.9281, 'lng': 39.2364, 'cc': 'et'}",
]
NEW_OLY = (
    "'Katarina Witt (2x Gold Eiskunstlauf – Geburtsort: Staaken, DDR/Deutschland)', 'lat': 52.5312, 'lng': 13.1208, 'cc': 'de'}, "
    + ", ".join(NEW_OLY_TAIL) + "]}"
)
patch(OLD_OLY, NEW_OLY, "olympische_rekorde +38")

# ============================================================
# PART 2: UEFA_STADIUMS_DATA 28 -> 50 (+22)
# ============================================================
OLD_UEFA_END = '{"name":"Stade Louis II","city":"Monaco","cc":"mc","lat":43.7272,"lng":7.4148}\n];'
NEW_UEFA_EXTRA = (
    ',\n{"name":"Camp Nou","city":"Barcelona","cc":"es","lat":41.3809,"lng":2.1228}'
    ',\n{"name":"Allianz Arena","city":"München","cc":"de","lat":48.2188,"lng":11.6248}'
    ',\n{"name":"Tottenham Hotspur Stadium","city":"London","cc":"gb","lat":51.6042,"lng":-0.0665}'
    ',\n{"name":"Estadio Santiago Bernébau","city":"Madrid","cc":"es","lat":40.4531,"lng":-3.6883}'
    ',\n{"name":"San Siro / Giuseppe Meazza","city":"Mailand","cc":"it","lat":45.4781,"lng":9.1240}'
    ',\n{"name":"Celtic Park","city":"Glasgow","cc":"gb","lat":55.8490,"lng":-4.2057}'
    ',\n{"name":"Estadio do Dragão","city":"Porto","cc":"pt","lat":41.1619,"lng":-8.5836}'
    ',\n{"name":"Juventus Stadium / Allianz Stadium","city":"Turin","cc":"it","lat":45.1096,"lng":7.6413}'
    ',\n{"name":"Fenerbahce Sukru Saracoglu","city":"Istanbul","cc":"tr","lat":40.9938,"lng":29.0337}'
    ',\n{"name":"Galatasaray Nef Stadyumu","city":"Istanbul","cc":"tr","lat":41.0717,"lng":29.0106}'
    ',\n{"name":"Maracanã","city":"Rio de Janeiro","cc":"br","lat":-22.9122,"lng":-43.2302}'
    ',\n{"name":"Estadio Azteca","city":"Mexiko-Stadt","cc":"mx","lat":19.3031,"lng":-99.1506}'
    ',\n{"name":"FNB Stadium (Soccer City)","city":"Johannesburg","cc":"za","lat":-26.2344,"lng":27.9849}'
    ',\n{"name":"Melbourne Cricket Ground","city":"Melbourne","cc":"au","lat":-37.8200,"lng":144.9836}'
    ',\n{"name":"National Stadium Bird\'s Nest","city":"Peking","cc":"cn","lat":39.9929,"lng":116.3912}'
    ',\n{"name":"Tokyo Olympic Stadium","city":"Tokio","cc":"jp","lat":35.6771,"lng":139.7163}'
    ',\n{"name":"Lusail Iconic Stadium","city":"Lusail","cc":"qa","lat":25.4366,"lng":51.5089}'
    ',\n{"name":"King Fahd International Stadium","city":"Riad","cc":"sa","lat":24.5714,"lng":46.7219}'
    ',\n{"name":"Estadio Monumental","city":"Buenos Aires","cc":"ar","lat":-34.5451,"lng":-58.4498}'
    ',\n{"name":"Rose Bowl","city":"Los Angeles","cc":"us","lat":34.1614,"lng":-118.1678}'
    ',\n{"name":"AT&T Stadium","city":"Dallas","cc":"us","lat":32.7479,"lng":-97.0945}'
    ',\n{"name":"MetLife Stadium","city":"New York/New Jersey","cc":"us","lat":40.8128,"lng":-74.0742}'
)
NEW_UEFA_END = '{"name":"Stade Louis II","city":"Monaco","cc":"mc","lat":43.7272,"lng":7.4148}' + NEW_UEFA_EXTRA + '\n];'
patch(OLD_UEFA_END, NEW_UEFA_END, "UEFA_STADIUMS_DATA +22")

# ============================================================
# PART 5: Remove BETA emojis
# ============================================================
# \U0001F9EA + space in Python strings
count_py = content.count('\\U0001F9EA ')
if count_py:
    content = content.replace('\\U0001F9EA ', '')
    print(f'[OK]   BETA \\U0001F9EA removal ({count_py} occurrences)')
else:
    print('[SKIP] BETA Python: none found')

# \u{1F9EA} + space in JS strings
count_js = content.count('\\u{1F9EA} ')
if count_js:
    content = content.replace('\\u{1F9EA} ', '')
    print(f'[OK]   BETA \\u{{1F9EA}} removal ({count_js} occurrences)')
else:
    print('[SKIP] BETA JS: none found')

# literal 🧪 + space
BETA_LIT = '\U0001F9EA '
count_lit = content.count(BETA_LIT)
if count_lit:
    content = content.replace(BETA_LIT, '')
    print(f'[OK]   BETA literal removal ({count_lit} occurrences)')
else:
    print('[SKIP] BETA literal: none found')

# ============================================================
# Write gen.py
# ============================================================
with open(GEN, 'w', encoding='utf-8') as f:
    f.write(content)
print('\ngen.py updated.')

# ============================================================
# PART 3: geo_pin.json
# ============================================================
GEO_PIN = DATA + '/geo_pin.json'
with open(GEO_PIN, encoding='utf-8') as f:
    geo_pin = json.load(f)

geo_pin['geo_fossilien_fundstaetten']['items'].extend([
    {"n": "Dinosaur National Monument (Utah/Colorado, USA)", "lat": 40.4375, "lng": -108.9898},
    {"n": "Morrison Formation (Colorado, USA)", "lat": 39.6500, "lng": -105.0000},
    {"n": "La Brea Tar Pits (Los Angeles, USA)", "lat": 34.0638, "lng": -118.3553},
    {"n": "Tendaguru (Tansania – Brachiosauruslagerstatte)", "lat": -10.0000, "lng": 39.0000},
    {"n": "Ghost Ranch (New Mexico, USA – Coelophysis)", "lat": 36.3261, "lng": -106.4837},
    {"n": "Isle of Sheppey (Kent, England – Eozane Fossilien)", "lat": 51.3930, "lng": 0.7800},
    {"n": "Liaoning (China – gefiederte Dinosaurier)", "lat": 41.5000, "lng": 122.0000},
    {"n": "Yixian Formation (Innere Mongolei, China)", "lat": 41.3000, "lng": 120.8000},
    {"n": "Karoo Basin (Sudafrika – Therapsida)", "lat": -32.5000, "lng": 24.5000},
    {"n": "Red Deer River (Alberta, Kanada – Ceratopsier)", "lat": 52.2650, "lng": -111.6450},
    {"n": "Hadar (Athiopien – Lucy/Australopithecus)", "lat": 11.4500, "lng": 40.5833},
    {"n": "Olduvai Gorge (Tansania – Homo habilis)", "lat": -2.9948, "lng": 35.3480},
    {"n": "Trinil (Java, Indonesien – Homo erectus)", "lat": -7.5500, "lng": 111.7667},
    {"n": "Zhoukoudian (Peking, China – Peking-Mensch)", "lat": 39.7083, "lng": 115.9300},
    {"n": "Chengjiang Fauna (Yunnan, China – Kambrische Explosion)", "lat": 24.6770, "lng": 102.9750},
    {"n": "Wheeler Shale (Utah, USA – Trilobiten)", "lat": 39.0500, "lng": -113.0167},
    {"n": "Mazon Creek (Illinois, USA – Karbon-Fossilien)", "lat": 41.4356, "lng": -88.0539},
    {"n": "Messel Pit UNESCO (Hessen, Deutschland)", "lat": 49.9236, "lng": 8.7511},
    {"n": "Niobrara Chalk (Kansas, USA – Kreide-Meerestiere)", "lat": 39.5000, "lng": -99.5000},
    {"n": "Karoo Hauptfundort (Beaufort West, Sudafrika)", "lat": -32.3576, "lng": 22.5780},
    {"n": "Riversleigh (Queensland, Australien – Megafauna)", "lat": -19.0500, "lng": 138.7000},
    {"n": "Naracoorte Caves (Sudaustralien – Pleistozan)", "lat": -36.9800, "lng": 140.7900},
    {"n": "Wadi Al-Hitan (Agypten – fossile Wale)", "lat": 29.2727, "lng": 30.0500},
    {"n": "Fayum Depression (Agypten – fruhe Primaten)", "lat": 29.3000, "lng": 30.5333},
    {"n": "Afar Triangle (Athiopien – Hominiden-Funde)", "lat": 11.7500, "lng": 40.9167},
    {"n": "Patagonia Chubutensis (Argentinien – Riesensaurier)", "lat": -43.5000, "lng": -66.0000},
    {"n": "Lark Quarry (Queensland, Australien – Dino-Stampede)", "lat": -24.7830, "lng": 142.1330},
    {"n": "Monte Hermoso (Argentinien – fossile Saugetiere)", "lat": -38.9833, "lng": -61.3000},
    {"n": "Phosphorites du Quercy (Frankreich – Eozan)", "lat": 44.5000, "lng": 1.5000},
    {"n": "Kimberley Diamond Mines (Sudafrika – Kimberlitfossilien)", "lat": -28.7316, "lng": 24.7699},
    {"n": "Rapa Nui Fossilien (Osterinsel – endemische Fauna)", "lat": -27.1127, "lng": -109.3497},
    {"n": "Bayan Mandahu (Innere Mongolei, China – Saurier)", "lat": 41.5356, "lng": 107.0300},
])

geo_pin['geo_ozeangraeben']['items'].extend([
    {"n": "Japangraben (Pazifik)", "lat": 38.0, "lng": 143.5},
    {"n": "Peru-Chile-Graben (Sudpazifik)", "lat": -20.0, "lng": -71.0},
    {"n": "Aleuten-Graben (Nordpazifik)", "lat": 52.0, "lng": -172.0},
    {"n": "Nankai-Graben (Japan – Subduktionszone)", "lat": 33.0, "lng": 136.0},
    {"n": "Ryukyu-Graben (Ostchinesisches Meer)", "lat": 25.0, "lng": 127.0},
    {"n": "Cayman-Graben (Karibik)", "lat": 19.7, "lng": -80.0},
    {"n": "Mittelamerikanischer Graben (Pazifik vor Mexiko)", "lat": 12.0, "lng": -92.0},
    {"n": "Diamantina-Zone (Indischer Ozean)", "lat": -33.0, "lng": 101.0},
    {"n": "Banda-Graben (Indonesien)", "lat": -6.5, "lng": 127.0},
    {"n": "Puysegur-Graben (Neuseeland)", "lat": -46.5, "lng": 166.0},
    {"n": "New Hebrides Graben (Vanuatu)", "lat": -16.0, "lng": 167.0},
    {"n": "Kermadec-Graben (Sudpazifik)", "lat": -30.0, "lng": -177.0},
    {"n": "Bougainville-Graben (Papua-Neuguinea)", "lat": -7.0, "lng": 153.0},
    {"n": "Hikurangi-Graben (Neuseeland – Ost)", "lat": -40.0, "lng": 179.0},
    {"n": "Romanche-Graben (Aquatorialer Atlantik)", "lat": 0.2, "lng": -18.5},
    {"n": "South Sandwich-Graben (Sudatlantik)", "lat": -57.0, "lng": -25.0},
    {"n": "Agulhas-Becken (Sudindischer Ozean)", "lat": -40.0, "lng": 26.0},
    {"n": "Macquarie-Graben (Subantarktischer Pazifik)", "lat": -55.0, "lng": 160.0},
    {"n": "Vema-Bruch (Atlantischer Rucken)", "lat": 10.8, "lng": -42.5},
    {"n": "Marianengraben Challenger Deep (tiefster Punkt Erde)", "lat": 11.33, "lng": 142.20},
    {"n": "Aleutian Trench West (Aleuten West)", "lat": 53.0, "lng": 175.0},
    {"n": "Java Deep (Sundagraben tiefster Punkt)", "lat": -11.0, "lng": 109.0},
])

geo_pin['geo_rifts']['items'].extend([
    {"n": "Afar Triple Junction (Athiopien/Eritrea/Dschibuti)", "lat": 11.5, "lng": 41.0},
    {"n": "Albertine Rift (Uganda/DRC/Rwanda)", "lat": -1.0, "lng": 29.5},
    {"n": "Malawi Rift (Lake Malawi)", "lat": -12.0, "lng": 34.5},
    {"n": "Tanganjika-Rift (DRC/Tansania)", "lat": -6.5, "lng": 29.5},
    {"n": "Gregory Rift (Kenia – ostlicher Hauptast)", "lat": 0.5, "lng": 36.0},
    {"n": "Natron-Rift (Tansania – aktive Vulkane)", "lat": -2.4, "lng": 36.1},
    {"n": "Erta Ale (Athiopien – Lavaseegraben)", "lat": 13.6, "lng": 40.7},
    {"n": "Dabbahu-Rift (Athiopien – jungste Riftspalte 2005)", "lat": 12.6, "lng": 40.5},
    {"n": "Rheingraben (Deutschland/Frankreich)", "lat": 48.0, "lng": 7.5},
    {"n": "Oslo Graben / Oslo Rift (Norwegen)", "lat": 59.9, "lng": 10.7},
    {"n": "Salton Trough (Sudkalifornien, USA)", "lat": 33.2, "lng": -115.5},
    {"n": "Midcontinent Rift (USA – prakambrisch)", "lat": 47.0, "lng": -88.0},
    {"n": "Snake River Plain (Idaho, USA – Hotspot-Spur)", "lat": 43.5, "lng": -115.0},
    {"n": "West Antarctic Rift (Antarktis)", "lat": -80.0, "lng": -90.0},
    {"n": "Gulf of California Rift (Mexiko)", "lat": 28.0, "lng": -113.0},
    {"n": "Benue Trough (Nigeria – Kreide-Rift)", "lat": 8.0, "lng": 9.5},
    {"n": "North Sea Rift / Wikinggraben", "lat": 58.0, "lng": 2.5},
    {"n": "Shanxi Rift (China – aktive Seismik)", "lat": 38.0, "lng": 112.5},
    {"n": "Limagne-Graben (Auvergne, Frankreich)", "lat": 45.75, "lng": 3.13},
    {"n": "Massif Central Rift (Frankreich)", "lat": 45.5, "lng": 3.0},
    {"n": "Suez-Rift (Agypten)", "lat": 29.9, "lng": 32.6},
    {"n": "Aden-Rucken (Golf von Aden)", "lat": 12.5, "lng": 44.0},
    {"n": "Juan de Fuca Ridge (Nordostpazifik)", "lat": 48.0, "lng": -130.0},
    {"n": "Pannonian Becken (Ungarn – ehemaliger Rift)", "lat": 47.0, "lng": 18.0},
    {"n": "Dniepr-Donez Rift (Ukraine – Karbon-Rift)", "lat": 49.5, "lng": 33.0},
    {"n": "Carlsberg Ridge (Nordindischer Ozean)", "lat": 5.0, "lng": 62.0},
    {"n": "Rio Grande Rift Nordteil (Colorado, USA)", "lat": 37.5, "lng": -106.0},
])

geo_pin['geo_nationalparks_geologie']['items'].extend([
    {"n": "Grand Canyon National Park (Arizona, USA)", "lat": 36.0544, "lng": -112.1401},
    {"n": "Arches National Park (Utah, USA)", "lat": 38.7331, "lng": -109.5925},
    {"n": "Bryce Canyon National Park (Utah, USA)", "lat": 37.5930, "lng": -112.1871},
    {"n": "Zion National Park (Utah, USA)", "lat": 37.2982, "lng": -113.0263},
    {"n": "Canyonlands National Park (Utah, USA)", "lat": 38.2000, "lng": -109.9300},
    {"n": "Cappadocia (Feenkamine – Turkei)", "lat": 38.6431, "lng": 34.8289},
    {"n": "Giant's Causeway (Nordirland)", "lat": 55.2408, "lng": -6.5116},
    {"n": "Zhangjiajie National Forest (Hunan, China)", "lat": 29.3190, "lng": 110.4340},
    {"n": "Guilin Karst (Guangxi, China)", "lat": 25.2740, "lng": 110.2900},
    {"n": "Jiuzhaigou Valley (Sichuan, China)", "lat": 33.2600, "lng": 103.9170},
    {"n": "Bungle Bungle / Purnululu (Westaustralien)", "lat": -17.5000, "lng": 128.4000},
    {"n": "Devils Tower (Wyoming, USA)", "lat": 44.5903, "lng": -104.7146},
    {"n": "Uluru / Ayers Rock (Northern Territory, Australien)", "lat": -25.3444, "lng": 131.0369},
    {"n": "Perito Moreno Gletscher-Park (Argentinien)", "lat": -50.4970, "lng": -73.1430},
    {"n": "Torres del Paine (Chile – Granitnadeln)", "lat": -51.0000, "lng": -73.0000},
    {"n": "Socotra (Jemen – Drachenblutbaume, UNESCO)", "lat": 12.5000, "lng": 53.8333},
    {"n": "Meteora (Griechenland – Sandsteinfelsen)", "lat": 39.7217, "lng": 21.6306},
    {"n": "Goreme National Park / Kappadokien (Turkei)", "lat": 38.6448, "lng": 34.8294},
    {"n": "Wadi Rum (Jordanien – Rote Wustenfelsen)", "lat": 29.5760, "lng": 35.4260},
    {"n": "Namib-Naukluft Park / Sossusvlei (Namibia)", "lat": -24.7274, "lng": 15.2897},
    {"n": "Virunga National Park (DRC – Nyiragongo Vulkan)", "lat": -1.5000, "lng": 29.2000},
    {"n": "Kilimanjaro NP (Tansania – Schildvulkan-Massiv)", "lat": -3.0674, "lng": 37.3556},
    {"n": "Ngorongoro Crater (Tansania – Vulkankrater)", "lat": -3.2096, "lng": 35.4972},
    {"n": "Drakensberg (Sudafrika – Basaltescarpment)", "lat": -29.5000, "lng": 29.3000},
    {"n": "Ha Long Bay (Vietnam – Karstformation)", "lat": 20.9101, "lng": 107.1839},
    {"n": "Phang Nga Bay (Thailand – Karstinseln)", "lat": 8.2722, "lng": 98.5013},
    {"n": "Palawan Underground River (Philippinen)", "lat": 10.1775, "lng": 118.9270},
    {"n": "Iguazu National Park (Argentinien/Brasilien)", "lat": -25.6953, "lng": -54.4367},
    {"n": "Petrified Forest NP (Arizona, USA – versteinerte Baume)", "lat": 34.9100, "lng": -109.8068},
    {"n": "Pinnacles NP (Kaliformien, USA – Basaltformationen)", "lat": 36.4906, "lng": -121.1825},
    {"n": "Zhangye Danxia (Gansu, China – Regenbogenberge)", "lat": 38.9303, "lng": 100.2553},
    {"n": "Danakil-Senke (Athiopien – tiefste Stelle Afrikas)", "lat": 14.2300, "lng": 40.2900},
])

with open(GEO_PIN, 'w', encoding='utf-8') as f:
    json.dump(geo_pin, f, ensure_ascii=False, indent=2)
print('geo_pin.json updated.')

# ============================================================
# PART 4: kultur.json
# ============================================================
KULTUR = DATA + '/kultur.json'
with open(KULTUR, encoding='utf-8') as f:
    kultur = json.load(f)

# hohe_stadien: 9 -> 30 (+21)
kultur['hohe_stadien'].extend([
    {"n": "Estadio Monumental Virgen de Copacabana 3860m (Peru)", "lat": -15.84, "lng": -70.02},
    {"n": "Estadio Patria 3650m (Sucre, Bolivien)", "lat": -19.05, "lng": -65.26},
    {"n": "Estadio Heroes de Abril 3630m (Oruro, Bolivien)", "lat": -17.97, "lng": -67.11},
    {"n": "Estadio Federativo 3600m (La Paz, Bolivien)", "lat": -16.50, "lng": -68.12},
    {"n": "Estadio Tahuichi Aguilera 2800m (Cochabamba, Bolivien)", "lat": -17.39, "lng": -66.16},
    {"n": "Estadio 12 de Octubre 2800m (Ibarra, Ecuador)", "lat": 0.35, "lng": -78.12},
    {"n": "Estadio Ciudad de Cuenca 2580m (Cuenca, Ecuador)", "lat": -2.90, "lng": -79.00},
    {"n": "Estadio Rodrigo Paz Delgado 2812m (Quito, Ecuador)", "lat": -0.19, "lng": -78.52},
    {"n": "Estadio Nemesio Camacho El Campin 2640m (Bogota)", "lat": 4.65, "lng": -74.08},
    {"n": "Estadio Chinchero 3800m (Cusco, Peru - geplant)", "lat": -13.42, "lng": -72.04},
    {"n": "Estadio Azteca 2240m (Mexiko-Stadt)", "lat": 19.30, "lng": -99.15},
    {"n": "Toluca Estadio Nemesio Diez 2680m (Mexiko)", "lat": 19.29, "lng": -99.67},
    {"n": "Coors Field Baseball 1609m (Denver, USA)", "lat": 39.76, "lng": -104.99},
    {"n": "Empower Field 1609m (Denver Broncos, USA)", "lat": 39.74, "lng": -105.02},
    {"n": "Loftus Versfeld 1340m (Pretoria, Sudafrika)", "lat": -25.75, "lng": 28.22},
    {"n": "Ellis Park 1753m (Johannesburg, Sudafrika)", "lat": -26.19, "lng": 28.05},
    {"n": "Rwandas Amahoro Stadium 1567m (Kigali, Rwanda)", "lat": -1.95, "lng": 30.10},
    {"n": "Nakivubo Stadium 1190m (Kampala, Uganda)", "lat": 0.31, "lng": 32.58},
    {"n": "Estadio Monumental (Lima, Peru) 154m", "lat": -12.06, "lng": -77.05},
    {"n": "Estadio Romelio Martinez 0m (Barranquilla, Kolumbien)", "lat": 10.97, "lng": -74.81},
    {"n": "Estadio Atanasio Girardot 1495m (Medellin, Kolumbien)", "lat": 6.26, "lng": -75.60},
])

# leichtathletik_wm: 13 -> 19 (+6 missing editions)
# Current: 1983, 1987, 1991, 1993, 1997, 1999, 2009, 2013, 2015, 2017, 2019, 2022, 2023
# Missing: 2001, 2003, 2005, 2007, 2011, 2025
kultur['leichtathletik_wm'].extend([
    {"n": "2001 Edmonton", "lat": 53.55, "lng": -113.47},
    {"n": "2003 Paris", "lat": 48.86, "lng": 2.35},
    {"n": "2005 Helsinki", "lat": 60.17, "lng": 24.93},
    {"n": "2007 Osaka", "lat": 34.69, "lng": 135.50},
    {"n": "2011 Daegu", "lat": 35.87, "lng": 128.60},
    {"n": "2025 Tokio", "lat": 35.69, "lng": 139.69},
])

with open(KULTUR, 'w', encoding='utf-8') as f:
    json.dump(kultur, f, ensure_ascii=False, indent=2)
print('kultur.json updated.')

print('\nAll patches applied successfully.')
