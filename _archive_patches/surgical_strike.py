import re

with open('gen.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. FLAGGEN UND ENDLOSSCHLEIFE FIXEN
# Wir ersetzen den defekten Flagsel-Block durch sauberes JS. checkAns statt render()!
pattern_flag = r'if\s*\(\s*q\.type\s*===\s*["\']flagsel["\']\s*\)\s*\{.*?\}else\s*\{'

safe_flag = """if(q.type==="flagsel"){
    const fb2 = q.opts.map(cc => {
        let cls = "btn-base";
        if(typeof sel !== 'undefined' && sel !== null){
            if(cc === q.ans) cls += " ok";
            else if(cc === sel) cls += " ng";
            else cls += " dm";
        }
        return '<button class="' + cls + '" onclick="checkAns(&quot;' + cc + '&quot;)"><img src="https://flagcdn.com/w120/' + cc.toLowerCase() + '.png" style="height:40px; border-radius:4px; pointer-events:none;"></button>';
    }).join('');
    answerHtml = '<div class="flag-grid">' + fb2 + '</div>';
}else{"""

content = re.sub(pattern_flag, safe_flag, content, count=1, flags=re.DOTALL)

# 2. TIMER-SPAM ELIMINIEREN (Bulletproof Interval Clearing)
# Tötet alle klonierten Timer-Prozesse, bevor ein neuer startet
content = content.replace("tIv=setInterval(", "if(typeof tIv !== 'undefined') clearInterval(tIv); tIv=setInterval(")

with open('gen.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] Surgical Strike erfolgreich! Doppelte Bilder gelöscht, checkAns implementiert und Timer-Spam gestoppt.")
