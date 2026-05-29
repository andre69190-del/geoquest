# -*- coding: utf-8 -*-
"""
Phase: 293
Scope: Länder-Antwortwerte der Match-Modi via displayCountry() lokalisieren

Viele Match-Modi (astro/geo/sport, lifestyle/airports …) haben als Antwort .c
einen deutschen LÄNDERNAMEN ("Italien", "Brasilien" …). Diese wurden bisher
nicht lokalisiert. Neu: _tcc(s) = länder-bewusste Variante von _tc:
  - de: unverändert
  - sonst: deutscher Ländername -> cc -> displayCountry(cc) (en/pl-Name)
  - kein Land: Fallback auf _tc (Inhaltstabelle)
Eingebaut in die Match-opts/ans aller Engines (statt _tc). Annotierte Werte
("China (Peking)") sind keine reinen Ländernamen -> bleiben über _tc-Fallback.
Antwortlogik bleibt konsistent (opts UND ans über _tcc).
Dependencies: patch_292_tpgt_i18n.py
"""
import os

GEN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'gen.py')
content = open(GEN, encoding='utf-8').read()

def rep(old, new, label, n=1):
    global content
    c = content.count(old)
    if c != n:
        print(f'[FAIL] {label}: count={c} (erwartet {n})'); raise SystemExit(1)
    content = content.replace(old, new)
    print(f'[OK]   {label} (x{c})')

# 1) _tcc nach _tc definieren
tc_def = 'function _tc(s){if(!s)return s;var _l=(typeof S!=="undefined"&&S.language)||localStorage.getItem("gq_lang")||"de";if(_l==="de")return s;var _m=_CONTENT_I18N[_l];return(_m&&_m[s])||s;}'
tcc_def = (
 '\n/* P293: länder-bewusste Inhalts-Übersetzung — dt. Ländername -> cc -> displayCountry */\n'
 'let _DE2CC=null;\n'
 'function _deCountryCc(name){if(_DE2CC===null){_DE2CC={};try{for(var i=0;i<COUNTRIES.length;i++){var cc=COUNTRIES[i].cc;var dn=getCountryName(cc,"de");if(dn)_DE2CC[dn]=cc;if(COUNTRIES[i].c)_DE2CC[COUNTRIES[i].c]=cc;}}catch(_e){}}return _DE2CC[name]||null;}\n'
 'function _tcc(s){if(!s)return s;var _l=(typeof S!=="undefined"&&S.language)||localStorage.getItem("gq_lang")||"de";if(_l==="de")return s;var _cc=_deCountryCc(s);if(_cc)return displayCountry(_cc);return _tc(s);}'
)
rep(tc_def, tc_def + tcc_def, '_tcc-Helper definiert')

# 2) Match opts/ans: _tc -> _tcc
rep('ans:_tc(correct.c),opts:opts.map(_tc)', 'ans:_tcc(correct.c),opts:opts.map(_tcc)', '_mkMatchQ opts/ans -> _tcc', n=1)
rep('ans:_tc(cor.c),opts:opts.map(_tc)', 'ans:_tcc(cor.c),opts:opts.map(_tcc)', 'tiere/pflanzen opts/ans -> _tcc', n=2)
rep('ans:_tc(cor),opts:opts.map(_tc)', 'ans:_tcc(cor),opts:opts.map(_tcc)', 'genUniversalMatchQ opts/ans -> _tcc', n=1)

_tmp = GEN + '.tmp'
open(_tmp, 'w', encoding='utf-8').write(content)
os.replace(_tmp, GEN)
print('\nPatch complete.')
