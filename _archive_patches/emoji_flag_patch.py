import re

with open('gen.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Wir suchen den generierten JavaScript-Block für die Flaggen
pattern = r"""if\(q\.type==="flagsel"\)\{\s*const fb2 = q\.opts\.map\(cc => \{\s*let cls = "btn-base";\s*if\(typeof sel !== 'undefined' && sel !== null\)\{\s*if\(cc === q\.ans\) cls \+= " ok";\s*else if\(cc === sel\) cls \+= " ng";\s*else cls \+= " dm";\s*\}\s*return '<button class="' \+ cls \+ '" onclick="checkAns\(&quot;' \+ cc \+ '&quot;\)"><img src="https://flagcdn\.com/w120/' \+ cc\.toLowerCase\(\) \+ '\.png" style="height:40px; border-radius:4px; pointer-events:none;"></button>';\s*\}\)\.join\(''\);\s*answerHtml = '<div class="flag-grid">' \+ fb2 \+ '</div>';\s*\}else\{"""

# Wir ersetzen das <img> Tag durch einen nativen Emoji-Wandler
safe_emoji_js = """if(q.type==="flagsel"){
    const fb2 = q.opts.map(cc => {
        let cls = "btn-base";
        if(typeof sel !== 'undefined' && sel !== null){
            if(cc === q.ans) cls += " ok";
            else if(cc === sel) cls += " ng";
            else cls += " dm";
        }
        // Wandelt ISO Code (z.B. DE) in Emoji Flagge um
        const getFlagEmoji = (countryCode) => countryCode.toUpperCase().replace(/./g, char => String.fromCodePoint(char.charCodeAt(0) + 127397));

        return '<button class="' + cls + '" onclick="checkAns(&quot;' + cc + '&quot;)" style="font-size: 3rem; line-height: 1; padding: 10px;">' + getFlagEmoji(cc) + '</button>';
    }).join('');
    answerHtml = '<div class="flag-grid">' + fb2 + '</div>';
}else{"""

content = re.sub(pattern, safe_emoji_js, content, flags=re.DOTALL)

with open('gen.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] Emoji Flag Patch erfolgreich angewendet!")
