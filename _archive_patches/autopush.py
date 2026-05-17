#!/usr/bin/env python3
"""
autopush.py — Ein-Klick Git-Push für GeoQuest
Ausführen nach jedem Fix-Skript: python autopush.py
"""
import subprocess
import sys
import os

REPO_DIR = os.path.dirname(os.path.abspath(__file__))

def run(cmd, label):
    """Führt einen Shell-Befehl aus und gibt den Output aus."""
    result = subprocess.run(
        cmd,
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    return result

def detect_latest_fix():
    """Sucht nach der neuesten fix*.py Datei im Repo-Verzeichnis."""
    import glob
    pattern = os.path.join(REPO_DIR, "fix*.py")
    files = sorted(glob.glob(pattern))
    if files:
        name = os.path.basename(files[-1])
        return name.replace(".py", "")
    return None

def main():
    print("=" * 50)
    print("🚀  GeoQuest Auto-Push")
    print("=" * 50)

    # Commit-Nachricht automatisch anreichern
    latest_fix = detect_latest_fix()
    if latest_fix:
        commit_msg = f"Auto-Commit: {latest_fix} — GeoQuest Update"
    else:
        commit_msg = "Auto-Commit: Updates via Fix-Skripte"

    # ── git add . ──────────────────────────────────────
    print("\n📦  Packe alle Änderungen (git add .) ...")
    r = run(["git", "add", "."], "git add")
    if r.returncode != 0:
        print("❌  git add fehlgeschlagen — ist das ein Git-Repo?")
        sys.exit(1)
    print("✅  Alle Dateien vorgemerkt.")

    # ── Prüfen ob es überhaupt etwas zu committen gibt ─
    diff = run(["git", "diff", "--cached", "--quiet"], "diff check")
    if diff.returncode == 0:
        print("\n💤  Keine neuen Änderungen zum Committen gefunden.")
        print("    (Alle Dateien sind bereits auf dem aktuellen Stand.)")
        print("\n✨  Nichts zu tun — du bist up to date!")
        return

    # ── git commit ─────────────────────────────────────
    print(f"\n🏷️   Erstelle Commit: \"{commit_msg}\" ...")
    r = run(
        ["git", "commit", "-m", commit_msg],
        "git commit"
    )
    if r.returncode != 0:
        # Könnte "nothing to commit" sein (race condition)
        out = (r.stdout + r.stderr).lower()
        if "nothing to commit" in out or "nothing added" in out:
            print("💤  Keine Änderungen gefunden — nichts zu committen.")
            return
        print("❌  git commit fehlgeschlagen:")
        print(r.stderr)
        sys.exit(1)
    print("✅  Commit erstellt.")

    # ── git push ───────────────────────────────────────
    print("\n🌍  Lade zu GitHub & Vercel hoch (git push) ...")
    r = run(["git", "push"], "git push")
    if r.returncode != 0:
        err = r.stderr.lower()
        if "no upstream" in err or "no configured push" in err:
            print("⚠️   Kein Remote-Branch konfiguriert.")
            print("    Einmalig ausführen: git push --set-upstream origin main")
        elif "rejected" in err:
            print("⚠️   Push abgelehnt — evtl. erst pullen: git pull --rebase")
        else:
            print("❌  git push fehlgeschlagen.")
        print("    Fehlermeldung:", r.stderr.strip())
        sys.exit(1)

    print("✅  Push erfolgreich!")
    print("\n" + "=" * 50)
    print("🎉  Fertig! GitHub & Vercel bauen gleich neu.")
    print("=" * 50)

if __name__ == "__main__":
    main()
