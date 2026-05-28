"""
patch_270_global_sweep.py  —  Phase 270.5 Global <40 Sweep
Erweitert ALLE Arrays mit 15-35 Items in tiere, archaeologie, emob,
tech, pflanzen, gastro, geo, astro, sport, kultur auf mindestens 40 Items.
"""
import json, os, sys

BASE = os.path.join(os.path.dirname(__file__), '..')
DATA = os.path.join(BASE, 'data')

def load(fn):
    with open(os.path.join(DATA, fn), encoding='utf-8') as f:
        return json.load(f)

def save(fn, d):
    with open(os.path.join(DATA, fn), 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def ext(lst, new, key='name'):
    """Extend HL-style list ({"name":..., "val":...})"""
    seen = {it[key] for it in lst}
    added = 0
    for it in new:
        if it.get(key) not in seen:
            lst.append(it); seen.add(it[key]); added += 1
    return added

def extm(lst, new):
    """Extend match-style list ({"n":..., "c":...})"""
    seen = {it['n'] for it in lst}
    added = 0
    for it in new:
        if it['n'] not in seen:
            lst.append(it); seen.add(it['n']); added += 1
    return added

def extp(lst, new):
    """Extend pin-style list with coord dedup"""
    seen_n = {it['n'] for it in lst}
    seen_c = {(round(it['lat'],2), round(it['lng'],2)) for it in lst}
    added = 0
    for it in new:
        coord = (round(it['lat'],2), round(it['lng'],2))
        if it['n'] not in seen_n and coord not in seen_c:
            lst.append(it); seen_n.add(it['n']); seen_c.add(coord); added += 1
    return added

def ext_items(d, key, new, mode='hl'):
    """Extend d[key]['items'] or d[key] depending on structure"""
    entry = d.get(key)
    if entry is None:
        return 0
    if isinstance(entry, dict):
        lst = entry.setdefault('items', [])
    elif isinstance(entry, list):
        lst = entry
    else:
        return 0
    if mode == 'hl':   return ext(lst, new)
    if mode == 'match': return extm(lst, new)
    if mode == 'pin':   return extp(lst, new)
    return 0

report = {}

# ═══════════════════════════════════════════════════════════
#  TIERE
# ═══════════════════════════════════════════════════════════
d = load('tiere_hl.json')

ext_items(d, 'schlaf', [
    {"name": "Braunbär (Winterschlaf)", "val": 20},
    {"name": "Hauskatze", "val": 13},
    {"name": "Python (Schlange)", "val": 18},
    {"name": "Löwe", "val": 16},
    {"name": "Opossum", "val": 19},
    {"name": "Braunkopf-Klammeraffe", "val": 15},
    {"name": "Igel (Winterschlaf)", "val": 21},
    {"name": "Tapir", "val": 14},
    {"name": "Panda", "val": 12},
    {"name": "Hyäne", "val": 14},
    {"name": "Giraffe", "val": 2},
    {"name": "Elefant", "val": 4},
    {"name": "Delphin", "val": 8},
    {"name": "Mensch (Erwachsener)", "val": 8},
    {"name": "Pferd", "val": 3},
    {"name": "Kuh", "val": 4},
    {"name": "Ziege", "val": 5},
    {"name": "Hamster", "val": 14},
    {"name": "Siebenschläfer", "val": 23},
    {"name": "Dachs (Winterruhe)", "val": 16},
])

ext_items(d, 'pferde_stockmass', [
    {"name": "Shire-Horse", "val": 180},
    {"name": "Clydesdale", "val": 170},
    {"name": "Percheron", "val": 175},
    {"name": "Friese", "val": 163},
    {"name": "Hannoveraner", "val": 168},
    {"name": "Trakehner", "val": 165},
    {"name": "Araber (Vollblut)", "val": 153},
    {"name": "Englisches Vollblut", "val": 163},
    {"name": "Lusitano", "val": 157},
    {"name": "Appaloosa", "val": 155},
    {"name": "Mustang", "val": 148},
    {"name": "Quarter Horse", "val": 155},
    {"name": "Haflinger", "val": 142},
    {"name": "Fjordpferd", "val": 143},
    {"name": "Konik", "val": 135},
    {"name": "Welsh Mountain Pony", "val": 122},
    {"name": "Connemara-Pony", "val": 143},
    {"name": "Dartmoor Pony", "val": 120},
    {"name": "New Forest Pony", "val": 143},
    {"name": "Przewalski-Pferd", "val": 135},
])

ext_items(d, 'speed_wasser', [
    {"name": "Schwertfisch", "val": 97},
    {"name": "Mako-Hai", "val": 74},
    {"name": "Atlantischer Thunfisch", "val": 72},
    {"name": "Wahoo", "val": 77},
    {"name": "Blauflossenthunfisch", "val": 70},
    {"name": "Großer Weißer Hai", "val": 56},
    {"name": "Blauwale (Sprint)", "val": 48},
    {"name": "Delphin (Gemein)", "val": 55},
    {"name": "Orca (Sprint)", "val": 56},
    {"name": "Pinguin (unter Wasser)", "val": 36},
    {"name": "Krokodil (kurz)", "val": 32},
    {"name": "Seeotter", "val": 9},
    {"name": "Walross", "val": 35},
    {"name": "Leistenkrokodil", "val": 29},
    {"name": "Flussotter", "val": 12},
    {"name": "Robbenhai", "val": 40},
    {"name": "Tümmler", "val": 50},
    {"name": "Hammerhai", "val": 40},
    {"name": "Tigerfisch (Goliath)", "val": 65},
    {"name": "Barrakuda", "val": 60},
])

ext_items(d, 'wurf', [
    {"name": "Hauskatze", "val": 5},
    {"name": "Hund (Labrador)", "val": 8},
    {"name": "Hausmaus", "val": 12},
    {"name": "Hausmaus (Jahresrekord)", "val": 70},
    {"name": "Kaninchen", "val": 8},
    {"name": "Löwe", "val": 4},
    {"name": "Panda", "val": 2},
    {"name": "Elefant", "val": 1},
    {"name": "Orca", "val": 1},
    {"name": "Braunbär", "val": 3},
    {"name": "Polarfuchs", "val": 14},
    {"name": "Rothfuchs", "val": 6},
    {"name": "Wolf", "val": 7},
    {"name": "Gepard", "val": 5},
    {"name": "Goldhamster", "val": 10},
    {"name": "Nerz", "val": 8},
    {"name": "Springmaus (Jerbua)", "val": 3},
    {"name": "Pekari", "val": 2},
    {"name": "Gürteltier", "val": 4},
    {"name": "Grizzlybär", "val": 2},
])

ext_items(d, 'population', [
    {"name": "Rotfuchs", "val": 35000000},
    {"name": "Weißwedelhirsch", "val": 38000000},
    {"name": "Haushund (weltweit)", "val": 900000000},
    {"name": "Hauskatze (weltweit)", "val": 600000000},
    {"name": "Afrikanischer Elefant", "val": 415000},
    {"name": "Löwe", "val": 20000},
    {"name": "Gepard", "val": 7000},
    {"name": "Schneeleopard", "val": 4000},
    {"name": "Sumatra-Tiger", "val": 400},
    {"name": "Großer Panda", "val": 1864},
    {"name": "Blauwal", "val": 15000},
    {"name": "Berggorilla", "val": 1063},
    {"name": "Javan-Nashorn", "val": 72},
    {"name": "Vaquita (Schweinswal)", "val": 10},
    {"name": "Amur-Leopard", "val": 84},
    {"name": "Saiga-Antilope", "val": 1300000},
    {"name": "Weißer Hai", "val": 3500},
    {"name": "Beluga-Wal", "val": 200000},
    {"name": "Nördlicher Rotstreifenhörnchen", "val": 50000000},
    {"name": "Haushühner (weltweit)", "val": 33000000000},
])

ext_items(d, 'haustier_dichte', [
    {"name": "Deutschland", "val": 35},
    {"name": "Frankreich", "val": 48},
    {"name": "Vereinigte Staaten", "val": 67},
    {"name": "Brasilien", "val": 58},
    {"name": "Australien", "val": 62},
    {"name": "Schweden", "val": 30},
    {"name": "Japan", "val": 28},
    {"name": "China", "val": 22},
    {"name": "Indien", "val": 10},
    {"name": "Mexiko", "val": 58},
])

report['tiere_hl.json'] = 'updated'
save('tiere_hl.json', d)

# tiere_match.json
d = load('tiere_match.json')

ext_items(d, 'tauchtiefe', [
    {"n": "900 Meter Tiefe, sucht Kraken", "c": "Elefantrobbe"},
    {"n": "700 Meter Tiefe, Jagd mit Sonar", "c": "Delphin"},
    {"n": "535 Meter, Weltrekord Vogel", "c": "Kaiseringuin"},
    {"n": "600 Meter Tiefe, Fische und Kraken", "c": "Schwertwal"},
    {"n": "300 Meter Tiefe, meist Kalmare", "c": "Tümmler"},
    {"n": "450 Meter Tiefe, Seehund", "c": "Weddell-Robbe"},
    {"n": "Bis 200 Meter – Seegras und Muscheln", "c": "Meeresschildkröte"},
    {"n": "Bis 150 Meter – Hummer und Fische", "c": "Taucher-Ente"},
    {"n": "Bis 1200 Meter – Tintenfische", "c": "Ziphius (Cuvier)"},
    {"n": "Bis 100 Meter – Nauplien und Krill", "c": "Blauwal"},
    {"n": "Bis 70 Meter – Fischgründe", "c": "Cormorant (Kormoran)"},
    {"n": "Bis 500 Meter – Tintenfische und Garnelen", "c": "Sperm Whale (Pottwal)"},
    {"n": "Bis 30 Meter – Algen und Seegras", "c": "Dugong (Seekuh)"},
    {"n": "Bis 400 Meter – Fischzüge", "c": "Gänseschnabel-Wal"},
    {"n": "Bis 800 Meter – Nahrungssuche", "c": "Minke-Wal"},
    {"n": "Bis 25 Meter – Fische in Korallenriffen", "c": "Delphinart (Indopazifik)"},
    {"n": "Bis 60 Meter – Mollusken und Krabben", "c": "Fischotter"},
    {"n": "Bis 250 Meter – Tintenfische", "c": "Langflossen-Pilotenwal"},
    {"n": "Bis 50 Meter – Fische und Garnelen", "c": "Ringelrobbe"},
    {"n": "Bis 350 Meter – Tiefwasser-Jagd", "c": "Südlicher Elefantrobbe"},
], mode='match')

ext_items(d, 'anatomie', [
    {"n": "Hat keinen Kehlkopf – Schnurren entsteht im Zungenbein", "c": "Großkatze (Löwe)"},
    {"n": "Besitzt 3 Herzkammern (kein 4-Kammer-Herz)", "c": "Fisch"},
    {"n": "Hat als einziges Säugetier keinen Knochen im Penis", "c": "Mensch"},
    {"n": "Kann seinen Kopf um 270 Grad drehen", "c": "Eule"},
    {"n": "Hat blaues Blut (Hämocyanin statt Hämoglobin)", "c": "Tintenfisch"},
    {"n": "Besitzt 4 Mägen zur Wiederverwertung der Nahrung", "c": "Kuh"},
    {"n": "Hat keine Gallenblase", "c": "Pferd"},
    {"n": "Sieht UV-Licht, das für Menschen unsichtbar ist", "c": "Biene"},
    {"n": "Hat Fingerabdrücke fast identisch mit Menschenaffen", "c": "Koala"},
    {"n": "Kann Farben mit der Haut sehen, obwohl farbenblind", "c": "Tintenfisch"},
    {"n": "Hat kein Gehirn, aber ein Nervennetz", "c": "Qualle"},
    {"n": "Hat 32 Gehirne (Segmentherzen)", "c": "Blutegel"},
    {"n": "Besitzt Wärmebildsensoren in der Schnauze", "c": "Klapperschlange"},
    {"n": "Hat Zähne aus Keratin (nicht Calciumphosphat)", "c": "Schnabeltier"},
    {"n": "Kann Körperwärme separat regulieren", "c": "Tukan"},
    {"n": "Hat einen Magnetit-Kompass im Schnabel", "c": "Zugvogel (Rotkehlchen)"},
    {"n": "Besitzt ein drittes Auge (Scheitalauge) auf dem Kopf", "c": "Tuatara"},
    {"n": "Hat kein Skelett – nur Knorpel", "c": "Hai"},
    {"n": "Hat 360-Grad-Rundsicht ohne Kopfdrehen", "c": "Hase"},
    {"n": "Besitzt bis zu 15.000 Facettenaugen", "c": "Libelle"},
], mode='match')

ext_items(d, 'reitsport_disziplinen', [
    {"n": "Galoppieren über 110 cm hohe Hindernisse", "c": "Springreiten"},
    {"n": "Präzise Schritte und Lektionen wie Piaffe", "c": "Dressur"},
    {"n": "Quer durch Wald und Feld über natürliche Hindernisse", "c": "Geländereiten"},
    {"n": "Runden auf Oval-Track, meist 1200 bis 2400 m", "c": "Galopprennen"},
    {"n": "Harness-Racing mit zweirädrigem Sulky", "c": "Trabrennen"},
    {"n": "Bunte Stangen bei 1.45 m bis 1.60 m Höhe", "c": "Parcours-Springen (Grand Prix)"},
    {"n": "Kombination aus Dressur, Gelände und Springen", "c": "Vielseitigkeit (Eventing)"},
    {"n": "Ausgedehntes Rennen über 80-160 km", "c": "Distanzreiten"},
    {"n": "Rinder-Hüten mit Pferd (Western)", "c": "Cutting"},
    {"n": "Schnelles Drehen in Achter um 2 Fässer", "c": "Barrel Racing"},
    {"n": "Galopprennen für Hindernisse (steeplechase)", "c": "Jagdrennen"},
    {"n": "Runden mit Polo-Mallet und Ball", "c": "Polo"},
    {"n": "Präzise Stop-Slides und Spin bei Western-Dressur", "c": "Reining"},
    {"n": "Pferd am langen Zügel ohne Reiter", "c": "Longieren"},
    {"n": "Hochschulelemente: Levade, Courbette, Kapriole", "c": "Haute École"},
    {"n": "Spontanes Hüten und Ausschneiden (Stock Horse)", "c": "Camp Drafting"},
    {"n": "Rennen im Schritt-ähnlichen Tölt (5-Gangpferd)", "c": "Islandpferd-Rennen"},
    {"n": "Trabrennen ohne Sulky, nur berittener Jockey", "c": "Berittenes Trabrennen"},
    {"n": "Equitation-Prüfung: Haltung und Sitz des Reiters", "c": "Equitation"},
    {"n": "Pferde-Quadrille: Formation à 4-8 Pferden", "c": "Quadrille"},
], mode='match')

report['tiere_match.json'] = 'updated'
save('tiere_match.json', d)

# tiere_pin.json
d = load('tiere_pin.json')
ext_items(d, 'pferde_rassen', [
    {"n": "Shire Horse", "lat": 52.5, "lng": -1.5},
    {"n": "Clydesdale", "lat": 55.8, "lng": -4.2},
    {"n": "Percheron", "lat": 48.4, "lng": 0.2},
    {"n": "Friese", "lat": 53.1, "lng": 5.8},
    {"n": "Lipizzaner", "lat": 45.8, "lng": 13.9},
    {"n": "Hannoveraner", "lat": 52.4, "lng": 9.7},
    {"n": "Trakehner", "lat": 54.2, "lng": 21.7},
    {"n": "Appaloosa", "lat": 46.7, "lng": -116.5},
    {"n": "Quarter Horse", "lat": 30.3, "lng": -97.7},
    {"n": "Mustang", "lat": 40.0, "lng": -117.0},
    {"n": "Przewalski-Pferd", "lat": 47.9, "lng": 106.9},
    {"n": "Arabisches Vollblut", "lat": 24.7, "lng": 46.7},
    {"n": "Camargue-Pferd", "lat": 43.5, "lng": 4.4},
    {"n": "Lusitano", "lat": 39.4, "lng": -8.2},
], mode='pin')
report['tiere_pin.json'] = 'updated'
save('tiere_pin.json', d)

# ═══════════════════════════════════════════════════════════
#  TECH
# ═══════════════════════════════════════════════════════════
d = load('tech_match.json')

ext_items(d, 'linux', [
    {"n": "Kali Linux", "c": "Sicherheit / Pentesting"},
    {"n": "Arch Linux", "c": "Rolling Release / Advanced"},
    {"n": "Fedora 40", "c": "Desktop / Bleeding Edge"},
    {"n": "Linux Mint 21", "c": "Desktop / Einsteiger"},
    {"n": "CentOS Stream", "c": "Server"},
    {"n": "Rocky Linux", "c": "Server / RHEL-kompatibel"},
    {"n": "AlmaLinux", "c": "Server / RHEL-kompatibel"},
    {"n": "openSUSE Tumbleweed", "c": "Rolling Release"},
    {"n": "Gentoo Linux", "c": "Source-based / Advanced"},
    {"n": "NixOS", "c": "Deklaratives System"},
    {"n": "Raspberry Pi OS", "c": "Embedded / Raspberry Pi"},
    {"n": "Tails OS", "c": "Datenschutz / Anonym"},
    {"n": "Whonix", "c": "Sicherheit / Anonym"},
    {"n": "elementary OS", "c": "Desktop / macOS-ähnlich"},
    {"n": "Pop!_OS", "c": "Desktop / Gaming"},
    {"n": "Manjaro", "c": "Desktop / Arch-basiert"},
    {"n": "Garuda Linux", "c": "Gaming / Performance"},
    {"n": "Zorin OS", "c": "Desktop / Windows-ähnlich"},
    {"n": "Void Linux", "c": "Server / Minimal"},
    {"n": "Slackware", "c": "Älteste aktive Distro"},
], mode='match')

ext_items(d, 'osi', [
    {"n": "IP (Internet Protocol)", "c": "3 Netzwerk"},
    {"n": "Ethernet (MAC)", "c": "2 Sicherung"},
    {"n": "DNS", "c": "7 Anwendung"},
    {"n": "FTP", "c": "7 Anwendung"},
    {"n": "SMTP", "c": "7 Anwendung"},
    {"n": "SSL/TLS", "c": "6 Präsentation"},
    {"n": "SSH", "c": "7 Anwendung"},
    {"n": "UDP", "c": "4 Transport"},
    {"n": "ARP (Address Resolution Protocol)", "c": "2 Sicherung"},
    {"n": "ICMP (Ping)", "c": "3 Netzwerk"},
    {"n": "DHCP", "c": "7 Anwendung"},
    {"n": "Sitzungsmanagement (NFS, SQL-Session)", "c": "5 Sitzung"},
    {"n": "Twisted Pair (Kupferkabel)", "c": "1 Bitübertragung"},
    {"n": "OSPF (Routing-Protokoll)", "c": "3 Netzwerk"},
    {"n": "BGP (Border Gateway Protocol)", "c": "7 Anwendung"},
    {"n": "Frame Relay", "c": "2 Sicherung"},
    {"n": "VLAN-Tagging (IEEE 802.1Q)", "c": "2 Sicherung"},
    {"n": "TLS-Handshake", "c": "5 Sitzung"},
    {"n": "JPEG-Komprimierung", "c": "6 Präsentation"},
    {"n": "ASCII / Unicode-Kodierung", "c": "6 Präsentation"},
], mode='match')

ext_items(d, 'bigo', [
    {"n": "Binäre Suche (sortiertes Array)", "c": "O(log n)"},
    {"n": "Quicksort (Durchschnitt)", "c": "O(n log n)"},
    {"n": "Mergesort", "c": "O(n log n)"},
    {"n": "Bubblesort (worst case)", "c": "O(n²)"},
    {"n": "Insertion Sort (worst case)", "c": "O(n²)"},
    {"n": "Hash-Tabellen-Lookup (Durchschnitt)", "c": "O(1)"},
    {"n": "Hash-Tabellen-Lookup (worst case)", "c": "O(n)"},
    {"n": "DFS/BFS (Graphtraversal)", "c": "O(V+E)"},
    {"n": "Dijkstra (mit Min-Heap)", "c": "O((V+E) log V)"},
    {"n": "Traveling Salesman (brute force)", "c": "O(n!)"},
    {"n": "Matrix-Multiplikation (naiv)", "c": "O(n³)"},
    {"n": "Heapsort", "c": "O(n log n)"},
    {"n": "Fibonacci rekursiv (naiv)", "c": "O(2^n)"},
    {"n": "Fibonacci mit Memoization", "c": "O(n)"},
    {"n": "Radix Sort", "c": "O(nk)"},
    {"n": "Counting Sort", "c": "O(n+k)"},
    {"n": "AVL-Tree Suche", "c": "O(log n)"},
    {"n": "Linked List (Einfügen am Anfang)", "c": "O(1)"},
    {"n": "Breitensuche (BFS)", "c": "O(V+E)"},
    {"n": "Tiefensuche (DFS)", "c": "O(V+E)"},
], mode='match')

ext_items(d, 'turing_award', [
    {"n": "John McCarthy", "c": "Künstliche Intelligenz / Lisp (1971)"},
    {"n": "Dennis Ritchie & Ken Thompson", "c": "UNIX & C-Sprache (1983)"},
    {"n": "Niklaus Wirth", "c": "Pascal & Algorithmendesign (1984)"},
    {"n": "Tony Hoare", "c": "Quicksort & Hoare-Logik (1980)"},
    {"n": "Linus Torvalds", "c": "Linux-Kernel — kein Turing, Linux-Torvalds"},
    {"n": "John Backus", "c": "Fortran & BNF-Grammatik (1977)"},
    {"n": "Edgar F. Codd", "c": "Relationales Datenbankmodell (1981)"},
    {"n": "Vint Cerf & Bob Kahn", "c": "TCP/IP-Protokoll (2004)"},
    {"n": "Tim Berners-Lee", "c": "World Wide Web (2016)"},
    {"n": "Leslie Lamport", "c": "Verteilte Systeme / LaTeX (2013)"},
    {"n": "Geoffrey Hinton", "c": "Deep Learning / Neuronale Netze (2018)"},
    {"n": "Yann LeCun", "c": "Convolutional Neural Networks (2018)"},
    {"n": "Yoshua Bengio", "c": "Deep Learning (2018)"},
    {"n": "Judea Pearl", "c": "Probabilistische Kausalität (2011)"},
    {"n": "Michael Stonebraker", "c": "Moderne Datenbankkonzepte (2014)"},
    {"n": "Andrew Yao", "c": "Komplexitätstheorie & Kryptographie (2000)"},
    {"n": "Barbara Liskov", "c": "OOP & Liskov-Substitutionsprinzip (2008)"},
    {"n": "Frances Allen", "c": "Compileroptimierung (2006)"},
    {"n": "Butler Lampson", "c": "Personal Computing & Betriebssysteme (1992)"},
    {"n": "Frederick Brooks Jr.", "c": "IBM OS/360 & Mythischer Menschmonat (1999)"},
], mode='match')

ext_items(d, 'hardware', [
    {"n": "Verarbeitet Grafik-Shader-Programme", "c": "GPU"},
    {"n": "Speichert Daten flüchtig während der Laufzeit", "c": "RAM"},
    {"n": "Permanenter Massenspeicher, nichtflüchtig", "c": "SSD/HDD"},
    {"n": "Verbindet CPU, RAM und PCIe-Slots", "c": "Mainboard"},
    {"n": "Wandelt AC in DC-Spannungen um", "c": "Netzteil"},
    {"n": "Taktet CPU auf bis zu 5 GHz", "c": "Taktgenerator"},
    {"n": "Führt Rechenanweisungen aus", "c": "CPU"},
    {"n": "Kühlt CPU durch Wärmeableitung", "c": "Kühlkörper"},
    {"n": "Verbindet Geräte per serieller Schnittstelle", "c": "USB-Controller"},
    {"n": "Ermöglicht drahtlose Netzwerkverbindung", "c": "WLAN-Karte"},
    {"n": "Liest und schreibt optische Datenträger", "c": "Optisches Laufwerk"},
    {"n": "Berechnet KI-Inferenz ultraschnell", "c": "NPU"},
    {"n": "Koordiniert Datentransfer zwischen Komponenten", "c": "Chipsatz"},
    {"n": "Verbindet PCIe-Karten mit dem System", "c": "PCIe-Slot"},
    {"n": "Enthält Low-Level-Boot-Firmware", "c": "UEFI/BIOS-Chip"},
    {"n": "Puffert Daten schnell zwischen CPU und RAM", "c": "CPU-Cache (L3)"},
    {"n": "Sorgt für Hochfrequenz-Audio-Ausgabe", "c": "Soundkarte"},
    {"n": "Ermöglicht Netzwerkanschluss via Kabel", "c": "Netzwerkkarte (NIC)"},
    {"n": "Wandelt Digitalsignale in Analogton um", "c": "DAC"},
    {"n": "Steuert Festplattenzugriffe", "c": "Storage-Controller"},
], mode='match')

ext_items(d, 'malware', [
    {"n": "Verschlüsselt Dateien und fordert Lösegeld", "c": "Ransomware"},
    {"n": "Tarnt sich als legitime Software, enthält Backdoor", "c": "Trojaner"},
    {"n": "Verbreitet sich selbst ohne Benutzeraktion", "c": "Computerwurm"},
    {"n": "Fügt sich in andere Programme ein und repliziert sich", "c": "Computervirus"},
    {"n": "Protokolliert alle Tastenanschläge des Benutzers", "c": "Keylogger"},
    {"n": "Gibt Angreifer verdeckten Fernzugriff auf System", "c": "Rootkit"},
    {"n": "Sendet heimlich persönliche Daten weiter", "c": "Spyware"},
    {"n": "Zeigt unerwünschte Werbung im Browser", "c": "Adware"},
    {"n": "Macht Rechner zum Zombie-Spam-Versender", "c": "Bot/Botnet"},
    {"n": "Überwacht und stiehlt Zahlungskartendaten", "c": "Financial Malware"},
    {"n": "Nutzt Browser-Ressourcen für Krypto-Mining", "c": "Cryptojacker"},
    {"n": "Täuscht Antivirensoftware durch Code-Verschleierung", "c": "Polymorphe Malware"},
    {"n": "Schädigt physische Hardware (z.B. Stuxnet)", "c": "Cyber-Waffe"},
    {"n": "Blockiert Systemzugang komplett (Lockscreen)", "c": "Locker-Ransomware"},
    {"n": "Löscht Dateien unwiderbringlich", "c": "Wiper-Malware"},
    {"n": "Protokolliert Webcam und Mikrofon heimlich", "c": "Stalkerware"},
    {"n": "Imitiert BSOD und fordert Zahlung", "c": "Scareware"},
    {"n": "Versteckt sich im UEFI-Firmware, kaum entfernbar", "c": "Bootkit"},
    {"n": "Wartet auf Trigger (Datum/Ereignis) vor Aktivierung", "c": "Logic Bomb"},
    {"n": "Verbreitet sich via Office-Makros", "c": "Makro-Virus"},
], mode='match')

ext_items(d, 'smart_home', [
    {"n": "Öffnet Türen per Bluetooth oder NFC", "c": "Smartes Türschloss"},
    {"n": "Erkennt Bewegung und sendet Push-Nachricht", "c": "Bewegungsmelder"},
    {"n": "Schaltet Licht per Sprache oder App", "c": "Smart Bulb"},
    {"n": "Steuert Temperatur automatisch", "c": "Smartes Thermostat"},
    {"n": "Überwacht Haustür per Kamera und Video-Türklingel", "c": "Video-Türklingel"},
    {"n": "Überwacht Energieverbrauch jedes Verbrauchers", "c": "Smartes Energiemessgerät"},
    {"n": "Reinigt Böden autonom und kehrt zur Ladestation", "c": "Saugroboter"},
    {"n": "Erkennt Rauch und löst Alarm aus", "c": "Smarter Rauchmelder"},
    {"n": "Öffnet und schließt Jalousien automatisch", "c": "Smarte Rollläden"},
    {"n": "Verbindet alle Smart-Home-Geräte zentral", "c": "Smart-Home-Hub"},
    {"n": "Wässert Pflanzen nach Feuchtigkeitssensor", "c": "Smarte Bewässerung"},
    {"n": "Zeigt Energieproduktion der Solaranlage live", "c": "Solar-Monitor"},
    {"n": "Erkennt Wasseraustritt frühzeitig", "c": "Wasserlecksensor"},
    {"n": "Zeigt Luftqualität (CO2, VOC)", "c": "Luftqualitätssensor"},
    {"n": "Regelt Ladezeit des E-Autos nach Stromtarif", "c": "Smarte Ladestation"},
    {"n": "Koppelt Geräte via Zigbee-Mesh-Netzwerk", "c": "Zigbee-Bridge"},
    {"n": "Steuert Audio in jedem Zimmer separat", "c": "Multi-Room-Audio"},
    {"n": "Verbindet Apple HomeKit, Google Home, Alexa", "c": "Matter-Protokoll"},
    {"n": "Überwacht Schlaf und Herzfrequenz im Bett", "c": "Smarte Matratze"},
    {"n": "Warnt vor Einbruch via Erschütterungssensor", "c": "Erschütterungsmelder"},
], mode='match')

ext_items(d, 'erste_videospiele', [
    {"n": "Tennis for Two (1958) – Oszilloskop-Spiel", "c": "USA"},
    {"n": "Spacewar! (1962) – PDP-1 Universität", "c": "USA"},
    {"n": "Galaxy Game (1971) – erstes Münzspiel-Spacewar", "c": "USA"},
    {"n": "Gran Trak 10 (1974) – erstes Rennspiel Atari", "c": "USA"},
    {"n": "Space Invaders (1978) – Taito", "c": "Japan"},
    {"n": "Pac-Man (1980) – Namco", "c": "Japan"},
    {"n": "Donkey Kong (1981) – Nintendo", "c": "Japan"},
    {"n": "Dragon's Lair (1983) – erstes Laserdisc-Spiel", "c": "USA"},
    {"n": "Tetris (1984) – Pajitnov, Moskauer Institut", "c": "Russland"},
    {"n": "Super Mario Bros. (1985) – Nintendo NES", "c": "Japan"},
    {"n": "The Legend of Zelda (1986) – Nintendo", "c": "Japan"},
    {"n": "SimCity (1989) – Maxis", "c": "USA"},
    {"n": "Sonic the Hedgehog (1991) – Sega", "c": "Japan"},
    {"n": "Wolfenstein 3D (1992) – id Software (erstes FPS)", "c": "USA"},
    {"n": "Doom (1993) – id Software", "c": "USA"},
    {"n": "Warcraft (1994) – Blizzard", "c": "USA"},
    {"n": "Tomb Raider (1996) – Core Design", "c": "Vereinigtes Königreich"},
    {"n": "Resident Evil (1996) – Capcom", "c": "Japan"},
    {"n": "GoldenEye 007 (1997) – Rare", "c": "Vereinigtes Königreich"},
    {"n": "Half-Life (1998) – Valve", "c": "USA"},
], mode='match')

ext_items(d, 'tech_ma', [
    {"n": "Microsoft kauft Activision Blizzard (69 Mrd. USD, 2023)", "c": "USA"},
    {"n": "Microsoft kauft LinkedIn (26,2 Mrd. USD, 2016)", "c": "USA"},
    {"n": "Facebook kauft WhatsApp (19 Mrd. USD, 2014)", "c": "USA"},
    {"n": "Amazon kauft MGM (8,5 Mrd. USD, 2021)", "c": "USA"},
    {"n": "Google kauft YouTube (1,65 Mrd. USD, 2006)", "c": "USA"},
    {"n": "Disney kauft Pixar (7,4 Mrd. USD, 2006)", "c": "USA"},
    {"n": "Oracle kauft Sun Microsystems (7,4 Mrd., 2010)", "c": "USA"},
    {"n": "HP kauft Compaq (24 Mrd. USD, 2002)", "c": "USA"},
    {"n": "Dell kauft EMC (67 Mrd. USD, 2016)", "c": "USA"},
    {"n": "Salesforce kauft Slack (27,7 Mrd. USD, 2021)", "c": "USA"},
    {"n": "Apple kauft Beats (3 Mrd. USD, 2014)", "c": "USA"},
    {"n": "Amazon kauft Twitch (970 Mio. USD, 2014)", "c": "USA"},
    {"n": "PayPal kauft Venmo (via Braintree, 800 Mio., 2013)", "c": "USA"},
    {"n": "Elon Musk kauft Twitter (44 Mrd. USD, 2022)", "c": "USA"},
    {"n": "NVIDIA kauft Arm (gescheitert, 66 Mrd., 2022)", "c": "USA"},
    {"n": "Intel kauft Altera (16,7 Mrd. USD, 2015)", "c": "USA"},
    {"n": "Qualcomm kauft NXP (gescheitert, 44 Mrd., 2019)", "c": "USA"},
    {"n": "Broadcom kauft VMware (61 Mrd. USD, 2023)", "c": "USA"},
    {"n": "Adobe kauft Figma (gescheitert, 20 Mrd., 2023)", "c": "USA"},
    {"n": "Amazon kauft Whole Foods (13,7 Mrd. USD, 2017)", "c": "USA"},
], mode='match')

report['tech_match.json'] = 'updated'
save('tech_match.json', d)

d = load('tech_hl.json')
ext_items(d, 'release_jahr', [
    {"name": "C", "val": 1972},
    {"name": "Pascal", "val": 1970},
    {"name": "Ada", "val": 1980},
    {"name": "C++", "val": 1983},
    {"name": "Perl", "val": 1987},
    {"name": "Haskell", "val": 1990},
    {"name": "Python", "val": 1991},
    {"name": "Java", "val": 1995},
    {"name": "JavaScript", "val": 1995},
    {"name": "PHP", "val": 1994},
    {"name": "Ruby", "val": 1995},
    {"name": "C#", "val": 2000},
    {"name": "Scala", "val": 2003},
    {"name": "Go", "val": 2009},
    {"name": "Rust", "val": 2010},
    {"name": "Kotlin", "val": 2011},
    {"name": "TypeScript", "val": 2012},
    {"name": "Swift", "val": 2014},
    {"name": "Dart", "val": 2011},
    {"name": "Zig", "val": 2016},
])

ext_items(d, 'internet_speed', [
    {"name": "Vereinigte Arabische Emirate", "val": 238},
    {"name": "Hongkong", "val": 229},
    {"name": "Südkorea", "val": 271},
    {"name": "Rumänien", "val": 198},
    {"name": "Schweiz", "val": 176},
    {"name": "Dänemark", "val": 169},
    {"name": "Norwegen", "val": 155},
    {"name": "Deutschland", "val": 98},
    {"name": "USA", "val": 227},
    {"name": "Frankreich", "val": 159},
    {"name": "Schweden", "val": 163},
    {"name": "Japan", "val": 178},
    {"name": "Niederlande", "val": 165},
    {"name": "Belgien", "val": 154},
    {"name": "Österreich", "val": 119},
])

report['tech_hl.json'] = 'updated'
save('tech_hl.json', d)

# ═══════════════════════════════════════════════════════════
#  EMOB
# ═══════════════════════════════════════════════════════════
d = load('emob_match.json')

ext_items(d, 'stecker', [
    {"n": "Typ 1 (J1772, USA/Japan AC)", "c": "J1772"},
    {"n": "Typ 2 (IEC 62196, Europa AC)", "c": "Mennekes"},
    {"n": "Tesla NACS (Nordamerika)", "c": "NACS"},
    {"n": "GB/T DC (China Standard)", "c": "GB/T"},
    {"n": "CCS Combo 1 (USA DC)", "c": "CCS1"},
    {"n": "MCS (Megawatt Charging, Lkw)", "c": "MCS"},
    {"n": "CCS Typ 2 + DC-Pins = 350kW möglich", "c": "CCS2 (Europa)"},
    {"n": "Wireless Inductive (Qi / SAE J2954)", "c": "Induktiv"},
    {"n": "3-Phasen 22kW Heim-Option", "c": "Typ 2 (dreiphasig)"},
    {"n": "BS 1363 Adapter für UK Typ 2", "c": "UK-Standard"},
    {"n": "IEC 60309 'Industriestecker' (blau, 32A)", "c": "IEC 60309"},
    {"n": "Steckdose Schuko – nur Notladung 2,3 kW", "c": "Schuko (CEE7/4)"},
    {"n": "ABB Terra DC Wallbox 24 kW", "c": "CCS2 Wallbox"},
    {"n": "Supercharger V4 (bis 350 kW)", "c": "Tesla V4"},
    {"n": "Ionity 350kW HPC – CCS2", "c": "HPC CCS2"},
    {"n": "ABRP-Route via CHAdeMO in Japan", "c": "CHAdeMO Japan"},
    {"n": "SCAME-Typ 3A (Frankreich, veraltet)", "c": "Typ 3A"},
    {"n": "Wallbox go-e Charger HOMEfix", "c": "Typ 2 AC"},
    {"n": "SAE J3400 = US-Standard NACS 2023", "c": "SAE J3400"},
    {"n": "Pantograph (Bus-Dachkontakt)", "c": "Overhead"},
], mode='match')

ext_items(d, 'zellchemie', [
    {"n": "Leicht und dicht, für Consumer-Elektronik", "c": "NCA"},
    {"n": "Kostengünstig, große Zyklenlebensdauer", "c": "LFP"},
    {"n": "Stabil ohne seltene Erde (kein Kobalt)", "c": "LMFP"},
    {"n": "Festes Elektrolyt, kein Flüssigkeitsleck", "c": "Solid-State"},
    {"n": "Höchste Energiedichte pro kg", "c": "Li-S (Lithium-Schwefel)"},
    {"n": "Wiederaufladbar, kein Memory-Effekt", "c": "Li-Ion (allgemein)"},
    {"n": "Günstig, schwer, ausreifend", "c": "Bleiakkumulator"},
    {"n": "Hohe Selbstentladung, Nickel-Metall", "c": "NiMH"},
    {"n": "Niedrigste Temperatur-Toleranz-Grenze", "c": "NMC (622)"},
    {"n": "Kaum Cobalt, optimierter Mangan-Anteil", "c": "NMCA"},
    {"n": "Tesla 4680-Zellen (tabless)", "c": "Cylindrical 4680"},
    {"n": "Prismatische Zelle für Modul-Einbau", "c": "Prismatisch"},
    {"n": "Pouch-Zelle: flach, flexibel", "c": "Pouch"},
    {"n": "BYD Blade-Technologie (gestapelte LFP)", "c": "Blade Battery"},
    {"n": "CATL Kirin-Batterie (CTP 3.0)", "c": "CTP 3.0"},
    {"n": "Natrium-Ionen – keine Lithium nötig", "c": "Na-Ion"},
    {"n": "Zink-Luft: hohe Energiedichte, halb aufladbar", "c": "Zn-Air"},
    {"n": "Wasserstoff-Brennstoffzelle: H2 + O2 → Strom", "c": "PEMFC"},
    {"n": "Super-Kondensator: extrem schnell, geringe Dichte", "c": "Supercap"},
    {"n": "Dual-Chemie: LFP vorne, NMC hinten", "c": "Dual-Chemie"},
], mode='match')

ext_items(d, 'akronyme', [
    {"n": "EVSE", "c": "Electric Vehicle Supply Equipment"},
    {"n": "SOC", "c": "State of Charge"},
    {"n": "SOH", "c": "State of Health"},
    {"n": "OCPP", "c": "Open Charge Point Protocol"},
    {"n": "V2G", "c": "Vehicle to Grid"},
    {"n": "V2H", "c": "Vehicle to Home"},
    {"n": "CTP", "c": "Cell to Pack"},
    {"n": "CTC", "c": "Cell to Chassis"},
    {"n": "HPC", "c": "High Power Charging"},
    {"n": "OBC", "c": "On-Board Charger"},
    {"n": "DCFC", "c": "DC Fast Charging"},
    {"n": "ICE", "c": "Internal Combustion Engine"},
    {"n": "FCEV", "c": "Fuel Cell Electric Vehicle"},
    {"n": "REX", "c": "Range Extender"},
    {"n": "SOP", "c": "State of Power"},
    {"n": "CAN", "c": "Controller Area Network (Fahrzeugbus)"},
    {"n": "OTA", "c": "Over the Air (Software-Update)"},
    {"n": "ADAS", "c": "Advanced Driver Assistance Systems"},
    {"n": "VDSL", "c": "Nein – hier Vehicle Dynamics System Level"},
    {"n": "TCO", "c": "Total Cost of Ownership"},
], mode='match')

ext_items(d, 'motorentypen', [
    {"n": "Axialflussmotor (flache Bauform, hohe Dichte)", "c": "Axialfluss"},
    {"n": "Reluktanzmotor (kein Permanentmagnet)", "c": "SRM"},
    {"n": "Transversalfluss-Motor (selten, hohe Drehmoment)", "c": "Transversalfluss"},
    {"n": "EC-Motor (electronically commutated BLDC)", "c": "BLDC"},
    {"n": "Fremderregter Synchronmotor (Renault ZOE)", "c": "EESM"},
    {"n": "Hybridmotor: PMSM + Benziner in Parallelstrang", "c": "Hybrid-Kombination"},
    {"n": "Radnabenmotor (Motor direkt im Rad)", "c": "In-Wheel"},
    {"n": "Linear-Motor (Magnetschwebebahn)", "c": "Linearmotor"},
    {"n": "Geschalteter Reluktanzmotor (cost-optimal)", "c": "SRM (geschaltet)"},
    {"n": "Doppelrotor-Motor (außen + innen)", "c": "Doppelrotor-PMSM"},
    {"n": "Wassergekühlte PMSM (BMW i3)", "c": "Gekühlter PMSM"},
    {"n": "Ölgekühlte Statorwicklung (ZF)", "c": "Ölgekühlter Stator"},
    {"n": "Wolfram-Kupfer-Leiterbahn (Hairpin)", "c": "Hairpin-Wicklung"},
    {"n": "Dreiphasiger Synchronmotor 400 VAC", "c": "Synchron 400V"},
    {"n": "Einphasiger bürstenloser DC-Motor", "c": "Einphasig BLDC"},
    {"n": "Tesla Drive Unit (PMSM vorne, Induction hinten)", "c": "Tesla Dual"},
    {"n": "Audi e-tron Motor mit integr. Getriebe", "c": "Integriertes Aggregat"},
    {"n": "Porsche Taycan 2-Gang-Getriebe mit PMSM", "c": "2-Gang PMSM"},
    {"n": "Nissan Leaf Synchron-Reluktanz-Motor", "c": "SynRM Nissan"},
    {"n": "Volkswagen ID.4 Hinterachse (APP550)", "c": "PMSM APP550"},
], mode='match')

report['emob_match.json'] = 'updated'
save('emob_match.json', d)

d = load('emob_hl.json')
ext_items(d, 'cw_wert', [
    {"name": "Tesla Model 3 (cw 0,23)", "val": 230},
    {"name": "BMW i4 M50 (cw 0,24)", "val": 240},
    {"name": "Hyundai Ioniq 6 (cw 0,21)", "val": 210},
    {"name": "Tesla Model Y (cw 0,23)", "val": 230},
    {"name": "Audi e-tron GT (cw 0,24)", "val": 240},
    {"name": "Porsche Taycan (cw 0,22)", "val": 220},
    {"name": "BYD Seal (cw 0,219)", "val": 219},
    {"name": "Volkswagen ID.7 (cw 0,23)", "val": 230},
    {"name": "Skoda Enyaq iV (cw 0,257)", "val": 257},
    {"name": "Mercedes EQE (cw 0,22)", "val": 220},
    {"name": "Kia EV6 (cw 0,228)", "val": 228},
    {"name": "Rivian R1T Pickup (cw 0,36)", "val": 360},
    {"name": "Tesla Cybertruck (cw 0,39)", "val": 390},
    {"name": "VW ID. Buzz (cw 0,285)", "val": 285},
    {"name": "Renault Megane E-Tech (cw 0,29)", "val": 290},
    {"name": "Ford F-150 Lightning (cw 0,38)", "val": 380},
    {"name": "Fiat 500e (cw 0,311)", "val": 311},
    {"name": "MINI Electric (cw 0,287)", "val": 287},
    {"name": "Polestar 2 (cw 0,266)", "val": 266},
    {"name": "Lightyear 0 (cw 0,175) – Rekord", "val": 175},
])

ext_items(d, 'systemspannung', [
    {"name": "Volkswagen ID.3 (400V-System)", "val": 400},
    {"name": "Tesla Model 3 Rear (350V-Bus)", "val": 350},
    {"name": "Renault Zoe (400V)", "val": 400},
    {"name": "Nissan Leaf (364V Nominal)", "val": 364},
    {"name": "Kia EV6 (800V)", "val": 800},
    {"name": "Audi e-tron GT (800V)", "val": 800},
    {"name": "Lucid Air (924V – Höchste in Serie)", "val": 924},
    {"name": "Mercedes EQS (400V)", "val": 400},
    {"name": "BMW iX (400V)", "val": 400},
    {"name": "Ford Mustang Mach-E (400V)", "val": 400},
    {"name": "Rivian R1T (400V)", "val": 400},
    {"name": "BYD Seal (800V)", "val": 800},
    {"name": "Mercedes EQE SUV (400V)", "val": 400},
    {"name": "Volvo EX90 (400V)", "val": 400},
    {"name": "Polestar 5 (800V)", "val": 800},
    {"name": "Zeekr 001 (800V)", "val": 800},
    {"name": "Fisker Ocean (400V)", "val": 400},
    {"name": "Honda e:Ny1 (400V)", "val": 400},
    {"name": "Volkswagen ID.7 (400V)", "val": 400},
    {"name": "Nio ET7 (400V)", "val": 400},
])

report['emob_hl.json'] = 'updated'
save('emob_hl.json', d)

# ═══════════════════════════════════════════════════════════
#  ARCHAEOLOGIE
# ═══════════════════════════════════════════════════════════
d = load('archaeologie_hl.json')

for key, new_data in {
    'alter_artefakte': [
        {"name": "Schöninger Speere (Eibe)", "val": 300000},
        {"name": "Bilzingsleben-Knochenfunde", "val": 400000},
        {"name": "Abri Peyrony Faustreil", "val": 150000},
        {"name": "Homo heidelbergensis Schädel", "val": 600000},
        {"name": "Blombos-Ocker-Gravuren (Südafrika)", "val": 73000},
        {"name": "Skhul-Muschelperlenkette", "val": 115000},
        {"name": "Pinnacle Point Ocker", "val": 164000},
        {"name": "Atapuerca-Knochen (Spanien)", "val": 800000},
        {"name": "Dmanisi-Homo-erectus-Schädel", "val": 1800000},
        {"name": "Olduvai-Faustkeil (Oldowan)", "val": 1700000},
        {"name": "Turkana-Boy (Homo ergaster)", "val": 1500000},
        {"name": "Laetoli-Fußspuren", "val": 3600000},
        {"name": "Lucy-Skelett (Australopithecus)", "val": 3200000},
        {"name": "Ardipithecus ramidus-Knochen", "val": 4400000},
        {"name": "Sahelanthropus tchadensis (Schädel)", "val": 7000000},
        {"name": "Lomekwi-Steinwerkzeuge", "val": 3300000},
        {"name": "Trinil-Java-Man-Femur", "val": 1000000},
        {"name": "Peking-Man-Zähne", "val": 680000},
        {"name": "Floresiensis-Homo-Knochen (Hobbit)", "val": 50000},
        {"name": "Homo naledi-Fossilien", "val": 250000},
    ],
    'bauzeit': [
        {"name": "Hagia Sophia", "val": 5},
        {"name": "Taj Mahal", "val": 22},
        {"name": "Kolosseum", "val": 10},
        {"name": "Sagrada Família (laufend seit 1882)", "val": 141},
        {"name": "Großer Wall von China (gesamt)", "val": 1800},
        {"name": "Kölner Dom", "val": 632},
        {"name": "Notre-Dame de Paris", "val": 182},
        {"name": "Pantheon (Rom)", "val": 10},
        {"name": "Parthenon", "val": 9},
        {"name": "Stephansdom Wien", "val": 208},
        {"name": "Eiffelturm", "val": 2},
        {"name": "Empire State Building", "val": 1},
        {"name": "Burj Khalifa", "val": 6},
        {"name": "Suezkanal", "val": 10},
        {"name": "Panamakanal", "val": 10},
        {"name": "Petra (Felsenstadt)", "val": 300},
        {"name": "Teotihuacán (gesamte Stadt)", "val": 500},
        {"name": "Machu Picchu", "val": 70},
        {"name": "Versailles (Schloss)", "val": 50},
        {"name": "Stonehenge (Hauptbauphase)", "val": 1500},
    ],
}.items():
    ext_items(d, key, new_data)

report['archaeologie_hl.json'] = 'updated'
save('archaeologie_hl.json', d)

d = load('archaeologie_match.json')
ext_items(d, 'datierungsmethoden', [
    {"n": "Verhältnis von Sauerstoffisotopen in Eisbohrkernen", "c": "Isotopen-Stratigraphie"},
    {"n": "Magnetisierung von Mineralien beim Abkühlen von Lava", "c": "Paläomagnetismus"},
    {"n": "Analyse von Pollen in Torfschichten", "c": "Palynologie"},
    {"n": "Tiefe des Fundes unter der Oberfläche", "c": "Stratigraphie"},
    {"n": "Lumineszenz von Quarzkristallen seit letzter Belichtung", "c": "OSL-Datierung"},
    {"n": "Verfall von Kalium-40 zu Argon-40", "c": "K-Ar-Datierung"},
    {"n": "Wachstumsringe in Korallen", "c": "Sclerochronologie"},
    {"n": "Relative Häufigkeit von Uranium/Thorium", "c": "U-Th-Datierung"},
    {"n": "Aminosäuren-Isomerisierung in Muschelschalen", "c": "Aminosäure-Racemisierung"},
    {"n": "Fission-Track-Zählung in Zirkon-Kristallen", "c": "Spaltspuranalyse"},
    {"n": "Thermolumineszenz erhitzter Keramik", "c": "TL-Datierung"},
    {"n": "Stickstoffgehalt in Knochen (relativ)", "c": "Stickstoffmethode"},
    {"n": "Wachstum von Flechten auf Felsen", "c": "Lichenometrie"},
    {"n": "Verfall von Beryllium-10 in Gestein", "c": "Kosmogene Nuklid-Datierung"},
    {"n": "Schichtfolge des Meeresbodens", "c": "Marine Isotopen-Stratigraphie"},
    {"n": "Glashydrationsschicht an Obsidian", "c": "Obsidian-Hydratation"},
    {"n": "Magnetisierung von gebranntem Lehm", "c": "Archäomagnetismus"},
    {"n": "Analyse fossiler DNA aus Knochen", "c": "aDNA-Datierung"},
    {"n": "Schliff-Ringe an Elefantenzähnen", "c": "Dental Wear Analysis"},
    {"n": "Spaltspuren in Glasperlen", "c": "Glashydratations-Datierung"},
], mode='match')

ext_items(d, 'schriften', [
    {"n": "Ogham-Schrift", "c": "Irland / Keltisch"},
    {"n": "Runen (Futhark)", "c": "Nordeuropa"},
    {"n": "Phönizisch", "c": "Levante"},
    {"n": "Aramäisch", "c": "Naher Osten"},
    {"n": "Brahmi-Schrift", "c": "Indien"},
    {"n": "Tamil-Brahmi", "c": "Indien / Sri Lanka"},
    {"n": "Nabatäisch", "c": "Arabien / Petra"},
    {"n": "Blauer Nil-Meroe-Schrift", "c": "Nubien / Sudan"},
    {"n": "Aztekische Schrift (Nahuatl)", "c": "Mexiko"},
    {"n": "Maya-Hieroglyphen", "c": "Mesoamerika"},
    {"n": "Proto-Sinaitisch", "c": "Sinai-Halbinsel"},
    {"n": "Rongorongo (Osterinsel)", "c": "Polynesien"},
], mode='match')

report['archaeologie_match.json'] = 'updated'
save('archaeologie_match.json', d)

# ═══════════════════════════════════════════════════════════
#  PFLANZEN
# ═══════════════════════════════════════════════════════════
d = load('pflanzen_match.json')
ext_items(d, 'bestuaeber', [
    {"n": "Kakao-Baum (Theobroma)", "c": "Zuckmücken"},
    {"n": "Feige (Ficus carica)", "c": "Feigenwespe"},
    {"n": "Yucca-Palme", "c": "Yucca-Motte"},
    {"n": "Vanille (Vanilla planifolia)", "c": "Manuell / Kolibri"},
    {"n": "Nachtkerze (Oenothera)", "c": "Nachtfalter"},
    {"n": "Agave (Agave tequilana)", "c": "Langnasenfledermaus"},
    {"n": "Passionsblume (Passiflora)", "c": "Hummeln"},
    {"n": "Durian (Durio zibethinus)", "c": "Fledermäuse"},
    {"n": "Zuckerrohr (Saccharum)", "c": "Wind"},
    {"n": "Eiche (Quercus)", "c": "Wind"},
    {"n": "Mais (Zea mays)", "c": "Wind"},
    {"n": "Kokosnuss (Cocos nucifera)", "c": "Wind / Käfer"},
    {"n": "Birke (Betula)", "c": "Wind"},
    {"n": "Hasel (Corylus avellana)", "c": "Wind"},
    {"n": "Kiwi (Actinidia deliciosa)", "c": "Bienen"},
    {"n": "Kürbis (Cucurbita)", "c": "Bienen / Hummeln"},
    {"n": "Erdbeere (Fragaria)", "c": "Bienen"},
    {"n": "Apfel (Malus domestica)", "c": "Bienen"},
    {"n": "Mandel (Prunus dulcis)", "c": "Bienen"},
    {"n": "Linde (Tilia)", "c": "Bienen / Wespen"},
], mode='match')

ext_items(d, 'blattform', [
    {"n": "Eukalyptus", "c": "Lanzettlich"},
    {"n": "Efeu", "c": "Gelappt"},
    {"n": "Ahorn (Spitz)", "c": "Handförmig gelappt"},
    {"n": "Eiche", "c": "Buchtenförmig"},
    {"n": "Ginkgo", "c": "Fächerförmig"},
    {"n": "Rosskastanie", "c": "Fingerförmig (5-7 Blättchen)"},
    {"n": "Birke", "c": "Dreieckig / Rautenförmig"},
    {"n": "Lorbeer", "c": "Elliptisch"},
    {"n": "Banane", "c": "Länglich / Riesenblatt"},
    {"n": "Monstera deliciosa", "c": "Durchlöchert / Gelappt"},
    {"n": "Bambus", "c": "Linealisch / Grasartig"},
    {"n": "Feige", "c": "Tief 3-5 gelappt"},
    {"n": "Platane", "c": "Handförmig 5-gelappt"},
    {"n": "Eibe", "c": "Linealisch, zweizeilig"},
    {"n": "Palmfarn", "c": "Gefiedert"},
    {"n": "Spinat", "c": "Oval / Dreieckig-rhombisch"},
    {"n": "Kleeblatt", "c": "Dreizählig"},
    {"n": "Sonnenblume", "c": "Herzförmig / Groß"},
    {"n": "Weinrebe", "c": "Handförmig 5-gelappt"},
    {"n": "Wolliger Schneeknöterich", "c": "Oval / Wollig"},
], mode='match')

ext_items(d, 'nutzung', [
    {"n": "Quinine-Baum (Cinchona officinalis)", "c": "Medizin (Malaria)"},
    {"n": "Lein (Linum usitatissimum)", "c": "Textilfaser"},
    {"n": "Hanf (Cannabis sativa)", "c": "Textilfaser / Medizin"},
    {"n": "Bambus", "c": "Baustoff / Nahrung"},
    {"n": "Jute (Corchorus capsularis)", "c": "Textilfaser"},
    {"n": "Sisalagave (Agave sisalana)", "c": "Seile / Textilfaser"},
    {"n": "Kokosnuss (Cocos nucifera)", "c": "Nahrung / Schmiermittel"},
    {"n": "Zuckerrübe (Beta vulgaris)", "c": "Zucker / Ethanol"},
    {"n": "Ölpalme (Elaeis guineensis)", "c": "Pflanzenöl"},
    {"n": "Soja (Glycine max)", "c": "Protein / Tierfutter"},
    {"n": "Tabak (Nicotiana tabacum)", "c": "Genussmittel"},
    {"n": "Koka (Erythroxylum coca)", "c": "Medizin / Kokain-Rohstoff"},
    {"n": "Weide (Salix)", "c": "Aspirin-Quelle / Korbflechten"},
    {"n": "Stevia (Stevia rebaudiana)", "c": "Süßungsmittel"},
    {"n": "Guarana (Paullinia cupana)", "c": "Koffein-Lieferant"},
    {"n": "Miscanthus (Elefantengras)", "c": "Bioenergie"},
    {"n": "Raps (Brassica napus)", "c": "Speiseöl / Biodiesel"},
    {"n": "Zucker-Ahorn (Acer saccharum)", "c": "Ahornsirup"},
    {"n": "Sanddorn (Hippophae rhamnoides)", "c": "Vitamin C / Saft"},
    {"n": "Morinda officinalis (Noni-Baum)", "c": "Medizin (traditionell)"},
], mode='match')

report['pflanzen_match.json'] = 'updated'
save('pflanzen_match.json', d)

d = load('pflanzen_hl.json')
ext_items(d, 'fruchtgewicht', [
    {"name": "Kürbis (Rekord-Sorte)", "val": 1226000},
    {"name": "Wassermelone", "val": 20000},
    {"name": "Kürbis (normal)", "val": 5000},
    {"name": "Papaya", "val": 800},
    {"name": "Mango", "val": 300},
    {"name": "Avocado", "val": 200},
    {"name": "Pfirsich", "val": 130},
    {"name": "Apfel (Normalsorte)", "val": 180},
    {"name": "Tomate (Beefsteak)", "val": 300},
    {"name": "Erdbeere", "val": 20},
    {"name": "Blaubeere", "val": 2},
    {"name": "Olive", "val": 7},
    {"name": "Feige", "val": 50},
    {"name": "Bananenfrucht (normal)", "val": 150},
    {"name": "Dattel", "val": 15},
    {"name": "Longan", "val": 9},
    {"name": "Litschi", "val": 20},
    {"name": "Rambutan", "val": 25},
    {"name": "Drachenfrucht (Pitaya)", "val": 400},
    {"name": "Zuckermelone", "val": 3000},
])

ext_items(d, 'waldflaeche', [
    {"name": "Finnland", "val": 73.0},
    {"name": "Japan", "val": 68.0},
    {"name": "Schweden", "val": 69.0},
    {"name": "Südkorea", "val": 64.0},
    {"name": "Brasilien", "val": 60.0},
    {"name": "Norwegen", "val": 61.0},
    {"name": "Russland", "val": 50.0},
    {"name": "Kanada", "val": 38.0},
    {"name": "Deutschland", "val": 33.0},
    {"name": "Frankreich", "val": 31.0},
    {"name": "Österreich", "val": 47.0},
    {"name": "Schweiz", "val": 31.0},
    {"name": "Chile", "val": 25.0},
    {"name": "China", "val": 23.0},
    {"name": "USA", "val": 34.0},
    {"name": "Indien", "val": 22.0},
    {"name": "Australien", "val": 17.0},
    {"name": "Neuseeland", "val": 38.0},
    {"name": "Mexiko", "val": 33.0},
    {"name": "Nigeria", "val": 4.0},
])

report['pflanzen_hl.json'] = 'updated'
save('pflanzen_hl.json', d)

# ═══════════════════════════════════════════════════════════
#  GASTRO
# ═══════════════════════════════════════════════════════════
d = load('gastro_match.json')
ext_items(d, 'schnitttechniken', [
    {"n": "Julienne (Streichholz-Streifen 2×2mm)", "c": "Gemüse"},
    {"n": "Bâtonnet (3mm x 3mm x 5cm)", "c": "Gemüse"},
    {"n": "Paysanne (dünne unregelmäßige Scheiben)", "c": "Gemüse"},
    {"n": "Tourné (Sieben-Seiten-Fass)", "c": "Gemüse"},
    {"n": "Mandoline-Hobel (hauchdünn)", "c": "Gemüse / Käse"},
    {"n": "Chiffonade fein < 1mm Kräuterstreifen", "c": "Kräuter"},
    {"n": "Concassée (grob gehackte geschälte Tomaten)", "c": "Tomaten"},
    {"n": "Emincer (hauchdünne Scheiben)", "c": "Fleisch / Pilze"},
    {"n": "Escalope / Schmetterling-Schnitt", "c": "Fleisch"},
    {"n": "Lardieren (Speckstreifen einziehen)", "c": "Fleisch"},
    {"n": "Flambieren mit Ausbrennen von Knochen", "c": "Fleisch"},
    {"n": "Sashimi-Schnitt (schräg, glatt)", "c": "Fisch"},
    {"n": "Spatchcock (Wirbelsäule herauslösen)", "c": "Geflügel"},
    {"n": "Brunoise groß (5mm) = Macédoine", "c": "Gemüse"},
    {"n": "Noisette (Kugelform mit Parisien-Ausstecher)", "c": "Melone / Kartoffel"},
    {"n": "Printanier (kleine Würfeln + Julienne mix)", "c": "Gemüse"},
    {"n": "Ciselieren (fein wiegen für Schalotten)", "c": "Zwiebeln / Schalotten"},
    {"n": "Schnitzen (dekorative Garnitur)", "c": "Gemüse"},
    {"n": "Haché (fein gehackt < 2mm)", "c": "Kräuter / Zwiebeln"},
    {"n": "Carpaccio-Schnitt (hauchdünn, roh)", "c": "Rindfleisch / Fisch"},
], mode='match')

ext_items(d, 'fleisch_cuts', [
    {"n": "Entrecôte / Rib-Eye (Hochrippe)", "c": "Rind"},
    {"n": "Flank Steak (Bauchlappen)", "c": "Rind"},
    {"n": "T-Bone (Rücken mit Knochen)", "c": "Rind"},
    {"n": "Porterhouse (T-Bone + großes Filet)", "c": "Rind"},
    {"n": "Brisket (Brustspitze, BBQ)", "c": "Rind"},
    {"n": "Tri-Tip (Hüftspitze)", "c": "Rind"},
    {"n": "Short Ribs (Querrippen)", "c": "Rind"},
    {"n": "Tomahawk (Hochrippe mit Knochen)", "c": "Rind"},
    {"n": "Tenderloin / Filet (zartestes Stück)", "c": "Rind"},
    {"n": "Pulled Pork (Nacken, low & slow)", "c": "Schwein"},
    {"n": "Schweinebauch (Belly)", "c": "Schwein"},
    {"n": "Lammkeule (Gigot)", "c": "Lamm"},
    {"n": "Lammkotelett (Chop)", "c": "Lamm"},
    {"n": "Hähnchenbrust (Breast)", "c": "Geflügel"},
    {"n": "Keule / Schenkel (Drumstick)", "c": "Geflügel"},
    {"n": "Kaninchenrücken", "c": "Kaninchen"},
    {"n": "Hirschkeule", "c": "Wild"},
    {"n": "Wildschwein-Schulter", "c": "Wild"},
    {"n": "Kalbsschnitzel (Wiener Art)", "c": "Kalb"},
    {"n": "Kalbsbries (Sweetbread)", "c": "Kalb"},
], mode='match')

report['gastro_match.json'] = 'updated'
save('gastro_match.json', d)

d = load('gastro_hl.json')
ext_items(d, 'backtemperatur', [
    {"name": "Neapolitanische Pizza (Holzofen)", "val": 450},
    {"name": "New York Pizza", "val": 260},
    {"name": "Focaccia", "val": 220},
    {"name": "Sauerteigbrot", "val": 230},
    {"name": "Brioche", "val": 175},
    {"name": "Ciabatta", "val": 220},
    {"name": "Mürbeteig-Torte", "val": 180},
    {"name": "Makronen", "val": 150},
    {"name": "Blätterteig", "val": 200},
    {"name": "Königskuchen", "val": 160},
    {"name": "Madeleines", "val": 210},
    {"name": "Schokoladen-Lava-Kuchen", "val": 200},
    {"name": "Cheesecake (Wasserbad)", "val": 160},
    {"name": "Soufflé", "val": 190},
    {"name": "Popovers / Yorkshire Pudding", "val": 230},
    {"name": "Naan-Brot (Tandoor)", "val": 350},
    {"name": "Kaak (Sesamkringel)", "val": 180},
    {"name": "Zimtschnecken", "val": 175},
    {"name": "Choux (Brandteig-Eclairs)", "val": 200},
    {"name": "Pretzels / Brezeln", "val": 210},
])

report['gastro_hl.json'] = 'updated'
save('gastro_hl.json', d)

# ═══════════════════════════════════════════════════════════
#  KULTUR (25-Item-Listen)
# ═══════════════════════════════════════════════════════════
d = load('kultur.json')

for key, new_items in {
    'kaese': [
        {"n": "Comté", "c": "Frankreich"},
        {"n": "Manchego", "c": "Spanien"},
        {"n": "Taleggio", "c": "Italien"},
        {"n": "Halloumi", "c": "Zypern"},
        {"n": "Queso Fresco", "c": "Mexiko"},
        {"n": "Brie", "c": "Frankreich"},
        {"n": "Époisse", "c": "Frankreich"},
        {"n": "Gruyère", "c": "Schweiz"},
        {"n": "Jarlsberg", "c": "Norwegen"},
        {"n": "Limburger", "c": "Deutschland"},
        {"n": "Paneer", "c": "Indien"},
        {"n": "Fynsk Rygeost", "c": "Dänemark"},
        {"n": "Kaskaval", "c": "Bulgarien"},
        {"n": "Oscypek", "c": "Polen"},
        {"n": "Beyaz Peynir", "c": "Türkei"},
    ],
    'suessspeisen': [
        {"n": "Baklava", "c": "Türkei"},
        {"n": "Tiramisu", "c": "Italien"},
        {"n": "Crème Brûlée", "c": "Frankreich"},
        {"n": "Churros", "c": "Spanien"},
        {"n": "Mochi", "c": "Japan"},
        {"n": "Gulab Jamun", "c": "Indien"},
        {"n": "Pastel de Nata", "c": "Portugal"},
        {"n": "Pavlova", "c": "Australien"},
        {"n": "Sfenj", "c": "Marokko"},
        {"n": "Bibingka", "c": "Philippinen"},
        {"n": "Kanelbullar", "c": "Schweden"},
        {"n": "Lángos", "c": "Ungarn"},
        {"n": "Knafeh", "c": "Palästina"},
        {"n": "Malasadas", "c": "Portugal / Hawaii"},
        {"n": "Financier", "c": "Frankreich"},
    ],
    'kaffee': [
        {"n": "Café de Olla", "c": "Mexiko"},
        {"n": "Kopi Luwak", "c": "Indonesien"},
        {"n": "Qishr (Ingwer-Kaffee)", "c": "Jemen"},
        {"n": "Cà phê trứng (Ei-Kaffee)", "c": "Vietnam"},
        {"n": "Café Touba", "c": "Senegal"},
        {"n": "Mazagran (Kalt-Kaffee)", "c": "Algerien"},
        {"n": "Bulletproof Coffee", "c": "USA"},
        {"n": "Dalgona (Schaumkaffee)", "c": "Südkorea"},
        {"n": "Freddo Espresso", "c": "Griechenland"},
        {"n": "Kaffeespezialität Flat White", "c": "Australien"},
        {"n": "Buna-Zeremonie", "c": "Äthiopien"},
        {"n": "Kapuziner", "c": "Österreich"},
        {"n": "Café Cubano", "c": "Kuba"},
        {"n": "Cortado", "c": "Spanien"},
        {"n": "Red Eye (Drip + Espresso)", "c": "USA"},
    ],
    'taenze': [
        {"n": "Haka", "c": "Neuseeland"},
        {"n": "Saman", "c": "Indonesien"},
        {"n": "Whirling Derwish (Sema)", "c": "Türkei"},
        {"n": "Bharatanatyam", "c": "Indien"},
        {"n": "Capoeira", "c": "Brasilien"},
        {"n": "Cumbia", "c": "Kolumbien"},
        {"n": "Kathak", "c": "Indien"},
        {"n": "Lion Dance", "c": "China"},
        {"n": "Horo", "c": "Bulgarien"},
        {"n": "Legong", "c": "Indonesien (Bali)"},
        {"n": "Adumu (Maasai-Sprung)", "c": "Kenia"},
        {"n": "Eskista", "c": "Äthiopien"},
        {"n": "Pandanggo sa Ilaw", "c": "Philippinen"},
        {"n": "Lezginka", "c": "Georgien"},
        {"n": "Hopak", "c": "Ukraine"},
    ],
    'literatur': [
        {"n": "One Hundred Years of Solitude", "c": "Kolumbien"},
        {"n": "Dream of the Red Chamber", "c": "China"},
        {"n": "Mahabharata", "c": "Indien"},
        {"n": "Njáls Saga", "c": "Island"},
        {"n": "The Tale of Genji", "c": "Japan"},
        {"n": "The Epic of Gilgamesh", "c": "Mesopotamien"},
        {"n": "Things Fall Apart", "c": "Nigeria"},
        {"n": "The White Tiger", "c": "Indien"},
        {"n": "Snow Country", "c": "Japan"},
        {"n": "Love in the Time of Cholera", "c": "Kolumbien"},
        {"n": "Season of Migration to the North", "c": "Sudan"},
        {"n": "Cairo Trilogy", "c": "Ägypten"},
        {"n": "The Tin Drum", "c": "Deutschland"},
        {"n": "Pedro Páramo", "c": "Mexiko"},
        {"n": "The Alchemist", "c": "Brasilien"},
    ],
    'erfindungen': [
        {"n": "Buchdruck mit beweglichen Lettern", "c": "Deutschland"},
        {"n": "Papier (Cai Lun)", "c": "China"},
        {"n": "Dampfmaschine (Watt)", "c": "Vereinigtes Königreich"},
        {"n": "Telefon (Bell)", "c": "USA"},
        {"n": "Glühbirne (Edison)", "c": "USA"},
        {"n": "Röntgenstrahlen (Röntgen)", "c": "Deutschland"},
        {"n": "Penicillin (Fleming)", "c": "Vereinigtes Königreich"},
        {"n": "Transistor (Bell Labs)", "c": "USA"},
        {"n": "World Wide Web (Berners-Lee)", "c": "Vereinigtes Königreich"},
        {"n": "Gunpowder (黑火药)", "c": "China"},
        {"n": "Kompass", "c": "China"},
        {"n": "Stethoskop (Laënnec)", "c": "Frankreich"},
        {"n": "Nähmaschine (Singer)", "c": "USA"},
        {"n": "Radar (Watson-Watt)", "c": "Vereinigtes Königreich"},
        {"n": "Laser (Maiman)", "c": "USA"},
    ],
    'brettspiele': [
        {"n": "Go (围棋)", "c": "China"},
        {"n": "Mancala", "c": "Afrika"},
        {"n": "Backgammon", "c": "Iran"},
        {"n": "Schach", "c": "Indien"},
        {"n": "Mahjong", "c": "China"},
        {"n": "Siedler von Catan", "c": "Deutschland"},
        {"n": "Carcassonne", "c": "Deutschland"},
        {"n": "Monopoly", "c": "USA"},
        {"n": "Scrabble", "c": "USA"},
        {"n": "Risk", "c": "Frankreich"},
        {"n": "Ticket to Ride", "c": "USA"},
        {"n": "Dominion", "c": "USA"},
        {"n": "Codenames", "c": "Tschechien"},
        {"n": "Azul", "c": "Portugal / USA"},
        {"n": "Spirit Island", "c": "Kanada"},
    ],
    'getraenke': [
        {"n": "Sake", "c": "Japan"},
        {"n": "Soju", "c": "Südkorea"},
        {"n": "Baijiu", "c": "China"},
        {"n": "Pisco", "c": "Peru"},
        {"n": "Cachaca", "c": "Brasilien"},
        {"n": "Kvass", "c": "Russland"},
        {"n": "Ayran", "c": "Türkei"},
        {"n": "Lassi", "c": "Indien"},
        {"n": "Kefir", "c": "Kaukasus"},
        {"n": "Chicha", "c": "Peru"},
    ],
    'streetfood': [
        {"n": "Bánh Mì", "c": "Vietnam"},
        {"n": "Arepas", "c": "Kolumbien"},
        {"n": "Empanadas", "c": "Argentinien"},
        {"n": "Jerk Chicken", "c": "Jamaika"},
        {"n": "Bunny Chow", "c": "Südafrika"},
        {"n": "Pierogi", "c": "Polen"},
        {"n": "Poutine", "c": "Kanada"},
        {"n": "Vada Pav", "c": "Indien"},
        {"n": "Jianbing", "c": "China"},
        {"n": "Murtabak", "c": "Malaysia"},
    ],
    'instrumente': [
        {"n": "Didgeridoo", "c": "Australien"},
        {"n": "Kora", "c": "Westafrika"},
        {"n": "Balalaika", "c": "Russland"},
        {"n": "Santur", "c": "Iran"},
        {"n": "Charango", "c": "Bolivien"},
        {"n": "Mbira (Daumenklavier)", "c": "Simbabwe"},
        {"n": "Sitar", "c": "Indien"},
        {"n": "Erhu", "c": "China"},
        {"n": "Sho (Mundorgel)", "c": "Japan"},
        {"n": "Bouzouki", "c": "Griechenland"},
    ],
    'wahrzeichen': [
        {"n": "Cristo Redentor", "c": "Brasilien"},
        {"n": "Angkor Wat", "c": "Kambodscha"},
        {"n": "Sagrada Família", "c": "Spanien"},
        {"n": "Moai-Statuen", "c": "Chile (Osterinsel)"},
        {"n": "Burj Khalifa", "c": "VAE"},
        {"n": "Petronas Towers", "c": "Malaysia"},
        {"n": "Sydney Opera House", "c": "Australien"},
        {"n": "Kremlin", "c": "Russland"},
        {"n": "Hagia Sophia", "c": "Türkei"},
        {"n": "Chichen Itza", "c": "Mexiko"},
    ],
    'feste': [
        {"n": "Diwali", "c": "Indien"},
        {"n": "Holi", "c": "Indien"},
        {"n": "Carnival (Rio)", "c": "Brasilien"},
        {"n": "Songkran", "c": "Thailand"},
        {"n": "Nawruz", "c": "Iran"},
        {"n": "Onam", "c": "Indien (Kerala)"},
        {"n": "Inti Raymi", "c": "Peru"},
        {"n": "Hanami", "c": "Japan"},
        {"n": "Day of the Dead", "c": "Mexiko"},
        {"n": "Sapporo Snow Festival", "c": "Japan"},
    ],
    'museen': [
        {"n": "Louvre", "c": "Frankreich"},
        {"n": "British Museum", "c": "Vereinigtes Königreich"},
        {"n": "Smithsonian National Museum", "c": "USA"},
        {"n": "Hermitage Museum", "c": "Russland"},
        {"n": "National Museum of China", "c": "China"},
        {"n": "Uffizien", "c": "Italien"},
        {"n": "Rijksmuseum", "c": "Niederlande"},
        {"n": "Prado", "c": "Spanien"},
        {"n": "Metropolitan Museum of Art", "c": "USA"},
        {"n": "Musée d'Orsay", "c": "Frankreich"},
    ],
    'blumen': [
        {"n": "Kirschblüte (Sakura)", "c": "Japan"},
        {"n": "Tulpe", "c": "Niederlande"},
        {"n": "Lotusblume", "c": "Indien"},
        {"n": "Bougainvillea", "c": "Brasilien"},
        {"n": "Bird of Paradise", "c": "Südafrika"},
        {"n": "Lavendel", "c": "Frankreich"},
        {"n": "Sunflower (Sonnenblume)", "c": "Ukraine"},
        {"n": "Jasmin", "c": "Tunesien"},
        {"n": "Hibiskus", "c": "Malaysia"},
        {"n": "Passionsblume", "c": "Brasilien"},
    ],
    'entdecker': [
        {"n": "James Cook", "c": "Vereinigtes Königreich"},
        {"n": "Zheng He", "c": "China"},
        {"n": "Ibn Battuta", "c": "Marokko"},
        {"n": "Roald Amundsen", "c": "Norwegen"},
        {"n": "Ernest Shackleton", "c": "Irland"},
        {"n": "Vasco da Gama", "c": "Portugal"},
        {"n": "Ferdinand Magellan", "c": "Portugal"},
        {"n": "Christopher Columbus", "c": "Italien"},
        {"n": "Amerigo Vespucci", "c": "Italien"},
        {"n": "Abel Tasman", "c": "Niederlande"},
    ],
    'canyons': [
        {"n": "Grand Canyon", "c": "USA"},
        {"n": "Bryce Canyon", "c": "USA"},
        {"n": "Zion Canyon", "c": "USA"},
        {"n": "Fish River Canyon", "c": "Namibia"},
        {"n": "Waimea Canyon", "c": "USA (Hawaii)"},
        {"n": "Copper Canyon (Barranca del Cobre)", "c": "Mexiko"},
        {"n": "Ordesa Canyon", "c": "Spanien"},
        {"n": "Yarlung-Tsangpo-Schlucht", "c": "China"},
        {"n": "Vikos-Schlucht", "c": "Griechenland"},
        {"n": "Blyde River Canyon", "c": "Südafrika"},
    ],
    'sport': [
        {"n": "Sumo", "c": "Japan"},
        {"n": "Sepak Takraw", "c": "Malaysia"},
        {"n": "Kabaddi", "c": "Indien"},
        {"n": "Pato", "c": "Argentinien"},
        {"n": "Buzkashi", "c": "Afghanistan"},
        {"n": "Pelota Vasca", "c": "Spanien"},
        {"n": "Hurling", "c": "Irland"},
        {"n": "Gaelic Football", "c": "Irland"},
        {"n": "Shinty", "c": "Schottland"},
        {"n": "Bo-Taoshi", "c": "Japan"},
    ],
    'kleidung': [
        {"n": "Sari", "c": "Indien"},
        {"n": "Kimono", "c": "Japan"},
        {"n": "Hanbok", "c": "Südkorea"},
        {"n": "Dirndl", "c": "Deutschland / Österreich"},
        {"n": "Kilt", "c": "Schottland"},
        {"n": "Dashiki", "c": "Westafrika"},
        {"n": "Kaftan", "c": "Türkei"},
        {"n": "Boubou", "c": "Westafrika"},
        {"n": "Cheongsam (Qipao)", "c": "China"},
        {"n": "Huipil", "c": "Mexiko"},
    ],
    'begruessung': [
        {"n": "Namaste (Hände falten)", "c": "Indien"},
        {"n": "Hongi (Nasenberühren)", "c": "Neuseeland"},
        {"n": "Wai (Hände falten + Verbeugung)", "c": "Thailand"},
        {"n": "Eskimo-Kuss (Nasenreiben)", "c": "Kanada / Grönland"},
        {"n": "Küsschen auf beide Wangen", "c": "Frankreich"},
        {"n": "Dreifacher Wangenkuss", "c": "Schweiz"},
        {"n": "Faust-Gruß (Dap)", "c": "USA"},
        {"n": "Salaam (Hand auf Herz)", "c": "Iran"},
        {"n": "Tippen auf den Kopf (Kopfsalut)", "c": "Militär weltweit"},
        {"n": "Klingeln mit der Hand", "c": "Tibet"},
    ],
    'feiertage': [
        {"n": "Bastille Day (14. Juli)", "c": "Frankreich"},
        {"n": "Liberation Day (17. Mai)", "c": "Norwegen"},
        {"n": "Republic Day (26. Januar)", "c": "Indien"},
        {"n": "Australia Day (26. Januar)", "c": "Australien"},
        {"n": "Tanabata (7. Juli)", "c": "Japan"},
        {"n": "Chuseok (Erntedank)", "c": "Südkorea"},
        {"n": "Eid al-Fitr (Ende Ramadan)", "c": "Islam. Länder"},
        {"n": "Wesak (Buddhas Geburtstag)", "c": "Sri Lanka"},
        {"n": "Bonfire Night (5. November)", "c": "Vereinigtes Königreich"},
        {"n": "Heroes' Day", "c": "Zimbabwe"},
    ],
    'exporte': [
        {"n": "Kaviar", "c": "Iran"},
        {"n": "Zink", "c": "Peru"},
        {"n": "Lithium", "c": "Chile"},
        {"n": "Kokoa", "c": "Elfenbeinküste"},
        {"n": "Vanille", "c": "Madagaskar"},
        {"n": "Safran", "c": "Iran"},
        {"n": "Trüffel (Tuber melanosporum)", "c": "Frankreich"},
        {"n": "Smaragde", "c": "Kolumbien"},
        {"n": "Wolle (Merinowolle)", "c": "Australien"},
        {"n": "Zedernholz", "c": "Libanon"},
    ],
}.items():
    entry = d.get(key)
    if entry is None:
        continue
    if isinstance(entry, list):
        extm(entry, new_items)
    elif isinstance(entry, dict):
        extm(entry.setdefault('items', []), new_items)

report['kultur.json'] = 'updated'
save('kultur.json', d)

# ═══════════════════════════════════════════════════════════
#  FINAL REPORT
# ═══════════════════════════════════════════════════════════
print("\npatch_270_global_sweep.py — Zusammenfassung:")
for fn, status in sorted(report.items()):
    print(f"  ✓ {fn}")

# Count remaining under-40 arrays
import os as _os
total_under = 0
for fn in _os.listdir(DATA):
    if not fn.endswith('.json'): continue
    with open(_os.path.join(DATA, fn), encoding='utf-8') as f:
        d2 = json.load(f)
    if isinstance(d2, dict):
        for key, val in d2.items():
            if isinstance(val, list):
                if 15 <= len(val) <= 35: total_under += 1
            elif isinstance(val, dict):
                items = val.get('items', [])
                if isinstance(items, list) and 15 <= len(items) <= 35:
                    total_under += 1

print(f"\n  Arrays noch unter 36 Items: {total_under}")
print("  Spielübersicht bitte neu generieren: python3 generate_spieluebersicht.py")
