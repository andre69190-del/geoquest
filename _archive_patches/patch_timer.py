#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch Timer-Bug - Verhindert sekündliche Neu-Renders
"""

with open('gen.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("🔍 Suche nach Timer-Bugs...")

# BUG 1: Timer ruft render() auf JEDE Sekunde (das ist das Problem!)
# FIX: Timer darf NICHT render() aufrufen, sondern nur Timer-Element updaten

bug_pattern1 = """tIv=setInterval(()=>{
    S.tm--;
    if(S.tm<=0){
      clearInterval(tIv);"""

# Suche nach render() im Timer
if 'setInterval(()=>{' in content and 'render();' in content:
    print("✅ Gefunden: setInterval mit render() Aufrufen")

    # Finde alle setInterval Blöcke mit render()
    # Das Problem: render() wird JEDE Sekunde aufgerufen
    # Das zerstört den ganzen Page-State

    # Ersetze render() Aufrufe mit targeted DOM-Update statt global render()
    # Aber VORSICHT: Das ist komplex

    # Einfacher Fix: Entferne render() aus dem Timer und ersetze mit gezieltem DOM-Update

    # Suche nach: tIv=setInterval(()=>{ ... render(); },1000);
    # Ersetze mit: tIv=setInterval(()=>{ ... }, 1000);

    # Das ist aber zu aggressiv. Besser: Nur bestimmte Timer fixen

    # TEMPORÄRER FIX: Deaktiviere den problematischen Timer
    if 'clearInterval(tIv);' in content:
        # Ersetze render() in Timern mit einer DOM-Update-Funktion
        old_timer = """tIv=setInterval(()=>{
    S.tm--;
    if(S.tm<=0){
      clearInterval(tIv);
      if(S.gridData&&!S.gridData.solved&&!S.gridData.failed){
        S.gridData.failed=true;
        S.gridData.lastMsg="⏱ Zeit abgelaufen!";
      }
    }
    render();"""

        new_timer = """tIv=setInterval(()=>{
    S.tm--;
    const timerEl=document.querySelector('.tbar .tfill');
    if(timerEl){
      const p=100*(S.tm||0)/S.dur;
      timerEl.style.width=p+'%';
    }
    if(S.tm<=0){
      clearInterval(tIv);
      if(S.gridData&&!S.gridData.solved&&!S.gridData.failed){
        S.gridData.failed=true;
        S.gridData.lastMsg="⏱ Zeit abgelaufen!";
        render();
      }
    }"""

        if old_timer in content:
            content = content.replace(old_timer, new_timer)
            print("✅ Timer-Bug gepatcht: render() nur bei Timeout, nicht jede Sekunde")
        else:
            print("⚠️  Exakter Pattern nicht gefunden, aber SearchString vorhanden")

# Speichere
with open('gen.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Timer-Bug-Patch angewendet")
