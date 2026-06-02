#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Expandiert alle extended-JSONs auf mind. 80 Eintraege.
EU-Schwerpunkt + globale Vielfalt. Idempotent.
Betroffene Dateien:
  kunst_extended.json     71 → 80  (+9)
  hunde_extended.json     79 → 80  (+1)
  musik_extended.json     46 → 80  (+34)
  webkultur_extended.json 52 → 80  (+28)
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def expand(filename, new_entries):
    path = os.path.join(ROOT, 'data', filename)
    d = json.load(open(path, encoding='utf-8'))
    added = 0
    for key, val in new_entries.items():
        if key not in d:
            d[key] = val
            added += 1
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('  %s: %d Eintraege (%d neu)' % (filename, len(d), added))

# ─────────────────────────────────────────────────────────────────────────────
# 1. KUNST  (+9, EU + Global)
# ─────────────────────────────────────────────────────────────────────────────
K = "Gemälde"; S = "Skulptur"; I = "Installation"

KUNST_NEW = {
    # EU — Hermitage / Russland (historisch EU-nah)
    "Die Heilige Familie (Raffael)": {
        "kategorie": K, "entstehungsjahr": 1507, "schaetzwert_mio_usd": None,
        "kuenstler": "Raffael", "epoche": "Renaissance",
        "standort_museum": "Hermitage, Sankt Petersburg"},
    # EU — Alte Pinakothek München
    "Selbstporträt (Dürer, 1500)": {
        "kategorie": K, "entstehungsjahr": 1500, "schaetzwert_mio_usd": None,
        "kuenstler": "Albrecht Dürer", "epoche": "Renaissance",
        "standort_museum": "Alte Pinakothek, München"},
    # EU — Nationalgalerie London
    "Die Botschafter": {
        "kategorie": K, "entstehungsjahr": 1533, "schaetzwert_mio_usd": None,
        "kuenstler": "Hans Holbein d. J.", "epoche": "Renaissance",
        "standort_museum": "National Gallery, London"},
    "Sonnenblumen (Van Gogh)": {
        "kategorie": K, "entstehungsjahr": 1888, "schaetzwert_mio_usd": None,
        "kuenstler": "Vincent van Gogh", "epoche": "Post-Impressionismus",
        "standort_museum": "National Gallery, London"},
    # EU — Städel Frankfurt
    "Flügelaltar (Elsheimer)": {
        "kategorie": K, "entstehungsjahr": 1610, "schaetzwert_mio_usd": None,
        "kuenstler": "Adam Elsheimer", "epoche": "Frühbarock",
        "standort_museum": "Städel Museum, Frankfurt"},
    # EU — Österreich
    "Beethoven-Fries": {
        "kategorie": I, "entstehungsjahr": 1902, "schaetzwert_mio_usd": None,
        "kuenstler": "Gustav Klimt", "epoche": "Jugendstil",
        "standort_museum": "Secession, Wien"},
    # Global — Asien
    "Dreiunddreißig Ansichten des Fuji": {
        "kategorie": K, "entstehungsjahr": 1835, "schaetzwert_mio_usd": None,
        "kuenstler": "Katsushika Hokusai", "epoche": "Ukiyo-e",
        "standort_museum": "Nationalmuseum, Tokio"},
    # Global — Lateinamerika
    "Der verwundete Hirsch": {
        "kategorie": K, "entstehungsjahr": 1946, "schaetzwert_mio_usd": None,
        "kuenstler": "Frida Kahlo", "epoche": "Surrealismus",
        "standort_museum": "Museo de Arte Moderno, Mexiko-Stadt"},
    # Global — USA Moderne
    "No. 61 (Rust and Blue)": {
        "kategorie": K, "entstehungsjahr": 1953, "schaetzwert_mio_usd": 46.5,
        "kuenstler": "Mark Rothko", "epoche": "Abstrakter Expressionismus",
        "standort_museum": "Museum of Contemporary Art, Los Angeles"},
}

# ─────────────────────────────────────────────────────────────────────────────
# 2. HUNDE  (+1, Asien/Ozeanien)
# ─────────────────────────────────────────────────────────────────────────────
HUNDE_NEW = {
    "Australian Cattle Dog": {
        "kategorie": "Hütehund", "max_gewicht_kg": 22.0,
        "lebenserwartung_jahre": 14, "widerristhoehe_cm": 51,
        "ursprungsland": "Australien", "fci_gruppe": 1},
}

# ─────────────────────────────────────────────────────────────────────────────
# 3. MUSIK  (+34, EU-Schwerpunkt + Global)
# ─────────────────────────────────────────────────────────────────────────────
# Schema: kategorie, gruendungsjahr, streams_mrd, verkaeufe_mio,
#         herkunftsland, grammys, groesster_hit
MUSIK_NEW = {
    # EU — Deutschland
    "Rammstein":         {"kategorie": "Rock",       "gruendungsjahr": 1994, "streams_mrd": 4.2, "verkaeufe_mio": 20.0,  "herkunftsland": "Deutschland",           "grammys": 0, "groesster_hit": "Du Hast"},
    "Kraftwerk":         {"kategorie": "Electronic", "gruendungsjahr": 1970, "streams_mrd": 1.8, "verkaeufe_mio": 15.0,  "herkunftsland": "Deutschland",           "grammys": 1, "groesster_hit": "Autobahn"},
    "Scorpions":         {"kategorie": "Rock",       "gruendungsjahr": 1965, "streams_mrd": 3.1, "verkaeufe_mio": 110.0, "herkunftsland": "Deutschland",           "grammys": 0, "groesster_hit": "Wind of Change"},
    "Herbert Grönemeyer": {"kategorie": "Pop",       "gruendungsjahr": 1979, "streams_mrd": 0.8, "verkaeufe_mio": 14.0,  "herkunftsland": "Deutschland",           "grammys": 0, "groesster_hit": "Männer"},
    # EU — Frankreich
    "Daft Punk":         {"kategorie": "Electronic", "gruendungsjahr": 1993, "streams_mrd": 7.2, "verkaeufe_mio": 12.0,  "herkunftsland": "Frankreich",            "grammys": 6, "groesster_hit": "Get Lucky"},
    "David Guetta":      {"kategorie": "Electronic", "gruendungsjahr": 2001, "streams_mrd": 9.0, "verkaeufe_mio": 10.0,  "herkunftsland": "Frankreich",            "grammys": 2, "groesster_hit": "Titanium"},
    "Stromae":           {"kategorie": "Electronic", "gruendungsjahr": 2009, "streams_mrd": 3.5, "verkaeufe_mio": 3.0,   "herkunftsland": "Belgien",               "grammys": 0, "groesster_hit": "Papaoutai"},
    # EU — Skandinavien
    "ABBA":              {"kategorie": "Pop",        "gruendungsjahr": 1972, "streams_mrd": 6.0, "verkaeufe_mio": 385.0, "herkunftsland": "Schweden",              "grammys": 0, "groesster_hit": "Dancing Queen"},
    "Roxette":           {"kategorie": "Pop",        "gruendungsjahr": 1986, "streams_mrd": 2.8, "verkaeufe_mio": 75.0,  "herkunftsland": "Schweden",              "grammys": 0, "groesster_hit": "It Must Have Been Love"},
    "Robyn":             {"kategorie": "Pop",        "gruendungsjahr": 1995, "streams_mrd": 2.1, "verkaeufe_mio": 4.0,   "herkunftsland": "Schweden",              "grammys": 0, "groesster_hit": "Dancing On My Own"},
    "Aurora":            {"kategorie": "Pop",        "gruendungsjahr": 2012, "streams_mrd": 1.4, "verkaeufe_mio": 1.0,   "herkunftsland": "Norwegen",              "grammys": 0, "groesster_hit": "Runaway"},
    "Sigur Rós":         {"kategorie": "Rock",       "gruendungsjahr": 1994, "streams_mrd": 0.9, "verkaeufe_mio": 2.0,   "herkunftsland": "Island",                "grammys": 0, "groesster_hit": "Hoppípolla"},
    # EU — UK (mehr)
    "Radiohead":         {"kategorie": "Rock",       "gruendungsjahr": 1985, "streams_mrd": 5.5, "verkaeufe_mio": 30.0,  "herkunftsland": "Vereinigtes Königreich", "grammys": 4, "groesster_hit": "Creep"},
    "Coldplay":          {"kategorie": "Rock",       "gruendungsjahr": 1996, "streams_mrd": 15.0,"verkaeufe_mio": 100.0, "herkunftsland": "Vereinigtes Königreich", "grammys": 9, "groesster_hit": "Yellow"},
    "Amy Winehouse":     {"kategorie": "Pop",        "gruendungsjahr": 2003, "streams_mrd": 4.8, "verkaeufe_mio": 20.0,  "herkunftsland": "Vereinigtes Königreich", "grammys": 5, "groesster_hit": "Rehab"},
    "Dua Lipa":          {"kategorie": "Pop",        "gruendungsjahr": 2015, "streams_mrd": 12.0,"verkaeufe_mio": 5.0,   "herkunftsland": "Vereinigtes Königreich", "grammys": 3, "groesster_hit": "Levitating"},
    # EU — Sonstige
    "U2":                {"kategorie": "Rock",       "gruendungsjahr": 1976, "streams_mrd": 6.2, "verkaeufe_mio": 170.0, "herkunftsland": "Irland",                "grammys": 22, "groesster_hit": "One"},
    "Stromae":           {"kategorie": "Electronic", "gruendungsjahr": 2009, "streams_mrd": 3.5, "verkaeufe_mio": 3.0,   "herkunftsland": "Belgien",               "grammys": 0, "groesster_hit": "Alors on Danse"},
    # Global — USA (mehr Vielfalt)
    "Beyoncé":           {"kategorie": "Pop",        "gruendungsjahr": 1997, "streams_mrd": 18.0,"verkaeufe_mio": 200.0, "herkunftsland": "Vereinigte Staaten",    "grammys": 32, "groesster_hit": "Crazy in Love"},
    "Taylor Swift":      {"kategorie": "Pop",        "gruendungsjahr": 2004, "streams_mrd": 26.0,"verkaeufe_mio": 200.0, "herkunftsland": "Vereinigte Staaten",    "grammys": 14, "groesster_hit": "Shake It Off"},
    "Kendrick Lamar":    {"kategorie": "Hip-Hop",    "gruendungsjahr": 2003, "streams_mrd": 14.0,"verkaeufe_mio": 8.0,   "herkunftsland": "Vereinigte Staaten",    "grammys": 17, "groesster_hit": "HUMBLE."},
    "Frank Ocean":       {"kategorie": "Pop",        "gruendungsjahr": 2009, "streams_mrd": 7.5, "verkaeufe_mio": 3.0,   "herkunftsland": "Vereinigte Staaten",    "grammys": 2, "groesster_hit": "Thinking Bout You"},
    # Global — Lateinamerika
    "J Balvin":          {"kategorie": "Pop",        "gruendungsjahr": 2004, "streams_mrd": 14.0,"verkaeufe_mio": 3.0,   "herkunftsland": "Kolumbien",             "grammys": 0, "groesster_hit": "Mi Gente"},
    "Bad Bunny":         {"kategorie": "Hip-Hop",    "gruendungsjahr": 2016, "streams_mrd": 20.0,"verkaeufe_mio": 2.0,   "herkunftsland": "Puerto Rico",           "grammys": 0, "groesster_hit": "Tití Me Preguntó"},
    "Shakira":           {"kategorie": "Pop",        "gruendungsjahr": 1991, "streams_mrd": 11.0,"verkaeufe_mio": 80.0,  "herkunftsland": "Kolumbien",             "grammys": 3, "groesster_hit": "Hips Don't Lie"},
    # Global — Asien / Afrika
    "BTS":               {"kategorie": "Pop",        "gruendungsjahr": 2013, "streams_mrd": 16.0,"verkaeufe_mio": 20.0,  "herkunftsland": "Südkorea",              "grammys": 0, "groesster_hit": "Dynamite"},
    "BLACKPINK":         {"kategorie": "Pop",        "gruendungsjahr": 2016, "streams_mrd": 10.0,"verkaeufe_mio": 5.0,   "herkunftsland": "Südkorea",              "grammys": 0, "groesster_hit": "How You Like That"},
    "Burna Boy":         {"kategorie": "Pop",        "gruendungsjahr": 2010, "streams_mrd": 5.0, "verkaeufe_mio": 2.0,   "herkunftsland": "Nigeria",               "grammys": 1, "groesster_hit": "Last Last"},
    "Wizkid":            {"kategorie": "Pop",        "gruendungsjahr": 2009, "streams_mrd": 6.0, "verkaeufe_mio": 2.0,   "herkunftsland": "Nigeria",               "grammys": 1, "groesster_hit": "Essence"},
    "Rosalía":           {"kategorie": "Pop",        "gruendungsjahr": 2017, "streams_mrd": 5.5, "verkaeufe_mio": 1.0,   "herkunftsland": "Spanien",               "grammys": 3, "groesster_hit": "DESPECHÁ"},
    "Anitta":            {"kategorie": "Pop",        "gruendungsjahr": 2010, "streams_mrd": 4.0, "verkaeufe_mio": 1.0,   "herkunftsland": "Brasilien",             "grammys": 0, "groesster_hit": "Envolver"},
}

# ─────────────────────────────────────────────────────────────────────────────
# 4. WEBKULTUR  (+28, EU-Schwerpunkt + Global)
# ─────────────────────────────────────────────────────────────────────────────
# Schema: kategorie, start_jahr, reichweite_mio, ursprungsland, gruender_creator
P = "Plattform"; C = "Creator"; M = "Meme"; HW = "Hardware"

WEBKULTUR_NEW = {
    # EU — Plattformen
    "Spotify":           {"kategorie": P,  "start_jahr": 2006, "reichweite_mio": 600.0,  "ursprungsland": "Schweden",           "gruender_creator": "Daniel Ek"},
    "Skype":             {"kategorie": P,  "start_jahr": 2003, "reichweite_mio": 300.0,  "ursprungsland": "Estland",            "gruender_creator": "Niklas Zennström"},
    "TransferWise (Wise)": {"kategorie": P,"start_jahr": 2011, "reichweite_mio": 16.0,   "ursprungsland": "Estland",            "gruender_creator": "Taavet Hinrikus"},
    "Booking.com":       {"kategorie": P,  "start_jahr": 1996, "reichweite_mio": 500.0,  "ursprungsland": "Niederlande",        "gruender_creator": "Geert-Jan Bruinsma"},
    "Deezer":            {"kategorie": P,  "start_jahr": 2007, "reichweite_mio": 16.0,   "ursprungsland": "Frankreich",         "gruender_creator": "Daniel Marhely"},
    "Dailymotion":       {"kategorie": P,  "start_jahr": 2005, "reichweite_mio": 300.0,  "ursprungsland": "Frankreich",         "gruender_creator": "Benjamin Bejbaum"},
    "XING":              {"kategorie": P,  "start_jahr": 2003, "reichweite_mio": 22.0,   "ursprungsland": "Deutschland",        "gruender_creator": "Lars Hinrichs"},
    "Zalando":           {"kategorie": P,  "start_jahr": 2008, "reichweite_mio": 50.0,   "ursprungsland": "Deutschland",        "gruender_creator": "Robert Gentz"},
    "Shazam":            {"kategorie": P,  "start_jahr": 2002, "reichweite_mio": 200.0,  "ursprungsland": "Vereinigtes Königreich", "gruender_creator": "Chris Barton"},
    "SoundCloud":        {"kategorie": P,  "start_jahr": 2007, "reichweite_mio": 175.0,  "ursprungsland": "Deutschland",        "gruender_creator": "Alexander Ljung"},
    # EU — Creator
    "PewDiePie":         {"kategorie": C,  "start_jahr": 2010, "reichweite_mio": 111.0,  "ursprungsland": "Schweden",           "gruender_creator": "Felix Kjellberg"},
    "KSI":               {"kategorie": C,  "start_jahr": 2009, "reichweite_mio": 24.0,   "ursprungsland": "Vereinigtes Königreich", "gruender_creator": "Olajide Olatunji"},
    "Markiplier":        {"kategorie": C,  "start_jahr": 2012, "reichweite_mio": 35.0,   "ursprungsland": "Vereinigte Staaten", "gruender_creator": "Mark Fischbach"},
    "Kurzgesagt":        {"kategorie": C,  "start_jahr": 2013, "reichweite_mio": 22.0,   "ursprungsland": "Deutschland",        "gruender_creator": "Philipp Dettmer"},
    "EinfachManny":      {"kategorie": C,  "start_jahr": 2014, "reichweite_mio": 3.5,    "ursprungsland": "Deutschland",        "gruender_creator": "Manuel Hamann"},
    # Global — Plattformen
    "WeChat":            {"kategorie": P,  "start_jahr": 2011, "reichweite_mio": 1350.0, "ursprungsland": "China",              "gruender_creator": "Zhang Xiaolong"},
    "LINE":              {"kategorie": P,  "start_jahr": 2011, "reichweite_mio": 178.0,  "ursprungsland": "Japan",              "gruender_creator": "Naver Corporation"},
    "KakaoTalk":         {"kategorie": P,  "start_jahr": 2010, "reichweite_mio": 53.0,   "ursprungsland": "Südkorea",           "gruender_creator": "Kim Beom-su"},
    "Mercado Libre":     {"kategorie": P,  "start_jahr": 1999, "reichweite_mio": 100.0,  "ursprungsland": "Argentinien",        "gruender_creator": "Marcos Galperin"},
    "Flipkart":          {"kategorie": P,  "start_jahr": 2007, "reichweite_mio": 150.0,  "ursprungsland": "Indien",             "gruender_creator": "Sachin Bansal"},
    "Baidu":             {"kategorie": P,  "start_jahr": 2000, "reichweite_mio": 1000.0, "ursprungsland": "China",              "gruender_creator": "Robin Li"},
    # Global — Creator
    "MrBeast":           {"kategorie": C,  "start_jahr": 2012, "reichweite_mio": 300.0,  "ursprungsland": "Vereinigte Staaten", "gruender_creator": "Jimmy Donaldson"},
    "T-Series":          {"kategorie": C,  "start_jahr": 2006, "reichweite_mio": 270.0,  "ursprungsland": "Indien",             "gruender_creator": "Bhushan Kumar"},
    "Cocomelon":         {"kategorie": C,  "start_jahr": 2006, "reichweite_mio": 175.0,  "ursprungsland": "Vereinigte Staaten", "gruender_creator": "Jay Jeon"},
    # Global — Meme/Kultur
    "Harlem Shake":      {"kategorie": M,  "start_jahr": 2013, "reichweite_mio": 500.0,  "ursprungsland": "Vereinigte Staaten", "gruender_creator": "Baauer / Filayyyy"},
    "Ice Bucket Challenge": {"kategorie": M,"start_jahr": 2014,"reichweite_mio": 400.0,  "ursprungsland": "Vereinigte Staaten", "gruender_creator": "Pete Frates"},
    # Global — Hardware
    "Raspberry Pi":      {"kategorie": HW, "start_jahr": 2012, "reichweite_mio": 50.0,   "ursprungsland": "Vereinigtes Königreich", "gruender_creator": "Eben Upton"},
    "Fairphone":         {"kategorie": HW, "start_jahr": 2013, "reichweite_mio": 2.0,    "ursprungsland": "Niederlande",        "gruender_creator": "Bas van Abel"},
}

print('\n== Expandiere alle extended-JSONs auf mind. 80 ==\n')
expand('kunst_extended.json',     KUNST_NEW)
expand('hunde_extended.json',     HUNDE_NEW)
expand('musik_extended.json',     MUSIK_NEW)
expand('webkultur_extended.json', WEBKULTUR_NEW)
print('\nFertig! Jetzt validate_content.py ausfuehren.')
