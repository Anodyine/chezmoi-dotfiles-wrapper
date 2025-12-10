# strategies/symlink.py
from pathlib import Path
from .base import FileStrategy

class SymlinkStrategy(FileStrategy):
    def process(self, source_file: Path, repo_root: Path):
        # Path relative to repo root for the symlink target
        include_path = source_file.relative_to(repo_root)

        # --- Destination Logic (Same as Text) ---
        parts = source_file.parts
        try:
            idx = parts.index('dotfiles')
            rel_parts = parts[idx+1:]
        except ValueError:
            rel_parts = source_file.relative_to(repo_root / "vendor/ml4w").parts

        dest_parts = []
        for part in rel_parts:
            if part.startswith('.'):
                dest_parts.append('dot_' + part[1:])
            else:
                dest_parts.append(part)
        
        dest_path = repo_root.joinpath(*dest_parts)
        
        # Symlink files in chezmoi start with symlink_
        dest_path = dest_path.with_name(f"symlink_{dest_path.name}.tmpl")
        
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        with open(dest_path, 'w') as f:
            # We use sourceDir to ensure absolute path correctness on the target machine
            f.write(f'{{{{ .chezmoi.sourceDir }}}}/{include_path}\n')
            
        print(f"   [Symlink] {dest_path.relative_to(repo_root)}")