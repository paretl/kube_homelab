#!/bin/bash

# Generate a formatted directory tree for the README
# This script is called by GitHub Actions before updating the README with Claude

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Directories and files to exclude
EXCLUDE_DIRS=".git|.venv|.helm|__pycache__|node_modules|.github/workflows"

# Try using tree command if available (produces best output)
if command -v tree &> /dev/null; then
    tree -L 3 --dirsfirst -I "$EXCLUDE_DIRS" "$REPO_ROOT" 2>/dev/null || fallback_tree
else
    fallback_tree
fi

# Fallback function for when tree command is not available
fallback_tree() {
    echo "kube_homelab/"
    
    # Use find to generate tree structure with proper formatting
    find "$REPO_ROOT" -maxdepth 3 -type f -o -type d 2>/dev/null | \
    grep -v -E "\.git|\.venv|\.helm|__pycache__|node_modules|\.github/workflows" | \
    sed 's|'"$REPO_ROOT"'||g' | \
    sed 's|^/||g' | \
    grep -v '^$' | \
    sort | \
    awk '
    BEGIN {
        OFS = ""
        FS = "/"
    }
    {
        depth = NF - 1
        name = $NF
        
        # Skip root
        if (depth == 0) next
        
        # Build tree characters
        prefix = ""
        for (i = 1; i < depth; i++) {
            prefix = prefix "│   "
        }
        
        # Check if file or directory
        if (system("test -d \"'"$REPO_ROOT"'/" $0 "\"") == 0) {
            suffix = "/"
        } else {
            suffix = ""
        }
        
        # Alternate between ├── and └──
        if (NR % 2 == 0) {
            print prefix "├── " name suffix
        } else {
            print prefix "└── " name suffix
        }
    }
    '
}
