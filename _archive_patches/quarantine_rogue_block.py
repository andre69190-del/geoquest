with open('gen.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Wir suchen den exakten Start- und Endpunkt aus dem Dump
start_str = "const candidates_safe = (typeof S !== 'undefined' && S.candidates) ? S.candidates : ((typeof candidates !== 'undefined') ? candidates : []);"
end_str = 'S.spotterInput="";render();'

start_idx = content.find(start_str)
end_idx = content.find(end_str, start_idx)

if start_idx != -1 and end_idx != -1:
    end_idx += len(end_str)
    rogue_block = content[start_idx:end_idx]

    # Wir packen den Code in einen Try-Catch Block und füllen die fehlenden Funktionen (Polyfill)
    safe_wrapper = f"""try {{
        const collKey = (c, cy) => String(c||'') + '|' + String(cy||'');
        if (typeof S !== 'undefined' && !S.collectedPlates) S.collectedPlates = [];
        {rogue_block}
    }} catch(e) {{
        console.warn("Rogue spotter block disabled to prevent crash");
    }}"""

    content = content[:start_idx] + safe_wrapper + content[end_idx:]

    with open('gen.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("[OK] Rogue block successfully quarantined with try-catch and polyfills!")
else:
    print("[ERROR] Could not find the rogue block anchors!")
