# GeoQuest — Architect's Handbook
## Systemdokumentation & Entwicklerhandbuch

**Version:** Phase 225 (Stand: Mai 2026)
**Build:** gen.py → 1.07 MB | GeoQuest.html → 1.64 MB | 299 Spielmodi

---

## Inhaltsverzeichnis

1. [Projektübersicht & Philosophie](#1-projektübersicht--philosophie)
2. [Build-Architektur](#2-build-architektur)
3. [Die 4 Universal-Engines](#3-die-4-universal-engines)
4. [Entwicklungs-Workflow & Tooling](#4-entwicklungs-workflow--tooling)
5. [State Management & Sicherheit](#5-state-management--sicherheit)
6. [Daten-Architektur](#6-daten-architektur)
7. [Modi-Registrierung & Routing](#7-modi-registrierung--routing)

---

## 1. Projektübersicht & Philosophie

### Was ist GeoQuest?

GeoQuest ist ein **vollständig clientseitiges, lokal persistiertes Geografie- und Wissens-Quiz** als Progressive Web App (PWA). Die gesamte Spiellogik, alle Daten und das vollständige UI befinden sich in einer einzigen HTML-Datei (`GeoQuest.html`), die ohne Server funktioniert.

**Kerneigenschaften:**

- **Zero-Backend-Dependency für Gameplay:** Alle 299 Spielmodi laufen komplett offline. Supabase wird optional für Cloud-Highscores genutzt, ist aber kein Pflichtbestandteil.
- **Single-File Output:** Das Build-System kompiliert alle Quellen zu einer einzigen `GeoQuest.html`. Hosting = eine Datei deployen.
- **Clientseitige Persistenz:** Spielfortschritt, Einstellungen und Sammlungen werden über `localStorage` gespeichert. Ein kryptografischer Salt schützt die Daten vor Manipulation.
- **PWA-Ready:** Service Worker cached die App für vollständigen Offline-Betrieb (nach erstem Laden).

### Philosophie: Content ≠ Logic

Die zentrale Architekturentscheidung ist die strikte Trennung von **Inhalt** (Daten in `data/*.json`) und **Logik** (Engines in `gen.py`). Neue Tiere, Gerichte oder Sehenswürdigkeiten hinzufügen bedeutet nur eine JSON-Datei editieren — kein Python-Code anfassen.

---

## 2. Build-Architektur

### Das Drei-Schichten-Modell

```
┌─────────────────────────────────────────────────────┐
│  CONTENT-SCHICHT          data/*.json               │
│  Rohdaten: Tiere, Kultur, Städte, Wortschmiede      │
│  Format: Echtes JSON, Node.js-validiert             │
├─────────────────────────────────────────────────────┤
│  LOGIK-SCHICHT            gen.py                    │
│  Spielengines, UI-Renderer, State-Management        │
│  Sprache: Python (Build) + JavaScript (Runtime)     │
├─────────────────────────────────────────────────────┤
│  OUTPUT-SCHICHT           GeoQuest.html             │
│  Single-File-Build: alles inline, kein CDN-Pflicht  │
│  Größe: ~1.64 MB, JS-Anteil ~1.58 MB               │
└─────────────────────────────────────────────────────┘
```

### Build-Ablauf: `python3 gen.py`

```
1. Python liest cities.json        → CJ  (JSON-String)
2. Python liest capitals.json      → CAPJ
3. Python liest data/kultur.json   → KULTUR_DATA_J
4. Python liest data/tiere_hl.json → TIER_HL_DATA_J
5. Python liest data/tiere_match.json → TIER_MATCH_DATA_J
6. Python liest data/tiere_ws.json → TIER_WS_DATA_J
   ... (weitere statische Datensätze)

7. JS = r'''...'''                 Großer Raw-String mit dem gesamten JavaScript.
                                   Enthält PLACEHOLDER_*-Marker.

8. JS = JS
   .replace('PLACEHOLDER_CJ',         CJ)
   .replace('PLACEHOLDER_KULTUR_DATA', KULTUR_DATA_J)
   .replace('PLACEHOLDER_TIER_HL_DATA', TIER_HL_DATA_J)
   ...                               Alle Daten werden injiziert.

9. re.sub(r'\\UXXXXXXXX', chr(...))  Unicode-Escapes werden aufgelöst.

10. HTML = _HTML_HEAD + JS + _HTML_TAIL
11. write('GeoQuest.html')
12. write('index.html')            Netlify-Deploy-Target
```

### Kritische Invarianten nach dem Build

| Invariante | Geprüft durch |
|-----------|---------------|
| Keine PLACEHOLDER_* mehr im Output | `verify.py` Check 4 |
| Alle 4 Datenobjekte vorhanden | `verify.py` Check 5 |
| JS-Syntax valide (`node --check`) | `verify.py` Check 3 |
| MODES-Array ≥ 200 Einträge | `verify.py` Check 6 |
| `_GQ_SALT` unverändert | `verify.py` Check 11 |

---

## 3. Die 4 Universal-Engines

GeoQuest verwendet vier generische Spielengines, die für beliebige Datenkategorien wiederverwendet werden. Neue Spielmodi entstehen durch Registrierung + Daten — keine neue Engine-Logik notwendig.

---

### 3.1 Universal Pin Engine (`genUniversalPinQ`)

**Aufgabe:** Der Spieler sieht einen Begriff (z.B. ein Gericht, ein Tier, eine Sehenswürdigkeit) und muss seinen geografischen Ursprungsort auf der Weltkarte anpinnen.

**D3.js Karten-Rendering:**

```javascript
// Projektion: Mercator, optimiert für World-110m TopoJSON
projection = d3.geoMercator().fitSize([W, H], worldGeoJSON);

// Panning-Limits: 2x Kartenbreite in jede Richtung (verhindert Verlieren der Karte)
zoom = d3.zoom()
  .scaleExtent([1, 10])
  .translateExtent([[-W, -H], [2*W, 2*H]])
  .on("zoom", ev => { g.attr("transform", ev.transform); ... });
```

**Spoiler-Protection für Tiere:**

Tiere-Pin-Modi wie "Nashorn-Chamäleon (Kamerun)" würden durch den Klammerzusatz den Kartenort verraten. Die Engine prüft die Gruppe des Modus und bereinigt das angezeigte Subjekt:

```javascript
function genUniversalPinQ(cat) {
  const item = data[~~(rng() * data.length)];
  const modeObj = MODES.find(m => m.id === "uk_" + cat) || {};

  // Spoiler-Guard: Nur für Tiere-Gruppe aktiv
  const _isTiere = modeObj.group === "tiere";
  const _displaySubj = _isTiere
    ? item.n
        .replace(/\s*\(.*?\)/g, "")   // "(Kamerun)" entfernen
        .replace(/\s*→.*$/, "")        // "→ Ostafrika" entfernen
        .trim()
    : item.n;

  return {
    type: "uk_pin",
    subj: _displaySubj,   // ← Bereinigter Anzeigetext
    ans:  item.n,         // ← Vollständiger Name für Auswertung (NICHT im DOM)
    targetLat: item.lat,
    targetLng: item.lng,
    lid: "ukp_" + cat + "_" + item.n.replace(/\s+/g, "_")
  };
}
```

**Anti-Spoiler-Garantie:** `ans` (der vollständige Name) wird niemals als DOM-Attribut gerendert. Die Auswertung findet ausschließlich im JavaScript-Heap statt.

---

### 3.2 Universal Higher/Lower Engine — Die Index-Fenster-Mathematik

**Aufgabe:** Zwei Entitäten (Tiere, Städte, Länder) werden verglichen. Der Spieler muss entscheiden, welche den höheren Wert hat (Gewicht, Einwohnerzahl, Fläche, ...).

**Das Problem trivialer Paarungen:** Ohne Schutzmaßnahme würde eine Engine Eisbär (500 kg) mit Ameise (0.001 g) vergleichen — trivial lösbar.

**Die Lösung: Das La-Paz-Fenster (`W = max(1, floor(N * 0.1))`)**

```
Datensatz sortiert nach Wert (aufsteigend):
Index:  0    1    2    3    4    5    6    7    8    9
Wert: [ 1,   3,   5,   8,  12,  15,  18,  22,  28,  45 ]

Zufällig gewählter Index A: 4 (Wert: 12)
Fenstergröße W: floor(10 * 0.1) = 1
Erlaubter Vergleichsbereich: Index 3–5 (Werte 8, 15)

→ Beide Kandidaten liegen nah beieinander → herausfordernde Paarung
→ Kein trivialer Vergleich mit Extremwerten möglich
```

**Implementierung in `getSmartMatch` (klassische H/L Modi):**

```javascript
function getSmartMatch(candidates, ccA, valA, ccFn, valFn) {
  var sorted = valid.sort((a,b) => Number(valFn(a)) - Number(valFn(b)));
  var W = Math.max(1, Math.floor(sorted.length * 0.1)); // 10% Fenster
  var lo = Math.max(0, aIdx - W);
  var hi = Math.min(sorted.length - 1, aIdx + W);
  // Wähle zufällig aus [lo, hi] ohne aIdx
}
```

**Identische Implementierung in `genTiereHL` (Tiere H/L Modi):**

```javascript
function genTiereHL(dataKey) {
  const sorted = cfg.items.sort((a,b) => parseFloat(a.val) - parseFloat(b.val));
  while (tries++ < 40) {
    var ai = ~~(rng() * len);
    var W  = Math.max(1, Math.floor(len * 0.1)); // 10% Fenster
    var lo = Math.max(0, ai - W);
    var hi = Math.min(len - 1, ai + W);
    // Paarung aus dem Fenster wählen
  }
}
```

**Warum `Math.max(1, ...)`?** Bei sehr kleinen Datensätzen (< 10 Einträge) würde `floor(N * 0.1)` = 0 ergeben — damit wäre kein Vergleichspartner wählbar. `Math.max(1, ...)` garantiert mindestens einen Nachbarn.

---

### 3.3 Universal Match Engine (`genUniversalMatchQ`)

**Aufgabe:** Multiple-Choice-Zuordnung — zu einem Subjekt (z.B. "Sushi") muss das korrekte Land/die korrekte Kategorie gewählt werden.

**Distraktor-Pool-Logik:**

Falsche Antworten werden nicht zufällig aus allen Kategorien gezogen, sondern gezielt aus **thematisch benachbarten Kategorien** (Cross-Category-Distraktion). So wird z.B. bei "Sake (Japan)" nicht "Deutschland" als falsche Antwort gewählt, sondern "China" oder "Südkorea" — Länder, die mit Fermentation kulturell assoziiert sind.

```javascript
function genUniversalMatchQ(cat) {
  // Korrekte Antwort
  const item = data[idx];
  const cor  = item.c;  // z.B. "Japan"

  // Distraktoren: andere Werte aus DERSELBEN oder verwandten Kategorien
  const pool = data.filter(d => d.c !== cor).map(d => d.c);
  const dis   = shuffle(pool).slice(0, 3);

  return {
    type: "uk_match",
    subj: item.n,
    ans:  cor,
    opts: shuffle([cor, ...dis])
    // Antwort-Buttons werden gerendert, aber `ans` ist NICHT als data-Attribut gesetzt
  };
}
```

**Anti-Cheat:** Die Antwort-Buttons enthalten keinen maschinenlesbaren Hinweis auf die korrekte Option. Die Auswertung (`checkAnswer`) vergleicht den angeklickten Text mit `S.q.ans` im JavaScript-Heap.

---

### 3.4 Wort-Schmiede — Anagramm-Engine mit i18n-Fallback

**Aufgabe:** Aus den Buchstaben eines Begriffs (z.B. "SCHNABELTIER") müssen gültige Wörter geformt werden. Jedes gefundene Wort gibt Punkte.

**Die i18n-Fallback-Kette:**

```javascript
function initTierWortSchmiede(key) {
  var userLang   = S.language || localStorage.getItem("gq_lang") || "en";
  var wsLang     = _WS_LANGS.has(userLang) ? userLang : "en";  // Fallback: EN
  var raw        = entry.validWords[wsLang];
  var hasOwn     = Array.isArray(raw) && raw.length > 0;
  var actualLang = hasOwn ? wsLang : "en";    // Zweiter Fallback: EN
  var src        = hasOwn ? raw : (entry.validWords["en"] || []);
  // ...
}
```

Fallback-Kette: `DE (wenn vorhanden)` → `EN (immer vorhanden)`. Kein Cold-Start-Crash möglich, da `en`-Arrays in allen Einträgen garantiert befüllt sind (geprüft durch `verify.py` Check 10).

**Das Inventar-Anti-Cheat:**

Das System verhindert, dass ein Spieler denselben Buchstaben mehrfach verwendet, obwohl er nur einmal im Ausgangswort vorkommt:

```javascript
// Beim Tippen: Inventar aus dem Zielwort ableiten
function wsCheckWord(input) {
  var inventory = {};
  for (var ch of targetWord) inventory[ch] = (inventory[ch] || 0) + 1;

  // Prüfen ob alle Buchstaben des Inputs im Inventar vorhanden sind
  for (var ch of input) {
    if (!inventory[ch] || inventory[ch] <= 0) return false; // Buchstabe verbraucht
    inventory[ch]--;
  }
  return validWords.has(input);
}
```

**Bereits gefundene Wörter** werden in `S.askedLids` (als `alpha_WORT`-Einträge) gespeichert und beim nächsten Spielversuch ausgefiltert:

```javascript
usedLetters = new Set(
  [...S.askedLids]
    .filter(l => l.startsWith('alpha_'))
    .map(l => l.slice(6))
);
```

---

## 4. Entwicklungs-Workflow & Tooling

### Das Zero-Bug-Workflow-Prinzip

Jede Änderung an `gen.py` erfolgt ausschließlich über **Patch-Skripte** im Verzeichnis `patches/`. Direkte Bearbeitung von `gen.py` ist verboten.

**Warum?**
- `gen.py` ist 1.07 MB groß. Manuelle Edits in solchen Dateien erzeugen leicht Syntaxfehler oder ruinieren Unicode-Encoding.
- Patch-Skripte sind versioniert, dokumentiert und reproduzierbar.
- Der `run_patch.py`-Runner bricht mit Auto-Rollback ab, wenn etwas schiefgeht.

### Patch-Skripte schreiben: Die Goldene Regel

**Jeder** `c.replace()` Aufruf muss mit einer Eindeutigkeits-Assertion beginnen:

```python
# RICHTIG:
assert c.count(old) == 1, f"Anker nicht eindeutig: {old!r}"
c = c.replace(old, new, 1)

# FALSCH — kann mehrere Stellen gleichzeitig ändern:
c = c.replace(old, new)
```

### Pflicht-Header für Patch-Skripte

```python
"""
Phase: 228
Date:  2026-06-01
Author: Claude / Andre
Scope: Kurzbeschreibung (max. 80 Zeichen)

Description:
  Ausführliche Beschreibung. Welches Problem wird gelöst?
  Welche Anker werden verwendet? Gibt es Abhängigkeiten?

Dependencies: patch_225_json_extraction.py
Zero-Bug Policy: All c.replace() calls use assert c.count(old)==1
"""
```

### `run_patch.py` — Der Patch-Runner

```bash
python3 run_patch.py patches/patch_228_new_feature.py
```

**Was der Runner automatisch macht:**

```
1. Validiert den Pflicht-Header (Phase / Date / Scope)
2. Erstellt Backup: gen.py.bak_YYYYMMDD_HHMMSS
3. Führt das Patch-Skript aus
4. Führt python3 gen.py aus (Build)
5. Führt python3 verify.py aus (33 Checks)
   ↓ Bei FEHLER in Schritt 3, 4 oder 5:
   └─ Stellt gen.py aus dem Backup wieder her
   └─ Löscht das Backup
   └─ Bricht mit Fehlermeldung ab
   ↓ Bei ERFOLG:
   └─ Löscht das Backup (nicht mehr gebraucht)
   └─ Zeigt Build-Statistiken + nächste Schritte
```

### `verify.py` — Die 33 Pre-Push-Checks

`verify.py` wird automatisch durch `unlock_and_push.bat` vor jedem `git push` ausgeführt. Schlägt es an, bricht der Push ab.

| # | Check | Was geprüft wird |
|---|-------|-----------------|
| 0 | File presence | GeoQuest.html, gen.py, alle 4 data/*.json |
| 1 | HTML size | ≥ 1 MB (Regression-Schutz) |
| 2 | JS extraction | ≥ 500 KB JS aus 5 Script-Blöcken |
| 3 | JS syntax | `node --check` auf extrahiertem JS |
| 4 | Placeholder substitution | Keine `PLACEHOLDER_*` im Output |
| 5 | Data objects (9x) | KULTUR_DATA, TIER_*, WORTSCHMIEDE_DATA, MODES, MODE_CATS, GEN, plates |
| 6 | MODES count | ≥ 200 Einträge im MODES-Array |
| 7 | Generators (6x) | genUniversalPinQ, genTiereMatchQ, genTiereHL, initTierWortSchmiede, genHauptstadtDistanzQ, getSmartMatch |
| 8 | Anti-cheat | `_displaySubj` + `subj:_displaySubj` vorhanden |
| 9 | Mojibake | Keine neuen Â/Ã-Sequenzen (15 Legacy-Patterns whitelisted) |
| 10 | JSON round-trip | Alle 4 JSON-Dateien valide + Top-Level-Keys gezählt |
| 11 | _GQ_SALT | Salt im Output vorhanden (User-Saves-Schutz) |

### Vollständiger Sprint-Workflow

```
1. Patch schreiben → patches/patch_NNN_beschreibung.py
2. python3 run_patch.py patches/patch_NNN_beschreibung.py
   → Auto-Build + Auto-Verify
3. Bei grünem Selftest: unlock_and_push.bat ausführen
   → verify.py (nochmals als Pre-Push-Gate)
   → git add -A
   → git commit -m "..."
   → git push origin main
4. Vercel deployed automatisch aus dem GitHub-Push
```

---

## 5. State Management & Sicherheit

### Das globale `S`-Objekt

Sämtlicher Spielzustand lebt in einer einzigen globalen Variable `S`. Das ist bewusst — kein versteckter State in Closures, kein Framework-Magic.

**Wichtigste Felder:**

```javascript
let S = {
  // Spielphasen
  ph:   "menu",       // "menu" | "playing" | "feedback" | "end"
  tab:  "home",       // Aktiver Tab: "home" | "stats" | "profile"
  mode: "city",       // ID des aktuellen Spielmodus

  // Session-Score
  sc:      0,         // Aktueller Score
  st:      0,         // Aktueller Streak
  bs:      0,         // Bester Streak dieser Session
  rd:      0,         // Aktuelle Runde (1–10)
  correct: 0,         // Richtige Antworten

  // Aktuelle Frage
  q:    null,         // Frage-Objekt (enthält ans — NICHT im DOM)
  sel:  null,         // Vom Spieler gewählte Antwort
  ok:   null,         // true/false nach Auswertung

  // Dedup-System
  askedLids: new Set(), // Bereits gestellte Fragen (verhindert Wiederholungen)

  // Einstellungen
  diff:     "casual", // "casual" | "hardcore" | "survival"
  language: "de",     // "de" | "en"
  darkMode: false,

  // Auth / Cloud
  sbProfile: null,    // Supabase-Profil-Objekt
  // ...
};
```

**ROUNDS = 10** — Jede Spielsession besteht aus exakt 10 Runden.

### Fragen-Dedup via `askedLids`

Jede generierte Frage hat eine eindeutige `lid` (Level-ID). Bevor eine neue Frage gestellt wird, prüft der Core-Loop:

```javascript
// In _lvNext():
let q = null, tries = 0;
while (tries++ < 15) {
  const _c = (GEN[S.mode] || genCityQ)();
  if (_c && !S.askedLids.has(_c.lid)) {
    q = _c;
    break;
  }
}
S.askedLids.add(q.lid);
```

`S.askedLids` wird beim Spielstart geleert und session-weit gepflegt — so werden in 10 Runden nie dieselbe Frage zweimal gestellt.

### LocalStorage-Schema

Alle persistierten Daten werden mit dem `x`-Suffix in `localStorage` geschrieben (historisches Namensmuster):

| Key | Inhalt | Typ |
|-----|--------|-----|
| `gq_langx` | Sprache (`"de"` / `"en"`) | String |
| `gq_usernamex` | Spielername | String |
| `gq_surv_bestx` | Survival-Highscore | Number |
| `gq_sessions_localx` | Lokale Spiel-History | JSON |
| `gq_darkx` | Dark Mode aktiv | `"1"` / `"0"` |
| `gq_onboardingx` | Onboarding abgeschlossen | Boolean |
| `gq_spotter_countryx` | Letztes gewähltes Land im Kennzeichen-Spotter | String |

### Anti-Tamper: `_GQ_SALT` und Score-Hashing

Gespeicherte Highscores werden zusammen mit einem Salt gehasht. Manipulierte `localStorage`-Einträge werden beim Laden erkannt und verworfen.

```javascript
const _GQ_SALT = "GQ®2025🌍XKCD327";
```

> ⚠️ **KRITISCH: Dieser Salt darf NIEMALS geändert werden.**
> Eine Änderung des Salts invalidiert alle `localStorage`-Saves aller Nutzer weltweit sofort und irreversibel. Neue Highscores wären nicht mehr mit alten vergleichbar.

### Anti-Cheat: Der JavaScript Proxy-Wrapper

Das `S`-Objekt wird nach der Initialisierung in einen `Proxy` eingewickelt:

```javascript
// Schreibgeschützte Score-Felder
const GUARDED_WRITE = new Set(["sc", "correct", "st", "bs", "pts", "collectedPlates"]);

// Sensibles Lesen (enthält aktuelle Antwort)
const SENSITIVE_READ = new Set(["q"]);

const _p = new Proxy(S, {
  get(t, k) {
    if (SENSITIVE_READ.has(k) && !_isTrusted()) {
      console.warn("🚫 GeoQuest Anti-Cheat: console read of S.q detected.");
    }
    return t[k];
  },
  set(t, k, v) {
    if (GUARDED_WRITE.has(k) && !_isTrusted()) {
      console.warn("🚫 GeoQuest: Schummeln erkannt! Feld '" + k + "' ist geschützt.");
      return true; // Schreibversuch stillschweigend ignorieren
    }
    t[k] = v; return true;
  }
});
// S ist ab jetzt nur noch über den Proxy zugänglich:
Object.defineProperty(window, "S", { get: () => _p, configurable: false });
```

**Trusted Functions:** Nur Funktionen aus der Whitelist (`answer`, `startGame`, `checkAnswer`, `_lvNext`, ...) dürfen `sc`, `correct`, `bs` schreiben. Ein `S.sc = 999` aus der Browser-Konsole wird erkannt und blockiert.

**Warum `S.q.ans` nicht im DOM:** Die korrekte Antwort lebt ausschließlich in `S.q.ans` im JavaScript-Heap. Sie wird nie als `data-answer` Attribut oder sichtbarer Text in den DOM geschrieben. Das Proxy-Warning bei `S.q`-Lese-Zugriff aus der Konsole macht versuchtes Schummeln sichtbar.

---

## 6. Daten-Architektur

### Dateistruktur

```
GeoQuest/
├── gen.py                  Haupt-Build-Skript (Logik, Engines, UI)
├── GeoQuest.html           Build-Output (Single-File-App)
├── index.html              Netlify-Deploy-Target (Kopie von GeoQuest.html)
│
├── data/                   Content-Schicht (Phase 225)
│   ├── kultur.json         84 Kategorien: Getränke, Streetfood, Tänze, ...
│   ├── tiere_hl.json       13 H/L-Kategorien: Gewicht, Geschwindigkeit, ...
│   ├── tiere_match.json    19 Match-Kategorien: Fährten, Lebensräume, ...
│   └── tiere_ws.json       11 Wort-Schmiede-Einträge: Schnabeltier, Komodo, ...
│
├── cities.json             ~2300 kuratierte Städte (aus GeoNames)
│
├── verify.py               Post-Build-Selftest (33 Checks)
├── run_patch.py            Patch-Runner (Backup + Build + Verify + Rollback)
│
├── patches/                Alle Patch-Skripte (Phase 212+)
│   ├── PATCHES.md          Konvention-Dokumentation
│   ├── patch_212_*.py
│   ├── patch_213_*.py
│   └── ...
│
├── unlock_and_push.bat     Git-Push mit Pre-Push verify.py Gate
└── ARCHITECTURE.md         Dieses Dokument
```

### JSON-Datenschema

**`data/kultur.json`** — Flaches Objekt, Schlüssel = Kategorie-ID:

```json
{
  "getraenke": [
    { "n": "Mate",      "c": "Argentinien" },
    { "n": "Pisco Sour","c": "Peru" }
  ],
  "wahrzeichen": [
    { "n": "Taj Mahal", "c": "Indien",
      "lat": 27.1751, "lng": 78.0421 }
  ]
}
```

Felder: `n` (Name), `c` (Land/Kontinent), `lat`/`lng` (optional, für Pin-Modi).

**`data/tiere_hl.json`** — H/L-Datensatz mit Prompt und Items:

```json
{
  "gewicht_land": {
    "prompt": "Welches Landtier ist schwerer?",
    "unit": "kg",
    "items": [
      { "name": "Afrikanischer Elefant", "val": 6000 },
      { "name": "Giraffe",               "val": 800  }
    ]
  }
}
```

**`data/tiere_match.json`** — Match-Datensatz mit Prompt und Items:

```json
{
  "faehrten": {
    "prompt": "Zu welchem Tier gehört diese Spur?",
    "items": [
      { "n": "4 Zehen ohne Krallen, runder Handballen", "c": "Loewe" }
    ]
  }
}
```

**`data/tiere_ws.json`** — Wort-Schmiede mit mehrsprachigen Wortlisten:

```json
{
  "schnabeltier": {
    "word": "SCHNABELTIER",
    "validWords": {
      "de": ["TIER", "BIER", "STEIN", "ELCH"],
      "en": ["LITER", "RAIN", "TRAIL", "SNAIL"]
    }
  }
}
```

---

## 7. Modi-Registrierung & Routing

### Das Drei-Strukturen-Prinzip

Jeder Spielmodus muss in genau drei Stellen synchron registriert sein:

```
MODES     → UI-Metadaten  (Titel, Gruppe, Prompt, Farbe, Icon)
MODE_CATS → Kategorisierung (Welche Kachel gehört zu welcher Kategorie)
GEN       → Dispatch-Table (mode-ID → Generator-Funktion)
```

**Aktueller Stand:** 299 Modi, 299/299/299 — perfekte Konsistenz.

### MODES-Eintrag (Beispiel)

```javascript
{
  id:     "uk_getraenke",
  title:  "Getränke-Heimat",
  group:  "kultur",
  prompt: "Aus welchem Land kommt dieses Getränk?",
  icon:   "🍹",
  color:  "#f59e0b",
  cost:   0
}
```

### GEN-Dispatch (Beispiel)

```javascript
const GEN = {
  city:           genCityQ,
  flag:           genFlagQ,
  uk_getraenke:   () => genUniversalMatchQ("getraenke"),
  uk_wahrzeichen_pin: () => genUniversalPinQ("wahrzeichen"),
  hl_tiere_gewicht_land: () => genTiereHL("gewicht_land"),
  // ...299 Einträge total
};
```

### Der dynamische Multiplayer-Pool

`_getMpMode()` und `_lvPickMode()` sind vollständig dynamisch — kein Modus ist hardcoded ausgeschlossen:

```javascript
// Multiplayer-Pool: Alle spielbaren, nicht-"Coming soon" Modi ohne noMultiplayer-Flag
MODES.filter(m => GEN[m.id] && !m.comingSoon && !m.noMultiplayer)

// Level-Picker: Alle spielbaren Modi in einer Kategorie
MODE_CATS[sCat].modes.filter(m => GEN[m.id] && !m.comingSoon)
```

Wort-Schmiede Modi tragen `noMultiplayer: true` — sie sind zu zeitintensiv für synchrones Multiplayer.

**Daily Challenge:** Intentionell hardcoded auf `S.mode = "city"`. Die Daily Challenge ist ein tägliches globales Leaderboard-Event — alle Spieler weltweit spielen denselben Modus. Das ist ein bewusstes Design-Entscheidung, kein Bug.

---

## 8. Bekannte Fallstricke & Gotchas

### ⚠️ KRITISCH: `targetLat`/`targetLng` — NICHT `lat`/`lng`

Die Game-Engine verwendet für alle Pin-Modi ausschließlich die Feldnamen `targetLat` und `targetLng` im Question-Objekt `S.q`:

```javascript
// Engine-Scoring (haversine):
const dist = haversineKm(clickedLat, clickedLng, S.q.targetLat, S.q.targetLng);

// Auto-Zoom zur richtigen Region:
if (S.q.targetLat != null && S.q.type === "uk_pin") { ... }

// Correct-Pin-Anzeige nach Antwort:
if (readOnly && S.q && S.q.targetLat != null) { ... }
```

**Jeder Generator, der ein `uk_pin`-Question-Objekt zurückgibt, MUSS `targetLat`/`targetLng` verwenden.**

❌ **FALSCH** (Generator gibt falsche Feldnamen zurück → Distanz = NaN → 0 Punkte):
```javascript
return { type: "uk_pin", subj: item.n, lat: item.lat, lng: item.lng, ... };
```

✅ **RICHTIG:**
```javascript
return { type: "uk_pin", subj: item.n, targetLat: item.lat, targetLng: item.lng,
         ans: item.n, lid: "prefix_" + cat + "_" + idx, cc: null, ... };
```

**Pflichtfelder eines vollständigen `uk_pin`-Question-Objekts:**

| Feld | Typ | Bedeutung |
|------|-----|-----------|
| `type` | `"uk_pin"` | Fragetyp |
| `subj` | string | Anzeigename (ggf. spoiler-bereinigt) |
| `ans` | string | Vollständiger korrekter Name (nie im DOM) |
| `targetLat` | number | Breitengrad des Zielorts |
| `targetLng` | number | Längengrad des Zielorts |
| `lid` | string | Eindeutige Level-ID für Dedup |
| `cc` | string\|null | Ländercode (optional, für Flaggen-Icon) |
| `prompt` | string | Fragetext |

> **Hintergrund:** Dieser Bug trat in Phase 229–231 auf, weil die `_mkPinQ`-Factory-Funktion mit `lat`/`lng` implementiert wurde (analog zu den alten Einzelfunktionen), während `genUniversalPinQ` von Anfang an korrekt `targetLat`/`targetLng` nutzte. Symptom: Karte zeigt Pin bei (0,0), Feedback zeigt "0 km entfernt · 0 Pkt.". Fix: Phase 232, `_mkPinQ` auf `targetLat`/`targetLng` umgestellt.

---

### ⚠️ Neue MODE_CATS müssen in `_CAT_ORDER` ergänzt werden

`renderHomeTab()` verwendet eine Liste `_CAT_ORDER` zur Reihenfolge der Kategorien. Ab Phase 232 wird diese dynamisch befüllt — alle Einträge aus `MODE_CATS`, die nicht in der festen Liste sind, werden automatisch angehängt:

```javascript
const fixed = ["pure_geo", "lifestyle", ..., "tiere", "pflanzen", "gastronomie", ...];
const extra = Object.keys(MODE_CATS).filter(k => !fixed.includes(k));
const _CAT_ORDER = fixed.concat(extra);
```

Neue Kategorien erscheinen damit **automatisch** am Ende der Liste. Soll eine neue Kategorie an einer bestimmten Position erscheinen, muss sie manuell in `fixed` eingetragen werden.

---

### ⚠️ `KULTUR_DATA` unterstützt zwei Datenformate

Ältere Einträge in `data/kultur.json` sind **einfache Arrays**:
```json
"tiere_endemisch": [ {"n": "...", "lat": 1.0, "lng": 2.0}, ... ]
```

Neuere Einträge (ab Phase 227) sind **Objekte mit Prompt**:
```json
"tiere_zoos": { "prompt": "Wo liegt dieser Zoo?", "items": [ {"n": "...", "lat": 1.0, "lng": 2.0} ] }
```

`genUniversalPinQ` erkennt beide Formate automatisch:
```javascript
const data = Array.isArray(raw) ? raw : (raw.items || []);
const storedPrompt = Array.isArray(raw) ? null : raw.prompt;
```

Alle anderen Datendateien (`gastro_pin.json`, `tech_pin.json`, etc.) verwenden **ausschließlich** das Objekt-Format.

---

### ⚠️ Pin-Modus: Name des Ortes wird absichtlich angezeigt

Bei allen `uk_pin`-Modi (z.B. "Wo liegt dieser Solarpark?") wird der **Name des gesuchten Ortes im Fragetext angezeigt**. Das ist kein Bug — es ist das beabsichtigte Spielkonzept: Der Spieler kennt den Namen und muss die **Position auf der Karte** finden. Der kognitive Aufwand liegt im geografischen Wissen, nicht im Erraten des Namens.

> Der Name `subj` erscheint im Header. `ans` (vollständiger Name inkl. Klammern) wird **niemals** als DOM-Attribut gesetzt — Anti-Cheat bleibt gewahrt.

---

### ⚠️ Pin-Feedback: "0 Pkt." trotz Punkte — Anzeigebug-Muster

Das Feedback-Pill für `uk_pin`/`airport_pin` verwendet zwei separate Renderpfade:
- ✓ richtig (`S.ok = dist <= 250 km`): zeigt `+${apPts} Pkt.`
- ✗ falsch (`S.ok = false`): zeigte früher **hardcoded** `0 Pkt.`

**Tatsächlich werden Punkte auch bei falscher Antwort vergeben** (solange `dist < 2500 km`):
```javascript
const pts = Math.max(0, Math.round(500 * (1 - dist / 2500)));
if (pts > 0) { S.sc += pts; ... }  // ← Punkte werden IMMER addiert wenn > 0
```

Das Scoring: 500 Pkt. bei 0 km, 0 Pkt. ab 2500 km linear. Bei 1765 km = ca. 147 Pkt.

**Regel:** Niemals Punkte im `ng`-Pfad hardcoden — immer `apPts` auslesen:
```javascript
// ❌ FALSCH:
:`<div class="fb ng">✗ ${apDist} km · 0 Pkt.</div>`;

// ✅ RICHTIG:
:`<div class="fb ng">✗ ${apDist} km${apPts > 0 ? " · +" + apPts + " Pkt." : ""}</div>`;
```

---

### ⚠️ SVG-Kartenlabel: Lange Namen overflow die Karte

Die Korrekt-Antwort-Markierung nach einer Pin-Antwort rendert `S.q.ans` als SVG-Text. Lange Namen (z.B. "Hershey's, Hershey Pennsylvania") füllen die gesamte Kartenbreite.

**Regel:** Label immer auf max. 22 Zeichen kürzen:
```javascript
// ✅ RICHTIG:
.text((S.q.ans||"").length > 22 ? (S.q.ans||"").slice(0,20) + "…" : S.q.ans||"")
```

Gilt auch für `airport_pin` und alle künftigen Pin-Modi. `subj` (spoiler-bereinigt, kürzer) ist oft besser geeignet als `ans`.

---

### ⚠️ `unlock_and_push.bat` muss `git push origin main` enthalten

Das Bat-File committed nur lokal (`git commit`). Ohne `git push origin main` erreichen die Änderungen Vercel/GitHub nie. **Pflicht-Inhalt:**
```bat
git add -A
git commit -m "..."
git push origin main
```

Symptom wenn vergessen: `nothing to commit, working tree clean` beim zweiten Ausführen, aber deployed Version ist noch alt.

---

### ⚠️ verify.py kann Null-Bytes enthalten (Padding-Korruption)

Wenn `verify.py` mit `SyntaxError: source code cannot contain null bytes` fehlschlägt, hat das File binäre Null-Bytes als Padding bekommen. Fix:
```python
with open('verify.py', 'rb') as f: content = f.read()
with open('verify.py', 'wb') as f: f.write(content.replace(b'\x00', b''))
```

Ursache: bestimmte Edit-Operationen schreiben manchmal Padding an das Dateiende.

---

### ⚠️ KRITISCH: `_mkHL`-Factory muss `type:"beta_hl"` zurückgeben — NICHT `type:"hl"`

Die Render-Engine hat **keinen Handler für `type:"hl"`**. Die einzigen unterstützten H/L-Typen sind:
`hl_pop`, `hl_river`, `hl_area`, `uk_hl`, **`beta_hl`**

Ein Generator, der `type:"hl"` zurückgibt, führt sofort zum Crash:
```
Uncaught TypeError: Cannot read properties of undefined (reading 'map')
```
…weil die Engine `q.opts.map(...)` aufruft und `opts` bei `type:"hl"` undefiniert ist.

❌ **FALSCH** (`_mkHL`-Factory v1, Phase 229–231):
```javascript
return { type: "hl", a: {name, val}, b: {name, val}, unit, prompt, higherWins: true };
```

✅ **RICHTIG** — muss `beta_hl`-Format mit `opts`/`ans`/`meta` zurückgeben:
```javascript
return {
  type: "beta_hl",
  prompt: d.prompt || "Welches ist mehr?",
  subj: "",
  opts: [a.name, b.name],          // ← Pflicht: Array mit 2 Namen
  ans: higher.name,                 // ← Pflicht: Name des Gewinners
  meta: a.name+": "+a.val+" "+unit+" · "+b.name+": "+b.val+" "+unit,
  lid: "mhl_"+key+"_"+Math.min(ai,bi)+"_"+Math.max(ai,bi),
  cc: "de"
};
```

**Referenz-Implementierungen** (korrekt, getestet): `genTiereHL`, `genPflanzenHL`

**La-Paz-Window**: Items müssen nach `val` sortiert werden; Auswahl über Pool-Methode (nicht `do-while`), mit 2%-Mindestabstand-Check, damit triviale Paarungen (fast gleicher Wert) verhindert werden.

> **Hintergrund:** Phase 232 — `_mkHL` wurde mit `type:"hl"` implementiert (intuitiv wirkende Feldstruktur), ohne den Render-Code zu prüfen. Betroffen: alle H/L-Modi für Tech, E-Mob, Gastronomie und Archäologie (~50 Modi). Fix: `patch_fix_mkhl.py`.

---

*Dieses Dokument wird bei jedem signifikanten Architektur-Sprint aktualisiert.*
*Letztes Update: Phase 232 — Bugfixes Pin-Engine, Feedback-Pill, _mkHL beta_hl-Fix, Mai 2026.*
