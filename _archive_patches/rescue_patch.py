import re

with open('gen.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Sichere Reparatur der Flaggen-Buttons (Ohne re.DOTALL!)
pattern_block = r"(const fb2\s*=\s*q\.opts\.map\(cc\s*=>\s*\{\s*let cls\s*=\s*[\"']btn-base[\"'];\s*)return\s+'<button.*?<\/button>';(\s*\}\)\.join\(''\);)"

def repl(m):
    return m.group(1) + """return '<button class="' + cls + '" onclick="checkAns(\\\'' + cc + '\\\')"><img src="https://flagcdn.com/w120/' + cc.toLowerCase() + '.png" style="height:40px; border-radius:4px; pointer-events:none;"></button>';""" + m.group(2)

content = re.sub(pattern_block, repl, content)

# 2. Radikale Deaktivierung der Timer-Loops (Single Line Regex!)
content = re.sub(r"setInterval\(\(\)=>(?:\{)?\s*evaluateWeeklyLeague\(\);?\s*(?:\})?,[ \d]+\);", "/* WeeklyLeague interval disabled */", content)
content = re.sub(r"setInterval\(\(\)=>(?:\{)?\s*renderHomeTab\(\);?\s*(?:\})?,[ \d]+\);", "/* HomeTab interval disabled */", content)

with open('gen.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] Emergency Rescue Patch Applied!")
