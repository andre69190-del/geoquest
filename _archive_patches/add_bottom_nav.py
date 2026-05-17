with open('gen.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Die fehlende renderBottomNav Funktion hinzufügen (vor der render() Funktion)
missing_function = '''function renderBottomNav(){
  const tabs = [
    {id:"home",icon:"🏠",label:"Home"},
    {id:"lernen",icon:"📚",label:"Lernen"},
    {id:"liga",icon:"🏆",label:"Liga"},
    {id:"profil",icon:"👤",label:"Profil"},
    {id:"album",icon:"📷",label:"Album"}
  ];
  return '<div class="bottom-nav">' + tabs.map(t => {
    const active = S.tab === t.id ? " active" : "";
    return '<button class="bn-item' + active + '" onclick="S.tab=\\''+t.id+'\\';render()"><span class="bn-icon">'+t.icon+'</span><span class="bn-lbl">'+t.label+'</span></button>';
  }).join('') + '</div>';
}

'''

# Finde die Stelle, wo wir die Funktion einfügen sollen (vor "function render()")
insert_pos = content.find("function render(){")
if insert_pos > 0:
    content = content[:insert_pos] + missing_function + content[insert_pos:]

with open('gen.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] renderBottomNav() Funktion erfolgreich hinzugefügt!")
