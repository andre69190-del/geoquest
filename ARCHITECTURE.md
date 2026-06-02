# GeoQuest — Architect's Handbook
## Systemdokumentation & Entwicklerhandbuch

**Version:** Phase 449 (Stand: Juni 2026)
**Build:** gen.py → 1.49 MB | GeoQuest.html → 5.83 MB | 999 Spielmodi | verify: 159/159 | data: 60 JSON

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
- **PWA-Ready:** Externer Service Worker (`sw.js`, hash-versioniert, generiert durch `gen.py`) cached die App und alle 43 Datendateien für vollständigen Offline-Betrieb nach erstem Laden.
- **Offline-Score-Queue:** Scores, die offline gespielt werden, landen in `localStorage` (`gq_offline_queue`) und werden bei Rückkehr ins Netz automatisch mit Supabase synchronisiert.

### Philosophie: Content ≠ Logic

Die zentrale Architekturentscheidung ist die strikte Trennung von **Inhalt** (Daten in `data/*.json`) und **Logik** (Engines in `gen.py`). Neue Tiere, Gerichte oder Sehenswürdigkeiten hinzufügen bedeutet nur eine JSON-Datei editieren — kein Python-Code anfassen.

---

## 2. Build-Architektur

### Das Drei-Schichten-Modell

```
┌─────────────────────────────────────────────────────┐
│  CONTENT-SCHICHT          data/*.json               │
│  43 Datendateien: Kultur, Tiere, Pflanzen, Gastro,  │
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
   ... (weitere Datensätze — 44 JSON-Dateien gesamt (inkl. autos.json, autos_extended.json, games_extended.json))

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
| sw.js: alle data/*.json in ASSETS (43 Dateien) | `verify.py` Check 12 |
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

// Panning-Limits: eng begrenzt — kein Off-Screen mehr möglich (Phase 275)
zoom = d3.zoom()
  .scaleExtent([1, 10])
  .translateExtent([[-W*0.5, -H*0.5], [W*1.5, H*1.5]])
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
| 10 | JSON round-trip | Alle 44 JSON-Dateien valide + Top-Level-Keys gezählt |
| 11 | _GQ_SALT | Salt im Output vorhanden (User-Saves-Schutz) |
| 12 | Service Worker | sw.js existiert, CACHE_NAME hash-versioniert, alle 44 data/*.json in ASSETS, Promise.allSettled vorhanden |

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

**Aktueller Stand:** 999 Modi, 999/999/999 — perfekte Konsistenz.

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
Stufe 1 — SW-Cache (Phase 238):   App-Shell + alle 44 data/*.json offline verfügbar
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
          console.warn('SW: skipped', url, err);  // Einzelfehler ueberspringen
        });
      })
    );
  })
);
```
Ein 404 fuer eine einzelne Datei verhindert nicht die Installation des gesamten Service Workers.

### Auth-UX Offline-Guards (Phase 239)

Alle vier Auth-Funktionen enthalten einen `navigator.onLine`-Guard der sofort eine deutschsprachige Fehlermeldung zeigt, ohne auf einen Supabase-Timeout zu warten:

```javascript
// doLogin, doRegister, doForgotPassword, doSetNewPassword:
if(!navigator.onLine){
  S.authError = "Du bist offline. Anmeldung ohne Internet nicht moeglich.";
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
  return 'Verbindungsfehler zum Server.';  // Fallback fuer {} aus 503-Body-Parse-Fehler
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
```

**Offline-Banner im Profil-Tab:** Wenn `S.isOffline === true` erscheint eine rote Benachrichtigungsleiste im Profil-Tab.

---

## 9. Bekannte Fallstricke & Gotchas

### targetLat/targetLng -- NICHT lat/lng

Die Game-Engine verwendet fuer alle Pin-Modi ausschliesslich `targetLat` und `targetLng` im Question-Objekt `S.q`. Jeder Generator MUSS diese Feldnamen verwenden:

```javascript
// RICHTIG:
return { type: "uk_pin", subj: item.n, targetLat: item.lat, targetLng: item.lng,
         ans: item.n, lid: "prefix_" + cat + "_" + idx, cc: null, prompt: "..." };
// FALSCH:
return { type: "uk_pin", subj: item.n, lat: item.lat, lng: item.lng, ... };
```

Symptom wenn falsch: Karte zeigt Pin bei (0,0), Feedback zeigt "0 km entfernt, 0 Pkt."

### Neue MODE_CATS muessen in `_CAT_ORDER` ergaenzt werden

`renderHomeTab()` verwendet `_CAT_ORDER`. Neue Kategorien erscheinen automatisch am Ende der Liste. Soll eine Kategorie an einer bestimmten Position erscheinen, muss sie manuell in `fixed` eingetragen werden.

### `KULTUR_DATA` unterstuetzt zwei Datenformate

Aeltere Eintraege: einfaches Array `[{n, lat, lng}]`. Neuere Eintraege: Objekt `{prompt, items:[{n, lat, lng}]}`. `genUniversalPinQ` erkennt beide Formate automatisch.

### `_mkHL`-Factory muss `type:"beta_hl"` zurueckgeben

Die Render-Engine hat keinen Handler fuer `type:"hl"`. Unterstuetzte H/L-Typen: `hl_pop`, `hl_river`, `hl_area`, `uk_hl`, `beta_hl`. Referenz-Implementierungen: `genTiereHL`, `genPflanzenHL`.

### `sw.js` wird bei jedem Build ueberschrieben

Manuelle Aenderungen an `sw.js` werden beim naechsten `python3 gen.py` ueberschrieben. Alle SW-Anpassungen gehoeren in den GENERATORS-Block in `gen.py`.

### SVG-Kartenlabel: Lange Namen overflow die Karte

Label immer auf max. 35 Zeichen kuerzen (Phase 274: 22→35):
```javascript
.text((S.q.ans||"").length > 35 ? (S.q.ans||"").slice(0,33) + "…" : S.q.ans||"")
```

### `unlock_and_push.bat` muss `git push origin main` enthalten

Ohne `git push origin main` erreichen Aenderungen Vercel/GitHub nie.

### verify.py kann Null-Bytes enthalten

Fix: `content.replace(b'\x00', b'')`

---

## 10. Supabase-Schema

GeoQuest nutzt Supabase fuer optionale Cloud-Features: Score-Sync, Leaderboards, Profil, Liga, Sammelmarken.

### Tabellen

**`profiles`** -- Ein Eintrag pro registriertem User:

| Spalte | Typ | Beschreibung |
|--------|-----|--------------|
| `id` | uuid (PK) | Supabase Auth User-ID |
| `username` | text | Anzeigename |
| `total_score` | integer | Gesamtpunkte |
| `games_played` | integer | Anzahl Sessions |
| `geo_coins` | integer | Muenzen (Ingame-Waehrung) |
| `current_title` | text | Aktueller Titel |
| `joker_5050` | integer | 50/50-Joker |
| `joker_freeze` | integer | Freeze-Joker |
| `plates_collected` | jsonb | Gesammelte Kennzeichen |
| `stats_mastery` | jsonb | Mastery-Map |
| `stats_history` | jsonb | Woechentliche Score-History |
| `survival_best` | integer | Bester Survival-Score |
| `last_daily_date` | text | Datum der letzten Daily-Challenge |
| `league_id` | integer | Aktuelle Liga-Stufe |
| `league_score` | integer | Punkte in aktueller Liga-Woche |

**`game_sessions`** -- Jede gespeicherte Spielsession:

| Spalte | Typ | Beschreibung |
|--------|-----|--------------|
| `id` | bigint (PK) | Session-ID |
| `user_id` | uuid | Spieler |
| `mode` | text | Modus-ID |
| `score` | integer | Erreichter Score |
| `best_streak` | integer | Bester Streak |
| `rounds` | integer | Anzahl Runden (immer 10) |
| `accuracy` | integer | Trefferquote in % |
| `device_type` | text | mobile / desktop |

### RPCs

| RPC | Beschreibung |
|-----|--------------|
| `add_score` | Addiert Score + Coins atomar |
| `add_coins` | Addiert Coins |
| `spend_coins` | Subtrahiert Coins (Joker-Kauf) |
| `upsert_stamp` | Reisepass-Stempel |
| `get_prev_week_rank` | Vorwochenrang |
| `update_league` | Liga-Stufe aktualisieren |

---

## 11. `validate_content.py` -- Semantischer Content-Validator

`validate_content.py` prueft alle 37 `data/*.json` Dateien auf inhaltliche Qualitaetsprobleme.

```bash
python3 validate_content.py          # Nur Warnungen
python3 validate_content.py --strict # Exit 1 bei Warnungen (CI-Modus)
```

**Check 1 -- Pin-Daten:** Pflichtfelder n/lat/lng, Koordinaten-Bereich, Null-Island, Duplikat-Koordinaten.

**Check 2 -- H/L-Daten:** Pflichtfelder name/val, mind. 6 Items, keine Duplikate, keine negativen Werte, Ratio-Check > 10Mx, Z-Score > 4sigma (nur Info).

**Check 3 -- Match-Daten:** Pflichtfelder n/c, mind. 4 unique c-Werte, keine Duplikate n.

**Check 4 -- WS-Daten:** word vorhanden/Grossbuchstaben, validWords ist Array, alle Loesungswoerter bildbar aus word-Buchstaben.

---

## 12. Phasen-Changelog

| Phase | Datei | Inhalt |
|-------|-------|--------|
| 212 | patch_212_kultur_modes.py | 27 Kultur/Lifestyle Universal-Modi |
| 213 | patch_213_perf_daily_1v1.py | Performance, Daily-History, 1v1-Selector CSS |
| 214 | patch_214_routing_audit.py | Routing-Audit + Regressionen |
| 215 | patch_215_uk_engine.py | UK-Engine-Modi registriert |
| 216 | patch_216_universal_engine.py | Universal-Engine + Custom-Mechanics |
| 220 | patch_220_security_audit.py | 5-Saeulen Security & Stability Audit |
| 221a | patch_221a_service_worker.py | Service Worker Cache |
| 221b | patch_221b_ws_multilingual.py | Wort-Schmiede Multilingual-Bonus |
| 221c | patch_221c_kompass_mode.py | Sonnen-Kompass Raetsel |
| 222 | patch_222_stadion_hl.py | Dynamischer Stadion-Hoehe-H/L-Generator |
| 223 | patch_223_map_zoom_fix.py | Karten-Zoom D3 lid-Binding + Drag-vs-Click Guard |
| 223 | patch_223_tiere_data_expand.py | Tiere/Pferde Datensatz 20->68 Eintraege |
| **225** | patch_225_json_extraction.py | **Daten aus gen.py nach data/*.json extrahiert** |
| 226 | patch_226_ux_fixes.py | UX-Fixes: Suche, HUD, HL-Buttons EN |
| 227a | patch_227a_tiere_routing.py | 21 Tiere-Modi Routing |
| 227b | patch_227b_tiere_data_part1.py | Tiere Pin + H/L Daten + Generatoren |
| 227c | patch_227c_tiere_data_part2.py | Tiere Match-Daten + Generator |
| 227d | patch_227d_pferde_dlc.py | Pferde DLC: Rassen, Fachbegriffe, Stockmass, Fluesterer |
| 228 | patch_228_pflanzen.py | Pflanzen-Kategorie (4 JSON, ~55 Modi) |
| 229 | patch_229_gastronomie.py | Gastronomie-Kategorie (4 JSON, ~51 Modi) |
| 230 | patch_230_tech_emob.py | Tech + E-Mobilitaet (8 JSON, ~110 Modi) |
| 231 | patch_231_archaeologie.py | Archaeologie (4 JSON, ~60 Modi) |
| 235 | patch_235_fixes.py | Qualitaets-Patch: BETA-Tags, Pflanzen-Gruppe |
| 236 | patch_236_fixes.py | Weitere QA-Fixes |
| 237 | patch_237_qa_triage.py | QA-Triage: Duplikate, WS-Validierung, Koordinaten |
| **238** | patch_238_offline_sw.py | **SW blob->extern; hash-versioned CACHE_NAME; manifest.json** |
| **239** | patch_239_offline_ux.py | **_authErrMsg(), navigator.onLine Guards** |
| **240** | patch_240_offline_sync.py | **isOffline State; Score-Queue; syncOfflineData()** |
| 241 | patch_241_security_ux.py | Security Cap, Gameover Offline-Banner, verify.py Section-0 |
| 242 | patch_242_engine_animals.py | Tiere-Pin JSON, Daily 5-Mode-Rotation, Blitz-Modus |
| **243** | patch_243_new_worlds.py | **3 Neue Welten: Astronomie, Geologie, Sport-Wissen (32 Modi)** |
| 243b | patch_243b_modes_fix.py | 32 fehlende MODES-Eintraege fuer Astro/Geo/Sport |
| 249 | patch_249_polish.py | Security, PWA-Banner Fix, LS-TTL 90d |
| 250 | patch_250_accordion_fix.py | Akkordeon-Fix: toggleAccordion() |
| 251 | patch_251_pwa_banner_scope_fix.py | HOTFIX: renderPwaBanner() Top-Level-Funktion |
| **252** | patch_252_astro_expansion.py | **Astronomie Expansion: 17 Modi. MODES: 590->607** |
| **253** | patch_253_geo_expansion.py | **Geologie Expansion: 40 Modi. MODES: 607->647** |
| **254** | patch_254_sport_expansion.py | **Sport-Wissen Expansion: 30 Modi. MODES: 647->677** |
| 255 | patch_255_supabase_feedback.py | Supabase feedback-Tabelle, domain-check |
| 256 | patch_256_tts_feedback.py | TTS (Web Speech API), openFeedback()-Modal, Supabase-Write |
| 257 | patch_257_hud_cleanup.py | HUD: Fehler-Button entfernt, Buttons kleiner, 💡 Startseite, TTS-Highlight |
| **258** | patch_258_pferde.py | **Pferde-Expansion: +4 Modi (MODES: 677->681). Offline-Feedback-Queue** |
| **259** | patch_259_data_expansion.py | **Data Expansion Sprint: 15 Modi aufgefüllt (+297 Einträge). 14x Kultur-Match 5→25, canyons 8→25** |
| **260** | patch_260_astro_massive.py | **Astronomie Massive Expansion: 20 Astro-Modi skaliert (+547 Einträge). astro_pin/hl/match auf 28-58 Items** |
| **261** | patch_261_geo_massive.py | **Geologie Massive Expansion: 20 Geo-Modi skaliert (+664 Einträge). geo_pin 8→38-48, geo_hl 8→36-46, geo_match 8→45-54** |
| **262** | patch_262_sport_massive.py | **Sport-Wissen Massive Expansion: 17 Sport-Modi skaliert (+608 Einträge). sport_pin 8→35-47, sport_hl 8→41-49, sport_match 8→50-54** |
| **263** | post_phase.py | **post_phase.py CLI Tooling implementiert** |
| **264** | patch_264_mega_sweep.py | **Mega-Sweep: tiere_pin/arch_match/emob/gastro/tech/pflanzen auf 40+ skaliert (+667 Eintraege). Coord-Dedup Guard aktiv** |
| **265** | patch_265_geo_sport_astro_sweep.py | **Geo/Sport/Astro Sweep: 40 Modi auf 25-40 Items skaliert. +787 Eintraege. Arch-Match Restluecken geschlossen.** |
| **266** | Timeline-Engine | **Timeline-Modus: Drag-and-Drop Zeitleiste. genTimelineQ + 4 neue Modi. data/timeline.json (96 Items).** |
| **267** | patch_267_hardcore.py | **Hardcore-Modus: Persistenz (gq_diffx), H/L 3%/10%, Pts x1.5, Profil-Toggle + Feedback-Card. 685 Modi.** |
| **268** | patch_268_spieluebersicht.py | **Zero-Blank-Policy Spieluebersicht: 130 fehlende Werte aufgeloest. 685/685 Modi mit Datenbasis-Wert.** |
| **269** | patch_269_final_fill.py | **Final Fill Sprint: 15+ JSON-Datensaetze auf 40-50 Items skaliert (emob, tech, gastro, pflanzen, tiere, timeline, kultur).** |
| **270** | patch_270_global_sweep.py | **Datendichte-Fix: 29 kultur.json-Datensaetze auf 40-50 Items skaliert. Spieluebersicht Datenbasis: 51.927 Items.** |
| **271** | patch_271_fill_to_50.py + topup | **Full-to-50 Sprint: Alle ausbaufaehigen Arrays auf ≥50 Items. BETA-Praefixe entfernt (70x). Jersey/Crest 15/10→50.** |
| **272** | patch_272_sport_poi_fill.py + 272b | **SPORT_POI Full-to-50 Sprint: Alle 18 SPORT_POI_GAMES auf 50 POIs (derby, eishockey, f1, tdf, fussball, olympia u.v.m.). UEFA_STADIUMS 28→50. geo_pin Fossilien/Graeben/Rifts/Geoparks 8→30-40. hohe_stadien 9→30, leichtathletik_wm 13→19. BETA komplett entfernt aus gen.py (0x Python, 0x JS). GeoQuest.html 3.79 MB.** |
| **273** | patch_273_schaetzer_fix.py | **Distanz-/Flugzeit-Schätzer Fix: JSON c-Werte normalisiert (einheitliches Format), ansPool in gen.py von 10→44 (distanz) und 8→15 (flugzeit) unique Werte erweitert. Spielübersicht: 10→50 Distanzen, 8→50 Flugzeiten.** |
| **274** | gen.py direkt | **Pin-Modus Anti-Spoiler: _mkPinQ zeigt jetzt nur Basisname ohne Stadt/Land in Klammern (subj=_dispSubj). Feedback-Label 22→35 Zeichen. "Levi's Stadium" statt "Levi's Stadium (Santa Clara, USA)" während Frage.** |
| **275** | gen.py direkt | **Pin-Map Scroll-Fix: translateExtent [-W,-H→2W,2H] → [-0.5W,-0.5H→1.5W,1.5H] (kein Off-Screen mehr). Reset-Button ↺ erscheint nach erstem Panning-Touch, zoomt zurück zur Zielregion oder Vollwelt.** |
| **276** | gen.py direkt | **Pin-Map Random-Offset: Zielort landet zufällig bei -10%...+110% des Viewports (gelegentlich außerhalb Rand). Anti-Cheat: Mitte-klicken hilft nicht mehr. Reset-Button stellt gleiche Zufallsposition wieder her.** |
| **277** | patch_277_zindex_fix.py | **Z-Index Bleeding Fix: bottom-nav z-index 300→1000, Fav/Info-Buttons 99999→2, body padding-bottom 68→80px. Buttons verschwinden sauber hinter Tab-Bar beim Scrollen.** |
| **278** | patch_278_push80_tiere_sport.py | **Data Sprint Push-to-80: 12 SPORT_POI_GAMES-Arrays (derby/eishockey/f1/tdf/olympia/wm/em/fussball/sommerspiele/rekorde) + UEFA_STADIUMS_DATA von 50→80 Items. 6 Hard-Limit-Arrays korrekt übersprungen. GeoQuest.html 4.43 MB.** |
| **279** | patch_279_mobile_pwa_landscape.py | **Mobile Fix: iOS PWA-Install (_isIOS + _isInStandaloneMode, Share-Button-Anleitung). Landscape-Detection: screen.orientation.type API, Timeout 120→350ms, resize-Event (debounced 200ms).** |
| **280** | patch_280_bugfixes.py | **Critical Bugfixes: _mkMatchQ + genFootballQ fehlende lid-Felder (Dedup-Fix). genFootballQ Math.random→rng() (MP-Sync). _lvNext opts-Guard (8 Retries, verhindert pin-Modi ohne Buttons im 1v1). _footballData.crests 10→51 Einträge (eindeutige shape+color-Paare).** |
| **281** | patch_281_1v1_sync.py |
| **282** | patch_282_lv_ux.py |
| **283** | patch_283_feedback_email.py | **Feedback-System: reportBug+Crash-Handler schreiben jetzt in Supabase (nicht nur mailto). Admin-Tab zeigt alle Feedback-Eintraege. KRITISCHER MP-FIX: initRng(seed) NACH startGame aufgerufen (startGame hatte rngSeed=null auf Zeile 10582 – dieser Root Cause erklaert ALLE falschen Online-MP-Fragen). verify: 137/137.** | **1v1 UX: Wort-Schmiede-Modi aus Spielauswahl entfernt (noMultiplayer-Filter). lv.lastP1Result gespeichert. Handoff-Screen zeigt jetzt Ergebnis-Badge: ✅ Richtig / ❌ Falsch / ⏱ Zeit.** | **1v1 Sync Fix: mpCountdown render() bei jedem Tick (Countdown zeigte nur "3"). 11x Math.random()→rng() in Fragen-Generatoren (getSmartVersusOpponent, getVersusCountryPair/-Advanced, getFlagFusionPairSafe, renderFlagFusion, initLogikGitter, renderTravelRoute) – gleicher Seed = gleiche Fragen.** |
| **284** | patch_284_daily_exploit.py | **Daily-Challenge Exploit-Fix: startDailyChallenge() setzte bisher KEIN Flag beim Start → Spieler konnte beliebig oft neu starten bis der Score passte. Fix (Option B – Resume statt Hard-Fail): neue Helper getDailyProgressKey/saveDailyProgress/loadDailyProgress, Start-Flag (gq_daily_prog_YYYY-MM-DD) wird SOFORT beim Erst-Start gesetzt, Progress nach jeder Antwort gespeichert, Resume bei Wiederkehr (Tages-Seed + askedLids wiederhergestellt), markDailyDone() löscht Progress-Key, renderDailyHero() zeigt Fortsetzen-Karte. verify: 137/137.** |
| **285** | patch_285_mp_sync.py | **1v1-Online-Sync-Fix ("Höheres BIP" zeigte unterschiedliche Fragen): (1) S.filter + S.diff wurden nie synchronisiert — die Vergleichs-Generatoren (_compPick→_rfilt nutzt S.filter, getSmartMatch-Fenster nutzt S.diff) lieferten daher trotz gleichem Seed andere Länder; game_start-Payload jetzt um {filt,dif} erweitert, Host autoritativ, mpCountdown wendet sie vor startGame an. (2) Runde 1 wurde vor initRng generiert (rngSeed=null in startGame, initRng erst danach) → erste Frage lief auf Math.random(); startGame(m,_mpSeed) seedet jetzt VOR dem ersten lq(). verify: 137/137.** |
| **286** | patch_286_mp_show_opp_answer.py | **1v1-Online: Gegner-Auswahl sichtbar. score_update überträgt jetzt zusätzlich {sel,selOk,lid}; Empfänger speichert S.mpOppSel/mpOppSelOk/mpOppLid. Anzeige nur bei lid-Match: (a) universelle Zeile unter der Duell-Leiste "⚔ <Gegner> wählte: <Auswahl> ✓/✗" (alle Modi), (b) Schwert-Marker auf dem vom Gegner gewählten Options-Button (z.B. Höheres BIP). Resets in mpCountdown + startGame. verify: 137/137, node --check OK.** |
| **287** | patch_287_i18n_de_en_pl.py | **i18n de/en/pl. (A) 15 hartkodierte deutsche Frage-Prompts (curr_real, neighbor×2, neighbor_fake, neighbor_count, border_q, de_plate, map_reverse, stadium, jersey, crest, beta_hl, beta_spotter, sport_poi, wappen) auf t() umgestellt — deutscher Wert 1:1 aus Original, en+pl ergänzt, übrige Sprachen Fallback EN. (B) LANG.pl von 115→158 Schlüssel komplettiert (inkl. Wort-Schmiede-UI) → de/en/pl jetzt alle 158, 0 Lücken. Andere 21 Sprachen bewusst unverändert. verify: 137/137, node --check OK.** |
| **288** | patch_288_pl_content_i18n.py | **Polnische Spielinhalte für 5 Rubriken (E-Mobilität, Archäologie, Astronomie, Geologie, Sport). NEU: erweiterbare Inhalts-Übersetzung `_CONTENT_I18N={pl:{…}}` + Helper `_tc(s)` (weitere Sprachen einfach ergänzbar). Übersetzt: 196 Frage-Prompts + 54 Einheiten + 79 Match-Antwort-Buttons/Länder (fixedOpts). Verdrahtet in _mkPinQ (prompt), _mkHL (prompt+unit), _mkMatchQ (prompt + opts/ans konsistent). Eigennamen/Codes (CCS, Tesla, ISO 15118 …) fallen unverändert durch. Offen: `.c`-Distraktor-Buttons in astro/geo/sport-Match (Länder/Eigennamen/offener Text) bleiben DE. verify: 137/137, node --check OK.** |
| **289** | patch_289_comp_i18n.py | **comparisons-Kategorie de/en/pl: comp_* Prompts (hartkodiert DE) über _tc lokalisiert — _compQ zentral gewrappt (11 Vergleiche) + 5 Spezial-Generatoren (Flughäfen/Gipfel/Olympia, mit Emoji). _CONTENT_I18N auf gültiges JSON normalisiert. +16 en/pl. verify: 137/137.** |
| **290** | patch_290_beta_i18n.py | **HL-Beta + Beta-Modi de/en/pl: genHLBeta (26 HL_BETA_PROMPTS), genBetaMCQ (100 Fragen), genBetaHL (3 Prompts) über _tc gewrappt; 129 dt. Strings → en+pl (indexbasiertes Mapping). verify: 137/137, node --check OK.** |
| **291** | patch_291_en_5cats.py | **Englisch für die 5 Rubriken: _CONTENT_I18N.en += 329 (196 Prompts + 54 Einheiten + 79 fixedOpts) — englische Entsprechungen der in P288 polnisch übersetzten Strings. Validierung: jeder Schlüssel existiert bereits in .pl. Damit die 5 Rubriken jetzt de/en/pl. verify: 137/137, node --check OK. Siehe GeoQuest_i18n_Audit.md.** |
| **292** | patch_292_tpgt_i18n.py | **Tiere/Pflanzen/Gastronomie/Technologie de/en/pl. genTiere*/genPflanzen*/genUniversal* mit _tc gewrappt (Prompt, Einheit, Match opts/ans); gastro/tech via bereits gewrappte _mk*. +337 en/pl (162 Prompts + 36 Einheiten + 139 fixedOpts, Eigennamen als Identität). verify: 137/137, node OK.** |
| **293** | patch_293_country_answers.py | **Länder-Antwortwerte der Match-Modi lokalisiert. NEU _tcc(s): dt. Ländername→cc→displayCountry (en/pl), sonst Fallback _tc. In alle Match-opts/ans eingebaut (statt _tc). Annotierte Werte bleiben über _tc-Fallback. verify: 137/137, node OK.** |
| **294** | patch_294_clean_c_categories.py | **Saubere .c-Kategorien de/en/pl: Gesteinsklassen, Kristallsysteme, Erdzeitalter, Sternenhimmel, Kontinente (101 Werte, alle distinct .c je Gruppe → keine gemischten Button-Sprachen). verify: 137/137, node OK.** |
| **297** | patch_297.py | **DS100 Hardcore Input-Modus + Zug-Depot Sammelalbum** |
| **298** | patch_298.py | **Metro-Logos weltweit + Trainspotter Expansion (Routen, Architektur, Hersteller)** |
| **299** | patch_299.py | **Taktfrequenz H/L + Rekord-Pin + Bahnhofs-Timeline (3 neue Zug-Modi)** |
| **300** | patch_300.py | **Grand Data Upscale: alle 4 Zug-Arrays auf 80 Items (zug_routen, bahnhof_typ, hersteller, metro_logos)** |
| **301** | patch_301.py | **Bugfixes: Crash-Guard, Pferde-HL-Key, WS-Cleanup, Züge-Kategorie sichtbar, landing.html aktualisiert** |
| **302** | patch_302.py | **Housekeeping: Duplikate entfernt, alle Zug-Arrays auf 80 Items (taktfrequenz, panorama, vkm, bahnhof_bau)** |
| **303** | patch_303.py | **Bugfix: breitengrad_match aus Match-Distractor-Pool entfernt (Koordinaten als Antwortoptionen)** |
| **304** | patch_304.py | **i18n-Fix: Züge-Kategorie vollständig übersetzt (EN+PL) — DS100, Metro-Logos, Depot-Labels** |
| **305** | patch_305.py | **KRITISCH: showTrainDepot aus answer()-Scope in globalen Scope verschoben — Crash auf Album-Tab behoben** |
| **306** | patch_306.py | **Spotter-Dashboard: Depot-Widget mit Progress-Bar (ab 10 Items) + i18n EN/PL** |
| **307** | patch_307.py | **Upscale: zug_rekorde_pin/ds100 auf 80, geo_pin/tiere_pin repariert, Spieluebersicht-Regex fix** |
| **308** | patch_308.py | **WS-Fixes (NIGHTJET/FLIXZUG/ACELA), Validator-Update (i18n-Check, metro_logos, timeline), WS-Modi ws_zug_panorama + ws_zug_nightjet** |
| **309** | patch_309.py | **KRITISCH: _tc() TDZ-Fix (S before initialization), _tc() aus MODES entfernt** |
| **310** | patch_310.py | **Zug-Streak-Badge + Daily Train Challenge (Zug-Tag-Indikator, 10 Zug-Modi im Pool)** |
| **315** | patch_315.py | **UIC-Scanner, Live-Spotting UI, Unified Spotter Dashboard (Tabs+Swipe), Waggon-Album Shortcut in Züge-Kategorie** |
| **320** | patch_320.py | **MP Sync: Lock & Reveal, Anti-Cheat, Disconnect UX, Score/Round Buffer, 5500ms Reveal Delay (Phasen 316-320)** |
| **321** | patch_321.py | **Neue Modi: Reisezeit-Schätzer (MC) + Strecken-Duell (HL) — 80 europäische Zugstrecken, zug_uic_laender-Duplikat entfernt** |
| **322** | patch_322.py | **Zug-Reisezeiten Upgrade: Heimvorteil-Algorithmus (70/30, land-basiert), 177 Strecken, Zugtyp im Strecken-Duell, genZugReisezeitHL verbessert** |
| **323** | patch_323.py | **Kultur-Balancing: wahrzeichen +40, museen +23, kunstwerke +21 — 16 unterrepräsentierte Länder (PL/CZ/HU/RO/SE/NO/FI/DK/HR/BG/BE/SK/NL/PT) ergänzt** |
| **324** | patches/patch_324_gastro_balancing.py | **Gastronomie-Arrays geografisch ausbalanciert: nationalgerichte (+30), streetfood (neu, 32), hausmannskost (+20), suessspeisen (neu, 31) — Fokus Ziel-Länder EU-Ost/Nord/West** |
| **325** | patches/patch_325_kultur_balancing.py | **Kultur-Finale: kleidung (+28), instrumente (+26), taenze (+18) — alle 16 Ziel-Länder EU-Ost/Nord/West vollständig abgedeckt** |
| **326** | patches/patch_326_natur_balancing.py | **Natur-Balancing: nationaltiere (+27), nationalpflanzen (+28), gewuerze (+17), nationalblumen (+15) — 16 Ziel-Länder EU-Ost/Nord/West abgedeckt** |
| **327** | patches/patch_327_rest_balancing.py | **Sport/Geo/Archäologie-Balancing: sport_herkunft, sport_sportlegende_land, geo_hoehlen_land, repatriierung, megalithanlagen — nur semantisch valide Länder-Arrays erweitert** |
| **328** | patches/patch_328_heimvorteil_engine.py | **ENGINE: Heimvorteil 70/30 in _mkMatchQ() — alle Match-Modi bevorzugen jetzt Einträge aus dem Heimatland des Nutzers (S.language → Ländername-Mapping, localPool, rng()<0.7). Fallback 100% global für nicht-geographische c-Felder.** |
| **329** | patches/patch_329_autos.py | **Auto-Quartett: 4 HL-Modi (PS, vmax, accel, ccm) aus data/autos.json — 50 Fahrzeuge von VW Käfer bis Rimac Nevera, 17 Länder, EVs im ccm-Array ausgeschlossen** |
| **330** | patches/patch_330_autos_eu_completion.py | **Auto-Quartett EU-Completion: +5 verifizierte Fahrzeuge (Belgien, Norwegen, Bulgarien, Portugal, Griechenland) — SK/FI/HU weggelassen (keine verifizierbaren Seriendaten)** |
| **331** | patches/patch_331_vw_bj.py | **VW-Sprint: Golf 1-8 GTI/R + Corrado VR6 + Phaeton W12 (10 Modelle) + NEU: auto_bj Baujahr-Array + hl_auto_bj Modus (726 Modi)** |
| **332** | patches/patch_332_audi.py | **Audi-Sprint: Quattro, Sport Quattro, RS2, TT, R8 V10, RS6 C8, e-tron GT (7 Modelle)** |
| **333** | patches/patch_333_bmw.py | **BMW-Sprint: 2002 Turbo, M1, M5 E34, Z8, M3 E92, M4 Competition (6 Modelle)** |
| **334** | patches/patch_334_opel.py | **Opel-Sprint: Manta 400, GT, Kadett E GSi, Corsa OPC (4 Modelle)** |
| **335** | patches/patch_335_smart.py | **Smart-Sprint: Fortwo (1998), Fortwo Brabus (2007) (2 Modelle)** |
| **336** | patches/patch_336_lancia.py | **Lancia-Sprint: Stratos HF, Delta HF Integrale Evo (2 Modelle)** |
| **337** | patches/patch_337_saab.py | **Saab-Sprint: 900 Turbo, 9-3 Aero (2 Modelle)** |
| **338** | patches/patch_338_subaru.py | **Subaru-Sprint: Impreza WRX STI (1 Modell)** |
| **339** | patches/patch_339_mercedes.py | **Mercedes-Benz-Sprint: 450 SEL 6.9, 500E W124, SLS AMG, A45 AMG, AMG GT Black Series (5 neue Modelle — gesamt 9 Mercedes)** |
| **340** | patches/patch_340_mercedes_suv_kombi.py | **Mercedes-Kategorie-Ergänzung: G 63 AMG (SUV) + E 63 AMG T-Modell (Kombi) — alle 6 MB-Kategorien jetzt repräsentiert (gesamt 11 Mercedes)** |
| **341** | patches/patch_341_mercedes_complete.py | **Mercedes-Vollständigkeit: B 250 Sport, CLA 45 AMG, CLS 63 AMG, GLC 63 S, GLE 63 S, GLS 63 AMG (6 Modelle) — alle Hauptbaureihen komplett** |
| **342** | patches/patch_342_data_completion.py | **Data Completion Sprint: Golf/Polo/Passat B1-B8, Corsa/Astra/Vectra, BMW 3er/5er, MB C/E-Klasse, Audi A3/A4, Peugeot/Renault, Fiat/Alfa, Škoda Octavia I-IV — 50 Jahre EU-Auto-Historie** |
| **343** | patches/patch_343_data_completion_c.py | **Data Completion Sprint 330c: BMW 1er/7er/X5, MB S/A/SL/G-Klasse, Audi A8/TT, Porsche Boxster/Cayenne, Opel Manta/Calibra, Ford Fiesta/Focus/Capri/Sierra, Volvo 240/V70/XC90, Saab, Smart W453, Mini** |
| **350** | patches/patch_350_enrich_merge.py | **autos_extended.json: 431 Fahrzeuge mit 22 technischen Zusatzfeldern (gewicht, drehmoment, cw, karosserie, antriebsart, konzern, …)** |
| **351** | patches/patch_351_validate_autos.py | **validate_content.py: check_autos_extended() + autos.json HL-Routing + auto_ccm EV-Check + Cross-Validation autos <-> autos_extended** |
| **352** | patches/patch_352c_auto_creative.py | **ENGINE SPRINT 352: Auto-Universum komplett — 25 neue Modi (12 H/L + 8 Match + 5 kreativ). AUTOS_EXT_DATA (431 Fzg., 22 Felder) inline. genAutosHLExt + genAutosMatchExt + Baujahr-MC + Leistungsgewicht + CO2 + Dekaden-Quiz.** |
| **353** | patches/patch_353_gen_match.py | **Generationen-Match: 21 Modellreihen (Golf/M3/Clio/Corsa/…) — Distraktor-Optionen = echte andere Generationen derselben Baureihe. JSON-Komprimierung: -60 KB (AUTOS_EXT_J compact)** |
| **354** | patches/patch_354_feedback_delay.py | **UX: Feedback-Anzeigedauer +1,5 s — Einzel: 1900→3400 ms, IATA: 2800→4300 ms, startNextRound: 1500→3000 ms (5×). Multiplayer (5500 ms) unverändert.** |
| **360** | patches/patch_360_games_engine.py | **Gaming-Kategorie: 50 Spiele (30 Modern/Mobile + 20 Klassiker), 13 Modi (games_pin, genre/land/adaption-Match, H/L release/vk/metacritic/usk, Baujahr-MC). Bridge: dev_lat/dev_lng → echter GeoQuest-Pin-Modus.** |
| **402** | patch_402.py | **Phase 401/402: Audit-Fixes (XSS, Zero-Trap, Sort, ES5) + 4 neue Gaming-Modi + games_extended Validator** |
| **403** | patch_403.py | **i18n Gaming-Modi: 16 Prompts via _tc() fuer EN/PL + post_phase MODES-Fix + Spieluebersicht-Auto + Backup-Cleanup** |
| **404** | patch_404.py | **Phase 403 Audit-Polish (JSON try/except, Prototype-Guard) + Phase 404: Modi esports+pegi, i18n +4, Backup-Policy 2-Backup-Regel** |
| **405** | patch_405.py | **Batch 3: 20 Indie/Klassiker-Spiele + peak_year + publisher_lat/lng + 3 neue Modi (peak_year_mc, hl_peak_year, hl_publisher_lat) + validate_content Indie-Enum** |
| **406** | patch_406.py | **Phase 406: Bugfixes — Spoiler genGamesPinQ, games_match_kategorie immer null (fixedPool 3->4), catLabels games, hl_games_dev_lat Syntax; JS 143/143** |
| **407** | patch_407.py | **generate_spieluebersicht: Datenbasis-Badges fuer Gaming (70 Spiele) + Auto-Extended (431) + genAutosHL korrekt; Dispatch-Regex 4 neue Muster; 0 von 774 Modi ohne Badge** |
| **408** | patch_408.py | **UX: _exitToMenu() — nach Spielende kehrt die App zur Kategorie des gespielten Modus zurueck (11x Exit-Button ersetzt, smooth scroll, filterCat gesetzt)** |
| **409** | patch_409.py | **Phase 409/410: Zuletzt-gespielt-Leiste (letzte 5 Modi, gq_recent), Gespielt-Tracking (gq_played), Fortschrittsbalken X/Y im Akkordeon-Header, Carousel-Grid-Reinit-Fix fuer Gaming** |
| **410** | patch_410.py | **Phase 410: 3 neue Gaming-Modi — games_match_protagonist (42 Helden), games_match_pub_is_dev (0 neue Felder!), hl_games_howlong (37 Spielzeiten). protagonist+howlong_h zu games_extended. 774->777 Modi** |
| **411** | patch_411.py | **Phase 411: wendekreis_m + zuladung_kg zu 431 Autos (91/74 gefüllt), 2 neue Auto-Modi hl_auto_wendekreis (lowerWins!) + hl_auto_zuladung. 777->999 Modi** |
| **412** | patch_412.py | **Bugfixes + 6 neue Konsolen-Modi: match_konsolen_handheld→Ja/Nein, timeline_auto_bj, generate_spieluebersicht Syntax-Error, hl_konsolen_ram/cpu, match_konsolen_generation/land. iOS Timeline-Bug (5 Fixes). MODES: 802→802** |
| **413** | patch_413.py | **Neue Kategorie 'Regionale Kultur & Kulinarik': 30 D-A-CH Einträge (Speisen, Weine, Getränke, Brauchtum), 6 Modi (Pin, 3x Match Land/Region/Kategorie, 2x H/L Alkohol/Saison), validate_content + i18n DE/EN/PL. MODES: 802→802** |
| **414** | patch_414.py | **Dual Menu Layout: Tab-Ansicht (3 Reihen × 8 Kategorien) + Settings-Toggle gq_menu_layout (accordion/tabs). CSS-Klasse tabs-mode blendet Akkordeon-Header aus, Carousel-Logik unverändert. verify: 146/146** |
| **415** | patch_415.py | **Settings konsolidiert: block4+block5 zu einem EINSTELLUNGEN-Block (Design-Segmented, Sprache, Menü-Ansicht-Toggle), Sprache aus Modal entfernt, Modal heißt 'Weitere Einstellungen'. Spielübersicht: _get_type() Match/Pin-Erkennung, Konsolen/Regional-Badges, return len(rows)** |
| **416** | patch_416.py | **Tab-Ansicht fix: Inline-Grid statt CSS-Klassen, Accordion-Header im JS-Rendering ausgeblendet. PWA-Banner: Schließen-Button für Android/Desktop, gq_pwa_dismissed in localStorage, Reaktivierung in Einstellungen** |
| **417** | patch_417.py | **Settings-Modal bereinigt: Dark Mode entfernt (doppelt mit Profilseite), Untertitel hinzugefügt. Tab-Ansicht + PWA-Dismiss aus Phase 416 finalisiert.** |
| **418** | patch_418.py | **Settings-Modal final: Menü-Ansicht entfernt (steht auf Profilseite), App installieren vor Schließen, saubere Reihenfolge: Heimatregion→TTS→Hardcore→Raster→Feedback→App installieren→Schließen** |
| **419** | patch_419.py | **Settings-Modal bugfix: App-installieren Button-Code war fälschlich in onclick eingebettet → korrektes IIFE-Pattern. Modal finale Struktur: Heimatregion→TTS→Hardcore→Raster→Feedback→App installieren (conditional)→Schließen** |
| **420** | patch_420.py | **Kategorie-Navigation als wischbares Karussell (data-cat=_catnav) statt 8-Spalten-Raster: 4 Spalten x 3 Reihen pro Seite, volle Kategorienamen, Schrift von 0.48rem auf 0.66rem vergroessert. Reihen pro Seite via neuer Einstellung geoquest_catnav_rows (2-6, Standard 3) im Einstellungs-Modal konfigurierbar. Nutzt bestehende Carousel-Engine (Swipe/Pfeile/Punkte/Seiten-Persistenz). verify 146/146, validate 0 Warnings.** |
| **421** | patch_421.py | **UI-Feinschliff Spielkarten: mode-card kompakter (Padding .6rem .4rem 30px -> .5rem .32rem 28px, Radius 12px->11px), mode-icon 1.4rem->1.25rem, Info-Button (i) 32x32px->28x28px (Radius 7px, Font .72rem). Aenderungen in geoquest_css.txt (echte CSS-Quelle) + Info-Btn inline in gen.py. Leserlichkeit und Tap-Flaeche bleiben erhalten (Button >=24px WCAG). verify 146/146, validate 0 Warnings.** |
| **422** | patch_422.py | **Tech-Debt + UX: totes CSS-Duplikat (~555 Zeilen <style> in _HTML_HEAD) aus gen.py entfernt (echte Quelle bleibt geoquest_css.txt). Kategorie-Chips barrierefrei: role=button, tabindex, aria-label, Tastatur (Enter/Space). mode-desc .65rem->.68rem. verify 146/146, validate 0 Warnings.** |
| **423** | patch_423.py | **8 neue Modi aus ungenutzten Datenfeldern: hl_konsolen_erscheinungsjahr/eingestellt, konsolen_match_spiel/aufloesung, hl_auto_nordschleife/baujahr_ende, games_match_publisher_land, hl_games_publisher_lng. MODES 802->810** |
| **424** | patch_424.py | **4 neue Geo/Zug-Modi: zug_match_land (177 Strecken→Land), odd_one_out (6 Kategorien: EU/NATO/Insel/Binnen/G7/Euro), clue_country (progressive Hinweise: Kontinent→Hauptstadt→Währung), sort_rank (4 Länder nach Metrik sortieren). MODES 810→814** |
| **425** | patch_425.py | **Hilfe-Button sichtbar gemacht: ?-Button zusaetzlich in die sichtbare Home-Kopfzeile (_hdr, eingeloggt + Gast) neben das Feedback-Symbol gesetzt. Vorher nur in der GEOQUEST-Logo-Leiste, die auf dem Home-Tab nicht sichtbar ist -> Hilfe wurde nicht gefunden. verify 146/146, validate 0 Warnings.** |
| **426** | patch_426.py | **Home-Kopfzeile entzerrt (war gequetscht): Begruessung+Streak links, einheitliche runde 34px ?/Feedback-Icons rechts; Streak-Pille bricht nicht mehr um (nowrap); Gast-Variante: 'Fortschritt sichern' jetzt eigene volle Zeile statt eingequetscht. verify 146/146, validate 0 Warnings.** |
| **427** | patch_427.py | **2 neue Kategorien: Kino & Film + Musikgeschichte. 40 Filme + 40 Künstler (global: DE/FR/JP/PL/IN/KR/AU/CO). 15 neue Modi: 8x Film (H/L+Match+Timeline) + 7x Musik (H/L+Match+Timeline). Neue Generatoren genFilmeHLExt/MatchExt/genMusikHLExt/MatchExt. Validator-Update. MODES 814->829** |
| **428** | patch_428.py | **2 neue Kategorien: Mythologie & Sagenwelt (40 Gottheiten: GR/NO/AE/RO/JP/AZ/MES) + Architektur & Megabauten (40 Bauwerke: Wolkenkratzer/Brücken/Staudämme/Tunnel/Tempel/Denkmäler). 11 neue Modi: myth_match_domain/kultur/typ/roemisch + myth_pin_herkunft + hl_arch_height/span/baujahr + arch_match_land/typ + arch_pin_megaprojects. MODES 829->840** |
| **429** | patch_429.py | **2 neue Kategorien: Literatur & Comics (40 Werke: Roman/Comic/Manga/Kinderbuch global) + KI, Robotik & Hardware (40 Systeme: WRO/FLL/Arduino/ChatGPT/AlphaGo/KUKA). Fix: MYTH_DATA/ARCH_DATA Placeholder-Bug (Phase 428 retrofix). 12 neue Modi: hl_lit_sales/release + lit_match_autor/land/protagonist + timeline_lit_release + hl_robot_jahr + robot_match_kategorie/land/entwickler/fakt + timeline_robot_jahr. MODES 840->852. verify: 152/152** |
| **430** | patch_430.py | **Phase 430: Wort-Schmiede für Literatur & Robotik/KI — ws_lit_protagonist (TINTENHERZ) + ws_robot_name (MASCHINENLERNEN). Neue Dateien: literatur_ws.json, robotik_ws.json. MODES: 859→861** |
| **431** | patch_431.py | **Phase 431: Kategorien Anatomie & Medizin + Wirtschaft & Marken. 13 neue Modi (6 Medizin, 7 Wirtschaft). Neue Dateien: medizin_extended.json (40), wirtschaft_extended.json (40), medizin_ws.json, wirtschaft_ws.json. MODES: 861→874** |
| **432** | patch_432.py | **Bugfix: match_regional_land öffnete sich nicht (genRegionalMatchQ pool.length<3 statt <2 — D-A-CH hat nur 3 Länder). Fix: Threshold auf 2 gesenkt, dis=p.slice(0,Math.min(3,p.length)). verify: 165/165** |
| **433** | patch_433.py | **Phase 433: EU-Erweiterung Regionale Kulinarik (30→80 Einträge, 22 EU-Länder). Bugfix match_regional_land: fixedPool entfernt (nutzt jetzt Echtdaten). validate_content.py: LAND-Enum EU-weit. Label: Regionale & EU-Kulinarik. verify: 165/165** |
| **434** | patch_434.py | **Phase 434: Datenbasis-Upgrade. generate_spieluebersicht.py: 3 neue Fn-Mappings (0 Warnings). literatur_extended 40→80, robotik_extended 40→80. timeline.json: robot_jahr auf 80 Einträge. verify: 165/165** |
| **435** | patch_435.py | **Phase 435 (432-Fortsetzung): Kategorien Weltgeschichte & Imperien + Webkultur & Social Media. 12 neue Modi. 4 neue JSON-Dateien (je 40 Einträge). Generatoren, i18n DE/EN/PL, timeline. verify: 165/165. MODES: 874→886** |
| **436** | patch_436.py | **Phase 436: WS Mythologie (PANTHEON, UNTERWELT) + WS Architektur (WOLKENKRATZER, FUNDAMENT) + hl_arch_laenge + timeline_arch_baujahr + myth_match_tier. 7 neue Modi. post_phase.py: landing.html Auto-Update. MODES: 886→893** |
| **437** | patch_437.py | **Phase 437: Datenbasis-Erweiterung. Serien 98→105 (+7), Filme 40→46 (+6), Musik 40→46 (+6), Webkultur 40→52 (+12), Wirtschaft 40→49 (+9). Serien-Enum-Fix (Sci-Fi→Sci-Fi/Mystery, Vergangenheit→Historisch). Timeline eco+web refreshed. verify: 165/165** |
| **438** | patch_438.py | **Freizeitparks & Kunstgeschichte: 15 neue Modi (HL, Match, Timeline, WS)** |
| **440** | patch_440.py | **Hunderassen & Gartenbau: 14 neue Modi (HL, Match, WS)** |
| **441** | patch_441.py | **Audit-Fixes: (1) Build-Breaker behoben — ungueltiger Unicode-Escape im Wort gießen (Modus garten_match_wasser), verify war 172/173 JS-Syntaxfehler. (2) 13 fehlende PL-Uebersetzungen in _CONTENT_I18N ergaenzt (Film-/Musik-Kategorie: Regisseur, IMDb, Oscars, Grammys, Streams, Tontraeger u.a.). verify 173/173, validate 74/74 0 Warnings, check_session 15/15.** |
| **439** | patch_439.py | **Brettspiele & Sprachen: 14 neue Modi (HL, Match, Timeline, WS)** |
| **442** | patch_442.py | **Geo-Pin-Welle: 13 neue Pin-Modi fuer Hunde, Brettspiele, Robotik, Serien, Musik, Webkultur, Literatur, Themeparks, Wirtschaft, Filme, Konsolen, Gaming-Hardware, Gartenbau. SPRACHEN_DATA Duplikat-Bug behoben.** |
| **444** | patch_444.py | **Nationalparks weltweit: 80 Parks, 7 neue Modi (Fläche, Gründung, Land, Kontinent, Ökosystem, Pin, WS Yellowstone). LAND_LATLON +14 Länder. i18n-Doppelquote-Bug gefixt.** |
| **445** | patch_445.py | **Hauptstädte weltweit: 80 Hauptstädte, 7 Modi (Einwohner, Höhe, Kontinent, Größenklasse, Pin, Äquator-Distanz, WS Reykjavik). LAND_LATLON erweitert.** |
| **446** | patch_446.py | **Inseln weltweit: 80 Inseln, 7 Modi (Fläche, Einwohner, Ozean, Kontinent, Pin, Äquator, WS Grönland). verify: 191/191.** |
| **447** | patch_447.py | **Gipfel & Berge: 80 Gipfel, 7 Modi (Höhe, Gebirge, Kontinent, Pin, Erstbesteigung, Timeline, WS Himalaya). verify: 191/191.** |
| **448** | patch_448.py | **Klimazonen weltweit: 80 Länder, 7 Modi (Zone, Kontinent, Temp, Niederschlag, Pin, Kälter, WS Monsun). verify: 191/191.** |
| **449** | patch_449.py | **Ozeane & Meere: 80 Gewässer, 8 Modi (Fläche, Tiefe, Typ, Kontinent, Kleiner, Seichter, Name, WS Atlantik). 999 Modi erreicht! verify: 191/191.** |

---

## Datenqualitäts-Audit (Stand Phase 328, Mai 2026)

Durchgeführt mit `audit_safety_check.py` + `validate_content.py` nach Abschluss der Balancing-Sprints 324–328.

### Ergebnisse

| Prüfung | Ergebnis | Befund |
|---|---|---|
| XSS / Injection-Scan | ✅ SAUBER | 0 unsichere Felder in 41 JSON-Dateien |
| Schema-Integrität | ✅ SAUBER | Alle Items haben gültige Pflichtfelder (n/c oder n/lat/lng) |
| Koordinaten-Plausibilität | ✅ SAUBER | Alle lat/lng-Werte im gültigen Bereich |
| JSON-Parse | ✅ SAUBER | Alle 41 Dateien fehlerfrei parsebar |
| validate_content.py | ✅ 41/41 ohne Warnings | Keine neuen Warnungen nach Phasen 324–328 |

### i18n Fallback-Analyse (c-Feld)

Das `audit_safety_check.py`-Skript identifiziert zwei Klassen von `c`-Werten:

**Klasse A — ISO-Ländernamen (automatisch übersetzt):** Alle Standard-Ländernamen (z.B. "Polen", "Schweden", "Türkei") werden durch `_tcc()` → `_deCountryCc()` → `Intl.DisplayNames` vollautomatisch in alle 24 Sprachen übersetzt. Kein manueller Aufwand.

**Klasse B — Semantische Kategorie-Werte (kein Bug):** Arrays wie `sport_teamgroesse` ("11 Spieler"), `geo_gesteinsarten` ("Magmatisch"), `zug_bahnhof_typ` ("Kopfbahnhof"), `sport_olympisch` ("Ja/Nein") nutzen `c` als Antwort-Kategorie, nicht als Ländername. Der `_tcc()`-Fallback zu `_tc()` greift hier korrekt; für 22 Sprachen ohne `_CONTENT_I18N`-Eintrag wird auf Deutsch zurückgefallen. Dies ist bekanntes Verhalten (dokumentiert als i18n Gap C).

**Bekannte Lücke (nicht kritisch):** `_CONTENT_I18N` hat nur `pl` und `en`. Prompt-Strings für fr, es, it, nl, ro, hu, cs, sk, hr, bg, el, da, sv, fi, et, lv, lt, mt, ga, sl erscheinen für Sprecher dieser Sprachen auf Deutsch. Adressierung in zukünftigen i18n-Sprints.

---

## i18n Technical Debt & Roadmap (Stand Phase 328, Mai 2026)

### Status Quo — Was bereits funktioniert

**Länder-Übersetzung (Klasse A, ~84% aller Geo-Felder):** `_tcc()` → `_deCountryCc()` → `Intl.DisplayNames` übersetzt alle Standard-ISO-Ländernamen vollautomatisch in alle 24 Sprachen. Kein manueller Aufwand, keine Lookup-Tabelle. Funktioniert seit Phase 293.

**Heimvorteil-Algorithmus (Phase 328):** `_mkMatchQ()` priorisiert Einträge aus dem Heimatland des Nutzers (70/30) via `S.language` → deutschem Ländernamen-Mapping. Fallback für nicht-geografische Arrays automatisch.

**Validierung:** `validate_content.py` prüft ab Phase 328 für 18 bekannte Geo-Arrays, ob `c`-Werte im ISO-Mapping vorhanden sind (als `info()`-Notice, nicht als blocking Warning).

### Known Limitations (Technical Debt)

**Klasse B — Geo-Regionen ohne ISO (201 Einträge, 16% der Geo-Felder):**
Werte wie "Westafrika", "Naher Osten", "Mesopotamien", "Nordamerika" haben keinen ISO-cc und fallen für 22 Sprachen auf Deutsch zurück. Vollständige Liste in `audit_i18n_gap.py` (Klasse-B-Ausgabe).

**Multi-Country `c`-Werte (173 Infos aus validate_content.py):**
Einträge wie `c="Portugal / Hawaii"`, `c="Slowenien/Kroatien"`, `c="Naher Osten/Südasien"` sind für den Heimvorteil-Algorithmus wertlos (kein Match auf einfachen Ländernamen) und erscheinen für 22 Sprachen auf Deutsch.

**`_CONTENT_I18N` deckt nur EN + PL:**
Prompt-Strings (Frage-Texte) sind für die 22 anderen Sprachen (fr, es, it, nl, ro, hu, cs, sk, hr, bg, el, da, sv, fi, et, lv, lt, mt, ga, sl) nicht übersetzt.

### Korrektur-Strategie (Roadmap)

1. **Sprints 329–332 (Geo-Regionen):** Die Top-10 Klasse-B-Werte ("Westafrika", "Naher Osten", "Nordamerika", "Südamerika", "Mesopotamien", "Zentralasien", "Persien", "Europa", "Asien", "Skandinavien") in `_CONTENT_I18N` mit EN + PL aufnehmen. Aufwand: ~20 Einträge pro Sprint.
2. **Multi-Country-Bereinigung:** `c`-Werte mit "/" auf Hauptland normieren (z.B. "Portugal / Hawaii" → "Portugal") oder in zwei separate Einträge aufteilen.
3. **`_CONTENT_I18N` Expansion:** Sukzessive Erweiterung um FR, ES, IT, NL (die 4 größten Nicht-DE Nutzergruppen). Pro Sprint: eine Sprache, alle 937 Keys.
4. **validate_content.py ISO-Check schärfen:** Aus `info()` → `warn()` promoten, sobald die Multi-Country-Bereinigung abgeschlossen ist.

### Tooling

| Skript | Zweck |
|---|---|
| `audit_safety_check.py` | XSS-Scan + c-Feld-Klassen-Übersicht |
| `audit_i18n_gap.py` | Detaillierte Klasse-B-Liste als Sprint-To-Do |
| `validate_content.py` (Phase 328+) | ISO-Check für 18 Geo-Arrays als `info()`-Notice |

---

*Dieses Dokument wird bei jedem signifikanten Architektur-Sprint aktualisiert.*
*Letztes Update: Phase 328 — Heimvorteil-Engine + i18n Technical Debt Roadmap, 539 Modi, 41 Datendateien, Mai 2026.*


---

## 13. Vollstaendiger Spielmodus-Katalog

**Stand Phase 283 -- 685 Modi in 20 Kategorien**

> **Pin** = Ort auf Karte finden | **H/L** = Hoeher/Niedriger | **Match** = Zuordnen | **WS** = Wort-Schmiede | **Classic** = Multiple Choice | **Karte** = Interaktive D3-Karte


## 13.1 Geografie-Klassiker -- 29 Modi

*Stadt/Flagge/Hauptstadt/Fluss, UNESCO, Wappen, Reverse-Modi, Klimavergleiche*

`16 Classic | 7 H/L | 2 Karte | 4 Match`


| Titel | Typ | Modus-ID |
|-------|-----|---------|
| Stadt -> Land | Classic | `city` |
| Flagge -> Land | Classic | `flag` |
| Hauptstadt -> Land | Classic | `capital` |
| Fluss -> Land | Classic | `river` |
| Sehenswürdigkeit | Classic | `landmark` |
| Nationalpark | Classic | `park` |
| UNESCO Welterbe | Classic | `unesco` |
| Wahrzeichen -> Stadt | Classic | `citymark` |
| U-Bahn-Netz | Classic | `subway` |
| Land -> Flagge | Classic | `flagsel` |
| Land -> Hauptstadt | Classic | `rcapital` |
| Land -> Stadt | Classic | `rcity` |
| Land -> Fluss | Classic | `rriver` |
| Fluss -> Land | Classic | `river_real` |
| [BETA] Niederschlag | H/L | `hl_b_rain` |
| [BETA] Temperatur | H/L | `hl_b_temp` |
| [BETA] Sonnenstunden | H/L | `hl_b_sun` |
| [BETA] Vulkane | H/L | `hl_b_vulc` |
| [BETA] Inseln | H/L | `hl_b_isl` |
| [BETA] Zeitzonen | H/L | `hl_b_tz` |
| [BETA] \u00c4ltestes Land | H/L | `hl_b_founded` |
| Wappen-Meister | Classic | `wappen_meister` |
| Stadt, Land, Fluss | Classic | `slf` |
| [BETA] Fl\u00fcsse pinnen | Karte | `river_map` |
| [BETA] UNESCO Karte | Karte | `unesco_map` |
| Kontinent-Zentren | Match | `uk_kontinent_mitte` |
| Kontinent zuordnen | Match | `uk_sort_kontinente` |
| Ozean zuordnen | Match | `uk_sort_ozeane` |
| Breitengrad-Match | Match | `uk_breitengrad_match` |

## 13.2 Kultur & Lifestyle -- 24 Modi

*Laenderumrisse, Gerichte, Waehrungen, Marken, Gipfel/Wuesten/Canyons pinnen*

`6 Classic | 4 H/L | 14 Match`


| Titel | Typ | Modus-ID |
|-------|-----|---------|
| L\u00e4nder-Umrisse | Classic | `outline` |
| Gericht -> Land | Classic | `food` |
| Marke -> Land | Classic | `brand` |
| W\u00e4hrung -> Land | Classic | `currency` |
| Land -> W\u00e4hrung | Classic | `curr_real` |
| Mehr Einwohner? | Classic | `pop_compare` |
| [BETA] Amtssprachen | H/L | `hl_b_lang` |
| [BETA] UNESCO | H/L | `hl_b_unesco` |
| [BETA] Tourismus | H/L | `hl_b_tour` |
| W\u00fcsten pinnen | Match | `uk_wuesten` |
| Berggipfel pinnen | Match | `uk_berggipfel` |
| Meeren\u2019gen pinnen | Match | `uk_meerengen` |
| Wasserf\u00e4lle pinnen | Match | `uk_wasserfaelle` |
| Canyons pinnen | Match | `uk_canyons` |
| Surf-Spots pinnen | Match | `uk_surf_spots` |
| Kaffee-Nation | H/L | `hl_b_coffee` |
| Inseln zuordnen | Match | `uk_insel_match` |
| Ehemalige Hauptst\u00e4dte | Match | `uk_ehemalige_hauptstaedte` |
| Philosophen | Match | `uk_philosophen` |
| Nationalpflanzen | Match | `uk_nationalpflanzen` |
| Nationaltiere | Match | `uk_nationaltiere` |
| Religionen & Ursprung | Match | `uk_religionen` |
| Schriftsysteme | Match | `uk_schriften` |
| Silhouette gedreht | Match | `uk_schatten_gedreht` |

## 13.3 EU-Kennzeichen -- 4 Modi

*Laenderkennzeichen Europa, Profi-Modus, Karte, Deutschland*

`3 Classic | 1 Karte`


| Titel | Typ | Modus-ID |
|-------|-----|---------|
| EU-Kennzeichen | Classic | `plate_casual` |
| Kennzeichen Pro | Classic | `plate_hard` |
| Kennzeichen-Knacker | Karte | `map_ivr` |
| Deutschland-KFZ | Classic | `de_plate` |

## 13.4 H/L Klassiker -- 11 Modi

*Laender-Daten vergleichen: Einwohner, Flaeche, BIP, Fluss, Kuestelaenge*

`11 H/L`


| Titel | Typ | Modus-ID |
|-------|-----|---------|
| H/L Einwohner | H/L | `hl_pop` |
| H/L Flussl\u00e4nge | H/L | `hl_river` |
| H/L Landfl\u00e4che | H/L | `hl_area` |
| H/L BIP | H/L | `hl_gdp` |
| H/L Bev\u00f6lkerungsdichte | H/L | `hl_density` |
| H/L H\u00f6chster Punkt | H/L | `hl_elevation` |
| H/L K\u00fcstenlänge | H/L | `hl_coastline` |
| H/L Nachbarl\u00e4nder | H/L | `hl_borders` |
| H/L Lebenserwartung | H/L | `hl_lifeexp` |
| H/L Medianalter | H/L | `hl_median_age` |
| H/L Waldf\u00e4che | H/L | `hl_forest` |

## 13.5 Vergleichs-Modi -- 31 Modi

*Zwei Laender direkt gegenueberstellen: Groesse, Infrastruktur, Klima*

`1 Classic | 30 H/L`


| Titel | Typ | Modus-ID |
|-------|-----|---------|
| [BETA] Nationalparks | H/L | `hl_b_parks` |
| [BETA] Stra\u00dfennetz | H/L | `hl_b_roads` |
| [BETA] Schienennetz | H/L | `hl_b_rail` |
| [BETA] Internetspeed | H/L | `hl_b_net` |
| [BETA] E-Ladesäulen | H/L | `hl_b_ev` |
| [BETA] Urbanisierung | H/L | `hl_b_urban` |
| [BETA] Kenn. Vergleich | Classic | `plate_compare` |
| Gr\u00f6\u00dferes Land? | H/L | `comp_area` |
| Mehr Einwohner? | H/L | `comp_pop` |
| Weiter n\u00f6rdlich? | H/L | `comp_north` |
| H\u00f6heres BIP? | H/L | `comp_gdp` |
| Dichter besiedelt? | H/L | `comp_density` |
| H\u00f6herer Gipfel? | H/L | `comp_elevation` |
| L\u00e4ngere K\u00fcste? | H/L | `comp_coast` |
| Mehr Nachbarn? | H/L | `comp_borders` |
| L\u00e4nger leben? | H/L | `comp_life` |
| H\u00f6heres Medianalter? | H/L | `comp_age` |
| Mehr Wald? | H/L | `comp_forest` |
| Mehr Flugh\u00e4fen? | H/L | `comp_airports` |
| Gr\u00f6\u00dferes Land? | H/L | `comp_flight` |
| H\u00f6herer Gipfel? | H/L | `comp_mountain` |
| L\u00e4nger Nord-S\u00fcd? | H/L | `comp_nsextent` |
| Mehr Olympia-Gold? | H/L | `comp_olympics` |
| Sprachen-Vielfalt | H/L | `hl_b_total_lang` |
| Nobelpreistr\u00e4ger | H/L | `hl_b_nobel` |
| Olympia-Medaillen | H/L | `hl_b_medals` |
| Nord-S\u00fcd-Ausdehnung | H/L | `hl_b_ns_km` |
| Fahrrad-Nation | H/L | `hl_b_bikes` |
| L\u00e4ngste Grenzen | H/L | `hl_b_land_border` |
| Milit\u00e4rausgaben | H/L | `hl_b_military` |
| Erneuerbare Energie | H/L | `hl_b_renewable` |

## 13.6 Flughaefen & Transport -- 34 Modi

*IATA-Codes, Zeitzonen, Flugrouten, Kanaele, Metro, Airlines, Distanzschaetzer*

`22 Classic | 1 Karte | 11 Match`


| Titel | Typ | Modus-ID |
|-------|-----|---------|
| IATA-Code? | Classic | `iata` |
| Welche Uhrzeit? | Classic | `tz_quiz` |
| Klima-Krimi | Classic | `climate_quiz` |
| Flaggen-Farben | Classic | `flagcolor` |
| Binnenstaat? | Classic | `landlocked_quiz` |
| [BETA] Flugh\u00e4fen | Karte | `airport_map` |
| Flugrouten-Duell | Classic | `flugrouten_duell` |
| Inland oder International? | Classic | `inlandsflug_intl` |
| Fr\u00fchere Sonne? | Classic | `sunrise_guesser` |
| Sonnen-Kompass | Classic | `sonnen_kompass` |
| \u00c4quator-Magnet | Classic | `aequator_magnet` |
| Kontinent-Klicker | Classic | `kontinent_klicker` |
| Hauptstadt-Distanz | Classic | `hauptstadt_distanz` |
| N\u00e4chster Flughafen | Classic | `naechster_airport` |
| Airport Pinnen | Classic | `airport_pin` |
| IATA Reverse | Classic | `iata_reverse` |
| Jetlag-Rechner | Classic | `jetlag_rechner` |
| K\u00fchlschrank vs. Backofen | Classic | `kuehlschrank_backofen` |
| Regen-Radar | Classic | `regen_radar` |
| H\u00f6henmeter-Sch\u00e4tzer | Classic | `hoehenmeter_schaetzer` |
| Klima-Ausrei\u00dfer | Classic | `klima_ausreisser` |
| Insel oder Festland? | Classic | `insel_festland` |
| Sprachen-Kompass | Classic | `sprachen_kompass` |
| Automarken-Heimat | Match | `uk_automarken` |
| Airlines zuordnen | Match | `uk_fluggesellschaften` |
| Ber\u00fchmte Bahnstrecken | Match | `uk_bahnstrecken` |
| Welthafen zuordnen | Match | `uk_hafen_world` |
| Kan\u00e4le zuordnen | Match | `uk_kanaele` |
| Reedereien zuordnen | Match | `uk_reedereien` |
| Autobahnsysteme | Match | `uk_autobahnen_beruhmt` |
| Metro-Systeme zuordnen | Match | `uk_metrostaedte` |
| Luftfahrt-Rekorde | Match | `uk_luft_rekorde` |
| Distanz-Sch\u00e4tzer | Match | `uk_distanz_schaetzer` |
| Flugzeit-Sch\u00e4tzer | Match | `uk_flugzeit_schaetzer` |

## 13.7 Laender-Nachbarn -- 20 Modi

*Grenzen, Exklaven, Halbinseln, Seen, Gebirge, Meerbusen, Grenzfluesse*

`11 Classic | 9 Match`


| Titel | Typ | Modus-ID |
|-------|-----|---------|
| Grenzg\u00e4nger | Classic | `neighbor` |
| Falscher Nachbar | Classic | `neighbor_fake` |
| Nachbar-Z\u00e4hler | Classic | `neighbor_count` |
| Teilen sie eine Grenze? | Classic | `border_q` |
| [BETA] Sandwich-Laender | Classic | `b21` |
| [BETA] Transit-Route | Classic | `b22` |
| [BETA] Kueste oder Inland? | Classic | `b23` |
| [BETA] Fehlender Nachbar | Classic | `b25` |
| [BETA] Längste Grenze | Classic | `b29` |
| [BETA] Hauptstadt-Naehe | Classic | `b37` |
| [BETA] Meiste Nachbarn | Classic | `b40` |
| Exklaven erkennen | Match | `uk_enklave` |
| Grenzfl\u00fcsse | Match | `uk_grenzfluesse` |
| Halbinseln zuordnen | Match | `uk_halbinseln` |
| Flussdeltas | Match | `uk_deltamuendungen` |
| Kaps der Welt | Match | `uk_kaps` |
| Meeresg\u00f6lfe | Match | `uk_meerbusen` |
| Inselgruppen zuordnen | Match | `uk_inselgruppen` |
| Gebirge zuordnen | Match | `uk_gebirge_match` |
| Seen zuordnen | Match | `uk_seen_match` |

## 13.8 Karten-Modi -- 16 Modi

*Interaktive D3-Weltkarte: Land finden, Hauptstaedte orten, Antipoden, Klimazonen*

`11 Classic | 3 Karte | 2 Match`


| Titel | Typ | Modus-ID |
|-------|-----|---------|
| Finde das Land | Karte | `map_guess` |
| Wer bin ich? | Karte | `map_reverse` |
| Hauptstadt-Radar | Karte | `map_capital` |
| [BETA] Äquator-Schuetze | Classic | `b41` |
| [BETA] Klimazonen-Spotter | Classic | `b42` |
| [BETA] Breitengrad-Duell | Classic | `b44` |
| [BETA] E-Mobility-Hotspot | Classic | `b45` |
| [BETA] Naturwunder-Spotter | Classic | `b46` |
| [BETA] Antipoden-Loch | Classic | `b47` |
| [BETA] Wuesten-Fokus | Classic | `b51` |
| [BETA] Meerengen & Kanaele | Classic | `b53` |
| [BETA] Gipfel-Spotter | Classic | `b54` |
| [BETA] See-Spotter | Classic | `b58` |
| Mercator-Illusion | Match | `uk_mercator_illusion` |
| Kartenausschnitt | Match | `uk_kartenausschnitt` |
| [BETA] Nacht-Satellit | Classic | `b60` |

## 13.9 Sport -- 37 Modi

*Trikot, Wappen, Stadion, F1, Olympia, WM, EM, Rekordhalterstaedte*

`31 Classic | 1 H/L | 2 Karte | 3 Match`


| Titel | Typ | Modus-ID |
|-------|-----|---------|
| [BETA] WM-Teilnahmen | H/L | `hl_b_wm` |
| Stadion-Quiz | Classic | `stadium` |
| Trikot-Quiz | Classic | `jersey` |
| Wappen-Quiz | Classic | `crest` |
| [BETA] Ausreisser-Farben | Classic | `b1` |
| [BETA] F1-Spotter | Classic | `b2` |
| [BETA] Olympia-Zeitmaschine | Classic | `b4` |
| [BETA] Nationalsportarten | Classic | `b6` |
| [BETA] Höhenluft-Stadien | Classic | `b7` |
| [BETA] Sport-Ursprung | Classic | `b9` |
| [BETA] Rivalen-Distanz | Classic | `b11` |
| [BETA] Medaillen-Spiegel | Classic | `b17` |
| [BETA] WM-Fehltritte | Classic | `b19` |
| [BETA] Sport-Wappen | Classic | `b20` |
| \U0001F9EA Derby-Hotspots | Classic | `derby_hotspots` |
| \U0001F9EA Eishockey-Nationen | Classic | `eishockey_nationen` |
| \U0001F9EA F1 Historische Strecken | Classic | `f1_historisch` |
| \U0001F9EA Tour de France Pässe | Classic | `tdf_paesse` |
| \U0001F9EA Olympische Winter-Historie | Classic | `olympia_winter_historie` |
| \U0001F9EA WM-Gastgeber-Historie | Classic | `wm_gastgeber` |
| \U0001F9EA WM-Finalstadien | Classic | `wm_finalstadien` |
| \U0001F9EA Weltmeister-Nationen | Classic | `weltmeister_nationen` |
| \U0001F9EA Heimat der Fußball-Legenden | Classic | `fussball_legenden` |
| \U0001F9EA Road to 2026 | Classic | `road_to_2026` |
| \U0001F9EA Frauen-WM-Meilensteine | Classic | `frauen_wm_meilensteine` |
| \U0001F9EA Sommerspiele-Metropolen | Classic | `sommerspiele_metropolen` |
| \U0001F9EA Winter-Exoten & Klassiker | Classic | `winter_exoten_klassiker` |
| \U0001F9EA Olympische Rekordhalter | Classic | `olympische_rekorde` |
| \U0001F9EA Olympia in extremer Höhe | Classic | `olympia_hoehe` |
| \U0001F9EA Die Boykott-Spiele | Classic | `boykott_spiele` |
| \U0001F9EA EM-Gastgeber-Historie | Classic | `em_gastgeber_historie` |
| \U0001F9EA Finalstadien der EM | Classic | `em_finalstadien` |
| [BETA] F1 Strecken | Karte | `f1_map` |
| [BETA] Europastadien | Karte | `stadium_map` |
| Hochgelegene Stadien | Match | `uk_hohe_stadien` |
| Leichtathletik-WM Orte | Match | `uk_leichtathletik_wm` |
| Offizieller Nationalsport | Match | `uk_nationalsport_off` |

## 13.10 Tiere -- 59 Modi

*Habitate pinnen, H/L Gewicht/Speed/Gift, Faehrten, Anatomie, Pferde-DLC*

`13 H/L | 34 Match | 1 Pin | 11 WS`


| Titel | Typ | Modus-ID |
|-------|-----|---------|
| Endemische Arten | Match | `uk_tiere_endemisch` |
| Big Five Afrikas | Match | `uk_tiere_bigfive` |
| Großkatzen-Habitate | Match | `uk_tiere_grosskatzen` |
| Invasive Arten | Match | `uk_tiere_invasiv` |
| Vogelzug-Knotenpunkte | Match | `uk_tiere_vogelzug` |
| Ursprung der Haustiere | Match | `uk_tiere_haustiere` |
| Nationaltiere Pin | Pin | `uk_tiere_nationaltier_pin` |
| Primaten-Zentren | Match | `uk_tiere_primaten` |
| Hai-Hotspots | Match | `uk_tiere_hai` |
| Bären-Verbreitung | Match | `uk_tiere_baeren` |
| H/L Gewicht Landtiere | H/L | `hl_tiere_gewicht_land` |
| H/L Gewicht Meerestiere | H/L | `hl_tiere_gewicht_meer` |
| H/L Speed: Land | H/L | `hl_tiere_speed_land` |
| H/L Speed: Luft | H/L | `hl_tiere_speed_luft` |
| H/L Speed: Wasser | H/L | `hl_tiere_speed_wasser` |
| H/L Lebenserwartung | H/L | `hl_tiere_lebenserwartung` |
| H/L Tr\u00e4chtigkeit | H/L | `hl_tiere_traechtigkeit` |
| H/L Wurfgr\u00f6\u00dfe | H/L | `hl_tiere_wurf` |
| H/L Giftigkeit | H/L | `hl_tiere_gift` |
| H/L Wildpopulation | H/L | `hl_tiere_population` |
| H/L Schlafbedarf | H/L | `hl_tiere_schlaf` |
| F\u00e4hrten & Spuren | Match | `uk_tiere_faehrten` |
| Tierische Architekten | Match | `uk_tiere_architekten` |
| Tarnungsk\u00fcnstler | Match | `uk_tiere_tarnung` |
| Ern\u00e4hrungstypen | Match | `uk_tiere_ernaehrung` |
| Symbiosen | Match | `uk_tiere_symbiose` |
| Tauchtiefen-Rekorde | Match | `uk_tiere_tauchtiefe` |
| Mimikry & Doppelg\u00e4nger | Match | `uk_tiere_mimikry` |
| Insekten-Metamorphose | Match | `uk_tiere_metamorphose` |
| Biolumineszenz | Match | `uk_tiere_biolumineszenz` |
| Skelett-Anatomie | Match | `uk_tiere_anatomie` |
| Tierlaute | Match | `uk_tiere_laute` |
| Sinnesleistungen | Match | `uk_tiere_sinne` |
| WS: Schnabeltier | WS | `ws_tiere_schnabeltier` |
| WS: Gottesanbeterin | WS | `ws_tiere_gottesanbeterin` |
| WS: Komodowaran | WS | `ws_tiere_komodowaran` |
| WS: Korallenriff | WS | `ws_tiere_korallenriff` |
| WS: Silberr\u00fccken | WS | `ws_tiere_silberruecken` |
| WS: Wanderfalke | WS | `ws_tiere_wanderfalke` |
| WS: Mauersegler | WS | `ws_tiere_mauersegler` |
| WS: B\u00e4rtierchen | WS | `ws_tiere_baertierchen` |
| WS: Lederschildkr\u00f6te | WS | `ws_tiere_lederschildkroete` |
| WS: Pfeilgiftfrosch | WS | `ws_tiere_pfeilgiftfrosch` |
| Darwins Finken | Match | `uk_tiere_darwin_finken` |
| Schutzgebiete | Match | `uk_tiere_schutzgebiete` |
| Zoos der Welt | Match | `uk_tiere_zoos` |
| Nutztier-Rassen | Match | `uk_tiere_nutztier_rassen` |
| Fossil-Fundst\u00e4tten | Match | `uk_tiere_fossilien` |
| Arktis vs. Antarktis | Match | `uk_tiere_arktis_antarktis` |
| Forscher-Eponyme | Match | `uk_tiere_forscher_eponyme` |
| Pelagial-Zonen | Match | `uk_tiere_pelagial` |
| W\u00fcsten-Spezialisten | Match | `uk_tiere_wuesten_spezialisten` |
| Gift-Hotspots | Match | `uk_tiere_gift_hotspots` |
| Tier-Migranten | Match | `uk_tiere_migranten` |
| H/L Rinder-Dichte | H/L | `hl_tiere_haustier_dichte` |
| Pferderassen | Pin | `uk_pferde_rassen` |
| Pferde-Fachbegriffe | Match | `uk_pferde_fachbegriffe` |
| H/L Stockmaß | H/L | `hl_pferde_stockmass` |
| WS: Pferdeflüsterer | WS | `ws_pferde_fluesterer` |
| H/L Galopp-Speed | H/L | `hl_pferde_speed` |
| H/L Körpergewicht | H/L | `hl_pferde_gewicht` |
| Reitsport-Disziplinen | Match | `uk_pferde_reitsport` |
| WS: Hufeisen | WS | `ws_pferde_hufeisen` |

## 13.11 Pflanzen -- 48 Modi

*Botanische Gaerten, Nutzpflanzen, H/L Wuchs/Alter/Produktion, Klimazonen*

`12 H/L | 27 Match | 9 WS`


| Titel | Typ | Modus-ID |
|-------|-----|---------|
| Nutzpflanzen-Ursprung | Match | `uk_pflanzen_nutzpflanzen` |
| Ber\u00fchmte B\u00e4ume | Match | `uk_pflanzen_einzelbaeume` |
| Botanische G\u00e4rten | Match | `uk_pflanzen_botanische_gaerten` |
| Tropenwälder | Match | `uk_pflanzen_tropenwald` |
| Weinanbaugebiete | Match | `uk_pflanzen_weinanbau` |
| Heilpflanzen-Regionen | Match | `uk_pflanzen_heilpflanzen` |
| Mangrovenwälder | Match | `uk_pflanzen_mangroven` |
| Kakao-Ursprungsgebiete | Match | `uk_pflanzen_kakao_ursprung` |
| Reisanbauregionen | Match | `uk_pflanzen_reisanbau` |
| Bambuswälder | Match | `uk_pflanzen_bambus` |
| Endemische Pflanzenzonen | Match | `uk_pflanzen_endemisch` |
| Nationalblumen-Heimat | Match | `uk_pflanzen_nationalblumen` |
| H/L Wuchsh\u00f6he | H/L | `hl_pflanzen_wuchshoehe` |
| H/L Baumalter | H/L | `hl_pflanzen_alter` |
| H/L Fruchtgewicht | H/L | `hl_pflanzen_fruchtgewicht` |
| H/L Samengr\u00f6\u00dfe | H/L | `hl_pflanzen_samenlaenge` |
| H/L Kaffeeproduktion | H/L | `hl_pflanzen_kaffeeproduktion` |
| H/L Weinproduktion | H/L | `hl_pflanzen_weinproduktion` |
| H/L Reisproduktion | H/L | `hl_pflanzen_reisproduktion` |
| H/L Waldanteil | H/L | `hl_pflanzen_waldflaeche` |
| H/L Stammumfang | H/L | `hl_pflanzen_stammumfang` |
| H/L Blattfl\u00e4che | H/L | `hl_pflanzen_blattflaeche` |
| H/L Bl\u00fchtdauer | H/L | `hl_pflanzen_bluehdauer` |
| H/L Genomgr\u00f6\u00dfe | H/L | `hl_pflanzen_genomgroesse` |
| Gew\u00fcrze-Herkunft | Match | `uk_pflanzen_gewuerze` |
| Pflanzenfamilien | Match | `uk_pflanzen_familien` |
| Bl\u00fctezeit | Match | `uk_pflanzen_bluetezeit` |
| Giftstoffe | Match | `uk_pflanzen_giftstoffe` |
| Fruchttypen | Match | `uk_pflanzen_fruchttyp` |
| Vermehrungsarten | Match | `uk_pflanzen_vermehrung` |
| Pflanzen-Lebensraum | Match | `uk_pflanzen_lebensraum` |
| Best\u00e4uber | Match | `uk_pflanzen_bestuaeber` |
| Kulturpflanzen-Herkunft | Match | `uk_pflanzen_herkunft` |
| Pflanzennutzung | Match | `uk_pflanzen_nutzung` |
| Blattformen | Match | `uk_pflanzen_blattform` |
| Klimazonen | Match | `uk_pflanzen_klimazone` |
| Scheinfrüchte | Match | `uk_pflanzen_scheinfruchte` |
| Baum des Jahres | Match | `uk_pflanzen_baum_des_jahres` |
| Giftpflanze des Jahres | Match | `uk_pflanzen_giftpflanze_jahres` |
| WS: Trauerweide | WS | `ws_pflanzen_trauerweide` |
| WS: Rhododendron | WS | `ws_pflanzen_rhododendron` |
| WS: Sonnenblume | WS | `ws_pflanzen_sonnenblume` |
| WS: Pusteblume | WS | `ws_pflanzen_pusteblume` |
| WS: Nachtschatten | WS | `ws_pflanzen_nachtschatten` |
| WS: Vergissmeinnicht | WS | `ws_pflanzen_vergissmeinnicht` |
| WS: Kaffeebohne | WS | `ws_pflanzen_kaffeebohne` |
| WS: Weihnachtsstern | WS | `ws_pflanzen_weihnachtsstern` |
| WS: Ginkgobaum | WS | `ws_pflanzen_ginkgobaum` |

## 13.12 Gastronomie -- 51 Modi

*Nationalgerichte/Brauereien pinnen, H/L Kalorien/Scoville, Kuechen-Fachbegriffe*

`15 H/L | 29 Match | 7 WS`


| Titel | Typ | Modus-ID |
|-------|-----|---------|
| Nationalgerichte pinnen | Match | `uk_gastro_nationalgerichte` |
| Kaffee-Anbaugebiete | Match | `uk_gastro_kaffee_anbau` |
| Brauereien pinnen | Match | `uk_gastro_brauereien` |
| Seltene Gewürze orten | Match | `uk_gastro_gewuerze_selten` |
| Historische Kaffeehäuser | Match | `uk_gastro_kaffeehaeuser` |
| Schokoladenfabriken | Match | `uk_gastro_schokoladen` |
| Weinlagen & Châteaux | Match | `uk_gastro_weinlagen` |
| Fermentations-Orte | Match | `uk_gastro_fermentation_orte` |
| Kulinarische Festivals | Match | `uk_gastro_kulinarische_feste` |
| HL: Kalorien | H/L | `hl_gastro_kalorien` |
| HL: Kerntemperatur | H/L | `hl_gastro_kerntemperatur` |
| HL: Zubereitungszeit | H/L | `hl_gastro_zubereitungszeit` |
| HL: Fermentationsdauer | H/L | `hl_gastro_fermentationsdauer` |
| HL: Scoville-Skala | H/L | `hl_gastro_scoville` |
| HL: Preis pro Kilo | H/L | `hl_gastro_preis_kg` |
| HL: Wasseranteil | H/L | `hl_gastro_wasseranteil` |
| HL: Backtemperatur | H/L | `hl_gastro_backtemperatur` |
| HL: Rezept-Alter | H/L | `hl_gastro_rezept_alter` |
| HL: Alkoholgehalt | H/L | `hl_gastro_alkoholgehalt` |
| HL: Zutaten-Anzahl | H/L | `hl_gastro_zutaten_anzahl` |
| HL: Schmelzpunkt | H/L | `hl_gastro_schmelzpunkt` |
| HL: Pro-Kopf-Verbrauch | H/L | `hl_gastro_prokopf_verbrauch` |
| HL: Haltbarkeit | H/L | `hl_gastro_haltbarkeit` |
| HL: Rekord-Gewicht | H/L | `hl_gastro_rekord_gewicht` |
| Hausmannskost zuordnen | Match | `uk_gastro_hausmannskost` |
| Küchengeräte sortieren | Match | `uk_gastro_kuechengeraete` |
| Schnitttechniken | Match | `uk_gastro_schnitttechniken` |
| Geburtsort-Rezept | Match | `uk_gastro_originalrezept` |
| Teigtaschen der Welt | Match | `uk_gastro_teigtaschen` |
| Gewürzmischungen | Match | `uk_gastro_gewuerzmischungen` |
| Fleischzuschnitte | Match | `uk_gastro_fleisch_cuts` |
| Mikroorganismen & Fermentation | Match | `uk_gastro_bakterien_pilze` |
| Kaffeespezialitäten | Match | `uk_gastro_kaffeespezialitaeten` |
| Pasta & Saucen | Match | `uk_gastro_pasta_formen` |
| Exotische Früchte | Match | `uk_gastro_exotische_fruechte` |
| Brotsorten der Welt | Match | `uk_gastro_brotsorten` |
| Vegane Alternativen | Match | `uk_gastro_vegan_alternativen` |
| Frühstück der Welt | Match | `uk_gastro_fruehstueck_welt` |
| Kochfachbegriffe | Match | `uk_gastro_fachbegriffe_herd` |
| Sushi-Stile | Match | `uk_gastro_sushi_arten` |
| Ess-Etikette weltweit | Match | `uk_gastro_ess_etikette` |
| Nahrungstabus | Match | `uk_gastro_tabus` |
| Essen im Film | Match | `uk_gastro_film_food` |
| Seidenstraße & Gewürze | Match | `uk_gastro_seidenstrasse` |
| WS: Zitruspresse | WS | `ws_gastro_zitruspresse` |
| WS: Küchenmaschine | WS | `ws_gastro_kuechenmaschine` |
| WS: Sauerteigbrot | WS | `ws_gastro_sauerteigbrot` |
| WS: Fermentation | WS | `ws_gastro_fermentation` |
| WS: Wurzelgemüse | WS | `ws_gastro_wurzelgemuese` |
| WS: Schwarzwälder | WS | `ws_gastro_schwarzwaelder` |
| WS: Kaltentsafter | WS | `ws_gastro_kaltentsafter` |

## 13.13 Technologie -- 43 Modi

*Halbleiter-Fabs, Programmiersprachen, H/L Transistoren, OSI, HTTP, Turing Award*

`8 H/L | 25 Match | 10 WS`


| Titel | Typ | Modus-ID |
|-------|-----|---------|
| Tech: Programmiersprachen | Match | `uk_tech_programmiersprachen` |
| Tech: Wettbewerbe | Match | `uk_tech_wettbewerbe` |
| Tech: Halbleiter-Fabs | Match | `uk_tech_halbleiter` |
| Tech: Heimcomputer | Match | `uk_tech_heimcomputer` |
| Tech: Rechenzentren | Match | `uk_tech_rechenzentren` |
| Tech: Pioniere | Match | `uk_tech_pioniere` |
| Tech: Technologiemuseen | Match | `uk_tech_tech_museen` |
| Tech: Supercomputer | Match | `uk_tech_supercomputer` |
| Tech: Transistorenanzahl | H/L | `hl_tech_transistoren` |
| Tech: Taktfrequenz | H/L | `hl_tech_taktfrequenz` |
| Tech: Freiheitsgrade | H/L | `hl_tech_freiheitsgrade` |
| Tech: Codezeilen | H/L | `hl_tech_code_zeilen` |
| Tech: Release-Jahr | H/L | `hl_tech_release_jahr` |
| Tech: Rechenleistung | H/L | `hl_tech_rechenleistung` |
| Tech: Internetgeschwindigkeit | H/L | `hl_tech_internet_speed` |
| Tech: TDP-Wert | H/L | `hl_tech_tdp` |
| Tech: Sensoren | Match | `uk_tech_sensoren` |
| Tech: Code-Syntax | Match | `uk_tech_syntax` |
| Tech: Linux-Distros | Match | `uk_tech_linux` |
| Tech: OSI-Modell | Match | `uk_tech_osi` |
| Tech: Big-O | Match | `uk_tech_bigo` |
| Tech: HTTP-Statuscodes | Match | `uk_tech_http` |
| Tech: Logikgatter | Match | `uk_tech_wahrheitstabellen` |
| Tech: Hardware-Komponenten | Match | `uk_tech_hardware` |
| Tech: Technik-Erfinder | Match | `uk_tech_erfinder` |
| Tech: Portnummern | Match | `uk_tech_portnummern` |
| Tech: Dateiendungen | Match | `uk_tech_dateiendungen` |
| Tech: Smart Home | Match | `uk_tech_smart_home` |
| Tech: Akronyme | Match | `uk_tech_akronyme` |
| Tech: Turing Award | Match | `uk_tech_turing_award` |
| Tech: Erste Videospiele | Match | `uk_tech_erste_videospiele` |
| Tech: Malware-Typen | Match | `uk_tech_malware` |
| Tech: Uebernahmen | Match | `uk_tech_tech_ma` |
| WS: Mikrocontroller | WS | `ws_tech_mikrocontroller` |
| WS: Datenbankmanagement | WS | `ws_tech_datenbankmanagement` |
| WS: Algorithmus | WS | `ws_tech_algorithmus` |
| WS: Quantencomputer | WS | `ws_tech_quantencomputer` |
| WS: Prozessorarchitektur | WS | `ws_tech_prozessorarchitektur` |
| WS: Grafikprozessor | WS | `ws_tech_grafikprozessor` |
| WS: Cybersicherheit | WS | `ws_tech_cybersicherheit` |
| WS: Softwareentwicklung | WS | `ws_tech_softwareentwicklung` |
| WS: Compilerbau | WS | `ws_tech_compilerbau` |
| WS: Betriebssystem | WS | `ws_tech_betriebssystem` |

## 13.14 E-Mobilitaet -- 57 Modi

*Gigafactories/Ladeparks pinnen, H/L Reichweite/Kapazitaet, Steckernormen*

`12 H/L | 35 Match | 10 WS`


| Titel | Typ | Modus-ID |
|-------|-----|---------|
| E-Mob: Gigafactories | Match | `uk_emob_gigafactories` |
| E-Mob: EV-Startups | Match | `uk_emob_ev_startups` |
| E-Mob: Ladeparks | Match | `uk_emob_ladeparks` |
| E-Mob: Lithiumvorkommen | Match | `uk_emob_lithium` |
| E-Mob: Historische Werke | Match | `uk_emob_historische_werke` |
| E-Mob: Formel E | Match | `uk_emob_formel_e` |
| E-Mob: Solarparks | Match | `uk_emob_solarparks` |
| E-Mob: Autonome Tests | Match | `uk_emob_autonom_tests` |
| E-Mob: Batterieforschung | Match | `uk_emob_batterie_forschung` |
| E-Mob: EV-Dichte-Staedte | Match | `uk_emob_ev_dichte_staedte` |
| E-Mob: Batterie-Recycling | Match | `uk_emob_recycling` |
| E-Mob: Erste EVs | Match | `uk_emob_erste_evs` |
| E-Mob: EV-Roadtrips | Match | `uk_emob_roadtrips` |
| E-Mob: Batteriekapazitaet | H/L | `hl_emob_kapazitaet` |
| E-Mob: Ladeleistung | H/L | `hl_emob_ladeleistung` |
| E-Mob: WLTP-Reichweite | H/L | `hl_emob_wltp` |
| E-Mob: 0–100 km/h | H/L | `hl_emob_0_100` |
| E-Mob: Fahrzeuggewicht | H/L | `hl_emob_gewicht` |
| E-Mob: Ladezeit 10–80% | H/L | `hl_emob_ladezeit_10_80` |
| E-Mob: cw-Wert | H/L | `hl_emob_cw_wert` |
| E-Mob: Systemspannung | H/L | `hl_emob_systemspannung` |
| E-Mob: Ladeanschluesse | H/L | `hl_emob_ladeanschluesse` |
| E-Mob: Drehmoment | H/L | `hl_emob_drehmoment` |
| E-Mob: Basispreis | H/L | `hl_emob_preis` |
| E-Mob: Zellenanzahl | H/L | `hl_emob_zell_anzahl` |
| E-Mob: Ladestecker | Match | `uk_emob_stecker` |
| E-Mob: EV-Plattformen | Match | `uk_emob_plattformen` |
| E-Mob: Zellchemie | Match | `uk_emob_zellchemie` |
| E-Mob: Akronyme | Match | `uk_emob_akronyme` |
| E-Mob: Autonomiegrade | Match | `uk_emob_level_autonomy` |
| E-Mob: Motorentypen | Match | `uk_emob_motorentypen` |
| E-Mob: Thermomanagement | Match | `uk_emob_thermomanagement` |
| E-Mob: V2X-Technologie | Match | `uk_emob_bidirektional` |
| E-Mob: Ladekurven | Match | `uk_emob_ladekurven` |
| E-Mob: EV & Smart Home | Match | `uk_emob_smart_home` |
| E-Mob: EV-Privilegien | Match | `uk_emob_privilegien` |
| E-Mob: Ladeanschluss-Position | Match | `uk_emob_port_position` |
| E-Mob: EV-Reifen | Match | `uk_emob_ev_reifen` |
| E-Mob: Lade-Roaming | Match | `uk_emob_roaming` |
| E-Mob: Warnleuchten | Match | `uk_emob_warnleuchten` |
| E-Mob: Startup-Laender | Match | `uk_emob_startups_match` |
| E-Mob: Reichweiten-Killer | Match | `uk_emob_reichweiten_killer` |
| E-Mob: AVAS-Vorschriften | Match | `uk_emob_avas` |
| E-Mob: Subventionen | Match | `uk_emob_subventionen` |
| E-Mob: Ladetikette | Match | `uk_emob_etikette` |
| E-Mob: Konzeptfahrzeuge | Match | `uk_emob_konzeptautos` |
| E-Mob: Strommix | Match | `uk_emob_strommix` |
| WS: Schnellladestation | WS | `ws_emob_schnellladestation` |
| WS: Rekuperation | WS | `ws_emob_rekuperation` |
| WS: Reichweitenangst | WS | `ws_emob_reichweitenangst` |
| WS: Fahrassistenzsystem | WS | `ws_emob_fahrassistenzsystem` |
| WS: Bordnetzspannung | WS | `ws_emob_bordnetzspannung` |
| WS: Elektroantrieb | WS | `ws_emob_elektroantrieb` |
| WS: Wechselstromladen | WS | `ws_emob_wechselstromladen` |
| WS: Gleichstromladen | WS | `ws_emob_gleichstromladen` |
| WS: Batteriemanagement | WS | `ws_emob_batteriemanagement` |
| WS: Bidirektionalladen | WS | `ws_emob_bidirektionalladen` |

## 13.15 Archaeologie -- 60 Modi

*Ausgrabungsstaetten pinnen, H/L Alter/Fundtiefe, Epochen, Schriften, Faelschungen*

`12 H/L | 41 Match | 7 WS`


| Titel | Typ | Modus-ID |
|-------|-----|---------|
| Artefakt-Standorte | Match | `uk_arch_artefakte` |
| Megalith-Anlagen | Match | `uk_arch_megalithanlagen` |
| Versunkene St\u00e4dte | Match | `uk_arch_versunkene_staedte` |
| H\u00f6hlenmalereien | Match | `uk_arch_hoehlenmalerien` |
| Digital-Arch\u00e4ologie | Match | `uk_arch_digitalprojekte` |
| Nekropolen | Match | `uk_arch_graberfelder` |
| Schiffswracks | Match | `uk_arch_schiffswracks` |
| Maya & Inka-Ruinen | Match | `uk_arch_maya_inka` |
| R\u00f6mischer Limes | Match | `uk_arch_roemische_limes` |
| Pfahlbauten | Match | `uk_arch_pfahlbauten` |
| W\u00fcstenkulturen | Match | `uk_arch_wuestenstaedte` |
| Fossilienfundst\u00e4tten | Match | `uk_arch_fossilien` |
| Sensationsfunde | Match | `uk_arch_sensationsfunde` |
| H/L: Alter von Artefakten | H/L | `hl_arch_alter_artefakte` |
| H/L: Megalith-Gewicht | H/L | `hl_arch_gewicht_megalithen` |
| H/L: Entdeckungsjahr | H/L | `hl_arch_entdeckungsjahr` |
| H/L: Fundtiefe | H/L | `hl_arch_fundtiefe` |
| H/L: Gr\u00f6\u00dfe von Ruinen | H/L | `hl_arch_groesse_ruinen` |
| H/L: Grabbeigaben | H/L | `hl_arch_grabbeigaben` |
| H/L: Antike Stra\u00dfenl\u00e4nge | H/L | `hl_arch_strassenlaenge` |
| H/L: C14-Alter | H/L | `hl_arch_c14_alter` |
| H/L: 3D-Scan-Daten | H/L | `hl_arch_scandatenvolumen` |
| H/L: Bauzeit | H/L | `hl_arch_bauzeit` |
| H/L: H\u00f6he antiker Bauwerke | H/L | `hl_arch_hoehe_bauwerke` |
| H/L: Artefakt-Wert | H/L | `hl_arch_versicherungswert` |
| Artefakt-Epochen | Match | `uk_arch_epochen` |
| Antike Werkzeuge | Match | `uk_arch_werkzeuge` |
| Ber\u00fchmte Arch\u00e4ologen | Match | `uk_arch_archaeologen` |
| Datierungsmethoden | Match | `uk_arch_datierungsmethoden` |
| 3D-Dokumentation | Match | `uk_arch_3d_methoden` |
| Antike Schriften | Match | `uk_arch_schriften` |
| Antike G\u00f6tter | Match | `uk_arch_goetter` |
| Bestattungsr\u00e4ten | Match | `uk_arch_bestattungsriten` |
| Stratigraphie-Prinzipien | Match | `uk_arch_stratigraphie` |
| Keramikstile | Match | `uk_arch_keramikstile` |
| Antike M\u00fcnzen | Match | `uk_arch_numismatik` |
| Isotopenanalyse | Match | `uk_arch_isotopenanalyse` |
| Artefakte & Museen | Match | `uk_arch_museen` |
| Arch\u00e4obotanik | Match | `uk_arch_archaeobotanik` |
| Antike Handelsrouten | Match | `uk_arch_handelsrouten` |
| Antike W\u00e4hrungen | Match | `uk_arch_waehrungen` |
| Arch\u00e4ologische F\u00e4lschungen | Match | `uk_arch_faelschungen` |
| Griechische Tempelordnungen | Match | `uk_arch_tempel_ordnungen` |
| Indus-Tal-Kulturst\u00e4tten | Match | `uk_arch_indus_tal` |
| Wikinger-Siedlungen | Match | `uk_arch_wikinger` |
| Repatriierung | Match | `uk_arch_repatriierung` |
| Popkultur vs. Realit\u00e4t | Match | `uk_arch_popkultur_vs_realitaet` |
| UNESCO: Bedrohte Welterbe | Match | `uk_arch_welterbe_gefahr` |
| Zufallsfunde | Match | `uk_arch_zufallsfunde` |
| Digitalprojekte nach Epoche | Match | `uk_arch_digifund_epochen` |
| Antike Medizin | Match | `uk_arch_antike_medizin` |
| Surveymethoden | Match | `uk_arch_schatzsuche_methoden` |
| Antike Astronomie | Match | `uk_arch_antike_astronomie` |
| WS: Ausgrabungsst\u00e4tte | WS | `ws_arch_ausgrabungsstaette` |
| WS: Antiquit\u00e4t | WS | `ws_arch_antiquitaet` |
| WS: Dendrochronologie | WS | `ws_arch_dendrochronologie` |
| WS: Hieroglyphen | WS | `ws_arch_hieroglyphen` |
| WS: Photogrammetrie | WS | `ws_arch_photogrammetrie` |
| WS: Stratigraphie | WS | `ws_arch_stratigraphie` |
| WS: Radiocarbondatierung | WS | `ws_arch_radiocarbondatierung` |

## 13.16 Astronomie -- 28 Modi

*Observatorien/Startrampen pinnen, H/L Planeten/Monde/Raketen, Missionen*

`9 H/L | 15 Match | 4 WS`


| Titel | Typ | Modus-ID |
|-------|-----|---------|
| Observatorien-Standorte | Match | `uk_astro_observatorien` |
| Startrampen-Standorte | Match | `uk_astro_startrampen` |
| H/L: Planetengröße | H/L | `hl_astro_planet_groesse` |
| H/L: Monde-Anzahl | H/L | `hl_astro_monde_anzahl` |
| H/L: Sonnenentfernung | H/L | `hl_astro_sonnenentfernung` |
| Raumfahrt-Missionen | Match | `uk_astro_missionen` |
| Planeten-Fakten | Match | `uk_astro_planeten` |
| Kosmologie-Fakten | Match | `uk_astro_kosmologie` |
| WS: Sternwarte | WS | `ws_astro_sternwarte` |
| WS: Raumstation | WS | `ws_astro_raumstation` |
| WS: Astronaut | WS | `ws_astro_astronaut` |
| Kontrollzentren & Raumfahrtbehörden | Match | `uk_astro_esa_nasa_zentren` |
| Teleskop-Standorte weltweit | Match | `uk_astro_weltraumteleskope` |
| Meteoritenkrater orten | Match | `uk_astro_meteoritenkrater` |
| Dark-Sky-Reservate | Match | `uk_astro_dark_sky` |
| H/L: Raketen-Nutzlast | H/L | `hl_astro_raketen_nutzlast` |
| H/L: Missionsdauer | H/L | `hl_astro_missionsdauer` |
| H/L: Oberflächengravitation | H/L | `hl_astro_schwerkraft` |
| H/L: Oberflächentemperatur | H/L | `hl_astro_temperaturen` |
| H/L: Entdeckungsjahr | H/L | `hl_astro_entdeckungsjahr` |
| H/L: Exoplaneten-Distanz | H/L | `hl_astro_exoplaneten_distanz` |
| Raumsonden & Ziele | Match | `uk_astro_sonden_ziele` |
| Himmelskörper-Typen | Match | `uk_astro_himmelskoerper_typ` |
| Sternbilder zuordnen | Match | `uk_astro_sternbilder_himmel` |
| Astronomie-Pioniere | Match | `uk_astro_pioniere` |
| Raketenantriebe | Match | `uk_astro_antriebe` |
| Galaxien-Typen | Match | `uk_astro_galaxien_typen` |
| WS: Schwarzes Loch | WS | `ws_astro_schwarzesloch` |

## 13.17 Geologie -- 51 Modi

*Vulkane/Hoehlen/Canyons/Gletscher pinnen, H/L Mohs-Haerte/VEI/Bohrtiefe*

`13 H/L | 29 Match | 9 WS`


| Titel | Typ | Modus-ID |
|-------|-----|---------|
| Vulkan-Standorte | Match | `uk_geo_vulkane` |
| Geothermie-Standorte | Match | `uk_geo_geothermal` |
| H/L: Berghöhen | H/L | `hl_geo_berghoehen` |
| H/L: Vulkanhöhen | H/L | `hl_geo_vulkan_hoehen` |
| H/L: Erdbeben-Magnitude | H/L | `hl_geo_erdbeben` |
| Gesteinsarten-Quiz | Match | `uk_geo_gesteinsarten` |
| Tektonische Platten | Match | `uk_geo_tektonik` |
| Mineralien-Quiz | Match | `uk_geo_mineralien` |
| WS: Stalaktiten | WS | `ws_geo_stalaktiten` |
| WS: Vulkanismus | WS | `ws_geo_vulkanismus` |
| WS: Erdbeben | WS | `ws_geo_erdbeben` |
| Felsformationen weltweit | Match | `uk_geo_felsformationen` |
| Höhlensysteme orten | Match | `uk_geo_hoehlensysteme` |
| Canyons & Schluchten | Match | `uk_geo_canyons` |
| Geysire orten | Match | `uk_geo_geysire` |
| Fossilien-Fundstätten | Match | `uk_geo_fossilien_fundstaetten` |
| Ozeangraben-Standorte | Match | `uk_geo_ozeangraeben` |
| Gletscher orten | Match | `uk_geo_gletscher` |
| Wüsten & Dünenlandschaften | Match | `uk_geo_wuesten` |
| Minen & Tiefbohrungen | Match | `uk_geo_minen_bohrungen` |
| Tektonische Gräben & Rifts | Match | `uk_geo_rifts` |
| Geologische Nationalparks | Match | `uk_geo_nationalparks_geologie` |
| Steilküsten & Klippen | Match | `uk_geo_steilkuesten` |
| H/L: Mohs-Härte | H/L | `hl_geo_mohshaerte` |
| H/L: Vulkan-Explosivität | H/L | `hl_geo_vei_ausbruch` |
| H/L: Höhlenlänge | H/L | `hl_geo_hoehlen_laenge` |
| H/L: Gesteinsalter | H/L | `hl_geo_gesteins_alter` |
| H/L: Schluchten-Tiefe | H/L | `hl_geo_schluchten_tiefe` |
| H/L: Kontinentaldrift | H/L | `hl_geo_ko