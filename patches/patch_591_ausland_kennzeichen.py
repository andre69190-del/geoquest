# -*- coding: utf-8 -*-
"""
Phase: 591
Date:  2026-10-26
Scope: Kennzeichen-Spotter Ausland — falsche/erfundene Laenderdaten in license_plates.json
       durch web-verifizierte Listen ersetzt + Italien-Hinweis korrigiert (gen.py)

Quellen: en.wikipedia "Vehicle registration plates of Croatia/Slovenia/Bulgaria/Greece/
Romania", de.wikipedia "Departement#Uebersichtstabelle", "Kfz-Kennzeichen (Oesterreich)".
- Frankreich: Datenmuell (Fahrzeugnamen, Seriennummern, Libyen-Region) -> 101 Departements
  (Nummer im blauen Feld rechts; seit 2009 frei waehlbar, Alt-Kennzeichen bis 2009 regional)
- Kroatien: 34 aktuelle + 5 alte Codes (vorher u.a. ST=Sibenik falsch, VA/ZGB/NV erfunden)
- Slowenien: 11 Codes (vorher GO=Gornja Radgona falsch, AX/IL/NG/SL/TL/TS erfunden)
- Bulgarien: 28 Bezirke (Latein-Schreibweise), vorher Kyrillisch/Latein-Mix mit Fehlern
- Griechenland: erfundene Liste (A=Athen ...) -> nur Nationalkennzeichen GR
  (echtes System: griech. Praefix-Buchstaben je Praefektur, Ausbau als Folgeaufgabe)
- Italien: Fremd-Codes 16/IT-AG/ROMA/I entfernt; Hinweis: Provinz steht rechts im blauen
  Feld (seit 1999 freiwillig), links ist eine landesweite Seriennummer
- Rumaenien: CJ-N und Platzhalter RO entfernt; Oesterreich: BA (Bad Aussee) ergaenzt
Idempotent.
"""
import io, json

REPL = {"Frankreich": [["01", "Ain"], ["02", "Aisne"], ["03", "Allier"], ["04", "Alpes-de-Haute-Provence"], ["05", "Hautes-Alpes"], ["06", "Alpes-Maritimes"], ["07", "Ardèche"], ["08", "Ardennes"], ["09", "Ariège"], ["10", "Aube"], ["11", "Aude"], ["12", "Aveyron"], ["13", "Bouches-du-Rhône"], ["14", "Calvados"], ["15", "Cantal"], ["16", "Charente"], ["17", "Charente-Maritime"], ["18", "Cher"], ["19", "Corrèze"], ["21", "Côte-d’Or"], ["22", "Côtes-d’Armor"], ["23", "Creuse"], ["24", "Dordogne"], ["25", "Doubs"], ["26", "Drôme"], ["27", "Eure"], ["28", "Eure-et-Loir"], ["29", "Finistère"], ["2A", "Corse-du-Sud"], ["2B", "Haute-Corse"], ["30", "Gard"], ["31", "Haute-Garonne"], ["32", "Gers"], ["33", "Gironde"], ["34", "Hérault"], ["35", "Ille-et-Vilaine"], ["36", "Indre"], ["37", "Indre-et-Loire"], ["38", "Isère"], ["39", "Jura"], ["40", "Landes"], ["41", "Loir-et-Cher"], ["42", "Loire"], ["43", "Haute-Loire"], ["44", "Loire-Atlantique"], ["45", "Loiret"], ["46", "Lot"], ["47", "Lot-et-Garonne"], ["48", "Lozère"], ["49", "Maine-et-Loire"], ["50", "Manche"], ["51", "Marne"], ["52", "Haute-Marne"], ["53", "Mayenne"], ["54", "Meurthe-et-Moselle"], ["55", "Meuse"], ["56", "Morbihan"], ["57", "Moselle"], ["58", "Nièvre"], ["59", "Nord"], ["60", "Oise"], ["61", "Orne"], ["62", "Pas-de-Calais"], ["63", "Puy-de-Dôme"], ["64", "Pyrénées-Atlantiques"], ["65", "Hautes-Pyrénées"], ["66", "Pyrénées-Orientales"], ["67", "Bas-Rhin"], ["68", "Haut-Rhin"], ["69", "Rhône"], ["70", "Haute-Saône"], ["71", "Saône-et-Loire"], ["72", "Sarthe"], ["73", "Savoie"], ["74", "Haute-Savoie"], ["75", "Paris"], ["76", "Seine-Maritime"], ["77", "Seine-et-Marne"], ["78", "Yvelines"], ["79", "Deux-Sèvres"], ["80", "Somme"], ["81", "Tarn"], ["82", "Tarn-et-Garonne"], ["83", "Var"], ["84", "Vaucluse"], ["85", "Vendée"], ["86", "Vienne"], ["87", "Haute-Vienne"], ["88", "Vosges"], ["89", "Yonne"], ["90", "Territoire de Belfort"], ["91", "Essonne"], ["92", "Hauts-de-Seine"], ["93", "Seine-Saint-Denis"], ["94", "Val-de-Marne"], ["95", "Val-d’Oise"], ["971", "Guadeloupe"], ["972", "Martinique"], ["973", "Französisch-Guayana"], ["974", "Réunion"], ["976", "Mayotte"]], "Kroatien": [["BJ", "Bjelovar"], ["BM", "Beli Manastir"], ["ČK", "Čakovec"], ["DA", "Daruvar"], ["DE", "Delnice"], ["DJ", "Đakovo"], ["DU", "Dubrovnik"], ["GS", "Gospić"], ["IM", "Imotski"], ["KA", "Karlovac"], ["KC", "Koprivnica"], ["KR", "Krapina"], ["KT", "Kutina"], ["KŽ", "Križevci"], ["MA", "Makarska"], ["NA", "Našice"], ["NG", "Nova Gradiška"], ["OG", "Ogulin"], ["OS", "Osijek"], ["PU", "Pula"], ["PŽ", "Požega"], ["RI", "Rijeka"], ["SB", "Slavonski Brod"], ["SK", "Sisak"], ["SL", "Slatina"], ["ST", "Split"], ["ŠI", "Šibenik"], ["VK", "Vinkovci"], ["VT", "Virovitica"], ["VU", "Vukovar"], ["VŽ", "Varaždin"], ["ZD", "Zadar"], ["ZG", "Zagreb"], ["ŽU", "Županja"], ["KN", "Krapina"], ["PS", "Slatina"], ["SI", "Sisak"], ["SP", "Požega"], ["TK", "Korenica"]], "Slowenien": [["CE", "Celje"], ["GO", "Nova Gorica"], ["KK", "Krško"], ["KP", "Koper"], ["KR", "Kranj"], ["LJ", "Ljubljana"], ["MB", "Maribor"], ["MS", "Murska Sobota"], ["NM", "Novo mesto"], ["PO", "Postojna"], ["SG", "Slovenj Gradec"]], "Bulgarien": [["A", "Burgas"], ["B", "Warna"], ["BH", "Widin"], ["BP", "Wraza"], ["BT", "Weliko Tarnowo"], ["E", "Blagoewgrad"], ["EB", "Gabrowo"], ["EH", "Plewen"], ["K", "Kardschali"], ["KH", "Kjustendil"], ["M", "Montana"], ["H", "Schumen"], ["OB", "Lowetsch"], ["P", "Russe"], ["PA", "Pasardschik"], ["PB", "Plowdiw"], ["PK", "Pernik"], ["PP", "Rasgrad"], ["C", "Sofia (Stadt)"], ["CA", "Sofia (Stadt)"], ["CB", "Sofia (Stadt)"], ["CH", "Sliwen"], ["CM", "Smoljan"], ["CO", "Oblast Sofia"], ["CC", "Silistra"], ["CT", "Stara Sagora"], ["T", "Targowischte"], ["TX", "Dobritsch"], ["Y", "Jambol"], ["X", "Haskowo"]], "Griechenland": [["GR", "Nationales Kennzeichen"]]}
REMOVE = {"Italien": ["16", "IT-AG", "ROMA", "I"], "Rumänien": ["CJ-N", "RO"]}
ADD = [["Österreich", "BA", "Bad Aussee"]]

PATH = 'license_plates.json'
with io.open(PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)
n0 = len(data)
data = [x for x in data if x.get('countryLabel') not in REPL
        and x.get('code') not in REMOVE.get(x.get('countryLabel'), [])]
for c, lst in REPL.items():
    for code, reg in lst:
        data.append({'code': code, 'regionLabel': reg, 'countryLabel': c})
have = {(x['code'], x['regionLabel'], x['countryLabel']) for x in data}
for c, code, reg in ADD:
    if (code, reg, c) not in have:
        data.append({'code': code, 'regionLabel': reg, 'countryLabel': c})
with io.open(PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
print('license_plates.json: %d -> %d' % (n0, len(data)))

# Italien-Hinweis im Spotter (gen.py)
G = 'gen.py'
with io.open(G, 'r', encoding='utf-8') as f:
    c = f.read()
OLD = "'Italien':{ph:'K\\u00fcrzel (z.B. RM, MI...)',info:'2 Buchst. links = Provinz',tp:'de',ex:'RM',lbl:'RM steht f\\u00fcr Rom',cc:'I',nums:'RM 123 AB'},"
NEW = "'Italien':{ph:'Provinz (z.B. RM, MI...)',info:'Provinz-K\\u00fcrzel im blauen Feld rechts (freiwillig) \\u2013 die Buchstaben links sind eine landesweite Seriennummer',tp:'fr',ex:'RM',lbl:'RM rechts steht f\\u00fcr die Provinz Rom',cc:'I',nums:'AB 123 CD'},"
if NEW not in c:
    assert c.count(OLD) == 1, 'Italien-Hinweis nicht eindeutig gefunden'
    c = c.replace(OLD, NEW)
    with io.open(G, 'w', encoding='utf-8') as f:
        f.write(c)
    print('gen.py: Italien-Hinweis aktualisiert')
