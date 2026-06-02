# GeoQuest — Claude Session Starter
## Was du am Anfang JEDER Session diesem Dokument entnehmen und Claude mitgeben solltest

> Kopiere den Block unter **"Pflicht-Kontext"** an den Anfang deiner ersten Nachricht.
> Claude liest dann automatisch alle relevanten Dateien und macht danach alles korrekt.

---

## PFLICHT-KONTEXT (immer mitgeben)

```
Projekt: GeoQuest – Single-File Web-Quiz-App
Ordner:  C:\Users\Andre\Desktop\Cowork\Geoquest

Aktueller Stand (Stand: Phase 431):
- gen.py ist die EINZIGE Build-Quelle — aus ihr wird GeoQuest.html generiert
- 874 Spielmodi in MODES-Array (gen.py)
- 53 JSON-Dateien in data/ (Spielinhalte, extern, per Placeholder geladen)
- Patch-System: patches/patch_NNN_description.py via run_patch.py
- Zero-Bug-Policy: assert c.count(old)==1 vor jedem c.replace()

Pflicht-Workflow nach JEDER Änderung:
1. python3 gen.py                → baut GeoQuest.html neu
2. python3 verify.py             → muss 143/143 (oder mehr) zeigen
3. python3 validate_content.py   → muss 0 warnings zeigen
4. python3 post_phase.py --phase NNN --summary "Beschreibung"
   ↳ aktualisiert AUTOMATISCH: ARCHITECTURE.md, README.md, GeoQuest_Website_Konzept.md,
     GeoQuest_Spielübersicht.html, unlock_and_push.bat UND dieses Dokument
     (CLAUDE_SESSION_STARTER.md: Phase, Modi-Zahl, verify-/validate-Score) — nicht von Hand pflegen!
5. python3 check_session.py      → Checks grün (prüft AUTOMATISCH auch, ob die Modi-Zahl in
     diesem Dokument zu gen.py passt, und warnt bei Abweichung)
6. unlock_and_push.bat           → deployed auf Vercel

Wichtige Dateien zum Lesen:
- gen.py                    → Haupt-Build-Datei (~1.5 MB JS+Python)
- geoquest_css.txt          → ECHTE CSS-Quelle! (wird in gen.py geladen) — CSS NICHT in gen.py editieren, die dortigen .mode-card o.ä. sind tote Duplikate
- data/games_extended.json  → 70 Spiele, 27 Felder je Eintrag (inkl. protagonist, howlong_h)
- data/autos_extended.json  → 431 Autos, 22 Felder je Eintrag
- patches/PATCHES.md        → Alle bisherigen Patches mit Phase-Nummern
- ARCHITECTURE.md           → Systemdokumentation
- CLAUDE_SESSION_STARTER.md → Dieses Dokument — Phase/Modi/Scores werden von post_phase.py AUTOMATISCH aktualisiert & von check_session.py geprüft (Phase 422+); inhaltliche Notizen weiterhin manuell pflegen
- GeoQuest_Checkliste_und_Prompt_Template.md → AM ANFANG JEDER SESSION LESEN! Prompt-Vorlagen + Datei-Checkliste
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
- [ ] MODES-Eintrag mit allen Feldern (id, icon, title, group, prompt, desc, prompt_en)
- [ ] MODE_CATS-Eintrag in der richtigen Kategorie
- [ ] GEN-Dispatch-Eintrag
- [ ] Generator-Funktion (falls neu benötigt)
- [ ] **NIEMALS harte Strings ins UI rendern!** Neue Prompts/Labels MÜSSEN in `_CONTENT_I18N` (DE/EN/PL) eingetragen und im Code via `_tc()` oder `_tcc()` abgerufen werden. Deutsche Texte direkt im JS schließen EN/PL-Spieler aus — striktes Verbot.
- [ ] validate_content.py ausführen → 0 warnings
- [ ] MODES-Zahl in gen.py zählen (nicht JSON-Keys!)
- [ ] post_phase.py mit korrekter Phase-Nummer ausführen
- [ ] PATCHES.md Eintrag ergänzen

### Bei neuen Daten (games/autos_extended.json)
- [ ] Alle 22 Pflichtfelder vorhanden
- [ ] Enums korrekt (kategorie, plattform, adaption, genre)
- [ ] f2p und esports sind Python-Booleans (True/False, nicht "true")
- [ ] dev_lat/dev_lng sind plausibel (nicht 0.0/0.0, korrektes Land)
- [ ] f2p=True → vk_mio=0.0
- [ ] **Schema-Änderung = Validator-Update!** Wenn ein neues Feld hinzukommt (z.B. `peak_year`), MUSS es sofort in `validate_content.py` → `check_games_extended()` als Pflicht- oder optionales Feld eingetragen werden. Sonst bleibt der Gatekeeper blind.
- [ ] validate_content.py ausführen

### Bei Bugfixes / Audits
- [ ] verify.py ausführen und Ergebnis prüfen
- [ ] validate_content.py ausführen
- [ ] Fixes direkt anwenden (nicht nur beschreiben)
- [ ] PHASE4XX_AUDIT.md erstellen mit Findings-Tabelle
- [ ] PATCHES.md aktualisieren

### Immer am Ende — SCHNELLWEG
```bash
python3 check_session.py   # prüft ALLES in einem Rutsch (14 Checks)
```
Oder manuell:
- [ ] verify.py: X/152 passed, 0 failed
- [ ] validate_content.py: 53/53 OK, 0 warnings
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
- `"Füge Spiel X zu games_extended.json hinzu"` → Claude prüft Schema, fügt ein, validiert
- `"Neuer Modus: [Beschreibung]"` → Claude implementiert alle 3 Einträge + Generator
- `"Audit Phase NNN"` → Claude liest alle Kern-Dateien und liefert Findings + Fixes

### Für größere Erweiterungen (gib diese Infos mit):
- **Phase-Nummer** (nächste wäre 425)
- **Kategorie** (games, autos, tiere, pflanzen, gastro, tech, emob, archäologie, astro, geo, sport)
- **Daten-Format** (JSON-Schema, Python-Dict mit Feldbeschreibungen)
- **Erwartete Modi-Typen** (H/L, Match, Pin, Wort-Schmiede, Multiple-Choice)

### H/L-Inversions-Falle (KRITISCH):
**Wenn ein kleinerer Wert "besser" oder "schneller" ist, MUSS `lowerWins: true` gesetzt sein.**  
Beispiele: 0–100 km/h Beschleunigung, Spritverbrauch (L/100km), cw-Wert, Platzierungen.  
Ohne `lowerWins: true` gewinnt immer die höhere Zahl — das wäre bei Verbrauch oder Beschleunigung falsch.
```javascript
// RICHTIG:
hl_auto_accel: ()=>genAutosHLExt("accel",{lowerWins:true, unit:"s", prompt:_tc("...")})
// FALSCH (fehlendes lowerWins):
hl_auto_accel: ()=>genAutosHLExt("accel",{unit:"s", prompt:_tc("...")})
```

### Für Sicherheits-/Qualitäts-Sprints:
- Sag explizit: `"Phase 400 Audit"` oder `"Security Review"`
- Claude wendet Fixes direkt an (kein reines Reporting)
- Claude führt danach validate + verify aus

---

## AKTUELLER PROJEKT-STATUS (Phase 431)

| Metrik | Wert |
|--------|------|
| Spielmodi | **874** |
| Fahrzeuge (autos_extended) | 431 |
| Spiele (games_extended) | 70 |
| Konsolen (konsolen.json) | 30 |
| JSON-Datendateien | 47 |
| gen.py Größe | ~1.53 MB |
| GeoQuest.html Größe | ~5.5 MB |
| verify.py | 159/159 ✓ |
| validate_content.py | 60/60 ✓ 0 Warnings |
| Sprachen vollständig (de/en/pl) | ✓ |
| Offline/PWA | ✓ |
| iOS Timeline-Bug | ✅ gefixt (Phase 412) |

### Gaming-Kategorie (Phase 360-402)
| Modi-ID | Beschreibung |
|---------|-------------|
| games_pin | Studio auf Weltkarte einpinnen |
| games_match_land | Herkunftsland des Studios |
| games_match_genre | Genre zuordnen |
| games_match_adaption | Verfilmung/Adaption |
| games_match_plattform | Plattform |
| games_match_kategorie | Gaming-Ära (Modern/Mobile/Klassiker) |
| games_match_publisher | Publisher (Phase 402) |
| games_match_f2p | F2P oder Kaufspiel? (Phase 402) |
| hl_games_release | Erscheinungsjahr H/L |
| hl_games_vk | Verkaufszahlen H/L |
| hl_games_downloads | Downloads H/L |
| hl_games_metacritic | Metacritic H/L |
| hl_games_usk | Altersfreigabe USK H/L |
| hl_games_sequel | Teile-Anzahl H/L |
| hl_games_peak | Peak Concurrent Players H/L (Phase 402) |
| hl_games_dev_lat | Studio-Breitengrad (nördlichstes Studio) H/L (Phase 402) |
| games_match_protagonist | Erkenne den Protagonisten (Phase 410) |
| games_match_pub_is_dev | Publisher = Developer? (Phase 410) |
| hl_games_howlong | Spielzeit H/L — HowLongToBeat (Phase 410) |
| games_match_esports | E-Sports-Szene? Ja/Nein (Phase 404) |
| hl_games_pegi | PEGI-Rating H/L (Phase 404) |
| hl_games_peak_year | Peak-Popularitätsjahr H/L (Phase 405) |
| hl_games_publisher_lat | Publisher-Standort: Wer liegt nördlicher? (Phase 405) |
| games_peak_year_mc | Hype-Jahr raten Multiple-Choice (Phase 405) |
| games_baujahr_mc | Erscheinungsjahr Multiple-Choice |

---

## UX-FEATURES (bereits implementiert ab Phase 408)

| Feature | Status | Beschreibung |
|---------|--------|-------------|
| Kategorie-Rückkehr nach Exit | ✅ Phase 408 | `_exitToMenu()` öffnet automatisch die Kategorie des gespielten Modus |
| "Zuletzt gespielt"-Leiste | ✅ Phase 409 | Letzte 5 Modi als Schnellstart über dem Akkordeon (`gq_recent`) |
| Gespielt-Tracking | ✅ Phase 409 | `gq_played` in localStorage — welche Modi wurden je gespielt |
| Fortschrittsbalken | ✅ Phase 409/410 | X/Y-Badge + Balken am Akkordeon-Header je Kategorie |
| Favoriten-Pin | ✅ bereits vorhanden | ❤️-Button auf jeder Karte, `showFavorites()`-Filter |
| Kategorie-Wisch-Leiste | ✅ Phase 420 | Kategorie-Nav als Carousel (`data-cat="_catnav"`), 4 Spalten × konfigurierbare Reihen (`geoquest_catnav_rows`, Standard 3), volle Namen statt Abkürzungen |
| Kompaktere Spielkarten | ✅ Phase 421 | mode-card Padding/Radius reduziert, Icon 1.25rem, Info-Button 28px (CSS in `geoquest_css.txt`) |

## SICHERHEITS-CHECKLISTE (nach Phase 401)

| Thema | Status |
|-------|--------|
| XSS: alle `q.subj` in innerHTML via `esc()` | ✅ gefixt |
| Zero-Trap: USK/pegi/sequel=0 erlaubt | ✅ gefixt |
| Biased sort() eliminiert | ✅ gefixt |
| Spread-Operator 