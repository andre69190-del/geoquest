"""
Phase 411 — Games & Hardware
- data/konsolen.json (30 Konsolen, Vollschema)
- data/timeline.json (+ konsolen_bj Einträge)
- validate_content.py (check_konsolen)
- gen.py:
    - Kategorie "Gaming" → "Games & Hardware"
    - KONSOLEN_DATA Placeholder + Loader
    - 6 neue Modi: timeline_konsolen_bj, hl_konsolen_verkauf, hl_konsolen_preis,
                   match_konsolen_hersteller, match_konsolen_medium, match_konsolen_handheld
    - genKonsolenHL / genKonsolenMatch Generator-Funktionen
    - i18n EN+PL für neue Prompts
"""
import os, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

def r(path): return open(path,'r',encoding='utf-8').read()
def w(path, content): open(path,'w',encoding='utf-8').write(content)

def rpl(c, old, new, label):
    assert c.count(old) == 1, f"ANCHOR NICHT EINDEUTIG ({c.count(old)}x): {label!r}"
    return c.replace(old, new)

# ─────────────────────────────────────────────────────────────
# 1. konsolen.json
# ─────────────────────────────────────────────────────────────
KONSOLEN = {
  "Atari 2600": {
    "hersteller": "Atari", "erscheinungsjahr": 1977, "eingestellt_jahr": 1992,
    "generation": 2, "verkauf_mio": 30.0, "preis_usd": 199,
    "cpu_mhz": 1.19, "ram_kb": 0.125,
    "herkunftsland": "USA", "nachfolger_von": None,
    "medium": "Cartridge", "aufloesung_max": "240p",
    "online_faehig": False, "handheld": False,
    "bekannteste_spiele": ["Space Invaders", "Pitfall!", "Pac-Man"]
  },
  "ColecoVision": {
    "hersteller": "Coleco", "erscheinungsjahr": 1982, "eingestellt_jahr": 1985,
    "generation": 2, "verkauf_mio": 6.0, "preis_usd": 175,
    "cpu_mhz": 3.58, "ram_kb": 1.0,
    "herkunftsland": "USA", "nachfolger_von": None,
    "medium": "Cartridge", "aufloesung_max": "240p",
    "online_faehig": False, "handheld": False,
    "bekannteste_spiele": ["Donkey Kong", "Zaxxon", "Q*bert"]
  },
  "NES": {
    "hersteller": "Nintendo", "erscheinungsjahr": 1983, "eingestellt_jahr": 2003,
    "generation": 3, "verkauf_mio": 61.91, "preis_usd": 179,
    "cpu_mhz": 1.79, "ram_kb": 2.0,
    "herkunftsland": "Japan", "nachfolger_von": None,
    "medium": "Cartridge", "aufloesung_max": "240p",
    "online_faehig": False, "handheld": False,
    "bekannteste_spiele": ["Super Mario Bros.", "The Legend of Zelda", "Metroid"]
  },
  "Sega Master System": {
    "hersteller": "Sega", "erscheinungsjahr": 1985, "eingestellt_jahr": 1996,
    "generation": 3, "verkauf_mio": 13.0, "preis_usd": 200,
    "cpu_mhz": 3.58, "ram_kb": 8.0,
    "herkunftsland": "Japan", "nachfolger_von": None,
    "medium": "Cartridge", "aufloesung_max": "240p",
    "online_faehig": False, "handheld": False,
    "bekannteste_spiele": ["Alex Kidd in Miracle World", "Phantasy Star", "Sonic the Hedgehog"]
  },
  "Sega Mega Drive": {
    "hersteller": "Sega", "erscheinungsjahr": 1988, "eingestellt_jahr": 1997,
    "generation": 4, "verkauf_mio": 30.75, "preis_usd": 189,
    "cpu_mhz": 7.61, "ram_kb": 64.0,
    "herkunftsland": "Japan", "nachfolger_von": "Sega Master System",
    "medium": "Cartridge", "aufloesung_max": "240p",
    "online_faehig": False, "handheld": False,
    "bekannteste_spiele": ["Sonic the Hedgehog", "Streets of Rage", "Mortal Kombat"]
  },
  "Game Boy": {
    "hersteller": "Nintendo", "erscheinungsjahr": 1989, "eingestellt_jahr": 2003,
    "generation": 1, "verkauf_mio": 118.69, "preis_usd": 89,
    "cpu_mhz": 4.19, "ram_kb": 8.0,
    "herkunftsland": "Japan", "nachfolger_von": None,
    "medium": "Cartridge", "aufloesung_max": "240p",
    "online_faehig": False, "handheld": True,
    "bekannteste_spiele": ["Tetris", "Pokémon Red/Blue", "Super Mario Land"]
  },
  "Super Nintendo": {
    "hersteller": "Nintendo", "erscheinungsjahr": 1990, "eingestellt_jahr": 2003,
    "generation": 4, "verkauf_mio": 49.1, "preis_usd": 199,
    "cpu_mhz": 3.58, "ram_kb": 128.0,
    "herkunftsland": "Japan", "nachfolger_von": "NES",
    "medium": "Cartridge", "aufloesung_max": "240p",
    "online_faehig": False, "handheld": False,
    "bekannteste_spiele": ["Super Mario World", "The Legend of Zelda: A Link to the Past", "Street Fighter II"]
  },
  "Neo Geo AES": {
    "hersteller": "SNK", "erscheinungsjahr": 1990, "eingestellt_jahr": 1997,
    "generation": 4, "verkauf_mio": 1.0, "preis_usd": 649,
    "cpu_mhz": 12.0, "ram_kb": 64.0,
    "herkunftsland": "Japan", "nachfolger_von": None,
    "medium": "Cartridge", "aufloesung_max": "240p",
    "online_faehig": False, "handheld": False,
    "bekannteste_spiele": ["Metal Slug", "The King of Fighters '94", "Samurai Shodown"]
  },
  "Atari Jaguar": {
    "hersteller": "Atari", "erscheinungsjahr": 1993, "eingestellt_jahr": 1996,
    "generation": 5, "verkauf_mio": 0.25, "preis_usd": 249,
    "cpu_mhz": 26.59, "ram_kb": 2048.0,
    "herkunftsland": "USA", "nachfolger_von": "Atari 2600",
    "medium": "Cartridge", "aufloesung_max": "480i",
    "online_faehig": False, "handheld": False,
    "bekannteste_spiele": ["Alien vs. Predator", "Tempest 2000", "Doom"]
  },
  "Sony PlayStation": {
    "hersteller": "Sony", "erscheinungsjahr": 1994, "eingestellt_jahr": 2006,
    "generation": 5, "verkauf_mio": 102.49, "preis_usd": 299,
    "cpu_mhz": 33.87, "ram_kb": 2048.0,
    "herkunftsland": "Japan", "nachfolger_von": None,
    "medium": "CD", "aufloesung_max": "480i",
    "online_faehig": False, "handheld": False,
    "bekannteste_spiele": ["Final Fantasy VII", "Gran Turismo", "Crash Bandicoot"]
  },
  "Sega Saturn": {
    "hersteller": "Sega", "erscheinungsjahr": 1994, "eingestellt_jahr": 2000,
    "generation": 5, "verkauf_mio": 9.5, "preis_usd": 399,
    "cpu_mhz": 28.6, "ram_kb": 2048.0,
    "herkunftsland": "Japan", "nachfolger_von": "Sega Mega Drive",
    "medium": "CD", "aufloesung_max": "480i",
    "online_faehig": False, "handheld": False,
    "bekannteste_spiele": ["Nights into Dreams", "Virtua Fighter 2", "Panzer Dragoon"]
  },
  "Nintendo 64": {
    "hersteller": "Nintendo", "erscheinungsjahr": 1996, "eingestellt_jahr": 2002,
    "generation": 5, "verkauf_mio": 32.93, "preis_usd": 199,
    "cpu_mhz": 93.75, "ram_kb": 4096.0,
    "herkunftsland": "Japan", "nachfolger_von": "Super Nintendo",
    "medium": "Cartridge", "aufloesung_max": "480i",
    "online_faehig": False, "handheld": False,
    "bekannteste_spiele": ["Super Mario 64", "The Legend of Zelda: Ocarina of Time", "GoldenEye 007"]
  },
  "Sega Dreamcast": {
    "hersteller": "Sega", "erscheinungsjahr": 1998, "eingestellt_jahr": 2001,
    "generation": 6, "verkauf_mio": 10.6, "preis_usd": 199,
    "cpu_mhz": 200.0, "ram_kb": 16384.0,
    "herkunftsland": "Japan", "nachfolger_von": "Sega Saturn",
    "medium": "GD-ROM", "aufloesung_max": "480p",
    "online_faehig": True, "handheld": False,
    "bekannteste_spiele": ["Sonic Adventure", "Shenmue", "SoulCalibur"]
  },
  "PlayStation 2": {
    "hersteller": "Sony", "erscheinungsjahr": 2000, "eingestellt_jahr": 2013,
    "generation": 6, "verkauf_mio": 155.0, "preis_usd": 299,
    "cpu_mhz": 294.91, "ram_kb": 32768.0,
    "herkunftsland": "Japan", "nachfolger_von": "Sony PlayStation",
    "medium": "DVD", "aufloesung_max": "480p",
    "online_faehig": True, "handheld": False,
    "bekannteste_spiele": ["Grand Theft Auto: San Andreas", "Kingdom Hearts", "Shadow of the Colossus"]
  },
  "Game Boy Advance": {
    "hersteller": "Nintendo", "erscheinungsjahr": 2001, "eingestellt_jahr": 2010,
    "generation": 3, "verkauf_mio": 81.51, "preis_usd": 99,
    "cpu_mhz": 16.78, "ram_kb": 256.0,
    "herkunftsland": "Japan", "nachfolger_von": "Game Boy",
    "medium": "Cartridge", "aufloesung_max": "240p",
    "online_faehig": False, "handheld": True,
    "bekannteste_spiele": ["Pokémon Ruby/Sapphire", "Golden Sun", "Metroid Fusion"]
  },
  "Nintendo GameCube": {
    "hersteller": "Nintendo", "erscheinungsjahr": 2001, "eingestellt_jahr": 2007,
    "generation": 6, "verkauf_mio": 21.74, "preis_usd": 199,
    "cpu_mhz": 485.0, "ram_kb": 24576.0,
    "herkunftsland": "Japan", "nachfolger_von": "Nintendo 64",
    "medium": "Mini-DVD", "aufloesung_max": "480p",
    "online_faehig": True, "handheld": False,
    "bekannteste_spiele": ["Super Smash Bros. Melee", "The Legend of Zelda: Wind Waker", "Metroid Prime"]
  },
  "Xbox": {
    "hersteller": "Microsoft", "erscheinungsjahr": 2001, "eingestellt_jahr": 2009,
    "generation": 6, "verkauf_mio": 24.0, "preis_usd": 299,
    "cpu_mhz": 733.0, "ram_kb": 65536.0,
    "herkunftsland": "USA", "nachfolger_von": None,
    "medium": "DVD", "aufloesung_max": "480p",
    "online_faehig": True, "handheld": False,
    "bekannteste_spiele": ["Halo: Combat Evolved", "Project Gotham Racing", "Fable"]
  },
  "Nintendo DS": {
    "hersteller": "Nintendo", "erscheinungsjahr": 2004, "eingestellt_jahr": 2014,
    "generation": 4, "verkauf_mio": 154.02, "preis_usd": 149,
    "cpu_mhz": 67.0, "ram_kb": 4096.0,
    "herkunftsland": "Japan", "nachfolger_von": "Game Boy Advance",
    "medium": "Cartridge", "aufloesung_max": "240p",
    "online_faehig": True, "handheld": True,
    "bekannteste_spiele": ["Pokémon Diamond/Pearl", "New Super Mario Bros.", "Brain Age"]
  },
  "PlayStation Portable": {
    "hersteller": "Sony", "erscheinungsjahr": 2004, "eingestellt_jahr": 2014,
    "generation": 4, "verkauf_mio": 80.0, "preis_usd": 249,
    "cpu_mhz": 333.0, "ram_kb": 32768.0,
    "herkunftsland": "Japan", "nachfolger_von": None,
    "medium": "UMD", "aufloesung_max": "480p",
    "online_faehig": True, "handheld": True,
    "bekannteste_spiele": ["God of War: Chains of Olympus", "Crisis Core: Final Fantasy VII", "Monster Hunter Freedom"]
  },
  "Xbox 360": {
    "hersteller": "Microsoft", "erscheinungsjahr": 2005, "eingestellt_jahr": 2016,
    "generation": 7, "verkauf_mio": 84.0, "preis_usd": 299,
    "cpu_mhz": 3200.0, "ram_kb": 524288.0,
    "herkunftsland": "USA", "nachfolger_von": "Xbox",
    "medium": "DVD", "aufloesung_max": "1080p",
    "online_faehig": True, "handheld": False,
    "bekannteste_spiele": ["Halo 3", "Gears of War", "Red Dead Redemption"]
  },
  "PlayStation 3": {
    "hersteller": "Sony", "erscheinungsjahr": 2006, "eingestellt_jahr": 2017,
    "generation": 7, "verkauf_mio": 87.4, "preis_usd": 499,
    "cpu_mhz": 3200.0, "ram_kb": 524288.0,
    "herkunftsland": "Japan", "nachfolger_von": "PlayStation 2",
    "medium": "Blu-ray", "aufloesung_max": "1080p",
    "online_faehig": True, "handheld": False,
    "bekannteste_spiele": ["The Last of Us", "Uncharted 2", "Metal Gear Solid 4"]
  },
  "Nintendo Wii": {
    "hersteller": "Nintendo", "erscheinungsjahr": 2006, "eingestellt_jahr": 2017,
    "generation": 7, "verkauf_mio": 101.63, "preis_usd": 249,
    "cpu_mhz": 729.0, "ram_kb": 88064.0,
    "herkunftsland": "Japan", "nachfolger_von": "Nintendo GameCube",
    "medium": "DVD", "aufloesung_max": "480p",
    "online_faehig": True, "handheld": False,
    "bekannteste_spiele": ["Wii Sports", "Mario Kart Wii", "Super Smash Bros. Brawl"]
  },
  "Nintendo 3DS": {
    "hersteller": "Nintendo", "erscheinungsjahr": 2011, "eingestellt_jahr": 2023,
    "generation": 5, "verkauf_mio": 75.94, "preis_usd": 249,
    "cpu_mhz": 268.0, "ram_kb": 131072.0,
    "herkunftsland": "Japan", "nachfolger_von": "Nintendo DS",
    "medium": "Cartridge", "aufloesung_max": "240p",
    "online_faehig": True, "handheld": True,
    "bekannteste_spiele": ["Pokémon X/Y", "Animal Crossing: New Leaf", "The Legend of Zelda: A Link Between Worlds"]
  },
  "PlayStation Vita": {
    "hersteller": "Sony", "erscheinungsjahr": 2011, "eingestellt_jahr": 2019,
    "generation": 5, "verkauf_mio": 16.0, "preis_usd": 249,
    "cpu_mhz": 444.0, "ram_kb": 524288.0,
    "herkunftsland": "Japan", "nachfolger_von": "PlayStation Portable",
    "medium": "Cartridge", "aufloesung_max": "480p",
    "online_faehig": True, "handheld": True,
    "bekannteste_spiele": ["Persona 4 Golden", "Tearaway", "Gravity Rush"]
  },
  "Nintendo Wii U": {
    "hersteller": "Nintendo", "erscheinungsjahr": 2012, "eingestellt_jahr": 2017,
    "generation": 8, "verkauf_mio": 13.56, "preis_usd": 299,
    "cpu_mhz": 1243.0, "ram_kb": 2097152.0,
    "herkunftsland": "Japan", "nachfolger_von": "Nintendo Wii",
    "medium": "Blu-ray", "aufloesung_max": "1080p",
    "online_faehig": True, "handheld": False,
    "bekannteste_spiele": ["Super Mario 3D World", "Mario Kart 8", "The Legend of Zelda: Wind Waker HD"]
  },
  "PlayStation 4": {
    "hersteller": "Sony", "erscheinungsjahr": 2013, "eingestellt_jahr": None,
    "generation": 8, "verkauf_mio": 117.2, "preis_usd": 399,
    "cpu_mhz": 1600.0, "ram_kb": 8388608.0,
    "herkunftsland": "Japan", "nachfolger_von": "PlayStation 3",
    "medium": "Blu-ray", "aufloesung_max": "1080p",
    "online_faehig": True, "handheld": False,
    "bekannteste_spiele": ["The Last of Us Part II", "God of War", "Red Dead Redemption 2"]
  },
  "Xbox One": {
    "hersteller": "Microsoft", "erscheinungsjahr": 2013, "eingestellt_jahr": 2020,
    "generation": 8, "verkauf_mio": 51.0, "preis_usd": 499,
    "cpu_mhz": 1750.0, "ram_kb": 8388608.0,
    "herkunftsland": "USA", "nachfolger_von": "Xbox 360",
    "medium": "Blu-ray", "aufloesung_max": "1080p",
    "online_faehig": True, "handheld": False,
    "bekannteste_spiele": ["Halo 5: Guardians", "Forza Motorsport 5", "Ori and the Blind Forest"]
  },
  "Nintendo Switch": {
    "hersteller": "Nintendo", "erscheinungsjahr": 2017, "eingestellt_jahr": None,
    "generation": 9, "verkauf_mio": 140.0, "preis_usd": 299,
    "cpu_mhz": 1020.0, "ram_kb": 4194304.0,
    "herkunftsland": "Japan", "nachfolger_von": "Nintendo Wii U",
    "medium": "Cartridge", "aufloesung_max": "1080p",
    "online_faehig": True, "handheld": True,
    "bekannteste_spiele": ["The Legend of Zelda: Breath of the Wild", "Animal Crossing: New Horizons", "Mario Kart 8 Deluxe"]
  },
  "PlayStation 5": {
    "hersteller": "Sony", "erscheinungsjahr": 2020, "eingestellt_jahr": None,
    "generation": 9, "verkauf_mio": 59.3, "preis_usd": 499,
    "cpu_mhz": 3500.0, "ram_kb": 16777216.0,
    "herkunftsland": "Japan", "nachfolger_von": "PlayStation 4",
    "medium": "Blu-ray", "aufloesung_max": "4K",
    "online_faehig": True, "handheld": False,
    "bekannteste_spiele": ["Demon's Souls", "Ratchet & Clank: Rift Apart", "Horizon Forbidden West"]
  },
  "Xbox Series X": {
    "hersteller": "Microsoft", "erscheinungsjahr": 2020, "eingestellt_jahr": None,
    "generation": 9, "verkauf_mio": 21.0, "preis_usd": 499,
    "cpu_mhz": 3800.0, "ram_kb": 16777216.0,
    "herkunftsland": "USA", "nachfolger_von": "Xbox One",
    "medium": "Blu-ray", "aufloesung_max": "4K",
    "online_faehig": True, "handheld": False,
    "bekannteste_spiele": ["Halo Infinite", "Forza Horizon 5", "Microsoft Flight Simulator"]
  }
}

konsolen_path = os.path.join(ROOT, 'data', 'konsolen.json')
w(konsolen_path, json.dumps(KONSOLEN, ensure_ascii=False, indent=2))
print(f"✅ konsolen.json: {len(KONSOLEN)} Einträge geschrieben")

# ─────────────────────────────────────────────────────────────
# 2. timeline.json — konsolen_bj Einträge hinzufügen
# ─────────────────────────────────────────────────────────────
tl_path = os.path.join(ROOT, 'data', 'timeline.json')
tl = json.loads(r(tl_path))
assert "konsolen_bj" not in tl, "konsolen_bj bereits in timeline.json!"

tl["konsolen_bj"] = {
  "prompt": "Sortiere die Konsolen nach Erscheinungsjahr (älteste zuerst)!",
  "unit": "Jahr",
  "items": [
    {"n": "Atari 2600",       "year": 1977, "hint": "Erste echte Heimkonsole für die Massen"},
    {"n": "NES",              "year": 1983, "hint": "Rettete die Videospielbranche nach dem Crash 1983"},
    {"n": "Sega Mega Drive",  "year": 1988, "hint": "Sega does what Nintendon't"},
    {"n": "Game Boy",         "year": 1989, "hint": "118 Mio verkaufte Einheiten — Tetris inklusive"},
    {"n": "Super Nintendo",   "year": 1990, "hint": "Rivals mit dem Mega Drive — der 16-bit-Krieg"},
    {"n": "Sony PlayStation", "year": 1994, "hint": "Sonys erster Schritt ins Konsolen-Business"},
    {"n": "Sega Saturn",      "year": 1994, "hint": "Überraschender Früh-Launch — kostet Sega teuer"},
    {"n": "Nintendo 64",      "year": 1996, "hint": "Letzter Cartridge-Veteran der großen Drei"},
    {"n": "Sega Dreamcast",   "year": 1998, "hint": "Segas letzte Heimkonsole — mit Online-Modem"},
    {"n": "PlayStation 2",    "year": 2000, "hint": "Meistverkaufte Konsole aller Zeiten: 155 Mio"},
    {"n": "Xbox",             "year": 2001, "hint": "Microsofts Debüt — mit eingebautem Halo"},
    {"n": "Nintendo DS",      "year": 2004, "hint": "Zwei Bildschirme, einer davon Touch"},
    {"n": "Xbox 360",         "year": 2005, "hint": "Startete die HD-Ära mit Achievements"},
    {"n": "Nintendo Wii",     "year": 2006, "hint": "Bewegungssteuerung für alle — Wii Sports Kult"},
    {"n": "PlayStation 3",    "year": 2006, "hint": "Blu-ray-Player und Cell-Prozessor im Paket"},
    {"n": "Nintendo 3DS",     "year": 2011, "hint": "3D ohne Brille — später Pokémon X/Y"},
    {"n": "PlayStation 4",    "year": 2013, "hint": "117 Mio Einheiten — dominante Gen-8-Konsole"},
    {"n": "Nintendo Switch",  "year": 2017, "hint": "Hybrid: Heimkonsole und Handheld in einem"},
    {"n": "PlayStation 5",    "year": 2020, "hint": "SSD-Revolution und DualSense Haptics"},
    {"n": "Xbox Series X",    "year": 2020, "hint": "Quick Resume und Game Pass — MS setzt auf Services"}
  ]
}

w(tl_path, json.dumps(tl, ensure_ascii=False, indent=2))
print(f"✅ timeline.json: konsolen_bj mit {len(tl['konsolen_bj']['items'])} Einträgen hinzugefügt")

# ─────────────────────────────────────────────────────────────
# 3. validate_content.py
# ─────────────────────────────────────────────────────────────
val_path = os.path.join(ROOT, 'validate_content.py')
vc = r(val_path)

CHECK_KONSOLEN = '''
def check_konsolen(filename, data):
    REQUIRED = [
        "hersteller", "erscheinungsjahr", "eingestellt_jahr", "generation",
        "verkauf_mio", "preis_usd", "cpu_mhz", "ram_kb", "herkunftsland",
        "nachfolger_von", "medium", "aufloesung_max", "online_faehig",
        "handheld", "bekannteste_spiele"
    ]
    MEDIUM = {"Cartridge", "CD", "DVD", "Blu-ray", "GD-ROM", "UMD", "Mini-DVD", "Digital"}
    AUFLOESUNG = {"144p", "240p", "480i", "480p", "576p", "720p", "1080p", "4K"}
    HERSTELLER = {"Nintendo", "Sony", "Microsoft", "Sega", "Atari", "SNK", "Coleco",
                  "NEC", "3DO Company", "Mattel"}
    for name, entry in data.items():
        for f in REQUIRED:
            if f not in entry:
                warn(filename, name, f, f"Pflichtfeld fehlt")
        m = entry.get("medium")
        if m and m not in MEDIUM:
            warn(filename, name, "medium", f"Unbekanntes Medium: {m!r}")
        a = entry.get("aufloesung_max")
        if a and a not in AUFLOESUNG:
            warn(filename, name, "aufloesung_max", f"Unbekannte Auflösung: {a!r}")
        if not isinstance(entry.get("online_faehig"), bool):
            warn(filename, name, "online_faehig", "Kein Bool")
        if not isinstance(entry.get("handheld"), bool):
            warn(filename, name, "handheld", "Kein Bool")
        spiele = entry.get("bekannteste_spiele", [])
        if not isinstance(spiele, list) or len(spiele) < 1:
            warn(filename, name, "bekannteste_spiele", "Mindestens 1 Spiel erwartet")

'''

# Vor check_games_extended einfügen
vc = rpl(vc,
    "def check_games_extended(filename, data):",
    CHECK_KONSOLEN + "def check_games_extended(filename, data):",
    "check_konsolen insertion")

# Call im elif-Baum nach autos_extended
vc = rpl(vc,
    '    elif name == "autos_extended.json":\n        check_autos_extended(filename, data)',
    '    elif name == "autos_extended.json":\n        check_autos_extended(filename, data)\n    elif name == "konsolen.json":\n        check_konsolen(filename, data)',
    "konsolen elif call")

w(val_path, vc)
print("✅ validate_content.py aktualisiert (check_konsolen hinzugefügt)")

# ─────────────────────────────────────────────────────────────
# 4. gen.py
# ─────────────────────────────────────────────────────────────
gen_path = os.path.join(ROOT, 'gen.py')
c = r(gen_path)

# 4a. Python-Loader
c = rpl(c,
    "with open(os.path.join(os.path.dirname(__file__), 'data/games_extended.json'), 'r', encoding='utf-8') as _gf:",
    "with open(os.path.join(os.path.dirname(__file__), 'data/konsolen.json'), 'r', encoding='utf-8') as _kf:\n        KONSOLEN_J = __import__('json').dumps(__import__('json').load(_kf), ensure_ascii=False, separators=(',',':'))\n    with open(os.path.join(os.path.dirname(__file__), 'data/games_extended.json'), 'r', encoding='utf-8') as _gf:",
    "py loader konsolen")

# 4b. JS Konstante
c = rpl(c,
    "const GAMES_EXT_DATA=PLACEHOLDER_GAMES_EXT;\n",
    "const GAMES_EXT_DATA=PLACEHOLDER_GAMES_EXT;\nconst KONSOLEN_DATA=PLACEHOLDER_KONSOLEN;\n",
    "js const KONSOLEN_DATA")

# 4c. Kategorie-Label umbenennen
c = rpl(c,
    'games:{label:"Gaming",icon:',
    'games:{label:"Games & Hardware",icon:',
    "rename Gaming label")

# 4d. Generator-Funktionen (vor Pflanzen-Block einfügen)
GEN_FUNS = r'''
/* Phase 411: genKonsolenHL / genKonsolenMatch */
function genKonsolenHL(field,opts){
  var o=opts||{};
  var items=[];
  var _KD=KONSOLEN_DATA;
  var _ks=Object.keys(_KD).filter(function(k){return Object.prototype.hasOwnProperty.call(_KD,k)});
  for(var _i=0;_i<_ks.length;_i++){
    var _n=_ks[_i];
    var _v=+(_KD[_n][field]);
    if(!_v||isNaN(_v)||_v<=0)continue;
    items.push({name:_n,val:_v});
  }
  if(items.length<4)return null;
  items.sort(function(a,b){return a.val-b.val;});
  var len=items.length;
  var tries=0;
  while(tries++<40){
    var ai=~~(rng()*len);
    var W=Math.max(1,Math.floor(len*(S.diff==='hardcore'?0.03:0.12)));
    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);
    var pool=[];
    for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}
    if(!pool.length)continue;
    var bi=pool[~~(rng()*pool.length)];
    var a=items[ai],b=items[bi];
    if(a.val===b.val)continue;
    var span=items[len-1].val-items[0].val;
    if(span>0&&Math.abs(a.val-b.val)<span*0.02)continue;
    var winner=o.lowerWins?(a.val<b.val?a:b):(a.val>b.val?a:b);
    var unit=o.unit||"";
    var meta=a.name+": "+a.val+(unit?" "+unit:"")+" · "+b.name+": "+b.val+(unit?" "+unit:"");
    return{type:"beta_hl",prompt:o.prompt||"Welches ist höher?",subj:"",
      opts:[a.name,b.name],ans:winner.name,meta:meta,
      lid:"khl_"+field+"_"+ai+"_"+bi,cc:"de"};
  }
  return null;
}
function genKonsolenMatch(field,prompt,fixedPool){
  var _KD=KONSOLEN_DATA;
  var valid=Object.keys(_KD).filter(function(k){return Object.prototype.hasOwnProperty.call(_KD,k)}).filter(function(n){
    var v=_KD[n][field];
    return v!==undefined&&v!==null&&v!=="";
  });
  if(valid.length<4)return null;
  var idx=~~(rng()*valid.length);
  var cons=valid[idx];
  var rawVal=_KD[cons][field];
  var correct=typeof rawVal==="boolean"?(rawVal?_tc("Handheld"):_tc("Heimkonsole")):String(rawVal);
  var pool=fixedPool
    ?fixedPool.filter(function(v){return v!==correct;})
    :valid.map(function(n){
        var rv=_KD[n][field];
        return typeof rv==="boolean"?(rv?_tc("Handheld"):_tc("Heimkonsole")):String(rv);
      }).filter(function(v,i,a){return a.indexOf(v)===i}).filter(function(v){return v!==correct;});
  if(pool.length<3)return null;
  var p=pool.slice();
  for(var j=p.length-1;j>0;j--){var k=~~(rng()*(j+1));var t=p[j];p[j]=p[k];p[k]=t;}
  var dis=p.slice(0,3);
  var opts=[correct].concat(dis);
  for(var j2=opts.length-1;j2>0;j2--){var k2=~~(rng()*(j2+1));var t2=opts[j2];opts[j2]=opts[k2];opts[k2]=t2;}
  return{type:"uk_match",prompt:prompt||("Eigenschaft von "+cons+"?"),
    subj:cons,ans:correct,opts:opts,lid:"kmatch_"+field+"_"+idx,cc:"de"};
}

'''

c = rpl(c,
    "/* === Phase 228: Pflanzen-Generatoren === */",
    GEN_FUNS + "/* === Phase 228: Pflanzen-Generatoren === */",
    "gen fns konsolen")

# 4e. MODES Einträge (nach letztem hl_games_dev_lat Eintrag)
NEW_MODES = r'''
    {id:"timeline_konsolen_bj",  icon:"\u{1F4C5}",title:"Hardware-Timeline",         group:"games",prompt:"Sortiere die Konsolen nach Erscheinungsjahr!",               desc:"Von Atari bis PS5 — die Geschichte der Spielkonsolen.",                  prompt_en:"Sort the consoles by release year!"},
    {id:"hl_konsolen_verkauf",   icon:"\u{1F4E6}",title:"Konsolen-Quartett: Absatz",  group:"games",prompt:"Welche Konsole hat mehr Einheiten verkauft?",                desc:"In Millionen — von 0,25 Mio. bis 155 Mio.",                             prompt_en:"Which console sold more units?"},
    {id:"hl_konsolen_preis",     icon:"\u{1F4B5}",title:"Konsolen-Quartett: Preis",   group:"games",prompt:"Welche Konsole war beim Launch teurer?",                     desc:"Launch-Preis in USD — manchmal spiegelt er Epik wider.",                 prompt_en:"Which console had the higher launch price?"},
    {id:"match_konsolen_hersteller",icon:"\u{1F3ED}",title:"Konsole: Hersteller",     group:"games",prompt:"Welches Unternehmen hat diese Konsole hergestellt?",          desc:"Sony, Nintendo, Microsoft, Sega oder Atari?",                           prompt_en:"Which company manufactured this console?"},
    {id:"match_konsolen_medium", icon:"\u{1F4BF}",title:"Konsole: Speichermedium",    group:"games",prompt:"Welches Medium nutzt diese Konsole?",                        desc:"Cartridge, CD, DVD, Blu-ray, GD-ROM oder UMD?",                         prompt_en:"Which storage medium does this console use?"},
    {id:"match_konsolen_handheld",icon:"\u{1F4F1}",title:"Konsole: Handheld?",        group:"games",prompt:"Heimkonsole oder Handheld?",                                 desc:"Standfest oder in der Hosentasche?",                                    prompt_en:"Home console or handheld?"},
'''

c = rpl(c,
    '},\n\n    {id:"uk_hafen_world"',
    NEW_MODES + '\n    {id:"uk_hafen_world"',
    "new modes after games")

# 4f. MODE_CATS games: neue Modi anhängen
c = rpl(c,
    '"games_baujahr_mc"],cost:0}',
    '"games_baujahr_mc","timeline_konsolen_bj","hl_konsolen_verkauf","hl_konsolen_preis","match_konsolen_hersteller","match_konsolen_medium","match_konsolen_handheld"],cost:0}',
    "MODE_CATS games extend")

# 4g. Dispatch-Einträge
NEW_DISPATCH = '''  timeline_konsolen_bj:()=>genTimelineQ("konsolen_bj"),
  hl_konsolen_verkauf:()=>genKonsolenHL("verkauf_mio",{unit:"Mio.",prompt:_tc("Welche Konsole hat mehr Einheiten verkauft?")}),
  hl_konsolen_preis:()=>genKonsolenHL("preis_usd",{unit:"USD",prompt:_tc("Welche Konsole war beim Launch teurer?")}),
  match_konsolen_hersteller:()=>genKonsolenMatch("hersteller",_tc("Welches Unternehmen hat diese Konsole hergestellt?"),["Nintendo","Sony","Microsoft","Sega","Atari","SNK","Coleco"]),
  match_konsolen_medium:()=>genKonsolenMatch("medium",_tc("Welches Medium nutzt diese Konsole?"),["Cartridge","CD","DVD","Blu-ray","GD-ROM","UMD","Mini-DVD"]),
  match_konsolen_handheld:()=>genKonsolenMatch("handheld",_tc("Heimkonsole oder Handheld?")),
'''

c = rpl(c,
    "  games_baujahr_mc:()=>genGamesBaujahrMC(),",
    "  games_baujahr_mc:()=>genGamesBaujahrMC(),\n" + NEW_DISPATCH,
    "dispatch konsolen")

# 4h. i18n EN
EN_STRINGS = '''"Welche Konsole hat mehr Einheiten verkauft?":"Which console sold more units?","Welche Konsole war beim Launch teurer?":"Which console had the higher launch price?","Welches Unternehmen hat diese Konsole hergestellt?":"Which company manufactured this console?","Welches Medium nutzt diese Konsole?":"Which storage medium does this console use?","Heimkonsole oder Handheld?":"Home console or handheld?","Handheld":"Handheld","Heimkonsole":"Home console",'''

c = rpl(c,
    '"en":{"Welches Land ist größer?"',
    '"en":{' + EN_STRINGS + '"Welches Land ist größer?"',
    "i18n EN konsolen")

# 4i. i18n PL
PL_STRINGS = '''"Welche Konsole hat mehr Einheiten verkauft?":"Która konsola sprzedała się w większej liczbie egzemplarzy?","Welche Konsole war beim Launch teurer?":"Która konsola była droższa w dniu premiery?","Welches Unternehmen hat diese Konsole hergestellt?":"Które przedsiębiorstwo wyprodukowało tę konsolę?","Welches Medium nutzt diese Konsole?":"Jakiego nośnika używa ta konsola?","Heimkonsole oder Handheld?":"Konsola domowa czy przenośna?","Handheld":"Przenośna","Heimkonsole":"Domowa",'''

c = rpl(c,
    '"pl":{"Auf welchem Kontinent',
    '"pl":{' + PL_STRINGS + '"Auf welchem Kontinent',
    "i18n PL konsolen")

# 4j. Replace-Chain
c = rpl(c,
    ".replace('PLACEHOLDER_GAMES_EXT',",
    ".replace('PLACEHOLDER_KONSOLEN',         KONSOLEN_J)\n  .replace('PLACEHOLDER_GAMES_EXT',",
    "replace chain konsolen")

w(gen_path, c)
print("✅ gen.py aktualisiert (9 Patches, alle Anchors eindeutig)")
print("\n🎉 Phase 411 Patch abgeschlossen!")
print("   Nächste Schritte:")
print("   1. python3 gen.py")
print("   2. python3 verify.py")
print("   3. python3 validate_content.py")
print("   4. python3 check_session.py")
