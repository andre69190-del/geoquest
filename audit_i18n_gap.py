#!/usr/bin/env python3
"""
GeoQuest i18n Gap Audit
Phase 328+ — Identifiziert c-Felder, die NICHT via Intl.DisplayNames übersetzt werden

Drei Klassen:
  A) Standard-ISO-Länder  → _tcc() löst auf → alle 24 Sprachen ✅
  B) Geo-Regionen (kein ISO) → _tc()-Fallback → nur DE/EN/PL ⚠️
  C) Semantische Kategorien → _tc()-Fallback → nur DE/EN/PL ℹ️ (kein Bug)

Arrays, die BEWUSST nicht geografisch sind, werden pro Datei annotiert.
"""

import json
import os
import re
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

# ---------------------------------------------------------------------------
# Vollständiges DE→ISO-cc Mapping (entspricht was _deCountryCc() zur Laufzeit baut)
# ---------------------------------------------------------------------------

DE_TO_CC = {
    'Afghanistan':'af','Albanien':'al','Algerien':'dz','Andorra':'ad','Angola':'ao',
    'Antigua und Barbuda':'ag','Armenien':'am','Argentinien':'ar','Australien':'au',
    'Österreich':'at','Aserbaidschan':'az','Bahamas':'bs','Bahrain':'bh',
    'Bangladesh':'bd','Barbados':'bb','Belarus':'by','Belgien':'be','Belize':'bz',
    'Benin':'bj','Bhutan':'bt','Bolivien':'bo','Bosnien und Herzegowina':'ba',
    'Botswana':'bw','Brasilien':'br','Brunei':'bn','Bulgarien':'bg',
    'Burkina Faso':'bf','Burundi':'bi','Kamerun':'cm','Kanada':'ca',
    'Kap Verde':'cv','Zentralafrikanische Republik':'cf','Tschad':'td',
    'Chile':'cl','China':'cn','Kolumbien':'co','Komoren':'km',
    'DR Kongo':'cd','Kongo':'cg','Costa Rica':'cr','Kroatien':'hr',
    'Kuba':'cu','Zypern':'cy','Tschechien':'cz','Dänemark':'dk',
    'Dschibuti':'dj','Dominikanische Republik':'do','Ecuador':'ec',
    'Ägypten':'eg','El Salvador':'sv','Äquatorialguinea':'gq','Eritrea':'er',
    'Estland':'ee','Äthiopien':'et','Fidschi':'fj','Finnland':'fi',
    'Frankreich':'fr','Gabun':'ga','Gambia':'gm','Georgien':'ge',
    'Deutschland':'de','Ghana':'gh','Griechenland':'gr','Grenada':'gd',
    'Guatemala':'gt','Guinea':'gn','Guinea-Bissau':'gw','Guyana':'gy',
    'Haiti':'ht','Honduras':'hn','Ungarn':'hu','Island':'is',
    'Indien':'in','Indonesien':'id','Iran':'ir','Irak':'iq',
    'Irland':'ie','Israel':'il','Italien':'it','Elfenbeinküste':'ci',
    'Jamaika':'jm','Japan':'jp','Jordanien':'jo','Kasachstan':'kz',
    'Kenia':'ke','Kiribati':'ki','Nordkorea':'kp','Südkorea':'kr',
    'Kuwait':'kw','Kirgisistan':'kg','Laos':'la','Lettland':'lv',
    'Libanon':'lb','Lesotho':'ls','Liberia':'lr','Libyen':'ly',
    'Liechtenstein':'li','Litauen':'lt','Luxemburg':'lu',
    'Madagaskar':'mg','Malawi':'mw','Malaysia':'my','Mali':'ml',
    'Malta':'mt','Mauretanien':'mr','Mauritius':'mu','Mexiko':'mx',
    'Moldau':'md','Monaco':'mc','Mongolei':'mn','Montenegro':'me',
    'Marokko':'ma','Mosambik':'mz','Myanmar':'mm','Namibia':'na',
    'Nauru':'nr','Nepal':'np','Niederlande':'nl','Neuseeland':'nz',
    'Nicaragua':'ni','Niger':'ne','Nigeria':'ng','Nordmazedonien':'mk',
    'Norwegen':'no','Oman':'om','Pakistan':'pk','Palau':'pw',
    'Palästina':'ps','Panama':'pa','Papua-Neuguinea':'pg','Paraguay':'py',
    'Peru':'pe','Philippinen':'ph','Polen':'pl','Portugal':'pt',
    'Puerto Rico':'pr','Katar':'qa','Rumänien':'ro','Russland':'ru',
    'Ruanda':'rw','Samoa':'ws','San Marino':'sm','Saudi-Arabien':'sa',
    'Senegal':'sn','Serbien':'rs','Sierra Leone':'sl','Singapur':'sg',
    'Slowakei':'sk','Slowenien':'si','Salomonen':'sb','Somalia':'so',
    'Südafrika':'za','Spanien':'es','Sri Lanka':'lk','Sudan':'sd',
    'Suriname':'sr','Eswatini':'sz','Schweden':'se','Schweiz':'ch',
    'Syrien':'sy','Taiwan':'tw','Tadschikistan':'tj','Tansania':'tz',
    'Thailand':'th','Timor-Leste':'tl','Togo':'tg','Tonga':'to',
    'Trinidad und Tobago':'tt','Tunesien':'tn','Türkei':'tr',
    'Turkmenistan':'tm','Tuvalu':'tv','Uganda':'ug','Ukraine':'ua',
    'Vereinigte Arabische Emirate':'ae','Großbritannien':'gb',
    'USA':'us','Uruguay':'uy','Usbekistan':'uz','Vanuatu':'vu',
    'Venezuela':'ve','Vietnam':'vn','Jemen':'ye','Sambia':'zm','Simbabwe':'zw',
    # Aliase
    'England':'gb','Schottland':'gb','Wales':'gb','Nordirland':'gb',
    'Grönland':'dk','Tibet/China':'cn','Tibet':'cn',
    'Bolivien/Peru':'bo','Peru/Bolivien':'bo',
    'Serbien/Kroatien':'rs',
    'Indien (Punjab)':'in','Indien/Pakistan':'in',
    'Großbritannien / Indien':'gb',
    'Rumänien/Israel':'ro',
    'Hawaii/Portugal':'us',
    'Peru/Anden':'pe',
}

# Arrays, bei denen c BEWUSST kein Länder-/Geo-Feld ist
KNOWN_NON_GEO_ARRAYS = {
    # Tiere
    'faehrten','architekten','tarnung','ernaehrung','symbiose','tauchtiefe',
    'mimikry','metamorphose','biolumineszenz','anatomie','laute','sinne',
    'arktis_antarktis','forscher_eponyme','pelagial','wuesten_spezialisten',
    'gift_hotspots','pferde_fachbegriffe','reitsport_disziplinen',
    'zug_bahnhof_typ','zug_hersteller',
    # Geo
    'geo_gesteinsarten','geo_tektonik','geo_mineralien','geo_wunder_entstehung',
    'geo_fossil_zeitalter','geo_erdbeben_jahr','geo_gestein_nutzung',
    'geo_landschaft_ursprung','geo_mineral_farbe','geo_kontinent_platte',
    'geo_mineral_kristall','geo_gebirge_entstehung','geo_berg_gebirge',
    # Sport
    'sport_teamgroesse','sport_weltverband','sport_olympisch',
    'sport_disziplin_kategorie','sport_sportart_kontinent','sport_rekordhalter',
    'sport_olympia_standort',
    # Archaeologie
    'epochen','werkzeuge','datierungsmethoden','3d_methoden','stratigraphie',
    'isotopenanalyse','archaeobotanik','faelschungen','popkultur_vs_realitaet',
    'welterbe_gefahr','zufallsfunde','digifund_epochen','schatzsuche_methoden',
    # Gastro
    'schnitttechniken','kuechengeraete','fleisch_cuts','bakterien_pilze',
    'kaffeespezialitaeten','pasta_formen','exotische_fruechte','brotsorten',
    'vegan_alternativen','fachbegriffe_herd','sushi_arten','ess_etikette','tabus',
    # Pflanzen
    'familien','bluetezeit','giftstoffe','fruchttyp','vermehrung','lebensraum',
    'bestuaeber','nutzung','blattform','klimazone','scheinfruchte',
    'baum_des_jahres','giftpflanze_jahres',
    # E-Mob
    'plattform','motortyp','ladestandard','reichweite_klasse','ladeposition',
    # Astro, Tech etc.
    'kaffeespezialitaeten',
}

# ---------------------------------------------------------------------------
# Geo-Regionen ohne ISO (kein Bug, aber kein auto-translate)
# ---------------------------------------------------------------------------

KNOWN_GEO_REGIONS = {
    'Westafrika','Ostafrika','Zentralafrika','Nordafrika','Südafrika (Region)',
    'Naher Osten','Arabische Halbinsel','Golf-Staaten','Levante','Persien',
    'Kaukasus','Zentralasien','Südostasien','Indochina','Fernost',
    'Nordamerika','Südamerika','Mittelamerika','Lateinamerika','Karibik',
    'Ozeanien','Melanesien','Polynesien','Mikronesien (Region)',
    'Nordskandinavien','Skandinavien','Baltikum','Balkanhalbinsel',
    'Asien','Europa','Amerika','Arktis','Antarktis',
    'Arktis (Nordpol)','Antarktis (Südpol)','Sahara',
    'Sargassosee','Indischer Ozean',
    # Historische Entitäten
    'Mesopotamien','Babylonien','Persisches Reich','Osmanisches Reich',
    'Byzantinisches Reich','Römisches Reich','Heiliges Römisches Reich',
    'Sowjetunion','Jugoslawien','Tschechoslowakei','Österreich-Ungarn',
    'Mayas','Maya','Azteken','Inka','Wikinger',
    'Römer','Griechen','Kelten','Phönizier',
    'Ägypten (antik)','Neolithikum','Neolithikum Europa',
    'Induskultur','Ancestral Puebloans',
    # Sub-nationale Regionen (bewusst genutzt)
    'Bayern','Böhmen','Mähren','Preußen','Franken','Westfalen','Dalmatien',
    'Toskana','Katalonien','Baskenland','Andalusien','Aragon',
    'Schottland','Wales','England','Nordirland',
    'Hawaii','Alaska','Sibirien','Tibet','Xinjiang','Kaschmir',
    'Palästina','Kurdistan','Grönland',
    'Mani-Halbinsel','Peloponnes','Kreta','Dalmatien',
    # Sonstige aus GeoQuest-Daten
    'Amazonasgebiet','Kongo-Becken','Gobi','Patagonia',
    'Trinidad','Java, Indonesien','Indonesien (Bali)','Indonesien (Aceh)',
    'Bolivien/Peru','Peru/Bolivien','Peru/Anden',
    'Indien (Punjab)','Indien/Pakistan','Hawaii/Portugal',
    'Serbien/Kroatien','Rumänien/Israel','Großbritannien / Indien',
    'Nordafrika (Marokko)',
}

# ---------------------------------------------------------------------------
# Scan
# ---------------------------------------------------------------------------

def scan_file(fname, data):
    results = defaultdict(list)  # array_key -> [(c_val, n_val, class)]

    def scan_obj(obj, arr_key):
        if isinstance(obj, dict):
            if 'items' in obj and isinstance(obj['items'], list):
                for item in obj['items']:
                    if not isinstance(item, dict): continue
                    if 'c' not in item or 'n' not in item: continue
                    c_val = item['c']
                    n_val = item['n']
                    if not isinstance(c_val, str): continue

                    if arr_key in KNOWN_NON_GEO_ARRAYS:
                        cls = 'C'  # semantic, expected
                    elif c_val in DE_TO_CC:
                        cls = 'A'  # ISO-mapped, auto-translated ✅
                    elif c_val in KNOWN_GEO_REGIONS:
                        cls = 'B'  # geo-region, _tc() fallback ⚠️
                    else:
                        cls = 'C'  # semantic or unknown

                    results[arr_key].append((c_val, n_val, cls))
            for k, v in obj.items():
                if k != 'items':
                    scan_obj(v, k)
        elif isinstance(obj, list):
            for i in obj:
                scan_obj(i, arr_key)

    scan_obj(data, '?')
    return results

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def run():
    print("=" * 65)
    print("GeoQuest i18n Gap Audit — Phase 328+")
    print("=" * 65)
    print()
    print("Klassen:")
    print("  A) ISO-Länder → Intl.DisplayNames → alle 24 Sprachen ✅")
    print("  B) Geo-Regionen (kein ISO) → _tc() → nur DE/EN/PL ⚠️")
    print("  C) Semantisch/Nicht-geo → _tc() Fallback → erwartet ℹ️")
    print()

    total = Counter()
    class_b_entries = defaultdict(set)  # c_val -> set of files

    files = sorted(f for f in os.listdir(DATA) if f.endswith('.json'))

    for fname in files:
        with open(os.path.join(DATA, fname)) as f:
            data = json.load(f)

        file_results = scan_file(fname, data)
        file_counts = Counter()

        for arr_key, items in file_results.items():
            for c_val, n_val, cls in items:
                file_counts[cls] += 1
                total[cls] += 1
                if cls == 'B':
                    class_b_entries[c_val].add(fname)

        if any(v > 0 for v in file_counts.values()):
            a = file_counts['A']
            b = file_counts['B']
            pct_a = 100*a/(a+b) if (a+b) > 0 else 100
            marker = '⚠️ ' if b > 0 else '✅'
            print(f"  {marker} {fname:<35s}  A:{a:4d}  B:{b:3d}  "
                  f"(ISO-Coverage: {pct_a:.0f}%)")

    print()
    print("=" * 65)
    print(f"GESAMT: A={total['A']} (ISO✅)  B={total['B']} (Geo-Region⚠️)  "
          f"C={total['C']} (Semantisch ℹ️)")
    total_geo = total['A'] + total['B']
    if total_geo > 0:
        print(f"ISO-Abdeckung geografischer Felder: "
              f"{100*total['A']//total_geo}% ({total['A']}/{total_geo})")

    print()
    print("=" * 65)
    print("Klasse-B Geo-Regionen (erscheinen für 22 Sprachen auf Deutsch):")
    print()
    sorted_b = sorted(class_b_entries.items(), key=lambda x: -len(x[1]))
    for c_val, file_set in sorted_b[:30]:
        print(f"  {c_val:<40s}  in {len(file_set)} Datei(en): "
              f"{', '.join(sorted(file_set))}")

    if len(sorted_b) > 30:
        print(f"  ... und {len(sorted_b)-30} weitere")

    print()
    print("=" * 65)
    print("Empfehlung für nächste i18n-Sprints:")
    print("  1. Häufigste Klasse-B-Werte in _CONTENT_I18N aufnehmen")
    print("     (mindestens EN + die 5 größten Nicht-DE Sprachen: PL/FR/ES/IT/NL)")
    print("  2. Für historische Kulturen/Epochen reicht ein kurzes")
    print("     Kulturkreis-Lookup (z.B. 'Mesopotamien' → Irak/Syrien/keine ISO)")
    print("  3. validate_content.py ISO-Check nur für bekannte Geo-Arrays aktivieren")
    print("=" * 65)


if __name__ == "__main__":
    run()
