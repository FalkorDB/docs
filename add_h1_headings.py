#!/usr/bin/env python3
"""Add H1 headings to all markdown files missing them."""

import os
import re
from pathlib import Path

def has_h1_heading(content_after_frontmatter):
    """Check if content has an H1 heading."""
    lines = content_after_frontmatter.strip().split('\n')
    for line in lines[:10]:  # Check first 10 lines
        if line.strip().startswith('# '):
            return True
    return False

def extract_title_from_frontmatter(content):
    """Extract title from YAML frontmatter."""
    match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
    if match:
        frontmatter = match.group(1)
        title_match = re.search(r'^title:\s*(.+)$', frontmatter, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
            # Remove quotes if present
            title = title.strip('"').strip("'")
            return title
    return None

def add_h1_heading(filepath):
    """Add H1 heading to a file if it's missing."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file has frontmatter
    if not content.startswith('---'):
        return False
    
    # Extract title
    title = extract_title_from_frontmatter(content)
    if not title:
        return False
    
    # Split at end of frontmatter
    match = re.search(r'^---\s*\n.*?\n---\s*\n', content, re.DOTALL | re.MULTILINE)
    if not match:
        return False
    
    frontmatter_end = match.end()
    frontmatter = content[:frontmatter_end]
    after_frontmatter = content[frontmatter_end:]
    
    # Check if H1 already exists
    if has_h1_heading(after_frontmatter):
        return False
    
    # Add H1 heading
    new_content = f"{frontmatter}\n# {title}\n{after_frontmatter}"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    """Process all markdown files in website/docs."""
    docs_dir = Path('/Users/danshalev/docs-staging/website/docs')
    
    fixed_files = []
    
    for md_file in docs_dir.rglob('*.md'):
        if add_h1_heading(md_file):
            rel_path = md_file.relative_to(docs_dir)
            fixed_files.append(str(rel_path))
            print(f"✓ Added H1 to: {rel_path}")
    
    print(f"\n{'='*60}")
    print(f"Fixed {len(fixed_files)} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
