import re

with open('gen.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Wir suchen den gesamten flagsel Block
pattern = r'if\s*\(\s*q\.type\s*===\s*["\']flagsel["\']\s*\)\s*\{.*?answerHtml.*?\}else\s*\{'

# Wir setzen den bewährten img-Tag von flagcdn ein, exakt so wie er im anderen Modus funktioniert!
safe_img_js = """if(q.type==="flagsel"){
    const fb2 = q.opts.map(cc => {
        let cls = "btn-base";
        if(typeof sel !== 'undefined' && sel !== null){
            if(cc === q.ans) cls += " ok";
            else if(cc === sel) cls += " ng";
            else cls += " dm";
        }
        return '<button class="' + cls + '" onclick="checkAns(&quot;' + cc + '&quot;)"><img src="https://flagcdn.com/h80/' + cc.toLowerCase() + '.png" style="max-height:50px; border-radius:4px; pointer-events:none; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></button>';
    }).join('');
    answerHtml = '<div class="flag-grid">' + fb2 + '</div>';
}else{"""

content = re.sub(pattern, safe_img_js, content, flags=re.DOTALL)

with open('gen.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] FlagCDN Restore erfolgreich!")
