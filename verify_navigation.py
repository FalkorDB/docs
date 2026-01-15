#!/usr/bin/env python3
"""
Verify that all pages referenced in sidebars.ts exist in the docs directory
"""
import re
from pathlib import Path
import json

def extract_doc_ids_from_sidebars(sidebars_path):
    """Extract all doc IDs referenced in sidebars.ts"""
    with open(sidebars_path, 'r') as f:
        content = f.read()
    
    # Find all string literals that look like doc paths
    # Pattern matches: 'path/to/doc' or "path/to/doc"
    doc_patterns = [
        r"'([a-zA-Z0-9/_-]+)'",  # Single quotes
        r'"([a-zA-Z0-9/_-]+)"',  # Double quotes
    ]
    
    doc_ids = set()
    for pattern in doc_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            # Filter out non-doc paths (like 'label', 'type', etc.)
            if '/' in match or match in ['index', 'datatypes', 'References', 'license']:
                doc_ids.add(match)
    
    return sorted(doc_ids)

def check_docs_exist(doc_ids, docs_dir):
    """Check if all doc IDs have corresponding files"""
    missing = []
    found = []
    
    for doc_id in doc_ids:
        # Try different extensions
        possible_paths = [
            docs_dir / f"{doc_id}.md",
            docs_dir / f"{doc_id}.mdx",
        ]
        
        exists = any(p.exists() for p in possible_paths)
        
        if exists:
            found.append(doc_id)
        else:
            missing.append(doc_id)
    
    return found, missing

def find_orphaned_docs(docs_dir, doc_ids):
    """Find markdown files that exist but aren't in the sidebar"""
    all_md_files = []
    
    for ext in ['*.md', '*.mdx']:
        for file in docs_dir.rglob(ext):
            rel_path = file.relative_to(docs_dir)
            # Convert path to doc ID format
            doc_id = str(rel_path.with_suffix(''))
            if doc_id not in doc_ids:
                all_md_files.append(doc_id)
    
    return sorted(all_md_files)

def main():
    workspace = Path('/Users/danshalev/docs-staging')
    sidebars_path = workspace / 'website' / 'sidebars.ts'
    docs_dir = workspace / 'website' / 'docs'
    
    print("=" * 70)
    print("NAVIGATION VERIFICATION REPORT")
    print("=" * 70)
    print()
    
    # Extract all doc IDs from sidebars
    print("📋 Extracting doc IDs from sidebars.ts...")
    doc_ids = extract_doc_ids_from_sidebars(sidebars_path)
    print(f"   Found {len(doc_ids)} doc references")
    print()
    
    # Check if files exist
    print("🔍 Checking if all referenced docs exist...")
    found, missing = check_docs_exist(doc_ids, docs_dir)
    
    if missing:
        print(f"   ❌ MISSING FILES: {len(missing)}")
        for doc_id in missing:
            print(f"      - {doc_id}")
    else:
        print(f"   ✅ All {len(found)} referenced docs exist!")
    print()
    
    # Check for orphaned files
    print("🔍 Checking for orphaned docs (exist but not in sidebar)...")
    orphaned = find_orphaned_docs(docs_dir, doc_ids)
    
    if orphaned:
        print(f"   ⚠️  ORPHANED FILES: {len(orphaned)}")
        for doc_id in orphaned:
            print(f"      - {doc_id}")
    else:
        print("   ✅ No orphaned files found!")
    print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total docs in sidebar: {len(doc_ids)}")
    print(f"Existing docs: {len(found)}")
    print(f"Missing docs: {len(missing)}")
    print(f"Orphaned docs: {len(orphaned)}")
    print()
    
    if missing:
        print("❌ NAVIGATION HAS ERRORS - Some referenced docs don't exist")
        return 1
    elif orphaned:
        print("⚠️  NAVIGATION IS INCOMPLETE - Some docs aren't in sidebar")
        return 0
    else:
        print("✅ NAVIGATION IS FULLY VERIFIED - All docs accounted for!")
        return 0

if __name__ == '__main__':
    exit(main())
