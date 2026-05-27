"""
Phase: 250
Date:  2026-05-27
Author: Claude / Andre
Scope: Accordion-Fix — toggleAccordion nutzt filterByCategory() als zuverlässigen Öffner

Description:
  Akkordeon-Kategorien Astronomie, Geologie & Sport-Wissen "ließen sich nicht öffnen".

  Root cause: toggleAccordion() manipulierte das DOM direkt (classList, cssText) und
  suchte schließende Elemente über querySelectorAll('.accordion-content.open') —
  aber nur wenn der 'open'-Klasse schon gesetzt war. Wenn filterByCategory() den
  Akkordeon zuvor via content.style.display='none' (ohne open-Klasse) geschlossen
  hatte, fand querySelectorAll(...open) nichts und der Öffner war inkonsistent mit
  dem CSS-Default (.accordion-content{display:none}).

  Fix: Der öffnende Pfad von toggleAccordion() delegiert jetzt an filterByCategory(),
  die NACHGEWIESENERMASSEN funktioniert:
    - Setzt S.filterCat = catId  ✓
    - Fügt .open-Klasse hinzu  ✓
    - Setzt inline display:block  ✓
    - Schließt alle anderen Sektionen konsistent  ✓
    - Ruft _initAllCarousels() auf  ✓

  Schließen (isOpen=true) bleibt direktes DOM-Manipulation, funktioniert einwandfrei.

Dependencies: patch_243b_modes_fix.py
Zero-Bug Policy: All c.replace() calls use assert c.count(old)==1
"""

import pathlib

ROOT = pathlib.Path(__file__).parent.parent
gen  = ROOT / "gen.py"
c    = gen.read_text(encoding="utf-8")

old = '''window.toggleAccordion=function(header,catId){
  var content=header.nextElementSibling;
  var arrow=header.querySelector('.acc-arrow');
  var isOpen=content.classList.contains('open');
  if(isOpen){
    content.classList.remove('open');
    content.style.display='none';
    if(arrow)arrow.style.transform='rotate(0deg)';
  } else {
    /* Phase 216: single-open accordion — close all others first */
    document.querySelectorAll('.accordion-content.open,.acc-body.open').forEach(function(el){
      if(el!==content){
        el.classList.remove('open');
        el.style.display='none';
        var sib=el.previousElementSibling;
        if(sib){var a=sib.querySelector('.acc-arrow');if(a)a.style.transform='rotate(0deg)';}
      }
    });
    var gc=(typeof S!=='undefined'&&S.gridCols)||(parseInt(localStorage.getItem('geoquest_grid_cols'))||4);
    content.style.cssText='display:block;padding:0;width:100%;box-sizing:border-box';
    content.classList.add('open');
    if(arrow)arrow.style.transform='rotate(180deg)';
    /* UX FIX: persist active category so menu restores to correct section after game */
    if(typeof S!=='undefined')S.filterCat=catId;
    setTimeout(function(){if(typeof window._initAllCarousels==="function")window._initAllCarousels();},50);
    /* Phase 218 FIX: restore saved page after section becomes visible */
    setTimeout(function(){if(typeof window._restoreCarouselPages==="function")window._restoreCarouselPages();},100);
  }
};'''

assert c.count(old) == 1, f"Anchor not unique: {old!r}"

new = '''window.toggleAccordion=function(header,catId){
  var content=header.nextElementSibling;
  if(!content)return;
  var arrow=header.querySelector('.acc-arrow');
  var isOpen=content.classList.contains('open');
  if(isOpen){
    /* Close: direct DOM — works reliably */
    content.classList.remove('open');
    content.style.display='none';
    if(arrow)arrow.style.transform='rotate(0deg)';
    if(typeof S!=='undefined')S.filterCat='pure_geo';
  } else {
    /* Phase 250 FIX: delegate to filterByCategory() — the proven, reliable open path.
       filterByCategory() sets S.filterCat, adds .open class, sets inline display:block,
       closes all others, and calls _initAllCarousels() — consistent CSS + JS state. */
    if(typeof window.filterByCategory==='function'){
      window.filterByCategory(catId);
    }
    setTimeout(function(){if(typeof window._restoreCarouselPages==="function")window._restoreCarouselPages();},150);
  }
};'''

c = c.replace(old, new, 1)
gen.write_text(c, encoding="utf-8")
print("  [OK] toggleAccordion() rewritten — öffnet via filterByCategory()")
print("patch_250_accordion_fix.py erfolgreich angewendet.")
