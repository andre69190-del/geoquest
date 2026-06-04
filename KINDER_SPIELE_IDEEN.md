# GeoQuest — 5 Lehrplan-Spiele für die Altersstufen (Ideen / Übergabe)

> **Status:** Ideen-Phase, NOCH NICHT gebaut. Bei Neustart hier weitermachen.
> **Datum:** 2026-06-03

## Ausgangslage (geprüft)

- **Altersstufen vorhanden:** `gq_kids_grade` → Klasse 1–2 (≈ 6–8 J.) = Level-Max **1**, Klasse 3–4 (≈ 8–10 J.) = Level-Max **2**. `_modeLevel(m)` liefert 1/2/3, `_kidHidden` blendet zu schwere Modi aus.
- **24 Kinder-Kategorien** (pure_geo, ozeane, tiere, klima, map_mode, …).
- **Vorhandene Mechaniken** (wiederverwendbar): `match` (Zuordnen), `beta_hl` (Höher/Tiefer), `pin` (Karte tippen), `letter`/Wort-Schmiede, `continent`, MC-Auswahl.
- **Keine** der 5 Ideen existiert bisher als eigener Modus (geprüft) → alles neu.

## Altersstufen erweitern (Lücke 11–13 J. / Teens)

**Problem (vom Nutzer erkannt):** Heute gibt es nur Kl. 1–2 (6–8) und Kl. 3–4 (8–10) → danach gleich „Erwachsen". 11–13-Jährige können viel mehr als Grundschüler, aber noch nicht das Erwachsenen-Spezialwissen (Jahreszahlen, Metacritic, Hubraum, Börsenwerte).

**Vorschlag — dritte Stufe + mitwachsende Spiele:**

| Stufe | Alter | Klasse | Level-Max | Curriculum |
|-------|-------|--------|-----------|------------|
| 1 | 6–8 | 1–2 (KS1) | 1 | Kontinente, Ozeane, Wetter, einfache Karten |
| 2 | 8–10 | 3–4 (KS2) | 2 | Lebensräume, Kompass 8, Klimazonen, Halbkugeln |
| **3 (NEU)** | **11–13** | **5–7 (Sek. I)** | **3** | Länder eines Kontinents, Hauptstädte weltweit, Längen-/Breitengrad, Biome, Flüsse/Gebirge der Welt, Plattentektonik-Basics |
| **4 (NEU)** | **14–15** | **8–9** | **4** | vertiefte physische & menschliche Geografie, Klimadiagramme lesen, Tektonik, Bevölkerung/Wirtschaft (ohne Trivia) |
| Erwachsene | 16+ | — | alle | zusätzlich Spezial-/Trivia-Wissen (Jahreszahlen, Metacritic, Hubraum, Marktdaten) |

- **Umsetzung:** `gq_kids_grade` um `'3'` und `'4'` erweitern → `_kidLevelMax()` liefert 3 bzw. 4. `_modeLevel` von 1–3 auf **1–4** erweitern: echtes Erwachsenen-Trivia bekommt **Level 5** (über Keyword-/ID-Signale Jahr/Metacritic/…), sodass es selbst für Stufe 4 (14–15) ausgeblendet bleibt. Grade-Selektor in den Einstellungen um die zwei neuen Stufen ergänzen (i18n de/en/pl).
- **Jedes der 5 Spiele wächst mit** (gleiche Mechanik, Pool & Schwierigkeit je Stufe):
  - Kontinente → Länder eines Kontinents → Länder feiner/kleiner
  - 5 Ozeane → Meere & Meerengen → Tiefsee/Strömungen
  - bekannte Tiere → Biome/seltene Arten → Ökosystem-Zusammenhänge
  - 4 Himmelsrichtungen → 8 Richtungen → Peilung in Grad / Koordinaten
  - Halbkugeln → Klimazonen → Klimadiagramme lesen

## Lehrplan-Grundlage (international, nicht nur DE)

Abgeglichen mit Grundschul-Geografie (UK KS1/KS2, stellvertretend für viele Länder):
- **Kl. 1–2 (KS1):** 7 Kontinente & 5 Ozeane benennen, Wetter, einfache Karten lesen, physische Geländeformen (Berg, Fluss, Insel, Strand, See, Wüste), Himmelsrichtungen N/O/S/W.
- **Kl. 3–4 (KS2):** Kontinente vertiefen, Lebensräume/Habitate (Wüste, Ozean, Polar, Regenwald, Savanne, Wald), Kompass mit 8 Richtungen, Klimazonen, Nord-/Südhalbkugel, physische vs. menschliche Geografie.

**Wichtig:** Alle 5 Spiele sind länderübergreifend (kein Deutschland-Fokus) — Kontinente, Ozeane, Tiere, Geländeformen, Himmelsrichtungen und Halbkugeln gelten weltweit.

---

## Die 5 Spiele

### 1. Kontinente-Finder 🌍 — Kategorie `pure_geo` · **Level 1** (Kl. 1–2)
- **Lerninhalt (KS1):** Die 7 Kontinente benennen und auf der Weltkarte verorten.
- **Mechanik:** Karten-Tipp (`pin`/Tap) ODER Auswahl — „Tippe auf **Afrika**" auf einer einfachen Weltkarte; bzw. „Welcher Kontinent ist das?" (markierter Kontinent → 4 Namen).
- **Daten:** 7 Kontinente mit Mittelpunkt-Koordinaten/Bounding (haben wir z. T. schon).
- **Erklärung nach Antwort:** kurzer Fakt je Kontinent (größter/bevölkerungsreichster …).

### 2. Die 5 Ozeane 🌊 — Kategorie `ozeane` · **Level 1** (Kl. 1–2)
- **Lerninhalt (KS1):** Die 5 Ozeane benennen/verorten (Pazifik, Atlantik, Indik, Arktik, Südpolarmeer).
- **Mechanik:** Karten-Tipp oder Match (Ozean-Name ↔ Lage/„umspült welche Kontinente?").
- **Daten:** 5 Ozeane (Lage, angrenzende Kontinente). Sehr kompakt.
- **Erklärung:** z. B. „Der Pazifik ist der größte und tiefste Ozean."

### 3. Tiere & Lebensräume 🦁 — Kategorie `tiere` · **Level 1 → 2**
- **Lerninhalt (KS1/KS2):** Tiere ihren Lebensräumen zuordnen (Wüste, Ozean, Polar, Regenwald, Savanne, Wald, Gebirge).
- **Mechanik:** Match — „Wo lebt der **Eisbär**?" → Polar. Level 1 = bekannte Tiere (Löwe, Pinguin, Kamel), Level 2 = mehr/feiner.
- **Daten:** ~24–40 Tiere weltweit mit Habitat-Tag (international, kein DE-Bias).
- **Erklärung:** „Kamele speichern Fett im Höcker — ideal für die Wüste."

### 4. Kompass & Himmelsrichtungen 🧭 — Kategorie `map_mode` · **Level 1 (4 Richtungen) → 2 (8 Richtungen)**
- **Lerninhalt (KS1/KS2):** Himmelsrichtungen, einfache Karten-Orientierung.
- **Mechanik:** MC — „Der Pfeil zeigt nach …" (N/O/S/W); Level 2 mit NO/SO/SW/NW. Optional: „Von A nach B — welche Richtung?".
- **Daten:** rein generativ (Pfeil-Winkel → Richtung), keine Länderdaten nötig → perfekt international & spracharm.
- **Erklärung:** Merksatz „Nie Ohne Seife Waschen" / international neutral über Symbole.

### 5. Jahreszeiten & Halbkugeln ☀️❄️ — Kategorie `klima` · **Level 2** (Kl. 3–4)
- **Lerninhalt (KS2):** Wetter/Jahreszeiten, Nord- vs. Südhalbkugel (in Australien ist im Dezember Sommer!).
- **Mechanik:** MC/Match — „In **Australien** (Südhalbkugel): Welche Jahreszeit ist im **Dezember**?" → Sommer. Oder Bild/Klimazone → Jahreszeit.
- **Daten:** Liste von Ländern/Orten mit Halbkugel; Monat → Jahreszeit-Logik generativ.
- **Erklärung:** „Auf der Südhalbkugel sind die Jahreszeiten umgekehrt."

---

## Umsetzungs-Hinweise (für die Build-Phase)

- Pro Spiel: MODES-Eintrag + MODE_CATS + GEN-Dispatch + Generator (siehe Session-Starter).
- **`_modeLevel`** muss korrekt 1 bzw. 2 liefern → ggf. ID so wählen, dass die Heuristik passt, sonst explizit behandeln.
- **i18n Pflicht:** alle Prompts/Buttons über `_tc()`/`t()` in DE/EN/PL — KEINE harten deutschen Strings.
- Neue Daten als `data/*.json` + `validate_content.py`-Eintrag.
- Nach Build: `verify.py` (inkl. neuer Checks 20/21) + `validate_content.py` müssen grün sein.
- Reihenfolge-Vorschlag (einfachster zuerst): **4 (Kompass, spracharm/generativ) → 1 (Kontinente) → 2 (Ozeane) → 3 (Tiere) → 5 (Halbkugeln)**.

## Zugesagte Zusatz-Verbesserungen (vom Nutzer bestätigt)

1. **Alter im Onboarding** — Altersstufe beim ersten Start abfragen (Schritt „Wer spielt?" erweitern) → setzt `gq_kids_grade` automatisch.
2. **Lern-Erklärungen** — kurzer Fakt nach jeder Antwort + „Gelernt"-Sammlung (`gq_learned`).
3. **Themen-Fortschritt** — „Du kennst X/Y" je Thema (z. B. Kontinente), gekoppelt an Sticker.
4. **Generator-Rauchtest** — Node-Skript, das jeden GEN-Modus einmal aufruft und Abstürze/Null-Rückgaben meldet (hätte `_mkHLQ`/Pin-Bugs gefunden).

## Build-Reihenfolge (entschieden)

1. **Generator-Rauchtest** (`smoke_test.js` o. ä.) — zuerst, prüft danach jedes neue Spiel automatisch.
2. **Altersstufen 3+4** ins System (`_kidLevelMax` 1–4, `_modeLevel` Trivia→Level 5, 4-Stufen-Selektor + i18n).
3. **5 Spiele** (einfache Auswahl, mitwachsend über alle Stufen, mit Lern-Erklärung).
4. **Alter im Onboarding** + **Themen-Fortschritt**.

## Offene Entscheidungen (vor dem Bauen)

1. Alle 5 bauen oder erst 1–2 als Prototyp?
2. Bei 1 & 2: Karten-Tipp (braucht Karten-Engine) oder einfache Bild/Text-Auswahl (schneller, robuster)?
3. Tier-Liste: wie viele Tiere (Aufwand vs. Abwechslung)?
