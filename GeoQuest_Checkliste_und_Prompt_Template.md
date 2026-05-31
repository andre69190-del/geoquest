# GeoQuest — Checkliste & Prompt-Template

## Teil 1: Was muss nach jeder Phase aktualisiert werden?

### Pflicht nach jeder Phase (immer!)

**unlock_and_push.bat** — Commit-Message updaten
- Phase-Nummer, Modi-Zahl, Patch-Dateiname, verify-Ergebnis
- Beispiel: `"Content: Phase 301. Neue-Feature +3 Modi. verify: 136/136."`
- Wichtig: Datei NUR mit dem Write-Tool bearbeiten, niemals mit Linux-sed (zerstört CRLF-Zeilenenden!)

**ARCHITECTURE.md** — Mindestens diese Felder prüfen/updaten:
- `**Version:**` — Phase-Nummer und Datum
- `**Build:**` — Modi-Zahl (z.B. 718 Spielmodi)
- Patch-Tabelle am Ende des Dokuments — neue Phase eintragen mit Datum und kurzer Beschreibung
- Tiere-Modus-Tabelle falls neue tiere/pflanzen/etc. Modi hinzugekommen

**README.md** — Deploy-Datum und Phase aktualisieren:
- `Last deploy:` Zeile
- Modi-Zahl in der Beschreibung
- verify-Ergebnis

**landing.html** — Modi-Zahl in allen Vorkommnissen updaten
- Suche nach der alten Zahl (z.B. 709, 713) und ersetze durch neue
- Achtung: die Zahl kann mehrfach vorkommen (war 14×)

**GeoQuest_Website_Konzept.md** — Phase-Nummer und Modi-Zahl

**unlock_and_push.bat** ausführen und verify.py muss mit 136/136 (oder mehr) durchlaufen

**Schnellweg — alle 5 Schritte automatisch:**
```
python3 post_phase.py --phase [NR] --summary "Kurze Beschreibung"
```
Das Skript erledigt: verify → ARCHITECTURE.md → README.md → landing.html → GeoQuest_Website_Konzept.md → Commit-Message generieren.

---

### Nach größeren Inhaltserweiterungen (neue Spielmodi)

**GeoQuest_Spieluebersicht.html** — Neu generieren!
- Skript: Aus den MODES-Daten in gen.py direkt generieren
- Zeigt alle Modi gruppiert nach Kategorie mit Suche
- Aktueller Stand: 721 Modi, Phase 323

**validate_content.py** ausführen — prüft:
- JSON-Dateien auf fehlende Pflichtfelder
- Koordinaten auf Plausibilität
- WS (Wort-Schmiede) Einträge: `can_spell()` prüft ob alle Wörter buchstabierbar sind
- Muss ohne neue Fehler durchlaufen

---

### Gelegentlich prüfen (nach Gruppen-Erweiterungen)

**verify.py** — Immer ausführen nach gen.py rebuild
- Testet alle kritischen Spielmodi durch
- Muss 136/136 zeigen (oder mehr wenn neue Tests)

**MODES + MODE_CATS + GEN** — Diese drei müssen immer synchron sein!
- Neuer Modus in MODES → auch in MODE_CATS (tiere, pflanzen etc.) eintragen
- Neuer Modus in MODES → auch im GEN dispatch-table registrieren
- Neue JSON-Datei → Placeholder in gen.py anlegen UND im Build-Ablauf laden

**GEOQUEST_GAMES_REPORT.md** — Nur bei großen Dokumentationsänderungen relevant (ist historisch, zeigt Stand Phase ~99)

---

## Teil 2: Prompt-Template für neue Änderungen oder neue Spielmodi

### Vorlage — Änderungen an bestehenden Modi / Bugfixes

```
GeoQuest Phase [NUMMER]: [Kurze Beschreibung]

**Aktueller Stand:**
- Phase 323, 721 Modi, verify: 136/136
- gen.py ist die einzige Build-Quelle (Single-File-Output)
- Patch-System: patches/patch_[NUMMER]_[name].py — jeder Patch nutzt content.replace(old, new, 1)

**Zu ändernde Datei:** gen.py (via Python-Patch)

**Patch-Regeln:**
- Ankertexte EXAKT aus gen.py kopieren (repr() nutzen wenn nötig)
- gen.py speichert JavaScript-Strings mit literalen Backslash-u-Sequenzen (z.B. ü für ü, nicht das echte ü)
- Jeder Patch: patch(OLD, NEW, "Label") — meldet [OK] oder [SKIP]
- Bei [SKIP]: Anker nicht gefunden → repr() des tatsächlichen Inhalts prüfen
- Patch-Datei speichern in: patches/patch_[NR]_[name].py
- Ausführen über: python3 patches/run_patch.py patches/patch_[NR]_[name].py

**Nach dem Patch:**
1. python3 gen.py (Build)
2. python3 verify.py (136/136 prüfen)
3. python3 validate_content.py (keine neuen Fehler)
4. unlock_and_push.bat Commit-Message updaten
5. Diese Dateien updaten: ARCHITECTURE.md, README.md, landing.html, GeoQuest_Website_Konzept.md

**Was geändert werden soll:**
[Konkrete Beschreibung der Änderung]
```

---

### Vorlage — Neuen Spielmodus hinzufügen

```
GeoQuest Phase [NUMMER]: Neuer Spielmodus "[Name]"

**Aktueller Stand:**
- Phase 323, 721 Modi, verify: 136/136
- 4 Universal-Engines: genUniversalPinQ(cat), genTiereHL(cat), genTiereMatchQ(cat), initTierWortSchmiede(key)

**Neue Daten (JSON-Dateien in data/):**
- Pin-Modus: tiere_pin.json → neuer Key mit [{name, lat, lng, prompt_en}]
- H/L-Modus: tiere_hl.json → neuer Key mit [{name, value, unit, prompt_en}]
- Match-Modus: tiere_match.json → neuer Key mit [{subject, matches:[]}]  (min. 20 Items)
- WS-Modus: tiere_ws.json → neuer Key mit {word, validWords:{de:[],en:[]}}
  → WS-Wort validieren: alle Wörter müssen aus den Buchstaben des Hauptworts formierbar sein (Counter-Check)

**MODES-Eintrag (in gen.py, nach passendem Anker einfügen):**
{id:"[id]", icon:"[emoji]", title:"[Titel]", group:"tiere", prompt:"[Frage]", prompt_en:"[Question]", desc:"[Beschreibung]"}

**MODE_CATS-Eintrag:**
- Gruppe tiere: id in das tiere-Array einfügen

**GEN dispatch-Eintrag:**
- case "[id]": return genUniversalPinQ("[data-key]");
  (oder genTiereHL / genTiereMatchQ / initTierWortSchmiede je nach Typ)

**Checkliste nach Patch:**
- [ ] MODES-Eintrag vorhanden
- [ ] MODE_CATS-Eintrag vorhanden
- [ ] GEN dispatch vorhanden
- [ ] JSON-Datei hat alle Pflichtfelder
- [ ] validate_content.py ohne neue Fehler
- [ ] verify.py 136/136
- [ ] unlock_and_push.bat Commit-Message aktuell
- [ ] ARCHITECTURE.md Modi-Zahl +N
- [ ] landing.html Modi-Zahl +N
- [ ] README.md aktuell
```

---

### Vorlage — Neue Kategorie (komplett neue Datensatzgruppe)

```
GeoQuest Phase [NUMMER]: Neue Kategorie "[Kategorie-Name]"

**Aktueller Stand:** Phase 323, 721 Modi

**Schritte (analog zu Phase 228 Pflanzen / Phase 229 Gastronomie):**

1. JSON-Dateien anlegen:
   data/[cat]_pin.json, data/[cat]_hl.json, data/[cat]_match.json, data/[cat]_ws.json

2. gen.py Placeholder anlegen:
   - PLACEHOLDER_[CAT]_PIN_DATA, PLACEHOLDER_[CAT]_HL_DATA, etc.
   - Im Python-Build-Abschnitt: [CAT]_PIN_J = json.dumps(...)
   - Im JS-Replace-Abschnitt: .replace('PLACEHOLDER_[CAT]_PIN_DATA', [CAT]_PIN_J)

3. MODES-Einträge mit group:"[cat]"

4. MODE_CATS neuen Eintrag:
   {key:"[cat]", label:"[Label]", emoji:"[Emoji]", ids:[...]}

5. GEN dispatch für alle neuen IDs

6. sw.js Cache-Liste: neue JSON-Dateien automatisch durch sw.js-Generator erfasst (data/*.json)

7. validate_content.py: prüft neue Dateien automatisch wenn sie data/*.json Pfad haben

**Datenmindestanforderungen:**
- Pin: ≥10 Items mit lat/lng
- H/L: ≥10 Items mit numerischem value + unit
- Match: ≥20 Items (5 Kategorien × 4 Items)
- WS: 1 Wort + ≥10 validWords.de + ≥8 validWords.en
```

---

## Teil 3: Schnell-Referenz — Wichtige Ankerpunkte in gen.py

| Was | Wo in gen.py |
|-----|--------------|
| MODES-Array Ende (tiere) | Nach `ws_pferde_fluesterer` Eintrag |
| MODE_CATS tiere-Gruppe | Suche nach `key:"tiere"` |
| GEN dispatch | Suche nach `case "uk_tiere_` |
| syncOfflineData() | Suche nach `function syncOfflineData` |
| openFeedback() | Suche nach `function openFeedback` |
| _ttsSpeakNow() | Suche nach `function _ttsSpeakNow` |
| Home-Header (eingeloggt) | Suche nach `\u{1FA99} \${_gc}` |

## Teil 4: Dateien-Checkliste (Stand Phase 323)

| Datei | Zeigt Phasennummer? | Zeigt Modi-Zahl? | Stand |
|-------|--------------------|--------------------|-------|
| ARCHITECTURE.md | ✅ Phase 323 | ✅ 718 | aktuell |
| README.md | ✅ Phase 323 | ✅ 718 | aktuell |
| landing.html | — | ✅ 718 | aktuell |
| GeoQuest_Website_Konzept.md | ✅ Phase 323 | ✅ 718 | aktuell |
| GeoQuest_Spieluebersicht.html | ✅ Phase 323 | ✅ 718 | aktuell |
| unlock_and_push.bat | ✅ Phase 323 | ✅ 136/136 | aktuell |
| landing.html URL | — | https://geoquest-web-git-main-andre69190-7419s-projects.vercel.app/ | deploy via unlock_and_push.bat |
| GEOQUEST_GAMES_REPORT.md | ❌ Phase ~99 | ❌ 55 | historisch, nicht updaten |

---

*Zuletzt aktualisiert: Mai 2026 — Phase 323*
