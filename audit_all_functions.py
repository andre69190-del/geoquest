#!/usr/bin/env python3
"""Complete audit of all critical functions in gen.py"""

import re

with open('gen.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("="*70)
print("COMPLETE GEN.PY AUDIT - CHECKING ALL CRITICAL PATTERNS")
print("="*70)

issues = []

# 1. Check for unclosed strings/quotes
print("\n1. QUOTE BALANCE CHECK")
print("-" * 70)

lines = content.split('\n')
for i, line in enumerate(lines, 1):
    # Skip comments
    if line.strip().startswith('//') or line.strip().startswith('/*'):
        continue
    
    # Count quotes (basic check)
    single = line.count("'") - line.count("\\'")
    double = line.count('"') - line.count('\\"')
    
    if single % 2 != 0 and ('html +=' in line or 'return' in line):
        print(f"⚠️  Line {i}: Uneven single quotes: {line[:60]}")
        issues.append(f"Line {i}: Uneven single quotes")

# 2. Check for problematic patterns
print("\n2. DANGEROUS PATTERN CHECK")
print("-" * 70)

patterns_to_check = [
    ('html += "<div', 'Quote collision: html += "<div'),
    ('return "<div', 'Quote collision: return "<div'),
    ('\\${', 'Escaped template literal (should be string concat)'),
    ('</div>"', 'Wrong quote ending (should be \';)'),
    ('</div>\\";', 'Backslash + double quote ending'),
    ('return \'<', 'OK - single quote outer'),
]

for pattern, description in patterns_to_check:
    count = content.count(pattern)
    if count > 0:
        status = "❌" if "wrong" in description.lower() or "collision" in description.lower() else "✅"
        print(f"{status} Pattern '{pattern}': {count} occurrences - {description}")
        
        # Show line numbers
        for i, line in enumerate(lines, 1):
            if pattern in line and ('html' in line or 'return' in line):
                if "OK" not in description:
                    print(f"   Line {i}: {line.strip()[:70]}")
                    issues.append(f"Line {i}: {pattern}")

# 3. Check specific critical functions
print("\n3. CRITICAL FUNCTION CHECK")
print("-" * 70)

critical_functions = [
    'renderBingoGrid',
    'renderStreakBadge',
    'generateWordGenGame',
    'renderStampCell',
]

for func in critical_functions:
    if f'function {func}' in content:
        # Find function boundaries
        start = content.find(f'function {func}')
        if start > 0:
            # Find the closing brace
            brace_count = 0
            pos = content.find('{', start)
            end = pos
            for i in range(pos, len(content)):
                if content[i] == '{':
                    brace_count += 1
                elif content[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end = i
                        break
            
            func_content = content[start:end+1]
            
            # Check for issues in this function
            if '\\${' in func_content:
                print(f"❌ {func}: Contains escaped template literals (\\${{...}})")
                issues.append(f"{func}: Escaped template literals")
            elif '${' in func_content:
                print(f"✅ {func}: Uses proper template literals ({{...}})")
            elif '+' in func_content and 'html' in func_content:
                print(f"✅ {func}: Uses string concatenation")
            
            # Check quote pairs in return statements
            if 'return' in func_content:
                for line in func_content.split('\n'):
                    if 'return' in line:
                        if 'return "<' in line and '="' in line:
                            print(f"⚠️  {func}: Potential quote collision in return")
                            issues.append(f"{func}: Quote collision in return")
                        elif 'return \'<' in line:
                            print(f"✅ {func}: Proper single quote return")

# 4. Summary
print("\n" + "="*70)
if issues:
    print(f"❌ FOUND {len(issues)} ISSUES:")
    for issue in issues:
        print(f"   - {issue}")
else:
    print("✅ NO CRITICAL ISSUES FOUND IN GEN.PY")

print("="*70)
