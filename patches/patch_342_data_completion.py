#!/usr/bin/env python3
"""
Phase: 342
Date:  2026-06-01
Author: Claude / Andre
Scope: Data Completion Sprint — 50 Jahre EU-Auto-Historie lückenlos

Description:
  Ergänzt für jede Generation (Basis + Top):
  • VW Golf 1–8 (Basismodelle), Polo 1–6, Passat B1–B8
  • Opel Corsa A–F, Kadett D/E, Astra F–L, Vectra A–C, Insignia A/B
  • BMW 3er E21–G20, 5er E12–G30
  • Mercedes C-Klasse W201–W205, E-Klasse W123–W213
  • Audi A3 8L–8Y, A4 B5–B9
  • Peugeot 205–208, Renault Clio I–V, Megane I–IV
  • Fiat Uno + Punto-Generationen, Alfa Romeo 155/156/Giulia
  • EU-Nischen: Škoda Octavia I–IV, K1 Attack, Toroidion, SEAT Ibiza Mk1

Dependencies: Phase 341
Zero-Bug Policy: Kein gen.py-Patch nötig — alle Arrays bereits registriert
"""
import json, os, subprocess, sys

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTOS = os.path.join(ROOT, "data", "autos.json")

# fmt: {"key": Name (Country, Year), "ps", "ccm" (0 für EV), "vmax", "accel", "bj", "ev"}
CARS = [
    # ──────────────────────────────────────────────────────────────────
    # VW GOLF — Basismodelle pro Generation (GTI/R bereits vorhanden)
    # ──────────────────────────────────────────────────────────────────
    {"key": "VW Golf 1 (Deutschland, 1974)",   "ps":  70, "ccm": 1471, "vmax": 157, "accel": 14.0, "bj": 1974, "ev": False},
    {"key": "VW Golf 2 (Deutschland, 1983)",   "ps":  55, "ccm": 1272, "vmax": 152, "accel": 16.5, "bj": 1983, "ev": False},
    {"key": "VW Golf 3 (Deutschland, 1991)",   "ps":  60, "ccm": 1390, "vmax": 163, "accel": 14.6, "bj": 1991, "ev": False},
    {"key": "VW Golf 4 (Deutschland, 1997)",   "ps":  75, "ccm": 1390, "vmax": 175, "accel": 12.9, "bj": 1997, "ev": False},
    {"key": "VW Golf 5 (Deutschland, 2003)",   "ps":  80, "ccm": 1390, "vmax": 178, "accel": 13.7, "bj": 2003, "ev": False},
    {"key": "VW Golf 6 (Deutschland, 2008)",   "ps":  86, "ccm": 1197, "vmax": 182, "accel": 12.3, "bj": 2008, "ev": False},
    {"key": "VW Golf 7 (Deutschland, 2012)",   "ps":  85, "ccm": 1197, "vmax": 185, "accel": 12.3, "bj": 2012, "ev": False},
    {"key": "VW Golf 8 (Deutschland, 2019)",   "ps":  90, "ccm":  999, "vmax": 192, "accel": 11.9, "bj": 2019, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # VW POLO — Generationen 1–6 (Basis + Top)
    # ──────────────────────────────────────────────────────────────────
    {"key": "VW Polo 1 (Deutschland, 1975)",          "ps":  40, "ccm":  895, "vmax": 130, "accel": 22.0, "bj": 1975, "ev": False},
    {"key": "VW Polo 1 Coupe GT (Deutschland, 1979)", "ps":  60, "ccm": 1272, "vmax": 165, "accel": 12.0, "bj": 1979, "ev": False},
    {"key": "VW Polo 2 (Deutschland, 1981)",          "ps":  40, "ccm":  895, "vmax": 130, "accel": 22.0, "bj": 1981, "ev": False},
    {"key": "VW Polo 2 G40 (Deutschland, 1987)",      "ps": 113, "ccm": 1272, "vmax": 180, "accel":  8.5, "bj": 1987, "ev": False},
    {"key": "VW Polo 3 (Deutschland, 1994)",          "ps":  45, "ccm":  999, "vmax": 143, "accel": 18.5, "bj": 1994, "ev": False},
    {"key": "VW Polo 3 GTI 16V (Deutschland, 1998)",  "ps": 125, "ccm": 1598, "vmax": 200, "accel":  8.2, "bj": 1998, "ev": False},
    {"key": "VW Polo 4 (Deutschland, 2001)",          "ps":  54, "ccm": 1198, "vmax": 153, "accel": 17.3, "bj": 2001, "ev": False},
    {"key": "VW Polo 4 GTI (Deutschland, 2006)",      "ps": 150, "ccm": 1798, "vmax": 210, "accel":  7.9, "bj": 2006, "ev": False},
    {"key": "VW Polo 5 (Deutschland, 2009)",          "ps":  60, "ccm": 1198, "vmax": 160, "accel": 15.2, "bj": 2009, "ev": False},
    {"key": "VW Polo 5 GTI (Deutschland, 2010)",      "ps": 180, "ccm": 1390, "vmax": 232, "accel":  6.9, "bj": 2010, "ev": False},
    {"key": "VW Polo 6 (Deutschland, 2017)",          "ps":  65, "ccm":  999, "vmax": 170, "accel": 14.4, "bj": 2017, "ev": False},
    {"key": "VW Polo 6 GTI (Deutschland, 2018)",      "ps": 200, "ccm": 1984, "vmax": 230, "accel":  6.7, "bj": 2018, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # VW PASSAT — Generationen B1–B8 (Basis + Top)
    # ──────────────────────────────────────────────────────────────────
    {"key": "VW Passat B1 (Deutschland, 1973)",            "ps":  55, "ccm": 1297, "vmax": 148, "accel": 15.5, "bj": 1973, "ev": False},
    {"key": "VW Passat B1 TS (Deutschland, 1975)",         "ps":  85, "ccm": 1471, "vmax": 170, "accel": 11.5, "bj": 1975, "ev": False},
    {"key": "VW Passat B2 (Deutschland, 1980)",            "ps":  60, "ccm": 1272, "vmax": 155, "accel": 15.0, "bj": 1980, "ev": False},
    {"key": "VW Passat B2 GLI 5-Zyl (Deutschland, 1985)", "ps": 136, "ccm": 2144, "vmax": 205, "accel":  9.0, "bj": 1985, "ev": False},
    {"key": "VW Passat B3 (Deutschland, 1988)",            "ps":  72, "ccm": 1595, "vmax": 170, "accel": 13.5, "bj": 1988, "ev": False},
    {"key": "VW Passat B3 G60 Syncro (Deutschland, 1989)","ps": 160, "ccm": 1781, "vmax": 210, "accel":  8.4, "bj": 1989, "ev": False},
    {"key": "VW Passat B4 (Deutschland, 1993)",            "ps": 101, "ccm": 1595, "vmax": 185, "accel": 11.3, "bj": 1993, "ev": False},
    {"key": "VW Passat B4 VR6 (Deutschland, 1994)",        "ps": 174, "ccm": 2792, "vmax": 225, "accel":  8.4, "bj": 1994, "ev": False},
    {"key": "VW Passat B5 (Deutschland, 1996)",            "ps": 101, "ccm": 1595, "vmax": 192, "accel": 11.6, "bj": 1996, "ev": False},
    {"key": "VW Passat B5 W8 (Deutschland, 2001)",         "ps": 275, "ccm": 3999, "vmax": 250, "accel":  6.6, "bj": 2001, "ev": False},
    {"key": "VW Passat B6 (Deutschland, 2005)",            "ps": 102, "ccm": 1595, "vmax": 195, "accel": 11.0, "bj": 2005, "ev": False},
    {"key": "VW Passat B6 R36 (Deutschland, 2007)",        "ps": 300, "ccm": 3597, "vmax": 250, "accel":  5.6, "bj": 2007, "ev": False},
    {"key": "VW Passat B7 (Deutschland, 2010)",            "ps": 122, "ccm": 1390, "vmax": 200, "accel":  9.7, "bj": 2010, "ev": False},
    {"key": "VW Passat B7 V6 (Deutschland, 2011)",         "ps": 300, "ccm": 3597, "vmax": 250, "accel":  5.6, "bj": 2011, "ev": False},
    {"key": "VW Passat B8 (Deutschland, 2014)",            "ps": 125, "ccm": 1395, "vmax": 207, "accel":  9.6, "bj": 2014, "ev": False},
    {"key": "VW Passat B8 2.0 TSI (Deutschland, 2019)",   "ps": 272, "ccm": 1984, "vmax": 250, "accel":  5.9, "bj": 2019, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # OPEL CORSA — Generationen A–F
    # ──────────────────────────────────────────────────────────────────
    {"key": "Opel Corsa A (Deutschland, 1982)",      "ps":  55, "ccm": 1196, "vmax": 148, "accel": 15.0, "bj": 1982, "ev": False},
    {"key": "Opel Corsa A GSi (Deutschland, 1987)",  "ps": 100, "ccm": 1598, "vmax": 185, "accel":  9.5, "bj": 1987, "ev": False},
    {"key": "Opel Corsa B (Deutschland, 1993)",      "ps":  45, "ccm": 1196, "vmax": 145, "accel": 18.0, "bj": 1993, "ev": False},
    {"key": "Opel Corsa B GSi (Deutschland, 1995)",  "ps": 106, "ccm": 1598, "vmax": 193, "accel":  9.3, "bj": 1995, "ev": False},
    {"key": "Opel Corsa C (Deutschland, 2000)",      "ps":  58, "ccm":  973, "vmax": 153, "accel": 15.9, "bj": 2000, "ev": False},
    {"key": "Opel Corsa C OPC (Deutschland, 2003)",  "ps": 180, "ccm": 1998, "vmax": 225, "accel":  7.0, "bj": 2003, "ev": False},
    {"key": "Opel Corsa D (Deutschland, 2006)",      "ps":  60, "ccm":  998, "vmax": 158, "accel": 14.9, "bj": 2006, "ev": False},
    # Corsa D OPC (2007) — bereits vorhanden als "Opel Corsa OPC (Deutschland, 2007)"
    {"key": "Opel Corsa E (Deutschland, 2014)",      "ps":  90, "ccm":  999, "vmax": 183, "accel": 11.9, "bj": 2014, "ev": False},
    {"key": "Opel Corsa E OPC (Deutschland, 2015)",  "ps": 207, "ccm": 1598, "vmax": 230, "accel":  6.8, "bj": 2015, "ev": False},
    {"key": "Opel Corsa F (Deutschland, 2019)",      "ps": 100, "ccm": 1199, "vmax": 190, "accel": 10.1, "bj": 2019, "ev": False},
    {"key": "Opel Corsa-e (Deutschland, 2020)",      "ps": 136, "ccm":    0, "vmax": 150, "accel":  8.1, "bj": 2020, "ev": True},

    # ──────────────────────────────────────────────────────────────────
    # OPEL KADETT D/E → ASTRA F–L
    # ──────────────────────────────────────────────────────────────────
    {"key": "Opel Kadett D (Deutschland, 1979)",         "ps":  55, "ccm": 1196, "vmax": 148, "accel": 16.5, "bj": 1979, "ev": False},
    {"key": "Opel Kadett D SR (Deutschland, 1982)",      "ps":  90, "ccm": 1598, "vmax": 178, "accel": 10.5, "bj": 1982, "ev": False},
    {"key": "Opel Kadett E (Deutschland, 1984)",         "ps":  60, "ccm": 1297, "vmax": 158, "accel": 14.5, "bj": 1984, "ev": False},
    # Kadett E GSi (1987) — bereits vorhanden
    {"key": "Opel Astra F (Deutschland, 1991)",          "ps":  60, "ccm": 1389, "vmax": 162, "accel": 14.8, "bj": 1991, "ev": False},
    {"key": "Opel Astra F GSi 16V (Deutschland, 1992)",  "ps": 150, "ccm": 1998, "vmax": 213, "accel":  7.8, "bj": 1992, "ev": False},
    {"key": "Opel Astra G (Deutschland, 1998)",          "ps":  90, "ccm": 1389, "vmax": 178, "accel": 11.5, "bj": 1998, "ev": False},
    {"key": "Opel Astra G OPC (Deutschland, 2002)",      "ps": 192, "ccm": 1998, "vmax": 230, "accel":  7.3, "bj": 2002, "ev": False},
    {"key": "Opel Astra H (Deutschland, 2004)",          "ps":  90, "ccm": 1389, "vmax": 178, "accel": 12.0, "bj": 2004, "ev": False},
    {"key": "Opel Astra H OPC (Deutschland, 2005)",      "ps": 240, "ccm": 1998, "vmax": 237, "accel":  6.3, "bj": 2005, "ev": False},
    {"key": "Opel Astra J (Deutschland, 2009)",          "ps": 100, "ccm": 1364, "vmax": 188, "accel": 11.7, "bj": 2009, "ev": False},
    {"key": "Opel Astra J OPC (Deutschland, 2012)",      "ps": 280, "ccm": 1998, "vmax": 250, "accel":  5.9, "bj": 2012, "ev": False},
    {"key": "Opel Astra K (Deutschland, 2015)",          "ps": 105, "ccm":  999, "vmax": 190, "accel": 11.9, "bj": 2015, "ev": False},
    {"key": "Opel Astra K GSi (Deutschland, 2017)",      "ps": 200, "ccm": 1598, "vmax": 235, "accel":  7.0, "bj": 2017, "ev": False},
    {"key": "Opel Astra L (Deutschland, 2021)",          "ps": 110, "ccm": 1199, "vmax": 190, "accel": 10.7, "bj": 2021, "ev": False},
    {"key": "Opel Astra L GSe (Deutschland, 2023)",      "ps": 225, "ccm": 1598, "vmax": 235, "accel":  7.5, "bj": 2023, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # OPEL VECTRA / INSIGNIA
    # ──────────────────────────────────────────────────────────────────
    {"key": "Opel Vectra A (Deutschland, 1988)",         "ps":  75, "ccm": 1598, "vmax": 170, "accel": 13.5, "bj": 1988, "ev": False},
    {"key": "Opel Vectra A GSi 16V (Deutschland, 1989)", "ps": 150, "ccm": 1998, "vmax": 213, "accel":  7.9, "bj": 1989, "ev": False},
    {"key": "Opel Vectra B (Deutschland, 1995)",         "ps": 100, "ccm": 1598, "vmax": 185, "accel": 11.5, "bj": 1995, "ev": False},
    {"key": "Opel Vectra B V6 (Deutschland, 1999)",      "ps": 170, "ccm": 2498, "vmax": 228, "accel":  8.1, "bj": 1999, "ev": False},
    {"key": "Opel Vectra C (Deutschland, 2002)",         "ps": 122, "ccm": 1796, "vmax": 205, "accel": 10.9, "bj": 2002, "ev": False},
    {"key": "Opel Vectra C OPC (Deutschland, 2003)",     "ps": 255, "ccm": 2792, "vmax": 250, "accel":  6.2, "bj": 2003, "ev": False},
    {"key": "Opel Insignia A (Deutschland, 2008)",       "ps": 180, "ccm": 1598, "vmax": 220, "accel":  8.8, "bj": 2008, "ev": False},
    {"key": "Opel Insignia A OPC (Deutschland, 2009)",   "ps": 325, "ccm": 2792, "vmax": 250, "accel":  5.9, "bj": 2009, "ev": False},
    {"key": "Opel Insignia B (Deutschland, 2017)",       "ps": 140, "ccm": 1490, "vmax": 205, "accel":  9.4, "bj": 2017, "ev": False},
    {"key": "Opel Insignia B GSi (Deutschland, 2018)",   "ps": 260, "ccm": 1998, "vmax": 250, "accel":  7.0, "bj": 2018, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # BMW 3er — E21, E30, E36, E46, E90, F30, G20
    # ──────────────────────────────────────────────────────────────────
    {"key": "BMW 316 E21 (Deutschland, 1975)",   "ps":  90, "ccm": 1573, "vmax": 165, "accel": 13.0, "bj": 1975, "ev": False},
    {"key": "BMW 323i E21 (Deutschland, 1977)",  "ps": 143, "ccm": 2315, "vmax": 200, "accel":  9.0, "bj": 1977, "ev": False},
    {"key": "BMW 316 E30 (Deutschland, 1982)",   "ps":  90, "ccm": 1573, "vmax": 165, "accel": 12.5, "bj": 1982, "ev": False},
    # BMW M3 E30 (1986) — bereits vorhanden
    {"key": "BMW 316i E36 (Deutschland, 1990)",  "ps": 102, "ccm": 1596, "vmax": 190, "accel": 11.5, "bj": 1990, "ev": False},
    {"key": "BMW M3 E36 (Deutschland, 1992)",    "ps": 286, "ccm": 2990, "vmax": 250, "accel":  5.5, "bj": 1992, "ev": False},
    {"key": "BMW 316i E46 (Deutschland, 1998)",  "ps": 115, "ccm": 1596, "vmax": 195, "accel": 11.5, "bj": 1998, "ev": False},
    {"key": "BMW M3 E46 (Deutschland, 2000)",    "ps": 343, "ccm": 3246, "vmax": 250, "accel":  4.9, "bj": 2000, "ev": False},
    {"key": "BMW 316i E90 (Deutschland, 2005)",  "ps": 115, "ccm": 1596, "vmax": 198, "accel": 11.8, "bj": 2005, "ev": False},
    # BMW M3 E92 (2008) — bereits vorhanden
    {"key": "BMW 316i F30 (Deutschland, 2012)",  "ps": 136, "ccm": 1598, "vmax": 210, "accel":  9.7, "bj": 2012, "ev": False},
    {"key": "BMW M3 F80 (Deutschland, 2014)",    "ps": 431, "ccm": 2979, "vmax": 250, "accel":  4.1, "bj": 2014, "ev": False},
    {"key": "BMW 318i G20 (Deutschland, 2018)",  "ps": 156, "ccm": 1499, "vmax": 215, "accel":  8.9, "bj": 2018, "ev": False},
    {"key": "BMW M3 G80 (Deutschland, 2021)",    "ps": 480, "ccm": 2993, "vmax": 290, "accel":  3.9, "bj": 2021, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # BMW 5er — E12, E28, E34, E39, E60, F10, G30
    # ──────────────────────────────────────────────────────────────────
    {"key": "BMW 518 E12 (Deutschland, 1972)",   "ps":  90, "ccm": 1766, "vmax": 170, "accel": 14.0, "bj": 1972, "ev": False},
    {"key": "BMW 528i E12 (Deutschland, 1977)",  "ps": 165, "ccm": 2788, "vmax": 200, "accel":  9.5, "bj": 1977, "ev": False},
    {"key": "BMW 518 E28 (Deutschland, 1981)",   "ps":  90, "ccm": 1766, "vmax": 170, "accel": 14.5, "bj": 1981, "ev": False},
    {"key": "BMW M535i E28 (Deutschland, 1985)", "ps": 218, "ccm": 3453, "vmax": 230, "accel":  7.0, "bj": 1985, "ev": False},
    {"key": "BMW 518i E34 (Deutschland, 1988)",  "ps": 113, "ccm": 1796, "vmax": 190, "accel": 12.0, "bj": 1988, "ev": False},
    # BMW M5 E34 (1988) — bereits vorhanden
    {"key": "BMW 520i E39 (Deutschland, 1996)",  "ps": 150, "ccm": 1991, "vmax": 215, "accel": 10.0, "bj": 1996, "ev": False},
    {"key": "BMW M5 E39 (Deutschland, 1998)",    "ps": 400, "ccm": 4941, "vmax": 250, "accel":  5.3, "bj": 1998, "ev": False},
    {"key": "BMW 520i E60 (Deutschland, 2003)",  "ps": 170, "ccm": 2171, "vmax": 228, "accel":  9.4, "bj": 2003, "ev": False},
    {"key": "BMW M5 E60 (Deutschland, 2004)",    "ps": 507, "ccm": 4999, "vmax": 250, "accel":  4.7, "bj": 2004, "ev": False},
    {"key": "BMW 520i F10 (Deutschland, 2010)",  "ps": 184, "ccm": 1997, "vmax": 235, "accel":  8.0, "bj": 2010, "ev": False},
    {"key": "BMW M5 F10 (Deutschland, 2011)",    "ps": 560, "ccm": 4395, "vmax": 250, "accel":  4.4, "bj": 2011, "ev": False},
    {"key": "BMW 520i G30 (Deutschland, 2017)",  "ps": 184, "ccm": 1998, "vmax": 235, "accel":  7.8, "bj": 2017, "ev": False},
    {"key": "BMW M5 F90 (Deutschland, 2018)",    "ps": 600, "ccm": 4395, "vmax": 250, "accel":  3.4, "bj": 2018, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # MERCEDES C-KLASSE — W201 (190er), W202, W203, W204, W205
    # ──────────────────────────────────────────────────────────────────
    {"key": "Mercedes-Benz 190 W201 (Deutschland, 1982)",       "ps":  90, "ccm": 1797, "vmax": 185, "accel": 12.5, "bj": 1982, "ev": False},
    # 190E 2.3-16 (1984) — bereits vorhanden
    {"key": "Mercedes-Benz C 180 W202 (Deutschland, 1993)",     "ps": 122, "ccm": 1799, "vmax": 206, "accel": 11.5, "bj": 1993, "ev": False},
    {"key": "Mercedes-Benz C 36 AMG W202 (Deutschland, 1994)",  "ps": 280, "ccm": 3606, "vmax": 250, "accel":  6.1, "bj": 1994, "ev": False},
    {"key": "Mercedes-Benz C 180 W203 (Deutschland, 2000)",     "ps": 143, "ccm": 1796, "vmax": 213, "accel": 10.2, "bj": 2000, "ev": False},
    {"key": "Mercedes-Benz C 32 AMG W203 (Deutschland, 2001)",  "ps": 354, "ccm": 3199, "vmax": 250, "accel":  5.2, "bj": 2001, "ev": False},
    {"key": "Mercedes-Benz C 180 W204 (Deutschland, 2007)",     "ps": 156, "ccm": 1597, "vmax": 217, "accel":  9.2, "bj": 2007, "ev": False},
    # C63 AMG W204 (2006) — bereits vorhanden
    {"key": "Mercedes-Benz C 180 W205 (Deutschland, 2014)",     "ps": 156, "ccm": 1595, "vmax": 218, "accel":  9.4, "bj": 2014, "ev": False},
    {"key": "Mercedes-Benz C 63 S AMG W205 (Deutschland, 2015)","ps": 510, "ccm": 3982, "vmax": 290, "accel":  3.9, "bj": 2015, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # MERCEDES E-KLASSE — W123, W124, W210, W211, W212, W213
    # ──────────────────────────────────────────────────────────────────
    {"key": "Mercedes-Benz 230 E W123 (Deutschland, 1976)",     "ps": 136, "ccm": 2307, "vmax": 195, "accel": 10.5, "bj": 1976, "ev": False},
    {"key": "Mercedes-Benz 280 E W123 (Deutschland, 1977)",     "ps": 185, "ccm": 2746, "vmax": 210, "accel":  9.5, "bj": 1977, "ev": False},
    {"key": "Mercedes-Benz 200 E W124 (Deutschland, 1984)",     "ps": 118, "ccm": 1997, "vmax": 187, "accel": 12.0, "bj": 1984, "ev": False},
    # 500E W124 (1992) — bereits vorhanden
    {"key": "Mercedes-Benz E 200 W210 (Deutschland, 1995)",     "ps": 136, "ccm": 1998, "vmax": 210, "accel": 11.0, "bj": 1995, "ev": False},
    {"key": "Mercedes-Benz E 55 AMG W210 (Deutschland, 1997)",  "ps": 354, "ccm": 5439, "vmax": 250, "accel":  5.7, "bj": 1997, "ev": False},
    {"key": "Mercedes-Benz E 200 W211 (Deutschland, 2002)",     "ps": 163, "ccm": 1796, "vmax": 220, "accel": 10.8, "bj": 2002, "ev": False},
    {"key": "Mercedes-Benz E 55 AMG W211 (Deutschland, 2002)",  "ps": 476, "ccm": 5439, "vmax": 250, "accel":  4.7, "bj": 2002, "ev": False},
    {"key": "Mercedes-Benz E 200 W212 (Deutschland, 2009)",     "ps": 184, "ccm": 1796, "vmax": 230, "accel":  9.2, "bj": 2009, "ev": False},
    # E63 AMG T-Modell (2009) — bereits vorhanden
    {"key": "Mercedes-Benz E 200 W213 (Deutschland, 2016)",     "ps": 184, "ccm": 1991, "vmax": 237, "accel":  8.5, "bj": 2016, "ev": False},
    {"key": "Mercedes-Benz E 63 S AMG W213 (Deutschland, 2017)","ps": 612, "ccm": 3982, "vmax": 300, "accel":  3.4, "bj": 2017, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # AUDI A3 — 8L, 8P, 8V, 8Y
    # ──────────────────────────────────────────────────────────────────
    {"key": "Audi A3 8L (Deutschland, 1996)",   "ps": 101, "ccm": 1595, "vmax": 195, "accel": 10.5, "bj": 1996, "ev": False},
    {"key": "Audi S3 8L (Deutschland, 1999)",   "ps": 210, "ccm": 1781, "vmax": 250, "accel":  6.6, "bj": 1999, "ev": False},
    {"key": "Audi A3 8P (Deutschland, 2003)",   "ps": 102, "ccm": 1595, "vmax": 190, "accel": 11.5, "bj": 2003, "ev": False},
    {"key": "Audi RS3 8P (Deutschland, 2011)",  "ps": 340, "ccm": 2480, "vmax": 250, "accel":  4.6, "bj": 2011, "ev": False},
    {"key": "Audi A3 8V (Deutschland, 2012)",   "ps": 105, "ccm": 1197, "vmax": 195, "accel": 11.5, "bj": 2012, "ev": False},
    {"key": "Audi RS3 8V (Deutschland, 2015)",  "ps": 367, "ccm": 2480, "vmax": 280, "accel":  4.3, "bj": 2015, "ev": False},
    {"key": "Audi A3 8Y (Deutschland, 2020)",   "ps": 110, "ccm":  999, "vmax": 200, "accel": 11.0, "bj": 2020, "ev": False},
    {"key": "Audi RS3 8Y (Deutschland, 2021)",  "ps": 400, "ccm": 2480, "vmax": 290, "accel":  3.8, "bj": 2021, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # AUDI A4 — B5, B6, B7, B8, B9
    # ──────────────────────────────────────────────────────────────────
    {"key": "Audi A4 B5 (Deutschland, 1994)",   "ps": 101, "ccm": 1595, "vmax": 195, "accel": 11.3, "bj": 1994, "ev": False},
    {"key": "Audi RS4 B5 (Deutschland, 2000)",  "ps": 380, "ccm": 2671, "vmax": 250, "accel":  4.9, "bj": 2000, "ev": False},
    {"key": "Audi A4 B6 (Deutschland, 2000)",   "ps": 102, "ccm": 1595, "vmax": 192, "accel": 12.2, "bj": 2000, "ev": False},
    {"key": "Audi RS4 B6 (Deutschland, 2004)",  "ps": 420, "ccm": 4163, "vmax": 250, "accel":  4.9, "bj": 2004, "ev": False},
    {"key": "Audi A4 B7 (Deutschland, 2005)",   "ps": 102, "ccm": 1595, "vmax": 192, "accel": 12.2, "bj": 2005, "ev": False},
    {"key": "Audi RS4 B7 (Deutschland, 2005)",  "ps": 420, "ccm": 4163, "vmax": 250, "accel":  4.8, "bj": 2005, "ev": False},
    {"key": "Audi A4 B8 (Deutschland, 2007)",   "ps": 160, "ccm": 1798, "vmax": 225, "accel":  9.4, "bj": 2007, "ev": False},
    {"key": "Audi RS4 B8 (Deutschland, 2012)",  "ps": 450, "ccm": 4163, "vmax": 250, "accel":  4.7, "bj": 2012, "ev": False},
    {"key": "Audi A4 B9 (Deutschland, 2015)",   "ps": 150, "ccm": 1395, "vmax": 221, "accel":  9.3, "bj": 2015, "ev": False},
    {"key": "Audi RS4 B9 (Deutschland, 2017)",  "ps": 450, "ccm": 2894, "vmax": 280, "accel":  4.1, "bj": 2017, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # PEUGEOT 205, 206, 207, 208
    # ──────────────────────────────────────────────────────────────────
    {"key": "Peugeot 205 (Frankreich, 1983)",         "ps":  45, "ccm":  954, "vmax": 143, "accel": 18.0, "bj": 1983, "ev": False},
    # 205 GTI (1984) — bereits vorhanden
    {"key": "Peugeot 206 (Frankreich, 1998)",         "ps":  60, "ccm": 1124, "vmax": 160, "accel": 14.9, "bj": 1998, "ev": False},
    {"key": "Peugeot 206 GTI 2.0 (Frankreich, 1999)", "ps": 136, "ccm": 1997, "vmax": 210, "accel":  8.3, "bj": 1999, "ev": False},
    {"key": "Peugeot 207 (Frankreich, 2006)",         "ps":  75, "ccm": 1360, "vmax": 170, "accel": 13.9, "bj": 2006, "ev": False},
    {"key": "Peugeot 207 GTI (Frankreich, 2007)",     "ps": 175, "ccm": 1598, "vmax": 225, "accel":  7.1, "bj": 2007, "ev": False},
    {"key": "Peugeot 208 (Frankreich, 2012)",         "ps":  68, "ccm":  999, "vmax": 166, "accel": 14.9, "bj": 2012, "ev": False},
    {"key": "Peugeot 208 GTI (Frankreich, 2013)",     "ps": 208, "ccm": 1598, "vmax": 240, "accel":  6.5, "bj": 2013, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # RENAULT CLIO — I, II, III, IV, V
    # ──────────────────────────────────────────────────────────────────
    {"key": "Renault Clio I (Frankreich, 1990)",              "ps":  55, "ccm": 1171, "vmax": 155, "accel": 15.5, "bj": 1990, "ev": False},
    {"key": "Renault Clio I Williams (Frankreich, 1993)",     "ps": 150, "ccm": 1998, "vmax": 214, "accel":  7.8, "bj": 1993, "ev": False},
    {"key": "Renault Clio II (Frankreich, 1998)",             "ps":  58, "ccm": 1149, "vmax": 157, "accel": 15.2, "bj": 1998, "ev": False},
    {"key": "Renault Clio II RS (Frankreich, 2001)",          "ps": 172, "ccm": 1998, "vmax": 220, "accel":  7.5, "bj": 2001, "ev": False},
    {"key": "Renault Clio III (Frankreich, 2005)",            "ps":  75, "ccm": 1149, "vmax": 167, "accel": 14.0, "bj": 2005, "ev": False},
    {"key": "Renault Clio III RS 197 (Frankreich, 2006)",     "ps": 197, "ccm": 1998, "vmax": 215, "accel":  6.9, "bj": 2006, "ev": False},
    {"key": "Renault Clio IV (Frankreich, 2012)",             "ps":  75, "ccm": 1149, "vmax": 173, "accel": 13.8, "bj": 2012, "ev": False},
    {"key": "Renault Clio IV RS 220 Trophy (Frankreich, 2015)","ps": 220, "ccm": 1618, "vmax": 240, "accel":  6.6, "bj": 2015, "ev": False},
    {"key": "Renault Clio V (Frankreich, 2019)",              "ps":  90, "ccm":  999, "vmax": 183, "accel": 11.0, "bj": 2019, "ev": False},
    {"key": "Renault Clio V RS Line (Frankreich, 2020)",      "ps": 131, "ccm": 1333, "vmax": 204, "accel":  9.0, "bj": 2020, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # RENAULT MEGANE — I, II, III, IV
    # ──────────────────────────────────────────────────────────────────
    {"key": "Renault Megane I (Frankreich, 1995)",              "ps":  75, "ccm": 1390, "vmax": 170, "accel": 13.5, "bj": 1995, "ev": False},
    {"key": "Renault Megane I RS 2.0 (Frankreich, 1999)",       "ps": 147, "ccm": 1998, "vmax": 210, "accel":  8.2, "bj": 1999, "ev": False},
    {"key": "Renault Megane II (Frankreich, 2002)",             "ps":  98, "ccm": 1390, "vmax": 182, "accel": 12.0, "bj": 2002, "ev": False},
    {"key": "Renault Megane II RS 225 (Frankreich, 2004)",      "ps": 225, "ccm": 1998, "vmax": 235, "accel":  6.5, "bj": 2004, "ev": False},
    {"key": "Renault Megane III (Frankreich, 2008)",            "ps": 100, "ccm": 1397, "vmax": 188, "accel": 11.8, "bj": 2008, "ev": False},
    {"key": "Renault Megane III RS Trophy (Frankreich, 2014)",  "ps": 275, "ccm": 1998, "vmax": 255, "accel":  5.8, "bj": 2014, "ev": False},
    {"key": "Renault Megane IV (Frankreich, 2016)",             "ps": 100, "ccm": 1197, "vmax": 192, "accel": 11.5, "bj": 2016, "ev": False},
    # Megane IV RS Trophy-R (2019) — bereits vorhanden

    # ──────────────────────────────────────────────────────────────────
    # FIAT UNO + PUNTO-GENERATIONEN
    # ──────────────────────────────────────────────────────────────────
    {"key": "Fiat Uno (Italien, 1983)",               "ps":  45, "ccm":  999, "vmax": 136, "accel": 17.0, "bj": 1983, "ev": False},
    {"key": "Fiat Uno Turbo i.e. (Italien, 1985)",    "ps": 105, "ccm": 1301, "vmax": 195, "accel":  7.7, "bj": 1985, "ev": False},
    {"key": "Fiat Punto Mk1 (Italien, 1993)",         "ps":  54, "ccm": 1108, "vmax": 150, "accel": 15.5, "bj": 1993, "ev": False},
    {"key": "Fiat Punto GT (Italien, 1994)",          "ps": 133, "ccm": 1372, "vmax": 202, "accel":  7.8, "bj": 1994, "ev": False},
    {"key": "Fiat Punto Mk2 (Italien, 1999)",         "ps":  60, "ccm": 1242, "vmax": 158, "accel": 13.9, "bj": 1999, "ev": False},
    {"key": "Fiat Punto HGT Abarth (Italien, 2002)",  "ps": 130, "ccm": 1747, "vmax": 209, "accel":  8.0, "bj": 2002, "ev": False},
    {"key": "Fiat Grande Punto (Italien, 2005)",      "ps":  65, "ccm": 1242, "vmax": 162, "accel": 14.4, "bj": 2005, "ev": False},
    {"key": "Fiat Grande Punto Abarth (Italien, 2007)","ps": 155, "ccm": 1368, "vmax": 218, "accel":  7.9, "bj": 2007, "ev": False},

    # ──────────────────────────────────────────────────────────────────
    # ALFA ROMEO 155, 156, GIULIA
    # ──────────────────────────────────────────────────────────────────
    {"key": "Alfa Romeo 155 1.8 TS (Italien, 1992)",  "ps": 129, "ccm": 1747, "vmax": 203, "accel":  9.8, "bj": 1992, "ev": False},
    {"key": "Alfa Romeo 155 Q4 (Italien, 1992)",      "ps": 190, "ccm": 1995, "vmax": 230, "accel":  7.0, "bj": 1992, "ev": False},
    {"key": "Alfa Romeo 156 1.6 TS (Italien, 1997)",  "ps": 120, "ccm": 1598, "vmax": 200, "accel": 11.5, "bj": 1997, "ev": False},
    {"key": "Alfa Romeo 156 GTA (Italien, 2002)",     "ps": 250, "ccm": 3179, "vmax": 250, "accel":  6.3, "bj": 2002, "ev": False},
    {"key": "Alfa Romeo Giulia 2.0T (Italien, 2016)", "ps": 200, "ccm": 1995, "vmax": 237, "accel":  6.6, "bj": 2016, "ev": False},
    # Giulia Quadrifoglio — bereits vorhanden

    # ──────────────────────────────────────────────────────────────────
    # EU NISCHEN
    # ──────────────────────────────────────────────────────────────────
    # Slowakei — K1 Attack Silhouette Racecar
    {"key": "K1 Attack (Slowakei, 2003)",          "ps": 125, "ccm":  998, "vmax": 200, "accel":  5.9, "bj": 2003, "ev": False},
    # Finnland — Toroidion 1MW Concept EV
    {"key": "Toroidion 1MW (Finnland, 2015)",      "ps":1360, "ccm":    0, "vmax": 400, "accel":  2.5, "bj": 2015, "ev": True},
    # Norwegen — Buddy Electric
    {"key": "Buddy Electric (Norwegen, 2008)",     "ps":  13, "ccm":    0, "vmax":  80, "accel": 15.0, "bj": 2008, "ev": True},
    # Ungarn — Puli X3 Range Extender EV
    {"key": "Puli X3 (Ungarn, 2012)",              "ps": 160, "ccm":    0, "vmax": 200, "accel":  7.5, "bj": 2012, "ev": True},
    # Spanien — SEAT Ibiza Mk1
    {"key": "SEAT Ibiza Mk1 (Spanien, 1984)",      "ps":  63, "ccm": 1193, "vmax": 155, "accel": 14.5, "bj": 1984, "ev": False},
    # Tschechien — Škoda Octavia I–IV
    {"key": "Škoda Octavia I (Tschechien, 1996)",  "ps":  68, "ccm": 1390, "vmax": 163, "accel": 14.7, "bj": 1996, "ev": False},
    {"key": "Škoda Octavia I RS (Tschechien, 2001)","ps": 180, "ccm": 1781, "vmax": 232, "accel":  7.3, "bj": 2001, "ev": False},
    {"key": "Škoda Octavia II (Tschechien, 2004)", "ps":  75, "ccm": 1390, "vmax": 170, "accel": 13.5, "bj": 2004, "ev": False},
    {"key": "Škoda Octavia II RS (Tschechien, 2006)","ps":200, "ccm": 1984, "vmax": 243, "accel":  7.0, "bj": 2006, "ev": False},
    {"key": "Škoda Octavia III (Tschechien, 2013)","ps":  85, "ccm": 1197, "vmax": 183, "accel": 12.3, "bj": 2013, "ev": False},
    {"key": "Škoda Octavia III RS (Tschechien, 2013)","ps":220,"ccm": 1984, "vmax": 247, "accel":  6.6, "bj": 2013, "ev": False},
    {"key": "Škoda Octavia IV (Tschechien, 2020)", "ps": 110, "ccm":  999, "vmax": 194, "accel": 11.1, "bj": 2020, "ev": False},
    {"key": "Škoda Octavia IV RS (Tschechien, 2020)","ps":245,"ccm": 1984, "vmax": 250, "accel":  6.4, "bj": 2020, "ev": False},
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
    print(f"PATCH 342 — Data Completion Sprint ({len(CARS)} Einträge)")
    print("=" * 60)

    with open(AUTOS, encoding="utf-8") as f:
        d = json.load(f)

    totals = {k: 0 for k in ("auto_ps", "auto_vmax", "auto_accel", "auto_ccm", "auto_bj")}
    skipped = 0

    for car in CARS:
        n = car["key"]
        added = dedup(d["auto_ps"]["items"], n, car["ps"])
        if added == 0:
            skipped += 1
            continue
        dedup(d["auto_vmax"]["items"],  n, car["vmax"])
        dedup(d["auto_accel"]["items"], n, car["accel"])
        dedup(d["auto_bj"]["items"],    n, car["bj"])
        if not car["ev"]:
            dedup(d["auto_ccm"]["items"], n, car["ccm"])
        totals["auto_ps"] += 1
        print(f"  + {n}")

    with open(AUTOS, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

    print(f"\n  Neu: {totals['auto_ps']} | Duplikate übersprungen: {skipped}")
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
         "--phase", "342",
         "--patch", "patches/patch_342_data_completion.py",
         "--summary",
         "Data Completion Sprint: Golf/Polo/Passat B1-B8, Corsa/Astra/Vectra, "
         "BMW 3er/5er, MB C/E-Klasse, Audi A3/A4, Peugeot/Renault, Fiat/Alfa, "
         "Škoda Octavia I-IV — 50 Jahre EU-Auto-Historie"])
