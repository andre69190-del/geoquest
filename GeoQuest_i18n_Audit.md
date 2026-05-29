# GeoQuest — Sprach-Audit (de / en / pl)

*Stand: Phase 294 · Mai 2026 · 685 Spielmodi · 24 wählbare UI-Sprachen*

Dieses Dokument beschreibt, welche Inhalte des Spiels in **Deutsch, Englisch und Polnisch** vorliegen — und was bewusst (noch) nur auf Deutsch ist.

---

## 1. Übersetzungs-Architektur

Es gibt **drei** Übersetzungs-Ebenen:

1. **UI-Texte** — Tabelle `LANG` + Funktion `t(key)`. 24 Sprachen hinterlegt; **de/en/pl zu 100 % vollständig** (158 Schlüssel). Fehlende Schlüssel anderer Sprachen fallen auf Englisch zurück.
2. **Länder-Antworten** — über `displayCountry()` / `Intl.DisplayNames`, lokalisiert für alle 24 Sprachen (sofern als Ländercode gespeichert).
3. **Spielinhalte (Prompts, Einheiten, Antwort-Buttons)** — erweiterbare Tabelle `_CONTENT_I18N = { en:{…}, pl:{…} }` + Funktion `_tc(s)`. Bei `de` wird der Originaltext gezeigt, sonst die hinterlegte Übersetzung, sonst (Fallback) das Original. **Weitere Sprachen** lassen sich durch Ergänzen eines Sprach-Blocks (`fr:{…}`, `es:{…}` …) hinzufügen.

> Hinweis: Das im alten Checklisten-Template vorgesehene Feld `prompt_en` wurde nie im Code verdrahtet (gen.py liest es nirgends) und ist faktisch wirkungslos. Die funktionierende Mehrsprachigkeit läuft ausschließlich über `t()` (UI) und `_tc()` (Inhalte).

---

## 2. Was vollständig in de / en / pl vorliegt

| Bereich | de | en | pl | Quelle |
|---|---|---|---|---|
| Komplette Benutzeroberfläche (Menüs, Buttons, Labels) | ✅ | ✅ | ✅ | LANG / t() |
| Kern-Geografie (Stadt, Flagge, Hauptstadt, Fluss, Wahrzeichen, Park, UNESCO, citymark …) | ✅ | ✅ | ✅ | t()-Prompts + Ländercode-Antworten |
| Higher/Lower-Vergleiche (`hl_*`) | ✅ | ✅ | ✅ | t() (Phase 287) |
| Nachbarländer-Kernmodi, Karten-Kernmodi, Airport-Kernmodi (airport_pin, iata …) | ✅ | ✅ | ✅ | t() |
| Kennzeichen (`plate_*`, `de_plate`, `map_ivr`) | ✅ | ✅ | ✅ | t() (de_plate seit 287) |
| 15 zuvor hartkodierte Prompts (Währung, Stadion, Trikot, Wappen, Sport-POI …) | ✅ | ✅ | ✅ | Phase 287 |
| **Vergleiche** (`comp_*`, inkl. Flughäfen/Gipfel/Olympia) | ✅ | ✅ | ✅ | **Phase 289** |
| **HL-Beta** (`hl_b_*`, 26 Prompts) | ✅ | ✅ | ✅ | **Phase 290** |
| **Beta-Modi** (`b1…b60`, 100 MCQ + 3 HL-Prompts) | ✅ | ✅ | ✅ | **Phase 290** |
| **5 Rubriken** — E-Mobilität, Archäologie, Astronomie, Geologie, Sport-Wissen: **Frage-Prompts (196), Einheiten (54), Match-Antwort-Buttons (79)** | ✅ | ✅ | ✅ | pl: Phase 288 · en: **Phase 291** |
| **Tiere & Natur, Pflanzen & Flora, Gastronomie, Technologie & Robotik** — Prompts (162) + Einheiten (36) + fixedOpts (139) | ✅ | ✅ | ✅ | **Phase 292** |
| **Länder-Antworten in Match-Modi** (astro/geo/sport, lifestyle/airports) — saubere Ländernamen via _tcc/displayCountry | ✅ | ✅ | ✅ | **Phase 293** |
| **Saubere .c-Kategorien** — Gesteinsklassen, Kristallsysteme, Erdzeitalter, Sternenhimmel, Kontinente (101 Werte) | ✅ | ✅ | ✅ | **Phase 294** |
| Wort-Schmiede (Anagramm) | ✅ | ✅ | ✅ | de/en/es/fr/pl unterstützt |

---

## 3. Was weiterhin nur auf Deutsch ist (bewusst / offen)

| Bereich | Status | Grund |
|---|---|---|
| **Item-/Eigennamen** in allen Themenmodi (Marken, Modelle, Orte, Missionen — ~14 000) | nur DE-Form, meist sprachneutral | Eigennamen bleiben i. d. R. identisch; bewusst ausgeschlossen |
| **Match-Antwortwerte ohne fixedOpts** (außer den in P293/294 erfassten Ländern + sauberen Kategorien) — z. B. beschreibende Phrasen, Agenturen (NASA), Galaxientypen, annotierte Werte ("China (Peking)") | nur DE | offener/uneinheitlicher Wertepool |
| **`uk_*`-Themeninhalte** in Kultur & Lifestyle / Airports / Nachbarländer (Getränke, Käse, Tänze, Automarken …) | Prompts via _tc (sofern übersetzt), Antwortinhalte überwiegend DE | thematische Dateninhalte, nicht im Auftrag |
| Übrige 21 UI-Sprachen (fr, es, it, nl …) | teilweise (UI ~57–79 %), Inhalte EN-Fallback | aktuell nicht erforderlich |

---

## 4. Empfohlene nächste Schritte (optional)

1. **Tiere, Pflanzen, Gastronomie, Technologie** auf de/en/pl ziehen — analog zu den 5 erledigten Rubriken (Prompts + Einheiten + fixedOpts via `_tc`).
2. **Länder-Antwortwerte** der Match-Modi (astro/geo/sport, lifestyle/airports) über `displayCountry()` lokalisieren — finite, hochwertige Teilmenge.
3. **Kleine saubere Kategorien** (Gesteinsklassen, Kristallsysteme, Erdzeitalter, Kontinente) der `.c`-Antwortpools übersetzen.
4. Bei Bedarf **weitere UI-Sprachen** (fr/es/it …) im `_CONTENT_I18N` ergänzen — Mechanismus ist erweiterbar.

---

## 5. Relevante Patches

| Phase | Datei | Inhalt |
|---|---|---|
| 287 | patch_287_i18n_de_en_pl.py | 15 hartkodierte Prompts → t(); LANG.pl komplettiert |
| 288 | patch_288_pl_content_i18n.py | _CONTENT_I18N + _tc(); pl für 5 Rubriken |
| 289 | patch_289_comp_i18n.py | comp_* Prompts de/en/pl |
| 290 | patch_290_beta_i18n.py | HL-Beta + Beta-Prompts de/en/pl |
| 291 | patch_291_en_5cats.py | Englisch für die 5 Rubriken |
| 292 | patch_292_tpgt_i18n.py | Tiere/Pflanzen/Gastro/Tech de/en/pl |
| 293 | patch_293_country_answers.py | Länder-Antworten via _tcc/displayCountry |
| 294 | patch_294_clean_c_categories.py | Saubere .c-Kategorien (Gestein/Kristall/Erdzeitalter/Kontinente) |

*Erstellt: Mai 2026 — aktualisiert Phase 294.*
