import re
from pathlib import Path

def fix_curly_braces_everywhere(file_path):
    """Escape ALL curly braces in the file for MDX compatibility"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace all occurrences of {word} with \{word\} 
        # but avoid doing it inside code blocks (between triple backticks)
        lines = content.split('\n')
        new_lines = []
        in_code_block = False
        
        for line in lines:
            # Track code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                new_lines.append(line)
                continue
            
            # If not in code block and line contains {something}, escape it
            if not in_code_block and '{' in line and '}' in line:
                # Replace {word} patterns with \{word\}
                # But be careful not to double-escape
                if not '\\{' in line:
                    line = re.sub(r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}', r'\\{\1\\}', line)
            
            new_lines.append(line)
        
        new_content = '\n'.join(new_lines)
        
        if new_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False
    
    return False

# Fix the rest.md file
file_path = Path('website/docs/integration/rest.md')
if fix_curly_braces_everywhere(file_path):
    print(f"Fixed curly braces in: {file_path}")
else:
    print(f"No changes needed or error in: {file_path}")
