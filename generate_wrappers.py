#!/usr/bin/env python3
import os
from pathlib import Path

# Import our strategies
from strategies.text import TextStrategy
from strategies.symlink import SymlinkStrategy

# CONFIGURATION
SOURCE_ROOT = Path("vendor/ml4w/dotfiles").resolve()
DEST_ROOT = Path("dot_config").resolve()
REPO_ROOT = Path.cwd().resolve() # The root of your wrapper repo

# Extensions that should use the TextStrategy (Include & Override)
TEXT_EXTENSIONS = {
    '.conf', '.sh', '.css', '.rasi', '.yuck', 
    '.xml', '.ini', '.toml', '.txt', '.md'
}

# Future: Structured files we want to merge intelligently
# For MVP, we treat them as text or simple symlinks until the parser is ready.
# We'll treat them as text for now so they are editable.
TEXT_EXTENSIONS.update({'.json', '.jsonc'})

def generate_wrappers():
    print(f"🚀 Starting Generator...")
    print(f"   Source: {SOURCE_ROOT}")
    print(f"   Dest:   {DEST_ROOT}")

    # Instantiate strategies once
    text_strategy = TextStrategy()
    symlink_strategy = SymlinkStrategy()

    for root, dirs, files in os.walk(SOURCE_ROOT):
        # Replicate directory structure
        rel_path = Path(root).relative_to(SOURCE_ROOT)
        target_dir = DEST_ROOT / rel_path
        target_dir.mkdir(parents=True, exist_ok=True)

        for filename in files:
            source_file = Path(root) / filename
            suffix = source_file.suffix

            # DISPATCH LOGIC
            match suffix:
                case s if s in TEXT_EXTENSIONS:
                    text_strategy.process(source_file, target_dir, SOURCE_ROOT)
                
                # FUTURE: Add JSON Strategy here
                # case '.json' | '.jsonc':
                #    json_strategy.process(source_file, target_dir, SOURCE_ROOT)
                
                case _:
                    # Default fallthrough for binaries, images, etc.
                    symlink_strategy.process(source_file, target_dir, SOURCE_ROOT)

    print(f"✅ Generation Complete.")

if __name__ == "__main__":
    if not SOURCE_ROOT.exists():
        print(f"❌ Error: Submodule not found at {SOURCE_ROOT}")
        exit(1)
    generate_wrappers()