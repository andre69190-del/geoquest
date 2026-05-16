#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aggressiver Timer-Patch mit Regex
"""
import re

with open('gen.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("🔍 Regex-Search für Timer...")

# Suche nach dem Muster: tIv=setInterval(()=>{...render();...},1000);
# und ersetze render() mit gezielterer DOM-Update

pattern = r'tIv=setInterval\(\(\)=>{\s*S\.tm--;\s*(?:.*?)\s*render\(\);?\s*},1000\);'

matches = re.findall(pattern, content, re.DOTALL)
if matches:
    print(f"✅ Gefunden: {len(matches)} Timer-Blöcke mit render()")

    # Ersetze alle render() Aufrufe die DIREKT im setInterval Timer sind
    # Mit einem gezielteren DOM-Update statt global render()

    # Einfacher Fix: Ersetze "render();" mit Kommentar (deaktiviert den Bug)
    # ABER: Das ist zu radikal

    # Besserer Fix: render() wird nur aufgerufen wenn Timer ausläuft
    # Nicht jede Sekunde

    # Nutze Regex um render() im setInterval zu entfernen/verschieben
    old_interval = re.compile(
        r'tIv=setInterval\(\(\)=>\{\s*S\.tm--;\s*(?:if\(S\.tm<=0\)\{[^}]*\})?.*?render\(\);?\s*\},1000\);',
        re.DOTALL
    )

    def replace_interval(match):
        original = match.group(0)
        # Entferne render() vom Timer-Tick und füge es nur beim Timeout ein
        modified = original.replace('render();', '')
        # Stelle sicher dass render() im if(S.tm<=0) Block ist
        if 'if(S.tm<=0)' not in modified:
            modified = modified.replace(
                'S.tm--;',
                'S.tm--;if(S.tm<=0){clearInterval(tIv);render();}'
            )
        return modified

    new_content = old_interval.sub(replace_interval, content)

    if new_content != content:
        print("✅ Entfernt: render() Aufrufe aus Timer-Loop")
        with open('gen.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ gen.py aktualisiert")
    else:
        print("⚠️  Keine Änderungen mit Regex gemacht")
else:
    print("⚠️  Kein Timer-Pattern mit render() gefunden")
