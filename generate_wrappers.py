#!/usr/bin/env python3
import os
from pathlib import Path

# Import our strategies
from strategies.text import TextStrategy
from strategies.symlink import SymlinkStrategy

# CONFIGURATION
# We resolve paths to ensure calculations are correct
REPO_ROOT = Path.cwd().resolve()
SOURCE_ROOT = (REPO_ROOT / "vendor/ml4w/dotfiles").resolve()

TEXT_FILENAMES = {
    '.bashrc', '.zshrc', '.zshenv', '.profile', '.bash_profile',
    '.Xresources', '.gtkrc-2.0',
    '00-init', '10-aliases', '20-customization', '30-autostart', # bashrc partials
    'config', # ssh config often named just 'config'
}

TEXT_EXTENSIONS = {
    '.conf', '.sh', '.css', '.rasi', '.yuck', 
    '.xml', '.ini', '.toml', '.txt', '.md',
    '.json', '.jsonc', '.fish', '.yaml', '.yml', '.vim'
}

def generate_wrappers():
    print(f"🚀 Starting Generator...")
    print(f"   Repo Root: {REPO_ROOT}")
    print(f"   Source:    {SOURCE_ROOT}")

    text_strategy = TextStrategy()
    symlink_strategy = SymlinkStrategy()

    # Iterate through the submodule
    for root, dirs, files in os.walk(SOURCE_ROOT):
        for filename in files:
            source_file = Path(root) / filename
            suffix = source_file.suffix

            # 2. UPDATE THE CHECK LOGIC
            # Check extension OR exact filename match
            if suffix in TEXT_EXTENSIONS or filename in TEXT_FILENAMES:
                text_strategy.process(source_file, REPO_ROOT)
            else:
                symlink_strategy.process(source_file, REPO_ROOT)

    print(f"✅ Generation Complete.")

if __name__ == "__main__":
    if not SOURCE_ROOT.exists():
        print(f"❌ Error: Submodule not found at {SOURCE_ROOT}")
        exit(1)
    generate_wrappers()