#!/bin/bash

echo "🔍 FEATURE-VERIFIZIERUNG"
echo "======================="
echo ""

echo "✓ Phase 152 - Impressum/Datenschutz:"
grep -c "legal-modal\|showLegalModal" index.html && echo "  → Modals gefunden" || echo "  → FEHLER"

echo ""
echo "✓ Phase 153 - Album Uncapped:"
grep -c "plate-list-container\|timeAgo" index.html && echo "  → Scrollable + Timestamps gefunden" || echo "  → FEHLER"

echo ""
echo "✓ Phase 154 - Map UI Overhaul:"
grep -c "map-marker\|map-pin\|#e0e0e0" index.html && echo "  → Map UI gefunden" || echo "  → FEHLER"

echo ""
echo "✓ Phase 155 - Map Timer:"
grep -c "timer-seconds\|updateMapTimer" index.html && echo "  → Timer Improvements gefunden" || echo "  → FEHLER"

echo ""
echo "✓ Phase 157 - Beta Features:"
grep -c "beta-badge\|bingo-grid\|beta-section" index.html && echo "  → Beta Features gefunden" || echo "  → FEHLER"

echo ""
echo "✓ Phase 159 - Altkennzeichen:"
grep -c "BR\|SNH\|BCH" index.html && echo "  → Altkennzeichen gefunden" || echo "  → FEHLER"

echo ""
echo "📊 Dateigrößen:"
du -h index.html GeoQuest.html gen.py | tail -3

