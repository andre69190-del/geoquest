# GeoQuest — System-Audit (Stand ~Phase 438)

**Datum:** 2026-06-02
**Methodik:** 9-Dimensionen-Audit gemäß Sektion „AUDIT-UMFANG" in `CLAUDE_SESSION_STARTER.md`
**Schweregrade:** 🔴 kritisch · 🟠 mittel · 🟡 niedrig · ✅ ok

> **Hinweis zum Kontext:** Während des Audits wurde das Projekt parallel aktiv weiterentwickelt
> (Modi-Zahl wechselte von 893 → 908, neue Kategorien wie Kunst/Filme/Freizeitparks).
> Die Befunde unten beziehen sich auf den Stand während des Laufs. Vor dem Anwenden von Fixes
> bitte auf einem stabilen Checkpoint erneut `verify.py` / `validate_content.py` laufen lassen.

---

## Zusammenfassung

| Dimension | Status | Kurzfassung |
|-----------|--------|-------------|
| 1 Build-Integrität | ✅ (nach Fix) | verify war 168/169 wegen veraltetem sw.js → nach `python3 gen.py` **169/169** |
| 2 Sicherheit | ✅ | kein `eval`/`new Function`; `esc()` 93×, `hasOwnProperty` 49×; keine offensichtliche XSS-Lücke |
| 3 MODES-Konsistenz | ✅ | MODES eindeutig, keine Duplikate; MODES/MODE_CATS/GEN konsistent (verify grün) |
| 4 Daten-Qualität | 🟡 | 0/0-Koordinaten in `kultur.json` & `tiere_pin.json` prüfen |
| 5 i18n | 🟠 | 13 fehlende PL-Übersetzungen (EN vorhanden) — neue Film/Künstler-Inhalte |
| 6 UX / A11y | 🟡 | sehr kleine Schriftgrößen in CSS (`.42`/`.45`/`.5`/`.52`/`.55rem`) prüfen |
| 7 Performance | 🟡 | GeoQuest.html ~5,8 MB (siehe Empfehlung) |
| 8 Doku-Sync | ✅ | post_phase pflegt alle Docs automatisch; PATCHES.md aktuell |
| 9 Toter Code | 🟡 | ungenutzte `.cat-tab`/`.tabs-nav`-CSS im `shakeCSS`-Inject (Alt-Kategorie-Nav) |

---

## 🔴→✅ D1 — Build-Integrität (behoben)

**Befund:** `verify.py` meldete **1 Fehler**:
`sw.js: 4 data files missing from ASSETS: ['kunst_extended.json','kunst_ws.json','themeparks_extended.json', …]`

**Ursache:** Neue Datendateien wurden hinzugefügt, aber die zuletzt gebaute `sw.js` (Offline-Cache-Liste) stammte von einem älteren Build und enthielt sie nicht.

**Fix (angewandt):** `python3 gen.py` neu ausgeführt → sw.js listet jetzt alle Datendateien → **verify 169/169, 0 Fehler**.

**Empfehlung:** Nach JEDEM Hinzufügen von `data/*.json` zwingend `gen.py` neu bauen (steht im Pflicht-Workflow). check_session.py fängt diesen Drift ab.

---

## 🟠 D5 — i18n: 13 fehlende PL-Übersetzungen

`validate_content.py` meldet PL-Lücken (EN vorhanden) im `_CONTENT_I18N` (Film-/Musik-Kategorie).
**Fertige DE → PL Übersetzungen zum Eintragen in `_CONTENT_I18N['pl']`:**

| Deutscher Key | EN (vorhanden) | PL (einzutragen) |
|---|---|---|
| Aus welchem Land kommt dieser Künstler/diese Band? | Which country is this artist/band from? | Z jakiego kraju pochodzi ten artysta/zespół? |
| In welchem Land wurde dieser Film hauptsächlich gedreht? | In which country was this film mainly shot? | W jakim kraju nakręcono głównie ten film? |
| Von welchem Regisseur stammt dieser Film? | Who directed this film? | Który reżyser nakręcił ten film? |
| Welcher Film erschien früher? | Which film was released earlier? | Który film ukazał się wcześniej? |
| Welcher Film hat die höhere IMDb-Bewertung? | Which film has the higher IMDb rating? | Który film ma wyższą ocenę IMDb? |
| Welcher Film hat mehr Oscars gewonnen? | Which film won more Oscars? | Który film zdobył więcej Oscarów? |
| Welcher Film hat mehr eingespielt? | Which film grossed more? | Który film zarobił więcej? |
| Welcher Film ist länger? | Which film is longer? | Który film jest dłuższy? |
| Welcher Song ist ein bekannter Hit von diesem Künstler? | Which song is a well-known hit by this artist? | Która piosenka to znany przebój tego artysty? |
| Wer gründete sich früher? | Who was founded / started earlier? | Kto powstał wcześniej? |

> Der gen.py-i18n-Check zählt 13 Lücken; 10 davon sind oben eindeutig identifiziert. Die restlichen 3
> bitte mit `validate_content.py` nach erneutem Build verifizieren (können EN-seitig fehlende Keys sein).

---

## 🟡 D4 — Daten-Qualität: 0/0-Koordinaten

`lat: 0.0` gefunden in `data/kultur.json` (mehrfach) und `data/tiere_pin.json`.
- Bei **Pin-/Karten-Modi** (z.B. `tiere_pin.json`) ist 0/0 fast sicher ein **Datenfehler** (Nullinsel im Golf von Guinea) → korrekte Koordinaten ergänzen.
- Bei `kultur.json` ggf. **gewollt** (Einträge ohne geografischen Bezug, z.B. Marken/Währungen) → prüfen, ob diese Felder dort überhaupt genutzt werden.

**Empfehlung:** `validate_content.py` um eine harte 0/0-Prüfung für Pin-Datendateien erweitern (Gatekeeper).

---

## 🟡 D6 — UX / Barrierefreiheit: zu kleine Schrift

In `geoquest_css.txt` existieren sehr kleine Schriftgrößen: `font-size:.42rem` (~6,7px), `.45rem`, `.5rem`, `.52rem`, `.55rem`, `.58rem` (3×).
Unter ~10px ist für Kinder/ältere Nutzer schwer lesbar (vgl. WCAG-Empfehlungen).
**Empfehlung:** betroffene Stellen identifizieren und auf ≥ `.62rem` anheben (analog zur Kategorie-Leiste in Phase 420). Die kleinsten (`.42`/`.45rem`) zuerst.

---

## 🟡 D7 — Performance

GeoQuest.html ~5,8 MB (Single-File, Daten inline). Über Vercel komprimiert (~1,3 MB Transfer) und per Service Worker offline gecacht — Netzwerk unkritisch. Kostenpunkt bleibt Parse/Startup auf schwachen Geräten.
**Empfehlung:** erst messen (Lighthouse, Mobile/Slow-4G). Bei Problemen Lazy-Loading der größten Datenblöcke (CITIES, AUTOS) erwägen. Nicht dringend.

---

## 🟡 D9 — Toter / redundanter Code

Im `shakeCSS`-Runtime-Inject (gen.py) stehen noch CSS-Regeln für `.cat-tab` / `.tabs-nav` — die **alte** Kategorie-Navigation, die seit Phase 420 durch das wischbare Carousel ersetzt wurde. Funktional harmlos, aber toter Ballast.
**Empfehlung:** `.cat-tab`/`.tabs-nav`-Regeln aus `shakeCSS` entfernen (die `wsShake`-Keyframes und `.tabs-mode`-Regeln dort bleiben — die werden noch gebraucht).

---

## ✅ D2 / D3 / D8 — ohne Befund

- **Sicherheit:** kein `eval`/`new Function`; `esc()` breit eingesetzt (93×); Prototype-Schutz (`hasOwnProperty` 49×). Keine offensichtliche XSS-Lücke gefunden.
- **MODES-Konsistenz:** keine doppelten Mode-IDs; MODES ↔ MODE_CATS ↔ GEN-Dispatch konsistent (verify grün).
- **Doku-Sync:** ARCHITECTURE/README/Konzept/Spielübersicht/Session-Starter werden von `post_phase.py` automatisch gepflegt; check_session.py prüft die Konsistenz.

---

## Empfohlene nächste Schritte (Priorität)

1. **(klein, sicher)** 10 PL-Übersetzungen oben eintragen, dann `validate_content.py` → die restlichen Lücken prüfen.
2. **(klein)** 0/0-Koordinaten in `tiere_pin.json` korrigieren.
3. **(klein)** Kleinste Schriftgrößen (`.42`/`.45rem`) anheben.
4. **(klein)** Toten `.cat-tab`/`.tabs-nav`-CSS aus `shakeCSS` entfernen.
5. **(optional)** Lighthouse-Messung vor Performance-Arbeiten.
