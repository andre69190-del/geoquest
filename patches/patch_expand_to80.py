#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Expandiert kunst_extended.json (54→80), hunde_extended.json (40→80)
und gartenbau_extended.json (40→80). EU-Schwerpunkt + globale Highlights.
Idempotent: Vorhandene Keys werden übersprungen.
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
    print(f'  {filename}: {len(d)} Einträge ({added} neu hinzugefügt)')

# ─────────────────────────────────────────────────────────────────────────────
# 1. KUNST  (54 → 80, +26)
# ─────────────────────────────────────────────────────────────────────────────
# Schema: kategorie, entstehungsjahr, schaetzwert_mio_usd, kuenstler, epoche, standort_museum
K = "Gemälde"; S = "Skulptur"; I = "Installation"

KUNST_NEW = {
    # EU — Prado, Madrid
    "Las Meninas": {
        "kategorie": K, "entstehungsjahr": 1656, "schaetzwert_mio_usd": None,
        "kuenstler": "Diego Velázquez", "epoche": "Barock",
        "standort_museum": "Prado, Madrid"},
    "Der Garten der Lüste": {
        "kategorie": K, "entstehungsjahr": 1510, "schaetzwert_mio_usd": None,
        "kuenstler": "Hieronymus Bosch", "epoche": "Spätgotik",
        "standort_museum": "Prado, Madrid"},
    "Saturnus verschlingt seinen Sohn": {
        "kategorie": K, "entstehungsjahr": 1823, "schaetzwert_mio_usd": None,
        "kuenstler": "Francisco de Goya", "epoche": "Romantik",
        "standort_museum": "Prado, Madrid"},
    "Die drei Grazien": {
        "kategorie": K, "entstehungsjahr": 1635, "schaetzwert_mio_usd": None,
        "kuenstler": "Peter Paul Rubens", "epoche": "Barock",
        "standort_museum": "Prado, Madrid"},
    # EU — Uffizien, Florenz
    "Die Geburt der Venus": {
        "kategorie": K, "entstehungsjahr": 1485, "schaetzwert_mio_usd": None,
        "kuenstler": "Sandro Botticelli", "epoche": "Renaissance",
        "standort_museum": "Uffizien, Florenz"},
    "Der Frühling": {
        "kategorie": K, "entstehungsjahr": 1482, "schaetzwert_mio_usd": None,
        "kuenstler": "Sandro Botticelli", "epoche": "Renaissance",
        "standort_museum": "Uffizien, Florenz"},
    "Judith mit dem Haupt des Holofernes": {
        "kategorie": K, "entstehungsjahr": 1620, "schaetzwert_mio_usd": None,
        "kuenstler": "Artemisia Gentileschi", "epoche": "Barock",
        "standort_museum": "Uffizien, Florenz"},
    # EU — Rijksmuseum, Amsterdam
    "Das Milchmädchen": {
        "kategorie": K, "entstehungsjahr": 1658, "schaetzwert_mio_usd": None,
        "kuenstler": "Johannes Vermeer", "epoche": "Barock",
        "standort_museum": "Rijksmuseum, Amsterdam"},
    "Die Nachtwache": {
        "kategorie": K, "entstehungsjahr": 1642, "schaetzwert_mio_usd": None,
        "kuenstler": "Rembrandt van Rijn", "epoche": "Barock",
        "standort_museum": "Rijksmuseum, Amsterdam"},
    # EU — Musée d'Orsay / Marmottan, Paris
    "Olympia": {
        "kategorie": K, "entstehungsjahr": 1863, "schaetzwert_mio_usd": None,
        "kuenstler": "Édouard Manet", "epoche": "Realismus",
        "standort_museum": "Musée d'Orsay, Paris"},
    "Die Ballettklasse": {
        "kategorie": K, "entstehungsjahr": 1874, "schaetzwert_mio_usd": None,
        "kuenstler": "Edgar Degas", "epoche": "Impressionismus",
        "standort_museum": "Musée d'Orsay, Paris"},
    "Impression, Sonnenaufgang": {
        "kategorie": K, "entstehungsjahr": 1872, "schaetzwert_mio_usd": None,
        "kuenstler": "Claude Monet", "epoche": "Impressionismus",
        "standort_museum": "Musée Marmottan Monet, Paris"},
    # EU — Österreich / Wien
    "Der Kuss": {
        "kategorie": K, "entstehungsjahr": 1907, "schaetzwert_mio_usd": 200.0,
        "kuenstler": "Gustav Klimt", "epoche": "Jugendstil",
        "standort_museum": "Österreichische Galerie Belvedere, Wien"},
    # EU — Italien / Vatikan / Florenz
    "David": {
        "kategorie": S, "entstehungsjahr": 1504, "schaetzwert_mio_usd": None,
        "kuenstler": "Michelangelo Buonarroti", "epoche": "Renaissance",
        "standort_museum": "Galleria dell'Accademia, Florenz"},
    "Die Schule von Athen": {
        "kategorie": K, "entstehungsjahr": 1511, "schaetzwert_mio_usd": None,
        "kuenstler": "Raffael", "epoche": "Renaissance",
        "standort_museum": "Vatikanische Museen, Rom"},
    # EU — Deutschland
    "Isenheimer Altar": {
        "kategorie": K, "entstehungsjahr": 1516, "schaetzwert_mio_usd": None,
        "kuenstler": "Matthias Grünewald", "epoche": "Renaissance",
        "standort_museum": "Musée d'Unterlinden, Colmar"},
    "Der Sämann": {
        "kategorie": K, "entstehungsjahr": 1888, "schaetzwert_mio_usd": None,
        "kuenstler": "Vincent van Gogh", "epoche": "Post-Impressionismus",
        "standort_museum": "Kröller-Müller Museum, Otterlo"},
    # EU — Polen
    "Porträt eines jungen Mannes (Raffael)": {
        "kategorie": K, "entstehungsjahr": 1514, "schaetzwert_mio_usd": None,
        "kuenstler": "Raffael", "epoche": "Renaissance",
        "standort_museum": "Nationalmuseum, Warschau"},
    "Dame mit dem Hermelin": {
        "kategorie": K, "entstehungsjahr": 1490, "schaetzwert_mio_usd": None,
        "kuenstler": "Leonardo da Vinci", "epoche": "Renaissance",
        "standort_museum": "Czartoryski-Museum, Krakau"},
    # Global — MoMA New York
    "Les Demoiselles d'Avignon": {
        "kategorie": K, "entstehungsjahr": 1907, "schaetzwert_mio_usd": None,
        "kuenstler": "Pablo Picasso", "epoche": "Kubismus",
        "standort_museum": "MoMA, New York"},
    "Die Beständigkeit der Erinnerung": {
        "kategorie": K, "entstehungsjahr": 1931, "schaetzwert_mio_usd": None,
        "kuenstler": "Salvador Dalí", "epoche": "Surrealismus",
        "standort_museum": "MoMA, New York"},
    "Campbell's Soup Cans": {
        "kategorie": I, "entstehungsjahr": 1962, "schaetzwert_mio_usd": None,
        "kuenstler": "Andy Warhol", "epoche": "Pop-Art",
        "standort_museum": "MoMA, New York"},
    # Global — Amerika
    "American Gothic": {
        "kategorie": K, "entstehungsjahr": 1930, "schaetzwert_mio_usd": None,
        "kuenstler": "Grant Wood", "epoche": "Regionalismus",
        "standort_museum": "Art Institute of Chicago"},
    "Die große Welle vor Kanagawa": {
        "kategorie": K, "entstehungsjahr": 1831, "schaetzwert_mio_usd": None,
        "kuenstler": "Katsushika Hokusai", "epoche": "Ukiyo-e",
        "standort_museum": "Metropolitan Museum, New York"},
    # Global — Lateinamerika / Sonstige
    "Selbstporträt mit Dornenhalskette": {
        "kategorie": K, "entstehungsjahr": 1940, "schaetzwert_mio_usd": 34.9,
        "kuenstler": "Frida Kahlo", "epoche": "Surrealismus",
        "standort_museum": "Harry Ransom Center, Austin"},
    "Balloon Dog (Orange)": {
        "kategorie": S, "entstehungsjahr": 1994, "schaetzwert_mio_usd": 58.4,
        "kuenstler": "Jeff Koons", "epoche": "Post-Moderne",
        "standort_museum": "Verschiedene Privatsammlungen"},
}

# ─────────────────────────────────────────────────────────────────────────────
# 2. HUNDE  (40 → 80, +40)
# ─────────────────────────────────────────────────────────────────────────────
# Schema: kategorie, max_gewicht_kg, lebenserwartung_jahre, widerristhoehe_cm,
#         ursprungsland, fci_gruppe
H = "Hütehund"; B = "Begleithund"; J = "Jagdhund"; T = "Terrier"; M = "Molosser"

HUNDE_NEW = {
    # EU — Deutschland / DACH
    "Hovawart":          {H: H, "max_gewicht_kg": 45.0, "lebenserwartung_jahre": 12, "widerristhoehe_cm": 70, "ursprungsland": "Deutschland",  "fci_gruppe": 2},
    "Eurasier":          {"kategorie": B, "max_gewicht_kg": 26.0, "lebenserwartung_jahre": 13, "widerristhoehe_cm": 60, "ursprungsland": "Deutschland",  "fci_gruppe": 5},
    "Mittelspitz":       {"kategorie": B, "max_gewicht_kg": 11.0, "lebenserwartung_jahre": 14, "widerristhoehe_cm": 38, "ursprungsland": "Deutschland",  "fci_gruppe": 5},
    "Berner Sennenhund": {"kategorie": M, "max_gewicht_kg": 52.0, "lebenserwartung_jahre":  8, "widerristhoehe_cm": 70, "ursprungsland": "Schweiz",      "fci_gruppe": 2},
    "Grosser Schweizer Sennenhund": {"kategorie": M, "max_gewicht_kg": 60.0, "lebenserwartung_jahre": 9, "widerristhoehe_cm": 72, "ursprungsland": "Schweiz", "fci_gruppe": 2},
    "Appenzeller Sennenhund": {"kategorie": H, "max_gewicht_kg": 25.0, "lebenserwartung_jahre": 13, "widerristhoehe_cm": 56, "ursprungsland": "Schweiz", "fci_gruppe": 1},
    "Entlebucher Sennenhund": {"kategorie": H, "max_gewicht_kg": 16.0, "lebenserwartung_jahre": 13, "widerristhoehe_cm": 50, "ursprungsland": "Schweiz", "fci_gruppe": 1},
    # EU — Frankreich / Belgien / Niederlande
    "Briard":            {"kategorie": H, "max_gewicht_kg": 45.0, "lebenserwartung_jahre": 12, "widerristhoehe_cm": 68, "ursprungsland": "Frankreich",   "fci_gruppe": 1},
    "Bouvier des Flandres": {"kategorie": H, "max_gewicht_kg": 40.0, "lebenserwartung_jahre": 12, "widerristhoehe_cm": 68, "ursprungsland": "Belgien",   "fci_gruppe": 1},
    "Pyrenäenberghund":  {"kategorie": M, "max_gewicht_kg": 60.0, "lebenserwartung_jahre": 12, "widerristhoehe_cm": 82, "ursprungsland": "Frankreich",   "fci_gruppe": 2},
    "Barbet":            {"kategorie": J, "max_gewicht_kg": 28.0, "lebenserwartung_jahre": 14, "widerristhoehe_cm": 64, "ursprungsland": "Frankreich",   "fci_gruppe": 8},
    "Basset Hound":      {"kategorie": J, "max_gewicht_kg": 35.0, "lebenserwartung_jahre": 12, "widerristhoehe_cm": 38, "ursprungsland": "Frankreich",   "fci_gruppe": 6},
    "Bloodhound":        {"kategorie": J, "max_gewicht_kg": 50.0, "lebenserwartung_jahre": 11, "widerristhoehe_cm": 69, "ursprungsland": "Belgien",      "fci_gruppe": 6},
    # EU — Grossbritannien / Irland
    "Irish Setter":      {"kategorie": J, "max_gewicht_kg": 32.0, "lebenserwartung_jahre": 13, "widerristhoehe_cm": 67, "ursprungsland": "Irland",       "fci_gruppe": 7},
    "Gordon Setter":     {"kategorie": J, "max_gewicht_kg": 36.0, "lebenserwartung_jahre": 12, "widerristhoehe_cm": 69, "ursprungsland": "Schottland",   "fci_gruppe": 7},
    "English Setter":    {"kategorie": J, "max_gewicht_kg": 36.0, "lebenserwartung_jahre": 12, "widerristhoehe_cm": 69, "ursprungsland": "Grossbritannien","fci_gruppe": 7},
    "Cocker Spaniel":    {"kategorie": J, "max_gewicht_kg": 13.0, "lebenserwartung_jahre": 14, "widerristhoehe_cm": 40, "ursprungsland": "Grossbritannien","fci_gruppe": 8},
    "English Springer Spaniel": {"kategorie": J, "max_gewicht_kg": 23.0, "lebenserwartung_jahre": 13, "widerristhoehe_cm": 51, "ursprungsland": "Grossbritannien", "fci_gruppe": 8},
    "Airedale Terrier":  {"kategorie": T, "max_gewicht_kg": 29.0, "lebenserwartung_jahre": 13, "widerristhoehe_cm": 61, "ursprungsland": "Grossbritannien","fci_gruppe": 3},
    "West Highland White Terrier": {"kategorie": T, "max_gewicht_kg": 10.0, "lebenserwartung_jahre": 14, "widerristhoehe_cm": 28, "ursprungsland": "Schottland", "fci_gruppe": 3},
    # EU — Ungarn / Osteuropa
    "Vizsla":            {"kategorie": J, "max_gewicht_kg": 30.0, "lebenserwartung_jahre": 13, "widerristhoehe_cm": 64, "ursprungsland": "Ungarn",       "fci_gruppe": 7},
    "Komondor":          {"kategorie": H, "max_gewicht_kg": 60.0, "lebenserwartung_jahre": 11, "widerristhoehe_cm": 80, "ursprungsland": "Ungarn",       "fci_gruppe": 1},
    "Puli":              {"kategorie": H, "max_gewicht_kg": 16.0, "lebenserwartung_jahre": 14, "widerristhoehe_cm": 45, "ursprungsland": "Ungarn",       "fci_gruppe": 1},
    "Kuvasz":            {"kategorie": H, "max_gewicht_kg": 52.0, "lebenserwartung_jahre": 12, "widerristhoehe_cm": 75, "ursprungsland": "Ungarn",       "fci_gruppe": 1},
    "Mudi":              {"kategorie": H, "max_gewicht_kg": 13.0, "lebenserwartung_jahre": 14, "widerristhoehe_cm": 47, "ursprungsland": "Ungarn",       "fci_gruppe": 1},
    # EU — Italien
    "Cane Corso":        {"kategorie": M, "max_gewicht_kg": 50.0, "lebenserwartung_jahre": 11, "widerristhoehe_cm": 70, "ursprungsland": "Italien",      "fci_gruppe": 2},
    "Neapolitanischer Mastiff": {"kategorie": M, "max_gewicht_kg": 70.0, "lebenserwartung_jahre":  9, "widerristhoehe_cm": 75, "ursprungsland": "Italien", "fci_gruppe": 2},
    "Lagotto Romagnolo": {"kategorie": J, "max_gewicht_kg": 16.0, "lebenserwartung_jahre": 17, "widerristhoehe_cm": 48, "ursprungsland": "Italien",      "fci_gruppe": 8},
    "Spinone Italiano":  {"kategorie": J, "max_gewicht_kg": 40.0, "lebenserwartung_jahre": 13, "widerristhoehe_cm": 70, "ursprungsland": "Italien",      "fci_gruppe": 7},
    # EU — Skandinavien
    "Finnischer Spitz":  {"kategorie": J, "max_gewicht_kg": 13.0, "lebenserwartung_jahre": 14, "widerristhoehe_cm": 50, "ursprungsland": "Finnland",     "fci_gruppe": 5},
    "Isländischer Schäferhund": {"kategorie": H, "max_gewicht_kg": 14.0, "lebenserwartung_jahre": 14, "widerristhoehe_cm": 46, "ursprungsland": "Island", "fci_gruppe": 5},
    # Global — Asien
    "Tibetischer Mastiff": {"kategorie": M, "max_gewicht_kg": 82.0, "lebenserwartung_jahre": 12, "widerristhoehe_cm": 80, "ursprungsland": "Tibet",      "fci_gruppe": 2},
    "Chow-Chow":         {"kategorie": M, "max_gewicht_kg": 32.0, "lebenserwartung_jahre": 12, "widerristhoehe_cm": 56, "ursprungsland": "China",        "fci_gruppe": 5},
    "Chinesischer Schopfhund": {"kategorie": B, "max_gewicht_kg": 5.5, "lebenserwartung_jahre": 15, "widerristhoehe_cm": 33, "ursprungsland": "China",   "fci_gruppe": 9},
    "Kangal":            {"kategorie": M, "max_gewicht_kg": 65.0, "lebenserwartung_jahre": 13, "widerristhoehe_cm": 81, "ursprungsland": "Türkei",       "fci_gruppe": 2},
    "Afghan Hound":      {"kategorie": J, "max_gewicht_kg": 27.0, "lebenserwartung_jahre": 14, "widerristhoehe_cm": 74, "ursprungsland": "Afghanistan",  "fci_gruppe": 10},
    "Saluki":            {"kategorie": J, "max_gewicht_kg": 30.0, "lebenserwartung_jahre": 14, "widerristhoehe_cm": 71, "ursprungsland": "Orient",       "fci_gruppe": 10},
    # Global — Afrika / Amerika
    "Dogo Argentino":    {"kategorie": M, "max_gewicht_kg": 50.0, "lebenserwartung_jahre": 12, "widerristhoehe_cm": 68, "ursprungsland": "Argentinien",  "fci_gruppe": 2},
    "Xoloitzcuintle":    {"kategorie": B, "max_gewicht_kg": 14.0, "lebenserwartung_jahre": 13, "widerristhoehe_cm": 55, "ursprungsland": "Mexiko",       "fci_gruppe": 5},
    "Boerboel":          {"kategorie": M, "max_gewicht_kg": 80.0, "lebenserwartung_jahre": 11, "widerristhoehe_cm": 70, "ursprungsland": "Südafrika",    "fci_gruppe": 2},
}
# Fix the Hovawart entry (typo: used H as variable for Hütehund but overwrote with kategorie key "H")
HUNDE_NEW["Hovawart"] = {"kategorie": "Hütehund", "max_gewicht_kg": 45.0, "lebenserwartung_jahre": 12, "widerristhoehe_cm": 70, "ursprungsland": "Deutschland", "fci_gruppe": 2}

# ─────────────────────────────────────────────────────────────────────────────
# 3. GARTENBAU  (40 → 80, +40)
# ─────────────────────────────────────────────────────────────────────────────
# Schema: kategorie, max_wuchshoehe_cm, wasserbedarf, bodenanspruch,
#         ursprungsregion, bluetezeit_start_monat
Z = "Zierpflanze"; N = "Nutzpflanze"; BA = "Baum"; ST = "Strauch"

GARTEN_NEW = {
    # Zierpflanzen (EU-nativ & Exoten)
    "Dahlie":          {"kategorie": Z, "max_wuchshoehe_cm": 150, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Mexiko",          "bluetezeit_start_monat": 8},
    "Zinnie":          {"kategorie": Z, "max_wuchshoehe_cm": 100, "wasserbedarf": "Wenig",   "bodenanspruch": "Neutral",   "ursprungsregion": "Mexiko",          "bluetezeit_start_monat": 7},
    "Ringelblume":     {"kategorie": Z, "max_wuchshoehe_cm":  50, "wasserbedarf": "Wenig",   "bodenanspruch": "Neutral",   "ursprungsregion": "Mittelmeer",      "bluetezeit_start_monat": 4},
    "Löwenmäulchen":   {"kategorie": Z, "max_wuchshoehe_cm":  80, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Mittelmeer",      "bluetezeit_start_monat": 4},
    "Petunie":         {"kategorie": Z, "max_wuchshoehe_cm":  40, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Südamerika",      "bluetezeit_start_monat": 5},
    "Begonie":         {"kategorie": Z, "max_wuchshoehe_cm":  50, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Südamerika",      "bluetezeit_start_monat": 6},
    "Gladiole":        {"kategorie": Z, "max_wuchshoehe_cm": 150, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Südafrika",       "bluetezeit_start_monat": 7},
    "Canna":           {"kategorie": Z, "max_wuchshoehe_cm": 200, "wasserbedarf": "Hoch",    "bodenanspruch": "Neutral",   "ursprungsregion": "Amerika",         "bluetezeit_start_monat": 7},
    "Echinacea":       {"kategorie": Z, "max_wuchshoehe_cm": 120, "wasserbedarf": "Wenig",   "bodenanspruch": "Neutral",   "ursprungsregion": "Nordamerika",     "bluetezeit_start_monat": 7},
    "Stauden-Aster":   {"kategorie": Z, "max_wuchshoehe_cm": 150, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Nordamerika",     "bluetezeit_start_monat": 9},
    "Clematis":        {"kategorie": ST,"max_wuchshoehe_cm": 500, "wasserbedarf": "Mittel",  "bodenanspruch": "Alkalisch", "ursprungsregion": "Europa/Asien",    "bluetezeit_start_monat": 5},
    "Passionsblume":   {"kategorie": ST,"max_wuchshoehe_cm":1000, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Südamerika",      "bluetezeit_start_monat": 7},
    "Trompetenblume":  {"kategorie": ST,"max_wuchshoehe_cm":1000, "wasserbedarf": "Wenig",   "bodenanspruch": "Tolerant",  "ursprungsregion": "Nordamerika",     "bluetezeit_start_monat": 7},
    # Nutzpflanzen (EU-Garten)
    "Paprika":         {"kategorie": N, "max_wuchshoehe_cm": 100, "wasserbedarf": "Hoch",    "bodenanspruch": "Neutral",   "ursprungsregion": "Südamerika",      "bluetezeit_start_monat": 7},
    "Aubergine":       {"kategorie": N, "max_wuchshoehe_cm": 120, "wasserbedarf": "Hoch",    "bodenanspruch": "Neutral",   "ursprungsregion": "Indien",          "bluetezeit_start_monat": 7},
    "Blattsalat":      {"kategorie": N, "max_wuchshoehe_cm":  30, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Mittelmeer",      "bluetezeit_start_monat": 3},
    "Spinat":          {"kategorie": N, "max_wuchshoehe_cm":  30, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Südwestasien",    "bluetezeit_start_monat": 3},
    "Stangenbohne":    {"kategorie": N, "max_wuchshoehe_cm": 250, "wasserbedarf": "Hoch",    "bodenanspruch": "Neutral",   "ursprungsregion": "Amerika",         "bluetezeit_start_monat": 6},
    "Erbse":           {"kategorie": N, "max_wuchshoehe_cm": 200, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Naher Osten",     "bluetezeit_start_monat": 5},
    "Kürbis":          {"kategorie": N, "max_wuchshoehe_cm":  40, "wasserbedarf": "Hoch",    "bodenanspruch": "Neutral",   "ursprungsregion": "Amerika",         "bluetezeit_start_monat": 7},
    "Zwiebel":         {"kategorie": N, "max_wuchshoehe_cm":  60, "wasserbedarf": "Wenig",   "bodenanspruch": "Neutral",   "ursprungsregion": "Zentralasien",    "bluetezeit_start_monat": 6},
    "Zitronenmelisse": {"kategorie": N, "max_wuchshoehe_cm":  80, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Südeuropa",       "bluetezeit_start_monat": 6},
    "Basilikum":       {"kategorie": N, "max_wuchshoehe_cm":  50, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Indien",          "bluetezeit_start_monat": 7},
    "Rosmarin":        {"kategorie": N, "max_wuchshoehe_cm": 150, "wasserbedarf": "Wenig",   "bodenanspruch": "Alkalisch", "ursprungsregion": "Mittelmeer",      "bluetezeit_start_monat": 4},
    "Salbei":          {"kategorie": N, "max_wuchshoehe_cm":  80, "wasserbedarf": "Wenig",   "bodenanspruch": "Alkalisch", "ursprungsregion": "Mittelmeer",      "bluetezeit_start_monat": 5},
    "Schnittlauch":    {"kategorie": N, "max_wuchshoehe_cm":  40, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Asien/Europa",    "bluetezeit_start_monat": 6},
    # Bäume (EU-nativ)
    "Birne":           {"kategorie": BA,"max_wuchshoehe_cm":1200, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Europa/Asien",    "bluetezeit_start_monat": 4},
    "Pflaume":         {"kategorie": BA,"max_wuchshoehe_cm": 800, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Europa",          "bluetezeit_start_monat": 4},
    "Pfirsich":        {"kategorie": BA,"max_wuchshoehe_cm": 600, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "China",           "bluetezeit_start_monat": 3},
    "Aprikose":        {"kategorie": BA,"max_wuchshoehe_cm": 600, "wasserbedarf": "Mittel",  "bodenanspruch": "Alkalisch", "ursprungsregion": "Zentralasien",    "bluetezeit_start_monat": 3},
    "Walnuss":         {"kategorie": BA,"max_wuchshoehe_cm":3000, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Zentralasien",    "bluetezeit_start_monat": 4},
    "Rotbuche":        {"kategorie": BA,"max_wuchshoehe_cm":4000, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Europa",          "bluetezeit_start_monat": 4},
    # Sträucher (EU-nativ & Klettergehölze)
    "Holunder":        {"kategorie": ST,"max_wuchshoehe_cm": 700, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Europa",          "bluetezeit_start_monat": 5},
    "Heidekraut":      {"kategorie": ST,"max_wuchshoehe_cm":  60, "wasserbedarf": "Wenig",   "bodenanspruch": "Sauer",     "ursprungsregion": "Europa",          "bluetezeit_start_monat": 8},
    "Weißdorn":        {"kategorie": ST,"max_wuchshoehe_cm":1000, "wasserbedarf": "Wenig",   "bodenanspruch": "Alkalisch", "ursprungsregion": "Europa",          "bluetezeit_start_monat": 4},
    "Liguster":        {"kategorie": ST,"max_wuchshoehe_cm": 300, "wasserbedarf": "Wenig",   "bodenanspruch": "Tolerant",  "ursprungsregion": "Europa/Asien",    "bluetezeit_start_monat": 6},
    "Haselnuss":       {"kategorie": ST,"max_wuchshoehe_cm": 600, "wasserbedarf": "Wenig",   "bodenanspruch": "Neutral",   "ursprungsregion": "Europa",          "bluetezeit_start_monat": 2},
    "Geißblatt":       {"kategorie": ST,"max_wuchshoehe_cm": 500, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Europa",          "bluetezeit_start_monat": 5},
    "Stachelbeere":    {"kategorie": ST,"max_wuchshoehe_cm": 150, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Europa",          "bluetezeit_start_monat": 4},
    "Johannisbeere":   {"kategorie": ST,"max_wuchshoehe_cm": 150, "wasserbedarf": "Mittel",  "bodenanspruch": "Neutral",   "ursprungsregion": "Europa",          "bluetezeit_start_monat": 4},
}

print('\n== Erweitere JSON-Dateien auf mind. 80 Einträge ==\n')
expand('kunst_extended.json',     KUNST_NEW)
expand('hunde_extended.json',     HUNDE_NEW)
expand('gartenbau_extended.json', GARTEN_NEW)
print('\nFertig!')
