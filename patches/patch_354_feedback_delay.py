#!/usr/bin/env python3
"""
Phase: 354
Date:  2026-06-01
Author: Claude / Andre
Scope: Feedback-Anzeigedauer +1,5 Sekunden (überall)

Änderungen:
  _fd (Haupt-Feedback-Timer, Einzel-Modus): 1900 → 3400 ms
  _fd (IATA-Modus):                         2800 → 4300 ms
  _fd (Multiplayer):                        5500 ms — UNVERÄNDERT (bereits optimiert)
  setTimeout(startNextRound, 1500)          1500 → 3000 ms (5 Stellen)

Dependencies: Phase 353
Zero-Bug Policy: assert c.count(old)==1 für eindeutige Anker;
                 globales replace() für die identischen startNextRound-Aufrufe
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN  = os.path.join(ROOT, "gen.py")

def patch(c, old, new, label):
    count = c.count(old)
    assert count == 1, f"[FAIL] Anker {count}× gefunden: {old[:70]!r}"
    print(f"  [OK] {label}")
    return c.replace(old, new, 1)

def run(cmd):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.stdout: print(r.stdout[-400:])
    if r.stderr and r.returncode != 0: print(r.stderr[-200:], file=sys.stderr)
    return r.returncode

if __name__ == "__main__":
    print("=" * 58)
    print("PATCH 354 — Feedback-Anzeigedauer +1,5 s überall")
    print("=" * 58)

    with open(GEN, encoding="utf-8") as f:
        c = f.read()

    # ── 1: Haupt-Feedback-Timer (_fd) ────────────────────────────────────
    # Original: 1900 ms (Default), 2800 ms (IATA), 5500 ms (MP unverändert)
    OLD_FD = "const _fd=(_isMpHost||_isMpGuest)?5500:(_qt===\"iata\"?2800:1900);"
    NEW_FD = "const _fd=(_isMpHost||_isMpGuest)?5500:(_qt===\"iata\"?4300:3400);"
    c = patch(c, OLD_FD, NEW_FD, "_fd: 1900→3400 ms | iata: 2800→4300 ms | MP: 5500 ms (unverändert)")

    # ── 2: setTimeout(startNextRound, 1500) — alle 5 Stellen ────────────
    old_snr = "setTimeout(startNextRound,1500);"
    count   = c.count(old_snr)
    assert count == 5, f"[FAIL] startNextRound 1500 erwartet 5×, gefunden {count}×"
    c = c.replace(old_snr, "setTimeout(startNextRound,3000);")
    print(f"  [OK] setTimeout(startNextRound): 1500→3000 ms ({count}× ersetzt)")

    with open(GEN, "w", encoding="utf-8") as f:
        f.write(c)
    print("  gen.py gespeichert")

    print("\n  Build …")
    if run([sys.executable, "gen.py"]) != 0: sys.exit(1)
    print("  Verify …")
    if run([sys.executable, "verify.py"]) != 0: sys.exit(1)

    subprocess.run([
        sys.executable, "post_phase.py",
        "--phase", "354",
        "--patch", "patches/patch_354_feedback_delay.py",
        "--summary",
        "UX: Feedback-Anzeigedauer +1,5 s — Einzel: 1900→3400 ms, "
        "IATA: 2800→4300 ms, startNextRound: 1500→3000 ms (5×). "
        "Multiplayer (5500 ms) unverändert."
    ], cwd=ROOT, capture_output=True, text=True)

    print("\n✅ Patch 354 — Feedback überall 1,5 s länger")
