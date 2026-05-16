with open('gen.py', 'r', encoding='utf-8') as f:
    content = f.read()

# FIX: Schütze alle candidates.map() Aufrufe mit Array.isArray() Guards
# Pattern 1: candidates.map (ohne S. Prefix)
if "candidates.map(" in content:
    content = content.replace("candidates.map(", "(Array.isArray(candidates) ? candidates : []).map(")

# Pattern 2: S.candidates.map (mit S. Prefix)
if "S.candidates.map(" in content:
    content = content.replace("S.candidates.map(", "(Array.isArray(S.candidates) ? S.candidates : []).map(")

with open('gen.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] Array.isArray() Guards hinzugefügt!")
print("- candidates.map() ist jetzt sicher vor TypeError")
print("- S.candidates.map() ist jetzt sicher vor TypeError")
