"""
Phase: 243b
Date:  2026-05-27
Author: Claude / Andre
Scope: Add 32 missing MODES entries for Astronomie, Geologie, Sport-Wissen

Description:
  Phase 243 registered 32 new modes in MODE_CATS and GEN but forgot to add
  entries to the MODES array. renderHomeTab() uses MODES.filter() to build
  the game cards inside each category accordion — without MODES entries the
  accordion opens but shows nothing (empty catModes array).

  This patch adds all 32 entries:
    - 11 Astronomie modes (uk_astro_*, hl_astro_*, ws_astro_*)
    - 11 Geologie modes   (uk_geo_*,  hl_geo_*,  ws_geo_*)
    - 10 Sport-Wissen modes (uk_sportwissen_*, hl_sportwissen_*, ws_sportwissen_*)

Dependencies: patch_243_new_worlds.py
Zero-Bug Policy: All c.replace() calls use assert c.count(old)==1
"""

import pathlib

ROOT = pathlib.Path(__file__).parent.parent
gen  = ROOT / "gen.py"
c    = gen.read_text(encoding="utf-8")

# ── Anchor: last MODES entry before closing ]; ─────────────────────────────
old = '{id:"ws_arch_radiocarbondatierung",icon:"\\u269B\\uFE0F",title:"WS: Radiocarbondatierung",group:"archaeologie",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus RADIOCARBONDATIERUNG!",desc:"Anagramm-R\\u00e4tsel \\u2014 20 Buchstaben"}'
assert c.count(old) == 1, f"Anchor not unique: {old!r}"

new_modes = """,
  /* === Phase 243b: Astronomie === */
  {id:"uk_astro_observatorien",icon:"\\u{1F52D}",title:"Observatorien-Standorte",group:"astronomie",prompt:"Wo liegt dieses Observatorium?",desc:"Berühmte Sternwarten weltweit"},
  {id:"uk_astro_startrampen",icon:"\\u{1F680}",title:"Startrampen-Standorte",group:"astronomie",prompt:"Wo befindet sich diese Startrampe?",desc:"Weltraumbahnhöfe & Raketenstarts"},
  {id:"hl_astro_planet_groesse",icon:"\\u{1FA90}",title:"H/L: Planetengröße",group:"astronomie",prompt:"Welcher Planet ist größer?",desc:"Höher/Niedriger: Durchmesser in km"},
  {id:"hl_astro_monde_anzahl",icon:"\\u{1F319}",title:"H/L: Monde-Anzahl",group:"astronomie",prompt:"Welcher Planet hat mehr Monde?",desc:"Höher/Niedriger: Anzahl bekannter Monde"},
  {id:"hl_astro_sonnenentfernung",icon:"\\u2600\\uFE0F",title:"H/L: Sonnenentfernung",group:"astronomie",prompt:"Welcher Planet ist weiter von der Sonne entfernt?",desc:"Höher/Niedriger: Entfernung in AE"},
  {id:"uk_astro_missionen",icon:"\\u{1F6F8}",title:"Raumfahrt-Missionen",group:"astronomie",prompt:"Welche Nation führte diese Mission durch?",desc:"Historische & aktuelle Raumfahrtmissionen"},
  {id:"uk_astro_planeten",icon:"\\u{1FA90}",title:"Planeten-Fakten",group:"astronomie",prompt:"Um welchen Planeten handelt es sich?",desc:"Planeten & ihre Eigenschaften"},
  {id:"uk_astro_kosmologie",icon:"\\u2728",title:"Kosmologie-Fakten",group:"astronomie",prompt:"Worum handelt es sich?",desc:"Schwarze Löcher, Nebel & Galaxien"},
  {id:"ws_astro_sternwarte",icon:"\\u{1F52D}",title:"WS: Sternwarte",group:"astronomie",noMultiplayer:true,prompt:"Bilde Wörter aus STERNWARTE!",desc:"Anagramm-Rätsel — 10 Buchstaben"},
  {id:"ws_astro_raumstation",icon:"\\u{1F6F8}",title:"WS: Raumstation",group:"astronomie",noMultiplayer:true,prompt:"Bilde Wörter aus RAUMSTATION!",desc:"Anagramm-Rätsel — 11 Buchstaben"},
  {id:"ws_astro_astronaut",icon:"\\u{1F9D1}\\u200D\\u{1F680}",title:"WS: Astronaut",group:"astronomie",noMultiplayer:true,prompt:"Bilde Wörter aus ASTRONAUT!",desc:"Anagramm-Rätsel — 9 Buchstaben"},
  /* === Phase 243b: Geologie === */
  {id:"uk_geo_vulkane",icon:"\\u{1F30B}",title:"Vulkan-Standorte",group:"geologie",prompt:"Wo liegt dieser Vulkan?",desc:"Aktive & bekannte Vulkane weltweit"},
  {id:"uk_geo_geothermal",icon:"\\u2668\\uFE0F",title:"Geothermie-Standorte",group:"geologie",prompt:"Wo liegt diese geothermische Anlage?",desc:"Geysire & Thermalquellen weltweit"},
  {id:"hl_geo_berghoehen",icon:"\\u26F0\\uFE0F",title:"H/L: Berghöhen",group:"geologie",prompt:"Welcher Berg ist höher?",desc:"Höher/Niedriger: Gipfelhöhe in Metern"},
  {id:"hl_geo_vulkan_hoehen",icon:"\\u{1F30B}",title:"H/L: Vulkanhöhen",group:"geologie",prompt:"Welcher Vulkan ist höher?",desc:"Höher/Niedriger: Höhe über dem Meeresspiegel"},
  {id:"hl_geo_erdbeben",icon:"\\u{1F30D}",title:"H/L: Erdbeben-Magnitude",group:"geologie",prompt:"Welches Erdbeben hatte eine höhere Magnitude?",desc:"Höher/Niedriger: Richterskala"},
  {id:"uk_geo_gesteinsarten",icon:"\\u{1FAA8}",title:"Gesteinsarten-Quiz",group:"geologie",prompt:"Zu welcher Gesteinsklasse gehört dieses Gestein?",desc:"Magmatit, Sedimentit oder Metamorphit?"},
  {id:"uk_geo_tektonik",icon:"\\u{1F30D}",title:"Tektonische Platten",group:"geologie",prompt:"Auf welcher Platte liegt dieser Ort?",desc:"Die Hauptplatten der Erdkruste"},
  {id:"uk_geo_mineralien",icon:"\\u{1F48E}",title:"Mineralien-Quiz",group:"geologie",prompt:"Wo wird dieses Mineral hauptsächlich abgebaut?",desc:"Seltene Erden & wichtige Rohstoffe"},
  {id:"ws_geo_stalaktiten",icon:"\\u{1FAA8}",title:"WS: Stalaktiten",group:"geologie",noMultiplayer:true,prompt:"Bilde Wörter aus STALAKTITEN!",desc:"Anagramm-Rätsel — 11 Buchstaben"},
  {id:"ws_geo_vulkanismus",icon:"\\u{1F30B}",title:"WS: Vulkanismus",group:"geologie",noMultiplayer:true,prompt:"Bilde Wörter aus VULKANISMUS!",desc:"Anagramm-Rätsel — 11 Buchstaben"},
  {id:"ws_geo_erdbeben",icon:"\\u{1F30D}",title:"WS: Erdbeben",group:"geologie",noMultiplayer:true,prompt:"Bilde Wörter aus ERDBEBEN!",desc:"Anagramm-Rätsel — 8 Buchstaben"},
  /* === Phase 243b: Sport-Wissen === */
  {id:"uk_sportwissen_olympiastadien",icon:"\\u{1F3DF}\\uFE0F",title:"Olympiastadien-Standorte",group:"sport_wissen",prompt:"Wo liegt dieses Olympiastadion?",desc:"Austragungsorte der Olympischen Spiele"},
  {id:"uk_sportwissen_marathonstrecken",icon:"\\u{1F3C3}",title:"Marathon-Standorte",group:"sport_wissen",prompt:"In welcher Stadt findet dieser Marathon statt?",desc:"Die berühmtesten Marathonläufe der Welt"},
  {id:"hl_sportwissen_marathon_alter",icon:"\\u{1F3C5}",title:"H/L: Marathon-Geschichte",group:"sport_wissen",prompt:"Welcher Marathon ist älter?",desc:"Höher/Niedriger: Gründungsjahr"},
  {id:"hl_sportwissen_stadien_kapazitaet",icon:"\\u{1F3DF}\\uFE0F",title:"H/L: Stadion-Kapazität",group:"sport_wissen",prompt:"Welches Stadion fasst mehr Zuschauer?",desc:"Höher/Niedriger: Kapazität in Personen"},
  {id:"uk_sportwissen_herkunft",icon:"\\u{1F3C6}",title:"Sportarten-Herkunft",group:"sport_wissen",prompt:"Aus welchem Land stammt dieser Sport?",desc:"Ursprungsländer bekannter Sportarten"},
  {id:"uk_sportwissen_teamgroesse",icon:"\\u{1F465}",title:"Teamgrößen-Quiz",group:"sport_wissen",prompt:"Wie viele Spieler hat ein Team dieser Sportart?",desc:"Spieleranzahl verschiedener Sportarten"},
  {id:"uk_sportwissen_olympia_standort",icon:"\\u{1F3C5}",title:"Olympia-Austragungsorte",group:"sport_wissen",prompt:"Wo fanden diese Olympischen Spiele statt?",desc:"Sommer- & Winterolympiaden weltweit"},
  {id:"ws_sportwissen_marathon",icon:"\\u{1F3C3}",title:"WS: Marathon",group:"sport_wissen",noMultiplayer:true,prompt:"Bilde Wörter aus MARATHON!",desc:"Anagramm-Rätsel — 8 Buchstaben"},
  {id:"ws_sportwissen_triathlon",icon:"\\u{1F3CA}",title:"WS: Triathlon",group:"sport_wissen",noMultiplayer:true,prompt:"Bilde Wörter aus TRIATHLON!",desc:"Anagramm-Rätsel — 9 Buchstaben"},
  {id:"ws_sportwissen_staffellauf",icon:"\\u{1F3C5}",title:"WS: Staffellauf",group:"sport_wissen",noMultiplayer:true,prompt:"Bilde Wörter aus STAFFELLAUF!",desc:"Anagramm-Rätsel — 11 Buchstaben"}"""

c = c.replace(old, old + new_modes, 1)

gen.write_text(c, encoding="utf-8")
print("patch_243b_modes_fix.py applied successfully.")
