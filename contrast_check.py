#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeoQuest — WCAG-Kontrast-Check (Phase 521)
Liest geoquest_css.txt, loest die CSS-Variablen fuer Hell- (:root) und Dunkel-Theme
([data-theme=dark]) auf und prueft die zentralen Text-auf-Flaeche-Paare auf WCAG-Kontrast.
Schwellen: normaler Text >=4.5:1 (FAIL <3.0, WARN <4.5), sekundaerer Text (text3) WARN <3.0.
Exit 1 bei FAIL.  ->  python3 contrast_check.py
"""
import re, sys, os

CSS = open(os.path.join(os.path.dirname(__file__), 'geoquest_css.txt'), encoding='utf-8').read()

def hex_to_rgb(h):
    h = h.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c*2 for c in h)
    if len(h) != 6:
        return None
    try:
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        return None

def _lin(c):
    c = c / 255.0
    return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055) ** 2.4

def luminance(rgb):
    r, g, b = (_lin(x) for x in rgb)
    return 0.2126*r + 0.7152*g + 0.0722*b

def ratio(fg, bg):
    l1, l2 = luminance(fg), luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)

def parse_vars(block):
    """--name:#hex; -> {name:#hex} (nur Farben)."""
    out = {}
    for m in re.finditer(r'(--[a-z0-9-]+)\s*:\s*([^;]+);', block):
        name, val = m.group(1), m.group(2).strip()
        if hex_to_rgb(val):
            out[name] = val
    return out

def theme_block(sel_regex):
    m = re.search(sel_regex + r'\s*\{([^}]*)\}', CSS, re.DOTALL)
    return m.group(1) if m else ''

light = parse_vars(theme_block(r':root'))
dark  = parse_vars(theme_block(r'\[data-theme=dark\]'))

# Zentrale Paare (Vordergrund-Var, Hintergrund-Var, Label, Mindestkontrast)
PAIRS = [
    ('--text',  '--bg',    'Haupttext auf App-Hintergrund', 4.5),
    ('--text',  '--bg2',   'Haupttext auf Flaeche bg2',      4.5),
    ('--text',  '--bg3',   'Haupttext auf Flaeche bg3',      4.5),
    ('--text',  '--qcard', 'Haupttext auf Quizkarte',        4.5),
    ('--text2', '--bg',    'Sekundaertext auf Hintergrund',  4.5),
    ('--text2', '--bg2',   'Sekundaertext auf bg2',          4.5),
    ('--text2', '--qcard', 'Sekundaertext auf Quizkarte',    4.5),
    ('--text3', '--bg',    'Hinweistext auf Hintergrund',    3.0),
    ('--text3', '--bg2',   'Hinweistext auf bg2',            3.0),
    ('--text3', '--qcard', 'Hinweistext auf Quizkarte',      3.0),
    ('--accent','--bg2',   'Akzent auf bg2 (Rahmen/Grosstext)', 1.0),
    ('--accent','--qcard', 'Akzent auf Quizkarte (Rahmen)',     1.0),
]

fails, warns = [], []
print('=' * 58)
print(' GeoQuest WCAG-Kontrast-Check')
print('=' * 58)
for theme_name, vmap in (('Hell', light), ('Dunkel', dark)):
    for fg, bg, label, minr in PAIRS:
        if fg not in vmap or bg not in vmap:
            continue
        r = ratio(hex_to_rgb(vmap[fg]), hex_to_rgb(vmap[bg]))
        tag = 'OK '
        if minr >= 3.0 and r < 3.0:
            tag = 'FAIL'; fails.append((theme_name, label, r, vmap[fg], vmap[bg]))
        elif r < minr:
            tag = 'WARN'; warns.append((theme_name, label, r, vmap[fg], vmap[bg]))
        if tag != 'OK ':
            print(f'  [{tag}] {theme_name:6} {label:32} {r:4.2f}:1  ({vmap[fg]} auf {vmap[bg]})')

print(f"\n Ergebnis: {len(fails)} FAIL (<3.0) | {len(warns)} WARN (<Sollwert)")
if not fails and not warns:
    print(' Alle geprueften Paare bestehen WCAG AA.')
sys.exit(1 if fails else 0)
