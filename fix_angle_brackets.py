#!/usr/bin/env python3
"""
Fix < > characters in markdown that should be escaped
"""
import re
from pathlib import Path

DOCS_DIR = Path("/Users/danshalev/docs-staging/website/docs")

def fix_angle_brackets(file_path):
    """Fix unescaped angle brackets in markdown"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Pattern to find < > that are not:
    # - Part of HTML/JSX tags (<div>, </div>, <Tabs>, etc.)
    # - In code blocks
    # - Already escaped
    
    # Split by code blocks to avoid modifying code
    parts = re.split(r'(```[\s\S]*?```|`[^`]+`)', content)
    
    fixed_parts = []
    for i, part in enumerate(parts):
        # Skip code blocks (odd indices)
        if i % 2 == 1:
            fixed_parts.append(part)
            continue
        
        # Fix angle brackets that look like placeholders (not real HTML tags)
        # Match patterns like: <sub_cmd>, <Lib>, <script>, etc.
        # But not: <div>, </div>, <Tabs>, <TabItem>, etc.
        
        # Pattern: < followed by lowercase or underscore (not capital letter = not a Component)
        # and not followed by / (not a closing tag)
        part = re.sub(r'<([a-z_][a-z0-9_]*)>', r'`<\1>`', part)
        
        # Also fix capital letter placeholders that don't look like components
        # Match <Word> where Word starts with capital but isn't a known component
        known_components = ['Tabs', 'TabItem', 'details', 'summary', 'br', 'hr', 'img', 'a', 'p', 'div', 'span']
        
        def replace_placeholder(match):
            tag = match.group(1)
            # If it's a known component, leave it
            if tag in known_components:
                return match.group(0)
            # If it looks like a placeholder (single word, simple), escape it
            if re.match(r'^[A-Z][a-z]*$', tag) or '_' in tag:
                return f'`<{tag}>`'
            return match.group(0)
        
        part = re.sub(r'<([A-Z][a-zA-Z0-9_]*)>', replace_placeholder, part)
        
        fixed_parts.append(part)
    
    content = ''.join(fixed_parts)
    
    # Only write if changed
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    """Main function"""
    fixed_count = 0
    
    for file_path in DOCS_DIR.rglob("*.md"):
        try:
            if fix_angle_brackets(file_path):
                print(f"Fixed: {file_path.relative_to(DOCS_DIR)}")
                fixed_count += 1
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    for file_path in DOCS_DIR.rglob("*.mdx"):
        try:
            if fix_angle_brackets(file_path):
                print(f"Fixed: {file_path.relative_to(DOCS_DIR)}")
                fixed_count += 1
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"\nTotal files fixed: {fixed_count}")

if __name__ == "__main__":
    main()
