# GeoQuest — Claude Session Starter
## Was du am Anfang JEDER Session diesem Dokument entnehmen und Claude mitgeben solltest

> Kopiere den Block unter **"Pflicht-Kontext"** an den Anfang deiner ersten Nachricht.
> Claude liest dann automatisch alle relevanten Dateien und macht danach alles korrekt.

---

## PFLICHT-KONTEXT (immer mitgeben)

```
Projekt: GeoQuest – Single-File Web-Quiz-App
Ordner:  C:\Users\Andre\Desktop\Cowork\Geoquest

Aktueller Stand (Stand: Phase 580):
- gen.py ist die EINZIGE Build-Quelle — aus ihr wird GeoQuest.html generiert
- 1099 Spielmodi in MODES-Array (gen.py)
- 74 JSON-Dateien in data/ (Spielinhalte, extern, per Placeholder geladen)
- Patch-System: patches/patch_NNN_description.py via run_patch.py
- Zero-Bug-Policy: assert c.count(old)==1 vor jedem c.replace()

Pflicht-Workflow nach JEDER Änderung:
1. python3 gen.py                → baut GeoQuest.html neu
2. python3 verify.py             → muss 173/173 (oder mehr) zeigen
3. python3 validate_content.py   → muss 0 warnings zeigen
4. python3 post_phase.py --phase NNN --summary "Beschreibung"
   ↳ aktualisiert AUTOMATISCH: ARCHITECTURE.md, README.md, GeoQuest_Website_Konzept.md,
     GeoQuest_Spielübersicht.html, unlock_and_push.bat UND dieses Dokument
     (CLAUDE_SESSION_STARTER.md: Phase, Modi-Zahl, verify-/validate-Score) — nicht von Hand pflegen!
5. python3 check_session.py      → Checks grün (prüft AUTOMATISCH auch, ob die Modi-Zahl in
     diesem Dokument zu gen.py passt, und warnt bei Abweichung)
6. unlock_and_push.bat           → deployed auf Vercel

⚠️ DEPLOY-/CACHE-FALLE (Phase 472): GeoQuest ist eine PWA mit cache-first Service Worker.
   Wenn Änderungen nach Deploy "nicht ankommen" (z.B. alte Karten trotz neuer Phase),
   liegt es fast immer am SW-Cache, NICHT am Build. Absicherung:
   - vercel.json setzt jetzt Cache-Control: no-cache auf /sw.js, /index.html (/play, Catch-all)
     und /manifest.json → Browser holt sw.js immer frisch, SW aktualisiert sich pro Build.
   - Beim Testen nach Deploy: einmal DevTools → Application → Service Workers → "Unregister"
     (oder "Clear site data"), dann neu laden. Ein blosses Strg+Shift+R umgeht den SW oft NICHT.
   - Konsistenz-Check: Sind ALLE neuen Features gleichzeitig weg, ist es der SW-Cache (eine alte
     index.html). Fehlt nur EIN Feature, ist es ein echter Code-Bug.

Wichtige Dateien zum Lesen:
- gen.py                    → Haupt-Build-Datei (~1.5 MB JS+Python)
- geoquest_css.txt          → ECHTE CSS-Quelle! (wird in gen.py geladen) — CSS NICHT in gen.py editieren, die dortigen .mode-card o.ä. sind tote Duplikate
- data/games_extended.json  → 70 Spiele, 27 Felder je Eintrag (inkl. protagonist, howlong_h)
- data/autos_extended.json  → 431 Autos, 22 Felder je Eintrag
- patches/PATCHES.md        → Alle bisherigen Patches mit Phase-Nummern
- ARCHITECTURE.md           → Systemdokumentation
- CLAUDE_SESSION_STARTER.md → Dieses Dokument — Phase/Modi/Scores werden von post_phase.py AUTOMATISCH aktualisiert & von check_session.py geprüft (Phase 422+); inhaltliche Notizen weiterhin manuell pflegen
- GeoQuest_Checkliste_und_Prompt_Template.md → AM ANFANG JEDER SESSION LESEN! Prompt-Vorlagen + Datei-Checkliste
- PERSONALISIERUNG_STATUS.md → Stand & offene Roadmap der Kinder-/Personalisierungs-Features (bei Neustart lesen!)
- check_session.py          → NEU: Session-End-Check (14 Punkte)
```

---

## PROJEKT-ÜBERBLICK FÜR CLAUDE

### Architektur in 30 Sekunden
```
gen.py (Python + eingebettetes JS)
  ├── Lädt data/*.json zur Build-Zeit
  ├── Ersetzt PLACEHOLDER_XXX im JS mit JSON-Daten
  ├── Schreibt GeoQuest.html (= index.html, ~5.5 MB)
  └── Schreibt sw.js (Service Worker für Offline)

GeoQuest.html
  ├── Gesamte App als Single File
  ├── Alle Daten inline als JS-Konstanten
  └── Keine externen API-Calls für Gameplay
```

### Spielmodi-Struktur
Jeder Modus braucht **3 Einträge** — alle drei müssen synchron sein:
```javascript
// 1. MODES-Array (Metadaten: title, icon, group, prompt, desc)
{id:"mein_modus", icon:"🎯", title:"Titel", group:"kategorie", ...}

// 2. MODE_CATS (Kategorie-Zuordnung)
kategorie: {modes: [..., "mein_modus", ...]}

// 3. GEN-Dispatch (Generator-Funktion)
mein_modus: () => meinGenerator()
```

### Daten-Schema games_extended.json (22 Pflichtfelder)
```
release, kategorie*, publisher, publisher_land, developer, dev_land,
dev_city, dev_lat, dev_lng, genre*, usk, pegi, f2p (bool), vk_mio,
downloads_mio, peak_concurrent_mio, metacritic, plattform*,
vorbild_land, adaption*, esports (bool), sequel_count,
peak_year, publisher_lat, publisher_lng,  ← Phase 405
protagonist, howlong_h                    ← Phase 410 (optional, None erlaubt)

* Enum-Felder:
  kategorie:  "Modern Youth" | "Global Mobile" | "Klassiker" | "Indie"
  plattform:  "PC" | "Konsole" | "Mobil" | "Multiplattform"
  adaption:   null | "Film" | "Serie" | "Anime"
  genre:      "Sandbox" | "Battle Royale" | "Rollenspiel" | "Ego-Shooter" |
              "Action-Adventure" | "Strategie" | "Jump 'n' Run" |
              "Sportsimulation" | "Puzzle" | "MOBA" | "Party-Spiel" |
              "Kampfspiel" | "Rennspiel" | "Social Deduction" |
              "Endless Runner" | "MMO"
```

### Placeholder-Reihenfolge in gen.py (KRITISCH!)
```python
# Spezifischste zuerst — sonst Substring-Kollision!
.replace('PLACEHOLDER_AUTOS_EXT', AUTOS_EXT_J)   # VOR AUTOS!
.replace('PLACEHOLDER_GAMES_EXT', GAMES_EXT_J)
.replace('PLACEHOLDER_AUTOS',     AUTOS_J)        # NACH AUTOS_EXT!
```

---

## WAS CLAUDE AUTOMATISCH TUN SOLL

Wenn du eine neue Aufgabe gibst, soll Claude **ohne Nachfragen**:

### Bei neuen Spielmodi
- [ ] **GEO-BEZUG-PFLICHT (oberste Regel):** JEDES Spiel MUSS einen geografischen Bezug haben — der Name ist „**Geo**Quest“. Eine Frage muss sich auf Länder, Kontinente, Regionen, Orte, Karten **oder** darauf beziehen, *wo* etwas vorkommt (z. B. „wo lebt dieses Tier“, „aus welchem Land kommt dieses Essen“). Reines Sach-/Tier-/Allgemeintrivia ohne Ortsbezug ist **nicht erlaubt**. Im Zweifel: Geo-Bezug ergänzen oder Spiel verwerfen.
- [ ] **Geo-Split (Allgemeinwissen):** Neue Modi gelten automatisch als **Geo** (Hauptbereich). Ein bewusst NICHT-geo Modus muss seine id in `NON_GEO_IDS` (gen.py, nahe `KIDS_CATS`) eintragen, sonst erscheint er im Geo-Hauptbereich. Steuert mit: `_catGeoRich` (Empfehlungen), `DAILY_POOL_GEO` (Daily), `renderRecentBar`/`playRandomGame` (geo-gefiltert). Umschalter: `S.nonGeo`.
- [ ] MODES-Eintrag mit allen Feldern (id, icon, title, group, prompt, desc, prompt_en)
- [ ] MODE_CATS-Eintrag in der richtigen Kategorie
- [ ] GEN-Dispatch-Eintrag
- [ ] Generator-Funktion (falls neu benötigt)
- [ ] **NIEMALS harte Strings ins UI rendern!** Neue Prompts/Labels MÜSSEN in `_CONTENT_I18N` (DE/EN/PL) eingetragen und im Code via `_tc()` oder `_tcc()` abgerufen werden. Deutsche Texte direkt im JS schließen EN/PL-Spieler aus — striktes Verbot.
- [ ] **DATEN-UMFANG (Ziel 80, min. 50):** Datensätze sollen — wo sinnvoll & exakt belegbar — auf **~80 Einträge** (mind. 50) kommen, sonst wird's schnell langweilig. Erweiterung NUR mit **web-verifizierten** Werten. Achtung: **volatile Felder** (Umsatz, Mitarbeiterzahl) liefern per Schnellsuche oft falsche/jahresverwechselte Werte → nur aus offizieller Primärquelle übernehmen oder Eintrag zurückstellen. **Stabile Fakten** (Gründungsjahr, Land, Gründer, Geschichts-/Mythologie-/Geo-Fakten) sind verlässlich erweiterbar.
- [ ] **GENAUIGKEIT ÜBER ALLEM — keine Halluzinationen:** Niemals Daten raten/erfinden. Neue Datenwerte nur aus **kuratierten Projektdaten** oder **per Web-Recherche verifiziert**. Bei Unsicherheit: Feld weglassen (lieber weniger Einträge als ein falscher). Mehrdeutige Fälle (Grenz-Bauwerke, Tunnel, spannende Brücken) bekommen kein eindeutiges Ortsfeld.
- [ ] **Datenbasis IMMER gefüllt:** Jeder neue Modus braucht eine echte Datengrundlage (genug Items für sinnvolle Frage + Distraktoren). In der Spielübersicht (`generate_spieluebersicht.py`) muss die Spalte „Datenbasis“ einen Wert zeigen — eine Zahl **oder** „dyn“ (laufzeit-/COUNTRIES-/Inline-basiert, per Smoke-Test geprüft). **Niemals leer/„—“.** Pflicht: `node smoke_test.js` deckt den Modus mit echten Fragen ab (0 NULL/THROW).
- [ ] validate_content.py ausführen → 0 warnings
- [ ] MODES-Zahl in gen.py zählen (nicht JSON-Keys!)
- [ ] post_phase.py mit korrekter Phase-Nummer ausführen
- [ ] PATCHES.md Eintrag ergänzen

## TEST-SUITE (gegen Fehler & Anzeigefehler) — Phase 511–545

**9 Ebenen**, die unterschiedliche Bug-Klassen fangen. **Vor jedem Deploy alle laufen lassen:**

1. `python3 verify.py` — Struktur/Build: undefinierte `*_DATA` (Check 20) & Helfer (Check 21), Dispatch, node --check, SW-App-Shell+Runtime-Cache (Check 12). Muss **195+/… | 0 failed**.
2. `python3 validate_content.py` — Daten/JSON. Muss **0 warnings**.
3. `node smoke_test.js` — **Generator-Laufzeit:** jeder GEN-Modus 6×. Muss **0 THROW** + **0 UNERWARTET NULL** (Allowlist `EXPECTED_NULL` = async-Daten + Custom-Flow).
4. `node ingame_render_test.js` — **Render-Laufzeit:** rendert JEDEN Modus (ungespielt + beantwortet) + seedet async-Daten (border/neighbor/plate/river/hl_area) + SRS-Replay + neue UI (Daily/SRS/Region). Muss **0 RENDER-FEHLER**.
5. `node option_quality_test.js` — doppelte/einzelne MC-Optionen. Muss **0 DUP / 0 SINGLE**.
6. `node i18n_test.js` — **i18n-Vollständigkeit:** jeder genutzte `_tc/_tcc`-String + `MODES.prompt` in de/en/pl. Muss **0 FEHLT**. (Übersetzungen in `data/i18n_extra.json`, reproduzierbar via `build_i18n_extra.py`.)
7. `python3 contrast_check.py` — WCAG-AA Text-auf-Fläche (Hell+Dunkel). Muss **0 FAIL**.
8. `python3 perf_check.py` — HTML-/SW-Precache-Größe. Muss **0 FAIL** (WARN = Hinweis).
9. `python3 a11y_check.py` — `<img>` ohne `alt` (FAIL) + Icon-Buttons ohne Label (WARN). Muss **0 FAIL**.

Zusätzlich informativ (blockt nicht): `python3 i18n_html_check.py` — findet hartkodiertes Deutsch im HTML, das nicht über `_tc` läuft (Wegweiser für i18n-Restarbeiten).

**Warum getrennt:** verify=Struktur, smoke=Generatoren *laufen*, ingame_render=Ergebnis *darstellbar*, dann Options/i18n/Kontrast/Performance/A11y. Ein Bug rutscht nur durch, wenn er ALLE besteht.

**Globales Render-Sicherheitsnetz (Phase 528):** `render()` ist ein try/catch-Wrapper um `_renderInner()` — bei jedem Render-Fehler erscheint ein Fallback („Überspringen"/„Zum Menü") statt White-Screen.

## LERN-/RETENTION-FEATURES (Phase 533–546) — Überblick

- **Daily Challenge** (`startDailyChallenge`/`renderDailyHero`): 1 Modus/Tag über `DAILY_POOL`+`getDailySeed`, Resume, 7-Tage-Liste, **30-Tage-Streak-Raster** (`_dailyDots`), **teilbares Emoji-Ergebnis** (`shareDailyResult`, `S.dailyMarks`).
- **Spaced Repetition / Fehler-Training** (`gq_srs`, Leitner): falsche Fragen → Snapshot (`_srsAdd`, nur MC/HL/Pin), Boxen 1–5 (`_srsGrade`), Modus „Schwächen üben" (`startSrsReview`/`srsNext`, `S.srsRun` → `nextRound` ruft `srsNext`). **Fehler-Tagebuch** (`renderSrsListModal`, Statistik + Leeren). An/aus via `gq_srs_off` (Einstellungen, `_srsToggle`). Home-Card `renderSrsHero`.
- **Region üben** (`renderRegionModal`/`renderRegionEntry`): Sub-Regionen-Filter zentral über `_regionOk` (`sub:<sr>`) — alle Geo-Generatoren via `_rfilt` betroffen, pro Spiel gescopt (`S._pendingFilter`→`startGame`). **Lernkarten** (`renderLearnDeck`, Flagge+Land+Hauptstadt) → „Jetzt testen" mit **Hauptstädten ODER Flaggen**; Kontinent-Quiz (`startContinent`/`_GRP_FILTER`).
- **Neue Spiele:** `geo_subregion` (Land→Region) + `geo_continent` (Land→Kontinent), beide `uk_match`, nutzen `COUNTRIES.sr`/`.ct` + `_SR_DE`/`_CONT_DE`.
- **In-Game-Doku:** Header-„?" → Hilfe (`renderHelpModal`) → „Mehr" → Handbuch (`renderGuideModal`, Tabs Kinder/Eltern). Neuer Abschnitt `guide_p7` „Lernen & Wiederholen" deckt obige Features ab (DE/EN/PL).

## ALTERSSTUFEN-KRITERIEN (für neue Spiele) — Phase 496–497

Die sichtbare Schwierigkeit steuert **`_modeLevel(m)`** (in gen.py) + **`_kidLevelMax()`** (aus `gq_kids_grade`). Ein Kind/Jugendlicher sieht einen Modus nur, wenn `_modeLevel(m) <= _kidLevelMax()`. Stufen: 1=6–8 · 2=8–10 · 3=11–13 · 4=14–15 · 5=16+/Erwachsene.

**So wird ein neuer Modus eingestuft (Reihenfolge in `_modeLevel`):**
1. **Explizite Level-1-Liste** (am Anfang von `_modeLevel`): die Lehrplan-Spiele (`kompass_richtung`, `kontinent_finder`, `ozean_finder`, `tier_lebensraum`, `jahreszeit_halbkugel`). Neues Stufe-1-Spiel ⇒ ID hier eintragen.
2. **`ws_…` / `_ws_`** (Wort-Schmiede) ⇒ Level 3.
3. **`match` / `_mc` / `timeline`** im id ⇒ Level 2 (NICHT mehr 1!).
4. **`hl_…`** (Höher/Tiefer-Vergleich) ⇒ Level 2.
5. **Teen-Token im id** (`auto`,`games`,`konsole`,`hw_`,`myth`,`lit_`,`boardgame`,`zug`,`bahn`,`timeline`) ⇒ Level 3 (auch `hl_`-Varianten).
6. **HARD-Keywords** (metacritic, imdb, pegi, hubraum, dichte, streams, umsatz, exoplanet, grammys, oscars … ) **oder HID-Signale** (`_bj`,`baujahr`,`_release`,`peak_year`,`erscheinungsjahr`,`reisezeit`,`breitengrad`,`_dekade`) ⇒ **Level 5** (erst ab 16).

**Was ein Spiel je Stufe erfüllen muss (Curriculum-Leitlinie, international):**
- **Stufe 1 (6–8, KS1):** bild-/symbolbasiert & spracharm (Emoji/Flagge/Pfeil als Frage), genau 1 klare richtige Antwort aus ≤4 Optionen, KEINE auswendig zu wissenden Eigennamen/Fakten außer sehr bekannten; Inhalt: Kontinente, Ozeane, Tiere↔Lebensraum, Himmelsrichtungen, Wetter/Jahreszeiten. Sollte intern mitwachsen. ⇒ in die explizite Level-1-Liste.
- **Stufe 2 (8–10, KS2):** Geografie & Natur: Kontinent-/Land-/Ozean-Zuordnung, Flaggen, Hauptstädte, Flüsse/Inseln/Gipfel, Klimazonen, Tiere/Pflanzen, einfache Vergleiche (größer/höher/schneller). Mechanik `match`/`_mc`/`hl_` reicht für Level 2. KEIN Spezial-/Industrie-Trivia.
- **Stufe 3 (11–13, Sek. I):** Special-Interest & vertieftes Wissen: Games (Genre/Publisher/Plattform), Autos (Technik/Marke), Mythologie, Literatur, Brettspiele, Bahn/Technik, Wort-Schmiede. Vertiefte Geografie ohne reine Zahlentrivia.
- **Stufe 4 (14–15):** vertiefte physische/menschliche Geografie & Naturwissenschaft (Klimadiagramme, Tektonik, Bevölkerung) — OHNE reines Erwachsenen-Trivia. (Aktuell sieht Stufe 4 dasselbe wie Stufe 3, da kein Modus exklusiv Level 4 ist; bei Bedarf gezielt Level-4-Inhalte ergänzen.)
- **Erst ab 16 (Erwachsene):** reines Trivia/Industriedaten — Jahreszahlen, Metacritic/IMDb, Oscars/Grammys, Streams/Verkäufe, technische Kennzahlen (Hubraum, Dichte, Breitengrad). Wird über HARD/HID automatisch auf Level 5 gesetzt.

**Faustregel beim Neubau:** Kann ein typisches Kind dieser Stufe die Frage UND die Antwort ohne Spezialwissen verstehen? Wenn nein → höhere Stufe. Prüfen mit dem Stufen-Runtime-Check (siehe `/tmp/age1.js`-Muster: App laden, `gq_kids_grade` setzen, `_modeLevel` je Modus auswerten).

### Bei neuen Daten (games/autos_extended.json)
- [ ] Alle 22 Pflichtfelder vorhanden
- [ ] Enums korrekt (kategorie, plattform, adaption, genre)
- [ ] f2p und esports sind Python-Booleans (True/False, nicht "true")
- [ ] dev_lat/dev_lng sind plausibel (nicht 0.0/0.0, korrektes Land)
- [ ] f2p=True → vk_mio=0.0
- [ ] **Schema-Änderung = Validator-Update!** Wenn ein neues Feld hinzukommt (z.B. `peak_year`), MUSS es sofort in `validate_content.py` → `check_games_extended()` als Pflicht- oder optionales Feld eingetragen werden. Sonst bleibt der Gatekeeper blind.
- [ ] validate_content.py ausführen

### Bei neuen WS-JSONs (Wortschmiede-Daten)
- [ ] `validate_content.py` nach dem Patch ausführen — stellt sicher, dass beide WS-Dateien mit **✓ OK** ausgewiesen werden
- [ ] Validator prüft: jeder Buchstabe im `validWords`-Eintrag muss aus dem Basis-Wort spellbar sein (z.B. BORN in RHODODENDRON = Fehler, kein B vorhanden)
- [ ] Keine Duplikate innerhalb derselben Sprache (EN, DE, PL)
- [ ] Mindestens 20 deutsche Wörter pro WS-Eintrag anstreben; Validator warnt ab <3 spielbaren Wörtern
- [ ] Bei kurzen Basis-Wörtern (≤8 Buchstaben, z.B. LOOPING) sind 20 DE-Wörter ggf. nicht erreichbar — dann mindestens 10 anstreben

### Bei Bugfixes / Audits
- [ ] verify.py ausführen und Ergebnis prüfen
- [ ] validate_content.py ausführen
- [ ] Fixes direkt anwenden (nicht nur beschreiben)
- [ ] PHASE4XX_AUDIT.md erstellen mit Findings-Tabelle
- [ ] PATCHES.md aktualisieren
- [ ] **Vollständiger Umfang siehe Sektion „AUDIT-UMFANG" unten**

---

## AUDIT-UMFANG (was IMMER geprüft wird)

Ein vollständiges Audit deckt diese 9 Dimensionen ab. Findings + angewandte Fixes in `PHASE<NNN>_AUDIT.md` (Tabelle: Befund · Schweregrad · Fix). Schweregrade: 🔴 kritisch · 🟠 mittel · 🟡 niedrig · ✅ ok.

1. **Build-Integrität** — `python3 gen.py` läuft fehlerfrei · `verify.py` grün · `validate_content.py` 0 Warnings · `check_session.py` grün · GeoQuest.html == index.html · keine `PLACEHOLDER_`-Reste im HTML.
2. **Sicherheit** — `esc()` in ALLEN innerHTML-Pfaden mit Nutzer-/Daten-Inhalt · kein `eval`/`new Function` mit Fremddaten · Prototype-Schutz (`hasOwnProperty`) · `JSON.parse`/`localStorage` in try/catch.
3. **MODES-Konsistenz** — MODES ↔ MODE_CATS ↔ GEN-Dispatch deckungsgleich · keine doppelten `id:` · H/L-Inversions-Falle (`lowerWins:true`, wenn kleiner = besser).
4. **Daten-Qualität** — alle Pflichtfelder · Enums gültig · Koordinaten plausibel (nicht 0/0, korrektes Land) · Cross-Validation (validate_content.py).
5. **i18n** — KEINE hartkodierten deutschen UI-Strings (alles via `t()`/`_tc()`) · DE/EN/PL vollständig · neue Keys in allen Sprachen.
6. **UX / Barrierefreiheit** — Touch-Targets ≥ 24px · lesbare Schriftgrößen (Labels nicht < ~10px) · interaktive Elemente tastatur-/ARIA-tauglich (`role`, `tabindex`, `aria-label`) · keine gequetschten/umbrechenden Layouts.
7. **Performance** — GeoQuest.html-Größe & Parse-Last im Blick (Lazy-Loading erwägen, wenn Startzeit problematisch) · keine Endlos-Renders/Timer-Leaks.
8. **Doku-Sync** — ARCHITECTURE/README/Konzept/Spielübersicht/Session-Starter aktuell (post_phase.py automatisch) · PATCHES.md-Eintrag vorhanden.
9. **Toter / redundanter Code** — keine ungenutzten CSS-Klassen oder Duplikate (z.B. CSS gehört NUR in geoquest_css.txt) · alte Backups aufräumen.

### Immer am Ende — SCHNELLWEG
```bash
python3 check_session.py   # prüft ALLES in einem Rutsch (14 Checks)
```
Oder manuell:
- [ ] verify.py: X/173 passed, 0 failed
- [ ] validate_content.py: 74/74 OK, 0 warnings
- [ ] ARCHITECTURE.md: Phase + Modi-Zahl aktualisiert
- [ ] README.md: Deployed-Zeile aktualisiert
- [ ] landing.html: Modi-Zahl aktualisiert
- [ ] GeoQuest_Website_Konzept.md: aktualisiert
- [ ] PATCHES.md: neuer Eintrag

---

## BEKANNTE AUTOMATISIERUNGSLÜCKEN (Claude soll diese kompensieren)

| Lücke | Was Claude stattdessen tut |
|-------|---------------------------|
| `post_phase.py` zählt JSON-Keys statt MODES | Claude liest MODES-Count direkt mit `re.findall(r'id:"', MODES_block)` |
| `GeoQuest_Spieluebersicht.html` wird nicht auto-rebuilt | Nach großen Modi-Erweiterungen: `python3 generate_spieluebersicht.py` aufrufen |
| `landing.html` hat eigene (veraltete) Modi-Zahl | Claude ersetzt binär mit `open('landing.html','rb')` + `.replace()` |
| `gen.py.bak_*` Backups häufen sich im Root an | Claude löscht Backups älter als 7 Tage nach erfolgreichem verify |
| `verify.py` kennt nicht alle neuen MODES-IDs | Wenn neue Sonder-Prefixes entstehen, NO_GEN_PFX in verify.py Zeile ~223 erweitern |

---

## TIPPS FÜR EFFIZIENTE SESSIONS

### Schnelle Aufgaben (sag einfach):
- `"Füge Spiel X zu games_extended.json hinzu