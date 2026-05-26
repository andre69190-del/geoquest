"""
patch_split_tiere_pflanzen.py
=============================
Splits the combined "tiere" MODE_CATS entry into two separate categories:
  - tiere  : "Tiere & Natur"   (icon 🦋) — only animal/horse modes
  - pflanzen: "Pflanzen & Flora" (icon 🌿) — all pflanzen modes

Also updates the spoiler-guard check (_isTiere) to cover both groups.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GEN  = os.path.join(ROOT, 'gen.py')

with open(GEN, 'r', encoding='utf-8') as fh:
    c = fh.read()

# ── 1. Split the MODE_CATS tiere entry ──────────────────────────────────────
# Remove pflanzen IDs from tiere and add new pflanzen category after it.

OLD_CATS = (
    '    "ws_tiere_pfeilgiftfrosch","uk_tiere_darwin_finken","uk_tiere_schutzgebiete",'
    '"uk_tiere_zoos","uk_tiere_nutztier_rassen","uk_tiere_fossilien","uk_tiere_arktis_antarktis",'
    '"uk_tiere_forscher_eponyme","uk_tiere_pelagial","uk_tiere_wuesten_spezialisten",'
    '"uk_tiere_gift_hotspots","uk_tiere_migranten","hl_tiere_haustier_dichte",'
    '"uk_pferde_rassen","uk_pferde_fachbegriffe","hl_pferde_stockmass","ws_pferde_fluesterer",\n'
    '    "uk_pflanzen_nutzpflanzen","uk_pflanzen_einzelbaeume","uk_pflanzen_botanische_gaerten",\n'
    '    "uk_pflanzen_tropenwald","uk_pflanzen_weinanbau","uk_pflanzen_heilpflanzen",\n'
    '    "uk_pflanzen_mangroven","uk_pflanzen_kakao_ursprung","uk_pflanzen_reisanbau",\n'
    '    "uk_pflanzen_bambus","uk_pflanzen_endemisch","uk_pflanzen_nationalblumen",\n'
    '    "hl_pflanzen_wuchshoehe","hl_pflanzen_alter","hl_pflanzen_fruchtgewicht",\n'
    '    "hl_pflanzen_samenlaenge","hl_pflanzen_kaffeeproduktion","hl_pflanzen_weinproduktion",\n'
    '    "hl_pflanzen_reisproduktion","hl_pflanzen_waldflaeche","hl_pflanzen_stammumfang",\n'
    '    "hl_pflanzen_blattflaeche","hl_pflanzen_bluehdauer","hl_pflanzen_genomgroesse",\n'
    '    "uk_pflanzen_gewuerze","uk_pflanzen_familien","uk_pflanzen_bluetezeit",\n'
    '    "uk_pflanzen_giftstoffe","uk_pflanzen_fruchttyp","uk_pflanzen_vermehrung",\n'
    '    "uk_pflanzen_lebensraum","uk_pflanzen_bestuaeber","uk_pflanzen_herkunft",\n'
    '    "uk_pflanzen_nutzung","uk_pflanzen_blattform","uk_pflanzen_klimazone",\n'
    '    "uk_pflanzen_scheinfruchte","uk_pflanzen_baum_des_jahres","uk_pflanzen_giftpflanze_jahres",\n'
    '    "ws_pflanzen_trauerweide","ws_pflanzen_rhododendron","ws_pflanzen_sonnenblume",\n'
    '    "ws_pflanzen_pusteblume","ws_pflanzen_nachtschatten","ws_pflanzen_vergissmeinnicht",\n'
    '    "ws_pflanzen_kaffeebohne","ws_pflanzen_weihnachtsstern","ws_pflanzen_ginkgobaum"\n'
    '  ],cost:0},\n'
    '};'
)

NEW_CATS = (
    '    "ws_tiere_pfeilgiftfrosch","uk_tiere_darwin_finken","uk_tiere_schutzgebiete",'
    '"uk_tiere_zoos","uk_tiere_nutztier_rassen","uk_tiere_fossilien","uk_tiere_arktis_antarktis",'
    '"uk_tiere_forscher_eponyme","uk_tiere_pelagial","uk_tiere_wuesten_spezialisten",'
    '"uk_tiere_gift_hotspots","uk_tiere_migranten","hl_tiere_haustier_dichte",'
    '"uk_pferde_rassen","uk_pferde_fachbegriffe","hl_pferde_stockmass","ws_pferde_fluesterer"\n'
    '  ],cost:0},\n'
    '  pflanzen:{label:"Pflanzen & Flora",icon:"\\u{1F33F}",modes:[\n'
    '    "uk_pflanzen_nutzpflanzen","uk_pflanzen_einzelbaeume","uk_pflanzen_botanische_gaerten",\n'
    '    "uk_pflanzen_tropenwald","uk_pflanzen_weinanbau","uk_pflanzen_heilpflanzen",\n'
    '    "uk_pflanzen_mangroven","uk_pflanzen_kakao_ursprung","uk_pflanzen_reisanbau",\n'
    '    "uk_pflanzen_bambus","uk_pflanzen_endemisch","uk_pflanzen_nationalblumen",\n'
    '    "hl_pflanzen_wuchshoehe","hl_pflanzen_alter","hl_pflanzen_fruchtgewicht",\n'
    '    "hl_pflanzen_samenlaenge","hl_pflanzen_kaffeeproduktion","hl_pflanzen_weinproduktion",\n'
    '    "hl_pflanzen_reisproduktion","hl_pflanzen_waldflaeche","hl_pflanzen_stammumfang",\n'
    '    "hl_pflanzen_blattflaeche","hl_pflanzen_bluehdauer","hl_pflanzen_genomgroesse",\n'
    '    "uk_pflanzen_gewuerze","uk_pflanzen_familien","uk_pflanzen_bluetezeit",\n'
    '    "uk_pflanzen_giftstoffe","uk_pflanzen_fruchttyp","uk_pflanzen_vermehrung",\n'
    '    "uk_pflanzen_lebensraum","uk_pflanzen_bestuaeber","uk_pflanzen_herkunft",\n'
    '    "uk_pflanzen_nutzung","uk_pflanzen_blattform","uk_pflanzen_klimazone",\n'
    '    "uk_pflanzen_scheinfruchte","uk_pflanzen_baum_des_jahres","uk_pflanzen_giftpflanze_jahres",\n'
    '    "ws_pflanzen_trauerweide","ws_pflanzen_rhododendron","ws_pflanzen_sonnenblume",\n'
    '    "ws_pflanzen_pusteblume","ws_pflanzen_nachtschatten","ws_pflanzen_vergissmeinnicht",\n'
    '    "ws_pflanzen_kaffeebohne","ws_pflanzen_weihnachtsstern","ws_pflanzen_ginkgobaum"\n'
    '  ],cost:0},\n'
    '};'
)

assert c.count(OLD_CATS) == 1, f"Anchor not unique (MODE_CATS split): {OLD_CATS[:80]!r}"
c = c.replace(OLD_CATS, NEW_CATS)
print("  [OK] MODE_CATS split: tiere trimmed, pflanzen category added")

# ── 2. Extend spoiler-guard to cover group:"pflanzen" as well ────────────────
OLD_GUARD = '  const _isTiere=modeObj.group==="tiere";'
NEW_GUARD = '  const _isTiere=modeObj.group==="tiere"||modeObj.group==="pflanzen";'

assert c.count(OLD_GUARD) == 1, f"Anchor not unique (spoiler guard): {OLD_GUARD!r}"
c = c.replace(OLD_GUARD, NEW_GUARD)
print("  [OK] Spoiler-guard extended to include group=pflanzen")

# ── Write back ───────────────────────────────────────────────────────────────
with open(GEN, 'w', encoding='utf-8') as fh:
    fh.write(c)

print("  [OK] gen.py updated")
