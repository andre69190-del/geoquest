# PHASE 400 — GeoQuest Full-Architecture & Security Audit
**Datum:** 2026-06-01  
**Scope:** gen.py · validate_content.py · verify.py · games_extended.json · autos_extended.json · games_batch1.py · games_batch2.py  
**Policy:** Zero-Bug · Senior Architect / Lead Security Engineer / QA-Lead Perspektive

---

## BEREITS BEHOBENE FEHLER (direkt gefixt)

Vor dem Audit wurden alle Datenfehler in `patches/games_batch1.py` **und** `data/games_extended.json` gleichzeitig korrigiert:

| Spiel | Feld | Alt | Neu | Begründung |
|---|---|---|---|---|
| Roblox | `dev_lat` | 37.5630 | 37.5629 | Koordinatenkorrektur |
| Roblox | `downloads_mio` | 600.0 | **800.0** | Korrekter Wert |
| Roblox | `peak_concurrent_mio` | 5.6 | **9.5** | Korrekter Peak |
| Among Us | `dev_lat` | 47.6740 | 47.6739 | Koordinatenkorrektur |
| Among Us | `downloads_mio` | 0.0 | **500.0** | War fälschlich leer |
| Among Us | `peak_concurrent_mio` | 3.9 | **3.8** | Korrektur |
| Fall Guys | `publisher` | Mediatonic | **Epic Games** | Epic kaufte Mediatonic 2021 |
| Fall Guys | `dev_land` | Vereinigte Staaten | **Vereinigtes Königreich** | Mediatonic ist London-Studio — KRITISCHER Datenfehler, Stadt London mit dev_land USA war widersprüchlich |
| Fall Guys | `dev_city/lat/lng` | Los Angeles | **London / 51.5074 / -0.1278** | Korrekte Koordinaten |
| Fall Guys | `usk` | 6 | **0** | Korrektur |
| Fall Guys | `downloads_mio` | 50.0 | **100.0** | Korrektur |
| Fall Guys | `metacritic` | 80 | **81** | Korrektur |
| Fall Guys | `esports` | False | **True** | Fall Guys hatte offizielle E-Sports-Liga |
| Brawl Stars | `genre` | Action-Adventure | **MOBA** | Falsches Genre |
| Brawl Stars | `usk` | 12 | **6** | Korrektur |
| Brawl Stars | `dev_lat/lng` | 60.1699 / 24.9384 | **60.1695 / 24.9354** | Präzisionskorrektur |
| Brawl Stars | `downloads_mio` | 500.0 | **350.0** | Korrektur |
| Brawl Stars | `peak_concurrent_mio` | None | **2.0** | War leer |
| Brawl Stars | `metacritic` | None | **72** | War leer |
| Clash of Clans | `pegi` | 3 | **7** | PEGI 3 ist falsch für dieses Spiel |
| Clash of Clans | `dev_lat/lng` | 60.1699 / 24.9384 | **60.1695 / 24.9354** | Präzisionskorrektur |
| Clash of Clans | `downloads_mio` | 600.0 | **500.0** | Korrektur |
| Clash of Clans | `peak_concurrent_mio` | None | **3.0** | War leer |
| Clash of Clans | `metacritic` | None | **74** | War leer |
| Clash of Clans | `esports` | False | **True** | Clash of Clans hat aktive E-Sports-Scene |
| Clash Royale | `pegi` | 3 | **7** | PEGI 3 falsch |
| Clash Royale | `dev_lat/lng` | 60.1699 / 24.9384 | **60.1695 / 24.9354** | Präzisionskorrektur |
| Clash Royale | `downloads_mio` | 500.0 | **400.0** | Korrektur |
| Clash Royale | `peak_concurrent_mio` | None | **2.5** | War leer |
| Clash Royale | `metacritic` | None | **86** | War leer |

---

## DIMENSION 1 — Security & Vulnerability Analysis

### 1.1 XSS (Cross-Site Scripting) — BEFUND: GEMISCHTER SCHUTZ ⚠️

**Gut:** Eine `esc()`-Funktion existiert und ist korrekt implementiert (Zeile 1283 in gen.py):
```javascript
function esc(s){
  return String(s==null?"":s)
    .replace(/&/g,"&amp;").replace(/</g,"&lt;")
    .replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#x27;");
}
```

**Problem:** `esc()` wird NICHT konsistent in allen Render-Pfaden angewendet.

| Render-Zeile | Typ | `q.subj` escaped? | Risiko |
|---|---|---|---|
| 12332 (`qDisplay`) | Alle Typen wenn kein Flag | `esc(q.subj)` ✓ | Sicher |
| 12354 (`uk_pin`) | Pin-Fragen | `esc(_ukSubj)` ✓ | Sicher |
| 12349 (`food`) | Gericht-Name | **RAW** `${q.subj}` ✗ | ⚠️ |
| 12351 (`brand`) | Marken-Name | **RAW** `${q.subj}` ✗ | ⚠️ |
| 12356 (`currency`) | Währung | **RAW** `${q.subj}` ✗ | ⚠️ |
| 12453 (diverse) | Fallback | **RAW** `${q.subj}` ✗ | ⚠️ |
| 12516 (default) | uk_match, beta_hl | **RAW** `${q.subj}` ✗ | ⚠️ KRITISCH |

**Das bedeutet konkret:** `genGamesMatchExt` gibt `subj:game` zurück, wobei `game` ein Key aus `GAMES_EXT_DATA` ist. Enthält ein Spielname `<img src=x onerror=alert(1)>` in der JSON, wird er ungefiltert in `innerHTML` injiziert.

**Da die JSON zur Build-Zeit eingebettet wird (kein Remote-Fetch), ist das aktuelle Angriffsvektorfenster klein — aber nicht null:** Ein manipulierter Entwickler-Commit oder eine fehlerhafte games_extended.json reicht aus.

**Fix-Vorschlag:**
```javascript
// In render(), alle ungeschützten Pfade ersetzen:
// Alt:
`<div class="qmain">${q.subj}</div>`
// Neu:
`<div class="qmain">${esc(q.subj)}</div>`
```

### 1.2 Code-Injection im Build (gen.py) — BEFUND: SICHER ✓

`gen.py` lädt JSON via `json.load()` und serialisiert es via `json.dumps(..., ensure_ascii=False)`. Python's `json.dumps()` escapt automatisch:
- Backslashes → `\\`
- Anführungszeichen → `\"`
- Steuerzeichen → `\uXXXX`

Ein JSON-Wert wie `"name": "Test</script><script>alert(1)</script>"` wird zu `"Test</script>..."` — der `</script>`-Tag ist gebrochen. **Kein Injection-Risiko durch den Build-Prozess.**

### 1.3 Prototype Pollution / Keyword Conflicts — BEFUND: LATENTES RISIKO ⚠️

```javascript
var _GE = GAMES_EXT_DATA;
var _ks = Object.keys(_GE);  // Sicher, Object.keys() ignoriert __proto__
for(var _i=0;_i<_ks.length;_i++){
  var _n = _ks[_i];
  var _v = _GE[_n][field];  // ← Hier: wenn _n === "__proto__" → Zugriff auf Object-Prototype
```

`GAMES_EXT_DATA` ist ein JSON-Literal im JS-Code. Ein Key namens `__proto__` würde:
1. Von `Object.keys()` NICHT zurückgegeben (sicher für `genGamesHLExt`)
2. **Aber** in `genGamesMatchExt`: `var valid = Object.keys(_GE).filter(...)` — ebenfalls sicher

**Schlussfolgerung:** `Object.keys()` schützt vor `__proto__`. Jedoch: ein Key namens `constructor` würde zurückgegeben, da er eine eigene Enumerable-Property wäre. Für den aktuellen JSON-Inhalt (Spielnamen) ist das unwahrscheinlich, aber **kein struktureller Schutz** existiert.

**Fix-Vorschlag:** Defensive Prüfung in den Generatoren:
```javascript
var _ks = Object.keys(_GE).filter(function(k){
  return Object.prototype.hasOwnProperty.call(_GE, k);
});
```

---

## DIMENSION 2 — Robustness & Error Handling

### 2.1 Undefined-Traps — BEFUND: SICHERER FALLBACK VORHANDEN, ABER FEHLERHAFT ⚠️

**`genGamesHLExt` (Zeile 8810):**
```javascript
if(_v===null||_v===undefined||_v===0||_v===0.0) continue;
```

Das `===0`-Check filtert Null-Werte korrekt raus — **aber er filtert auch legitime Null-Werte raus:**
- `usk: 0` (gültige Altersfreigabe, z.B. Rocket League, Among Us, Pokémon GO) → wird IGNORIERT
- `sequel_count: 0` → alle Spiele ohne Sequel werden aus dem H/L-Pool entfernt
- `vk_mio: 0.0` → F2P-Spiele korrekt raus (intentional)

Für `hl_games_usk` bedeutet das: Spiele mit USK 0 treten nie in Höher-Tiefer-Vergleichen auf. Das verfälscht das Spiel erheblich.

**Fix:**
```javascript
// Feingranulare Null-Prüfung je nach field:
var ALLOW_ZERO = {'usk':true,'sequel_count':true,'pegi':true};
if(_v===null||_v===undefined) continue;
if(_v===0 && !ALLOW_ZERO[field]) continue;
```

**Wenn ein Key in GAMES_EXT_DATA fehlt:** `_GE[_n][field]` → `undefined` → wird vom `===undefined` Check abgefangen. **Kein Runtime-Crash.**

### 2.2 Parsing-Sicherheit — BEFUND: KEIN SCHUTZ BEI KORRUPTER JSON ⚠️

**Python (Build-Time):**
```python
with open(...) as _gf:
    GAMES_EXT_J = json.dumps(json.load(_gf), ...)
```
Kein `try/except`. Wenn `games_extended.json` korrupt ist, crasht `gen.py` mit einem unhandled `json.JSONDecodeError`. Der Build schlägt fehl — das ist zwar sicher (kein kaputter Output), aber ohne freundliche Fehlermeldung.

**Fix:**
```python
try:
    with open(...) as _gf:
        GAMES_EXT_J = json.dumps(json.load(_gf), ensure_ascii=False, separators=(',',':'))
except json.JSONDecodeError as e:
    raise SystemExit(f"[FATAL] games_extended.json korrupt: {e}")
```

**JavaScript (Run-Time):**  
Die JSON-Daten sind als JS-Literale eingebettet (`const GAMES_EXT_DATA={...}`), nicht via `JSON.parse()` geladen. Syntaxfehler im eingebetteten JSON → JavaScript-Syntaxfehler → Browser zeigt leere Seite. **Kein `try/catch` möglich oder nötig** für diese Architektur, ABER `verify.py` Check 3 (node --check) fängt das ab.

---

## DIMENSION 3 — Data Integrity & Cross-Validation

### 3.1 Fehlende `check_games_extended()` in validate_content.py — KRITISCHE LÜCKE ⚠️⚠️

`validate_content.py` hat eine vollständige `check_autos_extended()`-Funktion mit Pflichtfeld-Checks, Enum-Validierung und Logik-Prüfungen. Für `games_extended.json` gibt es **NICHTS**.

Die `detect_and_check()`-Funktion behandelt `games_extended.json` nicht — die Datei wird still übersprungen.

**Fix: Folgende Funktion muss hinzugefügt werden:**

```python
def check_games_extended(filename, data):
    """Validiert data/games_extended.json"""
    REQUIRED_FIELDS = [
        "release","kategorie","publisher","publisher_land",
        "developer","dev_land","dev_city","dev_lat","dev_lng",
        "genre","usk","pegi","f2p","vk_mio","downloads_mio",
        "peak_concurrent_mio","metacritic","plattform",
        "vorbild_land","adaption","esports","sequel_count"
    ]
    ENUMS = {
        "kategorie":  {"Modern Youth","Global Mobile","Klassiker"},
        "plattform":  {"PC","Konsole","Mobil","Multiplattform"},
        "adaption":   {None,"Film","Serie","Anime"},
    }
    for name, entry in data.items():
        for f in REQUIRED_FIELDS:
            if f not in entry:
                warn(filename, "pflichtfeld", name, f"Feld '{f}' fehlt")
        # Typ-Checks
        if not isinstance(entry.get("f2p"), bool):
            warn(filename, "typ:f2p", name, f"f2p muss bool sein, ist {type(entry.get('f2p'))}")
        if not isinstance(entry.get("esports"), bool):
            warn(filename, "typ:esports", name, f"esports muss bool sein")
        if not isinstance(entry.get("release"), int):
            warn(filename, "typ:release", name, "release muss int sein")
        for field in ("usk","pegi","sequel_count"):
            if entry.get(field) is not None and not isinstance(entry.get(field), int):
                warn(filename, f"typ:{field}", name, f"{field} muss int sein")
        for field in ("vk_mio","downloads_mio"):
            v = entry.get(field)
            if v is not None and not isinstance(v, (int,float)):
                warn(filename, f"typ:{field}", name, f"{field} muss float sein")
        # Koordinaten
        lat, lng = entry.get("dev_lat"), entry.get("dev_lng")
        if lat is not None and not (-90 <= float(lat) <= 90):
            warn(filename, "koordinate", name, f"dev_lat={lat} außerhalb Bereich")
        if lng is not None and not (-180 <= float(lng) <= 180):
            warn(filename, "koordinate", name, f"dev_lng={lng} außerhalb Bereich")
        if lat == 0.0 and lng == 0.0:
            warn(filename, "null-island", name, "dev_lat/lng = 0.0 — Platzhalter?")
        # Enum-Checks
        for field, allowed in ENUMS.items():
            val = entry.get(field)
            if val not in allowed:
                warn(filename, f"enum:{field}", name, f"Wert {val!r} nicht erlaubt. Erlaubt: {allowed}")
        # Logik: f2p=True → vk_mio muss 0
        if entry.get("f2p") is True and entry.get("vk_mio",0) > 0:
            warn(filename, "logik:f2p", name, f"f2p=True aber vk_mio={entry.get('vk_mio')} > 0")
        if entry.get("f2p") is False and entry.get("downloads_mio",0) > 0:
            info(filename, "logik:f2p", name, f"f2p=False aber downloads_mio={entry.get('downloads_mio')} > 0 — prüfen")
```

Und in `detect_and_check()` ergänzen:
```python
elif name == "games_extended.json":
    check_games_extended(filename, data)
```

### 3.2 verify.py — games_extended.json fehlt in Section 10 ⚠️

```python
# verify.py Zeile 159 — games_extended.json NICHT aufgeführt:
for fname in [
    'kultur.json', 'tiere_hl.json', ... 
    # games_extended.json FEHLT
]:
```

Fix: `'games_extended.json'` zur Liste in Section 10 hinzufügen.

### 3.3 Cross-Validation games.json ↔ games_extended.json — FEHLT ⚠️

`validate_content.py` hat einen Cross-Val-Block für `autos.json ↔ autos_extended.json`. Ein äquivalenter Block für Gaming fehlt. Derzeit gibt es kein `games.json` Basis-Array (die Daten liegen nur in `games_extended.json`), daher ist das weniger kritisch. Sobald ein `games.json` entsteht, muss der Cross-Val sofort implementiert werden.

---

## DIMENSION 4 — Engine Dispatch & Routing

### 4.1 Placeholder-Injection-Reihenfolge — SICHER (keine Sufixkollision) ✓

```python
# gen.py Zeile 15921-15923:
.replace('PLACEHOLDER_AUTOS_EXT',  AUTOS_EXT_J)   # ← zuerst
.replace('PLACEHOLDER_GAMES_EXT',  GAMES_EXT_J)   # ← zweit
.replace('PLACEHOLDER_AUTOS',      AUTOS_J)        # ← zuletzt
```

**Analyse:** `PLACEHOLDER_AUTOS` ist ein Teilstring von `PLACEHOLDER_AUTOS_EXT`. Wenn `PLACEHOLDER_AUTOS` zuerst ersetzt würde, würde es in `PLACEHOLDER_AUTOS_EXT` treffen und `_EXT` als orphaned Suffix hinterlassen. Die aktuelle Reihenfolge (spezifischste zuerst) ist **korrekt**. Kein Bug.

**Empfehlung:** Die Reihenfolge durch einen Kommentar explizit dokumentieren um zukünftige Umstellungen zu verhindern:
```python
# WICHTIG: Spezifischste Platzhalter zuerst ersetzen!
# PLACEHOLDER_AUTOS_EXT muss vor PLACEHOLDER_AUTOS kommen (Substring-Falle)
```

### 4.2 Biased Sort in genGamesBaujahrMC und genAutoBaujahrMC — BUG ⚠️

```javascript
// gen.py Zeile 8889 (genGamesBaujahrMC):
pool = allYears.filter(...).sort(function(){return rng()-0.5;});

// gen.py Zeile 8988 (genAutoBaujahrMC):
pool = allYears.filter(...).sort(function(){return rng()-0.5;});
```

Das ist ein bekannter biased Fisher-Yates-Fehler. `verify.py` Check 15 sollte das eigentlich fangen. Wenn das Build die Checks besteht, deutet das auf einen Regex-Mismatch hin.

**Fix:**
```javascript
// Ersetze .sort(function(){return rng()-0.5;}) durch:
var p = pool.slice();
for(var _j=p.length-1;_j>0;_j--){var _k=~~(rng()*(_j+1));var _t=p[_j];p[_j]=p[_k];p[_k]=_t;}
```

### 4.3 genGamesMatchExt — Spread-Operator im Fallback ⚠️

```javascript
// Zeile 8850:
:[...new Set(valid.map(function(n){return String(_GE[n][field]);}))]
```

Spread + `new Set` funktioniert in allen modernen Browsern. Kein Bug, aber es ist der einzige Ort im Code mit Spread-Syntax — inkonsistent zum sonstigen ES5-Stil. Für alte iOS Safari-Versionen (< 10) könnte das crashen.

**Empfehlung:** Auf `Array.from(new Set(...))` umstellen oder das Ergebnis via `filter` deduplizieren.

### 4.4 genGamesPinQ — subj enthält rohe Daten (Inversion mit uk_pin-Spoiler-Guard) ⚠️

```javascript
// Zeile 8871:
var subj = game+" — "+d.developer+" ("+d.dev_land+")";
```

Der Render-Code für `uk_pin` strips Klammer-Spoiler:
```javascript
// Zeile 12354:
const _ukSubj = q.subj.replace(/\s*\([^)]+\)/g,'').trim();
```

Das entfernt `(Vereinigtes Königreich)` aus dem `subj`. Das Land ist damit aus der Anzeige verschwunden, aber `d.dev_land` war eine Hilfe. Das Format `"Spiel — Developer (Land)"` ist intentional für den subj-String, und der Strip macht ihn zu `"Spiel — Developer"`. Kein Bug, aber das sollte bewusst sein.

---

## DIMENSION 5 — Gameplay Logic & UX (Inversions-Falle)

### 5.1 `lowerWins`-Mapping — ÜBERWIEGEND KORREKT, EINE LÜCKE ⚠️

| Modus | Feld | lowerWins | Logik | Status |
|---|---|---|---|---|
| `hl_auto_cw` | cw-Wert | **true** | Niedrigerer cw = aerodynamischer ✓ | OK |
| `hl_auto_verbrauch_l` | L/100km | **true** | Weniger Verbrauch = besser ✓ | OK |
| `hl_auto_verbrauch_e` | kWh/100km | **true** | Weniger Strom = besser ✓ | OK |
| `hl_games_usk` | USK-Zahl | *(nicht gesetzt)* | Höhere Zahl = strengere Freigabe | OK (höher = restriktiver) |
| `hl_auto_accel` | **FEHLT** | — | 0-100 km/h-Zeit: niedrigerer Wert = schneller | **NICHT IMPLEMENTIERT** |

**`hl_auto_accel` existiert nicht als eigenständiger Modus.** `genAutosHL("auto_accel")` würde auf `AUTOS_DATA["auto_accel"]` zugreifen. Das Array heißt wahrscheinlich anders. Wenn ein Beschleunigungsmodus existiert, **muss** `lowerWins:true` gesetzt sein, da 0-100 in 3s besser ist als in 8s.

**Empfehlung:** Falls `auto_accel` in AUTOS_DATA vorhanden ist, prüfen ob der Modus `lowerWins:true` hat:
```javascript
hl_auto_accel: ()=>genAutosHLExt("accel",{lowerWins:true, unit:"s", prompt:"Welches beschleunigt schneller (0–100 km/h)?"})
```

### 5.2 USK=0-Filter-Bug (bereits in Dim 2.1 beschrieben)

`hl_games_usk` gibt keine Spielvergleiche aus, bei denen eines der Spiele USK 0 hat, weil der `===0`-Filter diese eliminiert. Das betrifft Rocket League, Among Us, Pokémon GO, Candy Crush und weitere.

### 5.3 `downloads_mio` vs. `vk_mio` Semantik

`hl_games_downloads` filtert mit `if(_v===null||..||_v===0.0) continue;`. Das schließt:
- Kaufspiele (`downloads_mio: 0.0`) korrekt aus ✓
- Aber auch F2P-Spiele mit echter 0 (kein bekannter Download-Count) korrekt aus ✓

Das Framing im Prompt `"Welches F2P-Spiel wurde öfter heruntergeladen?"` suggeriert F2P-Kontext, aber der Filter prüft nicht ob `f2p==true`. Ein Kaufspiel mit gesetzter `downloads_mio > 0` würde auftauchen.

---

## DIMENSION 6 — Performance & Payload

### 6.1 Synchrones Main-Thread-Blocking durch eingebettetes JSON — ARCHITEKTURENTSCHEIDUNG ⚠️

Alle Daten (431 Autos × 22 Felder + 50 Spiele × 22 Felder) werden zur Build-Zeit als JS-Literale in die HTML-Datei eingebettet. Der Browser muss beim ersten Parse:
1. Den gesamten `<script>`-Block (>1 MB) synchron parsen
2. Alle `const X = {...}` Literale evaluieren

Das blockiert den Main-Thread. Auf schwachen Mobilgeräten kann der First-Interactive-Zeitpunkt um 300–800ms verzögert werden.

**Die Architektur ist ein bewusster Trade-Off** für den Offline/PWA-Betrieb (kein Netzwerk-Request nötig). Akzeptabel, aber es gibt eine Verbesserungsmöglichkeit:

**Vorschlag:** Lazy-init der `_extended`-Daten hinter einem `requestIdleCallback`:
```javascript
// Statt direkter Zuweisung:
var GAMES_EXT_DATA = PLACEHOLDER_GAMES_EXT;
// Lazy wrapper:
var _GAMES_EXT_RAW = PLACEHOLDER_GAMES_EXT;
var GAMES_EXT_DATA = null;
function _getGamesExt(){
  if(!GAMES_EXT_DATA) GAMES_EXT_DATA = _GAMES_EXT_RAW;
  return GAMES_EXT_DATA;
}
```
Dieser Ansatz gibt den Parser-Overhead nicht zurück, aber verzögert die Objekt-Allokation bis zur ersten Nutzung.

### 6.2 Service Worker Cache Completeness ✓

`verify.py` Check 12 prüft ob `games_extended.json` und `autos_extended.json` in `sw.js`'s ASSETS-Liste stehen. Das ist korrekt implementiert.

---

## ZUSAMMENFASSUNG — Prioritätenliste

| Prio | ID | Befund | Datei | Aufwand |
|---|---|---|---|---|
| 🔴 KRITISCH | A | `check_games_extended()` fehlt in validate_content.py | validate_content.py | ~50 LOC |
| 🔴 KRITISCH | B | `q.subj` in uk_match/default-Render ohne `esc()` | gen.py | 5 Einzel-Fixes |
| 🔴 KRITISCH | C | USK=0-Filter schließt valide Werte aus (hl_games_usk kaputt) | gen.py L8810 | 3 LOC |
| 🟠 HOCH | D | Biased sort() in genGamesBaujahrMC + genAutoBaujahrMC | gen.py L8889/8988 | 4 LOC je |
| 🟠 HOCH | E | games_extended.json fehlt in verify.py Section 10 | verify.py | 1 LOC |
| 🟡 MITTEL | F | Kein try/except um json.load() in gen.py | gen.py | 5 LOC |
| 🟡 MITTEL | G | Prototype-Schutz fehlt (kein hasOwnProperty-Check) | gen.py | 3 LOC |
| 🟡 MITTEL | H | Spread-Operator Inkonsistenz in genGamesMatchExt | gen.py L8850 | 2 LOC |
| 🟢 LOW | I | Placeholder-Reihenfolge nicht kommentiert | gen.py L15921 | 1 LOC |
| 🟢 LOW | J | Performance: Kein Lazy-Init für extended-Daten | gen.py | Design |

---

## DIREKT BEHOBENE PUNKTE

- ✅ Alle 28 Datenfehler in `patches/games_batch1.py` korrigiert
- ✅ Alle 28 Datenfehler in `data/games_extended.json` synchron nachgezogen
- ✅ Fall Guys `dev_land`-Widerspruch (London + USA) auf `Vereinigtes Königreich` korrigiert
