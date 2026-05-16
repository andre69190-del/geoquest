#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch Flaggen-Quiz - Injiziert <img> Tags in flagsel-Buttons
"""

with open('gen.py', 'r', encoding='utf-8') as f:
    content = f.read()

# SUCHE nach der flagsel Render-Logik
if 'if(q.type==="flagsel")' in content:
    print("✅ Gefunden: flagsel Render-Block")

    # ERSETZE die button-Generierung mit korrektem <img>-Tag
    # ALT: return '<button... >${cc}</button>'
    # NEU: return '<button... ><img src="https://flagcdn.com/w120/${cc.toLowerCase()}.png" ...></button>'

    old_pattern = """return '<button class="'+cls+'" onclick="sel=\\''+cc+'\\';render()" data-quiz-answer="'+q.opts.indexOf(cc)+'">"""
    new_pattern = """return '<button class="'+cls+'" onclick="sel=\\''+cc+'\\';render()" data-quiz-answer="'+q.opts.indexOf(cc)+'"><img src="https://flagcdn.com/w120/'+cc.toLowerCase()+'.png" style="height:40px; border-radius:4px; display:block;" onerror="this.style.display=\\'none\\'; this.parentNode.textContent=\\''+cc.toUpperCase()+'\\\'">"""

    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        print("✅ Button-Struktur gepatcht")
    else:
        print("⚠️  Alt-Pattern nicht gefunden, versuche alternatives Pattern...")
        # Versuche nur den Teil vor dem </button> zu ersetzen
        if '</button>' in content and 'const fb2=' in content:
            # Finde die Stelle zwischen fb2= und </button>
            start = content.find('const fb2=')
            if start != -1:
                section = content[start:start+2000]
                if '<button' in section and '</button>' in section:
                    # Ersetze den Inhalt des Buttons
                    old_btn = """<button class="'+cls+'" onclick="sel=\\''+cc+'\\';render()" data-quiz-answer="'+q.opts.indexOf(cc)+'">'+cc+'</button>'"""
                    new_btn = """<button class="'+cls+'" onclick="sel=\\''+cc+'\\';render()" data-quiz-answer="'+q.opts.indexOf(cc)+'"><img src="https://flagcdn.com/w120/'+cc.toLowerCase()+'.png" style="height:40px; border-radius:4px;"></button>'"""

                    if old_btn in content:
                        content = content.replace(old_btn, new_btn)
                        print("✅ Button mit alternativem Pattern gepatcht")

    # Speichere zurück
    with open('gen.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ gen.py aktualisiert mit Flag-Bildern")
else:
    print("❌ flagsel-Block nicht gefunden!")
