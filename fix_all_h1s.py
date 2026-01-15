import os
import re
from pathlib import Path

def extract_frontmatter_title(content):
    """Extract title from frontmatter"""
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        title_match = re.search(r'^title:\s*(.+)$', frontmatter, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()
    return None

def find_first_h1_heading(content):
    """Find the first H1 heading and its position"""
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Match H1 headings but not comments in code blocks
        if re.match(r'^# [^#]', line):
            return i, line
    return None, None

def normalize_text(text):
    """Normalize text for comparison"""
    return re.sub(r'[^a-z0-9]', '', text.lower())

def remove_duplicate_h1(file_path):
    """Remove duplicate H1 heading from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        frontmatter_title = extract_frontmatter_title(content)
        h1_line_num, h1_text = find_first_h1_heading(content)
        
        if not frontmatter_title or h1_line_num is None:
            return False
        
        h1_content = h1_text[2:].strip()  # Remove "# "
        normalized_title = normalize_text(frontmatter_title)
        normalized_h1 = normalize_text(h1_content)
        
        # Check if they match
        if normalized_h1 == normalized_title or normalized_title in normalized_h1 or normalized_h1 in normalized_title:
            lines = content.split('\n')
            
            # Remove the H1 line
            del lines[h1_line_num]
            
            # If the next line is empty, remove it too to avoid extra spacing
            if h1_line_num < len(lines) and lines[h1_line_num].strip() == '':
                del lines[h1_line_num]
            
            # Write back
            new_content = '\n'.join(lines)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

docs_dir = Path('website/docs')
fixed_count = 0

# Process both .md and .mdx files
for pattern in ['*.md', '*.mdx']:
    for md_file in docs_dir.rglob(pattern):
        if remove_duplicate_h1(md_file):
            fixed_count += 1
            print(f"Fixed: {md_file.relative_to(docs_dir)}")

print(f"\n{'='*80}")
print(f"Fixed {fixed_count} files!")
