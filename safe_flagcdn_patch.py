with open('gen.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Exakter Austausch des Emoji-Codes gegen FlagCDN (Kein Regex!)
old_emoji_code = """        // Wandelt ISO Code (z.B. DE) in Emoji Flagge um
        const getFlagEmoji = (countryCode) => countryCode.toUpperCase().replace(/./g, char => String.fromCodePoint(char.charCodeAt(0) + 127397));

        return '<button class="' + cls + '" onclick="checkAns(&quot;' + cc + '&quot;)" style="font-size: 3rem; line-height: 1; padding: 10px;">' + getFlagEmoji(cc) + '</button>';"""

new_flagcdn_code = """        return '<button class="' + cls + '" onclick="checkAns(&quot;' + cc + '&quot;)"><img src="https://flagcdn.com/w120/' + cc.toLowerCase() + '.png" style="height:45px; border-radius:4px; pointer-events:none; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></button>';"""

content = content.replace(old_emoji_code, new_flagcdn_code)

# 2. Timeout Mojibake fixen
content = content.replace("â±", "⏳")
content = content.replace("â†'", "→")

with open('gen.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] Bulletproof String-Replace erfolgreich!")
