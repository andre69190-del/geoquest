import re

with open('gen.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fehlerhafte Guards vom letzten Patch entfernen
content = content.replace("(Array.isArray(candidates) ? candidates : []).map(", "candidates.map(")
content = content.replace("(Array.isArray(S.candidates) ? S.candidates : []).map(", "S.candidates.map(")

# 2. Echte Kapselung in die render() Funktion injizieren
# Wir suchen die Definition von render() und fügen als allererste Zeile einen Scope-Guard ein.
pattern_render = r'(function\s+render\s*\(\)\s*\{)'
safe_scope_injection = r'\1\n    /* ENCAPSULATION GUARD */\n    let candidates = (typeof S !== "undefined" && S && S.candidates) ? S.candidates : [];\n'

content = re.sub(pattern_render, safe_scope_injection, content, count=1)

with open('gen.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] True Encapsulation enforced! 'candidates' is now safely scoped inside render().")
