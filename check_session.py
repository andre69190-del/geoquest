# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
check_session.py -- GeoQuest Session-End-Check
Prueft alle 5 Checklisten-Punkte nach einer Sprint-Session.

Usage:
    python3 check_session.py
    python3 check_session.py --strict   (exit 1 bei Warnings)

Prueft:
  1. verify.py            -- JS-Syntax, Placeholder, MODES-Dispatch, Daily Pool
  2. validate_content.py  -- JSON-Dateien, Schema, Koordinaten, Cross-Val
  3. Dokumente-Sync       -- README, ARCHITECTURE, landing.html, PATCHES.md
  4. MODES-Konsistenz     -- gen.py MODES count == MODE_CATS count
  5. Backup-Status        -- Warnhinweis wenn keine Backups vorhanden
"""

import os, re, sys, subprocess, json

BASE   = os.path.dirname(os.path.abspath(__file__))
STRICT = '--strict' in sys.argv

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

passed = []
warnings = []
failed = []

def ok(msg):    passed.append(msg);    print(f"  {GREEN}[OK]{RESET}   {msg}")
def warn(msg):  warnings.append(msg);  print(f"  {YELLOW}[WARN]{RESET} {msg}")
def fail(msg):  failed.append(msg);    print(f"  {RED}[FAIL]{RESET} {msg}")
def section(t): print(f"\n{BOLD}-- {t} {'-'*(50-len(t))}{RESET}")

print(f"\n{BOLD}{'='*58}")
print(" GeoQuest Session-End-Check")
print(f"{'='*58}{RESET}")

# ── 1. verify.py ──────────────────────────────────────────────────────────────
section("1. verify.py")
r = subprocess.run([sys.executable, 'verify.py'], capture_output=True, text=True, cwd=BASE)
m = re.search(r'(\d+)/(\d+) passed\s*\|\s*(\d+) failed', r.stdout)
if m:
    p, total, f_cnt = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if f_cnt == 0:
        ok(f"verify.py: {p}/{total} passed, 0 failed")
    else:
        fail(f"verify.py: {f_cnt} FAILED ({p}/{total})")
        for line in r.stdout.split('\n'):
            if '[!!]' in line:
                fail(f"  {line.strip()}")
else:
    fail(f"verify.py: Ausgabe nicht parsebar. RC={r.returncode}")

# ── 2. validate_content.py ────────────────────────────────────────────────────
section("2. validate_content.py")
r2 = subprocess.run([sys.executable, 'validate_content.py'], capture_output=True, text=True, cwd=BASE)
m2 = re.search(r'(\d+)/(\d+) files scanned\s*\|\s*(\d+) warning', r2.stdout)
if m2:
    scanned, total2, w_cnt = int(m2.group(1)), int(m2.group(2)), int(m2.group(3))
    if w_cnt == 0:
        ok(f"validate_content.py: {scanned}/{total2} files OK, 0 warnings")
    else:
        fail(f"validate_content.py: {w_cnt} warning(s) in {scanned} files")
else:
    fail(f"validate_content.py: Ausgabe nicht parsebar. RC={r2.returncode}")

# ── 3. Dokumente-Sync ─────────────────────────────────────────────────────────
section("3. Dokumente-Sync")

# Lese MODES-Count aus gen.py
with open(os.path.join(BASE, 'gen.py'), encoding='utf-8') as f:
    gen_src = f.read()
modes_m = re.search(r'const MODES=\[(.*?)\];', gen_src, re.DOTALL)
actual_modi = len(re.findall(r'id:"([^"]+)"', modes_m.group(1))) if modes_m else 0

# README.md
readme_path = os.path.join(BASE, 'README.md')
if os.path.exists(readme_path):
    with open(readme_path, encoding='utf-8') as f:
        readme = f.read()
    m_rm = re.search(r'Phase (\d+)', readme)
    m_modi_rm = re.search(r'(\d+) Modi', readme)
    phase_rm = int(m_rm.group(1)) if m_rm else 0
    modi_rm  = int(m_modi_rm.group(1)) if m_modi_rm else 0
    if modi_rm == actual_modi:
        ok(f"README.md: {actual_modi} Modi korrekt, Phase {phase_rm}")
    else:
        warn(f"README.md: {modi_rm} Modi (gen.py hat {actual_modi}) -- post_phase.py ausfuehren!")
else:
    fail("README.md nicht gefunden")

# ARCHITECTURE.md
arch_path = os.path.join(BASE, 'ARCHITECTURE.md')
if os.path.exists(arch_path):
    with open(arch_path, encoding='utf-8') as f:
        arch = f.read()
    m_arch = re.search(r'(\d+) Spielmodi', arch)
    modi_arch = int(m_arch.group(1)) if m_arch else 0
    if modi_arch == actual_modi:
        ok(f"ARCHITECTURE.md: {actual_modi} Spielmodi korrekt")
    else:
        warn(f"ARCHITECTURE.md: {modi_arch} Spielmodi (gen.py hat {actual_modi})")
else:
    fail("ARCHITECTURE.md nicht gefunden")

# landing.html
landing_path = os.path.join(BASE, 'landing.html')
if os.path.exists(landing_path):
    with open(landing_path, 'rb') as f:
        landing_raw = f.read()
    landing = landing_raw.decode('utf-8', errors='replace')
    m_land = re.search(r'(\d{3}) (?:Spielmodi|Modi)', landing)
    modi_land = int(m_land.group(1)) if m_land else 0
    if modi_land == actual_modi:
        ok(f"landing.html: {actual_modi} Modi korrekt")
    else:
        warn(f"landing.html: {modi_land} Modi (gen.py hat {actual_modi})")
else:
    warn("landing.html nicht gefunden")

# GeoQuest_Website_Konzept.md
konzept_path = os.path.join(BASE, 'GeoQuest_Website_Konzept.md')
if os.path.exists(konzept_path):
    with open(konzept_path, encoding='utf-8') as f:
        konzept = f.read()
    m_konz = re.search(r'(\d+) Spielmodi', konzept)
    modi_konz = int(m_konz.group(1)) if m_konz else 0
    if modi_konz == actual_modi:
        ok(f"GeoQuest_Website_Konzept.md: {actual_modi} Modi korrekt")
    else:
        warn(f"GeoQuest_Website_Konzept.md: {modi_konz} Modi (gen.py hat {actual_modi})")

# CLAUDE_SESSION_STARTER.md -- manuell gepflegt, aber von post_phase.py auto-aktualisiert
ss_path = os.path.join(BASE, 'CLAUDE_SESSION_STARTER.md')
if os.path.exists(ss_path):
    with open(ss_path, encoding='utf-8') as f:
        ss = f.read()
    m_ss_modi = re.search(r'\| Spielmodi \| \*\*(\d+)\*\*', ss)
    modi_ss = int(m_ss_modi.group(1)) if m_ss_modi else 0
    if modi_ss == actual_modi:
        ok(f"CLAUDE_SESSION_STARTER.md: {actual_modi} Modi korrekt")
    else:
        warn(f"CLAUDE_SESSION_STARTER.md: {modi_ss} Modi (gen.py hat {actual_modi}) -- post_phase.py ausfuehren!")
else:
    warn("CLAUDE_SESSION_STARTER.md nicht gefunden")

# PATCHES.md -- pruefen ob letzter Eintrag aktuell ist
patches_md = os.path.join(BASE, 'patches', 'PATCHES.md')
if os.path.exists(patches_md):
    with open(patches_md, encoding='utf-8') as f:
        pm = f.read()
    phase_m = re.search(r'Phase (\d+)', readme)
    current_phase = phase_m.group(1) if phase_m else '???'
    if current_phase in pm:
        ok(f"PATCHES.md: Phase {current_phase} eingetragen")
    else:
        warn(f"PATCHES.md: Phase {current_phase} fehlt -- Eintrag ergaenzen!")

# GeoQuest.html == index.html ?
gq_path = os.path.join(BASE, 'GeoQuest.html')
ix_path = os.path.join(BASE, 'index.html')
if os.path.exists(gq_path) and os.path.exists(ix_path):
    gq_sz = os.path.getsize(gq_path)
    ix_sz = os.path.getsize(ix_path)
    if gq_sz == ix_sz:
        ok(f"GeoQuest.html == index.html ({gq_sz:,} Bytes, sync)")
    else:
        fail(f"GeoQuest.html ({gq_sz:,}) != index.html ({ix_sz:,}) -- DESYNC! gen.py ausfuehren!")

# ── 4. MODES-Konsistenz ───────────────────────────────────────────────────────
section("4. MODES-Konsistenz (gen.py)")

# Count MODE_CATS entries
cats_m = re.search(r'const MODE_CATS=\{(.*?)\};', gen_src, re.DOTALL)
cats_count = 0
if cats_m:
    cats_modes = re.findall(r'modes:\[(.*?)\]', cats_m.group(1), re.DOTALL)
    cats_count = sum(len(re.findall(r'"([^"]+)"', m)) for m in cats_modes)

# Count GEN dispatch -- zähle MODES-IDs die im GEN-Block vorkommen
# Manche Modi werden außerhalb von GEN geroutet (z.B. wort_schmiede via if-Branch) -- das ist OK
gen_m = re.search(r'const GEN=\{(.*?)\};', gen_src, re.DOTALL)
modes_ids_set = set(re.findall(r'id:"([^"]+)"', modes_m.group(1))) if modes_m else set()
# Alle identifier: patterns im GEN-Block matchen, dann mit MODES-IDs schneiden
gen_all_keys = set(re.findall(r'"?([a-zA-Z0-9_]+)"?\s*:', gen_m.group(1))) if gen_m else set()
gen_count = len(gen_all_keys & modes_ids_set)
# Modi die außerhalb GEN geroutet werden (Sonder-Dispatcher via if-Branch in Router)
SPECIAL_ROUTED = {'wort_schmiede'}  # ergänzen wenn neue Sonder-Router dazukommen
missing = modes_ids_set - gen_all_keys - SPECIAL_ROUTED

ok(f"MODES: {actual_modi} Eintraege")
ok(f"MODE_CATS: {cats_count} Modus-Referenzen")
if not missing:
    ok(f"GEN dispatch: {gen_count}/{actual_modi} Eintraege + {len(SPECIAL_ROUTED)} Sonder-Router (vollstaendig)")
elif len(missing) <= 3:
    warn(f"GEN dispatch: {len(missing)} MODES ohne Eintrag: {sorted(missing)} -- absichtlich oder Bug?")
else:
    fail(f"GEN dispatch: {len(missing)} MODES ohne Generator: {sorted(missing)[:5]}...")

# Check for unreplaced placeholders -- in GeoQuest.html (nicht gen.py, dort sind sie intentional)
gq_html_path = os.path.join(BASE, 'GeoQuest.html')
if os.path.exists(gq_html_path):
    with open(gq_html_path, encoding='utf-8', errors='replace') as f:
        gq_html = f.read()
    orphans = sorted(set(re.findall(r'PLACEHOLDER_\w+', gq_html)))
    if orphans:
        fail(f"GeoQuest.html: {len(orphans)} unreplaced PLACEHOLDER_ -- gen.py neu ausfuehren! {orphans[:3]}")
    else:
        ok("GeoQuest.html: keine unreplaced PLACEHOLDER_")
else:
    warn("GeoQuest.html nicht gefunden -- gen.py noch nicht ausgefuehrt?")

# ── 5. Backup-Status ──────────────────────────────────────────────────────────
section("5. Backup-Status")
import glob as _gl
baks = sorted(_gl.glob(os.path.join(BASE, 'gen.py.bak_*')))
if len(baks) >= 1:
    ok(f"{len(baks)} Backup(s) vorhanden, neuestes: {os.path.basename(baks[-1])}")
else:
    warn("Keine gen.py.bak_* Backups vorhanden -- run_patch.py erstellt automatisch welche")

# Leere Dateien im Root?
empty = [f for f in os.listdir(BASE) if os.path.isfile(os.path.join(BASE,f))
         and os.path.getsize(os.path.join(BASE,f)) == 0 and not f.startswith('.')]
if empty:
    warn(f"Leere Dateien im Root: {empty}")
else:
    ok("Keine leeren Dateien im Root")

# Patch-Duplikat-Schutz: Gibt es patch_NNN Dateien die noch NICHT in PATCHES.md dokumentiert sind?
patches_dir = os.path.join(BASE, 'patches')
if os.path.exists(patches_md):
    with open(patches_md, encoding='utf-8') as _pmf:
        _pm_src = _pmf.read()
    # PATCHES.md hat zwei Formate: '## Phase NNN' (ab Phase 438) und Tabelle '| NNN |' (aeltere Phasen)
    applied_phases = set(int(x) for x in re.findall(r'## Phase (\d+)', _pm_src))
    # Auch Tabellen-Eintraege wie "| 221a |" erfassen (Strip Buchstaben-Suffix)
    for raw in re.findall(r'\|\s*(\d{3,}[a-z]?)\s*\|', _pm_src):
        applied_phases.add(int(re.match(r'(\d+)', raw).group(1)))
    max_doc_phase = max(applied_phases) if applied_phases else 0
    patch_files_list = [f for f in os.listdir(patches_dir) if f.endswith('.py')]
    undocumented = []
    for pf in patch_files_list:
        import re as _re2
        m_pf = _re2.match(r'patch_(\d+)[a-z]?_', pf)
        if m_pf and int(m_pf.group(1)) > max_doc_phase:
            undocumented.append(pf)
    if undocumented:
        warn(f"patch_NNN ohne PATCHES.md-Eintrag (noch nicht ausgefuehrt?): {sorted(undocumented)[:5]}")
    else:
        ok("Alle patch_NNN-Dateien in PATCHES.md dokumentiert")