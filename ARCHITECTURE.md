# GeoQuest — Architect's Handbook
## Systemdokumentation & Entwicklerhandbuch

**Version:** Phase 242 (Stand: Mai 2026)
**Build:** gen.py → 1.17 MB | GeoQuest.html → 2.21 MB | 558 Spielmodi

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

- **Zero-Backend-Dependency für Gameplay:** Alle 558 Spielmodi laufen komplett offline. Supabase wird optional für Cloud-Highscores genutzt, ist aber kein Pflichtbestandteil.
- **Single-File Output:** Das Build-System kompiliert alle Quellen zu einer einzigen `GeoQuest.html`. Hosting = eine Datei deployen.
- **Clientseitige Persistenz:** Spielfortschritt, Einstellungen und Sammlungen werden über `localStorage` gespeichert. Ein kryptografischer Salt schützt die Daten vor Manipulation.
- **PWA-Ready:** Externer Service Worker (`sw.js`, hash-versioniert, generiert durch `gen.py`) cached die App und alle 24 Datendateien für vollständigen Offline-Betrieb nach erstem Laden.
- **Offline-Score-Queue:** Scores, die offline gespielt werden, landen in `localStorage` (`gq_offline_queue`) und werden bei Rückkehr ins Netz automatisch mit Supabase synchronisiert.

### Philosophie: Content ≠ Logic

Die zentrale Architekturentscheidung ist die strikte Trennung von **Inhalt** (Daten in `data/*.json`) und **Logik** (Engines in `gen.py`). Neue Tiere, Gerichte oder Sehenswürdigkeiten hinzufügen bedeutet nur eine JSON-Datei editieren — kein Python-Code anfassen.

---

## 2. Build-Architektur

### Das Drei-Schichten-Modell

```
┌─────────────────────────────────────────────────────┐
│  CONTENT-SCHICHT          data/*.json               │
│  24 Datendateien: Kultur, Tiere, Pflanzen, Gastro,  │
│  Tech, E-Mob, Archäologie — je 4 Spieltypen         │
├─────────────────────────────────────────────────────┤
│  LOGIK-SCHICHT            gen.py                    │
│  Spielengines, UI-Renderer, State-Management        │
│  Sprache: Python (Build) + JavaScript (Runtime)     │
├─────────────────────────────────────────────────────┤
│  OUTPUT-SCHICHT           GeoQuest.html             │
│  Single-File-Build: alles inline, kein CDN-Pflicht  │
│  Größe: ~2.10 MB, JS-Anteil ~2.06 MB               │
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
   ... (weitere Datensätze — 24 JSON-Dateien gesamt)

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
    - Alle data/*.json (24 Stück) dynamisch gelistet
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
| sw.js: alle 24 data/*.json in ASSETS | `verify.py` Check 12 |
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
- `gen.py` ist 1.14 MB groß. Manuelle Edits in solchen Dateien erzeugen leicht Syntaxfehler oder ruinieren Unicode-Encoding.
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
| 10 | JSON round-trip | Alle 24 JSON-Dateien valide + Top-Level-Keys gezählt |
| 11 | _GQ_SALT | Salt im Output vorhanden (User-Saves-Schutz) |
| 12 | Service Worker | sw.js existiert, CACHE_NAME hash-versioniert, alle 24 data/*.json in ASSETS, Promise.allSettled vorhanden |

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
├── gen.py                  Haupt-Build-Skript (Logik, Engines, UI) — 1.14 MB
├── GeoQuest.html           Build-Output (Single-File-App) — 2.10 MB
├── index.html              Netlify-Deploy-Target (Kopie von GeoQuest.html)
├── sw.js                   Service Worker (generiert durch gen.py, hash-versioniert)
├── manifest.json           PWA Manifest (generiert durch gen.py)
├── icon.svg                App-Icon (alle Größen via SVG)
│
├── data/                   Content-Schicht (Phase 225–231, 24 Dateien)
│   ├── kultur.json             84 Kategorien: Getränke, Streetfood, Tänze, ...
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
│   └── archaeologie_ws.json     7 Wort-Schmiede-Einträge
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

**Aktueller Stand:** 558 Modi, 558/558/558 — perfekte Konsistenz.

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
  // ...558 Einträge total
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
Stufe 1 — SW-Cache (Phase 238):   App-Shell + alle 24 data/*.json offline verfügbar
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

**Offline-Banner im Profil-Tab:** Wenn `S.isOffline === true` erscheint eine rote Bena