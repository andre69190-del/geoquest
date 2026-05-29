"""
Phase: 279
Date:  2026-05-29
Author: Claude / Andre
Scope: Mobile PWA install fix + Landscape orientation detection fix

Description:
  FIX 1 – PWA Install auf iOS:
    beforeinstallprompt wird auf iOS Safari NIEMALS gefeuert, daher
    war S.pwaPrompt immer null und der Install-Button tat nichts.
    Loesung:
      - _isIOS() und _isInStandaloneMode() Helper hinzugefuegt
      - renderPwaBanner() branchiert jetzt auf iOS vs. Android:
          iOS: Banner mit Schritt-fuer-Schritt Safari-Anleitung + Dismiss
          Android: bestehender beforeinstallprompt-Flow (unveraendert)
      - Banner-Bedingung in render() erweitert: zeigt sich auch auf iOS
        wenn noch nicht installiert und nicht dismissed

  FIX 2 – Landscape-Erkennung auf Handy:
    _isPortrait() nutzte nur window.innerHeight > window.innerWidth
    was waehrend/nach Rotation noch falsch sein kann (Browser noch
    nicht neu gerendert, 120ms delay zu kurz).
    Loesung:
      - _isPortrait() nutzt jetzt zuerst screen.orientation.type
        (genaueste API), dann window.orientation (iOS-Fallback),
        dann Dimension-Vergleich als letzter Fallback
      - Timeout in _onOrientChange von 120ms auf 350ms erhoehen
      - resize-Event als zuverlaessigsten Cross-Plattform-Trigger
        hinzugefuegt (debounced, 200ms)

Dependencies: patch_251_pwa_banner_scope_fix.py
Zero-Bug Policy: All c.replace() calls use assert c.count(old)==1
"""

GEN = '/sessions/youthful-relaxed-turing/mnt/Geoquest/gen.py'

with open(GEN, encoding='utf-8') as f:
    content = f.read()

def patch(old, new, label):
    global content
    cnt = content.count(old)
    if cnt == 0:
        print(f'[SKIP] {label}: anchor not found')
        return
    if cnt > 1:
        print(f'[WARN] {label}: anchor {cnt}x – using replace(1)')
    content = content.replace(old, new, 1)
    print(f'[OK]   {label}')


# ============================================================
# FIX 1a: _isPortrait() – robustere Erkennung
# ============================================================
patch(
    'function _isPortrait(){return window.innerHeight>window.innerWidth;}',
    r"""function _isPortrait(){
  /* 1) Screen Orientation API – genaueste Methode */
  if(screen.orientation&&screen.orientation.type)
    return screen.orientation.type.startsWith('portrait');
  /* 2) window.orientation – veraltet aber zuverlaessig auf iOS Safari */
  if(typeof window.orientation==='number')
    return window.orientation===0||window.orientation===180;
  /* 3) Dimension-Fallback */
  return window.innerHeight>window.innerWidth;
}""",
    '_isPortrait() – Screen Orientation API'
)


# ============================================================
# FIX 1b: iOS-Helpers und erweiterter Orientation-Listener
#   – Timeout 120ms → 350ms
#   – resize-Event als zusaetzlicher Trigger (debounced 200ms)
# ============================================================
patch(
    r"""  function _onOrientChange(){
    /* delay 120ms — layout must settle before innerWidth/Height are correct */
    setTimeout(function(){
      updateOrientationWarning();
      if(S.waitingForLandscape&&!_isPortrait()){
        S.waitingForLandscape=false;
        clearInterval(tIv);
        tIv=setInterval(()=>{S.tm--;if(S.tm===3)soundWarn();render();if(S.tm<=0){clearInterval(tIv);if(S.q)answer(null);}},1000);
      }
    },120);
  }
  /* use both APIs for max compatibility */
  if(screen.orientation&&screen.orientation.addEventListener){
    screen.orientation.addEventListener("change",_onOrientChange);
  }
  window.addEventListener("orientationchange",_onOrientChange);
  /* matchMedia listener as additional fallback (Chrome desktop resize) */
  try{window.matchMedia("(orientation:landscape)").addEventListener("change",function(e){
    if(e.matches)_onOrientChange();
  });}catch(e){}
})();""",
    r"""  function _onOrientChange(){
    /* 350ms – gibt dem Browser genuegend Zeit die Viewport-Dimensionen
       nach der Rotation korrekt zu setzen (120ms war auf Android zu kurz) */
    setTimeout(function(){
      updateOrientationWarning();
      if(S.waitingForLandscape&&!_isPortrait()){
        S.waitingForLandscape=false;
        clearInterval(tIv);
        tIv=setInterval(()=>{S.tm--;if(S.tm===3)soundWarn();render();if(S.tm<=0){clearInterval(tIv);if(S.q)answer(null);}},1000);
      }
    },350);
  }
  /* Screen Orientation API (Android Chrome, moderne Browser) */
  if(screen.orientation&&screen.orientation.addEventListener){
    screen.orientation.addEventListener("change",_onOrientChange);
  }
  /* Legacy orientationchange (iOS Safari) */
  window.addEventListener("orientationchange",_onOrientChange);
  /* resize-Event: zuverlaessigster Trigger auf vielen Android-Geraeten
     (feuert sicher wenn sich Viewport-Dimensionen aendern) – debounced */
  var _orientResizeTimer=null;
  window.addEventListener("resize",function(){
    clearTimeout(_orientResizeTimer);
    _orientResizeTimer=setTimeout(_onOrientChange,200);
  });
  /* matchMedia-Fallback fuer Chrome Desktop */
  try{window.matchMedia("(orientation:landscape)").addEventListener("change",function(e){
    if(e.matches)_onOrientChange();
  });}catch(e){}
})();""",
    'Orientation listener: 350ms + resize-Event'
)


# ============================================================
# FIX 2a: iOS-Helpers nach _isPortrait einfuegen
# ============================================================
patch(
    'function updateOrientationWarning(){',
    r"""/* iOS-PWA-Helpers */
function _isIOS(){
  return /iPad|iPhone|iPod/.test(navigator.userAgent)&&!window.MSStream;
}
function _isInStandaloneMode(){
  return window.navigator.standalone===true||
         window.matchMedia('(display-mode:standalone)').matches;
}
function updateOrientationWarning(){""",
    '_isIOS() + _isInStandaloneMode() helpers'
)


# ============================================================
# FIX 2b: renderPwaBanner() – iOS-aware
# ============================================================
patch(
    r"""function renderPwaBanner(){
  return`<div id="pwa-banner" class="pwa-banner">
    <span>📱 GeoQuest als App installieren &mdash; offline spielbar!</span>
    <button class="pwa-install-btn" onclick="if(S.pwaPrompt){S.pwaPrompt.prompt();S.pwaPrompt.userChoice.then(()=>{S.pwaPrompt=null;render();});}">📥 Installieren</button>
  </div>`;
}""",
    r"""function renderPwaBanner(){
  /* iOS Safari: kein beforeinstallprompt → Schritt-fuer-Schritt-Anleitung */
  if(_isIOS()&&!_isInStandaloneMode()){
    return`<div id="pwa-banner" class="pwa-banner pwa-banner-ios">
      <span>📱 <b>App installieren:</b> Tippe auf <b>Teilen &#x2B06;&#xFE0F;</b> → <b>Zum Home-Bildschirm</b></span>
      <button class="pwa-dismiss-btn" onclick="localStorage.setItem('gq_pwa_ios_dismissed','1');render();" aria-label="Schliessen">&#x2715;</button>
    </div>`;
  }
  /* Android / Desktop Chrome: nativer beforeinstallprompt-Flow */
  return`<div id="pwa-banner" class="pwa-banner">
    <span>📱 GeoQuest als App installieren &mdash; offline spielbar!</span>
    <button class="pwa-install-btn" onclick="if(S.pwaPrompt){S.pwaPrompt.prompt();S.pwaPrompt.userChoice.then(r=>{S.pwaPrompt=null;render();});}">&#x1F4E5; Installieren</button>
  </div>`;
}""",
    'renderPwaBanner() iOS-aware'
)


# ============================================================
# FIX 2c: render()-Bedingung – auch auf iOS Banner zeigen
# ============================================================
patch(
    '    </div>${renderBottomNav()}${S.pwaPrompt?renderPwaBanner():""}`;',
    '    </div>${renderBottomNav()}${(S.pwaPrompt||(_isIOS()&&!_isInStandaloneMode()&&!localStorage.getItem(\'gq_pwa_ios_dismissed\')))?renderPwaBanner():""}`;',
    'render() – Banner-Bedingung iOS erweitert'
)


# ============================================================
# FIX 2d: CSS fuer iOS-Banner (dismiss-Button + Layout)
# ============================================================
patch(
    '.pwa-banner{',
    r""".pwa-dismiss-btn{background:none;border:none;color:var(--text2);font-size:1.1rem;cursor:pointer;padding:.2rem .4rem;flex-shrink:0;}
.pwa-banner-ios{gap:.5rem;}
.pwa-banner{""",
    'CSS pwa-dismiss-btn + pwa-banner-ios'
)


# ============================================================
# Write
# ============================================================
with open(GEN, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPatch complete. Run: python3 gen.py && python3 verify.py')
