"""
Phase: 254
Date:  2026-05-27
Author: Claude / Andre
Scope: Sport-Wissen Expansion: 30 neue Modi (8 Pin, 8 HL, 8 Match, 6 WS).

Description:
  Erweitert die vier data/sport_*.json Dateien und registriert 30 neue Modi
  in der sport_wissen-Kategorie.

  sport_pin.json   (+8): fussballstadien, motorsport_strecken,
    wintersport_orte, grand_slam_arenen, ski_pisten, golf_platze,
    surfspots_welt, klettergebiete
  sport_hl.json    (+8): transferrekorde, hochsprung_rekorde,
    sportler_gehalt, olympia_goldmedaillen, fussball_marktwert,
    gewichtheben_rekorde, stadion_baujahr, tore_saison
  sport_match.json (+8): weltverband, olympisch, nationalsport_match,
    sportlegende_land, rekordhalter, wm_gastgeber_match,
    disziplin_kategorie, sportart_kontinent
  sport_ws.json    (+6): fussball, olympiade, weltmeister,
    startschuss, athletik, sportgeist

Dependencies: patch_243_new_worlds.py
Zero-Bug Policy: All c.replace() calls use assert c.count(old)==1
"""

import json, pathlib, sys
from collections import Counter

ROOT = pathlib.Path(__file__).parent.parent
DATA = ROOT / "data"
GEN  = ROOT / "gen.py"

# ==============================================================================
# 1. JSON DATA
# ==============================================================================

NEW_PIN = {
  "sport_fussballstadien": {
    "prompt": "Wo liegt dieses Fussballstadion?",
    "items": [
      {"n": "Camp Nou (FC Barcelona, Spanien)", "lat": 41.38, "lng": 2.12},
      {"n": "Wembley Stadium (London, England)", "lat": 51.56, "lng": -0.28},
      {"n": "Allianz Arena (Muenchen, Deutschland)", "lat": 48.22, "lng": 11.62},
      {"n": "Santiago Bernabeu (Real Madrid, Spanien)", "lat": 40.45, "lng": -3.69},
      {"n": "Estadio Azteca (Mexiko-Stadt)", "lat": 19.30, "lng": -99.15},
      {"n": "San Siro / Giuseppe Meazza (Mailand, Italien)", "lat": 45.48, "lng": 9.12},
      {"n": "Maracana (Rio de Janeiro, Brasilien)", "lat": -22.91, "lng": -43.23},
      {"n": "Old Trafford (Manchester United, England)", "lat": 53.46, "lng": -2.29}
    ]
  },
  "sport_motorsport_strecken": {
    "prompt": "Wo liegt diese Motorsport-Rennstrecke?",
    "items": [
      {"n": "Circuit de Monaco (Monte Carlo)", "lat": 43.73, "lng": 7.42},
      {"n": "Autodromo Nazionale Monza (Italien)", "lat": 45.62, "lng": 9.29},
      {"n": "Silverstone Circuit (England)", "lat": 52.07, "lng": -1.02},
      {"n": "Suzuka Circuit (Japan)", "lat": 34.84, "lng": 136.54},
      {"n": "Circuit of the Americas (Austin, USA)", "lat": 30.13, "lng": -97.64},
      {"n": "Nurburgring Nordschleife (Deutschland)", "lat": 50.33, "lng": 6.94},
      {"n": "Spa-Francorchamps (Belgien)", "lat": 50.44, "lng": 5.97},
      {"n": "Autodromo Jose Carlos Pace Interlagos (Brasilien)", "lat": -23.70, "lng": -46.70}
    ]
  },
  "sport_wintersport_orte": {
    "prompt": "Wo liegt dieser Wintersport-Ort?",
    "items": [
      {"n": "Kitzbuehel (Oesterreich) — Hahnenkamm-Rennen", "lat": 47.45, "lng": 12.39},
      {"n": "St. Moritz (Schweiz) — Olympia 1924 & 1948", "lat": 46.50, "lng": 9.84},
      {"n": "Whistler Blackcomb (Kanada) — Olympia 2010", "lat": 50.12, "lng": -122.95},
      {"n": "Wengen (Schweiz) — Lauberhorn-Rennen", "lat": 46.61, "lng": 7.92},
      {"n": "Lake Placid (USA) — Olympia 1932 & 1980", "lat": 44.28, "lng": -73.99},
      {"n": "Val d'Isere (Frankreich) — WM-Ort 2023", "lat": 45.45, "lng": 6.98},
      {"n": "Innsbruck (Oesterreich) — Olympia 1964 & 1976", "lat": 47.27, "lng": 11.39},
      {"n": "Are (Schweden) — Skiort WM 2019", "lat": 63.40, "lng": 13.08}
    ]
  },
  "sport_grand_slam_arenen": {
    "prompt": "Wo liegt diese Grand-Slam-Tennis-Arena?",
    "items": [
      {"n": "Roland Garros (Paris, Frankreich)", "lat": 48.85, "lng": 2.25},
      {"n": "Wimbledon All England Club (London)", "lat": 51.43, "lng": -0.21},
      {"n": "US Open USTA Billie Jean King (New York)", "lat": 40.75, "lng": -73.85},
      {"n": "Australian Open Melbourne Park", "lat": -37.82, "lng": 144.98},
      {"n": "ATP Finals O2 Arena (London)", "lat": 51.50, "lng": 0.00},
      {"n": "Davis Cup Arena La Caja Magica (Madrid)", "lat": 40.35, "lng": -3.68},
      {"n": "Laver Arena (Melbourne Park)", "lat": -37.82, "lng": 144.98},
      {"n": "Arthur Ashe Stadium (Flushing Meadows, NY)", "lat": 40.75, "lng": -73.85}
    ]
  },
  "sport_ski_pisten": {
    "prompt": "Wo liegt dieses beruehmt Skigebiet?",
    "items": [
      {"n": "Verbier (Schweiz) — Freeride World Tour", "lat": 46.10, "lng": 7.23},
      {"n": "Chamonix Mont-Blanc (Frankreich)", "lat": 45.92, "lng": 6.87},
      {"n": "Zermatt (Schweiz) — Matterhorn-Skigebiet", "lat": 46.02, "lng": 7.75},
      {"n": "Aspen Snowmass (Colorado, USA)", "lat": 39.19, "lng": -106.82},
      {"n": "Vail Mountain (Colorado, USA)", "lat": 39.64, "lng": -106.37},
      {"n": "Cortina d'Ampezzo (Dolomiten, Italien)", "lat": 46.54, "lng": 12.14},
      {"n": "Niseko (Hokkaido, Japan)", "lat": 42.80, "lng": 140.68},
      {"n": "Banff Sunshine Village (Alberta, Kanada)", "lat": 51.12, "lng": -115.76}
    ]
  },
  "sport_golf_platze": {
    "prompt": "Wo liegt dieser beruehmt Golfplatz?",
    "items": [
      {"n": "Augusta National Golf Club (Georgia, USA)", "lat": 33.50, "lng": -82.02},
      {"n": "St Andrews Old Course (Schottland)", "lat": 56.34, "lng": -2.80},
      {"n": "Pebble Beach Golf Links (Kalifornien, USA)", "lat": 36.57, "lng": -121.95},
      {"n": "Royal Birkdale (Southport, England)", "lat": 53.63, "lng": -3.03},
      {"n": "Pine Valley Golf Club (New Jersey, USA)", "lat": 39.80, "lng": -74.97},
      {"n": "Muirfield Golf Links (Schottland)", "lat": 56.03, "lng": -2.82},
      {"n": "Shinnecock Hills (New York, USA)", "lat": 40.87, "lng": -72.49},
      {"n": "Royal Melbourne Golf Club (Australien)", "lat": -37.94, "lng": 145.04}
    ]
  },
  "sport_surfspots_welt": {
    "prompt": "Wo liegt dieser weltberuehmt Surfspot?",
    "items": [
      {"n": "Pipeline (Oahu, Hawaii, USA)", "lat": 21.67, "lng": -158.05},
      {"n": "Teahupoo (Tahiti, Franzoesisch-Polynesien)", "lat": -17.86, "lng": -149.27},
      {"n": "Nazare (Portugal) — groesste Wellen der Welt", "lat": 39.60, "lng": -9.07},
      {"n": "Bells Beach (Victoria, Australien)", "lat": -38.37, "lng": 144.28},
      {"n": "Jeffreys Bay (Suedafrika)", "lat": -34.05, "lng": 24.93},
      {"n": "Uluwatu (Bali, Indonesien)", "lat": -8.83, "lng": 115.09},
      {"n": "Mundaka (Baskenland, Spanien)", "lat": 43.41, "lng": -2.70},
      {"n": "Mavericks (Half Moon Bay, Kalifornien)", "lat": 37.49, "lng": -122.50}
    ]
  },
  "sport_klettergebiete": {
    "prompt": "Wo liegt dieses beruehmt Klettergebiet?",
    "items": [
      {"n": "Yosemite Valley (Kalifornien, USA) — El Capitan", "lat": 37.74, "lng": -119.60},
      {"n": "Fontainebleau (Frankreich) — Bouldern", "lat": 48.41, "lng": 2.70},
      {"n": "Kalymnos (Griechenland) — Sportkletterer-Mekka", "lat": 36.95, "lng": 26.98},
      {"n": "Frankenjura (Bayern, Deutschland) — schwerste Routen", "lat": 49.75, "lng": 11.47},
      {"n": "Dolomiten (Suedtirol, Italien) — Klettersteigrouten", "lat": 46.50, "lng": 11.80},
      {"n": "Railay Beach (Thailand) — Kalkstein-Tuermen", "lat": 8.01, "lng": 98.83},
      {"n": "Red River Gorge (Kentucky, USA)", "lat": 37.78, "lng": -83.66},
      {"n": "Ceuse (Hautes-Alpes, Frankreich) — Sportklettern", "lat": 44.38, "lng": 5.97}
    ]
  }
}

NEW_HL = {
  "sport_transferrekorde": {
    "prompt": "Welcher Transfer war teurer?",
    "unit": "Mio Euro",
    "items": [
      {"name": "Neymar Jr. (Barcelona → PSG, 2017)", "val": 222},
      {"name": "Kylian Mbappe (Monaco → PSG, 2018)", "val": 180},
      {"name": "Antoine Griezmann (Atletico → Barcelona, 2019)", "val": 120},
      {"name": "Joao Felix (Benfica → Atletico, 2019)", "val": 126},
      {"name": "Cristiano Ronaldo (Real Madrid → Juve, 2018)", "val": 117},
      {"name": "Gareth Bale (Tottenham → Real Madrid, 2013)", "val": 101},
      {"name": "Ousmane Dembele (BVB → Barcelona, 2017)", "val": 105},
      {"name": "Coutinho (Liverpool → Barcelona, 2018)", "val": 135}
    ]
  },
  "sport_hochsprung_rekorde": {
    "prompt": "Wer sprang hoeher?",
    "unit": "cm",
    "items": [
      {"name": "Javier Sotomayor (WR Hochsprung)", "val": 245},
      {"name": "Stefka Kostadinova (WR Frauen-Hochsprung)", "val": 209},
      {"name": "Gianmarco Tamberi (Olympiasieger 2021)", "val": 237},
      {"name": "Mutaz Essa Barshim (WM-Sieger 2022)", "val": 237},
      {"name": "Dick Fosbury (erste Fosbury-Flop Olympia 1968)", "val": 224},
      {"name": "Valery Brumel (Weltrekord 1963)", "val": 228},
      {"name": "Charles Austin (Olympiasieger 1996)", "val": 239},
      {"name": "Ivan Ukhov (Olympiasieger 2012)", "val": 238}
    ]
  },
  "sport_sportler_gehalt": {
    "prompt": "Wer verdient mehr pro Jahr?",
    "unit": "Mio Euro/Jahr",
    "items": [
      {"name": "Cristiano Ronaldo (Al Nassr, Saudi-Arabien)", "val": 200},
      {"name": "Lionel Messi (Inter Miami, USA)", "val": 135},
      {"name": "Kylian Mbappe (Real Madrid)", "val": 90},
      {"name": "LeBron James (LA Lakers, NBA)", "val": 47},
      {"name": "Roger Federer (Werbeeinnahmen, pension)", "val": 90},
      {"name": "Tiger Woods (Golf-Earnings + Werbung)", "val": 55},
      {"name": "Novak Djokovic (Tennis-Profi)", "val": 38},
      {"name": "Max Verstappen (Red Bull Racing F1)", "val": 55}
    ]
  },
  "sport_olympia_goldmedaillen": {
    "prompt": "Wer gewann mehr Olympia-Goldmedaillen?",
    "unit": "Goldmedaillen",
    "items": [
      {"name": "Michael Phelps (Schwimmen, USA)", "val": 23},
      {"name": "Larisa Latynina (Turnen, UdSSR)", "val": 9},
      {"name": "Paavo Nurmi (Leichtathletik, Finnland)", "val": 9},
      {"name": "Mark Spitz (Schwimmen, USA)", "val": 9},
      {"name": "Carl Lewis (Leichtathletik, USA)", "val": 9},
      {"name": "Birgit Fischer (Kanu, Deutschland)", "val": 8},
      {"name": "Usain Bolt (Sprint, Jamaika)", "val": 8},
      {"name": "Simone Biles (Turnen, USA)", "val": 7}
    ]
  },
  "sport_fussball_marktwert": {
    "prompt": "Wer hat einen hoeheren Marktwert?",
    "unit": "Mio Euro",
    "items": [
      {"name": "Kylian Mbappe (Hoechstwert ca. 2022)", "val": 180},
      {"name": "Erling Haaland (Manchester City)", "val": 170},
      {"name": "Jude Bellingham (Real Madrid)", "val": 150},
      {"name": "Vinicius Jr. (Real Madrid)", "val": 150},
      {"name": "Bukayo Saka (Arsenal)", "val": 130},
      {"name": "Pedri (FC Barcelona)", "val": 110},
      {"name": "Rodri (Manchester City, Ballon d'Or 2024)", "val": 120},
      {"name": "Lamine Yamal (FC Barcelona)", "val": 120}
    ]
  },
  "sport_gewichtheben_rekorde": {
    "prompt": "Wer hob mehr? (Reissen + Stossen zusammen)",
    "unit": "kg",
    "items": [
      {"name": "Lasha Talakhadze (Georgien, >109 kg, WR)", "val": 484},
      {"name": "Tatiana Kashirina (Russland, Frauen WR)", "val": 348},
      {"name": "Andrei Aramnau (Belarus, 105 kg, OR 2008)", "val": 436},
      {"name": "Matthias Steiner (Deutschland, OR 2008)", "val": 461},
      {"name": "Zhang Guozheng (China, 69 kg WR)", "val": 347},
      {"name": "Naim Suleymanoglu (Tuerkei, 64 kg WR)", "val": 342},
      {"name": "Halil Mutlu (Tuerkei, 56 kg WR)", "val": 305},
      {"name": "Long Qingquan (China, 56 kg OR 2016)", "val": 307}
    ]
  },
  "sport_stadion_baujahr": {
    "prompt": "Welches Stadion wurde frueher erbaut?",
    "unit": "Baujahr",
    "items": [
      {"name": "Fenway Park (Boston Red Sox, Baseball)", "val": 1912},
      {"name": "Wrigley Field (Chicago Cubs, Baseball)", "val": 1914},
      {"name": "Yankee Stadium Original (New York)", "val": 1923},
      {"name": "Solitude-Rennstrecke (Stuttgart, Deutschland)", "val": 1935},
      {"name": "Maracana Original (Rio de Janeiro)", "val": 1950},
      {"name": "Azteca Stadion (Mexiko-Stadt)", "val": 1966},
      {"name": "Camp Nou (FC Barcelona)", "val": 1957},
      {"name": "Estadio Centenario (Montevideo, Uruguay)", "val": 1930}
    ]
  },
  "sport_tore_saison": {
    "prompt": "Wer erzielte mehr Tore in einer Saison?",
    "unit": "Tore",
    "items": [
      {"name": "Erling Haaland (PL-Saison 2022/23, 36 Spiele)", "val": 36},
      {"name": "Cristiano Ronaldo (La Liga 2011/12)", "val": 50},
      {"name": "Lionel Messi (La Liga 2011/12)", "val": 50},
      {"name": "Gerd Mueller (Bundesliga 1971/72)", "val": 40},
      {"name": "Robert Lewandowski (BL 2020/21, Muellerrekord)", "val": 41},
      {"name": "Luis Suarez (La Liga 2015/16)", "val": 40},
      {"name": "Hugo Sanchez (La Liga 1989/90)", "val": 38},
      {"name": "Ronaldo Nazario (La Liga 1996/97)", "val": 34}
    ]
  }
}

NEW_MATCH = {
  "sport_weltverband": {
    "prompt": "Welchem Weltverband gehoert diese Sportart an?",
    "items": [
      {"n": "Fussball", "c": "FIFA"},
      {"n": "Basketball", "c": "FIBA"},
      {"n": "Leichtathletik", "c": "World Athletics"},
      {"n": "Tennis", "c": "ITF"},
      {"n": "Schwimmen", "c": "World Aquatics"},
      {"n": "Volleyball", "c": "FIVB"},
      {"n": "Boxen (Amateure)", "c": "IBA"},
      {"n": "Radsport", "c": "UCI"},
      {"n": "Turnen", "c": "FIG"},
      {"n": "Handball", "c": "IHF"}
    ]
  },
  "sport_olympisch": {
    "prompt": "Ist diese Sportart bei den Olympischen Spielen vertreten?",
    "items": [
      {"n": "Surfen", "c": "Ja"},
      {"n": "Klettern", "c": "Ja"},
      {"n": "Skateboarden", "c": "Ja"},
      {"n": "Cricket", "c": "Nein"},
      {"n": "Schach", "c": "Nein"},
      {"n": "Softball", "c": "Ja"},
      {"n": "Squash", "c": "Nein"},
      {"n": "Breakdance", "c": "Ja"}
    ]
  },
  "sport_nationalsport_match": {
    "prompt": "Welches Land hat diesen Sport als inoffiziellen Nationalsport?",
    "items": [
      {"n": "Cricket", "c": "England"},
      {"n": "Sumo", "c": "Japan"},
      {"n": "Kabaddi", "c": "Indien"},
      {"n": "Hurling", "c": "Irland"},
      {"n": "Muay Thai", "c": "Thailand"},
      {"n": "Pelota Vasca", "c": "Baskenland"},
      {"n": "Curling", "c": "Kanada"},
      {"n": "Bandy", "c": "Russland"}
    ]
  },
  "sport_sportlegende_land": {
    "prompt": "Aus welchem Land kommt diese Sportlegende?",
    "items": [
      {"n": "Pele (Fussball)", "c": "Brasilien"},
      {"n": "Michael Jordan (Basketball)", "c": "USA"},
      {"n": "Muhammad Ali (Boxen)", "c": "USA"},
      {"n": "Senna (Formel 1)", "c": "Brasilien"},
      {"n": "Roger Federer (Tennis)", "c": "Schweiz"},
      {"n": "Nadia Comaneci (Turnen)", "c": "Rumaenien"},
      {"n": "Jesse Owens (Leichtathletik)", "c": "USA"},
      {"n": "Eddy Merckx (Radsport)", "c": "Belgien"},
      {"n": "Franz Beckenbauer (Fussball)", "c": "Deutschland"},
      {"n": "Katarina Witt (Eiskunstlauf)", "c": "Deutschland"}
    ]
  },
  "sport_rekordhalter": {
    "prompt": "Wer haelt diesen Weltrekord?",
    "items": [
      {"n": "100m-Sprint Maenner (9,58 s)", "c": "Usain Bolt"},
      {"n": "Hochsprung Maenner (2,45 m)", "c": "Javier Sotomayor"},
      {"n": "Weitsprung Maenner (8,95 m)", "c": "Mike Powell"},
      {"n": "Stabhochsprung Maenner (6,21 m)", "c": "Armand Duplantis"},
      {"n": "Marathon Maenner (2:00:35 offiz.)", "c": "Kelvin Kiptum"},
      {"n": "Schwimmen 100m Freistil (46,91 s)", "c": "Cesar Cielo"},
      {"n": "Gewichtheben gesamt (484 kg)", "c": "Lasha Talakhadze"},
      {"n": "100m-Sprint Frauen (10,49 s)", "c": "Florence Griffith-Joyner"}
    ]
  },
  "sport_wm_gastgeber_match": {
    "prompt": "In welchem Land fand diese Fussball-WM statt?",
    "items": [
      {"n": "FIFA WM 1930", "c": "Uruguay"},
      {"n": "FIFA WM 1954", "c": "Schweiz"},
      {"n": "FIFA WM 1970", "c": "Mexiko"},
      {"n": "FIFA WM 1974", "c": "Deutschland"},
      {"n": "FIFA WM 1994", "c": "USA"},
      {"n": "FIFA WM 2002", "c": "Japan und Korea"},
      {"n": "FIFA WM 2010", "c": "Suedafrika"},
      {"n": "FIFA WM 2022", "c": "Katar"}
    ]
  },
  "sport_disziplin_kategorie": {
    "prompt": "Zu welcher Sportdisziplin gehoert diese Uebung?",
    "items": [
      {"n": "Reihen (Sculling)", "c": "Rudern"},
      {"n": "Salomonsprung", "c": "Turnen"},
      {"n": "Tuck Position", "c": "Skifahren / Turnen"},
      {"n": "Kenterung (Eskimo Roll)", "c": "Kanu"},
      {"n": "Anschlag Freistil", "c": "Schwimmen"},
      {"n": "Schnitt (Skating)", "c": "Eisschnelllauf"},
      {"n": "Toe Loop", "c": "Eiskunstlauf"},
      {"n": "Salvo (Volley)", "c": "Tennis"}
    ]
  },
  "sport_sportart_kontinent": {
    "prompt": "Auf welchem Kontinent wurde diese Sportart erfunden / ist am populaersten?",
    "items": [
      {"n": "Sumo", "c": "Asien"},
      {"n": "American Football", "c": "Nordamerika"},
      {"n": "Rugby", "c": "Europa"},
      {"n": "Capoeira", "c": "Suedamerika"},
      {"n": "Curling", "c": "Europa"},
      {"n": "Rodeo", "c": "Nordamerika"},
      {"n": "Sepak Takraw", "c": "Asien"},
      {"n": "Pelota Vasca", "c": "Europa"}
    ]
  }
}

NEW_WS = {
  "fussball": {
    "word": "FUSSBALL",
    "validWords": {
      "de": ["BALL", "FALL", "FALLS", "BASS", "LAUB", "FLUSS", "FASS", "BLAU", "BLASS", "ALBUS", "BULL", "LAUF"],
      "en": ["BALL", "FALL", "FALLS", "BASS", "FULL", "BULL", "LABS", "SLABS", "FLAB", "ABS", "BUS", "BLUFF"]
    }
  },
  "olympiade": {
    "word": "OLYMPIADE",
    "validWords": {
      "de": ["OLYMP", "LAMPE", "LADE", "MADE", "IDEAL", "MAYO", "DAME", "DEMO", "MILD", "DIOL", "PAID", "MODAL", "PLAID", "POEM"],
      "en": ["OLYMPIAD", "PLAY", "AMID", "DIPLOMA", "PAID", "MAID", "LAID", "LAMP", "DAMP", "PALM", "MAYO", "PLAID", "MILD", "MODAL", "POLYAMIDE"]
    }
  },
  "weltmeister": {
    "word": "WELTMEISTER",
    "validWords": {
      "de": ["MEISTER", "WELT", "MISTER", "STREIT", "MIETE", "TITEL", "STIER", "MELT", "WESTE", "LISTE", "ELTER", "STERIL", "MIETES"],
      "en": ["MISTER", "WILT", "STIR", "MELT", "MILE", "SMELT", "STEM", "MERIT", "MERITS", "WILES", "SMILE", "SLIME", "SLIM", "WRITE", "WRITES", "SMELTER", "LITRE"]
    }
  },
  "startschuss": {
    "word": "STARTSCHUSS",
    "validWords": {
      "de": ["START", "SCHUSS", "STAU", "RUSS", "RAUCH", "TRUST", "STUSS", "STRAUCH", "RAUSCH", "TURM"],
      "en": ["STARCH", "CRASH", "TRASH", "CASH", "RASH", "ARCH", "CHARTS", "STAR", "RATS", "CART", "CARTS", "SCAR", "TSAR", "RUST", "CRUST", "THRUST", "RUTS", "CUTS", "TRUSS"]
    }
  },
  "athletik": {
    "word": "ATHLETIK",
    "validWords": {
      "de": ["ETHIK", "HALT", "TAKT", "ACHT", "HALTE", "EILT", "HAIE", "LATHE"],
      "en": ["LITHE", "KITE", "HIKE", "LAKE", "LIKE", "TAKE", "LATE", "TALE", "TILE", "KILT", "HILT", "HALT", "TALK", "ALIKE", "TAIL", "LATH", "LATHE", "TEAK", "HEAL", "HEAT", "EAT", "ATE"]
    }
  },
  "sportgeist": {
    "word": "SPORTGEIST",
    "validWords": {
      "de": ["SPORT", "GEIST", "PREIS", "TIGER", "TIGERS", "GRIPS", "GIST", "RIPS", "STEIG", "TRIPE", "GROT", "TRIPS"],
      "en": ["SPORT", "TIGERS", "GRIPS", "TRIPES", "STRIPE", "STRIPES", "GIST", "TRIPS", "GRIPE", "GRIPES", "SPRITE", "SPRITES", "ROPES", "PERSIST", "GIPSER", "STEP"]
    }
  }
}

# ==============================================================================
# 2. WRITE JSON FILES (idempotent — re-run safe)
# ==============================================================================
def merge_and_write(path, new_data):
    existing = json.loads(path.read_text(encoding="utf-8"))
    overwrites = [k for k in new_data if k in existing]
    if overwrites:
        print(f"  [idempotent] {path.name}: ueberschreibe {len(overwrites)} bestehende Keys (Re-Run)")
    existing.update(new_data)
    path.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    added = len([k for k in new_data if k not in overwrites])
    print(f"  OK {path.name}: +{added} neu, {len(overwrites)} aktualisiert ({len(existing)} total)")

print("-- Schreibe JSON-Daten --")
merge_and_write(DATA / "sport_pin.json",   NEW_PIN)
merge_and_write(DATA / "sport_hl.json",    NEW_HL)
merge_and_write(DATA / "sport_match.json", NEW_MATCH)
merge_and_write(DATA / "sport_ws.json",    NEW_WS)

# ==============================================================================
# 3. WS LETTER VALIDATION
# ==============================================================================
print("-- WS-Buchstabenvalidierung --")
# Step 1: Auto-filter invalid words
for key, entry in NEW_WS.items():
    base = Counter(entry["word"])
    for lang in list(entry["validWords"]):
        before = entry["validWords"][lang]
        filtered = [w for w in before
                    if all(Counter(w)[ch] <= base[ch] for ch in Counter(w))]
        removed = set(before) - set(filtered)
        if removed:
            print(f"  [auto-filter] {key}/{lang}: entfernt {sorted(removed)}")
        entry["validWords"][lang] = filtered

# Step 2: Final validation
errors = []
for key, entry in NEW_WS.items():
    base = Counter(entry["word"])
    for lang, words in entry["validWords"].items():
        for w in words:
            needed = Counter(w)
            for ch, cnt in needed.items():
                if base[ch] < cnt:
                    errors.append(f"  [{key}/{lang}] '{w}' needs {cnt}x'{ch}' but '{entry['word']}' has only {base[ch]}x")

if errors:
    print("  FEHLER:")
    for e in errors:
        print(e)
    sys.exit(1)
else:
    print("  OK Alle WS-Woerter buchstabenvalid")

# Re-write sport_ws.json with filtered validWords
existing_ws = json.loads((DATA / "sport_ws.json").read_text(encoding="utf-8"))
for key, entry in NEW_WS.items():
    existing_ws[key] = entry
(DATA / "sport_ws.json").write_text(json.dumps(existing_ws, ensure_ascii=False, indent=2), encoding="utf-8")
print("  OK sport_ws.json nach Filter neu geschrieben")

# ==============================================================================
# 4. PATCH gen.py
# ==============================================================================
print("-- Patch gen.py --")
c = GEN.read_text(encoding="utf-8")
orig_len = len(c)

# -- Step A: MODES (append before closing brace after staffellauf entry) -------
OLD_MODES = '  {id:"ws_sportwissen_staffellauf",icon:"\\u{1F3C5}",title:"WS: Staffellauf",group:"sport_wissen",noMultiplayer:true,prompt:"Bilde Wörter aus STAFFELLAUF!",desc:"Anagramm-Rätsel — 11 Buchstaben"}'
NEW_MODES_BLOCK = (
    OLD_MODES + ',\n'
    '  /* === Phase 254: Sport-Wissen Expansion === */\n'
    '  /* --- Pin --- */\n'
    '  {id:"uk_sportwissen_fussballstadien",icon:"\\u26BD",title:"Fussballstadien",group:"sport_wissen",prompt:"Wo liegt dieses Fussballstadion?",desc:"Camp Nou, Wembley, Allianz Arena und mehr"},\n'
    '  {id:"uk_sportwissen_motorsport_strecken",icon:"\\u{1F3CE}\\uFE0F",title:"Motorsport-Rennstrecken",group:"sport_wissen",prompt:"Wo liegt diese Rennstrecke?",desc:"Monaco, Monza, Silverstone, Nurburgring"},\n'
    '  {id:"uk_sportwissen_wintersport_orte",icon:"\\u26F7\\uFE0F",title:"Wintersport-Orte",group:"sport_wissen",prompt:"Wo liegt dieser Wintersport-Ort?",desc:"Kitzbuehel, St. Moritz, Whistler"},\n'
    '  {id:"uk_sportwissen_grand_slam_arenen",icon:"\\u{1F3BE}",title:"Grand-Slam-Arenen",group:"sport_wissen",prompt:"Wo liegt diese Tennis-Arena?",desc:"Roland Garros, Wimbledon, US Open, Australian Open"},\n'
    '  {id:"uk_sportwissen_ski_pisten",icon:"\\u{1F3BF}",title:"Ski-Pisten weltweit",group:"sport_wissen",prompt:"Wo liegt dieses Skigebiet?",desc:"Verbier, Chamonix, Aspen, Niseko"},\n'
    '  {id:"uk_sportwissen_golf_platze",icon:"\\u26F3",title:"Golfplaetze weltweit",group:"sport_wissen",prompt:"Wo liegt dieser Golfplatz?",desc:"Augusta, St Andrews, Pebble Beach"},\n'
    '  {id:"uk_sportwissen_surfspots_welt",icon:"\\u{1F3C4}",title:"Surf-Spots weltweit",group:"sport_wissen",prompt:"Wo liegt dieser Surfspot?",desc:"Pipeline, Teahupoo, Nazare, Jeffreys Bay"},\n'
    '  {id:"uk_sportwissen_klettergebiete",icon:"\\u{1F9D7}",title:"Klettergebiete",group:"sport_wissen",prompt:"Wo liegt dieses Klettergebiet?",desc:"Yosemite, Fontainebleau, Kalymnos, Frankenjura"},\n'
    '  /* --- H/L --- */\n'
    '  {id:"hl_sportwissen_transferrekorde",icon:"\\u{1F4B0}",title:"H/L: Transferrekorde",group:"sport_wissen",prompt:"Welcher Transfer war teurer?",desc:"Hoeher/Niedriger: Transfersumme Mio EUR"},\n'
    '  {id:"hl_sportwissen_hochsprung_rekorde",icon:"\\u{1F3C5}",title:"H/L: Hochsprung-Rekorde",group:"sport_wissen",prompt:"Wer sprang hoeher?",desc:"Hoeher/Niedriger: Hochsprungleistung in cm"},\n'
    '  {id:"hl_sportwissen_sportler_gehalt",icon:"\\u{1F4B5}",title:"H/L: Sportler-Gehaelter",group:"sport_wissen",prompt:"Wer verdient mehr?",desc:"Hoeher/Niedriger: Jahresgehalt Mio EUR"},\n'
    '  {id:"hl_sportwissen_olympia_goldmedaillen",icon:"\\u{1F947}",title:"H/L: Olympia-Gold",group:"sport_wissen",prompt:"Wer gewann mehr Goldmedaillen?",desc:"Hoeher/Niedriger: Olympia-Goldmedaillen gesamt"},\n'
    '  {id:"hl_sportwissen_fussball_marktwert",icon:"\\u26BD",title:"H/L: Fussball-Marktwert",group:"sport_wissen",prompt:"Wer hat einen hoeheren Marktwert?",desc:"Hoeher/Niedriger: Transfermarkt-Wert Mio EUR"},\n'
    '  {id:"hl_sportwissen_gewichtheben_rekorde",icon:"\\u{1F3CB}\\uFE0F",title:"H/L: Gewichtheben-Rekorde",group:"sport_wissen",prompt:"Wer hob mehr?",desc:"Hoeher/Niedriger: Gesamtgewicht kg"},\n'
    '  {id:"hl_sportwissen_stadion_baujahr",icon:"\\u{1F3DF}\\uFE0F",title:"H/L: Stadion-Baujahr",group:"sport_wissen",prompt:"Welches Stadion wurde frueher gebaut?",desc:"Hoeher/Niedriger: Baujahr"},\n'
    '  {id:"hl_sportwissen_tore_saison",icon:"\\u26BD",title:"H/L: Tore pro Saison",group:"sport_wissen",prompt:"Wer erzielte mehr Tore in einer Saison?",desc:"Hoeher/Niedriger: Tore"},\n'
    '  /* --- Match --- */\n'
    '  {id:"uk_sportwissen_weltverband",icon:"\\u{1F310}",title:"Sport-Weltverband",group:"sport_wissen",prompt:"Welchem Weltverband gehoert dieser Sport an?",desc:"FIFA, FIBA, World Athletics, ITF und mehr"},\n'
    '  {id:"uk_sportwissen_olympisch",icon:"\\u{1F3C5}",title:"Olympisch?",group:"sport_wissen",prompt:"Ist diese Sportart olympisch?",desc:"Welche Sportarten sind bei Olympia vertreten?"},\n'
    '  {id:"uk_sportwissen_nationalsport_match",icon:"\\u{1F3C6}",title:"Nationalsport weltweit",group:"sport_wissen",prompt:"Welches Land hat diesen Nationalsport?",desc:"Sumo-Japan, Hurling-Irland, Kabaddi-Indien"},\n'
    '  {id:"uk_sportwissen_sportlegende_land",icon:"\\u{1F3C5}",title:"Sportlegenden-Herkunft",group:"sport_wissen",prompt:"Aus welchem Land kommt diese Sportlegende?",desc:"Pele, Ali, Jordan, Federer und mehr"},\n'
    '  {id:"uk_sportwissen_rekordhalter",icon:"\\u{1F3C6}",title:"Weltrekord-Halter",group:"sport_wissen",prompt:"Wer haelt diesen Weltrekord?",desc:"Bolt, Sotomayor, Kiptum, Duplantis"},\n'
    '  {id:"uk_sportwissen_wm_gastgeber_match",icon:"\\u{1F30D}",title:"WM-Gastgeber",group:"sport_wissen",prompt:"In welchem Land fand diese Fussball-WM statt?",desc:"WM-Austragungslaender seit 1930"},\n'
    '  {id:"uk_sportwissen_disziplin_kategorie",icon:"\\u{1F3CB}\\uFE0F",title:"Disziplin-Zuordnung",group:"sport_wissen",prompt:"Zu welcher Disziplin gehoert diese Uebung?",desc:"Rudern, Turnen, Kanu, Schwimmen"},\n'
    '  {id:"uk_sportwissen_sportart_kontinent",icon:"\\u{1F30E}",title:"Sportart & Kontinent",group:"sport_wissen",prompt:"Wo ist diese Sportart am populaersten / entstanden?",desc:"Sumo-Asien, Capoeira-Suedamerika"},\n'
    '  /* --- WS --- */\n'
    '  {id:"ws_sportwissen_fussball",icon:"\\u26BD",title:"WS: Fussball",group:"sport_wissen",noMultiplayer:true,prompt:"Bilde Woerter aus FUSSBALL!",desc:"Anagramm-Raetsel -- 8 Buchstaben"},\n'
    '  {id:"ws_sportwissen_olympiade",icon:"\\u{1F3C5}",title:"WS: Olympiade",group:"sport_wissen",noMultiplayer:true,prompt:"Bilde Woerter aus OLYMPIADE!",desc:"Anagramm-Raetsel -- 9 Buchstaben"},\n'
    '  {id:"ws_sportwissen_weltmeister",icon:"\\u{1F3C6}",title:"WS: Weltmeister",group:"sport_wissen",noMultiplayer:true,prompt:"Bilde Woerter aus WELTMEISTER!",desc:"Anagramm-Raetsel -- 11 Buchstaben"},\n'
    '  {id:"ws_sportwissen_startschuss",icon:"\\u{1F3C1}",title:"WS: Startschuss",group:"sport_wissen",noMultiplayer:true,prompt:"Bilde Woerter aus STARTSCHUSS!",desc:"Anagramm-Raetsel -- 11 Buchstaben"},\n'
    '  {id:"ws_sportwissen_athletik",icon:"\\u{1F3CB}\\uFE0F",title:"WS: Athletik",group:"sport_wissen",noMultiplayer:true,prompt:"Bilde Woerter aus ATHLETIK!",desc:"Anagramm-Raetsel -- 8 Buchstaben"},\n'
    '  {id:"ws_sportwissen_sportgeist",icon:"\\u{1F4AA}",title:"WS: Sportgeist",group:"sport_wissen",noMultiplayer:true,prompt:"Bilde Woerter aus SPORTGEIST!",desc:"Anagramm-Raetsel -- 10 Buchstaben"}'
)
assert c.count(OLD_MODES) == 1, f"MODES-Anker nicht eindeutig: {OLD_MODES[:60]!r}"
c = c.replace(OLD_MODES, NEW_MODES_BLOCK, 1)
print("  OK Step A: 30 MODES-Eintraege eingefuegt")

# -- Step B: MODE_CATS (extend sport_wissen.modes) -----------------------------
OLD_CATS = '"ws_sportwissen_marathon","ws_sportwissen_triathlon","ws_sportwissen_staffellauf"\n  ],cost:0},\n};'
NEW_CATS = (
    '"ws_sportwissen_marathon","ws_sportwissen_triathlon","ws_sportwissen_staffellauf",\n'
    '    /* Phase 254 */ "uk_sportwissen_fussballstadien","uk_sportwissen_motorsport_strecken",\n'
    '    "uk_sportwissen_wintersport_orte","uk_sportwissen_grand_slam_arenen",\n'
    '    "uk_sportwissen_ski_pisten","uk_sportwissen_golf_platze",\n'
    '    "uk_sportwissen_surfspots_welt","uk_sportwissen_klettergebiete",\n'
    '    "hl_sportwissen_transferrekorde","hl_sportwissen_hochsprung_rekorde",\n'
    '    "hl_sportwissen_sportler_gehalt","hl_sportwissen_olympia_goldmedaillen",\n'
    '    "hl_sportwissen_fussball_marktwert","hl_sportwissen_gewichtheben_rekorde",\n'
    '    "hl_sportwissen_stadion_baujahr","hl_sportwissen_tore_saison",\n'
    '    "uk_sportwissen_weltverband","uk_sportwissen_olympisch",\n'
    '    "uk_sportwissen_nationalsport_match","uk_sportwissen_sportlegende_land",\n'
    '    "uk_sportwissen_rekordhalter","uk_sportwissen_wm_gastgeber_match",\n'
    '    "uk_sportwissen_disziplin_kategorie","uk_sportwissen_sportart_kontinent",\n'
    '    "ws_sportwissen_fussball","ws_sportwissen_olympiade","ws_sportwissen_weltmeister",\n'
    '    "ws_sportwissen_startschuss","ws_sportwissen_athletik","ws_sportwissen_sportgeist"\n'
    '  ],cost:0},\n'
    '};'
)
assert c.count(OLD_CATS) == 1, f"MODE_CATS-Anker nicht eindeutig: {OLD_CATS[:60]!r}"
c = c.replace(OLD_CATS, NEW_CATS, 1)
print("  OK Step B: MODE_CATS sport_wissen.modes um 30 IDs erweitert")

# -- Step C: GEN dispatch table ------------------------------------------------
OLD_GEN = '  ws_sportwissen_staffellauf:()=>{initSportWissenWS("staffellauf");return null;},\n  uk_surf_spots:()=>genUniversalPinQ("surf_spots"),'
NEW_GEN = (
    '  ws_sportwissen_staffellauf:()=>{initSportWissenWS("staffellauf");return null;},\n'
    '  /* Phase 254: Sport-Wissen Expansion */\n'
    '  uk_sportwissen_fussballstadien:()=>genSportWissenPinQ("sport_fussballstadien"),\n'
    '  uk_sportwissen_motorsport_strecken:()=>genSportWissenPinQ("sport_motorsport_strecken"),\n'
    '  uk_sportwissen_wintersport_orte:()=>genSportWissenPinQ("sport_wintersport_orte"),\n'
    '  uk_sportwissen_grand_slam_arenen:()=>genSportWissenPinQ("sport_grand_slam_arenen"),\n'
    '  uk_sportwissen_ski_pisten:()=>genSportWissenPinQ("sport_ski_pisten"),\n'
    '  uk_sportwissen_golf_platze:()=>genSportWissenPinQ("sport_golf_platze"),\n'
    '  uk_sportwissen_surfspots_welt:()=>genSportWissenPinQ("sport_surfspots_welt"),\n'
    '  uk_sportwissen_klettergebiete:()=>genSportWissenPinQ("sport_klettergebiete"),\n'
    '  hl_sportwissen_transferrekorde:()=>genSportWissenHL("sport_transferrekorde"),\n'
    '  hl_sportwissen_hochsprung_rekorde:()=>genSportWissenHL("sport_hochsprung_rekorde"),\n'
    '  hl_sportwissen_sportler_gehalt:()=>genSportWissenHL("sport_sportler_gehalt"),\n'
    '  hl_sportwissen_olympia_goldmedaillen:()=>genSportWissenHL("sport_olympia_goldmedaillen"),\n'
    '  hl_sportwissen_fussball_marktwert:()=>genSportWissenHL("sport_fussball_marktwert"),\n'
    '  hl_sportwissen_gewichtheben_rekorde:()=>genSportWissenHL("sport_gewichtheben_rekorde"),\n'
    '  hl_sportwissen_stadion_baujahr:()=>genSportWissenHL("sport_stadion_baujahr"),\n'
    '  hl_sportwissen_tore_saison:()=>genSportWissenHL("sport_tore_saison"),\n'
    '  uk_sportwissen_weltverband:()=>genSportWissenMatchQ("sport_weltverband"),\n'
    '  uk_sportwissen_olympisch:()=>genSportWissenMatchQ("sport_olympisch"),\n'
    '  uk_sportwissen_nationalsport_match:()=>genSportWissenMatchQ("sport_nationalsport_match"),\n'
    '  uk_sportwissen_sportlegende_land:()=>genSportWissenMatchQ("sport_sportlegende_land"),\n'
    '  uk_sportwissen_rekordhalter:()=>genSportWissenMatchQ("sport_rekordhalter"),\n'
    '  uk_sportwissen_wm_gastgeber_match:()=>genSportWissenMatchQ("sport_wm_gastgeber_match"),\n'
    '  uk_sportwissen_disziplin_kategorie:()=>genSportWissenMatchQ("sport_disziplin_kategorie"),\n'
    '  uk_sportwissen_sportart_kontinent:()=>genSportWissenMatchQ("sport_sportart_kontinent"),\n'
    '  ws_sportwissen_fussball:()=>{initSportWissenWS("fussball");return null;},\n'
    '  ws_sportwissen_olympiade:()=>{initSportWissenWS("olympiade");return null;},\n'
    '  ws_sportwissen_weltmeister:()=>{initSportWissenWS("weltmeister");return null;},\n'
    '  ws_sportwissen_startschuss:()=>{initSportWissenWS("startschuss");return null;},\n'
    '  ws_sportwissen_athletik:()=>{initSportWissenWS("athletik");return null;},\n'
    '  ws_sportwissen_sportgeist:()=>{initSportWissenWS("sportgeist");return null;},\n'
    '  uk_surf_spots:()=>genUniversalPinQ("surf_spots"),'
)
assert c.count(OLD_GEN) == 1, f"GEN-Anker nicht eindeutig: {OLD_GEN[:60]!r}"
c = c.replace(OLD_GEN, NEW_GEN, 1)
print("  OK Step C: GEN dispatch um 30 Eintraege erweitert")

GEN.write_text(c, encoding="utf-8")
print(f"  OK gen.py geschrieben ({orig_len} -> {len(c)} bytes, Delta={len(c)-orig_len:+d})")
print("\nOK patch_254_sport_expansion.py FERTIG")
