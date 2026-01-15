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

def find_h1_headings(content):
    """Find all H1 headings (# ) and their line numbers"""
    lines = content.split('\n')
    h1_headings = []
    for i, line in enumerate(lines, 1):
        # Match H1 headings but not comments in code blocks
        if re.match(r'^# [^#]', line):
            h1_headings.append((i, line.strip()))
    return h1_headings

def normalize_text(text):
    """Normalize text for comparison"""
    return re.sub(r'[^a-z0-9]', '', text.lower())

docs_dir = Path('website/docs')
results = []

# Process both .md and .mdx files
for pattern in ['*.md', '*.mdx']:
    for md_file in docs_dir.rglob(pattern):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter_title = extract_frontmatter_title(content)
            h1_headings = find_h1_headings(content)
            
            if frontmatter_title and h1_headings:
                normalized_title = normalize_text(frontmatter_title)
                for line_num, h1_text in h1_headings:
                    h1_content = h1_text[2:].strip()  # Remove "# "
                    normalized_h1 = normalize_text(h1_content)
                    
                    # Check for exact match or very similar match
                    if normalized_h1 == normalized_title or normalized_title in normalized_h1 or normalized_h1 in normalized_title:
                        relative_path = md_file.relative_to(Path('website/docs'))
                        results.append({
                            'file': str(relative_path),
                            'line': line_num,
                            'h1': h1_text,
                            'frontmatter_title': frontmatter_title
                        })
                        break
        except Exception as e:
            print(f"Error processing {md_file}: {e}")

# Sort results by file path
results.sort(key=lambda x: x['file'])

print(f"Found {len(results)} files with duplicate H1 headings:\n")
print("="*80)
for result in results:
    print(f"\nFile: {result['file']}")
    print(f"Line: {result['line']}")
    print(f"Heading: {result['h1']}")
    print(f"Frontmatter Title: {result['frontmatter_title']}")
    print("-"*80)
