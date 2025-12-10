#!/usr/bin/env python3
import os
from pathlib import Path

# Import our strategies
from strategies.text import TextStrategy
from strategies.symlink import SymlinkStrategy

# CONFIGURATION
REPO_ROOT = Path.cwd().resolve()
SOURCE_ROOT = (REPO_ROOT / "vendor/ml4w/dotfiles").resolve()

def is_text_file(filepath):
    """
    Robust heuristic: Read the first 1024 bytes.
    If we find a NULL byte (0x00), it's likely a binary file (image, executable).
    If not, we treat it as text.
    """
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
        
        # Files with a NULL byte are likely binary
        if b'\0' in chunk:
            return False
            
        # Empty files are treated as text
        return True
    except Exception as e:
        print(f"⚠️ Warning: Could not read {filepath}, defaulting to symlink. ({e})")
        return False

def generate_wrappers():
    print(f"🚀 Starting Smart Generator...")
    print(f"   Source: {SOURCE_ROOT}")

    text_strategy = TextStrategy()
    symlink_strategy = SymlinkStrategy()

    count_text = 0
    count_sym = 0

    for root, dirs, files in os.walk(SOURCE_ROOT):
        for filename in files:
            source_file = Path(root) / filename
            
            # --- THE NEW LOGIC ---
            # No more checking extensions lists. Check the content.
            if is_text_file(source_file):
                text_strategy.process(source_file, REPO_ROOT)
                count_text += 1
            else:
                symlink_strategy.process(source_file, REPO_ROOT)
                count_sym += 1

    print(f"✅ Generation Complete.")
    print(f"   Templates: {count_text}")
    print(f"   Symlinks:  {count_sym}")

if __name__ == "__main__":
    if not SOURCE_ROOT.exists():
        print(f"❌ Error: Submodule not found at {SOURCE_ROOT}")
        exit(1)
    generate_wrappers()