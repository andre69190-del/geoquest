# -*- coding: utf-8 -*-
"""
Phase: 584
Date:  2026-07-19
Scope: Security-Fixes — XSS-Escaping fuer Usernamen, Admin-Check ohne E-Mail,
       PWA-URL-Vereinheitlichung auf /play (manifest start_url + SW-Precache)

Fixes:
1. Stored XSS: Leaderboard rendert r.username jetzt via esc()
2. Self-XSS: value-Attribute authUsername/authEmail via esc()
3. Profil-Name via esc()
4. Admin-Gating: statt E-Mail-Vergleich (PII im Client!) jetzt
   sbUser.app_metadata.admin === true  (serverseitig gesetzt, nicht user-editierbar)
   -> SQL dazu: patches/584_security_rls_fix.sql
5. manifest start_url + SW-Precache: './GeoQuest.html' -> '/play' (kanonische URL)
"""
import io, sys

PATH = 'gen.py'
with io.open(PATH, 'r', encoding='utf-8') as f:
    c = f.read()

def rep(old, new, n=1):
    cnt = c.count(old)
    assert cnt == n, "Expected %d, found %d: %r" % (n, cnt, old[:80])
    return c.replace(old, new)

# 1. Stored XSS Leaderboard
c = rep("${r.username||'Anonym'}", "${esc(r.username||'Anonym')}")

# 2. Attribut-Injection Auth-Formulare
c = rep('value="${S.authUsername}"', 'value="${esc(S.authUsername)}"')
c = rep('value="${S.authEmail}"', 'value="${esc(S.authEmail)}"', n=2)

# 3. Profil-Name
c = rep('${name||"Spieler"}<button', '${esc(name)||"Spieler"}<button')

# 4. Admin-Check ohne E-Mail im Client
c = rep('const isAdmin=sbUser?.email==="andre69190@gmail.com";',
        'const isAdmin=sbUser?.app_metadata?.admin===true;')
c = rep('if(sbUser?.email!=="andre69190@gmail.com")return;',
        'if(sbUser?.app_metadata?.admin!==true)return;')
c = rep('if(sbUser?.email!=="andre69190@gmail.com")return`',
        'if(sbUser?.app_metadata?.admin!==true)return`')
c = rep("(typeof sbUser!=='undefined'&&sbUser&&sbUser.email==='andre69190@gmail.com')",
        "(typeof sbUser!=='undefined'&&sbUser&&sbUser.app_metadata&&sbUser.app_metadata.admin===true)")

# 4b. Tote Adresse kontakt@geoquest.app -> offizielle Kontaktadresse (wie Impressum)
c = rep('<a href="mailto:kontakt@geoquest.app" style="color:var(--text3);text-decoration:none">kontakt@geoquest.app</a>',
        '<a href="mailto:farndt691@gmail.com" style="color:var(--text3);text-decoration:none">farndt691@gmail.com</a>')

# 5. Kanonische URL /play
c = rep("'start_url': './GeoQuest.html',", "'start_url': '/play',")
c = rep("_cache_assets = ['./GeoQuest.html', './manifest.json', './icon.svg'] + _data_files",
        "_cache_assets = ['/play', './manifest.json', './icon.svg'] + _data_files")
c = rep("_precache_assets = ['./GeoQuest.html', './manifest.json', './icon.svg']",
        "_precache_assets = ['/play', './manifest.json', './icon.svg']")

with io.open(PATH, 'w', encoding='utf-8') as f:
    f.write(c)

print("[OK] patch_584_security_fixes: 11 Ersetzungen angewendet")
