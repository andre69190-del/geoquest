import csv
import json
import os

# === KONFIGURATION ===
# Wie viele Einwohner muss eine Stadt mindestens haben, um im Spiel zu sein?
# 15.000 ist ein exzellenter Wert für den Hardcore-Modus.
MIN_POPULATION = 15000 
INPUT_FILE = 'worldcities.csv'
OUTPUT_FILE = 'cities_data.js'

def generate_cities_data():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ FEHLER: Die Datei '{INPUT_FILE}' wurde nicht gefunden.")
        print("Bitte lade die kostenlose Datenbank herunter:")
        print("👉 https://simplemaps.com/data/world-cities")
        print("Lege die 'worldcities.csv' in diesen Ordner und starte das Skript neu.")
        return

    cities = []
    
    print(f"⏳ Lese '{INPUT_FILE}' und filtere Städte ab {MIN_POPULATION} Einwohnern...")
    
    with open(INPUT_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                pop_str = row['population']
                if not pop_str: # Leere Einträge überspringen
                    continue
                    
                pop = float(pop_str)
                if pop >= MIN_POPULATION:
                    cities.append({
                        "name": row['city'],
                        "country": row['country'],
                        "lat": float(row['lat']),
                        "lng": float(row['lng']),
                        "pop": int(pop)
                    })
            except ValueError:
                # Falls Koordinaten oder Einwohnerzahlen ungültig/leer sind
                continue

    # Sortieren nach Einwohnerzahl (Größte Metropolen zuerst)
    # Das ist genial für dein Spiel: Die ersten 1000 im Array sind perfekt für Casual, 
    # die hinteren 15.000 perfekt für Hardcore!
    cities.sort(key=lambda x: x['pop'], reverse=True)

    print(f"✅ {len(cities)} Städte erfolgreich verarbeitet!")
    print(f"💾 Speichere Daten in '{OUTPUT_FILE}'...")

    # JavaScript Datei generieren
    with open(OUTPUT_FILE, mode='w', encoding='utf-8') as js_file:
        js_file.write("// Automatisch generiert aus Simplemaps World Cities\n")
        js_file.write(f"// Ab {MIN_POPULATION} Einwohnern. Gesamt: {len(cities)} Städte.\n")
        js_file.write("const worldCitiesData = ")
        # JSON formatieren (indent=2 für Lesbarkeit)
        json.dump(cities, js_file, indent=2, ensure_ascii=False)
        js_file.write(";\n")

    print(f"🚀 FERTIG! Die Datei '{OUTPUT_FILE}' wurde erstellt.")

if __name__ == "__main__":
    generate_cities_data()