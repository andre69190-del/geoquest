# GeoQuest — Personalisierung: Status & Übergabe

> **Bei Session-Neustart:** zuerst `CLAUDE_SESSION_STARTER.md` lesen, dann dieses Dokument.
> Es hält den Stand der Personalisierungs-/Kinder-Features fest, damit nahtlos weitergearbeitet werden kann.
> Letztes Update: Phase 463. (Diese Zeile wird von post_phase.py automatisch gestempelt.)

## Architektur dieser Feature-Familie (wo liegt was)

Alles in `gen.py` (CSS in `geoquest_css.txt`, Übersicht in `generate_spieluebersicht.py`):

- **`CAT_META`** (direkt vor `const MODE_CATS=`): pro Kategorie `{a:[audience], i:[interests]}`.
  - audience ∈ `kids|teens|adults`; interests ∈ `geo|natur|mint|pop|kultur|sport|alltag`.
  - **Einzige Quelle** für Alters-/Interessen-Zuordnung. Neue Kategorie ⇒ hier eintragen.
- **`KIDS_CATS`** = Set aller Kategorien mit `kids` (aus CAT_META abgeleitet).
- **`_modeLevel(m)`** = Heuristik 1/2/3 (Mechanik + harte Keywords). **`_kidHidden(m)`** = KidsMode && Level≥3 → blendet schwere Modi auch in Kinder-Kategorien aus (im `catModes`-Filter).
- **Kinder-Modus:** `_getKidsMode()`/`_toggleKidsMode()` (localStorage `gq_kids_mode`), Toggle = 🧒-Button im Header.
- **Playlists/Empfehlungen:** `PLAYLISTS` (5 kuratierte), `_renderPlaylistStrip()`, `_getTopCats()` (aus `gq_played`), `_getInterestCats()` (aus `gq_interests`). „Für dich"-Leiste im Home (`#gq-playlists`).
- **Onboarding (4 Schritte):** `renderOnboarding()` step 0 Sprache, 1 „Wer spielt?" (`gq_audience`), 2 Interessen (`gq_interests`), 3 Zeit (`gq_time`). `finishOb()` speichert.
- **Übersicht:** `generate_spieluebersicht.py` zeigt 🧒-Marker + „Kindgeeignet X/999" (selbst-aktualisierend aus CAT_META + Heuristik).

## Erledigt (Phasen 452–456, alle verify 191/191, validate 0 Warnings)

| Phase | Inhalt |
|-------|--------|
| 452 | CAT_META + 4-Schritt-Onboarding + eu_plates für alle Altersstufen |
| 453 | Querformat-Notausgang („Trotzdem im Hochformat spielen") |
| 454 | **KRITISCHER FIX**: undefinierte Kinder-Modus-Funktionen ergänzt (Home crashte) + Playlists + „Für dich" |
| 455 | Spiel-Ebene-Filter (`_modeLevel`/`_kidHidden`) + Übersicht-🧒-Auswertung |
| 456 | Lehrplan-konforme Kinder-Tags (pflanzen/gartenbau/klima/fluesse/gipfel) → 410/999 kindgeeignet |
| 457 | Sticker-Sammlung (renderStickerModal, aus gq_played, Eintrag in Einstellungen) + Header-Icons app-weit auf 30px verkleinert |
| 458 | Antwort-Audit-Fix: 24 Jahr/Zahl-Modi (`_modeLevel` ID-Signale) im Kinder-Modus ausgeblendet |
| 459 | Unterwegs-Vorschlag (Geolocation, opt-in, `gq_travel_hint`, `_travelBanner`) — **Mobil-Test offen** |
| 460 | Familienduell (Hot-Seat-Rubrik, `initLV(family)`, pro Zug eigene Frage nach Spieler-Level) |
| 461 | Home-Hero: Daily voll breit, Live 1vs1 + Hot-Seat als kompaktes Paar |
| 462 | Klassenstufen (`_kidLevelMax`/`gq_kids_grade`: Kl.1-2 → Level 1, Kl.3-4 → Level 1-2) |
| 463 | Eltern-PIN (`gq_kids_pin`, `renderPinModal`, Kinder-Modus nur mit PIN abschaltbar) |

## OFFENE ROADMAP — ⚠️ = berührt Scoring/Backend, NICHT blind bauen

1. **Übungsmodus ohne Wertung** — Kinder/Casual spielen ohne Bestenlisten-Eintrag. ⚠️ Greift in `saveSession()` ein (Score+Supabase). Sauber: ein `practice`-Flag, das nur den Leaderboard-Submit überspringt (lokale Historie ok). Mit Test bauen.
2. **Getrennte Kinder-/Familien-Bestenliste** — fairste Lösung gegen „Erwachsene dominieren". ⚠️ Supabase-Schema (Leaderboard-Tabelle) ansehen + ggf. Spalte/Filter. Server-seitig, Entscheidung nötig.
3. **Adaptive Schwierigkeit** — pro Kategorie Trefferquote tracken → Level automatisch wählen. ⚠️ Muss in den Antwort-/Gameover-Fluss eingehängt werden.
4. **Casual-Schnellrunden** („2 Min" → 5 Fragen) — ⚠️ `const ROUNDS=10` steckt in `saveSession` (rounds:ROUNDS + Anti-Cheat-Cap). Variable Runden = Bestenlisten unfair. NUR als Teil des Übungsmodus (ohne Wertung) sicher.
5. **Performance / Lazy-Loading** — Daten nicht mehr komplett inline; pro Kategorie/Alter nachladen (siehe unten). Erst Lighthouse messen.
6. **Mobil-Test Unterwegs-Hinweis** (Phase 459) — auf echtem Handy im Auto/Zug prüfen.

## Performance & 1-MB-/Größen-Grenze (wichtig)

- GeoQuest.html ist ~5.8 MB Single-File (alle 74 data/*.json inline). Das skaliert nicht unendlich.
- **Empfehlung:** Größte Datenblöcke (CITIES ~306 KB, AUTOS ~196 KB, neue Extended-JSONs) NICHT mehr inline, sondern per `fetch()` laden, wenn Kategorie geöffnet wird (Muster existiert: Kennzeichen + einige Phase-28-Payloads laden bereits zur Laufzeit).
- **Alters-basiertes Nachladen:** Beim Start nur Kinder-/gewählte-Interessen-Daten laden, Rest „on demand". Spart Startup-Parse, genau dein Gedanke.
- Das ist ein eigener, größerer Umbau — am besten messen (Lighthouse Mobile) und dann gezielt die Top-3-Datenblöcke auslagern.

## Build-Hinweise für Folge-Sessions
- Bei jeder gen.py-Änderung: assert-gesicherte `.replace()` (Zero-Bug), dann `python3 gen.py && verify.py && validate_content.py && post_phase.py --phase NNN && check_session.py`.
- Sandbox-Mount kann nach Edits eine veraltete/abgeschnittene gen.py liefern; im Zweifel programmatisch (Python-Skript: lesen→assert→replace→compile→schreiben) editieren, nicht blind cp eines alten /tmp-S