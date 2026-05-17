#!/usr/bin/env python3
import re
import json

with open('GeoQuest.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the script section
script_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if not script_match:
    print("ERROR: No script tag found!")
    exit(1)

script = script_match.group(1)

# Check for common syntax errors
errors = []

# Check for unmatched braces
open_braces = script.count('{')
close_braces = script.count('}')
if open_braces != close_braces:
    errors.append(f"Brace mismatch: {open_braces} open, {close_braces} close")

# Check for unmatched parentheses
open_parens = script.count('(')
close_parens = script.count(')')
if open_parens != close_parens:
    errors.append(f"Parenthesis mismatch: {open_parens} open, {close_parens} close")

# Check for unmatched quotes (simple check)
single_quotes = script.count("'") - script.count("\\'")
double_quotes = script.count('"') - script.count('\\"')
if single_quotes % 2 != 0:
    errors.append(f"Single quote mismatch: {single_quotes} quotes")
if double_quotes % 2 != 0:
    errors.append(f"Double quote mismatch: {double_quotes} quotes")

# Check for orphaned semicolons or syntax patterns
if 'createCooldownWrapper(()=>{' in script:
    errors.append("WARNING: createCooldownWrapper lambda still present!")

# Check for common patterns in specialty handlers
if 'function handleLogicAnswerClick' in script:
    if 'if(S.isProcessing)return;' in script:
        print("[OK] handleLogicAnswerClick has S.isProcessing check")
    else:
        print("[WARN] handleLogicAnswerClick missing S.isProcessing check")

if errors:
    print("\nERRORS FOUND:")
    for error in errors:
        print(f"  - {error}")
    exit(1)
else:
    print("\n[OK] No obvious syntax errors detected!")
    print(f"Script size: {len(script)} chars")
    print(f"Braces: {open_braces} matched")
    print(f"Parentheses: {open_parens} matched")
    exit(0)
