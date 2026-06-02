#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase: 449b
Date:  2026-06-02
Scope: Bonus-Modus — Ozeane: Tiefe-Vergleich II => 999. Modus

Modus: hl_ozean_tiefe_klein (Welches Gewässer ist seichter?)
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN  = os.path.join(ROOT, 'gen.py')


def patch(path, edits):
    c = open(path, 'r', encoding='utf-8').read()
    for old, new, tag in edits:
        n = c.count(old)
        assert n == 1, f'Anker "{tag}" count={n} (erwartet 1)'
        c = c.replace(old, new)
        print('  OK  ' + tag)
    open(path, 'w', encoding='utf-8').write(c)


print('\n-- gen.py: +1 Bonus-Modus (hl_ozean_tiefe_klein) --')

I18N_PL_OLD = '"Wie heißt dieses Gewässer?":"Jak nazywa się ten akwen?"},"en":{"Welche Serie startete f'
I18N_PL_NEW = '"Wie heißt dieses Gewässer?":"Jak nazywa się ten akwen?","Welches Gewässer ist seichter?":"Które akwen jest płytsze?"},"en":{"Welche Serie startete f'

I18N_EN_OLD = '"What is this body of water called?"}};\nfuncti'
I18N_EN_NEW = '"What is this body of water called?","Welches Gewässer ist seichter?":"Which body of water is shallower?"}};\nfuncti'

MODES_OLD = '{id:"ws_ozean_atlantik",icon:"\\u{1F30A}",title:"WS: Atlantik",group:"ozeane",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus ATLANTIK!",desc:"Anagramm-R\\u00e4tsel \\u2014 8 Buchstaben",prompt_en:"Form words from ATLANTIK!"},'
MODES_NEW = (
    '{id:"ws_ozean_atlantik",icon:"\\u{1F30A}",title:"WS: Atlantik",group:"ozeane",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus ATLANTIK!",desc:"Anagramm-R\\u00e4tsel \\u2014 8 Buchstaben",prompt_en:"Form words from ATLANTIK!"},\n'
    '    {id:"hl_ozean_tiefe_klein",icon:"\\u{1F30A}",title:"Ozeane: Seichter?",group:"ozeane",prompt:"Welches Gew\\u00e4sser ist seichter?",desc:"Flachstes Gew\\u00e4sser finden",prompt_en:"Which body of water is shallower?"},'
)

CATS_OLD = 'ozeane:{label:"Ozeane & Meere",icon:"\\u{1F30A}",modes:["hl_ozean_flaeche","hl_ozean_tiefe","ozean_match_typ","ozean_match_kontinent","hl_ozean_flaeche_klein","ozean_match_name","ws_ozean_atlantik"],cost:0},'
CATS_NEW = 'ozeane:{label:"Ozeane & Meere",icon:"\\u{1F30A}",modes:["hl_ozean_flaeche","hl_ozean_tiefe","ozean_match_typ","ozean_match_kontinent","hl_ozean_flaeche_klein","ozean_match_name","ws_ozean_atlantik","hl_ozean_tiefe_klein"],cost:0},'

GEN_DISP_OLD = 'ws_ozean_atlantik:()=>{initOzeaneWS("atlantik");return null;},'
GEN_DISP_NEW = (
    'ws_ozean_atlantik:()=>{initOzeaneWS("atlantik");return null;},\n'
    '  hl_ozean_tiefe_klein:()=>genOzeaneHLExt("max_tiefe_m",{unit:"m",lowerWins:true,prompt:_tc("Welches Gewässer ist seichter?")}),'
)

patch(GEN, [
    (I18N_PL_OLD,  I18N_PL_NEW,  'GEN: i18n PL'),
    (I18N_EN_OLD,  I18N_EN_NEW,  'GEN: i18n EN'),
    (MODES_OLD,    MODES_NEW,    'GEN: MODES array'),
    (CATS_OLD,     CATS_NEW,     'GEN: MODE_CATS'),
    (GEN_DISP_OLD, GEN_DISP_NEW, 'GEN: GEN dispatch'),
])

print('\nBonus-Patch 449b fertig.')
