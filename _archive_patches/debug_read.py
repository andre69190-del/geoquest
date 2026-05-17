import re

with open('gen.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("========== FLAGSEL BLOCK ==========")
# Suche den Block für das Flaggen-Quiz
match_flag = re.search(r'(if\s*\(\s*q\.type\s*===\s*["\']flagsel["\']\s*\)\s*\{.*?answerHtml.*?\}else\s*\{)', content, re.DOTALL)
if match_flag:
    print(match_flag.group(1))
else:
    print("FEHLER: Flagsel-Block nicht gefunden oder Regex greift nicht!")

print("\n========== SETINTERVAL BLOCKS ==========")
# Suche alle setInterval Aufrufe im Code, um die Timer-Loop zu finden
matches_interval = re.finditer(r'([^\n]*setInterval\([^\n]*\)[^\n]*)', content)
found = False
for m in matches_interval:
    print(m.group(1).strip())
    found = True

if not found:
    print("Keine setInterval Aufrufe gefunden!")
