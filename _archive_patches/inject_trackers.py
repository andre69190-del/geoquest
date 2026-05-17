import re

with open('gen.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Wir injizieren grüne Konsolen-Logs an den 4 wichtigsten Wegpunkten der App-Logik

# Wegpunkt 1: Klick auf den Button (startGame)
content = re.sub(r'function startGame\((.*?)\)\s*\{', r'function startGame(\1){ console.log("🟢 [TRACKER] 1. startGame gestartet. Mode:", \1);', content)

# Wegpunkt 2: Frage generieren (lq / loadQuestion)
content = re.sub(r'function lq\(\)\s*\{', r'function lq(){ console.log("🟢 [TRACKER] 2. lq (loadQuestion) gestartet.");', content)

# Wegpunkt 3: Bildschirm zeichnen (render)
content = re.sub(r'function render\(\)\s*\{', r'function render(){ console.log("🟢 [TRACKER] 3. render gestartet. Aktuelle Phase:", typeof S !== "undefined" ? S.ph : "S is null");', content)

# Wegpunkt 4: HTML an den Browser schicken (Kurz vor app.innerHTML im Quiz-Block)
target = 'const puBar=`<div class="pu-bar">'
injection = 'console.log("🟢 [TRACKER] 4. Erreiche HTML-Zuweisung. Antwort-Block Länge:", typeof answerHtml !== "undefined" ? answerHtml.length : "UNDEFINED");\n  const puBar=`<div class="pu-bar">'
content = content.replace(target, injection)

with open('gen.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] Grüne Tracker-Sonden erfolgreich verteilt!")
