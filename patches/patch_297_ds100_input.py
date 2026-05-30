import os
import sys

def patch_verify():
    file_path = "verify.py"
    if not os.path.exists(file_path):
        print(f"Datei nicht gefunden: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Überspringe, wenn Sektion 19e schon existiert
    if "Sektion 19e: DS100 Hardcore" in content:
        print("[SKIP] DS100 Hardcore-Validierung existiert bereits in verify.py")
        return

    # Suche das Ende der Sektion 19 (Zug-Validatoren aus Phase 296.4)
    # und füge die neue Sektion für den Hardcore-Modus ein.
    # Als Anker nutzen wir eine typische Print-Ausgabe oder Kommentar aus 19d.
    anchor = """print("Sektion 19: Zug-Validatoren... OK")"""

    new_section = """
print("Sektion 19e: DS100 Hardcore Modus (Input) checken...")
has_ds100_hardcore = "zug_ds100_input" in MODES_IDS
if not has_ds100_hardcore:
    print("WARNING: Modus zug_ds100_input (DS100 Hardcore) fehlt in MODES.")
    # (Wir crashen hier nicht, falls es noch ein Rollback gab)
else:
    # Prüfe auf Generator-Dispatch in JS
    if "genDS100InputQ" not in js_content:
        raise Exception("genDS100InputQ fehlt in gen.py für den Hardcore-Modus")
print("Sektion 19: Zug-Validatoren... OK")
"""

    if anchor in content:
        content = content.replace(anchor, new_section, 1)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("[OK] Sektion 19e: DS100 Hardcore-Validierung hinzugefügt.")
    else:
        print("[SKIP] Anker für verify.py Sektion 19 nicht gefunden. Bitte manuell anpassen.")

patch_verify()
