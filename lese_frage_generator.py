with open('gen.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Suche die GEN object definition
gen_start = content.find('const GEN={')
if gen_start == -1:
    gen_start = content.find('const GEN = {')
if gen_start == -1:
    gen_start = content.find('const GEN =')
    
if gen_start > 0:
    snippet = content[gen_start:gen_start+2000]
    print("========== GEN OBJECT DEFINITION ==========")
    print(snippet)
    print("\n========== END SNIPPET ==========")
else:
    print("[ERROR] Konnte GEN object nicht finden!")

# Alternative: Suche nach genCityQ Funktion
gencity_idx = content.find('function genCityQ()')
if gencity_idx > 0:
    print("\n========== genCityQ FUNCTION ==========")
    print(content[gencity_idx:gencity_idx+500])
