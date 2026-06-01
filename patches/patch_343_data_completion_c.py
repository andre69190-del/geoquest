#!/usr/bin/env python3
"""
Phase: 343
Date:  2026-06-01
Author: Claude / Andre
Scope: Data Completion Sprint 330c — Oberklasse, Ford Europe, Skandinavien, Kult-Ikonen

Description:
  Schließt die letzten großen Lücken:
  • BMW: 1er (E87/F20/F40), 7er (E32/E38/E65/G11), X5 (E53/F15)
  • Mercedes: S-Klasse (W126/W140/W221/W223), A-Klasse (W168/W176 Basis),
              SL R129, G-Klasse W463 Basis
  • Audi: A8 (D2/D3/D4), TT (8J/8S — 8N bereits vorhanden)
  • Porsche: Boxster (986/981), Cayenne (9PA/9YA)
  • Opel: Manta B, Calibra
  • Ford of Europe: Fiesta Mk1/Mk3/Mk7, Focus Mk1/Mk2/Mk3 Basis,
                   Capri Mk3, Sierra Basis
  • Volvo: 240, V70, XC90 Gen1+Gen2
  • Saab: 900 Basis, 9-3 Basis
  • Smart: Fortwo W453
  • Mini: Classic (Basis), BMW Mini R50, F56

Dependencies: Phase 342
Zero-Bug Policy: Kein gen.py-Patch nötig — alle Arrays bereits registriert
"""
import json, os, subprocess, sys

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTOS = os.path.join(ROOT, "data", "autos.json")

CARS = [
    # ──────────────────────────────────────────────────────────────────
    # BMW 1er — E87, F20, F40
    # ──────────────────────────────────────────────────────────────────
    {"key": "BMW 116i E87 (Deutschland, 2004)",    "ps": 115, "ccm": 1596, "vmax": 196, "accel": 11.0, "bj": 2004, "ev": False},
    {"key": "BMW 130i E87 (Deutschland, 2005)",    "ps": 265, "ccm": 2996, "vmax": 250, "accel":  6.1, "bj": 2005, "ev": False},
    {"key": "BMW 116i F20 (Deutschland, 2011)",    "ps": 136, "ccm": 1598, "vmax": 208, "accel":  9.7, "bj": 2011, "ev": False},
    {"key": "BMW M135i F20 (Deutschland, 2012)",   "ps": 320, "ccm": 2979, "vmax": 250, "accel":  4.9, "bj": 2012, "ev": False},
    {"key": "BMW 116i F40 (Deutschland, 2019)",    "ps": 109, "ccm": 1499, "vmax": 198, "accel": 10.4, "bj": 2019, "ev": False},
    {"key": "BMW M135i xDrive F40 (Deutschland, 2019)", "ps": 306, "ccm": 1998, "vmax": 250, "accel":  4.8, "bj": 2019, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # BMW 7er — E32, E38, E65, G11
    # ──────────────────────────────────────────────────────────────────
    {"key": "BMW 730i E32 (Deutschland, 1986)",    "ps": 188, "ccm": 2986, "vmax": 225, "accel":  9.3, "bj": 1986, "ev": False},
    {"key": "BMW 750iL E32 (Deutschland, 1987)",   "ps": 300, "ccm": 4988, "vmax": 250, "accel":  7.4, "bj": 1987, "ev": False},
    {"key": "BMW 728i E38 (Deutschland, 1994)",    "ps": 193, "ccm": 2793, "vmax": 225, "accel":  9.5, "bj": 1994, "ev": False},
    {"key": "BMW 750iL E38 (Deutschland, 1994)",   "ps": 326, "ccm": 4988, "vmax": 250, "accel":  7.4, "bj": 1994, "ev": False},
    {"key": "BMW 730i E65 (Deutschland, 2001)",    "ps": 231, "ccm": 2996, "vmax": 250, "accel":  8.5, "bj": 2001, "ev": False},
    {"key": "BMW 760Li E65 (Deutschland, 2003)",   "ps": 445, "ccm": 5972, "vmax": 250, "accel":  5.5, "bj": 2003, "ev": False},
    {"key": "BMW 730i G11 (Deutschland, 2015)",    "ps": 258, "ccm": 1998, "vmax": 250, "accel":  6.8, "bj": 2015, "ev": False},
    {"key": "BMW M760Li G11 (Deutschland, 2016)",  "ps": 585, "ccm": 6592, "vmax": 250, "accel":  3.9, "bj": 2016, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # BMW X5 — E53, F15
    # ──────────────────────────────────────────────────────────────────
    {"key": "BMW X5 3.0i E53 (Deutschland, 1999)", "ps": 231, "ccm": 2979, "vmax": 210, "accel":  8.7, "bj": 1999, "ev": False},
    {"key": "BMW X5 4.6is E53 (Deutschland, 2002)","ps": 347, "ccm": 4619, "vmax": 237, "accel":  6.5, "bj": 2002, "ev": False},
    {"key": "BMW X5 xDrive25d F15 (Deutschland, 2013)","ps": 218, "ccm": 1995, "vmax": 223, "accel":  8.3, "bj": 2013, "ev": False},
    {"key": "BMW X5 M F85 (Deutschland, 2014)",    "ps": 575, "ccm": 4395, "vmax": 250, "accel":  4.2, "bj": 2014, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # MERCEDES S-KLASSE — W126, W140, W221, W223
    # ──────────────────────────────────────────────────────────────────
    {"key": "Mercedes-Benz 280 S W126 (Deutschland, 1979)",  "ps": 185, "ccm": 2746, "vmax": 210, "accel": 10.5, "bj": 1979, "ev": False},
    {"key": "Mercedes-Benz 560 SEL W126 (Deutschland, 1985)","ps": 300, "ccm": 5547, "vmax": 238, "accel":  7.0, "bj": 1985, "ev": False},
    {"key": "Mercedes-Benz 300 SE W140 (Deutschland, 1991)", "ps": 197, "ccm": 2960, "vmax": 228, "accel":  9.5, "bj": 1991, "ev": False},
    {"key": "Mercedes-Benz S 600 W140 (Deutschland, 1992)",  "ps": 394, "ccm": 5987, "vmax": 250, "accel":  6.1, "bj": 1992, "ev": False},
    {"key": "Mercedes-Benz S 350 W221 (Deutschland, 2005)",  "ps": 272, "ccm": 3498, "vmax": 250, "accel":  7.2, "bj": 2005, "ev": False},
    {"key": "Mercedes-Benz S 65 AMG W221 (Deutschland, 2006)","ps":612, "ccm": 5980, "vmax": 250, "accel":  4.4, "bj": 2006, "ev": False},
    {"key": "Mercedes-Benz S 500 W223 (Deutschland, 2020)",  "ps": 435, "ccm": 2999, "vmax": 250, "accel":  4.9, "bj": 2020, "ev": False},
    {"key": "Mercedes-Benz S 63 AMG W223 (Deutschland, 2021)","ps":612, "ccm": 3982, "vmax": 300, "accel":  3.4, "bj": 2021, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # MERCEDES A-KLASSE — W168 (1997), W176 Basis (2012, Top bereits als A45 AMG vorhanden)
    # ──────────────────────────────────────────────────────────────────
    {"key": "Mercedes-Benz A 140 W168 (Deutschland, 1997)",  "ps":  82, "ccm": 1397, "vmax": 160, "accel": 13.5, "bj": 1997, "ev": False},
    {"key": "Mercedes-Benz A 210 Evo W168 (Deutschland, 2000)","ps":140, "ccm": 2084, "vmax": 210, "accel":  7.9, "bj": 2000, "ev": False},
    {"key": "Mercedes-Benz A 160 W176 (Deutschland, 2012)",  "ps": 102, "ccm": 1595, "vmax": 200, "accel": 11.5, "bj": 2012, "ev": False},
    # A45 AMG W176 (2013) — bereits vorhanden

    # ──────────────────────────────────────────────────────────────────
    # MERCEDES SL R129 & G-KLASSE W463 Basis
    # ──────────────────────────────────────────────────────────────────
    {"key": "Mercedes-Benz SL 300 R129 (Deutschland, 1989)", "ps": 231, "ccm": 2962, "vmax": 245, "accel":  7.6, "bj": 1989, "ev": False},
    {"key": "Mercedes-Benz SL 73 AMG R129 (Deutschland, 1999)","ps":525, "ccm": 7291, "vmax": 300, "accel":  4.6, "bj": 1999, "ev": False},
    {"key": "Mercedes-Benz G 300 W463 (Deutschland, 1989)",  "ps": 170, "ccm": 2874, "vmax": 160, "accel": 14.5, "bj": 1989, "ev": False},
    {"key": "Mercedes-Benz G 500 W463 (Deutschland, 1998)",  "ps": 296, "ccm": 4966, "vmax": 210, "accel":  8.0, "bj": 1998, "ev": False},
    # G63 AMG (2012) — bereits vorhanden

    # ──────────────────────────────────────────────────────────────────
    # AUDI A8 — D2, D3, D4
    # ──────────────────────────────────────────────────────────────────
    {"key": "Audi A8 2.8 D2 (Deutschland, 1994)",  "ps": 174, "ccm": 2771, "vmax": 225, "accel":  9.0, "bj": 1994, "ev": False},
    {"key": "Audi S8 D2 (Deutschland, 1996)",       "ps": 360, "ccm": 4172, "vmax": 250, "accel":  5.6, "bj": 1996, "ev": False},
    {"key": "Audi A8 3.0 D3 (Deutschland, 2002)",   "ps": 220, "ccm": 2976, "vmax": 250, "accel":  7.6, "bj": 2002, "ev": False},
    {"key": "Audi S8 D3 (Deutschland, 2006)",        "ps": 450, "ccm": 5204, "vmax": 250, "accel":  5.1, "bj": 2006, "ev": False},
    {"key": "Audi A8 3.0 TFSI D4 (Deutschland, 2010)","ps":310, "ccm": 2995, "vmax": 250, "accel":  6.1, "bj": 2010, "ev": False},
    {"key": "Audi S8 D4 (Deutschland, 2012)",        "ps": 520, "ccm": 3993, "vmax": 250, "accel":  4.2, "bj": 2012, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # AUDI TT — 8J, 8S (8N bereits vorhanden)
    # ──────────────────────────────────────────────────────────────────
    {"key": "Audi TT 1.8 TFSI 8J (Deutschland, 2006)", "ps": 160, "ccm": 1798, "vmax": 225, "accel":  8.5, "bj": 2006, "ev": False},
    {"key": "Audi TTS 8J (Deutschland, 2008)",          "ps": 272, "ccm": 1984, "vmax": 250, "accel":  5.4, "bj": 2008, "ev": False},
    {"key": "Audi TT 2.0 TFSI 8S (Deutschland, 2014)", "ps": 230, "ccm": 1984, "vmax": 250, "accel":  5.9, "bj": 2014, "ev": False},
    {"key": "Audi TT RS 8S (Deutschland, 2016)",        "ps": 400, "ccm": 2480, "vmax": 280, "accel":  3.7, "bj": 2016, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # PORSCHE BOXSTER — 986, 981
    # ──────────────────────────────────────────────────────────────────
    {"key": "Porsche Boxster 986 (Deutschland, 1996)",   "ps": 204, "ccm": 2480, "vmax": 240, "accel":  6.9, "bj": 1996, "ev": False},
    {"key": "Porsche Boxster S 986 (Deutschland, 2000)", "ps": 252, "ccm": 3179, "vmax": 260, "accel":  5.9, "bj": 2000, "ev": False},
    {"key": "Porsche Boxster 981 (Deutschland, 2012)",   "ps": 265, "ccm": 2706, "vmax": 264, "accel":  5.7, "bj": 2012, "ev": False},
    {"key": "Porsche Boxster S 981 (Deutschland, 2012)", "ps": 315, "ccm": 3436, "vmax": 278, "accel":  5.1, "bj": 2012, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # PORSCHE CAYENNE — 9PA, 9YA
    # ──────────────────────────────────────────────────────────────────
    {"key": "Porsche Cayenne V6 9PA (Deutschland, 2002)",    "ps": 250, "ccm": 3179, "vmax": 217, "accel":  9.1, "bj": 2002, "ev": False},
    {"key": "Porsche Cayenne Turbo 9PA (Deutschland, 2002)", "ps": 450, "ccm": 4511, "vmax": 266, "accel":  5.6, "bj": 2002, "ev": False},
    {"key": "Porsche Cayenne V6 9YA (Deutschland, 2017)",    "ps": 340, "ccm": 2995, "vmax": 245, "accel":  6.2, "bj": 2017, "ev": False},
    {"key": "Porsche Cayenne Turbo S E-Hybrid 9YA (Deutschland, 2019)", "ps": 680, "ccm": 3996, "vmax": 295, "accel":  3.8, "bj": 2019, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # OPEL MANTA B & CALIBRA
    # ──────────────────────────────────────────────────────────────────
    {"key": "Opel Manta B (Deutschland, 1975)",         "ps":  75, "ccm": 1584, "vmax": 165, "accel": 13.5, "bj": 1975, "ev": False},
    {"key": "Opel Manta B GT/E (Deutschland, 1975)",    "ps": 105, "ccm": 1979, "vmax": 186, "accel": 10.5, "bj": 1975, "ev": False},
    # Opel Manta 400 (1982) — bereits vorhanden
    {"key": "Opel Calibra (Deutschland, 1990)",         "ps": 115, "ccm": 1998, "vmax": 200, "accel": 10.8, "bj": 1990, "ev": False},
    {"key": "Opel Calibra Turbo 4x4 (Deutschland, 1992)","ps":204, "ccm": 1998, "vmax": 240, "accel":  7.6, "bj": 1992, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # FORD FIESTA — Mk1, Mk3, Mk7
    # ──────────────────────────────────────────────────────────────────
    {"key": "Ford Fiesta Mk1 (Deutschland, 1976)",        "ps":  40, "ccm":  957, "vmax": 130, "accel": 20.0, "bj": 1976, "ev": False},
    {"key": "Ford Fiesta XR2 (Deutschland, 1981)",        "ps":  84, "ccm": 1599, "vmax": 170, "accel":  9.8, "bj": 1981, "ev": False},
    {"key": "Ford Fiesta Mk3 (Deutschland, 1989)",        "ps":  50, "ccm": 1118, "vmax": 145, "accel": 16.0, "bj": 1989, "ev": False},
    {"key": "Ford Fiesta XR2i 16V (Deutschland, 1992)",   "ps": 133, "ccm": 1597, "vmax": 200, "accel":  8.3, "bj": 1992, "ev": False},
    {"key": "Ford Fiesta Mk7 (Deutschland, 2008)",        "ps":  60, "ccm": 1242, "vmax": 158, "accel": 16.8, "bj": 2008, "ev": False},
    {"key": "Ford Fiesta ST Mk7 (Deutschland, 2013)",     "ps": 182, "ccm": 1596, "vmax": 222, "accel":  6.9, "bj": 2013, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # FORD FOCUS — Mk1, Mk2, Mk3
    # ──────────────────────────────────────────────────────────────────
    {"key": "Ford Focus Mk1 (Deutschland, 1998)",         "ps":  75, "ccm": 1388, "vmax": 175, "accel": 13.0, "bj": 1998, "ev": False},
    {"key": "Ford Focus RS Mk1 (Vereinigtes Königreich, 2002)", "ps": 215, "ccm": 1988, "vmax": 235, "accel":  6.5, "bj": 2002, "ev": False},
    {"key": "Ford Focus Mk2 (Deutschland, 2004)",         "ps":  80, "ccm": 1388, "vmax": 175, "accel": 13.3, "bj": 2004, "ev": False},
    {"key": "Ford Focus ST Mk2 (Vereinigtes Königreich, 2005)", "ps": 225, "ccm": 2521, "vmax": 247, "accel":  6.8, "bj": 2005, "ev": False},
    {"key": "Ford Focus Mk3 (Deutschland, 2011)",         "ps": 100, "ccm":  999, "vmax": 193, "accel": 10.5, "bj": 2011, "ev": False},
    # Focus RS Mk3 (2016) — bereits vorhanden als "Ford Focus RS (UK, 2016)"

    # ──────────────────────────────────────────────────────────────────
    # FORD CAPRI Mk3 & SIERRA Basis
    # ──────────────────────────────────────────────────────────────────
    {"key": "Ford Capri Mk3 (Deutschland, 1978)",              "ps":  73, "ccm": 1593, "vmax": 175, "accel": 13.5, "bj": 1978, "ev": False},
    {"key": "Ford Capri 2.8 Injection (Vereinigtes Königreich, 1981)", "ps": 160, "ccm": 2792, "vmax": 217, "accel":  8.7, "bj": 1981, "ev": False},
    {"key": "Ford Sierra (Deutschland, 1982)",                 "ps":  75, "ccm": 1593, "vmax": 175, "accel": 13.5, "bj": 1982, "ev": False},
    # Ford Sierra RS Cosworth (1986) — bereits vorhanden

    # ──────────────────────────────────────────────────────────────────
    # VOLVO 240, V70, XC90 Gen1+Gen2
    # ──────────────────────────────────────────────────────────────────
    # Volvo 850 T5-R (1994) — bereits vorhanden
    {"key": "Volvo 244 (Schweden, 1974)",              "ps":  97, "ccm": 1986, "vmax": 170, "accel": 13.5, "bj": 1974, "ev": False},
    {"key": "Volvo 244 Turbo (Schweden, 1981)",        "ps": 155, "ccm": 1986, "vmax": 195, "accel":  9.6, "bj": 1981, "ev": False},
    {"key": "Volvo 850 (Schweden, 1991)",              "ps": 144, "ccm": 2435, "vmax": 195, "accel": 10.6, "bj": 1991, "ev": False},
    # 850 T5-R bereits vorhanden
    {"key": "Volvo V70 (Schweden, 1996)",              "ps": 140, "ccm": 1984, "vmax": 200, "accel": 10.3, "bj": 1996, "ev": False},
    {"key": "Volvo V70 R (Schweden, 1998)",            "ps": 250, "ccm": 2319, "vmax": 250, "accel":  6.1, "bj": 1998, "ev": False},
    {"key": "Volvo XC90 T5 Gen1 (Schweden, 2002)",    "ps": 210, "ccm": 2521, "vmax": 210, "accel":  9.5, "bj": 2002, "ev": False},
    {"key": "Volvo XC90 V8 Gen1 (Schweden, 2005)",    "ps": 315, "ccm": 4414, "vmax": 225, "accel":  7.8, "bj": 2005, "ev": False},
    {"key": "Volvo XC90 T5 Gen2 (Schweden, 2014)",    "ps": 254, "ccm": 1969, "vmax": 220, "accel":  7.3, "bj": 2014, "ev": False},
    {"key": "Volvo XC90 T8 Twin Engine Gen2 (Schweden, 2015)", "ps": 407, "ccm": 1969, "vmax": 230, "accel":  5.6, "bj": 2015, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # SAAB 900, 9-3 (Basismodelle — Turbo/Aero bereits vorhanden)
    # ──────────────────────────────────────────────────────────────────
    # Saab 900 Turbo (1978) — bereits vorhanden
    {"key": "Saab 900 (Schweden, 1978)",               "ps": 100, "ccm": 1985, "vmax": 175, "accel": 11.0, "bj": 1978, "ev": False},
    # Saab 9-3 Aero (2002) — bereits vorhanden
    {"key": "Saab 9-3 (Schweden, 1998)",               "ps": 150, "ccm": 1985, "vmax": 210, "accel":  9.5, "bj": 1998, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # SMART FORTWO — W453 (W450 1998 bereits vorhanden)
    # ──────────────────────────────────────────────────────────────────
    # Smart Fortwo (1998) & Brabus (2007) — bereits vorhanden
    {"key": "Smart Fortwo W453 (Deutschland, 2014)",     "ps":  71, "ccm":  999, "vmax": 155, "accel": 11.0, "bj": 2014, "ev": False},
    {"key": "Smart Fortwo Brabus W453 (Deutschland, 2016)","ps":109, "ccm":  898, "vmax": 160, "accel":  9.5, "bj": 2016, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # MINI — Classic, BMW Mini R50, F56
    # ──────────────────────────────────────────────────────────────────
    # Classic Mini Cooper S (1964) — bereits vorhanden als "Mini Cooper S (UK, 1964)"
    {"key": "Mini Classic (Vereinigtes Königreich, 1959)",     "ps":  34, "ccm":  848, "vmax": 116, "accel": 27.0, "bj": 1959, "ev": False},
    {"key": "BMW Mini One R50 (Vereinigtes Königreich, 2001)", "ps":  90, "ccm": 1598, "vmax": 175, "accel": 12.0, "bj": 2001, "ev": False},
    {"key": "BMW Mini Cooper S R53 (Vereinigtes Königreich, 2002)", "ps": 163, "ccm": 1598, "vmax": 218, "accel":  7.4, "bj": 2002, "ev": False},
    {"key": "BMW Mini One F56 (Vereinigtes Königreich, 2014)", "ps": 102, "ccm": 1198, "vmax": 183, "accel": 10.5, "bj": 2014, "ev": False},
    {"key": "BMW Mini JCW F56 (Vereinigtes Königreich, 2015)", "ps": 231, "ccm": 1998, "vmax": 250, "accel":  6.3, "bj": 2015, "ev": False},
]


def dedup(items, name, val):
    if any(e["name"].lower() == name.lower() for e in items):
        return 0
    items.append({"name": name, "val": val})
    return 1


def run(cmd):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.stdout: print(r.stdout[-600:])
    if r.stderr: print(r.stderr[-200:], file=sys.stderr)
    return r.returncode


if __name__ == "__main__":
    print("=" * 60)
    print(f"PATCH 343 — Data Completion Sprint 330c ({len(CARS)} Einträge)")
    print("=" * 60)

    with open(AUTOS, encoding="utf-8") as f:
        d = json.load(f)

    totals = {"neu": 0, "skip": 0}

    for car in CARS:
        n = car["key"]
        added = dedup(d["auto_ps"]["items"], n, car["ps"])
        if added == 0:
            totals["skip"] += 1
            print(f"  ~ SKIP {n}")
            continue
        dedup(d["auto_vmax"]["items"],  n, car["vmax"])
        dedup(d["auto_accel"]["items"], n, car["accel"])
        dedup(d["auto_bj"]["items"],    n, car["bj"])
        if not car["ev"]:
            dedup(d["auto_ccm"]["items"], n, car["ccm"])
        totals["neu"] += 1
        print(f"  + {n}")

    with open(AUTOS, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

    print(f"\n  Neu: {totals['neu']} | Duplikate übersprungen: {totals['skip']}")
    for k in ("auto_ps", "auto_vmax", "auto_accel", "auto_bj"):
        print(f"  {k}: gesamt {len(d[k]['items'])}")
    print(f"  auto_ccm: gesamt {len(d['auto_ccm']['items'])} (EVs ausgeschlossen)")

    print("\n  Build …")
    if run([sys.executable, "gen.py"]) != 0:
        sys.exit(1)
    print("  Verify …")
    if run([sys.executable, "verify.py"]) != 0:
        sys.exit(1)
    run([sys.executable, "validate_content.py"])
    run([sys.executable, "post_phase.py",
         "--phase", "343",
         "--patch", "patches/patch_343_data_completion_c.py",
         "--summary",
         "Data Completion Sprint 330c: BMW 1er/7er/X5, MB S/A/SL/G-Klasse, "
         "Audi A8/TT, Porsche Boxster/Cayenne, Opel Manta/Calibra, "
         "Ford Fiesta/Focus/Capri/Sierra, Volvo 240/V70/XC90, Saab, Smart W453, Mini"])
