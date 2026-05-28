"""
patch_262_sport_massive.py
Phase 262 — Sport-Wissen Massive Expansion
Skaliert sport_pin.json, sport_hl.json, sport_match.json von 8-10 auf 40-60 Items.
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
# sport_pin.json
# ============================================================
pin = jload("sport_pin.json")

# --- sport_fussballstadien (Ziel: 50+) ---
fussball_new = [
    {"n": "Maracanã (Rio de Janeiro, Brasilien)", "lat": -22.91, "lng": -43.23},
    {"n": "Aztekenstadion (Mexiko-Stadt, Mexiko)", "lat": 19.30, "lng": -99.15},
    {"n": "Old Trafford (Manchester, England)", "lat": 53.46, "lng": -2.29},
    {"n": "Anfield (Liverpool, England)", "lat": 53.43, "lng": -2.96},
    {"n": "Emirates Stadium (London, England)", "lat": 51.55, "lng": -0.11},
    {"n": "Stamford Bridge (London, England)", "lat": 51.48, "lng": -0.19},
    {"n": "Santiago Bernabéu (Madrid, Spanien)", "lat": 40.45, "lng": -3.69},
    {"n": "Metropolitano (Madrid, Spanien)", "lat": 40.44, "lng": -3.60},
    {"n": "San Siro (Mailand, Italien)", "lat": 45.48, "lng": 9.12},
    {"n": "Stadio Olimpico (Rom, Italien)", "lat": 41.93, "lng": 12.45},
    {"n": "Juventus Stadium (Turin, Italien)", "lat": 45.11, "lng": 7.64},
    {"n": "Signal Iduna Park (Dortmund, Deutschland)", "lat": 51.49, "lng": 7.45},
    {"n": "Volksparkstadion (Hamburg, Deutschland)", "lat": 53.59, "lng": 9.90},
    {"n": "Red Bull Arena (Leipzig, Deutschland)", "lat": 51.35, "lng": 12.35},
    {"n": "Olympiastadion Berlin (Deutschland)", "lat": 52.51, "lng": 13.24},
    {"n": "Parc des Princes (Paris, Frankreich)", "lat": 48.84, "lng": 2.25},
    {"n": "Stade de France (Saint-Denis, Frankreich)", "lat": 48.92, "lng": 2.36},
    {"n": "Johan Cruyff Arena (Amsterdam, Niederlande)", "lat": 52.31, "lng": 4.94},
    {"n": "Friends Arena (Stockholm, Schweden)", "lat": 59.37, "lng": 17.99},
    {"n": "Celtic Park (Glasgow, Schottland)", "lat": 55.85, "lng": -4.21},
    {"n": "Ibrox Stadium (Glasgow, Schottland)", "lat": 55.85, "lng": -4.31},
    {"n": "Estádio do Dragão (Porto, Portugal)", "lat": 41.16, "lng": -8.58},
    {"n": "Estádio da Luz (Lissabon, Portugal)", "lat": 38.75, "lng": -9.18},
    {"n": "Luzhniki (Moskau, Russland)", "lat": 55.73, "lng": 37.56},
    {"n": "Besiktas Vodafone Park (Istanbul, Türkei)", "lat": 41.04, "lng": 29.01},
    {"n": "Atatürk Olympiastadion (Istanbul, Türkei)", "lat": 41.07, "lng": 28.77},
    {"n": "Nou Mestalla (Valencia, Spanien)", "lat": 39.47, "lng": -0.36},
    {"n": "Sánchez Pizjuán (Sevilla, Spanien)", "lat": 37.38, "lng": -5.97},
    {"n": "Croke Park (Dublin, Irland)", "lat": 53.36, "lng": -6.25},
    {"n": "Lusail Iconic Stadium (Lusail, Katar)", "lat": 25.43, "lng": 51.52},
    {"n": "Al Bayt Stadium (Al Khor, Katar)", "lat": 25.67, "lng": 51.52},
    {"n": "National Stadium (Singapur)", "lat": 1.30, "lng": 103.87},
    {"n": "Melbourne Cricket Ground (Melbourne, Australien)", "lat": -37.82, "lng": 144.98},
    {"n": "Stadium Australia (Sydney, Australien)", "lat": -33.85, "lng": 151.06},
    {"n": "FNB Stadium / Soccer City (Johannesburg, Südafrika)", "lat": -26.24, "lng": 27.98},
    {"n": "Cape Town Stadium (Kapstadt, Südafrika)", "lat": -33.90, "lng": 18.41},
    {"n": "Estadio Monumental (Buenos Aires, Argentinien)", "lat": -34.54, "lng": -58.45},
    {"n": "Estadio Nacional (Lima, Peru)", "lat": -12.07, "lng": -77.03},
    {"n": "Estadio Mineirao (Belo Horizonte, Brasilien)", "lat": -19.87, "lng": -43.97},
    {"n": "Stade Mohamed V (Casablanca, Marokko)", "lat": 33.58, "lng": -7.62},
    {"n": "Khalifa International Stadium (Doha, Katar)", "lat": 25.26, "lng": 51.45},
    {"n": "Rose Bowl (Pasadena, USA)", "lat": 34.16, "lng": -118.17},
    {"n": "MetLife Stadium (New Jersey, USA)", "lat": 40.81, "lng": -74.07},
    {"n": "Levi's Stadium (Santa Clara, USA)", "lat": 37.40, "lng": -121.97},
]

# --- sport_olympiastadien (Ziel: 45+) ---
olympia_new = [
    {"n": "Nationalstadion (Peking, China)", "lat": 39.99, "lng": 116.40},
    {"n": "Olympic Stadium (Tokio, Japan)", "lat": 35.68, "lng": 139.71},
    {"n": "Nilufar Shamsutdinova Komplex (Taschkent, Usbekistan)", "lat": 41.30, "lng": 69.25},
    {"n": "Olympic Stadium (München, Deutschland)", "lat": 48.17, "lng": 11.55},
    {"n": "Olympic Stadium (Montreal, Kanada)", "lat": 45.56, "lng": -73.55},
    {"n": "Olympiastadion Athen (Griechenland)", "lat": 38.00, "lng": 23.78},
    {"n": "Luzhniki Stadion (Moskau, Russland)", "lat": 55.73, "lng": 37.56},
    {"n": "Seoul Olympic Stadium (Seoul, Südkorea)", "lat": 37.52, "lng": 127.07},
    {"n": "Barcelona Olympic Stadium (Spanien)", "lat": 41.36, "lng": 2.15},
    {"n": "Centennial Olympic Stadium (Atlanta, USA)", "lat": 33.74, "lng": -84.39},
    {"n": "Stadium Australia (Sydney, Australien)", "lat": -33.85, "lng": 151.06},
    {"n": "Stadio Olimpico (Turin, Italien)", "lat": 45.04, "lng": 7.66},
    {"n": "Olympic Stadium (London, England)", "lat": 51.54, "lng": -0.02},
    {"n": "Estádio Olímpico João Havelange (Rio, Brasilien)", "lat": -22.88, "lng": -43.18},
    {"n": "Tokyo National Olympic Stadium (Japan, 1964)", "lat": 35.68, "lng": 139.71},
    {"n": "Olympic Stadium (Helsinki, Finnland)", "lat": 60.19, "lng": 24.92},
    {"n": "Wembley Empire (London, 1948)", "lat": 51.56, "lng": -0.28},
    {"n": "Parc des Princes (Paris, 1900)", "lat": 48.84, "lng": 2.25},
    {"n": "Olympic Stadium Amsterdam (Niederlande)", "lat": 52.34, "lng": 4.86},
    {"n": "Stade de Colombes (Paris, 1924)", "lat": 48.92, "lng": 2.25},
    {"n": "White City Stadium (London, 1908)", "lat": 51.51, "lng": -0.22},
    {"n": "Panathinaiko Stadion (Athen, 1896)", "lat": 37.97, "lng": 23.74},
    {"n": "Los Angeles Memorial Coliseum (USA)", "lat": 34.01, "lng": -118.29},
    {"n": "Bird's Nest (Peking, 2008)", "lat": 39.99, "lng": 116.40},
    {"n": "SoFi Stadium (Los Angeles, USA 2028)", "lat": 33.95, "lng": -118.34},
    {"n": "Stade de France (Paris, 2024)", "lat": 48.92, "lng": 2.36},
    {"n": "Melbourne Cricket Ground (Australien, 1956)", "lat": -37.82, "lng": 144.98},
    {"n": "Estadio Olímpico Universitario (Mexiko, 1968)", "lat": 19.32, "lng": -99.18},
    {"n": "Ben Hill Griffin Stadium (Gainesville, USA)", "lat": 29.65, "lng": -82.35},
    {"n": "Stade Olympique (Montréal)", "lat": 45.56, "lng": -73.55},
    {"n": "Olympic Green (Peking, Hauptgelände)", "lat": 40.00, "lng": 116.38},
    {"n": "Ariake Arena (Tokio, Japan)", "lat": 35.63, "lng": 139.78},
    {"n": "Olympic Park Stadium (Brisbane, Australien 2032)", "lat": -27.47, "lng": 153.04},
    {"n": "Fisht Olympic Stadium (Sotschi, Russland)", "lat": 43.41, "lng": 39.95},
    {"n": "Olympic Velodrome (Rio de Janeiro, Brasilien)", "lat": -22.97, "lng": -43.38},
    {"n": "Maracanã Olympia 2016 (Rio de Janeiro)", "lat": -22.91, "lng": -43.23},
    {"n": "Olympic Velodrome (London, England)", "lat": 51.54, "lng": -0.02},
]

# --- sport_motorsport_strecken (Ziel: 45+) ---
motor_new = [
    {"n": "Spa-Francorchamps (Belgien)", "lat": 50.44, "lng": 5.97},
    {"n": "Nürburgring Nordschleife (Deutschland)", "lat": 50.33, "lng": 6.94},
    {"n": "Hockenheimring (Deutschland)", "lat": 49.33, "lng": 8.57},
    {"n": "Circuit de Catalunya (Barcelona, Spanien)", "lat": 41.57, "lng": 2.26},
    {"n": "Hungaroring (Budapest, Ungarn)", "lat": 47.58, "lng": 19.25},
    {"n": "Autodromo Enzo e Dino Ferrari (Imola, Italien)", "lat": 44.34, "lng": 11.71},
    {"n": "Mugello Circuit (Toskana, Italien)", "lat": 43.99, "lng": 11.37},
    {"n": "Bahrain International Circuit (Sakhir)", "lat": 26.03, "lng": 50.51},
    {"n": "Yas Marina Circuit (Abu Dhabi, VAE)", "lat": 24.47, "lng": 54.60},
    {"n": "Jeddah Corniche Circuit (Saudi-Arabien)", "lat": 21.63, "lng": 39.10},
    {"n": "Circuit of the Americas (Austin, USA)", "lat": 30.13, "lng": -97.64},
    {"n": "Daytona International Speedway (Florida, USA)", "lat": 29.19, "lng": -81.07},
    {"n": "Indianapolis Motor Speedway (Indiana, USA)", "lat": 39.79, "lng": -86.24},
    {"n": "Talladega Superspeedway (Alabama, USA)", "lat": 33.57, "lng": -86.07},
    {"n": "Watkins Glen International (New York, USA)", "lat": 42.34, "lng": -76.93},
    {"n": "Road Atlanta (Georgia, USA)", "lat": 34.15, "lng": -83.82},
    {"n": "Suzuka Circuit (Japan)", "lat": 34.84, "lng": 136.54},
    {"n": "Fuji Speedway (Japan)", "lat": 35.37, "lng": 138.93},
    {"n": "Motegi Circuit (Japan)", "lat": 36.54, "lng": 140.19},
    {"n": "Shanghai International Circuit (China)", "lat": 31.34, "lng": 121.22},
    {"n": "Sepang International Circuit (Malaysia)", "lat": 2.76, "lng": 101.74},
    {"n": "Marina Bay Street Circuit (Singapur)", "lat": 1.29, "lng": 103.86},
    {"n": "Albert Park Circuit (Melbourne, Australien)", "lat": -37.85, "lng": 144.97},
    {"n": "Interlagos / Autódromo José Carlos Pace (Brasilien)", "lat": -23.70, "lng": -46.70},
    {"n": "Autódromo Hermanos Rodríguez (Mexiko-Stadt)", "lat": 19.40, "lng": -99.09},
    {"n": "Red Bull Ring (Spielberg, Österreich)", "lat": 47.22, "lng": 14.76},
    {"n": "Circuit Zandvoort (Niederlande)", "lat": 52.39, "lng": 4.54},
    {"n": "Baku City Circuit (Aserbaidschan)", "lat": 40.37, "lng": 49.85},
    {"n": "Circuit Gilles Villeneuve (Kanada)", "lat": 45.50, "lng": -73.52},
    {"n": "Miami International Autodrome (USA)", "lat": 25.96, "lng": -80.24},
    {"n": "Las Vegas Street Circuit (Nevada, USA)", "lat": 36.12, "lng": -115.17},
    {"n": "Losail International Circuit (Katar)", "lat": 25.49, "lng": 51.45},
    {"n": "Le Mans Circuit de la Sarthe (Frankreich)", "lat": 47.95, "lng": 0.21},
    {"n": "Goodwood Circuit (England)", "lat": 50.86, "lng": -0.76},
    {"n": "Brands Hatch (England)", "lat": 51.36, "lng": 0.26},
    {"n": "Laguna Seca Raceway (Monterey, USA)", "lat": 36.58, "lng": -121.75},
    {"n": "Kyalami Grand Prix Circuit (Südafrika)", "lat": -25.99, "lng": 28.07},
]

# --- sport_wintersport_orte (Ziel: 45+) ---
winter_new = [
    {"n": "St. Moritz (Graubünden, Schweiz)", "lat": 46.50, "lng": 9.84},
    {"n": "Davos (Graubünden, Schweiz)", "lat": 46.80, "lng": 9.84},
    {"n": "Verbier (Wallis, Schweiz)", "lat": 46.10, "lng": 7.23},
    {"n": "Courchevel (Savoyen, Frankreich)", "lat": 45.42, "lng": 6.63},
    {"n": "Méribel (Savoyen, Frankreich)", "lat": 45.39, "lng": 6.57},
    {"n": "Val d'Isère (Savoyen, Frankreich)", "lat": 45.45, "lng": 6.98},
    {"n": "Chamonix-Mont-Blanc (Frankreich)", "lat": 45.92, "lng": 6.87},
    {"n": "Les Deux Alpes (Isère, Frankreich)", "lat": 45.02, "lng": 6.12},
    {"n": "Megève (Haute-Savoie, Frankreich)", "lat": 45.86, "lng": 6.62},
    {"n": "Cortina d'Ampezzo (Dolomiten, Italien)", "lat": 46.54, "lng": 12.14},
    {"n": "Madonna di Campiglio (Trentino, Italien)", "lat": 46.23, "lng": 10.83},
    {"n": "Sestriere (Piemont, Italien)", "lat": 44.96, "lng": 6.88},
    {"n": "Söll (Tirol, Österreich)", "lat": 47.51, "lng": 12.19},
    {"n": "St. Anton am Arlberg (Tirol, Österreich)", "lat": 47.13, "lng": 10.27},
    {"n": "Sölden (Tirol, Österreich)", "lat": 46.97, "lng": 11.00},
    {"n": "Obertauern (Salzburg, Österreich)", "lat": 47.26, "lng": 13.57},
    {"n": "Lech am Arlberg (Vorarlberg, Österreich)", "lat": 47.21, "lng": 10.14},
    {"n": "Garmisch-Partenkirchen (Bayern, Deutschland)", "lat": 47.49, "lng": 11.09},
    {"n": "Oberstdorf (Allgäu, Deutschland)", "lat": 47.41, "lng": 10.28},
    {"n": "Berchtesgaden (Bayern, Deutschland)", "lat": 47.63, "lng": 13.00},
    {"n": "Zermatt (Wallis, Schweiz)", "lat": 46.02, "lng": 7.75},
    {"n": "Wengen (Bern, Schweiz)", "lat": 46.61, "lng": 7.92},
    {"n": "Adelboden (Bern, Schweiz)", "lat": 46.49, "lng": 7.56},
    {"n": "Grindelwald (Bern, Schweiz)", "lat": 46.62, "lng": 8.04},
    {"n": "Aspen (Colorado, USA)", "lat": 39.19, "lng": -106.82},
    {"n": "Vail (Colorado, USA)", "lat": 39.64, "lng": -106.37},
    {"n": "Park City Mountain Resort (Utah, USA)", "lat": 40.65, "lng": -111.51},
    {"n": "Whistler Blackcomb (British Columbia, Kanada)", "lat": 50.12, "lng": -122.96},
    {"n": "Squaw Valley (Lake Tahoe, USA)", "lat": 39.20, "lng": -120.24},
    {"n": "Breckenridge (Colorado, USA)", "lat": 39.48, "lng": -106.04},
    {"n": "Steamboat Springs (Colorado, USA)", "lat": 40.49, "lng": -106.83},
    {"n": "Sun Valley (Idaho, USA)", "lat": 43.70, "lng": -114.35},
    {"n": "Niseko (Hokkaido, Japan)", "lat": 42.80, "lng": 140.69},
    {"n": "Hakuba (Nagano, Japan)", "lat": 36.70, "lng": 137.86},
    {"n": "Thredbo (New South Wales, Australien)", "lat": -36.51, "lng": 148.30},
    {"n": "Queenstown Skigebiete (Neuseeland)", "lat": -45.03, "lng": 168.66},
    {"n": "Falun (Schweden)", "lat": 60.61, "lng": 15.63},
    {"n": "Lillehammer (Norwegen)", "lat": 61.11, "lng": 10.47},
    {"n": "Holmenkollen (Oslo, Norwegen)", "lat": 59.96, "lng": 10.67},
    {"n": "Ruka (Kuusamo, Finnland)", "lat": 66.17, "lng": 29.17},
    {"n": "Lahti (Finnland)", "lat": 60.98, "lng": 25.66},
    {"n": "Alpe d'Huez (Isère, Frankreich)", "lat": 45.09, "lng": 6.07},
]

# --- sport_grand_slam_arenen (Ziel: 20+) ---
tennis_new = [
    {"n": "Arthur Ashe Stadium (Flushing Meadows, USA)", "lat": 40.75, "lng": -73.85},
    {"n": "Louis Armstrong Stadium (New York, USA)", "lat": 40.75, "lng": -73.85},
    {"n": "Court Philippe-Chatrier (Roland Garros, Frankreich)", "lat": 48.85, "lng": 2.25},
    {"n": "Court Suzanne-Lenglen (Paris, Frankreich)", "lat": 48.84, "lng": 2.25},
    {"n": "Centre Court (Wimbledon, England)", "lat": 51.43, "lng": -0.21},
    {"n": "Court No. 1 (Wimbledon, England)", "lat": 51.43, "lng": -0.21},
    {"n": "Rod Laver Arena (Melbourne, Australien)", "lat": -37.82, "lng": 144.98},
    {"n": "Margaret Court Arena (Melbourne, Australien)", "lat": -37.82, "lng": 144.98},
    {"n": "Wimbledon All England Club (London, England)", "lat": 51.43, "lng": -0.21},
    {"n": "USTA Billie Jean King National Center (New York)", "lat": 40.75, "lng": -73.85},
    {"n": "Foro Italico (Rom, Italien)", "lat": 41.93, "lng": 12.46},
    {"n": "Lawn Tennis Association National Centre (London)", "lat": 51.43, "lng": -0.21},
    {"n": "Stadium Court (Indian Wells, USA)", "lat": 33.72, "lng": -116.38},
    {"n": "Miami Open Stadium (Miami Gardens, USA)", "lat": 25.96, "lng": -80.24},
    {"n": "Madrid Open Caja Mágica (Spanien)", "lat": 40.37, "lng": -3.72},
]

# --- sport_golf_platze (Ziel: 40+) ---
golf_new = [
    {"n": "Augusta National Golf Club (Georgia, USA)", "lat": 33.50, "lng": -82.02},
    {"n": "St Andrews Links (Schottland)", "lat": 56.34, "lng": -2.80},
    {"n": "Pebble Beach Golf Links (Kalifornien, USA)", "lat": 36.57, "lng": -121.95},
    {"n": "Royal Birkdale Golf Club (England)", "lat": 53.61, "lng": -3.04},
    {"n": "Royal St George's (Kent, England)", "lat": 51.28, "lng": 1.39},
    {"n": "Carnoustie Golf Links (Schottland)", "lat": 56.50, "lng": -2.71},
    {"n": "Turnberry (Ayrshire, Schottland)", "lat": 55.33, "lng": -4.82},
    {"n": "Muirfield (East Lothian, Schottland)", "lat": 56.05, "lng": -2.84},
    {"n": "TPC Sawgrass (Ponte Vedra Beach, USA)", "lat": 30.20, "lng": -81.40},
    {"n": "Pinehurst Resort No. 2 (North Carolina, USA)", "lat": 35.19, "lng": -79.47},
    {"n": "Bethpage Black (New York, USA)", "lat": 40.74, "lng": -73.46},
    {"n": "Oakmont Country Club (Pennsylvania, USA)", "lat": 40.52, "lng": -79.83},
    {"n": "Merion Golf Club (Pennsylvania, USA)", "lat": 39.99, "lng": -75.31},
    {"n": "Winged Foot Golf Club (New York, USA)", "lat": 40.96, "lng": -73.79},
    {"n": "Hazeltine National Golf Club (Minnesota, USA)", "lat": 44.74, "lng": -93.59},
    {"n": "Congressional Country Club (Maryland, USA)", "lat": 39.01, "lng": -77.08},
    {"n": "Valderrama Golf Club (Andalusien, Spanien)", "lat": 36.28, "lng": -5.36},
    {"n": "Emirates Golf Club (Dubai, VAE)", "lat": 25.10, "lng": 55.17},
    {"n": "Mission Hills Golf Club (Shenzhen, China)", "lat": 22.60, "lng": 113.92},
    {"n": "Kasumigaseki Country Club (Saitama, Japan)", "lat": 35.93, "lng": 139.39},
    {"n": "Royal Melbourne Golf Club (Australien)", "lat": -37.93, "lng": 145.04},
    {"n": "Kingston Heath Golf Club (Australien)", "lat": -37.94, "lng": 145.03},
    {"n": "Cape Kidnappers (Hawke's Bay, Neuseeland)", "lat": -39.63, "lng": 177.09},
    {"n": "Bandon Dunes (Oregon, USA)", "lat": 43.13, "lng": -124.41},
    {"n": "Shinnecock Hills (New York, USA)", "lat": 40.89, "lng": -72.46},
    {"n": "Kiawah Island Ocean Course (South Carolina, USA)", "lat": 32.62, "lng": -80.08},
    {"n": "Medinah Country Club (Illinois, USA)", "lat": 41.93, "lng": -88.06},
    {"n": "Torrey Pines Golf Course (La Jolla, USA)", "lat": 32.90, "lng": -117.25},
    {"n": "Royal County Down (Newcastle, Nordirland)", "lat": 54.22, "lng": -5.90},
    {"n": "Waterville Golf Links (Kerry, Irland)", "lat": 51.83, "lng": -10.17},
    {"n": "Ballybunion Golf Club (Kerry, Irland)", "lat": 52.51, "lng": -9.67},
    {"n": "Prairie Dunes Country Club (Kansas, USA)", "lat": 37.64, "lng": -98.08},
]

# --- sport_surfspots_welt (Ziel: 45+) ---
surf_new = [
    {"n": "Pipeline (Oahu, Hawaii, USA)", "lat": 21.66, "lng": -158.05},
    {"n": "Jaws / Peahi (Maui, Hawaii, USA)", "lat": 20.95, "lng": -156.33},
    {"n": "Waimea Bay (Oahu, Hawaii, USA)", "lat": 21.64, "lng": -158.07},
    {"n": "Mavericks (Half Moon Bay, Kalifornien)", "lat": 37.49, "lng": -122.50},
    {"n": "Steamer Lane (Santa Cruz, Kalifornien)", "lat": 36.96, "lng": -122.02},
    {"n": "Trestles (San Clemente, Kalifornien)", "lat": 33.40, "lng": -117.59},
    {"n": "Blacks Beach (La Jolla, Kalifornien)", "lat": 32.88, "lng": -117.25},
    {"n": "Teahupo'o (Tahiti, Französisch-Polynesien)", "lat": -17.83, "lng": -149.28},
    {"n": "Banzai Pipeline (North Shore, Hawaii)", "lat": 21.66, "lng": -158.05},
    {"n": "Cloudbreak (Fiji)", "lat": -18.13, "lng": 177.23},
    {"n": "Restaurants / Tavarua (Fiji)", "lat": -17.85, "lng": 177.21},
    {"n": "Uluwatu (Bali, Indonesien)", "lat": -8.83, "lng": 115.09},
    {"n": "Padang Padang (Bali, Indonesien)", "lat": -8.82, "lng": 115.09},
    {"n": "G-Land / Plengkung (Java, Indonesien)", "lat": -8.60, "lng": 114.42},
    {"n": "Desert Point (Lombok, Indonesien)", "lat": -8.73, "lng": 115.90},
    {"n": "Superbank (Gold Coast, Australien)", "lat": -28.03, "lng": 153.44},
    {"n": "Bells Beach (Victoria, Australien)", "lat": -38.37, "lng": 144.28},
    {"n": "Margaret River (Westaustralien)", "lat": -33.96, "lng": 114.95},
    {"n": "Snapper Rocks (Gold Coast, Australien)", "lat": -28.03, "lng": 153.44},
    {"n": "Hossegor / La Gravière (Frankreich)", "lat": 43.66, "lng": -1.42},
    {"n": "Mundaka (Baskenland, Spanien)", "lat": 43.41, "lng": -2.70},
    {"n": "Nazaré (Portugal)", "lat": 39.60, "lng": -9.07},
    {"n": "Ericeira (Portugal)", "lat": 38.96, "lng": -9.42},
    {"n": "Praia do Norte (Nazaré, Portugal)", "lat": 39.61, "lng": -9.07},
    {"n": "Puerto Escondido (Oaxaca, Mexiko)", "lat": 15.87, "lng": -97.07},
    {"n": "Playa Zicatela (Mexiko)", "lat": 15.86, "lng": -97.07},
    {"n": "Todos Santos (Baja California, Mexiko)", "lat": 23.45, "lng": -110.22},
    {"n": "Jeffrey's Bay (Südafrika)", "lat": -34.04, "lng": 24.92},
    {"n": "Dungeons (Kapstadt, Südafrika)", "lat": -34.18, "lng": 18.32},
    {"n": "Skeleton Bay / Donkey Bay (Namibia)", "lat": -22.68, "lng": 14.53},
    {"n": "Thurso East (Schottland)", "lat": 58.59, "lng": -3.52},
    {"n": "Bundoran (Donegal, Irland)", "lat": 54.48, "lng": -8.28},
    {"n": "Coxos (Ericeira, Portugal)", "lat": 38.99, "lng": -9.44},
    {"n": "Punta de Lobos (Chile)", "lat": -34.42, "lng": -72.00},
    {"n": "Arica (Chile)", "lat": -18.47, "lng": -70.33},
    {"n": "Santa Catalina (Panama)", "lat": 7.85, "lng": -80.98},
    {"n": "Salina Cruz (Oaxaca, Mexiko)", "lat": 16.17, "lng": -95.19},
    {"n": "Soup Bowls / Bathsheba (Barbados)", "lat": 13.22, "lng": -59.52},
    {"n": "Rincon (Puerto Rico)", "lat": 18.34, "lng": -67.25},
]

# --- sport_marathonstrecken (Ziel: 40+) ---
marathon_new = [
    {"n": "New York City Marathon (New York, USA)", "lat": 40.60, "lng": -74.05},
    {"n": "Chicago Marathon (Illinois, USA)", "lat": 41.88, "lng": -87.63},
    {"n": "Boston Marathon Ziel (Boylston St., USA)", "lat": 42.35, "lng": -71.08},
    {"n": "Berlin Marathon (Berlin, Deutschland)", "lat": 52.51, "lng": 13.37},
    {"n": "Tokyo Marathon (Japan)", "lat": 35.68, "lng": 139.77},
    {"n": "London Marathon (England)", "lat": 51.50, "lng": -0.12},
    {"n": "Paris Marathon (Frankreich)", "lat": 48.87, "lng": 2.30},
    {"n": "Rotterdam Marathon (Niederlande)", "lat": 51.92, "lng": 4.48},
    {"n": "Frankfurt Marathon (Deutschland)", "lat": 50.11, "lng": 8.68},
    {"n": "Hamburg Marathon (Deutschland)", "lat": 53.56, "lng": 10.00},
    {"n": "Amsterdam Marathon (Niederlande)", "lat": 52.34, "lng": 4.87},
    {"n": "Vienna City Marathon (Österreich)", "lat": 48.21, "lng": 16.37},
    {"n": "Budapest Marathon (Ungarn)", "lat": 47.50, "lng": 19.05},
    {"n": "Warsaw Marathon (Polen)", "lat": 52.23, "lng": 21.01},
    {"n": "Prague Marathon (Tschechien)", "lat": 50.08, "lng": 14.42},
    {"n": "Rome Marathon (Italien)", "lat": 41.90, "lng": 12.49},
    {"n": "Athens Classic Marathon (Griechenland)", "lat": 37.98, "lng": 23.73},
    {"n": "São Paulo Marathon (Brasilien)", "lat": -23.55, "lng": -46.63},
    {"n": "Buenos Aires Marathon (Argentinien)", "lat": -34.61, "lng": -58.43},
    {"n": "Sydney Marathon (Australien)", "lat": -33.87, "lng": 151.21},
    {"n": "Melbourne Marathon (Australien)", "lat": -37.82, "lng": 144.97},
    {"n": "Cape Town Marathon (Südafrika)", "lat": -33.91, "lng": 18.42},
    {"n": "Honolulu Marathon (Hawaii, USA)", "lat": 21.31, "lng": -157.85},
    {"n": "Toronto Waterfront Marathon (Kanada)", "lat": 43.64, "lng": -79.38},
    {"n": "Vancouver Marathon (Kanada)", "lat": 49.28, "lng": -123.12},
    {"n": "Seoul International Marathon (Südkorea)", "lat": 37.57, "lng": 126.98},
    {"n": "Mumbai Marathon (Indien)", "lat": 18.97, "lng": 72.82},
    {"n": "Comrades Marathon Start (Durban, Südafrika)", "lat": -29.88, "lng": 31.05},
    {"n": "Two Oceans Marathon (Kapstadt, Südafrika)", "lat": -34.00, "lng": 18.50},
    {"n": "Loch Ness Marathon (Schottland)", "lat": 57.35, "lng": -4.44},
    {"n": "Big Sur International Marathon (Kalifornien, USA)", "lat": 36.27, "lng": -121.81},
    {"n": "Walt Disney World Marathon (Orlando, USA)", "lat": 28.38, "lng": -81.57},
    {"n": "Antarktika Ice Marathon (King George Island)", "lat": -62.15, "lng": -58.95},
]

n_fuss = extend_key(pin, "sport_fussballstadien", fussball_new)
n_olym = extend_key(pin, "sport_olympiastadien", olympia_new)
n_moto = extend_key(pin, "sport_motorsport_strecken", motor_new)
n_wint = extend_key(pin, "sport_wintersport_orte", winter_new)
n_tenn = extend_key(pin, "sport_grand_slam_arenen", tennis_new)
n_golf = extend_key(pin, "sport_golf_platze", golf_new)
n_surf = extend_key(pin, "sport_surfspots_welt", surf_new)
n_mara = extend_key(pin, "sport_marathonstrecken", marathon_new)

jsave("sport_pin.json", pin)
print(f"  [OK] pin/fussballstadien: +{n_fuss}")
print(f"  [OK] pin/olympiastadien: +{n_olym}")
print(f"  [OK] pin/motorsport_strecken: +{n_moto}")
print(f"  [OK] pin/wintersport_orte: +{n_wint}")
print(f"  [OK] pin/grand_slam_arenen: +{n_tenn}")
print(f"  [OK] pin/golf_platze: +{n_golf}")
print(f"  [OK] pin/surfspots_welt: +{n_surf}")
print(f"  [OK] pin/marathonstrecken: +{n_mara}")

# ============================================================
# sport_hl.json
# ============================================================
hl = jload("sport_hl.json")

# --- sport_transferrekorde (Mio. €) — Ziel: 45+ ---
transfer_new = [
    {"name": "Joao Felix (Atletico → Chelsea, Leihe 2023)", "val": 11},
    {"name": "Jack Grealish (Aston Villa → ManCity, 2021)", "val": 117},
    {"name": "Harry Maguire (Leicester → Manchester Utd, 2019)", "val": 87},
    {"name": "Virgil van Dijk (Southampton → Liverpool, 2018)", "val": 85},
    {"name": "Alisson Becker (Roma → Liverpool, 2018)", "val": 67},
    {"name": "Kepa Arrizabalaga (Athletic → Chelsea, 2018)", "val": 80},
    {"name": "Eden Hazard (Chelsea → Real Madrid, 2019)", "val": 115},
    {"name": "Romelu Lukaku (Inter → Chelsea, 2021)", "val": 113},
    {"name": "Matthijs de Ligt (Juventus → Bayern, 2022)", "val": 77},
    {"name": "Jadon Sancho (Dortmund → Manchester Utd, 2021)", "val": 85},
    {"name": "Enzo Fernandez (Benfica → Chelsea, 2023)", "val": 121},
    {"name": "Declan Rice (West Ham → Arsenal, 2023)", "val": 116},
    {"name": "Moises Caicedo (Brighton → Chelsea, 2023)", "val": 116},
    {"name": "Vinicius Jr. (Real — Vertragsverlängerung 2024)", "val": 180},
    {"name": "Ruben Neves (Wolves → Al-Hilal, 2023)", "val": 55},
    {"name": "Karim Benzema (Real Madrid → Al-Ittihad, 2023)", "val": 30},
    {"name": "Roberto Firmino (Liverpool → Freier Wechsel, 2023)", "val": 0},
    {"name": "Erling Haaland (Dortmund → Manchester City, 2022)", "val": 60},
    {"name": "Aurelien Tchouameni (Monaco → Real Madrid, 2022)", "val": 100},
    {"name": "Ferran Torres (Valencia → Manchester City, 2021)", "val": 23},
    {"name": "Ferran Torres (ManCity → Barcelona, 2022)", "val": 55},
    {"name": "Pedri (verlängert bei Barça, 2023)", "val": 0},
    {"name": "Gavi (verlängert bei Barça, 2022)", "val": 0},
    {"name": "Jude Bellingham (Dortmund → Real Madrid, 2023)", "val": 103},
    {"name": "Gonzalo Higuain (Napoli → Juventus, 2016)", "val": 90},
    {"name": "Paul Pogba (Juventus → Manchester Utd, 2016)", "val": 105},
    {"name": "Gareth Bale (Tottenham → Real Madrid, 2013)", "val": 101},
    {"name": "Cristiano Ronaldo (Real → Juventus, 2018)", "val": 117},
    {"name": "Zlatan Ibrahimovic (Inter → Barcelona, 2009)", "val": 69},
    {"name": "Romelu Lukaku (Manchester Utd → Inter, 2019)", "val": 74},
    {"name": "Nicolas Pepe (Lille → Arsenal, 2019)", "val": 80},
    {"name": "Joao Cancelo (Juventus → ManCity, 2019)", "val": 65},
    {"name": "Riyad Mahrez (Leicester → ManCity, 2018)", "val": 67},
    {"name": "Benjamin Mendy (Monaco → ManCity, 2017)", "val": 57},
    {"name": "Bernardo Silva (Monaco → ManCity, 2017)", "val": 50},
    {"name": "Kaka (AC Milan → Real Madrid, 2009)", "val": 67},
    {"name": "Zinedine Zidane (Juventus → Real Madrid, 2001)", "val": 77},
    {"name": "Hernan Crespo (Lazio → Parma, 2000)", "val": 56},
    {"name": "Gianluigi Buffon (Parma → Juventus, 2001)", "val": 53},
    {"name": "Ronaldo (Fenomeno, Barcelona → Inter, 1997)", "val": 27},
    {"name": "Kylian Mbappe (PSG → Real Madrid, 2024, ablösefrei)", "val": 0},
]

# --- sport_stadien_kapazitaet (Tausend Zuschauer) --- Ziel: 45+ ---
stadion_kap_new = [
    {"name": "Salt Lake Stadium (Kolkata, Indien)", "val": 85},
    {"name": "FNB Stadium / Soccer City (Johannesburg, Südafrika)", "val": 94},
    {"name": "Wembley Stadium (London, England)", "val": 90},
    {"name": "Camp Nou (FC Barcelona, Spanien)", "val": 99},
    {"name": "Rose Bowl (Pasadena, USA)", "val": 92},
    {"name": "Estadio Monumental (Buenos Aires, Argentinien)", "val": 84},
    {"name": "Maracanã (Rio de Janeiro, Brasilien)", "val": 78},
    {"name": "Melbourne Cricket Ground (Australien)", "val": 100},
    {"name": "Cricket Ground Ahmedabad (Indien)", "val": 132},
    {"name": "Eden Gardens (Kolkata, Indien)", "val": 68},
    {"name": "National Stadium Peking (China)", "val": 91},
    {"name": "Ohio Stadium (Columbus, USA)", "val": 104},
    {"name": "Kyle Field (Texas A&M, USA)", "val": 102},
    {"name": "Neyland Stadium (Tennessee, USA)", "val": 102},
    {"name": "Tiger Stadium (Louisiana, USA)", "val": 102},
    {"name": "Bryant-Denny Stadium (Alabama, USA)", "val": 101},
    {"name": "Darrell K Royal Stadium (Texas, USA)", "val": 100},
    {"name": "Cotton Bowl (Dallas, USA)", "val": 92},
    {"name": "Luzhniki Stadion (Moskau, Russland)", "val": 81},
    {"name": "Celtic Park (Glasgow, Schottland)", "val": 60},
    {"name": "Croke Park (Dublin, Irland)", "val": 82},
    {"name": "Aztekenstadion (Mexiko-Stadt)", "val": 87},
    {"name": "Stade de France (Saint-Denis)", "val": 80},
    {"name": "Allianz Arena (München, Deutschland)", "val": 75},
    {"name": "Signal Iduna Park (Dortmund, Deutschland)", "val": 81},
    {"name": "Olympiastadion Berlin (Deutschland)", "val": 74},
    {"name": "San Siro (Mailand, Italien)", "val": 80},
    {"name": "Santiago Bernabéu (Madrid, Spanien)", "val": 81},
    {"name": "MetLife Stadium (New Jersey, USA)", "val": 82},
    {"name": "AT&T Stadium (Dallas, USA)", "val": 80},
    {"name": "Allegiant Stadium (Las Vegas, USA)", "val": 65},
    {"name": "SoFi Stadium (Los Angeles, USA)", "val": 70},
    {"name": "Levi's Stadium (Santa Clara, USA)", "val": 68},
    {"name": "Lambeau Field (Green Bay, USA)", "val": 81},
    {"name": "Arrowhead Stadium (Kansas City, USA)", "val": 77},
    {"name": "Heinz Field / Acrisure Stadium (Pittsburgh, USA)", "val": 68},
    {"name": "Optus Stadium (Perth, Australien)", "val": 60},
    {"name": "Accor Stadium (Sydney, Australien)", "val": 83},
    {"name": "Cairo International Stadium (Ägypten)", "val": 74},
    {"name": "Azadi Stadium (Teheran, Iran)", "val": 78},
    {"name": "Lusail Iconic Stadium (Katar)", "val": 88},
]

# --- sport_sportler_gehalt (Mio. $ pro Jahr) --- Ziel: 45+ ---
gehalt_new = [
    {"name": "Lionel Messi (Inter Miami, 2023)", "val": 135},
    {"name": "Cristiano Ronaldo (Al Nassr, 2023)", "val": 200},
    {"name": "Karim Benzema (Al Ittihad, 2023)", "val": 200},
    {"name": "Neymar Jr. (Al Hilal, 2023)", "val": 160},
    {"name": "Kylian Mbappe (PSG, 2022)", "val": 110},
    {"name": "LeBron James (NBA Lakers, 2023)", "val": 119},
    {"name": "Stephen Curry (Golden State Warriors, 2023)", "val": 51},
    {"name": "Kevin Durant (Phoenix Suns, 2023)", "val": 47},
    {"name": "Giannis Antetokounmpo (Milwaukee Bucks, 2023)", "val": 46},
    {"name": "Ja Morant (Memphis Grizzlies, 2023)", "val": 33},
    {"name": "Lewis Hamilton (F1 Mercedes, 2021)", "val": 62},
    {"name": "Max Verstappen (F1 Red Bull, 2023)", "val": 55},
    {"name": "Fernando Alonso (F1 Aston Martin, 2023)", "val": 20},
    {"name": "Tiger Woods (Golf, Lebenszeit)", "val": 60},
    {"name": "Rory McIlroy (Golf, 2023)", "val": 50},
    {"name": "Jon Rahm (Golf LIV, 2023)", "val": 560},
    {"name": "Dustin Johnson (LIV Golf, 2022)", "val": 125},
    {"name": "Phil Mickelson (LIV Golf, 2022)", "val": 200},
    {"name": "Novak Djokovic (Tennis, 2023)", "val": 34},
    {"name": "Rafael Nadal (Tennis, 2022)", "val": 14},
    {"name": "Roger Federer (Tennis, 2022)", "val": 90},
    {"name": "Naomi Osaka (Tennis, 2021)", "val": 57},
    {"name": "Serena Williams (Tennis, 2022 gest.)", "val": 41},
    {"name": "Conor McGregor (UFC Boxing, 2021)", "val": 180},
    {"name": "Tyson Fury (Boxing, 2021)", "val": 34},
    {"name": "Anthony Joshua (Boxing, 2021)", "val": 45},
    {"name": "Canelo Alvarez (Boxing, 2022)", "val": 90},
    {"name": "Floyd Mayweather (Boxing, allzeit)", "val": 285},
    {"name": "Patrick Mahomes (NFL Chiefs, 2020)", "val": 45},
    {"name": "Josh Allen (NFL Bills, 2021)", "val": 43},
    {"name": "Aaron Rodgers (NFL Packers, 2022)", "val": 50},
    {"name": "Lamar Jackson (NFL Ravens, 2023)", "val": 52},
    {"name": "Dak Prescott (NFL Cowboys, 2021)", "val": 40},
    {"name": "Mike Trout (MLB Angels, 2021)", "val": 38},
    {"name": "Mookie Betts (MLB Dodgers, 2020)", "val": 30},
    {"name": "Shohei Ohtani (MLB Dodgers, 2024)", "val": 70},
    {"name": "Max Scherzer (MLB Mets, 2022)", "val": 43},
    {"name": "Gerrit Cole (MLB Yankees, 2020)", "val": 36},
    {"name": "Simone Biles (Turnen, 2024)", "val": 10},
    {"name": "Katie Ledecky (Schwimmen, 2023)", "val": 3},
]

# --- sport_stadion_baujahr (Jahr) --- Ziel: 40+ ---
baujahr_new = [
    {"name": "Fenway Park (Boston Red Sox, USA)", "val": 1912},
    {"name": "Wrigley Field (Chicago Cubs, USA)", "val": 1914},
    {"name": "Yankee Stadium (New York, 2009)", "val": 2009},
    {"name": "Dodger Stadium (Los Angeles, USA)", "val": 1962},
    {"name": "Lambeau Field (Green Bay, USA)", "val": 1957},
    {"name": "Soldier Field (Chicago, USA)", "val": 1924},
    {"name": "Rose Bowl (Pasadena, USA)", "val": 1922},
    {"name": "Michigan Stadium (Ann Arbor, USA)", "val": 1927},
    {"name": "Aztekenstadion (Mexiko-Stadt)", "val": 1966},
    {"name": "Maracanã (Rio de Janeiro, Brasilien)", "val": 1950},
    {"name": "Old Trafford (Manchester, England)", "val": 1910},
    {"name": "Anfield (Liverpool, England)", "val": 1884},
    {"name": "Stamford Bridge (London, England)", "val": 1877},
    {"name": "Villa Park (Birmingham, England)", "val": 1897},
    {"name": "Ibrox Stadium (Glasgow, Schottland)", "val": 1899},
    {"name": "Hampden Park (Glasgow, Schottland)", "val": 1903},
    {"name": "Camp Nou (Barcelona, Spanien)", "val": 1957},
    {"name": "Santiago Bernabéu (Madrid, Spanien)", "val": 1947},
    {"name": "San Siro (Mailand, Italien)", "val": 1926},
    {"name": "Olimpico di Torino (Italien)", "val": 1933},
    {"name": "Panathinaiko Stadion (Athen, Griechenland)", "val": 329},
    {"name": "Olympic Stadium München (Deutschland)", "val": 1972},
    {"name": "Luzhniki Stadion (Moskau, Russland)", "val": 1956},
    {"name": "Melbourne Cricket Ground (Australien)", "val": 1853},
    {"name": "Eden Gardens (Kolkata, Indien)", "val": 1864},
    {"name": "Lord's Cricket Ground (London)", "val": 1814},
    {"name": "Oval Cricket Ground (London)", "val": 1845},
    {"name": "The Gabba (Brisbane, Australien)", "val": 1895},
    {"name": "SCG Sydney Cricket Ground (Australien)", "val": 1848},
    {"name": "Twickenham Stadium (London)", "val": 1909},
    {"name": "Millennium / Principality Stadium (Cardiff)", "val": 1999},
    {"name": "Murrayfield Stadium (Edinburgh)", "val": 1925},
    {"name": "Aviva Stadium (Dublin, Irland)", "val": 2010},
    {"name": "Stade de France (Saint-Denis, Frankreich)", "val": 1998},
    {"name": "Wembley Stadium (London, neu)", "val": 2007},
    {"name": "Allianz Arena (München, Deutschland)", "val": 2005},
    {"name": "Emirates Stadium (London)", "val": 2006},
    {"name": "Tottenham Hotspur Stadium (London)", "val": 2019},
    {"name": "AT&T Stadium (Dallas, USA)", "val": 2009},
    {"name": "MetLife Stadium (New Jersey, USA)", "val": 2010},
    {"name": "Lusail Iconic Stadium (Katar)", "val": 2021},
]

# --- sport_marathon_alter (Gründungsjahr) --- Ziel: 40+ ---
marathon_alter_new = [
    {"name": "Athens Classic Marathon (Griechenland)", "val": 1896},
    {"name": "Boston Marathon (USA)", "val": 1897},
    {"name": "Polytechnic Marathon (England)", "val": 1909},
    {"name": "Antwerp Olympic Marathon (Belgien)", "val": 1920},
    {"name": "Kosice Peace Marathon (Slowakei)", "val": 1924},
    {"name": "Fukuoka Marathon (Japan)", "val": 1947},
    {"name": "Enschede Marathon (Niederlande)", "val": 1948},
    {"name": "Comrades Marathon (Südafrika)", "val": 1921},
    {"name": "Karl-Marx-Stadt / Chemnitz Marathon (Deutschland)", "val": 1959},
    {"name": "New York City Marathon (USA)", "val": 1970},
    {"name": "Berlin Marathon (Deutschland)", "val": 1974},
    {"name": "London Marathon (England)", "val": 1981},
    {"name": "Chicago Marathon (USA)", "val": 1977},
    {"name": "Stockholm Marathon (Schweden)", "val": 1979},
    {"name": "Paris Marathon (Frankreich)", "val": 1976},
    {"name": "Vienna City Marathon (Österreich)", "val": 1984},
    {"name": "Rotterdam Marathon (Niederlande)", "val": 1981},
    {"name": "Amsterdam Marathon (Niederlande)", "val": 1975},
    {"name": "Seoul International Marathon (Südkorea)", "val": 1931},
    {"name": "Honolulu Marathon (USA)", "val": 1973},
    {"name": "Tokyo Marathon (Japan)", "val": 2007},
    {"name": "Toronto Waterfront Marathon (Kanada)", "val": 1971},
    {"name": "Singapore Marathon (Singapur)", "val": 1982},
    {"name": "Dubai Marathon (VAE)", "val": 2000},
    {"name": "Two Oceans Marathon (Südafrika)", "val": 1970},
    {"name": "São Paulo Marathon (Brasilien)", "val": 1979},
    {"name": "Buenos Aires Marathon (Argentinien)", "val": 1994},
    {"name": "Madrid Marathon (Spanien)", "val": 1978},
    {"name": "Brussels Marathon (Belgien)", "val": 1981},
    {"name": "Prague Marathon (Tschechien)", "val": 1995},
    {"name": "Warsaw Marathon (Polen)", "val": 1981},
    {"name": "Budapest Marathon (Ungarn)", "val": 1984},
    {"name": "Frankfurt Marathon (Deutschland)", "val": 1981},
    {"name": "Hamburg Marathon (Deutschland)", "val": 1986},
    {"name": "Rome Marathon (Italien)", "val": 1987},
    {"name": "Great Wall Marathon (China)", "val": 1999},
]

n_hl_transfer = extend_key(hl, "sport_transferrekorde", transfer_new, name_field="name")
n_hl_kap = extend_key(hl, "sport_stadien_kapazitaet", stadion_kap_new, name_field="name")
n_hl_geh = extend_key(hl, "sport_sportler_gehalt", gehalt_new, name_field="name")
n_hl_bau = extend_key(hl, "sport_stadion_baujahr", baujahr_new, name_field="name")
n_hl_mara = extend_key(hl, "sport_marathon_alter", marathon_alter_new, name_field="name")

jsave("sport_hl.json", hl)
print(f"  [OK] hl/transferrekorde: +{n_hl_transfer}")
print(f"  [OK] hl/stadien_kapazitaet: +{n_hl_kap}")
print(f"  [OK] hl/sportler_gehalt: +{n_hl_geh}")
print(f"  [OK] hl/stadion_baujahr: +{n_hl_bau}")
print(f"  [OK] hl/marathon_alter: +{n_hl_mara}")

# ============================================================
# sport_match.json
# ============================================================
match = jload("sport_match.json")

# --- sport_herkunft (Ursprungsland der Sportart) --- Ziel: 55+ ---
herkunft_new = [
    {"n": "Judo", "c": "Japan"},
    {"n": "Karate", "c": "Japan (Okinawa)"},
    {"n": "Kendo", "c": "Japan"},
    {"n": "Aikido", "c": "Japan"},
    {"n": "Kung Fu / Wushu", "c": "China"},
    {"n": "Tai Chi", "c": "China"},
    {"n": "Sepak Takraw", "c": "Südostasien (Malaysia/Thailand)"},
    {"n": "Kabaddi", "c": "Indien"},
    {"n": "Polo", "c": "Persien / Indien"},
    {"n": "Squash", "c": "England"},
    {"n": "Snooker", "c": "Indien (Brit. Armee)"},
    {"n": "Darts", "c": "England"},
    {"n": "Bowls / Bocce", "c": "Italien"},
    {"n": "Pétanque", "c": "Frankreich"},
    {"n": "Jai Alai / Pelota", "c": "Baskenland (Spanien)"},
    {"n": "Handball", "c": "Deutschland / Skandinavien"},
    {"n": "Field Hockey", "c": "England / Indien"},
    {"n": "Lacrosse", "c": "Nordamerika (Ureinwohner)"},
    {"n": "Curling", "c": "Schottland"},
    {"n": "Bobsled", "c": "Schweiz (St. Moritz)"},
    {"n": "Skeleton", "c": "Schweiz"},
    {"n": "Luge / Rennrodeln", "c": "Deutschland"},
    {"n": "Biathlon", "c": "Skandinavien (Norwegen)"},
    {"n": "Ski Jumping", "c": "Norwegen"},
    {"n": "Slalom / Alpine Ski", "c": "Österreich / Norwegen"},
    {"n": "Cross-Country Skiing", "c": "Norwegen / Skandinavien"},
    {"n": "Snowboarding", "c": "USA (Surfskate-Bewegung)"},
    {"n": "Beach Volleyball", "c": "USA (Santa Monica)"},
    {"n": "Water Polo", "c": "England"},
    {"n": "Synchronized Swimming", "c": "USA / Kanada"},
    {"n": "Fencing", "c": "Europa (Deutschland / Frankreich)"},
    {"n": "Modern Pentathlon", "c": "Frankreich (Pierre de Coubertin)"},
    {"n": "Triathlon", "c": "USA (San Diego)"},
    {"n": "Badminton", "c": "England (Badminton House)"},
    {"n": "Table Tennis / Ping Pong", "c": "England"},
    {"n": "Volleyball", "c": "USA (William Morgan)"},
    {"n": "Baseball", "c": "USA"},
    {"n": "American Football", "c": "USA"},
    {"n": "Ice Hockey", "c": "Kanada"},
    {"n": "Lacrosse (Box)", "c": "Kanada"},
    {"n": "Aussie Rules Football", "c": "Australien"},
    {"n": "Rugby League", "c": "England (Yorkshire)"},
    {"n": "Rugby Union", "c": "England (Rugby School)"},
    {"n": "Boxing", "c": "England (Marquess of Queensberry)"},
    {"n": "Wrestling / Freistil", "c": "USA"},
    {"n": "Greco-Roman Wrestling", "c": "Europa (Frankreich)"},
    {"n": "Athletics / Leichtathletik", "c": "Griechenland (antik)"},
    {"n": "Cycling Road", "c": "Frankreich"},
    {"n": "Gymnastics / Turnen", "c": "Deutschland (Friedrich Ludwig Jahn)"},
]

# --- sport_weltverband --- Ziel: 50+ ---
weltverband_new = [
    {"n": "Fußball", "c": "FIFA"},
    {"n": "Basketball", "c": "FIBA"},
    {"n": "Leichtathletik", "c": "World Athletics"},
    {"n": "Schwimmen", "c": "World Aquatics (FINA)"},
    {"n": "Tennis", "c": "ITF"},
    {"n": "Volleyball", "c": "FIVB"},
    {"n": "Handball", "c": "IHF"},
    {"n": "Rugby", "c": "World Rugby"},
    {"n": "Cricket", "c": "ICC"},
    {"n": "Golf", "c": "IGF"},
    {"n": "Hockey (Feld)", "c": "FIH"},
    {"n": "Boxen (olympisch)", "c": "IBA"},
    {"n": "Gewichtheben", "c": "IWF"},
    {"n": "Judo", "c": "IJF"},
    {"n": "Taekwondo", "c": "World Taekwondo"},
    {"n": "Karate", "c": "WKF"},
    {"n": "Fechten", "c": "FIE"},
    {"n": "Reiten", "c": "FEI"},
    {"n": "Segeln", "c": "World Sailing"},
    {"n": "Rudern", "c": "World Rowing"},
    {"n": "Kanu", "c": "ICF"},
    {"n": "Schießen", "c": "ISSF"},
    {"n": "Bogenschießen", "c": "World Archery"},
    {"n": "Radsport", "c": "UCI"},
    {"n": "Turnen", "c": "FIG"},
    {"n": "Curling", "c": "WCF"},
    {"n": "Eishockey", "c": "IIHF"},
    {"n": "Ski Alpin / Nordisch", "c": "FIS"},
    {"n": "Biathlon", "c": "IBU"},
    {"n": "Bobsport", "c": "IBSF"},
    {"n": "Eisschnelllauf", "c": "ISU"},
    {"n": "Shorttrack", "c": "ISU"},
    {"n": "Eiskunstlauf", "c": "ISU"},
    {"n": "Badminton", "c": "BWF"},
    {"n": "Tischtennis", "c": "ITTF"},
    {"n": "American Football", "c": "IFAF"},
    {"n": "Baseball / Softball", "c": "World Baseball Softball"},
    {"n": "Triathlon", "c": "World Triathlon"},
    {"n": "Moderner Fünfkampf", "c": "UIPM"},
    {"n": "Ringen", "c": "UWW"},
    {"n": "Snooker", "c": "WPBSA"},
    {"n": "Darts", "c": "BDO / PDC"},
    {"n": "Squash", "c": "WSF"},
    {"n": "Polo", "c": "FIP"},
    {"n": "Motorrad-Sport", "c": "FIM"},
    {"n": "Automobilsport", "c": "FIA"},
    {"n": "Wasserspringen", "c": "World Aquatics"},
    {"n": "Freiwasser-Schwimmen", "c": "World Aquatics"},
]

# --- sport_sportlegende_land --- Ziel: 55+ ---
legende_new = [
    {"n": "Roger Federer (Tennis)", "c": "Schweiz"},
    {"n": "Novak Djokovic (Tennis)", "c": "Serbien"},
    {"n": "Rafael Nadal (Tennis)", "c": "Spanien"},
    {"n": "Serena Williams (Tennis)", "c": "USA"},
    {"n": "Steffi Graf (Tennis)", "c": "Deutschland"},
    {"n": "Boris Becker (Tennis)", "c": "Deutschland"},
    {"n": "Max Verstappen (Formel 1)", "c": "Niederlande"},
    {"n": "Lewis Hamilton (Formel 1)", "c": "England"},
    {"n": "Michael Schumacher (Formel 1)", "c": "Deutschland"},
    {"n": "Ayrton Senna (Formel 1)", "c": "Brasilien"},
    {"n": "Usain Bolt (Leichtathletik)", "c": "Jamaika"},
    {"n": "Florence Griffith-Joyner (Leichtathletik)", "c": "USA"},
    {"n": "Michael Phelps (Schwimmen)", "c": "USA"},
    {"n": "Mark Spitz (Schwimmen)", "c": "USA"},
    {"n": "Katinka Hosszu (Schwimmen)", "c": "Ungarn"},
    {"n": "Nadia Comaneci (Turnen)", "c": "Rumänien"},
    {"n": "Simone Biles (Turnen)", "c": "USA"},
    {"n": "Larisa Latynina (Turnen)", "c": "UdSSR / Russland"},
    {"n": "Shaquille O'Neal (Basketball)", "c": "USA"},
    {"n": "Kobe Bryant (Basketball)", "c": "USA"},
    {"n": "Giannis Antetokounmpo (Basketball)", "c": "Griechenland"},
    {"n": "Dirk Nowitzki (Basketball)", "c": "Deutschland"},
    {"n": "Ronaldinho (Fußball)", "c": "Brasilien"},
    {"n": "Ronaldo (Fenomeno, Fußball)", "c": "Brasilien"},
    {"n": "Zinedine Zidane (Fußball)", "c": "Frankreich"},
    {"n": "Johan Cruyff (Fußball)", "c": "Niederlande"},
    {"n": "Franz Beckenbauer (Fußball)", "c": "Deutschland"},
    {"n": "Gerd Müller (Fußball)", "c": "Deutschland"},
    {"n": "George Best (Fußball)", "c": "Nordirland"},
    {"n": "Bobby Charlton (Fußball)", "c": "England"},
    {"n": "Diego Maradona (Fußball)", "c": "Argentinien"},
    {"n": "Thierry Henry (Fußball)", "c": "Frankreich"},
    {"n": "Ronaldo Cristiano (Fußball)", "c": "Portugal"},
    {"n": "Tiger Woods (Golf)", "c": "USA"},
    {"n": "Jack Nicklaus (Golf)", "c": "USA"},
    {"n": "Gary Player (Golf)", "c": "Südafrika"},
    {"n": "Lance Armstrong (Radsport)", "c": "USA"},
    {"n": "Eddy Merckx (Radsport)", "c": "Belgien"},
    {"n": "Bernard Hinault (Radsport)", "c": "Frankreich"},
    {"n": "Bjorn Daehlie (Skilanglauf)", "c": "Norwegen"},
    {"n": "Ingemar Stenmark (Ski Alpin)", "c": "Schweden"},
    {"n": "Hermann Maier (Ski Alpin)", "c": "Österreich"},
    {"n": "Marcel Hirscher (Ski Alpin)", "c": "Österreich"},
    {"n": "Valentina Vezzali (Fechten)", "c": "Italien"},
    {"n": "Haile Gebrselassie (Marathonlauf)", "c": "Äthiopien"},
    {"n": "Eliud Kipchoge (Marathonlauf)", "c": "Kenia"},
    {"n": "Wayde van Niekerk (Leichtathletik)", "c": "Südafrika"},
]

# --- sport_wm_gastgeber_match --- Ziel: 50+ ---
wm_gastgeber_new = [
    {"n": "WM 1930", "c": "Uruguay"},
    {"n": "WM 1934", "c": "Italien"},
    {"n": "WM 1938", "c": "Frankreich"},
    {"n": "WM 1950", "c": "Brasilien"},
    {"n": "WM 1954", "c": "Schweiz"},
    {"n": "WM 1958", "c": "Schweden"},
    {"n": "WM 1962", "c": "Chile"},
    {"n": "WM 1966", "c": "England"},
    {"n": "WM 1970", "c": "Mexiko"},
    {"n": "WM 1974", "c": "Westdeutschland"},
    {"n": "WM 1978", "c": "Argentinien"},
    {"n": "WM 1982", "c": "Spanien"},
    {"n": "WM 1986", "c": "Mexiko"},
    {"n": "WM 1990", "c": "Italien"},
    {"n": "WM 1994", "c": "USA"},
    {"n": "WM 1998", "c": "Frankreich"},
    {"n": "WM 2002", "c": "Südkorea / Japan"},
    {"n": "WM 2006", "c": "Deutschland"},
    {"n": "WM 2010", "c": "Südafrika"},
    {"n": "WM 2014", "c": "Brasilien"},
    {"n": "WM 2018", "c": "Russland"},
    {"n": "WM 2022", "c": "Katar"},
    {"n": "WM 2026", "c": "USA / Kanada / Mexiko"},
    {"n": "WM 2030", "c": "Spanien / Portugal / Marokko"},
    {"n": "Rugby WM 2019", "c": "Japan"},
    {"n": "Rugby WM 2023", "c": "Frankreich"},
    {"n": "Rugby WM 2027", "c": "Australien"},
    {"n": "Cricket WM 2023", "c": "Indien"},
    {"n": "Cricket WM 2024 T20", "c": "USA / Westindien"},
    {"n": "Basketball WM 2023", "c": "Philippinen / Japan / Indonesien"},
    {"n": "Handball WM 2021", "c": "Ägypten"},
    {"n": "Handball WM 2023", "c": "Polen / Schweden"},
    {"n": "Hockey WM 2023", "c": "Indien"},
    {"n": "Volleyball WM 2022", "c": "Polen / Slowenien"},
    {"n": "Schwimm-WM 2023", "c": "Japan (Fukuoka)"},
    {"n": "Leichtathletik-WM 2022", "c": "USA (Eugene)"},
    {"n": "Leichtathletik-WM 2023", "c": "Ungarn (Budapest)"},
    {"n": "Formel-1 Konstrukteurs-WM 2023", "c": "Red Bull Racing (Österreich)"},
    {"n": "Tour de France 2023 Sieger", "c": "Dänemark (Jonas Vingegaard)"},
    {"n": "Wimbledon 2023 Sieger", "c": "Spanien (Alcaraz)"},
    {"n": "Olympia Sommer 2020/21", "c": "Japan (Tokio)"},
    {"n": "Olympia Sommer 2024", "c": "Frankreich (Paris)"},
    {"n": "Olympia Sommer 2028", "c": "USA (Los Angeles)"},
    {"n": "Olympia Winter 2022", "c": "China (Peking)"},
    {"n": "Olympia Winter 2026", "c": "Italien (Mailand / Cortina)"},
]

n_m_herk = extend_key(match, "sport_herkunft", herkunft_new)
n_m_verb = extend_key(match, "sport_weltverband", weltverband_new)
n_m_leg = extend_key(match, "sport_sportlegende_land", legende_new)
n_m_wm = extend_key(match, "sport_wm_gastgeber_match", wm_gastgeber_new)

jsave("sport_match.json", match)
print(f"  [OK] match/herkunft: +{n_m_herk}")
print(f"  [OK] match/weltverband: +{n_m_verb}")
print(f"  [OK] match/sportlegende_land: +{n_m_leg}")
print(f"  [OK] match/wm_gastgeber: +{n_m_wm}")

# ============================================================
# FINALE ITEMZAHLEN
# ============================================================
print("\n=== FINALE ITEMZAHLEN ===")
print("\nsport_pin.json")
pin2 = jload("sport_pin.json")
for k, v in pin2.items():
    items = v.get("items", v) if isinstance(v, dict) else v
    print(f"  {k}: {len(items)}")

print("\nsport_hl.json")
hl2 = jload("sport_hl.json")
for k, v in hl2.items():
    items = v.get("items", v) if isinstance(v, dict) else v
    print(f"  {k}: {len(items)}")

print("\nsport_match.json")
m2 = jload("sport_match.json")
for k, v in m2.items():
    items = v.get("items", v) if isinstance(v, dict) else v
    print(f"  {k}: {len(items)}")
