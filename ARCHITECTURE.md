# GeoQuest — Architect's Handbook
## Systemdokumentation & Entwicklerhandbuch

**Version:** Phase 254 (Stand: Mai 2026)
**Build:** gen.py → 1.21 MB | GeoQuest.html → 2.36 MB | 677 Spielmodi | verify: 89/89

---

## Inhaltsverzeichnis

1. [Projektübersicht & Philosophie](#1-projektübersicht--philosophie)
2. [Build-Architektur](#2-build-architektur)
3. [Die 4 Universal-Engines](#3-die-4-universal-engines)
4. [Entwicklungs-Workflow & Tooling](#4-entwicklungs-workflow--tooling)
5. [State Management & Sicherheit](#5-state-management--sicherheit)
6. [Daten-Architektur](#6-daten-architektur)
7. [Modi-Registrierung & Routing](#7-modi-registrierung--routing)
8. [Service Worker & Offline-Architektur](#8-service-worker--offline-architektur)

---

## 1. Projektübersicht & Philosophie

### Was ist GeoQuest?

GeoQuest ist ein **vollständig clientseitiges, lokal persistiertes Geografie- und Wissens-Quiz** als Progressive Web App (PWA). Die gesamte Spiellogik, alle Daten und das vollständige UI befinden sich in einer einzigen HTML-Datei (`GeoQuest.html`), die ohne Server funktioniert.

**Kerneigenschaften:**

- **Zero-Backend-Dependency für Gameplay:** Alle Spielmodi laufen komplett offline. Supabase wird optional für Cloud-Highscores genutzt, ist aber kein Pflichtbestandteil.
- **Single-File Output:** Das Build-System kompiliert alle Quellen zu einer einzigen `GeoQuest.html`. Hosting = eine Datei deployen.
- **Clientseitige Persistenz:** Spielfortschritt, Einstellungen und Sammlungen werden über `localStorage` gespeichert. Ein kryptografischer Salt schützt die Daten vor Manipulation.
- **PWA-Ready:** Externer Service Worker (`sw.js`, hash-versioniert, generiert durch `gen.py`) cached die App und alle 37 Datendateien für vollständigen Offline-Betrieb nach erstem Laden.
- **Offline-Score-Queue:** Scores, die offline gespielt werden, landen in `localStorage` (`gq_offline_queue`) und werden bei Rückkehr ins Netz automatisch mit Supabase synchronisiert.

### Philosophie: Content ≠ Logic

Die zentrale Architekturentscheidung ist die strikte Trennung von **Inhalt** (Daten in `data/*.json`) und **Logik** (Engines in `gen.py`). Neue Tiere, Gerichte oder Sehenswürdigkeiten hinzufügen bedeutet nur eine JSON-Datei editieren — kein Python-Code anfassen.

---

## 2. Build-Architektur

### Das Drei-Schichten-Modell

```
┌─────────────────────────────────────────────────────┐
│  CONTENT-SCHICHT          data/*.json               │
│  37 Datendateien: Kultur, Tiere, Pflanzen, Gastro,  │
│  Tech, E-Mob, Archäologie, Astronomie, Geologie,    │
│  Sport-Wissen — je 4 Spieltypen                     │
├─────────────────────────────────────────────────────┤
│  LOGIK-SCHICHT            gen.py                    │
│  Spielengines, UI-Renderer, State-Management        │
│  Sprache: Python (Build) + JavaScript (Runtime)     │
├─────────────────────────────────────────────────────┤
│  OUTPUT-SCHICHT           GeoQuest.html             │
│  Single-File-Build: alles inline, kein CDN-Pflicht  │
│  Größe: ~2.36 MB, JS-Anteil ~2.32 MB               │
└─────────────────────────────────────────────────────┘
```

### Build-Ablauf: `python3 gen.py`

```
1. Python liest cities.json           → CJ  (JSON-String)
2. Python liest capitals.json         → CAPJ
3. Python liest data/kultur.json      → KULTUR_DATA_J
4. Python liest data/tiere_*.json     → TIER_*_J (3 Dateien)
5. Python liest data/pflanzen_*.json  → PFLANZEN_*_J
6. Python liest data/gastro_*.json    → GASTRO_*_J
7. Python liest data/tech_*.json      → TECH_*_J
8. Python liest data/emob_*.json      → EMOB_*_J
9. Python liest data/archaeologie_*.json → ARCH_*_J
10. Python liest data/astro_*.json       → ASTRO_*_J
11. Python liest data/geo_*.json         → GEO_*_J
12. Python liest data/sport_*.json       → SPORT_*_J
   ... (weitere Datensätze — 37 JSON-Dateien gesamt + kultur.json)

10. JS = r'''...'''                    Großer Raw-String mit gesamtem JavaScript.
                                       Enthält PLACEHOLDER_*-Marker.

11. JS = JS
    .replace('PLACEHOLDER_CJ',        CJ)
    .replace('PLACEHOLDER_KULTUR_DATA', KULTUR_DATA_J)
    .replace('PLACEHOLDER_TIER_HL_DATA', TIER_HL_DATA_J)
    ...                                Alle Daten werden injiziert.

12. re.sub(r'\\UXXXXXXXX', chr(...))   Unicode-Escapes werden aufgelöst.

13. HTML = _HTML_HEAD + JS + _HTML_TAIL
14. write('GeoQuest.html')
15. write('index.html')               Netlify-Deploy-Target

16. sw.js generieren (Phase 238):
    - Alle data/*.json (37 Stück) dynamisch gelistet
    - CACHE_NAME = 'geoquest-<md5[:8]>' — auto-bust bei Änderungen
    - write('sw.js')

17. manifest.json generieren (Phase 238):
    - theme_color: #10b981 (sync. mit CSS --accent)
    - icons: icon.svg only
    - write('manifest.json')
```

### Kritische Invarianten nach dem Build

| Invariante | Geprüft durch |
|-----------|---------------|
| Keine PLACEHOLDER_* mehr im Output | `verify.py` Check 4 |
| Alle 9 Datenobjekte vorhanden | `verify.py` Check 5 |
| JS-Syntax valide (`node --check`) | `verify.py` Check 3 |
| MODES-Array ≥ 200 Einträge | `verify.py` Check 6 |
| `_GQ_SALT` unverändert | `verify.py` Check 11 |
| sw.js: CACHE_NAME hash-versioniert | `verify.py` Check 12 |
| sw.js: alle 37 data/*.json in ASSETS | `verify.py` Check 12 |
| sw.js: Promise.allSettled vorhanden | `verify.py` Check 12 |

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

### ⚠️ Regel: Statistische Ausreißer in H/L-Datensätzen sind GEWOLLT — niemals automatisch löschen

**Kontext:** In `_hl.json`-Datensätzen tauchen naturgemäß Werte mit hohem Z-Score auf (z.B. Wanderratte: 7 Mrd. Individuen, Sauerbraten: 5760 min Zubereitungszeit, Röm. Heerstraßen: 400.000 km).

**Die Regel:** Statistische Ausreißer dürfen **niemals automatisch oder allein wegen eines hohen Z-Scores gelöscht werden**, sofern Faktenlage und Maßeinheiten korrekt sind.

**Begründung — zwei Schutzebenen:**

1. **Game Design:** Extreme Superlative ("die größten, schwersten, ältesten Dinge") sind essenzielle "Wow"-Momente für den Spielspaß. Sie zu entfernen macht das Spiel trivial.

2. **Architektur-Schutz (La-Paz-Fenster):** `_mkHL` sortiert den Datensatz vor jeder Abfrage nach Wert. Ein Extremwert auf Platz 1 tritt architektonisch zwingend nur gegen Platz 2 oder 3 an — ein triviales Duell "Größtes vs. Kleinstes" ist durch den Algorithmus bereits unmöglich.

**Anweisung für Validierung & Content-Erstellung:**

- Meldet `validate_content.py` einen Z-Score-Ausreißer (`[INFO]`), ist das **nur ein Hinweis zur Prüfung der Maßeinheiten** (z.B. "Wurden versehentlich Gramm mit Tonnen gemischt?").
- Sind Einheiten konsistent und der Fakt korrekt → Datensatz **zwingend erhalten**.
- `validate_content.py` gibt Z-Score-Ausreißer daher nur als stummen `[INFO]`-Print aus, **nicht** als `⚠ warn()`, um den QA-Warning-Count nicht künstlich aufzublähen.

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
- `gen.py` ist 1.21 MB groß. Manuelle Edits in solchen Dateien erzeugen leicht Syntaxfehler oder ruinieren Unicode-Encoding.
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
Phase: 240
Date:  2026-05-27
Author: Claude / Andre
Scope: Kurzbeschreibung (max. 80 Zeichen)

Description:
  Ausführliche Beschreibung. Welches Problem wird gelöst?
  Welche Anker werden verwendet? Gibt es Abhängigkeiten?

Dependencies: patch_238_offline_sw.py, patch_239_offline_ux.py
Zero-Bug Policy: All c.replace() calls use assert c.count(old)==1
"""
```

### `run_patch.py` — Der Patch-Runner

```bash
python3 run_patch.py patches/patch_240_offline_sync.py
```

**Was der Runner automatisch macht:**

```
1. Validiert den Pflicht-Header (Phase / Date / Scope)
2. Erstellt Backup: gen.py.bak_YYYYMMDD_HHMMSS
3. Führt das Patch-Skript aus
4. Führt python3 gen.py aus (Build)
5. Führt python3 verify.py aus (77 Checks)
   ↓ Bei FEHLER in Schritt 3, 4 oder 5:
   └─ Stellt gen.py aus dem Backup wieder her
   └─ Löscht das Backup
   └─ Bricht mit Fehlermeldung ab
   ↓ Bei ERFOLG:
   └─ Löscht das Backup (nicht mehr gebraucht)
   └─ Zeigt Build-Statistiken + nächste Schritte
```

### `verify.py` — Die 56 Pre-Push-Checks

`verify.py` wird automatisch durch `unlock_and_push.bat` vor jedem `git push` ausgeführt. Schlägt es an, bricht der Push ab.

| # | Check | Was geprüft wird |
|---|-------|-----------------|
| 0 | File presence | GeoQuest.html, gen.py, kultur.json, 4 tiere_*.json |
| 1 | HTML size | ≥ 1 MB (Regression-Schutz) |
| 2 | JS extraction | ≥ 500 KB JS aus 5 Script-Blöcken |
| 3 | JS syntax | `node --check` auf extrahiertem JS |
| 4 | Placeholder substitution | Keine `PLACEHOLDER_*` im Output |
| 5 | Data objects (9x) | KULTUR_DATA, TIER_*, WORTSCHMIEDE_DATA, MODES, MODE_CATS, GEN, plates |
| 6 | MODES count | ≥ 200 Einträge im MODES-Array |
| 7 | Generators (6x) | genUniversalPinQ, genTiereMatchQ, genTiereHL, initTierWortSchmiede, genHauptstadtDistanzQ, getSmartMatch |
| 8 | Anti-cheat | `_displaySubj` + `subj:_displaySubj` vorhanden |
| 9 | Mojibake | Keine neuen Â/Ã-Sequenzen (15 Legacy-Patterns whitelisted) |
| 10 | JSON round-trip | Alle 37 JSON-Dateien valide + Top-Level-Keys gezählt |
| 11 | _GQ_SALT | Salt im Output vorhanden (User-Saves-Schutz) |
| 12 | Service Worker | sw.js existiert, CACHE_NAME hash-versioniert, alle 37 data/*.json in ASSETS, Promise.allSettled vorhanden |

### Vollständiger Sprint-Workflow

```
1. Patch schreiben → patches/patch_NNN_beschreibung.py
2. python3 run_patch.py patches/patch_NNN_beschreibung.py
   → Auto-Build + Auto-Verify (77 Checks)
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

  // Offline-Status (Phase 240) — NICHT durch Anti-Cheat-Proxy geschützt
  isOffline: !navigator.onLine,  // wird durch online/offline Event-Listener aktualisiert
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

| Key | Inhalt | Typ |
|-----|--------|-----|
| `gq_langx` | Sprache (`"de"` / `"en"`) | String |
| `gq_usernamex` | Spielername | String |
| `gq_surv_bestx` | Survival-Highscore | Number |
| `gq_sessions_local` | Lokale Spiel-History (letzte 50 Sessions) | JSON |
| `gq_darkx` | Dark Mode aktiv | `"1"` / `"0"` |
| `gq_onboardingx` | Onboarding abgeschlossen | Boolean |
| `gq_spotter_countryx` | Letztes gewähltes Land im Kennzeichen-Spotter | String |
| `gq_offline_queue` | Offline-Score-Queue: `{pendingScore, pendingCoins}` | JSON |

**`gq_offline_queue`** (Phase 240): Akkumuliert Scores und Coins aus offline gespielten Sessions. Wird durch `syncOfflineData()` nach Rückkehr ins Netz geleert. Format: `{"pendingScore": 1500, "pendingCoins": 15}`.

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
const GUARDED_WRITE = new Set(["sc", "correct", "st", "bs", "pts", "collectedPlates", "sbProfile"]);

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

**Trusted Functions:** Die Whitelist umfasst alle Spielfunktionen die legitim Score-Felder schreiben dürfen:
`answer`, `startGame`, `mpCountdown`, `lq`, `nextRound`, `checkMastery`, `spotterCollect`, `saveSession`, `loadData`, `initAuth`, `handleGridAnswer`, `finishCustomGame`, `submitGridResult`, `render`, `renderWortSchmiede`, `renderLandHauptstadt`, `renderSLF`, `answerByIdx`, `handleWsCheck`, `handleSLFSubmit`, `handleLandHauptstadtSubmit`, `lvAnswer`, `syncOfflineData`

**`S.isOffline` ist bewusst NICHT in `GUARDED_WRITE`:** Die `online`/`offline`-Event-Listener (außerhalb der Trusted-Function-Liste) müssen `S.isOffline` direkt schreiben. Da `isOffline` kein spielrelevantes Score-Feld ist, stellt das kein Sicherheitsrisiko dar.

---

## 6. Daten-Architektur

### Dateistruktur

```
GeoQuest/
├── gen.py                  Haupt-Build-Skript (Logik, Engines, UI) — 1.21 MB
├── GeoQuest.html           Build-Output (Single-File-App) — 2.36 MB
├── index.html              Netlify-Deploy-Target (Kopie von GeoQuest.html)
├── sw.js                   Service Worker (generiert durch gen.py, hash-versioniert)
├── manifest.json           PWA Manifest (generiert durch gen.py)
├── icon.svg                App-Icon (alle Größen via SVG)
│
├── data/                   Content-Schicht (Phase 225–254, 37 Dateien + kultur.json)
│   ├── kultur.json             84 Kategorien: Getränke, Streetfood, Tänze, ...
│   ├── tiere_pin.json          10 Pin-Kategorien
│   ├── tiere_hl.json           13 H/L-Kategorien (Gewicht, Geschwindigkeit, ...)
│   ├── tiere_match.json        19 Match-Kategorien (Fährten, Lebensräume, ...)
│   ├── tiere_ws.json           11 Wort-Schmiede-Einträge
│   ├── pflanzen_pin.json       12 Pin-Kategorien
│   ├── pflanzen_hl.json        12 H/L-Kategorien
│   ├── pflanzen_match.json     15 Match-Kategorien
│   ├── pflanzen_ws.json         9 Wort-Schmiede-Einträge
│   ├── gastro_pin.json          9 Pin-Kategorien
│   ├── gastro_hl.json          15 H/L-Kategorien
│   ├── gastro_match.json       20 Match-Kategorien
│   ├── gastro_ws.json           7 Wort-Schmiede-Einträge
│   ├── tech_pin.json            8 Pin-Kategorien
│   ├── tech_hl.json             8 H/L-Kategorien
│   ├── tech_match.json         17 Match-Kategorien
│   ├── tech_ws.json            10 Wort-Schmiede-Einträge
│   ├── emob_pin.json           13 Pin-Kategorien
│   ├── emob_hl.json            12 H/L-Kategorien
│   ├── emob_match.json         22 Match-Kategorien
│   ├── emob_ws.json            10 Wort-Schmiede-Einträge
│   ├── archaeologie_pin.json   13 Pin-Kategorien
│   ├── archaeologie_hl.json    12 H/L-Kategorien
│   ├── archaeologie_match.json 28 Match-Kategorien
│   ├── archaeologie_ws.json     7 Wort-Schmiede-Einträge
│   ├── astro_pin.json           6 Pin-Kategorien
│   ├── astro_hl.json            9 H/L-Kategorien
│   ├── astro_match.json         9 Match-Kategorien
│   ├── astro_ws.json            4 Wort-Schmiede-Einträge
│   ├── geo_pin.json            14 Pin-Kategorien
│   ├── geo_hl.json             13 H/L-Kategorien
│   ├── geo_match.json          15 Match-Kategorien
│   ├── geo_ws.json              9 Wort-Schmiede-Einträge
│   ├── sport_pin.json          10 Pin-Kategorien
│   ├── sport_hl.json           10 H/L-Kategorien
│   ├── sport_match.json        11 Match-Kategorien
│   └── sport_ws.json            9 Wort-Schmiede-Einträge
│
├── cities.json             ~2315 kuratierte Städte (aus GeoNames)
│
├── verify.py               Post-Build-Selftest (77 Checks, Sektionen 0–12)
├── run_patch.py            Patch-Runner (Backup + Build + Verify + Rollback)
├── validate_content.py     Semantisches QA-Tool für data/*.json Dateien
│
├── patches/                Alle Patch-Skripte (Phase 212+)
│   ├── PATCHES.md          Konvention-Dokumentation
│   ├── patch_225_*.py      JSON-Extraktion
│   ├── patch_228_*.py      Pflanzen-Daten
│   ├── patch_229_*.py      Gastronomie
│   ├── patch_230_*.py      Tech & E-Mobilität
│   ├── patch_231_*.py      Archäologie
│   ├── patch_238_offline_sw.py   Service Worker + manifest.json
│   ├── patch_239_offline_ux.py   Auth UX: _authErrMsg + navigator.onLine guards
│   ├── patch_240_offline_sync.py Offline-Score-Queue + syncOfflineData
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

Alle anderen Kategorien (pflanzen, gastro, tech, emob, archaeologie) verwenden dieselben vier Dateistrukturen: `_pin.json`, `_hl.json`, `_match.json`, `_ws.json`.

---

## 7. Modi-Registrierung & Routing

### Das Drei-Strukturen-Prinzip

Jeder Spielmodus muss in genau drei Stellen synchron registriert sein:

```
MODES     → UI-Metadaten  (Titel, Gruppe, Prompt, Farbe, Icon)
MODE_CATS → Kategorisierung (Welche Kachel gehört zu welcher Kategorie)
GEN       → Dispatch-Table (mode-ID → Generator-Funktion)
```

**Aktueller Stand:** 677 Modi, 677/677/677 — perfekte Konsistenz.

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
  // ...677 Einträge total
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

**Daily Challenge:** Intentionell hardcoded auf `S.mode = "city"`. Die Daily Challenge ist ein tägliches globales Leaderboard-Event — alle Spieler weltweit spielen denselben Modus. Das ist eine bewusste Design-Entscheidung, kein Bug.

---

## 8. Service Worker & Offline-Architektur

### Überblick (Phase 238–240)

GeoQuest implementiert eine dreistufige Offline-Strategie:

```
Stufe 1 — SW-Cache (Phase 238):   App-Shell + alle 37 data/*.json offline verfügbar
Stufe 2 — Auth-UX (Phase 239):    navigator.onLine-Guards + _authErrMsg() für saubere Fehlermeldungen
Stufe 3 — Score-Queue (Phase 240): Optimistic writes → localStorage → Supabase bei Reconnect
```

### Service Worker (`sw.js`)

`sw.js` wird **nicht manuell gepflegt** — er wird bei jedem `python3 gen.py` Durchlauf frisch generiert.

**Hash-Versionierung:**
```python
_cache_assets = ['./GeoQuest.html', './index.html', './manifest.json', './icon.svg'] + _data_files
_cache_hash = hashlib.md5(''.join(_cache_assets).encode()).hexdigest()[:8]
_cache_name = 'geoquest-' + _cache_hash  # z.B. 'geoquest-a7d462a8'
```

Sobald eine Datei zu `data/` hinzukommt, entfernt wird oder umbenannt wird, ändert sich der Hash → altes Cache wird automatisch invalidiert.

**Caching-Strategie:**
- **Supabase-Requests** (`*.supabase.co`): Network-first, bei Fehler → leerer 503 (kein Cache)
- **Alle anderen Requests**: Cache-first; bei Cache-Miss → Network-fetch + Cache-put
- **Offline-Fallback**: Gibt `./GeoQuest.html` zurück, wenn kein Cache-Treffer und kein Netz
- **cities_data.js** (3.8 MB): Bewusst NICHT in ASSETS — zu groß für Install-Phase; wird lazy-gecacht beim ersten Fetch

**Non-Atomic Install via `Promise.allSettled`:**
```javascript
e.waitUntil(
  caches.open(CACHE_NAME).then(function(cache) {
    return Promise.allSettled(
      ASSETS.map(function(url) {
        return cache.add(url).catch(function(err) {
          console.warn('SW: skipped', url, err);  // Einzelfehler überspringen
        });
      })
    );
  })
);
```
Ein 404 für eine einzelne Datei verhindert nicht die Installation des gesamten Service Workers.

### Auth-UX Offline-Guards (Phase 239)

Alle vier Auth-Funktionen enthalten einen `navigator.onLine`-Guard der sofort eine deutschsprachige Fehlermeldung zeigt, ohne auf einen Supabase-Timeout zu warten:

```javascript
// doLogin, doRegister, doForgotPassword, doSetNewPassword:
if(!navigator.onLine){
  S.authError = "Du bist offline. Anmeldung ohne Internet nicht möglich.";
  render();
  return;
}
```

**`_authErrMsg(err)` Helper** (Phase 239): Behandelt fehlerhafte Supabase-Error-Objekte sicher:
```javascript
function _authErrMsg(err){
  if(!err) return '';
  const m = err?.message || err?.error_description || '';
  if(m && m.trim()) return m.trim();
  return 'Verbindungsfehler zum Server.';  // Fallback für {} aus 503-Body-Parse-Fehler
}
```
Verhindert, dass `{}` als Fehlermeldung im UI erscheint wenn Supabase offline ist.

### Offline Score Queue (Phase 240)

**Beim Spielen offline** schreibt `saveSession()` in die LocalStorage-Queue statt zu Supabase:

```javascript
if(!sb || !sbUser?.id || !navigator.onLine){
  if(score > 0){
    const _q = JSON.parse(localStorage.getItem('gq_offline_queue') || '{"pendingScore":0,"pendingCoins":0}');
    _q.pendingScore += score;
    _q.pendingCoins += Math.floor(score / 100);
    localStorage.setItem('gq_offline_queue', JSON.stringify(_q));
  }
  return;
}
// ... normaler Supabase-Write
```

**Beim Reconnect** ruft der `online`-Event-Listener `syncOfflineData()` auf:

```javascript
window.addEventListener('online', function(){
  S.isOffline = false;
  render();
  syncOfflineData();
});

async function syncOfflineData(){
  if(!sb || !sbUser?.id || !navigator.onLine) return;
  const _q = JSON.parse(localStorage.getItem('gq_offline_queue'));
  if(!_q || (!_q.pendingScore && !_q.pendingCoins)) return;
  await sb.rpc('add_score', {
    p_user_id: sbUser.id,
    p_score: _q.pendingScore || 0,
    p_coins: _q.pendingCoins || 0,
    p_rounds: 0,
    p_duration_ms: 0
  });
  localStorage.removeItem('gq_offline_queue');
  showToast('✅ Offline-Ergebnisse synchronisiert!');
  render();
}
```

**Offline-Banner im Profil-Tab:** Wenn `S.isOffline === true` erscheint eine rote Benachrichtigungsleiste im Profil-Tab, die den Nutzer informiert, dass Ergebnisse lokal zwischengespeichert und beim nächsten Online-Start automatisch synchronisiert werden.

---

## 9. Bekannte Fallstricke & Gotchas

### ⚠️ KRITISCH: `targetLat`/`targetLng` — NICHT `lat`/`lng`

Die Game-Engine verwendet für alle Pin-Modi ausschließlich die Feldnamen `targetLat` und `targetLng` im Question-Objekt `S.q`:

```javascript
// Engine-Scoring (haversine):
const dist = haversineKm(clickedLat, clickedLng, S.q.targetLat, S.q.targetLng);
```

**Jeder Generator, der ein `uk_pin`-Question-Objekt zurückgibt, MUSS `targetLat`/`targetLng` verwenden.**

❌ **FALSCH:**
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

> **Hintergrund:** Dieser Bug trat in Phase 229–231 auf, weil die `_mkPinQ`-Factory-Funktion mit `lat`/`lng` implementiert wurde, während `genUniversalPinQ` von Anfang an korrekt `targetLat`/`targetLng` nutzte. Symptom: Karte zeigt Pin bei (0,0), Feedback zeigt "0 km entfernt · 0 Pkt.". Fix: Phase 232, `_mkPinQ` auf `targetLat`/`targetLng` umgestellt.

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

Das Feedback-Pill für `uk_pin`/`airport_pin` verwendet zwei separate Renderpfade. **Tatsächlich werden Punkte auch bei falscher Antwort vergeben** (solange `dist < 2500 km`):

```javascript
const pts = Math.max(0, Math.round(500 * (1 - dist / 2500)));
```

Das Scoring: 500 Pkt. bei 0 km, 0 Pkt. ab 2500 km linear.

**Regel:** Niemals Punkte im `ng`-Pfad hardcoden — immer `apPts` auslesen:
```javascript
// ✅ RICHTIG:
:`<div class="fb ng">✗ ${apDist} km${apPts > 0 ? " · +" + apPts + " Pkt." : ""}</div>`;
```

---

### ⚠️ `_mkHL`-Factory muss `type:"beta_hl"` zurückgeben — NICHT `type:"hl"`

Die Render-Engine hat **keinen Handler für `type:"hl"`**. Die einzigen unterstützten H/L-Typen sind:
`hl_pop`, `hl_river`, `hl_area`, `uk_hl`, **`beta_hl`**

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

---

### ⚠️ `sw.js` wird bei jedem Build überschrieben

`sw.js` wird von `gen.py` generiert — manuelle Änderungen an `sw.js` werden beim nächsten `python3 gen.py` überschrieben. Alle SW-Anpassungen gehören in den GENERATORS-Block in `gen.py`.

---

### ⚠️ SVG-Kartenlabel: Lange Namen overflow die Karte

Die Korrekt-Antwort-Markierung nach einer Pin-Antwort rendert `S.q.ans` als SVG-Text. Lange Namen füllen die gesamte Kartenbreite.

**Regel:** Label immer auf max. 22 Zeichen kürzen:
```javascript
// ✅ RICHTIG:
.text((S.q.ans||"").length > 22 ? (S.q.ans||"").slice(0,20) + "…" : S.q.ans||"")
```

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

---

## 10. Supabase-Schema

GeoQuest nutzt Supabase für optionale Cloud-Features: Score-Sync, Leaderboards, Profil, Liga, Sammelmarken. Alle Features funktionieren auch ohne Supabase (localStorage-Fallback).

### Tabellen

**`profiles`** — Ein Eintrag pro registriertem User:

| Spalte | Typ | Beschreibung |
|--------|-----|--------------|
| `id` | uuid (PK) | Supabase Auth User-ID |
| `username` | text | Anzeigename |
| `total_score` | integer | Gesamtpunkte aller Zeiten |
| `games_played` | integer | Anzahl gespeicherter Sessions |
| `geo_coins` | integer | Aktuelle Münzen (Ingame-Währung) |
| `current_title` | text | Aktueller Titel (z.B. "Weltentdecker") |
| `joker_5050` | integer | Verbleibende 50/50-Joker |
| `joker_freeze` | integer | Verbleibende Freeze-Joker |
| `plates_collected` | jsonb | Gesammelte Kennzeichen `{cc: count}` |
| `stats_mastery` | jsonb | Mastery-Map `{cc: {n, p, t, ts}}` |
| `stats_history` | jsonb | Wöchentliche Score-History |
| `survival_best` | integer | Bester Survival-Score |
| `last_daily_date` | text | Datum der letzten Daily-Challenge (YYYY-MM-DD) |
| `league_id` | integer | Aktuelle Liga-Stufe |
| `league_score` | integer | Punkte in der aktuellen Liga-Woche |

**`game_sessions`** — Jede gespeicherte Spielsession:

| Spalte | Typ | Beschreibung |
|--------|-----|--------------|
| `id` | bigint (PK, auto) | Session-ID |
| `user_id` | uuid (FK → profiles) | Spieler |
| `mode` | text | Modus-ID (z.B. "city", "uk_getraenke") |
| `score` | integer | Erreichter Score |
| `best_streak` | integer | Bester Streak dieser Session |
| `rounds` | integer | Anzahl Runden (immer 10) |
| `accuracy` | integer | Trefferquote in % |
| `username` | text | Snapshot des Usernamens zum Zeitpunkt |
| `device_type` | text | `"mobile"` oder `"desktop"` |
| `created_at` | timestamptz | Timestamp |

**`leaderboard_weekly`** — View (kein direktes Insert möglich):

Gibt die wöchentliche Rangliste für einen Modus zurück. Wird über `sb.from("leaderboard_weekly").select("*").eq("mode", mode).order("rank")` abgefragt.

**`passport_stamps`** — Reisepass-Stempel (via `upsert_stamp` RPC):

Speichert pro User × Länderkürzel ob der Stempel gesammelt und ob Mastery erreicht wurde.

### RPCs (Stored Functions)

Alle schreibenden Score-Operationen laufen über RPCs — niemals direkte `UPDATE profiles SET total_score = ...` vom Client. Verhindert Client-seitige Manipulation.

| RPC | Parameter | Beschreibung |
|-----|-----------|--------------|
| `add_score` | `p_user_id`, `p_score`, `p_coins`, `p_rounds`, `p_duration_ms` | Addiert Score + Coins atomar auf das Profil. **Hauptfunktion nach jeder Session.** |
| `add_coins` | `p_user_id`, `p_amount` | Addiert Coins (Daily-Bonus, Titel-Belohnung). Gibt neuen Coins-Stand zurück. |
| `spend_coins` | `p_user_id`, `p_amount` | Subtrahiert Coins (Joker-Kauf, Modus-Unlock). Gibt neuen Stand zurück. Schlägt fehl wenn Saldo < Betrag. |
| `upsert_stamp` | `p_user_id`, `p_country_code`, `p_perfect` | Setzt/aktualisiert Reisepass-Stempel. |
| `get_prev_week_rank` | `p_user_id` | Gibt Vorwochenrang zurück (für Liga-Auswertung). |
| `update_league` | `p_user_id`, `p_new_league`, `p_eval_week` | Aktualisiert Liga-Stufe nach wöchentlicher Auswertung. |

### Client-Zugriff

```javascript
// Supabase-Client wird in gen.py konfiguriert:
const sb = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
let sbUser    = null;  // Supabase Auth User (nach Login)
let sbProfile = null;  // profiles-Zeile (nach loadProfile())
let sbOK      = false; // true sobald Auth + Profil geladen

// Globale Zustandscheck-Pattern:
if(!sb || !sbUser?.id) return;          // kein Login
if(!sbOK) return;                       // Profil noch nicht geladen
if(!navigator.onLine) { /* queue */ }   // kein Netz (Phase 240)
```

---

## 11. `validate_content.py` — Semantischer Content-Validator

`validate_content.py` prüft alle 37 `data/*.json` Dateien auf **inhaltliche** Qualitätsprobleme, die `verify.py` (Syntax/Struktur) nicht erkennen kann.

```bash
python3 validate_content.py          # Nur Warnungen ausgeben
python3 validate_content.py --strict # Exit 1 bei Warnungen (CI-Modus)
```

### Die 4 Prüfpfade

**Check 1 — Pin-Daten (`*_pin.json`, Pin-Einträge in `kultur.json`)**

| Prüfung | Was sie verhindert |
|---------|--------------------|
| Pflichtfelder `n`, `lat`, `lng` vorhanden | Silent fail: Pin bei (0,0) |
| `lat` ∈ [-90, 90], `lng` ∈ [-180, 180] | Unmögliche Koordinaten |
| Null-Island-Check: nicht beides = 0.0 | Vergessene Placeholder-Koordinaten |
| Duplikat-Koordinaten (4 Dezimalstellen ≈ 11m) | Zwei Orte auf identischem Pin |

**Check 2 — H/L-Daten (`*_hl.json`, `tiere_hl.json`)**

| Prüfung | Was sie verhindert |
|---------|--------------------|
| Pflichtfelder `name`, `val` | Generator gibt immer `null` zurück |
| Mindestens 6 Items | La-Paz-Window kann keinen validen Partner finden |
| Duplikate `name` | `lid`-Kollision → Dedup-System bricht |
| Negative Werte | Unbeabsichtigte Vorzeichen |
| Wert-Ratio > 10.000.000× | Gemischte Einheiten (g vs. kg, mm vs. km) |
| Z-Score-Ausreißer > 4σ | Tippfehler in Zahlenwert (z.B. 5000 statt 500) |

**Check 3 — Match-Daten (`*_match.json`, `tiere_match.json`, `kultur.json`-Match-Einträge)**

| Prüfung | Was sie verhindert |
|---------|--------------------|
| Pflichtfelder `n`, `c` | Silent fail im Generator |
| ≥ 4 unique `c`-Werte | Kein Distraktor-Pool für 3 falsche Antworten |
| Duplikate `n` (Subjekt) | Dieselbe Frage zweimal in einer Session |

**Check 4 — Wort-Schmiede-Daten (`*_ws.json`, `tiere_ws.json`)**

| Prüfung | Was sie verhindert |
|---------|--------------------|
| `word` vorhanden und GROSSBUCHSTABEN | Anagramm-Engine bricht |
| `word` nur Alpha-Zeichen, keine Leerzeichen | Zeichensatz-Fehler |
| `validWords[lang]` ist Array | Engine bricht beim Spielstart |
| Alle Lösungswörter GROSSBUCHSTABEN | Kein Match möglich |
| Lösungswort nicht länger als `word` | Logisch unmöglich |
| Anagramm-Validität: alle Buchstaben aus `word` entnehmbar | Spieler kann Wort physisch nicht legen |

### Automatische Format-Erkennung

`validate_content.py` erkennt den Dateityp automatisch anhand des Dateinamens-Suffix (`_pin`, `_hl`, `_match`, `_ws`) und bei `kultur.json` anhand der Datenstruktur (hat Einträge `lat`/`lng`? hat `val`? hat `c`?).

---

## 12. Phasen-Changelog

Kompakter Überblick aller signifikanten Patches seit dem Migrations-System (Phase 225).

| Phase | Datei | Inhalt |
|-------|-------|--------|
| 212 | `patch_212_kultur_modes.py` | 27 Kultur/Lifestyle Universal-Modi |
| 213 | `patch_213_perf_daily_1v1.py` | Performance, Daily-History, 1v1-Selector CSS |
| 214 | `patch_214_routing_audit.py` | Routing-Audit + Regressionen behoben |
| 215 | `patch_215_uk_engine.py` | UK-Engine-Modi registriert |
| 216 | `patch_216_universal_engine.py` | Universal-Engine + Custom-Mechanics |
| 220 | `patch_220_security_audit.py` | 5-Säulen Security & Stability Audit |
| 221a | `patch_221a_service_worker.py` | Service Worker Cache (blob-basiert, Phase 221) |
| 221b | `patch_221b_ws_multilingual.py` | Wort-Schmiede Multilingual-Bonus |
| 221c | `patch_221c_kompass_mode.py` | Sonnen-Kompass Rätsel — neuer Modus |
| 222 | `patch_222_stadion_hl.py` | Dynamischer Stadion-Höhe-H/L-Generator |
| 223 | `patch_223_map_zoom_fix.py` | Karten-Zoom D3 lid-Binding + Drag-vs-Click Guard |
| 223 | `patch_223_tiere_data_expand.py` | Tiere/Pferde Datensatz 20 → 68 Einträge |
| **225** | `patch_225_json_extraction.py` | **Daten aus gen.py nach `data/*.json` extrahiert** — Migrations-System eingeführt |
| 226 | `patch_226_ux_fixes.py` | UX-Fixes: Suche, HUD, HL-Buttons EN |
| 227a | `patch_227a_tiere_routing.py` | 21 Tiere-Modi Routing |
| 227b | `patch_227b_tiere_data_part1.py` | Tiere Pin + H/L Daten + Generatoren |
| 227c | `patch_227c_tiere_data_part2.py` | Tiere Match-Daten + Generator |
| 227d | `patch_227d_pferde_dlc.py` | Pferde DLC: Rassen, Fachbegriffe, Stockmaß, Flüsterer |
| 228 | `patch_228_pflanzen.py` | Pflanzen-Kategorie (4 JSON-Dateien, ~55 Modi) |
| 229 | `patch_229_gastronomie.py` | Gastronomie-Kategorie (4 JSON-Dateien, ~51 Modi) |
| 230 | `patch_230_tech_emob.py` | Tech + E-Mobilität (8 JSON-Dateien, ~110 Modi) |
| 231 | `patch_231_archaeologie.py` | Archäologie (4 JSON-Dateien, ~60 Modi) |
| 232 | *(inline)* | `_mkPinQ` auf `targetLat`/`targetLng` umgestellt; `_mkHL` auf `beta_hl` |
| 235 | `patch_235_fixes.py` | Qualitäts-Patch: BETA-Tags, Pflanzen-Gruppe, Datendichte |
| 236 | `patch_236_fixes.py` | Weitere QA-Fixes |
| 237 | `patch_237_qa_triage.py` | QA-Triage: Duplikate, WS-Validierung, Koordinaten |
| **238** | `patch_238_offline_sw.py` | **SW blob→external sw.js; hash-versioned CACHE_NAME; manifest.json; verify.py Sektion 12** |
| **239** | `patch_239_offline_ux.py` | **Auth-UX: `_authErrMsg()`, `navigator.onLine` Guards in 4 Auth-Funktionen** |
| **240** | `patch_240_offline_sync.py` | **`isOffline` State; online/offline Listener; Offline-Score-Queue; `syncOfflineData()`; Profil-Banner** |
| 241 | `patch_241_security_ux.py` | Security Cap (100k/1k), Gameover Offline-Banner, verify.py Section-0 dynamisch |
| 242 | `patch_242_engine_animals.py` | Tiere-Pin JSON, Daily 5-Mode-Rotation, Blitz-Modus (60s Speed-Round) |
| **243** | `patch_243_new_worlds.py` | **3 Neue Welten: Astronomie, Geologie, Sport-Wissen (12 JSON-Dateien, 32 Modi)** |
| 243b | `patch_243b_modes_fix.py` | 32 fehlende MODES-Einträge für Astro/Geo/Sport (leere Akkordeons gefixt) |
| 249 | `patch_249_polish.py` | Security: `submitRouteResult()` in `_TRUSTED_FNS`; PWA-Banner Fix; LS-TTL 90d; `run_patch.py` Pipeline-Upgrade |
| 250 | `patch_250_accordion_fix.py` | Akkordeon-Fix: `toggleAccordion()` delegiert an `filterByCategory()` |
| 251 | `patch_251_pwa_banner_scope_fix.py` | HOTFIX: `renderPwaBanner()` aus `renderBottomNav()` herausgelöst → Top-Level-Funktion |
| **252** | `patch_252_astro_expansion.py` | **Astronomie Expansion: 17 neue Modi — 4 Pin, 6 HL, 6 Match, 1 WS. MODES: 590→607** |
| **253** | `patch_253_geo_expansion.py` | **Geologie & Vulkane Expansion: 40 neue Modi — 12 Pin, 10 HL, 12 Match, 6 WS. MODES: 607→647** |
| **254** | `patch_254_sport_expansion.py` | **Sport-Wissen Expansion: 30 neue Modi — 8 Pin, 8 HL, 8 Match, 6 WS. MODES: 647→677** |

---

*Dieses Dokument wird bei jedem signifikanten Architektur-Sprint aktualisiert.*
*Letztes Update: Phase 254 — Sport-Wissen Expansion, 677 Modi, 37 Datendateien, Mai 2026.*
