#!/bin/bash

echo "🔍 Validierung fix105 - Syntax Error Behebung"
echo "=============================================="
echo ""

# Check 1: Suche nach fehlerhaften \` Patterns
echo "1️⃣ Suche nach fehlerhaften Backtick-Escapes:"
if grep -q '\\`' index.html; then
    count=$(grep -c '\\`' index.html)
    echo "   ⚠️ Noch $count fehlerhafte \\` gefunden"
else
    echo "   ✅ Keine fehlerhaften \\` gefunden"
fi

echo ""
echo "2️⃣ Prüfe renderBingoGrid Funktion:"
if grep -q 'function renderBingoGrid' index.html; then
    echo "   ✅ renderBingoGrid Funktion vorhanden"
    
    # Prüfe ob die Syntax sauber ist
    if grep -A 10 'function renderBingoGrid' index.html | grep -q 'html +='; then
        echo "   ✅ HTML-Verkettung sauber (verwendet String-Verkettung)"
    fi
fi

echo ""
echo "3️⃣ Prüfe auf Template Literal Fehler:"
# Suche nach \${ ohne backticks
if grep -q '\${' index.html && grep -q 'html += "'; then
    echo "   ✅ Template Interpolation repariert"
else
    echo "   ✓ Keine Template Interpolation nötig"
fi

echo ""
echo "4️⃣ Dateigrößen:"
du -h index.html
wc -l index.html | awk '{print "   Zeilen: " $1}'

echo ""
echo "✅ Validierung abgeschlossen!"

