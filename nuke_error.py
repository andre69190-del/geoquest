p = 'gen.py'
with open(p, 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

for i in range(len(lines)):
    # 1. Kaputte Flaggen-Zeile komplett durch eine simple, saubere ersetzen
    if 'data-fallback' in lines[i] and 'flagcdn' in lines[i]:
        lines[i] = "        html += '<img src=\"https://flagcdn.com/w120/' + cc.toLowerCase() + '.png\" style=\"height:50px;border-radius:8px;\">';"
        
    # 2. Kaputte Wappen-Zeile komplett durch eine simple, saubere ersetzen
    elif 'data-fallback' in lines[i] and 'wappenUrl' in lines[i]:
        lines[i] = "        html += '<img src=\"' + wappenUrl + '\" style=\"max-width:100%; max-height:130px; object-fit:contain; margin:10px auto; display:block;\">';"
        
    # 3. Den Template-Literal-Fehler killen, falls Claude ihn wieder eingeschleppt hat
    if 'x${st}' in lines[i]:
        lines[i] = lines[i].replace('x${st}', "x' + st + '")

with open(p, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("[OK] Die kaputten Zeilen wurden restlos vernichtet und ersetzt!")
