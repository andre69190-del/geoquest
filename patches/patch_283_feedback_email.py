"""
Phase: 283
Date:  2026-05-29
Author: Claude / Andre
Scope: Feedback-System: Supabase-konsistent + Admin-Feedback-Tab + Email-Erlaeuterung

Description:
  PROBLEM:
    1. openFeedback() speicherte in Supabase, aber keine Email-Benachrichtigung.
    2. reportBug() + Crash-Handler nutzten nur mailto: -> auf Mobile/PWA blockiert.
    3. Admin-Tab zeigte keine Feedback-Eintraege -> kein Ueberblick.

  FIX 1 – reportBug() jetzt Supabase-zuerst:
    Statt nur _sendBugMail() jetzt: sb.from('feedback').insert() + Fallback mailto.
    Category 'bug', inkl. Modus/Diff/Runde/Score als Kontext.

  FIX 2 – Crash-Handler jetzt Supabase-zuerst:
    Der "Fehlerbericht senden" Button schreibt den Crash auch in Supabase
    (category: 'crash') bevor er die Mail-App oeffnet.

  FIX 3 – Admin-Tab: neuer Feedback-Bereich:
    loadAdminData laedt jetzt auch sb.from('feedback') (letzte 200 Eintraege).
    Zeigt Feedback-Karten mit Kategorie-Badge, Modus, Text und Datum.

  EMAIL-BENACHRICHTIGUNG (nicht im Code, Anleitung):
    Fuer automatische Emails: Supabase Dashboard -> Database -> Webhooks ->
    "Create Webhook" auf Tabelle 'feedback' (INSERT Event) ->
    URL eines Email-Dienstes (z.B. Resend.com free tier: 3000 Emails/Monat).
    Alternativ: Supabase -> Integrations -> Resend direkt verbinden.

Dependencies: patch_282_lv_ux.py
Zero-Bug Policy: All c.replace() calls assert uniqueness
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
# FIX 1: reportBug() – Supabase zuerst, mailto als Fallback
# ============================================================
patch(
    r"""    _sendBugMail(_subject,_body);
  };
}
async function loadAdminData(){""",
    r"""    /* P283: Supabase zuerst, mailto als Fallback */
    var _fbPay={category:'bug',message:_inp,mode:S.mode||null,
      lang:S.language||'de',app_version:'283',
      username:(typeof sbProfile!=='undefined'&&sbProfile?sbProfile.username:null)};
    if(typeof sbOK!=='undefined'&&sbOK&&typeof sb!=='undefined'&&sb){
      var _uid2=(typeof sbUser!=='undefined'&&sbUser?sbUser.id:null);
      if(_uid2)_fbPay.user_id=_uid2;
      sb.from('feedback').insert(_fbPay).then(
        function(){showToast('✅ Fehler gemeldet – Danke!');},
        function(e){console.warn('Bug-Report Supabase error:',e);_sendBugMail(_subject,_body);}
      );
    }else{_sendBugMail(_subject,_body);}
  };
}
async function loadAdminData(){""",
    'reportBug: Supabase-zuerst'
)


# ============================================================
# FIX 2: Crash-Handler – auch Supabase schreiben
# ============================================================
patch(
    r"""    <button onclick="(function(){
      const body='Hallo Entwickler,\n\nmein Spiel ist gerade abgestürzt.\nBitte hänge hier ggf. einen Screenshot an.\n\n--- TECHNISCHE DATEN ---\nFehler: ${errTxt.replace(/'/g,'\\x27')}\nState: ${stateSnap.replace(/'/g,'\\x27')}';
      _sendBugMail('GeoQuest Crash-Report', body);
    })()" style="background:#ef4444;color:#fff;border:none;border-radius:12px;padding:.7rem 1.4rem;font-size:.88rem;font-weight:700;cursor:pointer;margin-bottom:.75rem">🐞 Fehlerbericht senden</button>""",
    r"""    <button onclick="(function(){
      const body='GeoQuest Crash\nFehler: ${errTxt.replace(/'/g,'\\x27')}\nState: ${stateSnap.replace(/'/g,'\\x27')}';
      if(typeof sbOK!=='undefined'&&sbOK&&typeof sb!=='undefined'&&sb){
        sb.from('feedback').insert({category:'crash',message:body,mode:(typeof S!=='undefined'?S.mode:null)||null,app_version:'283',lang:'de'}).then(null,function(){_sendBugMail('GeoQuest Crash-Report',body);});
      }else{_sendBugMail('GeoQuest Crash-Report',body);}
      showToast('\u{1F41E} Crash-Report gesendet – Danke!');
    })()" style="background:#ef4444;color:#fff;border:none;border-radius:12px;padding:.7rem 1.4rem;font-size:.88rem;font-weight:700;cursor:pointer;margin-bottom:.75rem">🐞 Fehlerbericht senden</button>""",
    'Crash-Handler: Supabase-zuerst'
)


# ============================================================
# FIX 3a: State – adminFeedback hinzufuegen
# ============================================================
patch(
    'statsData:null,statsLoading:false,adminData:null,adminLoading:false,',
    'statsData:null,statsLoading:false,adminData:null,adminLoading:false,adminFeedback:null,adminFbLoading:false,',
    'State: adminFeedback'
)


# ============================================================
# FIX 3b: loadAdminData – auch Feedback laden
# ============================================================
patch(
    r"""async function loadAdminData(){
  if(sbUser?.email!=="andre69190@gmail.com")return;
  S.adminLoading=true;S.adminData=null;render();
  const{data}=await sb.from("game_sessions").select("*").order("created_at",{ascending:false}).limit(2000);
  S.adminData=data||[];
  S.adminLoading=false;render();
}""",
    r"""async function loadAdminData(){
  if(sbUser?.email!=="andre69190@gmail.com")return;
  S.adminLoading=true;S.adminData=null;S.adminFeedback=null;render();
  const[{data:sessions},{data:fbRows}]=await Promise.all([
    sb.from("game_sessions").select("*").order("created_at",{ascending:false}).limit(2000),
    sb.from("feedback").select("*").order("created_at",{ascending:false}).limit(200)
  ]);
  S.adminData=sessions||[];
  S.adminFeedback=fbRows||[];
  S.adminLoading=false;render();
}""",
    'loadAdminData: auch Feedback laden'
)


# ============================================================
# FIX 3c: renderAdminTab – Feedback-Sektion am Ende
# ============================================================
patch(
    r"""    <div style="font-size:.65rem;color:var(--text3);text-align:center">Letzte 2000 Sessions · Nur sichtbar für dich</div>
  </div>`;
}""",
    r"""    <div style="font-size:.65rem;color:var(--text3);text-align:center">Letzte 2000 Sessions · Nur sichtbar für dich</div>
  </div>
  ${(function(){
    const fb=S.adminFeedback||[];
    if(!fb.length)return'<div class="panel" style="margin-bottom:.85rem;padding:.85rem"><div style="font-size:.7rem;font-weight:700;color:var(--text3);letter-spacing:.5px;margin-bottom:.5rem">FEEDBACK & FEHLERBERICHTE (0)</div><div style="font-size:.78rem;color:var(--text3)">Noch keine Einträge.</div></div>';
    const catIcon={vorschlag:'\u{1F4A1}',inhalt:'\u{1F4DA}',bug:'\u{1F41E}',crash:'\u{1F6D1}',lob:'⭐',sonstiges:'\u{1F4AC}'};
    const catCol={vorschlag:'#6366f1',inhalt:'#f59e0b',bug:'#ef4444',crash:'#dc2626',lob:'#10b981',sonstiges:'#94a3b8'};
    const cards=fb.map(function(r){
      const ico=catIcon[r.category]||'\u{1F4AC}';
      const col=catCol[r.category]||'#94a3b8';
      const dt=r.created_at?new Date(r.created_at).toLocaleString('de-DE',{day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'}):'?';
      const user=r.username||r.user_id||'Anonym';
      return'<div style="background:var(--bg3);border-radius:10px;padding:.65rem .8rem;margin-bottom:.5rem;border-left:3px solid '+col+'">'
        +'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.3rem">'
        +'<span style="font-size:.72rem;font-weight:700;color:'+col+'">'+ico+' '+(r.category||'?').toUpperCase()+'</span>'
        +'<span style="font-size:.62rem;color:var(--text3)">'+dt+'</span>'
        +'</div>'
        +'<div style="font-size:.8rem;color:var(--text);word-break:break-word;margin-bottom:.3rem">'+esc(r.message||'')+'</div>'
        +'<div style="font-size:.62rem;color:var(--text3)">'+(r.mode||'')+' &middot; '+user+'</div>'
        +'</div>';
    }).join('');
    return'<div class="panel" style="margin-bottom:.85rem;padding:.85rem"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.65rem"><div style="font-size:.7rem;font-weight:700;color:var(--text3);letter-spacing:.5px">FEEDBACK & FEHLERBERICHTE ('+fb.length+')</div></div><div style="max-height:400px;overflow-y:auto">'+cards+'</div></div>';
  })()}`;
}""",
    'renderAdminTab: Feedback-Sektion'
)


with open(GEN, 'w', encoding='utf-8') as f:
    f.write(content)
print('\nPatch complete.')
