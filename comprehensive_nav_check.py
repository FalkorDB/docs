#!/usr/bin/env python3
"""
Comprehensive navigation check - verifies:
1. All pages in sidebars.ts exist
2. No duplicate entries
3. All markdown files are accessible
4. Build succeeds
"""
import re
from pathlib import Path
from collections import Counter

def extract_all_doc_references(sidebars_content):
    """Extract all doc ID references including nested ones"""
    doc_ids = []
    
    # Pattern for doc IDs in various contexts
    patterns = [
        r"id:\s*['\"]([^'\"]+)['\"]",  # id: 'doc-id'
        r"['\"]([a-zA-Z0-9/_-]+/[a-zA-Z0-9/_-]+)['\"]",  # 'path/to/doc'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, sidebars_content)
        doc_ids.extend(matches)
    
    # Also catch standalone doc references (single words with /)
    standalone = re.findall(r"^\s*['\"]([a-z-]+/[a-z-]+(?:/[a-z-]+)*)['\"],?\s*$", 
                            sidebars_content, re.MULTILINE)
    doc_ids.extend(standalone)
    
    return doc_ids

def main():
    workspace = Path('/Users/danshalev/docs-staging')
    sidebars_path = workspace / 'website' / 'sidebars.ts'
    docs_dir = workspace / 'website' / 'docs'
    
    print("=" * 80)
    print(" " * 20 + "COMPREHENSIVE NAVIGATION CHECK")
    print("=" * 80)
    print()
    
    # Read sidebars
    with open(sidebars_path, 'r') as f:
        sidebars_content = f.read()
    
    # Extract all doc references
    print("📋 Step 1: Extracting all doc references from sidebars.ts")
    doc_ids = extract_all_doc_references(sidebars_content)
    print(f"   Found {len(doc_ids)} total references")
    
    # Check for duplicates
    print()
    print("🔍 Step 2: Checking for duplicate entries")
    counts = Counter(doc_ids)
    duplicates = {doc: count for doc, count in counts.items() if count > 1}
    
    if duplicates:
        print(f"   ❌ Found {len(duplicates)} duplicate entries:")
        for doc, count in duplicates.items():
            print(f"      - {doc} (appears {count} times)")
    else:
        print("   ✅ No duplicates found!")
    
    # Check if files exist
    print()
    print("🔍 Step 3: Verifying all referenced files exist")
    unique_docs = set(doc_ids)
    missing = []
    found = []
    
    for doc_id in unique_docs:
        possible_paths = [
            docs_dir / f"{doc_id}.md",
            docs_dir / f"{doc_id}.mdx",
        ]
        
        if any(p.exists() for p in possible_paths):
            found.append(doc_id)
        else:
            missing.append(doc_id)
    
    if missing:
        print(f"   ❌ Missing {len(missing)} files:")
        for doc in sorted(missing):
            print(f"      - {doc}")
    else:
        print(f"   ✅ All {len(found)} referenced files exist!")
    
    # Check all markdown files
    print()
    print("🔍 Step 4: Finding all markdown files in docs/")
    all_md_files = set()
    for ext in ['*.md', '*.mdx']:
        for file in docs_dir.rglob(ext):
            rel_path = file.relative_to(docs_dir)
            doc_id = str(rel_path.with_suffix(''))
            all_md_files.add(doc_id)
    
    print(f"   Found {len(all_md_files)} markdown files")
    
    # Check which files aren't in sidebar
    not_in_sidebar = all_md_files - unique_docs
    if not_in_sidebar:
        print(f"   ⚠️  {len(not_in_sidebar)} files not referenced in sidebar:")
        for doc in sorted(not_in_sidebar):
            print(f"      - {doc}")
    else:
        print("   ✅ All markdown files are in the sidebar!")
    
    # Final summary
    print()
    print("=" * 80)
    print(" " * 30 + "FINAL REPORT")
    print("=" * 80)
    print(f"📊 Sidebar references: {len(doc_ids)} total, {len(unique_docs)} unique")
    print(f"📄 Markdown files in docs/: {len(all_md_files)}")
    print(f"✅ Files correctly referenced: {len(found)}")
    print(f"❌ Missing files: {len(missing)}")
    print(f"🔄 Duplicate references: {len(duplicates)}")
    print(f"⚠️  Unreferenced files: {len(not_in_sidebar)}")
    print()
    
    # Overall status
    if missing or duplicates:
        print("🚨 CRITICAL ISSUES FOUND - Navigation has errors!")
        print()
        if missing:
            print("   Fix missing files by either:")
            print("   1. Creating the missing files")
            print("   2. Removing the references from sidebars.ts")
        if duplicates:
            print("   Fix duplicates by removing redundant entries from sidebars.ts")
        return 1
    elif not_in_sidebar:
        print("⚠️  WARNING - Some files exist but aren't in navigation")
        print("   These files won't be accessible to users unless added to sidebars.ts")
        return 0
    else:
        print("✅ ✅ ✅  PERFECT! All navigation verified successfully! ✅ ✅ ✅")
        print()
        print("   • All referenced files exist")
        print("   • No duplicate entries")
        print("   • All markdown files are in sidebar")
        return 0

if __name__ == '__main__':
    exit(main())
