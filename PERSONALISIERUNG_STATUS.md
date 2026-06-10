# GeoQuest — Personalisierung: Status & Übergabe

> **Bei Session-Neustart:** zuerst `CLAUDE_SESSION_STARTER.md` lesen, dann dieses Dokument.
> Es hält den Stand der Personalisierungs-/Kinder-Features fest, damit nahtlos weitergearbeitet werden kann.
> Letztes Update: Phase 531. (Diese Zeile wird von post_phase.py automatisch gestempelt.)

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

## WICHTIG: Bestenlisten & Fairness (Code-Analyse Phase 464)

- **Scores werden in Supabase-Tabelle `game_sessions` geschrieben** (`saveSession()`): Spalten user_id, mode, score, best_streak, **rounds:ROUNDS (immer 10)**, accuracy, username, device_type.
- **Die sichtbaren Bestenlisten/Liga lesen aus `leaderboard_weekly`** (server-seitig aggregiert), **IMMER `.eq("mode", mode)`** → **streng pro Spielmodus**, sortiert nach vorab berechnetem `rank`.
- **Es gibt KEINE globale/modusübergreifende Rangliste** (grep bestätigt).
- **⇒ Fazit: Bestenlisten sind bereits strukturell fair.** Man konkurriert nur mit Spielern desselben Modus + gleicher Rundenzahl (10). Kind und Erwachsener landen nie in derselben Rangliste, solange sie nicht denselben Modus spielen — und im Kinder-Modus sind schwere Modi ohnehin gefiltert.
- **⇒ Eine getrennte Kinder-Bestenliste ist NICHT nötig** (Modus-Trennung erledigt das). Nicht bauen — unnötige Komplexität/Backend-Risiko.
- **⇒ `const ROUNDS=10` NICHT variabel machen** — steckt im Score + Anti-Cheat-Cap (`_maxScore`) + `rounds`-Spalte. Variable Runden = unfaire Bestenliste. Kürzere Runden NUR im Übungsmodus (ohne Eintrag) erlaubt.
- **Übungsmodus (Phase 464):** `gq_practice`-Toggle; `saveSession()` schreibt dann nur lokale Historie und bricht VOR dem Leaderboard-Insert/Offline-Queue ab. Keine Runden-/Struktur-Änderung.

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

1. **Übungsmodus ohne Wertung** — Kinder/Casual spielen ohne Bestenlisten-E