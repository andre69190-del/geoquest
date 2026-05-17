with open('gen.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Füge die fehlende collKey Funktion vor render() ein
collkey_function = """/* Album Collection Key Generator */
const collKey = (code, country) => (code || '') + '|' + (country || '');

"""

# Finde die render() Funktion
render_pos = content.find("function render(){")
if render_pos > 0:
    # Füge die Funktion davor ein
    content = content[:render_pos] + collkey_function + content[render_pos:]

with open('gen.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] collKey() Funktion erfolgreich hinzugefügt!")
