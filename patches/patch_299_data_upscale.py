"""
patch_299_data_upscale.py
Phase 299 — Grand Data Upscale: alle Zug-Arrays auf 80+ Items
Sicher: extend() only, bestehende Daten werden NICHT ueberschrieben.
"""
import os, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def extend_safe(arr, new_items, key_field="n"):
    """Fuegt nur Items hinzu, die noch nicht im Array sind (Duplikat-Check via key_field)."""
    existing = {i[key_field] for i in arr if key_field in i}
    added = 0
    for item in new_items:
        if item.get(key_field) not in existing:
            arr.append(item)
            existing.add(item[key_field])
            added += 1
    return added

print("=" * 58)
print(" Patch 299 — Grand Data Upscale (Road to 80)")
print("=" * 58)

# =============================================================
# 1. zug_routen in kultur.json (+35 neue Items)
# =============================================================
print("\n[1] zug_routen (kultur.json) — Ziel: 80 Items")
with open(os.path.join(BASE, "data", "kultur.json"), "r", encoding="utf-8") as f:
    kultur = json.load(f)

NEW_ROUTEN = [
    {"n": "California Zephyr (Chicago–San Francisco)", "c": "USA"},
    {"n": "Empire Builder (Chicago–Seattle)", "c": "USA"},
    {"n": "Southwest Chief (Chicago–Los Angeles)", "c": "USA"},
    {"n": "Coast Starlight (Los Angeles–Seattle)", "c": "USA"},
    {"n": "Acela (Boston–Washington DC)", "c": "USA"},
    {"n": "Auto Train (Washington–Orlando)", "c": "USA"},
    {"n": "NightJet Wien–Hamburg", "c": "Oesterreich"},
    {"n": "NightJet Wien–Bruessel", "c": "Oesterreich"},
    {"n": "NightJet Innsbruck–Berlin", "c": "Oesterreich"},
    {"n": "NightJet Zuerich–Barcelona", "c": "Schweiz"},
    {"n": "FlixTrain Hamburg–Koeln", "c": "Deutschland"},
    {"n": "ICE Berlin–Muenchen", "c": "Deutschland"},
    {"n": "DB IC2 Hamburg–Stuttgart", "c": "Deutschland"},
    {"n": "Hokkaido Shinkansen (Shin-Aomori–Shin-Hakodate)", "c": "Japan"},
    {"n": "Kyushu Shinkansen (Hakata–Kagoshima)", "c": "Japan"},
    {"n": "Sanyo Shinkansen (Osaka–Hakata)", "c": "Japan"},
    {"n": "Joetsu Shinkansen (Tokio–Niigata)", "c": "Japan"},
    {"n": "Hokuriku Shinkansen (Tokio–Kanazawa)", "c": "Japan"},
    {"n": "SRT Suseo (Seoul–Busan, Linie 2)", "c": "Suedkorea"},
    {"n": "Mugunghwa Express (Seoul–Mokpo)", "c": "Suedkorea"},
    {"n": "IRYO Trenitalia ES (Madrid–Barcelona)", "c": "Spanien"},
    {"n": "Ouigo Espana (Madrid–Valencia)", "c": "Spanien"},
    {"n": "Talgo Alvia (Madrid–Bilbao)", "c": "Spanien"},
    {"n": "Renfe AVE Madrid–Valencia", "c": "Spanien"},
    {"n": "Intercites de Nuit Paris–Nice", "c": "Frankreich"},
    {"n": "InOui TGV Paris–Bordeaux", "c": "Frankreich"},
    {"n": "LEO Express Praha–Wien", "c": "Tschechien"},
    {"n": "PKP Pendolino (Warszawa–Gdansk)", "c": "Polen"},
    {"n": "Eurostar (London–Amsterdam)", "c": "Grossbritannien"},
    {"n": "Avanti West Coast (London–Manchester)", "c": "Grossbritannien"},
    {"n": "LNER Azuma (London–Edinburgh)", "c": "Grossbritannien"},
    {"n": "GWR IET (London–Bristol)", "c": "Grossbritannien"},
    {"n": "EuroCity Hamburg–Kopenhagen", "c": "Deutschland"},
    {"n": "Haramain HSR (Mekka–Medina)", "c": "Saudi-Arabien"},
    {"n": "Afrosiyob (Taschkent–Samarkand)", "c": "Usbekistan"},
]

added = extend_safe(kultur["zug_routen"], NEW_ROUTEN)
with open(os.path.join(BASE, "data", "kultur.json"), "w", encoding="utf-8") as f:
    json.dump(kultur, f, ensure_ascii=False, indent=2)
print(f"  [OK] +{added} Items -> gesamt: {len(kultur['zug_routen'])}")

# =============================================================
# 2. zug_bahnhof_typ + zug_hersteller in tiere_match.json
# =============================================================
print("\n[2] zug_bahnhof_typ + zug_hersteller (tiere_match.json)")
with open(os.path.join(BASE, "data", "tiere_match.json"), "r", encoding="utf-8") as f:
    tm = json.load(f)

# fixedOpts bleiben unveraendert: ["Kopfbahnhof","Durchgangsbahnhof","Turmbahnhof","Keilbahnhof"]
NEW_BAHNHOF_TYP = [
    {"n": "Grand Central Terminal New York",   "c": "Kopfbahnhof"},
    {"n": "Antwerpen-Centraal",                "c": "Kopfbahnhof"},
    {"n": "Venezia Santa Lucia",               "c": "Kopfbahnhof"},
    {"n": "Napoli Centrale",                   "c": "Kopfbahnhof"},
    {"n": "Torino Porta Nuova",                "c": "Kopfbahnhof"},
    {"n": "Porto Sao Bento",                   "c": "Kopfbahnhof"},
    {"n": "Paddington London",                 "c": "Kopfbahnhof"},
    {"n": "Liverpool Street London",           "c": "Kopfbahnhof"},
    {"n": "Euston London",                     "c": "Kopfbahnhof"},
    {"n": "Charing Cross London",              "c": "Kopfbahnhof"},
    {"n": "King's Cross London",               "c": "Kopfbahnhof"},
    {"n": "Gare Saint-Lazare Paris",           "c": "Kopfbahnhof"},
    {"n": "Gare de l'Est Paris",               "c": "Kopfbahnhof"},
    {"n": "Gare Montparnasse Paris",           "c": "Kopfbahnhof"},
    {"n": "Marseille Saint-Charles",           "c": "Kopfbahnhof"},
    {"n": "Toulouse Matabiau",                 "c": "Kopfbahnhof"},
    {"n": "Bordeaux Saint-Jean",               "c": "Kopfbahnhof"},
    {"n": "Helsinki Paarautatieasema",         "c": "Kopfbahnhof"},
    {"n": "Innsbruck Hbf",                     "c": "Kopfbahnhof"},
    {"n": "Graz Hbf",                          "c": "Kopfbahnhof"},
    {"n": "Sirkeci Istanbul",                  "c": "Kopfbahnhof"},
    {"n": "Haydarpasa Istanbul",               "c": "Kopfbahnhof"},
    {"n": "Zagreb Glavni Kolodvor",            "c": "Kopfbahnhof"},
    {"n": "Sofia Zentralbahnhof",              "c": "Kopfbahnhof"},
    {"n": "Oslo Sentralstasjon",               "c": "Durchgangsbahnhof"},
    {"n": "Lausanne",                          "c": "Durchgangsbahnhof"},
    {"n": "Linz Hbf",                          "c": "Durchgangsbahnhof"},
    {"n": "Lyon Part-Dieu",                    "c": "Durchgangsbahnhof"},
    {"n": "Lisboa Oriente",                    "c": "Durchgangsbahnhof"},
    {"n": "Bukarest Nord",                     "c": "Durchgangsbahnhof"},
    {"n": "Katowice Hbf",                      "c": "Durchgangsbahnhof"},
    {"n": "Beograd Prokop",                    "c": "Durchgangsbahnhof"},
    {"n": "Muenchen Pasing",                   "c": "Turmbahnhof"},
    {"n": "Berlin Suedkreuz",                  "c": "Turmbahnhof"},
    {"n": "Flensburg Hbf",                     "c": "Keilbahnhof"},
    {"n": "Ulm Hbf",                           "c": "Keilbahnhof"},
]

added_bt = extend_safe(tm["zug_bahnhof_typ"]["items"], NEW_BAHNHOF_TYP)
print(f"  [OK] zug_bahnhof_typ +{added_bt} -> gesamt: {len(tm['zug_bahnhof_typ']['items'])}")

# fixedOpts fuer zug_hersteller: ["Alstom","Siemens Mobility","Hitachi Rail","Stadler Rail"]
NEW_HERSTELLER = [
    {"n": "TALENT 3 (DB Regio)",               "c": "Alstom"},
    {"n": "TALENT 2 (Eurobahn)",               "c": "Alstom"},
    {"n": "Omneo Premium (SNCF TER)",          "c": "Alstom"},
    {"n": "Avelia Pendolino (NTV)",            "c": "Alstom"},
    {"n": "X'Trapolis M (Metro Trains AU)",    "c": "Alstom"},
    {"n": "Coradia Nordic (SJ)",               "c": "Alstom"},
    {"n": "Coradia Stream (DB AG)",            "c": "Alstom"},
    {"n": "TGV POS (SNCF)",                    "c": "Alstom"},
    {"n": "Avelia Ocean (SNCF M)",             "c": "Alstom"},
    {"n": "ICE 1 (BR 401)",                    "c": "Siemens Mobility"},
    {"n": "ICE 2 (BR 402)",                    "c": "Siemens Mobility"},
    {"n": "ICE T (BR 411)",                    "c": "Siemens Mobility"},
    {"n": "Velaro TR (TCDD YHT)",              "c": "Siemens Mobility"},
    {"n": "Desiro ML (DB Regio)",              "c": "Siemens Mobility"},
    {"n": "Desiro HC (RRX)",                   "c": "Siemens Mobility"},
    {"n": "Inspiro (Warschau Metro)",          "c": "Siemens Mobility"},
    {"n": "ES64U4 Taurus (OeBB)",              "c": "Siemens Mobility"},
    {"n": "Viaggio Comfort (RJ600)",           "c": "Siemens Mobility"},
    {"n": "Mireo Smart (DB)",                  "c": "Siemens Mobility"},
    {"n": "Class 385 (ScotRail)",              "c": "Hitachi Rail"},
    {"n": "AT100 (Class 717 GN Metroland)",    "c": "Hitachi Rail"},
    {"n": "Class 387 (GWR/Thameslink)",        "c": "Hitachi Rail"},
    {"n": "Shinkansen E6 (Komachi)",           "c": "Hitachi Rail"},
    {"n": "Shinkansen E7/W7 (Kagayaki)",       "c": "Hitachi Rail"},
    {"n": "Class 810 (Avanti Evero)",          "c": "Hitachi Rail"},
    {"n": "Caravaggio ETR 700 (NS Intercity)", "c": "Hitachi Rail"},
    {"n": "FLIRT 3 (DB Regio BA)",             "c": "Stadler Rail"},
    {"n": "FLIRT Akku (Batterie-Triebwagen)",  "c": "Stadler Rail"},
    {"n": "RABe 521 FLIRT (BLS)",              "c": "Stadler Rail"},
    {"n": "RABe 524 FLIRT (Ticino/Vaud)",      "c": "Stadler Rail"},
    {"n": "KISS Westbahn (WB 3)",              "c": "Stadler Rail"},
    {"n": "Flirt 3XL (Infrabel)",              "c": "Stadler Rail"},
    {"n": "GTW 6/10 (Arriva NL)",              "c": "Stadler Rail"},
    {"n": "TANGO (Bernmobil Strassenbahn)",    "c": "Stadler Rail"},
    {"n": "WINK (Niederflurzug DE)",           "c": "Stadler Rail"},
    {"n": "RABe 501 Traverso (SBB/TILO)",      "c": "Stadler Rail"},
]

added_h = extend_safe(tm["zug_hersteller"]["items"], NEW_HERSTELLER)
print(f"  [OK] zug_hersteller  +{added_h} -> gesamt: {len(tm['zug_hersteller']['items'])}")

with open(os.path.join(BASE, "data", "tiere_match.json"), "w", encoding="utf-8") as f:
    json.dump(tm, f, ensure_ascii=False, indent=2)

# =============================================================
# 3. metro_logos (+45 neue SVGs)
# =============================================================
print("\n[3] metro_logos (metro_logos.json) — Ziel: 80 Items")
with open(os.path.join(BASE, "data", "metro_logos.json"), "r", encoding="utf-8") as f:
    ml = json.load(f)

existing_cities = {m["city"] for m in ml}

NEW_METROS = [
    # Asien
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#8B1A8B'/><text x='50' y='72' font-size='52' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>M</text></svg>","city":"Osaka (Metro)","cc":"jp2"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#003087'/><text x='50' y='65' font-size='36' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>DMRC</text></svg>","city":"Delhi (Metro)","cc":"in"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><rect x='5' y='5' width='90' height='90' rx='8' fill='#E30613'/><text x='50' y='68' font-size='40' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>نقل</text></svg>","city":"Dubai (Metro)","cc":"ae"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#0057A8'/><text x='50' y='65' font-size='36' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>EMN</text></svg>","city":"Kairo (Metro)","cc":"eg"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><polygon points='50,4 96,27 96,73 50,96 4,73 4,27' fill='#ED1C24'/><text x='50' y='68' font-size='46' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>M</text></svg>","city":"Kopenhagen (Metro)","cc":"dk"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#F7901E'/><text x='50' y='72' font-size='52' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>M</text></svg>","city":"Helsinki (Metro)","cc":"fi"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#FFD700'/><circle cx='50' cy='50' r='35' fill='#003082'/><text x='50' y='65' font-size='36' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>ML</text></svg>","city":"Lissabon (Metro)","cc":"pt"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><rect x='5' y='5' width='90' height='90' rx='8' fill='#E30613'/><text x='50' y='65' font-size='40' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>BM</text></svg>","city":"Bilbao (Metro)","cc":"es3"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#F5A800'/><text x='50' y='72' font-size='52' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>M</text></svg>","city":"Lyon (Métro)","cc":"fr2"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#E30613'/><text x='50' y='65' font-size='36' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>TISSÉO</text></svg>","city":"Toulouse (Métro)","cc":"fr3"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#009FE3'/><text x='50' y='72' font-size='52' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>M</text></svg>","city":"Marseille (Métro)","cc":"fr4"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#E30613'/><rect x='20' y='44' width='60' height='12' fill='white' rx='2'/><circle cx='50' cy='50' r='12' fill='white'/><text x='50' y='56' font-size='14' fill='#E30613' font-family='Arial' font-weight='bold' text-anchor='middle'>MM</text></svg>","city":"Mailand (MM)","cc":"it2"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#003082'/><text x='50' y='65' font-size='36' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>GTT</text></svg>","city":"Turin (Metro)","cc":"it3"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#003580'/><text x='50' y='72' font-size='52' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>M</text></svg>","city":"Sofia (Metro)","cc":"bg"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#003F8A'/><text x='50' y='72' font-size='52' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>M</text></svg>","city":"Bukarest (Metro)","cc":"ro"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><rect x='5' y='5' width='90' height='90' rx='8' fill='#EF3340'/><text x='50' y='72' font-size='52' fill='#FFD700' font-family='Arial' font-weight='bold' text-anchor='middle'>M</text></svg>","city":"Budapest (Metro)","cc":"hu"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#003082'/><text x='50' y='65' font-size='36' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>KMЖ</text></svg>","city":"Kiew (Metro)","cc":"ua"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#C8102E'/><text x='50' y='72' font-size='52' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>M</text></svg>","city":"Minsk (Metro)","cc":"by"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#E30613'/><text x='50' y='65' font-size='36' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>Tbil</text></svg>","city":"Tiflis (Metro)","cc":"ge"},
    # Nordamerika
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#D62D20'/><text x='50' y='65' font-size='36' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>TTC</text></svg>","city":"Toronto (TTC)","cc":"ca2"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#003F8A'/><text x='50' y='65' font-size='28' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>SkyTrain</text></svg>","city":"Vancouver (SkyTrain)","cc":"ca3"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#0072BC'/><text x='50' y='65' font-size='36' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>LA</text></svg>","city":"Los Angeles (Metro)","cc":"us6"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#FF6600'/><text x='50' y='65' font-size='28' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>MARTA</text></svg>","city":"Atlanta (MARTA)","cc":"us7"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#FF6600'/><text x='50' y='65' font-size='24' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>Metrorail</text></svg>","city":"Miami (Metrorail)","cc":"us8"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#003087'/><text x='50' y='65' font-size='28' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>SEPTA</text></svg>","city":"Philadelphia (SEPTA)","cc":"us9"},
    # Suedamerika
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#003F8A'/><text x='50' y='72' font-size='52' fill='#FFD700' font-family='Arial' font-weight='bold' text-anchor='middle'>M</text></svg>","city":"Rio de Janeiro (Metro)","cc":"br2"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#CC0000'/><text x='50' y='72' font-size='52' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>M</text></svg>","city":"Santiago (Metro)","cc":"cl"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#009B3A'/><text x='50' y='72' font-size='52' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>M</text></svg>","city":"Medellin (Metro)","cc":"co"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#003F8A'/><text x='50' y='65' font-size='36' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>Lima</text></svg>","city":"Lima (Metro)","cc":"pe"},
    # Asien (weitere)
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#009944'/><text x='50' y='65' font-size='28' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>BTS</text></svg>","city":"Bangkok (BTS)","cc":"th"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><rect x='5' y='5' width='90' height='90' rx='8' fill='#003F8A'/><text x='50' y='65' font-size='28' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>RapidKL</text></svg>","city":"Kuala Lumpur (LRT)","cc":"my"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#003F8A'/><text x='50' y='65' font-size='28' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>MRT</text></svg>","city":"Jakarta (MRT)","cc":"id"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#E30613'/><text x='50' y='65' font-size='28' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>名古屋</text></svg>","city":"Nagoya (Subway)","cc":"jp3"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#009F6B'/><text x='50' y='65' font-size='28' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>福岡</text></svg>","city":"Fukuoka (Subway)","cc":"jp4"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#E30613'/><text x='50' y='65' font-size='28' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>Busan</text></svg>","city":"Busan (Metro)","cc":"kr2"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#E30613'/><text x='50' y='65' font-size='28' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>Mumbai</text></svg>","city":"Mumbai (Metro)","cc":"in2"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#003F8A'/><text x='50' y='65' font-size='28' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>Namma</text></svg>","city":"Bengaluru (Metro)","cc":"in3"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#7B2D8B'/><text x='50' y='65' font-size='28' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>HMRL</text></svg>","city":"Hyderabad (Metro)","cc":"in4"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#CC0000'/><text x='50' y='65' font-size='28' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>CMRL</text></svg>","city":"Chennai (Metro)","cc":"in5"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#003F8A'/><text x='50' y='65' font-size='28' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>Tehran</text></svg>","city":"Teheran (Metro)","cc":"ir"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#8B4513'/><text x='50' y='65' font-size='28' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>Doha</text></svg>","city":"Doha (Metro)","cc":"qa"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#006400'/><text x='50' y='65' font-size='28' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>RRX</text></svg>","city":"Riad (Metro)","cc":"sa"},
    # Europa (weitere)
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#E30613'/><text x='50' y='72' font-size='52' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>M</text></svg>","city":"Valencia (Metro)","cc":"es4"},
    {"svg":"<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='48' fill='#003082'/><text x='50' y='72' font-size='52' fill='white' font-family='Arial' font-weight='bold' text-anchor='middle'>M</text></svg>","city":"Porto (Metro)","cc":"pt2"},
]

added_m = 0
for item in NEW_METROS:
    if item["city"] not in existing_cities:
        ml.append(item)
        existing_cities.add(item["city"])
        added_m += 1

with open(os.path.join(BASE, "data", "metro_logos.json"), "w", encoding="utf-8") as f:
    json.dump(ml, f, ensure_ascii=False, indent=2)
print(f"  [OK] +{added_m} Items -> gesamt: {len(ml)}")

# =============================================================
# Abschluss-Report
# =============================================================
print("\n" + "=" * 58)
with open(os.path.join(BASE, "data", "kultur.json"), "r", encoding="utf-8") as f: k2=json.load(f)
with open(os.path.join(BASE, "data", "tiere_match.json"), "r", encoding="utf-8") as f: tm2=json.load(f)
with open(os.path.join(BASE, "data", "metro_logos.json"), "r", encoding="utf-8") as f: ml2=json.load(f)
print(f" zug_routen:      {len(k2['zug_routen']):3d} Items {'✅' if len(k2['zug_routen'])>=80 else '❌'}")
print(f" zug_bahnhof_typ: {len(tm2['zug_bahnhof_typ']['items']):3d} Items {'✅' if len(tm2['zug_bahnhof_typ']['items'])>=80 else '❌'}")
print(f" zug_hersteller:  {len(tm2['zug_hersteller']['items']):3d} Items {'✅' if len(tm2['zug_hersteller']['items'])>=80 else '❌'}")
print(f" metro_logos:     {len(ml2):3d} Items {'✅' if len(ml2)>=80 else '❌'}")
print("=" * 58)
print("[DONE] Jetzt: python gen.py && python verify.py")
