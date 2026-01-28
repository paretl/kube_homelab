#!/usr/bin/env python3

"""
Update README.md with Claude's help by analyzing the repository structure.
This script is run by GitHub Actions to keep the README in sync with the project.
"""

import os
import sys
from pathlib import Path
from anthropic import Anthropic

def read_file(filepath):
    """Read file contents."""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def write_file(filepath, content):
    """Write content to file."""
    with open(filepath, 'w') as f:
        f.write(content)

def get_tree_output():
    """Get the directory tree output."""
    tree_file = "/tmp/tree.txt"
    if os.path.exists(tree_file):
        return read_file(tree_file)
    
    # Fallback if tree.txt doesn't exist
    import subprocess
    try:
        result = subprocess.run(
            ["find", ".", "-maxdepth", "3", "-not", "-path", "*/.*", "-not", "-path", "*/__pycache__*"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent
        )
        return result.stdout
    except Exception as e:
        print(f"Error generating tree: {e}")
        return ""

def extract_sections(readme_content):
    """Extract README sections before and after Project Structure."""
    lines = readme_content.split('\n')
    
    # Find "## Project Structure" line
    structure_idx = None
    next_section_idx = None
    
    for i, line in enumerate(lines):
        if line.startswith('## Project Structure'):
            structure_idx = i
        elif structure_idx is not None and line.startswith('## ') and i > structure_idx:
            next_section_idx = i
            break
    
    if structure_idx is None:
        # No Project Structure section found, return full content
        return readme_content, "", readme_content
    
    # Extract sections
    before = '\n'.join(lines[:structure_idx]).rstrip()
    
    if next_section_idx is None:
        # Project Structure is the last section
        after = ""
    else:
        after = '\n'.join(lines[next_section_idx:])
    
    return before, after, readme_content

def update_readme_with_claude():
    """Call Claude to update the README structure section."""
    
    api_key = os.getenv('CLAUDE_API_KEY')
    if not api_key:
        print("Error: CLAUDE_API_KEY environment variable not set")
        sys.exit(1)
    
    # Read current README
    readme_path = Path(__file__).parent.parent.parent / "README.md"
    current_readme = read_file(readme_path)
    
    # Get directory tree
    tree = get_tree_output()
    
    # Extract sections
    before_section, after_section, _ = extract_sections(current_readme)
    
    # Create Claude client
    client = Anthropic()
    
    # Prepare the prompt
    prompt = f"""You are a technical documentation expert. I need you to update the README.md for a Kubernetes homelab project.

Here is the current repository structure:
```
{tree}
```

Here is the BEFORE part of the README (keep this exactly as-is):
```
{before_section}
```

Here is the AFTER part of the README (keep this exactly as-is):
```
{after_section}
```

Please generate ONLY the "## Project Structure" section that fits between the BEFORE and AFTER parts.

Requirements:
1. Use a formatted directory tree (with ├──, └──, │ characters)
2. Add descriptive comments for each file/folder
3. Keep it well-organized and readable
4. Make sure it accurately reflects the actual repository structure provided
5. Return ONLY the section starting with "## Project Structure" and ending before the next section

The output should be valid Markdown and ready to insert directly into the README."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract the response
        structure_section = message.content[0].text
        
        # Build the new README
        new_readme = f"{before_section}\n\n{structure_section}\n\n{after_section}"
        
        # Ensure proper file ending
        new_readme = new_readme.rstrip() + '\n'
        
        # Write back to file
        write_file(readme_path, new_readme)
        
        print("✓ README.md updated successfully with Claude")
        print(f"\nUpdated section preview:\n{structure_section[:500]}...\n")
        
    except Exception as e:
        print(f"Error updating README with Claude: {e}")
        sys.exit(1)

if __name__ == "__main__":
    update_readme_with_claude()
