#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeoQuest - i18n-HTML-Heuristik (Phase 536): findet hartkodierte deutsche UI-Labels
im gerenderten HTML, die NICHT ueber _tc/${} laufen. Nur WARN/informativ (exit 0)."""
import re, sys, os
HTML = open(os.path.join(os.path.dirname(__file__), 'GeoQuest.html'), encoding='utf-8').read()
ALLOW = {'GeoCoins', 'GeoQuest', 'Stadtverkehr-Experte'}
def is_noise(t):
    if '_tc(' in t or "'+" in t or "+'" in t or 'html+=' in t:
        return True
    if '"' in t or '+' in t or '\\' in t or ';' in t:
        return True
    if re.search(r'(px|rem|rgba?\(|#[0-9a-f]{3,6}|:\s*\d)', t):
        return True
    return False
text_hits = set()
for m in re.finditer(r'>([^<>{}$]{2,44}?[äöüßÄÖÜ][^<>{}$]*?)<', HTML):
    t = m.group(1).strip()
    if not t or t in ALLOW or is_noise(t):
        continue
    if not re.search(r'[A-Za-zÄÖÜäöü]{3,}', t):
        continue
    text_hits.add(t)
DE_WORDS = re.compile(r'\b(und|oder|für|über|Frage|Vorschlag|Einstellungen|Schließen|vorlesen|Beenden|Menü|ändern|Seite|zurücksetzen)\b', re.I)
title_hits = set()
for m in re.finditer(r'title="([^"${}]{2,50})"', HTML):
    t = m.group(1).strip()
    if t in ALLOW:
        continue
    if re.search(r'[äöüßÄÖÜ]', t) or DE_WORDS.search(t):
        title_hits.add(t)
print('=' * 58)
print(' GeoQuest i18n-HTML-Heuristik (informativ)')
print('=' * 58)
print('  Tag-Text mit Umlaut (kein _tc/${}): %d' % len(text_hits))
print('  Deutsche title-Tooltips:            %d' % len(title_hits))
if text_hits:
    print('\n  [WARN] hartkodierter Tag-Text:')
    for s in sorted(text_hits)[:25]:
        print('    ' + repr(s))
if title_hits:
    print('\n  [WARN] deutsche title-Tooltips:')
    for s in sorted(title_hits)[:25]:
        print('    ' + repr(s))
print('\n Ergebnis: %d WARN (informativ, blockiert nicht)' % (len(text_hits) + len(title_hits)))
sys.exit(0)
