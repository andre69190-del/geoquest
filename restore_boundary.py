import subprocess
import re

pristine_boundary = None

# 1. Wir reisen bis zu 25 Commits in die Vergangenheit, um die unzerstörte Nahtstelle zu finden
for i in range(2, 25):
    try:
        old_content = subprocess.check_output(['git', 'show', f'HEAD~{i}:gen.py']).decode('utf-8')
        # Wir suchen den sauberen Übergang: von 'let fb="";' über 'app.innerHTML' bis zum Fehler-Return von spotterCollect
        match = re.search(r'(let fb="";.*?app\.innerHTML.*?\}\s*function spotterCollect.*?S\.spotterMsg.*?render\(\);return;\s*\})', old_content, re.DOTALL)
        if match:
            pristine_boundary = match.group(1)
            print(f"[+] Pristine boundary found at commit HEAD~{i}")
            break
    except Exception:
        continue

if pristine_boundary:
    with open('gen.py', 'r', encoding='utf-8') as f:
        current_content = f.read()
    
    # 2. Wir ersetzen den korrupten Block in der aktuellen Datei
    # Wir ersetzen von 'let fb="";' bis genau vor unsere Quarantäne
    corrupted_match = re.search(r'(let fb="";.*?S\.spotterOk=false;render\(\);return;\s*\})', current_content, re.DOTALL)
    
    if corrupted_match:
        current_content = current_content.replace(corrupted_match.group(1), pristine_boundary)
        with open('gen.py', 'w', encoding='utf-8') as f:
            f.write(current_content)
        print("[OK] Mission accomplished! Render boundary and app.innerHTML successfully restored from Git history!")
    else:
        print("[ERROR] Could not find the corrupted block in current file.")
else:
    print("[ERROR] Could not find the pristine boundary in Git history.")
