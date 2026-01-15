#!/usr/bin/env python3
"""
Check for .md and .mdx files in website/docs that have frontmatter titles
but are missing H1 headings.
"""

import os
import re
from pathlib import Path

def extract_frontmatter_title(lines):
    """Extract title from frontmatter if it exists."""
    if not lines or not lines[0].strip().startswith('---'):
        return None
    
    in_frontmatter = False
    title = None
    
    for i, line in enumerate(lines):
        if i == 0 and line.strip() == '---':
            in_frontmatter = True
            continue
        
        if in_frontmatter:
            if line.strip() == '---':
                break
            
            # Check for title field
            title_match = re.match(r'^title:\s*(.+)$', line.strip())
            if title_match:
                title = title_match.group(1).strip()
                # Remove quotes if present
                title = title.strip('"').strip("'")
    
    return title

def has_h1_heading(lines):
    """Check if content has an H1 heading after frontmatter."""
    in_frontmatter = False
    frontmatter_ended = False
    
    for i, line in enumerate(lines):
        if i == 0 and line.strip().startswith('---'):
            in_frontmatter = True
            continue
        
        if in_frontmatter and line.strip() == '---':
            in_frontmatter = False
            frontmatter_ended = True
            continue
        
        if frontmatter_ended or not in_frontmatter:
            # Check for H1 heading (line starting with "# ")
            if line.strip().startswith('# ') and len(line.strip()) > 2:
                return True
    
    return False

def check_files(docs_dir):
    """Check all .md and .mdx files in docs directory."""
    missing_h1 = []
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(('.md', '.mdx')):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, docs_dir)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    title = extract_frontmatter_title(lines)
                    
                    # If there's a title in frontmatter but no H1 heading
                    if title and not has_h1_heading(lines):
                        missing_h1.append({
                            'path': rel_path,
                            'full_path': file_path,
                            'title': title
                        })
                
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return missing_h1

if __name__ == '__main__':
    docs_dir = '/Users/danshalev/docs-staging/website/docs'
    
    if not os.path.exists(docs_dir):
        print(f"Directory not found: {docs_dir}")
        exit(1)
    
    missing_h1_files = check_files(docs_dir)
    
    # Sort by path
    missing_h1_files.sort(key=lambda x: x['path'])
    
    # Focus on index and main section pages
    index_files = [f for f in missing_h1_files if 'index' in f['path']]
    other_main_files = [f for f in missing_h1_files if 'index' not in f['path']]
    
    print("=" * 80)
    print("FILES MISSING H1 HEADINGS")
    print("=" * 80)
    print()
    
    if index_files:
        print("INDEX PAGES:")
        print("-" * 80)
        for file in index_files:
            print(f"File: {file['path']}")
            print(f"  Title: {file['title']}")
            print(f"  Suggested H1: # {file['title']}")
            print()
    
    if other_main_files:
        print("\nOTHER PAGES:")
        print("-" * 80)
        for file in other_main_files:
            print(f"File: {file['path']}")
            print(f"  Title: {file['title']}")
            print(f"  Suggested H1: # {file['title']}")
            print()
    
    print("\n" + "=" * 80)
    print(f"TOTAL FILES MISSING H1: {len(missing_h1_files)}")
    print(f"  - Index pages: {len(index_files)}")
    print(f"  - Other pages: {len(other_main_files)}")
    print("=" * 80)
