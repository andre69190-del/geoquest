# GeoQuest — Personalisierung: Status & Übergabe

> **Bei Session-Neustart:** zuerst `CLAUDE_SESSION_STARTER.md` lesen, dann dieses Dokument.
> Es hält den Stand der Personalisierungs-/Kinder-Features fest, damit nahtlos weitergearbeitet werden kann.
> Letztes Update: Phase 461. (Diese Zeile wird von post_phase.py automatisch gestempelt.)

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

## OFFENE ROADMAP (priorisiert) — ⚠️ = braucht Entscheidung/Geräte-Test

1. **Familien-Duell** — mit `_modeLevel` abwechselnd leicht/schwer (fair Kind↔Erwachsen). *Engine-nah, mittel.*
4. **Klassenstufen** (Grundschule 1–2 vs 3–4) statt nur „kids" — feinere Empfehlung. *Daten+Onboarding, mittel.*
5. **Casual-Schnellrunden** („2 Min" → 5 Fragen) — ⚠️ NUR Casual/Solo, NICHT Ranked/Daily/1v1 (sonst Bestenlisten unfair, `const ROUNDS=10` ist Scoring-Kern). Vorher Round-Logik prüfen.
6. **Unterwegs-Hinweis** (Auto/Zug via Geolocation-Speed → Kennzeichen-/Waggon-Sammeln vorschlagen, einmalig, opt-in). ⚠️ Braucht Standort-Berechtigung + **Test auf echten Geräten** — nicht blind shippen.
7. **Antwort-Qualität pro Alter prüfen** — bei Kinder-Modi: sind Distraktoren altersgerecht? Ggf. mehr leichte Inhalte generieren. *Content-Audit, groß.*
8. **Performance / Lazy-Loading** — Daten nicht mehr komplett inline; pro Kategorie/Alter nachladen (siehe unten).

## Performance & 1-MB-/Größen-Grenze (wichtig)

- GeoQuest.html ist ~5.8 MB Single-File (alle 74 data/*.json inline). Das skaliert nicht unendlich.
- **Empfehlung:** Größte Datenblöcke (CITIES ~306 KB, AUTOS ~196 KB, neue Extended-JSONs) NICHT mehr inline, sondern per `fetch()` laden, wenn Kategorie geöffnet wird (Muster existiert: Kennzeichen + einige Phase-28-Payloads laden bereits zur Laufzeit).
- **Alters-basiertes Nachladen:** Beim Start nur Kinder-/gewählte-Interessen-Daten laden, Rest „on demand". Spart Startup-Parse, genau dein Gedanke.
- Das ist ein eigener, größerer Umbau — am besten messen (Lighthouse Mobile) und dann gezielt die Top-3-Datenblöcke auslagern.

## Build-Hinweise für Folge-Sessions
- Bei jeder gen.py-Änderung: assert-gesicherte `.replace()` (Zero-Bug), dann `python3 gen.py && verify.py && validate_content.py && post_phase.py --phase NNN && check_session.py`.
- Sandbox-Mount kann nach Edits eine veraltete/abgeschnittene gen.py liefern; im Zweifel programmatisch (Python-Skript: lesen→assert→replace→compile→schreiben) editieren, nicht blind cp eines alten /tmp-S