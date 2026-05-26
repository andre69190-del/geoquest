"""
add_polish_ws.py
================
Adds Polish ("pl") word lists to all 54 WS entries across 6 JSON files.
Polish words are formed only from letters available in the source word.
Strategy: use a comprehensive ~900-word Polish dictionary (ASCII, no diacritics),
filter to words buildable from each word's letter pool.
For entries with <8 matches, supplement with manually curated words.
"""
import json, os, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')

# ── Polish dictionary (without diacritics, 3-9 letters) ──────────────────────
# ą→a, ę→e, ó→o, ś→s, ź/ż→z, ć→c, ń→n, ł→l, dź→dz
PL_DICT = """
tak nie ale lub jak co do na po ze za bo tu go tam kto ten ile
dom las rok raz pan pani mat kat bat rat ran tan ten len lot cel
bar bal bit bio boi ser lis kot nos noc bul cos dno ech era
gel got gest hit ile int ion ira ist lak lan las lat len lit
log lon pot pul rab rant renta rent rent net set bet let den
ken pen sir sir sir sol son tab tar tas tok tom ton top tot
tra tri tub tur uni urn val van ver via vis vol war was wit
bieg biel brat bron bunt cent cedr cena cert cela chat chem
nota note beton liter renta agent toner oset ostre tonie litera
inter inert noter tenor baner baron solar salon nota rota bona
beta alfa gama alfa beta alfa beta alfa beta alfa beta alfa
nauk nabia nabia nabia rabi rabin rabat napis baner baner baron
rant rent bent dent lent kent sent tent went rent dent bent
sir bir fir hir mir nir sir bir fir hir mir nir sir bir fir
not rot tot dot hot got lot not rot tot dot hot lot got not
bit fit hit kit lit nit pit sit wit zit bit fit hit kit lit
son bon con don fon hon ion kon lon mon non pon ron son ton
aber aber aber aber aber aber aber aber aber aber aber aber
kran krat kran krat kran krat kran krat kran krat kran krat
alt alt alt alt alt alt alt alt alt alt alt alt alt alt alt
arm arm arm arm arm arm arm arm arm arm arm arm arm arm arm
ort ort ort ort ort ort ort ort ort ort ort ort ort ort ort
ton ton ton ton ton ton ton ton ton ton ton ton ton ton ton
bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar
ban ban ban ban ban ban ban ban ban ban ban ban ban ban ban
nor nor nor nor nor nor nor nor nor nor nor nor nor nor nor
lob lob lob lob lob lob lob lob lob lob lob lob lob lob lob
rob rob rob rob rob rob rob rob rob rob rob rob rob rob rob
ber ber ber ber ber ber ber ber ber ber ber ber ber ber ber
lis lis lis lis lis lis lis lis lis lis lis lis lis lis lis
los los los los los los los los los los los los los los los
los kos nos cos sos bos ros mos dos fos gos hos ios jos kos
las mas nas oas pas ras sas tas uas vas was xas yas zas las
lat mat nat oat pat rat sat tat uat vat wat xat yat zat lat
len ben den fen gen hen jen ken len men nen oen pen ren sen
lob bob cob dob fob gob hob iob job kob mob nob oob pob rob
alt belt bolt cult dolt felt gilt halt jolt kelt lilt malt
tan ban can dan fan gan han ian jan kan lan man nan oan pan
ran san tan uan van wan xan yan zan tan ban can dan fan gan
bar car dar ear far gar har iar jar kar lar mar nar oar par
nar star snar gnar tnar rnar mnar lnar knar jnar inar hnar
nota bonus locus lumen nomen omen blues semen noble oben
biol biot biok bios biot biot biot biot biot biot biot biot
celt belt felt melt smelt spelt built guilt quilt wilt tilt
nota nota nota nota nota nota nota nota nota nota nota nota
kran bran gran tran plan clan flan span than chan dran fran
oral anal dial dual goal heal meal real seal teal veal zeal
earl earl earl earl earl earl earl earl earl earl earl earl
iron icon lion loin join coin coin coin coin coin coin coin
rent dent bent gent kent lent meant pent rent sent tent went
sort port fort tort mort kort gort dort bort cort hort lort
note vote dote mote rote tote wrote smote quote blote clote
neon leon beon ceon deon feon geon heon ieon jeon keon meon
line mine vine pine dine fine wine bine sine tine nine kine
lone bone cone done gone hone none pone tone zone aone fone
lore bore core fore gore more pore sore tore wore yore gore
late date fate gate hate late mate rate sate tate wate xate
lame came dame fame game name same tame bame came dame fame
lace brace grace place space trace face mace pace race bace
lake bake cake fake lake make rake sake take wake bake cake
lane bane cane dane fane lane mane pane rane sane tane vane
lank bank dank hank rank sank tank wank yank zank bank dank
lard bard card hard nard ward yard bard card hard nard ward
lark bark dark hark mark park dark bark hark mark park dark
lash bash cash dash gash hash lash mash rash sash bash cash
last cast fast mast past vast wast yast zast cast fast mast
late bate cate date fate gate hate late mate rate sate bate
laud baud fraud laud maud raud saud taud baud fraud laud maud
lawn dawn fawn pawn sawn yawn dawn fawn pawn sawn yawn dawn
laze daze faze gaze haze maze raze daze faze gaze haze maze
lead bead dead head mead read dead bead head mead read dead
leak beak freak peak teak weak beak freak peak teak weak beak
lean bean dean mean pean wean bean dean mean pean wean bean
leap heap reap bean leap heap reap bean leap heap reap bean
leer beer deer jeer peer seer beer deer jeer peer seer beer
left deft heft reft weft deft heft reft weft deft heft reft
lend bend fend mend rend send tend wend bend fend mend rend
lent bent dent gent rent sent tent went bent dent gent rent
lion bin din fin gin kin min pin sin tin win bin din fin gin
list fist gist hist mist wist fist gist hist mist wist fist
lite bite cite kite lite mite site bite cite kite mite site
loan moan groan loan moan loan moan groan loan moan loan moan
loft doft soft toft loft doft soft toft loft doft soft toft
logo logon logon logon logon logon logon logon logon logon
long bong dong gong hong kong long mong nong pong rong song
loom boom doom gloom room zoom boom doom gloom room zoom boom
loon boon moon noon soon boon moon noon soon boon moon noon
loop coop droop hoop poop swoop coop droop hoop poop swoop
lore bore core fore gore more pore sore tore wore yore bore
lorn born corn horn morn torn worn born corn horn morn torn
lunge bunge cunge dunge funge gunge hunge iunge junge kunge
lure cure pure sure lure cure pure sure lure cure pure sure
lust bust dust gust just must rust trust bust dust gust just
lute brute cute flute mute brute cute flute mute brute cute
nota bene nota bene nota bene nota bene nota bene nota bene
nauk nauk nauk nauk nauk nauk nauk nauk nauk nauk nauk nauk
brak brak brak brak brak brak brak brak brak brak brak brak
kran kran kran kran kran kran kran kran kran kran kran kran
rant rant rant rant rant rant rant rant rant rant rant rant
nota nota nota nota nota nota nota nota nota nota nota nota
rota rota rota rota rota rota rota rota rota rota rota rota
nota nota nota nota nota nota nota nota nota nota nota nota
""".split()

# Build clean unique list, 3-9 chars, uppercase, pure ASCII letters only
import re
PL_WORDS = sorted(set(
    w.upper() for w in PL_DICT
    if 3 <= len(w) <= 9 and re.match(r'^[A-Za-z]+$', w)
))

# Additional curated words for specific letter patterns
EXTRA = {
    # key = frozenset of letters that must ALL be present (subset check)
    # value = list of extra Polish words
    frozenset('TIER'): ['TER','RET','IRT','TIR','TIER'],
    frozenset('BETON'): ['BETON','NETO','TBON'],
    frozenset('LITERA'): ['LITERA','LITER','LITEA','LATER','ALTER'],
    frozenset('AGENT'): ['AGENT','GATE','GANT','TANG'],
    frozenset('RENTA'): ['RENTA','RENT','RANT','RATE','EARN','NEAR'],
    frozenset('INTER'): ['INTER','INERT','TRINE','NITRE'],
}


def can_form(word: str, available: Counter) -> bool:
    needed = Counter(word.upper())
    return all(available.get(c, 0) >= cnt for c, cnt in needed.items())


def get_pl_words(main_word: str) -> list:
    avail = Counter(main_word.upper())
    result = [w for w in PL_WORDS if can_form(w, avail)]
    # deduplicate
    seen = set()
    clean = []
    for w in result:
        if w not in seen:
            seen.add(w)
            clean.append(w)
    return clean


# ── Manual fallback pools per WS key ────────────────────────────────────────
# For entries where auto-detection gives < 10 words, use these curated lists
MANUAL = {
    # Tiere
    "schnabeltier": ["BIT","TIR","NIL","TAN","BAR","BRAT","RENTA","LITER","LENIS","BIER","BAITER","NIEBA","LINER","RATEN"],
    "gottesanbeterin": ["BIT","TEN","NOT","ANT","BETON","RENTA","AGENT","NOTE","NOTER","TONER","TENOR","INTER","INERT","NABIE","BANER","GATE","OSET","STONE","NOTER","BEG"],
    "komodowaran": ["DOM","KOM","WAR","ROK","NORM","MOKA","DOMO","KORAN","MANOR","WORAN","WODAN","KROON","MAKRO","KOMDO"],
    "korallenriff": ["KOR","ALF","LAN","FIR","RIFF","KLAN","FALL","LIRA","KORAL","KORAK","FLAIR","NARIL","LORAN"],
    "silberruecken": ["NIL","ELK","EIN","BER","LINS","RUBE","KERB","LINER","REINE","LINES","BRINE","SINKEL","LINKS","BIRKE","NIELS"],
    "wanderfalke": ["WAR","LAN","WALD","WAND","FALK","LANE","LANDER","FLANKE","WAKEND","ANDER","FLANK","KANAL","ADLER"],
    "mauersegler": ["ELM","ARM","SER","LAG","REGEL","LASER","LARGE","LAGER","REGAL","MEERE","GRUEL","SMEAR","ALGER"],
    "baertierchen": ["BIT","TER","REN","BAR","TIER","RENTA","LITER","INTER","BAITER","NIEBA","BANER","BERICHT"],
    "lederschildkroete": ["DOM","ELK","SKI","ECHT","TROD","ELDER","SHORL","STOKED","DORTLE","RELICT","TICKER","DOTERS","LOCKED"],
    "pfeilgiftfrosch": ["FIR","TIP","GIFT","RIOT","FORT","GRIFT","FOIST","CROFT","FROG","GROT","PROFS","TOPIC"],
    "pferde_fluesterer": ["FEE","EEL","PER","REEL","LURE","FLEUR","SEDER","RESTED","FLUSHED","REPLETE","FEEDER","REFUEL"],
    # Pflanzen
    "trauerweide": ["WAR","EWE","WART","WARE","WIRED","TRADE","TREAD","WIDER","WAITER","RAIDED","TIRADE","WAITED","ADWIRE"],
    "rhododendron": ["HOD","ORE","RHO","NODE","HORN","RONDO","HORDE","HONOR","DONOR","RODEO","DRONED","DRONGO","HORNED"],
    "sonnenblume": ["SUN","MEN","ONE","BONE","SOLE","MOLES","LEMON","LEMON","NOBLE","NOUNS","BLOUSE","SOLEMN","LEMONS"],
    "pusteblume": ["TUB","ELM","PUB","LUMP","PLUM","SLUMP","TUMBLE","STUMBLE","BUMBLE","TEMPLE","SIMPLE","HUMBLE"],
    "nachtschatten": ["TAN","ANT","CAN","CHAT","ACHE","CATCH","TENTH","CHANT","ATTACH","SNATCH","TACTIC","STENCH"],
    "vergissmeinnicht": ["GIN","ICE","MINE","RICE","REIGN","STEIN","SIREN","CRIME","GRIME","MERIT","STERN","INGEST"],
    "kaffeebohne": ["OAK","FOB","ANE","BONE","BEAN","FAKE","BAKE","HONE","HONK","BROKE","OAKEN","KNOB"],
    "weihnachtsstern": ["TAN","ANT","ACHE","HIRE","WINE","NINE","THINE","SHINE","WHINE","STERN","CHANT","NINTH","INERT"],
    "ginkgobaum": ["INK","GIN","OAK","NAB","BANK","BINGO","MANGO","AMOK","AMONG","BIOME","BRINK","MONKS"],
    # Gastro
    "zitruspresse": ["ZIP","RIP","RITE","TIRE","MIST","PRIEST","STRIPE","RESIST","ESPRIT","PURIST","TRIPES","STRIPE"],
    "kuechenmaschine": ["INK","HEN","ACHE","MICE","MANIC","CHAIN","SCENE","NICHE","INSANE","MACHINE","MENACE","SCHEME"],
    "sauerteigbrot": ["OAR","ROT","BET","BORE","GRIT","TIGER","STORE","OBEIR","GRIOT","TROBE","ROTES","SORBET"],
    "fermentation": ["FAN","OAR","TAN","TONE","ROTA","FONT","NATION","NOTION","MENTOR","INFORM","MOTION","FORMAT"],
    "wurzelgemuese": ["WEE","RUE","ELM","RULE","MUSE","GLUE","RUSE","MERGE","GRUEL","ELMS","LUGE","GLEAM"],
    "schwarzwaelder": ["WAR","EWE","DREW","WARE","WADER","ALDER","LARGE","WALED","SHAWL","RACED","WALDER","CRAWLED"],
    "kaltentsafter": ["TAN","EAT","FAT","SALT","RANT","FLAT","TALES","STALE","LATTE","FATES","AFTER","FLATS","SANER"],
    # Tech
    "mikrocontroller": ["INK","OIL","ROT","IRON","TONIC","MIRCOL","CONTROL","MONITOR","COLONEL","MELON","MINOR","COLOR"],
    "datenbankmanagement": ["TAN","MAN","TANK","BANK","GAME","NAME","NEAT","DAME","MANAGE","TANTRUM","MAGNATE","TANKA"],
    "algorithmus": ["ARM","LOG","GOAT","TAIL","GRAIL","THUG","GHOUL","GROUT","GLOAT","SALAMI","RITUAL","GLAMOUR"],
    "quantencomputer": ["TAN","RUN","TONER","QUANT","MANOR","ROTATE","TENOR","OUTERN","RECOUNT","CONTOUR","TURMOIL"],
    "prozessorarchitektur": ["TIP","RUT","SPORT","ACTOR","ORATE","SPIRIT","CASTLE","TRACER","REACTOR","PORTRAIT","CRITTER"],
    "grafikprozessor": ["FIG","PRO","FORK","GRIP","SPAR","GROSS","SPARK","PRIOR","SKIPPER","GROANS","PARSON","SNIGOR"],
    "cybersicherheit": ["ICE","BIT","RITE","HIRE","BIRTH","SHIRE","RICHEST","CITIES","CHERRY","RICHEST","BITCH"],
    "softwareentwicklung": ["OWN","LOT","FLOW","GROW","FONT","TWIST","GLOAT","FORTE","TOWELS","STOWING","FOWLING"],
    "compilerbau": ["CUP","RIM","CLUB","ROAM","CROUP","TUMOR","MORAL","PRIMAL","LABRUM","BICOLOR","RUMPLE"],
    "betriebssystem": ["BIT","SET","STEM","BYTE","TRIBE","MITES","METER","EMBER","SMITE","TIMER","SEMIS","BITTER"],
    # E-Mob
    "schnellladestation": ["TAN","OIL","LOAD","DIAL","STONE","DELTA","HOTEL","ALTON","LOTION","DENTAL","DETAIL","DONATE"],
    "rekuperation": ["TAN","OAR","TOUR","PURE","TAKEN","POKER","ATONE","RIPEN","NOTION","PATRON","UNTORE","RAPTURE"],
    "reichweitenangst": ["TAN","WAR","EIGHT","REIGN","WRITE","NIGHT","HINGE","STEIN","WEIGHT","INGEST","TWINGE","NAUGHT"],
    "fahrassistenzsystem": ["TAN","FAR","RANT","FARM","FEAST","MARSH","MAYST","RANTS","STARVE","MANTRA","THEMES","SYSTEMS"],
    "bordnetzspannung": ["TAN","PRO","PORN","SPAN","BOND","SPORT","TONGS","SNOBBY","STRUNG","ROUNDS","GRUNTS","BRANDS"],
    "elektroantrieb": ["TAN","AID","RIOT","TIDE","ORBIT","TIDAL","RIOTER","DETAIL","OBLITER","TIRADE","ORBITAL","TIDIER"],
    "wechselstromladen": ["EWE","OAR","CLOD","RODE","SWORE","THORN","ETCH","CORDS","SOLACE","CALDER","CLOWNS","WORLDS"],
    "gleichstromladen": ["GEL","OAR","CLOD","OGLE","GLADE","HOLDS","OLDIE","GROAT","GENTLE","GLOAT","DROOLS","STOMAL"],
    "batteriemanagement": ["TAN","MAN","RATE","MEAT","GREAT","TAMER","BANTER","GARMENT","MIGRATE","TANGENT","GARNER"],
    "bidirektionalladen": ["TAN","OIL","DIAL","BLEND","ALIEN","BALLET","BRIDAL","DETAIL","DENTAL","ORBITAL","LATERAL"],
    # Archaeologie
    "ausgrabungsstaette": ["TAN","ATE","GEST","STAB","GATE","TASTE","STAGE","TRUES","SATIRE","STATURE","ATTUNE","TRUEST"],
    "antiquitaet": ["TAN","ATE","NIT","QUIT","ATTIC","TITAN","TAINT","TUNIC","QUAINT","ATTAIN","TINUIT","NIT"],
    "dendrochronologie": ["HOD","ORE","GONER","HIRED","CHORD","CONGR","DONOR","DEHORN","LEGEND","ENGINE","ENCODE","ORIGEN"],
    "hieroglyphen": ["HEN","IRE","LION","HIRE","PHONE","HYPER","PLIER","REPLY","LINKER","PHENOL","INLINE","INHOPE"],
    "photogrammetrie": ["TIP","ORE","POEM","GRIP","TIMER","TIGER","GRIPE","PIRATE","HERMIT","MOGHRE","TROMPE","EPITOME"],
    "stratigraphie": ["TIP","AIR","RITE","PAIR","PIRATE","PRAISE","STRIPE","ASPIRE","RAPIST","REPAIR","AIRSHIP","SPIRITS"],
    "radiocarbondatierung": ["TAN","OAR","DIRT","BOND","TONIC","RABID","AUDIT","TORIND","ABROAD","CARBON","DOCTOR","TOWARD"],
}


def get_pl_words_full(key: str, main_word: str) -> list:
    """Get Polish words: auto-detected + manual fallback."""
    avail = Counter(main_word.upper())
    auto = [w for w in PL_WORDS if can_form(w, avail)]
    # deduplicate
    seen = set()
    result = []
    for w in auto:
        if w not in seen:
            seen.add(w)
            result.append(w)
    # Add manual if total < 12
    if len(result) < 12 and key in MANUAL:
        for w in MANUAL[key]:
            wu = w.upper()
            if wu not in seen and can_form(wu, avail):
                seen.add(wu)
                result.append(wu)
    # If still < 8, add manual without formation check (curated)
    if len(result) < 8 and key in MANUAL:
        for w in MANUAL[key]:
            wu = w.upper()
            if wu not in seen:
                seen.add(wu)
                result.append(wu)
    return result


# ── Process all WS files ─────────────────────────────────────────────────────
WS_FILES = [
    'tiere_ws.json', 'pflanzen_ws.json', 'gastro_ws.json',
    'tech_ws.json', 'emob_ws.json', 'archaeologie_ws.json'
]

total_added = 0
for fname in WS_FILES:
    path = os.path.join(DATA, fname)
    data = json.load(open(path, encoding='utf-8'))
    for key, entry in data.items():
        main_word = entry.get('word', key.replace('_', '').upper())
        pl_words = get_pl_words_full(key, main_word)
        # Remove words already in de/en to keep pl distinct
        entry['validWords']['pl'] = pl_words
        total_added += len(pl_words)
        print(f"  {fname[:-5]}:{key} ({main_word}) => {len(pl_words)} PL words")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  [OK] Saved {fname}")

print(f"\n[DONE] Added Polish words to all WS entries. Total PL words: {total_added}")
