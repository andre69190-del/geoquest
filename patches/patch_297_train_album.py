import os
import sys

def patch_gen():
    file_path = "gen.py"
    if not os.path.exists(file_path):
        print(f"Datei nicht gefunden: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # --- TEIL 1: Tracking-Logik in _handleAnswer einfuegen ---
    # Wir muessen korrekte Antworten in den Zug-Modi abfangen
    anchor_answer = """if(isCorrect) {"""

    # Pruefen ob der Patch schon lief
    if "trackTrainDepot(" in content:
        print("[SKIP] Zug-Depot Tracking existiert bereits.")
    elif anchor_answer in content:
        new_tracking = """if(isCorrect) {
      trackTrainDepot();"""
        content = content.replace(anchor_answer, new_tracking, 1)
        print("[OK] Train-Depot Tracking-Hook eingebaut.")
    else:
        print("[SKIP] Anker fuer Antwort-Auswertung nicht gefunden.")

    # --- TEIL 2: Die kompletten JS-Funktionen fuer das Depot ---
    # Wir platzieren sie kurz vor der renderCollectionScreen Funktion
    anchor_render = """function renderCollectionScreen() {"""

    new_functions = """
// === TRAIN DEPOT (ZUG-SAMMELALBUM) ===
function loadTrainDepot() {
  var raw = window.localStorage.getItem("gq_train_depot");
  return raw ? JSON.parse(raw) : [];
}
function saveTrainDepot(arr) {
  window.localStorage.setItem("gq_train_depot", JSON.stringify(arr));
}
function trackTrainDepot() {
  if(!lv || !lv.q || !lv.mode) return;
  var trainModes = ["zug_vkm", "zug_panorama", "zug_ds100", "zug_ds100_input"];
  if(trainModes.indexOf(lv.mode) === -1) return;

  // Wir identifizieren das Item am Subject oder der Frage
  var itemKey = lv.q.subject || lv.q.q || lv.q.name;
  if(!itemKey) return;

  var depot = loadTrainDepot();
  if(depot.indexOf(itemKey) === -1) {
    depot.push(itemKey);
    saveTrainDepot(depot);
  }
}

function showTrainDepot() {
  // Wir lesen die möglichen Items aus den KULTUR_DATA (da der Agent die Train-Daten dort oder in tech_match abgelegt hat)
  // Fallback, falls die Arrays leicht anders heissen
  var allVkm = (KULTUR_DATA.zug_vkm || TECH_DATA.zug_vkm || []).map(function(i){ return i.subject || i.n; });
  var allPanorama = (KULTUR_DATA.zug_panorama || TECH_DATA.zug_panorama || []).map(function(i){ return i.subject || i.n; });
  var allDs100 = (KULTUR_DATA.ds100_bahnhoefe || KULTUR_DATA.ds100 || []).map(function(i){ return i.q || i.name; });

  var unlocked = loadTrainDepot();

  var html = '<div style="padding:10px;"><h2>🚉 Dein Zug-Depot</h2><button onclick="changeScreen(\\'collection\\')" style="margin-bottom:15px;" class="btn">Zurück</button>';

  function renderSection(title, allItems) {
    if(!allItems || allItems.length === 0) return '';
    var unlockedCount = 0;
    var gridHtml = '<div style="display:flex; flex-wrap:wrap; gap:10px; justify-content:center;">';

    allItems.forEach(function(item) {
      var isUnlocked = unlocked.indexOf(item) !== -1;
      if(isUnlocked) unlockedCount++;
      var style = isUnlocked ? 'background:#e0f7fa; color:#006064; border:1px solid #00838f;' : 'background:#eee; color:#999; opacity:0.5;';
      var icon = isUnlocked ? '🚄' : '🔒';
      gridHtml += '<div style="padding:10px; border-radius:5px; width:120px; text-align:center; font-size:12px; font-weight:bold; ' + style + '">' + icon + '<br>' + item + '</div>';
    });
    gridHtml += '</div>';

    var h = '<h3>' + title + ' (' + unlockedCount + '/' + allItems.length + ')</h3>';
    return h + gridHtml + '<hr style="margin:20px 0;">';
  }

  html += renderSection("Halterkürzel (VKM)", allVkm);
  html += renderSection("Panoramabahnen", allPanorama);
  html += renderSection("Bahnhofskürzel (DS100)", allDs100);

  html += '</div>';
  document.getElementById("app").innerHTML = html;
}

function renderCollectionScreen() {"""

    if "showTrainDepot()" not in content and anchor_render in content:
        content = content.replace(anchor_render, new_functions, 1)
        print("[OK] Train-Depot UI und Render-Logik eingebaut.")
    else:
        print("[SKIP] Render-Anker nicht gefunden oder Depot existiert schon.")

    # --- TEIL 3: Den Button in der alten Sammel-Screen platzieren ---
    # Wir suchen nach dem Schließen-Tag des Header-Bereichs in renderCollectionScreen
    anchor_btn = """<div class="col-grid">"""

    new_btn = """
    <div style="text-align:center; margin-bottom: 20px;">
        <button onclick="showTrainDepot()" class="btn" style="background:#00838f; color:white; font-size:16px;">🚉 Zum Zug-Depot</button>
    </div>
    <div class="col-grid">"""

    if "Zum Zug-Depot" not in content and anchor_btn in content:
        # Ersetze nur das erste Vorkommen in der Collection-Screen
        content = content.split(anchor_render)[0] + anchor_render + content.split(anchor_render)[1].replace(anchor_btn, new_btn, 1)
        print("[OK] Train-Depot Button im UI platziert.")
    else:
        print("[SKIP] Button-Anker nicht gefunden.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

patch_gen()
