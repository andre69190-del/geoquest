# GeoQuest - Geo-Bezug-Audit aller Spielmodi

**Datum:** 2026-06-13 | **Modi gesamt:** 1092 | **mit Geo-Bezug:** 521 | **ohne (Kandidaten):** 571

> **Methode:** Heuristik ueber Titel + Frage (DE/EN) auf Geo-Schluesselwoerter (Land, Kontinent, Stadt, Ozean, Fluss, Region, Karte, wo/woher, Herkunft, Flagge ...). Grob - der Geo-Bezug steckt manchmal im Motiv/in der Antwort statt in der Frage. Wort-/Sortierspiele mit Ortsnamen erscheinen faelschlich als 'kein Geo'.

## Kernaussage

Etwa die Haelfte der Modi stellt aktuell **keine** geografische Frage. **Die gute Nachricht:** Fast jeder zugrunde liegende Datensatz enthaelt ein Herkunfts-/Standortfeld (`land`, `ursprungsland`, `herkunftsland`, `produktionsland`, `hauptsitz_land`, `lat/lng`, `kontinent`). Damit laesst sich fuer die **grosse Mehrheit** ein Geo-Bezug ergaenzen - meist durch eine zusaetzliche Frage-Variante 'Aus welchem Land/welcher Region kommt das?'. Echt schwierig sind nur **astronomie** (Weltraum) und **medizin** (Terminologie).

## Uebersicht je Kategorie (nur Kategorien mit Nicht-Geo-Modi)

| Kategorie | Ohne Geo | Standortfeld in Daten | Urteil | Vorgeschlagener Geo-Bezug |
|---|--:|---|---|---|
| tiere | 43 | kontinent/lebensraum/nationaltier | Geo-faehig (teilw.) | "Auf welchem Kontinent/in welchem Lebensraum lebt das Tier?" statt reiner Gewicht/Tempo-Fragen |
| archaeologie | 40 | fundstaette land/lat/lng | Geo-faehig | "In welchem Land/welcher Stadt liegt diese Fundstaette?" |
| autos | 39 | marke->herkunftsland | Geo-faehig | "Aus welchem Land kommt diese Automarke?" (existiert) - auf mehr Modi ausweiten |
| emobilitaet | 39 | hauptsitz land/stadt | Geo-faehig | "Wo sitzt dieser EV-Hersteller?" / "In welcher Stadt faehrt dieser ePrix?" |
| games | 36 | publisher_land/dev_land/dev_city | Geo-faehig | "Aus welchem Land kommt der Publisher/das Studio?" (teilw. schon) |
| technologie | 35 | firmensitz (vgl. wirtschaft) | Geo-faehig (pruefen) | "Wo sitzt dieses Tech-Unternehmen?" - Datenfeld bestaetigen |
| pflanzen | 33 | ursprungsregion/heimat | Geo-faehig | "Aus welcher Region/welchem Kontinent stammt diese Pflanze?" |
| gastronomie | 33 | herkunftsland/region | Geo-faehig | "Aus welchem Land/welcher Region kommt dieses Gericht?" |
| zuege | 32 | land/strecke | Geo-faehig | "In welchem Land faehrt dieser Zug / liegt diese Strecke?" (teilw. schon) |
| astronomie | 27 | - | Schwer / nicht geo | Planeten/Sterne haben keinen Erdbezug. Hoechstens Sternwarten-Standorte. Eher als Nicht-Geo akzeptieren oder ausblenden. |
| geologie | 25 | region/platte/lat/lng | Geo-faehig (teilw.) | "Auf welcher tektonischen Platte / in welcher Region liegt das?" |
| sport_wissen | 22 | erfunden/land | Geo-faehig | "In welchem Land wurde der Sport erfunden / ist Nationalsport?" (teilw. schon) |
| hunde | 13 | ursprungsland | Geo-faehig | "Aus welchem Land kommt diese Hunderasse?" (existiert) - ausweiten |
| boardgames | 11 | ursprungsland | Geo-faehig | "Aus welchem Land stammt dieses Spiel?" |
| sport | 10 | ? | pruefen | - |
| architektur | 8 | land/lat/lng | Geo-faehig | "In welchem Land/welcher Stadt steht dieses Bauwerk?" |
| filme | 7 | drehort_land/produktionsland | Geo-faehig | "In welchem Land wurde gedreht / produziert?" |
| mythologie | 7 | herkunftsland/lat/lng | Geo-faehig | "Aus welchem Land/welcher Kultur stammt dieser Mythos?" |
| hl_compare | 6 | gemischt | Gemischt | Wie comparisons - Laender-Bezug behalten, abstrakte Groessenvergleiche pruefen. |
| comparisons | 6 | gemischt | Gemischt | Laender-Vergleiche sind geo; reine Zahl/Groessen-Vergleiche ohne Land nicht - einzeln pruefen. |
| hardware | 6 | company_land | Geo-faehig | "Aus welchem Land kommt dieser Hersteller?" |
| musik | 6 | herkunftsland | Geo-faehig | "Aus welchem Land kommt diese*r Kuenstler*in?" |
| serien | 6 | produktionsland | Geo-faehig | "Aus welchem Land kommt diese Serie?" |
| literatur | 6 | ursprungsland/lat/lng | Geo-faehig | "Aus welchem Land stammt dieser Autor?" (teilw. schon) |
| robotik | 6 | ursprungsland | Geo-faehig | "Aus welchem Land stammt dieser Roboter?" |
| medizin | 6 | lat. Begriff (kein Ort) | Schwer / nicht geo | Medizin-Terminologie hat keinen Ortsbezug. Eher als Nicht-Geo akzeptieren oder ausblenden. |
| wirtschaft | 6 | hauptsitz_land | Geo-faehig | "Wo hat dieses Unternehmen seinen Sitz?" |
| geschichte | 6 | zentrum_hauptstadt | Geo-faehig | "Wo lag das Zentrum dieser Kultur/dieses Reichs?" |
| kunst | 6 | standort_museum | Geo-faehig | "In welchem Museum/welcher Stadt haengt das Werk?" |
| gartenbau | 6 | ursprungsregion | Geo-faehig | "Aus welcher Region stammt diese Pflanze?" (existiert) |
| airports | 5 | (Geo-Kategorie) | Meist Falschtreffer | Wort-/Sortierspiele mit Ortsnamen - i.d.R. bereits geo. |
| webkultur | 5 | ursprungsland | Geo-faehig | "Aus welchem Land stammt dieser Web-Trend?" |
| pure_geo | 4 | (Geo-Kategorie) | Meist Falschtreffer | Wort-/Sortierspiele mit Ortsnamen - i.d.R. bereits geo. |
| map_mode | 4 | (Geo-Kategorie) | Meist Falschtreffer | Wort-/Sortierspiele mit Ortsnamen - i.d.R. bereits geo. |
| lifestyle | 3 | kultur/land | Geo-faehig (meist) | Brauchtum/Trachten/Begruessung an Land koppeln. |
| sprachen | 3 | ursprungsregion | Geo-faehig | "Wo wird diese Sprache gesprochen?" (teilw. schon) |
| klima | 2 | (Geo-Kategorie) | Meist Falschtreffer | Wort-/Sortierspiele mit Ortsnamen - i.d.R. bereits geo. |
| kultur | 2 | land | Geo-faehig (meist) | Bereits ueberwiegend geo. |
| themeparks | 2 | (Geo-Kategorie) | Meist Falschtreffer | Wort-/Sortierspiele mit Ortsnamen - i.d.R. bereits geo. |
| capitals | 2 | (Geo-Kategorie) | Meist Falschtreffer | Wort-/Sortierspiele mit Ortsnamen - i.d.R. bereits geo. |
| neighbors | 1 | (Geo-Kategorie) | Meist Falschtreffer | Wort-/Sortierspiele mit Ortsnamen - i.d.R. bereits geo. |
| new_modes | 1 | (Geo-Kategorie) | Meist Falschtreffer | Wort-/Sortierspiele mit Ortsnamen - i.d.R. bereits geo. |
| fluesse | 1 | (Geo-Kategorie) | Meist Falschtreffer | Wort-/Sortierspiele mit Ortsnamen - i.d.R. bereits geo. |
| nparks | 1 | (Geo-Kategorie) | Meist Falschtreffer | Wort-/Sortierspiele mit Ortsnamen - i.d.R. bereits geo. |
| inseln | 1 | (Geo-Kategorie) | Meist Falschtreffer | Wort-/Sortierspiele mit Ortsnamen - i.d.R. bereits geo. |
| gipfel | 1 | (Geo-Kategorie) | Meist Falschtreffer | Wort-/Sortierspiele mit Ortsnamen - i.d.R. bereits geo. |
| ozeane | 1 | (Geo-Kategorie) | Meist Falschtreffer | Wort-/Sortierspiele mit Ortsnamen - i.d.R. bereits geo. |

## Vollstaendige Liste aller Nicht-Geo-Modi (nach Kategorie)

### tiere (43)

- `hl_pferde_gewicht` - H/L Körpergewicht - "Welches Pferd ist schwerer?"
- `hl_pferde_speed` - H/L Galopp-Speed - "Welches Pferd ist schneller?"
- `hl_pferde_stockmass` - H/L Stockmaß - "Welches Pferd hat ein größeres Stockmaß?"
- `hl_tiere_gewicht_land` - H/L Gewicht Landtiere - "Welches Landtier ist schwerer?"
- `hl_tiere_gift` - H/L Giftigkeit - "Welches Tier ist giftiger?"
- `hl_tiere_lebenserwartung` - H/L Lebenserwartung - "Welches Tier wird älter?"
- `hl_tiere_population` - H/L Wildpopulation - "Von welchem Tier gibt es mehr Individuen?"
- `hl_tiere_schlaf` - H/L Schlafbedarf - "Welches Tier schläft länger?"
- `hl_tiere_speed_wasser` - H/L Speed: Wasser - "Welches Tier schwimmt schneller?"
- `hl_tiere_traechtigkeit` - H/L Trächtigkeit - "Welches Tier trägt länger?"
- `hl_tiere_wurf` - H/L Wurfgröße - "Welches Tier hat mehr Nachkommen?"
- `tiere_anzahl_beine` - Tiere: Wie viele Beine? - "Wie viele Beine hat dieses Tier?"
- `tiere_gross_klein` - Tiere: Größenvergleich - "Welches Tier ist größer?"
- `tiere_haustier_wild` - Haustier oder Wildtier? - "Ist das ein Haustier oder ein Wildtier?"
- `uk_pferde_fachbegriffe` - Pferde-Fachbegriffe - "Was bezeichnet dieser Fachbegriff beim Pferd?"
- `uk_pferde_reitsport` - Reitsport-Disziplinen - "Zu welcher Disziplin gehört dieser Begriff?"
- `uk_tiere_anatomie` - Skelett-Anatomie - "Welches Tier hat diese anatomische Besonderheit?"
- `uk_tiere_architekten` - Tierische Architekten - "Wer baut dieses Bauwerk?"
- `uk_tiere_arktis_antarktis` - Arktis vs. Antarktis - "Lebt dieses Tier in der Arktis oder Antarktis?"
- `uk_tiere_biolumineszenz` - Biolumineszenz - "Wer leuchtet so?"
- `uk_tiere_ernaehrung` - Ernährungstypen - "Welchem Ernährungstyp gehört dieses Tier an?"
- `uk_tiere_faehrten` - Fährten & Spuren - "Zu welchem Tier gehört diese Spur?"
- `uk_tiere_forscher_eponyme` - Forscher-Eponyme - "Nach welchem Forscher ist dieses Tier benannt?"
- `uk_tiere_laute` - Tierlaute - "Welches Tier macht diesen Laut?"
- `uk_tiere_metamorphose` - Insekten-Metamorphose - "Zu welchem Insekt wird diese Larve?"
- `uk_tiere_migranten` - Tier-Migranten - "Welche Route ist das Ziel dieses Wandertieres?"
- `uk_tiere_mimikry` - Mimikry & Doppelgänger - "Welches Tier zeigt diese Mimikry?"
- `uk_tiere_sinne` - Sinnesleistungen - "Welches Tier hat diese Sinnesfähigkeit?"
- `uk_tiere_symbiose` - Symbiosen - "Welches Tier lebt in Symbiose mit diesem?"
- `uk_tiere_tarnung` - Tarnungskünstler - "Welches Tier tarnt sich so?"
- `uk_tiere_tauchtiefe` - Tauchtiefen-Rekorde - "Welches Tier taucht so tief?"
- `ws_pferde_fluesterer` - WS: Pferdeflüsterer - "Bilde Wörter aus SHIREHORSE!"
- `ws_pferde_hufeisen` - WS: Hufeisen - "Bilde Wörter aus HUFEISEN!"
- `ws_tiere_baertierchen` - WS: Bärtierchen - "Bilde Wörter aus BAERTIERCHEN!"
- `ws_tiere_gottesanbeterin` - WS: Gottesanbeterin - "Bilde Wörter aus GOTTESANBETERIN!"
- `ws_tiere_komodowaran` - WS: Komodowaran - "Bilde Wörter aus KOMODOWARAN!"
- `ws_tiere_korallenriff` - WS: Korallenriff - "Bilde Wörter aus KORALLENRIFF!"
- `ws_tiere_lederschildkroete` - WS: Lederschildkröte - "Bilde Wörter aus LEDERSCHILDKROETE!"
- `ws_tiere_mauersegler` - WS: Mauersegler - "Bilde Wörter aus MAUERSEGLER!"
- `ws_tiere_pfeilgiftfrosch` - WS: Pfeilgiftfrosch - "Bilde Wörter aus PFEILGIFTFROSCH!"
- `ws_tiere_schnabeltier` - WS: Schnabeltier - "Bilde Wörter aus SCHNABELTIER!"
- `ws_tiere_silberruecken` - WS: Silberrücken - "Bilde Wörter aus SILBERRUECKEN!"
- `ws_tiere_wanderfalke` - WS: Wanderfalke - "Bilde Wörter aus WANDERFALKE!"

### archaeologie (40)

- `hl_arch_alter_artefakte` - H/L: Alter von Artefakten - "Welches Artefakt ist älter?"
- `hl_arch_bauzeit` - H/L: Bauzeit - "Wessen Bau dauerte länger?"
- `hl_arch_c14_alter` - H/L: C14-Alter - "Welches Objekt ist laut C14 älter?"
- `hl_arch_entdeckungsjahr` - H/L: Entdeckungsjahr - "Welche Entdeckung ist jünger?"
- `hl_arch_gewicht_megalithen` - H/L: Megalith-Gewicht - "Welcher Megalith ist schwerer?"
- `hl_arch_groesse_ruinen` - H/L: Größe von Ruinen - "Welche Ruine ist größer?"
- `hl_arch_hoehe_bauwerke` - H/L: Höhe antiker Bauwerke - "Welches Bauwerk ist höher?"
- `hl_arch_scandatenvolumen` - H/L: 3D-Scan-Daten - "Welches Scan-Projekt hat mehr Daten?"
- `hl_arch_strassenlaenge` - H/L: Antike Straßenlänge - "Welches Straßennetz ist länger?"
- `hl_arch_versicherungswert` - H/L: Artefakt-Wert - "Welches Artefakt ist wertvoller?"
- `uk_arch_3d_methoden` - 3D-Dokumentation - "Für welche Anwendung am besten?"
- `uk_arch_antike_astronomie` - Antike Astronomie - "Welcher Kultur gehört diese Beobachtung?"
- `uk_arch_antike_medizin` - Antike Medizin - "Welcher Kultur entstammt diese Praxis?"
- `uk_arch_archaeobotanik` - Archäobotanik - "Was verrät dieser Pflanzenfund?"
- `uk_arch_archaeologen` - Berühmte Archäologen - "Wer entdeckte diese Fundstätte?"
- `uk_arch_bestattungsriten` - Bestattungsräten - "Welcher Kultur gehört dieser Ritus?"
- `uk_arch_datierungsmethoden` - Datierungsmethoden - "Welche Methode passt hier?"
- `uk_arch_digifund_epochen` - Digitalprojekte nach Epoche - "Welche Epoche deckt dieses Projekt ab?"
- `uk_arch_epochen` - Artefakt-Epochen - "Welcher Epoche gehört dieses Artefakt an?"
- `uk_arch_faelschungen` - Archäologische Fälschungen - "Was behauptete diese Fälschung zu sein?"
- `uk_arch_goetter` - Antike Götter - "Zu welcher Kultur gehört diese Gottheit?"
- `uk_arch_handelsrouten` - Antike Handelsrouten - "Über welche Route kam dieses Gut?"
- `uk_arch_isotopenanalyse` - Isotopenanalyse - "Was verrät diese Analyse?"
- `uk_arch_keramikstile` - Keramikstile - "Welcher Kultur gehört dieser Stil?"
- `uk_arch_numismatik` - Antike Münzen - "Welcher Zivilisation gehört diese Münze?"
- `uk_arch_popkultur_vs_realitaet` - Popkultur vs. Realität - "Wie korrekt ist diese Darstellung?"
- `uk_arch_schatzsuche_methoden` - Surveymethoden - "Was erkennt diese Methode?"
- `uk_arch_schriften` - Antike Schriften - "Welcher Kultur entstammt diese Schrift?"
- `uk_arch_stratigraphie` - Stratigraphie-Prinzipien - "Welches Prinzip wird beschrieben?"
- `uk_arch_tempel_ordnungen` - Griechische Tempelordnungen - "Welcher Ordnung gehört dieser Tempel?"
- `uk_arch_waehrungen` - Antike Währungen - "Welcher Zivilisation gehörte diese Währung?"
- `uk_arch_werkzeuge` - Antike Werkzeuge - "Aus welcher Zeit stammt dieses Werkzeug?"
- `uk_arch_zufallsfunde` - Zufallsfunde - "Wie wurde diese Entdeckung gemacht?"
- `ws_arch_antiquitaet` - WS: Antiquität - "Bilde Wörter aus ANTIQUITAET!"
- `ws_arch_ausgrabungsstaette` - WS: Ausgrabungsstätte - "Bilde Wörter aus AUSGRABUNGSSTAETTE!"
- `ws_arch_dendrochronologie` - WS: Dendrochronologie - "Bilde Wörter aus DENDROCHRONOLOGIE!"
- `ws_arch_hieroglyphen` - WS: Hieroglyphen - "Bilde Wörter aus HIEROGLYPHEN!"
- `ws_arch_photogrammetrie` - WS: Photogrammetrie - "Bilde Wörter aus PHOTOGRAMMETRIE!"
- `ws_arch_radiocarbondatierung` - WS: Radiocarbondatierung - "Bilde Wörter aus RADIOCARBONDATIERUNG!"
- `ws_arch_stratigraphie` - WS: Stratigraphie - "Bilde Wörter aus STRATIGRAPHIE!"

### autos (39)

- `auto_baujahr_mc` - Auto-Quiz: Baujahr-Raten - "In welchem Jahr kam dieses Modell auf den Markt?"
- `auto_generationen_match` - Modell-Generationen-Match - "Wann erschien dieses Modell der Modellreihe?"
- `auto_match_antrieb` - Auto-Quiz: Antriebskonzept - "Welches Antriebskonzept hat dieses Fahrzeug?"
- `auto_match_antriebsart` - Auto-Quiz: Antriebsart - "Womit wird dieses Fahrzeug angetrieben?"
- `auto_match_getriebe` - Auto-Quiz: Getriebe - "Welches Getriebe hat dieses Fahrzeug?"
- `auto_match_karosserie` - Auto-Quiz: Karosserieform - "Welche Karosserieform hat dieses Fahrzeug?"
- `auto_match_konzern` - Auto-Quiz: Konzern - "Zu welchem Konzern gehörte dieses Fahrzeug bei Produktion?"
- `auto_match_motorbauart` - Auto-Quiz: Motorbauart - "Welche Motorbauart hat dieses Fahrzeug?"
- `auto_match_sitze` - Auto-Quiz: Sitzplätze - "Wie viele Sitzplätze hat dieses Fahrzeug?"
- `auto_match_turbo` - Auto-Quiz: Aufladung - "Hat dieses Fahrzeug einen Turbo oder Kompressor ab Werk?"
- `fahrzeug_match_karosserie` - Auto: Welcher Typ? - "Was für ein Fahrzeugtyp ist das?"
- `fahrzeug_match_konzern` - Auto: Welcher Konzern? - "Von welchem Konzern kommt dieses Auto?"
- `fahrzeug_match_sitze` - Wie viele Sitze hat dieses Auto? - "Wie viele Sitzplätze hat dieses Fahrzeug?"
- `hl_auto_accel` - Auto-Quartett: 0-100 km/h - "Welches Fahrzeug braucht Länger auf 100?"
- `hl_auto_akku` - Auto-Quartett: Batterie - "Welche EV-Batterie ist größer?"
- `hl_auto_baujahr_ende` - Auto-Quartett: Produktionsende - "Welches Auto wurde später eingestellt?"
- `hl_auto_bj` - Auto-Quartett: Baujahr - "Welches Fahrzeug wurde SPÄTER gebaut?"
- `hl_auto_ccm` - Auto-Quartett: Hubraum - "Welcher Verbrenner hat mehr Hubraum?"
- `hl_auto_co2` - Auto-Quartett: CO₂-Ausstoß - "Welches Fahrzeug stößt mehr CO₂ aus?"
- `hl_auto_cw` - Auto-Quartett: Aerodynamik - "Welches ist aerodynamischer (cw)?"
- `hl_auto_drehmoment` - Auto-Quartett: Drehmoment - "Welches hat mehr Drehmoment?"
- `hl_auto_gewicht` - Auto-Quartett: Gewicht - "Welches Fahrzeug ist schwerer?"
- `hl_auto_kofferraum` - Auto-Quartett: Kofferraum - "Welches hat mehr Kofferraum?"
- `hl_auto_laenge` - Auto-Quartett: Länge - "Welches Fahrzeug ist länger?"
- `hl_auto_neupreis` - Auto-Quartett: Neupreis - "Welches war bei Einführung teurer?"
- `hl_auto_nordschleife` - Auto-Quartett: Nordschleife - "Wer war schneller auf der Nürburgring-Nordschleife?"
- `hl_auto_ps` - Auto-Quartett: Leistung - "Welches Fahrzeug hat mehr PS?"
- `hl_auto_ps_kg` - Auto-Quartett: Leistungsgewicht - "Welches hat das bessere Leistungsgewicht (PS/kg)?"
- `hl_auto_reichweite` - Auto-Quartett: EV-Reichweite - "Welches EV hat mehr Reichweite?"
- `hl_auto_tank` - Auto-Quartett: Tank - "Welches hat mehr Tankvolumen?"
- `hl_auto_verbrauch_e` - Auto-Quartett: Verbrauch kWh - "Welches EV verbraucht WENIGER Strom?"
- `hl_auto_verbrauch_l` - Auto-Quartett: Verbrauch L - "Welcher Verbrenner verbraucht WENIGER?"
- `hl_auto_vmax` - Auto-Quartett: Top-Speed - "Welches Fahrzeug ist schneller?"
- `hl_auto_wendekreis` - Auto-Quartett: Wendekreis - "Welches Auto hat den kleineren Wendekreis?"
- `hl_auto_zuladung` - Auto-Quartett: Nutzlast - "Welches Auto darf mehr zuladen?"
- `hl_auto_zylinder` - Auto-Quartett: Zylinder - "Welches hat mehr Zylinder?"
- `hl_fahrzeug_gewicht` - Autos: Welches ist schwerer? - "Welches Auto ist schwerer?"
- `hl_fahrzeug_kofferraum` - Autos: Mehr Kofferraum? - "Welches Auto hat mehr Kofferraum?"
- `timeline_auto_bj` - Timeline: Auto-Evolution - "Sortiere die Autos nach Baujahr (ältestes zuerst)!"

### emobilitaet (39)

- `hl_emob_0_100` - E-Mob: 0–100 km/h - "Welches EV beschleunigt schneller auf 100?"
- `hl_emob_cw_wert` - E-Mob: cw-Wert - "Welches Fahrzeug hat einen niedrigeren Luftwiderstand?"
- `hl_emob_drehmoment` - E-Mob: Drehmoment - "Welches EV hat mehr Systemdrehmoment?"
- `hl_emob_gewicht` - E-Mob: Fahrzeuggewicht - "Welches EV ist schwerer?"
- `hl_emob_kapazitaet` - E-Mob: Batteriekapazitaet - "Welches EV hat eine groessere Batteriekapazitaet?"
- `hl_emob_ladeanschluesse` - E-Mob: Ladeanschluesse - "Welches EV hat mehr Ladeanschluesse?"
- `hl_emob_ladeleistung` - E-Mob: Ladeleistung - "Welches EV laedt mit hoeherer Maximalleistung?"
- `hl_emob_ladezeit_10_80` - E-Mob: Ladezeit 10–80% - "Bei welchem EV dauert das Laden von 10–80% kuerzer?"
- `hl_emob_preis` - E-Mob: Basispreis - "Welches EV ist teurer?"
- `hl_emob_systemspannung` - E-Mob: Systemspannung - "Welches EV arbeitet mit hoeherer Systemspannung?"
- `hl_emob_wltp` - E-Mob: WLTP-Reichweite - "Welches EV hat eine groessere WLTP-Reichweite?"
- `hl_emob_zell_anzahl` - E-Mob: Zellenanzahl - "Welches EV hat mehr Batteriezellen?"
- `uk_emob_akronyme` - E-Mob: Akronyme - "Wofuer steht dieses E-Mobilitaets-Akronym?"
- `uk_emob_avas` - E-Mob: AVAS-Vorschriften - "Was schreibt die AVAS-Vorschrift hier vor?"
- `uk_emob_bidirektional` - E-Mob: V2X-Technologie - "Welche V2X-Technologie beschreibt diese Interaktion?"
- `uk_emob_etikette` - E-Mob: Ladetikette - "Welche Verhaltensregel passt zu dieser Ladesituation?"
- `uk_emob_ev_reifen` - E-Mob: EV-Reifen - "Welchen Vorteil bietet dieses EV-Reifenmerkmal?"
- `uk_emob_konzeptautos` - E-Mob: Konzeptfahrzeuge - "Von welchem Hersteller stammt dieses EV-Konzept?"
- `uk_emob_ladekurven` - E-Mob: Ladekurven - "Welches Fahrzeug zeigt dieses Ladeverhalten?"
- `uk_emob_level_autonomy` - E-Mob: Autonomiegrade - "Welchem SAE-Autonomiegrad entspricht diese Funktion?"
- `uk_emob_motorentypen` - E-Mob: Motorentypen - "Auf welcher Technologie basiert dieser Elektromotor?"
- `uk_emob_plattformen` - E-Mob: EV-Plattformen - "Auf welcher Plattform basiert dieses EV-Modell?"
- `uk_emob_reichweiten_killer` - E-Mob: Reichweiten-Killer - "Welcher Faktor reduziert die EV-Reichweite hier?"
- `uk_emob_roaming` - E-Mob: Lade-Roaming - "Mit welchem Partner kann dieses Ladenetzwerk roamen?"
- `uk_emob_smart_home` - E-Mob: EV & Smart Home - "Welches Protokoll ermoeglicht diese EV-Smart-Home-Funktion?"
- `uk_emob_stecker` - E-Mob: Ladestecker - "Welchem Ladestandard entspricht dieser Stecker?"
- `uk_emob_thermomanagement` - E-Mob: Thermomanagement - "Welche Funktion uebernimmt diese TMS-Komponente?"
- `uk_emob_warnleuchten` - E-Mob: Warnleuchten - "Was bedeutet diese EV-Warnanzeige?"
- `uk_emob_zellchemie` - E-Mob: Zellchemie - "Welcher Vorteil ist typisch fuer diese Batteriechemie?"
- `ws_emob_batteriemanagement` - WS: Batteriemanagement - "Bilde Wörter aus BATTERIEMANAGEMENT!"
- `ws_emob_bidirektionalladen` - WS: Bidirektionalladen - "Bilde Wörter aus BIDIREKTIONALLADEN!"
- `ws_emob_bordnetzspannung` - WS: Bordnetzspannung - "Bilde Wörter aus BORDNETZSPANNUNG!"
- `ws_emob_elektroantrieb` - WS: Elektroantrieb - "Bilde Wörter aus ELEKTROANTRIEB!"
- `ws_emob_fahrassistenzsystem` - WS: Fahrassistenzsystem - "Bilde Wörter aus FAHRASSISTENZSYSTEM!"
- `ws_emob_gleichstromladen` - WS: Gleichstromladen - "Bilde Wörter aus GLEICHSTROMLADEN!"
- `ws_emob_reichweitenangst` - WS: Reichweitenangst - "Bilde Wörter aus REICHWEITENANGST!"
- `ws_emob_rekuperation` - WS: Rekuperation - "Bilde Wörter aus REKUPERATION!"
- `ws_emob_schnellladestation` - WS: Schnellladestation - "Bilde Wörter aus SCHNELLLADESTATION!"
- `ws_emob_wechselstromladen` - WS: Wechselstromladen - "Bilde Wörter aus WECHSELSTROMLADEN!"

### games (36)

- `digital_match_f2p` - Free-to-Play? - "Ist dieses Spiel kostenlos spielbar?"
- `digital_match_genre` - Spiel: Welches Genre? - "Welchem Genre gehört dieses Spiel an?"
- `digital_match_plattform` - Spiel: PC, Konsole oder Mobil? - "Auf welcher Plattform erschien dieses Spiel?"
- `games_baujahr_mc` - Gaming: Erscheinungsjahr raten - "In welchem Jahr erschien dieses Spiel erstmals?"
- `games_match_adaption` - Game-Verfilmung - "Wurde dieses Spiel verfilmt oder als Serie adaptiert?"
- `games_match_esports` - E-Sports-Szene? - "Hat dieses Spiel eine aktive E-Sports-Szene?"
- `games_match_f2p` - F2P oder Kaufspiel? - "Ist dieses Spiel kostenlos spielbar?"
- `games_match_genre` - Spielgenre zuordnen - "Welchem Genre gehört dieses Spiel an?"
- `games_match_kategorie` - Gaming-Ära - "Zu welcher Gaming-Kategorie gehört dieses Spiel?"
- `games_match_plattform` - Spielplattform - "Für welche Plattform erschien dieses Spiel primär?"
- `games_match_protagonist` - Protagonist-Match - "Zu welchem Spiel gehört dieser Protagonist?"
- `games_match_pub_is_dev` - Publisher = Developer? - "Ist der Publisher dieses Spiels auch der Entwickler?"
- `games_match_publisher` - Game-Publisher - "Welcher Publisher steckt hinter diesem Spiel?"
- `hl_digital_downloads` - Welches Spiel wurde öfter heruntergeladen? - "Welches Spiel hat mehr Downloads?"
- `hl_digital_vk` - Mehr Verkäufe? - "Mehr Verkäufe?"
- `hl_games_downloads` - Game-Quartett: Downloads - "Welches F2P-Spiel wurde öfter heruntergeladen?"
- `hl_games_howlong` - Game-Quartett: Spielzeit - "Welches Spiel hat die längere Hauptstory?"
- `hl_games_metacritic` - Game-Quartett: Metacritic - "Welches Spiel wurde von Kritikern besser bewertet?"
- `hl_games_pegi` - Game-Quartett: PEGI-Rating - "Welches Spiel hat eine höhere PEGI-Altersfreigabe?"
- `hl_games_release` - Game-Quartett: Erscheinungsjahr - "Welches Spiel erschien später?"
- `hl_games_sequel` - Game-Quartett: Teile-Anzahl - "Welche Spielserie hat mehr direkte Nachfolger?"
- `hl_games_usk` - Game-Quartett: Altersfreigabe USK - "Welches Spiel hat eine höhere USK-Freigabe?"
- `hl_games_vk` - Game-Quartett: Verkaufszahlen - "Welches Spiel wurde häufiger verkauft?"
- `hl_konsolen_cpu` - Konsolen-Quartett: CPU - "Welche Konsole hat den schnelleren Prozessor?"
- `hl_konsolen_eingestellt` - Konsolen-Quartett: Produktionsende - "Welche Konsole wurde später eingestellt?"
- `hl_konsolen_erscheinungsjahr` - Konsolen-Quartett: Erscheinungsjahr - "Welche Konsole erschien später?"
- `hl_konsolen_preis` - Konsolen-Quartett: Preis - "Welche Konsole war beim Launch teurer?"
- `hl_konsolen_ram` - Konsolen-Quartett: RAM - "Welche Konsole hat mehr Arbeitsspeicher?"
- `hl_konsolen_verkauf` - Konsolen-Quartett: Absatz - "Welche Konsole hat mehr Einheiten verkauft?"
- `konsolen_match_aufloesung` - Konsolen-Quiz: Auflösung - "Welche maximale Auflösung unterstützt diese Konsole?"
- `konsolen_match_spiel` - Konsolen-Quiz: Welche Konsole? - "Für welche Konsole ist dieses Spiel bekannt?"
- `match_konsolen_generation` - Konsole: Generation - "Welcher Konsolengeneration gehört dieses Modell an?"
- `match_konsolen_handheld` - Konsole: Handheld? - "Heimkonsole oder Handheld?"
- `match_konsolen_hersteller` - Konsole: Hersteller - "Welches Unternehmen hat diese Konsole hergestellt?"
- `match_konsolen_medium` - Konsole: Speichermedium - "Welches Medium nutzt diese Konsole?"
- `timeline_konsolen_bj` - Hardware-Timeline - "Sortiere die Konsolen nach Erscheinungsjahr!"

### technologie (35)

- `hl_tech_code_zeilen` - Tech: Codezeilen - "Welches Projekt hat mehr Codezeilen?"
- `hl_tech_freiheitsgrade` - Tech: Freiheitsgrade - "Welcher Roboter hat mehr Freiheitsgrade?"
- `hl_tech_rechenleistung` - Tech: Rechenleistung - "Welche GPU hat mehr Rechenleistung?"
- `hl_tech_release_jahr` - Tech: Release-Jahr - "Welche Sprache wurde frueher veroeffentlicht?"
- `hl_tech_taktfrequenz` - Tech: Taktfrequenz - "Welche CPU hat eine hoehere Taktfrequenz?"
- `hl_tech_tdp` - Tech: TDP-Wert - "Welche CPU/GPU hat einen hoeheren TDP?"
- `hl_tech_transistoren` - Tech: Transistorenanzahl - "Welcher Chip hat mehr Transistoren?"
- `timeline_tech_release` - Tech-Zeitleiste - "Ordne die Technologien nach Release-Jahr!"
- `uk_tech_akronyme` - Tech: Akronyme - "Wofuer steht dieses Technik-Akronym?"
- `uk_tech_bigo` - Tech: Big-O - "Welche Big-O-Komplexitaet hat dieser Algorithmus?"
- `uk_tech_dateiendungen` - Tech: Dateiendungen - "Zu welcher Dateiart gehoert diese Endung?"
- `uk_tech_erfinder` - Tech: Technik-Erfinder - "Wer hat diese Technologie erfunden?"
- `uk_tech_erste_videospiele` - Tech: Erste Videospiele - "In welchem Jahrzehnt erschien dieses Spiel?"
- `uk_tech_hardware` - Tech: Hardware-Komponenten - "Zu welchem Computersystem gehoert diese Komponente?"
- `uk_tech_http` - Tech: HTTP-Statuscodes - "Zu welcher Kategorie gehoert dieser HTTP-Code?"
- `uk_tech_linux` - Tech: Linux-Distros - "Fuer welchen Einsatz ist diese Distro bekannt?"
- `uk_tech_malware` - Tech: Malware-Typen - "Zu welcher Malware-Kategorie gehoert das?"
- `uk_tech_osi` - Tech: OSI-Modell - "Auf welchem OSI-Layer arbeitet dieses Protokoll?"
- `uk_tech_portnummern` - Tech: Portnummern - "Welcher Dienst nutzt diese Portnummer?"
- `uk_tech_sensoren` - Tech: Sensoren - "Was misst dieser Sensor?"
- `uk_tech_smart_home` - Tech: Smart Home - "Zu welchem Smart-Home-System gehoert das?"
- `uk_tech_syntax` - Tech: Code-Syntax - "In welcher Programmiersprache wird das verwendet?"
- `uk_tech_tech_ma` - Tech: Uebernahmen - "Von wem wurde dieses Unternehmen uebernommen?"
- `uk_tech_turing_award` - Tech: Turing Award - "Wofuer erhielt diese Person den Turing Award?"
- `uk_tech_wahrheitstabellen` - Tech: Logikgatter - "Welches Logikgatter erzeugt diesen Ausgang?"
- `ws_tech_algorithmus` - WS: Algorithmus - "Bilde Wörter aus ALGORITHMUS!"
- `ws_tech_betriebssystem` - WS: Betriebssystem - "Bilde Wörter aus BETRIEBSSYSTEM!"
- `ws_tech_compilerbau` - WS: Compilerbau - "Bilde Wörter aus COMPILERBAU!"
- `ws_tech_cybersicherheit` - WS: Cybersicherheit - "Bilde Wörter aus CYBERSICHERHEIT!"
- `ws_tech_datenbankmanagement` - WS: Datenbankmanagement - "Bilde Wörter aus DATENBANKMANAGEMENT!"
- `ws_tech_grafikprozessor` - WS: Grafikprozessor - "Bilde Wörter aus GRAFIKPROZESSOR!"
- `ws_tech_mikrocontroller` - WS: Mikrocontroller - "Bilde Wörter aus MIKROCONTROLLER!"
- `ws_tech_prozessorarchitektur` - WS: Prozessorarchitektur - "Bilde Wörter aus PROZESSORARCHITEKTUR!"
- `ws_tech_quantencomputer` - WS: Quantencomputer - "Bilde Wörter aus QUANTENCOMPUTER!"
- `ws_tech_softwareentwicklung` - WS: Softwareentwicklung - "Bilde Wörter aus SOFTWAREENTWICKLUNG!"

### pflanzen (33)

- `hl_pflanzen_alter` - H/L Baumalter - "Welcher Baum wird älter?"
- `hl_pflanzen_blattflaeche` - H/L Blattfläche - "Welches Blatt hat die größere Fläche?"
- `hl_pflanzen_bluehdauer` - H/L Blühtdauer - "Welche Pflanze blüht länger pro Jahr?"
- `hl_pflanzen_fruchtgewicht` - H/L Fruchtgewicht - "Welche Frucht ist schwerer?"
- `hl_pflanzen_genomgroesse` - H/L Genomgröße - "Welche Pflanze hat das größere Genom?"
- `hl_pflanzen_samenlaenge` - H/L Samengröße - "Welcher Samen ist länger?"
- `hl_pflanzen_stammumfang` - H/L Stammumfang - "Welcher Baum hat den größeren Stammumfang?"
- `hl_pflanzen_wuchshoehe` - H/L Wuchshöhe - "Welcher Baum wird höher?"
- `pflanze_baum_blume` - Baum, Blume oder Strauch? - "Was ist das?"
- `pflanze_essbar` - Essbar oder giftig? - "Ist diese Pflanze essbar?"
- `pflanze_farbe` - Welche Farbe hat diese Blume? - "Welche Farbe hat diese Blüte?"
- `pflanze_obst_gemuese` - Obst oder Gemüse? - "Ist das Obst oder Gemüse?"
- `uk_pflanzen_baum_des_jahres` - Baum des Jahres - "In welchem Jahr war dieser Baum "Baum des Jahres"?"
- `uk_pflanzen_bestuaeber` - Bestäuber - "Wer bestäubt diese Blume hauptsächlich?"
- `uk_pflanzen_blattform` - Blattformen - "Welche Blattform hat diese Pflanze?"
- `uk_pflanzen_bluetezeit` - Blütezeit - "In welcher Jahreszeit blüht diese Pflanze?"
- `uk_pflanzen_familien` - Pflanzenfamilien - "Zu welcher Familie gehört diese Art?"
- `uk_pflanzen_fruchttyp` - Fruchttypen - "Zu welchem Fruchttyp gehört diese Frucht?"
- `uk_pflanzen_giftpflanze_jahres` - Giftpflanze des Jahres - "In welchem Jahr war dies die Giftpflanze des Jahres?"
- `uk_pflanzen_giftstoffe` - Giftstoffe - "Welcher Wirkstoff macht diese Pflanze giftig?"
- `uk_pflanzen_lebensraum` - Pflanzen-Lebensraum - "In welchem Lebensraum wächst diese Pflanze?"
- `uk_pflanzen_nutzung` - Pflanzennutzung - "Wofür wird diese Pflanze hauptsächlich genutzt?"
- `uk_pflanzen_scheinfruchte` - Scheinfrüchte - "Wie klassifiziert die Botanik diese Frucht?"
- `uk_pflanzen_vermehrung` - Vermehrungsarten - "Wie vermehrt sich diese Pflanze hauptsächlich?"
- `ws_pflanzen_ginkgobaum` - WS: Ginkgobaum - "Bilde Wörter aus GINKGOBAUM!"
- `ws_pflanzen_kaffeebohne` - WS: Kaffeebohne - "Bilde Wörter aus KAFFEEBOHNE!"
- `ws_pflanzen_nachtschatten` - WS: Nachtschatten - "Bilde Wörter aus NACHTSCHATTEN!"
- `ws_pflanzen_pusteblume` - WS: Pusteblume - "Bilde Wörter aus PUSTEBLUME!"
- `ws_pflanzen_rhododendron` - WS: Rhododendron - "Bilde Wörter aus RHODODENDRON!"
- `ws_pflanzen_sonnenblume` - WS: Sonnenblume - "Bilde Wörter aus SONNENBLUME!"
- `ws_pflanzen_trauerweide` - WS: Trauerweide - "Bilde Wörter aus TRAUERWEIDE!"
- `ws_pflanzen_vergissmeinnicht` - WS: Vergissmeinnicht - "Bilde Wörter aus VERGISSMEINNICHT!"
- `ws_pflanzen_weihnachtsstern` - WS: Weihnachtsstern - "Bilde Wörter aus WEIHNACHTSSTERN!"

### gastronomie (33)

- `hl_gastro_alkoholgehalt` - HL: Alkoholgehalt - "Welches Getränk hat mehr Alkohol?"
- `hl_gastro_backtemperatur` - HL: Backtemperatur - "Bei welcher Temperatur wird das gebacken?"
- `hl_gastro_fermentationsdauer` - HL: Fermentationsdauer - "Welches Produkt fermentiert länger?"
- `hl_gastro_haltbarkeit` - HL: Haltbarkeit - "Welches Lebensmittel hält sich länger?"
- `hl_gastro_kalorien` - HL: Kalorien - "Welches Gericht hat mehr Kalorien pro 100g?"
- `hl_gastro_kerntemperatur` - HL: Kerntemperatur - "Welches Fleisch benötigt eine höhere Kerntemperatur?"
- `hl_gastro_preis_kg` - HL: Preis pro Kilo - "Was kostet mehr pro Kilogramm?"
- `hl_gastro_prokopf_verbrauch` - HL: Pro-Kopf-Verbrauch - "Welches Nahrungsmittel wird pro Kopf mehr gegessen?"
- `hl_gastro_rezept_alter` - HL: Rezept-Alter - "Welches Rezept ist älter?"
- `hl_gastro_schmelzpunkt` - HL: Schmelzpunkt - "Welches Produkt hat einen höheren Schmelzpunkt?"
- `hl_gastro_scoville` - HL: Scoville-Skala - "Welche Chilischote ist schärfer?"
- `hl_gastro_wasseranteil` - HL: Wasseranteil - "Welches Lebensmittel enthält mehr Wasser?"
- `hl_gastro_zubereitungszeit` - HL: Zubereitungszeit - "Welches Gericht dauert länger?"
- `hl_gastro_zutaten_anzahl` - HL: Zutaten-Anzahl - "Welches Rezept hat mehr Zutaten?"
- `uk_gastro_bakterien_pilze` - Mikroorganismen & Fermentation - "Bei welchem Produkt ist dieser Mikroorganismus beteiligt?"
- `uk_gastro_fachbegriffe_herd` - Kochfachbegriffe - "Welcher Kochtechnik-Kategorie gehört dieser Begriff an?"
- `uk_gastro_film_food` - Essen im Film - "Zu welchem Franchise gehört dieses ikonische Filmessen?"
- `uk_gastro_fleisch_cuts` - Fleischzuschnitte - "Von welchem Tier stammt dieser Fleischzuschnitt?"
- `uk_gastro_gewuerzmischungen` - Gewürzmischungen - "Welcher Küche gehört diese Gewürzmischung an?"
- `uk_gastro_kaffeespezialitaeten` - Kaffeespezialitäten - "Auf welcher Basis basiert dieser Kaffeedrink?"
- `uk_gastro_kuechengeraete` - Küchengeräte sortieren - "Welcher Kategorie gehört dieses Küchengerät an?"
- `uk_gastro_pasta_formen` - Pasta & Saucen - "Mit welcher Sauce wird diese Pasta kombiniert?"
- `uk_gastro_schnitttechniken` - Schnitttechniken - "Für welche Lebensmittelgruppe wird diese Technik genutzt?"
- `uk_gastro_sushi_arten` - Sushi-Stile - "Welcher Sushi-Stil beschreibt diese Form?"
- `uk_gastro_tabus` - Nahrungstabus - "Welcher Religion ist dieses Nahrungstabu zugeordnet?"
- `uk_gastro_vegan_alternativen` - Vegane Alternativen - "Was ersetzt dieses vegane Produkt?"
- `ws_gastro_fermentation` - WS: Fermentation - "Bilde Wörter aus FERMENTATION!"
- `ws_gastro_kaltentsafter` - WS: Kaltentsafter - "Bilde Wörter aus KALTENTSAFTER!"
- `ws_gastro_kuechenmaschine` - WS: Küchenmaschine - "Bilde Wörter aus KUECHENMASCHINE!"
- `ws_gastro_sauerteigbrot` - WS: Sauerteigbrot - "Bilde Wörter aus SAUERTEIGBROT!"
- `ws_gastro_schwarzwaelder` - WS: Schwarzwälder - "Bilde Wörter aus SCHWARZWAELDER!"
- `ws_gastro_wurzelgemuese` - WS: Wurzelgemüse - "Bilde Wörter aus WURZELGEMUESE!"
- `ws_gastro_zitruspresse` - WS: Zitruspresse - "Bilde Wörter aus ZITRUSPRESSE!"

### zuege (32)

- `hl_schienen_dauer` - Welche Fahrt dauert länger? - "Welche Zugfahrt dauert länger?"
- `hl_schienen_tempo` - Welcher Zug ist schneller? - "Welcher Zug fährt schneller?"
- `hl_zug_jahr` - H/L: Bahn-Geschichte - "Früher in Betrieb genommen?"
- `hl_zug_km` - H/L: Streckenkil. Fernzug - "Längere Strecke?"
- `hl_zug_speed` - H/L: Zuggeschwindigkeit - "Höhere Betriebsgeschwindigkeit?"
- `hl_zug_taktfrequenz` - H/L: Taktfrequenz - "Höhere Taktfrequenz (Züge/Stunde)?"
- `schienen_match_antrieb` - Elektro oder Diesel? - "Womit fährt dieser Zug?"
- `schienen_match_typ` - ICE, S-Bahn oder Tram? - "Was für ein Zug ist das?"
- `timeline_zug_bahnhof_bau` - Timeline: Bahnhofs-Bau - "Wann wurde dieser Bahnhof eroeffnet?"
- `timeline_zug_hsb` - Bahn-Timeline - "Chronologisch sortieren — Bahn-Meilensteine!"
- `ws_zug_acela` - WS: Acela - "Bilde Wörter aus dem Zugnamen!"
- `ws_zug_bernina` - WS: Bernina - "Bilde Wörter aus dem Zugnamen!"
- `ws_zug_eurostar` - WS: Eurostar - "Bilde Wörter aus dem Zugnamen!"
- `ws_zug_flixzug` - WS: Flixzug - "Bilde Wörter aus dem Zugnamen!"
- `ws_zug_frecciarossa` - WS: Frecciarossa - "Bilde Wörter aus dem Zugnamen!"
- `ws_zug_intercity` - WS: Intercity - "Bilde Wörter aus dem Zugnamen!"
- `ws_zug_itineraire` - WS: Itineraire - "Bilde Wörter aus dem Zugnamen!"
- `ws_zug_maglev` - WS: Maglev - "Bilde Wörter aus dem Zugnamen!"
- `ws_zug_nightjet` - WS: NightJet - "Bilde Wörter aus NIGHTJET!"
- `ws_zug_panorama` - WS: Panorama - "Bilde Wörter aus PANORAMA!"
- `ws_zug_pendolino` - WS: Pendolino - "Bilde Wörter aus dem Zugnamen!"
- `ws_zug_railjet` - WS: Railjet - "Bilde Wörter aus dem Zugnamen!"
- `ws_zug_shinkansen` - WS: Shinkansen - "Bilde Wörter aus dem Zugnamen!"
- `ws_zug_talgo` - WS: Talgo - "Bilde Wörter aus dem Zugnamen!"
- `ws_zug_thalys` - WS: Thalys - "Bilde Wörter aus dem Zugnamen!"
- `ws_zug_trenitalia` - WS: Trenitalia - "Bilde Wörter aus dem Zugnamen!"
- `ws_zug_velaro` - WS: Velaro - "Bilde Wörter aus dem Zugnamen!"
- `zug_bahnhof_typ` - Bahnhofs-Architektur - "Welche Bauform hat dieser Bahnhof?"
- `zug_ds100` - DS100 (Auswahl) - "Welches Betriebsstellenkürzel hat dieser Bahnhof?"
- `zug_ds100_input` - DS100 (Hardcore) - "Tippe das DS100-Betriebsstellenkürzel!"
- `zug_hersteller` - Zug-Hersteller - "Von welchem Hersteller stammt dieser Zug?"
- `zug_reisezeit_hl` - Strecken-Duell - "Welche Zugfahrt dauert länger?"

### astronomie (27)

- `astro_planet_groesse` - Großer oder kleiner Planet? - "Groß oder klein?"
- `astro_sonne_mond` - Sonne, Mond oder Stern? - "Was ist das?"
- `astro_stern_planet` - Stern oder Planet? - "Ist das ein Stern oder ein Planet?"
- `astro_tag_nacht` - Tag oder Nacht? - "Tag oder Nacht?"
- `hl_astro_entdeckungsjahr` - H/L: Entdeckungsjahr - "Welches Objekt wurde früher entdeckt?"
- `hl_astro_exoplaneten_distanz` - H/L: Exoplaneten-Distanz - "Welcher Exoplanet ist weiter entfernt?"
- `hl_astro_missionsdauer` - H/L: Missionsdauer - "Welche Mission/Sonde war länger aktiv?"
- `hl_astro_monde_anzahl` - H/L: Monde-Anzahl - "Welcher Planet hat mehr Monde?"
- `hl_astro_planet_groesse` - H/L: Planetengröße - "Welcher Planet ist größer?"
- `hl_astro_raketen_nutzlast` - H/L: Raketen-Nutzlast - "Welche Rakete trägt mehr Nutzlast in den LEO?"
- `hl_astro_schwerkraft` - H/L: Oberflächengravitation - "Welcher Himmelskörper hat stärkere Gravitation?"
- `hl_astro_sonnenentfernung` - H/L: Sonnenentfernung - "Welcher Planet ist weiter von der Sonne entfernt?"
- `hl_astro_temperaturen` - H/L: Oberflächentemperatur - "Welcher Planet ist durchschnittlich wärmer?"
- `planet_reihenfolge` - Planeten: Näher zur Sonne? - "Welcher Planet ist näher an der Sonne?"
- `timeline_astro_entdeckung` - Entdeckungs-Zeitleiste - "Ordne die Himmelskörper nach Entdeckungsjahr!"
- `uk_astro_antriebe` - Raketenantriebe - "Welche Antriebsart nutzt diese Rakete?"
- `uk_astro_galaxien_typen` - Galaxien-Typen - "Welchem Galaxientyp gehört diese Galaxie an?"
- `uk_astro_himmelskoerper_typ` - Himmelskörper-Typen - "Zu welchem Typ gehört dieser Himmelskörper?"
- `uk_astro_kosmologie` - Kosmologie-Fakten - "Worum handelt es sich?"
- `uk_astro_pioniere` - Astronomie-Pioniere - "Für welche Entdeckung ist dieser Wissenschaftler bekannt?"
- `uk_astro_planeten` - Planeten-Fakten - "Um welchen Planeten handelt es sich?"
- `uk_astro_sonden_ziele` - Raumsonden & Ziele - "Welches Ziel hat diese Raumsonde angesteuert?"
- `uk_astro_sternbilder_himmel` - Sternbilder zuordnen - "Zu welchem Sternenhimmel gehört dieses Sternbild?"
- `ws_astro_astronaut` - WS: Astronaut - "Bilde Wörter aus ASTRONAUT!"
- `ws_astro_raumstation` - WS: Raumstation - "Bilde Wörter aus RAUMSTATION!"
- `ws_astro_schwarzesloch` - WS: Schwarzes Loch - "Bilde Wörter aus SCHWARZESLOCH!"
- `ws_astro_sternwarte` - WS: Sternwarte - "Bilde Wörter aus STERNWARTE!"

### geologie (25)

- `hl_geo_bohrtiefe` - H/L: Bohrtiefe - "Welche Bohrung / Mine reicht tiefer?"
- `hl_geo_erdbeben` - H/L: Erdbeben-Magnitude - "Welches Erdbeben hatte eine höhere Magnitude?"
- `hl_geo_gesteins_alter` - H/L: Gesteinsalter - "Welches Gestein ist älter?"
- `hl_geo_gletscher_volumen` - H/L: Gletschervolumen - "Welches Eisvorkommen hat mehr Volumen?"
- `hl_geo_hoehlen_laenge` - H/L: Höhlenlänge - "Welches Höhlensystem ist länger?"
- `hl_geo_mohshaerte` - H/L: Mohs-Härte - "Welches Mineral ist härter?"
- `hl_geo_schluchten_tiefe` - H/L: Schluchten-Tiefe - "Welche Schlucht ist tiefer?"
- `hl_geo_schmelztemperatur` - H/L: Schmelztemperatur - "Welches Material hat höheren Schmelzpunkt?"
- `hl_geo_tsunami_hoehe` - H/L: Tsunami-Höhe - "Welcher Tsunami war höher?"
- `timeline_geo_erdbeben` - Erdbeben-Zeitleiste - "Ordne die Erdbeben chronologisch!"
- `uk_geo_erdbeben_jahr` - Historische Erdbeben - "In welchem Jahr ereignete sich dieses Erdbeben?"
- `uk_geo_fossil_zeitalter` - Fossilien & Erdzeitalter - "In welchem Erdzeitalter lebte dieses Wesen?"
- `uk_geo_gestein_nutzung` - Gestein & Nutzung - "Wofür wird dieses Gestein hauptsächlich genutzt?"
- `uk_geo_gesteinsarten` - Gesteinsarten-Quiz - "Zu welcher Gesteinsklasse gehört dieses Gestein?"
- `uk_geo_landschaft_ursprung` - Landschaftsformen & Ursprung - "Durch welchen Prozess entstand diese Landschaftsform?"
- `uk_geo_mineral_farbe` - Mineral-Farben - "Welche charakteristische Farbe hat dieses Mineral?"
- `uk_geo_mineral_kristall` - Mineral-Kristallsysteme - "Welchem Kristallsystem gehört dieses Mineral an?"
- `uk_geo_wunder_entstehung` - Naturwunder & Entstehung - "Durch welchen Prozess entstand dieses Naturwunder?"
- `ws_geo_erdbeben` - WS: Erdbeben - "Bilde Wörter aus ERDBEBEN!"
- `ws_geo_erdkruste` - WS: Erdkruste - "Bilde Wörter aus ERDKRUSTE!"
- `ws_geo_fossilien` - WS: Fossilien - "Bilde Wörter aus FOSSILIEN!"
- `ws_geo_magmakammer` - WS: Magmakammer - "Bilde Wörter aus MAGMAKAMMER!"
- `ws_geo_mineralien` - WS: Mineralien - "Bilde Wörter aus MINERALIEN!"
- `ws_geo_stalaktiten` - WS: Stalaktiten - "Bilde Wörter aus STALAKTITEN!"
- `ws_geo_tropfstein` - WS: Tropfstein - "Bilde Wörter aus TROPFSTEIN!"

### sport_wissen (22)

- `hl_sportwissen_fussball_marktwert` - H/L: Fussball-Marktwert - "Wer hat einen hoeheren Marktwert?"
- `hl_sportwissen_gewichtheben_rekorde` - H/L: Gewichtheben-Rekorde - "Wer hob mehr?"
- `hl_sportwissen_hochsprung_rekorde` - H/L: Hochsprung-Rekorde - "Wer sprang hoeher?"
- `hl_sportwissen_marathon_alter` - H/L: Marathon-Geschichte - "Welcher Marathon ist älter?"
- `hl_sportwissen_olympia_goldmedaillen` - H/L: Olympia-Gold - "Wer gewann mehr Goldmedaillen?"
- `hl_sportwissen_sportler_gehalt` - H/L: Sportler-Gehaelter - "Wer verdient mehr?"
- `hl_sportwissen_stadien_kapazitaet` - H/L: Stadion-Kapazität - "Welches Stadion fasst mehr Zuschauer?"
- `hl_sportwissen_stadion_baujahr` - H/L: Stadion-Baujahr - "Welches Stadion wurde frueher gebaut?"
- `hl_sportwissen_tore_saison` - H/L: Tore pro Saison - "Wer erzielte mehr Tore in einer Saison?"
- `hl_sportwissen_transferrekorde` - H/L: Transferrekorde - "Welcher Transfer war teurer?"
- `timeline_sport_stadien` - Stadion-Zeitleiste - "Ordne die Stadien nach Eröffnungsjahr!"
- `uk_sportwissen_disziplin_kategorie` - Disziplin-Zuordnung - "Zu welcher Disziplin gehoert diese Uebung?"
- `uk_sportwissen_olympisch` - Olympisch? - "Ist diese Sportart olympisch?"
- `uk_sportwissen_teamgroesse` - Teamgrößen-Quiz - "Wie viele Spieler hat ein Team dieser Sportart?"
- `ws_sportwissen_athletik` - WS: Athletik - "Bilde Woerter aus ATHLETIK!"
- `ws_sportwissen_fussball` - WS: Fussball - "Bilde Woerter aus FUSSBALL!"
- `ws_sportwissen_marathon` - WS: Marathon - "Bilde Wörter aus MARATHON!"
- `ws_sportwissen_olympiade` - WS: Olympiade - "Bilde Woerter aus OLYMPIADE!"
- `ws_sportwissen_sportgeist` - WS: Sportgeist - "Bilde Woerter aus SPORTGEIST!"
- `ws_sportwissen_staffellauf` - WS: Staffellauf - "Bilde Wörter aus STAFFELLAUF!"
- `ws_sportwissen_startschuss` - WS: Startschuss - "Bilde Woerter aus STARTSCHUSS!"
- `ws_sportwissen_triathlon` - WS: Triathlon - "Bilde Wörter aus TRIATHLON!"

### hunde (13)

- `hl_hund_alter` - Hunde: Lebenserwartung - "Welche Hunderasse lebt länger?"
- `hl_hund_gewicht` - Hunde: Gewicht - "Welche Hunderasse ist schwerer?"
- `hl_hund_hoehe` - Hunde: Widerristhoehe - "Welche Hunderasse ist größer?"
- `hund_arbeits_begleiter` - Arbeitshund oder Schoßhund? - "Arbeitshund oder Schoßhund?"
- `hund_groesse_klasse` - Hunde: Größenklasse - "Zu welcher Größenklasse gehört diese Rasse?"
- `hund_gross_oder_klein_r` - Große oder kleine Rasse? - "Groß oder klein?"
- `hund_match_fci_gruppe` - Hunde: FCI-Gruppe - "Zu welcher FCI-Gruppe gehört diese Rasse?"
- `hund_match_kategorie` - Hunde: Gruppe - "Welcher Gruppe gehört diese Hunderasse an?"
- `hund_oder_katze_rasse` - Hund oder Katze? - "Hund oder Katze?"
- `hund_pelz_art` - Kurzes oder langes Fell? - "Fell-Typ?"
- `hund_tier_gross` - Hunde: Groß oder Klein? - "Wie groß ist diese Hunderasse?"
- `ws_hund_begleiter` - WS: Begleithund - "Bilde Wörter aus BEGLEITHUND!"
- `ws_hund_welpe` - WS: Welpenschule - "Bilde Wörter aus WELPENSCHULE!"

### boardgames (11)

- `boardgame_match_autor` - Brettspiele: Autor - "Wer hat dieses Spiel erfunden?"
- `hl_boardgame_dauer` - Brettspiele: Spieldauer - "Welches Spiel hat die längere Spieldauer?"
- `hl_boardgame_jahr` - Brettspiele: Älteres Spiel - "Welches Brettspiel ist älter?"
- `hl_boardgame_rating` - Brettspiele: BGG-Wertung - "Welches Spiel hat die höhere BGG-Wertung?"
- `hl_boardgame_spieler` - Brettspiele: Maximale Spieler - "Welches Spiel hat mehr Spieler?"
- `spiel_hl_spieler` - Welches Spiel hat mehr Spieler? - "Welches Spiel kann mit mehr Spielern gespielt werden?"
- `spiel_kurz_lang` - Kurzes oder langes Spiel? - "Wie lange dauert eine Partie?"
- `spiel_spieler_anzahl` - Wie viele Spieler? - "Wie viele Spieler kann man maximal spielen?"
- `spiel_strategie_zufall` - Strategie oder Glück? - "Basiert dieses Spiel mehr auf Strategie oder Glück?"
- `timeline_boardgame_jahr` - Brettspiele-Timeline - "Welches Spiel ist älter?"
- `ws_boardgame_spielbrett` - WS: Spielbrett - "Bilde Wörter aus SPIELBRETT!"

### sport (10)

- `b11` - Rivalen-Distanz - "Wie weit liegen Derby-Gegner auseinander?"
- `b19` - WM-Fehltritte - "Wer war nie bei der WM dabei?"
- `b4` - Olympia-Zeitmaschine - "Wer war Gastgeber der Sommerspiele?"
- `hl_b_wm` - WM-Teilnahmen - "Mehr WM-Teilnahmen?"
- `sport_ball_oder_nicht` - Ballsport? - "Ist das ein Ballsport?"
- `sport_olympia_sommer` - Sommer- oder Wintersport? - "Ist das ein Sommer- oder Wintersport?"
- `sport_sommer_winter_oly` - Olympia: Sommer oder Winter? - "Bei welchen Olympischen Spielen dabei?"
- `sport_spieler_anzahl` - Wie viele Spieler pro Team? - "Wie viele Spieler hat ein Team in diesem Sport?"
- `sport_teamsport` - Team- oder Einzelsport? - "Wird dieser Sport in Teams gespielt?"
- `sport_wasser_land_sport` - Wassersport oder Landsport? - "Ist das ein Wasser- oder Landsport?"

### architektur (8)

- `arch_match_typ` - Architektur: Typ - "Welchem Typ gehört dieses Bauwerk an?"
- `hl_arch_baujahr` - Architektur: Älteres Bauwerk - "Welches Bauwerk ist älter?"
- `hl_arch_height` - Architektur: Höhe - "Welches Bauwerk ist höher?"
- `hl_arch_laenge` - Architektur: Länge - "Welches Bauwerk ist länger?"
- `hl_arch_span` - Architektur: Brückenspannweite - "Welche Brücke hat die größere Spannweite?"
- `timeline_arch_baujahr` - Architektur-Timeline - "Welches Bauwerk ist älter?"
- `ws_arch_fundament` - WS: Fundament - "Bilde Wörter aus FUNDAMENT!"
- `ws_arch_wolkenkratzer` - WS: Wolkenkratzer - "Bilde Wörter aus WOLKENKRATZER!"

### filme (7)

- `film_match_regisseur` - Film-Quiz: Regisseur - "Von welchem Regisseur stammt dieser Film?"
- `hl_film_boxoffice` - Film-Quartett: Einspielergebnis - "Welcher Film hat mehr eingespielt?"
- `hl_film_imdb` - Film-Quartett: IMDb-Rating - "Welcher Film hat die höhere IMDb-Bewertung?"
- `hl_film_laenge` - Film-Quartett: Spielzeit - "Welcher Film ist länger?"
- `hl_film_oscars` - Film-Quartett: Oscars - "Welcher Film hat mehr Oscars gewonnen?"
- `hl_film_release` - Film-Quartett: Älterer Film - "Welcher Film erschien früher?"
- `timeline_film_release` - Film-Timeline - "Welcher Film erschien zuerst?"

### mythologie (7)

- `myth_match_domain` - Mythologie: Domäne - "Welchem Bereich/welcher Domäne gehört diese mythologische Figur an?"
- `myth_match_kultur` - Mythologie: Kultur - "Welcher Mythologie/Kultur gehört diese Figur an?"
- `myth_match_roemisch` - Mythologie: Röm. Gegenstück - "Wie lautet das römische Gegenstück?"
- `myth_match_tier` - Mythologie: Tier-Symbol - "Welches Tier ist mit dieser Gottheit verbunden?"
- `myth_match_typ` - Mythologie: Typ - "Welchen Typ hat diese mythologische Figur?"
- `ws_myth_pantheon` - WS: Pantheon - "Bilde Wörter aus PANTHEON!"
- `ws_myth_unterwelt` - WS: Unterwelt - "Bilde Wörter aus UNTERWELT!"

### hl_compare (6)

- `hl_density` - H/L Bevölkerungsdichte - "Dichter besiedelt?"
- `hl_forest` - H/L Waldfäche - "Mehr Wald?"
- `hl_gdp` - H/L BIP - "Höheres BIP?"
- `hl_lifeexp` - H/L Lebenserwartung - "Länger leben?"
- `hl_median_age` - H/L Medianalter - "Höheres Medianalter?"
- `hl_pop` - H/L Einwohner - "Mehr Einwohner?"

### comparisons (6)

- `comp_age` - Höheres Medianalter? - "Höheres Medianalter?"
- `comp_gdp` - Höheres BIP? - "Höheres BIP pro Kopf?"
- `hl_b_ev` - E-Ladesäulen - "Mehr E-Ladesäulen?"
- `hl_b_net` - Internetspeed - "Schnelleres Internet?"
- `hl_b_rail` - Schienennetz - "Längeres Schienennetz?"
- `hl_b_roads` - Straßennetz - "Längeres Straßennetz?"

### hardware (6)

- `hl_hw_units` - Hardware-Quartett: Verkaufszahlen - "Welche Konsole verkaufte sich häufiger?"
- `hl_hw_year` - Hardware-Quartett: Release-Jahr - "Welche Konsole erschien später?"
- `hw_baujahr_mc` - Hardware: Release-Jahr raten - "In welchem Jahr erschien diese Konsole?"
- `hw_match_company` - Hardware: Hersteller - "Von welchem Unternehmen stammt diese Konsole?"
- `hw_match_generation` - Hardware: Konsolengeneration - "Zu welcher Konsolengeneration gehört diese Konsole?"
- `hw_match_type` - Hardware: Konsolen-Typ - "Welche Art von Konsole ist das?"

### musik (6)

- `hl_musik_grammys` - Musik-Quartett: Grammys - "Wer hat mehr Grammys?"
- `hl_musik_gruendung` - Musik-Quartett: Älterer Künstler - "Wer gründete sich früher?"
- `hl_musik_streams` - Musik-Quartett: Streams - "Wer hat mehr Streams?"
- `hl_musik_verkaeufe` - Musik-Quartett: Verkäufe - "Wer hat mehr Tonträger verkauft?"
- `musik_match_hit` - Musik-Quiz: Größter Hit - "Welcher Song ist ein bekannter Hit von diesem Künstler?"
- `timeline_musik_gruendung` - Musik-Timeline - "Welcher Künstler ist älter?"

### serien (6)

- `hl_serie_episoden` - Serien-Quartett: Episoden - "Welche Serie hat mehr Episoden?"
- `hl_serie_imdb` - Serien-Quartett: IMDb-Rating - "Welche Serie hat die höhere IMDb-Bewertung?"
- `hl_serie_staffeln` - Serien-Quartett: Staffeln - "Welche Serie hat mehr Staffeln?"
- `hl_serie_start` - Serien-Quartett: Älter - "Welche Serie startete früher?"
- `serie_match_genre` - Serien-Quiz: Genre - "Welches Genre hat diese Serie?"
- `timeline_serie_start` - Serien-Timeline - "Welche Serie startete zuerst?"

### literatur (6)

- `hl_lit_release` - Literatur-Quartett: Älteres Werk - "Welches Werk erschien früher?"
- `hl_lit_sales` - Literatur-Quartett: Verkäufe - "Welches Werk hat mehr Exemplare verkauft?"
- `lit_match_autor` - Literatur-Quiz: Autor - "Wer schrieb dieses Werk?"
- `lit_match_protagonist` - Literatur-Quiz: Protagonist - "Wer ist der Protagonist dieses Werks?"
- `timeline_lit_release` - Literatur-Timeline - "Welches Werk erschien zuerst?"
- `ws_lit_protagonist` - WS: Tintenherz - "Bilde Wörter aus TINTENHERZ!"

### robotik (6)

- `hl_robot_jahr` - KI/Robotik: Ältestes System - "Welcher Meilenstein/welches System kam zuerst?"
- `robot_match_entwickler` - KI/Robotik-Quiz: Entwickler - "Wer entwickelte dieses System?"
- `robot_match_fakt` - KI/Robotik-Quiz: Fakten-Match - "Welcher Fakt beschreibt dieses System am besten?"
- `robot_match_kategorie` - KI/Robotik-Quiz: Kategorie - "Welcher Kategorie gehört dieses KI/Robotik-System an?"
- `timeline_robot_jahr` - KI/Robotik-Timeline - "Welcher Meilenstein kam zuerst?"
- `ws_robot_name` - WS: Maschinenlernen - "Bilde Wörter aus MASCHINENLERNEN!"

### medizin (6)

- `hl_med_gewicht` - Medizin: Organgewicht - "Welches Organ/Körperteil ist schwerer?"
- `hl_med_knochen` - Medizin: Knochen - "Welcher Knochen kommt öfter vor?"
- `med_match_fachbegriff` - Medizin: Fachbegriff - "Wie lautet der lateinische Fachbegriff?"
- `timeline_med_meilensteine` - Medizin-Timeline - "Welcher Meilenstein kam zuerst?"
- `ws_med_blutkreislauf` - WS: Blutkreislauf - "Bilde Wörter aus BLUTKREISLAUF!"
- `ws_med_stoffwechsel` - WS: Stoffwechsel - "Bilde Wörter aus STOFFWECHSEL!"

### wirtschaft (6)

- `eco_match_branche` - Wirtschaft: Branche - "Welcher Branche gehört dieses Unternehmen an?"
- `hl_eco_gruendung` - Wirtschaft: Älteres Unternehmen - "Welches Unternehmen wurde früher gegründet?"
- `hl_eco_mitarbeiter` - Wirtschaft: Mitarbeiter - "Welches Unternehmen hat mehr Mitarbeiter?"
- `hl_eco_umsatz` - Wirtschaft: Umsatz - "Welches Unternehmen hat höheren Umsatz?"
- `timeline_eco_gruendung` - Wirtschaft-Timeline - "Welches Unternehmen wurde früher gegründet?"
- `ws_eco_aktie` - WS: Aktiengesellschaft - "Bilde Wörter aus AKTIENGESELLSCHAFT!"

### geschichte (6)

- `hist_match_figur` - Geschichte: Schlüsselfigur - "Wer war die Schlüsselfigu?"
- `hl_hist_ausdehnung` - Geschichte: Ausdehnung - "Welches Reich hatte eine größere Ausdehnung?"
- `hl_hist_dauer` - Geschichte: Dauer - "Was dauerte länger?"
- `hl_hist_start` - Geschichte: Ältestes Reich/Epoche - "Was begann früher?"
- `timeline_hist_start` - Geschichte-Timeline - "Was begann früher?"
- `ws_hist_renaissance` - WS: Renaissance - "Bilde Wörter aus RENAISSANCE!"

### kunst (6)

- `hl_kunst_jahr` - Kunstgeschichte: Älteres Werk - "Welches Kunstwerk ist älter?"
- `hl_kunst_wert` - Kunstgeschichte: Schätzwert - "Welches Kunstwerk hat einen höheren Schätzwert?"
- `kunst_match_epoche` - Kunstgeschichte: Epoche - "Welcher Kunstepoche gehört dieses Werk an?"
- `kunst_match_kuenstler` - Kunstgeschichte: Künstler - "Wer hat dieses Kunstwerk erschaffen?"
- `timeline_kunst_jahr` - Kunst-Timeline - "Welches Kunstwerk ist älter?"
- `ws_kunst_renaissance` - WS: Renaissance - "Bilde Wörter aus RENAISSANCE!"

### gartenbau (6)

- `garten_match_boden` - Gartenbau: Bodenanspruch - "Welchen Bodenanspruch hat diese Pflanze?"
- `garten_match_wasser` - Gartenbau: Wasserbedarf - "Welchen Wasserbedarf hat diese Pflanze?"
- `hl_garten_bluete` - Gartenbau: Frühster Blüher - "Welche Pflanze blüht früher im Jahr?"
- `hl_garten_hoehe` - Gartenbau: Wuchshoehe - "Welche Pflanze wächst höher?"
- `ws_garten_rhodo` - WS: Rhododendron - "Bilde Wörter aus RHODODENDRON!"
- `ws_garten_strelitzie` - WS: Strelitzie - "Bilde Wörter aus STRELITZIE!"

### airports (5)

- `flugrouten_duell` - Flugrouten-Duell - "Welche Flugroute ist länger?"
- `jetlag_rechner` - Jetlag-Rechner - "Wie spät ist es bei der Landung Ortszeit?"
- `sonnen_kompass` - Sonnen-Kompass - "Wohin geht die Sonne unter?"
- `uk_distanz_schaetzer` - Distanz-Schätzer - "Wie weit ist diese Strecke (ca.)?"
- `uk_flugzeit_schaetzer` - Flugzeit-Schätzer - "Wie lange dauert dieser Flug?"

### webkultur (5)

- `hl_web_reichweite` - Webkultur: Reichweite - "Welches Internet-Phänomen hat mehr Reichweite?"
- `hl_web_start` - Webkultur: Ältestes Phänomen - "Was startete früher?"
- `timeline_web_start` - Webkultur-Timeline - "Was startete früher?"
- `web_match_kategorie` - Webkultur: Kategorie - "Welcher Kategorie gehört dieses Internet-Phänomen an?"
- `ws_web_algorithmus` - WS: Algorithmus - "Bilde Wörter aus ALGORITHMUS!"

### pure_geo (4)

- `hl_b_rain` - Niederschlag - "Mehr Regen?"
- `hl_b_sun` - Sonnenstunden - "Mehr Sonne?"
- `hl_b_temp` - Temperatur - "Wärmer?"
- `land_in_eu` - EU-Mitglied? - "EU-Mitglied?"

### map_mode (4)

- `b51` - Wuesten-Fokus - "Klicke auf das Wuestenland"
- `karte_nord_sued` - Nördlich oder südlich? - "Nördlich oder südlich?"
- `kompass_richtung` - Kompass: Himmelsrichtungen - "In welche Himmelsrichtung zeigt der Pfeil?"
- `uk_mercator_illusion` - Mercator-Illusion - "Stimmt diese Größenaussage? (Ja/Nein)"

### lifestyle (3)

- `hl_b_lang` - Amtssprachen - "Mehr Amtssprachen?"
- `hl_b_tour` - Tourismus - "Mehr Touristen?"
- `uk_schatten_gedreht` - Silhouette gedreht - "Erkenne diesen Umriss — auch gedreht!"

### sprachen (3)

- `sprache_match_familie` - Sprachen: Sprachfamilie - "Welcher Sprachfamilie gehört diese Sprache an?"
- `sprache_match_schrift` - Sprachen: Schriftsystem - "Welche Schrift verwendet diese Sprache?"
- `ws_sprache_grammatik` - WS: Grammatik - "Bilde Wörter aus GRAMMATIK!"

### klima (2)

- `wetter_piktogramm` - Wetter-Symbole - "Welches Wetter zeigt dieses Symbol?"
- `ws_klima_monsun` - WS: Monsun - "Bilde Wörter aus MONSUN!"

### kultur (2)

- `uk_ruinen` - Historische Ruinen - "📍 Pinne diese historische Ruine:"
- `uk_wolkenkratzer` - Wolkenkratzer-Duell - "Welches Gebäude ist höher?"

### themeparks (2)

- `park_match_kategorie` - Freizeitpark: Typ - "Welchem Typ gehört diese Attraktion an?"
- `ws_park_achterbahn` - WS: Achterbahn - "Bilde Wörter aus ACHTERBAHN!"

### capitals (2)

- `capital_anfang` - Mit welchem Buchstaben? - "Anfangsbuchstabe?"
- `ws_capital_reykjavik` - WS: Reykjavik - "Bilde Wörter aus REYKJAVIK!"

### neighbors (1)

- `neighbor` - Grenzgänger - "Grenzt an…?"

### new_modes (1)

- `logic_grid` - Logik-Gitter - "Löse das Rätsel"

### fluesse (1)

- `ws_fluss_amazonas` - WS: Amazonas - "Bilde Wörter aus AMAZONAS!"

### nparks (1)

- `ws_npark_yellowstone` - WS: Yellowstone - "Bilde Wörter aus YELLOWSTONE!"

### inseln (1)

- `ws_insel_groenland` - WS: Grönland - "Bilde Wörter aus GROENLAND!"

### gipfel (1)

- `ws_gipfel_himalaya` - WS: Himalaya - "Bilde Wörter aus HIMALAYA!"

### ozeane (1)

- `ws_ozean_atlantik` - WS: Atlantik - "Bilde Wörter aus ATLANTIK!"
