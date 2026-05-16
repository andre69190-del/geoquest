import re

with open('gen.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Strikte Längen-Checks in allen Generatoren von 3 auf 1 lockern
pattern = r'if\(pool\.length\s*<\s*3\)\s*return\s*null;'
replacement = r'if(pool.length<1) return null;'
content = re.sub(pattern, replacement, content)

# 2. Die rote Debug-Sonde exakt vor dem Return in genCityQ platzieren
target = 'return{type:"city"'
injection = 'console.log("🔴 DEBUG genCityQ pool.length:", pool ? pool.length : 0, "pf:", pf);\n  return{type:"city"'
content = content.replace(target, injection)

with open('gen.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] Checks gelockert (3 -> 1) und rote Debug-Sonde platziert!")
