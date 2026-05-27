# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
GeoQuest Patch Runner (Phase 225 / Suggestion 1)

Usage:
    python3 run_patch.py patches/patch_228_new_feature.py

What it does:
    1. Validates the patch file has the required header fields
    2. Creates a safety backup of gen.py
    3. Runs the patch script
    4. Runs python3 gen.py to rebuild GeoQuest.html
    5. Runs verify.py to check build integrity
    6. Reports pass/fail; restores backup on failure

On success: prints summary and reminds you to update unlock_and_push.bat.
On failure: automatically restores gen.py from backup.
"""
import sys, os, subprocess, shutil, re, datetime

def die(msg):
    print("[FAIL] " + msg)
    sys.exit(1)

if len(sys.argv) < 2:
    die("Usage: python3 run_patch.py patches/patch_NNN_description.py")

patch_file = sys.argv[1]
if not os.path.isfile(patch_file):
    die("Patch file not found: " + patch_file)

# ---- 1. Validate header ----
print("=" * 58)
print(" GeoQuest Patch Runner")
print("=" * 58)
print(" Patch: " + patch_file)
print()

with open(patch_file, 'r', encoding='utf-8', errors='replace') as f:
    src = f.read()

required_fields = ['Phase:', 'Date:', 'Scope:']
missing = [f for f in required_fields if f not in src]
if missing:
    print("[WARN] Patch header missing fields: " + str(missing))
    print("       (Continuing anyway -- please fix for future patches)")
else:
    print("[OK]  Header validated: Phase / Date / Scope present")

# ---- 2. Backup gen.py ----
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
backup = 'gen.py.bak_' + ts
shutil.copy2('gen.py', backup)
print("[OK]  Backup created: " + backup)

# ---- 3. Run patch ----
print("\n-- Running patch " + "-" * 42)
r = subprocess.run([sys.executable, patch_file], text=True)
if r.returncode != 0:
    print("\n[FAIL] Patch script exited with error. Restoring gen.py...")
    shutil.copy2(backup, 'gen.py')
    os.remove(backup)
    die("Patch FAILED -- gen.py restored from backup.")
print("[OK]  Patch script completed successfully")

# ---- 4. Rebuild ----
print("\n-- Rebuilding GeoQuest.html " + "-" * 30)
r = subprocess.run([sys.executable, 'gen.py'], text=True)
if r.returncode != 0:
    print("\n[FAIL] gen.py build failed. Restoring gen.py...")
    shutil.copy2(backup, 'gen.py')
    os.remove(backup)
    die("Build FAILED -- gen.py restored from backup.")
print("[OK]  Build completed")

# ---- 5. Verify ----
print("\n-- Running verify.py " + "-" * 37)
r = subprocess.run([sys.executable, 'verify.py'], text=True)
if r.returncode != 0:
    print("\n[FAIL] verify.py reported errors. Restoring gen.py...")
    shutil.copy2(backup, 'gen.py')
    os.remove(backup)
    die("Verify FAILED -- gen.py restored from backup.")

# ---- 6. Cleanup backup ----
os.remove(backup)

# ---- 6b. validate_content (non-blocking, info only) ----
print("\n-- Running validate_content.py " + "-" * 26)
subprocess.run([sys.executable, "validate_content.py"], text=True)
print("[INFO] validate_content.py finished (warnings do not block the build)")

# ---- 7. Summary ----
print("\n" + "=" * 58)
print(" PATCH APPLIED SUCCESSFULLY")
print("=" * 58)
html_size = os.path.getsize('GeoQuest.html') if os.path.isfile('GeoQuest.html') else 0
gen_size  = os.path.getsize('gen.py') if os.path.isfile('gen.py') else 0
print(" gen.py:        " + str(gen_size) + " bytes")
print(" GeoQuest.html: " + str(html_size) + " bytes")
print()
print(" Next steps:")
print("   1. Update unlock_and_push.bat commit message")
print("   2. Run unlock_and_push.bat to push to GitHub/Vercel")
print("   3. Check https://vercel.com for deployment status")
