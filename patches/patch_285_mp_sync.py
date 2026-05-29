"""
Phase: 285
Date:  2026-05-29
Author: Claude / Andre
Scope: 1v1-Online-Multiplayer Sync-Fix: identische Fragen in identischer Reihenfolge

Description:
  BUG (gemeldet: "Höheres BIP" 1v1 – Fragen unterschiedlich):
    Im Online-1v1 bekamen beide Spieler trotz gleichem RNG-Seed
    UNTERSCHIEDLICHE Fragen. Zwei unabhängige Ursachen:

    URSACHE 1 – filter/diff werden nicht synchronisiert:
      Die Vergleichs-Generatoren (genCompGdpQ → _compPick → _rfilt,
      getSmartMatch) hängen von S.filter (Regions-Filter) und S.diff
      (Schwierigkeit, bestimmt Fenster-Größe W) ab. Beides sind LOKALE,
      persistente Einstellungen (S.diff aus localStorage 'gq_diffx',
      S.filter aus Regionsauswahl) und werden von startGame() NICHT
      zurückgesetzt. Das game_start-Broadcast überträgt nur {seed,mode}.
      → Spieler mit unterschiedlichem Rest-Filter/Schwierigkeit aus einem
        vorherigen Solo-Spiel ziehen aus demselben Seed andere Länder.

    URSACHE 2 – Runde 1 wird VOR dem Seed generiert:
      startGame() ruft am Ende lq() (erste Frage) auf, während rngSeed
      noch null ist (Zeile: rngSeed=null). mpCountdown() ruft initRng(seed)
      erst NACH startGame() auf. → Die erste Frage nutzt immer Math.random()
      und desynct garantiert.

  FIX (Host ist autoritativ):
    1. game_start-Payload um {filt:S.filter, dif:S.diff} erweitert
       (beide Host-Sendestellen).
    2. mpCountdown(seed,mode,filt,dif): wendet filt/dif VOR startGame an
       und übergibt den seed an startGame.
    3. Guest-Handler reicht payload.filt/payload.dif an mpCountdown durch.
    4. startGame(m,_mpSeed): optionaler Seed-Parameter → initRng() direkt
       nach dem State-Reset, also VOR dem ersten lq(). Damit ist auch
       Runde 1 seed-basiert. Das doppelte initRng nach startGame entfällt.

  Abwärtskompatibel: filt/dif werden mit Guards angewendet (undefined/null
  → keine Änderung); _mpSeed defaultet auf undefined → Solo/Daily unberührt.

Dependencies: patch_284_daily_exploit.py
Zero-Bug Policy: jeder patch() prüft Anker-Eindeutigkeit (count==1).
"""

import os
GEN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'gen.py')

with open(GEN, encoding='utf-8') as f:
    content = f.read()

def patch(old, new, label):
    global content
    cnt = content.count(old)
    if cnt == 0:
        print(f'[SKIP] {label}: anchor not found')
        return
    if cnt > 1:
        print(f'[WARN] {label}: anchor {cnt}x - using replace(1)')
    content = content.replace(old, new, 1)
    print(f'[OK]   {label}')


# ============================================================
# FIX 1: Host-Sendestelle A (player_ready-Handler)
# ============================================================
patch(
    """      if(S.mp.myReady&&S.mp.oppReady){
        const seed=~~(Math.random()*1e9);
        const mode=_getMpMode();  /* Phase 212: use UI-selected mode */
        mpSend("game_start",{seed,mode});
        mpCountdown(seed,mode);
      }""",
    """      if(S.mp.myReady&&S.mp.oppReady){
        const seed=~~(Math.random()*1e9);
        const mode=_getMpMode();  /* Phase 212: use UI-selected mode */
        const filt=S.filter,dif=S.diff;  /* P285: Filter+Schwierigkeit syncen */
        mpSend("game_start",{seed,mode,filt,dif});
        mpCountdown(seed,mode,filt,dif);
      }""",
    'Host-Sendestelle A: filt/dif in game_start'
)


# ============================================================
# FIX 2: Host-Sendestelle B (mpReady)
# ============================================================
patch(
    """  if(S.mp.role==="host"&&S.mp.oppReady){
    const seed=~~(Math.random()*1e9);
    const mode=_getMpMode();  /* Phase 212: use UI-selected mode */
    mpSend("game_start",{seed,mode});
    mpCountdown(seed,mode);
  }""",
    """  if(S.mp.role==="host"&&S.mp.oppReady){
    const seed=~~(Math.random()*1e9);
    const mode=_getMpMode();  /* Phase 212: use UI-selected mode */
    const filt=S.filter,dif=S.diff;  /* P285: Filter+Schwierigkeit syncen */
    mpSend("game_start",{seed,mode,filt,dif});
    mpCountdown(seed,mode,filt,dif);
  }""",
    'Host-Sendestelle B: filt/dif in game_start'
)


# ============================================================
# FIX 3: Guest-Handler reicht filt/dif durch
# ============================================================
patch(
    """      mpLog("game_start received:",payload);
      mpCountdown(payload.seed,payload.mode);""",
    """      mpLog("game_start received:",payload);
      mpCountdown(payload.seed,payload.mode,payload.filt,payload.dif);""",
    'Guest-Handler: filt/dif durchreichen'
)


# ============================================================
# FIX 4: mpCountdown-Signatur + filt/dif anwenden + seed an startGame
# ============================================================
patch(
    'function mpCountdown(seed,mode){',
    'function mpCountdown(seed,mode,filt,dif){',
    'mpCountdown: Signatur um filt,dif erweitert'
)

patch(
    """      startGame(mode||"city");
      initRng(seed);  /* re-set seed after startGame clears it */""",
    """      /* P285: Host-Filter + Schwierigkeit VOR startGame anwenden,
         damit Vergleichs-Pools (z.B. "Höheres BIP") auf beiden Clients gleich sind */
      if(filt!==undefined&&filt!==null)S.filter=filt;
      if(dif!==undefined&&dif!==null)S.diff=dif;
      startGame(mode||"city",seed);  /* P285: seed an startGame -> auch Runde 1 ist geseedet */""",
    'mpCountdown: filt/dif anwenden + seed an startGame (kein doppeltes initRng)'
)


# ============================================================
# FIX 5: startGame – optionaler Seed-Param, initRng VOR erstem lq()
# ============================================================
patch(
    'function startGame(m){\n  /* Phase 217 QA: 300ms nav lock -- prevents stacked game-init on rapid taps */',
    'function startGame(m,_mpSeed){\n  /* Phase 217 QA: 300ms nav lock -- prevents stacked game-init on rapid taps */',
    'startGame: optionaler _mpSeed-Parameter'
)

patch(
    'mpOpponent:null,mpOppScore:0,mpOppFinal:null,mpOppRd:0});  /* P208/P210: always reset sub-game state on new game */',
    'mpOpponent:null,mpOppScore:0,mpOppFinal:null,mpOppRd:0});  /* P208/P210: always reset sub-game state on new game */\n  if(_mpSeed!=null)initRng(_mpSeed);  /* P285: MP-Seed VOR erstem lq() -> Runde 1 synchron; Solo/Daily unberührt (undefined) */',
    'startGame: initRng(_mpSeed) vor erstem lq()'
)


# ── atomic write (verhindert Datei-Truncation bei Fehler) ──────────────
_tmp = GEN + '.tmp'
with open(_tmp, 'w', encoding='utf-8') as f:
    f.write(content)
os.replace(_tmp, GEN)
print('\nPatch complete.')
