import re
from pathlib import Path

def extract_frontmatter_title(content):
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        title_match = re.search(r'^title:\s*(.+)$', frontmatter, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()
    return None

def normalize_text(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())

# Test with graph.list.mdx
file_path = Path('website/docs/commands/graph.list.mdx')
with open(file_path, 'r') as f:
    content = f.read()

title = extract_frontmatter_title(content)
print(f'Title: {title}')
print(f'Normalized: {normalize_text(title)}')

# Check H1
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if re.match(r'^# [^#]', line):
        h1_content = line[2:].strip()
        print(f'H1 at line {i}: {line}')
        print(f'H1 content: {h1_content}')
        print(f'Normalized H1: {normalize_text(h1_content)}')
        print(f'Match: {normalize_text(title) == normalize_text(h1_content)}')
        break
