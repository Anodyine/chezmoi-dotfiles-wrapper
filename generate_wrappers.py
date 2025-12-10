#!/usr/bin/env python3
import os
from pathlib import Path

# Import our strategies
from strategies.text import TextStrategy
from strategies.symlink import SymlinkStrategy

# CONFIGURATION
REPO_ROOT = Path.cwd().resolve()
SOURCE_ROOT = (REPO_ROOT / "vendor/ml4w/dotfiles").resolve()

# --- CUSTOM RULES ---
CUSTOM_RULES = {
    "dot_config/ml4w/settings/waybar-theme.sh": "/ml4w-modern;/ml4w-modern/default",
    "dot_config/ml4w/settings/wallpaper-effect.sh": "off",
    "dot_config/ml4w/settings/blur.sh": "50x30",
    "dot_config/waybar/themes/symlink_config": "{{ .chezmoi.homeDir }}/.config/waybar/themes/ml4w-modern/config",
    "dot_config/waybar/themes/symlink_style.css": "{{ .chezmoi.homeDir }}/.config/waybar/themes/ml4w-modern/default/style.css",
    "dot_config/rofi/symlink_config.rasi": "config-modern.rasi",
    "dot_config/nwg-dock-hyprland/symlink_style.css": "{{ .chezmoi.homeDir }}/.config/nwg-dock-hyprland/themes/modern/style.css"
}

def is_text_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
        return not (b'\0' in chunk)
    except Exception:
        return False

def generate_wrappers():
    print(f"🚀 Starting Smart Generator (Safe Mode)...")
    
    text_strategy = TextStrategy()
    symlink_strategy = SymlinkStrategy()
    
    new_files = 0
    skipped_files = 0

    # 1. Walk the Submodule
    for root, dirs, files in os.walk(SOURCE_ROOT):
        for filename in files:
            source_file = Path(root) / filename
            
            # Determine destination path to check existence
            # We simulate the strategy logic to find the dest path
            rel_path = source_file.relative_to(REPO_ROOT / "vendor/ml4w/dotfiles")
            # This logic mimics the strategy: replace dots with dot_
            parts = []
            for part in rel_path.parts:
                if part.startswith('.'):
                    parts.append('dot_' + part[1:])
                else:
                    parts.append(part)
            
            dest_name = parts[-1]
            if is_text_file(source_file):
                dest_name = f"{dest_name}.tmpl"
            else:
                dest_name = f"symlink_{dest_name}.tmpl"
            
            dest_path = REPO_ROOT.joinpath(*parts[:-1]) / dest_name
            
            # --- SAFE MODE CHECK ---
            if dest_path.exists():
                skipped_files += 1
                continue

            # If missing, generate it
            if is_text_file(source_file):
                text_strategy.process(source_file, REPO_ROOT)
            else:
                symlink_strategy.process(source_file, REPO_ROOT)
            new_files += 1

    # 2. Apply Custom Rules (Only if missing)
    print(f"💉 Checking Custom Rules...")
    for file_path, content in CUSTOM_RULES.items():
        dest_path = REPO_ROOT / file_path
        
        # Handle suffixes
        if "symlink_" in dest_path.name:
            dest_path = dest_path.with_suffix(".tmpl")
        else:
            dest_path = dest_path.with_suffix(".tmpl")
            
        if dest_path.exists():
            continue

        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, 'w') as f:
            f.write(content + "\n")
        print(f"   [Created] {dest_path.relative_to(REPO_ROOT)}")
        new_files += 1

    print(f"✅ Complete. Created {new_files} new wrappers. Skipped {skipped_files} existing.")

if __name__ == "__main__":
    if not SOURCE_ROOT.exists():
        print(f"❌ Error: Submodule not found at {SOURCE_ROOT}")
        exit(1)
    generate_wrappers()