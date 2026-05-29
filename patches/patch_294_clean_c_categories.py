# -*- coding: utf-8 -*-
"""
Phase: 294
Scope: Saubere .c-Antwortkategorien der Match-Modi de/en/pl

Gesteinsklassen (geo_gesteinsarten), Kristallsysteme (geo_mineral_kristall),
Erdzeitalter (geo_fossil_zeitalter), Sternenhimmel (astro_sternbilder_himmel),
Kontinente (sport_sportart_kontinent). Match-opts/ans laufen bereits über
_tcc -> _tc, daher genügt Ergänzung in _CONTENT_I18N (en+pl).
Pro Gruppe werden ALLE distinct .c übersetzt (sonst gemischte Button-Sprachen).
Validierung: dict-Keys == extrahierte .c-Menge (vollständig + keine Tippfehler).
Dependencies: patch_293_country_answers.py
"""
import os, json

GEN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'gen.py')
content = open(GEN, encoding='utf-8').read()

# de -> (en, pl)
TR = {
# --- Gesteinsklassen ---
"Impaktgestein": ("Impact rock", "Skała impaktowa"),
"Impaktgestein/Bruchzone": ("Impact rock/fault zone", "Skała impaktowa/strefa uskoku"),
"Magmatisch": ("Igneous", "Magmowa"),
"Magmatisch (Granulitfazies)": ("Igneous (granulite facies)", "Magmowa (facja granulitowa)"),
"Magmatisch (poröses Vulkangestein)": ("Igneous (porous volcanic rock)", "Magmowa (porowata skała wulkaniczna)"),
"Magmatisch (pyroklastisch)": ("Igneous (pyroclastic)", "Magmowa (piroklastyczna)"),
"Magmatisch/Hydrotherm": ("Igneous/hydrothermal", "Magmowa/hydrotermalna"),
"Metamorph": ("Metamorphic", "Metamorficzna"),
"Metamorph (Bruchzone)": ("Metamorphic (fault zone)", "Metamorficzna (strefa uskoku)"),
"Metamorph (Hochdruck/Tiefe)": ("Metamorphic (high-pressure/depth)", "Metamorficzna (wysokociśnieniowa/głęboka)"),
"Sedimentaer": ("Sedimentary", "Osadowa"),
"Sedimentaer/Kiesel": ("Sedimentary/siliceous", "Osadowa/krzemionkowa"),
"Sedimentär": ("Sedimentary", "Osadowa"),
"Sedimentär (biogen)": ("Sedimentary (biogenic)", "Osadowa (biogeniczna)"),
"Sedimentär (chemisch)": ("Sedimentary (chemical)", "Osadowa (chemiczna)"),
# --- Kristallsysteme ---
"Hexagonal": ("Hexagonal", "Heksagonalny"),
"Hexagonal (geschichtet)": ("Hexagonal (layered)", "Heksagonalny (warstwowy)"),
"Kubisch": ("Cubic", "Regularny"),
"Kubisch (Oktaeder)": ("Cubic (octahedron)", "Regularny (oktaedr)"),
"Kubisch (Tetraeder)": ("Cubic (tetrahedron)", "Regularny (tetraedr)"),
"Kubisch (Wuerfel)": ("Cubic (cube)", "Regularny (sześcian)"),
"Monoklin": ("Monoclinic", "Jednoskośny"),
"Orthorhombisch": ("Orthorhombic", "Rombowy"),
"Tetragonal": ("Tetragonal", "Tetragonalny"),
"Trigonal": ("Trigonal", "Trygonalny"),
"Trigonal (Hexagonal)": ("Trigonal (hexagonal)", "Trygonalny (heksagonalny)"),
"Trigonal (Rhomboeder)": ("Trigonal (rhombohedron)", "Trygonalny (romboedr)"),
"Trigonal (Rhomboedrisch)": ("Trigonal (rhombohedral)", "Trygonalny (romboedryczny)"),
"Trigonal / Hexagonal": ("Trigonal / hexagonal", "Trygonalny / heksagonalny"),
"Triklin": ("Triclinic", "Trójskośny"),
# --- Erdzeitalter ---
"Devon (Paläozoikum)": ("Devonian (Palaeozoic)", "Dewon (paleozoik)"),
"Devon bis Heute": ("Devonian to present", "Dewon do dziś"),
"Eozaen (Kaenozoikum)": ("Eocene (Cenozoic)", "Eocen (kenozoik)"),
"Jura (Mesozoikum)": ("Jurassic (Mesozoic)", "Jura (mezozoik)"),
"Jura-Heute": ("Jurassic–present", "Jura–dziś"),
"Jura-Kreide (Mesozoikum)": ("Jurassic–Cretaceous (Mesozoic)", "Jura–kreda (mezozoik)"),
"Kambrium (Palaeozoikum)": ("Cambrian (Palaeozoic)", "Kambr (paleozoik)"),
"Kambrium-Heute": ("Cambrian–present", "Kambr–dziś"),
"Kambrium-Trias (Palaeozoikum-Mesozoikum)": ("Cambrian–Triassic (Palaeozoic–Mesozoic)", "Kambr–trias (paleozoik–mezozoik)"),
"Karbon (Paläozoikum)": ("Carboniferous (Palaeozoic)", "Karbon (paleozoik)"),
"Karbon-Perm (Palaeozoikum)": ("Carboniferous–Permian (Palaeozoic)", "Karbon–perm (paleozoik)"),
"Kreide (Mesozoikum)": ("Cretaceous (Mesozoic)", "Kreda (mezozoik)"),
"Känozoikum": ("Cenozoic", "Kenozoik"),
"Mesozoikum": ("Mesozoic", "Mezozoik"),
"Miozaen-Pliozaen (Kaenozoikum)": ("Miocene–Pliocene (Cenozoic)", "Miocen–pliocen (kenozoik)"),
"Ordovizium-Devon (Palaeozoikum)": ("Ordovician–Devonian (Palaeozoic)", "Ordowik–dewon (paleozoik)"),
"Ordovizium-Heute": ("Ordovician–present", "Ordowik–dziś"),
"Paläogen (Känozoikum)": ("Paleogene (Cenozoic)", "Paleogen (kenozoik)"),
"Paläozoikum": ("Palaeozoic", "Paleozoik"),
"Paläozoikum–heute": ("Palaeozoic–present", "Paleozoik–dziś"),
"Pleistozaen (Kaenozoikum)": ("Pleistocene (Cenozoic)", "Plejstocen (kenozoik)"),
"Pleistozän (Känozoikum)": ("Pleistocene (Cenozoic)", "Plejstocen (kenozoik)"),
"Pliozän (Känozoikum)": ("Pliocene (Cenozoic)", "Pliocen (kenozoik)"),
"Präkambrium": ("Precambrian", "Prekambr"),
"Trias (Mesozoikum)": ("Triassic (Mesozoic)", "Trias (mezozoik)"),
"Trias-Heute": ("Triassic–present", "Trias–dziś"),
# --- Sternenhimmel ---
"Aequatorial": ("Equatorial", "Równikowy"),
"Aequatorial/Nord": ("Equatorial/Northern", "Równikowy/północny"),
"Aequatorial/Sued": ("Equatorial/Southern", "Równikowy/południowy"),
"Nordhimmel": ("Northern sky", "Niebo północne"),
"Suedhimmel": ("Southern sky", "Niebo południowe"),
"Südhimmel": ("Southern sky", "Niebo południowe"),
"Äquatorbereich": ("Equatorial region", "Obszar równikowy"),
# --- Kontinente (sport_sportart_kontinent) ---
"Afrika": ("Africa", "Afryka"),
"Asien": ("Asia", "Azja"),
"Asien (Indien)": ("Asia (India)", "Azja (Indie)"),
"Asien (Korea)": ("Asia (Korea)", "Azja (Korea)"),
"Asien (Myanmar)": ("Asia (Myanmar)", "Azja (Mjanma)"),
"Asien (Thailand)": ("Asia (Thailand)", "Azja (Tajlandia)"),
"Asien (Ursprung)": ("Asia (origin)", "Azja (pochodzenie)"),
"Asien (Zentralasien)": ("Asia (Central Asia)", "Azja (Azja Środkowa)"),
"Asien Japan": ("Asia – Japan", "Azja – Japonia"),
"Asien Myanmar": ("Asia – Myanmar", "Azja – Mjanma"),
"Asien Philippinen": ("Asia – Philippines", "Azja – Filipiny"),
"Asien Suedostasien": ("Asia – Southeast Asia", "Azja – Azja Płd.-Wsch."),
"Asien/Europa": ("Asia/Europe", "Azja/Europa"),
"Australien/Ozeanien": ("Australia/Oceania", "Australia/Oceania"),
"Europa": ("Europe", "Europa"),
"Europa (Finnland)": ("Europe (Finland)", "Europa (Finlandia)"),
"Europa (Island)": ("Europe (Iceland)", "Europa (Islandia)"),
"Europa (Nordrussland)": ("Europe (Northern Russia)", "Europa (północna Rosja)"),
"Europa (Ostfriesland)": ("Europe (East Frisia)", "Europa (Fryzja Wschodnia)"),
"Europa (Schottland)": ("Europe (Scotland)", "Europa (Szkocja)"),
"Europa (Schweiz)": ("Europe (Switzerland)", "Europa (Szwajcaria)"),
"Europa England": ("Europe – England", "Europa – Anglia"),
"Europa Finnland": ("Europe – Finland", "Europa – Finlandia"),
"Europa Griechenland": ("Europe – Greece", "Europa – Grecja"),
"Europa Island": ("Europe – Iceland", "Europa – Islandia"),
"Europa Niederlande": ("Europe – Netherlands", "Europa – Holandia"),
"Europa Russland": ("Europe – Russia", "Europa – Rosja"),
"Europa Schottland": ("Europe – Scotland", "Europa – Szkocja"),
"Europa Schweiz": ("Europe – Switzerland", "Europa – Szwajcaria"),
"Europa Skandinavien": ("Europe – Scandinavia", "Europa – Skandynawia"),
"Europa/Ozeanien": ("Europe/Oceania", "Europa/Oceania"),
"Nordamerika": ("North America", "Ameryka Północna"),
"Nordamerika (USA)": ("North America (USA)", "Ameryka Północna (USA)"),
"Nordamerika/Europa": ("North America/Europe", "Ameryka Północna/Europa"),
"Ozeanien": ("Oceania", "Oceania"),
"Suedamerika": ("South America", "Ameryka Południowa"),
"Südamerika": ("South America", "Ameryka Południowa"),
"Südamerika (Argentinien)": ("South America (Argentina)", "Ameryka Południowa (Argentyna)"),
}

# --- Vollständigkeits-Check gegen die echten Gruppen ---
GROUPS = {
 'geo_gesteinsarten': 'geo_match.json',
 'geo_mineral_kristall': 'geo_match.json',
 'geo_fossil_zeitalter': 'geo_match.json',
 'astro_sternbilder_himmel': 'astro_match.json',
 'sport_sportart_kontinent': 'sport_match.json',
}
need = set()
for g, f in GROUPS.items():
    d = json.load(open(f'data/{f}', encoding='utf-8'))
    for it in d[g]['items']:
        if it.get('c'): need.add(it['c'])
missing = need - set(TR)
extra = set(TR) - need
assert not missing, ('Fehlende Übersetzungen: ' + repr(sorted(missing)))
if extra:
    print('[WARN] extra keys (nicht in Gruppen):', sorted(extra))

EN = {de: en for de, (en, pl) in TR.items()}
PL = {de: pl for de, (en, pl) in TR.items()}

def block(src, name):
    a = src.index(name + '=') + len(name + '=')
    d = 0; k = a; ins = None; esc = False
    while k < len(src):
        c = src[k]
        if ins:
            if esc: esc = False
            elif c == '\\': esc = True
            elif c == ins: ins = None
        else:
            if c in '"\'`': ins = c
            elif c == '{': d += 1
            elif c == '}':
                d -= 1
                if d == 0: k += 1; break
        k += 1
    return a, k, src[a:k]

s_idx, e_idx, obj = block(content, 'const _CONTENT_I18N')
data = json.loads(obj)
data.setdefault('en', {}).update(EN)
data.setdefault('pl', {}).update(PL)
content = content[:s_idx] + json.dumps(data, ensure_ascii=False) + content[e_idx:]
print(f'[OK]   _CONTENT_I18N += {len(EN)} en/pl (Gesteins/Kristall/Erdzeitalter/Himmel/Kontinente)')

_tmp = GEN + '.tmp'
open(_tmp, 'w', encoding='utf-8').write(content)
os.replace(_tmp, GEN)
print('\nPatch complete.')
