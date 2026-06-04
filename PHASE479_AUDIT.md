# GeoQuest — Großes Audit nach Umbau (Phase 479)

**Datum:** 2026-06-03
**Anlass:** Nach umfangreichen Änderungen (Phase 467–478: Begrüßung, Handbuch, Pastell-Karten, Wisch-/Scroll-Leisten, `_goCat`-Navigation, Deploy-/Cache-Fixes, SW-Cache, Runtime-Crash-Fixes).
**Schweregrade:** 🔴 kritisch · 🟠 mittel · 🟡 niedrig · ✅ ok

## Ergebnis je Dimension

| # | Dimension | Befund | Status |
|---|-----------|--------|--------|
| 1 | **Build-Integrität** | `gen.py` baut fehlerfrei · verify **192/192** · validate **0 Warnings** · check_session grün · `GeoQuest.html == index.html` · 0 `PLACEHOLDER_`-Reste | ✅ |
| 2 | **Sicherheit** | 0× `eval(`, 0× `new Function(` · 95× `esc()` · 43× `innerHTML` (mit esc abgedeckt) · neue Modals (Handbuch) rendern nur statische LANG-Texte, kein Nutzer-Input | ✅ |
| 3 | **Runtime-Referenzen** | **5 Crashes behoben** (undefinierte `*_DATA` in Pin-Generatoren, Phase 478) · neuer verify-Check (Dim. 1) deckt die Klasse künftig ab · keine undefinierten `window.X()`-Funktionsaufrufe · alle neuen Helfer (`_goCat`,`_catTint`,`_recCat`,`renderGuideModal`) definiert | ✅ |
| 4 | **i18n** | Alle neuen Keys (`guide_*`, `ob_help_hint`) in DE/EN/PL vorhanden · `renderGuideModal` 0 hartkodierte Strings · Begrüßung/Onboarding über LANG · polnische Korruption „Gościu" repariert | ✅ |
| 5 | **Generatoren** | ~878 GEN-Dispatch-Einträge · verify MODES/Dispatch-Abgleich grün · alle 12 `genExtPinByLand`-Aufrufe referenzieren definierte Daten-Variablen | ✅ |
| 6 | **Daten** | alle 92 `data/*.json` valide | ✅ |
| 7 | **UX/Kontrast** | Pastell-Tints dezent (rgba ~0.10) über `--text2`; WCAG-Kontrast Phase 466 bereits gefixt · Recent-/Kategorie-Leisten mit weichem Auslauf + Mausrad-Scroll (Desktop) + Touch (Mobil) | ✅ |
| 8 | **Fairness** | Bestenlisten unverändert: pro Modus + feste 10 Runden, keine globale Rangliste (Analyse Phase 464) | ✅ |
| 9 | **Performance** | `GeoQuest.html` 5,9 MB · SW-Cache verschlankt (index.html-Duplikat raus, Phase 476) → kein `QuotaExceededError` mehr · vercel.json `Cache-Control` korrekt | ✅ |

## In diesem Audit gefundene & behobene Probleme

| Befund | Schweregrad | Fix |
|--------|-------------|-----|
| 5 Pin-Generatoren (Freizeitparks/Serien/Musik/Webkultur/Filme) crashten beim Start (undefinierte Daten-Variable → ReferenceError → `lq() exhausted`) | 🔴 | Phase 478: korrekte `*_EXT_DATA`/`PARKS_DATA`/`WEB_DATA`-Namen |
| Diese Fehlerklasse war für `verify.py` unsichtbar (Build/Syntax grün, Crash erst zur Laufzeit) | 🟠 | Phase 478: neuer verify-Check „Undefinierte Daten-Variablen" (Dim. 20) |
| `vercel.json` ohne Cache-Control → PWA servierte ewig alte Version | 🟠 | Phase 472: `no-cache` auf sw.js/index.html/manifest |
| SW cachte index.html + GeoQuest.html doppelt (12 MB) → Quota-Fehler | 🟠 | Phase 476: Duplikat aus Precache entfernt |
| Kategorie-Klick schien wirkungslos (scrollIntoView scrollte in PWA nicht) | 🟠 | Phase 475: `_goCat` mit `scrollTo`-Fallback + Retry |
| Kategorie-Leisten am Desktop nicht scrollbar (kein Touch, keine Scrollbar) | 🟡 | Phase 477: Mausrad→horizontal-Handler |

## Beobachtungen / offene Punkte (nicht aus diesem Umbau)

- 🟡 **i18n-Schuld im Einstellungs-Modal:** `renderSettingsModal` enthält noch hartkodierte deutsche Labels („Weitere Einstellungen", „Heimatregion", „Vorlesen (TTS)", „Hardcore-Modus" …). Vorbestehend, nicht aus diesem Umbau. Kandidat für eine separate i18n-Runde.
- 🟡 **Begrüßung `home_hi` ({name} 👋):** sehr lange Benutzernamen werden durch `nowrap` ggf. mit Ellipse gekürzt. Kosmetisch, akzeptabel.
- 🟡 **Übrige `*_pin_land`-Generatoren** (hund/boardgame/robot/eco/konsole/hw/garten): Variablen definiert; Feldnamen nicht erneut einzeln gegen die Daten geprüft (liefen vor diesem Umbau bereits). Bei Bedarf in einer Datenrunde verifizierbar.

## Fazit

Der Umbau ist stabil. Ein kritischer Laufzeit-Crash (5 Spiele) wurde gefunden und behoben, die Deploy-/Cache-Kette ist repariert, und `verify.py` fängt die ursächliche Fehlerklasse jetzt automatisch ab (192/192). Keine offenen 🔴/🟠-Punkte.
