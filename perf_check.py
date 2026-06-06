#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeoQuest — Performance-/Groessen-Check (Phase 521)
Prueft die ausgelieferte GeoQuest.html und den Service-Worker-Precache auf Groesse.
Schwellen (anpassbar): WARN ab 6.5 MB, FAIL ab 9.0 MB HTML; SW-Precache WARN ab 9 MB.
Exit 1 bei FAIL.  ->  python3 perf_check.py
"""
import os, re, sys

HERE = os.path.dirname(__file__)
def size(path):
    p = os.path.join(HERE, path)
    return os.path.getsize(p) if os.path.exists(p) else 0

def mb(n): return n / (1024*1024)

html = size('GeoQuest.html')
idx  = size('index.html')
sw   = size('sw.js')
data_total = sum(size(os.path.join('data', f)) for f in os.listdir(os.path.join(HERE, 'data'))) if os.path.isdir(os.path.join(HERE,'data')) else 0

# Inline-Script-Bytes der HTML (grobe JS-Last)
js_bytes = 0
try:
    h = open(os.path.join(HERE, 'GeoQuest.html'), encoding='utf-8').read()
    for m in re.finditer(r'<script\b([^>]*)>([\s\S]*?)</script>', h, re.I):
        if 'src=' not in m.group(1):
            js_bytes += len(m.group(2).encode('utf-8'))
except OSError:
    pass

# SW-Precache: groesste Datei im Precache-Array
sw_files = []
try:
    s = open(os.path.join(HERE, 'sw.js'), encoding='utf-8').read()
    m = re.search(r'\[([^\]]*)\]', s)
    if m:
        sw_files = re.findall(r'["\']([^"\']+)["\']', m.group(1))
except OSError:
    pass
sw_precache_est = sum(size(f.lstrip('./')) for f in sw_files if not f.startswith('http'))

WARN_HTML, FAIL_HTML = 6.5, 9.0
WARN_SW = 9.0

fails, warns = [], []
print('=' * 58)
print(' GeoQuest Performance-/Groessen-Check')
print('=' * 58)
print(f'  GeoQuest.html : {mb(html):5.2f} MB')
print(f'  index.html    : {mb(idx):5.2f} MB')
print(f'  davon Inline-JS: {mb(js_bytes):5.2f} MB')
print(f'  data/ gesamt  : {mb(data_total):5.2f} MB')
print(f'  sw.js         : {mb(sw):5.2f} MB ({len(sw_files)} Precache-Eintraege)')
print(f'  SW-Precache~  : {mb(sw_precache_est):5.2f} MB (lokale Dateien)')

if mb(html) >= FAIL_HTML: fails.append(f'GeoQuest.html {mb(html):.2f} MB >= {FAIL_HTML} MB')
elif mb(html) >= WARN_HTML: warns.append(f'GeoQuest.html {mb(html):.2f} MB >= {WARN_HTML} MB')
if mb(sw_precache_est) >= WARN_SW: warns.append(f'SW-Precache {mb(sw_precache_est):.2f} MB >= {WARN_SW} MB (PWA-Quota-Risiko)')
if idx and abs(idx - html) > 2048: warns.append('index.html weicht von GeoQuest.html ab (Build evtl. nicht kopiert)')

print()
for w in warns: print('  [WARN] ' + w)
for f in fails: print('  [FAIL] ' + f)
if not fails and not warns:
    print('  Alle Groessen im gruenen Bereich.')
print(f"\n Ergebnis: {len(fails)} FAIL | {len(warns)} WARN")
sys.exit(1 if fails else 0)
